"""verify_checks 결정적 테스트 (LLM 0·순수 결정적·파일시스템 픽스처·네트워크 0).

검사 대상(done 매핑):
  - (a) VT-1 존재 vs 부재 산출물 — check_artifacts.
  - (b) VT-4 금지 패턴 있음 vs 없음 — scan_patterns.
  - (c) VT-4 전수성 — 한 파일 다중 매치·다중 파일·한 라인 다중 매치를 빠짐없이 수집.
  - (d) 빈 입력 — 빈 artifacts/patterns 처리.
  - 결정성 — 같은 입력·같은 파일시스템 → 같은 출력(바이트 동일).
  - CLI end-to-end(subprocess) — --artifact/--pattern/--scan·--stdin·종료 코드.
  - scope 정직성 — 바이너리·비UTF8 파일은 filesSkipped 로 노출(누락 은폐 없음).

픽스처는 tmp_path 아래에 합성 폴더를 만든다(실 UAF 저장소 무접촉).
"""

import json
import os
import subprocess
import sys

import pytest

import verify_checks
from verify_checks import (
    PatternError,
    check_artifacts,
    resolve_scan_files,
    run_checks,
    scan_patterns,
)


# ==========================================================================
# (a) VT-1 산출물 존재 검증 — 존재 vs 부재.
# ==========================================================================
def test_vt1_present_vs_absent(tmp_path):
    (tmp_path / "exists.txt").write_text("hi", encoding="utf-8")
    (tmp_path / "adir").mkdir()
    res = check_artifacts(["exists.txt", "adir", "missing.txt"], tmp_path)
    assert res["checked"] == 3
    by_path = {r["path"]: r for r in res["results"]}
    assert by_path["exists.txt"]["exists"] is True
    assert by_path["exists.txt"]["type"] == "file"
    assert by_path["adir"]["exists"] is True
    assert by_path["adir"]["type"] == "dir"
    assert by_path["missing.txt"]["exists"] is False
    assert by_path["missing.txt"]["type"] is None
    assert res["present"] == ["exists.txt", "adir"]
    assert res["absent"] == ["missing.txt"]


def test_vt1_preserves_input_order(tmp_path):
    # 결정성: results 순서 = 입력 순서.
    for n in ("c", "a", "b"):
        (tmp_path / n).write_text("x", encoding="utf-8")
    res = check_artifacts(["c", "a", "b"], tmp_path)
    assert [r["path"] for r in res["results"]] == ["c", "a", "b"]


def test_vt1_absolute_path(tmp_path):
    target = tmp_path / "abs.txt"
    target.write_text("x", encoding="utf-8")
    res = check_artifacts([str(target)], tmp_path / "otherroot")
    # 절대경로는 root 무관하게 판정.
    assert res["results"][0]["exists"] is True


# ==========================================================================
# (b) VT-4 금지 패턴 있음 vs 없음.
# ==========================================================================
def test_vt4_pattern_present_and_absent(tmp_path):
    (tmp_path / "f.txt").write_text("alpha TODO beta\ngamma\n", encoding="utf-8")
    res = scan_patterns(["TODO", "NOTHERE"], ["f.txt"], tmp_path)
    reports = {p["pattern"]: p for p in res["patterns"]}
    assert reports["TODO"]["count"] == 1
    assert reports["TODO"]["matches"][0]["file"] == "f.txt"
    assert reports["TODO"]["matches"][0]["line"] == 1
    assert reports["TODO"]["matches"][0]["col"] == 7  # 1-base 열.
    assert reports["TODO"]["matches"][0]["match"] == "TODO"
    # 없는 패턴도 리포트에 count 0 으로 존재(명시적).
    assert reports["NOTHERE"]["count"] == 0
    assert reports["NOTHERE"]["matches"] == []
    assert res["totalMatches"] == 1


# ==========================================================================
# (c) VT-4 전수성 — 다중 매치·다중 파일·한 라인 다중 매치 전부 수집.
# ==========================================================================
def test_vt4_exhaustive_multi_match_multi_file(tmp_path):
    # 파일1: 3개 매치(2개 라인, 그중 한 라인에 2개), 파일2: 1개 매치. 총 4개.
    (tmp_path / "a.txt").write_text("X and X here\nnone\nX again\n", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "b.txt").write_text("only one X\n", encoding="utf-8")
    res = scan_patterns(["X"], ["."], tmp_path)  # 디렉터리 재귀 스캔.
    rep = res["patterns"][0]
    assert rep["count"] == 4, rep["matches"]  # 전수 — 라인 축약 시 3 이 되어 실패.
    assert res["totalMatches"] == 4
    # 한 라인 다중 매치가 서로 다른 열로 개별 수집됐는지.
    a_line1 = [m for m in rep["matches"] if m["file"] == "a.txt" and m["line"] == 1]
    assert len(a_line1) == 2
    assert sorted(m["col"] for m in a_line1) == [1, 7]
    # 다중 파일 커버.
    files = {m["file"] for m in rep["matches"]}
    assert files == {"a.txt", "sub/b.txt"}
    assert res["filesScanned"] == 2


def test_vt4_exhaustive_regex_pattern(tmp_path):
    # 정규식 패턴의 모든 매치도 전수 수집(리터럴 아님).
    (tmp_path / "code.py").write_text(
        "import ai_helper\nx = call_ai()\nsafe = 1\nAI_MODE = True\n", encoding="utf-8")
    res = scan_patterns([r"(?i)ai"], ["code.py"], tmp_path)
    rep = res["patterns"][0]
    # ai_helper(1), call_ai(1), AI_MODE(1) = 3 (case-insensitive).
    assert rep["count"] == 3, rep["matches"]
    lines = sorted(m["line"] for m in rep["matches"])
    assert lines == [1, 2, 4]


def test_vt4_glob_scope(tmp_path):
    (tmp_path / "keep.py").write_text("BAD\n", encoding="utf-8")
    (tmp_path / "skip.md").write_text("BAD\n", encoding="utf-8")
    d = tmp_path / "deep" / "nested"
    d.mkdir(parents=True)
    (d / "x.py").write_text("BAD BAD\n", encoding="utf-8")
    res = scan_patterns(["BAD"], ["**/*.py"], tmp_path)  # .py 만·재귀.
    files = {m["file"] for m in res["patterns"][0]["matches"]}
    assert files == {"keep.py", "deep/nested/x.py"}  # skip.md 제외.
    assert res["patterns"][0]["count"] == 3  # keep(1) + x.py(2).


# ==========================================================================
# (d) 빈 입력.
# ==========================================================================
def test_empty_artifacts(tmp_path):
    res = check_artifacts([], tmp_path)
    assert res["checked"] == 0
    assert res["results"] == []
    assert res["present"] == [] and res["absent"] == []


def test_empty_scan_scope(tmp_path):
    # 패턴은 있으나 스캔 범위 없음 → 파일 0·매치 0(에러 아님).
    res = scan_patterns(["TODO"], [], tmp_path)
    assert res["filesScanned"] == 0
    assert res["patterns"][0]["count"] == 0
    assert res["totalMatches"] == 0


def test_run_checks_omits_absent_sections(tmp_path):
    # artifacts 만 → vt1 만. patterns 만 → vt4 만. 둘 다 없으면 상위 CLI 가 막는다.
    only1 = run_checks(["x"], None, None, tmp_path)
    assert "vt1" in only1 and "vt4" not in only1
    only4 = run_checks(None, ["x"], ["."], tmp_path)
    assert "vt4" in only4 and "vt1" not in only4


# ==========================================================================
# 결정성 — 같은 입력·같은 파일시스템 → 같은 출력(바이트 동일).
# ==========================================================================
def test_determinism_same_input_same_output(tmp_path):
    (tmp_path / "a.txt").write_text("TODO x\nTODO y\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text("TODO z\n", encoding="utf-8")
    (tmp_path / "keep.txt").write_text("ok", encoding="utf-8")
    args = (["keep.txt", "missing"], ["TODO"], ["."], tmp_path)
    out1 = json.dumps(run_checks(*args), ensure_ascii=False, sort_keys=False)
    out2 = json.dumps(run_checks(*args), ensure_ascii=False, sort_keys=False)
    assert out1 == out2


def test_scan_files_sorted(tmp_path):
    for n in ("z.txt", "a.txt", "m.txt"):
        (tmp_path / n).write_text("x", encoding="utf-8")
    files = resolve_scan_files(["."], tmp_path)
    names = [f.name for f in files]
    assert names == sorted(names)  # 정렬 = 결정적 순회.


# ==========================================================================
# scope 정직성 — 바이너리·비UTF8 파일은 filesSkipped 로 노출(누락 은폐 없음).
# ==========================================================================
def test_vt4_binary_file_skipped_not_hidden(tmp_path):
    (tmp_path / "text.txt").write_text("TODO here\n", encoding="utf-8")
    (tmp_path / "blob.bin").write_bytes(b"TODO\x00\x01binary")  # 널바이트 = 바이너리.
    res = scan_patterns(["TODO"], ["."], tmp_path)
    assert res["patterns"][0]["count"] == 1  # 텍스트 파일에서만.
    skipped = {s["file"]: s["reason"] for s in res["filesSkipped"]}
    assert skipped.get("blob.bin") == "binary"  # 누락이 아니라 명시적 노출.


def test_vt4_non_utf8_skipped(tmp_path):
    (tmp_path / "cp949.txt").write_bytes("금지어".encode("cp949"))  # 비 UTF-8.
    res = scan_patterns(["x"], ["."], tmp_path)
    skipped = {s["file"]: s["reason"] for s in res["filesSkipped"]}
    assert skipped.get("cp949.txt") == "non-utf8"


# ==========================================================================
# 패턴 오류 — 잘못된 정규식은 재해석 없이 오류로 에스컬레이션.
# ==========================================================================
def test_bad_regex_raises(tmp_path):
    (tmp_path / "f.txt").write_text("x", encoding="utf-8")
    with pytest.raises(PatternError):
        scan_patterns(["[unclosed"], ["f.txt"], tmp_path)


# ==========================================================================
# CLI end-to-end (subprocess) — entry 선례 동형.
# ==========================================================================
def _run_cli(args, tmp_path, stdin_text=None):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(verify_checks.__file__), *args],
        capture_output=True, text=True, encoding="utf-8", env=env,
        input=stdin_text, cwd=str(tmp_path),
    )


def test_cli_vt1_and_vt4(tmp_path):
    (tmp_path / "present.txt").write_text("data", encoding="utf-8")
    (tmp_path / "scan.txt").write_text("FIXME now\nFIXME again\n", encoding="utf-8")
    proc = _run_cli(
        ["--artifact", "present.txt", "--artifact", "gone.txt",
         "--pattern", "FIXME", "--scan", "scan.txt", "--root", "."],
        tmp_path)
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["vt1"]["present"] == ["present.txt"]
    assert out["vt1"]["absent"] == ["gone.txt"]
    assert out["vt4"]["patterns"][0]["count"] == 2
    assert out["vt4"]["totalMatches"] == 2


def test_cli_stdin(tmp_path):
    (tmp_path / "s.txt").write_text("TODO\nTODO\nTODO\n", encoding="utf-8")
    payload = json.dumps({"vt4": {"patterns": ["TODO"], "scan": ["s.txt"]}})
    proc = _run_cli(["--stdin", "--root", "."], tmp_path, stdin_text=payload)
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["vt4"]["patterns"][0]["count"] == 3
    assert "vt1" not in out  # artifacts 미제공 → vt1 없음.


def test_cli_no_input_usage_error(tmp_path):
    proc = _run_cli([], tmp_path)
    assert proc.returncode == 2  # 입력 없음 = 사용법 오류.


def test_cli_bad_pattern_exit3(tmp_path):
    (tmp_path / "f.txt").write_text("x", encoding="utf-8")
    proc = _run_cli(["--pattern", "[bad", "--scan", "f.txt", "--root", "."], tmp_path)
    assert proc.returncode == 3
    assert "BAD-PATTERN" in proc.stderr


def test_cli_does_not_mutate(tmp_path):
    # 순수 판독 — 스캔·검사가 파일시스템을 바꾸지 않음.
    (tmp_path / "f.txt").write_text("TODO", encoding="utf-8")
    before = sorted(p.name for p in tmp_path.iterdir())
    _run_cli(["--pattern", "TODO", "--scan", ".", "--artifact", "f.txt", "--root", "."], tmp_path)
    after = sorted(p.name for p in tmp_path.iterdir())
    assert before == after
