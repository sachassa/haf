"""Artifact Record·Registry — 파생 인덱스 (05 §3.6·PO-INV 7·2·8·판단 0).

이 모듈이 소유하는 것(05 §3.6 — 본 Layer 신규 소유 계약의 실현):
  - ArtifactRecord — 8필드 산출물 계보·provenance 레코드(05 §3.6 표 그대로).
  - approvalState 파생 사다리 — draft → verified(CP2 Pass) → approved(CP3) →
    user_approved(사용자 게이트 해소). **mutable 필드가 아니라 게이트/검증 이벤트의
    파생 뷰**다(PO-INV 7). 각 등급은 대응 이벤트 실재에서만 파생된다.
  - Artifact Declaration 원장 — 완료 보고(02 §3.2-C `artifacts`)에서 append-only 로
    포집한 산출물 선언(인메모리+JSONL). **레지스트리는 이 선언 원장과 게이트/검증
    이벤트에서 파생되는 인덱스이며 제2 진리원천이 아니다**(05 §3.6·PO-INV 2 — 별도
    mutable 저장 0).
  - derive_registry() — (선언 원장, 이벤트 로그) → {artifactId: [ArtifactRecord]}
    **순수 함수**. approvalState 를 게이트/검증 이벤트에서 파생한다.
  - resolve_references() — 번들 조립용 확정 참조 해석. 요구 등급 이상 approvalState 의
    **최신 버전만** 해석한다(05 §3.6 — 미완성·미승인 산출물 추측·인용 0).

판단 0(PO-INV 1): 이 모듈은 산출물의 의미(무엇이 좋은 산출물인가)를 판정하지 않는다 —
완료 보고에서 선언을 포집하고, 게이트/검증 이벤트에서 approvalState 를 파생하며, 등급
비교로 확정 참조를 해석한다. 검증·승인의 실제 판정은 CP2 Verifier·CP3 Advisor·사용자가
소유하고, 이 모듈은 그 이벤트의 실재를 파생 판독만 한다.

계보 append-only(PO-INV 7): `supersedes` 는 삭제가 아니라 계보 append 이며 과거 버전
문면(`location`+`contentHash` 뒤의 내용)은 불변이다(03-project-contract §3.4·PC-INV 9
동형). derive_registry 는 계보 전체를 보존하고 resolve 만 최신 등급 충족 버전을 고른다.

특정 provider·모델·상류 Layer 고유명 토큰은 이 모듈 어디에도 두지 않는다(PO-INV 8).
approvalState 어휘(draft/verified/approved/user_approved)·verdict `Pass` 는 05 §3.6·
06 §3.2-C 계약 어휘이며 provider 토큰이 아니다.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol

# 게이트/검증 이벤트 파생 판독은 같은 Layer 중립 모듈 gates.py 에 위임한다(재구현 0).
# gates.py 는 provider·모델 토큰 0 이며, approvalState 는 05 §3.6 이 게이트 이벤트로
# 정의하므로 이 결속은 계약 정합이다(PO-INV 8 보존).
from gates import (
    GATE_USER_DECISION_REQUIRED,
    REF_KIND_APPROVAL,
    GatePolicy,
    is_resolved,
    latest_marker_verdict,
)

# revision kind 어휘는 같은 Layer 중립 leaf 모듈 revision.py 가 소유한다(재정의 0). review
# evidence 재사용 판정(아래 find_valid_cp2_evidence)의 stale 규칙 (b)가 revision 이 task 를
# 대상하는지 판독하는 데 쓴다. revision.py 는 이 계층 어떤 모듈도 import 하지 않는 leaf 라
# 순환이 없다(artifacts→revision·artifacts→gates 둘 다 acyclic).
from revision import (
    KIND_DEPENDENCY_ADDED,
    KIND_TASK_ADDED,
    KIND_TASK_SUPERSEDED,
)


# ==========================================================================
# approvalState 파생 사다리 (05 §3.6 — 어휘·전순서 정본)
# ==========================================================================
APPROVAL_DRAFT = "draft"                 # 0 — 선언만(검증 이벤트 부재)
APPROVAL_VERIFIED = "verified"           # 1 — CP2 Pass 이벤트 실재
APPROVAL_APPROVED = "approved"           # 2 — CP3(Advisor 역할 승인) 이벤트 실재
APPROVAL_USER_APPROVED = "user_approved" # 3 — 사용자 게이트 해소 이벤트 실재

# 오름차순(약 → 강). 인덱스가 곧 등급 값이다(전순서).
APPROVAL_LADDER = (
    APPROVAL_DRAFT,
    APPROVAL_VERIFIED,
    APPROVAL_APPROVED,
    APPROVAL_USER_APPROVED,
)
_APPROVAL_INDEX = {state: index for index, state in enumerate(APPROVAL_LADDER)}

# CP2 Pass 이벤트 마커 — host.py 가 CP2 통과 시 append 하는 ref.kind(중립 어휘).
CP2_PASS_REF_KIND = "cp2-pass"

# verdict 어휘(06 §3.2-C). CP3 승인 마커의 status 소비에만 쓰인다(내용 판정 0·PO-INV 1).
VERDICT_PASS = "Pass"


def approval_grade(state: Any) -> int:
    """approvalState 의 전순서 등급 값. 미지의 값은 ValueError(추측 금지·O4)."""
    if state not in _APPROVAL_INDEX:
        raise ValueError("알 수 없는 approvalState: " + repr(state))
    return _APPROVAL_INDEX[state]


def content_hash(data: Any) -> str:
    """문면 불변 증빙용 결정적 해시(선택 필드 `contentHash` 산출).

    str 은 utf-8 바이트로, bytes 는 그대로 해싱한다. 순수 함수 — 같은 내용 → 같은 해시.
    provider 토큰이 아니라 표준 해시 알고리즘이다(PO-INV 8 무관).
    """
    if isinstance(data, str):
        raw = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        raw = bytes(data)
    else:
        raise TypeError("content_hash 는 str/bytes 만 받는다")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def hash_file(path: str) -> str:
    """파일 내용의 결정적 해시(문면 불변 실측용). 파일을 읽기만 한다(변경 0)."""
    with open(path, "rb") as fh:
        return "sha256:" + hashlib.sha256(fh.read()).hexdigest()


# ==========================================================================
# ArtifactRecord — 본 Layer 신규 소유 레코드 8필드 (05 §3.6 표)
# ==========================================================================
@dataclass
class ArtifactRecord:
    """산출물 계보·provenance 레코드.

    필드 소유 정본(05 §3.6):
      artifactId    -> 논리 식별자.
      version       -> append-only 인스턴스 버전(단조).
      supersedes    -> 직전 버전 참조 — 기존 문면 불변(PC-INV 9 동형). 없으면 None.
      derivedFrom   -> 입력 artifact 참조 목록(07 interfaceContract consumes 실측치).
      producedBy    -> provenance {runId·stepId·attempt·role·capability·model} — **불투명
                       부속**(SP-INV 3 동형). 소비 조건으로 쓰지 않는다.
      approvalState -> **게이트/검증 이벤트 파생 뷰**(PO-INV 7). 직접 쓰지 않는다.
      location      -> 워크스페이스 물리 경로(Adapter 소관·SP-INV 7 귀속).
      contentHash   -> 선택 — 문면 불변 증빙(없으면 None).
    """

    artifactId: str
    version: int = 1
    supersedes: Any = None
    derivedFrom: list[Any] = field(default_factory=list)
    producedBy: dict[str, Any] = field(default_factory=dict)
    approvalState: str = APPROVAL_DRAFT
    location: Any = None
    contentHash: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifactId": self.artifactId,
            "version": self.version,
            "supersedes": self.supersedes,
            "derivedFrom": list(self.derivedFrom),
            "producedBy": dict(self.producedBy),
            "approvalState": self.approvalState,
            "location": self.location,
            "contentHash": self.contentHash,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ArtifactRecord":
        if not isinstance(data, dict):
            raise TypeError("ArtifactRecord 직렬화는 매핑이어야 한다")
        if not data.get("artifactId"):
            raise ValueError("ArtifactRecord 에 artifactId 가 없다")
        return cls(
            artifactId=str(data["artifactId"]),
            version=int(data.get("version", 1)),
            supersedes=data.get("supersedes"),
            derivedFrom=list(data.get("derivedFrom") or []),
            producedBy=dict(data.get("producedBy") or {}),
            approvalState=data.get("approvalState", APPROVAL_DRAFT),
            location=data.get("location"),
            contentHash=data.get("contentHash"),
        )


# ==========================================================================
# Artifact Declaration — 완료 보고에서 포집하는 append-only 선언(05 §3.6)
#
# 선언은 approvalState 를 담지 않는다(그것은 파생 뷰다). 선언 원장은 이벤트 로그·revision
# 원장과 같은 append-only 원칙 위의 provenance 원장이며, 레지스트리는 이 선언과 이벤트에서
# 파생될 뿐 별도 mutable 상태로 저장되지 않는다(PO-INV 2 — 제2 진리원천 아님).
# ==========================================================================
DECLARATION_FIELDS = (
    "artifactId",
    "version",
    "supersedes",
    "derivedFrom",
    "producedBy",
    "location",
    "contentHash",
)


def normalize_declaration(
    entry: Any,
    *,
    producedBy: dict[str, Any] | None = None,
    default_derived_from: Iterable[Any] | None = None,
) -> dict[str, Any]:
    """완료 보고 artifacts 항목을 표준 선언 dict 로 정규화한다(05 §3.6 임의 형태 수용).

    - 문자열(경로)  -> 최소 선언(artifactId=location=경로·version 1·supersedes None).
    - dict          -> 구조화 선언(artifactId·version·supersedes·derivedFrom·location·
                       contentHash·(선택) producedBy). 명시값 우선.
    producedBy 는 선언에 명시가 있으면 존중하고, 없으면 인자 producedBy 를 붙인다(포집 지점의
    provenance). 선언은 approvalState 를 담지 않는다(파생 뷰).
    """
    if isinstance(entry, str):
        decl: dict[str, Any] = {
            "artifactId": entry,
            "version": 1,
            "supersedes": None,
            "derivedFrom": list(default_derived_from or []),
            "location": entry,
            "contentHash": None,
        }
        own_provenance = None
    elif isinstance(entry, dict):
        aid = entry.get("artifactId") or entry.get("location") or entry.get("id")
        if not aid:
            raise ValueError("artifact 선언 dict 에 artifactId/location 이 없다")
        decl = {
            "artifactId": str(aid),
            "version": int(entry.get("version", 1)),
            "supersedes": entry.get("supersedes"),
            "derivedFrom": list(
                entry.get("derivedFrom")
                if entry.get("derivedFrom") is not None
                else (default_derived_from or [])
            ),
            "location": entry.get("location", aid),
            "contentHash": entry.get("contentHash"),
        }
        own_provenance = entry.get("producedBy")
    else:
        raise TypeError("artifact 선언은 문자열(경로) 또는 dict 여야 한다")

    if own_provenance:
        decl["producedBy"] = dict(own_provenance)
    elif producedBy is not None:
        decl["producedBy"] = dict(producedBy)
    else:
        decl["producedBy"] = {}
    return decl


class ArtifactDeclarationStore(Protocol):
    """append-only 선언 저장 추상. 직렬화 형식은 구현체(Adapter) 소관이다."""

    def append(self, declaration: dict[str, Any]) -> None: ...

    def read_all(self) -> list[dict[str, Any]]: ...


class InMemoryArtifactDeclarationStore:
    """테스트·비영속 용 append-only 저장. 기존 선언은 재작성·삭제하지 않는다(PO-INV 2)."""

    def __init__(self, seed: Iterable[dict[str, Any]] | None = None) -> None:
        self._declarations: list[dict[str, Any]] = [dict(d) for d in (seed or [])]

    def append(self, declaration: dict[str, Any]) -> None:
        self._declarations.append(dict(declaration))

    def read_all(self) -> list[dict[str, Any]]:
        return [dict(d) for d in self._declarations]


class JsonlArtifactDeclarationStore:
    """파일 기반 append-only 저장 — 1행 = 1선언(자기서술 데이터 객체).

    갱신·정정은 기존 행을 바꾸지 않고 새 선언 행을 추가한다(append-only·PO-INV 2).
    events.py JsonlEventStore·revision.py JsonlRevisionStore 와 동형이다.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        directory = os.path.dirname(os.path.abspath(path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(path):
            with open(path, "a", encoding="utf-8"):
                pass

    def append(self, declaration: dict[str, Any]) -> None:
        line = json.dumps(declaration, ensure_ascii=False, sort_keys=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        declarations: list[dict[str, Any]] = []
        with open(self.path, "r", encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if raw:
                    declarations.append(json.loads(raw))
        return declarations


# ==========================================================================
# ArtifactCapturingInvoker — 완료 보고 artifacts 를 선언 원장에 포집(05 §3.6)
#
# 중립 Invoker 계약을 감싸는 데코레이터다. inner.invoke 를 그대로 호출하고(재정의 0),
# Worker 완료 보고에 artifacts 가 있으면 선언을 포집·append 한다. CP2/CP3 반환(verdict)은
# artifacts 가 없으므로 포집되지 않는다. Host 는 이 래퍼를 일반 Invoker 로만 본다(무수정).
# ==========================================================================
class ArtifactCapturingInvoker:
    """Invoker 래퍼 — 완료 보고 artifacts → 선언 원장 append(provenance 포집).

    inner 의 반환을 변경하지 않고 그대로 통과시킨다(투명). 포집은 부작용(선언 append)이며
    실행 결과에 영향을 주지 않는다. runId 는 provenance 부속으로만 기록된다(불투명·SP-INV 3).
    """

    # role 어휘(02 §3.2-A). Worker 완료만 산출물을 낸다 — Verifier/Advisor 반환은 verdict.
    ROLE_WORKER = "Worker"

    def __init__(self, inner: Any, store: ArtifactDeclarationStore, *, run_id: Any = None) -> None:
        self.inner = inner
        self.store = store
        self.run_id = run_id

    def invoke(self, request: Any) -> Any:
        result = self.inner.invoke(request)
        try:
            self._maybe_capture(request, result)
        except Exception:
            # 포집 실패가 실행을 오염시키지 않도록 격리한다(포집은 파생 인덱스 부속·판단 0).
            # 은폐가 아니다 — 실행 결과(result)는 그대로 반환되고 선언만 누락될 수 있으며,
            # 그 경우 레지스트리는 해당 산출물을 단순히 알지 못한다(추측 0).
            pass
        return result

    def _maybe_capture(self, request: Any, result: Any) -> None:
        completion = getattr(result, "completion", None)
        if not isinstance(completion, dict):
            return
        artifacts = completion.get("artifacts")
        if not artifacts:
            return
        # verdict 반환(Verifier/Advisor)은 산출물 선언이 아니다 — 포집 제외.
        if "verdict" in completion:
            return
        bundle = getattr(request, "bundle", None) or {}
        sc = bundle.get("step_contract") or {}
        step_id = sc.get("id")
        ifc = sc.get("interfaceContract") or {}
        consumes = ifc.get("consumes")
        if consumes is None:
            consumes = sc.get("dependsOn") or []
        provenance = {
            "runId": self.run_id,
            "stepId": step_id,
            "attempt": completion.get("attempt"),
            "role": getattr(request, "role", None),
            "capability": getattr(request, "capability", None),
            "model": getattr(request, "model", None),
        }
        for entry in artifacts:
            decl = normalize_declaration(
                entry, producedBy=provenance, default_derived_from=consumes
            )
            self.store.append(decl)


# ==========================================================================
# approvalState 파생 — 게이트/검증 이벤트 파생 뷰 (05 §3.6·PO-INV 7·판단 0)
# ==========================================================================
def derive_approval_state(
    events: Iterable[dict[str, Any]],
    step_id: Any,
    *,
    gate_id_for: Any = None,
    gate_policy: GatePolicy | None = None,
) -> str:
    """산출물을 낸 step 의 검증/게이트 이벤트에서 approvalState 를 파생한다(직접 쓰지 않음).

    사다리(각 등급은 대응 이벤트 실재에서만 파생·최고 등급 채택):
      - verified      : 산출 step 의 CP2 Pass 이벤트 실재(host.py `cp2-pass`).
      - approved      : 산출 step 게이트의 CP3(Advisor) 승인 마커 verdict == Pass.
      - user_approved : 산출 step 게이트의 user_decision 게이트가 적격 사용자 actor 로 해소.
    gate_id_for 미지정 시 게이트 축(approved/user_approved)은 파생하지 않는다(draft/verified).

    순수 함수(events·정책만으로 결정). 게이트 판독은 gates.py 순수 함수에 위임한다(재구현 0).
    """
    events = list(events)
    grade = APPROVAL_DRAFT

    # verified — CP2 Pass 이벤트(대상 step cycle).
    for e in events:
        if (
            e.get("cycle_id") == step_id
            and e.get("outcome") == "pass"
            and isinstance(e.get("ref"), dict)
            and e["ref"].get("kind") == CP2_PASS_REF_KIND
        ):
            grade = _max_grade(grade, APPROVAL_VERIFIED)
            break

    if gate_id_for is not None and step_id is not None:
        gate_id = gate_id_for(step_id)
        # approved — CP3 승인 마커 status(내용 판정 0·PO-INV 1).
        if latest_marker_verdict(events, gate_id, REF_KIND_APPROVAL) == VERDICT_PASS:
            grade = _max_grade(grade, APPROVAL_APPROVED)
        # user_approved — user_decision 게이트가 적격 사용자 actor 로 해소(확정 권위 보존).
        policy = gate_policy if gate_policy is not None else GatePolicy()
        if is_resolved(events, gate_id, GATE_USER_DECISION_REQUIRED, policy):
            grade = _max_grade(grade, APPROVAL_USER_APPROVED)

    return grade


def _max_grade(a: str, b: str) -> str:
    return a if approval_grade(a) >= approval_grade(b) else b


# ==========================================================================
# review_required evidence 재사용 판정 — 유효 cp2-pass 탐색 + stale 3규칙
#   (순수·fail-closed·판단 0 — 05 §3.3 review_required · T2)
#
# review_required 게이트를 재검증 Verifier 세션 재기동 대신 **이미 기록된 유효 cp2-pass
# (host 가 CP2 Pass 시 append)를 소비**해 해소하기 위한 순수 판독 함수다. cp2-pass 실재는
# Verifier 의 기록된 Pass 이며, 이 함수는 그 실재·순서·해시 동등성만 구조적으로 판독한다 —
# 의미 재판정을 하지 않는다(PO-INV 1). 어느 규칙에서도 **증명 불가는 stale(fail-closed)**로
# 귀결해 안전측(재검증 디스패치)으로 떨어진다.
# ==========================================================================
# 판정 사유 코드(구조화 근거·마커/진단에 실림).
CP2_EVIDENCE_VALID = "valid"                                   # 3규칙 전부 통과 → 재사용 적격
CP2_EVIDENCE_ABSENT = "absent"                                 # cp2-pass 부재 → 디스패치(재사용 불가)
CP2_EVIDENCE_STALE_REOPENED = "stale:reopened"                # rule (a) 재실행/retry
CP2_EVIDENCE_STALE_REVISION = "stale:revision"                # rule (b) 기지 revision 이 evidence 이후 대상
CP2_EVIDENCE_STALE_UNKNOWN_REVISION = "stale:unknown-revision"  # rule (b) 미지 kind — fail-closed
CP2_EVIDENCE_STALE_HASH = "stale:hash"                        # rule (c) 기록된 artifact 해시 확인 불가/불일치


@dataclass
class Cp2EvidenceFinding:
    """review_required 게이트의 cp2-pass evidence 재사용 판정 결과(구조화 근거).

    valid=True 이면 재검증 디스패치를 생략하고 basis 를 해소 마커에 실을 수 있다. valid=False
    이면 reason 이 부재(ABSENT) 또는 stale 종류를 가리키며, 소비 측은 기존 재검증 디스패치
    경로(fallback)로 간다. evidence 는 판정 대상 cp2-pass 이벤트(부재 시 None), basis 는 valid
    시 해소 마커 ref 에 실을 근거 참조(provenance 사슬)다.
    """

    valid: bool
    reason: str
    evidence: dict[str, Any] | None = None
    basis: dict[str, Any] | None = None


def _rev_field(rev: Any, name: str) -> Any:
    """RevisionEvent(dataclass) 또는 dict 형태의 revision 에서 필드를 꺼낸다(duck-typing)."""
    if isinstance(rev, dict):
        return rev.get(name)
    return getattr(rev, name, None)


def _latest_cp2_pass(events: list[dict[str, Any]], step_id: Any) -> dict[str, Any] | None:
    """step_id cycle 의 **최신**(at 최대) cp2-pass 이벤트. 없으면 None.

    derive_approval_state 의 cp2-pass 판독 조건(cycle_id·outcome pass·ref.kind==CP2_PASS_REF_KIND)
    과 동형이되, 최종 시도 판정을 쓰기 위해 존재 여부가 아니라 at 최대값을 고른다.
    """
    rows = [
        e for e in events
        if e.get("cycle_id") == step_id
        and e.get("outcome") == "pass"
        and isinstance(e.get("ref"), dict)
        and e["ref"].get("kind") == CP2_PASS_REF_KIND
    ]
    if not rows:
        return None
    return max(rows, key=lambda e: e.get("at", 0))


def _revision_touches(rev: Any, step_id: Any) -> bool | None:
    """이 revision 이 step_id task 를 대상으로 하는가(rule (b) 순서 판정 대상 판별).

    True  — 대상함. False — 무관. None — 미지/미지원 kind(무엇을 대상하는지 알 수 없음 →
    fail-closed 로 무조건 stale 처리). 기지 kind 3종:
      - task_added        : payload.id == step_id (같은 id 를 새로 낳는 경우만 대상).
      - dependency_added  : payload.id == step_id.
      - task_superseded   : supersedes == step_id (피대체) 또는 id == step_id (재발행 동일 id).
    """
    kind = _rev_field(rev, "kind")
    payload = _rev_field(rev, "payload") or {}
    if kind == KIND_TASK_ADDED:
        return payload.get("id") == step_id
    if kind == KIND_DEPENDENCY_ADDED:
        return payload.get("id") == step_id
    if kind == KIND_TASK_SUPERSEDED:
        return payload.get("supersedes") == step_id or payload.get("id") == step_id
    return None  # 미지 kind — fail-closed(닿는지 알 수 없으므로 닿는 것으로 간주).


def _revision_grounding_at(rev: Any, events: list[dict[str, Any]]) -> int | None:
    """이 revision 이 실재 가능해진 **하한 시점**(at) — 근거 게이트 통과 이벤트 중 가장 이른 at.

    revision 은 basis.gateEventRef 게이트 **통과** 이벤트가 append 된 뒤에만 존재할 수 있다
    (PO-INV 5). 따라서 그 gate_id 를 가진 outcome==pass 이벤트의 최소 at 이 revision 실재
    시점의 하한이다. gateEventRef 부재·미실재(통과 이벤트 0)면 None(순서 증명 불가 →
    소비 측이 fail-closed).
    """
    basis = _rev_field(rev, "basis") or {}
    gate_ref = basis.get("gateEventRef")
    if not gate_ref:
        return None
    ats = [
        e.get("at") for e in events
        if e.get("outcome") == "pass"
        and isinstance(e.get("ref"), dict)
        and e["ref"].get("gate_id") == gate_ref
        and e.get("at") is not None
    ]
    return min(ats) if ats else None


def _hash_mismatch(records: Iterable[Any], step_id: Any, hash_observer: Any) -> bool:
    """rule (c): step 산출 artifact 에 contentHash 가 **기록되어 있고** 문면 불변을 확인할 수
    없으면 True(stale). 기록이 없으면(현 baseline 전부 null) 공허 통과(False — 정본 문면
    '해시 기록 시 불일치' 그대로).

    기록된 해시가 있으면 hash_observer(location) 로 현재 해시를 관측해 비교한다. 관측 불일치는
    물론, 관측 자체가 불가(hash_observer 미제공·파일 부재·미가독)한 경우도 문면 불변을 확인할
    수 없으므로 fail-closed(True)로 처리한다(rule (c)의 fail-closed 지점).
    """
    for r in records:
        produced = getattr(r, "producedBy", None)
        if produced is None and isinstance(r, dict):
            produced = r.get("producedBy")
        produced = produced or {}
        if produced.get("stepId") != step_id:
            continue
        recorded = getattr(r, "contentHash", None)
        if recorded is None and isinstance(r, dict):
            recorded = r.get("contentHash")
        if not recorded:
            continue  # 해시 미기록 → 공허(이 규칙은 발동하지 않음).
        if hash_observer is None:
            return True  # 관측 수단 없음 → 확인 불가 → fail-closed.
        location = getattr(r, "location", None)
        if location is None and isinstance(r, dict):
            location = r.get("location")
        try:
            observed = hash_observer(location)
        except Exception:
            return True  # 관측 실패(파일 부재·미가독) → 확인 불가 → fail-closed.
        if observed != recorded:
            return True  # 불일치 관측 → stale.
    return False


def find_valid_cp2_evidence(
    events: Iterable[dict[str, Any]],
    step_id: Any,
    *,
    revisions: Iterable[Any] = (),
    artifact_records: Iterable[Any] = (),
    hash_observer: Any = None,
) -> Cp2EvidenceFinding:
    """review_required 게이트가 소비할 **유효 cp2-pass evidence** 를 찾는다(순수·fail-closed).

    step_id cycle 의 최신 cp2-pass 를 찾고, 다음 stale 3규칙을 **전부** 통과할 때만 valid=True:

      (a) 재실행/retry: cp2-pass 이후(at) 같은 cycle 에 후속 이벤트(재디스패치·rework·fail)가
          없어야 한다 — cp2-pass 가 최종 시도의 판정이어야 한다. 결정적 모델에서 Passed 는 종단
          이므로 최신 cp2-pass 이후 같은 cycle 이벤트는 재개(재실행) 흔적뿐이다.
      (b) supersede/revision 영향: 이 task 를 대상으로 하는 grounded revision 이 cp2-pass 검증
          시점(at) **이후**에 적용됐으면 stale. 순서는 revision 실재 하한(_revision_grounding_at)
          과 cp2-pass at 비교로 판정한다. 미지 revision kind 가 닿으면 무조건 stale(fail-closed).
          순서 증명 불가(grounding_at None)도 stale.
      (c) artifact 해시: 산출 artifact 에 contentHash 가 기록돼 있고 문면 불변을 확인 못 하면 stale.
          기록 없으면 공허 통과.

    판단 0(PO-INV 1): cp2-pass 실재는 host 가 기록한 Verifier Pass 이며 이 함수는 그 실재·순서·
    해시 동등성만 판독한다. 어떤 규칙도 의미 재판정을 하지 않으며, 불확실은 안전측(stale)으로
    떨어진다. 순수 함수 — 입력(events·revisions·records)과 hash_observer 관측만으로 결정된다.
    """
    events = list(events)
    pass_event = _latest_cp2_pass(events, step_id)
    if pass_event is None:
        return Cp2EvidenceFinding(valid=False, reason=CP2_EVIDENCE_ABSENT)

    p_at = pass_event.get("at", 0)

    # rule (a) — 최신 cp2-pass 이후 같은 cycle 후속 이벤트 = 재개(재실행/retry) 흔적.
    for e in events:
        if e.get("cycle_id") == step_id and e.get("at", 0) > p_at:
            return Cp2EvidenceFinding(
                valid=False, reason=CP2_EVIDENCE_STALE_REOPENED, evidence=pass_event
            )

    # rule (b) — supersede/revision 영향(순서 비교·fail-closed).
    for rev in revisions:
        touches = _revision_touches(rev, step_id)
        if touches is None:
            return Cp2EvidenceFinding(
                valid=False, reason=CP2_EVIDENCE_STALE_UNKNOWN_REVISION, evidence=pass_event
            )
        if not touches:
            continue
        g_at = _revision_grounding_at(rev, events)
        if g_at is None or g_at > p_at:
            # grounding_at None = 순서 증명 불가(fail-closed). g_at > p_at = revision 이
            # cp2-pass 이후 적용(하한이 이미 cp2-pass 를 넘음) → evidence 는 구내용 검증.
            return Cp2EvidenceFinding(
                valid=False, reason=CP2_EVIDENCE_STALE_REVISION, evidence=pass_event
            )
        # g_at <= p_at: revision 이 cp2-pass 를 선행 → 이 evidence 는 개정본을 검증(무관).

    # rule (c) — 기록된 artifact 해시 확인.
    if _hash_mismatch(artifact_records, step_id, hash_observer):
        return Cp2EvidenceFinding(
            valid=False, reason=CP2_EVIDENCE_STALE_HASH, evidence=pass_event
        )

    ref = pass_event.get("ref") or {}
    basis = {
        "kind": CP2_PASS_REF_KIND,
        "at": p_at,
        "seq": pass_event.get("seq"),
        "cycle_id": step_id,
        "verdict_ref": ref.get("verdict_ref"),
    }
    return Cp2EvidenceFinding(
        valid=True, reason=CP2_EVIDENCE_VALID, evidence=pass_event, basis=basis
    )


# ==========================================================================
# derive_registry — 파생 인덱스 (순수 함수·05 §3.6·PO-INV 2·7)
# ==========================================================================
def derive_registry(
    declarations: Iterable[dict[str, Any]],
    events: Iterable[dict[str, Any]],
    *,
    gate_id_for: Any = None,
    gate_policy: GatePolicy | None = None,
) -> dict[str, list[ArtifactRecord]]:
    """(선언 원장, 이벤트 로그) → {artifactId: [ArtifactRecord]} 파생 인덱스.

    - **순수 함수**: 입력만으로 출력 결정(I/O·상태 없음 — PO-INV 3 동형). 같은 두 원장 →
      같은 레지스트리.
    - **계보 append-only 보존**(PO-INV 7): 모든 버전 레코드를 보존하고 version 오름차순
      정렬한다. 같은 (artifactId, version) 이 복수 선언되면 마지막 선언을 채택한다
      (append-only latest — 재시도 재선언 등에 안정). supersedes 계보는 그대로 둔다.
    - **approvalState 파생 뷰**: 각 레코드의 approvalState 를 산출 step 의 검증/게이트
      이벤트에서 파생한다(derive_approval_state). 선언은 approvalState 를 담지 않는다.
    - **제2 진리원천 아님**: 레지스트리는 저장되지 않고 매 호출 새로 파생된다(mutable 저장 0).
    """
    events = list(events)
    # (artifactId -> version -> 선언) — 같은 버전 재선언은 마지막이 이긴다(append-only latest).
    grouped: dict[str, dict[int, dict[str, Any]]] = {}
    for decl in declarations:
        aid = decl.get("artifactId")
        if not aid:
            continue
        version = int(decl.get("version", 1))
        grouped.setdefault(aid, {})[version] = decl

    registry: dict[str, list[ArtifactRecord]] = {}
    for aid in sorted(grouped.keys(), key=str):
        records: list[ArtifactRecord] = []
        for version in sorted(grouped[aid].keys()):
            decl = grouped[aid][version]
            producedBy = dict(decl.get("producedBy") or {})
            step_id = producedBy.get("stepId")
            state = derive_approval_state(
                events, step_id, gate_id_for=gate_id_for, gate_policy=gate_policy
            )
            records.append(
                ArtifactRecord(
                    artifactId=str(aid),
                    version=version,
                    supersedes=decl.get("supersedes"),
                    derivedFrom=list(decl.get("derivedFrom") or []),
                    producedBy=producedBy,
                    approvalState=state,
                    location=decl.get("location"),
                    contentHash=decl.get("contentHash"),
                )
            )
        registry[str(aid)] = records
    return registry


# ==========================================================================
# resolve_references — 번들 확정 참조 해석 (05 §3.6·07 R2)
# ==========================================================================
def resolve_references(
    registry: dict[str, list[ArtifactRecord]],
    required_grade: str,
) -> list[ArtifactRecord]:
    """번들 조립용 확정 참조 — 요구 등급 이상 approvalState 의 **최신 버전만** 해석한다.

    각 artifactId 에 대해 approvalState 등급이 required_grade 이상인 레코드 중 **최고
    version** 하나를 고른다. 요구 등급을 충족하는 버전이 없으면 그 artifactId 는 해석되지
    않는다(미완성·미승인 산출물은 추측·인용 0 — 05 §3.6·07 R2). 결과는 artifactId 사전순
    안정 정렬(결정적).

    계보는 배제하지 않는다 — 등급 미달·구버전 레코드는 레지스트리에 그대로 남고(계보
    append-only·문면 불변) resolve 만 확정 참조에서 제외한다.
    """
    threshold = approval_grade(required_grade)
    resolved: list[ArtifactRecord] = []
    for aid in sorted(registry.keys(), key=str):
        qualifying = [
            r for r in registry[aid]
            if approval_grade(r.approvalState) >= threshold
        ]
        if not qualifying:
            continue
        # 요구 등급 이상 중 최신(최고 version) 하나만 확정 참조로 해석한다.
        best = max(qualifying, key=lambda r: r.version)
        resolved.append(best)
    return resolved
