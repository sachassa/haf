"""Contract vN → 초기 Work Graph 결정적 컴파일러 (F4 — 배선 수정 Wave 1).

이 모듈은 확정된 Project Contract(project-contract.v*.md) 를 오케스트레이션 엔진이
초기 그래프로 소비할 **순수 데이터**(config / graph / gate_policy 3종 dict)로 컴파일한다.
결정적이며 LLM 0·판단 0·디스크 쓰기 0 이다 — 실제 Phase 분해는 런타임 실 LLM(seed
proposal step)이 담당한다(05 §3.1 "고정 파이프라인 하드코딩 금지"). F4 는 그 seed 방출
까지의 **결정적** 부분만 소유한다.

소유 경계(무엇을 하지 않는가):
  - 디스크에 쓰지 않는다(compile 은 dict 만 반환 — Wave 2 러너가 물리화·구동 소관).
  - orchestration/framework/** · uahf/** 를 수정하지 않는다(import 도 하지 않는다 —
    이 모듈은 stdlib only 순수 데이터 생성기다). Step/GatePolicy 스키마는 그 코드가
    소비 가능한 형태로 **재현**될 뿐이며, 정합은 테스트가 실제 코드로 검증한다.
  - Contract 내용을 파싱·해석하지 않는다(resolve 는 파일명 버전만 본다). 실제 요구
    분해는 seed 프롬프트가 런타임 LLM 에 위임한다.

스키마 정본(재현 대상·무수정 재사용):
  - Work Graph = uahf/specs/07-workflow.md §3.2-A {goal, tasks, dependencies, completion}.
  - Task/Step 필드 = uahf/framework/loop/step-host/step.py Step(from_dict·missing_fields).
  - gate_policy 데이터 = orchestration/framework/orchestrator/gates.py GatePolicy.from_dict.
  - config 키 = build_orchestrator(_orch_common.py / k_common.py) 가 읽는 실제 키.

오프라인 안전(핵심 불변): seed 노드의 done AC 및 프롬프트가 요구하는 하위 task done AC 는
파일 존재 · `python -c` 구조 assert · `node --check <file>.ts`(Node 24 타입 스트립 문법검사)
만 사용한다. npm / npx / tsc / `npm run build` 는 오프라인 불가이므로 금지한다.

일반화(2026-07-19): 프로젝트 표기·버전·seed id·run_id·경계 문구를 소비 프로젝트에서 파생하도록
전환해 임의 Contract 소비 프로젝트에서 동작한다(전신 = tms-system 도메인 하드코딩 실측·binding
§5.7 앵커). 도메인·계층·설계 결정 하드코딩 0 — 반영할 앵커는 런타임 LLM 이 입력 문서에서 식별한다.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
from typing import Any


# ==========================================================================
# 상수 — 정책 데이터 경계 값(중립 코드 아님·adapter 경계이므로 model 슬롯 허용)
# ==========================================================================
DEFAULT_MODEL = "sonnet"

# 오프라인 안전 allowed_tools — npm/npx 부재(설치 불가). node 는 `node --check` 문법검사용,
# python 은 CP1 자체 점검 AC(python -c 구조 assert) 실행용.
DEFAULT_ALLOWED_TOOLS = [
    "Write", "Read", "Edit", "Glob", "Grep",
    "Bash(node:*)", "Bash(python:*)",
]

# 초. seed 는 설계 소비·계획 방출만 하지만 여유 확보.
# 900 → 2400 상향(2026-07-25 · 사용자 확정). `uaf-verified:` 근거 = 원장 실측으로
# 900 초 초과가 반복 확인됐다 — cheongryong-bubble `impl-s14-15-ui-sound` 가 같은
# 단위에서 3회 연속(retry 0·1·2 소진 → Escalated) · `impl-s16-18-final` 1회 ·
# `impl-s04-08-core` 1회 · yt-stt `impl-yt-stt-m4afix2` 1회. **검색 범위** =
# 이 저장소의 `DEFAULT_TIMEOUT`·`timeout=900` ripgrep 스윕 + 적중 run 의
# events.jsonl 판독. Escalated 는 해소 채널이 없어(백로그 J — `escalated` 이벤트에
# gate_id 부재 · stop-signal 미생성) 상한 초과가 곧 run 폐기이므로 상한 자체를 올린다.
DEFAULT_TIMEOUT = 2400

IMPL_PLAN_FILE = "impl-plan.json"

# 하위 구현 task 개수 범위(seed 프롬프트가 요구·seed done AC 가 검사). 3~6개.
_MIN_TASKS = 3
_MAX_TASKS = 6


# ==========================================================================
# 순수 파생 헬퍼 — seed id·슬러그(내용 파싱 0·부작용 0·소비 프로젝트 중립)
# ==========================================================================
# 슬러그 길이 상한(백로그 §P·§L Desired 4-b — 공통 규칙). seed 단위 id 가 그대로
# `steps/<unitId>.json`·`logs/invoke-NN-<Role>-<unitId>.json` 파일명이 되므로 상한이 없으면
# (a) Windows 경로 한계 `OSError: [Errno 22]` 크래시(§P 실측)·(b) git `Filename too long` 로
# **run 원장을 커밋할 수 없다**(§L 4-b 실측 · 파일명 239자·경로 367자). 접는 규칙은
# 결정적이며 48자 이하 입력에는 **바이트 동일**(기존 run 디렉터리·id 하위호환).
SLUG_MAX_LEN = 48
SLUG_HASH_LEN = 8


def fold_slug(normalized: str, raw: Any) -> str:
    """정규화된 슬러그가 상한을 넘으면 `앞 48자 + "-" + sha256(원문)[:8]` 로 접는다.

    - `normalized` = 각 호출자의 정규화 규칙을 이미 통과한 문자열(규칙은 호출자 소유).
    - `raw` = **정규화 전 원 입력**. 해시를 원문에서 뽑아야 정규화가 같은 값으로 뭉갠
      서로 다른 입력(예: 대소문자·구분자만 다른 phase)이 구분된다.
    - 결정적(같은 입력 → 같은 값)·순수(부작용 0). 결과 길이 상한 = 48+1+8 = 57.
    - 48자 이하는 **그대로 반환**(바이트 동일) — 기존 run_id·unit id 하위호환.
    """
    if len(normalized) <= SLUG_MAX_LEN:
        return normalized
    digest = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()[:SLUG_HASH_LEN]
    return normalized[:SLUG_MAX_LEN] + "-" + digest


def _slug(text: str) -> str:
    """자유 텍스트를 안전 슬러그로 정규화한다(소문자·비영숫자→'-'·연속 축약·양끝 제거).

    빈 결과는 "run" 으로 폴백한다. 순수 함수(부작용 0). 예: "Phase 1"→"phase-1",
    "정산 코어"→"run"(비ASCII 영숫자는 '-' 로 흡수되어 폴백).

    길이 상한(`fold_slug`·48자)을 적용한다 — 긴 ASCII phase 에서 파일명·경로 한계로
    크래시하거나 원장 커밋이 막히는 결함(백로그 §P·§L 4-b)의 해소다.
    """
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return fold_slug(s or "run", text)


def seed_task_id(phase_scope: str) -> str:
    """seed proposal 노드 id 를 phase_scope 에서 파생한다("impl-plan-" + _slug).

    phase_scope="phase1" → "impl-plan-phase1"(전신 하드코딩 값과 파생적으로 일치).
    """
    return "impl-plan-" + _slug(phase_scope)


# ==========================================================================
# 1. Contract 해소 — 파일명 버전 기준 최대 인스턴스 선택(내용 파싱 0·판단 0)
# ==========================================================================
_CONTRACT_GLOB = "project-contract.v*.md"
_VERSION_RE = re.compile(r"project-contract\.v(\d+)\.md$")


def resolve_contract(project_root: Path) -> Path:
    """`<root>/.claude/project-contract/project-contract.v*.md` 중 **파일명 버전** 최대 선택.

    내용을 파싱하지 않는다 — 파일명의 v<정수>를 정수로 비교해 최대치를 고른다(v10 > v2 —
    사전식 아님·수치식). 후보가 없으면 FileNotFoundError. 반환은 절대경로(resolve).
    """
    root = Path(project_root)
    contract_dir = root / ".claude" / "project-contract"
    candidates: list[tuple[int, Path]] = []
    for p in contract_dir.glob(_CONTRACT_GLOB):
        m = _VERSION_RE.search(p.name)
        if m is None:
            continue  # 버전 없는 파일명은 후보에서 제외(판단 0 — 순수 필터).
        candidates.append((int(m.group(1)), p))
    if not candidates:
        raise FileNotFoundError(
            "project-contract.v*.md 를 찾을 수 없다: " + str(contract_dir)
        )
    # 버전 정수 최대. 동률(있을 수 없음·파일명 유일)은 경로 문자열로 안정 tie-break.
    best = max(candidates, key=lambda item: (item[0], str(item[1])))
    return best[1].resolve()


def contract_version(contract_path: Path) -> int:
    """해소된 Contract 파일명에서 버전 정수를 파생한다(_VERSION_RE 재사용·내용 파싱 0).

    파일명이 project-contract.v<N>.md 형태가 아니면 ValueError. resolve_contract 반환
    경로에 적용하는 것이 표준 용법(resolve_contract 가 이미 버전 있는 파일만 선택하므로
    정상 경로에선 항상 성립).
    """
    name = Path(contract_path).name
    m = _VERSION_RE.search(name)
    if m is None:
        raise ValueError("Contract 파일명에서 버전을 파생할 수 없다: " + name)
    return int(m.group(1))


# ==========================================================================
# 2. seed proposal 노드 + 초기 그래프
# ==========================================================================
def _done_ac() -> str:
    """seed 산출(impl-plan.json) 구조 검사 AC — **오프라인 안전**(python -c·파일 존재).

    impl-plan.json 존재 ∧ 파싱 ∧ tasks 가 3~6개 리스트 ∧ 각 task 가 11키 전부 보유 ∧
    unitType 이 {implementation, milestone} 집합에 속함 ∧ **milestone 최소 1건**(CP3
    approval 트리거 단위·phase 경계 승인) ∧ **implementation 최소 1건**. 종료 코드 0 = 통과.
    npm/tsc/build 불사용(오프라인).
    """
    return (
        "python -c \"import json,os;p='" + IMPL_PLAN_FILE + "';"
        "assert os.path.exists(p),p;"
        "d=json.load(open(p,encoding='utf-8'));t=d.get('tasks');"
        "assert isinstance(t,list) and " + str(_MIN_TASKS) + "<=len(t)<=" + str(_MAX_TASKS)
        + ",repr(len(t) if isinstance(t,list) else t);"
        "ks=['id','task','done','interfaceContract','ownedBoundary','dependsOn',"
        "'delegation','capability','role','model','unitType'];"
        "miss=[(x.get('id'),k) for x in t for k in ks if k not in x];"
        "assert not miss,miss;"
        "ut=[x.get('unitType') for x in t];"
        "assert set(ut)<={'implementation','milestone'},ut;"
        "assert ut.count('milestone')>=1,ut;"
        "assert ut.count('implementation')>=1,ut\" (종료 코드 0 = 통과)"
    )


def _seed_prompt(
    contract_path: Path,
    sd_path: Path,
    phase_scope: str,
    project_name: str,
    version: int,
) -> str:
    """seed proposal 단계 자족 프롬프트 — 설계 소비·구현 task 구성 규칙(오프라인 안전 AC 강제).

    이 단계는 코드를 직접 작성하지 않는다. Contract v<N> + solution-design.md 를 읽어(읽기 전용)
    분해 대상(phase_scope)을 3~6개 task(= implementation N개 + **milestone 정확히 1개**)로
    분해해 impl-plan.json 을 방출한다. **어떤 도메인·계층·설계 결정도 여기 하드코딩하지 않는다** —
    반영할 설계 앵커는 런타임 LLM 이 입력 설계 문서(Contract §6 결정 레코드·solution-design)에서
    스스로 식별·인용한다(05 §3.1 "고정 파이프라인 하드코딩 금지"). milestone 은 해당 phase 범위의
    인수/완결 판정 단위로 approval_required(CP3·Advisor 경계 승인)를 트리거한다.
    """
    cp = str(contract_path)
    sd = str(sd_path)
    vlabel = "v" + str(version)
    return (
        "너는 **" + project_name + "** 프로젝트의 **" + phase_scope + " 구현 계획 단계**"
        "(Project Orchestration 형태 B — impl-plan 제안 step)를 수행하는 실행 단위다. 대상 = "
        "확정 완결된 Project Contract(" + vlabel + ").\n\n"
        "[역할] 너는 코드를 직접 작성하지 않는다. 확정 설계를 소비해 **" + phase_scope + " 구현 task "
        "3~6개의 실행 계획**을 JSON 으로 산출한다. 각 구현 task 는 이후(사용자 게이트 승인 후) "
        "task_added revision 으로 편입되어 별도 fresh-context 세션이 실제 코드를 작성한다.\n\n"
        "[입력 정독 — 2개 문서·전부 읽기 전용 절대경로] 다음을 Read 도구로만 정독하라(생성·"
        "수정·삭제 금지):\n"
        "  ① Project Contract " + vlabel + " (구현 명세의 정본 — §6 architectureDirection 설계 "
        "결정 레코드):\n"
        "     " + cp + "\n"
        "  ② Solution Design (도메인 모델·계층 경계·인터페이스 계약의 정본):\n"
        "     " + sd + "\n\n"
        "[이번 분해 대상 = " + phase_scope + "] 그 범위와 반영할 설계 앵커를 **입력 문서에서 스스로 "
        "식별**하라 — Contract 의 architectureDirection(설계 결정 레코드)과 solution-design 의 확정 "
        "결정에서 " + phase_scope + " 에 해당하는 결정들을 찾아 **결정 식별자를 명시 인용**해 앵커로 "
        "삼아라. 설계 문서가 단계화(phasing)를 정의하면 그에 따르고, 없으면 " + phase_scope + " 를 "
        "전체 범위 라벨로 취급하라. **선언된 전 영역(백엔드·UI/UX 접점·인터페이스 등)을 계층 편향 "
        "없이 커버**하고, 특정 계층으로 좁히려면 그 근거가 되는 설계 결정을 인용하라.\n\n"
        "[산출 — " + IMPL_PLAN_FILE + "] 현재 작업 디렉터리(워크스페이스 = 대상 프로젝트 루트)에 "
        + IMPL_PLAN_FILE + " 을 산출하라. 최상위는 단일 객체이며 스키마는:\n"
        "  { \"tasks\": [ <task dict 3~6개> ] }\n"
        "각 task dict 는 **11키 스키마**를 모두 가진다: id·task·done·interfaceContract·"
        "ownedBoundary·dependsOn·delegation·capability·role·model·unitType.\n\n"
        "[단위 구성 — 필수 배합] 총 3~6개 task 중:\n"
        "  - **대부분은 unitType = \"implementation\"** (최소 1개·phase 범위 구현 단위).\n"
        "  - **정확히 1개는 unitType = \"milestone\"** — 해당 phase 범위의 **인수/완결 판정 "
        "단위**다(phase 경계 승인 — 선행 구현 산출의 정합·완결을 판정). 이 milestone "
        "단위는 **approval_required(CP3·Advisor 경계 승인) 게이트를 트리거**하며, 모든(또는 종단) "
        "implementation 단위에 `dependsOn` 으로 의존하는 **DAG 의 마지막 경계 노드**여야 한다"
        "(다른 단위가 이 milestone 에 의존하지 않는다). milestone 단위도 코드를 직접 작성하지 "
        "않고 선행 구현 산출의 정합/완결을 오프라인 안전 AC(python -c 구조 assert·파일 존재·"
        "node --check)로 판정하되, ownedBoundary 는 비어있지 않게(예: 인수 판정 스크립트·"
        "인수 기록 파일 등 이 단위가 소유하는 상대경로) 두어라.\n\n"
        "[구현 task 구성 규칙]\n"
        "  - unitType = \"implementation\" 또는 (마지막 1개) \"milestone\" — 위 배합 준수.\n"
        "  - role = \"Worker\", model = \"" + DEFAULT_MODEL + "\" (전부).\n"
        "  - id = 고유 슬러그(케밥 케이스). 계획 내 유일(중복 금지).\n"
        "  - dependsOn = **계획 내 다른 task id 만** 참조하는 배열(DAG — 자기참조·사이클 금지). "
        "선행 산출에 의존하면 그 task id 를 넣어라(예: 핵심 로직 task 는 도메인 모델 task 에 의존).\n"
        "  - ownedBoundary = 이 task 가 생성/수정하는 파일·디렉터리의 **상대경로 배열**(대상 "
        "프로젝트 루트 기준·비어있지 않게). **task 간 상호 비중첩**(한 경로가 다른 task 경로의 "
        "조상/자손이면 안 됨 — 병렬 실행 대비). 보호 경계(아래) 항목 금지·절대경로/`..` 금지.\n"
        "  - interfaceContract = {\"produces\":[<산출 파일/디렉터리>], \"consumes\":[<선행 task "
        "산출 또는 설계 문서>]}.\n"
        "  - task = **fresh-context 자족 지시문** — 구현 파일 경로·내용 요건·근거가 되는 설계 결정 "
        "인용(설계 결정 식별자 — Contract §6 결정 레코드 또는 solution-design 절 번호)·워크스페이스 "
        "밖 파일 금지·보호 경계 무수정·Execute 종료 시 CP1 자체 점검(done AC 실행) 지시를 모두 "
        "포함한다.\n"
        "  - done = **단일 셸 커맨드 실행형 AC**(종료 코드 0 = 통과)이되 **오프라인 안전 검사만** "
        "사용한다 — 다음 중 하나 이상만 허용된다:\n"
        "      · 파일 존재 검사(python -c \"import os;assert os.path.exists('<경로>')\"),\n"
        "      · `python -c` 구조 assert(JSON/텍스트 구조 검증),\n"
        "      · `node --check <파일>.ts`(스택 해당 시 — Node 24 타입 스트립 문법검사·단일 파일).\n"
        "    **금지: npm install · npx · tsc · `npm run build` · 네트워크 접근**(오프라인 환경 — "
        "설치·전체 빌드는 실행 불가). 해당 task 산출만 검사하고 비공백이어야 한다.\n"
        "  - capability = 임의 슬러그(예: \"cap-impl-core\"). role/model 슬롯과 함께 채운다.\n"
        "  - timeout = **선택 키**(11키 밖·생략 가능) — 이 단위 실행 예산의 **초 단위 양의 "
        "정수**(예: 5400). 명백히 대형인 단위에만 지정하고, 근거 없이 값을 발명하지 마라. "
        "미지정이면 전역 기본 예산이 적용된다(권장 = 대부분 미지정).\n"
        "  - delegation = 8필드(from=\"Advisor\"·to=\"Worker\"·task=\"위 task 필드와 동일\""
        "(참조형 sentinel)·input·output=산출 파일·done=\"위 done 필드와 동일\"(참조형 sentinel)·"
        "context·constraints=\"워크스페이스(" + project_name + ") 밖 파일 생성·수정 금지, 보호 경계"
        "(.claude/·docs/solution-design.md) 읽기 전용\"). delegation.task/done 은 상위 task/done "
        "전문을 다시 쓰지 말고 위 sentinel 문면을 그대로 넣어라(참조형 표준·토큰 절약). 상위 "
        "task/done 원문을 바이트 동일하게 전재하는 것도 허용된다 — 둘 중 하나면 된다.\n\n"
        "[보호 경계 — 절대 수정 금지] 다음은 읽기 전용이다. 어느 구현 task 의 ownedBoundary 에도 "
        "넣지 말고 task 문면에도 수정 금지를 명시하라:\n"
        "  - .claude/**  (Scaffold·Contract·AGENT.md·agents)\n"
        "  - docs/solution-design.md\n"
        "구현 산출은 앱 소스 파일(프로젝트 스택의 소스·설정 파일 — 예: src/ 등)로 한정한다. "
        "**오프라인이므로 npm install 산출(node_modules)에 의존하는 done AC 를 두지 마라.**\n\n"
        "[금지] 이 워크스페이스(" + project_name + " 루트) 밖의 어떤 파일도 생성·수정하지 마라. "
        "입력 2개 문서는 읽기 전용이다. 너의 이번 산출은 오직 " + IMPL_PLAN_FILE + " 한 파일뿐이다"
        "(구현 코드는 이후 revision task 가 작성).\n\n"
        "[CP1 자체 점검] Execute 종료 시 done 의 AC 커맨드를 실제로 실행하여(CP1 자체 점검) 종료 "
        "코드 0 을 확인한 뒤에만 완료 보고를 내라. 완료 보고 artifacts 에 " + IMPL_PLAN_FILE
        + " 경로를 실어라."
    )


def _solution_design_path(project_root: Path) -> Path:
    """대상 프로젝트의 solution-design.md 절대경로(읽기 전용 참조·seed 프롬프트 인용용)."""
    return (Path(project_root) / "docs" / "solution-design.md").resolve()


def build_seed_graph(
    contract_path: Path,
    project_root: Path,
    *,
    mode: str,
    phase_scope: str,
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """{goal, tasks:[<단일 proposal 노드>], dependencies:[], completion} 초기 그래프.

    단일 proposal 노드는 런타임 실 LLM 이 Contract v<N> + solution-design 을 소비해 분해 대상
    (phase_scope)을 구현 task 3~6개로 분해하도록 지시한다(결정적 부분은 seed 방출까지). 노드는
    step.py Step 의 from_dict + missing_fields 검증을 누락 0 으로 통과하도록 필수 필드(done·
    interfaceContract·delegation.input/output/done/context·id)를 모두 채운다.

    프로젝트 표기·버전은 소비 프로젝트에서 파생한다(내용 파싱 0): project 표기 = 워크스페이스
    루트 폴더명, Contract 버전 = 해소된 파일명(contract_version). seed 노드 id 도 phase_scope
    에서 파생한다(seed_task_id). mode·phase_scope 는 goal·프롬프트 문면에 반영되는 개방
    데이터다(엔진 판단 대상 아님).

    seed proposal 노드의 role=Planner 다 — 이 스텝의 실제 일 = 확정 설계 소비→구현 task 실행
    계획(impl-plan) 산출 = 작업 분해 초안 = Planner Lifecycle capability(05 §3.4·§DC-7). 이
    스텝이 생성하는 impl 자식 task 는 실행 단위이므로 seed 프롬프트 내 role=Worker 로 유지된다.
    """
    contract_path = Path(contract_path).resolve()
    root = Path(project_root).resolve()
    project_name = root.name
    version = contract_version(contract_path)
    sd_path = _solution_design_path(project_root)
    done_ac = _done_ac()
    prompt = _seed_prompt(contract_path, sd_path, phase_scope, project_name, version)

    constraints = (
        "워크스페이스(" + project_name + ") 밖 파일 생성·수정 금지. "
        + project_name + "/.claude/** 및 docs/solution-design.md 는 읽기 전용 — 생성·수정·삭제 금지."
    )
    delegation = {
        "from": "Advisor",
        "to": "Planner",
        "task": prompt,
        "input": (
            "Project Contract v" + str(version) + "(읽기 전용·" + str(contract_path) + ") + "
            "Solution Design(읽기 전용·" + str(sd_path) + ")"
        ),
        "output": IMPL_PLAN_FILE,
        "done": done_ac,
        "context": [
            "Project Orchestration 형태 B — impl-plan 제안 step(초기 그래프 seed·05 §3.1)",
            "확정 Contract v" + str(version) + " 를 실 LLM 이 소비해 " + str(phase_scope)
            + " 구현 task 제안",
            "대상 Contract·solution-design.md 는 읽기 전용 참조(수정 금지)",
            "phase 범위·설계 앵커는 입력 설계 문서(Contract §6 결정 레코드·solution-design)에서 "
            "seed 가 식별·인용한다(프롬프트 지시·하드코딩 0)",
            "impl-plan.json 은 사용자 구조 게이트 해소 후 검증·일괄 승격(task_added revision)",
        ],
        "constraints": constraints,
    }

    seed_node = {
        "id": seed_task_id(phase_scope),
        "task": prompt,
        "done": done_ac,
        "interfaceContract": {
            "consumes": [str(contract_path)],
            "produces": [IMPL_PLAN_FILE],
        },
        "ownedBoundary": [IMPL_PLAN_FILE],
        "dependsOn": [],
        "delegation": delegation,
        "capability": "cap-impl-plan",
        # 이 proposal 스텝 = 분해 초안 = Planner Lifecycle capability(05 §3.4 2축 직교·§DC-7).
        # 반면 이 스텝이 생성하는 impl 자식 task 는 실행 단위이므로 seed 프롬프트 내 role=Worker 유지(불변).
        "role": "Planner",
        "model": model,
        "unitType": "proposal",  # 게이트 descriptor(정책 매칭용·개방 데이터).
    }

    goal = (
        project_name + " 프로젝트(Contract v" + str(version) + ") " + str(phase_scope)
        + " 구현 orchestration(mode=" + str(mode) + " · 확정 설계 소비 → 구현 task 제안 → "
        "사용자 게이트 → 구현). phase 범위·설계 앵커는 입력 설계 문서에서 seed 가 식별·인용한다."
    )
    return {
        "goal": goal,
        "tasks": [seed_node],
        "dependencies": [],
        "completion": "all-passed",
    }


# ==========================================================================
# 3. gate_policy — GatePolicy.from_dict 소비 가능 형태(3 엔트리)
# ==========================================================================
def gate_policy() -> dict[str, Any]:
    """게이트 정책 데이터 — proposal→user_decision · implementation→review · milestone→approval.

    GatePolicy.from_dict(gates.py) 가 예외 없이 로드하는 스키마다: entries[{target,gate}] +
    userActorClass + escalationResolvers + gateRaiser. gate 값은 gateKind 5종 중 3종.
    """
    return {
        "entries": [
            {"target": {"unitType": "proposal"}, "gate": "user_decision_required"},
            {"target": {"unitType": "implementation"}, "gate": "review_required"},
            {"target": {"unitType": "milestone"}, "gate": "approval_required"},
        ],
        "userActorClass": "human",
        "escalationResolvers": ["Advisor", "human"],
        "gateRaiser": "Advisor",
    }


# ==========================================================================
# 4. config — build_orchestrator* 가 읽는 실제 키
# ==========================================================================
def build_config(
    run_id: str,
    workspace_dir: str,
    *,
    allowed_tools: list[str],
    timeout: int,
    policy: str = "interactive",
) -> dict[str, Any]:
    """오케스트레이터 config 데이터 — build_orchestrator(_orch_common/k_common) 소비 키 정합.

    읽히는 키(orchestrator.py 파라미터 경유): run_id · retry_limit · policy · timeout ·
    workspace_dir · allowed_tools · output_format. workspace_dir 는 run 디렉터리 밖 절대경로
    (build_orchestrator_k 가 workdir 로 배선). 순수 데이터 — 디스크 미기록.
    """
    return {
        "run_id": run_id,
        "policy": policy,
        "retry_limit": 2,
        "timeout": timeout,
        "allowed_tools": list(allowed_tools),
        "output_format": "json",
        "workspace_dir": workspace_dir,
    }


# ==========================================================================
# 5. compile — {config, graph, gate_policy} 순수 데이터(디스크 쓰기 0)
# ==========================================================================
def compile(
    project_root: Path,
    *,
    mode: str,
    phase_scope: str,
) -> dict[str, Any]:
    """Contract vN → 초기 Work Graph 3종 데이터로 컴파일한다(순수·디스크 미기록).

    반환 = {"config": {...}, "graph": {...}, "gate_policy": {...}}. 물리화(디스크 쓰기)·
    오케스트레이터 구동은 Wave 2 소관 — 이 함수는 dict 만 만든다(부작용 0).
    """
    root = Path(project_root).resolve()
    contract_path = resolve_contract(root)
    graph = build_seed_graph(
        contract_path, root, mode=mode, phase_scope=phase_scope
    )
    gp = gate_policy()
    # run_id = 소비 프로젝트 표기(워크스페이스 루트 폴더명) + phase_scope 파생(raw — 슬러그
    # 정규화는 런처 slugify_run_id 소관·분업 불변). 도메인 하드코딩 0.
    run_id = "orch-" + root.name + "-" + str(phase_scope)
    config = build_config(
        run_id,
        str(root),
        allowed_tools=DEFAULT_ALLOWED_TOOLS,
        timeout=DEFAULT_TIMEOUT,
    )
    return {"config": config, "graph": graph, "gate_policy": gp}
