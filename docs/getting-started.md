# UAF 시작하기 (Getting Started)

작성일: 2026-07-06
상태: v1.0 Baseline (개정 — stale 정합·이력 절 신설 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-07 · 직전 기준선: v0.9 Baseline)
상위 규약: .claude/AGENT.md
정본 포인터: ARCHITECTURE.md · ROADMAP.md · uahf/specs/ (Frozen) · uahf/framework/core/structure.md §8
성격: 신규 참여자 문서 진입점 — 정본을 재정의하지 않고 포인터로만 안내한다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.9 Baseline | 최초 작성(v0.9 Task T5) — 신규 참여자 진입점. (이력 절은 v1.0 T8b에서 사후 신설 — 일자·주체는 문서 머리 자기 선언 기준, L-07) | Worker (v0.9 Task T5) |
| 2026-07-06 | v1.0 Draft (개정 — stale 정합·이력 절 신설) | (변경 요약: line 47 괄호 예시 제거·line 74 시제 정합·전수 대조 결과·이월 후보 #8 해소) | Worker (Advisor 위임, Task T8b) |
| 2026-07-07 | v1.0 Baseline | v1.0 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 21/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | v1.0 (정합 — UAF 승격·버전 무상승) | UAF 승격 위계 정합 — 제목·§0·§1의 "UAHF=전체" 서술을 UAF 기준으로 정정(UAHF=`uahf/` 하네스 실행 Layer 위계 반영), §2 구조 지도를 "4경계" → 6 Layer(entry/discovery/planning/orchestration/knowledge/uahf) + `docs/` + `.claude/`로 재작성(정본 포인터 전용·재정의 0), handoff 포인터 4곳을 삭제된 session-handoff-v0.X → `docs/next-session-prompt.md`로 교체. §0~§5 규범 논지·기존 정본 포인터(ARCHITECTURE §1·§3·§5) 유지·새 정의 창설 0. (사용자 결정) | Worker (Advisor 위임, Wave 1 W6) |
| 2026-07-17 | v1.0 (정합 — anchor 정합) | §1 정본 포인터 라인(:37)의 stale § 앵커 정정 — 설계 원칙 §3→§6·6 Layer(+Memory Cross-cutting Service) §5→§2·§4(루트 ARCHITECTURE.md 현행 § 실측 정합). §1 Vision·기타 부분 무촉. | Worker (Advisor 위임, Wave 2 W4) |
| 2026-07-17 | v1.0 (정합 — 설계 원칙 라인) | §1 설계 원칙 라인 정정 — "6종(ARCHITECTURE §3)"(UAHF 하네스 원칙 목록의 오전사)을 루트 현행 "10종(§6)" 목록으로 교체, UAHF 자체 6종은 uahf/ARCHITECTURE.md §3 소관으로 병기(루트 §6 실측 정합). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, verification-checklist.md §9 동형. 이후 개정은 이 표에 append-only로 기록한다. §9는 신설 편의 번호이며 신설로 기존 §0~§5 번호·문면은 불변이다.)

---

## §0. 이 문서의 위치

- 이 문서는 UAF에 처음 참여하는 사람이 **가장 먼저 읽는 안내**다. 프로젝트가 무엇인지, 어디에 무엇이 있는지, 세션을 어떻게 시작하는지를 가리킨다.
- **정본은 이 문서가 아니다.** 모든 계약·구조·절차의 정본은 아래 포인터가 가리키는 문서다. 이 문서는 요약·지도이며, 충돌 시 정본이 우선한다(재정의·확장 0). 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행 — ARCHITECTURE·Spec 충돌은 사용자 보고).
- 용어의 정본은 uahf/specs/00-glossary.md다. 이 문서는 새 용어를 만들지 않는다.

---

## §1. UAF는 무엇인가

Universal Agentic Framework(UAF)는 AI 에이전트를 위한 범용 Development Operating System을 지향하는 **전체 프레임워크**다 — 특정 AI 모델이나 개발 환경에 종속되지 않는, 재사용 가능한 Agentic Development Framework를 목표로 한다. "설계 → 구현 → 검증 → 학습"이 자동으로 반복되고, 프로젝트가 커질수록 안정적으로 동작하며 실패를 학습해 시간이 지날수록 더 똑똑해지는 것을 지향한다.

- **UAHF와의 관계.** UAF는 프로젝트를 진입부터 실행까지 관통하는 6개 Layer(entry/discovery/planning/orchestration/knowledge/uahf)를 아우르는 상위 프레임워크다. 그중 **UAHF(Universal Agentic Harness Framework)**는 `uahf/` Layer — 파이프라인 하류에서 실행(Execution)을 담당하는 하네스 실행 Layer(구현체)다. UAF는 전체 프레임워크를, UAHF는 그 안의 한 Layer를 가리킨다(정본: ARCHITECTURE.md §0 · README.md — 재정의 아님).
- 정본: ARCHITECTURE.md (§1 Vision · §6 설계 원칙 · §2·§4 6 Layer + Memory Cross-cutting Service).
- 설계 원칙 10종(ARCHITECTURE §6): AI-Agnostic · Stable Contract · Stable Core · Layer Separation · Dependency Direction · Event Driven · Capability First · Policy as Data · Future Extensibility · Knowledge Consult. (UAHF 하네스 자체의 설계 원칙 6종은 uahf/ARCHITECTURE.md §3 소관.)

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
| `docs/` | UAF 레벨 운용 문서 — 세션 핸드오프·검증 리포트·프로토콜·정책. | docs/next-session-prompt.md(최신 핸드오프) · docs/delegation-protocol.md 등 |
| `.claude/` | Agent 정의(`agents/`)·상위 규약(`AGENT.md`)·Advisor 진입점(`CLAUDE.md`)·확장 표면(`commands`·`hooks`·`skills/`) — 환경 의존(Adapter 경계·Global Default). | ARCHITECTURE.md §5 · .claude/AGENT.md |

- 6 Layer 중 `entry/·discovery/·planning/·orchestration/·uahf/`는 진입→실행 파이프라인을 이루고, `knowledge/`는 그 위를 횡단하는 공용 Base다(ARCHITECTURE §2·§4). UAHF의 Core 경계 문서 본문은 특정 AI·언어·툴체인 토큰 0건을 유지하고, 환경 의존 토큰은 `uahf/framework/adapters/`와 `.claude/`로 격리된다(structure.md §5, ARCHITECTURE §6 AI Agnostic).

---

## §3. 세션 진입 절차

새 세션은 항상 다음 순서로 착수한다(핸드오프 관행 — `docs/next-session-prompt.md` 최신 핸드오프).

1. **최신 핸드오프 정독** — `docs/next-session-prompt.md`(최신 핸드오프)를 읽는다. 이 문서가 세션 시작 정본이며, 직전 세션의 상태·결정을 담는다.
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
| 세션 진입·직전 상태 | docs/next-session-prompt.md(최신 핸드오프) |
| framework 디렉터리 구조 | uahf/framework/core/structure.md §8 |

---

## §5. 설치 안내

- 신규 프로젝트 설치 가이드는 **uahf/docs/v0.9-install-guide.md**다 (v0.9 Baseline에서 확정 완료). 이 문서는 그 경로만 안내하며 내용을 인용하지 않는다.
- 설치·초기화의 계약 정본은 uahf/specs/12-scaffold.md다.

---

이 문서는 지도다. 상세·정본은 위 포인터를 따른다. 충돌 시 정본이 우선하며, 충돌을 발견하면 Advisor에게 보고한다.
