# planning/specs/03-project-contract — Project Contract Specification

작성일: 2026-07-07
상태: v1.3 Baseline (개정 — §3.3-E 스키마 개정 요건의 기록 locus 를 git 으로 이전 · 계보 append-only 와의 경계 명시. 사용자 결정 2026-07-27)
상위 규약: AGENT.md (INV-1)
근거 정본:

- 사용자 승인 v1.1 실행 계획 (Project Discovery & Entry Layer Architecture) — 본 문서가 확정하는 내용(지위·논리 스키마·필수 코어 필드·Dimension→필드 매핑·버저닝 전략·인스턴스 거버넌스·역참조 금지 불변·UAHF Interface)의 상위 정본. 특히 §"설계 골격 > uaf/specs/03-project-contract.md" 절과 결정 **D5-P3**(Stable Contract)·**D6-C2**(Contract Versioning)·**D2④**(UAHF 하위 호환 — Contract=선택 입력).
- ARCHITECTURE.md — UAF 상위 구조 정본. 특히 §2.2(6요소 구조)·§2.5(의존 방향 단방향)·§6(설계 원칙 12종)·§7 P3(§7)·§7.1(상시 불변 확인 2건)·§8 UAF-INV ①②③⑤(§8)·§10(책임 경계표)·§11(Non-Goals)·§12.1·§12.2(Discovery Request 추상). **본 문서는 이 정본을 재정의·확장하지 않고 § 포인터로만 참조한다.**
- discovery/specs/02-discovery.md (v1.1 Draft) — Project Discovery 정본. 특히 §3.1(Compiler·불완전 출력 금지)·§3.3-A(mode 분기)·§3.7(Execution Ready 2축 판정·Readiness 선언 구성·필수 코어 필드 추상 참조)·§3.11(Discovery Dimension 5·"Contract 매핑은 W4 소유" 위임). Discovery의 산출인 본 Contract의 완결 기준을 소비하는 상류 계약.
- entry/specs/01-entry.md (v1.1 Draft) — Entry Layer & Entry Resolution 정본. 특히 §3.1·§3.2-C(contract-presence)·EN-INV 2 — Entry는 Project Contract를 **유/무 증거로만 관측**하고 스키마·내용을 다루지 않는다.
- uahf/specs/00-glossary.md 0.2 — UAHF 용어 정본. 네임스페이스 분리의 근거. 특히 §3.2-C(Memory Service Interface)·§3.2-E(Agent 역할)·§3.2-F(Agent Lifecycle의 Consult)·§3.2-G(Spec Status: Frozen). UAHF 용어는 § 포인터로만 참조한다.
- uahf/specs/12-scaffold.md 0.1 — Scaffold 정본. 특히 §3.2-A(Project Template) — Contract가 신규 프로젝트 설치 시 배치되는 정본 문서로 성립하는 소비 지점의 근거(§3.5-B).
- uahf/specs/TEMPLATE.md 0.1 — spec 문서 구조(§0~§9)·품질 기준 관행.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본 배치 · 논리 스키마만.** 이 문서는 **UAF specs 경계**의 **Project Contract 정본**이며, UAF 파이프라인 6요소 중 **Project Contract** 요소(ARCHITECTURE.md §2.2)의 상세 계약 — **논리 스키마·버저닝·UAHF Interface** — 를 소유·최종 고정한다. Project Contract는 UAF와 UAHF의 **유일한 접점**이다(ARCHITECTURE.md §8 UAF-INV ①). 정의 범위는 **논리 스키마**(필드 그룹·필드·의미·불변)뿐이며 **직렬화 형식·물리 포맷·저장 위치**는 Adapter 소관이다(§4) — 이 경계가 AI-Agnostic 원칙의 스키마 측 실현이다(ARCHITECTURE.md §6 원칙 1).

- **UAF·UAHF 상위 정본 § 포인터 참조 (재정의·확장 0).** 이 문서는 UAF 상위 구조(ARCHITECTURE.md)와 UAHF 정본(ARCHITECTURE.md·uahf/specs/·uahf/framework/·상위 규약)을 **재정의·확장하지 않고 § 포인터로만 참조**한다. 특히 §3.5 UAHF Interface는 UAHF spec의 어떤 연산·필드·불변도 추가·변경하지 않는다(UAF-INV ① 접점 원칙).

- **선행 인터페이스만 소비.** 상위 근거는 ARCHITECTURE.md와 discovery/specs/02-discovery.md의 **확정 계약**이다. Discovery는 이 Contract를 산출하는 상류 Compiler이며(02-discovery §3.1), 본 문서는 그 산출의 완결 기준·필수 코어 필드·Dimension 매핑을 고정하여 02-discovery §3.7·§3.11의 위임을 해소한다.

- **AI 비의존 · 네임스페이스 분리.** 본문 전체(특히 §3 Core Contract)에 특정 AI 이름·모델명·제품 기능명·방법론 고유명을 두지 않고(uahf/specs/TEMPLATE.md §3, ARCHITECTURE.md §0 동형), 구체 실현(직렬화 형식·저장 위치·환경 경로 관례)은 Adapter Binding 소관 포인터로만 가리킨다(§4). 본 문서가 소유하는 스키마 용어(필드 그룹명·`schemaVersion`·`instanceVersion`·tolerant reader·opaque annex·supersedes 등)는 본 문서 정의로만 확정하며, UAHF Glossary 동명 용어는 § 포인터로 참조하고 재정의하지 않는다(ARCHITECTURE.md §12 동형). 새 UAHF 용어는 신설하지 않는다.

---

## §1. 목적 (Purpose)

이 문서는 **Project Contract가 UAF와 UAHF를 잇는 공식 Stable Contract(Public API)로서 무엇을 담고 어떻게 장기 호환을 유지하는가**를 확정한다. 책임은 네 가지다 — (i) **지위**(Stable Contract·Public API)와 **논리 스키마 전용** 경계 명문화(§3.1, P3·D5), (ii) **논리 스키마**(필드 그룹 9종·필수 코어 필드·Dimension→필드 매핑) 확정(§3.2), (iii) **버저닝 전략**(schemaVersion/instanceVersion 분리·SemVer·tolerant reader·필드 제거 금지)과 **인스턴스 거버넌스** 확정(§3.3·§3.4, D6-C2), (iv) **UAHF Interface**(선택 입력·소비 지점·UAHF 무수정 근거·확장 포인트)와 불변(PC-INV) 확정(§3.5·§3.6, D2④).

### 본 문서가 실현하는 정본 결정

- **P3 (ARCHITECTURE.md §7).** Project Contract = UAF↔UAHF 공식 **Stable Contract(Public API)**. Discovery는 교체 가능하되 Contract는 장기 유지된다. 접점은 이 계약 하나뿐이다. 본 문서는 이 지위를 재정의하지 않고 그 스키마·버저닝 상세를 고정한다.
- **D6-C2 (승인 계획 §Context D6).** Contract Versioning — `schemaVersion`은 SemVer 규율(MINOR = 후방 호환 추가만·MAJOR = 원칙 금지·마이그레이션 필수), 소비자는 tolerant reader(미지 필드 must-ignore), 필드 제거 금지·deprecation 정책. Discovery 내부 변경과 독립적으로 장기 호환을 유지한다. 본 문서가 이 버저닝 계약의 소유 정본이다(§3.3).

### Non-Goals

- **직렬화·물리 포맷·저장 위치 비정의.** Contract의 물리 표현은 Adapter 소관이다(§4). 본 문서는 논리 스키마만 정의한다.
- **Discovery 내부 설계 비정의.** State Machine·Strategy·Confidence·Question Budget 등 Discovery의 오케스트레이션·모듈 계약은 discovery/specs/02-discovery.md 소관이다. 본 문서는 Discovery의 **산출 계약**만 소유한다.
- **UAHF 계약 변경 비수행.** UAHF의 연산·필드·불변을 추가·변경하지 않는다. Contract의 UAHF 소비는 기존 UAHF 관행으로 성립하며, 정식 등재는 확장 포인트로만 남긴다(§3.5, UAF-INV ①).
- **Discovery 실행 호스팅·Memory 활용 비설계.** ARCHITECTURE.md §11 Non-Goals와 정합한다. 본 문서는 데이터 계약이므로 Memory에 접근하지 않는다(§5).

---

## §2. Position

- **아키텍처 상 위치.** UAF 파이프라인의 **Project Contract** 요소다(ARCHITECTURE.md §2.2). UAHF 6-Layer 스택의 지층(Layer)이 아니라, 그 **외부·상류의 UAF 레벨 구조**이며 UAHF와 UAF의 **유일 접점**이다(ARCHITECTURE.md §2.4, uahf/specs/00-glossary.md §3.3 INV-3 무촉). Discovery의 산출이자 UAHF의 선택 입력이다.

- **의존하는 정본 (읽기 전 이해 필요).**
  - ARCHITECTURE.md (실재, v1.3) — §2(구조·의존 방향)·§6(원칙)·§7 P3(§7)·§7.1(상시 불변)·§8 UAF-INV ①②③⑤·§10(책임 경계)·§11(Non-Goals)·§12.2(Discovery Request). 본 문서의 최상위 근거.
  - discovery/specs/02-discovery.md (실재, v1.1 Draft) — §3.1 Compiler·§3.7 Execution Ready 2축 판정·§3.11 Discovery Dimension. 본 Contract를 산출·소비하는 상류.
  - entry/specs/01-entry.md (실재, v1.1 Draft) — §3.2-C contract-presence. Entry가 Contract를 유/무 증거로만 관측함의 근거.
  - uahf/specs/00-glossary.md (실재, Frozen 0.2) — UAHF 용어 정본·네임스페이스 분리 대조 기준. 특히 §3.2-C·§3.2-E·§3.2-F·§3.2-G·§3.2-J.
  - uahf/specs/TEMPLATE.md (실재, Frozen 0.1) — 문서 구조·품질 기준.

- **이 문서에 의존하는 문서 (dependents).**
  - discovery/specs/02-discovery.md — 필수 코어 필드·완결 기준·Dimension 매핑을 본 문서가 확정함으로써 §3.7·§3.11의 추상 참조가 해소된다(§3.2-B·§3.2-C). Discovery의 종단 판정(Compiling)은 본 스키마를 타깃으로 컴파일한다.
  - (구현 버전, 예정) — UAHF 측 Contract 정식 소비 경로. 본 문서는 확장 포인트로만 표기한다(§3.5).

- **순환 의존 없음.** 의존은 항상 본 문서 → ARCHITECTURE.md·02-discovery 방향이다. Contract는 하위 요소(UAHF·Execution)나 Discovery 내부 개념을 역참조하지 않는다(ARCHITECTURE.md §2.5 의존 방향 단방향; 역참조 금지 불변, §3.6 PC-INV 2).

---

## §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 환경 의존 실현은 §4에 둔다.

### 3.1 Interface — 지위·논리 스키마·입출력

#### 3.1-A 지위 (Stable Contract · Public API)

**Project Contract는 UAF↔UAHF 공식 Stable Contract(Public API)다**(P3, ARCHITECTURE.md §7·§8 UAF-INV ①②).

- **공식 안정 계약.** Contract는 UAF와 UAHF를 잇는 공식 계약이며 장기 호환을 유지한다. **Discovery는 교체 가능하되(UAF-INV ②) Contract의 스키마는 안정성을 유지한다(교체 불가).** 안정 계약이 교체 가능한 생산자(Discovery)를 흡수한다.
- **유일 접점.** UAF와 UAHF의 접점은 이 계약 하나뿐이다. 다른 어떤 요소도 UAHF에 직접 닿지 않는다(ARCHITECTURE.md §2.5).
- **논리 스키마 전용.** 본 문서는 **논리 스키마만** 정의한다. 직렬화·물리 포맷·저장 위치는 정의하지 않으며 Adapter 소관이다(§4). 지위와 스키마는 물리 실현과 무관하게 유지된다.

#### 3.1-B 연산 계약

| 항목 | 계약 |
|---|---|
| **생산자** | 두 생산 경로가 있다. **(i) 최초 인스턴스** — Project Discovery의 Back-end(Contract Compiler)가 단일 타깃 형식으로 컴파일한다(discovery/specs/02-discovery.md §3.1). **(ii) superseding 성숙 인스턴스** — Solution Design(정본 `planning/specs/04-solution-design.md`)이 Ready 종단 인스턴스 vN을 기준선으로 superseding 인스턴스 v(N+1)을 재발행한다(§3.4 동일 supersedes 메커니즘·사용자 승인 게이트 통과 — 정본 04). 두 경로 모두 **불완전 Contract를 산출하지 않는다** — Compiler는 불완전 출력을 내지 않고 성숙 재발행은 완결 인스턴스만 산출한다(§3.7 Completeness 불가침 정합, §3.6 PC-INV 7). |
| **소비자** | UAHF는 Contract를 **선택 입력**으로 소비한다 — **tolerant reader**로서 **필수 코어 필드만 의존**하고 미지 필드·부속 네임스페이스는 must-ignore한다(§3.3-C). 부재 시 UAHF는 기존 방식으로 운용된다(하위 호환, §3.5, D2④). |
| **완결 기준** | 필수 코어 필드(§3.2-B)가 전건 충족(실측 또는 가정)되고 Readiness가 선언되어야 유효한 Ready Contract다(02-discovery §3.7 축 1 Completeness). 완결 기준 = 필수 코어 필드 전건 충족. |
| **불변 준수** | 스키마 본문(코어 필드 정의)에 Discovery 내부 개념 참조 0건(Provenance 부속 제외, §3.6 PC-INV 2). 버저닝은 SemVer·tolerant reader·필드 제거 금지를 지킨다(§3.6 PC-INV 4·5·6). |

### 3.2 Data Format — 논리 스키마

#### 3.2-A 필드 그룹 (9종)

Project Contract의 논리 스키마는 **9개 필드 그룹**으로 구성된다. 아래 표가 정본이다. 각 그룹은 논리 필드와 의미만 정의하며, 물리 표현은 Adapter 소관이다(§4).

| # | 필드 그룹 | 논리 구성 | 의미 |
|---|---|---|---|
| 1 | **Meta** | `id` · `schemaVersion` · `instanceVersion` · 계보(`supersedes`) | Contract 인스턴스의 식별과 버전. `id`는 인스턴스 논리 식별자, `schemaVersion`은 스키마 버전(§3.3), `instanceVersion`은 인스턴스 버전(§3.4), `supersedes`는 대체한 이전 인스턴스의 계보 참조. |
| 2 | **Intent** | 프로젝트 의도 서술 | 프로젝트가 이루려는 목적·해결하려는 문제. "무엇을 왜 하는가." |
| 3 | **Requirements** | 기능 요구 · 품질 요구 | 프로젝트가 충족해야 할 기능·품질 요구. "무엇을 만족해야 하는가." |
| 4 | **Constraints** | 제약 목록 | 기술·자원·정책·시간상의 제약. "무엇에 매여 있는가." |
| 5 | **Risks** | 리스크 목록 | 불확실성·위협·실패 가능 지점. "무엇이 어긋날 수 있는가." |
| 6 | **Architecture Direction** | 결정 · 미결 | 아키텍처 방향과 주요 설계 결정·미결 사항. "어떻게 구성할 것인가." |
| 7 | **Assumption Ledger** | 가정 원장(가정 항목의 기록) | 실측이 아닌 **가정**으로 충족한 항목의 원장. 각 가정은 대상 필드·근거·미해결 상태를 담는다. Ready에서는 비어 있을 수 있고, ReadyWithAssumptions에서는 비어 있을 수 없다(§3.2-B). |
| 8 | **Readiness** | Completeness 판정 · Confidence Vector · 미해결 질문 목록(Open Questions) · 사용자 승인 기록 | **Execution Ready 선언**의 기록. 종단 판정의 산출을 담는다(02-discovery §3.7 Readiness 선언 구성). 구성 요소는 §3.2-B 아래 경계 문면 참조. |
| 9 | **Provenance** | 생성 Discovery 실행 메타 (**불투명 부속 — opaque annex**) | 이 Contract를 생성한 Discovery 실행의 메타. **불투명 부속이며 UAHF는 소비하지 않는다(must-ignore).** 내부 구조는 본 스키마가 정의하지 않으며 Discovery 측(discovery/specs/02-discovery.md §3.5·§3.16)·Adapter 측 소관이다. 상세는 §3.2-D. |

**Readiness 구성의 경계 문면 (역참조 금지 정합 — 중요).** Readiness의 **Confidence Vector · Assumption Ledger(참조) · 미해결 질문 목록(Open Questions)**은 02-discovery §3.7 "Readiness 선언의 구성"이 규정한 종단 판정의 **산출 기록**이다. 이들은 Contract가 기록하는 **결과**이며, Discovery의 **내부 개념**(질문 선택·전략·예산 집행·Strategy·Capability — HOW 발견이 수행되었는가의 기계)이 **아니다**. 특히 "미해결 질문 목록(Open Questions)"의 '질문'은 Contract가 남기는 미해결 사항이며, Discovery 내부의 '질문 선택' 기계와 다르다. 따라서 이 산출 기록은 §3.6 PC-INV 2 역참조 금지의 대상이 아니다. 반대로 코어 필드 정의(위 9종 그룹 1~8)에는 Discovery 내부 개념이 0건이다(Provenance 부속 제외).

#### 3.2-B 필수 코어 필드 (Required Core Fields)

**필수 코어 필드**는 유효한 Ready Contract가 반드시 충족해야 하는 필드의 집합이다. 이 목록이 discovery/specs/02-discovery.md §3.7 축 1 **Contract Completeness**("필수 코어 필드 전건 충족")의 **판정 대상**이며, 02-discovery §3.7·§0의 추상 참조("필수 코어 필드의 정의·목록은 03-project-contract.md 소관")가 **본 절에서 해소**된다.

| 필수 코어 필드 | 소속 그룹 | 충족(satisfied) 의미 |
|---|---|---|
| `id` | Meta | 인스턴스 논리 식별자가 존재한다. |
| `schemaVersion` | Meta | 스키마 버전이 표기된다(§3.3). |
| `instanceVersion` | Meta | 인스턴스 버전이 표기된다(§3.4). |
| **Intent** | Intent | 프로젝트 의도가 충족된다 — 비어 있을 수 없다. |
| **Requirements** | Requirements | 최소 기능 요구를 포함하여 충족된다. |
| **Constraints** | Constraints | 충족된다 — 명시적 공집합("없음")도 충족으로 인정된다. |
| **Risks** | Risks | 충족된다 — 명시적 공집합("없음")도 충족으로 인정된다. |
| **Architecture Direction** | Architecture Direction | 충족된다 — 결정·미결이 표기된다(미결의 명시도 충족). |
| **Readiness** | Readiness | Completeness 판정·Confidence Vector·미해결 질문 목록·사용자 승인 기록을 포함하여 존재한다. |
| **Assumption Ledger** | Assumption Ledger | 구조 요소로 존재한다. Ready에서는 빈 원장이 허용되고, ReadyWithAssumptions에서는 비어 있을 수 없다. |

**충족의 의미 (02-discovery §3.7 정합).**

- **충족 = 실측 또는 가정.** 각 필수 코어 필드는 **실측**으로 채워지거나 **가정**으로 채워진다. 가정으로 충족한 항목은 Assumption Ledger에 기재된다. `Ready`는 필수 필드를 실측으로, `ReadyWithAssumptions`는 필수 필드를 **가정으로** 충족시키고 원장에 기재한다(02-discovery §3.7 축 1).
- **Completeness는 타협 불가.** 필수 코어 필드는 **모든 Ready 종단에서 전건 충족**되어야 한다. Compiler는 불완전 Contract를 산출하지 않는다(02-discovery §3.1·§3.7, §3.6 PC-INV 7).
- **Provenance는 비-코어.** Provenance는 필수 코어 필드가 **아니다**. 불투명 부속이며 Completeness 판정 대상이 아니고 UAHF 소비 대상도 아니다(§3.2-D). tolerant reader는 Provenance를 must-ignore한다(§3.3-C).

#### 3.2-C Discovery Dimension → Contract 필드 매핑 (컴파일 방향)

discovery/specs/02-discovery.md §3.11은 "각 차원의 이해가 Project Contract의 어느 필드로 컴파일되는가 … 그 스키마 정본은 03-project-contract.md 소관"으로 위임했다. 본 절이 그 **컴파일 방향 매핑**을 확정하여 위임을 해소한다.

| Discovery Dimension (02-discovery §3.11) | → | Contract 필드 그룹 (§3.2-A) |
|---|---|---|
| Intent | → | Intent |
| Requirement | → | Requirements |
| Constraint | → | Constraints |
| Risk | → | Risks |
| Architecture | → | Architecture Direction |

- **컴파일 방향만.** 이 표는 Discovery의 Back-end(Contract Compiler)가 **Discovery → Contract 방향으로** 각 차원의 이해를 어느 필드 그룹으로 컴파일하는가만 정의한다(02-discovery §3.1 Back-end).
- **역방향 의존 없음.** 이 매핑은 **컴파일 경계 주석**이며 코어 필드 정의(§3.2-A 그룹 정의)의 일부가 아니다. Contract 스키마는 Discovery Dimension을 **스키마 의존으로 import하지 않는다** — 필드 그룹은 자기완결적으로 정의되며, Dimension이 사라지거나 교체되어도 필드 그룹 정의는 불변이다. 매핑은 생산 시점의 컴파일 대응일 뿐, Contract가 Discovery를 역참조하게 만들지 않는다(§3.6 PC-INV 2, ARCHITECTURE.md §2.5 의존 방향).
- **Strategy Invariance 정합.** 어떤 Strategy로 발견하든 같은 Dimension은 같은 필드 그룹으로 컴파일된다 — 출력 스키마·완결 기준은 불변이다(ARCHITECTURE.md §8 UAF-INV ③, 02-discovery §3.8 DISC-INV-7).

#### 3.2-D Provenance — 불투명 부속 (Opaque Annex)

- **불투명.** Provenance는 이 Contract를 생성한 Discovery 실행의 메타를 담는 **불투명 부속**이다. **UAHF는 이를 소비하지 않는다(must-ignore, §3.3-C).**
- **내부 구조 비정의.** 본 스키마는 Provenance의 내부 구조를 정의하지 않는다. Discovery 실행 기록의 내부 형식은 Discovery 측(discovery/specs/02-discovery.md §3.5 Event 로그·§3.16 Metrics)·Adapter 측 소관이며, 본 문서는 그 소유 지점을 포인터로만 표기한다.
- **격리 근거.** Discovery 내부 변경(기법·전략·예산·질문 방식의 변화)은 오직 이 부속과 `instanceVersion`에만 반영되고 **코어 스키마·`schemaVersion`에 도달하지 못한다**(§3.4, §3.6 PC-INV 2·3). 이 격리가 Discovery 교체 가능성을 스키마 측에서 보존한다(상시 불변 ①, §3.6 PC-INV 10).

### 3.3 버저닝 전략 (Versioning — D6-C2)

#### 3.3-A schemaVersion / instanceVersion 분리

두 버전을 분리한다.

- **`schemaVersion`** — **스키마 버전**. Contract의 논리 스키마 자체의 버전이다. SemVer 규율을 따른다(§3.3-B). 스키마 개정은 spec 버전 상승 + Revision History를 요구한다(§3.3-E).
- **`instanceVersion`** — **인스턴스 버전**. 특정 프로젝트 Contract 인스턴스의 버전이다. 인스턴스 갱신 거버넌스를 따른다(§3.4). Discovery 내부 변경은 instanceVersion·Provenance에만 반영되고 schemaVersion에 도달하지 못한다(§3.2-D).

#### 3.3-B schemaVersion SemVer 규율

`schemaVersion`은 SemVer 규율을 따른다.

- **MINOR = 후방 호환 추가만.** 선택 필드·부속 네임스페이스의 **추가**만 MINOR 상승으로 허용된다. 기존 필수 코어 필드의 의미·형태는 불변이다. tolerant reader는 추가된 미지 필드를 must-ignore하므로 기존 소비자는 영향받지 않는다(§3.3-C).
- **MAJOR = 파괴 변경 (원칙 금지).** 필수 코어 필드의 제거·의미 변경 등 파괴 변경은 MAJOR에 해당하며 **원칙적으로 금지**된다. 불가피할 경우 **마이그레이션 경로 + 거버넌스 개정 절차**가 필수다 — 이 둘 없이 MAJOR 상승은 허용되지 않는다(§3.6 PC-INV 4).
- **후방 호환 유지.** Discovery 내부 변경이 스키마 파괴로 이어지지 않도록, Discovery 관련 변화는 Provenance 부속·선택 필드로만 흡수된다(§3.2-D).

#### 3.3-C tolerant reader 소비자 규칙

UAHF는 Contract를 **tolerant reader**로 소비한다.

- **필수 코어 필드만 의존.** UAHF는 필수 코어 필드(§3.2-B)에만 의존한다.
- **미지 필드·부속 must-ignore.** 알지 못하는 필드·부속 네임스페이스(Provenance 포함)는 **무시한다(must-ignore)** — 존재를 오류로 취급하지 않는다.
- **결과.** Discovery 내부 변경이 만들어내는 선택 필드·Provenance 부속은 tolerant reader에 도달하지 못한다. 이로써 **Discovery 내부 변경은 코어 스키마 소비에 영향을 주지 못한다**(상시 불변 ②, §3.6 PC-INV 5·11).

#### 3.3-D 필드 제거 금지·deprecation

- **필드 제거 금지.** 확정된 필드는 **제거하지 않는다**. 사용 중단이 필요하면 `deprecated`로 마킹하고 **유지**한다(§3.6 PC-INV 6).
- **deprecated 소비.** deprecated 필드는 tolerant reader가 계속 안전하게 소비·무시할 수 있어야 한다. 제거가 필요해 보이면 그것은 파괴 변경(MAJOR)이며 §3.3-B 원칙 금지·마이그레이션 절차의 대상이다.

#### 3.3-E 스키마 개정 거버넌스

- **스키마 개정 = spec 버전 상승 + 개정 기록.** 본 스키마(코어 필드·버저닝 규칙)의 개정은 **본 문서(spec)의 버전 상승 + git 커밋 기록**(취지·범위를 커밋 메시지에)으로만 이뤄진다. 이는 UAHF spec 개정 관행과 동형이다(uahf/specs/00-glossary.md §3.2-G Spec Status: Frozen; 기록 locus 정본 = `docs/spec-versioning-policy.md` §3 — 파일 내 이력 절은 폐지됨).
  - **주의 — 이 항은 *문서의 개정 기록*이다.** 아래 §3.4 인스턴스 거버넌스의 append-only(인스턴스 파일 버전 체인·`supersedes` 계보·PC-INV 9)와 혼동하지 않는다. 계보는 제품 생성 동작의 부품이므로 **유지**된다(`docs/spec-versioning-policy.md` §3.4 경계 ②).
- **거버넌스 게이트.** 스키마 개정은 Advisor 승인·사용자 승인 게이트를 거친다(ARCHITECTURE.md §8 UAF-INV ⑤ Preserve Human Authority). MAJOR 개정은 여기에 마이그레이션 경로를 더한다(§3.3-B).

### 3.4 인스턴스 거버넌스 (Instance Governance)

특정 프로젝트 Contract **인스턴스**의 갱신 거버넌스다. 스키마 개정(§3.3-E)과 구분된다.

- **append-only 이력.** 인스턴스 갱신은 **append-only**다. 기존 `instanceVersion`의 문면은 **불변**이며, 갱신은 새 인스턴스 버전을 덧붙일 뿐 과거 버전을 고쳐 쓰지 않는다(§3.6 PC-INV 9; UAHF loop-data append-only 관행과 동형 — uahf/specs/03-loop.md §3.2-A).
- **supersedes 계보.** 기존 Contract를 기준선으로 이어가는 새 발견 실행(예: Incremental Discovery — discovery/specs/02-discovery.md §3.3-A Contextualizing의 incremental 분기)은 **새 `instanceVersion` + Meta의 `supersedes` 계보 기록**을 남긴다. 이전 인스턴스는 계보로 보존된다.
- **갱신 유형 — Contract Maturation(성숙) 추가.** supersedes 갱신을 낳는 사유는 위 **새 발견 실행**(예: Incremental Discovery)에 더해 **Contract Maturation(성숙)** 이 있다 — Solution Design(정본 `planning/specs/04-solution-design.md`)이 Ready 종단 인스턴스 vN을 기준선으로 새 설계 결정을 반영한 superseding 인스턴스 v(N+1)을 재발행하는 것이다. 성숙은 **동일한 append-only·supersedes 메커니즘**을 쓰며 **새 갱신 메커니즘을 창설하지 않는다** — 인스턴스 이력 append-only(§3.6 PC-INV 9)를 그대로 따르고 `schemaVersion`·코어 스키마는 무촉이다. 성숙 활동의 상세 계약은 정본 04(§3.1 단계 계약·§3.6 경계 기준) 소관이며, 본 문서는 그 갱신이 §3.4 supersedes 계보로 표현됨만 확정한다.
- **Discovery 내부 변경의 도달 한계.** Discovery 내부 변경(기법·전략·예산·질문 방식)은 `instanceVersion`·Provenance 부속에만 반영되고 **`schemaVersion`·코어 스키마에 도달하지 못한다**(§3.2-D, §3.6 PC-INV 2). 즉 인스턴스가 어떤 발견 과정을 거쳐 갱신되었든, 스키마(Public API)는 그 사실로 인해 변하지 않는다.

### 3.5 UAHF Interface

Contract가 존재할 때 UAHF가 이를 어떻게 소비하는가를 정의한다. **본 절은 UAHF spec의 어떤 연산·필드·불변도 추가·변경하지 않는다**(UAF-INV ①). 두 소비 지점은 기존 UAHF 관행으로 성립하며, 정식 등재는 확장 포인트로만 남긴다.

#### 3.5-A 선택 입력 (하위 호환 — D2④)

- Contract는 UAHF의 **선택 입력**이다. **부재 시 UAHF는 기존 방식으로 운용된다(하위 호환)** — Contract 없이도 UAHF 운용은 불변이다(ARCHITECTURE.md §2.2). Entry는 Contract를 유/무 증거로만 관측하며(entry/specs/01-entry.md §3.2-C contract-presence, EN-INV 2) 그 스키마·내용을 다루지 않는다.

#### 3.5-B 두 소비 지점 (UAHF 정본 무수정으로 성립)

Contract가 존재하면 "프로젝트 정의의 정본 문서"로서 다음 두 지점에서 소비된다. 두 소비 모두 **UAHF 계약 요소를 변경하지 않고 기존 문서 소비 관행으로 성립**한다.

| 소비 지점 | 성립 방식 | UAHF 무수정 근거 |
|---|---|---|
| **(a) Advisor 착수 정독 (Consult 관행)** | UAHF Advisor가 착수 전 상위 규약·Architecture·컨텍스트를 정독하는 **Consult 단계**(uahf/specs/00-glossary.md §3.2-F Agent Lifecycle의 Consult; uahf/specs/02-agent.md §3.2 Advisor의 Consult 참조 주도)에서, 존재하는 Contract를 **또 하나의 프로젝트 정의 정본 문서로 정독**한다. | 문서를 정독하는 것은 UAHF spec의 연산·필드·불변을 바꾸지 않는다. Consult 관행은 이미 "착수 전 문서 정독"을 포함하며, Contract는 그 정독 대상 문서일 뿐이다. |
| **(b) 신규 프로젝트 설치 배치** | UAHF Scaffold가 신규 프로젝트에 규약·정의 문서를 설치하는 관행(uahf/specs/12-scaffold.md §3.2-A Project Template)에서, Contract를 프로젝트에 배치되는 **정본 문서**로 함께 둔다. | 프로젝트에 문서를 배치하는 것은 UAHF Scaffold 계약(연산·필드·불변)을 바꾸지 않는다. Contract는 설치되는 프로젝트 정의 문서일 뿐이다. |

#### 3.5-C 정식 등재는 확장 포인트

- **확장 포인트(설계 안 함).** Contract를 UAHF spec에 **필수 입력·명명 산출물로 정식 등재**하는 경로(예: UAHF Agent spec의 명명된 Consult 입력·Scaffold Install Manifest의 명명 항목으로 등록)는 UAHF 정본을 확장하므로, 본 문서에서 설계하지 **않고** **구현 버전의 확장 포인트로만** 표기한다. 정식 등재를 여기서 설계하면 UAF-INV ①(접점 원칙 — 재정의·확장 없이 § 포인터 참조)을 위반한다.

### 3.6 Invariants (PC-INV)

Project Contract는 어떤 구현·버전에서도 다음을 유지한다. PC-INV 10·11은 ARCHITECTURE.md §7.1 **상시 불변 확인 2건**의 본 문서 반영이다.

- **PC-INV 1 (Stable Contract·논리 스키마 전용).** Contract는 UAF↔UAHF 공식 Stable Contract(Public API)이며 **논리 스키마만** 정의한다. 직렬화·물리 포맷·저장 위치는 Adapter 소관이다(§3.1, §4).
- **PC-INV 2 (역참조 금지).** 스키마 본문(코어 필드 정의 — §3.2-A 그룹 1~8)에 Discovery 내부 개념(질문 선택·전략·예산·Strategy·Capability) 참조가 **0건**이다(**Provenance 부속 제외**). Readiness의 산출 기록(Confidence Vector·Assumption Ledger·미해결 질문 목록)은 종단 판정의 결과이지 Discovery 내부 개념이 아니다(§3.2-A 경계 문면). 이것이 Strategy Invariance(P2·UAF-INV ③)의 **스키마 측 성립 조건**이다.
- **PC-INV 3 (Provenance 불투명).** Provenance는 불투명 부속이며 UAHF는 소비하지 않는다(must-ignore). 내부 구조는 본 스키마가 정의하지 않는다(§3.2-D).
- **PC-INV 4 (SemVer).** `schemaVersion`은 SemVer를 따른다 — MINOR = 후방 호환 추가만, MAJOR = 파괴 변경(원칙 금지 — 마이그레이션 경로 + 거버넌스 개정 필수)(§3.3-B).
- **PC-INV 5 (tolerant reader).** UAHF는 필수 코어 필드만 의존하고 미지 필드·부속 네임스페이스는 must-ignore한다(§3.3-C).
- **PC-INV 6 (필드 제거 금지).** 확정 필드는 제거하지 않는다. deprecated 마킹 후 유지한다(§3.3-D).
- **PC-INV 7 (Completeness 불가침).** 필수 코어 필드는 모든 Ready 종단에서 전건 충족되어야 한다(실측 또는 가정). Compiler는 불완전 Contract를 산출하지 않는다(§3.2-B, discovery/specs/02-discovery.md §3.1·§3.7).
- **PC-INV 8 (UAHF 무수정).** Contract의 UAHF 소비는 UAHF spec의 연산·필드·불변을 변경하지 않는다. 접점은 Contract 하나이며, 정식 등재는 확장 포인트로만 남긴다(§3.5, UAF-INV ①).
- **PC-INV 9 (인스턴스 이력 append-only).** 인스턴스 갱신은 append-only다 — 기존 `instanceVersion` 문면은 불변이며 갱신은 새 버전 + `supersedes` 계보로 기록된다(§3.4).
- **PC-INV 10 (상시 불변 ① — Discovery 교체 가능성 보존).** 역참조 금지(PC-INV 2)와 Provenance 불투명(PC-INV 3)으로 Discovery 내부 개념이 코어 스키마·UAHF 접점으로 새지 않는다. Discovery는 언제든 교체 가능하게 유지된다(ARCHITECTURE.md §7.1 ①·§8 UAF-INV ②③).
- **PC-INV 11 (상시 불변 ② — 장기 호환 훼손 0).** SemVer(PC-INV 4)·tolerant reader(PC-INV 5)·필드 제거 금지(PC-INV 6)로 Public API의 장기 호환성이 훼손되지 않는다(ARCHITECTURE.md §7.1 ②·§8 UAF-INV ①②).
- **PC-INV 12 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·실행 환경·방법론에 의존하지 않는다. 환경 바인딩은 §4에 위치한다.

---

## §4. Adapter Binding (환경 의존)

### 4.1 바인딩 대상

§3 Core Contract(논리 스키마·버저닝·불변)는 AI·환경 비의존이다. 다음 실현은 Adapter Binding 소관이다.

| §3 계약 요소 | 바인딩 지점(일반형) |
|---|---|
| Contract 직렬화·물리 포맷(§3.1·§3.2) | 논리 스키마를 실제 문서·레코드로 표현하는 직렬화 형식. |
| Contract 저장 위치(§3.2) | Contract 인스턴스가 프로젝트에 배치·보관되는 물리 위치·경로 관례. |
| `schemaVersion`·`instanceVersion` 표기 형식(§3.3·§3.4) | 버전 값의 물리 표기·직렬화. |
| Provenance 부속 물리 형식(§3.2-D) | 불투명 부속의 물리 저장 형식 — Discovery 측·Adapter 측 소관(내부 구조 비정의). |

특정 AI·모델·제품 기능·방법론·직렬화 형식·환경 경로는 여기서도 명명하지 않는다. 구체 인스턴스는 해당 Adapter Binding 문서 소관이다(uahf/framework/core/structure.md §5 C-3 동형).

### 4.2 이식 교체 지점 (Portability Swap Points)

- Contract 직렬화 형식 → 대상 환경의 문서·레코드 포맷.
- Contract 저장 위치·경로 관례 → 대상 환경의 배치 메커니즘.
- 버전 표기·Provenance 물리 형식 → 대상 환경의 표기·기록 메커니즘.

유지되는 것: §3.1 지위·논리 스키마, §3.2 필드 그룹 9종·필수 코어 필드·Dimension 매핑, §3.3 버저닝 규율, §3.4 인스턴스 거버넌스, §3.5 UAHF Interface, §3.6 Invariants. 이들은 이식 시 바뀌지 않는다(§3.6 PC-INV 1).

---

## §5. Memory Access

**해당 없음.** Project Contract는 **데이터 계약 스키마**의 정의이며, Memory Service를 회수·기록하는 연산 주체가 아니다. Contract를 산출하는 Discovery조차 Memory 활용은 v1.1에서 **확장 포인트로만** 열려 있고(ARCHITECTURE.md §10 비담당 ④·§11), 본 문서는 그보다 하류의 산출물 스키마이므로 Memory에 접근하지 않는다.

- **확장 포인트(설계 안 함).** 향후 어떤 주체가 Contract 관련 기억을 활용한다면, 접근은 **Memory Service Interface(단일 Port)** 경유만 허용되며 영속성 백엔드에 직접 접근하지 않는다(uahf/specs/00-glossary.md §3.2-C, uahf/ARCHITECTURE.md §5.1). v1.1은 이 경로를 설계하지 않는다.

---

## §6. Failure Modes

| 실패 시나리오 | 대응 | 위반 불변 / Lesson |
|---|---|---|
| Discovery 내부 개념(질문·전략·예산·Strategy·Capability)이 코어 필드 정의에 유입 | 차단·교정. 스키마 본문에 Discovery 내부 개념 0건(Provenance 부속 제외). | PC-INV 2 위반 · Lesson 후보 |
| UAHF가 Provenance·미지 필드에 의존 | 차단. UAHF는 필수 코어 필드만 의존하고 미지 필드·부속은 must-ignore. | PC-INV 5·3 위반 · Lesson 후보 |
| 마이그레이션·거버넌스 없이 MAJOR 파괴 변경 시도 | 거부. MAJOR는 원칙 금지 — 마이그레이션 경로 + 거버넌스 개정 절차 없이는 불가. | PC-INV 4 위반 · Lesson 후보 |
| 확정 필드 제거 시도 | 거부. 제거 금지 — deprecated 마킹 후 유지. 제거 필요 판단은 MAJOR 절차로 회부. | PC-INV 6 위반 · Lesson 후보 |
| 불완전 Contract 산출(필수 코어 필드 미충족) | 차단. Compiler는 불완전 출력을 내지 않는다. Ready 종단 무효(가정 충족+원장 기재로만 ReadyWithAssumptions 성립). | PC-INV 7 위반 · Lesson 후보 |
| 기존 `instanceVersion` 문면 변경(비-append 갱신) | 차단. 인스턴스 이력은 append-only. 갱신은 새 버전 + `supersedes`로만. | PC-INV 9 위반 · Lesson 후보 |
| Contract 소비를 성립시키려 UAHF spec 연산·필드·불변 변경 시도 | 차단. UAHF 무수정 — 두 소비는 기존 관행으로 성립하고 정식 등재는 확장 포인트. | PC-INV 8 위반(UAF-INV ①) · Lesson 후보 |
| Discovery 내부 변경이 `schemaVersion`·코어 스키마에 도달 | 차단·교정. Discovery 내부 변경은 `instanceVersion`·Provenance 부속에만 반영. | PC-INV 2·10 위반 · Lesson 후보 |

---

## §7. Verification

### 완료 기준 (시연 가능 문장)

판정은 아래 항목을 지목 절 문면과 직접 대조해 내린다(여기서 §3을 재서술하지 않는다). 괄호는 원 done 번호다.

1. 지위(Stable Contract·Public API·논리 스키마 전용 · 직렬화·물리 포맷·저장 위치는 §4 격리) — §3.1-A (done 1)
2. 필드 그룹 9종 열거 — §3.2-A (done 2)
3. 필수 코어 필드 열거 ↔ 02-discovery §3.7 축 1 Completeness 판정 대상 정합(§3.7·§0 추상 참조 해소) — §3.2-B (done 3)
4. Dimension 매핑이 컴파일 방향뿐이고 역방향 의존 0 — §3.2-C (done 4)
5. 버저닝(버전 2종 분리·SemVer·tolerant reader must-ignore·필드 제거 금지·스키마 개정 거버넌스) — §3.3 (done 5)
6. 인스턴스 거버넌스(append-only 이력·`supersedes` 계보·Discovery 내부 변경의 도달 한계) — §3.4 (done 6)
7. 역참조 0 — 코어 필드 정의(§3.2-A 그룹 1~8)에 Discovery 내부 개념 0건(Provenance 부속 제외·다중 패턴 스캔) · Readiness 산출 기록은 경계 문면으로 구분 — §3.2-A·PC-INV 2 (done 7)
8. UAHF Interface(선택 입력·두 소비 지점·UAHF 무수정 근거·정식 등재 확장 포인트) — §3.5 (done 8)
9. 상시 불변 2건 반영·위반 서술 0건 — PC-INV 10·11 (done 9)
10. P3·D6-C2 정본 문면 적재 — §1 (done 10)
11. 관행 규격(상태 라인·개정 기록 = git 커밋[규범 `docs/spec-versioning-policy.md` §3]·§ 포인터 재정의 0 · 특정 AI 실명·모델명·제품 기능명·방법론 고유명 0건 스캔) (done 11)

### 검증 방법 (Verifier)

- Verifier가 §3.2-A 코어 필드 정의(그룹 1~8)를 Discovery 내부 개념 다중 패턴(질문·전략·예산·Strategy·Capability)으로 grep하여 0건(Provenance 부속 제외)임을 확인한다.
- Verifier가 §3.2-C 매핑을 discovery/specs/02-discovery.md §3.11 5차원과 직접 대조하고 역방향 의존 서술이 없음을 확인한다.
- Verifier가 §3.2-B 필수 코어 필드를 discovery/specs/02-discovery.md §3.7 Completeness 판정 대상과 대조한다.
- Verifier가 §3.3 버저닝 규칙(SemVer·tolerant reader·필드 제거 금지)과 §3.4 인스턴스 거버넌스를 D6-C2 문면과 대조한다.
- Verifier가 §3.5가 UAHF spec의 연산·필드·불변을 변경·확장하는 서술을 포함하지 않음을 확인한다(UAHF 무수정).
- Verifier가 본문 전체를 특정 AI 실명·모델명·제품 기능명·방법론 고유명 다중 패턴으로 전수 스캔해 0건을 확인한다.
- 판정 순서는 UAHF 검증 게이트 관행과 동형이다 — CP1 Worker 자체 점검 → CP2 Verifier 독립 판정 → CP3 Advisor 승인(uahf/specs/00-glossary.md §3.2-E·§3.2-F). 자체 점검은 최종 승인이 아니다.

---

## §8. Examples

예시는 **논리 스키마 골격**만 보인다. 물리 직렬화·저장 위치는 Adapter 소관이며(§4) 여기서 명명하지 않는다.

### 예 1 — Ready Contract (논리 골격)

- **Meta.** { id: (인스턴스 식별자), schemaVersion: 1.0, instanceVersion: 1, supersedes: 없음 }
- **Intent.** (프로젝트 의도 — 실측 충족)
- **Requirements.** { 기능: (…), 품질: (…) — 실측 충족 }
- **Constraints.** (제약 목록 — 실측 충족)
- **Risks.** (리스크 목록 — 실측 충족)
- **Architecture Direction.** { 결정: (…), 미결: (…) }
- **Assumption Ledger.** 빔(가정 없음).
- **Readiness.** { Completeness: 필수 코어 필드 전건 실측 충족, Confidence Vector: 전 차원 임계 충족, 미해결 질문 목록: 없음, 사용자 승인 기록: 승인됨 }
- **Provenance.** (불투명 부속 — UAHF must-ignore)

필수 코어 필드가 전건 실측 충족되고 사용자 승인이 기록되어 `Ready` 종단에 정합한다(02-discovery §3.7). Provenance는 소비되지 않는다.

### 예 2 — MINOR schemaVersion 상승 (후방 호환)

기존 `schemaVersion: 1.0`에 **선택 필드**를 추가하여 `1.1`로 MINOR 상승한다(§3.3-B).

- 필수 코어 필드는 불변이다.
- 기존 UAHF tolerant reader는 추가된 선택 필드를 **must-ignore**하므로 소비 거동이 변하지 않는다(§3.3-C, PC-INV 5).
- 파괴 변경이 아니므로 MAJOR가 아니다. 스키마 개정으로서 본 spec 버전 상승 + git 커밋 기록을 거친다(§3.3-E).

### 예 3 — 인스턴스 갱신 (append-only + supersedes)

기존 Contract를 기준선으로 이어가는 새 발견 실행(Incremental — 02-discovery §3.3-A)이 인스턴스를 갱신한다.

- 기존 `instanceVersion: 1` 문면은 **불변**이다.
- 새 `instanceVersion: 2`가 생성되고 Meta의 `supersedes`가 인스턴스 1을 가리킨다(§3.4, PC-INV 9).
- `schemaVersion`은 **불변**이다 — 발견 과정의 변화는 `instanceVersion`·Provenance에만 반영되고 코어 스키마에 도달하지 못한다(§3.2-D, PC-INV 2·10).

주: 완전한 시나리오 워크스루(Greenfield /new · Brownfield /continue 최초 도입 · 가상 /import 확장)는 별도 검증 산출물(`uahf/docs/v1.1-scenario-walkthrough.md@cd9247b` — 산출 후 산출물 수명 정책에 따라 아카이브) 소관이다. 본 예시는 스키마·버저닝 최소 예시다.
