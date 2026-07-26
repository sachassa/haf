# specs/07-workflow — Workflow Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05 · 2026-07-26 정합(격리 개정 — 슬림화·앵커 90ca19c))
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Workflow는 큰 작업을 병렬로 처리하는 오케스트레이션 규격이다.

Workflow는 세 가지 문제를 해결한다.

- 큰 작업을 한 Agent가 직렬로 처리하면 느리고 컨텍스트가 무너진다. 작업을 그래프로 분해해 병렬화한다.
- 분해가 임의적이면 병렬 작업이 서로의 파일·계약을 침범한다. 소유 경계를 분리해 간섭을 금지한다.
- 계약 없는 분해는 병합 시 충돌한다. 각 하위 작업에 완료 조건과 인터페이스 계약을 강제한다.

## 책임 (1~3문장)

Workflow는 큰 작업을 작업 그래프(Work Graph)로 분해하고, 하위 작업을 여러 Agent에게 병렬 디스패치하며, 완료·검증된 결과를 병합·충돌 처리하는 오케스트레이션 규격이다.

Workflow는 분해·디스패치·병합의 계약만 정의하고, 개별 Agent의 실행과 판정에는 관여하지 않는다.

## Non-Goals

- 개별 Agent의 Lifecycle 7단계 전이 규칙을 정의하지 않는다 — specs/03-loop.md 소관이다.
- 검증 판정 기준(무엇이 통과인가)을 정의하지 않는다 — specs/06-verifier.md 소관이다. Workflow는 "검증을 통과한 결과만 병합한다"는 의무만 정의한다.
- Agent 역할 경계·위임 메시지·보고 메시지의 필드를 재정의하지 않는다 — specs/02-agent.md 소관이다. Workflow는 인용만 한다.
- Memory와 Lessons의 내부 포맷·생성 규칙을 정의하지 않는다 — specs/04-memory.md, specs/05-lessons.md 소관이다.
- 특정 AI·병렬 실행 API·직렬화 포맷을 정의하지 않는다 — Adapter Binding(§4) 소관이다.

---

# §2. Position

- 아키텍처 상 위치: Workflow Layer (Glossary §3.2-A). Core Component "Workflow (Component)" (Glossary §3.2-D)의 규격 문서다.
- Workflow Layer는 Presentation → **Workflow** → Agent → Runtime → Core → Adapter 스택에서 Presentation Layer 아래, Agent Layer 위에 위치한다 (ARCHITECTURE.md 5).
- Workflow는 Agent Layer의 Agent에게 하위 작업을 디스패치한다. Agent를 오케스트레이션하되, Agent 내부 계약은 침범하지 않는다.

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 5 스택, 5.1 Memory Service, 3.4 Verify Everything.
- specs/00-glossary.md (실재, Frozen) — 모든 용어의 정본.
- specs/TEMPLATE.md (실재, Frozen) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약. 위임·검증·Memory 원칙.
- specs/02-agent.md (실재, Frozen) — 역할 경계(§3.2-A)와 위임 메시지(§3.2-B)·완료 보고(§3.2-C)·실패 보고(§3.2-D)의 소유 spec. Workflow는 이 계약을 인용한다.
- ROADMAP.md v0.7 (실재) — Workflow & Parallel Orchestration 완료 조건과 산출물.

(상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·02·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`. 종전 "Review"·"Adopted" 표기는 작성 시점 기록이었다.)

## 이 spec에 의존하는 spec (dependents)

- 현재 이 spec에 의존한다고 선언한 spec은 없다. 의존 방향은 항상 07 → 02(위임·역할 계약)이다.
- Workflow Layer는 스택상 Presentation Layer 아래에 위치하므로(§2), 향후 Presentation 진입점이 Workflow를 소비할 수 있으나 그 정식화는 이 wave의 조율 범위 밖이다.

## 순환 의존

없다. Workflow의 Core Contract(§3)는 02-agent의 위임·역할 계약을 인용하는 방향(07 → 02)이다. specs/02-agent.md §2는 07을 자신의 dependent로 명시하며, 02는 07에 의존하지 않는다. 순환은 성립하지 않는다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 AI·환경 의존 실현은 §4에 둔다.

Workflow는 세 가지 연산과 그 데이터 포맷을 정의한다.

- 분해 (Decompose) — 큰 작업을 Work Graph로 (§3.1-A, §3.2-A/B)
- 디스패치 (Dispatch) — 병렬 집합을 여러 Agent에게 (§3.1-B, §3.2-C)
- 병합 (Merge) — 완료·검증된 결과의 수합·정합성·충돌 처리 (§3.1-C, §3.2-D)

Workflow는 위임 메시지·역할 경계 포맷을 소유하지 않는다. 그 소유는 specs/02-agent.md이며 Workflow는 인용한다.

---

## 3.1 Interface

Workflow는 다음 연산을 노출한다. 모든 연산의 실패는 공통 Failure Report(§3.2-E) 구조로 보고한다.

### A. Decompose (분해)

- 입력: 큰 작업 1건 — 목표와 범위.
- 출력: Work Graph(§3.2-A) 1건.
- 완료 조건: (1) 모든 Task(§3.2-B)가 완료 조건과 인터페이스 계약을 가진다 (INV-1). (2) 각 병렬 집합 내 Task들의 소유 경계가 서로 겹치지 않는다 (INV-2). (3) 의존 관계에 순환이 없다.
- 실패 보고: reason = `MissingCompletionCriteria` | `MissingInterfaceContract` | `OwnershipOverlap` | `DependencyCycle`.

### B. Dispatch (디스패치)

- 입력: 하나의 병렬 집합(§3.2-A) + 그 집합에 속한 각 Task의 위임 메시지(specs/02-agent.md §3.2-B).
- 출력: 디스패치된 Task 핸들 집합 — Task id → 수임 Agent 매핑.
- 완료 조건: 병렬 집합의 각 Task가, 선행 의존이 모두 완료된 상태에서, 02 §3.2-B 필수 필드를 모두 갖춘 위임 메시지로 서로 다른 Agent에게 전달된다.
- 실패 보고: reason = `IncompleteDelegation` | `UnmetDependency`.

### C. Merge (병합)

- 입력: 완료·검증된 Task 결과 집합 — 각 결과는 완료 보고(02 §3.2-C)를 동반한다.
- 출력: 병합 결과 + 상호 참조 정합성 판정 + (있다면) 충돌 목록.
- 완료 조건: (1) 모든 Task 결과가 개별 검증을 통과했다 (INV-5). (2) Task 간 상호 참조가 정합하다. (3) 충돌이 0건이거나, 발견된 충돌이 Advisor 중재로 해소되었다 (INV-6).
- 실패 보고: reason = `UnverifiedResult` | `CrossReferenceMismatch` | `UnresolvedConflict`.

주의: "개별 검증을 통과했다"의 판정 기준은 specs/06-verifier.md 소관이다. Workflow는 검증 통과 여부를 병합의 선행 조건으로 요구할 뿐, 판정 자체를 정의하지 않는다 (Non-Goals, §9 조율).

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)은 Adapter Binding(§4)이 정한다.

### A. Work Graph (작업 그래프)

Workflow의 정의 포맷이다. 큰 작업의 분해 결과를 담는다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `goal` | 워크플로 전체의 목표와 범위. | 예 |
| `tasks` | Task(§3.2-B) 목록. 분해된 하위 작업 전부. | 예 |
| `dependencies` | Task 간 의존 관계 — 선행 Task id → 후행 Task id. 순환이 없어야 한다. | 아니오(없으면 전부 독립) |
| `parallelSets` | 병렬 집합 목록. 각 집합은 동시에 디스패치 가능한 Task id 그룹이다. 같은 집합의 Task는 서로 의존하지 않고 소유 경계가 겹치지 않는다. | 예 |
| `completion` | 워크플로 전체의 완료 조건 — 모든 Task가 완료·검증되고 병합이 성립하는 조건. | 예 |

병렬 집합은 의존 관계에서 도출된다. 선행 의존이 없는 Task들, 또는 공통 선행이 모두 완료된 Task들이 하나의 병렬 집합을 이룬다.

### B. Task (하위 작업)

분해의 최소 단위다. 각 Task는 다음을 반드시 가진다 (없으면 디스패치되지 않는다 — INV-1).

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Task 고유 식별자. 의존·병렬 집합·핸들이 이 id로 참조한다. | 예 |
| `task` | 작업 요약. | 예 |
| `done` | 완료 조건 — 검증 가능한 형태 (ROADMAP v0.7 완료 조건). | 예 |
| `interfaceContract` | 인터페이스 계약 — 이 Task가 제공(produces)하고 소비(consumes)하는 확정된 계약. 다른 Task는 이 계약만 참조할 수 있다. | 예 |
| `ownedBoundary` | 소유 경계 — 이 Task가 배타적으로 소유하는 파일·계약 집합. 같은 병렬 집합의 다른 Task와 겹치지 않는다 (INV-2). | 예 |
| `dependsOn` | 선행 Task id 목록. 모두 완료·검증되어야 디스패치된다. | 아니오(기본 없음) |
| `delegation` | 이 Task를 디스패치할 때 사용하는 위임 메시지(02 §3.2-B) 매핑. | 예 |

`done`과 `interfaceContract`는 ROADMAP v0.7의 "작업 분해 결과에 완료 조건과 인터페이스 계약이 포함된다" 완료 조건을 충족한다.

### C. Parallel Dispatch Protocol (병렬 디스패치 프로토콜)

하나의 병렬 집합을 여러 Agent에게 동시에 위임하는 규칙이다.

- **R1 (위임 메시지 전용).** 각 Task는 서로 다른 Agent에게 02 §3.2-B 위임 메시지로만 디스패치된다. Workflow는 위임 메시지 포맷을 재정의하지 않는다 (INV-3).
- **R2 (미완성 산출물 불추측).** 병렬 Task는 동시 진행 중인 다른 Task의 미완성 산출물을 추측하거나 인용하지 않는다. 오직 확정된 `interfaceContract`(§3.2-B)만 참조한다 (INV-4).
- **R3 (조율 에스컬레이션).** Task 진행 중 다른 Task와의 조율이 필요한 사항(계약 불명확, 경계 충돌 조짐, 의존 계약 미확정)을 발견하면, 추측하지 않고 Advisor에게 에스컬레이션한다 (AGENT.md 추측 금지, 02 O4·INV-6).
- **R4 (경계 준수).** 각 Task는 자신의 `ownedBoundary` 밖의 파일·계약을 수정하지 않는다 (INV-2).

이 프로토콜은 이 프로젝트의 spec 병렬 작성 Wave가 실증한다 — 병렬 작성 중인 spec은 00/01/02(확정)만 인용하고, 동시 작성 중인 03~13은 추측하지 않으며, 조율 필요 사항을 §9로 에스컬레이션한다 (§8 예1).

### D. Merge Result (병합 결과)

병렬 결과의 수합·정합성 검증·충돌 처리 결과를 담는다.

| 필드 | 의미 |
|---|---|
| `collected` | 수합된 Task 결과 집합. 각 항목은 개별 검증을 통과한 결과만 포함한다 (INV-5). |
| `crossRefStatus` | 상호 참조 정합성 판정 — `Consistent` / `Mismatch`. 한 Task가 참조하는 다른 Task의 계약·산출물이 실제와 일치하는지. |
| `conflicts` | 충돌 목록. 두 Task가 같은 계약을 다르게 실현했거나 소유 경계가 사후 충돌한 경우. 각 항목은 중재 대상이다. |
| `arbitration` | 충돌 해소 결과. 중재자는 Advisor다 (INV-6). Workflow는 충돌을 검출·보고하고, 해소 결정은 Advisor가 내린다. |

충돌 처리 순서: 수합 → 상호 참조 정합성 검증 → 충돌 검출 → (충돌 시) Advisor 중재 → 병합 성립.

### E. Failure Report (공통 실패 보고)

모든 Workflow 연산의 공통 실패 보고 구조다.

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Decompose / Dispatch / Merge). |
| `target` | 대상 (Work Graph, Task id, 병렬 집합, 충돌 항목). |
| `reason` | 사유 코드 (MissingCompletionCriteria / MissingInterfaceContract / OwnershipOverlap / DependencyCycle / IncompleteDelegation / UnmetDependency / UnverifiedResult / CrossReferenceMismatch / UnresolvedConflict). |
| `location` | 실패 지점 참조 (Task id, 경계 항목, 참조 위치). |

---

## 3.3 Invariants

- **INV-1 (계약 강제).** 모든 Task는 완료 조건(`done`)과 인터페이스 계약(`interfaceContract`)을 가진다. 둘 중 하나라도 없으면 디스패치되지 않는다 (ROADMAP v0.7 완료 조건).
- **INV-2 (간섭 금지).** 같은 병렬 집합 내 Task들의 소유 경계(`ownedBoundary`)는 서로 겹치지 않는다. 각 Task는 자신의 소유 경계 밖 파일·계약을 수정하지 않는다.
- **INV-3 (위임 계약 불침범).** 디스패치는 02 §3.2-B 위임 메시지로만 이루어진다. Workflow는 위임 메시지·역할 경계 포맷을 재정의하지 않고 인용한다 (02 소유).
- **INV-4 (불추측 조율).** 병렬 Task는 서로의 미완성 산출물을 추측·인용하지 않는다. 확정된 인터페이스 계약만 참조하고, 조율 필요 사항은 Advisor에게 에스컬레이션한다.
- **INV-5 (검증 후 병합).** 각 Task 결과는 개별 검증을 통과한 뒤에만 병합 대상이 된다. 검증 판정 기준은 이 spec이 정의하지 않는다 (06-verifier 소관). 검증되지 않은 결과의 병합은 완료가 아니다 (ARCHITECTURE.md 3.4).
- **INV-6 (중재자 = Advisor).** 충돌의 중재자는 Advisor다. Workflow는 충돌을 검출·보고하고, 해소 결정은 Advisor가 내린다. 설계·역할 충돌의 결정 권한은 Advisor에게 있다 (02 §3.2-A 역할 경계).
- **INV-7 (Memory 단일 Port).** Workflow는 Memory에 Memory Service Interface(단일 Port)를 통해서만 접근한다 (ARCHITECTURE.md 5.1).
- **INV-8 (경계 불가침).** Workflow는 Agent Lifecycle 7단계 전이(03-loop 소관)와 검증 판정 기준(06-verifier 소관)을 정의하지 않는다. 분해·디스패치·병합의 오케스트레이션 계약만 정의한다.
- **INV-9 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 실행 모델·병렬 실행 메커니즘은 §4에 위치한다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다. 이 프로젝트 자체의 Wave 병렬 위임 구조가 Workflow의 실사용 형태다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Work Graph(§3.2-A) 직렬화 | 계획·로드맵 문서. 예: ROADMAP.md의 Wave 분해와 Parallel Track Map(§4). |
| Task(§3.2-B) 정의 | 로드맵 Wave 내 개별 작업 항목(예: 각 spec 작성). `done`·`interfaceContract`는 TEMPLATE DoD와 각 spec §2 Position 선언에 대응. |
| 병렬 디스패치(§3.2-C) | Advisor가 서브에이전트 동시 위임으로 한 병렬 집합의 Task들을 여러 Worker에게 동시에 전달한다. 위임 메시지 전달 메커니즘은 02 §4.1을 재사용한다. |
| 위임 메시지 전달 | 02 §4.1 위임 메커니즘(서브에이전트 위임) 재사용. Workflow는 채널을 새로 정의하지 않는다. |
| 결과 회수(§3.2-D collected) | 각 서브에이전트의 최종 응답 = 완료 보고(02 §3.2-C). 02 §4.1 보고 회수 재사용. |
| 상호 참조 정합성·충돌 중재 | Advisor(`.claude/CLAUDE.md` 진입점)가 병렬 결과를 수합·대조하고 충돌을 중재한다. |
| 검증 통합 | 각 Task 결과는 개별 검증(Verifier 판정)을 거친 뒤 병합된다. 판정 표면은 06-verifier §4 소관. |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부. Core Contract(§3)는 유지되고 아래만 교체된다.

1. **Work Graph 직렬화** — 계획·로드맵 문서 포맷 → 대상 환경의 작업 그래프 서술자.
2. **병렬 디스패치 메커니즘** — 서브에이전트 동시 위임 → 대상 환경의 병렬 오케스트레이션 API.
3. **위임/보고 채널** — 서브에이전트 위임·최종 응답 → 대상 환경의 Agent 호출·결과 반환 채널 (02 §4.2 SP-4/SP-5 재사용, 이 spec은 참조만).
4. **중재 진입점** — Advisor 바인딩(`.claude/CLAUDE.md`) → 대상 환경의 오케스트레이터 진입점.

유지되는 것: §3.2-A Work Graph 필드, §3.2-B Task 필수 필드, §3.2-C 병렬 디스패치 프로토콜 규칙(R1~R4), §3.3 Invariants. 이들은 이식 시 바뀌지 않는다.

---

# §5. Memory Access (해당 시)

Workflow는 Memory 소비자다 (ARCHITECTURE.md 5.1 — Memory 소비자 목록에 Workflow 포함). Memory에는 Memory Service Interface(단일 Port)를 통해서만 접근한다 (INV-7).

## 읽기 (Recall)

- 목적: 착수 전, 유사 작업의 분해 패턴과 과거 충돌·간섭 Lessons를 회수해 분해 품질을 높인다.
- 범위: 회수 정책(Recall Policy, Glossary §3.2-C)에 따라 최소 범위로. 현재 워크플로에 필요한 것만 읽는다.
- 시점: 필요할 때만. 매 분해마다 전량을 무조건 로드하지 않는다 (Token Efficiency, ARCHITECTURE.md 3.6).

## 쓰기 (Record)

- 기록 대상: 분해 결정, 작업 이력(어떤 Task를 어떻게 병렬화·병합했는가), 충돌 해소 결과 중 다음 사이클에 필요한 것.
- Lesson 생성 조건: 병렬 작업 간 간섭·상호 참조 불일치·병합 충돌은 Lesson 후보가 된다 (AGENT.md — 모든 실패는 Lesson 후보). 성공한 분해 패턴은 Best Practice 후보가 된다.

접근 경로만 이 spec이 정의한다. Memory와 Lessons의 상세 포맷·생성 규칙은 specs/04-memory.md, specs/05-lessons.md 소관이다.

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다.

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| Task에 완료 조건 또는 인터페이스 계약 누락 | Decompose 실패. reason=MissingCompletionCriteria \| MissingInterfaceContract. 디스패치 차단 (INV-1). | 예 |
| 병렬 집합 내 소유 경계 중첩 (간섭 위험) | Decompose 실패. reason=OwnershipOverlap. 재분해로 경계 분리 (INV-2). | 예 |
| 의존 관계 순환 | Decompose 실패. reason=DependencyCycle. | 예 |
| 미완성 산출물 추측·인용 | INV-4 위반. R3 에스컬레이션으로 교정. 추측 결과는 무효. | 예 |
| 선행 의존 미완료 Task 조기 디스패치 | Dispatch 실패. reason=UnmetDependency. | 예 |
| 위임 메시지 필수 필드 누락 | Dispatch 실패. reason=IncompleteDelegation. 수임 Agent가 착수 전 반환·질의 (02 INV-6). | 예 |
| 미검증 결과를 병합 | Merge 실패. reason=UnverifiedResult. INV-5로 차단. | 예 |
| 상호 참조 불일치 | Merge 실패. reason=CrossReferenceMismatch. Advisor 중재로 넘김. | 예 |
| 충돌 미해소 (두 Task가 같은 계약을 다르게 실현) | Merge 실패. reason=UnresolvedConflict. Advisor가 중재한다 (INV-6). | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.7 완료 조건과 정렬한다.

- **병렬 시연.** 3개 이상의 Task가 하나의 병렬 집합으로 디스패치되고, 각 Task가 개별 검증을 통과한 뒤 병합이 성립하는 Workflow를 시연한다 (ROADMAP v0.7 "3개 이상의 작업이 병렬로 수행되고 각각 검증까지 완료").
- **계약 시연.** Work Graph의 각 Task가 완료 조건(`done`)과 인터페이스 계약(`interfaceContract`)을 가짐을 대조로 보인다 (ROADMAP v0.7 "작업 분해 결과에 완료 조건과 인터페이스 계약이 포함된다", INV-1).
- **간섭 금지 시연.** 한 병렬 집합 내 모든 Task의 소유 경계 교집합이 0임을 보인다 (INV-2).
- **충돌 처리 시연.** 병합 시 상호 참조 정합성 검증이 수행되고, 충돌 발견 시 Advisor 중재로 넘어가 해소됨을 시연한다 (ROADMAP v0.7 "병합 시 충돌 처리 규칙이 동작한다", INV-6).
- **경계 시연.** Workflow가 Agent Lifecycle 단계 전이(03)와 검증 판정 기준(06)을 정의하지 않고 오케스트레이션 계약만 노출함을 보인다 (INV-8).
- **AI 비의존 시연.** §3 본문에 특정 AI 모델명·제품 기능 참조가 0건임을 보인다 (INV-9).

## 검증 방법

- Verifier가 Work Graph의 각 Task 필수 필드(`done`, `interfaceContract`, `ownedBoundary`)의 존재를 §3.2-B와 대조한다.
- Verifier가 병렬 집합 내 소유 경계의 쌍별 교집합이 0임을 확인한다.
- Verifier가 각 Task 결과가 개별 검증을 통과했는지 확인한 뒤에만 병합이 성립했음을 확인한다 (INV-5).
- Advisor가 충돌 중재 및 최종 승인을 수행한다 (INV-6).
- Verifier가 §3 본문을 스캔해 AI 의존 토큰(모델명·제품 기능명)이 0건임을 확인한다 (DoD-3).

---

# §8. Examples

**예 1 — 이 프로젝트의 spec 병렬 작성 Wave (실증 사례)**

큰 작업: v0.1 Specification Baseline — 13개 spec 확정.

- **분해 (Decompose):** 00/01/02는 나머지가 참조하는 공통 기반이므로 선행(직렬) Task로, 03~13은 병렬 Task로 분해한다 (ROADMAP v0.1 병렬 작업 단계).
- **Work Graph:** `tasks` = 각 spec 1개, `dependencies` = 03~13 → {00,01,02}, `parallelSets` = {03-loop, 04-memory, 05-lessons, 06-verifier, **07-workflow**, 08~13}.
- **Task 계약:** 각 Task의 `done` = TEMPLATE DoD 8항목, `interfaceContract` = 각 spec §2 Position의 의존/피의존 선언, `ownedBoundary` = 자기 spec 파일 하나.
- **병렬 디스패치 (§3.2-C):** Advisor가 각 spec Task를 서로 다른 Worker에게 02 §3.2-B 위임 메시지로 동시 위임한다. 각 Worker는 확정된 00/01/02만 인용하고(R2), 동시 작성 중인 03~13은 추측하지 않으며(R2), 조율 필요 사항을 §9로 에스컬레이션한다(R3). 각 Worker는 자기 파일만 수정한다(R4).
- **병합 (Merge):** Advisor가 완료·검증된 spec들을 수합하고, §2 상호 참조 정합성을 검증하며, 충돌을 중재한다 (INV-6).
- **검증 통합:** 각 spec은 개별 DoD 검증(Verifier 판정)을 거친 뒤 병합된다 (INV-5).

이 Workflow의 산출물 하나가 본 spec(07-workflow.md) 자신이며, 본 spec은 03~13을 추측하지 않고 §9에 조율 항목으로 남긴다.

**예 2 — 3-Task 병렬 워크플로 (최소 시연)**

큰 작업: "API 계층 추가". 분해 → 3개 Task, 모두 한 병렬 집합.

| Task | `done` | `interfaceContract` | `ownedBoundary` |
|---|---|---|---|
| T1 스키마 | 스키마 검증 통과 | produces: DataSchema | schema 파일 |
| T2 핸들러 | 핸들러 테스트 통과 | consumes: DataSchema / produces: HandlerAPI | handler 파일 |
| T3 문서 | 문서 대조 통과 | consumes: HandlerAPI | docs 파일 |

- 소유 경계 교집합 = 0 → 간섭 없음 (INV-2). 세 Task를 병렬 디스패치.
- 각 Task는 상대의 **확정된** 계약(DataSchema, HandlerAPI)만 참조하고 미완성 산출물은 추측하지 않는다 (R2). T2가 DataSchema를 불명확하다고 판단하면 추측 없이 Advisor에게 에스컬레이션한다 (R3).
- 3개 결과가 각각 개별 검증 통과 → 병합. Merge가 상호 참조(T2→T1, T3→T2) 정합성을 검증한다. 충돌 시 Advisor 중재 (INV-6).

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**Glossary 추가 요청** — 용어 5종(Work Graph 작업 그래프 · Task 하위 작업 · 병렬 집합 Parallel Set · 소유 경계 Ownership Boundary · 인터페이스 계약 Interface Contract)은 00-glossary §3.2-J-07 정본 등재 완료(요청 5건 전부 Advisor 승인). 상세 필드의 정본은 이 spec §3.2-A/B가 유지한다.

**타 spec 조율:**

- **03-loop 조율** — 해소(Decompose·Dispatch·Merge는 다중 사이클 오케스트레이션으로 03의 단일 사이클 밖에 위치한다(03 §9 동일 기록). 이 spec은 오케스트레이션 계약만 정의하고 단계 전이는 침범하지 않았다(INV-8) · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- **06-verifier 조율** — 해소(INV-5의 "개별 검증을 통과했다"의 판정 기준은 06 §3.2-C 최종 판정을 사용한다. 이 spec은 "검증 통과 결과만 병합한다"는 의무만 정의 · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- **04-memory 조율** — 해소(§5의 분해 결정·작업 이력·충돌 해소 결과 기록은 04 Port 계약을 준수한다. 이 spec은 Memory Service Interface(단일 Port) 경유의 접근 경로만 정의 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

**경계 인용 확인 (02-agent — 인용 가능, 재정의 안 함):**

- 위임 메시지(§3.2-C R1, INV-3)·역할 경계(INV-6 Advisor 중재자)·완료 보고(§3.1-C 입력)는 모두 specs/02-agent.md §3.2가 소유한다. 이 spec은 인용만 하고 필드를 재정의하지 않았다. 02 §2는 07을 자신의 dependent로 이미 명시한다.

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 5(Workflow Layer 위치)·5.1(Memory 단일 Port)·3.4(Verify Everything)와 Glossary §3.2-D 정의에 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

- Glossary 추가 요청 5건 승인 — Glossary §3.2-J 반영.
- 03/06/04 조율: 각 spec 완성 후 대조 — Decompose·Dispatch·Merge는 다중 사이클 오케스트레이션으로 03의 단일 사이클 밖에 위치(03 §9 동일 기록), INV-5의 판정 기준은 06 §3.2-C 최종 판정 사용, §5 기록은 04 Port 계약 준수. 모순 없음.

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 항목(03·06·04 조율)의 원문+답 이중 잔존 1줄화, Glossary 추가 요청 블록의 등재 완료 1줄화, §2 stale 상태 표기(Review/Adopted → Frozen) 현행 정정. 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — §3 전체·§6·§7·§8 규범-예시(병렬 Wave 실증·3-Task 시연) 무촉, dependents(§2 = 선언된 dependent 0) 참조 영향 0(정책 §4-a·§4-c). §3·§8의 "동시 작성 중" 서술은 당시 Wave의 사실 기록이므로 보존한다(`uaf-allow-legacy: §8 예1은 v0.1 병렬 작성 Wave의 실증 이력 인용 — 시점 기록 보존`). 종전 문면 = git 앵커 90ca19c.
