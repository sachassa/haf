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


if __name__ == "__main__":
    unittest.main(verbosity=2)
