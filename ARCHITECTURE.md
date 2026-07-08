# Universal Agentic Harness Framework (UAHF)

Version: 0.2 (Draft)

---

# 1. Vision

Universal Agentic Harness Framework (UAHF)는
AI 에이전트를 위한 범용 Development Operating System이다.

UAHF의 목표는 특정 AI 모델이나 특정 개발 환경에 종속되지 않는
재사용 가능한 Agentic Development Framework를 제공하는 것이다.

프로젝트 규모가 커질수록
더 안정적으로 동작하고,
실패를 학습하며,
시간이 지날수록 더 똑똑해지는 Framework를 목표로 한다.

UAHF는 단순한 Claude Code 설정 모음이 아니다.

UAHF는 AI 개발을 위한 Operating System이다.

---

# 2. Mission

UAHF는 다음 문제를 해결하기 위해 만들어진다.

- 프로젝트가 커질수록 컨텍스트가 무너지는 문제
- 반복되는 동일한 실수
- AI마다 다른 Workflow
- 검증 없는 구현
- 프로젝트별 중복 설정
- 사람이 계속 동일한 지시를 반복해야 하는 문제

UAHF는 이러한 문제를 해결하여

"설계 → 구현 → 검증 → 학습"

이 자동으로 반복되는 개발 환경을 제공한다.

---

# 3. Design Principles

UAHF는 다음 원칙을 따른다.

## 3.1 AI Agnostic

특정 AI 모델에 종속되지 않는다.

Claude는 첫 번째 Adapter일 뿐이다.

새로운 AI가 등장하면 Adapter만 추가하면 된다.

---

## 3.2 Modular

모든 기능은 독립적인 모듈이다.

필요한 모듈만 사용할 수 있다.

모든 모듈은 교체 가능해야 한다.

---

## 3.3 Agent First

모든 작업은 Agent 중심으로 수행한다.

각 Agent는 명확한 책임을 가진다.

---

## 3.4 Verify Everything

모든 구현은 검증되어야 한다.

검증되지 않은 결과는 완료가 아니다.

---

## 3.5 Learn from Failure

실패는 기록된다.

원인을 분석한다.

교훈을 생성한다.

다음 작업에서 활용한다.

같은 실수를 반복하지 않는다.

---

## 3.6 Token Efficiency

항상 최소한의 Context만 사용한다.

Memory는 필요한 경우에만 읽는다.

---

# 4. Core Philosophy

UAHF는

Prompt Engineering

↓

Context Engineering

↓

Harness Engineering

↓

Loop Engineering

↓

Memory Engineering

↓

Agentic Engineering

을 하나의 Framework로 통합한다.

---

# 5. High Level Architecture

UAHF는 6개의 Layer와
1개의 Cross-cutting Service로 구성된다.

Presentation Layer

↓

Workflow Layer

↓

Agent Layer

↓

Runtime Layer

↓

Core Layer

↓

Adapter Layer

각 Layer는 서로 독립적으로 동작한다.

---

## 5.1 Memory Service (Cross-cutting)

Memory는 Layer가 아니다.

Memory는 모든 Layer를 관통하는 Cross-cutting Service다.

Memory는 특정 계층만 사용하는 지층(stratum)이 아니라
모든 Agent가 Lifecycle의 매 사이클마다 사용하는 능력(capability)이기 때문이다.

Memory Service는 다음 원칙을 따른다.

- 접근 경로는 Memory Service Interface(단일 Port) 하나뿐이다.
- Agent, Loop, Workflow, Verifier는 이 Interface를 통해서만 Memory에 접근한다.
- 회수 정책은 계약에 내장된다. 필요할 때만, 목적을 명시하고, 최소 범위로 읽는다.
- 영속성 백엔드는 Adapter Layer 뒤에 위치한다. 환경 이식 시 Adapter만 교체한다.
- Lessons는 Memory Service 위의 특화 계약이다.

---

# 6. Core Components

UAHF는 다음 Core Component를 가진다.

- Scaffold
- Harness
- Workflow
- Agent
- Runtime
- Loop
- Memory
- Lessons
- Verifier
- Plugins
- Skills
- Hooks
- Adapters

Memory와 Lessons는
Layer 스택이 아닌 Cross-cutting Service로 동작한다.

모든 Component는 독립적으로 사용할 수 있으며

통합하면 하나의 Development Operating System이 된다.

---

# 7. Non Goals

UAHF는 다음을 목표로 하지 않는다.

- Claude 전용 Framework
- 특정 언어 전용 Framework
- 특정 IDE 전용 Framework
- 특정 회사 Workflow 강제

---

# 8. Future Direction

UAHF는 앞으로

- 새로운 AI 모델
- 새로운 IDE
- 새로운 Workflow
- 새로운 Memory
- 새로운 Runtime

을 Plugin 형태로 확장할 수 있도록 설계한다.

Framework는 시간이 지나도
전체를 다시 작성하지 않아야 한다.

새로운 기술은 Adapter 또는 Plugin만 추가하면 된다.

---

# 9. Revision History

- 0.1: 최초 Draft
- 0.2: Memory를 Layer에서 Cross-cutting Service로 재정의 (설계 검토 후 승인)
