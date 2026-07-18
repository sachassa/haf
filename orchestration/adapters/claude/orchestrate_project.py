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
  - status=="stopped"(그 외·Escalated) → exit 2.
  - completed → 0.  halted → 3.

이 모듈은 stdlib + 기존 저장소 모듈 import 만 쓴다(외부 패키지 0·오프라인 안전).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
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
    예: "orch-tms-Phase 1" → "orch-tms-Phase-1"(공백 제거). 빈 결과는 "run" 으로 폴백한다.
    """
    s = _SLUG_UNSAFE.sub("-", str(raw)).strip("-._")
    return s or "run"


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
        return 2

    if result.status == "stopped":
        print("[STOP] escalated -> exit code 2")
        return 2

    if result.completed:
        print("[COMPLETE] all units Passed.")
        return 0

    print("[HALTED] not completed, not stopped.")
    return 3


# --------------------------------------------------------------------------
# CLI — 실 claude CLI 발화(make_invoker) 경로
# --------------------------------------------------------------------------
def _resolve_slug(run_id: Any, phase_scope: str) -> str:
    """resume 시 run_dir 이름을 재현하기 위한 슬러그 산출(compile 과 동일 규칙)."""
    if run_id:
        return slugify_run_id(run_id)
    return slugify_run_id("orch-tms-" + str(phase_scope))


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

    root = Path(args.project_root).resolve()

    if args.resume:
        slug = _resolve_slug(args.run_id, args.phase)
        run_dir = RUNS_DIR / slug
        if not run_dir.exists():
            print("[ERR] --resume 대상 run_dir 부재: %s" % run_dir, file=sys.stderr)
            return 1
        with open(run_dir / "config.json", "r", encoding="utf-8") as fh:
            config = json.load(fh)
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

    # 러너 PID 기록(외부 관측용·run_k 선례).
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    with open(run_dir / "logs" / "host.pid", "w", encoding="utf-8") as fh:
        fh.write(str(os.getpid()))

    # 실 claude CLI invoker(LoggingClaudeInvoker) — e2e make_invoker 재사용.
    wire_paths()
    from _orch_common import make_invoker  # noqa: E402  (무수정 재사용)
    invoker = make_invoker(run_dir, config)

    orch, _cfg = build(run_dir, invoker)
    return run_and_map(orch, invoker, run_dir)


if __name__ == "__main__":
    sys.exit(main())
