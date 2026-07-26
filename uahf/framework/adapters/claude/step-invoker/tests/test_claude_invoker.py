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


class VerifierAcAdequacyBriefTest(unittest.TestCase):
    """백로그 O · D-O2 — Verifier 브리프의 AC 적정성 / 실출력 픽스처 판정 축.

    접합부 왕복: 브리프 상수를 직접 읽지 않고 build_command() 실호출로 조립된 argv 의
    --append-system-prompt 값을 검사한다(실 CLI 미발화 — argv 조립까지).
    """

    def _verifier_system_prompt(self) -> str:
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(role=ROLE_VERIFIER))
        self.assertIn("--append-system-prompt", cmd)
        return cmd[cmd.index("--append-system-prompt") + 1]

    def test_ac_adequacy_axis_reaches_argv(self) -> None:
        """(i) AC 적정성 판정 축이 실제 argv 에 실린다."""
        brief = self._verifier_system_prompt()
        self.assertIn("AC 적정성", brief)
        self.assertIn("합성", brief)          # 합성 입력이 실출력을 대체했는가.
        self.assertIn("통과했다", brief)      # 통과 자체가 증거가 되는가.

    def test_inadequate_ac_forces_fail_with_ac_defect(self) -> None:
        """부적정 AC 는 Fail + rework 에 AC 결함 명시 지시가 argv 에 실린다."""
        brief = self._verifier_system_prompt()
        self.assertIn("Fail", brief)
        self.assertIn("AC 결함", brief)

    def test_external_tool_fixture_axis_reaches_argv(self) -> None:
        """(ii) 외부 도구 호출 단위의 실출력 픽스처 소비 확인 축이 argv 에 실린다."""
        brief = self._verifier_system_prompt()
        self.assertIn("실출력 캡처 픽스처", brief)
        self.assertIn("미검증 외부 계약", brief)

    def test_existing_verifier_sentences_preserved(self) -> None:
        """가법 증명 — 기존 브리프 문장(신뢰 금지·결정적 리포트·참조형 sentinel)이 보존됨."""
        brief = self._verifier_system_prompt()
        self.assertIn("완료 보고를 그대로 신뢰하지 말고", brief)
        self.assertIn("결정적 검증 리포트", brief)
        self.assertIn("참조형 표준", brief)
        # verdict JSON 출력 계약이 여전히 브리프의 마지막 지시로 남아있다.
        self.assertIn('{"verdict":"Pass|Fail","rework":...}', brief)

    def test_worker_brief_untouched_by_verifier_axes(self) -> None:
        """Worker 브리프에는 신규 축 문면이 새지 않는다(역할 격리)."""
        inv = ClaudeInvoker()
        cmd = inv.build_command(req(role=ROLE_WORKER))
        brief = cmd[cmd.index("--append-system-prompt") + 1]
        self.assertIn("너는 Worker 다", brief)
        self.assertNotIn("AC 적정성", brief)
        self.assertNotIn("미검증 외부 계약", brief)


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
