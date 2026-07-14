"""Dynamic Allocation·Model Selection·CP3 정지 테스트 (표준 라이브러리 unittest 만).

allocation.py 순수 테스트 + orchestrator 통합 테스트(모의 invoker)를 한 파일에 둔다
(S2 test_orchestrator.py·S3 test_gates.py·test_revision.py 무손상 — done 8).

커버(위임 done 1~9·설계 §5 S4 시나리오 f/g/h + CP3 정지 i + tie-break j):
  - AgentSpec 7필드·3층 구분·매칭 deterministic (05 §3.4 일치·done 2)
  - (f) capability class 상이 두 단위 → 상이 모델 슬롯 직렬화·InvokeRequest 전달 실측
  - (g) 정상 재실행 재선택 없음 + retry 한도 도달에서만 fallback 차상위(hysteresis·done 3)
  - (h) CP2 Verifier 모델 독립 지정(orchestrator 경유 StepHost 전달·OQ-SH-4)
  - (i) CP3 비-Pass 정지·적격 해소 재개(status 소비·PO-INV 1·done 5)
  - (j) tie-break: 구체 selector 우선·version 우선 각각(05 §9 OQ 8 S4 확정)
  - PO-INV 6: 매칭기는 capability 선언까지만 소비·AgentSpec 물리 매핑 해석 0(불투명·done 9)

모델 슬롯은 전부 불투명 문자열(tier-a 등)이다 — 실제 모델명 토큰 0(PO-INV 8·done 6).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

_ORCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ORCH_DIR not in sys.path:
    sys.path.insert(0, _ORCH_DIR)

import allocation as allocation_mod  # noqa: E402
from allocation import (  # noqa: E402
    Allocation,
    AgentSpec,
    AgentSpecRegistry,
    ModelSelectionPolicy,
    RESELECTION_TRIGGER_KINDS,
    TRIGGER_MODEL_POLICY_EVENT,
    TRIGGER_RETRY_LIMIT,
)
from gates import (  # noqa: E402
    GATE_APPROVAL_REQUIRED,
    GATE_ESCALATION_REQUIRED,
    GatePolicy,
    GatePolicyEntry,
    append_gate_resolution,
)
from orchestrator import ProjectOrchestrator  # noqa: E402
from revision import InMemoryRevisionStore, RevisionLedger  # noqa: E402
from stephost_bridge import (  # noqa: E402
    InMemoryEventStore,
    Invoker,
    InvokeResult,
    KIND_COMPLETION,
    PASSED,
    ROLE_ADVISOR,
    ROLE_VERIFIER,
    ROLE_WORKER,
)


# --------------------------------------------------------------------------
# 픽스처 — 모델 슬롯 없는 Task(allocation 이 채움) + 모델 캡처 invoker
# --------------------------------------------------------------------------
def alloc_task(tid, capability, depends_on=None):
    """model 슬롯을 두지 않은 Task — allocation 이 직렬화 시점에 채운다(명시값 부재)."""
    return {
        "id": tid,
        "task": "unit " + tid,
        "done": "AC-" + tid,
        "interfaceContract": {"produces": ["c-" + tid]},
        "ownedBoundary": ["file-" + tid],
        "dependsOn": list(depends_on or []),
        "delegation": {
            "from": "Advisor", "to": "Worker", "task": "impl",
            "input": "in-" + tid, "output": "out-" + tid, "done": "AC-" + tid,
            "context": ["doc"], "constraints": None,
        },
        "capability": capability,
        # role·model 슬롯 없음(allocation 이 채운다).
    }


def _completion(step_id):
    return InvokeResult(
        kind=KIND_COMPLETION,
        completion={"artifacts": ["art-" + str(step_id)], "self_check": "done",
                    "failures": "없음", "open_questions": "없음", "verify_basis": "self"},
        ref="wr",
    )


def _verdict(passed=True, rework=None):
    return InvokeResult(kind=KIND_COMPLETION,
                        completion={"verdict": "Pass" if passed else "Fail", "rework": rework},
                        ref="vd")


class ModelCapturingInvoker(Invoker):
    """Worker=완료 / Verifier·Advisor=verdict. 각 호출의 model 슬롯을 기록한다.

    worker/verifier/advisor 스크립트로 시나리오별 반환을 지정한다(중립 stub·provider 0).
    """

    def __init__(self, worker=None, verifier=None, advisor_default=None):
        self.worker = {k: list(v) for k, v in (worker or {}).items()}
        self.verifier = {k: list(v) for k, v in (verifier or {}).items()}
        self.advisor_default = advisor_default  # 게이트 CP3 반환(비-Pass 실증용).
        self.calls = []  # {role, step_id, model, is_gate}

    def invoke(self, request):
        step_id = (request.bundle.get("step_contract") or {}).get("id")
        is_gate = "gate" in request.bundle
        self.calls.append({"role": request.role, "step_id": step_id,
                           "model": request.model, "is_gate": is_gate})
        if request.role == ROLE_ADVISOR:
            return self.advisor_default if self.advisor_default is not None else _verdict(True)
        if request.role == ROLE_VERIFIER:
            script = self.verifier.get(step_id)
            if script:
                return script.pop(0)
            return _verdict(True)
        script = self.worker.get(step_id)
        if script:
            return script.pop(0)
        return _completion(step_id)

    def models_for(self, role, step_id=None, gate=None):
        return [c["model"] for c in self.calls
                if c["role"] == role
                and (step_id is None or c["step_id"] == step_id)
                and (gate is None or c["is_gate"] == gate)]


def build_orch(tasks, allocation=None, gate_policy=None, retry_limit=2, invoker=None):
    store = InMemoryEventStore()
    graph = {"goal": "g", "tasks": tasks, "completion": "all-passed"}
    ledger = RevisionLedger(InMemoryRevisionStore(), graph)
    inv = invoker if invoker is not None else ModelCapturingInvoker()
    orch = ProjectOrchestrator(ledger, store, inv, retry_limit=retry_limit,
                               gate_policy=gate_policy, allocation=allocation)
    return orch, inv, store


def demo_allocation(cp2_slot=None):
    """불투명 슬롯만 쓰는 데모 allocation — 실제 모델명 0(PO-INV 8)."""
    registry = AgentSpecRegistry([
        AgentSpec(specId="spec-mech", capabilitySelector="cap-mech",
                  modelPolicyClass="mechanical", version=1),
        AgentSpec(specId="spec-design", capabilitySelector="cap-design",
                  modelPolicyClass="design", version=1),
    ])
    policy = ModelSelectionPolicy(
        slots={"mechanical": "tier-a", "design": "tier-c"},
        fallback_chain=["tier-a", "tier-b", "tier-c", "tier-d"],
        cp2_slot=cp2_slot,
    )
    return Allocation(registry=registry, model_policy=policy)


# ==========================================================================
# AgentSpec — 7필드·3층 구분·직렬화 (05 §3.4 — done 2)
# ==========================================================================
class AgentSpecRecord(unittest.TestCase):
    def test_seven_fields_roundtrip(self):
        spec = AgentSpec(
            specId="s1", capabilitySelector={"domain": "d"}, briefTemplateRef="tref",
            defaultConstraints={"c": 1}, toolPolicyClass="tool-x",
            modelPolicyClass="mech", version=3,
        )
        d = spec.to_dict()
        self.assertEqual(
            set(d.keys()),
            {"specId", "capabilitySelector", "briefTemplateRef", "defaultConstraints",
             "toolPolicyClass", "modelPolicyClass", "version"},
        )
        self.assertEqual(AgentSpec.from_dict(d), spec)

    def test_from_dict_requires_spec_id(self):
        with self.assertRaises(ValueError):
            AgentSpec.from_dict({"capabilitySelector": "x"})


# ==========================================================================
# capability 매칭 deterministic + tie-break (j) (05 §3.4·§9 OQ 8)
# ==========================================================================
class MatchingAndTieBreak(unittest.TestCase):
    def test_no_match_returns_none(self):
        reg = AgentSpecRegistry([AgentSpec(specId="a", capabilitySelector="cap-x")])
        self.assertIsNone(reg.match("cap-other"))

    def test_wildcard_matches_anything(self):
        reg = AgentSpecRegistry([AgentSpec(specId="a", capabilitySelector="*")])
        self.assertEqual(reg.match("anything").specId, "a")

    def test_dict_selector_matches_by_all_constraints(self):
        reg = AgentSpecRegistry([
            AgentSpec(specId="a", capabilitySelector={"domain": "d", "kind": "k"}),
        ])
        self.assertEqual(reg.match({"domain": "d", "kind": "k", "x": 1}).specId, "a")
        self.assertIsNone(reg.match({"domain": "d"}))  # kind 불일치.

    def test_tie_break_more_specific_selector_wins(self):
        # j: 구체 selector 우선 — "*"(특이도 0) vs 정확 "cap-x"(특이도 1) → 정확 선택.
        reg = AgentSpecRegistry([
            AgentSpec(specId="wild", capabilitySelector="*", version=9),
            AgentSpec(specId="exact", capabilitySelector="cap-x", version=1),
        ])
        self.assertEqual(reg.match("cap-x").specId, "exact")  # 높은 version 이어도 특이도 우선.

    def test_tie_break_highest_version_when_equal_specificity(self):
        # j: 같은 특이도 → 최고 version 선택.
        reg = AgentSpecRegistry([
            AgentSpec(specId="v1", capabilitySelector="cap-x", version=1),
            AgentSpec(specId="v2", capabilitySelector="cap-x", version=2),
        ])
        self.assertEqual(reg.match("cap-x").specId, "v2")

    def test_tie_break_is_deterministic_and_data_overridable(self):
        # 기본(specificity 우선) 오버라이드 → version 우선. 데이터로 규칙 교체 가능.
        specs = [
            AgentSpec(specId="wild", capabilitySelector="*", version=5),
            AgentSpec(specId="exact", capabilitySelector="cap-x", version=1),
        ]
        default = AgentSpecRegistry(specs)  # specificity 우선.
        self.assertEqual(default.match("cap-x").specId, "exact")
        override = AgentSpecRegistry(specs, tie_break=("version", "specificity"))
        self.assertEqual(override.match("cap-x").specId, "wild")  # version 우선.

    def test_true_tie_resolved_by_spec_id_stable(self):
        # 모든 차원 동률 → specId 사전순으로 결정적(진짜 동률에서도 안정).
        reg = AgentSpecRegistry([
            AgentSpec(specId="b", capabilitySelector="cap-x", version=1),
            AgentSpec(specId="a", capabilitySelector="cap-x", version=1),
        ])
        self.assertEqual(reg.match("cap-x").specId, "a")
        self.assertEqual(reg.match("cap-x").specId, "a")  # 반복 결정성.

    def test_unknown_tie_break_dim_rejected(self):
        with self.assertRaises(ValueError):
            AgentSpecRegistry([], tie_break=("bogus",))


# ==========================================================================
# ModelSelectionPolicy — select_model·fallback·cp2 (05 §3.5)
# ==========================================================================
class ModelSelection(unittest.TestCase):
    def test_base_selection_by_class(self):
        pol = ModelSelectionPolicy(slots={"mech": "tier-a", "design": "tier-c"})
        self.assertEqual(pol.select_model("mech"), "tier-a")
        self.assertEqual(pol.select_model("design"), "tier-c")

    def test_unknown_class_uses_default_slot(self):
        pol = ModelSelectionPolicy(slots={"mech": "tier-a"}, default_slot="tier-x")
        self.assertEqual(pol.select_model("unknown"), "tier-x")
        self.assertIsNone(ModelSelectionPolicy(slots={}).select_model("unknown"))

    def test_fallback_advances_along_chain_and_clamps(self):
        pol = ModelSelectionPolicy(
            slots={"mech": "tier-a"}, fallback_chain=["tier-a", "tier-b", "tier-c"])
        self.assertEqual(pol.select_model("mech", 0), "tier-a")
        self.assertEqual(pol.select_model("mech", 1), "tier-b")
        self.assertEqual(pol.select_model("mech", 2), "tier-c")
        self.assertEqual(pol.select_model("mech", 9), "tier-c")  # clamp 끝.

    def test_base_outside_chain_does_not_reselect(self):
        # base 가 체인 밖 → fallback 미정의 → 재선택 없음(추측 금지·O4).
        pol = ModelSelectionPolicy(slots={"mech": "tier-z"}, fallback_chain=["tier-a", "tier-b"])
        self.assertEqual(pol.select_model("mech", 3), "tier-z")

    def test_cp2_slot(self):
        self.assertIsNone(ModelSelectionPolicy().cp2_model())
        self.assertEqual(ModelSelectionPolicy(cp2_slot="tier-v").cp2_model(), "tier-v")

    def test_cp2_model_for_overrides_and_fallback(self):
        # W2-3 가법 확장: capability class 별 CP2 오버라이드 우선·없으면 전역 cp2_slot 폴백.
        pol = ModelSelectionPolicy(
            cp2_slot="tier-vglobal",
            cp2_slots={"mech": "tier-vmech", "design": "tier-vdesign"},
        )
        self.assertEqual(pol.cp2_model_for("mech"), "tier-vmech")
        self.assertEqual(pol.cp2_model_for("design"), "tier-vdesign")
        self.assertEqual(pol.cp2_model_for("unknown"), "tier-vglobal")  # 미매칭 → 전역 폴백.
        self.assertEqual(pol.cp2_model_for(None), "tier-vglobal")
        self.assertTrue(pol.has_cp2_overrides())

    def test_cp2_slots_empty_preserves_global_single(self):
        # 오버라이드 없음(기본) → 항상 전역 cp2_slot(전역 단일 거동 보존·무회귀).
        pol = ModelSelectionPolicy(cp2_slot="tier-v")
        self.assertEqual(pol.cp2_model_for("mech"), "tier-v")
        self.assertFalse(pol.has_cp2_overrides())
        # cp2_slot 도 None 이면 항상 None(Host 상속).
        self.assertIsNone(ModelSelectionPolicy().cp2_model_for("mech"))

    def test_select_model_is_pure(self):
        pol = ModelSelectionPolicy(slots={"mech": "tier-a"}, fallback_chain=["tier-a", "tier-b"])
        self.assertEqual(pol.select_model("mech", 1), pol.select_model("mech", 1))


class AllocationLoaders(unittest.TestCase):
    def test_from_dict_roundtrip(self):
        data = {
            "registry": {
                "specs": [{"specId": "s1", "capabilitySelector": "cap-x",
                           "modelPolicyClass": "mech", "version": 2}],
                "tieBreak": ["specificity", "version"],
            },
            "modelSelection": {
                "slots": {"mech": "tier-a"},
                "fallbackChain": ["tier-a", "tier-b"],
                "cp2ModelSlot": "tier-v",
            },
        }
        alloc = Allocation.from_dict(data)
        self.assertEqual(alloc.match("cap-x").specId, "s1")
        self.assertEqual(alloc.model_for("cap-x"), "tier-a")
        self.assertEqual(alloc.model_for("cap-x", 1), "tier-b")
        self.assertEqual(alloc.cp2_model(), "tier-v")

    def test_from_dict_reads_cp2_model_slots(self):
        # W2-3: cp2ModelSlots(가법) 로드 + Allocation.cp2_model_for capability 경유 해석.
        data = {
            "registry": {"specs": [{"specId": "s1", "capabilitySelector": "cap-x",
                                    "modelPolicyClass": "mech", "version": 1}]},
            "modelSelection": {
                "slots": {"mech": "tier-a"},
                "cp2ModelSlot": "tier-vglobal",
                "cp2ModelSlots": {"mech": "tier-vmech"},
            },
        }
        alloc = Allocation.from_dict(data)
        self.assertTrue(alloc.has_cp2_overrides())
        self.assertEqual(alloc.cp2_model_for("cap-x"), "tier-vmech")   # class mech 오버라이드.
        self.assertEqual(alloc.cp2_model_for("cap-none"), "tier-vglobal")  # 미매칭 → 전역 폴백.
        # cp2ModelSlots 미지정(하위호환) → 오버라이드 없음.
        alloc2 = Allocation.from_dict({
            "registry": {"specs": [{"specId": "s", "capabilitySelector": "*", "modelPolicyClass": "m"}]},
            "modelSelection": {"slots": {"m": "tier-a"}, "cp2ModelSlot": "tier-v"},
        })
        self.assertFalse(alloc2.has_cp2_overrides())
        self.assertEqual(alloc2.cp2_model_for("anything"), "tier-v")

    def test_from_file_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "alloc.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({
                    "registry": {"specs": [{"specId": "s", "capabilitySelector": "*",
                                            "modelPolicyClass": "m"}]},
                    "modelSelection": {"slots": {"m": "tier-a"}},
                }, fh)
            alloc = Allocation.from_file(path)
            self.assertEqual(alloc.model_for("whatever"), "tier-a")

    def test_model_for_none_when_no_match_or_no_class(self):
        # 매칭 실패 → None.
        alloc = Allocation(AgentSpecRegistry([]), ModelSelectionPolicy(slots={"m": "tier-a"}))
        self.assertIsNone(alloc.model_for("x"))
        # 매칭하나 modelPolicyClass 부재 → None(불투명 키 없음).
        alloc2 = Allocation(
            AgentSpecRegistry([AgentSpec(specId="s", capabilitySelector="*")]),
            ModelSelectionPolicy(slots={"m": "tier-a"}))
        self.assertIsNone(alloc2.model_for("x"))


# ==========================================================================
# (f) capability class 상이 → 상이 모델 슬롯 직렬화·InvokeRequest 전달 실측
# ==========================================================================
class ScenarioF_DistinctModelPerCapabilityClass(unittest.TestCase):
    def test_distinct_slots_recorded_and_passed_to_invoker(self):
        tasks = [alloc_task("u1", "cap-mech"), alloc_task("u2", "cap-design", depends_on=["u1"])]
        orch, inv, store = build_orch(tasks, allocation=demo_allocation())
        result = orch.run()
        self.assertTrue(result.completed, result.status)

        # 직렬화 시점 슬롯이 각 단위 capability class 별로 상이(Worker InvokeRequest 실측).
        self.assertEqual(inv.models_for(ROLE_WORKER, "u1"), ["tier-a"])
        self.assertEqual(inv.models_for(ROLE_WORKER, "u2"), ["tier-c"])
        # Step 직렬화 뷰(active_graph → _build_steps)에도 동일 슬롯이 기록된다.
        steps = {s.id: s for s in orch._build_steps(orch.active_graph())}
        self.assertEqual(steps["u1"].model, "tier-a")
        self.assertEqual(steps["u2"].model, "tier-c")

    def test_explicit_model_slot_is_respected_over_allocation(self):
        # 이미 채워진 Step 슬롯은 존중(명시값 우선) — allocation 이 덮어쓰지 않는다.
        task = alloc_task("u1", "cap-mech")
        task["model"] = "explicit-tier"
        orch, inv, store = build_orch([task], allocation=demo_allocation())
        orch.run()
        self.assertEqual(inv.models_for(ROLE_WORKER, "u1"), ["explicit-tier"])


# ==========================================================================
# (g) hysteresis — 정상 재실행 재선택 없음 + retry 한도 도달에서만 fallback (done 3)
# ==========================================================================
class ScenarioG_Hysteresis(unittest.TestCase):
    def test_normal_retry_does_not_reselect_model(self):
        # budget 내 CP2 Fail→재시도: 두 Worker 디스패치 모두 base 슬롯(재선택 없음).
        inv = ModelCapturingInvoker(verifier={"u1": [_verdict(False, rework="다시"), _verdict(True)]})
        orch, inv, store = build_orch([alloc_task("u1", "cap-mech")],
                                      allocation=demo_allocation(), retry_limit=2, invoker=inv)
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        worker_models = inv.models_for(ROLE_WORKER, "u1")
        self.assertEqual(len(worker_models), 2)  # 1차 실패·2차 성공.
        self.assertEqual(worker_models, ["tier-a", "tier-a"])  # 재선택 0.

    def test_fallback_level_counts_only_reselection_triggers(self):
        # done 3: 재선택 트리거는 정확히 2건(retry-limit-exceeded·model-policy-event).
        # 정상 fail 이벤트는 트리거가 아니므로 level 을 올리지 않는다.
        orch, inv, store = build_orch([alloc_task("u1", "cap-mech")], allocation=demo_allocation())
        log = orch.log
        # 평범한 fail(budget 내) — 트리거 아님.
        log.append(cycle_id="u1", to_stage="Verify", trigger="Verify 실패", outcome="fail",
                   actor=ROLE_WORKER, ref={"kind": "failure"})
        self.assertEqual(orch._fallback_level("u1"), 0)
        # (a) retry 한도 도달 에스컬레이션 — 트리거.
        log.append(cycle_id="u1", to_stage="Complete", trigger="에스컬레이션", outcome="escalated",
                   actor="Advisor", ref={"kind": TRIGGER_RETRY_LIMIT, "limit": 2})
        self.assertEqual(orch._fallback_level("u1"), 1)
        # (b) 명시적 모델 정책 이벤트 — 트리거.
        log.append(cycle_id="u1", to_stage="Complete", trigger="정책", outcome="pass",
                   actor="Advisor", ref={"kind": TRIGGER_MODEL_POLICY_EVENT})
        self.assertEqual(orch._fallback_level("u1"), 2)
        # 트리거 목록은 정확히 2종(코드 구조 확인).
        self.assertEqual(set(RESELECTION_TRIGGER_KINDS),
                         {TRIGGER_RETRY_LIMIT, TRIGGER_MODEL_POLICY_EVENT})

    def test_retry_limit_trigger_advances_model_slot(self):
        # retry 한도 도달 이벤트 1건 → 직렬화 슬롯이 fallback 차상위(tier-a → tier-b).
        orch, inv, store = build_orch([alloc_task("u1", "cap-mech")], allocation=demo_allocation())
        # 재선택 전: base 슬롯.
        step0 = orch._build_steps(orch.active_graph())[0]
        self.assertEqual(step0.model, "tier-a")
        # retry 한도 도달 트리거 append → 재선택 차상위.
        orch.log.append(cycle_id="u1", to_stage="Complete", trigger="에스컬레이션",
                        outcome="escalated", actor="Advisor",
                        ref={"kind": TRIGGER_RETRY_LIMIT, "limit": 2})
        step1 = orch._build_steps(orch.active_graph())[0]
        self.assertEqual(step1.model, "tier-b")


# ==========================================================================
# (h) CP2 Verifier 모델 독립 지정 — orchestrator 경유 StepHost 전달 (OQ-SH-4)
# ==========================================================================
class ScenarioH_Cp2ModelIndependence(unittest.TestCase):
    def test_orchestrator_routes_independent_cp2_model_to_verifier(self):
        alloc = demo_allocation(cp2_slot="tier-verify")
        orch, inv, store = build_orch([alloc_task("u1", "cap-mech")], allocation=alloc)
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        # Worker 는 capability 기반 슬롯(tier-a), CP2(Verifier)는 독립 슬롯(tier-verify).
        self.assertEqual(inv.models_for(ROLE_WORKER, "u1"), ["tier-a"])
        self.assertEqual(inv.models_for(ROLE_VERIFIER, "u1"), ["tier-verify"])

    def test_no_cp2_slot_verifier_inherits_step_model(self):
        # cp2_slot 미지정 → CP2 는 대상 step 슬롯 상속(기존 거동·OQ-SH-4 기본).
        orch, inv, store = build_orch([alloc_task("u1", "cap-mech")], allocation=demo_allocation())
        orch.run()
        self.assertEqual(inv.models_for(ROLE_VERIFIER, "u1"), ["tier-a"])


def demo_allocation_cp2_overrides():
    """capability class 별 CP2 오버라이드를 둔 데모 allocation(가법 확장·불투명 슬롯)."""
    registry = AgentSpecRegistry([
        AgentSpec(specId="spec-mech", capabilitySelector="cap-mech",
                  modelPolicyClass="mechanical", version=1),
        AgentSpec(specId="spec-design", capabilitySelector="cap-design",
                  modelPolicyClass="design", version=1),
    ])
    policy = ModelSelectionPolicy(
        slots={"mechanical": "tier-a", "design": "tier-c"},
        fallback_chain=["tier-a", "tier-b", "tier-c", "tier-d"],
        cp2_slot="tier-vglobal",
        cp2_slots={"mechanical": "tier-vmech", "design": "tier-vdesign"},
    )
    return Allocation(registry=registry, model_policy=policy)


class ScenarioH2_DescriptorAwareCp2(unittest.TestCase):
    """W2-3 — descriptor-aware CP2 슬롯: capability class 별로 CP2 모델이 차등된다.

    가법·spec 문면 대조 통과분(05 §3.5 "CP2 = 독립 정책 행" — 전역 단일 계약 아님). 오버라이드가
    없으면 resolver 는 배선되지 않아 기존 (h) 거동이 완전 보존된다(무회귀).
    """

    def test_cp2_model_differs_per_capability_class(self):
        tasks = [alloc_task("u1", "cap-mech"), alloc_task("u2", "cap-design", depends_on=["u1"])]
        orch, inv, store = build_orch(tasks, allocation=demo_allocation_cp2_overrides())
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        # Worker 슬롯은 capability class 기본(불변).
        self.assertEqual(inv.models_for(ROLE_WORKER, "u1"), ["tier-a"])
        self.assertEqual(inv.models_for(ROLE_WORKER, "u2"), ["tier-c"])
        # CP2(Verifier)는 capability class 별 오버라이드(위험도별 차등).
        self.assertEqual(inv.models_for(ROLE_VERIFIER, "u1"), ["tier-vmech"])
        self.assertEqual(inv.models_for(ROLE_VERIFIER, "u2"), ["tier-vdesign"])

    def test_unmatched_capability_falls_back_to_global_cp2(self):
        # 오버라이드 class 밖 capability → 전역 cp2_slot 폴백(resolver 는 배선되나 전역 반환).
        alloc = demo_allocation_cp2_overrides()
        # cap-other 는 어느 AgentSpec 도 매칭하지 않음 → model_for None → step.model 미채움.
        # 명시 model 슬롯을 주어 Worker 는 그 값, CP2 는 전역 cp2 폴백을 검증한다.
        task = alloc_task("u1", "cap-other")
        task["model"] = "explicit"
        orch, inv, store = build_orch([task], allocation=alloc)
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        self.assertEqual(inv.models_for(ROLE_WORKER, "u1"), ["explicit"])
        self.assertEqual(inv.models_for(ROLE_VERIFIER, "u1"), ["tier-vglobal"])

    def test_no_overrides_preserves_existing_cp2_behavior(self):
        # cp2_slots 없음 → resolver 미배선 → (h) 전역 cp2_slot 거동 완전 보존(무회귀).
        orch, inv, store = build_orch([alloc_task("u1", "cap-mech")],
                                      allocation=demo_allocation(cp2_slot="tier-verify"))
        orch.run()
        self.assertEqual(inv.models_for(ROLE_VERIFIER, "u1"), ["tier-verify"])


# ==========================================================================
# (i) CP3 비-Pass 정지·적격 해소 재개 (status 소비·PO-INV 1·done 5)
# ==========================================================================
def approval_policy():
    return GatePolicy(entries=[
        GatePolicyEntry(target={"unitType": "t-approval"}, gate=GATE_APPROVAL_REQUIRED),
    ], user_actor_class="human", escalation_resolvers=("Advisor", "human"))


def approval_task(tid):
    t = alloc_task(tid, "cap-mech")
    t["unitType"] = "t-approval"
    return t


class ScenarioI_Cp3NotPassStops(unittest.TestCase):
    def test_cp3_not_pass_escalates_and_stops_then_resumes(self):
        inv = ModelCapturingInvoker(advisor_default=_verdict(False, rework="설계 재검토"))
        orch, inv, store = build_orch([approval_task("t1")], gate_policy=approval_policy(),
                                      invoker=inv)
        result = orch.run()

        # CP3 비-Pass → escalation 게이트 정지(적격 해소로만 재개).
        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.stop_reason, "gate")
        self.assertEqual([g["gateKind"] for g in result.pending_gates], [GATE_ESCALATION_REQUIRED])
        gid = orch._gate_id_for("t1")
        self.assertEqual(result.pending_gates[0]["gate_id"], gid)
        self.assertEqual(result.pending_gates[0]["scoped_question"]["cause"], "cp3_not_pass")
        # 단위 실행 자체는 완료(정지는 게이트 축) — CP3 는 1회만 디스패치.
        self.assertEqual(orch.derive_states()["t1"], PASSED)
        self.assertEqual(len(inv.models_for(ROLE_ADVISOR, gate=True)), 1)

        # 부적격 actor(Worker) 해소 시도 → 무효(여전히 정지·재디스패치 0).
        append_gate_resolution(orch.log, gid, GATE_ESCALATION_REQUIRED, actor="Worker")
        again = orch.run()
        self.assertTrue(again.stopped, again.status)
        self.assertEqual(len(inv.models_for(ROLE_ADVISOR, gate=True)), 1)  # 멱등.

        # 적격 actor(Advisor) 해소 → 완주.
        append_gate_resolution(orch.log, gid, GATE_ESCALATION_REQUIRED, actor="Advisor")
        done = orch.run()
        self.assertTrue(done.completed, done.status)

    def test_cp3_pass_does_not_stop(self):
        # 대조: CP3 Pass → 정지 없음(기존 approval 거동 보존).
        inv = ModelCapturingInvoker(advisor_default=_verdict(True))
        orch, inv, store = build_orch([approval_task("t1")], gate_policy=approval_policy(),
                                      invoker=inv)
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        self.assertEqual(result.pending_gates, [])


# ==========================================================================
# PO-INV 6 — 매칭기는 capability 선언까지만 소비·물리 매핑 해석 0 (done 9)
# ==========================================================================
class POINV6_OpaqueMapping(unittest.TestCase):
    def test_match_selects_by_capability_only_not_by_opaque_fields(self):
        # briefTemplateRef·defaultConstraints·toolPolicyClass 는 매칭에 관여하지 않는다
        # (capability selector 만 소비). 물리 매핑을 해석하지 않는 불투명 참조다.
        reg = AgentSpecRegistry([
            AgentSpec(specId="a", capabilitySelector="cap-x", briefTemplateRef="brief-A",
                      defaultConstraints={"x": 1}, toolPolicyClass="tool-A", version=1),
            AgentSpec(specId="b", capabilitySelector="cap-x", briefTemplateRef="brief-B",
                      defaultConstraints={"y": 9}, toolPolicyClass="tool-B", version=2),
        ])
        # 두 spec 은 capability selector 만 같다(불투명 필드는 상이). 선택은 version 만으로
        # 결정된다 — 불투명 필드는 매칭·tie-break 에 관여하지 않는다.
        self.assertEqual(reg.match("cap-x").specId, "b")

    def test_model_class_consumed_as_opaque_key(self):
        # modelPolicyClass 는 불투명 정책 클래스 키로만 소비된다(물리 매핑 해석 0).
        # 코드는 그 값의 의미를 모른 채 정책 dict 키로만 쓴다.
        alloc = Allocation(
            AgentSpecRegistry([AgentSpec(specId="s", capabilitySelector="*",
                                         modelPolicyClass="opaque-class-token")]),
            ModelSelectionPolicy(slots={"opaque-class-token": "tier-a"}))
        self.assertEqual(alloc.model_for("anything"), "tier-a")


class SchemaConsistency(unittest.TestCase):
    """스키마 default 가 코드 fallback 과 일치(단일 진리원천 대조·gates 관례 동형)."""

    def test_allocation_schema_tie_break_default_matches_code(self):
        path = os.path.join(_ORCH_DIR, "allocation_schema.json")
        with open(path, "r", encoding="utf-8") as fh:
            schema = json.load(fh)
        default = schema["properties"]["tieBreak"]["default"]
        self.assertEqual(tuple(default), allocation_mod.DEFAULT_TIE_BREAK)

    def test_schemas_are_valid_json(self):
        for name in ("allocation_schema.json", "model_selection_schema.json"):
            path = os.path.join(_ORCH_DIR, name)
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self.assertEqual(data["type"], "object", name)

    def test_model_selection_schema_registers_cp2_model_slots(self):
        path = os.path.join(_ORCH_DIR, "model_selection_schema.json")
        with open(path, "r", encoding="utf-8") as fh:
            schema = json.load(fh)
        # 스키마 property 집합 = from_dict 소비 키 집합(단일 진리원천 대조).
        self.assertEqual(
            set(schema["properties"]),
            {"slots", "fallbackChain", "cp2ModelSlot", "defaultSlot", "cp2ModelSlots"})
        prop = schema["properties"]["cp2ModelSlots"]
        self.assertEqual(prop["type"], "object")
        self.assertEqual(prop["additionalProperties"], {"type": "string"})
        self.assertIs(schema["additionalProperties"], False)  # 가법 등재 후에도 닫힌 스키마 유지.


if __name__ == "__main__":
    unittest.main(verbosity=2)
