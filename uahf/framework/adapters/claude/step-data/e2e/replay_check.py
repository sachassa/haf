"""결정적 재개 검사 (SH-INV-3) — 동일 로그 -> 동일 재개 지점.

사용법:  python replay_check.py <events.jsonl> <steps-dir> <step_order_csv>

주어진 이벤트 로그를 *읽기 전용*으로 재생해 derive_states 와 ready_set 을 계산하고
정규화 JSON 으로 stdout 에 출력한다. 로그를 변경하지 않는다(순수 판독). 같은 입력에
대해 항상 같은 출력을 내야 한다 — 두 번 실행해 stdout 을 비교하면 결정성이 실증된다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _e2e_common import load_steps  # 경로 배선 포함

from host import StepHost  # noqa: E402
from events import JsonlEventStore  # noqa: E402


def main() -> int:
    events_path = Path(sys.argv[1]).resolve()
    steps_dir = Path(sys.argv[2]).resolve()
    order = sys.argv[3].split(",")

    # steps/<id>.json 로드를 위해 run_dir(= steps_dir 의 부모) 사용.
    run_dir = steps_dir.parent
    steps = load_steps(run_dir, order)

    # 읽기 전용 재생: JsonlEventStore 는 append 만 추가하고, 여기서는 read 만 한다.
    store = JsonlEventStore(str(events_path))
    host = StepHost(steps, invoker=None, store=store)  # invoker 미사용(재생만).

    states = host.derive_states()
    ready = host.ready_set(states)
    escalated = host.has_escalated(states)

    out = {
        "states": states,
        "ready_set": ready,
        "escalated": escalated,
        "all_passed": host.all_passed(states),
    }
    # 정규화(sort_keys) 출력 — 결정성 비교용.
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
