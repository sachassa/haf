# orchestration — Roadmap (프로젝트 오케스트레이션 Layer)

상태: v1.6 Baseline (CP2 5단계 전건 첫 판정 Pass — S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0 · CP3 승인 · 사용자 승인 2026-07-13)
상위: Universal Agentic Framework (root README/ARCHITECTURE 참조)

## 역할
orchestration Layer의 로드맵을 담는다. 전체 Framework 로드맵(root ROADMAP)의 orchestration 축(루트 §2.3 Agentic Runtime slot 실현)을 상세화한다.

## 정본 포인터
정본: `orchestration/specs/05-project-orchestration.md` · 개관 = `orchestration/ARCHITECTURE.md` · 설계 정본 = `docs/project-orchestration-design.md` · 상위 로드맵 = root `ROADMAP.md`.

## 현재
- **v1.6 Baseline (완결, 2026-07-13):** S1~S5 전 단계 완료 — 사용자 승인·번호 v1.6 부여. CP2 5단계 전건 첫 판정 Pass(S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0)·CP3 승인. 커밋 사슬: fd112cd→ce0cdba→c65d20f→04b8f6e→745f26e→5e843dc.
  - **S1** Layer 골격 + spec 정본(`orchestration/ARCHITECTURE.md`·`orchestration/specs/05-project-orchestration.md`·본 ROADMAP 신설·배치 재검증 게이트 확정). CP2 8/0/0 · 커밋 fd112cd.
  - **S2** Graph Revision Ledger + 중립 Orchestrator 드라이버(`orchestration/framework/orchestrator/`). CP2 7/0/0 · 커밋 ce0cdba.
  - **S3** Gate Policy 5종 평가기 + 게이트 큐 파생 뷰 + 제시 채널 바인딩(부분). CP2 10/0/0 · 커밋 c65d20f(바이트코드 정리 04b8f6e).
  - **S4** Dynamic Allocation·Model Selection·OQ-SH-4 해소·CP3 비-Pass 정지. CP2 9/0/0 · 커밋 745f26e.
  - **S5** Artifact Registry + 바인딩 완성 + 실 CLI 축소판 종단 dogfooding(테스트 165). CP2 9/0/0 · 커밋 5e843dc.
  - 단계별 산출·E2E 시나리오 정본 = `docs/project-orchestration-design.md` §5.

## 이 문서의 지위
S1~S5 완결로 Layer 산출물이 실재화되었다(중립 Orchestrator 모듈·claude 바인딩·`orchestration-data/` run 데이터). 루트 라우터 등재(`orchestration/` 1행)는 v1.6 Baseline 승격과 함께 완료되었다(루트 `ARCHITECTURE.md` v1.5 §2.1 라우터 표·문서버전 상승). 단계별 상세·E2E 시나리오 정본은 `docs/project-orchestration-design.md` §5다.
