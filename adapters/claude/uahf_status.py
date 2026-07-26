#!/usr/bin/env python3
"""uahf_status — /uahf-status 상태 표면화 결정적 로더 (형태 B·LLM 0·순수 판독).

무엇을 하는가:
  `.claude/commands/uahf-status.md`(형태 A 문서 명령)가 "정본에서 회수해 표면화하라"고 지시하던
  절차 중 **결정적으로 기계화 가능한 판독**을 실행 스크립트로 물리화한다. 종전 경로는 주 세션이
  `docs/session-handoff.md`(15KB 단일 스냅샷)를 정독하는 LLM 턴이었고, 이를 결정적 추출로 대체해
  턴을 제거한다(성능 실측 1위 레버 = form-B 턴 제거). 선례 = `entry/adapters/claude/entry_resolve.py`
  (Entry Resolution 로더)·`adapters/claude/verify_checks.py`(Verifier 결정적 슬라이스).

  물리 홈 = 저장소 루트 `adapters/claude/` — 루트 ARCHITECTURE.md §5 "UAF-level 거버넌스 실행
  스크립트의 물리 홈". config 가 아니라 실행 스크립트이므로 루트 `.claude/`(설정 디렉터리)에 두지 않는다.

무엇을 하지 않는가(경계):
  - **상태를 판정·해석하지 않는다.** 핸드오프·ARCHIVE 문면을 추출해 그대로 방출한다. "지금 무엇을
    착수할지"의 결정은 주 세션(Advisor)·사용자 게이트 몫이다.
  - **정본을 재정의하지 않는다.** 값을 하드코딩하지 않으며(마일스톤·순위·포인터 전부 파일에서 추출),
    문서 문면이 바뀌면 출력도 따라 바뀐다.
  - 파일을 쓰지 않는다(읽기 전용). git 은 `rev-parse`·`log -1` 판독만 호출한다.
  - 핸드오프 전문을 덤프하지 않는다 — 표면화 항목만 추출한다(토큰 위생). 전문이 필요하면 주 세션이
    직접 정독한다.

결정성:
  같은 파일시스템·git 상태 → 같은 출력. 추출은 heading 기반 파싱이며 순서는 문서 순서를 보존한다.

fail-soft 계약(상태 표면화 도구가 상태를 죽이면 안 된다):
  - 절(節) 부재 → 크래시 대신 `[해당 절 미검출 — docs/session-handoff.md 직접 정독 필요]` 폴백 줄
    출력 후 계속 진행.
  - 핸드오프 파일 자체 부재 → 그 사실을 출력하고 나머지 섹션은 계속 진행.
  - git 미가용/실패 → `git 미가용` 표기 후 계속 진행.
  - 종료 코드는 어떤 경우에도 0이다(예외 방어 포함). 이 스크립트의 실패가 세션 진입을 차단하지 않는다.

인코딩(한국어 출력 전제):
  stdout/stderr 를 UTF-8 로 재구성한다(`sys.stdout.reconfigure`). 호출 측에서도
  `PYTHONIOENCODING=utf-8` 을 명시하는 것을 권장한다(cp949 폴백 시 출력 깨짐·stderr 조용한 유실 방지).

경로 재정의(테스트·이동 대응):
  - `UAHF_STATUS_HANDOFF` — 핸드오프 파일 경로 재정의(부재 경로 지정 시 fail-soft 분기 검증용).
  - `UAHF_STATUS_ARCHIVE` — ARCHIVE 원장 경로 재정의.
  - `UAHF_STATUS_ROOT` — 저장소 루트 재정의(기본 = 이 파일의 조부모 디렉터리).

사용:
  PYTHONIOENCODING=utf-8 python adapters/claude/uahf_status.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

MISSING_SECTION = "[해당 절 미검출 — docs/session-handoff.md 직접 정독 필요]"

try:  # pragma: no cover - 인터프리터 구현 의존
    # newline="\n" — Windows 텍스트 모드의 CRLF 변환을 끄고 플랫폼 간 바이트 동일 출력을 유지한다.
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[attr-defined]
except Exception:
    pass


# --------------------------------------------------------------------------
# 경로 해석
# --------------------------------------------------------------------------

def repo_root() -> Path:
    override = os.environ.get("UAHF_STATUS_ROOT")
    if override:
        return Path(override)
    # <root>/adapters/claude/uahf_status.py → parents[2] == <root>
    return Path(__file__).resolve().parents[2]


def handoff_path(root: Path) -> Path:
    override = os.environ.get("UAHF_STATUS_HANDOFF")
    if override:
        return Path(override)
    return root / "docs" / "session-handoff.md"


def archive_path(root: Path) -> Path:
    override = os.environ.get("UAHF_STATUS_ARCHIVE")
    if override:
        return Path(override)
    return root / "ARCHIVE.md"


def read_lines(path: Path) -> Optional[List[str]]:
    """텍스트 파일을 라인 리스트로 판독. 부재·판독 실패 시 None(fail-soft)."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    return text.splitlines()


# --------------------------------------------------------------------------
# heading 기반 추출 유틸
# --------------------------------------------------------------------------

def is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s", line))


def find_heading_index(lines: List[str], needle: str) -> Optional[int]:
    """heading 줄 중 needle 을 포함하는 첫 인덱스."""
    for i, line in enumerate(lines):
        if is_heading(line) and needle in line:
            return i
    return None


def find_section_index(lines: List[str], letter: str) -> Optional[int]:
    """`## §<letter>.` 형태의 상위 절 heading 인덱스.

    부분문자열 매칭을 쓰지 않는다 — `§D` 는 `§DC` 를 언급하는 다른 절 heading 에도 부분
    일치하므로(실측: `## §B ... §DC 산재분 병합` 이 `§D` 조회에 먼저 걸려 §D 표가 미검출됨),
    절 문자 뒤에 구분자(`.`·공백)가 오는 형태로 앵커한다.
    """
    pattern = re.compile(r"^#{2,3}\s+§" + re.escape(letter) + r"(?:[.\s]|$)")
    for i, line in enumerate(lines):
        if pattern.match(line):
            return i
    return None


def block_after_heading(lines: List[str], start: int) -> List[str]:
    """heading(start) 다음부터 다음 heading 직전까지의 본문 라인(양끝 공백 줄 제거)."""
    body: List[str] = []
    for line in lines[start + 1:]:
        if is_heading(line):
            break
        body.append(line)
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return body


def first_bold_paragraph(body: List[str]) -> Optional[str]:
    """본문에서 굵은 강조(**)로 시작하는 첫 문단을 한 덩어리로 반환."""
    buf: List[str] = []
    for line in body:
        if not buf:
            if line.lstrip().startswith("**"):
                buf.append(line.strip())
            continue
        if not line.strip():
            break
        buf.append(line.strip())
    if not buf:
        return None
    return " ".join(buf)


# --------------------------------------------------------------------------
# ① git 상태
# --------------------------------------------------------------------------

def git_line(root: Path) -> str:
    def run(args: List[str]) -> Optional[str]:
        try:
            proc = subprocess.run(
                ["git", "-C", str(root)] + args,
                capture_output=True,
                timeout=15,
            )
        except Exception:
            return None
        if proc.returncode != 0:
            return None
        return proc.stdout.decode("utf-8", errors="replace").strip()

    branch = run(["rev-parse", "--abbrev-ref", "HEAD"])
    head = run(["log", "-1", "--format=%h %s"])
    if branch is None and head is None:
        return "git 미가용 (branch·HEAD 판독 실패 — 계속 진행)"
    return f"branch={branch or '판독 실패'} · HEAD={head or '판독 실패'}"


# --------------------------------------------------------------------------
# 섹션 방출
# --------------------------------------------------------------------------

def emit(line: str = "") -> None:
    print(line)


def emit_handoff(lines: Optional[List[str]], path: Path) -> None:
    emit("## ② 핸드오프 추출 (docs/session-handoff.md)")
    emit()
    if lines is None:
        emit(f"[핸드오프 부재·판독 실패: {path}]")
        emit("→ 경로·`UAHF_STATUS_HANDOFF` 재정의 점검. 회수는 수기 정독 폴백.")
        emit()
        return

    # 머리 지위 줄 (문서 머리 1~7행 범위)
    status_line = next((l.strip() for l in lines[:7] if l.strip().startswith("지위:")), None)
    emit("### 머리 지위")
    emit(status_line or MISSING_SECTION)
    emit()

    # §A 현행 상태 — 첫 굵은 요약 문단
    emit("### §A 현행 상태 (첫 요약 문단)")
    idx_a = find_section_index(lines, "A")
    summary = first_bold_paragraph(block_after_heading(lines, idx_a)) if idx_a is not None else None
    emit(summary or MISSING_SECTION)
    emit()

    # ★ 다음 착수 순위 — 블록 전문
    emit("### ★ 다음 착수 순위 (블록 전문)")
    idx_star = find_heading_index(lines, "다음 착수 순위")
    if idx_star is None:
        emit(MISSING_SECTION)
    else:
        emit(lines[idx_star].lstrip("# ").strip())
        star_body = block_after_heading(lines, idx_star)
        while star_body and re.match(r"^-{3,}$", star_body[-1].strip()):  # 절 구분선 제거
            star_body.pop()
            while star_body and not star_body[-1].strip():
                star_body.pop()
        for line in star_body:
            emit(line)
    emit()

    # §B 하위 heading 목록
    emit("### §B 이월·미해소 — 하위 절 목록")
    idx_b = find_section_index(lines, "B")
    sub: List[str] = []
    if idx_b is not None:
        for line in lines[idx_b + 1:]:
            if re.match(r"^##\s", line):  # 다음 상위 절에서 멈춤
                break
            if re.match(r"^###\s", line):
                sub.append(line.lstrip("# ").strip())
    if sub:
        for title in sub:
            emit(f"- {title}")
    else:
        emit(MISSING_SECTION)
    emit()

    # §DC 잔여 절 유무
    # §DC 잔여 — 판정 규칙: `###` 하위 절 heading 중 §DC 를 언급하는 것만 센다.
    # 상위 `##` 절 heading 은 병합 이력 서술로 §DC 를 언급할 수 있어 제외한다(실측 오탐 1건).
    emit("### §DC 잔여")
    dc_heads = [
        l.lstrip("# ").strip()
        for l in lines
        if re.match(r"^###\s", l) and "§DC" in l
    ]
    if dc_heads:
        emit(f"유 ({len(dc_heads)}절) — " + " / ".join(dc_heads))
    else:
        emit("무 (### 하위 절 heading 에 §DC 언급 없음 — 잔여 절 미검출)")
    emit()


def emit_pointer_table(lines: Optional[List[str]]) -> None:
    emit("## ③ §D 정본 포인터 (전문)")
    emit()
    if lines is None:
        emit(MISSING_SECTION)
        emit()
        return
    idx_d = find_section_index(lines, "D")
    if idx_d is None:
        emit(MISSING_SECTION)
        emit()
        return
    body = block_after_heading(lines, idx_d)
    table = [l for l in body if l.lstrip().startswith("|")]
    if not table:
        emit(MISSING_SECTION)
    else:
        for line in table:
            emit(line)
    emit()


def emit_archive(lines: Optional[List[str]], path: Path) -> None:
    emit("## ④ ARCHIVE 원장")
    emit()
    if lines is None:
        emit(f"[ARCHIVE 파일 부재·판독 실패: {path}]")
        emit()
        return
    rows = 0
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.match(r"^\|[\s:|-]+\|$", stripped):  # 구분 행
            continue
        if "앵커 커밋" in stripped:  # 헤더 행
            continue
        rows += 1
    emit(f"{path.name} 데이터 행 {rows}건 (열람 = `git show <앵커>:<경로>`)")
    emit()


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    root = repo_root()
    hpath = handoff_path(root)
    apath = archive_path(root)
    hlines = read_lines(hpath)
    alines = read_lines(apath)

    emit("# /uahf-status — 상태 표면화 (형태 B · LLM 0 · 읽기 전용)")
    emit()
    emit("## ① git")
    emit()
    emit(git_line(root))
    emit()
    emit_handoff(hlines, hpath)
    emit_pointer_table(hlines)
    emit_archive(alines, apath)
    emit("---")
    emit(f"원본 = {hpath.name} · {apath.name}. 판정·착수 결정은 주 세션·사용자 게이트 몫. 폴백 줄이 보이면 원본 직접 정독.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail-soft — 상태 도구가 세션을 죽이지 않는다
        print(f"[uahf_status 내부 예외 — fail-soft 계속] {type(exc).__name__}: {exc}")
        sys.exit(0)
