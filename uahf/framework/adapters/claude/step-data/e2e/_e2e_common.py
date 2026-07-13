"""W3 dogfooding E2E — 공통 하네스 (형태 B Step Hosting).

이 모듈은 W2 확정·커밋된 코드를 *수정하지 않고* 실 claude CLI 로 구동하기 위한
E2E 하네스다. 여기는 Adapter 경계(step-data/) 이하이므로 provider 토큰 사용이 허용된다.

핵심 원칙:
  - 중립 Host(framework/loop/step-host/)와 ClaudeInvoker(step-invoker/)는 그대로 사용한다.
    LoggingClaudeInvoker 는 ClaudeInvoker 를 *상속*만 하며(super() 로 실제 코드 경로 실행),
    build_command/parse_result 훅에서 argv·원출력·종료 코드·판정 kind 를 logs/ 에 캡처한다.
    -> 커밋된 코드는 무수정으로 실제 실행된다.
  - run 데이터 백엔드 = step-data/runs/<run-id>/ (바인딩 §3.2 구조).
  - 정지 신호 = 종료 코드 2 (바인딩 §5.3). 런처가 stop_handler 를 sys.exit(2) 로 바인딩.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

# --- 경로 배선: 커밋된 중립 Host·claude invoker 를 import 경로에 둔다 ---------------
HERE = Path(__file__).resolve().parent                 # .../claude/step-data/e2e
CLAUDE_DIR = HERE.parents[1]                            # .../framework/adapters/claude
STEP_INVOKER_DIR = CLAUDE_DIR / "step-invoker"          # .../claude/step-invoker
STEP_HOST_DIR = CLAUDE_DIR.parents[1] / "loop" / "step-host"  # .../framework/loop/step-host
REPO_ROOT = CLAUDE_DIR.parents[3]                       # .../universa-agentic-harness-framework
RUNS_DIR = CLAUDE_DIR / "step-data" / "runs"

for p in (str(STEP_HOST_DIR), str(STEP_INVOKER_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

# 커밋된 W2 코드 (무수정 사용).
from claude_invoker import ClaudeInvoker  # noqa: E402
from invoker import InvokeRequest, InvokeResult, ROLE_ADVISOR  # noqa: E402


class LoggingClaudeInvoker(ClaudeInvoker):
    """ClaudeInvoker 상속 로깅 래퍼 — 실제 코드 경로를 super() 로 그대로 실행하고
    각 invoke 의 조립 argv·원출력·종료 코드·판정 kind 를 logs/ 에 캡처한다.

    커밋된 claude_invoker.py 는 무수정이다. 이 래퍼는 step-data/e2e/ 경계 소속이다.
    """

    def __init__(self, *args: Any, logs_dir: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.logs_dir = logs_dir
        self.invoke_count = 0
        self._ctx: dict[str, Any] = {}

    def _bundle_ctx(self, request: InvokeRequest) -> dict[str, Any]:
        sc = request.bundle.get("step_contract") or {}
        return {
            "role": request.role,
            "step_id": sc.get("id"),
            "model": request.model,
            "policy": request.policy,
            "feedback": request.bundle.get("feedback"),
        }

    def build_command(self, request: InvokeRequest) -> list:
        cmd = super().build_command(request)
        # invoke() 내부에서 build_command 가 호출되는 시점의 컨텍스트를 stash 한다.
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
        step_id = ctx.get("step_id") or "unknown"
        # 봉투에서 session_id 를 추출(fresh 세션 실증용).
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
            "model": ctx.get("model"),
            "policy": ctx.get("policy"),
            "feedback_present": ctx.get("feedback") is not None,
            "feedback": ctx.get("feedback"),
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


def load_config(run_dir: Path) -> dict[str, Any]:
    with open(run_dir / "config.json", "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_steps(run_dir: Path, order: list) -> list:
    from step import Step  # 지연 import (경로 배선 후)
    steps = []
    for sid in order:
        with open(run_dir / "steps" / (sid + ".json"), "r", encoding="utf-8") as fh:
            data = json.load(fh)
        steps.append(Step.from_dict(data))
    return steps


def resolve_workdir(run_dir: Path, mode: str) -> str:
    if mode == "repo_root":
        return str(REPO_ROOT)
    ws = run_dir / "workspace"
    os.makedirs(ws, exist_ok=True)
    return str(ws)


def make_invoker(logs_dir: str, allowed_tools: list | None, output_format: str = "json"):
    extra: list = []
    if allowed_tools:
        extra = ["--allowedTools"] + list(allowed_tools)
    return LoggingClaudeInvoker(
        logs_dir=logs_dir,
        output_format=output_format,
        extra_args=extra,
    )
