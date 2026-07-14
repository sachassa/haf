"""T1-② 번들 payload 계측 단위 테스트 (합성 invoke 로그·순수 판독·run 원장 무접촉).

검증 축:
  (a) argv 의 -p 다음 원소 UTF-8 바이트 산출 정확성(멀티바이트 한글/일본어 포함).
  (b) by_class 귀속 = 기존 classify(role, gate_id) 규칙과 동일.
  (c) -p 부재/argv 결손 세션의 분리 계수(0 왜곡 금지).

conftest.py 가 상위 e2e/ 를 sys.path 에 배선하므로 collect_metrics 를 flat import 한다.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import collect_metrics as cm


# --- 합성 invoke 로그/rec 헬퍼 -------------------------------------------------
def _write_invoke(dirpath, name, role, gate_id, bundle=None,
                  include_p=True, include_argv=True):
    """합성 invoke-*.json 을 물리화한다(임시 dir·run 원장 무접촉)."""
    argv = ["claude"]
    if include_p:
        if bundle is not None:
            argv += ["-p", bundle]
        else:
            argv += ["-p"]  # -p 는 있으나 다음 원소 결손.
    argv += ["--model", "sonnet", "--output-format", "json"]
    rec = {
        "invoke_seq": 1, "role": role, "step_id": "s", "gate_id": gate_id,
        "model": "sonnet", "session_id": "sess-x",
        "raw_stdout": json.dumps({"usage": {}, "total_cost_usd": 0.0}),
    }
    if include_argv:
        rec["argv"] = argv
    p = Path(dirpath) / name
    p.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    return p


def _rec(role, gate_id, payload_bytes=None, missing=False):
    """bundle_payload_block 입력용 최소 rec(parse_invoke_log 산출 동형)."""
    return {"role": role, "gate_id": gate_id,
            "payload_bytes": payload_bytes, "payload_missing": missing}


# --- (a) UTF-8 바이트 산출 정확성 ----------------------------------------------
class Utf8ByteCount(unittest.TestCase):
    def test_multibyte_korean_japanese(self):
        bundle = '{"goal": "한글 목표 テスト 混在"}'  # 멀티바이트 다수.
        with tempfile.TemporaryDirectory() as tmp:
            p = _write_invoke(tmp, "invoke-01.json", "Worker", None, bundle=bundle)
            rec = cm.parse_invoke_log(p)
        expected = len(bundle.encode("utf-8"))
        self.assertFalse(rec["payload_missing"])
        self.assertEqual(rec["payload_bytes"], expected)
        # 멀티바이트 증거: 바이트 수 > 문자 수(한글/일본어는 3바이트).
        self.assertGreater(expected, len(bundle))

    def test_ascii_bytes_equal_len(self):
        bundle = '{"a": 1}'  # 순수 ASCII.
        with tempfile.TemporaryDirectory() as tmp:
            p = _write_invoke(tmp, "invoke-01.json", "Worker", None, bundle=bundle)
            rec = cm.parse_invoke_log(p)
        self.assertEqual(rec["payload_bytes"], len(bundle))  # ASCII 는 1바이트/문자.

    def test_payload_computed_even_on_raw_stdout_parse_error(self):
        # raw_stdout 파싱 실패로 조기 반환하더라도 payload 는 argv 로 독립 산출된다.
        bundle = '{"goal": "값"}'
        with tempfile.TemporaryDirectory() as tmp:
            argv = ["claude", "-p", bundle, "--model", "sonnet"]
            rec_json = {"role": "Worker", "gate_id": None, "argv": argv,
                        "raw_stdout": "NOT JSON <<<"}
            p = Path(tmp) / "invoke-01.json"
            p.write_text(json.dumps(rec_json, ensure_ascii=False), encoding="utf-8")
            rec = cm.parse_invoke_log(p)
        self.assertIsNotNone(rec["parse_error"])            # raw 파싱은 실패했으나
        self.assertEqual(rec["payload_bytes"], len(bundle.encode("utf-8")))  # payload 는 산출.
        self.assertFalse(rec["payload_missing"])


# --- (b) by_class 귀속(classify 규칙 동일) -------------------------------------
class ByClassAttribution(unittest.TestCase):
    def test_three_classes_attributed(self):
        rows = [
            _rec("Worker", None, payload_bytes=10),      # Worker step.
            _rec("Verifier", None, payload_bytes=20),    # CP2(gate_id 없음).
            _rec("Verifier", "g1", payload_bytes=30),    # gate re-verification.
        ]
        blk = cm.bundle_payload_block(rows)
        self.assertEqual(blk["by_class_bytes"]["Worker step"], 10)
        self.assertEqual(blk["by_class_bytes"]["CP2"], 20)
        self.assertEqual(blk["by_class_bytes"]["gate re-verification"], 30)
        self.assertEqual(blk["total_bytes"], 60)
        self.assertEqual(blk["sessions_counted"], 3)
        self.assertEqual(blk["sessions_missing_argv"], 0)
        self.assertEqual(blk["grade"], cm.G_CONFIRMED)
        # by_class 합 == total.
        self.assertEqual(sum(blk["by_class_bytes"].values()), blk["total_bytes"])

    def test_classify_rule_matches_collect_metrics(self):
        # bundle_payload 귀속 규칙이 collect_metrics.classify 와 동일해야 한다.
        self.assertEqual(cm.classify("Worker", None), "Worker step")
        self.assertEqual(cm.classify("Verifier", None), "CP2")
        self.assertEqual(cm.classify("Verifier", "g1"), "gate re-verification")

    def test_per_session_stats(self):
        rows = [_rec("Worker", None, payload_bytes=b) for b in (10, 30, 20)]
        blk = cm.bundle_payload_block(rows)
        self.assertEqual(blk["per_session"]["min"], 10)
        self.assertEqual(blk["per_session"]["max"], 30)
        self.assertEqual(blk["per_session"]["median"], 20)  # 홀수 → 중앙값.

    def test_per_session_median_even_count(self):
        rows = [_rec("Worker", None, payload_bytes=b) for b in (10, 20)]
        blk = cm.bundle_payload_block(rows)
        self.assertEqual(blk["per_session"]["median"], 15.0)  # 짝수 → 평균(float).


# --- (c) 결손 argv/-p 분리 계수 -----------------------------------------------
class MissingArgvSeparation(unittest.TestCase):
    def test_missing_argv_and_missing_p_counted_separately(self):
        with tempfile.TemporaryDirectory() as tmp:
            p1 = _write_invoke(tmp, "invoke-01.json", "Worker", None, bundle='{"a":1}')
            p2 = _write_invoke(tmp, "invoke-02.json", "Worker", None,
                               include_argv=False)                    # argv 결손.
            p3 = _write_invoke(tmp, "invoke-03.json", "Verifier", None,
                               bundle=None, include_p=False)          # argv 있으나 -p 부재.
            rows = [cm.parse_invoke_log(x) for x in (p1, p2, p3)]
        blk = cm.bundle_payload_block(rows)
        self.assertEqual(blk["sessions_counted"], 1)
        self.assertEqual(blk["sessions_missing_argv"], 2)
        self.assertEqual(blk["total_bytes"], len('{"a":1}'.encode("utf-8")))
        # 결손 세션은 by_class 합산에 0 을 넣지 않는다(왜곡 금지) — total = 계측 세션 합.
        self.assertEqual(sum(blk["by_class_bytes"].values()), blk["total_bytes"])

    def test_p_flag_present_but_no_following_element(self):
        # argv 마지막이 "-p" 인 경우(다음 원소 결손) → 미상(index+1 범위 밖).
        with tempfile.TemporaryDirectory() as tmp:
            rec_json = {"role": "Worker", "gate_id": None,
                        "argv": ["claude", "-p"], "raw_stdout": "{}"}
            pp = Path(tmp) / "invoke-01.json"
            pp.write_text(json.dumps(rec_json), encoding="utf-8")
            rec = cm.parse_invoke_log(pp)
        self.assertTrue(rec["payload_missing"])
        self.assertIsNone(rec["payload_bytes"])

    def test_all_missing_per_session_none(self):
        rows = [_rec("Worker", None, missing=True),
                _rec("Verifier", None, missing=True)]
        blk = cm.bundle_payload_block(rows)
        self.assertEqual(blk["sessions_counted"], 0)
        self.assertEqual(blk["sessions_missing_argv"], 2)
        self.assertEqual(blk["total_bytes"], 0)
        self.assertIsNone(blk["per_session"]["min"])
        self.assertIsNone(blk["per_session"]["median"])
        self.assertIsNone(blk["per_session"]["max"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
