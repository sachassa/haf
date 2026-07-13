"""Fresh Context 번들 조립 (프로토콜 §3.2).

각 Step 은 전체 컨텍스트를 상속하지 않고, 신규(격리된) 실행 컨텍스트에서 다음
번들만으로 실행된다:

    번들 = Step Contract + 확정 참조 + Memory 재료 + constraints + (재시도 시) feedback

- 확정 참조(R2 준수): input·interfaceContract 가 가리키는 확정된 산출물만. 동시
  진행 중인 미완성 산출물은 추측·인용하지 않는다(07 R2·INV-4).
- Host 의 Memory 직접 접근 금지(SH-INV-5): 이 모듈은 Memory Store·Index 에 접근하는
  코드 경로를 두지 않는다. Memory 재료는 오직 Step 의 delegation.context 에 위임자가
  실어 보낸 것만 번들에 들어온다(프로토콜 §3.2 경로 (a)).
"""

from __future__ import annotations

from typing import Any

from step import Step


def assemble_bundle(step: Step, feedback: Any = None) -> dict[str, Any]:
    """Step 하나의 Fresh Context 번들을 조립한다.

    반환은 직렬화 이전의 순수 데이터(매핑)다 — 직렬화 형식은 Adapter/invoker 소관이다.
    Host 는 이 데이터를 구성만 하고 의미 판단을 하지 않는다(SH-INV-1).
    """
    delegation = dict(step.delegation)
    bundle: dict[str, Any] = {
        # Step Contract (§3.1)
        "step_contract": step.contract(),
        # 확정 참조만 (R2) — 위임의 input 과 Task 의 interfaceContract.
        "confirmed_references": {
            "input": delegation.get("input"),
            "interfaceContract": step.interfaceContract,
        },
        # Memory 재료 — 위임자가 context 에 실어 보낸 것만. Host 는 Memory 에 직접
        # 접근하지 않는다(SH-INV-5). 회수·정책은 위임자/실행 단위 Consult 소관.
        "memory_material": delegation.get("context"),
        # constraints (선택).
        "constraints": delegation.get("constraints"),
        # feedback — 재시도 시에만(§5.1). 직전 실패 보고·CP2 재작업 지시 파생.
        "feedback": feedback,
        # 역할/모델 슬롯 — 전달만(§3.9).
        "role": step.role,
        "capability": step.capability,
        "model": step.model,
    }
    return bundle
