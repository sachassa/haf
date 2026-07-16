"""T3 W1 — 얇은 결정적 검증 러너 (LLM 0·순수 판독·원장 무수정).

사용법:
  python verify_run.py <run-dir> [<run-dir> ...] [--replay] [--git-hygiene] [-o <출력 디렉터리>]

무엇을 하는가:
  run 데이터 백엔드(events.jsonl·revisions.jsonl·artifacts.jsonl·graph.json)와 (있으면) 산출
  plan artifact 를 **순수 판독**으로 검사해 결정적 검증 리포트 JSON 을 낸다. LLM 을 전혀 호출하지
  않으며(러너 소관 = 결정적 축), Verifier(LLM)는 의미 축을 전담한다(T3 분리 원칙). 기존 중립
  검증기·순수 함수를 **조립 없이 재사용**한다(collect_metrics.py 선례 — orchestrator 조립이
  수반하는 workspace makedirs 를 회피해 consumer/SD 데이터 무접촉).

검사 축(전부 순수 판독·run 파일 mtime 불변):
  (a) 원장 위생   — cycle별 seq 단조·전역 at 단조·ref.kind 관측 어휘·outcome 어휘·게이트 순서
                    (required→provenance→resolved)·simulated 라벨 정직성 스캔. [신규 최소·stdlib]
  (b) revision 무결 — 중립 revision.validate_revision/fold 재사용(조립 없이 progressive fold).
  (c) plan 스키마 — stage-plan/impl-plan artifact 실재 시 validate_stage_plan/validate_impl_plan.
  (d) delegation 정합 — delegation_check(참조형 sentinel 또는 상위 원문 전재·W4 공유 함수).
  (e) 계수 정합   — artifacts.derive_registry 대조(선언 수·artifact 수·record 수 정합).
  (f) [--replay]  — k 계열 run 만 replay 결정성(replay_k 2회 stdout 동일·workspace 안전 확인 후).
  (g) [--git-hygiene] — git porcelain 클린 검사(저장소 무변경 확인).

원칙(불변):
  - 순수 판독. 기본 검사(a~e)는 run 디렉터리·원장·workspace 를 **일절 수정하지 않는다**
    (파일 추가·mtime 변경 0). orchestrator 를 조립하지 않는다(workspace makedirs 회피).
  - 출력은 run 디렉터리 **밖**(기본 e2e/metrics/verify/)에만 쓴다.
  - python 3 stdlib + 중립/e2e 순수 함수만(외부 패키지 0).
  - 실 검출은 숨기지 않는다(O5) — 리포트에 findings 로 그대로 남긴다.

이 스크립트는 orchestration-data/e2e/ 경계 소속이다(비프로덕션 검증 러너).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

# --- 경로 배선: 중립 코드(revision·artifacts)를 조립 없이 순수 함수로 import ----------
HERE = Path(__file__).resolve().parent                       # .../orchestration-data/e2e
CLAUDE_DIR = HERE.parents[1]                                 # .../framework/adapters/claude
STEP_HOST_DIR = CLAUDE_DIR.parents[1] / "loop" / "step-host"
REPO_ROOT = CLAUDE_DIR.parents[3]                            # repo root
ORCH_DIR = REPO_ROOT / "orchestration" / "framework" / "orchestrator"
for _p in (str(ORCH_DIR), str(STEP_HOST_DIR), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from revision import RevisionEvent, fold, validate_revision  # noqa: E402  (중립·순수)
from artifacts import derive_registry  # noqa: E402  (중립·순수)
from delegation_check import delegation_errors_for_task  # noqa: E402  (W4 공유)


# ==========================================================================
# 관측 어휘 화이트리스트 — 코드 소유 어휘에서 도출(host.py·gates.py·allocation.py·드라이버)
# ==========================================================================
# ref.kind 어휘. 출처를 주석에 밝힌다(단일 좁은 스캔이 아니라 코드 전수 도출·완전성 규율).
OBSERVED_REF_KINDS = frozenset({
    # host.py (step-host) — 디스패치·CP2·진입 판정·차단·재시도 피드백.
    "dispatch", "cp2-pass", "scoped-query", "blocked",
    "retry-limit-exceeded", "interrupted", "failure", "rework", "unknown-result",
    # gates.py (orchestrator) — 게이트 요구/해소/리뷰/승인 마커.
    "gate-required", "gate-resolved", "gate-review", "gate-approval",
    # allocation.py — 명시적 모델 정책 이벤트(재선택 트리거).
    "model-policy-event",
    # 드라이버(resolve_m/w·resolve_and_revise) — 사용자 해소 provenance·시뮬레이션 라벨.
    "user-resolution-provenance", "simulation-annotation",
})

VALID_OUTCOMES = frozenset({"pass", "fail", "escalated"})

# 정지 게이트(required→resolved 쌍 순서 검사 대상).
STOPPING_GATE_KINDS = frozenset({"escalation_required", "user_decision_required"})


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_jsonl(path: Path) -> list:
    rows: list = []
    if not path.exists():
        return rows
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if raw:
                rows.append(json.loads(raw))
    return rows


def _result(check: str, status: str, detail: Any = None, findings: list | None = None) -> dict:
    return {"check": check, "status": status, "detail": detail, "findings": findings or []}


# ==========================================================================
# (a) 원장 위생 — events.jsonl (신규 최소·stdlib·순수 판독)
# ==========================================================================
def check_ledger_hygiene(run_dir: Path) -> dict:
    ev_path = run_dir / "events.jsonl"
    events = load_jsonl(ev_path)
    if not events:
        return _result("ledger_hygiene", "skip", "events.jsonl 부재·비어 있음")

    findings: list = []

    # 전역 at 단조 — 1..M 연속·엄격 증가(EventLog at = len(existing)+1).
    ats = [e.get("at") for e in events]
    expected_at = list(range(1, len(events) + 1))
    if ats != expected_at:
        # 정확 위반 지점만 열거(최대 5건).
        for i, (got, exp) in enumerate(zip(ats, expected_at)):
            if got != exp:
                findings.append("전역 at 비연속/비단조: index %d at=%r (기대 %d)" % (i, got, exp))
                if len([f for f in findings if "at" in f]) >= 5:
                    break

    # cycle별 seq 단조 — 각 cycle_id 의 seq 가 파일(=at) 순서로 1..k 연속.
    seq_by_cycle: dict = {}
    for e in events:
        seq_by_cycle.setdefault(e.get("cycle_id"), []).append(e.get("seq"))
    for cid, seqs in seq_by_cycle.items():
        if seqs != list(range(1, len(seqs) + 1)):
            findings.append("cycle=%r seq 비연속/비단조: %r (기대 1..%d)" % (cid, seqs, len(seqs)))

    # ref.kind 관측 어휘 + outcome 어휘.
    refs_without_kind: list = []
    for e in events:
        outcome = e.get("outcome")
        if outcome not in VALID_OUTCOMES:
            findings.append("cycle=%r at=%r outcome 어휘 위반: %r" % (e.get("cycle_id"), e.get("at"), outcome))
        ref = e.get("ref")
        if isinstance(ref, dict):
            kind = ref.get("kind")
            if kind is None:
                refs_without_kind.append(e.get("at"))
            elif kind not in OBSERVED_REF_KINDS:
                findings.append("cycle=%r at=%r ref.kind 관측 어휘 밖: %r" % (e.get("cycle_id"), e.get("at"), kind))

    # 게이트 순서(required→[provenance]→resolved) — gate-resolved 실재 gate_id 마다.
    gate_order = _check_gate_order(events)
    findings.extend(gate_order)

    # simulated 라벨 정직성 스캔 — human actor 인데 simulated=true 라벨이면 모순(정직성 위반).
    sim_true = 0
    sim_false = 0
    sim_annotations = 0
    for e in events:
        ref = e.get("ref") if isinstance(e.get("ref"), dict) else {}
        if ref.get("kind") == "simulation-annotation":
            sim_annotations += 1
        simulated = ref.get("simulated")
        if simulated is True:
            sim_true += 1
            if e.get("actor") == "human":
                findings.append("정직성 모순: actor=human 인데 ref.simulated=true (cycle=%r at=%r)"
                                % (e.get("cycle_id"), e.get("at")))
        elif simulated is False:
            sim_false += 1

    detail = {
        "event_count": len(events),
        "cycles": len(seq_by_cycle),
        "refs_without_kind_at": refs_without_kind,
        "simulated_true": sim_true,
        "simulated_false": sim_false,
        "simulation_annotations": sim_annotations,
    }
    status = "fail" if findings else "pass"
    return _result("ledger_hygiene", status, detail, findings)


def _check_gate_order(events: list) -> list:
    """정지 게이트마다 required→[provenance]→resolved 시간(at) 순서 검사."""
    findings: list = []
    # gate_id -> {required_at, resolved_at, resolved_kind, provenance_at}
    gates: dict = {}
    for e in events:
        ref = e.get("ref") if isinstance(e.get("ref"), dict) else {}
        kind = ref.get("kind")
        gid = ref.get("gate_id")
        at = e.get("at")
        if gid is None:
            continue
        g = gates.setdefault(gid, {})
        if kind == "gate-required":
            g.setdefault("required_at", at)
            g["gateKind"] = ref.get("gateKind")
        elif kind == "gate-resolved":
            g["resolved_at"] = at
            g["resolved_gateKind"] = ref.get("gateKind")
        elif kind == "user-resolution-provenance":
            g["provenance_at"] = at
    for gid, g in gates.items():
        res_at = g.get("resolved_at")
        req_at = g.get("required_at")
        if res_at is None:
            continue  # 해소 이벤트 없는 게이트(리뷰/승인 마커 등)는 순서 쌍 검사 대상 아님.
        if req_at is None:
            findings.append("게이트 %r 에 gate-resolved(at=%r) 는 있으나 선행 gate-required 부재(무근거 해소)" % (gid, res_at))
            continue
        if not (req_at < res_at):
            findings.append("게이트 %r 순서 위반: required at=%r 가 resolved at=%r 보다 앞서지 않음" % (gid, req_at, res_at))
        prov_at = g.get("provenance_at")
        if prov_at is not None and not (req_at <= prov_at <= res_at):
            findings.append("게이트 %r provenance 순서 위반: required=%r provenance=%r resolved=%r"
                            % (gid, req_at, prov_at, res_at))
    return findings


# ==========================================================================
# (b) revision 무결 — 중립 validate_revision/fold 재사용(조립 없이·progressive)
# ==========================================================================
def check_revision_integrity(run_dir: Path) -> dict:
    rev_rows = load_jsonl(run_dir / "revisions.jsonl")
    if not rev_rows:
        return _result("revision_integrity", "skip", "revisions.jsonl 부재·비어 있음")
    graph_path = run_dir / "graph.json"
    if not graph_path.exists():
        return _result("revision_integrity", "skip", "graph.json 부재")
    initial_graph = load_json(graph_path)

    revs = [RevisionEvent.from_dict(r) for r in rev_rows]
    findings: list = []

    # revisionSeq 전순서(단조 1..N).
    seqs = [r.revisionSeq for r in revs]
    if seqs != list(range(1, len(revs) + 1)):
        findings.append("revisionSeq 비연속/비단조: %r (기대 1..%d)" % (seqs, len(revs)))

    # progressive validate — 각 revision 을 적용 직전 그래프에 대해 구조 검증(순수·조립 0).
    for i, rev in enumerate(revs):
        graph = fold(revs[:i], initial_graph)
        try:
            reason = validate_revision(rev, graph)
        except ValueError as exc:  # 구조 misuse(중복 id·미존재 supersede 대상 등).
            findings.append("revisionSeq=%s (%s) 구조 misuse: %s" % (rev.revisionSeq, rev.kind, exc))
            continue
        if reason is not None:
            findings.append("revisionSeq=%s (%s) 구조 검증 실패: %s" % (rev.revisionSeq, rev.kind, reason))

    # 최종 fold task 수(참고 지표).
    final = fold(revs, initial_graph)
    detail = {
        "revision_count": len(revs),
        "kinds": sorted({r.kind for r in revs}),
        "final_task_count": len(final.get("tasks") or []),
    }
    status = "fail" if findings else "pass"
    return _result("revision_integrity", status, detail, findings)


# ==========================================================================
# (c) plan 스키마 — stage-plan/impl-plan artifact 실재 시 중립 검증기 호출
# ==========================================================================
def check_plan_schema(run_dir: Path, cfg: dict) -> dict:
    workspace = cfg.get("workspace_dir") or str(run_dir / "workspace")
    ws = Path(workspace)
    stage_plan = ws / "stage-plan.json"
    impl_plan = ws / "impl-plan.json"

    if stage_plan.exists():
        from resolve_m import validate_stage_plan  # 지연 import(의존 체인 국소화).
        plan = load_json(stage_plan)
        errors = validate_stage_plan(plan)
        detail = {"plan": "stage-plan.json", "path": str(stage_plan), "error_count": len(errors)}
        return _result("plan_schema", "fail" if errors else "pass", detail, list(errors))

    if impl_plan.exists():
        from resolve_w import validate_impl_plan
        plan = load_json(impl_plan)
        errors = validate_impl_plan(plan)
        detail = {"plan": "impl-plan.json", "path": str(impl_plan), "error_count": len(errors)}
        return _result("plan_schema", "fail" if errors else "pass", detail, list(errors))

    return _result("plan_schema", "skip", "stage-plan.json·impl-plan.json 부재(plan 산출 run 아님)")


# ==========================================================================
# (d) delegation 정합 — graph.json tasks + task_added revision payloads (W4 공유 함수)
# ==========================================================================
def check_delegation(run_dir: Path) -> dict:
    graph_path = run_dir / "graph.json"
    if not graph_path.exists():
        return _result("delegation", "skip", "graph.json 부재")
    findings: list = []
    checked = 0

    graph = load_json(graph_path)
    for i, t in enumerate(graph.get("tasks") or []):
        checked += 1
        findings.extend(delegation_errors_for_task(t, where="graph.tasks[%d](id=%s)" % (i, t.get("id"))))

    for r in load_jsonl(run_dir / "revisions.jsonl"):
        kind = str(r.get("kind") or "")
        if "task_added" in kind or "task_superseded" in kind:
            payload = r.get("payload") or {}
            checked += 1
            findings.extend(delegation_errors_for_task(
                payload, where="revision seq=%s(id=%s)" % (r.get("revisionSeq"), payload.get("id"))))

    detail = {"tasks_checked": checked}
    status = "fail" if findings else "pass"
    return _result("delegation", status, detail, findings)


# ==========================================================================
# (e) 계수 정합 — artifacts.derive_registry 대조(순수·조립 없이)
# ==========================================================================
def check_artifact_counts(run_dir: Path) -> dict:
    declarations = load_jsonl(run_dir / "artifacts.jsonl")
    if not declarations:
        return _result("artifact_counts", "skip", "artifacts.jsonl 부재·비어 있음")
    events = load_jsonl(run_dir / "events.jsonl")
    findings: list = []

    # 선언 무결(artifactId 실재).
    missing_id = [i for i, d in enumerate(declarations) if not d.get("artifactId")]
    if missing_id:
        findings.append("artifactId 없는 선언 index: %r" % missing_id)

    try:
        registry = derive_registry(declarations, events)
    except Exception as exc:  # noqa: BLE001  (정직 표면화)
        findings.append("derive_registry 실패: %s: %s" % (type(exc).__name__, exc))
        return _result("artifact_counts", "fail", {"declaration_count": len(declarations)}, findings)

    record_count = sum(len(v) for v in registry.values())
    # (artifactId, version) 고유 조합 수 == record 수여야 한다(같은 버전 재선언은 병합됨).
    distinct_av = len({(d.get("artifactId"), int(d.get("version", 1))) for d in declarations})
    if record_count != distinct_av:
        findings.append("record 수(%d) != 고유 (artifactId,version) 수(%d)" % (record_count, distinct_av))

    detail = {
        "declaration_count": len(declarations),
        "artifact_count": len(registry),
        "record_count": record_count,
        "distinct_id_version": distinct_av,
        "approval_states": sorted({r.approvalState for recs in registry.values() for r in recs}),
    }
    status = "fail" if findings else "pass"
    return _result("artifact_counts", status, detail, findings)


# ==========================================================================
# (f) [--replay] k 계열 replay 결정성 (workspace 안전 확인 후·opt-in)
# ==========================================================================
def check_replay_determinism(run_dir: Path, cfg: dict) -> dict:
    run_id = cfg.get("run_id") or run_dir.name
    # k 계열만(replay_k 는 build_orchestrator_k 로 workspace makedirs 를 수반 — m/w 는 SD/
    # consumer 접근 금지 대상이라 제외한다). k 는 temp scratchpad workspace 라 안전.
    if "orch-k" not in str(run_id):
        return _result("replay_determinism", "skip",
                       "k 계열 run 아님(%s) — replay 는 k 계열만(workspace 안전 경계)" % run_id)
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    outs = []
    for _ in range(2):
        proc = subprocess.run(
            [sys.executable, str(HERE / "replay_k.py"), str(run_dir)],
            capture_output=True, text=True, cwd=str(HERE), env=env, encoding="utf-8",
        )
        outs.append((proc.returncode, proc.stdout))
    findings: list = []
    if outs[0][0] != 0 or outs[1][0] != 0:
        findings.append("replay_k 종료 코드 비0: %r" % [o[0] for o in outs])
    if outs[0][1] != outs[1][1]:
        findings.append("replay_k 2회 stdout 불일치(결정성 위반)")
    detail = {"run_id": run_id, "identical": outs[0][1] == outs[1][1] and outs[0][0] == 0}
    status = "fail" if findings else "pass"
    return _result("replay_determinism", status, detail, findings)


# ==========================================================================
# (g) [--git-hygiene] git porcelain 클린 (opt-in)
# ==========================================================================
def check_git_hygiene() -> dict:
    try:
        proc = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except Exception as exc:  # noqa: BLE001
        return _result("git_hygiene", "skip", "git 조회 실패: %s" % exc)
    changed = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
    detail = {"changed_count": len(changed), "changed": changed[:50]}
    status = "pass" if not changed else "fail"
    findings = [] if not changed else ["작업 트리 비클린(%d 항목) — run 이 예상 밖 변경을 남겼는지 확인" % len(changed)]
    return _result("git_hygiene", status, detail, findings)


# ==========================================================================
# run 단위 집계
# ==========================================================================
def collect_run(run_dir: Path, *, do_replay: bool) -> dict:
    run_dir = run_dir.resolve()
    cfg_path = run_dir / "config.json"
    cfg = load_json(cfg_path) if cfg_path.exists() else {}

    checks = [
        check_ledger_hygiene(run_dir),
        check_revision_integrity(run_dir),
        check_plan_schema(run_dir, cfg),
        check_delegation(run_dir),
        check_artifact_counts(run_dir),
    ]
    if do_replay:
        checks.append(check_replay_determinism(run_dir, cfg))

    statuses = [c["status"] for c in checks]
    run_status = "fail" if "fail" in statuses else "pass"
    return {
        "run_id": cfg.get("run_id") or run_dir.name,
        "run_dir": str(run_dir),
        "status": run_status,
        "summary": {
            "pass": statuses.count("pass"),
            "fail": statuses.count("fail"),
            "skip": statuses.count("skip"),
        },
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="T3 W1 얇은 결정적 검증 러너(LLM 0·순수 판독·원장 무수정)")
    parser.add_argument("run_dirs", nargs="+", help="run 데이터 백엔드 디렉터리(1개 이상)")
    parser.add_argument("--replay", action="store_true",
                        help="k 계열 run replay 결정성 검사(replay_k 2회 stdout 동일·opt-in)")
    parser.add_argument("--git-hygiene", action="store_true",
                        help="git porcelain 클린 검사(저장소 무변경 확인·opt-in)")
    parser.add_argument("-o", "--out", default=None,
                        help="출력 디렉터리(기본 = 이 스크립트 옆 metrics/verify/)")
    args = parser.parse_args()

    outdir = Path(args.out).resolve() if args.out else (HERE / "metrics" / "verify")
    outdir.mkdir(parents=True, exist_ok=True)

    run_reports = []
    overall_fail = False
    for rd in args.run_dirs:
        rep = collect_run(Path(rd), do_replay=args.replay)
        run_reports.append(rep)
        out_path = outdir / ("%s.verify.json" % rep["run_id"])
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=2, sort_keys=True)
        s = rep["summary"]
        print("[VERIFY] %s -> %s  status=%s (pass=%d fail=%d skip=%d)"
              % (rep["run_id"], out_path.name, rep["status"], s["pass"], s["fail"], s["skip"]))
        for c in rep["checks"]:
            mark = {"pass": "OK ", "fail": "XX ", "skip": ".. "}[c["status"]]
            print("    %s%-20s %s" % (mark, c["check"], "" if c["status"] != "fail" else c["findings"]))
        if rep["status"] == "fail":
            overall_fail = True

    if args.git_hygiene:
        gh = check_git_hygiene()
        gh_path = outdir / "git-hygiene.verify.json"
        with open(gh_path, "w", encoding="utf-8") as fh:
            json.dump(gh, fh, ensure_ascii=False, indent=2, sort_keys=True)
        print("[GIT-HYGIENE] status=%s changed=%d" % (gh["status"], gh["detail"]["changed_count"]))
        if gh["status"] == "fail":
            overall_fail = True

    print("[OVERALL] %s (%d run)" % ("FAIL" if overall_fail else "PASS", len(run_reports)))
    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main())
