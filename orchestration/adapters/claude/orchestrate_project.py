"""임의 소비 프로젝트(Contract vN) → 오케스트레이션 엔진 구동 **프로덕션 런처** (F3).

이 모듈은 확정된 Project Contract 를 가진 임의 소비 프로젝트를 중립 Orchestrator 로 구동하는
프로덕션 진입점이다. 자기규정 "비프로덕션"인 e2e 드라이버(orchestration-data/e2e/)의
**중립 조립부는 import 로 재사용**하고(중복 신설 0), 특정 시나리오(j/k/w) 픽스처에 묶이지
않게 일반화한다. F4(contract_to_graph.compile)가 만든 순수 데이터(config/graph/gate_policy)를
물리화하고, e2e 의 워크스페이스 인지 조립부(build_orchestrator_k)로 오케스트레이터를 구성한다.

경계·불변(무엇을 하지 않는가):
  - orchestration/framework/** · uahf/** 를 **수정하지 않는다**(import 만). e2e 드라이버도
    무수정 재사용한다(build_orchestrator_k·make_invoker 를 그대로 import).
  - 소비 프로젝트 루트(workspace)를 **삭제·스캐폴드·클로버하지 않는다** — 실재 확인만 한다
    (setup_w 선례). run 디렉터리(runs/<run-id>/)만 fresh-init 하되 RUNS_DIR 밖 오삭제를 가드한다.
  - 실 claude CLI 발화는 CLI main 경로(make_invoker)만 담당한다. 조립/구동을 함수로 분리해
    테스트가 no-op/stub invoker 를 주입할 수 있게 한다(오프라인 dry-run).

exit-code 매핑(orchestration-data/e2e/run_k.py 와 동일·바인딩 §5.3):
  - status=="stopped" & stop_reason=="gate"(정지 게이트) → logs/stop-signal.json 기록 + exit 2.
  - status=="stopped"(그 외·Escalated) → **같은 계약 형태로** logs/stop-signal.json 기록 + exit 2.
    (백로그 §J ① — 정지 사유와 무관하게 stop-signal 을 일관 갱신한다. 엔진이 실행
     에스컬레이션에 게이트 좌표를 부여하므로 resolve_gate 가 추측 없이 해소 대상을 복원한다.)
  - completed → 0.  halted → 3.
  - 런처 자체 실패(project_root 부재·resume 대상 부재 등 정직 실패) → 1.
    미처리 예외도 비영 종료이며 `logs/failure.json` 에 사후 진단 사본이 남는다.

관측 계약(백로그 §L·§P — 이 런처 소유·중립 코드 무촉):
  - `logs/heartbeat.json` — invoke 시작 전·종료 후 덮어쓰기. hang(F2)은 종료 이벤트가
    원리적으로 없으므로 "마지막 진행 시각"이 유일한 정체 탐지 수단이다.
  - `logs/failure.json` — 미처리 예외의 구조화 기록(재raise 병행·은폐 0).
  - 두 기록 모두 **failure-isolated** — 기록 실패가 run 을 실패시키지 않는다.

이 모듈은 stdlib + 기존 저장소 모듈 import 만 쓴다(외부 패키지 0·오프라인 안전).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import sys
import traceback
from pathlib import Path
from typing import Any


# --------------------------------------------------------------------------
# 경로 배선 — 이 런처 디렉터리(F4 compile) + e2e 중립 조립부(build_orchestrator_k)
# --------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent                    # orchestration/adapters/claude
REPO_ROOT = HERE.parents[2]                               # repo root
E2E_DIR = REPO_ROOT / "uahf" / "framework" / "adapters" / "claude" / "orchestration-data" / "e2e"
RUNS_DIR = REPO_ROOT / "uahf" / "framework" / "adapters" / "claude" / "orchestration-data" / "runs"

# 이 런처 디렉터리를 import 경로에 둔다(contract_to_graph 는 같은 디렉터리의 F4 모듈).
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import contract_to_graph  # noqa: E402  (F4 — stdlib only 순수 데이터 생성기)


def _wire_e2e_path() -> None:
    """e2e 중립 조립부(k_common/_orch_common)를 import 경로에 둔다.

    k_common import 가 로드 시점에 중립 코드 경로(orchestrator/·step-host/·step-invoker/)를
    sys.path 에 배선한다(_orch_common 38~41행). 따라서 E2E_DIR 만 추가하면 나머지 중립 경로는
    자동 배선된다.
    """
    p = str(E2E_DIR)
    if p not in sys.path:
        sys.path.insert(0, p)


def wire_paths():
    """전체 import 경로(e2e + 중립 코드)를 배선하고 k_common 모듈을 반환한다(테스트 seam)."""
    _wire_e2e_path()
    import k_common  # noqa: E402  (import 부작용으로 중립 경로 배선)
    return k_common


# --------------------------------------------------------------------------
# run_id 슬러그 — 물리 디렉터리 안전 정규화
# --------------------------------------------------------------------------
_SLUG_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


def slugify_run_id(raw: Any) -> str:
    """run_id 를 물리 디렉터리 안전 슬러그로 정규화한다.

    영숫자·`.`·`_`·`-` 외 문자(공백·특수문자)를 `-` 로 치환하고 앞뒤 구분자를 제거한다.
    예: "orch-myproj-Phase 1" → "orch-myproj-Phase-1"(공백 제거). 빈 결과는 "run" 으로 폴백한다.

    길이 상한은 `contract_to_graph.fold_slug`(48자 + `-<sha8>`) **공통 규칙**을 재사용한다 —
    컴파일러 `_slug`(unit id)와 런처(run_id)가 서로 다른 상한을 쓰면 접합부가 어긋난다.
    48자 이하 입력은 바이트 동일(기존 run 디렉터리 하위호환·백로그 §P·§L 4-b).
    """
    s = _SLUG_UNSAFE.sub("-", str(raw)).strip("-._")
    return contract_to_graph.fold_slug(s or "run", raw)


# --------------------------------------------------------------------------
# 물리화 — run 데이터 백엔드 조립(바인딩 §5.3)
# --------------------------------------------------------------------------
def _write_json(path: Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)


def _materialize_run_dir(
    run_dir: Path, slug: str, config: dict, graph: dict, gate_policy: dict
) -> None:
    """run 디렉터리를 fresh-init 하고 3종 데이터 + steps 뷰를 기록한다(setup_w 선례).

    오삭제 가드(핵심): run_dir 이 RUNS_DIR 직속이 아니면(=소비 프로젝트 등 무관 경로면) 삭제하지
    않고 중단한다. run_dir 이 이미 있으면 basename==slug 확인 후에만 rmtree 한다(재실행 대상).
    소비 프로젝트 루트(workspace)는 이 함수가 결코 건드리지 않는다(별도 경로·RUNS_DIR 밖).
    """
    if run_dir.resolve().parent != RUNS_DIR.resolve():
        raise RuntimeError(
            "run_dir 이 RUNS_DIR 밖이다 — 오삭제 방지 가드로 중단: %s" % run_dir
        )
    if run_dir.exists():
        if run_dir.name != slug:
            raise RuntimeError(
                "run_dir basename 불일치 — 오삭제 방지 가드로 중단: %s" % run_dir
            )
        shutil.rmtree(run_dir)
    (run_dir / "steps").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "workspace").mkdir(parents=True, exist_ok=True)

    _write_json(run_dir / "config.json", config)
    _write_json(run_dir / "graph.json", graph)
    _write_json(run_dir / "gate_policy.json", gate_policy)
    for task in graph.get("tasks", []):
        _write_json(run_dir / "steps" / (task["id"] + ".json"), task)


def prepare_run(
    project_root: Any,
    *,
    mode: str = "incremental",
    phase_scope: str = "Phase 1",
    run_id: Any = None,
    retry_limit: Any = None,
    model: Any = None,
    policy: str = "auto_approve",
) -> tuple[Path, dict]:
    """소비 프로젝트를 컴파일(F4)·물리화해 (run_dir, config) 를 반환한다(구동 전 준비).

    - project_root 실재 확인(부재/비디렉터리 → FileNotFoundError·정직 실패).
    - contract_to_graph.compile 로 {config, graph, gate_policy} 순수 데이터 생성.
    - run_id sanitize: --run-id 우선, 없으면 compile 이 준 run_id 를 슬러그 정규화. config.run_id 일치.
    - config.workspace_dir = project_root 절대경로 재확인(compile 이 이미 설정).
    - retry_limit override(선택·smoke 지원): build_config 하드코딩(2)을 덮어쓴다.
    - run_dir 물리화(RUNS_DIR/<slug>/). 소비 프로젝트는 건드리지 않는다.
    """
    root = Path(project_root).resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError("project_root 가 실재하지 않는다(비디렉터리/부재): %s" % root)

    compiled = contract_to_graph.compile(root, mode=mode, phase_scope=phase_scope)
    config = compiled["config"]
    graph = compiled["graph"]
    gate_policy = compiled["gate_policy"]

    slug = slugify_run_id(run_id if run_id else config.get("run_id"))
    config["run_id"] = slug
    config["workspace_dir"] = str(root)  # 재확인(compile 이 이미 설정하나 불변 보장).
    # Autonomy Policy override — 이 런처는 headless 드라이버이므로 auto_approve 를 기본으로 소유한다
    # (interactive 는 headless 에서 승인 주체 부재로 비기능·e2e j/k 선례 = auto_approve). 게이트 5종은
    # policy 와 직교하게 전부 작동한다(05 §3.3 orthogonality — 정지 게이트 보존).
    config["policy"] = policy
    if retry_limit is not None:
        config["retry_limit"] = int(retry_limit)

    # model 슬롯 override(선택·smoke 티어 절감): 초기 그래프 노드(=seed proposal)의 model 슬롯만
    # 덮어쓴다. 하위 구현 task 의 model 은 런타임 impl-plan(LLM)이 정한다(F4 계약).
    if model:
        for task in graph.get("tasks", []):
            task["model"] = model

    run_dir = RUNS_DIR / slug
    _materialize_run_dir(run_dir, slug, config, graph, gate_policy)
    return run_dir, config


def build(run_dir: Any, invoker: Any):
    """run 데이터 백엔드에서 중립 Orchestrator 를 조립한다(e2e build_orchestrator_k 재사용).

    build_orchestrator_k 는 workdir 를 config.workspace_dir(=소비 프로젝트 루트 절대경로)로
    배선한다(외부 워크스페이스 인지). 무수정 라이브러리 import — 이 런처는 조립부를 재현하지
    않고 그대로 재사용한다(중복 신설 0). 반환 = (orch, cfg).
    """
    wire_paths()
    from k_common import build_orchestrator_k  # noqa: E402  (무수정 재사용)
    return build_orchestrator_k(Path(run_dir), invoker)


# --------------------------------------------------------------------------
# 횡단 결함 검지 관측 — [REWORK-NOTE] (백로그 §M D-M2 ①)
# --------------------------------------------------------------------------
# 왜 필요한가: CP2 재작업(rework)은 **그 단위에만 있는 결함의 신호가 아니다**. 같은 API 오용·
# 같은 잘못된 관례가 동료 단위에 복제돼 있어도 각 단위의 done AC 는 자기 산출만 보므로 통과한다.
# 재작업이 발생한 run 은 "다른 단위도 같은 패턴을 갖고 있을 수 있다"는 유일한 기계 신호를
# 원장에 남기므로, 런처가 그 신호를 종료 표면에 올린다.
#
# 경계(엔진 판단 0·PO-INV 1): 이 관측은 **파생·열거·권고**까지만 한다. 어떤 패턴을 스윕할지,
# 적중을 어떻게 조치할지는 사람/Advisor 소유다. 자동 되돌림은 미도입(D-M3 — 결함 패턴 추출은
# 내용 판단이라 엔진이 소유할 수 없다).
REWORK_REF_KIND = "rework"
SWEEP_TOOL = "orchestration/adapters/claude/sweep_units.py"
# 인용 문면 표시 상한 — sweep_units.LINE_CLIP 동형(긴 재작업 지시가 종료 표면을 삼키지 않게).
REWORK_QUOTE_CLIP = 200
REWORK_QUOTE_CLIP_MARK = "…(클립)"


def _quote_rework(value: Any) -> Any:
    """`ref.rework` 를 note 1행에 실을 인용 문자열로 만든다(**인용만** — 해석·요약·추출 0).

    - 문자열이 아니면 `json.dumps`(원 구조 보존 직렬화)로 문자열화한다.
    - 개행은 note 가 단위별 1행 계약이므로 공백으로 접는다(행 맞춤 — 내용 변형 아님).
    - `REWORK_QUOTE_CLIP` 초과분은 자르고 클립 표기를 붙인다(잘렸다는 사실을 숨기지 않는다).
    - None·빈 문자열이면 None 을 반환해 **인용 행 자체를 생략**한다(없는 것을 발명하지 않는다).
    """
    if value is None:
        return None
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    text = text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").strip()
    if not text:
        return None
    if len(text) > REWORK_QUOTE_CLIP:
        text = text[:REWORK_QUOTE_CLIP] + REWORK_QUOTE_CLIP_MARK
    return text


def rework_details(run_dir: Any) -> list:
    """`events.jsonl` 에서 rework 단위와 **마지막** 재작업 지시 원문을 파생한다(읽기 전용).

    반환 = `[(cycle_id, quote|None), ...]` — 원장 첫 등장 순서(결정적), 단위당 1건.
    `quote` 는 그 단위의 **마지막** `ref.rework` 인용(뒤 이벤트가 앞을 덮는다 — 가장 최근
    지시가 현재 상태를 말한다). 어휘 좌표는 step-host `_record_failure`
    (CP2 Fail/Conditional → `ref={"kind":"rework","rework":<지시>,...}`)이며 이 함수는 그
    어휘를 읽기만 한다. 파일 부재·행 파손 등 판독 실패는 **호출자에게 예외로 표면화**한다(침묵 0).
    """
    path = Path(run_dir) / "events.jsonl"
    order: list = []
    quotes: dict = {}
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            event = json.loads(raw)
            ref = event.get("ref")
            if isinstance(ref, dict) and ref.get("kind") == REWORK_REF_KIND:
                cycle_id = event.get("cycle_id")
                if cycle_id is None:
                    continue
                if cycle_id not in quotes:
                    order.append(cycle_id)
                quotes[cycle_id] = _quote_rework(ref.get("rework"))
    return [(cid, quotes[cid]) for cid in order]


def rework_units(run_dir: Any) -> list:
    """rework 가 발생한 cycle_id 목록(원장 등장 순·중복 제거). `rework_details` 의 투영."""
    return [cid for cid, _quote in rework_details(run_dir)]


def print_rework_note(run_dir: Any) -> list:
    """[REWORK-NOTE] 관측 라인을 출력한다(부가 표면 — 종료 코드·기존 출력 불변).

    - rework 0 이면 **어떤 라인도 출력하지 않는다**(종전 출력 바이트 보존).
    - 원장 판독 실패(파일 부재·파손)는 note 를 생략하되 stderr 1행으로 생략 사실을 명시한다
      (render_gates 부가 표면 방어와 동형 — 관측 장치가 run 을 죽이지 않되 침묵하지도 않는다).
    반환 = 열거된 단위 목록(생략 시 빈 목록).
    """
    try:
        details = rework_details(run_dir)
    except Exception as exc:  # noqa: BLE001  (관측 부가 표면 — 런처 흐름 불변)
        print("[REWORK-NOTE-SKIP] 재작업 원장 판독 실패 — 횡단 스윕 권고 생략"
              "(run 결과·종료 코드는 유효): %s" % exc, file=sys.stderr)
        return []
    if not details:
        return []
    units = [cid for cid, _q in details]
    print("[REWORK-NOTE] CP2 재작업이 발생한 단위: %s"
          % json.dumps(units, ensure_ascii=False))
    # 마지막 재작업 지시 **원문 인용**(해석·요약·패턴 추출 0 — 표면화까지가 이 층의 몫이다).
    # 지시가 없는 단위는 인용 행을 내지 않는다(발명 0).
    for cycle_id, quote in details:
        if quote is not None:
            print("              · %s ← %s" % (cycle_id, quote))
    print("              같은 결함 패턴이 동료 단위에 복제돼 있을 수 있다 — 결함 패턴을 "
          "정한 뒤 전 단위 횡단 스윕을 권고한다(패턴 선정·조치 판단은 사람/Advisor 소유).")
    print("              python %s %s --pattern \"<정규식>\"" % (SWEEP_TOOL, run_dir))
    return units


# --------------------------------------------------------------------------
# 구동 + exit-code 매핑 (run_k.py 와 동일)
# --------------------------------------------------------------------------
def run_and_map(orch: Any, invoker: Any, run_dir: Any) -> int:
    """orch.run() 후 결과를 종료 코드로 매핑한다(run_k.py 바이트 동형 매핑).

    정지 게이트(stopped & gate) → logs/stop-signal.json 기록 + exit 2.
    그 외 stopped(Escalated) → exit 2.  completed → 0.  halted → 3.
    """
    run_dir = Path(run_dir)
    result = orch.run()

    print("[RESULT] status=%s stop_reason=%s epochs=%s"
          % (result.status, result.stop_reason, result.epochs))
    print("[GRAPH] tasks=%s" % json.dumps(result.graph_task_ids, ensure_ascii=False))
    print("[STATES] %s" % json.dumps(result.states, ensure_ascii=False))
    print("[INVOKES] total=%s" % getattr(invoker, "invoke_count", "n/a"))
    # 횡단 결함 검지 관측(백로그 §M D-M2 ①) — status 무관·rework 0 이면 무출력.
    print_rework_note(run_dir)

    if result.status == "stopped" and result.stop_reason == "gate":
        marker = {
            "stop_reason": result.stop_reason,
            "stopped_tasks": result.stopped_tasks,
            "pending_gates": result.pending_gates,
            "note": "정지 게이트 물리 정지 — 실 사용자/상위 개입 대기(exit 2). "
                    "autonomy policy 와 무관하게 정지 게이트는 보존된다(PO-INV 4).",
        }
        (run_dir / "logs").mkdir(parents=True, exist_ok=True)
        with open(run_dir / "logs" / "stop-signal.json", "w", encoding="utf-8") as fh:
            json.dump(marker, fh, ensure_ascii=False, indent=2)
        print("[STOP] gate pending=%s -> exit code 2"
              % json.dumps([g.get("gate_id") for g in result.pending_gates],
                           ensure_ascii=False))
        print("[PENDING-GATES] %s" % json.dumps(result.pending_gates, ensure_ascii=False))
        # 사람 친화 게이트 큐 렌더(부가 표면·OQ-PO-B1). 위 [STOP]/[PENDING-GATES] 라인과
        # stop-signal.json 을 **바이트 보존**한 뒤 그 이후에 render_gates 렌더 함수를 재사용해
        # 추가 출력한다. 렌더는 부가 표면이므로 실패(import·파싱)해도 정지 신호를 깨지 않는다
        # (렌더 실패 시 기존 출력만 유지·방어). policy 는 render_gates.load_pending 이 동일 경로
        # (gate_policy.json)에서 로드하고, 렌더 입력은 run 결과 result.pending_gates(권위)를 쓴다.
        try:
            import render_gates  # noqa: E402  (같은 어댑터 경계·form-B 순수 렌더)

            _pending, policy = render_gates.load_pending(run_dir)
            print(render_gates.render_pending(result.pending_gates, policy))
        except Exception as exc:  # noqa: BLE001  (렌더는 부가 표면 — 정지 신호 불변)
            print("[RENDER-SKIP] 게이트 큐 렌더 생략(정지 신호는 유효): %s" % exc,
                  file=sys.stderr)
        return 2

    if result.status == "stopped":
        # 기존 라인 **바이트 보존**(계약·기존 테스트) 후, 게이트 분기와 **같은 계약 형태**로
        # stop-signal.json 을 기록한다(백로그 §J ① — 모든 정지 사유에서 일관 갱신). 엔진이
        # escalated 정지에 게이트 좌표를 부여하므로(gate_id) resolve_gate 가 해소 대상을
        # 추측 없이 복원할 수 있다. pending_gates 가 비면(게이트 정책 부재 레거시 run 등)
        # 빈 배열 + note 에 그 사실을 명시한다(침묵 0).
        print("[STOP] escalated -> exit code 2")
        pending = list(getattr(result, "pending_gates", None) or [])
        note = (
            "실행 에스컬레이션 물리 정지 — 상위(Advisor/사람) 해소 대기(exit 2). "
            "해소: resolve_gate.py --gate-kind escalation --actor <Advisor|human> "
            "→ 재개: orchestrate_project.py <project_root> --resume (해소 1건 = 추가 시도 1회)."
        )
        if not pending:
            note += (
                " pending_gates 가 비어 있다 — 이 run 은 게이트 정책 없이 조립됐거나(레거시) "
                "게이트 좌표가 아직 없다. --resume 1회로 요구 이벤트가 생성되면 해소 가능해진다."
            )
        marker = {
            "stop_reason": result.stop_reason,
            "stopped_tasks": result.stopped_tasks,
            "pending_gates": pending,
            "note": note,
        }
        (run_dir / "logs").mkdir(parents=True, exist_ok=True)
        with open(run_dir / "logs" / "stop-signal.json", "w", encoding="utf-8") as fh:
            json.dump(marker, fh, ensure_ascii=False, indent=2)
        print("[PENDING-GATES] %s" % json.dumps(pending, ensure_ascii=False))
        try:
            import render_gates  # noqa: E402  (같은 어댑터 경계·form-B 순수 렌더)

            _pending, policy = render_gates.load_pending(run_dir)
            print(render_gates.render_pending(pending, policy))
        except Exception as exc:  # noqa: BLE001  (렌더는 부가 표면 — 정지 신호 불변)
            print("[RENDER-SKIP] 게이트 큐 렌더 생략(정지 신호는 유효): %s" % exc,
                  file=sys.stderr)
        return 2

    if result.completed:
        print("[COMPLETE] all units Passed.")
        return 0

    print("[HALTED] not completed, not stopped.")
    return 3


# --------------------------------------------------------------------------
# 관측 계약 — heartbeat(F2 정체 탐지) · failure.json(F1 사후 진단)  [백로그 §L 1·2]
# --------------------------------------------------------------------------
# 왜 필요한가(백로그 §L Problem): 실패 모드 3종 중 **F2(hang·무한대기)** 는 프로세스가 끝나지
# 않으므로 종료 이벤트가 **원리적으로 오지 않는다**. 침묵이 "진행 중"인지 "멈춤"인지 구분하는
# 유일한 수단이 **진행의 능동적 증거 = 마지막 진행 시각**이다. 엔진 stdout 은 버퍼링돼 실행
# 중에는 비어 있으므로 로그 tail 로는 대체되지 않는다.
#
# 불변(둘 다 failure-isolated): 기록 실패는 **절대 run 을 실패시키지 않는다**. 관측 장치가
# 관측 대상을 죽이면 안 된다(render_gates 부가 표면·`_orch_common` 섀도 장치 동형). 기록 실패는
# stderr 경고로 표면화한다 — 조용히 삼키지 않는다(침묵 0).
HEARTBEAT_FILE = "heartbeat.json"
FAILURE_FILE = "failure.json"


def _now_iso() -> str:
    """물리 시각 ISO 문자열. 어댑터 코드이므로 실시각 사용이 허용된다(중립 코드 무촉)."""
    return datetime.datetime.now().astimezone().isoformat()


def _request_hint(request: Any) -> Any:
    """요청에서 파생 가능한 **단위 식별 최선값**(없으면 None). 파생 실패도 None(관측 격리).

    step 번들 계약상 단위 id 는 `bundle["step_contract"]["id"]` 에 있다(`_orch_common`
    로그 파일명 파생과 동일 좌표). 계약이 달라지거나 부재해도 하트비트는 계속 뛰어야
    하므로 어떤 예외도 None 으로 흡수한다.
    """
    try:
        bundle = getattr(request, "bundle", None) or {}
        sc = bundle.get("step_contract") or {}
        unit_id = sc.get("id")
        role = getattr(request, "role", None)
        if unit_id and role:
            return "%s/%s" % (role, unit_id)
        return unit_id or role or None
    except Exception:  # noqa: BLE001  (관측 파생은 run 을 깨지 않는다)
        return None


class HeartbeatInvoker:
    """invoker 데코레이터 — invoke **시작 전·종료 후** `logs/heartbeat.json` 을 덮어쓴다.

    런처 소유 래퍼다: 중립 코드(`orchestration/framework/**`)·e2e 조립부(`make_invoker`)를
    수정하지 않고 어댑터 경계에서만 관측을 얹는다(무수정 재사용 원칙 보존).

    인터페이스 보존: `invoke(request)` 를 원 invoker 에 위임하고, 그 밖의 속성은
    `__getattr__` 로 **투과**한다 — 특히 `run_and_map` 이 읽는 `invoke_count` 가 원
    invoker 값 그대로 보이도록(관측 수치 왜곡 0).

    파일은 append 가 아니라 **덮어쓰기**다 — 소비자가 알아야 하는 것은 "마지막 진행 시각"
    하나이며, 누적 계측은 백로그 H(Continuous Telemetry) 소관이다(경계 구분).
    """

    def __init__(self, inner: Any, run_dir: Any) -> None:
        self._inner = inner
        self._run_dir = Path(run_dir)
        self._invokes = 0

    def __getattr__(self, name: str) -> Any:
        # 래퍼 자체 속성(_inner/_run_dir/_invokes/invoke)은 정상 조회로 해결되므로 여기 오지
        # 않는다. object.__getattribute__ 로 꺼내 __init__ 이전 접근 시 무한재귀를 막는다.
        return getattr(object.__getattribute__(self, "_inner"), name)

    def invoke(self, request: Any):
        self._invokes += 1
        hint = _request_hint(request)
        self._beat("invoke-start", hint)
        try:
            return self._inner.invoke(request)
        finally:
            self._beat("invoke-end", hint)

    def _beat(self, stage: str, request_hint: Any) -> None:
        """하트비트 1회 기록. **어떤 실패도 run 에 전파하지 않는다**(failure isolation)."""
        try:
            logs = self._run_dir / "logs"
            logs.mkdir(parents=True, exist_ok=True)
            payload = {
                "ts": _now_iso(),
                "stage": stage,
                "invokes": self._invokes,
                "request_hint": request_hint,
                "pid": os.getpid(),
            }
            with open(logs / HEARTBEAT_FILE, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
        except Exception as exc:  # noqa: BLE001  (관측 장치가 run 을 죽이지 않는다)
            print("[HEARTBEAT-SKIP] 하트비트 기록 실패(run 은 계속 진행): %s" % exc,
                  file=sys.stderr)


def _record_failure(run_dir: Any, run_id: Any, argv: Any, exc: BaseException) -> None:
    """미처리 예외를 `logs/failure.json` 에 구조화 기록한다(계약 필드 6종).

    `{ts, run_id, argv, error_type, error, traceback}`. 스택트레이스는 **stderr 에도 그대로**
    올라간다(호출부가 재raise) — 이 파일은 은폐 수단이 아니라 사후 진단용 사본이다(은폐 0).
    run_dir 을 아직 모르면(인자 파싱 직후 실패 등) 기록을 생략한다 — 임의 경로 추측 금지.
    기록 자체도 failure-isolated: 기록 실패가 원 예외를 가리지 않는다.
    """
    try:
        if run_dir is None:
            print("[FAILURE-SKIP] run_dir 미확정 — failure.json 생략(원 예외는 그대로 전파)",
                  file=sys.stderr)
            return
        logs = Path(run_dir) / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        payload = {
            "ts": _now_iso(),
            "run_id": run_id,
            "argv": list(argv) if argv is not None else [],
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": "".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)
            ),
        }
        with open(logs / FAILURE_FILE, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
        print("[FAILURE] 미처리 예외 기록: %s" % (logs / FAILURE_FILE), file=sys.stderr)
    except Exception as rec_exc:  # noqa: BLE001  (기록 실패가 원 예외를 가리지 않는다)
        print("[FAILURE-SKIP] failure.json 기록 실패: %s" % rec_exc, file=sys.stderr)


# --------------------------------------------------------------------------
# CLI — 실 claude CLI 발화(make_invoker) 경로
# --------------------------------------------------------------------------
def _run_dir_candidates(limit: int = 10) -> list:
    """RUNS_DIR 의 **실존** 하위 디렉터리 이름을 수정시각 최신순으로 최대 `limit` 개 반환.

    `--resume` 부재 오류가 "부재"만 알리고 **실재하는 run 이 옆에 있다는 사실을 알려주지
    않는** 결함(백로그 §L 5)의 해소다. 조회 실패는 빈 목록(부가 표면·오류 경로를 깨지 않음).
    """
    try:
        entries = [p for p in RUNS_DIR.iterdir() if p.is_dir()]
    except OSError:
        return []
    def _mtime(p: Path) -> float:
        try:
            return p.stat().st_mtime
        except OSError:
            return 0.0
    entries.sort(key=_mtime, reverse=True)
    return [p.name for p in entries[:limit]]


def _resolve_slug(run_id: Any, phase_scope: str, project_name: str) -> str:
    """resume 시 run_dir 이름을 재현하기 위한 슬러그 산출(compile 과 동일 규칙).

    compile 의 run_id 파생("orch-" + 워크스페이스 루트 폴더명 + "-" + phase_scope)을 동일하게
    재현한다(도메인 하드코딩 0). --run-id override 시 그 값을 슬러그 정규화한다.
    """
    if run_id:
        return slugify_run_id(run_id)
    return slugify_run_id("orch-" + str(project_name) + "-" + str(phase_scope))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Contract vN 소비 프로젝트를 오케스트레이션 엔진으로 구동하는 프로덕션 런처"
    )
    parser.add_argument("project_root", help="소비 프로젝트 루트(Contract vN 보유)")
    parser.add_argument("--mode", default="incremental", help="컴파일 모드(기본 incremental)")
    parser.add_argument("--phase", default="Phase 1", help="phase scope(기본 'Phase 1')")
    parser.add_argument("--run-id", default=None, help="run-id override(미지정 시 compile 값 슬러그)")
    parser.add_argument("--retry-limit", type=int, default=None,
                        help="retry_limit override(선택·smoke 지원)")
    parser.add_argument("--model", default=None,
                        help="seed 노드 model 슬롯 override(선택·smoke 티어 절감·예: haiku)")
    parser.add_argument("--policy", default="auto_approve",
                        choices=["interactive", "auto_approve", "unrestricted"],
                        help="Autonomy Policy(기본 auto_approve — headless 쓰기 가능·게이트와 직교)")
    parser.add_argument("--resume", action="store_true",
                        help="compile/조립 건너뛰고 기존 run_dir 로 구동")
    args = parser.parse_args(argv)

    # 미처리 예외 → logs/failure.json 기록 후 **재raise**(기존 규약대로 비영 종료 + 스택
    # 트레이스가 stderr 에 그대로 — 은폐 0·백로그 §L 2). 기존 정직 실패 경로([ERR] 출력 +
    # return 1)는 예외가 아니므로 이 래퍼를 통과하지 않는다(거동 보존).
    state: dict = {"run_dir": None, "run_id": args.run_id}
    try:
        return _drive(args, state)
    except SystemExit:
        raise
    except BaseException as exc:  # noqa: BLE001  (기록 후 즉시 재raise — 삼키지 않는다)
        _record_failure(
            state.get("run_dir"), state.get("run_id"),
            list(argv) if argv is not None else sys.argv[1:], exc,
        )
        raise


def _drive(args: Any, state: dict) -> int:
    """파싱된 인자로 run 을 준비·구동한다(main 의 구동 경로 본체·관측 래퍼 대상).

    `state` 는 관측용 출력 채널이다 — run_dir·run_id 가 확정되는 즉시 담아, 이후 미처리
    예외가 나면 `_record_failure` 가 **어느 run 에서 터졌는지** 기록할 수 있게 한다.
    """
    root = Path(args.project_root).resolve()

    if args.resume:
        slug = _resolve_slug(args.run_id, args.phase, root.name)
        run_dir = RUNS_DIR / slug
        if not run_dir.exists():
            # 기존 라인 **바이트 보존** 후 실존 후보 목록을 덧붙인다(백로그 §L 5) — `--run-id`
            # 를 생략하면 슬러그가 `--phase` 에서 재파생돼 **실재하지 않는 경로**를 보는데,
            # 종전 메시지는 "부재"만 알리고 옆에 있는 실제 run 을 알려주지 않았다.
            print("[ERR] --resume 대상 run_dir 부재: %s" % run_dir, file=sys.stderr)
            candidates = _run_dir_candidates()
            if candidates:
                print("[HINT] RUNS_DIR 실존 run 후보(수정시각 최신순·최대 10): %s"
                      % ", ".join(candidates), file=sys.stderr)
                print("[HINT] 재개는 run-id 를 명시한다: --resume --run-id <위 이름 중 하나>"
                      " (생략 시 --phase 에서 재파생된다)", file=sys.stderr)
            else:
                print("[HINT] RUNS_DIR 에 실존 run 디렉터리가 없다: %s" % RUNS_DIR,
                      file=sys.stderr)
            return 1
        state["run_dir"] = run_dir
        state["run_id"] = run_dir.name
        with open(run_dir / "config.json", "r", encoding="utf-8") as fh:
            config = json.load(fh)
        # --resume 에서도 --retry-limit override 를 config 에 반영한다(비반영이면 CLI 플래그가
        # 조용히 무시돼 관측이 어긋난다 — 침묵 금지). 재작업 되돌림은 한도와 무관하게 1회
        # 추가 시도를 부여하므로(엔진 설계) 이 override 는 편의이지 해소의 전제가 아니다.
        if args.retry_limit is not None:
            before = config.get("retry_limit")
            after = int(args.retry_limit)
            config["retry_limit"] = after
            _write_json(run_dir / "config.json", config)
            print("[CONFIG] retry_limit %s -> %s (--resume override 반영·config.json 재기록)"
                  % (before, after))
    else:
        try:
            run_dir, config = prepare_run(
                root, mode=args.mode, phase_scope=args.phase,
                run_id=args.run_id, retry_limit=args.retry_limit,
                model=args.model, policy=args.policy,
            )
        except (FileNotFoundError, RuntimeError) as exc:
            print("[ERR] %s" % exc, file=sys.stderr)
            return 1
        state["run_dir"] = run_dir
        state["run_id"] = config.get("run_id")

    # 러너 PID 기록(외부 관측용·run_k 선례).
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    with open(run_dir / "logs" / "host.pid", "w", encoding="utf-8") as fh:
        fh.write(str(os.getpid()))

    # 실 claude CLI invoker(LoggingClaudeInvoker) — e2e make_invoker 재사용.
    wire_paths()
    from _orch_common import make_invoker  # noqa: E402  (무수정 재사용)
    # 하트비트 래퍼(백로그 §L 1) — 원 invoker 를 감싸 invoke 시작·종료마다 진행 증거를 남긴다.
    # 인터페이스 투과이므로 엔진·중립 조립부에서 본 거동은 불변이다.
    invoker = HeartbeatInvoker(make_invoker(run_dir, config), run_dir)

    orch, _cfg = build(run_dir, invoker)
    return run_and_map(orch, invoker, run_dir)


def _force_utf8_console() -> None:
    """CLI 진입 시 stdout/stderr 를 UTF-8 로 재구성한다(Windows cp949 콘솔 방어).

    정지 게이트 시 render_gates 사람 친화 블록(한국어 문면)을 자동 출력하므로, cp949 등
    비-UTF-8 콘솔에서도 렌더가 `[RENDER-SKIP]` 로 떨어지지 않고 실제 표면화되게 한다(§3.2
    런처 자동 출력 취지 보존). 재구성 가능한 TextIOWrapper 일 때만 적용·실패 무시(어댑터
    격리 지점의 물리 표면 보정·중립 코드 무변경). 테스트는 main()/run_and_map 을 직접
    호출하므로 이 경로 미경유·무영향.
    """
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfig = getattr(stream, "reconfigure", None)
        if reconfig is not None:
            try:
                reconfig(encoding="utf-8")
            except (ValueError, OSError):
                pass


if __name__ == "__main__":
    _force_utf8_console()
    sys.exit(main())
