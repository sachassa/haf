"""시나리오 (w) run 데이터 백엔드를 물리화한다 (setup_m.py 동형·워크스페이스 가드 상이).

사용법:  python setup_w.py

생성 구조 (orchestration-data/runs/orch-w-impl-cp/):
  config.json        run 파라미터·메타(workspace_dir 포함)
  graph.json         초기 그래프(impl-plan 단위 1개 — full Task dict)
  gate_policy.json   Gate Policy 데이터(proposal→user_decision·implementation→review)
  steps/<id>.json    단위별 직렬화 뷰(참조용·초기 그래프 미러)
  logs/·workspace/   invoke 캡처·(미사용) 로컬 workspace 슬롯
  (events.jsonl·revisions.jsonl·artifacts.jsonl 은 러너/resolve_w 가 append-only 생성)

**워크스페이스 가드 차이(setup_k·setup_m 와 상이):**
  - run 디렉터리(runs/<id>/)는 fresh 초기화한다(있으면 rmtree — run 데이터는 재실행 대상).
    basename 가드(오삭제 방지): run_dir.name == RUN_ID 일 때만 rmtree.
  - 외부 워크스페이스(config.workspace_dir = C:\\my-claude-project\\uahf-control-plane)는 **실
    소비 프로젝트(독립 git 저장소)**다. setup 은 이를 **삭제·초기화·생성하지 않는다** — 실재
    확인만 한다(존재 그대로 사용). setup_m 의 append-only 가드("선재 파일 있으면 에러")와도 다르다:
    실 프로젝트이므로 선재 파일이 있는 것이 정상이며 그대로 보존한다. 부재 시에만 정직 실패한다
    (실 프로젝트를 setup 이 날조·생성하지 않는다).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import w_scenario
from _orch_common import RUNS_DIR


def _write(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)


def main() -> int:
    # --- run 디렉터리: fresh 초기화(재실행 대상·basename 가드) --------------
    run_dir = Path(RUNS_DIR) / w_scenario.RUN_ID
    if run_dir.exists():
        if run_dir.name != w_scenario.RUN_ID:
            print("[ERR] run_dir basename 불일치 — 오삭제 방지 가드로 중단: %s" % run_dir,
                  file=sys.stderr)
            return 1
        shutil.rmtree(run_dir)
    (run_dir / "steps").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "workspace").mkdir(parents=True, exist_ok=True)

    graph = w_scenario.initial_graph()
    cfg = w_scenario.config()
    _write(run_dir / "config.json", cfg)
    _write(run_dir / "graph.json", graph)
    _write(run_dir / "gate_policy.json", w_scenario.gate_policy())

    # steps/<id>.json — 초기 그래프 단위의 직렬화 뷰(참조용).
    for task in graph["tasks"]:
        _write(run_dir / "steps" / (task["id"] + ".json"), task)

    # --- 외부 워크스페이스 = 실 소비 프로젝트: 실재 확인만(삭제·초기화·생성 금지) ----
    workspace = cfg.get("workspace_dir")
    ws_path = Path(workspace) if workspace else None
    if ws_path is None:
        print("[ERR] config.workspace_dir 미설정.", file=sys.stderr)
        return 1
    if not ws_path.exists() or not ws_path.is_dir():
        print(
            "[ERR] 워크스페이스(실 소비 프로젝트)가 실재하지 않는다 — setup 은 이를 날조·생성하지 "
            "않는다: %s" % ws_path,
            file=sys.stderr,
        )
        return 1
    existing = len(list(ws_path.iterdir()))

    print("[SETUP-W] -> %s" % run_dir)
    print("  initial tasks: %s" % ", ".join(t["id"] for t in graph["tasks"]))
    print("  gate policy: proposal(impl-plan)->user_decision_required, "
          "implementation->review_required")
    print("  workspace (실 프로젝트·보존·무수정 — 선재 항목 %d개 그대로 사용): %s"
          % (existing, ws_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
