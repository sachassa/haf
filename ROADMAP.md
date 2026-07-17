# Universal Agentic Framework — Roadmap

상태: v1.7 Baseline 확정 (첫 실제 신규 외부 소비 프로젝트 · 사용자 승인 2026-07-14) — 이 ROADMAP 문서 자체는 스텁이며 완전 저술은 후속 트랙

## 이 문서의 범위
root ROADMAP는 Framework 전체 로드맵을 담는다. Layer별 상세 로드맵은 각 Layer의 `ROADMAP.md`가 정본이다.

## Layer별 ROADMAP 포인터
- `entry/ROADMAP.md`
- `discovery/ROADMAP.md`
- `planning/ROADMAP.md`
- `uahf/ROADMAP.md` (UAHF 로드맵 정본)
- `knowledge/ROADMAP.md`
- `orchestration/ROADMAP.md`

## 현재 트랙
- v1.2 Baseline 확정 완료(UAHF, `uahf/`).
- v1.2.1 Repository Refactoring — **Baseline 확정** (구조 이동 완결 · 사용자 승인 2026-07-09): Phase 1(Layer 이동)·Phase 2(uaf 분할 → entry/discovery/planning)·Phase 3(runtime→uahf 승격). 커밋 e1b36c4·3951407·6764465.
- v1.3 Solution Design (마일스톤, 2026-07-13) — Discovery~UAHF 사이 성숙 활동의 아키텍처 정본 확립: `planning/specs/04-solution-design.md` 신설·03 v1.2·루트 ARCHITECTURE 문서버전 v1.4·planning ARCH 이중 책임·비정본 부록 2종(설계만·형태 A). 상세 = `uahf/ROADMAP.md` §3 v1.3 행·`docs/v1.3-context-and-design.md`. ※ 루트 ARCHITECTURE **문서 버전** v1.3과 별개 네임스페이스.
- v1.4 Solution Design Binding + Dogfooding E2E (마일스톤, 2026-07-13) — `solution-design-binding.md` 신설(UAF 레벨 바인딩 4종째)·`solution-design-data/` 백엔드·실제 pc-uahf-001 v1→v2 성숙 E2E 완주(사용자 승인 게이트 T8 실동작·v1 byte 불변·append-only 이벤트 로그). 파이프라인 Discovery→Contract v1→Solution Design→Contract v2→UAHF 실행 가능 연결 실증. 상세 = `uahf/ROADMAP.md` §3 v1.4 행·`docs/v1.4-context-and-design.md`.
- v1.5 형태 B Step Execution Hosting (마일스톤, 2026-07-13) — 형태 B 실행 코드 첫 도입: `uahf/framework/runtime/step-hosting-protocol.md`(provider-중립 계약·SH-INV 8)·중립 Step Host(`framework/loop/step-host/`·AI/provider 토큰 0)·claude 바인딩+invoker(dangerously 유일 소재). dogfooding E2E 7 시나리오 전건 실증 — 실 CLI 무인 구동·append-only run 데이터·게이트 등급 분리(unrestricted에서도 Human Decision Gate 정지)·deterministic resume·Full UAF/Standalone 진입 분기. Frozen spec 개정 0·형태 A 병존. 상세 = `uahf/ROADMAP.md` §3 v1.5 행·`docs/form-b-step-hosting-design.md`.
- v1.6 Project Orchestration / Dynamic Agent System (마일스톤, 2026-07-13) — UAF 레벨 신규 최상위 Layer `orchestration/` 신설(루트 §2.3 Agentic Runtime slot 실현·루트 ARCHITECTURE 문서버전 v1.5): `orchestration/specs/05-project-orchestration.md` 정본·중립 Orchestrator 6 모듈(`orchestration/framework/orchestrator/`)·Gate Policy 5종·Allocation/Model Selection·Artifact Registry·claude 바인딩(`project-orchestration-binding.md`)+`orchestration-data/`·실 CLI 축소판 종단 dogfooding E2E(시나리오 j)·OQ-SH-4 해소·테스트 165. CP2 5단계 전건 첫 판정 Pass(S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0)·사용자 승인. UAHF 6-Layer 무촉·UAHF 정본 substrate 라이브러리 무수정 소비·Frozen spec 개정 0. 상세 = `uahf/ROADMAP.md` §3 v1.6 행·`docs/project-orchestration-design.md`.

- v1.7 첫 실제 신규 외부 소비 프로젝트 + OQ-PO-B4 해소 (마일스톤, 2026-07-14) — UAF가 자기 파이프라인으로 외부 제품을 실제 생성: Entry `/new` 행1 → Greenfield Discovery(`greenfield-r003`·질문 루프 실 사용자·G2) → `C:\my-claude-project\uahf-control-plane\` 신설(Contract v1 관례 배치·Scaffold 첫 실 설치 27산출물) → **첫 orchestration 형태 B 호스팅 성숙 run**(`maturation-r003`+`orch-m-maturation-cp` — 05 §3.7 실현·역할 동적 할당 2종·독립 제안·Wireframe 사용자 수정 요구 task_superseded·Reconcile·Integrated Review·T8) → Contract v2 발행 → **OQ-PO-B4 해소**(`orch-w-impl-cp` — 실 LLM 제안 step 4-task 계획·픽스처 0·실 CLI 16세션·수동 코딩 0) → Next.js MVP 대시보드 실동작(빌드 통과·실데이터 3라우트 200). 선행 W0 스모크 = 시나리오 k(`orch-k-nonfixture-smoke` — 실 LLM 제안·실 사용자 게이트·외부 워크스페이스 실증). CP2 총 8회 전건 Pass·사용자 게이트 6회 전부 실 해소·시뮬레이션 라벨 0. UAHF 정본 무수정(드라이버는 orchestration-data/e2e 격리 지점·신규 파일만). 상세 = `docs/next-session-prompt.md@ad451ee`(v1.7 마감본 — `git show ad451ee:docs/next-session-prompt.md`로 열람)·플랜 `typed-skipping-turtle`.

## 이 문서의 지위
스텁이다. 내용은 후속 트랙에서 완전 저술된다.
