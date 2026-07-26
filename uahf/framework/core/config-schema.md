# framework/core/config-schema — UAHF Config 스키마 규격

작성일: 2026-07-05
상태: v0.3 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-05)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-B — Config 스코프·로딩 순서·우선순위·결정성·누락 스코프 규칙의 정본.
- specs/01-runtime.md §3.1-B — Load Config 연산 시그니처의 정본.
- specs/01-runtime.md §3.2-D — Failure Report 공통 보고 구조의 정본.
- specs/01-runtime.md §3.3 INV-5 — 결정적 Config 불변.
- specs/01-runtime.md §8 예2 — 스코프 병합 예시(§6 재현 근거).
- specs/01-runtime.md §9 OQ-R1 — Config 우선순위 방향 결정의 정본.
- specs/03-loop.md §3.1-B — 재시도 한도 항목 원문(DP-1 승계 근거).
- framework/core/structure.md §2·§5·§7 — 소속·소유 경계(4경계 배치 표)·금지 토큰 규칙(C-3)·Core Contract 불변(C-1).
- specs/00-glossary.md §3.2-I — Config 용어 정본.

거버넌스: 이 문서는 `framework/core/` 소속 Core 문서다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.3 Draft | 최초 작성. 01 §3.2-B Config 스코프·로딩 순서·우선순위·결정성·누락 스코프 규칙 인스턴스화, 언어 중립 추상 스키마·Load Config 시그니처(01 §3.1-B·§3.2-D), 01 §8 예2 병합 예시 재현, DP-1(재시도 한도) 자리 예약. | Worker (Advisor 위임, Task A3) |
| 2026-07-05 | v0.3 Draft r2 | Advisor 개정 2건. (1) DP-1 해소 — §7: 재시도 한도 추상 키 `retry.limit`, 기본값 2, Global 스코프 기본 + Project/Module override (근거: v0.1·v0.2 재작업 실측). (2) §5 주 — `SchemaViolation` 대조 스키마 출처의 조율 결정(A3 완료 보고 open_question 해소). | Advisor |
| 2026-07-05 | v0.3 Draft r3 | CP2(A8 Verifier) Fail 재작업 — r2 개정 잔여 결함 교정. (1) §1·§7 서두·§7 제목·§10의 "미결정/자리만 예약/미기입" 서술을 DP-1 해소 상태와 정합화 (§5.3 상태 서술 모순 해소). (2) §7 말미 주의 실재하지 않는 "§Open Questions" 참조 제거 — §5 조율 결정으로 해소됨을 명시 (DoD-5 준용 해소). Verifier 검출 위반 2건 전체 대응. | Advisor |
| 2026-07-05 | v0.3 Baseline | v0.3 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass, CP3 Advisor 승인, DP-1 사용자 재가: `retry.limit` 기본값 2·Global). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-XX·mi 유지)·삭제 산출물 참조 앵커 전환(@cd9247b·@004bfa9). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 3 — 비계약 격리 개정: 경계 중복·복제 절 포인터화·감사 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다. uaf-allow-legacy: §9 기존 행은 개정 시점의 이력 기록이므로 문면을 고치지 않고 보존한다.)

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(다른 절에서 반복하지 않는다).

- **정본은 specs/01-runtime.md §3.2-B(Config)·§3.1-B(Load Config)·§3.2-D(Failure Report)·§3.3 INV-5다.** 이 문서는 그 Core Contract의 **인스턴스**이며 계약을 재정의·확장하지 않는다(structure.md §7 C-1).
- 이 문서는 `framework/core/` 소속 **Config 스키마 문서**다(structure.md §2·§4 C-2 — Core 경계는 계약·스키마 문서 전용). 물리 소스·직렬화 형식은 여기서 정하지 않는다 — Adapter Binding 소관이다(01 §4.1, §8).
- **Core 문서.** 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명)을 두지 않으며 규칙 서술 문안에서도 구체 예시 토큰을 나열하지 않는다 — 규칙·분류 정본은 structure.md §5 C-3(및 01 §3.3 INV-4)이다.
- 용어는 specs/00-glossary.md §3.2-I 정본만 사용하고 새 용어를 신설하지 않는다. `C-1`·`C-2`·`C-3`(structure.md 확정 조건)과 `DP-1`(§7)은 **서술 참조 라벨**이며 Glossary 표제어가 아니다.

---

## §1. 목적

이 문서는 01 §3.2-B Config 계약을 `framework/core/` 경계 위에 **스키마 수준**으로 인스턴스화한다 — 3스코프 정의·로딩 순서·우선순위·결정성·누락 스코프 처리(§3·§4) · 언어 중립 추상 스키마와 Load Config 시그니처(§2·§5) · 01 §8 예2 병합 도출 재현(§6) · 재시도 한도 키(§7, DP-1 해소). 01 §3의 어떤 계약 요소도 재정의·확장하지 않는다(C-1).

---

## §2. Config 추상 스키마 (언어 중립)

Config는 스코프를 가진 **key→value 트리**다 (01 §3.2-B, Glossary §3.2-I). 스키마는 추상 수준으로만 정의하며, 직렬화 형식(파일 형태·문법)은 Adapter Binding 문서 소관이다 (01 §3.2 서두, §4.1).

각 스코프는 하나의 key→value 트리를 기여한다. 기여 트리의 서술 요소는 다음과 같다 (언어 중립 표기 — 특정 언어 타입 표기법을 쓰지 않는다).

```
Config(scope 기여 단위)
├─ scope   : { Global | Project | Module }         # 이 트리가 속한 스코프 (01 §3.2-B)
├─ target  : module id                             # Module scope에서만 유효 — 대상 Module 네임스페이스 (01 §3.2-B)
└─ entries : key → value 트리                        # 이 스코프가 기여하는 설정 항목
```

- **scope 속성.** 각 기여 트리는 {Global, Project, Module} 중 정확히 하나의 스코프에 태깅된다 (§3).
- **target 속성.** Module scope 트리에만 존재한다. `target` = 대상 module id이며, 그 트리의 entries는 해당 Module id 네임스페이스에 국한된다 (01 §3.2-B "Module scope — 특정 Module(target = module id) 네임스페이스에 국한된 설정"). Global·Project scope 트리에는 target이 없으며 모든 대상에 적용된다.
- **entries 속성.** key→value 트리. value는 스칼라 또는 하위 key→value 트리일 수 있다(중첩 키). key 표기의 구체 문법은 Adapter Binding 문서 소관이다.
- **산출(effective config).** 스코프별 기여 트리를 우선순위대로 병합한 유효 설정이다 (01 §3.2-B, §4·§5).

**계약 위치 명시 (C-1).** 위 추상 스키마는 **01 §3.2-B의 인스턴스이며 계약 확장·수정이 아니다 (structure.md §7 C-1)**. Config의 스코프 집합·필드 의미의 정본은 01 §3.2-B가 유지하고, 본 문서는 § 포인터로만 참조한다.

---

## §3. 스코프 정의 (3스코프)

01 §3.2-B의 3스코프를 그대로 인용한다. 정의·적용 범위·우선순위 지위는 재정의하지 않는다.

| 스코프 | 정의 (01 §3.2-B) | 적용 범위 | 우선순위 지위 |
|---|---|---|---|
| **Global scope** | Framework 전역 기본값. | 모든 대상에 적용. | 최저 우선순위. |
| **Project scope** | 프로젝트 단위 override. | 모든 대상에 적용. | 중간 (Global 위, Module 아래). |
| **Module scope** | 특정 Module(`target` = module id) 네임스페이스에 국한된 설정. | `target` Module id 네임스페이스에 국한. | 최고 우선순위. |

- 세 스코프의 정의·적용 범위 문안은 01 §3.2-B와 셀 단위로 일치한다. 우선순위 지위 열은 §4의 우선순위 규칙을 스코프별로 재기입한 것이며, 방향의 정본은 §4가 인용하는 01 §3.2-B·§9 OQ-R1이다.
- Module scope의 `target`은 대상 Module의 안정적 id를 참조한다 (안정 식별자 규칙: 01 §3.3 INV-7 — 재정의하지 않고 참조).

---

## §4. 로딩 순서·우선순위·결정성·누락 스코프

01 §3.2-B "로딩 순서와 우선순위" 절과 01 §3.3 INV-5를 인스턴스화한다. 규칙 원문의 정본은 01이다.

### §4.1 로딩 순서

- 로딩 순서: **Global → Project → Module** (01 §3.2-B). 스코프 소스를 이 순서로 읽는다.

### §4.2 우선순위

- 우선순위(높음 → 낮음): **Module > Project > Global** (01 §3.2-B). 같은 키가 여러 스코프에 겹치면 높은 우선순위 스코프의 값이 이긴다 (last-writer-wins by precedence, 01 §3.2-B).
- **정합 관찰(01 규칙의 재기술, 확장 아님).** 로딩 순서(Global → Project → Module)는 우선순위의 오름차순과 일치한다. 따라서 로딩 순서대로 순차 덮어쓰기를 하면 마지막 기록자가 Module → Project → Global 순의 최고 우선순위가 되어, 우선순위 규칙 Module > Project > Global과 동일한 결과를 낸다. 이는 01 §3.2-B가 이미 규정한 두 문장(로딩 순서·우선순위)의 관계를 관찰한 것이며, 새 규칙을 추가하지 않는다.

**우선순위 방향의 결정 근거 (01 §9 OQ-R1 인용).**

- 01 §3.2-B는 Project ↔ Module 우선순위 방향이 ARCHITECTURE·ROADMAP이 명시하지 않은 Runtime 설계 결정임을 밝히고 §9에 확인 항목으로 올렸다.
- 결정(Advisor, 01 §9 OQ-R1): **Module > Project > Global**로 확정. 근거 — Module scope는 모듈 자체의 기본값이 아니라 특정 Module을 겨냥해 작성되는 **가장 좁은 override**이므로, 좁은 스코프 우선(specificity) 원칙이 결정성과 예측 가능성을 높인다.
- 같은 결정의 부가 근거(01 §9 OQ-R1): Module 자체의 기본값은 Manifest `configSchema` 기본값(01 §3.2-A `configSchema` 필드 — 필수: 아니오)으로서 병합 최하위에 위치하므로, "Project가 모듈 기본값을 덮는" 요구는 Project scope로 이미 충족된다. (본 문서는 이 근거를 01 §9 OQ-R1의 결정 인용으로만 재기술하며, `configSchema` 필드의 계약은 01 §3.2-A가 정본이다 — 재정의하지 않는다.)

### §4.3 결정성

- effective config는 **결정적(deterministic)**이다. 동일 입력은 항상 동일 결과를 낸다 (01 §3.2-B). Config 병합은 결정적이며 우선순위 순서(§4.2)는 고정된다 (01 §3.3 INV-5).

### §4.4 누락 스코프 처리

- 존재하지 않는 스코프는 병합에서 **건너뛴다** (01 §3.2-B). 누락 스코프는 실패가 아니라 그 스코프의 기여가 없음으로 처리되며, 남은 스코프가 우선순위대로 병합된다 (01 §3.1-B 완료 조건 "누락 스코프는 건너뛴다").
- 한 스코프가 특정 키를 지정하지 않으면, 그 키에 대해 그 스코프는 기여하지 않고 차하위 우선순위의 값이 적용된다 (01 §8 예2의 도출과 동일 — §6).

---

## §5. Load Config 연산 시그니처 (언어 중립)

01 §3.1-B Load Config 연산과 01 §3.2-D Failure Report의 인스턴스다. 시그니처는 언어 중립으로만 표기하며, 특정 언어 타입 표기법을 쓰지 않는다.

| 요소 | 값 (01 §3.1-B·§3.2-D) |
|---|---|
| **입력** | 스코프별 Config 소스 집합 (Global / Project / Module). |
| **출력** | effective config — 우선순위(§4.2)대로 병합된 유효 설정 (01 §3.2-B). |
| **완료 조건** | 모든 존재하는 스코프가 정의된 우선순위(§4.2)로 결정적으로 병합된다. 누락 스코프는 건너뛴다 (01 §3.1-B). |
| **실패** | reason = `SchemaViolation`, location = 스코프/키 (01 §3.1-B). |

**실패 보고 구조 (01 §3.2-D Failure Report 인스턴스).** Load Config 실패는 Runtime 공통 Failure Report로 보고된다.

| 필드 | Load Config에서의 값 (01 §3.2-D) |
|---|---|
| `operation` | `LoadConfig`. |
| `target` | config 스코프·키. |
| `reason` | `SchemaViolation`. |
| `location` | 실패 지점 참조 — 스코프·키 (01 §3.1-B). |

**계약 위치 명시 (C-1).** 위 시그니처와 실패 보고는 **01 §3.1-B·§3.2-D의 인스턴스이며 계약 확장·수정이 아니다 (structure.md §7 C-1)**. 연산의 입력·출력·완료 조건·실패 사유 코드의 정본은 01 §3.1-B·§3.2-D가 유지한다.

주: `SchemaViolation` 판정이 대조하는 "스키마"의 출처는 스코프에 따라 다를 수 있다. 이 문서는 01이 정의한 실패 사유 코드와 location 구조만 인스턴스화한다.

**조율 결정 (Advisor, 2026-07-05 — 01이 규정하지 않은 지점의 운용 해석, 계약 확장 아님).** `SchemaViolation`의 대조 기준은 다음과 같다.

- **Module scope 값** — 대상 Module Manifest의 `configSchema`(01 §3.2-A, 선택 필드)로 대조한다. `configSchema` 부재 시 §2 구조 규칙(스코프 태깅·`target` 유효성·트리 형태)만 적용한다.
- **Global/Project scope 값** — 키가 특정 Module 네임스페이스에 속하면 그 Module의 `configSchema`로 대조하고, Framework 수준 키는 §2 구조 규칙으로 대조한다.
- 이 해석은 01 §3.2-A·§3.2-B가 이미 정의한 계약 요소의 조합이며 새 계약을 추가하지 않는다. `configSchema` 필드의 정본은 01 §3.2-A가 유지한다.

---

## §6. 병합 규칙 예시 (01 §8 예2 재현)

01 §8 예2의 키·값을 그대로 사용해 도출 결과를 재현한다.

**예 — 키 `verify.strict` (01 §8 예2 재현).**

| 스코프 | 기여 값 |
|---|---|
| Global scope | `false` (Framework 기본값) |
| Project scope | `true` (이 프로젝트는 엄격 검증) |
| Module scope (`target` = 특정 Verifier Module) | 미지정 |

도출: 우선순위 Module > Project > Global(§4.2)에서 Module scope가 이 키를 미지정하므로 그 키에 대해 Module은 기여하지 않는다(§4.4). 남은 스코프 중 최고 우선순위는 Project다.

→ effective config의 `verify.strict` = **`true`**.

이 결과는 01 §8 예2("Module이 미지정이므로 Project가 이긴다")와 동일하다.

**동형 예 — Module scope가 같은 키를 지정하는 경우.**

같은 키 `verify.strict`에서 Module scope(`target` = 특정 Verifier Module)가 `false`를 지정하면, 우선순위 Module > Project > Global에 따라 Module 값이 이긴다.

→ effective config의 `verify.strict` = **`false`**.

두 예는 같은 입력 집합에 대해 항상 같은 결과를 내며(결정성, §4.3, 01 §3.3 INV-5), 우선순위 규칙(§4.2)이 스코프 지정 여부에 따라 어떻게 승자를 정하는지 보인다.

---

## §7. 재시도 한도 키 (DP-1 — 해소)

재작업 재시도 한도 값은 Config(01 §3.2-B)로 주어진다(specs/03-loop.md §3.1-B). 그 기본값·스코프는 **2026-07-05 Advisor 결정(DP-1)으로 해소**되어 아래에 확정 기입되었다(v0.3 마일스톤 승인 시 사용자 재가 완료 — §9).

| 예약 요소 | 값 |
|---|---|
| 키 이름 (추상) | `retry.limit` — 재작업 재시도 한도 항목의 추상 키 (DP-1 결정, 2026-07-05). 물리 표기·명명 관례는 Adapter Binding 문서 소관. |
| 타입 | 비음의 정수 형태의 상한값(재작업 되돌림 허용 횟수의 상한). retry_count가 이 값을 초과하면 에스컬레이션된다 (specs/03-loop.md §3.1-B). |
| 기본값이 위치하는 스코프 | **Global** (Framework 전역 기본값). Project/Module scope의 override를 허용한다 — 우선순위는 §4.2 (01 §3.2-B) 그대로. |
| 기본값 | **`2`** (DP-1 결정, 2026-07-05). |

**결정 기록 (DP-1 해소 — Advisor, 2026-07-05).** 기본값 **2**, 기본값 스코프 **Global**(Project/Module override 허용).

- 근거: 03 §3.1-B는 값·스코프를 Config·Adapter Binding 소관으로 열어 두었고(`uahf/docs/session-handoff-v0.2.md@004bfa9` §3.5가 보류 항목으로 승계), v0.1·v0.2 실측에서 모든 재작업이 1회로 해소되었으므로(같은 문서 §1.4) 한도 2는 1회 재작업 + 1회 여유를 허용하면서 한도 초과 에스컬레이션을 과도하게 지연시키지 않는다. Framework 전역 기본값의 정의 위치는 Global scope이며(01 §3.2-B) 프로젝트·모듈별 조정은 §4.2 우선순위로 충족된다.
- Loop의 한도 초과 판정 규칙 자체는 03 §3.1-B 소관으로 불변이다. 이 키의 대조 스키마 출처는 §5 조율 결정으로 해소되었다 — Framework 수준 키이므로 §2 구조 규칙으로 대조하며, 물리 표기·명명 관례는 Adapter Binding 소관이다.

---

## §8. 물리 소스·직렬화 형식 경계

- Config 소스의 **물리 파일 위치·직렬화 형식(파일 형태·문법)**은 이 Core 문서가 정하지 않는다. **Adapter Binding 문서 소관**이다 (01 §3.2 서두 "직렬화 형식은 Adapter Binding(§4)이 정한다", 01 §4.1 Config 소스 바인딩 행).
- 스코프별 물리 소스(Global/Project/Module 각각의 실제 저장 위치)와 그 형식은 대상 환경마다 교체되는 이식 지점이다 (01 §4.2 "Config 소스·위치"). 본 문서의 스코프·우선순위·결정성 계약(§3~§6)은 이식 시에도 유지된다.
- 따라서 본 문서 본문에는 구체 파일 경로·형식 토큰을 두지 않는다 (§0, structure.md §5 C-3).
