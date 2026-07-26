# ARCHIVE — 아카이브 원장 (append-only)

용도: 작업 트리에서 제거된 산출물의 **앵커 열람 원장**이다. 모든 원본은 git 이력에 영구 보존되며, `git show <앵커커밋>:<경로>` 로 열람한다 (디렉터리 목록: `git ls-tree -r <앵커커밋> -- <경로>`). 근거·절차 = `docs/artifact-lifecycle-policy.md` §5. 이 표는 append-only이며 행 문면을 사후 수정하지 않는다.

파일 수는 등재일의 git 추적 실측 기준이다.

| 대상 (경로 · 파일 수) | 앵커 커밋 | 등급 | 사유 | 등재일 |
|---|---|---|---|---|
| `uahf/docs/` 버전 마일스톤 문서 42파일 (v0.2~v1.2 — demo·demo-procedure·verification-report·promotion-review·release-notes·dogfooding-spec/report·install-guide 등, `v1.0-user-guide.md` 제외) | `cd9247b` | track-design | v0.2~v1.2 마일스톤 동결 이력 (superseded 세대) | 2026-07-17 |
| `uahf/docs/v0.5-demo-fixtures/` (7파일) | `cd9247b` | evidence | v0.5 데모 실증 픽스처 | 2026-07-17 |
| `uahf/docs/v0.6-demo-fixtures/` (12파일) | `cd9247b` | evidence | v0.6 데모 실증 픽스처 (loop-data v06·mi-0031~0034 report_ref 대상) | 2026-07-17 |
| `uahf/docs/v0.7-demo-fixtures/` (9파일) | `cd9247b` | evidence | v0.7 데모 실증 픽스처 (workflow-binding §7 실측 판정 근거였음 — 앵커 전환 완료) | 2026-07-17 |
| `uahf/docs/v0.8-demo-fixtures/` (32파일) | `cd9247b` | evidence | v0.8 Extension 데모 픽스처 (plugins-binding DP-E6 bundle 원본 — 앵커 전환 완료) | 2026-07-17 |
| `uahf/docs/v0.9-demo-fixtures/` (37파일) | `cd9247b` | evidence | v0.9 Scaffold 설치 시연 사본 | 2026-07-17 |
| `uahf/docs/v1.0-generic-demo-fixtures/` (16파일) | `cd9247b` | evidence | v1.0 Generic Adapter conformance C3 판정 근거 (앵커 전환 완료) | 2026-07-17 |
| `uahf/dogfooding/uahf-lessons/` (35파일) | `cd9247b` | evidence | v1.0 자기적용(dogfooding) 실증 — 소형 CLI 샘플 프로젝트 전체 트리 | 2026-07-17 |
| `uahf/framework/adapters/claude/orchestration-data/runs/` 4 run·86파일 (orch-j-e2e·orch-k-nonfixture-smoke·orch-m-maturation-cp·orch-w-impl-cp) | `cd9247b` | evidence | v1.6 종단 E2E·v1.7 Control Plane run·Performance Baseline evidence(원 동결 커밋 `ad451ee`) | 2026-07-17 |
| `uahf/framework/adapters/claude/step-data/runs/` 8 run·74파일 (e2e-s1~s7b) | `cd9247b` | evidence | v1.5 형태 B Step Hosting E2E 7시나리오+resume 실증 | 2026-07-17 |
| `uahf/framework/adapters/claude/solution-design-data/events/` maturation-r001~r003 (20파일) | `cd9247b` | evidence | Project Contract v1→v2→v3 성숙 계보 원장 (성숙 결과물 = `discovery-data/contracts/uahf/` 유지) | 2026-07-17 |
| `uahf/framework/adapters/claude/discovery-data/events/` brownfield-r001·greenfield-r002·greenfield-r003 (6파일) | `cd9247b` | evidence | v1.2 Discovery 검증·v1.7 Control Plane Greenfield Discovery 원장 | 2026-07-17 |
| `uahf/framework/adapters/claude/discovery-data/e2e-greenfield-project/` (전체) | `cd9247b` | ephemeral | Discovery E2E 작업 잔재 | 2026-07-17 |
| `uahf/framework/adapters/claude/loop-data/` (11파일) | `cd9247b` | evidence | v0.6~v1.0 데모·dogfooding 루프 사이클 원장 | 2026-07-17 |
| `uahf/framework/adapters/claude/orchestration-data/e2e/metrics/` (9파일) | `cd9247b` | evidence | Performance Baseline 측정 파생 산출물 (재산출 도구 = e2e/collect_metrics.py·verify_run.py 유지) | 2026-07-17 |
| 루트 `docs/` 완결 트랙 설계 문서 9파일 (v1.2.1-context-and-design·v1.2.1-migration-plan-draft·v1.2.1-repository-refactoring-brief·v1.3-context-and-design·v1.4-context-and-design·form-b-step-hosting-design·project-orchestration-design·performance-tuning-plan·baseline-performance-cost-analysis) | `cd9247b` | track-design | v1.2.1 재구성·v1.3·v1.4·v1.5 형태B·v1.6 Orchestration·Performance Tuning 트랙 설계·실측 정본 | 2026-07-17 |
| `uahf/docs/session-handoff-v0.1.md` ~ `session-handoff-v1.2.md` (12파일) | `004bfa9` | track-design | 세션 시간축 기록 — 정책 §6 제정 전(커밋 `1bd6948`) 삭제분의 소급 등재 | 2026-07-17 |
| `tms-system/` (7파일 — Contract v1·v2·SD 성숙 원장·SD policy 사본·solution-design.md·impl-plan.json·verify-impl-plan.py) | `4934bc8` | evidence | 외부 제품 테스트 트랙(운송주선 TMS) 종료 — Discovery→SD 성숙→impl-plan 6task 승격까지 파이프라인 실증 완수·구현 미착수(사용자 결정 2026-07-19: 테스트 목적 완수·삭제) | 2026-07-19 |
| `uahf/framework/adapters/claude/orchestration-data/runs/orch-tms-phase1-smoke/` (12파일) | `4934bc8` | evidence | tms Phase-1 프로덕션 실 run 원장 — project-orchestration-binding §5.7 실측 근거(앵커 전환 완료) | 2026-07-19 |
| `docs/backlog-k-delegation-b-ledger.md` (1파일) | `90ca19c` | evidence | 백로그 K·위임 규율 B-1/B-3/B-4·§5-A(per-unit timeout·N·M·O) 트랙 원장 — 등재 항목이 CP3 승인으로 종결됨(`uaf-verified:` 등재일에 원장 전문 정독 + `OPEN`·`미해소` 문자열 스윕 — 검색 범위 = 이 파일. 잔여 = B-4 실시간 전파 미해소·각 트랙 미검증 축 이월분이며 이들은 `docs/session-handoff.md` 이월 절로 승격되어 있다). 각 항목의 현행 정본은 `orchestration/adapters/claude/project-orchestration-binding.md` §3.3·§5.8 과 `docs/post-tuning-improvement-backlog.md` 해소 행이 소유 | 2026-07-26 |
| `docs/rca-prescriptions-ledger.md` (1파일) | `90ca19c` | evidence | UAF 자체 RCA 처방 5건 트랙 원장(W-hook·W-J·W-L) — 등재 항목이 Advisor CP2 Pass + CP3 로 종결됨(`uaf-verified:` 등재일에 원장 전문 정독 — 검색 범위 = 이 파일). 현행 정본 = `.claude/AGENT.md` §Invariants·`docs/verification-checklist.md` §5.7·§5.8·binding §3.4·§5.8 | 2026-07-26 |
| `docs/post-tuning-improvement-backlog.md` 해소 항목 9건의 상세 해소 서술 + 2026-07-14 Dogfooding Evidence 표 (문서는 live 유지·해소분 서술만 제거) | `90ca19c` | evidence | 항목 B·C·J·K·L·M·N·O·P 해소 경위·검증 근거 서술 및 v1.7 실사용 dogfooding 실측 표 — 해소분 정본은 각 바인딩 §가 소유하므로 백로그 파일에는 해소 1줄 요약만 유지 | 2026-07-26 |
| `docs/proportionality-track-w3-b-worker-1.md` (1파일) | `64ebd49` | evidence | 절차 비례화 W3-b 완료 보고 전문(보고-파일 역전 규약의 첫 셀프 적용 표본) — 미결 2건은 트랙 원장 §8.11 항 10·11로 승격 완료. 현행 규약 정본 = docs/delegation-protocol.md §2.2/§2.3/§3.2·역할 정의 3종 "출력" 절 | 2026-07-27 |
| `docs/proportionality-track-w4-worker-1.md` (1파일) | `b7294bc` | evidence | 절차 비례화 W4 완료 보고 전문 — 미결 4건(OQ-W4-1~4)은 트랙 원장 §6.3 항 8~10으로 승격 완료. 현행 정본 = discovery-binding §8.3·lightweight-policy.yaml·entry-registry 행 6 | 2026-07-27 |
| `docs/proportionality-track-w5-worker-1.md` (1파일) | `e802317` | evidence | 절차 비례화 W5 완료 보고 전문(E2E 8지점 로그·이탈 5건·미해소 전량 열거) — OQ 5건은 트랙 원장 헤더 실행 상태 항의 Advisor 판정으로 승격 완료 | 2026-07-27 |
| `docs/proportionality-track-ledger.md` (1파일) | `af57be0` | track-design+evidence | 절차 비례화 트랙 원장(분해 채택본·게이트 확정 표·Wave 1~5 실행 상태·브리프 7건·개정 유형 표 20행·근거 표 F-1~F-38) — 실행 완료로 아카이브. 잔여 미해소는 docs/session-handoff.md §B-2 승격. 현행 정본 = CLAUDE.md 레인 분기 절·lane-registry.json·binding §5.9·solution-design-binding §7A.2-S/L·discovery-binding §8.3·delegation-protocol §2.2/§3.2 | 2026-07-27 |
| `docs/wave0-history-governance-report.md` (1파일) | `64b6570` | evidence | 이력 거버넌스 전환 Wave 0 완료 보고 전문(r1~r5 재작업 경위·CP2 7/7·구 규범 잔존표 §6-A/B/C) — 현행 정본 = docs/spec-versioning-policy.md §3·루트 ARCHITECTURE.md §6 원칙 12 | 2026-07-27 |
| `docs/wave3-reaccum-guard-report.md` (1파일) | `2c3992b` | evidence | 이력 재퇴적 가드 Wave 3 완료 보고 전문(가드 5케이스·`--check` 3케이스 실측) — 검증 케이스 인용 1절은 Wave 2 일괄 적용에 스텁 전환된 상태로 앵커됨(해당 인용의 원 수치는 본문 §3에 잔존) | 2026-07-27 |
