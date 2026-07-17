"""entry_resolve 테스트용 sys.path 배선 — 상위 entry/adapters/claude/ 를 import 경로에 둔다.

entry_resolve.py 는 flat import 관례를 쓰므로(e2e/tests/conftest.py 선례 동형) 이 디렉터리를
sys.path 에 넣어야 pytest 수집 시 `import entry_resolve` 가 성립한다.
"""

import os
import sys

_ADAPTER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # entry/adapters/claude
if _ADAPTER not in sys.path:
    sys.path.insert(0, _ADAPTER)
