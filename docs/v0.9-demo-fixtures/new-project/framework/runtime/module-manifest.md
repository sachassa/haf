# framework/runtime/module-manifest — Module Manifest 포맷 규격

작성일: 2026-07-05
상태: v0.3 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-05)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드(`id`/`contract`/`version`/`requires`/`entrypoint`/`configSchema`/`replaceable`). 본 문서가 인스턴스화하는 계약의 정본. 필드명·의미·필수/선택 표기의 정본은 이 § 하나가 유지한다.
- specs/01-runtime.md §3.3 INV-7 — 안정 식별자 불변 규칙(`id`·`contract` id 안정성).
- specs/01-runtime.md §3.3 INV-1 — 교체 가능성(`replaceable` 기본값의 근거).
- specs/01-runtime.md §3.2-B — Config 계약(정본). `configSchema` 필드가 참조하는 계약. 본 문서는 § 포인터로만 참조한다.
- specs/01-runtime.md §4 — Adapter Binding(구체 직렬화·진입점 해소 소관). 본 문서는 § 포인터로만 참조하고 구체 바인딩 토큰을 재현하지 않는다.
- framework/core/structure.md §5 — 금지 토큰 규칙(확정 조건 C-3). §6 — 본 파일의 소속 경계 배정(`framework/runtime/`, 01 §3.2-A 인스턴스). §7 — Core Contract 불변 조건(확정 조건 C-1).
- ROADMAP.md v0.3 — 산출물 "Runtime 프로토콜 구현물"(일부).

거버넌스: 이 문서는 `framework/runtime/` 소속 Core 문서다. 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인 비의존을 유지한다 (framework/core/structure.md §5 확정 조건 C-3). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.3 Draft | 최초 작성. 01 §3.2-A Module Manifest 7필드 인스턴스화(필드명·의미·필수/선택 표기 정본 대조), 필드별 작성 지침(좋은/나쁜 예), INV-7 안정 식별자 규칙, 언어 중립 추상 스키마 시그니처(확정 조건 C-1). | Worker (Advisor 위임, Task A2) |
| 2026-07-05 | v0.3 Baseline | v0.3 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass, CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/01-runtime.md §3.2-A이다.** 이 문서는 그 Module Manifest 계약의 **인스턴스**이며, 필드·의미·필수/선택 표기를 **재정의·확장하지 않는다**. 필드 계약 요소는 01 §3.2-A를 § 포인터로만 참조한다 (framework/core/structure.md §7 확정 조건 C-1).
- 이 문서는 Module 등록 서술자(Module Manifest)를 이 프로젝트에서 **어떻게 작성·판독하는가**를 규율하는 규격이다. 계약 요소의 진위 판정 기준은 항상 01 §3.2-A다.
- **이 문서는 Core 문서다.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (framework/core/structure.md §5 C-3, 01 §3.3 INV-4). 구체 직렬화 형식·물리 진입점 해소·환경 경로 관례는 **Adapter Binding 문서 소관**이며 (01 §4), 필요한 자리에는 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Module / Module Manifest / 모듈 시스템 / Runtime Context는 Glossary §3.2-I가 정본이다. 새 용어를 정본처럼 신설하지 않는다.
- 필드명에 쓰는 백틱 표기(`id` 등)와 예시 식별자는 특정 언어·직렬화 형식의 문법이 아니라, 정본 01 §3.2-A가 쓰는 필드명·서술 라벨을 그대로 인용한 것이다.

---

## §1. 목적

Module Manifest는 Module의 **등록 서술자**다 (Glossary §3.2-I, 01 §3.2-A). Register 연산의 입력이자, Resolve·Replace가 의존하는 안정 기준의 원천이다 (등록·해소·교체 운용 규칙은 module-registry.md 소관).

이 규격의 책임은 세 가지다.

- 01 §3.2-A의 7필드를 **재정의 없이** 이 프로젝트의 작성 지침으로 인스턴스화한다 — 각 필드를 무엇으로 채우고 무엇을 피하는가.
- 교체·해소가 의존하는 **안정 식별자 규칙**(INV-7)을 작성 규범으로 전개한다.
- Manifest의 **언어 중립 추상 스키마 시그니처**를 제시하여, 실행 코드(향후 형태 B) 도입 시에도 01 §3.2-A 계약 변경이 0으로 유지됨을 보장한다 (C-1).

각 Module은 자기완결(self-contained) 단위이므로, Manifest는 그 Module의 `id`·`contract`·`entrypoint` 등 자기완결 참조를 한 서술자에 묶는다 (01 §3.2-E 규칙 2).

---

## §2. Module Manifest 7필드 (정본 대조 표)

아래 표는 01 §3.2-A의 7필드를 **정본과 일치하게** 옮긴 것이다. 필드명·의미·필수/선택 표기는 정본 그대로이며, 본 문서는 이를 재정의하지 않는다.

| 필드 | 의미 (정본: 01 §3.2-A) | 필수 |
|---|---|---|
| `id` | Module 고유 식별자. 안정적(stable)이어야 교체의 기준이 된다. | 예 |
| `contract` | 이 Module이 구현하는 계약(Port/Interface) 식별자. 교체는 동일 `contract` 내에서만 성립한다. | 예 |
| `version` | Module 버전. | 예 |
| `requires` | 의존하는 contract id 목록. Resolve 시 모두 해소되어야 한다. | 아니오(기본 없음) |
| `entrypoint` | 실행 진입점의 추상 참조. 구체 바인딩은 01 §4가 해소한다. | 예 |
| `configSchema` | 이 Module의 Config 스키마. | 아니오 |
| `replaceable` | 교체 가능 여부. 기본 `true` (ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 아니오(기본 true) |

주:

- **필수/선택 표기는 정본 그대로 보존한다.** `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 같은 속성 표기는 필드명과 함께 복제한다 — 이 표기가 누락되면 계약 변경으로 읽힌다.
- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true).
- 의미 열의 "구체 바인딩은 01 §4가 해소한다"는 정본의 "§4"를 소속 spec으로 명시한 것이다(01 §4 = Adapter Binding). 계약 변경이 아니라 § 포인터의 명시화다.
- 상세 필드 계약의 정본은 01 §3.2-A가 유지한다. 이 표는 인스턴스이며 진위 판정 기준이 아니다.

---

## §3. 필드별 작성 지침 (좋은/나쁜 예)

각 필드를 무엇으로 채우고 무엇을 피하는가. 예시 식별자는 전부 **일반형 예시**이며, 특정 AI·언어·툴체인·직렬화 형식·제품 기능 토큰을 담지 않는다 (§0, C-3).

### `id` (필수)

- 채우는 법: 역할·계약에 기반한 **안정 식별자**. 구현 세부(버전·환경·백엔드 종류)를 인코딩하지 않는다.
- 좋은 예: `dispatcher` — 구현이 여러 번 교체돼도 유지되는 안정 식별자. 교체의 기준이 된다 (INV-7).
- 나쁜 예: `dispatcher-fast-rev2` — 성능 특성·리비전을 id에 인코딩. 구현이 바뀔 때마다 id가 바뀌어 교체의 안정 기준(INV-7)이 무너진다.

### `contract` (필수)

- 채우는 법: 이 Module이 구현하는 **Port/Interface 계약** 식별자. 교체 후보 Module들이 공유하는 안정 식별자다.
- 좋은 예: `DispatchPort` — 여러 구현 Module이 공유하는 계약 식별자. 동일 `contract` 내에서만 교체가 성립한다 (INV-1).
- 나쁜 예: `DispatchPort-implA` — 특정 구현을 계약 식별자에 섞음. 계약과 구현이 1:1로 묶여 동일 contract 교체(INV-1)가 불가능해진다.

### `version` (필수)

- 채우는 법: 이 Module의 버전을 가리키는 **고정된 버전 문자열**. 같은 문자열은 항상 같은 Module 버전을 가리킨다.
- 좋은 예: `2.3.0` — 특정 시점의 Module 버전을 고정적으로 식별하는 버전 문자열.
- 나쁜 예: `latest` — 가리키는 대상이 시점에 따라 달라지는 비고정 라벨. 버전으로서 안정 참조가 되지 못한다.

### `requires` (선택 — 기본 없음)

- 채우는 법: 의존하는 **contract id** 목록. **module id가 아니라 contract id**를 나열한다. Resolve 시 모두 해소되어야 한다. 의존이 없으면 생략한다(기본 없음).
- 좋은 예: contract id `StorageContract`, `ClockContract`를 나열 — 계약에 의존하므로 그 계약의 활성 구현이 무엇으로 교체돼도 이 Module은 영향받지 않는다.
- 나쁜 예: 특정 module id(예: `storage-provider-alpha`)를 나열 — 구현 Module에 직접 의존하면 그 Module 교체가 이 Module의 참조를 깨어 교체 가능성(INV-1)을 훼손한다.

### `entrypoint` (필수)

- 채우는 법: Module 활성화 진입을 가리키는 **추상 참조**(논리적 진입점). 구체 바인딩(직렬화·물리 경로·호출 규약)은 기입하지 않는다.
- 좋은 예: 이 Module의 활성화 진입을 가리키는 논리적 진입점 참조. 구체 해소는 Adapter Binding 문서 소관이다 (01 §4).
- 나쁜 예: 특정 실행 환경의 물리 경로·형식별 로케이터를 Manifest에 직접 기입 — 환경 의존을 Core 서술자에 하드코딩하면 이식 시 서술자가 함께 바뀌어 AI/환경 비의존(INV-4)이 깨진다. 물리 바인딩은 Adapter로 격리한다.

### `configSchema` (선택)

- 채우는 법: 이 Module이 수용하는 설정의 **스키마 참조**. 자기 Module 네임스페이스에 국한된다. 설정을 받지 않으면 생략한다. Config 계약 정본은 01 §3.2-B다.
- 좋은 예: 이 Module의 설정만을 서술하는 스키마 참조. 없으면 생략(선택 필드).
- 나쁜 예: 다른 Module의 설정까지 이 스키마에 포함 — `configSchema`는 자기 Module 범위에 한정된다. 타 Module 설정은 그 Module의 `configSchema` 소관이다.

### `replaceable` (선택 — 기본 true)

- 채우는 법: 교체 가능 여부. 기본은 `true`이므로 보통 생략한다. `false`는 명시적 예외이며 근거를 요구한다.
- 좋은 예: 생략(= 기본 `true`). 모든 Module은 교체 가능이 기본이다 (INV-1, ARCHITECTURE 3.2).
- 나쁜 예: 근거 없이 `false` 지정 — `false`는 근거를 요구하는 명시적 예외다 (INV-1). 근거 없는 `false`는 Modular 원칙 위반이다.

---

## §4. 안정 식별자 규칙 (INV-7)

Module `id`와 `contract` id는 **안정적**이어야 한다. 교체(Replace)와 해소(Resolve)가 이 안정성에 의존한다 (01 §3.3 INV-7). 작성 규범으로 전개하면 다음과 같다.

1. **`id` 안정성.** 한 Module의 `id`는 구현이 바뀌어도 유지된다. `id`는 교체 전후를 잇는 기준이므로, 버전·환경·백엔드 종류 같은 가변 정보를 `id`에 인코딩하지 않는다 (§3 `id` 나쁜 예).
2. **`contract` id 안정성.** `contract` id는 교체 후보 Module들이 공유하는 계약 식별자다. 계약이 안정적이어야 "동일 `contract` 내 교체"(INV-1)가 성립하고, 계약 소비자의 참조가 변경 0으로 유지된다.
3. **가변 정보의 분리.** 버전은 `version` 필드가, 구현 선택·환경 바인딩은 Registry의 활성 바인딩(운용 규칙은 module-registry.md 소관)과 Adapter Binding(01 §4)이 담당한다. 이 가변 정보들이 안정 식별자(`id`·`contract`)에 새어 들어가지 않게 한다.
4. **안정성 위반의 신호.** 교체 때마다 `id`나 `contract`를 바꿔야 성립하는 설계는 안정 식별자 규칙 위반이다. 이 경우 추측으로 우회하지 않고 Advisor에게 보고한다 (상위 규약 — 추측 금지, 계약 충돌 보고).

---

## §5. 언어 중립 추상 스키마 시그니처 (C-1)

Manifest 7필드의 **타입 수준** 서술이다. 특정 언어의 타입 표기법·문법을 쓰지 않고, 언어 중립 서술어(식별자 / 식별자 목록 / 버전 문자열 / 추상 참조 / 불리언)로만 표현한다.

| 필드 | 타입 수준 서술 | 필수/선택 |
|---|---|---|
| `id` | 식별자 | 필수 |
| `contract` | 식별자 | 필수 |
| `version` | 버전 문자열 | 필수 |
| `requires` | 식별자 목록 (원소는 contract id) | 선택 (기본 없음) |
| `entrypoint` | 추상 참조 | 필수 |
| `configSchema` | 추상 참조 (Config 스키마 참조) | 선택 |
| `replaceable` | 불리언 | 선택 (기본 참 — 정본 표기 `true`) |

서술어 정의(언어 중립):

- **식별자** — 안정적으로 대상 하나를 가리키는 이름. 물리 표현·인코딩은 규정하지 않는다.
- **식별자 목록** — 식별자 0개 이상의 순서 없는 모음.
- **버전 문자열** — 특정 Module 버전을 고정적으로 가리키는 문자열.
- **추상 참조** — 대상(진입점·스키마)을 가리키되 물리 해소는 미루는 논리 참조. 구체 해소는 Adapter Binding 소관이다 (01 §4).
- **불리언** — 참/거짓 두 값.

**C-1 명시.** 이 시그니처는 01 §3.2-A Module Manifest의 **인스턴스**이며 계약의 **확장·수정이 아니다** (framework/core/structure.md §7 확정 조건 C-1). 실행 코드(형태 B) 도입 시 이 시그니처를 구현하더라도 01 §3.2-A 계약 요소(필드·의미·필수/선택)는 변경 0으로 유지된다. 위반(형태 B가 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현을 진행하지 않고 Advisor에게 보고한다 (structure.md §7 규칙 4).

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- 본 문서의 모든 필드 계약은 01 §3.2-A의 인스턴스다. 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A다 (C-1).
- 본문·표·예시 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명이 0건이다. 필드 값의 물리 표현(직렬화·진입점 해소)이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관 (01 §4)" 포인터를 둔다 (mention/use 경계 — 금지 토큰의 예시도 Core 문서에서는 누출이다).
- §3의 예시 식별자(`dispatcher`, `DispatchPort`, `StorageContract` 등)는 일반형 예시일 뿐, 특정 제품·환경·구현을 명명하지 않는다.

---

## §7. 요약 (한눈에 보기)

- Module Manifest = Module의 등록 서술자. 정본 = 01 §3.2-A (본 문서는 인스턴스, 재정의 아님 — C-1).
- 7필드: `id`(식별자, 필수) · `contract`(식별자, 필수) · `version`(버전 문자열, 필수) · `requires`(식별자 목록, 선택·기본 없음) · `entrypoint`(추상 참조, 필수) · `configSchema`(추상 참조, 선택) · `replaceable`(불리언, 선택·기본 true).
- 안정 식별자 규칙(INV-7): `id`·`contract`는 교체·해소의 기준이므로 가변 정보를 인코딩하지 않는다.
- 언어 중립 시그니처는 실행 코드 도입 후에도 01 §3.2-A 계약 변경 0을 보장한다 (C-1).
- 구체 직렬화·물리 진입점·환경 경로는 Adapter Binding 문서 소관 (01 §4). Core 문서 본문에는 그 토큰이 0건이다 (C-3).
