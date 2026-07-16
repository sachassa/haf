#!/usr/bin/env python3
"""4-트리 테스트 러너 (deterministic·Skill 아님·python3 stdlib only).

저장소 루트를 이 파일 위치 기준으로 역산해 4개 pytest 트리를 1회 subprocess 로 실행한다.
목적 = 매 단계 4경로 명령을 재도출하는 수고 제거(튜닝 Before/After 효과 주장은 불포함).

사용법:
  python run_all_tests.py            # -q 기본.
  python run_all_tests.py -v -k foo  # 추가 인자는 pytest 로 패스스루.

pytest 종료코드를 그대로 반환한다. 기대 통과 수는 하드코딩하지 않는다(트랙 진행에 따라 증가).
"""

import subprocess
import sys
from pathlib import Path

# 이 파일: <repo>/uahf/framework/adapters/claude/orchestration-data/e2e/run_all_tests.py
#          parents[0]=e2e ... parents[5]=orchestration-data ... 아래 index 로 <repo> 역산.
_HERE = Path(__file__).resolve().parent                       # .../orchestration-data/e2e
_REPO = _HERE.parents[5]                                       # <repo 루트>

TEST_TREES = [
    "orchestration/framework/orchestrator/tests",
    "uahf/framework/loop/step-host/tests",
    "uahf/framework/adapters/claude/step-invoker/tests",
    "uahf/framework/adapters/claude/orchestration-data/e2e/tests",
]


def main(argv):
    paths = [str(_REPO / tree) for tree in TEST_TREES]
    extra = argv if argv else ["-q"]
    cmd = [sys.executable, "-m", "pytest", *paths, *extra]
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
