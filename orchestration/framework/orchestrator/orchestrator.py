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

from revision import RevisionLedger, RevisionRejected, fold
from stephost_bridge import (
    DEFAULT_RETRY_LIMIT,
    EventLog,
    EventStore,
    Invoker,
    POLICY_INTERACTIVE,
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
    stop_reason: str | None = None
    stopped_tasks: list[str] = field(default_factory=list)
    epochs: int = 0

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
    ) -> None:
        self.ledger = ledger
        # step 이벤트 store 는 Step Host 와 **공유**한다 — 두 원장이 아니라 이중 원장
        # 중 하나(step 이벤트 로그)를 Host 와 같은 백엔드로 본다(PO-INV 2·3).
        self.event_store = event_store
        self.invoker = invoker
        self.log = EventLog(event_store)
        self.retry_limit = retry_limit
        self.policy = policy
        self.workdir = workdir
        self.timeout = timeout
        self.stop_handler = stop_handler

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
        if not gate_ref:
            return False
        return any(
            self._event_gate_id(e) == gate_ref for e in self.event_store.read_all()
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

            # completed | halted → 수용된 revision 으로 그래프가 성장했는지 확인(④).
            after_ids = [t.get("id") for t in self.active_graph()["tasks"]]
            if set(after_ids) != set(before_ids):
                continue  # 그래프 확장 → 재fold 후 계속(이미 Passed 인 Step 은 재실행 0).

            return OrchestrationResult(
                status=result.status,
                graph_task_ids=after_ids,
                states=result.states,
                epochs=epochs,
            )
