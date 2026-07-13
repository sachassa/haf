"""시나리오 (m) — 구조 승인 게이트의 실 사용자 수정 요구 반영 (task_superseded 1건).

사용법:  python amend_m_wireframe.py <run-dir>

구조 승인 게이트(gate-unit-assess)의 실 사용자 응답(2026-07-14)은 "승인 + Wireframe 요구
추가"였다 — stage-plan 4단계 편입은 resolve_m --phase structure 가 수행했고, 본 스크립트는
그 **동일 게이트 승인 응답이 요구한 수정**(propose-ui-view-designer 산출에 텍스트 기반
Wireframe 절 포함)을 append-only 그래프 진화로 반영한다:

  - kind = task_superseded, supersedes = id = "propose-ui-view-designer"(동일 id 대체 —
    피대체 Task 의 정렬 위치·후속 의존(reconcile.dependsOn) 승계, revision.py fold).
  - payload = assess 산출 stage-plan 의 해당 stage 사본에 task/done/delegation 만 보강 —
    Wireframe 절 요구를 task 에 추가하고 done AC 가 'Wireframe' 마커를 검사하도록 확장.
  - basis = {proposingStepRef: "assess", gateEventRef: "gate-unit-assess"} — 제안 원천은
    assess 산출물이고, 수정 지시의 근거는 게이트 해소 레코드
    (logs/gate-resolution-record-structure.json)의 실 사용자 응답 원문이다(PO-INV 5).

이 스크립트는 orchestration-data/e2e/ 경계 소속이다. 기존 파일·stage-plan.json 은 수정하지
않는다(assess artifact 불변 — 수정은 revision 원장 위에서만).
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from k_common import build_orchestrator_k, load_json

from revision import KIND_TASK_SUPERSEDED  # noqa: E402 (중립 코드 무수정 import)

import m_scenario  # noqa: E402

GATE_ID = "gate-unit-assess"
TARGET_ID = "propose-ui-view-designer"

WIREFRAME_REQ = (
    "\n\n[사용자 게이트 수정 요구 — 구조 승인 게이트 실 사용자 응답 2026-07-14] 산출문서에 "
    "'## Wireframe' 절을 반드시 포함하라: run 목록 뷰와 단일 run 심층 뷰 각각의 화면 레이아웃을 "
    "텍스트 기반 Wireframe(ASCII/텍스트 다이어그램)으로 스케치하고, 주요 영역(헤더·run 목록 "
    "테이블·이벤트 타임라인·게이트 패널·revision/artifact 계보 뷰·토큰/비용 패널)의 배치를 "
    "표현하라. 리터럴 문자열 'Wireframe' 을 절 제목에 포함하라."
)

AMENDED_DONE = (
    "python -c \"import io;p='proposal-ui-view-designer.md';t=io.open(p,encoding='utf-8')"
    ".read();assert len(t)>0,'empty';assert 'Wireframe' in t,'wireframe-section'\" "
    "(종료 코드 0 = 통과)"
)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python amend_m_wireframe.py <run-dir>", file=sys.stderr)
        return 64
    run_dir = Path(sys.argv[1]).resolve()

    cfg = load_json(run_dir / "config.json")
    plan = load_json(Path(cfg["workspace_dir"]) / m_scenario.STAGE_PLAN_FILE)
    base = next(st for st in plan["stages"] if st["id"] == TARGET_ID)

    payload = copy.deepcopy(base)
    payload["supersedes"] = TARGET_ID          # 동일 id 대체(의존·위치 승계)
    payload["task"] = base["task"] + WIREFRAME_REQ
    payload["done"] = AMENDED_DONE
    payload["delegation"]["task"] = payload["task"]
    payload["delegation"]["done"] = AMENDED_DONE
    payload["delegation"]["context"] = list(base["delegation"]["context"]) + [
        "구조 승인 게이트 실 사용자 수정 요구(2026-07-14): 텍스트 Wireframe 절 포함 — "
        "근거 = logs/gate-resolution-record-structure.json 사용자 응답 원문",
    ]

    class _NoInvoke:
        def invoke(self, request):
            raise RuntimeError("amend 스크립트는 실행하지 않는다(revision append 전용)")

    orch, _cfg = build_orchestrator_k(run_dir, _NoInvoke())
    revision = orch.accept_revision(
        KIND_TASK_SUPERSEDED, payload, proposingStepRef="assess", gateEventRef=GATE_ID
    )
    print("[AMEND] task_superseded seq=%s id=%s (동일 id 대체·Wireframe 절 요구·done AC 확장)"
          % (revision.revisionSeq, payload["id"]))
    print("[BASIS] proposingStepRef=assess gateEventRef=%s — 수정 지시 근거 = "
          "gate-resolution-record-structure.json 실 사용자 응답" % GATE_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
