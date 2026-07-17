# framework/memory/memory-store — UAHF Memory Store 구조·포맷 + Memory 인덱스 규격

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/04-memory.md §3.2-A — Memory Item 스키마의 정본. 본 문서 §2가 인스턴스화하는 계약.
- specs/04-memory.md §3.2-C — Memory Index / Index Entry 규격의 정본. 본 문서 §3이 인스턴스화하는 계약.
- specs/04-memory.md §3.2-E — 저장 구조 규격(계약 수준)의 정본. 본 문서 §4가 인스턴스화하는 계약.
- specs/04-memory.md §3.2-B — scope 지정자(narrowing 차원)의 정본. 본 문서 §5의 해소 대상.
- specs/04-memory.md §3.3 INV-3·INV-4·INV-6·INV-7 — 전량 로드 금지·최소 Context 우선·기록 불변·인덱스 정합 불변 규칙. 본 문서가 준수·대조하는 불변.
- specs/04-memory.md §3.1-A·§3.1-B — Record / Recall 연산. 본 문서는 Store·Index가 이 연산에 참여하는 방식만 § 포인터로 참조한다(재정의 0).
- framework/core/structure.md §2 — 본 파일의 소속 경계(Module 구현 디렉터리 `framework/{loop,memory,verifier,workflow,plugins}/` 중 `framework/memory/`). 본 파일이 이 경계의 첫 실사용 인스턴스다(structure.md §2 주).
- framework/core/structure.md §5 — 금지 토큰 규칙(확정 조건 C-3 확장). 본 문서 본문 준수 대상.
- specs/00-glossary.md §3.2-J — Memory Item·Memory Store·Memory Index·Index Entry·Record·Recall 용어 정본(04 §9 Glossary 추가 요청 6건 승인 반영). 본 문서는 새 용어를 신설하지 않는다.

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다. 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 비의존을 유지한다(structure.md §5, C-3 확장). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. Memory Store 구조·포맷과 Memory 인덱스 규격을 04 §3.2-A·§3.2-C·§3.2-E·§3.2-B와 INV-3·INV-4·INV-6·INV-7의 인스턴스로 확정. Memory Item 스키마 인스턴스(§2, 6필드·필수/선택 표기 보존), Memory Index / Index Entry 규격(§3), Store 계약 구조(§4, append-only·정합 갱신·전량 로드 금지·물리 실현 포인터화), scope 해소 대응 표(§5), 경계·비의존(§6). 04 계약 재정의 0, Glossary 밖 새 용어 0, 물리 실현 서술 0(Adapter Binding 소관 포인터). | Worker (Advisor 위임, Task M3) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/04-memory.md §3이다.** 이 문서는 그 Core Contract의 **인스턴스**이며, 계약을 재정의·확장하지 않는다. 계약 요소는 § 포인터로만 참조한다(structure.md §7 C-1과 같은 인스턴스 원칙).
- 이 문서는 `framework/memory/` 아래 **Memory Store 구조·포맷과 Memory 인덱스 규격**을 확정한다. 04 §3.2-A(Memory Item)·§3.2-C(Memory Index / Index Entry)·§3.2-E(저장 구조 규격)·§3.2-B(scope)의 계약을 이 경계 위에 배치·대조한다.
- **이 문서는 Module 구현 디렉터리 문서다.** `framework/memory/`는 structure.md §2가 지정한 Module 구현 디렉터리 경계이며, structure.md §2 주에 따라 v0.4에서 **이 경계의 첫 실사용 인스턴스**가 된다. 그 문서 본문은 특정 AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명을 두지 않는다(structure.md §5 C-3 확장, 04 §3.3 INV-8).
- **물리 실현 비서술(경계).** Memory Store·Memory Index의 물리 형식·경로·직렬화·백엔드 I/O는 이 문서가 서술하지 않는다. 이는 **Adapter Binding 문서 소관**이다(04 §4 Adapter Binding — §4.1 환경 바인딩·§4.2 이식 교체 지점; 물리 격리 경계는 `framework/adapters/<adapter>/`, structure.md §2·§6). 필요한 자리에는 소관 포인터만 둔다.
- **kind·content 불투명 경계(INV-5).** Memory는 `kind`와 `content`를 불투명하게 다룬다. kind별 값·content 상세 스키마·생성 규칙은 특화 계약(Lessons, Best Practice) 소관이며 specs/05-lessons.md가 소유한다. 본 문서는 그 내부를 인용·추측하지 않고 § 포인터로만 참조한다(04 §3.3 INV-5).
- **동시 작성 형제 문서 경계(07 R2).** 같은 v0.4 Wave에서 동시 작성 중인 형제 문서(Memory Service Interface 계약 인스턴스, Lessons 인스턴스)의 미완성 내용은 인용·추측하지 않는다. 이들과의 관계는 확정된 정본 spec(04 §3.1·§3.4 Port 계약, 05 Lessons 소관)을 통해서만 참조한다.
- 용어는 specs/00-glossary.md 정본(§3.2-J)만 사용한다. 새 용어를 신설하지 않는다.

---

## §1. 목적

`framework/memory/`의 이 규격은 세 가지를 확정한다.

- **Memory Store 구조·포맷** — 기억의 최소 기록 단위(Memory Item)의 스키마와, 그 저장 구조(Memory Store)의 계약 수준 규칙(§2, §4).
- **Memory 인덱스 규격** — 회수 대상을 최소 Context로 찾는 조회 구조(Memory Index)와 그 경량 서술자(Index Entry)의 규격(§3).
- **scope 해소 대응** — 회수 범위 지정자(scope)의 narrowing 차원이 Index Entry의 어느 필드로 해소되는가(§5).

이 규격은 04 §3.2-A·§3.2-C·§3.2-E·§3.2-B Core Contract의 **인스턴스**다. 계약 요소(필드·연산·불변 규칙)를 재정의·확장하지 않는다. 형태 A(문서)에서 형태 B(실행 코드)로 전환되어도 04 §3 Core Contract 변경은 0이며, 위반이 발견되면 구현하지 않고 Advisor에게 보고한다(structure.md §7 C-1과 같은 불변 원칙).

---

## §2. Memory Item 스키마 인스턴스 (정본: 04 §3.2-A)

Memory Item은 기억의 최소 기록 단위다. 아래 필드·의미·필수 표기는 04 §3.2-A 정본을 **그대로 보존**한다(재정의 0). 필드명뿐 아니라 필수/선택 속성 표기까지 정본과 일치시킨다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Memory Item 고유 식별자. 안정적(stable)이며 회수·참조의 기준이 된다. Record 시 유일하게 할당된다. | 예(Record가 할당) |
| `kind` | 기억의 종류(분류자). 특화 계약이 자신의 kind 값을 정의한다. Memory는 `kind`를 불투명(opaque) 분류자로만 취급한다 (INV-5). | 예 |
| `content` | 기억 내용(payload). `kind`별 상세 스키마는 특화 계약 소관이다. Memory는 `content`를 불투명 페이로드로 다룬다 (INV-5). | 예 |
| `source` | 출처. 이 기억을 생성한 주체·작업·사이클 참조. | 예 |
| `timestamp` | 기록 시점. | 예 |
| `labels` | 회수 범위 해소용 태그 집합. Memory Index가 scope 해소에 사용한다. | 아니오 |

- `id`를 제외한 필수 필드(kind / content / source / timestamp)는 Record 입력에 모두 포함되어야 한다. `id`는 Record가 유일하게 할당한다(04 §3.1-A). `labels`는 선택이며, 있을 때 Memory Index의 scope 해소(§5)에 쓰인다.
- `kind`와 `content`의 내부 의미는 Memory가 해석하지 않는다(INV-5). kind별 값과 content 상세 스키마는 05 소관이다 — 본 문서는 그 상세를 인용·추측하지 않는다(§0 경계).
- 필드의 상세 정본은 04 §3.2-A가 유지한다. 본 표는 그 스키마를 인스턴스화할 뿐 계약을 재정의하지 않는다.

---

## §3. Memory Index / Index Entry 규격 (정본: 04 §3.2-C)

### §3.1 Memory Index

Memory Index는 회수 대상을 최소 Context로 찾기 위한 조회 구조다. scope 지정자(`kind` / `labels` / `timeRange` / `source`)를 Index Entry 집합으로 해소한다. Memory Store 전체를 스캔·로드하지 않고 후보를 찾게 하는 것이 목적이다(04 §3.2-C, INV-3).

### §3.2 Index Entry — 경량 서술자

아래 필드·의미는 04 §3.2-C 정본을 그대로 보존한다(재정의 0).

| 필드 | 의미 |
|---|---|
| `id` | 대응 Memory Item의 `id`. |
| `kind` | 분류자. scope의 `kind` 차원 해소. |
| `source` | 출처. |
| `timestamp` | 시점. scope의 `timeRange` 차원 해소. |
| `labels` | 범위 태그. scope의 `labels` 차원 해소. |
| `digest` | 짧은 서술(선택). Record 시 caller가 제공한다. `content` 원문을 담지 않는다. |

- **Index Entry는 `content` 원문을 담지 않는다(INV-4).** 기본 회수는 Index Entry(참조)만 반환하며, `content` 원문은 `detail = full`이 명시되고 scope로 한정된 경우에만 materialize된다(04 §3.1-B·§3.3 INV-4). `digest`도 짧은 서술일 뿐 `content` 원문이 아니다.
- **모든 Memory Item은 대응하는 Index Entry를 가진다(INV-7).** Record가 Memory Item 기록과 Index Entry 생성을 함께 완료한다(04 §3.1-A 완료 조건, §4의 정합 갱신).
- 필드의 상세 정본은 04 §3.2-C가 유지한다. 본 표는 그 규격을 인스턴스화할 뿐 계약을 재정의하지 않는다.

---

## §4. Memory Store 계약 구조 (정본: 04 §3.2-E)

Memory Store는 Memory Item의 저장 구조다. Record가 쓰고, Recall이 (Index를 거쳐) 읽는다. 아래는 04 §3.2-E 저장 구조 규격(계약 수준)의 인스턴스이며, 물리 실현은 서술하지 않는다.

### §4.1 계약 수준 규칙

- **append-only — 기록 불변(INV-6).** 기록된 Memory Item은 불변이다. Record는 추가만 한다. 갱신·정정은 기존 Item을 바꾸지 않고 **새 Memory Item 기록**으로 표현한다. `source`와 `timestamp`는 이 불변성 위에서 의미를 가진다(04 §3.3 INV-6).
- **Store + Index 정합 갱신(INV-7).** Record는 Memory Store 기록과 Memory Index의 Index Entry 생성을 **함께** 완료한다. 모든 Memory Item은 대응 Index Entry를 가지며(INV-7, §3.2), 불일치는 `IndexInconsistent` 위반이다(04 §3.1-A, §3.3 INV-7).
- **전량 로드 금지(INV-3).** Memory Store 전체를 반환하는 연산은 없다. Recall은 Memory Index로 scope를 해소해 후보를 찾은 뒤 scope로 한정된 대상만 읽는다. bounded가 아닌(전체 store를 겨냥하는) scope는 `UnboundedScope`로 거부된다(04 §3.1-B·§3.3 INV-3).
- **단일 Port 노출.** Memory Store와 Memory Index는 하나의 영속성 백엔드 뒤에 있으며, 소비자에게는 Memory Service Interface(단일 Port)를 통해서만 노출된다(04 §3.2-E, §3.4, INV-1). 소비자는 백엔드에 직접 접근하지 않는다.

### §4.2 물리 실현 경계 (Adapter Binding 소관 포인터)

- Memory Store·Memory Index의 **물리 형식·경로·직렬화·백엔드 I/O 메커니즘**은 이 문서가 서술하지 않는다. Core Contract는 영속성 백엔드 종류에 무관하다(04 §3.3 INV-8).
- 이 물리 실현은 전부 **Adapter Binding 문서 소관**이며 `framework/adapters/<adapter>/` 뒤로 격리된다(04 §4.1 — Memory Item 직렬화·Memory Store 물리 저장·Memory Index 물리 구현·백엔드 격리; §4.2 이식 교체 지점; structure.md §2·§6 Adapter 경계). 이식 시 §3의 Port 시그니처·회수 정책·추상 스키마·인덱스 계약·불변은 유지되고 물리 실현만 교체된다(04 §4.2).

---

## §5. scope 해소 규칙 대응 (정본: 04 §3.2-B / §3.2-C)

Recall Request의 `scope`는 narrowing 차원(`kind` / `labels` / `timeRange` / `source`) 중 최소 하나 또는 finite `limit`을 가져야 한다(04 §3.2-B). Memory Index는 이 scope 지정자를 Index Entry 집합으로 해소한다(04 §3.2-C). 각 narrowing 차원이 해소되는 Index Entry 필드는 다음과 같다.

| scope narrowing 차원 (04 §3.2-B) | 해소하는 Index Entry 필드 (04 §3.2-C) | 근거 |
|---|---|---|
| `kind` | Index Entry `kind` | 04 §3.2-C: "분류자. scope의 `kind` 차원 해소." |
| `labels` | Index Entry `labels` | 04 §3.2-C: "범위 태그. scope의 `labels` 차원 해소." |
| `timeRange` | Index Entry `timestamp` | 04 §3.2-C: "시점. scope의 `timeRange` 차원 해소." |
| `source` | Index Entry `source` | 04 §3.2-C Memory Index: scope 지정자(kind/labels/timeRange/source)를 Index Entry 집합으로 해소하며, `source` 차원은 Index Entry `source` 필드로 해소된다. |

- 위 대응은 04 §3.2-B/C를 **인용**한 것이며 재정의가 아니다. 각 차원의 정본은 04 §3.2-B(scope), 각 필드의 정본은 04 §3.2-C(Index Entry)가 유지한다.
- scope가 어느 차원도 갖지 않고 finite `limit`도 없으면(전체 store를 겨냥하면) `UnboundedScope`로 거부된다(04 §3.3 INV-3). scope 해소가 인덱스에서 부합 항목을 찾지 못하면 `ScopeUnresolvable`이다(04 §3.1-B).
- scope narrowing taxonomy(이 4차원)의 추가·변경 여부는 04 §9-OQ-M3·결정 기록 소관이다(04에서 v0.1 4차원 수용 확정). 본 문서는 이를 변경하지 않는다.

---

## §6. 경계와 비의존 (Core/Binding 분리 · 재정의 0 · 05·07 경계)

본 문서가 준수하는 경계를 한자리에 모은다. 검증 대조 지점이다.

- **04 계약 재정의·확장 0.** §2~§5의 모든 필드·연산·불변 규칙은 04 §3의 인스턴스이며 § 포인터로만 참조한다. 스키마 표는 정본을 그대로 보존(재정의 0)한다. 위반(형태 B가 04 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다.
- **05 경계(INV-5).** kind별 content 상세 스키마·Lesson/Best Practice 생성 규칙은 인용·추측하지 않는다. Memory는 `kind`·`content`를 불투명하게 다루고, 상세는 05 소관 § 포인터로만 처리한다.
- **07 R2 경계.** 같은 v0.4 Wave에서 동시 작성 중인 형제 문서의 미완성 내용은 인용·추측하지 않는다. 확정된 정본(04 §3.1·§3.4, 05 소관)만 참조한다.
- **물리 실현 비서술.** Memory Store·Memory Index의 물리 형식·경로·직렬화·백엔드 I/O는 서술하지 않고 Adapter Binding 문서 소관 포인터로만 처리한다(§4.2).
- **금지 토큰 비의존(structure.md §5 C-3 확장, 04 INV-8).** 본 문서 본문에는 특정 AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명 토큰을 두지 않는다. 금지 토큰의 예시조차 본문에 나열하지 않는다 — 구체 인스턴스가 필요한 자리에는 일반형 표기(`<adapter>`)와 "Adapter Binding 문서 소관" 포인터만 둔다(mention/use 경계).
- **Glossary 정본.** 사용 용어는 전부 specs/00-glossary.md §3.2-J 정본이다. 새 용어를 신설하지 않는다.

---

## §7. 요약 (규격 한눈에 보기)

- **Memory Item(§2)** — 6필드(`id` / `kind` / `content` / `source` / `timestamp` / `labels`). 04 §3.2-A 스키마 인스턴스, 필수/선택 표기 보존. `kind`·`content`는 불투명(INV-5).
- **Memory Index / Index Entry(§3)** — Index Entry 6필드(`id` / `kind` / `source` / `timestamp` / `labels` / `digest`). Index Entry는 `content` 원문을 담지 않는다(INV-4). 모든 Memory Item은 대응 Index Entry를 가진다(INV-7).
- **Memory Store(§4)** — append-only(INV-6, 갱신은 새 Item 기록), Record의 Store+Index 정합 갱신(INV-7), 전량 로드 금지(INV-3), 단일 Port 노출(INV-1). 물리 실현은 Adapter Binding 소관 포인터.
- **scope 해소(§5)** — `kind`→`kind`, `labels`→`labels`, `timeRange`→`timestamp`, `source`→`source`. bounded 강제(INV-3).
- **경계(§6)** — 04 재정의 0, 05·07 경계 준수, 물리 실현 비서술, Core 문서 본문 금지 토큰 0, Glossary 정본만 사용.
- 모든 규격은 04 §3의 인스턴스이며, 형태 A → 형태 B 전환에도 Core Contract 변경은 0이다.
