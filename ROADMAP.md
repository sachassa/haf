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

## 완료 마일스톤 (1행 요약)

경위·Δ·검증 판정 수치는 이 표에 옮기지 않는다 — 각 행의 **상세 좌표** 칸이 실재 정본을 행별로 지정한다.

| 마일스톤 | 완료 | 한 줄 산출물 | 상세 좌표 |
|---|---|---|---|
| v1.2 Baseline (UAHF) | — | UAHF 기준선 확정(`uahf/`). | `uahf/ROADMAP.md` §3 v1.2 행 |
| v1.2.1 Repository Refactoring | 2026-07-09 | Layer 중심 구조 이동 3 Phase — uaf 분할 → entry/discovery/planning · runtime→uahf 승격. | git 커밋 e1b36c4·3951407·6764465 (`uahf/ROADMAP.md` §3에 행 없음) |
| v1.3 Solution Design | 2026-07-13 | `planning/specs/04-solution-design.md` 신설 — Discovery~UAHF 사이 성숙 활동의 정본 확립. | `uahf/ROADMAP.md` §3 v1.3 행 |
| v1.4 SD Binding + Dogfooding E2E | 2026-07-13 | `solution-design-binding.md`+`solution-design-data/` · Contract v1→v2 성숙 E2E 완주. | `uahf/ROADMAP.md` §3 v1.4 행 |
| v1.5 형태 B Step Execution Hosting | 2026-07-13 | 실행 코드 첫 도입 — 중립 Step Host + provider-중립 계약(SH-INV 8). | `uahf/ROADMAP.md` §3 v1.5 행 |
| v1.6 Project Orchestration | 2026-07-13 | 최상위 Layer `orchestration/` 신설(루트 ARCHITECTURE §2.3 slot 실현)·정본 `orchestration/specs/05-project-orchestration.md`. | `uahf/ROADMAP.md` §3 v1.6 행 · `orchestration/ARCHITECTURE.md` §9 |
| v1.7 첫 외부 소비 프로젝트 | 2026-07-14 | UAF 자기 파이프라인으로 외부 제품 생성(`uahf-control-plane`) · OQ-PO-B4 해소. | `docs/next-session-prompt.md@ad451ee` (v1.7 마감본 — 열람: `git show ad451ee:docs/next-session-prompt.md`) |

압축으로 걷어낸 서술의 직전 원문은 git 앵커 90ca19c에서 열람한다.

## 현재 트랙
v1.7 Baseline 이후는 하네스 결함·처방 트랙과 소비 제품 트랙이 병행한다. 진행 상태의 단일 live 정본은 `docs/session-handoff.md`이며, 이 ROADMAP는 마일스톤 축만 담는다.

## 이 문서의 지위
스텁이다. 내용은 후속 트랙에서 완전 저술된다.
