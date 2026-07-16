"""Step — 실행 시점 자기완결 직렬화 단위 (프로토콜 §3.1).

Step = Task 필드(07 §3.2-B) + delegation 8필드(02 §3.2-B) + role/capability/model
슬롯 + (재시도 시) feedback 의 자기완결 직렬화다. 새 계약 요소 0 — 전 필드가
기존 계약에 실재한다(프로토콜 §3.1). 이 모듈은 그 구조의 로드·유효성 검사만 담당하며
의미 판단을 하지 않는다(SH-INV-1).

이 디렉터리(실행 호스팅 Module 경계)는 언어 중립 제약(C-3)의 대상이 아니다(설계 §4
표 행 2). 그러나 특정 실행 단위·provider 토큰은 코드·주석·테스트 어디에도 두지
않는다 — provider 호출은 invoker 추상 인터페이스로만 이뤄진다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# 위임 8필드 중 "하나라도 누락 시 착수 불가"의 필수 필드 (02 §3.2-B·INV-6·프로토콜 §3.1).
# task/from/to/constraints 는 유효성 게이트에서 제외한다(02 §3.2-B: constraints 선택,
# input/output/done/context 가 착수 가능성 판정 기준).
REQUIRED_DELEGATION_FIELDS = ("input", "output", "done", "context")

# Task 레벨 필수 필드 (07 INV-1: done + interfaceContract 없으면 디스패치 금지).
REQUIRED_TASK_FIELDS = ("done", "interfaceContract")


def _is_present(value: Any) -> bool:
    """값이 실질적으로 존재하는가 — None·빈 문자열·빈 컬렉션은 부재로 본다."""
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) > 0
    return True


@dataclass
class Step:
    """실행 시점 직렬화된 하나의 Step.

    필드 소유 정본(재사용):
      id · task · done · interfaceContract · ownedBoundary · dependsOn  -> 07 §3.2-B Task
      delegation(from·to·task·input·output·done·context·constraints)    -> 02 §3.2-B 위임 8필드
      role · capability · model                                          -> 슬롯(전달만·해석 안 함)
      feedback                                                           -> 재시도 시 주입(§5.1)
    """

    id: str
    task: str = ""
    done: Any = None
    interfaceContract: Any = None
    ownedBoundary: Any = field(default_factory=list)
    dependsOn: list[str] = field(default_factory=list)
    delegation: dict[str, Any] = field(default_factory=dict)
    # role/capability/model 슬롯 — Host 는 전달만 하고 해석하지 않는다(프로토콜 §3.1·설계 §3.9).
    role: Any = None
    capability: Any = None
    model: Any = None
    # feedback 은 Step 파일에 직렬화되지 않고 재시도 시 Host 가 로그에서 도출해 주입한다(§5.1).
    feedback: Any = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Step":
        """직렬화된 Step(자기완결 번들)을 로드한다. 형식(JSON 등)은 Adapter 소관이다."""
        if not isinstance(data, dict):
            raise TypeError("Step 직렬화는 매핑이어야 한다")
        if not _is_present(data.get("id")):
            raise ValueError("Step 에 id 가 없다 — 로드 불가")
        return cls(
            id=str(data["id"]),
            task=data.get("task", "") or "",
            done=data.get("done"),
            interfaceContract=data.get("interfaceContract"),
            ownedBoundary=data.get("ownedBoundary") or [],
            dependsOn=list(data.get("dependsOn") or []),
            delegation=dict(data.get("delegation") or {}),
            role=data.get("role"),
            capability=data.get("capability"),
            model=data.get("model"),
        )

    def missing_fields(self) -> list[str]:
        """진입 Sufficiency 판정(프로토콜 §6.1): 누락된 필수 필드 목록.

        비어 있으면 착수 가능(즉시 디스패치). 하나라도 있으면 디스패치 금지 —
        호출자(Host)가 scoped 질의 기록 + Escalated 로 넘긴다(§6.1). 이 함수는
        누락 사실만 보고하고 판단·해석하지 않는다(SH-INV-1).
        """
        missing: list[str] = []
        for name in REQUIRED_TASK_FIELDS:
            if not _is_present(getattr(self, name)):
                missing.append(name)
        for name in REQUIRED_DELEGATION_FIELDS:
            if not _is_present(self.delegation.get(name)):
                missing.append("delegation." + name)
        return missing

    def is_ready_to_dispatch(self) -> bool:
        return not self.missing_fields()

    def contract(self) -> dict[str, Any]:
        """Step Contract — Fresh Context 번들에 실리는 자기완결 계약 뷰(§3.2)."""
        return {
            "id": self.id,
            "task": self.task,
            "done": self.done,
            "interfaceContract": self.interfaceContract,
            "ownedBoundary": self.ownedBoundary,
            "dependsOn": list(self.dependsOn),
            "delegation": dict(self.delegation),
            "role": self.role,
            "capability": self.capability,
            "model": self.model,
        }
