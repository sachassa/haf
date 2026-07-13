"""시나리오 (m) — Solution Design 성숙 run 의 orchestration 형태 B 호스팅 정본 스펙.

시나리오 (k)의 **동적 그래프 성장**(assess 산출 → 게이트 → task_added revision 편입)을
확장해, `pc-uahf-control-plane-001 v1` 의 **Solution Design 성숙 run 을 orchestration run 으로
호스팅**한다(05 §3.7 매핑). 04 §3.4 협업 프로토콜의 비종단 단계를 headless step 으로,
`Validating`(T8/T9/T10) 사용자 게이트를 `user_decision_required` 로 물리화한다.

05 §3.7 정본 매핑:
  Assessing/Proposing/Reconciling/Reviewing = headless step
  Validating(T8/T9/T10) = user_decision_required 게이트
  성숙 입력 = Contract v1(Ready — 04 §3.1-B 정합·2축 Ready 판정)

흐름(2단 게이트·3위상):
  [Phase 1] assess(sd_assess·user_decision 게이트·sonnet) 실행·Pass →
            **구조 게이트 물리 정지 exit 2** →
  [Advisor: 사용자 구조 게이트] → resolve_m --phase structure:
            assess 산출 stage-plan.json 검증(validate_stage_plan) →
            잔여 단계(propose×N·reconcile·review) task_added revision **일괄 append**
            (각 basis = {proposingStepRef:"assess", gateEventRef:<구조 게이트>} · PO-INV 5) →
  [Phase 2] propose×N → reconcile → review 순차 실행(dependsOn 사슬·review_required 게이트) →
            review Pass → **T8 Validating 게이트 물리 정지 exit 2** →
  [Advisor: T8 사용자 게이트] → resolve_m --phase final: 게이트 해소만(revision 0) →
  [Phase 3] 재실행 → 완주 exit 0.

스킵 분기(04 T2→T9): assess 가 정당하게 "스킵" 판정을 내면 stage-plan.json.maturation="skip"
이고 stages 는 비어 있다. resolve_m --phase structure 가 이를 감지해 **revision 0건**(게이트
해소만)으로 분기한다 — 성숙 단계 없이 경량 사용자 확인만.

산출 내용을 고정하지 않으므로(실 LLM 산출) CP2 재현성은 exact-content 가 아니라 **구조 계약**
(파일 존재·JSON 스키마·11키 stage·revision 인과 사슬·게이트 물리 정지)으로 확보한다.

모델 슬롯(sonnet)은 E2E 드라이버·정책 데이터 경계에만 존재한다(중립 코드 아님·격리 지점·
PO-INV 8 무관). provider 토큰이 허용되는 Adapter 격리 경계다.

러너·재생은 데이터 주도 스크립트 run_k.py·replay_k.py 를 그대로 재사용한다(config 주도·
k_scenario 무참조 — 신규 러너 불필요). 게이트 해소·검증만 (m) 고유이므로 resolve_m.py 만 신설.
"""

from __future__ import annotations

from pathlib import Path

RUN_ID = "orch-m-maturation-cp"
SONNET = "sonnet"
ALLOWED_TOOLS = ["Write", "Read", "Edit", "Bash(python:*)"]

# --- 산출물 파일명(내용은 고정하지 않음 — 실 LLM 산출) --------------------------
ASSESS_JUDGMENT_FILE = "assessing-judgment.md"
STAGE_PLAN_FILE = "stage-plan.json"

# --- 대상 Contract(읽기 전용·외부 프로젝트 저장소) -------------------------------
# pc-uahf-control-plane-001 v1 — greenfield-r003 종단 Ready(2축 판정·사용자 승인 2026-07-13).
# 이 파일은 대상 프로젝트 저장소(UAHF 밖) 소속이며 이 run 에서 절대 수정하지 않는다.
CONTRACT_V1_PATH = (
    r"C:\my-claude-project\uahf-control-plane\.claude\project-contract"
    r"\project-contract.v1.md"
)

# --- 외부 워크스페이스(run 디렉터리 밖·UAHF 저장소 내부 절대경로) ----------------
# k 와 달리 워크스페이스를 **UAHF 저장소 내부**의 SD 선례 위치 관례(events/maturation-rNNN/)에
# 둔다(승인 결정 2 — run 데이터 UAHF 내부·r001/r002 와 같은 위치). run 데이터 백엔드
# (runs/<id>/)와는 물리적으로 분리된 외부 워크스페이스다. 중립 코드 ProjectOrchestrator
# (workdir=...) 는 이미 파라미터이므로(orchestrator.py) config 데이터로만 실현한다(무수정).
#   e2e/  →  parents[1] = .../framework/adapters/claude
_HERE = Path(__file__).resolve().parent
_CLAUDE_DIR = _HERE.parents[1]
WORKSPACE_DIR = str(
    _CLAUDE_DIR / "solution-design-data" / "events" / "maturation-r003"
)


def _assess_ac() -> str:
    """Assess 단위 실행형 AC — 내용 비고정, 구조만 검사(종료 코드 0 = 통과).

    2파일 존재 ∧ stage-plan.json 파싱 ∧ maturation ∈ {needed,skip} ∧
    needed 면 stages 가 비어있지 않은 리스트.
    """
    return (
        "python -c \""
        "import json,os;"
        "assert os.path.exists('assessing-judgment.md'),'assessing-judgment.md';"
        "assert os.path.exists('stage-plan.json'),'stage-plan.json';"
        "d=json.load(open('stage-plan.json',encoding='utf-8'));"
        "m=d.get('maturation');"
        "assert m in ('needed','skip'),repr(m);"
        "assert m=='skip' or (isinstance(d.get('stages'),list) and len(d['stages'])>0),"
        "repr(d.get('stages'))\" (종료 코드 0 = 통과)"
    )


def _deleg(task, input_, output_, done, context):
    return {
        "from": "Advisor", "to": "Worker", "task": task,
        "input": input_, "output": output_, "done": done,
        "context": context, "constraints": "워크스페이스 밖 파일 생성·수정 금지",
    }


def _assess_prompt() -> str:
    """Assess 단계 자족적 프롬프트(fresh-context 전제) — 판정·역할 할당·stage-plan 구성 규칙.

    stages(propose×N·reconcile·review)의 **구성 규칙**만 지시하며, 실제 stage Task dict 는
    실 LLM 이 산출한다(드라이버 픽스처 아님). resolve_m.validate_stage_plan 이 구조를 검증한
    뒤에만 task_added revision 으로 승격한다(동적 그래프 성장).
    """
    return (
        "너는 Solution Design 성숙 run 의 **Assessing 단계**(04-solution-design §3.2 복잡도 "
        "판정 + §3.3 역할 할당)를 수행하는 실행 단위다. 대상 = Project Contract 인스턴스 "
        "pc-uahf-control-plane-001 v1(greenfield-r003 종단 Ready).\n\n"
        "[입력 정독] 다음 절대경로의 Contract v1 을 Read 도구로 **읽기 전용** 정독하라(수정 금지):\n"
        "  " + CONTRACT_V1_PATH + "\n"
        "이 파일은 **대상 프로젝트 저장소(UAHF 밖) 소속**이며 이 run 에서 절대 수정하지 않는다"
        "(관찰 전용).\n\n"
        "[판정 — 04 §3.2] 이 Contract 를 성숙(superseding v2)할 필요가 있는가, 아니면 스킵(v1 을 "
        "그대로 소비)인가를 판정하라. 판정 근거를 Contract 의 실측 필드(architectureDirection.open·"
        "readiness.openQuestions·requirements·risks 등)로 제시하라. 판정은 이진 분기다 — "
        "'needed'(성숙 필요) 또는 'skip'(스킵). 스킵도 정당한 산출이다(무근거로 성숙을 강제하지 마라).\n\n"
        "[역할 할당 — 04 §3.3] 성숙이 다뤄야 할 **설계 관심사**를 식별하고 각 관심사에 최소 역할을 "
        "할당하라(**최소 할당 SP-INV 8** — 역할 1~3개·불필요한 다중 역할 금지). 역할명은 **개방 "
        "네임스페이스**다(고정 카탈로그·표준 팀 열거 금지) — 이 run 의 자유 논리 선언이다. 각 역할은 "
        "roleId·capability(어느 설계 관심사에 대해 설계 결정을 끌어올리는가)를 가진다.\n\n"
        "[산출 1 — assessing-judgment.md] 현재 작업 디렉터리(이 워크스페이스)에 자유 서술 문서로 "
        "판정(needed|skip)·근거·식별 관심사·할당 역할(roleId·capability)을 서술하라. 형식은 자유이되 "
        "위 네 요소를 반드시 포함한다.\n\n"
        "[산출 2 — stage-plan.json] 현재 작업 디렉터리에 다음 스키마의 JSON 을 산출하라"
        "(최상위 단일 객체·UTF-8):\n"
        "  {\n"
        "    \"maturation\": \"needed\" | \"skip\",\n"
        "    \"concerns\": [<식별 관심사 문자열 배열>],\n"
        "    \"roles\": [<{\"roleId\":..., \"capability\":...} 객체 배열>],\n"
        "    \"stages\": [<Task dict 배열 — maturation=='needed' 일 때만 비어있지 않게; "
        "'skip' 이면 [] 또는 생략>]\n"
        "  }\n\n"
        "[stages 구성 규칙 — maturation=='needed' 인 경우만] stages 는 아래 순서·규칙으로 구성한다. "
        "각 원소는 **11키 스키마**를 모두 가진 Task dict 다: id·task·done·interfaceContract·"
        "ownedBoundary·dependsOn·delegation·capability·role·model·unitType.\n"
        "  (A) propose 단계 — **할당 역할당 1개**. id=\"propose-<역할슬러그>\"(슬러그 = roleId 의 "
        "소문자·하이픈 표기), unitType=\"sd_propose\", dependsOn=[\"assess\"], "
        "interfaceContract={\"produces\":[\"proposal-<슬러그>.md\"],\"consumes\":"
        "[\"assessing-judgment.md\"]}, ownedBoundary=[\"proposal-<슬러그>.md\"], "
        "capability=\"cap-sd-propose\". 서로 다른 역할의 proposal 파일명은 겹치지 않게 하라"
        "(병렬 실행·소유 경계 비중첩).\n"
        "  (B) reconcile 단계 — **정확히 1개**. id=\"reconcile\", unitType=\"sd_reconcile\", "
        "dependsOn=[**모든 propose id**], interfaceContract={\"produces\":"
        "[\"reconciling-record.md\"],\"consumes\":[<모든 proposal 파일>]}, "
        "ownedBoundary=[\"reconciling-record.md\"], capability=\"cap-sd-reconcile\".\n"
        "  (C) review 단계 — **정확히 1개**. id=\"review\", unitType=\"sd_review\", "
        "dependsOn=[\"reconcile\"], interfaceContract={\"produces\":[\"reviewing-record.md\","
        "\"candidate/project-contract.v2.CANDIDATE.md\"],\"consumes\":[\"reconciling-record.md\"]}, "
        "ownedBoundary=[\"reviewing-record.md\",\"candidate/project-contract.v2.CANDIDATE.md\"], "
        "capability=\"cap-sd-review\". 후보 문면(candidate/project-contract.v2.CANDIDATE.md)은 "
        "대상 Contract v1 전문을 성숙 반영해 재작성하되 meta.instanceVersion=2·meta.supersedes=1 로 "
        "하고 **placeholder 3개소**를 포함한다 — (i) readiness.userApproval 미확정 placeholder "
        "(ii) provenance.terminal 미확정 placeholder (iii) 문서 상단 CANDIDATE(미발행) 배너.\n"
        "  각 stage 의 role=\"Worker\", model=\"sonnet\", delegation 은 8필드(from=\"Advisor\"·"
        "to=\"Worker\"·task=해당 task 와 동일·input·output=산출 파일·done=해당 done 과 동일·"
        "context·constraints=\"워크스페이스 밖 파일 생성·수정 금지\").\n"
        "  각 stage 의 **task 프롬프트는 자족적**이어야 한다(fresh-context 전제) — 입력 파일의 "
        "상대/절대 경로·산출 요건·워크스페이스 밖 파일 금지·이 디렉터리의 events.jsonl 등 기존 파일 "
        "무접촉·Execute 종료 시 CP1 자체 점검(done AC 실행) 지시를 모두 포함한다.\n"
        "  각 stage 의 **done 은 단일 `python -c` 한 줄 실행형 AC**(종료 코드 0 = 통과)로, 자신이 "
        "산출하는 파일의 존재·필수 마커/JSON 키를 검사한다(내용 고정 아님·구조 검사).\n\n"
        "[스킵 분기] 판정이 'skip' 이면 stages 를 비우고(빈 배열 또는 생략) concerns·roles 도 그에 "
        "맞춰 최소로 둔다 — 성숙 단계를 만들지 않는다(04 T2→T9 경량 사용자 확인 경로).\n\n"
        "[금지] 이 워크스페이스 밖의 어떤 파일도 생성·수정하지 마라. 이 디렉터리의 events.jsonl"
        "(Solution Design 정본 로그 — Advisor 소관)·기타 기존 파일을 생성·수정·삭제하지 마라 — "
        "너의 산출은 오직 " + ASSESS_JUDGMENT_FILE + " 와 " + STAGE_PLAN_FILE + " 두 파일뿐이다. "
        "대상 Contract v1 은 읽기 전용이다.\n\n"
        "[CP1 자체 점검] Execute 종료 시 done 의 AC 커맨드를 실제로 실행하여(CP1 자체 점검) 종료 "
        "코드 0 을 확인한 뒤에만 완료 보고를 내라. 완료 보고 artifacts 에 두 산출 파일 경로를 실어라."
    )


def assess_task():
    """Assess 단위 assess — 복잡도 판정 + 역할 할당 + stage-plan 산출(sd_assess·user_decision 게이트).

    산출 stage-plan.json 은 resolve_m 이 validate_stage_plan 으로 검증 후 잔여 단계 task_added
    revision 으로 승격하는 **실 LLM 산출 artifact**다(드라이버 픽스처 아님). dependsOn=[] — run 의
    유일한 초기 단위이며, 이 단위 Pass 뒤 사용자 구조 게이트(user_decision)가 물리 정지시킨다.
    """
    ac = _assess_ac()
    task = _assess_prompt()
    deleg = _deleg(
        task,
        "pc-uahf-control-plane-001 v1(읽기 전용·외부 저장소) + 빈 워크스페이스",
        ASSESS_JUDGMENT_FILE + ", " + STAGE_PLAN_FILE,
        ac,
        ["Project Orchestration (m) — SD 성숙 run 의 orchestration 형태 B 호스팅(05 §3.7)",
         "04-solution-design §3.2 복잡도 판정 · §3.3 역할 최소 할당(SP-INV 8·개방 네임스페이스)",
         "대상 Contract v1 은 읽기 전용 참조(수정 금지) — 대상 프로젝트 저장소 소속",
         "stage-plan.json 은 사용자 구조 게이트 해소 후 resolve_m 이 검증·승격한다"],
    )
    return {
        "id": "assess",
        "task": task,
        "done": ac,
        "interfaceContract": {
            "produces": [ASSESS_JUDGMENT_FILE, STAGE_PLAN_FILE],
            "consumes": [CONTRACT_V1_PATH],
        },
        "ownedBoundary": [ASSESS_JUDGMENT_FILE, STAGE_PLAN_FILE],
        "dependsOn": [],
        "delegation": deleg,
        "capability": "cap-sd-assess",
        "role": "Worker",
        "model": SONNET,
        "unitType": "sd_assess",   # 게이트 descriptor(정책 매칭용·개방 데이터).
    }


def initial_graph():
    return {
        "goal": "pc-uahf-control-plane-001 v1 성숙 run 의 orchestration 호스팅(05 §3.7)",
        "tasks": [assess_task()],
        "completion": "all-passed",
    }


def gate_policy():
    """assess → user_decision(구조 게이트·정지) · propose/reconcile → review · review → user_decision(T8·정지).

    비종단 4단계 중 Assessing(assess)·Reviewing(review)의 뒤에 사용자 게이트를 둔다:
      - assess 뒤 user_decision = **구조 승인 게이트**(동적 그래프 성장 전 사용자 확정).
      - review 뒤 user_decision = **T8 Validating 게이트**(04 §3.4 T8/T9/T10 물리화·05 §3.7).
    Proposing/Reconciling 는 review_required(CP2 외 추가 독립 리뷰·비정지).
    """
    return {
        "entries": [
            {"target": {"unitType": "sd_assess"}, "gate": "user_decision_required"},
            {"target": {"unitType": "sd_propose"}, "gate": "review_required"},
            {"target": {"unitType": "sd_reconcile"}, "gate": "review_required"},
            {"target": {"unitType": "sd_review"}, "gate": "user_decision_required"},
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
        "timeout": 420,
        "allowed_tools": ALLOWED_TOOLS,
        "output_format": "json",
        "workspace_dir": WORKSPACE_DIR,
        "note": (
            "SD 성숙 run 의 orchestration 형태 B 호스팅 **첫 사례**(05 §3.7) — Assessing/Proposing/"
            "Reconciling/Reviewing = headless step·Validating = user_decision 게이트. 대상 = "
            "pc-uahf-control-plane-001 v1(Ready). 산출 내용 비고정(실 LLM 산출)·2단 사용자 게이트"
            "(구조·T8)는 실 사용자가 해소(시뮬레이션 0·resolve_m). workspace_dir = UAHF 저장소 내부 "
            "SD 선례 위치(events/maturation-r003/)·run 디렉터리 밖 외부 워크스페이스. **주의**: "
            "workspace 의 events.jsonl 은 Solution Design 정본 로그(Advisor 가 규약 절차로 append)이며 "
            "드라이버·step 은 쓰지 않는다."
        ),
    }
