"""verify_checks 테스트용 sys.path 배선 — 상위 adapters/claude/ 를 import 경로에 둔다.

verify_checks.py 는 flat import 관례를 쓴다(entry/adapters/claude/tests/conftest.py 선례 동형).
이 디렉터리의 상위(adapters/claude)를 sys.path 에 넣어야 pytest 수집 시 `import verify_checks` 가 성립한다.
"""

import os
import sys

_ADAPTER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # adapters/claude
if _ADAPTER not in sys.path:
    sys.path.insert(0, _ADAPTER)
