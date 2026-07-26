# framework/verifier/module-manifest — Verifier Provider Module Manifest 인스턴스

작성일: 2026-07-06
상태: v0.5 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드(`id`/`contract`/`version`/`requires`/`entrypoint`/`configSchema`/`replaceable`). 본 문서가 채우는 서술자 계약의 정본. 필드명·의미·필수/선택 표기의 진위 판정 기준은 이 §가 유지한다.
- specs/01-runtime.md §3.3 INV-7 — 안정 식별자(`id`·`contract` id 안정성). INV-1 — 교체 가능(`replaceable` 기본값 근거). INV-2 — 단독 사용(선택 계약 부재는 Degraded, `requires` 값 근거). INV-4 — Core AI 비의존.
- specs/01-runtime.md §4 — Adapter Binding(구체 직렬화·물리 진입점 해소 소관). 본 문서는 § 포인터로만 참조한다.
- specs/01-runtime.md §8 예2 — Config 스코프 병합 예시(키 `verify.strict`). 이 Manifest의 `configSchema` 생략 근거(DP-V2)에서 참조 대상으로만 인용한다.
- specs/06-verifier.md §1·§2 — Verifier의 목적과 Module 지위("판정을 수행하는 실행 단위는 Runtime이 호스팅하는 하나의 Module", 01 §3.2-A·§4.1 `framework/verifier/`).
- specs/06-verifier.md §3.1 — 판정 연산(Verify). `entrypoint`가 노출하는 논리 진입점의 근거.
- specs/06-verifier.md §4.1 — Verifier 진입점·구현 디렉터리 바인딩. 물리 진입점 해소의 소관 포인터.
- framework/runtime/module-manifest.md — Module Manifest **형식 규격**(7필드 작성 지침·안정 식별자 규칙·언어 중립 시그니처). 본 문서는 그 형식을 이 Provider에 대해 채운 **인스턴스**다.
- framework/memory/module-manifest.md — Manifest 인스턴스 **관례 정본**(구성·표기·`version` 독립 축 `0.1.0` 관례 동형 적용).
- framework/core/structure.md §2·§5 — Module 구현 디렉터리 경계(자기완결, C-3 확장 — 문서 본문 비의존), 금지 토큰 규칙.
- framework/core/config-schema.md §6 — `verify.strict` 병합 예시(참조만 — DP-V2 근거).

거버넌스: 이 문서는 `framework/verifier/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인·직렬화 형식 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.5 Draft | 최초 작성. Verifier Provider Module의 01 §3.2-A 7필드 인스턴스(`id`=`verifier-provider`·`contract`=`VerifierInterface`(DP-V1)·`version`=`0.1.0`·`requires`=없음·`entrypoint`=추상 참조·`configSchema`=선언하지 않음(DP-V2)·`replaceable`=기본 true), 필드별 인스턴스 값·근거, `entrypoint` 추상 참조 + 물리 해소 Adapter Binding 소관 포인터(물리 경로·형식 하드코딩 0), 필수/선택 표기 정본 대조 보존, DP-V1·DP-V2 결정 기록. 01·06 계약 재정의·확장 0, 금지 토큰 0, Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task V2) |
| 2026-07-06 | v0.5 Draft (r2) | Advisor 확인 2건 반영. open_questions로 올렸던 인스턴스 값 `id`(=`verifier-provider`)·`requires`(=없음)가 Advisor 확인(2026-07-06)으로 승인됨에 따라, §3 `id`·`requires` 말미 주와 §6 "확인 대기" 항목의 미확정 서술을 확인 완료로 전 지점 정합화(L-06), §5에 "Advisor 확인 — 인스턴스 값" 기록 추가(DP와 구분되는 승인 기록). 7필드 값·근거·DP-V1·V2 기록 무변경. | Worker (Advisor r2 지시, Task V2 r2) |
| 2026-07-06 | v0.5 Baseline | v0.5 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 26/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 3 — 비계약 격리 개정: 경계 중복·표-산문 이중·감사 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **필드 계약의 정본은 specs/01-runtime.md §3.2-A이다.** 이 문서는 그 Module Manifest 계약을 **Verifier Provider Module에 대해 채운 인스턴스**이며, 필드·의미·필수/선택 표기를 **재정의·확장하지 않는다** (framework/core/structure.md §7 확정 조건 C-1). 필드 계약 요소는 01 §3.2-A를 § 포인터로 참조한다.
- **형식 규격의 정본은 framework/runtime/module-manifest.md이다.** 그 문서는 임의 Manifest를 **어떻게 작성·판독하는가**(7필드 형식·안정 식별자 규칙·언어 중립 시그니처)를 규율하고, 이 문서는 그 형식을 이 Provider 하나에 대해 **구체 값으로 채운** 등록 서술자다. 두 문서 모두 01 §3.2-A를 진위 판정 기준으로 삼는다.
- **판정 계약의 정본은 specs/06-verifier.md이다.** 이 Provider가 구현하는 contract(§3 아래 `VerifierInterface`)가 노출하는 판정 연산·독립성·리포트 계약은 06 §3이 소유한다. 본 문서는 그 계약을 **재정의·재서술하지 않고** § 포인터로만 참조하며, 이 Manifest는 그 Module의 등록 서술자일 뿐이다.
- **이 문서는 Module 구현 디렉터리 문서다** (framework/core/structure.md §2 — 각 Module의 Manifest를 자기 경계에 두는 자기완결 단위, 01 §3.2-E 규칙 2). 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (framework/core/structure.md §5 C-3 확장, 01 §3.3 INV-4). 구체 직렬화·물리 진입점 해소·환경 경로 관례는 **Adapter Binding 문서 소관**이며 (01 §4, 06 §4.1), 필요한 자리에는 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Module / Module Manifest / 모듈 시스템 / Runtime Context는 Glossary §3.2-I가 정본이다. Verifier / 검증 / 판정은 Glossary 기존 용어다. 새 용어를 정본처럼 신설하지 않는다. **`VerifierInterface`는 이 Provider가 구현하는 contract 식별자 **값**이지 Glossary 표제어의 신설이 아니다** (§5 DP-V1 참조).
- 필드명 백틱 표기(`id` 등)와 예시 식별자는 특정 언어·직렬화 형식의 문법이 아니라, 정본 01 §3.2-A가 쓰는 필드명·서술 라벨을 그대로 인용한 것이다.

---

## §1. 목적

이 문서는 **Verifier Provider Module**의 등록 서술자(Module Manifest)다. Verifier Provider는 contract `VerifierInterface`를 구현하는 Module이며, 판정을 수행하는 실행 단위를 Runtime이 등록·해소·교체한다 (06 §2, 01 §3.1-A·§4.1 `framework/verifier/`).

이 규격의 책임은 두 가지다.

- 01 §3.2-A의 7필드를 이 Provider에 대한 **구체 값**으로 채운다 — `contract`는 `VerifierInterface`로 확정하고(§5 DP-V1), `entrypoint`는 판정 연산(Verify, 06 §3.1)을 노출하는 추상 참조로 두며 물리 해소는 Adapter Binding 문서 소관으로 미룬다. `configSchema`는 선언하지 않는다(§5 DP-V2).
- 필드의 필수/선택 표기를 정본 그대로 보존한다 (필수/선택 표기 보존).

이 Manifest는 Runtime의 **Register** 연산(01 §3.1-A, 운용 규칙: framework/runtime/module-registry.md §2.1)의 입력이 된다. 각 Module은 자기완결(self-contained) 단위이므로, 이 Manifest는 그 Module의 `id`·`contract`·`entrypoint` 등 자기완결 참조를 한 서술자에 묶는다 (01 §3.2-E 규칙 2). 이 Provider가 구현하는 판정 계약(§3.1 Verify 연산·독립성·검증 리포트)의 정본은 specs/06-verifier.md가 유지하며, 본 문서는 그 계약을 재서술하지 않는다.

---

## §2. 7필드 인스턴스 (정본 대조 표)

아래 표는 01 §3.2-A의 7필드를 이 Provider에 대한 값으로 채운 것이다. **필드명·의미·필수/선택 표기는 정본(01 §3.2-A) 그대로**이며, "값 (이 Provider 인스턴스)" 열만 본 문서가 채운다. 필드 계약을 재정의하지 않는다.

| 필드 | 의미 (정본: 01 §3.2-A) | 값 (이 Provider 인스턴스) | 필수 |
|---|---|---|---|
| `id` | Module 고유 식별자. 안정적(stable)이어야 교체의 기준이 된다. | `verifier-provider` (역할·계약 기반 안정 식별자 — §3 참조) | 예 |
| `contract` | 이 Module이 구현하는 계약(Port/Interface) 식별자. 교체는 동일 `contract` 내에서만 성립한다. | `VerifierInterface` (DP-V1 — §3·§5 참조) | 예 |
| `version` | Module 버전. | `0.1.0` (이 Provider Module 자체 버전 — §3 참조) | 예 |
| `requires` | 의존하는 contract id 목록. Resolve 시 모두 해소되어야 한다. | 없음 (기본 — §3 참조) | 아니오(기본 없음) |
| `entrypoint` | 실행 진입점의 추상 참조. 구체 바인딩은 01 §4가 해소한다. | 추상 참조 — 판정 연산 Verify(06 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4). | 예 |
| `configSchema` | 이 Module의 Config 스키마. | 선언하지 않음 (생략 — DP-V2, §3·§5 참조) | 아니오 |
| `replaceable` | 교체 가능 여부. 기본 `true` (ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 기본 `true` (생략 — §3 참조) | 아니오(기본 true) |

주:

- **필수/선택 표기는 정본 그대로 보존한다.** `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기를 복제한다 — 누락되면 계약 변경으로 읽힌다.
- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true).
- 상세 필드 계약의 정본은 01 §3.2-A가, 형식 작성 지침은 framework/runtime/module-manifest.md가 유지한다. 이 표는 값 인스턴스이며 계약의 진위 판정 기준이 아니다.

---

## §3. 필드별 인스턴스 값·근거

각 필드의 값과 1줄 근거다(§5는 결정 ID·결론만 둔다 — 쌍둥이 서술 제거). 값은 이 Provider의 인스턴스이며 필드 계약은 재정의하지 않는다.

- **`id` = `verifier-provider`** (필수) — 역할·계약 기반 **안정 식별자**(01 INV-7): 구현 세부(버전·환경·검사 도구)를 인코딩하지 않아 교체(Replace)의 기준이 유지된다. 명명은 관례 정본(framework/memory/module-manifest.md §3 `memory-service-provider`) 동형. Advisor 확인 완료(2026-07-06 — §5).
- **`contract` = `VerifierInterface`** (필수) — 이 Provider가 구현하는 판정 계약(Port/Interface) 식별자. 동일 `contract` 내 교체로 소비자 참조가 유지된다(01 INV-1). 계약이 노출하는 판정 연산·독립성·리포트의 정본은 06 §3. 결정 = §5 DP-V1.
- **`version` = `0.1.0`** (필수) — 이 Provider Module 자체 버전의 고정 문자열. Framework/Spec 버전과 **독립 축**이며 구현 갱신 시 상승한다(Memory Manifest 관례 동형).
- **`requires` = 없음** (선택 — 기본 없음) — Verify의 입력은 산출물+대조 기준이고 판정은 산출물 자체를 근거로 하므로(06 §3.1·INV-1) 하드 의존이 없다. Memory 소비(06 §5·INV-10)는 단일 Port를 통한 "필요할 때만"의 선택적 보강이라 Resolve를 게이트하지 않으며, 하드 선언은 01 INV-2(단독 사용)와 마찰한다. 존재하지 않는 contract id를 신설·추측하지 않는다. Advisor 확인 완료(2026-07-06 — §5).
- **`entrypoint` = 추상 참조** (필수) — 판정 연산 Verify(06 §3.1)를 노출하는 논리 진입점. 구체 바인딩(직렬화·물리 경로·호출 규약·검사 도구 배선)은 기입하지 않는다 — 환경 의존을 Core 서술자에 하드코딩하면 비의존(01 INV-4, 06 INV-8)이 깨진다. 상세 = §4.
- **`configSchema` = 선언하지 않음** (선택) — 06 §3 계약에 이 Provider가 소비하는 Config 의존 값이 없다. 결정 = §5 DP-V2.
- **`replaceable` = 기본 `true`** (선택 — 기본 true) — 교체 가능이 기본이며(01 INV-1) 이 Provider에는 교체 불가의 근거가 없다. 근거 없는 `false`를 두지 않는다.

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider Module의 활성화 진입을 가리키는 **추상(논리) 참조**다. 그것이 노출하는 것은 판정 연산 Verify(06 §3.1) — 산출물과 대조 기준을 입력받아 검증 리포트를 출력하는 독립 판정 — 이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩 — 직렬화 형식, 물리 경로·로케이터, 호출 규약, 검사 도구 배선 — 은 전부 **Adapter Binding 문서 소관**이다 (01 §4, 06 §4.1). 이 Core 서술자에는 그 어떤 물리 경로·형식 토큰도 하드코딩하지 않는다 (framework/runtime/module-manifest.md §3 `entrypoint` 회피 규칙 정합).
- 이 분리로 검사 도구·실행 환경 이식·교체(01 §8 예1, 06 §4.2 이식 교체 지점) 시에도 이 Manifest의 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고, 물리 바인딩만 Adapter 경계에서 교체된다.

---

## §5. 결정 기록 (Advisor 결정 — DP-V1·DP-V2)

결정 ID + 결론만 둔다(근거는 §3 필드별 1줄 — 쌍둥이 서술 제거). 두 결정은 위임의 확정 입력이며 본 문서는 이를 그대로 반영한다.

- **DP-V1 — `contract` = `VerifierInterface`.** 판정 계약 식별자를 이 값으로 확정한다(저장소 사전 명명 부재 → Advisor 결정 사안. Glossary 정본 어휘 "Verifier" + Manifest 관례 접미 "Interface"의 조합이며 Memory 선례 `MemoryServiceInterface`와 동형). 이 값은 `contract` 필드의 **값(식별자)**이지 Glossary 표제어 신설이 아니다(§0·§6).
- **DP-V2 — `configSchema` 생략.** 01 §3.2-A 선택 필드로 선언하지 않는다. `verify.strict`(01 §8 예2·framework/core/config-schema.md §6)는 Config 병합 규칙의 예시 키일 뿐이며, 그 키에 판정 의미를 부여하면 06 §3.2-C·§3.3과 충돌 소지가 있는 계약 창설이 된다. Config 병합 규칙 정본은 01 §3.2-B·framework/core/config-schema.md.
- **Advisor 확인 — `id`·`requires` 인스턴스 값 (2026-07-06).** 새 결정(DP)이 아니라 관례·정본 근거로 채운 두 인스턴스 값에 대한 승인 기록이다(근거 = §3). 이 확인으로 종전의 "확인 대기" 상태가 해소되었다.

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- **재정의·확장 0.** 본 문서의 7필드는 01 §3.2-A의 인스턴스이며 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A(필드 계약)와 framework/runtime/module-manifest.md(형식 규격)다. 판정 계약(06 §3)은 § 포인터로만 참조했고, 필수/선택 표기를 정본 그대로 보존했으며 새 필드를 추가하지 않았다.
- **새 계약·용어 0.** `requires`에서 존재하지 않는 백엔드/저장 contract를 신설하지 않았고, Glossary 밖 새 용어를 만들지 않았다(`VerifierInterface`는 `contract` 필드의 식별자 값 — §5 DP-V1).
- **금지 토큰·Glossary 경계.** 금지 토큰 규칙과 정당 매치 분류의 판정 기준은 framework/core/structure.md §5 C-3 확장이 소유한다(01 INV-4, 06 INV-8). 진입점·검사 도구의 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관(01 §4, 06 §4.1)" 포인터를 둔다(mention/use 경계).
- **미확정·open 잔여 = 없음.** `contract` 명명(DP-V1)·`configSchema` 생략(DP-V2)은 Advisor 결정, `id`·`requires`는 Advisor 확인(2026-07-06)으로 확정되었다(§5).
