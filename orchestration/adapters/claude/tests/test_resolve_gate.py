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


def _seed_proposal_task(tid: str = "impl-plan-phase1"):
    """물리 graph.json 에 심는 seed proposal 노드(F4 build_seed_graph 형태 모사).

    derive_proposing_step_ref 가 unitType=="proposal" 노드 id 를 파생하므로, 기본 id 를
    전신 하드코딩 값("impl-plan-phase1")과 동일하게 두어 proposingStepRef 기대값을 보존한다.
    """
    return {
        "id": tid, "task": "impl-plan 제안 step", "done": "impl-plan.json 산출",
        "interfaceContract": "impl-plan 제안 계약", "ownedBoundary": ["impl-plan.json"],
        "dependsOn": [], "delegation": dict(_SENTINEL_DELEG),
        "capability": "cap-impl-plan", "role": "Planner", "model": "sonnet",
        "unitType": "proposal",
    }


# 설계완성도 게이트(§DC-1 Wave 3) 통과용 최소 정책 — always 6종만 required(touchpoint/interface 미선언).
_DESIGN_POLICY = {
    "projectionSelection": {
        "requirementClasses": {
            "always": "항상 required",
            "touchpoint": "접점 선언 시 required",
            "interface": "연계 선언 시 required",
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
        "exclusionRule": {"silentOmission": "금지"},
    }
}

# 접점·연계 미선언 → always 6종만 required·전부 produced인 통과 매니페스트.
# 정책에 touchpoint/interface 항목이 있으나 미선언이므로 클래스 전체 제외를
# classExclusions{reason,confirmedBy}로 표면화·확인해야 게이트를 통과한다(원칙 11 (c)).
_DESIGN_MANIFEST_OK = {
    "declaredTouchpoints": [],
    "declaredInterfaces": [],
    "classExclusions": {
        "touchpoint": {"reason": "접점 없는 배치/파이프라인 프로젝트 — UI 클래스 전체 제외", "confirmedBy": "user"},
        "interface": {"reason": "외부 연계 없음 — 인터페이스 클래스 전체 제외", "confirmedBy": "user"},
    },
    "artifacts": [
        {"id": "project-plan", "status": "produced"},
        {"id": "requirements-def", "status": "produced"},
        {"id": "business-process", "status": "produced"},
        {"id": "functional-spec", "status": "produced"},
        {"id": "table-def", "status": "produced"},
        {"id": "test-plan-cases", "status": "produced"},
    ],
}


def _write_design(run: Path, *, policy=_DESIGN_POLICY, manifest=_DESIGN_MANIFEST_OK) -> None:
    """워크스페이스 SD 데이터에 정책(YAML)·매니페스트(JSON)를 시드한다. manifest=None → 매니페스트 부재."""
    import yaml  # 테스트 픽스처 전용(체커와 동일 로컬 라이브러리).

    sd = run / "workspace" / ".claude" / "solution-design"
    (sd / "policy").mkdir(parents=True, exist_ok=True)
    (sd / "policy" / "default-policy.yaml").write_text(
        yaml.safe_dump(policy, allow_unicode=True), encoding="utf-8"
    )
    if manifest is not None:
        (sd / "design-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
        )


def _build_run(base: Path, gate_kind: str, gate_id: str, *, plan=None, seed_design: bool = True,
               graph_tasks=None) -> Path:
    run = base / "run"
    (run / "logs").mkdir(parents=True)
    (run / "workspace").mkdir(parents=True)
    (run / "steps").mkdir(parents=True)
    # 설계완성도 게이트 통과 전제 시드(기본). seed_design=False → 매니페스트 부재(게이트 차단 재현).
    if seed_design:
        _write_design(run)

    (run / "config.json").write_text(
        json.dumps({"workspace_dir": str(run / "workspace"), "run_id": "test-run"}),
        encoding="utf-8",
    )
    # 물리 그래프(graph.json) — orchestrate_project 가 물리화하는 초기 그래프 모사. 기본 =
    # 단일 seed proposal 노드(derive_proposing_step_ref 파생 기준). graph_tasks 로 0건/2건 등
    # 이상 그래프를 주입해 파생 오류 경로를 재현한다(n3).
    if graph_tasks is None:
        graph_tasks = [_seed_proposal_task()]
    (run / "graph.json").write_text(
        json.dumps({"tasks": graph_tasks}), encoding="utf-8"
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


# --------------------------------------------------------------------------
# 설계완성도 게이트(§DC-1 Wave 3) — impl 승격 직전 침묵 누락 차단·원장 무오염
# --------------------------------------------------------------------------
import design_completeness as dc  # noqa: E402  (같은 어댑터 경계 모듈)


class TestDesignCompletenessGate(unittest.TestCase):
    def test_absent_manifest_blocks_and_leaves_ledger_untouched(self):
        # 설계 미완(매니페스트 부재) → 유효 impl-plan·적격 actor 라도 승격 전 차단·원장 무변경.
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_valid_plan(), seed_design=False)
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertNotEqual(rc, 0, "매니페스트 부재는 승격 전 비영 종료로 차단")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before, "revisions.jsonl 무변경")
            policy = GatePolicy.from_dict({})
            self.assertFalse(is_resolved(_events(run), "g-struct", GATE_USER_DECISION_REQUIRED, policy))

    def test_silent_omission_blocks(self):
        # always 필수 중 하나 누락(산출도 정당화 제외도 없음) → 차단·원장 무변경.
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            partial = {"declaredTouchpoints": [], "declaredInterfaces": [],
                       "artifacts": [{"id": "project-plan", "status": "produced"}]}  # 5종 누락.
            _write_design(run, manifest=partial)
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertNotEqual(rc, 0)
            self.assertEqual(_sha(run / "events.jsonl"), ev_before)
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before)

    def test_all_produced_passes_through_to_promotion(self):
        # 기본 시드(_DESIGN_MANIFEST_OK·전부 produced) → 게이트 통과·정상 승격(rc 0).
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertEqual(rc, 0, "전부 produced 는 게이트 통과·승격")

    def test_justified_exclusion_passes(self):
        # 접점 선언(screen-list 등 required) 후 정당화 제외(reason+confirmedBy) → 통과.
        # 연계는 미선언이므로 interface 클래스 전체 제외를 classExclusions.interface 로 확인해야 통과.
        errors = dc.check_design_completeness(*self._pair(
            manifest={
                "declaredTouchpoints": ["web-portal"],
                "declaredInterfaces": [],
                "classExclusions": {
                    "interface": {"reason": "외부 연계 없음", "confirmedBy": "user"},
                },
                "artifacts": [
                    {"id": "project-plan", "status": "produced"},
                    {"id": "requirements-def", "status": "produced"},
                    {"id": "business-process", "status": "produced"},
                    {"id": "functional-spec", "status": "produced"},
                    {"id": "table-def", "status": "produced"},
                    {"id": "test-plan-cases", "status": "produced"},
                    {"id": "screen-list", "status": "produced"},
                    {"id": "menu-structure", "status": "produced"},
                    {"id": "screen-design", "status": "excluded",
                     "reason": "MVP 범위 밖 — 후속 반영", "confirmedBy": "user"},
                ],
            }))
        self.assertEqual(errors, [], "정당화 제외(reason+confirmedBy)는 통과: %r" % errors)

    def test_exclusion_missing_confirmedby_blocks(self):
        errors = dc.check_design_completeness(*self._pair(
            manifest={
                "declaredTouchpoints": ["web-portal"],
                "declaredInterfaces": [],
                "artifacts": [
                    {"id": "project-plan", "status": "produced"},
                    {"id": "requirements-def", "status": "produced"},
                    {"id": "business-process", "status": "produced"},
                    {"id": "functional-spec", "status": "produced"},
                    {"id": "table-def", "status": "produced"},
                    {"id": "test-plan-cases", "status": "produced"},
                    {"id": "screen-list", "status": "excluded", "reason": "범위 밖"},  # confirmedBy 누락.
                    {"id": "menu-structure", "status": "produced"},
                    {"id": "screen-design", "status": "produced"},
                ],
            }))
        self.assertTrue(any("정당화 제외 요건 미충족" in e for e in errors), errors)

    # --- 클래스 전체 제외 표면화(원칙 11 (c)) — 케이스 A(미확인 차단)·B(확인 통과) ---
    _ALWAYS_6 = [
        {"id": "project-plan", "status": "produced"},
        {"id": "requirements-def", "status": "produced"},
        {"id": "business-process", "status": "produced"},
        {"id": "functional-spec", "status": "produced"},
        {"id": "table-def", "status": "produced"},
        {"id": "test-plan-cases", "status": "produced"},
    ]

    def test_touchpoint_class_dropped_without_confirmation_blocks(self):
        # 케이스 A(touchpoint): 정책에 touchpoint 항목 존재 + 접점 미선언 + classExclusions 없음 → 차단.
        errors = dc.check_design_completeness(*self._pair(
            manifest={
                "declaredTouchpoints": [],
                "declaredInterfaces": ["payment-gateway"],  # interface 는 선언(트리거)해 격리.
                "artifacts": list(self._ALWAYS_6) + [
                    {"id": "interface-spec", "status": "produced"},
                ],
            }))
        self.assertTrue(
            any("touchpoint 클래스 전체 제외" in e and "classExclusions" in e for e in errors),
            "접점 미선언+classExclusions 부재는 차단되어야 한다: %r" % errors,
        )

    def test_interface_class_dropped_without_confirmation_blocks(self):
        # 케이스 A(interface 동형): interface 항목 존재 + 연계 미선언 + classExclusions 없음 → 차단.
        errors = dc.check_design_completeness(*self._pair(
            manifest={
                "declaredTouchpoints": ["web-portal"],  # touchpoint 는 선언해 격리.
                "declaredInterfaces": [],
                "artifacts": list(self._ALWAYS_6) + [
                    {"id": "screen-list", "status": "produced"},
                    {"id": "menu-structure", "status": "produced"},
                    {"id": "screen-design", "status": "produced"},
                ],
            }))
        self.assertTrue(
            any("interface 클래스 전체 제외" in e and "classExclusions" in e for e in errors),
            "연계 미선언+classExclusions 부재는 차단되어야 한다: %r" % errors,
        )

    def test_class_exclusion_missing_confirmedby_blocks(self):
        # 케이스 A 변형: classExclusions.touchpoint 있으나 confirmedBy 누락 → 요건 미충족 차단.
        errors = dc.check_design_completeness(*self._pair(
            manifest={
                "declaredTouchpoints": [],
                "declaredInterfaces": [],
                "classExclusions": {
                    "touchpoint": {"reason": "UI 없음"},  # confirmedBy 누락.
                    "interface": {"reason": "연계 없음", "confirmedBy": "user"},
                },
                "artifacts": list(self._ALWAYS_6),
            }))
        self.assertTrue(
            any("touchpoint 클래스 전체 제외" in e and "confirmedBy" in e for e in errors),
            "classExclusions 요건 미충족(confirmedBy 누락)은 차단되어야 한다: %r" % errors,
        )

    def test_class_exclusion_confirmed_passes(self):
        # 케이스 B: 접점·연계 미선언 + classExclusions{reason,confirmedBy} 확인 + always 6종 produced → 통과.
        errors = dc.check_design_completeness(*self._pair(
            manifest={
                "declaredTouchpoints": [],
                "declaredInterfaces": [],
                "classExclusions": {
                    "touchpoint": {"reason": "접점 없는 배치 프로젝트", "confirmedBy": "user"},
                    "interface": {"reason": "외부 연계 없음", "confirmedBy": "user"},
                },
                "artifacts": list(self._ALWAYS_6),
            }))
        self.assertEqual(errors, [], "클래스 제외 확인(reason+confirmedBy)은 통과: %r" % errors)

    def _pair(self, *, manifest):
        """임시 정책·매니페스트 파일 쌍을 만들어 (policy_path, manifest_path) 반환(체커 직접 호출용)."""
        import yaml
        td = tempfile.mkdtemp()
        sd = Path(td)
        (sd / "default-policy.yaml").write_text(
            yaml.safe_dump(_DESIGN_POLICY, allow_unicode=True), encoding="utf-8")
        (sd / "design-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        self.addCleanup(lambda: __import__("shutil").rmtree(td, ignore_errors=True))
        return str(sd / "default-policy.yaml"), str(sd / "design-manifest.json")


# --------------------------------------------------------------------------
# n3 — proposingStepRef 파생: proposal 노드 0건/2건 → 오류 + 원장 무변경
# --------------------------------------------------------------------------
class TestProposingStepRefDerivation(unittest.TestCase):
    def test_derive_single_proposal(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g", plan=None)
            self.assertEqual(rg.derive_proposing_step_ref(run), "impl-plan-phase1")

    def test_zero_proposal_node_blocks_and_ledger_untouched(self):
        # 물리 그래프에 proposal 노드 0건(implementation 만) → 파생 불가·비영 종료·원장 무변경.
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(
                Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan(),
                graph_tasks=[_task("impl-only", "src/x.py", [])],  # unitType=implementation.
            )
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertNotEqual(rc, 0, "proposal 0건 그래프는 파생 실패로 비영 종료")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before, "revisions.jsonl 무변경")

    def test_two_proposal_nodes_blocks_and_ledger_untouched(self):
        # proposal 노드 2건 → 파생 모호·비영 종료·원장 무변경(추측 0).
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(
                Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan(),
                graph_tasks=[_seed_proposal_task("p1"), _seed_proposal_task("p2")],
            )
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertNotEqual(rc, 0, "proposal 2건 그래프는 파생 모호로 비영 종료")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before)
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before)


# --------------------------------------------------------------------------
# n4 — F4→F5 통합 관통: compile → 물리화(graph.json) → resolve_gate 승격.
#      proposingStepRef 가 파생 seed id 와 일치함을 실증(격리 검증만으로 끝내지 않음).
# --------------------------------------------------------------------------
class TestF4F5Integration(unittest.TestCase):
    def test_compile_to_resolve_gate_proposing_ref_matches_derived(self):
        fixture = _TEST_FILE.parent / "fixtures" / "consumer-ws"
        # phase2 로 컴파일 → seed id = "impl-plan-phase2"(기본값 아님·진짜 파생 실증).
        compiled = f4.compile(fixture, mode="incremental", phase_scope="phase2")
        seed_id = compiled["graph"]["tasks"][0]["id"]
        self.assertEqual(seed_id, "impl-plan-phase2", "compile seed id 는 phase_scope 파생")

        with tempfile.TemporaryDirectory() as td:
            # compile 이 만든 실제 그래프를 graph.json 으로 물리화(관통 경로).
            run = _build_run(
                Path(td), GATE_USER_DECISION_REQUIRED, "g-int", plan=_valid_plan(),
                graph_tasks=compiled["graph"]["tasks"],
            )
            # resolve_gate 는 graph.json 에서 proposingStepRef 를 파생한다(하드코딩 아님).
            self.assertEqual(rg.derive_proposing_step_ref(run), seed_id)

            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertEqual(rc, 0, "관통 해소는 0")

            revs = _read_jsonl(run / "revisions.jsonl")
            added = [r for r in revs if r.get("kind") == "task_added"]
            self.assertEqual(len(added), 3)
            for r in added:
                self.assertEqual(
                    (r.get("basis") or {}).get("proposingStepRef"), seed_id,
                    "승격 basis.proposingStepRef 가 compile 파생 seed id 와 일치해야 한다",
                )


if __name__ == "__main__":
    unittest.main()
