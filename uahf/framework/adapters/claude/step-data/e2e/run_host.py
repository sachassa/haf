"""W3 E2E 호스트 런처 — <run-dir> 하나를 구동한다.

사용법:  python run_host.py <run-dir>

- config.json 의 step_order 대로 steps/<id>.json 을 Step.from_dict 로 로드한다.
- 커밋된 StepHost 를 LoggingClaudeInvoker 로 구동한다(중립 Host 무수정).
- stop_handler 를 sys.exit(2) 로 바인딩한다 — blocked/Escalated 정지 시 종료 코드 2
  (바인딩 §5.3). 정상 완주 = 0, halted = 3.
- config.cp3.enabled 이고 완주 시 배치 종단 CP3(Advisor) 를 별도 fresh 세션으로
  디스패치해 final_verdict 를 logs/cp3-result.json 에 기록한다(OQ-SH-1).

이 스크립트는 step-data/e2e/ 경계 소속이다(provider 토큰 허용).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from _e2e_common import (
    load_config,
    load_steps,
    make_invoker,
    resolve_workdir,
    RUNS_DIR,
    InvokeRequest,
    ROLE_ADVISOR,
)

# 경로 배선 후 커밋된 중립 Host 를 import.
from host import StepHost  # noqa: E402
from events import JsonlEventStore  # noqa: E402


def dispatch_cp3(run_dir: Path, cfg: dict, steps, result, invoker) -> None:
    """배치 종단 CP3 — Advisor 역할 fresh 세션(사람 승인 아님·02 §3.1)."""
    cp3 = cfg.get("cp3") or {}
    model = cp3.get("model", "sonnet")
    workdir = resolve_workdir(run_dir, cfg.get("workspace_mode", "subdir"))
    verdicts = []
    for step in steps:
        bundle = {
            "step_contract": step.contract(),
            "final_state": result.states.get(step.id),
            "criteria": step.done,
            "artifacts_workdir": workdir,
            "note": (
                "CP1 자체 점검·CP2 독립 판정을 이미 통과해 Passed 로 기록된 Step 이다. "
                "산출물을 직접 확인하고 최종 승인 판정을 내려라. 거짓 완료가 아님을 검증하라."
            ),
        }
        req = InvokeRequest(
            bundle=bundle,
            role=ROLE_ADVISOR,
            model=model,
            policy=cfg.get("policy", "auto_approve"),
            workdir=workdir,
            timeout=cfg.get("timeout"),
            criteria=step.done,
        )
        res = invoker.invoke(req)
        verdicts.append({
            "step_id": step.id,
            "kind": res.kind,
            "final_verdict": (res.completion or {}).get("verdict"),
            "rework": (res.completion or {}).get("rework"),
        })
    with open(run_dir / "logs" / "cp3-result.json", "w", encoding="utf-8") as fh:
        json.dump({"cp3_model": model, "verdicts": verdicts}, fh, ensure_ascii=False, indent=2)
    print("[CP3] dispatched (model=%s): %s" % (model, json.dumps(verdicts, ensure_ascii=False)))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python run_host.py <run-dir>", file=sys.stderr)
        return 64
    run_dir = Path(sys.argv[1]).resolve()
    cfg = load_config(run_dir)
    order = cfg["step_order"]
    steps = load_steps(run_dir, order)

    logs_dir = str(run_dir / "logs")
    os.makedirs(logs_dir, exist_ok=True)
    events_path = str(run_dir / "events.jsonl")
    workdir = resolve_workdir(run_dir, cfg.get("workspace_mode", "subdir"))

    invoker = make_invoker(
        logs_dir=logs_dir,
        allowed_tools=cfg.get("allowed_tools"),
        output_format=cfg.get("output_format", "json"),
    )

    # 런처가 자기 PID 를 기록한다(s4 강제 중단용).
    with open(run_dir / "host.pid", "w", encoding="utf-8") as fh:
        fh.write(str(os.getpid()))

    def stop_handler(reason, tasks):
        marker = {"stop_reason": reason, "stopped_tasks": list(tasks)}
        with open(run_dir / "logs" / "stop-signal.json", "w", encoding="utf-8") as fh:
            json.dump(marker, fh, ensure_ascii=False, indent=2)
        print("[STOP] reason=%s tasks=%s -> exit code 2" % (reason, tasks))
        sys.exit(2)  # 바인딩 §5.3 물리 정지 신호.

    host = StepHost(
        steps,
        invoker,
        store=JsonlEventStore(events_path),
        retry_limit=cfg.get("retry_limit", 2),
        policy=cfg.get("policy", "auto_approve"),
        workdir=workdir,
        timeout=cfg.get("timeout"),
        stop_handler=stop_handler,
    )

    result = host.run()  # stop_handler 가 정지 시 sys.exit(2) 로 preempt.

    print("[RESULT] status=%s states=%s" % (result.status, json.dumps(result.states, ensure_ascii=False)))
    print("[INVOKES] total=%d" % invoker.invoke_count)

    if result.completed and (cfg.get("cp3") or {}).get("enabled"):
        dispatch_cp3(run_dir, cfg, steps, result, invoker)

    if result.completed:
        return 0
    return 3  # halted (완주 아님·Escalated 아님) — 재개 대기.


if __name__ == "__main__":
    sys.exit(main())
