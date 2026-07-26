# UAHF Development Roadmap

Version: v0.1 → v1.2

Status: Approved Baseline (v0.1 → v1.2)

---

# 1. Purpose

이 문서는 Universal Agentic Harness Framework(UAHF)의
개발 단계를 정의한다.

이 로드맵은 v1.2.1(uahf/ Layer 승격) 이후의 UAF 레벨 마일스톤(entry/orchestration
Layer 신설 등) 기록도 포함한다. UAF(리포 최상위 프레임워크) 로드맵의 정본은 리포 루트
`ROADMAP.md`다.

ROADMAP은 ARCHITECTURE.md를 최우선 기준으로 따른다.

모든 버전은 Worker(Opus)가 병렬로 개발하기 쉬운 형태로 분해되어 있다.

---

# 2. Roadmap Principles

## 2.1 Spec First

구현 전에 스펙을 동결한다. v0.1이 전체 로드맵의 기반이며, 스펙이 없는 컴포넌트는
구현하지 않는다.

## 2.2 Interface Contract First

각 버전은 인터페이스 계약을 먼저 확정한다. 계약이 확정된 작업 단위는 Worker가 서로
간섭 없이 병렬 개발할 수 있다.

## 2.3 Core–Adapter 분리

v0.x 전반은 Claude Code를 적극 활용한다. 단, 모든 산출물은 **UAHF Core 계약(AI
비의존)**과 **Claude Adapter 바인딩(Claude 의존)**을 반드시 구분해서 작성한다. 다른
LLM 환경으로 이식할 때 Adapter만 교체하면 되도록 계층을 유지한다.

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
| v1.1 | Project Discovery & Entry Layer | UAF Entry Architecture 설계 — 신규 `uaf/` 경계(Entry Layer·Entry Resolution·Project Discovery·Project Contract). Architecture 설계만(구현 0)·UAHF 정본 무수정 | 중간 |
| v1.2 | Project Discovery Implementation | uaf/ 정본 4문서 §4 바인딩 지점 11건을 Claude Adapter 경계에 형태 A로 물리화 + Greenfield/Brownfield 두 경로 E2E 실동작 검증. 실행 코드 0 | 중간 |
| v1.3 | Solution Design (Contract Maturation) | Discovery~UAHF 사이 성숙 활동의 아키텍처 정본 확립 — `planning/specs/04-solution-design.md` 신설(SP-INV·복잡도 게이트·Expert Role 개방 네임스페이스). 형태 A·실행 코드 0 | 중간 |
| v1.4 | Solution Design Binding & Dogfooding E2E | 04 §4.1 바인딩 4행 물리화(`solution-design-binding.md`+`solution-design-data/`) + pc-uahf-001 v1→v2 성숙 E2E 완주. 실행 코드 0 | 중간 |
| v1.5 | Form B Step Execution Hosting | 형태 B 실행 코드 첫 도입 — `framework/runtime/step-hosting-protocol.md`(provider-중립·SH-INV 8)·중립 Step Host·claude step-invoker + dogfooding E2E 7 시나리오 | 중간 |
| v1.6 | Project Orchestration / Dynamic Agent System | UAF 레벨 신규 최상위 Layer `orchestration/` 신설(루트 §2.3 slot 실현) — 정본 `orchestration/specs/05-project-orchestration.md`·중립 Orchestrator 6 모듈·Gate Policy 5종·claude 바인딩. UAHF 6-Layer 무촉 | 중간 |

> 각 버전의 완료일·산출물 목록·Δ·검증 판정 수치·run evidence 경로는 이 표에 옮기지 않는다 — 근거 = git 앵커 90ca19c.

> 버전 네임스페이스 주의 — 표의 v1.3은 **마일스톤 버전**이다. 루트 `ARCHITECTURE.md`의 **문서 버전 v1.3**(2026-07-09 라우터 재저술)과는 별개 네임스페이스이며, 마일스톤 v1.3에서 루트 문서 버전은 v1.4로 상승했다(설계 정본 = `docs/v1.3-context-and-design.md@cd9247b`).

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
- v1.1 이후는 UAHF 컴포넌트 트랙이 아니라 그 상위의 UAF 레벨 신설·실현 트랙이므로, 기존 v0.x~v1.0 컴포넌트 트랙과 병렬 관계를 갖지 않고 직렬로 이어진다.

---

# 5. Version Details

완료 마일스톤(v0.1~v1.2)의 버전별 상세 블록(목표·선행 조건·완료 조건·산출물·병렬 작업
가능 여부)은 이 문서에 두지 않는다 — # 3 개요표가 버전당 1행을 담고, 상세·산출물 경로는
**git 앵커 90ca19c**가 근거다.

이 절을 비운 부수 효과로, # 8 이력 2026-07-17 행이 자인한 broken 경로 위험(v1.1/v1.2
산출물 목록의 `docs/…` 경로가 실 위치 `uahf/docs/`와 불일치)은 소멸한다.

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
| 2026-07-17 | v1.2 (유지) | 동결 폐지 후 위계 자기서술 최소 정정 — # 1 Purpose 범위 문장에 UAF 레벨 마일스톤 포함·UAF 로드맵 정본=리포 루트 ROADMAP.md 병기. 마일스톤 이력·산출물 목록 무촉(append-only). 사용자 결정. | Worker (Advisor 위임) |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — #3 표 v1.5·v1.6 행의 삭제 run 경로 evidence 앵커 부기(`step-data/runs/@cd9247b`·`orchestration-data/runs/orch-j-e2e/@cd9247b`)·표 하단 주의 v1.3 설계 정본 포인터 앵커(`docs/v1.3-context-and-design.md@cd9247b`). v1.1/v1.2 #5 산출물 목록의 `docs/…` 경로는 실 위치(uahf/docs/) 불일치로 앵커 부기 시 broken 위험 → Advisor 판정 대기(무촉). 마일스톤 이력·계약 무변경(append-only). | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 5 — 비계약 격리 개정: 재서술·경위·완료 마일스톤 상세 압축(앵커 90ca19c), 원칙·불변·계약 문면 무변경 | Advisor 위임 |

(이력 절은 문서 말미에 둔다 — 루트 ARCHITECTURE.md # 9 이력 관행 동형. 이후 개정은 이 표에 append-only로 기록한다.)
