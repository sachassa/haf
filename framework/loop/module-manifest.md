# framework/loop/module-manifest — Loop Provider Module Manifest 인스턴스

작성일: 2026-07-06
상태: v0.6 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드(`id`/`contract`/`version`/`requires`/`entrypoint`/`configSchema`/`replaceable`). 본 문서가 채우는 서술자 계약의 정본. 필드명·의미·필수/선택 표기의 진위 판정 기준은 이 §가 유지한다.
- specs/01-runtime.md §3.3 INV-7 — 안정 식별자(`id`·`contract` id 안정성). INV-1 — 교체 가능(`replaceable` 기본값 근거). INV-2 — 단독 사용(필수 계약 해소 시 부분 집합 기동; `requires` 값의 Resolve 게이트 논의 근거). INV-4 — Core AI 비의존.
- specs/01-runtime.md §3.1-A — Register/Resolve 연산. Resolve 완료 조건("requires가 모두 해소된다")이 `requires` 값의 계약 근거다. 이 Manifest는 Register의 입력이 된다.
- specs/01-runtime.md §8 예1 — contract id `MemoryServiceInterface`(사전 명명). 이 Manifest의 `requires` 값이 **기존 contract id 참조**임의 정합 기준(동일 contract 백엔드 스왑 예시).
- specs/01-runtime.md §4 — Adapter Binding(구체 직렬화·물리 진입점 해소 소관). 본 문서는 § 포인터로만 참조한다.
- specs/03-loop.md §3.1 — Loop가 노출하는 **사이클 구동 연산**(단일 위임 1건 + Runtime Context를 입력으로 Lifecycle 한 사이클 구동). `entrypoint`가 노출하는 논리 진입점의 근거.
- specs/03-loop.md §3.1-A(6) Memory Update·§5(Memory 소비 — Record 경로)·§3.3 INV-5(Learn 불가피성 — 모든 사이클 종료는 Learn → Memory Update)·INV-7(Memory 단일 Port). `requires` = `MemoryServiceInterface`의 Core 근거.
- specs/03-loop.md §4.1 — Memory 접근 행(물리 실현이 Memory Service Interface Module의 Resolve임을 확인). Adapter Binding 소관 포인터로만 인용한다.
- framework/runtime/module-manifest.md — Module Manifest **형식 규격**(7필드 작성 지침·안정 식별자 규칙·언어 중립 시그니처). 본 문서는 그 형식을 이 Provider에 대해 채운 **인스턴스**다.
- framework/verifier/module-manifest.md — Manifest 인스턴스 **관례 표본**(구성·필수/선택 표기 보존·§5 결정 기록 절·"Advisor 확인 — 인스턴스 값" 기록 관례·DP-V1/DP-V2 동형 적용). 단, `requires` 값은 사실 관계 상이(§3 `requires`·§5 참조).
- framework/memory/module-manifest.md — Manifest 인스턴스 관례 정본(`version` 독립 축 `0.1.0` 관례·`id` 접미 `-provider` 관례 동형 적용). `contract` = `MemoryServiceInterface`가 이 Manifest의 `requires`가 참조하는 계약임의 인스턴스 근거.
- framework/core/config-schema.md §7 — 재시도 한도 키 `retry.limit`(기본 2·Global 스코프)의 **소유 소재**. Loop가 이 키의 소비자일 뿐 소유자가 아님의 근거(DP-L2).
- framework/core/structure.md §2(Module 구현 디렉터리 경계 — 자기완결, C-3 확장)·§5(금지 토큰 규칙 C-3 확장)·§7(Core Contract 불변 조건 C-1).
- specs/00-glossary.md — 용어 정본. Module / Module Manifest / 모듈 시스템 / Runtime Context는 §3.2-I, **Loop**는 Core Component 표제어(정본 specs/03-loop.md)다.

거버넌스: 이 문서는 `framework/loop/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인·직렬화 형식 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.6 Draft | 최초 작성. Loop Provider Module의 01 §3.2-A 7필드 인스턴스(`id`=`loop-provider`·`contract`=`LoopInterface`(DP-L1)·`version`=`0.1.0`·`requires`=`MemoryServiceInterface`(Advisor 확인 — 인스턴스 값)·`entrypoint`=추상 참조(03 §3.1 사이클 구동 연산 노출)·`configSchema`=선언하지 않음(DP-L2)·`replaceable`=기본 true), 필드별 인스턴스 값·근거, `entrypoint` 추상 참조 + 물리 해소 Adapter Binding 소관 포인터(물리 경로·형식 하드코딩 0), 필수/선택 표기 정본 대조 보존, DP-L1·DP-L2 결정 기록 + `id`·`requires` Advisor 확인 기록. 01·03 계약 재정의·확장 0, 금지 토큰 0(자가 전수 스캔), Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task L2) |
| 2026-07-06 | v0.6 Baseline | v0.6 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **필드 계약의 정본은 specs/01-runtime.md §3.2-A이다.** 이 문서는 그 Module Manifest 계약을 **Loop Provider Module에 대해 채운 인스턴스**이며, 필드·의미·필수/선택 표기를 **재정의·확장하지 않는다** (framework/core/structure.md §7 확정 조건 C-1). 필드 계약 요소는 01 §3.2-A를 § 포인터로 참조한다.
- **형식 규격의 정본은 framework/runtime/module-manifest.md이다.** 그 문서는 임의 Manifest를 **어떻게 작성·판독하는가**(7필드 형식·안정 식별자 규칙·언어 중립 시그니처)를 규율하고, 이 문서는 그 형식을 이 Provider 하나에 대해 **구체 값으로 채운** 등록 서술자다. 두 문서 모두 01 §3.2-A를 진위 판정 기준으로 삼는다.
- **사이클 구동 계약의 정본은 specs/03-loop.md이다.** 이 Provider가 구현하는 contract(§3 아래 `LoopInterface`)가 노출하는 단계 전이·재작업 루프·종료·기록 계약은 03 §3이 소유한다. 본 문서는 그 계약을 **재정의·재서술하지 않고** § 포인터로만 참조하며, 이 Manifest는 그 Module의 등록 서술자일 뿐이다.
- **이 문서는 Module 구현 디렉터리 문서다** (framework/core/structure.md §2 — 각 Module의 Manifest를 자기 경계에 두는 자기완결 단위, 01 §3.2-E 규칙 2). 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (framework/core/structure.md §5 C-3 확장, 01 §3.3 INV-4). 구체 직렬화·물리 진입점 해소·역할 실행 채널·환경 경로 관례는 **Adapter Binding 문서 소관**이며 (01 §4, 03 §4.1), 필요한 자리에는 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Module / Module Manifest / 모듈 시스템 / Runtime Context는 Glossary §3.2-I가, Loop / Agent Lifecycle / Memory Service Interface는 Glossary 기존 용어가 정본이다. 새 용어를 정본처럼 신설하지 않는다. **`LoopInterface`는 이 Provider가 구현하는 contract 식별자 값이지 Glossary 표제어의 신설이 아니다** (§5 DP-L1 참조).
- 필드명 백틱 표기(`id` 등)와 예시 식별자는 특정 언어·직렬화 형식의 문법이 아니라, 정본 01 §3.2-A가 쓰는 필드명·서술 라벨을 그대로 인용한 것이다.

---

## §1. 목적

이 문서는 **Loop Provider Module**의 등록 서술자(Module Manifest)다. Loop Provider는 contract `LoopInterface`를 구현하는 Module이며, 단일 위임 하나에 대해 Agent Lifecycle(Consult → Complete) 한 사이클을 구동하는 실행 단위를 Runtime이 등록·해소·교체한다 (03 §3.1, 01 §3.1-A·§4.1 `framework/loop/`).

이 규격의 책임은 두 가지다.

- 01 §3.2-A의 7필드를 이 Provider에 대한 **구체 값**으로 채운다 — `contract`는 `LoopInterface`로 확정하고(§5 DP-L1), `entrypoint`는 사이클 구동 연산(03 §3.1)을 노출하는 추상 참조로 두며 물리 해소는 Adapter Binding 문서 소관으로 미룬다. `requires`는 `MemoryServiceInterface`를 선언하고(§3·§5 — Memory Update가 모든 사이클의 불가피 단계이므로), `configSchema`는 선언하지 않는다(§5 DP-L2).
- 필드의 필수/선택 표기를 정본 그대로 보존한다 (필수/선택 표기 보존 — session-handoff-v0.2 §1.5 Lesson 후보 2).

이 Manifest는 Runtime의 **Register** 연산(01 §3.1-A, 운용 규칙: framework/runtime/module-registry.md §2.1)의 입력이 된다. 각 Module은 자기완결(self-contained) 단위이므로, 이 Manifest는 그 Module의 `id`·`contract`·`entrypoint`·`requires` 등 자기완결 참조를 한 서술자에 묶는다 (01 §3.2-E 규칙 2). 이 Provider가 구현하는 사이클 구동 계약(§3.1 단계 전이·§3.1-B 재작업 루프·§3.1-C 종료·§3.2 기록 포맷)의 정본은 specs/03-loop.md가 유지하며, 본 문서는 그 계약을 재서술하지 않는다.

---

## §2. 7필드 인스턴스 (정본 대조 표)

아래 표는 01 §3.2-A의 7필드를 이 Provider에 대한 값으로 채운 것이다. **필드명·의미·필수/선택 표기는 정본(01 §3.2-A) 그대로**이며, "값 (이 Provider 인스턴스)" 열만 본 문서가 채운다. 필드 계약을 재정의하지 않는다.

| 필드 | 의미 (정본: 01 §3.2-A) | 값 (이 Provider 인스턴스) | 필수 |
|---|---|---|---|
| `id` | Module 고유 식별자. 안정적(stable)이어야 교체의 기준이 된다. | `loop-provider` (역할·계약 기반 안정 식별자 — §3 참조) | 예 |
| `contract` | 이 Module이 구현하는 계약(Port/Interface) 식별자. 교체는 동일 `contract` 내에서만 성립한다. | `LoopInterface` (DP-L1 — §3·§5 참조) | 예 |
| `version` | Module 버전. | `0.1.0` (이 Provider Module 자체 버전 — §3 참조) | 예 |
| `requires` | 의존하는 contract id 목록. Resolve 시 모두 해소되어야 한다. | `MemoryServiceInterface` (Memory Update가 모든 사이클의 불가피 단계 — 03 INV-5·INV-7; §3·§5 참조) | 아니오(기본 없음) |
| `entrypoint` | 실행 진입점의 추상 참조. 구체 바인딩은 01 §4가 해소한다. | 추상 참조 — 사이클 구동 연산(03 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4). | 예 |
| `configSchema` | 이 Module의 Config 스키마. | 선언하지 않음 (생략 — DP-L2, §3·§5 참조) | 아니오 |
| `replaceable` | 교체 가능 여부. 기본 `true` (ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 기본 `true` (생략 — §3 참조) | 아니오(기본 true) |

주:

- **필수/선택 표기는 정본 그대로 보존한다.** `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기를 복제한다 — 누락되면 계약 변경으로 읽힌다 (session-handoff-v0.2 §1.5 Lesson 후보 2). `requires`는 **선택 필드(기본 없음)**이며, 이 Provider는 그 선택 필드에 값(`MemoryServiceInterface`)을 **채운** 것이다 — 필드의 필수/선택 지위를 바꾸지 않는다.
- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true).
- 상세 필드 계약의 정본은 01 §3.2-A가, 형식 작성 지침은 framework/runtime/module-manifest.md가 유지한다. 이 표는 값 인스턴스이며 계약의 진위 판정 기준이 아니다.

---

## §3. 필드별 인스턴스 값·근거

각 필드의 값 선택 근거다. 값은 이 Provider의 인스턴스이며, 필드 계약은 재정의하지 않는다.

### `id` = `loop-provider` (필수)

- 근거: 역할·계약에 기반한 **안정 식별자**. 구현 세부(버전·환경·오케스트레이션 방식)를 인코딩하지 않는다 (framework/runtime/module-manifest.md §3 `id`, 01 INV-7). 구현이 교체돼도 이 `id`는 유지되어 교체(Replace)의 기준이 된다. 명명은 관례 정본(framework/memory/module-manifest.md §3 `id`=`memory-service-provider`, framework/verifier/module-manifest.md §3 `id`=`verifier-provider`)과 **동형**으로 역할명 + 관례 접미 `-provider`를 조합한 인스턴스 값이다.
- 회피: 오케스트레이션 방식·리비전·마일스톤 어휘(예: "engine")를 `id`에 섞지 않는다 — 그러면 교체마다 `id`가 바뀌어 안정 기준(INV-7)이 무너진다.
- 주: 이 `id` 값은 명시 Advisor 결정(DP) 대상이 아니라 Manifest 인스턴스 관례에 따른 **인스턴스 값**이며, **Advisor 확인 완료(2026-07-06)** — 관례 동형이고 01 INV-7 안정 식별자 요건을 충족한다는 근거로 승인되었다 (§5 "Advisor 확인 — 인스턴스 값" 기록).

### `contract` = `LoopInterface` (필수)

- 근거: 이 Provider가 구현하는 **사이클 구동 계약(Port/Interface)** 식별자다. Advisor 결정 DP-L1로 확정한다(§5). 구현·오케스트레이션 방식이 다른 새 Provider로 교체(Replace)해도 동일 `contract` 내이므로, 이 계약의 소비자(03 dependents — Workflow의 다중 사이클 오케스트레이션 등, 03 §2)의 참조는 그대로다 (01 INV-1, §8 예1 동형). 이 계약이 노출하는 단계 전이 규칙·재작업 루프·종료 규칙·기록 포맷의 정본은 03 §3이 유지한다.
- 회피: 특정 구현·오케스트레이션 방식을 `contract`에 섞지 않는다 — 동일 contract 교체(INV-1)가 불가능해진다.
- 결정 기록: §5 DP-L1.

### `version` = `0.1.0` (필수)

- 근거: 이 **Provider Module 자체의 버전**을 가리키는 고정된 버전 문자열이다 (framework/runtime/module-manifest.md §3 `version` — 같은 문자열은 항상 같은 Module 버전). Framework/Spec 버전(현재 v0.6 마일스톤)과는 **별개의 축**이며, Provider 구현이 갱신되면 이 값이 상승한다. 초기 인스턴스 값으로 `0.1.0`을 둔다 (framework/memory/module-manifest.md·framework/verifier/module-manifest.md 관례 동형 — Provider Module 버전은 독립 축, 초기 `0.1.0`).
- 회피: 시점에 따라 대상이 달라지는 비고정 라벨을 쓰지 않는다 — 버전으로서 안정 참조가 되지 못한다.

### `requires` = `MemoryServiceInterface` (선택 — 기본 없음; 이 Provider는 값을 채움)

- 근거: 이 Provider가 구현하는 사이클 구동 연산은 **Memory Update 단계를 불가피하게 포함**한다. 03 INV-5(Learn 불가피성)는 "성공이든 실패든 모든 사이클 종료는 Learn → Memory Update를 거친다"고 규정하고, 03 §3.1-A(6) Memory Update 단계는 "모든 접근은 Memory Service Interface(단일 Port) 경유"(03 INV-7)로 후보를 기록한다. 즉 이 Module은 어느 사이클에서도 Memory Service Interface 계약 없이는 자신의 사이클 구동 계약을 완결할 수 없다. `requires`는 "의존하는 contract id 목록 — Resolve 시 모두 해소되어야 한다"(01 §3.2-A)이므로, 이 불가피 의존을 `MemoryServiceInterface`로 선언한다.
- **module id가 아니라 contract id를 나열한다** (framework/runtime/module-manifest.md §3 `requires`). `MemoryServiceInterface`는 Memory Service Provider Module(`id`=`memory-service-provider`, framework/memory/module-manifest.md)이 구현하는 **contract id**이며 01 §8 예1·04 §4.1이 사전 명명한 값이다. 계약에 의존하므로 저장 백엔드가 다른 Provider로 교체(01 §8 예1)돼도 이 Module의 `requires` 참조는 유지된다 (01 INV-1).
- **역할 실행(CP1~CP3)은 `requires`에 넣지 않는다.** 검증 게이트의 각 역할(Worker/Verifier/Advisor) 실행은 위임·보고 메시지(02 §3.2-B/C/D) 흐름을 통한 역할 디스패치이며, Runtime의 module Resolve가 아니다. 그 물리 실현 채널은 Adapter Binding 문서 소관이다 (03 §4.1 "역할 실행" 행, 02 §4.1). 따라서 이 역할들은 이 Manifest의 `requires`(= 의존 contract id 목록)에 포함하지 않는다 — `requires`는 Runtime이 Resolve로 해소하는 계약 의존만 담는다.
- **INV-2와의 정합.** `MemoryServiceInterface`를 hard `requires`로 선언하면 Loop Provider가 Resolve될 때 Memory Service Interface 바인딩이 함께 해소되어야 한다 (01 §3.1-A Resolve 완료 조건). 이는 01 INV-2(단독 사용 — 필수 계약만 해소되면 부분 집합으로 기동)를 위반하지 않는다. INV-2는 **Runtime이 필수 계약 집합만으로 기동**할 수 있음을 보장하는 규칙이고, 이 `requires`는 Loop Provider가 활성일 때 Memory Service Interface를 그 의존 집합에 포함시킬 뿐이다. Loop 사이클 구동에 Memory Update가 불가피(03 INV-5)한 이상, 이 의존은 선택적 보강이 아니라 계약적 필수다.
- **Verifier 선례(requires=없음)와의 사실 관계 차이.** framework/verifier/module-manifest.md §3은 `requires`=없음을 택했다 — Verifier의 Memory 회수(Recall)는 06 §5의 **"필요할 때만"** 이뤄지는 **선택적 보강**이며 판정 연산의 Resolve를 게이트하지 않기 때문이다. Loop는 사실 관계가 다르다 — Memory **쓰기(Record)**가 Memory Update 단계로 **모든 사이클에서 실행**되므로(03 §5 쓰기·INV-5), 선택적 회수가 아니라 불가피한 계약 의존이다. 두 Provider는 같은 관례를 따르되, Memory에 대한 의존의 성격이 다르므로 `requires` 값이 갈린다.
- 회피: 존재하지 않는 contract id를 여기서 **신설·추측하지 않는다** (Glossary 밖 새 용어 금지, 03 §3 재정의 금지). `MemoryServiceInterface`는 사전 명명된 기존 contract 값이며(01 §8 예1·04 §4.1), 신조어가 아니다. 물리 바인딩이 추가 Adapter contract 의존을 도입한다면 그 선언은 Adapter Binding 문서가 소유한다 (01 §4, 03 §4.1) — 이 Core 서술자가 아니다.
- 주: 이 `requires` 값은 **Advisor 확인 완료(2026-07-06)** — Memory Update는 모든 사이클의 필수 단계(03 INV-5·INV-7)이고 03 §4.1 Memory 접근 행이 명시적으로 Memory Service Interface Module의 Resolve를 요구하며, 역할 실행은 module Resolve가 아니어서 requires에 넣지 않는다는 근거로 이 인스턴스 값이 승인되었다 (§5 "Advisor 확인 — 인스턴스 값" 기록).

### `entrypoint` = 추상 참조 (필수)

- 근거: 이 Module의 활성화 진입 — 단일 위임 하나에 대해 Lifecycle 한 사이클을 구동하는 연산(03 §3.1: 입력 = 위임 메시지 1건(02 §3.2-B) + Runtime Context(01 §3.2-C), 출력 = 완료 보고(02 §3.2-C) 또는 에스컬레이션) — 을 노출하는 논리적 진입점을 가리키는 **추상 참조**다. 구체 바인딩(직렬화·물리 경로·호출 규약·역할 실행 채널 배선)은 기입하지 않는다. 상세는 §4.
- 회피: 특정 실행 환경의 물리 경로·형식별 로케이터를 Manifest에 직접 기입하지 않는다 — 환경 의존을 Core 서술자에 하드코딩하면 이식 시 서술자가 함께 바뀌어 AI·환경 비의존(01 INV-4, 03 INV-9)이 깨진다.

### `configSchema` = 선언하지 않음 (선택)

- 근거 (Advisor 결정 DP-L2, §5): Loop가 소비하는 유일한 Config 값은 **재시도 한도**이며(03 §3.1-B — "재시도 한도 값은 Config로 주어진다. Loop는 한도 초과 판정 규칙만 정의한다"), 그 키 `retry.limit`은 **Framework 수준 키**로 framework/core/config-schema.md §7이 이미 소유한다(추상 키 `retry.limit`, 기본 `2`, Global 스코프 기본 + Project/Module override). 이 키를 이 Manifest의 `configSchema`로 끌어오면 **값 소유가 이중화**된다. Loop는 effective config의 **소비자**(01 §3.2-B)일 뿐 그 키의 소유자가 아니다. 따라서 이 Manifest는 `configSchema`를 **선언하지 않는다**(01 §3.2-A 선택 필드).
- 회피: `retry.limit`을 이 Manifest의 자기 Module `configSchema`로 재선언하지 않는다 — `configSchema`는 자기 Module 네임스페이스에 국한된 설정이고(framework/runtime/module-manifest.md §3 `configSchema`), Framework 수준 키를 여기에 담으면 config-schema.md §7의 소유와 충돌하며 값 원천이 둘로 갈린다.
- 결정 기록: §5 DP-L2.

### `replaceable` = 기본 `true` (선택 — 기본 true)

- 근거: 생략하여 기본값 `true`를 취한다. 모든 Module은 교체 가능이 기본이다 (01 INV-1, ARCHITECTURE 3.2). 사이클을 구동하는 실행 단위도 Runtime이 호스팅하는 하나의 Module이므로(03 §2) 동일 `contract` 내 교체가 성립해야 한다. 이 Provider에는 교체 불가의 근거가 없다.
- 회피: 근거 없는 `false`를 두지 않는다 — `false`는 근거를 요구하는 명시적 예외다 (01 INV-1).

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider Module의 활성화 진입을 가리키는 **추상(논리) 참조**다. 그것이 노출하는 것은 사이클 구동 연산(03 §3.1) — 단일 위임 1건과 Runtime Context를 입력받아 7단계 Lifecycle 한 사이클을 구동하고 완료 보고 또는 에스컬레이션을 산출하는 연산 — 이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩 — 직렬화 형식, 물리 경로·로케이터, 호출 규약, 역할 실행 채널·루프 상태 기록 저장 배선 — 은 전부 **Adapter Binding 문서 소관**이다 (01 §4, 03 §4.1). 이 Core 서술자에는 그 어떤 물리 경로·형식 토큰도 하드코딩하지 않는다 (framework/runtime/module-manifest.md §3 `entrypoint` 회피 규칙 정합).
- 이 분리로 실행 환경 이식·교체(01 §8 예1, 03 §4.2 이식 교체 지점) 시에도 이 Manifest의 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고, 물리 바인딩만 Adapter 경계에서 교체된다.
- `requires`가 참조하는 `MemoryServiceInterface`의 물리 실현 역시 Adapter 소관이다 — 03 §4.1 "Memory 접근" 행은 그 단일 Port 경유가 "Runtime이 배선한 Memory Service Interface Module을 Resolve하여 실현"됨을 명시한다. 이 Core 서술자는 그 Resolve 대상 contract id를 `requires`로 선언할 뿐, 물리 배선을 기입하지 않는다.

---

## §5. 결정 기록 (Advisor 결정 — DP-L1·DP-L2 + Advisor 확인)

이 절은 이 Manifest에 반영된 Advisor 결정 2건(DP-L1·DP-L2)과 인스턴스 값 확인 2건(`id`·`requires`)을 기록한다. 두 결정은 위임의 확정 입력이며, 본 문서는 이를 그대로 반영한다(임의 변경 없음). 인스턴스 값 확인은 새 결정이 아니라, 관례·정본 근거로 채운 값에 대한 Advisor 승인이다.

### DP-L1 — `contract` = `LoopInterface`

- **결정:** 이 Provider가 구현하는 사이클 구동 계약 식별자를 `LoopInterface`로 확정한다.
- **근거:** 저장소에 이 계약의 **사전 명명이 없다**(Advisor 실측 — `LoopInterface`/`LoopPort` 저장소 전역 0건. 작성 시점 재확인: 전역 검색 0건 — 실측 후 기록 L-07). Memory 선례의 contract `MemoryServiceInterface`는 01 §8 예1이 사전 명명했고, Loop에는 그런 대응물이 부재하다(Verifier의 `VerifierInterface`도 사전 명명 부재였던 DP-V1과 동형 상황). 따라서 이 명명은 Advisor의 결정 사안이며, Glossary 정본 어휘 **"Loop"**(Core Component 표제어, 정본 specs/03-loop.md)에 Manifest 관례 접미 **"Interface"**(Port/Interface 계약 식별자 관례, 01 §3.2-A)를 조합해 확정했다. 이는 **신조어 창설이 아니라** 기존 정본 어휘 + 관례 접미의 조합이며, Memory 선례(`MemoryServiceInterface`)·Verifier 선례(`VerifierInterface`)와 동형이다.
- **"Engine" 배제:** Glossary 설명문·ROADMAP 마일스톤이 "Loop Engine"/"엔진" 어휘를 쓰나, contract 식별자는 Glossary 표제어 "Loop"만 취한다. "Engine"은 ROADMAP 마일스톤 명칭이므로 안정 식별자에 넣지 않는다(마일스톤·버전 계열 어휘를 식별자에 인코딩하지 않는 안정 식별자 규칙 — framework/runtime/module-manifest.md §3 `id`/`contract`, 01 INV-7).
- **경계:** `LoopInterface`는 이 Manifest의 `contract` 필드 **값(식별자)**이지 Glossary 표제어의 신설이 아니다(§0, §6 — DP-V1 동형 경계 문구). 이 값이 노출하는 단계 전이·재작업·종료·기록 계약의 정본은 03 §3이 유지하며, 이 Manifest는 그 계약을 재정의하지 않는다.

### DP-L2 — `configSchema` 생략

- **결정:** 이 Manifest는 `configSchema`를 **선언하지 않는다**(01 §3.2-A 선택 필드).
- **근거:** Loop가 소비하는 Config 값은 재시도 한도뿐이며(03 §3.1-B), 그 키 `retry.limit`은 **Framework 수준 키**로 framework/core/config-schema.md §7이 소유한다(기본 `2`·Global 스코프 기본 + Project/Module override — DP-1 해소). Loop는 effective config의 **소비자**(01 §3.2-B)일 뿐 그 키의 소유자가 아니므로, 이 키를 자기 Module `configSchema`로 끌어오면 값 소유가 이중화된다. 이는 Verifier의 `configSchema` 생략(DP-V2 — 소비 Config 값 부재)과 동형의 생략이되, 근거가 다르다: Verifier는 **소비 값 자체가 없어서** 생략했고, Loop는 **소비 값은 있으나 그 소유가 Framework 수준(config-schema.md §7)에 이미 있어서** 생략한다.
- **명기:** `configSchema` 생략(01 §3.2-A 선택 필드) — `retry.limit`은 framework/core/config-schema.md §7이 소유하는 Framework 수준 키이며 본 Manifest는 이를 재선언하지 않는다. 이 키의 값·스코프·병합 규칙의 정본은 config-schema.md §7·01 §3.2-B가 유지한다.

### Advisor 확인 — `id`·`requires` 인스턴스 값 (2026-07-06)

- **성격:** 이 항목은 새 설계 **결정(DP)이 아니라**, 명시 DP 없이 관례·정본 근거로 채운 두 **인스턴스 값**(`id`·`requires`)에 대한 Advisor **확인(승인)** 기록이다. 두 값의 원천 근거는 §3에 있으며, 이 확인으로 미확정 잔여가 없다(§3·§6·§9 정합).
- **`id` = `loop-provider` 승인:** Manifest 인스턴스 관례(framework/memory/module-manifest.md §3 `id`=`memory-service-provider`, framework/verifier/module-manifest.md §3 `id`=`verifier-provider`)와 동형이고, 01 INV-7 안정 식별자 요건을 충족한다.
- **`requires` = `MemoryServiceInterface` 승인:** Loop는 Memory Update가 모든 사이클의 필수 단계(03 INV-5·INV-7)이고, 03 §4.1 Memory 접근 행이 명시적으로 Memory Service Interface Module의 Resolve를 요구한다. 이는 Verifier 선례(requires=없음)와 **사실 관계가 상이**하다 — Verifier의 Memory 소비는 06 §5 "필요할 때만"의 **선택적 보강**이라 Resolve를 게이트하지 않지만, Loop의 Memory Update는 불가피한 계약 필수다. 역할 실행(CP1~CP3)은 위임·보고 메시지 흐름의 역할 디스패치(02 §4.1, 03 §4.1)로 module Resolve가 아니므로 `requires`에 넣지 않는다. 이 근거로 인스턴스 값(`MemoryServiceInterface`)이 승인되었다.

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- **재정의·확장 0.** 본 문서의 7필드는 01 §3.2-A의 인스턴스다. 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A(필드 계약)와 framework/runtime/module-manifest.md(형식 규격)다. 이 Provider가 구현하는 사이클 구동 계약(03 §3 단계 전이·재작업 루프·종료·기록)도 **재정의하지 않고** § 포인터로만 참조했다. 필수/선택 표기(`requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)")를 정본 그대로 보존했고, `requires`의 선택 지위를 바꾸지 않은 채 값만 채웠으며, 새 필드를 추가하지 않았다.
- **금지 토큰 0 (자가 전수 스캔).** 본문·표·예시 전체를 다음 후보 집합 **전체**로 전수 스캔하여 0건임을 확인했다 (framework/core/structure.md §5 C-3 확장, 단일 토큰 검색에 국한하지 않음) — { 특정 AI 이름·모델명·제품 기능명 } ∪ { 특정 프로그래밍 언어명·툴체인명·직렬화 형식명·환경 경로 토큰 }. 진입점·역할 실행 채널·루프 상태 기록 저장의 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관 (01 §4, 03 §4.1)" 포인터를 두었다 (mention/use 경계 — 금지 토큰의 예시도 누출이다, session-handoff-v0.2 §1.5 Lesson 후보 3). `id`·`contract`·`requires` 값(`loop-provider`·`LoopInterface`·`MemoryServiceInterface`)은 계약 **필드 값**이지 금지 토큰이 아니다.
- **새 계약·용어 0.** `requires`에서 존재하지 않는 contract를 신설하지 않았다 — `MemoryServiceInterface`는 01 §8 예1·04 §4.1이 사전 명명한 기존 contract 값이다. Glossary 밖 새 용어를 만들지 않았다. `LoopInterface`는 `contract` 필드의 식별자 **값**이며 Glossary 표제어의 신설이 아니다 — Glossary 정본 어휘 "Loop" + 관례 접미 "Interface"의 조합으로 Advisor가 확정했다(§5 DP-L1).
- **미완성 형제 산출물 비인용 (07 R2).** 같은 Wave에서 동시 작성 중인 형제 산출물(예: 루프 상태 기록 인스턴스 문서)은 추측·인용하지 않았다. 본 문서는 확정 정본(01·03 spec)과 기존 Baseline(framework/runtime/·memory/·verifier/·core/ 문서)만 참조했다.
- **설계 확정(Advisor).** `contract` 명명(DP-L1)과 `configSchema` 생략(DP-L2)은 Advisor 결정으로 확정되어 §2·§3·§5에 반영했다. `id`(=`loop-provider`)·`requires`(=`MemoryServiceInterface`) 값은 명시 DP 없이 관례·정본 근거로 채운 **인스턴스 값**이며 Advisor 확인으로 승인되었다(§5 "Advisor 확인 — 인스턴스 값"). `version` 부여 관례(Framework/Spec 버전과 독립 축, 초기 `0.1.0`, 구현 갱신 시 상승)는 Memory·Verifier Manifest 관례 동형으로 적용했다. 미확정·open 잔여는 없다.

---

## §7. 요약 (한눈에 보기)

- 이 문서 = **Loop Provider Module**의 등록 서술자(Manifest) **인스턴스**. 필드 계약 정본 = 01 §3.2-A, 형식 규격 = framework/runtime/module-manifest.md, 사이클 구동 계약 정본 = 03 §3 (본 문서는 값 인스턴스, 재정의 아님 — C-1).
- 7필드 값: `id`=`loop-provider`(안정 식별자) · `contract`=`LoopInterface`(DP-L1) · `version`=`0.1.0`(Provider 자체 버전, 독립 축) · `requires`=`MemoryServiceInterface`(Memory Update가 모든 사이클의 불가피 단계 — 03 INV-5·INV-7; Advisor 확인) · `entrypoint`=추상 참조(사이클 구동 연산 03 §3.1 노출, 물리 해소 Adapter 소관) · `configSchema`=선언하지 않음(DP-L2 — `retry.limit`은 config-schema.md §7 소유) · `replaceable`=기본 true.
- 필수 4(`id`·`contract`·`version`·`entrypoint`) / 선택 3(`requires`·`configSchema`·`replaceable`) — 필수/선택 표기 정본 그대로. `requires`는 선택 필드이되 이 Provider가 값을 채운 경우다.
- `requires`가 Verifier 선례(=없음)와 갈리는 이유: Loop의 Memory 쓰기(Record)는 Memory Update 단계로 **모든 사이클에서 실행**되는 불가피 의존(03 INV-5·§5)이고, Verifier의 Memory 회수는 "필요할 때만"의 선택적 보강(06 §5)이라 Resolve를 게이트하지 않는다. 역할 실행(CP1~CP3)은 역할 디스패치(02 §4.1)로 module Resolve가 아니므로 `requires`에 넣지 않는다.
- 이 Manifest는 Runtime Register(01 §3.1-A, module-registry.md §2.1)의 입력이며, 구현하는 사이클 구동 계약은 03 §3.
- 물리 진입점·직렬화·역할 실행 채널·Memory 배선은 Adapter Binding 문서 소관 (01 §4, 03 §4.1). Module 구현 디렉터리 문서 본문에는 그 토큰이 0건이다 (C-3 확장).
