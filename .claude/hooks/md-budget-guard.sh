#!/usr/bin/env sh
# md-budget-guard — SessionStart: md 재퇴적 방지 예산 가드
# (1) docs/session-handoff.md 바이트 예산과 (2) git 추적 *.md 총량 워터마크를 매 세션 측정한다.
# 감지·지시만 한다 — 문서를 자동 수정하지 않는다(시맨틱 압축은 판단이 필요하므로).
# 정상 시 침묵한다(출력 0줄) — SessionStart 노이즈를 만들지 않으려고 상시 리마인더를 두지 않는다.
set -eu

HANDOFF="docs/session-handoff.md"
BUDGET_HANDOFF="${BUDGET_HANDOFF:-25000}"   # 핸드오프 단일 파일 바이트 예산
# 워터마크 하향 2,700,000 -> 2,500,000 (compaction 트랙 2026-07-27 — 이력 절 제거로 확보한 여유를 재퇴적 여지로 남기지 않는다).
BUDGET_TOTAL="${BUDGET_TOTAL:-2500000}"     # git 추적 *.md 총 바이트 워터마크

# --- 검사 1: 핸드오프 단일 파일 예산 -----------------------------------------
# 부재 시 조용히 skip(무해) — 다른 머신/클론·부분 체크아웃 대비.
if [ -f "$HANDOFF" ]; then
  SIZE=$(wc -c < "$HANDOFF" | tr -d ' ')
  if [ "$SIZE" -gt "$BUDGET_HANDOFF" ]; then
    printf '[핸드오프 예산 가드]\n'
    printf '%s=%sB (예산 %sB · 초과 %sB).\n' \
      "$HANDOFF" "$SIZE" "$BUDGET_HANDOFF" "$((SIZE - BUDGET_HANDOFF))"
    printf '조치: 제자리 갱신하라 — 갱신 블록 누적 append 금지(정책 §6). 과거 갱신분은 git 이력에 있으니 본문에서 제거하고, 초과분은 §B 이월 항목으로 통합하거나 상세 앵커 문서로 이관하라. 정리 후 wc -c로 예산 이하 확인.\n'
  fi
fi

# --- 검사 2: git 추적 *.md 총량 워터마크 --------------------------------------
# git 부재·비저장소·명령 실패 시 조용히 skip(fail-open).
command -v git >/dev/null 2>&1 || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# 주: xargs 배치 분할 시 wc -c 는 "total" 을 배치마다 내므로 마지막 total 만 읽으면
# 과소 집계된다. per-file 행을 직접 합산하고 total 행은 배제한다.
TOTAL=$(git ls-files -z '*.md' 2>/dev/null | xargs -0 wc -c 2>/dev/null \
  | awk '$NF == "total" { next } { s += $1 } END { print s+0 }') || TOTAL=""

[ -n "$TOTAL" ] || exit 0
case "$TOTAL" in ''|*[!0-9]*) exit 0 ;; esac

if [ "$TOTAL" -gt "$BUDGET_TOTAL" ]; then
  printf '[md 총량 워터마크]\n'
  printf 'git 추적 *.md 총 %sB (기준 %sB · 초과 %sB).\n' \
    "$TOTAL" "$BUDGET_TOTAL" "$((TOTAL - BUDGET_TOTAL))"
  printf '조치: 슬림화 감사 재실행을 검토하라(선례 = refactor/md-slimming — 중복 정본·append 누적·기계 생성 덤프 제거로 -1.04MB).\n'
fi
