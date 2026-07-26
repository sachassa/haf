# framework/memory/memory-service — Memory Service Interface (단일 Port) 계약 인스턴스

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/04-memory.md §3.1-A·§3.1-B·§3.1-C — Record·Recall 연산과 회수 정책의 정본(§3).
- specs/04-memory.md §3.2-A·§3.2-B·§3.2-C·§3.2-D — Memory Item·Recall Request/Result·Memory Index/Index Entry·Failure Report의 정본(§4).
- specs/04-memory.md §3.3 INV-1~8 — 불변 규칙(§6 대조, 재정의 0).
- specs/04-memory.md §3.4 — 소비자 계약·단일 Port 우회 금지의 정본(§7).
- specs/04-memory.md §8 예1·예2 — 기록·회수(index-first) 사이클, 회수 정책 강제 예시.
- specs/01-runtime.md §8 예1 — contract id `MemoryServiceInterface` 정합 기준.
- framework/core/structure.md §2·§5 — 소속 경계·금지 토큰 규칙(C-3 확장).

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다(structure.md §2). 본문은 AI·언어·툴체인·직렬화 형식 비의존을 유지한다(structure.md §5 C-3). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. 04 §3.1-A(Record)·§3.1-B(Recall)·§3.1-C(회수 정책)·§3.2-A(Memory Item)·§3.2-B(Recall Request/Result)·§3.2-C(Memory Index/Index Entry)·§3.2-D(Failure Report) 인스턴스 절(필드 필수/선택 표기 정본 대조 보존), 기록·회수 프로토콜(Record = Item 기록+Index Entry 생성 함께 완료 — INV-7, Recall = index-first — INV-4·§8 예1), reason 코드 8종 소속 § 명시, 04 §3.3 INV-1~8 대조. 04 계약 재정의·확장 0, 05-lessons 내부 포맷 불인용, Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task M2) |
| 2026-07-05 | v0.4 Draft (r2) | Advisor 재작업 지시 반영. (1) 말미 요약 절 헤더의 § 번호를 머리 이력 절과 충돌하지 않게 §10으로 개칭, 05 조율 참조를 `04 §9`로 명시화. (2) §4.1(Memory Item)·§4.3(Memory Index/Index Entry) 전문 표 제거 → 04 §3.2-A/§3.2-C 정본 + framework/memory/memory-store.md §2·§3 소유 포인터로 대체(이중 갱신 방지); §4.2·§4.4는 M2 소유 유지. §1·§2 표·§2 주·§4 도입·§10에서 §4.1/§4.3 참조 전 지점 갱신. (3) Recall 시스템 상한 값 원천 = Provider Module Config `recall.limit.max`(기본 20)로 확정(Advisor 결정 DP-M1) — §3.2 주·§8 값 원천 서술을 확정형으로 갱신. | Worker (Advisor 재작업 지시, Task M2 r2) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 3 — 비계약 격리 개정: 경계 중복·복제 절 포인터화·감사 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다. uaf-allow-legacy: §9 기존 행은 개정 시점의 이력 기록이므로 문면을 고치지 않고 보존한다.)

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(다른 절에서 반복하지 않는다).

- **정본은 specs/04-memory.md §3이다.** 이 문서는 그 Memory Service Interface(단일 Port) Core Contract의 **인스턴스**이며 연산·데이터 포맷·불변 규칙·회수 정책을 재정의·확장하지 않는다(structure.md §7 C-1). 연산·필드의 진위 판정 기준은 항상 04 §3이다.
- **Module 구현 디렉터리 문서.** 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명)을 두지 않는다 — 규칙·분류 정본은 structure.md §5 C-3(및 04 §3.3 INV-8)이다. 물리 저장·직렬화·영속성 백엔드·물리 진입점 해소는 Adapter Binding 문서 소관이다(04 §4).
- 용어는 specs/00-glossary.md 정본만 사용한다(Memory Item / Memory Store / Memory Index / Index Entry / Record / Recall = Glossary §3.2-J, 04 §9 승인). 새 용어를 신설하지 않는다.
- **특화 계약(Lessons, Best Practice 등)은 이 문서 소관이 아니다.** Memory는 `kind`·`content`를 불투명하게 다루며(04 INV-5), kind 값·content 상세 스키마·생성 규칙은 특화 계약 소관이다 — 정본 specs/05-lessons.md, 구현 인스턴스는 framework/memory/lessons.md. 내부 포맷을 인용·추측하지 않는다(04 §9 05 조율).
- **인스턴스 소유 경계(확정).** Memory Item(04 §3.2-A)·Memory Index/Index Entry(04 §3.2-C)의 인스턴스는 framework/memory/memory-store.md §2·§3이 단일 소유한다 — 본 문서 §4.1·§4.3은 전문 표 없이 § 포인터만 둔다(이중 갱신 방지, Advisor 조율 확정 Task M2 r2). §4.2·§4.4는 본 문서(M2) 소유다.

---

## §1. 목적

Memory Service Interface는 UAHF의 기억 능력에 접근하는 **정확히 하나의 Port**다(04 §3, ARCHITECTURE 5.1). 이 문서는 그 단일 Port 계약을 인스턴스로 확정하고 기록·회수 운용을 규율한다 — 두 연산·회수 정책·요청/보고 데이터 계약의 인스턴스화(§3·§4) · 기록·회수 프로토콜(§5) · 연산별 reason 코드 소속(§5.3). 영속성 백엔드는 이 Port 뒤 Adapter Layer에 격리된다(04 INV-1·INV-8).

---

## §2. Port 개요 (단일 Port 구성)

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

모든 연산의 실패는 공통 Failure Report(§4.4)로 보고한다(04 §3.1).

---

## §3. Interface 인스턴스

정본 = `uahf/specs/04-memory.md §3.1`(재정의 0 · 입력·출력·완료 조건·실패 문면은 정본 참조).

### §3.1 Record — 쓰기 (04 §3.1-A)

- 입력 = Memory Item 1건(`id` 제외 필수 필드 `kind`·`content`·`source`·`timestamp` 포함), 출력 = 할당된 `id`. 완료 조건은 스키마 충족 + `id` 유일 할당 + 대응 Index Entry 생성이다.
- 실패 reason = `SchemaViolation` | `DuplicateId` | `IndexInconsistent` (전부 Record 소속 — §5.3).
- **본 문서 고유 델타.** Record는 **추가(append)** 만 한다 — 기록된 Memory Item은 불변이며(04 INV-6) 갱신·정정은 새 Item 기록으로 표현한다. `source`·`timestamp`는 이 불변성 위에서 의미를 가진다.

### §3.2 Recall — 읽기 (04 §3.1-B)

- 입력 = Recall Request(§4.2, `purpose`·`scope` 필수), 출력 = Recall Result(scope로 한정된 Index Entry 집합 또는 `detail = full`의 Memory Item 집합 + `truncated`). 완료 조건은 `purpose`·`scope` 존재 + bounded scope + Memory Index 해소 + 반환량이 `limit`·시스템 상한 이내다.
- 실패 reason = `MissingPurpose` | `MissingScope` | `UnboundedScope` | `ScopeUnresolvable` (전부 Recall 소속 — §5.3). Recall은 어떤 경우에도 Memory Store 전량을 반환하지 않는다(04 INV-3).
- **본 문서 고유 델타 (DP-M1 — 시스템 상한 값 원천 확정).** 04 §3.1-B는 상한의 **존재**만 규정하고 값 원천은 실현 소관이다. 그 자리는 이 Provider Module의 Config(Module scope, 01 §3.2-B)이며, 구체 키·타입·기본값은 자매 문서 framework/memory/module-manifest.md의 `configSchema` 선언 — 키 `recall.limit.max`(유한 양의 정수, 기본값 20)다.

### §3.3 회수 정책 (Recall Policy) — 계약 내장 (04 §3.1-C)

회수 정책은 Token Efficiency 원칙(ARCHITECTURE 3.6)의 계약 구현이며, Glossary §3.2-C의 "필요할 때만, 목적을 명시하고, 최소 범위로 읽는다"를 Port가 강제한다. 강제 지점의 문면 정본은 04 §3.1-C이고, 이 Port에서의 실현은 `purpose` 필수(무목적 회수 거부) · `scope` 필수 + bounded 강제(전체 store 겨냥 scope는 `UnboundedScope` 거부) · `detail` 기본 `index`(content는 `detail = full` + scope 한정 시에만 materialize)다. 전량 로드는 금지되며 04 INV-2/INV-3/INV-4로 불변화된다(§6).

---

## §4. Data Format 인스턴스 (04 §3.2)

§4.2·§4.4는 이 Port의 요청/보고 계약으로 본 문서가 인스턴스를 단일 소유하며, 필드 표는 04 §3.2-B/§3.2-D 정본과 일치하는 인스턴스 대조다. §4.1·§4.3은 인스턴스 소유가 memory-store.md이므로 포인터 절이다(§0). 직렬화 형식·물리 저장은 Adapter Binding 소관이다(04 §4).

### §4.1 Memory Item (포인터 — 정본 04 §3.2-A)

- 필드 스키마 정본 = 04 §3.2-A. 이 프로젝트의 인스턴스 소유 = framework/memory/memory-store.md §2(전문 표 단일 소유).
- **이 Port가 필요로 하는 관계:** Record 입력은 Memory Item 1건이며(§3.1), Recall Result의 `entries`는 `detail = full`일 때 Memory Item 집합이 된다(§4.2). Memory는 `kind`·`content`를 불투명하게 다룬다(04 INV-5 — 상세는 특화 계약 소관, §0).

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

- 필드 스키마 정본 = 04 §3.2-C(`digest`의 "(선택)" 표기 포함). 이 프로젝트의 인스턴스 소유 = framework/memory/memory-store.md §3.
- **이 Port가 필요로 하는 관계:** Recall이 Memory Index로 scope를 해소해 Index Entry를 반환하고(§3.2·§5.2), Record가 Item 기록과 Index Entry 생성을 함께 완료한다(§3.1·§5.1, 04 INV-7). Index Entry는 `content` 원문을 담지 않는다(04 INV-4). Memory Index의 물리 구현은 Adapter Binding 소관이다(04 §4.1).

### §4.4 Failure Report (정본 04 §3.2-D)

| 필드 | 의미 (정본: 04 §3.2-D) |
|---|---|
| `operation` | 실패한 연산 (Record / Recall). |
| `reason` | 사유 코드 (SchemaViolation / DuplicateId / IndexInconsistent / MissingPurpose / MissingScope / UnboundedScope / ScopeUnresolvable / PortBypass). |
| `target` | 대상 (Memory Item `id`, scope 지정자, label, kind). |
| `location` | 실패 지점 참조. |

(Failure Report는 정본 04 §3.2-D에 필수 열이 없다 — 필드/의미 2열 그대로 옮긴다. reason 코드의 소속 연산·§은 §5.3에서 명시한다.)

---

## §5. 기록·회수 프로토콜

04 §3.1의 두 연산을 운용 프로토콜로 전개한다. 계약의 진위 판정 기준은 04 §3.1이다(§0).

### §5.1 Record 프로토콜 — Item 기록 + Index Entry 생성 함께 완료 (04 INV-7)

1. `id` 제외 필수 필드(`kind`·`content`·`source`·`timestamp`)를 확인한다. 누락이면 기록하지 않는다(`SchemaViolation`).
2. `id`를 Memory Store에서 **유일하게** 할당한다. 성립하지 않으면 기록하지 않는다(`DuplicateId`).
3. Memory Item 기록과 **대응 Index Entry 생성**을 함께 완료한다. Store↔Index 불일치는 실패다(`IndexInconsistent`, 04 INV-7).
4. Record는 **추가(append)** 만 한다. 기록된 Item은 불변이며 갱신·정정은 새 Item 기록으로 표현한다(04 INV-6).
5. `content`는 불투명 페이로드로 다룬다(04 INV-5) — 해석 시도는 경계 침범이다(04 §6).

물리 기록·인덱스 갱신의 실현(정합 갱신 메커니즘 포함)은 Adapter Binding 소관이다(04 §4.1).

### §5.2 Recall 프로토콜 — index-first (04 INV-4, §8 예1)

1. `purpose`·`scope` 존재를 확인한다. 하나라도 없으면 거부한다(`MissingPurpose` / `MissingScope`, 04 INV-2).
2. `scope`가 bounded인지 확인한다 — narrowing 차원(`kind` / `labels` / `timeRange` / `source`) 최소 하나 또는 finite `limit`. 전체 store를 겨냥하면 거부한다(`UnboundedScope`, 04 INV-3).
3. `scope`를 **Memory Index로 해소**해 Index Entry 후보를 찾는다. Store 전체를 스캔·로드하지 않으며, 부합 항목이 없으면 해소 실패다(`ScopeUnresolvable`).
4. **기본은 index-first다.** `detail` 기본값이 `index`이므로 참조만 반환하고(04 INV-4), `content` 원문은 `detail = full`이 **명시되고 scope로 한정된** 경우에만 materialize된다.
5. 반환량이 `limit`과 시스템 상한을 넘지 않게 하고 절단 시 `truncated`로 표시한다(§4.2). 전량 반환은 없다(04 INV-3).

예(04 §8 예1 정합). `scope = { labels: { task: A }, kind: decision }`, `detail = index`로 Recall하면 Index Entry 후보만 반환된다. 특정 `id`의 원문이 필요하면 `scope = { id }`, `detail = full`로 다시 Recall한다. 접근은 contract `MemoryServiceInterface`(단일 Port) 경유다.

### §5.3 reason 코드 소속 § (연산별 — 혼입 방지)

Failure Report **구조**의 정본은 04 §3.2-D이며, 아래는 그 `reason` 값 8종의 소속 정리다. 서로 다른 연산의 reason 코드를 섞지 않는다.

| reason 코드 | 소속 (연산 / 불변 규칙) | 소속 § (정본) | 사유 |
|---|---|---|---|
| `SchemaViolation` | Record | 04 §3.1-A | Memory Item 필수 필드 누락 등 04 §3.2-A 스키마 위반. |
| `DuplicateId` | Record | 04 §3.1-A | 할당하려는 `id`가 Memory Store에서 유일하지 않음. |
| `IndexInconsistent` | Record (INV-7) | 04 §3.1-A | Store↔Index 불일치 — 대응 Index Entry 없는 Memory Item. |
| `MissingPurpose` | Recall (INV-2) | 04 §3.1-B | `purpose` 누락 — 회수 정책 위반. |
| `MissingScope` | Recall (INV-2) | 04 §3.1-B | `scope` 누락 — 회수 정책 위반. |
| `UnboundedScope` | Recall (INV-3) | 04 §3.1-B | 전체 store를 겨냥하는 scope — 전량 로드 시도. |
| `ScopeUnresolvable` | Recall | 04 §3.1-B | scope가 Memory Index로 해소되지 않음(부합 항목 없음). |
| `PortBypass` | 연산 무관 — 단일 Port 우회 | 04 §3.3 INV-1 | 영속성 백엔드 직접 접근. 단일 Port(§7) 경유로 교정. |

어느 연산의 실패인지는 Failure Report `operation`으로 구분된다. `PortBypass`는 특정 연산의 완료 조건 실패가 아니라 단일 Port 우회(04 INV-1) 위반이므로 소속을 04 §3.3 INV-1로 명시한다 — `operation`은 우회가 대체하려 한 연산을 가리킬 수 있으나 reason의 근거는 INV-1이다.

---

## §6. Invariants 대조 (04 §3.3 INV-1~8)

불변 규칙의 정본은 04 §3.3이며, 본 문서는 재정의하지 않고 준수 지점만 가리킨다.

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

- 소비자는 Agent, Loop, Workflow, Verifier다(04 §3.4, ARCHITECTURE 5.1).
- 모든 소비자는 Record와 Recall을 Memory Service Interface(단일 Port)로만 호출한다. 백엔드 직접 접근은 금지된다(04 INV-1 — 우회는 `PortBypass`, §5.3).
- **Runtime은 소비자가 아니다.** Runtime은 Memory Service를 contract `MemoryServiceInterface`의 교체 가능한 Module로 등록·배선만 하고 Memory 내용에는 접근하지 않는다(04 §3.4, 01 §5 단서·§8 예1; Provider Module 서술자는 framework/memory/module-manifest.md).
- **특화 계약(Lessons, Best Practice 등)은 소비자가 아니다.** Memory Item의 `kind`로 이 Port 위에 올라탄다(04 §3.4, §8 예3). kind별 상세는 05 소관이다(§0).
- 방향: 소비자 → 이 Port. 이 문서는 소비자에 의존하지 않는다(04 §2 순환 의존).
