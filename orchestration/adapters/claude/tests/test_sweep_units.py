"""횡단 결함 검지(백로그 §M D-M1·D-M2) 오프라인 테스트 — 실 LLM 미발화(stdlib unittest).

위임 done 1~4 를 실제 코드로 뒷받침한다:
  - done 1: `_seed_prompt` milestone 규칙에 단위 간 계약 정합 검사 의무 + 횡단 관점 지시 실재
            (기존 문면 — timeout 선택 키 항 포함 — 무삭제).
  - done 2: 런처 `[REWORK-NOTE]` — rework 실재 run 에서 단위 id·스윕 명령 힌트 출력 /
            rework 0 run 에서 무출력 / 원장 부재·파손 시 종료 코드·stdout 무변 + stderr 고지.
  - done 3: `sweep_units.py` — 히트 exit 2 / 무히트 exit 0 / 오류 exit 1 /
            디렉터리 재귀·바이너리 스킵 건수 보고. **실파일 픽스처**로만 판정한다.
  - done 4: 접합부 왕복 — 엔진 실구동(CP2 Fail→rework→재시도 Pass) → 실물 events.jsonl 판독
            → 같은 run_dir 에 sweep_units 실 argv 구동 → 워크스페이스 실파일 히트.

중립 조립부(build_orchestrator_k)·중립 코드(orchestrator/)는 무수정 import 만 한다(재정의 0).
"""

from __future__ import annotations

import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# --- 경로 배선: 어댑터 모듈 디렉터리 -------------------------------------------
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]          # orchestration/adapters/claude
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import contract_to_graph as ctg  # noqa: E402
import orchestrate_project as op  # noqa: E402
import sweep_units as sw  # noqa: E402

op.wire_paths()
from stephost_bridge import (  # noqa: E402  (무수정 import — 중립 코드)
    InvokeResult,
    KIND_COMPLETION,
    ROLE_VERIFIER,
)


# ==========================================================================
# 픽스처
# ==========================================================================
def _make_project_root(base: Path) -> Path:
    """Contract v1 을 심은 임시 소비 project_root(테스트 지역 헬퍼·기존 트리 무촉)."""
    root = base / "consumer-project"
    cd = root / ".claude" / "project-contract"
    cd.mkdir(parents=True)
    (cd / "project-contract.v1.md").write_text("# dummy contract v1\n", encoding="utf-8")
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "solution-design.md").write_text("# sd\n", encoding="utf-8")
    return root


class _PassStub:
    """Worker=완료 보고·Verifier=Pass. rework 이벤트가 발생하지 않는 대조군."""

    def __init__(self, workspace: Path | None = None, payload: str = "{}\n") -> None:
        self.invoke_count = 0
        self._ws = workspace
        self._payload = payload

    def _emit(self) -> None:
        if self._ws is not None:
            (self._ws / ctg.IMPL_PLAN_FILE).write_text(self._payload, encoding="utf-8")

    def invoke(self, request):
        self.invoke_count += 1
        if request.role == ROLE_VERIFIER:
            return InvokeResult(kind=KIND_COMPLETION,
                                completion={"verdict": "Pass", "rework": None}, ref="vd")
        self._emit()
        return InvokeResult(
            kind=KIND_COMPLETION,
            completion={"artifacts": [ctg.IMPL_PLAN_FILE], "self_check": "done",
                        "failures": "없음", "open_questions": "없음", "verify_basis": "self"},
            ref="wr",
        )


_REWORK_TEXT = "산출이 done AC 를 판별하지 못한다 — 재작업"


class _ReworkThenPassStub(_PassStub):
    """CP2 가 **첫 판정만 Fail**(rework 지시) 후 Pass — host `_record_failure` 의
    `ref.kind=="rework"` 이벤트를 실제로 원장에 남기는 유일한 경로다(합성 append 아님)."""

    def __init__(self, workspace: Path | None = None, payload: str = "{}\n") -> None:
        super().__init__(workspace, payload)
        self.verdicts = 0

    def invoke(self, request):
        if request.role == ROLE_VERIFIER:
            self.invoke_count += 1
            self.verdicts += 1
            if self.verdicts == 1:
                return InvokeResult(
                    kind=KIND_COMPLETION,
                    completion={"verdict": "Fail", "rework": _REWORK_TEXT},
                    ref="vd-fail",
                )
            return InvokeResult(kind=KIND_COMPLETION,
                                completion={"verdict": "Pass", "rework": None}, ref="vd")
        return super().invoke(request)


class _RunDirCleanup(unittest.TestCase):
    """RUNS_DIR 직속 run_dir 정리(실 RUNS_DIR 오염 방지 — 기존 트리 관례 동형)."""

    def setUp(self) -> None:
        self._run_dirs: list = []

    def tearDown(self) -> None:
        for rd in self._run_dirs:
            rd = Path(rd)
            if rd.exists() and rd.resolve().parent == op.RUNS_DIR.resolve():
                shutil.rmtree(rd, ignore_errors=True)

    def _track(self, run_dir) -> Path:
        run_dir = Path(run_dir)
        self._run_dirs.append(run_dir)
        return run_dir

    def _drive(self, base: Path, run_id: str, stub) -> tuple:
        """실 엔진 구동 1회 — (root, run_dir, stub, code, stdout, stderr)."""
        root = _make_project_root(base)
        run_dir, _cfg = op.prepare_run(root, phase_scope="Phase 1", run_id=run_id)
        run_dir = self._track(run_dir)
        stub._ws = root
        orch, _c = op.build(run_dir, stub)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = op.run_and_map(orch, stub, run_dir)
        return root, run_dir, stub, code, out.getvalue(), err.getvalue()


def _make_sweep_run(base: Path) -> tuple:
    """스윕 전용 실파일 픽스처 — run 데이터 3종 + 실제 워크스페이스 파일 트리.

    단위 2개: (a) 디렉터리 경계(`src`·재귀 대상·바이너리 1개 포함) (b) 단일 파일 경계 +
    미실재 경계 항목 1건. 전부 물리 파일이며 합성 문자열 스캔이 아니다.
    """
    run_dir = base / "run"
    (run_dir / "logs").mkdir(parents=True)
    ws = base / "ws"
    (ws / "src" / "deep").mkdir(parents=True)
    (ws / "src" / "a.py").write_text(
        "import os\nos.system('rm -rf /')  # BAD_API 오용\n", encoding="utf-8")
    (ws / "src" / "deep" / "b.py").write_text(
        "def f():\n    return 1\n# BAD_API 여기도 복제됨\n", encoding="utf-8")
    (ws / "src" / "blob.bin").write_bytes(b"\x00\x01BAD_API\x00")
    (ws / "notes.txt").write_text("깨끗한 파일\n", encoding="utf-8")

    graph = {
        "goal": "sweep fixture",
        "tasks": [
            {"id": "unit-a", "task": "t", "done": "d", "interfaceContract": {},
             "ownedBoundary": ["src"], "dependsOn": [], "delegation": {},
             "capability": "cap", "role": "Worker", "model": "m",
             "unitType": "implementation"},
            {"id": "unit-b", "task": "t", "done": "d", "interfaceContract": {},
             "ownedBoundary": ["notes.txt", "missing.txt"], "dependsOn": [],
             "delegation": {}, "capability": "cap", "role": "Worker", "model": "m",
             "unitType": "implementation"},
        ],
        "dependencies": [],
        "completion": "all-passed",
    }
    config = {"run_id": "sweep-fixture", "workspace_dir": str(ws),
              "retry_limit": 2, "policy": "auto_approve"}
    for name, data in (("config.json", config), ("graph.json", graph),
                       ("gate_policy.json", ctg.gate_policy())):
        with open(run_dir / name, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
    # 조립이 부재 시 생성하던 3종 원장 — 스윕은 읽기 전용이므로 픽스처가 미리 둔다
    # (실 run 은 엔진이 만든다). 이들이 없으면 sweep_units 는 precheck 로 exit 1 한다.
    for name in ("events.jsonl", "revisions.jsonl", "artifacts.jsonl"):
        (run_dir / name).write_text("", encoding="utf-8")
    return run_dir, ws


def _snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


# ==========================================================================
# done 1 — D-M1 seed 프롬프트 milestone 규칙
# ==========================================================================
class SeedPromptCrossUnitRuleTests(unittest.TestCase):
    def _prompt(self) -> str:
        return ctg._seed_prompt(
            Path("/x/.claude/project-contract/project-contract.v1.md"),
            Path("/x/docs/solution-design.md"),
            "Phase 1", "proj", 1,
        )

    def test_milestone_requires_cross_unit_contract_check(self) -> None:
        """milestone done AC 에 '단위 간 계약 정합 검사 최소 1건' 의무가 문면에 실재한다."""
        p = self._prompt()
        self.assertIn("단위 간 계약 정합 검사를 최소 1건 포함한다", p)
        self.assertIn("나열만으로는 **불충분**", p)
        self.assertIn("둘 이상의 단위를 상호 ", p)
        # 오프라인 안전형 예시 3종(produces↔consumes 상호 대조·모듈 경계 참조 무결·키 집합).
        self.assertIn("produces 경로와 후행 단위 consumes 경로를 **서로 대조**", p)
        self.assertIn("모듈 경계 참조 무결", p)
        self.assertIn("키 집합 일치", p)

    def test_milestone_task_has_cross_cutting_directive(self) -> None:
        """공통 결함 패턴의 횡단 관점 지시(복제 전제·동료 단위 대조·결과 보고)가 실재한다."""
        p = self._prompt()
        self.assertIn("횡단 관점", p)
        self.assertIn("여러 단위에 복제", p)
        self.assertIn("동료 단위에도 같은 기준으로 대조", p)
        self.assertIn("개별 단위 합격의 단순 합을 phase 완결로 단정하지 않는다", p)

    def test_existing_rules_preserved(self) -> None:
        """기존 문면 무삭제 — 직전 트랙의 timeout 선택 키 항·기존 done AC 규칙 보존."""
        p = self._prompt()
        self.assertIn("timeout = **선택 키**", p)
        self.assertIn("초 단위 양의 ", p)
        self.assertIn("미지정이면 전역 기본 예산이 적용된다", p)
        self.assertIn("**오프라인 안전 검사만** ", p)
        self.assertIn("금지: npm install", p)
        self.assertIn("**정확히 1개는 unitType = \"milestone\"**", p)
        self.assertIn("DAG 의 마지막 경계 노드", p)


# ==========================================================================
# done 2 — 런처 [REWORK-NOTE]
# ==========================================================================
class ReworkNoteTests(_RunDirCleanup):
    def test_rework_run_emits_note_with_unit_and_command(self) -> None:
        """CP2 Fail→rework 실제 발생 run 에서 단위 id·스윕 명령 힌트가 출력된다."""
        with tempfile.TemporaryDirectory() as td:
            _root, run_dir, stub, code, out, _err = self._drive(
                Path(td), "sweep-test-rework", _ReworkThenPassStub())
            self.assertGreaterEqual(stub.verdicts, 2, "CP2 재판정 실제 발생")
            self.assertIn("[REWORK-NOTE]", out)
            self.assertIn("impl-plan-phase-1", out)
            self.assertIn("sweep_units.py", out)
            self.assertIn(str(run_dir), out)
            self.assertIn("--pattern", out)
            # 부가 표면 — 기존 종료 표면·코드 불변(정지 게이트 도달).
            self.assertEqual(code, 2)
            self.assertIn("[INVOKES] total=", out)
            self.assertLess(out.index("[INVOKES] total="), out.index("[REWORK-NOTE]"))
            # 원장에 rework 이벤트가 실재한다(파생의 근거·합성 아님).
            events = [json.loads(l) for l in
                      (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
                      if l.strip()]
            rework = [e for e in events if (e.get("ref") or {}).get("kind") == "rework"]
            self.assertTrue(rework, "ref.kind=='rework' 이벤트 실재")
            self.assertEqual(rework[0]["cycle_id"], "impl-plan-phase-1")

    def test_clean_run_emits_no_note_line(self) -> None:
        """rework 0 run 에서는 [REWORK-NOTE] 계열 라인이 **한 줄도** 없다(종전 출력 보존)."""
        with tempfile.TemporaryDirectory() as td:
            _root, run_dir, _stub, code, out, err = self._drive(
                Path(td), "sweep-test-clean", _PassStub())
            self.assertEqual(code, 2)
            self.assertNotIn("[REWORK-NOTE]", out)
            self.assertNotIn("[REWORK-NOTE-SKIP]", out)
            self.assertNotIn("[REWORK-NOTE-SKIP]", err)
            events = [json.loads(l) for l in
                      (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
                      if l.strip()]
            self.assertFalse([e for e in events
                              if (e.get("ref") or {}).get("kind") == "rework"])

    def test_missing_ledger_skips_note_without_changing_flow(self) -> None:
        """events.jsonl 부재 — stdout·반환값 무변 + stderr 1행으로 생략 사실 고지."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "rd"
            run_dir.mkdir()
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                units = op.print_rework_note(run_dir)
            self.assertEqual(units, [])
            self.assertEqual(out.getvalue(), "", "stdout 무출력(종전 표면 보존)")
            self.assertIn("[REWORK-NOTE-SKIP]", err.getvalue())
            self.assertIn("생략", err.getvalue())

    def test_corrupt_ledger_skips_note_and_preserves_exit_code(self) -> None:
        """파손 events.jsonl — run_and_map 종료 코드·기존 라인 무변 + stderr 고지."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "rd"
            (run_dir / "logs").mkdir(parents=True)
            (run_dir / "events.jsonl").write_text("{ not json\n", encoding="utf-8")

            class _R:
                status = "completed"
                stop_reason = None
                stopped_tasks: list = []
                pending_gates: list = []
                epochs = 1
                graph_task_ids: list = []
                states: dict = {}
                completed = True

            class _O:
                def run(self):
                    return _R()

            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = op.run_and_map(_O(), None, run_dir)
            self.assertEqual(code, 0, "종료 코드 무변")
            self.assertIn("[COMPLETE] all units Passed.", out.getvalue())
            self.assertNotIn("[REWORK-NOTE]", out.getvalue())
            self.assertIn("[REWORK-NOTE-SKIP]", err.getvalue())

    def test_note_quotes_last_rework_verbatim_and_clips(self) -> None:
        """[재작업 2] `ref.rework` 원문 인용 — 마지막 지시·200자 초과 시 클립 표기."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            long_text = "가" * 250
            rows = [
                {"cycle_id": "u1", "ref": {"kind": "rework", "rework": "첫 지시(덮인다)"}},
                {"cycle_id": "u1", "ref": {"kind": "rework",
                                           "rework": "AC 가 산출을 판별하지 못한다"}},
                {"cycle_id": "u2", "ref": {"kind": "rework", "rework": long_text}},
            ]
            (run_dir / "events.jsonl").write_text(
                "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                op.print_rework_note(run_dir)
            text = out.getvalue()
            self.assertIn("· u1 ← AC 가 산출을 판별하지 못한다", text)
            self.assertNotIn("첫 지시(덮인다)", text, "마지막 지시만 인용")
            self.assertIn("· u2 ← " + "가" * op.REWORK_QUOTE_CLIP
                          + op.REWORK_QUOTE_CLIP_MARK, text)
            self.assertNotIn("가" * (op.REWORK_QUOTE_CLIP + 1), text)

    def test_note_omits_quote_line_when_rework_absent(self) -> None:
        """[재작업 2] `ref.rework` 부재/None 이면 인용 행 생략·note 본행은 유지(발명 0)."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            rows = [
                {"cycle_id": "u1", "ref": {"kind": "rework"}},           # 키 자체 부재
                {"cycle_id": "u2", "ref": {"kind": "rework", "rework": None}},
                {"cycle_id": "u3", "ref": {"kind": "rework", "rework": "   "}},  # 공백뿐
            ]
            (run_dir / "events.jsonl").write_text(
                "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                units = op.print_rework_note(run_dir)
            text = out.getvalue()
            self.assertEqual(units, ["u1", "u2", "u3"])
            self.assertIn("[REWORK-NOTE] CP2 재작업이 발생한 단위:", text)
            self.assertIn("sweep_units.py", text)
            self.assertNotIn("←", text, "인용 행 0")

    def test_note_quotes_non_string_rework_as_json(self) -> None:
        """비-문자열 지시는 `json.dumps` 직렬화로 인용한다(구조 보존·해석 0)."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "events.jsonl").write_text(
                json.dumps({"cycle_id": "u1",
                            "ref": {"kind": "rework",
                                    "rework": {"items": ["AC 보강", "픽스처 고정"]}}},
                           ensure_ascii=False) + "\n", encoding="utf-8")
            details = op.rework_details(run_dir)
            self.assertEqual(details,
                             [("u1", '{"items": ["AC 보강", "픽스처 고정"]}')])

    def test_rework_units_derivation_is_deduped_and_ordered(self) -> None:
        """단위 계약 — 중복 제거 + 원장 등장 순서. 비-dict ref·타 kind 는 무시."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            rows = [
                {"cycle_id": "u1", "ref": {"kind": "dispatch"}},
                {"cycle_id": "u2", "ref": {"kind": "rework"}},
                {"cycle_id": "u1", "ref": {"kind": "rework"}},
                {"cycle_id": "u2", "ref": {"kind": "rework"}},
                {"cycle_id": "u3", "ref": "문자열 ref"},
                {"cycle_id": "u4", "ref": None},
            ]
            (run_dir / "events.jsonl").write_text(
                "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                encoding="utf-8")
            self.assertEqual(op.rework_units(run_dir), ["u2", "u1"])


# ==========================================================================
# done 3 — sweep_units.py
# ==========================================================================
class SweepUnitsTests(unittest.TestCase):
    def test_hit_reports_unit_file_line_and_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir, _ws = _make_sweep_run(Path(td))
            out = io.StringIO()
            with redirect_stdout(out):
                rc = sw.main([str(run_dir), "--pattern", "BAD_API"])
            text = out.getvalue()
            self.assertEqual(rc, 2, text)
            self.assertIn("[UNIT] unit-a", text)
            self.assertIn("a.py:2 ::", text)
            self.assertIn("b.py:3 ::", text)          # 디렉터리 재귀(하위 deep/)
            self.assertIn("BAD_API 오용", text)        # 히트 문면 동봉
            self.assertIn("[UNIT] unit-b (state=", text)
            self.assertIn("total_hits=2", text)
            self.assertIn(sw.NEXT_LINE.split("]")[0] + "]", text)
            self.assertIn("supersede(원장 경유)", text)
            self.assertIn("원장 밖 직접 수정 금지", text)

    def test_no_hit_exits_0(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir, _ws = _make_sweep_run(Path(td))
            out = io.StringIO()
            with redirect_stdout(out):
                rc = sw.main([str(run_dir), "--pattern", "존재하지않는패턴XYZ"])
            self.assertEqual(rc, 0)
            self.assertIn("total_hits=0", out.getvalue())

    def test_error_paths_exit_1(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir, _ws = _make_sweep_run(Path(td))
            # (i) run_dir 부재
            err = io.StringIO()
            with redirect_stderr(err):
                rc = sw.main([str(Path(td) / "nope"), "--pattern", "x"])
            self.assertEqual(rc, 1)
            self.assertIn("[ERR] run_dir", err.getvalue())
            # (ii) 패턴 무지정 — 도구는 패턴을 발명하지 않는다
            err = io.StringIO()
            with redirect_stderr(err):
                rc = sw.main([str(run_dir)])
            self.assertEqual(rc, 1)
            self.assertIn("--pattern", err.getvalue())
            # (iii) 정규식 컴파일 실패
            err = io.StringIO()
            with redirect_stderr(err):
                rc = sw.main([str(run_dir), "--pattern", "([unclosed"])
            self.assertEqual(rc, 1)
            self.assertIn("정규식 컴파일 실패", err.getvalue())

    def test_incomplete_run_dir_exits_1_and_creates_nothing(self) -> None:
        """[재작업 1] 조립이 생성하던 파일이 부재하면 **만들지 않고** exit 1(쓰기 0 보장)."""
        for victim in ("events.jsonl", "revisions.jsonl", "artifacts.jsonl"):
            with tempfile.TemporaryDirectory() as td:
                run_dir, ws = _make_sweep_run(Path(td))
                (run_dir / victim).unlink()   # 3종 JSONL 중 victim 만 없는 상태.
                before_run, before_ws = _snapshot(run_dir), _snapshot(ws)
                err = io.StringIO()
                with redirect_stderr(err):
                    rc = sw.main([str(run_dir), "--pattern", "BAD_API"])
                self.assertEqual(rc, 1, victim)
                self.assertIn("읽기 전용 도구라 생성하지 않는다", err.getvalue())
                self.assertIn(victim, err.getvalue())
                # 물리 확인: 부재 파일이 **여전히 부재**하고 나머지도 무변.
                self.assertFalse((run_dir / victim).exists(), "%s 생성 0" % victim)
                self.assertEqual(_snapshot(run_dir), before_run)
                self.assertEqual(_snapshot(ws), before_ws)

    def test_absent_workspace_dir_exits_1_without_creating_it(self) -> None:
        """[재작업 1] workspace_dir 부재 → exit 1 + 디렉터리 미생성(makedirs 차단)."""
        with tempfile.TemporaryDirectory() as td:
            run_dir, ws = _make_sweep_run(Path(td))
            shutil.rmtree(ws)
            err = io.StringIO()
            with redirect_stderr(err):
                rc = sw.main([str(run_dir), "--pattern", "BAD_API"])
            self.assertEqual(rc, 1)
            self.assertIn("워크스페이스 디렉터리 부재", err.getvalue())
            self.assertFalse(ws.exists(), "workspace 디렉터리 생성 0")

    def test_precheck_passes_on_complete_run_dir(self) -> None:
        """단위 계약 — 완비 run_dir 은 부재 0을 반환하고, precheck 자체가 아무것도 만들지 않는다."""
        with tempfile.TemporaryDirectory() as td:
            run_dir, _ws = _make_sweep_run(Path(td))
            before = _snapshot(run_dir)
            self.assertEqual(sw.precheck(run_dir), [])
            self.assertEqual(_snapshot(run_dir), before)

    def test_directory_recursion_binary_skip_and_counts(self) -> None:
        """디렉터리 재귀·바이너리 스킵 **건수 보고**·미실재 경계 항목 보고(침묵 0)."""
        with tempfile.TemporaryDirectory() as td:
            run_dir, ws = _make_sweep_run(Path(td))
            result = sw.sweep(run_dir, [re.compile("BAD_API")])
            unit_a = [u for u in result["units"] if u["id"] == "unit-a"][0]
            unit_b = [u for u in result["units"] if u["id"] == "unit-b"][0]
            # 재귀: src/a.py + src/deep/b.py 스캔(blob.bin 은 바이너리로 제외).
            self.assertEqual(unit_a["files_scanned"], 2)
            self.assertEqual(len(result["skipped_binary"]), 1)
            self.assertIn("blob.bin", result["skipped_binary"][0])
            self.assertEqual(unit_b["missing"], ["missing.txt"])
            self.assertEqual(unit_b["files_scanned"], 1)
            # 렌더에 스킵 건수·미실재가 **항상** 표면화된다.
            text = sw.render(result, ["BAD_API"])
            self.assertIn("[SKIPPED] binary=1 unreadable=0", text)
            self.assertIn("미실재 경계 항목 1 건", text)
            # 바이너리 안에도 패턴 바이트가 있으나 히트로 세지 않는다(스킵의 실증).
            self.assertEqual(result["total_hits"], 2)
            # 워크스페이스 쓰기 0.
            self.assertTrue((ws / "src" / "blob.bin").exists())

    def test_workspace_and_ledger_are_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir, ws = _make_sweep_run(Path(td))
            ws_before, run_before = _snapshot(ws), _snapshot(run_dir)
            out = io.StringIO()
            with redirect_stdout(out):
                sw.main([str(run_dir), "--pattern", "BAD_API"])
            self.assertEqual(ws_before, _snapshot(ws), "워크스페이스 무변경(쓰기 0)")
            # [재작업 1] 사전 검사 도입 후에는 run_dir 도 **파일 목록·바이트 전부 동일**하다
            # (조립이 부재 JSONL 을 생성하던 경로가 애초에 열리지 않는다).
            self.assertEqual(run_before, _snapshot(run_dir), "run_dir 무변경(생성 0)")

    def test_json_output_is_structured_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir, _ws = _make_sweep_run(Path(td))
            outs = []
            for _ in range(2):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = sw.main([str(run_dir), "--pattern", "BAD_API", "--json"])
                outs.append(buf.getvalue())
            self.assertEqual(rc, 2)
            self.assertEqual(outs[0], outs[1], "동일 입력 → 동일 출력(결정적)")
            data = json.loads(outs[0])
            self.assertEqual(data["total_hits"], 2)
            self.assertEqual([u["id"] for u in data["units"]], ["unit-a", "unit-b"])

    def test_ignore_case_flag(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_dir, _ws = _make_sweep_run(Path(td))
            quiet = io.StringIO()
            with redirect_stdout(quiet):
                rc0 = sw.main([str(run_dir), "--pattern", "bad_api"])
            self.assertEqual(rc0, 0)
            out = io.StringIO()
            with redirect_stdout(out):
                rc = sw.main([str(run_dir), "--pattern", "bad_api", "--ignore-case"])
            self.assertEqual(rc, 2)


# ==========================================================================
# done 4 — 접합부 왕복(§5.7 형태·실물)
# ==========================================================================
class ReworkToSweepRoundtripTests(_RunDirCleanup):
    def test_engine_run_to_note_to_sweep_hit(self) -> None:
        """엔진 실구동(CP2 Fail→rework→재시도 Pass) → 실물 원장 판독 → 실 argv 스윕 히트."""
        with tempfile.TemporaryDirectory() as td:
            payload = json.dumps(
                {"tasks": [], "note": "os.system('rm -rf /')  # BAD_API"},
                ensure_ascii=False) + "\n"
            root, run_dir, stub, code, out, _err = self._drive(
                Path(td), "sweep-test-roundtrip",
                _ReworkThenPassStub(payload=payload))

            # (a) 엔진이 실제로 재작업을 돌았다(스텁 판정 2회·원장 rework 이벤트 1건).
            self.assertEqual(code, 2)
            self.assertGreaterEqual(stub.verdicts, 2)
            events = [json.loads(l) for l in
                      (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
                      if l.strip()]
            rework = [e for e in events if (e.get("ref") or {}).get("kind") == "rework"]
            self.assertEqual(len(rework), 1)

            # (b) 런처 경로의 note 파생이 **그 실물 events.jsonl** 을 읽어 단위를 열거했다.
            self.assertIn("[REWORK-NOTE]", out)
            derived = op.rework_units(run_dir)
            self.assertEqual(derived, ["impl-plan-phase-1"])
            self.assertIn(derived[0], out)
            # 실 엔진이 원장에 남긴 재작업 지시가 note 에 **원문 그대로** 인용됐다.
            self.assertEqual(op.rework_details(run_dir),
                             [("impl-plan-phase-1", _REWORK_TEXT)])
            self.assertIn("· impl-plan-phase-1 ← %s" % _REWORK_TEXT, out)

            # (c) 같은 run_dir 에 sweep_units 를 **실 argv** 로 구동 → 워크스페이스 실파일 히트.
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = sw.main([str(run_dir), "--pattern", r"os\.system\("])
            text = buf.getvalue()
            self.assertEqual(rc, 2, text)
            self.assertIn("[UNIT] impl-plan-phase-1", text)
            self.assertIn("%s:1 ::" % ctg.IMPL_PLAN_FILE, text)
            self.assertIn("state=Passed", text)
            # 스윕이 본 파일은 소비 프로젝트 워크스페이스의 실물이다.
            self.assertTrue((root / ctg.IMPL_PLAN_FILE).exists())


if __name__ == "__main__":
    unittest.main()
