"""invoker 추상 인터페이스 — 신규 실행 컨텍스트 기동 계약 (프로토콜 §3.2·§7.2).

Host 는 실행 단위를 직접 기동하지 않는다. 대신 이 추상 인터페이스로만 "직렬화된
번들 → 신규(격리된) 실행 컨텍스트 기동 → 보고 회수"를 위임한다. 구체 실행 표면(특정
실행 환경·CLI·권한 옵션 등)은 전부 이 인터페이스 너머의 구현체(Adapter) 소관이며,
이 중립 코드에는 어떤 구현체 이름도 하드코딩하지 않는다 — 구현체는 config 의 모듈
경로 문자열로 로드한다(load_invoker).

입력: 직렬화 이전 번들 + 역할/모델 슬롯 + policy + 작업 디렉터리 + 타임아웃.
출력: 완료 보고 / 실패 보고 / 정지 신호(blocked) 중 하나(InvokeResult).

Host 는 반환의 kind 로만 분기하며 내용 기반 판정을 내리지 않는다(SH-INV-1) — 완료/실패/
차단의 선언은 실행 단위·Verifier 가 소유하고, invoker 는 그 선언을 kind 로 표면화한다.
"""

from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# policy 어휘(Policy as Data — §6.2). Host 는 이 값을 데이터로 invoker 에 전달만 한다.
POLICY_INTERACTIVE = "interactive"
POLICY_AUTO_APPROVE = "auto_approve"
POLICY_UNRESTRICTED = "unrestricted"
POLICY_VALUES = (POLICY_INTERACTIVE, POLICY_AUTO_APPROVE, POLICY_UNRESTRICTED)

# 실행 단위 역할 슬롯(전달용 라벨). 값의 원천은 기존 구조(하네스 역할·04-solution-design
# §3.3 Capability 선언). Host 는 전달만 한다(§3.1).
ROLE_WORKER = "Worker"
ROLE_VERIFIER = "Verifier"
ROLE_ADVISOR = "Advisor"

# InvokeResult.kind 값.
KIND_COMPLETION = "completion"  # 완료 보고 회수(CP1 자체 점검 포함 / CP2 verdict 포함).
KIND_FAILURE = "failure"        # 실패 보고 회수(재시도 대상).
KIND_BLOCKED = "blocked"        # 차단 선언(blocking=차단됨) — Escalated + 정지 신호.


@dataclass
class InvokeRequest:
    """신규 실행 컨텍스트 기동 요청."""

    bundle: dict[str, Any]
    role: Any = None
    capability: Any = None
    model: Any = None
    policy: str = POLICY_INTERACTIVE
    workdir: str | None = None
    timeout: float | None = None
    # CP2 등 검증 디스패치에서 판정 대상·기준을 싣는다(선택).
    criteria: Any = None


@dataclass
class InvokeResult:
    """실행 컨텍스트 반환 — 상위로는 요약·상태·검증 결과 수준만 올라온다(SH-INV-8)."""

    kind: str
    # 완료 보고 5필드 수준(02 §3.2-C): artifacts·self_check·failures·open_questions·verify_basis.
    # CP2(Verifier) 반환의 경우 verdict/rework 를 담는다.
    completion: dict[str, Any] | None = None
    # 실패 보고(02 §3.2-D): reason·repro·attempted·lesson_candidate·blocking.
    failure: dict[str, Any] | None = None
    # run 데이터 백엔드에 남은 실행 상세에 대한 경량 참조(내용 아님).
    ref: Any = None

    def verdict_pass(self) -> bool:
        """CP2 반환의 verdict 소비 — Host 는 Verifier 가 낸 판정을 읽기만 한다(SH-INV-1)."""
        if self.completion is None:
            return False
        return self.completion.get("verdict") == "Pass"

    def rework(self) -> Any:
        if self.completion is None:
            return None
        return self.completion.get("rework")


class Invoker(ABC):
    """실행 컨텍스트 기동 계약. 구현체(Adapter)가 구체 실행 표면을 소유한다."""

    @abstractmethod
    def invoke(self, request: InvokeRequest) -> InvokeResult:
        """번들을 신규(격리된) 실행 컨텍스트에서 실행하고 보고를 회수한다."""
        raise NotImplementedError


def load_invoker(module_path: str, options: dict[str, Any] | None = None) -> Invoker:
    """config 의 모듈 경로 문자열로 invoker 구현체를 로드한다.

    module_path = "패키지.모듈:클래스" 또는 "패키지.모듈:factory". 콜론 뒤 이름을
    options(dict) 로 인스턴스화한다. 중립 코드에 구현체 이름을 하드코딩하지 않기 위한
    유일한 로딩 경로다.
    """
    if ":" not in module_path:
        raise ValueError("invoker 모듈 경로는 '모듈:이름' 형식이어야 한다: " + repr(module_path))
    mod_name, attr = module_path.split(":", 1)
    module = importlib.import_module(mod_name)
    target = getattr(module, attr)
    instance = target(**(options or {}))
    if not isinstance(instance, Invoker):
        raise TypeError("로드된 invoker 는 Invoker 를 구현해야 한다: " + repr(module_path))
    return instance
