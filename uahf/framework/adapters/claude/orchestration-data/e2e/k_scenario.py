"""시나리오 (k) — 비픽스처 소형 종단 흐름 정본 스펙 (OQ-PO-B4 해소 선행 스모크).

시나리오 (j)와의 결정적 차이 = **비픽스처**: (j)는 구현 제안을 드라이버 픽스처
(resolve_and_revise.j_scenario.impl_revision_payload)로 하드코딩했으나, (k)는 그 자리를
**그래프 내 실 LLM 제안 step(p1)의 산출 artifact(impl-proposal.json)**로 대체한다. 설계
내용·제안 내용은 고정하지 않는다(실 LLM 산출). 사용자 게이트도 시뮬레이션이 아니라 **실
사용자**가 해소한다(resolve_k.py — 05 §3.2 인과 사슬·PO-INV 5).

흐름:
  d1(설계·review 게이트·haiku) → p1(실 LLM 제안·user_decision 게이트·sonnet, dependsOn d1) →
  [물리 정지 exit 2] → resolve_k.py 가 **실 사용자 응답** 기록 + p1 산출 artifact 를
  검증(validate_proposal)해 task_added revision append(basis = proposingStepRef **p1** +
  gateEventRef) → impl(구현·review 게이트) → 완주.

산출 내용을 고정하지 않으므로 CP2 재현성은 exact-content 가 아니라 **구조 계약**(파일 존재·
첫 줄 형식·JSON 스키마·revision 인과 사슬·게이트 물리 정지)으로 확보한다.

모델 슬롯(haiku/sonnet)은 E2E 드라이버·정책 데이터 경계에만 존재한다(중립 코드 아님·격리
지점·PO-INV 8 무관). provider 토큰이 허용되는 Adapter 격리 경계다.
"""

from __future__ import annotations

RUN_ID = "orch-k-nonfixture-smoke"
HAIKU = "haiku"
SONNET = "sonnet"
ALLOWED_TOOLS = ["Write", "Read", "Edit", "Bash(python:*)"]

# --- 산출물 파일명(내용은 고정하지 않음 — 실 LLM 산출) --------------------------
D1_FILE = "design-decision.md"
PROPOSAL_FILE = "impl-proposal.json"

# --- 외부 워크스페이스(run 디렉터리 밖 절대경로) — W4 전제 실측용 ----------------
# run 데이터 백엔드(runs/<id>/)와 물리적으로 분리된 절대경로. 중립 코드
# ProjectOrchestrator(workdir=...) 는 이미 파라미터이므로(orchestrator.py:116·:419)
# 외부 워크스페이스는 config 데이터로만 실현한다(중립 코드 무수정).
WORKSPACE_DIR = (
    r"C:\Users\aime8\AppData\Local\Temp\claude"
    r"\C--my-claude-project-universa-agentic-harness-framework"
    r"\d9d393c9-726b-4364-bd4f-77e02970747d\scratchpad\orch-k-workspace"
)


def _design_ac() -> str:
    """설계 단위 실행형 AC — 내용 비고정, 구조만 검사(종료 코드 0 = 통과).

    파일 존재 ∧ 첫 줄이 'DESIGN-DECISION: ' 로 시작 ∧ 총 2줄 이상.
    """
    return (
        "python -c \"import io,os;p='design-decision.md';assert os.path.exists(p),p;"
        "L=io.open(p,encoding='utf-8').read().splitlines();"
        "assert L and L[0].startswith('DESIGN-DECISION: '),repr(L[:1]);"
        "assert len(L)>=2,len(L)\" (종료 코드 0 = 통과)"
    )


def _proposal_ac() -> str:
    """제안 단위 실행형 AC — impl-proposal.json 구조 검사(종료 코드 0 = 통과).

    json.load 성공 ∧ 필수 키 11종 존재 ∧ id=='impl' ∧ dependsOn==['d1'].
    """
    return (
        "python -c \"import json;d=json.load(open('impl-proposal.json',encoding='utf-8'));"
        "ks=['id','task','done','interfaceContract','ownedBoundary','dependsOn',"
        "'delegation','capability','role','model','unitType'];"
        "miss=[k for k in ks if k not in d];assert not miss,miss;"
        "assert d['id']=='impl',d['id'];assert d['dependsOn']==['d1'],d['dependsOn']\" "
        "(종료 코드 0 = 통과)"
    )


def _deleg(task, input_, output_, done, context):
    return {
        "from": "Advisor", "to": "Worker", "task": task,
        "input": input_, "output": output_, "done": done,
        "context": context, "constraints": "워크스페이스 밖 파일 생성·수정 금지",
    }


def design_task():
    """설계 단위 d1 — review 게이트 대상(unitType=design·비정지).

    내용은 고정하지 않는다(실 LLM 결정). 산출 계약만 강제한다(첫 줄 형식·2줄 이상).
    """
    ac = _design_ac()
    task = (
        "현재 작업 디렉터리(이 워크스페이스)에 %s 파일을 생성하라. 주제: 대시보드 이벤트 "
        "타임라인 렌더링의 정렬 키를 seq(이벤트 로그 순서 값)와 물리 timestamp 중에서 "
        "선택하고, 그 선택의 근거를 2~3줄로 서술하라. 파일의 **첫 줄은 정확히** "
        "`DESIGN-DECISION: <선택값>` 형식이어야 한다(<선택값>은 네 결정 — 예: seq 또는 "
        "timestamp). 둘째 줄부터 근거를 적어 **총 2줄 이상**이 되게 하라. 이 워크스페이스 "
        "밖의 어떤 파일도 생성·수정하지 마라. Execute 종료 시 done 의 AC 커맨드를 실제로 "
        "실행하여(CP1 자체 점검) 종료 코드 0 을 확인한 뒤에만 완료 보고를 내라. 완료 보고 "
        "artifacts 에 %s 경로를 실어라." % (D1_FILE, D1_FILE)
    )
    deleg = _deleg(
        task, "빈 워크스페이스(설계 착수)", D1_FILE, ac,
        ["Project Orchestration (k) 비픽스처 스모크 — 설계 단위·review 게이트",
         "상위 Contract 는 읽기 전용 참조(재실행 금지)"],
    )
    return {
        "id": "d1",
        "task": task,
        "done": ac,
        "interfaceContract": {"produces": [D1_FILE]},
        "ownedBoundary": [D1_FILE],
        "dependsOn": [],
        "delegation": deleg,
        "capability": "cap-design",
        "role": "Worker",
        "model": HAIKU,
        "unitType": "design",   # 게이트 descriptor(정책 매칭용·07 개방 데이터).
    }


def proposal_task():
    """제안 단위 p1 — 실 LLM 이 설계 결정을 소비해 구현 task 1개를 JSON 으로 제안한다.

    user_decision 게이트 대상(unitType=proposal·정지). dependsOn=[d1] — 설계 Passed 후
    착수(07 R2 인과 사슬). 산출 impl-proposal.json 은 resolve_k.py 가 검증 후 task_added
    revision 으로 승격하는 **실 LLM 산출 artifact**다(드라이버 픽스처 아님·OQ-PO-B4).

    모델은 sonnet — JSON 스키마 준수 신뢰성(haiku 보다 구조화 산출 안정). 이 값은 정책
    데이터 경계에만 존재한다(PO-INV 8 무관).
    """
    ac = _proposal_ac()
    task = (
        "워크스페이스의 %s 를 읽고, 그 결정을 구현하는 **단일 소형 구현 task 1개**를 JSON 으로 "
        "제안해 %s 에 기록하라. JSON 최상위는 단일 객체이며 필수 키는 다음 11종이다:\n"
        "  - id: 정확히 'impl'.\n"
        "  - task: 자족적 지시문(fresh-context 전제) — 구현 대상 파일명·내용 요건·워크스페이스 "
        "밖 파일 생성/수정 금지·Execute 종료 시 CP1 자체 점검(done AC 실행) 지시를 모두 포함.\n"
        "  - done: 단일 `python -c` 한 줄 실행형 AC(종료 코드 0 = 통과) — 네가 제안한 산출 "
        "파일을 검사한다.\n"
        "  - interfaceContract: {\"produces\": [<산출 파일 1개>], \"consumes\": [\"%s\"]}.\n"
        "  - ownedBoundary: [<산출 파일 1개>](상대경로).\n"
        "  - dependsOn: 정확히 [\"d1\"].\n"
        "  - delegation: {\"from\":\"Advisor\",\"to\":\"Worker\",\"task\":<task 와 동일>,"
        "\"input\":\"%s\",\"output\":<산출 파일>,\"done\":<done 과 동일>,\"context\":[...],"
        "\"constraints\":\"워크스페이스 밖 파일 생성·수정 금지\"}.\n"
        "  - capability: 'cap-impl'.\n"
        "  - role: 'Worker'.\n"
        "  - model: 'haiku'.\n"
        "  - unitType: 'implementation'.\n"
        "구현 task 는 **파일 1개 생성 규모**를 넘지 마라. 산출 파일명은 %s 와 겹치지 않게 "
        "하라. %s 외의 다른 파일은 생성하지 마라. 기록 후 done 의 AC 를 실제로 실행하여 "
        "종료 코드 0 을 확인한 뒤에만 완료 보고를 내라. 완료 보고 artifacts 에 %s 경로를 실어라."
        % (D1_FILE, PROPOSAL_FILE, D1_FILE, D1_FILE, PROPOSAL_FILE, PROPOSAL_FILE, PROPOSAL_FILE)
    )
    deleg = _deleg(
        task, D1_FILE, PROPOSAL_FILE, ac,
        ["Project Orchestration (k) 비픽스처 스모크 — 제안 단위·user_decision 게이트",
         "산출 artifact 는 실 사용자 게이트 해소 후 resolve_k.py 가 검증·승격한다"],
    )
    return {
        "id": "p1",
        "task": task,
        "done": ac,
        "interfaceContract": {"produces": [PROPOSAL_FILE], "consumes": [D1_FILE]},
        "ownedBoundary": [PROPOSAL_FILE],
        "dependsOn": ["d1"],
        "delegation": deleg,
        "capability": "cap-proposal",
        "role": "Worker",
        "model": SONNET,
        "unitType": "proposal",
    }


def initial_graph():
    return {
        "goal": "비픽스처 소형 종단: 설계→실 LLM 제안→게이트→구현",
        "tasks": [design_task(), proposal_task()],
        "completion": "all-passed",
    }


def gate_policy():
    """설계 → review · 제안 → user_decision(정지·실 사용자 해소) · 구현 → review."""
    return {
        "entries": [
            {"target": {"unitType": "design"}, "gate": "review_required"},
            {"target": {"unitType": "proposal"}, "gate": "user_decision_required"},
            {"target": {"unitType": "implementation"}, "gate": "review_required"},
        ],
        "userActorClass": "human",
        "escalationResolvers": ["Advisor", "human"],
        "gateRaiser": "Advisor",
    }


def config():
    return {
        "run_id": RUN_ID,
        "policy": "auto_approve",
        "retry_limit": 2,
        "timeout": 300,
        "allowed_tools": ALLOWED_TOOLS,
        "output_format": "json",
        "workspace_dir": WORKSPACE_DIR,
        "note": (
            "비픽스처 스모크 — 제안 내용·설계 내용 비고정(실 LLM 산출)·사용자 게이트 실 "
            "사용자 해소 예정(시뮬레이션 0). OQ-PO-B4 해소 선행 스모크(project-orchestration-"
            "binding.md:201). workspace_dir 은 run 디렉터리 밖 외부 절대경로(W4 전제 실측)."
        ),
    }
