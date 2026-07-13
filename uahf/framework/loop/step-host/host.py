"""Step Host — 판단하지 않는 기계 구동자 (프로토콜 §2·§4·§5·§6).

Step Host 는 03 사이클 구동과 07 디스패치·순서 규칙을 무인으로 트리거·반복만 한다.
의미 판단(완료/실패/차단/검증/승인)은 전부 invoker 너머 실행 단위·Verifier·Advisor 가
소유하며, Host 는 그 반환값을 소비만 한다(SH-INV-1).

이 모듈이 소유하는 강제:
  - append-only 파생 뷰(SH-INV-2): events.EventLog 위임 — mutable 상태 필드 0.
  - 결정적 재개(SH-INV-3): ready_set 은 로그의 순수 함수.
  - 게이트 등급 분리(SH-INV-4): 어떤 policy 값에서도 CP2 우회 없음·Escalated 정지.
  - Memory 직접 접근 금지(SH-INV-5): 이 모듈에 Memory Store/Index 접근 코드 경로 0.
  - 컨텍스트 격리(SH-INV-8): 상위로는 완료 보고 5필드 수준 요약만.

provider 토큰은 이 모듈 어디에도 두지 않는다 — 실행 표면은 invoker 추상 인터페이스 너머다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

from bundle import assemble_bundle
from events import (
    ACTIVE,
    ESCALATED,
    EventLog,
    EventStore,
    FAILED,
    InMemoryEventStore,
    PASSED,
    PENDING,
)
from invoker import (
    Invoker,
    InvokeRequest,
    KIND_BLOCKED,
    KIND_COMPLETION,
    KIND_FAILURE,
    POLICY_INTERACTIVE,
    ROLE_VERIFIER,
    ROLE_WORKER,
)
from step import Step

# 재시도 한도 기본값. 실값은 Config(01 §3.2-B) 소관이며 Host 는 소비자다(§5.1).
# 이 기본값은 중립 fallback 이고, Adapter/Config 가 명시 지정하면 그 값이 우선한다.
DEFAULT_RETRY_LIMIT = 2

# 정지 사유.
STOP_ESCALATED = "escalated"
STOP_BLOCKED = "blocked"


@dataclass
class RunResult:
    """run 종료 결과 — 상위(호출자/Adapter)로의 요약(SH-INV-8)."""

    status: str  # "completed" | "stopped" | "halted"
    states: dict[str, str] = field(default_factory=dict)
    stop_reason: str | None = None
    stopped_tasks: list[str] = field(default_factory=list)

    @property
    def stopped(self) -> bool:
        return self.status == "stopped"

    @property
    def completed(self) -> bool:
        return self.status == "completed"


class StepHost:
    """Work Graph 의 Step 집합을 무인 구동하는 Step Host."""

    def __init__(
        self,
        steps: Iterable[Step],
        invoker: Invoker,
        *,
        store: EventStore | None = None,
        retry_limit: int = DEFAULT_RETRY_LIMIT,
        policy: str = POLICY_INTERACTIVE,
        workdir: str | None = None,
        timeout: float | None = None,
        stop_handler: Callable[[str, list[str]], None] | None = None,
    ) -> None:
        self.steps: list[Step] = list(steps)
        self.steps_by_id: dict[str, Step] = {s.id: s for s in self.steps}
        self.invoker = invoker
        self.log = EventLog(store if store is not None else InMemoryEventStore())
        self.retry_limit = retry_limit
        # policy 는 데이터로 보관해 invoker 에 전달만 한다(§6.2). Host 는 policy 로
        # 게이트 동작을 바꾸지 않는다 — 게이트 등급 분리(SH-INV-4)는 아래 코드가 소유한다.
        self.policy = policy
        self.workdir = workdir
        self.timeout = timeout
        # 물리 정지 신호의 값(종료 코드 등)은 Adapter 소관이다(프로토콜 §7.2). 중립 Host 는
        # 콜백으로만 정지를 알리고 특정 값을 두지 않는다.
        self.stop_handler = stop_handler

    # ------------------------------------------------------------------
    # 상태 파생 · 결정적 재개 (SH-INV-2·SH-INV-3)
    # ------------------------------------------------------------------
    def derive_states(self) -> dict[str, str]:
        return self.log.derive_states(self.steps_by_id.keys())

    def ready_set(self, states: dict[str, str] | None = None) -> list[str]:
        """다음 디스패치 대상 = "Passed 아닌 Task 중 dependsOn 전부 Passed인 최소 순번 집합".

        07 §3.2-A parallelSets 도출 논리와 동일(순차는 특수형). 로그의 순수 함수이므로
        같은 로그 → 항상 같은 재개 집합(SH-INV-3). Active(실행 중)·Escalated 는 대상이
        아니다 — Active 는 진행 중, Escalated 는 정지 대상이다.
        """
        if states is None:
            states = self.derive_states()
        ready: list[str] = []
        for step in self.steps:
            st = states.get(step.id, PENDING)
            if st in (PENDING, FAILED):
                if all(states.get(dep) == PASSED for dep in step.dependsOn):
                    ready.append(step.id)
        # 결정적 순서: Step 등록 순서 기준(로그·그래프에 대해 안정).
        return ready

    def has_escalated(self, states: dict[str, str] | None = None) -> list[str]:
        if states is None:
            states = self.derive_states()
        return [cid for cid, st in states.items() if st == ESCALATED]

    def all_passed(self, states: dict[str, str] | None = None) -> bool:
        if states is None:
            states = self.derive_states()
        return bool(states) and all(st == PASSED for st in states.values())

    # ------------------------------------------------------------------
    # 실행 루프 (프로토콜 §4.3 — 4 국면)
    # ------------------------------------------------------------------
    def run(self) -> RunResult:
        # 크래시 재개: Active 잔존(중단 흔적) → Failed(실행 중단) append 후 재시도 규칙(§4.2).
        self.recover_active_remnants()

        while True:
            states = self.derive_states()

            # 게이트 보존(SH-INV-4): Escalated 잔존 시 즉시 정지 — policy 무관.
            escalated = self.has_escalated(states)
            if escalated:
                self._emit_stop(STOP_ESCALATED, escalated)
                return RunResult(
                    status="stopped",
                    states=states,
                    stop_reason=STOP_ESCALATED,
                    stopped_tasks=escalated,
                )

            ready = self.ready_set(states)
            if not ready:
                status = "completed" if self.all_passed(states) else "halted"
                return RunResult(status=status, states=states)

            # 한 번에 한 Task 를 처리하고 재파생한다(결정적·진행 보장). 병렬 집합의 각
            # 원소는 순차 처리되며, 스케줄 판정(ready_set)이 병렬 집합 논리를 담는다.
            self._process_step(self.steps_by_id[ready[0]])

    def recover_active_remnants(self) -> None:
        """재생 결과 Active 로 남은 Task = 결과 미확정 → Failed(실행 중단) append(§4.2·멱등)."""
        states = self.derive_states()
        for step in self.steps:
            if states.get(step.id) == ACTIVE:
                attempt = self.log.prior_failures(step.id)
                self._record_failure(
                    step,
                    attempt,
                    feedback={"kind": "interrupted", "reason": "실행 중단"},
                    actor=ROLE_WORKER,
                    trigger="재작업 되돌림",
                    from_stage="Execute",
                    to_stage="Execute",
                )

    # ------------------------------------------------------------------
    # 한 Step 의 처리 (정상 / 실패·재시도 / Blocked / 진입 판정)
    # ------------------------------------------------------------------
    def _process_step(self, step: Step) -> None:
        # 진입 Sufficiency 판정(§6.1): 필수 필드 누락 → 디스패치 금지, scoped 질의 + Escalated.
        missing = step.missing_fields()
        if missing:
            self.log.append(
                cycle_id=step.id,
                from_stage=None,
                to_stage="Consult",
                trigger="에스컬레이션",
                outcome="escalated",
                actor=ROLE_WORKER,
                retry_count=self.log.prior_failures(step.id),
                ref={"kind": "scoped-query", "missing": missing},
            )
            return

        attempt = self.log.prior_failures(step.id)
        feedback = self.log.last_failure_ref(step.id) if attempt > 0 else None

        # 디스패치(Pending/Failed → Active): Execute 진입 이벤트를 먼저 기록한다. 이 이벤트가
        # 남고 완료(Complete)가 뒤따르지 않으면 재개 시 Active(중단 흔적)로 파생된다(§4.2).
        self.log.append(
            cycle_id=step.id,
            from_stage=(None if attempt == 0 else "Failed"),
            to_stage="Execute",
            trigger=("완료 조건 충족" if attempt == 0 else "재작업 되돌림"),
            outcome="pass",
            actor=ROLE_WORKER,
            retry_count=attempt,
            ref={"kind": "dispatch"},
        )

        # Fresh Context 번들 조립(§3.2) — Host 는 Memory 에 직접 접근하지 않는다(SH-INV-5).
        bundle = assemble_bundle(step, feedback=feedback)
        request = InvokeRequest(
            bundle=bundle,
            role=step.role or ROLE_WORKER,
            capability=step.capability,
            model=step.model,
            policy=self.policy,  # 데이터로 전달만(§6.2).
            workdir=self.workdir,
            timeout=self.timeout,
        )
        result = self.invoker.invoke(request)

        # Blocked 국면: 차단 선언 → Escalated + 정지 신호(§4.3). policy 무관(SH-INV-4).
        if result.kind == KIND_BLOCKED:
            self.log.append(
                cycle_id=step.id,
                from_stage="Execute",
                to_stage="Execute",
                trigger="에스컬레이션",
                outcome="escalated",
                actor=ROLE_WORKER,
                retry_count=attempt,
                ref={"kind": "blocked", "report_ref": result.ref},
            )
            return

        # CP1 실패(실행 단위 실패 보고) → Failed(재시도 규칙 §5.1).
        if result.kind == KIND_FAILURE:
            fb = {
                "kind": "failure",
                "reason": (result.failure or {}).get("reason"),
                "repro": (result.failure or {}).get("repro"),
            }
            self._record_failure(
                step, attempt, feedback=fb, actor=ROLE_WORKER,
                trigger="Verify 실패", from_stage="Execute", to_stage="Verify",
            )
            return

        if result.kind != KIND_COMPLETION:
            # 알 수 없는 반환 — 추측하지 않고 Failed 로 처리(진행 보장·재시도).
            self._record_failure(
                step, attempt,
                feedback={"kind": "unknown-result", "reason": "invoker 반환 kind 미해석: " + str(result.kind)},
                actor=ROLE_WORKER, trigger="Verify 실패", from_stage="Execute", to_stage="Verify",
            )
            return

        # 완료 보고 회수(CP1 자체 점검 포함). 자가판정으로 완료를 확정하지 않는다 —
        # CP2 를 별도 독립 단위(Verifier)로 디스패치한다. 게이트 등급 분리(SH-INV-4):
        # 어떤 policy 값에서도 이 CP2 디스패치를 우회하지 않는다.
        verdict = self._dispatch_cp2(step, result)

        if verdict.kind == KIND_COMPLETION and verdict.verdict_pass():
            # CP2 Pass 확정 후에만 Passed append.
            self.log.append(
                cycle_id=step.id,
                from_stage="Verify",
                to_stage="Complete",
                trigger="완료 조건 충족",
                outcome="pass",
                actor=ROLE_VERIFIER,
                retry_count=attempt,
                ref={"kind": "cp2-pass", "verdict_ref": verdict.ref},
            )
            return

        # CP2 Fail/Conditional → Failed(재작업 지시 파생 feedback, §5.1).
        fb = {
            "kind": "rework",
            "rework": verdict.rework(),
            "verdict_ref": verdict.ref,
        }
        self._record_failure(
            step, attempt, feedback=fb, actor=ROLE_VERIFIER,
            trigger="Verify 실패", from_stage="Verify", to_stage="Verify",
        )

    def _dispatch_cp2(self, step: Step, worker_result) -> Any:
        """CP2 를 별도 독립 실행 단위(Verifier 역할)로 디스패치한다(§5.2).

        산출물 자체를 근거로 판정하며(06 V1), CP1 과 같은 단위가 겸하지 않는다. Host 는
        판정을 내리지 않고 Verifier 반환을 소비만 한다(SH-INV-1).
        """
        completion = worker_result.completion or {}
        criteria = step.done
        verify_bundle = {
            "step_contract": step.contract(),
            "artifacts": completion.get("artifacts"),
            "completion_report": completion,
            "criteria": criteria,
        }
        request = InvokeRequest(
            bundle=verify_bundle,
            role=ROLE_VERIFIER,
            capability=step.capability,
            model=step.model,
            policy=self.policy,
            workdir=self.workdir,
            timeout=self.timeout,
            criteria=criteria,
        )
        return self.invoker.invoke(request)

    def _record_failure(
        self,
        step: Step,
        attempt: int,
        feedback: Any,
        *,
        actor: str,
        trigger: str,
        from_stage: str,
        to_stage: str,
    ) -> None:
        """Failed append 후 재시도 한도 초과 시 Escalated 로 정지(§5.1).

        feedback 은 ref 에 실려 로그에서 도출 가능하다 — 별도 상태 시스템 신설 0(§5.1).
        """
        self.log.append(
            cycle_id=step.id,
            from_stage=from_stage,
            to_stage=to_stage,
            trigger=trigger,
            outcome="fail",
            actor=actor,
            retry_count=attempt,
            ref=feedback,
        )
        failures_now = attempt + 1
        if failures_now > self.retry_limit:
            # 한도 초과 → Escalated(03 §3.1-D 조건 1). 실패는 로그에 남아 은폐되지 않는다.
            self.log.append(
                cycle_id=step.id,
                from_stage=to_stage,
                to_stage="Complete",
                trigger="에스컬레이션",
                outcome="escalated",
                actor="Advisor",
                retry_count=failures_now,
                ref={"kind": "retry-limit-exceeded", "limit": self.retry_limit},
            )

    def _emit_stop(self, reason: str, tasks: list[str]) -> None:
        """물리 정지 신호를 상위에 위임한다. 신호의 구체 값(종료 코드 등)은 Adapter 소관."""
        if self.stop_handler is not None:
            self.stop_handler(reason, tasks)
