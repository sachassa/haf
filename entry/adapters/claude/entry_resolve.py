#!/usr/bin/env python3
"""entry_resolve — Entry Resolution 결정적 실행 로더 (형태 B·LLM 0·순수 관측).

무엇을 하는가:
  UAF 공식 진입점(`/new`·`/continue`)의 Entry Resolution 엔진 고정 5단계(entry/specs/01-entry.md
  §3.2-A)를 **결정적 실행 스크립트**로 물리화한다. 이는 entry-binding.md §2 표가 "형태 B: … 미도입"
  으로 예약해 둔 슬롯을 채우는 것이며, 형태 A(주 세션 규약 절차)와 공존한다(structure.md §7 C-1 —
  형태 A→B 전환에도 01 §3 Core Contract 변경 0).

  LLM 을 전혀 호출하지 않는다(엔진 소관 = 결정적 판별). Discovery 를 수행하지 않고(EN-INV 1),
  Project Contract 를 생성·해석하지 않으며(EN-INV 2 — 유/무만 관측), 폴더를 생성·scaffold 하지
  않는다(EN-INV 1 — "신규 폴더명"은 의도 기록일 뿐, 파일시스템 무변경·순수 판독). 충돌은 게이트
  로 확정하지 않고 데이터로 flag 만 한다 — 게이트 제시는 주 세션 소관이다(EN-INV 6).

엔진 고정 5단계(01 §3.2-A — 재정의 0):
  ① 매칭       — 명시 Entry(name)로 Entry Registry(entry-registry.json)에서 Descriptor 조회.
  ② 확인 관측  — <folder> 파일시스템 실측(entry-binding §4 하이브리드): contract-presence·
                 repository-presence 의 유/무만 관측(내용 파싱 금지·EN-INV 2). 사용자 주입 의도가
                 관측 로커스·기대값을 확정한다(entry-binding §4.0).
  ③ 우선순위 평가 — Descriptor 결정 행(entry-registry decisionRows)을 관측 증거에 대조해 단일 행 선택.
  ④ 결정성 검증  — 관측 조합이 단일 행에만 매칭됨을 확인(등록 무결성 = 각 Entry 의 Evidence 값
                 공간을 전수·상호배타로 분할, 01 §3.2-A 4단계·EN-INV 3).
  ⑤ 방출       — 단일 Discovery Request {mode, inputs, policy}(§5.1 레코드) + 엔진 메타(matchedRow·
                 gate)를 구조화 JSON 으로 stdout 방출.

게이트 구동(Policy as Data 단일 소스·entry-binding §4.2·§4.4·EN-INV 6):
  게이트는 **매칭 행의 policy.ref == "user-confirmation-gate"**(canonical 결정 테이블 행 2·3·4·5)로만
  구동한다. 게이트 이유는 그 행의 policy.conflict(repository-present/contract-present/
  nothing-to-continue·정본 = 01 §3.2-D)에 있다. 하이브리드 선언↔상태 충돌(entry-binding §4.2)은 별도
  imperative 판정이 아니라 이 canonical policy 에 포섭된다 — '신규인데 콘텐츠 존재'=행 2·4, '기존인데
  이어갈 실체 전무'=행 5. Contract 존재 시(행 7·8)는 D3 ③에 따라 incremental·게이트 없음이다.
  **병행 imperative conflict 판정을 두지 않는다**(Policy as Data 위반·거짓 게이트 방지 — 행 7 회귀 정정).
  방출 필드 gate 는 policy.ref 의 투영(별도 판정 아님)이며, 게이트 제시는 주 세션 소관이다.

사용법:
  python entry_resolve.py --entry {new|continue} --folder <경로> [--intent {new|existing}]
                          [--registry <path>] [--indent N]
  # --entry 는 슬래시 없는 new|continue 가 1차 형태(Git Bash MSYS 경로 변환 안전). /new·/continue 도
  #   허용·정규화한다(OQ-7 정정 — 주 세션 Bash 도구 호출 안전).
  # --intent(new|existing) 는 주입 선언의 provenance 에코 입력이며 게이트를 구동하지 않는다. 미지정 시
  #   Entry 기본값(entry-registry defaultIntent: /new→new, /continue→existing).
  # --folder 대신 stdin JSON({"entry","folder","intent"?}) 입력도 허용(--stdin).

종료 코드:
  0 = 해소 성공(gate 유무 무관 — gate=true 는 정상 방출 결과·게이트 제시는 주 세션 소관).
  2 = 사용법 오류(argparse).
  3 = 미등록 Entry(§6 Failure Mode — 임의 해석 금지).
  4 = 결정성 위반 Registry(§6 Failure Mode — 전수·상호배타 분할 실패).

원칙(불변):
  - 순수 판독. <folder>·저장소를 일절 수정하지 않는다(파일·디렉터리 생성 0·EN-INV 1).
  - Policy as Data 단일 소스. 결정 테이블·mode 매핑·게이트(policy.ref)·관측 경로 규칙은 전부
    entry-registry.json 에 있고, 이 코드는 그것을 소비할 뿐 하드코딩하지 않는다. 게이트와 병행하는
    별도 imperative conflict 판정을 두지 않는다(canonical policy 단일 소스·행 7 거짓 게이트 방지).
  - 재정의 0. 01 §3 계약 요소(Descriptor·엔진 단계·결정 행·Evidence·EN-INV)를 재정의하지 않는다 —
    판정 기준은 01 §3, 물리 실현은 entry-binding §4·§5 다.
  - python 3 stdlib 만(외부 패키지 0).

이 스크립트는 entry/adapters/claude/ 경계 소속이다(레이어 co-location·환경 의존 격리 지점).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(유/무 등 비ASCII stdout) — e2e PYTHONUTF8 관례 동형 --------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE / "entry-registry.json"

# 01 §3.2-C valueDomain 정본 토큰 — Registry 선언과 대조 검증한다(하드코딩 아님·동기화 확인).
PRESENT = "유"
ABSENT = "무"
EXPECTED_VALUE_DOMAIN = frozenset({PRESENT, ABSENT})


class RegistryError(Exception):
    """Registry 무결성 위반(결정성 위반 포함) — §6 Failure Mode."""


# ==========================================================================
# Registry 적재 + 무결성/결정성 검증(01 §3.2-A 4단계 — 등록 시점 무결 조건)
# ==========================================================================
def load_registry(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        reg = json.load(fh)

    # Evidence valueDomain 이 01 §3.2-C 정본 유/무 도메인과 일치하는지 대조(동기화 확인).
    for src in reg.get("evidenceSources", []):
        dom = set(src.get("valueDomain") or [])
        if dom != EXPECTED_VALUE_DOMAIN:
            raise RegistryError(
                "Evidence %r valueDomain %r 이 01 §3.2-C 유/무 도메인과 불일치"
                % (src.get("sourceType"), sorted(dom)))

    verify_determinism(reg)
    return reg


def verify_determinism(reg: dict) -> None:
    """01 §3.2-A 4단계 결정성 검증 — 각 Entry 의 (contract×repo) 4조합을 decisionRows 가
    전수·상호배타로 분할하는지 확인. 위반 Registry 는 무효(§6·EN-INV 3)."""
    rows = reg.get("decisionRows") or []
    entries = [e["name"] for e in reg.get("entries") or []]
    combos = [(c, r) for c in (PRESENT, ABSENT) for r in (PRESENT, ABSENT)]

    problems: list[str] = []
    for name in entries:
        for (c, r) in combos:
            matched = [row for row in rows
                       if row.get("entry") == name
                       and row.get("contract") == c and row.get("repo") == r]
            if len(matched) == 0:
                problems.append("전수 위반: Entry %s + contract=%s repo=%s 매칭 행 0개" % (name, c, r))
            elif len(matched) > 1:
                problems.append("상호배타 위반: Entry %s + contract=%s repo=%s 매칭 행 %d개(%r)"
                                % (name, c, r, len(matched), [m.get("row") for m in matched]))
    # decisionRows 에 등재된 Entry 가 entries 목록에 있는지(고아 행 방지).
    known = set(entries)
    for row in rows:
        if row.get("entry") not in known:
            problems.append("고아 결정 행: 미등록 Entry %r (row=%r)" % (row.get("entry"), row.get("row")))

    if problems:
        raise RegistryError("Registry 결정성/무결성 위반:\n  - " + "\n  - ".join(problems))


# ==========================================================================
# ② 확인 관측 — 파일시스템 실측(순수 판독·유/무만·내용 파싱 0·EN-INV 2)
# ==========================================================================
def observe_contract_presence(folder: Path, obs_cfg: dict) -> str:
    """<folder> 로 스코프한 Contract 저장 위치에 project-contract.v<N>.md 인스턴스가
    하나라도 실재하는가(entry-binding §4.1). 유무만 — front-matter·본문 파싱 없음(EN-INV 2)."""
    if not folder.exists() or not folder.is_dir():
        return ABSENT
    for pattern in obs_cfg.get("contractLocations", []):
        for m in folder.glob(pattern):
            if m.is_file():
                return PRESENT
    return ABSENT


def _file_excluded(rel_posix: str, prefixes: tuple[str, ...]) -> bool:
    return any(rel_posix.startswith(p) for p in prefixes)


def observe_repository_presence(folder: Path, obs_cfg: dict) -> str:
    """<folder> 에 '이어갈 실질 프로젝트 본체' 파일이 하나라도 실재하는가(entry-binding §4.2·
    D3 ② 정의). 부재/빈/맨 초기화(.git·메타데이터)·Contract 저장 위치는 본체에서 제외 → 무.
    유무만 관측하며 콘텐츠를 수집·해석하지 않는다(EN-INV 1·2)."""
    if not folder.exists() or not folder.is_dir():
        return ABSENT
    body = obs_cfg.get("repositoryBody", {})
    exclude_prefixes = tuple(body.get("excludePrefixes", []))
    ignore_basenames = set(body.get("ignoreBasenames", []))

    for root, dirs, files in os.walk(folder):
        rel_root = Path(root).relative_to(folder).as_posix()
        # 완전 제외 디렉터리 가지치기(.git/ 등) — 부분 제외(.claude/project-contract/)는 파일 단계에서.
        pruned = []
        for d in dirs:
            rel_dir = (d if rel_root == "." else "%s/%s" % (rel_root, d)) + "/"
            if _file_excluded(rel_dir, exclude_prefixes):
                continue
            pruned.append(d)
        dirs[:] = pruned

        for fname in files:
            if fname in ignore_basenames:
                continue
            rel = fname if rel_root == "." else "%s/%s" % (rel_root, fname)
            if _file_excluded(rel, exclude_prefixes):
                continue
            return PRESENT  # 본체 파일 1개면 충분(유).
    return ABSENT


# ==========================================================================
# ③④ 우선순위 평가 + 결정성 검증(단일 행)
# ==========================================================================
def match_row(reg: dict, entry: str, contract: str, repo: str) -> dict:
    matched = [row for row in reg.get("decisionRows", [])
               if row.get("entry") == entry
               and row.get("contract") == contract and row.get("repo") == repo]
    if len(matched) != 1:
        # load_registry 의 verify_determinism 을 통과했다면 도달 불가 — 방어적 확인.
        raise RegistryError(
            "결정성 위반(런타임): Entry %s + contract=%s repo=%s → %d 행 매칭"
            % (entry, contract, repo, len(matched)))
    return matched[0]


# ==========================================================================
# Entry 인자 정규화 — new|continue(슬래시 없음·Git Bash MSYS 안전) → canonical /new·/continue
# ==========================================================================
def normalize_entry(raw: str | None) -> str | None:
    """--entry 인자 정규화(OQ-7 정정). 슬래시 없는 new|continue 를 1차 형태로 받아 canonical
    /new·/continue 로 매핑한다. 이미 슬래시가 있으면 그대로. Registry entry name 은 /new·/continue 다.
    주 세션이 Bash 도구로 호출할 때 `/new` 가 MSYS 경로로 변환되는 문제를 회피한다."""
    if raw is None:
        return None
    return raw if raw.startswith("/") else "/" + raw


# ==========================================================================
# 엔진 실행(5단계 오케스트레이션)
# ==========================================================================
def resolve(reg: dict, entry: str, folder: Path, intent: str | None) -> dict:
    # ① 매칭 — Entry Descriptor 조회(entry 는 canonical /new·/continue).
    descriptor = next((e for e in reg.get("entries", []) if e.get("name") == entry), None)
    if descriptor is None:
        known = [e.get("name") for e in reg.get("entries", [])]
        raise LookupError("미등록 Entry %r — 등재 Entry: %r (§6 Failure Mode·임의 해석 금지)"
                          % (entry, known))
    if intent is None:
        intent = descriptor.get("defaultIntent")

    # ② 확인 관측 — 파일시스템 실측(순수 판독·유/무만).
    obs_cfg = reg.get("observation", {})
    contract = observe_contract_presence(folder, obs_cfg)
    repo = observe_repository_presence(folder, obs_cfg)

    # ③④ 우선순위 평가 + 결정성 검증(단일 행).
    row = match_row(reg, entry, contract, repo)

    # 게이트 = canonical policy.ref 의 투영(Policy as Data 단일 소스·별도 imperative 판정 없음).
    gate = row["policy"].get("ref") == "user-confirmation-gate"

    # ⑤ 방출 — Discovery Request {mode, inputs, policy}(§5.1) + 엔진 메타.
    return {
        "entry": entry,
        "intent": intent,          # 주입 선언의 provenance 에코 — 게이트를 구동하지 않는다.
        "folder": str(folder),
        "mode": row["mode"],
        "provisional": bool(row.get("provisional", False)),
        "inputs": [
            {"sourceType": "contract-presence", "observed": contract},
            {"sourceType": "repository-presence", "observed": repo},
        ],
        "policy": row["policy"],
        "matchedRow": row["row"],
        "gate": gate,              # policy.ref == user-confirmation-gate 의 투영(canonical 단일 소스).
        "_note": ("mode·inputs·policy = Discovery Request(entry-binding §5.1·§12.2·재정의 0). "
                  "matchedRow·gate = 엔진 메타. gate 는 canonical policy.ref 의 투영일 뿐 별도 "
                  "conflict 판정이 아니다(Policy as Data 단일 소스). intent 는 provenance 에코(게이트 "
                  "미구동). Entry 는 여기서 멈춘다 — Discovery 수행·Contract 생성 0(EN-INV 1·2)."),
    }


# ==========================================================================
# CLI
# ==========================================================================
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Entry Resolution 결정적 실행 로더(형태 B·LLM 0·순수 관측·01 §3 재정의 0)")
    parser.add_argument("--entry", choices=["new", "continue", "/new", "/continue"],
                        metavar="{new|continue}",
                        help="명시 Entry(new|continue — 슬래시 없는 형태가 1차·Git Bash MSYS 안전; "
                             "/new·/continue 도 허용·정규화, 01 §3.1). --stdin 사용 시 생략 가능.")
    parser.add_argument("--folder", help="관측 대상 폴더(사용자 주입 로커스, entry-binding §4.0).")
    parser.add_argument("--intent", choices=["new", "existing"], default=None,
                        help="주입 신규/기존 의도(provenance 에코·게이트 미구동). 미지정 시 Entry "
                             "기본값(entry-registry defaultIntent).")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                        help="Entry Registry 데이터 파일(기본 = 이 스크립트 옆 entry-registry.json).")
    parser.add_argument("--stdin", action="store_true",
                        help="stdin 에서 JSON {entry, folder, intent?} 을 읽는다(CLI 인자 대체).")
    parser.add_argument("--indent", type=int, default=2, help="JSON 들여쓰기(기본 2).")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    entry = args.entry
    folder = args.folder
    intent = args.intent
    if args.stdin:
        payload = json.load(sys.stdin)
        entry = payload.get("entry", entry)
        folder = payload.get("folder", folder)
        intent = payload.get("intent", intent)

    entry = normalize_entry(entry)  # new|continue → /new·/continue(OQ-7 정정).

    if not entry or not folder:
        print("사용법 오류: --entry 와 --folder 는 필수다(또는 --stdin JSON).", file=sys.stderr)
        return 2

    try:
        reg = load_registry(Path(args.registry))
    except RegistryError as exc:
        print("[REGISTRY-INVALID] %s" % exc, file=sys.stderr)
        return 4
    except (OSError, json.JSONDecodeError) as exc:  # 부재·손상 Registry 도 §6 Registry 실패로.
        print("[REGISTRY-UNREADABLE] %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 4

    try:
        result = resolve(reg, entry, Path(folder), intent)
    except LookupError as exc:  # 미등록 Entry.
        print("[UNKNOWN-ENTRY] %s" % exc, file=sys.stderr)
        return 3
    except RegistryError as exc:  # 런타임 결정성 위반(방어적).
        print("[NON-DETERMINISTIC] %s" % exc, file=sys.stderr)
        return 4

    json.dump(result, sys.stdout, ensure_ascii=False, indent=args.indent)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
