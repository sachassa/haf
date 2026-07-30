"""커밋 훅 보조 — 스테이징된 md diff 의 추가 행에 이진 원칙 어휘 검사.

binary_state_guard.py(PreToolUse)는 Claude 도구 쓰기만 본다 — IDE 직접 편집·
스크립트 산출 등 비도구 경로로 들어온 문면은 검사 없이 커밋될 수 있다(2026-07-30
실측: 종전 pre-commit 은 예산·재퇴적 가드 2종만 호출). 이 스크립트가 그 구멍을
커밋 시점에 막는다. 검사 대상은 **스테이징 diff 의 추가 행만** — "신규부터 +
닿는 것만" 스코프(사용자 결정 2026-07-21)와 동일하며 기존 본문을 소급하지 않는다.

계약(.githooks/pre-commit 소비): 위반 시 stdout 보고 + exit 0. 정상 침묵.
fail-open — git 부재·diff 실패·내부 예외는 절대 발화하지 않는다(자기-DoS 방지).
어휘·마커 정본 = binary_state_guard.py 를 import 해 재사용한다(값 사본 0).
백로그 등재 형식 검사는 이관하지 않는다 — 세그먼트 판정에 파일 전체 문맥이
필요해 diff 단편으로는 오판하므로 Write 훅이 계속 소유한다.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binary_state_guard import (  # noqa: E402
    MARKER,
    _COMPLETENESS_TERMS,
    _EVIDENCE_MARKERS,
    find_violations,
)

_MD_SUFFIXES = (".md", ".markdown")


def added_lines_by_file():
    """스테이징 diff 에서 md 파일별 추가 행 텍스트를 모은다."""
    out = subprocess.run(
        ["git", "diff", "--cached", "-U0", "--no-color", "--diff-filter=ACMR"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        check=True,
    ).stdout
    files = {}
    cur = None
    for line in out.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            cur = path[2:] if path.startswith("b/") else None
            continue
        if cur and line.startswith("+") and not line.startswith("+++"):
            files.setdefault(cur, []).append(line[1:])
    return {p: "\n".join(ls) for p, ls in files.items()
            if p.lower().endswith(_MD_SUFFIXES)}


def check(staged):
    """파일별 추가 행을 검사해 보고 행 목록을 반환한다. 순수 함수."""
    reports = []
    for path, text in sorted(staged.items()):
        if MARKER in text:
            continue  # 사유 기록된 이탈 — 허용
        violations = find_violations(text)
        if not any(m in text for m in _EVIDENCE_MARKERS):
            for term in _COMPLETENESS_TERMS:
                match = re.search(re.escape(term), text)
                if match:
                    start = max(0, match.start() - 30)
                    end = min(len(text), match.end() + 30)
                    violations.append((
                        "완전성 주장 %r (근거 표기 없음)" % term,
                        text[start:end].replace("\n", " ").strip(),
                    ))
                    break
        for term, excerpt in violations:
            reports.append("  %s · %r — ...%s..." % (path, term, excerpt))
    return reports


def main():
    try:
        staged = added_lines_by_file()
        reports = check(staged)
    except Exception:  # noqa: BLE001 — fail-open
        return 0
    if reports:
        print("[이진 원칙 커밋 검사] 스테이징된 md 추가 행에 금지 문면이 있다:")
        print("\n".join(reports))
        print("고치는 법 = 이진 표기로 환원(binary_state_guard.py 안내와 동일). "
              "정당한 용법이면 해당 파일 추가 행에 '%s <사유>' 를 포함하라." % MARKER)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001
        sys.exit(0)
