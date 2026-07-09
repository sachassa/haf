# UAHF Session Handoff — v0.4 → 다음 세션

작성일: 2026-07-06
작성자: Advisor (v0.4 세션)
목적: 이 문서만 읽어도 새 세션이 다음 마일스톤을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v0.3.md, v0.2, v0.1)

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v0.4 — Memory & Lessons, Track A)

1. **Execution Plan 수립** — Planner 초안(9 Task·6 Wave) → Advisor 채택(OQ 3건 결정) → 사용자 승인. 형태 A(규격 문서+프로토콜, 실물 파일 연산 시연) 유지, C-1~C-3 계속 적용.
2. **Wave 실행 (M1~M9, 9 Task·6 Wave)** — 경계 개정(M1: structure.md에 Module 구현 디렉터리 경계 추가) → 병렬 3종: Port 계약+Manifest / Store·Index 규격 / Lessons 규칙(M2·M3·M4) → 병렬 2종: Adapter 바인딩 / 시연 절차서(M5·M6) → 시연 수행+실데이터 등록(M7) → Verifier 독립 검증(M8) → 핸드오프(M9, Advisor 직접). 위임·검증은 확립 관행(delegation-protocol / verification-checklist 게이트 A~D) 그대로.
3. **시연 6종 완주 (실물 파일 연산)** — ⓞ 초기 실데이터 등록·승격(Lesson 8건 Register→Advisor 승인 참조 첨부→Active) / ⓐ 실패→Lesson→회수 사이클(applicability 매칭 최소 집합 {L-06} 1건, 기본 detail=index) / ⓑ 회수 정책 거부 3케이스(MissingPurpose·MissingScope·UnboundedScope)+기본 index / ⓒ 승격 권한 차단(NotApproved 음성) / ⓓ 재발 판정 3분류(Novel·RecallGap·Recurrence, 회수 이력 수동 입력) / ⓔ Best Practice 대칭(BP-01). **물리 실데이터 생성**: framework/adapters/claude/memory-data/ — store 21파일 + index.jsonl 21라인.
4. **검증 리포트** — docs/v0.4-verification-report.md: 항목 판정 31건, VT-4 전수 스캔(5부류), VT-5 물리 재관측·재계산(store↔index 전수 대조, 스키마 42건 셀 대조, promotion-review 확정값 전건 대조 개작 0, 회수 독립 재현, 진리표 재검, 음성 케이스 역산). 최초 **Fail(위반 1)** → demo.md r3 재작업 → **최종 Pass (충족 31/위반 0/판정 불가 0)**.

## 1.2 v0.4 완료 조건 대조 (ROADMAP)

| 완료 조건 | 판정 | 근거 |
|---|---|---|
| 실패→Lesson 생성→다음 작업 회수 사이클 시연 (Learn from Failure) | 충족 | 시연 ⓞ+ⓐ — Verifier가 index만으로 회수를 독립 재현 (검증 리포트) |
| 회수 규칙이 최소 Context 원칙 준수 (Token Efficiency) | 충족 | 시연 ⓑ(+ⓐ 최소 집합) — 거부 3케이스·기본 index·recall.limit.max=20 |
| 모든 접근이 Memory Service Interface 경유 (Cross-cutting) | 충족 | 전 시연 §5 관측 PortBypass 0 + 물리 데이터 Adapter 경계 이하 전량 |
| Memory·Lessons 포맷이 스펙(04·05)과 일치 | 충족 | 스키마 42건 셀 단위 대조 위반 0, contract id 3중 일치 |

04 §7 완료 기준 6건·05 §7 완료 기준 7건도 전건 충족 (검증 리포트 — contract id·AI 비의존 2건 포함 Verifier 직접 수행).

## 1.3 이번 세션의 설계 결정 (전부 확정, 근거 기록)

| 결정 | 내용 | 주체 |
|---|---|---|
| **DP-M1: Recall 시스템 상한** | Provider Module Config 키 `recall.limit.max`(유한 양의 정수, **기본 20**)로 표현. 04는 상한 존재만 규정, 값 원천은 Module scope config(01 §3.2-B). 기록: module-manifest.md §3 | Advisor 결정 |
| Module 구현 디렉터리 경계 | structure.md §2에 4번째 경계 행 추가 — `framework/{loop,memory,verifier,workflow,plugins}/`, 자기완결(01 §3.2-E 규칙 2), 문서 본문 AI·언어·툴체인 비의존(**C-3 확장**) | Advisor + 사용자(계획 승인) |
| **C-2 적용 주** | 형태 B 실행 코드 경계에 Module 구현 디렉터리 포함(core/ 문서 전용 불변 핵심 보존, Module 디렉터리=Runtime 호스팅 실현). v0.3 문서 잠재 불일치(§3 규칙 2 vs §4) 해소 | Advisor + **사용자 승인(2026-07-06, Baseline 승인에 포함)** |
| Item·Index 인스턴스 소유 | 04 §3.2-A/C 인스턴스는 memory-store.md **단일 소유** — memory-service.md는 포인터만(이중 갱신 방지). M2 Worker의 R3 에스컬레이션을 Advisor 조율로 확정 | Advisor |
| **투영 규칙 보강 (OQ-M5-1 해소)** | lessons.md §5.2 r2 — applicability 외에 **안정 `id`·`status`도 labels 투영**, **최신 상태 해소 규칙**(같은 안정 id 중 timestamp 최신=현재 상태). 05 §3.1-B "Active 최소 집합"의 index 단계 해소. labels는 04 자유 태그 집합이므로 계약 변경 아님 | Advisor 결정 |
| 라벨 키 물리 표기 정본 | memory-binding.md §5.4 — `situation`/`stable_id`/`status`/`verdict`/`matched_lesson_id` 5키 (Adapter 소관, 첫 실사용 v0.4 시연) | Advisor (OQ-M7-1 해소) |
| Manifest 파일명·version | Module 경계별 자기 `module-manifest.md` 관례(향후 loop/verifier/workflow 확장). Provider Module version=0.1.0 — Framework 버전과 독립 축, 구현 갱신 시 상승 | Advisor |
| BP 시연 출처 | 역사 실증 모범 사례(v0.3 §1.4) 우선 — provenance 실물 문서 기반 | Advisor |
| 승격 사전 심사 방식 | Advisor가 시연 착수 전 후보 전건 심사, 승인 기록 문서(docs/v0.4-promotion-review.md)를 위임 input으로 제공. 참조 첨부=승격 성립 조건 | Advisor |
| **이력 행 시점 기록 원칙** | §9 이력 행은 시점 기록 — 재검증 기준("잔존 서술 0건")은 라이브 본문에만 적용, 기존 이력 행 문면은 append-only 불변 (memory-binding r2 과잉 적용 → r3 원복 사례) | Advisor 판정 |
| 문서 상태 라벨 관례 | 개정 중 "v0.4 Draft (CP2/CP3 미완)" 정직 표기 → CP3+사용자 승인 시 Baseline 행 append·상태 라인 승격 | Advisor (M1 OQ 수용) |
| OQ-M5-2: Record 원자성 | Bootstrap(형태 A)은 절차 준수+완료 후 대조로 정합 보증. 강한 원자성은 **형태 B/DP-4 재상정 시 확정** (계약 변경 아님) | Advisor 수용 |

## 1.4 검증 결과 (검증 게이트 실동작 기록)

- 위임 총 10회 (Planner 1 · Worker 8 · Verifier 1) + 재작업·재검증 라우팅 7회(전부 기존 에이전트 재개). 거짓 완료 보고 0건.
- **CP2 Fail → 재작업 → Pass 1건:** demo.md가 기록 timestamp를 "실제 수행 시각"으로 서술했으나 실측상 store 21파일은 25ms 창 일괄 생성, 기록 내 timestamp는 생성기 배정 순서 값 — **Verifier가 Advisor 게이트 C도 놓친 서술↔실측 모순을 검출** (L-07 유형 재발. v0.3 A8에 이어 CP2 독립 판정 존재 이유 2번째 실증). r3 서술 교정(물리 데이터는 INV-6 append-only로 무수정) → 재검증 Pass.
- **Advisor 게이트 C 재작업 2건:** M2 r2(§9 번호 충돌 + Advisor 결정 3건 반영), demo.md r2(§9-note 번호 정리 — M2 전례 일관 적용).
- **Worker 자가 검출·공개 3건 (BP-01 반복 실증):** M3 금지 토큰 누출 2건 자가 교정, M2 소유 경계 중첩 R3 에스컬레이션(추측 정리 없이), memory-binding r2 거버넌스 판단 투명 공개(→ Advisor 원복 판정).
- Wave 2 수합 정합 대조(07 §4.1)에서 M2↔M3 소유 중첩 조짐을 병합 전 해소 — 병렬 집합 충돌 중재의 실사용 사례.

## 1.5 Lesson 후보 (v0.4 세션 신규 — **이제 정식 등록 경로 존재**)

이전과 달리 Memory Service가 가동 중이므로, 아래 후보는 차기 세션에서 Register Candidate → Advisor 승격 심사 경로로 **정식 등록**한다 (지연 등록 사유: CP2가 store 21건 구성으로 판정을 닫은 뒤 발생/확정된 후보들).

1. **기록 내 timestamp 성격 구분 서술** — 기록 필드의 timestamp(순서 값)와 물리 생성 시각(실측)을 구분 서술한다. "실제 수행 시각" 류 주장은 실측 대조 후에만 기입 (L-07의 재발 사례 — demo.md r3. 재발 판정 계약상 실제 Recurrence 유형 후보: L-07이 이 세션에 회수·적용되었음에도 동종 실패 발생).
2. **재검증 기준의 적용 범위 명시** — 재작업 지시의 "잔존 서술 0건" 류 기준은 라이브 본문에 적용됨을 명시하고, 시점-스코프 기록(이력 행·인용·교정 경위)은 제외 명시한다. 이력 행 문면은 append-only 불변 (memory-binding r2→r3 사례).

## 1.6 차기 개정 일괄 후보 (비차단 — Verifier 관찰 + 승계)

1. lessons.md §5.2에 재발 판정 레코드의 `verdict`·`matched_lesson_id` labels 투영 명시 편입 (현재 memory-binding.md §5.4에만 물리 키 존재).
2. structure.md §8 트리에 v0.4 파일 반영 (§6 표는 "v0.3 산출물" 명시 범위 유지 — v0.4 산출물 표 추가 여부 포함).
3. Glossary 일괄 개정(v0.1~v0.3 승계: "Wave" 표제어 승격 등) + config-schema.md 경미 어휘 정리 (v0.3 §5.3 승계).

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1~v0.3 완료(기준선). **v0.4 완료 — 사용자 승인으로 공식 기준선 확정 (2026-07-06).** ROADMAP상 다음 개방 트랙: **v0.5 (Verifier, Track B) ∥ v0.8 착수(Extension System, Track D)**. v0.6(Loop Engine)은 v0.4+v0.5 완료가 선행 조건 — v0.5가 크리티컬 패스.
- 승인 근거: Verifier 독립 판정 Pass(충족 31/위반 0, 재작업 1회 후) + CP3 Advisor 승인 + 사용자 승인(C-2 적용 주 포함 명시 보고 후).

## 2.2 산출물 상태 (전부 v0.4 Baseline — 사용자 승인 2026-07-06, 각 문서 이력에 기록)

| 파일 | 내용 | 비고 |
|---|---|---|
| `framework/core/structure.md` | 4경계 구조 규격 (Module 구현 디렉터리 경계·C-3 확장·C-2 적용 주) | v0.4 개정 (M1) |
| `framework/memory/memory-service.md` | Memory Service Interface(단일 Port) 계약 인스턴스 + 기록·회수 프로토콜 | r2 — Item·Index는 포인터화 |
| `framework/memory/module-manifest.md` | Provider Module Manifest (contract=`MemoryServiceInterface`, configSchema `recall.limit.max`=20) | r2 — DP-M1 |
| `framework/memory/memory-store.md` | Memory Item 스키마 + Index·Index Entry 규격 + store 계약 구조 (04 §3.2-A/C/E 인스턴스 단일 소유) | |
| `framework/memory/lessons.md` | Lesson·BP·재발 판정 스키마 + 생성·승격 규칙 + kind 3종 + 투영 규칙(안정 id·status·최신 상태 해소) | r2 — OQ-M5-1 |
| `framework/adapters/claude/memory-binding.md` | 물리 실현 정본 — memory-data/ 구조·직렬화·Record/Recall 절차·라벨 키 5종(§5.4) | r3 — 이력 원복 포함 |
| `framework/adapters/claude/memory-data/` | **물리 실데이터** — store/mi-0001~0021.json(21) + index/index.jsonl(21라인). Active Lesson 8·Active BP 1·Candidate 9·재발 레코드 3 | append-only, 계속 사용 |
| `docs/v0.4-demo-procedure.md` | 시연 6종 절차·판정 문장 17건 대응표·기록 포맷 | |
| `docs/v0.4-demo.md` | 시연 수행 기록 (실물 관측·재현 값) | r3 — timestamp 서술 교정 이력 보존 |
| `docs/v0.4-promotion-review.md` | Advisor 승격 사전 심사 기록 (L-01~L-08·BP-01 확정 필드값·승인) | Advisor 직접 산출물 |
| `docs/v0.4-verification-report.md` | CP2 검증 리포트 — Fail→Pass 이력 보존, 항목 31건 | |
| Frozen specs 15개, ARCHITECTURE.md(0.2), ROADMAP.md, v0.2·v0.3 산출물 | 무변경 (Verifier 실측 확인) | |

## 2.3 하네스 상태

**Bootstrap 유지** (13 §3.2-B — DP-2 판정 승계). **Memory Service는 이제 실가동 상태다** — 단일 Port 계약·물리 store·Active Lesson 8건·BP 1건이 실재하며, 차기 세션의 Consult 단계에서 실제 회수가 가능하다 (아래 §3.4). Formal 전이는 로드맵대로 v0.9 사안.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙 선택 (사용자 결정 사안)

ROADMAP §4: v0.4 완료로 {v0.5 (Verifier, Track B) ∥ v0.8 착수 (Extension System, Track D)}가 개방 상태다. **권장: v0.5** — v0.6(Loop Engine, 통합점)의 선행 조건이 v0.4+v0.5이므로 크리티컬 패스다. v0.8은 병렬 여력이 있을 때 조기 착수 가능 (릴리스 정렬만 v0.6 이후).

## 3.2 v0.5 목표·완료 조건 (ROADMAP — Verifier, Track B)

검증 엔진 구축: Worker 결과물 검증 리포트 자동 생성 / 거짓 완료 보고 검출 케이스 1개 이상 시연 / 완료 판정 기준이 specs/06-verifier.md와 일치. 산출물: Verifier 프로토콜 구현물, 검증 리포트 스키마, 완료 판정 기준 카탈로그, 재작업 지시 포맷. 실현 경계: framework/verifier/ (Module 구현 디렉터리 — structure.md §2 v0.4 개정으로 경계 정본 존재).

## 3.3 v0.5 참고 (v0.4에서 마련된 것)

- v0.3·v0.4 검증 리포트 2건이 06 계약의 실사용 인스턴스 — v0.5 스키마·카탈로그의 실증 기반.
- 거짓 완료 검출 실사례 축적: v0.2 CP2 검출 1건, v0.3 CP2 검출 1건(Advisor 결함), v0.4 CP2 검출 1건(서술↔실측 모순).
- Module 경계 관례 확립: framework/verifier/에 자기 module-manifest.md(contract id는 01 §8 예2 계열) + 문서 본문 C-3 확장 적용 + 물리 실현은 adapters/claude/ 바인딩 문서.

## 3.4 신규 관행 — Memory 실사용 (모든 차기 세션 공통)

1. **Consult**: 착수 전 Memory Service Interface로 회수한다 — purpose 명시, scope{kind=`lesson`, labels: status=Active + 상황 투영}, 기본 detail=index. 물리 수행은 memory-binding.md §3.2 (index.jsonl 조회 → 대상 store 파일만 로드). Active Lesson 8건(L-01~L-08)·BP-01이 실재한다.
2. **Memory Update**: 세션 실패·성공에서 후보를 도출해 Register Candidate로 기록하고(§1.5 신규 후보 2건 포함), Advisor 승격 심사를 거친다. 기록은 append-only — 기존 파일 수정 금지.
3. 재발 판정: 새 실패는 Judge Recurrence 3분류로 판정·기록한다 (회수 이력은 수동 제공 — 03-loop 미구현 동안).

## 3.5 v0.4 이월 사항

- DP-4 재상정 시(v0.9 전후): Record 원자성 메커니즘(OQ-M5-2), 형태 B 코드 물리 분할.
- §1.6 차기 개정 일괄 후보 3건.
- 13 §3.2-B 전이 조건 재판정·Adapter Interface 정식화 — v0.9 (v0.3 승계).

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — v0.5 가정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v0.4 (Memory & Lessons, Track A)가 완료되었다.
이번 세션의 목표는 ROADMAP v0.5 (Verifier, Track B)다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v0.4.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md §3.2
   절차로 Active Lesson(kind=lesson, status=Active)·BP를 목적·최소 범위로 회수하고
   회수 집합을 기록한다 (이번 세션부터 실가동 — handoff §3.4).
3. ARCHITECTURE.md(0.2), ROADMAP.md v0.5 섹션, specs/06-verifier.md,
   framework/core/structure.md(v0.4 — 4경계), docs/v0.3·v0.4-verification-report.md
   (06 계약 실사용 인스턴스)를 정독한다.
4. .claude/AGENT.md, .claude/agents/ 4종, docs/delegation-protocol.md,
   docs/verification-checklist.md를 읽는다 (작업 도구·경계 정본).
5. v0.5 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v0.4 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D), 구현 Worker(Opus) 위임, 완료 보고 불신·
독립 검증, Frozen spec 변경은 버전 상승+Revision History, Architecture-Spec 충돌은
사용자 보고, C-1~C-3(+Module 구현 디렉터리 C-3 확장) 전 산출물 적용.
세션 종료 시 Memory Update — 실패·성공 후보 Register Candidate + Advisor 승격 심사
(handoff §1.5 이월 후보 2건 포함).
```

---

# 5. 주의사항

1. **물리 store는 append-only다** — framework/adapters/claude/memory-data/ 이하 기존 파일의 수정·삭제는 04 INV-6 위반이다. 갱신·정정·status 전이는 새 Memory Item 기록으로만 표현한다 (같은 stable_id, timestamp 최신 = 현재 상태 — lessons.md §5.2).
2. **§9 이력 행은 시점 기록** — 문면 불변, append만. 재검증·개정 기준은 라이브 본문에만 적용한다 (§1.3 결정).
3. **개정 시 전 지점 전수 갱신** (L-06) + **상태 서술은 실측 후 기록** (L-07 — timestamp 성격 구분 포함, §1.5-1). v0.4 산출물의 개정은 Advisor 승인 + 각 문서 §9 기록.
4. **승격 권한은 Advisor 전속** (05 INV-4) — 승인 기록 참조 없는 승격은 NotApproved. 심사 기록 관례: docs/v0.4-promotion-review.md 동형.
5. **C-2 적용 주의 실효는 형태 B(DP-4, v0.9 전후) 시점** — 그 전까지 Module 구현 디렉터리에 실행 코드를 두는 결정은 없다.
