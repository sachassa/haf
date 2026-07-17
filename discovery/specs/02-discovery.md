# discovery/specs/02-discovery — Project Discovery Specification

작성일: 2026-07-07
상태: v1.1 Baseline (CP2 첫 판정 Pass 15/0/0 · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: AGENT.md (INV-1)
근거 정본:

- 사용자 승인 v1.1 실행 계획 (Project Discovery & Entry Layer Architecture) — 본 문서 Workflow부가 확정하는 내용(Compiler 프레이밍·State Machine 단일 정본·파생 뷰·Event Model·Termination·Execution Ready 판정)의 정본 정의. 특히 §"설계 골격 > uaf/specs/02-discovery.md"의 [Workflow] 표기 항목과 결정 D2①·C3.
- ARCHITECTURE.md (v1.3) — UAF 상위 구조 정본. 선행 확정 인터페이스. 특히 §12.2 Discovery Request 추상·§7 사용자 고정 원칙 P1~P5·§7.1 상시 불변 확인 2건·§8 UAF-INV 6건·§10 책임 경계표·§11 Non-Goals·§12 용어. UAF 상위 계약은 § 포인터로만 참조하고 재정의하지 않는다.
- uahf/specs/00-glossary.md 0.2 — UAHF 용어 정본. 네임스페이스 분리(§8 UAF 용어와 별개)의 근거. 특히 §3.2-A(Layer)·§3.2-C(Memory Service Interface)·§3.2-E(Agent 역할)·§3.2-F(Agent Lifecycle 7단계). UAHF 용어는 § 포인터로만 참조한다.
- uahf/specs/TEMPLATE.md 0.1 — spec 문서 구조(§0~§9)·품질 기준 관행.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-07 | v1.1 Draft | 최초 작성 — `uaf/specs/` 경계 Project Discovery 정본 신설(**Workflow부**). Compiler 프레이밍(P2·Strategy Invariance, §3.1)·Discovery Principles 5(§3.2)·**State Machine 단일 정본**(비종단 6·종단 5, 상태·전이·종단 전수 열거표, §3.3)·파생 뷰 3(Lifecycle·Process·Workflow, 정본 재정의 금지 규칙, §3.4)·Event Model 15(append-only·Metrics 파생 원칙, §3.5)·Termination 4경로(§3.6)·Execution Ready 2축 판정식 C3(§3.7)·Invariants(상시 불변 2건 반영, §3.8) 확정. **Module부**(§3.9~§3.16 및 §1 Non-Goals의 P4 재기재·§5·§6·§7의 Module 상세)는 후속 W3 Task 완성 대상으로 자리 표시. 입력 Discovery Request는 uaf/ARCHITECTURE.md §8.2 확정 추상만 참조(병렬 작성 중 `uaf/specs/01-entry.md` 미참조 — 07 R2). UAHF·UAF 상위 정본 무수정(§ 포인터만·재정의 0)·특정 AI 실명·모델명·제품 기능명 0(자가 전수 스캔). | Worker (Advisor 위임, v1.1 W2 T3) |
| 2026-07-07 | v1.1 Draft (Module부 완성) | **Module부 완성** — §3.9 Module Structure(7모듈 책임·경계·상호 의존 표)·§3.10 Strategy Provider Interface(Capability 선언·입출력 계약·레퍼런스 Provider 1건·방법론 대응 비정본 부록 § 포인터)·§3.11 Discovery Dimension 5(Intent/Requirement/Constraint/Risk/Architecture — 차원별 Confidence)·§3.12 Confidence([0,1]·근거 등급·Policy 임계)·§3.13 Adaptive Discovery·§3.14 Question Budget(soft/hard·소진 강제 종합·T17 재진입 예산 규칙)·§3.15 Discovery Policy(Policy as Data)·§3.16 Metrics 분류(효율·품질·개입 — 전 지표 §3.5 Event 파생) 확정. §1 Non-Goals P4 비담당 5건 재기재. §3.3-A Contextualizing에 incremental mode 결속 명시(Advisor 승인 보강 2건). §4~§7 Module부 주석을 상세·§ 포인터로 해소. Workflow부(§3.1~§3.8) 문면 보존(§3.3-B 전이표 불변). 방법론 고유명·특정 AI 실명·모델명·제품 기능명 0(자가 전수 스캔)·정본 재정의 0(§ 포인터만). | Worker (Advisor 위임, v1.1 W3 T4) |
| 2026-07-07 | v1.1 Baseline | v1.1 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass — 충족 15/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | v1.1 (정합) | 루트 v1.7 UAF-INV ① 재정의(구 "무수정"[동결] 폐지·접점 원칙[Project Contract 단일 접점] 존치) 인용 정합 — 사용자 승인 하 Frozen 개정. §0 경계 표제 "무수정"→"§ 포인터 참조(재정의·확장 0)"·① 인용에 "접점 원칙" 명기(본문 의미 2 "재정의·확장하지 않고 § 포인터로만 참조"·"유일한 접점은 Project Contract 하나" 서술 존치). DISC-INV 1~9·State Machine·전이표·§9 기존 행 무변. 참조 정합(시맨틱 개정 아님·버전 무상승). | Worker (Advisor 위임) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, ARCHITECTURE.md §9·uahf/framework/core/structure.md §9 동형. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본 배치.** 이 문서는 **UAF specs 경계**의 **Project Discovery 정본**이다. UAF 파이프라인 6요소 중 **Project Discovery** 요소(ARCHITECTURE.md §2.2)의 상세 계약을 소유한다. 특히 Discovery의 **오케스트레이션 구조**(어떻게 상태가 전이하며 산출로 수렴하는가)를 확정한다.

- **Workflow부 / Module부 완성.** 본 문서는 **두 단계에 걸쳐 완성**되었다. **Workflow부**(§3.1~§3.8 — Compiler 프레이밍·State Machine·파생 뷰·Event Model·Termination·Execution Ready·Invariants)는 v1.1 W2 Task가 완성했고, **Module부**(§3.9~§3.16 및 §1 Non-Goals의 P4 재기재·§4~§7의 Module 상세 — Module Structure·Strategy Provider Interface·Discovery Dimension·Confidence·Adaptive Discovery·Question Budget·Discovery Policy·Metrics 분류)는 v1.1 W3 Task가 완성한다. 두 부는 하나의 정본으로 통합되며, 어느 부도 §3.3 State Machine 단일 정본을 재정의하지 않는다(DISC-INV-2).

- **UAF·UAHF 상위 정본 § 포인터 참조 (재정의·확장 0).** 이 문서는 UAF 상위 구조(ARCHITECTURE.md)와 UAHF 정본(ARCHITECTURE.md·uahf/specs/·uahf/framework/·상위 규약)을 **재정의·확장하지 않고 § 포인터로만 참조**한다. Discovery와 UAHF의 유일한 접점은 Project Contract 하나다(ARCHITECTURE.md §8 UAF-INV ① 접점 원칙).

- **선행 인터페이스만 소비.** Discovery의 입력인 **Discovery Request**의 확정 추상은 ARCHITECTURE.md §12.2다(3요소 {mode, inputs, policy}). 본 문서는 이 확정 추상만 소비하며, Entry Resolution의 상세 정본(`entry/specs/01-entry.md`, 예정)은 병렬 작성 중이므로 그 미완성 산출물을 참조·추측하지 않는다(07 R2).

- **AI 비의존.** 본문 전체(특히 §3 Core Contract)에 특정 AI 이름·모델명·제품 기능명을 두지 않는다(uahf/specs/TEMPLATE.md §3, uahf/framework/core/structure.md §5 C-3 동형). 구체 실현(진입 명령의 형태·직렬화 형식·증거 스캔 구현·사용자 확인 채널)은 Adapter Binding 소관이며(§4), 필요한 자리에는 일반형 표기와 소관 포인터만 둔다.

- **네임스페이스 분리.** Discovery 내부 용어(파생 뷰 라벨 "Lifecycle"·"Process"·"Workflow" 등)는 UAHF Glossary(uahf/specs/00-glossary.md)의 동명 용어와 **네임스페이스로 구분**한다(ARCHITECTURE.md §12 동형). UAHF 용어는 정본을 § 포인터로 참조하고 재정의하지 않는다.

- **정본 위임.** Contract 스키마·버저닝·UAHF Interface의 상세 정본은 `planning/specs/03-project-contract.md`(예정, W4)가 소유한다. 본 문서는 "필수 코어 필드"·"완결 기준"을 추상으로 참조하고 그 소유 지점을 포인터로만 표기한다.

---

## §1. 목적 (Purpose)

이 문서는 Project Discovery가 **Discovery Request(+증거)를 입력으로 어떻게 Project Contract로 수렴하는가**의 오케스트레이션 구조를 확정한다.

Workflow부의 책임은 다섯 가지다.

- Discovery를 **Compiler**로 프레이밍하고 3부 구조와 Strategy Invariance를 명문화한다(§3.1).
- Discovery Principles 5를 열거한다(§3.2).
- Discovery의 진행을 **단일 정본 State Machine**으로 정의하고, 상태·전이·종단을 전수 열거한다(§3.3). 파생 뷰 3이 이 정본에서 도출됨을 규정한다(§3.4).
- 모든 전이를 유발하는 **Event Model 15종**을 열거하고, 기록의 append-only 성질과 Metrics의 파생 원칙을 확정한다(§3.5).
- **Termination 4경로**와 **Execution Ready 2축 판정식**을 문면화한다(§3.6, §3.7). 상시 불변 2건을 반영한다(§3.8).

### Non-Goals

- **구현 0.** v1.1은 Architecture·계약 설계만 수행한다. 실행 코드·물리 실현을 정의하지 않는다(Adapter 소관, §4).
- **UAHF 하류 책임 비담당 (P4 재기재).** Project Discovery는 다음 **5건을 담당하지 않는다** — 전부 하류 UAHF의 책임이며(ARCHITECTURE.md §10 책임 경계표 비담당 5), Discovery는 Project Contract를 산출한 지점에서 멈춘다.
  - ① **Agent 실행** — UAHF Agent Layer 소관(uahf/specs/00-glossary.md §3.2-A).
  - ② **Planning** — 구현 계획·작업 분해. UAHF Advisor/Planner 소관(uahf/specs/00-glossary.md §3.2-E).
  - ③ **Workflow 실행** — 분해·병렬 디스패치·병합. UAHF Workflow Layer 소관(uahf/specs/00-glossary.md §3.2-A).
  - ④ **Memory Consult** — 기억 회수. UAHF Memory Service 소관(uahf/specs/00-glossary.md §3.2-C).
  - ⑤ **UAHF Execution** — 핵심 루프 구동. UAHF 하류 소관(uahf/specs/00-glossary.md §3.2-J 핵심 루프).
- **Contract 스키마 상세 비정의.** Project Contract의 필드·스키마·버저닝은 `planning/specs/03-project-contract.md`(예정, W4) 소관이다. 본 문서는 "필수 코어 필드"를 추상으로만 다룬다.
- **Discovery 실행 호스팅·Memory 활용 비설계.** 역할 추상까지만 정의하고 물리 호스팅은 설계하지 않으며, Memory 활용은 확장 포인트로만 표기한다(ARCHITECTURE.md §11, §5).

---

## §2. Position

- **아키텍처 상 위치.** UAF 파이프라인의 **Project Discovery** 요소다(ARCHITECTURE.md §2.2). UAHF 6-Layer 스택의 지층(Layer)이 아니라, 그 **외부·상류의 UAF 레벨 구조**다(ARCHITECTURE.md §2.4, uahf/specs/00-glossary.md INV-3 무촉). Discovery는 Discovery Request를 입력받아 Project Contract를 산출한 지점에서 멈춘다.

- **의존하는 문서 (이 문서를 읽기 전에 이해가 필요한 것).**
  - ARCHITECTURE.md (실재, v1.3) — UAF 구조·의존 방향(§2)·원칙(§6)·P1~P5(§7)·상시 불변(§7.1)·UAF-INV(§8)·책임 경계(§10)·Non-Goals(§11)·용어와 **Discovery Request 추상(§12.2)**. 본 문서의 최상위 근거.
  - uahf/specs/00-glossary.md (실재, Frozen 0.2) — UAHF 용어 정본. 네임스페이스 분리의 대조 기준. 특히 §3.2-A·§3.2-C·§3.2-E·§3.2-F.
  - uahf/specs/TEMPLATE.md (실재, Frozen 0.1) — 문서 구조(§0~§9)·품질 기준.

- **입력 계약(선행 확정).** Discovery의 입력 **Discovery Request** {mode, inputs, policy}의 추상은 ARCHITECTURE.md §12.2가 확정한다. 이 추상만 소비한다. Entry Resolution 상세(`entry/specs/01-entry.md`, 예정)는 병렬 작성 중이며 본 문서는 참조·추측하지 않는다(07 R2).

- **이 문서에 의존하는 문서 (dependents).**
  - `planning/specs/03-project-contract.md` (예정, W4) — Discovery의 산출(Project Contract)의 스키마·완결 기준·UAHF Interface 정본. Discovery의 출력 계약을 소비·고정한다.
  - 본 문서 **Module부**(§3.9~§3.16) — v1.1 W3 Task로 완성되어 본 문서에 통합되었다(별도 하류 문서 아님).

- **순환 의존.** 없다. Discovery는 상위(ARCHITECTURE.md·Glossary)의 확정 계약을 소비하는 방향이며, 하위 요소(UAHF·Execution)를 역참조하지 않는다(ARCHITECTURE.md §2.5 의존 방향).

---

## §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 환경 의존 실현은 §4에 둔다.

§3.1~§3.8은 **Workflow부**(v1.1 W2 Task 완성)다. §3.9~§3.16은 **Module부**(v1.1 W3 Task 완성)다.

---

### 3.1 Compiler 프레이밍 (P2 · Strategy Invariance) — [Workflow부]

**Project Discovery는 단일 기능이 아니라 Project Contract를 생성하는 Compiler다**(ARCHITECTURE.md §7 P2). Discovery Request(+증거)를 입력으로, 단일 타깃 형식인 Project Contract를 산출한다.

Compiler는 **3부 구조**다. 각 부는 §3.3 State Machine의 특정 구간에서 활성화된다.

| 부 | 역할 | 활성 구간(§3.3) | 상세 정본 |
|---|---|---|---|
| **Front-end — Strategy (교체 가능)** | 증거 수집. 어떤 기법으로 프로젝트를 이해하는가. **교체 가능한 증거 수집 계층**이다. | Contextualizing · Eliciting | Strategy Provider Interface 상세 = **§3.10** |
| **Middle — Confidence · Synthesis** | 판정. 수집 증거로 차원별 확신을 측정하고 이해를 종합한다. | Synthesizing (Confidence는 전 구간 누적) | Confidence 상세 = **§3.12** |
| **Back-end — Contract Compiler** | 컴파일. 종합된 이해를 **단일 타깃 형식(Project Contract)**으로 산출한다. | Compiling | 출력 스키마·완결 기준 정본 = `planning/specs/03-project-contract.md` (예정, W4) |

- **Strategy Invariance (P2, ARCHITECTURE.md §8 UAF-INV ③).** Front-end(Strategy)가 바뀌어도 Middle·Back-end의 **출력 스키마와 완결 기준은 불변**이다. 즉 어떤 Strategy를 쓰든 결과는 항상 동일한 Project Contract다. 교체 가능한 생산자(Strategy)를 안정 계약(Contract)이 흡수한다.
- **불완전 출력 금지 (P2 정합).** Compiler는 불완전 출력을 내지 않는다. 필수 코어 필드가 채워지지 않은 Contract는 산출하지 않는다(§3.7 Completeness 불가침, DISC-INV-5).
- **경계.** Strategy가 어떤 방법론을 쓰는지는 Framework가 알지 않는다. 방법론은 교체 가능한 Strategy Provider만이 안다(ARCHITECTURE.md §8 UAF-INV ⑥). Strategy Provider Interface의 상세는 Module부(§3.10) 소관이다.

---

### 3.2 Discovery Principles (5) — [Workflow부]

Discovery는 다음 5원칙을 따른다. 각 원칙은 §3.3~§3.7의 계약으로 구체화된다.

- **P-D1 One Discovery Many Techniques.** Discovery는 하나이되, 그것을 수행하는 기법(Strategy)은 여럿이며 교체 가능하다. 하나의 State Machine·Event Model이 어떤 기법을 쓰든 동일한 산출로 수렴한다(§3.1 Strategy Invariance, §3.8 DISC-INV-7).
- **P-D2 Confidence Driven Discovery.** 진행과 종료는 차원별 **Confidence**가 규율한다. 확신이 임계에 이르면 그 차원의 수집을 멈추고, 전 차원이 임계에 이르면 종합으로 넘어간다(§3.3, §3.7). Confidence 척도·근거 등급의 상세는 §3.12.
- **P-D3 Adaptive Discovery.** 고정 대본이 아니라 적응적으로 진행한다. 남은 예산 대비 확신 이득이 큰 방향을 택하고, 포화한 차원은 건너뛴다. 적응 규칙 상세는 §3.13.
- **P-D4 Minimize Human Intervention.** 일상적 진행은 자동으로 수행하고, 사람 개입은 꼭 필요한 지점(확인·강제)에서만 요구한다. 개입 최소화는 UAHF Loop의 "사람 개입 최소" 관행과 정합한다(uahf/specs/03-loop.md §3.1-D 동형).
- **P-D5 Preserve Human Authority.** 사람의 권한을 보존한다. **확정 게이트는 사용자 승인**이며(ARCHITECTURE.md §8 UAF-INV ⑤), 사용자는 언제든 `UserOverride`로 진행을 강제(일시중단·종료·에스컬레이션)할 수 있다(§3.3, §3.6).

주: P-D4(개입 최소)와 P-D5(권한 보존)는 상충하지 않는다. 반복적·기계적 판단은 자동화하되(P-D4), 최종 확정 게이트와 강제 권한은 항상 사용자에게 남긴다(P-D5).

---

### 3.3 State Machine (단일 정본) — [Workflow부]

Discovery의 진행은 **단일 정본 State Machine**으로 정의된다. 이 절의 상태·전이·종단 전수 열거표가 **정본**이며, 다른 어떤 서술(§3.4 파생 뷰 포함)도 이를 재정의하지 못한다.

**핵심 규칙.** 모든 상태 전이는 §3.5 Event Model의 **Event로만** 일어난다. Event 없는 전이는 없다(DISC-INV-1).

#### 3.3-A 상태 (비종단 6 · 종단 5)

**비종단 상태(6).** 기계는 Discovery Request가 결속될 때 `Initiated`로 **생성**된다(생성은 전이가 아니라 인스턴스화다).

| 상태 | 의미 |
|---|---|
| `Initiated` | Discovery Request가 결속되어 발견을 개시할 준비가 된 상태. |
| `Contextualizing` | 초기 맥락·증거 기준선을 확보하는 상태. mode에 따라 **분기**한다 — Greenfield: 프레이밍(신규 문맥 구성) / Brownfield: 증거 스캔(기존 산출물에서 증거 수집) / Incremental: 기존 Project Contract를 증거 기준선으로 결속하는 스캔(ARCHITECTURE.md §12.2 mode 3종 — greenfield/incremental/brownfield 정합). 세 분기는 모두 `ContextCaptured`로 수렴한다. |
| `Eliciting` | **적응 질문 루프**. 차원별 확신을 끌어올리기 위해 질문·답변·증거·확신 갱신을 반복한다. 질문 선택(적응)·예산 집행 상세는 §3.13·§3.14. |
| `Synthesizing` | 수집 증거를 종합해 이해를 구성하고, 잔여 갭에 가정을 기재하며, 완결성을 평가하는 상태. |
| `Validating` | **사용자 확인** 상태. 종합된 이해·가정·미해결 질문을 사용자에게 제시하고 승인/수정 응답을 받는다(P-D5, UAF-INV ⑤). |
| `Compiling` | Back-end가 Project Contract를 컴파일하고 Readiness를 선언하는 상태. |

**종단 상태(5).**

| 종단 | 의미 | Contract 산출 |
|---|---|---|
| `Ready` | 2축 게이트(§3.7)를 완전 충족하여 실행 준비 완료. | 완전한 Contract |
| `ReadyWithAssumptions` | 필수 코어 필드는 (일부) 가정으로 충족되고 Assumption Ledger에 기재되어 실행 준비 완료. Confidence만 가정으로 대체됨. | 완전한 Contract(+ 가정 원장) |
| `Suspended` | 진행이 중단되어 대기하는 상태. 상태가 보존되어 재개 가능하다. | 없음(미완) |
| `Escalated` | 기계가 자율적으로 Ready에 이를 수 없어 상위(사람) 판단으로 넘긴 상태. | 없음(미완) |
| `Aborted` | 발견이 종료되었고 Contract를 산출하지 않는다. | 없음 |

#### 3.3-B 전이 전수 열거표 (정본)

아래 표가 상태 전이의 **전수 열거**다. `from`에서 `Event`가 발생하고 `Guard`가 참이면 `to`로 전이한다. `to`가 `from`과 같으면 자기 전이(self-transition — 내부 기록 갱신, 상태 불변)다. Event 정의는 §3.5.

| # | From | Event | Guard | To |
|---|---|---|---|---|
| T1 | `Initiated` | `DiscoveryStarted` | — | `Contextualizing` |
| T2 | `Contextualizing` | `EvidenceRecorded` | Brownfield 증거 스캔 진행 | `Contextualizing` (self) |
| T3 | `Contextualizing` | `ContextCaptured` | 맥락 기준선 확보 (Greenfield 프레이밍 완료 ∨ Brownfield 스캔 완료) | `Eliciting` |
| T4 | `Eliciting` | `QuestionAsked` | — | `Eliciting` (self) |
| T5 | `Eliciting` | `AnswerReceived` | 미해결 질문에 대한 응답 | `Eliciting` (self) |
| T6 | `Eliciting` | `EvidenceRecorded` | — | `Eliciting` (self) |
| T7 | `Eliciting` | `ConfidenceUpdated` | — | `Eliciting` (self) |
| T8 | `Eliciting` | `BudgetConsumed` | soft — 잔여 예산 > 0 | `Eliciting` (self) |
| T9 | `Eliciting` | `DimensionSaturated` | 일부(전부는 아닌) 필수 차원 포화 | `Eliciting` (self) |
| T10 | `Eliciting` | `DimensionSaturated` | 전 필수 차원 포화 | `Synthesizing` |
| T11 | `Eliciting` | `BudgetConsumed` | hard — 예산 소진 | `Synthesizing` |
| T12 | `Synthesizing` | `AssumptionRecorded` | 잔여 갭에 가정 기재 | `Synthesizing` (self) |
| T13 | `Synthesizing` | `ConfidenceUpdated` | — | `Synthesizing` (self) |
| T14 | `Synthesizing` | `ValidationRequested` | 필수 코어 필드 충족 가능(실측 ∨ 가정) | `Validating` |
| T15 | `Synthesizing` | `BudgetConsumed` | hard ∧ 필수 코어 필드가 가정으로도 충족 불가 | `Escalated` |
| T16 | `Validating` | `AnswerReceived` | 사용자 승인 | `Compiling` |
| T17 | `Validating` | `AnswerReceived` | 사용자 수정 요청(추가 발견 필요) | `Eliciting` |
| T18 | `Compiling` | `ContractCompiled` | Back-end가 Contract 컴파일 | `Compiling` (self) |
| T19 | `Compiling` | `ExecutionReadyDeclared` | Completeness ∧ 전 차원 Confidence 임계 ∧ 사용자 승인 | `Ready` |
| T20 | `Compiling` | `ExecutionReadyDeclared` | Completeness(필수 필드 가정 충족·원장 기재) ∧ 사용자 승인 ∧ 일부 차원 Confidence 미달 | `ReadyWithAssumptions` |
| T21 | 임의 비종단 | `UserOverride` | 사용자 강제 일시중단 | `Suspended` |
| T22 | 임의 비종단 | `UserOverride` | 사용자 강제 종료 | `Aborted` |
| T23 | 임의 비종단 | `UserOverride` | 사용자 강제 에스컬레이션 | `Escalated` |
| T24 | 임의 비종단 | `DiscoverySuspended` | — | `Suspended` |
| T25 | 임의 비종단 | `DiscoveryAborted` | — | `Aborted` |

주(전수성 확인):

- **Event 커버리지.** 15 Event가 모두 표에 등장한다 — `DiscoveryStarted`(T1)·`ContextCaptured`(T3)·`QuestionAsked`(T4)·`AnswerReceived`(T5·T16·T17)·`EvidenceRecorded`(T2·T6)·`ConfidenceUpdated`(T7·T13)·`BudgetConsumed`(T8·T11·T15)·`DimensionSaturated`(T9·T10)·`AssumptionRecorded`(T12)·`ValidationRequested`(T14)·`UserOverride`(T21~T23)·`ContractCompiled`(T18)·`ExecutionReadyDeclared`(T19·T20)·`DiscoverySuspended`(T24)·`DiscoveryAborted`(T25).
- **종단 도달성.** 5 종단이 모두 도달 가능하다 — `Ready`(T19)·`ReadyWithAssumptions`(T20)·`Suspended`(T21·T24)·`Escalated`(T15·T23)·`Aborted`(T22·T25).
- **비종단 진출성.** 6 비종단 상태는 모두 진출 전이를 가진다 — `Initiated`(T1)·`Contextualizing`(T3)·`Eliciting`(T10·T11)·`Synthesizing`(T14·T15)·`Validating`(T16·T17)·`Compiling`(T19·T20). 여기에 더해 모든 비종단 상태는 `UserOverride`·`DiscoverySuspended`·`DiscoveryAborted`(T21~T25)로 예외 종단에 이를 수 있다.
- **설계 결정 기록(비차단).** 15 Event에는 전용 "escalation" 이벤트가 없으므로, `Escalated`는 (i) 자동 — 예산 소진 시 완결 불가 판정(T15), (ii) 지시 — 사용자 강제(T23)의 두 경로로 도달한다. 또한 `AnswerReceived`는 "미해결 요청(질문 또는 확인 요청)에 대한 사용자 응답"이라는 단일 의미로 정의되어 Eliciting의 답변(T5)과 Validating의 승인/수정 응답(T16·T17)에 함께 쓰인다. 이 이벤트-전이 결속은 본 문서(State·Event 상세 소유)의 설계 결정이며, Advisor 확인 대상으로 완료 보고 open_questions에 기록한다.

---

### 3.4 파생 뷰 3 (Lifecycle · Process · Workflow) — [Workflow부]

§3.3 State Machine은 **단일 정본**이다. 아래 세 뷰는 그 정본에서 **도출되는 뷰(view)**이며, 정본을 **재정의하지 않는다**(정본 재정의 금지 규칙, 결정 D2①).

| 뷰 | 관점 | State Machine에서 도출하는 것 | 네임스페이스 주의 |
|---|---|---|---|
| **Lifecycle 뷰** | 단계(stage) 관점 | 비종단 6상태를 발견의 단계 진행으로 본 뷰(Initiated → Contextualizing → Eliciting → Synthesizing → Validating → Compiling → 종단). | UAHF **Agent Lifecycle**(uahf/specs/00-glossary.md §3.2-F, 7단계 Consult~Complete)과 별개다. Discovery의 Lifecycle 뷰는 State Machine 단계의 나열이며 UAHF Agent Lifecycle이 아니다. |
| **Process 뷰** | 역할·책임 관점 | 각 단계에서 누가 무엇을 하는가 — Front-end(Strategy)가 증거 수집(Contextualizing·Eliciting), Middle(Confidence·Synthesis)이 판정(Synthesizing), Back-end(Contract Compiler)가 컴파일(Compiling), 사용자가 확인(Validating). | "Process"는 본 뷰의 **라벨**이며 UAHF 정본 용어가 아니다(새 용어 신설 아님). |
| **Workflow 뷰** | 오케스트레이션 관점 | 단계가 어떤 Event로 구동·순서화되고, 예산·종료가 어떻게 통제되는가(§3.5·§3.6). | UAHF **Workflow**(Layer — uahf/specs/00-glossary.md §3.2-A / Component — §3.2-D)와 별개다. Discovery의 Workflow 뷰는 발견 내부 오케스트레이션 관점이며 UAHF Workflow 계층·컴포넌트가 아니다. |

**규칙(명문화).** 세 뷰는 편의상 관점을 달리한 **표현**일 뿐이다. 어떤 뷰도 §3.3의 상태·전이·종단을 새로 정의·변경할 수 없다. 뷰와 정본이 어긋나면 정본(§3.3)이 우선한다.

---

### 3.5 Event Model (15) — [Workflow부]

모든 상태 전이는 아래 15 Event로만 일어난다(DISC-INV-1). Event는 발생 순서대로 **append-only**로 기록된다.

| Event | 의미 | 주 발생 구간(§3.3) |
|---|---|---|
| `DiscoveryStarted` | 발견이 개시된다. | Initiated → Contextualizing |
| `ContextCaptured` | 초기 맥락·증거 기준선이 확보된다. | Contextualizing → Eliciting |
| `QuestionAsked` | 질문이 제시된다. | Eliciting |
| `AnswerReceived` | 미해결 요청(질문 또는 확인 요청)에 대한 사용자 응답이 도착한다. | Eliciting · Validating |
| `EvidenceRecorded` | 증거가 기록된다. | Contextualizing · Eliciting |
| `ConfidenceUpdated` | 차원별 확신이 갱신된다. | Eliciting · Synthesizing |
| `BudgetConsumed` | 질문 예산이 소비된다(soft/hard 경계 판정 포함). | Eliciting · (hard 회계) Synthesizing |
| `DimensionSaturated` | 한 차원이 확신 임계에 도달(포화)한다. | Eliciting |
| `AssumptionRecorded` | 잔여 갭에 가정이 기재된다(Assumption Ledger 대상). | Synthesizing |
| `ValidationRequested` | 사용자 확인이 요청된다. | Synthesizing → Validating |
| `UserOverride` | 사용자가 진행을 강제한다(일시중단·종료·에스컬레이션 — P-D5). | 임의 비종단 |
| `ContractCompiled` | Project Contract가 컴파일된다. | Compiling |
| `ExecutionReadyDeclared` | Readiness가 선언된다(§3.7 구성 포함). | Compiling → 종단 |
| `DiscoverySuspended` | 발견이 일시중단된다. | 임의 비종단 → Suspended |
| `DiscoveryAborted` | 발견이 종료(폐기)된다. | 임의 비종단 → Aborted |

**원칙.**

- **Append-only 기록.** Event 기록은 순서 있는 append-only 로그다. 기록된 뒤에 전이가 유효하며, 기록되지 않은 전이는 없다. 이는 UAHF의 loop-data 관행과 동형이다(uahf/specs/03-loop.md §3.2-A 루프 상태 기록 append-only, uahf/specs/08-hooks.md §3.2-A Event가 확정 계약에서 도출되는 관행 동형).
- **Metrics는 이 Event에서만 파생된다.** 발견의 관측 지표(효율·품질·개입 등)는 별도 계측이 아니라 **이 Event 로그에서만** 파생된다(ARCHITECTURE.md §6 원칙 6 Event Driven). Metrics의 분류·산식 상세는 **§3.16** 소관이다.

---

### 3.6 Termination (4경로) — [Workflow부]

Discovery는 반드시 종단에 이른다. 종단에 이르는 경로는 정확히 다음 4가지다. 각 경로는 §3.3 전이표의 특정 전이로 실현된다.

| 경로 | 조건 | 종단 | 전이(§3.3) |
|---|---|---|---|
| **① 2축 게이트 충족** | Completeness ∧ 전 차원 Confidence 임계 ∧ 사용자 승인(§3.7). | `Ready` | T19 |
| **② 예산 소진 + Confidence 미달** | Question Budget 소진, Confidence 임계 미달. 필수 코어 필드가 가정으로 충족되면 `ReadyWithAssumptions`(**Assumption Ledger 필수**), 가정으로도 충족 불가하면 `Escalated`. | `ReadyWithAssumptions` / `Escalated` | T11 → … → T20 / T15 |
| **③ 사용자 강제 종료** | 사용자가 `UserOverride`로 진행을 강제한다(Preserve Human Authority, P-D5). | `Suspended` / `Aborted` / `Escalated` | T21 / T22 / T23 |
| **④ Abort** | 발견이 폐기된다(Contract 미산출). | `Aborted` | T25 (또는 T22) |

- **경로 ②의 Completeness 불가침.** 예산이 소진되어도 Compiler는 불완전 Contract를 내지 않는다. 필수 코어 필드는 실측 또는 **가정**으로 충족되어야 하며, 가정으로 충족한 항목은 Assumption Ledger에 기재된다(§3.7). 어느 쪽으로도 충족 불가하면 Ready 종단이 아니라 `Escalated`다.
- **일시중단·재개.** `Suspended`는 상태가 보존되어 재개 가능하다. 재개 시맨틱의 물리 실현(직렬화·복원)은 Adapter 소관이다(§4).
- **종단 보장.** 어떤 경로로도 검증되지 않은 결과가 Ready로 보고되지 않는다(§3.7, DISC-INV-5·DISC-INV-6). 이는 UAHF Loop의 종료 보장 관행과 정합한다(uahf/specs/03-loop.md §3.1-C 동형).

---

### 3.7 Execution Ready 2축 판정 (C3) — [Workflow부]

Discovery의 종단 판정 **Execution Ready**는 다음 판정식으로 정의된다.

```
Ready = Contract Completeness  ∧  Confidence  ∧  사용자 승인
        (필수 코어 필드 전건 충족)   (전 차원 임계 충족)   (Preserve Human Authority)
```

- **축 1 — Contract Completeness (타협 불가).** 필수 코어 필드가 **전건 충족**되어야 한다. 이 축은 **모든 Ready 종단에서 타협 불가**다. `Ready`는 필수 필드를 실측으로 충족하고, `ReadyWithAssumptions`도 필수 필드를 **가정으로 충족**시키고 Assumption Ledger에 기재해야 성립한다. Compiler는 불완전 출력을 내지 않는다(§3.1, DISC-INV-5). 필수 코어 필드의 정의·목록은 `planning/specs/03-project-contract.md`(예정, W4) 소관이며, 본 문서는 추상으로만 참조한다.
- **축 2 — Confidence (가정 대체 허용).** 전 차원 Confidence가 임계를 충족하면 `Ready`다. 예산 소진 등으로 일부 차원이 임계에 미달하면, **Confidence 축에 한해** 가정으로 대체하여 `ReadyWithAssumptions`로 성립한다(축 1은 여전히 충족 필수). Confidence 차원·척도·임계 상세는 §3.11·§3.12·§3.15.
- **축 3 — 사용자 승인 (게이트).** 사용자 최종 승인 게이트 없이 어떤 Ready 종단에도 도달하지 못한다(ARCHITECTURE.md §8 UAF-INV ⑤, DISC-INV-6). 승인은 `Validating` 상태에서 받고(T16), 그 결과는 Readiness 선언에 기록된다.

**Readiness 선언의 구성.** `ExecutionReadyDeclared`(§3.5)가 선언하는 Readiness는 다음으로 구성된다.

- Completeness 판정(필수 코어 필드 충족 여부·충족 방식[실측/가정]),
- Confidence Vector(차원별 확신 — 상세 형식은 §3.11·§3.12),
- Assumption Ledger(가정 원장 — 가정으로 충족한 항목의 기록),
- 미해결 질문 목록,
- 사용자 승인 기록.

**Ready vs ReadyWithAssumptions.**

| | Completeness(축 1) | Confidence(축 2) | 사용자 승인(축 3) | Assumption Ledger |
|---|---|---|---|---|
| `Ready` | 필수 필드 실측 충족 | 전 차원 임계 충족 | 필수 | 비었거나 무관 |
| `ReadyWithAssumptions` | 필수 필드 가정 충족(원장 기재) | 일부 차원 미달(가정 대체) | 필수 | **필수(비어 있을 수 없음)** |

---

### 3.8 Invariants — [Workflow부]

Discovery는 어떤 구현·Strategy에서도 다음을 유지한다. DISC-INV-7·DISC-INV-8은 ARCHITECTURE.md §7.1 **상시 불변 확인 2건**의 본 문서 반영이다.

- **DISC-INV-1 (Event 전이).** 모든 상태 전이는 §3.5 Event로만 일어난다. Event 없는 전이는 없다.
- **DISC-INV-2 (단일 정본).** §3.3 State Machine이 단일 정본이다. §3.4 파생 뷰는 이를 재정의하지 않는다.
- **DISC-INV-3 (Append-only 로그).** Event 기록은 순서 있는 append-only 로그다. 기록되지 않은 전이는 없다(uahf/specs/03-loop.md §3.2-A 관행 동형).
- **DISC-INV-4 (Metrics 파생).** 모든 Metrics는 §3.5 Event에서만 파생된다(ARCHITECTURE.md §6 원칙 6). 별도 계측을 정본으로 두지 않는다.
- **DISC-INV-5 (Completeness 불가침 · 불완전 출력 금지).** Compiler는 불완전 Contract를 산출하지 않는다. 모든 Ready 종단에서 필수 코어 필드 Completeness는 타협 불가다(§3.7, P2 정합).
- **DISC-INV-6 (사용자 승인 게이트).** 사용자 최종 승인 없이 `Ready`·`ReadyWithAssumptions` 종단에 도달하지 않는다(ARCHITECTURE.md §8 UAF-INV ⑤).
- **DISC-INV-7 (Strategy Invariance — 상시 불변 ①).** 어떤 Strategy(Front-end)를 쓰든 State Machine·Event는 **동일한 스키마·동일한 완결 기준의 Project Contract**로 수렴한다. Discovery는 언제든 교체 가능하게 유지된다(ARCHITECTURE.md §7.1 ①·§8 UAF-INV ③).
- **DISC-INV-8 (Stable Contract 정합 — 상시 불변 ②).** Contract 완결 기준은 Project Contract의 Stable Contract 지위와 정합한다. Discovery 내부 개념(질문·전략·예산)이 Contract 코어 스키마나 UAHF 접점으로 **새어나가지 않는다**. 장기 호환성 규칙의 상세 정본은 `planning/specs/03-project-contract.md`(예정, W4)가 소유한다(ARCHITECTURE.md §7.1 ②·§8 UAF-INV ①②).
- **DISC-INV-9 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 환경 바인딩은 §4에 위치한다.

---

### 3.9 Module Structure — [Module부]

Discovery는 §3.1 Compiler 3부를 실현하는 **7개 모듈**로 구성된다. 각 모듈의 책임·경계·상호 의존은 아래 표가 정본이다. 모듈은 §3.3 State Machine을 재정의하지 않으며 그것을 구동·집행하는 단위일 뿐이다(DISC-INV-2).

| 모듈 | Compiler 부(§3.1) | 책임 | 경계 (하지 않는 것) | 상호 의존 |
|---|---|---|---|---|
| **Orchestrator** | 전 구간 구동 | §3.3 State Machine을 구동한다 — Event를 받아 전이를 실행하고 현재 상태를 유지하며, 종단 판정(§3.7)을 집행한다. | 질문을 만들지 않고(Question Engine 소관) 증거를 해석하지 않는다(Confidence Model 소관). 전이 규칙을 새로 만들지 않는다(§3.3 정본). | 모든 모듈을 조정. 전이를 Evidence Store의 Event 로그에 append(§3.5). |
| **Strategy Registry + Strategy Provider Interface** | Front-end | 교체 가능한 Strategy Provider를 Capability 선언으로 등록·선택한다(§3.10). 선택된 Provider가 다음 질문 집합 또는 차원 포화 신호를 낸다. | 특정 방법론을 알지 않는다(UAF-INV ⑥). Confidence를 판정하지 않고 Contract를 컴파일하지 않는다. | Evidence·Confidence Vector·잔여 Budget 소비(§3.10). Question Engine에 질문 집합 공급. |
| **Question Engine** | Front-end 집행 | Strategy가 낸 질문 집합에서 다음 질문을 선택하고 Question Budget(§3.14)을 집행하며 적응 규칙(§3.13)을 적용한다. | 질문 내용을 스스로 창안하지 않는다(Strategy 소관). 예산 값을 하드코딩하지 않는다(Policy 데이터, §3.15). | Strategy Provider·Discovery Policy·Confidence Model 소비. `QuestionAsked`·`BudgetConsumed` Event 방출. |
| **Evidence Store** | 전 구간 | 증거와 Event 로그를 **append-only**로 보관한다(§3.5, DISC-INV-3). | 증거를 수정·삭제하지 않는다(append-only). 증거를 해석하지 않는다(Confidence Model 소관). | 모든 모듈이 기록·조회. UAHF Memory가 아니다(§5 네임스페이스 구분). |
| **Confidence Model** | Middle | 수집 증거로 차원별 Confidence(§3.11·§3.12)를 측정·갱신하고 차원 포화를 판정한다. | 질문을 만들지 않고 Contract를 컴파일하지 않는다. 임계값을 소유하지 않는다(Policy 데이터, §3.15). | Evidence Store 소비. `ConfidenceUpdated`·`DimensionSaturated` Event 방출. Confidence Vector를 Question Engine·Orchestrator에 공급. |
| **Contract Compiler** | Back-end | 종합된 이해를 **단일 타깃 형식(Project Contract)**으로 컴파일한다(§3.1 Back-end). | Strategy·질문·예산 등 Discovery 내부 개념을 Contract 코어 스키마로 내보내지 않는다(DISC-INV-8). 출력 스키마를 정의하지 않는다(`planning/specs/03-project-contract.md` 예정, W4 소유). | Evidence Store·Confidence Model·Assumption Ledger 소비. `ContractCompiled`·`ExecutionReadyDeclared` Event 방출. |
| **Discovery Policy** | 전 구간(데이터) | 임계값·예산·종료 규칙·충돌 게이트 정책을 **데이터로 외부화**한다(§3.15, Policy as Data). | 실행 로직을 담지 않는다(데이터일 뿐). 엔진 코드에 정책을 하드코딩하지 않는다. | Confidence Model(임계값)·Question Engine(예산)·Orchestrator(종료 규칙)가 참조. |

- **Strategy Invariance 보존(DISC-INV-7).** 교체되는 것은 Strategy Registry에 등록된 Provider뿐이다. Orchestrator·Confidence Model·Contract Compiler·Discovery Policy의 계약과 출력(Project Contract 스키마·완결 기준)은 어떤 Provider에서도 불변이다(§3.1, ARCHITECTURE.md §8 UAF-INV ③).
- **누출 차단(DISC-INV-8).** Strategy·Capability·질문·예산은 Front-end·집행 모듈(Strategy Registry·Question Engine) 내부에 갇힌다. Contract Compiler는 이 내부 개념을 Contract 코어 스키마나 UAHF 접점으로 내보내지 않는다(ARCHITECTURE.md §7.1 ②).
- **모듈 경계 = AI 비의존.** 이 표는 논리 모듈 경계이며, 각 모듈의 물리 실행 호스팅은 Adapter 소관이다(§4). Discovery 실행 호스팅은 역할 추상까지만 정의하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE.md §11).

---

### 3.10 Strategy Provider Interface — [Module부]

Strategy는 **교체 가능한 증거 수집 Front-end**이고(§3.1), Strategy Provider는 그 구현 제공자다. Framework는 특정 방법론을 알지 않으며, 방법론은 이 Provider만이 안다(ARCHITECTURE.md §8 UAF-INV ⑥).

#### 3.10-A Capability 선언 (Capability First)

Strategy Provider는 고정 열거가 아니라 **Capability 선언**으로 선택된다(ARCHITECTURE.md §6 원칙 7 Capability First). 하나의 Provider는 다음을 선언한다.

| 선언 항목 | 정의 |
|---|---|
| **providerId** | Provider의 논리 식별자. |
| **capability** | 이 Provider가 **어느 Discovery Dimension(§3.11)에 대해 증거를 끌어올릴 수 있는가**의 선언. Strategy Registry는 이 선언으로 Provider를 선택한다. |
| **inputContract** | 입력 계약 — {Evidence(Evidence Store 조회), Confidence Vector(§3.12), 잔여 Budget(§3.14)}. |
| **outputContract** | 출력 계약 — {다음 질문 집합} 또는 {차원 포화 신호} 중 택일. |

#### 3.10-B 입출력 계약

- **입력.** (i) Evidence — Evidence Store의 현재 증거, (ii) Confidence Vector — 차원별 현재 Confidence(§3.12), (iii) 잔여 Budget — 총량·차원별 잔여 예산(§3.14).
- **출력(택일).** (i) **다음 질문 집합** — 확신 이득이 기대되는 질문들, 또는 (ii) **차원 포화 신호** — 해당 차원에서 더 물을 것이 없다는 신호(`DimensionSaturated`의 근거, §3.5).
- **불변.** Provider가 무엇을 내든 State Machine·Event·Contract 완결 기준은 불변이다(DISC-INV-7). Provider 교체는 질문 방식만 바꾸며 산출 Contract를 바꾸지 않는다.

#### 3.10-C 레퍼런스 Provider (예시 1건)

정본이 싣는 레퍼런스 Provider는 **정확히 1건**이며, 방법론 고유명 없이 일반형으로 서술한다.

- **기본 적응 질문 Provider (Default Adaptive Question Provider).** capability로 5개 Discovery Dimension(§3.11) 전부를 선언한다. 입력의 Confidence Vector에서 **가장 확신이 낮은 미포화 차원**을 골라 그 차원의 확신을 끌어올릴 질문 집합을 출력하고, 모든 차원이 포화하거나 잔여 Budget이 소진되면 차원 포화 신호를 낸다. 이 Provider는 특정 발견·설계 방법론에 매이지 않은 **일반형 기본값**이다.

#### 3.10-D 방법론 대응 (비정본 — 정본 청정)

특정 발견·설계 방법론(외부 고유명을 가진 기법)과 Strategy Provider Capability의 대응표는 **본 정본이 소유하지 않는다**. 방법론 지식이 Framework 정본으로 새면 UAF-INV ⑥ 위반이다. 방법론 대응은 **비정본 부록**(`planning/docs/appendix/methodology-mapping.md`, 예정 — 후속 W5)이 소유하며, 본 절은 그 소유 지점을 § 포인터로만 표기한다. 따라서 본 정본에 방법론 고유명은 0건이다.

---

### 3.11 Discovery Dimension (5) — [Module부]

Discovery가 확신(Confidence)을 측정하는 축이 **Discovery Dimension**이다(ARCHITECTURE.md §12.1 — 상위 정의). v1.1 정본 차원은 **5개**이며, 각 차원은 **자신의 Confidence를 독립적으로 보유**한다(차원별 Confidence, §3.12).

| # | 차원 | 정의 |
|---|---|---|
| 1 | **Intent** | 프로젝트가 이루려는 목적·해결하려는 문제. "무엇을 왜 하는가." |
| 2 | **Requirement** | 프로젝트가 충족해야 할 기능·품질 요구. "무엇을 만족해야 하는가." |
| 3 | **Constraint** | 기술·자원·정책·시간상의 제약. "무엇에 매여 있는가." |
| 4 | **Risk** | 불확실성·위협·실패 가능 지점. "무엇이 어긋날 수 있는가." |
| 5 | **Architecture** | 아키텍처 방향과 주요 설계 결정·미결 사항. "어떻게 구성할 것인가." |

- **책임 경계 정합.** 이 5차원은 ARCHITECTURE.md §10 책임 경계표 담당 ①("프로젝트 이해 — 의도·요구·제약·리스크·방향")의 5축을 실현한다.
- **차원별 Confidence 보유.** 각 차원은 [0,1] Confidence 스칼라를 독립 보유하며(§3.12), 차원별 포화·임계 판정(`DimensionSaturated`, §3.5)은 차원 단위로 일어난다.
- **Contract 매핑은 W4 소유.** 각 차원의 이해가 Project Contract의 어느 필드로 컴파일되는가는 Back-end(§3.1)의 일이며, 그 스키마 정본은 `planning/specs/03-project-contract.md`(예정, W4)가 소유한다. 본 절은 Discovery 내부의 확신 측정 축만 정의하고 Contract 스키마를 정의하지 않는다(DISC-INV-8).

---

### 3.12 Confidence 상세 — [Module부]

각 Discovery Dimension(§3.11)의 확신도가 **Confidence**다(ARCHITECTURE.md §12.1 — 상위 정의). Confidence Model(§3.9)이 이를 측정·갱신한다.

- **척도.** 차원별 **[0,1] 스칼라**다. 전 차원의 Confidence를 모은 것이 **Confidence Vector**(§3.7)다.
- **근거 등급.** 각 Confidence는 근거의 강도로 등급화된다 — **사용자 진술 > 추론 > 가정** 순이다. 사용자 진술 기반 확신이 가장 강하고, 추론 기반이 다음, 가정 기반이 가장 약하다. 예산 소진 시 Confidence 축을 대체하는 가정은 이 등급의 최하위다(§3.7 축 2, §3.14).
- **임계값은 Policy 데이터.** 차원별 포화·Ready를 판정하는 Confidence 임계값은 엔진에 하드코딩되지 않고 **Discovery Policy 데이터**다(§3.15, Policy as Data). 임계값 변경은 엔진 변경을 요구하지 않는다.
- **갱신 경로.** Confidence는 `ConfidenceUpdated` Event로만 갱신되고(§3.5) 임계 도달은 `DimensionSaturated`로 표시된다. 별도 계측을 정본으로 두지 않는다(DISC-INV-4).

---

### 3.13 Adaptive Discovery — [Module부]

Discovery는 고정 대본이 아니라 **적응적으로** 진행한다(P-D3, §3.2). 적응 규칙은 다음과 같다.

- **기대 확신 이득 최대화.** 단위 Budget당 **기대 Confidence 이득이 가장 큰 방향**을 택한다. Question Engine(§3.9)은 Strategy가 낸 질문 집합 중 확신 이득이 큰 질문을 우선 선택한다.
- **포화 차원 스킵.** 이미 임계에 도달(포화)한 차원(`DimensionSaturated`, §3.5)은 더 묻지 않고 건너뛴다. 잔여 Budget을 미포화 차원에 집중한다.
- **규모·리스크별 깊이 조정.** 프로젝트 규모·리스크 수준에 따라 발견 깊이(차원별 목표 임계·예산 배분)를 조정한다. 이 조정 파라미터는 엔진이 아니라 **Discovery Policy 데이터**다(§3.15, Policy as Data).
- **적응의 무규정 불변.** 적응은 질문 선택 순서·깊이만 바꾼다. 어떤 적응도 §3.3 State Machine·§3.5 Event·Contract 완결 기준을 바꾸지 않는다(DISC-INV-2·7).

---

### 3.14 Question Budget — [Module부]

**Question Budget**은 질문의 총량·차원별 상한이다(ARCHITECTURE.md §12.1 — 상위 정의). Question Engine(§3.9)이 이를 집행한다.

- **구성.** 예산은 **총량 예산**과 **차원별 예산**으로 구성된다. 소비는 `BudgetConsumed` Event로 회계된다(§3.5).
- **soft / hard 경계(Policy as Data).** 예산에는 두 경계가 있다 — **soft 경계**(초과 시 적응 압박, 잔여 예산 > 0이면 Eliciting 계속: T8) 와 **hard 경계**(소진 시 강제 종합으로 전이: T11). 두 경계 값은 엔진이 아니라 Discovery Policy 데이터다(§3.15).
- **소진 시 강제 Synthesize + 가정 명시.** hard 경계 소진 시 Orchestrator는 `Eliciting`에서 `Synthesizing`으로 강제 전이하고(T11) 잔여 갭은 가정으로 기재된다(`AssumptionRecorded`, T12). 필수 코어 필드가 가정으로도 충족 불가하면 `Escalated`다(T15). 이 경로는 §3.6 종단 경로 ②와 정합한다.

#### 3.14-A 수정 요청 재진입 예산 규칙 (T17 정합)

§3.3-B 전이 T17(`Validating` → `Eliciting`, 사용자 수정 요청 — 추가 발견 필요)은 예산이 이미 소진된 상태에서도 발생할 수 있다. 이 재진입의 예산 처리를 다음으로 확정한다. **본 절은 예산 집행 규칙만 추가하며 §3.3 전이표 문면은 불변이다.**

- **재할당 또는 보충(Policy 데이터).** 사용자 수정 요청으로 `Eliciting`에 재진입할 때, Question Engine은 (i) 잔여 예산을 수정 대상 차원으로 **재할당**하거나, (ii) Discovery Policy가 정한 **보충 예산(supplementary budget)**을 부여받는다. 재할당·보충의 양과 조건은 **Discovery Policy 데이터**이며(§3.15, Policy as Data) 엔진에 하드코딩되지 않는다.
- **근거.** 사용자 수정 요청은 사용자 권한 행사(P-D5)이므로 예산 소진이 사용자 지시 발견을 봉쇄해서는 안 된다. 보충 예산은 무한정이 아니라 Policy가 정한 상한 아래에서 부여되며, 재진입 후에도 hard 경계 소진 규칙(T11·T15)은 그대로 적용된다.
- **불변 보존.** 이 규칙은 예산 **집행 정책**만 정의한다. §3.3-B 전이(T11·T15·T17)의 from·Event·Guard·to 문면은 변경되지 않는다(DISC-INV-1·2).

---

### 3.15 Discovery Policy — [Module부]

**Discovery Policy**는 Discovery의 판정·집행 파라미터를 **데이터로 외부화**한 계약이다(ARCHITECTURE.md §6 원칙 8 Policy as Data). Discovery Request의 `policy` 요소(ARCHITECTURE.md §12.2)가 이 정책을 참조한다.

| 정책 항목 | 외부화 대상 | 소비 모듈(§3.9) |
|---|---|---|
| **임계값 정책** | 차원별 Confidence 포화·Ready 임계값(§3.12). | Confidence Model |
| **예산 정책** | 총량·차원별 예산, soft/hard 경계, 재진입 재할당·보충 예산(§3.14). | Question Engine |
| **종료 규칙 정책** | Termination 경로별 조건(§3.6)·깊이 조정 파라미터(§3.13). | Orchestrator |
| **충돌 게이트 정책** | 충돌·모호 입력의 사용자 확인 게이트 표기(Preserve Human Authority, P-D5). | Orchestrator |

- **Policy as Data 불변.** 정책 값 변경은 **엔진(모듈 코드) 변경을 요구하지 않는다**. 임계값·예산·종료 규칙·게이트 정책을 데이터로 바꾸는 것만으로 Discovery 거동이 조정된다.
- **정책 값 상세의 소재.** 구체 정책 값(수치·경계)은 물리 실현이며 그 데이터 소스·직렬화는 Adapter 소관이다(§4). Discovery Request가 참조로 담는다(ARCHITECTURE.md §12.2).

---

### 3.16 Metrics 분류 — [Module부]

Discovery의 관측 지표(Metrics)는 별도 계측이 아니라 **§3.5 Event 로그에서만 파생된다**(DISC-INV-4, ARCHITECTURE.md §6 원칙 6 Event Driven). v1.1 정본은 **최소 3분류**를 확정하고 각 지표가 어느 Event에서 파생되는지를 매핑으로 보인다. 지표의 상세 산식·스키마는 **구현 버전으로 이연**한다(계획 D2②).

| 분류 | 지표(예) | 파생 Event(§3.5) |
|---|---|---|
| **효율 (Efficiency)** | 질문 수 | `QuestionAsked` 개수 |
| | Budget 소비 | `BudgetConsumed` 누적 |
| | 소요 | Event 로그 구간(`DiscoveryStarted` → `ExecutionReadyDeclared`) |
| **품질 (Quality)** | 최종 Confidence | 최종 `ConfidenceUpdated`의 Confidence Vector |
| | 가정 수 | `AssumptionRecorded` 개수 |
| | Contract 개정 빈도 | `ContractCompiled` 재발생 횟수 |
| **개입 (Intervention)** | 개입 횟수 | `ValidationRequested`·`AnswerReceived`(Validating 구간) 개수 |
| | Override 횟수 | `UserOverride` 개수 |

- **전 지표 Event 파생.** 위 표의 모든 지표는 §3.5 Event 로그만으로 산출된다 — 별도 계측 채널을 정본으로 두지 않는다(DISC-INV-4).
- **상세 이연.** 정규화·가중·집계 산식과 지표 스키마는 v1.1이 확정하지 않고 구현 버전으로 이연한다(계획 D2②). 본 절은 분류와 Event 매핑까지가 정본이다.

---

## §4. Adapter Binding (환경 의존)

### 4.1 바인딩 지점

§3 Core Contract(State Machine·Event Model·Termination·판정식)는 AI·환경 비의존이다. 다음 실현은 Adapter Binding 소관이다.

| §3 계약 요소 | 바인딩 지점(일반형) |
|---|---|
| Event 로그 직렬화(§3.5) | append-only Event 기록의 저장 형식·위치. |
| 사용자 확인·`UserOverride` 채널(§3.3 Validating, §3.6) | 사용자 승인/수정/강제 응답을 받는 개입 채널. |
| Contextualizing 증거 스캔·프레이밍(§3.3) | Greenfield 프레이밍·Brownfield 증거 스캔의 물리 구현·증거 소스 접근. |
| Strategy 실행 호스팅(§3.1 Front-end) | Discovery 실행을 어느 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE.md §11). |

특정 AI·모델·제품 기능·직렬화 형식·환경 경로는 여기서도 명명하지 않는다. 구체 인스턴스는 해당 Adapter Binding 문서 소관이다(uahf/framework/core/structure.md §5 C-3 동형).

### 4.2 이식 교체 지점 (Portability Swap Points)

- Event 로그 직렬화 포맷·저장 위치 → 대상 환경의 로깅 메커니즘.
- 사용자 확인·Override 채널 → 대상 환경의 사람 개입 메커니즘.
- 증거 소스 접근·스캔 구현 → 대상 환경의 증거 수집 메커니즘.
- Strategy 실행 환경 → 대상 환경의 실행 주체.

유지되는 것: §3.3 State Machine, §3.5 Event Model, §3.6 Termination, §3.7 판정식, §3.8 Invariants. 이들은 이식 시 바뀌지 않는다.

**Module부 바인딩(§3.9~§3.16).** Strategy Provider 실행 호스팅은 **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(§3.10, ARCHITECTURE.md §11). Question Engine의 예산·Discovery Policy의 정책 값(임계값·예산·경계 수치)의 **데이터 소스·직렬화**는 Adapter 소관이다(§3.14·§3.15). Evidence Store의 물리 저장은 위 Event 로그 직렬화 바인딩과 동일하다(§3.9). 이들 물리 실현이 교체되어도 §3.9 모듈 경계·§3.10 Provider 계약·§3.15 Policy as Data 계약은 유지된다.

---

## §5. Memory Access

Discovery는 v1.1에서 UAHF Memory를 회수·활용하지 **않는다**. Memory Consult는 Discovery의 **비담당**이며(ARCHITECTURE.md §10 비담당 ④), Discovery의 Memory 활용은 **확장 포인트로만** 열어두고 설계하지 않는다(ARCHITECTURE.md §11).

- **확장 포인트(설계 안 함).** 향후 Discovery가 Memory를 활용한다면, 접근은 **Memory Service Interface(단일 Port)** 경유만 허용되며 영속성 백엔드에 직접 접근하지 않는다(uahf/specs/00-glossary.md §3.2-C, uahf/ARCHITECTURE.md §5.1). v1.1은 이 경로를 설계하지 않는다.
- **네임스페이스 구분.** §3.5 Discovery Event 로그(append-only)는 Discovery **내부 기록**이며 UAHF Memory가 아니다. 둘을 혼동하지 않는다.

**Module부 정합.** §3.9 Evidence Store는 Discovery 내부 append-only 기록이며 UAHF Memory가 아니다(위 네임스페이스 구분). 어떤 Module부 모듈도 v1.1에서 UAHF Memory를 회수·기록하지 않는다 — Memory Consult는 여전히 비담당이다(ARCHITECTURE.md §10 비담당 ④, §1 Non-Goals P4 ④). Discovery의 Memory 활용은 확장 포인트로만 열려 있다(ARCHITECTURE.md §11).

---

## §6. Failure Modes

Workflow부 범위의 대표 실패 시나리오와 대응이다.

| 실패 시나리오 | 대응 | 종단/불변 |
|---|---|---|
| 예산 소진 + Confidence 미달, 필수 코어 필드 가정 충족 가능 | 가정 기재 후 `ReadyWithAssumptions`. Assumption Ledger 필수. | 종단 경로 ②(§3.6) |
| 예산 소진, 필수 코어 필드 가정으로도 충족 불가 | `Escalated`(사람 판단). Compiler는 불완전 출력을 내지 않는다. | T15, DISC-INV-5 |
| 사용자 강제 종료 | `UserOverride`로 `Suspended`/`Aborted`/`Escalated`. | 종단 경로 ③, P-D5 |
| 조기 Ready 선언(사용자 승인 없이) | 무효·차단. 사용자 승인 게이트 없이는 Ready 불가. | DISC-INV-6 위반 |
| 불완전 Contract 산출 시도 | 무효·차단. Completeness 타협 불가. | DISC-INV-5 위반 |
| Event 없는 전이 | 무효. 모든 전이는 Event로만. | DISC-INV-1 위반 |
| Discovery 내부 개념(질문·전략·예산)이 Contract 코어/UAHF 접점에 누출 | 차단·교정. Stable Contract 정합 위반. | DISC-INV-8 위반 |

**Module부 실패 시나리오.**

| 실패 시나리오 | 대응 | 종단/불변 |
|---|---|---|
| Strategy Provider 실행 실패·미응답 | Registry에서 대체 Provider 선택, 불가 시 Escalate. 교체 가능성은 유지된다. | DISC-INV-7 |
| Confidence 오보정(과대/과소 확신) | 근거 등급(사용자 진술 > 추론 > 가정)으로 보정, 임계는 Policy 데이터로 조정(엔진 무변경). | §3.12·§3.15 |
| Budget 정책 오류(경계 미설정·모순) | Policy 데이터 무결성 위반으로 거부·정정. 엔진에 정책을 하드코딩하지 않으므로 데이터 정정으로 해소. | §3.15 Policy as Data |
| 방법론 고유명이 정본에 유입 | 차단·교정. 방법론은 Strategy Provider만 알고 정본은 청정하다(비정본 부록 소관, §3.10-D). | UAF-INV ⑥ 위반 |
| Discovery 내부 개념(질문·전략·예산)이 Contract 코어/UAHF 접점에 누출 | 차단·교정. Contract Compiler는 내부 개념을 코어 스키마로 내보내지 않는다. | DISC-INV-8 위반 |

---

## §7. Verification

### 완료 기준 (시연 가능 문장) — Workflow부

- **전이 전수성 시연.** §3.3-B 표의 모든 전이가 Event를 가지고(Event 없는 전이 0), 비종단 6·종단 5가 모두 도달·진출 가능함을 표로 보인다.
- **Event 커버리지 시연.** 15 Event가 모두 전이표에 등장함을 대조로 보인다.
- **Termination 정합 시연.** 4 Termination 경로가 전이표·판정식과 정합함을 보인다.
- **사용자 승인 게이트 시연.** `Ready`·`ReadyWithAssumptions` 종단이 사용자 승인 없이 도달 불가함을 보인다(DISC-INV-6).
- **Completeness 불가침 시연.** 모든 Ready 종단에서 필수 코어 필드 Completeness가 충족됨을(ReadyWithAssumptions는 가정 충족+원장 기재) 보인다(DISC-INV-5).
- **파생 뷰 무재정의 시연.** 파생 뷰 3이 §3.3 정본을 재정의하지 않고 참조·도출만 함을 보인다.
- **상시 불변 시연.** 상시 불변 2건 위반 서술 0건 — Discovery 내부 개념의 Contract 코어/UAHF 접점 누출 0(DISC-INV-7·DISC-INV-8).
- **AI 비의존 시연.** §3 본문에 특정 AI 모델명·제품 기능명이 0건임을 다중 패턴 전수 스캔으로 보인다(DISC-INV-9).

### 검증 방법

- Verifier가 §3.3-B 전이표를 파싱해 Event 부여·종단 도달성·비종단 진출성을 확인한다.
- Verifier가 15 Event·4 Termination·판정식을 §3.5·§3.6·§3.7과 대조한다.
- Verifier가 Discovery 내부 개념의 누출과 AI 의존 토큰을 전수 스캔한다.
- 판정 순서는 UAHF 검증 게이트 관행과 동형이다 — CP1 Worker 자체 점검 → CP2 Verifier 독립 판정 → CP3 Advisor 승인(uahf/specs/03-loop.md §3.1-A 게이트-단계 매핑, uahf/specs/00-glossary.md §3.2-E). 자체 점검은 최종 승인이 아니다.

**Module부 완료 기준 (시연 가능 문장).**

- **모듈 경계 시연.** §3.9 표가 7개 모듈의 책임·경계·상호 의존을 열거하고, Strategy 교체가 Strategy Registry의 Provider에 국한됨을 보인다(DISC-INV-7).
- **Provider 계약 시연.** §3.10이 Capability 선언·입출력 계약을 정의하고, 레퍼런스 Provider가 정확히 1건이며 방법론 고유명이 0건임을 스캔으로 보인다(UAF-INV ⑥).
- **차원·확신 시연.** §3.11이 5차원을, §3.12가 [0,1]·근거 등급·Policy 임계를 정의함을 보인다.
- **예산·정책 시연.** §3.14 soft/hard 경계·소진 강제 종합·T17 재진입 예산 규칙과 §3.15 Policy as Data(정책 변경 ↔ 엔진 무변경)를 대조한다.
- **Metrics Event 파생 시연.** §3.16의 전 지표가 §3.5 Event에서 파생됨을 매핑표로 보인다(DISC-INV-4).
- **누출 0 시연.** Strategy·Capability·질문·예산이 Contract 코어 스키마·UAHF 접점 서술로 새지 않음을 전수 스캔한다(DISC-INV-8).

---

## §8. Examples

**예 1 — Greenfield 발견 → `Ready`**

`DiscoveryStarted`(Initiated→Contextualizing, Greenfield 프레이밍) → `ContextCaptured`(→Eliciting) → 적응 질문 루프[`QuestionAsked`·`AnswerReceived`·`EvidenceRecorded`·`ConfidenceUpdated`·`BudgetConsumed`(soft), 차원별 `DimensionSaturated`] → `DimensionSaturated`[전 필수 차원 포화](→Synthesizing) → `ConfidenceUpdated` → `ValidationRequested`(→Validating) → `AnswerReceived`[사용자 승인](→Compiling) → `ContractCompiled` → `ExecutionReadyDeclared`[Completeness ∧ 전 차원 Confidence ∧ 승인](→`Ready`).

Event 로그가 순서대로 append-only로 남고, 가정 원장은 비어 있다.

**예 2 — 예산 소진 → `ReadyWithAssumptions`**

… 적응 질문 루프 중 `BudgetConsumed`[hard](Eliciting→Synthesizing) → `AssumptionRecorded`(잔여 갭 가정 기재) → `ValidationRequested`(→Validating, 사용자에게 가정·미해결 질문 제시) → `AnswerReceived`[승인](→Compiling) → `ContractCompiled` → `ExecutionReadyDeclared`[Completeness(필수 필드 가정 충족) ∧ 승인 ∧ 일부 Confidence 미달](→`ReadyWithAssumptions`).

Assumption Ledger가 필수로 채워진다(비어 있을 수 없음, §3.7). 필수 코어 필드가 가정으로도 충족 불가였다면 `BudgetConsumed`[hard ∧ 미충족](T15)로 `Escalated`에 이른다.

**예 3 — 사용자 강제 종료 → `Suspended`**

임의 비종단 상태에서 `UserOverride`[강제 일시중단](T21) → `Suspended`. 상태가 보존되어 재개 가능하다(P-D5).

주: 완전한 시나리오 워크스루(Greenfield /new · Brownfield /continue 최초 도입 · 가상 /import 확장)는 별도 검증 산출물(`docs/v1.1-scenario-walkthrough.md`, 예정) 소관이다. 본 예시는 State Machine 최소 예시다.
