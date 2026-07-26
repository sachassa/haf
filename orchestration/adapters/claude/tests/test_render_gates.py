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


# ==========================================================================
# r7 — resolve_command 의 --gate-id 지목 (렌더 ↔ resolve_gate 접합 정합)
# --------------------------------------------------------------------------
# resolve_gate 는 같은 gateKind 가 2건 이상 pending 이면 무지목 호출을 차단한다(binding §3.4).
# 따라서 항목별 렌더 명령은 그 게이트의 gate_id 를 항상 실어야 **그대로 실행 가능**하다.
# ==========================================================================
def _seed_stop_signal(run: Path) -> list:
    """렌더와 같은 파생 뷰로 logs/stop-signal.json 을 시드한다(런처 계약 동형·resolve_gate 입력).

    렌더 자체는 stop-signal 을 읽지 않는다(원장 직접 파생) — 이 파일은 **resolve_gate 쪽**
    입력이다. 왕복 테스트가 두 접합면을 같은 run 에서 잇기 위해 필요하다.
    """
    pending, _policy = rgd.load_pending(run)
    (run / "logs").mkdir(parents=True, exist_ok=True)
    (run / "logs" / "stop-signal.json").write_text(
        json.dumps({"stop_reason": "gate", "stopped_tasks": [g["gate_id"] for g in pending],
                    "pending_gates": pending}, ensure_ascii=False),
        encoding="utf-8",
    )
    return pending


def _executable_argv(command: str, run_dir: Path) -> list:
    """렌더가 낸 명령 문자열을 **그대로** 받아 resolve_gate.main 이 먹는 argv 로 만든다.

    치환은 문서화된 자리표시자 관례 2가지뿐이다 — `<run_dir>` → 실제 경로 · 대괄호로 감싼
    선택 인자(`[--response "…"]`)는 제거. 옵션 이름·순서·`--gate-id` 값은 손대지 않는다.
    """
    import re
    import shlex

    text = re.sub(r"\[[^\]]*\]", "", command).strip()
    tokens = shlex.split(text)
    assert tokens[0] == "python" and tokens[1] == rgd.RESOLVE_SCRIPT, tokens
    return [str(run_dir) if t == "<run_dir>" else t for t in tokens[2:]]


class TestResolveCommandNamesGate(unittest.TestCase):
    def test_r7a_text_and_json_commands_carry_gate_id(self):
        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [
                ("g-user", GATE_USER_DECISION_REQUIRED),
                ("g-esc", GATE_ESCALATION_REQUIRED),
            ])
            # 텍스트 모드 — 각 블록의 해소 명령에 그 게이트의 gate_id 가 실린다.
            rc, out = _run_main([str(run)])
            self.assertEqual(rc, 0)
            self.assertIn("--gate-kind user_decision --actor human --gate-id g-user", out)
            self.assertIn("--gate-kind escalation --actor Advisor --gate-id g-esc", out)

            # JSON 모드 — 항목별 resolve_command 가 자기 gate_id 만 지목한다(교차 오염 0).
            rc, out = _run_main([str(run), "--json"])
            self.assertEqual(rc, 0)
            by_id = {it["gate_id"]: it for it in json.loads(out)}
            for gid, other in (("g-user", "g-esc"), ("g-esc", "g-user")):
                cmd = by_id[gid]["resolve_command"]
                self.assertIn("--gate-id %s" % gid, cmd)
                self.assertNotIn(other, cmd)

    def test_r7b_unit_contract_of_resolve_command(self):
        policy = GatePolicy.from_dict({})
        # gate_id 미지정(일반형) = 종전 문면 — 가법 보장.
        plain = rgd.resolve_command(GATE_ESCALATION_REQUIRED, policy)
        self.assertNotIn("--gate-id", plain)
        # 엔진 파생 gate_id(`::` 포함)는 인용 없이 그대로 실린다.
        named = rgd.resolve_command(GATE_ESCALATION_REQUIRED, policy,
                                    "gate-unit-impl-1::exec-escalation")
        self.assertIn("--gate-id gate-unit-impl-1::exec-escalation", named)
        # 공백 등 안전 집합 밖 문자는 인용된다(셸 토큰 분해 방지).
        quoted = rgd.resolve_command(GATE_ESCALATION_REQUIRED, policy, "gate id with space")
        self.assertIn('--gate-id "gate id with space"', quoted)
        # 미지 gateKind 는 종전대로 명령을 구성하지 않는다.
        self.assertIn("미지 gateKind", rgd.resolve_command("nope", policy, "g-x"))

    def test_r7c_roundtrip_multi_pending_each_command_resolves_own_gate(self):
        """접합부 왕복 — 다중 pending run 에서 렌더 명령을 그대로 실행해 자기 게이트만 해소."""
        import resolve_gate as rg  # noqa: E402  (같은 어댑터 경계)
        from gates import is_resolved  # noqa: E402

        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [
                ("gate-unit-a::exec-escalation", GATE_ESCALATION_REQUIRED),
                ("gate-unit-b::exec-escalation", GATE_ESCALATION_REQUIRED),
            ])
            pending = _seed_stop_signal(run)
            self.assertEqual(len(pending), 2, "전제: 동일 kind 2건 pending")
            policy = GatePolicy.from_dict({})

            rc, out = _run_main([str(run), "--json"])
            self.assertEqual(rc, 0)
            items = json.loads(out)

            # 첫 명령을 그대로 실행 → 자기 게이트만 해소되고 나머지는 pending 유지.
            first, second = items[0], items[1]
            argv = _executable_argv(first["resolve_command"], run)
            self.assertIn("--gate-id", argv, "렌더 명령이 지목을 싣지 않으면 다중 pending 에서 차단된다")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = rg.main(argv)
            self.assertEqual(code, 0, buf.getvalue())

            events = [json.loads(l) for l in
                      (run / "events.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
            self.assertTrue(is_resolved(events, first["gate_id"], GATE_ESCALATION_REQUIRED, policy))
            self.assertFalse(is_resolved(events, second["gate_id"], GATE_ESCALATION_REQUIRED, policy),
                             "지목하지 않은 게이트는 미해소로 남는다")

            # 두 번째 명령도 그대로 실행 → 나머지 게이트 해소(잔여 pending 0).
            _seed_stop_signal(run)
            buf2 = io.StringIO()
            with redirect_stdout(buf2):
                code2 = rg.main(_executable_argv(second["resolve_command"], run))
            self.assertEqual(code2, 0, buf2.getvalue())
            rc, out = _run_main([str(run)])
            self.assertEqual(out.strip(), "미해소 정지 게이트 없음")

    def test_r7d_roundtrip_single_pending_command_executes(self):
        """단일 pending 에서도 렌더 명령(지목 포함)이 그대로 실행된다 — 회귀 방지."""
        import resolve_gate as rg  # noqa: E402

        with tempfile.TemporaryDirectory() as td:
            run = _seed_run(Path(td), [("g-solo-esc", GATE_ESCALATION_REQUIRED)])
            _seed_stop_signal(run)
            rc, out = _run_main([str(run), "--json"])
            self.assertEqual(rc, 0)
            item = json.loads(out)[0]

            buf = io.StringIO()
            with redirect_stdout(buf):
                code = rg.main(_executable_argv(item["resolve_command"], run))
            self.assertEqual(code, 0, buf.getvalue())
            _, out = _run_main([str(run)])
            self.assertEqual(out.strip(), "미해소 정지 게이트 없음")


if __name__ == "__main__":
    unittest.main()
