"""S5 dogfooding E2E (시나리오 j) — 공통 하네스 (Project Orchestration·형태 B).

이 모듈은 S2~S5 확정·커밋된 중립 코드를 *수정하지 않고* 실 claude CLI 로 구동하기 위한
E2E 하네스다. 여기는 Adapter 경계(orchestration-data/) 이하이므로 provider 토큰(claude CLI·
모델 별칭·권한 플래그) 사용이 허용된다(격리 지점 — step-data/e2e 선례 동형). **비프로덕션**
드라이버다 — 배포물이 아니라 dogfooding 실증 도구다.

핵심 원칙(L-07·O5):
  - 중립 Orchestrator(orchestration/framework/orchestrator/)·중립 Host(framework/loop/
    step-host/)·ClaudeInvoker(step-invoker/)는 그대로 라이브러리로 무수정 사용한다.
    LoggingClaudeInvoker 는 ClaudeInvoker 를 *상속*만 하며(super() 로 실제 코드 경로 실행),
    build_command/parse_result 훅에서 argv·원출력·종료 코드·판정 kind 를 logs/ 에 캡처한다.
  - run 데이터 백엔드 = orchestration-data/runs/<run-id>/ (바인딩 §5.3 구조·step-data 선례).
    events.jsonl(step 이벤트+게이트 이벤트)·revisions.jsonl(그래프 revision 원장)·
    artifacts.jsonl(산출물 선언 원장)·graph.json(초기 그래프)·gate_policy.json(정책 데이터)·
    steps/(단위별 직렬화 뷰)·workspace/(호스팅 세션 산출)·logs/(invoke 캡처).
  - 정지 신호 = 종료 코드 2 (바인딩 §5.3). 게이트 정지 시 러너가 sys.exit(2).
  - 실 CLI 실패는 은폐하지 않는다(O5) — 캡처·보고한다.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

# --- 경로 배선: 커밋된 중립 코드를 import 경로에 둔다 -------------------------------
HERE = Path(__file__).resolve().parent                       # .../orchestration-data/e2e
CLAUDE_DIR = HERE.parents[1]                                 # .../framework/adapters/claude
STEP_INVOKER_DIR = CLAUDE_DIR / "step-invoker"               # .../claude/step-invoker
STEP_HOST_DIR = CLAUDE_DIR.parents[1] / "loop" / "step-host" # .../framework/loop/step-host
REPO_ROOT = CLAUDE_DIR.parents[3]                            # repo root
ORCH_DIR = REPO_ROOT / "orchestration" / "framework" / "orchestrator"  # 중립 Orchestrator
RUNS_DIR = CLAUDE_DIR / "orchestration-data" / "runs"

for p in (str(ORCH_DIR), str(STEP_HOST_DIR), str(STEP_INVOKER_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

# 커밋된 코드 (무수정 사용).
from claude_invoker import ClaudeInvoker  # noqa: E402
from invoker import InvokeRequest, InvokeResult  # noqa: E402


class LoggingClaudeInvoker(ClaudeInvoker):
    """ClaudeInvoker 상속 로깅 래퍼 — 실제 코드 경로를 super() 로 그대로 실행하고
    각 invoke 의 조립 argv·원출력·종료 코드·판정 kind·session_id 를 logs/ 에 캡처한다.

    커밋된 claude_invoker.py 는 무수정이다. 이 래퍼는 orchestration-data/e2e/ 경계 소속이다.
    """

    def __init__(self, *args: Any, logs_dir: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.logs_dir = logs_dir
        self.invoke_count = 0
        self._ctx: dict[str, Any] = {}

    def _bundle_ctx(self, request: InvokeRequest) -> dict[str, Any]:
        sc = request.bundle.get("step_contract") or {}
        gate = request.bundle.get("gate") or {}
        return {
            "role": request.role,
            "step_id": sc.get("id"),
            "gate_id": gate.get("gate_id"),
            "model": request.model,
            "policy": request.policy,
            "feedback": request.bundle.get("feedback"),
        }

    def build_command(self, request: InvokeRequest) -> list:
        cmd = super().build_command(request)
        self._ctx = self._bundle_ctx(request)
        self._ctx["argv"] = list(cmd)
        return cmd

    def parse_result(self, stdout: str, returncode: int) -> InvokeResult:
        result = super().parse_result(stdout, returncode)
        self.invoke_count += 1
        self._write_log(stdout, returncode, result)
        return result

    def _write_log(self, stdout: str, returncode: int, result: InvokeResult) -> None:
        if not self.logs_dir:
            return
        os.makedirs(self.logs_dir, exist_ok=True)
        ctx = dict(self._ctx)
        seq = self.invoke_count
        role = ctx.get("role") or "Worker"
        step_id = ctx.get("step_id") or ctx.get("gate_id") or "unknown"
        session_id = None
        result_text = None
        try:
            env = json.loads(stdout) if stdout else None
            if isinstance(env, dict):
                session_id = env.get("session_id")
                result_text = env.get("result")
        except (ValueError, TypeError):
            pass
        entry = {
            "invoke_seq": seq,
            "role": role,
            "step_id": step_id,
            "gate_id": ctx.get("gate_id"),
            "model": ctx.get("model"),
            "policy": ctx.get("policy"),
            "feedback_present": ctx.get("feedback") is not None,
            "argv": ctx.get("argv"),
            "returncode": returncode,
            "result_kind": result.kind,
            "session_id": session_id,
            "result_text": result_text,
            "raw_stdout": stdout,
        }
        fname = "invoke-%02d-%s-%s.json" % (seq, role, step_id)
        with open(os.path.join(self.logs_dir, fname), "w", encoding="utf-8") as fh:
            json.dump(entry, fh, ensure_ascii=False, indent=2)


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def build_orchestrator(run_dir: Path, invoker: Any):
    """run 데이터 백엔드에서 중립 Orchestrator 를 조립한다(JSONL 이중 원장 + 선언 원장).

    - 초기 그래프 = graph.json (full Task dict — 게이트 descriptor 용 unitType 등 보존).
    - revision 원장 = revisions.jsonl (JsonlRevisionStore·append-only).
    - step 이벤트 로그 = events.jsonl (JsonlEventStore·게이트 이벤트 동거).
    - 산출물 선언 원장 = artifacts.jsonl (JsonlArtifactDeclarationStore·append-only).
    - gate 정책 = gate_policy.json (GatePolicy.from_dict).
    Orchestrator·Host 는 무수정 라이브러리로 import 된다(재정의 0).
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

    workdir = str(run_dir / "workspace")
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


def make_invoker(run_dir: Path, cfg: dict) -> LoggingClaudeInvoker:
    logs_dir = str(run_dir / "logs")
    os.makedirs(logs_dir, exist_ok=True)
    allowed = cfg.get("allowed_tools")
    extra: list = []
    if allowed:
        extra = ["--allowedTools"] + list(allowed)
    return LoggingClaudeInvoker(
        logs_dir=logs_dir,
        output_format=cfg.get("output_format", "json"),
        extra_args=extra,
    )
