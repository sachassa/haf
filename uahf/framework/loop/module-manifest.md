# framework/loop/module-manifest — Loop Provider Module Manifest 인스턴스

작성일: 2026-07-06
상태: v0.6 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드 계약의 정본(필드명·의미·필수/선택 표기의 진위 판정 기준).
- specs/01-runtime.md §3.3 INV-7·INV-1·INV-2·INV-4 — 안정 식별자·교체 가능·단독 사용·Core AI 비의존.
- specs/01-runtime.md §3.1-A — Register/Resolve 연산(이 Manifest는 Register의 입력).
- specs/01-runtime.md §8 예1 — contract id `MemoryServiceInterface` 사전 명명.
- specs/01-runtime.md §4 — 구체 직렬화·물리 진입점 해소 소관(§4 포인터).
- specs/03-loop.md §3.1 — 사이클 구동 연산(`entrypoint`가 노출하는 논리 진입점 근거).
- specs/03-loop.md §3.1-A(6)·§5·§3.3 INV-5·INV-7 — `requires` = `MemoryServiceInterface`의 Core 근거.
- specs/03-loop.md §4.1 — Memory 접근 행(Adapter Binding 소관 포인터).
- framework/runtime/module-manifest.md — Module Manifest 형식 규격(본 문서는 그 형식의 인스턴스).
- framework/verifier/module-manifest.md · framework/memory/module-manifest.md — 인스턴스 관례 표본(`requires` 값은 사실 관계 상이 — §5).
- framework/core/config-schema.md §7 — `retry.limit`의 소유 소재(DP-L2 근거).
- framework/core/structure.md §2·§5·§7 — 소속 경계·금지 토큰 규칙·Core Contract 불변 C-1.
- specs/00-glossary.md §3.2-I — Module / Module Manifest / 모듈 시스템 / Runtime Context 용어 정본.

거버넌스: 이 문서는 `framework/loop/` 소속 Module 구현 디렉터리 문서다(structure.md §2). 본문은 AI·언어·툴체인·직렬화 형식 비의존을 유지한다(structure.md §5 C-3). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(다른 절에서 반복하지 않는다).

- **필드 계약의 정본은 specs/01-runtime.md §3.2-A다.** 이 문서는 그 계약을 Loop Provider Module에 대해 채운 **인스턴스**이며 필드·의미·필수/선택 표기를 재정의·확장하지 않는다(structure.md §7 C-1).
- **형식 규격의 정본은 framework/runtime/module-manifest.md다**(7필드 작성 지침·안정 식별자 규칙·언어 중립 시그니처). 두 문서 모두 01 §3.2-A를 진위 판정 기준으로 삼는다.
- **사이클 구동 계약의 정본은 specs/03-loop.md §3이다.** 이 Manifest는 그 Module의 등록 서술자일 뿐이며 단계 전이·재작업 루프·종료·기록 계약을 재정의·재서술하지 않는다.
- **Module 구현 디렉터리 문서.** 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로)을 두지 않는다 — 규칙·분류 정본은 structure.md §5 C-3(및 01 §3.3 INV-4)이다. 작성 시점의 동시 작성 형제 불인용(07 R2)·추측 0(07 R4) 준수 서술 = 종전 문면 git 앵커 90ca19c(정본 = uahf/specs/07-workflow.md §3.2-C). 구체 직렬화·물리 진입점 해소·역할 실행 채널은 Adapter Binding 문서 소관이다(01 §4, 03 §4.1).
- 용어는 specs/00-glossary.md 정본만 사용한다(§3.2-I 등). **`LoopInterface`는 이 Provider가 구현하는 contract 식별자 값이지 Glossary 표제어의 신설이 아니다**(§5 DP-L1). 필드명 백틱 표기는 01 §3.2-A의 필드명 인용이다.

---

## §1. 목적

이 문서는 **Loop Provider Module**의 등록 서술자(Module Manifest)다. Loop Provider는 contract `LoopInterface`를 구현하며, 단일 위임 하나에 대해 Agent Lifecycle 한 사이클을 구동하는 실행 단위를 Runtime이 등록·해소·교체한다(03 §3.1, 01 §3.1-A). 이 Manifest는 Runtime **Register** 연산(01 §3.1-A, 운용 규칙 framework/runtime/module-registry.md §2.1)의 입력이며, 01 §3.2-A 7필드를 이 Provider의 구체 값으로 채우고 필수/선택 표기를 정본 그대로 보존한다.

---

## §2. 7필드 인스턴스 (값 — 필드 의미의 정본은 01 §3.2-A)

정본 = `uahf/specs/01-runtime.md §3.2-A`(재정의 0 · 필드 의미 문면은 정본 참조). 아래는 값 행만 둔다.

| 필드 | 값 (이 Provider 인스턴스) | 필수 |
|---|---|---|
| `id` | `loop-provider` (역할·계약 기반 안정 식별자) | 예 |
| `contract` | `LoopInterface` (DP-L1 — §5) | 예 |
| `version` | `0.1.0` (Provider Module 자체 버전 — 독립 축) | 예 |
| `requires` | `MemoryServiceInterface` (03 INV-5·INV-7) | 아니오(기본 없음) |
| `entrypoint` | 추상 참조 — 사이클 구동 연산(03 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 소관(§4). | 예 |
| `configSchema` | 선언하지 않음 (생략 — DP-L2, §5) | 아니오 |
| `replaceable` | 기본 `true` (생략) | 아니오(기본 true) |

- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true). `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기는 정본 표기이며, 이 Provider는 선택 필드에 값을 **채운** 것일 뿐 필수/선택 지위를 바꾸지 않는다.

---

## §3. 필드별 값 근거 (결정 결론은 §5)

- **`id` = `loop-provider`** — 역할·계약 기반 안정 식별자로, 구현 세부(버전·환경·오케스트레이션 방식)를 인코딩하지 않는다(01 INV-7; memory/verifier Manifest의 `-provider` 접미 관례 동형). 마일스톤 어휘("engine")를 섞지 않는다. Advisor 확인 완료(§5).
- **`contract` = `LoopInterface`** — 이 Provider가 구현하는 사이클 구동 계약(Port/Interface) 식별자. 동일 `contract` 내 교체가 성립하므로 소비자 참조가 유지된다(01 INV-1). 결정 = §5 DP-L1.
- **`version` = `0.1.0`** — Provider Module 자체 버전(Framework/Spec 버전과 독립 축, 구현 갱신 시 상승). 초기 값 관례는 memory·verifier Manifest 동형이다.
- **`requires` = `MemoryServiceInterface`** — 사이클 구동은 Memory Update를 불가피하게 포함하므로(03 INV-5 Learn 불가피성 · §3.1-A(6) · INV-7 단일 Port) 이 계약 없이는 사이클을 완결할 수 없다. **module id가 아니라 contract id를 나열한다**(01 §8 예1·04 §4.1이 사전 명명한 기존 값 — 신설 0). **역할 실행(CP1~CP3)은 넣지 않는다** — 위임·보고 메시지 흐름의 역할 디스패치이며 Runtime Resolve가 아니다(02 §4.1, 03 §4.1). 01 INV-2(단독 사용) 위반이 아니다 — INV-2는 Runtime이 필수 계약 집합만으로 기동함을 보장하는 규칙이고, 이 값은 Loop Provider 활성 시의 의존 집합을 정한다. Advisor 확인 완료(§5).
- **`entrypoint` = 추상 참조** — 사이클 구동 연산(03 §3.1: 입력 = 위임 메시지 1건 + Runtime Context, 출력 = 완료 보고 또는 에스컬레이션)을 노출하는 논리 진입점. 물리 경로·형식별 로케이터를 Core 서술자에 기입하지 않는다(01 INV-4, 03 INV-9). 상세는 §4.
- **`configSchema` = 선언하지 않음** — Loop가 소비하는 Config 값은 재시도 한도뿐이고 그 키 `retry.limit`은 framework/core/config-schema.md §7이 소유하는 Framework 수준 키다. Loop는 effective config의 **소비자**(01 §3.2-B)일 뿐이므로 자기 Module `configSchema`로 재선언하면 값 소유가 이중화된다. 결정 = §5 DP-L2.
- **`replaceable` = 기본 `true`** — 생략하여 기본값을 취한다. 모든 Module은 교체 가능이 기본이며(01 INV-1) 이 Provider에 교체 불가의 근거가 없다. 근거 없는 `false`를 두지 않는다.

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider의 활성화 진입을 가리키는 **추상(논리) 참조**이며, 노출하는 것은 사이클 구동 연산(03 §3.1)이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩(직렬화 형식·물리 경로·호출 규약·역할 실행 채널·루프 상태 기록 저장 배선)은 전부 Adapter Binding 문서 소관이다(01 §4, 03 §4.1). 이 Core 서술자에는 물리 경로·형식 토큰을 하드코딩하지 않는다.
- 이 분리로 이식·교체(01 §8 예1, 03 §4.2) 시에도 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고 물리 바인딩만 Adapter 경계에서 교체된다.
- `requires`가 참조하는 `MemoryServiceInterface`의 물리 실현 역시 Adapter 소관이다(03 §4.1 Memory 접근 행 — 단일 Port 경유가 Memory Service Interface Module의 Resolve로 실현됨).

---

## §5. 결정 기록 (Advisor 결정 — DP-L1·DP-L2 + Advisor 확인)

- **DP-L1 — `contract` = `LoopInterface`.** 사이클 구동 계약 식별자를 `LoopInterface`로 확정한다. 저장소에 사전 명명이 없어(Advisor 실측 — 전역 0건) Advisor 결정 사안이며, Glossary 정본 어휘 "Loop" + 관례 접미 "Interface"의 조합이다(Memory `MemoryServiceInterface`·Verifier `VerifierInterface` 선례 동형). 마일스톤 어휘 "Engine"은 안정 식별자에서 배제한다(01 INV-7). 이 값은 `contract` 필드 값이지 Glossary 표제어 신설이 아니다.
- **DP-L2 — `configSchema` 생략.** 이 Manifest는 `configSchema`를 선언하지 않는다(01 §3.2-A 선택 필드). 근거: `retry.limit`은 framework/core/config-schema.md §7이 소유하는 Framework 수준 키이며(값·스코프·병합 규칙 정본은 config-schema.md §7·01 §3.2-B) Loop는 그 소비자일 뿐이므로 재선언은 값 이중화다. Verifier DP-V2(소비 값 자체 부재)와 **동형의 생략이되 근거가 다르다** — Loop는 소비 값이 있으나 소유가 Framework 수준에 이미 있다.
- **Advisor 확인 — `id`·`requires` 인스턴스 값 (2026-07-06).** 새 결정(DP)이 아니라 관례·정본 근거로 채운 값의 승인이다. `id`=`loop-provider`는 Manifest 관례 동형 + 01 INV-7 충족. `requires`=`MemoryServiceInterface`는 03 INV-5·INV-7과 03 §4.1 Memory 접근 행 근거이며, Verifier 선례(requires=없음)와 **사실 관계가 상이**하다 — Verifier의 Memory 회수는 06 §5 "필요할 때만"의 선택적 보강이라 Resolve를 게이트하지 않지만, Loop의 Memory Update는 불가피한 계약 필수다. 미확정 잔여는 없다.
