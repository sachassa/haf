# UAF 시작하기 (Getting Started)

작성일: 2026-07-06
상태: v1.0 Baseline (개정 — stale 정합·이력 절 신설 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-07 · 직전 기준선: v0.9 Baseline)
상위 규약: .claude/AGENT.md
정본 포인터: ARCHITECTURE.md · ROADMAP.md · uahf/specs/ (Frozen) · uahf/framework/core/structure.md §8
성격: 신규 참여자 문서 진입점 — 정본을 재정의하지 않고 포인터로만 안내한다.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치

- 이 문서는 UAF에 처음 참여하는 사람이 **가장 먼저 읽는 안내**다. 프로젝트가 무엇인지, 어디에 무엇이 있는지, 세션을 어떻게 시작하는지를 가리킨다.
- **정본은 이 문서가 아니다.** 모든 계약·구조·절차의 정본은 아래 포인터가 가리키는 문서다. 이 문서는 요약·지도이며, 충돌 시 정본이 우선한다(재정의·확장 0). 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행 — ARCHITECTURE·Spec 충돌은 사용자 보고).
- 용어의 정본은 uahf/specs/00-glossary.md다. 이 문서는 새 용어를 만들지 않는다.

---

## §1. UAF는 무엇인가

- **UAHF와의 관계.** UAF는 프로젝트를 진입부터 실행까지 관통하는 6개 Layer(entry/discovery/planning/orchestration/knowledge/uahf)를 아우르는 상위 프레임워크다. 그중 **UAHF(Universal Agentic Harness Framework)**는 `uahf/` Layer — 파이프라인 하류에서 실행(Execution)을 담당하는 하네스 실행 Layer(구현체)다. UAF는 전체 프레임워크를, UAHF는 그 안의 한 Layer를 가리킨다(정본: ARCHITECTURE.md §0 · README.md — 재정의 아님).
- 정본: ARCHITECTURE.md (§1 Vision · §6 설계 원칙 · §2·§4 6 Layer + Memory Cross-cutting Service). UAHF 하네스 자체의 설계 원칙은 uahf/ARCHITECTURE.md §3 소관이다.

---

## §2. 6 Layer 구조 지도

프로젝트(UAF)의 최상위 물리 구조는 **6개 Layer**(진입→실행 파이프라인 5 + 횡단 knowledge)와 UAF 레벨 운용 문서(`docs/`)·환경 표면(`.claude/`)으로 나뉜다. 아래는 지도이며, 각 행은 정본을 **재정의하지 않고 포인터로만** 안내한다. 최상위 지도의 정본은 ARCHITECTURE.md §2(라우터·6 Layer)다.

| 자리 | 무엇이 있는가 | 정본 포인터 |
|---|---|---|
| `entry/` | 진입 / Entry Resolution Layer — UAF 공식 진입점·Discovery Request 산출. | ARCHITECTURE.md §2 · entry/ARCHITECTURE.md · entry/specs/01-entry.md |
| `discovery/` | Project Discovery Layer — Discovery Request(+증거) → Project Contract 컴파일. | ARCHITECTURE.md §2 · discovery/ARCHITECTURE.md · discovery/specs/02-discovery.md |
| `planning/` | Project Contract / Solution Design(설계 성숙 루프) Layer — UAF↔UAHF 유일 접점. | ARCHITECTURE.md §2·§3 · planning/ARCHITECTURE.md · planning/specs/03-project-contract.md · 04-solution-design.md |
| `orchestration/` | Project Orchestration Layer — 동적 작업 그래프·게이트·역할/모델 할당·산출물 계보(UAHF를 substrate로 소비). | ARCHITECTURE.md §2.3 · orchestration/ARCHITECTURE.md · orchestration/specs/05-project-orchestration.md |
| `knowledge/` | 횡단 Knowledge Base — 파이프라인 단계가 아니라 모든 Layer가 Consult하는 공용 Base. | ARCHITECTURE.md §4 · knowledge/ARCHITECTURE.md |
| `uahf/` | 하네스 실행 Layer(UAHF 구현체) — Core Contract 스펙(`uahf/specs/`)·framework 구현(`uahf/framework/`)·하네스 문서(`uahf/docs/`). | uahf/ARCHITECTURE.md · uahf/specs/00-glossary.md · uahf/framework/core/structure.md §8 |
| `docs/` | UAF 레벨 운용 문서 — 세션 핸드오프·검증 리포트·프로토콜·정책. | docs/session-handoff.md(최신 핸드오프) · docs/delegation-protocol.md 등 |
| `.claude/` | Agent 정의(`agents/`)·상위 규약(`AGENT.md`)·Advisor 진입점(`CLAUDE.md`)·확장 표면(`commands`·`hooks`·`skills/`) — 환경 의존(Adapter 경계·Global Default). | ARCHITECTURE.md §5 · .claude/AGENT.md |

---

## §3. 세션 진입 절차

새 세션은 항상 다음 순서로 착수한다(핸드오프 관행 — `docs/session-handoff.md` 최신 핸드오프).

1. **최신 핸드오프 정독** — `docs/session-handoff.md`(최신 핸드오프)를 읽는다. 이 문서가 세션 시작 정본이며, 직전 세션의 상태·결정을 담는다.
2. **Consult (Memory 회수)** — uahf/framework/adapters/claude/memory-binding.md §3.2 절차로 관련 Lessons·이전 결정을 목적·최소 범위로 회수한다.
3. **정본 정독** — ARCHITECTURE.md · ROADMAP.md(해당 버전 절) · 관련 specs · uahf/framework/core/structure.md §8.
4. **규약·프로토콜 확인** — .claude/AGENT.md · .claude/agents/ 4종 · docs/delegation-protocol.md · docs/verification-checklist.md.
5. **계획 수립·승인** — 실행 계획을 세워 사용자 승인을 받은 뒤 착수한다(구현 전 계획 — Advisor 관행).

- 빠른 상태 확인은 `.claude/commands/uahf-status.md`(현재 마일스톤·최신 핸드오프·하네스 상태·Consult 절차·다음 진입 절차 표면화)를 참고한다.

---

## §4. 핵심 문서 지도

| 주제 | 문서 |
|---|---|
| 비전·설계 원칙·아키텍처 | ARCHITECTURE.md |
| 개발 단계·버전·산출물 | ROADMAP.md |
| Core Contract 스펙 | uahf/specs/ (00-glossary ~ 13-harness + TEMPLATE.md, 15개) |
| 위임·보고 운용 프로토콜 | docs/delegation-protocol.md |
| 검증 체크리스트(게이트 A~D) | docs/verification-checklist.md |
| 역할 빠른 참조(Advisor·Planner·Worker·Verifier) | docs/roles-quick-reference.md |
| 세션 진입·직전 상태 | docs/session-handoff.md(최신 핸드오프) |
| framework 디렉터리 구조 | uahf/framework/core/structure.md §8 |

---

## §5. 설치 안내

- 신규 프로젝트 설치 가이드는 **uahf/docs/v0.9-install-guide.md@cd9247b**다 (v0.9 Baseline에서 확정 완료 — 산출물 수명 정책에 따라 작업 트리에서 아카이브; 열람: `git show cd9247b:uahf/docs/v0.9-install-guide.md`). 이 문서는 그 경로만 안내하며 내용을 인용하지 않는다.
- 설치·초기화의 계약 정본은 uahf/specs/12-scaffold.md다.
