"""pretooluse_design_guard (§DC-3 존재 최후방어 백스톱) 오프라인 테스트 — stdlib unittest.

가드를 **subprocess**(sys.executable 로 guard.py 실행·stdin 에 JSON 주입)로 구동해 실제
stdin/stdout PreToolUse 계약을 검증한다(형제 test_resolve_gate.py 관례 정합·오프라인·실 LLM 0).

케이스:
  A 차단(manifest 부재)   : W/src/foo.py Write → deny·exit 0.
  B 차단(침묵 누락)        : manifest 있으나 required 미산출 → deny.
  C 허용(설계 완료)        : required 전부 produced/정당화 제외 → deny 없음·exit 0.
  D no-op(비-src)          : W/docs/foo.md Write(설계 미완이어도) → deny 없음.
  E no-op(비게이트)        : solution-design/ 없는 디렉터리의 src/foo.py → deny 없음.
  F fail-open(깨진 stdin)  : 비-JSON stdin → exit 0·deny 없음.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# 가드 스크립트 경로(형제 모듈 디렉터리 = orchestration/adapters/claude).
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]
_GUARD = _MODULE_DIR / "pretooluse_design_guard.py"


# always 6종만 required(touchpoint/interface 미선언) 최소 유효 정책 — test_resolve_gate 동형.
_POLICY = {
    "projectionSelection": {
        "requirementClasses": {
            "always": "항상 required",
            "touchpoint": "접점 선언 시 required",
            "interface": "연계 선언 시 required",
        },
        "defaultRequiredSet": [
            {"id": "project-plan", "name": "프로젝트 계획서", "requirement": "always"},
        ],
        "exclusionRule": {"silentOmission": "금지"},
    }
}

# required(project-plan) 산출 완료 매니페스트 — touchpoint/interface 항목이 정책에 없으므로
# 클래스 전체 제외 표면화도 불필요(always 1종만).
_MANIFEST_OK = {
    "declaredTouchpoints": [],
    "declaredInterfaces": [],
    "artifacts": [{"id": "project-plan", "status": "produced"}],
}


def _write_policy(workspace: Path) -> None:
    """워크스페이스 SD 정책(YAML)을 시드한다(게이트-소비 프로젝트 앵커)."""
    import yaml  # 체커와 동일 로컬 라이브러리.

    pol = workspace / ".claude" / "solution-design" / "policy"
    pol.mkdir(parents=True, exist_ok=True)
    (pol / "default-policy.yaml").write_text(
        yaml.safe_dump(_POLICY, allow_unicode=True), encoding="utf-8"
    )


def _write_manifest(workspace: Path, manifest) -> None:
    sd = workspace / ".claude" / "solution-design"
    sd.mkdir(parents=True, exist_ok=True)
    (sd / "design-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
    )


def _run_guard(payload, *, raw: str = None):
    """가드를 subprocess 로 구동. payload(dict) 또는 raw(문자열) stdin 주입 → (rc, stdout, stderr)."""
    stdin = raw if raw is not None else json.dumps(payload, ensure_ascii=False)
    proc = subprocess.run(
        [sys.executable, str(_GUARD)],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return proc.returncode, proc.stdout, proc.stderr


def _decision(stdout: str):
    """stdout 에서 permissionDecision 을 추출한다. 무출력/파싱 불가면 None(=deny 아님)."""
    s = stdout.strip()
    if not s:
        return None
    try:
        doc = json.loads(s)
    except ValueError:
        return None
    return (doc.get("hookSpecificOutput") or {}).get("permissionDecision")


class TestPreToolUseDesignGuard(unittest.TestCase):
    def _payload(self, workspace: Path, rel_file: str, tool: str = "Write"):
        return {
            "tool_name": tool,
            "tool_input": {"file_path": str(workspace / rel_file)},
            "cwd": str(workspace),
        }

    # --- A: manifest 부재 → 차단 --------------------------------------------------
    def test_A_missing_manifest_denies_src_write(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "proj"
            _write_policy(ws)  # 정책만·매니페스트 없음.
            rc, out, err = _run_guard(self._payload(ws, "src/foo.py"))
            self.assertEqual(rc, 0, err)
            self.assertEqual(_decision(out), "deny", "manifest 부재는 src/ Write 차단: %r" % out)

    # --- B: 침묵 누락 → 차단 ------------------------------------------------------
    def test_B_silent_omission_denies(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "proj"
            _write_policy(ws)
            # manifest 는 있으나 required(project-plan) 미산출(빈 artifacts).
            _write_manifest(ws, {"declaredTouchpoints": [], "declaredInterfaces": [],
                                 "artifacts": []})
            rc, out, err = _run_guard(self._payload(ws, "src/foo.py"))
            self.assertEqual(rc, 0, err)
            self.assertEqual(_decision(out), "deny", "침묵 누락은 차단: %r" % out)

    # --- C: 설계 완료 → 허용 ------------------------------------------------------
    def test_C_complete_design_allows(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "proj"
            _write_policy(ws)
            _write_manifest(ws, _MANIFEST_OK)
            rc, out, err = _run_guard(self._payload(ws, "src/foo.py"))
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out), "설계 완료는 deny 없음(무출력): %r" % out)

    def test_C_justified_exclusion_allows(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "proj"
            _write_policy(ws)
            _write_manifest(ws, {"declaredTouchpoints": [], "declaredInterfaces": [],
                                 "artifacts": [{"id": "project-plan", "status": "excluded",
                                                "reason": "범위 밖", "confirmedBy": "user"}]})
            rc, out, err = _run_guard(self._payload(ws, "src/foo.py"))
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out), "정당화 제외는 deny 없음: %r" % out)

    # --- D: 비-src → no-op -------------------------------------------------------
    def test_D_non_src_path_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "proj"
            _write_policy(ws)  # 매니페스트 부재(설계 미완) — 그래도 비-src 는 통과.
            rc, out, err = _run_guard(self._payload(ws, "docs/foo.md"))
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out), "비-src 는 no-op(deny 없음): %r" % out)

    def test_D_nested_src_still_guarded(self):
        # 세그먼트 매칭 실증 — packages/x/src/foo.py 는 여전히 포섭·차단(설계 미완).
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "proj"
            _write_policy(ws)  # 매니페스트 부재.
            rc, out, err = _run_guard(self._payload(ws, "packages/x/src/foo.py"))
            self.assertEqual(rc, 0, err)
            self.assertEqual(_decision(out), "deny", "중첩 src/ 도 포섭·차단: %r" % out)

    # --- E: 비게이트(solution-design/ 없음) → no-op ------------------------------
    def test_E_non_gate_workspace_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "plain"
            (ws / "src").mkdir(parents=True)
            # solution-design/ 없음 → 게이트-소비 프로젝트 아님.
            rc, out, err = _run_guard(self._payload(ws, "src/foo.py"))
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out), "비게이트 워크스페이스는 no-op: %r" % out)

    # --- F: 깨진 stdin → fail-open -----------------------------------------------
    def test_F_broken_stdin_fail_open(self):
        rc, out, err = _run_guard(None, raw="이건 JSON 이 아니다 {{{")
        self.assertEqual(rc, 0, "fail-open 은 exit 0")
        self.assertIsNone(_decision(out), "fail-open 은 deny 없음(무출력): %r" % out)

    # --- 보강: 비-쓰기 도구 → no-op ----------------------------------------------
    def test_non_write_tool_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "proj"
            _write_policy(ws)  # 설계 미완이지만 Read 는 대상 아님.
            payload = {"tool_name": "Read", "tool_input": {"file_path": str(ws / "src/foo.py")},
                       "cwd": str(ws)}
            rc, out, err = _run_guard(payload)
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out), "비-쓰기 도구는 no-op: %r" % out)


if __name__ == "__main__":
    unittest.main()
