# specs/06-verifier — Verifier Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05)
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Verifier는 완료를 판정하는 컴포넌트다.

ARCHITECTURE.md 3.4는 "검증되지 않은 결과는 완료가 아니다"라고 선언한다. Verifier는 이 원칙을 검증 가능한 계약으로 구체화한다.

## 이 컴포넌트가 해결하는 문제

- 완료 보고를 그대로 믿으면 거짓 완료가 통과한다.
- 판정 기준이 없으면 검증이 사람마다 달라진다.
- 검사 범위가 명시되지 않으면 좁은 검사로 넓은 결론을 낸다.
- 재작업 지시가 없으면 실패가 교정으로 이어지지 않는다.

## 책임 (1~3문장)

Verifier는 Worker 완료 보고(specs/02-agent.md §3.2-C)를 그대로 신뢰하지 않고, 산출물 자체를 근거로 완료 여부를 독립 판정한다.

Verifier는 판정 기준 카탈로그·검증 리포트·재작업 지시·독립성 계약을 소유한다.

## Non-Goals

- Verify 단계가 Lifecycle에서 언제 실행되고 어디로 전이하는지 정의하지 않는다 — specs/03-loop.md 소관이다.
- Agent 역할의 공통 계약(역할 경계·위임·보고 포맷)을 재정의하지 않는다 — specs/02-agent.md 소관이다. 이 spec은 그 계약을 판정 대상으로만 참조한다.
- Lesson의 생성·회수 내부 규칙을 정의하지 않는다 — specs/05-lessons.md 소관이다.
- 산출물을 구현·수정하지 않는다 — 구현은 Worker 소관이다 (02 §3.2-A).
- 최종 승인(재량 판정)을 하지 않는다 — 최종 승인은 Advisor 소관이다 (02 §3.2-A).
- 설계 원칙을 재정의하지 않는다. ARCHITECTURE.md를 참조로만 연결한다.

---

# §2. Position

- 아키텍처 상 위치: Core Component "Verifier" (Glossary §3.2-D)의 규격 문서다. 판정을 수행하는 Verifier는 Agent 역할(Glossary §3.2-E)이며 Agent Layer에서 Verify 단계의 독립 판정을 수행한다.
- 이 spec은 판정 기준·검증 리포트·재작업 지시·독립성 계약을 소유한다. 판정을 수행하는 실행 단위는 Runtime이 호스팅하는 하나의 Module이다 (specs/01-runtime.md §3.2-A, §4.1 `framework/verifier/`).

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 특히 3.4 Verify Everything. 최상위 기준.
- specs/00-glossary.md (실재, Review) — 모든 용어의 정본.
- specs/TEMPLATE.md (실재, Adopted) — 문서 구조와 DoD. DoD 8항목 자체가 규격 준수 검증(§3.2-E VT-3)의 대표 대조 기준이다.
- .claude/AGENT.md (실재) — 상위 규약. 특히 Verification, Memory.
- specs/02-agent.md (실재, Review) — 역할 경계(§3.2-A), 완료 보고(§3.2-C), 실패 보고(§3.2-D). 판정 대상 계약이다.
- specs/01-runtime.md (실재, Review) — Verifier Module 호스팅 계약, Failure Report(§3.2-D) 구분.
- ROADMAP.md v0.5 (실재) — Verifier 완료 조건과 산출물.

## 이 spec에 의존하는 spec (dependents)

- specs/03-loop.md — Loop가 Verify 단계에서 이 판정을 구동·소비하고, Fail 시 재작업 루프를 돌린다.
- specs/07-workflow.md — Workflow의 병합·검증이 이 판정 계약을 소비한다.
- specs/05-lessons.md — 검출된 위반·거짓 완료 보고가 Lesson 후보가 된다.

## 순환 의존

없다. 이 spec은 00·01·02에 의존한다. 03·05·07이 이 spec에 의존하는 방향(하위 → 06)이다. 06은 03·05·07의 내용에 의존하지 않으며, 그 내용을 추측·인용하지 않았다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 AI·환경 의존 실현은 §4에 둔다.

Verifier는 세 가지 계약을 정의한다.

- 판정 연산 계약 (§3.1)
- 검증 리포트·판정 값·검증 유형·재작업 지시 포맷 (§3.2)
- 독립성·근거·범위 정직·결정성 불변 규칙 (§3.3)

---

## 3.1 Interface

### 독립 판정 의무 (Verifier Obligations)

AGENT.md Responsibilities와 02 §3.2-A Verifier 경계의 검증 가능한 구체화다.

- V1 독립성 — 판정은 산출물 자체를 근거로 한다. Worker 완료 보고(02 §3.2-C)는 검사 대상(claim)일 뿐 판정 근거가 아니다.
- V2 대조 근거 — 모든 판정은 명시된 대조 기준(criteria)에 대해 이루어진다. 기준 없는 판정은 없다.
- V3 근거 필수 — 모든 항목별 판정에 근거(evidence)를 남긴다. 근거 없는 "충족"은 무효다.
- V4 검사 범위 정직 — 각 판정은 검사 범위(scope)를 명시한다. 좁은 범위 검사로 넓은 결론을 내지 않는다.
- V5 비구현 — Verifier는 산출물을 구현·수정하지 않는다 (02 §3.2-A). 판정만 한다.
- V6 판정 불가 불은폐 — 판정 불가(Undetermined)를 충족(Met)으로 위장하지 않는다.

### 판정 연산

Verifier는 다음 연산을 노출한다.

**Verify**
- 입력: 판정 대상 — 산출물(artifacts) + 대조 기준(criteria) 집합. 참고 입력으로 Worker 완료 보고(02 §3.2-C)를 받되, 판정 근거로 삼지 않는다 (V1).
- 출력: 검증 리포트(§3.2-A) 1건 — 항목별 판정 + 최종 판정.
- 완료 조건: 모든 대조 기준 항목이 판정되고, 각 판정에 근거와 검사 범위가 붙으며, 최종 판정이 항목별 판정에서 §3.2-C 규칙으로 결정적으로 도출된다.
- 실패 보고: Verifier 자신의 연산 실패(예: 산출물 접근 불가, 대조 기준 부재)는 실패 보고로 반환한다. 이는 판정 대상에 대한 `final_verdict = Fail`과 구분된다 (§9-OQ-V4).

주의: `final_verdict = Fail`은 Verifier의 정상 출력이다(대상이 기준을 충족하지 못했다는 판정). Verifier 연산 실패는 Verifier가 판정 자체를 수행하지 못한 상태다. 둘을 혼동하지 않는다.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식·저장 위치는 Adapter Binding(§4)이 정한다.

### A. 검증 리포트 (Verification Report)

판정의 기록 산출물이다 (ROADMAP v0.5 산출물 "검증 리포트 스키마").

| 필드 | 의미 | 필수 |
|---|---|---|
| `target` | 판정 대상 — 산출물 경로 목록과 대상 작업 식별자. | 예 |
| `criteria_basis` | 대조 기준 출처 — 무엇에 대조했는가(위임 완료 조건 / 규격 / 경계 규칙 / 시연 기준). | 예 |
| `items` | 항목별 판정 목록(§3.2-B). 최소 1건. | 예 |
| `final_verdict` | 최종 판정 — Pass / Fail / Conditional(§3.2-C). | 예 |
| `verifier_scope` | 이 검증이 실제로 검사한 범위. 검사하지 못했거나 제외한 범위를 함께 명시한다(V4). | 예 |
| `rework` | 재작업 지시(§3.2-D). `final_verdict`가 Fail 또는 Conditional일 때 필수, Pass면 "없음". | 조건부 |

### B. 항목별 판정 (Verdict Item)

| 필드 | 의미 | 필수 |
|---|---|---|
| `criterion` | 대조한 기준 1건. 검증 가능한 문장으로 표현한다. | 예 |
| `verdict` | 충족(Met) / 위반(Violated) / 판정 불가(Undetermined). | 예 |
| `evidence` | 판정 근거 — 산출물의 어느 부분이 근거인가(V3). | 예 |
| `scope` | 이 항목을 검사한 범위(V4). | 예 |
| `verification_type` | 이 항목에 적용한 검증 유형(§3.2-E, VT-1 ~ VT-5). | 예 |

판정 값 정의:
- **충족(Met)** — 기준이 산출물에서 만족됨을 근거로 확인했다.
- **위반(Violated)** — 기준이 산출물에서 만족되지 않음을 근거로 확인했다.
- **판정 불가(Undetermined)** — 근거 부족·검사 범위 한계로 충족/위반을 확정할 수 없다. 충족으로 취급하지 않는다 (V6).

### C. 최종 판정 도출 규칙 (Final Verdict Derivation)

최종 판정은 항목별 판정에서 결정적으로 도출된다 (INV-5). 동일한 항목별 판정 집합은 항상 동일한 최종 판정을 낸다.

- 모든 항목이 충족(Met) → **통과(Pass)**.
- 하나라도 위반(Violated) → **실패(Fail)**.
- 위반은 없으나 판정 불가(Undetermined)가 하나 이상 → **조건부(Conditional)**.

조건부(Conditional)는 완료가 아니다. 판정 불가 항목이 해소되어 통과로 전이하거나, 그 항목이 완료를 막지 않는다는 Advisor의 최종 판정(재량)을 받아야 한다. 재량 판정은 Verifier가 하지 않는다 (02 §3.2-A, TEMPLATE DoD-7·DoD-8).

### D. 재작업 지시 (Rework Instruction)

검증 실패 시 Worker에게 반환되는 지시다 (ROADMAP v0.5 산출물 "재작업 지시 포맷"). 전달·라우팅 채널은 03-loop·02 §4 소관이며, 이 spec은 포맷만 소유한다.

| 필드 | 의미 |
|---|---|
| `violated_items` | 위반·판정 불가 항목 목록(`criterion` + `verdict`). |
| `expected_state` | 각 항목의 기대 상태 — 무엇이 충족되어야 하는가. |
| `revalidation_criteria` | 재검증 기준 — 재작업 후 무엇을 다시 검사하면 통과인가. |
| `evidence_gap` | (판정 불가 항목에 한함) 판정을 막은 근거 부족·검사 범위 한계. |

### E. 검증 유형 카탈로그 (Verification Type Catalog)

검증은 5개 유형으로 분류한다. 각 판정 항목은 하나 이상의 유형에 대응한다 (ROADMAP v0.5 산출물 "완료 판정 기준 카탈로그").

| 유형 | 판정 대상 | 판정 방법 | 충족 조건 |
|---|---|---|---|
| **VT-1 산출물 존재 검증** | 위임 output이 지정한 산출물 | 지정 산출물이 실제로 존재하고 접근 가능한지 확인 | 모든 지정 산출물이 존재 |
| **VT-2 완료 조건 대조 검증** | 위임 완료 조건(done) 항목 | 각 완료 조건을 산출물과 항목별로 대조 | 모든 완료 조건 항목 충족 |
| **VT-3 규격 준수 검증** | 산출물이 따라야 할 규격 (예: TEMPLATE DoD 8항목, 대상 spec §7 완료 기준) | 규격의 각 항목을 산출물과 대조 | 규격 전 항목 충족 |
| **VT-4 경계 검증** | 불변 규칙·경계 (예: Core에 AI 의존 요소 0건, 역할 경계 불침범) | 금지 요소를 전수 스캔(exhaustive scan)한다. 검사 범위를 산출물의 해당 경계 전체로 명시한다 (V4) | 금지 요소 0건 |
| **VT-5 시연 검증** | "시연 가능 문장"으로 표현된 완료 기준 (TEMPLATE §7) | 시연 시나리오를 실제로 재현하고 결과를 관측 | 시연이 기대대로 관측됨 |

VT-4 판정 방법 주의: 경계 검증은 좁은 대리 지표 하나로 대체될 수 없다. 금지 요소의 후보 집합 전체(예: 특정 AI·모델명·제품 기능명 등)를 대상으로, 산출물의 해당 경계 전 범위를 검사해야 한다. 검사 범위를 `scope`에 명시한다 (V4, INV-4). 이 규칙이 §3.2-F 거짓 완료 보고 검출의 핵심이다.

### F. 거짓 완료 보고 검출 계약 (False Completion Report Detection)

Verifier는 Worker 완료 보고(02 §3.2-C)의 주장과 실제 산출물의 불일치를 검출한다 (ROADMAP v0.5 완료 조건).

불일치가 성립하는 경우:
- 완료 보고의 `self_check`가 "충족"이라 주장하나, 해당 기준에 대한 독립 판정이 위반(Violated)이다.
- 완료 보고의 `artifacts`가 지정한 산출물이 존재하지 않는다(VT-1 위반).
- 완료 보고의 `failures`가 "없음"이라 주장하나, 독립 판정에서 위반이 존재한다.
- 완료 보고의 `verify_basis`가 근거로 든 검사가 실제 필요한 범위를 덮지 못했다(좁은 범위 검사).

검출 절차:
- Verifier는 완료 보고의 주장을 신뢰하지 않고, 동일 기준을 산출물에 대해 충분한 범위로 재판정한다 (V1, V4).
- 재판정 결과가 완료 보고의 주장과 모순되면 거짓 완료 보고로 판정한다.
- `final_verdict = Fail`을 산출하고, 모순의 근거와 재작업 지시(§3.2-D)를 리포트에 포함한다.

주의: 완료 보고의 `self_check`가 정직하더라도, 그 근거가 된 검사 범위가 좁으면 거짓 완료가 통과할 수 있다. Verifier의 V4·VT-4가 그 좁은 범위를 넘어 전수 검사함으로써 검출한다 (§6, §8 예 1).

---

## 3.3 Invariants

- **INV-1 (독립성).** 판정은 산출물 자체를 근거로 한다. Worker 완료 보고는 판정 근거가 아니라 검사 대상이다.
- **INV-2 (대조 기준 필수).** 모든 판정은 명시된 대조 기준(criteria)에 대해 이루어진다. 기준 없는 판정은 무효다.
- **INV-3 (근거 필수).** 모든 항목별 판정에 근거(evidence)가 붙는다. 근거 없는 충족은 무효다.
- **INV-4 (검사 범위 정직).** 검사 범위를 명시하고, 좁은 범위 검사로 넓은 결론을 내지 않는다. 경계 검증(VT-4)은 전수 검사한다.
- **INV-5 (결정적 최종 판정).** 최종 판정은 항목별 판정에서 §3.2-C 규칙으로 결정적으로 도출된다.
- **INV-6 (비구현·비수정).** Verifier는 산출물을 구현·수정하지 않는다 (02 §3.2-A). 판정만 한다.
- **INV-7 (완료의 정의).** 검증되지 않은 결과는 완료가 아니다 (ARCHITECTURE.md 3.4). 최종 판정이 Pass가 아닌 산출물은 완료로 승인될 수 없다.
- **INV-8 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. Verifier의 실행 모델·검사 도구 바인딩은 §4에 위치한다.
- **INV-9 (경계 불가침).** Verify 단계의 시점·전이·시퀀싱은 정의하지 않는다 (03-loop 소관). Verifier는 판정 기준·검증 리포트·독립성 계약만 소유한다.
- **INV-10 (Memory 단일 Port).** Verifier는 Memory에 Memory Service Interface(단일 Port)를 통해서만 접근한다 (ARCHITECTURE.md 5.1).

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다 (ROADMAP v0.5, ARCHITECTURE.md 3.1 "Claude는 첫 번째 Adapter").

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Verifier Module 진입점 | `.claude/agents/verifier.md` — Runtime generic Module 계약의 Verifier Agent 구현 바인딩 (01-runtime §4.1). 진입점 내부 역할 계약은 02 §4 소관. |
| Verifier 구현 디렉터리 | `framework/verifier/` (01-runtime §4.1 Module 구현 디렉터리). |
| 검증 리포트(§3.2-A) 직렬화 | Markdown 리포트 파일 또는 구조화 파일. 검증 산출물 위치. |
| 판정 대상 회수 | 산출물 = 위임 output이 지정한 파일 경로. Worker 완료 보고 = 서브에이전트 최종 응답 (02 §4.1). |
| 검사 도구 바인딩 (VT-1 ~ VT-5) | 존재 확인·전수 스캔·시연 실행에 쓰는 Claude Code 표면의 도구(파일 조회, 텍스트 검색, 명령 실행 등). |
| 재작업 지시(§3.2-D) 전달 | Advisor/Loop가 Worker 서브에이전트에게 재위임 메시지로 전달한다. 전달·전이 채널은 03-loop·02 §4 소관. |
| 실행 모델 바인딩 | Verifier 역할의 실행 모델 지정은 02 §4 실행 모델 바인딩 영역이다. 06은 참조만 하고 지정하지 않는다. |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부다. §3 Core Contract는 유지된다.

- SP-1: Verifier Module 진입점 파일 위치·포맷(`.claude/agents/verifier.md`) → 대상 환경의 Agent 정의 메커니즘.
- SP-2: 검증 리포트 직렬화·저장 위치 → 대상 환경의 산출물 포맷.
- SP-3: 검사 도구(존재 확인·전수 스캔·시연 실행) → 대상 환경의 검사 도구.
- SP-4: 판정 대상·완료 보고 회수 채널(서브에이전트 최종 응답) → 대상 환경의 결과 반환 채널.
- SP-5: 재작업 지시 전달 채널 → 대상 환경의 재위임·오케스트레이션 메커니즘 (03-loop 정식화).
- SP-6: Verifier 실행 모델 지정 → 02 §4 소관. 06은 참조만 한다.

유지되는 것: §3.2-A 검증 리포트·§3.2-B 판정 값·§3.2-D 재작업 지시의 필수 필드, §3.2-E 검증 유형, §3.2-F 검출 계약, §3.3 Invariants. 이들은 이식 시 바뀌지 않는다.

---

# §5. Memory Access (해당 시)

Verifier는 Memory 소비자다 (ARCHITECTURE.md 5.1의 소비자 목록: Agent, Loop, Workflow, Verifier). Memory에는 Memory Service Interface(단일 Port)를 통해서만 접근한다 (INV-10).

## 읽기 (Recall)

- 목적: 과거 검증 실패 이력과 관련 Lessons를 회수해 재발 여부를 판정에 반영한다 (예: 이전에 검출된 "검사 범위 부족" 유형을 검사 항목에 포함).
- 범위: 회수 정책(Recall Policy)에 따라 최소 범위로. 현재 판정 대상에 관련된 것만 읽는다.
- 시점: 필요할 때만. 판정 착수 시. 매 판정마다 전량을 무조건 로드하지 않는다 (Token Efficiency, ARCHITECTURE.md 3.6).

## 쓰기 (Record)

- 기록 대상: 검증 결과 중 다음 사이클에 필요한 것 (Memory Update 단계).
- Lesson 생성 조건: 검출된 위반·거짓 완료 보고는 Lesson 후보가 된다 (AGENT.md Memory, 02 §3.2-D). Lesson의 생성·회수 상세 계약은 specs/05-lessons.md 소관이다 (§9-OQ-V2). 이 spec은 접근 경로 계약만 정의한다.

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다. Lesson 후보 판정의 상세는 05-lessons와 조율한다 (§9-OQ-V2).

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| 거짓 완료 보고 — `self_check` "충족" 주장 ↔ 산출물 위반 | 산출물 근거 재판정으로 검출(§3.2-F). `final_verdict = Fail` + 재작업 지시. | 예 |
| 자체 점검 검사 범위 부족 — 좁은 대리 지표만 검사(예: 단일 토큰 grep)하여 잔여 위반을 놓침 | VT-4 전수 스캔·INV-4로 검출. 좁은 범위 `self_check`를 그대로 신뢰하지 않는다. (§8 예 1) | 예 |
| 산출물 부재 — `artifacts` 경로가 실재하지 않음 | VT-1 위반. `final_verdict = Fail`. | 예 |
| 근거 없는 판정 — `evidence` 누락 | INV-3 위반. 해당 판정은 무효. 판정 불가로 처리. | 예 |
| 대조 기준 부재 — criteria 미제공 | 판정 불가. Verifier 연산 실패 보고. Advisor에게 기준 요청. | 예 |
| Verifier 역할 침범 — 산출물 수정·구현 | INV-6 위반. 02 §3.2-A 경계로 차단. | 예 |
| 판정 불가를 충족으로 위장 | V6·INV-3 위반. 무효. | 예 |
| 재량 판정 월권 — Verifier가 조건부 항목을 스스로 통과 처리 | 경계 위반. 조건부는 Advisor 최종 판정으로 넘긴다(§3.2-C, 02 §3.2-A). | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

- **검증 리포트 스키마 시연.** 임의의 판정에 대해 `target`·`criteria_basis`·항목별 판정(충족/위반/판정 불가)·`evidence`·`final_verdict` 필드가 모두 존재함을 보인다(§3.2-A/B).
- **거짓 완료 보고 검출 시연 (ROADMAP v0.5 핵심).** 완료 보고가 "AI 의존 0건 충족"이라 주장하나 산출물에 금지 요소가 잔존하는 케이스에서, VT-4 전수 스캔이 위반을 검출하고 `final_verdict = Fail`을 산출함을 보인다(§8 예 1).
- **검증 유형 적용 시연.** VT-1 ~ VT-5 각각이 한 판정 항목에 적용되고, 유형별 판정 방법대로 verdict가 도출됨을 보인다(§3.2-E).
- **최종 판정 결정성 시연.** 동일한 항목별 판정 집합에서 §3.2-C 규칙이 항상 동일한 `final_verdict`를 내고, Pass/Fail/Conditional이 규칙대로 도출됨을 보인다(INV-5).
- **재작업 지시 시연.** Fail 리포트의 `rework`에 위반 항목·기대 상태·재검증 기준이 모두 포함됨을 보인다(§3.2-D).
- **독립성 시연.** `self_check` "충족" 주장과 무관하게 판정이 산출물 근거로만 이루어짐을 보인다(INV-1).
- **경계 시연.** 이 spec이 Verify 단계의 시점·전이를 정의하지 않고 판정 기준·리포트·독립성 계약만 정의함을 보인다(INV-9).
- **Core AI 비의존 시연.** §3 본문 전체를 전수 스캔해 특정 AI·모델명·제품 기능 참조가 0건임을 보인다(INV-8, DoD-3).

## 검증 방법

- Verifier가 임의 리포트의 필수 필드를 §3.2-A/B/D와 대조한다.
- Verifier가 거짓 완료 보고 케이스(§8 예 1)를 재현해 Fail 도출을 확인한다.
- Verifier가 §3.2-C 도출 규칙을 세 가지 항목별 판정 집합(전부 충족 / 위반 포함 / 판정 불가 포함)에 적용해 결정성을 확인한다.
- Verifier가 §3 본문을 전수 스캔해 AI 의존 토큰(특정 AI·모델명·제품 기능명 포함, 단일 토큰 검사에 국한하지 않음)이 0건임을 확인한다 (DoD-3). 이 검증 자체가 이 spec이 경계하는 "검사 범위 부족"을 스스로 피한다.
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 거짓 완료 보고 검출 (검사 범위 부족 유형, ROADMAP v0.5 완료 조건 시연)**

Worker 완료 보고(02 §3.2-C):
- artifacts: 어떤 spec 파일
- self_check: "DoD-3 §3 AI 의존 0건 (충족)"
- failures: 없음
- verify_basis: "단일 토큰 검색으로 특정 AI 이름을 찾음 → 0건"

Verifier 독립 판정(검증 리포트):
- criteria_basis: TEMPLATE DoD-3 — Core Contract(§3)에 AI 의존 요소 0건.
- verification_type: VT-4 경계 검증.
- scope: 대상 §3 본문 전체. 금지 요소 후보 = 특정 AI 이름 + 모델명 + 제품 기능명 (완료 보고의 검사 범위보다 넓다).
- verdict: 위반(Violated) — 단일 토큰 검색이 놓친 모델명이 §3에 잔존.
- evidence: 잔존 위치 인용.
- final_verdict: Fail.
- rework: violated_items = [DoD-3], expected_state = §3에 금지 요소 후보 전부 0건, revalidation_criteria = 전수 스캔 재실행 후 0건, evidence_gap = 없음.

결론: Worker의 `self_check`는 정직했으나 검사 범위가 좁았다(단일 토큰만). Verifier의 V4(검사 범위 정직)·VT-4(전수 스캔)가 그 범위를 넘어 검사해 위반을 검출했다. 이것이 "자체 점검의 검사 범위 부족" 유형이다. 이 프로젝트에서 실제로 Advisor 재검증이 동일 유형을 검출한 바 있다.

**예 2 — 조건부 판정과 Advisor 경계 (Conditional)**

어떤 spec의 검증에서 위반은 없으나, §9 Open Question 1건의 해소 여부가 근거 부족으로 판정 불가(Undetermined)로 남는다.

- items: 모든 규격 항목 충족(Met), Open Question 해소 여부 판정 불가(Undetermined).
- final_verdict: Conditional (위반 없음 + 판정 불가 존재, §3.2-C).
- rework: evidence_gap = "남은 Open Question이 Frozen을 막는지 판단할 근거가 이 산출물만으로는 부족".

Verifier는 이 항목을 스스로 통과 처리하지 않는다. Frozen 저지 여부의 재량 판정은 Advisor 소관이다 (TEMPLATE DoD-7, 02 §3.2-A). Verifier는 Conditional로 판정하고 Advisor 최종 판정에 넘긴다.

**예 3 — 통과 판정 (VT-1 + VT-2 + VT-3)**

- target: 위임 output이 지정한 산출물 1개.
- items: 산출물 존재(VT-1, Met) / 완료 조건 전 항목 대조(VT-2, Met) / TEMPLATE DoD 8항목 대조(VT-3, Met). 각 항목에 evidence와 scope 명시.
- final_verdict: Pass (모든 항목 충족, §3.2-C).
- rework: 없음.

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**타 spec 조율:**

- **OQ-V1 (03-loop 조율 — 경계 명시, 02 §9-OQ-4 응답).**
  02 §9-OQ-4는 "Verify 단계의 자체 점검, Verifier 독립 판정, Advisor 최종 승인의 정확한 시퀀싱"을 03-loop와 06의 소관으로 지목했다. 응답: 세 행위의 **역할 구분**은 확정한다 — 자체 점검은 Worker(02 §3.2-C), 독립 판정은 Verifier(이 spec §3.1), 최종 승인·재량 판정은 Advisor(02 §3.2-A). 세 행위의 **시점·전이·시퀀싱**은 이 spec이 정의하지 않는다 (INV-9, specs/03-loop.md 소관). 06은 판정 기준·검증 리포트·독립성 계약만 소유한다. 03-loop 완성 시 시퀀싱 정합을 확인한다. 03의 내용을 추측·인용하지 않았다.

- **OQ-V2 (05-lessons 조율).**
  검증 결과(위반·거짓 완료 보고)가 Lesson 후보가 되는 상세 규칙(생성 조건·포맷·회수)은 specs/05-lessons.md 소관이다. 06은 "모든 실패는 Lesson 후보"(AGENT.md, 02 §3.2-D)라는 상위 규약만 참조하고, §5에서 접근 경로 계약만 정의했다. 05의 내용을 추측하지 않았다. 05 완성 시 §5 쓰기 계약과 정합을 확인한다.

- **OQ-V3 (07-workflow 조율 — 비차단).**
  Workflow의 병합·검증(ROADMAP v0.7)이 이 Verifier 판정 계약을 소비하는 정확한 표면은 07 완성 시 확인한다. 이 spec은 07을 추측하지 않았다. 이 항목은 Frozen을 막지 않는다.

- **OQ-V4 (01-runtime 정합 — 확인 완료).**
  Verifier는 Runtime의 generic Module로 호스팅된다 (01 §4.1 `framework/verifier/`). 두 실패 구조는 목적이 다르며 충돌하지 않는다 — 01 §3.2-D Failure Report는 Runtime 연산 실패용이고, 이 spec §3.2-A 검증 리포트는 판정 산출물이다. Verifier 자신의 연산 실패(산출물 접근 불가 등)와 판정 대상의 `final_verdict = Fail`을 §3.1에서 명시적으로 구분했다.

**Glossary 승격 후보 (Advisor 판단 대상, Glossary §9-OQ6 흐름):**

- 이 spec은 새 용어를 신설하지 않았다. 핵심 명사는 ROADMAP v0.5 어휘("검증 리포트", "재작업 지시", "거짓 완료 보고")이거나 Glossary 기존 용어(Verifier, Worker 완료 보고, 검증, 판정)이거나 평이한 열거 값(충족/위반/판정 불가, 통과/실패/조건부)이다. 상세 필드의 정본은 이 spec §3.2가 유지한다.
- 승격 후보: 03·05·07이 이 spec을 참조하며 아래 용어를 교차 참조할 경우, Advisor 판단으로 Glossary에 정본화할 수 있다 — 검증 리포트(Verification Report, §3.2-A), 검증 유형(Verification Type, §3.2-E), 재작업 지시(Rework Instruction, §3.2-D), 거짓 완료 보고(False Completion Report, §3.2-F). 확정 전까지 타 spec은 이 spec의 § 포인터로 참조한다(02가 자신의 메시지 포맷을 참조시킨 방식과 동일). 06이 단독으로 Glossary를 수정하지 않았다.

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE.md 3.4(Verify Everything)에 정렬한다 — 검증되지 않은 결과는 완료가 아니다(INV-7).

## 결정 기록 (Advisor — Wave 4 통합)

- OQ-V1: 03 §3.1-A 게이트-단계 매핑과 대조 — 정합 확인 완료.
- OQ-V2: 05 완성 확인 — 검증 실패의 Lesson 후보화는 05 §3.1-A Register Candidate와 정합.
- OQ-V3: 07 완성 확인 — 07 INV-5(검증 후 병합)가 06 판정을 선행 조건으로 소비. 정합.
- Glossary 승격 후보 4건(검증 리포트·검증 유형·재작업 지시·거짓 완료 보고) 승인 — Glossary §3.2-J 반영.
