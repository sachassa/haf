#!/usr/bin/env python3
"""pretooluse_coverage_guard — 커버리지(축 4) "존재 최후방어" 백스톱(PreToolUse 차단 훅).

무엇을 하는가:
  Claude Code 세션이 **Project Contract 인스턴스 파일**을 Write/Edit/MultiEdit 하려 할 때, 그
  Contract 와 **같은 디렉터리**에 놓인 Coverage 원장(`coverage-ledger.json`)을 결정적 체커
  (`coverage_check.check_coverage`)로 재검사해, 정책이 선언한 필수 질문 축에 미심문이 남아 있으면
  그 쓰기를 차단(deny)한다.

  Contract 는 Discovery 종단 판정(02 §3.7)의 산출물이고 축 4(Coverage)는 그 판정의 타협 불가
  조건이다(DISC-INV-10). 정상 경로에서는 규약 절차가 이를 강제하지만, 절차를 우회한 임시 직접
  쓰기까지 포섭하는 "존재 최후방어"다. 선례 = `orchestration/adapters/claude/
  pretooluse_design_guard.py`(동일 성격·동일 fail 정책·동일 재사용 구조).

  이 훅은 **새 판정 로직을 만들지 않는다** — 기존 결정적 체커 check_coverage 를 그대로 재사용한다.
  훅이 담당하는 것은 (1) 스코프 판정 (2) 원장·정책 **경로 해소** (3) PreToolUse 계약 입출력뿐이다.
  판정 규칙의 정본은 `discovery/adapters/claude/coverage-ledger.schema.md` 「판정 규칙」이다.

스코프 판정 — 경로 앵커(결정적·내용 무관):
  대상 파일의 **basename** 이 Contract 인스턴스 파일명 관례 `project-contract.v<N>.md`
  (N = 십진 정수 = `instanceVersion`, `planning/adapters/claude/contract-binding.md` §4.1·§5)와
  정확히 일치할 때만 동작한다. 그 밖의 모든 Write 는 no-op 이다.

  **Contract 내용을 읽지 않는다.** 스코프도 원장 위치도 전부 경로에서 나온다 — 쓰이는 텍스트가
  자기 검사 여부를 결정하는 "자기신고" 구조를 원천 배제하기 위함이다(그 구조에서는 provenance 를
  생략하는 것만으로 검사를 벗어난다). design_guard 가 워크스페이스 앵커를 파일시스템 사실에서
  얻는 것과 동형이며, 경로 기반이므로 Write·Edit·MultiEdit 세 도구 모두 동일하게 포섭한다
  (내용 파싱 방식이라면 Edit 계열은 전문을 주지 않아 Write 에서만 실효했을 것이다).

원장 위치 — Contract 인스턴스 디렉터리 병치(schema.md §배치 위치):
  `<Contract 파일과 같은 디렉터리>/coverage-ledger.json`
  탐색·추정·최신 선택·mtime 정렬은 **0**이다(디렉터리가 같으므로 도출이 곧 확정이다).

정책 해소 — 원장이 선언한 policyRef(discovery-binding §8.3 (a)):
  원장 `policyRef` 값 `<ref>` → `<repo>/uahf/framework/adapters/claude/discovery-data/policy/
  <ref>-policy.yaml`. 저장소 루트는 **이 파일 위치**에서 얻는다(대상 경로와 무관 — 소비 워크스페이스가
  어디에 있든 정책 프로파일의 소유자는 하네스 트리다). 원장이 선언한 정책과 다른 정책으로 판정하면
  조용한 드리프트이므로, policyRef 부재·비문자열·해소 실패는 **차단**이다.

fail 경계(중요 — 두 층의 fail 방향이 다르다):
  - **체커는 fail-closed** — 원장 부재·판독 실패·정책 판독 실패는 "판정 불가"이며 통과가 아니다
    (schema.md 「판정 불가는 통과가 아니다」). 훅은 이 성질을 **보존**한다.
  - **훅은 fail-open** — 그러나 이는 **훅 자신의 결함**(stdin 파싱 실패·체커 import 실패·내부 예외)
    에만 적용된다. 자기-DoS 방지다.
  - 두 경계를 섞지 않는다: "원장이 없어서 판정 불가"는 체커의 차단 사유이지 훅의 내부 오류가 아니다.

PreToolUse 계약(stdin JSON → stdout JSON·exit code):
  차단: stdout 에 permissionDecision=deny 페이로드 + exit 0.
  허용/무관: stdout 무출력 + exit 0(no-op).

제약(불변):
  - 오프라인·순수 판독: 원장·정책·대상 파일을 일절 수정하지 않는다. 네트워크 0.
  - 프레임워크 코어 import·수정 0. coverage_check.py 만 재사용 import(같은 어댑터 경계).
  - 결정적: 같은 입력(stdin·파일시스템) → 같은 출력.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(비ASCII stderr) — design_guard 선례 동형 -------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

# 쓰기 계열 도구만 백스톱 대상(그 외 tool_name 은 no-op).
_WRITE_TOOLS = ("Write", "Edit", "MultiEdit")

# Contract 인스턴스 파일명 관례(contract-binding §4.1 파일명·§5 instanceVersion 정수).
# 스코프를 이 한 패턴으로 좁힌다 — 무관한 Write 를 막으면 세션이 마비된다.
_CONTRACT_NAME_RE = re.compile(r"^project-contract\.v\d+\.md$")

# 원장 파일명(schema.md §배치 위치 — Contract 인스턴스 디렉터리 병치).
_LEDGER_NAME = "coverage-ledger.json"

# 정책 프로파일 디렉터리(저장소 루트 기준 — discovery-binding §4.1·§8.3 (a)).
_POLICY_DIR_REL = Path("uahf/framework/adapters/claude/discovery-data/policy")

_WARN_PREFIX = "[coverage-guard] 경고: "


def _fail_open(message: str) -> int:
    """가드 **자신의** 오류 시 fail-open — stdout 무출력·stderr 경고·exit 0. 자기-DoS 방지."""
    sys.stderr.write("%s%s (fail-open, Write 허용)\n" % (_WARN_PREFIX, message))
    return 0


def _deny(reason: str) -> int:
    """PreToolUse deny 결정을 stdout 에 방출하고 exit 0. 확정 차단 판정 전용."""
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    return 0


def _abridge(errors, limit: int = 5) -> str:
    """오류 목록을 `; ` 로 조인하되 길면 앞 limit 건 + "외 N건"으로 축약(결정적)."""
    if len(errors) <= limit:
        return "; ".join(errors)
    return "%s; 외 %d건" % ("; ".join(errors[:limit]), len(errors) - limit)


def _repo_root() -> Path:
    """이 파일 위치에서 저장소 루트를 얻는다.

    `<repo>/discovery/adapters/claude/pretooluse_coverage_guard.py` → parents[3] = <repo>.
    대상 파일 경로와 무관하게 결정된다 — 정책 프로파일의 소유자는 하네스 트리이지 소비
    워크스페이스가 아니기 때문이다(discovery-binding §4.1).
    """
    return Path(__file__).resolve().parents[3]


def _resolve_policy(ledger_path: Path):
    """원장이 선언한 policyRef 를 정책 파일 경로로 해소한다. (경로, 차단사유) 반환.

    차단사유가 비어 있지 않으면 그것이 곧 deny 사유다. 이 함수는 **경로 해소**만 하며 커버리지
    판정을 수행하지 않는다(판정은 전량 check_coverage 소유).
    """
    if not ledger_path.exists():
        return None, (
            "Coverage 원장 부재 — 축 4 미확정(판정 불가는 통과가 아니다·DISC-INV-10): %s"
            % ledger_path
        )
    try:
        doc = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, "Coverage 원장 판독 실패(%s): %s — 축 4 판정 불가" % (ledger_path, exc)
    if not isinstance(doc, dict):
        return None, "Coverage 원장 최상위가 매핑(dict)이 아니다: %s" % type(doc).__name__

    ref = doc.get("policyRef")
    if not isinstance(ref, str) or not ref.strip():
        return None, (
            "Coverage 원장 policyRef 가 비어 있지 않은 문자열이 아니다: %r — 축 집합의 출처 "
            "정책이 미확정이므로 판정 불가(discovery-binding §8.3 (a))" % (ref,)
        )
    ref = ref.strip()
    # ref 는 파일명 조각이다 — 경로 이탈(`../`·절대경로)을 허용하지 않는다.
    if "/" in ref or "\\" in ref or ref in (".", ".."):
        return None, "Coverage 원장 policyRef 에 경로 구분자가 있다: %r — 해소 거부" % (ref,)

    policy_path = _repo_root() / _POLICY_DIR_REL / ("%s-policy.yaml" % ref)
    if not policy_path.exists():
        return None, (
            "policyRef=%r 해소 실패 — 정책 프로파일 부재: %s (원장이 선언한 정책으로 판정할 수 "
            "없으므로 차단·다른 정책으로 대체 판정하면 조용한 드리프트다)" % (ref, policy_path)
        )
    return policy_path, ""


def run(raw_stdin: str) -> int:
    """백스톱 본체 — raw stdin 문자열을 받아 종료 코드를 반환한다(부수효과=stdout/stderr).

    반환은 항상 0 이다(PreToolUse 계약). 차단은 stdout deny JSON 유무로 구분된다.
    내부 예외는 상위 main 이 fail-open 으로 감싼다.
    """
    # (1) stdin JSON 파싱. 실패 → fail-open(절대 차단하지 않는다).
    try:
        payload = json.loads(raw_stdin)
    except (ValueError, TypeError) as exc:
        return _fail_open("stdin JSON 파싱 실패: %s" % exc)
    if not isinstance(payload, dict):
        return _fail_open("stdin 최상위가 객체(dict)가 아님: %s" % type(payload).__name__)

    # (2) 필드 추출. 쓰기 계열 도구가 아니거나 file_path 부재면 no-op.
    #     Write·Edit·MultiEdit 는 모두 tool_input.file_path 를 준다 — 경로 앵커 방식이므로
    #     세 도구가 동일하게 포섭된다(내용 파싱 방식과 달리 Edit 계열 구멍이 없다).
    if payload.get("tool_name") not in _WRITE_TOOLS:
        return 0
    tool_input = payload.get("tool_input")
    file_path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    if not isinstance(file_path, str) or not file_path.strip():
        return 0

    # (3) 대상 절대경로 산출. 상대경로면 cwd(없으면 $CLAUDE_PROJECT_DIR) 기준 절대화.
    cwd = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    p = Path(file_path)
    target = (p if p.is_absolute() else (Path(cwd) / p)).resolve()

    # (4) 스코프 — Contract 인스턴스 파일명 관례에 정확히 일치할 때만 동작(좁고 결정적).
    if not _CONTRACT_NAME_RE.match(target.name):
        return 0

    # (5) 원장 경로 = Contract 와 같은 디렉터리(schema.md §배치 위치). 탐색·추정 0.
    ledger_path = target.parent / _LEDGER_NAME

    # (6) 정책 해소 — 원장이 선언한 policyRef 기준. 해소 실패는 차단(체커 fail-closed 보존).
    policy_path, block_reason = _resolve_policy(ledger_path)
    if block_reason:
        return _deny(
            "[COVERAGE-INCOMPLETE] 커버리지(축 4) 백스톱 — Contract 쓰기 차단. 대상: %s. 사유: %s"
            % (target, block_reason)
        )

    # (7) 커버리지 판정 — 기존 결정적 체커 재사용(design_guard 의 sys.path 삽입 패턴 동형).
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    from coverage_check import check_coverage  # noqa: E402

    errors = check_coverage(policy_path, ledger_path)
    if not errors:
        return 0  # 미심문 0 — 정상 flow 허용(no-op).

    return _deny(
        "[COVERAGE-INCOMPLETE] 커버리지(축 4) 백스톱 — 미심문 축이 남아 Contract 쓰기 차단"
        "(심문 또는 정당화 제외 필요·DISC-INV-10). 대상: %s. 원장: %s. 정책: %s. 미충족: %s"
        % (target, ledger_path, policy_path, _abridge(errors))
    )


def main() -> int:
    # 모든 내부 예외 → fail-open(exit 0·stdout 무출력·stderr 경고). 백스톱이 세션 전체 Write 를
    # 브릭하는 자기-DoS 방지. 오직 run() 이 확정 차단을 stdout 에 쓴 경우에만 차단된다.
    try:
        raw = sys.stdin.read()
    except Exception as exc:  # noqa: BLE001
        return _fail_open("stdin 읽기 실패: %s" % exc)
    try:
        return run(raw)
    except Exception as exc:  # noqa: BLE001  (체커 import 실패·기타 — 정직 fail-open)
        return _fail_open("내부 예외(%s): %s" % (type(exc).__name__, exc))


if __name__ == "__main__":
    sys.exit(main())
