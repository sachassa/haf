# framework/runtime/module-registry — 모듈 등록/해소/교체/해제 규칙

작성일: 2026-07-05
상태: v0.3 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-05)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.1-A — Module 시스템 4연산(Register / Resolve / Replace / Deregister). 각 연산의 입력·출력·완료 조건·실패 보고의 정본. 본 문서가 인스턴스화하는 계약이다.
- specs/01-runtime.md §3.2-C — Runtime Context의 `registry` 필드(contract id → 활성 module id 바인딩과 등록된 Manifest 집합). 본 문서는 § 포인터로만 참조한다.
- specs/01-runtime.md §3.2-D — Failure Report 공통 구조(`operation`/`target`/`reason`/`location`). 본 문서는 구조를 재정의하지 않고 § 포인터로만 참조하며, reason 코드 목록만 연산별로 전개한다.
- specs/01-runtime.md §3.3 INV-1(교체 가능)·INV-3(계약당 단일 바인딩)·INV-7(안정 식별자). 등록/교체 절차 규칙의 근거.
- specs/01-runtime.md §8 예1 — 동일 contract 교체(백엔드 스왑) 예시. 본 문서는 § 포인터로만 참조하고 구체 예시 토큰을 재현하지 않는다.
- specs/01-runtime.md §3.2-A — Register/Replace의 입력인 Module Manifest. 필드 정본이자, 자매 문서 framework/runtime/module-manifest.md가 인스턴스화하는 계약. 본 문서는 § 포인터로만 참조한다.
- framework/core/structure.md §5 — 금지 토큰 규칙(확정 조건 C-3). §6 — 본 파일의 소속 경계 배정(`framework/runtime/`). §7 — Core Contract 불변 조건(확정 조건 C-1).
- ROADMAP.md v0.3 — 산출물 "모듈 등록/교체 규칙 문서".

거버넌스: 이 문서는 `framework/runtime/` 소속 Core 문서다. 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인 비의존을 유지한다 (framework/core/structure.md §5 확정 조건 C-3). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.3 Draft | 최초 작성. 01 §3.1-A 4연산(Register/Resolve/Replace/Deregister)을 입력·출력·완료 조건·실패 reason으로 운용 규칙 전개, 등록/교체/해제 절차 규칙(INV-1·INV-3, 소비자 참조 변경 0 확인, DependentExists 거부), 4연산 언어 중립 시그니처(C-1), 연산별 reason 코드 목록. | Worker (Advisor 위임, Task A2) |
| 2026-07-05 | v0.3 Baseline | v0.3 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass, CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/01-runtime.md §3.1-A(4연산)와 §3.2-C(registry)·§3.2-D(Failure Report)이다.** 이 문서는 그 Module 시스템 계약의 **인스턴스**이며, 연산의 입력·출력·완료 조건·실패 구조를 **재정의·확장하지 않는다**. 계약 요소는 01의 해당 §를 § 포인터로 참조한다 (framework/core/structure.md §7 확정 조건 C-1).
- 이 문서는 Registry(등록부)의 4연산을 이 프로젝트에서 **어떻게 운용하는가**를 규율하는 규칙 문서다. 연산의 진위 판정 기준은 항상 01 §3.1-A다.
- **이 문서는 Core 문서다.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (framework/core/structure.md §5 C-3, 01 §3.3 INV-4). 구체 등록·활성화의 물리 실현은 Adapter Binding 문서 소관이며 (01 §4), 필요한 자리에는 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Module / Module System / Module Manifest / Runtime Context는 Glossary §3.2-I가 정본이다. 새 용어를 정본처럼 신설하지 않는다.
- Registry가 무엇을 담는지(contract id → 활성 module id 바인딩, 등록된 Manifest 집합)는 01 §3.2-C `registry` 필드가 정본이다. 본 문서는 그 구조를 재정의하지 않고, 그 위에서 4연산이 어떻게 작동하는가만 규율한다.

---

## §1. 목적

Registry는 Module의 **정의·등록·해소·교체 규칙의 총체**(Module System, Glossary §3.2-I)를 담는 등록부다. Runtime Component가 관장한다 (01 §3.1-A).

이 규격의 책임은 세 가지다.

- 01 §3.1-A의 4연산(Register/Resolve/Replace/Deregister)을 **재정의 없이** 이 프로젝트의 운용 규칙으로 전개한다 — 각 연산의 입력·출력·완료 조건·실패 reason.
- 등록·교체·해제의 **절차 규칙**을 명문화한다 — 동일 contract 내 교체(INV-1), 계약당 활성 바인딩 정확히 1(INV-3), 소비자 참조 변경 0 확인, 의존 존재 시 해제 거부(DependentExists).
- 4연산의 **언어 중립 시그니처**를 제시하여, 실행 코드(향후 형태 B) 도입 시에도 01 §3.1-A 계약 변경이 0으로 유지됨을 보장한다 (C-1).

Register/Replace의 입력인 Module Manifest의 필드 계약은 자매 문서 framework/runtime/module-manifest.md가 01 §3.2-A를 인스턴스화한다. 본 문서는 그 계약을 소비하며 재정의하지 않는다.

---

## §2. 4연산 운용 규칙

각 연산의 입력·출력·완료 조건·실패 reason은 01 §3.1-A와 **일치**한다. 아래는 그 계약을 운용 규칙으로 전개한 것이다. 실패 보고의 공통 구조(`operation`/`target`/`reason`/`location`)는 01 §3.2-D가 정본이며 여기서 재정의하지 않는다 (연산별 reason 코드는 §5 참조).

### 2.1 Register — 등록

- **입력.** Module Manifest 1건 (필드 계약: 01 §3.2-A / 작성 지침: module-manifest.md).
- **출력.** 등록 결과 — 등록된 module id.
- **완료 조건.** Manifest가 Module Interface 계약을 만족하고, `id`가 Registry에서 유일하다.
- **운용 규칙.**
  1. 입력 Manifest의 필수 필드(`id`·`contract`·`version`·`entrypoint`)를 확인한다. 계약 불만족이면 등록하지 않는다.
  2. `id`가 Registry에 이미 존재하면 등록하지 않는다 (유일성). 안정 식별자 규칙(INV-7)에 따라 `id`는 재사용·충돌이 없어야 한다.
  3. 등록은 Manifest를 Registry의 등록된 Manifest 집합에 넣는 것까지다. 활성 바인딩 성립 여부는 Resolve(§2.2)가 판정한다.
- **실패 reason.** `ContractMismatch`(Module Interface 계약 불만족) | `DuplicateId`(`id`가 Registry에서 유일하지 않음).

### 2.2 Resolve — 해소

- **입력.** contract id (또는 module id).
- **출력.** 해당 계약의 활성 Module 핸들 — **정확히 1개**.
- **완료 조건.** 대상 계약에 활성 바인딩이 정확히 하나 존재하고, 그 `requires`가 모두 해소된다.
- **운용 규칙.**
  1. 대상 contract의 활성 바인딩이 0개면 해소 실패(`UnresolvedContract`).
  2. 대상 contract의 활성 바인딩이 2개 이상이면 INV-3(계약당 단일 바인딩) 위반이므로 해소 실패(`DuplicateBinding`). Resolve는 항상 유일한 핸들을 반환해야 한다.
  3. 대상 Module의 `requires`(의존 contract id 목록)를 재귀적으로 해소한다. 의존 그래프에 순환이 있으면 해소 실패(`DependencyCycle`).
- **실패 reason.** `UnresolvedContract`(활성 바인딩 없음) | `DuplicateBinding`(활성 바인딩 2개 이상, INV-3 위반) | `DependencyCycle`(requires 의존 순환).

### 2.3 Replace — 교체

- **입력.** 대상 contract id + 새 Module Manifest.
- **출력.** 교체 결과 — 이전 module id → 새 module id.
- **완료 조건.** 새 Module이 **동일 contract**를 만족하며 활성화되고, 이전 Module이 비활성화되며, **계약 소비자의 참조는 변경되지 않는다**.
- **운용 규칙.**
  1. 새 Manifest의 `contract`가 대상 contract와 **동일**한지 확인한다. 다르면 교체하지 않는다 (`ContractMismatch`) — 교체는 동일 contract 내에서만 성립한다 (INV-1).
  2. 대상의 현재 활성 Module이 `replaceable=false`이면 교체를 거부한다 (`NotReplaceable`). `false`는 명시적 예외이며 근거를 요구한다 (INV-1, module-manifest.md §3 `replaceable`).
  3. 새 Module을 활성화하고 이전 Module을 비활성화(Deactivate)한다. contract id가 동일하므로 계약 소비자의 참조(해당 contract에 대한 Resolve 경로)는 그대로 유지된다 — 소비자 코드·규격 변경 0 (INV-1).
  4. 교체 후 Resolve(대상 contract)는 새 Module 핸들을 반환한다. (동일 contract 백엔드 스왑의 계약 흐름 예시는 01 §8 예1 참조 — 본 문서는 구체 토큰을 재현하지 않는다.)
- **실패 reason.** `ContractMismatch`(새 Module이 동일 contract를 만족하지 않음) | `NotReplaceable`(대상이 교체 불가).

### 2.4 Deregister — 등록 해제

- **입력.** 대상 module id.
- **출력.** 등록 해제 결과 — 해제된 module id.
- **완료 조건.** 대상 Module이 비활성화(Deactivate)된 후 Registry에서 제거되고, 그 contract 바인딩이 해제된다. 다른 활성 Module의 `requires`가 그 contract에 의존 중이면 해제를 거부한다.
- **운용 규칙.**
  1. 대상 module id가 Registry에 없으면 해제 실패(`NotRegistered`).
  2. 다른 활성 Module의 `requires`가 대상의 contract에 의존 중인지 확인한다. 의존이 하나라도 존재하면 해제를 거부한다 (`DependentExists`) — 의존 소비자를 끊는 해제를 막는다.
  3. 의존이 없으면 대상 Module을 비활성화하고 Registry에서 제거하며, 그 contract 바인딩을 해제한다.
- **실패 reason.** `DependentExists`(대상 contract에 의존하는 활성 Module 존재) | `NotRegistered`(대상 module id 미등록).

---

## §3. 등록·교체·해제 절차 규칙

4연산 위에서 지켜지는 절차 규칙이다. 근거는 01 §3.3 불변 규칙이다.

### R-교체-1. 교체는 동일 contract 내에서만 (INV-1)

Replace는 새 Module의 `contract`가 대상 contract와 동일할 때만 성립한다 (§2.3 규칙 1). contract가 다르면 교체가 아니라 다른 계약의 등록이므로 `ContractMismatch`로 거부한다. `replaceable=false`인 Module은 교체 예외이며 `NotReplaceable`로 거부한다.

### R-바인딩-1. 계약당 활성 바인딩 정확히 1 (INV-3)

한 contract에는 활성 Module이 **정확히 하나** 바인딩된다.

- Register는 Manifest를 등록부에 넣을 뿐, 한 contract에 활성 바인딩이 둘이 되게 만들지 않는다.
- Replace는 새 Module 활성화와 이전 Module 비활성화를 **한 교체 단위**로 수행하여, 교체 중에도 활성 바인딩이 1을 유지하도록 한다(이전 비활성화 없이 새 활성화만 하지 않는다).
- Resolve는 활성 바인딩이 정확히 1일 때만 유일한 핸들을 반환한다. 2개 이상이면 `DuplicateBinding`으로 실패한다 (§2.2 규칙 2).

### R-참조-1. 소비자 참조 변경 0 확인 (INV-1)

교체가 계약 소비자에게 투명함을 확인하는 절차다.

1. 교체는 동일 `contract` 내에서만 이뤄지므로, 소비자가 참조하는 것은 **contract id**이지 특정 module id가 아니다 (module-manifest.md §4 안정 식별자 규칙 — 의존은 contract에 건다).
2. 교체 전후로 소비자의 Resolve 대상(contract id)이 동일함을 확인한다. contract id가 안정적이므로(INV-7) 소비자 경로는 변하지 않는다.
3. 소비자 참조 변경이 0이 아니면(즉 소비자가 특정 module id에 직접 의존하고 있으면) 이는 INV-1 위반 신호다. 추측으로 우회하지 않고 Advisor에게 보고한다 (상위 규약 — 계약 충돌 보고).

### R-해제-1. 의존 존재 시 해제 거부 (DependentExists)

Deregister는 대상 Module의 contract에 의존하는 다른 활성 Module이 존재하면 거부한다 (§2.4 규칙 2). 이는 의존 소비자의 `requires`를 끊는 해제를 막아, 해제 후 Resolve가 `UnresolvedContract`로 깨지는 상태를 예방한다. 의존을 먼저 해소(해제하려는 contract에 의존하는 Module들을 먼저 Deregister)한 뒤에만 대상 Module을 해제한다.

---

## §4. 4연산 언어 중립 시그니처 (C-1)

각 연산의 입력·출력·실패를 **타입 수준**으로 서술한다. 특정 언어의 타입 표기법·문법을 쓰지 않고, 언어 중립 서술어(식별자 / 서술자 / 핸들 참조 / 식별자 쌍 / 실패 보고)로만 표현한다.

| 연산 | 입력 (타입 수준) | 출력 (타입 수준) | 실패 (타입 수준) |
|---|---|---|---|
| Register | 서술자 1건 (Module Manifest) | 식별자 (등록된 module id) | 실패 보고 (reason ∈ {ContractMismatch, DuplicateId}) |
| Resolve | 식별자 (contract id 또는 module id) | 핸들 참조 1건 (활성 Module 핸들, 정확히 1개) | 실패 보고 (reason ∈ {UnresolvedContract, DuplicateBinding, DependencyCycle}) |
| Replace | 식별자 (대상 contract id) + 서술자 1건 (새 Module Manifest) | 식별자 쌍 (이전 module id → 새 module id) | 실패 보고 (reason ∈ {ContractMismatch, NotReplaceable}) |
| Deregister | 식별자 (대상 module id) | 식별자 (해제된 module id) | 실패 보고 (reason ∈ {DependentExists, NotRegistered}) |

서술어 정의(언어 중립):

- **식별자** — 안정적으로 대상 하나를 가리키는 이름 (module id, contract id).
- **서술자** — Module Manifest 1건. 필드 계약은 01 §3.2-A(작성 지침: module-manifest.md).
- **핸들 참조** — 활성 Module을 가리키는 논리 참조. 물리 실현은 Adapter Binding 소관 (01 §4).
- **식별자 쌍** — 이전·새 module id 두 식별자의 순서쌍(교체 결과).
- **실패 보고** — 공통 Failure Report(구조 정본: 01 §3.2-D). reason은 위 집합의 한 값.

**C-1 명시.** 이 시그니처는 01 §3.1-A 4연산의 **인스턴스**이며 계약의 **확장·수정이 아니다** (framework/core/structure.md §7 확정 조건 C-1). 실행 코드(형태 B) 도입 시 이 시그니처를 구현하더라도 01 §3.1-A 계약 요소(입력·출력·완료 조건·실패 reason)는 변경 0으로 유지된다. 위반(형태 B가 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현을 진행하지 않고 Advisor에게 보고한다 (structure.md §7 규칙 4).

---

## §5. 실패 reason 코드 목록

4연산의 실패는 공통 Failure Report 구조로 보고한다. **구조(`operation`/`target`/`reason`/`location`)의 정본은 01 §3.2-D**이며, 본 문서는 구조를 재정의하지 않는다. 아래는 4연산에 해당하는 reason 코드만 연산별로 정리한 목록이다.

| 연산 | reason 코드 | 사유 |
|---|---|---|
| Register | `ContractMismatch` | Manifest가 Module Interface 계약을 만족하지 않음. |
| Register | `DuplicateId` | `id`가 Registry에서 유일하지 않음. |
| Resolve | `UnresolvedContract` | 대상 계약에 활성 바인딩이 없음. |
| Resolve | `DuplicateBinding` | 대상 계약에 활성 바인딩이 2개 이상 (INV-3 위반). |
| Resolve | `DependencyCycle` | `requires` 의존 그래프에 순환. |
| Replace | `ContractMismatch` | 새 Module이 동일 contract를 만족하지 않음 (INV-1). |
| Replace | `NotReplaceable` | 대상 Module이 교체 불가(`replaceable=false`). |
| Deregister | `DependentExists` | 대상 contract에 의존하는 활성 Module 존재. |
| Deregister | `NotRegistered` | 대상 module id가 등록되어 있지 않음. |

주:

- 위 목록은 4연산(Module 시스템)에 한정된다. 01 §3.2-D의 완전한 reason 열거에는 Config·수명주기 연산의 코드(예: SchemaViolation, MissingRequired, ShutdownIncomplete 등)도 포함되나, 그 연산들은 본 문서의 소관이 아니다 — 완전 열거의 정본은 01 §3.2-D를 참조한다.
- `ContractMismatch`는 Register와 Replace가 공유한다 (01 §3.1-A). 어느 연산의 실패인지는 Failure Report의 `operation` 필드로 구분된다 (구조 정본 01 §3.2-D).

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- 본 문서의 모든 연산 계약은 01 §3.1-A의 인스턴스다. 어떤 연산도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.1-A(연산)·§3.2-C(registry)·§3.2-D(Failure Report)다 (C-1).
- 본문·표·규칙 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명이 0건이다. 등록·활성화의 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관 (01 §4)" 포인터를 둔다 (mention/use 경계 — 금지 토큰의 예시도 Core 문서에서는 누출이다).
- reason 코드(`ContractMismatch` 등)와 필드명(`id`·`contract`·`requires`·`replaceable`)은 정본 01 §3이 쓰는 계약 식별자를 그대로 인용한 것이며, 특정 언어·직렬화 형식의 문법이 아니다.

---

## §7. 요약 (한눈에 보기)

- Registry = Module System의 등록부. 4연산의 정본 = 01 §3.1-A (본 문서는 인스턴스, 재정의 아님 — C-1).
- 4연산: Register(등록·유일성) · Resolve(활성 바인딩 정확히 1 → 유일 핸들) · Replace(동일 contract 내 교체, 소비자 참조 0) · Deregister(의존 존재 시 거부).
- 절차 규칙: 동일 contract 교체(INV-1) · 계약당 활성 바인딩 1(INV-3) · 소비자 참조 변경 0 확인(INV-1) · DependentExists 해제 거부.
- 언어 중립 시그니처는 실행 코드 도입 후에도 01 §3.1-A 계약 변경 0을 보장한다 (C-1).
- Failure Report 구조 정본 = 01 §3.2-D. 본 문서는 4연산 reason 코드 목록만 전개한다.
- 구체 등록·활성화의 물리 실현은 Adapter Binding 문서 소관 (01 §4). Core 문서 본문에는 그 토큰이 0건이다 (C-3).
