#!/usr/bin/env sh
# F-H4 픽스처 Hook action — archive (순서 결정성 시연, 결함 없음)
# 시연 픽스처 — 실계약 문서 아님.
# order-trace에 자기 hookId를 append → 실행 순서를 관측 가능하게 남긴다.
set -eu
TRACE="${HOOK_ORDER_TRACE:?HOOK_ORDER_TRACE must be provided by the dispatch host}"
echo "archive" >> "$TRACE"
