#!/usr/bin/env sh
# EX-DH Hook Dispatch 드라이버 — 형태 A 호스트(주 세션 오케스트레이션) 절차 구동
# 시연 도구 — 실계약 문서 아님. 라이브 하네스 native hook 실행 메커니즘(형태 B, .claude/settings.json)이 아니다(DP-E3, 미도입).
#
# hooks-binding §5.1 Form A Dispatch 5단계를 예/아니오 판정 가능하게 실현한다:
#   1. 이벤트 관찰 (호스트, occurredAt = 순서 값 — L-09)
#   2. 바인딩 해소 (Hook Registry에서 (event, phase) 일치분 수집 — 08 §3.1-C)
#   3. 결정적 정렬 (08 §3.1-D 3단 기준: order 오름차순 → Module 등록 순서(regIndex) → hookId 사전순)
#   4. 격리 호출 (각 action에 Event Record 읽기 전용 전달 — INV-3)
#   5. 실패 격리·비차단 (Hook Failure Report blocking=false, 본 작업·다른 Hook 계속 — INV-2)
#
# 사용법: ex-dh-dispatch-driver.sh <event> <phase> <registry.tsv> <occurredAt>
#   registry.tsv 열(TAB 구분): hookId <TAB> event <TAB> phase <TAB> order <TAB> regIndex <TAB> actionPath
#   출력 경로(환경 변수): HOOK_DISPATCH_LOG(필수) HOOK_FAILURE_REPORTS(필수) HOOK_AUDIT_LOG HOOK_ORDER_TRACE
set -u
TAB=$(printf '\t')
EVENT="$1"; PHASE="$2"; REGISTRY="$3"; OCCURRED_AT="$4"
: "${HOOK_DISPATCH_LOG:?}"; : "${HOOK_FAILURE_REPORTS:?}"
log() { printf '%s\n' "$*" >> "$HOOK_DISPATCH_LOG"; }

log "=== Hook Dispatch (형태 A, hooks-binding §5.1) — event=$EVENT phase=$PHASE occurredAt=$OCCURRED_AT ==="

# 단계 1: 이벤트 관찰 (호스트 관찰 — OQ-H2 §4 소관; occurredAt = 순서 값, 벽시계 아님 — L-09)
log "step1 관찰: 호스트가 (event=$EVENT, phase=$PHASE) 관찰(형태 A). occurredAt=$OCCURRED_AT (순서 값, 벽시계 시각 아님 — L-09)."

# 단계 2: 바인딩 해소 ((event, phase) 일치분 수집 — Hook Registry, 08 §3.1-C)
MATCHES=$(awk -F"$TAB" -v e="$EVENT" -v p="$PHASE" '$2==e && $3==p {print}' "$REGISTRY")
if [ -z "$MATCHES" ]; then
  log "step2 해소: ($EVENT, $PHASE) 바인딩 0건 — Dispatch가 아무 Hook도 호출하지 않고 종료(본 작업 결과 불변)."
  log "dispatch 종료: 본 작업 결과 불변 (INV-1)."
  exit 0
fi
log "step2 해소: 일치 바인딩 —"
printf '%s\n' "$MATCHES" | while IFS="$TAB" read -r hid ev ph ord ridx act; do
  log "   - hookId=$hid order=$ord regIndex=$ridx action=$act"
done

# 단계 3: 결정적 정렬 (08 §3.1-D 3단 기준 — order asc → regIndex asc → hookId 사전순)
SORTED=$(printf '%s\n' "$MATCHES" | sort -t "$TAB" -k4,4n -k5,5n -k1,1)
log "step3 정렬(08 §3.1-D: order 오름차순 → 등록 순서(regIndex) → hookId 사전순) —"
printf '%s\n' "$SORTED" | while IFS="$TAB" read -r hid ev ph ord ridx act; do
  log "   -> $hid (order=$ord, regIndex=$ridx)"
done

# 단계 4 & 5: 격리 호출 + 실패 격리·비차단
printf '%s\n' "$SORTED" | while IFS="$TAB" read -r hid ev ph ord ridx act; do
  log "step4 격리 호출: hookId=$hid action=$act (Event Record 읽기 전용 전달 — INV-3)"
  # Event Record 5필드(08 §3.2-C / hooks-binding §5.2)를 읽기 전용으로 전달. 서브셸 격리 호출.
  ( HOOK_EVENT_ID="$EVENT" \
    HOOK_PHASE="$PHASE" \
    HOOK_SOURCE_REF="loop-data:v08-demo-h.jsonl#$EVENT" \
    HOOK_CONTEXT_VIEW="read-only-projection(원천 spec 소유 — 08 §3.2-C)" \
    HOOK_OCCURRED_AT="$OCCURRED_AT" \
    HOOK_AUDIT_LOG="${HOOK_AUDIT_LOG:-/dev/null}" \
    HOOK_ORDER_TRACE="${HOOK_ORDER_TRACE:-/dev/null}" \
    sh "$act" )
  rc=$?
  if [ "$rc" -ne 0 ]; then
    log "step5 실패 격리: hookId=$hid 실패(rc=$rc) — Hook Failure Report(blocking=false) 기록. 본 작업·다른 Hook 계속 (INV-2)."
    {
      echo "--- Hook Failure Report (08 §3.2-E / hooks-binding §5.3) ---"
      echo "hookId: $hid"
      echo "event: $EVENT"
      echo "phase: $PHASE"
      echo "reason: action error (exit $rc — 모사 timeout/오류)"
      echo "blocking: false"
      echo "lesson_candidate: 예 — Hook action 실패는 Lesson 후보 (08 §6)"
      echo ""
    } >> "$HOOK_FAILURE_REPORTS"
  else
    log "step4 결과: hookId=$hid 성공."
  fi
done

log "dispatch 완료: 바인딩된 모든 Hook 정확히 한 번 호출. 본 작업 결과 불변 (INV-1) — Hook 결과와 독립."
