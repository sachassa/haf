#!/usr/bin/env sh
# githooks-wiring-guard — SessionStart: 커밋 훅 배선 생존 확인.
# core.hooksPath 는 클론(로컬 설정)마다 1회 지정해야 하며, 풀리면 pre-commit 은
# 조용히 죽는다(훅 배선 실패는 침묵한다 — 실측 교훈). 매 세션 배선을 검사해
# 죽어 있으면 복구 명령을 지시한다. 정상 시 침묵한다(출력 0줄).
# fail-open: git 부재·비저장소는 조용히 skip.
set -u

command -v git >/dev/null 2>&1 || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

HOOKSPATH=$(git config core.hooksPath 2>/dev/null) || HOOKSPATH=""

if [ "$HOOKSPATH" != ".githooks" ] || [ ! -f ".githooks/pre-commit" ]; then
  printf '[커밋 훅 배선 사망]\n'
  printf 'core.hooksPath=%s · .githooks/pre-commit %s — 커밋 시점 재퇴적 방어가 꺼져 있다.\n' \
    "${HOOKSPATH:-미설정}" "$([ -f .githooks/pre-commit ] && echo 존재 || echo 부재)"
  printf '조치: git config core.hooksPath .githooks 실행 후, 위반 강제 케이스로 차단 발화를 실호출 확인하라.\n'
fi
