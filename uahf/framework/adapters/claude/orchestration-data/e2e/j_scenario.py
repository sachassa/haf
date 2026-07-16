"""시나리오 (j) — 축소판 종단 흐름 정본 스펙 (설계 §5 S5 · 바인딩 §5).

흐름: 초기 그래프 = 설계 단위(d1·user_decision 게이트) → [물리 정지 exit 2] →
드라이버가 사용자 actor 해소(시뮬레이션·라벨) + 구현 단위 제안 revision → 구현 step(impl·
review 게이트) → 완주. 완주 후 상류 재실행 흔적 0·deterministic resume replay 검증.

모델 슬롯: 전부 haiku(저비용·소형 태스크·v1.5 E2E 선례). 이 값은 E2E 드라이버·정책 데이터
경계에만 존재한다(중립 코드 아님·격리 지점·PO-INV 8 무관).

산출 내용은 CP2 재현성을 위해 **정확 내용**으로 고정한다(설계 메모를 exact-content 설계
결정 레코드로 축약 — 정직 표기). 이는 실 CLI 판정의 흔들림을 줄이기 위한 픽스처 선택이다.
"""

from __future__ import annotations

RUN_ID = "orch-j-e2e"
HAIKU = "haiku"
ALLOWED_TOOLS = ["Write", "Read", "Edit", "Bash(python:*)"]

# --- 산출물 정확 내용(후행 개행 없이) ------------------------------------------
D1_FILE = "design-decision.md"
D1_CONTENT = "DESIGN-DECISION: append-only-ledger"
IMPL_FILE = "impl-note.txt"
IMPL_CONTENT = "IMPL: ledger.append(record)"


def _content_ac(fname: str, content: str) -> str:
    """실행형 AC — 파일 내용 정확 일치(종료 코드 0 = 통과). step-data 선례 동형."""
    return ("python -c \"import io;d=io.open(%r,encoding='utf-8').read();"
            "assert d==%r,repr(d)\" (종료 코드 0 = 통과)" % (fname, content))


def _deleg(task, input_, output_, done, context):
    return {
        "from": "Advisor", "to": "Worker", "task": task,
        "input": input_, "output": output_, "done": done,
        "context": context, "constraints": "워크스페이스 밖 파일 생성·수정 금지",
    }


def design_task():
    """설계 단위 d1 — user_decision 게이트 대상(unitType=design_maturation)."""
    ac = _content_ac(D1_FILE, D1_CONTENT)
    task = (
        "현재 작업 디렉터리(이 워크스페이스)에 %s 파일을 생성하라. 내용은 정확히\n"
        "%s\n"
        "이며 후행 개행을 붙이지 마라. 이 워크스페이스 밖의 어떤 파일도 생성·수정하지 마라. "
        "Execute 종료 시 done 의 AC 커맨드를 실제로 실행하여(CP1 자체 점검) 종료 코드 0 을 "
        "확인한 뒤에만 완료 보고를 내라. 완료 보고 artifacts 에 %s 경로를 실어라."
        % (D1_FILE, D1_CONTENT, D1_FILE)
    )
    deleg = _deleg(task, "빈 워크스페이스(설계 착수)", D1_FILE, ac,
                   ["Project Orchestration S5 E2E (j) — 설계 단위·user_decision 게이트",
                    "상위 Contract 는 읽기 전용 참조(재실행 금지)"])
    return {
        "id": "d1",
        "task": task,
        "done": ac,
        "interfaceContract": {"produces": [D1_FILE], "content": D1_CONTENT},
        "ownedBoundary": [D1_FILE],
        "dependsOn": [],
        "delegation": deleg,
        "capability": "cap-design",
        "role": "Worker",
        "model": HAIKU,
        "unitType": "design_maturation",   # 게이트 descriptor(정책 매칭용·07 개방 데이터).
    }


def impl_revision_payload():
    """구현 단위 impl — 설계 Passed·게이트 해소 후 드라이버가 제안하는 task_added payload.

    review 게이트 대상(unitType=implementation). dependsOn=[d1] — 설계 완료 후 착수(07 R2 —
    미래 task 선참조 금지의 인과 사슬 준수: 설계 Passed → 게이트 → revision append).
    interfaceContract.consumes = [design-decision.md] (derivedFrom 실측치).
    """
    ac = _content_ac(IMPL_FILE, IMPL_CONTENT)
    task = (
        "input 이 가리키는 설계 결정 %s 를 읽고(그 결정에 따라), 현재 워크스페이스에 %s 파일을 "
        "생성하라. 내용은 정확히\n%s\n이며 후행 개행을 붙이지 마라. 워크스페이스 밖 파일 금지. "
        "CP1 에서 done 의 AC 를 실제 실행해 확인하라. 완료 보고 artifacts 에 %s 경로를 실어라."
        % (D1_FILE, IMPL_FILE, IMPL_CONTENT, IMPL_FILE)
    )
    deleg = _deleg(task, "%s (설계 결정 — impl 값의 원천)" % D1_FILE, IMPL_FILE, ac,
                   ["Project Orchestration S5 E2E (j) — 구현 단위·review 게이트"])
    return {
        "id": "impl",
        "task": task,
        "done": ac,
        "interfaceContract": {"produces": [IMPL_FILE], "consumes": [D1_FILE],
                              "content": IMPL_CONTENT},
        "ownedBoundary": [IMPL_FILE],
        "dependsOn": ["d1"],
        "delegation": deleg,
        "capability": "cap-impl",
        "role": "Worker",
        "model": HAIKU,
        "unitType": "implementation",
    }


def initial_graph():
    return {"goal": "설계→구현 축소판 종단 흐름", "tasks": [design_task()],
            "completion": "all-passed"}


def gate_policy():
    """설계 단위 → user_decision_required(정지·사용자 확정) · 구현 단위 → review_required."""
    return {
        "entries": [
            {"target": {"unitType": "design_maturation"}, "gate": "user_decision_required"},
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
        "note": "비프로덕션 dogfooding E2E — Project Orchestration S5 시나리오 (j).",
    }
