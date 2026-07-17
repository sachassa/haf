"""entry_resolve 결정적 테스트 (LLM 0·순수 결정적·파일시스템 픽스처).

검사 대상:
  - 결정 테이블 8조합(01 §3.2-D) 각각이 정확히 한 결과(matchedRow·mode)로 해소됨(결정성·EN-INV 3).
  - **게이트 = canonical 결정 테이블 policy 단일 소스**(policy.ref == user-confirmation-gate·행
    2·3·4·5). 행 1·6·7·8 = 게이트 없음. 특히 **행 7(/continue+contract유+repo무)=incremental·게이트
    없음**(CP2 거짓 게이트 정정 회귀 테스트).
  - Registry 무결성(전수·상호배타 분할·01 §3.2-A 4단계).
  - --entry 정규화(new|continue → /new·/continue·Git Bash MSYS 안전·OQ-7).
  - 엔진이 <folder> 를 수정하지 않음(순수 판독·EN-INV 1).

픽스처는 tmp_path 아래에 합성 폴더를 만든다(실 UAF 저장소 무접촉). contract·repo 축을 직교로 구성한다.
"""

import json
import os
import subprocess
import sys

import pytest

import entry_resolve
from entry_resolve import (
    ABSENT,
    PRESENT,
    load_registry,
    normalize_entry,
    resolve,
    verify_determinism,
)

REGISTRY_PATH = entry_resolve.DEFAULT_REGISTRY

# 01 §3.2-D 정본 결정 테이블 — (entry, contract, repo) → (row, mode, gate).
# 게이트 = policy.ref == user-confirmation-gate (canonical 행 2·3·4·5). 행 1·6·7·8 = 게이트 없음.
CANONICAL_TABLE = [
    ("/new",      ABSENT,  ABSENT,  1, "greenfield",  False),
    ("/new",      ABSENT,  PRESENT, 2, "greenfield",  True),
    ("/new",      PRESENT, ABSENT,  3, "greenfield",  True),
    ("/new",      PRESENT, PRESENT, 4, "greenfield",  True),
    ("/continue", ABSENT,  ABSENT,  5, "greenfield",  True),
    ("/continue", ABSENT,  PRESENT, 6, "brownfield",  False),
    ("/continue", PRESENT, ABSENT,  7, "incremental", False),
    ("/continue", PRESENT, PRESENT, 8, "incremental", False),
]


@pytest.fixture()
def reg():
    return load_registry(REGISTRY_PATH)


def make_folder(tmp_path, *, contract: bool, repo: bool, exist: bool = True):
    """(contract, repo) 상태를 가진 합성 폴더를 만든다.
      contract 유 → <folder>/.claude/project-contract/project-contract.v1.md
      repo 유     → <folder>/src/app.txt (본체 파일)
      exist=False → 폴더 자체를 만들지 않는다(부재 관측 — 신규 폴더명 케이스).
    """
    folder = tmp_path / "workspace"
    if not exist:
        return folder  # mkdir 하지 않음 — 부재.
    folder.mkdir(parents=True, exist_ok=True)
    if contract:
        cdir = folder / ".claude" / "project-contract"
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / "project-contract.v1.md").write_text("---\nschemaVersion: '1.0'\n---\n", encoding="utf-8")
    if repo:
        src = folder / "src"
        src.mkdir(parents=True, exist_ok=True)
        (src / "app.txt").write_text("project body content", encoding="utf-8")
    return folder


# --------------------------------------------------------------------------
# ⑤ 8조합 결정성 — 각 (entry, contract, repo) 가 정확히 단일 행·정본 mode·정본 게이트.
# --------------------------------------------------------------------------
@pytest.mark.parametrize("entry,contract,repo,row,mode,gate", CANONICAL_TABLE)
def test_eight_combos_deterministic(reg, tmp_path, entry, contract, repo, row, mode, gate):
    folder = make_folder(tmp_path, contract=(contract == PRESENT), repo=(repo == PRESENT))
    result = resolve(reg, entry, folder, intent=None)  # 기본 의도 사용(게이트 미구동).
    # 관측이 의도한 축과 일치.
    obs = {i["sourceType"]: i["observed"] for i in result["inputs"]}
    assert obs["contract-presence"] == contract
    assert obs["repository-presence"] == repo
    # 단일 행·정본 mode.
    assert result["matchedRow"] == row
    assert result["mode"] == mode
    # 게이트 = canonical policy.ref 단일 소스. result["gate"] 는 그 투영(별도 판정 아님).
    assert result["gate"] is gate
    assert (result["policy"]["ref"] == "user-confirmation-gate") is gate
    # 병행 imperative conflict 필드는 제거됨(Policy as Data 단일 소스).
    assert "conflict" not in result


def test_gate_is_intent_independent(reg, tmp_path):
    # 게이트는 주입 의도와 무관하게 canonical policy로만 결정된다(intent 는 provenance 에코).
    folder = make_folder(tmp_path, contract=True, repo=False)  # 행 7.
    for intent in ("new", "existing", None):
        result = resolve(reg, "/continue", folder, intent=intent)
        assert result["matchedRow"] == 7
        assert result["gate"] is False  # intent 가 바뀌어도 거짓 게이트 없음.


def test_registry_partition_integrity(reg):
    # verify_determinism 이 예외 없이 통과 = 전수·상호배타 분할 성립(01 §3.2-A 4단계).
    verify_determinism(reg)  # 예외 미발생이면 통과.
    # 8행 정확히 존재.
    assert len(reg["decisionRows"]) == 8
    rows = sorted(r["row"] for r in reg["decisionRows"])
    assert rows == list(range(1, 9))
    # 게이트 행 = 정확히 {2,3,4,5}(canonical).
    gate_rows = sorted(r["row"] for r in reg["decisionRows"]
                       if r["policy"].get("ref") == "user-confirmation-gate")
    assert gate_rows == [2, 3, 4, 5]


# --------------------------------------------------------------------------
# ① 신규 폴더(부재) + /new → 행 1 greenfield · 게이트 없음.
# --------------------------------------------------------------------------
def test_case1_new_absent_folder_row1(reg, tmp_path):
    folder = make_folder(tmp_path, contract=False, repo=False, exist=False)
    assert not folder.exists()  # 부재 확인.
    result = resolve(reg, "/new", folder, intent="new")
    assert result["matchedRow"] == 1
    assert result["mode"] == "greenfield"
    assert result["policy"]["ref"] == "default"
    assert result["gate"] is False
    assert not folder.exists()  # 엔진이 폴더를 생성하지 않음(EN-INV 1·순수 판독).


# --------------------------------------------------------------------------
# ② 기존 폴더 + contract 유 + /continue → 행 8 incremental · 게이트 없음.
# --------------------------------------------------------------------------
def test_case2_existing_contract_present_incremental(reg, tmp_path):
    folder = make_folder(tmp_path, contract=True, repo=True)  # contract 유·repo 유.
    result = resolve(reg, "/continue", folder, intent="existing")
    assert result["matchedRow"] in (7, 8)
    assert result["mode"] == "incremental"
    assert result["policy"]["ref"] == "default"
    assert result["gate"] is False


# --------------------------------------------------------------------------
# ③ 기존 폴더 + contract 무 + repo 유 + /continue → 행 6 brownfield · 게이트 없음.
# --------------------------------------------------------------------------
def test_case3_existing_no_contract_brownfield(reg, tmp_path):
    folder = make_folder(tmp_path, contract=False, repo=True)  # contract 무·repo 유.
    result = resolve(reg, "/continue", folder, intent="existing")
    assert result["matchedRow"] == 6
    assert result["mode"] == "brownfield"
    assert result["policy"]["ref"] == "default"
    assert result["gate"] is False


# --------------------------------------------------------------------------
# ④ 신규 선언인데 폴더에 콘텐츠 존재 → 행 2 · 게이트 (canonical policy로 구동·별도 conflict 아님).
# --------------------------------------------------------------------------
def test_case4_new_declared_but_content_gate(reg, tmp_path):
    folder = make_folder(tmp_path, contract=False, repo=True)  # repo 유(콘텐츠 존재).
    result = resolve(reg, "/new", folder, intent="new")
    assert result["matchedRow"] == 2  # /new + contract 무 + repo 유.
    assert result["gate"] is True
    # 게이트는 canonical 결정 테이블 policy로 구동(하이브리드 선언↔상태 충돌 포섭).
    assert result["policy"]["ref"] == "user-confirmation-gate"
    assert result["policy"]["conflict"] == "repository-present"
    assert result["provisional"] is True
    assert "conflict" not in result  # 병행 conflict 필드 없음.


def test_case4b_existing_declared_but_empty_gate(reg, tmp_path):
    # 대칭 케이스: 기존 선언인데 폴더 부재/빈 → 행 5 게이트(nothing-to-continue).
    folder = make_folder(tmp_path, contract=False, repo=False, exist=True)  # 빈 폴더.
    result = resolve(reg, "/continue", folder, intent="existing")
    assert result["matchedRow"] == 5
    assert result["gate"] is True
    assert result["policy"]["ref"] == "user-confirmation-gate"
    assert result["policy"]["conflict"] == "nothing-to-continue"
    assert "conflict" not in result


# --------------------------------------------------------------------------
# CP2 정정 회귀 — 행 7(/continue + contract 유 + repo 무) → incremental · 거짓 게이트 부재.
# --------------------------------------------------------------------------
def test_row7_contract_present_no_repo_no_false_gate(reg, tmp_path):
    # 구 compute_conflict(의도 existing↔repo 무)가 만들던 거짓 게이트가 제거되었음을 확증한다.
    # 정본 = incremental·policy default·게이트 없음(D3③ Contract 우선). dogfooding 초기 현실 상태.
    folder = make_folder(tmp_path, contract=True, repo=False)  # contract만·본체 무.
    result = resolve(reg, "/continue", folder, intent="existing")  # 기존 의도인데 repo 무.
    obs = {i["sourceType"]: i["observed"] for i in result["inputs"]}
    assert obs["contract-presence"] == PRESENT
    assert obs["repository-presence"] == ABSENT
    assert result["matchedRow"] == 7
    assert result["mode"] == "incremental"
    assert result["policy"]["ref"] == "default"  # 게이트 없음(정본).
    assert result["gate"] is False               # 거짓 게이트 부재(회귀 정정 확증).
    assert "conflict" not in result


# --------------------------------------------------------------------------
# 관측 직교성 — contract 유가 repository-presence 를 오염시키지 않음(본체에서 제외).
# --------------------------------------------------------------------------
def test_contract_storage_excluded_from_repo_body(reg, tmp_path):
    folder = make_folder(tmp_path, contract=True, repo=False)  # contract만·본체 무.
    result = resolve(reg, "/continue", folder, intent="existing")
    obs = {i["sourceType"]: i["observed"] for i in result["inputs"]}
    assert obs["contract-presence"] == PRESENT
    assert obs["repository-presence"] == ABSENT  # Contract 저장 위치는 본체에서 제외.


def test_git_init_only_is_absent(reg, tmp_path):
    # 맨 초기화(.git 만) → repository-presence 무.
    folder = tmp_path / "ws"
    (folder / ".git").mkdir(parents=True)
    (folder / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (folder / ".gitkeep").write_text("", encoding="utf-8")
    result = resolve(reg, "/new", folder, intent="new")
    obs = {i["sourceType"]: i["observed"] for i in result["inputs"]}
    assert obs["repository-presence"] == ABSENT
    assert result["matchedRow"] == 1


# --------------------------------------------------------------------------
# --entry 정규화 — new|continue(슬래시 없음) → /new·/continue (OQ-7·Git Bash MSYS 안전).
# --------------------------------------------------------------------------
def test_normalize_entry():
    assert normalize_entry("new") == "/new"
    assert normalize_entry("continue") == "/continue"
    assert normalize_entry("/new") == "/new"
    assert normalize_entry("/continue") == "/continue"
    assert normalize_entry(None) is None


def test_cli_entry_without_slash(tmp_path):
    # 슬래시 없는 --entry new 가 end-to-end 로 동작(정규화 → /new·행 1).
    folder = tmp_path / "empty"
    folder.mkdir()
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, str(entry_resolve.__file__), "--entry", "new", "--folder", str(folder)],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["entry"] == "/new"   # 정규화 확인.
    assert out["matchedRow"] == 1   # 빈 폴더 → 행 1.
    assert out["gate"] is False


# --------------------------------------------------------------------------
# 미등록 Entry — LookupError(§6 Failure Mode).
# --------------------------------------------------------------------------
def test_unknown_entry_raises(reg, tmp_path):
    with pytest.raises(LookupError):
        resolve(reg, "/import", tmp_path, intent=None)


# --------------------------------------------------------------------------
# 출력 스키마 — Discovery Request 3요소 + 엔진 메타(matchedRow·gate)·conflict 필드 제거 확증.
# --------------------------------------------------------------------------
def test_output_schema_shape(reg, tmp_path):
    folder = make_folder(tmp_path, contract=False, repo=False, exist=False)
    result = resolve(reg, "/new", folder, intent="new")
    # Discovery Request 3요소(§5.1).
    assert set(["mode", "inputs", "policy"]).issubset(result.keys())
    # 엔진 메타.
    assert "matchedRow" in result and "gate" in result
    assert "conflict" not in result  # 병행 conflict 필드 제거(Policy as Data 단일 소스).
    # inputs = Evidence 참조 목록(2종·유/무).
    assert [i["sourceType"] for i in result["inputs"]] == ["contract-presence", "repository-presence"]
    # JSON 직렬화 가능(방출 형식).
    json.dumps(result, ensure_ascii=False)
