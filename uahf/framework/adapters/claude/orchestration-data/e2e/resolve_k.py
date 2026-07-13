"""시나리오 (k) — **실 사용자** 게이트 해소 + 실 LLM 제안 artifact 검증·revision append.

사용법:
  python resolve_k.py <run-dir> --user-response "<실 사용자 응답 원문>"

resolve_and_revise.py(j)와의 결정적 차이 = **시뮬레이션이 아니다**. (j)는 사용자 해소를
드라이버가 시뮬레이션(simulated=true)했고 구현 제안을 드라이버 픽스처로 append 했다. (k)는:
  - 사용자 게이트를 **실 사용자**가 해소한다(simulated=false·user_response 원문 기록).
    L-07 의 반대 방향 정직성: 실 사용자를 시뮬레이션으로 오표기하는 것도 금지한다.
  - 구현 제안을 드라이버 픽스처가 아니라 **그래프 내 실 LLM 제안 step(p1)의 산출 artifact**
    (외부 워크스페이스의 impl-proposal.json)에서 읽어 검증 후 승격한다(OQ-PO-B4 해소 스모크).

동작(정지와 재개 사이):
  1. stop-signal.json 에서 정지한 user_decision 게이트 gate_id 를 읽는다(러너가 실제로 올린
     게이트 그대로 — 추측 0).
  2. `--user-response`(실 사용자 응답 원문) 필수 — 없으면 에러 종료(무인 해소 금지).
     append-only 로그에 provenance annotation 이벤트를 append(simulated=false·actor=human).
  3. 사용자 actor 해소 이벤트 append(적격성 = userActorClass=human).
  4. logs/gate-resolution-record.json 기록(simulated=false·실 사용자·실 LLM 제안 출처 명시).
  5. p1 산출 artifact(impl-proposal.json)를 검증(validate_proposal) — 위반 시 **정직 실패**
     (오류 열거 후 비0 종료·자동 수정 0).
  6. 통과 시 task_added revision append(basis = proposingStepRef **p1** + gateEventRef).
     accept_revision 이 게이트 통과 이벤트 실재를 검증한 뒤에만 수용한다(PO-INV 5).

이 스크립트는 orchestration-data/e2e/ 경계 소속이다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# k_common import 가 중립 코드 경로를 sys.path 에 배선한다(먼저 실행되어야 함).
from k_common import build_orchestrator_k, load_json

# 중립 코드 심볼(무수정 라이브러리).
from events import EventLog, JsonlEventStore  # noqa: E402
from gates import GATE_USER_DECISION_REQUIRED, append_gate_resolution  # noqa: E402
from revision import KIND_TASK_ADDED  # noqa: E402

import k_scenario  # noqa: E402


# task_added payload 필수 키 11종(k_scenario.proposal_task 계약과 정합).
REQUIRED_KEYS = (
    "id", "task", "done", "interfaceContract", "ownedBoundary", "dependsOn",
    "delegation", "capability", "role", "model", "unitType",
)


def _relpath_errors(item) -> list:
    """ownedBoundary 항목의 상대경로 위반(절대경로·`..`)을 열거한다."""
    if not isinstance(item, str) or item.strip() == "":
        return ["ownedBoundary 항목이 비어 있지 않은 문자열이어야 한다: %r" % (item,)]
    errs = []
    norm = item.replace("\\", "/")
    if os.path.isabs(item) or norm.startswith("/") or (len(item) >= 2 and item[1] == ":"):
        errs.append("ownedBoundary 항목이 절대경로다(상대경로여야 함): %r" % (item,))
    if ".." in norm.split("/"):
        errs.append("ownedBoundary 항목에 '..' 가 있다(경계 이탈 금지): %r" % (item,))
    return errs


def validate_proposal(payload) -> list:
    """실 LLM 제안 payload 의 구조 검증 — 오류 목록을 반환한다(빈 목록 = 통과).

    검사(자동 수정 0·정직 실패):
      - 최상위가 단일 객체(dict).
      - 필수 키 11종 존재.
      - id == 'impl' · dependsOn == ['d1'] · unitType == 'implementation'.
      - ownedBoundary 가 비어 있지 않고 각 항목이 상대경로(절대경로·'..' 금지).
      - done 이 'python -c' 를 포함하는 문자열.
    순수 함수(payload 만으로 결정). 이 함수는 run 데이터가 아니라 임의 payload 에 대한
    단위 검사에도 쓰인다(가짜 샘플 JSON 으로 CP1 단위 점검).
    """
    if not isinstance(payload, dict):
        return ["제안 payload 최상위가 단일 객체(dict)가 아니다: %s" % type(payload).__name__]

    errors = []
    for key in REQUIRED_KEYS:
        if key not in payload:
            errors.append("필수 키 누락: %r" % (key,))

    if "id" in payload and payload["id"] != "impl":
        errors.append("id 는 정확히 'impl' 이어야 한다: %r" % (payload["id"],))
    if "dependsOn" in payload and payload["dependsOn"] != ["d1"]:
        errors.append("dependsOn 은 정확히 ['d1'] 이어야 한다: %r" % (payload["dependsOn"],))
    if "unitType" in payload and payload["unitType"] != "implementation":
        errors.append("unitType 은 'implementation' 이어야 한다: %r" % (payload["unitType"],))

    if "ownedBoundary" in payload:
        ob = payload["ownedBoundary"]
        if not isinstance(ob, list) or len(ob) == 0:
            errors.append("ownedBoundary 는 비어 있지 않은 리스트여야 한다: %r" % (ob,))
        else:
            for item in ob:
                errors.extend(_relpath_errors(item))

    if "done" in payload:
        done = payload["done"]
        if not isinstance(done, str) or "python -c" not in done:
            errors.append("done 은 'python -c' 를 포함하는 문자열이어야 한다: %r" % (done,))

    return errors


PROVENANCE_NOTE = (
    "주 세션 게이트 제시에 대한 실 사용자 응답 — 시뮬레이션 아님. L-07 의 반대 방향 "
    "정직성: 실 사용자를 시뮬레이션으로 오표기하지 않는다. actor=human 은 실제 사용자 "
    "개입이며, user_response 는 그 응답 원문이다."
)

IMPL_PROPOSAL_SOURCE = (
    "실 LLM 제안 step p1 산출 artifact(impl-proposal.json) — 드라이버 픽스처 아님"
    "(OQ-PO-B4 해소 스모크). resolve_and_revise.py(j)의 j_scenario.impl_revision_payload "
    "하드코딩을 그래프 내 실 LLM 산출로 대체한 지점이다."
)


class _NoInvoke:
    def invoke(self, request):
        raise RuntimeError("resolve_k 는 실행하지 않는다(revision append 전용)")


def main() -> int:
    parser = argparse.ArgumentParser(description="시나리오 (k) 실 사용자 게이트 해소 + revision append")
    parser.add_argument("run_dir", help="run 데이터 백엔드 디렉터리")
    parser.add_argument(
        "--user-response", required=True,
        help="실 사용자 응답 원문(필수 — 무인 해소 금지). 시뮬레이션 아님.",
    )
    args = parser.parse_args()

    user_response = args.user_response
    if not user_response or not user_response.strip():
        print("[ERR] --user-response 는 비어 있을 수 없다(무인 해소 금지).", file=sys.stderr)
        return 2
    run_dir = Path(args.run_dir).resolve()

    # (1) 정지 게이트 gate_id 회수(추측 0).
    stop = load_json(run_dir / "logs" / "stop-signal.json")
    pending = stop.get("pending_gates") or []
    user_gates = [g for g in pending if g.get("gateKind") == GATE_USER_DECISION_REQUIRED]
    if not user_gates:
        print("[ERR] 정지 신호에 user_decision 게이트가 없다 — 재개 불가.", file=sys.stderr)
        print("      pending=%s" % json.dumps(pending, ensure_ascii=False), file=sys.stderr)
        return 1
    gate_id = user_gates[0]["gate_id"]

    log = EventLog(JsonlEventStore(str(run_dir / "events.jsonl")))

    # (2) 실 사용자 응답 provenance annotation append(simulated=false·actor=human).
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
            "simulated": False,
            "user_response": user_response,
            "note": PROVENANCE_NOTE,
        },
    )

    # (3) 사용자 actor 해소 이벤트 append(적격성 = userActorClass=human).
    append_gate_resolution(log, gate_id, GATE_USER_DECISION_REQUIRED, actor="human")

    # (4) 정직 기록 파일(simulated=false).
    record = {
        "gate_id": gate_id,
        "gateKind": GATE_USER_DECISION_REQUIRED,
        "resolved_by_actor": "human",
        "simulated": False,
        "user_response": user_response,
        "note": PROVENANCE_NOTE,
        "impl_proposal_source": IMPL_PROPOSAL_SOURCE,
    }
    with open(run_dir / "logs" / "gate-resolution-record.json", "w", encoding="utf-8") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)

    # orchestrator 조립(no-op invoker — accept_revision 은 invoke 하지 않는다).
    orch, cfg = build_orchestrator_k(run_dir, _NoInvoke())

    # (5) 실 LLM 산출 artifact 회수·검증(외부 워크스페이스 기준).
    workspace = cfg.get("workspace_dir") or str(run_dir / "workspace")
    proposal_path = Path(workspace) / k_scenario.PROPOSAL_FILE
    if not proposal_path.exists():
        print("[ERR] 제안 artifact 부재 — 검증 불가: %s" % proposal_path, file=sys.stderr)
        print("      (실 LLM 제안 step p1 이 아직 산출하지 않았거나 경로 불일치.)", file=sys.stderr)
        return 1
    payload = load_json(proposal_path)

    errors = validate_proposal(payload)
    if errors:
        print("[REJECT] 제안 payload 검증 실패 — 자동 수정하지 않는다(정직 실패):", file=sys.stderr)
        for e in errors:
            print("  - %s" % e, file=sys.stderr)
        return 1

    # (6) task_added revision append — basis = proposingStepRef p1 + gateEventRef(PO-INV 5).
    revision = orch.accept_revision(
        KIND_TASK_ADDED, payload, proposingStepRef="p1", gateEventRef=gate_id
    )

    print("[RESOLVE] gate_id=%s resolved by actor=human (실 사용자·simulated=false)." % gate_id)
    print("[VALIDATE] 제안 payload 검증 통과(필수 키 11종·id/impl·dependsOn/['d1']·상대경로).")
    print("[REVISION] task_added seq=%s id=%s basis.proposingStepRef=p1 gateEventRef=%s"
          % (revision.revisionSeq, payload["id"], gate_id))
    print("[NOTE] 실 사용자 응답·실 LLM 제안 출처 = logs/gate-resolution-record.json + "
          "user-resolution-provenance 이벤트(append-only 로그).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
