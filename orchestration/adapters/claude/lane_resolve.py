#!/usr/bin/env python3
"""lane_resolve — 절차 레인 판별 결정적 로더 (형태 B·LLM 0·순수 판독·계산·방출까지만).

무엇을 하는가:
  절차 비례화 트랙의 **레인 판별식**(docs/proportionality-track-ledger.md §2.1)을 결정적 실행
  스크립트로 물리화한다. 선언된 대상 집합(declaredTargets)과 선택적 사용자 override 를 입력받아
  lane("standard"|"lightweight") + 판정 근거 + 사유 기록 요구 여부를 구조화 JSON 으로 stdout 에
  방출한다. 이 스크립트는 `entry_resolve.py`·`solution_design_resolve.py`·`design_completeness.py`
  와 **동일 성격**이다 — LLM 0·결정적·오프라인 안전·순수 판독·계산해서 방출까지만(실행 안 함).

  **적용하지 않는다(경계 — 원장 §2.2 (i)·constraints).** 레인을 *계산*할 뿐 *적용*하지 않는다:
  policy 시드·위임 발부·게이트 해소·마커 파일 기입을 일절 수행하지 않는다(파일시스템 쓰기 0).
  적용은 주 세션 form-A 소관이며, 그 물리 산출물이 레인 마커(.claude/lane.json — 레지스트리
  marker 절)다. 로더가 무엇이든 쓰면 경계 위반이다.

판별식(원장 §2.1 — 재정의 0):
  override != null                      -> override      (사유 원장 기록 필수)
  declaredTargets == null | 공집합      -> standard       (fail-closed)
  any(t in declaredTargets: touches(t)) -> standard
  else                                  -> lightweight

  touches(t) 는 경로 패턴 집합에 대한 순수 술어다. 패턴 집합·레인 어휘·fail-closed 귀결값·사유
  필드명은 전부 데이터(lane-registry.json)에 있고 이 코드는 소비만 한다(Policy as Data 단일 소스).
  패턴 매칭 불가(루트 기준 상대화 실패) 대상도 fail-closed 로 standard 에 귀결한다(§2.2 (i)
  "선언 부재·패턴 매칭 불가 → standard").

사용법:
  python lane_resolve.py --target <경로> [--target <경로> ...]
                         [--override {standard|lightweight}] [--override-reason <사유>]
                         [--root <레인 워크스페이스 루트>] [--registry <path>] [--indent N]
  python lane_resolve.py --stdin      # stdin JSON {declaredTargets:[...], override?, laneOverrideReason?}
  # --root 미지정 시 기본 = 이 스크립트가 속한 리포 루트(<root>/orchestration/adapters/claude 의 3단 상위).
  #   접점 패턴은 이 루트 기준 상대 POSIX 경로에 대해 판정된다(훅 측 기준 = 마커 디렉터리 W).

종료 코드:
  0 = 판정 성공(lane 방출).
  2 = 사용법 오류(argparse).
  3 = override 지정 + 사유 부재(사유 기록 요구 미충족 — 임의 해석 금지·음성 대조 지점).
  4 = 무효 Registry(부재·손상·어휘 불일치·패턴 결손).

원칙(불변):
  - 순수 판독. 파일·디렉터리를 생성·수정하지 않는다. 네트워크 0. LLM·서브에이전트 호출 0.
  - Policy as Data 단일 소스. 접점 패턴 문자열을 이 코드에 두지 않는다(전부 lane-registry.json).
  - 결정적. 같은 입력(인자·레지스트리) → byte 동일 출력(시각·난수·환경 의존 값 0).
  - python 3 stdlib 만(외부 패키지 0).

이 스크립트는 orchestration/adapters/claude/ 경계 소속이다(Q-3 확정 배치 — 게이트·강제 계열 동거).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(비ASCII stdout/stderr) — entry_resolve 선례 동형 ---------------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE / "lane-registry.json"
# <repo root>/orchestration/adapters/claude/<이 파일> → 3단 상위가 리포 루트.
# (등재 접점 패턴과 문자 동일한 경로 리터럴을 코드에 두지 않는다 — done 8 판정 오염 방지.)
DEFAULT_ROOT = HERE.parents[2]

# 원장 §2.3 정본 레인 어휘 — Registry 선언과 대조 검증한다(하드코딩이 아니라 동기화 확인.
# entry_resolve 의 EXPECTED_VALUE_DOMAIN 유/무 대조 선례 동형).
LANE_STANDARD = "standard"
LANE_LIGHTWEIGHT = "lightweight"
EXPECTED_LANE_VOCABULARY = (LANE_STANDARD, LANE_LIGHTWEIGHT)


class RegistryError(Exception):
    """Registry 무결성 위반 — 판정 불가(임의 해석 금지)."""


class OverrideReasonMissing(Exception):
    """override 지정 + 사유 부재 — 사유 기록 요구 미충족."""


# ==========================================================================
# Registry 적재 + 무결성 검증
# ==========================================================================
def load_registry(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        reg = json.load(fh)
    verify_registry(reg)
    return reg


def verify_registry(reg: dict) -> None:
    """레인 어휘 2값 고정·fail-closed 귀결값·사유 필드명·마커 경로·접점 패턴 결손을 대조한다.
    위반 Registry 는 무효다(판정 불가 — 관성 통과 방지)."""
    problems: list[str] = []

    vocab = reg.get("laneVocabulary")
    if not isinstance(vocab, list) or tuple(vocab) != EXPECTED_LANE_VOCABULARY:
        problems.append(
            "laneVocabulary %r 이 정본 2값 %r 과 불일치(세 번째 값 금지·§2.3)"
            % (vocab, list(EXPECTED_LANE_VOCABULARY)))

    fail_closed = reg.get("failClosedLane")
    if fail_closed != LANE_STANDARD:
        problems.append("failClosedLane %r 이 안전측 귀결값 %r 과 불일치(§2.3)"
                        % (fail_closed, LANE_STANDARD))

    reason_field = reg.get("overrideReasonField")
    if not isinstance(reason_field, str) or not reason_field.strip():
        problems.append("overrideReasonField 부재·비문자열: %r" % (reason_field,))

    marker = reg.get("marker")
    marker_rel = marker.get("relativePath") if isinstance(marker, dict) else None
    if not isinstance(marker_rel, str) or not marker_rel.strip():
        problems.append("marker.relativePath 부재·비문자열: %r" % (marker_rel,))
    if isinstance(marker, dict) and marker.get("enforcedLane") not in EXPECTED_LANE_VOCABULARY:
        problems.append("marker.enforcedLane %r 이 레인 어휘 밖" % (marker.get("enforcedLane"),))

    classes = reg.get("touchpointClasses")
    if not isinstance(classes, list) or not classes:
        problems.append("touchpointClasses 부재·공집합(접점 술어 판정 불가)")
    else:
        for idx, cls in enumerate(classes):
            if not isinstance(cls, dict):
                problems.append("touchpointClasses[%d] 가 객체가 아님" % idx)
                continue
            name = cls.get("class")
            if not isinstance(name, str) or not name.strip():
                problems.append("touchpointClasses[%d].class 부재·비문자열" % idx)
            pats = cls.get("patterns")
            if not isinstance(pats, list) or not pats:
                problems.append("접점 클래스 %r 의 patterns 부재·공집합" % (name,))
                continue
            for p in pats:
                if not isinstance(p, str) or not p.strip():
                    problems.append("접점 클래스 %r 에 비문자열·공백 패턴: %r" % (name, p))

    if problems:
        raise RegistryError("Registry 무결성 위반:\n  - " + "\n  - ".join(problems))


# ==========================================================================
# touches(t) — 경로 패턴 순수 술어(패턴은 데이터·문법만 코드)
# ==========================================================================
def _glob_to_regex(pattern: str) -> str:
    """glob 패턴을 full-match 정규식으로 변환한다(레지스트리 _patternSyntax 문법).

    `**/` = 0개 이상 세그먼트 · `**` = 구분자 포함 임의 문자 · `*` = 세그먼트 내 임의 문자 ·
    `?` = 세그먼트 내 한 문자 · 그 밖 = 리터럴. fnmatch 는 `*` 가 구분자를 넘어 매칭하므로
    쓰지 않는다(세그먼트 경계 보존을 위해 직접 변환).
    """
    out: list[str] = []
    i = 0
    n = len(pattern)
    star = "*"
    while i < n:
        ch = pattern[i]
        if ch == star:
            if pattern.startswith(star * 2, i):
                if pattern.startswith(star * 2 + "/", i):
                    out.append("(?:[^/]+/)*")
                    i += 3
                else:
                    out.append(".*")
                    i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif ch == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(ch))
            i += 1
    return "".join(out)


def _relative_posix(target: Path, root: Path):
    """대상을 루트 기준 상대 POSIX 경로로 변환. 루트 밖·상대화 실패면 None(패턴 매칭 불가)."""
    try:
        return target.relative_to(root).as_posix()
    except ValueError:
        return None


def classify_target(raw: str, root: Path, classes: list) -> dict:
    """단일 대상의 접점 판정 레코드를 만든다(순수 함수·파일시스템 존재 여부 무관).

    파일 존재를 요구하지 않는다 — 판정 대상은 *선언*이므로 미생성 파일도 판정 가능해야 한다.
    """
    p = Path(raw)
    target = p if p.is_absolute() else (root / p)
    # 정규화(.. 해소). resolve 는 미존재 경로도 안전 처리(strict=False 기본).
    target = target.resolve()
    rel = _relative_posix(target, root)

    record = {
        "target": raw,
        "relative": rel,
        "resolvable": rel is not None,
        "touched": False,
        "matchedClass": None,
        "matchedPattern": None,
    }
    if rel is None:
        return record  # 패턴 매칭 불가 → fail-closed 사유(호출자가 집계).

    for cls in classes:
        for pat in cls["patterns"]:
            if re.fullmatch(_glob_to_regex(pat), rel):
                record["touched"] = True
                record["matchedClass"] = cls["class"]
                record["matchedPattern"] = pat
                return record  # 최초 적중에서 멈춘다(등재 순서 = 결정적).
    return record


def touches(raw: str, root: Path, reg: dict) -> bool:
    """원장 §2.1 touches(t) 술어 — 접점 적중 또는 패턴 매칭 불가(fail-closed)면 True."""
    rec = classify_target(raw, root, reg["touchpointClasses"])
    return bool(rec["touched"]) or not rec["resolvable"]


# ==========================================================================
# 판별식(§2.1)
# ==========================================================================
def resolve_lane(reg: dict, declared_targets, root: Path,
                 override=None, override_reason=None) -> dict:
    classes = reg["touchpointClasses"]
    reason_field = reg["overrideReasonField"]
    fail_closed = reg["failClosedLane"]

    targets = list(declared_targets or [])
    records = [classify_target(t, root, classes) for t in targets]
    touched = [r for r in records if r["touched"]]
    unresolvable = [r for r in records if not r["resolvable"]]

    if override is not None:
        if override not in reg["laneVocabulary"]:
            raise RegistryError("override %r 이 레인 어휘 %r 밖(세 번째 값 금지)"
                                % (override, reg["laneVocabulary"]))
        if not isinstance(override_reason, str) or not override_reason.strip():
            raise OverrideReasonMissing(
                "override=%r 지정 시 %s(사유)는 필수다 — 사유 없는 override 는 원장 기록 요구를 "
                "충족하지 못한다(원장 §2.1 '사유 원장 기록 필수')" % (override, reason_field))
        lane = override
        basis = "override"
    elif not targets:
        lane = fail_closed
        basis = "fail-closed:no-declared-targets"
    elif touched:
        lane = fail_closed
        basis = "touchpoint-match"
    elif unresolvable:
        lane = fail_closed
        basis = "fail-closed:unresolvable-target"
    else:
        lane = LANE_LIGHTWEIGHT
        basis = "no-touchpoint"

    result = {
        "lane": lane,
        "basis": basis,
        "root": root.as_posix(),
        "declaredTargets": records,
        "touchedCount": len(touched),
        "unresolvableCount": len(unresolvable),
        "override": override,
        # 사유 기록 요구 플래그 — override 로 확정된 레인은 사유를 원장에 기록해야 한다.
        "laneOverrideReasonRequired": override is not None,
        reason_field: override_reason if override is not None else None,
        "markerScaffold": {
            "_note": ("주 세션(form-A)이 이 골격을 마커 경로(%s)에 물리화한다. 로더는 쓰지 않는다 — "
                      "decidedAt 은 결정성 보존을 위해 방출하지 않으며 기입 시점에 주 세션이 채운다."
                      % reg["marker"]["relativePath"]),
            "path": reg["marker"]["relativePath"],
            "lane": lane,
            reason_field: override_reason if override is not None else None,
            "declaredTargets": targets,
        },
        "_note": ("lane·basis = 원장 §2.1 판별식의 투영(재정의 0). 접점 패턴·레인 어휘·사유 필드명은 "
                  "lane-registry.json 데이터이며 이 코드에 사본이 없다(Policy as Data 단일 소스). "
                  "로더는 여기서 멈춘다 — 레인 적용(policy 시드·위임 발부·게이트 해소·마커 기입) 0."),
    }
    return result


# ==========================================================================
# CLI
# ==========================================================================
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="절차 레인 판별 결정적 로더(형태 B·LLM 0·순수 판독·원장 §2.1 재정의 0)")
    parser.add_argument("--target", action="append", default=[], metavar="PATH",
                        help="선언 대상 경로(반복 지정 가능). 루트 기준 상대 또는 절대경로.")
    parser.add_argument("--override", choices=list(EXPECTED_LANE_VOCABULARY), default=None,
                        help="사용자 override 레인(양방향). 지정 시 --override-reason 필수.")
    parser.add_argument("--override-reason", default=None, metavar="TEXT",
                        help="override 사유(원장 기록 대상). override 지정 시 필수.")
    parser.add_argument("--root", default=str(DEFAULT_ROOT),
                        help="접점 패턴 상대 기준 루트(기본 = 이 스크립트가 속한 리포 루트).")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                        help="레인 레지스트리 데이터 파일(기본 = 이 스크립트 옆 lane-registry.json).")
    parser.add_argument("--stdin", action="store_true",
                        help="stdin 에서 JSON {declaredTargets, override?, laneOverrideReason?} 을 읽는다.")
    parser.add_argument("--indent", type=int, default=2, help="JSON 들여쓰기(기본 2).")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    targets = list(args.target)
    override = args.override
    reason = args.override_reason
    if args.stdin:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            print("사용법 오류: --stdin JSON 최상위는 객체여야 한다.", file=sys.stderr)
            return 2
        targets = list(payload.get("declaredTargets") or targets)
        override = payload.get("override", override)
        reason = payload.get("laneOverrideReason", reason)

    try:
        reg = load_registry(Path(args.registry))
    except RegistryError as exc:
        print("[REGISTRY-INVALID] %s" % exc, file=sys.stderr)
        return 4
    except (OSError, json.JSONDecodeError) as exc:
        print("[REGISTRY-UNREADABLE] %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 4

    root = Path(args.root).resolve()
    try:
        result = resolve_lane(reg, targets, root, override=override, override_reason=reason)
    except OverrideReasonMissing as exc:
        print("[OVERRIDE-REASON-MISSING] %s" % exc, file=sys.stderr)
        return 3
    except RegistryError as exc:
        print("[REGISTRY-INVALID] %s" % exc, file=sys.stderr)
        return 4

    json.dump(result, sys.stdout, ensure_ascii=False, indent=args.indent)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
