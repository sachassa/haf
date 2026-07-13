"""시나리오 (j2) — 사용자 게이트 해소(시뮬레이션·라벨) + 구현 단위 revision append.

사용법:  python resolve_and_revise.py <run-dir>

이 스크립트가 하는 일(정지와 재개 사이):
  1. stop-signal.json 에서 정지한 user_decision 게이트 gate_id 를 읽는다(러너가 실제로
     올린 게이트를 그대로 사용 — 추측 0).
  2. **시뮬레이션 라벨을 append-only 로그에 명시 기록**한 뒤(annotation 이벤트) 사용자
     actor(userActorClass=human) 해소 이벤트를 append 한다. gate-resolution-record.json
     에도 "드라이버 시뮬레이션(테스트 픽스처)·실 사용자 아님"을 명시한다(L-07·O5 — 실
     사용자 승인으로 위장 금지).
  3. 구현 단위 제안(픽스처)을 task_added revision 으로 append 한다. basis =
     {proposingStepRef=d1, gateEventRef=<해소된 게이트 통과 이벤트>} — 근거 없는 그래프
     변경 0(PO-INV 5). accept_revision 이 게이트 통과 이벤트 실재를 검증한 뒤에만 수용한다.

정직 표기: 사용자 해소·구현 제안 내용은 **E2E 드라이버 픽스처**이며 실 사용자·실 LLM 제안
step 이 아니다. 실증 대상은 게이트 물리 정지·사용자 actor 적격성·revision 인과 사슬·
deterministic 재개이며, 그 축들은 실 데이터(이벤트·원장)로 남는다.

이 스크립트는 orchestration-data/e2e/ 경계 소속이다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _orch_common import build_orchestrator, load_json

# 중립 코드 심볼(무수정 라이브러리).
from events import EventLog, JsonlEventStore  # noqa: E402
from gates import GATE_USER_DECISION_REQUIRED, append_gate_resolution  # noqa: E402
from revision import KIND_TASK_ADDED  # noqa: E402

import j_scenario  # noqa: E402


SIM_NOTE = (
    "드라이버 시뮬레이션(테스트 픽스처) — 실 사용자 아님. L-07: 실 사용자 승인으로 위장 "
    "금지. actor=human 은 gates.is_eligible_resolver 사용자 actor 클래스 적격성을 통과시키기 "
    "위한 값이며, 실제 사용자 개입이 아니라 E2E 드라이버가 사용자 역할을 시뮬레이션한 것이다."
)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python resolve_and_revise.py <run-dir>", file=sys.stderr)
        return 64
    run_dir = Path(sys.argv[1]).resolve()

    stop = load_json(run_dir / "logs" / "stop-signal.json")
    pending = stop.get("pending_gates") or []
    user_gates = [g for g in pending if g.get("gateKind") == GATE_USER_DECISION_REQUIRED]
    if not user_gates:
        print("[ERR] 정지 신호에 user_decision 게이트가 없다 — 재개 불가.", file=sys.stderr)
        print("      pending=%s" % json.dumps(pending, ensure_ascii=False), file=sys.stderr)
        return 1
    gate_id = user_gates[0]["gate_id"]

    log = EventLog(JsonlEventStore(str(run_dir / "events.jsonl")))

    # (a) 시뮬레이션 라벨을 append-only 로그에 명시 기록(annotation — 게이트·step 파생에 무간섭).
    log.append(
        cycle_id="annotation::sim-" + str(gate_id),
        from_stage=None,
        to_stage="note",
        trigger="시뮬레이션 라벨",
        outcome="pass",
        actor="e2e-driver-sim",
        ref={"kind": "simulation-annotation", "gate_id": gate_id,
             "simulated": True, "note": SIM_NOTE},
    )

    # (b) 사용자 actor 해소 이벤트 append(적격성 = userActorClass=human).
    append_gate_resolution(log, gate_id, GATE_USER_DECISION_REQUIRED, actor="human")

    # (c) 정직 기록 파일.
    record = {
        "gate_id": gate_id,
        "gateKind": GATE_USER_DECISION_REQUIRED,
        "resolved_by_actor": "human",
        "simulated": True,
        "note": SIM_NOTE,
        "impl_proposal_source": (
            "driver-fixture (j_scenario.impl_revision_payload) — 실 LLM 제안 step 아님. "
            "실증 대상은 게이트 정지·해소·revision 인과 사슬이며 제안 내용은 픽스처다."
        ),
    }
    with open(run_dir / "logs" / "gate-resolution-record.json", "w", encoding="utf-8") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)

    # (d) 구현 단위 revision append — 게이트 통과 이벤트 근거로만 수용(PO-INV 5).
    #     accept_revision 은 invoke 하지 않으므로 no-op invoker 로 orchestrator 를 조립한다.
    class _NoInvoke:
        def invoke(self, request):
            raise RuntimeError("resolve_and_revise 는 실행하지 않는다(revision append 전용)")

    orch, _cfg = build_orchestrator(run_dir, _NoInvoke())
    payload = j_scenario.impl_revision_payload()
    revision = orch.accept_revision(
        KIND_TASK_ADDED, payload, proposingStepRef="d1", gateEventRef=gate_id
    )

    print("[RESOLVE] gate_id=%s resolved by actor=human (SIMULATED·라벨 기록)." % gate_id)
    print("[REVISION] task_added seq=%s id=%s basis.gateEventRef=%s"
          % (revision.revisionSeq, payload["id"], gate_id))
    print("[NOTE] 시뮬레이션·픽스처 라벨 = logs/gate-resolution-record.json + "
          "annotation::sim 이벤트(append-only 로그).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
