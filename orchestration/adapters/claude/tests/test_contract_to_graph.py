"""contract_to_graph (F4) 단위 테스트 — 실제 코드 스키마로 정합 검증(stdlib unittest).

이 테스트는 위임 done 1~7 을 실제 코드로 뒷받침한다:
  - resolve_contract 버전 최대 선택(v2·v10 수치식·done 1)
  - seed 노드가 **실제** step.py Step.from_dict + missing_fields 를 누락 0 통과(done 2)
  - gate_policy 가 **실제** gates.py GatePolicy.from_dict 로 로드·3 엔트리(done 3)
  - compile 3키 dict·디스크 미기록(tmp 격리·done 4)
  - seed·프롬프트 done AC 오프라인 안전(tsc/npm install/npm run build 부재·done 5)

step.py 는 uahf/framework/loop/step-host/, gates.py 는 orchestration/framework/orchestrator/
에서 **무수정 import** 만 한다(수정 0·PO-INV 8·done 7).
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

# --- 경로 배선 ------------------------------------------------------------
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]          # orchestration/adapters/claude
_REPO_ROOT = _TEST_FILE.parents[4]           # repo root
_GATES_DIR = _REPO_ROOT / "orchestration" / "framework" / "orchestrator"
_STEP_DIR = _REPO_ROOT / "uahf" / "framework" / "loop" / "step-host"

for _p in (str(_MODULE_DIR), str(_GATES_DIR), str(_STEP_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import contract_to_graph as c2g  # noqa: E402
from gates import GatePolicy  # noqa: E402  (무수정 import — orchestration/framework)
from step import Step  # noqa: E402  (무수정 import — uahf/framework/loop/step-host)

_TMS_ROOT = _REPO_ROOT / "tms-system"


class ResolveContractTests(unittest.TestCase):
    def test_tms_real_path_selects_v2(self) -> None:
        """done 1 — 실 tms-system 경로에서 v2 를 고른다(v1 아님)."""
        p = c2g.resolve_contract(_TMS_ROOT)
        self.assertTrue(p.is_absolute())
        self.assertEqual(p.name, "project-contract.v2.md")

    def test_numeric_max_not_lexical(self) -> None:
        """v2·v10 픽스처에서 v10 을 고른다(수치식 — 사전식이면 v2 오선택)."""
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            cd = Path(td) / ".claude" / "project-contract"
            cd.mkdir(parents=True)
            for v in ("1", "2", "10"):
                (cd / ("project-contract.v" + v + ".md")).write_text("x", encoding="utf-8")
            p = c2g.resolve_contract(Path(td))
            self.assertEqual(p.name, "project-contract.v10.md")

    def test_missing_raises(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                c2g.resolve_contract(Path(td))


class SeedGraphStepSchemaTests(unittest.TestCase):
    """done 2 — seed 단일 task 가 실제 Step 검증을 누락 0 통과."""

    def _seed_task(self) -> dict:
        contract = c2g.resolve_contract(_TMS_ROOT)
        graph = c2g.build_seed_graph(
            contract, _TMS_ROOT, mode="greenfield", phase_scope="phase1"
        )
        self.assertEqual(len(graph["tasks"]), 1)
        return graph["tasks"][0]

    def test_step_from_dict_missing_fields_zero(self) -> None:
        task = self._seed_task()
        step = Step.from_dict(task)          # id 부재 시 예외 — 여기서 통과해야 함.
        self.assertEqual(step.missing_fields(), [])
        self.assertTrue(step.is_ready_to_dispatch())

    def test_seed_node_shape(self) -> None:
        task = self._seed_task()
        self.assertEqual(task["id"], "impl-plan-phase1")
        self.assertEqual(task["unitType"], "proposal")
        self.assertEqual(task["role"], "Planner")
        self.assertEqual(task["capability"], "cap-impl-plan")
        self.assertEqual(task["dependsOn"], [])
        self.assertEqual(task["ownedBoundary"], ["impl-plan.json"])
        self.assertEqual(task["interfaceContract"]["produces"], ["impl-plan.json"])
        # consumes = 절대 Contract 경로(단일).
        consumes = task["interfaceContract"]["consumes"]
        self.assertEqual(len(consumes), 1)
        self.assertTrue(Path(consumes[0]).is_absolute())
        self.assertEqual(Path(consumes[0]).name, "project-contract.v2.md")
        # delegation 8필드 존재.
        for k in ("from", "to", "task", "input", "output", "done", "context", "constraints"):
            self.assertIn(k, task["delegation"])

    def test_graph_keys(self) -> None:
        contract = c2g.resolve_contract(_TMS_ROOT)
        graph = c2g.build_seed_graph(
            contract, _TMS_ROOT, mode="greenfield", phase_scope="phase1"
        )
        self.assertEqual(set(graph.keys()), {"goal", "tasks", "dependencies", "completion"})
        self.assertEqual(graph["dependencies"], [])


class GatePolicyTests(unittest.TestCase):
    """done 3 — gate_policy 출력이 실제 GatePolicy.from_dict 로 로드·3 엔트리."""

    def test_loads_without_error(self) -> None:
        gp = GatePolicy.from_dict(c2g.gate_policy())
        self.assertEqual(len(gp.entries), 3)
        self.assertEqual(gp.user_actor_class, "human")
        self.assertEqual(tuple(gp.escalation_resolvers), ("Advisor", "human"))

    def test_evaluate_maps_unit_types(self) -> None:
        gp = GatePolicy.from_dict(c2g.gate_policy())
        self.assertEqual(gp.evaluate({"unitType": "proposal"}), "user_decision_required")
        self.assertEqual(gp.evaluate({"unitType": "implementation"}), "review_required")
        self.assertEqual(gp.evaluate({"unitType": "milestone"}), "approval_required")


class MilestoneCp3WiringTests(unittest.TestCase):
    """항목 7 정정 — milestone(CP3 approval) 배선이 결정적으로 트리거 가능함을 증명."""

    def _prompt(self) -> str:
        contract = c2g.resolve_contract(_TMS_ROOT)
        graph = c2g.build_seed_graph(
            contract, _TMS_ROOT, mode="greenfield", phase_scope="phase1"
        )
        return graph["tasks"][0]["task"]

    def test_prompt_instructs_milestone_emission(self) -> None:
        """(a) 프롬프트에 milestone/approval 단위 방출 지시 문자열이 존재."""
        prompt = self._prompt()
        self.assertIn("milestone", prompt)
        self.assertIn("approval_required", prompt)
        self.assertIn("정확히 1개", prompt)  # milestone 정확히 1개 배합 지시.

    def test_seed_done_ac_checks_milestone(self) -> None:
        """seed done AC 가 milestone 최소 1건 + implementation 최소 1건을 검사."""
        contract = c2g.resolve_contract(_TMS_ROOT)
        graph = c2g.build_seed_graph(
            contract, _TMS_ROOT, mode="greenfield", phase_scope="phase1"
        )
        done = graph["tasks"][0]["done"]
        self.assertIn("milestone", done)
        self.assertIn("count('milestone')>=1", done)
        self.assertIn("count('implementation')>=1", done)

    def test_fixture_plan_triggers_cp3_via_policy(self) -> None:
        """(b) 결정적 fixture 계획(impl 2 + milestone 1) → 정책 evaluate 시 CP3 산출.

        LLM 없이 gate_policy() + GatePolicy.from_dict 로 각 단위를 evaluate 해
        approval_required(CP3) ≥1·review_required ≥1 을 실행 assert 한다(milestone 배선 증명).
        """
        # seed 프롬프트가 요구하는 형태를 모사한 대표 계획(impl 2 + milestone 1).
        fixture_tasks = [
            {"id": "master-domain", "unitType": "implementation"},
            {"id": "settlement-core", "unitType": "implementation"},
            {"id": "phase1-acceptance", "unitType": "milestone"},
        ]
        gp = GatePolicy.from_dict(c2g.gate_policy())
        gates = [gp.evaluate({"unitType": t["unitType"]}) for t in fixture_tasks]
        self.assertGreaterEqual(
            gates.count("approval_required"), 1,
            "milestone 단위가 CP3(approval_required)를 트리거하지 못함: " + repr(gates),
        )
        self.assertGreaterEqual(
            gates.count("review_required"), 1,
            "implementation 단위가 review_required 를 산출하지 못함: " + repr(gates),
        )


class CompilePurityTests(unittest.TestCase):
    """done 4 — compile 3키 dict·디스크 미기록(tmp 격리)."""

    def test_three_keys(self) -> None:
        out = c2g.compile(_TMS_ROOT, mode="greenfield", phase_scope="phase1")
        self.assertEqual(set(out.keys()), {"config", "graph", "gate_policy"})
        self.assertIn("workspace_dir", out["config"])
        self.assertIn("run_id", out["config"])
        self.assertIn("allowed_tools", out["config"])

    def test_no_disk_writes(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cd = root / ".claude" / "project-contract"
            cd.mkdir(parents=True)
            (cd / "project-contract.v2.md").write_text("x", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "solution-design.md").write_text("y", encoding="utf-8")

            def snapshot() -> set:
                return {str(p) for p in root.rglob("*")}

            before = snapshot()
            out = c2g.compile(root, mode="greenfield", phase_scope="phase1")
            after = snapshot()
            self.assertEqual(before, after)  # 디스크 미기록.
            self.assertEqual(set(out.keys()), {"config", "graph", "gate_policy"})


class OfflineSafeAcTests(unittest.TestCase):
    """done 5 — seed·프롬프트 done AC 오프라인 안전(금지 토큰 부재·안전 토큰 존재)."""

    _FORBIDDEN = ("tsc", "npm install", "npm run build", "npx")

    def _collect_ac_strings(self) -> list[str]:
        contract = c2g.resolve_contract(_TMS_ROOT)
        graph = c2g.build_seed_graph(
            contract, _TMS_ROOT, mode="greenfield", phase_scope="phase1"
        )
        task = graph["tasks"][0]
        return [task["done"], task["delegation"]["done"], task["task"]]

    def test_seed_done_forbidden_absent(self) -> None:
        task_done = self._collect_ac_strings()[0]
        for tok in self._FORBIDDEN:
            self.assertNotIn(tok, task_done, "seed done 에 금지 토큰: " + tok)

    def test_seed_done_safe_present(self) -> None:
        task_done = self._collect_ac_strings()[0]
        self.assertTrue(
            ("python -c" in task_done)
            or ("node --check" in task_done)
            or ("os.path.exists" in task_done),
            "seed done 에 오프라인 안전 검사가 없다: " + task_done,
        )

    def test_prompt_bans_online_tools(self) -> None:
        """프롬프트가 하위 task done AC 에 대해 npm install/tsc/build 금지를 명시하는가."""
        prompt = self._collect_ac_strings()[2]
        self.assertIn("금지", prompt)
        self.assertIn("npm install", prompt)  # 금지 대상으로 명시(문면에 등장).
        self.assertIn("node --check", prompt)  # 허용 안전 검사로 명시.

    def test_prompt_offers_offline_checks(self) -> None:
        prompt = self._collect_ac_strings()[2]
        self.assertIn("python -c", prompt)
        self.assertIn("os.path.exists", prompt)


class ConfigSchemaTests(unittest.TestCase):
    def test_build_config_keys(self) -> None:
        cfg = c2g.build_config(
            "orch-tms-phase1", str(_TMS_ROOT),
            allowed_tools=["Read", "Write"], timeout=900,
        )
        for k in ("run_id", "policy", "retry_limit", "timeout",
                  "allowed_tools", "output_format", "workspace_dir"):
            self.assertIn(k, cfg)
        self.assertEqual(cfg["workspace_dir"], str(_TMS_ROOT))
        self.assertEqual(cfg["policy"], "interactive")

    def test_allowed_tools_offline_no_npm(self) -> None:
        """오프라인 기본 allowed_tools 에 npm 이 없다(설치 불가)."""
        joined = " ".join(c2g.DEFAULT_ALLOWED_TOOLS)
        self.assertNotIn("npm", joined)
        self.assertIn("Bash(node:*)", c2g.DEFAULT_ALLOWED_TOOLS)
        self.assertIn("Bash(python:*)", c2g.DEFAULT_ALLOWED_TOOLS)


if __name__ == "__main__":
    unittest.main()
