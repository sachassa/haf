"""T3 W1(러너 위생·검사 경계) + W3(섀도 스텁) + W4(delegation 참조형) 단위 테스트.

표준 라이브러리 unittest + pytest 수집. 실 CLI 0(합성 스텁)·run 원장 무접촉(임시 dir).
conftest.py 가 상위 e2e/ 를 sys.path 에 배선한다.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import delegation_check as dc
import verify_run as vr
from _orch_common import LoggingClaudeInvoker
from invoker import InvokeRequest, InvokeResult, KIND_COMPLETION, ROLE_VERIFIER, ROLE_WORKER


# ==========================================================================
# W4 — delegation 참조형 표준 경계
# ==========================================================================
def _task(top_task, top_done, dg_task, dg_done):
    return {
        "id": "t", "task": top_task, "done": top_done,
        "delegation": {"from": "Advisor", "to": "Worker", "task": dg_task,
                       "input": "in", "output": "out", "done": dg_done, "context": ["d"]},
    }


class DelegationReferenceForm(unittest.TestCase):
    def test_sentinel_form_passes(self):
        t = _task("전체 task 문면", "python -c ...", dc.SENTINEL_TASK, dc.SENTINEL_DONE)
        self.assertEqual(dc.delegation_errors_for_task(t), [])

    def test_verbatim_form_passes(self):
        t = _task("전체 task 문면", "python -c ...", "전체 task 문면", "python -c ...")
        self.assertEqual(dc.delegation_errors_for_task(t), [])

    def test_mixed_sentinel_task_verbatim_done_passes(self):
        t = _task("T", "D", dc.SENTINEL_TASK, "D")
        self.assertEqual(dc.delegation_errors_for_task(t), [])

    def test_summary_form_fails(self):
        # 요약/변형은 sentinel 도 원문 전재도 아니므로 실패.
        t = _task("전체 긴 task 문면 원문", "python -c 원문", "task 요약", "done 요약")
        errs = dc.delegation_errors_for_task(t)
        self.assertEqual(len(errs), 2)  # task·done 둘 다.

    def test_partial_excerpt_fails(self):
        t = _task("전체 긴 문면 ABCDEF", "python -c full", "전체 긴 문면", "python -c full")
        errs = dc.delegation_errors_for_task(t)
        self.assertEqual(len(errs), 1)  # task 부분 발췌만 실패(done 은 원문 전재라 통과).

    def test_missing_delegation_fails(self):
        errs = dc.delegation_errors_for_task({"id": "t", "task": "T", "done": "D"})
        self.assertTrue(errs)

    def test_non_string_delegation_task_fails(self):
        t = _task("T", "D", None, dc.SENTINEL_DONE)
        errs = dc.delegation_errors_for_task(t)
        self.assertEqual(len(errs), 1)


# ==========================================================================
# W1 — 러너 위생·검사 함수 (임시 run dir·순수 판독)
# ==========================================================================
def _write_run(tmp, events=None, graph=None, revisions=None, artifacts=None, config=None):
    d = Path(tmp)
    if config is not None:
        (d / "config.json").write_text(json.dumps(config), encoding="utf-8")
    if graph is not None:
        (d / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
    for name, rows in (("events.jsonl", events), ("revisions.jsonl", revisions),
                       ("artifacts.jsonl", artifacts)):
        if rows is not None:
            (d / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                                  encoding="utf-8")
    return d


def _ev(cycle, seq, at, outcome="pass", kind="dispatch", **ref_extra):
    ref = {"kind": kind}
    ref.update(ref_extra)
    return {"cycle_id": cycle, "seq": seq, "at": at, "from_stage": None, "to_stage": "Execute",
            "trigger": "t", "outcome": outcome, "retry_count": 0, "actor": "Worker", "ref": ref}


class GateOrderCheck(unittest.TestCase):
    def test_good_order_passes(self):
        events = [
            {"cycle_id": "gate::g", "at": 1, "ref": {"kind": "gate-required", "gate_id": "g",
                                                      "gateKind": "user_decision_required"}},
            {"cycle_id": "ann::g", "at": 2, "ref": {"kind": "user-resolution-provenance", "gate_id": "g"}},
            {"cycle_id": "gate::g", "at": 3, "ref": {"kind": "gate-resolved", "gate_id": "g",
                                                      "gateKind": "user_decision_required"}},
        ]
        self.assertEqual(vr._check_gate_order(events), [])

    def test_resolved_before_required_fails(self):
        events = [
            {"cycle_id": "gate::g", "at": 1, "ref": {"kind": "gate-resolved", "gate_id": "g"}},
            {"cycle_id": "gate::g", "at": 2, "ref": {"kind": "gate-required", "gate_id": "g"}},
        ]
        self.assertTrue(vr._check_gate_order(events))

    def test_resolved_without_required_fails(self):
        events = [{"cycle_id": "gate::g", "at": 1, "ref": {"kind": "gate-resolved", "gate_id": "g"}}]
        self.assertTrue(vr._check_gate_order(events))


class LedgerHygieneCheck(unittest.TestCase):
    def test_clean_ledger_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = [_ev("d1", 1, 1), _ev("d1", 2, 2, kind="cp2-pass", verdict_ref="v")]
            d = _write_run(tmp, events=events)
            r = vr.check_ledger_hygiene(d)
            self.assertEqual(r["status"], "pass", r["findings"])

    def test_unknown_ref_kind_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = [_ev("d1", 1, 1, kind="bogus-kind")]
            d = _write_run(tmp, events=events)
            r = vr.check_ledger_hygiene(d)
            self.assertEqual(r["status"], "fail")

    def test_nonmonotonic_at_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = [_ev("d1", 1, 1), _ev("d1", 2, 5)]  # at gap.
            d = _write_run(tmp, events=events)
            r = vr.check_ledger_hygiene(d)
            self.assertEqual(r["status"], "fail")

    def test_bad_outcome_vocab_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = [_ev("d1", 1, 1, outcome="weird")]
            d = _write_run(tmp, events=events)
            r = vr.check_ledger_hygiene(d)
            self.assertEqual(r["status"], "fail")

    def test_human_actor_simulated_true_is_contradiction(self):
        with tempfile.TemporaryDirectory() as tmp:
            ev = _ev("ann::g", 1, 1, kind="user-resolution-provenance", gate_id="g", simulated=True)
            ev["actor"] = "human"
            d = _write_run(tmp, events=[ev])
            r = vr.check_ledger_hygiene(d)
            self.assertEqual(r["status"], "fail")


class DelegationCheckRunner(unittest.TestCase):
    def test_graph_verbatim_and_sentinel_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            graph = {"tasks": [
                _task("Tv", "Dv", "Tv", "Dv"),            # verbatim.
            ]}
            graph["tasks"][0]["id"] = "a"
            revs = [{"revisionSeq": 1, "kind": "task_added",
                     "payload": {"id": "b", "task": "Tb", "done": "Db",
                                 "delegation": {"task": dc.SENTINEL_TASK, "done": dc.SENTINEL_DONE}},
                     "basis": {}}]
            d = _write_run(tmp, graph=graph, revisions=revs)
            r = vr.check_delegation(d)
            self.assertEqual(r["status"], "pass", r["findings"])
            self.assertEqual(r["detail"]["tasks_checked"], 2)

    def test_graph_summary_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = _task("전체 원문 task 문면 길다", "python -c full", "요약된 task", "요약된 done")
            t["id"] = "a"
            d = _write_run(tmp, graph={"tasks": [t]})
            r = vr.check_delegation(d)
            self.assertEqual(r["status"], "fail")


class RevisionIntegrityCheck(unittest.TestCase):
    def _base_graph(self):
        return {"goal": "g", "tasks": [{"id": "A", "done": "AC", "interfaceContract": {"produces": ["a"]},
                                        "ownedBoundary": ["fa"], "dependsOn": []}], "completion": "all-passed"}

    def test_valid_task_added_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            revs = [{"revisionSeq": 1, "kind": "task_added",
                     "payload": {"id": "B", "done": "AC", "interfaceContract": {"produces": ["b"]},
                                 "ownedBoundary": ["fb"], "dependsOn": ["A"]},
                     "basis": {"proposingStepRef": "A", "gateEventRef": "g"}}]
            d = _write_run(tmp, graph=self._base_graph(), revisions=revs)
            r = vr.check_revision_integrity(d)
            self.assertEqual(r["status"], "pass", r["findings"])

    def test_missing_completion_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            revs = [{"revisionSeq": 1, "kind": "task_added",
                     "payload": {"id": "B", "interfaceContract": {"produces": ["b"]},
                                 "ownedBoundary": ["fb"], "dependsOn": ["A"]},  # done 누락.
                     "basis": {"proposingStepRef": "A", "gateEventRef": "g"}}]
            d = _write_run(tmp, graph=self._base_graph(), revisions=revs)
            r = vr.check_revision_integrity(d)
            self.assertEqual(r["status"], "fail")

    def test_nonmonotonic_seq_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            revs = [{"revisionSeq": 2, "kind": "task_added",
                     "payload": {"id": "B", "done": "AC", "interfaceContract": {"produces": ["b"]},
                                 "ownedBoundary": ["fb"], "dependsOn": ["A"]},
                     "basis": {"proposingStepRef": "A", "gateEventRef": "g"}}]
            d = _write_run(tmp, graph=self._base_graph(), revisions=revs)
            r = vr.check_revision_integrity(d)
            self.assertEqual(r["status"], "fail")


# ==========================================================================
# W3 — 섀도 검증 스텁(합성 invoker·실 CLI 0)
# ==========================================================================
class _StubShadowInvoker:
    def __init__(self, verdict):
        self.verdict = verdict
        self.calls = []

    def invoke(self, request):
        self.calls.append(request)
        return InvokeResult(kind=KIND_COMPLETION, completion={"verdict": self.verdict}, ref="shadow")


class _StubbedLogging(LoggingClaudeInvoker):
    """주 invoke 경로를 합성 결과로 대체(_primary_invoke seam·실 CLI 0)."""

    def __init__(self, primary_result, **kw):
        super().__init__(**kw)
        self._primary_result = primary_result

    def _primary_invoke(self, request):
        return self._primary_result


def _verifier_req():
    return InvokeRequest(bundle={"step_contract": {"id": "s1"}, "gate": {"gate_id": "g1"}},
                         role=ROLE_VERIFIER, model="primary-tier", criteria="AC")


class ShadowVerification(unittest.TestCase):
    def _primary(self, verdict="Pass"):
        return InvokeResult(kind=KIND_COMPLETION, completion={"verdict": verdict}, ref="p")

    def test_shadow_off_by_default_no_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            inv = _StubbedLogging(self._primary("Pass"), logs_dir=tmp)  # shadow 미설정.
            result = inv.invoke(_verifier_req())
            self.assertEqual(result.completion["verdict"], "Pass")
            self.assertFalse(os.path.exists(os.path.join(tmp, "shadow-verify.jsonl")))
            self.assertEqual(inv.shadow_count, 0)

    def test_shadow_agreement_recorded_primary_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            stub = _StubShadowInvoker("Pass")
            logp = os.path.join(tmp, "shadow.jsonl")
            inv = _StubbedLogging(
                self._primary("Pass"), logs_dir=tmp,
                shadow={"enabled": True, "model": "shadow-tier", "log_path": logp},
                shadow_invoker_factory=lambda: stub,
            )
            result = inv.invoke(_verifier_req())
            # 주 판정은 그대로.
            self.assertEqual(result.completion["verdict"], "Pass")
            # 섀도 재호출은 상위 모델을 썼다.
            self.assertEqual(stub.calls[0].model, "shadow-tier")
            entries = [json.loads(l) for l in open(logp, encoding="utf-8")]
            self.assertEqual(len(entries), 1)
            self.assertTrue(entries[0]["agreement"])
            self.assertEqual(entries[0]["primary_verdict"], "Pass")
            self.assertEqual(entries[0]["shadow_verdict"], "Pass")

    def test_shadow_disagreement_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            stub = _StubShadowInvoker("Fail")
            logp = os.path.join(tmp, "shadow.jsonl")
            inv = _StubbedLogging(
                self._primary("Pass"), logs_dir=tmp,
                shadow={"enabled": True, "model": "shadow-tier", "log_path": logp},
                shadow_invoker_factory=lambda: stub,
            )
            result = inv.invoke(_verifier_req())
            self.assertEqual(result.completion["verdict"], "Pass")  # 주 판정 불변.
            entries = [json.loads(l) for l in open(logp, encoding="utf-8")]
            self.assertFalse(entries[0]["agreement"])

    def test_shadow_not_applicable_for_worker(self):
        with tempfile.TemporaryDirectory() as tmp:
            stub = _StubShadowInvoker("Pass")
            logp = os.path.join(tmp, "shadow.jsonl")
            inv = _StubbedLogging(
                InvokeResult(kind=KIND_COMPLETION, completion={"artifacts": ["x"]}, ref="p"),
                logs_dir=tmp,
                shadow={"enabled": True, "model": "shadow-tier", "log_path": logp},
                shadow_invoker_factory=lambda: stub,
            )
            req = InvokeRequest(bundle={"step_contract": {"id": "s1"}}, role=ROLE_WORKER, model="m")
            inv.invoke(req)
            self.assertEqual(inv.shadow_count, 0)
            self.assertFalse(os.path.exists(logp))

    def test_shadow_failure_is_best_effort(self):
        with tempfile.TemporaryDirectory() as tmp:
            def boom():
                raise RuntimeError("shadow boom")
            logp = os.path.join(tmp, "shadow.jsonl")
            inv = _StubbedLogging(
                self._primary("Pass"), logs_dir=tmp,
                shadow={"enabled": True, "model": "shadow-tier", "log_path": logp},
                shadow_invoker_factory=boom,
            )
            result = inv.invoke(_verifier_req())
            self.assertEqual(result.completion["verdict"], "Pass")  # run 무영향.
            entries = [json.loads(l) for l in open(logp, encoding="utf-8")]
            self.assertIn("error", entries[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
