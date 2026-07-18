"""프로덕션 게이트 resolver (F5·OQ-PO-B3) — headless 엔진 정지 게이트를 주 세션이 해소.

이 스크립트는 headless Orchestrator(05 §2.2)가 물리 정지(exit 2·stop-signal.json)한
정지 게이트를 **주 세션(사용자 대화 주체)** 이 이벤트 로그 append 로 해소하는 브리지다
(project-orchestration-binding §3.3 해소 응답 → 게이트 해소 이벤트 append). 엔진을
대체하지 않는다 — 원장(events.jsonl)에 append 만 하며, 다음 재기동 시 `_process_gates`
가 그 해소 이벤트를 파생 판정(`is_resolved`)해 통과시킨다(결정적 재개).

비프로덕션 드라이버 `orchestration-data/e2e/resolve_w.py` 를 **일반화**하되 그 구조 검사
헬퍼(`_cycle_error`·`_relpath_errors`·`_protected_errors`·`_overlaps` 등)와 해소 조립
(`build_orchestrator_k`)은 **import 재사용**한다(재정의 0). 단 impl-plan 검증은
`resolve_w.validate_impl_plan`(모든 task 를 implementation 으로 강제·milestone 거부)을
그대로 쓰지 않고 F4(contract_to_graph) 계약을 수용하는 `validate_impl_plan_adapter` 로
교체한다(F4↔F5 계약 정합 — milestone 단위 수용). 게이트 불가침: actor 자격은 코드(gates.py
`is_eligible_resolver`/`is_resolved`)가 소유하며 이 스크립트가 우회하지 않는다.

사용법:
  python orchestration/adapters/claude/resolve_gate.py <run_dir> \
      --gate-kind {user_decision|escalation|approval-escalation} \
      --actor {human|Advisor} [--response "<원문>"]

동작 요약:
  - stop-signal.json 에서 해소 대상 gate_id·gateKind 복원(계약 =
    {stop_reason, stopped_tasks, pending_gates:[{gate_id,gateKind,target,scoped_question,since}]}).
  - 구조 게이트(user_decision_required, impl-plan 방출 후):
      1) run_dir/workspace/impl-plan.json 을 **먼저** validate_impl_plan 으로 검증.
         실패 시 오류 열거 + 비영 종료 · **원장 무변경**(해소/revision append 0).
      2) 통과 시 actor 자격 확인(gates.is_eligible_resolver) — user_decision 은 actor=human
         만 적격(binding §3.3). 부적격 actor 는 원장 무변경 + 비영 종료.
      3) 적격 시 provenance annotation + append_gate_resolution(actor) append.
         그 뒤 방출된 각 구현 task 를 accept_revision(KIND_TASK_ADDED, ...,
         proposingStepRef="impl-plan-phase1", gateEventRef=gate_id) 로 승격
         (accept_revision 이 gate-pass 이벤트 실재를 재검증).
  - escalation 게이트(CP3 non-Pass escalation 포함): actor ∈ escalationResolvers 자격 확인 후
    append_gate_resolution(actor) append. revision 승격 없음(escalation 은 분해 제안 아님).

정직 규율(resolve_w L-07 동형): simulated=false·실제 actor 기록. 검증 실패·부적격은
열거 + 비영 종료, 자동 수정 0.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# --- 경로 배선: 비프로덕션 드라이버(e2e) 를 import 경로에 둔다(그 함수만 재사용) ----------
#   resolve_gate.py = orchestration/adapters/claude/resolve_gate.py
#   parents[2] = repo root.
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
E2E_DIR = REPO_ROOT / "uahf" / "framework" / "adapters" / "claude" / "orchestration-data" / "e2e"
if str(E2E_DIR) not in sys.path:
    sys.path.insert(0, str(E2E_DIR))

# k_common import 가 _orch_common 을 통해 중립 코드 경로(orchestrator·step-host·step-invoker)
# 를 sys.path 에 배선한다(먼저 로드되어야 함·무수정 재사용).
from k_common import build_orchestrator_k, load_json  # noqa: E402

# 비프로덕션 드라이버 resolve_w 의 **구조 검사 public 헬퍼**를 재사용한다(재정의 0·무수정 import).
# resolve_w.validate_impl_plan 자체는 쓰지 않는다 — 그것은 모든 task 를
# unitType=="implementation" 으로 강제해 F4(contract_to_graph)의 milestone 단위를 거부하기
# 때문이다(F4↔F5 계약 모순). 어댑터 검증기(validate_impl_plan_adapter)가 unitType/개수 규칙만
# F4 계약으로 교체하고, 그 외 구조 검사(11키·상대경로/보호경계·비중첩·사이클·delegation)는
# 아래 헬퍼로 **동일 강도** 재사용한다.
from resolve_w import (  # noqa: E402
    REQUIRED_TASK_KEYS,
    _cycle_error,
    _norm,
    _overlaps,
    _protected_errors,
    _relpath_errors,
)
from delegation_check import delegation_errors_for_task  # noqa: E402

# 중립 게이트 평가기(무수정 라이브러리).
from gates import (  # noqa: E402
    GATE_ESCALATION_REQUIRED,
    GATE_USER_DECISION_REQUIRED,
    GatePolicy,
    append_gate_resolution,
    is_resolved,
)
from revision import KIND_TASK_ADDED  # noqa: E402
from events import EventLog, JsonlEventStore  # noqa: E402


# CLI gate-kind → 중립 gateKind 상수. approval-escalation = CP3 non-Pass 시 escalation 으로
# 승격된 정지 게이트(STOPPING_GATES 는 escalation/user_decision 뿐 — approval_required 는
# 정지 게이트가 아니라 CP3 마커이며 비Pass 시 escalation_required 로 정지한다).
GATE_KIND_MAP = {
    "user_decision": GATE_USER_DECISION_REQUIRED,
    "escalation": GATE_ESCALATION_REQUIRED,
    "approval-escalation": GATE_ESCALATION_REQUIRED,
}

IMPL_PLAN_FILE = "impl-plan.json"
PROPOSING_STEP_REF = "impl-plan-phase1"

PROVENANCE_NOTE = (
    "주 세션이 headless 엔진의 정지 게이트를 해소한 provenance 기록 — 시뮬레이션 아님"
    "(simulated=false). actor 는 실제 해소 주체이며, 자격은 gates.py"
    "(is_eligible_resolver/is_resolved)가 코드로 소유한다(이 스크립트는 우회하지 않는다)."
)


class _NoInvoke:
    """해소는 디스패치가 아니다 — 오케스트레이터 재구성 전용 no-op invoker(실 CLI 미호출)."""

    def invoke(self, request):  # noqa: ANN001, D401
        raise RuntimeError(
            "resolve_gate 는 실행하지 않는다(게이트 해소·revision append 전용·엔진 대체 아님)"
        )


# ==========================================================================
# 어댑터 impl-plan 검증기 — F4(contract_to_graph) 계약 수용 (unitType/개수 규칙만 교체)
# ==========================================================================
# F4 계약(contract_to_graph._done_ac·_seed_prompt·gate_policy)와 **정확히 일치**한다:
#   - tasks 3~6개(총 개수).
#   - 각 task unitType ∈ {implementation, milestone}.
#   - milestone ≥ 1(CP3 approval_required 트리거 단위·phase 경계 승인)·implementation ≥ 1.
#   - milestone 은 DAG 종단 — 어떤 task 도 milestone 을 dependsOn 하지 않는다(milestone 자신은
#     implementation 을 dependsOn 할 수 있다). (contract_to_graph._seed_prompt 계약.)
# 그 외 구조 검사(11키·id 유일·dependsOn 무결성/자기참조/사이클(DAG)·ownedBoundary 상대경로/
# 보호경계/상호 비중첩·done 비공백·delegation 참조형)는 resolve_w 헬퍼로 동일 강도 재사용한다.
_ADAPTER_MIN_TASKS = 3
_ADAPTER_MAX_TASKS = 6
_ADAPTER_UNIT_TYPES = ("implementation", "milestone")


def validate_impl_plan_adapter(plan) -> list:
    """F4 계약을 수용하는 impl-plan 구조 검증 — 오류 목록 반환(빈 목록 = 통과). 순수 함수."""
    if not isinstance(plan, dict):
        return ["impl-plan 최상위가 단일 객체(dict)가 아니다: %s" % type(plan).__name__]

    tasks = plan.get("tasks")
    if not isinstance(tasks, list):
        return ["tasks 가 리스트가 아니다: %r" % (tasks,)]
    if not (_ADAPTER_MIN_TASKS <= len(tasks) <= _ADAPTER_MAX_TASKS):
        return ["tasks 개수가 %d~%d개 범위를 벗어난다: %d 개"
                % (_ADAPTER_MIN_TASKS, _ADAPTER_MAX_TASKS, len(tasks))]

    errors: list = []
    seen_ids: set = set()
    ob_by_task: list = []       # (index, [정규화 ownedBoundary]) — 상호 비중첩 검사용.
    milestone_ids: set = set()  # milestone 단위 id — DAG 종단 검사용.

    # 1차 스윕: id 집합·milestone id 확정(참조 무결성·종단 검사 기준).
    id_list = [t.get("id") for t in tasks
               if isinstance(t, dict) and isinstance(t.get("id"), str) and t.get("id").strip()]
    id_set = set(id_list)
    for t in tasks:
        if isinstance(t, dict) and t.get("unitType") == "milestone":
            tid = t.get("id")
            if isinstance(tid, str) and tid.strip():
                milestone_ids.add(tid)

    unit_types: list = []
    for i, t in enumerate(tasks):
        where = "tasks[%d]" % i
        if not isinstance(t, dict):
            errors.append("%s 가 객체(dict)가 아니다: %s" % (where, type(t).__name__))
            ob_by_task.append((i, []))
            continue

        # 11키.
        for k in REQUIRED_TASK_KEYS:
            if k not in t:
                errors.append("%s 필수 키 누락: %r" % (where, k))

        # unitType 집합 소속(F4).
        ut = t.get("unitType")
        unit_types.append(ut)
        if ut not in _ADAPTER_UNIT_TYPES:
            errors.append("%s unitType 이 {implementation, milestone} 중 하나가 아니다: %r"
                          % (where, ut))

        # id 유일성.
        tid = t.get("id")
        if not isinstance(tid, str) or not tid.strip():
            errors.append("%s id 가 비어 있지 않은 문자열이어야 한다: %r" % (where, tid))
        elif tid in seen_ids:
            errors.append("%s id 중복: %r" % (where, tid))
        else:
            seen_ids.add(tid)

        # dependsOn 참조 무결성(계획 내 id 만·자기참조 금지) + milestone 종단.
        dep = t.get("dependsOn")
        if not isinstance(dep, list):
            errors.append("%s dependsOn 이 리스트가 아니다: %r" % (where, dep))
        else:
            for d in dep:
                if d == tid:
                    errors.append("%s dependsOn 에 자기 자신이 포함됨(자기참조 금지): %r" % (where, tid))
                elif d not in id_set:
                    errors.append("%s dependsOn 참조가 계획 내 task id 가 아니다: %r" % (where, d))
                elif d in milestone_ids:
                    # milestone 은 DAG 마지막 경계 노드 — 어떤 task 도 이를 dependsOn 할 수 없다.
                    errors.append(
                        "%s 가 milestone 단위 %r 를 dependsOn 한다(milestone 은 DAG 종단·다른 "
                        "단위가 의존 불가·F4 계약)" % (where, d)
                    )

        # ownedBoundary 상대경로·보호 경계(resolve_w 헬퍼 재사용).
        ob = t.get("ownedBoundary")
        norm_items: list = []
        if not isinstance(ob, list) or len(ob) == 0:
            errors.append("%s ownedBoundary 가 비어 있지 않은 리스트가 아니다: %r" % (where, ob))
        else:
            for item in ob:
                errors.extend(_relpath_errors(item, where))
                errors.extend(_protected_errors(item, where))
                if isinstance(item, str) and item.strip():
                    norm_items.append(_norm(item))
        ob_by_task.append((i, norm_items))

        # done 비공백 문자열.
        done = t.get("done")
        if not isinstance(done, str) or not done.strip():
            errors.append("%s done 이 비어 있지 않은 문자열이어야 한다(비공백): %r" % (where, done))

        # delegation.task/done 참조형 표준(resolve_w 와 동일 함수 재사용).
        errors.extend(delegation_errors_for_task(t, where=where))

    # 배합 규칙(F4): milestone ≥ 1 · implementation ≥ 1.
    if unit_types.count("milestone") < 1:
        errors.append("milestone 단위가 최소 1건이어야 한다(CP3 approval 트리거·F4 계약): unitTypes=%r"
                      % (unit_types,))
    if unit_types.count("implementation") < 1:
        errors.append("implementation 단위가 최소 1건이어야 한다(F4 계약): unitTypes=%r" % (unit_types,))

    # ownedBoundary 상호 비중첩(resolve_w 헬퍼 재사용).
    for a in range(len(ob_by_task)):
        ia, items_a = ob_by_task[a]
        for b in range(a + 1, len(ob_by_task)):
            ib, items_b = ob_by_task[b]
            for pa in items_a:
                for pb in items_b:
                    if _overlaps(pa, pb):
                        errors.append(
                            "tasks[%d]·tasks[%d] ownedBoundary 가 상호 중첩된다(비중첩 위반): "
                            "%r ↔ %r" % (ia, ib, pa, pb)
                        )

    # 사이클(DAG) 검사(resolve_w 헬퍼 재사용).
    errors.extend(_cycle_error(tasks))
    return errors


# ==========================================================================
# stop-signal.json 에서 해소 대상 gate_id·gateKind 복원 (추측 0)
# ==========================================================================
def recover_gate(run_dir: Path, wanted_kind: str):
    """stop-signal.json 의 pending_gates 에서 wanted_kind 게이트 gate_id 를 복원한다.

    계약 = {stop_reason, stopped_tasks, pending_gates:[{gate_id,gateKind,target,
    scoped_question,since}]}. 해당 gateKind 게이트가 없으면 (None, 목록) 반환(추측 금지).
    """
    stop = load_json(run_dir / "logs" / "stop-signal.json")
    pending = stop.get("pending_gates") or []
    matches = [g for g in pending if g.get("gateKind") == wanted_kind]
    if not matches:
        return None, pending
    return matches[0]["gate_id"], pending


# ==========================================================================
# provenance annotation + 정직 기록 파일 (L-07 동형)
# ==========================================================================
def _append_provenance(
    log: EventLog, gate_id, gate_kind: str, actor: str, response: str, phase: str
) -> None:
    """실제 해소 provenance annotation append(simulated=false·실제 actor·응답 원문)."""
    log.append(
        cycle_id="annotation::provenance-" + str(gate_id),
        from_stage=None,
        to_stage="note",
        trigger="게이트 해소 provenance",
        outcome="pass",
        actor=actor,
        ref={
            "kind": "gate-resolution-provenance",
            "gate_id": gate_id,
            "gateKind": gate_kind,
            "phase": phase,
            "simulated": False,
            "actor": actor,
            "response": response,
            "note": PROVENANCE_NOTE,
        },
    )


def _write_record(
    run_dir: Path, gate_id, gate_kind: str, actor: str, response: str, resolved: bool
) -> None:
    """정직 기록 파일(gateKind 별·simulated=false·실제 자격 판정 결과 명시)."""
    record = {
        "gate_id": gate_id,
        "gateKind": gate_kind,
        "resolved_by_actor": actor,
        "simulated": False,
        "response": response,
        "resolved": resolved,
        "note": (
            "주 세션 게이트 해소 기록. resolved 는 gates.is_resolved(적격성 포함) 파생 결과다 — "
            "부적격 actor 의 append 는 로그에 남아도 resolved=false 로 게이트가 pending 이다."
        ),
    }
    with open(
        run_dir / "logs" / ("gate-resolution-record-%s.json" % gate_kind),
        "w",
        encoding="utf-8",
    ) as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)


# ==========================================================================
# 구조 게이트(user_decision) 해소 + impl-plan 검증 + 구현 task 승격
# ==========================================================================
def resolve_structural(run_dir: Path, gate_id, actor: str, response: str, policy: GatePolicy) -> int:
    gate_kind = GATE_USER_DECISION_REQUIRED

    # (1) 검증 먼저 — 어떤 원장 append 도 하기 전에. (원장 무오염 보장.)
    cfg = load_json(run_dir / "config.json")
    workspace = cfg.get("workspace_dir") or str(run_dir / "workspace")
    plan_path = Path(workspace) / IMPL_PLAN_FILE
    if not plan_path.exists():
        print("[ERR] impl-plan 부재 — 검증 불가: %s" % plan_path, file=sys.stderr)
        return 1
    plan = load_json(plan_path)

    errors = validate_impl_plan_adapter(plan)
    if errors:
        print("[REJECT] impl-plan 검증 실패 — 자동 수정하지 않는다(정직 실패):", file=sys.stderr)
        for e in errors:
            print("  - %s" % e, file=sys.stderr)
        print("      (게이트 미해소·원장 무오염 — 이벤트/revision 0 append.)", file=sys.stderr)
        return 1

    # (2) actor 자격 확인(gates.py 소유·우회 금지). user_decision 은 actor=human 만 적격.
    #     부적격이면 원장을 오염시키지 않고(해소/revision append 0) 비영 종료한다 — outcome=pass
    #     해소 이벤트를 남기면 accept_revision 근거로 오용될 수 있으므로 append 전에 거부한다.
    if not policy.is_eligible_resolver(gate_kind, actor):
        print(
            "[REJECT] actor=%r 는 %s 해소에 부적격이다(binding §3.3 — user_decision 은 "
            "userActorClass=%r 만 확정 권위). 원장 무변경·게이트 pending 유지."
            % (actor, gate_kind, policy.user_actor_class),
            file=sys.stderr,
        )
        return 3

    # (3) 적격 → provenance + 해소 이벤트 append.
    log = EventLog(JsonlEventStore(str(run_dir / "events.jsonl")))
    _append_provenance(log, gate_id, gate_kind, actor, response, phase="structure")
    append_gate_resolution(log, gate_id, gate_kind, actor=actor)

    resolved = is_resolved(log.all_events(), gate_id, gate_kind, policy)
    _write_record(run_dir, gate_id, gate_kind, actor, response, resolved)
    if not resolved:
        # 방어: 적격성 통과 후에도 is_resolved 가 False 면(요구 이벤트 부재 등) 승격하지 않는다.
        print("[ERR] 해소 이벤트 append 후에도 is_resolved=False — 승격 중단(요구 이벤트 부재?).",
              file=sys.stderr)
        return 4

    # (4) 방출된 구현 task 전체를 task_added revision 으로 승격
    #     (accept_revision 이 gate-pass 이벤트 실재를 재검증).
    orch, _ = build_orchestrator_k(run_dir, _NoInvoke())
    accepted = []
    for st in plan["tasks"]:
        try:
            rev = orch.accept_revision(
                KIND_TASK_ADDED, st, proposingStepRef=PROPOSING_STEP_REF, gateEventRef=gate_id
            )
        except Exception as exc:  # noqa: BLE001  (구조 misuse·근거 미실재 등 정직 표면화)
            print(
                "[REJECT] task_added revision 수용 실패(자동 수정 0·정직 실패): id=%r — %s: %s"
                % (st.get("id"), type(exc).__name__, exc),
                file=sys.stderr,
            )
            return 1
        accepted.append((rev.revisionSeq, st.get("id"), st.get("unitType")))

    print("[RESOLVE] gate_id=%s resolved by actor=%s (simulated=false)." % (gate_id, actor))
    print("[VALIDATE] impl-plan 검증 통과.")
    print("[REVISION] task_added %d 건 append (basis.proposingStepRef=%s gateEventRef=%s):"
          % (len(accepted), PROPOSING_STEP_REF, gate_id))
    for seq, sid, ut in accepted:
        print("  - seq=%s id=%s unitType=%s" % (seq, sid, ut))
    return 0


# ==========================================================================
# escalation 게이트 해소 (revision 승격 없음)
# ==========================================================================
def resolve_escalation(run_dir: Path, gate_id, actor: str, response: str, policy: GatePolicy) -> int:
    gate_kind = GATE_ESCALATION_REQUIRED

    # actor 자격 확인(gates.py 소유). escalation 은 actor ∈ escalationResolvers.
    if not policy.is_eligible_resolver(gate_kind, actor):
        print(
            "[REJECT] actor=%r 는 %s 해소에 부적격이다(허용 resolver=%s). 원장 무변경·pending 유지."
            % (actor, gate_kind, list(policy.escalation_resolvers)),
            file=sys.stderr,
        )
        return 3

    log = EventLog(JsonlEventStore(str(run_dir / "events.jsonl")))
    _append_provenance(log, gate_id, gate_kind, actor, response, phase="escalation")
    append_gate_resolution(log, gate_id, gate_kind, actor=actor)

    resolved = is_resolved(log.all_events(), gate_id, gate_kind, policy)
    _write_record(run_dir, gate_id, gate_kind, actor, response, resolved)
    if not resolved:
        print("[ERR] 해소 이벤트 append 후에도 is_resolved=False(요구 이벤트 부재?).",
              file=sys.stderr)
        return 4

    print("[RESOLVE] gate_id=%s resolved by actor=%s (escalation·simulated=false)." % (gate_id, actor))
    print("[NOTE] escalation 해소는 분해 제안이 아니므로 revision 승격 없음.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="프로덕션 게이트 resolver — headless 엔진 정지 게이트를 주 세션이 해소(F5·OQ-PO-B3)"
    )
    parser.add_argument("run_dir", help="run 데이터 백엔드 디렉터리")
    parser.add_argument(
        "--gate-kind", required=True, choices=tuple(GATE_KIND_MAP.keys()),
        help="user_decision=구조 게이트(impl-plan 검증·구현 task 승격) · "
             "escalation/approval-escalation=escalation_required 해소(승격 없음)",
    )
    parser.add_argument(
        "--actor", required=True,
        help="해소 주체(예: human|Advisor). 자격은 gates.py 가 코드로 판정한다(우회 불가).",
    )
    parser.add_argument(
        "--response", default="",
        help="해소 응답 원문(선택·기록용). 시뮬레이션 아님.",
    )
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).resolve()
    wanted_kind = GATE_KIND_MAP[args.gate_kind]

    gate_id, pending = recover_gate(run_dir, wanted_kind)
    if gate_id is None:
        print("[ERR] 정지 신호에 %s 게이트가 없다 — 해소 불가." % wanted_kind, file=sys.stderr)
        print("      pending=%s" % json.dumps(pending, ensure_ascii=False), file=sys.stderr)
        return 1

    policy = GatePolicy.from_dict(load_json(run_dir / "gate_policy.json"))

    if wanted_kind == GATE_USER_DECISION_REQUIRED:
        return resolve_structural(run_dir, gate_id, args.actor, args.response, policy)
    return resolve_escalation(run_dir, gate_id, args.actor, args.response, policy)


if __name__ == "__main__":
    sys.exit(main())
