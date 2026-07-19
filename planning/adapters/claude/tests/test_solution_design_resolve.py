"""solution_design_resolve (산출물 생산 프로토콜 form-B 로더) 오프라인 테스트 — 실 LLM/소환 0(stdlib unittest).

위임 명세(⑤)의 최소 케이스를 실제 코드로 뒷받침한다:
  - 접점 선언 O → 디자이너 활성·screen-list/menu-structure/screen-design required=true·owner=디자이너.
  - 접점 선언 X → 디자이너 excludedConditional·위 3종 required=false·classExclusions.touchpoint placeholder.
  - 연계 선언 O/X → interface-spec required true/false 대응.
  - --data-complex O → DBA 활성 / X → DBA excludedConditional.
  - always 6종 항상 required·owner 정확.
  - 결정성: 같은 입력 2회 호출 → 동일 JSON.
  - 실 정책(default-policy.yaml) 기반 스모크 1건.

이 로더는 실행 호스팅 0(subagent spawn·Agent/Task 호출 0)·순수 판독·결정적이다.
"""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

# --- 경로 배선: 로더 모듈 디렉터리 -------------------------------------------
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]          # planning/adapters/claude
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import solution_design_resolve as sdr  # noqa: E402

# 실 정책 파일(현행 물리 위치 — binding §12·2차 디커플링 트랙에서 확정).
_REPO_ROOT = _TEST_FILE.parents[4]
_REAL_POLICY = (_REPO_ROOT / "uahf" / "framework" / "adapters" / "claude"
                / "solution-design-data" / "policy" / "default-policy.yaml")


# 테스트 픽스처 정책(실 정책 스키마 동형·자기완결 — 실 파일 의존 최소화).
def _fixture_policy() -> dict:
    return {
        "policyId": "test-policy",
        "roleSelection": {
            "wholeScopeCoverage": "required",
            "maxSpecialistRoles": 4,
            "fixedTeam": "금지",
            "defaultComposition": {
                "coverageFloor": "PM",
                "baseSpecialists": ["기획", "아키텍처"],
                "conditionalSpecialists": [
                    {"role": "디자이너", "when": "접점 선언 시", "whenSignal": "touchpoint"},
                    {"role": "DBA", "when": "데이터 복잡 시", "whenSignal": "dataComplex"},
                ],
            },
        },
        "projectionSelection": {
            "requirementClasses": {
                "always": "항상",
                "touchpoint": "접점 선언 시",
                "interface": "연계 선언 시",
            },
            "defaultRequiredSet": [
                {"id": "project-plan", "name": "프로젝트 계획서", "requirement": "always"},
                {"id": "requirements-def", "name": "요구사항 정의서", "requirement": "always"},
                {"id": "business-process", "name": "업무 프로세스", "requirement": "always"},
                {"id": "functional-spec", "name": "기능 명세서", "requirement": "always"},
                {"id": "table-def", "name": "테이블 정의서", "requirement": "always"},
                {"id": "test-plan-cases", "name": "테스트 계획·케이스", "requirement": "always"},
                {"id": "screen-list", "name": "화면 목록", "requirement": "touchpoint"},
                {"id": "menu-structure", "name": "메뉴 구조도", "requirement": "touchpoint"},
                {"id": "screen-design", "name": "화면 설계서", "requirement": "touchpoint"},
                {"id": "interface-spec", "name": "인터페이스 명세서", "requirement": "interface"},
            ],
        },
        "artifactOwnership": [
            {"id": "project-plan", "owner": "PM"},
            {"id": "requirements-def", "owner": "기획"},
            {"id": "business-process", "owner": "기획"},
            {"id": "functional-spec", "owner": "기획"},
            {"id": "test-plan-cases", "owner": "기획"},
            {"id": "table-def", "owner": "아키텍처", "assist": "DBA"},
            {"id": "interface-spec", "owner": "아키텍처"},
            {"id": "screen-list", "owner": "디자이너"},
            {"id": "menu-structure", "owner": "디자이너"},
            {"id": "screen-design", "owner": "디자이너"},
        ],
    }


_ALWAYS_IDS = ["project-plan", "requirements-def", "business-process",
               "functional-spec", "table-def", "test-plan-cases"]
_TOUCHPOINT_IDS = ["screen-list", "menu-structure", "screen-design"]


def _plan_by_id(result: dict) -> dict:
    return {p["id"]: p for p in result["artifactPlan"]}


class TouchpointDeclaredTest(unittest.TestCase):
    def setUp(self):
        self.res = sdr.resolve(_fixture_policy(), ["웹"], [], False)

    def test_designer_activated(self):
        activated = [a["role"] for a in self.res["roleComposition"]["activatedConditional"]]
        self.assertIn("디자이너", activated)
        self.assertIn("디자이너", self.res["roleComposition"]["roles"])

    def test_touchpoint_artifacts_required_and_owned(self):
        by_id = _plan_by_id(self.res)
        for tid in _TOUCHPOINT_IDS:
            self.assertTrue(by_id[tid]["required"], tid)
            self.assertEqual(by_id[tid]["owner"], "디자이너", tid)

    def test_roles_order_preserved(self):
        # coverageFloor + base + activated(정책 입력순) — 디자이너만 활성(DBA 미활성).
        self.assertEqual(self.res["roleComposition"]["roles"],
                         ["PM", "기획", "아키텍처", "디자이너"])


class TouchpointAbsentTest(unittest.TestCase):
    def setUp(self):
        self.res = sdr.resolve(_fixture_policy(), [], [], False)

    def test_designer_excluded(self):
        excluded = [e["role"] for e in self.res["roleComposition"]["excludedConditional"]]
        self.assertIn("디자이너", excluded)
        self.assertNotIn("디자이너", self.res["roleComposition"]["roles"])

    def test_touchpoint_artifacts_not_required(self):
        by_id = _plan_by_id(self.res)
        for tid in _TOUCHPOINT_IDS:
            self.assertFalse(by_id[tid]["required"], tid)
            self.assertIn("classExclusions.touchpoint", by_id[tid]["note"])

    def test_class_exclusion_placeholder_present(self):
        cx = self.res["manifestScaffold"]["classExclusions"]
        self.assertIn("touchpoint", cx)
        self.assertEqual(cx["touchpoint"], {"reason": "", "confirmedBy": ""})

    def test_scaffold_artifacts_only_required(self):
        ids = [a["id"] for a in self.res["manifestScaffold"]["artifacts"]]
        self.assertEqual(set(ids), set(_ALWAYS_IDS))
        for a in self.res["manifestScaffold"]["artifacts"]:
            self.assertEqual(a["status"], "pending")


class InterfaceDeclarationTest(unittest.TestCase):
    def test_interface_required_when_declared(self):
        res = sdr.resolve(_fixture_policy(), [], ["결제게이트웨이"], False)
        by_id = _plan_by_id(res)
        self.assertTrue(by_id["interface-spec"]["required"])
        self.assertEqual(by_id["interface-spec"]["owner"], "아키텍처")
        self.assertNotIn("interface", res["manifestScaffold"]["classExclusions"])

    def test_interface_not_required_when_absent(self):
        res = sdr.resolve(_fixture_policy(), [], [], False)
        by_id = _plan_by_id(res)
        self.assertFalse(by_id["interface-spec"]["required"])
        self.assertIn("interface", res["manifestScaffold"]["classExclusions"])


class DataComplexTest(unittest.TestCase):
    def test_dba_activated_when_data_complex(self):
        res = sdr.resolve(_fixture_policy(), [], [], True)
        activated = [a["role"] for a in res["roleComposition"]["activatedConditional"]]
        self.assertIn("DBA", activated)
        self.assertIn("DBA", res["roleComposition"]["roles"])

    def test_dba_excluded_when_not_data_complex(self):
        res = sdr.resolve(_fixture_policy(), [], [], False)
        excluded = [e["role"] for e in res["roleComposition"]["excludedConditional"]]
        self.assertIn("DBA", excluded)


class AlwaysClassTest(unittest.TestCase):
    def test_always_six_required_regardless_of_signals(self):
        for tp, iface, dc in [([], [], False), (["웹"], ["x"], True)]:
            res = sdr.resolve(_fixture_policy(), tp, iface, dc)
            by_id = _plan_by_id(res)
            for aid in _ALWAYS_IDS:
                self.assertTrue(by_id[aid]["required"], (aid, tp, iface, dc))

    def test_always_owner_accuracy(self):
        res = sdr.resolve(_fixture_policy(), [], [], False)
        by_id = _plan_by_id(res)
        self.assertEqual(by_id["project-plan"]["owner"], "PM")
        self.assertEqual(by_id["requirements-def"]["owner"], "기획")
        self.assertEqual(by_id["table-def"]["owner"], "아키텍처")


class DeterminismTest(unittest.TestCase):
    def test_same_input_same_output(self):
        p = _fixture_policy()
        r1 = sdr.resolve(copy.deepcopy(p), ["웹", "앱"], ["결제"], True)
        r2 = sdr.resolve(copy.deepcopy(p), ["웹", "앱"], ["결제"], True)
        self.assertEqual(r1, r2)


class WhenSignalErrorTest(unittest.TestCase):
    def test_unknown_when_signal_raises(self):
        p = _fixture_policy()
        p["roleSelection"]["defaultComposition"]["conditionalSpecialists"][0]["whenSignal"] = "미지신호"
        with self.assertRaises(sdr.PolicyError):
            sdr.resolve(p, ["웹"], [], False)

    def test_missing_owner_raises(self):
        p = _fixture_policy()
        p["artifactOwnership"] = [e for e in p["artifactOwnership"] if e["id"] != "project-plan"]
        with self.assertRaises(sdr.PolicyError):
            sdr.resolve(p, [], [], False)


class RealPolicySmokeTest(unittest.TestCase):
    def test_real_policy_touchpoint_declared(self):
        self.assertTrue(_REAL_POLICY.exists(), "실 정책 파일 부재: %s" % _REAL_POLICY)
        policy = sdr.load_policy(_REAL_POLICY)
        res = sdr.resolve(policy, ["웹"], ["외부API"], True)
        # 실 정책 = 10 산출물·5 역할(PM·기획·아키텍처·디자이너·DBA 활성).
        self.assertEqual(len(res["artifactPlan"]), 10)
        self.assertEqual(res["roleComposition"]["roles"],
                         ["PM", "기획", "아키텍처", "디자이너", "DBA"])
        by_id = _plan_by_id(res)
        self.assertTrue(all(by_id[i]["required"] for i in _ALWAYS_IDS))
        self.assertTrue(by_id["interface-spec"]["required"])

    def test_real_policy_minimal_signals(self):
        policy = sdr.load_policy(_REAL_POLICY)
        res = sdr.resolve(policy, [], [], False)
        self.assertEqual(res["roleComposition"]["roles"], ["PM", "기획", "아키텍처"])
        cx = res["manifestScaffold"]["classExclusions"]
        self.assertIn("touchpoint", cx)
        self.assertIn("interface", cx)


if __name__ == "__main__":
    unittest.main()
