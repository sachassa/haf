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
from dataclasses import dataclass, field
from typing import Any

from gates import (
    GATE_APPROVAL_REQUIRED,
    GATE_AUTO_CONTINUE,
    GATE_REVIEW_REQUIRED,
    REF_KIND_APPROVAL,
    REF_KIND_REVIEW,
    GatePolicy,
    append_approval_marker,
    append_gate_requirement,
    append_review_marker,
    effective_gate,
    has_requirement,
    has_settlement,
    is_resolved,
    pending_gates,
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

    def _gate_event_exists(self, gate_ref: Any) -> bool:
        """revision 을 근거짓는 게이트 **통과** 이벤트가 실재하는가(PO-INV 5).

        게이트 통과(승인·해소)만 revision 을 근거지을 수 있다 — outcome == "pass" 로
        한정한다. S3 게이트 요구 이벤트(outcome == "escalated")는 아직 미해소이므로
        revision 을 근거지어서는 안 된다(요구만으로 그래프 변경 0). S2 게이트 승인 이벤트는
        전부 outcome == "pass" 이므로 이 한정은 S2 거동을 보존한다(강화적 정정).
        """
        if not gate_ref:
            return False
        return any(
            e.get("outcome") == "pass" and self._event_gate_id(e) == gate_ref
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
        grounded = [
            r for r in self.ledger.all()
            if self._gate_event_exists(r.basis.get("gateEventRef"))
        ]
        return fold(grounded, self.ledger.initial_graph)

    def _build_steps(self, graph: dict[str, Any]) -> list[Step]:
        """현재 그래프 Task 를 기존 step.py Step 으로 직렬화한다(새 Step 클래스 창설 0)."""
        return [Step.from_dict(task) for task in graph.get("tasks") or []]

    def _new_host(self, steps: list[Step]) -> StepHost:
        """StepHost 를 무수정 import·구동한다(공유 EventStore). 재정의 0."""
        return StepHost(
            steps,
            self.invoker,
            store=self.event_store,
            retry_limit=self.retry_limit,
            policy=self.policy,
            workdir=self.workdir,
            timeout=self.timeout,
            stop_handler=self.stop_handler,
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
        return self.invoker.invoke(request)

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
                # CP2 외 추가 독립 리뷰(Verifier) 1회 디스패치(멱등) — 비정지.
                if not has_settlement(events, gate_id, REF_KIND_REVIEW):
                    result = self._dispatch_gate_step(task, gate_id, ROLE_VERIFIER)
                    append_review_marker(
                        self.log, gate_id, gate, self._verdict_summary(result), actor=ROLE_VERIFIER
                    )
                continue

            if gate == GATE_APPROVAL_REQUIRED:
                # 경계 CP3(Advisor 역할) 1회 디스패치(멱등·물리화) — 비정지.
                if not has_settlement(events, gate_id, REF_KIND_APPROVAL):
                    result = self._dispatch_gate_step(task, gate_id, ROLE_ADVISOR)
                    append_approval_marker(
                        self.log, gate_id, gate, self._verdict_summary(result), actor=ROLE_ADVISOR
                    )
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
                # Escalated 잔존 → 즉시 정지. 게이트 등급 분리는 Host 가 소유(SH-INV-4).
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
