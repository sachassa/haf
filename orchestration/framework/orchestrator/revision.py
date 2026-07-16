"""Graph Revision Ledger — 동적 그래프의 append-only 실현 (05 §3.2·PO-INV 2·3·5).

진행 중 그래프 확장은 07 Work Graph 재정의가 아니라 "신규 발견 작업에 대한
Decompose(07 §3.1-A) 반복 실행 산출의 append-only 합성"이다(05 §3.2). 각 revision
epoch 가 낳는 파생 그래프는 07 §3.2-A Work Graph 1건을 온전히 만족한다.

이 모듈이 소유하는 것:
  - RevisionEvent — 본 Layer 신규 소유 레코드(05 §0 표). payload 는 07 §3.2-B Task
    전 필드를 담으며 Task 계약을 재정의하지 않는다.
  - RevisionLedger — append-only 저장(인메모리+JSONL). Step Host events.py 의 저장
    패턴과 **동형**이며, 기존 revision 레코드를 수정하는 코드 경로는 0이다(PO-INV 2).
  - fold() — revision 열 → 현재 Task 집합 파생. **순수 함수**·안정 정렬(PO-INV 3).
  - validate_revision() — 스키마 완전성·순환 0·같은 병렬 집합 ownedBoundary 비중첩.
    **순수 함수**. 실패는 07 §3.1-A 사유 코드 재사용(05 §3.2 ③).

판단 0(PO-INV 1): 이 모듈은 revision 의 의미 수용 여부를 판정하지 않는다 — 구조 검증
(순수 함수)과 저장만 한다. 의미 수용은 게이트가 소유하고, 게이트 근거(gateEventRef)
실재 검증은 orchestrator 가 수행한다(05 §3.2 결정성 조건 ①·PO-INV 5).

특정 provider·모델·상류 Layer 고유명 토큰은 이 모듈 어디에도 두지 않는다(PO-INV 8).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol


# --- revision kind 어휘 (05 §3.2) -------------------------------------------
KIND_TASK_ADDED = "task_added"
KIND_DEPENDENCY_ADDED = "dependency_added"
KIND_TASK_SUPERSEDED = "task_superseded"
VALID_KINDS = (KIND_TASK_ADDED, KIND_DEPENDENCY_ADDED, KIND_TASK_SUPERSEDED)

# --- 검증 실패 사유 코드 = 07 §3.1-A Decompose 사유 코드 재사용 (05 §3.2 ③·실측 동형) --
# (07-workflow.md §3.1-A / §3.2-E / §6 에서 문자열 실측 — 재정의 0.)
REASON_MISSING_COMPLETION = "MissingCompletionCriteria"
REASON_MISSING_INTERFACE = "MissingInterfaceContract"
REASON_OWNERSHIP_OVERLAP = "OwnershipOverlap"
REASON_DEPENDENCY_CYCLE = "DependencyCycle"


def _present(value: Any) -> bool:
    """값이 실질적으로 존재하는가 — None·빈 문자열·빈 컬렉션은 부재로 본다.

    step.py `_is_present` 와 동형(진입 Sufficiency 판정 관례 재사용).
    """
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) > 0
    return True


# ==========================================================================
# RevisionEvent — 본 Layer 신규 소유 레코드 (05 §3.2)
# ==========================================================================
@dataclass
class RevisionEvent:
    """진행 중 그래프 확장의 append-only 원장 항목.

    필드 소유 정본:
      revisionSeq  -> 전순서(단조 증가). 원장이 append 시점에 부여(05 §3.2 조건 ①).
      kind         -> task_added | dependency_added | task_superseded.
      payload      -> 07 §3.2-B Task 전 필드(Task 계약 재정의 0). dependency_added 는
                      {id, dependsOn}, task_superseded 는 Task + supersedes 포인터.
      basis        -> {proposingStepRef, gateEventRef} — 근거 없는 그래프 변경 0(PO-INV 5).
    """

    revisionSeq: int
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    basis: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "revisionSeq": self.revisionSeq,
            "kind": self.kind,
            "payload": dict(self.payload),
            "basis": dict(self.basis),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RevisionEvent":
        if not isinstance(data, dict):
            raise TypeError("RevisionEvent 직렬화는 매핑이어야 한다")
        return cls(
            revisionSeq=data.get("revisionSeq"),
            kind=data.get("kind"),
            payload=dict(data.get("payload") or {}),
            basis=dict(data.get("basis") or {}),
        )


class RevisionRejected(Exception):
    """revision 수용 거부. 원장은 오염되지 않는다(append 전에 raise — PO-INV 2·5).

    reason 은 검증 실패 사유(07 §3.1-A 코드 또는 PO-INV 5 근거 부재 사유)다.
    """

    def __init__(self, reason: str, revision: "RevisionEvent | None" = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.revision = revision


# ==========================================================================
# 저장 추상 — Step Host events.py 저장 패턴과 동형 (인메모리 + JSONL)
# ==========================================================================
class RevisionStore(Protocol):
    """append-only revision 저장 추상. 직렬화 형식은 구현체(Adapter) 소관이다."""

    def append(self, revision: dict[str, Any]) -> None: ...

    def read_all(self) -> list[dict[str, Any]]: ...


class InMemoryRevisionStore:
    """테스트·비영속 용 append-only 저장. 기존 항목은 재작성·삭제하지 않는다(PO-INV 2)."""

    def __init__(self, seed: Iterable[dict[str, Any]] | None = None) -> None:
        self._revisions: list[dict[str, Any]] = [dict(r) for r in (seed or [])]

    def append(self, revision: dict[str, Any]) -> None:
        self._revisions.append(dict(revision))

    def read_all(self) -> list[dict[str, Any]]:
        return [dict(r) for r in self._revisions]


class JsonlRevisionStore:
    """파일 기반 append-only 저장 — 1행 = 1 revision(자기서술 데이터 객체).

    갱신·정정은 기존 행을 바꾸지 않고 새 revision 행을 추가한다(append-only·PO-INV 2).
    events.py JsonlEventStore 와 동형이다.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        directory = os.path.dirname(os.path.abspath(path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(path):
            with open(path, "a", encoding="utf-8"):
                pass

    def append(self, revision: dict[str, Any]) -> None:
        line = json.dumps(revision, ensure_ascii=False, sort_keys=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        revisions: list[dict[str, Any]] = []
        with open(self.path, "r", encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if raw:
                    revisions.append(json.loads(raw))
        return revisions


# ==========================================================================
# fold — revision 열 → 현재 그래프 파생 뷰 (순수 함수·안정 정렬·PO-INV 3)
# ==========================================================================
def _copy_task(task: dict[str, Any]) -> dict[str, Any]:
    """Task 를 얕게 복제하되 mutate 대상(dependsOn·ownedBoundary)은 새 리스트로 분리.

    fold 는 caller 의 원본 데이터를 변경하지 않는다(순수 함수 보장).
    """
    out = dict(task)
    out["dependsOn"] = list(task.get("dependsOn") or [])
    out["ownedBoundary"] = list(task.get("ownedBoundary") or [])
    return out


def fold(
    revisions: Iterable[RevisionEvent],
    initial_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """revision 목록을 초기 그래프에 접어(fold) 현재 그래프 파생 뷰를 만든다.

    - **순수 함수**: 입력만으로 출력이 결정된다(I/O·상태 없음 — PO-INV 3, 05 §3.2 조건 ③ 계열).
    - **안정 정렬**: revision 은 revisionSeq 로 정렬(전순서). 파생 Task 는
      (epoch, revisionSeq / 초기 선언 순서)로 결정적 정렬한다 — 05 §3.2 조건 ②
      "(revisionSeq, payload 선언 순서)"의 대응물. ready_set 순서 결정성을 보존한다.
    - `task_superseded` 는 삭제가 아니라 superseding 포인터 append 이며, 원장의 과거
      문면은 불변이다(PC-INV 9 동형). fold 는 현재 뷰에서만 superseded 를 대체한다.
    """
    initial_graph = initial_graph or {}
    current: dict[str, dict[str, Any]] = {}
    order: dict[str, tuple[int, int]] = {}

    # epoch 0 — 초기 그래프 Task(선언 순서).
    for idx, task in enumerate(initial_graph.get("tasks") or []):
        tid = task.get("id")
        if tid is None:
            continue
        current[tid] = _copy_task(task)
        order[tid] = (0, idx)

    # epoch 1 — revision(전순서 revisionSeq). sorted 는 안정 정렬이므로 동seq 는 입력 순서 보존.
    for rev in sorted(revisions, key=lambda r: r.revisionSeq):
        payload = rev.payload or {}
        if rev.kind == KIND_TASK_ADDED:
            tid = payload.get("id")
            if tid is None:
                continue
            current[tid] = _copy_task(payload)
            order[tid] = (1, rev.revisionSeq)
        elif rev.kind == KIND_DEPENDENCY_ADDED:
            tid = payload.get("id")
            if tid in current:
                deps = current[tid]["dependsOn"]
                for dep in payload.get("dependsOn") or []:
                    if dep not in deps:
                        deps.append(dep)
        elif rev.kind == KIND_TASK_SUPERSEDED:
            superseded_id = payload.get("supersedes")
            new_id = payload.get("id")
            if new_id is None:
                continue
            # 위치 안정성: 대체 Task 는 피대체 Task 의 정렬 위치를 승계한다.
            keep_order = order.get(superseded_id, (1, rev.revisionSeq))
            if superseded_id in current and superseded_id != new_id:
                del current[superseded_id]
                order.pop(superseded_id, None)
            current[new_id] = _copy_task(payload)
            order[new_id] = keep_order

    ordered_ids = sorted(current.keys(), key=lambda k: order[k])
    tasks = [current[k] for k in ordered_ids]
    return {
        "goal": initial_graph.get("goal"),
        "tasks": tasks,
        "dependencies": _derive_dependencies(tasks),
        "completion": initial_graph.get("completion"),
    }


def _derive_dependencies(tasks: list[dict[str, Any]]) -> list[list[str]]:
    """dependsOn 에서 07 dependencies(선행 → 후행) 파생. 파생 뷰이며 저장하지 않는다."""
    ids = {t.get("id") for t in tasks}
    deps: list[list[str]] = []
    for task in tasks:
        for dep in task.get("dependsOn") or []:
            if dep in ids:
                deps.append([dep, task.get("id")])
    return deps


# ==========================================================================
# 구조 검증 — 순환·소유 경계 중첩 (순수 함수·05 §3.2 조건 ③)
# ==========================================================================
def _adjacency(tasks: list[dict[str, Any]]) -> dict[str, list[str]]:
    ids = {t.get("id") for t in tasks}
    return {
        t.get("id"): [d for d in (t.get("dependsOn") or []) if d in ids]
        for t in tasks
    }


def _has_cycle(tasks: list[dict[str, Any]]) -> bool:
    """dependsOn 방향 그래프의 순환 존재 여부(DFS 3색)."""
    adj = _adjacency(tasks)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in adj}

    def visit(node: str) -> bool:
        color[node] = GRAY
        for nxt in adj[node]:
            if color[nxt] == GRAY:
                return True
            if color[nxt] == WHITE and visit(nxt):
                return True
        color[node] = BLACK
        return False

    return any(color[node] == WHITE and visit(node) for node in adj)


def _reachable(tasks: list[dict[str, Any]]) -> dict[str, set[str]]:
    """각 Task 가 (전이적으로) 의존하는 Task 집합."""
    adj = _adjacency(tasks)
    reach: dict[str, set[str]] = {}
    for node in adj:
        seen: set[str] = set()
        stack = list(adj[node])
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(adj.get(cur, []))
        reach[node] = seen
    return reach


def _has_ownership_overlap(tasks: list[dict[str, Any]]) -> bool:
    """같은 병렬 집합(의존으로 서로 정렬되지 않는 쌍) 내 ownedBoundary 중첩 여부(07 INV-2).

    두 Task 가 서로 의존 관계가 아니면(어느 쪽도 상대의 전이 의존이 아니면) 동시 디스패치
    가능한 같은 병렬 집합 후보이며, 이때 소유 경계가 겹치면 안 된다.
    """
    reach = _reachable(tasks)
    n = len(tasks)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = tasks[i], tasks[j]
            ai, bi = a.get("id"), b.get("id")
            if bi in reach.get(ai, ()) or ai in reach.get(bi, ()):
                continue  # 의존으로 정렬됨 → 같은 병렬 집합 아님.
            if set(a.get("ownedBoundary") or []) & set(b.get("ownedBoundary") or []):
                return True
    return False


def validate_revision(
    revision: RevisionEvent,
    current_graph: dict[str, Any],
) -> str | None:
    """revision 수용 구조 검증 — **순수 함수**(05 §3.2 조건 ③).

    검사: (1) 스키마 완전성 (2) 순환 0 (3) 같은 병렬 집합 ownedBoundary 비중첩.
    실패는 07 §3.1-A 사유 코드 문자열을 반환한다. 통과는 None.

    의미 수용 여부(이 revision 이 프로젝트에 바람직한가)는 판정하지 않는다 — 게이트
    소유(판단 0·PO-INV 1). 구조 misuse(중복 id·미존재 supersede 대상 등)는 사유 코드가
    아니라 ValueError 로 구분한다(정상 검증 실패와 프로그래밍/드라이버 오류의 분리).
    """
    kind = revision.kind
    if kind not in VALID_KINDS:
        raise ValueError("알 수 없는 revision kind: " + repr(kind))

    payload = revision.payload or {}
    current_tasks = current_graph.get("tasks") or []
    current_ids = {t.get("id") for t in current_tasks}

    # --- (1) 스키마 완전성 (kind 별) --------------------------------------
    if kind == KIND_TASK_ADDED:
        tid = payload.get("id")
        if not _present(tid):
            raise ValueError("task_added payload 에 id 가 없다")
        if tid in current_ids:
            raise ValueError("task_added 가 기존 id 를 중복한다: " + repr(tid))
        if not _present(payload.get("done")):
            return REASON_MISSING_COMPLETION
        if not _present(payload.get("interfaceContract")):
            return REASON_MISSING_INTERFACE
    elif kind == KIND_TASK_SUPERSEDED:
        superseded_id = payload.get("supersedes")
        new_id = payload.get("id")
        if not _present(superseded_id) or not _present(new_id):
            raise ValueError("task_superseded payload 에 supersedes/id 가 필요하다")
        if superseded_id not in current_ids:
            raise ValueError("존재하지 않는 Task 를 supersede 한다: " + repr(superseded_id))
        if not _present(payload.get("done")):
            return REASON_MISSING_COMPLETION
        if not _present(payload.get("interfaceContract")):
            return REASON_MISSING_INTERFACE
    elif kind == KIND_DEPENDENCY_ADDED:
        tid = payload.get("id")
        if not _present(tid) or not _present(payload.get("dependsOn")):
            raise ValueError("dependency_added payload 에 id/dependsOn 이 필요하다")
        if tid not in current_ids:
            raise ValueError("존재하지 않는 Task 에 의존을 추가한다: " + repr(tid))

    # --- (2)·(3) 순환·소유 경계 중첩 (파생 그래프 대상) ---------------------
    prospective = fold([revision], current_graph)["tasks"]
    if _has_cycle(prospective):
        return REASON_DEPENDENCY_CYCLE
    if _has_ownership_overlap(prospective):
        return REASON_OWNERSHIP_OVERLAP
    return None


# ==========================================================================
# RevisionLedger — append-only 원장 파사드 (PO-INV 2)
# ==========================================================================
class RevisionLedger:
    """revision 의 append-only 원장 + 현재 그래프 파생 뷰.

    revisionSeq 는 append 시점에 원장이 전역 단조 증가로 부여한다(전순서 보장·05 §3.2
    조건 ①). "현재 그래프"는 mutable 상태가 아니라 원장의 fold 파생 뷰다(PO-INV 2).
    기존 revision 을 수정하는 코드 경로는 없다.
    """

    def __init__(
        self,
        store: RevisionStore,
        initial_graph: dict[str, Any] | None = None,
    ) -> None:
        self.store = store
        self.initial_graph = initial_graph or {"tasks": []}

    def all(self) -> list[RevisionEvent]:
        return [RevisionEvent.from_dict(d) for d in self.store.read_all()]

    def current_graph(self) -> dict[str, Any]:
        """전체 원장 fold 파생 뷰(근거 검증 없는 순수 구조 뷰).

        게이트 근거(gateEventRef) 실재 필터링은 orchestrator 소관이다(PO-INV 5) —
        원장은 이벤트 로그를 알지 못하므로 구조 fold 만 제공한다.
        """
        return fold(self.all(), self.initial_graph)

    def next_seq(self) -> int:
        return len(self.store.read_all()) + 1

    def append(
        self,
        kind: str,
        payload: dict[str, Any],
        basis: dict[str, Any],
    ) -> RevisionEvent:
        """구조 검증 통과 시에만 revision 을 append 한다(원장 오염 0).

        검증 실패 시 store.append 이전에 RevisionRejected 를 raise 하므로 원장은
        변경되지 않는다(PO-INV 2 — 실패한 revision 의 흔적을 남기지 않는다).
        """
        if (
            not isinstance(basis, dict)
            or not _present(basis.get("proposingStepRef"))
            or not _present(basis.get("gateEventRef"))
        ):
            # basis 필드 스키마 전제(PO-INV 5) — proposingStepRef·gateEventRef 필수.
            raise ValueError(
                "revision basis 에 proposingStepRef/gateEventRef 가 필요하다 (PO-INV 5)"
            )
        revision = RevisionEvent(
            revisionSeq=self.next_seq(),
            kind=kind,
            payload=dict(payload),
            basis=dict(basis),
        )
        reason = validate_revision(revision, self.current_graph())
        if reason is not None:
            raise RevisionRejected(reason, revision)
        self.store.append(revision.to_dict())
        return revision
