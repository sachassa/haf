"""pretooluse_coverage_guard(커버리지 축 4 PreToolUse 백스톱) 오프라인 테스트.

stdlib unittest 만 쓴다(형제 `orchestration/adapters/claude/tests/test_pretooluse_design_guard.py`
관례 정합·오프라인·실 LLM 0). 라이브 차단 실증을 대체하지 않는다 — 실제 도구 호출 차단은 별도로
수행했고(훅이 죽어도 도구 호출은 조용히 통과하므로 단위 검증으로 갈음 불가), 본 파일은 스코프
판정·경로 해소·fail 경계의 회귀 고정을 담당한다.

검증 축:
  S — 스코프: Contract 파일명 관례에만 반응하고 그 밖은 no-op. 쓰기 계열 도구만 대상.
  L — 원장 해소: Contract 와 같은 디렉터리 병치. 부재·손상은 차단(체커 fail-closed 보존).
  P — 정책 해소: policyRef → <ref>-policy.yaml. 부재·비문자열·경로 이탈은 차단.
  V — 판정 위임: 미심문 있으면 차단·미심문 0 이면 통과(판정은 check_coverage 소유).
  O — 훅 자신의 결함은 fail-open(자기-DoS 방지).
  T — Write·Edit·MultiEdit 세 도구 전부 포섭(경로 앵커 방식의 핵심 이득).

픽스처는 테스트가 tempfile 로 만들고 tearDown 에서 지운다(리포에 잔재 0).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]              # discovery/adapters/claude
_REPO = _TEST_FILE.parents[4]                    # 저장소 루트
_GUARD = _MODULE_DIR / "pretooluse_coverage_guard.py"
_POLICY_DIR = _REPO / "uahf/framework/adapters/claude/discovery-data/policy"

sys.path.insert(0, str(_MODULE_DIR))
import pretooluse_coverage_guard as guard  # noqa: E402


def _real_axis_ids() -> list:
    """실 정책의 축 id 를 데이터에서 읽는다(사본 금지 규율 — 코드에 축 실값을 두지 않는다)."""
    import yaml
    doc = yaml.safe_load((_POLICY_DIR / "default-policy.yaml").read_text(encoding="utf-8"))
    return [a["id"] for a in doc["coverage"]["requiredAxes"]]


class _Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cov-guard-"))
        self.cdir = self.tmp / ".claude" / "project-contract"
        self.cdir.mkdir(parents=True)
        self.contract = self.cdir / "project-contract.v1.md"
        self.ledger = self.cdir / "coverage-ledger.json"
        self.axis_ids = _real_axis_ids()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_ledger(self, axes, policy_ref="default", **extra) -> None:
        doc = {"schema": "coverage-ledger/v1", "mode": "greenfield", "runId": "t-001",
               "policyRef": policy_ref, "axes": axes}
        doc.update(extra)
        self.ledger.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")

    def all_interrogated(self) -> list:
        return [{"id": i, "status": "interrogated", "evidenceGrade": "user-stated"}
                for i in self.axis_ids]

    def invoke(self, path, tool="Write") -> str:
        """훅을 in-process 로 호출하고 stdout(deny JSON 또는 빈 문자열)을 반환한다."""
        import io
        payload = json.dumps({"tool_name": tool, "cwd": str(self.tmp),
                              "tool_input": {"file_path": str(path), "content": "x",
                                             "new_string": "y"}})
        buf, err = io.StringIO(), io.StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = buf, err
        try:
            rc = guard.run(payload)
        finally:
            sys.stdout, sys.stderr = old_out, old_err
        self.assertEqual(rc, 0, "PreToolUse 계약상 exit 는 항상 0 이어야 한다")
        return buf.getvalue()

    def assertDenied(self, out, needle=None) -> None:
        self.assertTrue(out.strip(), "차단이 기대됐으나 no-op 통과했다")
        doc = json.loads(out)
        hs = doc["hookSpecificOutput"]
        self.assertEqual(hs["hookEventName"], "PreToolUse")
        self.assertEqual(hs["permissionDecision"], "deny")
        if needle:
            self.assertIn(needle, hs["permissionDecisionReason"])

    def assertAllowed(self, out) -> None:
        self.assertEqual(out, "", "no-op 통과가 기대됐으나 차단됐다: %s" % out)


class TestScope(_Base):
    """S — 무관한 Write 를 막으면 세션이 마비된다. 스코프는 좁고 결정적이어야 한다."""

    def test_S1_unrelated_files_are_noop(self) -> None:
        self.write_ledger([])  # 원장이 비어 있어도(= 차단 상태) 스코프 밖이면 통과해야 한다.
        for name in ("README.md", "settings.json", "project-contract.md",
                     "project-contract.v1.txt", "my-project-contract.v1.md",
                     "project-contract.vX.md", "coverage-ledger.json"):
            self.assertAllowed(self.invoke(self.cdir / name))

    def test_S2_contract_name_variants_are_scoped(self) -> None:
        self.write_ledger([])
        for name in ("project-contract.v1.md", "project-contract.v2.md",
                     "project-contract.v42.md"):
            self.assertDenied(self.invoke(self.cdir / name))

    def test_S3_non_write_tools_are_noop(self) -> None:
        self.write_ledger([])
        for tool in ("Read", "Bash", "Glob", "Grep", "NotebookEdit"):
            self.assertAllowed(self.invoke(self.contract, tool=tool))

    def test_S4_missing_file_path_is_noop(self) -> None:
        out = guard.run(json.dumps({"tool_name": "Write", "tool_input": {}}))
        self.assertEqual(out, 0)


class TestToolCoverage(_Base):
    """T — 경로 앵커 방식의 핵심 이득: 세 쓰기 도구가 동일하게 포섭된다.

    내용 파싱 방식이었다면 Write 만 전문을 주므로 Edit/MultiEdit 가 조용히 통과했을 것이다.
    """

    def test_T1_all_write_tools_blocked(self) -> None:
        self.write_ledger([{"id": self.axis_ids[0], "status": "unasked"}])
        for tool in ("Write", "Edit", "MultiEdit"):
            self.assertDenied(self.invoke(self.contract, tool=tool), needle="COVERAGE-INCOMPLETE")

    def test_T2_all_write_tools_allowed_when_complete(self) -> None:
        self.write_ledger(self.all_interrogated())
        for tool in ("Write", "Edit", "MultiEdit"):
            self.assertAllowed(self.invoke(self.contract, tool=tool))


class TestLedgerResolution(_Base):
    """L — 원장은 Contract 와 같은 디렉터리. 부재·손상은 통과가 아니다(fail-closed 보존)."""

    def test_L1_absent_ledger_blocks(self) -> None:
        self.assertDenied(self.invoke(self.contract), needle="원장 부재")

    def test_L2_corrupt_ledger_blocks(self) -> None:
        self.ledger.write_text("{ not json", encoding="utf-8")
        self.assertDenied(self.invoke(self.contract), needle="판독 실패")

    def test_L3_ledger_not_mapping_blocks(self) -> None:
        self.ledger.write_text("[1, 2, 3]", encoding="utf-8")
        self.assertDenied(self.invoke(self.contract))

    def test_L4_sibling_directory_ledger_is_not_used(self) -> None:
        # 다른 디렉터리의 원장이 새어 들어오지 않는다(도출은 같은 디렉터리로 확정).
        other = self.tmp / "elsewhere"
        other.mkdir()
        (other / "coverage-ledger.json").write_text(
            json.dumps({"schema": "coverage-ledger/v1", "policyRef": "default",
                        "axes": self.all_interrogated()}), encoding="utf-8")
        self.assertDenied(self.invoke(self.contract), needle="원장 부재")


class TestPolicyResolution(_Base):
    """P — 원장이 선언한 정책으로 판정한다. 다른 정책으로 대체하면 조용한 드리프트다."""

    def test_P1_missing_policy_ref_blocks(self) -> None:
        self.ledger.write_text(json.dumps({"schema": "coverage-ledger/v1", "axes": []}),
                               encoding="utf-8")
        self.assertDenied(self.invoke(self.contract), needle="policyRef")

    def test_P2_blank_policy_ref_blocks(self) -> None:
        self.write_ledger([], policy_ref="   ")
        self.assertDenied(self.invoke(self.contract), needle="policyRef")

    def test_P3_unresolvable_policy_ref_blocks(self) -> None:
        self.write_ledger(self.all_interrogated(), policy_ref="no-such-profile")
        self.assertDenied(self.invoke(self.contract), needle="해소 실패")

    def test_P4_path_traversal_ref_rejected(self) -> None:
        for bad in ("../default", "a/b", "..\\x", ".."):
            self.write_ledger([], policy_ref=bad)
            self.assertDenied(self.invoke(self.contract))

    def test_P5_lightweight_profile_resolves(self) -> None:
        # 두 프로파일 모두 해소되고 동일 축 집합이므로 동일 판정이 나온다(§8.3 (b) coverage 행).
        self.write_ledger(self.all_interrogated(), policy_ref="lightweight")
        self.assertAllowed(self.invoke(self.contract))


class TestVerdictDelegation(_Base):
    """V — 판정은 check_coverage 소유. 훅은 그 결과를 그대로 표면화한다."""

    def test_V1_unasked_blocks_and_names_axis(self) -> None:
        axes = self.all_interrogated()
        axes[0] = {"id": self.axis_ids[0], "status": "unasked"}
        self.write_ledger(axes)
        self.assertDenied(self.invoke(self.contract), needle=self.axis_ids[0])

    def test_V2_inferred_grade_blocks(self) -> None:
        axes = self.all_interrogated()
        axes[1]["evidenceGrade"] = "inferred"
        self.write_ledger(axes)
        self.assertDenied(self.invoke(self.contract))

    def test_V3_complete_ledger_allows(self) -> None:
        self.write_ledger(self.all_interrogated())
        self.assertAllowed(self.invoke(self.contract))

    def test_V4_empty_axes_blocks(self) -> None:
        # 빈 원장은 "제외 0·미심문 0" 이 아니다 — 정책 축 전건이 미심문으로 계수된다.
        self.write_ledger([])
        self.assertDenied(self.invoke(self.contract))

    def test_V5_deterministic(self) -> None:
        self.write_ledger([{"id": self.axis_ids[0], "status": "unasked"}])
        self.assertEqual(self.invoke(self.contract), self.invoke(self.contract))


class TestFailOpen(_Base):
    """O — 훅 **자신의** 결함만 fail-open. 체커의 fail-closed 와 섞지 않는다."""

    def test_O1_malformed_stdin_is_fail_open(self) -> None:
        import io
        for raw in ("{ not json", "", "[1,2]", "null"):
            buf, err = io.StringIO(), io.StringIO()
            old_out, old_err = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = buf, err
            try:
                rc = guard.run(raw)
            finally:
                sys.stdout, sys.stderr = old_out, old_err
            self.assertEqual(rc, 0)
            self.assertEqual(buf.getvalue(), "", "훅 자신의 결함은 차단하지 않는다(자기-DoS 방지)")

    def test_O2_pure_read_no_mutation(self) -> None:
        self.write_ledger([{"id": self.axis_ids[0], "status": "unasked"}])
        before = self.ledger.read_bytes()
        names_before = sorted(p.name for p in self.cdir.iterdir())
        self.invoke(self.contract)
        self.assertEqual(self.ledger.read_bytes(), before)
        self.assertEqual(sorted(p.name for p in self.cdir.iterdir()), names_before)
        self.assertFalse(self.contract.exists(), "훅이 대상 파일을 생성해서는 안 된다")


class TestCliContract(_Base):
    """서브프로세스 경로 — 실제 배선 형태(stdin → stdout JSON · exit 0)로도 동작하는지."""

    def _run(self, payload: dict):
        return subprocess.run([sys.executable, str(_GUARD)],
                              input=json.dumps(payload), capture_output=True,
                              text=True, encoding="utf-8", cwd=str(_REPO))

    def test_C1_subprocess_deny(self) -> None:
        self.write_ledger([{"id": self.axis_ids[0], "status": "unasked"}])
        r = self._run({"tool_name": "Write", "cwd": str(self.tmp),
                       "tool_input": {"file_path": str(self.contract), "content": "x"}})
        self.assertEqual(r.returncode, 0)
        self.assertEqual(
            json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_C2_subprocess_allow(self) -> None:
        self.write_ledger(self.all_interrogated())
        r = self._run({"tool_name": "Write", "cwd": str(self.tmp),
                       "tool_input": {"file_path": str(self.contract), "content": "x"}})
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")


class TestWiring(unittest.TestCase):
    """배선 회귀 — settings.json 에 상대경로로 등재돼 있는지($CLAUDE_PROJECT_DIR 금지)."""

    def test_W1_registered_in_settings_with_relative_path(self) -> None:
        settings = json.loads((_REPO / ".claude/settings.json").read_text(encoding="utf-8"))
        cmds = [h["command"]
                for block in settings["hooks"]["PreToolUse"]
                for h in block["hooks"]]
        mine = [c for c in cmds if "pretooluse_coverage_guard.py" in c]
        self.assertEqual(len(mine), 1, "커버리지 가드가 PreToolUse 에 정확히 1건 등재돼야 한다")
        self.assertNotIn("CLAUDE_PROJECT_DIR", mine[0],
                         "이 환경의 PreToolUse 훅에서 $CLAUDE_PROJECT_DIR 은 차단을 내지 못한다")
        self.assertIn("discovery/adapters/claude/pretooluse_coverage_guard.py", mine[0])

    def test_W2_matcher_covers_all_write_tools(self) -> None:
        settings = json.loads((_REPO / ".claude/settings.json").read_text(encoding="utf-8"))
        blocks = [b for b in settings["hooks"]["PreToolUse"]
                  if any("pretooluse_coverage_guard.py" in h["command"] for h in b["hooks"])]
        self.assertEqual(len(blocks), 1)
        for tool in ("Write", "Edit", "MultiEdit"):
            self.assertIn(tool, blocks[0]["matcher"])

    def test_W3_guard_file_exists(self) -> None:
        self.assertTrue(_GUARD.exists())


if __name__ == "__main__":
    unittest.main()
