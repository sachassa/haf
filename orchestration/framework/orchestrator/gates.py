"""Gate Policy 평가기 + 게이트 큐 파생 뷰 (05 §3.3·PO-INV 4·PO-INV 2·판단 0).

이 모듈이 소유하는 것(05 §3.3 본 Layer 신규 소유 계약):
  - gateKind 5종 어휘 + 심각도 전순서(auto_continue < review_required <
    approval_required < escalation_required < user_decision_required).
  - GatePolicyEntry / GatePolicy — 정책 데이터(Policy as Data)의 로드·평가.
    evaluate(target_descriptor) → gateKind 는 순수·결정적 함수다.
  - 게이트 단조성(PO-INV 4): 코드 소유 하한(floor) 테이블. 정책 데이터가 하한보다
    약한 값을 지정해도 effective_gate = max(floor, policy) 로 하한에 클램프된다
    (약화 불가·강화만). floor 는 **스키마가 아니라 코드가 소유**한다(정책 데이터로
    내릴 수 없다).
  - 게이트 이벤트 필드 관례의 단일 소유 — S2 의 `gate::` 관례를 정식화한다. 게이트
    요구 이벤트·해소 이벤트·리뷰/승인 마커는 03 §3.2-A 전이 이벤트 10필드를 **무수정
    재사용**하고 자유 형식 ref 필드에 gate_id/gateKind 를 싣는다(새 이벤트 스키마 0).
  - 게이트 큐 파생 뷰: pending_gates(events, policy) — 미해소 게이트 요구 이벤트의
    **파생 함수**다(mutable 큐 자료구조 아님·PO-INV 2).

판단 0(PO-INV 1): 이 모듈은 게이트의 의미(무엇을 승인할지)를 판정하지 않는다 —
정책 데이터·순수 함수로 gateKind 를 평가하고, 해소 적격성을 actor 클래스 매칭으로만
판정한다. 실제 검증/승인/결정은 리뷰 단위(Verifier)·Advisor·사용자가 소유한다.

특정 provider·모델·상류 Layer 고유명 토큰은 이 모듈 어디에도 두지 않는다(PO-INV 8).
actor·역할 문자열은 02 §3.2-A 역할 어휘·03 §3.2-A actor 어휘(Advisor/Verifier/human)
이며 provider 토큰이 아니다.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterable


# ==========================================================================
# gateKind 5종 어휘 + 심각도 전순서 (05 §3.3 표 — 어휘·순서 정본)
# ==========================================================================
GATE_AUTO_CONTINUE = "auto_continue"
GATE_REVIEW_REQUIRED = "review_required"
GATE_APPROVAL_REQUIRED = "approval_required"
GATE_ESCALATION_REQUIRED = "escalation_required"
GATE_USER_DECISION_REQUIRED = "user_decision_required"

# 심각도 오름차순(약 → 강). 인덱스가 곧 심각도 값이다(전순서).
GATE_KINDS = (
    GATE_AUTO_CONTINUE,          # 0 — 추가 게이트 0 (단 CP2 는 불변 하한·아래 주석)
    GATE_REVIEW_REQUIRED,        # 1 — CP2 외 추가 독립 리뷰(Verifier)
    GATE_APPROVAL_REQUIRED,      # 2 — 경계 CP3(Advisor 역할 승인)
    GATE_ESCALATION_REQUIRED,    # 3 — Escalated 정지·Advisor/사람 해소
    GATE_USER_DECISION_REQUIRED, # 4 — Escalated 정지·사용자 응답만 해소
)
_SEVERITY = {kind: index for index, kind in enumerate(GATE_KINDS)}

# 정지 게이트(Escalated 정지·해소 이벤트로만 재개). 나머지는 기계가 인라인 처리한다.
STOPPING_GATES = (GATE_ESCALATION_REQUIRED, GATE_USER_DECISION_REQUIRED)


def severity(gate_kind: str) -> int:
    """gateKind 의 심각도 전순서 값. 미지의 값은 ValueError(추측 금지)."""
    if gate_kind not in _SEVERITY:
        raise ValueError("알 수 없는 gateKind: " + repr(gate_kind))
    return _SEVERITY[gate_kind]


def max_gate(a: str, b: str) -> str:
    """두 gateKind 중 더 심각한 쪽. 게이트 단조성 클램프의 기본 연산(강화만)."""
    return a if severity(a) >= severity(b) else b


# ==========================================================================
# 게이트 단조성 하한(floor) — **코드 소유**(정책 데이터로 약화 불가·PO-INV 4)
# ==========================================================================
# (i) 실행 착수/Contract 지점 target class → user_decision_required 하한.
TARGETCLASS_EXECUTION_INITIATION = "execution_initiation"   # 04 §3.1-D Handoff 실행 착수
TARGETCLASS_CONTRACT_POINT = "contract_point"               # Contract Ready/Matured 지점
_FLOOR_USER_DECISION_CLASSES = (
    TARGETCLASS_EXECUTION_INITIATION,
    TARGETCLASS_CONTRACT_POINT,
)

# (ii) 03 §3.1-D 사람 개입 조건 2~5 대응 target → escalation_required 이상 하한.
#      (조건 1 재시도 한도 초과는 Step Host 가 이미 Escalated 정지로 소유한다.)
INTERVENTION_BLOCKING = "blocking"                     # 03 §3.1-D 조건 2 차단성 실패
INTERVENTION_DEPENDENCY_UNCERTAIN = "dependency_uncertain"  # 조건 3 의존 계약 미확정
INTERVENTION_ARCHITECTURE_CONFLICT = "architecture_conflict"  # 조건 4 상위 규약·Arch 충돌
INTERVENTION_ROLE_BOUNDARY_EXCEEDED = "role_boundary_exceeded"  # 조건 5 역할 경계 초과
_FLOOR_ESCALATION_CONDITIONS = (
    INTERVENTION_BLOCKING,
    INTERVENTION_DEPENDENCY_UNCERTAIN,
    INTERVENTION_ARCHITECTURE_CONFLICT,
    INTERVENTION_ROLE_BOUNDARY_EXCEEDED,
)

# ── CP2 는 floor 테이블에 없다(설계 의도). CP2 는 Step Host 가 policy·gate 무관하게
#    무조건 별도 디스패치하며(host.py `_dispatch_cp2`·SH-INV-4), 우회 경로 자체가
#    존재하지 않는다. 따라서 게이트 정책·floor 가 CP2 에 관여할 필요가 없다(README §CP2).


def floor(target_descriptor: dict[str, Any]) -> str:
    """이 target 의 **코드 소유 하한** gateKind(정책 데이터로 약화 불가).

    - targetClass 가 실행 착수/Contract 지점 → user_decision_required.
    - interventionCondition 이 03 §3.1-D 조건 2~5 → escalation_required.
    - 그 외 → auto_continue(하한 없음).

    순수 함수. descriptor 데이터만으로 결정된다.
    """
    descriptor = target_descriptor or {}
    if descriptor.get("targetClass") in _FLOOR_USER_DECISION_CLASSES:
        return GATE_USER_DECISION_REQUIRED
    if descriptor.get("interventionCondition") in _FLOOR_ESCALATION_CONDITIONS:
        return GATE_ESCALATION_REQUIRED
    return GATE_AUTO_CONTINUE


# ==========================================================================
# actor 클래스 기본값 — 기본값은 스키마(gate_policy_schema.json)가 default 로 소유하며,
# 정책 데이터 미지정 시 아래 중립 fallback 을 쓴다(중립 코드 하드코딩 최소화·03 §3.2-A
# actor 어휘: Advisor 역할·human). provider 토큰 아님(PO-INV 8).
# ==========================================================================
DEFAULT_USER_ACTOR_CLASS = "human"          # user_decision_required 를 해소할 수 있는 actor 클래스
DEFAULT_ESCALATION_RESOLVERS = ("Advisor", "human")  # escalation_required 해소 허용 actor 집합
DEFAULT_GATE_RAISER = "Advisor"             # 게이트 요구 이벤트를 append 하는 권위 actor


# ==========================================================================
# GatePolicyEntry / GatePolicy — 정책 데이터(Policy as Data)
# ==========================================================================
@dataclass
class GatePolicyEntry:
    """05 §3.3 GatePolicyEntry — {target, gateKind}.

    target 은 매처(dict)다 — descriptor 의 필드에 대한 등가 제약 집합. 05 §3.3 의
    target 차원(단위 유형 | 전이 | artifact class)에 대응한다:
      {"unitType": ...}      → 단위 유형 기본(tier 1)
      {"transition": ...}    → 명시 target(tier 2)
      {"artifactClass": ...} → 명시 target(tier 2)
      {} (또는 target 생략)   → 전역 기본(tier 0)
    gate 는 gateKind 5종 중 하나.
    """

    target: dict[str, Any] = field(default_factory=dict)
    gate: str = GATE_AUTO_CONTINUE

    def __post_init__(self) -> None:
        if self.gate not in _SEVERITY:
            raise ValueError("GatePolicyEntry.gate 는 gateKind 여야 한다: " + repr(self.gate))
        if not isinstance(self.target, dict):
            raise ValueError("GatePolicyEntry.target 은 매핑이어야 한다")


def _entry_tier(target: dict[str, Any]) -> int:
    """매칭 특이도 tier — 05 §3.3 우선순위(명시 target > 단위 유형 기본 > 전역 기본).

    tier 2(명시 target) — 전이(transition)·artifact class 를 지정한 엔트리.
    tier 1(단위 유형 기본) — 단위 유형(unitType)만 지정한 엔트리.
    tier 0(전역 기본) — 제약 없는 엔트리(target {}).
    """
    if "transition" in target or "artifactClass" in target:
        return 2
    if "unitType" in target:
        return 1
    return 0


def _matches(target: dict[str, Any], descriptor: dict[str, Any]) -> bool:
    """엔트리 target 의 모든 제약이 descriptor 와 등가면 매칭. 빈 target 은 전역 매칭."""
    for key, value in target.items():
        if descriptor.get(key) != value:
            return False
    return True


@dataclass
class GatePolicy:
    """게이트 정책 데이터 + deterministic 평가기(05 §3.3).

    evaluate 매칭 우선순위: 명시 target(tier 2) > 단위 유형 기본(tier 1) > 전역 기본
    (tier 0). 같은 tier 에서 복수 엔트리가 매칭하면 **가장 심각한 gateKind** 로
    tie-break 한다(안전측·단조성 보존 — 모호성에서 약한 게이트를 고르지 않는다).
    매칭 엔트리가 하나도 없으면 auto_continue(전역 미설정 = 무게이트).

    user_actor_class / escalation_resolvers 는 해소 적격성 판정용 actor 클래스 데이터다.
    """

    entries: list[GatePolicyEntry] = field(default_factory=list)
    user_actor_class: str = DEFAULT_USER_ACTOR_CLASS
    escalation_resolvers: tuple[str, ...] = DEFAULT_ESCALATION_RESOLVERS
    gate_raiser: str = DEFAULT_GATE_RAISER

    # --- 평가 -------------------------------------------------------------
    def evaluate(self, target_descriptor: dict[str, Any]) -> str:
        """target descriptor → gateKind(정책 데이터 부분·floor 미적용). 순수·결정적.

        floor(단조성 하한)와 합성한 실효 게이트는 effective_gate() 를 쓴다.
        """
        descriptor = target_descriptor or {}
        matching = [e for e in self.entries if _matches(e.target, descriptor)]
        if not matching:
            return GATE_AUTO_CONTINUE  # 전역 미설정 = 무게이트(S2 기본 거동 보존).
        top_tier = max(_entry_tier(e.target) for e in matching)
        candidates = [e for e in matching if _entry_tier(e.target) == top_tier]
        # tie-break: 같은 tier 복수 매칭 → 가장 심각한 gateKind(강화측·결정적).
        chosen = candidates[0].gate
        for e in candidates[1:]:
            chosen = max_gate(chosen, e.gate)
        return chosen

    # --- 해소 적격성 (actor 클래스 매칭·순수) -------------------------------
    def is_eligible_resolver(self, gate_kind: str, actor: Any) -> bool:
        """이 actor 가 이 정지 게이트를 해소할 자격이 있는가.

        - user_decision_required: actor 가 사용자 actor 클래스일 때만(확정 권위 보존).
        - escalation_required: actor 가 허용 resolver 집합에 속하면.
        비정지 게이트는 해소 이벤트 개념이 없으므로 False.
        """
        if gate_kind == GATE_USER_DECISION_REQUIRED:
            return actor == self.user_actor_class
        if gate_kind == GATE_ESCALATION_REQUIRED:
            return actor in self.escalation_resolvers
        return False

    # --- 로드 -------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "GatePolicy":
        data = data or {}
        entries = [
            GatePolicyEntry(
                target=dict(e.get("target") or {}),
                gate=e.get("gate", GATE_AUTO_CONTINUE),
            )
            for e in (data.get("entries") or [])
        ]
        resolvers = data.get("escalationResolvers")
        return cls(
            entries=entries,
            user_actor_class=data.get("userActorClass", DEFAULT_USER_ACTOR_CLASS),
            escalation_resolvers=(
                tuple(resolvers) if resolvers is not None else DEFAULT_ESCALATION_RESOLVERS
            ),
            gate_raiser=data.get("gateRaiser", DEFAULT_GATE_RAISER),
        )

    @classmethod
    def from_file(cls, path: str) -> "GatePolicy":
        with open(path, "r", encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))

    @classmethod
    def empty(cls) -> "GatePolicy":
        return cls(entries=[])


def effective_gate(target_descriptor: dict[str, Any], policy: GatePolicy) -> str:
    """실효 게이트 = max(floor(descriptor), policy.evaluate(descriptor)).

    게이트 단조성(PO-INV 4): 정책 데이터는 코드 소유 하한을 **강화만** 할 수 있고
    약화할 수 없다. 정책이 하한보다 약한 값을 지정해도 하한으로 클램프된다. 순수·결정적.
    """
    return max_gate(floor(target_descriptor), policy.evaluate(target_descriptor))


# ==========================================================================
# 게이트 이벤트 필드 관례 — S2 `gate::` 관례의 정식화(단일 소유)
#
# 게이트 이벤트는 새 스키마가 아니라 03 §3.2-A 전이 이벤트 10필드 그대로이며, step 이
# 아닌 별도 cycle 네임스페이스("gate::<gate_id>")를 써 Step Host 의 step 상태 파생에
# 간섭하지 않는다(cycle_id 가 step id 집합에 없으므로 derive_states 에 노출되지 않음).
# 자유 형식 ref 필드에 gate_id/gateKind 를 싣는다.
# ==========================================================================
GATE_CYCLE_PREFIX = "gate::"

REF_KIND_REQUIRED = "gate-required"    # 정지 게이트 요구(Escalated 정지) 이벤트
REF_KIND_RESOLVED = "gate-resolved"    # 정지 게이트 해소 이벤트(적격 actor 만 유효)
REF_KIND_REVIEW = "gate-review"        # review_required 처리 마커(추가 리뷰 디스패치 완료)
REF_KIND_APPROVAL = "gate-approval"    # approval_required 처리 마커(CP3 Advisor 디스패치 완료)


def gate_cycle_id(gate_id: Any) -> str:
    return GATE_CYCLE_PREFIX + str(gate_id)


def is_gate_event(event: dict[str, Any]) -> bool:
    cid = event.get("cycle_id")
    ref = event.get("ref")
    return (
        isinstance(cid, str)
        and cid.startswith(GATE_CYCLE_PREFIX)
        and isinstance(ref, dict)
        and ref.get("gate_id") is not None
    )


def gate_id_of(event: dict[str, Any]) -> Any:
    """게이트 이벤트에서 gate_id 추출(자유 형식 ref 필드 재사용)."""
    ref = event.get("ref")
    if isinstance(ref, dict):
        return ref.get("gate_id")
    return None


def gate_events_for(events: Iterable[dict[str, Any]], gate_id: Any) -> list[dict[str, Any]]:
    rows = [e for e in events if is_gate_event(e) and gate_id_of(e) == gate_id]
    rows.sort(key=lambda e: e.get("at", 0))
    return rows


def latest_requirement(events: Iterable[dict[str, Any]], gate_id: Any) -> dict[str, Any] | None:
    reqs = [
        e for e in gate_events_for(events, gate_id)
        if (e.get("ref") or {}).get("kind") == REF_KIND_REQUIRED
    ]
    return reqs[-1] if reqs else None


def has_requirement(events: Iterable[dict[str, Any]], gate_id: Any) -> bool:
    return latest_requirement(events, gate_id) is not None


def has_settlement(events: Iterable[dict[str, Any]], gate_id: Any, *ref_kinds: str) -> bool:
    """이 gate_id 에 대해 지정 ref.kind 마커 이벤트가 실재하는가(리뷰/승인 처리 완료 판정)."""
    wanted = set(ref_kinds)
    return any(
        (e.get("ref") or {}).get("kind") in wanted
        for e in gate_events_for(events, gate_id)
    )


def latest_marker_verdict(
    events: Iterable[dict[str, Any]],
    gate_id: Any,
    ref_kind: str,
) -> Any:
    """지정 마커(리뷰/승인)의 최신 verdict **status** 를 반환한다(내용 아님·상태만).

    approval/review 마커의 ref.verdict 는 `{verdict, ref}` 경량 요약(_verdict_summary)이다.
    이 함수는 그 verdict status 만 꺼낸다 — 판정 내용을 해석하지 않는다(PO-INV 1). 마커가
    없으면 None(미디스패치·미처리). 소비 측(orchestrator)이 이 status 로만 분기한다
    (host.py verdict_pass 동형 — status 소비이지 내용 판단 아님).
    """
    rows = [
        e for e in gate_events_for(events, gate_id)
        if (e.get("ref") or {}).get("kind") == ref_kind
    ]
    if not rows:
        return None
    verdict = (rows[-1].get("ref") or {}).get("verdict")
    if isinstance(verdict, dict):
        return verdict.get("verdict")
    return verdict


def is_resolved(
    events: Iterable[dict[str, Any]],
    gate_id: Any,
    gate_kind: str,
    policy: GatePolicy,
) -> bool:
    """정지 게이트가 **적격 actor** 의 해소 이벤트로 해소되었는가(파생 판정).

    요구 이벤트가 먼저 실재해야 하며, 그 이후(at 순서)에 등장한 해소 이벤트의 actor 가
    정책 데이터 기준 적격일 때만 해소로 인정한다. 부적격 actor 의 해소 시도는 무효다
    (여전히 pending). 순수 함수(events·policy 만으로 결정).
    """
    req = latest_requirement(events, gate_id)
    if req is None:
        return False
    since = req.get("at", 0)
    for e in gate_events_for(events, gate_id):
        ref = e.get("ref") or {}
        if ref.get("kind") != REF_KIND_RESOLVED:
            continue
        if e.get("at", 0) <= since:
            continue  # 요구 이전의 해소 이벤트는 이 요구를 해소하지 않는다.
        if policy.is_eligible_resolver(gate_kind, e.get("actor")):
            return True
    return False


def pending_gates(
    events: Iterable[dict[str, Any]],
    policy: GatePolicy,
) -> list[dict[str, Any]]:
    """게이트 큐 파생 뷰 — 미해소 정지 게이트 요구의 목록(mutable 큐 아님·PO-INV 2).

    같은 (events, policy) → 같은 pending 목록(결정적·PO-INV 3 동형). 순서는
    (since, gate_id) 안정 정렬. 항목: {gate_id, gateKind, target, scoped_question, since}.
    """
    events = list(events)
    result: list[dict[str, Any]] = []
    seen: set[Any] = set()
    for e in events:
        ref = e.get("ref") or {}
        if not is_gate_event(e) or ref.get("kind") != REF_KIND_REQUIRED:
            continue
        gid = ref.get("gate_id")
        if gid in seen:
            continue
        seen.add(gid)
        gate_kind = ref.get("gateKind")
        if is_resolved(events, gid, gate_kind, policy):
            continue
        req = latest_requirement(events, gid)
        req_ref = req.get("ref") or {}
        result.append({
            "gate_id": gid,
            "gateKind": gate_kind,
            "target": req_ref.get("target"),
            "scoped_question": req_ref.get("scoped_question"),
            "since": req.get("at"),
        })
    result.sort(key=lambda g: (g["since"] if g["since"] is not None else 0, str(g["gate_id"])))
    return result


# ==========================================================================
# 게이트 이벤트 append 헬퍼 — 03 10필드 무수정 재사용(단일 소유). log = events.EventLog.
# ==========================================================================
def append_gate_requirement(
    log: Any,
    gate_id: Any,
    gate_kind: str,
    *,
    target: Any = None,
    scoped_question: Any = None,
    actor: str = DEFAULT_GATE_RAISER,
) -> dict[str, Any]:
    """정지 게이트 요구 이벤트 append(Escalated 정지 신호). outcome=escalated."""
    return log.append(
        cycle_id=gate_cycle_id(gate_id),
        from_stage=None,
        to_stage="Consult",
        trigger="에스컬레이션",
        outcome="escalated",
        actor=actor,
        retry_count=0,
        ref={
            "kind": REF_KIND_REQUIRED,
            "gate_id": gate_id,
            "gateKind": gate_kind,
            "target": target,
            "scoped_question": scoped_question,
        },
    )


def append_gate_resolution(
    log: Any,
    gate_id: Any,
    gate_kind: str,
    *,
    actor: str,
) -> dict[str, Any]:
    """정지 게이트 해소 이벤트 append. 적격성은 소비 측(is_resolved)이 판정한다."""
    return log.append(
        cycle_id=gate_cycle_id(gate_id),
        from_stage="Consult",
        to_stage="Complete",
        trigger="완료 조건 충족",
        outcome="pass",
        actor=actor,
        retry_count=0,
        ref={"kind": REF_KIND_RESOLVED, "gate_id": gate_id, "gateKind": gate_kind},
    )


def append_review_marker(
    log: Any,
    gate_id: Any,
    gate_kind: str,
    verdict: Any,
    *,
    actor: str = "Verifier",
) -> dict[str, Any]:
    """review_required 처리 마커 append(추가 독립 리뷰 디스패치 완료·멱등 판정용)."""
    return log.append(
        cycle_id=gate_cycle_id(gate_id),
        from_stage="Verify",
        to_stage="Complete",
        trigger="완료 조건 충족",
        outcome="pass",
        actor=actor,
        retry_count=0,
        ref={"kind": REF_KIND_REVIEW, "gate_id": gate_id, "gateKind": gate_kind, "verdict": verdict},
    )


def append_approval_marker(
    log: Any,
    gate_id: Any,
    gate_kind: str,
    verdict: Any,
    *,
    actor: str = "Advisor",
) -> dict[str, Any]:
    """approval_required 처리 마커 append(CP3 Advisor 디스패치 완료·멱등 판정용)."""
    return log.append(
        cycle_id=gate_cycle_id(gate_id),
        from_stage="Verify",
        to_stage="Complete",
        trigger="완료 조건 충족",
        outcome="pass",
        actor=actor,
        retry_count=0,
        ref={"kind": REF_KIND_APPROVAL, "gate_id": gate_id, "gateKind": gate_kind, "verdict": verdict},
    )
