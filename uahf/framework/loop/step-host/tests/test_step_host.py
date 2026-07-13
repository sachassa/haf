"""Step Host 자체 테스트 (표준 라이브러리 unittest 만·외부 의존 0).

stub invoker(ScriptedInvoker)로 프로토콜 §4·§5·§6 의 전건을 커버한다:

  1. 정상 완주 (CP1 -> CP2 독립 -> Passed)
  2. 실패 -> feedback 주입 재시도
  3. 재시도 한도 초과 -> Escalated
  4. blocked -> Escalated + 정지 신호
  5. 크래시 재개 결정성 (동일 로그 2회 재생 -> 동일 재개 집합)
  6. Active 잔존 -> Failed(실행 중단) 처리
  7. unrestricted 에서도 Escalated 정지 (게이트 등급 분리) + CP2 우회 없음
  8. 필수 필드 누락 -> 디스패치 거부
  9. append-only (로그 재기록 없음)

이 파일은 특정 provider·실행 환경 토큰을 두지 않는다 — stub invoker 는 중립이다.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

# 이 테스트가 대상 모듈을 flat 임포트할 수 있도록 step-host 디렉터리를 sys.path 에 넣는다.
_STEP_HOST_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _STEP_HOST_DIR not in sys.path:
    sys.path.insert(0, _STEP_HOST_DIR)

from events import (  # noqa: E402
    ACTIVE,
    ESCALATED,
    FAILED,
    InMemoryEventStore,
    JsonlEventStore,
    PASSED,
    PENDING,
)
from host import DEFAULT_RETRY_LIMIT, StepHost  # noqa: E402
from invoker import (  # noqa: E402
    Invoker,
    InvokeRequest,
    InvokeResult,
    KIND_BLOCKED,
    KIND_COMPLETION,
    KIND_FAILURE,
    POLICY_INTERACTIVE,
    POLICY_UNRESTRICTED,
    ROLE_VERIFIER,
    ROLE_WORKER,
    load_invoker,
)
from step import Step  # noqa: E402


# --------------------------------------------------------------------------
# 테스트 픽스처 — 중립 stub invoker
# --------------------------------------------------------------------------
def completion(artifacts=("art",), **extra):
    payload = {"artifacts": list(artifacts), "self_check": "done", "failures": "없음",
               "open_questions": "없음", "verify_basis": "self-test"}
    payload.update(extra)
    return InvokeResult(kind=KIND_COMPLETION, completion=payload, ref="wr")


def failure(reason="beta 결함", repro="입력 X"):
    return InvokeResult(kind=KIND_FAILURE,
                        failure={"reason": reason, "repro": repro, "blocking": "계속 가능"},
                        ref="fr")


def blocked(reason="의존 계약 미확정"):
    return InvokeResult(kind=KIND_BLOCKED,
                        failure={"reason": reason, "blocking": "차단됨"},
                        ref="blk")


def verdict(passed=True, rework=None):
    return InvokeResult(kind=KIND_COMPLETION,
                        completion={"verdict": "Pass" if passed else "Fail", "rework": rework},
                        ref="vd")


class ScriptedInvoker(Invoker):
    """역할·Step 별 스크립트대로 반환하는 stub. 실행 표면·provider 는 없다."""

    def __init__(self, worker=None, worker_default=None, verifier=None, verifier_default=None):
        self.worker = {k: list(v) for k, v in (worker or {}).items()}
        self.worker_default = worker_default or {}
        self.verifier = {k: list(v) for k, v in (verifier or {}).items()}
        self.verifier_default = verifier_default or {}
        # 관찰 기록: 각 호출의 (role, step_id, policy, feedback 존재).
        self.calls = []

    def invoke(self, request: InvokeRequest) -> InvokeResult:
        step_id = (request.bundle.get("step_contract") or {}).get("id")
        self.calls.append({
            "role": request.role,
            "step_id": step_id,
            "policy": request.policy,
            "feedback": request.bundle.get("feedback"),
        })
        if request.role == ROLE_VERIFIER:
            script = self.verifier.get(step_id)
            if script:
                return script.pop(0)
            return self.verifier_default.get(step_id, verdict(passed=True))
        script = self.worker.get(step_id)
        if script:
            return script.pop(0)
        return self.worker_default.get(step_id, completion())

    def worker_calls(self, step_id=None):
        return [c for c in self.calls if c["role"] == ROLE_WORKER
                and (step_id is None or c["step_id"] == step_id)]

    def verifier_calls(self, step_id=None):
        return [c for c in self.calls if c["role"] == ROLE_VERIFIER
                and (step_id is None or c["step_id"] == step_id)]


def make_step(step_id, depends_on=None, done="AC-1", ifc=None, delegation_over=None):
    delegation = {
        "from": "Advisor", "to": "Worker", "task": "구현", "input": "in-" + step_id,
        "output": "out-" + step_id, "done": "AC-1", "context": ["doc-a"],
        "constraints": None,
    }
    if delegation_over:
        delegation.update(delegation_over)
    return Step(
        id=step_id, task="구현", done=done,
        interfaceContract=(ifc if ifc is not None else {"produces": ["c-" + step_id]}),
        ownedBoundary=["file-" + step_id], dependsOn=list(depends_on or []),
        delegation=delegation, role=ROLE_WORKER, capability="cap", model="slot-model",
    )


class StopRecorder:
    def __init__(self):
        self.calls = []

    def __call__(self, reason, tasks):
        self.calls.append((reason, list(tasks)))


# --------------------------------------------------------------------------
# 시나리오 테스트
# --------------------------------------------------------------------------
class Scenario1Normal(unittest.TestCase):
    def test_normal_run_cp1_cp2_passed(self):
        inv = ScriptedInvoker()
        host = StepHost([make_step("s1")], inv)
        result = host.run()

        self.assertTrue(result.completed, result.status)
        self.assertEqual(result.states["s1"], PASSED)
        # CP1(Worker) 과 CP2(Verifier)가 각각 별도 디스패치됐다(자가판정 완료 확정 금지).
        self.assertEqual(len(inv.worker_calls("s1")), 1)
        self.assertEqual(len(inv.verifier_calls("s1")), 1)
        # Passed 는 CP2 Pass 후에만 append 된다.
        events = host.log.events_for("s1")
        passed = [e for e in events if e["to_stage"] == "Complete" and e["outcome"] == "pass"]
        self.assertEqual(len(passed), 1)
        self.assertEqual(passed[0]["actor"], ROLE_VERIFIER)


class Scenario2RetryFeedback(unittest.TestCase):
    def test_failure_then_feedback_retry(self):
        inv = ScriptedInvoker(worker={"s1": [failure(reason="1차 결함", repro="repro-1"),
                                             completion()]})
        host = StepHost([make_step("s1")], inv)
        result = host.run()

        self.assertTrue(result.completed, result.status)
        self.assertEqual(result.states["s1"], PASSED)
        # 2회 디스패치(1차 실패·2차 성공).
        wcalls = inv.worker_calls("s1")
        self.assertEqual(len(wcalls), 2)
        # 1차 디스패치 feedback 없음, 2차 디스패치 feedback 주입(직전 실패 보고 파생).
        self.assertIsNone(wcalls[0]["feedback"])
        self.assertIsNotNone(wcalls[1]["feedback"])
        self.assertEqual(wcalls[1]["feedback"]["reason"], "1차 결함")
        self.assertEqual(wcalls[1]["feedback"]["repro"], "repro-1")
        # Failed 이벤트가 로그에 남아 은폐되지 않는다.
        fails = [e for e in host.log.events_for("s1") if e["outcome"] == "fail"]
        self.assertEqual(len(fails), 1)
        # 재디스패치의 retry_count 증가.
        dispatches = [e for e in host.log.events_for("s1")
                      if e["to_stage"] == "Execute" and (e.get("ref") or {}).get("kind") == "dispatch"]
        self.assertEqual(dispatches[0]["retry_count"], 0)
        self.assertEqual(dispatches[1]["retry_count"], 1)


class Scenario3RetryLimitExceeded(unittest.TestCase):
    def test_retry_limit_exceeded_escalates(self):
        stop = StopRecorder()
        inv = ScriptedInvoker(worker_default={"s1": failure()})  # 항상 실패
        host = StepHost([make_step("s1")], inv, retry_limit=2, stop_handler=stop)
        result = host.run()

        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.states["s1"], ESCALATED)
        self.assertEqual(result.stop_reason, "escalated")
        # 한도 2 -> 시도 3회(retry_count 0·1·2) 후 Escalated.
        self.assertEqual(len(inv.worker_calls("s1")), 3)
        fails = [e for e in host.log.events_for("s1") if e["outcome"] == "fail"]
        self.assertEqual(len(fails), 3)
        esc = [e for e in host.log.events_for("s1") if e["outcome"] == "escalated"]
        self.assertEqual(len(esc), 1)
        self.assertEqual(esc[0]["ref"]["kind"], "retry-limit-exceeded")
        # 정지 신호 발생.
        self.assertEqual(len(stop.calls), 1)
        self.assertEqual(stop.calls[0][0], "escalated")


class Scenario4Blocked(unittest.TestCase):
    def test_blocked_escalates_and_stops(self):
        stop = StopRecorder()
        inv = ScriptedInvoker(worker={"s1": [blocked()]})
        host = StepHost([make_step("s1")], inv, stop_handler=stop)
        result = host.run()

        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.states["s1"], ESCALATED)
        # 차단은 재시도하지 않고 즉시 Escalated + 정지 신호.
        self.assertEqual(len(inv.worker_calls("s1")), 1)
        self.assertEqual(len(inv.verifier_calls("s1")), 0)  # CP2 도달 전 차단.
        esc = [e for e in host.log.events_for("s1") if e["outcome"] == "escalated"]
        self.assertEqual(esc[0]["ref"]["kind"], "blocked")
        self.assertEqual(len(stop.calls), 1)


class Scenario5DeterministicResume(unittest.TestCase):
    def test_same_log_same_ready_set(self):
        # A Passed, B·C 는 A 의존. 파일 기반 로그로 두 재개 인스턴스가 동일 로그를 재생.
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "run.jsonl")
            store = JsonlEventStore(path)
            steps = [make_step("A"), make_step("B", depends_on=["A"]),
                     make_step("C", depends_on=["A"]), make_step("D", depends_on=["B", "C"])]
            # A 를 Passed 로 만든다(디스패치 + CP2 Pass).
            seeder = StepHost(steps, ScriptedInvoker(), store=store)
            seeder.log.append(cycle_id="A", to_stage="Execute", trigger="완료 조건 충족",
                              outcome="pass", actor=ROLE_WORKER, ref={"kind": "dispatch"})
            seeder.log.append(cycle_id="A", from_stage="Verify", to_stage="Complete",
                              trigger="완료 조건 충족", outcome="pass", actor=ROLE_VERIFIER,
                              ref={"kind": "cp2-pass"})

            # 두 개의 독립 재개 인스턴스가 같은 파일을 읽는다.
            h1 = StepHost(steps, ScriptedInvoker(), store=JsonlEventStore(path))
            h2 = StepHost(steps, ScriptedInvoker(), store=JsonlEventStore(path))
            r1 = h1.ready_set()
            r2 = h2.ready_set()

            self.assertEqual(r1, r2)
            self.assertEqual(r1, ["B", "C"])  # A 완료 -> B·C 준비, D 는 대기.
            self.assertEqual(h1.derive_states()["A"], PASSED)
            self.assertEqual(h1.derive_states()["D"], PENDING)
            # 재생은 로그를 변경하지 않는다(순수 판독).
            self.assertEqual(len(JsonlEventStore(path).read_all()), 2)


class Scenario6ActiveRemnant(unittest.TestCase):
    def test_active_remnant_becomes_failed_interrupted(self):
        store = InMemoryEventStore()
        steps = [make_step("s1")]
        host = StepHost(steps, ScriptedInvoker(), store=store)
        # 디스패치만 하고 완료 없이 중단된 흔적 -> Active.
        host.log.append(cycle_id="s1", to_stage="Execute", trigger="완료 조건 충족",
                        outcome="pass", actor=ROLE_WORKER, ref={"kind": "dispatch"})
        self.assertEqual(host.derive_states()["s1"], ACTIVE)

        host.recover_active_remnants()

        self.assertEqual(host.derive_states()["s1"], FAILED)
        interrupted = [e for e in host.log.events_for("s1")
                       if e["outcome"] == "fail" and (e.get("ref") or {}).get("kind") == "interrupted"]
        self.assertEqual(len(interrupted), 1)

    def test_full_run_recovers_and_completes(self):
        store = InMemoryEventStore()
        steps = [make_step("s1")]
        # 재개 후 재디스패치는 성공한다.
        host = StepHost(steps, ScriptedInvoker(), store=store)
        host.log.append(cycle_id="s1", to_stage="Execute", trigger="완료 조건 충족",
                        outcome="pass", actor=ROLE_WORKER, ref={"kind": "dispatch"})
        result = host.run()
        self.assertTrue(result.completed, result.status)
        self.assertEqual(result.states["s1"], PASSED)


class Scenario7GateSeparation(unittest.TestCase):
    def test_unrestricted_still_stops_on_escalated(self):
        stop = StopRecorder()
        inv = ScriptedInvoker(worker={"s1": [blocked()]})
        host = StepHost([make_step("s1")], inv, policy=POLICY_UNRESTRICTED, stop_handler=stop)
        result = host.run()
        # unrestricted 에서도 Escalated 는 정지된다(SH-INV-4).
        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.states["s1"], ESCALATED)
        self.assertEqual(len(stop.calls), 1)
        # policy 는 데이터로 invoker 에 그대로 전달된다.
        self.assertEqual(inv.worker_calls("s1")[0]["policy"], POLICY_UNRESTRICTED)

    def test_unrestricted_does_not_bypass_cp2(self):
        inv = ScriptedInvoker()
        host = StepHost([make_step("s1")], inv, policy=POLICY_UNRESTRICTED)
        result = host.run()
        self.assertTrue(result.completed)
        # 정상 완료여도 CP2(Verifier)가 반드시 디스패치된다 — 우회 없음.
        self.assertEqual(len(inv.verifier_calls("s1")), 1)
        self.assertEqual(inv.verifier_calls("s1")[0]["policy"], POLICY_UNRESTRICTED)

    def test_cp2_fail_under_unrestricted_retries_not_passes(self):
        inv = ScriptedInvoker(verifier={"s1": [verdict(passed=False, rework="다시"),
                                               verdict(passed=True)]})
        host = StepHost([make_step("s1")], inv, policy=POLICY_UNRESTRICTED)
        result = host.run()
        self.assertTrue(result.completed)
        self.assertEqual(result.states["s1"], PASSED)
        # CP2 Fail 은 재작업(feedback=rework)으로 이어진다 — unrestricted 여도 통과 확정 없음.
        wcalls = inv.worker_calls("s1")
        self.assertEqual(len(wcalls), 2)
        self.assertEqual(wcalls[1]["feedback"]["kind"], "rework")
        self.assertEqual(wcalls[1]["feedback"]["rework"], "다시")


class Scenario8MissingFields(unittest.TestCase):
    def test_missing_required_field_refuses_dispatch(self):
        stop = StopRecorder()
        # delegation.input 누락(빈 문자열).
        step = make_step("s1", delegation_over={"input": ""})
        inv = ScriptedInvoker()
        host = StepHost([step], inv, stop_handler=stop)
        result = host.run()

        self.assertTrue(result.stopped, result.status)
        self.assertEqual(result.states["s1"], ESCALATED)
        # 디스패치 자체가 없다 — Worker/Verifier 호출 0.
        self.assertEqual(len(inv.calls), 0)
        esc = [e for e in host.log.events_for("s1") if e["outcome"] == "escalated"]
        self.assertEqual(esc[0]["ref"]["kind"], "scoped-query")
        self.assertIn("delegation.input", esc[0]["ref"]["missing"])

    def test_missing_task_field_refuses_dispatch(self):
        step = make_step("s1", done="")  # Task done 누락.
        inv = ScriptedInvoker()
        host = StepHost([step], inv)
        result = host.run()
        self.assertTrue(result.stopped)
        esc = [e for e in host.log.events_for("s1") if e["outcome"] == "escalated"]
        self.assertIn("done", esc[0]["ref"]["missing"])


class Scenario9AppendOnly(unittest.TestCase):
    def test_append_only_no_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "run.jsonl")
            store = JsonlEventStore(path)
            steps = [make_step("s1"), make_step("s2", depends_on=["s1"])]
            inv = ScriptedInvoker(worker={"s1": [failure(), completion()]})
            host = StepHost(steps, inv, store=store)
            result = host.run()
            self.assertTrue(result.completed, result.status)

            with open(path, "r", encoding="utf-8") as fh:
                lines_after_first = fh.read().splitlines()

            all_events = store.read_all()
            # 파일 라인 수 = 이벤트 수(1행 1이벤트).
            self.assertEqual(len(lines_after_first), len(all_events))
            # at 은 전역 단조 증가(1..N)로 append 순서를 확정한다.
            ats = [e["at"] for e in all_events]
            self.assertEqual(ats, list(range(1, len(all_events) + 1)))
            # seq 는 cycle 별 단조 증가.
            for cid in ("s1", "s2"):
                seqs = [e["seq"] for e in host.log.events_for(cid)]
                self.assertEqual(seqs, list(range(1, len(seqs) + 1)))

            # 추가 append 후에도 기존 라인은 접두로 보존된다(재기록 없음).
            store.append({"cycle_id": "s2", "seq": 99, "from_stage": None,
                          "to_stage": "X", "trigger": "완료 조건 충족", "outcome": "pass",
                          "retry_count": 0, "actor": ROLE_WORKER, "ref": None, "at": 999})
            with open(path, "r", encoding="utf-8") as fh:
                lines_after_second = fh.read().splitlines()
            self.assertEqual(lines_after_second[:len(lines_after_first)], lines_after_first)
            self.assertEqual(len(lines_after_second), len(lines_after_first) + 1)


class InvokerLoaderTest(unittest.TestCase):
    """config 모듈 경로 문자열로 invoker 를 로드한다 — 중립 코드에 구현체 이름 0."""

    def test_load_invoker_by_module_path(self):
        inv = load_invoker(__name__ + ":ScriptedInvoker")
        self.assertIsInstance(inv, Invoker)

    def test_load_invoker_rejects_non_invoker(self):
        with self.assertRaises(TypeError):
            load_invoker(__name__ + ":make_step")

    def test_load_invoker_rejects_bad_path(self):
        with self.assertRaises(ValueError):
            load_invoker("no_colon_here")


class MultiStepGraphTest(unittest.TestCase):
    """병렬 집합(선행 의존 완료) 논리로 여러 Step 을 순차 완주한다."""

    def test_diamond_graph_completes(self):
        steps = [make_step("A"), make_step("B", depends_on=["A"]),
                 make_step("C", depends_on=["A"]), make_step("D", depends_on=["B", "C"])]
        inv = ScriptedInvoker()
        host = StepHost(steps, inv)
        result = host.run()
        self.assertTrue(result.completed, result.status)
        for sid in ("A", "B", "C", "D"):
            self.assertEqual(result.states[sid], PASSED)


if __name__ == "__main__":
    unittest.main(verbosity=2)
