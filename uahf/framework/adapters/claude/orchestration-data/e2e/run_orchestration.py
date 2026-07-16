"""시나리오 (j) 단일 위상 러너 — 중립 Orchestrator 를 실 claude CLI 로 구동한다.

사용법:  python run_orchestration.py <run-dir>

- run 데이터 백엔드에서 Orchestrator 를 조립(무수정 라이브러리)해 run() 한다.
- 게이트 정지(escalation/user_decision 미해소) 시 stop-signal.json + pending_gates 를
  기록하고 **종료 코드 2**로 종료한다(바인딩 §5.3 물리 정지 신호). = (j1) 물리 정지.
- 정상 완주 = 0, halted = 3, Escalated 정지(Step Host) = 2.
- 실 CLI 실패는 은폐하지 않는다(O5) — result·로그가 그대로 남는다.

이 스크립트는 orchestration-data/e2e/ 경계 소속이다(provider 토큰 허용).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from _orch_common import build_orchestrator, make_invoker


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python run_orchestration.py <run-dir>", file=sys.stderr)
        return 64
    run_dir = Path(sys.argv[1]).resolve()

    # 러너가 자기 PID 를 기록한다(외부 관측용).
    with open(run_dir / "host.pid", "w", encoding="utf-8") as fh:
        fh.write(str(os.getpid()))

    # config 를 먼저 읽어 invoker 를 만든다.
    from _orch_common import load_json
    cfg = load_json(run_dir / "config.json")
    invoker = make_invoker(run_dir, cfg)

    orch, _cfg = build_orchestrator(run_dir, invoker)
    result = orch.run()

    print("[RESULT] status=%s stop_reason=%s epochs=%s"
          % (result.status, result.stop_reason, result.epochs))
    print("[GRAPH] tasks=%s" % json.dumps(result.graph_task_ids, ensure_ascii=False))
    print("[STATES] %s" % json.dumps(result.states, ensure_ascii=False))
    print("[INVOKES] total=%d" % invoker.invoke_count)

    if result.status == "stopped" and result.stop_reason == "gate":
        # (j1) 물리 정지 — 미해소 정지 게이트 큐를 기록하고 종료 코드 2.
        marker = {
            "stop_reason": result.stop_reason,
            "stopped_tasks": result.stopped_tasks,
            "pending_gates": result.pending_gates,
            "note": "user_decision 게이트 물리 정지 — 사용자 해소 이벤트 대기(exit 2). "
                    "unrestricted/auto_approve 여부와 무관하게 게이트 정지는 보존된다(PO-INV 4).",
        }
        with open(run_dir / "logs" / "stop-signal.json", "w", encoding="utf-8") as fh:
            json.dump(marker, fh, ensure_ascii=False, indent=2)
        print("[STOP] gate pending=%s -> exit code 2"
              % json.dumps([g["gate_id"] for g in result.pending_gates], ensure_ascii=False))
        print("[PENDING-GATES] %s" % json.dumps(result.pending_gates, ensure_ascii=False))
        return 2

    if result.status == "stopped":
        # Escalated(Step Host) 정지도 종료 코드 2.
        print("[STOP] escalated -> exit code 2")
        return 2

    if result.completed:
        print("[COMPLETE] all units Passed.")
        return 0

    print("[HALTED] not completed, not stopped.")
    return 3


if __name__ == "__main__":
    sys.exit(main())
