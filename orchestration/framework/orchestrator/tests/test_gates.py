"""Gate Policy 평가기·게이트 큐 파생 뷰·orchestrator 게이트 통합 테스트.

표준 라이브러리 unittest 만·외부 의존 0. gates.py 순수 테스트 + orchestrator 통합
테스트(모의 invoker)를 한 파일에 둔다(S2 test_orchestrator.py 무손상 — done 10).

커버(설계 §5 S3 시나리오 + done 1~10):
  - gateKind 5종·심각도 전순서·05 §3.3 표 일치(done 2)
  - floor(코드 소유 하한)·effective_gate 단조성 클램프(약화→하한, done 3)
  - GatePolicy.evaluate 매칭 우선순위·tie-break·JSON 로드
  - pending_gates 파생 뷰·해소 적격성(user_decision=사용자만·done 5·6)
  - 결정성(같은 (정책, 이벤트 로그) → 동일 결과·done 6)
  - (d) 같은 그래프 gateKind별 상이 거동 + 비사용자 해소 무효→사용자 해소 재개
  - (e) Autonomy 직교(unrestricted 에서도 정지 게이트 정지·done 4)

특정 provider·모델·상류 Layer 고유명 토큰을 두지 않는다(PO-INV 8).
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

import gates  # noqa: E402
from gates import (  # noqa: E402
    DEFAULT_ESCALATION_RESOLVERS,
    DEFAULT_USER_ACTOR_CLASS,
    GATE_APPROVAL_REQUIRED,
    GATE_AUTO_CONTINUE,
    GATE_ESCALATION_REQUIRED,
    GATE_KINDS,
    GATE_REVIEW_REQUIRED,
    GATE_USER_DECISION_REQUIRED,
    REF_KIND_APPROVAL,
    REF_KIND_REVIEW,
    GatePolicy,
    GatePolicyEntry,
    append_gate_requirement,
    append_gate_resolution,
    effective_gate,
    floor,
    has_settlement,
    is_resolved,
    max_gate,
    pending_gates,
    severity,
)
from artifacts import InMemoryArtifactDeclarationStore  # noqa: E402
from orchestrator import OrchestrationResult, ProjectOrchestrator  # noqa: E402
from revision import (  # noqa: E402
    InMemoryRevisionStore,
    KIND_DEPENDENCY_ADDED,
    KIND_TASK_ADDED,
    KIND_TASK_SUPERSEDED,
    RevisionLedger,
)
from stephost_bridge import (  # noqa: E402
    EventLog,
    InMemoryEventStore,
    Invoker,
    InvokeResult,
    KIND_COMPLETION,
    PASSED,
    POLICY_INTERACTIVE,
    POLICY_UNRESTRICTED,
    ROLE_ADVISOR,
    ROLE_VERIFIER,
    ROLE_WORKER,
)


# ==========================================================================
# gateKind 5종·심각도 전순서 (05 §3.3 표 정확 일치 — done 2)
# ==========================================================================
class GateKindVocabularyAndSeverity(unittest.TestCase):
    def test_five_kinds_exact(self):
        self.assertEqual(
            GATE_KINDS,
            (
                "auto_continue",
                "review_required",
                "approval_required",
                "escalation_required",
                "user_decision_required",
            ),
        )

    def test_severity_is_strict_total_order(self):
        order = [severity(k) for k in GATE_KINDS]
        self.assertEqual(order, [0, 1, 2, 3, 4])
        # 전순서: auto < review < approval < escalation < user_decision.
        for i in range(len(GATE_KINDS) - 1):
            self.assertLess(severity(GATE_KINDS[i]), severity(GATE_KINDS[i + 1]))

    def test_max_gate_picks_more_severe(self):
        self.assertEqual(max_gate(GATE_AUTO_CONTINUE, GATE_REVIEW_REQUIRED), GATE_REVIEW_REQUIRED)
        self.assertEqual(
            max_gate(GATE_USER_DECISION_REQUIRED, GATE_APPROVAL_REQUIRED),
            GATE_USER_DECISION_REQUIRED,
        )

    def test_unknown_kind_raises(self):
        with self.assertRaises(ValueError):
            severity("not_a_gate")


# ==========================================================================
# floor(코드 소유 하한)·effective_gate 단조성 클램프 (PO-INV 4 — done 3)
# ==========================================================================
class FloorAndMonotonicity(unittest.TestCase):
    def test_floor_execution_initiation_is_user_decision(self):
        self.assertEqual(
            floor({"targetClass": gates.TARGETCLASS_EXECUTION_INITIATION}),
            GATE_USER_DECISION_REQUIRED,
        )

    def test_floor_contract_point_is_user_decision(self):
        self.assertEqual(
            floor({"targetClass": gates.TARGETCLASS_CONTRACT_POINT}),
            GATE_USER_DECISION_REQUIRED,
        )

    def test_floor_intervention_conditions_are_escalation(self):
        for cond in (
            gates.INTERVENTION_BLOCKING,
            gates.INTERVENTION_DEPENDENCY_UNCERTAIN,
            gates.INTERVENTION_ARCHITECTURE_CONFLICT,
            gates.INTERVENTION_ROLE_BOUNDARY_EXCEEDED,
        ):
            self.assertEqual(
                floor({"interventionCondition": cond}), GATE_ESCALATION_REQUIRED, cond
            )

    def test_floor_none_is_auto(self):
        self.assertEqual(floor({}), GATE_AUTO_CONTINUE)
        self.assertEqual(floor({"unitType": "generic"}), GATE_AUTO_CONTINUE)

    def test_effective_clamps_weak_policy_up_to_floor(self):
        # 정책 데이터가 하한 target 에 auto_continue 를 지정 → 하한으로 클램프(약화 불가).
        policy = GatePolicy(entries=[
            GatePolicyEntry(target={"unitType": "launch"}, gate=GATE_AUTO_CONTINUE),
        ])
        descriptor = {
            "unitType": "launch",
            "targetClass": gates.TARGETCLASS_EXECUTION_INITIATION,
        }
        # policy 자체는 auto 를 반환하나 effective 는 floor(user_decision)로 클램프.
        self.assertEqual(policy.evaluate(descriptor), GATE_AUTO_CONTINUE)
        self.assertEqual(effective_gate(descriptor, policy), GATE_USER_DECISION_REQUIRED)

    def test_effective_allows_strengthening_above_floor(self):
        # 정책이 하한보다 강하면(escalation vs 하한 없음) 정책값 채택(강화 가능).
        policy = GatePolicy(entries=[
            GatePolicyEntry(target={"unitType": "risky"}, gate=GATE_ESCALATION_REQUIRED),
        ])
        descriptor = {"unitType": "risky"}  # floor 없음(auto).
        self.assertEqual(effective_gate(descriptor, policy), GATE_ESCALATION_REQUIRED)

    def test_policy_cannot_weaken_intervention_floor(self):
        # 개입 조건(escalation 하한)에 auto 를 지정해도 escalation 으로 클램프.
        policy = GatePolicy(entries=[
            GatePolicyEntry(target={"unitType": "u"}, gate=GATE_REVIEW_REQUIRED),
        ])
        descriptor = {"unitType": "u", "interventionCondition": gates.INTERVENTION_BLOCKING}
        self.assertEqual(effective_gate(descriptor, policy), GATE_ESCALATION_REQUIRED)


# ==========================================================================
# GatePolicy.evaluate — 매칭 우선순위·tie-break·JSON 로드
# ==========================================================================
class GatePolicyEvaluate(unittest.TestCase):
    def test_no_match_is_auto(self):
        self.assertEqual(GatePolicy(entries=[]).evaluate({"unitType": "x"}), GATE_AUTO_CONTINUE)

    def test_global_default_matches_anything(self):
        policy = GatePolicy(entries=[GatePolicyEntry(target={}, gate=GATE_REVIEW_REQUIRED)])
        self.assertEqual(policy.evaluate({"unitType": "anything"}), GATE_REVIEW_REQUIRED)

    def test_unit_type_default_over_global(self):
        policy = GatePolicy(entries=[
            GatePolicyEntry(target={}, gate=GATE_AUTO_CONTINUE),
            GatePolicyEntry(target={"unitType": "design"}, gate=GATE_APPROVAL_REQUIRED),
        ])
        self.assertEqual(policy.evaluate({"unitType": "design"}), GATE_APPROVAL_REQUIRED)
        self.assertEqual(policy.evaluate({"unitType": "other"}), GATE_AUTO_CONTINUE)

    def test_explicit_target_over_unit_type(self):
        # 전이/artifact class(tier 2 명시) > unitType(tier 1).
        policy = GatePolicy(entries=[
            GatePolicyEntry(target={"unitType": "design"}, gate=GATE_REVIEW_REQUIRED),
            GatePolicyEntry(target={"transition": "handoff"}, gate=GATE_APPROVAL_REQUIRED),
        ])
        descriptor = {"unitType": "design", "transition": "handoff"}
        self.assertEqual(policy.evaluate(descriptor), GATE_APPROVAL_REQUIRED)

    def test_tie_break_same_tier_most_severe(self):
        # 같은 tier 복수 매칭 → 가장 심각한 gateKind(강화측).
        policy = GatePolicy(entries=[
            GatePolicyEntry(target={}, gate=GATE_AUTO_CONTINUE),
            GatePolicyEntry(target={}, gate=GATE_APPROVAL_REQUIRED),
        ])
        self.assertEqual(policy.evaluate({"unitType": "x"}), GATE_APPROVAL_REQUIRED)

    def test_from_dict_and_defaults(self):
        policy = GatePolicy.from_dict({
            "entries": [{"target": {"unitType": "t"}, "gate": "escalation_required"}],
        })
        self.assertEqual(policy.evaluate({"unitType": "t"}), GATE_ESCALATION_REQUIRED)
        # actor 클래스 미지정 → 코드 fallback(스키마 default 와 동일).
        self.assertEqual(policy.user_actor_class, DEFAULT_USER_ACTOR_CLASS)
        self.assertEqual(policy.escalation_resolvers, DEFAULT_ESCALATION_RESOLVERS)

    def test_from_file_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "policy.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({
                    "entries": [{"target": {"unitType": "d"}, "gate": "review_required"}],
                    "userActorClass": "human",
                    "escalationResolvers": ["Advisor", "human"],
                }, fh)
            policy = GatePolicy.from_file(path)
            self.assertEqual(policy.evaluate({"unitType": "d"}), GATE_REVIEW_REQUIRED)
            self.assertEqual(policy.user_actor_class, "human")

    def test_invalid_gate_kind_rejected(self):
        with self.assertRaises(ValueError):
            GatePolicyEntry(target={}, gate="bogus")

    def test_schema_defaults_match_code_fallbacks(self):
        # gate_policy_schema.json 의 default 가 코드 fallback 과 일치(단일 진리원천 대조).
        schema_path = os.path.join(_ORCH_DIR, "gate_policy_schema.json")
        with open(schema_path, "r", encoding="utf-8") as fh:
            schema = json.load(fh)
        props = schema["properties"]
        self.assertEqual(props["userActorClass"]["default"], DEFAULT_USER_ACTOR_CLASS)
        self.assertEqual(tuple(props["escalationResolvers"]["default"]), DEFAULT_ESCALATION_RESOLVERS)


# ==========================================================================
# 게이트 큐 파생 뷰·해소 적격성 (PO-INV 2 — 파생 뷰·done 5·6)
# ==========================================================================
class PendingGatesAndResolution(unittest.TestCase):
    def _log_with_requirement(self, gate_id, gate_kind, policy):
        store = InMemoryEventStore()
        log = EventLog(store)
        append_gate_requirement(log, gate_id, gate_kind, target={"u": gate_id}, actor="Advisor")
        return store, log

    def test_requirement_without_resolution_is_pending(self):
        policy = GatePolicy()
        store, _ = self._log_with_requirement("g1", GATE_USER_DECISION_REQUIRED, policy)
        pend = pending_gates(store.read_all(), policy)
        self.assertEqual(len(pend), 1)
        self.assertEqual(pend[0]["gate_id"], "g1")
        self.assertEqual(pend[0]["gateKind"], GATE_USER_DECISION_REQUIRED)
        self.assertIsNotNone(pend[0]["since"])

    def test_pending_gates_is_pure_function_not_mutable_queue(self):
        # 파생 뷰(PO-INV 2): 같은 이벤트 로그를 두 번 접어도 같은 결과·부작용 0.
        policy = GatePolicy()
        store, _ = self._log_with_requirement("g1", GATE_ESCALATION_REQUIRED, policy)
        events = store.read_all()
        first = pending_gates(events, policy)
        second = pending_gates(events, policy)
        self.assertEqual(first, second)
        # 입력 이벤트는 변경되지 않는다(순수).
        self.assertEqual(store.read_all(), events)

    def test_user_decision_only_user_actor_resolves(self):
        policy = GatePolicy(user_actor_class="human")
        store, log = self._log_with_requirement("g1", GATE_USER_DECISION_REQUIRED, policy)
        # 비사용자 actor(Advisor) 해소 시도 → 무효(여전히 pending).
        append_gate_resolution(log, "g1", GATE_USER_DECISION_REQUIRED, actor="Advisor")
        self.assertFalse(is_resolved(store.read_all(), "g1", GATE_USER_DECISION_REQUIRED, policy))
        self.assertEqual(len(pending_gates(store.read_all(), policy)), 1)
        # 사용자 actor(human) 해소 → 유효(해소·pending 0).
        append_gate_resolution(log, "g1", GATE_USER_DECISION_REQUIRED, actor="human")
        self.assertTrue(is_resolved(store.read_all(), "g1", GATE_USER_DECISION_REQUIRED, policy))
        self.assertEqual(pending_gates(store.read_all(), policy), [])

    def test_escalation_resolved_by_resolver_set(self):
        policy = GatePolicy(escalation_resolvers=("Advisor", "human"))
        store, log = self._log_with_requirement("g2", GATE_ESCALATION_REQUIRED, policy)
        # 집합 밖 actor → 무효.
        append_gate_resolution(log, "g2", GATE_ESCALATION_REQUIRED, actor="Worker")
        self.assertFalse(is_resolved(store.read_all(), "g2", GATE_ESCALATION_REQUIRED, policy))
        # 집합 내 actor(Advisor) → 해소.
        append_gate_resolution(log, "g2", GATE_ESCALATION_REQUIRED, actor="Advisor")
        self.assertTrue(is_resolved(store.read_all(), "g2", GATE_ESCALATION_REQUIRED, policy))

    def test_resolution_before_requirement_does_not_count(self):
        # 요구 이전의 해소 이벤트는 그 요구를 해소하지 않는다(at 순서 인과).
        policy = GatePolicy()
        store = InMemoryEventStore()
        log = EventLog(store)
        append_gate_resolution(log, "g3", GATE_USER_DECISION_REQUIRED, actor="human")  # 요구 전.
        append_gate_requirement(log, "g3", GATE_USER_DECISION_REQUIRED, actor="Advisor")
        self.assertFalse(is_resolved(store.read_all(), "g3", GATE_USER_DECISION_REQUIRED, policy))
        self.assertEqual(len(pending_gates(store.read_all(), policy)), 1)

    def test_determinism_same_inputs_same_outputs(self):
        # done 6: 동일 (정책, 이벤트 로그) → 동일 pending_gates·동일 evaluate.
        policy = GatePolicy(entries=[GatePolicyEntry(target={"unitType": "u"}, gate=GATE_REVIEW_REQUIRED)])
        store, _ = self._log_with_requirement("gd", GATE_ESCALATION_REQUIRED, policy)
        events = store.read_all()
        self.assertEqual(pending_gates(events, policy), pending_gates(events, policy))
        self.assertEqual(policy.evaluate({"unitType": "u"}), policy.evaluate({"unitType": "u"}))


# ==========================================================================
# orchestrator 통합 — 모의 invoker (설계 §5 S3 시나리오 d·e)
# ==========================================================================
def gate_task(tid, unit_type=None, target_class=None, intervention=None, owned=None):
    task = {
        "id": tid,
        "task": "unit " + tid,
        "done": "AC-" + tid,
        "interfaceContract": {"produces": ["c-" + tid]},
        "ownedBoundary": (owned if owned is not None else ["file-" + tid]),
        "dependsOn": [],
        "delegation": {
            "from": "Advisor", "to": "Worker", "task": "impl",
            "input": "in-" + tid, "output": "out-" + tid, "done": "AC-" + tid,
            "context": ["doc"], "constraints": None,
        },
        "role": "Worker", "capability": "cap", "model": "slot",
    }
    if unit_type is not None:
        task["unitType"] = unit_type
    if target_class is not None:
        task["targetClass"] = target_class
    if intervention is not None:
        task["interventionCondition"] = intervention
    return task


class GateMockInvoker(Invoker):
    """Worker=완료 / Verifier=Pass / Advisor=Pass. 게이트 디스패치 흔적을 기록한다."""

    def __init__(self):
        self.calls = []  # (role, step_id, is_gate)

    def invoke(self, request):
        step_id = (request.bundle.get("step_contract") or {}).get("id")
        is_gate = "gate" in request.bundle
        self.calls.append((request.role, step_id, is_gate))
        if request.role in (ROLE_VERIFIER, ROLE_ADVISOR):
            return InvokeResult(kind=KIND_COMPLETION, completion={"verdict": "Pass", "rework": None}, ref="vd")
        return InvokeResult(
            kind=KIND_COMPLETION,
            completion={
                "artifacts": ["art-" + str(step_id)], "self_check": "done",
                "failures": "없음", "open_questions": "없음", "verify_basis": "self",
            },
            ref="wr",
        )

    def gate_calls(self, role):
        return [c for c in self.calls if c[0] == role and c[2]]


def build_orch(tasks, policy, autonomy=POLICY_INTERACTIVE, store=None):
    store = store if store is not None else InMemoryEventStore()
    graph = {"goal": "g", "tasks": tasks, "completion": "all-passed"}
    ledger = RevisionLedger(InMemoryRevisionStore(), graph)
    inv = GateMockInvoker()
    orch = ProjectOrchestrator(ledger, store, inv, policy=autonomy, gate_policy=policy)
    return orch, inv, store


def mixed_policy():
    return GatePolicy(entries=[
        GatePolicyEntry(target={"unitType": "t-auto"}, gate=GATE_AUTO_CONTINUE),
        GatePolicyEntry(target={"unitType": "t-review"}, gate=GATE_REVIEW_REQUIRED),
        GatePolicyEntry(target={"unitType": "t-approval"}, gate=GATE_APPROVAL_REQUIRED),
        GatePolicyEntry(target={"unitType": "t-user"}, gate=GATE_USER_DECISION_REQUIRED),
    ], user_actor_class="human", escalation_resolvers=("Advisor", "human"))


def mixed_tasks():
    return [
        gate_task("t-auto", unit_type="t-auto"),
        gate_task("t-review", unit_type="t-review"),
        gate_task("t-approval", unit_type="t-approval"),
        gate_task("t-user", unit_type="t-user"),
    ]


class ScenarioD_MixedGateBehavior(unittest.TestCase):
    def test_distinct_behavior_per_gatekind_and_user_resume(self):
        orch, inv, store = build_orch(mixed_tasks(), mixed_policy())
        result = orch.run()

        # user_decision 단위로 정지(정지 게이트 미해소).
        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.stop_reason, "gate")
        # pending 큐에 user 게이트만.
        self.assertEqual([g["gateKind"] for g in result.pending_gates], [GATE_USER_DECISION_REQUIRED])
        user_gate_id = orch._gate_id_for("t-user")
        self.assertEqual(result.pending_gates[0]["gate_id"], user_gate_id)

        events = store.read_all()
        # auto_continue: 게이트 이벤트 흔적 0.
        auto_gate_id = orch._gate_id_for("t-auto")
        self.assertEqual(gates.gate_events_for(events, auto_gate_id), [])
        # review_required: T2 — 유효 cp2-pass evidence 재사용으로 해소(재검증 디스패치 0).
        #   t-review 는 host 가 CP2 Pass → cp2-pass 를 남겼고 이를 대상하는 stale revision·
        #   해시 불일치가 없으므로 evidence-reuse 마커가 근거 cp2-pass 를 명시 참조한다.
        #   (T2 이전 기대: 재검증 Verifier 디스패치 1회. T2 의미론상 evidence 소비로 대체됨.)
        review_gate_id = orch._gate_id_for("t-review")
        self.assertTrue(has_settlement(events, review_gate_id, REF_KIND_REVIEW))
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 0)  # 재검증 디스패치 생략.
        review_marker = [
            e for e in gates.gate_events_for(events, review_gate_id)
            if (e.get("ref") or {}).get("kind") == REF_KIND_REVIEW
        ][-1]
        self.assertEqual(review_marker["ref"].get("mode"), gates.REVIEW_MODE_EVIDENCE_REUSE)
        self.assertEqual((review_marker["ref"].get("basis") or {}).get("kind"), "cp2-pass")
        # approval_required: Advisor(CP3) 디스패치 흔적 + 마커 이벤트.
        approval_gate_id = orch._gate_id_for("t-approval")
        self.assertTrue(has_settlement(events, approval_gate_id, REF_KIND_APPROVAL))
        self.assertEqual(len(inv.gate_calls(ROLE_ADVISOR)), 1)
        # 모든 단위는 실행되어 Passed(정지는 게이트 축이지 실행 축이 아님).
        self.assertEqual(orch.derive_states()["t-user"], PASSED)

        # 비사용자 actor(Advisor) 해소 시도 → 무효(재기동해도 여전히 정지).
        append_gate_resolution(orch.log, user_gate_id, GATE_USER_DECISION_REQUIRED, actor="Advisor")
        again = orch.run()
        self.assertTrue(again.stopped, again.status)
        self.assertEqual([g["gate_id"] for g in again.pending_gates], [user_gate_id])
        # 재기동 시 review/approval 재디스패치 0(멱등). T2: review 는 evidence 재사용이라
        # 애초에 재검증 디스패치 0(마커 실재로 재처리도 0), approval 은 1회 디스패치 유지.
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 0)
        self.assertEqual(len(inv.gate_calls(ROLE_ADVISOR)), 1)

        # 사용자 actor(human) 해소 → 완주.
        append_gate_resolution(orch.log, user_gate_id, GATE_USER_DECISION_REQUIRED, actor="human")
        done = orch.run()
        self.assertTrue(done.completed, done.status)
        self.assertEqual(pending_gates(store.read_all(), orch.gate_policy), [])

    def test_auto_continue_only_runs_to_completion(self):
        # auto_continue 만인 그래프는 정지 없이 완주(무정지 완주).
        policy = GatePolicy(entries=[GatePolicyEntry(target={}, gate=GATE_AUTO_CONTINUE)])
        orch, inv, store = build_orch([gate_task("a"), gate_task("b")], policy)
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        self.assertEqual(result.pending_gates, [])
        self.assertEqual(inv.gate_calls(ROLE_VERIFIER), [])  # 추가 리뷰 0.


class ScenarioE_AutonomyOrthogonality(unittest.TestCase):
    def test_unrestricted_still_stops_at_user_decision_gate(self):
        # done 4: autonomy=unrestricted 여도 정지 게이트는 그대로 정지.
        orch, inv, store = build_orch(
            mixed_tasks(), mixed_policy(), autonomy=POLICY_UNRESTRICTED
        )
        result = orch.run()
        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.stop_reason, "gate")
        self.assertEqual([g["gateKind"] for g in result.pending_gates], [GATE_USER_DECISION_REQUIRED])

    def test_gate_behavior_identical_across_autonomy_values(self):
        # 5종 게이트 거동이 autonomy 값과 무관하게 동일(게이트 축 ⟂ 도구 승인 축).
        def outcome(autonomy):
            orch, inv, store = build_orch(mixed_tasks(), mixed_policy(), autonomy=autonomy)
            r = orch.run()
            events = store.read_all()
            return (
                r.status,
                r.stop_reason,
                [g["gateKind"] for g in r.pending_gates],
                has_settlement(events, orch._gate_id_for("t-review"), REF_KIND_REVIEW),
                has_settlement(events, orch._gate_id_for("t-approval"), REF_KIND_APPROVAL),
                gates.gate_events_for(events, orch._gate_id_for("t-auto")),
            )

        base = outcome(POLICY_INTERACTIVE)
        self.assertEqual(base, outcome(POLICY_UNRESTRICTED))
        self.assertEqual(base, outcome("auto_approve"))

    def test_escalation_gate_stops_under_unrestricted(self):
        # escalation_required(개입 조건 하한 유발)도 unrestricted 에서 정지.
        policy = GatePolicy(entries=[])  # floor 만으로 escalation 유발.
        tasks = [gate_task("e", intervention=gates.INTERVENTION_BLOCKING)]
        orch, inv, store = build_orch(tasks, policy, autonomy=POLICY_UNRESTRICTED)
        result = orch.run()
        self.assertTrue(result.stopped, result.status)
        self.assertEqual([g["gateKind"] for g in result.pending_gates], [GATE_ESCALATION_REQUIRED])


# ==========================================================================
# ScenarioF — review_required evidence 재사용 통합 (T2·판단 0·fail-closed)
#
# review_required 게이트가 유효 cp2-pass evidence 를 소비해 해소하는지(디스패치 0), stale
# 3규칙·정책 플래그·미지 revision 에서 재검증 디스패치(fallback)로 떨어지는지, 마커 실재
# 시 재처리 0(멱등)인지를 orchestrator 통합으로 실증한다. 직접 _process_gates 경로는 seed
# 로 특정 stale 상태를 구성하되 states 를 명시 공급한다(파생 상태 우회 — 게이트 결정만 관찰).
# ==========================================================================
def _review_policy(require_independent=False):
    return GatePolicy(entries=[
        GatePolicyEntry(
            target={"unitType": "impl"}, gate=GATE_REVIEW_REQUIRED,
            require_independent_review=require_independent,
        ),
    ])


def _cp2_pass_ev(cycle, at, seq=1, verdict_ref="v"):
    return {"cycle_id": cycle, "seq": seq, "from_stage": "Verify", "to_stage": "Complete",
            "trigger": "완료 조건 충족", "outcome": "pass", "actor": ROLE_VERIFIER,
            "ref": {"kind": "cp2-pass", "verdict_ref": verdict_ref}, "at": at}


def _dispatch_ev(cycle, at, seq=1):
    return {"cycle_id": cycle, "seq": seq, "from_stage": None, "to_stage": "Execute",
            "trigger": "완료 조건 충족", "outcome": "pass", "actor": ROLE_WORKER,
            "ref": {"kind": "dispatch"}, "at": at}


def _grounding_ev(gate_id, at):
    return {"cycle_id": "gate::" + gate_id, "seq": 1, "from_stage": "Consult",
            "to_stage": "Complete", "trigger": "완료 조건 충족", "outcome": "pass",
            "actor": "human", "ref": {"kind": "gate-resolved", "gate_id": gate_id}, "at": at}


def _last_review_marker(events, gate_id):
    rows = [
        e for e in gates.gate_events_for(events, gate_id)
        if (e.get("ref") or {}).get("kind") == REF_KIND_REVIEW
    ]
    return rows[-1] if rows else None


def _build_direct(task, policy, seed_events, *, revisions=None, artifact_store=None):
    """seed 된 이벤트/원장으로 orchestrator 를 구성한다(직접 _process_gates 관찰용)."""
    store = InMemoryEventStore(seed=seed_events)
    graph = {"goal": "g", "tasks": [task], "completion": "all-passed"}
    ledger = RevisionLedger(InMemoryRevisionStore(seed=revisions or []), graph)
    inv = GateMockInvoker()
    orch = ProjectOrchestrator(
        ledger, store, inv, gate_policy=policy, artifact_store=artifact_store
    )
    return orch, inv, store


class ScenarioF_ReviewEvidenceReuse(unittest.TestCase):
    def test_valid_cp2_pass_reused_no_dispatch(self):
        # 유효 cp2-pass → 재검증 디스패치 0 + 마커가 근거 cp2-pass 를 명시 참조.
        orch, inv, store = build_orch([gate_task("u", unit_type="impl")], _review_policy())
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        gid = orch._gate_id_for("u")
        events = store.read_all()
        self.assertTrue(has_settlement(events, gid, REF_KIND_REVIEW))
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 0)  # 디스패치 생략.
        marker = _last_review_marker(events, gid)
        self.assertEqual(marker["ref"].get("mode"), gates.REVIEW_MODE_EVIDENCE_REUSE)
        basis = marker["ref"].get("basis") or {}
        self.assertEqual(basis.get("kind"), "cp2-pass")
        self.assertEqual(basis.get("cycle_id"), "u")
        self.assertIsNotNone(basis.get("at"))
        self.assertEqual(basis.get("verdict_ref"), "vd")  # host cp2-pass verdict_ref

    def test_stale_a_retry_after_dispatches(self):
        # cp2-pass 이후 같은 cycle 재디스패치(재실행 흔적) → stale → 재검증 디스패치.
        task = gate_task("u", unit_type="impl")
        seed = [_dispatch_ev("u", 1), _cp2_pass_ev("u", 2, seq=2), _dispatch_ev("u", 3, seq=3)]
        orch, inv, store = _build_direct(task, _review_policy(), seed)
        r = orch._process_gates({"u": PASSED}, 1)
        self.assertIsNone(r)  # review 비정지.
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 1)  # stale → 디스패치.
        marker = _last_review_marker(store.read_all(), orch._gate_id_for("u"))
        self.assertIsNone(marker["ref"].get("mode"))  # 디스패치 경로(mode 없음).

    def test_stale_b_reissue_revision_dispatches(self):
        # 재발행(id==u) revision 이 cp2-pass 이후 grounded → stale → 재검증 디스패치.
        payload = gate_task("u", unit_type="impl")
        payload["supersedes"] = "u"
        rev = {"revisionSeq": 1, "kind": KIND_TASK_SUPERSEDED, "payload": payload,
               "basis": {"proposingStepRef": "u", "gateEventRef": "g-reissue"}}
        task = gate_task("u", unit_type="impl")
        seed = [_cp2_pass_ev("u", 2), _grounding_ev("g-reissue", 5)]
        orch, inv, store = _build_direct(task, _review_policy(), seed, revisions=[rev])
        orch._process_gates({"u": PASSED}, 1)
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 1)
        marker = _last_review_marker(store.read_all(), orch._gate_id_for("u"))
        self.assertIsNone(marker["ref"].get("mode"))

    def test_creating_revision_before_evidence_reuses(self):
        # task_added(id==u) 가 cp2-pass 를 선행(grounded at 1 < cp2-pass at 4) → 재사용(디스패치 0).
        rev = {"revisionSeq": 1, "kind": KIND_TASK_ADDED,
               "payload": gate_task("u", unit_type="impl"),
               "basis": {"proposingStepRef": "p", "gateEventRef": "g-create"}}
        task = gate_task("u", unit_type="impl")
        seed = [_grounding_ev("g-create", 1), _dispatch_ev("u", 2), _cp2_pass_ev("u", 4, seq=2)]
        orch, inv, store = _build_direct(task, _review_policy(), seed, revisions=[rev])
        orch._process_gates({"u": PASSED}, 1)
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 0)  # evidence 재사용.
        marker = _last_review_marker(store.read_all(), orch._gate_id_for("u"))
        self.assertEqual(marker["ref"].get("mode"), gates.REVIEW_MODE_EVIDENCE_REUSE)

    def test_stale_c_recorded_hash_mismatch_dispatches(self):
        # 산출 artifact 에 contentHash 기록 + 실파일 재해시 불일치 → stale → 재검증 디스패치.
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "art.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("actual content")
            decl_store = InMemoryArtifactDeclarationStore(seed=[{
                "artifactId": "a-u", "version": 1,
                "producedBy": {"stepId": "u"}, "location": path,
                "contentHash": "sha256:" + "0" * 64,  # 기록값 ≠ 실파일 재해시.
            }])
            task = gate_task("u", unit_type="impl")
            seed = [_cp2_pass_ev("u", 2)]
            orch, inv, store = _build_direct(
                task, _review_policy(), seed, artifact_store=decl_store
            )
            orch._process_gates({"u": PASSED}, 1)
            self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 1)
            marker = _last_review_marker(store.read_all(), orch._gate_id_for("u"))
            self.assertIsNone(marker["ref"].get("mode"))

    def test_unknown_revision_kind_fail_closed_dispatches(self):
        # 미지 revision kind(grounded)가 있으면 fail-closed → 재검증 디스패치.
        rev = {"revisionSeq": 1, "kind": "frobnicate", "payload": {"id": "u"},
               "basis": {"proposingStepRef": "p", "gateEventRef": "g-x"}}
        task = gate_task("u", unit_type="impl")
        seed = [_cp2_pass_ev("u", 2), _grounding_ev("g-x", 1)]
        orch, inv, store = _build_direct(task, _review_policy(), seed, revisions=[rev])
        orch._process_gates({"u": PASSED}, 1)
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 1)
        marker = _last_review_marker(store.read_all(), orch._gate_id_for("u"))
        self.assertIsNone(marker["ref"].get("mode"))

    def test_policy_flag_forces_dispatch(self):
        # 정책이 독립 2차 검증 요구 → 유효 evidence 여도 무조건 재검증 디스패치.
        orch, inv, store = build_orch(
            [gate_task("u", unit_type="impl")], _review_policy(require_independent=True)
        )
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        gid = orch._gate_id_for("u")
        events = store.read_all()
        self.assertTrue(has_settlement(events, gid, REF_KIND_REVIEW))
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), 1)  # 정책 강제 디스패치.
        marker = _last_review_marker(events, gid)
        self.assertIsNone(marker["ref"].get("mode"))  # 디스패치 경로(mode 없음).
        self.assertNotIn("basis", marker["ref"])  # 근거 참조 없음(evidence 재사용 아님).

    def test_resume_is_idempotent_no_reprocessing(self):
        # 마커 실재 시 재기동해도 재처리 0(새 이벤트·재디스패치 0·결정적 재개).
        orch, inv, store = build_orch([gate_task("u", unit_type="impl")], _review_policy())
        orch.run()
        gid = orch._gate_id_for("u")
        n_events = len(store.read_all())
        n_verifier = len(inv.gate_calls(ROLE_VERIFIER))
        again = orch.run()
        self.assertTrue(again.completed, again.status)
        self.assertEqual(len(store.read_all()), n_events)  # 새 이벤트 0(재처리 없음).
        self.assertEqual(len(inv.gate_calls(ROLE_VERIFIER)), n_verifier)  # 재디스패치 0.
        markers = [
            e for e in gates.gate_events_for(store.read_all(), gid)
            if (e.get("ref") or {}).get("kind") == REF_KIND_REVIEW
        ]
        self.assertEqual(len(markers), 1)  # 마커 정확히 1개(중복 append 0).


class GateClampIntegration(unittest.TestCase):
    def test_floor_stops_even_when_policy_says_auto(self):
        # done 3 통합: 정책이 auto 를 지정해도 실행 착수 target 은 floor(user_decision)로
        # 클램프되어 정지한다(약화 불가).
        policy = GatePolicy(entries=[
            GatePolicyEntry(target={"unitType": "launch"}, gate=GATE_AUTO_CONTINUE),
        ])
        tasks = [gate_task("L", unit_type="launch",
                           target_class=gates.TARGETCLASS_EXECUTION_INITIATION)]
        orch, inv, store = build_orch(tasks, policy)
        result = orch.run()
        self.assertTrue(result.stopped, result.status)
        self.assertEqual([g["gateKind"] for g in result.pending_gates], [GATE_USER_DECISION_REQUIRED])


class GatePolicyNoneIsS2Behavior(unittest.TestCase):
    def test_no_gate_policy_no_gate_processing(self):
        # gate_policy 미지정 → 게이트 처리 0(S2 거동 보존): user 단위여도 정지 안 함.
        store = InMemoryEventStore()
        graph = {"goal": "g", "tasks": mixed_tasks(), "completion": "all-passed"}
        ledger = RevisionLedger(InMemoryRevisionStore(), graph)
        orch = ProjectOrchestrator(ledger, store, GateMockInvoker())  # gate_policy=None
        result = orch.run()
        self.assertTrue(result.completed, result.status)
        self.assertEqual(result.pending_gates, [])


class LatestEligibleResolutionAndResponse(unittest.TestCase):
    """latest_eligible_resolution(원자료 판독)·해소 응답 동봉(가법)의 순수 단위 테스트."""

    def _log(self):
        from stephost_bridge import EventLog
        store = InMemoryEventStore()
        return EventLog(store), store

    def test_returns_none_without_eligible_resolution(self):
        log, store = self._log()
        policy = GatePolicy()
        append_gate_requirement(log, "g1", GATE_ESCALATION_REQUIRED)
        # 부적격 actor 해소만 존재 → None.
        append_gate_resolution(log, "g1", GATE_ESCALATION_REQUIRED, actor="Worker")
        self.assertIsNone(gates.latest_eligible_resolution(
            store.read_all(), "g1", GATE_ESCALATION_REQUIRED, policy))

    def test_returns_latest_eligible_regardless_of_requirement_order(self):
        log, store = self._log()
        policy = GatePolicy()
        # 요구 이전 해소도 **원자료로는** 반환된다(선후 판정은 호출부 몫 — is_resolved 와 대비).
        append_gate_resolution(log, "g2", GATE_ESCALATION_REQUIRED, actor="Advisor",
                               response="첫 응답")
        append_gate_requirement(log, "g2", GATE_ESCALATION_REQUIRED)
        found = gates.latest_eligible_resolution(
            store.read_all(), "g2", GATE_ESCALATION_REQUIRED, policy)
        self.assertIsNotNone(found)
        self.assertEqual(gates.resolution_response(found), "첫 응답")
        # is_resolved 는 요구 이후 해소만 인정하므로 여전히 미해소다(역할 분리 확인).
        self.assertFalse(is_resolved(store.read_all(), "g2", GATE_ESCALATION_REQUIRED, policy))
        # 요구 이후 적격 해소가 추가되면 그것이 최신으로 반환된다.
        append_gate_resolution(log, "g2", GATE_ESCALATION_REQUIRED, actor="human",
                               response="둘째 응답")
        found2 = gates.latest_eligible_resolution(
            store.read_all(), "g2", GATE_ESCALATION_REQUIRED, policy)
        self.assertEqual(gates.resolution_response(found2), "둘째 응답")
        self.assertTrue(is_resolved(store.read_all(), "g2", GATE_ESCALATION_REQUIRED, policy))

    def test_response_absent_keeps_ref_byte_shape(self):
        log, _store = self._log()
        event = append_gate_resolution(log, "g3", GATE_ESCALATION_REQUIRED, actor="Advisor")
        self.assertEqual(sorted(event["ref"].keys()), ["gateKind", "gate_id", "kind"])
        self.assertIsNone(gates.resolution_response(event))


if __name__ == "__main__":
    unittest.main(verbosity=2)
