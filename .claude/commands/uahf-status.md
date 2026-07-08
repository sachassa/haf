---
description: UAHF 하네스의 현재 상태(현재 마일스톤·최신 세션 핸드오프·하네스 상태·Memory Consult 절차·다음 진입 절차)를 정본 포인터로 표면화한다.
---

# /uahf-status — UAHF 하네스 상태 표면화 (Presentation 진입 명령)

작성일: 2026-07-06
상태: v0.9 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: .claude/AGENT.md
성격: Presentation 진입 명령 — 형태 A(문서 명령), 실행 코드 0 (사용자 결정 DP-U1)

---

## §0. 이 명령의 위치와 성격

- 이 파일은 `.claude/commands/` 아래의 **Presentation 진입 표면**이다 — 확장 Module 표면(BP-6 확장). 계약 표면: specs/01-runtime.md §4.1("확장 Module 표면 = `.claude/commands/`") · framework/adapters/claude/runtime-binding.md §2 #3. `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰의 사용이 허용된다(framework/core/structure.md §2 Adapter 경계).
- **형태 A(문서 명령) — 실행 코드 0.** 이 명령은 실행 스크립트를 포함하지 않는다(사용자 결정 DP-U1). 호출 시 아래 항목을 **정본에서 회수해 표면화**하도록 안내하는 문서다. (`형태 A/B`는 structure.md §4 서술 라벨이다.)
- **정본 재정의 0.** 이 문서는 어떤 상태 값·계약도 스스로 확정하지 않는다. 아래 모든 항목은 **정본 포인터**로만 안내하며, 실제 값은 정본(특히 최신 세션 핸드오프)에서 회수한다. 값을 하드코딩하지 않으므로 상태가 진행돼도 이 명령은 낡지 않는다.

---

## §1. 목적

호출 시 하네스의 **현재 상태**를 한자리에 표면화한다 — "지금 어디까지 왔고, 이어서 무엇을 읽어야 하는가"를 가리킨다.

---

## §2. 표면화 항목 (invoke 시 표면화)

호출되면 다음을 순서대로 표면화한다. 각 항목은 **정본(라이브)에서 회수**하며, 아래 "작성 시점 스냅샷"은 실측 근거일 뿐 라이브 정본이 우선한다(L-07 — 상태 서술은 실측 후, 값은 정본에서 회수).

1. **현재 마일스톤.**
   - 정본(라이브): 최신 `docs/session-handoff-v0.X.md`의 상태 라인 + §3(다음 세션에서 수행할 작업 / 다음 트랙).
   - 회수 절차: `docs/`에서 가장 높은 N의 `session-handoff-v0.X.md`를 연다 — 그 문서가 세션 시작 정본이다.
   - 작성 시점 스냅샷(2026-07-06, 직접 실측): 최신본 = `docs/session-handoff-v0.8.md` — 직전 완료 **v0.8 (Extension System — Hooks·Skills·Plugins)**, 그 핸드오프가 지목한 다음 트랙 = **v0.9 (Adapter Layer & Scaffold)**. ※ 스냅샷일 뿐이다 — 실제 최신본을 `docs/`에서 확인하라.

2. **최신 세션 핸드오프 위치.**
   - `docs/session-handoff-v0.X.md`의 최신본(최고 N). 이 문서만 읽어도 다음 마일스톤을 이어갈 수 있게 작성된다(핸드오프 관행).
   - 작성 시점 최신 = `docs/session-handoff-v0.8.md`(스냅샷).

3. **하네스 상태.**
   - **Bootstrap** (specs/13-harness.md §3.2-B). 다수 표면이 정식 실행 Module이 아니라 규약 문서·관행으로 실현된다(형태 A). 실행 코드 표면(형태 B)은 도입 시 구분된다.
   - 실행 환경 실현 판정(완전성·불변·루프 통과)의 자리: framework/adapters/claude/adapter-conformance.md(Conformance Report).

4. **Memory Consult 절차 포인터.**
   - 착수 전 관련 Lessons·이전 결정·컨텍스트 회수: **framework/adapters/claude/memory-binding.md §3.2**(Recall 물리 절차 — index-first, scope 내 대상만 로드). 목적을 명시하고 최소 범위로 회수한다(Token Efficiency — specs/04-memory.md §3.3 INV-3/INV-4).
   - 회수 대상 집합의 현재 규모(Active Lesson·Best Practice 건수 등)는 최신 핸드오프의 Memory 실사용 절에서 회수한다(값 하드코딩 안 함).

5. **다음 진입 절차.**
   - 최신 `docs/session-handoff-v0.X.md` §4(Bootstrap Prompt 관행): 최신 핸드오프 정독 → Consult(Memory 회수) → 정본 정독(ARCHITECTURE.md·ROADMAP.md·관련 specs·structure.md §8) → .claude/AGENT.md·.claude/agents/ 4종·docs/delegation-protocol.md·docs/verification-checklist.md 확인 → 계획 수립·사용자 승인 후 착수.
   - 신규 참여자는 먼저 `docs/getting-started.md`를 읽는다.

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선한다.

| 표면화 항목 | 정본 (가리키기만 함) |
|---|---|
| 현재 마일스톤 / 최신 핸드오프 | 최신 `docs/session-handoff-v0.X.md` (상태 라인·§3) |
| 로드맵·버전 개요 | `ROADMAP.md` |
| 하네스 상태(Bootstrap) | `specs/13-harness.md` §3.2-B |
| 실행 환경 실현 판정 | `framework/adapters/claude/adapter-conformance.md` |
| Memory Consult 절차 | `framework/adapters/claude/memory-binding.md` §3.2 |
| 진입 절차 | 최신 `docs/session-handoff-v0.X.md` §4 |
| 신규 참여자 안내 | `docs/getting-started.md` |
| Presentation 표면 계약 | `specs/01-runtime.md` §4.1 · `framework/adapters/claude/runtime-binding.md` §2 #3 |
| 용어 | `specs/00-glossary.md` |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다. 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행).
