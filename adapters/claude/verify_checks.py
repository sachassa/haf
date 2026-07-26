#!/usr/bin/env python3
"""verify_checks — Verifier 결정적 검증 슬라이스 실행기 (형태 B·LLM 0·순수 관측).

무엇을 하는가:
  UAF-level 거버넌스 에이전트 Verifier(`.claude/agents/verifier.md`)의 검증 유형 중 **결정적으로
  기계화 가능한 두 슬라이스**를 결정적 실행 스크립트로 물리화한다. 이는 verifier.md 의 VT 계약(형태
  A: 주 세션 규약 절차)을 결정적 실행(form-B)으로 승격한 것이며, entry/adapters/claude/entry_resolve.py
  와 동형이다(ARCHITECTURE.md §5 "UAF-level 거버넌스 form-B 스크립트의 물리 홈 = 저장소 루트
  adapters/claude/"). 이 스크립트는 config 가 아니라 실행 스크립트이므로 루트 `.claude/`(설정 디렉터리)
  가 아닌 저장소 루트 `adapters/claude/` 에 둔다.

  구현하는 슬라이스:
    VT-1 산출물 존재 검증 — 입력으로 받은 "기대 산출물 경로 집합" 각각의 존재/부재를 결정적으로 판정
                            (uahf/specs/06-verifier.md §3.2-E VT-1: "모든 지정 산출물이 존재").
    VT-4 경계 검증(전수 스캔) — 입력으로 받은 "금지/경계 패턴 집합"과 "스캔 범위(경로/글롭)"에 대해,
                            각 패턴의 **모든** 매치를 file:line(:col)과 함께 **전수(exhaustive)** 수집
                            (uahf/specs/06-verifier.md §3.2-E VT-4: "금지 요소를 전수 스캔(exhaustive
                            scan)한다" / 충족 조건 "금지 요소 0건" — 판정의 근거가
                            되는 전수 매치 목록을 결정적으로 산출. 전수성은 어떤 이유로도 완화하지 않는다).

무엇을 하지 않는가(결정적 슬라이스 경계 — verifier.md·AGENT.md §Verification & Gate):
  - **verdict(통과/실패/조건부)를 내리지 않는다.** VT-1 은 존재/부재 사실만, VT-4 는 매치 목록·카운트만
    방출한다. "모든 산출물이 존재하는가", "금지 요소 0건인가"의 최종 판정(Met/Violated/Undetermined,
    final_verdict)은 Verifier LLM 몫이다(verifier.md §출력 "판정 값과 최종 판정 도출 (결정적)" ·
    정본 06 §3.2-C). 이 스크립트는 그 판정의
    결정적·재현 가능한 **근거(evidence)** 만 제공해, LLM 이 애매 잔여만 판정하도록 한다.
  - **원문 라인을 덤프하지 않는다.** 매치는 file:line:col + 매칭 substring(truncate)만 담는다. 산출물
    본문을 그대로 실어 나르지 않는다(토큰 위생·AGENT.md §Core Principles).
  - Memory·Architecture·Spec 을 해석하지 않는다. 순수 파일시스템 관측이다.

결정성(AGENT.md §Verification & Gate — 같은 입력 → 같은 출력):
  - VT-1 결과는 입력 경로 순서를 보존해 방출한다(입력 결정 → 출력 결정).
  - VT-4 스캔 파일 집합은 중복 제거 후 정렬(sorted)해 순회한다. 매치는 (파일순, 라인순, 열순)으로 정렬된다.
  - 파일시스템 상태가 동일하면 출력은 바이트 동일하다.

VT-4 전수성 보장과 그 한계(정직한 scope 명시 — verifier.md §출력 verifier_scope·VT-4 주의):
  - 스캔한 각 텍스트 파일 **안에서는** 각 패턴의 모든 발생을 (라인·열) 단위로 빠짐없이 수집한다. 한 라인에
    여러 번 나오면 각각을 별개 매치로 센다(라인 단위 축약 금지 — 거짓 저카운트 방지).
  - 스캔 단위는 **라인**이다. 따라서 여러 라인에 걸친(multiline) 패턴은 이 스크립트가 잡지 않는다(설계 제약).
    그런 경계는 형태 A(Verifier LLM) 소관으로 남긴다.
  - 텍스트로 디코드할 수 없는 파일(널바이트 포함 바이너리·비 UTF-8)은 스캔하지 않고 `filesSkipped` 에
    사유와 함께 **명시**한다. 이는 누락 은폐가 아니라 검사 못한 범위의 정직한 노출이다 — Verifier 는 이를
    보고 해당 경계를 Undetermined 로 판정할 수 있다(verifier.md §판정 값·evidence_gap).

Compact 출력 포맷(기계가독 JSON·stdout — Verifier LLM 소비용):
  {
    "root": "<상대경로 기준 디렉터리>",
    "vt1": {                                  # --artifact / stdin.vt1.artifacts 가 있을 때만
      "checked": <int>,                       # 검사한 경로 수
      "results": [ {"path","exists","type"} ],# type = "file"|"dir"|"other"|null(부재)
      "present": ["<path>", ...],             # 존재하는 경로(입력 순)
      "absent":  ["<path>", ...]              # 부재 경로(입력 순)
    },
    "vt4": {                                  # --pattern 이 있을 때만
      "scanScope": ["<glob|dir|file>", ...],  # 요청한 스캔 범위(입력 순)
      "filesScanned": <int>,                  # 실제 스캔한 텍스트 파일 수
      "filesSkipped": [ {"file","reason"} ],  # 스캔 못한 파일(binary|non-utf8|unreadable)
      "patterns": [ {                         # 요청한 패턴별(입력 순) — 매치 0건도 포함
        "pattern": "<regex>",
        "count": <int>,                       # 이 패턴의 전수 매치 수
        "matches": [ {"file","line","col","match"} ]  # match = 매칭 substring(truncate)
      } ],
      "totalMatches": <int>                   # 전 패턴 매치 합
    }
  }
  vt1·vt4 는 해당 입력이 주어졌을 때만 키로 존재한다(빈 입력 → 해당 키 없음).

사용법:
  # VT-1 만:
  python verify_checks.py --artifact path/a --artifact path/b [--root DIR]
  # VT-4 만:
  python verify_checks.py --pattern "TODO" --pattern "FIXME" --scan "src/**/*.py" --scan docs [--root DIR]
  # 둘 다 + stdin JSON:
  echo '{"vt1":{"artifacts":[...]},"vt4":{"patterns":[...],"scan":[...]}}' | python verify_checks.py --stdin
  # --root 는 상대 경로·글롭의 기준 디렉터리(기본 = 현재 작업 디렉터리).
  # --scan 항목: glob 메타문자(* ? [)가 있으면 <root> 기준 glob(** 재귀 지원), 없으면 경로
  #   (파일이면 그 파일, 디렉터리면 재귀 전체). 스캔 범위가 없으면 VT-4 는 파일 0개(빈 결과).

종료 코드:
  0 = 검사 수행 성공(매치 유무·존재 유무 무관 — 이것은 verdict 가 아니라 관측 결과다).
  2 = 사용법 오류(입력 없음·argparse).
  3 = 잘못된 정규식 패턴(재해석 금지·임의 우회 금지 → 오류로 에스컬레이션).

원칙(불변):
  - 순수 판독. 스캔 대상·산출물을 일절 수정하지 않는다(파일·디렉터리 생성 0).
  - 결정성. 같은 입력·같은 파일시스템 → 같은 출력.
  - python 3 stdlib 만(외부 패키지 0 — entry 선례 동형).
  - 재정의 0. verifier.md 의 VT 계약·판정 규칙을 재정의하지 않는다. verdict 는 내지 않는다.

이 스크립트는 저장소 루트 adapters/claude/ 경계 소속이다(UAF-level 거버넌스 form-B 스크립트의 물리 홈).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(비ASCII stdout) — entry 선례 동형 -----------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

# 매칭 substring 최대 길이 — 원문 덤프 방지(긴 정규식 매치 truncate).
MAX_MATCH_TEXT = 200
# glob 메타문자 — 스캔 범위 항목이 glob 인지 경로인지 판별.
_GLOB_META = ("*", "?", "[")


class PatternError(Exception):
    """잘못된 정규식 패턴 — §종료코드 3(재해석 금지·오류 에스컬레이션)."""


# ==========================================================================
# VT-1 산출물 존재 검증 — 경로 집합 각각의 존재/부재를 결정적 판정(순수 판독)
# ==========================================================================
def _path_type(p: Path) -> str:
    if p.is_file():
        return "file"
    if p.is_dir():
        return "dir"
    return "other"  # 심볼릭 링크·특수 파일 등 — 존재하지만 file/dir 아님.


def check_artifacts(paths: list[str], root: Path) -> dict:
    """입력 경로 각각의 존재/부재를 판정한다. 입력 순서를 보존한다(결정성).
    verdict('모두 존재하는가')는 내지 않는다 — 존재/부재 사실만 방출(Verifier LLM 몫)."""
    results: list[dict] = []
    present: list[str] = []
    absent: list[str] = []
    for raw in paths:
        p = (root / raw) if not Path(raw).is_absolute() else Path(raw)
        exists = p.exists()
        results.append({
            "path": raw,
            "exists": exists,
            "type": _path_type(p) if exists else None,
        })
        (present if exists else absent).append(raw)
    return {
        "checked": len(paths),
        "results": results,
        "present": present,
        "absent": absent,
    }


# ==========================================================================
# VT-4 경계 검증 — 스캔 범위 해소 + 패턴별 전수 매치 수집(exhaustive)
# ==========================================================================
def resolve_scan_files(scan: list[str], root: Path) -> list[Path]:
    """스캔 범위 항목들을 실제 파일 목록으로 해소한다. 중복 제거 후 정렬(결정성).
      - glob 메타문자 포함 → <root> 기준 glob(** 재귀 지원).
      - 그 외 → 경로: 파일이면 그 파일, 디렉터리면 재귀 전체(rglob), 부재면 무시.
    디렉터리는 파일 자체가 아니므로 결과에서 제외(파일만 스캔 대상)."""
    collected: set[Path] = set()
    for item in scan:
        base = Path(item)
        is_glob = any(meta in item for meta in _GLOB_META)
        if is_glob:
            anchor = root if not base.is_absolute() else Path(base.anchor)
            pattern = item if not base.is_absolute() else str(base.relative_to(base.anchor))
            for m in anchor.glob(pattern):
                if m.is_file():
                    collected.add(m)
        else:
            target = base if base.is_absolute() else (root / item)
            if target.is_file():
                collected.add(target)
            elif target.is_dir():
                for m in target.rglob("*"):
                    if m.is_file():
                        collected.add(m)
            # 부재 경로는 조용히 무시(스캔 대상 아님) — 존재 검증은 VT-1 소관.
    return sorted(collected)


def read_text_or_reason(path: Path) -> tuple[str | None, str | None]:
    """파일을 텍스트로 읽는다. 실패 시 (None, 사유). 사유 = binary|non-utf8|unreadable.
    스캔 못한 파일은 filesSkipped 로 정직하게 노출한다(누락 은폐 금지·scope 명시)."""
    try:
        data = path.read_bytes()
    except OSError:
        return None, "unreadable"
    if b"\x00" in data:
        return None, "binary"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, "non-utf8"


def scan_patterns(patterns: list[str], scan: list[str], root: Path) -> dict:
    """각 패턴의 모든 매치를 스캔 파일 전수에서 (file, line, col) 단위로 수집한다.
    한 라인 다중 매치도 각각 개별 카운트(라인 축약 금지). verdict 는 내지 않는다."""
    # 패턴 컴파일 — 실패는 오류로 에스컬레이션(재해석 금지).
    compiled: list[tuple[str, re.Pattern]] = []
    for pat in patterns:
        try:
            compiled.append((pat, re.compile(pat)))
        except re.error as exc:
            raise PatternError("잘못된 정규식 패턴 %r: %s" % (pat, exc)) from exc

    files = resolve_scan_files(scan, root)

    # 파일 텍스트를 1회 읽어 재사용(패턴 수 × 파일 수 재읽기 방지). 스캔 못한 파일은 기록.
    files_skipped: list[dict] = []
    texts: list[tuple[str, list[str]]] = []  # (표시경로, 라인목록)
    for f in files:
        text, reason = read_text_or_reason(f)
        display = _display_path(f, root)
        if text is None:
            files_skipped.append({"file": display, "reason": reason})
            continue
        # split("\n") — 라인 번호 1-base 기준. \r\n 의 \r 은 라인 끝에 남아 매치·열 계산 무영향.
        texts.append((display, text.split("\n")))

    pattern_reports: list[dict] = []
    total = 0
    for pat, rx in compiled:
        matches: list[dict] = []
        for display, lines in texts:  # texts 는 이미 정렬된 files 순서.
            for lineno, line in enumerate(lines, start=1):
                for m in rx.finditer(line):
                    snippet = m.group(0)
                    if len(snippet) > MAX_MATCH_TEXT:
                        snippet = snippet[:MAX_MATCH_TEXT] + "…"
                    matches.append({
                        "file": display,
                        "line": lineno,
                        "col": m.start() + 1,  # 1-base 열.
                        "match": snippet,
                    })
        pattern_reports.append({"pattern": pat, "count": len(matches), "matches": matches})
        total += len(matches)

    return {
        "scanScope": list(scan),
        "filesScanned": len(texts),
        "filesSkipped": files_skipped,
        "patterns": pattern_reports,
        "totalMatches": total,
    }


def _display_path(p: Path, root: Path) -> str:
    """가능하면 root 기준 상대 POSIX 경로로 표시(결정적·플랫폼 독립). 밖이면 절대경로."""
    try:
        return p.resolve().relative_to(root.resolve()).as_posix()
    except (ValueError, OSError):
        return p.as_posix()


# ==========================================================================
# 오케스트레이션
# ==========================================================================
def run_checks(artifacts: list[str] | None, patterns: list[str] | None,
               scan: list[str] | None, root: Path) -> dict:
    out: dict = {"root": str(root)}
    if artifacts:
        out["vt1"] = check_artifacts(artifacts, root)
    if patterns:
        out["vt4"] = scan_patterns(patterns, scan or [], root)
    return out


# ==========================================================================
# CLI
# ==========================================================================
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verifier 결정적 검증 슬라이스(VT-1 산출물 존재·VT-4 경계 전수 스캔). "
                    "verdict 는 내지 않는다 — 관측 근거만 방출(verifier.md 재정의 0).")
    parser.add_argument("--artifact", action="append", default=[], metavar="PATH",
                        help="VT-1 기대 산출물 경로(반복 지정). 존재/부재를 판정한다.")
    parser.add_argument("--pattern", action="append", default=[], metavar="REGEX",
                        help="VT-4 금지/경계 정규식 패턴(반복 지정). 각 패턴의 전수 매치를 수집.")
    parser.add_argument("--scan", action="append", default=[], metavar="GLOB|PATH",
                        help="VT-4 스캔 범위(반복 지정). glob(* ? [) 또는 경로/디렉터리(재귀).")
    parser.add_argument("--root", default=".",
                        help="상대 경로·글롭의 기준 디렉터리(기본 = 현재 작업 디렉터리).")
    parser.add_argument("--stdin", action="store_true",
                        help="stdin 에서 JSON {vt1:{artifacts},vt4:{patterns,scan}} 을 읽어 병합한다.")
    parser.add_argument("--indent", type=int, default=2, help="JSON 들여쓰기(기본 2).")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    artifacts = list(args.artifact)
    patterns = list(args.pattern)
    scan = list(args.scan)

    if args.stdin:
        try:
            payload = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            print("사용법 오류: --stdin JSON 파싱 실패: %s" % exc, file=sys.stderr)
            return 2
        vt1 = payload.get("vt1") or {}
        vt4 = payload.get("vt4") or {}
        artifacts += list(vt1.get("artifacts") or [])
        patterns += list(vt4.get("patterns") or [])
        scan += list(vt4.get("scan") or [])

    if not artifacts and not patterns:
        print("사용법 오류: --artifact 또는 --pattern 중 최소 하나가 필요하다(또는 --stdin JSON).",
              file=sys.stderr)
        return 2

    root = Path(args.root)

    try:
        result = run_checks(artifacts, patterns, scan, root)
    except PatternError as exc:
        print("[BAD-PATTERN] %s" % exc, file=sys.stderr)
        return 3

    json.dump(result, sys.stdout, ensure_ascii=False, indent=args.indent)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
