"""Artifact Record·Registry 테스트 (표준 라이브러리 unittest 만).

artifacts.py 순수 테스트 + orchestrator 통합 테스트(모의 invoker)를 한 파일에 둔다
(S2 test_orchestrator.py·S3 test_gates.py·S4 test_allocation.py 무손상 — done 9).

커버(위임 done 1~10·설계 §5 S5 시나리오 i):
  - ArtifactRecord 8필드·직렬화 왕복 (05 §3.6 일치·done 2)
  - approvalState 파생 사다리(draft→verified→approved→user_approved)·전순서 (done 2)
  - derive_approval_state — 각 등급이 대응 이벤트 실재에서만 파생(PO-INV 7·done 2)
  - derive_registry — 순수 함수·계보 append-only·version 정렬·재파생 동일(done 2·mutable 저장 0)
  - resolve_references — 요구 등급 미만·구버전 배제·최신 등급 충족 버전만 (done 3)
  - normalize_declaration / ArtifactCapturingInvoker — 완료 보고 artifacts 포집 (done 5)
  - (i) 통합: 설계 v1 → 리뷰 반려 rework → v2(supersedes·derivedFrom) → 소비 번들이
    required_grade 충족 버전만 참조·v1 문면 불변(물리 파일 해시 대조·done 4)

approvalState 어휘·verdict Pass 는 05 §3.6·06 계약 어휘이며 provider 토큰 0(PO-INV 8·done 7).
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

_ORCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ORCH_DIR not in sys.path:
    sys.path.insert(0, _ORCH_DIR)

import artifacts as artifacts_mod  # noqa: E402
from artifacts import (  # noqa: E402
    APPROVAL_APPROVED,
    APPROVAL_DRAFT,
    APPROVAL_LADDER,
    APPROVAL_USER_APPROVED,
    APPROVAL_VERIFIED,
    CP2_EVIDENCE_ABSENT,
    CP2_EVIDENCE_STALE_HASH,
    CP2_EVIDENCE_STALE_REOPENED,
    CP2_EVIDENCE_STALE_REVISION,
    CP2_EVIDENCE_STALE_UNKNOWN_REVISION,
    CP2_EVIDENCE_VALID,
    ArtifactCapturingInvoker,
    ArtifactRecord,
    InMemoryArtifactDeclarationStore,
    JsonlArtifactDeclarationStore,
    approval_grade,
    content_hash,
    derive_approval_state,
    derive_registry,
    find_valid_cp2_evidence,
    hash_file,
    normalize_declaration,
    resolve_references,
)
from gates import (  # noqa: E402
    GATE_APPROVAL_REQUIRED,
    GATE_USER_DECISION_REQUIRED,
    GatePolicy,
    GatePolicyEntry,
    append_gate_resolution,
)
from orchestrator import ProjectOrchestrator  # noqa: E402
from revision import (  # noqa: E402
    InMemoryRevisionStore,
    KIND_DEPENDENCY_ADDED,
    KIND_TASK_ADDED,
    KIND_TASK_SUPERSEDED,
    RevisionLedger,
)
from stephost_bridge import (  # noqa: E402
    EventLog,
    InMemoryEventStore,
    Invoker,
    InvokeResult,
    KIND_COMPLETION,
    PASSED,
    ROLE_ADVISOR,
    ROLE_VERIFIER,
    ROLE_WORKER,
)


# ==========================================================================
# ArtifactRecord — 8필드·직렬화 왕복 (05 §3.6 — done 2)
# ==========================================================================
class ArtifactRecordShape(unittest.TestCase):
    def test_eight_fields_roundtrip(self):
        rec = ArtifactRecord(
            artifactId="design-memo",
            version=2,
            supersedes=1,
            derivedFrom=["contract@v2"],
            producedBy={"runId": "r1", "stepId": "d1", "attempt": 0,
                        "role": "Worker", "capability": "design", "model": "tier-c"},
            approvalState=APPROVAL_VERIFIED,
            location="ws/design-memo.md",
            contentHash="sha256:abc",
        )
        d = rec.to_dict()
        self.assertEqual(
            set(d.keys()),
            {"artifactId", "version", "supersedes", "derivedFrom", "producedBy",
             "approvalState", "location", "contentHash"},
        )
        self.assertEqual(ArtifactRecord.from_dict(d), rec)

    def test_from_dict_requires_artifact_id(self):
        with self.assertRaises(ValueError):
            ArtifactRecord.from_dict({"version": 1})


# ==========================================================================
# approvalState 사다리 — 전순서 (05 §3.6 — done 2)
# ==========================================================================
class ApprovalLadder(unittest.TestCase):
    def test_ladder_order(self):
        self.assertEqual(
            list(APPROVAL_LADDER),
            [APPROVAL_DRAFT, APPROVAL_VERIFIED, APPROVAL_APPROVED, APPROVAL_USER_APPROVED],
        )
        self.assertLess(approval_grade(APPROVAL_DRAFT), approval_grade(APPROVAL_VERIFIED))
        self.assertLess(approval_grade(APPROVAL_VERIFIED), approval_grade(APPROVAL_APPROVED))
        self.assertLess(approval_grade(APPROVAL_APPROVED), approval_grade(APPROVAL_USER_APPROVED))

    def test_unknown_grade_rejected(self):
        with self.assertRaises(ValueError):
            approval_grade("bogus")


# ==========================================================================
# content_hash / hash_file — 문면 불변 증빙 (done 3 지원)
# ==========================================================================
class ContentHash(unittest.TestCase):
    def test_content_hash_deterministic(self):
        self.assertEqual(content_hash("abc"), content_hash("abc"))
        self.assertNotEqual(content_hash("abc"), content_hash("abd"))
        self.assertTrue(content_hash("x").startswith("sha256:"))

    def test_hash_file_reads_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("HELLO")
            h1 = hash_file(path)
            self.assertEqual(h1, content_hash("HELLO"))
            # 파일이 변경되지 않았음(재해시 동일).
            self.assertEqual(hash_file(path), h1)


# ==========================================================================
# normalize_declaration — 문자열/ dict / provenance (done 5)
# ==========================================================================
class NormalizeDeclaration(unittest.TestCase):
    def test_string_entry_minimal(self):
        d = normalize_declaration("ws/out.txt", producedBy={"stepId": "s1"})
        self.assertEqual(d["artifactId"], "ws/out.txt")
        self.assertEqual(d["location"], "ws/out.txt")
        self.assertEqual(d["version"], 1)
        self.assertIsNone(d["supersedes"])
        self.assertEqual(d["producedBy"], {"stepId": "s1"})
        self.assertNotIn("approvalState", d)  # 선언은 approvalState 를 담지 않는다.

    def test_dict_entry_structured(self):
        d = normalize_declaration(
            {"artifactId": "A", "version": 2, "supersedes": 1,
             "derivedFrom": ["B"], "location": "ws/A.md", "contentHash": "sha256:z"},
            producedBy={"stepId": "d2"},
        )
        self.assertEqual(d["version"], 2)
        self.assertEqual(d["supersedes"], 1)
        self.assertEqual(d["derivedFrom"], ["B"])
        self.assertEqual(d["contentHash"], "sha256:z")

    def test_dict_own_provenance_wins(self):
        d = normalize_declaration(
            {"artifactId": "A", "producedBy": {"stepId": "own"}},
            producedBy={"stepId": "ctx"},
        )
        self.assertEqual(d["producedBy"]["stepId"], "own")

    def test_default_derived_from_applied_to_string(self):
        d = normalize_declaration("A", default_derived_from=["c1"])
        self.assertEqual(d["derivedFrom"], ["c1"])

    def test_bad_entry_rejected(self):
        with self.assertRaises(TypeError):
            normalize_declaration(123)
        with self.assertRaises(ValueError):
            normalize_declaration({"version": 1})  # artifactId/location 없음.


# ==========================================================================
# derive_approval_state — 각 등급이 대응 이벤트 실재에서만 파생 (PO-INV 7·done 2)
# ==========================================================================
def _cp2_pass_event(step_id, at):
    return {"cycle_id": step_id, "seq": 1, "to_stage": "Complete", "outcome": "pass",
            "actor": ROLE_VERIFIER, "ref": {"kind": "cp2-pass", "verdict_ref": "v"}, "at": at}


class DeriveApprovalState(unittest.TestCase):
    def gate_id_for(self, step_id):
        return "gate-unit-" + str(step_id)

    def test_draft_when_no_verification(self):
        self.assertEqual(derive_approval_state([], "d1", gate_id_for=self.gate_id_for),
                         APPROVAL_DRAFT)

    def test_verified_requires_cp2_pass_event(self):
        events = [_cp2_pass_event("d1", 1)]
        self.assertEqual(derive_approval_state(events, "d1", gate_id_for=self.gate_id_for),
                         APPROVAL_VERIFIED)
        # 다른 step 의 CP2 Pass 는 이 step 을 verified 로 만들지 않는다.
        self.assertEqual(derive_approval_state(events, "d2", gate_id_for=self.gate_id_for),
                         APPROVAL_DRAFT)

    def test_approved_requires_cp3_pass_marker(self):
        log = EventLog(InMemoryEventStore())
        _cp2 = log.append(cycle_id="d1", to_stage="Complete", trigger="완료 조건 충족",
                          outcome="pass", actor=ROLE_VERIFIER, ref={"kind": "cp2-pass"})
        gid = self.gate_id_for("d1")
        from gates import append_approval_marker
        append_approval_marker(log, gid, GATE_APPROVAL_REQUIRED,
                               {"verdict": "Pass", "ref": "a"}, actor=ROLE_ADVISOR)
        events = log.all_events()
        self.assertEqual(derive_approval_state(events, "d1", gate_id_for=self.gate_id_for),
                         APPROVAL_APPROVED)

    def test_cp3_fail_marker_does_not_approve(self):
        log = EventLog(InMemoryEventStore())
        log.append(cycle_id="d1", to_stage="Complete", trigger="완료 조건 충족",
                   outcome="pass", actor=ROLE_VERIFIER, ref={"kind": "cp2-pass"})
        gid = self.gate_id_for("d1")
        from gates import append_approval_marker
        append_approval_marker(log, gid, GATE_APPROVAL_REQUIRED,
                               {"verdict": "Fail", "ref": "a"}, actor=ROLE_ADVISOR)
        # CP3 마커가 Fail 이면 verified 에 머문다(approved 아님).
        self.assertEqual(derive_approval_state(log.all_events(), "d1",
                         gate_id_for=self.gate_id_for), APPROVAL_VERIFIED)

    def test_user_approved_requires_eligible_user_resolution(self):
        log = EventLog(InMemoryEventStore())
        log.append(cycle_id="d1", to_stage="Complete", trigger="완료 조건 충족",
                   outcome="pass", actor=ROLE_VERIFIER, ref={"kind": "cp2-pass"})
        gid = self.gate_id_for("d1")
        policy = GatePolicy(user_actor_class="human")
        from gates import append_gate_requirement
        append_gate_requirement(log, gid, GATE_USER_DECISION_REQUIRED, actor="Advisor")
        # 부적격 actor(Advisor) 해소 → user_approved 아님(여전히 verified).
        append_gate_resolution(log, gid, GATE_USER_DECISION_REQUIRED, actor="Advisor")
        self.assertEqual(derive_approval_state(log.all_events(), "d1",
                         gate_id_for=self.gate_id_for, gate_policy=policy), APPROVAL_VERIFIED)
        # 적격 사용자(human) 해소 → user_approved.
        append_gate_resolution(log, gid, GATE_USER_DECISION_REQUIRED, actor="human")
        self.assertEqual(derive_approval_state(log.all_events(), "d1",
                         gate_id_for=self.gate_id_for, gate_policy=policy), APPROVAL_USER_APPROVED)

    def test_no_gate_id_for_limits_to_verified(self):
        # gate_id_for 미지정 → 게이트 축 파생 안 함(draft/verified 만).
        events = [_cp2_pass_event("d1", 1)]
        self.assertEqual(derive_approval_state(events, "d1"), APPROVAL_VERIFIED)


# ==========================================================================
# derive_registry — 순수·계보·정렬·재파생 동일 (done 2·mutable 저장 0)
# ==========================================================================
class DeriveRegistry(unittest.TestCase):
    def gate_id_for(self, step_id):
        return "gate-unit-" + str(step_id)

    def _decls(self):
        return [
            {"artifactId": "A", "version": 1, "supersedes": None, "derivedFrom": [],
             "location": "ws/A.v1", "contentHash": "sha256:1",
             "producedBy": {"stepId": "d1"}},
            {"artifactId": "A", "version": 2, "supersedes": 1, "derivedFrom": ["A@1"],
             "location": "ws/A.v2", "contentHash": "sha256:2",
             "producedBy": {"stepId": "d2"}},
        ]

    def test_lineage_preserved_and_sorted(self):
        reg = derive_registry(self._decls(), [], gate_id_for=self.gate_id_for)
        self.assertEqual([r.version for r in reg["A"]], [1, 2])  # 계보 전체·오름차순.
        self.assertEqual(reg["A"][1].supersedes, 1)
        self.assertEqual(reg["A"][1].derivedFrom, ["A@1"])
        # 문면(contentHash) 은 선언 그대로 보존(불변).
        self.assertEqual(reg["A"][0].contentHash, "sha256:1")

    def test_approval_state_derived_per_step_events(self):
        events = [_cp2_pass_event("d1", 1)]  # v1 만 CP2 Pass.
        reg = derive_registry(self._decls(), events, gate_id_for=self.gate_id_for)
        self.assertEqual(reg["A"][0].approvalState, APPROVAL_VERIFIED)  # v1 verified.
        self.assertEqual(reg["A"][1].approvalState, APPROVAL_DRAFT)     # v2 아직 draft.

    def test_pure_reproducible(self):
        events = [_cp2_pass_event("d1", 1)]
        r1 = derive_registry(self._decls(), events, gate_id_for=self.gate_id_for)
        r2 = derive_registry(self._decls(), events, gate_id_for=self.gate_id_for)
        self.assertEqual(
            {k: [x.to_dict() for x in v] for k, v in r1.items()},
            {k: [x.to_dict() for x in v] for k, v in r2.items()},
        )

    def test_duplicate_version_last_wins(self):
        decls = [
            {"artifactId": "A", "version": 1, "location": "old", "producedBy": {"stepId": "d1"}},
            {"artifactId": "A", "version": 1, "location": "new", "producedBy": {"stepId": "d1"}},
        ]
        reg = derive_registry(decls, [])
        self.assertEqual(len(reg["A"]), 1)
        self.assertEqual(reg["A"][0].location, "new")  # append-only latest.


# ==========================================================================
# resolve_references — 요구 등급·최신 버전만 (done 3)
# ==========================================================================
class ResolveReferences(unittest.TestCase):
    def _registry(self, v1_state, v2_state):
        return {
            "A": [
                ArtifactRecord(artifactId="A", version=1, approvalState=v1_state,
                               location="ws/A.v1", contentHash="sha256:1"),
                ArtifactRecord(artifactId="A", version=2, supersedes=1, approvalState=v2_state,
                               location="ws/A.v2", contentHash="sha256:2"),
            ]
        }

    def test_latest_qualifying_version_resolved(self):
        reg = self._registry(APPROVAL_VERIFIED, APPROVAL_VERIFIED)
        refs = resolve_references(reg, APPROVAL_VERIFIED)
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0].version, 2)  # 요구 등급 충족 중 최신.

    def test_below_grade_excluded(self):
        # v2 가 draft(미검증)면 요구 등급 verified 미달 → v1(verified)로 해석.
        reg = self._registry(APPROVAL_VERIFIED, APPROVAL_DRAFT)
        refs = resolve_references(reg, APPROVAL_VERIFIED)
        self.assertEqual(refs[0].version, 1)

    def test_none_qualifying_omits_artifact(self):
        reg = self._registry(APPROVAL_DRAFT, APPROVAL_DRAFT)
        # 요구 등급 approved 를 충족하는 버전이 없음 → 해석 안 됨(추측·인용 0).
        self.assertEqual(resolve_references(reg, APPROVAL_APPROVED), [])

    def test_higher_grade_requirement(self):
        reg = self._registry(APPROVAL_VERIFIED, APPROVAL_APPROVED)
        refs = resolve_references(reg, APPROVAL_APPROVED)
        self.assertEqual(refs[0].version, 2)  # approved 만 충족.


# ==========================================================================
# ArtifactCapturingInvoker — 완료 보고 artifacts 포집 (done 5)
# ==========================================================================
class CapturingInvoker(unittest.TestCase):
    def _request(self, role, step_id, capability="cap", model="tier-a", consumes=None):
        class _Req:
            pass
        req = _Req()
        req.role = role
        req.capability = capability
        req.model = model
        ifc = {"produces": ["A"]}
        if consumes is not None:
            ifc["consumes"] = consumes
        req.bundle = {"step_contract": {"id": step_id, "interfaceContract": ifc}}
        return req

    def test_captures_worker_artifacts_with_provenance(self):
        store = InMemoryArtifactDeclarationStore()

        class Inner(Invoker):
            def invoke(self, request):
                return InvokeResult(kind=KIND_COMPLETION,
                                    completion={"artifacts": ["ws/A.md"], "self_check": "ok"},
                                    ref="wr")
        cap = ArtifactCapturingInvoker(Inner(), store, run_id="run-1")
        cap.invoke(self._request(ROLE_WORKER, "d1", model="tier-c", consumes=["contract@v2"]))
        decls = store.read_all()
        self.assertEqual(len(decls), 1)
        self.assertEqual(decls[0]["artifactId"], "ws/A.md")
        self.assertEqual(decls[0]["producedBy"]["runId"], "run-1")
        self.assertEqual(decls[0]["producedBy"]["stepId"], "d1")
        self.assertEqual(decls[0]["producedBy"]["model"], "tier-c")
        self.assertEqual(decls[0]["derivedFrom"], ["contract@v2"])

    def test_verdict_return_not_captured(self):
        store = InMemoryArtifactDeclarationStore()

        class Inner(Invoker):
            def invoke(self, request):
                # verdict 반환에 artifacts 가 섞여 있어도 포집 제외(검증 단위 산출 아님).
                return InvokeResult(kind=KIND_COMPLETION,
                                    completion={"verdict": "Pass", "artifacts": ["x"]}, ref="vd")
        cap = ArtifactCapturingInvoker(Inner(), store)
        cap.invoke(self._request(ROLE_VERIFIER, "d1"))
        self.assertEqual(store.read_all(), [])

    def test_transparent_passthrough(self):
        store = InMemoryArtifactDeclarationStore()
        sentinel = InvokeResult(kind=KIND_COMPLETION, completion={"artifacts": ["A"]}, ref="wr")

        class Inner(Invoker):
            def invoke(self, request):
                return sentinel
        cap = ArtifactCapturingInvoker(Inner(), store)
        out = cap.invoke(self._request(ROLE_WORKER, "d1"))
        self.assertIs(out, sentinel)  # 반환 변경 0(투명).


# ==========================================================================
# 선언 원장 저장 — JSONL append-only (PO-INV 2)
# ==========================================================================
class DeclarationStore(unittest.TestCase):
    def test_jsonl_append_only_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "artifacts.jsonl")
            store = JsonlArtifactDeclarationStore(path)
            store.append({"artifactId": "A", "version": 1})
            store.append({"artifactId": "A", "version": 2})
            # 재로드해도 두 선언 모두 보존(기존 행 불변).
            store2 = JsonlArtifactDeclarationStore(path)
            self.assertEqual([d["version"] for d in store2.read_all()], [1, 2])


# ==========================================================================
# (i) 통합 — 설계 v1 → rework v2 → 소비 번들 required_grade·v1 문면 불변 (done 4)
#
# 모의 invoker 로 orchestrator 를 실제 구동한다: 설계 단위가 v1 산출 → CP2 Pass(verified)
# → 리뷰 반려를 근거로 rework(task_superseded) revision → v2(supersedes v1·derivedFrom
# 기록) → CP2 Pass → 소비 단위 번들이 resolve_references(verified)로 최신 검증 버전만
# 참조. v1 문면(물리 파일 해시)은 v2 산출 후에도 불변임을 실측한다.
# ==========================================================================
def _design_task(tid, version, supersedes=None, derived_from=None, workdir=None):
    """설계 단위 Task — 산출 artifact 선언 템플릿을 interfaceContract 에 싣는다.

    Step.contract() 는 interfaceContract 를 온전히 보존하므로(step.py) 모의 invoker 가
    이 템플릿을 읽어 물리 파일을 쓰고 구조화 선언을 반환한다. 07 Task 는 interfaceContract
    를 임의 dict 로 수용한다(개방 데이터).
    """
    location = (os.path.join(workdir, "design-memo.v%d.md" % version)
                if workdir else "design-memo.v%d.md" % version)
    ifc = {
        "produces": ["design-memo"],
        "_decl": {
            "version": version,
            "supersedes": supersedes,
            "derivedFrom": list(derived_from or []),
            "location": location,
        },
    }
    if derived_from is not None:
        ifc["consumes"] = list(derived_from)
    return {
        "id": tid,
        "task": "설계 메모 산출 " + tid,
        "done": "design-memo v" + str(version) + " 산출",
        "interfaceContract": ifc,
        "ownedBoundary": ["design-memo"],
        "dependsOn": [],
        "delegation": {
            "from": "Advisor", "to": "Worker", "task": "설계",
            "input": "contract", "output": "design-memo", "done": "AC",
            "context": ["contract"], "constraints": None,
        },
        "capability": "cap-design",
        "role": "Worker", "model": "tier-c",
    }


class ArtifactAwareInvoker(Invoker):
    """설계 단위는 구조화 artifact 선언을 완료 보고에 실어 반환하고, 물리 파일을 쓴다.

    Verifier/Advisor 는 verdict(Pass) 반환. Worker 완료 보고의 artifacts 에 구조화 선언
    (version·supersedes·derivedFrom·location·contentHash)을 실어 ArtifactCapturingInvoker
    가 포집하도록 한다. 물리 파일을 써서 v1 문면 불변을 실측할 수 있게 한다.
    """

    def __init__(self):
        self.written = {}  # location -> content(해시 대조용)

    def invoke(self, request):
        role = request.role
        sc = request.bundle.get("step_contract") or {}
        if role == ROLE_VERIFIER:
            return InvokeResult(kind=KIND_COMPLETION,
                                completion={"verdict": "Pass", "rework": None}, ref="vd")
        if role == ROLE_ADVISOR:
            return InvokeResult(kind=KIND_COMPLETION,
                                completion={"verdict": "Pass"}, ref="ad")
        # Worker — interfaceContract._decl 템플릿을 읽어 물리 파일 산출 + 구조화 선언.
        decl_tpl = (sc.get("interfaceContract") or {}).get("_decl") or {}
        version = decl_tpl.get("version", 1)
        location = decl_tpl.get("location")
        content = "DESIGN-MEMO-CONTENT-v%d" % version
        if location:
            os.makedirs(os.path.dirname(os.path.abspath(location)), exist_ok=True)
            with open(location, "w", encoding="utf-8") as fh:
                fh.write(content)
            self.written[location] = content
        decl = {
            "artifactId": "design-memo",
            "version": version,
            "supersedes": decl_tpl.get("supersedes"),
            "derivedFrom": decl_tpl.get("derivedFrom") or [],
            "location": location,
            "contentHash": content_hash(content),
        }
        return InvokeResult(
            kind=KIND_COMPLETION,
            completion={"artifacts": [decl], "self_check": "ok", "failures": "없음",
                        "open_questions": "없음", "verify_basis": "self"},
            ref="wr",
        )


class ScenarioI_ArtifactLineage(unittest.TestCase):
    def test_v1_rework_v2_supersedes_and_resolve_and_immutability(self):
        with tempfile.TemporaryDirectory() as ws:
            inv = ArtifactAwareInvoker()
            store = InMemoryEventStore()
            art_store = InMemoryArtifactDeclarationStore()
            graph = {"goal": "설계", "tasks": [_design_task("d1", 1, workdir=ws)],
                     "completion": "all-passed"}
            ledger = RevisionLedger(InMemoryRevisionStore(), graph)
            orch = ProjectOrchestrator(ledger, store, inv, artifact_store=art_store,
                                       run_id="maturation-r001")

            # (1) 설계 v1 산출 → CP2 Pass(verified).
            r1 = orch.run()
            self.assertTrue(r1.completed, r1.status)
            reg = orch.artifact_registry()
            self.assertEqual([r.version for r in reg["design-memo"]], [1])
            self.assertEqual(reg["design-memo"][0].approvalState, APPROVAL_VERIFIED)
            v1_location = reg["design-memo"][0].location
            v1_hash_after_v1 = hash_file(v1_location)

            # (2) 리뷰 반려를 근거로 rework revision(task_superseded) — 게이트 통과 이벤트 근거.
            #     게이트 통과(해소) 이벤트를 append 해 revision 을 근거짓는다(PO-INV 5).
            gid = "review-gate-d1"
            append_gate_resolution(orch.log, gid, GATE_APPROVAL_REQUIRED, actor="Advisor")
            d2 = _design_task("d2", 2, supersedes="d1", derived_from=["design-memo"], workdir=ws)
            d2["supersedes"] = "d1"
            orch.accept_revision(
                KIND_TASK_SUPERSEDED,
                {**{k: v for k, v in d2.items()}, "supersedes": "d1"},
                proposingStepRef="d1", gateEventRef=gid,
            )

            # (3) 재구동 — v2 산출(supersedes v1·derivedFrom 기록) → CP2 Pass(verified).
            r2 = orch.run()
            self.assertTrue(r2.completed, r2.status)
            reg2 = orch.artifact_registry()
            versions = [r.version for r in reg2["design-memo"]]
            self.assertEqual(versions, [1, 2])  # 계보 전체 보존(v1 삭제 0).
            v2 = reg2["design-memo"][1]
            self.assertEqual(v2.supersedes, "d1")
            self.assertEqual(v2.derivedFrom, ["design-memo"])
            self.assertEqual(v2.approvalState, APPROVAL_VERIFIED)

            # (4) 소비 번들 확정 참조 — required_grade=verified 의 최신 버전만(v2).
            refs = orch.resolve_references(APPROVAL_VERIFIED)
            memo_refs = [r for r in refs if r.artifactId == "design-memo"]
            self.assertEqual(len(memo_refs), 1)
            self.assertEqual(memo_refs[0].version, 2)  # 최신 검증 버전.

            # (5) v1 문면 불변 — v2 산출 후에도 v1 물리 파일 해시 동일(location 분리·불변).
            self.assertNotEqual(v1_location, v2.location)  # 버전별 별도 파일.
            self.assertEqual(hash_file(v1_location), v1_hash_after_v1)  # v1 바이트 불변.
            self.assertEqual(reg2["design-memo"][0].contentHash, v1_hash_after_v1)

    def test_registry_is_rederived_not_stored(self):
        # mutable 저장 0 — 같은 두 원장에서 매번 새로 파생(PO-INV 2·제2 진리원천 아님).
        with tempfile.TemporaryDirectory() as ws:
            inv = ArtifactAwareInvoker()
            store = InMemoryEventStore()
            art_store = InMemoryArtifactDeclarationStore()
            graph = {"goal": "g", "tasks": [_design_task("d1", 1, workdir=ws)],
                     "completion": "all-passed"}
            orch = ProjectOrchestrator(RevisionLedger(InMemoryRevisionStore(), graph),
                                       store, inv, artifact_store=art_store)
            orch.run()
            a = orch.artifact_registry()
            b = orch.artifact_registry()
            self.assertIsNot(a, b)  # 매 호출 새 객체(저장된 상태 아님).
            self.assertEqual({k: [x.to_dict() for x in v] for k, v in a.items()},
                             {k: [x.to_dict() for x in v] for k, v in b.items()})


# ==========================================================================
# find_valid_cp2_evidence — 유효 cp2-pass 탐색 + stale 3규칙 (순수·fail-closed·T2)
# ==========================================================================
def _cp2(cycle, at, seq=1, verdict_ref="v"):
    return {"cycle_id": cycle, "seq": seq, "from_stage": "Verify", "to_stage": "Complete",
            "trigger": "완료 조건 충족", "outcome": "pass", "actor": ROLE_VERIFIER,
            "ref": {"kind": "cp2-pass", "verdict_ref": verdict_ref}, "at": at}


def _dispatch(cycle, at, seq=1):
    return {"cycle_id": cycle, "seq": seq, "from_stage": None, "to_stage": "Execute",
            "trigger": "완료 조건 충족", "outcome": "pass", "actor": ROLE_WORKER,
            "ref": {"kind": "dispatch"}, "at": at}


def _fail(cycle, at, seq=1):
    return {"cycle_id": cycle, "seq": seq, "from_stage": "Verify", "to_stage": "Verify",
            "trigger": "Verify 실패", "outcome": "fail", "actor": ROLE_VERIFIER,
            "ref": {"kind": "rework"}, "at": at}


def _gate_pass(gate_id, at):
    return {"cycle_id": "gate::" + gate_id, "seq": 1, "from_stage": "Consult",
            "to_stage": "Complete", "trigger": "완료 조건 충족", "outcome": "pass",
            "actor": "human", "ref": {"kind": "gate-resolved", "gate_id": gate_id}, "at": at}


class FindValidCp2Evidence(unittest.TestCase):
    # --- 부재·기본 유효 ---------------------------------------------------
    def test_absent_when_no_cp2_pass(self):
        f = find_valid_cp2_evidence([], "u")
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_ABSENT)
        self.assertIsNone(f.basis)

    def test_valid_basic_carries_provenance_basis(self):
        events = [_dispatch("u", 1), _cp2("u", 2, seq=2, verdict_ref="vd")]
        f = find_valid_cp2_evidence(events, "u")
        self.assertTrue(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_VALID)
        self.assertEqual(f.basis, {
            "kind": "cp2-pass", "at": 2, "seq": 2, "cycle_id": "u", "verdict_ref": "vd",
        })

    def test_latest_cp2_pass_is_basis(self):
        # 재시도(dispatch→fail→dispatch→cp2-pass) — 최종 cp2-pass 를 근거로(중간 fail 무해).
        events = [_dispatch("u", 1), _fail("u", 2, seq=2), _dispatch("u", 3, seq=3), _cp2("u", 4, seq=4)]
        f = find_valid_cp2_evidence(events, "u")
        self.assertTrue(f.valid)
        self.assertEqual(f.basis["at"], 4)

    # --- rule (a) 재실행/retry -------------------------------------------
    def test_stale_a_reopened_after_cp2_pass(self):
        # cp2-pass 이후 같은 cycle 재디스패치 → 최종 판정 아님 → stale.
        events = [_dispatch("u", 1), _cp2("u", 2, seq=2), _dispatch("u", 3, seq=3)]
        f = find_valid_cp2_evidence(events, "u")
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_REOPENED)

    def test_other_cycle_event_after_does_not_reopen(self):
        # 다른 cycle 의 후속 이벤트는 이 cycle 의 evidence 를 stale 로 만들지 않는다.
        events = [_cp2("u", 2), _dispatch("other", 3)]
        f = find_valid_cp2_evidence(events, "u")
        self.assertTrue(f.valid)

    # --- rule (b) supersede/revision 영향 --------------------------------
    def test_stale_b_reissue_revision_after_evidence(self):
        # 재발행(id==u) revision grounded at 5 > cp2-pass at 2 → stale.
        events = [_cp2("u", 2), _gate_pass("g1", 5)]
        rev = {"kind": KIND_TASK_SUPERSEDED, "payload": {"supersedes": "u", "id": "u"},
               "basis": {"gateEventRef": "g1"}}
        f = find_valid_cp2_evidence(events, "u", revisions=[rev])
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_REVISION)

    def test_valid_when_creating_revision_precedes_evidence(self):
        # task_added(id==u) grounded at 1 <= cp2-pass at 4 → evidence 는 개정본을 검증(무관·valid).
        # orch-w 실거동 대응: impl 단위는 task_added 로 생성 후 실행·cp2-pass(생성 선행).
        events = [_gate_pass("g1", 1), _dispatch("u", 2), _cp2("u", 4, seq=2)]
        rev = {"kind": KIND_TASK_ADDED, "payload": {"id": "u"}, "basis": {"gateEventRef": "g1"}}
        f = find_valid_cp2_evidence(events, "u", revisions=[rev])
        self.assertTrue(f.valid)

    def test_unrelated_revision_ignored(self):
        # 다른 task 를 대상하는 revision 은 무관 → valid.
        events = [_cp2("u", 2), _gate_pass("g1", 5)]
        rev = {"kind": KIND_TASK_ADDED, "payload": {"id": "other"}, "basis": {"gateEventRef": "g1"}}
        f = find_valid_cp2_evidence(events, "u", revisions=[rev])
        self.assertTrue(f.valid)

    def test_dependency_added_after_evidence_is_stale(self):
        events = [_cp2("u", 2), _gate_pass("g1", 5)]
        rev = {"kind": KIND_DEPENDENCY_ADDED, "payload": {"id": "u", "dependsOn": ["x"]},
               "basis": {"gateEventRef": "g1"}}
        f = find_valid_cp2_evidence(events, "u", revisions=[rev])
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_REVISION)

    def test_stale_b_unknown_kind_fail_closed(self):
        # 미지 revision kind → 무엇을 대상하는지 알 수 없음 → fail-closed stale.
        events = [_cp2("u", 2), _gate_pass("g1", 1)]
        rev = {"kind": "frobnicate", "payload": {"id": "u"}, "basis": {"gateEventRef": "g1"}}
        f = find_valid_cp2_evidence(events, "u", revisions=[rev])
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_UNKNOWN_REVISION)

    def test_stale_b_grounding_unprovable_fail_closed(self):
        # touches=True 이나 gateEventRef 부재(근거 통과 이벤트 미실재) → 순서 증명 불가 → stale.
        events = [_cp2("u", 2)]
        rev = {"kind": KIND_TASK_SUPERSEDED, "payload": {"supersedes": "u", "id": "u2"},
               "basis": {"gateEventRef": None}}
        f = find_valid_cp2_evidence(events, "u", revisions=[rev])
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_REVISION)

    # --- rule (c) artifact 해시 -----------------------------------------
    def test_vacuous_c_when_no_recorded_hash(self):
        # 해시 미기록(baseline 전부 null) → rule (c) 공허 통과(valid). hash_observer 무관.
        rec = ArtifactRecord(artifactId="a", producedBy={"stepId": "u"}, location="/x", contentHash=None)
        f = find_valid_cp2_evidence([_cp2("u", 2)], "u", artifact_records=[rec])
        self.assertTrue(f.valid)

    def test_stale_c_recorded_hash_mismatch(self):
        rec = ArtifactRecord(artifactId="a", producedBy={"stepId": "u"}, location="/x",
                             contentHash="sha256:aaa")
        f = find_valid_cp2_evidence(
            [_cp2("u", 2)], "u", artifact_records=[rec], hash_observer=lambda loc: "sha256:bbb"
        )
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_HASH)

    def test_valid_c_recorded_hash_match(self):
        rec = ArtifactRecord(artifactId="a", producedBy={"stepId": "u"}, location="/x",
                             contentHash="sha256:aaa")
        f = find_valid_cp2_evidence(
            [_cp2("u", 2)], "u", artifact_records=[rec], hash_observer=lambda loc: "sha256:aaa"
        )
        self.assertTrue(f.valid)

    def test_stale_c_recorded_hash_unobservable_fail_closed(self):
        # 해시 기록됨 + 관측 수단 없음(hash_observer None) → 문면 불변 확인 불가 → fail-closed.
        rec = ArtifactRecord(artifactId="a", producedBy={"stepId": "u"}, location="/x",
                             contentHash="sha256:aaa")
        f = find_valid_cp2_evidence([_cp2("u", 2)], "u", artifact_records=[rec])
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_HASH)

    def test_hash_observer_exception_is_fail_closed(self):
        def boom(loc):
            raise OSError("gone")
        rec = ArtifactRecord(artifactId="a", producedBy={"stepId": "u"}, location="/x",
                             contentHash="sha256:aaa")
        f = find_valid_cp2_evidence([_cp2("u", 2)], "u", artifact_records=[rec], hash_observer=boom)
        self.assertFalse(f.valid)
        self.assertEqual(f.reason, CP2_EVIDENCE_STALE_HASH)

    def test_hash_rule_ignores_other_step_records(self):
        # 다른 step 산출의 해시 불일치는 이 step evidence 를 stale 로 만들지 않는다.
        rec = ArtifactRecord(artifactId="a", producedBy={"stepId": "other"}, location="/x",
                             contentHash="sha256:aaa")
        f = find_valid_cp2_evidence(
            [_cp2("u", 2)], "u", artifact_records=[rec], hash_observer=lambda loc: "sha256:bbb"
        )
        self.assertTrue(f.valid)

    def test_is_pure_no_input_mutation(self):
        events = [_cp2("u", 2)]
        snapshot = [dict(e) for e in events]
        find_valid_cp2_evidence(events, "u")
        self.assertEqual(events, snapshot)


# ==========================================================================
# 스키마 정합 — artifact_record_schema.json 유효성·enum 대조 (단일 진리원천)
# ==========================================================================
class SchemaConsistency(unittest.TestCase):
    def test_artifact_record_schema_valid_and_enum_matches_code(self):
        import json
        path = os.path.join(_ORCH_DIR, "artifact_record_schema.json")
        with open(path, "r", encoding="utf-8") as fh:
            schema = json.load(fh)
        self.assertEqual(schema["type"], "object")
        enum = schema["properties"]["approvalState"]["enum"]
        self.assertEqual(tuple(enum), APPROVAL_LADDER)  # 스키마 enum = 코드 사다리.


if __name__ == "__main__":
    unittest.main(verbosity=2)
