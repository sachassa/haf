"""render_gates (OQ-PO-B1 게이트 큐 렌더러) 오프라인 테스트 — 실 LLM/CLI 미발화(stdlib unittest).

form-B 결정적 렌더러의 계약을 실제 코드로 뒷받침한다(§DC-9·binding §3.2):
  - r1: user_decision + escalation 요구 2건 → 라벨 2종·gate_id·적격 actor·해소 명령 포함.
  - r2: 그중 1건을 적격 actor 로 해소한 원장 → 해소된 게이트가 렌더에서 제외(파생 뷰 정확).
  - r3: --json 구조(원 필드 + label + eligible_resolvers + resolve_command).
  - r4: 동일 입력 2회 실행 stdout 바이트 동일(결정성).
  - r5: 실행 전후 run_dir 파일 목록·내용 무변경(원장 무변경·읽기 전용).
  - r6: pending 0건 문면("미해소 정지 게이트 없음").

중립 코드(gates·events)·resolve_gate 는 무수정 import 만 한다(재정의 0).
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# --- 경로 배선: 렌더러 모듈 디렉터리 ------------------------------------------
_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]          # orchestration/adapters/claude
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import render_gates as rgd  # noqa: E402  (import 시 e2e·중립 코드 경로 배선)

from gates import (  # noqa: E402
    GATE_ESCALATION_REQUIRED,
    GATE_USER_DECISION_REQUIRED,
    GatePolicy,
    append_gate_requirement,
    append_gate_resolution,
)
from events import EventLog, JsonlEventStore  # noqa: E402


# --------------------------------------------------------------------------
# 픽스처 — run_dir 에 gate_policy.json + events.jsonl(게이트 요구) 시드
# --------------------------------------------------------------------------
def _seed_run(base: Path, requirements, *, resolutions=None, policy=None) -> Path:
    """run_dir 을 만들고 gate_policy.json + events.jsonl(요구·선택 해소) 을 시드한다.

    requirements: [(gate_id, gateKind)] — 각 게이트 요구 이벤트.
    resolutions:  [(gate_id, gateKind, actor)] — 요구 이후 append 할 해소 이벤트(선택).
    policy: gate_policy.json 로 직렬화할 dict(기본 {} — userActorClass=human·resolvers=(Advisor,human)).
    """
    run = base / "run"
    (run / "logs").mkdir(parents=True)
    run.mkdir(parents=True, exist_ok=True)

    (run / "gate_policy.json").write_text(
        json.dumps(policy if policy is not None else {}), encoding="utf-8"
    )

    log = EventLog(JsonlEventStore(str(run / "events.jsonl")))
    for gate_id, gate_kind in requirements:
        append_gate_requirement(
            log, gate_id, gate_kind,
            target={"unitId": gate_id},
            scoped_question={"unitId": gate_id, "gateKind": gate_kind},
        )
    for gate_id, gate_kind, actor in (resolutions or []):
        append_gate_resolution(log, gate_id, gate_kind, actor=actor)
    return run


def _run_main(argv):
    """render_gates.main(argv) 을 stdout 캡처로 실행 → (rc, stdout_str)."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = rgd.main(argv)
    return rc, buf.getvalue()


def _snapshot(root: Path) -> dict:
    """root 하위 전 파일 (상대경로 -> 바이트) 스냅샷(원장 무변경 검증용)."""
    snap = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            snap[str(p.relative_to(root))] = p.read_bytes()
    return snap


# ==========================================================================
# r1 — 두 정지 게이트 요구 → 라벨·gate_id·적격 actor·해소 명령 포함
# ==========================================================================
class TestRenderTwoGates(unittest.TestCase):
    def test_render_contains_both_gates(self):
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [
                ("g-user", GATE_USER_DECISION_REQUIRED),
                ("g-esc", GATE_ESCALATION_REQUIRED),
            ])
            rc, out = _run_main([str(run)])
            self.assertEqual(rc, 0)
            # 라벨 2종(binding §3.2 승계 문면).
            self.assertIn("사용자 결정 대기(확정 권위)", out)
            self.assertIn("Advisor/사람 해소 대기", out)
            # gate_id.
            self.assertIn("g-user", out)
            self.assertIn("g-esc", out)
            # 적격 해소 actor(정책 데이터 파생·기본값): user_decision=human·escalation=Advisor,human.
            self.assertIn("적격 해소 actor: human", out)
            self.assertIn("Advisor", out)
            # 해소 명령(resolve_gate.py 실제 CLI 형태).
            self.assertIn("resolve_gate.py", out)
            self.assertIn("--gate-kind user_decision --actor human", out)
            self.assertIn("--gate-kind escalation --actor Advisor", out)
            # 요구 순번(since) 표기.
            self.assertIn("요구 순번", out)


# ==========================================================================
# r2 — 1건 적격 해소 → 해소된 게이트 렌더 제외(파생 뷰 정확·부분 해소 후 재렌더)
# ==========================================================================
class TestResolvedGateExcluded(unittest.TestCase):
    def test_resolved_gate_not_rendered(self):
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(
                Path(td),
                [("g-user", GATE_USER_DECISION_REQUIRED),
                 ("g-esc", GATE_ESCALATION_REQUIRED)],
                # escalation 을 적격 actor(Advisor)로 해소 → 렌더에서 빠져야 한다.
                resolutions=[("g-esc", GATE_ESCALATION_REQUIRED, "Advisor")],
            )
            rc, out = _run_main([str(run)])
            self.assertEqual(rc, 0)
            self.assertIn("g-user", out)          # 미해소 → 잔존.
            self.assertNotIn("g-esc", out)        # 적격 해소 → 제외.
            self.assertIn("(1건)", out)            # 1건만 남음.

    def test_ineligible_resolution_keeps_gate(self):
        # 부적격 actor(user_decision 을 Advisor)로 해소 시도 → 여전히 미해소·렌더 잔존.
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(
                Path(td),
                [("g-user", GATE_USER_DECISION_REQUIRED)],
                resolutions=[("g-user", GATE_USER_DECISION_REQUIRED, "Advisor")],
            )
            rc, out = _run_main([str(run)])
            self.assertEqual(rc, 0)
            self.assertIn("g-user", out)  # 부적격 해소는 무효 → 잔존.


# ==========================================================================
# r3 — --json 구조 검증
# ==========================================================================
class TestJsonOutput(unittest.TestCase):
    def test_json_structure(self):
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [
                ("g-user", GATE_USER_DECISION_REQUIRED),
                ("g-esc", GATE_ESCALATION_REQUIRED),
            ])
            rc, out = _run_main([str(run), "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(out)
            self.assertEqual(len(payload), 2)
            by_id = {it["gate_id"]: it for it in payload}
            u = by_id["g-user"]
            # pending_gates 원 필드 보존.
            for k in ("gate_id", "gateKind", "target", "scoped_question", "since"):
                self.assertIn(k, u)
            # 파생 추가 필드.
            self.assertEqual(u["label"], "사용자 결정 대기(확정 권위)")
            self.assertEqual(u["eligible_resolvers"], ["human"])
            self.assertIn("--gate-kind user_decision --actor human", u["resolve_command"])
            e = by_id["g-esc"]
            self.assertEqual(e["eligible_resolvers"], ["Advisor", "human"])
            self.assertIn("--gate-kind escalation --actor Advisor", e["resolve_command"])


# ==========================================================================
# r4 — 결정성(동일 입력 2회 → stdout 바이트 동일)
# ==========================================================================
class TestDeterminism(unittest.TestCase):
    def test_two_runs_identical_stdout(self):
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [
                ("g-user", GATE_USER_DECISION_REQUIRED),
                ("g-esc", GATE_ESCALATION_REQUIRED),
            ])
            _, out1 = _run_main([str(run)])
            _, out2 = _run_main([str(run)])
            self.assertEqual(out1, out2)
            # --json 도 결정적.
            _, j1 = _run_main([str(run), "--json"])
            _, j2 = _run_main([str(run), "--json"])
            self.assertEqual(j1, j2)


# ==========================================================================
# r5 — 원장 무변경(실행 전후 run_dir 파일 목록·내용 동일)
# ==========================================================================
class TestLedgerUnchanged(unittest.TestCase):
    def test_render_does_not_write_any_file(self):
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [
                ("g-user", GATE_USER_DECISION_REQUIRED),
                ("g-esc", GATE_ESCALATION_REQUIRED),
            ])
            before = _snapshot(run)
            _run_main([str(run)])
            _run_main([str(run), "--json"])
            after = _snapshot(run)
            self.assertEqual(before, after, "렌더는 어떤 파일도 쓰지 않는다(읽기 전용)")


# ==========================================================================
# r6 — pending 0건 문면
# ==========================================================================
class TestNoPending(unittest.TestCase):
    def test_no_pending_message(self):
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [])  # 요구 이벤트 0.
            rc, out = _run_main([str(run)])
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "미해소 정지 게이트 없음")

    def test_all_resolved_is_no_pending(self):
        # 요구 후 전부 적격 해소 → 미해소 0건 문면.
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(
                Path(td),
                [("g-user", GATE_USER_DECISION_REQUIRED)],
                resolutions=[("g-user", GATE_USER_DECISION_REQUIRED, "human")],
            )
            rc, out = _run_main([str(run)])
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "미해소 정지 게이트 없음")


# ==========================================================================
# 오류 처리 — run_dir/파일 부재 → stderr + exit 1
# ==========================================================================
class TestErrors(unittest.TestCase):
    def test_absent_run_dir_returns_1(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "nope"
            rc, _ = _run_main([str(missing)])
            self.assertEqual(rc, 1)

    def test_absent_events_returns_1(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td) / "run"
            run.mkdir()
            (run / "gate_policy.json").write_text("{}", encoding="utf-8")
            rc, _ = _run_main([str(run)])
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
