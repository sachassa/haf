# UAHF Development Roadmap

Version: v0.1 → v1.2

Status: Approved Baseline (v0.1 → v1.2)

---

# 1. Purpose

이 문서는 Universal Agentic Harness Framework(UAHF)의
개발 단계를 정의한다.

ROADMAP은 ARCHITECTURE.md를 최우선 기준으로 따른다.

모든 버전은 Worker(Opus)가 병렬로 개발하기 쉬운 형태로 분해되어 있다.

---

# 2. Roadmap Principles

## 2.1 Spec First

구현 전에 스펙을 동결한다.

v0.1이 전체 로드맵의 기반이다.

스펙이 없는 컴포넌트는 구현하지 않는다.

## 2.2 Interface Contract First

각 버전은 인터페이스 계약을 먼저 확정한다.

계약이 확정된 작업 단위는 Worker가 서로 간섭 없이 병렬 개발할 수 있다.

## 2.3 Core–Adapter 분리

v0.x 전반은 Claude Code를 적극 활용한다.

단, 모든 산출물은 다음 두 가지를 반드시 구분해서 작성한다.

- UAHF Core 계약 (AI 비의존)
- Claude Adapter 바인딩 (Claude 의존)

다른 LLM 환경으로 이식할 때 Adapter만 교체하면 되도록
계층을 유지한다.

---

# 3. Version Overview

| 버전 | 이름 | 핵심 내용 | 병렬성 |
|---|---|---|---|
| v0.1 | Specification Baseline | 13개 컴포넌트 스펙 동결 | 높음 |
| v0.2 | Agent Harness Bootstrap | Agent 4종 정의, self-hosting 시작 | 높음 |
| v0.3 | Runtime & Core Kernel | 모듈 시스템, config, 수명주기 | 중간 |
| v0.4 | Memory & Lessons (Track A) | 기억과 교훈의 기록/회수 | 높음 |
| v0.5 | Verifier (Track B) | 검증 엔진, 완료 판정 | 중간 |
| v0.6 | Loop Engine | Agent Lifecycle 루프 자동화 (통합점) | 낮음 |
| v0.7 | Workflow & Parallel Orchestration (Track C) | 작업 분해, 병렬 디스패치, 병합 | 중간 |
| v0.8 | Extension System (Track D) | Hooks, Skills, Plugins | 높음 |
| v0.9 | Adapter Layer & Scaffold | Claude Adapter 정식화, Scaffold, Presentation | 높음 |
| v1.0 | Architecture Validation & Release | 2nd Adapter 최소 구현, Dogfooding, 문서화 | 높음 |
| v1.1 | Project Discovery & Entry Layer | UAF Entry Architecture 설계 — 신규 uaf/ 경계(Entry Layer·Entry Resolution·Project Discovery·Project Contract), Architecture 설계만(구현 0), UAHF 정본 무수정 | 중간 |
| v1.2 | Project Discovery Implementation | uaf/ 정본 4문서 §4 바인딩 지점 11건을 Claude Adapter 경계에 형태 A로 물리화(바인딩 3 + 진입 명령 2), Greenfield/Brownfield 두 경로 E2E 실동작 검증(검증 중점 5건), UAHF 정본 명시 3건 한정 개정·실행 코드 0 | 중간 |
| v1.3 | Solution Design (Contract Maturation) | Discovery~UAHF 사이 성숙 활동(Solution Design)의 아키텍처 정본 확립 — `planning/specs/04-solution-design.md` 신설(단계 계약·복잡도 게이트·Expert Role 개방 네임스페이스·협업 프로토콜 골격·SP-INV 1~8), 03 v1.2(생산자 2경로·Maturation 갱신 유형), 루트 ARCHITECTURE 문서버전 v1.4(6요소 유지·성숙 루프·§12 용어 4건), planning ARCH 이중 책임, 비정본 부록 2종. Architecture 설계만(형태 A·실행 코드 0)·UAHF 정본 무수정 — Adapter 바인딩·dogfooding E2E는 v1.4 | 중간 |

> 버전 네임스페이스 주의 — 표의 v1.3은 **마일스톤 버전**이다. 루트 `ARCHITECTURE.md`의 **문서 버전 v1.3**(2026-07-09 라우터 재저술)과는 별개 네임스페이스이며, 마일스톤 v1.3에서 루트 문서 버전은 v1.4로 상승했다(설계 정본 = `docs/v1.3-context-and-design.md`).

---

# 4. Parallel Track Map

버전 번호는 릴리스 순서를 의미한다.

착수 순서는 아래 의존 관계를 따르며,
중괄호 안의 트랙은 서로 독립적으로 병렬 진행할 수 있다.

```
v0.1 → v0.2 → v0.3 → { v0.4 ∥ v0.5 ∥ v0.8(착수) } → v0.6 → { v0.7 ∥ v0.8(완료) } → v0.9 → v1.0 → v1.1 → v1.2
```

- Track A (v0.4 Memory & Lessons)와 Track B (v0.5 Verifier)는 상호 독립이다.
- Track D (v0.8 Extension System)는 선행 조건이 v0.3뿐이므로 v0.4 시점부터 조기 착수할 수 있다. 릴리스 정렬만 v0.6 이후로 한다.
- v0.6 Loop Engine은 Track A와 Track B를 통합하는 지점이므로 병렬화하지 않는다.
- v1.1 (Project Discovery & Entry Layer)은 단일 트랙이다 — UAHF 컴포넌트 트랙이 아니라 그 상위의 UAF 레벨 신설이므로, 기존 v0.x~v1.0 컴포넌트 트랙과 병렬 관계를 갖지 않고 v1.0 완료 이후 직렬로 이어진다.
- v1.2 (Project Discovery Implementation)은 v1.1의 직렬 후행 트랙이다 — v1.1이 설계한 UAF Entry Architecture를 Claude Adapter 경계에 물리화·실동작 검증하는 구현/검증 트랙이므로, 다른 트랙과 병렬 관계를 갖지 않고 v1.1 완료 이후 직렬로 이어진다.

---

# 5. Version Details

---

## v0.1 — Specification Baseline

### 목표

13개 Core Component 전체의 스펙을 확정하고 동결한다.

모든 스펙에 Core 계약과 Adapter 구현의 경계를 정의한다.

이후 모든 버전이 이 스펙을 기준으로 개발된다.

### 선행 조건

- ARCHITECTURE.md v0.1 승인 (완료)

### 완료 조건

- 모든 스펙이 다음 항목을 포함한다.
  - 목적
  - 인터페이스 (입력 / 출력)
  - 데이터 포맷
  - Core 계약 vs Adapter 구현 경계
  - 완료 기준 (검증 가능한 형태)
- 스펙 간 상호 참조에 누락과 모순이 없다.
- Advisor 검증을 통과한다.

### 산출물

- specs/00-glossary.md — 용어집, Layer 및 Cross-cutting Service 책임 정의 (승인됨)
- 스펙 공통 템플릿
- specs/01-runtime.md ~ specs/11-adapters.md (11개 완성)
- specs/12-scaffold.md, specs/13-harness.md (승인됨: 스펙 커버리지 갭 해소)

### 병렬 작업 가능 여부

높음.

- 1단계 (직렬, Worker 1): 용어집 + 스펙 템플릿 작성
- 2단계 (직렬, Worker 1~2): 01-runtime, 02-agent — 나머지 스펙이 참조하는 공통 기반이므로 우선 작성
- 3단계 (병렬, Worker N): 나머지 스펙을 스펙 단위로 병렬 작성

---

## v0.2 — Agent Harness Bootstrap

### 목표

UAHF가 스스로를 개발할 최소 하네스를 구축한다 (self-hosting 시작).

Advisor, Planner, Worker, Verifier 4종 Agent를 정의하고
위임과 보고의 프로토콜을 확정한다.

### 선행 조건

- v0.1 (특히 specs/02-agent.md)

### 완료 조건

- 4개 Agent 정의가 specs/02-agent.md와 AGENT.md를 준수한다.
- 위임 → 구현 → 검증 → 승인 사이클을 실제로 1회 이상 시연한다.
- 각 Agent의 입력, 출력, 완료 조건, 실패 보고 포맷이 정의되어 있다.

### 산출물

- .claude/agents/advisor.md
- .claude/agents/planner.md
- .claude/agents/worker.md
- .claude/agents/verifier.md
- 위임/보고 프로토콜 문서
- Advisor용 검증 체크리스트

### 병렬 작업 가능 여부

높음.

공통 규약(AGENT.md 정합화)을 먼저 확정한 뒤,
Agent 4종을 각각 별도 Worker가 병렬 작성한다.

---

## v0.3 — Runtime & Core Kernel

### 목표

Core Layer와 Runtime Layer의 골격을 구축한다.

모듈 시스템, 설정(config), 수명주기를 정의하고
Core 규격(Claude 비의존)과 Claude 바인딩을 물리적으로 분리한다.

### 선행 조건

- v0.1 (specs/01-runtime.md)
- v0.2 (작업을 수행할 하네스)

### 완료 조건

- 모듈을 단독으로 사용하거나 교체할 수 있음을 시연한다 (Modular 원칙 검증).
- Core 디렉터리에 Claude 의존 요소가 없다.
- config 스키마가 스펙과 일치한다.
- Verifier 검증을 통과한다.

### 산출물

- Core 모듈 디렉터리 구조 (규격)
- Runtime 프로토콜 구현물
- config 스키마
- 모듈 등록/교체 규칙 문서

### 병렬 작업 가능 여부

중간.

모듈 경계 확정(직렬)이 끝나면 모듈 단위로 병렬 개발 가능.

---

## v0.4 — Memory & Lessons (Track A)

### 목표

Memory Service(Cross-cutting)를 구축한다.

모든 Layer가 Memory Service Interface(단일 Port)를 통해서만
Memory에 접근하는 구조를 만든다.

실패가 Lesson으로 기록되고,
다음 작업에서 자동으로 회수되는 학습 구조를 만든다.

Learn from Failure와 Token Efficiency 원칙을 구현한다.

### 선행 조건

- v0.3

### 완료 조건

- 실패 → Lesson 생성 → 다음 작업에서 회수 사이클을 시연한다 (Learn from Failure 검증).
- Memory는 필요한 경우에만 읽는다 — 회수 규칙이 최소 Context 원칙을 지킨다 (Token Efficiency 검증).
- 모든 Memory 접근이 Memory Service Interface를 경유한다 (Cross-cutting 계약 검증).
- Memory 포맷과 Lessons 포맷이 스펙과 일치한다.

### 산출물

- Memory Service Interface (단일 Port 계약)
- Memory store 구조와 포맷
- Lessons 포맷과 생성 규칙
- 기록/회수 프로토콜 (회수 정책 포함)
- Memory 인덱스 규격

### 병렬 작업 가능 여부

높음.

- Memory와 Lessons는 별도 Worker가 병렬 개발 가능
- v0.5 (Verifier)와 상호 독립 — 버전 전체가 병렬 트랙

---

## v0.5 — Verifier (Track B)

### 목표

검증 엔진을 구축한다.

Worker의 완료 보고를 그대로 신뢰하지 않고
독립적으로 판정하는 구조를 만든다.

Verify Everything 원칙을 구현한다.

### 선행 조건

- v0.3

### 완료 조건

- Worker 결과물에 대해 검증 리포트가 자동 생성된다.
- 거짓 완료 보고를 검출하는 케이스를 1개 이상 시연한다 (Verify Everything 검증).
- 완료 판정 기준이 스펙(specs/06-verifier.md)과 일치한다.

### 산출물

- Verifier 프로토콜 구현물
- 검증 리포트 스키마
- 완료 판정 기준 카탈로그
- 검증 실패 시 재작업 지시 포맷

### 병렬 작업 가능 여부

중간.

- v0.4와 상호 독립 — 버전 전체가 병렬 트랙
- 내부적으로는 리포트 스키마 확정 후 판정 기준 카탈로그를 병렬 작성 가능

---

## v0.6 — Loop Engine

### 목표

AGENT.md의 Agent Lifecycle

Consult → Plan → Execute → Verify → Learn → Memory Update → Complete

를 자동으로 반복하는 루프를 구축한다.

v0.4(Memory, Lessons)와 v0.5(Verifier)를 하나의 루프로 통합한다.

### 선행 조건

- v0.4
- v0.5

### 완료 조건

- 단일 작업이 사람 개입 최소로 전체 Lifecycle을 통과한다.
- 루프의 각 단계 전이가 기록으로 남는다.
- Verify 실패 시 재작업 루프가 동작한다.
- Learn 단계에서 Lesson이 실제로 생성된다.

### 산출물

- Loop 오케스트레이션 규격과 구현물
- 루프 상태 기록 포맷
- 단계 전이 규칙 문서

### 병렬 작업 가능 여부

낮음.

통합 마일스톤이다. Worker 1~2명이 담당한다.

이 기간에 Track D(v0.8)를 병렬 진행하여 전체 처리량을 유지한다.

---

## v0.7 — Workflow & Parallel Orchestration (Track C)

### 목표

Workflow Layer를 구축한다.

큰 작업을 분해하고,
여러 Worker에게 병렬로 디스패치하고,
결과를 병합·검증하는 구조를 만든다.

### 선행 조건

- v0.6

### 완료 조건

- 3개 이상의 작업이 병렬로 수행되고 각각 검증까지 완료되는 Workflow를 시연한다.
- 작업 분해 결과에 완료 조건과 인터페이스 계약이 포함된다.
- 병합 시 충돌 처리 규칙이 동작한다.

### 산출물

- Workflow 정의 포맷
- 작업 분해 규칙
- 병렬 디스패치 프로토콜
- 결과 병합/충돌 처리 규칙

### 병렬 작업 가능 여부

중간.

- v0.8과 병렬 트랙
- 내부적으로는 분해 규칙 / 디스패치 / 병합을 각각 병렬 개발 가능

---

## v0.8 — Extension System (Track D)

### 목표

확장 시스템 3종을 구축한다.

- Hooks: 이벤트 기반 확장점
- Skills: 재사용 가능한 작업 능력
- Plugins: 기능 묶음 배포 단위

Framework 본체 수정 없이 기능을 추가할 수 있게 한다.

### 선행 조건

- v0.3 (Runtime의 확장점)
- 착수는 v0.4 시점부터 가능. 릴리스 정렬만 v0.6 이후.

### 완료 조건

- Hook, Skill, Plugin을 각 1개씩 서드파티 형태로 추가만 하여 동작이 확장됨을 시연한다.
- 본체 코드/규격 수정 없이 확장이 완료된다.
- 각 규격이 스펙(08, 09, 10)과 일치한다.

### 산출물

- Hooks 규격 + 이벤트 카탈로그 + 레퍼런스 Hook 1개
- Skills 규격 + 레퍼런스 Skill 1개
- Plugins 규격 + 매니페스트 포맷 + 레퍼런스 Plugin 1개

### 병렬 작업 가능 여부

높음.

Hooks, Skills, Plugins는 상호 독립적인 서브시스템이다.

3개를 각각 별도 Worker가 완전 병렬로 개발한다.

---

## v0.9 — Adapter Layer & Scaffold

### 목표

Adapter Layer를 정식화한다.

v0.2~v0.8 동안 Claude에 직접 바인딩된 부분을 모두
Adapter 규격 뒤로 이동시킨다.

Scaffold(신규 프로젝트 부트스트랩)와
Presentation 최소 기능을 구축한다.

### 선행 조건

- v0.6 (필수)
- v0.7, v0.8 (완료 권장 — Adapter가 감싸야 할 표면이 확정됨)

### 완료 조건

- Adapter Interface가 최종 확정된다.
- Core에 Claude 의존 요소가 0건이다 (경계 검증).
- 새 프로젝트에 Scaffold로 UAHF를 설치하고 루프가 동작함을 시연한다.
- Spec versioning과 하위호환 규칙이 문서화된다 (제안 반영).

### 산출물

- adapters/claude/ — Claude Adapter 완성본
- Adapter Interface 최종 규격
- Scaffold 도구와 프로젝트 템플릿
- Presentation 최소 기능 (명령/문서 진입점)
- 신규 프로젝트 설치 가이드
- Spec versioning 정책 문서

### 병렬 작업 가능 여부

높음.

- Adapter 정식화 / Scaffold / Presentation은 3개 병렬 트랙
- Adapter Interface 확정(직렬)만 선행

---

## v1.0 — Architecture Validation & Release

### 목표

AI Agnostic Architecture를 실제로 증명한다.

Claude Adapter는 완전 구현을 유지하고,
두 번째 Adapter(OpenAI 또는 Generic)를 최소 구현하여
Adapter Interface가 다른 AI에도 적용 가능함을 검증한다.

두 번째 Adapter는 기능 완성이 아니라
Architecture Validation을 위한 최소 구현이면 충분하다.

Dogfooding과 문서화로 릴리스를 완성한다.

### 선행 조건

- v0.9

### 완료 조건

- 2nd Adapter로 핵심 루프가 1회 이상 통과한다 (AI Agnostic 실증).
- UAHF를 사용해 실제 프로젝트 1개를 개발 완료한다 (Dogfooding).
- 전체 스펙과 구현의 정합성 검증을 통과한다.
- Core의 Claude 의존이 0건으로 유지된다.
- README를 포함한 문서 세트가 완성된다.

### 산출물

- adapters/openai/ 또는 adapters/generic/ — 최소 구현
- Adapter 호환성 리포트
- Dogfooding 결과 보고서
- README.md 및 사용자 문서 세트
- v1.0 릴리스 노트

### 병렬 작업 가능 여부

높음.

- 2nd Adapter / 문서화 / Dogfooding은 3개 병렬 트랙
- 최종 정합성 검증만 직렬 (통합 판정)

---

## v1.1 — Project Discovery & Entry Layer

### 목표

Execution 이전의 공식 Entry Architecture를 UAF 레벨에 설계한다.

파이프라인 순서는 Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF다.

v1.1은 UAHF 6-Layer 컴포넌트 트랙이 아니라 그 상위의 UAF 레벨 신설 트랙이다 — 신규 최상위 경계 `uaf/`에 UAF 정본을 두며, UAHF 정본(ARCHITECTURE.md·specs·framework/·상위 규약)은 무수정으로 유지하고 접점은 Project Contract 하나뿐이다. 따라서 # 6 Principle Coverage·# 7 Component Coverage(13개 UAHF Core Component 배정)에는 v1.1 행이 추가되지 않는다.

v1.1은 Architecture 설계만 수행한다(구현 0).

### 선행 조건

- v1.0 (완료)

### 완료 조건

승인 계획 §검증의 9건을 요약한다.

1. 채택 범위 전 항목이 `uaf/` 정본에 정의된다.
2. 사용자 고정 원칙 5건(P1 Entry=Resolution만·P2 Discovery=Compiler·P3 Stable Contract·P4 책임 경계·P5 설계 순서)이 정본 문면으로 존재한다.
3. Project Contract 스키마 본문에 Discovery 내부 개념(질문·전략·예산) 역참조가 0건이다.
4. Entry Resolution 결정 테이블이 전 입력 조합에 단일 결과를 낸다(결정성 — 전수 열거 검증).
5. UAHF 정본 무수정 — 명시 개정 대상은 이 ROADMAP뿐이다.
6. 시나리오 워크스루 3건이 통과한다(Greenfield 진입·Brownfield 최초 도입·확장 진입 워크스루).
7. 사용자 확인 3건(Entry Descriptor 등록 모델·Contract 버저닝 규율·Execution Ready 2축 판정)이 정본 문면으로 존재한다.
8. `uaf/` 정본 본문이 Core 문서 관행과 동형이다 — 특정 AI·모델·제품 기능명 0건.
9. 전 산출물이 관행 규격(상태 라인·이력 절·§ 포인터)을 보유한다.

### 산출물

- ARCHITECTURE.md
- entry/specs/01-entry.md
- discovery/specs/02-discovery.md
- planning/specs/03-project-contract.md
- planning/docs/appendix/methodology-mapping.md
- docs/v1.1-scenario-walkthrough.md
- docs/v1.1-verification-report.md
- docs/v1.1-promotion-review.md
- docs/session-handoff-v1.1.md
- ROADMAP 개정

---

## v1.2 — Project Discovery Implementation

### 목표

v1.1이 UAF 레벨에 설계한 Entry Architecture를 Claude Adapter 경계에 물리화하고, 실입력으로 완주해 실동작을 검증한다.

uaf/ 정본 4문서의 §4 바인딩 지점 11건을 Claude Adapter 경계에 형태 A(문서 바인딩·실행 코드 0)로 물리화하고(바인딩 3문서 + 진입 명령 2), Greenfield `/new`·Brownfield `/continue` 두 경로를 실입력으로 완주해 검증 중점 5건(① Entry Resolution 실동작 ② Discovery→Contract ③ Contract→UAHF ④ Greenfield/Brownfield ⑤ Compiler E2E)을 실동작 검증한다.

v1.2는 v1.1 설계를 구현·검증하는 UAF 레벨 실현 트랙이다 — 산출물이 Claude Adapter 경계에 놓이고, UAHF 정본은 명시 3건에 한정해 개정하며 실행 코드는 생성하지 않는다(형태 A 유지). v1.2는 UAF 레벨 실현 트랙(Adapter 경계 산출물)이지 UAHF Core Component 트랙이 아니므로, # 6 Principle Coverage·# 7 Component Coverage(13개 UAHF Core Component 배정)에는 v1.2 행이 추가되지 않는다 — v1.1 선례 동형.

### 선행 조건

- v1.1 (완료)

### 완료 조건

승인 계획 §완료 조건(시연 가능 문장 10)의 10건이다.

1. uaf/ §4 바인딩 지점 11건(01 불릿3 + 02 표4행·Module부 + 03 표4행) 전부 형태 A 바인딩 문서로 물리화 — 각 표에 실재/규약/형태 B 3구분.
2. 진입 명령 2건이 uahf-status 선례 동형으로 실재.
3. Greenfield /new: 실 Evidence 관측(행 1)→State Machine 완주(실 Event 로그)→실 값 Contract(코어 필드 전건)→2축 판정 Ready 완주.
4. Brownfield /continue: 본 저장소 실 증거 스캔(T2)→최초 Contract(instanceVersion 1·supersedes 없음) 생성 완주(dogfooding).
5. 산출 Contract가 UAHF 선택 입력으로 실소비 — Advisor Consult 정독 + Scaffold 배치, UAHF 정본 무수정.
6. 검증 중점 5건 각각 최소 1개 Task done으로 시연.
7. 사용자 게이트 2건(G1 실 Q&A·G2 Ready 승인)이 실 사용자와 수행·Event 로그 기록.
8. 상시 불변 2건 매 게이트 위반 0 — ① Discovery 내부 개념의 Contract 코어/UAHF 접점 누출 0 ② SemVer·tolerant reader·필드 제거 금지 훼손 0.
9. UAHF 정본 개정 = 명시 3건(ROADMAP·structure.md §8·adapter-conformance 계수) 한정·그 외 수정 0·실행 코드 0(형태 A 유지).
10. 전 산출물 관행 규격(상태 라인·§9 이력·§ 포인터 재정의 0) 보유.

### 산출물

신규:

- framework/adapters/claude/contract-binding.md (UAF 정본 바인딩)
- framework/adapters/claude/entry-binding.md (UAF 정본 바인딩)
- framework/adapters/claude/discovery-binding.md (UAF 정본 바인딩)
- .claude/commands/uaf-new.md (진입 명령)
- .claude/commands/uaf-continue.md (진입 명령)
- framework/adapters/claude/discovery-data/ (백엔드 격리 데이터 — Event 로그 2 run·Discovery Request 2·Policy 1·Contract 인스턴스 2: 본 저장소 pc-uahf-001·신규 프로젝트 pc-uahf-quickstart-001)

개정:

- ROADMAP.md
- framework/core/structure.md §8
- framework/adapters/claude/adapter-conformance.md 계수

프로토콜 산출물(예정):

- docs/v1.2-verification-report.md
- docs/v1.2-promotion-review.md
- docs/session-handoff-v1.2.md

---

# 6. Principle Coverage

ARCHITECTURE.md의 6개 설계 원칙은 다음 버전에서 검증된다.

| 원칙 | 검증 버전 |
|---|---|
| AI Agnostic | v1.0 (2nd Adapter로 실증) |
| Modular | v0.3 (모듈 단독 사용/교체 시연) |
| Agent First | v0.2 (Agent 위임 사이클 시연) |
| Verify Everything | v0.5 (거짓 완료 보고 검출) |
| Learn from Failure | v0.4 (실패 → Lesson → 회수 사이클) |
| Token Efficiency | v0.4 (최소 Context 회수 규칙) |

---

# 7. Component Coverage

13개 Core Component의 버전 배정.

| Component | 스펙 확정 | 구현/정식화 |
|---|---|---|
| Runtime | v0.1 | v0.3 |
| Agent | v0.1 | v0.2 |
| Loop | v0.1 | v0.6 |
| Memory | v0.1 | v0.4 |
| Lessons | v0.1 | v0.4 |
| Verifier | v0.1 | v0.5 |
| Workflow | v0.1 | v0.7 |
| Hooks | v0.1 | v0.8 |
| Skills | v0.1 | v0.8 |
| Plugins | v0.1 | v0.8 |
| Adapters | v0.1 | v0.9 → v1.0 |
| Scaffold | v0.1 (specs/12) | v0.9 |
| Harness | v0.1 (specs/13) | v0.2 (부트스트랩) → v0.9 (정식화) |

---

# 8. Revision History

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 이전 | v0.1 → v1.0 | Approved Baseline (소급 기록 — 본 이력 절 신설 이전의 기준선 확정) | Advisor |
| 2026-07-07 | v1.1 등재 Draft | v1.1(Project Discovery & Entry Layer) 트랙 등재 — 상태 라인·#3 표·#4 맵·#5 절 갱신·이력 절 신설. 사용자 승인 대기 | Worker (Advisor 위임, v1.1 W5 T8) |
| 2026-07-07 | v1.1 Baseline | v1.1 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass 15/0/0 · CP3 Advisor 승인). 상태 라인 승격 (Approved Baseline v0.1 → v1.1). | Advisor |
| 2026-07-07 | v1.2 등재 Draft | v1.2(Project Discovery Implementation) 트랙 등재 — 상태 라인·#3 표·#4 맵·#5 절 갱신·이력 절 append. 사용자 승인 대기 | Worker (Advisor 위임, Task T-R) |
| 2026-07-07 | v1.2 Baseline | v1.2 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass 16/0/0 · CP3 Advisor 승인). 상태 라인 승격 (Approved Baseline v0.1 → v1.2). | Advisor |

(이력 절은 문서 말미에 둔다 — 루트 ARCHITECTURE.md # 9 이력 관행 동형. 이후 개정은 이 표에 append-only로 기록한다.)
