"""W3 E2E — 시나리오를 run 데이터 백엔드에 물리화한다 (바인딩 §3.2 구조).

사용법:  python setup_run.py <scenario-name>   (예: s1, s2, ... s7a, s7b)

생성 구조:
  runs/<run-id>/config.json          (run 파라미터·메타)
  runs/<run-id>/steps/<id>.json      (Step 직렬화 — JSON)
  runs/<run-id>/logs/                (invoke 캡처 대기)
  runs/<run-id>/workspace/           (호스팅 세션 산출 — subdir 모드)

기존 run 디렉터리가 있으면 초기화한다(fresh setup). s4 resume 은 setup 을 1회만 하고
두 번째 호스트 실행이 같은 디렉터리를 재사용한다.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import scenarios
from _e2e_common import RUNS_DIR


def main() -> int:
    name = sys.argv[1]
    spec = scenarios.get(name)
    run_id = spec["run_id"]
    run_dir = Path(RUNS_DIR) / run_id

    if run_dir.exists():
        shutil.rmtree(run_dir)
    (run_dir / "steps").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    if spec.get("workspace_mode", "subdir") == "subdir":
        (run_dir / "workspace").mkdir(parents=True, exist_ok=True)

    # steps/<id>.json
    for sid, step in spec["steps"].items():
        with open(run_dir / "steps" / (sid + ".json"), "w", encoding="utf-8") as fh:
            json.dump(step, fh, ensure_ascii=False, indent=2, sort_keys=True)

    # config.json — 스텝 본문 제외 run 파라미터·메타.
    config = {k: v for k, v in spec.items() if k != "steps"}
    with open(run_dir / "config.json", "w", encoding="utf-8") as fh:
        json.dump(config, fh, ensure_ascii=False, indent=2, sort_keys=True)

    print("[SETUP] %s -> %s" % (name, run_dir))
    print("  steps: %s" % ", ".join(spec["step_order"]))
    print("  policy=%s workspace_mode=%s cp3=%s"
          % (spec.get("policy"), spec.get("workspace_mode"),
             (spec.get("cp3") or {}).get("enabled")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
