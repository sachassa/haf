"""W3 E2E — 7 시나리오 정본 스펙 (Advisor 확정 run-id·설계).

각 시나리오는 run 데이터 백엔드에 물리화된다: config.json(run 파라미터·메타)·
steps/<id>.json(Step 직렬화·바인딩 §3.1 JSON). setup_run.py 가 이 스펙을 파일로 쓴다.

모델 슬롯: Worker/Verifier=haiku(비용·속도), s6 Worker=sonnet(코드 편집 품질),
CP3 Advisor=sonnet. policy 기본 auto_approve, s5 만 unrestricted.
"""

from __future__ import annotations


def _content_ac(fname: str, content: str) -> str:
    """실행형 AC — 파일 내용 정확 일치 검사(종료 코드 0 = 통과)."""
    return ("python -c \"import io;d=io.open(%r,encoding='utf-8').read();"
            "assert d==%r,repr(d)\"" % (fname, content))


def _both_ac(f1: str, c1: str, f2: str, c2: str) -> str:
    return ("python -c \"import io;a=io.open(%r,encoding='utf-8').read();"
            "b=io.open(%r,encoding='utf-8').read();assert a==%r and b==%r,"
            "(repr(a),repr(b))\"" % (f1, f2, c1, c2))


def _deleg(task, input_, output_, done, context, constraints=None):
    return {
        "from": "Advisor", "to": "Worker", "task": task,
        "input": input_, "output": output_, "done": done,
        "context": context, "constraints": constraints,
    }


def _step(sid, task, done, ifc, owned, depends, deleg, model, role="Worker", cap="impl"):
    return {
        "id": sid, "task": task, "done": done, "interfaceContract": ifc,
        "ownedBoundary": owned, "dependsOn": depends, "delegation": deleg,
        "role": role, "capability": cap, "model": model,
    }


HAIKU = "haiku"
SONNET = "sonnet"
DEFAULT_TOOLS = ["Bash(python:*)", "Read", "Write", "Edit"]


def s1():
    ac = _content_ac("greeting.txt", "UAHF-E2E-S1") + " (종료 코드 0 = 통과)"
    task = (
        "현재 작업 디렉터리(이 워크스페이스)에 greeting.txt 파일을 생성하라. 내용은 "
        "정확히 UAHF-E2E-S1 이며 후행 개행을 붙이지 마라(총 11바이트). 이 워크스페이스 "
        "밖의 어떤 파일도 생성·수정하지 마라. Execute 종료 시 done 의 AC 커맨드를 실제로 "
        "실행하여(CP1 자체 점검) 종료 코드 0 을 확인한 뒤에만 완료 보고를 내라."
    )
    deleg = _deleg(task, "빈 워크스페이스(신규 생성)", "greeting.txt (내용 UAHF-E2E-S1)",
                   ac, ["형태 B Step Hosting W3 E2E s1 — 정상 완주 + CP3 물리 형태 실증"],
                   "워크스페이스 밖 파일 생성·수정 금지")
    return {
        "run_id": "e2e-s1-normal", "policy": "auto_approve", "retry_limit": 2,
        "timeout": 300, "allowed_tools": DEFAULT_TOOLS, "workspace_mode": "subdir",
        "cp3": {"enabled": True, "model": SONNET},
        "step_order": ["s1"],
        "steps": {"s1": _step("s1", task, ac, {"produces": ["greeting.txt"],
                  "content": "UAHF-E2E-S1"}, ["greeting.txt"], [], deleg, HAIKU)},
    }


def s2():
    ac = _both_ac("part1.txt", "P1", "part2.txt", "P2") + " (종료 코드 0 = 통과)"
    task = (
        "번들의 feedback 필드를 먼저 확인하라.\n"
        "(1) feedback 이 null 이면 첫 실행이다: part1.txt(내용 정확히 P1)만 만들고 "
        "part2.txt 등 다른 파일은 절대 만들지 마라. 이어서 done 의 AC 를 실행하면 "
        "part2.txt 부재로 실패한다 — 추측으로 part2 를 만들지 말고 실패 보고를 "
        "blocking='계속 가능' 으로 제출하라(reason: part2.txt=P2 가 필요하나 첫 실행 "
        "지시상 만들 수 없음, repro: AC 실행 결과).\n"
        "(2) feedback 이 있으면 재시도다: feedback 의 지시대로 부족분 part2.txt(내용 정확히 "
        "P2)를 마저 만들어 AC 를 통과시킨 뒤 완료 보고를 내라. feedback 지시는 task 문면에 "
        "우선한다. 워크스페이스 밖 파일은 금지."
    )
    deleg = _deleg(task, "빈 워크스페이스(신규)", "part1.txt(P1) + part2.txt(P2)", ac,
                   ["형태 B W3 E2E s2 — 실패→feedback 재주입→fresh 재실행"],
                   "워크스페이스 밖 금지·첫 실행엔 part1.txt 만")
    return {
        "run_id": "e2e-s2-retry", "policy": "auto_approve", "retry_limit": 2,
        "timeout": 300, "allowed_tools": DEFAULT_TOOLS, "workspace_mode": "subdir",
        "cp3": {"enabled": False},
        "step_order": ["s2r"],
        "steps": {"s2r": _step("s2r", task, ac, {"produces": ["part1.txt", "part2.txt"]},
                  ["part1.txt", "part2.txt"], [], deleg, HAIKU)},
    }


def s3():
    task = (
        "input 이 가리키는 사양 파일 spec-s3.txt 를 읽고, 그 내용 그대로 answer.txt 를 "
        "생성하라. 만약 spec-s3.txt 가 존재하지 않으면 O4(추측 금지)에 따라 값을 절대 "
        "추측하지 마라 — answer.txt 를 만들지 말고, 실패 보고를 blocking='차단됨' 으로 "
        "제출하라. reason 에 무엇이 필요한지(사양 파일 spec-s3.txt 제공)를 scoped question "
        "으로 명확히 적어라. 이것이 차단 선언이다."
    )
    done = "answer.txt 의 내용이 spec-s3.txt 의 값과 일치. (spec-s3.txt 부재 시 착수 불가)"
    deleg = _deleg(task, "spec-s3.txt (이 워크스페이스의 사양 파일 — answer.txt 값의 원천)",
                   "answer.txt", done,
                   ["형태 B W3 E2E s3 — blocked→정지 신호→Advisor 해소 대기"],
                   "값 추측 금지(O4)·워크스페이스 밖 금지")
    return {
        "run_id": "e2e-s3-blocked", "policy": "auto_approve", "retry_limit": 2,
        "timeout": 300, "allowed_tools": DEFAULT_TOOLS, "workspace_mode": "subdir",
        "cp3": {"enabled": False},
        "step_order": ["s3b"],
        "steps": {"s3b": _step("s3b", task, done, {"produces": ["answer.txt"],
                  "depends_input": "spec-s3.txt"}, ["answer.txt"], [], deleg, HAIKU)},
    }


def _mkfile_step(sid, fname, content, depends):
    ac = _content_ac(fname, content) + " (종료 코드 0 = 통과)"
    task = ("현재 워크스페이스에 %s 파일을 생성하라. 내용은 정확히 %s (후행 개행 없이). "
            "워크스페이스 밖 파일 금지. CP1 에서 done 의 AC 를 실제 실행해 확인하라."
            % (fname, content))
    deleg = _deleg(task, "빈 워크스페이스", fname, ac,
                   ["형태 B W3 E2E s4 — 강제 중단→deterministic resume"],
                   "워크스페이스 밖 금지")
    return _step(sid, task, ac, {"produces": [fname], "content": content},
                 [fname], depends, deleg, HAIKU)


def s4():
    return {
        "run_id": "e2e-s4-resume", "policy": "auto_approve", "retry_limit": 2,
        "timeout": 300, "allowed_tools": DEFAULT_TOOLS, "workspace_mode": "subdir",
        "cp3": {"enabled": False},
        "step_order": ["A", "B", "C"],
        "steps": {
            "A": _mkfile_step("A", "fileA.txt", "A", []),
            "B": _mkfile_step("B", "fileB.txt", "B", ["A"]),
            "C": _mkfile_step("C", "fileC.txt", "C", ["B"]),
        },
    }


def s5():
    ac_ok = _content_ac("s5-ok.txt", "OK") + " (종료 코드 0 = 통과)"
    task_ok = ("현재 워크스페이스에 s5-ok.txt 파일을 생성하라. 내용은 정확히 OK (후행 개행 "
               "없이). 워크스페이스 밖 파일 금지. CP1 에서 done 의 AC 를 실제 실행해 확인하라.")
    deleg_ok = _deleg(task_ok, "빈 워크스페이스", "s5-ok.txt", ac_ok,
                      ["형태 B W3 E2E s5 — unrestricted 플래그 매핑 실증"],
                      "워크스페이스 밖 금지")
    task_blk = (
        "input 이 가리키는 사양 파일 spec-s5.txt 를 읽고 그 내용대로 s5-answer.txt 를 "
        "생성하라. spec-s5.txt 가 존재하지 않으면 O4(추측 금지)에 따라 값을 추측하지 말고 "
        "실패 보고를 blocking='차단됨' 으로 제출하라(reason 에 spec-s5.txt 필요를 명기). "
        "이것이 차단 선언이다. unrestricted policy 여도 추측하지 마라."
    )
    done_blk = "s5-answer.txt 가 spec-s5.txt 값과 일치. (spec-s5.txt 부재 시 착수 불가)"
    deleg_blk = _deleg(task_blk, "spec-s5.txt (부재 시 착수 불가)", "s5-answer.txt", done_blk,
                       ["형태 B W3 E2E s5 — unrestricted 에서도 게이트 보존"],
                       "값 추측 금지(O4)")
    return {
        "run_id": "e2e-s5-unrestricted", "policy": "unrestricted", "retry_limit": 2,
        "timeout": 300, "allowed_tools": None, "workspace_mode": "subdir",
        "cp3": {"enabled": False},
        "step_order": ["s5a", "s5b"],
        "steps": {
            "s5a": _step("s5a", task_ok, ac_ok, {"produces": ["s5-ok.txt"], "content": "OK"},
                         ["s5-ok.txt"], [], deleg_ok, HAIKU),
            "s5b": _step("s5b", task_blk, done_blk, {"produces": ["s5-answer.txt"],
                         "depends_input": "spec-s5.txt"}, ["s5-answer.txt"], ["s5a"],
                         deleg_blk, HAIKU),
        },
    }


def s6():
    target = "uahf/framework/adapters/claude/step-invoker/claude_invoker.py"
    testfile = "uahf/framework/adapters/claude/step-invoker/tests/test_claude_invoker.py"
    ac = ("AC1: `python %s` 가 전건 Pass(종료 코드 0). "
          "AC2: 같은 파일의 FileNotFoundError 분기가 더 이상 blocking='차단됨' 을 쓰지 "
          "않고 KIND_FAILURE(비차단 실패) 의미와 정합하는 비차단 값을 쓴다." % testfile)
    task = (
        "저장소 루트가 현재 작업 디렉터리다. Full UAF Mode 진입이다 — 상위 산출물(Contract "
        "pc-uahf-001 v2·설계)은 재사용하며 상위 Interview/Plan 을 재수행하지 마라.\n"
        "실제 작업: %s 의 invoke() 메서드 안 FileNotFoundError 분기(225행 부근)를 정정하라. "
        "그 분기는 kind=KIND_FAILURE(비차단 실패=재시도 대상)를 반환하는데 failure 딕셔너리의 "
        "'blocking' 값이 '차단됨'(=blocked=Escalated 의미)으로 되어 있어 내부 불일치다(확정 결함 "
        "O-1). blocking 값을 비차단 표기 '계속 가능' 으로 바꿔 KIND_FAILURE 의미와 정합시켜라.\n"
        "오직 이 한 파일의 이 한 곳만 수정하라. 테스트 파일·다른 파일·다른 로직을 절대 "
        "건드리지 마라. 수정 후 done 의 AC(테스트 전건 Pass)를 실제 실행해 확인한 뒤 완료 "
        "보고를 내라." % target
    )
    deleg = _deleg(task, "claude_invoker.py 확정 결함 O-1(FileNotFoundError 분기 blocking 라벨 불일치)",
                   "정정된 claude_invoker.py", ac,
                   ["형태 B W3 E2E s6 — Full UAF Mode(상위 재실행 0)",
                    "Contract: pc-uahf-001 v2 — discovery-data/contracts/uahf/project-contract.v2.md"],
                   "오직 claude_invoker.py 만 수정. 테스트/기타 파일 생성·수정 금지. 상위 재수행 금지.")
    return {
        "run_id": "e2e-s6-full-uaf", "policy": "auto_approve", "retry_limit": 2,
        "timeout": 300, "allowed_tools": ["Edit", "Read", "Grep", "Glob", "Bash(python:*)"],
        "workspace_mode": "repo_root",
        "entry_mode": "full-uaf",
        "contract_ref": "uahf/framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v2.md",
        "upstream_reuse": "상위 산출물 재사용·상위 Interview/Plan 재실행 금지(Full UAF Mode)",
        "cp3": {"enabled": False},
        "step_order": ["s6fix"],
        "steps": {"s6fix": _step("s6fix", task, ac, {"modifies": [target]}, [target], [],
                  deleg, SONNET)},
    }


def s7a():
    ac = _content_ac("s7a.txt", "S7A") + " (종료 코드 0 = 통과)"
    task = ("현재 워크스페이스에 s7a.txt 파일을 생성하라. 내용은 정확히 S7A (후행 개행 없이). "
            "워크스페이스 밖 파일 금지. CP1 에서 done 의 AC 를 실제 실행해 확인하라.")
    deleg = _deleg(task, "빈 워크스페이스(신규)", "s7a.txt", ac,
                   ["형태 B W3 E2E s7a — Standalone 충분 → 즉시 디스패치"],
                   "워크스페이스 밖 금지")
    return {
        "run_id": "e2e-s7a-sufficient", "policy": "auto_approve", "retry_limit": 2,
        "timeout": 300, "allowed_tools": DEFAULT_TOOLS, "workspace_mode": "subdir",
        "cp3": {"enabled": False},
        "step_order": ["s7a1"],
        "steps": {"s7a1": _step("s7a1", task, ac, {"produces": ["s7a.txt"], "content": "S7A"},
                  ["s7a.txt"], [], deleg, HAIKU)},
    }


def s7b():
    # done·context 누락 Step — 디스패치 금지(진입 Sufficiency 실패). delegation 에서
    # done·context 를 의도적으로 뺀다. task 레벨 done 도 뺀다.
    incomplete_deleg = {
        "from": "Advisor", "to": "Worker",
        "task": "무언가를 만들어라(불충분한 위임 — done·context 누락).",
        "input": "불명확한 입력", "output": "불명확한 출력",
        "constraints": None,
        # done·context 의도적 누락.
    }
    step = {
        "id": "s7b1",
        "task": "불충분한 Step — 진입 Sufficiency 판정에서 걸려야 한다.",
        # task-level done 의도적 누락.
        "interfaceContract": {"produces": ["something"]},
        "ownedBoundary": ["something"],
        "dependsOn": [],
        "delegation": incomplete_deleg,
        "role": "Worker", "capability": "impl", "model": HAIKU,
    }
    return {
        "run_id": "e2e-s7b-insufficient", "policy": "auto_approve", "retry_limit": 2,
        "timeout": 300, "allowed_tools": DEFAULT_TOOLS, "workspace_mode": "subdir",
        "cp3": {"enabled": False},
        "step_order": ["s7b1"],
        "steps": {"s7b1": step},
    }


ALL = {
    "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6,
    "s7a": s7a, "s7b": s7b,
}


def get(name):
    return ALL[name]()
