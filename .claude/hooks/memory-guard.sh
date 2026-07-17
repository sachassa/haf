#!/usr/bin/env sh
# memory-guard — SessionStart: 자동 메모리 클린 가드
# MEMORY.md(auto-memory 색인)를 매 세션 측정해 (1) 압축 작성 규율을 주입하고
# (2) 예산 초과 시 색인 압축 클린을 지시한다. 상세는 개별 메모리 파일 본문에 보존.
# 감지·지시만 한다 — 색인을 자동 수정하지 않는다(시맨틱 압축은 판단이 필요하므로).
set -eu

# auto-memory 색인 경로 ($HOME 사용 — 사용자명 하드코딩 없음).
# 프로젝트 인코딩 디렉터리는 이 저장소 고정값. 다른 머신/클론에서 부재 시 조용히 종료(무해).
MEM="$HOME/.claude/projects/C--my-claude-project-universal-agentic-framework/memory/MEMORY.md"
BUDGET=6000      # 색인 총 바이트 예산
LINE_CAP=400     # 항목당 바이트 상한

[ -f "$MEM" ] || exit 0

SIZE=$(wc -c < "$MEM" | tr -d ' ')
LONG=$(awk -v cap="$LINE_CAP" 'length($0) > cap { c++ } END { print c+0 }' "$MEM")

if [ "$SIZE" -gt "$BUDGET" ] || [ "$LONG" -gt 0 ]; then
  printf '[메모리 자동 클린 — SessionStart guard]\n'
  printf 'MEMORY.md=%sB (예산 %sB) · 항목당 상한(%sB) 초과=%s개.\n' "$SIZE" "$BUDGET" "$LINE_CAP" "$LONG"
  printf '조치: 색인을 "- [Title](file.md) — 짧은 훅" 한 줄 형식으로 압축하라. 커밋해시·날짜·하위트랙·CP카운트·seq는 개별 메모리 파일 본문에만 두고 색인에서 제거. 링크·제목·상태(대기/완결) 훅은 보존. 압축 후 wc -c로 예산 이하 확인.\n'
fi

printf '[메모리 규율] 신규/갱신 항목은 항상 한 줄+짧은 훅(<= %sB). 상세는 개별 파일 본문에만.\n' "$LINE_CAP"
