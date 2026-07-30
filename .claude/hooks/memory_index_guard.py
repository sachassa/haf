"""PreToolUse 운영 훅 — 메모리 색인(MEMORY.md) 예산 쓰기 차단.

memory-guard.sh(SessionStart)는 경고만 낸다 — 경고만으로는 초과가 방치됨이
실측됐다(2026-07-30 핸드오프 4,782B 초과 방치 사례와 동형·사용자 지적). 이
훅은 색인을 예산 초과로 **키우는** Write/Edit 를 저장 시점에 거부한다.
축소·비증가 쓰기는 예산 초과 상태에서도 허용한다 — 스스로 못 고치는 잠금
(자기-DoS)을 만들지 않기 위한 불변.

대상 = 경로가 .../memory/MEMORY.md 인 파일만. 예산 값 = memory-guard.sh 와
동일(총 6,000B · 색인 항목 행 400B). 행 상한 검사는 전체 내용을 아는 Write 만
수행한다 — Edit 의 new_string 은 행 조각일 수 있어 오탐 위험으로 제외한다.
계약·fail-open 불변 = binary_state_guard.py 동형(stdin JSON → deny JSON·exit 0).
"""

import json
import os
import sys

BUDGET = 6000      # memory-guard.sh BUDGET 과 동치 유지
LINE_CAP = 400     # memory-guard.sh LINE_CAP 과 동치 유지


def _fail_open(message):
    print("[memory-index-guard] fail-open: %s" % message, file=sys.stderr)
    return 0


def _deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }, ensure_ascii=False))
    return 0


def _is_index(path):
    if not isinstance(path, str):
        return False
    return path.replace("\\", "/").endswith("/memory/MEMORY.md")


def _nbytes(text):
    return len(text.encode("utf-8"))


def run(raw_stdin):
    try:
        payload = json.loads(raw_stdin)
    except Exception as exc:  # noqa: BLE001
        return _fail_open("stdin 파싱 실패: %s" % exc)
    if not isinstance(payload, dict):
        return _fail_open("stdin 최상위가 객체가 아님")

    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    path = tool_input.get("file_path")
    if not _is_index(path):
        return 0

    if tool_name == "Write":
        content = tool_input.get("content")
        if not isinstance(content, str):
            return 0
        size = _nbytes(content)
        if size > BUDGET:
            return _deny(
                "메모리 색인 예산 초과 — 이 내용은 %dB > 예산 %dB. 항목을 "
                "'한 줄+짧은 훅'으로 줄여라(커밋해시·날짜·하위트랙은 개별 "
                "메모리 파일 본문에만). 예산 이하 내용은 언제나 저장된다."
                % (size, BUDGET))
        long_lines = [l for l in content.splitlines()
                      if l.startswith("- ") and _nbytes(l) > LINE_CAP]
        if long_lines:
            return _deny(
                "메모리 색인 항목 행 상한(%dB) 초과 %d개 — 상세는 개별 파일 "
                "본문에 두고 색인 행을 줄여라." % (LINE_CAP, len(long_lines)))
        return 0

    # Edit/MultiEdit — 증가분만 판정(new_string 은 행 조각일 수 있다).
    try:
        current = os.path.getsize(path)
    except OSError:
        return 0
    if tool_name == "Edit":
        old = tool_input.get("old_string")
        new = tool_input.get("new_string")
        if not (isinstance(old, str) and isinstance(new, str)):
            return 0
        if tool_input.get("replace_all"):
            try:
                with open(path, encoding="utf-8") as fh:
                    occurrences = fh.read().count(old)
            except OSError as exc:
                return _fail_open("파일 읽기 실패: %s" % exc)
        else:
            occurrences = 1
        delta = (_nbytes(new) - _nbytes(old)) * occurrences
    elif tool_name == "MultiEdit":
        edits = tool_input.get("edits")
        if not isinstance(edits, list):
            return 0
        delta = sum(
            _nbytes(e["new_string"]) - _nbytes(e["old_string"])
            for e in edits
            if isinstance(e, dict)
            and isinstance(e.get("old_string"), str)
            and isinstance(e.get("new_string"), str))
    else:
        return 0

    if delta > 0 and current + delta > BUDGET:
        return _deny(
            "메모리 색인 예산 초과 — 이 편집 후 약 %dB > 예산 %dB(현재 %dB·"
            "증가 +%dB). 먼저 다른 항목을 줄인 뒤 추가하라. 축소·비증가 "
            "편집은 언제나 허용된다." % (current + delta, BUDGET, current, delta))
    return 0


def main():
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
