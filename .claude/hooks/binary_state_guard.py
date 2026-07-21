"""PreToolUse 운영 훅 — 이진 상태 원칙 기계 강제(금지 어휘 차단).

`.claude/AGENT.md` §Invariants "이진 상태(0 아니면 1)"의 물리 강제다. 불변 자체는
AGENT.md 가 소유하며 이 훅은 재정의하지 않는다(재정의 0).

**왜 훅인가.** 규율을 문서에만 두면 지켜지지 않는다는 것이 2026-07-21 실측으로
확인됐다 — 메모리에 규율이 있는데도 잘못 적용됐고, 같은 세션에서 Advisor 가
"부수 방어(권장)"라고 써서 그 항목이 실행층에서 실제로 누락됐다. 애매한 상태
표기는 게이트가 통과/차단 어느 쪽도 판정하지 못해 **관성으로 통과**한다.

PreToolUse 계약(stdin JSON → stdout JSON · exit code) — `pretooluse_design_guard.py` 동형:
  입력(stdin): {"tool_name", "tool_input": {...}} (Claude Code 훅 페이로드).
  출력(차단): stdout 에 {"hookSpecificOutput": {"hookEventName": "PreToolUse",
    "permissionDecision": "deny", "permissionDecisionReason": "..."}} + exit 0.
  출력(허용): stdout 무출력 + exit 0.

**불변 — fail-open.** stdin 파싱 실패·내부 예외는 **절대 차단하지 않는다**(exit 0·
stdout 무출력·stderr 경고). 훅 자신의 결함으로 세션을 브릭하는 자기-DoS 를 만들지
않는다. 오직 확정 위반만 차단한다.

**스코프 — 새로 쓰는 텍스트만.** Write 는 `content`, Edit/MultiEdit 는 `new_string`
만 검사한다. 기존 파일 본문은 읽지도 검사하지도 않는다 — 사용자 결정(2026-07-21)
"신규부터 + 닿는 것만" 을 그대로 구현한 것이다. 따라서 기존 문서의 애매한 문면은
그 줄을 실제로 고칠 때 걸린다.

**대상 — Markdown 문서만.** 코드(.py 등)는 대상이 아니다. 코드 주석·식별자에서
오탐이 나기 쉽고, 이 원칙의 대상은 설계·규약 문면이기 때문이다.

**이탈 — 사유 기록 시 허용.** 이력 인용(과거 상태 기술·부결 기록 보존 등)은 정당한
용법이므로, 쓰는 내용 안에 `uaf-allow-legacy:` 마커와 사유를 함께 두면 통과한다
(책임 있는 자율 (b) — 자율 = 기본값 + 이탈 시 사유 기록).
"""

import json
import re
import sys

MARKER = "uaf-allow-legacy:"

# 상태값 계열 — 게이트 판정에 직접 종속되므로 오탐이 적고 임팩트가 크다.
_STATE_TERMS = [
    "부분 해소",
    "부분해소",
    "조건부 확정",
    "조건부확정",
    "판정 보류",
    "판정보류",
    "TBD",
]

# 강도 부사 계열 — 필수(1)/비요구(0) 중 하나로 환원해야 하는 중간 강도 표현.
# "권장"·"고려"는 서술적 정당 용법(예: "권장 경로")이 많아 1단계에서 제외한다.
_HEDGE_TERMS = [
    "가급적",
    "바람직하다",
    "바람직함",
    "해도 그만",
]

_TERMS = _STATE_TERMS + _HEDGE_TERMS

# 강한 완전성 주장 — 근거 표기 없이는 검증 불가이므로 주장이 아니라 인상이다.
# `.claude/AGENT.md` §Invariants "근거 표기 이진(확인함 아니면 추정)" 의 물리 강제.
# 오탐을 줄이기 위해 약한 표현("모두"·"전부" 등 일상어)은 대상에서 뺀다.
_COMPLETENESS_TERMS = [
    "전수",
    "전건",
    "잔여 0",
    "예외 없이",
    "빠짐없이",
]

# 근거 종류를 이진으로 밝히는 마커. 둘 중 하나가 같은 쓰기 안에 있으면 통과한다.
_EVIDENCE_MARKERS = ("uaf-verified:", "uaf-assumed:", "스윕 범위", "검색 범위")

_MD_SUFFIXES = (".md", ".markdown")


def _fail_open(message: str) -> int:
    """훅 자신의 결함으로 세션을 막지 않는다 — 경고만 남기고 허용."""
    print("[binary-state-guard] fail-open: %s" % message, file=sys.stderr)
    return 0


def _deny(reason: str) -> int:
    """확정 위반만 차단한다(PreToolUse 계약상 exit 0 · stdout deny JSON)."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }, ensure_ascii=False))
    return 0


def _collect_written_text(tool_name: str, tool_input: dict):
    """새로 쓰이는 텍스트만 모은다 — 기존 파일 본문은 보지 않는다."""
    if tool_name == "Write":
        value = tool_input.get("content")
        return [value] if isinstance(value, str) else []
    if tool_name == "Edit":
        value = tool_input.get("new_string")
        return [value] if isinstance(value, str) else []
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits")
        if not isinstance(edits, list):
            return []
        return [e.get("new_string") for e in edits
                if isinstance(e, dict) and isinstance(e.get("new_string"), str)]
    return []


def find_violations(text: str):
    """금지 어휘 출현을 (용어, 발췌) 목록으로 반환한다. 순수 함수."""
    hits = []
    for term in _TERMS:
        for match in re.finditer(re.escape(term), text):
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            excerpt = text[start:end].replace("\n", " ").strip()
            hits.append((term, excerpt))
            break  # 용어당 1건만 — 보고를 짧게 유지
    return hits


def run(raw_stdin: str) -> int:
    try:
        payload = json.loads(raw_stdin)
    except Exception as exc:  # noqa: BLE001
        return _fail_open("stdin JSON 파싱 실패: %s" % exc)
    if not isinstance(payload, dict):
        return _fail_open("stdin 최상위가 객체가 아님: %s" % type(payload).__name__)

    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return _fail_open("tool_input 부재 또는 비객체")

    file_path = tool_input.get("file_path")
    if not isinstance(file_path, str) or not file_path.lower().endswith(_MD_SUFFIXES):
        return 0  # Markdown 문서만 대상

    texts = _collect_written_text(tool_name, tool_input)
    if not texts:
        return 0

    joined = "\n".join(texts)
    if MARKER in joined:
        return 0  # 사유 기록된 이탈 — 허용

    violations = find_violations(joined)

    # 근거 표기 이진 — 강한 완전성 주장에 근거 마커가 없으면 위반.
    if not any(m in joined for m in _EVIDENCE_MARKERS):
        for term in _COMPLETENESS_TERMS:
            match = re.search(re.escape(term), joined)
            if match:
                start = max(0, match.start() - 30)
                end = min(len(joined), match.end() + 30)
                violations.append((
                    "완전성 주장 %r (근거 표기 없음)" % term,
                    joined[start:end].replace("\n", " ").strip(),
                ))
                break

    if not violations:
        return 0

    lines = ["이진 원칙 위반 — 애매한 표기는 게이트가 판정할 수 없어 관성 통과합니다",
             "(.claude/AGENT.md §Invariants '이진 상태' · '근거 표기 이진').", ""]
    for term, excerpt in violations:
        lines.append("  · %r — ...%s..." % (term, excerpt))
    lines += [
        "",
        "고치는 법:",
        "  - 상태는 이진으로: '부분 해소' → '해소' 또는 '미해소'(미해소는 정당하며 하류를 막는다).",
        "  - 강도 부사는 필수/비요구로 환원: '가급적 X' → 'X 한다' 또는 요구에서 제외.",
        "  - 임계값 'TBD' 로 케이스를 닫지 않는다 — 합격선 없는 검증은 반드시 관성 통과한다.",
        "  - 조건은 판정 가능한 술어로: 'X 전제로 유효' → 'X == true 일 때만 유효'.",
        "  - 완전성 주장에는 근거를 이진으로: 'uaf-verified: <무엇을 어떤 수단으로 훑었나>'",
        "    또는 'uaf-assumed: <왜 확인하지 않았나>'. '스윕 범위'·'검색 범위' 명시도 통과합니다.",
        "",
        "이력 인용 등 정당한 용법이면 쓰는 내용에 '%s <사유>' 를 함께 두면 통과합니다." % MARKER,
    ]
    return _deny("\n".join(lines))


def main() -> int:
    try:
        raw = sys.stdin.read()
    except Exception as exc:  # noqa: BLE001
        return _fail_open("stdin 읽기 실패: %s" % exc)
    try:
        return run(raw)
    except Exception as exc:  # noqa: BLE001
        return _fail_open("내부 예외: %s" % exc)


if __name__ == "__main__":
    sys.exit(main())
