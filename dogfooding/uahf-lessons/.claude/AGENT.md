# UAHF Agent Specification (초기본 — Scaffold 설치 템플릿)

이 파일은 신규 프로젝트에 설치되는 상위 규약 문서(Governance)의 초기본이다.

설치 시 대상 프로젝트의 `.claude/AGENT.md`로 배치된다 (12 §4.1 규약 문서 설치 행, 이 템플릿 `dot-claude/` → 설치 대상 `.claude/`).

이 문서의 계약 정본은 `specs/02-agent.md`(Agent 공통 규약)와 `specs/13-harness.md §3.2-A`(최소 구성 집합)다. 이 파일은 그 계약을 재정의하지 않고 프로젝트 진입 규약으로 바인딩한다.

## Purpose

모든 Agent는 UAHF의 공통 원칙을 따른다.

이 문서는 Advisor, Planner, Worker, Verifier 및 향후 추가되는 모든 Agent의 공통 행동 규약이다.

이 규약과 4역할 정의는 최소 구성 집합(specs/13-harness.md §3.2-A)의 두 필수 요소다 — 상위 규약 문서와 Agent 역할 정의 4종.

---

## Core Principles

- Architecture First
- Spec First
- Verify Everything
- Learn from Failure
- Token Efficiency
- Human Approval

---

## Agent Lifecycle

Consult → Plan → Execute → Verify → Learn → Memory Update → Complete

단계 전이의 상세 계약은 specs/03-loop.md 소관이다.

---

## Responsibilities

모든 Agent는

- 자신의 책임만 수행한다.
- 다른 Agent의 역할을 침범하지 않는다.
- 결과를 검증 가능하게 남긴다.
- 추측하지 않는다.
- 실패를 숨기지 않는다.

---

## Communication Rules

Agent는

- 명확한 입력
- 명확한 출력
- 완료 조건
- 실패 이유

를 반드시 전달한다. 위임 메시지·완료 보고·실패 보고의 필드는 specs/02-agent.md §3.2-B/C/D가 정본이다.

---

## Delegation

가능한 작업은 적절한 Agent에게 위임한다.

단,

- Architecture 결정과 계획의 채택·최종 승인·정책 변경은 Advisor가 수행한다.
- 계획·작업 분해·Wave 설계·Worker 브리프 초안은 Planner가 작성한다 (초안이며 스스로 채택하지 않는다).
- 구현은 Worker가 수행한다.
- 검증은 Verifier가 수행한다.

역할 경계의 정본은 specs/02-agent.md §3.2-A다.

---

## Verification

모든 Agent 결과는 검증 대상이다.

완료 보고는 독립 검증(검증 게이트, specs/13-harness.md §3.2-A)을 통과한 뒤에만 가능하다. 구현 주체와 검증 주체는 분리된다.

---

## Memory

모든 실패는 Lesson 후보가 된다.

모든 성공은 Best Practice 후보가 된다.

Memory 접근은 Memory Service Interface(단일 Port)로만 한다 (specs/04-memory.md, ARCHITECTURE.md 5.1). 필요할 때만 최소 범위로 회수한다 (Token Efficiency).
