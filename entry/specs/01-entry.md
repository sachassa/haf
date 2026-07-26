# entry/specs/01-entry — Entry Layer & Entry Resolution 정본

작성일: 2026-07-07
상태: v1.1 Baseline (CP2 첫 판정 Pass 15/0/0 · CP3 승인 · 사용자 승인 2026-07-07) · 2026-07-26 정합(격리 개정 — 슬림화·앵커 90ca19c)
상위 규약: AGENT.md (INV-1)
근거 정본:

- 사용자 승인 v1.1 실행 계획 (Project Discovery & Entry Layer Architecture) — 본 문서가 확정하는 내용(Entry 추상·Entry Descriptor 등록 모델·결정 테이블·판별 규칙·Evidence Source 확장 스키마)의 상위 정본. 특히 §"설계 골격 > uaf/specs/01-entry.md" 절과 결정 D3(Entry 판별)·D5(P1~P5)·D6-C1(Entry Resolution 확장성).
- ARCHITECTURE.md (v1.3) — UAF 상위 구조 정본. 특히 §2(구조·의존 방향)·§6(설계 원칙 10종)·§7(P1~P5·상시 불변 확인)·§8(UAF-INV 6건)·§10(책임 경계표)·§12(용어)·§12.2(Discovery Request 인터페이스 추상). **본 문서는 이 정본을 재정의·확장하지 않고 § 포인터로만 참조한다.**
- uahf/specs/00-glossary.md 0.2 (UAHF 용어 정본) — INV-3(Layer 정확히 6개)·용어 네임스페이스 분리의 근거. § 포인터로만 참조하며 UAHF 정본을 재정의하지 않는다.
- uahf/specs/TEMPLATE.md 0.1 — spec 문서 구조(§0~§9) 관행 참고.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본 배치 · 상위 정본 § 포인터 참조 (재정의·복제 0).** 이 문서는 **UAF specs 경계**의 최초 산출물이며 **UAF Entry Layer와 Entry Resolution의 정본**으로, ARCHITECTURE.md §2.2 요소 "Entry Layer → Entry Resolution"의 상세 계약을 소유한다. 상위 구조·원칙·불변·용어와 UAHF 계약 요소(ARCHITECTURE.md·uahf/specs/·uahf/framework/·상위 규약)는 각 정본이 소유하며, 본 문서는 이를 재정의·복제하지 않고 **§ 포인터로만 참조**한다. UAF와 UAHF의 유일한 접점은 Project Contract 하나다 (UAF-INV ① 접점 원칙, ARCHITECTURE.md §8).

- **INV-3 무촉 (Layer 어휘 주의).** "Entry Layer"의 "Layer"는 UAHF 6-Layer 스택(uahf/specs/00-glossary.md §3.2-A)의 지층(stratum)이 아니라 UAF 파이프라인의 한 **단계(stage)** 명칭이다 (ARCHITECTURE.md §0 용어 주의·§2.4). 본 문서는 UAHF Layer 수를 늘리는 서술을 두지 않으므로 Glossary INV-3("Layer는 정확히 6개다", uahf/specs/00-glossary.md §3.3)는 무촉이다.

- **논리 식별자 · Core 문서 관행.** `/new`·`/continue`·`/import`는 Entry의 **논리 식별자(name)**이며, 물리 진입 형태(어떤 진입 명령·선택·추론으로 발화되는가)는 Adapter 소관이다 (§4, AI-Agnostic — ARCHITECTURE.md §6 원칙 1). 본문에 특정 AI 이름·모델명·제품 기능명을 두지 않고(ARCHITECTURE.md §0 Core 문서 관행 동형), 구체 실현(명령의 물리 형태·직렬화 형식·환경 경로 관례)은 일반형 표기와 소관 포인터로만 가리킨다.

- **하류 경계 주의.** Discovery Request의 소비자인 Project Discovery의 상세 계약은 `discovery/specs/02-discovery.md`(실재 — v1.1 Baseline) 소관이다. 본 문서는 하류 내부 계약을 참조·추측하지 않으며, 두 문서가 공유하는 유일한 확정 인터페이스는 ARCHITECTURE.md §12.2의 Discovery Request 추상뿐이다.

---

## §1. 목적 (Purpose)

이 문서는 **UAF 공식 진입점(Entry Layer)이 사용자 입력을 어떻게 판별하여 Discovery Request로 해소하는가**를 확정한다. 책임은 세 가지다 — (i) Entry를 추상 연산으로 정의하고 Entry Layer의 유일한 연산 **Entry Resolution**의 입력·출력·완료 조건을 확정(§3.1), (ii) Entry를 고정 열거가 아니라 **Entry Registry의 데이터 레코드(Entry Descriptor)**로 모델링하고 그 위의 **고정 Resolution 엔진**·**결정 테이블(Policy as Data)**·**Evidence Source 확장 스키마**를 확정(§3.2), (iii) 신규 Entry가 **Layer·엔진 무변경으로 Registry 행·Policy 데이터 추가만으로** 확장됨을 등록 모델과 가상 `/import` 워크스루로 실증(§8).

### 본 문서가 실현하는 사용자 고정 원칙

- **P1 (ARCHITECTURE.md §7).** Entry Layer는 UAF 공식 진입점으로서 사용자 입력으로 진입 종류를 판별하고 **Entry Resolution만 담당**한다. Discovery를 수행하지 않으며, 출력은 **Discovery Request까지**다. 본 문서는 이 원칙을 재정의하지 않고 그 실현 계약을 확정한다.
- **D6-C1 (승인 계획 §Context D6).** Entry Resolution 확장성 — 신규 Entry는 Entry Layer·Resolution 엔진 **무변경**으로, **Registry 행·Policy 데이터 추가만으로** 확장 가능해야 한다. 검증 수단은 **Entry Descriptor 등록 모델(§3.2) + Evidence Source 확장 스키마(§3.2) + 가상 `/import` 등록 워크스루(§8)**다. 본 문서가 이 확장성 계약의 소유 정본이다.

### Non-Goals

- **Discovery 수행 제외.** 증거 수집·확신 판정·Project Contract 생성은 Project Discovery 소관이다 (ARCHITECTURE.md §10 책임 경계표, UAF-INV ④).
- **Discovery Request 추상 재정의 제외.** 3요소 구조({mode, inputs, policy})는 ARCHITECTURE.md §12.2 정본 추상이며, 본 문서는 산출이 그 추상에 정합함만 보인다.
- **Discovery Policy 값 상세 제외.** 임계값·예산·종료 규칙 등 정책 값의 상세 정본은 `discovery/specs/02-discovery.md`(실재 — v1.1 Baseline) 소관이며, 본 문서는 policy를 참조로만 다룬다.
- **사용자 흐름 시나리오 제외.** 운용 시나리오는 후속 운용 문서 소관이며, 본 문서의 `/import` 워크스루는 **등록 모델 수준**까지만이다 (§8).
- **물리 실현 제외.** 진입 명령의 물리 형태·직렬화 형식은 Adapter 소관이다 (§4).

---

## §2. 위치 (Position)

- **아키텍처 상 위치.** UAF 파이프라인의 최상류 단계다 — Entry Layer → Entry Resolution (ARCHITECTURE.md §2.2 6요소 중 첫 두 요소). UAHF 6-Layer 스택의 **외부**, 그보다 상위의 UAF 레벨 구조이며 UAHF Layer를 늘리지 않는다 (§0, ARCHITECTURE.md §2.4).
- **의존하는 정본 (읽기 전 이해 필요).**
  - ARCHITECTURE.md — §2(구조·의존 방향)·§6(원칙)·§7(P1~P5)·§8(UAF-INV)·§12(용어)·§12.2(Discovery Request 추상). 본 문서의 상위 계약.
  - uahf/specs/00-glossary.md — §3.2-A(UAHF 6-Layer)·§3.3(INV-3). Layer 어휘 네임스페이스 분리 근거.
- **이 문서에 의존하는 정본 (하류 소비자).**
  - `discovery/specs/02-discovery.md`(실재 — v1.1 Baseline) — Entry Resolution의 출력 Discovery Request를 소비한다. **단, 두 문서의 공유 계약은 ARCHITECTURE.md §12.2 확정 추상뿐이며, 본 문서는 하류 내부 계약을 참조·추측하지 않는다.**
- **순환 의존 없음.** 의존은 항상 본 문서 → ARCHITECTURE.md 방향이다 (ARCHITECTURE.md §2.5 의존 방향 단방향).

---

## §3. Core Contract (AI 비의존)

이 절에는 특정 AI 의존 내용이 한 줄도 들어가지 않는다 (uahf/specs/TEMPLATE.md §3, ARCHITECTURE.md §0 Core 문서 관행).

### §3.1 Interface — Entry & Entry Resolution 연산

**Entry (추상 연산).**

- **정의.** Entry는 UAF 공식 진입점으로서 사용자 입력을 수용하는 **추상 연산**이다 (ARCHITECTURE.md §12.1). 물리 실현(진입 명령의 형태)은 Adapter 소관이다 (§4, AI-Agnostic).
- **책임 한계.** Entry Layer가 수행하는 연산은 **Entry Resolution 하나뿐**이다. Entry는 Discovery를 수행하지 않고 Project Contract를 생성하지 않는다 (P1, UAF-INV ④; ARCHITECTURE.md §2.5·§7·§8).

**Entry Resolution (연산 계약).**

| 항목 | 계약 |
|---|---|
| **입력** | (i) **명시 Entry** — 발화된 Entry의 논리 식별자(name). (ii) **Workspace Evidence** — 판별에 필요한 확정 증거 집합. v1.1 정본 증거는 2종이다: Project Contract 유무, Repository 유무 (§3.2 Evidence 스키마). |
| **출력** | **Discovery Request 하나** — ARCHITECTURE.md §12.2가 확정한 3요소 구조 {mode, inputs, policy}. 그 이상(Discovery 수행·Project Contract·질문·전략)을 산출하지 않는다. |
| **완료 조건** | 입력 (명시 Entry × Workspace Evidence) 조합이 Entry Registry의 결정 테이블에서 **정확히 한 결과**로 해소되고, 그 결과가 §12.2 추상에 정합하는 Discovery Request로 방출된다 (결정성 불변, §3.3 EN-INV 3). |
| **실패 보고** | 해소 불가·미확정 입력은 임의 해석하지 않는다. 판별 실패 유형과 대응은 §6가 정의한다. 충돌·모호 입력은 policy에 **사용자 확인 게이트**를 표기해 하류로 전달하며(Preserve Human Authority, UAF-INV ⑤), Entry가 스스로 확정하지 않는다. |

**Entry 2종 (v1.1 등재).**

- **`/new`** — **순수 Greenfield 전용** 진입. 빈 워크스페이스에서 새 프로젝트를 시작하는 Discovery를 요청한다. 기본 Discovery mode = `greenfield`.
- **`/continue`** — 기존 프로젝트를 이어가는 진입. 증거에 따라 **Incremental Discovery**(Project Contract 존재 시) 또는 **Brownfield Full Discovery**(Contract 부재·Repository 존재 시, 최초 Contract 생성)를 요청한다.

두 Entry의 상세 Descriptor(필드·결정 행·mode 매핑)는 §3.2에 둔다.

### §3.2 Data Format — Entry Descriptor 등록 모델·결정 테이블·Evidence 스키마

#### §3.2-A Entry Descriptor 등록 모델 (D6-C1)

Entry는 코드에 고정된 열거가 아니라 **Entry Registry의 데이터 레코드**다. 하나의 레코드가 **Entry Descriptor**다.

**Entry Descriptor 필드 (5).**

| 필드 | 정의 |
|---|---|
| **name** | Entry의 논리 식별자 (예: `/new`, `/continue`). |
| **trigger** | 진입 트리거의 **논리** 서술. 물리 발화 형태(진입 명령의 형태)는 Adapter 소관이며 Descriptor는 논리 트리거만 담는다 (§4). |
| **requiredEvidence** | 이 Entry가 판별에 참조하는 **Evidence Source 종류 목록** (§3.2-C). 신규 Source 종류는 Evidence Source 확장 스키마로 추가된다. |
| **decisionRows** | 이 Entry의 **결정 테이블 행** — (Evidence 조합 → 결과) 매핑. 코드가 아닌 **데이터(Policy as Data)**다 (§3.2-D). |
| **modeMapping** | Evidence 조건별 **Discovery mode 매핑** — 이 Entry가 산출할 Discovery Request의 mode를 Evidence 조건에 따라 지정한다. mode는 확장 네임스페이스의 값이다 (§3.2-E, ARCHITECTURE.md §12.2). |

**Entry Registry.** Entry Descriptor 레코드의 집합이다. **신규 Entry 등록 = Registry에 Descriptor 행 1개 + 그 행이 참조하는 Policy 데이터(decisionRows·modeMapping·필요 시 Evidence Source 선언) 추가**뿐이다. Entry Layer와 Resolution 엔진은 변경되지 않는다 (§3.3 EN-INV 4).

**Resolution 엔진 (고정 알고리즘).** 엔진은 Registry 행을 평가하는 **고정 알고리즘**만 가진다 — 정책 지식을 코드에 담지 않는다.

1. **매칭.** 명시 Entry의 name으로 Registry에서 해당 Entry Descriptor를 찾는다.
2. **증거 수집.** Descriptor의 requiredEvidence가 지정한 Evidence Source들의 값을 관측한다 (관측만 — Entry는 증거를 수집·해석하는 Discovery를 수행하지 않는다; 유무 값의 확정 관측까지다).
3. **우선순위 평가.** Descriptor의 decisionRows를 **우선순위 순서**로 관측 증거에 대조하여 매칭되는 단일 결과 행을 선택한다.
4. **결정성 검증.** decisionRows는 각 Entry의 Evidence 값 공간을 **전수·상호배타로 분할**해야 한다 — 어떤 증거 조합도 두 개 이상의 결과 행에 매칭되지 않고(상호배타), 매칭되는 행이 없는 조합이 존재하지 않는다(전수). 이 검증은 등록 시점의 무결성 조건이며, 위반 Registry는 유효하지 않다.
5. **방출.** 선택된 결과를 §12.2 추상에 정합하는 Discovery Request {mode, inputs, policy}로 방출한다.

엔진은 이 5단계 외의 정책 분기를 갖지 않는다. 정책(어느 조합이 어느 결과가 되는가)은 전부 decisionRows·modeMapping·policy 데이터에 있다 (Policy as Data — ARCHITECTURE.md §6).

#### §3.2-B Discovery Request 매핑 (§12.2 정합 — 재정의 0)

Entry Resolution 산출의 3요소는 ARCHITECTURE.md §12.2 정본 추상에 다음과 같이 정합한다. **본 문서는 §12.2를 재정의하지 않고 채움 규칙만 명시한다.**

| §12.2 요소 | Entry Resolution의 채움 규칙 |
|---|---|
| **mode** | Entry Descriptor의 modeMapping을 관측 증거에 적용한 값. **닫힌 열거가 아니라 확장 네임스페이스**의 값이다 (§12.2). v1.1 초기 등재값: `greenfield` / `incremental` / `brownfield`. |
| **inputs** | 관측된 Workspace Evidence의 **참조 목록**. §12.2가 정한 대로 "Evidence 참조 목록"으로 일반화되며, 확정된 참조만 담는다(미완성·동시 작성 산출물 비참조). 신규 Evidence Source의 등록으로 확장된다 (§3.2-C). |
| **policy** | Discovery Policy **참조** (Policy as Data). 정책 값의 상세 정본은 `discovery/specs/02-discovery.md`(실재 — v1.1 Baseline) 소관이며, Entry는 참조만 담는다. 충돌 조합에서는 **사용자 확인 게이트를 포함하는 정책 번들**을 가리킨다 (§3.2-D 충돌 처리). |

#### §3.2-C Workspace Evidence & Evidence Source 확장 스키마 (D6-C1)

**Evidence Source (등록 스키마 — Capability 선언형).** 하나의 Evidence Source는 다음을 선언한다.

| 선언 항목 | 정의 |
|---|---|
| **sourceType** | Evidence Source의 식별자. |
| **capability** | 이 Source가 **무엇을 관측·판정하는가**의 Capability 선언 (Capability First — ARCHITECTURE.md §6). |
| **valueDomain** | 관측 값의 도메인 (예: 유/무 이진값, 또는 향후 등급·집합값). |

**v1.1 정본 Evidence 2종.**

| sourceType | capability | valueDomain |
|---|---|---|
| **contract-presence** | 워크스페이스에 **Project Contract가 존재하는가**를 관측한다. | 유 / 무 |
| **repository-presence** | 워크스페이스에 **Repository가 존재하는가**를 관측한다. | 유 / 무 |

**Workspace Evidence.** Entry Resolution 시점에 관측된 Evidence Source 값들의 집합이다. v1.1에서는 위 2종의 유/무 값이다.

**확장 개방.** 신규 Source 타입(예: 요구 문서·원격 저장소·외부 산출물)은 위 등록 스키마에 sourceType·capability·valueDomain을 **선언 등록**하는 것만으로 참여한다. Evidence Source의 추가는 Entry Layer·Resolution 엔진을 변경하지 않으며, Discovery Request의 inputs가 "Evidence 참조 목록"으로 일반화되어 있으므로 계약을 깨지 않는다 (§12.2 닫힘 없음 원칙, §3.3 EN-INV 4·5).

#### §3.2-D Entry Resolution 결정 테이블 (전 8조합 전수 열거 — 결정성 불변)

입력 조합은 **Entry 2종 × Contract 유무 × Repository 유무 = 8조합**이다. 각 조합은 **정확히 하나의 결과**(단일 Discovery Request)를 가진다 (결정성 불변, §3.3 EN-INV 3).

| # | Entry | Contract | Repo | → mode | policy | 근거 |
|---|---|---|---|---|---|---|
| 1 | `/new` | 무 | 무 | `greenfield` | 기본 | P-C (순수 Greenfield — `/new` 정상 경로) |
| 2 | `/new` | 무 | 유 | `greenfield` (잠정) | **충돌{repository-present}·게이트 = 사용자 확인** | P-D (Repo가 "순수 Greenfield" 전제와 상충) |
| 3 | `/new` | 유 | 무 | `greenfield` (잠정) | **충돌{contract-present}·게이트 = 사용자 확인** | **D3 ①** (`/new` + 기존 Contract → 사용자 확인) |
| 4 | `/new` | 유 | 유 | `greenfield` (잠정) | **충돌{contract-present}·게이트 = 사용자 확인** | **D3 ①** (`/new` + 기존 Contract → 사용자 확인) |
| 5 | `/continue` | 무 | 무 | `greenfield` (잠정) | **충돌{nothing-to-continue}·게이트 = 사용자 확인** | P-D (이어갈 증거 부재) |
| 6 | `/continue` | 무 | 유 | `brownfield` | 기본 | **D3 ②** (`/continue` + Contract 부재 + Repo 존재 → Brownfield Full Discovery, 최초 Contract 생성) |
| 7 | `/continue` | 유 | 무 | `incremental` | 기본 | **D3 ③** (`/continue` + Contract 존재 → Incremental Discovery) |
| 8 | `/continue` | 유 | 유 | `incremental` | 기본 | **D3 ③** (Contract 우선 — Contract 존재 시 Incremental) |

**판별 규칙 D3 (문면 3건).**

- **D3 ① — `/new` + 기존 Contract 존재 → 충돌 정책 = 사용자 확인.** `/new`는 순수 Greenfield 전용이므로 기존 Project Contract가 존재하면 사용자 의도와 증거가 상충한다. 충돌은 policy의 사용자 확인 게이트로 표기되며, Entry가 스스로 덮어쓰기·재라우팅을 결정하지 않는다 (Preserve Human Authority, UAF-INV ⑤). 결정 테이블 행 3·4에 실현된다.
- **D3 ② — `/continue` + Contract 부재 + Repository 존재 → Brownfield Full Discovery.** 기존 저장소가 있으나 아직 Contract가 없는 최초 도입은 `/continue`의 소관이다 (`/new`가 아님). mode = `brownfield`로 최초 Project Contract 생성을 요청한다. 결정 테이블 행 6에 실현된다.
- **D3 ③ — `/continue` + Contract 존재 → Incremental Discovery.** Project Contract가 이미 존재하면 그 계약을 기준선으로 이어가는 Incremental Discovery다. mode = `incremental`. Repository 유무와 무관하게 Contract 존재가 우선한다. 결정 테이블 행 7·8에 실현된다.

**나머지 조합의 도출 원칙 (D3 명시 밖 — 본 문서 확정).** D3는 위 3건(행 3·4·6·7·8)을 고정한다. 나머지 행(1·2·5)은 다음 원칙으로 단일 결과를 도출한다.

- **P-C (Greenfield 정상).** `/new` + Contract 무 + Repo 무 = 상충 증거 0 → `greenfield` 정상 경로 (행 1).
- **P-D (충돌 → 사용자 확인).** 명시 Entry의 전제와 관측 증거가 상충하면(행 2: `/new` 전제 vs Repo 존재; 행 5: `/continue` 전제 vs 이어갈 증거 부재) 임의 재라우팅 대신 policy에 사용자 확인 게이트를 표기한다 (Preserve Human Authority, UAF-INV ⑤). 이 원칙은 D3 ①의 충돌 처리와 동형이다.

**충돌 처리 정합.** 충돌 조합(행 2·3·4·5)에서도 Entry는 여전히 **Discovery Request 하나를 방출**한다 — 다만 그 policy가 사용자 확인 게이트를 포함하는 정책 번들을 가리킨다. Entry는 게이트를 **데이터로 표기**할 뿐 확정 결정을 내리지 않으며, 확정 게이트(사용자 승인)는 하류에서 존중된다 (P1 — Entry는 Resolution만; UAF-INV ⑤). 잠정 mode는 명시 Entry의 기본값이며, 사용자 확인의 결과로 다른 Entry가 재발화되면 결정 테이블이 다시 결정적으로 재해소된다(재해소도 단일 결과).

#### §3.2-E mode 네임스페이스 (§12.2 정합)

Discovery Request의 mode는 **닫힌 열거가 아니라 확장 가능한 네임스페이스**다 (ARCHITECTURE.md §12.2 — 재정의 0). v1.1 초기 등재값은 `greenfield` / `incremental` / `brownfield`다. 신규 진입·신규 발견 모드는 열거 변경 없이 네임스페이스에 등재되며, 이는 §8 확장 워크스루에서 실증된다.

### §3.3 Invariants (EN-INV — Entry 불변)

본 문서는 다음 불변을 어떤 구현·확장에서도 유지한다. 이들은 ARCHITECTURE.md의 상위 불변을 Entry 계약 수준에서 구속한다.

- **EN-INV 1 — Entry Resolution만.** Entry Layer의 산출은 **Discovery Request 하나**다. Entry는 Discovery를 수행하지 않으며 그 이상을 산출하지 않는다 (P1, UAF-INV ④; ARCHITECTURE.md §7·§8).
- **EN-INV 2 — Contract 직접 생성 금지.** Entry는 Project Contract를 직접 생성·수정하지 않는다. Contract 생성은 Project Discovery의 책임이다 (ARCHITECTURE.md §2.5·§10). Entry는 Contract를 Evidence(유/무)로만 **관측**한다.
- **EN-INV 3 — 결정성.** 동일 (명시 Entry × Workspace Evidence) 입력 조합은 항상 **단일** Discovery Request로 해소된다. Registry의 decisionRows는 각 Entry의 Evidence 값 공간을 전수·상호배타로 분할한다 (§3.2-A 결정성 검증, §3.2-D 8조합 전수 열거).
- **EN-INV 4 — Layer·엔진 불변 확장.** 신규 Entry·신규 Evidence Source·신규 mode의 추가는 **Registry 행·Policy 데이터·Evidence Source 선언의 추가로만** 이뤄지며, Entry Layer와 Resolution 엔진의 고정 알고리즘을 변경하지 않는다 (Future Extensibility·Capability First·Policy as Data — ARCHITECTURE.md §6; D6-C1).
- **EN-INV 5 — Discovery Request 정합·재정의 0.** Entry Resolution의 산출은 ARCHITECTURE.md §12.2가 확정한 Discovery Request 추상({mode, inputs, policy})에 정합하며, 본 문서는 그 추상을 재정의·확장하지 않는다. mode는 확장 네임스페이스, inputs는 Evidence 참조 목록이다.
- **EN-INV 6 — 확정 게이트 보존.** Entry는 확정 결정을 내리지 않는다. 충돌·모호 입력은 policy에 사용자 확인 게이트로 표기하여 Preserve Human Authority(UAF-INV ⑤)를 하류로 전달한다.

**상시 불변 확인 정합 (ARCHITECTURE.md §7.1).** 본 문서는 ARCHITECTURE.md §7.1의 상시 불변 확인 2건을 훼손하지 않는다 — (i) Project Discovery는 교체 가능한 Compiler로 남으며, 본 문서는 Discovery 내부 개념(질문·전략·예산)을 Entry 계약에 끌어들이지 않는다(EN-INV 1·2). (ii) Project Contract의 Stable Contract 지위를 건드리지 않는다 — Entry는 Contract를 유/무 증거로만 관측하고 그 스키마·내용을 다루지 않는다(EN-INV 2). Entry가 Discovery를 수행하거나 Contract를 컴파일한다는 서술은 본 문서에 0건이다.

---

## §4. Adapter Binding (환경 의존)

### §4.1 바인딩 대상

- **진입 트리거의 물리 형태.** Entry Descriptor의 trigger는 논리 서술이며, 그 물리 발화 형태(어떤 진입 명령·선택·추론으로 Entry가 발화되는가)는 Adapter가 바인딩한다. Core Contract는 논리 name·trigger만 소유한다 (§3.2-A).
- **Workspace Evidence 관측의 물리 실현.** contract-presence·repository-presence를 실제 환경에서 어떻게 탐지하는가(경로 관례·직렬화 형식·존재 판정 수단)는 Adapter 소관이다. Core Contract는 capability 선언과 유/무 값 도메인만 소유한다 (§3.2-C).
- **Discovery Request 직렬화.** {mode, inputs, policy}의 물리 직렬화·전달 방식은 Adapter 소관이다.

### §4.2 이식 교체 지점

다른 AI·실행 환경으로 이식할 때 바뀌는 것: 진입 트리거의 물리 형태, Evidence 관측의 물리 수단, Discovery Request의 직렬화. **바뀌지 않는 것**: Entry Descriptor 등록 모델·Resolution 엔진의 고정 알고리즘·결정 테이블 데이터·Evidence Source 선언 스키마·Discovery Request 추상 정합 — 이들은 전부 Core Contract(§3)이며 이식 시 유지된다.

---

## §5. Memory Access (해당 시)

**해당 없음.** Entry Resolution은 Memory Service를 회수·기록하지 않는다. Memory Consult는 하류 UAHF 소관(비담당)이며 Discovery조차 Memory 활용은 v1.1에서 **확장 포인트로만** 열려 있다 (ARCHITECTURE.md §10 책임 경계표·§11 Non-Goals). Entry는 그보다 상류이므로 Memory에 접근하지 않는다.

---

## §6. Failure Modes

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| **미등록 Entry 발화** — 명시 name이 Registry에 없다. | 임의 해석하지 않는다. 판별 실패로 보고하고, 확장이 필요하면 Registry 등록 절차(§3.2-A)로 처리한다. Entry Layer·엔진은 변경하지 않는다. | 후보 |
| **증거-의도 충돌** — 명시 Entry의 전제와 관측 증거가 상충한다(예: `/new` + 기존 Contract). | 결정 테이블이 정의한 충돌 행으로 해소하되, policy에 사용자 확인 게이트를 표기해 하류에 위임한다. Entry가 임의 재라우팅·덮어쓰기를 결정하지 않는다 (D3 ①, EN-INV 6). | 후보 |
| **결정성 위반 Registry** — decisionRows가 어떤 조합에 대해 결과가 없거나 둘 이상이다. | 결정성 검증(§3.2-A 4단계)에서 무효 Registry로 거부한다. 전수·상호배타 분할을 만족하도록 Policy 데이터를 정정한다. | 후보 |
| **미완성 하류 계약 추측 유혹** — Discovery 측 상세 계약이 필요해 보인다. | 추측하지 않는다. 공유 계약은 ARCHITECTURE.md §12.2 확정 추상뿐이며, 그 이상이 필요하면 Advisor에게 에스컬레이션한다 (병렬 경계, §0). | 후보 |

---

## §7. Verification

### 완료 기준 (시연 가능 문장)

판정은 아래 항목을 지목 절 문면과 직접 대조해 내린다(여기서 §3을 재서술하지 않는다). 괄호는 원 done 번호다.

1. 추상·비수행(Entry Resolution만 · 출력은 Discovery Request까지 · Discovery 수행/Contract 생성 서술 0건) — §3.1·EN-INV 1·2 (done 10)
2. 등록 모델(Descriptor 5필드 · 엔진 고정 5단계 = 우선순위 + 결정성 검증) — §3.2-A
3. 결정 테이블 8조합(2×2×2) 열거·결정성(각 조합 단일 결과 — 중복·누락 0) — §3.2-D·EN-INV 3
4. 판별 규칙 D3 3건 ↔ 결정 행 대응(① 행 3·4 / ② 행 6 / ③ 행 7·8) — §3.2-D
5. Discovery Request 정합·재정의 0 — §3.2-B ↔ ARCHITECTURE.md §12.2 (done 8)
6. Evidence Source 확장 스키마 개방(v1.1 Evidence 2종 + Capability 선언형 등록) — §3.2-C (done 7)
7. 확장 무변경(변경 목록 = Registry 행 + Policy 데이터 + Evidence Source 선언뿐 · Layer·엔진 문면 변경 0) — §8 예 3·D6-C1 (done 9)

### 검증 방법 (Verifier)

- Verifier가 §3.2-D 표의 행 수(8)와 각 행의 단일 결과를 센다.
- Verifier가 D3 3건과 결정 테이블 행의 대응을 대조한다.
- Verifier가 §3.2-B와 ARCHITECTURE.md §12.2를 직접 대조해 재정의 0을 확인한다.
- Verifier가 §8 워크스루의 변경 목록에 Entry Layer·엔진 변경이 없음을 확인한다.
- Verifier가 본문 전체를 특정 AI 실명·모델명·제품 기능명 다중 패턴으로 전수 스캔해 0건을 확인한다.

---

## §8. Examples

### 예 1 — Entry Resolution (결정 테이블 적용)

**입력.** 명시 Entry = `/continue`; Workspace Evidence = {contract-presence: 유, repository-presence: 유}.

**해소 (Resolution 엔진 5단계).**

1. 매칭 — `/continue` Descriptor를 Registry에서 찾는다.
2. 증거 수집 — requiredEvidence(contract-presence·repository-presence)를 관측: {유, 유}.
3. 우선순위 평가 — decisionRows 대조: Contract 존재가 우선(§3.2-D 행 8).
4. 결정성 검증 — 이 조합은 단일 행(8)에만 매칭.
5. 방출 — Discovery Request { mode: `incremental`, inputs: [contract-presence(유), repository-presence(유)], policy: 기본 정책 참조 }.

**결과.** Incremental Discovery 요청 (D3 ③). Entry는 여기서 멈춘다 — Discovery 수행·Contract 생성은 하지 않는다.

### 예 2 — 충돌 조합 (사용자 확인 게이트)

**입력.** 명시 Entry = `/new`; Workspace Evidence = {contract-presence: 유, repository-presence: 무}.

**해소.** §3.2-D 행 3에 매칭 → Discovery Request { mode: `greenfield`(잠정), inputs: [contract-presence(유), repository-presence(무)], policy: 충돌{contract-present} 게이트=사용자 확인 정책 참조 }.

**결과.** `/new`(순수 Greenfield 전용)와 기존 Contract가 상충한다(D3 ①). Entry는 덮어쓸지 이어갈지 **스스로 결정하지 않고** policy에 사용자 확인 게이트를 표기해 하류로 전달한다 (Preserve Human Authority, EN-INV 6). 사용자가 `/continue`를 재발화하면 결정 테이블이 행 7로 결정적으로 재해소된다.

### 예 3 — 가상 `/import` 등록 워크스루 (D6-C1 실증 — 등록 모델 수준)

**확장 규칙 (§3.2-A·C·E의 적용 형태).** 신규 Entry 등록의 변경 목록은 항상 **Evidence Source 선언(필요 시) + Entry Descriptor 행 + decisionRows·modeMapping·policy 데이터 + mode 네임스페이스 등재**뿐이며, Entry Layer·Resolution 엔진·Discovery Request 추상은 변경되지 않는다 (EN-INV 4·D6-C1). 아래는 가상 Entry `/import`(외부 산출물을 Discovery 씨앗으로 도입) 1건의 적용 예이며, **등록 모델 수준까지만** 다룬다 (§1 Non-Goals).

**변경되는 것 (4건).**

1. **Evidence Source 선언 추가** (§3.2-C) — sourceType `external-deliverable-presence` / capability "지정된 외부 산출물이 존재·접근 가능한가를 관측한다" / valueDomain 유·무.
2. **Entry Descriptor 행 추가** (§3.2-A) — name `/import` · trigger(논리 — 물리 형태는 Adapter 소관) · requiredEvidence [external-deliverable-presence, contract-presence] · decisionRows(외부 산출물 유 + Contract 무 → import 정상 / 외부 산출물 유 + Contract 유 → 충돌·사용자 확인 / 외부 산출물 무 → 판별 실패 — 각 조합 단일 결과·상호배타 분할) · modeMapping(외부 산출물 유 → mode `import`).
3. **mode 네임스페이스 등재** (§3.2-E) — `import` 등재. 열거 변경이 아니므로 Discovery Request 계약은 불변이다(§12.2).
4. **policy 데이터 추가** — 결정 행이 참조할 정책 번들(정상·충돌 게이트).

**변경되지 않는 것 (3건 — D6-C1 핵심 실증).** Entry Layer(진입점 추상) · Resolution 엔진(고정 5단계 = 매칭 → 증거 수집 → 우선순위 평가 → 결정성 검증 → 방출) · Discovery Request 추상(mode는 확장 네임스페이스이므로 스키마 변경 0 · inputs는 Evidence 참조 목록이므로 신규 참조를 담아도 계약 불변).
