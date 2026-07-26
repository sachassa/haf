"""게이트 큐 렌더러 (OQ-PO-B1·§DC-9) — `pending_gates` 파생 뷰의 사람 친화 제시 표면.

이 스크립트는 headless 엔진(05 §2.2)이 물리 정지(exit 2)한 정지 게이트 큐를 **주 세션
(사용자 대화 주체)** 이 사용자에게 표면화할 때 쓰는 form-B 렌더러다(project-orchestration-
binding §3.2 게이트 큐 제시 채널). LLM 을 호출하지 않는 **결정적 순수 렌더**이며, 어떤
파일도 쓰지 않는다(원장 무변경·읽기 전용).

진리원천 = `gates.pending_gates(events, policy)` 파생 뷰(binding §3.1·PO-INV 2). stop-signal.json
에 의존하지 않고 원장(events.jsonl + gate_policy.json)에서 **직접 파생**하므로, 부분 해소 후
재렌더도 정확하다(해소 이벤트가 append 되면 파생 뷰가 그 게이트를 자동 제외). 라벨·문면은
binding §3.2 구조 제안(L66-70)을 그대로 승계하며 새 어휘를 발명하지 않는다.

사용법:
  python orchestration/adapters/claude/render_gates.py <run_dir> [--json]

  - 기본: 사람 친화 한국어 마크다운 텍스트를 stdout 으로.
  - --json: 항목별 구조화 JSON(pending 원 필드 + label + eligible_resolvers + resolve_command).
  - 미해소 정지 게이트 0건: "미해소 정지 게이트 없음" 1줄.
  - 성공 시 exit 0(렌더는 뷰다 — 정지 신호 exit 2 는 런처 소관). run_dir/파일 부재 등
    오류는 stderr + exit 1.

거버넌스: 이 스크립트는 `orchestration/adapters/claude/` 소속 어댑터다 — 한국어 사용자 문면·
라벨(구체 토큰)의 사용이 허용되는 격리 지점이다(PO-INV 8 은 중립 `orchestration/framework/`
에만 적용). 중립 계약(gates.py 어휘)을 재정의하지 않고 파생 뷰를 판독·표면화만 한다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# --- 경로 배선: 비프로덕션 드라이버(e2e) 를 import 경로에 둔다(resolve_gate.py 동형) -----
#   render_gates.py = orchestration/adapters/claude/render_gates.py
#   parents[2] = repo root. k_common import 가 _orch_common 을 통해 중립 코드 경로
#   (orchestrator·step-host)를 sys.path 에 배선한다(gates 판독 전제).
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
E2E_DIR = REPO_ROOT / "uahf" / "framework" / "adapters" / "claude" / "orchestration-data" / "e2e"
if str(E2E_DIR) not in sys.path:
    sys.path.insert(0, str(E2E_DIR))

from k_common import load_json  # noqa: E402  (읽기 전용 json 로더·중립 경로 배선 부작용)

# 중립 게이트 평가기·파생 뷰(무수정 라이브러리).
from gates import (  # noqa: E402
    GATE_ESCALATION_REQUIRED,
    GATE_USER_DECISION_REQUIRED,
    GatePolicy,
    pending_gates,
)


# ==========================================================================
# 어댑터 소유 데이터 — 사람 친화 라벨·CLI 매핑 (다국어·문면 조정의 확장점)
#
# 이 표들은 **어댑터가 소유하는 데이터**다(중립 gates.py 어휘가 아님). 라벨 문면은 binding
# §3.2 구조 제안(L67)을 그대로 승계한다. 다국어·문면 변경은 **이 표 교체**가 확장점이며,
# 렌더 로직 본문은 건드리지 않는다(정책-as-데이터 동형).
# ==========================================================================
GATE_LABELS = {
    GATE_USER_DECISION_REQUIRED: "사용자 결정 대기(확정 권위)",
    GATE_ESCALATION_REQUIRED: "Advisor/사람 해소 대기",
}

# gateKind → resolve_gate.py 의 --gate-kind CLI 인자(정확한 해소 명령 구성용).
# resolve_gate.py GATE_KIND_MAP 의 역방향(정지 게이트분): user_decision·escalation.
GATE_KIND_TO_CLI = {
    GATE_USER_DECISION_REQUIRED: "user_decision",
    GATE_ESCALATION_REQUIRED: "escalation",
}

# 해소 명령 템플릿(resolve_gate.py 실제 CLI 형태·L17-19·L457-470 정독 기반).
RESOLVE_SCRIPT = "orchestration/adapters/claude/resolve_gate.py"


def _label(gate_kind):
    """gateKind → 사람 친화 라벨(미지 gateKind 는 원 값 그대로·추측 금지)."""
    return GATE_LABELS.get(gate_kind, str(gate_kind))


def eligible_resolvers(gate_kind, policy: GatePolicy) -> list:
    """이 정지 게이트를 해소할 자격이 있는 actor 목록(정책 데이터 파생·하드코딩 0).

    - user_decision_required → [정책 userActorClass](확정 권위·단일 actor 클래스).
    - escalation_required → 정책 escalationResolvers 목록.
    is_eligible_resolver 와 동일 근거(정책 데이터)에서 파생한다 — 표시용 목록이다.
    """
    if gate_kind == GATE_USER_DECISION_REQUIRED:
        return [policy.user_actor_class]
    if gate_kind == GATE_ESCALATION_REQUIRED:
        return list(policy.escalation_resolvers)
    return []


# --gate-id 값에 인용이 필요 없는 문자 집합(엔진 파생 gate_id 는 `gate-unit-<id>::exec-escalation`
# 형태라 통상 이 집합에 든다). 벗어나면 큰따옴표로 감싼다 — 렌더 명령을 그대로 붙여 넣어도
# 셸이 토큰을 쪼개지 않게 하는 결정적 규칙이다.
_SAFE_CLI_CHARS = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" "-_.:/@+=,"
)


def _cli_token(value) -> str:
    """CLI 인자 값 1개를 셸 안전 토큰으로 만든다(결정적·안전 문자면 그대로)."""
    text = str(value)
    if text and all(ch in _SAFE_CLI_CHARS for ch in text):
        return text
    return '"%s"' % text.replace('"', '\\"')


def resolve_command(gate_kind, policy: GatePolicy, gate_id=None) -> str:
    """이 게이트를 해소하는 resolve_gate.py 실제 CLI 1줄(적격 actor 예시 채움).

    <run_dir> 는 호출자가 채우는 자리표시자다(렌더는 run_dir 절대경로를 강제하지 않는다).
    actor 예시 = 적격 목록의 첫 값(정책 데이터 파생). 미지 gateKind 는 명령을 구성하지 않는다.

    `gate_id` 를 주면 `--gate-id <gate_id>` 를 **항상** 싣는다(항목별 렌더는 언제나 준다).
    이유 = resolve_gate 는 같은 gateKind 가 2건 이상 pending 이면 무지목 호출을 차단하므로
    (binding §3.4), 지목 없는 명령은 다중 pending 상황에서 그대로 실행되지 않는다. 지목을
    항상 실어 두면 단일/다중 어느 상황에서도 렌더 명령이 그대로 실행된다. `gate_id=None`
    (게이트 문맥 없는 일반형 조회)이면 종전 문면 그대로다 — 가법.
    """
    cli = GATE_KIND_TO_CLI.get(gate_kind)
    if cli is None:
        return "(해소 명령 없음 — 미지 gateKind: %s)" % gate_kind
    resolvers = eligible_resolvers(gate_kind, policy)
    actor = resolvers[0] if resolvers else "<actor>"
    named = "" if gate_id is None else (" --gate-id %s" % _cli_token(gate_id))
    return (
        "python %s <run_dir> --gate-kind %s --actor %s%s [--response \"<응답 원문>\"]"
        % (RESOLVE_SCRIPT, cli, actor, named)
    )


def _scoped_sentence(gate_kind, scoped_question) -> str:
    """구조화 힌트 {unitId, gateKind} → 사람 친화 문면(원 데이터도 병기용으로 분리 제공).

    binding §3.2 L69: "gates.py 가 실은 구조화 힌트 {unitId, gateKind}; 사람 친화 문면 렌더는
    이 제시 채널이 담당". unitId 부재 시 라벨만으로 문면을 구성한다(추측 금지).
    """
    hint = scoped_question or {}
    unit_id = hint.get("unitId")
    label = _label(gate_kind)
    if unit_id is not None:
        return "단위 %s에 %s 게이트가 걸려 있습니다." % (unit_id, label)
    return "%s 게이트가 걸려 있습니다." % label


def _json_item(pend: dict, policy: GatePolicy) -> dict:
    """--json 항목 = pending_gates 원 필드 + label + eligible_resolvers + resolve_command."""
    gate_kind = pend.get("gateKind")
    item = dict(pend)  # 원 필드 보존(gate_id·gateKind·target·scoped_question·since).
    item["label"] = _label(gate_kind)
    item["eligible_resolvers"] = eligible_resolvers(gate_kind, policy)
    item["resolve_command"] = resolve_command(gate_kind, policy, pend.get("gate_id"))
    return item


def render_pending(pending: list, policy: GatePolicy) -> str:
    """미해소 정지 게이트 목록 → 사람 친화 한국어 마크다운(런처가 import 재사용).

    결정적 순수 함수(같은 입력 → 같은 문자열·부작용 0). 항목당 block은 binding §3.2 구조
    제안(라벨·gate_id·target·scoped_question·since·적격 actor·해소 명령)을 그대로 승계한다.
    미해소 0건이면 "미해소 정지 게이트 없음" 1줄.
    """
    if not pending:
        return "미해소 정지 게이트 없음"

    lines: list = []
    lines.append("# 미해소 정지 게이트 큐 (%d건)" % len(pending))
    lines.append("")
    lines.append(
        "아래 게이트는 headless 엔진이 물리 정지(exit 2)한 미해소 정지 게이트다. "
        "`pending_gates` 파생 뷰에서 직접 파생했다(원장 무변경). 적격 actor 가 해소 명령으로 "
        "게이트-해소 이벤트를 append 한 뒤 `--resume` 하면 결정적으로 재개된다."
    )
    lines.append("")
    for i, pend in enumerate(pending, start=1):
        gate_kind = pend.get("gateKind")
        gate_id = pend.get("gate_id")
        target = pend.get("target")
        scoped_question = pend.get("scoped_question")
        since = pend.get("since")
        resolvers = eligible_resolvers(gate_kind, policy)

        lines.append("## [%d] %s" % (i, _label(gate_kind)))
        lines.append("- gate_id: `%s`" % gate_id)
        lines.append("- gateKind: `%s`" % gate_kind)
        lines.append("- target: `%s`" % json.dumps(target, ensure_ascii=False, sort_keys=True))
        lines.append("- 결정/해소 사항: %s" % _scoped_sentence(gate_kind, scoped_question))
        lines.append(
            "  - (원 scoped_question: `%s`)"
            % json.dumps(scoped_question, ensure_ascii=False, sort_keys=True)
        )
        lines.append(
            "- since: 요구 순번 %s — run 전역 append 순서·물리 시각 아님(binding §3.1)" % since
        )
        lines.append("- 적격 해소 actor: %s" % ", ".join(str(r) for r in resolvers))
        lines.append("- 해소 명령:")
        lines.append("  ```")
        lines.append("  %s" % resolve_command(gate_kind, policy, gate_id))
        lines.append("  ```")
        lines.append("")
    # 말미 개행 정리 — 결정적 산출을 위해 후행 빈 줄 1개로 정규화.
    while len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
        lines.pop()
    return "\n".join(lines).rstrip("\n")


# ==========================================================================
# 원장 판독(읽기 전용) — pending_gates 파생 (어떤 파일도 쓰지 않는다)
# ==========================================================================
def _read_events(events_path: Path) -> list:
    """events.jsonl 을 읽기 전용으로 판독한다(1행 1이벤트·resolve_gate 테스트 _read_jsonl 동형).

    JsonlEventStore 는 생성자에서 파일·디렉터리를 만들 수 있어(쓰기) 원장 무변경 요건에
    부적합하다 — 여기서는 순수 판독만 하는 별도 로더를 쓴다(파일 부재 시 FileNotFoundError).
    """
    out: list = []
    with open(events_path, "r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if raw:
                out.append(json.loads(raw))
    return out


def load_pending(run_dir: Path):
    """(pending_gates, policy) 를 원장에서 직접 파생한다(읽기 전용·stop-signal 비의존).

    events.jsonl + gate_policy.json 을 판독해 gates.pending_gates 로 파생한다. 파일 부재·
    파싱 오류는 예외로 표면화한다(호출자가 stderr + exit 1 로 정직 처리).
    """
    events = _read_events(run_dir / "events.jsonl")
    policy = GatePolicy.from_dict(load_json(run_dir / "gate_policy.json"))
    return pending_gates(events, policy), policy


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="게이트 큐 렌더러 — pending_gates 파생 뷰의 사람 친화 제시(form-B·읽기 전용)"
    )
    parser.add_argument("run_dir", help="run 데이터 백엔드 디렉터리")
    parser.add_argument("--json", action="store_true",
                        help="구조화 JSON 출력(pending 원 필드 + label + eligible_resolvers + resolve_command)")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print("[ERR] run_dir 이 디렉터리가 아니다(부재?): %s" % run_dir, file=sys.stderr)
        return 1

    try:
        pending, policy = load_pending(run_dir)
    except FileNotFoundError as exc:
        print("[ERR] 원장 파일 부재 — 렌더 불가: %s" % exc, file=sys.stderr)
        return 1
    except (ValueError, json.JSONDecodeError) as exc:
        print("[ERR] 원장 파싱 오류 — 렌더 불가: %s" % exc, file=sys.stderr)
        return 1

    if args.json:
        payload = [_json_item(p, policy) for p in pending]
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_pending(pending, policy))
    return 0


def _force_utf8_console() -> None:
    """CLI 진입 시 stdout/stderr 를 UTF-8 로 재구성한다(Windows cp949 콘솔 방어).

    이 렌더러의 출력 본문은 전부 한국어 문면이라, cp949 등 비-UTF-8 콘솔에서 그대로 print 하면
    UnicodeEncodeError 로 크래시한다. 재구성 가능한 TextIOWrapper 일 때만 적용하며 실패는
    무시한다(어댑터 격리 지점의 물리 표면 보정일 뿐 렌더 로직·중립 코드 무변경). 테스트는
    main() 을 직접 호출하므로(이 경로 미경유) 영향받지 않는다.
    """
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfig = getattr(stream, "reconfigure", None)
        if reconfig is not None:
            try:
                reconfig(encoding="utf-8")
            except (ValueError, OSError):
                pass


if __name__ == "__main__":
    _force_utf8_console()
    sys.exit(main())
