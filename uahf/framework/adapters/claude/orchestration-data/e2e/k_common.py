"""시나리오 (k) 공통 배선 — _orch_common 무수정 재사용 + 외부 워크스페이스 빌더.

(k)는 (j)와 동일한 무수정 중립 코드(orchestration/framework/orchestrator/·
framework/loop/step-host/·step-invoker/claude_invoker.py)를 라이브러리로 쓴다.
_orch_common 을 **import 재사용**(수정 아님)하고, 다른 점은 단 하나 —
Orchestrator 의 workdir 를 config 의 `workspace_dir`(run 디렉터리 밖 절대경로)로 배선하는
`build_orchestrator_k` 뿐이다. 중립 코드 ProjectOrchestrator(workdir=...) 는 이미
파라미터이므로(orchestrator.py:116) 외부 워크스페이스는 config 데이터로만 실현된다
(중립 코드 무수정·07 격리 경계).

LoggingClaudeInvoker·load_json·RUNS_DIR·make_invoker 는 _orch_common 것을 그대로 재사용한다.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

# _orch_common import 가 중립 코드 경로를 sys.path 에 배선한다(모듈 로드 시점·38~40행).
from _orch_common import (  # noqa: F401  (재수출)
    LoggingClaudeInvoker,
    RUNS_DIR,
    load_json,
    make_invoker,
)


def build_orchestrator_k(run_dir: Path, invoker: Any):
    """run 데이터 백엔드에서 중립 Orchestrator 를 조립한다(_orch_common.build_orchestrator 동형).

    유일한 차이: workdir = config 의 `workspace_dir`(절대경로). 부재 시 run_dir/workspace
    기본값(j 거동)으로 폴백한다. 그 외 이중 원장·선언 원장·게이트 정책 배선은 (j)와 바이트
    동형이다(무수정 라이브러리 import·재정의 0).
    """
    from orchestrator import ProjectOrchestrator
    from revision import JsonlRevisionStore, RevisionLedger
    from gates import GatePolicy
    from artifacts import JsonlArtifactDeclarationStore
    from events import JsonlEventStore

    cfg = load_json(run_dir / "config.json")
    initial_graph = load_json(run_dir / "graph.json")
    gate_policy = GatePolicy.from_dict(load_json(run_dir / "gate_policy.json"))

    ledger = RevisionLedger(
        JsonlRevisionStore(str(run_dir / "revisions.jsonl")), initial_graph
    )
    event_store = JsonlEventStore(str(run_dir / "events.jsonl"))
    art_store = JsonlArtifactDeclarationStore(str(run_dir / "artifacts.jsonl"))

    # 외부 워크스페이스(run 디렉터리 밖 절대경로)를 config 데이터로만 실현한다.
    workspace = cfg.get("workspace_dir")
    workdir = str(Path(workspace)) if workspace else str(run_dir / "workspace")
    os.makedirs(workdir, exist_ok=True)

    orch = ProjectOrchestrator(
        ledger,
        event_store,
        invoker,
        retry_limit=cfg.get("retry_limit", 2),
        policy=cfg.get("policy", "auto_approve"),
        workdir=workdir,
        timeout=cfg.get("timeout"),
        gate_policy=gate_policy,
        artifact_store=art_store,
        run_id=cfg.get("run_id"),
    )
    return orch, cfg
