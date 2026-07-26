"""경량(lightweight) 레인 원장 표본 물리화 + 결정적 자체 점검 (setup_m.py 동형·비프로덕션).

사용법:  python setup_lite.py            (표본 물리화 + 점검 5축 실행)
         python setup_lite.py --check-only  (물리화 생략·기존 표본만 점검)

재생성 순서(물리화는 run 디렉터리를 fresh 초기화하므로 `logs/*.log` 가 지워진다):
  1) python setup_lite.py                       > <run-dir>/logs/lite-check.log   (건너뛰고 재실행 시 2·3만)
  2) python verify_run.py <run-dir>             > <run-dir>/logs/verify-run.log
  3) python setup_lite.py --check-only          > <run-dir>/logs/lite-check.log
`*.log` 는 빌더 산출이 아니므로 결정성 대조(축 4)에서 제외한다.

무엇을 하는가:
  절차 비례화 트랙 경량 레인(엔진을 돌리지 않고 Advisor 직접 위임으로 조율하는 레인)의
  **구현 층 원장 표본**을 `orchestration-data/runs/<run-id>-lite/` 에 물리화하고, 그 표본이
  기존 닫힌 스키마·기존 결정적 러너로 검증 가능함을 결정적으로 점검한다. 새 레코드 종류·새
  필드·새 원장 루트·새 검증기를 만들지 않는다 — 규약 정본 = `orchestration/adapters/claude/
  project-orchestration-binding.md` §5.9.

점검 5축(전부 결정적·LLM 0·네트워크 0):
  (1) 스키마 — revisions.jsonl 전행을 `revision_schema.json` 으로, 파생 ArtifactRecord 전건을
      `artifact_record_schema.json` 으로 검증(둘 다 스키마 파일 무수정 판독). artifacts.jsonl 은
      **선언** 원장이므로 approvalState 를 담지 않고(파생 뷰·05 §3.6) 스키마 property 부분집합
      규율만 받는다. 검증기는 이 파일 안의 stdlib 최소 검증기이며, `jsonschema` 가 import 되면
      draft-07 정식 검증도 추가로 돌린다(fail-soft·부재 시 그 사실을 출력에 명시).
  (2) basis 왕복 — `basis.proposingStepRef`·`basis.gateEventRef` 두 참조를 `<경로>#<프래그먼트>`
      로 해석해 (a) 경로 실재 (b) 프래그먼트 실재 (c) gateEventRef 프래그먼트 == events.jsonl
      게이트 이벤트 `ref.gate_id` 문자 동일을 확인한다.
  (3) approvalState 파생 — 중립 `artifacts.derive_registry` 를 게이트 id 규약과 함께 호출해
      verified·approved·user_approved 3전이가 **게이트/검증 이벤트에서 파생**됨을 보인다
      (직접 기입 0·PO-INV 7). 선언 원장에 approvalState 키가 0건임을 함께 확인한다.
  (4) 결정성 — 같은 빌더를 임시 디렉터리에 재실행해 전 파일 byte 동일을 확인한다.
  (5) 음성 대조 — 게이트 순서(required→provenance→resolved)를 의도적으로 어긴 임시 표본에
      `verify_run.py` 를 실행해 findings 가 비공집합·exit 1 임을 확인한다(검증기가 실제로 거부를
      낼 수 있음을 증명).

경계(불가침):
  - 스키마 파일(`revision_schema.json`·`artifact_record_schema.json`)·중립 코드
    (`orchestration/framework/**`)·`verify_run.py` 를 **읽기만** 한다(수정 0).
  - 쓰기 대상은 `RUNS_DIR/<run-id>-lite/` 와 임시 디렉터리뿐이다. 삭제는 이름이 `-lite` 로
    끝나는 RUNS_DIR 직속 디렉터리에만 허용한다(오삭제 가드 — setup_m.py 가드 동형).
  - stdlib only(선택적 `jsonschema` 는 있으면 추가 검증·없으면 건너뜀).

표본의 정직 라벨(L-07): 이 표본의 cp2-pass·게이트 해소·CP3 승인 마커는 **형태 표본(fixture)**
이며 실 판정 발화가 아니다. 그 사실은 `events.jsonl` 첫 이벤트(`ref.kind=simulation-annotation`
·`simulated=true`)와 `logs/gate-resolution-record.json`(`simulated=true`)에 기계 판독 가능하게
남는다. 표본 등급 = ephemeral(재실행으로 재생성 — `docs/artifact-lifecycle-policy.md` §2).
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _orch_common import RUNS_DIR

HERE = Path(__file__).resolve().parent                     # .../orchestration-data/e2e
CLAUDE_DIR = HERE.parents[1]                               # .../framework/adapters/claude
REPO_ROOT = CLAUDE_DIR.parents[3]                          # 리포 루트
ORCH_DIR = REPO_ROOT / "orchestration" / "framework" / "orchestrator"
for _p in (str(ORCH_DIR), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from artifacts import derive_registry  # noqa: E402  (중립·순수)
from gates import GatePolicy  # noqa: E402  (중립·순수)
from revision import RevisionEvent, fold, validate_revision  # noqa: E402  (중립·순수)

# ==========================================================================
# 표본 좌표 — run-id 는 `-lite` 접미를 포함하며 디렉터리명과 동일하다(§5.9).
# ==========================================================================
RUN_ID = "lw-w2b-sample-lite"

S1 = "lw-w2b-plan"                 # proposal  — 분해 초안(Planner)
S2 = "lw-w2b-ledger-section"       # implementation — 원장 규약 절 신설(Worker)
S3 = "lw-w2b-verify-milestone"     # milestone — 검증 왕복(Worker)

G1 = "gate-unit-" + S1             # user_decision_required
G2 = "gate-unit-" + S2             # review_required
G3 = "gate-unit-" + S3             # approval_required

# lane 어휘(정본 = W2-a `lane_resolve` 방출 어휘 — 본 파일은 원장 문면 소비 측이다).
LANE_LIGHTWEIGHT = "lightweight"
LANE_STANDARD = "standard"         # 참조용(표본은 lightweight 만 싣는다)

BRIEF_REF = "docs/proportionality-track-ledger.md#W2-b"
GATE_RECORD_REL = "logs/gate-resolution-record.json"
GATE_EVENT_REF = GATE_RECORD_REL + "#" + G1

SENTINEL_TASK = "위 task 필드와 동일"
SENTINEL_DONE = "위 done 필드와 동일"

FIXTURE_NOTE = (
    "경량 레인 원장 **형태 표본**(fixture) — 이 run 의 cp2-pass·게이트 해소·CP3 승인 마커는 "
    "형태 예시이며 실 판정 발화가 아니다(L-07 정직 구분). 표본의 목적은 경량 레인 원장이 "
    "기존 닫힌 스키마(revision_schema·artifact_record_schema)와 기존 결정적 러너(verify_run.py)로 "
    "검증 가능함을 실증하는 것이다. 등급 = ephemeral(setup_lite.py 재실행으로 재생성)."
)


def _lane_line(lane: str, override_reason=None) -> str:
    """원장 payload 문면의 lane 표기 1행(신규 필드 0 — 기존 delegation.context 항목이다)."""
    return "lane=%s · laneOverrideReason=%s" % (
        lane, "null" if override_reason is None else json.dumps(override_reason, ensure_ascii=False)
    )


# ==========================================================================
# 표본 데이터 — 결정적(시각·난수·환경 의존 0)
# ==========================================================================
def config() -> dict:
    return {
        # 키 집합은 기존 표준 run config 의 부분집합이다(신규 키 0). lane 표기는 config 가 아니라
        # graph.goal · revision payload delegation.context · 게이트 기록 3지점에 싣는다(§5.9 (e)).
        "allowed_tools": ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python:*)"],
        "output_format": "json",
        "policy": "auto_approve",
        "retry_limit": 2,
        "run_id": RUN_ID,
        "timeout": 900,
    }


def gate_policy() -> dict:
    """표준 레인 컴파일러(`contract_to_graph`)가 내는 3엔트리와 동일 문면(신설 0)."""
    return {
        "entries": [
            {"gate": "user_decision_required", "target": {"unitType": "proposal"}},
            {"gate": "review_required", "target": {"unitType": "implementation"}},
            {"gate": "approval_required", "target": {"unitType": "milestone"}},
        ],
        "escalationResolvers": ["Advisor", "human"],
        "gateRaiser": "Advisor",
        "userActorClass": "human",
    }


def _task_s1() -> dict:
    task = (
        "절차 비례화 트랙 Wave 2 분해 초안 산출 — 경량 레인 판별·경량 원장 물리 형태 제안을 "
        "포함한 Wave 브리프 초안(채택·확정 권위는 Advisor·사용자)"
    )
    done = [
        "초안에 경량 원장의 물리 형태 제안이 존재한다(기존 스키마 재사용·신규 포맷 0)",
        "각 Wave 브리프에 done·constraints·동료 계약 블록이 존재한다",
    ]
    return {
        "capability": "cap-lw-decompose",
        "delegation": {
            "constraints": "정본 수정 0(제안까지만). 계획 자기 채택 금지 — 채택은 Advisor 소관.",
            "context": [
                "절차 비례화 트랙 — Planner 분해 초안 단위(경량 레인·엔진 디스패치 0)",
                _lane_line(LANE_LIGHTWEIGHT),
                "브리프 정본 = docs/proportionality-track-ledger.md §4",
            ],
            "done": SENTINEL_DONE,
            "from": "Advisor",
            "input": ".claude/CLAUDE.md · .claude/AGENT.md · docs/delegation-protocol.md §2",
            "output": "docs/proportionality-track-ledger.md",
            "task": SENTINEL_TASK,
            "to": "Planner",
        },
        "done": done,
        "dependsOn": [],
        "id": S1,
        "interfaceContract": {
            "consumes": [".claude/CLAUDE.md", "docs/delegation-protocol.md"],
            "produces": ["docs/proportionality-track-ledger.md"],
        },
        "model": "opus",
        "ownedBoundary": ["docs/proportionality-track-ledger.md"],
        "role": "Planner",
        "task": task,
        "unitType": "proposal",
    }


def _task_s2() -> dict:
    task = (
        "경량 레인 구현 원장을 기존 닫힌 스키마 재사용으로 확정하고 바인딩 문서에 규약 절을 "
        "신설한다(새 포맷·새 루트 0)"
    )
    done = [
        "project-orchestration-binding.md 에 경량 레인 원장 규약 절이 존재한다(기존 절 번호 보존)",
        "규약이 최소 필드·배치 경로·form-A 수기 append 절차를 명시한다",
    ]
    return {
        "capability": "cap-lw-ledger-contract",
        "delegation": {
            "constraints": (
                "스키마 파일 수정 0 · 중립 코드(orchestration/framework/**) 수정 0 · "
                "verify_run.py 수정 0 · 새 원장 포맷·새 루트 신설 0"
            ),
            "context": [
                "절차 비례화 트랙 Wave 2 W2-b — 경량 원장 물리 형태(경량 레인·엔진 디스패치 0)",
                _lane_line(LANE_LIGHTWEIGHT),
                "동료 Task = W2-a(레인 판별 로더) — lane 어휘·laneOverrideReason 필드명 공유·파일 무교차",
                "브리프 정본 = docs/proportionality-track-ledger.md §3·§4 W2-b",
            ],
            "done": SENTINEL_DONE,
            "from": "Advisor",
            "input": (
                "orchestration/specs/05-project-orchestration.md §3.2·§3.6 · "
                "orchestration/framework/orchestrator/{revision_schema.json,artifact_record_schema.json}"
            ),
            "output": "orchestration/adapters/claude/project-orchestration-binding.md",
            "task": SENTINEL_TASK,
            "to": "Worker",
        },
        "done": done,
        "dependsOn": [S1],
        "id": S2,
        "interfaceContract": {
            "consumes": [
                "docs/proportionality-track-ledger.md",
                "orchestration/framework/orchestrator/revision_schema.json",
                "orchestration/framework/orchestrator/artifact_record_schema.json",
            ],
            "produces": ["orchestration/adapters/claude/project-orchestration-binding.md"],
        },
        "model": "opus",
        "ownedBoundary": [
            "orchestration/adapters/claude/project-orchestration-binding.md",
            "uahf/framework/adapters/claude/orchestration-data/e2e/setup_lite.py",
        ],
        "role": "Worker",
        "task": task,
        "unitType": "implementation",
    }


def _task_s3() -> dict:
    task = (
        "경량 원장 표본을 기존 결정적 러너로 검증하고 음성 대조까지 남긴다(단위 간 계약 정합 "
        "검사 — 규약 문면 ↔ 표본 실물 ↔ 러너 판정 3면 대조)"
    )
    done = [
        "verify_run.py 를 표본 run 디렉터리에 실행해 findings 0·exit 0 이다(로그 보존)",
        "게이트 순서 위반 표본에 같은 러너를 실행하면 findings 가 비공집합이다(음성 대조)",
        "규약 절이 명시한 최소 필드 집합과 표본 실물의 키 집합이 일치한다(문면↔실물 대조)",
    ]
    return {
        "capability": "cap-lw-ledger-verify",
        "delegation": {
            "constraints": "verify_run.py 수정 0 — 기존 러너를 그대로 재사용한다(새 검증기 신설 0).",
            "context": [
                "절차 비례화 트랙 Wave 2 W2-b — 검증 왕복 밀스톤(경량 레인·엔진 디스패치 0)",
                _lane_line(LANE_LIGHTWEIGHT),
                "러너 = uahf/framework/adapters/claude/orchestration-data/e2e/verify_run.py 축 (a)·(b)·(e)",
            ],
            "done": SENTINEL_DONE,
            "from": "Advisor",
            "input": "표본 run 디렉터리 원장 3종 + graph.json + gate_policy.json",
            "output": "logs/verify-run.log · logs/negative-gate-order.log",
            "task": SENTINEL_TASK,
            "to": "Worker",
        },
        "done": done,
        "dependsOn": [S2],
        "id": S3,
        "interfaceContract": {
            "consumes": [
                "orchestration/adapters/claude/project-orchestration-binding.md",
                "uahf/framework/adapters/claude/orchestration-data/e2e/verify_run.py",
            ],
            "produces": [
                "uahf/framework/adapters/claude/orchestration-data/runs/%s/logs/verify-run.log" % RUN_ID,
            ],
        },
        "model": "opus",
        "ownedBoundary": [
            "uahf/framework/adapters/claude/orchestration-data/runs/%s/logs/" % RUN_ID,
        ],
        "role": "Worker",
        "task": task,
        "unitType": "milestone",
    }


def initial_graph() -> dict:
    """초기 그래프 = proposal 단위 1개(표준 레인 seed 관례 동형). 구현·밀스톤 단위는 revision 승격."""
    return {
        "completion": "all-passed",
        "dependencies": [],
        "goal": (
            "절차 비례화 트랙 Wave 2 W2-b — 경량 레인(lane=%s) 구현 원장의 물리 형태를 기존 "
            "닫힌 스키마 재사용으로 확정하고 기존 결정적 러너로 검증 가능함을 실증한다. 조율 주체 = "
            "Advisor 직접 위임(엔진 디스패치 0)이며 원장 0건 금지는 표준 레인과 동일하게 적용된다."
        ) % LANE_LIGHTWEIGHT,
        "tasks": [_task_s1()],
    }


def revisions() -> list:
    """task_added 2건 — 사용자 게이트(G1) 해소를 근거로 구현·밀스톤 단위를 승격(kind 신설 0)."""
    basis = {"gateEventRef": GATE_EVENT_REF, "proposingStepRef": BRIEF_REF}
    return [
        {"basis": dict(basis), "kind": "task_added", "payload": _task_s2(), "revisionSeq": 1},
        {"basis": dict(basis), "kind": "task_added", "payload": _task_s3(), "revisionSeq": 2},
    ]


def _ev(at, cycle_id, seq, *, actor, outcome, ref, from_stage=None, to_stage, trigger):
    """03 §3.2-A 10필드 이벤트(필드 신설 0)."""
    return {
        "actor": actor,
        "at": at,
        "cycle_id": cycle_id,
        "from_stage": from_stage,
        "outcome": outcome,
        "ref": ref,
        "retry_count": 0,
        "seq": seq,
        "to_stage": to_stage,
        "trigger": trigger,
    }


def events() -> list:
    return [
        _ev(1, "annotation::sim", 1, actor="Advisor", outcome="pass", to_stage="note",
            trigger="표본 라벨",
            ref={"kind": "simulation-annotation", "simulated": True, "note": FIXTURE_NOTE}),
        _ev(2, S1, 1, actor="Worker", outcome="pass", to_stage="Execute",
            trigger="완료 조건 충족", ref={"kind": "dispatch"}),
        _ev(3, S1, 2, actor="Verifier", outcome="pass", from_stage="Verify", to_stage="Complete",
            trigger="완료 조건 충족", ref={"kind": "cp2-pass", "verdict_ref": "verdict"}),
        _ev(4, "gate::" + G1, 1, actor="Advisor", outcome="escalated", to_stage="Consult",
            trigger="에스컬레이션",
            ref={"kind": "gate-required", "gate_id": G1, "gateKind": "user_decision_required",
                 "target": {"unitType": "proposal"},
                 "scoped_question": "Wave 2 분해 초안(경량 레인 원장 물리 형태 제안)을 채택하는가"}),
        _ev(5, "annotation::provenance-" + G1, 1, actor="human", outcome="pass", to_stage="note",
            trigger="게이트 해소 provenance",
            ref={"actor": "human", "gateKind": "user_decision_required", "gate_id": G1,
                 "kind": "user-resolution-provenance",
                 "note": "경량 레인 게이트 해소 provenance 기록(form-A 수기 append). 자격 판정은 "
                         "gates.py(is_eligible_resolver/is_resolved)가 코드로 소유하며 이 원장은 "
                         "우회하지 않는다. 표본 라벨 = at=1 simulation-annotation.",
                 "record": GATE_RECORD_REL,
                 "response": "채택 — Wave 2 병렬(W2-a ∥ W2-b) 착수, lane 어휘 standard|lightweight 고정"}),
        _ev(6, "gate::" + G1, 2, actor="human", outcome="pass", from_stage="Consult",
            to_stage="Complete", trigger="완료 조건 충족",
            ref={"kind": "gate-resolved", "gate_id": G1, "gateKind": "user_decision_required"}),
        _ev(7, S2, 1, actor="Worker", outcome="pass", to_stage="Execute",
            trigger="완료 조건 충족", ref={"kind": "dispatch"}),
        _ev(8, S2, 2, actor="Verifier", outcome="pass", from_stage="Verify", to_stage="Complete",
            trigger="완료 조건 충족", ref={"kind": "cp2-pass", "verdict_ref": "verdict"}),
        _ev(9, "gate::" + G2, 1, actor="Verifier", outcome="pass", from_stage="Verify",
            to_stage="Complete", trigger="완료 조건 충족",
            ref={"kind": "gate-review", "gate_id": G2, "gateKind": "review_required",
                 "mode": "evidence-reuse",
                 "basis": {"at": 8, "cycle_id": S2, "kind": "cp2-pass", "seq": 2,
                           "verdict_ref": "verdict"},
                 "verdict": {"ref": "verdict", "verdict": "Pass"}}),
        _ev(10, S3, 1, actor="Worker", outcome="pass", to_stage="Execute",
            trigger="완료 조건 충족", ref={"kind": "dispatch"}),
        _ev(11, S3, 2, actor="Verifier", outcome="pass", from_stage="Verify", to_stage="Complete",
            trigger="완료 조건 충족", ref={"kind": "cp2-pass", "verdict_ref": "verdict"}),
        _ev(12, "gate::" + G3, 1, actor="Advisor", outcome="pass", from_stage="Verify",
            to_stage="Complete", trigger="완료 조건 충족",
            ref={"kind": "gate-approval", "gate_id": G3, "gateKind": "approval_required",
                 "verdict": {"ref": "verdict", "verdict": "Pass"}}),
    ]


def declarations() -> list:
    """artifact **선언** 원장(7필드·approvalState 부재 — 파생 뷰다·05 §3.6)."""
    def decl(aid, step, capability, role, derived):
        return {
            "artifactId": aid,
            "contentHash": None,
            "derivedFrom": derived,
            "location": aid,
            "producedBy": {"attempt": None, "capability": capability, "model": "opus",
                           "role": role, "runId": RUN_ID, "stepId": step},
            "supersedes": None,
            "version": 1,
        }
    return [
        decl("docs/proportionality-track-ledger.md", S1, "cap-lw-decompose", "Planner",
             [".claude/CLAUDE.md", "docs/delegation-protocol.md"]),
        decl("orchestration/adapters/claude/project-orchestration-binding.md", S2,
             "cap-lw-ledger-contract", "Worker",
             ["docs/proportionality-track-ledger.md",
              "orchestration/framework/orchestrator/revision_schema.json",
              "orchestration/framework/orchestrator/artifact_record_schema.json"]),
        decl("uahf/framework/adapters/claude/orchestration-data/runs/%s/logs/verify-run.log" % RUN_ID,
             S3, "cap-lw-ledger-verify", "Worker",
             ["orchestration/adapters/claude/project-orchestration-binding.md",
              "uahf/framework/adapters/claude/orchestration-data/e2e/verify_run.py"]),
    ]


def gate_record() -> dict:
    """게이트 기록(form-A) — basis.gateEventRef 가 가리키는 실파일. 필드 = §5.9 표."""
    return {
        "gateKind": "user_decision_required",
        "gate_id": G1,
        "lane": LANE_LIGHTWEIGHT,
        "laneOverrideReason": None,
        "note": FIXTURE_NOTE,
        "presentedBy": "Advisor",
        "resolutionEventAt": 6,
        "resolvedByActor": "human",
        "response": "채택 — Wave 2 병렬(W2-a ∥ W2-b) 착수, lane 어휘 standard|lightweight 고정",
        "runId": RUN_ID,
        "scopedQuestion": "Wave 2 분해 초안(경량 레인 원장 물리 형태 제안)을 채택하는가",
        "simulated": True,
    }


# ==========================================================================
# 물리화
# ==========================================================================
def _write_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def _write_jsonl(path: Path, rows) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _guarded_rmtree(run_dir: Path) -> None:
    """오삭제 가드 — RUNS_DIR 직속이고 이름이 `-lite` 로 끝나는 디렉터리만 삭제한다."""
    run_dir = run_dir.resolve()
    if not run_dir.exists():
        return
    if run_dir.parent != Path(RUNS_DIR).resolve() or not run_dir.name.endswith("-lite"):
        raise RuntimeError("삭제 가드: RUNS_DIR 직속 `-lite` 디렉터리만 재초기화한다: %s" % run_dir)
    shutil.rmtree(run_dir)


def build_into(run_dir: Path, *, guard: bool = True) -> Path:
    """표본 run 디렉터리를 결정적으로 물리화한다(같은 입력 → byte 동일 산출)."""
    if guard:
        _guarded_rmtree(run_dir)
    elif run_dir.exists():
        shutil.rmtree(run_dir)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    _write_json(run_dir / "config.json", config())
    _write_json(run_dir / "graph.json", initial_graph())
    _write_json(run_dir / "gate_policy.json", gate_policy())
    _write_jsonl(run_dir / "events.jsonl", events())
    _write_jsonl(run_dir / "revisions.jsonl", revisions())
    _write_jsonl(run_dir / "artifacts.jsonl", declarations())
    _write_json(run_dir / GATE_RECORD_REL, gate_record())
    return run_dir


# ==========================================================================
# (1) 스키마 — stdlib 최소 검증기 + (있으면) jsonschema draft-07
# ==========================================================================
_SUPPORTED_KEYWORDS = {
    "$schema", "$id", "title", "description", "type", "required", "properties",
    "additionalProperties", "enum", "minimum", "items",
}
_TYPE_MAP = {
    "object": dict, "array": list, "string": str, "integer": int,
    "number": (int, float), "boolean": bool, "null": type(None),
}


def _check_type(value, spec) -> bool:
    names = spec if isinstance(spec, list) else [spec]
    for name in names:
        py = _TYPE_MAP.get(name)
        if py is None:
            return True  # 미지원 type 이름은 판정하지 않는다(범위 정직).
        if name == "integer" and isinstance(value, bool):
            continue
        if name in ("number",) and isinstance(value, bool):
            continue
        if isinstance(value, py):
            return True
    return False


def minimal_validate(instance, schema, where="$", unsupported=None) -> list:
    """draft-07 부분집합 검증(지원 키워드 = _SUPPORTED_KEYWORDS). 미지원 키워드는 수집·미판정."""
    errors: list = []
    if unsupported is not None:
        for key in schema:
            if key not in _SUPPORTED_KEYWORDS:
                unsupported.add(key)
    if "type" in schema and not _check_type(instance, schema["type"]):
        errors.append("%s type 위반: 기대 %r, 실제 %s" % (where, schema["type"], type(instance).__name__))
        return errors
    if "enum" in schema and instance not in schema["enum"]:
        errors.append("%s enum 위반: %r not in %r" % (where, instance, schema["enum"]))
    if "minimum" in schema and isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if instance < schema["minimum"]:
            errors.append("%s minimum 위반: %r < %r" % (where, instance, schema["minimum"]))
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append("%s required 키 부재: %r" % (where, key))
        props = schema.get("properties") or {}
        addl = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in props:
                errors.extend(minimal_validate(value, props[key], "%s.%s" % (where, key), unsupported))
            elif addl is False:
                errors.append("%s additionalProperties=false 위반: 미허용 키 %r" % (where, key))
            elif isinstance(addl, dict):
                errors.extend(minimal_validate(value, addl, "%s.%s" % (where, key), unsupported))
    if isinstance(instance, list) and isinstance(schema.get("items"), dict):
        for i, item in enumerate(instance):
            errors.extend(minimal_validate(item, schema["items"], "%s[%d]" % (where, i), unsupported))
    return errors


def _load(path: Path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_jsonl(path: Path) -> list:
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if raw:
                rows.append(json.loads(raw))
    return rows


def check_schema(run_dir: Path, out) -> list:
    rev_schema = _load(ORCH_DIR / "revision_schema.json")
    art_schema = _load(ORCH_DIR / "artifact_record_schema.json")
    findings: list = []
    unsupported: set = set()

    rev_rows = _load_jsonl(run_dir / "revisions.jsonl")
    for i, row in enumerate(rev_rows):
        findings.extend(minimal_validate(row, rev_schema, "revisions[%d]" % i, unsupported))

    # 선언 원장 — approvalState 는 파생 뷰이므로 선언에 없어야 한다(05 §3.6).
    decls = _load_jsonl(run_dir / "artifacts.jsonl")
    allowed = set(art_schema["properties"])
    for i, d in enumerate(decls):
        extra = set(d) - allowed
        if extra:
            findings.append("artifacts[%d] 스키마 밖 키: %r" % (i, sorted(extra)))
        if "approvalState" in d:
            findings.append("artifacts[%d] 선언에 approvalState 기입(파생 뷰 위반·PO-INV 7)" % i)

    # 파생 ArtifactRecord — 스키마 전 필드 검증 대상.
    registry = derive_registry(decls, _load_jsonl(run_dir / "events.jsonl"),
                              gate_id_for=lambda sid: "gate-unit-%s" % sid,
                              gate_policy=GatePolicy.from_dict(_load(run_dir / "gate_policy.json")))
    records = [r.to_dict() for recs in registry.values() for r in recs]
    for i, rec in enumerate(records):
        findings.extend(minimal_validate(rec, art_schema, "records[%d]" % i, unsupported))

    out.append("  revisions.jsonl %d행 · artifacts.jsonl 선언 %d행 · 파생 ArtifactRecord %d건"
               % (len(rev_rows), len(decls), len(records)))
    out.append("  stdlib 최소 검증기 지원 키워드 = %s" % sorted(_SUPPORTED_KEYWORDS))
    out.append("  두 스키마에서 만난 미지원 키워드(미판정) = %s" % (sorted(unsupported) or "없음"))

    try:
        import jsonschema  # noqa: PLC0415  (선택 의존·fail-soft)
    except ImportError:
        out.append("  jsonschema 미설치 — draft-07 정식 검증 생략(stdlib 검증만·범위 정직)")
    else:
        for i, row in enumerate(rev_rows):
            for e in jsonschema.Draft7Validator(rev_schema).iter_errors(row):
                findings.append("[jsonschema] revisions[%d] %s: %s" % (i, list(e.path), e.message))
        for i, rec in enumerate(records):
            for e in jsonschema.Draft7Validator(art_schema).iter_errors(rec):
                findings.append("[jsonschema] records[%d] %s: %s" % (i, list(e.path), e.message))
        from importlib.metadata import version as _pkg_version  # noqa: PLC0415
        out.append("  jsonschema %s draft-07 정식 검증 동반 실행" % _pkg_version("jsonschema"))

    # 중립 구조 검증기(순수)도 함께 통과해야 한다.
    graph = _load(run_dir / "graph.json")
    revs = [RevisionEvent.from_dict(r) for r in rev_rows]
    for i, rev in enumerate(revs):
        reason = validate_revision(rev, fold(revs[:i], graph))
        if reason is not None:
            findings.append("validate_revision seq=%s 실패: %s" % (rev.revisionSeq, reason))
    out.append("  중립 validate_revision progressive 검증 %d건" % len(revs))
    return findings


# ==========================================================================
# (2) basis 왕복
# ==========================================================================
def check_basis(run_dir: Path, out) -> list:
    findings: list = []
    events_rows = _load_jsonl(run_dir / "events.jsonl")
    gate_ids = {(e.get("ref") or {}).get("gate_id") for e in events_rows
                if isinstance(e.get("ref"), dict)}
    for row in _load_jsonl(run_dir / "revisions.jsonl"):
        basis = row["basis"]
        seq = row["revisionSeq"]
        for field, base, base_label in (("proposingStepRef", REPO_ROOT, "리포 루트"),
                                        ("gateEventRef", run_dir, "run 디렉터리")):
            ref = basis[field]
            if "#" not in ref:
                findings.append("seq=%s %s 에 `#<프래그먼트>` 부재: %r" % (seq, field, ref))
                continue
            rel, frag = ref.rsplit("#", 1)
            target = (base / rel)
            if not target.exists():
                findings.append("seq=%s %s 경로 미실재(%s 기준): %s" % (seq, field, base_label, rel))
                continue
            text = target.read_text(encoding="utf-8", errors="replace")
            if frag not in text:
                findings.append("seq=%s %s 프래그먼트 미실재: %r in %s" % (seq, field, frag, rel))
                continue
            out.append("  seq=%s %s -> %s (%s 기준) · 프래그먼트 %r 실재"
                       % (seq, field, rel, base_label, frag))
            if field == "gateEventRef" and frag not in gate_ids:
                findings.append("seq=%s gateEventRef 프래그먼트가 events.jsonl ref.gate_id 에 부재: %r"
                                % (seq, frag))
            elif field == "gateEventRef":
                out.append("    프래그먼트 == events.jsonl ref.gate_id 문자 동일 (게이트 좌표 복원 가능)")
    return findings


# ==========================================================================
# (3) approvalState 파생
# ==========================================================================
EXPECTED_STATES = {S1: "user_approved", S2: "verified", S3: "approved"}


def check_approval(run_dir: Path, out) -> list:
    findings: list = []
    decls = _load_jsonl(run_dir / "artifacts.jsonl")
    events_rows = _load_jsonl(run_dir / "events.jsonl")
    policy = GatePolicy.from_dict(_load(run_dir / "gate_policy.json"))
    registry = derive_registry(decls, events_rows,
                              gate_id_for=lambda sid: "gate-unit-%s" % sid, gate_policy=policy)
    seen: dict = {}
    for aid in sorted(registry):
        for rec in registry[aid]:
            step = (rec.producedBy or {}).get("stepId")
            seen[step] = rec.approvalState
            out.append("  %-24s v%d %-14s <- stepId=%s" % (aid.split("/")[-1], rec.version,
                                                           rec.approvalState, step))
    for step, expected in EXPECTED_STATES.items():
        got = seen.get(step)
        if got != expected:
            findings.append("stepId=%s approvalState 기대 %r, 파생 %r" % (step, expected, got))
    ladder = [seen.get(S2), seen.get(S3), seen.get(S1)]
    out.append("  3전이 파생 = %s (게이트/검증 이벤트 파생 뷰 — 직접 기입 0)" % " -> ".join(map(str, ladder)))
    # 음성 대조: 게이트 좌표를 주지 않으면 게이트 축(approved/user_approved)은 파생되지 않는다.
    bare = derive_registry(decls, events_rows)
    bare_states = sorted({r.approvalState for recs in bare.values() for r in recs})
    out.append("  gate_id_for 미지정 시 파생 등급 = %s (게이트 축 미파생 — 파생 의존 증명)" % bare_states)
    if bare_states != ["verified"]:
        findings.append("gate_id_for 미지정 파생이 기대(verified 만)와 다르다: %r" % bare_states)
    return findings


# ==========================================================================
# (4)(5) 결정성 · 음성 대조
# ==========================================================================
def _run_verify(run_dir: Path, outdir: Path):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, str(HERE / "verify_run.py"), str(run_dir), "-o", str(outdir)],
        capture_output=True, text=True, cwd=str(HERE), env=env, encoding="utf-8",
    )
    return proc


def _cmp_tree(a: Path, b: Path) -> list:
    """빌더 소유 파일만 대조한다 — `*.log`(러너 실행 출력)는 빌더 산출이 아니라 제외."""
    diff: list = []
    def names(root: Path) -> list:
        return sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                      if p.is_file() and p.suffix != ".log")
    names_a, names_b = names(a), names(b)
    if names_a != names_b:
        diff.append("파일 집합 불일치: %r vs %r" % (names_a, names_b))
        return diff
    for name in names_a:
        if not filecmp.cmp(a / name, b / name, shallow=False):
            diff.append("byte 불일치: %s" % name)
    return diff


def check_determinism(run_dir: Path, out) -> list:
    with tempfile.TemporaryDirectory() as tmp:
        twin = build_into(Path(tmp) / RUN_ID, guard=False)
        diff = _cmp_tree(run_dir, twin)
    out.append("  재빌드 산출 byte 대조: %s" % ("동일" if not diff else diff))
    return diff


def check_negative_gate_order(out) -> list:
    """게이트 순서(required→provenance→resolved) 위반 표본에 같은 러너를 먹인다."""
    findings: list = []
    with tempfile.TemporaryDirectory() as tmp:
        bad = build_into(Path(tmp) / (RUN_ID + "-negative-lite"), guard=False)
        rows = events()
        # G1 해소 이벤트를 요구 이벤트보다 **앞**으로 옮긴다(at 재부여·cycle seq 재부여).
        req = [r for r in rows if (r["ref"] or {}).get("kind") == "gate-required"][0]
        res = [r for r in rows if (r["ref"] or {}).get("kind") == "gate-resolved"][0]
        rest = [r for r in rows if r is not req and r is not res]
        i = rest.index([r for r in rest if (r["ref"] or {}).get("kind")
                        == "user-resolution-provenance"][0])
        reordered = rest[:i] + [res, req] + rest[i:]
        for at, row in enumerate(reordered, start=1):
            row["at"] = at
        seqs: dict = {}
        for row in reordered:
            seqs[row["cycle_id"]] = seqs.get(row["cycle_id"], 0) + 1
            row["seq"] = seqs[row["cycle_id"]]
        _write_jsonl(bad / "events.jsonl", reordered)
        outdir = Path(tmp) / "verify-out"
        proc = _run_verify(bad, outdir)
        reports = sorted(outdir.glob("*.verify.json"))
        if len(reports) != 1:
            findings.append("음성 대조 리포트 산출이 1건이 아니다: %r" % [p.name for p in reports])
            return findings
        report = _load(reports[0])
        hygiene = [c for c in report["checks"] if c["check"] == "ledger_hygiene"][0]
        out.append("  음성 대조 exit=%d status=%s" % (proc.returncode, report["status"]))
        for f in hygiene["findings"]:
            out.append("    finding: %s" % f)
        if proc.returncode == 0:
            findings.append("음성 대조가 exit 0 — 러너가 거부를 내지 못했다")
        if not hygiene["findings"]:
            findings.append("음성 대조 findings 공집합 — 게이트 순서 검사가 발화하지 않았다")
        if hygiene["status"] != "fail":
            findings.append("음성 대조 ledger_hygiene status=%r (기대 fail)" % hygiene["status"])
    return findings


# ==========================================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="경량 레인 원장 표본 물리화 + 결정적 자체 점검")
    parser.add_argument("--check-only", action="store_true", help="물리화 생략(기존 표본만 점검)")
    args = parser.parse_args()

    run_dir = (Path(RUNS_DIR) / RUN_ID).resolve()
    if not args.check_only:
        build_into(run_dir)
        print("[SETUP-LITE] -> %s" % run_dir)
        print("  files: %s" % ", ".join(sorted(
            p.relative_to(run_dir).as_posix() for p in run_dir.rglob("*") if p.is_file())))
    else:
        print("[SETUP-LITE] --check-only -> %s" % run_dir)

    axes = [
        ("(1) 스키마 검증", lambda out: check_schema(run_dir, out)),
        ("(2) basis 왕복", lambda out: check_basis(run_dir, out)),
        ("(3) approvalState 파생", lambda out: check_approval(run_dir, out)),
        ("(4) 빌더 결정성", lambda out: check_determinism(run_dir, out)),
        ("(5) 음성 대조(게이트 순서)", lambda out: check_negative_gate_order(out)),
    ]
    failed = 0
    for label, fn in axes:
        out: list = []
        findings = fn(out)
        print("%s %s" % ("XX" if findings else "OK", label))
        for line in out:
            print(line)
        for f in findings:
            print("  FINDING: %s" % f)
        if findings:
            failed += 1
    print("[LITE-CHECK] %s (%d/%d 축 통과)" % ("FAIL" if failed else "PASS",
                                              len(axes) - failed, len(axes)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
