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
| 2026-07-26 | (정합) | md 슬림화 Wave 3 — 비계약 격리 개정: 경계 중복·표-산문 이중·감사 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

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

각 필드의 값과 1줄 근거다(§5는 결정 ID·결론만 둔다 — 쌍둥이 서술 제거). 값은 이 Provider의 인스턴스이며 필드 계약은 재정의하지 않는다.

- **`id` = `workflow-provider`** (필수) — 역할·계약 기반 **안정 식별자**(01 INV-7): 구현 세부(버전·환경·오케스트레이션 방식)·마일스톤 어휘를 인코딩하지 않아 교체 기준이 유지된다. 명명 = Glossary 표제어 "Workflow" + 관례 접미 `-provider`(memory/·verifier/·loop/module-manifest 동형). 결정 = §5 DP-W1, Advisor 확인 = §5.
- **`contract` = `WorkflowInterface`** (필수) — 이 Provider가 구현하는 오케스트레이션 계약(Port/Interface) 식별자. 동일 `contract` 내 교체로 소비자 참조가 유지된다(01 INV-1). 계약이 노출하는 분해·디스패치·병합 규칙·데이터 포맷의 정본은 07 §3. 결정 = §5 DP-W1.
- **`version` = `0.1.0`** (필수) — 이 Provider Module 자체 버전의 고정 문자열. Framework/Spec 버전과 **독립 축**이며 구현 갱신 시 상승한다. Advisor 확인 = §5.
- **`requires` = `LoopInterface`** (선택 — 기본 없음; 이 Provider는 값을 채움) — 병합(Merge, 07 §3.1-C)은 "완료·검증된 Task 결과"만 대상으로 삼으므로(07 INV-5) 각 Task의 사이클 구동 완결(Verify 게이트 통과) 없이는 완료 조건이 성립하지 않는다 = **계약적 필수 의존**. Workflow의 다중 사이클 오케스트레이션은 03의 사이클 구동 계약의 소비자다(03 §2 dependents, 07 §9 결정 기록). 결정 = §5 DP-W2.
  - **contract id 나열(module id 아님).** `LoopInterface`는 Loop Provider Module이 구현하는 **확정된 기존 contract id**이며 이 Manifest가 신설하는 값이 아니다. 계약 의존이므로 Loop 구현 교체에도 참조는 유지된다(01 INV-1). 존재하지 않는 contract id를 신설·추측하지 않는다.
  - **세 Provider의 `requires`가 갈리는 기준 = 각 연산 완료 조건이 무엇을 불가피하게 요구하는가.** Loop=`MemoryServiceInterface`(모든 사이클 Learn → Memory Update, 03 INV-5) · Verifier=없음(판정은 산출물 자체 근거, 06 §3.1·INV-1) · Workflow=`LoopInterface`. Workflow의 Memory 소비(07 §5)는 Recall "필요할 때만"·Record 조건부의 선택적 보강이라 연산 완료 조건을 게이트하지 않으므로 hard `requires`에 넣지 않는다(Verifier 선례와 사실 관계 동형). 접근 시 단일 Port 경유(07 INV-7)는 불변이며 물리 배선은 Adapter Binding 소관이다.
  - **역할 실행 제외.** 디스패치의 Agent 전달은 위임·보고 메시지 흐름의 **역할 디스패치**(02 §4.1을 07 §4.1이 재사용)이지 Runtime module Resolve가 아니므로 `requires`에 포함하지 않는다.
  - **INV-2와의 정합.** hard `requires` 선언은 Workflow Provider가 활성일 때 Loop를 그 의존 집합에 포함시킬 뿐이며, Runtime이 필수 계약 집합만으로 기동함을 보장하는 01 INV-2를 위반하지 않는다.
- **`entrypoint` = 추상 참조** (필수) — 분해·디스패치·병합 세 연산(07 §3.1)을 노출하는 논리 진입점. 구체 바인딩(직렬화·물리 경로·호출 규약·역할 실행 채널·병합 중재 진입점 배선)은 기입하지 않는다 — 환경 의존을 Core 서술자에 하드코딩하면 비의존(01 INV-4, 07 INV-9)이 깨진다. 상세 = §4.
- **`configSchema` = 선언하지 않음** (선택) — 07 §3에 이 Provider가 소비하는 Config 값의 소비 지점이 부재하다. 소비 지점 없는 키를 자기 Module 스키마로 창설하지 않는다. 결정 = §5 DP-W3.
- **`replaceable` = 기본 `true`** (선택 — 기본 true) — 교체 가능이 기본이며(01 INV-1) 이 Provider에는 교체 불가의 근거가 없다. 근거 없는 `false`를 두지 않는다.

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider Module의 활성화 진입을 가리키는 **추상(논리) 참조**다. 그것이 노출하는 것은 오케스트레이션 세 연산(07 §3.1) — 큰 작업 1건을 작업 그래프로 분해하고, 병렬 집합을 여러 Agent에게 디스패치하며, 완료·검증된 결과를 병합·충돌 처리하는 연산 — 이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩 — 직렬화 형식, 물리 경로·로케이터, 호출 규약, 병렬 디스패치·위임 메시지 전달 채널, 결과 회수·충돌 중재 진입점 배선 — 은 전부 **Adapter Binding 문서 소관**이다 (01 §4, 07 §4.1). 이 Core 서술자에는 그 어떤 물리 경로·형식 토큰도 하드코딩하지 않는다 (framework/runtime/module-manifest.md §3 `entrypoint` 회피 규칙 정합).
- 이 분리로 실행 환경 이식·교체(01 §8 예1, 07 §4.2 이식 교체 지점) 시에도 이 Manifest의 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고, 물리 바인딩만 Adapter 경계에서 교체된다.
- `requires`가 참조하는 `LoopInterface`의 물리 실현 역시 Adapter 소관이다 — Workflow가 병렬 Task 각각에 대해 소비하는 사이클 구동 계약의 물리 배선은 07 §4.1의 병렬 디스패치·위임 메시지 전달 행이 지정하는 Adapter 경계에서 해소된다. 이 Core 서술자는 그 의존 대상 contract id를 `requires`로 선언할 뿐, 물리 배선을 기입하지 않는다. 마찬가지로 역할 디스패치 채널(07 §4.1의 02 §4.1 재사용)과 충돌 중재 진입점(07 §4.1)의 물리 실현도 Adapter Binding 문서 소관이다.

---

## §5. 결정 기록 (Advisor 결정 — DP-W1·DP-W2·DP-W3 + Advisor 확인)

결정 ID + 결론만 둔다(근거는 §3 필드별 1줄 — 쌍둥이 서술 제거). 세 결정은 위임의 확정 입력이며 본 문서는 이를 그대로 반영한다.

- **DP-W1 — `contract` = `WorkflowInterface`, `id` = `workflow-provider`.** 두 식별자를 이 값으로 확정한다(저장소 사전 명명 부재 → Advisor 결정 사안. Glossary 표제어 "Workflow"(§3.2-D) + 관례 접미 "Interface"·"-provider"의 조합이며 Memory·Verifier·Loop 선례와 동형). 마일스톤·버전 계열·오케스트레이션 방식 어휘는 안정 식별자에 인코딩하지 않는다(01 INV-7). 두 값은 필드 **값(식별자)**이지 Glossary 표제어 신설이 아니다(§0·§6).
- **DP-W2 — `requires` = `LoopInterface` (단독).** 01 §3.2-A 선택 필드에 이 값을 채운다(근거·선례 구분 = §3). `LoopInterface`는 framework/loop/module-manifest.md가 확정한 기존 contract id 참조이지 새 계약의 신설이 아니며, 그 사이클 구동 계약의 정본은 03 §3이 유지한다.
- **DP-W3 — `configSchema` 생략.** 01 §3.2-A 선택 필드로 선언하지 않는다 — 07 §3에 소비 지점이 부재하다. 이는 verifier/module-manifest.md DP-V2(소비 값 자체 부재)와 동형이고 loop/module-manifest.md DP-L2와는 근거가 다르다(Loop는 소비 값이 있으나 소유가 Framework 수준이라 값 이중화를 피해 생략). 향후 물리 바인딩이 Config 소비를 도입하면 그 선언 소재는 Adapter Binding 또는 Framework 수준 config 소유 문서 소관이다(01 §3.2-B·§4).
- **Advisor 확인 — `id`·`version` 인스턴스 값 (2026-07-06).** 두 값이 승인되었다(`id`는 DP-W1 명명 결정으로, `version`은 Manifest 인스턴스 관례로 채운 값). 미확정 잔여 = 없음.

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- **재정의·확장 0.** 본 문서의 7필드는 01 §3.2-A의 인스턴스이며 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A(필드 계약)와 framework/runtime/module-manifest.md(형식 규격)다. 오케스트레이션 계약(07 §3)은 § 포인터로만 참조했다. 필수/선택 표기를 정본 그대로 보존했고, `requires`의 선택 지위를 바꾸지 않은 채 값만 채웠으며 새 필드를 추가하지 않았다.
- **새 계약·용어 0.** `requires`에서 존재하지 않는 contract를 신설하지 않았다(`LoopInterface` = framework/loop/module-manifest.md가 확정한 기존 contract 값). `WorkflowInterface`는 `contract` 필드의 식별자 값이며 Glossary 표제어 신설이 아니다(§5 DP-W1).
- **금지 토큰·Glossary 경계.** 금지 토큰 규칙과 정당 매치 분류(계약 필드 값 `workflow-provider`·`WorkflowInterface`·`LoopInterface` 포함)의 판정 기준은 framework/core/structure.md §5 C-3 확장이 소유한다(01 INV-4, 07 INV-9). 진입점·역할 실행 채널·병합 중재·Memory 배선의 물리 실현이 필요한 자리에는 "Adapter Binding 문서 소관(01 §4, 07 §4.1)" 포인터만 두고 특정 Adapter Binding 문서명·물리 경로를 인용하지 않는다(mention/use 경계).
- **미확정·open 잔여 = 없음.** `contract`·`id` 명명(DP-W1)·`requires` 값(DP-W2)·`configSchema` 생략(DP-W3)은 Advisor 결정, `id`·`version`은 Advisor 확인(2026-07-06)으로 확정되었다(§5).
