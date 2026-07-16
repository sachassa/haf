"""e2e 드라이버 테스트용 sys.path 배선 — 상위 e2e/ 디렉터리를 import 경로에 둔다.

e2e/ 모듈(verify_run·delegation_check·_orch_common 등)은 flat import 관례를 쓰므로
(k_common·resolve_* 실측 동형) 이 디렉터리를 sys.path 에 넣어야 pytest 수집 시 import 가
성립한다. _orch_common import 가 다시 중립 코드 경로(orchestrator·step-host·step-invoker)를
배선한다.
"""

import os
import sys

_E2E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _E2E not in sys.path:
    sys.path.insert(0, _E2E)
