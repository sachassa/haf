#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""history_compact.py — 문서 이력 절 제거 (형태 B · 결정적 · LLM 0)

사용자 결정 2026-07-27: 전 md 의 이력 절(Revision History) 본문을 파일에서 제거하고
기록은 git 으로만 보존한다. 파일에는 절 헤딩 + git 포인터 1줄 스텁만 남긴다.

- 결정성: datetime · random 미사용. 같은 입력 -> 같은 출력. 재실행 멱등.
- 절 밖 바이트는 1바이트도 변경하지 않는다.
- dry-run 이 기본이며 --apply 를 명시해야 파일을 쓴다.

usage:
  python .claude/tools/history_compact.py --anchor <hash> [--root DIR]
                                          [--exclude GLOB]... [--include-ambiguous]
                                          [--report PATH] [--apply]
  python .claude/tools/history_compact.py --check [--root DIR] [--exclude GLOB]...

--check (재퇴적 감시 모드):
  이력 절 안에 표 데이터 행(헤더·구분행 제외)이 1행 이상 남아 있는 파일을 열거한다.
  출력 = `REACCUM <경로> rows=<n>` 행들 + 마지막 `TOTAL files=<k> rows=<m>`.
  탐지 0이면 출력 0줄. 종료 코드는 항상 0(가드 fail-open — 판정은 출력 유무로).
  dry-run/apply 경로와 코드가 분리돼 있어 기존 출력에 영향이 없다.
"""

import argparse
import fnmatch
import io
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- 정책 데이터

# 이력 절 헤딩 탐지 (대소문자 무시)
HEADING_RE = re.compile(r"^(#+)[ \t]+.*(이력|Revision History|개정 ?이력|Changelog)", re.IGNORECASE)
# 임의 헤딩 (스팬 종료 판정용)
ANY_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+\S")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
# 절 말미 수평선 (thematic break) — 스텁 뒤에 보존한다.
HRULE_RE = re.compile(r"^ {0,3}(-{3,}|_{3,}|\*{3,})\s*$")
# 표 행 / 표 구분행 (--check 재퇴적 감시 전용 — dry-run/apply 경로는 쓰지 않는다)
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:|-]*-[\s:|-]*\|\s*$")

STUB_TEMPLATE = (
    "이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 {anchor}). "
    "UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3."
)

# 하드코딩 제외 (경로 glob · posix 상대경로 기준)
# 사용자 정정 지시 2026-07-27 "전체 md 다 해, 빼지 말고" — 기본 제외 폐기.
# .git 은 파일 수집 단계에서 배제한다. --exclude 로만 추가 제외가 가능하다.
DEFAULT_EXCLUDES = []

# 관측용 — 종전 제외 후보였던 경로. 대상에서 빠지지 않으며 보고에만 별도 표기한다.
WATCH_PATTERNS = [
    "uahf/framework/adapters/claude/discovery-data/contracts/**",  # 계약 인스턴스 계보
    "orchestration/adapters/claude/tests/fixtures/**",             # 테스트 픽스처 (러너 파손 위험)
    "ARCHIVE.md",                                                  # 앵커 원장
]

# 정규식에는 걸리지만 "이력 절"이 아닌 규범 본문 절 (기본 제외 · --include-ambiguous 로 편입)
# (상대경로, 헤딩 라인 정확 문자열, 사유)
AMBIGUOUS_SECTIONS = [
    (
        "docs/spec-versioning-policy.md",
        "### §3.4 Revision History 관례 (L-10 명문화)",
        "이력 절이 아니라 '이력 관례'를 규정하는 규범 본문 — 스텁이 참조하는 규범(§3) 자신이다.",
    ),
    (
        "uahf/framework/loop/loop-state-record.md",
        "## §6. 회수 이력 기록 방식 — 결정 기록 (Advisor DP-L5)",
        "이력 절이 아니라 '회수 이력 기록 방식'을 확정하는 규범 본문(DP-L5 결정 기록).",
    ),
]

# ---------------------------------------------------------------- 코어


def find_sections(lines):
    """이력 절 스팬 목록을 반환한다. [(start_idx, end_idx_exclusive, heading_text)]"""
    fenced = False
    heads = []  # (idx, level, is_history)
    for i, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = ANY_HEADING_RE.match(line)
        if not m:
            continue
        level = len(m.group(1))
        heads.append((i, level, bool(HEADING_RE.match(line))))

    spans = []
    for pos, (idx, level, is_hist) in enumerate(heads):
        if not is_hist:
            continue
        end = len(lines)
        for nidx, nlevel, _ in heads[pos + 1:]:
            if nlevel <= level:
                end = nidx
                break
        spans.append((idx, end, lines[idx].rstrip("\r\n")))
    return spans


def eol_of(line):
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return "\n"


def rewrite(lines, spans, anchor):
    """뒤에서부터 치환해 인덱스 안정성을 유지한다. 절 밖 라인은 원본 객체 그대로 재사용."""
    out = list(lines)
    stub = STUB_TEMPLATE.format(anchor=anchor)
    details = []
    for start, end, heading in reversed(spans):
        eol = eol_of(lines[start])
        orig = lines[start:end]
        # 스팬 끝이 EOF 이고 원본 마지막 줄에 개행이 없으면 그 형태를 유지한다.
        has_tail_eol = end < len(lines) or lines[end - 1].endswith("\n")
        # 절 말미 수평선 보존 (Advisor 판정 2026-07-27) — 스팬의 마지막 유의미 라인이
        # 수평선이면 절 구분선 관행을 유지한다. 재실행 시에도 같은 형태로 수렴한다(멱등).
        rule_line = None
        for cand in reversed(lines[start + 1:end]):
            if cand.strip() == "":
                continue
            if HRULE_RE.match(cand.rstrip("\r\n")):
                rule_line = cand if cand.endswith("\n") else cand + eol
            break
        if has_tail_eol:
            new = [lines[start], eol, stub + eol, eol]
            if rule_line is not None:
                new += [rule_line, eol]
        else:
            new = [lines[start], eol, stub]
            if rule_line is not None:
                new = [lines[start], eol, stub + eol, eol, rule_line.rstrip("\r\n")]
        before_b = len("".join(orig).encode("utf-8"))
        after_b = len("".join(new).encode("utf-8"))
        details.append(
            {
                "heading": heading,
                "lines_before": len(orig),
                "lines_after": len(new),
                "bytes_before": before_b,
                "bytes_after": after_b,
            }
        )
        out[start:end] = new
    details.reverse()
    return out, details


def count_table_data_rows(lines):
    """스팬 안의 표 데이터 행 수를 센다 (헤더·구분행 제외 · --check 전용).

    연속한 표 행 블록마다 구분행을 찾고, 구분행 위(헤더)와 구분행 자신을 뺀 나머지를
    데이터 행으로 센다. 구분행이 없는 블록은 표가 아니라고 보고 0으로 센다.
    """
    total = 0
    block = []

    def flush(blk):
        sep_at = next((i for i, ln in enumerate(blk) if TABLE_SEP_RE.match(ln)), None)
        if sep_at is None:
            return 0
        return len(blk) - sep_at - 1

    fenced = False
    for raw in lines:
        line = raw.rstrip("\r\n")
        if FENCE_RE.match(line):
            fenced = not fenced
            total += flush(block)
            block = []
            continue
        if fenced:
            continue
        if TABLE_ROW_RE.match(line):
            block.append(line)
        else:
            total += flush(block)
            block = []
    total += flush(block)
    return total


def run_check(root, excludes, include_ambiguous=False):
    """이력 절에 표 데이터 행이 남은 파일을 열거한다. 반환 = (라인 목록, files, rows)."""
    out = []
    n_files = n_rows = 0
    for path in sorted(p for p in root.rglob("*.md") if ".git" not in p.parts):
        rel = path.relative_to(root).as_posix()
        if match_any(rel, excludes):
            continue
        try:
            with open(path, "r", encoding="utf-8", newline="") as fh:
                lines = fh.read().splitlines(keepends=True)
        except (OSError, UnicodeDecodeError):
            continue  # fail-open — 읽히지 않는 파일은 조용히 건너뛴다
        rows = 0
        for start, end, heading in find_sections(lines):
            if not include_ambiguous and any(
                a[0] == rel and a[1] == heading for a in AMBIGUOUS_SECTIONS
            ):
                continue
            rows += count_table_data_rows(lines[start:end])
        if rows > 0:
            n_files += 1
            n_rows += rows
            out.append("REACCUM {} rows={}".format(rel, rows))
    if out:
        out.append("TOTAL files={} rows={}".format(n_files, n_rows))
    return out, n_files, n_rows


def match_any(relpath, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(relpath, pat):
            return pat
        if pat.endswith("/**") and (relpath == pat[:-3] or relpath.startswith(pat[:-2])):
            return pat
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="문서 이력 절을 git 포인터 스텁으로 축약한다.")
    ap.add_argument("--anchor", default=None, help="제거 전 전문 git 앵커 해시 (--check 외 필수)")
    ap.add_argument("--root", default=None, help="대상 루트 (기본 = 리포 루트)")
    ap.add_argument("--exclude", action="append", default=[], help="추가 제외 glob (반복 가능)")
    ap.add_argument("--include-ambiguous", action="store_true",
                    help="규범 본문으로 분류된 모호 절도 대상에 포함한다")
    ap.add_argument("--report", default=None, help="보고를 파일로도 기록할 경로")
    ap.add_argument("--apply", action="store_true", help="실제 파일에 기록 (없으면 dry-run)")
    ap.add_argument("--check", action="store_true",
                    help="재퇴적 감시 모드 — 이력 절에 표 데이터 행이 남은 파일만 열거한다")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[2]
    excludes = DEFAULT_EXCLUDES + list(args.exclude)

    # --check 는 dry-run/apply 와 완전히 분리된 조기 반환 경로다(기존 출력 무영향).
    if args.check:
        lines_out, _f, _r = run_check(root, excludes, args.include_ambiguous)
        for ln in lines_out:
            sys.stdout.write(ln + "\n")
        return 0  # 가드 fail-open — 판정은 종료 코드가 아니라 출력 유무로 한다

    if not args.anchor:
        ap.error("--anchor 는 --check 모드가 아니면 필수다")

    buf = io.StringIO()

    def emit(s=""):
        buf.write(s + "\n")

    emit("# history_compact — {} (anchor={})".format("APPLY" if args.apply else "DRY-RUN", args.anchor))
    emit("root: {}".format(root))
    emit("excludes: {}".format(", ".join(excludes)))
    emit("")

    files = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)

    n_files = n_sections = 0
    tot_before = tot_after = tot_lines_removed = 0
    skipped = []
    ambiguous_hits = []
    watch_hits = []

    for path in files:
        rel = path.relative_to(root).as_posix()
        pat = match_any(rel, excludes)
        if pat:
            skipped.append((rel, "exclude:{}".format(pat)))
            continue

        with open(path, "r", encoding="utf-8", newline="") as fh:
            text = fh.read()
        lines = text.splitlines(keepends=True)
        spans = find_sections(lines)
        wpat = match_any(rel, WATCH_PATTERNS)
        if wpat and spans:
            for _s, _e, _h in spans:
                watch_hits.append((rel, _h, wpat))
        if not spans:
            continue

        kept = []
        for start, end, heading in spans:
            amb = next((a for a in AMBIGUOUS_SECTIONS if a[0] == rel and a[1] == heading), None)
            if amb and not args.include_ambiguous:
                ambiguous_hits.append((rel, heading, amb[2]))
                continue
            kept.append((start, end, heading))
        if not kept:
            continue

        new_lines, details = rewrite(lines, kept, args.anchor)
        new_text = "".join(new_lines)

        n_files += 1
        emit("## {}".format(rel))
        for d in details:
            n_sections += 1
            tot_before += d["bytes_before"]
            tot_after += d["bytes_after"]
            tot_lines_removed += d["lines_before"] - d["lines_after"]
            emit("   - heading : {}".format(d["heading"]))
            emit("     lines   : {} -> {} (removed {})".format(
                d["lines_before"], d["lines_after"], d["lines_before"] - d["lines_after"]))
            emit("     bytes   : {} -> {} (saved {})".format(
                d["bytes_before"], d["bytes_after"], d["bytes_before"] - d["bytes_after"]))
        emit("     file    : {} -> {} bytes".format(
            len(text.encode("utf-8")), len(new_text.encode("utf-8"))))

        if args.apply and new_text != text:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new_text)

    emit("")
    emit("## SKIPPED (제외 목록 매칭): {}건".format(len(skipped)))
    for rel, why in skipped:
        emit("   - {}  [{}]".format(rel, why))

    emit("")
    emit("## WATCH (종전 제외 후보 경로 — 현재 대상에 포함됨)")
    for pat in WATCH_PATTERNS:
        hits = [h for h in watch_hits if h[2] == pat]
        if not hits:
            emit("   - {} : 매칭 없음 (이력 절 탐지 0)".format(pat))
        else:
            emit("   - {} : {}건 탐지".format(pat, len(hits)))
            for rel, heading, _ in hits:
                emit("       {} :: {}".format(rel, heading))

    emit("")
    emit("## AMBIGUOUS (규범 본문 — 기본 제외): {}건".format(len(ambiguous_hits)))
    for rel, heading, why in ambiguous_hits:
        emit("   - {} :: {}".format(rel, heading))
        emit("     사유: {}".format(why))
    stale = [a for a in AMBIGUOUS_SECTIONS
             if not any(h[0] == a[0] and h[1] == a[1] for h in ambiguous_hits)]
    if stale:
        emit("   ! STALE 등재 {}건 (대상 헤딩이 현재 리포에 없음 — 목록 갱신 필요)".format(len(stale)))
        for rel, heading, _why in stale:
            emit("     - {} :: {}".format(rel, heading))

    emit("")
    emit("## TOTAL")
    emit("   files              : {}".format(n_files))
    emit("   sections           : {}".format(n_sections))
    emit("   lines removed      : {}".format(tot_lines_removed))
    emit("   section bytes      : {} -> {} (saved {})".format(
        tot_before, tot_after, tot_before - tot_after))
    emit("   mode               : {}".format("APPLY (파일 기록됨)" if args.apply else "DRY-RUN (무변경)"))

    out = buf.getvalue()
    sys.stdout.write(out)
    if args.report:
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        with open(rp, "w", encoding="utf-8", newline="") as fh:
            fh.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
