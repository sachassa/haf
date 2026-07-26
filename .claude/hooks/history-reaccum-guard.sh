#!/usr/bin/env sh
# history-reaccum-guard — SessionStart: 문서 이력 절 재퇴적 감지
# 사용자 결정 2026-07-27 로 in-file 이력 절은 폐지되고 헤딩 + git 포인터 스텁만 남는다.
# 이 가드는 이력 절 안에 표 데이터 행이 다시 쌓였는지를 매 세션 측정한다.
# 감지·지시만 한다 — 문서를 자동 수정하지 않는다(재압축은 앵커 해시 선택이 필요하므로).
# 정상 시 침묵한다(출력 0줄) — SessionStart 노이즈를 만들지 않으려고 상시 리마인더를 두지 않는다.
# fail-open: python 부재·스크립트 오류·비정상 출력은 절대 발화하지 않는다(자기-DoS 방지).
# 경로는 전부 상대경로다(선례 = md-budget-guard.sh · $CLAUDE_PROJECT_DIR 은 이 환경에서 죽는다).
set -u

TOOL=".claude/tools/history_compact.py"
[ -f "$TOOL" ] || exit 0

# python 실행기 탐색 — 없으면 조용히 종료.
PY=""
if command -v python >/dev/null 2>&1; then
  PY="python"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
fi
[ -n "$PY" ] || exit 0

# 한국어 경로·출력 환경 전제 — 미지정 시 cp949 로 stdout 이 깨지거나 stderr 가 유실된다.
# stderr 는 버린다: 내부 오류를 세션 표면에 흘리지 않는다(fail-open).
OUT=$(PYTHONIOENCODING=utf-8 "$PY" "$TOOL" --check 2>/dev/null) || exit 0

[ -n "$OUT" ] || exit 0

# 방어: 기대 형식(REACCUM 행)이 아니면 발화하지 않는다 — 오탐·잡음 차단.
printf '%s\n' "$OUT" | grep -q '^REACCUM ' || exit 0

printf '[이력 표 재퇴적 감지]\n'
printf '이력 절 안에 표 데이터 행이 다시 쌓였다. history_compact.py 로 재압축하라(규범 = docs/spec-versioning-policy.md §3).\n'
printf '조치: 제거 전 전문을 담은 git 앵커 해시를 정한 뒤 `python %s --anchor <hash> [--root DIR]` 로 dry-run 하고, 확인 후 --apply 하라. 이력은 파일이 아니라 git 이 보존한다.\n' "$TOOL"
printf '%s\n' "$OUT"
