"""resolve_gate (F5 프로덕션 게이트 resolver) 오프라인 테스트 — 실 LLM/CLI 미발화(stdlib unittest).

위임 done 1~4 를 실제 코드로 뒷받침한다:
  - done 1: 검증-먼저 — 잘못된 impl-plan(DAG 사이클)으로 실행 → 비영 종료 +
            원장(events.jsonl/revisions.jsonl) 바이트 무변경(before/after 해시 동일).
  - done 2: 정상 해소 — 유효 impl-plan(impl 2 + 통합 milestone 1)로 실행 → events.jsonl 에
            gate-resolution(actor=human) append + revisions.jsonl 에 3 task_added(각 basis=
            {proposingStepRef, gateEventRef}) append. accept_revision 이 gate-pass 재검증.
  - done 3: actor 자격 — user_decision 을 actor=Advisor 로 해소 시도 → 부적격·is_resolved False
            유지·revision 승격 0·원장 무변경.
  - done 4: escalation 해소 — escalation 게이트를 actor=Advisor 로 해소 → 적격·resolved True.

중립 코드(orchestration/framework/·uahf/**)·resolve_w 는 무수정 import 만 한다(재정의 0).
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

# --- 경로 배선: resolver 모듈 디렉터리 ----------------------------------------
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]          # orchestration/adapters/claude
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import resolve_gate as rg  # noqa: E402  (import 시 e2e·중립 코드 경로 배선)
import contract_to_graph as f4  # noqa: E402  (F4 어댑터 — gate_policy CP3 사슬 검증용)

# resolve_gate 가 이미 sys.path 에 올린 중립 코드(무수정 import).
from gates import (  # noqa: E402
    GATE_ESCALATION_REQUIRED,
    GATE_USER_DECISION_REQUIRED,
    GatePolicy,
    append_gate_requirement,
    is_resolved,
    pending_gates,
)
from events import EventLog, JsonlEventStore  # noqa: E402


# --------------------------------------------------------------------------
# 픽스처 헬퍼
# --------------------------------------------------------------------------
_SENTINEL_DELEG = {"task": "위 task 필드와 동일", "done": "위 done 필드와 동일"}


def _task(tid: str, boundary: str, deps, unit: str = "implementation"):
    return {
        "id": tid,
        "task": "구현 " + tid,
        "done": tid + " 완료 조건 충족",
        "interfaceContract": tid + " API 계약",
        "ownedBoundary": [boundary],
        "dependsOn": list(deps),
        "delegation": dict(_SENTINEL_DELEG),
        "capability": unit,
        "role": "Worker",
        "model": "sonnet",
        "unitType": unit,
    }


def _valid_plan():
    # F4 계약: implementation×2 + milestone×1. milestone 은 impl 들에 dependsOn(DAG 종단)이며
    # 아무도 milestone 을 dependsOn 하지 않는다.
    return {"tasks": [
        _task("impl-auth", "src/auth.py", []),
        _task("impl-api", "src/api.py", ["impl-auth"]),
        _task("milestone-integration", "src/integration.py", ["impl-auth", "impl-api"], "milestone"),
    ]}


def _cyclic_plan():
    # DAG 사이클(a↔b)이 유일한 결함 — milestone≥1 은 충족시켜 사이클만 거부 사유가 되게 한다.
    return {"tasks": [
        _task("impl-a", "src/a.py", ["impl-b"]),
        _task("impl-b", "src/b.py", ["impl-a"]),
        _task("milestone-m", "src/m.py", ["impl-a"], "milestone"),
    ]}


def _all_impl_plan():
    # milestone 0개(전부 implementation) — F4 계약 위반(milestone≥1)으로 거부되어야 한다.
    return {"tasks": [
        _task("impl-a", "src/a.py", []),
        _task("impl-b", "src/b.py", ["impl-a"]),
        _task("impl-c", "src/c.py", ["impl-b"]),
    ]}


def _two_milestone_plan():
    # milestone 2개 — 둘 다 DAG 종단(서로 의존 안 함·아무도 의존 안 함). 허용(각각 approval_required).
    return {"tasks": [
        _task("impl-a", "src/a.py", []),
        _task("milestone-x", "src/x.py", ["impl-a"], "milestone"),
        _task("milestone-y", "src/y.py", ["impl-a"], "milestone"),
    ]}


def _design_task():
    return {
        "id": "design", "task": "설계", "done": "설계 완료",
        "interfaceContract": "설계 문서", "ownedBoundary": ["docs/design.md"],
        "dependsOn": [], "delegation": dict(_SENTINEL_DELEG),
        "capability": "design", "role": "Advisor", "model": "opus", "unitType": "design",
    }


def _build_run(base: Path, gate_kind: str, gate_id: str, *, plan=None) -> Path:
    run = base / "run"
    (run / "logs").mkdir(parents=True)
    (run / "workspace").mkdir(parents=True)
    (run / "steps").mkdir(parents=True)

    (run / "config.json").write_text(
        json.dumps({"workspace_dir": str(run / "workspace"), "run_id": "test-run"}),
        encoding="utf-8",
    )
    (run / "graph.json").write_text(
        json.dumps({"tasks": [_design_task()]}), encoding="utf-8"
    )
    # 정책 데이터 기본값({}) — userActorClass=human·escalationResolvers=(Advisor,human).
    (run / "gate_policy.json").write_text("{}", encoding="utf-8")
    (run / "revisions.jsonl").write_text("", encoding="utf-8")
    (run / "artifacts.jsonl").write_text("", encoding="utf-8")

    # events.jsonl 에 게이트 요구 이벤트 seed(is_resolved 요구 전제·pending_gates 파생 기준).
    log = EventLog(JsonlEventStore(str(run / "events.jsonl")))
    append_gate_requirement(
        log, gate_id, gate_kind,
        target={"unitId": "impl-plan"},
        scoped_question={"unitId": "impl-plan", "gateKind": gate_kind},
    )

    # stop-signal.json = pending_gates 파생(run_orchestration.py 계약 동형).
    policy = GatePolicy.from_dict({})
    pend = pending_gates(log.all_events(), policy)
    (run / "logs" / "stop-signal.json").write_text(
        json.dumps({"stop_reason": "gate", "stopped_tasks": ["impl-plan"], "pending_gates": pend},
                   ensure_ascii=False),
        encoding="utf-8",
    )

    if plan is not None:
        (run / "workspace" / "impl-plan.json").write_text(
            json.dumps(plan, ensure_ascii=False), encoding="utf-8"
        )
    return run


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_jsonl(path: Path):
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def _events(run: Path):
    return _read_jsonl(run / "events.jsonl")


# --------------------------------------------------------------------------
# done 1 — 검증-먼저: 잘못된 impl-plan → 비영 종료 + 원장 바이트 무변경
# --------------------------------------------------------------------------
class TestValidationFirst(unittest.TestCase):
    def test_invalid_plan_leaves_ledger_untouched(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_cyclic_plan())
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")

            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])

            self.assertNotEqual(rc, 0, "잘못된 impl-plan 은 비영 종료여야 한다")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 바이트 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before, "revisions.jsonl 바이트 무변경")


# --------------------------------------------------------------------------
# done 2 — 정상 해소: gate-resolution(human) + N task_added(각 basis) + accept_revision 재검증
# --------------------------------------------------------------------------
class TestValidResolution(unittest.TestCase):
    def test_valid_plan_resolves_and_promotes(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())

            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human",
                          "--response", "승인합니다"])
            self.assertEqual(rc, 0, "유효 impl-plan 정상 해소는 0")

            # (a) events.jsonl 에 적격 actor=human gate-resolved append.
            events = _events(run)
            resolved_evs = [
                e for e in events
                if (e.get("ref") or {}).get("kind") == "gate-resolved"
                and (e.get("ref") or {}).get("gate_id") == "g-struct"
            ]
            self.assertEqual(len(resolved_evs), 1)
            self.assertEqual(resolved_evs[0]["actor"], "human")

            # is_resolved(적격성 포함) True.
            policy = GatePolicy.from_dict({})
            self.assertTrue(is_resolved(events, "g-struct", GATE_USER_DECISION_REQUIRED, policy))

            # (b) revisions.jsonl 에 3 task_added(각 basis={proposingStepRef, gateEventRef}).
            revs = _read_jsonl(run / "revisions.jsonl")
            added = [r for r in revs if r.get("kind") == "task_added"]
            self.assertEqual(len(added), 3, "impl 2 + milestone 1 = 3 task_added")
            for r in added:
                basis = r.get("basis") or {}
                self.assertEqual(basis.get("proposingStepRef"), "impl-plan-phase1")
                self.assertEqual(basis.get("gateEventRef"), "g-struct")

            # (c) accept_revision 이 gate-pass 실재를 재검증함을 확인 —
            #     승격 task 가 grounded active_graph 에 반영되었는가(orchestrator 파생 뷰).
            orch, _ = rg.build_orchestrator_k(run, rg._NoInvoke())
            graph_tasks = orch.active_graph().get("tasks") or []
            graph_ids = {t.get("id") for t in graph_tasks}
            self.assertTrue({"impl-auth", "impl-api", "milestone-integration"} <= graph_ids)

            # (d) F4→F5→gate_policy CP3 사슬 실증 — 승격된 milestone task 를 F4 게이트 정책으로
            #     evaluate 하면 approval_required(CP3) 산출(즉 CP3 가 실제 도달 가능).
            f4_policy = GatePolicy.from_dict(f4.gate_policy())
            milestone = next(t for t in graph_tasks if t.get("id") == "milestone-integration")
            self.assertEqual(milestone.get("unitType"), "milestone")
            self.assertEqual(
                f4_policy.evaluate({"unitType": milestone["unitType"]}),
                "approval_required",
                "승격된 milestone → CP3(approval_required) 도달 실증",
            )
            # implementation 단위는 review_required(CP3 아님) — 정책 사슬 대조.
            self.assertEqual(f4_policy.evaluate({"unitType": "implementation"}), "review_required")

    def test_promotion_requires_real_gate_pass_event(self):
        """accept_revision 의 gate-pass 재검증 실증 — 요구만 있고 해소 이벤트가 없으면
        (게이트 미해소) 근거 부재로 승격이 거부된다(PO-INV 5·UngroundedRevision)."""
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            # 해소 이벤트를 append 하지 않은 상태에서 직접 승격 시도 → 거부되어야 한다.
            orch, _ = rg.build_orchestrator_k(run, rg._NoInvoke())
            with self.assertRaises(Exception):
                orch.accept_revision(
                    rg.KIND_TASK_ADDED, _valid_plan()["tasks"][0],
                    proposingStepRef="impl-plan-phase1", gateEventRef="g-struct",
                )
            # 원장(revisions.jsonl)은 거부로 무오염.
            self.assertEqual((run / "revisions.jsonl").read_text(encoding="utf-8").strip(), "")


# --------------------------------------------------------------------------
# done 3 — actor 자격: user_decision 을 actor=Advisor 로 해소 시도 → 부적격
# --------------------------------------------------------------------------
class TestActorEligibility(unittest.TestCase):
    def test_user_decision_advisor_is_ineligible(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")

            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "Advisor"])
            self.assertNotEqual(rc, 0, "user_decision 을 Advisor 로 해소하면 부적격·비영 종료")

            # is_resolved False 유지.
            policy = GatePolicy.from_dict({})
            self.assertFalse(is_resolved(_events(run), "g-struct", GATE_USER_DECISION_REQUIRED, policy))

            # 승격 0·원장 무변경(부적격은 append 전에 거부).
            self.assertEqual(_sha(run / "events.jsonl"), ev_before)
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before)


# --------------------------------------------------------------------------
# done 4 — escalation 해소: escalation 게이트를 actor=Advisor 로 해소 → 적격·resolved
# --------------------------------------------------------------------------
class TestEscalationResolution(unittest.TestCase):
    def test_escalation_advisor_is_eligible(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_ESCALATION_REQUIRED, "g-esc")

            rc = rg.main([str(run), "--gate-kind", "escalation", "--actor", "Advisor",
                          "--response", "상위 개입 완료"])
            self.assertEqual(rc, 0, "escalation 을 Advisor 로 해소하면 적격·0")

            policy = GatePolicy.from_dict({})
            self.assertTrue(is_resolved(_events(run), "g-esc", GATE_ESCALATION_REQUIRED, policy))

            # escalation 은 분해 제안이 아니므로 revision 승격 없음.
            self.assertEqual((run / "revisions.jsonl").read_text(encoding="utf-8").strip(), "")

    def test_approval_escalation_maps_to_escalation(self):
        # CP3 non-Pass → escalation_required 로 정지된 게이트도 이 경로로 해소.
        self.assertEqual(rg.GATE_KIND_MAP["approval-escalation"], GATE_ESCALATION_REQUIRED)
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_ESCALATION_REQUIRED, "g-esc2")
            rc = rg.main([str(run), "--gate-kind", "approval-escalation", "--actor", "Advisor"])
            self.assertEqual(rc, 0)
            policy = GatePolicy.from_dict({})
            self.assertTrue(is_resolved(_events(run), "g-esc2", GATE_ESCALATION_REQUIRED, policy))


# --------------------------------------------------------------------------
# 어댑터 검증기 — F4 계약(milestone) 수용/거부 (unit-level + resolve_gate 경로)
# --------------------------------------------------------------------------
class TestAdapterValidator(unittest.TestCase):
    def test_milestone_plan_passes(self):
        self.assertEqual(rg.validate_impl_plan_adapter(_valid_plan()), [])

    def test_two_milestones_allowed(self):
        # milestone 2개(둘 다 종단) 허용 — 오류 0.
        self.assertEqual(rg.validate_impl_plan_adapter(_two_milestone_plan()), [])
        # 각 milestone 은 approval_required 로 평가된다(정책 사슬).
        pol = GatePolicy.from_dict(f4.gate_policy())
        self.assertEqual(pol.evaluate({"unitType": "milestone"}), "approval_required")

    def test_zero_milestone_rejected(self):
        errs = rg.validate_impl_plan_adapter(_all_impl_plan())
        self.assertTrue(any("milestone 단위가 최소 1건" in e for e in errs),
                        "milestone 0개 계획은 거부되어야 한다: %r" % errs)

    def test_dependent_on_milestone_rejected(self):
        # 어떤 task 가 milestone 을 dependsOn → DAG 종단 위반 거부.
        plan = {"tasks": [
            _task("impl-a", "src/a.py", []),
            _task("milestone-m", "src/m.py", ["impl-a"], "milestone"),
            _task("impl-c", "src/c.py", ["milestone-m"]),  # milestone 에 의존 — 위반.
        ]}
        errs = rg.validate_impl_plan_adapter(plan)
        self.assertTrue(any("milestone 은 DAG 종단" in e for e in errs), errs)

    def test_zero_milestone_via_resolve_gate_untouched(self):
        # milestone 0 계획을 resolve_gate 로 → 검증-먼저 거부·원장 무변경.
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_all_impl_plan())
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertNotEqual(rc, 0)
            self.assertEqual(_sha(run / "events.jsonl"), ev_before)
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before)


if __name__ == "__main__":
    unittest.main()
