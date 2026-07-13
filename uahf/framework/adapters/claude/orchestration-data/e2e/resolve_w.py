"""시나리오 (w) — **실 사용자** 구조 게이트 해소 + impl-plan 검증·구현 task 일괄 편입.

사용법:
  python resolve_w.py <run-dir> --phase structure --user-response "<실 사용자 응답 원문>"

resolve_m.py(m)와의 관계 = **동형·단순화**. (m)은 2단 게이트(구조 + T8 Validating)였으나,
(w)의 구현 단계 게이트는 review_required(비정지)이므로 **구조 게이트 1단**만 사용자 해소가
필요하다 — 따라서 (w)는 structure phase 만 갖는다(final 불필요).

--phase structure 동작(검증 우선·무근거 게이트 해소 회피):
  1. stop-signal.json 에서 정지한 user_decision 게이트 gate_id 회수(추측 0).
  2. impl-plan 산출 impl-plan.json 회수·검증(validate_impl_plan) — **게이트 해소보다 먼저**.
     검증 실패 시 어떤 이벤트도 append 하지 않고(게이트 미해소·원장 무오염) 비0 종료(정직 실패).
  3. 검증 통과 → 실 사용자 구조 게이트 해소(provenance annotation + 해소 이벤트 + 정직 기록·
     simulated=false·actor=human·user_response 원문).
  4. 구현 task 전체(3~6개)를 task_added revision 으로 **일괄 append**
     (각 basis = {proposingStepRef:"impl-plan", gateEventRef:<구조 게이트>} · PO-INV 5).
     accept_revision 이 게이트 통과 이벤트 실재를 검증한 뒤에만 수용한다.

정직성(L-07 양방향):
  - 실 사용자를 시뮬레이션으로 오표기하지 않는다(simulated=false·actor=human·user_response 원문).
  - impl-plan 검증 실패는 자동 수정하지 않고 오류를 열거해 비0 종료한다(정직 실패).

이 스크립트는 orchestration-data/e2e/ 경계 소속이다(비프로덕션 드라이버).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# k_common import 가 중립 코드 경로를 sys.path 에 배선한다(먼저 실행되어야 함·무수정 재사용).
from k_common import build_orchestrator_k, load_json

# 중립 코드 심볼(무수정 라이브러리).
from events import EventLog, JsonlEventStore  # noqa: E402
from gates import GATE_USER_DECISION_REQUIRED, append_gate_resolution  # noqa: E402
from revision import KIND_TASK_ADDED  # noqa: E402

import w_scenario  # noqa: E402


# 구현 task dict 필수 키 11종(w_scenario 구성 규칙과 정합).
REQUIRED_TASK_KEYS = (
    "id", "task", "done", "interfaceContract", "ownedBoundary", "dependsOn",
    "delegation", "capability", "role", "model", "unitType",
)

# 보호 경계 — 어느 구현 task 의 ownedBoundary 에도 나타나면 안 되는 UAHF Scaffold·Contract 영역.
PROTECTED_PREFIXES = (".claude/", "specs/", "framework/")
PROTECTED_EXACT = (".claude", "specs", "framework", "install-manifest.md")

MIN_TASKS = 1
MAX_TASKS = 6


def _norm(item: str) -> str:
    """경로 정규화 — 역슬래시를 슬래시로, 앞뒤 공백·후행 슬래시 제거."""
    return item.replace("\\", "/").strip().rstrip("/")


def _relpath_errors(item, where: str) -> list:
    """ownedBoundary 항목의 상대경로 위반(비문자열·절대경로·`..`)을 열거한다."""
    if not isinstance(item, str) or item.strip() == "":
        return ["%s ownedBoundary 항목이 비어 있지 않은 문자열이어야 한다: %r" % (where, item)]
    errs = []
    norm = item.replace("\\", "/")
    if os.path.isabs(item) or norm.startswith("/") or (len(item) >= 2 and item[1] == ":"):
        errs.append("%s ownedBoundary 항목이 절대경로다(상대경로여야 함): %r" % (where, item))
    if ".." in norm.split("/"):
        errs.append("%s ownedBoundary 항목에 '..' 가 있다(경계 이탈 금지): %r" % (where, item))
    return errs


def _protected_errors(item, where: str) -> list:
    """ownedBoundary 항목이 보호 경계(.claude/·install-manifest.md·specs/·framework/)를
    침범하는지 검사한다(침범 시 거부)."""
    if not isinstance(item, str) or item.strip() == "":
        return []  # 비문자열/빈 항목은 _relpath_errors 가 이미 표기.
    norm = _norm(item)
    if norm in PROTECTED_EXACT or any(norm.startswith(p) for p in PROTECTED_PREFIXES):
        return [
            "%s ownedBoundary 항목이 보호 경계(.claude/·install-manifest.md·specs/·framework/)를 "
            "침범한다(UAHF Scaffold·Contract 무수정): %r" % (where, item)
        ]
    return []


def _overlaps(a: str, b: str) -> bool:
    """정규화된 두 경로가 겹치는가 — 동일하거나 한쪽이 다른쪽의 조상 디렉터리이면 True."""
    if a == b:
        return True
    return a.startswith(b + "/") or b.startswith(a + "/")


def _cycle_error(tasks) -> list:
    """dependsOn 그래프(task → dependsOn)에 사이클이 있으면 오류를 반환한다(DFS 색칠)."""
    graph = {}
    for t in tasks:
        tid = t.get("id")
        dep = t.get("dependsOn")
        if isinstance(tid, str) and tid.strip():
            graph[tid] = [d for d in (dep if isinstance(dep, list) else []) if isinstance(d, str)]

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}

    def visit(node) -> bool:
        color[node] = GRAY
        for nxt in graph.get(node, ()):
            if nxt not in color:
                continue  # 미존재 참조는 dependsOn 무결성에서 별도 표기.
            if color[nxt] == GRAY:
                return True
            if color[nxt] == WHITE and visit(nxt):
                return True
        color[node] = BLACK
        return False

    for node in graph:
        if color[node] == WHITE and visit(node):
            return ["dependsOn 그래프에 사이클이 있다(DAG 위반): 시작 노드 %r 부근" % (node,)]
    return []


def validate_impl_plan(plan) -> list:
    """impl-plan(구현 계획)의 구조 검증 — 오류 목록을 반환한다(빈 목록 = 통과).

    순수 함수(plan 만으로 결정·run 데이터 무접촉). 임의 payload 단위 검사에도 쓰인다
    (가짜 샘플 JSON 으로 CP1 단위 점검). 자동 수정 0·정직 실패.

    검사:
      - 최상위 dict · tasks 가 1~6개 리스트.
      - 각 task: 11키 전부 존재 · unitType == 'implementation'.
      - id 가 비어있지 않은 문자열 · task 간 유일(중복 0).
      - dependsOn 이 리스트 · 참조가 **계획 내 task id 만** · 자기참조 금지 · 사이클 금지(DAG).
      - ownedBoundary 가 비어있지 않은 리스트 · 각 항목 상대경로(절대경로·'..' 금지).
      - ownedBoundary 항목이 보호 경계(.claude/·install-manifest.md·specs/·framework/) 미침범.
      - ownedBoundary 항목이 task 간 상호 비중첩(동일·조상/자손 관계 금지).
      - done 이 비어있지 않은 문자열(비공백).
    """
    if not isinstance(plan, dict):
        return ["impl-plan 최상위가 단일 객체(dict)가 아니다: %s" % type(plan).__name__]

    tasks = plan.get("tasks")
    if not isinstance(tasks, list):
        return ["tasks 가 리스트가 아니다: %r" % (tasks,)]
    if not (MIN_TASKS <= len(tasks) <= MAX_TASKS):
        return ["tasks 개수가 %d~%d개 범위를 벗어난다: %d 개"
                % (MIN_TASKS, MAX_TASKS, len(tasks))]

    errors: list = []
    id_list: list = []            # 등장 순서대로 id 수집(dependsOn 참조 무결성 기준).
    seen_ids: set = set()
    # (task_index, [정규화된 ownedBoundary 항목]) — 상호 비중첩 검사용.
    ob_by_task: list = []

    # 1차 스윕: id 수집(참조 무결성 기준 집합 확정).
    for t in tasks:
        if isinstance(t, dict):
            tid = t.get("id")
            if isinstance(tid, str) and tid.strip():
                id_list.append(tid)
    id_set = set(id_list)

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

        # unitType.
        if t.get("unitType") != "implementation":
            errors.append("%s unitType 이 'implementation' 이 아니다: %r" % (where, t.get("unitType")))

        # id 유일성.
        tid = t.get("id")
        if not isinstance(tid, str) or not tid.strip():
            errors.append("%s id 가 비어 있지 않은 문자열이어야 한다: %r" % (where, tid))
        elif tid in seen_ids:
            errors.append("%s id 중복: %r" % (where, tid))
        else:
            seen_ids.add(tid)

        # dependsOn 참조 무결성(계획 내 id 만·자기참조 금지).
        dep = t.get("dependsOn")
        if not isinstance(dep, list):
            errors.append("%s dependsOn 이 리스트가 아니다: %r" % (where, dep))
        else:
            for d in dep:
                if d == tid:
                    errors.append("%s dependsOn 에 자기 자신이 포함됨(자기참조 금지): %r" % (where, tid))
                elif d not in id_set:
                    errors.append(
                        "%s dependsOn 참조가 계획 내 task id 가 아니다: %r" % (where, d)
                    )

        # ownedBoundary 상대경로·보호 경계.
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

    # ownedBoundary 상호 비중첩(task 쌍 × 항목 쌍).
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

    # 사이클(DAG) 검사.
    errors.extend(_cycle_error(tasks))

    return errors


PROVENANCE_NOTE = (
    "주 세션 게이트 제시에 대한 실 사용자 응답 — 시뮬레이션 아님. L-07 의 반대 방향 정직성: "
    "실 사용자를 시뮬레이션으로 오표기하지 않는다. actor=human 은 실제 사용자 개입이며, "
    "user_response 는 그 응답 원문이다."
)

_PHASE_NOTE = {
    "structure": (
        "구조 승인 게이트(impl-plan 뒤 user_decision) — 실 사용자 승인. 해소 후 impl-plan 의 구현 "
        "task 전체(3~6개)를 task_added revision 으로 일괄 append(동적 그래프 성장). 구현 단계 "
        "게이트는 review_required(비정지)이므로 이후 사용자 게이트는 없다."
    ),
}


class _NoInvoke:
    def invoke(self, request):
        raise RuntimeError("resolve_w 는 실행하지 않는다(게이트 해소·revision append 전용)")


def _recover_user_gate(run_dir: Path) -> str:
    """stop-signal.json 에서 정지한 user_decision 게이트 gate_id 를 회수한다(추측 0)."""
    stop = load_json(run_dir / "logs" / "stop-signal.json")
    pending = stop.get("pending_gates") or []
    user_gates = [g for g in pending if g.get("gateKind") == GATE_USER_DECISION_REQUIRED]
    if not user_gates:
        print("[ERR] 정지 신호에 user_decision 게이트가 없다 — 재개 불가.", file=sys.stderr)
        print("      pending=%s" % json.dumps(pending, ensure_ascii=False), file=sys.stderr)
        return ""
    return user_gates[0]["gate_id"]


def _append_resolution(run_dir: Path, gate_id: str, user_response: str, phase: str) -> None:
    """실 사용자 게이트 해소 — provenance annotation + 해소 이벤트 + 정직 기록 파일(simulated=false)."""
    log = EventLog(JsonlEventStore(str(run_dir / "events.jsonl")))

    # (1) 실 사용자 응답 provenance annotation append(simulated=false·actor=human).
    log.append(
        cycle_id="annotation::provenance-" + str(gate_id),
        from_stage=None,
        to_stage="note",
        trigger="사용자 응답 provenance",
        outcome="pass",
        actor="human",
        ref={
            "kind": "user-resolution-provenance",
            "gate_id": gate_id,
            "phase": phase,
            "simulated": False,
            "user_response": user_response,
            "note": PROVENANCE_NOTE,
        },
    )

    # (2) 사용자 actor 해소 이벤트 append(적격성 = userActorClass=human).
    append_gate_resolution(log, gate_id, GATE_USER_DECISION_REQUIRED, actor="human")

    # (3) 정직 기록 파일(phase 별·simulated=false).
    record = {
        "gate_id": gate_id,
        "gateKind": GATE_USER_DECISION_REQUIRED,
        "phase": phase,
        "resolved_by_actor": "human",
        "simulated": False,
        "user_response": user_response,
        "note": _PHASE_NOTE.get(phase, ""),
        "impl_plan_source": (
            "실 LLM 제안 step impl-plan 산출 artifact(impl-plan.json) — 드라이버 픽스처 아님"
            "(OQ-PO-B4 완전 해소). 구현 task 전체가 이 산출에서 검증·승격된다."
        ),
    }
    with open(
        run_dir / "logs" / ("gate-resolution-record-%s.json" % phase), "w", encoding="utf-8"
    ) as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)


def _resolve_structure(run_dir: Path, gate_id: str, user_response: str) -> int:
    """구조 게이트 해소 + impl-plan 검증 + 구현 task 전체 task_added revision 일괄 append."""
    # 검증 우선(무근거 게이트 해소 회피) — orchestrator 조립(no-op invoker).
    orch, cfg = build_orchestrator_k(run_dir, _NoInvoke())
    workspace = cfg.get("workspace_dir") or str(run_dir / "workspace")
    plan_path = Path(workspace) / w_scenario.IMPL_PLAN_FILE
    if not plan_path.exists():
        print("[ERR] impl-plan 부재 — 검증 불가: %s" % plan_path, file=sys.stderr)
        print("      (impl-plan step 이 아직 산출하지 않았거나 경로 불일치.)", file=sys.stderr)
        return 1
    plan = load_json(plan_path)

    errors = validate_impl_plan(plan)
    if errors:
        print("[REJECT] impl-plan 검증 실패 — 자동 수정하지 않는다(정직 실패):", file=sys.stderr)
        for e in errors:
            print("  - %s" % e, file=sys.stderr)
        print("      (게이트 미해소·원장 무오염 — 이벤트 0 append.)", file=sys.stderr)
        return 1

    # 검증 통과 → 실 사용자 구조 게이트 해소(provenance + 해소 이벤트 + 기록).
    _append_resolution(run_dir, gate_id, user_response, "structure")

    # 구현 task 전체를 task_added revision 일괄 append.
    accepted = []
    for st in plan["tasks"]:
        try:
            revision = orch.accept_revision(
                KIND_TASK_ADDED, st, proposingStepRef="impl-plan", gateEventRef=gate_id
            )
        except Exception as exc:  # noqa: BLE001  (구조 misuse·근거 미실재 등 정직 표면화)
            print(
                "[REJECT] task_added revision 수용 실패(자동 수정 0·정직 실패): id=%r"
                % (st.get("id"),),
                file=sys.stderr,
            )
            print("  - %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
            return 1
        accepted.append((revision.revisionSeq, st.get("id"), st.get("unitType")))

    print("[RESOLVE] gate_id=%s resolved by actor=human (실 사용자·simulated=false)." % gate_id)
    print("[VALIDATE] impl-plan 검증 통과(11키·unitType·id 유일·dependsOn DAG·상대경로·보호 경계·"
          "비중첩·done 비공백).")
    print("[REVISION] task_added %d 건 일괄 append (basis.proposingStepRef=impl-plan gateEventRef=%s):"
          % (len(accepted), gate_id))
    for seq, sid, ut in accepted:
        print("  - seq=%s id=%s unitType=%s" % (seq, sid, ut))
    print("[NOTE] 동적 그래프 성장 — 실 사용자 응답 = logs/gate-resolution-record-structure.json + "
          "user-resolution-provenance 이벤트(append-only 로그). 구현 게이트는 review_required"
          "(비정지)이므로 이후 사용자 게이트는 없다.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="시나리오 (w) 실 사용자 구조 게이트 해소 + impl-plan 검증·구현 task 일괄 편입"
    )
    parser.add_argument("run_dir", help="run 데이터 백엔드 디렉터리")
    parser.add_argument(
        "--phase", required=True, choices=("structure",),
        help="structure=구조 게이트(impl-plan 뒤·impl-plan 검증·구현 task revision 일괄). "
             "구현 게이트는 review_required(비정지)이므로 final phase 는 없다.",
    )
    parser.add_argument(
        "--user-response", required=True,
        help="실 사용자 응답 원문(필수 — 무인 해소 금지). 시뮬레이션 아님.",
    )
    args = parser.parse_args()

    if not args.user_response or not args.user_response.strip():
        print("[ERR] --user-response 는 비어 있을 수 없다(무인 해소 금지).", file=sys.stderr)
        return 2
    run_dir = Path(args.run_dir).resolve()

    gate_id = _recover_user_gate(run_dir)
    if not gate_id:
        return 1

    return _resolve_structure(run_dir, gate_id, args.user_response)


if __name__ == "__main__":
    sys.exit(main())
