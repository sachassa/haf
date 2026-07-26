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

    def _resolution_ref(self, run, gate_id):
        rows = [
            e for e in _events(run)
            if (e.get("ref") or {}).get("kind") == "gate-resolved"
            and (e.get("ref") or {}).get("gate_id") == gate_id
        ]
        self.assertEqual(len(rows), 1, "해소 이벤트 1건")
        return rows[0]["ref"]

    def test_response_is_embedded_in_resolution_ref(self):
        # D3 — --response 원문이 해소 이벤트 ref 에 동봉된다(엔진이 재작업 지시로 전파).
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_ESCALATION_REQUIRED, "g-esc-resp")
            rc = rg.main([str(run), "--gate-kind", "escalation", "--actor", "Advisor",
                          "--response", "타임아웃 상향 후 재시도하라"])
            self.assertEqual(rc, 0)
            ref = self._resolution_ref(run, "g-esc-resp")
            self.assertEqual(ref["response"], "타임아웃 상향 후 재시도하라")

    def test_absent_response_keeps_resolution_ref_shape(self):
        # 가법 보장 — --response 미지정이면 ref 는 종전 3키 그대로(기존 해소 이벤트 형태 보존).
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_ESCALATION_REQUIRED, "g-esc-noresp")
            rc = rg.main([str(run), "--gate-kind", "escalation", "--actor", "Advisor"])
            self.assertEqual(rc, 0)
            ref = self._resolution_ref(run, "g-esc-noresp")
            self.assertEqual(sorted(ref.keys()), ["gateKind", "gate_id", "kind"])

    def test_resume_hint_printed_after_resolution(self):
        # 해소 이벤트만으로는 아무 것도 실행되지 않는다 — 재개 명령이 표면화되어야 한다.
        import io
        from contextlib import redirect_stdout

        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_ESCALATION_REQUIRED, "g-esc-hint")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = rg.main([str(run), "--gate-kind", "escalation", "--actor", "Advisor"])
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("[NEXT]", out)
            self.assertIn("--resume", out)
            self.assertIn("orchestrate_project.py", out)

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
# designElements 게이트(Visual Contract 트랙) — 디자인 필수 요소 선언 완전성
# --------------------------------------------------------------------------
# 정책에 designElements 섹션이 있고 접점이 선언될 때만 활성. defaultRequiredSet 에 touchpoint
# 항목을 두지 않아(always 6종만) 산출물 요구와 designElements 요구를 격리·집중 검증한다.
_DE_PROJECT = [
    {"id": "design-tokens-values", "name": "디자인 토큰 실값"},
    {"id": "tone-and-manner", "name": "톤앤매너 확정"},
    {"id": "accessibility-floor", "name": "접근성 최소선"},
]
_DE_SCREEN = [
    {"id": "layout-structure", "name": "레이아웃 구조"},
    {"id": "navigation", "name": "네비게이션"},
    {"id": "component-states", "name": "컴포넌트 상태 5종"},
    {"id": "data-rules", "name": "데이터 표시 규칙"},
    {"id": "responsive", "name": "반응형 기준"},
]
_DESIGN_POLICY_VC = {
    "projectionSelection": {
        "requirementClasses": {
            "always": "항상 required", "touchpoint": "접점 선언 시", "interface": "연계 선언 시",
        },
        "defaultRequiredSet": [
            {"id": "project-plan", "name": "프로젝트 계획서", "requirement": "always"},
            {"id": "requirements-def", "name": "요구사항 정의서", "requirement": "always"},
            {"id": "business-process", "name": "업무 프로세스", "requirement": "always"},
            {"id": "functional-spec", "name": "기능 명세서", "requirement": "always"},
            {"id": "table-def", "name": "테이블 정의서", "requirement": "always"},
            {"id": "test-plan-cases", "name": "테스트 계획·케이스", "requirement": "always"},
        ],
        "exclusionRule": {"silentOmission": "금지"},
    },
    "designElements": {
        "appliesWhen": "touchpoint",
        "projectScope": [dict(e) for e in _DE_PROJECT],
        "screenScope": [dict(e) for e in _DE_SCREEN],
        "exclusionRule": {"silentOmission": "금지"},
    },
}
_VC_ALWAYS_6 = [
    {"id": "project-plan", "status": "produced"},
    {"id": "requirements-def", "status": "produced"},
    {"id": "business-process", "status": "produced"},
    {"id": "functional-spec", "status": "produced"},
    {"id": "table-def", "status": "produced"},
    {"id": "test-plan-cases", "status": "produced"},
]


def _covered(ids):
    return {i: {"status": "covered", "pointer": "docs/x.md#%s" % i} for i in ids}


class TestDesignElementsGate(unittest.TestCase):
    _PROJECT_IDS = [e["id"] for e in _DE_PROJECT]
    _SCREEN_IDS = [e["id"] for e in _DE_SCREEN]

    def _pair(self, *, manifest, policy=_DESIGN_POLICY_VC):
        import yaml
        td = Path(tempfile.mkdtemp())
        (td / "default-policy.yaml").write_text(
            yaml.safe_dump(policy, allow_unicode=True), encoding="utf-8")
        (td / "design-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        self.addCleanup(lambda: __import__("shutil").rmtree(str(td), ignore_errors=True))
        return str(td / "default-policy.yaml"), str(td / "design-manifest.json")

    def _full_manifest(self):
        return {
            "declaredTouchpoints": ["web-portal"], "declaredInterfaces": [],
            "artifacts": list(_VC_ALWAYS_6),
            "designElements": {
                "project": _covered(self._PROJECT_IDS),
                "screens": {"home": _covered(self._SCREEN_IDS)},
            },
        }

    # t1 — 하위호환: 구 정책(designElements 무) + 접점 선언 매니페스트 → designElements 검사 비적용.
    def test_t1_old_policy_no_designelements_unaffected(self):
        # _DESIGN_POLICY(구 정책·designElements 없음)로 접점 선언 시에도 designElements 오류 0.
        errors = dc.check_design_completeness(*TestDesignCompletenessGate._pair(
            self, manifest={
                "declaredTouchpoints": ["web-portal"], "declaredInterfaces": [],
                "classExclusions": {"interface": {"reason": "연계 없음", "confirmedBy": "user"}},
                "artifacts": list(_ALWAYS_6_HELPER),
            }))
        self.assertFalse(any("designElements" in e or "요소" in e for e in errors),
                         "구 정책은 designElements 검사가 비적용이어야 한다: %r" % errors)

    # t2 — 신 정책 + 접점 선언 + 완전 선언 → 오류 0(exit 0).
    def test_t2_full_declaration_passes(self):
        self.assertEqual(dc.check_design_completeness(*self._pair(manifest=self._full_manifest())), [])

    # t3 — screens 공집합 → 오류.
    def test_t3_empty_screens_blocks(self):
        m = self._full_manifest()
        m["designElements"]["screens"] = {}
        errors = dc.check_design_completeness(*self._pair(manifest=m))
        self.assertTrue(any("screens 가 비어" in e for e in errors), errors)

    # t4 — 화면 1개에서 요소 1개 미선언 → 오류 문면에 화면id·요소id.
    def test_t4_missing_screen_element_names_screen_and_element(self):
        m = self._full_manifest()
        del m["designElements"]["screens"]["home"]["navigation"]
        errors = dc.check_design_completeness(*self._pair(manifest=m))
        self.assertTrue(any("home" in e and "navigation" in e for e in errors),
                        "오류 문면에 화면id·요소id 포함되어야 한다: %r" % errors)

    # t5 — excluded 인데 reason/confirmedBy 결손 → 오류.
    def test_t5_excluded_missing_confirmedby_blocks(self):
        m = self._full_manifest()
        m["designElements"]["project"]["tone-and-manner"] = {"status": "excluded", "reason": "MVP 밖"}
        errors = dc.check_design_completeness(*self._pair(manifest=m))
        self.assertTrue(any("tone-and-manner" in e and "confirmedBy" in e for e in errors), errors)

    # t5b — 정당화 excluded(reason+confirmedBy) → 통과.
    def test_t5b_justified_exclusion_passes(self):
        m = self._full_manifest()
        m["designElements"]["project"]["accessibility-floor"] = {
            "status": "excluded", "reason": "내부 관리자 도구 — 접근성 최소선 후속 이연", "confirmedBy": "user"}
        self.assertEqual(dc.check_design_completeness(*self._pair(manifest=m)), [])

    # t6 — 접점 미선언 + 신 정책 → designElements 비적용(활성 안 됨).
    def test_t6_no_touchpoint_designelements_inactive(self):
        m = {
            "declaredTouchpoints": [], "declaredInterfaces": [],
            "artifacts": list(_VC_ALWAYS_6),
            # designElements 매니페스트 없음 — 접점 미선언이므로 검사 비적용이어야 한다.
        }
        errors = dc.check_design_completeness(*self._pair(manifest=m))
        self.assertEqual(errors, [], "접점 미선언 시 designElements 는 비적용: %r" % errors)

    # t7 — projectScope 요소 미선언 → 오류.
    def test_t7_missing_project_element_blocks(self):
        m = self._full_manifest()
        del m["designElements"]["project"]["accessibility-floor"]
        errors = dc.check_design_completeness(*self._pair(manifest=m))
        self.assertTrue(any("accessibility-floor" in e for e in errors), errors)

    # t8 — 결정성: 같은 입력 2회 → 동일 출력.
    def test_t8_determinism(self):
        m = self._full_manifest()
        del m["designElements"]["screens"]["home"]["responsive"]
        pair = self._pair(manifest=m)
        self.assertEqual(dc.check_design_completeness(*pair), dc.check_design_completeness(*pair))


# always 6종 헬퍼(구 정책 t1 재사용 — _DESIGN_POLICY 는 touchpoint 3종·interface 1종 포함).
_ALWAYS_6_HELPER = [
    {"id": "project-plan", "status": "produced"},
    {"id": "requirements-def", "status": "produced"},
    {"id": "business-process", "status": "produced"},
    {"id": "functional-spec", "status": "produced"},
    {"id": "table-def", "status": "produced"},
    {"id": "test-plan-cases", "status": "produced"},
    {"id": "screen-list", "status": "produced"},
    {"id": "menu-structure", "status": "produced"},
    {"id": "screen-design", "status": "produced"},
]


# --------------------------------------------------------------------------
# scaffold 벤더링 미러 — design_completeness.py 로직 본문 바이트 동일(§DC-3 W3 관례)
# --------------------------------------------------------------------------
class TestScaffoldMirror(unittest.TestCase):
    def test_mirror_logic_body_byte_identical(self):
        repo = _TEST_FILE.parents[4]
        src = (repo / "orchestration" / "adapters" / "claude" / "design_completeness.py")
        mirror = (repo / "uahf" / "framework" / "adapters" / "claude" / "scaffold-template"
                  / "dot-claude" / "hooks" / "design-guard" / "design_completeness.py")
        src_lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
        mir_lines = mirror.read_text(encoding="utf-8").splitlines(keepends=True)
        # 미러 = shebang(1) + 벤더링 헤더 주석(8) + 원본 본문. 헤더 8줄 제거 후 원본과 바이트 동일.
        self.assertEqual(mir_lines[0], src_lines[0], "shebang 동일")
        self.assertTrue(all(l.startswith("#") for l in mir_lines[1:9]), "헤더 8줄 주석")
        self.assertEqual(mir_lines[:1] + mir_lines[9:], src_lines,
                         "미러 로직 본문은 원본과 바이트 동일해야 한다(헤더 8줄만 차이)")


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


# --------------------------------------------------------------------------
# 백로그 K — Contract 포인터 정합: 산출물이 지목한 정본 인스턴스 vs 현재 인스턴스
# --------------------------------------------------------------------------
# 정책을 always 1종(project-plan)만으로 최소화해 포인터 오류를 다른 완전성 오류와 격리한다.
_K_POLICY = {
    "projectionSelection": {
        "requirementClasses": {"always": "항상 required"},
        "defaultRequiredSet": [
            {"id": "project-plan", "name": "프로젝트 계획서", "requirement": "always"},
        ],
        "exclusionRule": {"silentOmission": "금지"},
    }
}

# 실물 yt-stt Projection 헤더 문면 2종(바이트 복사 — 접합부 왕복 픽스처).
_K_REAL_HEADER_A = (
    "> Solution Design 산출물 · id `project-plan` · 소유 역할 = PM(전체 커버리지 / coverageFloor).\n"
    "> 정본 계약 = `.claude/project-contract/project-contract.v4.md`(pc-yt-stt-004 · 인스턴스 v4).\n"
)
_K_REAL_HEADER_B = (
    "> Solution Design 산출물. 소유 = Architecture 역할.\n"
    "> 정본 = Project Contract v4 (`.claude/project-contract/project-contract.v4.md`). "
    "본 문서는 Contract Architecture Direction을 **설계 방향 수준**으로 구체화하며 재정의하지 않는다.\n"
)


class TestContractPointerIntegrity(unittest.TestCase):
    """백로그 K — design_completeness 의 Contract 포인터 정합 검사."""

    def _tree(self, *, versions, docs, artifacts):
        """관례 배치 임시 트리를 만들고 (policy_path, manifest_path) 반환.

        <td>/.claude/project-contract/project-contract.v<N>.md   (versions)
        <td>/.claude/solution-design/{default-policy.yaml,design-manifest.json}
        <td>/docs/<name>                                          (docs: {상대명: 본문})
        contract_dir 인자를 넘기지 않으므로 **파생 경로**(<manifest 부모의 부모>/project-contract)를
        실제로 타는 구성이다(k12 = 이 헬퍼를 쓰는 전 케이스가 파생 경로를 커버).
        """
        import yaml
        td = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(td, ignore_errors=True))

        if versions:
            cdir = td / ".claude" / "project-contract"
            cdir.mkdir(parents=True)
            for n in versions:
                (cdir / ("project-contract.v%d.md" % n)).write_text(
                    "# Project Contract 인스턴스 v%d\n" % n, encoding="utf-8")

        for rel, body in docs.items():
            p = td / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")

        sd = td / ".claude" / "solution-design"
        sd.mkdir(parents=True, exist_ok=True)
        (sd / "default-policy.yaml").write_text(
            yaml.safe_dump(_K_POLICY, allow_unicode=True), encoding="utf-8")
        (sd / "design-manifest.json").write_text(
            json.dumps({"declaredTouchpoints": [], "declaredInterfaces": [],
                        "artifacts": artifacts}, ensure_ascii=False),
            encoding="utf-8")
        return str(sd / "default-policy.yaml"), str(sd / "design-manifest.json")

    @staticmethod
    def _plan_art(**extra):
        a = {"id": "project-plan", "status": "produced", "path": "../../docs/plan.md"}
        a.update(extra)
        return a

    def test_k1_stale_pointer_blocks(self):
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v1.md`\n"},
            artifacts=[self._plan_art()])
        errors = dc.check_design_completeness(*pair)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("stale", errors[0])
        self.assertIn("project-plan", errors[0])
        self.assertIn("v1", errors[0])
        self.assertIn("v2", errors[0])

    def test_k2_max_reference_wins_over_history_line(self):
        # 헤더가 현재 v2 를 지목하고 이력 줄에 v1 을 병기 → 최고 참조 == 현재 → 통과.
        body = ("정본 = `.claude/project-contract/project-contract.v2.md`\n"
                "이력: v1(`project-contract.v1.md`) 을 supersede.\n")
        pair = self._tree(versions=[1, 2], docs={"docs/plan.md": body},
                          artifacts=[self._plan_art()])
        self.assertEqual(dc.check_design_completeness(*pair), [])

    def test_k3_absent_contract_lineage_is_inapplicable(self):
        pair = self._tree(
            versions=[],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v1.md`\n"},
            artifacts=[self._plan_art()])
        self.assertEqual(dc.check_design_completeness(*pair), [])

    def test_k4_zero_reference_is_skipped(self):
        pair = self._tree(versions=[1, 2],
                          docs={"docs/plan.md": "# 계획서\nContract 를 언급하지 않는 본문.\n"},
                          artifacts=[self._plan_art()])
        self.assertEqual(dc.check_design_completeness(*pair), [])

    def test_k5_dangling_pointer_blocks(self):
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v3.md`\n"},
            artifacts=[self._plan_art()])
        errors = dc.check_design_completeness(*pair)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("dangling", errors[0])
        self.assertIn("v3", errors[0])

    def test_k6_valid_pin_skips_check(self):
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v1.md`\n"},
            artifacts=[self._plan_art(contractRefPinned={
                "reason": "v2 는 구현 범위 밖 확장 — 본 산출물은 v1 근거를 유지",
                "confirmedBy": "user"})])
        self.assertEqual(dc.check_design_completeness(*pair), [])

    def test_k7_invalid_pin_reports_and_still_checks(self):
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v1.md`\n"},
            artifacts=[self._plan_art(contractRefPinned={"reason": "사유만 있음"})])
        errors = dc.check_design_completeness(*pair)
        self.assertEqual(len(errors), 2, errors)
        self.assertIn("contractRefPinned 요건 미충족", errors[0])
        self.assertIn("confirmedBy", errors[0])
        self.assertIn("stale", errors[1], "무효 핀은 핀이 아니다 — 포인터 검사가 그대로 수행된다")

    def test_k8_deterministic(self):
        pair = self._tree(
            versions=[1, 2, 3],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v1.md`\n"},
            artifacts=[self._plan_art()])
        self.assertEqual(dc.check_design_completeness(*pair),
                         dc.check_design_completeness(*pair))

    def test_k9_non_md_artifact_is_skipped(self):
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v2.md`\n",
                  "mocks/index.html": "<!-- project-contract.v1.md -->\n"},
            artifacts=[self._plan_art(),
                       {"id": "screen-mock", "status": "produced",
                        "path": "../../mocks/index.html"}])
        self.assertEqual(dc.check_design_completeness(*pair), [])

    def test_k10_real_header_roundtrip(self):
        # 실물 헤더 문면 2종(v4 표기) — 계보 v1..v4 면 통과.
        docs = {"docs/plan.md": _K_REAL_HEADER_A, "docs/arch.md": _K_REAL_HEADER_B}
        arts = [self._plan_art(),
                {"id": "arch-direction", "status": "produced", "path": "../../docs/arch.md"}]
        pair = self._tree(versions=[1, 2, 3, 4], docs=docs, artifacts=arts)
        self.assertEqual(dc.check_design_completeness(*pair), [])

        # 계보에 v5 추가 → 두 산출물 모두 stale.
        pair2 = self._tree(versions=[1, 2, 3, 4, 5], docs=docs, artifacts=arts)
        errors = dc.check_design_completeness(*pair2)
        self.assertEqual(len(errors), 2, errors)
        self.assertTrue(all("stale" in e for e in errors), errors)
        self.assertIn("project-plan", errors[0])
        self.assertIn("arch-direction", errors[1])
        self.assertTrue(all("v4" in e and "v5" in e for e in errors), errors)

    def test_k11_gate_level_blocks_and_ledger_untouched(self):
        # 게이트 레벨 접합부: 워크스페이스에 계보 v1·v2 + 산출물이 v1 참조 → 비영 종료·원장 무변경.
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            ws = run / "workspace"
            cdir = ws / ".claude" / "project-contract"
            cdir.mkdir(parents=True)
            for n in (1, 2):
                (cdir / ("project-contract.v%d.md" % n)).write_text(
                    "# 인스턴스 v%d\n" % n, encoding="utf-8")
            (ws / "docs").mkdir(parents=True, exist_ok=True)
            (ws / "docs" / "plan.md").write_text(
                "정본 = `.claude/project-contract/project-contract.v1.md`\n", encoding="utf-8")

            manifest = json.loads(json.dumps(_DESIGN_MANIFEST_OK))  # 깊은 복사(원본 불변).
            manifest["artifacts"][0]["path"] = "../../docs/plan.md"  # project-plan.
            _write_design(run, manifest=manifest)

            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertNotEqual(rc, 0, "stale 포인터는 승격 전 비영 종료로 차단")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before, "revisions.jsonl 무변경")

    def test_k11b_gate_level_current_pointer_passes(self):
        # 음성 대조의 짝 — 동일 배선에서 포인터가 현재 인스턴스면 통과·정상 승격(rc 0).
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            ws = run / "workspace"
            cdir = ws / ".claude" / "project-contract"
            cdir.mkdir(parents=True)
            for n in (1, 2):
                (cdir / ("project-contract.v%d.md" % n)).write_text(
                    "# 인스턴스 v%d\n" % n, encoding="utf-8")
            (ws / "docs").mkdir(parents=True, exist_ok=True)
            (ws / "docs" / "plan.md").write_text(
                "정본 = `.claude/project-contract/project-contract.v2.md`\n", encoding="utf-8")

            manifest = json.loads(json.dumps(_DESIGN_MANIFEST_OK))
            manifest["artifacts"][0]["path"] = "../../docs/plan.md"
            _write_design(run, manifest=manifest)

            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertEqual(rc, 0, "현재 인스턴스 포인터는 게이트 통과·승격")

    def test_k12_explicit_contract_dir_argument(self):
        # 3번째 인자 명시 경로(파생과 다른 위치)도 동작한다 — 파생 커버는 k1~k10(관례 배치).
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v1.md`\n"},
            artifacts=[self._plan_art()])
        explicit = Path(pair[1]).resolve().parent.parent / "project-contract"
        errors = dc.check_design_completeness(pair[0], pair[1], str(explicit))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("stale", errors[0])
        # 존재하지 않는 명시 경로 → 비적용(계보 부재 경로와 동형).
        self.assertEqual(
            dc.check_design_completeness(pair[0], pair[1], str(explicit) + "-nonexistent"), [])

    # --- 판독 실패 = 판정 불가 = 차단(이진 상태 원칙) — 비적용과 구분 ---
    def test_k13_lineage_read_failure_blocks(self):
        # 계보 디렉터리는 실재하는데 iterdir 이 OSError → 비적용이 아니라 차단.
        from unittest import mock
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v2.md`\n"},
            artifacts=[self._plan_art()])
        self.assertEqual(dc.check_design_completeness(*pair), [], "패치 전 기저는 통과")

        real_iterdir = Path.iterdir

        def fake_iterdir(self):
            # 대상 계보 디렉터리에서만 raise — 정책·매니페스트 판독 경로는 오염시키지 않는다.
            if self.name == "project-contract":
                raise OSError(13, "permission denied(테스트 주입)")
            return real_iterdir(self)

        with mock.patch.object(Path, "iterdir", fake_iterdir):
            errors = dc.check_design_completeness(*pair)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("Contract 계보 판독 실패", errors[0])
        self.assertIn("판정 불가", errors[0])

    def test_k14_artifact_read_failure_blocks(self):
        # 산출물 본문 판독 실패 → 스킵이 아니라 차단.
        from unittest import mock
        pair = self._tree(
            versions=[1, 2],
            docs={"docs/plan.md": "정본 = `.claude/project-contract/project-contract.v2.md`\n"},
            artifacts=[self._plan_art()])
        self.assertEqual(dc.check_design_completeness(*pair), [], "패치 전 기저는 통과")

        real_read_text = Path.read_text

        def fake_read_text(self, *a, **kw):
            # 대상 산출물에서만 raise — 정책 YAML·매니페스트 JSON 판독은 그대로 둔다.
            if self.name == "plan.md":
                raise OSError(5, "I/O error(테스트 주입)")
            return real_read_text(self, *a, **kw)

        with mock.patch.object(Path, "read_text", fake_read_text):
            errors = dc.check_design_completeness(*pair)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("산출물 판독 실패", errors[0])
        self.assertIn("project-plan", errors[0])


# ==========================================================================
# 다중 pending 동일 gateKind 특정 지목 (--gate-id) — 침묵 첫-선택 제거
# --------------------------------------------------------------------------
# 결함: recover_gate 가 matches[0] 를 조용히 골라 사용자가 의도하지 않은 게이트를 해소했다.
# 사양: --gate-id 지목 + 무지목 다중 매칭 시 명시 오류(후보 열거)·원장 무변경.
# 기존 단일 게이트 경로(무지목 1건 매칭)는 위 기존 케이스들이 무수정 통과로 증명한다.
# ==========================================================================
def _add_pending_gate(run: Path, gate_kind: str, gate_id: str, unit_id: str) -> None:
    """기존 run 에 정지 게이트 요구를 1건 더 append 하고 stop-signal 을 재파생한다(가법 헬퍼).

    stop-signal 의 pending_gates 는 런처(`orchestrate_project.run_and_map`)와 동일하게
    `gates.pending_gates(events, policy)` 파생 결과를 그대로 싣는다 — 픽스처가 손으로
    만든 형태가 아니라 실물 계약(binding §3.4 4필드)과 같은 산출 경로다.
    """
    log = EventLog(JsonlEventStore(str(run / "events.jsonl")))
    append_gate_requirement(
        log, gate_id, gate_kind,
        target={"unitId": unit_id},
        scoped_question={"unitId": unit_id, "gateKind": gate_kind,
                         "cause": "execution_escalated"},
    )
    pend = pending_gates(log.all_events(), GatePolicy.from_dict({}))
    sig = run / "logs" / "stop-signal.json"
    stop = json.loads(sig.read_text(encoding="utf-8"))
    stop["pending_gates"] = pend
    sig.write_text(json.dumps(stop, ensure_ascii=False), encoding="utf-8")


def _stop_pending(run: Path):
    return json.loads(
        (run / "logs" / "stop-signal.json").read_text(encoding="utf-8")
    )["pending_gates"]


class TestMultiPendingGateSelection(unittest.TestCase):
    def _two_escalation_run(self, td) -> Path:
        run = _build_run(Path(td), GATE_ESCALATION_REQUIRED, "gate-unit-a::exec-escalation")
        _add_pending_gate(run, GATE_ESCALATION_REQUIRED,
                          "gate-unit-b::exec-escalation", "unit-b")
        self.assertEqual(len(_stop_pending(run)), 2, "픽스처 전제: 동일 kind 2건 pending")
        return run

    def _run_cli(self, argv):
        import io
        from contextlib import redirect_stderr, redirect_stdout

        err, out = io.StringIO(), io.StringIO()
        with redirect_stderr(err), redirect_stdout(out):
            rc = rg.main(argv)
        return rc, out.getvalue(), err.getvalue()

    # g1 — 동일 kind 2건 pending + 무지목 → 비영 종료 · 원장 무변경 · 후보 열거.
    def test_g1_multiple_pending_without_gate_id_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            run = self._two_escalation_run(td)
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")

            rc, _out, err = self._run_cli(
                [str(run), "--gate-kind", "escalation", "--actor", "Advisor"])

            self.assertNotEqual(rc, 0, "다중 매칭 무지목은 비영 종료여야 한다(침묵 첫-선택 금지)")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 바이트 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before, "revisions.jsonl 무변경")
            # 후보 열거 + 지목 안내가 stderr 에 있다.
            self.assertIn("gate-unit-a::exec-escalation", err)
            self.assertIn("gate-unit-b::exec-escalation", err)
            self.assertIn("--gate-id", err)
            self.assertIn("since=", err)

    # g2 — --gate-id 로 두 번째 게이트 지목 → 그 게이트만 해소(첫 게이트 pending 유지).
    def test_g2_gate_id_resolves_only_the_named_gate(self):
        with tempfile.TemporaryDirectory() as td:
            run = self._two_escalation_run(td)
            pend = _stop_pending(run)
            target = pend[1]["gate_id"]
            other = pend[0]["gate_id"]

            rc, out, err = self._run_cli(
                [str(run), "--gate-kind", "escalation", "--actor", "Advisor",
                 "--gate-id", target, "--response", "b 단위만 재작업하라"])
            self.assertEqual(rc, 0, err)
            self.assertIn(target, out)

            # 해소 이벤트의 gate_id 로 확증 — 지목한 게이트에만 append 됐다.
            resolved = [e for e in _events(run)
                        if (e.get("ref") or {}).get("kind") == "gate-resolved"]
            self.assertEqual([e["ref"]["gate_id"] for e in resolved], [target])

            policy = GatePolicy.from_dict({})
            self.assertTrue(is_resolved(_events(run), target, GATE_ESCALATION_REQUIRED, policy))
            self.assertFalse(is_resolved(_events(run), other, GATE_ESCALATION_REQUIRED, policy),
                             "지목하지 않은 게이트는 미해소로 남는다")
            # 파생 큐에도 나머지 1건만 남는다.
            self.assertEqual([g["gate_id"] for g in pending_gates(_events(run), policy)], [other])

    # g3 — --gate-id 가 pending 에 없는 id → 비영 종료 · 원장 무변경.
    def test_g3_absent_gate_id_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_ESCALATION_REQUIRED, "g-esc-only")
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")

            rc, _out, err = self._run_cli(
                [str(run), "--gate-kind", "escalation", "--actor", "Advisor",
                 "--gate-id", "gate-does-not-exist"])

            self.assertNotEqual(rc, 0)
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 바이트 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before, "revisions.jsonl 무변경")
            self.assertIn("gate-does-not-exist", err)
            self.assertIn("pending_gates 에 없다", err)

    # g4 — --gate-id 는 실재하나 gateKind 불일치 → 비영 종료 · 사유 문면 · 원장 무변경.
    def test_g4_gate_id_kind_mismatch_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_valid_plan())
            _add_pending_gate(run, GATE_ESCALATION_REQUIRED, "g-esc-other", "unit-b")
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")

            # escalation 을 요청하면서 user_decision 게이트를 지목했다.
            rc, _out, err = self._run_cli(
                [str(run), "--gate-kind", "escalation", "--actor", "Advisor",
                 "--gate-id", "g-struct"])

            self.assertNotEqual(rc, 0)
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 바이트 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before, "revisions.jsonl 무변경")
            self.assertIn("gateKind 가 요청과 다르다", err)
            self.assertIn(GATE_USER_DECISION_REQUIRED, err)

    # g5 — recover_gate 단위: 다중 매칭은 ValueError(후보 포함) · 지목/미지목 반환 계약.
    def test_g5_recover_gate_unit_contract(self):
        with tempfile.TemporaryDirectory() as td:
            run = self._two_escalation_run(td)

            with self.assertRaises(ValueError) as ctx:
                rg.recover_gate(run, GATE_ESCALATION_REQUIRED)
            msg = str(ctx.exception)
            self.assertIn("gate-unit-a::exec-escalation", msg)
            self.assertIn("gate-unit-b::exec-escalation", msg)
            self.assertIn("--gate-id", msg)

            # 지목하면 그 gate_id 를 그대로 돌려준다.
            gid, pend = rg.recover_gate(run, GATE_ESCALATION_REQUIRED,
                                        gate_id="gate-unit-b::exec-escalation")
            self.assertEqual(gid, "gate-unit-b::exec-escalation")
            self.assertEqual(len(pend), 2)

            # 부재 id·kind 불일치는 (None, pending) — raise 아님.
            self.assertEqual(rg.recover_gate(run, GATE_ESCALATION_REQUIRED, gate_id="nope")[0],
                             None)
            self.assertEqual(
                rg.recover_gate(run, GATE_USER_DECISION_REQUIRED,
                                gate_id="gate-unit-a::exec-escalation")[0],
                None)

            # 매칭 0건(다른 kind)은 기존대로 (None, pending) — 기본 인자 계약 보존.
            self.assertEqual(rg.recover_gate(run, GATE_USER_DECISION_REQUIRED)[0], None)


# --------------------------------------------------------------------------
# 백로그 §L Desired 4 — per-unit timeout (D-T1·D-T2 검증 + 접합부 실물 왕복)
#
# 스키마: impl-plan task 의 **선택 12번째 키** timeout(실행 예산 초·양의 정수).
# 부재 = 전역 fallback(무검사 통과). REQUIRED_TASK_KEYS 11키는 무변.
# --------------------------------------------------------------------------
def _plan_with_timeout(value, *, sentinel=object()):
    """첫 implementation 단위에만 timeout 을 얹은 유효 계획(그 외 단위는 미지정)."""
    plan = _valid_plan()
    if value is not sentinel:
        plan["tasks"][0]["timeout"] = value
    return plan


class TestPerUnitTimeoutValidation(unittest.TestCase):
    """D-T1·D-T2 — 키 존재 시 양의 정수만 수용(판정 불가 ≠ 통과·fail-closed)."""

    def _errors(self, value):
        return [e for e in rg.validate_impl_plan_adapter(_plan_with_timeout(value))
                if "timeout" in e]

    def test_absent_key_passes(self):
        # 부재 = 무검사(하위호환) — 기존 계획이 그대로 통과해야 한다.
        self.assertEqual(rg.validate_impl_plan_adapter(_valid_plan()), [])

    def test_positive_int_passes(self):
        self.assertEqual(rg.validate_impl_plan_adapter(_plan_with_timeout(1200)), [])

    def test_invalid_values_rejected(self):
        # bool·0·음수·실수·문자열 — 전부 오류 목록에 오른다(각각 독립 판정).
        for bad in (0, -5, True, "1200", 1200.5, None):
            with self.subTest(bad=bad):
                errs = self._errors(bad)
                self.assertEqual(len(errs), 1, "%r 는 정확히 1건의 timeout 오류: %r" % (bad, errs))
                self.assertIn("tasks[0]", errs[0])

    def test_required_task_keys_unchanged(self):
        # 필수 키 승격이 아니다 — 11키 집합에 timeout 이 들어가면 기존 계획이 전부 깨진다.
        self.assertNotIn("timeout", set(rg.REQUIRED_TASK_KEYS))
        self.assertEqual(len(rg.REQUIRED_TASK_KEYS), 11)

    def test_invalid_timeout_blocks_via_resolve_gate_ledger_untouched(self):
        # 검증-먼저 — 불량 timeout 은 승격 전에 차단되고 원장은 바이트 무변경이다.
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_plan_with_timeout(-1))
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertNotEqual(rc, 0, "불량 timeout 계획은 비영 종료")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before)
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before)


class _TimeoutRecordingInvoker:
    """수신 request 의 (role, step_id, timeout) 을 기록하는 stub(실 CLI 미발화).

    Verifier(CP2) 는 Pass verdict 를 돌려 run 이 실제로 진행되게 한다.
    """

    def __init__(self):
        self.seen = []

    def invoke(self, request):
        from invoker import InvokeResult, KIND_COMPLETION

        step_id = (request.bundle.get("step_contract") or {}).get("id")
        self.seen.append((request.role, step_id, request.timeout))
        if request.role == "Verifier":
            return InvokeResult(kind=KIND_COMPLETION,
                                completion={"verdict": "Pass", "rework": None}, ref="vd")
        return InvokeResult(
            kind=KIND_COMPLETION,
            completion={"artifacts": [], "self_check": "done", "failures": "없음",
                        "open_questions": "없음", "verify_basis": "self"},
            ref="wr",
        )

    def timeouts_for(self, step_id):
        return [t for (_r, sid, t) in self.seen if sid == step_id]


class TestPerUnitTimeoutRoundTrip(unittest.TestCase):
    """§5.7 접합부 실물 왕복 — 생산 실물을 소비자에게 실제로 먹인다(격리 검증 아님).

    impl-plan.json(timeout 포함) → validate_impl_plan_adapter 실통과 → accept_revision
    (task_added) 실승격 → active_graph fold 에 timeout 잔존 → 엔진 run → stub invoker 가
    수신한 request.timeout 실측. 중간 어느 접합부에서 필드가 탈락해도 마지막 단계가 깨진다.
    """

    GLOBAL_TIMEOUT = 777
    UNIT_TIMEOUT = 1200

    # 실 엔진 run 까지 가려면 delegation 8필드가 채워져 있어야 한다 — 기존 픽스처의 sentinel
    # 2필드만으로는 Host 가 Consult 에서 scoped-query 로 에스컬레이션한다(디스패치 0). 검증
    # 대상은 timeout 전파이므로 이 클래스 전용으로 위임 필드를 채운 픽스처를 별도로 둔다.
    @staticmethod
    def _fill_delegation(task):
        task["delegation"] = dict(
            _SENTINEL_DELEG,
            **{"from": "Advisor", "to": "Worker", "input": "설계 문서",
               "output": task["ownedBoundary"][0], "context": ["docs/solution-design.md"],
               "constraints": "워크스페이스 밖 파일 금지"},
        )
        return task

    def _plan(self):
        plan = _plan_with_timeout(self.UNIT_TIMEOUT)
        for t in plan["tasks"]:
            self._fill_delegation(t)
        return plan

    def _proposal_node(self):
        return self._fill_delegation(_seed_proposal_task())

    def test_impl_plan_timeout_reaches_invoke_request(self):
        with tempfile.TemporaryDirectory() as td:
            plan = self._plan()
            timed_id = plan["tasks"][0]["id"]          # impl-auth — 지정 단위.
            plain_id = plan["tasks"][1]["id"]          # impl-api  — 미지정 단위(대조).
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=plan,
                             graph_tasks=[self._proposal_node()])

            # 전역 예산을 config 에 실어 per-unit 값과 구분 가능하게 한다(k_common 소비 키).
            cfg = json.loads((run / "config.json").read_text(encoding="utf-8"))
            cfg["timeout"] = self.GLOBAL_TIMEOUT
            (run / "config.json").write_text(json.dumps(cfg), encoding="utf-8")

            # ① 실 resolver 경로로 검증·해소·승격(픽스처 우회 0).
            rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human"])
            self.assertEqual(rc, 0, "timeout 포함 유효 계획은 정상 해소·승격")

            # ② 승격된 revision payload 에 timeout 이 잔존한다(fold._copy_task 얕은 복제).
            added = [r for r in _read_jsonl(run / "revisions.jsonl")
                     if r.get("kind") == "task_added"]
            timed_rev = next(r for r in added if (r.get("payload") or {}).get("id") == timed_id)
            self.assertEqual((timed_rev["payload"]).get("timeout"), self.UNIT_TIMEOUT)

            # ③ active_graph fold 에도 잔존한다(엔진이 읽는 파생 뷰).
            inv = _TimeoutRecordingInvoker()
            orch, _cfg = rg.build_orchestrator_k(run, inv)
            graph_tasks = {t.get("id"): t for t in orch.active_graph().get("tasks") or []}
            self.assertEqual(graph_tasks[timed_id].get("timeout"), self.UNIT_TIMEOUT)
            self.assertNotIn("timeout", graph_tasks[plain_id])
            self.assertEqual(orch._unit_timeouts(), {timed_id: self.UNIT_TIMEOUT})

            # ④ 실 엔진 run — stub invoker 가 수신한 request.timeout 실측.
            orch.run()
            self.assertTrue(inv.seen, "엔진이 실제로 디스패치했어야 한다")
            self.assertEqual(set(inv.timeouts_for(timed_id)), {self.UNIT_TIMEOUT},
                             "지정 단위의 전 요청이 단위 예산: %r" % (inv.seen,))
            self.assertEqual(set(inv.timeouts_for(plain_id)), {self.GLOBAL_TIMEOUT},
                             "미지정 단위의 전 요청은 전역 예산: %r" % (inv.seen,))


# --------------------------------------------------------------------------
# 백로그 N — 조건부 승인의 하류 전달 (D-N1·D-N2·D-N3·D-N7 + 접합부 실물 왕복)
#
# 결함: 사용자가 "조건부 승인"으로 단 조건이 provenance 원장에만 남고 실행 단위에는 닿지
# 않았다. 채널 = 구조 게이트 해소 시 승격 payload 의 delegation.context 주입(원 impl-plan
# 파일은 무변조 · 원장은 원문을 계속 소유).
# --------------------------------------------------------------------------
_COND_RESPONSE = "로그 마스킹을 적용한 뒤 진행하라"


def _plan_with_context(ctx):
    """모든 task 의 delegation.context 를 ctx 로 고정한 유효 계획(그 외 필드는 기존 sentinel)."""
    plan = _valid_plan()
    for t in plan["tasks"]:
        t["delegation"] = dict(_SENTINEL_DELEG, context=ctx)
    return plan


def _promoted_payloads(run: Path):
    return [r.get("payload") or {} for r in _read_jsonl(run / "revisions.jsonl")
            if r.get("kind") == "task_added"]


def _contexts_of(run: Path):
    return [((p.get("delegation") or {}).get("context")) for p in _promoted_payloads(run)]


def _resolve(run: Path, *args):
    """구조 게이트를 실 CLI 경로(main)로 해소한다 — 표준출력을 함께 포획해 반환."""
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = rg.main([str(run), "--gate-kind", "user_decision", "--actor", "human", *args])
    return rc, buf.getvalue()


class TestGateConditionInjection(unittest.TestCase):
    """D-N1·D-N2 — 비공백 응답이 승격 payload 전건의 delegation.context 에 주입된다."""

    def _expected(self, gate_id="g-struct", actor="human", response=_COND_RESPONSE):
        return "[게이트 조건 — %s 해소(actor=%s)] %s" % (gate_id, actor, response)

    def test_condition_reaches_every_promoted_task(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_plan_with_context(["docs/solution-design.md"]))
            plan_sha = _sha(run / "workspace" / "impl-plan.json")

            rc, _out = _resolve(run, "--response", _COND_RESPONSE)
            self.assertEqual(rc, 0)

            # (a) 승격 전건(3건)에 조건 항목이 실린다 — D-N4 균일 적용.
            ctxs = _contexts_of(run)
            self.assertEqual(len(ctxs), 3, "impl 2 + milestone 1 전건 승격")
            for ctx in ctxs:
                self.assertEqual(ctx, ["docs/solution-design.md", self._expected()])

            # (b) 원 산출(impl-plan.json)은 바이트 무변조 — 주입은 payload 사본에만.
            self.assertEqual(_sha(run / "workspace" / "impl-plan.json"), plan_sha)

            # (c) 조건 **원문**은 provenance 이벤트가 계속 소유한다(원장 분리 보존).
            prov = [e for e in _events(run)
                    if (e.get("ref") or {}).get("kind") == "gate-resolution-provenance"]
            self.assertEqual(len(prov), 1)
            self.assertEqual(prov[0]["ref"]["response"], _COND_RESPONSE)

    def test_condition_text_is_deterministic(self):
        # D-N2 — 타임스탬프 없음(같은 입력 → 같은 문면). gate_id·actor 로 이벤트와 상호 추적.
        self.assertEqual(rg.format_condition("g-1", "human", "조건"),
                         "[게이트 조건 — g-1 해소(actor=human)] 조건")

    def test_gate_id_and_actor_are_embedded(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "gate-xyz",
                             plan=_plan_with_context(["docs/a.md"]))
            rc, _out = _resolve(run, "--response", _COND_RESPONSE)
            self.assertEqual(rc, 0)
            for ctx in _contexts_of(run):
                self.assertEqual(ctx[-1], self._expected(gate_id="gate-xyz"))


class TestGateConditionBehaviorPreserved(unittest.TestCase):
    """거동 보존 — 응답이 없거나 공백이면 주입 0(승격 payload = plan task 동일)."""

    def _assert_no_injection(self, run: Path, plan):
        payloads = _promoted_payloads(run)
        self.assertEqual(payloads, plan["tasks"], "주입 0 — 승격 payload 가 plan task 와 동일")

    def test_absent_response_injects_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            plan = _plan_with_context(["docs/a.md"])
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=plan)
            rc, out = _resolve(run)
            self.assertEqual(rc, 0)
            self._assert_no_injection(run, plan)
            self.assertNotIn("[CONDITION]", out, "미주입 시 조건 라인 없음(D-N7)")

    def test_blank_response_injects_nothing(self):
        for blank in ("", "   ", "\t\n "):
            with self.subTest(blank=repr(blank)), tempfile.TemporaryDirectory() as td:
                plan = _plan_with_context(["docs/a.md"])
                run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=plan)
                rc, out = _resolve(run, "--response", blank)
                self.assertEqual(rc, 0)
                self._assert_no_injection(run, plan)
                self.assertNotIn("[CONDITION]", out)

    def test_legacy_plan_without_context_still_resolves(self):
        # 기존 픽스처(_valid_plan — delegation.context 부재)가 조건부 승인에서도 통과한다.
        # 부재는 "담을 수 없는 형"이 아니라 빈 채널이므로 [조건] 신설로 처리한다.
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            rc, _out = _resolve(run, "--response", _COND_RESPONSE)
            self.assertEqual(rc, 0)
            for ctx in _contexts_of(run):
                self.assertEqual(
                    ctx, ["[게이트 조건 — g-struct 해소(actor=human)] " + _COND_RESPONSE])


class TestGateConditionCreatedContextNotice(unittest.TestCase):
    """context 부재 신설의 관측 신호 — 조건 주입이 위임 결함을 가리지 않게 표면화(차단 아님).

    부재 단위는 종전이라면 Host 가 디스패치 직전 missing_fields(delegation.context)로 잡아
    Escalated 시켰을 단위다. 주입으로 디스패치 가능해지므로 그 사실을 침묵시키지 않는다.
    """

    def test_absent_context_is_reported_with_task_ids(self):
        with tempfile.TemporaryDirectory() as td:
            plan = _valid_plan()                       # delegation.context 부재.
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=plan)

            rc, out = _resolve(run, "--response", _COND_RESPONSE)

            self.assertEqual(rc, 0, "관측 신호일 뿐 차단이 아니다(rc 무변)")
            self.assertIn("[CONDITION-NOTE]", out)
            for t in plan["tasks"]:
                self.assertIn(t["id"], out.split("[CONDITION-NOTE]")[1],
                              "신설된 단위 id 가 주의 라인에 열거되어야 한다")
            self.assertIn("delegation.context 부재", out)
            self.assertIn("Escalated", out)

    def test_present_list_context_emits_no_notice(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_plan_with_context(["docs/a.md"]))
            rc, out = _resolve(run, "--response", _COND_RESPONSE)
            self.assertEqual(rc, 0)
            self.assertIn("[CONDITION]", out, "주입 자체는 일어났다")
            self.assertNotIn("[CONDITION-NOTE]", out, "context 실재 시 주의 라인 없음")

    def test_created_list_is_reported_per_task(self):
        # 혼재 계획 — 일부만 context 부재. 신설된 단위만 목록에 오른다(순수 함수 층 직접 판정).
        plan = _valid_plan()
        plan["tasks"][1]["delegation"] = dict(_SENTINEL_DELEG, context=["docs/a.md"])
        _payloads, errors, injected, created = rg.build_promotion_payloads(
            plan["tasks"], "g-struct", "human", _COND_RESPONSE)

        self.assertEqual(errors, [])
        self.assertEqual(injected, 3)
        self.assertEqual(created, [plan["tasks"][0]["id"], plan["tasks"][2]["id"]])

    def test_no_response_emits_no_notice(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=_valid_plan())
            rc, out = _resolve(run)
            self.assertEqual(rc, 0)
            self.assertNotIn("[CONDITION-NOTE]", out, "주입 0 이면 신설도 0")


class TestGateConditionTypeRules(unittest.TestCase):
    """D-N3 — list=사본 append · str=[원문, 조건] · 그 외 형=원장 무오염 비영 종료."""

    def test_list_context_appends_on_a_copy(self):
        # 원본 plan 객체는 변조되지 않는다(사본 규율) — 순수 함수 층에서 직접 판정.
        plan = _plan_with_context(["docs/a.md", "docs/b.md"])
        original = json.loads(json.dumps(plan))
        payloads, errors, injected, created = rg.build_promotion_payloads(
            plan["tasks"], "g-struct", "human", _COND_RESPONSE)

        self.assertEqual(errors, [])
        self.assertEqual(injected, 3)
        self.assertEqual(created, [], "기존 context 가 있으므로 신설 0")
        self.assertEqual(plan, original, "plan 객체 무변조(사본에만 주입)")
        for p in payloads:
            self.assertEqual(len(p["delegation"]["context"]), 3)
            self.assertEqual(p["delegation"]["context"][:2], ["docs/a.md", "docs/b.md"])

    def test_string_context_is_promoted_to_two_element_list(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_plan_with_context("docs/single.md"))
            rc, _out = _resolve(run, "--response", _COND_RESPONSE)
            self.assertEqual(rc, 0)
            for ctx in _contexts_of(run):
                self.assertEqual(
                    ctx,
                    ["docs/single.md",
                     "[게이트 조건 — g-struct 해소(actor=human)] " + _COND_RESPONSE])

    def test_unsupported_context_type_aborts_with_untouched_ledger(self):
        # dict context + 비공백 응답 → 조건이 담길 곳이 없다. 침묵 탈락 대신 비영 종료하고
        # 원장은 바이트 무변경이어야 한다(주입 선구성이 어떤 append 보다 앞선다).
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_plan_with_context({"docs": "a.md"}))
            ev_before, rev_before = _sha(run / "events.jsonl"), _sha(run / "revisions.jsonl")

            rc, _out = _resolve(run, "--response", _COND_RESPONSE)

            self.assertNotEqual(rc, 0, "주입 불가 형은 비영 종료")
            self.assertEqual(_sha(run / "events.jsonl"), ev_before, "events.jsonl 바이트 무변경")
            self.assertEqual(_sha(run / "revisions.jsonl"), rev_before,
                             "revisions.jsonl 바이트 무변경")

    def test_unsupported_context_type_passes_when_no_condition(self):
        # 대조 — 응답이 없으면 dict context 라도 종전대로 통과한다(가법 보장·주입 경로만 판정).
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_plan_with_context({"docs": "a.md"}))
            rc, _out = _resolve(run)
            self.assertEqual(rc, 0, "주입 0 경로는 context 형을 보지 않는다")

    def test_context_is_not_inspected_by_delegation_reference_check(self):
        # 검증 축(정본 열거): 어댑터 검증기는 delegation.task/done 참조형만 본다 —
        # context 에 항목이 늘어도 검증과 충돌하지 않는다(주입의 전제).
        for ctx in (["docs/a.md", "조건"], "docs/a.md", {"docs": "a.md"}, None):
            with self.subTest(ctx=ctx):
                self.assertEqual(rg.validate_impl_plan_adapter(_plan_with_context(ctx)), [])


class TestGateConditionOutputSurface(unittest.TestCase):
    """D-N7 — 주입은 조용히 일어나지 않는다(건수 명시)."""

    def test_condition_line_reports_count(self):
        with tempfile.TemporaryDirectory() as td:
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct",
                             plan=_plan_with_context(["docs/a.md"]))
            rc, out = _resolve(run, "--response", _COND_RESPONSE)
            self.assertEqual(rc, 0)
            self.assertIn("[CONDITION]", out)
            self.assertIn("승격 3 건", out)


class _BundleRecordingInvoker:
    """수신 번들을 역할별로 기록하는 stub(실 CLI 미발화) — 조건의 물리 도달 실측용."""

    def __init__(self):
        self.exec_material = []     # (step_id, bundle.memory_material)
        self.verify_context = []    # (step_id, verify_bundle.step_contract.delegation.context)

    def invoke(self, request):
        from invoker import InvokeResult, KIND_COMPLETION

        bundle = request.bundle or {}
        contract = bundle.get("step_contract") or {}
        step_id = contract.get("id")
        if request.role == "Verifier":
            self.verify_context.append(
                (step_id, (contract.get("delegation") or {}).get("context")))
            return InvokeResult(kind=KIND_COMPLETION,
                                completion={"verdict": "Pass", "rework": None}, ref="vd")
        self.exec_material.append((step_id, bundle.get("memory_material")))
        return InvokeResult(
            kind=KIND_COMPLETION,
            completion={"artifacts": [], "self_check": "done", "failures": "없음",
                        "open_questions": "없음", "verify_basis": "self"},
            ref="wr",
        )

    def material_for(self, step_id):
        return [m for (sid, m) in self.exec_material if sid == step_id]

    def verify_for(self, step_id):
        return [c for (sid, c) in self.verify_context if sid == step_id]


class TestGateConditionRoundTrip(unittest.TestCase):
    """§5.7 접합부 실물 왕복 — 생산 실물을 소비자에게 실제로 먹인다(격리 검증 아님).

    실 CLI argv → revision payload → active_graph fold → 엔진 run → Worker 실행 번들의
    memory_material · CP2 verify 번들의 step_contract.delegation.context 양쪽에서 조건을
    실측한다. 중간 어느 접합부(fold·Step.from_dict 화이트리스트·번들 조립)에서 탈락해도
    마지막 단계가 깨진다.
    """

    BASE_CONTEXT = "docs/solution-design.md"

    @staticmethod
    def _fill_delegation(task):
        # 실 엔진 run 까지 가려면 위임 8필드가 채워져 있어야 한다(미충족 시 Host 가 Consult
        # 에서 에스컬레이션해 디스패치 0). 검증 대상은 조건 전파이므로 전용 픽스처를 둔다.
        task["delegation"] = dict(
            _SENTINEL_DELEG,
            **{"from": "Advisor", "to": "Worker", "input": "설계 문서",
               "output": task["ownedBoundary"][0],
               "context": [TestGateConditionRoundTrip.BASE_CONTEXT],
               "constraints": "워크스페이스 밖 파일 금지"},
        )
        return task

    def test_condition_reaches_worker_bundle_and_cp2(self):
        with tempfile.TemporaryDirectory() as td:
            plan = _valid_plan()
            for t in plan["tasks"]:
                self._fill_delegation(t)
            unit_id = plan["tasks"][0]["id"]        # impl-auth
            run = _build_run(Path(td), GATE_USER_DECISION_REQUIRED, "g-struct", plan=plan,
                             graph_tasks=[self._fill_delegation(_seed_proposal_task())])

            expected = "[게이트 조건 — g-struct 해소(actor=human)] " + _COND_RESPONSE

            # ① 실 resolver CLI 경로(픽스처 우회 0).
            rc, out = _resolve(run, "--response", _COND_RESPONSE)
            self.assertEqual(rc, 0)
            self.assertIn("[CONDITION]", out)

            # ② revision 원장 payload 에 주입 잔존.
            for ctx in _contexts_of(run):
                self.assertEqual(ctx, [self.BASE_CONTEXT, expected])

            # ③ active_graph fold 에도 잔존한다(엔진이 읽는 파생 뷰).
            inv = _BundleRecordingInvoker()
            orch, _cfg = rg.build_orchestrator_k(run, inv)
            folded = {t.get("id"): t for t in orch.active_graph().get("tasks") or []}
            self.assertEqual(folded[unit_id]["delegation"]["context"],
                             [self.BASE_CONTEXT, expected])

            # ④ 실 엔진 run — Worker 실행 번들과 CP2 검증 번들 양쪽에서 실측.
            orch.run()
            self.assertTrue(inv.exec_material, "엔진이 실제로 디스패치했어야 한다")
            material = inv.material_for(unit_id)
            self.assertTrue(material, "대상 단위가 디스패치되지 않았다: %r" % (inv.exec_material,))
            for m in material:
                self.assertEqual(m, [self.BASE_CONTEXT, expected],
                                 "Worker fresh-context 번들 memory_material 에 조건 도달")
            verified = inv.verify_for(unit_id)
            self.assertTrue(verified, "CP2 verify 번들이 없다: %r" % (inv.verify_context,))
            for c in verified:
                self.assertIn(expected, c, "CP2 verify 번들 step_contract 에도 조건 도달")


if __name__ == "__main__":
    unittest.main()
