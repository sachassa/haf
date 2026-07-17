# framework/memory/module-manifest — Memory Service Provider Module Manifest 인스턴스

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드(`id`/`contract`/`version`/`requires`/`entrypoint`/`configSchema`/`replaceable`). 본 문서가 채우는 서술자 계약의 정본. 필드명·의미·필수/선택 표기의 진위 판정 기준은 이 §가 유지한다.
- specs/01-runtime.md §8 예1 — contract id `MemoryServiceInterface`. 이 Manifest의 `contract` 값 정합 기준(동일 contract 백엔드 스왑 예시).
- specs/01-runtime.md §3.3 INV-7 — 안정 식별자(`id`·`contract` id 안정성). §3.3 INV-1 — 교체 가능(`replaceable` 기본값 근거).
- specs/01-runtime.md §4 — Adapter Binding(구체 직렬화·물리 진입점 해소 소관). 본 문서는 § 포인터로만 참조한다.
- specs/04-memory.md §3·§4.1 — Memory Service Interface(단일 Port) 계약과 그 Provider Module 등록. `contract = MemoryServiceInterface`, 영속성 백엔드는 Port 뒤 Adapter Layer(04 §4.1, INV-8).
- framework/runtime/module-manifest.md — Module Manifest **형식 규격**(7필드 작성 지침·안정 식별자 규칙·언어 중립 시그니처). 본 문서는 그 형식을 이 Provider에 대해 채운 **인스턴스**다 (작성 관례).
- framework/runtime/module-registry.md §2.1 — Register 연산(이 Manifest가 입력이 되는 등록 운용). § 포인터로만 참조한다.
- framework/memory/memory-service.md — 이 Provider가 구현하는 Port 계약 인스턴스(자매 문서, 동일 Task M2 산출물).
- framework/core/structure.md §2·§5 — Module 구현 디렉터리 경계(자기완결, C-3 확장 — 문서 본문 비의존), 금지 토큰 규칙.

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인·직렬화 형식 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. Memory Service Provider Module의 01 §3.2-A 7필드 인스턴스(`id`·`contract`=`MemoryServiceInterface`·`version`·`requires`·`entrypoint`·`configSchema`·`replaceable`), 필드별 인스턴스 값·근거, entrypoint 추상 참조 + 물리 해소 Adapter Binding 소관 포인터(물리 경로·형식 하드코딩 0), 필수/선택 표기 정본 대조 보존. 01 §3.2-A 계약 재정의·확장 0, 금지 토큰 0, Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task M2) |
| 2026-07-05 | v0.4 Draft (r2) | Advisor 재작업 지시 반영. (1) `configSchema` 생략 → 선언: 자기 Module 네임스페이스 키 `recall.limit.max`(유한 양의 정수, 기본 20) — Recall 시스템 상한 값 원천(Advisor 결정 DP-M1). (2) `version` 서술을 확정형으로 갱신(Advisor 승인 — Framework/Spec 버전과 독립 축, 초기 0.1.0, Provider 구현 갱신 시 상승). §2 표·§3·§5·§6의 동일 서술을 전수 확정형으로 갱신(확정 대기 잔여 0). 스키마 표기는 계약 수준(추상) — 구체 직렬화는 Adapter 소관 유지. | Worker (Advisor 재작업 지시, Task M2 r2) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **필드 계약의 정본은 specs/01-runtime.md §3.2-A이다.** 이 문서는 그 Module Manifest 계약을 **Memory Service Provider Module에 대해 채운 인스턴스**이며, 필드·의미·필수/선택 표기를 **재정의·확장하지 않는다** (framework/core/structure.md §7 확정 조건 C-1). 필드 계약 요소는 01 §3.2-A를 § 포인터로 참조한다.
- **형식 규격의 정본은 framework/runtime/module-manifest.md이다.** 그 문서는 임의 Manifest를 **어떻게 작성·판독하는가**(7필드 형식·안정 식별자 규칙)를 규율하고, 이 문서는 그 형식을 이 Provider 하나에 대해 **구체 값으로 채운** 등록 서술자다. 두 문서 모두 01 §3.2-A를 진위 판정 기준으로 삼는다.
- **이 문서는 Module 구현 디렉터리 문서다** (framework/core/structure.md §2 — 각 Module의 Manifest를 자기 경계에 두는 자기완결 단위, 01 §3.2-E 규칙 2). 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (framework/core/structure.md §5 C-3 확장, 01 §3.3 INV-4). 구체 직렬화·물리 진입점 해소·환경 경로 관례는 **Adapter Binding 문서 소관**이며 (01 §4, 04 §4.1), 필요한 자리에는 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Module / Module Manifest / 모듈 시스템 / Runtime Context는 Glossary §3.2-I가 정본이다. 새 용어를 정본처럼 신설하지 않는다.
- 필드명 백틱 표기(`id` 등)와 예시 식별자는 특정 언어·직렬화 형식의 문법이 아니라, 정본 01 §3.2-A가 쓰는 필드명·서술 라벨을 그대로 인용한 것이다.

---

## §1. 목적

이 문서는 **Memory Service Provider Module**의 등록 서술자(Module Manifest)다. Memory Service Provider는 contract `MemoryServiceInterface`(단일 Port)를 구현하는 Module이며, Runtime이 이를 등록·해소·교체한다 (04 §4.1, 01 §3.1-A·§8 예1).

이 규격의 책임은 두 가지다.

- 01 §3.2-A의 7필드를 이 Provider에 대한 **구체 값**으로 채운다 — `contract`는 `MemoryServiceInterface`로 고정하고(01 §8 예1 정합), `entrypoint`는 추상 참조로 두며 물리 해소는 Adapter Binding 문서 소관으로 미룬다.
- 필드의 필수/선택 표기를 정본 그대로 보존한다 (필수/선택 표기 보존).

이 Manifest는 Runtime의 **Register** 연산(01 §3.1-A, 운용 규칙: framework/runtime/module-registry.md §2.1)의 입력이 된다. 이 Provider가 구현하는 Port 계약의 인스턴스는 자매 문서 framework/memory/memory-service.md다. 각 Module은 자기완결(self-contained) 단위이므로, 이 Manifest는 그 Module의 `id`·`contract`·`entrypoint` 등 자기완결 참조를 한 서술자에 묶는다 (01 §3.2-E 규칙 2).

---

## §2. 7필드 인스턴스 (정본 대조 표)

아래 표는 01 §3.2-A의 7필드를 이 Provider에 대한 값으로 채운 것이다. **필드명·의미·필수/선택 표기는 정본(01 §3.2-A) 그대로**이며, "값 (이 Provider 인스턴스)" 열만 본 문서가 채운다. 필드 계약을 재정의하지 않는다.

| 필드 | 의미 (정본: 01 §3.2-A) | 값 (이 Provider 인스턴스) | 필수 |
|---|---|---|---|
| `id` | Module 고유 식별자. 안정적(stable)이어야 교체의 기준이 된다. | `memory-service-provider` | 예 |
| `contract` | 이 Module이 구현하는 계약(Port/Interface) 식별자. 교체는 동일 `contract` 내에서만 성립한다. | `MemoryServiceInterface` | 예 |
| `version` | Module 버전. | `0.1.0` (이 Provider Module 자체 버전 — §3 참조) | 예 |
| `requires` | 의존하는 contract id 목록. Resolve 시 모두 해소되어야 한다. | 없음 (기본 — §3 참조) | 아니오(기본 없음) |
| `entrypoint` | 실행 진입점의 추상 참조. 구체 바인딩은 01 §4가 해소한다. | 추상 참조 — Record/Recall 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4). | 예 |
| `configSchema` | 이 Module의 Config 스키마. | 선언 — 자기 Module 키 `recall.limit.max`(유한 양의 정수, 기본값 20; Recall 시스템 상한). §3 참조. | 아니오 |
| `replaceable` | 교체 가능 여부. 기본 `true` (ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 기본 `true` (생략 — §3 참조) | 아니오(기본 true) |

주:

- **필수/선택 표기는 정본 그대로 보존한다.** `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기를 복제한다 — 누락되면 계약 변경으로 읽힌다.
- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true).
- 상세 필드 계약의 정본은 01 §3.2-A가, 형식 작성 지침은 framework/runtime/module-manifest.md가 유지한다. 이 표는 값 인스턴스이며 계약의 진위 판정 기준이 아니다.

---

## §3. 필드별 인스턴스 값·근거

각 필드의 값 선택 근거다. 값은 이 Provider의 인스턴스이며, 필드 계약은 재정의하지 않는다.

### `id` = `memory-service-provider` (필수)

- 근거: 역할·계약에 기반한 **안정 식별자**. 구현 세부(버전·환경·백엔드 종류)를 인코딩하지 않는다 (framework/runtime/module-manifest.md §3 `id`, 01 INV-7). 백엔드가 교체돼도(01 §8 예1) 이 `id`는 유지되어 교체의 기준이 된다.
- 회피: 백엔드 종류·리비전을 `id`에 섞지 않는다 — 그러면 교체마다 `id`가 바뀌어 안정 기준(INV-7)이 무너진다.

### `contract` = `MemoryServiceInterface` (필수)

- 근거: 이 Provider가 구현하는 **Port 계약** 식별자. 01 §8 예1과 04 §4.1이 지정한 값으로 고정한다. 저장 백엔드가 다른 새 Provider로 교체(Replace)해도 동일 `contract` 내이므로 계약 소비자(Agent·Loop·Workflow·Verifier)의 참조는 그대로다 (01 INV-1, §8 예1; 소비자 계약은 memory-service.md §7).
- 회피: 특정 구현·백엔드를 `contract`에 섞지 않는다 — 동일 contract 교체(INV-1)가 불가능해진다.

### `version` = `0.1.0` (필수)

- 근거: 이 **Provider Module 자체의 버전**을 가리키는 고정된 버전 문자열이다 (framework/runtime/module-manifest.md §3 `version` — 같은 문자열은 항상 같은 Module 버전). Framework/Spec 버전(v0.4)과는 별개의 축이며, Provider 구현이 갱신되면 이 값이 증가한다. 초기 인스턴스 값으로 `0.1.0`을 둔다.
- 회피: 시점에 따라 대상이 달라지는 비고정 라벨을 쓰지 않는다 — 버전으로서 안정 참조가 되지 못한다.
- 확정 (Advisor 승인, v0.4): Provider Module 버전은 Framework/Spec 버전과 독립 축이며, 초기 `0.1.0`, Provider 구현 갱신 시 상승한다.

### `requires` = 없음 (선택 — 기본 없음)

- 근거: 04 §3 Core Contract는 Memory Service Provider가 의존하는 **다른 named contract**를 선언하지 않는다. 영속성 백엔드는 이 Port 뒤 Adapter Layer에 격리되며(04 INV-8, §4.1), 그 배선은 Adapter Binding 문서 소관이다. 따라서 Core 인스턴스 수준에서 `requires`는 비워 둔다(기본 없음).
- 회피: 존재하지 않는 저장·백엔드 contract id를 여기서 **신설·추측하지 않는다** (Glossary 밖 새 용어 금지, 04 §3 재정의 금지). 물리 바인딩이 백엔드/Adapter contract 의존을 도입한다면 그 선언은 Adapter Binding 문서가 소유한다 (01 §4, 04 §4.1) — 이 Core 서술자가 아니다.

### `entrypoint` = 추상 참조 (필수)

- 근거: 이 Module의 활성화 진입 — Record/Recall(memory-service.md §3)을 노출하는 논리적 진입점 — 을 가리키는 **추상 참조**다. 구체 바인딩(직렬화·물리 경로·호출 규약)은 기입하지 않는다. 상세는 §4.
- 회피: 특정 실행 환경의 물리 경로·형식별 로케이터를 Manifest에 직접 기입하지 않는다 — 환경 의존을 Core 서술자에 하드코딩하면 이식 시 서술자가 함께 바뀌어 AI·환경 비의존(01 INV-4, 04 INV-8)이 깨진다.

### `configSchema` = 선언 (선택 — 자기 Module 네임스페이스)

이 Provider의 Config 스키마를 자기 Module 네임스페이스에 선언한다. Config 계약 정본은 01 §3.2-B이며, `configSchema`는 자기 Module 범위에 국한된다 (framework/runtime/module-manifest.md §3 `configSchema`). 아래 표는 계약 수준(추상) 서술이며, 구체 직렬화 형식·물리 표현은 Adapter Binding 문서 소관이다 (01 §4).

| Config 키 | 의미 | 타입 | 기본값 |
|---|---|---|---|
| `recall.limit.max` | Recall 시스템 상한 — 요청 `limit`의 상한이자 `limit` 미지정 시 적용값 (04 §3.1-B "시스템 상한"의 값 원천; 소비 지점은 memory-service.md §3.2·§4.2). | 유한 양의 정수 | 20 |

- 근거 (Advisor 결정 DP-M1, v0.4): 04는 상한의 **존재**만 규정하고 값 원천은 실현 소관이며, Module scope config(01 §3.2-B)가 그 자리다. 기본 `20`은 v0.1~v0.3 실측 기억 규모에서 단일 회수 20건 초과를 최소 범위 원칙(04 INV-4) 위반 신호로 보는 운용 결정이다. override는 01 §3.2-B 병합 규칙(Module > Project > Global)을 따른다.
- 경계: 이 키는 자기 Module(`memory-service-provider`) 네임스페이스에 국한되며 타 Module 설정을 포함하지 않는다. 스키마는 계약 수준이며 구체 직렬화는 Adapter Binding 문서 소관이다 (01 §4).

### `replaceable` = 기본 `true` (선택 — 기본 true)

- 근거: 생략하여 기본값 `true`를 취한다. 모든 Module은 교체 가능이 기본이다 (01 INV-1, ARCHITECTURE 3.2). 특히 01 §8 예1의 "저장 백엔드가 다른 새 Provider Module로 Replace"가 이 값(교체 가능)에 의존한다.
- 회피: 근거 없는 `false`를 두지 않는다 — `false`는 근거를 요구하는 명시적 예외다 (01 INV-1). 이 Provider는 교체 가능해야 하므로 `false` 근거가 없다.

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider Module의 활성화 진입을 가리키는 **추상(논리) 참조**다. 그것이 노출하는 것은 Memory Service Interface의 두 연산(Record·Recall, memory-service.md §3)이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩 — 직렬화 형식, 물리 경로·로케이터, 호출 규약, 영속성 백엔드 연결 — 은 전부 **Adapter Binding 문서 소관**이다 (01 §4, 04 §4.1). 이 Core 서술자에는 그 어떤 물리 경로·형식 토큰도 하드코딩하지 않는다 (framework/runtime/module-manifest.md §3 `entrypoint` 회피 규칙 정합).
- 이 분리로 백엔드 이식·교체(01 §8 예1, 04 §4.2 이식 교체 지점) 시에도 이 Manifest의 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고, 물리 바인딩만 Adapter 경계에서 교체된다.

---

## §5. 정본 경계·금지 토큰 준수 (self-note)

- **재정의·확장 0.** 본 문서의 7필드는 01 §3.2-A의 인스턴스다. 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A(필드 계약)와 framework/runtime/module-manifest.md(형식 규격)다. 필수/선택 표기(`requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 등)를 정본 그대로 보존했고, 새 필드를 추가하지 않았다.
- **금지 토큰 0.** 본문·표·예시 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명이 0건이다 (framework/core/structure.md §5 C-3 확장). 진입점·백엔드의 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관 (01 §4, 04 §4.1)" 포인터를 둔다 (mention/use 경계 — 금지 토큰의 예시도 누출이다).
- **새 계약·용어 0.** `requires`에서 존재하지 않는 백엔드/저장 contract를 신설하지 않았고, Glossary 밖 새 용어를 만들지 않았다. `contract` 값 `MemoryServiceInterface`는 01 §8 예1·04 §4.1의 인용이다.
- **설계 확정(Advisor).** `version` 부여 관례(Framework/Spec 버전과 독립 축, 초기 `0.1.0`, 구현 갱신 시 상승 — Advisor 승인)와 Recall 시스템 상한의 값 원천(Provider Module Config 키 `recall.limit.max`, 기본 20 — 결정 DP-M1)은 Advisor 결정으로 확정되어 §2·§3에 반영했다. 확정 대기 잔여 0.

---

## §6. 요약 (한눈에 보기)

- 이 문서 = **Memory Service Provider Module**의 등록 서술자(Manifest) **인스턴스**. 필드 계약 정본 = 01 §3.2-A, 형식 규격 = framework/runtime/module-manifest.md (본 문서는 값 인스턴스, 재정의 아님 — C-1).
- 7필드 값: `id`=`memory-service-provider`(안정 식별자) · `contract`=`MemoryServiceInterface`(01 §8 예1·04 §4.1 정합) · `version`=`0.1.0`(Provider 자체 버전, 독립 축 — Advisor 승인) · `requires`=없음(기본) · `entrypoint`=추상 참조(Record/Recall 노출, 물리 해소 Adapter 소관) · `configSchema`=선언(`recall.limit.max`: 유한 양의 정수, 기본 20 — Recall 시스템 상한, 결정 DP-M1) · `replaceable`=기본 true.
- 필수 4(`id`·`contract`·`version`·`entrypoint`) / 선택 3(`requires`·`configSchema`·`replaceable`) — 필수/선택 표기 정본 그대로.
- 이 Manifest는 Runtime Register(01 §3.1-A, module-registry.md §2.1)의 입력이며, 구현하는 Port 계약은 memory-service.md.
- 물리 진입점·직렬화·백엔드는 Adapter Binding 문서 소관 (01 §4, 04 §4.1). Module 구현 디렉터리 문서 본문에는 그 토큰이 0건이다 (C-3 확장).
