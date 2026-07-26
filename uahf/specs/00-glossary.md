# specs/00-glossary — Glossary Specification

Version: 0.3
Status: Frozen (v0.3 개정 — §3.2-G Frozen 정의의 개정 기록 locus 를 git 으로 이전. 사용자 결정 2026-07-27)
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

이 문서는 UAHF의 공용 용어를 정의한다.

모든 spec은 여기 정의된 용어만 사용한다.

이 문서의 책임은 세 가지다.

- Layer, Cross-cutting Service, Component, Agent, 계약 용어의 정본(canonical) 정의를 한 곳에 모은다.
- ARCHITECTURE.md 0.2와 모든 spec 사이의 용어 정합성을 보장한다.
- 용어 충돌과 미정의 용어 사용을 예방한다.

## Non-Goals

- 이 문서는 설계 원칙을 재정의하지 않는다. ARCHITECTURE.md 섹션을 참조로만 연결한다.
- 이 문서는 각 Component의 상세 계약을 정의하지 않는다. 상세는 각 담당 spec이 정의한다.
- 이 문서는 구현을 정의하지 않는다. 용어는 AI 비의존 계약이다.

---

# §2. Position

- 아키텍처 상 위치: Layer도 Cross-cutting Service도 아니다. 전 Layer·전 Component가 공유하는 용어 기준 문서(foundational reference)다.
- 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것):
  - ARCHITECTURE.md 0.2 (실재)
  - specs/TEMPLATE.md (실재)
  - .claude/AGENT.md (실재)
  - ROADMAP.md v0.1 (실재)
- 이 spec에 의존하는 spec:
  - specs/01-runtime.md ~ specs/13-harness.md 전체. 모든 spec은 용어를 Glossary에서 가져온다.
  - specs/01 ~ specs/13 전체가 작성 완료 상태로 실재한다 (placeholder 아님, Wave 3 완료).
- 순환 의존: 없다. Glossary는 어떤 spec에도 의존하지 않는다. 의존은 항상 spec → Glossary 방향이다.

---

# §3. Core Contract (AI 비의존)

이 섹션이 용어 정의 본문이다.

용어는 AI 비의존 계약이므로 Core Contract에 배치한다.

## 3.1 Interface

- 입력: 임의의 spec 또는 Agent가 참조하는 용어.
- 출력: 해당 용어의 정본 정의.
- 완료 조건: 참조된 모든 용어가 §3.2에 정의되어 있다.
- 실패 보고 포맷: 미정의 용어를 발견하면 "미정의 용어: <용어> / 참조 위치: <spec §>" 형식으로 Advisor에게 Glossary 추가를 요청한다. 스스로 새 용어를 만들지 않는다.

## 3.2 Data Format — 용어 정의

용어는 10개 카테고리로 나눈다.

- A. Layer (6)
- B. Cross-cutting Service 및 Layer 판정 기준
- C. Memory Service 용어
- D. Core Component (13)
- E. Agent 역할 (4)
- F. Agent Lifecycle (7단계)
- G. 계약 용어
- H. 설계 원칙 (참조 전용)
- I. Runtime 계약 용어 (5)
- J. 컴포넌트 계약 용어 (spec별)

### 용어 범위 주의 (Disambiguation)

일부 단어는 Layer와 Component 양쪽에서 쓰인다. 범위가 다르므로 별도 정의한다.

- Workflow: Layer(A) vs Component(D)
- Agent: Layer(A) vs Component(D) vs 역할 주체(E)
- Runtime: Layer(A) vs Component(D)
- Adapter / Adapters: Layer(A) vs Component(D)
- Memory: Cross-cutting Service(C) vs Component(D)
- Verifier: Agent 역할(E) vs Component(D)

참조 시 어느 범위인지 명시한다.

---

### A. Layer (6)

Layer는 UAHF 아키텍처의 수직 스택을 이루는 지층(stratum)이다.

스택 순서는 다음과 같다 (ARCHITECTURE.md 5).

Presentation → Workflow → Agent → Runtime → Core → Adapter

각 Layer는 서로 독립적으로 동작한다.

주의: ARCHITECTURE.md 5는 스택 순서만 명시하고 각 Layer의 책임을 명문화하지 않는다. 아래 책임 경계는 ARCHITECTURE.md 0.2와 ROADMAP.md v0.1 힌트에서 도출한 것이며, 일부는 제안이다. 제안 항목은 (제안) 표시하고 §9에 에스컬레이션한다.

**Presentation Layer**
사용자와 Framework 사이의 진입점. 명령과 문서를 통해 UAHF와 상호작용하는 표면.
근거: ROADMAP.md v0.9 "Presentation 최소 기능 (명령/문서 진입점)". (도출)

**Workflow Layer**
큰 작업을 분해하고, 여러 Agent에게 병렬로 디스패치하며, 결과를 병합·검증하는 오케스트레이션 계층.
근거: ROADMAP.md v0.7. (도출)

**Agent Layer**
명확한 책임을 가진 개별 Agent가 작업을 수행하는 계층. Advisor / Planner / Worker / Verifier가 여기서 동작한다.
근거: ARCHITECTURE.md 3.3 Agent First. (도출)

**Runtime Layer**
Agent와 모듈의 실행·수명주기·설정(config)을 관장하는 실행 환경 계층. Loop Engine이 이 계층에서 Lifecycle을 구동한다.
근거: ROADMAP.md v0.3 "모듈 시스템, 설정, 수명주기". (Advisor 확정 — §9-OQ1 결정)

**Core Layer**
AI 비의존 계약과 모듈 시스템의 근간을 정의하는 계층(Adapter 위). 모든 Core Contract가 여기에 귀속되며 AI 의존 요소를 포함하지 않는다.
근거: ROADMAP.md v0.3 (Core 규격은 AI 비의존, Core 디렉터리에 AI 의존 요소 없음). (Advisor 확정 — §9-OQ1 결정)

**Adapter Layer**
Core 계약을 특정 AI 모델·실행 환경·영속성 백엔드에 바인딩하는 최하위 경계 계층. 이식 시 이 계층만 교체한다.
근거: ARCHITECTURE.md 3.1, 5.1, 8. (도출)

---

### B. Cross-cutting Service 및 Layer 판정 기준

**Layer (지층 / stratum)**
수직 스택에서 고정된 한 위치를 차지하는 계층. 주로 인접 Layer가 소비한다.

**Cross-cutting Service (관통 서비스 / capability)**
스택의 특정 위치에 고정되지 않고 모든 Layer를 관통하는 능력(capability). 단일 Port로만 접근한다.
UAHF의 Cross-cutting Service는 Memory Service 하나다 (ARCHITECTURE.md 5.1).

**Layer vs Cross-cutting Service 판정 기준**
어떤 능력이 다음 세 조건을 모두 만족하면 Cross-cutting Service다.

1. 소비자가 여러 Layer에 걸친다.
2. 모든 Agent Lifecycle 사이클(Consult ~ Complete)에서 사용된다.
3. 스택의 특정 위치에 고정되지 않는다.

세 조건을 모두 만족하지 않고 스택의 한 위치를 차지하며 인접 Layer가 주로 소비하면 Layer(지층)다.

적용: Memory는 세 조건을 모두 만족하므로 Cross-cutting Service다 (ARCHITECTURE.md 5.1). 현재 세 조건을 모두 만족하는 것은 Memory뿐이다.

---

### C. Memory Service 용어

**Memory Service**
기억을 기록하고 회수하는 Cross-cutting Service. Layer가 아니다. 모든 Agent가 Lifecycle의 매 사이클마다 사용한다.
근거: ARCHITECTURE.md 5.1.

**Memory Service Interface (단일 Port)**
Memory에 접근하는 유일한 경로. Agent, Loop, Workflow, Verifier는 이 Interface를 통해서만 Memory에 접근한다.
근거: ARCHITECTURE.md 5.1.

**Port**
어떤 능력에 접근하는 단일 계약 경로. Memory Service는 정확히 하나의 Port(Memory Service Interface)만 노출한다. 영속성 백엔드는 이 Port 뒤의 Adapter Layer에 위치한다.
근거: ARCHITECTURE.md 5.1.

**회수 정책 (Recall Policy)**
Memory를 읽는 규칙. 계약에 내장된다. 필요할 때만, 목적을 명시하고, 최소 범위로 읽는다. Token Efficiency 원칙을 구현한다.
근거: ARCHITECTURE.md 5.1, 3.6, ROADMAP.md v0.4.

**Lessons**
실패에서 도출된 교훈. Memory Service 위의 특화 계약이다. 실패는 Lesson 후보가 되고, 다음 작업에서 회수된다.
근거: ARCHITECTURE.md 5.1, AGENT.md Memory, ROADMAP.md v0.4. 담당 spec: specs/05-lessons.md.

**Best Practice**
성공에서 도출된 재사용 가능한 모범 사례. Lessons와 대칭인 Memory Service 위의 특화 기록이다. 모든 성공은 Best Practice 후보가 된다.
근거: AGENT.md Memory. (specs/02-agent.md §9-OQ-3 요청으로 Advisor 승인 추가)

---

### D. Core Component (13)

Component는 독립적으로 사용 가능한 기능 단위다. 통합하면 하나의 Development Operating System이 된다 (ARCHITECTURE.md 6).

Memory와 Lessons는 Layer 스택이 아닌 Cross-cutting Service로 동작한다 (ARCHITECTURE.md 6).

순서는 ARCHITECTURE.md 6의 나열 순서를 따른다.

| Component | 정의 | 담당 spec |
|---|---|---|
| Scaffold | 신규 프로젝트에 UAHF를 부트스트랩(설치·초기화)하는 도구. | specs/12-scaffold.md |
| Harness | Agent가 스스로를 개발·운용하기 위한 최소 실행 골격. self-hosting의 기반. | specs/13-harness.md |
| Workflow (Component) | 큰 작업의 분해·병렬 디스패치·병합·검증을 정의하는 오케스트레이션 규격. | specs/07-workflow.md |
| Agent (Component) | 명확한 책임을 가진 작업 수행 주체의 공통 규격. Advisor/Planner/Worker/Verifier의 공통 계약. | specs/02-agent.md |
| Runtime (Component) | 모듈 시스템·설정(config)·수명주기를 관장하는 실행 환경 규격. | specs/01-runtime.md |
| Loop | Agent Lifecycle(Consult ~ Complete)을 자동 반복하는 오케스트레이션 엔진. | specs/03-loop.md |
| Memory (Component) | 기억의 기록·회수 규격. Cross-cutting Service로 동작. | specs/04-memory.md |
| Lessons | 실패에서 도출된 교훈의 기록·회수 규격. Memory Service 위의 특화 계약. | specs/05-lessons.md |
| Verifier (Component) | Worker 완료 보고를 독립적으로 판정하는 검증 규격. | specs/06-verifier.md |
| Plugins | 기능 묶음 배포 단위. 본체 수정 없이 기능을 추가한다. | specs/10-plugins.md |
| Skills | 재사용 가능한 작업 능력 단위. | specs/09-skills.md |
| Hooks | 이벤트 기반 확장점. | specs/08-hooks.md |
| Adapters (Component) | Core 계약을 특정 AI·환경·영속성 백엔드에 바인딩하는 규격. | specs/11-adapters.md |

**Component→Layer 매핑 (Advisor 확정 — §9-OQ6 이행)**

| Component | 귀속 | 근거 |
|---|---|---|
| Runtime | Runtime Layer | specs/01 §2 |
| Agent | Agent Layer | specs/02 §2 |
| Loop | Runtime Layer | §9-OQ2 결정, specs/03 §2 |
| Workflow | Workflow Layer | specs/07 §2 |
| Memory / Lessons | Cross-cutting Service (Memory Service / 그 위 특화 계약) | ARCHITECTURE 5.1 |
| Verifier | Agent Layer (판정 역할; 실행 단위는 Runtime이 호스팅하는 Module) | specs/06 §2 |
| Hooks / Skills / Plugins | 특정 Layer에 고정되지 않음 — Runtime Layer의 Module 계약 위 확장 서브시스템 | specs/08·09·10 §2 |
| Adapters | Adapter Layer | specs/11 §2 |
| Scaffold | Presentation Layer (사용자 대면 호출 표면; 산출물은 전 Layer에 걸치는 설치 도구) | specs/12 §9-OQ-1 결정 |
| Harness | 단일 Layer 아님 — 여러 Layer 요소의 최소 구성 조합(composition) | specs/13 §2 |

주: Cross-cutting 판정 3조건(§3.2-B)을 만족하는 것은 Memory뿐이다. Hooks/Skills/Plugins/Harness는 스택에 고정되지 않으나 관통 능력이 아닌 확장·조합 규격이므로 Cross-cutting Service가 아니다 (INV-3 유지).

---

### E. Agent 역할 (4)

Agent는 명확한 책임을 가진 작업 수행 주체다. 모든 Agent는 AGENT.md 공통 규약을 따른다.

역할 분담 기준: Architecture 결정은 Advisor, 구현은 Worker, 검증은 Verifier (AGENT.md Delegation, .claude/CLAUDE.md).

**Advisor**
메인 조언자. Architecture, Spec, 설계 결정, 검증, 최종 승인을 담당한다. 계획·작업 분해·Worker 위임에 집중하고, 불필요한 직접 구현은 하지 않는다. Worker 결과를 반드시 검증 후 승인한다.
근거: .claude/CLAUDE.md, AGENT.md Delegation.

**Planner**
Advisor로부터 위임받아 구현 계획과 작업 분해의 초안을 작성한다. 계획의 채택·승인과 Architecture 결정은 Advisor 소관이며, Planner는 결정 권한을 갖지 않는다. (Advisor 확정 — §9-OQ4 결정)
근거: AGENT.md Purpose(역할 열거), ROADMAP.md v0.2(Agent 4종).

**Worker**
구현을 담당한다. Advisor의 위임을 받아 산출물을 생성하고, 완료 보고를 남긴다. 실패를 숨기지 않는다. 실행 모델 바인딩은 Adapter Binding 영역이다 (§4.1).
근거: AGENT.md Delegation, .claude/CLAUDE.md.

**Verifier**
검증을 담당한다. Worker 완료 보고를 그대로 신뢰하지 않고 독립적으로 판정한다.
근거: AGENT.md Delegation, Verification.

---

### F. Agent Lifecycle (7단계)

**Agent Lifecycle**
모든 Agent 작업이 거치는 7단계 수명주기. Loop Engine이 이를 자동 반복한다.
단계 순서 (AGENT.md):

Consult → Plan → Execute → Verify → Learn → Memory Update → Complete

주의: AGENT.md는 단계 이름만 열거한다. 아래 한 줄 정의는 AGENT.md Core Principles에서 도출했다. 각 단계의 상세 계약은 specs/03-loop.md에서 확정된다.

- **Consult** — 착수 전 상위 규약·Architecture·Memory를 참조한다.
- **Plan** — 작업을 계획·분해한다.
- **Execute** — 계획을 구현한다.
- **Verify** — 결과를 독립적으로 검증한다.
- **Learn** — 실패와 성공에서 교훈을 도출한다.
- **Memory Update** — 필요 시 Memory와 Lessons를 갱신한다.
- **Complete** — 검증을 통과한 뒤에만 완료한다.

---

### G. 계약 용어

**Core Contract**
AI에 의존하지 않는 계약. 입력/출력/완료 조건/데이터 포맷/불변 규칙을 정의한다. 특정 AI 의존 내용이 한 줄도 들어가지 않는다.
근거: TEMPLATE.md §3, ROADMAP.md 2.3.

**Adapter Binding**
Core Contract를 특정 AI 실행 환경에 구현하는 환경 의존 바인딩. v0.x의 첫 번째 Adapter 바인딩이 이에 해당한다.
근거: TEMPLATE.md §4, ROADMAP.md 2.3.

**이식 교체 지점 (Portability Swap Point)**
다른 AI 환경으로 이식할 때 바뀌는 모든 것. Core Contract는 유지되고 Adapter Binding만 교체된다.
근거: TEMPLATE.md §4.2, ARCHITECTURE.md 3.1.

**Invariant (불변 규칙)**
어떤 구현에서도 지켜야 할 규칙. 구현이 바뀌어도 변하지 않는다.
근거: TEMPLATE.md §3.3.

**Spec Status**
spec의 성숙 단계. 세 값을 가진다.
- Draft — Worker 작성 중.
- Review — 검증 및 Advisor 검토 중.
- Frozen — v0.1 기준선 확정. 이후 변경은 spec 버전 상승과 **개정 기록**이 필수다(기록 locus = git 커밋 — 운용 절차 정본 = `docs/spec-versioning-policy.md` §3).
근거: TEMPLATE.md §4.

**Definition of Done (DoD, 완료 기준)**
spec이 Frozen이 되기 위해 만족해야 하는 8개 품질 기준. TEMPLATE.md §3에 정의된다. 검증 가능한 형태여야 하며, "시연할 수 있는 문장"으로 환원된다.
근거: TEMPLATE.md §3, §7.

**Wave**
병렬 집합(Parallel Set)의 순차 배치 단위. 하나의 Wave는 동시에 디스패치 가능한 한 병렬 집합의 실행 회차다. Planner의 Wave 설계가 큰 작업을 Wave 단위로 배치한다. (v0.9 정본화 — ROADMAP·운용 문서의 편의 라벨을 정본 표제어로 승격.)
근거: specs/07-workflow.md §3.2-A(병렬 집합), AGENT.md Delegation(Planner의 Wave 설계).

**Baseline**
사용자 승인으로 확정된 인스턴스 문서(framework/ 이하)·운용 문서의 상태. spec의 Frozen(§3.2-G Spec Status)에 대응하는 확정 상태 라벨이다. (v0.9 정본화 — v0.3~v0.8 상태 라인 관행의 정본화.)
근거: docs/spec-versioning-policy.md §3.3.

**형태 A / 형태 B**
실현 형태를 서술하는 라벨. 형태 A = 계약·규약 문서와 관행으로 실현된 상태(문서 실현), 형태 B = 실행 코드로 실현된 상태(실행 실현). 형태 A→B 전환에도 Core Contract 변경은 0이다(structure.md C-1). (v0.9 정본화 — 실현 형태 서술 라벨의 정본화.)
근거: framework/core/structure.md §4(형태 A/형태 B 라벨 첫 사용처).

---

### H. 설계 원칙 (참조 전용)

설계 원칙은 여기서 재정의하지 않는다. ARCHITECTURE.md 섹션 참조로만 연결한다.

| 원칙 | 참조 |
|---|---|
| AI Agnostic | ARCHITECTURE.md 3.1 |
| Modular | ARCHITECTURE.md 3.2 |
| Agent First | ARCHITECTURE.md 3.3 |
| Verify Everything | ARCHITECTURE.md 3.4 |
| Learn from Failure | ARCHITECTURE.md 3.5 |
| Token Efficiency | ARCHITECTURE.md 3.6 |
| Human Approval | AGENT.md Core Principles (계약화: specs/03-loop.md §3.1-D) |

---

### I. Runtime 계약 용어 (5)

(specs/01-runtime.md §9 요청으로 Advisor 승인 추가)

**Module (모듈)**
독립적으로 사용·교체 가능한 기능 단위. 안정적 id와 구현 contract를 가지며 Runtime이 등록·해소·교체한다.
근거: ARCHITECTURE.md 3.2, specs/01-runtime.md §3.

**Module System (모듈 시스템)**
Module의 정의·등록·해소·교체 규칙의 총체. Runtime Component가 관장한다.
근거: specs/01-runtime.md §3.1-A.

**Module Manifest**
Module의 등록 서술자. 필드 정의는 specs/01-runtime.md §3.2-A가 정본이다.

**Config (설정)**
스코프(Global / Project / Module)와 우선순위를 가진 key→value 설정 트리. 상세는 specs/01-runtime.md §3.2-B가 정본이다.

**Runtime Context**
Bootstrap의 산출물이자 호스팅 상태. 필드 정의는 specs/01-runtime.md §3.2-C가 정본이다.

---

### J. 컴포넌트 계약 용어 (spec별)

각 spec의 §9 Glossary 추가 요청으로 Advisor가 승인한 컴포넌트 계약 용어다. 각 용어는 한 줄 정의와 정본 포인터만 둔다. 상세 필드의 정본은 소유 spec이 유지한다 (I 카테고리와 동일 방식).

**J-03 (Loop, specs/03-loop.md — §9 요청으로 Advisor 승인 추가):**
- 재작업 루프 (Rework Loop) — Verify 실패 시 결함 근본 원인에 따라 Execute/Plan/Consult로 되돌아가 재시도하는 루프백. 재시도 한도 초과 시 에스컬레이션. 정본: specs/03-loop.md §3.1-B.
- 루프 상태 기록 (Loop State Record) — 각 단계 전이를 append-only로 남기는 전이 이벤트 로그. 정본: specs/03-loop.md §3.2-A.
- 단계 전이 (Stage Transition) — Lifecycle 한 단계에서 다음 단계로의 이동. 진입·완료 조건으로 규율된다. 정본: specs/03-loop.md §3.1-A.

**J-04 (Memory, specs/04-memory.md — §9 요청으로 Advisor 승인 추가):**
- Memory Item (기억 항목) — 기억의 최소 기록 단위. 정본: specs/04-memory.md §3.2-A.
- Memory Store — Memory Item의 저장 구조. 물리 형식은 Adapter 소관. 정본: specs/04-memory.md §3.2-E.
- Memory Index — 회수 대상을 최소 Context로 찾는 조회 구조. 정본: specs/04-memory.md §3.2-C.
- Index Entry — Memory Index의 경량 서술자. content 원문을 담지 않는다. 정본: specs/04-memory.md §3.2-C.
- Record (기록 연산) — Memory Service Interface의 쓰기 연산. 정본: specs/04-memory.md §3.1-A.
- Recall (회수 연산) — Memory Service Interface의 읽기 연산. purpose·scope 필수. 정본: specs/04-memory.md §3.1-B.

**J-05 (Lessons, specs/05-lessons.md — §9 요청으로 Advisor 승인 추가):**
- 적용 조건 (Applicability Condition) — Lesson·Best Practice가 언제 회수되어야 하는가를 규정하는 매칭 signature. 정본: specs/05-lessons.md §3.2-C.
- 승격 (Promotion) — 후보가 Advisor 승인으로 정식(Active) 기록이 되는 절차. 승격 권한은 Advisor. 정본: specs/05-lessons.md §3.1-A.
- 재발 (Recurrence) — 회수되었음에도 같은 실패가 다시 발생한 상태. 판정 3분류(Novel/RecallGap/Recurrence)의 하나. 정본: specs/05-lessons.md §3.1-C.

**J-06 (Verifier, specs/06-verifier.md — §9 요청으로 Advisor 승인 추가):**
- 검증 리포트 (Verification Report) — 판정의 기록 산출물. 정본: specs/06-verifier.md §3.2-A.
- 검증 유형 (Verification Type) — VT-1~VT-5 판정 방법 분류. 정본: specs/06-verifier.md §3.2-E.
- 재작업 지시 (Rework Instruction) — 검증 실패 시 Worker에게 반환되는 지시. 정본: specs/06-verifier.md §3.2-D.
- 거짓 완료 보고 (False Completion Report) — 완료 보고의 주장과 산출물의 불일치. 정본: specs/06-verifier.md §3.2-F.

**J-07 (Workflow, specs/07-workflow.md — §9 요청으로 Advisor 승인 추가):**
- Work Graph (작업 그래프) — 큰 작업의 분해 결과 포맷. 정본: specs/07-workflow.md §3.2-A.
- Task (하위 작업) — 분해의 최소 단위. done·interfaceContract·ownedBoundary 필수. 정본: specs/07-workflow.md §3.2-B.
- 병렬 집합 (Parallel Set) — 동시 디스패치 가능한 Task 그룹. 상호 비의존·소유 경계 비중첩. 정본: specs/07-workflow.md §3.2-A.
- 소유 경계 (Ownership Boundary) — 한 Task가 배타 소유하는 파일·계약 집합. 정본: specs/07-workflow.md §3.2-B.
- 인터페이스 계약 (Interface Contract) — Task가 제공·소비하는 확정된 계약. 병렬 Task는 이것만 참조한다. 정본: specs/07-workflow.md §3.2-B.

**J-08 (Hooks, specs/08-hooks.md — §9 요청으로 Advisor 승인 추가):**
- Event (이벤트) — 확정된 계약에서 도출된 관찰 가능한 지점. 정본: specs/08-hooks.md §3.2-A.
- Event Catalog (이벤트 카탈로그) — 바인딩 가능한 Event의 명명된 목록과 확장 규칙. 정본: specs/08-hooks.md §3.2-A/B.
- Phase (before/after) — Hook 실행 시점 지정 값. 정본: specs/08-hooks.md §3.2-A.
- Hook Binding — Hook을 (event, phase)에 연결하는 서술자. 정본: specs/08-hooks.md §3.2-D.
- Hook Dispatch — Event 발생 시 바인딩된 Hook을 결정적 순서로 격리 호출하는 실행 계약. 정본: specs/08-hooks.md §3.1-D.

**J-09 (Skills, specs/09-skills.md — §9 요청으로 Advisor 승인 추가):**
- Skill Manifest — Skill의 등록 서술자. Module Manifest의 특화. 정본: specs/09-skills.md §3.2-A.
- Trigger (트리거 조건) — 언제 Skill이 적용되는가를 선언하는 조건. 경량 메타데이터. 정본: specs/09-skills.md §3.2-A.
- Skill Body (지시 본문) — Skill 수행 절차. 선택된 뒤에만 로드된다. 정본: specs/09-skills.md §3.2-A.
- Skill I/O Contract — Skill의 입력·출력 계약. 재사용성의 기반. 정본: specs/09-skills.md §3.2-B.
- SkillInterface — Skill이 구현하는 공통 계약 식별자. 정본: specs/09-skills.md §3.2-A.

**J-10 (Plugins, specs/10-plugins.md — §9 요청으로 Advisor 승인 추가):**
- Plugin (개별 배포 단위) — 하나 이상의 Module(및 확장 요소)을 묶어 배포하는 자기완결 단위. 정본: specs/10-plugins.md §3.
- Plugin Manifest — Plugin의 배포 서술자. 정본: specs/10-plugins.md §3.2-A.

**J-11 (Adapters, specs/11-adapters.md — §9 요청으로 Advisor 승인 추가):**
- Adapter Interface — 하나의 Adapter가 제공해야 하는 바인딩 지점의 전체 집합. 정본: specs/11-adapters.md §3.2-A.
- 바인딩 지점 (Binding Point) — 하나의 이식 교체 지점을 바인딩하는 단위. 정확히 하나의 Core Contract 요소를 실현. 정본: specs/11-adapters.md §3.2-A.
- Conformance (적합성 판정) — 유효한 Adapter의 판정 (필수 바인딩 완전성 + Core 불변 + 핵심 루프 통과). 정본: specs/11-adapters.md §3.2-B.
- 완전 Adapter / 최소 구현 Adapter — Conformance 등급 2종. 정본: specs/11-adapters.md §3.2-B.
- 핵심 루프 (Core Loop) — 위임 → 구현 → 검증 → 승인 사이클. 정본: specs/11-adapters.md §3.1 (ROADMAP v0.2·v1.0 어휘의 정본화).

**J-12 (Scaffold, specs/12-scaffold.md — §9 요청으로 Advisor 승인 추가):**
- Project Template (프로젝트 템플릿) — Scaffold가 설치하는 구조의 추상 정의. 정본: specs/12-scaffold.md §3.2-A.
- Install Manifest (설치 매니페스트) — 설치 내용의 서술자. 멱등성·제거의 기준. 정본: specs/12-scaffold.md §3.2-B.
- 설치 검증 체크리스트 (Install Verification Checklist) — 설치 유효성 판정 계약 CK-1~CK-8. 정본: specs/12-scaffold.md §3.2-C.

**J-13 (Harness, specs/13-harness.md — §9 요청으로 Advisor 승인 추가):**
- 최소 구성 집합 (Minimal Composition Set) — Harness 성립에 필수인 5개 요소의 집합. 정본: specs/13-harness.md §3.2-A.
- Harness 상태 (Bootstrap / Formal) — 부트스트랩·정식 두 상태와 전이 조건 4개. 정본: specs/13-harness.md §3.2-B.
- 검증 게이트 (Verification Gate) — 완료 보고를 독립 검증 없이 승인하지 않는 통제 지점. 상세 판정은 06 소관. 정본: specs/13-harness.md §3.2-A.
- 작업 추적 (Task Tracking) — 위임 사이클의 진행·완료 상태와 결정을 기록·추적하는 필수 요소. 정본: specs/13-harness.md §3.2-A.

## 3.3 Invariants

- INV-1: 어떤 용어 정의도 ARCHITECTURE.md 0.2와 모순되지 않는다. 충돌이 발견되면 정의를 만들지 않고 §9에 보고한다.
- INV-2: Memory와 Lessons는 Layer가 아니다. Cross-cutting Service다.
- INV-3: Layer는 정확히 6개다. Cross-cutting Service는 Memory Service 1개다. Core Component는 13개다.
- INV-4: 모든 spec은 Glossary에 정의된 용어만 사용한다. 새 용어는 Glossary에 먼저 추가한다.
- INV-5: Core Contract 용어와 Adapter Binding 용어는 분리한다. 특정 AI 의존 정의는 Core 용어에 섞이지 않는다.
- INV-6: Glossary 자체는 AI 비의존이다. 특정 AI에 대한 정의를 담지 않으며, 어떤 AI도 "첫 번째 Adapter" 예시 이상으로 등장하지 않는다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

용어 정의 자체는 바인딩이 없다.

단, Agent 역할의 실행 모델 지정(예: v0.x에서 Worker의 기본 모델)은 Adapter Binding 영역이다. 상세는 specs/02-agent.md §4가 정의한다.

## 4.2 이식 교체 지점

해당 없음. 용어집은 이식 시 바뀌지 않는다. 다른 AI 환경으로 이식해도 용어 정의는 그대로 유지된다.

---

# §5. Memory Access (해당 시)

해당 없음. Glossary는 Memory를 읽거나 쓰지 않는다. Memory Service Interface에 접근하지 않는다.

---

# §6. Failure Modes

- 미정의 용어 사용: spec이 Glossary에 없는 용어를 사용한다. 대응 — §3.1 실패 보고 포맷으로 Advisor에게 추가 요청. Lesson 후보.
- 용어 충돌: 같은 용어를 두 spec이 다르게 해석한다. 대응 — Glossary 정본으로 통일. Lesson 후보.
- ARCHITECTURE 모순 정의: 정의가 ARCHITECTURE.md 0.2와 어긋난다. 대응 — INV-1에 따라 정의를 만들지 않고 §9에 보고. Lesson 후보.
- 범위 혼동: Layer 의미와 Component 의미를 혼용한다(예: Workflow). 대응 — §3.2 Disambiguation에 따라 범위 명시.
- Layer/Cross-cutting 오분류: Memory를 Layer로 취급한다. 대응 — INV-2, §3.2-B 판정 기준으로 교정. Lesson 후보.

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

- 임의의 v0.1 spec을 열어, 참조된 모든 용어가 Glossary §3.2에 정의되어 있음을 대조로 보인다.
- Memory와 Lessons가 Layer 목록(§3.2-A)에 없고 Cross-cutting Service(§3.2-C)로 분류되어 있음을 보인다.
- Layer 6개, Cross-cutting Service 1개, Core Component 13개, Agent 역할 4개, Lifecycle 7단계가 각각 정확히 그 수만큼 정의되어 있음을 센다.
- 각 Component 정의가 담당 spec 파일 경로를 가짐을 보인다.
- Layer vs Cross-cutting 판정 기준(§3.2-B)을 Memory에 적용하면 Cross-cutting Service로 판정됨을 시연한다.

## 검증 방법

- Verifier가 각 spec의 용어 목록을 추출해 Glossary §3.2와 diff 한다. 미정의 용어가 0건이어야 한다.
- Verifier가 개수(6/1/13/4/7)를 센다.
- Verifier가 각 정의를 ARCHITECTURE.md 0.2와 대조해 모순 0건을 확인한다 (INV-1).
- Verifier가 §3에 Claude 의존 요소가 0건임을 확인한다 (INV-6, DoD-3).

---

# §8. Examples

**예 1 — 용어 조회**
specs/07-workflow.md가 "회수 정책"을 참조한다.
→ Glossary §3.2-C에서 "회수 정책 (Recall Policy)"의 정본 정의를 얻는다: 필요할 때만, 목적을 명시하고, 최소 범위로 읽는다.
→ Workflow spec은 이 정의를 새로 만들지 않고 참조만 한다.

**예 2 — Layer vs Cross-cutting 판정**
질문: Memory는 Layer인가 Cross-cutting Service인가?
→ §3.2-B 판정 기준 적용.
  1. 소비자가 여러 Layer에 걸치는가? 예 (Agent, Loop, Workflow, Verifier가 모두 접근).
  2. 모든 Lifecycle 사이클에서 사용되는가? 예 (매 사이클 Memory Update 단계 등).
  3. 스택의 특정 위치에 고정되지 않는가? 예.
→ 세 조건 모두 만족 → Cross-cutting Service. ARCHITECTURE.md 5.1과 일치.

---

# §9. Open Questions

Advisor 결정 기록. OQ1~OQ6 전 항목이 해소되었다 (OQ5·OQ6은 Wave 3~4에서 이행 완료).

- **OQ1: Core Layer와 Runtime Layer의 책임 분담** — 해소(결정(Advisor): Runtime Layer = 실행·수명주기·config를 관장하는 실행 환경 / Core Layer = AI 비의존 계약과 모듈 시스템의 근간. 정밀 경계는 specs/01-runtime.md §2·§3이 상세화하되 이 정의와 모순될 수 없다 · 상세 = git 앵커 90ca19c).

- **OQ2: Loop Engine의 계층 귀속** — 해소(결정(Advisor): Loop는 Runtime Layer에서 구동된다 — Lifecycle의 실행·반복은 실행 환경의 책임. 상세는 specs/03-loop.md가 정의한다).

- **OQ3: Layer 책임 정의의 근거** — 해소(결정(Advisor): ROADMAP v0.1의 승인된 산출물 정의에 따라 본 Glossary가 Layer 책임 정의의 정본이다. ARCHITECTURE.md 반영은 별도 제안으로 사용자 승인 대기 중이며, 반영 전까지 두 문서는 모순 없이 공존한다(ARCHITECTURE = 스택 순서, Glossary = 책임 정의)).

- **OQ4: Planner 역할 경계** — 해소(결정(Advisor): Planner는 Advisor로부터 위임받아 구현 계획·작업 분해의 초안을 작성하는 보조 역할이며, 계획의 채택·승인과 Architecture 결정은 Advisor 소관이다. AGENT.md Delegation에 Planner 항목 추가는 상위 규약 변경이므로 사용자 승인 대상 제안으로 이관되었고 — AGENT.md §Delegation·§Roles에 Planner 반영 확인(2026-07-26 실측 · `uaf-verified: .claude/AGENT.md §Delegation·§Roles & Boundaries 직접 대조`)).

- **OQ5: specs/12-scaffold.md·specs/13-harness.md 미작성** — 해소(두 파일이 작성·검증 완료되어 §2 dependents가 실재와 일치한다. 두 spec은 현재 Frozen 확정 상태다).

- **OQ6: 전체 Component→Layer 매핑 정본화** — 해소(결정(Advisor): 정본 매핑표는 Glossary가 소유한다. 각 spec §2 Position 선언을 대조 검증한 매핑표가 §3.2-D에 추가되어 이행 완료).

---

# Revision History

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

