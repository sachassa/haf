"""step-host 라이브러리 무수정 재사용 브리지 (05 §0·§2.2·§6).

orchestration Layer 의 중립 코드가 `uahf/framework/loop/step-host/` 중립 모듈을
**라이브러리로 무수정 import** 하기 위한 유일한 경로다. Step Host 는 평면(flat) import
관례를 쓰므로(그 디렉터리 README·tests 실측 — `from host import ...`), 그 디렉터리를
`sys.path` 에 넣어야 import 가 성립한다.

경로 조작은 **전적으로 orchestration 쪽에서만** 이뤄진다. `uahf/` 트리는 읽기·import
만 하며 무촉이다(05 §0 — substrate 라이브러리 무수정 import 는 UAF-INV ①(접점 원칙)과 병존). 이 모듈은 Step Host
의 공개 심볼을 그대로 재노출할 뿐, 재정의·수정하지 않는다(05 §2.2 재정의 0).
"""

from __future__ import annotations

import os
import sys

# 이 파일: orchestration/framework/orchestrator/stephost_bridge.py
# 저장소 루트까지 3단계 상향(orchestrator → framework → orchestration → repo root).
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_HERE, os.pardir, os.pardir, os.pardir))
STEP_HOST_DIR = os.path.join(_REPO_ROOT, "uahf", "framework", "loop", "step-host")

if STEP_HOST_DIR not in sys.path:
    sys.path.insert(0, STEP_HOST_DIR)

# --- Step Host 중립 모듈 공개 심볼 재노출(무수정) --------------------------------
from step import Step  # noqa: E402
from events import (  # noqa: E402
    EVENT_FIELDS,
    ACTIVE,
    ESCALATED,
    EventLog,
    EventStore,
    FAILED,
    InMemoryEventStore,
    JsonlEventStore,
    PASSED,
    PENDING,
)
from host import (  # noqa: E402
    DEFAULT_RETRY_LIMIT,
    RunResult,
    StepHost,
    STOP_BLOCKED,
    STOP_ESCALATED,
)
from invoker import (  # noqa: E402
    Invoker,
    InvokeRequest,
    InvokeResult,
    KIND_BLOCKED,
    KIND_COMPLETION,
    KIND_FAILURE,
    POLICY_AUTO_APPROVE,
    POLICY_INTERACTIVE,
    POLICY_UNRESTRICTED,
    ROLE_ADVISOR,
    ROLE_VERIFIER,
    ROLE_WORKER,
    load_invoker,
)

__all__ = [
    "STEP_HOST_DIR",
    # step.py
    "Step",
    # events.py
    "EVENT_FIELDS",
    "EventLog",
    "EventStore",
    "InMemoryEventStore",
    "JsonlEventStore",
    "PENDING",
    "ACTIVE",
    "PASSED",
    "FAILED",
    "ESCALATED",
    # host.py
    "StepHost",
    "RunResult",
    "DEFAULT_RETRY_LIMIT",
    "STOP_ESCALATED",
    "STOP_BLOCKED",
    # invoker.py
    "Invoker",
    "InvokeRequest",
    "InvokeResult",
    "load_invoker",
    "KIND_COMPLETION",
    "KIND_FAILURE",
    "KIND_BLOCKED",
    "POLICY_INTERACTIVE",
    "POLICY_AUTO_APPROVE",
    "POLICY_UNRESTRICTED",
    "ROLE_WORKER",
    "ROLE_VERIFIER",
    "ROLE_ADVISOR",
]
