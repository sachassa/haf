# framework/memory/module-manifest — Memory Service Provider Module Manifest 인스턴스

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드 계약의 정본(필드명·의미·필수/선택 표기의 진위 판정 기준).
- specs/01-runtime.md §8 예1 — contract id `MemoryServiceInterface`(이 Manifest `contract` 값의 정합 기준).
- specs/01-runtime.md §3.3 INV-7·INV-1 — 안정 식별자·교체 가능(`replaceable` 기본값 근거).
- specs/01-runtime.md §4 — 구체 직렬화·물리 진입점 해소 소관(§4 포인터).
- specs/04-memory.md §3·§4.1 — Memory Service Interface(단일 Port) 계약과 Provider Module 등록·백엔드 격리(INV-8).
- framework/runtime/module-manifest.md — Module Manifest 형식 규격(본 문서는 그 형식의 인스턴스).
- framework/runtime/module-registry.md §2.1 — Register 연산(이 Manifest가 입력).
- framework/memory/memory-service.md — 이 Provider가 구현하는 Port 계약 인스턴스(자매 문서).
- framework/core/structure.md §2·§5 — 소속 경계·금지 토큰 규칙(C-3 확장).

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다(structure.md §2). 본문은 AI·언어·툴체인·직렬화 형식 비의존을 유지한다(structure.md §5 C-3). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. Memory Service Provider Module의 01 §3.2-A 7필드 인스턴스(`id`·`contract`=`MemoryServiceInterface`·`version`·`requires`·`entrypoint`·`configSchema`·`replaceable`), 필드별 인스턴스 값·근거, entrypoint 추상 참조 + 물리 해소 Adapter Binding 소관 포인터(물리 경로·형식 하드코딩 0), 필수/선택 표기 정본 대조 보존. 01 §3.2-A 계약 재정의·확장 0, 금지 토큰 0, Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task M2) |
| 2026-07-05 | v0.4 Draft (r2) | Advisor 재작업 지시 반영. (1) `configSchema` 생략 → 선언: 자기 Module 네임스페이스 키 `recall.limit.max`(유한 양의 정수, 기본 20) — Recall 시스템 상한 값 원천(Advisor 결정 DP-M1). (2) `version` 서술을 확정형으로 갱신(Advisor 승인 — Framework/Spec 버전과 독립 축, 초기 0.1.0, Provider 구현 갱신 시 상승). §2 표·§3·§5·§6의 동일 서술을 전수 확정형으로 갱신(확정 대기 잔여 0). 스키마 표기는 계약 수준(추상) — 구체 직렬화는 Adapter 소관 유지. | Worker (Advisor 재작업 지시, Task M2 r2) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 3 — 비계약 격리 개정: 경계 중복·복제 절 포인터화·감사 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다. uaf-allow-legacy: §9 기존 행은 개정 시점의 이력 기록이므로 문면을 고치지 않고 보존한다.)

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(다른 절에서 반복하지 않는다).

- **필드 계약의 정본은 specs/01-runtime.md §3.2-A다.** 이 문서는 그 계약을 Memory Service Provider Module에 대해 채운 **인스턴스**이며 필드·의미·필수/선택 표기를 재정의·확장하지 않는다(structure.md §7 C-1).
- **형식 규격의 정본은 framework/runtime/module-manifest.md다.** 두 문서 모두 01 §3.2-A를 진위 판정 기준으로 삼는다.
- **Module 구현 디렉터리 문서.** 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명)을 두지 않는다 — 규칙·분류 정본은 structure.md §5 C-3(및 01 §3.3 INV-4)이다. 구체 직렬화·물리 진입점 해소·환경 경로 관례는 Adapter Binding 문서 소관이다(01 §4, 04 §4.1).
- 용어는 specs/00-glossary.md 정본만 사용한다(§3.2-I 등). 필드명 백틱 표기는 01 §3.2-A의 필드명 인용이다.

---

## §1. 목적

이 문서는 **Memory Service Provider Module**의 등록 서술자(Module Manifest)다. Memory Service Provider는 contract `MemoryServiceInterface`(단일 Port)를 구현하며 Runtime이 이를 등록·해소·교체한다(04 §4.1, 01 §3.1-A·§8 예1). 이 Manifest는 Runtime **Register** 연산(01 §3.1-A, 운용 규칙 framework/runtime/module-registry.md §2.1)의 입력이며, 01 §3.2-A 7필드를 구체 값으로 채우고 필수/선택 표기를 정본 그대로 보존한다. 이 Provider가 구현하는 Port 계약의 인스턴스는 자매 문서 framework/memory/memory-service.md다.

---

## §2. 7필드 인스턴스 (값 — 필드 의미의 정본은 01 §3.2-A)

정본 = `uahf/specs/01-runtime.md §3.2-A`(재정의 0 · 필드 의미 문면은 정본 참조). 아래는 값 행만 둔다.

| 필드 | 값 (이 Provider 인스턴스) | 필수 |
|---|---|---|
| `id` | `memory-service-provider` | 예 |
| `contract` | `MemoryServiceInterface` | 예 |
| `version` | `0.1.0` (Provider Module 자체 버전 — 독립 축) | 예 |
| `requires` | 없음 (기본) | 아니오(기본 없음) |
| `entrypoint` | 추상 참조 — Record/Recall 노출 진입점. 물리 해소는 Adapter Binding 소관(§4). | 예 |
| `configSchema` | 선언 — 자기 Module 키 `recall.limit.max`(유한 양의 정수, 기본값 20; Recall 시스템 상한). §3 참조. | 아니오 |
| `replaceable` | 기본 `true` (생략) | 아니오(기본 true) |

- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true). `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기는 정본 표기다.

---

## §3. 필드별 값 근거

- **`id` = `memory-service-provider`** — 역할·계약 기반 안정 식별자로 구현 세부(버전·환경·백엔드 종류)를 인코딩하지 않는다(01 INV-7). 백엔드가 교체돼도(01 §8 예1) 이 `id`는 유지되어 교체의 기준이 된다.
- **`contract` = `MemoryServiceInterface`** — 01 §8 예1·04 §4.1이 지정한 값으로 고정한다. 저장 백엔드가 다른 Provider로 교체돼도 동일 `contract` 내이므로 소비자 참조는 그대로다(01 INV-1; 소비자 계약은 memory-service.md §7). 특정 구현·백엔드를 `contract`에 섞지 않는다.
- **`version` = `0.1.0`** — Provider Module 자체 버전(Advisor 승인 확정, v0.4: Framework/Spec 버전과 독립 축 · 초기 `0.1.0` · 구현 갱신 시 상승). 시점에 따라 대상이 달라지는 비고정 라벨은 쓰지 않는다.
- **`requires` = 없음** — 04 §3 Core Contract는 이 Provider가 의존하는 다른 named contract를 선언하지 않는다. 영속성 백엔드는 Port 뒤 Adapter Layer에 격리되며(04 INV-8·§4.1) 그 배선은 Adapter Binding 소관이므로 Core 인스턴스 수준에서 비워 둔다. 존재하지 않는 백엔드·저장 contract id를 신설·추측하지 않는다.
- **`entrypoint` = 추상 참조** — Record/Recall(memory-service.md §3)을 노출하는 논리 진입점. 물리 경로·형식별 로케이터를 Core 서술자에 기입하지 않는다(01 INV-4, 04 INV-8). 상세는 §4.
- **`replaceable` = 기본 `true`** — 생략하여 기본값을 취한다(01 INV-1). 특히 01 §8 예1의 "저장 백엔드가 다른 새 Provider Module로 Replace"가 이 값에 의존한다. 근거 없는 `false`를 두지 않는다.

### `configSchema` = 선언 (선택 — 자기 Module 네임스페이스)

Config 계약 정본은 01 §3.2-B이며 `configSchema`는 자기 Module 범위에 국한된다. 아래는 계약 수준(추상) 서술이고 구체 직렬화·물리 표현은 Adapter Binding 소관이다(01 §4).

| Config 키 | 의미 | 타입 | 기본값 |
|---|---|---|---|
| `recall.limit.max` | Recall 시스템 상한 — 요청 `limit`의 상한이자 `limit` 미지정 시 적용값 (04 §3.1-B "시스템 상한"의 값 원천; 소비 지점은 memory-service.md §3.2·§4.2). | 유한 양의 정수 | 20 |

- **근거 (Advisor 결정 DP-M1, v0.4).** 04는 상한의 **존재**만 규정하고 값 원천은 실현 소관이며 Module scope config(01 §3.2-B)가 그 자리다. 기본 `20`은 v0.1~v0.3 실측 기억 규모에서 단일 회수 20건 초과를 최소 범위 원칙(04 INV-4) 위반 신호로 보는 운용 결정이다. override는 01 §3.2-B 병합 규칙(Module > Project > Global)을 따른다.
- **경계.** 이 키는 자기 Module(`memory-service-provider`) 네임스페이스에 국한되며 타 Module 설정을 포함하지 않는다.

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider의 활성화 진입을 가리키는 **추상(논리) 참조**이며, 노출하는 것은 Memory Service Interface의 두 연산(Record·Recall, memory-service.md §3)이다.
- **물리 해소는 이 문서 밖이다.** 직렬화 형식·물리 경로·호출 규약·영속성 백엔드 연결은 전부 Adapter Binding 문서 소관이다(01 §4, 04 §4.1). 이 Core 서술자에는 물리 경로·형식 토큰을 하드코딩하지 않는다.
- 이 분리로 백엔드 이식·교체(01 §8 예1, 04 §4.2) 시에도 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고 물리 바인딩만 Adapter 경계에서 교체된다.
