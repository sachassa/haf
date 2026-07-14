"""T1 Minimal Telemetry — Baseline run 집계 스크립트 (순수 판독·원장 무수정).

사용법:
  python collect_metrics.py <run-dir> [<run-dir> ...]
                            [--git-anchor <시작커밋> <끝커밋>]
                            [-o <출력 디렉터리>]

무엇을 하는가:
  v1.7 Dogfooding E2E 의 invoke 로그·파일 mtime·(선택) git 타임스탬프에서
  `docs/baseline-performance-cost-analysis.md` §15 지표 전부를 재산출한다. 1차 분석이
  수동 스크립트였던 것을 **고정 산식**으로 대체해 Before/After 비교의 재현성을 확보한다.

원칙(불변):
  - 순수 판독. run 디렉터리(원장·로그)를 **일절 수정하지 않는다**(파일 추가·mtime 변경 0).
  - 출력은 run 디렉터리 **밖**(기본 e2e/metrics/)에만 쓴다.
  - 벽시계 값(mtime·git ts)은 **metrics 출력 파일에만** 담는다 — 원장/run 파일에 쓰지 않는다
    (L-09: 순서 값 전속, 벽시계는 별도).
  - python 3 stdlib 만 사용(외부 패키지 0).
  - 산출 불가·소실 항목은 값을 추정·날조하지 않고 등급으로 표기한다.

등급 체계(1차 분석 §Baseline Facts 와 동일):
  확인 = 원시 로그 직접 합산 · 계산 = 실측치 합산/도출(파생 — mtime·git ts 파생 포함,
  1차 §2 "계산(mtime·커밋)" 동형) · 근사 = 관측 기반 추정(정밀 앵커 부재) ·
  불가 = 측정 수단 부재 · 소실 = 계측은 가능했으나 덮어쓰기 등으로 소실.

세션 분류 판별식(1차 §7·events gate-review 대응으로 확정):
  role==Worker                        → Worker step
  role==Verifier & gate_id 없음(null) → CP2 (독립 판정)
  role==Verifier & gate_id 있음       → 게이트 재검증 (gate-review)

ready_set 동시성(그래프 성장 인지):
  동적 추가 task(task_added revision)는 그 proposing step 이 완료·게이트 해소된 뒤에야
  그래프에 편입되므로, 추가 task 의 실질 선행 = 선언 dependsOn ∪ {proposingStepRef}.
  이 증강 후 최대 동시 ready 폭(wave 폭)을 산출한다 — m 의 propose 쌍 = 2, k·w = 1.

이 스크립트는 orchestration-data/e2e/ 경계 소속이다(비프로덕션 텔레메트리 도구).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# --- 등급 상수 -----------------------------------------------------------------
G_CONFIRMED = "확인"     # 원시 로그 직접 합산
G_COMPUTED = "계산"      # 파생/도출(mtime·git ts 파생 포함)
G_APPROX = "근사"        # 관측 추정(정밀 앵커 부재)
G_IMPOSSIBLE = "불가"    # 측정 수단 부재
G_LOST = "소실"          # 계측 가능했으나 소실

USER_DECISION = "user_decision_required"


def load_json(path: Path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _iso(ts: float) -> str:
    """UNIX ts → 로컬 ISO 문자열(사람 판독용·metrics 출력 전용)."""
    return datetime.fromtimestamp(ts).isoformat()


# --- invoke 로그 파싱 ----------------------------------------------------------
def parse_invoke_log(path: Path) -> dict:
    """단일 invoke-*.json 에서 계측 필드를 추출한다(raw_stdout 안의 중첩 JSON 포함)."""
    d = load_json(path)
    rec = {
        "file": path.name,
        "invoke_seq": d.get("invoke_seq"),
        "role": d.get("role"),
        "step_id": d.get("step_id"),
        "gate_id": d.get("gate_id"),
        "model_alias": d.get("model"),
        "returncode": d.get("returncode"),
        "feedback_present": bool(d.get("feedback_present")),
        "session_id": d.get("session_id"),
        "duration_ms": 0,
        "cost_usd": 0.0,
        "output_tokens": 0,
        "input_tokens": 0,
        "cache_read": 0,
        "cache_write": 0,
        "model_usage": {},
        "parse_error": None,
    }
    raw = d.get("raw_stdout") or ""
    try:
        rj = json.loads(raw)
    except Exception as exc:  # noqa: BLE001  (정직 표면화 — 값 날조 금지)
        rec["parse_error"] = "raw_stdout JSON 파싱 실패: %s" % (exc,)
        return rec
    rec["duration_ms"] = rj.get("duration_ms", 0) or 0
    rec["cost_usd"] = rj.get("total_cost_usd", 0.0) or 0.0
    u = rj.get("usage", {}) or {}
    rec["output_tokens"] = u.get("output_tokens", 0) or 0
    rec["input_tokens"] = u.get("input_tokens", 0) or 0
    rec["cache_read"] = u.get("cache_read_input_tokens", 0) or 0
    rec["cache_write"] = u.get("cache_creation_input_tokens", 0) or 0
    for mn, mv in (rj.get("modelUsage", {}) or {}).items():
        rec["model_usage"][mn] = {
            "input_tokens": mv.get("inputTokens", 0) or 0,
            "output_tokens": mv.get("outputTokens", 0) or 0,
            "cache_read": mv.get("cacheReadInputTokens", 0) or 0,
            "cache_write": mv.get("cacheCreationInputTokens", 0) or 0,
            "cost_usd": mv.get("costUSD", 0.0) or 0.0,
        }
    return rec


def classify(role, gate_id) -> str:
    if role == "Worker":
        return "Worker step"
    if gate_id:
        return "gate re-verification"
    return "CP2"


# --- 그래프 fold(task_added) + ready_set 동시성 --------------------------------
def fold_graph(run_dir: Path) -> dict:
    """graph.json(초기) + revisions.jsonl(task_added)을 순수 판독으로 fold 한다.

    build_orchestrator_k 를 쓰지 않는 이유: 그 함수는 config.workspace_dir 에
    os.makedirs 를 호출한다 — w run 의 workspace = 접근 금지 대상(control-plane),
    m run 의 workspace = 무수정 대상(maturation-r003). 따라서 run 디렉터리 파일만으로
    직접 fold 한다(task_added append 의미론만 적용 — 그 외 kind 는 unsupported 로 표면화).
    결과 task 집합·dependsOn 검증: k 는 replay(active_graph) 실측 대조, m·w 는 분석적
    동치 확인(m 의 task_superseded 는 동일 id·동일 deps 재발행이라 결과 불변)이다 —
    m·w 는 실행 대조가 아니다(orchestrator 조립이 workspace makedirs 를 수반해 회피).
    """
    initial = load_json(run_dir / "graph.json")
    tasks = {}      # id -> {dependsOn, proposingStepRef(추가분만), source}
    for t in initial.get("tasks", []) or []:
        tid = t.get("id")
        if tid is not None:
            tasks[tid] = {
                "dependsOn": list(t.get("dependsOn") or []),
                "proposingStepRef": None,
                "source": "initial",
            }
    unsupported = []
    rev_path = run_dir / "revisions.jsonl"
    if rev_path.exists():
        for line in rev_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            kind = str(r.get("kind") or r.get("revisionKind") or "")
            payload = r.get("payload") or {}
            basis = r.get("basis") or {}
            if "task_added" in kind:
                tid = payload.get("id")
                if tid is not None:
                    tasks[tid] = {
                        "dependsOn": list(payload.get("dependsOn") or []),
                        "proposingStepRef": basis.get("proposingStepRef"),
                        "source": "added",
                    }
            else:
                # task_added 외 kind 는 fold 미적용·unsupported 로 표면화한다
                # (예: m run 의 task_superseded[seq5] — 동일 id·동일 deps 자기 재발행이라
                #  태스크 집합·dependsOn 결과에는 무영향).
                unsupported.append({"kind": kind, "revisionSeq": r.get("revisionSeq")})
    return {"tasks": tasks, "unsupported_revisions": unsupported}


def ready_concurrency(run_dir: Path) -> dict:
    """그래프 성장 인지 최대 동시 ready 폭을 산출한다(deterministic wave)."""
    folded = fold_graph(run_dir)
    tasks = folded["tasks"]
    # 실질 선행 = 선언 dependsOn ∪ {proposingStepRef}(추가 task 는 proposing step 완료 후 편입).
    eff = {}
    for tid, meta in tasks.items():
        deps = set(meta["dependsOn"])
        psr = meta.get("proposingStepRef")
        if psr and psr in tasks:
            deps.add(psr)
        eff[tid] = deps
    done = set()
    remaining = set(tasks.keys())
    max_ready = 0
    waves = []
    guard = 0
    while remaining and guard < 10000:
        guard += 1
        ready = sorted(i for i in remaining if eff[i] <= done)
        if not ready:
            break  # 사이클/미해결 외부 참조 — 정직 중단.
        waves.append(ready)
        max_ready = max(max_ready, len(ready))
        done |= set(ready)
        remaining -= set(ready)
    return {
        "value": max_ready,
        "grade": G_COMPUTED,
        "waves": waves,
        "unreached_tasks": sorted(remaining),
        "unsupported_revisions": folded["unsupported_revisions"],
        "note": "그래프 성장 인지 최대 동시 ready 폭 — 추가 task 실질선행 = dependsOn ∪ "
                "{proposingStepRef}. 물리 동시 디스패치는 미실행(직렬 소비)이므로 이는 "
                "'동시 실행 가능했던' 기회 폭이다.",
    }


# --- 게이트 대기(mtime·gate_id 내용 매칭·naming-agnostic) -----------------------
def gate_waits(run_dir: Path) -> dict:
    """stop-signal(라이브+아카이브) mtime ↔ gate-resolution-record mtime 차로 대기 산출.

    매칭은 파일명 규약이 아니라 **파일 내용의 gate_id** 로 한다(드라이버 아카이브 명명에
    비종속). 라이브 stop-signal.json 은 다중 게이트 run 에서 마지막 게이트로 덮어써지므로,
    선행 게이트는 아카이브(stop-signal-*.json)가 있어야 대기 산출 가능 — 없으면 '소실'.
    """
    logs = run_dir / "logs"
    # (gate_id -> (mtime, filename, kind)); 아카이브를 라이브보다 우선.
    stop_by_gate = {}
    sources = []
    live = logs / "stop-signal.json"
    if live.exists():
        sources.append((live, "live"))
    for p in sorted(logs.glob("stop-signal-*.json")):
        sources.append((p, "archive"))
    for p, kind in sources:
        try:
            data = load_json(p)
        except Exception:  # noqa: BLE001
            continue
        mt = os.stat(p).st_mtime
        for g in (data.get("pending_gates") or []):
            if g.get("gateKind") == USER_DECISION:
                gid = g.get("gate_id")
                cur = stop_by_gate.get(gid)
                if cur is None or (kind == "archive" and cur[2] != "archive"):
                    stop_by_gate[gid] = (mt, p.name, kind)

    results = []
    for p in sorted(logs.glob("gate-resolution-record*.json")):
        try:
            rec = load_json(p)
        except Exception:  # noqa: BLE001
            continue
        gid = rec.get("gate_id")
        phase = rec.get("phase")
        res_mt = os.stat(p).st_mtime
        st = stop_by_gate.get(gid)
        if st is None:
            results.append({
                "gate_id": gid,
                "phase": phase,
                "grade": G_LOST,
                "wait_seconds": None,
                "resolution_file": p.name,
                "reason": "stop-signal 이 후속 게이트로 덮어써졌고 위상 아카이브가 없어 "
                          "정지 시각 소실 — 추정하지 않는다(값 없음).",
            })
        else:
            stop_mt, stop_file, kind = st
            wait = res_mt - stop_mt
            results.append({
                "gate_id": gid,
                "phase": phase,
                "grade": G_COMPUTED,
                "wait_seconds": round(wait, 3),
                "wait_minutes": round(wait / 60.0, 2),
                "stop_signal_file": stop_file,
                "stop_signal_source": kind,
                "stop_mtime_iso": _iso(stop_mt),
                "resolution_file": p.name,
                "resolution_mtime_iso": _iso(res_mt),
                "note": "wait = resolution mtime - stop-signal mtime (벽시계·mtime 기반). "
                        "metrics 출력 전용(원장 무기재).",
            })
    computable = [r for r in results if r["grade"] == G_COMPUTED]
    lost = [r for r in results if r["grade"] == G_LOST]
    return {
        "gates": results,
        "computable_count": len(computable),
        "lost_count": len(lost),
        "total_wait_seconds": round(sum(r["wait_seconds"] for r in computable), 3),
    }


# --- run 단위 집계 -------------------------------------------------------------
def collect_run(run_dir: Path) -> dict:
    run_dir = run_dir.resolve()
    run_id = run_dir.name
    logs = run_dir / "logs"
    if not logs.exists():
        raise SystemExit("[ERR] logs 디렉터리 부재: %s" % logs)

    invokes = [parse_invoke_log(p) for p in sorted(logs.glob("invoke-*.json"))]
    parse_errors = [r["file"] for r in invokes if r["parse_error"]]

    # 분류.
    by_class = {"Worker step": [], "CP2": [], "gate re-verification": []}
    for r in invokes:
        by_class[classify(r["role"], r["gate_id"])].append(r)

    def _sum(rows, key):
        return sum(r[key] for r in rows)

    # 세션 수.
    session_ids = [r["session_id"] for r in invokes if r["session_id"]]
    fresh_unique = len(set(session_ids))
    sessions = {
        "total": {"value": len(invokes), "grade": G_CONFIRMED},
        "by_role": {
            "Worker": sum(1 for r in invokes if r["role"] == "Worker"),
            "Verifier": sum(1 for r in invokes if r["role"] == "Verifier"),
        },
        "by_class": {k: len(v) for k, v in by_class.items()},
        "by_model_alias": {},
        "fresh": {
            "value": fresh_unique,
            "grade": G_CONFIRMED,
            "note": "각 invoke = 독립 headless CLI 세션(고유 session_id). "
                    "고유 session_id 수 == 총 세션 수 이면 전부 fresh-context.",
        },
        "fresh_equals_total": fresh_unique == len(invokes),
    }
    for r in invokes:
        a = r["model_alias"]
        sessions["by_model_alias"][a] = sessions["by_model_alias"].get(a, 0) + 1

    # 시간(duration_ms).
    duration = {
        "total_ms": {"value": _sum(invokes, "duration_ms"), "grade": G_CONFIRMED},
        "total_seconds": {"value": round(_sum(invokes, "duration_ms") / 1000.0, 1),
                          "grade": G_CONFIRMED},
        "by_class_seconds": {k: round(_sum(v, "duration_ms") / 1000.0, 1)
                             for k, v in by_class.items()},
        "by_class_grade": G_CONFIRMED,
    }

    # 비용.
    cost = {
        "total_usd": {"value": round(_sum(invokes, "cost_usd"), 4), "grade": G_CONFIRMED},
        "by_class_usd": {k: round(_sum(v, "cost_usd"), 4) for k, v in by_class.items()},
        "by_model_alias_usd": {},
        "by_model_alias_grade": G_CONFIRMED,
    }
    for r in invokes:
        a = r["model_alias"]
        cost["by_model_alias_usd"][a] = round(
            cost["by_model_alias_usd"].get(a, 0.0) + r["cost_usd"], 4)

    # 토큰(top-level usage 합).
    tokens = {
        "output": {"value": _sum(invokes, "output_tokens"), "grade": G_CONFIRMED},
        "input_noncache": {"value": _sum(invokes, "input_tokens"), "grade": G_CONFIRMED},
        "cache_read": {"value": _sum(invokes, "cache_read"), "grade": G_CONFIRMED},
        "cache_write": {"value": _sum(invokes, "cache_write"), "grade": G_CONFIRMED},
        "cache_read_per_session_avg": {
            "value": round(_sum(invokes, "cache_read") / len(invokes), 1) if invokes else 0,
            "grade": G_COMPUTED},
    }

    # 모델별(underlying modelUsage) 토큰/비용.
    model_usage = {}
    for r in invokes:
        for mn, mv in r["model_usage"].items():
            e = model_usage.setdefault(mn, {"input_tokens": 0, "output_tokens": 0,
                                            "cache_read": 0, "cache_write": 0, "cost_usd": 0.0})
            e["input_tokens"] += mv["input_tokens"]
            e["output_tokens"] += mv["output_tokens"]
            e["cache_read"] += mv["cache_read"]
            e["cache_write"] += mv["cache_write"]
            e["cost_usd"] = round(e["cost_usd"] + mv["cost_usd"], 4)
    model_breakdown = {
        "by_model_usage": model_usage,
        "grade": G_CONFIRMED,
        "note": "modelUsage(실제 underlying 모델) 기준 — 세션 by_model_alias(주 모델)와 다를 수 "
                "있다(sonnet 세션이 소량 haiku 토큰을 포함).",
    }

    # CP2 / 게이트 재검증 수.
    counts = {
        "worker_step": {"value": len(by_class["Worker step"]), "grade": G_CONFIRMED},
        "cp2": {"value": len(by_class["CP2"]), "grade": G_CONFIRMED},
        "gate_reverification": {"value": len(by_class["gate re-verification"]),
                                "grade": G_CONFIRMED},
    }

    # 이벤트 원장에서 gate-review·rework·retry 집계 + 분류 교차검증.
    events = []
    ev_path = run_dir / "events.jsonl"
    if ev_path.exists():
        for line in ev_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                events.append(json.loads(line))
    gate_review_evts = [e for e in events if (e.get("ref") or {}).get("kind") == "gate-review"]
    rework_evts = [e for e in events if (e.get("ref") or {}).get("kind") == "rework"]
    max_retry = max((e.get("retry_count", 0) or 0) for e in events) if events else 0
    retry = {
        "value": len(rework_evts),
        "grade": G_CONFIRMED,
        "max_retry_count_field": max_retry,
        "worker_feedback_present_count": sum(1 for r in invokes if r["feedback_present"]),
        "note": "retry 수 = events 의 ref.kind=='rework' 개수. max retry_count 필드·"
                "Worker feedback_present 수와 교차 일관.",
    }
    classification_crosscheck = {
        "gate_review_events": len(gate_review_evts),
        "gate_reverification_sessions": len(by_class["gate re-verification"]),
        "consistent": len(gate_review_evts) == len(by_class["gate re-verification"]),
        "grade": G_CONFIRMED,
    }

    # CLI critical path(직렬 실행 — 물리 동시성 0 → 총합).
    critical_path = {
        "cli_serial_ms": {"value": _sum(invokes, "duration_ms"), "grade": G_COMPUTED},
        "cli_serial_seconds": {"value": round(_sum(invokes, "duration_ms") / 1000.0, 1),
                               "grade": G_COMPUTED},
        "scope_note": "CLI 구간 한정·invoke_seq 직렬 합산 수준. 이 run 은 물리 동시 디스패치 "
                      "미실행(직렬)이므로 CLI critical path = 총 CLI wall-time. 전체 E2E "
                      "critical path(주 세션·하네스 서브에이전트 포함)는 %s(로그 미노출)." % G_IMPOSSIBLE,
    }

    return {
        "run_id": run_id,
        "run_dir": str(run_dir),
        "invoke_count": len(invokes),
        "parse_errors": parse_errors,
        "sessions": sessions,
        "duration": duration,
        "cost": cost,
        "tokens": tokens,
        "model_breakdown": model_breakdown,
        "counts": counts,
        "retry": retry,
        "classification_crosscheck": classification_crosscheck,
        "critical_path": critical_path,
        "ready_set_concurrency": ready_concurrency(run_dir),
        "gate_wait": gate_waits(run_dir),
        "impossible_metrics": {
            "main_session_tokens_cost": {"grade": G_IMPOSSIBLE,
                                         "note": "주 세션(Advisor) 토큰·비용 — 하네스 미노출."},
            "harness_subagent_usd": {"grade": G_IMPOSSIBLE,
                                     "note": "하네스 서브에이전트 USD — 완료 통지는 토큰만. "
                                             "수치 전사 자리 = e2e/metrics/harness-subagent-metrics.json."},
        },
        "_rows": invokes,  # 내부 집계용(aggregate 에서 제거).
    }


# --- git anchor elapsed --------------------------------------------------------
def git_commit_ts(repo: Path, commit: str):
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "show", "-s", "--format=%ct", commit],
            capture_output=True, text=True, check=True,
        )
        return int(out.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return None


def compute_elapsed(repo: Path, start: str, end: str) -> dict:
    s = git_commit_ts(repo, start)
    e = git_commit_ts(repo, end)
    if s is None or e is None:
        return {"grade": G_IMPOSSIBLE, "value": None,
                "note": "git anchor 커밋 타임스탬프 조회 실패(%s..%s)." % (start, end)}
    sec = e - s
    return {
        "grade": G_COMPUTED,
        "start_commit": start, "end_commit": end,
        "start_iso": _iso(s), "end_iso": _iso(e),
        "elapsed_seconds": sec, "elapsed_hours": round(sec / 3600.0, 2),
        "note": "트랙 Total Elapsed = git 커밋 ts 차. 사용자 대기(게이트·주간) 포함. "
                "Active(B) 와 분리 관리(1차 §1).",
    }


# --- aggregate -----------------------------------------------------------------
def aggregate(run_metrics: list, elapsed: dict) -> dict:
    all_rows = []
    for rm in run_metrics:
        all_rows.extend(rm["_rows"])

    by_class = {"Worker step": [], "CP2": [], "gate re-verification": []}
    for r in all_rows:
        by_class[classify(r["role"], r["gate_id"])].append(r)

    def _sum(rows, key):
        return sum(r[key] for r in rows)

    model_alias_cost = {}
    model_alias_count = {}
    for r in all_rows:
        a = r["model_alias"]
        model_alias_cost[a] = round(model_alias_cost.get(a, 0.0) + r["cost_usd"], 4)
        model_alias_count[a] = model_alias_count.get(a, 0) + 1

    model_usage = {}
    for r in all_rows:
        for mn, mv in r["model_usage"].items():
            e = model_usage.setdefault(mn, {"input_tokens": 0, "output_tokens": 0,
                                            "cache_read": 0, "cache_write": 0, "cost_usd": 0.0})
            e["input_tokens"] += mv["input_tokens"]
            e["output_tokens"] += mv["output_tokens"]
            e["cache_read"] += mv["cache_read"]
            e["cache_write"] += mv["cache_write"]
            e["cost_usd"] = round(e["cost_usd"] + mv["cost_usd"], 4)

    total_dur = _sum(all_rows, "duration_ms")
    verif_cost = _sum(by_class["CP2"], "cost_usd") + _sum(by_class["gate re-verification"], "cost_usd")
    verif_time = _sum(by_class["CP2"], "duration_ms") + _sum(by_class["gate re-verification"], "duration_ms")
    total_cost = _sum(all_rows, "cost_usd")

    # 게이트 대기 aggregate.
    gate_all = []
    gate_computable_total = 0.0
    gate_lost = 0
    for rm in run_metrics:
        for g in rm["gate_wait"]["gates"]:
            gate_all.append({"run_id": rm["run_id"], **g})
            if g["grade"] == G_COMPUTED:
                gate_computable_total += g["wait_seconds"]
            elif g["grade"] == G_LOST:
                gate_lost += 1

    return {
        "runs": [rm["run_id"] for rm in run_metrics],
        "sessions": {
            "cli_total": {"value": len(all_rows), "grade": G_CONFIRMED},
            "fresh_total": {"value": sum(len({r["session_id"] for r in rm["_rows"] if r["session_id"]})
                                         for rm in run_metrics), "grade": G_CONFIRMED},
            "by_class": {k: len(v) for k, v in by_class.items()},
            "by_model_alias": model_alias_count,
        },
        "duration": {
            "total_seconds": {"value": round(total_dur / 1000.0, 1), "grade": G_CONFIRMED},
            "by_class_seconds": {k: round(_sum(v, "duration_ms") / 1000.0, 1)
                                 for k, v in by_class.items()},
        },
        "cost": {
            "total_usd": {"value": round(total_cost, 4), "grade": G_CONFIRMED},
            "by_run_usd": {rm["run_id"]: rm["cost"]["total_usd"]["value"] for rm in run_metrics},
            "by_class_usd": {k: round(_sum(v, "cost_usd"), 4) for k, v in by_class.items()},
            "by_model_alias_usd": model_alias_cost,
        },
        "tokens": {
            "output": {"value": _sum(all_rows, "output_tokens"), "grade": G_CONFIRMED},
            "input_noncache": {"value": _sum(all_rows, "input_tokens"), "grade": G_CONFIRMED},
            "cache_read": {"value": _sum(all_rows, "cache_read"), "grade": G_CONFIRMED},
            "cache_write": {"value": _sum(all_rows, "cache_write"), "grade": G_CONFIRMED},
            "cache_read_per_session_avg": {
                "value": round(_sum(all_rows, "cache_read") / len(all_rows), 1) if all_rows else 0,
                "grade": G_COMPUTED},
        },
        "model_by_usage": {"by_model_usage": model_usage, "grade": G_CONFIRMED},
        "counts": {
            "worker_step": {"value": len(by_class["Worker step"]), "grade": G_CONFIRMED},
            "cp2": {"value": len(by_class["CP2"]), "grade": G_CONFIRMED},
            "gate_reverification": {"value": len(by_class["gate re-verification"]),
                                    "grade": G_CONFIRMED},
        },
        "retry": {"value": sum(rm["retry"]["value"] for rm in run_metrics), "grade": G_CONFIRMED},
        "verification_ratio": {
            "time_ratio": round(verif_time / total_dur, 4) if total_dur else None,
            "cost_ratio": round(verif_cost / total_cost, 4) if total_cost else None,
            "verification_cost_usd": round(verif_cost, 4),
            "grade": G_COMPUTED,
            "note": "검증 = CP2 + 게이트 재검증(시간·비용).",
        },
        "ready_set_concurrency": {
            "by_run": {rm["run_id"]: rm["ready_set_concurrency"]["value"] for rm in run_metrics},
            "max_across_runs": max((rm["ready_set_concurrency"]["value"] for rm in run_metrics),
                                   default=0),
            "grade": G_COMPUTED,
        },
        "gate_wait": {
            "gates": gate_all,
            "computable_total_seconds": round(gate_computable_total, 3),
            "computable_total_minutes": round(gate_computable_total / 60.0, 2),
            "lost_count": gate_lost,
            "grade": G_COMPUTED,
            "note": "산출 가능 게이트 대기 합(+소실 %d건 별도). 벽시계·mtime 기반." % gate_lost,
        },
        "time_separation": {
            "A_total_elapsed": elapsed,
            "B_active_processing_cli_only": {
                "value_seconds": round(total_dur / 1000.0, 1),
                "grade": G_CONFIRMED,
                "note": "CLI step 세션 능동 시간만. 전체 Active(하네스 서브에이전트+주 세션 포함)"
                        "는 %s(로그 미노출) — harness-subagent-metrics.json 전사 후 합산." % G_IMPOSSIBLE,
            },
            "C_user_gate_waiting": {
                "computable_seconds": round(gate_computable_total, 3),
                "computable_minutes": round(gate_computable_total / 60.0, 2),
                "lost_gates": gate_lost,
                "grade": G_COMPUTED,
                "note": "1차 §1 지표 C. mtime 기반. 소실 게이트는 값 없음(추정 금지).",
            },
        },
        "impossible_metrics": {
            "main_session_tokens_cost": G_IMPOSSIBLE,
            "harness_subagent_usd": G_IMPOSSIBLE,
        },
    }


def _strip_rows(rm: dict) -> dict:
    out = dict(rm)
    out.pop("_rows", None)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="T1 Minimal Telemetry — Baseline run 집계(순수 판독·원장 무수정)")
    parser.add_argument("run_dirs", nargs="+", help="run 데이터 백엔드 디렉터리(1개 이상)")
    parser.add_argument("--git-anchor", nargs=2, metavar=("START", "END"),
                        help="트랙 Total Elapsed 산출용 git 시작/끝 커밋")
    parser.add_argument("-o", "--out", default=None,
                        help="출력 디렉터리(기본 = 이 스크립트 옆 metrics/)")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    outdir = Path(args.out).resolve() if args.out else (here / "metrics")
    outdir.mkdir(parents=True, exist_ok=True)

    run_metrics = []
    for rd in args.run_dirs:
        rm = collect_run(Path(rd))
        run_metrics.append(rm)
        out_path = outdir / ("%s.run-metrics.json" % rm["run_id"])
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(_strip_rows(rm), fh, ensure_ascii=False, indent=2, sort_keys=True)
        print("[RUN] %s → %s (invoke %d)" % (rm["run_id"], out_path.name, rm["invoke_count"]))
        if rm["parse_errors"]:
            print("      [WARN] raw_stdout 파싱 실패: %s" % rm["parse_errors"])

    elapsed = {"grade": G_IMPOSSIBLE, "value": None,
               "note": "--git-anchor 미제공 → 트랙 Total Elapsed 산출 불가(추정 금지)."}
    if args.git_anchor:
        # 저장소 루트 추정 = 이 스크립트에서 상위로 올라간 git repo.
        repo = here
        while repo != repo.parent and not (repo / ".git").exists():
            repo = repo.parent
        elapsed = compute_elapsed(repo, args.git_anchor[0], args.git_anchor[1])

    agg = aggregate(run_metrics, elapsed)
    agg_path = outdir / "aggregate.run-metrics.json"
    with open(agg_path, "w", encoding="utf-8") as fh:
        json.dump({
            "generated_at": _iso(datetime.now(timezone.utc).timestamp()),
            "generator": "collect_metrics.py (T1 Minimal Telemetry)",
            "source": "invoke 로그·파일 mtime·(선택) git ts — 순수 판독",
            "aggregate": agg,
        }, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print("[AGG] %d run → %s" % (len(run_metrics), agg_path.name))
    print("[TOTALS] sessions=%d cost=$%.4f dur=%.1fs output_tok=%d cacheRead=%d"
          % (agg["sessions"]["cli_total"]["value"], agg["cost"]["total_usd"]["value"],
             agg["duration"]["total_seconds"]["value"], agg["tokens"]["output"]["value"],
             agg["tokens"]["cache_read"]["value"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
