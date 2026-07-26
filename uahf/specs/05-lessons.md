# specs/05-lessons — Lessons Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05 · 2026-07-26 정합(격리 개정 — 슬림화·앵커 90ca19c))
근거: ARCHITECTURE.md 0.2 (특히 3.5 Learn from Failure, 5.1 Memory Service)
상위 규약: AGENT.md

---

# §1. Purpose

Lessons는 UAHF가 실패에서 배우고 성공을 재사용하는 특화 계약이다.

Lessons는 세 가지 문제를 해결한다.

- 반복되는 동일한 실수 문제. 실패를 교훈(Lesson)으로 기록하고 다음 작업에서 회수해 같은 실수를 막는다.
- 성공이 휘발되는 문제. 성공을 모범 사례(Best Practice)로 기록하고 재사용한다.
- "학습했다"를 검증할 수 없는 문제. 같은 실수의 반복 여부를 판정 가능한 계약으로 만든다.

## 책임 (1~3문장)

Lessons는 Lesson과 Best Practice의 포맷·생성·회수·효과 추적을 정의한다.

Lessons는 Memory Service 위의 특화 계약이다 (ARCHITECTURE 5.1, Glossary §3.2-C). Layer가 아니다.

모든 저장·회수는 Memory Service Interface(단일 Port)를 경유한다. Lessons는 그 Port 위의 계약만 정의한다.

## Non-Goals

- Memory store의 내부 구조·인덱스·영속성을 정의하지 않는다 — specs/04-memory.md 소관이다. Lessons는 Port 위 특화 계약만 정의한다.
- Agent Lifecycle의 Learn·Memory Update 단계 전이 규칙을 정의하지 않는다 — specs/03-loop.md 소관이다. Lessons는 연산 계약만 정의한다.
- Agent 역할 경계·위임/보고 포맷을 정의하지 않는다 — specs/02-agent.md 소관이다. Lessons는 그 포맷을 입력으로 소비한다.
- Verifier의 상세 판정 기준을 정의하지 않는다 — specs/06-verifier.md 소관이다.
- 특정 AI·매칭 알고리즘·검색 엔진·직렬화 포맷을 정의하지 않는다 — Adapter Binding(§4)과 04 소관이다.

---

# §2. Position

- 아키텍처 상 위치: Cross-cutting Service(Memory Service) 위의 특화 계약. Layer가 아니다 (Glossary §3.2-C, INV-2). Core Component "Lessons"(Glossary §3.2-D)의 규격 문서다.
- Lessons는 스택의 특정 위치를 차지하지 않는다. 회수는 매 Consult에서, 기록은 매 Memory Update에서 일어나므로 모든 Layer를 관통하는 Memory Service를 통해 소비된다.

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 3.5 Learn from Failure, 5.1 Memory Service, 3.6 Token Efficiency.
- specs/00-glossary.md (실재, Frozen) — 모든 용어의 정본. 특히 §3.2-C Lessons·Best Practice·회수 정책·Memory Service Interface.
- specs/TEMPLATE.md (실재, Frozen) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약. 특히 Memory("모든 실패는 Lesson 후보", "모든 성공은 Best Practice 후보")와 Agent Lifecycle.
- specs/02-agent.md (실재, Frozen) — 실패 보고(§3.2-D)의 `lesson_candidate`, 완료 보고(§3.2-C), Memory Access(§5), 역할 경계(§3.2-A)를 입력·근거로 인용한다.
- specs/01-runtime.md (실재, Frozen) — Memory Service를 교체 가능한 Module로 배선하는 방식(§5). 참조만.
- ROADMAP.md v0.4 (실재) — Memory & Lessons 완료 조건과 산출물.

(상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·01·02·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`. 종전 "Review"·"Adopted" 표기는 작성 시점 기록이었다.)

## 이 spec에 의존하는 spec (dependents)

- specs/03-loop.md — Loop Engine이 Learn·Memory Update 단계에서 이 spec의 생성·승격·회수·재발 판정 연산을 구동한다. 단계 전이는 03이 소유하고, 연산 계약은 05가 소유한다.
- specs/06-verifier.md — Verifier는 Verify 단계의 독립 판정을 Learn 입력으로 제공한다 (02 §3.1). 이 입력이 승격(§3.1-A)의 근거가 된다.
- specs/07-workflow.md 및 모든 Agent — Consult에서 회수를, Memory Update에서 기록을 이 계약을 통해 소비한다. 접근 경로는 Memory Service Interface 하나다.

## 순환 의존

없다.

- 05는 02의 보고 포맷(§3.2-C/D)과 Memory Service Interface(단일 Port)에 의존한다.
- 02는 "Lesson의 생성·회수는 §5와 specs/05-lessons.md가 정의한다"(02 §3.2-D, §5)로 05를 **포인터로만** 연결한다. 02의 계약은 05 내용 없이 완결되며 05의 상세에 기능적으로 의존하지 않는다. 따라서 02 ↔ 05 순환은 없다.
- 04는 Memory store를 소유하고 05는 그 Port 위에 얹힌다. 의존 방향은 05 → Port(04 소관 표면)이며 04 → 05 방향 의존은 없다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 매칭 알고리즘·검색 엔진·직렬화·실행 모델 바인딩은 전부 §4와 04 소관이다.

Lessons는 네 가지 계약을 정의한다.

- 생성·승격 계약 (§3.1-A, §3.2-A)
- 회수 계약 (§3.1-B, §3.2-C)
- 효과 추적 계약 (§3.1-C, §3.2-E)
- Best Practice 대칭 계약 (§3.1-D, §3.2-B)

모든 연산의 저장·회수는 Memory Service Interface(단일 Port)를 경유한다 (INV-1). 모든 연산의 실패는 공통 실패 보고(§3.2-F) 구조로 보고한다.

---

## 3.1 Interface

### A. 생성·승격 연산 (Lesson)

**Register Candidate (후보 등록)**
- 입력: 02 §3.2-D 실패 보고 1건 — `reason`·`repro`·`attempted`·`lesson_candidate`·`blocking` + 출처 작업 참조.
- 출력: Lesson 레코드 1건 (status = `Candidate`, §3.2-A).
- 완료 조건: `lesson_candidate.여부 = 예`인 실패는 정확히 하나의 Candidate로 등록되고, provenance(§3.2-D)가 채워지며, Memory Service Interface를 통해 기록된다. `여부 = 아니오`인 실패도 후보 자격은 유지된다 (INV-3) — 자동 등록되지는 않으나 승격 심사에서 재평가 대상이 된다.
- 실패 보고: reason = `InvalidSource`(실패 보고 형식 아님) | `MissingProvenance` | `PortWriteFailed`.

**Promote (승격 — Candidate → Active)**
- 입력: Lesson Candidate 1건 + Verifier가 제공한 Learn 입력(독립 판정 결과, 02 §3.1) + Advisor 승격 승인.
- 출력: 정식 Lesson (status = `Active`) — 안정적 `id`와 매칭 가능한 `applicability`(§3.2-A)를 갖는다.
- 완료 조건: 승격 조건(§3.2-A 승격 규칙)을 만족하고, Advisor가 승격을 승인한다 (INV-4). Verifier의 Learn 입력이 근거로 첨부된다.
- 실패 보고: reason = `PromotionCriteriaUnmet` | `NotApproved`(Advisor 승인 없음) | `PortWriteFailed`.

주의: 승격이 어느 시점에(Learn → Memory Update 전이) 호출되는지는 specs/03-loop.md 소관이다. 이 spec은 "누가 어떤 조건으로 승격하는가"의 권한·조건 계약만 정의한다.

### B. 회수 연산

**Recall (회수)**
- 입력: 현재 작업의 상황 서술자(situation descriptor) + 회수 목적 + 회수 범위 한도(회수 정책).
- 출력: `applicability`가 현재 상황과 매칭되는 Active Lesson·Active Best Practice의 **최소 집합**.
- 완료 조건: 적용 조건 매칭(§3.2-C)이 수행되고, 회수 정책(필요할 때만·목적 명시·최소 범위, Glossary §3.2-C)을 준수하며, Memory Service Interface를 경유한다. 매칭이 없으면 빈 집합을 반환한다(실패 아님).
- 시점: Consult 단계 (02 §5). 단계 전이는 03 소관.
- 실패 보고: reason = `PortReadFailed` | `ScopeExceeded`(최소 범위 초과 요청).

### C. 효과 추적 연산

**Judge Recurrence (재발 판정)**
- 입력: 새 실패의 signature(실패 보고에서 도출) + 그 작업에서 회수된 Lesson 집합(회수 이력) + `applicability`가 매칭되는 기존 Active Lesson(Port 조회).
- 출력: 판정 결과 ∈ { `Novel`, `RecallGap`, `Recurrence` } + 재발 판정 레코드(§3.2-E).
  - `Novel` — 매칭되는 기존 Lesson이 없다. → 신규 후보 등록 대상.
  - `RecallGap` — 매칭되는 Lesson이 존재했으나 그 작업의 회수 집합에 없었다. → **회수 규칙/적용 조건의 결함**이며 Lesson 내용 결함이 아니다.
  - `Recurrence` — 매칭되는 Lesson이 존재하고 회수되었음에도 같은 실패가 발생했다. → **"같은 실수 반복"**이며 Lesson 효과 미달이다.
- 완료 조건: 새 실패 signature가 기존 Lesson `applicability`와 대조되어 세 결과 중 정확히 하나로 분류되고, 판정 레코드가 Port를 통해 기록된다.
- 근거: 이 연산이 ARCHITECTURE 3.5 "같은 실수를 반복하지 않는다"를 검증 가능한 판정으로 환원한다 (INV-7).
- 실패 보고: reason = `SignatureUnmatchable` | `PortReadFailed` | `PortWriteFailed`.

### D. Best Practice 대칭 연산

**Register Best Practice Candidate / Promote (Best Practice)**
- 입력: 02 §3.2-C 완료 보고 1건(Verify 통과) — `artifacts`·`self_check`·`verify_basis` + 출처 작업 참조.
- 출력: Best Practice 레코드(§3.2-B). Candidate → Active 승격은 Lesson과 동일한 권한·절차를 따른다 (INV-4, INV-9).
- 완료 조건: Verify를 통과한 완료 보고에서 재사용 가능한 practice가 도출되고, provenance가 채워지며, Advisor가 승격을 승인한다.
- 실패 보고: Lesson 연산과 동일한 코드 집합(§3.2-F)을 사용한다.

주의: 02 §3.2-C 완료 보고에는 `lesson_candidate`와 대칭인 명시 필드가 없다. "모든 성공은 Best Practice 후보"(AGENT.md)이므로 후보 자격은 Verify를 통과한 모든 완료 보고에 보편적으로 성립한다. 명시 필드 추가 여부는 02 결정 사항으로 §9에 기록한다.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)과 매칭 구현은 Adapter Binding(§4)과 04가 정한다.

### A. Lesson (교훈) 스키마

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Lesson 고유·안정 식별자. 회수·재발 판정·supersede의 기준. | 예 |
| `status` | `Candidate` / `Active` / `Superseded` / `Retired`. | 예 |
| `failure` | 무엇이 실패했는가 — 실패 현상 서술. 출처 실패 보고의 `reason`·`repro`에서 도출. | 예 |
| `cause` | 원인 — 왜 실패했는가 (근본 원인). | 예 |
| `lesson` | 교훈 — 다음에 무엇을 다르게 할 것인가. 실행 가능한 지시. | 예 |
| `applicability` | 적용 조건 — 언제 이 Lesson이 회수되어야 하는가. 회수 매칭 signature(§3.2-C). | 예 |
| `provenance` | 출처 — 어느 작업·실패 보고에서 생성됐는가(§3.2-D). | 예 |
| `supersedes` | 이 Lesson이 대체하는 이전 Lesson `id`. 재발 대응 시 사용. | 아니오 |

**승격 규칙 (Candidate → Active).** 다음을 모두 만족해야 승격된다.

1. `failure`·`cause`·`lesson`·`applicability`·`provenance`가 모두 채워져 있다 (검증 가능성, INV-5).
2. Verifier의 Learn 입력(독립 판정)이 실패의 실재를 뒷받침한다.
3. Advisor가 승격을 승인한다 (승격 권한은 Advisor에 있다, INV-4). Worker는 후보를 제출하고 Verifier는 근거를 제공하나 승격을 결정하지 않는다.

### B. Best Practice (모범 사례) 스키마

Lessons와 대칭이다 (Glossary §3.2-C).

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | 고유·안정 식별자. | 예 |
| `status` | `Candidate` / `Active` / `Superseded` / `Retired`. | 예 |
| `success` | 무엇이 성공했는가 — 성공 현상·맥락. 출처 완료 보고에서 도출. | 예 |
| `practice` | 모범 사례 — 재사용 가능한 방법. 다음에 무엇을 반복할 것인가. 실행 가능한 지시. | 예 |
| `applicability` | 적용 조건 — 언제 회수되어야 하는가(§3.2-C). | 예 |
| `provenance` | 출처 — 어느 작업·완료 보고에서 생성됐는가(§3.2-D). | 예 |
| `supersedes` | 대체하는 이전 Best Practice `id`. | 아니오 |

대칭 대응: `Lesson.failure` ↔ `BestPractice.success`, `Lesson.cause`+`Lesson.lesson` ↔ `BestPractice.practice`. `id`·`status`·`applicability`·`provenance`는 두 스키마가 동일한 형태를 공유한다.

### C. Applicability Condition (적용 조건)

회수 매칭의 기준이 되는 추상 signature다.

- 구성: 상황 유형(situation type)과 트리거 서술(어떤 맥락·작업 특성에서 이 기록이 관련되는가)의 집합.
- 회수 시 현재 작업의 상황 서술자(situation descriptor)와 대조되어 관련성(relevance)이 산출된다.
- AI 비의존: 계약은 "적용 조건과 상황 서술자를 대조해 관련성을 산출한다"만 요구한다. 대조 알고리즘(키워드·의미 검색·임베딩 등)은 규정하지 않는다 — Adapter/04 소관이다.

### D. Provenance (출처)

출처 없는 Lesson·Best Practice는 성립하지 않는다 (INV-5).

| 필드 | 의미 |
|---|---|
| `task_ref` | 어느 작업에서 생성됐는가. |
| `report_ref` | 원천 보고 참조 — 실패 보고(02 §3.2-D) 또는 완료 보고(02 §3.2-C). |
| `origin_role` | 후보를 제출한 역할(예: Worker)과 승격을 승인한 역할(Advisor). |
| `ordering_ref` | 생성 순서를 판정할 수 있는 순서 기준. 재발 판정의 "기존 Lesson이 작업 착수 전에 존재했는가"에 사용. 구체 시간 포맷은 직렬화(§4) 소관. |

### E. Recurrence Judgment (재발 판정 레코드)

효과 추적 연산(§3.1-C)의 산출물이다.

| 필드 | 의미 |
|---|---|
| `failure_signature` | 판정 대상 새 실패의 signature. |
| `matched_lesson_id` | 매칭된 기존 Active Lesson의 `id`(있으면). |
| `was_recalled` | 그 Lesson이 해당 작업의 회수 집합에 포함되었는가. |
| `verdict` | `Novel` / `RecallGap` / `Recurrence`(§3.1-C). |
| `follow_up` | 후속 조치 참조 — 신규 후보 등록 / 회수 규칙·적용 조건 조정 / Lesson 강화·supersede. |

### F. Failure Report (Lessons 연산 공통)

모든 Lessons 연산의 공통 실패 보고 구조다.

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (RegisterCandidate / Promote / Recall / JudgeRecurrence / RegisterBestPractice). |
| `reason` | 사유 코드 (InvalidSource / MissingProvenance / PromotionCriteriaUnmet / NotApproved / PortReadFailed / PortWriteFailed / ScopeExceeded / SignatureUnmatchable). |
| `target` | 대상 (Candidate/Lesson/Best Practice `id`, 또는 출처 보고 참조). |
| `location` | 실패 지점 참조. |

---

## 3.3 Invariants

- **INV-1 (단일 Port).** 모든 Lesson·Best Practice·재발 판정 레코드의 저장·회수는 Memory Service Interface(단일 Port)를 경유한다 (ARCHITECTURE 5.1). Lessons는 영속성 백엔드에 직접 접근하지 않는다.
- **INV-2 (Layer 아님).** Lessons는 Layer가 아니다. Memory Service 위의 특화 계약이다 (Glossary §3.2-C, Glossary INV-2).
- **INV-3 (보편 후보 자격).** 모든 실패는 Lesson 후보 자격을 갖는다 (AGENT.md). 후보는 승격 절차(§3.2-A)를 거쳐야 정식 Lesson(`Active`)이 된다. `lesson_candidate.여부 = 아니오`도 자격을 소멸시키지 않는다.
- **INV-4 (승격 권한).** 승격(`Candidate → Active`)은 Advisor 승인으로만 성립한다 (역할 경계, 02 §3.2-A). Worker는 후보를 제출하고, Verifier는 Learn 입력을 제공하며, 승격 결정 권한은 Advisor에 있다. Best Practice 승격도 동일하다.
- **INV-5 (출처 필수).** 모든 Active Lesson·Active Best Practice는 provenance(§3.2-D)를 갖는다. 출처 없는 교훈·모범 사례는 성립하지 않는다.
- **INV-6 (최소 회수).** 회수는 회수 정책(필요할 때만·목적 명시·최소 범위)을 준수한다 (Token Efficiency, ARCHITECTURE 3.6). 전량 로드는 위반이다.
- **INV-7 (재발 판정).** 적용 조건이 매칭되고 회수되었음에도 같은 실패가 재발하면 `Recurrence`로 판정된다. 이것이 ARCHITECTURE 3.5 "같은 실수를 반복하지 않는다"의 검증 가능화다.
- **INV-8 (대칭).** Best Practice는 Lessons와 대칭이며 동일한 저장·회수·승격 계약을 따른다. 실패에서 Lesson이, 성공에서 Best Practice가 도출된다 (Glossary §3.2-C).
- **INV-9 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·매칭 구현·검색 엔진·직렬화에 의존하지 않는다. 그 실현은 §4·04·Adapter 소관이다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Lesson·Best Practice·재발 판정 레코드 직렬화 | Memory store 뒤의 Adapter가 정한다(04·Adapter). Lessons는 스키마(§3.2)만 정의한다. |
| 후보 제출 흐름 | Worker의 실패 보고(02 §3.2-D)가 서브에이전트 최종 응답으로 회수되고, 그 `lesson_candidate`가 Register Candidate 입력이 된다. |
| 승격 승인 주체 | Advisor 역할이 승격을 승인한다. 실행 모델 지정은 02 §4 소관(참조). |
| Verifier Learn 입력 | Verifier 서브에이전트의 독립 판정 결과가 승격 근거로 첨부된다. |
| 회수 흐름 | Consult 단계에서 Agent가 Memory Service Interface로 상황 서술자를 질의해 최소 집합을 받는다. |
| 적용 조건 매칭 구현 | 상황 서술자 ↔ `applicability` 대조 알고리즘은 Adapter/04 구현 선택(키워드·의미 검색 등). |
| 저장 위치 | Memory store 경계 뒤. Core 디렉터리와 분리된 Adapter 경계에 격리. |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부. §3 Core Contract는 유지된다.

- SP-1: 레코드 직렬화·저장 위치 → 대상 환경 Memory store Adapter(04·Adapter).
- SP-2: 적용 조건 매칭 구현(대조 알고리즘) → 대상 환경의 매칭 메커니즘.
- SP-3: 후보 제출·회수의 물리 채널(보고 회수·세션) → 대상 환경의 결과 반환·컨텍스트 주입 채널.
- SP-4: 승격 승인 주체의 실행 모델 지정 → 02 §4 소관(Lessons는 참조만).

유지되는 것: §3.2 스키마 필드, 승격 권한 경계(INV-4), 회수 정책(INV-6), 재발 판정 3분류(§3.1-C), Lesson↔Best Practice 대칭(INV-8).

---

# §5. Memory Access (해당 시)

Lessons는 Memory Service의 소비자이자 그 위의 특화 계약이다. 모든 접근은 Memory Service Interface(단일 Port)를 경유한다 (INV-1, ARCHITECTURE 5.1).

## 읽기 (Recall)

- 목적: Consult 단계에서 현재 작업에 관련된 Active Lesson·Best Practice를 회수한다 (02 §5). 재발 판정 시 매칭 Lesson을 조회한다.
- 범위: 회수 정책에 따라 최소 범위로. 적용 조건이 매칭되는 최소 집합만 읽는다. 전량 로드하지 않는다 (INV-6, Token Efficiency).
- 시점: 필요할 때만. 매 사이클 무조건 전량 로드하지 않는다.

## 쓰기 (Record)

- 기록 대상: Register Candidate로 생성된 Lesson Candidate, 승격된 Active Lesson·Best Practice, 재발 판정 레코드(§3.2-E).
- 시점: Memory Update 단계 (02 §5). 단계 전이는 03 소관.
- 조건: 모든 기록은 provenance를 포함한다 (INV-5).

## 경계

Memory store의 내부 구조·인덱스·영속성은 04 소관이다. Lessons는 Port 위의 특화 계약(무엇을·어떤 조건으로 저장·회수하는가)만 정의하고, 어떻게 저장·색인되는가는 정의하지 않는다. Lessons가 Port에 요구하는 연산 표면은 §9에 "04 조율 필요"로 기록한다.

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다.

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| 실패했으나 Candidate 미등록 (`lesson_candidate` 누락) | INV-3 위반. 검증(§7)에서 미등록으로 판정. | 예 |
| Advisor 승인 없이 `Active`로 승격 | INV-4 위반. Promote 거부(reason=NotApproved). | 예 |
| 출처 없는 Lesson·Best Practice 생성 | INV-5 위반. 무효. reason=MissingProvenance. | 예 |
| 회수 시 전량 로드 | INV-6 위반. 회수 정책 위배. Token Efficiency 저해. | 예 |
| 적용 Lesson이 존재했으나 미회수 → 실패 반복 | `RecallGap` 판정. 회수 규칙·적용 조건 조정. | 예 |
| 회수됐음에도 같은 실패 재발 | `Recurrence` 판정. Lesson 강화 또는 supersede. | 예 |
| Port를 우회해 영속성 백엔드 직접 접근 | INV-1 위반. 단일 Port 경유로 교정. | 예 |
| 매칭되는 Lesson 없음(신규 실패) | 실패 아님. `Novel` 판정 → 신규 후보 등록. | 해당(신규 Lesson) |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.4 완료 조건과 정렬한다.

- **학습 사이클 시연 (ROADMAP v0.4 핵심).** 한 작업의 실패 보고 `lesson_candidate`(여부=예) → Register Candidate → Verifier Learn 입력 → Advisor 승격 → Active Lesson → **다음 작업 Consult에서 적용 조건 매칭으로 회수**됨을, 실패 → Lesson 생성 → 회수의 끊김 없는 사이클로 보인다.
- **최소 회수 시연.** 회수가 전량이 아니라 적용 조건이 매칭되는 최소 집합만 반환함을 보인다 (INV-6, Token Efficiency).
- **단일 Port 시연.** 모든 저장·회수가 Memory Service Interface를 경유함을 보인다 (INV-1).
- **승격 권한 시연.** Advisor 승인 없는 승격이 차단됨(reason=NotApproved)을 보인다 (INV-4).
- **재발 판정 시연.** 같은 실패가 (a) 회수된 Lesson과 겹치면 `Recurrence`, (b) 존재하나 미회수면 `RecallGap`, (c) 매칭 없으면 `Novel`로 분류됨을 케이스로 보인다 (INV-7 — "같은 실수를 반복하지 않는다"의 검증 가능화).
- **Best Practice 대칭 시연.** 성공 완료 보고 → Best Practice 생성 → 회수가 Lessons와 동일 계약으로 동작함을 보인다 (INV-8).
- **AI 비의존 시연.** §3 본문에 특정 AI 모델명·제품 기능·매칭 구현 참조가 0건임을 보인다 (INV-9, DoD-3).

## 검증 방법

- Verifier가 학습 사이클의 각 단계 산출물(실패 보고 → Candidate → Active Lesson → 회수 결과)을 순서대로 대조한다.
- Verifier가 회수 결과가 적용 조건 매칭 집합과 일치하고 전량이 아님을 확인한다.
- Verifier가 모든 접근 경로가 Memory Service Interface임을 확인한다.
- Verifier가 승격 승인 주체가 Advisor임을 §3.2-A 승격 규칙과 대조한다.
- Verifier가 재발 판정 3분류를 세 케이스로 확인한다.
- Verifier가 §3 본문을 스캔해 AI 의존 토큰(모델명·제품 기능명·매칭 엔진명)이 0건임을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 실패 → Lesson → 회수 사이클 (ROADMAP v0.4 대표)**

작업 T1에서 Worker가 실패 보고를 남긴다 (02 §8 예3 재사용):
- reason: 의존 인터페이스 미확정
- lesson_candidate: 여부 = 예 — "의존 계약 미확정 시 착수 전 조율 필요"

→ Register Candidate: status=`Candidate`, provenance(task_ref=T1, report_ref=T1 실패 보고).
→ Verifier가 Learn 입력(실패 실재 확인)을 제공한다.
→ Advisor가 승격을 승인한다 → 정식 Lesson L1 (status=`Active`):
  - failure: 의존 인터페이스 미확정 상태에서 착수해 진행 불가.
  - cause: 착수 전 의존 계약 정합을 확인하지 않음.
  - lesson: 의존 계약이 미확정이면 착수 전에 조율한다.
  - applicability: "의존 인터페이스가 확정되지 않은 작업에 착수하려는 상황".
→ 다음 작업 T2의 Consult: T2 상황 서술자가 L1의 applicability와 매칭 → L1이 최소 범위로 회수된다.
→ T2는 착수 전 의존 계약을 조율한다 → 같은 실패를 회피한다.

**예 2 — 재발 판정 (효과 추적)**

작업 T3에서 L1 적용 상황의 실패가 다시 발생한다.
- L1이 T3 Consult에서 회수되었는데도 같은 실패 → `Recurrence`. L1의 `lesson`을 강화하거나 supersede하는 새 Lesson을 만든다.
- L1이 존재했으나 T3 회수 집합에 없었다면 → `RecallGap`. L1의 `applicability` 또는 회수 규칙을 조정한다(Lesson 내용 결함이 아니다).
- 매칭되는 기존 Lesson이 없었다면 → `Novel`. 신규 후보로 등록한다.

**예 3 — Best Practice (대칭)**

작업 T4가 성공으로 완료 보고된다(Verify 통과). "위임 전 의존 계약을 먼저 조율하니 재작업이 없었다"가 도출된다.
→ Register Best Practice Candidate → Advisor 승격 → Active Best Practice BP1:
  - success: 위임 전 의존 계약 조율로 재작업 0.
  - practice: 위임 전에 의존 계약 정합을 먼저 확인한다.
  - applicability: "여러 작업이 공통 의존 계약을 공유하는 위임 상황".
→ 다음 유사 작업의 Consult에서 Lessons와 동일한 회수 계약으로 회수된다.

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**04 조율 필요 (Memory Service Interface에 요구하는 연산 표면):**

- 04 조율 3건 — 해소. (a) 타입 지정 레코드 쓰기(Lesson/Best Practice/재발 판정) = Memory Item `kind`로, 적용 조건 매칭 기반 범위 조회 = `scope`(kind/labels)로 충족(provenance·ordering_ref 보존 포함). (b) 적용 조건 매칭의 **계약 표면**은 05 소유·**구현**(알고리즘)은 Adapter 소관(04 §9 동일 기록). (c) "작업별 회수 집합(회수 이력)" 조회는 03 루프 상태 기록 소관이며 05는 입력으로 받는다. Lessons는 내부 인덱스·저장 구조·색인 방식을 규정하지 않는다. (상세 = 결정 기록 소절·git 앵커 90ca19c.)

**03 조율 필요:**

- 03 조율 필요: Learn·Memory Update 단계 전이(언제 Register Candidate·Promote·Judge Recurrence가 호출되는가)는 specs/03-loop.md 소관이다. 이 spec은 연산의 권한·조건 계약만 정의하고 단계 전이는 침범하지 않았다. 두 계약이 정합해야 한다.

**02 조율 (비차단):**

- 02 조율: 완료 보고(02 §3.2-C)에 `lesson_candidate` 대칭인 `best_practice_candidate` 명시 필드 부재 — 해소(v0.1은 보편 후보 자격("모든 성공은 Best Practice 후보" — AGENT.md)으로 충족. 02 수정 보류 — v0.2 이후 재검토. 비차단 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

**상위 규약 정합 (비차단):**

- AGENT.md Memory("모든 실패는 Lesson 후보")와 02 §3.2-D `lesson_candidate.여부`(예/아니오)의 관계 — 해소(승인된 정합 해석 = 모든 실패가 후보 **자격**을 가지며(INV-3), 여부=예이면 즉시 Candidate 등록, 여부=아니오라도 자격은 유지되어 승격 심사에서 재평가된다. 하드 충돌 아님 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

**Glossary 추가 요청** — 용어 3종(적용 조건 Applicability Condition · 승격 Promotion · 재발 Recurrence)은 00-glossary §3.2-J-05 정본 등재 완료(요청 3건 전부 Advisor 승인). 상세 필드·판정의 정본은 이 spec(§3.1-A/C·§3.2-C)이 유지한다.

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 3.5(Learn from Failure)·5.1(Memory 단일 Port·Lessons 특화 계약)·3.6(Token Efficiency)과 Glossary §3.2-C 정의에 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

- 04 조율 3건 해소: (a) 타입 지정 쓰기는 Memory Item kind로, 범위 조회는 scope(kind/labels)로 충족. (b) 매칭 계약 표면은 05 소유·구현은 Adapter (04 §9 동일 기록). (c) 회수 이력은 03 루프 상태 기록 소관, 05는 입력으로 받는다.
- 02 best_practice_candidate 필드: v0.1은 보편 후보 자격(AGENT.md)으로 충족. 02 수정 보류 — v0.2 이후 재검토.
- 상위 규약 정합 해석(모든 실패 = 후보 자격 보유, 여부=예는 즉시 등록) 승인.
- Glossary 추가 요청 3건 승인 — Glossary §3.2-J 반영.

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 항목(04 조율 3건·02 조율·상위 규약 정합)의 원문+답 이중 잔존 1줄화, Glossary 추가 요청 블록의 등재 완료 1줄화, §2 stale 상태 표기(Review/Adopted → Frozen) 현행 정정. 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — §3 전체·§6 표·§7 무촉, dependents(§2 목록 = 03·06·07) 참조 영향 0(정책 §4-a·§4-c). 종전 문면 = git 앵커 90ca19c.
