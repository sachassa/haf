"""이벤트 로그·상태 파생 (프로토콜 §4.1).

기록은 03 §3.2-A 전이 이벤트 스키마(10필드)를 동형 재사용하는 append-only 로그다.
"현재 상태"는 별도의 mutable 필드가 아니라 로그의 파생 뷰이며, 마지막 관련 이벤트가
상태를 결정한다(SH-INV-2). Host 는 mutable 상태 필드를 두지 않는다.

상태 5종은 03 §3.2-B 정본을 그대로 흡수한다 — 새 상태 열거 신설 0.

직렬화 형식은 개념상 Adapter 소관이므로(프로토콜 §7.2) 저장은 EventStore 추상으로
주입한다. 기본 구현 JsonlEventStore 는 1행 1이벤트 append-log 이며, Adapter 는 이를
교체할 수 있다. 어떤 provider 토큰도 두지 않는다.
"""

from __future__ import annotations

import json
import os
from typing import Any, Iterable, Protocol


# 03 §3.2-A 전이 이벤트 10필드 (필드명·의미·필수 표기의 정본은 03 §3.2-A).
EVENT_FIELDS = (
    "cycle_id",   # 이 Lifecycle 사이클 식별자 — Step Host 에서는 Step(Task) id.
    "seq",        # 사이클 내 전이 순번. 단조 증가.
    "from_stage", # 전이 이전 단계. 사이클 시작 시 없음(선택).
    "to_stage",   # 전이 이후 단계.
    "trigger",    # 전이 사유.
    "outcome",    # pass / fail / escalated.
    "retry_count",# 재작업 되돌림 횟수.
    "actor",      # 전이를 유발한 역할 또는 human.
    "ref",        # 관련 산출물·보고 참조(선택).
    "at",         # 순서 보장용 값(물리 시각 아님).
)

# 03 §3.2-B 단계 상태 5종 (정본). 비정본 검토 어휘는 프로토콜 §4.1 표에 병기.
PENDING = "Pending"
ACTIVE = "Active"
PASSED = "Passed"
FAILED = "Failed"
ESCALATED = "Escalated"


class EventStore(Protocol):
    """append-only 이벤트 저장 추상. 직렬화 형식은 구현체(Adapter) 소관이다."""

    def append(self, event: dict[str, Any]) -> None: ...

    def read_all(self) -> list[dict[str, Any]]: ...


class InMemoryEventStore:
    """테스트·비영속 용 append-only 저장. 기존 항목은 재작성·삭제하지 않는다."""

    def __init__(self, seed: Iterable[dict[str, Any]] | None = None) -> None:
        self._events: list[dict[str, Any]] = [dict(e) for e in (seed or [])]

    def append(self, event: dict[str, Any]) -> None:
        self._events.append(dict(event))

    def read_all(self) -> list[dict[str, Any]]:
        return [dict(e) for e in self._events]


class JsonlEventStore:
    """파일 기반 append-only 저장 — 1행 = 1이벤트(자기서술 데이터 객체).

    갱신·정정은 기존 행을 바꾸지 않고 새 이벤트 행을 추가한다(append-only, 03 INV-3).
    """

    def __init__(self, path: str) -> None:
        self.path = path
        directory = os.path.dirname(os.path.abspath(path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(path):
            # 빈 로그 파일을 만들어 둔다(재개 시 존재 전제).
            with open(path, "a", encoding="utf-8"):
                pass

    def append(self, event: dict[str, Any]) -> None:
        line = json.dumps(event, ensure_ascii=False, sort_keys=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        with open(self.path, "r", encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if raw:
                    events.append(json.loads(raw))
        return events


class EventLog:
    """이벤트 로그 판독·기록 파사드 + 상태 파생 뷰.

    seq 는 로그 전역 단조 증가로 부여한다(append 시점 자동). "현재 상태"는 이 로그의
    파생 뷰이며 저장되지 않는다(SH-INV-2).
    """

    def __init__(self, store: EventStore) -> None:
        self.store = store

    # --- 기록 -------------------------------------------------------------
    def append(
        self,
        *,
        cycle_id: str,
        to_stage: str,
        trigger: str,
        outcome: str,
        actor: str,
        retry_count: int = 0,
        from_stage: str | None = None,
        ref: Any = None,
    ) -> dict[str, Any]:
        existing = self.store.read_all()
        # seq = 사이클 내 전이 순번(03 §3.2-A). 하나의 run 로그에 여러 Step(사이클)이
        # 섞이므로 cycle_id 별로 계수한다.
        seq = sum(1 for e in existing if e.get("cycle_id") == cycle_id) + 1
        # at = 로그 전역 append 순서(순서 보장용 값·물리 시각 아님 — L-09). 교차 사이클
        # 순서를 확정한다.
        global_at = len(existing) + 1
        event = {
            "cycle_id": cycle_id,
            "seq": seq,
            "from_stage": from_stage,
            "to_stage": to_stage,
            "trigger": trigger,
            "outcome": outcome,
            "retry_count": retry_count,
            "actor": actor,
            "ref": ref,
            "at": global_at,
        }
        self.store.append(event)
        return event

    # --- 판독 -------------------------------------------------------------
    def all_events(self) -> list[dict[str, Any]]:
        return self.store.read_all()

    def events_for(self, cycle_id: str) -> list[dict[str, Any]]:
        rows = [e for e in self.store.read_all() if e.get("cycle_id") == cycle_id]
        rows.sort(key=lambda e: e.get("seq", 0))
        return rows

    def prior_failures(self, cycle_id: str) -> int:
        return sum(1 for e in self.events_for(cycle_id) if e.get("outcome") == "fail")

    def last_failure_ref(self, cycle_id: str) -> Any:
        for e in reversed(self.events_for(cycle_id)):
            if e.get("outcome") == "fail":
                return e.get("ref")
        return None

    def derive_state(self, cycle_id: str) -> str:
        """한 Step 의 파생 상태 — 마지막 관련 이벤트가 결정한다(§4.1)."""
        events = self.events_for(cycle_id)
        if not events:
            return PENDING
        last = events[-1]
        outcome = last.get("outcome")
        to_stage = last.get("to_stage")
        if outcome == "escalated":
            return ESCALATED
        if to_stage == "Complete" and outcome == "pass":
            return PASSED
        if outcome == "fail":
            return FAILED
        # 디스패치(Execute 진입)만 있고 완료(Complete)가 없는 경우 = 실행 중 / 중단 흔적.
        return ACTIVE

    def derive_states(self, cycle_ids: Iterable[str]) -> dict[str, str]:
        return {cid: self.derive_state(cid) for cid in cycle_ids}
