#!/usr/bin/env python3
"""pretooluse_lane_guard — 경량 레인 접점 침범 차단 훅(원장 §2.2 (ii) Write 시점 강제 지점).

무엇을 하는가:
  Claude Code 세션이 파일을 Write/Edit/MultiEdit 하려 할 때, 그 파일이 속한 **레인 워크스페이스의
  레인 마커**(`<W>/.claude/lane.json` — 경로는 lane-registry.json marker 절 데이터)를 판독한다.
  마커의 lane 이 `lightweight` 로 확정된 워크스페이스에서 **접점 파일**(Contract·게이트·정본 문서·
  스키마·정책 데이터 — 패턴은 lane-registry.json 데이터)을 건드리려 하면 그 쓰기를 **deny** 한다.

  이 훅은 새 판정 로직을 만들지 않는다 — `lane_resolve.classify_target`(같은 어댑터 경계의 결정적
  접점 술어)을 **그대로 재사용**한다. 훅은 스코프 판정(마커 탐색·레인 판독)과 PreToolUse 계약
  입출력만 담당한다(pretooluse_design_guard 가 design_completeness 를 재사용하는 선례 동형).

  「강제 없는 규율 신설 금지」의 강제 지점이 바로 이 훅이다 — 레인 판별(형태 B 로더)은 계산만 하고
  적용을 강제하지 않으므로, 경량 레인 선언이 실제로 무엇을 막는가는 여기서만 물리적으로 성립한다.

PreToolUse 계약(stdin JSON → stdout JSON·exit code):
  입력(stdin): {"tool_name", "tool_input":{"file_path"...}, "cwd"...} (Claude Code 훅 페이로드).
  출력(차단): stdout 에 {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":
    "deny","permissionDecisionReason":"..."}} + exit 0.
  출력(허용/무관): stdout 무출력 + exit 0(no-op — 정상 flow 허용).

fail 정책(자기-DoS 방지 — 가드가 세션 전체 Write 를 브릭하지 않는다):
  - stdin 파싱 실패·마커 부재·마커 파싱 실패·레지스트리 부재/손상·import 실패·내부 예외
    → **fail-open**(exit 0·stdout 무출력·stderr 경고).
  - **오직 "마커 lane == lightweight + 접점 패턴 적중" 확정 판정만 차단**한다
    (fail-closed on finding, fail-open on guard error).

제약(불변):
  - 오프라인·순수 판독: 마커·레지스트리·대상 파일을 일절 수정하지 않는다. 네트워크 0. LLM 0.
  - 프레임워크 코어(uahf/framework/**·orchestration/framework/**) import·수정 0.
  - lane_resolve.py 만 재사용 import(같은 어댑터 경계·Path(__file__).parent 배선).
  - 접점 패턴·레인 어휘·마커 경로를 코드에 두지 않는다(전부 lane-registry.json — Policy as Data).
  - 결정적: 같은 입력(stdin·파일시스템) → 같은 출력.

침묵 주의(관측 경로): 훅 배선이 죽으면 이 파일은 **아무 소리도 내지 않고** 도구 호출이 통과한다.
  배선 변경 시 단위 테스트가 아니라 실제 도구 호출로 차단을 확인한다(.claude/CLAUDE.md 훅 배선 절).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(비ASCII stderr) — pretooluse_design_guard 선례 동형 ---------------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

# 쓰기 계열 도구만 대상(그 외 tool_name 은 no-op).
_WRITE_TOOLS = ("Write", "Edit", "MultiEdit")

_WARN_PREFIX = "[lane-guard] 경고: "

HERE = Path(__file__).resolve().parent
_REGISTRY = HERE / "lane-registry.json"


def _fail_open(message: str) -> int:
    """가드 오류 시 fail-open — stdout 무출력·stderr 경고·exit 0(Write 허용). 자기-DoS 방지."""
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


def _find_marker(target: Path, marker_rel: str):
    """대상 파일의 부모부터 파일시스템 루트까지 상향 탐색해, 레인 마커가 존재하는 최초 디렉터리
    W(레인 워크스페이스 루트)와 마커 경로를 반환한다. 없으면 (None, None)."""
    for base in [target.parent, *target.parent.parents]:
        candidate = base / marker_rel
        if candidate.is_file():
            return base, candidate
    return None, None


def run(raw_stdin: str) -> int:
    """가드 본체 — raw stdin 문자열을 받아 종료 코드를 반환한다(부수효과=stdout/stderr).

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
    target = target.resolve()  # 정규화(.. 해소·미존재 경로 안전).

    # (4) 레지스트리 적재(마커 경로·접점 패턴·레인 어휘의 단일 소스). 부재·손상 → fail-open.
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    from lane_resolve import classify_target, load_registry  # noqa: E402  (import 실패 → main fail-open)

    reg = load_registry(_REGISTRY)
    marker_cfg = reg["marker"]
    marker_rel = marker_cfg["relativePath"]
    enforced_lane = marker_cfg["enforcedLane"]

    # (5) 스코프 A — 레인 마커 탐색. 없으면 no-op(레인 선언이 없는 표면 = 훅 무동작).
    workspace, marker_path = _find_marker(target, marker_rel)
    if workspace is None:
        return 0

    # (6) 마커 판독. 파싱 실패·lane 값 미인식 → fail-open(무동작 통과).
    try:
        with open(marker_path, "r", encoding="utf-8") as fh:
            marker = json.load(fh)
    except (OSError, ValueError) as exc:
        return _fail_open("레인 마커 판독 실패(%s): %s" % (marker_path, exc))
    if not isinstance(marker, dict):
        return _fail_open("레인 마커 최상위가 객체가 아님: %s" % marker_path)
    lane = marker.get("lane")
    if lane not in reg["laneVocabulary"]:
        return _fail_open("레인 마커의 lane 값 미인식(%r) — 어휘 %r 밖: %s"
                          % (lane, reg["laneVocabulary"], marker_path))

    # (7) 스코프 B — 강제 대상 레인만. standard 는 접점을 건드려도 무동작(강제 대상 아님).
    if lane != enforced_lane:
        return 0

    # (8) 접점 판정 — lane_resolve 의 결정적 술어 재사용(새 판정 로직 0).
    record = classify_target(str(target), workspace, reg["touchpointClasses"])
    if not record["touched"]:
        return 0  # 접점 아님 — 경량 레인의 정상 작업 표면(허용).

    reason = (
        "[LANE-LIGHTWEIGHT] 경량 레인 접점 침범 차단 — 이 워크스페이스는 lane=%s 로 선언돼 있는데 "
        "대상이 접점 클래스 '%s'(패턴 %s)에 적중했다. 접점 변경은 표준 레인 절차(전 게이트·전 원장) "
        "소관이다. 해소 경로 2개: ① 레인을 standard 로 승급(마커 %s 의 lane 을 standard 로 재판정 — "
        "lane_resolve.py 로 재계산) ② 사용자 override 로 진행하되 %s(사유)를 마커·원장에 기록. "
        "워크스페이스: %s. 대상: %s"
        % (lane, record["matchedClass"], record["matchedPattern"], marker_path,
           reg["overrideReasonField"], workspace, record["relative"])
    )
    return _deny(reason)


def main() -> int:
    # 모든 내부 예외 → fail-open(exit 0·stdout 무출력·stderr 경고). 가드가 세션 전체 Write 를
    # 브릭하는 자기-DoS 방지. 오직 run() 이 확정 차단(deny)을 stdout 에 쓴 경우에만 차단된다.
    try:
        raw = sys.stdin.read()
    except Exception as exc:  # noqa: BLE001
        return _fail_open("stdin 읽기 실패: %s" % exc)
    try:
        return run(raw)
    except Exception as exc:  # noqa: BLE001  (lane_resolve import 실패·레지스트리 손상·기타)
        return _fail_open("내부 예외(%s): %s" % (type(exc).__name__, exc))


if __name__ == "__main__":
    sys.exit(main())
