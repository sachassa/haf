"""coverage_check(커버리지 축 4 결정적 체커) 오프라인 테스트.

stdlib unittest 만 쓴다(형제 `orchestration/adapters/claude/tests/` 관례 정합·오프라인·실 LLM 0).
검증 축은 `discovery/adapters/claude/coverage-ledger.schema.md` 「판정 규칙」 표 6행 + 「판정 불가는
통과가 아니다」 + 「원장 부재」 절의 열거에서 도출했다(축 발명 0).

음성 케이스(표 행 ↔ 테스트):
  행1 원장에 축 부재        → N1  미심문과 동치
  행2 status=unasked        → N2
  행3 excluded 요건 미충족  → N3a(reason 공백)·N3b(confirmedBy 부재)
  행4 highImpact + excluded → N4  surfacedAt 부재
  행5 interrogated + 추론/가정 → N5a(inferred)·N5b(assumed)·N5c(등급 부재)
  행6 정책에 없는 id        → N6  미상응
  (문면 미명시) 원장 중복 id → N7  중복 위반 — 보고에 명시한 해석 지점
  상태 어휘 밖             → N8

양성:  P1 전 축 interrogated(user-stated) · P2 고임팩트 축 정당 제외(surfacedAt 동반)
fail-closed: F1 원장 부재 · F2 손상 JSON · F3 정책 coverage 절 부재 · F4 정책 부재 ·
             F5 axes 비목록 · F6 원장 최상위 비매핑
회귀:  R1 실 정책 2종 적재 성공(축 집합 동일) · R2 두 프로파일 동일 판정(통과·차단 양방향)
CLI:   C1 통과 exit 0 · C2 차단 exit 2 · C3 사용법 오류 exit 2 · C4 순수 판독(입력 무변)

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
_CHECKER = _MODULE_DIR / "coverage_check.py"
_POLICY_DIR = _REPO / "uahf/framework/adapters/claude/discovery-data/policy"
_REAL_POLICIES = [_POLICY_DIR / "default-policy.yaml", _POLICY_DIR / "lightweight-policy.yaml"]

sys.path.insert(0, str(_MODULE_DIR))
import coverage_check  # noqa: E402  (경로 주입 후 import — 어댑터 로컬 모듈)


# 합성 정책의 축 id 는 **테스트 소유 값**이다(실 정책 축 id 의 사본이 아니다 — 사본 금지 규율).
_AX_A = "test-axis-alpha"
_AX_B = "test-axis-bravo"
_AX_HI = "test-axis-highimpact"


def _synthetic_policy_yaml() -> str:
    return (
        "policyId: synthetic-policy\n"
        "coverage:\n"
        "  requiredAxes:\n"
        "    - id: %s\n      label: 알파\n      dimension: intent\n      highImpact: false\n"
        "    - id: %s\n      label: 브라보\n      dimension: risk\n      highImpact: false\n"
        "    - id: %s\n      label: 고임팩트\n      dimension: architecture\n      highImpact: true\n"
        % (_AX_A, _AX_B, _AX_HI)
    )


def _ledger(axes: list) -> dict:
    return {
        "schema": "coverage-ledger/v1",
        "mode": "greenfield",
        "runId": "test-run",
        "policyRef": "synthetic",
        "axes": axes,
    }


def _ok(axis_id: str) -> dict:
    return {"id": axis_id, "status": "interrogated", "evidenceGrade": "user-stated"}


class _Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="coverage-check-test-"))
        self.policy = self.tmp / "synthetic-policy.yaml"
        self.policy.write_text(_synthetic_policy_yaml(), encoding="utf-8")
        self.ledger = self.tmp / "coverage-ledger.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_ledger(self, axes: list) -> Path:
        self.ledger.write_text(
            json.dumps(_ledger(axes), ensure_ascii=False, indent=1), encoding="utf-8"
        )
        return self.ledger

    def run_check(self, axes: list) -> list:
        return coverage_check.check_coverage(self.policy, self.write_ledger(axes))

    def all_ok(self) -> list:
        return [_ok(_AX_A), _ok(_AX_B), _ok(_AX_HI)]


class TestNegative(_Base):
    """판정 규칙 표의 각 행이 실제로 차단하는지(음성 케이스)."""

    def test_N1_axis_absent_from_ledger(self) -> None:
        errors = self.run_check([_ok(_AX_A), _ok(_AX_HI)])
        self.assertTrue(any(_AX_B in e and "미심문" in e for e in errors), errors)

    def test_N2_unasked(self) -> None:
        errors = self.run_check([_ok(_AX_A), {"id": _AX_B, "status": "unasked"}, _ok(_AX_HI)])
        # 사유까지 대조한다 — 어휘 밖 status 로 오분류되면(catch-all 로 흘러가면) 차단은 되지만
        # 사유가 틀린다. 차단 여부만 보면 그 오분류를 놓친다(변이 M7 실측).
        self.assertTrue(any(_AX_B in e and "status=unasked" in e for e in errors), errors)

    def test_N3a_excluded_blank_reason(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), {"id": _AX_B, "status": "excluded", "reason": "   ",
                          "confirmedBy": "user"}, _ok(_AX_HI)]
        )
        self.assertTrue(any(_AX_B in e and "reason" in e for e in errors), errors)

    def test_N3b_excluded_missing_confirmed_by(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), {"id": _AX_B, "status": "excluded", "reason": "해당 없음"}, _ok(_AX_HI)]
        )
        self.assertTrue(any(_AX_B in e and "confirmedBy" in e for e in errors), errors)

    def test_N4_high_impact_excluded_without_surfaced_at(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), _ok(_AX_B),
             {"id": _AX_HI, "status": "excluded", "reason": "해당 없음", "confirmedBy": "user"}]
        )
        self.assertTrue(
            any(_AX_HI in e and "surfacedAt" in e for e in errors), errors
        )
        # 대조: 같은 형태라도 highImpact 가 아닌 축이면 surfacedAt 없이 통과해야 한다(과잉 차단 방지).
        ok_errors = self.run_check(
            [_ok(_AX_A),
             {"id": _AX_B, "status": "excluded", "reason": "해당 없음", "confirmedBy": "user"},
             _ok(_AX_HI)]
        )
        self.assertEqual(ok_errors, [])

    def test_N5a_interrogated_inferred(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), {"id": _AX_B, "status": "interrogated", "evidenceGrade": "inferred"},
             _ok(_AX_HI)]
        )
        self.assertTrue(any(_AX_B in e and "inferred" in e for e in errors), errors)

    def test_N5b_interrogated_assumed(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), {"id": _AX_B, "status": "interrogated", "evidenceGrade": "assumed"},
             _ok(_AX_HI)]
        )
        self.assertTrue(any(_AX_B in e and "assumed" in e for e in errors), errors)

    def test_N5c_interrogated_missing_grade(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), {"id": _AX_B, "status": "interrogated"}, _ok(_AX_HI)]
        )
        self.assertTrue(any(_AX_B in e for e in errors), errors)

    def test_N6_unmatched_id_in_ledger(self) -> None:
        errors = self.run_check(self.all_ok() + [_ok("test-axis-not-in-policy")])
        self.assertTrue(
            any("test-axis-not-in-policy" in e and "미상응" in e for e in errors), errors
        )

    def test_N7_duplicate_id_in_ledger(self) -> None:
        errors = self.run_check([_ok(_AX_A), _ok(_AX_A), _ok(_AX_B), _ok(_AX_HI)])
        self.assertTrue(any(_AX_A in e and "중복" in e for e in errors), errors)

    def test_N8_unknown_status(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), {"id": _AX_B, "status": "skipped"}, _ok(_AX_HI)]
        )
        self.assertTrue(any(_AX_B in e for e in errors), errors)

    def test_N9_malformed_axis_entries(self) -> None:
        errors = self.run_check([_ok(_AX_A), "문자열", {"status": "interrogated"}, _ok(_AX_HI)])
        self.assertTrue(len(errors) >= 3, errors)  # 비매핑 + id 부재 + 미심문 2축(B·HI 중 B)


class TestPositive(_Base):
    def test_P1_all_interrogated(self) -> None:
        self.assertEqual(self.run_check(self.all_ok()), [])

    def test_P2_high_impact_excluded_with_surfaced_at(self) -> None:
        errors = self.run_check(
            [_ok(_AX_A), _ok(_AX_B),
             {"id": _AX_HI, "status": "excluded", "reason": "외부 전달 표면 0으로 확정",
              "confirmedBy": "user", "surfacedAt": "Eliciting 중 즉시 제시"}]
        )
        self.assertEqual(errors, [])

    def test_P3_deterministic(self) -> None:
        axes = [_ok(_AX_A), {"id": _AX_B, "status": "unasked"}, _ok(_AX_HI)]
        first = coverage_check.check_coverage(self.policy, self.write_ledger(axes))
        second = coverage_check.check_coverage(self.policy, self.ledger)
        self.assertEqual(first, second)


class TestFailClosed(_Base):
    """판정 불가는 통과가 아니다 — 부재·손상·절 부재는 전부 비영(오류 비공집합)."""

    def test_F1_ledger_absent(self) -> None:
        errors = coverage_check.check_coverage(self.policy, self.tmp / "no-such-ledger.json")
        self.assertTrue(errors)
        self.assertTrue(any("부재" in e for e in errors), errors)

    def test_F2_corrupt_json(self) -> None:
        self.ledger.write_text("{ this is not json", encoding="utf-8")
        errors = coverage_check.check_coverage(self.policy, self.ledger)
        self.assertTrue(errors)
        # 손상을 "axes 공집합"으로 관대 해석하면 차단은 되나 사유가 '전 축 미심문'으로 바뀐다
        # — 판독 실패 사실이 은폐된다. 사유까지 대조한다(변이 M10 실측).
        self.assertTrue(any("판독 실패" in e for e in errors), errors)

    def test_F3_policy_without_coverage_section(self) -> None:
        p = self.tmp / "no-coverage.yaml"
        p.write_text("policyId: x\nbudget:\n  total: 40\n", encoding="utf-8")
        errors = coverage_check.check_coverage(p, self.write_ledger(self.all_ok()))
        self.assertTrue(errors)
        # 절 부재와 타입 위반을 구분해 사유까지 대조한다(변이 M9 실측).
        self.assertTrue(any("coverage 절이 없다" in e for e in errors), errors)

    def test_F4_policy_absent(self) -> None:
        errors = coverage_check.check_coverage(
            self.tmp / "no-such-policy.yaml", self.write_ledger(self.all_ok())
        )
        self.assertTrue(errors)

    def test_F5_axes_not_a_list(self) -> None:
        self.ledger.write_text(
            json.dumps({"schema": "coverage-ledger/v1", "axes": {}}), encoding="utf-8"
        )
        self.assertTrue(coverage_check.check_coverage(self.policy, self.ledger))

    def test_F6_ledger_top_not_mapping(self) -> None:
        self.ledger.write_text("[]", encoding="utf-8")
        self.assertTrue(coverage_check.check_coverage(self.policy, self.ledger))

    def test_F7_empty_ledger_axes_is_not_pass(self) -> None:
        # 공집합 axes 를 "제외 0·미심문 0"으로 해석하는 경로가 없는지(침묵 생략 재생산 방지).
        errors = self.run_check([])
        self.assertEqual(len(errors), 3)  # 합성 정책 3축 전부 미심문.

    def test_F8_policy_axis_without_high_impact(self) -> None:
        p = self.tmp / "no-highimpact.yaml"
        p.write_text(
            "coverage:\n  requiredAxes:\n    - id: %s\n      label: 알파\n" % _AX_A,
            encoding="utf-8",
        )
        self.assertTrue(coverage_check.check_coverage(p, self.write_ledger([_ok(_AX_A)])))


class TestRealPolicies(_Base):
    """실 정책 2종 회귀 — 적재 성공 + 두 프로파일 동일 판정(축 집합 동일이므로)."""

    def _axes_of(self, policy: Path) -> list:
        axes, errors = coverage_check.load_policy_axes(policy)
        self.assertEqual(errors, [], "%s 적재 오류" % policy)
        self.assertTrue(axes, "%s 축 0건" % policy)
        return axes

    def test_R1_real_policies_load(self) -> None:
        for p in _REAL_POLICIES:
            self.assertTrue(p.exists(), p)
            self._axes_of(p)

    def test_R2_two_profiles_identical_verdict(self) -> None:
        sets = [self._axes_of(p) for p in _REAL_POLICIES]
        self.assertEqual(sets[0], sets[1], "두 프로파일 축 집합이 다르다")

        # 양성 — 실 정책 축 전부를 interrogated 로 채운 원장(축 id 는 데이터에서 파생·사본 0).
        full = self.write_ledger([_ok(a["id"]) for a in sets[0]])
        verdicts_pass = [coverage_check.check_coverage(p, full) for p in _REAL_POLICIES]
        self.assertEqual(verdicts_pass[0], [])
        self.assertEqual(verdicts_pass[0], verdicts_pass[1])

        # 음성 — 첫 축을 unasked 로 되돌린 원장도 두 프로파일에서 동일 판정.
        broken_axes = [_ok(a["id"]) for a in sets[0]]
        broken_axes[0] = {"id": sets[0][0]["id"], "status": "unasked"}
        broken = self.write_ledger(broken_axes)
        verdicts_fail = [coverage_check.check_coverage(p, broken) for p in _REAL_POLICIES]
        self.assertTrue(verdicts_fail[0])
        self.assertEqual(verdicts_fail[0], verdicts_fail[1])

    def test_R3_high_impact_axis_exists_in_real_policy(self) -> None:
        # 정책 데이터에 highImpact 축이 실재해야 행4 분기가 실 데이터에서도 도달 가능하다.
        for p in _REAL_POLICIES:
            self.assertTrue(any(a["highImpact"] for a in self._axes_of(p)), p)


class TestCli(_Base):
    def _run(self, args: list) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(_CHECKER), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )

    def test_C1_pass_exit_zero(self) -> None:
        r = self._run([str(self.policy), str(self.write_ledger(self.all_ok()))])
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_C2_block_exit_two(self) -> None:
        r = self._run([str(self.policy), str(self.write_ledger([]))])
        self.assertEqual(r.returncode, 2)
        self.assertIn("COVERAGE-INCOMPLETE", r.stderr)

    def test_C3_usage_error(self) -> None:
        self.assertEqual(self._run([str(self.policy)]).returncode, 2)

    def test_C4_pure_read(self) -> None:
        led = self.write_ledger([{"id": _AX_A, "status": "unasked"}])
        before_p, before_l = self.policy.read_bytes(), led.read_bytes()
        names_before = sorted(x.name for x in self.tmp.iterdir())
        self._run([str(self.policy), str(led)])
        self.assertEqual(self.policy.read_bytes(), before_p)
        self.assertEqual(led.read_bytes(), before_l)
        self.assertEqual(sorted(x.name for x in self.tmp.iterdir()), names_before)


# ==========================================================================
# D — 어휘 드리프트 대조 (코드 상수 ↔ 스키마 문서 문자열)
#
# 축 실값(id·label·highImpact)은 정책 데이터가 소유하지만, **상태 어휘**와 **근거 등급 어휘**는
# 전 Strategy 공통 정본(02 §3.12·schema.md)이라 스키마 문서와 코드 상수가 함께 소유한다.
# 두 표면이 말없이 어긋나면 문서가 허용한 값을 코드가 미심문으로 계수하거나 그 반대가 된다.
# 선례 = orchestration/framework/orchestrator/tests/test_gates.py
#         ::test_schema_defaults_match_code_fallbacks(스키마 default ↔ 코드 fallback 대조).
# ==========================================================================
_SCHEMA_MD = _MODULE_DIR / "coverage-ledger.schema.md"


def _quoted_values_after_key(text: str, key: str) -> set:
    """schema.md jsonc 블록에서 `"<key>": "a" | "b" | ...` 행의 값 어휘를 추출한다."""
    import re
    m = re.search(r'"%s"\s*:\s*(.+)' % re.escape(key), text)
    if m is None:
        return set()
    # 행 끝 주석(//) 이후는 어휘가 아니다.
    line = m.group(1).split("//")[0]
    return set(re.findall(r'"([^"]+)"', line))


class TestVocabularyDrift(unittest.TestCase):
    """schema.md 문자열과 coverage_check.py 상수의 어휘가 정확히 일치하는지 대조."""

    @classmethod
    def setUpClass(cls) -> None:
        if not _SCHEMA_MD.exists():
            raise unittest.SkipTest("schema.md 부재: %s" % _SCHEMA_MD)
        cls.text = _SCHEMA_MD.read_text(encoding="utf-8")

    def test_D1_status_vocabulary_matches_schema_block(self) -> None:
        doc = _quoted_values_after_key(self.text, "status")
        self.assertEqual(doc, set(coverage_check._KNOWN_STATUS),
                         "상태 어휘 드리프트 — schema.md 스키마 블록 %r vs 코드 %r"
                         % (sorted(doc), sorted(coverage_check._KNOWN_STATUS)))

    def test_D2_grade_vocabulary_matches_schema_block(self) -> None:
        doc = _quoted_values_after_key(self.text, "evidenceGrade")
        self.assertEqual(doc, set(coverage_check._KNOWN_GRADES),
                         "근거 등급 어휘 드리프트 — schema.md %r vs 코드 %r"
                         % (sorted(doc), sorted(coverage_check._KNOWN_GRADES)))

    def test_D3_status_vocabulary_matches_prose_table(self) -> None:
        # 두 번째 문서 표면(「상태 어휘」 표)도 같은 3값이어야 한다 — 단일 대리 지표 회피.
        import re
        seg = self.text.split("### 상태 어휘", 1)
        self.assertEqual(len(seg), 2, "schema.md 에 「상태 어휘」 절이 없다")
        body = seg[1].split("###", 1)[0]
        rows = set(re.findall(r"^\|\s*`([a-z-]+)`\s*\|", body, flags=re.M))
        self.assertEqual(rows, set(coverage_check._KNOWN_STATUS),
                         "상태 어휘 표 드리프트 — 표 %r vs 코드 %r"
                         % (sorted(rows), sorted(coverage_check._KNOWN_STATUS)))

    def test_D4_non_satisfying_grades_are_subset_and_documented(self) -> None:
        non_sat = set(coverage_check._NON_SATISFYING_GRADES)
        self.assertTrue(non_sat < set(coverage_check._KNOWN_GRADES),
                        "충족 불가 등급은 등급 어휘의 진부분집합이어야 한다")
        # 문서가 그 두 등급을 "심문됨의 근거가 되지 못한다"로 명시하는지 대조.
        for g in sorted(non_sat):
            self.assertIn(g, self.text, "충족 불가 등급 %r 이 schema.md 에 없다" % g)
        # 유일한 충족 등급이 문서의 심문됨 근거 등급과 일치한다.
        satisfying = set(coverage_check._KNOWN_GRADES) - non_sat
        self.assertEqual(satisfying, {coverage_check._GRADE_USER_STATED})

    def test_D5_duplicate_id_contract_is_documented(self) -> None:
        # ① 중복 축 id 계약이 스키마 문서에 명시됐는지(코드가 계약을 앞서지 않게 하는 고정).
        self.assertIn("축 id 중복", self.text)
        self.assertIn("상태 판정은 수행하지 않는다", self.text)


if __name__ == "__main__":
    unittest.main()
