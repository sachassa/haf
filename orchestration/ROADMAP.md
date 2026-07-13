# orchestration — Roadmap (프로젝트 오케스트레이션 Layer)

상태: S1 확정 스텁 (CP2 Pass 8/0/0 · CP3 승인 2026-07-13 — Layer 신설 산출물·완전 저술은 후속 단계)
상위: Universal Agentic Framework (root README/ARCHITECTURE 참조)

## 역할
orchestration Layer의 로드맵을 담는다. 전체 Framework 로드맵(root ROADMAP)의 orchestration 축(루트 §2.3 Agentic Runtime slot 실현)을 상세화한다.

## 정본 포인터
정본: `orchestration/specs/05-project-orchestration.md` · 개관 = `orchestration/ARCHITECTURE.md` · 설계 정본 = `docs/project-orchestration-design.md` · 상위 로드맵 = root `ROADMAP.md`.

## 현재
- **S1 (완료, 2026-07-13):** Layer 골격 + spec 정본 저술. `orchestration/ARCHITECTURE.md` + `orchestration/specs/05-project-orchestration.md` + 본 ROADMAP 신설. 배치 재검증 게이트 확정(UAF 레벨 신규 Layer·UAHF substrate 라이브러리 무수정 소비). CP2 첫 판정 Pass 8/0/0 · CP3 승인. 상세 = `docs/project-orchestration-design.md` §5.
- **S2~S5 (예정):** 중립 Orchestrator 모듈(`orchestration/framework/orchestrator/`) + Revision Ledger·Gate Policy·Allocation·Model Selection·Artifact Registry + Adapter 바인딩(`uahf/framework/adapters/<adapter>/project-orchestration-binding.md`) + dogfooding E2E. Baseline 승격은 S5 후 사용자 게이트. 단계별 산출·E2E 시나리오 정본 = `docs/project-orchestration-design.md` §5.

## 이 문서의 지위
스텁이다. 내용은 후속 단계(S2~S5)에서 완전 저술된다. 루트 라우터 등재(`orchestration/` 1행)는 트랙 종단 별도 결정(루트 문서버전 상승·사용자 게이트)이다.
