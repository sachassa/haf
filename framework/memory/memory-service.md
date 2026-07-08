# framework/memory/memory-service — Memory Service Interface (단일 Port) 계약 인스턴스

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/04-memory.md §3.1-A — Record(쓰기) 연산. 본 문서가 인스턴스화하는 계약의 정본. 입력·출력·완료 조건·실패 reason의 진위 판정 기준은 이 §가 유지한다.
- specs/04-memory.md §3.1-B — Recall(읽기) 연산. 입력·출력·완료 조건·실패 reason의 정본.
- specs/04-memory.md §3.1-C — 회수 정책(Recall Policy). 계약 내장 읽기 규칙의 정본.
- specs/04-memory.md §3.2-A — Memory Item 추상 스키마. 필드명·의미·필수/선택 표기의 정본.
- specs/04-memory.md §3.2-B — Recall Request / Recall Result. 필드명·의미·필수/선택 표기의 정본.
- specs/04-memory.md §3.2-C — Memory Index / Index Entry. 필드명·의미의 정본.
- specs/04-memory.md §3.2-D — Failure Report 공통 구조. `operation`/`reason`/`target`/`location` 구조의 정본.
- specs/04-memory.md §3.3 INV-1~8 — 불변 규칙. 본 문서는 재정의하지 않고 § 포인터로 참조한다.
- specs/04-memory.md §3.4 — 소비자 계약. 단일 Port·우회 금지의 정본.
- specs/04-memory.md §8 예1·예2 — 기록·회수(index-first) 사이클, 회수 정책 강제(거부 케이스) 예시.
- specs/01-runtime.md §8 예1 — contract id `MemoryServiceInterface` 정합 기준 (자매 문서 framework/memory/module-manifest.md의 Manifest `contract` 값과 정합).
- framework/core/structure.md §2·§5 — Module 구현 디렉터리 경계(자기완결, C-3 확장 — 문서 본문 AI·언어·툴체인 비의존), 금지 토큰 규칙. §0 정본 경계.

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인·직렬화 형식 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. 04 §3.1-A(Record)·§3.1-B(Recall)·§3.1-C(회수 정책)·§3.2-A(Memory Item)·§3.2-B(Recall Request/Result)·§3.2-C(Memory Index/Index Entry)·§3.2-D(Failure Report) 인스턴스 절(필드 필수/선택 표기 정본 대조 보존), 기록·회수 프로토콜(Record = Item 기록+Index Entry 생성 함께 완료 — INV-7, Recall = index-first — INV-4·§8 예1), reason 코드 8종 소속 § 명시, 04 §3.3 INV-1~8 대조. 04 계약 재정의·확장 0, 05-lessons 내부 포맷 불인용, Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task M2) |
| 2026-07-05 | v0.4 Draft (r2) | Advisor 재작업 지시 반영. (1) 말미 요약 절 헤더의 § 번호를 머리 이력 절과 충돌하지 않게 §10으로 개칭, 05 조율 참조를 `04 §9`로 명시화. (2) §4.1(Memory Item)·§4.3(Memory Index/Index Entry) 전문 표 제거 → 04 §3.2-A/§3.2-C 정본 + framework/memory/memory-store.md §2·§3 소유 포인터로 대체(이중 갱신 방지); §4.2·§4.4는 M2 소유 유지. §1·§2 표·§2 주·§4 도입·§10에서 §4.1/§4.3 참조 전 지점 갱신. (3) Recall 시스템 상한 값 원천 = Provider Module Config `recall.limit.max`(기본 20)로 확정(Advisor 결정 DP-M1) — §3.2 주·§8 값 원천 서술을 확정형으로 갱신. | Worker (Advisor 재작업 지시, Task M2 r2) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/04-memory.md §3이다.** 이 문서는 그 Memory Service Interface(단일 Port) Core Contract의 **인스턴스**이며, 연산·데이터 포맷·불변 규칙·회수 정책을 **재정의·확장하지 않는다**. 계약 요소는 04의 해당 §를 § 포인터로 참조한다 (framework/core/structure.md §7 확정 조건 C-1 정합 — 인스턴스는 계약 변경이 아니다).
- 이 문서는 Memory Service Interface를 이 프로젝트에서 **어떻게 노출·운용하는가**를 규율하는 규격이다. 연산·필드의 진위 판정 기준은 항상 04 §3이다. 아래 표는 정본과 일치하게 옮긴 **인스턴스 대조**이며, 이 문서에서 계약의 진위가 새로 확정되지 않는다.
- **이 문서는 Module 구현 디렉터리 문서다** (framework/core/structure.md §2 — `framework/memory/`가 이 경계의 첫 실사용 인스턴스). 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (framework/core/structure.md §5 C-3 확장, 04 §3.3 INV-8). 물리 저장·직렬화·영속성 백엔드·물리 진입점 해소는 **Adapter Binding 문서 소관**이며 (04 §4), 필요한 자리에는 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Memory Item / Memory Store / Memory Index / Index Entry / Record / Recall은 04 §9 Glossary 추가 요청 6건이 승인되어 Glossary §3.2-J가 정본이다 (04 §9 결정 기록). 새 용어를 정본처럼 신설하지 않는다.
- **특화 계약(Lessons, Best Practice 등)은 이 문서 소관이 아니다.** Memory는 `kind`·`content`를 불투명하게 다루며(04 INV-5), kind 값·content 상세 스키마·생성 규칙은 특화 계약 소관이다 — 정본은 specs/05-lessons.md, 이 프로젝트의 구현 인스턴스는 framework/memory/lessons.md 소관이다. 이 문서는 특화 계약의 내부 포맷을 인용·추측하지 않고 경계 포인터만 둔다 (04 §9 05 조율).

---

## §1. 목적

Memory Service Interface는 UAHF의 기억 능력에 접근하는 **정확히 하나의 Port**다 (04 §3, ARCHITECTURE 5.1). 이 문서는 그 단일 Port 계약을 이 프로젝트의 인스턴스로 확정하고, 그 위에서 기록·회수가 어떻게 운용되는가를 규율한다.

이 규격의 책임은 세 가지다.

- 04 §3의 두 연산(Record·Recall)·하나의 회수 정책·이 Port의 요청/보고 데이터 계약(Recall Request/Result·Failure Report)을 **재정의 없이** 인스턴스화한다 — 필드의 필수/선택 표기를 정본 그대로 보존한다 (필수/선택 표기 보존 — session-handoff-v0.2 §1.5 Lesson 후보 2). Memory Item·Memory Index/Index Entry(04 §3.2-A/§3.2-C)는 인스턴스 소유가 framework/memory/memory-store.md이므로 § 포인터로만 참조한다 (전문 표 중복 없음 — 이중 갱신 방지, Advisor 조율 확정 Task M2 r2).
- **기록·회수 프로토콜**을 명문화한다 — Record는 Item 기록과 Index Entry 생성을 함께 완료하고(04 INV-7), Recall은 index-first로 최소 Context만 회수한다(04 INV-4, §8 예1).
- 연산별 거부·실패 reason 코드를 소속 §과 함께 정리하여, 서로 다른 연산의 reason 코드가 혼입되지 않게 한다 (필드 계약 혼입 방지 — session-handoff-v0.2 §1.5 Lesson 후보 1).

Memory 접근 경로는 이 Port 하나뿐이다. 영속성 백엔드는 이 Port 뒤 Adapter Layer에 격리된다 (04 INV-1·INV-8, §4.1 — 물리 실현은 Adapter Binding 문서 소관).

---

## §2. Port 개요 (단일 Port 구성)

Memory Service는 정확히 하나의 Port(Memory Service Interface)를 노출한다 (04 §3). 이 Port는 다음으로 구성된다.

| 구성 요소 | 정본 § | 이 문서의 절 |
|---|---|---|
| Record 연산 (쓰기) | 04 §3.1-A | §3.1 |
| Recall 연산 (읽기) | 04 §3.1-B | §3.2 |
| 회수 정책 (Recall Policy) — 계약 내장 | 04 §3.1-C | §3.3 |
| Memory Item 데이터 계약 | 04 §3.2-A | §4.1 (포인터 — 인스턴스 소유 memory-store.md §2) |
| Recall Request / Recall Result 데이터 계약 | 04 §3.2-B | §4.2 |
| Memory Index / Index Entry 데이터 계약 | 04 §3.2-C | §4.3 (포인터 — 인스턴스 소유 memory-store.md §3) |
| Failure Report 공통 구조 | 04 §3.2-D | §4.4 |
| 소비자 계약 (Agent·Loop·Workflow·Verifier) | 04 §3.4 | §7 |

- 모든 연산의 실패는 공통 Failure Report(§4.4)로 보고한다 (04 §3.1).
- **Memory Item·Memory Index/Index Entry·Memory Store 저장 구조(04 §3.2-A/§3.2-C/§3.2-E)의 인스턴스는 framework/memory/memory-store.md가 단일 소유한다.** 본 문서(§4.1·§4.3)는 그 데이터 계약을 § 포인터로만 참조하고 전문 표를 중복하지 않는다 (이중 갱신 방지 — Advisor 조율 확정, Task M2 r2). Record가 쓰고 Recall이 (Index를 거쳐) 읽는 대상이며, 물리 저장·직렬화·백엔드는 Adapter Binding 문서 소관이다 (04 §4, INV-8).

---

## §3. Interface 인스턴스 (04 §3.1)

아래 절은 04 §3.1의 연산 계약을 정본과 일치하게 옮긴 인스턴스다. 입력·출력·완료 조건·실패 reason의 진위 판정 기준은 04 §3.1이며, 본 문서는 재정의하지 않는다.

### §3.1 Record — 쓰기 (04 §3.1-A)

- **입력.** Memory Item(§4.1) 1건. `id`를 제외한 필수 필드(`kind`, `content`, `source`, `timestamp`)를 모두 포함한다.
- **출력.** 기록 결과 — 할당된 Memory Item `id`.
- **완료 조건.** Memory Item이 §4.1(정본 04 §3.2-A) 스키마를 만족하고, `id`가 Memory Store에서 유일하게 할당되며, 대응하는 Index Entry(§4.3, 정본 04 §3.2-C)가 Memory Index에 생성된다.
- **실패 보고.** reason = `SchemaViolation` | `DuplicateId` | `IndexInconsistent` (전부 Record 소속 — 04 §3.1-A. §5 reason 표 참조).

Record는 Memory Item을 **추가(append)** 한다. 이미 기록된 Memory Item은 불변이다 (04 INV-6). 갱신·정정은 새 Memory Item 기록으로 표현한다. `source`와 `timestamp`는 이 불변성 위에서 의미를 가진다.

### §3.2 Recall — 읽기 (04 §3.1-B)

- **입력.** Recall Request(§4.2). `purpose`와 `scope`는 필수다.
- **출력.** Recall Result(§4.2) — scope로 한정된 Index Entry 집합(`detail = index`) 또는 Memory Item 집합(`detail = full`)과 절단(`truncated`) 표시.
- **완료 조건.** `purpose`와 `scope`가 모두 존재하고, `scope`가 bounded이며(§3.3), `scope`가 Memory Index로 해소되고, 반환량이 scope의 `limit`과 시스템 상한을 넘지 않는다.
- **실패 보고.** reason = `MissingPurpose` | `MissingScope` | `UnboundedScope` | `ScopeUnresolvable` (전부 Recall 소속 — 04 §3.1-B. §5 reason 표 참조).

Recall은 어떤 경우에도 Memory Store 전량을 반환하지 않는다 (04 INV-3).

주 (시스템 상한 — 값 원천 확정). Recall 완료 조건과 Recall Request `limit`(§4.2)이 참조하는 "시스템 상한"의 **값 원천**은 이 Provider Module의 Config다 (Advisor 결정 DP-M1, v0.4). 04 §3.1-B는 상한의 존재만 규정하고 값 원천은 실현 소관이며, Module scope config(01 §3.2-B)가 그 자리다. 구체 키·타입·기본값은 자매 문서 framework/memory/module-manifest.md의 `configSchema` 선언 — 키 `recall.limit.max`(유한 양의 정수, 기본값 20)이다.

### §3.3 회수 정책 (Recall Policy) — 계약 내장 (04 §3.1-C)

회수 정책은 Token Efficiency 원칙(ARCHITECTURE 3.6)의 계약 구현이다. Glossary §3.2-C의 "필요할 때만, 목적을 명시하고, 최소 범위로 읽는다"를 Port가 강제한다 (04 §3.1-C).

| 정책 문구 | 계약 강제 지점 (정본 04 §3.1-C) |
|---|---|
| 필요할 때만 | `purpose` 필수 — 목적이 없으면 Recall이 성립하지 않는다. 무목적·상시 회수는 유효한 purpose를 가질 수 없다. 회수 "시점"의 판단은 소비자와 Loop(specs/03-loop.md)에 있으나, Port는 목적 없는 회수를 거부한다. |
| 목적을 명시하고 | `purpose` 필수 — 모든 Recall은 회수 이유를 명시한다. |
| 최소 범위로 | `scope` 필수 + bounded 강제 — 전체 store를 겨냥하는 scope(narrowing 차원도 finite limit도 없는 scope)는 `UnboundedScope`로 거부된다. 기본 회수 세분도(`detail`)는 `index`로, content 원문 없이 후보만 반환한다. content는 명시적으로 `detail = full`을 요청하고 scope로 한정된 경우에만 materialize된다. |

전량 로드는 금지된다. 회수 정책은 04 §3.3 INV-2 / INV-3 / INV-4로 불변화된다 (§6 대조).

---

## §4. Data Format 인스턴스 (04 §3.2)

이 절은 Port 인터페이스가 다루는 데이터 계약을 규율한다. **§4.2(Recall Request/Result)·§4.4(Failure Report)는 이 Port의 요청/보고 계약으로 M2가 인스턴스를 단일 소유**하며, 필드 표는 04 §3.2-B/§3.2-D 정본과 일치하게 옮긴 인스턴스 대조다(필드명·의미·필수/선택 표기 정본 그대로 — session-handoff-v0.2 §1.5 Lesson 후보 2, 재정의 아님). **§4.1(Memory Item)·§4.3(Memory Index/Index Entry)는 인스턴스 소유가 framework/memory/memory-store.md이므로 § 포인터 절로만 둔다**(전문 표 중복 없음 — 이중 갱신 방지, Advisor 조율 확정 Task M2 r2). 직렬화 형식·물리 저장은 Adapter Binding 문서 소관이다 (04 §4).

### §4.1 Memory Item (포인터 — 정본 04 §3.2-A)

Memory Item은 기억의 최소 기록 단위이며 Record의 입력이다 (§3.1). Recall Result의 `entries`는 `detail = full`일 때 Memory Item 집합이 된다 (§4.2).

- **필드 스키마 정본:** 04 §3.2-A (필드명·의미·필수/선택 표기 포함).
- **이 프로젝트의 인스턴스 소유:** framework/memory/memory-store.md §2. 필드 전문 표는 그 문서가 단일 소유하며, 본 문서는 중복 인스턴스를 두지 않는다 (이중 갱신 방지 — Advisor 조율 확정, Task M2 r2).
- **이 Port가 필요로 하는 관계:** Record 입력은 Memory Item 1건이며 `id`를 제외한 필수 필드를 모두 포함한다 (§3.1). Memory는 `kind`·`content`를 불투명하게 다룬다 (04 INV-5) — kind 값·content 상세 스키마는 특화 계약 소관이다 (정본 specs/05-lessons.md; 구현 인스턴스는 framework/memory/lessons.md 소관 — §0, 04 §9).

### §4.2 Recall Request / Recall Result (정본 04 §3.2-B)

**Recall Request**

| 필드 | 의미 (정본: 04 §3.2-B) | 필수 |
|---|---|---|
| `purpose` | 회수 목적. 이 회수가 왜 필요한가. | 예 |
| `scope` | 회수 범위 지정자. 반환 대상을 한정한다. narrowing 차원(`kind` / `labels` / `timeRange` / `source`) 중 최소 하나 또는 finite `limit`을 가져야 한다. 전체 store를 겨냥하는 scope는 거부된다. | 예 |
| `detail` | 반환 세분도. `index`(Index Entry만) 또는 `full`(Memory Item). 기본값 `index`. | 아니오(기본 `index`) |
| `limit` | 최대 반환 개수. 미지정 시 시스템 상한을 적용한다. | 아니오 |

**Recall Result**

| 필드 | 의미 (정본: 04 §3.2-B) |
|---|---|
| `entries` | scope에 부합하는 Index Entry(§4.3) 또는 Memory Item(§4.1)의 정렬된 집합. `detail`에 따라 결정된다. |
| `truncated` | 결과가 `limit` 또는 시스템 상한으로 절단되었는지 여부. |

(Recall Result는 정본 04 §3.2-B에 필수 열이 없다 — 필드/의미 2열 그대로 옮긴다.)

### §4.3 Memory Index / Index Entry (포인터 — 정본 04 §3.2-C)

Memory Index는 scope 지정자(`kind` / `labels` / `timeRange` / `source`)를 Index Entry 집합으로 해소하는 조회 구조이고, Index Entry는 그 경량 서술자다. Recall은 기본적으로 Index Entry만 반환하고(index-first, §5.2), Record는 Memory Item마다 대응 Index Entry를 생성한다 (§5.1).

- **필드 스키마 정본:** 04 §3.2-C (필드명·의미 포함, `digest`의 "(선택)" 표기 포함).
- **이 프로젝트의 인스턴스 소유:** framework/memory/memory-store.md §3. 필드 전문 표는 그 문서가 단일 소유하며, 본 문서는 중복 인스턴스를 두지 않는다 (이중 갱신 방지 — Advisor 조율 확정, Task M2 r2).
- **이 Port가 필요로 하는 관계:** Recall이 Memory Index로 scope를 해소해 Index Entry를 반환하고(§3.2·§5.2), Record가 Item 기록과 Index Entry 생성을 함께 완료한다 (§3.1·§5.1, 04 INV-7). Index Entry는 `content` 원문을 담지 않는다 (04 INV-4). Memory Index의 물리 구현은 Adapter Binding 문서 소관이다 (04 §4.1).

### §4.4 Failure Report (정본 04 §3.2-D)

모든 Memory Service 연산의 공통 실패 보고 구조다. 이 구조는 04 §3.2-D가 정본이며, 본 문서는 재정의하지 않고 연산별 reason 코드만 §5에서 전개한다.

| 필드 | 의미 (정본: 04 §3.2-D) |
|---|---|
| `operation` | 실패한 연산 (Record / Recall). |
| `reason` | 사유 코드 (SchemaViolation / DuplicateId / IndexInconsistent / MissingPurpose / MissingScope / UnboundedScope / ScopeUnresolvable / PortBypass). |
| `target` | 대상 (Memory Item `id`, scope 지정자, label, kind). |
| `location` | 실패 지점 참조. |

(Failure Report는 정본 04 §3.2-D에 필수 열이 없다 — 필드/의미 2열 그대로 옮긴다. reason 코드의 소속 연산·§은 §5에서 명시한다.)

---

## §5. 기록·회수 프로토콜

04 §3.1의 두 연산을 이 프로젝트의 운용 프로토콜로 전개한다. 계약의 진위 판정 기준은 04 §3.1이며(§0), 아래는 그 계약을 운용 절차로 편 것이다.

### §5.1 Record 프로토콜 — Item 기록 + Index Entry 생성 함께 완료 (04 INV-7)

1. 입력 Memory Item의 `id` 제외 필수 필드(`kind`·`content`·`source`·`timestamp`)를 확인한다. 필수 필드가 누락되면 §4.1(정본 04 §3.2-A) 스키마 위반이므로 기록하지 않는다 (`SchemaViolation` — Record, 04 §3.1-A).
2. `id`를 Memory Store에서 **유일하게** 할당한다. 유일 할당이 성립하지 않으면 기록하지 않는다 (`DuplicateId` — Record, 04 §3.1-A).
3. Memory Item 기록과 **대응 Index Entry(§4.3) 생성**을 함께 완료한다. 모든 Memory Item은 대응 Index Entry를 가져야 하며(04 INV-7), Store↔Index 불일치는 실패다 (`IndexInconsistent` — Record, 04 §3.1-A).
4. Record는 **추가(append)** 만 한다. 기록된 Memory Item은 불변이다 (04 INV-6). 갱신·정정은 새 Memory Item 기록으로 표현한다.
5. `content`는 불투명 페이로드로 다룬다 (04 INV-5). Memory는 `kind`·`content` 내부를 해석하지 않는다 — 해석 시도는 경계 침범이다 (04 §6, INV-5).

물리 기록·인덱스 갱신의 실현(정합 갱신 메커니즘 포함)은 Adapter Binding 문서 소관이다 (04 §4.1). 이 문서는 계약 수준 프로토콜만 규율한다.

### §5.2 Recall 프로토콜 — index-first (04 INV-4, §8 예1)

1. `purpose`와 `scope`가 모두 존재하는지 확인한다. 하나라도 없으면 거부한다 (`MissingPurpose` / `MissingScope` — Recall, 04 §3.1-B, INV-2).
2. `scope`가 bounded인지 확인한다 — narrowing 차원(`kind` / `labels` / `timeRange` / `source`) 최소 하나 또는 finite `limit`을 가져야 한다. 전체 store를 겨냥하는 scope는 거부한다 (`UnboundedScope` — Recall, 04 §3.1-B, INV-3).
3. `scope`를 **Memory Index로 해소**해 Index Entry 후보를 찾는다. Memory Store 전체를 스캔·로드하지 않는다. 인덱스에 부합 항목이 없으면 해소 실패다 (`ScopeUnresolvable` — Recall, 04 §3.1-B).
4. **기본은 index-first다.** `detail`의 기본값은 `index`이므로 Recall은 기본적으로 Index Entry(참조)만 반환한다 (04 INV-4). `content` 원문은 `detail = full`이 **명시되고 scope로 한정된** 경우에만 materialize된다.
5. 반환량이 scope의 `limit`과 시스템 상한을 넘지 않게 하고, 절단 시 `truncated`로 표시한다 (§4.2). Recall은 어떤 경우에도 Memory Store 전량을 반환하지 않는다 (04 INV-3).

예(정본 04 §8 예1 정합). 소비자가 `scope = { labels: { task: A }, kind: decision }`, `detail = index`(기본값)로 Recall하면 Index Entry 후보만 반환된다. 특정 `id`의 원문이 필요하면 `scope = { id }`, `detail = full`로 다시 Recall한다. 접근은 contract `MemoryServiceInterface`(단일 Port) 경유다.

### §5.3 reason 코드 소속 § (연산별 — 혼입 방지)

reason 코드는 연산별로 소속이 구분된다. 서로 다른 연산의 reason 코드를 섞지 않는다 (필드 계약 혼입 방지 — session-handoff-v0.2 §1.5 Lesson 후보 1). Failure Report **구조**의 정본은 04 §3.2-D이며, 아래는 그 `reason` 값 8종의 소속만 정리한 목록이다.

| reason 코드 | 소속 (연산 / 불변 규칙) | 소속 § (정본) | 사유 |
|---|---|---|---|
| `SchemaViolation` | Record | 04 §3.1-A | Memory Item 필수 필드 누락 등 §4.1(04 §3.2-A) 스키마 위반. |
| `DuplicateId` | Record | 04 §3.1-A | 할당하려는 `id`가 Memory Store에서 유일하지 않음. |
| `IndexInconsistent` | Record (INV-7) | 04 §3.1-A | Store↔Index 불일치 — 대응 Index Entry 없는 Memory Item. |
| `MissingPurpose` | Recall (INV-2) | 04 §3.1-B | `purpose` 누락 — 회수 정책 위반. |
| `MissingScope` | Recall (INV-2) | 04 §3.1-B | `scope` 누락 — 회수 정책 위반. |
| `UnboundedScope` | Recall (INV-3) | 04 §3.1-B | 전체 store를 겨냥하는 scope — 전량 로드 시도. |
| `ScopeUnresolvable` | Recall | 04 §3.1-B | scope가 Memory Index로 해소되지 않음(부합 항목 없음). |
| `PortBypass` | 연산 무관 — 단일 Port 우회 | 04 §3.3 INV-1 | 영속성 백엔드 직접 접근. 단일 Port(§7) 경유로 교정. |

주:

- `SchemaViolation`·`DuplicateId`·`IndexInconsistent`는 **Record**(04 §3.1-A) 소속이며, `MissingPurpose`·`MissingScope`·`UnboundedScope`·`ScopeUnresolvable`는 **Recall**(04 §3.1-B) 소속이다. 두 집합은 섞이지 않는다. 어느 연산의 실패인지는 Failure Report의 `operation` 필드로 구분된다 (구조 정본 04 §3.2-D).
- `PortBypass`는 특정 연산의 완료 조건 실패가 아니라 단일 Port 우회(04 INV-1) 위반이므로, 소속을 04 §3.3 INV-1로 명시한다. `operation`은 우회가 대체하려 한 연산(Record 또는 Recall)을 가리킬 수 있으나, reason의 근거는 INV-1이다.

---

## §6. Invariants 대조 (04 §3.3 INV-1~8)

04 §3.3의 8개 불변 규칙을 이 인스턴스가 어떻게 지키는지 대조한다. 불변 규칙의 정본은 04 §3.3이며, 본 문서는 재정의하지 않고 준수 지점만 가리킨다.

| 불변 규칙 (정본 04 §3.3) | 이 인스턴스의 준수 지점 |
|---|---|
| INV-1 (단일 Port) | §2 Port 개요·§7 소비자 계약 — 접근 경로는 이 Port 하나. 우회는 `PortBypass`(§5.3). |
| INV-2 (회수 정책 — 목적·범위 필수) | §3.2·§3.3·§5.2 1 — `purpose`·`scope` 없는 Recall 거부(`MissingPurpose`/`MissingScope`). |
| INV-3 (전량 로드 금지) | §3.2·§3.3·§5.2 2·5 — bounded scope 강제, 전량 반환 없음(`UnboundedScope`). |
| INV-4 (최소 Context 우선) | §3.3·§4.2(`detail` 기본 `index`)·§5.2 4 — 기본 index-first, content는 `detail=full`+scope 한정 시에만. |
| INV-5 (kind·content 불투명) | §4.1·§5.1 5 — `kind`·`content` 불투명 취급, 상세는 특화 계약(05) 소관. |
| INV-6 (기록 불변) | §3.1·§5.1 4 — Record는 append만, 갱신은 새 Item. |
| INV-7 (인덱스 정합) | §3.1·§4.3·§5.1 3 — 모든 Item에 대응 Index Entry, Record가 함께 갱신(`IndexInconsistent`). |
| INV-8 (AI·백엔드 비의존) | §0·본문 전체 — 특정 AI·직렬화·백엔드 토큰 0, 물리 실현은 Adapter Binding 소관. |

---

## §7. 소비자 계약 (04 §3.4)

- 소비자는 Agent, Loop, Workflow, Verifier다 (04 §3.4, ARCHITECTURE 5.1).
- 모든 소비자는 Record와 Recall을 Memory Service Interface(단일 Port)로만 호출한다. 백엔드 직접 접근은 금지된다 (04 INV-1 — 우회는 `PortBypass`, §5.3).
- **Runtime은 소비자가 아니다.** Runtime은 Memory Service를 contract `MemoryServiceInterface`의 교체 가능한 Module로 등록·배선(wiring)만 하고 Memory 내용에는 접근하지 않는다 (04 §3.4, specs/01-runtime.md §5 단서·§8 예1과 정합; Provider Module 서술자는 자매 문서 framework/memory/module-manifest.md).
- **특화 계약(Lessons, Best Practice 등)은 소비자가 아니다.** Memory Item의 `kind`로 이 Port 위에 올라탄다 (04 §3.4, §8 예3). kind별 상세는 05 소관이다 (§0).
- 방향: 소비자 → 이 Port. 이 문서(04 §3의 인스턴스)는 소비자에 의존하지 않는다 (04 §2 순환 의존).

---

## §8. 정본 경계·금지 토큰·설계 확정 (self-note)

- **재정의·확장 0.** 본 문서의 모든 연산·데이터 계약·불변 규칙은 04 §3의 인스턴스다. 어떤 요소도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 04 §3이다. M2 소유 필드 표(§4.2 Recall Request/Result·§4.4 Failure Report)는 정본과 일치하게 옮긴 인스턴스 대조이며, 필수/선택 표기(예: Recall Request `detail`의 "아니오(기본 `index`)"·`limit`의 "아니오"·`purpose`/`scope`의 "예")를 정본 그대로 보존했다. Memory Item·Memory Index/Index Entry(§4.1·§4.3)는 전문 표를 두지 않고 framework/memory/memory-store.md 소유 포인터로 참조한다. 새 필드·새 reason 코드·새 연산·새 차원을 추가하지 않았다.
- **금지 토큰 0.** 본문·표·예시 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명이 0건이다 (framework/core/structure.md §5 C-3 확장). 물리 저장·직렬화·백엔드·물리 진입점 해소가 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관 (04 §4)" 포인터를 둔다 (mention/use 경계 — 금지 토큰의 예시도 누출이다, session-handoff-v0.2 §1.5 Lesson 후보 3).
- **05-lessons 불인용.** Lessons·Best Practice의 kind 값·content 상세 스키마·생성 규칙은 인용·추측하지 않고 경계 포인터(정본 specs/05-lessons.md; 구현 인스턴스는 framework/memory/lessons.md 소관)만 두었다 (04 INV-5, 04 §9 05 조율).
- **시스템 상한 값 원천 (확정).** Recall "시스템 상한"(§3.2·§4.2)의 값 원천은 Provider Module Config 키 `recall.limit.max`(유한 양의 정수, 기본값 20)로 확정되었다 (Advisor 결정 DP-M1, v0.4; 선언은 자매 문서 framework/memory/module-manifest.md `configSchema`). 04는 상한의 존재만 규정하고 값 원천은 실현 소관(Module scope config, 01 §3.2-B)이다.
- **인스턴스 소유 경계 (확정).** Memory Item(04 §3.2-A)·Memory Index/Index Entry(04 §3.2-C)의 인스턴스는 framework/memory/memory-store.md가 단일 소유한다. 본 문서 §4.1·§4.3은 전문 표를 두지 않고 § 포인터로만 참조한다 (이중 갱신 방지 — Advisor 조율 확정, Task M2 r2). §4.2(Recall Request/Result)·§4.4(Failure Report)는 M2 소유 인스턴스 표로 유지한다.

---

## §10. 요약 (한눈에 보기)

- Memory Service Interface = 기억 접근의 **단일 Port**. 정본 = 04 §3 (본 문서는 인스턴스, 재정의 아님).
- 두 연산: Record(쓰기 — Item 기록 + Index Entry 생성 함께 완료, append·불변) · Recall(읽기 — index-first, `purpose`·`scope` 필수, bounded, 전량 로드 금지).
- 회수 정책(04 §3.1-C)이 "필요할 때만·목적 명시·최소 범위"를 Port에서 강제한다 (INV-2/3/4). Recall 시스템 상한 값 원천 = Provider Module Config `recall.limit.max`(기본 20 — Advisor 결정 DP-M1; 선언은 module-manifest.md `configSchema`).
- 데이터 계약: Recall Request/Result(§4.2)·Failure Report(§4.4)는 M2 소유 인스턴스 표(04 §3.2-B/§3.2-D 정본, 필수/선택 표기 그대로); Memory Item(§4.1)·Memory Index/Index Entry(§4.3)는 인스턴스 소유가 framework/memory/memory-store.md(§2·§3)이므로 § 포인터 절.
- reason 코드 8종은 연산별 소속(Record 3 / Recall 4 / INV-1 우회 1)이 §5.3에 명시되어 혼입되지 않는다.
- 물리 저장·직렬화·백엔드·물리 진입점은 Adapter Binding 문서 소관 (04 §4). Module 구현 디렉터리 문서 본문에는 그 토큰이 0건이다 (C-3 확장).
