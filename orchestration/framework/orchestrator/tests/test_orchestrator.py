"""Project Orchestrator 통합 테스트 (표준 라이브러리 unittest 만·외부 의존 0).

**모의 invoker 통합 테스트**다 — 실 CLI E2E 는 S5 소관이며, 여기서는 기존 invoker.py
Invoker 추상을 구현한 중립 stub 으로 설계 §5 S2 시나리오 3건을 실증한다:

  (a) 2-task 그래프 실행 중 산출이 task 3 제안 → 게이트 승인 이벤트 append →
      revision append → 이어 실행
  (b) 중단 후 재기동 — 동일 2원장(revision 원장·이벤트 로그) 재생 → 동일 재개 지점
      (그래프 지문·ready_set·순서 동일 실측)
  (c) 순환 유발 revision → 07 사유 코드로 차단·원장 오염 0

추가로 PO-INV 5(게이트 근거 없는 revision 수용 거부·fold 수준 배제)를 실증한다.

이 파일은 stephost_bridge 를 통해 uahf/ step-host 를 라이브러리로 무수정 import 한다.
특정 provider·모델·상류 Layer 고유명 토큰을 두지 않는다(PO-INV 8).
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

_ORCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ORCH_DIR not in sys.path:
    sys.path.insert(0, _ORCH_DIR)

from orchestrator import (  # noqa: E402
    OrchestrationResult,
    ProjectOrchestrator,
    REASON_UNGROUNDED_REVISION,
)
from revision import (  # noqa: E402
    InMemoryRevisionStore,
    JsonlRevisionStore,
    KIND_DEPENDENCY_ADDED,
    KIND_TASK_ADDED,
    REASON_DEPENDENCY_CYCLE,
    RevisionEvent,
    RevisionLedger,
    RevisionRejected,
)
from stephost_bridge import (  # noqa: E402
    InMemoryEventStore,
    Invoker,
    InvokeResult,
    JsonlEventStore,
    KIND_COMPLETION,
    PASSED,
    PENDING,
    ROLE_ADVISOR,
    ROLE_VERIFIER,
    ROLE_WORKER,
)
from gates import (  # noqa: E402
    GATE_APPROVAL_REQUIRED,
    GATE_ESCALATION_REQUIRED,
    GATE_USER_DECISION_REQUIRED,
    REF_KIND_REQUIRED,
    GatePolicy,
    append_gate_resolution,
    pending_gates,
)


# --------------------------------------------------------------------------
# 픽스처 — 07 Task payload + 중립 stub invoker
# --------------------------------------------------------------------------
def task_payload(tid, depends_on=None, owned=None):
    return {
        "id": tid,
        "task": "unit " + tid,
        "done": "AC-" + tid,
        "interfaceContract": {"produces": ["c-" + tid]},
        "ownedBoundary": (owned if owned is not None else ["file-" + tid]),
        "dependsOn": list(depends_on or []),
        "delegation": {
            "from": "Advisor", "to": "Worker", "task": "impl",
            "input": "in-" + tid, "output": "out-" + tid, "done": "AC-" + tid,
            "context": ["doc"], "constraints": None,
        },
        "role": "Worker", "capability": "cap", "model": "slot",
    }


def initial_two_task():
    return {
        "goal": "goal",
        "tasks": [task_payload("s1"), task_payload("s2", depends_on=["s1"])],
        "completion": "all-passed",
    }


def _completion(step_id):
    return InvokeResult(
        kind=KIND_COMPLETION,
        completion={
            "artifacts": ["art-" + str(step_id)], "self_check": "done",
            "failures": "없음", "open_questions": "없음", "verify_basis": "self",
        },
        ref="wr",
    )


def _verdict_pass():
    return InvokeResult(
        kind=KIND_COMPLETION,
        completion={"verdict": "Pass", "rework": None},
        ref="vd",
    )


class MockInvoker(Invoker):
    """중립 stub invoker — Worker=완료, Verifier=Pass. 특정 실행 표면·provider 없음.

    hooks[step_id] 에 콜백을 걸면 그 Worker step 의 최초 invoke 시 1회 실행된다 —
    "실행 중 산출이 새 task 를 제안"하는 외부 드라이버 거동을 모형화한다.
    """

    def __init__(self):
        self.hooks = {}
        self._fired = set()
        self.calls = []  # (role, step_id)

    def invoke(self, request):
        step_id = (request.bundle.get("step_contract") or {}).get("id")
        self.calls.append((request.role, step_id))
        if request.role == ROLE_VERIFIER:
            return _verdict_pass()
        # Worker: 제안 훅(있으면 1회) 실행 후 완료 보고 반환.
        hook = self.hooks.get(step_id)
        if hook is not None and step_id not in self._fired:
            self._fired.add(step_id)
            hook(request)
        return _completion(step_id)

    def worker_calls(self, step_id=None):
        return [c for c in self.calls if c[0] == ROLE_WORKER and (step_id is None or c[1] == step_id)]


def _append_gate_event(orch, gate_id):
    """외부(드라이버)가 게이트 승인 이벤트를 이벤트 로그에 append 한다.

    새 스키마가 아니라 03 전이 이벤트 그대로이며, step 이 아닌 별도 cycle 네임스페이스
    ("gate::<id>")를 써 Step Host 의 step 상태 파생에 간섭하지 않는다. ref 에 gate_id 를
    싣는다(자유 형식 ref 필드 재사용).
    """
    orch.log.append(
        cycle_id="gate::" + gate_id,
        to_stage="Complete",
        trigger="완료 조건 충족",
        outcome="pass",
        actor=ROLE_ADVISOR,
        ref={"kind": "gate", "gate_id": gate_id},
    )


# ==========================================================================
# 시나리오 (a) — 실행 중 task 3 제안 → 게이트 승인 → revision → 이어 실행
# ==========================================================================
class ScenarioA_ProposalThenContinue(unittest.TestCase):
    def test_proposal_accepted_and_executed(self):
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        inv = MockInvoker()
        orch = ProjectOrchestrator(ledger, store, inv)

        def propose_s3(request):
            # 외부가 게이트 승인 이벤트 append → orchestrator 는 실재 검증만 하고 revision append.
            _append_gate_event(orch, "g-s3")
            orch.accept_revision(
                KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]),
                proposingStepRef="s2#1", gateEventRef="g-s3",
            )

        inv.hooks["s2"] = propose_s3

        result = orch.run()

        self.assertTrue(result.completed, result.status)
        # 그래프가 실행 중 확장되어 s3 이 실재·실행됐다.
        self.assertEqual(set(result.graph_task_ids), {"s1", "s2", "s3"})
        self.assertEqual(result.states["s3"], PASSED)
        self.assertEqual(result.states["s1"], PASSED)
        self.assertEqual(result.states["s2"], PASSED)
        # 원장에 s3 revision 1건.
        self.assertEqual(len(ledger.store.read_all()), 1)
        # s3 은 각 1회만 Worker·Verifier 디스패치(재실행 없음).
        self.assertEqual(len(inv.worker_calls("s3")), 1)
        # 성장으로 최소 2 epoch 소요.
        self.assertGreaterEqual(result.epochs, 2)

    def test_gate_event_is_ordinary_event_not_step_state(self):
        # 게이트 이벤트가 step 상태를 오염시키지 않음(별도 cycle 네임스페이스).
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        inv = MockInvoker()
        orch = ProjectOrchestrator(ledger, store, inv)
        inv.hooks["s2"] = lambda req: (
            _append_gate_event(orch, "g-s3"),
            orch.accept_revision(KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]),
                                 proposingStepRef="s2#1", gateEventRef="g-s3"),
        )
        orch.run()
        # gate cycle 은 step 집합에 없다 → derive_states 에 노출되지 않는다.
        self.assertNotIn("gate::g-s3", orch.derive_states())


# ==========================================================================
# 시나리오 (b) — 중단 후 재기동: 동일 2원장 → 동일 재개 지점
# ==========================================================================
class ScenarioB_DeterministicResume(unittest.TestCase):
    def _seed_midstate(self, event_store, revision_store):
        """중단 지점 시드: s1 Passed + 게이트 이벤트 + 근거 있는 s3 revision.

        재개 지점 = ready_set. s1 Passed → s2 ready, s3(dep s2) 대기.
        """
        from stephost_bridge import EventLog
        log = EventLog(event_store)
        # s1 Passed (dispatch + CP2 Pass).
        log.append(cycle_id="s1", to_stage="Execute", trigger="완료 조건 충족",
                   outcome="pass", actor=ROLE_WORKER, ref={"kind": "dispatch"})
        log.append(cycle_id="s1", from_stage="Verify", to_stage="Complete",
                   trigger="완료 조건 충족", outcome="pass", actor=ROLE_VERIFIER,
                   ref={"kind": "cp2-pass"})
        # 게이트 이벤트 + 근거 있는 s3 revision.
        log.append(cycle_id="gate::g-s3", to_stage="Complete", trigger="완료 조건 충족",
                   outcome="pass", actor=ROLE_ADVISOR, ref={"kind": "gate", "gate_id": "g-s3"})
        seeder = RevisionLedger(revision_store, initial_two_task())
        seeder.append(KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]),
                      {"proposingStepRef": "s2#1", "gateEventRef": "g-s3"})

    def test_same_two_ledgers_same_resume_point(self):
        with tempfile.TemporaryDirectory() as tmp:
            epath = os.path.join(tmp, "events.jsonl")
            rpath = os.path.join(tmp, "revisions.jsonl")
            self._seed_midstate(JsonlEventStore(epath), JsonlRevisionStore(rpath))

            # 두 독립 재개 인스턴스가 같은 두 원장을 재생한다.
            orch_a = ProjectOrchestrator(
                RevisionLedger(JsonlRevisionStore(rpath), initial_two_task()),
                JsonlEventStore(epath), MockInvoker())
            orch_b = ProjectOrchestrator(
                RevisionLedger(JsonlRevisionStore(rpath), initial_two_task()),
                JsonlEventStore(epath), MockInvoker())

            # 동일 그래프(순서·내용) — 지문·id 순서 동일.
            self.assertEqual(orch_a.graph_fingerprint(), orch_b.graph_fingerprint())
            ids_a = [t["id"] for t in orch_a.active_graph()["tasks"]]
            ids_b = [t["id"] for t in orch_b.active_graph()["tasks"]]
            self.assertEqual(ids_a, ids_b)
            self.assertEqual(ids_a, ["s1", "s2", "s3"])

            # 동일 재개 지점(ready_set) — s1 Passed → s2 준비, s3 대기.
            self.assertEqual(orch_a.ready_set(), orch_b.ready_set())
            self.assertEqual(orch_a.ready_set(), ["s2"])
            self.assertEqual(orch_a.derive_states()["s1"], PASSED)
            self.assertEqual(orch_a.derive_states()["s3"], PENDING)

            # 재생은 두 원장을 변경하지 않는다(순수 판독).
            self.assertEqual(len(JsonlEventStore(epath).read_all()), 3)
            self.assertEqual(len(JsonlRevisionStore(rpath).read_all()), 1)

    def test_resume_after_full_run_is_idempotent(self):
        # run 완료 후 같은 두 원장으로 재기동해도 그래프 지문 동일(결정적 재개).
        store = InMemoryEventStore()
        rstore = InMemoryRevisionStore()
        ledger = RevisionLedger(rstore, initial_two_task())
        inv = MockInvoker()
        orch = ProjectOrchestrator(ledger, store, inv)
        inv.hooks["s2"] = lambda req: (
            _append_gate_event(orch, "g-s3"),
            orch.accept_revision(KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]),
                                 proposingStepRef="s2#1", gateEventRef="g-s3"),
        )
        first = orch.run()
        fp_after_run = orch.graph_fingerprint()

        # 같은 두 원장으로 재기동.
        resumed = ProjectOrchestrator(
            RevisionLedger(rstore, initial_two_task()), store, MockInvoker())
        self.assertEqual(resumed.graph_fingerprint(), fp_after_run)
        # 전부 Passed → ready_set 비었고 재실행 없음.
        self.assertEqual(resumed.ready_set(), [])
        again = resumed.run()
        self.assertTrue(again.completed)
        self.assertEqual(len(resumed.invoker.worker_calls()), 0)  # 재실행 0.
        self.assertTrue(first.completed)


# ==========================================================================
# 시나리오 (c) — 순환 유발 revision → 사유 코드 차단·원장 오염 0
# ==========================================================================
class ScenarioC_CyclicRevisionBlocked(unittest.TestCase):
    def test_cyclic_revision_blocked_ledger_clean(self):
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        inv = MockInvoker()
        orch = ProjectOrchestrator(ledger, store, inv)
        # 게이트 이벤트는 실재(근거는 충족) — 차단 사유는 순환(구조)임을 분리 실증.
        _append_gate_event(orch, "g-cyc")

        with self.assertRaises(RevisionRejected) as ctx:
            # 초기 s2 -> s1. 여기에 s1 -> s2 의존 추가 → 순환.
            orch.accept_revision(
                KIND_DEPENDENCY_ADDED, {"id": "s1", "dependsOn": ["s2"]},
                proposingStepRef="p", gateEventRef="g-cyc",
            )
        self.assertEqual(ctx.exception.reason, REASON_DEPENDENCY_CYCLE)
        # 원장 오염 0.
        self.assertEqual(len(ledger.store.read_all()), 0)
        # 그래프 불변 — 초기 2-task 그대로.
        self.assertEqual([t["id"] for t in orch.active_graph()["tasks"]], ["s1", "s2"])


# ==========================================================================
# PO-INV 5 — revision 근거 필수 (게이트 이벤트 실재)
# ==========================================================================
class POINV5_RevisionGrounding(unittest.TestCase):
    def test_ungrounded_revision_refused_at_accept(self):
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        orch = ProjectOrchestrator(ledger, store, MockInvoker())
        # 게이트 이벤트가 로그에 실재하지 않는다 → 수용 거부.
        with self.assertRaises(RevisionRejected) as ctx:
            orch.accept_revision(
                KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]),
                proposingStepRef="p", gateEventRef="nonexistent",
            )
        self.assertEqual(ctx.exception.reason, REASON_UNGROUNDED_REVISION)
        # 원장 오염 0.
        self.assertEqual(len(ledger.store.read_all()), 0)

    def test_active_graph_excludes_ungrounded_until_gate_event_appears(self):
        # 원장에 근거 미실현 revision 이 직접 들어와도(accept 우회) fold 수준에서 배제된다.
        store = InMemoryEventStore()
        rstore = InMemoryRevisionStore()
        rstore.append(RevisionEvent(
            revisionSeq=1, kind=KIND_TASK_ADDED, payload=task_payload("s3", depends_on=["s2"]),
            basis={"proposingStepRef": "p", "gateEventRef": "ghost"},
        ).to_dict())
        orch = ProjectOrchestrator(
            RevisionLedger(rstore, initial_two_task()), store, MockInvoker())

        # 게이트 이벤트 없음 → s3 은 그래프에 없다.
        self.assertEqual([t["id"] for t in orch.active_graph()["tasks"]], ["s1", "s2"])
        # 게이트 이벤트가 실재하면 → s3 수용(그래프 반영).
        _append_gate_event(orch, "ghost")
        self.assertEqual(
            set(t["id"] for t in orch.active_graph()["tasks"]), {"s1", "s2", "s3"})


# ==========================================================================
# 판단 0 (PO-INV 1) — Escalated 잔존 시 즉시 정지 (Host 반환 소비만)
# ==========================================================================
class POINV1_NoJudgment(unittest.TestCase):
    def test_escalated_stops_immediately(self):
        # Worker 가 차단(blocked)을 선언하면 Step Host 가 Escalated·stopped 반환 →
        # orchestrator 는 그 status 만 소비해 즉시 정지한다(내용 판정 0).
        from stephost_bridge import KIND_BLOCKED

        class BlockingInvoker(Invoker):
            def invoke(self, request):
                if request.role == ROLE_VERIFIER:
                    return _verdict_pass()
                sid = (request.bundle.get("step_contract") or {}).get("id")
                if sid == "s1":
                    return InvokeResult(kind=KIND_BLOCKED,
                                        failure={"reason": "의존 계약 미확정", "blocking": "차단됨"},
                                        ref="blk")
                return _completion(sid)

        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        orch = ProjectOrchestrator(ledger, store, BlockingInvoker())
        result = orch.run()
        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.stop_reason, "escalated")
        self.assertIn("s1", result.stopped_tasks)


# ==========================================================================
# OQ-PO-B5 — 게이트 근거 실재 검증에 해소 actor 자격 재검증 (설계 D1)
#
# _gate_event_exists 강화: 정지 게이트 해소를 선언하는 pass 이벤트(ref.kind=gate-resolved·
# gateKind ∈ STOPPING_GATES)는 gate_policy 존재 시 적격 actor 일 때만 revision 을 근거지을
# 수 있다. 거동 보존 3면(레거시 ref.kind="gate"·비정지 gateKind·gate_policy None)은
# 실재-만 검증을 유지한다. 이 강화는 accept_revision(수용)·_grounded_revisions(fold) 양시점.
# ==========================================================================
def _stopping_policy():
    """정지 게이트 적격성 판정용 정책(user_decision=human·escalation={Advisor,human})."""
    return GatePolicy(user_actor_class="human", escalation_resolvers=("Advisor", "human"))


def _new_task_revision_args():
    """근거 검증 대상 revision 인자(s3 task_added·gateEventRef 는 케이스별 지정)."""
    return dict(kind=KIND_TASK_ADDED, payload=task_payload("s3", depends_on=["s2"]),
                proposingStepRef="p")


class POINV5_B5_ResolverActorReverification(unittest.TestCase):
    def _orch(self, *, gate_policy):
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        orch = ProjectOrchestrator(ledger, store, MockInvoker(), gate_policy=gate_policy)
        return orch, ledger

    def test_t1_ineligible_stopping_resolver_rejected(self):
        # gate_policy 있음 + user_decision 을 부적격 actor(Advisor)로 해소 → 승격 근거 부적격.
        orch, ledger = self._orch(gate_policy=_stopping_policy())
        append_gate_resolution(orch.log, "g-user", GATE_USER_DECISION_REQUIRED, actor=ROLE_ADVISOR)
        with self.assertRaises(RevisionRejected) as ctx:
            orch.accept_revision(**_new_task_revision_args(), gateEventRef="g-user")
        self.assertEqual(ctx.exception.reason, REASON_UNGROUNDED_REVISION)
        self.assertEqual(len(ledger.store.read_all()), 0)  # 원장 오염 0.

    def test_t2_eligible_stopping_resolver_accepted(self):
        # gate_policy 있음 + 적격 actor(=userActorClass=human) → 수용.
        orch, ledger = self._orch(gate_policy=_stopping_policy())
        append_gate_resolution(orch.log, "g-user", GATE_USER_DECISION_REQUIRED, actor="human")
        rev = orch.accept_revision(**_new_task_revision_args(), gateEventRef="g-user")
        self.assertIsNotNone(rev)
        self.assertEqual(len(ledger.store.read_all()), 1)
        self.assertEqual(
            set(t["id"] for t in orch.active_graph()["tasks"]), {"s1", "s2", "s3"})

    def test_t3_gate_policy_none_accepts_stopping_resolution_s2_preserved(self):
        # gate_policy None + 동일 gate-resolved 이벤트 → 기존대로 수용(S2 보존·실재-만 검증).
        orch, ledger = self._orch(gate_policy=None)
        # 부적격 actor 여도 정책 부재 시 적격성 판정 없이 실재-만으로 수용.
        append_gate_resolution(orch.log, "g-user", GATE_USER_DECISION_REQUIRED, actor=ROLE_ADVISOR)
        rev = orch.accept_revision(**_new_task_revision_args(), gateEventRef="g-user")
        self.assertIsNotNone(rev)
        self.assertEqual(len(ledger.store.read_all()), 1)

    def test_t4_legacy_gate_event_accepted_with_policy(self):
        # 레거시 ref.kind="gate"(gateKind 부재) + gate_policy 있음 → 기존대로 수용(강화 무적용).
        orch, ledger = self._orch(gate_policy=_stopping_policy())
        _append_gate_event(orch, "g-legacy")  # ref={"kind":"gate","gate_id":...}·actor=Advisor
        rev = orch.accept_revision(**_new_task_revision_args(), gateEventRef="g-legacy")
        self.assertIsNotNone(rev)
        self.assertEqual(len(ledger.store.read_all()), 1)

    def test_t5_nonstopping_gatekind_resolution_accepted(self):
        # 비정지 gateKind(approval_required) gate-resolved + gate_policy 있음 → 기존대로 수용.
        #   is_eligible_resolver(approval_required, ...) 는 False 지만 적용 범위(STOPPING_GATES)
        #   밖이므로 실재-만 검증이 적용된다(test_artifacts L540 rework 근거 패턴 보존).
        orch, ledger = self._orch(gate_policy=_stopping_policy())
        append_gate_resolution(orch.log, "g-appr", GATE_APPROVAL_REQUIRED, actor=ROLE_ADVISOR)
        rev = orch.accept_revision(**_new_task_revision_args(), gateEventRef="g-appr")
        self.assertIsNotNone(rev)
        self.assertEqual(len(ledger.store.read_all()), 1)

    def test_t6_fold_excludes_ineligible_grounding_until_eligible_appears(self):
        # 부적격-근거 revision 이 원장에 이미 있을 때(accept 우회) fold 가 배제하고,
        # 적격 이벤트가 추가되면 다시 포함한다(재개 시 방어·양시점 강화).
        store = InMemoryEventStore()
        rstore = InMemoryRevisionStore()
        rstore.append(RevisionEvent(
            revisionSeq=1, kind=KIND_TASK_ADDED,
            payload=task_payload("s3", depends_on=["s2"]),
            basis={"proposingStepRef": "p", "gateEventRef": "g-user"},
        ).to_dict())
        orch = ProjectOrchestrator(
            RevisionLedger(rstore, initial_two_task()), store, MockInvoker(),
            gate_policy=_stopping_policy())

        # 부적격 해소(Advisor)만 → s3 은 fold 에서 배제(그래프 미반영).
        append_gate_resolution(orch.log, "g-user", GATE_USER_DECISION_REQUIRED, actor=ROLE_ADVISOR)
        self.assertEqual([t["id"] for t in orch.active_graph()["tasks"]], ["s1", "s2"])

        # 적격 해소(human) 추가 → s3 다시 fold 에 포함(재개 시 재확인).
        append_gate_resolution(orch.log, "g-user", GATE_USER_DECISION_REQUIRED, actor="human")
        self.assertEqual(
            set(t["id"] for t in orch.active_graph()["tasks"]), {"s1", "s2", "s3"})


# ==========================================================================
# 백로그 §J — 실행 에스컬레이션 해소 채널 (D1 좌표 발급 · D2 rework · D3 응답 전파)
#
# Host 는 재시도 한도 초과를 Escalated 로 종단시키고 정지한다. 지금까지 그 정지는 원장
# 좌표(gate_id)가 없어 해소 이벤트를 append 할 대상 자체가 없었다(§J ①). 아래 케이스는
# ① 좌표 발급·멱등, ② 적격 해소 후 재작업 되돌림 → 정확히 1회 추가 디스패치,
# ③ 재에스컬레이션 시 이전 해소 소진(새 요구), ④ 부적격/선행 해소 무효, ⑤ 응답 전파,
# ⑥ gate_policy 부재(레거시) 거동 보존을 실증한다.
# ==========================================================================
from stephost_bridge import KIND_FAILURE  # noqa: E402
from orchestrator import (  # noqa: E402
    CAUSE_EXECUTION_ESCALATED,
    REF_KIND_GATE_REWORK,
)


class _FailingInvoker(Invoker):
    """지정 step 의 Worker 디스패치를 실패시킨다(fail_ids 를 비우면 다음 시도는 성공).

    Verifier 는 항상 Pass — 실패 원인을 CP1 실패 하나로 고정해 재시도 한도 경로를 분리 실증한다.
    """

    def __init__(self, fail_ids=()):
        self.fail_ids = set(fail_ids)
        self.calls = []          # (role, step_id)
        self.worker_bundles = []  # Worker 디스패치 번들(재작업 feedback 전달 실측용)

    def invoke(self, request):
        step_id = (request.bundle.get("step_contract") or {}).get("id")
        self.calls.append((request.role, step_id))
        if request.role == ROLE_VERIFIER:
            return _verdict_pass()
        self.worker_bundles.append(request.bundle)
        if step_id in self.fail_ids:
            return InvokeResult(
                kind=KIND_FAILURE,
                failure={"reason": "실행 실패", "repro": "동일 입력 재현"},
                ref="fr",
            )
        return _completion(step_id)

    def worker_calls(self, step_id=None):
        return [c for c in self.calls
                if c[0] == ROLE_WORKER and (step_id is None or c[1] == step_id)]


def _escalation_policy():
    """정지 게이트 적격성 정책(escalation 해소 = {Advisor, human})."""
    return GatePolicy(user_actor_class="human", escalation_resolvers=("Advisor", "human"))


def _gate_required_events(store, gate_id):
    return [
        e for e in store.read_all()
        if (e.get("ref") or {}).get("kind") == REF_KIND_REQUIRED
        and (e.get("ref") or {}).get("gate_id") == gate_id
    ]


def _rework_events(store, cycle_id):
    return [
        e for e in store.read_all()
        if e.get("cycle_id") == cycle_id
        and (e.get("ref") or {}).get("kind") == REF_KIND_GATE_REWORK
    ]


class BacklogJ_EscalationResolutionChannel(unittest.TestCase):
    ESC_GATE = "gate-unit-s1::exec-escalation"

    def _run_to_escalation(self, *, gate_policy):
        """s1 을 재시도 한도(0) 초과로 Escalated 시켜 정지시킨다. 반환 = (store, result, inv)."""
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        inv = _FailingInvoker(fail_ids={"s1"})
        orch = ProjectOrchestrator(
            ledger, store, inv, retry_limit=0, gate_policy=gate_policy)
        result = orch.run()
        return store, ledger, inv, result

    # --- D1 좌표 발급 ---------------------------------------------------
    def test_d1_escalated_stop_appends_gate_requirement_and_pending(self):
        store, _ledger, _inv, result = self._run_to_escalation(
            gate_policy=_escalation_policy())

        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.stop_reason, "escalated")
        self.assertIn("s1", result.stopped_tasks)

        reqs = _gate_required_events(store, self.ESC_GATE)
        self.assertEqual(len(reqs), 1, "실행 에스컬레이션 게이트 요구 1건")
        ref = reqs[0]["ref"]
        self.assertEqual(ref["gateKind"], GATE_ESCALATION_REQUIRED)
        self.assertEqual(ref["scoped_question"]["unitId"], "s1")
        self.assertEqual(ref["scoped_question"]["cause"], CAUSE_EXECUTION_ESCALATED)
        # 결과에 게이트 큐가 탑재된다(런처 stop-signal 계약의 입력).
        self.assertEqual([g["gate_id"] for g in result.pending_gates], [self.ESC_GATE])
        self.assertEqual(result.pending_gates[0]["gateKind"], GATE_ESCALATION_REQUIRED)
        # 단위 경계 게이트 id 와 비충돌(같은 단위의 다른 게이트를 덮지 않는다).
        self.assertNotEqual(self.ESC_GATE, ProjectOrchestrator._gate_id_for("s1"))

    def test_d1_idempotent_no_duplicate_requirement_on_rerun(self):
        store, ledger, _inv, _result = self._run_to_escalation(
            gate_policy=_escalation_policy())
        before = len(store.read_all())

        # 같은 두 원장으로 재기동(해소 없음) → 요구 재append 0·재실행 0.
        inv2 = _FailingInvoker(fail_ids={"s1"})
        orch2 = ProjectOrchestrator(
            RevisionLedger(ledger.store, initial_two_task()), store, inv2,
            retry_limit=0, gate_policy=_escalation_policy())
        again = orch2.run()

        self.assertTrue(again.stopped)
        self.assertEqual(len(_gate_required_events(store, self.ESC_GATE)), 1, "중복 append 0")
        self.assertEqual(len(store.read_all()), before, "이벤트 로그 무증가(멱등)")
        self.assertEqual(len(inv2.worker_calls()), 0, "재실행 0")

    def test_d1_no_gate_policy_preserves_legacy_behavior(self):
        store, _ledger, _inv, result = self._run_to_escalation(gate_policy=None)
        self.assertTrue(result.stopped)
        self.assertEqual(result.stop_reason, "escalated")
        # 게이트 이벤트 0(gate:: 네임스페이스 이벤트 자체가 없다)·pending 빈 목록.
        self.assertEqual(
            [e for e in store.read_all() if str(e.get("cycle_id", "")).startswith("gate::")], [])
        self.assertEqual(result.pending_gates, [])

    # --- D2 rework 적용 + D3 응답 전파 ------------------------------------
    def _resolve(self, store, *, actor, response=None, gate_id=None):
        from stephost_bridge import EventLog
        append_gate_resolution(
            EventLog(store), gate_id or self.ESC_GATE, GATE_ESCALATION_REQUIRED,
            actor=actor, response=response)

    def test_d2_eligible_resolution_reworks_and_redispatches_once(self):
        store, ledger, _inv, _result = self._run_to_escalation(
            gate_policy=_escalation_policy())
        self._resolve(store, actor=ROLE_ADVISOR, response="timeout 상향 후 재시도")

        inv2 = _FailingInvoker(fail_ids=set())  # 재시도는 성공.
        orch2 = ProjectOrchestrator(
            RevisionLedger(ledger.store, initial_two_task()), store, inv2,
            retry_limit=0, gate_policy=_escalation_policy())
        result = orch2.run()

        # 되돌림 이벤트 1건 → 추가 디스패치 1회 → 완료.
        rework = _rework_events(store, "s1")
        self.assertEqual(len(rework), 1)
        self.assertEqual(rework[0]["outcome"], "fail")
        self.assertEqual(rework[0]["ref"]["gate_id"], self.ESC_GATE)
        self.assertEqual(rework[0]["actor"], ROLE_ADVISOR, "해소 주체를 provenance 로 기록")
        self.assertEqual(len(inv2.worker_calls("s1")), 1, "정확히 1회 추가 디스패치")
        self.assertTrue(result.completed, result.status)
        self.assertEqual(result.states["s1"], PASSED)

        # D3 — 해소 응답이 되돌림 ref 로 복사되고 재디스패치 번들 feedback 까지 도달한다.
        self.assertEqual(rework[0]["ref"]["response"], "timeout 상향 후 재시도")
        s1_bundles = [b for b in inv2.worker_bundles
                      if (b.get("step_contract") or {}).get("id") == "s1"]
        self.assertEqual(len(s1_bundles), 1)
        self.assertEqual(s1_bundles[0]["feedback"], rework[0]["ref"],
                         "last_failure_ref → 번들 feedback 전달(실측)")

    def test_d2_ineligible_actor_resolution_does_not_rework(self):
        store, ledger, _inv, _result = self._run_to_escalation(
            gate_policy=_escalation_policy())
        self._resolve(store, actor=ROLE_WORKER, response="부적격 해소 시도")  # 정책 밖 actor.

        inv2 = _FailingInvoker(fail_ids=set())
        orch2 = ProjectOrchestrator(
            RevisionLedger(ledger.store, initial_two_task()), store, inv2,
            retry_limit=0, gate_policy=_escalation_policy())
        result = orch2.run()

        self.assertEqual(_rework_events(store, "s1"), [], "부적격 해소 → 되돌림 0")
        self.assertEqual(len(inv2.worker_calls()), 0, "재디스패치 0")
        self.assertTrue(result.stopped)
        self.assertEqual([g["gate_id"] for g in result.pending_gates], [self.ESC_GATE])

    def test_d2_resolution_before_escalation_does_not_rework(self):
        """R_at ≤ E_at — 에스컬레이션보다 앞선 해소는 그 에스컬레이션을 해소하지 않는다."""
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        # 아직 아무 일도 없는 시점에 (적격 actor) 해소를 먼저 append 한다.
        self._resolve(store, actor=ROLE_ADVISOR, response="선행 해소")

        inv = _FailingInvoker(fail_ids={"s1"})
        orch = ProjectOrchestrator(
            ledger, store, inv, retry_limit=0, gate_policy=_escalation_policy())
        result = orch.run()

        self.assertEqual(_rework_events(store, "s1"), [], "선행 해소 → 되돌림 0")
        self.assertTrue(result.stopped)
        self.assertEqual(len(_gate_required_events(store, self.ESC_GATE)), 1)
        self.assertEqual([g["gate_id"] for g in result.pending_gates], [self.ESC_GATE])

    # --- 재에스컬레이션(해소 1건 = 시도 1회) --------------------------------
    def test_reescalation_appends_new_requirement_and_consumes_prior_resolution(self):
        store, ledger, _inv, _result = self._run_to_escalation(
            gate_policy=_escalation_policy())
        self._resolve(store, actor=ROLE_ADVISOR, response="한 번 더 시도")

        inv2 = _FailingInvoker(fail_ids={"s1"})  # 되돌림 후에도 실패.
        orch2 = ProjectOrchestrator(
            RevisionLedger(ledger.store, initial_two_task()), store, inv2,
            retry_limit=0, gate_policy=_escalation_policy())
        result = orch2.run()

        self.assertEqual(len(_rework_events(store, "s1")), 1, "되돌림 1회")
        self.assertEqual(len(inv2.worker_calls("s1")), 1, "추가 시도 정확히 1회")
        self.assertTrue(result.stopped, "재실패 → 정직하게 재에스컬레이션")
        # 이전 해소가 새 요구를 해소하지 못한다 — 새 요구 append 로 소진된다.
        self.assertEqual(len(_gate_required_events(store, self.ESC_GATE)), 2, "새 요구 append")
        self.assertEqual([g["gate_id"] for g in result.pending_gates], [self.ESC_GATE])
        self.assertEqual(
            [g["gate_id"] for g in pending_gates(store.read_all(), _escalation_policy())],
            [self.ESC_GATE], "파생 뷰도 여전히 pending")


# ==========================================================================
# 백로그 §L Desired 4 — per-unit timeout (D-T3~D-T5)
#
# 전역 timeout 하나가 규모가 다른 단위를 같은 예산에 묶는 문제를 단위별 재기입으로 푼다.
# 검증 축: ① 래퍼 순수성(원본 request 무변조)·비매칭 통과·속성 투과 ② 맵 파생(유효값만)
# ③ 3 디스패치 경로(exec·CP2·게이트) 균일 적용 ④ timeout 부재 그래프 거동 보존(래핑 0).
# ==========================================================================
from orchestrator import (  # noqa: E402
    TASK_TIMEOUT_KEY,
    UnitTimeoutInvoker,
)
from stephost_bridge import InvokeRequest  # noqa: E402


GLOBAL_TIMEOUT = 999
UNIT_TIMEOUT = 1200


def timeout_task(tid, timeout=None, depends_on=None):
    """task_payload 에 선택 timeout 키를 얹은 07 Task(개방 데이터·11키 무변)."""
    task = task_payload(tid, depends_on=depends_on)
    if timeout is not None:
        task[TASK_TIMEOUT_KEY] = timeout
    return task


class _RecordingInvoker(Invoker):
    """수신 request 의 (role, step_id, timeout) 을 그대로 기록하는 중립 stub.

    Verifier(CP2)·Advisor(게이트 승인) 반환은 Pass verdict — 게이트 경로가 escalation 으로
    빠지지 않게 해 3 경로를 한 run 에서 전부 관측한다.
    """

    def __init__(self):
        self.seen = []  # (role, step_id, timeout)
        self.requests = []

    def invoke(self, request):
        step_id = (request.bundle.get("step_contract") or {}).get("id")
        self.seen.append((request.role, step_id, request.timeout))
        self.requests.append(request)
        if request.role in (ROLE_VERIFIER, ROLE_ADVISOR):
            return _verdict_pass()
        return _completion(step_id)

    def timeouts_for(self, role, step_id):
        return [t for (r, sid, t) in self.seen if r == role and sid == step_id]


def _approval_everywhere_policy():
    """전역 기본(tier 0) approval_required — 모든 Passed 단위가 게이트 디스패치를 탄다."""
    from gates import GatePolicyEntry

    return GatePolicy(
        entries=[GatePolicyEntry(target={}, gate=GATE_APPROVAL_REQUIRED)],
        user_actor_class="human",
        escalation_resolvers=("Advisor", "human"),
    )


class PerUnitTimeout_Wrapper(unittest.TestCase):
    """UnitTimeoutInvoker 단위 계약(순수 재기입·비매칭 통과·속성 투과)."""

    def _request(self, step_id, timeout=GLOBAL_TIMEOUT):
        return InvokeRequest(
            bundle={"step_contract": {"id": step_id}}, role=ROLE_WORKER, timeout=timeout)

    def test_matching_unit_is_rewritten_and_original_untouched(self):
        inv = _RecordingInvoker()
        wrapped = UnitTimeoutInvoker(inv, {"s1": UNIT_TIMEOUT})
        req = self._request("s1")
        wrapped.invoke(req)

        self.assertEqual(inv.seen[0][2], UNIT_TIMEOUT, "매칭 단위는 단위 예산으로 재기입")
        self.assertEqual(req.timeout, GLOBAL_TIMEOUT, "원본 request 객체는 무변조(순수)")
        self.assertIsNot(inv.requests[0], req, "재기입은 새 객체(dataclasses.replace)")

    def test_non_matching_unit_passes_original_request_object(self):
        inv = _RecordingInvoker()
        wrapped = UnitTimeoutInvoker(inv, {"s1": UNIT_TIMEOUT})
        req = self._request("s2")
        wrapped.invoke(req)

        self.assertEqual(inv.seen[0][2], GLOBAL_TIMEOUT, "비매칭은 전역값 그대로")
        self.assertIs(inv.requests[0], req, "비매칭은 원 request 객체 그대로 통과")

    def test_absent_step_contract_passes_through(self):
        inv = _RecordingInvoker()
        wrapped = UnitTimeoutInvoker(inv, {"s1": UNIT_TIMEOUT})
        req = InvokeRequest(bundle={}, role=ROLE_WORKER, timeout=GLOBAL_TIMEOUT)
        wrapped.invoke(req)
        self.assertIs(inv.requests[0], req, "step_contract 부재는 원 request 그대로")

    def test_attribute_passthrough(self):
        inv = _RecordingInvoker()
        inv.invoke_count = 7  # 런처·관측이 읽는 속성(HeartbeatInvoker 선례 동형).
        wrapped = UnitTimeoutInvoker(inv, {"s1": UNIT_TIMEOUT})
        self.assertEqual(wrapped.invoke_count, 7, "래퍼는 inner 속성을 투과해야 한다")
        self.assertEqual(wrapped.timeouts_for(ROLE_WORKER, "s1"), [], "메서드도 투과")


class PerUnitTimeout_MapDerivation(unittest.TestCase):
    """맵 원천 = active_graph 파생. 유효값(양의 정수·bool 제외)만 편입한다(D-T4)."""

    def _orch(self, tasks):
        graph = {"goal": "goal", "tasks": tasks, "completion": "all-passed"}
        return ProjectOrchestrator(
            RevisionLedger(InMemoryRevisionStore(), graph),
            InMemoryEventStore(), _RecordingInvoker(), timeout=GLOBAL_TIMEOUT)

    def test_only_positive_ints_enter_the_map(self):
        orch = self._orch([
            timeout_task("ok", UNIT_TIMEOUT),
            timeout_task("absent"),
            timeout_task("zero", 0),
            timeout_task("negative", -5),
            timeout_task("boolean", True),
            timeout_task("string", "1200"),
            timeout_task("float", 1200.5),
        ])
        self.assertEqual(orch._unit_timeouts(), {"ok": UNIT_TIMEOUT})

    def test_empty_map_means_zero_wrapping(self):
        orch = self._orch([timeout_task("a"), timeout_task("b")])
        self.assertEqual(orch._unit_timeouts(), {})
        self.assertIs(orch._effective_invoker(), orch.invoker,
                      "맵 공집합이면 래핑 0 — 기존 반환 그대로(거동 보존)")

    def test_non_empty_map_wraps_outermost(self):
        orch = self._orch([timeout_task("a", UNIT_TIMEOUT)])
        eff = orch._effective_invoker()
        self.assertIsInstance(eff, UnitTimeoutInvoker, "비공집합이면 최외곽 래핑")
        self.assertIs(eff._inner, orch.invoker)

    def test_artifact_capturing_wrapper_stays_inside(self):
        # 포집 래퍼가 있는 조립에서도 timeout 래퍼가 최외곽이고 포집 배선은 무변이다.
        from artifacts import ArtifactCapturingInvoker, InMemoryArtifactDeclarationStore

        graph = {"goal": "goal", "tasks": [timeout_task("a", UNIT_TIMEOUT)],
                 "completion": "all-passed"}
        orch = ProjectOrchestrator(
            RevisionLedger(InMemoryRevisionStore(), graph),
            InMemoryEventStore(), _RecordingInvoker(), timeout=GLOBAL_TIMEOUT,
            artifact_store=InMemoryArtifactDeclarationStore())
        eff = orch._effective_invoker()
        self.assertIsInstance(eff, UnitTimeoutInvoker)
        self.assertIsInstance(eff._inner, ArtifactCapturingInvoker)
        self.assertIs(eff._inner.inner, orch.invoker)


class PerUnitTimeout_DispatchPaths(unittest.TestCase):
    """exec·CP2·게이트 디스패치 3경로에 같은 단위 예산이 균일 적용된다(D-T5)."""

    def _run(self, tasks, *, gate_policy):
        store = InMemoryEventStore()
        ledger = RevisionLedger(
            InMemoryRevisionStore(),
            {"goal": "goal", "tasks": tasks, "completion": "all-passed"})
        inv = _RecordingInvoker()
        orch = ProjectOrchestrator(
            ledger, store, inv, timeout=GLOBAL_TIMEOUT, gate_policy=gate_policy)
        result = orch.run()
        return inv, result

    def test_three_paths_receive_unit_timeout(self):
        inv, result = self._run(
            [timeout_task("s1", UNIT_TIMEOUT), timeout_task("s2", depends_on=["s1"])],
            gate_policy=_approval_everywhere_policy())
        self.assertTrue(result.completed, "게이트 Pass 승인으로 완주해야 한다: %r" % (result,))

        # 지정 단위(s1) — exec(Worker)·CP2(Verifier)·게이트(Advisor) 셋 다 단위 예산.
        self.assertEqual(inv.timeouts_for(ROLE_WORKER, "s1"), [UNIT_TIMEOUT], "exec 경로")
        self.assertEqual(inv.timeouts_for(ROLE_VERIFIER, "s1"), [UNIT_TIMEOUT], "CP2 경로")
        self.assertEqual(inv.timeouts_for(ROLE_ADVISOR, "s1"), [UNIT_TIMEOUT], "게이트 경로")

        # 미지정 단위(s2) — 3경로 전부 전역값(전역 fallback 보존·D-T7).
        for role in (ROLE_WORKER, ROLE_VERIFIER, ROLE_ADVISOR):
            self.assertEqual(inv.timeouts_for(role, "s2"), [GLOBAL_TIMEOUT],
                             "미지정 단위는 전역 예산: role=%r" % (role,))

    def test_graph_without_timeout_preserves_global_everywhere(self):
        # 거동 보존 — timeout 필드가 없는 그래프는 래핑 0 경로이며 전 요청이 전역값이다.
        inv, result = self._run(
            [timeout_task("s1"), timeout_task("s2", depends_on=["s1"])],
            gate_policy=_approval_everywhere_policy())
        self.assertTrue(result.completed)
        self.assertTrue(inv.seen, "요청이 실제로 발생했어야 한다")
        self.assertEqual({t for (_r, _s, t) in inv.seen}, {GLOBAL_TIMEOUT})

    def test_promoted_task_timeout_applies_after_revision(self):
        # revision 승격(task_added)으로 들어온 단위의 timeout 도 같은 맵 파생을 탄다
        # (맵 원천 = active_graph 이므로 fold 반영 즉시 유효 — 제2 진리원천 0).
        store = InMemoryEventStore()
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        inv = _RecordingInvoker()
        orch = ProjectOrchestrator(ledger, store, inv, timeout=GLOBAL_TIMEOUT)

        # 게이트 근거 append 후 승격 — 그래프 fold 에 timeout 을 실은 단위가 편입된다.
        _append_gate_event(orch, "g-s3-timeout")
        orch.accept_revision(
            KIND_TASK_ADDED, timeout_task("s3", UNIT_TIMEOUT, depends_on=["s2"]),
            proposingStepRef="s2#1", gateEventRef="g-s3-timeout",
        )

        result = orch.run()
        self.assertTrue(result.completed)
        self.assertEqual(inv.timeouts_for(ROLE_WORKER, "s3"), [UNIT_TIMEOUT])
        self.assertEqual(inv.timeouts_for(ROLE_WORKER, "s1"), [GLOBAL_TIMEOUT])


if __name__ == "__main__":
    unittest.main(verbosity=2)
