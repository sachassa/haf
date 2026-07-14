"""시나리오 (m) — **실 사용자** 게이트 해소 + stage-plan 검증·동적 그래프 성장(2위상).

사용법:
  python resolve_m.py <run-dir> --phase structure --user-response "<실 사용자 응답 원문>"
  python resolve_m.py <run-dir> --phase final     --user-response "<실 사용자 응답 원문>"

resolve_k.py(k)와의 결정적 차이 = **2단 게이트 + 동적 그래프 일괄 성장**. (k)는 단일
user_decision 게이트를 해소하고 실 LLM 제안 1건을 검증·승격했다. (m)은:
  --phase structure: assess 산출 stage-plan.json 을 validate_stage_plan 으로 검증(오류 열거·
     자동 수정 0·정직 실패)한 뒤, **잔여 단계 전체**(propose×N·reconcile·review)를 task_added
     revision 으로 **일괄 append**한다(각 basis = proposingStepRef "assess" + gateEventRef=
     구조 게이트 · PO-INV 5). 판정이 'skip' 이면 revision **0건**(게이트 해소만·04 T2→T9).
  --phase final: T8 Validating 게이트 해소만(revision 0). 발행(v2 생성)은 Advisor 소관.

정직성(L-07 양방향):
  - 실 사용자를 시뮬레이션으로 오표기하지 않는다(simulated=false·actor=human·user_response 원문).
  - stage-plan 검증 실패는 자동 수정하지 않고 오류를 열거해 비0 종료한다(정직 실패).

검증 우선(무근거 게이트 해소 회피):
  --phase structure 는 **stage-plan 검증을 게이트 해소보다 먼저** 수행한다. 검증 실패 시 어떤
  이벤트도 append 하지 않고(게이트 미해소·원장 무오염) 비0 종료한다. (k)는 해소 후 검증했으나,
  (m)은 무효 입력에 게이트를 조기 해소하지 않도록 순서를 조정했다(정직성 강화·자동 수정 0).

이 스크립트는 orchestration-data/e2e/ 경계 소속이다(비프로덕션 드라이버).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# k_common import 가 중립 코드 경로를 sys.path 에 배선한다(먼저 실행되어야 함·무수정 재사용).
from k_common import build_orchestrator_k, load_json

# 중립 코드 심볼(무수정 라이브러리).
from events import EventLog, JsonlEventStore  # noqa: E402
from gates import GATE_USER_DECISION_REQUIRED, append_gate_resolution  # noqa: E402
from revision import KIND_TASK_ADDED  # noqa: E402

import m_scenario  # noqa: E402


# stage Task dict 필수 키 11종(m_scenario 구성 규칙과 정합).
REQUIRED_STAGE_KEYS = (
    "id", "task", "done", "interfaceContract", "ownedBoundary", "dependsOn",
    "delegation", "capability", "role", "model", "unitType",
)

VALID_STAGE_UNIT_TYPES = ("sd_propose", "sd_reconcile", "sd_review")


def _relpath_errors(item) -> list:
    """ownedBoundary 항목의 상대경로 위반(절대경로·`..`·비문자열)을 열거한다."""
    if not isinstance(item, str) or item.strip() == "":
        return ["ownedBoundary 항목이 비어 있지 않은 문자열이어야 한다: %r" % (item,)]
    errs = []
    norm = item.replace("\\", "/")
    if os.path.isabs(item) or norm.startswith("/") or (len(item) >= 2 and item[1] == ":"):
        errs.append("ownedBoundary 항목이 절대경로다(상대경로여야 함): %r" % (item,))
    if ".." in norm.split("/"):
        errs.append("ownedBoundary 항목에 '..' 가 있다(경계 이탈 금지): %r" % (item,))
    return errs


def validate_stage_plan(plan) -> list:
    """assess 산출 stage-plan 의 구조 검증 — 오류 목록을 반환한다(빈 목록 = 통과).

    순수 함수(plan 만으로 결정·run 데이터 무접촉). 임의 payload 단위 검사에도 쓰인다
    (가짜 샘플 JSON 으로 CP1 단위 점검). 자동 수정 0.

    검사(maturation=='needed' 경로):
      - 최상위 dict · maturation ∈ {needed, skip}.
      - stages 가 비어 있지 않은 리스트.
      - 각 stage: 11키 전부 존재.
      - unitType ∈ {sd_propose, sd_reconcile, sd_review}.
      - id 가 'assess' 와 충돌하지 않고 stage 간 중복 0.
      - dependsOn 이 리스트이며 참조가 'assess' 또는 **선행 stage id** 만(무결).
      - ownedBoundary 가 비어 있지 않고 각 항목이 상대경로(절대경로·'..' 금지).
      - done 이 'python -c' 를 포함하는 문자열.
      - propose ≥ 1 · reconcile 정확히 1 · review 정확히 1.
      - reconcile.dependsOn = 전체 propose id 집합(정확 일치).
      - review.dependsOn = ["reconcile"].
    검사(maturation=='skip' 경로):
      - stages 가 비어 있어야 한다(성숙 단계 무산출 — 비어있지 않으면 불일치 오류).
    """
    if not isinstance(plan, dict):
        return ["stage-plan 최상위가 단일 객체(dict)가 아니다: %s" % type(plan).__name__]

    errors: list = []
    maturation = plan.get("maturation")
    if maturation not in ("needed", "skip"):
        errors.append("maturation 은 'needed'|'skip' 이어야 한다: %r" % (maturation,))

    if maturation == "skip":
        stages = plan.get("stages")
        if stages:  # 비어있지 않은 stages 는 스킵과 불일치(무산출 원칙).
            errors.append(
                "maturation=skip 인데 stages 가 비어있지 않다(스킵은 무산출): 길이 %d"
                % (len(stages) if isinstance(stages, (list, tuple)) else -1,)
            )
        return errors

    if maturation != "needed":
        # 알 수 없는 maturation 은 위에서 이미 오류로 표기됨 — stages 검증 생략.
        return errors

    # --- maturation == 'needed' 경로 -------------------------------------
    stages = plan.get("stages")
    if not isinstance(stages, list) or len(stages) == 0:
        errors.append("maturation=needed 인데 stages 가 비어있지 않은 리스트가 아니다: %r" % (stages,))
        return errors

    known_ids = {"assess"}          # dependsOn 참조 무결성 기준(assess + 선행 stage id).
    seen_ids: set = set()
    propose_ids: list = []
    reconcile_ids: list = []
    review_ids: list = []
    reconcile_stage = None
    review_stage = None

    for i, st in enumerate(stages):
        if not isinstance(st, dict):
            errors.append("stages[%d] 가 객체(dict)가 아니다: %s" % (i, type(st).__name__))
            continue

        for k in REQUIRED_STAGE_KEYS:
            if k not in st:
                errors.append("stages[%d] 필수 키 누락: %r" % (i, k))

        sid = st.get("id")
        ut = st.get("unitType")

        # id 유일성 + 'assess' 비충돌.
        if sid == "assess":
            errors.append("stages[%d] id 가 'assess'(초기 단위)와 충돌한다: %r" % (i, sid))
        elif sid in seen_ids:
            errors.append("stages[%d] id 중복: %r" % (i, sid))
        elif isinstance(sid, str) and sid.strip():
            seen_ids.add(sid)
        else:
            errors.append("stages[%d] id 가 비어 있지 않은 문자열이어야 한다: %r" % (i, sid))

        # unitType.
        if ut not in VALID_STAGE_UNIT_TYPES:
            errors.append(
                "stages[%d] unitType 이 sd_propose|sd_reconcile|sd_review 가 아니다: %r" % (i, ut)
            )

        # dependsOn 참조 무결성(assess 또는 선행 stage id 만).
        dep = st.get("dependsOn")
        if not isinstance(dep, list):
            errors.append("stages[%d] dependsOn 이 리스트가 아니다: %r" % (i, dep))
        else:
            for d in dep:
                if d not in known_ids:
                    errors.append(
                        "stages[%d] dependsOn 참조 무결성 위반(assess 또는 선행 stage id 만): %r"
                        % (i, d)
                    )

        # ownedBoundary 상대경로.
        ob = st.get("ownedBoundary")
        if not isinstance(ob, list) or len(ob) == 0:
            errors.append("stages[%d] ownedBoundary 가 비어 있지 않은 리스트가 아니다: %r" % (i, ob))
        else:
            for item in ob:
                errors.extend("stages[%d] %s" % (i, e) for e in _relpath_errors(item))

        # done 이 'python -c' 포함 문자열.
        done = st.get("done")
        if not isinstance(done, str) or "python -c" not in done:
            errors.append("stages[%d] done 이 'python -c' 를 포함하는 문자열이 아니다: %r" % (i, done))

        # 유형별 버킷.
        if ut == "sd_propose":
            propose_ids.append(sid)
        elif ut == "sd_reconcile":
            reconcile_ids.append(sid)
            reconcile_stage = st
        elif ut == "sd_review":
            review_ids.append(sid)
            review_stage = st

        # 후행 stage 의 dependsOn 참조를 위해 이 id 를 알려진 id 로 등록(선행 = 배열 앞선 원소).
        if isinstance(sid, str) and sid.strip() and sid != "assess":
            known_ids.add(sid)

    # 개수 제약.
    if len(propose_ids) < 1:
        errors.append("propose 단계가 최소 1개여야 한다: %d 개" % len(propose_ids))
    if len(reconcile_ids) != 1:
        errors.append("reconcile 단계가 정확히 1개여야 한다: %d 개" % len(reconcile_ids))
    if len(review_ids) != 1:
        errors.append("review 단계가 정확히 1개여야 한다: %d 개" % len(review_ids))

    # reconcile.dependsOn = 전체 propose id 집합(정확 일치).
    if reconcile_stage is not None:
        rec_dep = reconcile_stage.get("dependsOn")
        if (
            not isinstance(rec_dep, list)
            or set(rec_dep) != set(propose_ids)
            or len(rec_dep) != len(set(propose_ids))
        ):
            errors.append(
                "reconcile.dependsOn 이 전체 propose id 집합과 일치해야 한다: dep=%r propose=%r"
                % (rec_dep, propose_ids)
            )

    # review.dependsOn = ["reconcile"].
    if review_stage is not None:
        rev_dep = review_stage.get("dependsOn")
        if rev_dep != ["reconcile"]:
            errors.append("review.dependsOn 이 ['reconcile'] 이어야 한다: %r" % (rev_dep,))

    return errors


PROVENANCE_NOTE = (
    "주 세션 게이트 제시에 대한 실 사용자 응답 — 시뮬레이션 아님. L-07 의 반대 방향 정직성: "
    "실 사용자를 시뮬레이션으로 오표기하지 않는다. actor=human 은 실제 사용자 개입이며, "
    "user_response 는 그 응답 원문이다."
)

_PHASE_NOTE = {
    "structure": (
        "구조 승인 게이트(assess 뒤 user_decision) — 실 사용자 승인. 해소 후 stage-plan 잔여 단계"
        "(propose×N·reconcile·review)를 task_added revision 으로 일괄 append(동적 그래프 성장). "
        "판정이 'skip' 이면 revision 0건(04 T2→T9)."
    ),
    "final": (
        "T8 Validating — 실 사용자 승인(04 §3.4 T8·05 §3.7). 게이트 해소만(revision 0). "
        "성숙 산출(v2 발행)은 T8 승인 후 Advisor 소관."
    ),
}


def _archive_stop_signal(run_dir: Path, phase: str) -> None:
    """해소 시점의 stop-signal.json 을 위상별로 mtime 보존 복사한다(T1 텔레메트리·순수 부가).

    러너(run_*.py)는 다음 게이트 정지 시 stop-signal.json 을 **덮어써** 선행 게이트의 정지
    시각(mtime)을 소실시킨다 — (m)은 구조/T8 2단 게이트라 구조 게이트 정지 시각이 실제로
    소실됐다(1차 §T1 (a) 실측). 해소 직전에 위상별(structure/final)로 mtime 보존 복사
    (shutil.copy2)해 두면 이후 게이트가 라이브 파일을 덮어써도 선행 게이트 정지 시각이
    보존된다. **신규 run 에만 효력**(과거 Baseline run 은 무소급). 기존 아카이브는 덮어쓰지
    않는다(idempotent·정직 보존). record 명명(gate-resolution-record-<phase>.json)과 대칭.
    """
    src = run_dir / "logs" / "stop-signal.json"
    if not src.exists():
        return  # 정지 신호 부재 — 아카이브할 것 없음.
    dst = run_dir / "logs" / ("stop-signal-%s.json" % phase)
    if dst.exists():
        return  # 기존 아카이브 보존(덮어쓰기 금지).
    shutil.copy2(src, dst)  # copy2 = mtime(=게이트 정지 시각) 보존.


class _NoInvoke:
    def invoke(self, request):
        raise RuntimeError("resolve_m 는 실행하지 않는다(게이트 해소·revision append 전용)")


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
    # 해소 시점 위상 아카이브(T1) — 라이브 stop-signal 덮어쓰기 전 정지 시각 보존.
    _archive_stop_signal(run_dir, phase)

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
    }
    with open(
        run_dir / "logs" / ("gate-resolution-record-%s.json" % phase), "w", encoding="utf-8"
    ) as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)


def _resolve_structure(run_dir: Path, gate_id: str, user_response: str) -> int:
    """구조 게이트 해소 + stage-plan 검증 + 잔여 단계 task_added revision 일괄 append."""
    # 검증 우선(무근거 게이트 해소 회피) — orchestrator 조립(no-op invoker).
    orch, cfg = build_orchestrator_k(run_dir, _NoInvoke())
    workspace = cfg.get("workspace_dir") or str(run_dir / "workspace")
    plan_path = Path(workspace) / m_scenario.STAGE_PLAN_FILE
    if not plan_path.exists():
        print("[ERR] stage-plan 부재 — 검증 불가: %s" % plan_path, file=sys.stderr)
        print("      (assess step 이 아직 산출하지 않았거나 경로 불일치.)", file=sys.stderr)
        return 1
    plan = load_json(plan_path)

    errors = validate_stage_plan(plan)
    if errors:
        print("[REJECT] stage-plan 검증 실패 — 자동 수정하지 않는다(정직 실패):", file=sys.stderr)
        for e in errors:
            print("  - %s" % e, file=sys.stderr)
        print("      (게이트 미해소·원장 무오염 — 이벤트 0 append.)", file=sys.stderr)
        return 1

    maturation = plan.get("maturation")

    # 검증 통과 → 실 사용자 구조 게이트 해소(provenance + 해소 이벤트 + 기록).
    _append_resolution(run_dir, gate_id, user_response, "structure")

    if maturation == "skip":
        print("[RESOLVE] gate_id=%s resolved by actor=human (실 사용자·simulated=false)." % gate_id)
        print("[SKIP] maturation=skip — 잔여 단계 없음. revision 0건(04 T2→T9 경량 확인 경로).")
        print("[NOTE] v1 이 그대로 소비 대상. 스킵 판정 기록은 assessing-judgment.md 에 존재.")
        return 0

    # maturation == needed → stages 순서대로 task_added revision 일괄 append.
    accepted = []
    for st in plan["stages"]:
        try:
            revision = orch.accept_revision(
                KIND_TASK_ADDED, st, proposingStepRef="assess", gateEventRef=gate_id
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
    print("[VALIDATE] stage-plan 검증 통과(11키·unitType·dependsOn 무결·개수·reconcile/review 사슬).")
    print("[REVISION] task_added %d 건 일괄 append (basis.proposingStepRef=assess gateEventRef=%s):"
          % (len(accepted), gate_id))
    for seq, sid, ut in accepted:
        print("  - seq=%s id=%s unitType=%s" % (seq, sid, ut))
    print("[NOTE] 동적 그래프 성장 — 실 사용자 응답 = logs/gate-resolution-record-structure.json + "
          "user-resolution-provenance 이벤트(append-only 로그).")
    return 0


def _resolve_final(run_dir: Path, gate_id: str, user_response: str) -> int:
    """T8 Validating 게이트 해소만(revision 0)."""
    _append_resolution(run_dir, gate_id, user_response, "final")
    print("[RESOLVE] gate_id=%s resolved by actor=human (실 사용자·simulated=false)." % gate_id)
    print("[FINAL] T8 Validating — 실 사용자 승인. revision 0건(게이트 해소만).")
    print("[NOTE] 성숙 산출(v2 발행)은 T8 승인 후 Advisor 소관(위임 제약). 기록 = "
          "logs/gate-resolution-record-final.json.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="시나리오 (m) 실 사용자 게이트 해소 + stage-plan 검증·동적 그래프 성장"
    )
    parser.add_argument("run_dir", help="run 데이터 백엔드 디렉터리")
    parser.add_argument(
        "--phase", required=True, choices=("structure", "final"),
        help="structure=구조 게이트(assess 뒤·stage-plan 검증·revision 일괄) / final=T8 게이트(해소만)",
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

    if args.phase == "structure":
        return _resolve_structure(run_dir, gate_id, args.user_response)
    return _resolve_final(run_dir, gate_id, args.user_response)


if __name__ == "__main__":
    sys.exit(main())
