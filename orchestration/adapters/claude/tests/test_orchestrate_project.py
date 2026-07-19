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

import io
import json
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
    ROLE_VERIFIER,
)


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


if __name__ == "__main__":
    unittest.main()
