#!/usr/bin/env sh
# F-H2 픽스처 Hook action — notify-fail
# 시연 픽스처 — 실계약 문서 아님. 의도적 결함 정당 보유.
# 비차단 격리 시연(08 §8 예2·INV-2)을 위해 의도적으로 실패(timeout/오류 모사)한다.
echo "notify-fail: simulated action error (timeout) — 의도적 결함" 1>&2
exit 1
