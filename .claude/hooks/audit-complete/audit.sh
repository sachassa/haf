#!/usr/bin/env sh
# F-H1 레퍼런스 Hook action — audit-complete (08 §8 예1 동형)
# 감사 기록 생성. Event Record를 읽기 전용으로 소비한다 (INV-3, 08 §3.1-B).
# 이 action은 Event Record나 이벤트 원천 상태를 변경하지 않는다 (read-only 강제, INV-3).
set -eu

# 감사 로그 출력 경로는 Dispatch 호스트(형태 A)가 주입한다.
AUDIT_LOG="${HOOK_AUDIT_LOG:?HOOK_AUDIT_LOG must be provided by the dispatch host}"

# Event Record 5필드 읽기 전용 투영 (08 §3.2-C / hooks-binding §5.2) — 환경 변수로 전달됨.
EID="${HOOK_EVENT_ID:-}"
PHASE="${HOOK_PHASE:-}"
SREF="${HOOK_SOURCE_REF:-}"
CVIEW="${HOOK_CONTEXT_VIEW:-}"
OAT="${HOOK_OCCURRED_AT:-}"   # 순서 값(논리 시각) — 벽시계 시각 아님 (L-09)

# 부수 동작: 감사 기록 append (자기 경계 안 산출물 기록 — 08 §3.1-B 할 수 있는 것).
printf '[audit] hookId=audit-complete eventId=%s phase=%s sourceRef=%s contextView=%s occurredAt=%s\n' \
  "$EID" "$PHASE" "$SREF" "$CVIEW" "$OAT" >> "$AUDIT_LOG"
