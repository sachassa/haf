# ARCHITECTURE — Universal Agentic Framework 상위 구조 정본

작성일: 2026-07-07
상태: v1.1 Baseline (CP2 첫 판정 Pass 15/0/0 · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: AGENT.md (INV-1)
근거 정본:

- 사용자 승인 v1.1 실행 계획 (Project Discovery & Entry Layer Architecture) — 본 문서가 확정하는 내용(구조·의존 방향·원칙·불변·경계·용어)의 정본 정의. 특히 §Context 결정 표(D1~D6)와 §"설계 골격 > ARCHITECTURE.md" 절.
- uahf/ARCHITECTURE.md 0.2 (UAHF 정본) — 무수정 대상. UAF는 UAHF를 늘리지 않고, 접점은 Project Contract 하나뿐이다. UAHF 계약 요소는 § 포인터로만 참조한다.
- uahf/specs/00-glossary.md 0.2 (UAHF 용어 정본) — INV-3(Layer 정확히 6개)·용어 네임스페이스 분리의 근거. UAF 신규 용어의 소유 지점은 본 문서 §8이다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-07 | v1.1 Draft | 최초 작성 — `uaf/` 경계 최초 산출물. UAF 상위 구조 정본 신설: 6요소 구조(Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF → Execution)·slot 2종(Agentic Runtime 향후·Extension System 기존)·의존 방향 단방향(§2.4)·설계 원칙 9종(§3)·사용자 고정 원칙 P1~P5와 상시 불변 확인 2건(§4)·UAF 불변 UAF-INV 6건(§5)·책임 경계표 P4(§6)·Non-Goals(§7)·UAF 용어 절(§8 — Discovery Request 인터페이스 추상 {mode, inputs, policy} 확정). UAHF 정본 무수정(§ 포인터만·재정의 0)·INV-3 무촉(Entry·Discovery는 UAHF 6-Layer 외부의 UAF 레벨 구조)·특정 AI 실명·모델명·제품 기능명 0(자가 전수 스캔). | Worker (Advisor 위임, v1.1 W1 T1) |
| 2026-07-07 | v1.1 Draft (r2) | § 포인터 오기 1건 정정 — §2.1 Execution 불릿의 핵심 루프 인용 `specs/00-glossary.md §3.2-I` → `§3.2-J`(정본 실측: 핵심 루프(Core Loop)는 §3.2 카테고리 J "컴포넌트 계약 용어" J-11 소속, Glossary line 403; §3.2-I는 "Runtime 계약 용어"로 오기였다). + 동종 결함 전수 재대조(BP-01) — 문서 내 전 § 포인터를 대상 정본 직접 실측 대조, 그 외 오기 0. 본문 그 외 문면 무변경·소유 경계 유지(uaf/ARCHITECTURE.md 1개). | Worker (Advisor 재작업 지시, v1.1 W1 T1 r2) |
| 2026-07-07 | v1.1 Baseline | v1.1 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass — 충족 15/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-09 | v1.2.1 | uaf/ARCHITECTURE.md → 루트 ARCHITECTURE.md 이관(경로 참조 정합·물리 Layer 매핑 추가). 논지 무변경. | Worker(Advisor 위임, Phase 2) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, uahf/framework/core/structure.md §9 동형. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본 배치.** 이 문서는 **UAF(Universal Agentic Framework) 상위 구조의 정본**(루트 `ARCHITECTURE.md` — v1.2.1에서 `uaf/ARCHITECTURE.md`로부터 이관)이다. UAHF(Universal Agentic Harness Framework)와는 별개의 네임스페이스이자 별개의 정본 경계다. UAF는 UAHF를 감싸는 **상위 진입 구조**를 정의하고, UAHF는 그 안에서 실행(Execution)을 담당한다.

- **UAHF 정본 무수정.** UAF의 신설은 UAHF 정본을 변경하지 않는다. UAF와 UAHF의 유일한 접점은 **Project Contract 하나**다 (UAF-INV ①, §5). 본 문서는 UAHF 계약 요소(ARCHITECTURE.md·specs/·framework/·상위 규약)를 재정의·확장하지 않고 **§ 포인터로만 참조**한다.

- **INV-3 무촉 (핵심 경계 선언).** Entry Layer·Entry Resolution·Project Discovery·Project Contract는 UAHF의 6-Layer 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter, uahf/specs/00-glossary.md §3.2-A)에 **새 Layer로 추가되지 않는다**. 이들은 UAHF 6-Layer의 **외부**, 그보다 상위의 **UAF 레벨 구조**다. 따라서 Glossary INV-3("Layer는 정확히 6개다")는 무촉이며, 본 문서는 UAHF Layer 수를 늘리는 어떤 서술도 두지 않는다.
  - 용어 주의: "**Entry Layer**"의 "Layer"는 UAHF Layer 스택의 지층(stratum)이 아니라, UAF 파이프라인의 한 **단계(stage)** 를 가리키는 명칭이다. UAHF Glossary §3.2-A의 Layer 정의와는 별개 네임스페이스이며(§8 용어 네임스페이스 분리), UAHF의 수직 스택에 편입되지 않는다.

- **Core 문서 관행.** 본문 전체에 특정 AI 이름·모델명·제품 기능명을 두지 않는다 (uahf/framework/core/structure.md §5 C-3 동형). 구체 실현(진입 명령의 물리 형태·직렬화 형식·환경 경로 관례)은 Adapter Binding 소관이며, 필요한 자리에는 일반형 표기와 소관 포인터만 둔다.

- **정본 위임.** 이 문서는 상위 구조(Layer 단계)만 확정한다. 각 요소의 상세 계약(Entry Resolution 결정 테이블·Discovery State Machine·Contract 스키마)은 후속 `각 Layer specs/` 정본(예정)이 소유하며, 본 문서는 그 소유 지점을 slot·포인터로만 표기한다.

---

## §1. 목적 (Purpose)

이 문서는 UAF가 **Execution 이전에 어떤 순서로 프로젝트를 이해하고 계약으로 고정하는가**의 상위 구조를 확정한다.

책임은 네 가지다.

- UAF 구조 6요소의 **순서와 위상**을 정의한다 (§2).
- 요소 간 **의존 방향**을 단방향으로 명문화한다 (§2.4).
- UAF가 따르는 **설계 원칙 9종**과 **사용자 고정 원칙(P1~P5)**, **불변 규칙(UAF-INV) 6건**, **책임 경계**를 확정한다 (§3~§6).
- UAF 신규 **용어**를 소유·정의하고, 특히 후속 병렬 작업의 선행 확정 인터페이스인 **Discovery Request 추상**을 여기서 고정한다 (§8).

이 문서는 상위 구조의 정본이다. 구현을 정의하지 않는다 — v1.1은 Architecture 설계만 수행한다(구현 0).

---

## §2. UAF 구조와 의존 방향 (Structure & Dependency Direction)

### §2.1 6요소 순서

UAF는 사용자 입력에서 UAHF 실행에 이르는 파이프라인을 다음 **6요소**로 정의한다. 순서는 위(입력)에서 아래(실행)로 흐른다.

```
Entry Layer          — UAF 공식 진입점 (사용자 입력 수용)
      │
      ▼
Entry Resolution     — 진입 판별 → Discovery Request 산출 (Discovery 비수행)
      │  (Discovery Request: {mode, inputs, policy} — §8에서 확정)
      ▼
Project Discovery    — Discovery Request(+증거) → Project Contract 산출 (Compiler)
      │
      ▼
Project Contract     — UAF↔UAHF 공식 Stable Contract (Public API) — 유일 접점
      │  (UAHF의 선택 입력 — 부재 시 기존 UAHF 운용 불변)
      ▼
UAHF                 — 기존 UAHF 6-Layer Framework (본 문서 무수정 대상)
      │
      ▼
Execution            — UAHF 핵심 루프 구동 (위임 → 구현 → 검증 → 승인)
```

- **Entry Layer** — UAF의 공식 진입점. 사용자 입력을 수용하는 추상 연산이다. 물리 실현(진입 명령의 형태)은 Adapter 소관이다 (AI-Agnostic, §3).
- **Entry Resolution** — Entry Layer가 수행하는 유일한 연산. 명시 진입과 Workspace Evidence를 평가해 **Discovery Request**를 산출한다. Discovery를 직접 수행하지 않는다 (P1, UAF-INV ④).
- **Project Discovery** — Discovery Request를 입력으로 **Project Contract를 산출하는 Compiler**다 (P2). 어떤 Discovery Strategy를 쓰든 결과는 항상 동일한 Project Contract다 (Strategy Invariance, UAF-INV ③).
- **Project Contract** — UAF와 UAHF의 **공식 Stable Contract(Public API)**이자 **유일한 접점**이다 (P3, UAF-INV ①). UAHF에는 **선택 입력**으로 주어진다 — 부재 시 UAHF는 기존 방식으로 운용된다(하위 호환).
- **UAHF** — 기존 Universal Agentic Harness Framework 전체(6-Layer + Cross-cutting Memory Service, uahf/ARCHITECTURE.md §5·§5.1). 본 문서의 무수정 대상이며, § 포인터로만 참조한다.
- **Execution** — UAHF가 Project Contract(있으면)를 참조하여 핵심 루프(Core Loop: 위임 → 구현 → 검증 → 승인, uahf/specs/00-glossary.md §3.2-J 핵심 루프)를 구동하는 실행 단계다.

**Project Contract의 이중 지위 주의.** Project Contract는 (i) 파이프라인의 한 요소(Discovery의 산출)이면서 동시에 (ii) UAF↔UAHF의 계약 접점이다. 데이터 계약인 **Discovery Request**는 Entry Resolution의 출력이자 Project Discovery의 입력인 요소 간 인터페이스이며, 그 추상은 §8에서 확정된다.

### §2.2 slot (설계 제외 — 자리 표기만)

다음 두 요소는 UAF 구조상 **자리(slot)만 표기**하고 v1.1에서 설계하지 않는다.

- **Agentic Runtime (향후)** — UAF 레벨의 향후 에이전트 실행 기반을 위한 자리. v1.1 미설계. (주의: UAHF의 Runtime Layer, uahf/specs/00-glossary.md §3.2-A와는 별개 네임스페이스다 — §8.)
- **Extension System (기존)** — UAHF의 기존 확장 서브시스템(Hooks / Skills / Plugins, uahf/specs/00-glossary.md §3.2-D)을 가리키는 자리. UAF는 이를 재설계하지 않으며, § 포인터로만 참조한다. 설계 제외 (Non-Goals, §7).

### §2.3 UAF 레벨 위상 (INV-3 무촉 재확인)

§2.1의 6요소 중 Entry Layer·Entry Resolution·Project Discovery·Project Contract는 **UAHF 6-Layer 스택의 외부**에 위치한다. 이들은 UAHF Layer를 늘리지 않고, UAHF의 수직 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter)에 편입되지도 않는다. UAHF와 Execution은 파이프라인의 하류에서 **기존 그대로** 소비되는 요소다. 이로써 Glossary INV-3("Layer는 정확히 6개다")는 UAF 신설로도 무촉이다.

### §2.4 의존 방향 (Dependency Direction)

UAF의 요소 간 의존은 **위→아래 단방향**이다. 하위 요소는 상위 요소를 알지 못하며, 상위 요소만이 하위 요소를 안다.

- **UAHF는 Entry·Entry Resolution·Project Discovery를 모른다.** UAHF가 아는 것은 자신에게 주어질 수 있는 선택 입력, 즉 Project Contract 하나뿐이다. Entry·Discovery는 UAHF의 인지 밖(상류)에 있다.
- **Entry는 Project Contract를 직접 만들지 않는다 (P1).** Entry Layer의 책임은 **Entry Resolution만**이다 — 진입을 판별해 Discovery Request를 산출하는 데서 멈춘다. Project Contract를 생성하는 것은 Project Discovery의 책임이며, Entry는 Discovery를 수행하지 않는다 (UAF-INV ④).
- **의존의 폐쇄성.** Discovery는 Entry로 역참조하지 않고, Contract는 Discovery 내부 개념(질문·전략·예산)으로 역참조하지 않는다. 이 폐쇄성이 각 요소의 교체 가능성을 성립시킨다 (Strategy Invariance의 구조 측 조건, §5 UAF-INV ③).

의존 방향을 단방향으로 고정함으로써, 상위 요소(Entry·Discovery)의 교체가 하위 요소(UAHF·Execution)에 파급되지 않는다. 파급을 차단하는 유일 접점이 Project Contract다.

---

## §3. 설계 원칙 (Design Principles — 9종)

UAF는 다음 9종 원칙을 따른다. UAHF와 동형인 원칙은 UAHF 정본을 § 포인터로 참조하며 재정의하지 않는다.

1. **AI-Agnostic** — UAF는 특정 AI 모델·실행 환경에 종속되지 않는다. Entry·Discovery의 물리 실현은 Adapter 소관이다 (uahf/ARCHITECTURE.md §3.1 동형 원칙을 UAF 레벨에 적용).
2. **Stable Contract** — Project Contract는 장기 호환을 유지하는 공식 계약(Public API)이다. Discovery 내부 변경과 독립적으로 안정을 유지한다 (P3, §4).
3. **Stable Core** — UAHF 정본(Core)은 UAF 신설로 변경되지 않는다. UAF는 UAHF를 감싸되 무수정으로 감싼다. 접점은 Project Contract 하나다 (UAF-INV ①, §5).
4. **Layer Separation** — Entry·Resolution·Discovery·Contract·UAHF·Execution은 서로 독립된 관심사로 분리된다. 한 요소의 내부 변경이 다른 요소의 규격으로 새지 않는다 (uahf/ARCHITECTURE.md §3.2 Modular 동형).
5. **Dependency Direction** — 의존은 위→아래 단방향이다. 하위는 상위를 모른다 (§2.4).
6. **Event Driven** — Discovery의 상태 전이는 Event로만 일어나고, 관측 지표(Metrics)는 그 Event에서 파생된다. (전이·이벤트·지표의 상세 정본은 후속 `discovery/specs/02-discovery.md`(예정) 소관 — 본 문서는 원칙만 선언한다.)
7. **Capability First** — Strategy·Entry의 확장 대상은 고정 열거가 아니라 **Capability 선언**으로 선택된다. 신규 능력은 선언을 등록하면 참여한다.
8. **Policy as Data** — 진입 판별의 결정 테이블, Discovery의 임계값·예산·종료 규칙은 코드가 아니라 **데이터(Policy)**다. 정책 변경이 엔진 변경을 요구하지 않는다.
9. **Future Extensibility** — 신규 Entry·Strategy·Runtime은 Layer·엔진 변경 없이 **Registry 행·Policy 데이터 추가만으로** 확장된다. Framework 전체를 다시 쓰지 않는다 (uahf/ARCHITECTURE.md §8 동형 지향을 UAF 레벨에 적용).

---

## §4. 사용자 고정 Architecture 원칙 (P1~P5)

다음 5건은 사용자가 고정한 UAF Architecture 원칙이며, 본 문서의 정본 문면이다. 후속 전 산출물이 이를 훼손해서는 안 된다.

- **P1 — Entry = Entry Resolution만.** Entry Layer는 UAF 공식 진입점으로서 사용자 입력으로 진입 종류를 판별하고 **Entry Resolution만 담당**한다. Discovery를 수행하지 않으며, 출력은 Discovery Request까지다 (§2.4, UAF-INV ④).
- **P2 — Discovery = Project Contract를 생성하는 Compiler.** Project Discovery는 단일 기능이 아니라 **Compiler**다. 어떤 Discovery Strategy를 쓰든 결과는 항상 **동일한 Project Contract**다 (**Strategy Invariance**, UAF-INV ③). Strategy는 교체 가능한 증거 수집 Front-end이고, Contract 산출 형식은 단일 타깃이다.
- **P3 — Project Contract = UAF↔UAHF 공식 Stable Contract(Public API).** Project Contract는 UAF와 UAHF를 잇는 **공식 안정 계약**이다. Discovery는 교체 가능하되 Contract는 장기 유지된다. UAF와 UAHF의 접점은 이 계약 하나뿐이다 (UAF-INV ①②).
- **P4 — Discovery 책임 경계.** Project Discovery가 담당하는 것과 담당하지 않는 것을 명확히 가른다. 담당 4건·비담당 5건의 정본 경계표는 §6에 둔다.
- **P5 — 설계 순서 = Layer → Workflow → Module → Contract.** UAF의 설계는 상위 구조(Layer)를 먼저 고정하고, 그다음 오케스트레이션(Workflow), 모듈 구성(Module), 마지막에 계약 상세(Contract)를 고정하는 순서로 진행한다.
  - **결정 기록.** Contract의 지위(공식 Stable Contract)와 스키마 안정성 불변은 본 W1(Layer 단계)에서 선언되므로 인터페이스 방향성은 선행 확보되고, Contract의 상세 스키마는 마지막 단계에서 고정한다. 이 설계 순서는 사용자 고정 원칙(P5)이며, 방법론 상세는 정본이 아니라 비정본 부록 소관이다 (Non-Goals, §7; UAF-INV ⑥).

### §4.6 상시 불변 확인 2건

다음 2건은 후속 모든 산출물이 통과해야 하는 상시 확인 항목이다. 통과하지 못한 산출물은 승인 대상이 아니다.

- **① Project Discovery는 단일 기능이 아니라 Project Contract를 생성하는 Compiler다.** 산출물은 Discovery를 **언제든 교체 가능하게** 유지해야 한다 — Strategy·Discovery 내부 개념(질문·전략·예산)이 Contract 코어 스키마나 UAHF 접점으로 새어나가서는 안 된다 (P2, UAF-INV ②③).
- **② Project Contract는 UAF↔UAHF 공식 Stable Contract(Public API)다.** 장기 호환성 규칙(스키마 버전 규율·소비자의 관용적 읽기·필드 제거 금지)이 훼손되어서는 안 된다. 규칙의 상세 정본은 후속 `planning/specs/03-project-contract.md`(예정)가 소유하며, 본 문서는 지위와 원칙만 선언한다 (P3, UAF-INV ①②).

---

## §5. UAF 불변 (UAF-INV — 6건)

UAF는 어떤 구현·확장에서도 다음 6건을 유지한다.

- **UAF-INV ①** — **UAHF 정본 무수정.** UAF의 신설·확장은 UAHF 정본(ARCHITECTURE.md·specs/·framework/·상위 규약)을 변경하지 않는다. UAF와 UAHF의 접점은 **Project Contract 하나뿐**이다.
- **UAF-INV ②** — **Discovery 교체 가능·Project Contract 교체 불가.** Project Discovery(및 그 Strategy)는 언제든 교체될 수 있으나, Project Contract의 스키마는 안정성을 유지한다(교체 불가). 안정 계약이 교체 가능한 생산자를 흡수한다.
- **UAF-INV ③** — **Strategy Invariance.** 어떤 Discovery Strategy를 쓰든 산출 결과는 항상 **동일한 Project Contract**(동일 스키마·동일 완결 기준)다. Front-end가 바뀌어도 출력 계약은 불변이다.
- **UAF-INV ④** — **Entry는 Discovery를 수행하지 않는다.** Entry Layer의 책임은 Entry Resolution까지이며, Discovery Request를 산출하는 데서 멈춘다. Contract 생성은 Project Discovery의 책임이다.
- **UAF-INV ⑤** — **확정 게이트 = 사용자 승인 (Preserve Human Authority).** Project Contract가 Execution Ready로 확정되는 게이트는 **사용자 승인**이다. 사용자 승인 없이 Ready 종단에 도달하지 않는다.
- **UAF-INV ⑥** — **Framework는 특정 방법론을 모른다.** UAF는 특정 발견·설계 방법론을 알지 않는다. 방법론은 교체 가능한 **Strategy Provider**만이 안다. 방법론 지식이 Framework 정본으로 새지 않는다.

---

## §6. 책임 경계표 (Responsibility Boundary — P4)

Project Discovery가 **담당하는 것(4)**과 **담당하지 않는 것(5)**의 정본 경계다. 비담당 5건은 하류(UAHF 및 그 Execution)의 책임이며, Discovery는 Project Contract를 산출한 지점에서 멈춘다.

| 구분 | 항목 |
|---|---|
| **담당 (4)** | ① 프로젝트 이해 (대상 프로젝트의 의도·요구·제약·리스크·방향 파악) |
| | ② Discovery 수행 (증거 수집·확신 판정·적응적 진행) |
| | ③ Execution Ready 판단 (계약 완결성·확신·사용자 승인의 종단 판정) |
| | ④ Project Contract 생성 (단일 타깃 형식으로의 컴파일) |
| **비담당 (5)** | ① Agent 실행 (UAHF Agent Layer 소관) |
| | ② Planning (구현 계획·작업 분해 — UAHF Advisor/Planner 소관) |
| | ③ Workflow 실행 (분해·병렬 디스패치·병합 — UAHF Workflow Layer 소관) |
| | ④ Memory Consult (기억 회수 — UAHF Memory Service 소관) |
| | ⑤ UAHF Execution (핵심 루프 구동 — UAHF 하류 소관) |

주: 비담당 5건은 전부 **하류 UAHF의 책임**이다. Discovery가 이들을 수행하지 않음으로써 의존 방향(§2.4)과 UAHF 무수정(UAF-INV ①)이 함께 성립한다. 비담당 항목의 상세 계약 정본은 각 UAHF spec(uahf/specs/02-agent.md·07-workflow.md·04-memory.md 등)이 소유하며, 본 표는 § 포인터로만 경계를 가른다.

---

## §7. Non-Goals

UAF v1.1은 다음을 **설계하지 않는다**.

- **Agent Runtime 설계 제외** — 에이전트 실행 기반은 UAHF Agent/Runtime Layer 소관이며, UAF는 이를 재설계하지 않는다.
- **Memory 설계 제외** — 기억의 기록·회수는 UAHF Memory Service(Cross-cutting) 소관이다 (uahf/ARCHITECTURE.md §5.1).
- **Execution Engine 설계 제외** — 핵심 루프 구동은 UAHF 하류 소관이다.
- **Workflow Engine 설계 제외** — 작업 분해·오케스트레이션은 UAHF Workflow Layer 소관이다.
- **Extension System 설계 제외** — UAHF의 기존 확장 서브시스템(Hooks/Skills/Plugins)은 자리(slot)로만 표기하고 재설계하지 않는다 (§2.2).

다음은 **확장 포인트로만** 열어두고 v1.1 본문에서 설계하지 않는다.

- **Discovery 실행 호스팅** — Discovery를 어느 실행 주체가 호스팅하는가는 **역할 추상까지만** 정의하고, 물리 호스팅은 설계하지 않는다.
- **Discovery의 Memory 활용** — Discovery가 UAHF Memory를 회수·활용하는 경로는 **확장 포인트로만** 표기하고, v1.1에서 설계하지 않는다.

---

## §8. UAF 용어 (Glossary — 네임스페이스 분리)

UAF 신규 용어의 **소유 지점**은 이 절(및 후속 `각 Layer specs/` 정본, 예정)이다.

- **네임스페이스 분리.** UAF 용어는 UAHF Glossary(uahf/specs/00-glossary.md)에 신설·병합하지 않는다. 같은 단어가 양쪽에서 쓰이면(예: "Layer" — §0 용어 주의, "Runtime" — §2.2, "Policy") **네임스페이스로 구분**한다. UAHF 용어는 Glossary 정본을 § 포인터로 참조하고 재정의하지 않는다.
- **향후 분권.** 아래 용어 중 상세 계약을 요하는 항목의 정본은 후속 `각 Layer specs/`가 이어받는다. 본 절은 상위 구조 수준의 정의와, **선행 확정이 필요한 인터페이스 추상**을 고정한다.

### §8.1 용어 정의

- **Entry** — UAF 공식 진입점. 사용자 입력을 수용하는 추상 연산이다. 물리 실현(진입 명령의 형태)은 Adapter 소관이다. 상세 정본: `entry/specs/01-entry.md`(예정).
- **Entry Resolution** — Entry가 명시 진입과 Workspace Evidence를 결정 테이블(Policy as Data)로 평가해 **Discovery Request**를 산출하는 연산. Discovery를 수행하지 않는다 (P1, UAF-INV ④). 상세 정본: `entry/specs/01-entry.md`(예정).
- **Discovery Request** — Entry Resolution의 출력이자 Project Discovery의 입력인 데이터 계약. 3요소 구조(§8.2에서 확정).
- **Project Discovery** — Discovery Request(+증거)를 입력으로 **Project Contract를 산출하는 Compiler**. 상세 정본: `discovery/specs/02-discovery.md`(예정).
- **Discovery Dimension** — Discovery가 확신을 측정하는 축. 상세(차원 목록·판정)의 정본: `discovery/specs/02-discovery.md`(예정).
- **Confidence** — Discovery Dimension별 확신도. 상세(척도·근거 등급·임계)의 정본: `discovery/specs/02-discovery.md`(예정).
- **Question Budget** — 질문의 총량·차원별 예산. Policy as Data. 상세 정본: `discovery/specs/02-discovery.md`(예정).
- **Execution Ready** — Discovery의 종단 판정. 계약 완결성 ∧ 확신 ∧ **사용자 승인**의 결합이다 (UAF-INV ⑤). 상세(판정식·종단 종류)의 정본: `discovery/specs/02-discovery.md`(예정).
- **Project Contract** — UAF↔UAHF 공식 **Stable Contract(Public API)**. Project Discovery의 산출이자 UAHF의 선택 입력이다 (P3, UAF-INV ①②). 상세(스키마·버저닝·UAHF Interface)의 정본: `planning/specs/03-project-contract.md`(예정).
- **Strategy / Strategy Provider** — 교체 가능한 증거 수집 Front-end와 그 제공자. Capability 선언 기반으로 선택된다 (Capability First). 특정 방법론은 이 Provider만이 안다 (UAF-INV ⑥). 상세 정본: `discovery/specs/02-discovery.md`(예정).

### §8.2 Discovery Request 인터페이스 추상 (여기서 확정)

**Discovery Request**는 Entry Resolution의 출력이자 Project Discovery의 입력인 데이터 계약이다. 이 추상은 본 절에서 확정되며, 후속 병렬 작업(`entry/specs/01-entry.md`·`discovery/specs/02-discovery.md`)의 **선행 확정 인터페이스**가 된다 — 두 작업은 이 확정 계약만 참조한다.

Discovery Request는 **3요소** 구조다.

| 요소 | 정의 |
|---|---|
| **mode** | 발견 모드. **닫힌 열거가 아니라 확장 가능한 네임스페이스**다. 초기 등재값: `greenfield` / `incremental` / `brownfield`. 신규 모드는 열거 변경 없이 네임스페이스에 등재된다 (Future Extensibility). |
| **inputs** | Discovery가 참조할 **Evidence 참조 목록**. 초기에는 Workspace Evidence(Project Contract 유무·Repository 유무 등)를 참조로 담되, 신규 Evidence Source 타입의 등록으로 확장 가능하다 (스키마 열림). 미완성·동시 작성 중인 산출물이 아니라 **확정된 참조**만 담는다. |
| **policy** | **Discovery Policy 참조**. 임계값·예산·종료 규칙 등 정책 데이터를 가리킨다 (Policy as Data). 정책 값의 상세 정본은 `discovery/specs/02-discovery.md`(예정) 소관이며, Discovery Request는 참조만 담는다. |

- **닫힘 없음 원칙.** mode는 확장 네임스페이스, inputs는 Evidence 참조 목록으로 일반화되어 있어, 신규 진입·신규 증거·신규 모드가 이 계약을 깨지 않고 확장된다.
- **경계.** Discovery Request는 Entry Resolution의 산출까지의 계약이다. Contract 자체를 담지 않으며(그것은 Discovery의 산출), Discovery 내부 개념(질문·전략)을 담지 않는다 (의존 방향, §2.4).

---

## 물리 Layer 매핑 (v1.2.1 구조 이동)

위 6요소 파이프라인(§2.1)은 다음 물리 Layer 디렉터리에 대응한다.

| 파이프라인 요소 | 물리 Layer 디렉터리 | Layer ARCHITECTURE 포인터 |
|---|---|---|
| Entry Layer | `entry/` | `entry/ARCHITECTURE.md` |
| Entry Resolution · Project Discovery | `discovery/` | `discovery/ARCHITECTURE.md` |
| Project Contract | `planning/` | `planning/ARCHITECTURE.md` |
| UAHF | `uahf/` | `uahf/ARCHITECTURE.md` |
| Execution | `uahf/` (실행 단계 — 별도 디렉터리 없음) | `uahf/ARCHITECTURE.md` |

- `knowledge/`는 파이프라인 단계가 아니라 모든 Layer가 Consult하는 공용 Knowledge Base다(원칙 10).

**주.** 완전한 루트 ARCHITECTURE(새 Layer 구조·knowledge 반영)의 재저술은 후속 트랙이다. 본 절과 이관은 v1.2.1 구조 이동 산출물이며, §0~§8의 논지는 무변경으로 보존된다.
