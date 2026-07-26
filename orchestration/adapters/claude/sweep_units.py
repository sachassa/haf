"""횡단 결함 스윕 도구 (F6·백로그 §M D-M2 ②) — 단위 경계별 패턴 스캔(form-B·LLM 0).

CP2 재작업은 그 단위만의 결함 신호가 아니다 — 같은 API 오용·같은 잘못된 관례가 동료 단위에
복제돼 있어도 각 단위의 done AC 는 자기 산출만 보므로 통과한다. 이 도구는 사람/Advisor 가
**패턴을 정해** 넘기면 현재 그래프의 **모든 단위 경계(ownedBoundary)** 를 같은 기준으로 훑어
어느 단위가 그 패턴을 갖고 있는지 `file:line` 으로 보고한다(런처 `[REWORK-NOTE]` 의 짝).

경계·불변(무엇을 하지 않는가):
  - **판단 0.** 어떤 패턴이 결함인지, 적중을 어떻게 조치할지는 전부 사람/Advisor 소유다
    (PO-INV 1 — 엔진·도구는 기계 파생·기계 스캔만 한다). 이 도구는 자동 수정·자동 되돌림을
    하지 않는다(D-M3 미도입 결정).
  - **쓰기 0(사전 검사로 보장).** 워크스페이스도 run 원장도 읽기만 한다. 조립부
    (`build_orchestrator_k`)는 부재 JSONL 3종을 빈 파일로 **생성**하고 `workspace_dir` 을
    `makedirs` 하므로, 조립 **전에** 그 대상들의 실재를 직접 판독해 하나라도 없으면 아무것도
    만들지 않고 exit 1 로 끊는다(`precheck`). 따라서 정상·오류 어느 경로에서도 실행 전후의
    파일 집합이 동일하다.
  - **재정의 0.** 그래프·상태 파생은 중립 엔진(`active_graph`/`derive_states`)에서만 오고,
    오케스트레이터 조립은 `k_common.build_orchestrator_k` 를 무수정 재사용한다.

사용법:
  python orchestration/adapters/claude/sweep_units.py <run_dir> \
      --pattern "<정규식>" [--pattern "<정규식>" ...] [--ignore-case] [--json]

종료 코드:
  0 = 히트 0(스윕은 정상 수행됨)  ·  2 = 히트 존재  ·  1 = 오류(run_dir 부재·패턴 무지정 등).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- 경로 배선: e2e 중립 조립부(k_common)를 import 경로에 둔다(resolve_gate 선례 동형) ------
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
E2E_DIR = REPO_ROOT / "uahf" / "framework" / "adapters" / "claude" / "orchestration-data" / "e2e"
if str(E2E_DIR) not in sys.path:
    sys.path.insert(0, str(E2E_DIR))

# k_common import 가 _orch_common 을 통해 중립 코드 경로를 sys.path 에 배선한다(무수정 재사용).
from k_common import build_orchestrator_k, load_json  # noqa: E402


# 히트 문면 표시 상한 — 긴 minified 행 하나가 보고 전체를 삼키지 않게 자른다(결정적).
LINE_CLIP = 200
# 바이너리 판정 표본 크기 — 앞부분에 NUL 바이트가 있으면 텍스트로 취급하지 않는다.
BINARY_PROBE = 8192


class _NoInvoke:
    """스윕은 디스패치가 아니다 — 그래프 재구성 전용 no-op invoker(실 CLI 미발화).

    resolve_gate._NoInvoke 와 같은 역할이다(그쪽은 해소 전용·이쪽은 판독 전용).
    """

    def invoke(self, request):  # noqa: ANN001, D401
        raise RuntimeError(
            "sweep_units 는 실행하지 않는다(단위 경계 판독·패턴 스캔 전용·엔진 대체 아님)"
        )


# ==========================================================================
# 읽기 전용 사전 검사 — 조립 부작용 차단 (Advisor CP2 판정 ① (c))
# ==========================================================================
# `build_orchestrator_k` 는 라이브러리로서 **쓰기 부작용**을 갖는다(조립 코드 재정독으로 확정):
#   - `JsonlEventStore(run_dir/events.jsonl)`      — 부재 시 빈 파일 생성(events.py :75~78)
#   - `JsonlRevisionStore(run_dir/revisions.jsonl)` — 부재 시 빈 파일 생성(revision.py :147~149)
#   - `JsonlArtifactDeclarationStore(run_dir/artifacts.jsonl)` — 부재 시 빈 파일 생성(artifacts.py :275~277)
#   - `os.makedirs(workdir, exist_ok=True)`         — workspace_dir 디렉터리 생성(k_common)
# 이 도구는 판독 전용이므로 그 생성을 **일어나기 전에** 막는다 — 불완전한 run_dir 을 스윕 실행이
# "완성"시켜 버리면 이후 판독이 무엇을 봤는지가 흐려진다(관측 장치가 관측 대상을 바꾸면 안 된다).
# 검사는 순수 판독(`os.path` + `load_json`)만 쓴다.
REQUIRED_RUN_FILES = (
    "config.json",        # 조립 입력(부재 시 load_json 예외) + workspace_dir 원천
    "graph.json",         # 초기 그래프
    "gate_policy.json",   # 게이트 정책
    "events.jsonl",       # ↓ 아래 3종은 부재 시 조립이 **생성**한다
    "revisions.jsonl",
    "artifacts.jsonl",
)


def precheck(run_dir: Path) -> list:
    """조립 전에 실재를 검사한다 — 반환 = 부재 항목 설명 목록(빈 목록 = 통과·쓰기 0).

    검사 대상 = 조립이 소비하거나 **부재 시 생성**하는 run 파일 전부 + config `workspace_dir`
    디렉터리. 이 함수는 어떤 파일·디렉터리도 만들지 않는다.
    """
    run_dir = Path(run_dir)
    missing: list = []
    for name in REQUIRED_RUN_FILES:
        if not (run_dir / name).is_file():
            missing.append("run 파일 부재: %s" % (run_dir / name))

    # workspace_dir 은 config.json 에서만 나온다 — config 가 없으면 여기서 더 볼 것이 없다.
    if (run_dir / "config.json").is_file():
        try:
            cfg = load_json(run_dir / "config.json")
        except Exception as exc:  # noqa: BLE001  (판독 불가는 정직 실패로 표면화)
            missing.append("config.json 판독 실패: %s: %s" % (type(exc).__name__, exc))
            return missing
        ws_raw = cfg.get("workspace_dir")
        workspace = Path(ws_raw) if ws_raw else (run_dir / "workspace")
        if not workspace.is_dir():
            missing.append("워크스페이스 디렉터리 부재: %s" % workspace)
    return missing


# ==========================================================================
# 파일 수집 — ownedBoundary(워크스페이스 상대경로) 해석
# ==========================================================================
def _is_binary(path: Path) -> bool:
    """NUL 바이트 표본으로 바이너리를 판정한다(판독 불가 파일 스킵 기준·결정적)."""
    with open(path, "rb") as fh:
        return b"\x00" in fh.read(BINARY_PROBE)


def collect_files(workspace: Path, boundary: list) -> dict:
    """ownedBoundary 항목들을 실파일 목록으로 해석한다(디렉터리는 재귀).

    반환 = {"files": [Path...정렬], "missing": [상대경로...], "outside": [상대경로...]}.
    - 절대경로·`..` 등으로 워크스페이스 밖을 가리키는 항목은 스캔하지 않고 `outside` 로 보고한다
      (경계 밖 판독 금지 — 침묵 스킵 0).
    - 실재하지 않는 항목은 `missing` 으로 보고한다(아직 산출되지 않은 단위 = 정상 상황이지만
      "0 히트"가 "검사했는데 없음"인지 "검사 자체가 없었음"인지 구분되어야 한다).
    """
    ws = workspace.resolve()
    files: list = []
    missing: list = []
    outside: list = []
    for raw in boundary or []:
        rel = str(raw)
        target = (ws / rel).resolve()
        try:
            target.relative_to(ws)
        except ValueError:
            outside.append(rel)
            continue
        if target.is_dir():
            files.extend(p for p in target.rglob("*") if p.is_file())
        elif target.is_file():
            files.append(target)
        else:
            missing.append(rel)
    # 중복 제거 + 결정적 정렬.
    uniq = sorted({str(p) for p in files})
    return {"files": [Path(p) for p in uniq], "missing": missing, "outside": outside}


def scan_file(path: Path, patterns: list) -> list:
    """한 파일을 라인 단위로 스캔해 [(lineno, 문면)] 히트를 반환한다(판독 전용).

    판독은 `encoding="utf-8", errors="replace"` 로 고정한다 — 한국어·혼합 인코딩 환경에서
    디코딩 예외로 스윕이 중단되면 관측 경로가 유실된다(치환 문자는 그대로 보고에 실린다).
    """
    hits: list = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, start=1):
            text = line.rstrip("\n").rstrip("\r")
            if any(p.search(text) for p in patterns):
                clipped = text if len(text) <= LINE_CLIP else text[:LINE_CLIP] + "…"
                hits.append((lineno, clipped))
    return hits


# ==========================================================================
# 스윕 본체 — 순수 파생(쓰기 0)
# ==========================================================================
def sweep(run_dir: Path, patterns: list) -> dict:
    """현재 그래프의 단위별로 ownedBoundary 를 스캔해 구조화 결과를 반환한다.

    그래프·상태는 중립 엔진 파생(`active_graph`/`derive_states`)만 쓴다 — 제2 진리원천 0.
    워크스페이스 루트 = config `workspace_dir`(부재 시 `run_dir/workspace` — build_orchestrator_k
    폴백과 동일 규칙).
    """
    orch, cfg = build_orchestrator_k(Path(run_dir), _NoInvoke())
    graph = orch.active_graph()
    states = orch.derive_states()

    ws_raw = cfg.get("workspace_dir")
    workspace = Path(ws_raw) if ws_raw else (Path(run_dir) / "workspace")

    units: list = []
    total_hits = 0
    files_scanned = 0
    skipped_binary: list = []
    skipped_unreadable: list = []
    for task in graph.get("tasks", []):
        unit_id = task.get("id")
        collected = collect_files(workspace, task.get("ownedBoundary") or [])
        unit_hits: list = []
        scanned = 0
        for path in collected["files"]:
            try:
                if _is_binary(path):
                    skipped_binary.append(str(path))
                    continue
                found = scan_file(path, patterns)
            except OSError as exc:
                skipped_unreadable.append("%s (%s)" % (path, exc))
                continue
            scanned += 1
            for lineno, text in found:
                try:
                    shown = str(path.relative_to(workspace.resolve()))
                except ValueError:  # 방어 — collect_files 가 이미 경계를 강제한다.
                    shown = str(path)
                unit_hits.append({"file": shown, "line": lineno, "text": text})
        files_scanned += scanned
        total_hits += len(unit_hits)
        units.append({
            "id": unit_id,
            "state": states.get(unit_id, "unknown"),
            "boundary": list(task.get("ownedBoundary") or []),
            "files_scanned": scanned,
            "missing": collected["missing"],
            "outside": collected["outside"],
            "hits": unit_hits,
        })

    return {
        "run_dir": str(Path(run_dir).resolve()),
        "workspace": str(workspace),
        "units": units,
        "total_hits": total_hits,
        "files_scanned": files_scanned,
        "skipped_binary": skipped_binary,
        "skipped_unreadable": skipped_unreadable,
    }


# ==========================================================================
# 사람 친화 렌더 (결정적·타임스탬프 0)
# ==========================================================================
NEXT_LINE = (
    "[NEXT] 조치는 **수정 run 또는 supersede(원장 경유)** 로만 한다 — 적중 단위를 워크스페이스에서 "
    "직접 손보지 마라(원장 밖 직접 수정 금지·계보 단절)."
)


def render(result: dict, patterns_src: list) -> str:
    lines: list = []
    lines.append("[SWEEP] run_dir=%s" % result["run_dir"])
    lines.append("[SWEEP] workspace=%s" % result["workspace"])
    lines.append("[SWEEP] patterns=%s" % json.dumps(patterns_src, ensure_ascii=False))
    lines.append("[SWEEP] units=%d files_scanned=%d total_hits=%d"
                 % (len(result["units"]), result["files_scanned"], result["total_hits"]))
    for unit in result["units"]:
        lines.append("")
        lines.append("[UNIT] %s (state=%s) files=%d hits=%d"
                     % (unit["id"], unit["state"], unit["files_scanned"], len(unit["hits"])))
        for hit in unit["hits"]:
            lines.append("  - %s:%d :: %s" % (hit["file"], hit["line"], hit["text"]))
        if unit["missing"]:
            lines.append("  · 미실재 경계 항목 %d 건(아직 산출되지 않음): %s"
                         % (len(unit["missing"]),
                            json.dumps(unit["missing"], ensure_ascii=False)))
        if unit["outside"]:
            lines.append("  · 워크스페이스 밖 경계 항목 %d 건(판독 안 함): %s"
                         % (len(unit["outside"]),
                            json.dumps(unit["outside"], ensure_ascii=False)))
    lines.append("")
    # 스킵 건수는 항상 보고한다 — 0 건도 명시해야 "검사 범위"가 이진으로 읽힌다(침묵 0).
    lines.append("[SKIPPED] binary=%d unreadable=%d"
                 % (len(result["skipped_binary"]), len(result["skipped_unreadable"])))
    for path in result["skipped_binary"]:
        lines.append("  · binary: %s" % path)
    for path in result["skipped_unreadable"]:
        lines.append("  · unreadable: %s" % path)
    lines.append(NEXT_LINE)
    return "\n".join(lines)


# ==========================================================================
# CLI
# ==========================================================================
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="횡단 결함 스윕 — 단위 경계(ownedBoundary)별 패턴 스캔(읽기 전용·판단 0)",
    )
    parser.add_argument("run_dir", help="run 데이터 백엔드 디렉터리")
    parser.add_argument("--pattern", action="append", default=None,
                        help="검색할 정규식(복수 지정 가능·OR 결합). 1개 이상 필수.")
    parser.add_argument("--ignore-case", action="store_true", help="대소문자 무시")
    parser.add_argument("--json", action="store_true", help="구조화 JSON 출력")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print("[ERR] run_dir 이 디렉터리가 아니다(부재?): %s" % run_dir, file=sys.stderr)
        return 1

    raw_patterns = args.pattern or []
    if not raw_patterns:
        print("[ERR] --pattern 이 1개도 지정되지 않았다 — 무엇을 결함 패턴으로 볼지는 "
              "사람/Advisor 가 정한다(도구는 패턴을 발명하지 않는다).", file=sys.stderr)
        return 1

    # 조립 부작용 차단 — 어떤 파일도 만들기 전에 실재를 확인한다(읽기 전용 보장).
    missing = precheck(run_dir)
    if missing:
        print("[ERR] 불완전한 run_dir — 읽기 전용 도구라 생성하지 않는다(스윕 중단):",
              file=sys.stderr)
        for item in missing:
            print("  · %s" % item, file=sys.stderr)
        return 1

    flags = re.IGNORECASE if args.ignore_case else 0
    patterns = []
    for src in raw_patterns:
        try:
            patterns.append(re.compile(src, flags))
        except re.error as exc:
            print("[ERR] 정규식 컴파일 실패: %r — %s" % (src, exc), file=sys.stderr)
            return 1

    try:
        result = sweep(run_dir, patterns)
    except Exception as exc:  # noqa: BLE001  (판독 실패는 정직 실패로 표면화·추측 0)
        print("[ERR] 스윕 실패(원장/그래프 판독 불가): %s: %s"
              % (type(exc).__name__, exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render(result, raw_patterns))

    return 2 if result["total_hits"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
