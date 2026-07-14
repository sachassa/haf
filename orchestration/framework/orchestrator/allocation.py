"""Dynamic Allocation + Model Selection Policy (05 §3.4·§3.5·PO-INV 6·8·판단 0).

이 모듈이 소유하는 것(05 §3.4·§3.5 — 본 Layer 신규 소유 계약의 실현):
  - AgentSpec — 실행 프로파일 레코드 7필드(05 §3.4 표). Role 층(04 §3.3 Expert Role)은
    재정의하지 않고 그 위의 실행 프로파일만 소유한다.
  - AgentSpecRegistry — 버전 있는 AgentSpec 데이터 로드 + capability 매칭(deterministic).
    레지스트리 실값의 **의미를 코드가 해석하지 않는다**(불투명 참조·PO-INV 6). match 는
    capability 선언까지만 소비하고 어느 실행 주체가 호스팅하는가(물리 매핑)는 해석하지
    않는다.
  - ModelSelectionPolicy — Policy as Data(05 §3.5). capability class → 모델 슬롯 매핑 +
    fallback 체인 + CP2 Verifier 독립 슬롯. select_model 은 순수·결정적이다.
  - Allocation — 위 둘을 묶어 orchestrator 가 소비하는 파사드(capability → 모델 슬롯).

hysteresis(05 §3.5): 모델 선택은 Step 직렬화 시점 1회 고정이다. select_model 은 순수
함수이므로 같은 입력 → 같은 슬롯(정상 재실행에서 재선택 없음). 슬롯을 바꾸는 재선택
트리거는 정확히 2건뿐이며(아래 RESELECTION_TRIGGER_KINDS), 그 판정은 orchestrator 가
이벤트 로그에서 수행한다(재선택 경로가 코드 구조로 2건에 한정됨).

판단 0(PO-INV 1): 이 모듈은 어느 capability 가 바람직한가를 판정하지 않는다 — capability
"제안"은 LLM step 이 산출하고 수용은 게이트가 소유하며(05 §3.4), 이 모듈은 정책 데이터의
deterministic 평가(매칭·모델 슬롯 선택)만 수행한다.

중립성(PO-INV 8): 이 모듈·스키마·테스트에 특정 provider·모델 고유명 토큰은 0건이다 —
모델 슬롯은 불투명 문자열이며 실값(실제 모델명)은 Adapter/프로젝트 정책 데이터 소관이다.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


# ==========================================================================
# 재선택 트리거 — 정확히 2건(05 §3.5 hysteresis). 이벤트 로그의 ref.kind 값으로만
# 재선택(fallback 차상위)을 유발한다. 그 외 어떤 경로도 모델 슬롯을 바꾸지 않는다.
#   (a) retry 한도 도달 후 재디스패치 = Step Host 의 retry-limit-exceeded 에스컬레이션.
#   (b) 명시적 모델 정책 이벤트.
# 정상 재실행(budget 내 재시도·크래시 재개)은 이 목록에 없으므로 재선택이 일어나지 않는다.
# ==========================================================================
TRIGGER_RETRY_LIMIT = "retry-limit-exceeded"   # (a) Step Host host.py 가 append 하는 ref.kind.
TRIGGER_MODEL_POLICY_EVENT = "model-policy-event"  # (b) 명시적 모델 정책 이벤트 ref.kind.
RESELECTION_TRIGGER_KINDS = (TRIGGER_RETRY_LIMIT, TRIGGER_MODEL_POLICY_EVENT)


def _present(value: Any) -> bool:
    """값이 실질적으로 존재하는가 — None·빈 문자열·빈 컬렉션은 부재로 본다(step.py 동형)."""
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) > 0
    return True


# ==========================================================================
# AgentSpec — 실행 프로파일 레코드 7필드 (05 §3.4 표)
# ==========================================================================
@dataclass
class AgentSpec:
    """실행 프로파일. Role(04 §3.3 Expert Role) 위의 버전 있는 데이터 레코드다.

    필드 소유 정본(05 §3.4):
      specId              -> AgentSpec 식별자.
      capabilitySelector  -> capability 매칭용 selector(문자열 "*"·정확 문자열·매처 dict).
      briefTemplateRef    -> brief 템플릿 참조(불투명 — 코드가 해석하지 않음).
      defaultConstraints  -> 기본 constraints(불투명 — Adapter/실행 단위 소비).
      toolPolicyClass     -> 도구 정책 클래스(불투명 정책 키).
      modelPolicyClass    -> 모델 정책 클래스(불투명 정책 키·Model Selection 입력 축).
      version             -> 버전(정수·단조). tie-break 에 쓰인다.

    briefTemplateRef·defaultConstraints·toolPolicyClass·modelPolicyClass 는 전부 **불투명
    참조**다 — 이 코드는 그 실값의 의미를 해석하지 않고 전달·키 사용만 한다(PO-INV 6).
    """

    specId: str
    capabilitySelector: Any = "*"
    briefTemplateRef: Any = None
    defaultConstraints: Any = None
    toolPolicyClass: Any = None
    modelPolicyClass: Any = None
    version: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "specId": self.specId,
            "capabilitySelector": self.capabilitySelector,
            "briefTemplateRef": self.briefTemplateRef,
            "defaultConstraints": self.defaultConstraints,
            "toolPolicyClass": self.toolPolicyClass,
            "modelPolicyClass": self.modelPolicyClass,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentSpec":
        if not isinstance(data, dict):
            raise TypeError("AgentSpec 직렬화는 매핑이어야 한다")
        if not _present(data.get("specId")):
            raise ValueError("AgentSpec 에 specId 가 없다")
        return cls(
            specId=str(data["specId"]),
            capabilitySelector=data.get("capabilitySelector", "*"),
            briefTemplateRef=data.get("briefTemplateRef"),
            defaultConstraints=data.get("defaultConstraints"),
            toolPolicyClass=data.get("toolPolicyClass"),
            modelPolicyClass=data.get("modelPolicyClass"),
            version=int(data.get("version", 1)),
        )


# ==========================================================================
# capability 매칭 — selector 매칭 + 특이도(specificity) (deterministic)
# ==========================================================================
def _selector_matches(selector: Any, capability: Any) -> bool:
    """selector 가 capability 를 매칭하는가.

    - "*"          -> 무엇이든 매칭(전역·특이도 0).
    - 문자열        -> capability(문자열)와 정확 일치.
    - dict(매처)    -> capability(dict)의 모든 제약 필드가 등가면 매칭.
    이 함수는 selector 실값의 **의미를 해석하지 않는다** — 구조적 등가 매칭만 한다(PO-INV 6).
    """
    if selector == "*":
        return True
    if isinstance(selector, dict):
        if not isinstance(capability, dict):
            return False
        return all(capability.get(k) == v for k, v in selector.items())
    return selector == capability


def _specificity(selector: Any) -> int:
    """selector 특이도(클수록 구체적). tie-break 의 "더 구체적 selector 우선"의 척도.

    "*"(전역) = 0 · dict 매처 = 제약 키 수 · 그 외(정확 문자열) = 1.
    """
    if selector == "*":
        return 0
    if isinstance(selector, dict):
        return len(selector)
    return 1


# tie-break 차원 — 데이터 오버라이드 가능(05 §9 OQ 8 의 S4 확정분). 기본값 = 더 구체적
# selector 우선("specificity") → 같으면 최고 version("version"). 두 차원 모두 값이 클수록
# 선호된다. 데이터가 순서를 바꾸면(예: ["version","specificity"]) 우선순위가 뒤바뀐다.
TIE_BREAK_SPECIFICITY = "specificity"
TIE_BREAK_VERSION = "version"
DEFAULT_TIE_BREAK = (TIE_BREAK_SPECIFICITY, TIE_BREAK_VERSION)
_TIE_BREAK_DIMS = (TIE_BREAK_SPECIFICITY, TIE_BREAK_VERSION)


class AgentSpecRegistry:
    """버전 있는 AgentSpec 데이터 로드 + capability 매칭(deterministic).

    match(capability) 는 capability 를 매칭하는 AgentSpec 중 tie-break 규칙으로 하나를
    고른다. 규칙 기본값(05 §9 OQ 8 S4 확정): **더 구체적인 selector 우선 → 같으면 최고
    version**. tie_break 데이터로 오버라이드 가능하다(차원 순서 재지정). 최종 안정성은
    specId 사전순으로 보장한다(진짜 동률에서도 결정적).

    레지스트리는 실값의 의미를 해석하지 않는다(불투명 참조·PO-INV 6) — 구조적 매칭·정렬만.
    """

    def __init__(
        self,
        specs: Any = None,
        *,
        tie_break: tuple[str, ...] | None = None,
    ) -> None:
        self.specs: list[AgentSpec] = list(specs or [])
        tb = tuple(tie_break) if tie_break else DEFAULT_TIE_BREAK
        for dim in tb:
            if dim not in _TIE_BREAK_DIMS:
                raise ValueError("알 수 없는 tie-break 차원: " + repr(dim))
        self.tie_break: tuple[str, ...] = tb

    def _rank(self, spec: AgentSpec) -> tuple[Any, ...]:
        """tie-break 정렬 키(내림차순 선호). 마지막에 specId 로 안정 결정성 보장.

        각 차원은 값이 클수록 선호되므로 max() 로 최선을 고른다. 진짜 동률(모든 차원 동일)은
        specId 사전순 **역**을 마지막 키로 두어 사전 앞선 specId 가 선택되게 한다(결정적).
        """
        dims = {
            TIE_BREAK_SPECIFICITY: _specificity(spec.capabilitySelector),
            TIE_BREAK_VERSION: spec.version,
        }
        key = tuple(dims[d] for d in self.tie_break)
        # specId 역순 정렬키(문자별 음수)로 max 시 사전 앞선 specId 채택 — 결정적 최종 tiebreak.
        stable = tuple(-ord(c) for c in spec.specId)
        return key + (stable,)

    def match(self, capability: Any) -> AgentSpec | None:
        """capability 를 매칭하는 AgentSpec 중 tie-break 규칙으로 하나 선택(없으면 None)."""
        candidates = [s for s in self.specs if _selector_matches(s.capabilitySelector, capability)]
        if not candidates:
            return None
        return max(candidates, key=self._rank)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "AgentSpecRegistry":
        data = data or {}
        specs = [AgentSpec.from_dict(s) for s in (data.get("specs") or [])]
        tie_break = data.get("tieBreak")
        return cls(specs, tie_break=tuple(tie_break) if tie_break else None)


# ==========================================================================
# ModelSelectionPolicy — Policy as Data (05 §3.5)
# ==========================================================================
@dataclass
class ModelSelectionPolicy:
    """모델 선택 정책 데이터 + 순수 선택 함수(05 §3.5).

    필드:
      slots          -> capability class → 기본 모델 슬롯(불투명 문자열).
      fallback_chain -> 티어 순서 리스트(약 → 강). fallback 은 base 슬롯을 이 체인에서
                        찾아 level 만큼 차상위로 진행한다(clamp).
      cp2_slot       -> CP2 Verifier 독립 모델 슬롯(OQ-SH-4·전역 기본). None = Host 가 상속.
      cp2_slots      -> capability class → CP2 모델 슬롯 오버라이드(선택·가법 확장). 05 §3.5
                        "CP2 = 독립 정책 행"의 데이터 확장 — 위험도별 CP2 차등을 정책 데이터로
                        실현한다(고위험 단위 CP2 = 상위 티어·저위험 = 약 티어). 매칭 class 가
                        없으면 cp2_slot(전역 기본)으로 폴백한다. 빈 dict(기본) = 전역 단일 거동
                        완전 보존(기존 테스트·baseline 무회귀). cp2_slot 은 default 로 존치한다.
      default_slot   -> slots 미매칭 capability class 의 fallback 기본값(선택).

    모델 슬롯은 전부 불투명 문자열이다 — 실제 모델명은 Adapter 정책 실값에만 등장한다(C-3).
    """

    slots: dict[str, str] = field(default_factory=dict)
    fallback_chain: list[str] = field(default_factory=list)
    cp2_slot: str | None = None
    default_slot: str | None = None
    cp2_slots: dict[str, str] = field(default_factory=dict)

    def select_model(self, capability_class: Any, level: int = 0) -> str | None:
        """capability class → 모델 슬롯(순수·결정적).

        level = 재선택 차수(0 = 직렬화 시점 기본 선택). level > 0 은 재선택 트리거
        (RESELECTION_TRIGGER_KINDS)가 그만큼 누적됐을 때만 orchestrator 가 전달한다.
        base 슬롯을 fallback_chain 에서 찾아 level 만큼 차상위로 진행(끝은 clamp)한다.
        base 가 체인 밖이면 재선택하지 않고 base 를 유지한다(정의되지 않은 fallback 추측 0).
        """
        base = self.slots.get(capability_class, self.default_slot)
        if level <= 0 or base is None:
            return base
        chain = self.fallback_chain or []
        if base not in chain:
            return base  # 체인 밖 → fallback 미정의 → 재선택 없음(추측 금지·O4).
        idx = chain.index(base)
        return chain[min(idx + level, len(chain) - 1)]

    def cp2_model(self) -> str | None:
        """CP2 Verifier 독립 모델 슬롯 전역 기본(없으면 None → Host 상속·OQ-SH-4 기본 거동)."""
        return self.cp2_slot

    def cp2_model_for(self, capability_class: Any) -> str | None:
        """capability class → CP2 모델 슬롯(오버라이드 우선·없으면 전역 cp2_slot 폴백·순수).

        cp2_slots 에 capability class 매칭이 있으면 그 오버라이드를, 없으면 cp2_slot(전역
        기본)을 반환한다. cp2_slots 가 비어 있으면 항상 cp2_slot 이다(전역 단일 거동 보존).
        """
        if capability_class is not None and capability_class in self.cp2_slots:
            return self.cp2_slots[capability_class]
        return self.cp2_slot

    def has_cp2_overrides(self) -> bool:
        """capability class 별 CP2 오버라이드가 하나라도 있는가(resolver 배선 여부 판정용)."""
        return bool(self.cp2_slots)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ModelSelectionPolicy":
        data = data or {}
        return cls(
            slots=dict(data.get("slots") or {}),
            fallback_chain=list(data.get("fallbackChain") or []),
            cp2_slot=data.get("cp2ModelSlot"),
            default_slot=data.get("defaultSlot"),
            cp2_slots=dict(data.get("cp2ModelSlots") or {}),
        )


# ==========================================================================
# Allocation — orchestrator 소비 파사드 (capability → 모델 슬롯·CP2 슬롯)
# ==========================================================================
@dataclass
class Allocation:
    """AgentSpecRegistry + ModelSelectionPolicy 파사드.

    orchestrator 는 이 파사드만 소비한다. model_for 는 capability → AgentSpec →
    modelPolicyClass(불투명 키) → 모델 슬롯의 결정적 선택이다. AgentSpec 의 물리 매핑은
    해석하지 않는다(PO-INV 6 — modelPolicyClass 는 정책 클래스 키로만 소비).
    """

    registry: AgentSpecRegistry
    model_policy: ModelSelectionPolicy

    def match(self, capability: Any) -> AgentSpec | None:
        return self.registry.match(capability)

    def model_for(self, capability: Any, level: int = 0) -> str | None:
        """capability → 모델 슬롯(level fallback 반영). 매칭 실패 시 None."""
        spec = self.registry.match(capability)
        if spec is None:
            return None
        # modelPolicyClass 는 불투명 정책 클래스 키로만 소비 — 물리 실행 주체 매핑은
        # 해석하지 않는다(PO-INV 6). 값이 없으면 모델 선택 불가 → None.
        model_class = spec.modelPolicyClass
        if model_class is None:
            return None
        return self.model_policy.select_model(model_class, level)

    def cp2_model(self) -> str | None:
        return self.model_policy.cp2_model()

    def cp2_model_for(self, capability: Any) -> str | None:
        """capability → CP2 모델 슬롯(오버라이드 우선·전역 cp2_slot 폴백).

        capability → AgentSpec → modelPolicyClass(불투명 키) → cp2_slots 오버라이드 조회.
        매칭 실패·class 부재 시 class=None 으로 전역 cp2_slot 을 반환한다(폴백). PO-INV 6 —
        modelPolicyClass 는 불투명 정책 키로만 소비.
        """
        spec = self.registry.match(capability)
        model_class = spec.modelPolicyClass if spec is not None else None
        return self.model_policy.cp2_model_for(model_class)

    def has_cp2_overrides(self) -> bool:
        return self.model_policy.has_cp2_overrides()

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "Allocation":
        """{registry: {...allocation_schema...}, modelSelection: {...model_selection_schema...}}.

        직렬화 형식(JSON 등)·물리 경로는 Adapter Binding 소관이며, 이 로더는 이미 파싱된
        매핑을 받는다(중립 코드에 형식·경로 토큰 0).
        """
        data = data or {}
        return cls(
            registry=AgentSpecRegistry.from_dict(data.get("registry")),
            model_policy=ModelSelectionPolicy.from_dict(data.get("modelSelection")),
        )

    @classmethod
    def from_file(cls, path: str) -> "Allocation":
        with open(path, "r", encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))
