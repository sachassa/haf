"""시나리오 (m) run 데이터 백엔드 + 외부 워크스페이스를 물리화한다 (setup_k.py 동형·가드 상이).

사용법:  python setup_m.py

생성 구조 (orchestration-data/runs/orch-m-maturation-cp/):
  config.json        run 파라미터·메타(workspace_dir 포함)
  graph.json         초기 그래프(assess 단위 1개 — full Task dict)
  gate_policy.json   Gate Policy 데이터(assess→user_decision·propose/reconcile→review·review→user_decision)
  steps/<id>.json    단위별 직렬화 뷰(참조용·초기 그래프 미러)
  logs/·workspace/   invoke 캡처·(미사용) 로컬 workspace 슬롯
  (events.jsonl·revisions.jsonl·artifacts.jsonl 은 러너/resolve_m 이 append-only 생성)

추가로 config 의 workspace_dir(run 디렉터리 **밖**·UAHF 저장소 내부 절대경로 —
solution-design-data/events/maturation-r003/)에 외부 워크스페이스 디렉터리를 생성한다 — SD
성숙 산출(assessing-judgment.md·stage-plan.json·proposal-*.md·reconciling-record.md·
reviewing-record.md·candidate/)의 물리 위치다.

**가드 차이(setup_k 와 상이):**
  - run 디렉터리(runs/<id>/)는 fresh 초기화한다(있으면 rmtree — run 데이터는 재실행 대상).
  - 외부 워크스페이스(maturation-r003/)는 **Solution Design 데이터·append-only** 이므로 절대
    삭제하지 않는다. 선재 파일이 있으면 **에러로 중단**한다(오삭제·SD 로그 훼손 방지).
    부재 시에만 디렉터리를 생성한다(빈 디렉터리는 허용·no-op).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import m_scenario
from _orch_common import RUNS_DIR


def _write(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)


def _has_files(path: Path) -> bool:
    """디렉터리에 (파일이든 하위 디렉터리든) 선재 항목이 하나라도 있으면 True."""
    return path.exists() and any(path.iterdir())


def main() -> int:
    # --- run 디렉터리: fresh 초기화(재실행 대상) ---------------------------
    run_dir = Path(RUNS_DIR) / m_scenario.RUN_ID
    if run_dir.exists():
        shutil.rmtree(run_dir)
    (run_dir / "steps").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "workspace").mkdir(parents=True, exist_ok=True)

    graph = m_scenario.initial_graph()
    cfg = m_scenario.config()
    _write(run_dir / "config.json", cfg)
    _write(run_dir / "graph.json", graph)
    _write(run_dir / "gate_policy.json", m_scenario.gate_policy())

    # steps/<id>.json — 초기 그래프 단위의 직렬화 뷰(참조용).
    for task in graph["tasks"]:
        _write(run_dir / "steps" / (task["id"] + ".json"), task)

    # --- 외부 워크스페이스: SD 데이터 append-only 가드(rmtree 금지) --------
    workspace = cfg.get("workspace_dir")
    ws_path = Path(workspace) if workspace else None
    if ws_path is not None:
        if _has_files(ws_path):
            print(
                "[ERR] 외부 워크스페이스에 선재 파일이 있다 — SD 데이터 append-only 이므로 "
                "삭제하지 않고 중단한다: %s" % ws_path,
                file=sys.stderr,
            )
            print(
                "      (fresh 초기화는 run 디렉터리에만 적용된다. maturation-r003 을 새로 쓰려면 "
                "다른 runId 를 쓰거나 사용자가 명시적으로 정리하라.)",
                file=sys.stderr,
            )
            return 1
        ws_path.mkdir(parents=True, exist_ok=True)

    print("[SETUP-M] -> %s" % run_dir)
    print("  initial tasks: %s" % ", ".join(t["id"] for t in graph["tasks"]))
    print("  gate policy: sd_assess->user_decision_required, sd_propose->review_required, "
          "sd_reconcile->review_required, sd_review->user_decision_required")
    print("  external workspace (SD append-only·오삭제 가드): %s" % ws_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
