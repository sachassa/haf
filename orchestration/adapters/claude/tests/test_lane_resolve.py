"""lane_resolve(형태 B 레인 판별 로더) + pretooluse_lane_guard(Write 시점 강제) 오프라인 테스트.

stdlib unittest 만 쓴다(형제 test_pretooluse_design_guard.py 관례 정합·오프라인·실 LLM 0).
로더·가드를 **subprocess**로 구동해 실제 CLI·종료 코드·stdin/stdout PreToolUse 계약을 검증한다.

검증 축은 위임 done 11항 + 원장 §2.1(판별식)·§2.2(판정 시점 2개)·§2.3(fail-closed 이진)의
열거에서 도출했다(축 발명 0 — docs/verification-checklist.md §5.8).

로더 케이스:
  L1 접점 포함        → lane=="standard"                       (done 1)
  L2 접점 0           → lane=="lightweight"                    (done 2)
  L3 선언 부재/공집합 → lane=="standard"·fail-closed           (done 3)
  L4 override+사유    → lane==override·사유 플래그 true         (done 4)
  L5 override-사유부재→ 비영 종료(3)                           (done 5·음성 대조)
  L6 결정성           → 연속 2회 stdout byte 동일               (done 7)
  L7 패턴 위치        → 접점 패턴 문자열이 레인 .py 에 0건      (done 8)
  L8 클래스 커버      → 등재 5클래스 각각 최소 1건 적중(전수)
  L9 루트 밖 대상     → standard(패턴 매칭 불가 fail-closed)
  L10 무효 레지스트리 → 비영 종료(4)(세 번째 레인 값 거부·음성 대조)

가드 케이스:
  G1 lightweight + 접점      → deny                            (done 9 단위 측·라이브는 보고 참조)
  G2 lightweight + 비접점    → deny 없음                       (음성 대조 — 통과 사유 확인)
  G3 standard + 접점         → deny 없음                       (강제 대상 레인만)
  G4 마커 부재               → deny 없음(무동작)
  G5 비-쓰기 도구            → deny 없음
  G6 깨진 stdin              → fail-open exit 0                (done 10)
  G7 마커 JSON 손상          → fail-open                       (done 10)
  G8 마커 lane 미인식 값     → fail-open                       (done 10)
  G9 lane_resolve import 불가→ fail-open                       (done 10)
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_TEST_FILE = Path(__file__).resolve()
_MODULE_DIR = _TEST_FILE.parents[1]          # orchestration/adapters/claude
_LOADER = _MODULE_DIR / "lane_resolve.py"
_GUARD = _MODULE_DIR / "pretooluse_lane_guard.py"
_REGISTRY = _MODULE_DIR / "lane-registry.json"

_REG = json.loads(_REGISTRY.read_text(encoding="utf-8"))
_MARKER_REL = _REG["marker"]["relativePath"]

def _sample_for_pattern(pat: str) -> str:
    """등재 패턴에서 그 패턴에 적중하는 대표 경로 표본을 **결정적으로 생성**한다.

    표본을 테스트 소스에 리터럴로 두지 않는 이유: 리터럴 패턴(예: 특정 게이트 파일 경로)은 표본과
    문자 단위로 같아져 done 8(패턴 문자열이 .py 에 0건) 판정을 오염시킨다 — 실측으로 검출됨.
    따라서 표본은 데이터에서 파생한다(단일 소스 유지).
    """
    star = "*"
    out = pat.replace(star * 2 + "/", "seg/").replace(star * 2, "seg/leaf")
    return out.replace(star, "x").replace("?", "y")


# 클래스명 → 그 클래스의 첫 패턴에서 파생한 대표 경로 표본(등재 5클래스 전수 커버 확인용).
_CLASS_SAMPLES = {
    cls["class"]: _sample_for_pattern(cls["patterns"][0]) for cls in _REG["touchpointClasses"]
}
# 패턴별 표본(전 패턴 전수 커버 — 클래스 단위보다 촘촘한 축).
_PATTERN_SAMPLES = [
    (cls["class"], pat, _sample_for_pattern(pat))
    for cls in _REG["touchpointClasses"] for pat in cls["patterns"]
]
# 접점 0 대상(어느 클래스에도 적중하지 않는 표면).
_NON_TOUCH = ["docs/session-handoff.md", "README.md", "src/app/main.ts"]


def _run_loader(args, *, stdin: str = None):
    proc = subprocess.run(
        [sys.executable, str(_LOADER), *args],
        input=stdin, capture_output=True, text=True, encoding="utf-8",
    )
    return proc.returncode, proc.stdout, proc.stderr


def _run_guard(payload, *, raw: str = None, guard: Path = None):
    stdin = raw if raw is not None else json.dumps(payload, ensure_ascii=False)
    proc = subprocess.run(
        [sys.executable, str(guard or _GUARD)],
        input=stdin, capture_output=True, text=True, encoding="utf-8",
    )
    return proc.returncode, proc.stdout, proc.stderr


def _decision(stdout: str):
    s = stdout.strip()
    if not s:
        return None
    try:
        doc = json.loads(s)
    except ValueError:
        return None
    return (doc.get("hookSpecificOutput") or {}).get("permissionDecision")


class TestLaneResolveLoader(unittest.TestCase):
    def _resolve(self, targets, extra=()):
        args = []
        for t in targets:
            args += ["--target", t]
        args += list(extra)
        rc, out, err = _run_loader(args)
        self.assertEqual(rc, 0, "예상 exit 0, 실제 %d: %s" % (rc, err))
        return json.loads(out)

    # --- L1: 접점 1건 포함 → standard (done 1) ------------------------------------
    def test_L1_touchpoint_yields_standard(self):
        doc = self._resolve([_NON_TOUCH[0], _CLASS_SAMPLES["정본 문서"]])
        self.assertEqual(doc["lane"], "standard")
        self.assertEqual(doc["basis"], "touchpoint-match")
        self.assertEqual(doc["touchedCount"], 1)

    # --- L2: 접점 0 → lightweight (done 2) ----------------------------------------
    def test_L2_no_touchpoint_yields_lightweight(self):
        doc = self._resolve(_NON_TOUCH)
        self.assertEqual(doc["lane"], "lightweight")
        self.assertEqual(doc["basis"], "no-touchpoint")
        self.assertEqual(doc["touchedCount"], 0)

    # --- L3: 선언 부재 → standard(fail-closed) (done 3) ---------------------------
    def test_L3_no_declaration_fail_closed(self):
        doc = self._resolve([])
        self.assertEqual(doc["lane"], "standard")
        self.assertEqual(doc["basis"], "fail-closed:no-declared-targets")

    def test_L3_empty_stdin_declaration_fail_closed(self):
        rc, out, err = _run_loader(["--stdin"], stdin=json.dumps({"declaredTargets": []}))
        self.assertEqual(rc, 0, err)
        self.assertEqual(json.loads(out)["lane"], "standard")

    # --- L4: override 양방향 + 사유 플래그 (done 4) --------------------------------
    def test_L4_override_to_lightweight_with_reason(self):
        doc = self._resolve(
            [_CLASS_SAMPLES["게이트"]],  # 접점이지만 override 가 우선한다.
            extra=["--override", "lightweight", "--override-reason", "사용자 판단: 오타 1자 정정"],
        )
        self.assertEqual(doc["lane"], "lightweight")
        self.assertEqual(doc["basis"], "override")
        self.assertTrue(doc["laneOverrideReasonRequired"])
        self.assertEqual(doc["laneOverrideReason"], "사용자 판단: 오타 1자 정정")

    def test_L4_override_to_standard_with_reason(self):
        doc = self._resolve(
            _NON_TOUCH,  # 접점 0 이지만 override 로 승급.
            extra=["--override", "standard", "--override-reason", "사용자 판단: 리스크 높음"],
        )
        self.assertEqual(doc["lane"], "standard")
        self.assertTrue(doc["laneOverrideReasonRequired"])

    def test_L4_no_override_flag_is_false(self):
        doc = self._resolve(_NON_TOUCH)
        self.assertFalse(doc["laneOverrideReasonRequired"])
        self.assertIsNone(doc["laneOverrideReason"])

    # --- L5: override + 사유 부재 → 비영 종료 (done 5·음성 대조) -------------------
    def test_L5_override_without_reason_is_nonzero(self):
        rc, out, err = _run_loader(["--target", _NON_TOUCH[0], "--override", "lightweight"])
        self.assertNotEqual(rc, 0, "사유 없는 override 는 비영 종료여야 한다")
        self.assertEqual(rc, 3)
        self.assertEqual(out.strip(), "", "실패 시 판정 JSON 을 방출하지 않는다")
        self.assertIn("OVERRIDE-REASON-MISSING", err)

    def test_L5_override_with_blank_reason_is_nonzero(self):
        rc, _out, err = _run_loader(
            ["--target", _NON_TOUCH[0], "--override", "lightweight", "--override-reason", "   "])
        self.assertEqual(rc, 3, err)

    # --- L6: 결정성 — 연속 2회 byte 동일 (done 7) ---------------------------------
    def test_L6_determinism_byte_identical(self):
        args = ["--target", _NON_TOUCH[0], "--target", _CLASS_SAMPLES["스키마"]]
        rc1, out1, _ = _run_loader(args)
        rc2, out2, _ = _run_loader(args)
        self.assertEqual((rc1, rc2), (0, 0))
        self.assertEqual(out1.encode("utf-8"), out2.encode("utf-8"))

    # --- L7: 접점 패턴 문자열이 레인 .py 에 0건 (done 8) --------------------------
    def test_L7_no_pattern_literals_in_lane_python(self):
        patterns = [p for cls in _REG["touchpointClasses"] for p in cls["patterns"]]
        self.assertGreaterEqual(len(patterns), 5)
        offenders = []
        for py in (_LOADER, _GUARD, _TEST_FILE):
            text = py.read_text(encoding="utf-8")
            for pat in patterns:
                if pat in text:
                    offenders.append((py.name, pat))
        self.assertEqual(offenders, [], "접점 패턴 리터럴이 .py 에 있다: %r" % (offenders,))

    # --- L8: 등재 전 패턴·전 클래스 전수 커버 --------------------------------------
    def test_L8_every_registered_pattern_matches_its_sample(self):
        self.assertGreaterEqual(len(_PATTERN_SAMPLES), 5)
        for cls_name, pat, sample in _PATTERN_SAMPLES:
            doc = self._resolve([sample])
            rec = doc["declaredTargets"][0]
            self.assertTrue(rec["touched"], "패턴 %s 표본 %s 미적중" % (pat, sample))
            self.assertEqual(rec["matchedClass"], cls_name,
                             "패턴 %s 표본이 다른 클래스에 먼저 적중" % pat)
            self.assertEqual(doc["lane"], "standard")

    def test_L8b_every_registered_class_matches_a_sample(self):
        registered = [cls["class"] for cls in _REG["touchpointClasses"]]
        self.assertEqual(sorted(registered), sorted(_CLASS_SAMPLES.keys()),
                         "등재 클래스 집합과 표본 집합이 어긋난다(축 누락 방지)")
        for cls_name, sample in _CLASS_SAMPLES.items():
            doc = self._resolve([sample])
            rec = doc["declaredTargets"][0]
            self.assertTrue(rec["touched"], "%s 표본 %s 미적중" % (cls_name, sample))
            self.assertEqual(rec["matchedClass"], cls_name)
            self.assertEqual(doc["lane"], "standard")

    # --- L9: 루트 밖 대상 → 패턴 매칭 불가 fail-closed ----------------------------
    def test_L9_unresolvable_target_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            outside = Path(td) / "elsewhere" / "notes.txt"
            doc = self._resolve([str(outside)])
            self.assertEqual(doc["lane"], "standard")
            self.assertEqual(doc["basis"], "fail-closed:unresolvable-target")
            self.assertFalse(doc["declaredTargets"][0]["resolvable"])

    # --- L10: 무효 레지스트리(세 번째 레인 값) → 비영 종료 ------------------------
    def test_L10_third_lane_value_registry_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            bad = json.loads(_REGISTRY.read_text(encoding="utf-8"))
            bad["laneVocabulary"] = ["standard", "lightweight", "medium"]
            reg_path = Path(td) / "bad-registry.json"
            reg_path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
            rc, _out, err = _run_loader(
                ["--target", _NON_TOUCH[0], "--registry", str(reg_path)])
            self.assertEqual(rc, 4, err)
            self.assertIn("REGISTRY-INVALID", err)

    def test_L10_missing_registry_rejected(self):
        rc, _out, err = _run_loader(
            ["--target", _NON_TOUCH[0], "--registry", "존재하지-않는-레지스트리.json"])
        self.assertEqual(rc, 4, err)


class TestPreToolUseLaneGuard(unittest.TestCase):
    def _workspace(self, td: str, lane, *, raw_marker: str = None) -> Path:
        ws = Path(td) / "ws"
        marker = ws / _MARKER_REL
        marker.parent.mkdir(parents=True, exist_ok=True)
        if raw_marker is not None:
            marker.write_text(raw_marker, encoding="utf-8")
        else:
            marker.write_text(json.dumps(
                {"lane": lane, "laneOverrideReason": None,
                 "declaredTargets": [], "decidedAt": "2026-07-26T00:00:00Z"},
                ensure_ascii=False), encoding="utf-8")
        return ws

    def _payload(self, ws: Path, rel: str, tool: str = "Write"):
        return {"tool_name": tool,
                "tool_input": {"file_path": str(ws / rel)},
                "cwd": str(ws)}

    # --- G1: lightweight + 접점 → deny -------------------------------------------
    def test_G1_lightweight_touchpoint_denied(self):
        with tempfile.TemporaryDirectory() as td:
            ws = self._workspace(td, "lightweight")
            for cls_name, sample in _CLASS_SAMPLES.items():
                rc, out, err = _run_guard(self._payload(ws, sample))
                self.assertEqual(rc, 0, err)
                self.assertEqual(_decision(out), "deny",
                                 "%s 접점(%s)은 경량 레인에서 차단: %r" % (cls_name, sample, out))
                self.assertIn("LANE-LIGHTWEIGHT", out)

    # --- G2: lightweight + 비접점 → 허용(음성 대조) ------------------------------
    def test_G2_lightweight_non_touchpoint_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            ws = self._workspace(td, "lightweight")
            for rel in _NON_TOUCH:
                rc, out, err = _run_guard(self._payload(ws, rel))
                self.assertEqual(rc, 0, err)
                self.assertIsNone(_decision(out), "비접점(%s)은 허용: %r" % (rel, out))

    # --- G3: standard + 접점 → 허용(강제 대상 레인만) ----------------------------
    def test_G3_standard_lane_not_enforced(self):
        with tempfile.TemporaryDirectory() as td:
            ws = self._workspace(td, "standard")
            rc, out, err = _run_guard(self._payload(ws, _CLASS_SAMPLES["게이트"]))
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out), "standard 레인은 이 훅의 강제 대상이 아니다: %r" % out)

    # --- G4: 마커 부재 → 무동작 ---------------------------------------------------
    def test_G4_no_marker_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "plain"
            (ws / "docs").mkdir(parents=True)
            rc, out, err = _run_guard(self._payload(ws, _CLASS_SAMPLES["게이트"]))
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out), "마커 부재는 무동작 통과: %r" % out)

    # --- G5: 비-쓰기 도구 → 무동작 -----------------------------------------------
    def test_G5_non_write_tool_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            ws = self._workspace(td, "lightweight")
            rc, out, err = _run_guard(self._payload(ws, _CLASS_SAMPLES["게이트"], tool="Read"))
            self.assertEqual(rc, 0, err)
            self.assertIsNone(_decision(out))

    # --- G6: 깨진 stdin → fail-open (done 10-①) ----------------------------------
    def test_G6_broken_stdin_fail_open(self):
        rc, out, err = _run_guard(None, raw="이건 JSON 이 아니다 {{{")
        self.assertEqual(rc, 0, "fail-open 은 exit 0")
        self.assertIsNone(_decision(out), "fail-open 은 deny 없음: %r" % out)
        self.assertIn("fail-open", err)

    def test_G6b_non_object_stdin_fail_open(self):
        rc, out, err = _run_guard(None, raw="[1, 2, 3]")
        self.assertEqual(rc, 0)
        self.assertIsNone(_decision(out))
        self.assertIn("fail-open", err)

    # --- G7: 마커 JSON 손상 → fail-open (done 10-②) ------------------------------
    def test_G7_corrupt_marker_fail_open(self):
        with tempfile.TemporaryDirectory() as td:
            ws = self._workspace(td, None, raw_marker="{이건 JSON 이 아니다")
            rc, out, err = _run_guard(self._payload(ws, _CLASS_SAMPLES["게이트"]))
            self.assertEqual(rc, 0)
            self.assertIsNone(_decision(out), "마커 파싱 실패는 무동작 통과: %r" % out)
            self.assertIn("fail-open", err)

    # --- G8: 마커 lane 미인식 값 → fail-open (done 10-③) -------------------------
    def test_G8_unknown_lane_value_fail_open(self):
        with tempfile.TemporaryDirectory() as td:
            ws = self._workspace(td, "medium")
            rc, out, err = _run_guard(self._payload(ws, _CLASS_SAMPLES["게이트"]))
            self.assertEqual(rc, 0)
            self.assertIsNone(_decision(out))
            self.assertIn("fail-open", err)

    # --- G9: lane_resolve import 불가 → fail-open (done 10-④) --------------------
    def test_G9_import_failure_fail_open(self):
        with tempfile.TemporaryDirectory() as td:
            # 가드만 격리 복사(형제 lane_resolve.py·lane-registry.json 없음) → import 실패.
            lonely = Path(td) / "lonely"
            lonely.mkdir()
            guard_copy = lonely / _GUARD.name
            shutil.copyfile(_GUARD, guard_copy)
            ws = self._workspace(td, "lightweight")
            rc, out, err = _run_guard(self._payload(ws, _CLASS_SAMPLES["게이트"]),
                                      guard=guard_copy)
            self.assertEqual(rc, 0, "import 실패도 fail-open exit 0")
            self.assertIsNone(_decision(out), "import 실패는 차단하지 않는다: %r" % out)
            self.assertIn("fail-open", err)


if __name__ == "__main__":
    unittest.main()
