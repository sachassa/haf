# specs/03-loop — Loop Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05 · 2026-07-26 정합(격리 개정 — 슬림화·앵커 90ca19c))
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Loop는 Agent Lifecycle을 자동으로 반복하는 오케스트레이션 규격이다.

Loop는 네 가지 문제를 해결한다.

- Agent Lifecycle 7단계가 자동으로 이어지지 않으면 사람이 매 단계를 지시해야 한다. 단계 전이 규칙을 통일한다.
- Verify 실패 뒤 무엇을 할지 계약이 없으면 실패가 방치되거나 무한히 재시도된다. 재작업 루프와 재시도 한도를 규격화한다.
- 단계 전이가 기록되지 않으면 무슨 일이 있었는지 검증할 수 없다. 모든 전이를 기록으로 남긴다.
- 사람 개입 조건이 불명확하면 개입이 과하거나(비효율) 부족하다(무단 진행). 사람 개입 지점을 계약으로 확정한다.

## 책임 (1~3문장)

Loop는 단일 작업 하나에 대해 Agent Lifecycle(Consult → Complete) 한 사이클을 구동하는 오케스트레이션 규격이다.

Loop는 단계 전이 규칙, 재작업 루프, 루프 상태 기록, Learn 트리거, 사람 개입 지점을 정의한다.

## Non-Goals

- Runtime의 Bootstrap/Shutdown 호스팅 계약을 정의·재정의하지 않는다 — specs/01-runtime.md 소관이다. Loop는 Runtime의 "Serve" 구간(01 §3.1-C)을 소비하는 쪽이다.
- Verify 단계의 판정 기준·검증 방법·거짓 완료 검출을 정의하지 않는다 — specs/06-verifier.md 소관이다. Loop는 Verify의 오케스트레이션 순서만 정의한다.
- Agent 역할의 내부 계약(위임/보고 메시지 필드, 역할 경계)을 정의하지 않는다 — specs/02-agent.md 소관이다.
- Memory·Lessons의 내부 포맷·생성 규칙·후보 승격을 정의하지 않는다 — specs/04-memory.md, specs/05-lessons.md 소관이다. Loop는 Memory Update의 접근 경로와 기록 시점만 정의한다.
- 큰 작업의 분해·병렬 디스패치·병합을 정의하지 않는다 — specs/07-workflow.md 소관이다. Loop는 단일 작업의 단일 Lifecycle 사이클만 구동한다.

---

# §2. Position

- 아키텍처 상 위치: Runtime Layer에서 구동되는 Core Component "Loop"의 규격 문서다 (Glossary §3.2-D Loop, §3.2-A Runtime Layer, §9-OQ2). Loop는 Runtime의 "Serve" 구간(01 §3.1-C)에서 호스팅 계약(Config·계약 해소·자원)을 소비한다.
- Loop는 Layer 스택의 특정 위치를 새로 차지하지 않는다. Runtime Layer가 제공하는 실행 환경 위에서 Agent Lifecycle을 구동한다.

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 특히 3.4 Verify Everything, 3.5 Learn from Failure, 3.6 Token Efficiency, 5.1 Memory Service.
- specs/00-glossary.md (실재, Frozen) — 모든 용어의 정본. 특히 §3.2-F Agent Lifecycle.
- specs/TEMPLATE.md (실재, Frozen) — 문서 구조와 DoD.
- AGENT.md (실재) — Agent Lifecycle 원문 순서, Core Principles(Human Approval 포함), Memory 원칙.
- ROADMAP.md v0.6 (실재) — Loop Engine 완료 조건과 산출물.
- specs/01-runtime.md (실재, Frozen) — Serve 구간 호스팅 계약. 인용 가능.
- specs/02-agent.md (실재, Frozen) — 역할 경계, 위임/완료/실패 메시지, INV-4. 인용 가능.

(상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·01·02·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`. 종전 "Review"·"Adopted" 표기는 작성 시점 기록이었다.)

## 이 spec에 의존하는 spec (dependents)

- specs/07-workflow.md — Workflow는 여러 Loop 사이클을 분해·병렬 디스패치·병합한다. 단일 사이클 구동은 Loop, 다중 사이클 오케스트레이션은 Workflow다 (§9 조율).

## 경계(위임) 관계 — 순환 아님

- specs/06-verifier.md — Loop는 Verify 단계의 순서만 정의하고 판정 내용을 06에 위임한다. Loop의 시퀀스 골격은 06의 내부 판정 정의에 의존하지 않으므로 순환이 아니다 (§9 조율).
- specs/04-memory.md, specs/05-lessons.md — Loop는 기록 시점과 접근 경로만 정의하고 내부 포맷을 04/05에 위임한다 (§9 조율).

## 순환 의존

없다. Loop의 Core Contract(§3)는 00/01/02의 계약을 소비하는 방향(03 → 01, 03 → 02)이다. 06/07은 Loop를 소비하는 방향이다. 06/04/05에 대한 관계는 의존이 아니라 위임이며, Loop는 그들의 내부 정의 없이도 자신의 계약을 완결한다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 실행 바인딩은 §4에 둔다.

Loop는 세 가지 계약을 정의한다.

- 단계 전이 계약 (§3.1-A) — 7단계의 진입·완료·전이 규칙.
- 재작업·종료·개입 계약 (§3.1-B, §3.1-C, §3.1-D) — 실패 시 되돌림, 종료 보장, 사람 개입 조건.
- 기록·산출 포맷 (§3.2) — 루프 상태 기록, 단계 상태, Learn 트리거와 산출.

---

## 3.1 Interface

Loop는 단일 위임 하나에 대해 Lifecycle 한 사이클을 구동하는 연산을 노출한다.

- 입력: 위임 메시지 1건 (02 §3.2-B) + Runtime이 Serve 구간에 제공하는 호스팅 컨텍스트 (01 §3.2-C Runtime Context — effective config, 계약 해소, 자원). Loop는 이 컨텍스트를 소비만 하고 변경하지 않는다.
- 출력: 완료 보고 메시지 (02 §3.2-C) — Complete 도달 시. 또는 에스컬레이션 산출 — 사람 승인 요청 및/또는 실패 보고 메시지 (02 §3.2-D).
- 완료 조건: 7단계를 순서대로 통과하고 검증 게이트(§3.1-A Verify, §3.1-C)를 통과한 뒤 Complete에 도달한다.
- 실패 보고 포맷: 재시도 한도 초과·차단성 실패·사람 개입 필요 시 에스컬레이션한다 (§3.1-C, §3.1-D, §6).

전이 판정을 유발하는 각 역할의 책임은 02 §3.1을 따른다. Loop는 그 책임을 전이 규칙으로 배열할 뿐 역할 내부 계약을 재정의하지 않는다.

---

### A. 단계 전이 규칙 (Stage Transition Rules)

Loop는 성공 경로에서 7단계를 선형 순서로 전이한다.

Consult → Plan → Execute → Verify → Learn → Memory Update → Complete (AGENT.md, Glossary §3.2-F).

각 단계는 진입 조건이 충족될 때만 진입한다. 완료 조건이 충족될 때만 다음 단계로 전이한다. 모든 전이는 루프 상태 기록(§3.2-A)에 남는다 (INV-3). 각 단계의 실패는 재작업 루프(§3.1-B) 또는 에스컬레이션(§3.1-C)으로 분기한다.

**1. Consult**
- 진입 조건: 위임 메시지가 완전하다 (02 INV-6 — 입력·출력·완료 조건·컨텍스트 존재). 불완전하면 진입하지 않고 반환·질의한다.
- 활동: 상위 규약·Architecture·관련 spec·Memory를 참조한다. Advisor가 참조를 주도한다 (02 §3.1). Memory 회수는 회수 정책에 따라 최소 범위로 한다 (§5).
- 완료 조건: 착수에 필요한 컨텍스트가 확보된다.
- 전이: → Plan.
- 실패: 컨텍스트 부재·의존 계약 미확정으로 추측 없이 진행 불가 → 에스컬레이션 (02 O4, §3.1-D 조건 3).

**2. Plan**
- 진입 조건: Consult 완료.
- 활동: 작업을 계획·분해한다. Planner가 초안을 작성하고 Advisor가 채택한다 (02 §3.1, INV-3).
- 완료 조건: Advisor가 계획을 채택한다.
- 전이: → Execute.
- 실패: 계획 미채택 → Plan 재작성. 반복 미채택 → 에스컬레이션.

**3. Execute**
- 진입 조건: Plan 채택 완료.
- 활동: Worker가 계획을 구현하고 산출물을 생성한다 (02 §3.1).
- 완료 조건: 산출물이 생성되고 Worker 자체 점검(self_check, 02 §3.2-C)이 수행된다. 자체 점검은 최종 승인이 아니다 (02 §3.2-A Worker 경계).
- 전이: → Verify.
- 실패: 구현 불가·차단 → 실패 보고(02 §3.2-D) → 재작업 루프 또는 에스컬레이션.

**4. Verify** (오케스트레이션 순서만 정의 — 판정 내용은 06 소관)
- 진입 조건: Execute 완료 (산출물 + 자체 점검 존재).
- 활동: 검증 게이트를 오케스트레이션한다. 게이트는 Loop가 소유하는 순서 있는 세 체크포인트다.
  - CP1. Worker 자체 점검 — Execute 산출을 입력으로 받는다.
  - CP2. Verifier 독립 판정 — Worker 보고를 그대로 신뢰하지 않고 독립 판정한다 (02 §3.2-A, §3.1). 판정 기준·검증 방법은 06 소관이다.
  - CP3. Advisor 승인 — 최종 승인 (02 §3.1). CP3는 Complete 전이 게이트로 실현된다(아래 "게이트-단계 매핑" 참조).
- 완료 조건(Verify 통과): CP2가 PASS다. Verify 통과 후에만 완료 보고가 생성될 수 있다 (02 INV-4).
- 전이(통과): → Learn.
- 전이(실패): CP1 또는 CP2 실패 → 재작업 루프(§3.1-B).
- 경계: Loop는 CP1 → CP2 → CP3 순서만 소유한다. 각 체크포인트의 판정 내용은 CP1·CP3가 02(Worker·Advisor), CP2가 06(Verifier) 소관이다.

**5. Learn**
- 진입 조건: (a) Verify 통과(성공 경로), 또는 (b) 사이클이 에스컬레이션으로 종료되기 직전(실패 경로). 두 경우 모두 Learn을 거친다 (INV-5).
- 활동: 실패와 성공에서 후보를 도출한다 (§3.2-C). Verifier가 Learn 입력을 제공한다 (02 §3.1).
- 완료 조건: 이 사이클의 Lesson 후보(누적 실패)와 Best Practice 후보(성공 시)가 도출된다.
- 전이: → Memory Update.
- 실패: 없음(도출만 수행). 후보가 없으면 "없음"을 기록한다.

**6. Memory Update**
- 진입 조건: Learn 완료.
- 활동: Learn이 도출한 후보를 기록한다. 모든 접근은 Memory Service Interface(단일 Port) 경유다 (§5, INV-7).
- 완료 조건: 후보가 단일 Port를 통해 기록된다. 내부 포맷·승격은 04/05 소관이다.
- 전이(성공 경로): → Complete. 전이(실패 경로): → 에스컬레이션(§3.1-C).
- 실패: Port 접근 불가 → 에스컬레이션.

**7. Complete**
- 진입 조건: Memory Update 완료 + 검증 게이트 CP1·CP2 통과.
- 활동: CP3(Advisor 최종 승인, 02 §3.1)을 게이트로 삼아 사이클을 닫고 완료 보고 메시지(02 §3.2-C)를 산출한다.
- 완료 조건: Advisor가 최종 승인한다. 미승인 시 재작업 루프(§3.1-B) 또는 에스컬레이션.
- 전이: 사이클 종료(정상).

**게이트-단계 매핑 (검증 게이트 CP1→CP2→CP3의 단계 배치).**
Loop는 세 체크포인트의 순서를 불변으로 소유한다. 각 체크포인트는 다음 단계에 배치된다.

| 체크포인트 | 배치 단계 | 소유(내용) |
|---|---|---|
| CP1 Worker 자체 점검 | Execute 종료 → Verify 입력 | 02 (Worker) |
| CP2 Verifier 독립 판정 | Verify | 06 (Verifier) |
| CP3 Advisor 승인 | Complete 진입 게이트 | 02 (Advisor 최종 승인) |

이 배치는 02 §3.1(Verifier 판정 = Verify, Advisor 최종 승인 = Complete)과 02 INV-4(완료 보고는 Verify 통과 후)에 정렬한다. "Verify 통과"는 CP2 PASS로 정의된다. Advisor 최종 승인(CP3)은 Complete 게이트다. 정합 확인은 §9에 기록한다.

---

### B. 재작업 루프 (Rework Loop)

검증 게이트의 어느 체크포인트라도 실패하면 재작업 루프가 동작한다 (ROADMAP v0.6). 되돌아갈 단계는 결함의 근본 원인에 따라 결정된다.

| 결함 근본 원인 | 되돌아갈 단계 |
|---|---|
| 산출물 결함 (CP1/CP2가 산출물 자체의 완료 조건 미충족을 지목) | Execute |
| 계획 결함 (계획 자체가 잘못되었음이 판정됨) | Plan |
| 전제·컨텍스트 결함 (착수 전제가 틀렸음이 판정됨) | Consult |

기본 되돌림 대상은 Execute다. 상위 근본 원인이 판정된 경우에만 Plan 또는 Consult로 되돌린다.

- 재시도 한도: 재작업 되돌림마다 retry_count가 증가한다. retry_count가 재시도 한도를 초과하면 에스컬레이션한다(§3.1-C, §3.1-D 조건 1). 재시도 한도 값은 Config(01 §3.2-B)로 주어진다. 기본값·스코프는 Config·Adapter Binding(§4)이 정한다. Loop는 한도 초과 판정 규칙만 정의한다.
- 각 재작업 되돌림은 루프 상태 기준으로 하나의 전이 이벤트로 기록된다 (§3.2-A). 되돌림의 원인이 된 실패 보고(02 §3.2-D)는 Learn 입력으로 누적된다 (§3.2-C).
- 무한 재작업은 없다 (INV-4). 재작업은 언제나 재시도 한도 안에서만 반복된다.

06의 판정 결과(pass/fail)와 재작업 지시 포맷이 이 재작업 루프의 입력과 정합해야 한다 — §9 조율.

---

### C. 종료 규칙 (Termination)

Loop는 반드시 종료한다. 종료는 정확히 두 유형 중 하나다 (INV-4).

- **정상 종료** — Complete 도달. 완료 보고 메시지(02 §3.2-C)를 반환한다.
- **에스컬레이션 종료** — 아래 사유로 자동 진행이 불가한 경우. 종료 직전 반드시 Learn → Memory Update를 거쳐 누적 후보를 기록한 뒤(INV-5) 사람 개입 및/또는 실패 보고로 넘긴다.
  - 재시도 한도 초과 (§3.1-B).
  - 차단성 실패 (blocking = 차단됨, 02 §3.2-D).
  - 사람 개입 필요 조건 발생 (§3.1-D).

어떤 종료도 검증되지 않은 결과를 완료로 보고하지 않는다 (INV-2, ARCHITECTURE 3.4).

---

### D. 사람 개입 지점 (Human Intervention Points)

Loop는 사람 개입 없이 7단계를 자동 통과하는 것을 기본으로 한다 (ROADMAP v0.6 "사람 개입 최소"). 사람 승인은 아래 열거된 조건에서만 요구된다 (AGENT.md Core Principles "Human Approval"). 이 목록에 없는 전이는 Agent 역할(Advisor/Planner/Worker/Verifier)의 자동 판정으로 진행한다.

사람 승인이 필요한 조건 (열거 — 이 목록이 계약이다):

1. **재시도 한도 초과** — 재작업 루프가 Config 재시도 한도를 초과한다 (§3.1-B).
2. **차단성 실패** — 실패 보고의 blocking = 차단됨 (02 §3.2-D). 자동 재작업으로 해소 불가.
3. **의존 계약 미확정 / 추측 필요** — Consult·Plan에서 의존 인터페이스가 미확정이라 추측 없이 진행 불가하다 (02 O4).
4. **상위 규약·Architecture 충돌** — 단계 수행 중 상위 규약 또는 Architecture와의 충돌을 발견한다. 자동 해석하지 않고 사람에게 보고한다.
5. **역할 경계 초과 결정** — Architecture 결정 등 Agent 역할 권한을 넘어 사람 승인이 명시적으로 요구되는 사항.

각 사람 개입 발생은 루프 상태 기록(§3.2-A)에 actor = human으로 남는다.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)은 Adapter Binding(§4)이 정한다.

### A. 루프 상태 기록 (Loop State Record)

각 단계 전이가 기록으로 남는다 (ROADMAP v0.6 완료 조건). 루프 상태 기록은 전이 이벤트(Transition Event)의 순서 있는 append-only 로그다.

전이 이벤트 필드:

| 필드 | 의미 | 필수 |
|---|---|---|
| `cycle_id` | 이 Lifecycle 사이클의 식별자. 하나의 위임 = 하나의 사이클. | 예 |
| `seq` | 사이클 내 전이 순번. 단조 증가한다. | 예 |
| `from_stage` | 전이 이전 단계. 사이클 시작 시 없음. | 아니오 |
| `to_stage` | 전이 이후 단계. | 예 |
| `trigger` | 전이 사유 — 완료 조건 충족 / Verify 실패 / 재작업 되돌림 / 에스컬레이션. | 예 |
| `outcome` | 단계 결과 — pass / fail / escalated. | 예 |
| `retry_count` | 현재까지 재작업 되돌림 횟수 (§3.1-B). | 예 |
| `actor` | 전이를 유발한 역할 (Advisor/Planner/Worker/Verifier) 또는 human(사람 개입 시). | 예 |
| `ref` | 관련 산출물·보고 참조 (위임/완료/실패 보고, Verifier 판정 참조). | 아니오 |
| `at` | 전이 시점. 순서 보장용 추상 시각. | 예 |

불변 규칙: 기록은 append-only다. 전이는 기록된 뒤에 유효하다 (INV-3). 기록되지 않은 전이는 없다. 이 로그로 사이클 전체를 재구성·검증할 수 있어야 한다 (§7).

### B. 단계 상태 (Stage Status)

각 단계는 다음 상태 중 하나를 가진다.

- `Pending` — 진입 전.
- `Active` — 진입 후 진행 중.
- `Passed` — 완료 조건 충족. 다음 단계로 전이 가능.
- `Failed` — 완료 조건 불충족. 재작업 루프 대상.
- `Escalated` — 사람 개입 또는 상위 에스컬레이션 대상.

### C. Learn 트리거와 산출

Learn 단계는 실패와 성공에서 후보를 도출한다 (ARCHITECTURE 3.5, AGENT.md Memory).

산출 후보:

- **Lesson 후보** — 실패 경로에서 도출. 입력은 재작업 루프의 각 Verify 실패와 차단 실패의 실패 보고(02 §3.2-D)이며, 그 lesson_candidate 표시를 근거로 한다. 모든 실패는 Lesson 후보다 (AGENT.md, 02 §5).
- **Best Practice 후보** — 성공 경로에서 도출. 사이클이 Verify 통과로 Complete를 향할 때. 모든 성공은 Best Practice 후보다 (AGENT.md, Glossary §3.2-C, 02 §5).

트리거 규칙:

- 재작업 루프 진입(Verify 실패)마다 그 실패의 실패 보고가 이 사이클의 누적 실패 집합에 추가된다.
- Learn 진입 시, 누적 실패 집합 전체가 Lesson 후보로, 성공 시 그 사이클이 Best Practice 후보로 도출된다.
- 성공이든 에스컬레이션이든 사이클 종료 전 Learn은 항상 실행된다 (INV-5). 실패가 학습 없이 버려지지 않는다.

Learn은 후보를 **도출만** 한다. 후보의 포맷·생성 규칙·승격은 04/05 소관이다 (§9). 실제 기록은 Memory Update 단계에서 단일 Port 경유로 이뤄진다 (§5).

---

## 3.3 Invariants

- **INV-1 (단계 순서 고정).** 성공 경로에서 Loop는 Consult → Plan → Execute → Verify → Learn → Memory Update → Complete 순서로만 전이하며 단계를 건너뛰지 않는다 (AGENT.md, Glossary §3.2-F).
- **INV-2 (검증 게이트).** Complete는 검증 게이트(CP1 자체 점검 → CP2 Verifier 독립 판정 → CP3 Advisor 승인)를 통과한 뒤에만 도달된다. 완료 보고는 Verify 통과(CP2 PASS) 후에만 생성된다 (02 INV-4). 검증되지 않은 결과는 완료가 아니다 (ARCHITECTURE 3.4).
- **INV-3 (전이 기록).** 모든 단계 전이는 루프 상태 기록(§3.2-A)에 append-only로 남는다. 기록되지 않은 전이는 없다 (ROADMAP v0.6).
- **INV-4 (종료 보장).** Loop는 반드시 종료한다. 종료는 Complete 또는 에스컬레이션 둘 중 하나다. 재작업은 Config 재시도 한도 안에서만 반복된다. 무한 루프는 없다.
- **INV-5 (Learn 불가피성).** 성공이든 실패든 모든 사이클 종료는 Learn → Memory Update를 거친다. 모든 실패는 Lesson 후보, 모든 성공은 Best Practice 후보다 (ARCHITECTURE 3.5, AGENT.md).
- **INV-6 (사람 개입 최소).** 사람 승인은 §3.1-D에 열거된 조건에서만 요구된다. 그 외 전이는 Agent 자동 판정으로 진행한다 (ROADMAP v0.6).
- **INV-7 (Memory 단일 Port).** Memory Update의 모든 기록·회수는 Memory Service Interface(단일 Port) 경유다 (ARCHITECTURE 5.1). 영속성 백엔드에 직접 접근하지 않는다.
- **INV-8 (경계 불가침).** Loop는 Runtime의 Bootstrap/Shutdown을 재정의하지 않고 Serve 구간을 소비한다 (01). Verify 판정 기준·방법을 정의하지 않고 순서만 정의한다 (06). Agent 역할 내부 계약(02), Memory 내부 포맷(04/05), Workflow 다중 사이클(07)을 정의하지 않는다.
- **INV-9 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 실행 바인딩은 §4에 위치한다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다 (ROADMAP v0.6, ARCHITECTURE.md 3.1 "Claude는 첫 번째 Adapter").

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Loop 호스팅 (Serve 구간) | Claude Code 세션/턴이 Runtime의 Bootstrap~Serve~Shutdown 구간을 호스팅한다 (01 §4.1). Loop는 이 Serve 구간에서 구동된다. |
| 역할 실행 (CP1/CP2/CP3) | 각 역할은 `.claude/agents/*.md` 서브에이전트로 실행된다 (02 §4.1). CP1=Worker, CP2=Verifier, CP3=Advisor. Worker 기본 실행 모델(Opus 등) 지정은 02 §4 소관이며 이 spec은 참조만 한다. |
| 단계 전이 유발 | 위임·보고는 서브에이전트 위임과 최종 응답으로 흐른다 (02 §4.1). |
| 루프 상태 기록 직렬화 | §3.2-A 추상 스키마를 파일 기반 기록(구조화 로그/마크다운 등)으로 직렬화한다. 구체 경로·문법은 이 바인딩이 정한다. |
| 재시도 한도 Config | 재시도 한도 값은 effective config(01 §3.2-B)로 주어진다. v0.x에서 `.claude/CLAUDE.md`·설정 파일이 Project scope Config를 제공한다 (01 §4.1). |
| 사람 개입 채널 | §3.1-D 사람 승인 요청은 Claude Code 세션에서 사용자에게 제시된다. `.claude/CLAUDE.md`의 "Architecture와 Spec 충돌 시 사용자 보고"가 조건 4의 바인딩이다. |
| Memory 접근 | Memory Update의 단일 Port 경유는 Runtime이 배선한 Memory Service Interface Module을 Resolve하여 실현한다 (01 §5, 02 §4). |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부다. §3 Core Contract는 유지된다.

- SP-1: Loop 호스트 프로세스(Claude Code 세션/턴) → 대상 환경의 실행 프로세스 (01 §4.2와 정렬).
- SP-2: 역할 실행 모델·서브에이전트 위임 → 대상 환경의 Agent 오케스트레이션 (02 §4.2 SP-3/SP-4).
- SP-3: 루프 상태 기록 직렬화 포맷·저장 위치 → 대상 환경의 로깅 메커니즘.
- SP-4: 재시도 한도 등 Config 소스 → 대상 환경의 Config 메커니즘 (01 §4.2).
- SP-5: 사람 승인 채널 → 대상 환경의 사람 개입 메커니즘.

유지되는 것: §3.1-A 단계 전이 규칙, §3.1-B 재작업 루프, §3.1-C 종료 규칙, §3.1-D 사람 개입 조건, §3.2-A 루프 상태 기록 스키마, §3.2-C Learn 트리거. 이들은 이식 시 바뀌지 않는다.

---

# §5. Memory Access (해당 시)

Loop는 Memory 소비자다 (ARCHITECTURE 5.1 — Agent, Loop, Workflow, Verifier). Loop는 Memory Service Interface(단일 Port)를 통해서만 Memory에 접근한다 (INV-7).

## 읽기 (Recall)

- 목적: Consult 단계에서 착수 전 관련 Lessons·이전 결정·컨텍스트를 회수한다. Loop가 Consult 오케스트레이션 시 회수를 수행한다.
- 범위: 회수 정책(Recall Policy)에 따라 최소 범위로. 현재 사이클에 필요한 것만 읽는다.
- 시점: 필요할 때만. 매 전이마다 전량을 로드하지 않는다 (Token Efficiency, ARCHITECTURE 3.6).

## 쓰기 (Record)

- 시점: Memory Update 단계. Learn이 도출한 후보(Lesson 후보 / Best Practice 후보, §3.2-C)를 기록한다.
- 기록 대상: 다음 사이클에 필요한 결과·결정·상태, 그리고 Learn 산출 후보.
- 경로: Memory Service Interface 경유만 허용된다 (INV-7). 영속성 백엔드 직접 접근은 금지된다.

내부 포맷·생성 규칙·후보 승격은 specs/04-memory.md, specs/05-lessons.md 소관이다. 이 spec은 접근 경로와 기록 시점만 정의한다 (§9 조율).

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다. 별도 표시가 없으면 모두 Lesson 후보다.

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| 산출물 결함으로 검증 게이트 실패 | 재작업 루프 → Execute 재진입 (§3.1-B). | 예 |
| 계획 결함 판정 | 재작업 루프 → Plan 재진입. | 예 |
| 전제·컨텍스트 결함 판정 | 재작업 루프 → Consult 재진입. | 예 |
| 재시도 한도 초과 | Learn → Memory Update 후 사람 개입으로 에스컬레이션 (§3.1-C, §3.1-D 조건 1). | 예 |
| 차단성 실패 (blocking) | 사람 개입으로 에스컬레이션 (§3.1-D 조건 2). | 예 |
| 위임 불완전 (진입 실패) | Consult 진입 거부, 반환·질의 (02 INV-6). | 예 |
| 조기 Complete (검증 게이트 미통과) | INV-2 위반. 차단. Verify 통과 전 완료는 무효. | 예 |
| 전이 기록 누락 | INV-3 위반. 검증(§7) 실패로 판정. | 예 |
| 무한 재시도 | INV-4 위반. Config 재시도 한도로 차단. | 예 |
| Memory 우회 접근 | INV-7 위반. 단일 Port 경유로 교정. | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.6 완료 조건과 정렬한다.

- **자동 통과 시연.** 단일 작업이 사람 개입 없이 7단계를 통과해 Complete에 도달함을 보인다 (ROADMAP v0.6 "사람 개입 최소", INV-6).
- **전이 기록 시연.** 각 단계 전이가 루프 상태 기록에 append-only로 남고, 그 기록만으로 사이클을 재구성할 수 있음을 보인다 (INV-3, ROADMAP v0.6 "각 단계 전이가 기록으로 남는다").
- **재작업 루프 시연.** Verify를 의도적으로 실패시키면 재작업 루프가 근본 원인에 따른 단계(Execute/Plan/Consult)로 되돌아가고, retry_count가 증가하며, 재시도 한도 초과 시 사람 개입으로 에스컬레이션함을 보인다 (ROADMAP v0.6 "Verify 실패 시 재작업 루프 동작", §3.1-B).
- **Learn 생성 시연.** Verify 실패가 Lesson 후보를, 성공이 Best Practice 후보를 Learn에서 생성함을 보인다 (ROADMAP v0.6 "Learn 단계에서 Lesson 생성", §3.2-C).
- **검증 게이트 시연.** Complete가 게이트(CP1→CP2→CP3) 통과 후에만 도달되고, 게이트 미통과 시 Complete가 차단됨을 보인다 (INV-2, 02 INV-4).
- **개입 최소 시연.** 사람 승인이 §3.1-D 열거 조건에서만 요구되고, 그 외 전이가 자동 진행함을 보인다 (INV-6).
- **AI 비의존 시연.** §3 본문에 특정 AI 모델·실행 환경 의존 토큰이 0건임을 보인다 (INV-9, DoD-3).

## 검증 방법

- Verifier가 루프 상태 기록을 파싱해 전이 순서·완료 조건 충족·append-only 여부를 확인한다.
- Verifier가 재작업·한도 초과·에스컬레이션 케이스를 실행해 되돌림 대상과 종료 유형(Complete/에스컬레이션)을 확인한다.
- Verifier가 Learn 산출(Lesson/Best Practice 후보)의 트리거 시점을 §3.2-C와 대조한다.
- Verifier가 검증 게이트 미통과 시 Complete 차단을 확인한다 (INV-2).
- Verifier가 §3 본문을 스캔해 AI 의존 토큰(모델명·제품 기능명)이 0건임을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 정상 사이클 (성공 경로)**

위임 도착 → Consult(Memory 회수, Advisor 참조 주도) → Plan(Planner 초안, Advisor 채택) → Execute(Worker 산출 + 자체 점검 CP1) → Verify(CP2 Verifier PASS) → Learn(Best Practice 후보 도출) → Memory Update(단일 Port 기록) → Complete(CP3 Advisor 최종 승인, 완료 보고 산출).

각 전이가 루프 상태 기록에 순번(seq)과 함께 남는다. retry_count는 0으로 종료한다.

**예 2 — 재작업 루프 (Verify 실패 → 재구현 → 통과)**

Verify에서 Verifier(CP2)가 산출물 결함을 판정한다. → 재작업 루프가 Execute로 되돌린다(retry_count = 1). → Worker가 재구현한다. → Verify 재판정 통과. → Learn에서 이 실패의 Lesson 후보와 성공 Best Practice 후보를 함께 도출한다. → Memory Update → Complete.

루프 상태 기록에 outcome = fail 전이와 retry_count = 1이 남는다.

**예 3 — 한도 초과 에스컬레이션 (사람 개입)**

Verify가 반복 실패해 retry_count가 Config 재시도 한도를 초과한다(§3.1-D 조건 1). → Loop는 종료 전 Learn(누적 Lesson 후보 도출) → Memory Update를 실행한다(INV-5). → 사람 승인으로 에스컬레이션한다. → 사람 승인 대기 상태로 사이클이 에스컬레이션 종료된다.

루프 상태 기록에 outcome = escalated, actor = human 전이가 남는다. 완료 보고는 생성되지 않는다(검증 게이트 미통과, INV-2).

---

# §9. Open Questions

Advisor 에스컬레이션 및 조율 대상.

## 정합 확인 (기존 spec 요청에 대한 응답)

- **01-runtime 정합 확인 (01 §9 "03-loop 조율 필요" 응답)** — 해소(Loop가 Runtime에 요구하는 노출 표면 3종 = (a) effective config 읽기(01 §3.2-B), (b) Resolve를 통한 역할·Memory Service Interface 계약 해소(01 §3.1-A), (c) Serve 구간 자원. Loop는 소비만 하고 Bootstrap/Shutdown을 재정의하지 않는다 — 모순 없음 확인 · 상세 = git 앵커 90ca19c).

- **02-agent 정합 확인 (02 §9-OQ-4 응답)** — 해소(이 spec의 게이트 순서 CP1 자체 점검 → CP2 Verifier 판정 → CP3 Advisor 승인이 02 INV-4·§3.1과 정렬. "Verify 통과" = CP2 PASS, "Advisor 최종 승인" = Complete 게이트(CP3). 판정 내용은 06 위임 — 모순 없음 확인 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

## 타 spec 조율 (내용 추측·인용하지 않음)

- **06-verifier 조율 필요.** Verify 단계의 판정 기준·검증 방법·거짓 완료 검출은 06 소관이다. 이 spec은 오케스트레이션 순서(CP1→CP2→CP3)와 게이트 통과/실패 전이만 정의했다. 06의 판정 결과(pass/fail)와 재작업 지시 포맷이 §3.1-B 재작업 루프의 입력과 정합해야 한다.
- **04-memory 조율 필요.** Memory Update가 기록하는 후보(Lesson/Best Practice)의 내부 포맷과 회수 인터페이스 상세는 04 소관이다. 이 spec은 단일 Port 경유와 기록 시점(Memory Update 단계)만 정의했다.
- **05-lessons 조율 필요.** Lesson 후보의 생성 규칙·포맷·승격(promotion) 및 Best Practice 기록 규칙은 05 소관이다. 이 spec은 Learn 트리거 시점과 후보 종류(실패→Lesson 후보, 성공→Best Practice 후보)만 정의했다.
- **07-workflow 조율 필요.** 여러 Loop 사이클의 분해·병렬 디스패치·병합은 07 소관이다. 이 spec은 단일 작업의 단일 Lifecycle 사이클만 정의했다.

## Glossary 추가 요청 (Glossary §9-OQ6 흐름 — 01-runtime §9 선례와 동일 패턴)

용어 3종(재작업 루프 Rework Loop · 루프 상태 기록 Loop State Record · 단계 전이 Stage Transition)은 00-glossary §3.2-J-03 정본 등재 완료(요청 3건 전부 Advisor 승인). 상세 정의의 정본은 이 spec(§3.1-A/B·§3.2-A)이 유지하고 Glossary는 참조한다.

참고: "검증 게이트", "재시도 한도", "사람 개입 지점"은 위 용어와 ROADMAP/AGENT.md 원문에서 파생된 서술적 표현으로 사용했으며, 별도 정본 용어로 신설하지 않았다.

## 상위 규약 원칙 참조 등록 요청

**Human Approval**(AGENT.md Core Principles — 이 spec §3.1-D가 계약화) 참조 등록은 00-glossary §3.2-H 등재 완료(Advisor 승인). 이 spec은 새 정의를 만들지 않고 AGENT.md 원칙을 참조했다.

## 잠재 불일치 보고 (비차단 — 자동 해석하지 않고 보고)

- **AGENT.md Lifecycle 다이어그램의 선형성** — 해소(이 spec이 더한 재작업 루프(§3.1-B)·에스컬레이션 분기(§3.1-C)·종료 전 Learn 보장(INV-5)은 단계 전이 규칙의 구체화이며 성공 경로의 선형 순서를 위반하지 않는다. 상위 규약 수정 불필요 — Advisor 확인 완료 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

## 결정 기록 (Advisor — Wave 4 통합)

- 게이트-단계 매핑(CP2 PASS=Verify 통과, CP3=Complete 진입 게이트) 승인.
- Glossary 추가 요청 3건 승인 — Glossary §3.2-J 반영. Human Approval 참조 등록 승인 — Glossary §3.2-H 반영.
- AGENT.md 선형성: 재작업 루프·에스컬레이션 분기·종료 전 Learn 보장은 Lifecycle의 구체화이며 성공 경로 순서를 위반하지 않는다. 상위 규약 수정 불필요 — 확인 완료.
- 06/04/05/07 조율: 각 spec 완성 후 대조 결과 모순 없음 (06 §9-OQ-V1, 04 §9, 05 §9, 07 §9와 상호 확인).

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 항목(01·02 정합 확인 · AGENT.md 선형성)의 원문+답 이중 잔존 1줄화, Glossary 추가 요청·Human Approval 참조 등록 블록의 등재 완료 1줄화, §2 stale 상태 표기(Review/Adopted → Frozen) 현행 정정. 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — §3.1-A~D·§3.2·§8 상태기계 워크스루 무촉, dependents(§2 목록 = 07) 참조 영향 0(정책 §4-a·§4-c). 종전 문면 = git 앵커 90ca19c.
