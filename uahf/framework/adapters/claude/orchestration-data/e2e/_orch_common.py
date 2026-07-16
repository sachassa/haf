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
from dataclasses import replace
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
from invoker import InvokeRequest, InvokeResult, ROLE_VERIFIER  # noqa: E402


class LoggingClaudeInvoker(ClaudeInvoker):
    """ClaudeInvoker 상속 로깅 래퍼 — 실제 코드 경로를 super() 로 그대로 실행하고
    각 invoke 의 조립 argv·원출력·종료 코드·판정 kind·session_id 를 logs/ 에 캡처한다.

    커밋된 claude_invoker.py 는 무수정이다. 이 래퍼는 orchestration-data/e2e/ 경계 소속이다.

    섀도 검증(선택·기본 off·T3 W3): shadow 설정이 켜지면 Verifier invoke(criteria 실재)를
    감지해 지정 상위 모델로 **병행 재호출**하고 두 판정(verdict)의 일치 여부를 섀도 로그에
    기록한다. **주 판정만 run 거동에 반영**되고 섀도는 관측 전용이다 — 섀도 재호출이 실패해도
    run 에 무영향(best-effort·swallow). shadow 미설정(기본)이면 invoke 거동은 byte 동일이다.
    """

    def __init__(
        self,
        *args: Any,
        logs_dir: str | None = None,
        shadow: dict | None = None,
        shadow_invoker_factory: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.logs_dir = logs_dir
        self.invoke_count = 0
        self._ctx: dict[str, Any] = {}
        # 섀도 검증 설정(기본 None → off·byte 동일 거동). shadow = {enabled, model, log_path?}.
        shadow = shadow or {}
        self.shadow_enabled: bool = bool(shadow.get("enabled"))
        self.shadow_model: Any = shadow.get("model")
        self.shadow_log_path: Any = shadow.get("log_path")
        # 섀도 재호출용 invoker 팩토리(테스트 주입점·합성 스텁). 미지정이면 실 ClaudeInvoker.
        self.shadow_invoker_factory = shadow_invoker_factory
        self.shadow_count = 0

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

    # ------------------------------------------------------------------
    # 섀도 검증(선택·기본 off·관측 전용·best-effort) — T3 W3
    # ------------------------------------------------------------------
    def _primary_invoke(self, request: InvokeRequest) -> InvokeResult:
        """주 invoke 경로(무수정 ClaudeInvoker.invoke). 이 seam 을 통해 테스트가 CLI 없이 주
        판정을 주입해 섀도 로직을 검증한다(합성 스텁·실 CLI 0). 기본은 실제 코드 경로다."""
        return ClaudeInvoker.invoke(self, request)

    def invoke(self, request: InvokeRequest) -> InvokeResult:
        """주 invoke(무수정 코드 경로) 실행 후, 섀도가 켜져 있고 적용 대상이면 병행 재호출한다.

        반환은 **주 판정 그대로**다 — 섀도는 run 거동에 반영되지 않는다(관측 전용). 섀도 경로의
        어떤 예외도 삼켜 run 을 오염시키지 않는다(best-effort·O5 은폐 아님 — 실패 사실은 섀도
        로그에 error 로 남는다). shadow off(기본)이면 주 경로 그대로라 byte 동일이다.
        """
        result = self._primary_invoke(request)
        if self.shadow_enabled:
            try:
                self._maybe_shadow(request, result)
            except Exception as exc:  # noqa: BLE001  (관측 전용·run 무영향)
                self._write_shadow_error(request, exc)
        return result

    def _shadow_applicable(self, request: InvokeRequest) -> bool:
        """섀도 대상 = Verifier 역할 + criteria 실재 + 섀도 모델 지정(검증 판정 재확인 축)."""
        if request.role != ROLE_VERIFIER or not self.shadow_model:
            return False
        criteria = request.criteria if request.criteria is not None else (request.bundle or {}).get("criteria")
        return bool(criteria)

    def _new_shadow_invoker(self) -> Any:
        """섀도 재호출용 invoker — 주입 팩토리 우선(테스트 스텁), 없으면 실 ClaudeInvoker."""
        if self.shadow_invoker_factory is not None:
            return self.shadow_invoker_factory()
        return ClaudeInvoker(cli=self.cli, output_format=self.output_format,
                             extra_args=list(self.extra_args))

    @staticmethod
    def _verdict_of(result: Any) -> Any:
        comp = getattr(result, "completion", None) or {}
        return comp.get("verdict")

    def _shadow_log_target(self) -> str | None:
        if self.shadow_log_path:
            return str(self.shadow_log_path)
        if self.logs_dir:
            return os.path.join(self.logs_dir, "shadow-verify.jsonl")
        return None

    def _maybe_shadow(self, request: InvokeRequest, primary: InvokeResult) -> None:
        if not self._shadow_applicable(request):
            return
        shadow_req = replace(request, model=self.shadow_model)
        inv = self._new_shadow_invoker()
        shadow_result = inv.invoke(shadow_req)
        self.shadow_count += 1
        primary_v = self._verdict_of(primary)
        shadow_v = self._verdict_of(shadow_result)
        comparable = primary_v is not None and shadow_v is not None
        entry = {
            "shadow_seq": self.shadow_count,
            "role": request.role,
            "step_id": (request.bundle.get("step_contract") or {}).get("id"),
            "gate_id": (request.bundle.get("gate") or {}).get("gate_id"),
            "primary_model": request.model,
            "shadow_model": self.shadow_model,
            "primary_verdict": primary_v,
            "shadow_verdict": shadow_v,
            "primary_kind": getattr(primary, "kind", None),
            "shadow_kind": getattr(shadow_result, "kind", None),
            "comparable": comparable,
            "agreement": (primary_v == shadow_v) if comparable else None,
            "note": "섀도 검증(관측 전용) — 주 판정만 run 에 반영. 병행 재호출은 상위 모델로 "
                    "Verifier 판정을 재확인해 일치 여부만 기록한다(run 거동 무영향).",
        }
        self._append_shadow(entry)

    def _write_shadow_error(self, request: InvokeRequest, exc: Exception) -> None:
        self.shadow_count += 1
        self._append_shadow({
            "shadow_seq": self.shadow_count,
            "role": request.role,
            "step_id": (request.bundle.get("step_contract") or {}).get("id"),
            "shadow_model": self.shadow_model,
            "error": "%s: %s" % (type(exc).__name__, exc),
            "note": "섀도 재호출 실패(best-effort) — 주 판정은 정상 반영됨. run 무영향.",
        })

    def _append_shadow(self, entry: dict) -> None:
        target = self._shadow_log_target()
        if not target:
            return
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def resolve_allocation(run_dir: Path, cfg: dict, allocation_path: Any = None):
    """(선택) Allocation 정책 데이터를 로드한다 — Risk-based Model Routing 배선(T3 W2).

    우선순위: 명시 인자 allocation_path > cfg["allocation_file"] > None(미배선). 경로는
    절대경로이거나 이 e2e 디렉터리(HERE) 기준 상대경로다. 부재 시 None 을 반환해 orchestrator
    가 슬롯 채움을 하지 않는다(현행 거동 완전 보존·하위호환). 신규 run 만 정책을 배선하며,
    시나리오가 model 슬롯을 명시 지정하면 그 값이 우선한다(명시값 우선·05 §3.4·§3.5).
    """
    from allocation import Allocation  # 무수정 중립 코드(ORCH_DIR 이 sys.path 에 배선됨).

    ref = allocation_path if allocation_path is not None else cfg.get("allocation_file")
    if not ref:
        return None
    p = Path(ref)
    if not p.is_absolute():
        p = HERE / ref
    return Allocation.from_file(str(p))


def build_orchestrator(run_dir: Path, invoker: Any, allocation_path: Any = None):
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

    allocation = resolve_allocation(run_dir, cfg, allocation_path)

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
        allocation=allocation,
    )
    return orch, cfg


def make_invoker(run_dir: Path, cfg: dict) -> LoggingClaudeInvoker:
    logs_dir = str(run_dir / "logs")
    os.makedirs(logs_dir, exist_ok=True)
    allowed = cfg.get("allowed_tools")
    extra: list = []
    if allowed:
        extra = ["--allowedTools"] + list(allowed)
    # 섀도 검증 설정(선택·config 주도·기본 off). cfg["shadow_verify"] = {enabled, model, log_path?}.
    return LoggingClaudeInvoker(
        logs_dir=logs_dir,
        output_format=cfg.get("output_format", "json"),
        extra_args=extra,
        shadow=cfg.get("shadow_verify"),
    )
