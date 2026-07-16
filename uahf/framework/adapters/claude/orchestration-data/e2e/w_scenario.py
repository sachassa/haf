"""시나리오 (w) — MVP 구현 orchestration run 정본 스펙 (OQ-PO-B4 완전 해소 지점).

시나리오 (k)가 **소형**으로 실증한 "설계 단위 산출 artifact를 실 LLM 제안 step이 소비해
구현 task를 제안하는 완전 성숙 run"(project-orchestration-binding.md:201)을 (w)가 **실
프로젝트 규모**로 완성한다. (k)는 단일 파일 1개 규모의 구현 1건을 제안했으나, (w)는:
  - 성숙 완결된 설계 artifact(maturation-r003 reconciling/reviewing-record.md·통합 아키텍처)를
    실 LLM 제안 step(impl-plan)이 소비해 **구현 task 3~6개의 실행 계획**을 제안하고,
  - 사용자 게이트 승인 후 그 계획을 task_added revision **일괄 편입**하며(resolve_w),
  - 구현 step들이 실 CLI로 대상 프로젝트(uahf-control-plane)에 **Next.js MVP 대시보드를
    실제로 구현**한다(수동 스캐폴딩·npm install·`npm run build` 통과까지).

흐름(1단 게이트·비종단 review):
  impl-plan(실 LLM 제안·user_decision 게이트·sonnet, dependsOn []) 실행·Pass →
    **user_decision 게이트 물리 정지 exit 2** →
  [Advisor: 사용자 구조 게이트] → resolve_w --phase structure:
    impl-plan 산출 impl-plan.json 검증(validate_impl_plan·검증 우선) →
    구현 task 전체(3~6개) task_added revision **일괄 append**
    (각 basis = {proposingStepRef:"impl-plan", gateEventRef:<게이트>} · PO-INV 5) →
  구현 step들 순차/병렬 실행(dependsOn DAG·review_required 게이트=비정지) → 완주 exit 0.

(m)과의 차이: (m)은 Validating(T8)에 **2단째 사용자 게이트**가 있었으나(성숙 발행이 사용자
승인 게이트에 종속), (w)의 구현 단계 게이트는 **review_required(비정지)** 이므로 구조 게이트
1단만 사용자 해소가 필요하다 — 따라서 resolve_w 는 structure phase 만 갖는다(final 불필요).

산출 내용을 고정하지 않으므로(실 LLM 산출) CP2 재현성은 exact-content 가 아니라 **구조 계약**
(파일 존재·JSON 스키마·11키 task·revision 인과 사슬·게이트 물리 정지·보호 경계 불가침)으로
확보한다.

모델 슬롯(sonnet)은 E2E 드라이버·정책 데이터 경계에만 존재한다(중립 코드 아님·격리 지점·
PO-INV 8 무관). provider 토큰이 허용되는 Adapter 격리 경계다.

러너·재생은 데이터 주도 스크립트 run_k.py·replay_k.py 를 그대로 재사용한다(config 주도·
w_scenario 무참조 — 신규 러너 불필요). 게이트 해소·검증만 (w) 고유이므로 resolve_w.py 만 신설.
"""

from __future__ import annotations

from pathlib import Path

RUN_ID = "orch-w-impl-cp"
SONNET = "sonnet"

# 구현 step 이 실제 코드를 작성·설치·빌드하려면 npm/npx/node 셸 접근이 필요하다(수동 스캐폴딩·
# npm install·npm run build). python 은 CP1 자체 점검 AC 실행용. 이 토큰들은 Adapter 격리
# 경계(정책 데이터)에만 존재한다.
ALLOWED_TOOLS = [
    "Write", "Read", "Edit", "Glob", "Grep",
    "Bash(npm:*)", "Bash(npx:*)", "Bash(node:*)", "Bash(python:*)",
]

# --- 산출물 파일명(내용은 고정하지 않음 — 실 LLM 산출) --------------------------
IMPL_PLAN_FILE = "impl-plan.json"

# --- 외부 워크스페이스 = 실 소비 프로젝트(run 디렉터리 밖·UAHF 저장소 밖 절대경로) --------
# W4 대상 = uahf-control-plane 실 git 저장소(main). 구현 step 이 이 디렉터리 안에 Next.js 앱을
# 실제로 생성한다. run 데이터 백엔드(runs/<id>/)와는 물리적으로 분리된 외부 워크스페이스다.
# 중립 코드 ProjectOrchestrator(workdir=...) 는 이미 파라미터이므로(orchestrator.py) config
# 데이터로만 실현한다(중립 코드 무수정·07 격리 경계).
WORKSPACE_DIR = r"C:\my-claude-project\uahf-control-plane"

# --- 대상 Contract v2(구현 명세의 정본·읽기 전용·외부 프로젝트 저장소) ------------
# pc-uahf-control-plane-001 v2 — Matured(maturation-r003·사용자 승인 2026-07-14). 이 파일은 대상
# 프로젝트 저장소(UAHF 밖) 소속이며 이 run 에서 절대 수정하지 않는다(관찰 전용).
CONTRACT_V2_PATH = (
    r"C:\my-claude-project\uahf-control-plane\.claude\project-contract"
    r"\project-contract.v2.md"
)

# --- 설계 정본 산출(통합 아키텍처·읽기 전용·UAHF 저장소 내부 SD 데이터) ------------
# maturation-r003 성숙 run 의 Reconcile/Review 산출. 인터페이스 계약·모듈 경계·파일 배치의
# 정본이다. 이 run 에서는 읽기 전용 참조다(SD append-only 로그 훼손 금지).
#   e2e/  →  parents[1] = .../framework/adapters/claude
_HERE = Path(__file__).resolve().parent
_CLAUDE_DIR = _HERE.parents[1]
_R003 = _CLAUDE_DIR / "solution-design-data" / "events" / "maturation-r003"
RECONCILING_PATH = str(_R003 / "reconciling-record.md")
REVIEWING_PATH = str(_R003 / "reviewing-record.md")

# UAHF 저장소 경로(대시보드 fs-reader 가 orchestration-data/runs/ 를 정독할 소스 루트).
# 소스 하드코딩 금지 — 구현 계획은 이를 .env.local 로 주입하도록 지시한다.
UAHF_REPO_PATH = r"C:\my-claude-project\universa-agentic-harness-framework"


def _implplan_ac() -> str:
    """impl-plan 단위 실행형 AC — 내용 비고정, 구조만 검사(종료 코드 0 = 통과).

    impl-plan.json 존재 ∧ 파싱 ∧ tasks 가 1~6개 리스트 ∧ 각 task 가 11키 전부 보유.
    """
    return (
        "python -c \"import json,os;p='impl-plan.json';"
        "assert os.path.exists(p),p;"
        "d=json.load(open(p,encoding='utf-8'));t=d.get('tasks');"
        "assert isinstance(t,list) and 1<=len(t)<=6,repr(len(t) if isinstance(t,list) else t);"
        "ks=['id','task','done','interfaceContract','ownedBoundary','dependsOn',"
        "'delegation','capability','role','model','unitType'];"
        "miss=[(x.get('id'),k) for x in t for k in ks if k not in x];"
        "assert not miss,miss\" (종료 코드 0 = 통과)"
    )


def _deleg(task, input_, output_, done, context):
    return {
        "from": "Advisor", "to": "Worker", "task": task,
        "input": input_, "output": output_, "done": done,
        "context": context,
        "constraints": (
            "워크스페이스 밖 파일 생성·수정 금지. 보호 경계(.claude/·install-manifest.md·"
            "specs/·framework/)는 읽기 전용 — 생성·수정·삭제 금지."
        ),
    }


def _implplan_prompt() -> str:
    """impl-plan 단계 자족적 프롬프트(fresh-context 전제) — 설계 소비·구현 task 구성 규칙.

    이 단계는 코드를 직접 작성하지 않는다. 성숙 산출 설계 artifact를 소비해 **구현 task 3~6개의
    실행 계획**을 impl-plan.json 으로 산출한다. resolve_w.validate_impl_plan 이 구조를 검증한
    뒤에만 task_added revision 으로 승격한다(동적 그래프 성장). 실제 stage Task dict 는 실 LLM 이
    산출한다(드라이버 픽스처 아님 — OQ-PO-B4 완전 해소).
    """
    return (
        "너는 uahf-control-plane 프로젝트의 **MVP 구현 계획 단계**(Project Orchestration 형태 B "
        "— impl-plan 제안 step)를 수행하는 실행 단위다. 대상 = 성숙 완결된 Project Contract "
        "pc-uahf-control-plane-001 v2(Matured — maturation-r003).\n\n"
        "[역할] 너는 코드를 직접 작성하지 않는다. 성숙 산출 설계 artifact를 소비해 **구현 task "
        "3~6개의 실행 계획**을 JSON 으로 산출한다. 각 구현 task 는 이후(사용자 게이트 승인 후) "
        "task_added revision 으로 편입되어 별도 fresh-context 세션이 실제 코드를 작성한다.\n\n"
        "[입력 정독 — 3개 문서·전부 읽기 전용 절대경로] 다음을 Read 도구로 정독하라(수정 금지):\n"
        "  ① Contract v2 (구현 명세의 정본 — architectureDirection.decisions 14항):\n"
        "     " + CONTRACT_V2_PATH + "\n"
        "  ② 통합 아키텍처 (모듈 경계·파일 배치·인터페이스 계약):\n"
        "     " + RECONCILING_PATH + "\n"
        "  ③ 리뷰 기록 (비차단 관찰 사항 정리 지침 §4.2):\n"
        "     " + REVIEWING_PATH + "\n"
        "  ③의 §4.2 = `GateEvent.state` 필드가 생산자·소비자 없는 필드로 남아 있다는 관찰이다. "
        "구현 시 (i) 타입 선언에서 제거하거나 (ii) `reduceGateStates` 산출 후 이벤트 목록에 "
        "역주입하는 **후처리 캐싱 필드로 명시 재정의** 하는 것 중 **하나를 택해** 반영하도록 관련 "
        "구현 task 문면에 지시하라.\n\n"
        "[대상 프로젝트 현황] `" + WORKSPACE_DIR + "\\` 는 **이미 존재하는 git 저장소(main)** 이며 "
        ".claude/·framework/·specs/·install-manifest.md(UAHF Scaffold+Contract)를 보유한다. "
        "**Next.js 앱은 아직 없다** — 구현 task 들이 package.json·설정·소스를 생성하고 npm install "
        "까지 수행해야 한다.\n"
        "  - `npx create-next-app` 은 **비어있지 않은 디렉터리를 거부**하므로 쓰지 마라. 대신 "
        "**수동 스캐폴딩**을 계획하라: package.json 직접 작성 → npm install → 설정 파일"
        "(next.config·tsconfig·tailwind·postcss 등) 작성 → 소스 파일 작성.\n"
        "  - 실행 환경(실측): Node v24.15.0 · npm 11.12.1.\n\n"
        "[보호 경계 — 절대 수정 금지] 다음은 UAHF Scaffold·Contract 로 **읽기 전용**이다. 어느 "
        "구현 task 의 ownedBoundary 에도 넣지 말고, task 문면에도 수정 금지를 명시하라:\n"
        "  - .claude/**  (Scaffold·Contract·AGENT.md·agents)\n"
        "  - install-manifest.md\n"
        "  - specs/**\n"
        "  - framework/**\n"
        "  구현 산출은 앱 파일(package.json·package-lock.json·next.config.*·tsconfig.json·"
        "tailwind/postcss 설정·app/·lib/·components/ 등)과 npm install 산출(node_modules)로 "
        "한정한다.\n\n"
        "[env 설정] UAHF 저장소 경로는 소스 하드코딩 금지 — `.env.local` 에 둔다"
        "(예: `UAHF_REPO_PATH=" + UAHF_REPO_PATH + "`). fs-reader 가 이 env 를 읽어 "
        "orchestration-data/runs/ 를 읽기 전용 정독하도록 계획하라.\n\n"
        "[산출 — " + IMPL_PLAN_FILE + "] 현재 작업 디렉터리(이 워크스페이스 = 대상 프로젝트 루트)에 "
        + IMPL_PLAN_FILE + " 을 산출하라. 최상위는 단일 객체이며 스키마는:\n"
        "  { \"tasks\": [ <구현 task dict 3~6개> ] }\n"
        "각 구현 task dict 는 **11키 스키마**를 모두 가진다: id·task·done·interfaceContract·"
        "ownedBoundary·dependsOn·delegation·capability·role·model·unitType.\n\n"
        "[구현 task 구성 규칙]\n"
        "  - unitType = \"implementation\" (전부).\n"
        "  - role = \"Worker\", model = \"sonnet\" (전부).\n"
        "  - id = 고유 슬러그(케밥 케이스). 계획 내 유일(중복 금지).\n"
        "  - dependsOn = **계획 내 다른 task id 만** 참조하는 배열(DAG — 자기참조·사이클 금지). "
        "선행 산출에 의존하면 그 task id 를 넣어라(예: 도메인 계층은 스캐폴딩 task 에 의존).\n"
        "  - ownedBoundary = 이 task 가 생성/수정하는 파일·디렉터리의 **상대경로 배열**(대상 "
        "프로젝트 루트 기준·비어있지 않게). **task 간 상호 비중첩**(한 경로가 다른 task 경로의 "
        "조상/자손이면 안 됨 — 병렬 실행 대비). 보호 경계(위) 항목 금지·절대경로/`..` 금지.\n"
        "  - interfaceContract = {\"produces\":[<산출 파일/디렉터리>], \"consumes\":[<선행 task "
        "산출 또는 설계 문서>]}.\n"
        "  - task = **fresh-context 자족 지시문** — 구현 파일 경로·내용 요건·근거가 되는 설계 결정 "
        "인용(Contract v2 architectureDirection 항 또는 reconciling-record §번호)·워크스페이스 밖 "
        "파일 금지·보호 경계 무수정·Execute 종료 시 CP1 자체 점검(done AC 실행) 지시를 모두 "
        "포함한다.\n"
        "  - done = **단일 셸 커맨드 실행형 AC**(종료 코드 0 = 통과) — python -c / node -e / "
        "npm run 등. 해당 task 산출만 검사한다(파일 존재·타입 체크·빌드 통과 등·비공백).\n"
        "  - delegation = 8필드(from=\"Advisor\"·to=\"Worker\"·**task=\"위 task 필드와 동일\"**"
        "(참조형 sentinel — 권장)·input·output=산출 파일·**done=\"위 done 필드와 동일\"**"
        "(참조형 sentinel — 권장)·context·constraints=\"워크스페이스 밖 파일 생성·수정 금지, "
        "보호 경계(.claude/·install-manifest.md·specs/·framework/) 무수정\").\n"
        "    delegation.task/done 은 상위 task/done 전문을 다시 쓰지 말고 위 sentinel 문면"
        "(\"위 task 필드와 동일\"·\"위 done 필드와 동일\")을 **그대로** 넣어라(참조형 표준·토큰 "
        "절약). 상위 task/done 원문을 **바이트 동일**하게 전재하는 것도 허용된다 — 둘 중 하나면 "
        "된다. **요약·부분 발췌·변형은 검증 실패다.**\n\n"
        "[권장 분해 — 참고만·강제 아님] 아래는 예시일 뿐 네 판단으로 3~6개로 조정하라:\n"
        "  ① 프로젝트 스캐폴딩 — package.json(deps: next·react·react-dom·typescript·@types/*·"
        "zod·tailwindcss·postcss·autoprefixer·shadcn 계열 등) 작성 → npm install → next.config·"
        "tsconfig.json·tailwind/postcss 설정·app/globals.css·app/layout.tsx 최소 골격. "
        "done 에 npm install 성공 또는 `npx tsc --noEmit` 통과 등.\n"
        "  ② 파서/도메인 계층 — lib/data/types.ts(NormalizedEvent 판별 유니온·Revision·Artifact·"
        "InvokeLog·RunSummary·LineageTree/LineageTreeNode·CostAggregate/ModelCostAggregate + zod "
        "이중 정의), lib/data/parsers/(events·revisions·artifacts·invoke-log·fs-reader), "
        "lib/data/domain/(gate-state[reduceGateStates]·lineage[buildLineageGraph+toLineageTree]·"
        "cost-aggregate[aggregateCosts]·run-summary). 단방향 의존 parsers→domain 고정. "
        "reconciling §4 계층 구조·§4.2 신설 타입·§4.3 인터페이스 계약을 인용. GateEvent.state "
        "정리(reviewing §4.2) 반영.\n"
        "  ③ UI 계층 — app/page.tsx(목록·RunSummary[]) + app/runs/[runId]/page.tsx(4패널) + "
        "loading.tsx + not-found.tsx + components/(RunHeader·EventTimelinePanel[+"
        "ParserWarningAlert]·LineagePanel[재귀 LineageTreeNode]·CostPanel[CostSummaryCards+"
        "CostBreakdownTable]) + shadcn/ui 컴포넌트. RSC 가 domain/* 함수를 직접 await·API route "
        "미생성·force-dynamic(reconciling §4.3·Contract v2 결정).\n"
        "  ④ 종단 빌드·실데이터 스모크 — .env.local(UAHF_REPO_PATH) 설정 후 실데이터(예: "
        "orch-k run) 렌더 확인. **마지막(빌드) task 의 done 은 반드시 `npm run build` 성공"
        "(종료 코드 0)을 포함**하라. 이 task 의 ownedBoundary 도 비어있지 않게 하라(예: "
        ".env.local·빌드 스모크 산출 파일 등 이 task 가 소유하는 구체 상대경로).\n\n"
        "[금지] 이 워크스페이스(대상 프로젝트 루트) 밖의 어떤 파일도 생성·수정하지 마라. 보호 경계"
        "(.claude/·install-manifest.md·specs/·framework/)를 생성·수정·삭제하지 마라. 너의 이번 "
        "산출은 오직 " + IMPL_PLAN_FILE + " 한 파일뿐이다(구현 코드는 이후 revision task 가 작성). "
        "입력 3개 문서는 읽기 전용이다.\n\n"
        "[CP1 자체 점검] Execute 종료 시 done 의 AC 커맨드를 실제로 실행하여(CP1 자체 점검) 종료 "
        "코드 0 을 확인한 뒤에만 완료 보고를 내라. 완료 보고 artifacts 에 " + IMPL_PLAN_FILE
        + " 경로를 실어라."
    )


def implplan_task():
    """impl-plan 단위 — 실 LLM 이 설계 artifact 를 소비해 구현 task 3~6개를 JSON 으로 제안한다.

    user_decision 게이트 대상(unitType=proposal·정지). dependsOn=[] — run 의 유일한 초기
    단위이며, 이 단위 Pass 뒤 사용자 구조 게이트(user_decision)가 물리 정지시킨다. 산출
    impl-plan.json 은 resolve_w 가 validate_impl_plan 으로 검증 후 구현 task 전체를 task_added
    revision 으로 승격하는 **실 LLM 산출 artifact**다(드라이버 픽스처 아님·OQ-PO-B4 완전 해소).

    모델은 sonnet — JSON 스키마 준수 신뢰성·설계 소비의 추론 부담. 이 값은 정책 데이터 경계에만
    존재한다(PO-INV 8 무관).
    """
    ac = _implplan_ac()
    task = _implplan_prompt()
    deleg = _deleg(
        task,
        "pc-uahf-control-plane-001 v2(읽기 전용) + reconciling/reviewing-record.md(읽기 전용) "
        "+ 실 프로젝트 워크스페이스(uahf-control-plane)",
        IMPL_PLAN_FILE,
        ac,
        ["Project Orchestration (w) — MVP 구현 orchestration run(OQ-PO-B4 완전 해소·"
         "project-orchestration-binding.md:201)",
         "성숙 산출 설계 artifact(maturation-r003 통합 아키텍처)를 실 LLM 이 소비해 구현 task 제안",
         "대상 Contract v2·설계 문서는 읽기 전용 참조(수정 금지)",
         "보호 경계(.claude/·install-manifest.md·specs/·framework/)는 UAHF Scaffold·Contract — 무수정",
         "impl-plan.json 은 사용자 구조 게이트 해소 후 resolve_w 가 검증·일괄 승격한다"],
    )
    return {
        "id": "impl-plan",
        "task": task,
        "done": ac,
        "interfaceContract": {
            "produces": [IMPL_PLAN_FILE],
            "consumes": [CONTRACT_V2_PATH, RECONCILING_PATH, REVIEWING_PATH],
        },
        "ownedBoundary": [IMPL_PLAN_FILE],
        "dependsOn": [],
        "delegation": deleg,
        "capability": "cap-impl-plan",
        "role": "Worker",
        "model": SONNET,
        "unitType": "proposal",   # 게이트 descriptor(정책 매칭용·개방 데이터).
    }


def initial_graph():
    return {
        "goal": "uahf-control-plane MVP 대시보드 구현 orchestration(설계 소비→구현 task 제안→"
                "게이트→구현·OQ-PO-B4 완전 해소)",
        "tasks": [implplan_task()],
        "completion": "all-passed",
    }


def gate_policy():
    """impl-plan(proposal) → user_decision(구조 게이트·정지) · 구현(implementation) → review(비정지).

    (m)과 달리 구현 단계 게이트는 review_required(비정지)이므로 사용자 게이트는 구조 게이트 1단만
    필요하다 — resolve_w 는 structure phase 만 갖는다(final 불필요).
    """
    return {
        "entries": [
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
        "timeout": 900,          # npm install·npm run build 감안(구현 step 은 장시간).
        "allowed_tools": ALLOWED_TOOLS,
        "output_format": "json",
        "workspace_dir": WORKSPACE_DIR,
        "note": (
            "MVP 구현 orchestration run — OQ-PO-B4 **완전 해소** 지점(project-orchestration-"
            "binding.md:201). 성숙 산출 설계 artifact(maturation-r003 통합 아키텍처)를 실 LLM 제안 "
            "step(impl-plan)이 소비해 구현 task 3~6개를 제안 → 사용자 구조 게이트 → resolve_w 가 "
            "검증·일괄 승격 → 구현 step 들이 실 CLI 로 uahf-control-plane 에 Next.js MVP 를 구현. "
            "구현 게이트는 review_required(비정지) — 사용자 게이트는 구조 게이트 1단만. "
            "workspace_dir = 실 소비 프로젝트(uahf-control-plane·UAHF 저장소 밖·독립 git). **주의**: "
            "setup 은 이 워크스페이스를 삭제·초기화하지 않는다(실 프로젝트 보존). 보호 경계"
            "(.claude/·install-manifest.md·specs/·framework/)는 UAHF Scaffold·Contract — 무수정. "
            "산출 내용 비고정(실 LLM 산출)·구조 게이트는 실 사용자가 해소(시뮬레이션 0·resolve_w)."
        ),
    }
