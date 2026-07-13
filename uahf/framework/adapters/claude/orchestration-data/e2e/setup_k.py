"""시나리오 (k) run 데이터 백엔드 + 외부 워크스페이스를 물리화한다 (setup_j.py 동형).

사용법:  python setup_k.py

생성 구조 (orchestration-data/runs/orch-k-nonfixture-smoke/):
  config.json        run 파라미터·메타(workspace_dir 포함)
  graph.json         초기 그래프(d1 설계 + p1 실 LLM 제안 — full Task dict)
  gate_policy.json   Gate Policy 데이터(설계→review·제안→user_decision·구현→review)
  steps/<id>.json    단위별 직렬화 뷰(참조용·초기 그래프 미러)
  logs/·workspace/   invoke 캡처·(미사용) 로컬 workspace 슬롯
  (events.jsonl·revisions.jsonl·artifacts.jsonl 은 러너가 append-only 생성)

추가로 config 의 workspace_dir(run 디렉터리 **밖** 절대경로)에 외부 워크스페이스 디렉터리를
생성한다 — 실 LLM step 산출(design-decision.md·impl-proposal.json)의 물리 위치다.

기존 run 디렉터리·외부 워크스페이스가 있으면 초기화한다(fresh setup). 외부 워크스페이스 삭제는
basename 이 'orch-k-workspace' 일 때만 수행한다(오삭제 방지 가드).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import k_scenario
from _orch_common import RUNS_DIR


def _write(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)


def main() -> int:
    run_dir = Path(RUNS_DIR) / k_scenario.RUN_ID
    if run_dir.exists():
        shutil.rmtree(run_dir)
    (run_dir / "steps").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "workspace").mkdir(parents=True, exist_ok=True)

    graph = k_scenario.initial_graph()
    cfg = k_scenario.config()
    _write(run_dir / "config.json", cfg)
    _write(run_dir / "graph.json", graph)
    _write(run_dir / "gate_policy.json", k_scenario.gate_policy())

    # steps/<id>.json — 초기 그래프 단위의 직렬화 뷰(참조용).
    for task in graph["tasks"]:
        _write(run_dir / "steps" / (task["id"] + ".json"), task)

    # 외부 워크스페이스(run 디렉터리 밖 절대경로) 물리화 — fresh(오삭제 방지 가드).
    workspace = cfg.get("workspace_dir")
    ws_path = Path(workspace) if workspace else None
    if ws_path is not None:
        if ws_path.exists() and ws_path.name == "orch-k-workspace":
            shutil.rmtree(ws_path)
        ws_path.mkdir(parents=True, exist_ok=True)

    print("[SETUP-K] -> %s" % run_dir)
    print("  initial tasks: %s" % ", ".join(t["id"] for t in graph["tasks"]))
    print("  gate policy: design->review_required, proposal->user_decision_required, "
          "implementation->review_required")
    print("  external workspace: %s" % ws_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
