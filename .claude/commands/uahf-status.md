---
description: UAHF 하네스의 현재 상태(현재 마일스톤·최신 세션 핸드오프·하네스 상태·Memory Consult 절차·다음 진입 절차)를 정본 포인터로 표면화한다.
---

# /uahf-status — UAHF 하네스 상태 표면화 (Presentation 진입 명령)

상태: v0.9 Baseline · 2026-07-26 형태 B 로더 도입
상위 규약: .claude/AGENT.md

---

## §0. 이 명령의 위치와 성격

- **Presentation 진입 표면** — 확장 Module 표면(계약 = uahf/specs/01-runtime.md §4.1 · uahf/framework/adapters/claude/runtime-binding.md §2 #3). `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰 사용이 허용된다(structure.md §2).
- **형태 A(문서 명령) — 실행 코드 0 · 정본 재정의 0.** 상태 값·계약을 스스로 확정하지 않고, 아래 항목을 정본(특히 최신 세션 핸드오프)에서 회수해 표면화하도록 안내한다.
- **형태 A/B 공존(2026-07-26 추가).** 이 파일 자체는 여전히 실행 코드 0이며, 표면화 판독은 (i) 형태 B 로더 `adapters/claude/uahf_status.py`(권장 경로 — §2) 또는 (ii) 주 세션이 §2 절차를 직접 실수행하는 형태 A 폴백으로 실현된다. 두 경로의 표면화 항목 계약은 동일하다(structure.md §7 C-1 동형).

---

## §1. 목적

호출 시 하네스의 **현재 상태**를 한자리에 표면화한다 — "지금 어디까지 왔고, 이어서 무엇을 읽어야 하는가"를 가리킨다.

---

## §2. 표면화 항목 (invoke 시 표면화)

### 형태 B 로더 호출 (권장 경로)

```
PYTHONIOENCODING=utf-8 python adapters/claude/uahf_status.py
```

- 로더는 LLM 을 호출하지 않는 **결정적·읽기 전용 판독**이다 — git 상태(브랜치·HEAD) + `docs/session-handoff.md` 의 머리 지위 줄·§A 첫 요약 문단·★ 다음 착수 순위 블록·§B 하위 절 목록·§DC 잔여 유무·§D 정본 포인터 표 + `ARCHIVE.md` 데이터 행 수를 heading 기반으로 추출해 방출한다. 핸드오프 전문을 정독하는 LLM 턴을 제거한다(선례 = `entry/adapters/claude/entry_resolve.py`).
- 값을 하드코딩하지 않는다 — 추출원은 라이브 정본이며 문서 문면이 바뀌면 출력도 따라 바뀐다(재정의 0).
- **fail-soft** — 절·파일이 부재해도 크래시하지 않고 폴백 줄을 출력하며 종료 코드는 0이다. 폴백 줄이 보이면 해당 항목만 원본 직접 정독으로 메운다. 경로 재정의 = `UAHF_STATUS_HANDOFF`·`UAHF_STATUS_ARCHIVE`·`UAHF_STATUS_ROOT`.
- **형태 A 폴백 공존** — 로더가 가용하지 않으면 아래 절차(형태 A)를 주 세션이 직접 실수행한다.
- `uaf-verified:` 로더 동작은 이 저장소 실행으로 실측했다(정상 판독 exit 0·부재 경로 지정 시 fail-soft exit 0). 검사 범위 = 이 저장소의 현행 `docs/session-handoff.md`·`ARCHIVE.md` 문면 1부이며, 다른 heading 관행의 문서에 대한 일반 보장은 아니다.

### 형태 A 절차 (로더 미가용 시 폴백)

호출되면 다음을 순서대로 표면화한다. 각 항목은 **정본(라이브)에서 회수**한다.

1. **현재 마일스톤.**
   - 정본(라이브): `docs/session-handoff.md`(최신 핸드오프)의 상태 라인 + 다음 세션에서 수행할 작업 / 다음 트랙.
   - 회수 절차: `docs/session-handoff.md`를 연다 — 그 문서가 세션 시작 정본이다.

2. **최신 세션 핸드오프 위치.**
   - `docs/session-handoff.md`. 이 문서만 읽어도 다음 마일스톤을 이어갈 수 있게 작성된다(핸드오프 관행).

3. **하네스 상태.**
   - **Bootstrap** (uahf/specs/13-harness.md §3.2-B). 다수 표면이 정식 실행 Module이 아니라 규약 문서·관행으로 실현된다(형태 A). 실행 코드 표면(형태 B)은 도입 시 구분된다.
   - 실행 환경 실현 판정(완전성·불변·루프 통과)의 자리: uahf/framework/adapters/claude/adapter-conformance.md(Conformance Report).

4. **Memory Consult 절차 포인터.**
   - 착수 전 관련 Lessons·이전 결정·컨텍스트 회수: **uahf/framework/adapters/claude/memory-binding.md §3.2**(Recall 물리 절차 — index-first, scope 내 대상만 로드). 목적을 명시하고 최소 범위로 회수한다(Token Efficiency — uahf/specs/04-memory.md §3.3 INV-3/INV-4).
   - 회수 대상 집합의 현재 규모(Active Lesson·Best Practice 건수 등)는 최신 핸드오프의 Memory 실사용 절에서 회수한다(값 하드코딩 안 함).

5. **다음 진입 절차.**
   - `docs/session-handoff.md`·auto-memory 트랙(Bootstrap Prompt 관행): 최신 핸드오프 정독 → Consult(Memory 회수) → 정본 정독(ARCHITECTURE.md·ROADMAP.md·관련 specs·structure.md §8) → .claude/AGENT.md·.claude/agents/ 4종·docs/delegation-protocol.md·docs/verification-checklist.md 확인 → 계획 수립·사용자 승인 후 착수.
   - 신규 참여자는 먼저 `docs/getting-started.md`를 읽는다.

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선한다.

| 표면화 항목 | 정본 (가리키기만 함) |
|---|---|
| 현재 마일스톤 / 최신 핸드오프 / 진입 절차 | `docs/session-handoff.md` |
| 로드맵·버전 개요 | `ROADMAP.md` |
| 신규 참여자 안내 | `docs/getting-started.md` |
| Presentation 표면 계약 | `uahf/specs/01-runtime.md` §4.1 · `uahf/framework/adapters/claude/runtime-binding.md` §2 #3 |
| 용어 | `uahf/specs/00-glossary.md` |
| 형태 B 로더 (판독 실행체) | `adapters/claude/uahf_status.py` |
| 거버넌스 실행 스크립트 물리 홈 | 루트 `ARCHITECTURE.md` §5 |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다. 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행).
