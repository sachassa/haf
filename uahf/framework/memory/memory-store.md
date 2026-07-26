# framework/memory/memory-store — UAHF Memory Store 구조·포맷 + Memory 인덱스 규격

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/04-memory.md §3.2-A — Memory Item 스키마의 정본(§2).
- specs/04-memory.md §3.2-C — Memory Index / Index Entry 규격의 정본(§3).
- specs/04-memory.md §3.2-E — 저장 구조 규격(계약 수준)의 정본(§4).
- specs/04-memory.md §3.2-B — scope 지정자(narrowing 차원)의 정본(§5).
- specs/04-memory.md §3.3 INV-3·INV-4·INV-6·INV-7 — 준수·대조 불변.
- specs/04-memory.md §3.1-A·§3.1-B — Record / Recall 연산(참여 방식만 § 포인터, 재정의 0).
- framework/core/structure.md §2·§5 — 소속 경계(`framework/memory/`)·금지 토큰 규칙(C-3 확장).
- specs/00-glossary.md §3.2-J — 용어 정본(04 §9 Glossary 추가 요청 6건 승인 반영).

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다. 본문은 AI·언어·툴체인·직렬화 형식 비의존을 유지한다(structure.md §5 C-3). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(§6은 이 절을 가리키는 포인터일 뿐 반복하지 않는다).

- **정본은 specs/04-memory.md §3이다.** 이 문서는 그 Core Contract의 **인스턴스**이며 계약을 재정의·확장하지 않는다(structure.md §7 C-1). 위반(형태 B가 04 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다.
- 이 문서는 `framework/memory/` 아래 **Memory Store 구조·포맷과 Memory 인덱스 규격**을 확정한다 — 04 §3.2-A/§3.2-C/§3.2-E/§3.2-B의 계약을 이 경계 위에 배치·대조한다.
- **Module 구현 디렉터리 문서.** `framework/memory/`는 structure.md §2가 지정한 경계이며 v0.4에서 그 경계의 첫 실사용 인스턴스가 되었다. 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명)을 두지 않는다 — 규칙·분류 정본은 structure.md §5 C-3(및 04 §3.3 INV-8)이다. 작성 시점의 동시 작성 형제 불인용(07 R2)·추측 0(07 R4) 준수 서술 = 종전 문면 git 앵커 90ca19c(정본 = uahf/specs/07-workflow.md §3.2-C).
- **물리 실현 비서술.** Memory Store·Memory Index의 물리 형식·경로·직렬화·백엔드 I/O는 서술하지 않는다 — Adapter Binding 문서 소관이다(04 §4.1·§4.2; 격리 경계 `framework/adapters/<adapter>/`, structure.md §2·§6). 상세는 §4.2.
- **kind·content 불투명 경계(INV-5).** kind별 값·content 상세 스키마·생성 규칙은 특화 계약(Lessons, Best Practice) 소관이며 specs/05-lessons.md가 소유한다 — 내부를 인용·추측하지 않고 § 포인터로만 참조한다.
- 용어는 specs/00-glossary.md §3.2-J 정본만 사용한다. 새 용어를 신설하지 않는다.

---

## §1. 목적

`framework/memory/`의 이 규격은 세 가지를 확정한다 — Memory Item 스키마와 Memory Store 계약 구조(§2·§4) · Memory Index / Index Entry 규격(§3) · scope narrowing 차원의 해소 대응(§5). 형태 A(문서) → 형태 B(실행 코드) 전환에도 04 §3 Core Contract 변경은 0이다.

---

## §2. Memory Item 스키마 인스턴스

정본 = `uahf/specs/04-memory.md §3.2-A`(재정의 0 · 필드 의미·필수 표기는 정본 문면 보존). Memory Item은 기억의 최소 기록 단위다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Memory Item 고유 식별자. 안정적(stable)이며 회수·참조의 기준이 된다. Record 시 유일하게 할당된다. | 예(Record가 할당) |
| `kind` | 기억의 종류(분류자). 특화 계약이 자신의 kind 값을 정의한다. Memory는 `kind`를 불투명(opaque) 분류자로만 취급한다 (INV-5). | 예 |
| `content` | 기억 내용(payload). `kind`별 상세 스키마는 특화 계약 소관이다. Memory는 `content`를 불투명 페이로드로 다룬다 (INV-5). | 예 |
| `source` | 출처. 이 기억을 생성한 주체·작업·사이클 참조. | 예 |
| `timestamp` | 기록 시점. | 예 |
| `labels` | 회수 범위 해소용 태그 집합. Memory Index가 scope 해소에 사용한다. | 아니오 |

- `id`를 제외한 필수 필드(kind / content / source / timestamp)는 Record 입력에 모두 포함되어야 하며, `id`는 Record가 유일하게 할당한다(04 §3.1-A). `labels`는 선택이며 있을 때 scope 해소(§5)에 쓰인다.
- `kind`·`content`의 내부 의미는 Memory가 해석하지 않는다(INV-5) — 상세는 05 소관이다(§0).

---

## §3. Memory Index / Index Entry 규격

정본 = `uahf/specs/04-memory.md §3.2-C`(재정의 0 · 필드 의미는 정본 문면 보존).

### §3.1 Memory Index

Memory Index는 회수 대상을 최소 Context로 찾기 위한 조회 구조다. scope 지정자(`kind` / `labels` / `timeRange` / `source`)를 Index Entry 집합으로 해소하며, Memory Store 전체를 스캔·로드하지 않고 후보를 찾게 하는 것이 목적이다(04 §3.2-C, INV-3).

### §3.2 Index Entry — 경량 서술자

| 필드 | 의미 |
|---|---|
| `id` | 대응 Memory Item의 `id`. |
| `kind` | 분류자. scope의 `kind` 차원 해소. |
| `source` | 출처. |
| `timestamp` | 시점. scope의 `timeRange` 차원 해소. |
| `labels` | 범위 태그. scope의 `labels` 차원 해소. |
| `digest` | 짧은 서술(선택). Record 시 caller가 제공한다. `content` 원문을 담지 않는다. |

- **Index Entry는 `content` 원문을 담지 않는다(INV-4).** 기본 회수는 Index Entry(참조)만 반환하며, `content` 원문은 `detail = full`이 명시되고 scope로 한정된 경우에만 materialize된다(04 §3.1-B·INV-4). `digest`도 짧은 서술일 뿐 원문이 아니다.
- **모든 Memory Item은 대응하는 Index Entry를 가진다(INV-7).** Record가 Item 기록과 Index Entry 생성을 함께 완료한다(04 §3.1-A 완료 조건, §4).

---

## §4. Memory Store 계약 구조 (정본: 04 §3.2-E)

Memory Store는 Memory Item의 저장 구조다. Record가 쓰고, Recall이 (Index를 거쳐) 읽는다.

### §4.1 계약 수준 규칙

- **append-only — 기록 불변(INV-6).** 기록된 Memory Item은 불변이다. Record는 추가만 한다. 갱신·정정은 기존 Item을 바꾸지 않고 **새 Memory Item 기록**으로 표현한다. `source`와 `timestamp`는 이 불변성 위에서 의미를 가진다.
- **Store + Index 정합 갱신(INV-7).** Record는 Memory Store 기록과 Index Entry 생성을 **함께** 완료한다. 불일치는 `IndexInconsistent` 위반이다(04 §3.1-A).
- **전량 로드 금지(INV-3).** Memory Store 전체를 반환하는 연산은 없다. Recall은 Memory Index로 scope를 해소한 뒤 한정된 대상만 읽으며, bounded가 아닌 scope는 `UnboundedScope`로 거부된다(04 §3.1-B).
- **단일 Port 노출.** Memory Store와 Memory Index는 하나의 영속성 백엔드 뒤에 있으며 소비자에게는 Memory Service Interface(단일 Port)를 통해서만 노출된다(04 §3.2-E·§3.4, INV-1).

### §4.2 물리 실현 경계 (Adapter Binding 소관 포인터)

- Memory Store·Memory Index의 물리 형식·경로·직렬화·백엔드 I/O 메커니즘은 이 문서가 서술하지 않는다 — Core Contract는 영속성 백엔드 종류에 무관하다(04 INV-8).
- 이 물리 실현은 전부 Adapter Binding 문서 소관이며 `framework/adapters/<adapter>/` 뒤로 격리된다(04 §4.1 — Memory Item 직렬화·Store 물리 저장·Index 물리 구현·백엔드 격리; §4.2 이식 교체 지점). 이식 시 §2~§5의 추상 스키마·인덱스 계약·불변은 유지되고 물리 실현만 교체된다.

---

## §5. scope 해소 규칙 대응 (정본: 04 §3.2-B / §3.2-C)

Recall Request의 `scope`는 narrowing 차원(`kind` / `labels` / `timeRange` / `source`) 중 최소 하나 또는 finite `limit`을 가져야 하며(04 §3.2-B), Memory Index가 이를 Index Entry 집합으로 해소한다(04 §3.2-C).

| scope narrowing 차원 (04 §3.2-B) | 해소하는 Index Entry 필드 (04 §3.2-C) |
|---|---|
| `kind` | Index Entry `kind` |
| `labels` | Index Entry `labels` |
| `timeRange` | Index Entry `timestamp` |
| `source` | Index Entry `source` |

- 위 대응은 04 §3.2-B/C의 인용이며 재정의가 아니다 — 각 차원의 정본은 04 §3.2-B, 각 필드의 정본은 04 §3.2-C가 유지한다.
- scope가 어느 차원도 갖지 않고 finite `limit`도 없으면 `UnboundedScope`로 거부되고(INV-3), 인덱스에서 부합 항목을 찾지 못하면 `ScopeUnresolvable`이다(04 §3.1-B).
- scope narrowing taxonomy(이 4차원)의 추가·변경 여부는 04 §9-OQ-M3·결정 기록 소관이다(04에서 v0.1 4차원 수용 확정). 본 문서는 이를 변경하지 않는다.

---

## §6. 경계와 비의존

경계 선언 정본은 §0이다(04 재정의·확장 0 · 05 kind/content 불투명 경계 · 물리 실현 비서술 · 금지 토큰 규칙 = structure.md §5 C-3 · 07 R2·R4 = uahf/specs/07-workflow.md §3.2-C · Glossary 정본 = uahf/specs/00-glossary.md §3.2-J).
