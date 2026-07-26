# specs/04-memory — Memory Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05 · 2026-07-26 정합(격리 개정 — 슬림화·앵커 90ca19c))
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Memory는 UAHF의 기억 능력이다.

Memory는 기록(Record)과 회수(Recall)를 하나의 계약으로 통일한다.

Memory는 세 가지 문제를 해결한다.

- 기억이 여러 경로로 흩어져 접근이 제각각인 문제. 접근을 단일 Port(Memory Service Interface) 하나로 통일한다.
- Context가 무너지는 문제. 회수 정책(Recall Policy)을 계약에 내장해 전량 로드를 금지하고 최소 범위만 읽게 한다.
- 특화 기록(Lessons, Best Practice)이 각자 저장·회수를 재발명하는 문제. 일반 기록·회수 계약을 제공해 특화 계약이 그 위에 올라타게 한다.

## 책임 (1~3문장)

이 spec은 Memory Service Interface(단일 Port)의 정본 정의 문서다.

Memory Item의 추상 스키마, Record·Recall 연산, 회수 정책, Memory Index 계약, 소비자 계약을 AI 비의존 형태로 확정한다.

## Non-Goals

- Memory는 Layer가 아니다. Layer 규격을 정의하지 않는다 (ARCHITECTURE 5.1, Glossary §3.2-B/C).
- Lessons·Best Practice의 상세 포맷과 생성 규칙을 정의하지 않는다 — specs/05-lessons.md 소관이다. Memory는 특화 계약이 올라탈 일반 계약만 정의한다.
- Memory Update 단계가 언제 실행되는가(Lifecycle 단계 전이)를 정의하지 않는다 — specs/03-loop.md 소관이다.
- 특정 AI·직렬화 포맷·영속성 백엔드를 정의하지 않는다 — Adapter Binding(§4) 소관이다.

---

# §2. Position

- 아키텍처 상 위치: **Cross-cutting Service (Memory Service)**. Layer가 아니다 (ARCHITECTURE 5.1, Glossary §3.2-B/C). Core Component "Memory" (Glossary §3.2-D)의 규격 문서다.
- Memory Service는 스택의 특정 위치에 고정되지 않고 모든 Layer를 관통한다. 접근 경로는 Memory Service Interface(단일 Port) 하나뿐이다. 영속성 백엔드는 이 Port 뒤 Adapter Layer에 위치한다.

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 5.1 Memory Service, 3.6 Token Efficiency, 6 Core Components.
- specs/00-glossary.md (실재, Frozen) — 모든 용어의 정본. 특히 §3.2-B(판정 기준), §3.2-C(Memory Service 용어).
- specs/TEMPLATE.md (실재, Frozen) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약. Memory 원칙("모든 실패는 Lesson 후보", "모든 성공은 Best Practice 후보").
- ROADMAP.md v0.4 (실재) — Memory & Lessons 산출물과 완료 조건.
- specs/01-runtime.md (실재, Frozen) — §4 Adapter Binding에서만 의존. Memory Service Provider가 Runtime의 Module로 등록되는 메커니즘(01 §3.1-A Register, §3.2-A Module Manifest). contract id는 01 §8 예1의 `MemoryServiceInterface`와 정합한다.

## 이 spec에 의존하는 spec (dependents)

- specs/02-agent.md (실재, Frozen) — Agent는 소비자다. 02 §5·INV-8이 "Agent는 Memory Service Interface(단일 Port)를 통해서만 접근"을 이미 선언하고, 상세 포맷을 이 spec에 위임한다. 방향은 02 → 04다.
- specs/03-loop.md — Loop는 소비자다. Memory Update·Consult 단계에서 Record·Recall을 호출한다. 단계 전이 시점은 03 소관이다 (§9 조율).
- specs/05-lessons.md — Lessons·Best Practice는 소비자가 아니라 Memory Item의 kind로 이 Port 위에 올라타는 특화 계약이다 (§9 조율).
- specs/06-verifier.md — Verifier는 소비자다 (§9 조율).
- specs/07-workflow.md — Workflow는 소비자다 (§9 조율).

(위 상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·01·02·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`. 종전 "Review"·"Adopted" 표기는 작성 시점 기록이었다.)

## 순환 의존

없다. 이 spec의 Core Contract(§3)는 소비자(02/03/05/06/07) 중 어느 것에도 의존하지 않는다. 의존은 항상 소비자 → 04 방향이다. 04는 §4 Adapter Binding에서만 01-runtime에 의존하며, 01의 Core Contract(§3)는 04에 의존하지 않는다. 02에 대한 참조(§3.4)는 소비자 관계를 서술하는 back-reference일 뿐 Core Contract 의존이 아니다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경·직렬화·영속성 백엔드 의존 내용이 한 줄도 들어가지 않는다. 모든 환경 의존 실현은 §4에 둔다.

Memory Service는 정확히 하나의 Port(Memory Service Interface)를 노출한다. 이 Port는 두 연산과 하나의 회수 정책, 하나의 인덱스 계약으로 구성된다.

- Record 연산 (§3.1-A) — 쓰기.
- Recall 연산 (§3.1-B) — 읽기.
- 회수 정책 (§3.1-C) — 계약에 내장된 읽기 규칙.
- Memory Item·Memory Index 데이터 계약 (§3.2).
- 소비자 계약 (§3.4).

---

## 3.1 Interface

모든 연산의 실패는 공통 Failure Report(§3.2-D) 구조로 보고한다.

### A. Record (쓰기)

- 입력: Memory Item(§3.2-A) 1건. `id`를 제외한 필수 필드(kind, content, source, timestamp)를 모두 포함한다.
- 출력: 기록 결과 — 할당된 Memory Item `id`.
- 완료 조건: Memory Item이 §3.2-A 스키마를 만족하고, `id`가 Memory Store에서 유일하게 할당되며, 대응하는 Index Entry(§3.2-C)가 Memory Index에 생성된다.
- 실패 보고: reason = `SchemaViolation` | `DuplicateId` | `IndexInconsistent`.

Record는 Memory Item을 추가(append)한다. 이미 기록된 Memory Item은 불변이다 (INV-6). 갱신은 새 Memory Item 기록으로 표현한다.

### B. Recall (읽기)

- 입력: Recall Request(§3.2-B). `purpose`와 `scope`는 필수다.
- 출력: Recall Result(§3.2-B) — scope로 한정된 Index Entry 집합(`detail = index`) 또는 Memory Item 집합(`detail = full`)과 절단(truncated) 표시.
- 완료 조건: `purpose`와 `scope`가 모두 존재하고, `scope`가 bounded이며(§3.1-C), `scope`가 Memory Index로 해소되고, 반환량이 scope의 `limit`과 시스템 상한을 넘지 않는다.
- 실패 보고: reason = `MissingPurpose` | `MissingScope` | `UnboundedScope` | `ScopeUnresolvable`.

Recall은 어떤 경우에도 Memory Store 전량을 반환하지 않는다 (INV-3).

### C. 회수 정책 (Recall Policy) — 계약 내장

회수 정책은 Token Efficiency 원칙(ARCHITECTURE 3.6)의 계약 구현이다. Glossary §3.2-C의 "필요할 때만, 목적을 명시하고, 최소 범위로 읽는다"를 인터페이스가 강제한다.

| 정책 문구 | 계약 강제 지점 |
|---|---|
| 필요할 때만 | `purpose` 필수 — 목적이 없으면 Recall이 성립하지 않는다. 무목적·상시 회수는 유효한 purpose를 가질 수 없다. 회수 "시점"의 판단은 소비자와 Loop(03)에 있으나, Port는 목적 없는 회수를 거부한다. |
| 목적을 명시하고 | `purpose` 필수 — 모든 Recall은 회수 이유를 명시한다. |
| 최소 범위로 | `scope` 필수 + bounded 강제 — 전체 store를 겨냥하는 scope(narrowing 차원도 finite limit도 없는 scope)는 `UnboundedScope`로 거부된다. 기본 회수 세분도(`detail`)는 `index`로, content 원문 없이 후보만 반환한다. content는 명시적으로 `detail = full`을 요청하고 scope로 한정된 경우에만 materialize된다. |

전량 로드는 금지된다. 회수 정책은 §3.3 INV-2 / INV-3 / INV-4로 불변화된다.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)과 물리 저장은 Adapter Binding(§4)이 정한다.

### A. Memory Item

기억의 최소 기록 단위다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Memory Item 고유 식별자. 안정적(stable)이며 회수·참조의 기준이 된다. Record 시 유일하게 할당된다. | 예(Record가 할당) |
| `kind` | 기억의 종류(분류자). 특화 계약이 자신의 kind 값을 정의한다. Memory는 `kind`를 불투명(opaque) 분류자로만 취급한다 (INV-5). | 예 |
| `content` | 기억 내용(payload). `kind`별 상세 스키마는 특화 계약 소관이다. Memory는 `content`를 불투명 페이로드로 다룬다 (INV-5). | 예 |
| `source` | 출처. 이 기억을 생성한 주체·작업·사이클 참조. | 예 |
| `timestamp` | 기록 시점. | 예 |
| `labels` | 회수 범위 해소용 태그 집합. Memory Index가 scope 해소에 사용한다. | 아니오 |

`kind`와 `content`의 내부 의미는 Memory가 해석하지 않는다. Lessons·Best Practice 등 특화 계약이 kind 값과 content 스키마를 소유한다 (§9 조율, specs/05-lessons.md).

### B. Recall Request / Recall Result

**Recall Request**

| 필드 | 의미 | 필수 |
|---|---|---|
| `purpose` | 회수 목적. 이 회수가 왜 필요한가. | 예 |
| `scope` | 회수 범위 지정자. 반환 대상을 한정한다. narrowing 차원(`kind` / `labels` / `timeRange` / `source`) 중 최소 하나 또는 finite `limit`을 가져야 한다. 전체 store를 겨냥하는 scope는 거부된다. | 예 |
| `detail` | 반환 세분도. `index`(Index Entry만) 또는 `full`(Memory Item). 기본값 `index`. | 아니오(기본 `index`) |
| `limit` | 최대 반환 개수. 미지정 시 시스템 상한을 적용한다. | 아니오 |

**Recall Result**

| 필드 | 의미 |
|---|---|
| `entries` | scope에 부합하는 Index Entry(§3.2-C) 또는 Memory Item(§3.2-A)의 정렬된 집합. `detail`에 따라 결정된다. |
| `truncated` | 결과가 `limit` 또는 시스템 상한으로 절단되었는지 여부. |

### C. Memory Index / Index Entry

**Memory Index**

회수 대상을 최소 Context로 찾기 위한 조회 구조다. scope 지정자(`kind` / `labels` / `timeRange` / `source`)를 Index Entry 집합으로 해소한다. Memory Store 전체를 스캔·로드하지 않고 후보를 찾게 하는 것이 목적이다.

**Index Entry** — 경량 서술자

| 필드 | 의미 |
|---|---|
| `id` | 대응 Memory Item의 `id`. |
| `kind` | 분류자. scope의 `kind` 차원 해소. |
| `source` | 출처. |
| `timestamp` | 시점. scope의 `timeRange` 차원 해소. |
| `labels` | 범위 태그. scope의 `labels` 차원 해소. |
| `digest` | 짧은 서술(선택). Record 시 caller가 제공한다. `content` 원문을 담지 않는다. |

Index Entry는 `content` 원문을 담지 않는다 (INV-4). 모든 Memory Item은 대응하는 Index Entry를 가진다 (INV-7). Record가 Memory Item 기록과 Index Entry 생성을 함께 완료한다 (§3.1-A 완료 조건).

### D. Failure Report

모든 Memory Service 연산의 공통 실패 보고 구조다.

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Record / Recall). |
| `reason` | 사유 코드 (SchemaViolation / DuplicateId / IndexInconsistent / MissingPurpose / MissingScope / UnboundedScope / ScopeUnresolvable / PortBypass). |
| `target` | 대상 (Memory Item `id`, scope 지정자, label, kind). |
| `location` | 실패 지점 참조. |

### E. 저장 구조 규격 (계약 수준)

물리 형식과 경로는 §4가 정한다. 여기서는 AI 비의존 규칙만 정의한다.

- Memory Store는 Memory Item의 저장 구조다. Record가 쓰고, Recall이 (Index를 거쳐) 읽는다.
- Memory Store와 Memory Index는 하나의 영속성 백엔드 뒤에 있으며, 소비자에게는 Memory Service Interface(단일 Port)를 통해서만 노출된다.
- 영속성 백엔드는 Adapter Layer 뒤에 둔다. Core Contract는 백엔드 종류(파일·DB 등)에 무관하다 (INV-8).

---

## 3.3 Invariants

- **INV-1 (단일 Port).** Memory 접근 경로는 Memory Service Interface 하나뿐이다. 소비자는 영속성 백엔드에 직접 접근하지 않는다. 우회 접근은 `PortBypass` 위반이다 (ARCHITECTURE 5.1).
- **INV-2 (회수 정책 — 목적·범위 필수).** Recall은 `purpose`와 `scope` 없이는 성립하지 않는다. 하나라도 누락되면 거부된다 (`MissingPurpose` / `MissingScope`).
- **INV-3 (전량 로드 금지).** Memory Store 전체를 반환하는 연산은 없다. `scope`는 bounded여야 하며, 전체 store를 겨냥하는 scope는 `UnboundedScope`로 거부된다.
- **INV-4 (최소 Context 우선).** 기본 회수 세분도는 `index`다. Recall은 기본적으로 Index Entry(참조)만 반환한다. `content` 원문은 `detail = full`이 명시되고 scope로 한정된 경우에만 materialize된다.
- **INV-5 (kind·content 불투명).** Memory는 `kind`와 `content`를 불투명하게 다룬다. 특화 계약(Lessons, Best Practice 등)이 kind별 값과 content 상세 스키마를 소유한다.
- **INV-6 (기록 불변).** 기록된 Memory Item은 불변이다. Record는 추가만 한다. 갱신·정정은 새 Memory Item 기록으로 표현한다. `source`와 `timestamp`는 이 불변성 위에서 의미를 가진다.
- **INV-7 (인덱스 정합).** 모든 Memory Item은 대응하는 Index Entry를 가진다. Record는 Store와 Index를 함께 갱신한다. 불일치는 `IndexInconsistent` 위반이다.
- **INV-8 (AI·백엔드 비의존).** §3의 어떤 계약도 특정 AI·직렬화·영속성 백엔드에 의존하지 않는다. 모든 환경 의존은 Adapter Layer 뒤(§4)에 둔다.

---

## 3.4 소비자 계약 (Consumer Contract)

- 소비자는 Agent, Loop, Workflow, Verifier다 (ARCHITECTURE 5.1).
- 모든 소비자는 Record와 Recall을 Memory Service Interface(단일 Port)로만 호출한다. 백엔드 직접 접근은 금지된다 (INV-1).
- **Runtime은 소비자가 아니다.** Runtime은 Memory Service를 contract `MemoryServiceInterface`의 교체 가능한 Module로 등록·배선(wiring)만 하고, Memory 내용에는 접근하지 않는다 (specs/01-runtime.md §5 단서, §8 예1과 정합).
- **특화 계약(Lessons, Best Practice 등)은 소비자가 아니다.** 이들은 Memory Item의 `kind`로 이 Port 위에 올라탄다. Memory는 일반 기록·회수만 제공하고, kind별 상세는 specs/05-lessons.md가 소유한다 (§9 조율).
- 방향: 소비자 → 04 (소비자가 이 계약을 사용). 04 §3은 소비자에 의존하지 않는다 (§2 순환 의존 참조).

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Memory Service를 Claude Code 위 파일 기반 백엔드로 실현한다. §3의 추상 계약을 다음과 같이 바인딩한다. 백엔드는 단일 Port 뒤에 격리된다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Memory Service Interface (Port) | Memory Service Provider Module. `framework/memory/`에 구현한다 (01 §4.1 "Module 구현 디렉터리"와 정합). contract = `MemoryServiceInterface` (01 §8 예1과 정합). Runtime이 01 §3.1-A Register로 등록하고 Resolve로 해소한다. |
| Memory Item 직렬화 (§3.2-A) | Memory Item의 파일 표현. 예: item 당 파일 또는 append-log 레코드. `content`는 불투명 페이로드로 직렬화한다. |
| Memory Store 물리 저장 (§3.2-E) | 파일 기반 store. 물리 경로·구조는 백엔드로서 Adapter 경계 뒤에 둔다. |
| Memory Index 물리 구현 (§3.2-C) | 파일 기반 인덱스(예: 인덱스 파일). scope 해소는 인덱스 파일 조회로 수행한다. |
| Record 실행 (§3.1-A) | Memory Item 파일 기록 + 인덱스 파일 갱신을 함께 수행한다(정합 갱신 지향, INV-7). |
| Recall 실행 (§3.1-B) | 인덱스 파일 조회로 Index Entry 후보를 해소한 뒤, scope 내 대상 Memory Item 파일만 읽는다. 전량 로드하지 않는다 (INV-3/INV-4). |
| 백엔드 격리 | store·index·직렬화·I/O는 `framework/adapters/` 뒤로 격리한다 (01 §4.1 "Adapter Binding 산출물" 경계와 정합). Port 앞에서는 백엔드가 보이지 않는다. |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI·저장 환경으로 이식할 때 바뀌는 것 전부. §3 Core Contract는 유지되고 아래만 교체된다.

1. **Memory Item / Index Entry 직렬화 포맷** — 파일 표현 → 대상 환경의 레코드 포맷.
2. **Memory Store 물리 저장** — 파일 기반 store → DB / object store 등.
3. **Memory Index 구현** — 파일 기반 인덱스 → DB 인덱스 / 검색 백엔드 등.
4. **백엔드 I/O 메커니즘** — 파일 I/O → 대상 백엔드의 접근 메커니즘.
5. **Provider Module 등록 경로** — Runtime의 Module 등록 바인딩(01 §4.2와 정합). Runtime 이식 시 함께 교체된다. Memory는 참조만 하고 정의하지 않는다.

유지되는 것: §3의 Port 시그니처(Record / Recall), 회수 정책, Memory Item 추상 스키마, Memory Index 계약, §3.3 Invariants. 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다.

---

# §5. Memory Access (해당 시)

**이 spec이 Memory Service의 정의 문서다.** Memory Service Interface(단일 Port)의 정본은 이 문서 §3이다.

따라서 이 spec은 Memory의 소비자로서 Recall/Record를 "사용"하지 않는다. 대신 그 접근 계약을 정의한다. 자기 참조를 다음과 같이 정리한다.

- 읽기(Recall) 계약: §3.1-B. 목적·범위·시점 강제: §3.1-C 회수 정책 + INV-2 / INV-3 / INV-4.
- 쓰기(Record) 계약: §3.1-A. 기록 대상: Memory Item(§3.2-A). Lesson 생성 조건: Memory는 `kind`로만 수용하고, 생성 규칙 상세는 specs/05-lessons.md 소관이다 (§9 조율).
- 단일 Port·우회 금지: §3.4, INV-1.

다른 spec의 Memory Access는 이 §3을 가리킨다.

- specs/02-agent.md §5·INV-8 (Agent 소비자) → 이 §3.1 / §3.4.
- specs/01-runtime.md §5 단서 (Runtime은 배선만, 내용 접근 안 함) → 이 §3.4.
- specs/03-loop.md, specs/06-verifier.md, specs/07-workflow.md (소비자) → 이 §3 (§9 조율).

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다. 모두 Lesson 후보다.

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| 목적 없는 회수 (`purpose` 누락) | Recall 거부. reason=MissingPurpose. INV-2로 차단. | 예 |
| 범위 없는 회수 (`scope` 누락) | Recall 거부. reason=MissingScope. INV-2로 차단. | 예 |
| 전량 로드 시도 (전체 store 겨냥 scope) | Recall 거부. reason=UnboundedScope. INV-3으로 차단. | 예 |
| scope 해소 실패 (인덱스에 부합 항목 없음) | Recall 실패. reason=ScopeUnresolvable. | 예 |
| Port 우회 — 백엔드 직접 접근 | INV-1 위반. reason=PortBypass. 단일 Port 경유로 교정. | 예 |
| 인덱스 없는 Memory Item (Store↔Index 불일치) | INV-7 위반. reason=IndexInconsistent. Record 정합 갱신으로 교정. | 예 |
| Memory가 `kind`·`content` 내부를 해석하려 시도 | 경계 침범. INV-5 위반. 상세 스키마는 05 소관으로 이관. | 예 |
| Record 스키마 위반 (필수 필드 누락) | Record 거부. reason=SchemaViolation. | 예 |
| 기록된 Memory Item 변경 시도 | INV-6 위반. 갱신은 새 Item 기록으로 표현. | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.4 완료 조건과 정렬한다.

- **단일 Port 시연.** Memory에 접근하는 모든 경로가 Memory Service Interface(단일 Port) 하나임을 보인다. 백엔드 직접 접근이 없음을 보인다 (INV-1, Cross-cutting 계약 검증).
- **회수 정책 시연 (Token Efficiency).** `purpose` 또는 `scope`가 없는 Recall이 거부되고(INV-2), 전체 store를 겨냥한 Recall이 거부되며(INV-3), 기본 회수가 Index Entry만 반환함(INV-4)을 보인다. 즉 Memory가 필요할 때만·목적을 명시하고·최소 범위로만 읽힘을 시연한다.
- **기록·회수 사이클 시연.** Memory Item을 Record하면 Index Entry가 생성되고(INV-7), 이후 scope로 Recall하면 인덱스를 거쳐 그 Item만 회수됨을 보인다. 이때 contract id가 `MemoryServiceInterface`임을 보인다 (01 §8 예1 정합).
- **포맷 일치 시연.** 임의의 Memory Item과 Index Entry가 §3.2-A / §3.2-C 스키마와 일치함을 대조로 보인다.
- **경계 시연.** Memory가 `kind`·`content`를 불투명하게 다루고, Lesson·Best Practice의 상세 스키마를 정의하지 않음을 보인다 (INV-5, 05 경계).
- **AI 비의존 시연.** §3 본문 전체를 스캔해 특정 AI 이름·모델명·제품 기능·백엔드 의존 토큰이 0건임을 보인다 (INV-8, DoD-3).

참고: ROADMAP v0.4의 "실패 → Lesson 생성 → 다음 작업에서 회수" 사이클에서 Memory는 회수(Recall)와 기록(Record) 절반을 제공한다. Lesson 생성 규칙은 specs/05-lessons.md, 사이클 구동(단계 전이)은 specs/03-loop.md 소관이다 (§9 조율).

## 검증 방법

- Verifier가 소비자의 Memory 접근 경로를 추적해 단일 Port 경유임을 확인한다.
- Verifier가 `purpose`/`scope` 누락·전량 로드·index 기본값에 대한 거부/반환을 §3.1과 대조한다.
- Verifier가 Record → Index Entry 생성 → scope Recall 회수 사이클을 실행해 결과를 확인한다.
- Verifier가 Memory Item·Index Entry 필드를 §3.2 스키마와 대조한다.
- Verifier가 §3 본문에서 금지 토큰(특정 AI 이름·모델명·제품 기능·백엔드)이 0건임을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 기록·회수 (Record → Recall, index-first)**

Record 입력 (Memory Item):
- kind: `decision`
- content: (불투명 페이로드 — 어떤 설계 결정의 기록)
- source: Advisor / 작업 A / 사이클 3
- timestamp: (기록 시점)
- labels: { topic: memory, task: A }

→ Record가 `id`를 유일 할당하고, 대응 Index Entry(id, kind, source, timestamp, labels, digest)를 Memory Index에 생성한다 (INV-7).

Recall 입력 (Recall Request):
- purpose: "작업 A의 이전 설계 결정 참조"
- scope: { labels: { task: A }, kind: `decision` }
- detail: `index` (기본값)

→ Recall이 Memory Index로 scope를 해소해 Index Entry 후보만 반환한다. content 원문은 로드하지 않는다 (INV-4). 소비자가 특정 `id`의 원문이 필요하면 `scope = { id }`, `detail = full`로 다시 Recall한다. 접근은 contract `MemoryServiceInterface`(단일 Port) 경유다.

**예 2 — 회수 정책 강제 (거부 케이스)**

- Recall(purpose 누락) → `MissingPurpose`로 거부 (INV-2).
- Recall(scope 누락) → `MissingScope`로 거부 (INV-2).
- Recall(scope = 전체 store, narrowing 차원·limit 없음) → `UnboundedScope`로 거부 (INV-3).

→ "필요할 때만, 목적을 명시하고, 최소 범위로"가 인터페이스 수준에서 강제됨을 보인다.

**예 3 — 특화 계약이 위에 올라탐 (Lessons)**

Lesson은 Memory Item의 한 `kind`로 Record된다.
- kind: (05가 정의하는 Lesson kind 값)
- content: (05가 정의하는 Lesson 상세 스키마 — Memory는 불투명 취급)

→ Memory는 이 Item을 일반 Memory Item과 동일하게 기록·인덱싱·회수한다. Memory는 `content` 내부를 해석하지 않는다 (INV-5). Lesson의 kind 값·상세 포맷·생성 규칙은 specs/05-lessons.md가 소유한다. 이 예는 05의 내부 포맷을 추측하지 않으며, 특화 계약이 이 Port 위에 올라타는 경계만 보인다.

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**Glossary 추가 요청** — 용어 6종(Memory Item · Memory Store · Memory Index · Index Entry · Record(기록 연산) · Recall(회수 연산))은 00-glossary §3.2-J-04 정본 등재 완료(요청 6건 전부 Advisor 승인). 상세 필드의 정본은 이 spec §3.1·§3.2가 유지한다.

**설계 확인 요청:**

- **OQ-M1: 기본 회수 세분도 `detail = index`** — 해소(승인·확정. 근거 = 최소 Context 우선(INV-4)을 기본 동작으로 삼아 Token Efficiency(ARCHITECTURE 3.6)를 인터페이스 기본값에 내장. content 로드는 `detail = full` opt-in. 규범 정본 = §3.1 · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- **OQ-M2: 기록 불변(append-only)** — 해소(승인·확정. 근거 = `source`·`timestamp` 의미 보존과 Index 정합(INV-7) 단순화. 갱신·정정은 새 Item 기록으로 표현. 규범 정본 = INV-6 · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- **OQ-M3: scope 지정자 taxonomy** — 해소(4차원 `kind`/`labels`/`timeRange`/`source`를 v0.1로 수용. 소비자(03/06/07) 확정 결과 추가 차원 요구 없음 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

**타 spec 조율:**

- **05-lessons 조율 필요** — Lessons·Best Practice는 Memory Item의 `kind`로 이 Port 위에 올라탄다. Memory는 `kind`·`content`를 불투명하게 다루고(INV-5), kind 값·content 상세 스키마·생성 규칙은 05가 소유한다. 조율 지점: (1) Lesson/Best Practice가 사용할 `kind` 값의 명명, (2) 회수 시 scope의 `labels`/`kind`를 통한 Lesson 선택 방식. 05의 내부 포맷을 추측·인용하지 않았다.
- **03-loop 조율 필요** — Memory Update 단계에서 Record가, Consult 단계에서 Recall이 언제 호출되는가(단계 전이 시점)는 03 소관이다. Memory는 연산 계약만 정의하고 호출 시점은 정의하지 않았다. ROADMAP v0.4의 "실패 → Lesson → 회수" 사이클 구동도 03이 오케스트레이션한다.
- **06-verifier / 07-workflow 조율 필요** — Verifier와 Workflow는 소비자다. 두 spec이 Memory 접근을 이 §3.1 / §3.4 계약으로 선언하는지 확정 시 정합을 확인한다. 두 spec의 내용을 추측·인용하지 않았다.
- **01-runtime 조율 (확인됨)** — Memory Service Provider가 contract `MemoryServiceInterface`의 Module로 등록된다. 01 §5 단서(Runtime은 배선만, 내용 접근 안 함)·§8 예1(contract id `MemoryServiceInterface`)과 정합함을 확인했다. 01은 Frozen 확정 상태로 인용 가능하다.
- **02-agent 조율 (확인됨)** — 02 §5·INV-8이 Agent의 단일 Port 접근을 선언하고 상세를 이 spec에 위임한다. 방향 02 → 04로 정합하며 순환은 없다(§2). 02는 Frozen 확정 상태로 인용 가능하다.

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 5.1(단일 Port·회수 정책 내장·백엔드 Adapter 뒤·Lessons는 특화 계약)·3.6(Token Efficiency)·6(Cross-cutting Service)과 Glossary §3.2-B/C에 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

- OQ-M1 승인 — 기본 회수 세분도 detail=index 확정.
- OQ-M2 승인 — 기록 불변(append-only) 확정.
- OQ-M3 — scope 4차원(kind/labels/timeRange/source)을 v0.1로 수용. 소비자 확정 결과 추가 차원 요구 없음.
- 05 조율 결정: applicability 매칭의 계약 표면은 05가 소유하고 구현은 Adapter 소관이다. Port는 kind/labels/timeRange/source 범위 조회만 제공하며(04 계약 변경 없음), 매칭은 Port 위에서 수행된다. applicability는 labels·kind로 투영 가능하다.
- 회수 이력(작업별 회수 집합) 조회: 03의 루프 상태 기록 소관으로 확정. 05는 입력으로 받는다.
- Glossary 추가 요청 6건 승인 — Glossary §3.2-J 반영.

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 OQ(OQ-M1·M2·M3)의 원문+답 이중 잔존 1줄화, Glossary 추가 요청 블록의 등재 완료 1줄화, §2·§9 stale 상태 표기(Review/Adopted → Frozen) 현행 정정. 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — §3 전체·§6 표·§7 무촉, dependents(§2 목록 = 02·03·05·06·07) 참조 영향 0(정책 §4-a·§4-c). 종전 문면 = git 앵커 90ca19c.
