"""Project Orchestrator — 판단하지 않는 기계 구동자 (05 §2·§3.2·§4).

Project Orchestrator 는 상류 산출물을 인수해 프로젝트 완료까지 lifecycle 을 조율하되,
단일 run 의 무인 실행은 UAHF Step Host 를 substrate 로 **라이브러리 무수정 재사용**
하여 위임한다(05 §0·§2.2). 자신은 run/작업 단위 입도로 그래프 진화·게이트 근거 검증을
deterministic 하게 구동할 뿐 의미 판단을 하지 않는다(PO-INV 1).

이 모듈이 소유하는 강제:
  - 판단 0 (PO-INV 1): InvokeResult.kind·이벤트·순수 검증 함수 결과로만 분기하고,
    내용 판정 로직을 두지 않는다.
  - 이중 원장 append-only (PO-INV 2): revision 원장·step 이벤트 로그 모두 append-only.
    현재 그래프·상태는 전부 파생 함수(fold·derive_states).
  - 결정적 재개 (PO-INV 3): (revision 원장, 이벤트 로그) 쌍 재생 → 동일 그래프 →
    동일 재개 지점. active_graph·ready_set 은 두 원장의 순수 함수.
  - revision 근거 필수 (PO-INV 5): 게이트 이벤트가 이벤트 로그에 실재해야 revision 을
    수용한다. orchestrator 는 실재 검증만 하고 게이트 정책을 평가하지 않는다(S3 소관).
  - Step/이벤트 계약 재사용: 새 Step 클래스·새 이벤트 스키마·새 상태 열거 창설 0 —
    step.py Step·events.py 로그/상태를 그대로 쓴다(stephost_bridge 경유).

특정 provider·모델·상류 Layer 고유명 토큰은 이 모듈 어디에도 두지 않는다(PO-INV 8).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from typing import Any

from allocation import Allocation, _present
from artifacts import (
    ArtifactCapturingInvoker,
    ArtifactDeclarationStore,
    derive_registry,
    find_valid_cp2_evidence,
    hash_file,
    resolve_references,
)
from gates import (
    GATE_APPROVAL_REQUIRED,
    GATE_AUTO_CONTINUE,
    GATE_ESCALATION_REQUIRED,
    GATE_REVIEW_REQUIRED,
    REF_KIND_APPROVAL,
    REF_KIND_RESOLVED,
    REF_KIND_REVIEW,
    REVIEW_MODE_EVIDENCE_REUSE,
    STOPPING_GATES,
    GatePolicy,
    append_approval_marker,
    append_gate_requirement,
    append_review_marker,
    effective_gate,
    has_requirement,
    has_settlement,
    is_resolved,
    latest_eligible_resolution,
    latest_marker_verdict,
    latest_requirement,
    pending_gates,
    resolution_response,
)
from revision import RevisionLedger, RevisionRejected, fold
from stephost_bridge import (
    DEFAULT_RETRY_LIMIT,
    EventLog,
    EventStore,
    Invoker,
    InvokeRequest,
    PASSED,
    POLICY_INTERACTIVE,
    ROLE_ADVISOR,
    ROLE_VERIFIER,
    Step,
    StepHost,
)

# revision 근거 부재 거부 사유(PO-INV 5). 07 §3.1-A Decompose 코드가 아니라 인과 근거
# (게이트 이벤트 실재) 위반이므로 별도 사유로 구분한다.
REASON_UNGROUNDED_REVISION = "UngroundedRevision"

# 진행 보장 안전판 — epoch 무한 성장 방지(설계상 revision 은 유한·append-only).
DEFAULT_MAX_EPOCHS = 1000

# Host 정지 사유 중 "Escalated 잔존"(host.py STOP_ESCALATED). 이 값과의 동등 비교만 한다.
STOP_REASON_ESCALATED = "escalated"

# 실행 에스컬레이션 게이트의 gate_id 접미사 — 단위 경계 게이트(_gate_id_for)와 **비충돌**
# 하도록 같은 단위 id 위에 구분자를 덧붙인다(결정적·재개 간 안정). 단위 경계 게이트
# "gate-unit-<id>" 는 그대로 두고 실행 에스컬레이션은 "gate-unit-<id>::exec-escalation".
ESCALATION_GATE_SUFFIX = "::exec-escalation"

# 실행 에스컬레이션 게이트 요구의 원인 표기(scoped_question.cause — 자유 형식 데이터).
CAUSE_EXECUTION_ESCALATED = "execution_escalated"

# 게이트 해소로 단위를 재작업 되돌림할 때 step 사이클에 남기는 이벤트의 ref.kind.
# 03 §3.2-A 10필드 무수정 — 자유 형식 ref 안에서만 구분한다(새 필드 창설 0).
REF_KIND_GATE_REWORK = "gate-rework"

# 위 되돌림 이벤트의 trigger(03 전이 사유 어휘 "재작업 되돌림"의 사유 표기).
TRIGGER_GATE_REWORK = "재작업 되돌림(에스컬레이션 해소)"

# verdict 어휘(06 §3.2-C — Pass 판정). provider·모델 토큰이 아니라 검증 판정 어휘다.
# host.py 의 verdict_pass 가 소비하는 것과 동일 어휘이며, orchestrator 의 CP3 status
# 소비도 이 값과의 동등 비교만 한다(내용 판정 0·PO-INV 1).
VERDICT_PASS = "Pass"

# 단위(Task)의 선택 실행 예산 키(초·양의 정수). 07 Task 는 개방 데이터이므로 필수 키가 아니며,
# 부재 시 전역 timeout(Orchestrator.timeout) 이 그대로 쓰인다(하위호환·D-T7).
TASK_TIMEOUT_KEY = "timeout"


class UnitTimeoutInvoker:
    """Invoker 래퍼 — 단위별 실행 예산(timeout)을 InvokeRequest 에 재기입한다(D-T3).

    전역 timeout 하나로는 규모가 크게 다른 단위를 같은 예산에 묶는다. 이 데코레이터는
    `{단위 id: timeout}` 맵을 들고 요청 번들의 `step_contract.id` 가 맵에 있으면 그 값으로
    요청을 재기입한다 — 매칭이 없으면 **원 요청 객체 그대로** 통과시킨다(래핑 무해).

    순수 재기입: 원본 request 를 변조하지 않고 `dataclasses.replace` 로 새 요청을 만든다
    (호출부가 들고 있는 객체의 timeout 은 불변). 판단 0(PO-INV 1) — 값의 타당성은 상류
    검증 게이트가 소유하고 여기서는 기계 재기입만 한다.

    인터페이스 보존: `invoke` 만 가로채고 그 밖의 속성은 `__getattr__` 로 **투과**한다
    (HeartbeatInvoker·ArtifactCapturingInvoker 선례 동형 — `invoke_count` 등 관측 수치 왜곡 0).
    """

    def __init__(self, inner: Any, timeouts: dict[Any, Any]) -> None:
        self._inner = inner
        self._timeouts = dict(timeouts)

    def __getattr__(self, name: str) -> Any:
        # 래퍼 자체 속성(_inner/_timeouts/invoke)은 정상 조회로 해결되므로 여기 오지 않는다.
        # object.__getattribute__ 로 꺼내 __init__ 이전 접근 시 무한재귀를 막는다.
        return getattr(object.__getattribute__(self, "_inner"), name)

    def invoke(self, request: Any) -> Any:
        return self._inner.invoke(self._retarget(request))

    def _retarget(self, request: Any) -> Any:
        """단위 timeout 이 있으면 그 값으로 재기입한 새 요청을, 없으면 원 요청을 반환한다."""
        bundle = getattr(request, "bundle", None)
        if not isinstance(bundle, dict):
            return request
        contract = bundle.get("step_contract")
        if not isinstance(contract, dict):
            return request
        step_id = contract.get("id")
        if not isinstance(step_id, str):
            return request
        value = self._timeouts.get(step_id)
        if value is None:
            return request
        return replace(request, timeout=value)


@dataclass
class OrchestrationResult:
    """orchestration run 종료 결과 — 상위로의 요약(PO-INV 8·SH-INV-8 동형)."""

    status: str  # "completed" | "stopped" | "halted"
    graph_task_ids: list[str] = field(default_factory=list)
    states: dict[str, str] = field(default_factory=dict)
    stop_reason: str | None = None  # "escalated"(Step Host) | "gate"(정지 게이트)
    stopped_tasks: list[str] = field(default_factory=list)
    epochs: int = 0
    # 정지 게이트(escalation/user_decision)로 정지 시 미해소 게이트 큐 파생 뷰(05 §3.3).
    pending_gates: list[dict[str, Any]] = field(default_factory=list)

    @property
    def stopped(self) -> bool:
        return self.status == "stopped"

    @property
    def completed(self) -> bool:
        return self.status == "completed"


class ProjectOrchestrator:
    """(revision 원장, step 이벤트 store, invoker)를 구동하는 중립 Orchestrator."""

    def __init__(
        self,
        ledger: RevisionLedger,
        event_store: EventStore,
        invoker: Invoker,
        *,
        retry_limit: int = DEFAULT_RETRY_LIMIT,
        policy: str = POLICY_INTERACTIVE,
        workdir: str | None = None,
        timeout: float | None = None,
        stop_handler: Any = None,
        gate_policy: GatePolicy | None = None,
        allocation: Allocation | None = None,
        artifact_store: ArtifactDeclarationStore | None = None,
        run_id: Any = None,
    ) -> None:
        self.ledger = ledger
        # step 이벤트 store 는 Step Host 와 **공유**한다 — 두 원장이 아니라 이중 원장
        # 중 하나(step 이벤트 로그)를 Host 와 같은 백엔드로 본다(PO-INV 2·3).
        self.event_store = event_store
        self.invoker = invoker
        self.log = EventLog(event_store)
        self.retry_limit = retry_limit
        # policy = Autonomy Policy 3값(도구 승인 축·step-host §6.2). **게이트 축과 직교**
        # (PO-INV 4·05 §3.3) — 아래 게이트 **결정** 로직(gateKind 평가·must_stop·해소 적격성)은
        # self.policy 를 참조하지 않는다(서브단위 실행 InvokeRequest 에는 동일 autonomy 를 전달만 한다).
        # 따라서 unrestricted 에서도 정지 게이트는 그대로 정지한다.
        self.policy = policy
        self.workdir = workdir
        self.timeout = timeout
        self.stop_handler = stop_handler
        # gate_policy 미지정(None) 시 게이트 처리를 하지 않는다 — S2 거동 완전 보존.
        self.gate_policy = gate_policy
        # allocation 미지정(None) 시 슬롯 채움을 하지 않는다 — S2·S3 거동 완전 보존.
        # 지정 시 Step 직렬화 시점에 미지정 슬롯(role/model)만 채운다(명시값 우선·05 §3.4·§3.5).
        self.allocation = allocation
        # artifact_store 미지정(None) 시 산출물 포집을 하지 않는다 — S2~S4 거동 완전 보존.
        # 지정 시 실행 invoker 를 ArtifactCapturingInvoker 로 감싸 Worker 완료 보고의
        # artifacts 를 append-only 선언 원장에 포집한다(05 §3.6). 레지스트리는 그 선언과
        # 이벤트 로그에서 파생될 뿐 별도 mutable 상태로 저장되지 않는다(제2 진리원천 아님).
        self.artifact_store = artifact_store
        self.run_id = run_id

    # ------------------------------------------------------------------
    # 게이트 근거 실재 검증 (PO-INV 5 — 실재 검증만·판단 0)
    # ------------------------------------------------------------------
    @staticmethod
    def _event_gate_id(event: dict[str, Any]) -> Any:
        """이벤트에서 게이트 식별자를 추출한다.

        게이트 승인 이벤트는 새 스키마가 아니라 03 전이 이벤트(events.py 10필드) 그대로
        이며, 자유 형식 `ref` 필드에 게이트 식별자를 싣는다(ref = {"gate_id": ...}).
        orchestrator 는 이 식별자의 실재만 확인하고 게이트 의미를 해석하지 않는다.
        """
        ref = event.get("ref")
        if isinstance(ref, dict):
            return ref.get("gate_id")
        return None

    def _event_grounds_gate(self, event: dict[str, Any], gate_ref: Any) -> bool:
        """이 이벤트가 gate_ref 를 근거지을 자격이 있는가(PO-INV 5 + OQ-PO-B5 actor 재검증).

        기본 = 실재 검증(PO-INV 5): outcome == "pass" 이고 gate_id 가 일치하면 근거로
        인정한다. 게이트 통과(승인·해소)만 revision 을 근거지을 수 있다 — S3 게이트 요구
        이벤트(outcome == "escalated")는 미해소이므로 근거가 아니다(요구만으로 그래프 변경 0).

        OQ-PO-B5 강화(2026-07-19·해소): 매칭 pass 이벤트가 **정지 게이트 해소로 자신을
        선언**하고(ref.kind == REF_KIND_RESOLVED 그리고 ref.gateKind ∈ STOPPING_GATES)
        self.gate_policy 가 존재하면, 그 해소 actor 가 정책상 적격일 때만
        (gate_policy.is_eligible_resolver) 근거로 인정한다. 05 §3.3 확정 권위를 엔진 근거
        검증에 반영한다 — user_decision_required 는 사용자 actor 클래스(userActorClass)의
        해소 이벤트만·escalation_required 는 허용 resolver 집합(escalationResolvers)의 해소
        이벤트만 승격 근거가 된다. 부적격 actor 의 pass 해소 이벤트는 로그에 남아도(append-only)
        승격 근거가 되지 못한다.

        거동 보존 3면(불가침):
          (a) 레거시 이벤트(ref.kind == "gate"·gateKind 부재·S2 관례) → 실재-만 검증(강화
              무적용). 정지 게이트 해소 선언이 아니므로 else 분기로 근거 인정.
          (b) 비정지 gateKind(review_required/approval_required 등)를 실은 gate-resolved
              이벤트 → 실재-만 검증. is_eligible_resolver 는 비정지 gateKind 에 항상 False 라
              일괄 적용 시 test_artifacts 의 approval_required 근거 rework 패턴이 깨진다 —
              적용 범위를 STOPPING_GATES 로 한정하는 이유다.
          (c) self.gate_policy is None(S2 조립·게이트 처리 0 원칙) → 실재-만 검증(적격성
              판정 불가·게이트 정책 부재 시 근거 실재만으로 수용).
        """
        if event.get("outcome") != "pass":
            return False
        if self._event_gate_id(event) != gate_ref:
            return False
        ref = event.get("ref")
        if isinstance(ref, dict):
            gate_kind = ref.get("gateKind")
            if (
                ref.get("kind") == REF_KIND_RESOLVED
                and gate_kind in STOPPING_GATES
                and self.gate_policy is not None
            ):
                # 정지 게이트 해소 선언 + 정책 존재 → actor 적격성까지 요구(OQ-PO-B5).
                return self.gate_policy.is_eligible_resolver(gate_kind, event.get("actor"))
        # 레거시·비정지·정책 부재 → 실재-만 검증(거동 보존 3면).
        return True

    def _gate_event_exists(self, gate_ref: Any) -> bool:
        """revision 을 근거짓는 게이트 **통과** 이벤트가 자격 있게 실재하는가(PO-INV 5·OQ-PO-B5).

        각 이벤트를 `_event_grounds_gate` 로 판정한다 — 정지 게이트 해소를 선언하는 pass
        이벤트는 적격 actor 일 때만 근거가 되고, 그 외(레거시·비정지·정책 부재)는 종전대로
        실재-만 검증이다(거동 보존 3면·해당 메서드 docstring).

        `accept_revision`(수용 시점)과 `_grounded_revisions`(재개 fold 필터) 양쪽에서 쓰이므로
        이 강화는 **수용 시점과 재개 시점 모두**에 걸린다 — 부적격-근거 revision 은 수용도
        거부되고, 우회 append 되어 원장에 있더라도 fold 에서 배제된다(방어적 이중화의 엔진 측
        완성).
        """
        if not gate_ref:
            return False
        return any(
            self._event_grounds_gate(e, gate_ref)
            for e in self.event_store.read_all()
        )

    # ------------------------------------------------------------------
    # revision 수용 — 게이트 근거 실재 검증 후 원장 append (05 §3.2 ①·PO-INV 5)
    # ------------------------------------------------------------------
    def accept_revision(
        self,
        kind: str,
        payload: dict[str, Any],
        *,
        proposingStepRef: str,
        gateEventRef: Any,
    ) -> Any:
        """게이트 통과 이벤트가 이벤트 로그에 append 된 뒤에만 revision 을 수용한다.

        게이트 이벤트가 실재하지 않으면 RevisionRejected(UngroundedRevision) 로 거부하고
        원장을 건드리지 않는다(근거 없는 그래프 변경 0·PO-INV 5). 게이트 승인 이벤트 자체는
        외부(상위/드라이버)가 append 하는 데이터이며, orchestrator 는 실재 검증만 한다
        (판단 0 — 게이트 정책 평가 엔진은 S3 소관).
        """
        if not self._gate_event_exists(gateEventRef):
            raise RevisionRejected(REASON_UNGROUNDED_REVISION, None)
        basis = {"proposingStepRef": proposingStepRef, "gateEventRef": gateEventRef}
        # 구조 검증(스키마·순환·중첩)은 원장 append 에 내장(순수 함수·07 코드).
        return self.ledger.append(kind, payload, basis)

    # ------------------------------------------------------------------
    # 파생 뷰 — 그래프·재개 지점 (전부 두 원장의 순수 함수·PO-INV 3)
    # ------------------------------------------------------------------
    def active_graph(self) -> dict[str, Any]:
        """게이트 근거가 실재하는 revision 만 접어(fold) 만든 현재 그래프.

        방어적 PO-INV 5: gateEventRef 가 이벤트 로그에 실재하지 않는 revision 은
        그래프에 반영하지 않는다. accept_revision 이 이미 근거를 보장하지만, 이 fold
        필터가 근거를 fold 수준에서도 강제하므로 재개 시 근거 실재를 재확인한다.
        """
        return fold(self._grounded_revisions(), self.ledger.initial_graph)

    def _grounded_revisions(self) -> list[Any]:
        """게이트 근거(gateEventRef)가 이벤트 로그에 실재하는 revision 만(PO-INV 5 필터).

        active_graph 의 fold 입력과 동일 필터다 — 그래프에 실제 반영된 revision 집합. review
        evidence 재사용 판정(rule (b))도 이 집합만 본다(미grounded revision 은 그래프 무영향).
        """
        return [
            r for r in self.ledger.all()
            if self._gate_event_exists(r.basis.get("gateEventRef"))
        ]

    def _build_steps(self, graph: dict[str, Any]) -> list[Step]:
        """현재 그래프 Task 를 기존 step.py Step 으로 직렬화한다(새 Step 클래스 창설 0).

        allocation 이 지정되면 Step 직렬화 시점에 미지정 슬롯(role/model)을 채운다
        (명시값 우선·05 §3.4·§3.5). 채움은 결정적 파생이므로 같은 두 원장 → 같은 슬롯이다
        (PO-INV 3 — 별도 mutable 기록 없이 원장에서 파생). allocation 미지정이면 무처리
        (S2·S3 거동 보존).
        """
        steps = [Step.from_dict(task) for task in graph.get("tasks") or []]
        if self.allocation is not None:
            for step in steps:
                self._fill_slots(step)
        return steps

    # ------------------------------------------------------------------
    # 할당·모델 슬롯 채움 (05 §3.4·§3.5·PO-INV 6 — 불투명 전달·hysteresis)
    # ------------------------------------------------------------------
    def _fallback_level(self, step_id: str) -> int:
        """이 step 의 재선택 차수 = 재선택 트리거 이벤트 누적 수(05 §3.5 hysteresis).

        재선택 트리거는 정확히 2건뿐이며(allocation.RESELECTION_TRIGGER_KINDS) 이 함수가
        이벤트 로그에서 그 개수만 센다 — 그 외 어떤 경로도 모델 슬롯을 바꾸지 않는다(코드
        구조로 2건 한정 확인 가능). 정상 재시도(budget 내 fail)·크래시 재개는 트리거가
        아니므로 계수되지 않는다(재선택 없음). 순수 함수(이벤트 로그 파생·판단 0).
        """
        from allocation import RESELECTION_TRIGGER_KINDS

        count = 0
        for e in self.event_store.read_all():
            if e.get("cycle_id") != step_id:
                continue
            ref = e.get("ref")
            if isinstance(ref, dict) and ref.get("kind") in RESELECTION_TRIGGER_KINDS:
                count += 1
        return count

    def _fill_slots(self, step: Step) -> None:
        """미지정 role/model 슬롯을 채운다(명시값 우선·불투명 전달·PO-INV 6).

        - role: 미지정이면 위임 8필드의 to(수임 역할·02 §3.2-B)를 슬롯에 반영(물리 매핑 0).
        - model: 미지정이면 capability → AgentSpec → modelPolicyClass(불투명 키) → 모델
          슬롯(재선택 차수 fallback 반영). 이미 채워진 슬롯은 존중한다(명시값 우선).
        capability 슬롯은 매칭 입력이며 그대로 둔다. AgentSpec 의 물리 매핑은 해석하지
        않는다(PO-INV 6 — modelPolicyClass 를 불투명 정책 키로만 소비).
        """
        if not _present(step.role):
            to_role = (step.delegation or {}).get("to")
            if _present(to_role):
                step.role = to_role
        if not _present(step.model) and _present(step.capability):
            level = self._fallback_level(step.id)
            slot = self.allocation.model_for(step.capability, level)
            if slot is not None:
                step.model = slot

    def _effective_invoker(self) -> Any:
        """실행 invoker — artifact_store 지정 시 산출물 포집 래퍼로 감싼다(05 §3.6).

        미지정(None)이면 self.invoker 그대로(래핑 0·S2~S4 거동 바이트 동일 보존). 래퍼는
        inner.invoke 반환을 변경하지 않고 투명 통과시키며 Worker 완료 보고의 artifacts 만
        선언 원장에 포집한다(부작용·판단 0). read_only 파생 경로에서는 invoke 가 호출되지
        않으므로 래핑이 무해하다(포집 없음).

        그 위에 단위별 timeout 재기입 래퍼를 **최외곽**으로 얹는다(맵 공집합이면 래핑 0 —
        기존 반환 그대로·거동 보존). 포집 래퍼의 위치·거동은 무변이다(D-T5 ①).
        """
        if self.artifact_store is None:
            return self._wrap_unit_timeout(self.invoker)
        return self._wrap_unit_timeout(
            ArtifactCapturingInvoker(self.invoker, self.artifact_store, run_id=self.run_id)
        )

    def _unit_timeouts(self) -> dict[str, Any]:
        """현재 그래프에서 파생한 {단위 id: 실행 예산(초)} 맵(순수 파생·PO-INV 3·D-T4).

        원천은 `active_graph()` 하나뿐이다 — 제2 진리원천을 두지 않는다. 맵에는 **유효값만**
        편입한다(양의 정수·bool 제외). 불량값은 편입하지 않고 조용히 전역 fallback 으로
        남긴다: 차단은 상류 검증 게이트(impl-plan 어댑터 검증)가 소유하며 래퍼는 기계
        재기입만 한다(판단 0). 검증 경로를 지난 값은 이미 유효하므로 이 필터는 비검증
        경로(seed 그래프·레거시 원장)의 불량값이 실행을 죽이지 않게 하는 안전망이다.
        """
        result: dict[str, Any] = {}
        for task in self.active_graph().get("tasks") or []:
            if not isinstance(task, dict):
                continue
            tid = task.get("id")
            value = task.get(TASK_TIMEOUT_KEY)
            if not isinstance(tid, str) or not tid.strip():
                continue
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                continue
            result[tid] = value
        return result

    def _wrap_unit_timeout(self, invoker: Any) -> Any:
        """단위 timeout 맵이 비어 있지 않을 때만 재기입 래퍼로 감싼다(공집합 = 래핑 0)."""
        timeouts = self._unit_timeouts()
        if not timeouts:
            return invoker
        return UnitTimeoutInvoker(invoker, timeouts)

    def _cp2_model_for(self, step: Step) -> Any:
        """descriptor-aware CP2 슬롯 resolver — step.capability → CP2 모델 슬롯(전달만·해석 0).

        allocation 의 capability class 별 CP2 오버라이드(있으면)를 반영하고, 없으면 전역 cp2_slot
        으로 폴백한다(순수 파생·PO-INV 6 — modelPolicyClass 불투명 키 소비). allocation 부재 시
        None(resolver 자체가 배선되지 않음).
        """
        if self.allocation is None:
            return None
        return self.allocation.cp2_model_for(step.capability)

    def _new_host(self, steps: list[Step]) -> StepHost:
        """StepHost 를 무수정 import·구동한다(공유 EventStore). 재정의 0.

        allocation 이 CP2 독립 모델 슬롯을 정의하면 그 전역 값을 StepHost 에 전달한다
        (OQ-SH-4 해소·전달만·해석 0). 미정의면 None → Host 가 대상 step 슬롯 상속(기존 거동).
        allocation 이 capability class 별 CP2 오버라이드(cp2_slots)를 가지면 descriptor-aware
        resolver 를 추가 배선한다(위험도별 CP2 차등·가법). 오버라이드가 없으면 resolver 는
        None → 전역 cp2_model 경로만 쓰여 기존 거동(S4 테스트 포함)이 완전히 보존된다.
        """
        cp2_model = self.allocation.cp2_model() if self.allocation is not None else None
        cp2_resolver = None
        if self.allocation is not None and self.allocation.has_cp2_overrides():
            cp2_resolver = self._cp2_model_for
        return StepHost(
            steps,
            self._effective_invoker(),
            store=self.event_store,
            retry_limit=self.retry_limit,
            policy=self.policy,
            workdir=self.workdir,
            timeout=self.timeout,
            stop_handler=self.stop_handler,
            cp2_model=cp2_model,
            cp2_model_resolver=cp2_resolver,
        )

    def derive_states(self) -> dict[str, str]:
        """현재 그래프 각 Task 의 파생 상태(events.py 상태 파생 재사용·읽기만)."""
        host = self._new_host(self._build_steps(self.active_graph()))
        return host.derive_states()

    def ready_set(self) -> list[str]:
        """다음 디스패치 대상 = 재개 지점. 두 원장의 순수 함수(읽기만·append 0)."""
        host = self._new_host(self._build_steps(self.active_graph()))
        return host.ready_set()

    def graph_fingerprint(self) -> str:
        """현재 그래프의 결정적 지문 — 순서·내용 동일성 실측용(PO-INV 3).

        같은 (revision 원장, 이벤트 로그) 쌍 → 같은 fold → 같은 지문.
        """
        tasks = self.active_graph()["tasks"]
        canonical = [
            {
                "id": t.get("id"),
                "task": t.get("task"),
                "done": t.get("done"),
                "interfaceContract": t.get("interfaceContract"),
                "ownedBoundary": t.get("ownedBoundary"),
                "dependsOn": t.get("dependsOn"),
            }
            for t in tasks
        ]
        blob = json.dumps(canonical, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------
    # Artifact Registry — 파생 인덱스 (05 §3.6·PO-INV 2·7 — 읽기만·mutable 저장 0)
    # ------------------------------------------------------------------
    def artifact_registry(self) -> dict[str, Any]:
        """{artifactId: [ArtifactRecord]} 파생 인덱스를 매 호출 새로 파생한다.

        입력 = (선언 원장, 이벤트 로그). approvalState 는 게이트/검증 이벤트에서 파생되며
        게이트 식별자는 orchestrator 의 `_gate_id_for` 관례(같은 단위 → 같은 gate_id)로
        해석한다. 선언 원장 미지정(artifact_store None) 시 빈 레지스트리. 순수 파생 —
        별도 mutable 상태로 저장하지 않는다(제2 진리원천 아님·PO-INV 2).
        """
        declarations = self.artifact_store.read_all() if self.artifact_store is not None else []
        return derive_registry(
            declarations,
            self.event_store.read_all(),
            gate_id_for=self._gate_id_for,
            gate_policy=self.gate_policy,
        )

    def _flat_artifact_records(self) -> list[Any]:
        """레지스트리를 평탄화한 ArtifactRecord 목록(review evidence rule (c) 입력·읽기만).

        artifact_store 미지정이면 빈 목록 → rule (c) 공허(현 baseline 거동). 매 호출 파생이며
        별도 저장하지 않는다(제2 진리원천 아님).
        """
        return [r for records in self.artifact_registry().values() for r in records]

    def resolve_references(self, required_grade: str) -> list[Any]:
        """번들 조립용 확정 참조 — 요구 등급 이상 approvalState 의 최신 버전만 해석한다.

        미완성·미승인 산출물은 추측·인용하지 않는다(05 §3.6·07 R2). 계보는 배제하지 않고
        resolve 만 확정 참조에서 제외한다(문면 불변 보존).
        """
        return resolve_references(self.artifact_registry(), required_grade)

    # ------------------------------------------------------------------
    # 게이트 처리 — 단위 경계(배치 종단)에서 gates.evaluate 소비 (05 §3.3·PO-INV 1·4)
    #
    # 판단 0(PO-INV 1): gateKind 평가(effective_gate)·해소 적격성(is_resolved)은 전부
    # gates.py 의 데이터·순수 함수다. 여기서는 그 결과(gateKind·해소 여부)로만 분기하며
    # 내용 판정을 두지 않는다. 배치 종단 일괄 처리(v1.5 OQ-SH-1 선례) — Step Host 가
    # 모든 단위를 Passed 시킨 뒤 각 단위의 게이트를 결정적 순서로 평가한다.
    # ------------------------------------------------------------------
    @staticmethod
    def _descriptor_for(task: dict[str, Any]) -> dict[str, Any]:
        """단위(Task)에서 게이트 target descriptor 파생(정책 평가·floor 입력).

        07 Task 는 이 필드들을 강제하지 않는다(개방 데이터) — 부재 시 None 이며
        floor·정책 어느 쪽도 매칭하지 않아 auto_continue 로 귀결한다(S2 단위 보존).
        """
        return {
            "unitId": task.get("id"),
            "unitType": task.get("unitType"),
            "transition": task.get("transition"),
            "artifactClass": task.get("artifactClass"),
            "targetClass": task.get("targetClass"),
            "interventionCondition": task.get("interventionCondition"),
        }

    @staticmethod
    def _gate_id_for(task_id: Any) -> str:
        """단위 게이트의 결정적 식별자 — 재기동 멱등성의 기반(같은 단위 → 같은 gate_id)."""
        return "gate-unit-" + str(task_id)

    @staticmethod
    def _verdict_summary(result: Any) -> dict[str, Any]:
        """리뷰/승인 디스패치 반환의 경량 요약(내용 아님·provenance 부속·SH-INV-8 동형)."""
        completion = getattr(result, "completion", None) or {}
        return {"verdict": completion.get("verdict"), "ref": getattr(result, "ref", None)}

    def _dispatch_gate_step(self, task: dict[str, Any], gate_id: str, role: str) -> Any:
        """게이트 리뷰/승인 단위를 기존 invoker 로 디스패치한다(_dispatch_cp2 패턴 동형).

        Host 의 CP2 디스패치와 동형으로 산출물(artifacts) 계약을 번들에 싣고 role 만
        바꿔 별도 실행 단위를 기동한다. Orchestrator 는 판정을 내리지 않고 반환을 소비만
        한다(PO-INV 1). model 슬롯은 대상 단위 슬롯을 전달한다(전달만·02 §4 소관).

        timeout 은 전역값으로 조립한 뒤 `_wrap_unit_timeout` 경유로만 단위값이 재기입된다
        (D-T5 ② — 같은 맵·같은 규칙). 산출물 포집 래퍼는 이 경로에 새로 끼우지 않는다
        (게이트 반환은 verdict 이며 산출물 선언이 아니다 — 기존 포집 배선 무변).
        """
        step = Step.from_dict(task)
        bundle = {
            "step_contract": step.contract(),
            "criteria": step.done,
            "gate": {"gate_id": gate_id, "role": role},
        }
        request = InvokeRequest(
            bundle=bundle,
            role=role,
            capability=step.capability,
            model=step.model,
            policy=self.policy,
            workdir=self.workdir,
            timeout=self.timeout,
            criteria=step.done,
        )
        return self._wrap_unit_timeout(self.invoker).invoke(request)

    def _settle_review_gate(
        self,
        task: dict[str, Any],
        tid: Any,
        gate_id: str,
        gate: str,
        descriptor: dict[str, Any],
        events: list[dict[str, Any]],
    ) -> None:
        """review_required 게이트를 해소한다 — 유효 CP2 evidence 소비 우선·재검증 디스패치 fallback.

        ① 정책이 독립 2차 검증을 요구하면(고위험 unitType 등·R3) 기존 경로(재검증 디스패치) 그대로.
        ② 아니면 유효 cp2-pass evidence 를 찾아 존재 시 **디스패치 생략**하고 근거 참조를 실은
           evidence-reuse 마커를 append. ③ evidence 부재/stale 이면 기존 재검증 디스패치 경로.

        판단 0(PO-INV 1): evidence 유효성은 순수 구조 판독(find_valid_cp2_evidence)이며, 마커의
        verdict 는 host 가 기록한 cp2-pass Pass status 를 그대로 반영(재판정 0·host.py verdict_pass
        동형). fallback 디스패치는 판정 권위(Verifier)를 그대로 재기동한다.
        """
        # ① 정책이 독립 2차 검증을 요구 — evidence 재사용 안 함(재검증 디스패치 존치).
        if self.gate_policy.requires_independent_review(descriptor):
            result = self._dispatch_gate_step(task, gate_id, ROLE_VERIFIER)
            append_review_marker(
                self.log, gate_id, gate, self._verdict_summary(result), actor=ROLE_VERIFIER
            )
            return

        # ② 유효 cp2-pass evidence 탐색(순수·fail-closed).
        finding = find_valid_cp2_evidence(
            events,
            tid,
            revisions=self._grounded_revisions(),
            artifact_records=self._flat_artifact_records(),
            hash_observer=hash_file,
        )
        if finding.valid:
            basis = finding.basis or {}
            # verdict 요약은 근거 cp2-pass 의 Pass status 를 반영(status passthrough·판단 0).
            verdict = {"verdict": VERDICT_PASS, "ref": basis.get("verdict_ref")}
            append_review_marker(
                self.log, gate_id, gate, verdict, actor=ROLE_VERIFIER,
                basis=basis, mode=REVIEW_MODE_EVIDENCE_REUSE,
            )
            return

        # ③ evidence 부재/stale → 기존 재검증 디스패치(fallback).
        result = self._dispatch_gate_step(task, gate_id, ROLE_VERIFIER)
        append_review_marker(
            self.log, gate_id, gate, self._verdict_summary(result), actor=ROLE_VERIFIER
        )

    def _process_gates(self, states: dict[str, str], epoch: int) -> "OrchestrationResult | None":
        """단위 경계 게이트를 배치 종단에서 일괄 평가·처리한다.

        반환:
          - OrchestrationResult(status="stopped", stop_reason="gate") — 정지 게이트
            (escalation/user_decision)가 하나라도 미해소일 때. 적격 해소 이벤트 등장 후
            재기동하면 이 함수가 다시 pending 0 을 확인해 통과시킨다(결정적 재개).
          - None — 정지 게이트 없음(auto/review/approval 처리 후 계속 진행).

        멱등성: review/approval 은 마커 이벤트 실재 시 재디스패치하지 않고, 정지 게이트
        요구는 이미 실재하면 재append 하지 않는다(같은 두 원장 재생 → 같은 로그).
        """
        if self.gate_policy is None:
            return None

        graph = self.active_graph()
        must_stop = False
        for task in graph["tasks"]:
            tid = task.get("id")
            if states.get(tid) != PASSED:
                continue  # 게이트는 단위 완료(Passed) 경계에서만 평가한다.
            descriptor = self._descriptor_for(task)
            gate = effective_gate(descriptor, self.gate_policy)  # floor 클램프 포함.
            if gate == GATE_AUTO_CONTINUE:
                continue  # 무정지.
            gate_id = self._gate_id_for(tid)
            events = self.event_store.read_all()

            if gate == GATE_REVIEW_REQUIRED:
                # 유효 CP2 evidence(cp2-pass) 소비로 해소하되, 재검증 디스패치는 fallback 으로
                # 존치한다(멱등·비정지·05 §3.3·T2). 마커 실재 시 재처리 0(결정적 재개).
                if not has_settlement(events, gate_id, REF_KIND_REVIEW):
                    self._settle_review_gate(task, tid, gate_id, gate, descriptor, events)
                continue

            if gate == GATE_APPROVAL_REQUIRED:
                # 경계 CP3(Advisor 역할) 1회 디스패치(멱등·물리화).
                if not has_settlement(events, gate_id, REF_KIND_APPROVAL):
                    result = self._dispatch_gate_step(task, gate_id, ROLE_ADVISOR)
                    append_approval_marker(
                        self.log, gate_id, gate, self._verdict_summary(result), actor=ROLE_ADVISOR
                    )
                    events = self.event_store.read_all()  # 마커 append 반영.
                # CP3 verdict **status** 소비(내용 판정 0·PO-INV 1·host.py verdict_pass 동형).
                # 비-Pass 면 escalation 게이트 요구 append + 정지(적격 해소로만 재개). status
                # 를 읽어 분기할 뿐 승인 내용을 판단하지 않는다 — StepHost 의 CP2 소비와 동형.
                if latest_marker_verdict(events, gate_id, REF_KIND_APPROVAL) != VERDICT_PASS:
                    if not is_resolved(events, gate_id, GATE_ESCALATION_REQUIRED, self.gate_policy):
                        if not has_requirement(events, gate_id):
                            append_gate_requirement(
                                self.log, gate_id, GATE_ESCALATION_REQUIRED,
                                target=descriptor,
                                scoped_question={
                                    "unitId": tid,
                                    "gateKind": GATE_ESCALATION_REQUIRED,
                                    "cause": "cp3_not_pass",
                                },
                                actor=self.gate_policy.gate_raiser,
                            )
                        must_stop = True
                continue

            # escalation_required | user_decision_required — 정지 게이트.
            if not is_resolved(events, gate_id, gate, self.gate_policy):
                if not has_requirement(events, gate_id):
                    append_gate_requirement(
                        self.log, gate_id, gate,
                        target=descriptor,
                        scoped_question={"unitId": tid, "gateKind": gate},
                        actor=self.gate_policy.gate_raiser,
                    )
                must_stop = True

        if must_stop:
            pending = pending_gates(self.event_store.read_all(), self.gate_policy)
            return OrchestrationResult(
                status="stopped",
                graph_task_ids=[t.get("id") for t in graph["tasks"]],
                states=states,
                stop_reason="gate",
                stopped_tasks=[g["gate_id"] for g in pending],
                epochs=epoch,
                pending_gates=pending,
            )
        return None

    # ------------------------------------------------------------------
    # 실행 에스컬레이션 해소 채널 — Escalated 정지에 게이트 좌표 부여 + 적격 해소 후 재작업
    # (05 §3.3 정지 게이트 어휘 재사용·PO-INV 1 판단 0·PO-INV 2 append-only)
    #
    # Step Host 는 재시도 한도 초과/차단 선언을 Escalated 로 종단시키고 정지한다(SH-INV-4).
    # 그 정지는 "상위 위임"이라는 의미는 맞지만, 지금까지 **원장 좌표(gate_id)가 없어서**
    # 상위가 해소 이벤트를 append 할 대상이 없었다. 여기서 그 정지를 05 §3.3 의
    # escalation_required 게이트 요구로 좌표화하고, 적격 해소가 등장하면 단위를 Failed 로
    # 되돌려(재작업 되돌림 이벤트) Host 가 정확히 1회 추가 디스패치하게 한다.
    #
    # 판단 0: 해소 적격성은 gates.py(is_eligible_resolver)가 소유하고, 여기서는 그 결과와
    # 이벤트 at 선후만 비교한다. 해소 응답 내용은 해석하지 않고 ref 로 전달만 한다.
    # ------------------------------------------------------------------
    @staticmethod
    def _escalation_gate_id(task_id: Any) -> str:
        """실행 에스컬레이션 게이트의 결정적 식별자(같은 단위 → 같은 gate_id·비충돌)."""
        return ProjectOrchestrator._gate_id_for(task_id) + ESCALATION_GATE_SUFFIX

    @staticmethod
    def _latest_escalated_event(
        events: list[dict[str, Any]], task_id: Any
    ) -> dict[str, Any] | None:
        """이 단위 사이클의 마지막 escalated 이벤트(없으면 None). 순수 판독."""
        latest: dict[str, Any] | None = None
        for e in events:
            if e.get("cycle_id") != task_id or e.get("outcome") != "escalated":
                continue
            if latest is None or e.get("at", 0) >= latest.get("at", 0):
                latest = e
        return latest

    def _apply_gate_rework(
        self, task_id: Any, gate_id: str, resolution: dict[str, Any], escalated: dict[str, Any] | None
    ) -> dict[str, Any]:
        """적격 해소를 받아 단위를 재작업 되돌림한다 — 이벤트 1건 append(append-only).

        outcome="fail" 이므로 events.py 상태 파생이 Escalated → Failed 로 바뀌고(마지막
        이벤트가 상태를 결정), Host 의 ready_set 이 이 단위를 다시 포함한다. Host 는 한도를
        **실패 시점에만** 판정하므로(host.py `_record_failure`) 이 되돌림은 정확히 1회의 추가
        디스패치를 부여하고, 그 시도가 또 실패하면 정직하게 재에스컬레이션된다.

        actor 는 해소 주체를 그대로 기록하고(provenance), 해소 응답 원문은 ref 에 전달만 한다
        (내용 판단 0). retry_count 는 현재까지의 실패 계수(prior_failures)를 그대로 싣는다.
        """
        return self.log.append(
            cycle_id=task_id,
            # from_stage 는 되돌림 직전 단계 = 에스컬레이션 이벤트의 to_stage(파생·추측 0).
            from_stage=(escalated or {}).get("to_stage"),
            to_stage="Execute",
            trigger=TRIGGER_GATE_REWORK,
            outcome="fail",
            actor=resolution.get("actor"),
            retry_count=self.log.prior_failures(task_id),
            ref={
                "kind": REF_KIND_GATE_REWORK,
                "gate_id": gate_id,
                "response": resolution_response(resolution),
            },
        )

    def _process_escalations(
        self, result: Any, epoch: int, before_ids: list[Any]
    ) -> "OrchestrationResult | None":
        """Host escalated 정지를 게이트 좌표화하고 적격 해소를 재작업으로 적용한다.

        단위별 판정(E_at = 마지막 escalated 이벤트 at, R_at = 최신 적격 해소 at):
          - R_at > E_at            → 재작업 되돌림 적용(정지하지 않음).
          - 요구 부재 또는 요구가 E_at 보다 앞섬 → 새 요구 append + 정지.
          - 그 외(요구 실재·미해소) → 재append 0(멱등) + 정지.

        재에스컬레이션 시 **새 요구**를 append 하므로 이전 해소는 소진된다(is_resolved 의
        since 규칙 = latest_requirement.at 이후 해소만 인정). 반환 None = 재작업 적용됨
        (호출부가 루프를 계속). gate_policy 부재(레거시)는 호출부가 진입 전에 걸러낸다.
        """
        graph = self.active_graph()
        tasks_by_id = {t.get("id"): t for t in graph["tasks"]}
        must_stop = False
        reworked: list[Any] = []
        for tid in result.stopped_tasks:
            events = self.event_store.read_all()
            escalated = self._latest_escalated_event(events, tid)
            e_at = escalated.get("at", 0) if escalated is not None else None
            gate_id = self._escalation_gate_id(tid)
            resolution = latest_eligible_resolution(
                events, gate_id, GATE_ESCALATION_REQUIRED, self.gate_policy
            )
            r_at = resolution.get("at", 0) if resolution is not None else None
            if r_at is not None and e_at is not None and r_at > e_at:
                self._apply_gate_rework(tid, gate_id, resolution, escalated)
                reworked.append(tid)
                continue
            req = latest_requirement(events, gate_id)
            if req is None or (e_at is not None and req.get("at", 0) < e_at):
                append_gate_requirement(
                    self.log, gate_id, GATE_ESCALATION_REQUIRED,
                    target=self._descriptor_for(tasks_by_id.get(tid) or {"id": tid}),
                    scoped_question={
                        "unitId": tid,
                        "gateKind": GATE_ESCALATION_REQUIRED,
                        "cause": CAUSE_EXECUTION_ESCALATED,
                    },
                    actor=self.gate_policy.gate_raiser,
                )
            must_stop = True

        if reworked and not must_stop:
            return None  # 전건 되돌림 완료 → 재fold 후 계속(추가 디스패치 1회).

        pending = pending_gates(self.event_store.read_all(), self.gate_policy)
        return OrchestrationResult(
            status="stopped",
            graph_task_ids=before_ids,
            states=result.states,
            stop_reason=result.stop_reason,
            stopped_tasks=result.stopped_tasks,
            epochs=epoch,
            pending_gates=pending,
        )

    # ------------------------------------------------------------------
    # 실행 루프 — fold → 직렬화 → Step Host 구동 → 성장 확인 (05 §3.2·04 loop ①~⑤)
    # ------------------------------------------------------------------
    def run(self, max_epochs: int = DEFAULT_MAX_EPOCHS) -> OrchestrationResult:
        """프로젝트 그래프를 완료까지 구동한다.

        ① 현재 그래프 fold  ② Step 직렬화(기존 Step 재사용)  ③ StepHost 무수정 구동
        (공유 EventStore)  ④ 수용된 revision 으로 그래프가 성장하면 확장 후 계속
        ⑤ Escalated 잔존(Host 가 stopped 반환) 시 즉시 정지(SH 동형).

        재기동해도 두 원장 재생으로 이미 Passed 인 Step 은 재실행되지 않고 동일 재개
        지점에서 이어진다(PO-INV 3 — StepHost 결정적 재개 위임).
        """
        epochs = 0
        while True:
            epochs += 1
            if epochs > max_epochs:
                # 진행 보장 안전판 — 정상 흐름에서는 도달하지 않는다.
                raise RuntimeError("orchestration epoch 한도 초과 — 진행 보장 위반 방지")

            graph = self.active_graph()
            before_ids = [t.get("id") for t in graph["tasks"]]
            host = self._new_host(self._build_steps(graph))
            result = host.run()

            if result.status == "stopped":
                # Escalated 잔존 → 정지. 게이트 등급 분리는 Host 가 소유(SH-INV-4).
                # gate_policy 가 있으면 이 정지에 게이트 좌표(gate_id)를 부여하고, 적격 해소가
                # 이미 있으면 재작업 되돌림 후 계속한다(해소 채널). gate_policy 부재(레거시)
                # 또는 escalated 이외 정지 사유면 종전 거동 그대로 즉시 정지한다.
                if (
                    self.gate_policy is not None
                    and result.stop_reason == STOP_REASON_ESCALATED
                ):
                    esc_stop = self._process_escalations(result, epochs, before_ids)
                    if esc_stop is not None:
                        return esc_stop
                    continue  # 재작업 되돌림 적용 → 재fold 후 계속(추가 디스패치 1회).
                return OrchestrationResult(
                    status="stopped",
                    graph_task_ids=before_ids,
                    states=result.states,
                    stop_reason=result.stop_reason,
                    stopped_tasks=result.stopped_tasks,
                    epochs=epochs,
                )

            # completed | halted → 단위 경계 게이트를 배치 종단에서 평가한다(05 §3.3).
            # 정지 게이트 미해소 시 즉시 정지(적격 해소 이벤트 등장 후 재기동으로 재개).
            # auto/review/approval 은 여기서 처리되고 계속 진행한다. gate_policy 미지정 시
            # None 반환 → S2 거동 그대로.
            gate_stop = self._process_gates(result.states, epochs)
            if gate_stop is not None:
                return gate_stop

            # 수용된 revision 으로 그래프가 성장했는지 확인(④). 게이트 이벤트는 step id 가
            # 아닌 "gate::" 네임스페이스이므로 그래프 task 집합을 바꾸지 않는다.
            after_ids = [t.get("id") for t in self.active_graph()["tasks"]]
            if set(after_ids) != set(before_ids):
                continue  # 그래프 확장 → 재fold 후 계속(이미 Passed 인 Step 은 재실행 0).

            return OrchestrationResult(
                status=result.status,
                graph_task_ids=after_ids,
                states=result.states,
                epochs=epochs,
            )
