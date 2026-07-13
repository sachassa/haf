"""시나리오 (k) 결정적 재개 검사 (PO-INV 3) — replay_check.py 동형·k_common 빌더.

사용법:  python replay_k.py <run-dir>

주어진 run 데이터 백엔드를 *읽기 전용*으로 재생해 active_graph·ready_set·states·
graph_fingerprint 를 계산하고 정규화 JSON 으로 stdout 에 출력한다. 원장·로그를 변경하지
않는다(순수 판독). invoker 는 절대 호출되지 않음을 보장하기 위해 호출 시 예외를 던지는
sentinel 을 주입한다(재생 중 실 CLI 0). 두 번 실행해 stdout 을 비교하면 결정성이 실증된다.

빌더만 k_common.build_orchestrator_k(외부 워크스페이스 배선)로 바뀔 뿐, 재생은 read-only
경로이므로 workdir 은 파생에 무간섭이다(invoke 미호출).

이 스크립트는 orchestration-data/e2e/ 경계 소속이다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from k_common import build_orchestrator_k


class _NoInvoke:
    def invoke(self, request):
        raise RuntimeError("replay_k 는 실행하지 않는다(읽기 전용 재생)")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python replay_k.py <run-dir>", file=sys.stderr)
        return 64
    run_dir = Path(sys.argv[1]).resolve()

    orch, _cfg = build_orchestrator_k(run_dir, _NoInvoke())

    graph = orch.active_graph()
    out = {
        "active_task_ids": [t.get("id") for t in graph["tasks"]],
        "states": orch.derive_states(),
        "ready_set": orch.ready_set(),
        "graph_fingerprint": orch.graph_fingerprint(),
    }
    # 정규화(sort_keys) 출력 — 결정성 비교용.
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
