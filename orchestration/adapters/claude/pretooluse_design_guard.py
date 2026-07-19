#!/usr/bin/env python3
"""pretooluse_design_guard — 설계완성도 "존재 최후방어" 백스톱(§DC-3·PreToolUse 차단 훅).

무엇을 하는가:
  Claude Code 세션이 게이트-소비 프로젝트의 `src/` 아래 파일을 Write/Edit/MultiEdit 하려 할 때,
  그 프로젝트의 설계완성도(design_completeness.check_design_completeness)를 **편입 게이트와 무관하게
  실행 시점에** 재검사해, 필수 설계 산출물이 미완이면 그 쓰기를 차단(deny)한다. 엔진 게이트
  (resolve_gate)가 정상 경로에서 이미 이를 강제하지만, 엔진 경유를 우회한 임시 직접 쓰기까지
  포섭하는 "존재 최후방어"다.

  이 훅은 새 판정 로직을 만들지 않는다 — 기존 결정적 체커 check_design_completeness 를 **그대로
  재사용**한다(resolve_gate 와 동일 정책·매니페스트 경로 관례). 훅은 스코프 판정(게이트 워크스페이스
  탐지·src/ 경로 매칭)과 PreToolUse 계약 입출력만 담당한다.

PreToolUse 계약(stdin JSON → stdout JSON·exit code):
  입력(stdin): {"tool_name", "tool_input":{"file_path"...}, "cwd"...} (Claude Code 훅 페이로드).
  출력(차단): stdout 에 {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":
    "deny","permissionDecisionReason":"..."}} + exit 0.
  출력(허용/무관): stdout 무출력 + exit 0(no-op — 정상 flow 허용).

fail 정책(자기-DoS 방지 — 백스톱이 세션 전체 Write 를 브릭하지 않는다):
  - stdin 파싱 실패·내부 예외(체커 import 실패 등) → **fail-open**(exit 0·stdout 무출력·stderr 경고).
  - **오직 "게이트 대상 src/ + 설계 미완" 확정 판정만 차단**한다(fail-closed on finding,
    fail-open on guard error).

제약(불변):
  - 오프라인·순수 판독: 파일·정책·매니페스트를 일절 수정하지 않는다. 네트워크 0.
  - 프레임워크 코어(uahf/framework/**·orchestration/framework/**) import·수정 0.
  - design_completeness.py 만 재사용 import(같은 어댑터 경계·Path(__file__).parent 배선).
  - 결정적: 같은 입력(stdin·파일시스템) → 같은 출력.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(비ASCII stderr) — design_completeness 선례 동형 -----------------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

# 쓰기 계열 도구만 백스톱 대상(그 외 tool_name 은 no-op).
_WRITE_TOOLS = ("Write", "Edit", "MultiEdit")

# 게이트-소비 프로젝트 판정 앵커(워크스페이스 SD 데이터 관례 — resolve_gate.py 와 동일).
_SD_POLICY_REL = Path(".claude") / "solution-design" / "policy" / "default-policy.yaml"
_SD_MANIFEST_REL = Path(".claude") / "solution-design" / "design-manifest.json"

# 백스톱 적용 경로 세그먼트(§DC-3 문면: `src/`). 세그먼트 단위 매칭이므로 `src/…`·
# `packages/x/src/…` 모두 포섭한다. 나중에 policy-configurable 로 확장 가능(현재는 상수).
_GUARDED_PATH_SEGMENTS = ("src",)

_WARN_PREFIX = "[design-guard] 경고: "


def _fail_open(message: str) -> int:
    """가드 오류 시 fail-open — stdout 무출력·stderr 경고·exit 0(Write 허용). 자기-DoS 방지."""
    sys.stderr.write("%s%s (fail-open, Write 허용)\n" % (_WARN_PREFIX, message))
    return 0


def _find_workspace_root(target: Path):
    """대상 파일의 부모부터 파일시스템 루트까지 상향 탐색해, SD 정책 파일이 존재하는 최초
    디렉터리 W(게이트 워크스페이스 루트)를 반환한다. 없으면 None(게이트-소비 프로젝트 아님)."""
    for base in [target.parent, *target.parent.parents]:
        if (base / _SD_POLICY_REL).exists():
            return base
    return None


def _relative_segments(target: Path, workspace: Path):
    """대상 경로를 워크스페이스 기준 상대경로 세그먼트 리스트로 변환. 실패 시 None."""
    try:
        rel = target.relative_to(workspace)
    except ValueError:
        return None
    return list(rel.parts)


def _abridge(errors, limit: int = 5) -> str:
    """오류 목록을 `; ` 로 조인하되 너무 길면 앞 limit 건 + "외 N건"으로 축약(결정적)."""
    if len(errors) <= limit:
        return "; ".join(errors)
    head = "; ".join(errors[:limit])
    return "%s; 외 %d건" % (head, len(errors) - limit)


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


def run(raw_stdin: str) -> int:
    """백스톱 본체 — raw stdin 문자열을 받아 종료 코드를 반환한다(부수효과=stdout/stderr).

    반환 0 은 항상(차단이든 허용이든 PreToolUse 계약상 exit 0). 차단은 stdout deny JSON 유무로
    구분된다. 내부 예외는 상위 main 이 fail-open 으로 감싼다.
    """
    # (1) stdin JSON 파싱. 실패 → fail-open(절대 차단하지 않는다).
    try:
        payload = json.loads(raw_stdin)
    except (ValueError, TypeError) as exc:
        return _fail_open("stdin JSON 파싱 실패: %s" % exc)
    if not isinstance(payload, dict):
        return _fail_open("stdin 최상위가 객체(dict)가 아님: %s" % type(payload).__name__)

    # (2) 필드 추출. 쓰기 계열 도구가 아니거나 file_path 부재면 no-op.
    tool_name = payload.get("tool_name")
    if tool_name not in _WRITE_TOOLS:
        return 0
    tool_input = payload.get("tool_input")
    file_path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    if not isinstance(file_path, str) or not file_path.strip():
        return 0

    # (3) 대상 절대경로 산출. 상대경로면 cwd(없으면 $CLAUDE_PROJECT_DIR) 기준 절대화.
    cwd = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    p = Path(file_path)
    target = p if p.is_absolute() else (Path(cwd) / p)
    # 정규화(.. 등 해소). resolve 는 존재하지 않는 경로도 안전 처리(strict=False 기본).
    target = target.resolve()

    # (4) 스코프 A — 게이트 워크스페이스 탐지. 없으면 no-op(설계-게이트 소비 프로젝트 아님.
    #     프레임워크 자체 .claude/ 는 solution-design/ 이 없어 여기서 걸러진다).
    workspace = _find_workspace_root(target)
    if workspace is None:
        return 0

    # (5) 스코프 B — src/ 경로. 워크스페이스 기준 상대경로 세그먼트에 정확히 'src' 세그먼트가
    #     없으면 no-op(§DC-3 문면: src/). 세그먼트 단위이므로 하위 임의 깊이 src/ 를 포섭한다.
    segments = _relative_segments(target, workspace)
    if segments is None:
        return 0
    # 마지막 세그먼트(파일명)는 디렉터리 세그먼트가 아니므로 제외하고 검사.
    dir_segments = segments[:-1]
    if not any(seg in _GUARDED_PATH_SEGMENTS for seg in dir_segments):
        return 0

    # (6) 완성도 검사 — 기존 결정적 체커 재사용(resolve_gate.py 의 sys.path 삽입 패턴 동형).
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    from design_completeness import check_design_completeness  # noqa: E402

    policy_path = workspace / _SD_POLICY_REL
    manifest_path = workspace / _SD_MANIFEST_REL
    design_errors = check_design_completeness(policy_path, manifest_path)

    if not design_errors:
        return 0  # 설계 완료 — 정상 flow 허용(no-op).

    reason = (
        "[DESIGN-INCOMPLETE] 설계완성도 백스톱 — 필수 설계 산출물 미완으로 src/ 구현 차단"
        "(Solution Design에서 산출 또는 정당화 제외 필요). 워크스페이스: %s. 누락: %s"
        % (workspace, _abridge(design_errors))
    )
    return _deny(reason)


def main() -> int:
    # 모든 내부 예외 → fail-open(exit 0·stdout 무출력·stderr 경고). 백스톱이 세션 전체 Write 를
    # 브릭하는 자기-DoS 방지. 오직 run() 이 확정 차단(deny)을 stdout 에 쓴 경우에만 차단된다.
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
