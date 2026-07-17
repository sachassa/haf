# framework/workflow/module-manifest — Workflow Provider Module Manifest 인스턴스

작성일: 2026-07-06
상태: v0.7 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드(`id`/`contract`/`version`/`requires`/`entrypoint`/`configSchema`/`replaceable`). 본 문서가 채우는 서술자 계약의 정본. 필드명·의미·필수/선택 표기의 진위 판정 기준은 이 §가 유지한다.
- specs/01-runtime.md §3.3 INV-7 — 안정 식별자(`id`·`contract` id 안정성). INV-1 — 교체 가능(`replaceable` 기본값 근거). INV-2 — 단독 사용(필수 계약 해소 시 부분 집합 기동; `requires` 값의 Resolve 게이트 논의 근거). INV-4 — Core AI 비의존.
- specs/01-runtime.md §3.1-A — Register/Resolve 연산. Resolve 완료 조건("requires가 모두 해소된다")이 `requires` 값의 계약 근거다. 이 Manifest는 Register의 입력이 된다.
- specs/01-runtime.md §8 예1 — contract id 백엔드 스왑 예시(동일 contract 내 교체). 이 Manifest의 `requires` 값이 **기존 contract id 참조**임의 정합 기준.
- specs/01-runtime.md §4 — Adapter Binding(구체 직렬화·물리 진입점 해소·역할 실행 채널 소관). 본 문서는 § 포인터로만 참조한다.
- specs/07-workflow.md §2 — Workflow의 Position·dependents. Workflow가 여러 사이클을 분해·병렬 디스패치·병합하는 다중 사이클 오케스트레이션임의 근거.
- specs/07-workflow.md §3.1 — Workflow가 노출하는 세 연산(분해 Decompose·디스패치 Dispatch·병합 Merge). `entrypoint`가 노출하는 논리 진입점의 근거.
- specs/07-workflow.md §3.1-C·§3.3 INV-5 — Merge 완료 조건("완료·검증된 Task 결과"만 병합, "각 Task 결과가 개별 검증을 통과했다"). `requires` = `LoopInterface`의 계약 근거(각 Task의 사이클 구동 완결 없이 병합 완료 조건 불성립).
- specs/07-workflow.md §5·§3.3 INV-7 — Memory 소비(Recall "필요할 때만"·Record "…중 다음 사이클에 필요한 것"의 조건부 소비)와 Memory 단일 Port. `requires`에서 Memory를 제외한 근거.
- specs/07-workflow.md §4.1 — 병렬 디스패치·위임 메시지 전달이 02 §4.1 역할 디스패치를 재사용함. `requires`에서 역할 실행을 제외한 근거(역할 디스패치는 module Resolve가 아니다).
- specs/07-workflow.md §9 결정 기록 — "Decompose·Dispatch·Merge는 다중 사이클 오케스트레이션으로 03의 단일 사이클 밖". `requires` = `LoopInterface` 근거의 원문.
- specs/03-loop.md §2 dependents — "Workflow는 여러 Loop 사이클을 분해·병렬 디스패치·병합한다. 단일 사이클 구동은 Loop, 다중 사이클 오케스트레이션은 Workflow다". `requires` = `LoopInterface` 근거의 원문(Workflow가 03의 사이클 구동 계약의 소비자임).
- framework/runtime/module-manifest.md — Module Manifest **형식 규격**(7필드 작성 지침·안정 식별자 규칙·언어 중립 시그니처). 본 문서는 그 형식을 이 Provider에 대해 채운 **인스턴스**다.
- framework/loop/module-manifest.md — Manifest 인스턴스 **관례 표본**(구성·필수/선택 표기 보존·§5 결정 기록 절·"Advisor 확인 — 인스턴스 값" 기록 형식·DP 동형 적용). 또한 이 Manifest의 `requires` 값 `LoopInterface`가 **확정된 기존 contract id**임의 출처(이 Provider가 신설하는 값이 아님).
- framework/verifier/module-manifest.md — 선례(`requires`=없음). 본 Manifest의 Memory 제외 근거가 이 선례와 **사실 관계 동형**임의 대비 대상(§3 `requires`·§5).
- framework/memory/module-manifest.md — 선례(`requires`=`MemoryServiceInterface`). 본 Manifest의 `requires` 근거가 이 선례와 **사실 관계 상이**함의 대비 대상. `version` 독립 축 `0.1.0` 관례·`id` 접미 `-provider` 관례 동형 적용.
- framework/core/structure.md §2(Module 구현 디렉터리 경계 — 자기완결, C-3 확장)·§5(금지 토큰 규칙 C-3 확장)·§7(Core Contract 불변 조건 C-1).
- specs/00-glossary.md — 용어 정본. Module / Module Manifest / 모듈 시스템 / Runtime Context는 §3.2-I, **Workflow (Component)**는 §3.2-D 표제어(정본 specs/07-workflow.md)다.
- AGENT.md — 상위 규약(위임·검증·Memory 원칙).

거버넌스: 이 문서는 `framework/workflow/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인·직렬화 형식 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.7 Draft | 최초 작성. Workflow Provider Module의 01 §3.2-A 7필드 인스턴스(`id`=`workflow-provider`(DP-W1)·`contract`=`WorkflowInterface`(DP-W1)·`version`=`0.1.0`(Advisor 확인 — 인스턴스 값)·`requires`=`LoopInterface`(DP-W2 — 병합은 각 Task의 사이클 구동 완결을 요구, Memory·역할 실행 제외)·`entrypoint`=추상 참조(07 §3.1 분해·디스패치·병합 연산 노출)·`configSchema`=선언하지 않음(DP-W3)·`replaceable`=기본 true), 필드별 인스턴스 값·근거, `entrypoint` 추상 참조 + 물리 해소 Adapter Binding 소관 포인터(물리 경로·형식 하드코딩 0), 필수/선택 표기 정본 대조 보존, DP-W1·DP-W2·DP-W3 결정 기록 + `id`·`version` Advisor 확인 기록. `requires` 근거를 Verifier 선례(없음)·Loop 선례(`MemoryServiceInterface`)와 정본 § 포인터로 구분 서술. 01·07 계약 재정의·확장 0, 금지 토큰 0(자가 전수 스캔), Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task WF2) |
| 2026-07-06 | v0.7 Baseline | v0.7 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **필드 계약의 정본은 specs/01-runtime.md §3.2-A이다.** 이 문서는 그 Module Manifest 계약을 **Workflow Provider Module에 대해 채운 인스턴스**이며, 필드·의미·필수/선택 표기를 **재정의·확장하지 않는다** (framework/core/structure.md §7 확정 조건 C-1). 필드 계약 요소는 01 §3.2-A를 § 포인터로 참조한다.
- **형식 규격의 정본은 framework/runtime/module-manifest.md이다.** 그 문서는 임의 Manifest를 **어떻게 작성·판독하는가**(7필드 형식·안정 식별자 규칙·언어 중립 시그니처)를 규율하고, 이 문서는 그 형식을 이 Provider 하나에 대해 **구체 값으로 채운** 등록 서술자다. 두 문서 모두 01 §3.2-A를 진위 판정 기준으로 삼는다.
- **오케스트레이션 계약의 정본은 specs/07-workflow.md이다.** 이 Provider가 구현하는 contract(§3 아래 `WorkflowInterface`)가 노출하는 분해·디스패치·병합 연산·데이터 포맷·불변 규칙은 07 §3이 소유한다. 본 문서는 그 계약을 **재정의·재서술하지 않고** § 포인터로만 참조하며, 이 Manifest는 그 Module의 등록 서술자일 뿐이다.
- **이 문서는 Module 구현 디렉터리 문서다** (framework/core/structure.md §2 — 각 Module의 Manifest를 자기 경계에 두는 자기완결 단위, 01 §3.2-E 규칙 2). 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (framework/core/structure.md §5 C-3 확장, 01 §3.3 INV-4). 구체 직렬화·물리 진입점 해소·역할 실행 채널·환경 경로 관례는 **Adapter Binding 문서 소관**이며 (01 §4, 07 §4.1), 필요한 자리에는 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Module / Module Manifest / 모듈 시스템 / Runtime Context는 Glossary §3.2-I가, **Workflow (Component)** / Work Graph / Task / 병렬 집합 / 소유 경계 / 인터페이스 계약은 Glossary §3.2-D·§3.2-J가, Agent Lifecycle / Memory Service Interface / Loop는 Glossary 기존 용어가 정본이다. 새 용어를 정본처럼 신설하지 않는다. **`WorkflowInterface`는 이 Provider가 구현하는 contract 식별자 값이지 Glossary 표제어의 신설이 아니다** (§5 DP-W1 참조).
- 필드명 백틱 표기(`id` 등)와 예시 식별자는 특정 언어·직렬화 형식의 문법이 아니라, 정본 01 §3.2-A가 쓰는 필드명·서술 라벨을 그대로 인용한 것이다.

---

## §1. 목적

이 문서는 **Workflow Provider Module**의 등록 서술자(Module Manifest)다. Workflow Provider는 contract `WorkflowInterface`를 구현하는 Module이며, 큰 작업을 작업 그래프(Work Graph)로 분해하고 병렬 집합을 여러 Agent에게 디스패치하며 완료·검증된 결과를 병합하는 실행 단위를 Runtime이 등록·해소·교체한다 (07 §3.1, 01 §3.1-A·§4.1 `framework/workflow/`).

이 규격의 책임은 두 가지다.

- 01 §3.2-A의 7필드를 이 Provider에 대한 **구체 값**으로 채운다 — `contract`는 `WorkflowInterface`로 확정하고(§5 DP-W1), `id`는 `workflow-provider`로 확정하며(§5 DP-W1), `entrypoint`는 분해·디스패치·병합 연산(07 §3.1)을 노출하는 추상 참조로 두고 물리 해소는 Adapter Binding 문서 소관으로 미룬다. `requires`는 `LoopInterface`를 단독 선언하고(§3·§5 DP-W2 — 병합은 각 Task의 사이클 구동 완결을 요구하므로), `configSchema`는 선언하지 않는다(§5 DP-W3).
- 필드의 필수/선택 표기를 정본 그대로 보존한다 (필수/선택 표기 보존).

이 Manifest는 Runtime의 **Register** 연산(01 §3.1-A, 운용 규칙: framework/runtime/module-registry.md §2.1)의 입력이 된다. 각 Module은 자기완결(self-contained) 단위이므로, 이 Manifest는 그 Module의 `id`·`contract`·`entrypoint`·`requires` 등 자기완결 참조를 한 서술자에 묶는다 (01 §3.2-E 규칙 2). 이 Provider가 구현하는 오케스트레이션 계약(§3.1 분해·디스패치·병합 연산·§3.2 데이터 포맷·§3.3 불변 규칙)의 정본은 specs/07-workflow.md가 유지하며, 본 문서는 그 계약을 재서술하지 않는다.

---

## §2. 7필드 인스턴스 (정본 대조 표)

아래 표는 01 §3.2-A의 7필드를 이 Provider에 대한 값으로 채운 것이다. **필드명·의미·필수/선택 표기는 정본(01 §3.2-A) 그대로**이며, "값 (이 Provider 인스턴스)" 열만 본 문서가 채운다. 필드 계약을 재정의하지 않는다.

| 필드 | 의미 (정본: 01 §3.2-A) | 값 (이 Provider 인스턴스) | 필수 |
|---|---|---|---|
| `id` | Module 고유 식별자. 안정적(stable)이어야 교체의 기준이 된다. | `workflow-provider` (역할·계약 기반 안정 식별자 — DP-W1; §3·§5 참조) | 예 |
| `contract` | 이 Module이 구현하는 계약(Port/Interface) 식별자. 교체는 동일 `contract` 내에서만 성립한다. | `WorkflowInterface` (DP-W1 — §3·§5 참조) | 예 |
| `version` | Module 버전. | `0.1.0` (이 Provider Module 자체 버전 — §3 참조) | 예 |
| `requires` | 의존하는 contract id 목록. Resolve 시 모두 해소되어야 한다. | `LoopInterface` (병합은 각 Task의 사이클 구동 완결(Verify 게이트)을 요구 — 03 §2·07 §3.1-C·INV-5; DP-W2; §3·§5 참조) | 아니오(기본 없음) |
| `entrypoint` | 실행 진입점의 추상 참조. 구체 바인딩은 01 §4가 해소한다. | 추상 참조 — 분해(Decompose)·디스패치(Dispatch)·병합(Merge) 연산(07 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4). | 예 |
| `configSchema` | 이 Module의 Config 스키마. | 선언하지 않음 (생략 — DP-W3, §3·§5 참조) | 아니오 |
| `replaceable` | 교체 가능 여부. 기본 `true` (ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 기본 `true` (생략 — §3 참조) | 아니오(기본 true) |

주:

- **필수/선택 표기는 정본 그대로 보존한다.** `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기를 복제한다 — 누락되면 계약 변경으로 읽힌다. `requires`는 **선택 필드(기본 없음)**이며, 이 Provider는 그 선택 필드에 값(`LoopInterface`)을 **채운** 것이다 — 필드의 필수/선택 지위를 바꾸지 않는다.
- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true).
- 상세 필드 계약의 정본은 01 §3.2-A가, 형식 작성 지침은 framework/runtime/module-manifest.md가 유지한다. 이 표는 값 인스턴스이며 계약의 진위 판정 기준이 아니다.

---

## §3. 필드별 인스턴스 값·근거

각 필드의 값 선택 근거다. 값은 이 Provider의 인스턴스이며, 필드 계약은 재정의하지 않는다.

### `id` = `workflow-provider` (필수)

- 근거: 역할·계약에 기반한 **안정 식별자**. 구현 세부(버전·환경·오케스트레이션 방식)를 인코딩하지 않는다 (framework/runtime/module-manifest.md §3 `id`, 01 INV-7). 구현이 교체돼도 이 `id`는 유지되어 교체(Replace)의 기준이 된다. 명명은 Advisor 결정 DP-W1로 확정하며(§5), 관례 정본(framework/memory/module-manifest.md §3 `id`=`memory-service-provider`, framework/verifier/module-manifest.md §3 `id`=`verifier-provider`, framework/loop/module-manifest.md §3 `id`=`loop-provider`)과 **동형**으로 역할명(Glossary 표제어 "Workflow") + 관례 접미 `-provider`를 조합한 값이다.
- 회피: 오케스트레이션 방식·리비전·마일스톤 어휘를 `id`에 섞지 않는다 — 그러면 교체마다 `id`가 바뀌어 안정 기준(INV-7)이 무너진다.
- 결정 기록: §5 DP-W1(명명) + "Advisor 확인 — 인스턴스 값"(승인).

### `contract` = `WorkflowInterface` (필수)

- 근거: 이 Provider가 구현하는 **오케스트레이션 계약(Port/Interface)** 식별자다. Advisor 결정 DP-W1로 확정한다(§5). 구현·오케스트레이션 방식이 다른 새 Provider로 교체(Replace)해도 동일 `contract` 내이므로, 이 계약의 소비자(스택상 Workflow Layer 위의 Presentation 진입점 등 — 07 §2)의 참조는 그대로다 (01 INV-1, §8 예1 동형). 이 계약이 노출하는 분해·디스패치·병합 규칙·데이터 포맷의 정본은 07 §3이 유지한다.
- 회피: 특정 구현·오케스트레이션 방식을 `contract`에 섞지 않는다 — 동일 contract 교체(INV-1)가 불가능해진다.
- 결정 기록: §5 DP-W1.

### `version` = `0.1.0` (필수)

- 근거: 이 **Provider Module 자체의 버전**을 가리키는 고정된 버전 문자열이다 (framework/runtime/module-manifest.md §3 `version` — 같은 문자열은 항상 같은 Module 버전). Framework/Spec 버전(현재 v0.7 마일스톤)과는 **별개의 축**이며, Provider 구현이 갱신되면 이 값이 상승한다. 초기 인스턴스 값으로 `0.1.0`을 둔다 (framework/memory/·verifier/·loop/module-manifest.md 관례 동형 — Provider Module 버전은 독립 축, 초기 `0.1.0`).
- 회피: 시점에 따라 대상이 달라지는 비고정 라벨을 쓰지 않는다 — 버전으로서 안정 참조가 되지 못한다.
- 확인 기록: §5 "Advisor 확인 — 인스턴스 값"(승인).

### `requires` = `LoopInterface` (선택 — 기본 없음; 이 Provider는 값을 채움)

- 근거: 이 Provider가 구현하는 세 연산 중 **병합(Merge, 07 §3.1-C)은 "완료·검증된 Task 결과"만 병합 대상으로 삼는다** (07 INV-5 — 검증 후 병합: "각 Task 결과는 개별 검증을 통과한 뒤에만 병합 대상이 된다"). 각 Task 결과가 개별 검증(Verify 게이트)을 통과하려면 그 Task의 Agent Lifecycle 한 사이클이 구동·완결되어야 하며, 그 **단일 사이클 구동 계약**이 `LoopInterface`다. Workflow의 다중 사이클 오케스트레이션은 03의 사이클 구동 계약의 **소비자**다 (03 §2 dependents — "단일 사이클 구동은 Loop, 다중 사이클 오케스트레이션은 Workflow"; 07 §9 결정 기록 — "Decompose·Dispatch·Merge는 다중 사이클 오케스트레이션으로 03의 단일 사이클 밖"). 즉 각 Task의 사이클 구동 완결 없이는 병합 완료 조건(07 §3.1-C·INV-5)이 성립할 수 없다 = **계약적 필수 의존**. `requires`는 "의존하는 contract id 목록 — Resolve 시 모두 해소되어야 한다"(01 §3.2-A)이므로, 이 불가피 의존을 `LoopInterface`로 선언한다.
- **module id가 아니라 contract id를 나열한다** (framework/runtime/module-manifest.md §3 `requires`). `LoopInterface`는 Loop Provider Module(`id`=`loop-provider`, framework/loop/module-manifest.md)이 구현하는 **확정된 기존 contract id**이며, 이 Manifest가 신설하는 값이 아니다. 계약에 의존하므로 Loop 구현이 다른 Provider로 교체(01 §8 예1)돼도 이 Manifest의 `requires` 참조는 유지된다 (01 INV-1).
- **Memory 제외 — Verifier 선례(`requires`=없음)와의 사실 관계 동형.** Workflow도 Memory 소비자이나(07 §5·INV-7), 그 회수(Recall)는 07 §5가 **"필요할 때만"** 최소 범위로 규정한 선택적 보강이고, 기록(Record)도 "…중 다음 사이클에 필요한 것"으로 조건부 소비다. 어느 것도 분해·디스패치·병합 연산의 완료 조건(07 §3.1)을 게이트하지 않는다. 이는 framework/verifier/module-manifest.md §3이 `requires`=없음을 택한 것과 **사실 관계가 동형**이다 — Verifier의 Memory 회수도 06 §5 "필요할 때만"의 선택적 보강이라 판정 연산의 Resolve를 게이트하지 않아 `requires`에 넣지 않았다. 따라서 Workflow도 Memory를 hard `requires`로 선언하지 않는다. 단 접근 시 단일 Port 경유(07 INV-7)는 불변이며, 그 물리 배선은 Adapter Binding 문서 소관이다 (01 §4, 07 §4.1).
- **Loop 선례(`requires`=`MemoryServiceInterface`)와의 사실 관계 차이.** framework/loop/module-manifest.md §3은 Memory를 hard `requires`로 선언했다 — Loop의 Memory Update는 03 INV-5(Learn 불가피성)로 **모든 사이클에서 실행**되는 불가피 의존이기 때문이다. Workflow의 불가피 의존은 Memory가 아니라 `LoopInterface`다 — Workflow의 병합 완료(07 INV-5)를 게이트하는 것은 각 Task의 사이클 구동 완결(03의 계약)이지 Workflow 자신의 Memory 접근이 아니다. 세 Provider의 `requires`는 각자의 연산 완료 조건이 무엇을 **불가피하게** 요구하는가에 따라 갈린다 — Loop=`MemoryServiceInterface`(모든 사이클 Learn → Memory Update, 03 INV-5), Verifier=없음(판정은 산출물 자체 근거, 06 §3.1·INV-1), Workflow=`LoopInterface`(병합은 각 Task의 Verify 게이트 통과 요구, 07 §3.1-C·INV-5).
- **역할 실행(Worker/Verifier/Advisor) 제외.** 디스패치(Dispatch, 07 §3.1-B)가 각 Task를 서로 다른 Agent에게 전달하는 것은 위임·보고 메시지(02 §3.2-B/C/D) 흐름의 **역할 디스패치**이며(07 §4.1이 02 §4.1 위임 메커니즘을 재사용), Runtime의 module Resolve가 아니다. 그 물리 실현 채널은 Adapter Binding 문서 소관이다 (01 §4, 07 §4.1). 따라서 역할 실행은 이 Manifest의 `requires`(= Runtime이 Resolve로 해소하는 계약 의존 목록)에 포함하지 않는다 — 이는 framework/loop/module-manifest.md §3 `requires`가 역할 실행(CP1~CP3)을 requires에서 제외한 것과 동형이다.
- **INV-2와의 정합.** `LoopInterface`를 hard `requires`로 선언하면 Workflow Provider가 Resolve될 때 Loop 바인딩이 함께 해소되어야 한다 (01 §3.1-A Resolve 완료 조건). 이는 01 INV-2(단독 사용 — 필수 계약만 해소되면 부분 집합으로 기동)를 위반하지 않는다. INV-2는 **Runtime이 필수 계약 집합만으로 기동**할 수 있음을 보장하는 규칙이고, 이 `requires`는 Workflow Provider가 활성일 때 Loop를 그 의존 집합에 포함시킬 뿐이다. Workflow의 병합이 각 Task의 사이클 구동 완결에 불가피하게 의존(07 INV-5·03의 계약)하는 이상, 이 의존은 선택적 보강이 아니라 계약적 필수다.
- 회피: 존재하지 않는 contract id를 여기서 **신설·추측하지 않는다** (Glossary 밖 새 용어 금지, 07 §3 재정의 금지). `LoopInterface`는 framework/loop/module-manifest.md가 확정한 기존 contract 값이며 신조어가 아니다. 물리 바인딩이 추가 Adapter contract 의존을 도입한다면 그 선언은 Adapter Binding 문서가 소유한다 (01 §4, 07 §4.1) — 이 Core 서술자가 아니다.
- 결정 기록: §5 DP-W2.

### `entrypoint` = 추상 참조 (필수)

- 근거: 이 Module의 활성화 진입 — 큰 작업을 작업 그래프로 분해하고(Decompose), 병렬 집합을 여러 Agent에게 디스패치하며(Dispatch), 완료·검증된 결과를 병합하는(Merge) 세 연산(07 §3.1)을 노출하는 논리적 진입점을 가리키는 **추상 참조**다. 구체 바인딩(직렬화·물리 경로·호출 규약·역할 실행 채널·병합 중재 진입점 배선)은 기입하지 않는다. 상세는 §4.
- 회피: 특정 실행 환경의 물리 경로·형식별 로케이터를 Manifest에 직접 기입하지 않는다 — 환경 의존을 Core 서술자에 하드코딩하면 이식 시 서술자가 함께 바뀌어 AI·환경 비의존(01 INV-4, 07 INV-9)이 깨진다.

### `configSchema` = 선언하지 않음 (선택)

- 근거 (Advisor 결정 DP-W3, §5): 07 §3 Core Contract에는 이 Provider가 소비하는 **Config 의존 값이 없다** — 분해·디스패치·병합 연산(07 §3.1)의 어느 완료 조건도 Config 키를 소비 지점으로 요구하지 않는다. 소비 값 자체가 부재하므로 이 Manifest는 `configSchema`를 **선언하지 않는다**(01 §3.2-A 선택 필드). 이는 framework/verifier/module-manifest.md §5 DP-V2(소비 Config 값 부재)와 **동형의 생략**이며, framework/loop/module-manifest.md §5 DP-L2와는 **근거가 다르다**(§5 DP-W3에 구분 서술).
- 회피: 소비 지점이 없는 Config 키를 이 Manifest의 자기 Module `configSchema`로 창설하지 않는다 — `configSchema`는 자기 Module 네임스페이스에 국한된 설정이고(framework/runtime/module-manifest.md §3 `configSchema`), 소비 값이 없는데 스키마를 두면 07 §3 계약에 없는 소비 지점을 우회 창설하는 것이 된다.
- 결정 기록: §5 DP-W3.

### `replaceable` = 기본 `true` (선택 — 기본 true)

- 근거: 생략하여 기본값 `true`를 취한다. 모든 Module은 교체 가능이 기본이다 (01 INV-1, ARCHITECTURE 3.2). 큰 작업을 오케스트레이션하는 실행 단위도 Runtime이 호스팅하는 하나의 Module이므로 동일 `contract` 내 교체가 성립해야 한다. 이 Provider에는 교체 불가의 근거가 없다.
- 회피: 근거 없는 `false`를 두지 않는다 — `false`는 근거를 요구하는 명시적 예외다 (01 INV-1).

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider Module의 활성화 진입을 가리키는 **추상(논리) 참조**다. 그것이 노출하는 것은 오케스트레이션 세 연산(07 §3.1) — 큰 작업 1건을 작업 그래프로 분해하고, 병렬 집합을 여러 Agent에게 디스패치하며, 완료·검증된 결과를 병합·충돌 처리하는 연산 — 이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩 — 직렬화 형식, 물리 경로·로케이터, 호출 규약, 병렬 디스패치·위임 메시지 전달 채널, 결과 회수·충돌 중재 진입점 배선 — 은 전부 **Adapter Binding 문서 소관**이다 (01 §4, 07 §4.1). 이 Core 서술자에는 그 어떤 물리 경로·형식 토큰도 하드코딩하지 않는다 (framework/runtime/module-manifest.md §3 `entrypoint` 회피 규칙 정합).
- 이 분리로 실행 환경 이식·교체(01 §8 예1, 07 §4.2 이식 교체 지점) 시에도 이 Manifest의 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고, 물리 바인딩만 Adapter 경계에서 교체된다.
- `requires`가 참조하는 `LoopInterface`의 물리 실현 역시 Adapter 소관이다 — Workflow가 병렬 Task 각각에 대해 소비하는 사이클 구동 계약의 물리 배선은 07 §4.1의 병렬 디스패치·위임 메시지 전달 행이 지정하는 Adapter 경계에서 해소된다. 이 Core 서술자는 그 의존 대상 contract id를 `requires`로 선언할 뿐, 물리 배선을 기입하지 않는다. 마찬가지로 역할 디스패치 채널(07 §4.1의 02 §4.1 재사용)과 충돌 중재 진입점(07 §4.1)의 물리 실현도 Adapter Binding 문서 소관이다.

---

## §5. 결정 기록 (Advisor 결정 — DP-W1·DP-W2·DP-W3 + Advisor 확인)

이 절은 이 Manifest에 반영된 Advisor 결정 3건(DP-W1·DP-W2·DP-W3)과 인스턴스 값 확인(`id`·`version`)을 기록한다. 세 결정은 위임의 확정 입력이며, 본 문서는 이를 그대로 반영한다(임의 변경 없음). 인스턴스 값 확인은 새 결정이 아니라, 관례·정본 근거로 채운 값에 대한 Advisor 승인이다.

### DP-W1 — `contract` = `WorkflowInterface`, `id` = `workflow-provider`

- **결정:** 이 Provider가 구현하는 오케스트레이션 계약 식별자를 `WorkflowInterface`로, Module 고유 식별자를 `workflow-provider`로 확정한다.
- **근거:** 저장소에 이 계약·식별자의 **사전 명명이 없다**(Advisor 실측 2026-07-06 — `WorkflowInterface`/`WorkflowPort`/`workflow-provider` 저장소 전역 0건. 작성 시점 재확인: 전역 검색 0건). Memory 선례의 contract `MemoryServiceInterface`는 01 §8 예1이 사전 명명했으나, Workflow에는 그런 대응물이 부재하다(Verifier의 `VerifierInterface`·Loop의 `LoopInterface`도 사전 명명 부재였던 DP-V1·DP-L1과 동형 상황). 따라서 이 명명은 Advisor의 결정 사안이며, Glossary 정본 어휘 **"Workflow"**(Core Component 표제어 "Workflow (Component)", Glossary §3.2-D, 정본 specs/07-workflow.md)에 Manifest 관례 접미 **"Interface"**(Port/Interface 계약 식별자 관례, 01 §3.2-A)·**"-provider"**(역할명 + 관례 접미, framework/memory/·verifier/·loop/module-manifest.md 동형)를 조합해 확정했다. 이는 **신조어 창설이 아니라** 기존 정본 어휘 + 관례 접미의 조합이며, Memory 선례(`MemoryServiceInterface`)·Verifier 선례(`VerifierInterface`)·Loop 선례(`LoopInterface`)와 동형이다.
- **마일스톤·오케스트레이션 방식 어휘 배제:** Glossary 설명문·ROADMAP 마일스톤이 "오케스트레이션"·마일스톤 어휘를 쓰나, contract·id 식별자는 Glossary 표제어 "Workflow"만 취하고 마일스톤·버전 계열·오케스트레이션 방식 어휘를 안정 식별자에 인코딩하지 않는다(안정 식별자 규칙 — framework/runtime/module-manifest.md §3 `id`/`contract`, 01 INV-7).
- **경계:** `WorkflowInterface`는 이 Manifest의 `contract` 필드 **값(식별자)**이지 Glossary 표제어의 신설이 아니다(§0, §6 — DP-L1·DP-V1 동형 경계 문구). 마찬가지로 `workflow-provider`는 `id` 필드 값이지 새 용어가 아니다. 이 값이 노출하는 분해·디스패치·병합 계약의 정본은 07 §3이 유지하며, 이 Manifest는 그 계약을 재정의하지 않는다.

### DP-W2 — `requires` = `LoopInterface` (단독)

- **결정:** 이 Manifest의 `requires`에 `LoopInterface`를 단독으로 선언한다(01 §3.2-A 선택 필드에 값을 채움).
- **근거:** Workflow의 다중 사이클 오케스트레이션은 03의 사이클 구동 계약의 **소비자**다(03 §2 dependents, 07 §9 결정 기록). 병합(Merge)의 완료 조건은 "완료·검증된 Task 결과"만 병합하는 것이며(07 §3.1-C·INV-5), 각 Task의 사이클 구동 완결(Verify 게이트 통과) 없이는 성립할 수 없다 = 계약적 필수 의존. `LoopInterface`는 framework/loop/module-manifest.md가 확정한 **기존 contract id**(신설 아님)이며, 계약 의존이므로 Loop 구현 교체에도 이 참조는 유지된다(01 INV-1).
- **Memory 제외 (Verifier 선례와 동형):** Workflow의 Memory 소비(07 §5)는 Recall "필요할 때만"·Record 조건부의 선택적 보강이며 연산 완료 조건을 게이트하지 않는다. 이는 framework/verifier/module-manifest.md §3의 `requires`=없음(Memory 회수는 06 §5 "필요할 때만"의 선택적 보강이라 Resolve 비게이트)과 **사실 관계 동형**이다. 단 접근 시 단일 Port 경유(07 INV-7)는 불변이며, 물리 배선은 Adapter Binding 문서 소관이다(01 §4, 07 §4.1).
- **Loop 선례와의 사실 관계 차이:** framework/loop/module-manifest.md §3은 `requires`=`MemoryServiceInterface`를 선언했다 — Loop의 Memory Update는 모든 사이클에서 실행되는 불가피 의존(03 INV-5)이기 때문이다. Workflow의 불가피 의존은 Memory가 아니라 `LoopInterface`이며(병합을 게이트하는 것은 각 Task의 사이클 구동 완결), 이 사실 관계 차이로 두 Provider의 `requires` 값이 갈린다.
- **역할 실행 제외:** 디스패치의 Agent 전달은 위임·보고 메시지 흐름의 역할 디스패치(02 §4.1, 07 §4.1 재사용)이지 Runtime module Resolve가 아니므로 `requires`에 넣지 않는다(framework/loop/module-manifest.md §3 requires 주 동형). 물리 실현은 Adapter Binding 문서 소관이다(01 §4, 07 §4.1).
- **경계:** `LoopInterface`는 이 Manifest의 `requires` 필드 값(기존 contract id 참조)이지 새 계약의 신설이 아니다. 이 값이 노출하는 사이클 구동 계약의 정본은 03 §3이 유지한다.

### DP-W3 — `configSchema` 생략

- **결정:** 이 Manifest는 `configSchema`를 **선언하지 않는다**(01 §3.2-A 선택 필드).
- **근거:** 07 §3에 Workflow가 소유·소비하는 Config 값의 소비 지점이 **부재**하다 — 분해·디스패치·병합 연산(07 §3.1)의 어느 완료 조건도 Config 키를 요구하지 않는다. 소비 값 자체가 없으므로 선언할 스키마가 없다.
- **선례와의 근거 구분:** 이는 framework/verifier/module-manifest.md §5 DP-V2(소비 Config 값 자체 부재)와 **동형의 생략**이다. framework/loop/module-manifest.md §5 DP-L2와는 근거가 다르다 — Loop는 소비 값(`retry.limit`)은 **있으나** 그 소유가 Framework 수준(framework/core/config-schema.md §7)에 이미 있어 값 이중화를 피하려 생략했고, Workflow는 소비 값 **자체가 없어서** 생략한다.
- **명기:** `configSchema` 생략(01 §3.2-A 선택 필드). 향후 물리 바인딩이 Config 소비를 도입한다면 그 선언 소재는 Adapter Binding 문서 또는 Framework 수준 config 소유 문서 소관이며(01 §3.2-B·§4), 이 Core 서술자가 아니다.

### Advisor 확인 — `id`·`version` 인스턴스 값 (2026-07-06)

- **성격:** 이 항목은 두 인스턴스 값(`id`·`version`)에 대한 Advisor **확인(승인)** 기록이다. `id`(=`workflow-provider`)는 DP-W1의 명명 결정으로 확정된 값이고, `version`(=`0.1.0`)은 명시 DP 없이 Manifest 인스턴스 관례로 채운 값이다. 두 값 모두 Advisor 확인으로 승인되었으며, 미확정 잔여가 없다(§3·§6·§9 정합).
- **`id` = `workflow-provider` 승인:** DP-W1 명명 근거(Glossary 표제어 "Workflow" + 관례 접미 "-provider")에 따라 확정되었고, Manifest 인스턴스 관례(framework/memory/·verifier/·loop/module-manifest.md §3 `id`=`memory-service-provider`·`verifier-provider`·`loop-provider`)와 동형이며 01 INV-7 안정 식별자 요건을 충족한다.
- **`version` = `0.1.0` 승인:** Provider Module 자체 버전을 가리키는 고정 버전 문자열이며, Framework/Spec 버전(현재 v0.7 마일스톤)과 **독립 축**이다(framework/memory/·verifier/·loop/module-manifest.md 관례 동형 — 초기 `0.1.0`, Provider 구현 갱신 시 상승).

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- **재정의·확장 0.** 본 문서의 7필드는 01 §3.2-A의 인스턴스다. 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A(필드 계약)와 framework/runtime/module-manifest.md(형식 규격)다. 이 Provider가 구현하는 오케스트레이션 계약(07 §3 분해·디스패치·병합 연산·데이터 포맷·불변 규칙)도 **재정의하지 않고** § 포인터로만 참조했다. 필수/선택 표기(`requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)")를 정본 그대로 보존했고, `requires`의 선택 지위를 바꾸지 않은 채 값만 채웠으며, 새 필드를 추가하지 않았다.
- **금지 토큰 0 (자가 전수 스캔).** 본문·표·예시 전체를 다음 후보 집합 **전체**로 전수 스캔하여 0건임을 확인했다 (framework/core/structure.md §5 C-3 확장, 단일 토큰 검색에 국한하지 않음) — { 특정 AI 이름·모델명·제품 기능명 } ∪ { 특정 프로그래밍 언어명·툴체인명·직렬화 형식명·환경 경로 토큰 }. 진입점·역할 실행 채널·병합 중재·Memory 배선의 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관 (01 §4, 07 §4.1)" 포인터를 두었고, 특정 Adapter Binding 문서명·물리 경로도 인용하지 않았다 (mention/use 경계 — 금지 토큰의 예시도 누출이다). `id`·`contract`·`requires` 값(`workflow-provider`·`WorkflowInterface`·`LoopInterface`)은 계약 **필드 값**이지 금지 토큰이 아니다.
- **새 계약·용어 0.** `requires`에서 존재하지 않는 contract를 신설하지 않았다 — `LoopInterface`는 framework/loop/module-manifest.md가 확정한 기존 contract 값이다. Glossary 밖 새 용어를 만들지 않았다. `WorkflowInterface`는 `contract` 필드의 식별자 **값**이며 Glossary 표제어의 신설이 아니다 — Glossary 정본 어휘 "Workflow" + 관례 접미 "Interface"의 조합으로 Advisor가 확정했다(§5 DP-W1).
- **미완성 형제 산출물 비인용 (07 R2).** 같은 마일스톤에서 동시 작성 중일 수 있는 형제 산출물(예: Work Graph·Task 정의 포맷 인스턴스 문서 등)은 추측·인용하지 않았다. 본 문서는 확정 정본(01·03·07 spec)과 기존 Baseline(framework/runtime/·memory/·verifier/·loop/·core/ 문서)만 참조했다.
- **설계 확정(Advisor).** `contract`·`id` 명명(DP-W1)·`requires` 값(DP-W2)·`configSchema` 생략(DP-W3)은 Advisor 결정으로 확정되어 §2·§3·§5에 반영했다. `id`(=`workflow-provider`)·`version`(=`0.1.0`) 인스턴스 값은 Advisor 확인으로 승인되었다(§5 "Advisor 확인 — 인스턴스 값"). 미확정·open 잔여는 없다.

---

## §7. 요약 (한눈에 보기)

- 이 문서 = **Workflow Provider Module**의 등록 서술자(Manifest) **인스턴스**. 필드 계약 정본 = 01 §3.2-A, 형식 규격 = framework/runtime/module-manifest.md, 오케스트레이션 계약 정본 = 07 §3 (본 문서는 값 인스턴스, 재정의 아님 — C-1).
- 7필드 값: `id`=`workflow-provider`(DP-W1) · `contract`=`WorkflowInterface`(DP-W1) · `version`=`0.1.0`(Provider 자체 버전, 독립 축 — Advisor 확인) · `requires`=`LoopInterface`(DP-W2 — 병합은 각 Task의 사이클 구동 완결을 요구; 03 §2·07 §3.1-C·INV-5) · `entrypoint`=추상 참조(분해·디스패치·병합 연산 07 §3.1 노출, 물리 해소 Adapter 소관) · `configSchema`=선언하지 않음(DP-W3 — 소비 Config 값 부재, Verifier DP-V2 동형·Loop DP-L2와 근거 상이) · `replaceable`=기본 true.
- 필수 4(`id`·`contract`·`version`·`entrypoint`) / 선택 3(`requires`·`configSchema`·`replaceable`) — 필수/선택 표기 정본 그대로. `requires`는 선택 필드이되 이 Provider가 값을 채운 경우다.
- `requires`가 세 Provider에서 갈리는 이유(연산 완료 조건의 불가피 요구 대상): Loop=`MemoryServiceInterface`(모든 사이클 Learn → Memory Update, 03 INV-5) · Verifier=없음(판정은 산출물 자체 근거, 06 §3.1·INV-1) · Workflow=`LoopInterface`(병합은 각 Task의 Verify 게이트 통과 요구, 07 §3.1-C·INV-5). Workflow의 Memory 소비는 Verifier 선례와 동형으로 조건부 보강이라 `requires`에 넣지 않고, 역할 실행은 역할 디스패치(02 §4.1)로 module Resolve가 아니므로 넣지 않는다.
- 이 Manifest는 Runtime Register(01 §3.1-A, module-registry.md §2.1)의 입력이며, 구현하는 오케스트레이션 계약은 07 §3.
- 물리 진입점·직렬화·역할 실행 채널·병합 중재·Memory 배선은 Adapter Binding 문서 소관 (01 §4, 07 §4.1). Module 구현 디렉터리 문서 본문에는 그 토큰이 0건이다 (C-3 확장).
