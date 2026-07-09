# UAHF 시작하기 (Getting Started)

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

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, verification-checklist.md §9 동형. 이후 개정은 이 표에 append-only로 기록한다. §9는 신설 편의 번호이며 신설로 기존 §0~§5 번호·문면은 불변이다.)

---

## §0. 이 문서의 위치

- 이 문서는 UAHF에 처음 참여하는 사람이 **가장 먼저 읽는 안내**다. 프로젝트가 무엇인지, 어디에 무엇이 있는지, 세션을 어떻게 시작하는지를 가리킨다.
- **정본은 이 문서가 아니다.** 모든 계약·구조·절차의 정본은 아래 포인터가 가리키는 문서다. 이 문서는 요약·지도이며, 충돌 시 정본이 우선한다(재정의·확장 0). 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행 — ARCHITECTURE·Spec 충돌은 사용자 보고).
- 용어의 정본은 uahf/specs/00-glossary.md다. 이 문서는 새 용어를 만들지 않는다.

---

## §1. UAHF는 무엇인가

Universal Agentic Harness Framework(UAHF)는 AI 에이전트를 위한 범용 Development Operating System이다 — 특정 AI 모델이나 개발 환경에 종속되지 않는, 재사용 가능한 Agentic Development Framework를 목표로 한다. "설계 → 구현 → 검증 → 학습"이 자동으로 반복되고, 프로젝트가 커질수록 안정적으로 동작하며 실패를 학습해 시간이 지날수록 더 똑똑해지는 것을 지향한다.

- 정본: ARCHITECTURE.md (§1 Vision · §3 설계 원칙 · §5 6 Layer + Memory Cross-cutting Service).
- 설계 원칙 6종(ARCHITECTURE §3): AI Agnostic · Modular · Agent First · Verify Everything · Learn from Failure · Token Efficiency.

---

## §2. 4경계 구조 지도

프로젝트는 크게 네 자리로 나뉜다. 아래는 지도이며, `uahf/framework/` 내부 경계의 정본 트리는 uahf/framework/core/structure.md §8이다.

| 자리 | 무엇이 있는가 | 정본 포인터 |
|---|---|---|
| `uahf/specs/` | Core Contract 스펙 — Frozen 기준선. `00-glossary.md`(용어 정본)부터 `13-harness.md`까지 번호 스펙 14개 + `TEMPLATE.md` = **15개**. 계약의 최종 정본. | uahf/specs/00-glossary.md · 각 spec |
| `uahf/framework/` | 4경계: `core/`(계약·스키마 문서)·`runtime/`(모듈 시스템·수명주기 문서)·Module 구현 디렉터리(`loop`·`memory`·`verifier`·`workflow`·`plugins/`)·`adapters/<adapter>/`(환경 의존 바인딩 격리). | uahf/framework/core/structure.md §8 (정본 트리) |
| `docs/` | 운용 문서 — 세션 핸드오프·검증 리포트·시연 기록·프로토콜·정책. | uahf/docs/session-handoff-v0.X.md(최신본) 등 |
| `.claude/` | Agent 정의(`agents/` 4종)·상위 규약(`AGENT.md`)·Advisor 진입점(`CLAUDE.md`)·확장 표면(`commands`·`hooks`·`skills/`) — 환경 의존(Adapter 경계). | .claude/AGENT.md · uahf/specs/11-adapters.md |

- Core 경계(`uahf/framework/core`·`uahf/framework/runtime`)와 Module 구현 디렉터리의 문서 본문은 특정 AI·언어·툴체인 토큰 0건을 유지하고, 환경 의존 토큰은 `uahf/framework/adapters/`와 `.claude/`로 격리된다(structure.md §5, ARCHITECTURE §3.1 AI Agnostic).

---

## §3. 세션 진입 절차

새 세션은 항상 다음 순서로 착수한다(핸드오프 관행 — 최신 uahf/docs/session-handoff-v0.X.md §4 Bootstrap Prompt).

1. **최신 핸드오프 정독** — `uahf/docs/session-handoff-v0.X.md`에서 가장 높은 N의 문서를 읽는다. 이 문서가 세션 시작 정본이며, 직전 세션의 상태·결정을 담는다.
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
| 세션 진입·직전 상태 | uahf/docs/session-handoff-v0.X.md(최신본) |
| framework 디렉터리 구조 | uahf/framework/core/structure.md §8 |

---

## §5. 설치 안내

- 신규 프로젝트 설치 가이드는 **uahf/docs/v0.9-install-guide.md**다 (v0.9 Baseline에서 확정 완료). 이 문서는 그 경로만 안내하며 내용을 인용하지 않는다.
- 설치·초기화의 계약 정본은 uahf/specs/12-scaffold.md다.

---

이 문서는 지도다. 상세·정본은 위 포인터를 따른다. 충돌 시 정본이 우선하며, 충돌을 발견하면 Advisor에게 보고한다.
