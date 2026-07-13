"""Graph Revision Ledger 자체 테스트 (표준 라이브러리 unittest 만·외부 의존 0).

revision.py 는 순수 모듈(step-host 무의존)이므로 이 파일은 브리지를 거치지 않고
orchestrator 디렉터리만 sys.path 에 넣는다.

커버:
  1. RevisionEvent 직렬화 왕복
  2. fold — task_added·dependency_added·task_superseded·안정 정렬·순수성
  3. task_superseded 문면 불변(원장에 과거 레코드 보존·현재 뷰만 대체)
  4. validate_revision — 4종 07 사유 코드(Missing*·DependencyCycle·OwnershipOverlap)
  5. RevisionLedger — revisionSeq 전순서·구조 검증 거부 시 원장 오염 0·append-only
  6. 결정성 3조건 대응물(전순서·안정 정렬·순수 함수 검증)

특정 provider·모델·상류 Layer 고유명 토큰을 두지 않는다(PO-INV 8).
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

_ORCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ORCH_DIR not in sys.path:
    sys.path.insert(0, _ORCH_DIR)

from revision import (  # noqa: E402
    InMemoryRevisionStore,
    JsonlRevisionStore,
    KIND_DEPENDENCY_ADDED,
    KIND_TASK_ADDED,
    KIND_TASK_SUPERSEDED,
    REASON_DEPENDENCY_CYCLE,
    REASON_MISSING_COMPLETION,
    REASON_MISSING_INTERFACE,
    REASON_OWNERSHIP_OVERLAP,
    RevisionEvent,
    RevisionLedger,
    RevisionRejected,
    fold,
    validate_revision,
)


# --------------------------------------------------------------------------
# 픽스처 — 07 Task payload 빌더 (필수 필드 완비)
# --------------------------------------------------------------------------
def task_payload(tid, depends_on=None, done=None, ifc=None, owned=None):
    return {
        "id": tid,
        "task": "unit " + tid,
        "done": (done if done is not None else "AC-" + tid),
        "interfaceContract": (ifc if ifc is not None else {"produces": ["c-" + tid]}),
        "ownedBoundary": (owned if owned is not None else ["file-" + tid]),
        "dependsOn": list(depends_on or []),
        "delegation": {
            "from": "Advisor", "to": "Worker", "task": "impl",
            "input": "in-" + tid, "output": "out-" + tid, "done": "AC-" + tid,
            "context": ["doc"], "constraints": None,
        },
        "role": "Worker", "capability": "cap", "model": "slot",
    }


def initial_two_task():
    return {
        "goal": "goal",
        "tasks": [task_payload("s1"), task_payload("s2", depends_on=["s1"])],
        "completion": "all-passed",
    }


def rev(seq, kind, payload, gate="g1", proposer="p1"):
    return RevisionEvent(
        revisionSeq=seq, kind=kind, payload=payload,
        basis={"proposingStepRef": proposer, "gateEventRef": gate},
    )


# --------------------------------------------------------------------------
class RevisionEventSerialization(unittest.TestCase):
    def test_roundtrip(self):
        r = rev(1, KIND_TASK_ADDED, task_payload("s3"))
        again = RevisionEvent.from_dict(r.to_dict())
        self.assertEqual(again.revisionSeq, 1)
        self.assertEqual(again.kind, KIND_TASK_ADDED)
        self.assertEqual(again.payload["id"], "s3")
        self.assertEqual(again.basis["gateEventRef"], "g1")


class FoldBehavior(unittest.TestCase):
    def test_fold_empty_returns_initial_tasks_in_order(self):
        graph = fold([], initial_two_task())
        self.assertEqual([t["id"] for t in graph["tasks"]], ["s1", "s2"])
        # dependencies 파생: s1 -> s2.
        self.assertIn(["s1", "s2"], graph["dependencies"])

    def test_task_added_appends_in_revisionseq_order(self):
        revs = [
            rev(2, KIND_TASK_ADDED, task_payload("s4", depends_on=["s2"])),
            rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"])),
        ]
        graph = fold(revs, initial_two_task())
        # 안정 정렬: 초기(s1,s2) → revisionSeq 순(s3 seq1, s4 seq2).
        self.assertEqual([t["id"] for t in graph["tasks"]], ["s1", "s2", "s3", "s4"])

    def test_dependency_added_merges_depends_on(self):
        base = fold([], initial_two_task())
        revs = [rev(1, KIND_DEPENDENCY_ADDED, {"id": "s2", "dependsOn": ["s1", "s1"]})]
        graph = fold(revs, initial_two_task())
        s2 = next(t for t in graph["tasks"] if t["id"] == "s2")
        # 중복 제거되어 s1 한 번만.
        self.assertEqual(s2["dependsOn"], ["s1"])
        # 원본 initial 은 변경되지 않는다(순수 함수).
        self.assertEqual(base["tasks"][1]["dependsOn"], ["s1"])

    def test_task_superseded_replaces_current_view_keeps_position(self):
        revs = [
            rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"])),
            rev(2, KIND_TASK_SUPERSEDED,
                dict(task_payload("s3", depends_on=["s2"], done="AC-3-v2"),
                     supersedes="s3")),
        ]
        graph = fold(revs, initial_two_task())
        ids = [t["id"] for t in graph["tasks"]]
        self.assertEqual(ids, ["s1", "s2", "s3"])  # 위치 승계.
        s3 = next(t for t in graph["tasks"] if t["id"] == "s3")
        self.assertEqual(s3["done"], "AC-3-v2")  # 현재 뷰는 대체판.

    def test_fold_is_pure_same_input_same_output(self):
        revs = [rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]))]
        g1 = fold(revs, initial_two_task())
        g2 = fold(revs, initial_two_task())
        self.assertEqual([t["id"] for t in g1["tasks"]], [t["id"] for t in g2["tasks"]])
        self.assertEqual(g1["dependencies"], g2["dependencies"])


class ValidateRevision(unittest.TestCase):
    def setUp(self):
        self.current = fold([], initial_two_task())

    def test_valid_task_added_returns_none(self):
        r = rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]))
        self.assertIsNone(validate_revision(r, self.current))

    def test_missing_completion_criteria(self):
        payload = task_payload("s3", depends_on=["s2"])
        payload["done"] = ""  # 완료 조건 누락.
        r = rev(1, KIND_TASK_ADDED, payload)
        self.assertEqual(validate_revision(r, self.current), REASON_MISSING_COMPLETION)

    def test_missing_interface_contract(self):
        payload = task_payload("s3", depends_on=["s2"])
        payload["interfaceContract"] = None  # 인터페이스 계약 누락.
        r = rev(1, KIND_TASK_ADDED, payload)
        self.assertEqual(validate_revision(r, self.current), REASON_MISSING_INTERFACE)

    def test_dependency_cycle(self):
        # 초기: s2 -> s1 (s2 가 s1 의존). 여기에 s1 -> s2 의존 추가 → s1<->s2 순환.
        r = rev(1, KIND_DEPENDENCY_ADDED, {"id": "s1", "dependsOn": ["s2"]})
        self.assertEqual(validate_revision(r, self.current), REASON_DEPENDENCY_CYCLE)

    def test_ownership_overlap_same_parallel_set(self):
        # s3·s4 둘 다 s2 의존(서로 의존 없음 = 같은 병렬 집합) + 같은 소유 경계.
        current = fold(
            [rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"], owned=["shared"]))],
            initial_two_task(),
        )
        r = rev(2, KIND_TASK_ADDED, task_payload("s4", depends_on=["s2"], owned=["shared"]))
        self.assertEqual(validate_revision(r, current), REASON_OWNERSHIP_OVERLAP)

    def test_no_overlap_when_dependency_ordered(self):
        # s3 이 s2 의존이고 소유 경계가 s2 와 겹쳐도, 의존으로 정렬되면 같은 병렬 집합이
        # 아니므로 중첩 위반이 아니다(07 INV-2 는 "같은 병렬 집합 내" 한정).
        current = fold([], initial_two_task())
        r = rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"], owned=["file-s2"]))
        self.assertIsNone(validate_revision(r, current))

    def test_duplicate_task_added_raises_valueerror(self):
        r = rev(1, KIND_TASK_ADDED, task_payload("s1"))  # 기존 id 중복.
        with self.assertRaises(ValueError):
            validate_revision(r, self.current)


class RevisionLedgerAppendOnly(unittest.TestCase):
    def test_append_assigns_monotonic_revisionseq(self):
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        basis = {"proposingStepRef": "p", "gateEventRef": "g"}
        r1 = ledger.append(KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]), basis)
        r2 = ledger.append(KIND_TASK_ADDED, task_payload("s4", depends_on=["s2"]), basis)
        self.assertEqual(r1.revisionSeq, 1)
        self.assertEqual(r2.revisionSeq, 2)
        self.assertEqual(len(ledger.store.read_all()), 2)

    def test_rejected_revision_leaves_ledger_clean(self):
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        basis = {"proposingStepRef": "p", "gateEventRef": "g"}
        # 순환 유발(dependency_added s1 -> s2 while s2 -> s1) → 거부.
        with self.assertRaises(RevisionRejected) as ctx:
            ledger.append(KIND_DEPENDENCY_ADDED, {"id": "s1", "dependsOn": ["s2"]}, basis)
        self.assertEqual(ctx.exception.reason, REASON_DEPENDENCY_CYCLE)
        # 원장 오염 0.
        self.assertEqual(len(ledger.store.read_all()), 0)

    def test_missing_basis_raises(self):
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        with self.assertRaises(ValueError):
            ledger.append(KIND_TASK_ADDED, task_payload("s3"), {"proposingStepRef": "p"})

    def test_superseded_keeps_past_record_in_ledger(self):
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        basis = {"proposingStepRef": "p", "gateEventRef": "g"}
        ledger.append(KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]), basis)
        ledger.append(
            KIND_TASK_SUPERSEDED,
            dict(task_payload("s3", depends_on=["s2"], done="AC-3-v2"), supersedes="s3"),
            basis,
        )
        # 원장에는 두 레코드가 모두 보존된다(과거 문면 불변·append-only).
        raw = ledger.store.read_all()
        self.assertEqual(len(raw), 2)
        self.assertEqual(raw[0]["payload"]["done"], "AC-s3")  # 최초판 문면 불변 보존.
        self.assertEqual(raw[1]["payload"]["done"], "AC-3-v2")
        # 현재 뷰는 대체판만.
        s3 = next(t for t in ledger.current_graph()["tasks"] if t["id"] == "s3")
        self.assertEqual(s3["done"], "AC-3-v2")

    def test_jsonl_append_only_prefix_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "revisions.jsonl")
            store = JsonlRevisionStore(path)
            ledger = RevisionLedger(store, initial_two_task())
            basis = {"proposingStepRef": "p", "gateEventRef": "g"}
            ledger.append(KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]), basis)
            with open(path, "r", encoding="utf-8") as fh:
                first = fh.read().splitlines()
            ledger.append(KIND_TASK_ADDED, task_payload("s4", depends_on=["s2"]), basis)
            with open(path, "r", encoding="utf-8") as fh:
                second = fh.read().splitlines()
            # 기존 라인은 접두로 보존된다(재기록 없음).
            self.assertEqual(second[:len(first)], first)
            self.assertEqual(len(second), len(first) + 1)


class DeterminismConditions(unittest.TestCase):
    """05 §3.2 결정성 3조건 대응물 실재 확인."""

    def test_total_order_ledger_assigns_sequence(self):
        # ① 전순서: 원장이 revisionSeq 를 단조 부여(입력 seq 무관하게 재현 가능).
        ledger = RevisionLedger(InMemoryRevisionStore(), initial_two_task())
        basis = {"proposingStepRef": "p", "gateEventRef": "g"}
        seqs = [
            ledger.append(KIND_TASK_ADDED, task_payload("s%d" % i, depends_on=["s2"]), basis).revisionSeq
            for i in range(3, 6)
        ]
        self.assertEqual(seqs, [1, 2, 3])

    def test_stable_sort_independent_of_input_order(self):
        # ② 안정 정렬: 입력 순서가 달라도 revisionSeq 기준 동일 결과.
        a = [
            rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"])),
            rev(2, KIND_TASK_ADDED, task_payload("s4", depends_on=["s2"])),
        ]
        b = list(reversed(a))
        ga = [t["id"] for t in fold(a, initial_two_task())["tasks"]]
        gb = [t["id"] for t in fold(b, initial_two_task())["tasks"]]
        self.assertEqual(ga, gb)
        self.assertEqual(ga, ["s1", "s2", "s3", "s4"])

    def test_validation_is_pure_no_store_mutation(self):
        # ③ 검증의 결정성: validate_revision 은 순수 함수(입력만으로 결과·부작용 0).
        current = fold([], initial_two_task())
        r = rev(1, KIND_TASK_ADDED, task_payload("s3", depends_on=["s2"]))
        first = validate_revision(r, current)
        second = validate_revision(r, current)
        self.assertEqual(first, second)
        self.assertIsNone(first)
        # current 는 변경되지 않는다.
        self.assertEqual([t["id"] for t in current["tasks"]], ["s1", "s2"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
