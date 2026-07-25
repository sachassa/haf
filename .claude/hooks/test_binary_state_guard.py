"""binary_state_guard 단위 테스트 (표준 라이브러리 unittest 만 사용).

실행:
  PYTHONIOENCODING=utf-8 python -m unittest discover -s .claude/hooks -p "test_*.py" -v
또는:
  PYTHONIOENCODING=utf-8 python .claude/hooks/test_binary_state_guard.py

검사 대상:
  1) 백로그 등재 형식 검사(신규) — 6종 (a)~(f)
  2) 기존 어휘·완전성 검사 회귀 — 추가 검사 배선이 기존 판정을 바꾸지 않음을 고정
"""

import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import binary_state_guard as guard  # noqa: E402

BACKLOG = "docs/post-tuning-improvement-backlog.md"


def invoke(tool_name, tool_input, raw=None):
    """훅을 stdin 계약으로 호출하고 (exit_code, stdout) 을 돌려준다."""
    if raw is None:
        raw = json.dumps({"tool_name": tool_name, "tool_input": tool_input},
                         ensure_ascii=False)
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = guard.run(raw)
    return code, out.getvalue()


def assert_deny(testcase, code, stdout):
    """deny 계약 동형 단언 — exit 0 + stdout deny JSON."""
    testcase.assertEqual(0, code, "PreToolUse 계약상 종료 코드는 항상 0")
    payload = json.loads(stdout)
    hook_out = payload["hookSpecificOutput"]
    testcase.assertEqual("PreToolUse", hook_out["hookEventName"])
    testcase.assertEqual("deny", hook_out["permissionDecision"])
    return hook_out["permissionDecisionReason"]


class BacklogFormatCheckTest(unittest.TestCase):
    """신규 검사 6종 — 위임 done #3 (a)~(f) 에 1:1 대응."""

    def test_a_missing_enforcement_in_new_item_denies(self):
        content = (
            "## S. 새 백로그 항목\n\n"
            "- **Problem**: 어떤 문제.\n"
            "- **Desired Outcome**: 어떤 결과.\n"
        )
        code, stdout = invoke("Edit", {"file_path": BACKLOG, "new_string": content})
        reason = assert_deny(self, code, stdout)
        self.assertIn("S. 새 백로그 항목", reason)
        self.assertIn("강제 지점", reason)

    def test_b_item_with_enforcement_line_passes(self):
        content = (
            "## S. 새 백로그 항목\n\n"
            "- **Problem**: 어떤 문제.\n"
            "- **강제 지점**: `.claude/hooks/binary_state_guard.py` 에서 차단.\n"
        )
        code, stdout = invoke("Edit", {"file_path": BACKLOG, "new_string": content})
        self.assertEqual(0, code)
        self.assertEqual("", stdout)

    def test_c_same_heading_in_other_md_is_not_checked(self):
        content = "## A. 다른 문서의 항목 헤딩\n\n본문만 있고 강제 표기는 없다.\n"
        code, stdout = invoke("Write", {"file_path": "docs/other-doc.md",
                                        "content": content})
        self.assertEqual(0, code)
        self.assertEqual("", stdout)

    def test_d_full_file_write_segment_judgement(self):
        """머리 문단의 '강제 지점' 이 다른 항목의 누락을 가리지 못한다(세그먼트 판정)."""
        content = (
            "# Post-Tuning Improvement Backlog\n\n"
            "**등재 형식 규율**: 신규 항목은 「강제 지점」 행을 포함한다.\n\n"
            "---\n\n"
            "## A. 첫 항목\n\n"
            "- **강제 지점**: 게이트 X 에서 강제.\n\n"
            "## B. 둘째 항목\n\n"
            "- **Problem**: 해당 표기가 빠진 항목.\n\n"
        )
        code, stdout = invoke("Write", {"file_path": BACKLOG, "content": content})
        reason = assert_deny(self, code, stdout)
        self.assertIn("B. 둘째 항목", reason)
        self.assertNotIn("A. 첫 항목", reason)

    def test_e_allow_legacy_marker_passes(self):
        content = (
            "## S. 새 백로그 항목\n\n"
            "- **Problem**: 어떤 문제.\n"
            "%s 과거 등재 문면 이력 인용.\n" % guard.MARKER
        )
        code, stdout = invoke("Edit", {"file_path": BACKLOG, "new_string": content})
        self.assertEqual(0, code)
        self.assertEqual("", stdout)

    def test_f_non_json_stdin_fails_open(self):
        code, stdout = invoke(None, None, raw="not-json{")
        self.assertEqual(0, code)
        self.assertEqual("", stdout, "fail-open 은 차단 JSON 을 내지 않는다")


class BacklogFormatPureFunctionTest(unittest.TestCase):
    """순수 함수 단위 — 배선과 무관하게 판정 규칙을 고정한다."""

    def test_path_matching_is_basename_and_case_insensitive(self):
        self.assertTrue(guard.is_backlog_path(
            r"C:\p\docs\Post-Tuning-Improvement-Backlog.md"))
        self.assertTrue(guard.is_backlog_path(
            "/home/x/docs/post-tuning-improvement-backlog.md"))
        self.assertFalse(guard.is_backlog_path("docs/session-handoff.md"))
        self.assertFalse(guard.is_backlog_path(None))

    def test_multi_letter_and_trailing_segment(self):
        text = "## AB. 두 글자 항목\n\n본문 끝(다음 헤딩 없음).\n"
        self.assertEqual(["## AB. 두 글자 항목"],
                         guard.find_backlog_format_violations(text))

    def test_non_item_headings_are_ignored(self):
        text = "## 일반 헤딩\n\n본문.\n\n### D. 서브 헤딩\n\n본문.\n"
        self.assertEqual([], guard.find_backlog_format_violations(text))

    def test_h1_terminates_segment(self):
        text = ("## S. 항목\n\n본문.\n\n# 다른 절\n\n여기 강제 지점 이 있어도 무관.\n")
        self.assertEqual(["## S. 항목"], guard.find_backlog_format_violations(text))


class ExistingChecksRegressionTest(unittest.TestCase):
    """기존 검사 회귀 — 추가 검사 배선이 기존 판정을 바꾸지 않음을 고정한다."""

    def test_state_term_still_denied(self):
        code, stdout = invoke("Write", {"file_path": "docs/x.md",
                                        "content": "이 항목은 부분 해소 상태다.\n"})
        reason = assert_deny(self, code, stdout)
        self.assertIn("부분 해소", reason)

    def test_hedge_term_still_denied(self):
        code, stdout = invoke("Edit", {"file_path": "docs/x.md",
                                       "new_string": "가급적 이렇게 한다.\n"})
        assert_deny(self, code, stdout)

    def test_completeness_claim_without_evidence_denied(self):
        code, stdout = invoke("Write", {"file_path": "docs/x.md",
                                        "content": "잔여 0 이다.\n"})
        reason = assert_deny(self, code, stdout)
        self.assertIn("완전성 주장", reason)

    def test_completeness_claim_with_evidence_passes(self):
        code, stdout = invoke("Write", {
            "file_path": "docs/x.md",
            "content": "잔여 0 이다. uaf-verified: rg 로 저장소 .md 전 파일 스윕.\n"})
        self.assertEqual(0, code)
        self.assertEqual("", stdout)

    def test_non_md_path_skipped(self):
        code, stdout = invoke("Write", {"file_path": "src/x.py",
                                        "content": "부분 해소\n"})
        self.assertEqual(0, code)
        self.assertEqual("", stdout)

    def test_multiedit_new_strings_are_scanned(self):
        code, stdout = invoke("MultiEdit", {
            "file_path": "docs/x.md",
            "edits": [{"old_string": "a", "new_string": "정상 문면."},
                      {"old_string": "b", "new_string": "판정 보류 상태."}]})
        reason = assert_deny(self, code, stdout)
        self.assertIn("판정 보류", reason)

    def test_clean_text_passes(self):
        code, stdout = invoke("Write", {"file_path": "docs/x.md",
                                        "content": "이 항목은 해소됐다.\n"})
        self.assertEqual(0, code)
        self.assertEqual("", stdout)

    def test_backlog_check_does_not_shadow_term_check(self):
        """백로그 파일이라도 형식이 맞으면 기존 어휘 검사가 그대로 동작한다."""
        content = ("## S. 항목\n\n- **강제 지점**: 훅에서 차단.\n"
                   "- **상태**: 부분 해소.\n")
        code, stdout = invoke("Edit", {"file_path": BACKLOG, "new_string": content})
        reason = assert_deny(self, code, stdout)
        self.assertIn("부분 해소", reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)
