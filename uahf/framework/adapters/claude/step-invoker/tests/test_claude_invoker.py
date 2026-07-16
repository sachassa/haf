"""ClaudeInvoker 자체 테스트 — 명령행 조립·결과 파싱 (CLI 실호출 없음·W3 소관).

표준 라이브러리 unittest 만 사용한다. 실제 claude 프로세스를 띄우지 않고, build_command·
permission_flags·parse_result 의 순수 로직만 검증한다.
"""

from __future__ import annotations

import os
import sys
import unittest

# step-invoker 디렉터리(대상 모듈)를 sys.path 에 넣는다. claude_invoker 가 임포트 시
# 중립 Host 의 invoker 계약 경로도 sys.path 에 추가한다.
_INVOKER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _INVOKER_DIR not in sys.path:
    sys.path.insert(0, _INVOKER_DIR)

from claude_invoker import ClaudeInvoker  # noqa: E402
from invoker import (  # noqa: E402
    InvokeRequest,
    KIND_BLOCKED,
    KIND_COMPLETION,
    KIND_FAILURE,
    POLICY_AUTO_APPROVE,
    POLICY_INTERACTIVE,
    POLICY_UNRESTRICTED,
    ROLE_VERIFIER,
    ROLE_WORKER,
)


def req(policy=POLICY_INTERACTIVE, role=ROLE_WORKER, model=None, workdir=None):
    return InvokeRequest(
        bundle={"step_contract": {"id": "s1"}, "feedback": None},
        role=role, model=model, policy=policy, workdir=workdir,
    )


class PermissionMappingTest(unittest.TestCase):
    def test_interactive_no_bypass_flag(self):
        inv = ClaudeInvoker()
        self.assertEqual(inv.permission_flags(POLICY_INTERACTIVE), [])

    def test_auto_approve_maps_accept_edits(self):
        inv = ClaudeInvoker()
        self.assertEqual(inv.permission_flags(POLICY_AUTO_APPROVE),
                         ["--permission-mode", "acceptEdits"])

    def test_unrestricted_maps_dangerously_skip(self):
        inv = ClaudeInvoker()
        self.assertEqual(inv.permission_flags(POLICY_UNRESTRICTED),
                         ["--dangerously-skip-permissions"])


class CommandAssemblyTest(unittest.TestCase):
    def test_headless_print_and_json_output(self):
        inv = ClaudeInvoker()
        cmd = inv.build_command(req())
        self.assertEqual(cmd[0], "claude")
        self.assertIn("-p", cmd)
        self.assertIn("--output-format", cmd)
        self.assertEqual(cmd[cmd.index("--output-format") + 1], "json")

    def test_interactive_has_no_dangerous_flag(self):
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(policy=POLICY_INTERACTIVE))
        self.assertNotIn("--dangerously-skip-permissions", cmd)

    def test_unrestricted_has_dangerous_flag(self):
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(policy=POLICY_UNRESTRICTED))
        self.assertIn("--dangerously-skip-permissions", cmd)

    def test_model_slot_passed(self):
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(model="slot-alias"))
        self.assertIn("--model", cmd)
        self.assertEqual(cmd[cmd.index("--model") + 1], "slot-alias")

    def test_model_omitted_when_absent(self):
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(model=None))
        self.assertNotIn("--model", cmd)

    def test_workdir_added(self):
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(workdir=os.getcwd()))
        self.assertIn("--add-dir", cmd)

    def test_role_brief_in_system_prompt(self):
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(role=ROLE_VERIFIER))
        self.assertIn("--append-system-prompt", cmd)
        brief = cmd[cmd.index("--append-system-prompt") + 1]
        self.assertIn("Verifier", brief)

    def test_prompt_carries_bundle(self):
        inv = ClaudeInvoker()
        prompt = inv.build_prompt(req())
        self.assertIn("step_contract", prompt)


class ResultParsingTest(unittest.TestCase):
    def _envelope(self, result_text, is_error=False):
        import json
        return json.dumps({"type": "result", "result": result_text, "is_error": is_error})

    def test_parse_completion_report(self):
        inv = ClaudeInvoker()
        text = '작업 완료. {"artifacts":["a.md"],"self_check":"done","verify_basis":"x"}'
        res = inv.parse_result(self._envelope(text), 0)
        self.assertEqual(res.kind, KIND_COMPLETION)
        self.assertEqual(res.completion["artifacts"], ["a.md"])

    def test_parse_failure_report(self):
        inv = ClaudeInvoker()
        text = '{"reason":"결함","repro":"입력X","blocking":"계속 가능"}'
        res = inv.parse_result(self._envelope(text), 0)
        self.assertEqual(res.kind, KIND_FAILURE)

    def test_parse_blocked_report(self):
        inv = ClaudeInvoker()
        text = '{"reason":"의존 미확정","blocking":"차단됨"}'
        res = inv.parse_result(self._envelope(text), 0)
        self.assertEqual(res.kind, KIND_BLOCKED)

    def test_parse_verdict_pass(self):
        inv = ClaudeInvoker()
        text = '판정 결과 {"verdict":"Pass","rework":null}'
        res = inv.parse_result(self._envelope(text), 0)
        self.assertEqual(res.kind, KIND_COMPLETION)
        self.assertTrue(res.verdict_pass())

    def test_parse_verdict_fail(self):
        inv = ClaudeInvoker()
        text = '{"verdict":"Fail","rework":"AC-2 미충족"}'
        res = inv.parse_result(self._envelope(text), 0)
        self.assertEqual(res.kind, KIND_COMPLETION)
        self.assertFalse(res.verdict_pass())
        self.assertEqual(res.rework(), "AC-2 미충족")

    def test_parse_missing_report_is_failure(self):
        inv = ClaudeInvoker()
        res = inv.parse_result(self._envelope("보고 없음 텍스트만"), 0)
        self.assertEqual(res.kind, KIND_FAILURE)

    def test_extract_last_json_object(self):
        inv = ClaudeInvoker()
        text = '{"verdict":"Fail"} 이후 정정 {"verdict":"Pass"}'
        res = inv.parse_result(self._envelope(text), 0)
        self.assertTrue(res.verdict_pass())

    def test_plain_text_stdout_without_envelope(self):
        inv = ClaudeInvoker()
        # --output-format text 처럼 봉투 없이 보고만 온 경우도 파싱한다.
        text = '{"artifacts":["x"],"self_check":"ok"}'
        res = inv.parse_result(text, 0)
        self.assertEqual(res.kind, KIND_COMPLETION)


if __name__ == "__main__":
    unittest.main(verbosity=2)
