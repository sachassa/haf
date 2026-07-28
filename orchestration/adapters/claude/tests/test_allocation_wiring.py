"""allocation_file 배선 3지점 + 경량 레인 CP2 차등 — 오프라인 검증(실 LLM 미발화).

절차 비례화 트랙 W3-a 위임 done 1~7 을 실제 코드·실제 원장으로 뒷받침한다.

  - done 1: config.json 에 allocation_file 키가 생산되고, **미지정 시 키 부재 → allocation
            ==None** 으로 현행 거동·직렬화가 byte 동일하게 보존된다(무회귀 대조).
  - done 2: allocation_file 지정 시 저위험 capability class 의 **CP2 모델 슬롯이 저티어**로
            해소된다(엔진 실주행 원장 + Verifier 디스패치 실물 관측).
  - done 3: 고위험·미매칭 capability 의 CP2 슬롯이 안전측(sonnet)으로 귀결한다(음성 대조).
  - done 4: CP2 디스패치 자체가 어떤 정책 값에서도 우회되지 않는다(host.py `_dispatch_cp2`
            호출의 **무분기** AST 근거 + 저위험 경로 원장의 `cp2-pass` ref 실물).
  - done 5: gates.py · host.py 게이트 하한 상수의 diff hunk 0(git diff + 축자 상수 대조).
  - done 6: 스크립트 AC 는 브리프 층(done 축) 소관이며 CP2 실행 여부를 바꾸지 않는다(문면).
  - done 7: allocation_file 상대경로 해석 기준(= orchestration-data/e2e/) 실측 + 문서 명시.

중립 코드(orchestration/framework/**·uahf/framework/loop/**)는 무수정 import·판독만 한다.
"""

from __future__ import annotations

import ast
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# --- 경로 배선: 런처 모듈 디렉터리(test_orchestrate_project 선례 동형) ------------
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]              # orchestration/adapters/claude
_REPO = _TEST_FILE.parents[4]                    # 리포 루트
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import contract_to_graph as c2g                  # noqa: E402
import orchestrate_project as op                 # noqa: E402

op.wire_paths()
from stephost_bridge import (                    # noqa: E402  (무수정 import)
    InvokeResult,
    KIND_COMPLETION,
    ROLE_VERIFIER,
)

_E2E = _REPO / "uahf" / "framework" / "adapters" / "claude" / "orchestration-data" / "e2e"
_POLICY_DIR = _E2E / "policy"
_LIGHT_REL = "policy/allocation-lightweight.json"
_LIGHT_ABS = _POLICY_DIR / "allocation-lightweight.json"
_POLICY_README = _POLICY_DIR / "README.md"

_GATES_PY = _REPO / "orchestration" / "framework" / "orchestrator" / "gates.py"
_HOST_PY = _REPO / "uahf" / "framework" / "loop" / "step-host" / "host.py"

# 저위험/고위험 capability 실값(정책 데이터 소관 어휘 — 코드에 넣지 않는다).
_CAP_LOW = "cap-impl-mechanical"
_CAP_HIGH = "cap-impl-plan"
_CAP_UNKNOWN = "cap-impl-core"                   # 레지스트리 미등재(seed 프롬프트 예시 슬러그)

# 기대 슬롯 실값 — Adapter 격리 경계 데이터이므로 테스트가 실값을 알아도 된다(PO-INV 8 무관).
_TIER_LOW = "haiku"
_TIER_SAFE = "sonnet"


# --------------------------------------------------------------------------
# 픽스처
# --------------------------------------------------------------------------
def _make_project_root(base: Path) -> Path:
    root = base / "consumer-project"
    cd = root / ".claude" / "project-contract"
    cd.mkdir(parents=True)
    (cd / "project-contract.v1.md").write_text("# dummy contract v1\n", encoding="utf-8")
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "solution-design.md").write_text("# sd\n", encoding="utf-8")
    return root


class _RecordingStubInvoker:
    """중립 stub — Worker/Verifier 를 즉시 성공시키고 **역할별 model 슬롯을 기록**한다.

    실 claude CLI 를 발화하지 않는다. CP2 모델 슬롯 결정은 Host 가 하므로(host.py:326-332)
    이 stub 이 관측하는 `request.model` 은 엔진·Host 가 실제로 정한 값이다(관측만·개입 0).
    """

    def __init__(self) -> None:
        self.calls: list = []

    def invoke(self, request):
        self.calls.append({
            "role": request.role,
            "capability": request.capability,
            "model": request.model,
        })
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

    def models_for(self, role: str) -> list:
        return [c["model"] for c in self.calls if c["role"] == role]


def _load_allocation(ref):
    """소비 슬롯(resolve_allocation)을 그대로 써서 정책을 로드한다(런처가 쓰는 경로 동일).

    run_dir 은 임의 임시 경로를 준다 — 상대경로 기준이 run_dir 이 **아님**을 동시에 실측한다.
    """
    if str(_E2E) not in sys.path:
        sys.path.insert(0, str(_E2E))
    from _orch_common import resolve_allocation  # noqa: E402  (무수정 재사용)
    with tempfile.TemporaryDirectory() as td:
        return resolve_allocation(Path(td), {}, ref)


# ==========================================================================
# done 1 — 키 생산 + 미지정 시 byte 동일 무회귀
# ==========================================================================
class ConfigKeyProductionTests(unittest.TestCase):
    """`build_config` 가 allocation_file 을 **선택적으로** 생산한다."""

    _BASE_KEYS = {
        "run_id", "policy", "retry_limit", "timeout",
        "allowed_tools", "output_format", "workspace_dir",
    }

    def _cfg(self, **kw):
        return c2g.build_config(
            "orch-x-phase-1", "/ws", allowed_tools=["Read"], timeout=900, **kw
        )

    def test_key_absent_when_unspecified(self) -> None:
        cfg = self._cfg()
        self.assertNotIn("allocation_file", cfg)
        self.assertEqual(set(cfg.keys()), self._BASE_KEYS, "종전 7키 정확 보존")

    def test_key_absent_when_empty_string(self) -> None:
        """빈 문자열은 미지정과 동일 취급(falsy) — 빈 값 키로 소비 슬롯을 혼란시키지 않는다."""
        self.assertNotIn("allocation_file", self._cfg(allocation_file=""))
        self.assertNotIn("allocation_file", self._cfg(allocation_file=None))

    def test_key_produced_when_specified(self) -> None:
        cfg = self._cfg(allocation_file=_LIGHT_REL)
        self.assertEqual(cfg["allocation_file"], _LIGHT_REL)
        self.assertEqual(set(cfg.keys()), self._BASE_KEYS | {"allocation_file"})

    def test_path_object_is_stringified(self) -> None:
        cfg = self._cfg(allocation_file=_LIGHT_ABS)
        self.assertIsInstance(cfg["allocation_file"], str)

    def test_compile_forwards_allocation_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            plain = c2g.compile(root, mode="incremental", phase_scope="Phase 1")
            wired = c2g.compile(
                root, mode="incremental", phase_scope="Phase 1",
                allocation_file=_LIGHT_REL,
            )
        self.assertNotIn("allocation_file", plain["config"])
        self.assertEqual(wired["config"]["allocation_file"], _LIGHT_REL)
        # graph·gate_policy 는 allocation 과 직교(무영향).
        self.assertEqual(plain["graph"], wired["graph"])
        self.assertEqual(plain["gate_policy"], wired["gate_policy"])


class ConfigByteRegressionTests(unittest.TestCase):
    """미지정 경로의 config.json 직렬화가 **개정 전 byte 와 동일**하다(무회귀 잠금).

    개정 전 실측 본문(정규화 = workspace_dir 절대경로만 <ROOT> 치환)을 리터럴로 잠근다.
    실측 근거 로그의 NORMALIZED_SHA256 =
    4e7e7875c36fa6c1b2d47015f024c5d76805dbae5dc8e50529c79ff59b31bfdc
    """

    _BEFORE = """{
  "allowed_tools": [
    "Write",
    "Read",
    "Edit",
    "Glob",
    "Grep",
    "Bash(node:*)",
    "Bash(python:*)"
  ],
  "output_format": "json",
  "policy": "auto_approve",
  "retry_limit": 2,
  "run_id": "orch-baseline-fixed",
  "timeout": 2400,
  "workspace_dir": "<ROOT>"
}"""

    def _materialized(self, base: Path, **kw):
        root = _make_project_root(base)
        runs = base / "runs"
        runs.mkdir()
        orig = op.RUNS_DIR
        op.RUNS_DIR = runs
        try:
            run_dir, cfg = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-baseline-fixed", **kw
            )
            raw = (run_dir / "config.json").read_text(encoding="utf-8")
        finally:
            op.RUNS_DIR = orig
        return raw.replace(json.dumps(str(root))[1:-1], "<ROOT>"), cfg

    def test_unspecified_config_json_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            text, cfg = self._materialized(Path(td))
        self.assertNotIn("allocation_file", cfg)
        self.assertEqual(text, self._BEFORE, "미지정 경로 config.json byte 동일(무회귀)")

    def test_specified_config_json_adds_exactly_one_line(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            text, cfg = self._materialized(Path(td), allocation_file=_LIGHT_REL)
        self.assertEqual(cfg["allocation_file"], _LIGHT_REL)
        added = [ln for ln in text.splitlines() if ln not in self._BEFORE.splitlines()]
        self.assertEqual(len(added), 1, "추가는 allocation_file 1행뿐: %r" % added)
        self.assertIn("allocation_file", added[0])

    def test_resolve_allocation_none_without_key(self) -> None:
        """소비 슬롯이 키 부재를 None 으로 귀결한다(현행 거동 = allocation 미배선)."""
        self.assertIsNone(_load_allocation(None))


# ==========================================================================
# done 2 · done 3 — 저위험 CP2 저티어 해소 / 고위험·미매칭 안전측 귀결
# ==========================================================================
class LightweightPolicyDataTests(unittest.TestCase):
    """경량 프로파일 데이터의 순수 판정(스키마 정합 + 슬롯 해소)."""

    def setUp(self) -> None:
        self.alloc = _load_allocation(_LIGHT_REL)
        self.assertIsNotNone(self.alloc, "경량 프로파일이 소비 슬롯으로 로드된다")

    def test_lowrisk_cp2_slot_is_low_tier(self) -> None:
        """[done 2 · 데이터 층] 저위험 capability → CP2 슬롯 저티어."""
        self.assertEqual(self.alloc.cp2_model_for(_CAP_LOW), _TIER_LOW)

    def test_highrisk_cp2_slot_is_safe_tier(self) -> None:
        """[done 3] 고위험 등재 capability → 전역 cp2ModelSlot(안전측) 폴백."""
        self.assertEqual(self.alloc.cp2_model_for(_CAP_HIGH), _TIER_SAFE)

    def test_unmatched_capability_cp2_falls_back_safe(self) -> None:
        """[done 3] 미등재 capability → `*` spec → cp2ModelSlots 미매칭 → 안전측."""
        self.assertEqual(self.alloc.cp2_model_for(_CAP_UNKNOWN), _TIER_SAFE)
        self.assertEqual(self.alloc.cp2_model_for(None), _TIER_SAFE)

    def test_unmatched_worker_slot_is_default_slot(self) -> None:
        """[done 3] Worker 슬롯의 미매칭 귀결은 defaultSlot(= 안전측 sonnet)이다.

        주의(층 구분): CP2 슬롯의 폴백은 `cp2ModelSlot`, Worker 슬롯의 미매칭 폴백은
        `defaultSlot` 이다 — 이 프로파일은 두 값을 모두 sonnet(안전측)으로 두어 관측값이
        같지만 **기제가 다르다**. 두 기제를 각각 친다.
        """
        raw = json.loads(_LIGHT_ABS.read_text(encoding="utf-8"))
        self.assertEqual(raw["modelSelection"]["defaultSlot"], _TIER_SAFE)
        self.assertEqual(raw["modelSelection"]["cp2ModelSlot"], _TIER_SAFE)
        self.assertEqual(self.alloc.model_for(_CAP_UNKNOWN), _TIER_SAFE)
        self.assertEqual(self.alloc.model_for(_CAP_LOW), _TIER_LOW)

    def test_no_uniform_low_tier(self) -> None:
        """균일 저티어 고정 금지 — 저위험만 저티어다(README 규율의 데이터 대조)."""
        raw = json.loads(_LIGHT_ABS.read_text(encoding="utf-8"))
        cp2_slots = raw["modelSelection"]["cp2ModelSlots"]
        self.assertEqual(list(cp2_slots), ["low-risk-semantic"])
        self.assertEqual(cp2_slots["low-risk-semantic"], _TIER_LOW)

    def test_model_selection_keys_are_schema_registered(self) -> None:
        """스키마 additionalProperties:false 를 열지 않고 **등재된 키만** 쓴다."""
        schema = json.loads(
            (_REPO / "orchestration" / "framework" / "orchestrator"
             / "model_selection_schema.json").read_text(encoding="utf-8")
        )
        self.assertFalse(schema["additionalProperties"], "닫힌 스키마 유지 전제")
        allowed = set(schema["properties"])
        raw = json.loads(_LIGHT_ABS.read_text(encoding="utf-8"))
        self.assertTrue(set(raw["modelSelection"]).issubset(allowed),
                        "미등재 키 사용 0: %s" % (set(raw["modelSelection"]) - allowed))

    def test_no_cp2_disabling_key(self) -> None:
        """[done 4 · 데이터 층] CP2 를 끄는 키가 데이터에 **존재하지 않는다**."""
        raw = json.loads(_LIGHT_ABS.read_text(encoding="utf-8"))
        cp2_keys = [k for k in raw["modelSelection"] if "cp2" in k.lower()]
        self.assertEqual(sorted(cp2_keys), ["cp2ModelSlot", "cp2ModelSlots"],
                         "CP2 관련 키는 모델 슬롯 2종뿐(실행 여부 키 0)")


class LiveDispatchLedgerTests(unittest.TestCase):
    """[done 2 · done 4 — 원장 실물] 엔진을 실제로 구동해 원장·디스패치를 관측한다.

    실 claude CLI 는 발화하지 않는다(stub invoker). 그러나 **CP2 디스패치 여부·CP2 모델
    슬롯 결정·원장 append 는 전부 엔진·Step Host 소관**이므로 이 관측은 배선의 실물 근거다.
    """

    def _run(self, base: Path, capability: str, allocation_file=None):
        root = _make_project_root(base)
        runs = base / "runs"
        runs.mkdir()
        orig = op.RUNS_DIR
        op.RUNS_DIR = runs
        try:
            run_dir, _cfg = op.prepare_run(
                root, phase_scope="Phase 1", run_id="orch-alloc-" + capability,
                allocation_file=allocation_file,
            )
            # seed 노드의 capability·model 을 대상 시나리오로 바꾼다(정책 매칭 표면 조작).
            # model 슬롯은 비운다 — 명시 model 이 있으면 그 값이 우선하므로(README) 정책
            # 차등을 관측할 수 없다.
            graph = json.loads((run_dir / "graph.json").read_text(encoding="utf-8"))
            for task in graph["tasks"]:
                task["capability"] = capability
                task["model"] = None
            (run_dir / "graph.json").write_text(
                json.dumps(graph, ensure_ascii=False, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            invoker = _RecordingStubInvoker()
            orch, _c = op.build(run_dir, invoker)
            with redirect_stdout(io.StringIO()):
                orch.run()
            events = [
                json.loads(ln)
                for ln in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
                if ln.strip()
            ]
            return invoker, events
        finally:
            op.RUNS_DIR = orig

    @staticmethod
    def _cp2_pass_refs(events: list) -> list:
        return [
            e for e in events
            if isinstance(e.get("ref"), dict) and e["ref"].get("kind") == "cp2-pass"
        ]

    def test_lowrisk_cp2_dispatched_at_low_tier(self) -> None:
        """[done 2] 저위험 단위의 **CP2 디스패치가 저티어 슬롯**으로 일어난다."""
        with tempfile.TemporaryDirectory() as td:
            invoker, events = self._run(Path(td), _CAP_LOW, allocation_file=_LIGHT_REL)
        cp2_models = invoker.models_for(ROLE_VERIFIER)
        self.assertTrue(cp2_models, "CP2 디스패치가 실제로 일어났다")
        self.assertEqual(set(cp2_models), {_TIER_LOW}, "CP2 슬롯 = 저티어: %r" % cp2_models)
        # [done 4] 저위험 경로에서도 cp2-pass ref 가 원장에 append 된다.
        self.assertTrue(self._cp2_pass_refs(events), "cp2-pass ref 원장 실물 존재")

    def test_highrisk_cp2_dispatched_at_safe_tier(self) -> None:
        """[done 3 · 음성 대조] 미등재 capability 는 안전측 슬롯으로 CP2 를 받는다."""
        with tempfile.TemporaryDirectory() as td:
            invoker, events = self._run(Path(td), _CAP_UNKNOWN, allocation_file=_LIGHT_REL)
        self.assertEqual(set(invoker.models_for(ROLE_VERIFIER)), {_TIER_SAFE})
        self.assertTrue(self._cp2_pass_refs(events))

    def test_cp2_slot_comes_from_cp2_slots_not_step_inheritance(self) -> None:
        """[done 2 · 기제 분간] CP2 슬롯이 **cp2ModelSlots** 에서 온다(step 슬롯 상속 아님).

        경량 프로파일은 저위험의 Worker 슬롯과 CP2 슬롯이 **둘 다 haiku** 라서, 관측된
        CP2=haiku 만으로는 (a) cp2ModelSlots 오버라이드 (b) 대상 step 슬롯 상속을 분간할 수
        없다. 두 값을 **일부러 갈라놓은** 픽스처로 기제를 확정한다 — Worker=sonnet 인데
        CP2=haiku 면 상속이 아니라 오버라이드가 작동한 것이다.
        """
        raw = json.loads(_LIGHT_ABS.read_text(encoding="utf-8"))
        raw["modelSelection"]["slots"]["low-risk-semantic"] = _TIER_SAFE  # Worker 만 상위 티어
        with tempfile.TemporaryDirectory() as td:
            fixture = Path(td) / "allocation-split.json"
            fixture.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
            invoker, events = self._run(
                Path(td) / "run", _CAP_LOW, allocation_file=str(fixture),
            )
        worker_models = [c["model"] for c in invoker.calls if c["role"] != ROLE_VERIFIER]
        self.assertEqual(set(worker_models), {_TIER_SAFE}, "대상 step 슬롯 = sonnet")
        self.assertEqual(set(invoker.models_for(ROLE_VERIFIER)), {_TIER_LOW},
                         "CP2 슬롯 = haiku → cp2ModelSlots 오버라이드가 기제다")
        self.assertTrue(self._cp2_pass_refs(events))

    def test_build_explicit_arg_wires_allocation_without_config_key(self) -> None:
        """[output ① 3지점 중 build 전달] `build(run_dir, invoker, path)` 명시 인자 경로.

        config 에 allocation_file 키가 **없는** run_dir 에 명시 인자만으로 정책을 배선한다
        (`resolve_allocation` 우선순위 = 명시 인자 > config > None). `--resume` 처럼 config
        재기록이 없는 경로에서 플래그가 조용히 무시되지 않는 근거다.
        """
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = _make_project_root(base)
            runs = base / "runs"
            runs.mkdir()
            orig = op.RUNS_DIR
            op.RUNS_DIR = runs
            try:
                run_dir, cfg = op.prepare_run(
                    root, phase_scope="Phase 1", run_id="orch-explicit-arg",
                )
                self.assertNotIn("allocation_file", cfg, "config 경유 배선이 없는 상태")
                plain, _c = op.build(run_dir, _RecordingStubInvoker())
                self.assertIsNone(plain.allocation, "명시 인자 없으면 미배선(현행 거동)")
                wired, _c2 = op.build(run_dir, _RecordingStubInvoker(), _LIGHT_REL)
            finally:
                op.RUNS_DIR = orig
        self.assertIsNotNone(wired.allocation, "명시 인자로 배선된다")
        self.assertEqual(wired.allocation.cp2_model_for(_CAP_LOW), _TIER_LOW)

    def test_cp2_dispatched_even_without_allocation(self) -> None:
        """[done 4] allocation 미배선(현행 거동)에서도 CP2 는 그대로 디스패치된다."""
        with tempfile.TemporaryDirectory() as td:
            invoker, events = self._run(Path(td), _CAP_LOW, allocation_file=None)
        self.assertTrue(invoker.models_for(ROLE_VERIFIER), "정책 0 에서도 CP2 존재")
        self.assertTrue(self._cp2_pass_refs(events))


# ==========================================================================
# done 4 — CP2 우회 불가(코드 하한 근거)
# ==========================================================================
class Cp2NoBypassSourceTests(unittest.TestCase):
    """host.py 의 `_dispatch_cp2` 호출이 **어떤 조건 아래에도 없다**(AST 근거)."""

    def test_dispatch_cp2_call_is_unconditional(self) -> None:
        tree = ast.parse(_HOST_PY.read_text(encoding="utf-8"))
        parents: dict = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node

        call_sites = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "_dispatch_cp2"
        ]
        self.assertEqual(len(call_sites), 1, "호출 지점 정확히 1(무분기 판정 대상)")

        # 호출 지점에서 함수 정의까지 거슬러 올라가며 조건·예외 분기 노드를 만나면 실패.
        branching = (ast.If, ast.IfExp, ast.While, ast.Try, ast.ExceptHandler,
                     ast.With, ast.BoolOp)
        node = call_sites[0]
        chain: list = []
        while node in parents:
            node = parents[node]
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                break
            chain.append(type(node).__name__)
            self.assertNotIsInstance(
                node, branching,
                "CP2 디스패치가 분기 아래 있다(SH-INV-4 위반 신호): %s" % chain,
            )
        self.assertIsInstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))

    def test_no_policy_or_gate_symbol_guards_cp2(self) -> None:
        """정책·게이트·allocation 어휘가 CP2 디스패치 문장 자체에 섞여 있지 않다."""
        lines = _HOST_PY.read_text(encoding="utf-8").splitlines()
        stmt = [ln for ln in lines if "self._dispatch_cp2(" in ln]
        self.assertEqual(len(stmt), 1)
        for token in ("if ", "policy", "gate", "allocation", "skip"):
            self.assertNotIn(token, stmt[0], token)


# ==========================================================================
# done 5 — 게이트 하한 상수 무촉
# ==========================================================================
class GateFloorUntouchedTests(unittest.TestCase):
    """게이트 하한 상수·합성식이 축자 보존된다(커밋 상태와 무관한 영구 잠금).

    종전에는 `git diff HEAD` 로 gates.py·host.py 의 미커밋 변경이 0 인지도 함께 단언했다
    (test_git_diff_hunk_zero). 그 가드는 **워킹트리 상태에 의존**해서, 자기 트랙의 무촉을
    증명하는 소임이 끝난 뒤에도 남아 이후 gates.py 를 정당하게 고치는 모든 트랙에서 가짜
    실패를 냈다(K-1 실측 — 하한 신설 작업이 커밋 전에 이 단언 하나로 스위트를 깼다).
    제거 근거: 그 가드가 지키려던 실질(하한 상수·effective_gate 합성식 보존)은 아래 축자
    대조가 커밋 여부와 무관하게 소유하고, host.py 쪽 실질은 같은 파일 위쪽의 SH-INV-4
    구조 검사(AST 파싱·CP2 디스패치 위치·심볼 혼입 금지)가 소유한다.
    """

    def test_floor_constants_verbatim(self) -> None:
        """git 상태와 무관한 축자 대조(커밋 후에도 유효한 잠금)."""
        text = _GATES_PY.read_text(encoding="utf-8")
        for token in (
            "_FLOOR_USER_DECISION_CLASSES",
            "_FLOOR_ESCALATION_CONDITIONS",
            'DEFAULT_USER_ACTOR_CLASS = "human"',
            'DEFAULT_GATE_RAISER = "Advisor"',
            "return max_gate(floor(target_descriptor), policy.evaluate(target_descriptor))",
        ):
            self.assertIn(token, text, token)
        # CP2 는 floor 테이블에 등재되지 않는다(설계 의도 — 주석 문면 존치 확인).
        self.assertIn("CP2 는 floor 테이블에 없다", text)


# ==========================================================================
# done 6 · done 7 — 문면 명시(스크립트 AC 층 · 상대경로 기준)
# ==========================================================================
class RelativePathBaseTests(unittest.TestCase):
    """[done 7] 상대경로 해석 기준 = orchestration-data/e2e/ 실측 + 문서 명시."""

    def test_relative_ref_resolves_against_e2e_not_run_dir(self) -> None:
        alloc = _load_allocation(_LIGHT_REL)   # run_dir = 임의 임시 경로(무관함을 실측)
        self.assertIsNotNone(alloc, "run_dir 과 무관하게 e2e 기준으로 해석된다")
        self.assertEqual(alloc.cp2_model_for(_CAP_LOW), _TIER_LOW)

    def test_absolute_ref_also_resolves(self) -> None:
        alloc = _load_allocation(str(_LIGHT_ABS))
        self.assertEqual(alloc.cp2_model_for(_CAP_LOW), _TIER_LOW)

    def test_relative_ref_is_not_cwd_relative(self) -> None:
        """cwd 를 리포 루트로 두어도 `policy/...` 는 cwd 기준으로 풀리지 않는다."""
        self.assertFalse((_REPO / _LIGHT_REL).exists(),
                         "cwd 기준 경로는 실재하지 않는다(기준이 e2e 임을 반증적으로 실측)")

    @staticmethod
    def _flat(path: Path) -> str:
        """마크다운 줄바꿈·강조 기호를 접어 문면 대조를 줄나눔에 취약하지 않게 만든다."""
        raw = path.read_text(encoding="utf-8").replace("*", "").replace("`", "")
        return " ".join(raw.split())

    def test_readme_documents_base_and_layers(self) -> None:
        flat = self._flat(_POLICY_README)
        # [done 7] 상대경로 해석 기준 명시 + run_dir 기준 아님 명시.
        self.assertIn("상대경로 해석 기준 = orchestration-data/e2e/", flat)
        self.assertIn("run_dir 기준이 아니다", flat)
        self.assertIn("우선순위 = 명시 인자 > config.allocation_file > None", flat)
        # [done 6] 판정 근거(스크립트 AC)는 브리프 층(done 축) 소관이며 실행 여부 무변 문면.
        self.assertIn("위임 브리프의 done 축 소관", flat)
        self.assertIn("판정 주체·실행 여부를 바꾸지 않는다", flat)
        # SH-INV-4·데이터 파일명 존치.
        self.assertIn("SH-INV-4", flat)
        self.assertIn("allocation-lightweight.json", flat)
        self.assertIn("CP2 를 끄는 키는 존재하지 않는다", flat)

    def test_command_doc_teaches_flag_and_base(self) -> None:
        doc = (_REPO / ".claude" / "commands" / "uaf-implement.md").read_text(encoding="utf-8")
        self.assertIn("--allocation-file", doc)
        self.assertIn("orchestration-data/e2e/", doc)
        self.assertIn("SH-INV-4", doc)

    def test_cli_accepts_allocation_file_flag(self) -> None:
        """[접합부 왕복] 문서가 가르치는 플래그를 런처 파서가 실제로 받는다."""
        with tempfile.TemporaryDirectory() as td:
            root = _make_project_root(Path(td))
            runs = Path(td) / "runs"
            runs.mkdir()
            orig = op.RUNS_DIR
            op.RUNS_DIR = runs
            try:
                err = io.StringIO()
                import contextlib
                with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                    rc = op.main([
                        str(root), "--resume", "--run-id", "orch-nope",
                        "--allocation-file", _LIGHT_REL,
                    ])
            finally:
                op.RUNS_DIR = orig
        self.assertEqual(rc, 1, "파싱 성공(SystemExit 없음) 후 run_dir 부재로 1")


if __name__ == "__main__":
    unittest.main()
