"""시나리오 (j) run 데이터 백엔드를 물리화한다 (바인딩 §5.3 구조).

사용법:  python setup_j.py

생성 구조 (orchestration-data/runs/orch-j-e2e/):
  config.json        run 파라미터·메타
  graph.json         초기 그래프(full Task dict — 게이트 descriptor 보존)
  gate_policy.json   Gate Policy 데이터(설계→user_decision·구현→review)
  steps/<id>.json    단위별 직렬화 뷰(참조용·초기 그래프 미러)
  logs/·workspace/   invoke 캡처·호스팅 산출 대기
  (events.jsonl·revisions.jsonl·artifacts.jsonl 은 러너가 append-only 생성)

기존 run 디렉터리가 있으면 초기화한다(fresh setup).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import j_scenario
from _orch_common import RUNS_DIR


def _write(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)


def main() -> int:
    run_dir = Path(RUNS_DIR) / j_scenario.RUN_ID
    if run_dir.exists():
        shutil.rmtree(run_dir)
    (run_dir / "steps").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "workspace").mkdir(parents=True, exist_ok=True)

    graph = j_scenario.initial_graph()
    _write(run_dir / "config.json", j_scenario.config())
    _write(run_dir / "graph.json", graph)
    _write(run_dir / "gate_policy.json", j_scenario.gate_policy())

    # steps/<id>.json — 초기 그래프 단위의 직렬화 뷰(참조용).
    for task in graph["tasks"]:
        _write(run_dir / "steps" / (task["id"] + ".json"), task)

    print("[SETUP-J] -> %s" % run_dir)
    print("  initial tasks: %s" % ", ".join(t["id"] for t in graph["tasks"]))
    print("  gate policy: design_maturation->user_decision_required, "
          "implementation->review_required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
