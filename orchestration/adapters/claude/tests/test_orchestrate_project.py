"""orchestrate_project (F3 프로덕션 런처) 오프라인 테스트 — 실 LLM 미발화(stdlib unittest).

위임 done 1~6 을 실제 코드로 뒷받침한다:
  - done 1: dry-run 조립(no-op invoker) — run_dir 3종 파일 생성 + active_graph() seed fold +
            실 claude CLI 미발화 + project_root 소스 무변경(before/after 스냅샷 동일).
  - done 2: 워크스페이스 가드 — 존재 project_root 무삭제/무스캐폴드·부재 project_root 명확 에러.
  - done 3: exit-code 매핑 — stub invoker 유발 gate-stop → stop-signal.json + 2, completed→0, halted→3.
  - done 4: run_id 슬러그 — --phase "Phase 1" → run_dir 디렉터리명 공백 없음.

중립 조립부(build_orchestrator_k)·중립 코드(orchestrator/)는 무수정 import 만 한다(재정의 0).
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# --- 경로 배선: 런처 모듈 디렉터리 ---------------------------------------------
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]          # orchestration/adapters/claude
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import orchestrate_project as op  # noqa: E402

# 런처가 e2e + 중립 코드 경로를 배선한다(stephost_bridge import 를 위해 먼저 호출).
op.wire_paths()
from stephost_bridge import (  # noqa: E402  (무수정 import — 중립 코드)
    InvokeResult,
    KIND_COMPLETION,
    KIND_FAILURE,
    ROLE_VERIFIER,
)
from gates import GATE_ESCALATION_REQUIRED  # noqa: E402


# --------------------------------------------------------------------------
# 픽스처 — 임시 소비 project_root(Contract v1 심음)
# --------------------------------------------------------------------------
def _make_project_root(base: Path) -> Path:
    """base 안에 .claude/project-contract/project-contract.v1.md 를 심어 project_root 를 만든다.

    compile 은 resolve_contract(파일명 버전) 로만 계약을 소비하므로 v1 더미 1개면 충분하다
    (내용 파싱 0). solution-design.md 는 seed 프롬프트가 경로 문자열로만 참조하므로 불필요.
    """
    root = base / "consumer-project"
    cd = root / ".claude" / "project-contract"
    cd.mkdir(parents=True)
    (cd / "project-contract.v1.md").write_text("# dummy contract v1\n", encoding="utf-8")
    (root / "docs").mkdir(parents=True)  # 실 프로젝트 유사 구조(참조·수정 안 함).
    (root / "docs" / "solution-design.md").write_text("# sd\n", encoding="utf-8")
    return root


def _snapshot(root: Path) -> dict:
    """project_root 하위 전체 파일의 (상대경로 -> 내용) 스냅샷(소스 무변경 검증용)."""
    snap = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            snap[str(p.relative_to(root))] = p.read_bytes()
    return snap


class _NoInvoke:
    """no-op invoker — invoke 되면 실패한다(실 CLI 미발화 보장). 호출 여부를 기록한다."""

    def __init__(self) -> None:
        self.invoked = False

    def invoke(self, request):
        self.invoked = True
        raise RuntimeError("dry-run: no-op invoker 는 실행하지 않는다(실 CLI 미발화)")


class _StubInvoker:
    """중립 stub — Worker=완료 보고, Verifier=Pass. 실 provider/CLI 없음(오프라인 결정적).

    seed proposal 단위를 Passed 로 몰아 proposal→user_decision(정지 게이트) 발화를 유발한다.
    """

    def __init__(self) -> None:
        self.invoke_count = 0

    def invoke(self, request):
        self.invoke_count += 1
        if request.role == ROLE_VERIFIER:
            return InvokeResult(
                kind=KIND_COMPLETION,
                completion={"verdict": "Pass", "rework": None},
                ref="vd",
            )
        return InvokeResult(
            kind=KIND_COMPLETION,
            completion={
                "artifacts": ["impl-plan.json"], "self_check": "done",
                "failures": "없음", "open_questions": "없음", "verify_basis": "self",
            },
            ref="wr",
        )


class _FailingStubInvoker:
    """중립 stub — Worker=실패 보고(재시도 한도 소진 유발), Verifier=Pass. 실 CLI 없음.

    fail 을 False 로 바꾸면 이후 Worker 디스패치는 완료 보고를 낸다(해소 후 재시도 성공 모형).
    """

    def __init__(self, fail: bool = True) -> None:
        self.invoke_count = 0
        self.fail = fail
        self.worker_bundles: list = []

    def invoke(self, request):
        self.invoke_count += 1
        if request.role == ROLE_VERIFIER:
            return InvokeResult(
                kind=KIND_COMPLETION,
                completion={"verdict": "Pass", "rework": None},
                ref="vd",
            )
        self.worker_bundles.append(request.bundle)
        if self.fail:
            return InvokeResult(
                kind=KIND_FAILURE,
                failure={"reason": "실행 타임아웃", "repro": "동일 단위 재실행"},
                ref="fr",
            )
        return InvokeResult(
            kind=KIND_COMPLETION,
            completion={
                "artifacts": ["impl-plan.json"], "self_check": "done",
                "failures": "없음", "open_questions": "없음", "verify_basis": "self",
            },
            ref="wr",
        )


class _FakeResult:
    """run_and_map 매핑 검증용 합성 결과(엔진 미구동·매핑 로직만 결정적으로 친다)."""

    def __init__(self, status: str) -> None:
        self.status = status
        self.stop_reason = None
        self.stopped_tasks: list = []
        self.pending_gates: list = []
        self.epochs = 0
        self.graph_task_ids: list = []
        self.states: dict = {}

    @property
    def completed(self) -> bool:
        return self.status == "completed"


class _FakeOrch:
    def __init__(self, result) -> None:
        self._r = result

    def run(self):
        return self._r


# --------------------------------------------------------------------------
# 공통 — 테스트가 만든 run_dir 정리(실 RUNS_DIR 오염 방지)
# --------------------------------------------------------------------------
class _RunDirCleanup(unittest.TestCase):
    def setUp(self) -> None:
        self._run_dirs: list = []

    def tearDown(self) -> None:
        for rd in self._run_dirs:
            rd = Path(rd)
            # 안전: RUNS_DIR 직속만 삭제(가드 동형).
            if rd.exists() and rd.resolve().parent == op.RUNS_DIR.resolve():
                shutil.rmtree(rd, ignore_errors=True)

    def _track(self, run_dir) -> Path:
        run_dir = Path(run_dir)
        self._run_dirs.append(run_dir)
        return run_dir


# ==========================================================================
# done 1 — dry-run 조립(no-op invoker)
# ==========================================================================
class DryRunAssemblyTests(_RunDirCleanup):
    def test_assemble_creates_run_dir_and_seed_fold(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            before = _snapshot(root)

            run_dir, config = op.prepare_run(
                root, mode="incremental", phase_scope="Phase 1",
                run_id="orch-test-dryrun",
            )
            run_dir = self._track(run_dir)

            # 3종 데이터 파일 생성 확인(바인딩 §5.3).
            for fname in ("config.json", "graph.json", "gate_policy.json"):
                self.assertTrue((run_dir / fname).exists(), fname)
            for d in ("steps", "logs", "workspace"):
                self.assertTrue((run_dir / d).is_dir(), d)

            # no-op invoker 로 조립(실 CLI 미발화) → active_graph() seed fold 확인.
            noop = _NoInvoke()
            orch, cfg = op.build(run_dir, noop)
            graph = orch.active_graph()
            self.assertEqual(len(graph["tasks"]), 1, "seed 단일 proposal 노드")
            # seed id = seed_task_id(phase_scope) 파생 — phase_scope="Phase 1" → "impl-plan-phase-1".
            self.assertEqual(graph["tasks"][0]["id"], "impl-plan-phase-1")
            self.assertEqual(graph["tasks"][0]["unitType"], "proposal")

            # 실 claude CLI 미발화(no-op invoker 는 한 번도 호출되지 않음).
            self.assertFalse(noop.invoked, "no-op invoker 미호출(실 CLI 미발화)")

            # project_root 소스 무변경(before/after 스냅샷 동일).
            after = _snapshot(root)
            self.assertEqual(before, after, "project_root 소스 무변경")

            # config.workspace_dir 가 project_root 절대경로.
            self.assertEqual(Path(cfg["workspace_dir"]).resolve(), root.resolve())


# ==========================================================================
# done 2 — 워크스페이스 가드
# ==========================================================================
class WorkspaceGuardTests(_RunDirCleanup):
    def test_existing_project_root_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            before = _snapshot(root)
            run_dir, _cfg = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-test-guard",
            )
            run_dir = self._track(run_dir)
            op.build(run_dir, _NoInvoke())  # makedirs(workspace, exist_ok) 만 — 클로버 없음.
            after = _snapshot(root)
            self.assertEqual(before, after, "존재 project_root 무삭제·무스캐폴드")

    def test_absent_project_root_errors(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "does-not-exist"
            with self.assertRaises(FileNotFoundError):
                op.prepare_run(missing, phase_scope="Phase 1", run_id="orch-test-absent")

    def test_run_dir_outside_runs_dir_guarded(self) -> None:
        """RUNS_DIR 밖 run_dir 삭제 시도는 가드로 중단(오삭제 방지·소비 프로젝트 보존 원리)."""
        with tempfile.TemporaryDirectory() as td:
            outside = Path(td) / "not-a-run"
            outside.mkdir()
            with self.assertRaises(RuntimeError):
                op._materialize_run_dir(outside, "not-a-run", {}, {"tasks": []}, {})


# ==========================================================================
# done 3 — exit-code 매핑
# ==========================================================================
class ExitCodeMappingTests(_RunDirCleanup):
    def test_gate_stop_writes_signal_and_returns_2(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            run_dir, _cfg = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-test-gatestop",
            )
            run_dir = self._track(run_dir)

            stub = _StubInvoker()
            orch, _c = op.build(run_dir, stub)
            code = op.run_and_map(orch, stub, run_dir)

            self.assertEqual(code, 2, "정지 게이트 → exit 2")
            sig = run_dir / "logs" / "stop-signal.json"
            self.assertTrue(sig.exists(), "stop-signal.json 기록")
            marker = json.loads(sig.read_text(encoding="utf-8"))
            self.assertEqual(marker["stop_reason"], "gate")
            self.assertTrue(marker["pending_gates"], "미해소 게이트 큐 비어있지 않음")
            # 계약 필드(gate_id·gateKind) 실재.
            g0 = marker["pending_gates"][0]
            self.assertIn("gate_id", g0)
            self.assertIn("gateKind", g0)

    def test_gate_stop_preserves_lines_and_appends_render(self) -> None:
        # 회귀(OQ-PO-B1 배선): 정지 게이트 시 기존 [STOP]/[PENDING-GATES] 라인을 보존하고
        # 그 이후에 render_gates 사람 친화 블록을 추가 출력한다(렌더는 부가 표면·가법).
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            run_dir, _cfg = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-test-render",
            )
            run_dir = self._track(run_dir)

            stub = _StubInvoker()
            orch, _c = op.build(run_dir, stub)
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = op.run_and_map(orch, stub, run_dir)
            out = buf.getvalue()

            self.assertEqual(code, 2)
            # 기존 라인 보존(바이트 형태).
            self.assertIn("[STOP] gate pending=", out)
            self.assertIn("[PENDING-GATES] ", out)
            # 렌더 블록이 [PENDING-GATES] '이후'에 추가된다.
            self.assertIn("미해소 정지 게이트 큐", out)
            self.assertLess(out.index("[PENDING-GATES] "), out.index("미해소 정지 게이트 큐"))
            # 사용자 결정 게이트 라벨·해소 명령 표면화.
            self.assertIn("사용자 결정 대기(확정 권위)", out)
            self.assertIn("resolve_gate.py", out)

    def test_completed_returns_0(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "rd"
            (run_dir / "logs").mkdir(parents=True)
            code = op.run_and_map(_FakeOrch(_FakeResult("completed")), None, run_dir)
            self.assertEqual(code, 0)

    def test_halted_returns_3(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "rd"
            (run_dir / "logs").mkdir(parents=True)
            code = op.run_and_map(_FakeOrch(_FakeResult("halted")), None, run_dir)
            self.assertEqual(code, 3)

    def test_escalated_stop_returns_2(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "rd"
            (run_dir / "logs").mkdir(parents=True)
            res = _FakeResult("stopped")
            res.stop_reason = "escalated"
            code = op.run_and_map(_FakeOrch(res), None, run_dir)
            self.assertEqual(code, 2)


# ==========================================================================
# done 4 — run_id 슬러그
# ==========================================================================
class RunIdSlugTests(_RunDirCleanup):
    def test_phase_scope_slug_has_no_space(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            # run_id 미지정 → compile 값("orch-<root.name>-Phase 1")을 슬러그 정규화.
            # _make_project_root 의 root.name = "consumer-project".
            run_dir, cfg = op.prepare_run(root, phase_scope="Phase 1")
            run_dir = self._track(run_dir)
            self.assertNotIn(" ", run_dir.name, "run_dir 디렉터리명 공백 없음")
            self.assertEqual(run_dir.name, "orch-consumer-project-Phase-1")
            self.assertEqual(cfg["run_id"], run_dir.name, "config.run_id 일치")

    def test_slugify_unit(self) -> None:
        self.assertEqual(op.slugify_run_id("orch-myproj-Phase 1"), "orch-myproj-Phase-1")
        self.assertEqual(op.slugify_run_id("a/b:c*d"), "a-b-c-d")
        self.assertEqual(op.slugify_run_id("  spaced  "), "spaced")
        self.assertEqual(op.slugify_run_id("---"), "run")

    def test_resolve_slug_derives_from_root_name(self) -> None:
        # resume 재현 규칙 = compile 과 동일("orch-" + root.name + "-" + phase_scope·도메인 0).
        self.assertEqual(
            op._resolve_slug(None, "phase1", "consumer-ws"), "orch-consumer-ws-phase1"
        )
        self.assertEqual(
            op._resolve_slug(None, "Phase 1", "my-proj"), "orch-my-proj-Phase-1"
        )
        # --run-id override 우선.
        self.assertEqual(op._resolve_slug("custom id", "phase1", "x"), "custom-id")


# ==========================================================================
# 백로그 §J — escalated 정지의 stop-signal 기록(D4) · resume retry-limit override(D5) ·
# 접합부 왕복(런처 산출 stop-signal → resolve_gate 실호출 → 엔진 재디스패치)
# ==========================================================================
class EscalatedStopSignalTests(_RunDirCleanup):
    def _escalated_run(self, td: Path, run_id: str):
        """seed 단위를 재시도 한도(0) 소진으로 Escalated 시켜 런처 정지까지 몰고 간다."""
        root = _make_project_root(td)
        run_dir, _cfg = op.prepare_run(
            root, phase_scope="Phase 1", run_id=run_id, retry_limit=0)
        run_dir = self._track(run_dir)
        stub = _FailingStubInvoker(fail=True)
        orch, _c = op.build(run_dir, stub)
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = op.run_and_map(orch, stub, run_dir)
        return root, run_dir, stub, code, buf.getvalue()

    def test_escalated_stop_writes_contract_shaped_signal(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            _root, run_dir, _stub, code, out = self._escalated_run(Path(td), "orch-test-escsig")

            self.assertEqual(code, 2, "escalated 정지 → exit 2(기존 매핑 보존)")
            self.assertIn("[STOP] escalated -> exit code 2", out, "기존 라인 보존")
            self.assertIn("[PENDING-GATES] ", out)

            sig = run_dir / "logs" / "stop-signal.json"
            self.assertTrue(sig.exists(), "escalated 정지에도 stop-signal.json 기록(§J ①)")
            marker = json.loads(sig.read_text(encoding="utf-8"))
            self.assertEqual(
                sorted(marker.keys()),
                sorted(["stop_reason", "stopped_tasks", "pending_gates", "note"]),
                "게이트 분기와 같은 계약 형태 4필드",
            )
            self.assertEqual(marker["stop_reason"], "escalated")
            self.assertTrue(marker["stopped_tasks"], "정지 단위 실재")
            g0 = marker["pending_gates"][0]
            self.assertEqual(g0["gateKind"], GATE_ESCALATION_REQUIRED)
            self.assertEqual(g0["scoped_question"]["unitId"], marker["stopped_tasks"][0])

    def test_legacy_escalated_result_without_gates_notes_empty_queue(self) -> None:
        # pending_gates 가 빈(게이트 정책 부재 레거시) escalated 결과도 기록되고, note 가
        # 그 사실을 명시한다(침묵 0). 기존 exit 매핑 불변.
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "rd"
            (run_dir / "logs").mkdir(parents=True)
            res = _FakeResult("stopped")
            res.stop_reason = "escalated"
            code = op.run_and_map(_FakeOrch(res), None, run_dir)
            self.assertEqual(code, 2)
            marker = json.loads((run_dir / "logs" / "stop-signal.json").read_text(encoding="utf-8"))
            self.assertEqual(marker["pending_gates"], [])
            self.assertIn("pending_gates 가 비어 있다", marker["note"])

    def test_roundtrip_signal_to_resolver_to_redispatch(self) -> None:
        """접합부 왕복 — 런처가 **실제로 쓴** stop-signal → resolve_gate 실호출 → 엔진 재디스패치."""
        import resolve_gate as rg  # noqa: E402  (같은 어댑터 경계)

        with tempfile.TemporaryDirectory() as td:
            _root, run_dir, stub, code, _out = self._escalated_run(
                Path(td), "orch-test-roundtrip")
            self.assertEqual(code, 2)
            invokes_before = stub.invoke_count

            # (a) 런처 산출 실물 stop-signal.json → recover_gate 로 escalation gate_id 복원.
            gate_id, pending = rg.recover_gate(run_dir, GATE_ESCALATION_REQUIRED)
            self.assertIsNotNone(gate_id, "escalation gate_id 복원 실패: %r" % (pending,))

            # (b) resolver CLI **실호출**(main → recover_gate → resolve_escalation) →
            #     해소 이벤트 실물 append. 요약·재구성 없이 실제 산출을 흘린다.
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = rg.main([str(run_dir), "--gate-kind", "escalation",
                              "--actor", "Advisor",
                              "--response", "타임아웃 상향 후 재시도하라"])
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertIn("[NEXT]", buf.getvalue(), "재개 명령 안내 출력")
            self.assertIn("--resume", buf.getvalue())

            # (c) 같은 run 데이터를 엔진이 재기동 → 해소 소비 → 대상 단위 재디스패치.
            stub2 = _FailingStubInvoker(fail=False)
            orch2, _c2 = op.build(run_dir, stub2)
            result = orch2.run()
            self.assertGreater(stub2.invoke_count, 0, "해소 후 재디스패치 발생")
            self.assertGreater(stub2.invoke_count + invokes_before, invokes_before)

            # 되돌림 이벤트가 원장에 실재하고 해소 응답이 전파됐다(D2·D3).
            events = [json.loads(l) for l in
                      (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
            rework = [e for e in events if (e.get("ref") or {}).get("kind") == "gate-rework"]
            self.assertEqual(len(rework), 1)
            self.assertEqual(rework[0]["ref"]["response"], "타임아웃 상향 후 재시도하라")
            # 재개 결과는 정지 게이트(user_decision)로 이어진다 — 재디스패치가 실제로 진행됐다는 증거.
            self.assertTrue(result.stopped or result.completed, result.status)


class ResumeRetryLimitOverrideTests(_RunDirCleanup):
    def test_resume_applies_retry_limit_to_config(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            run_dir, cfg = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-test-resume-rl", retry_limit=1)
            run_dir = self._track(run_dir)
            self.assertEqual(cfg["retry_limit"], 1)

            # main() 의 resume 분기만 친다 — 실 invoker 조립·엔진 구동은 대체(오프라인).
            import _orch_common
            orig_make, orig_build = _orch_common.make_invoker, op.build
            _orch_common.make_invoker = lambda rd, config: _StubInvoker()
            op.build = lambda rd, invoker: (_FakeOrch(_FakeResult("completed")), {})
            try:
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = op.main([str(root), "--resume", "--run-id", "orch-test-resume-rl",
                                  "--retry-limit", "5"])
            finally:
                _orch_common.make_invoker, op.build = orig_make, orig_build

            self.assertEqual(rc, 0)
            self.assertIn("[CONFIG] retry_limit 1 -> 5", buf.getvalue())
            saved = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["retry_limit"], 5, "config.json 재기록")


# ==========================================================================
# 백로그 §L 1 — heartbeat(F2 정체 탐지) · failure isolation
# ==========================================================================
class HeartbeatTests(_RunDirCleanup):
    def test_stub_run_writes_heartbeat_with_invoke_end(self) -> None:
        """[done 1] stub invoker 로 엔진 구동 → heartbeat.json 마지막 기록 = invoke-end."""
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            run_dir, _cfg = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-test-heartbeat")
            run_dir = self._track(run_dir)

            hb_invoker = op.HeartbeatInvoker(_StubInvoker(), run_dir)
            orch, _c = op.build(run_dir, hb_invoker)
            buf = io.StringIO()
            with redirect_stdout(buf):
                op.run_and_map(orch, hb_invoker, run_dir)

            hb_path = run_dir / "logs" / op.HEARTBEAT_FILE
            self.assertTrue(hb_path.exists(), "logs/heartbeat.json 생성")
            beat = json.loads(hb_path.read_text(encoding="utf-8"))
            self.assertEqual(
                sorted(beat.keys()),
                sorted(["ts", "stage", "invokes", "request_hint", "pid"]),
                "하트비트 계약 필드 5종",
            )
            self.assertEqual(beat["stage"], "invoke-end", "마지막 기록 = invoke-end")
            self.assertGreaterEqual(beat["invokes"], 1)
            self.assertTrue(beat["ts"], "ts 실재")
            self.assertEqual(beat["pid"], os.getpid())
            # request_hint 는 최선값 — 이 엔진 경로에서는 실제 단위 식별이 실린다.
            self.assertIsNotNone(beat["request_hint"])

    def test_heartbeat_interface_passthrough(self) -> None:
        """래퍼가 원 invoker 속성을 투과한다 — 특히 run_and_map 이 읽는 invoke_count."""
        stub = _StubInvoker()
        w = op.HeartbeatInvoker(stub, Path("."))
        self.assertEqual(w.invoke_count, 0)
        stub.invoke_count = 7
        self.assertEqual(w.invoke_count, 7, "원 invoker 값 투과(관측 수치 왜곡 0)")
        with self.assertRaises(AttributeError):
            _ = w.no_such_attribute

    def test_heartbeat_write_failure_does_not_break_run(self) -> None:
        """[done 1] 하트비트 쓰기에 예외를 주입해도 run 결과·종료 코드가 불변(failure isolation)."""
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            # (a) 기준선 — 정상 하트비트로 구동.
            rd_ok, _ = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-test-hb-ok")
            rd_ok = self._track(rd_ok)
            ok_inv = op.HeartbeatInvoker(_StubInvoker(), rd_ok)
            orch_ok, _c = op.build(rd_ok, ok_inv)
            with redirect_stdout(io.StringIO()):
                code_ok = op.run_and_map(orch_ok, ok_inv, rd_ok)

            # (b) 대조 — _beat 내부에서 예외가 나도록 쓰기 경로를 깬다.
            rd_bad, _ = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-test-hb-bad")
            rd_bad = self._track(rd_bad)
            bad_inv = op.HeartbeatInvoker(_StubInvoker(), rd_bad)
            bad_inv._run_dir = Path("\x00invalid")  # mkdir/open 이 반드시 실패한다.
            orch_bad, _c2 = op.build(rd_bad, bad_inv)
            err = io.StringIO()
            with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                code_bad = op.run_and_map(orch_bad, bad_inv, rd_bad)

            self.assertEqual(code_bad, code_ok, "하트비트 실패에도 종료 코드 불변")
            self.assertEqual(code_bad, 2)
            self.assertTrue((rd_bad / "logs" / "stop-signal.json").exists(),
                            "run 산출(정지 신호) 불변")
            self.assertIn("[HEARTBEAT-SKIP]", err.getvalue(), "기록 실패는 stderr 로 표면화")
            self.assertGreater(bad_inv.invoke_count, 0, "invoke 는 정상 수행")


# ==========================================================================
# 백로그 §L 2 — failure.json(미처리 예외 구조화 기록)
# ==========================================================================
class FailureRecordTests(_RunDirCleanup):
    def _resume_with_injected_failure(self, td: Path, exc: BaseException):
        """resume 경로로 진입한 뒤 조립 단계에서 강제 예외를 던진다."""
        root = _make_project_root(td)
        run_dir, _cfg = op.prepare_run(
            root, phase_scope="Phase 1", run_id="orch-test-failrec")
        run_dir = self._track(run_dir)

        import _orch_common
        orig_make, orig_build = _orch_common.make_invoker, op.build

        def _boom(rd, invoker):
            raise exc

        _orch_common.make_invoker = lambda rd, config: _StubInvoker()
        op.build = _boom
        try:
            with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(type(exc)):
                    op.main([str(root), "--resume", "--run-id", "orch-test-failrec"])
        finally:
            _orch_common.make_invoker, op.build = orig_make, orig_build
        return run_dir

    def test_unhandled_exception_writes_failure_json(self) -> None:
        """[done 2] 강제 예외 → failure.json 계약 필드 6종 + 예외 재raise(비영 종료)."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = self._resume_with_injected_failure(
                Path(td), ZeroDivisionError("강제 주입 실패"))

            fp = run_dir / "logs" / op.FAILURE_FILE
            self.assertTrue(fp.exists(), "logs/failure.json 기록")
            rec = json.loads(fp.read_text(encoding="utf-8"))
            self.assertEqual(
                sorted(rec.keys()),
                sorted(["ts", "run_id", "argv", "error_type", "error", "traceback"]),
                "failure.json 계약 필드 6종",
            )
            self.assertEqual(rec["error_type"], "ZeroDivisionError")
            self.assertEqual(rec["error"], "강제 주입 실패")
            self.assertIn("ZeroDivisionError", rec["traceback"])
            self.assertEqual(rec["run_id"], "orch-test-failrec")
            self.assertIn("--resume", rec["argv"])
            self.assertTrue(rec["ts"])

    def test_honest_error_paths_return_1_without_failure_json(self) -> None:
        """[done 2] 기존 [ERR] 정직 실패 경로 거동 보존 — 예외가 아니므로 failure.json 없음."""
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "does-not-exist"
            err = io.StringIO()
            with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                rc = op.main([str(missing), "--run-id", "orch-test-honest"])
            self.assertEqual(rc, 1, "정직 실패 = return 1(예외 아님)")
            self.assertIn("[ERR] ", err.getvalue())
            self.assertFalse((op.RUNS_DIR / "orch-test-honest").exists())


# ==========================================================================
# 백로그 §P·§L 4-b — 런처 슬러그 상한 + 접합부 왕복 a(§5.7)
# ==========================================================================
class SlugLengthCapTests(_RunDirCleanup):
    _LONG_PHASE = "M1 defect fix " + ("alpha beta gamma delta " * 13)  # >300자 ASCII.

    def test_slugify_caps_long_input(self) -> None:
        """[done 3] 300자 ASCII 입력 → 결과 ≤57자·결정적·크래시 0."""
        raw = "orch-consumer-project-" + ("x" * 300)
        self.assertGreater(len(raw), 300)
        out = op.slugify_run_id(raw)
        self.assertLessEqual(len(out), 57)
        self.assertEqual(out, op.slugify_run_id(raw), "결정적")
        self.assertNotEqual(op.slugify_run_id(raw), op.slugify_run_id(raw + "y"))

    def test_slugify_short_input_byte_identical(self) -> None:
        """[done 3] 48자 이하 입력은 바이트 동일(기존 run 디렉터리 하위호환)."""
        self.assertEqual(op.slugify_run_id("orch-myproj-Phase 1"), "orch-myproj-Phase-1")
        self.assertEqual(op.slugify_run_id("a/b:c*d"), "a-b-c-d")
        self.assertEqual(op.slugify_run_id("---"), "run")
        self.assertEqual(op.slugify_run_id("z" * 48), "z" * 48)

    def test_long_phase_prepare_run_succeeds(self) -> None:
        """[done 3] 300자 ASCII --phase 로 prepare_run 이 run_dir 생성 성공(§P 크래시 해소)."""
        self.assertGreater(len(self._LONG_PHASE), 300)
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            run_dir, cfg = op.prepare_run(root, phase_scope=self._LONG_PHASE)
            run_dir = self._track(run_dir)
            self.assertTrue(run_dir.is_dir(), "긴 phase 로도 run_dir 물리 생성")
            self.assertLessEqual(len(run_dir.name), 57)
            self.assertEqual(cfg["run_id"], run_dir.name)
            # seed unit id 파일명도 실제로 만들어졌다(원장 커밋 불가 결함 지점).
            steps = list((run_dir / "steps").glob("*.json"))
            self.assertEqual(len(steps), 1)
            self.assertLess(len(steps[0].name), 80, steps[0].name)

    def test_prepare_run_dirname_matches_resolve_slug(self) -> None:
        """[done 4 · 접합부 왕복 a] prepare_run 실물 run_dir 이름 == _resolve_slug 재현값.

        생산자 = prepare_run(compile → slugify), 소비자 = --resume 의 `_resolve_slug`.
        두 경로가 어긋나면 resume 이 **실재하지 않는 경로**를 조용히 본다(백로그 §L 5).
        예시·재구성이 아니라 **실물 디렉터리 이름**으로 대조한다(§5.7).
        """
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            for phase in ("Phase 1", "phase1", self._LONG_PHASE):
                run_dir, _cfg = op.prepare_run(root, phase_scope=phase)
                run_dir = self._track(run_dir)
                self.assertEqual(
                    run_dir.name,
                    op._resolve_slug(None, phase, root.name),
                    "실물 run_dir 이름 ↔ resume 재파생 슬러그 왕복 일치: phase=%r" % phase,
                )


# ==========================================================================
# 백로그 §L 5 — --resume 부재 오류의 실존 후보 제시
# ==========================================================================
class ResumeMissingRunDirHintTests(unittest.TestCase):
    def test_error_lists_existing_candidates(self) -> None:
        """[done 5] 실물 run 디렉터리 2개를 만들고, 오류 메시지에 그 이름이 포함되는지 본다."""
        with tempfile.TemporaryDirectory() as td:
            fake_runs = Path(td) / "runs"
            (fake_runs / "orch-alpha-phase1").mkdir(parents=True)
            (fake_runs / "orch-beta-phase2").mkdir(parents=True)
            root = _make_project_root(Path(td))

            orig = op.RUNS_DIR
            op.RUNS_DIR = fake_runs
            try:
                err = io.StringIO()
                with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                    rc = op.main([str(root), "--resume", "--run-id", "orch-nope"])
            finally:
                op.RUNS_DIR = orig

            out = err.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("[ERR] --resume 대상 run_dir 부재", out, "기존 라인 보존")
            self.assertIn("orch-alpha-phase1", out, "실존 후보 이름 포함")
            self.assertIn("orch-beta-phase2", out, "실존 후보 이름 포함")
            self.assertIn("--resume --run-id", out, "올바른 사용법 안내")

    def test_empty_runs_dir_states_the_fact(self) -> None:
        """후보가 0건이면 그 사실을 명시한다(침묵 0)."""
        with tempfile.TemporaryDirectory() as td:
            fake_runs = Path(td) / "runs"
            fake_runs.mkdir()
            root = _make_project_root(Path(td))
            orig = op.RUNS_DIR
            op.RUNS_DIR = fake_runs
            try:
                err = io.StringIO()
                with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                    rc = op.main([str(root), "--resume", "--run-id", "orch-nope"])
            finally:
                op.RUNS_DIR = orig
            self.assertEqual(rc, 1)
            self.assertIn("실존 run 디렉터리가 없다", err.getvalue())


# ==========================================================================
# 접합부 왕복 b(§5.7) — 명령 문서 §2 예시 ↔ 런처 argparse 수용
# ==========================================================================
class CommandDocFlagRoundtripTests(unittest.TestCase):
    """`.claude/commands/uaf-implement.md` §2 가 가르치는 사용법을 런처가 실제로 받는가.

    백로그 §L 5 재발 실측의 근본 원인 = **문서가 틀린 사용법을 가르쳤다**(재개 예시가
    `--resume` 만 표기 → `--run-id` 를 준 run 은 반드시 실패). 문서(생산자) 예시를 런처
    파서(소비자)에 **실제로 통과**시켜 왕복을 닫는다(§5.7 — 예시가 아니라 실물 실행).
    """

    _DOC = (
        Path(__file__).resolve().parents[4] / ".claude" / "commands" / "uaf-implement.md"
    )

    def test_doc_teaches_run_id_on_resume(self) -> None:
        text = self._DOC.read_text(encoding="utf-8")
        self.assertIn("--resume --run-id", text,
                      "재개 예시가 --run-id 를 함께 표기해야 한다(백로그 §L 5)")

    def test_documented_flags_accepted_by_parser(self) -> None:
        flags = ["--resume", "--run-id", "X", "--retry-limit", "3",
                 "--phase", "Phase 1", "--mode", "incremental",
                 "--model", "haiku", "--policy", "auto_approve",
                 "--allocation-file", "policy/allocation-lightweight.json"]
        # 문서가 가르치는 플래그 집합이 파서에 실제로 수용되는지 — 부재 run_dir 오류(1)까지
        # 도달하면 파싱은 성공한 것이다(argparse 실패는 SystemExit 2).
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            fake_runs = Path(td) / "runs"
            fake_runs.mkdir()
            orig = op.RUNS_DIR
            op.RUNS_DIR = fake_runs
            try:
                with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    rc = op.main([str(root)] + flags)
            finally:
                op.RUNS_DIR = orig
            self.assertEqual(rc, 1, "파싱 성공(SystemExit 없음) 후 run_dir 부재로 1")

    def test_doc_exit_code_table_present(self) -> None:
        text = self._DOC.read_text(encoding="utf-8")
        for token in ("exit 0", "exit 2", "exit 3", "exit 1",
                      "heartbeat.json", "failure.json"):
            self.assertIn(token, text, token)


if __name__ == "__main__":
    unittest.main()
