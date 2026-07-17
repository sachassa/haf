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
