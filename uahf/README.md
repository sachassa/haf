# Universal Agentic Harness Framework (UAHF)

## Overview

UAHF is the harness-execution Layer of the **Universal Agentic Framework
(UAF)** — this repository's top-level framework, organized into six Layers
(`entry`, `discovery`, `planning`, `orchestration`, `knowledge`, `uahf`). It is
the implementation that lives in the `uahf/` Layer; the vision below is that
harness Layer's vision.

Universal Agentic Harness Framework (UAHF) is a reusable, AI-agnostic
Development Operating System for AI agents. Rather than a bundle of settings for
one AI tool, it defines the contracts, roles, and loops that let an agentic
project **design, implement, verify, and learn on repeat** — staying stable as a
project grows and getting smarter over time by learning from its own failures.
Its core is deliberately independent of any specific AI model or execution
environment: support for a new AI is added by writing an Adapter, not by
rewriting the framework.

**Key characteristics**

- **AI Agnostic** — the Core carries zero AI-specific dependencies; all
  environment bindings live behind the Adapter Layer.
- **Six design principles** — AI Agnostic, Modular, Agent First, Verify
  Everything, Learn from Failure, Token Efficiency (`ARCHITECTURE.md` §3).
- **Agent roles** — Advisor, Planner, Worker, Verifier, coordinated by a
  delegate → implement → verify → approve core loop.
- **Frozen specification baseline** — 15 spec documents under `specs/` define the
  Core Contracts.

**Where to go next**

- New to the project? Read `docs/getting-started.md`.
- Operating UAHF? Read `docs/v1.0-user-guide.md`.
- Design authority: `ARCHITECTURE.md`. Version plan: `ROADMAP.md`. Contracts:
  `specs/`.

---

## 소개

UAHF(Universal Agentic Harness Framework)는 AI 에이전트를 위한 범용 Development
Operating System이다. 특정 AI 모델이나 개발 환경에 종속되지 않는, 재사용 가능한
Agentic Development Framework를 목표로 한다 (ARCHITECTURE.md §1 Vision).

UAHF는 UAF(Universal Agentic Framework — 이 저장소의 최상위 프레임워크, 6 Layer:
entry/discovery/planning/orchestration/knowledge/uahf)의 `uahf/` 하네스 실행 Layer
구현체이며, 위 서술은 이 하네스 Layer의 비전이다. 리포 전체 구조의 정본은 리포
루트 ARCHITECTURE.md다.

"설계 → 구현 → 검증 → 학습"이 자동으로 반복되며, 프로젝트가 커질수록 안정적으로
동작하고 실패를 학습해 시간이 지날수록 더 똑똑해지는 것을 지향한다
(ARCHITECTURE.md §2 Mission).

설계 원칙 6종 (ARCHITECTURE.md §3):

- **AI Agnostic** — 특정 AI 모델에 종속되지 않는다. 새 AI는 Adapter만 추가하면 된다.
- **Modular** — 모든 기능은 독립 모듈이며 교체 가능하다.
- **Agent First** — 모든 작업은 명확한 책임을 가진 Agent 중심으로 수행한다.
- **Verify Everything** — 검증되지 않은 결과는 완료가 아니다.
- **Learn from Failure** — 실패를 기록·분석해 교훈을 만들고 다음 작업에서 활용한다.
- **Token Efficiency** — 항상 최소한의 Context만 사용한다.

Core는 AI 비의존을 유지하고, 환경 의존 요소는 Adapter Layer 뒤로 격리한다
(ARCHITECTURE.md §3.1 AI Agnostic, §5). 정본은 ARCHITECTURE.md다.

---

## uahf/ Layer 내부 구조

`uahf/` Layer(UAHF 하네스 구현체)의 내부는 네 자리로 나뉜다. 아래는 `uahf/` 내부
지도이며, 리포 전체 구조의 정본은 리포 최상위 `ARCHITECTURE.md`(루트)다. `framework/`
내부 경계의 정본 트리는 `framework/core/structure.md` §8이다 (structure.md §2·§8 정합).

| 자리 | 무엇이 있는가 | 정본 포인터 |
|---|---|---|
| `specs/` | Core Contract 스펙 — Frozen 기준선. `00-glossary.md`(용어 정본)부터 `13-harness.md`까지 번호 스펙 14개 + `TEMPLATE.md` = **15개**. 계약의 최종 정본. | specs/00-glossary.md · 각 spec |
| `framework/` | 4경계: `core/`(계약·스키마 문서)·`runtime/`(모듈 시스템·수명주기 문서)·Module 구현 디렉터리(`loop`·`memory`·`verifier`·`workflow`·`plugins/`)·`adapters/<adapter>/`(환경 의존 바인딩 격리). | framework/core/structure.md §8 (정본 트리) |
| `docs/` | 운용 문서 — 검증 리포트·시연 기록·프로토콜·정책·가이드. 세션 진입 최신 상태 포인터는 리포 루트 `docs/next-session-prompt.md`. | docs/next-session-prompt.md(리포 루트) 등 |
| `.claude/` | uahf/ 로컬 override 설정 표면 — 현재 override 없음(v1.2.1 스텁, `uahf/.claude/README.md`뿐). Agent 정의(`agents/` 4종)·상위 규약(`AGENT.md`)·Advisor 진입점(`CLAUDE.md`)·확장 표면(`commands`·`hooks`·`skills/`) 실물은 리포 루트 `.claude/`(Global Default). 환경 의존(Adapter 경계). | 리포 루트 .claude/AGENT.md · specs/11-adapters.md |

- Core 경계(`framework/core`·`framework/runtime`)와 Module 구현 디렉터리의 문서
  본문은 특정 AI·언어·툴체인 토큰 0건을 유지하고, 환경 의존 토큰은
  `framework/adapters/`와 `.claude/`로 격리된다 (structure.md §5, ARCHITECTURE §3.1).

---

## 시작하기

UAHF를 처음 접했거나 새 세션을 시작한다면 아래 문서를 따른다. 이 절은 경로만
안내하며 절차를 재서술하지 않는다.

- **신규 참여자·세션 진입:** `docs/getting-started.md` — 프로젝트 소개·구조 지도·세션
  진입 절차의 진입점.
- **신규 프로젝트에 UAHF 설치:** `docs/v0.9-install-guide.md` — Install →
  VerifyInstall → Bootstrap → Loop 1 사이클 절차. 설치 계약 정본은
  `specs/12-scaffold.md`.
- **운용 안내(설치·위임·검증·Memory·이식):** `docs/v1.0-user-guide.md`.
- **빠른 상태 확인:** `.claude/commands/uahf-status.md` — 현재 마일스톤·최신
  핸드오프·하네스 상태·다음 진입 절차 표면화.

---

## Adapter 이식 개요

UAHF는 AI Agnostic Architecture다. Core Contract는 유지한 채, 다른 AI·실행
환경으로의 **이식은 Adapter Layer만 교체**하는 것으로 이뤄진다 (ARCHITECTURE §3.1,
specs/11-adapters.md §4.2).

Adapter는 두 등급을 갖는다 (specs/11-adapters.md §3.2-B):

- **완전 Adapter (Full Adapter)** — 필수 바인딩 전부 + 선택 바인딩까지 제공.
- **최소 구현 Adapter (Minimal Adapter)** — 필수 바인딩(최소 부분집합 13개)만 제공하고
  선택 바인딩은 생략할 수 있다. Adapter Interface가 다른 AI에도 적용 가능함을
  증명하기 위한 최소 구현이다.

현재 두 Adapter 경계가 실재한다:

- `framework/adapters/claude/` — 첫 번째 Adapter. 선택 바인딩까지 포함하는 완전 구현을
  목표로 한다 (specs/11 §4.1).
- `framework/adapters/generic/` — 두 번째 Adapter. 환경 중립 최소 구현(최소 바인딩
  부분집합).

각 Adapter의 **적합성 판정(Conformance verdict)**과 핵심 루프 통과 근거는 이 문서가
선취하지 않는다. 판정은 각 Adapter 경계의 Conformance 문서
(`framework/adapters/<adapter>/adapter-conformance.md`)와 해당 검증
리포트(`docs/`)를 정본으로 참조한다.

---

## 문서 역할 구분

README·getting-started·user-guide는 역할이 다르며 서로 중복 정의하지 않는다.

- **README.md** (이 문서) — 저장소 소개·지도. 프로젝트가 무엇이고 어디에 무엇이
  있는지 가리킨다.
- **docs/getting-started.md** — 신규 참여자 세션 진입. 처음 참여하는 사람이 세션을
  시작하는 절차를 안내한다.
- **docs/v1.0-user-guide.md** — 운용 안내. 설치·위임·검증·Memory·이식의 운용을 정본 §
  포인터로 엮는다.

세 문서 모두 정본을 재정의하지 않는다. 계약·구조·절차의 정본은 각 포인터가 가리키는
문서(ARCHITECTURE·ROADMAP·specs·framework/core/structure.md)다. 충돌을 발견하면
Advisor에게 보고한다 (CLAUDE.md — Architecture·Spec 충돌 시 사용자 보고).

---

## 정본 포인터

| 주제 | 정본 |
|---|---|
| 비전·설계 원칙·아키텍처 | ARCHITECTURE.md |
| 개발 단계·버전·산출물 | ROADMAP.md |
| Core Contract 스펙 (15개) | specs/ (00-glossary ~ 13-harness + TEMPLATE.md) |
| framework 디렉터리 구조 | framework/core/structure.md §8 |
| 위임·보고 운용 프로토콜 | docs/delegation-protocol.md |
| 검증 체크리스트(게이트 A~D) | docs/verification-checklist.md |
| 역할 빠른 참조(Advisor·Planner·Worker·Verifier) | docs/roles-quick-reference.md |
| 세션 진입·직전 상태 | docs/next-session-prompt.md(리포 루트) |
| 신규 프로젝트 설치 | docs/v0.9-install-guide.md · specs/12-scaffold.md |
| 용어 정본 | specs/00-glossary.md |
| 상위 규약 | .claude/AGENT.md |

---

이 문서는 **v1.0 기준**이다. 세션 진입 최신 상태는 리포 루트 `docs/next-session-prompt.md`를
따른다.
