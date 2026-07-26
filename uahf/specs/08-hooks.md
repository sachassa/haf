# specs/08-hooks — Hooks Specification

Version: 0.2
Status: Frozen (v0.2 개정 — Event ID 안정성 항의 개정 기록 locus 를 git 으로 이전. 사용자 결정 2026-07-27)
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Hooks는 UAHF의 이벤트 기반 확장점이다 (Glossary §3.2-D).

Hooks는 하나의 문제를 해결한다.

- 본체를 수정하지 않고 특정 이벤트 시점에 동작을 덧붙일 표준 확장점이 없다는 문제.

Framework의 확정된 지점(전이·연산·메시지·Port 접근)에서 부수 동작을 실행할 표준 계약이 없으면, 확장은 매번 본체 코드·규격을 고쳐야 한다. Hooks는 이 확장을 "추가만으로" 가능하게 만든다.

## 책임 (1~3문장)

Hooks Component는 Framework 이벤트에 부수 동작을 바인딩하는 공통 계약을 정의한다.

이벤트 카탈로그(무엇에 걸 수 있는가), Hook 규격(어느 이벤트에·어느 phase에·무엇을 할 수 있고 없는가), 등록·순서·실패 처리, 그리고 Hook이 침범할 수 없는 경계를 검증 가능한 형태로 확정한다.

## Non-Goals

- Agent Lifecycle 단계의 정의·전이 규칙을 정의하지 않는다 — specs/03-loop.md 소관이다. Hooks는 전이 "이벤트"만 소비한다 (Glossary §3.2-F).
- 이벤트 원천의 연산·메시지 semantics를 정의하지 않는다 — 각 원천 spec(01, 02, 04)이 소유한다. Hooks는 관찰 가능한 표면만 카탈로그화한다.
- Skills(specs/09) · Plugins(specs/10)의 계약을 정의하지 않는다. 셋은 상호 독립 확장 서브시스템이다 (조율은 §9).
- 새 Module 등록 메커니즘을 정의하지 않는다 — Runtime의 Module 등록 계약(specs/01-runtime.md §3.1-A)을 확장점으로 그대로 사용한다.
- Verify 판정(specs/06-verifier.md), 역할 경계(specs/02-agent.md §3.2-A), Memory 내용·포맷(specs/04-memory.md)을 정의·변경하지 않는다.

---

# §2. Position

- 아키텍처 상 위치: Core Component "Hooks" (Glossary §3.2-D)의 규격 문서다. Layer도 Cross-cutting Service도 아니다. Hooks는 Runtime의 Module 등록 계약(01 §3.1-A) 위에 호스팅되는 확장 서브시스템으로 실현된다.
- Cross-cutting Service 아님: UAHF의 Cross-cutting Service는 Memory Service 하나뿐이다 (ARCHITECTURE.md 5.1, Glossary §3.2-B/INV-2). Hooks가 소비하는 이벤트는 여러 Layer에서 발생하지만, Hooks 자체는 Cross-cutting Service가 아니다.
- 확장점 근거: Hooks는 Runtime의 Module 등록/교체 계약을 확장점으로 사용한다. 이것이 ROADMAP v0.8의 선행 조건이 v0.3(Runtime)인 이유다 (01 §2 dependents, ROADMAP v0.8 선행 조건).

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 5(스택), 5.1(Memory 단일 Port), 6(Component 목록).
- specs/00-glossary.md (실재, Frozen) — 용어 정본. 특히 §3.2-D(Hooks), §3.2-F(Lifecycle 7단계), §3.2-I(Runtime 계약 용어).
- specs/TEMPLATE.md (실재, Frozen) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약. Hook은 역할 경계를 침범하지 않는다.
- ROADMAP.md v0.8 (실재) — Extension System 완료 조건과 산출물.
- specs/01-runtime.md (실재, Frozen) — Module 등록/교체 계약(§3.1-A), Runtime 연산(§3.1), 결정성(§3.3-INV-5). Hook 등록과 runtime 도메인 이벤트의 원천.
- specs/02-agent.md (실재, Frozen) — 위임/완료/실패 보고(§3.2-B/C/D), 역할 경계(§3.2-A). agent 도메인 이벤트의 원천이자 경계.

(상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·01·02·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`. 종전 "Review"·"Adopted" 표기는 작성 시점 기록이었다.)

## 이 spec에 의존하는 spec (dependents)

- 확정된 하드 의존은 없다. Hooks의 Core Contract(§3)는 어떤 확장 서브시스템에도 의존하지 않는다.
- specs/10-plugins.md — Plugin이 Hook을 번들해 배포할 수 있다. 이 경우 번들된 Hook의 등록도 본 spec의 Hook Binding·Runtime Module 등록 계약을 따른다. 배포 단위·매니페스트 소유는 10 소관이다. 상호 독립 원칙에 따라 하드 의존이 아닌 조율 항목으로 기록한다 (§9).
- specs/09-skills.md — Skills와 Hooks는 상호 독립이다. 겹치는 계약을 가정하지 않는다 (§9).

## 순환 의존

없다. Hooks는 01·02의 확정 계약을 소비하는 방향(08 → 01, 08 → 02)이며, 01·02는 Hooks에 의존하지 않는다. 01 §2는 이미 08-hooks를 "01의 Module 등록/교체 계약을 확장점으로 사용하는" dependent로 명시한다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 환경 의존 실현은 §4에 둔다.

Hooks는 네 가지 계약을 정의한다.

- 이벤트 카탈로그 계약 (§3.1-A, §3.2-A, §3.2-B)
- Hook 정의·능력 계약 (§3.1-B)
- 등록·Dispatch·순서 계약 (§3.1-C, §3.1-D, §3.2-D)
- 실패·격리 계약 (§3.1-E, §3.2-E)

---

## 3.1 Interface

### A. 이벤트 카탈로그 (Event Catalog)

Hook이 바인딩할 수 있는 대상은 카탈로그(§3.2-A)에 등재된 Event뿐이다.

- 입력: 없음 (카탈로그는 정적 선언이다).
- 출력: 바인딩 가능한 Event 목록과 각 Event의 가용 phase.
- 완료 조건: 카탈로그의 모든 Event가 확정된 원천 계약에서 도출되어 있다 (§3.2-A 근거 열, INV-6).
- 실패 보고: 카탈로그에 없는 Event에 바인딩 시도 시 등록이 거부된다 (§3.1-C, reason=`UnknownEvent`).

### B. Hook 정의와 능력 (Hook Definition & Capability)

Hook은 하나의 Event와 하나의 phase에 바인딩된 부수 동작(action)이다.

- 정의: Hook = (event, phase, action). event는 카탈로그(§3.2-A)에 존재해야 한다. phase ∈ {before, after}.
- 입력: 해당 (event, phase)의 Event Record(§3.2-C) — 읽기 전용.
- 출력: Hook Result — 성공 또는 Hook Failure Report(§3.2-E).

Hook이 **할 수 있는 것**:

- Event Record를 읽는다 (읽기 전용 투영).
- 자기 경계 안에서 부수 동작을 수행한다 (예: 로그·알림·감사 기록 생성, 파생 산출물 기록).
- Memory에 기록·회수가 필요하면 Memory Service Interface(단일 Port)만 사용한다 (§5, INV-7).

Hook이 **할 수 없는 것** (경계):

- 이벤트 원천의 입력·출력·상태를 변경한다 → 금지 (INV-3, read-only).
- 본 작업(이벤트 원천 연산)을 차단·veto·재정의한다 → v0.1 미지원 (INV-2, §9).
- 역할 경계(02 §3.2-A)를 행사·침범한다 → 금지 (INV-7).
- Verify 판정(06)을 대체·무효화한다 → 금지 (INV-7).
- Memory 단일 Port를 우회한다 → 금지 (INV-7).

### C. 등록 (Registration — Runtime Module 계약 재사용)

Hook의 등록은 Runtime의 Module 등록 계약(01 §3.1-A Register)만 사용한다. 새 등록 메커니즘을 만들지 않는다.

- 입력: Hook을 담은 Module 1건. 이 Module의 Manifest는 01 §3.2-A를 따르며, 자기완결적 경계(01 §3.2-E) 안에 Hook Binding(§3.2-D) 선언을 둔다.
- 출력: 등록 결과 — 공표된 Hook Binding 집합이 Hook Registry에 반영된다.
- 완료 조건: 각 Binding의 event가 카탈로그에 존재하고, phase가 유효하며, hookId가 유일하다. Module 자체는 01 Register 완료 조건을 만족한다.
- 실패 보고: reason = `UnknownEvent` | `InvalidPhase` | `DuplicateHookId`. Module 계약 위반은 01의 Register 실패 코드(`ContractMismatch` | `DuplicateId`)로 위임한다.
- 교체: Hook Module의 교체는 01 INV-1(동일 contract, 소비자 참조 불변)을 따른다. Hook 추가·교체·제거는 본체를 수정하지 않는다 (INV-1, INV-4).

### D. Dispatch와 실행 순서 (Dispatch & Ordering)

카탈로그 Event가 발생하면, 그 phase에 바인딩된 모든 Hook이 Hook Dispatch에 의해 순서대로 호출된다.

- 입력: 발생한 (event, phase)와 Event Record(§3.2-C).
- 출력: 각 Hook의 Hook Result 모음. 본 작업의 결과에는 영향을 주지 않는다 (INV-1, INV-2).
- 실행 순서: 같은 (event, phase)에 여러 Hook이 있으면 결정적 순서로 실행한다 (INV-5).
  - 1차 기준: `order` 오름차순 (작을수록 먼저).
  - 2차 기준(동률): Module 등록 순서.
  - 3차 기준(동률): hookId 사전순.
  - before·after 모두 동일 규칙을 적용한다. Hook은 비차단·격리(§3.1-E)이므로 순서는 부수 동작의 실행 순서에만 영향을 주고 본 작업 결과는 바꾸지 않는다.
- 완료 조건: 바인딩된 모든 Hook이 정확히 한 번 호출된다. 한 Hook의 실패가 다른 Hook 호출을 막지 않는다.

### E. 실패 처리 (Failure Handling — 비차단·격리)

Hook 실패는 본 작업을 차단하지 않는다.

- 각 Hook 호출은 격리된다. Hook이 오류·타임아웃으로 실패해도 Hook Failure Report(§3.2-E)를 남기고, 본 작업과 다른 Hook은 계속 진행된다 (INV-2).
- 본 작업(이벤트 원천 연산)의 성공·결과는 Hook 결과와 독립이다. Hook 추가·실패는 본체 동작을 바꾸지 않는다 (INV-1).
- 모든 Hook 실패는 Lesson 후보가 된다 (§6, §3.2-E lesson_candidate).
- blocking 값은 항상 false다 (INV-2). v0.1은 차단·veto Hook을 제공하지 않는다.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)은 Adapter Binding(§4)이 정한다.

### A. 이벤트 카탈로그 (Event Catalog)

Event ID는 `<domain>.<name>` 형식이다. domain은 소문자, name은 lowerCamelCase다. 카탈로그의 모든 Event는 확정된 원천 계약에서 도출된다 (INV-6). 모든 Event는 before·after 두 phase를 가진다.

| Event ID | Domain | 원천 (근거) | 설명 |
|---|---|---|---|
| `lifecycle.consult` | lifecycle | Glossary §3.2-F | Consult 단계 전이 |
| `lifecycle.plan` | lifecycle | Glossary §3.2-F | Plan 단계 전이 |
| `lifecycle.execute` | lifecycle | Glossary §3.2-F | Execute 단계 전이 |
| `lifecycle.verify` | lifecycle | Glossary §3.2-F | Verify 단계 전이 |
| `lifecycle.learn` | lifecycle | Glossary §3.2-F | Learn 단계 전이 |
| `lifecycle.memoryUpdate` | lifecycle | Glossary §3.2-F | Memory Update 단계 전이 |
| `lifecycle.complete` | lifecycle | Glossary §3.2-F | Complete 단계 전이 |
| `agent.delegation` | agent | 02 §3.2-B | 위임 메시지 발신·수신 지점 |
| `agent.completionReport` | agent | 02 §3.2-C | 완료 보고 생성 지점 |
| `agent.failureReport` | agent | 02 §3.2-D | 실패 보고 생성 지점 |
| `runtime.register` | runtime | 01 §3.1-A | Module Register 연산 |
| `runtime.resolve` | runtime | 01 §3.1-A | Module Resolve 연산 |
| `runtime.replace` | runtime | 01 §3.1-A | Module Replace 연산 |
| `runtime.loadConfig` | runtime | 01 §3.1-B | Load Config 연산 |
| `runtime.bootstrap` | runtime | 01 §3.1-C | Bootstrap 연산 |
| `runtime.shutdown` | runtime | 01 §3.1-C | Shutdown 연산 |
| `memory.recall` | memory | ARCHITECTURE 5.1, 02 §5 | 단일 Port 회수(읽기) 접근 |
| `memory.record` | memory | ARCHITECTURE 5.1, 02 §5 | 단일 Port 기록(쓰기) 접근 |

phase 의미:

- `before` — 원천 연산·전이·메시지 생성·Port 접근이 일어나기 직전.
- `after` — 그 직후.

lifecycle 도메인의 "전이" 이벤트는 단계 진입(before)·종료(after) 신호만 소비한다. 단계의 정의·전이 규칙은 specs/03-loop.md 소관이며 Hooks는 이름(Glossary §3.2-F)만 사용한다. 정확한 방출 경계는 03 조율 대상이다 (§9).

### B. 명명 규칙과 확장 (Naming & Extensibility)

- Event ID = `<domain>.<name>`. domain ∈ {lifecycle, agent, runtime, memory} (현재 4개). name은 원천 연산·전이·메시지 이름에서 도출한다.
- Event ID는 안정적(stable)이다. 한 번 공개된 Event ID의 변경·삭제는 spec 버전 상승과 **개정 기록**을 요구한다(기록 locus = git 커밋 — 운용 절차 정본 = `docs/spec-versioning-policy.md` §3).
- phase는 Event ID의 일부가 아니다. Hook이 바인딩 시점에 선택한다.

새 Event 추가 규칙 (카탈로그는 확장 가능하다):

1. 새 Event는 반드시 다른 spec의 **확정된 계약**(그 spec의 §3)에서 도출된 관찰 가능한 지점이어야 한다. 추측으로 추가하지 않는다 (INV-6, O4).
2. 원천 spec이 자신의 관찰 가능한 연산·전이·메시지·Port 접근을 확정하면, 그 spec과 조율하여 `<domain>.<name>`으로 카탈로그에 등재한다.
3. 새 domain은 새로운 이벤트 원천 계층·Component가 확정될 때만 추가한다. Glossary와 조율한다.
4. 추가는 Advisor 승인 후 반영한다. 기존 Event ID의 안정성을 깨지 않는다.

### C. Event Record

Hook에 전달되는 읽기 전용 입력이다.

| 필드 | 의미 |
|---|---|
| `eventId` | 카탈로그(§3.2-A)의 Event 식별자. |
| `phase` | `before` \| `after`. |
| `sourceRef` | 원천 연산·전이·메시지·Port 접근의 참조. 내용은 원천 spec이 소유한다. |
| `contextView` | 원천이 노출하는 읽기 전용 컨텍스트 투영. 상세 스키마는 원천 spec 소유(§9 조율). Hook은 읽기만 한다 (INV-3). |
| `occurredAt` | 발생 순서 기준(논리 시각). 직렬화는 §4. |

### D. Hook Binding

Hook을 (event, phase)에 연결하는 서술자다. Hook Module의 자기완결적 경계(01 §3.2-E) 안에 선언된다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `hookId` | Hook 고유 식별자. 안정적이어야 한다. | 예 |
| `event` | 바인딩 대상 Event ID. 카탈로그(§3.2-A)에 존재해야 한다. | 예 |
| `phase` | `before` \| `after`. | 예 |
| `order` | 실행 우선순위 정수(작을수록 먼저). 기본값 0. | 아니오(기본 0) |
| `action` | Hook 동작 진입점의 추상 참조. 구체 바인딩은 §4. | 예 |
| `replaceable` | 교체 가능 여부. 01 INV-1을 따른다. 기본 `true`. | 아니오(기본 true) |

### E. Hook Failure Report

Hook 실패의 공통 보고 구조다. 02 §3.2-D 실패 보고와 정합한다.

| 필드 | 의미 |
|---|---|
| `hookId` | 실패한 Hook 식별자. |
| `event` | 바인딩된 Event ID. |
| `phase` | `before` \| `after`. |
| `reason` | 사유 (Hook action 오류·타임아웃·경계 위반 등). |
| `blocking` | 항상 `false` (INV-2). 본 작업을 차단하지 않았음을 명시한다. |
| `lesson_candidate` | 여부와 한 줄 요약. 모든 Hook 실패는 Lesson 후보다 (§6). |

---

## 3.3 Invariants

- **INV-1 (본체 불가침 / non-invasive).** Hook의 추가·교체·제거·실패는 이벤트 원천(본체)의 코드·규격·판정 결과를 바꾸지 않는다. 본체는 Hook의 존재를 전제로 동작하지 않는다.
- **INV-2 (비차단·격리).** Hook 실패는 격리된다. 본 작업과 다른 Hook을 차단하지 않는다. blocking 값은 항상 false다. v0.1은 차단·veto Hook을 제공하지 않는다.
- **INV-3 (read-only context).** Hook은 Event Record를 읽기만 한다. 이벤트 원천의 입력·출력·상태를 변경하지 않는다.
- **INV-4 (Runtime 등록 재사용).** Hook 등록은 Runtime의 Module 등록 계약(01 §3.1-A)만 사용한다. 새 등록 메커니즘을 만들지 않는다. 교체는 01 INV-1을 따른다.
- **INV-5 (결정적 순서).** 같은 (event, phase)의 Hook 실행 순서는 결정적이다 (§3.1-D 규칙). 01 INV-5(결정성)의 정신과 정렬한다.
- **INV-6 (도출된 이벤트).** 카탈로그의 모든 Event는 확정된 spec 계약(Glossary §3.2-F, 01 §3.1, 02 §3.2, ARCHITECTURE 5.1 Port)에서 도출된다. 추측 이벤트는 없다.
- **INV-7 (경계 불가침).** Hook은 역할 경계(02 §3.2-A), Verify 판정(06), Memory 단일 Port(ARCHITECTURE 5.1)를 침범·우회하지 않는다. Memory 접근이 필요하면 Memory Service Interface(단일 Port)만 사용한다.
- **INV-8 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 환경 바인딩은 §4에 위치한다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다. 01 §4.1은 이미 `.claude/hooks/`를 확장 Module 표면으로 매핑한다. 본 spec은 그 표면을 다음과 같이 구체화한다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Hook Module 정의·직렬화 (§3.2-D) | `.claude/hooks/` 하위 정의와 `.claude/settings.json`의 hooks 선언. Manifest 직렬화는 01 §4.1(Markdown + front-matter / 설정 파일)을 따른다. |
| Event 방출·계측 지점 (§3.2-A) | Claude Code 세션/턴에서 이벤트 원천(lifecycle 전이, runtime 연산, agent 메시지, memory Port 접근)이 발생하는 지점의 계측. |
| Hook Dispatch·순서·격리 (§3.1-D/E) | Claude Code 하네스의 hook 실행 메커니즘이 결정적 순서와 격리 실행을 실현한다. |
| Event Record 직렬화 (§3.2-C) | 하네스가 원천 컨텍스트를 읽기 전용으로 Hook action에 전달하는 형태. |
| Hook action 진입점 (§3.2-D `action`) | `.claude/hooks/` 스크립트·명령 진입점. 실행 모델 지정은 02 §4 실행 모델 바인딩과 정합한다. |

주의: lifecycle·memory 도메인 이벤트의 정확한 방출 경계는 각각 specs/03-loop.md, specs/04-memory.md의 §4 바인딩과 정합해야 한다 (§9 조율).

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부. §3 Core Contract는 유지되고 아래만 교체된다.

- **SP-1: Hook 정의 위치·포맷** — `.claude/hooks/`, `.claude/settings.json` hooks → 대상 환경의 확장 정의 메커니즘.
- **SP-2: 이벤트 계측·방출 지점** — Claude Code 세션/턴 계측 → 대상 환경의 이벤트 방출 메커니즘.
- **SP-3: Hook Dispatch/실행기** — Claude Code 하네스의 hook 실행 → 대상 환경의 dispatch.
- **SP-4: 순서·격리·비차단 실현** — 하네스의 실행 모델 → 대상 환경의 실행 모델.
- **SP-5: Event Record 직렬화·컨텍스트 전달** — 하네스의 컨텍스트 투영 → 대상 환경의 전달 채널.

유지되는 것: §3.2-A 이벤트 카탈로그 ID·명명 규칙, Event Record 형태, Hook Binding 필수 필드, §3.1-D/E 순서·격리·비차단 계약, §3.3 Invariants. 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다.

---

# §5. Memory Access (해당 시)

해당 없음.

Hooks Component 계약 자체는 Memory를 읽거나 쓰지 않는다. Hooks는 `memory.recall` · `memory.record` 이벤트를 **관찰만** 하며, 관찰이 Memory 접근은 아니다.

단서 (불변 규칙): 특정 Hook의 action이 Memory에 기록·회수를 수행한다면, 그 접근 경로는 Memory Service Interface(단일 Port) 하나뿐이며 영속성 백엔드는 Adapter Layer 뒤에 둔다 (ARCHITECTURE.md 5.1, INV-7). Hook은 어떤 경우에도 단일 Port를 우회하지 않는다.

---

# §6. Failure Modes

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| Hook action 오류·타임아웃 | 격리. 본 작업과 다른 Hook은 계속. Hook Failure Report(blocking=false) 보고 (INV-2). | 예 |
| 카탈로그에 없는 Event에 바인딩 시도 | 등록 거부. reason=`UnknownEvent` (§3.1-C). | 예 |
| 유효하지 않은 phase / 중복 hookId | 등록 거부. reason=`InvalidPhase` \| `DuplicateHookId`. | 예 |
| Hook이 Event context 변경 시도 | INV-3 위반. read-only 강제로 차단. | 예 |
| Hook이 본 작업 차단·veto 시도 | v0.1 미지원. INV-1/INV-2 위반으로 무효. | 예 |
| Hook이 Memory 단일 Port 우회 | INV-7 위반. 단일 Port 경유로 교정. | 예 |
| Hook이 역할 경계(02) 또는 Verify 판정(06) 침범 | INV-7 위반. 차단. | 예 |
| 같은 (event, phase) 실행 순서 비결정 | INV-5 위반. §3.1-D 결정 규칙으로 교정. | 예 |
| Hook 추가로 본체 동작이 바뀜 | INV-1 위반. 확장은 본체 불가침이어야 한다. | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.8 완료 조건과 정렬한다.

- **본체 수정 0 시연.** 이벤트 원천의 코드·규격을 한 줄도 바꾸지 않고 Hook 하나를 확장 표면에 추가만 하여, 특정 (event, phase)(예: `lifecycle.complete` @ after)에서 부수 동작(예: 감사 로그 기록)이 실행됨을 보인다. 본체 코드/규격 diff = 0 (INV-1).
- **비차단 시연.** Hook action을 의도적으로 실패시켜도 본 작업이 정상 완료되고, 다른 Hook이 계속 실행됨을 보인다. Hook Failure Report의 blocking=false를 확인한다 (INV-2).
- **순서 결정성 시연.** 같은 (event, phase)에 두 Hook을 등록하고, §3.1-D 규칙대로 실행 순서가 결정적임을 보인다 (INV-5).
- **카탈로그 도출 시연.** 카탈로그의 각 Event가 원천 계약(Glossary §3.2-F / 01 §3.1 / 02 §3.2 / ARCHITECTURE 5.1)에서 도출됨을 근거 열과 대조로 보인다 (INV-6).
- **경계 시연.** Hook이 Event Record를 변경하지 못하고(read-only, INV-3), Memory 접근 시 단일 Port만 경유하며(INV-7), 역할 경계·Verify 판정을 침범하지 않음을 보인다.
- **§3 AI 비의존 시연.** §3 전체를 스캔해 AI 모델명·제품 기능 참조가 0건임을 보인다 (INV-8, DoD-3).

## 검증 방법

- Verifier가 Hook 추가 전후 본체 diff가 0임을 확인한다.
- Verifier가 실패 Hook을 주입한 뒤 본 작업 완료와 다른 Hook 실행을 확인한다.
- Verifier가 두 Hook 등록 후 실행 순서를 §3.1-D 규칙과 대조한다.
- Verifier가 카탈로그의 각 Event를 원천 spec 참조와 대조해 미도출 Event 0건을 확인한다 (INV-6).
- Verifier가 §3 본문을 스캔해 AI 의존 토큰(모델명·제품 기능명·"Claude") 0건을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 추가만으로 확장 (본체 수정 0)**

목표: 모든 작업이 완료될 때 감사 로그를 남긴다.

- Hook Binding: `{ hookId: audit-complete, event: lifecycle.complete, phase: after, order: 0, action: <감사 로그 기록> }`.
- Hook을 담은 Module을 Runtime Register(01 §3.1-A)로 등록만 한다. 이벤트 원천(Loop·Runtime)의 코드·규격은 한 줄도 바뀌지 않는다.
- `lifecycle.complete`가 발생하면 after phase에서 Hook이 호출되어 로그를 남긴다. 본 작업 결과는 그대로다 (INV-1).

**예 2 — 비차단 실패**

- Hook Binding: `{ hookId: notify-replace, event: runtime.replace, phase: after, action: <외부 알림> }`.
- Replace(01 §3.1-A)가 성공한 뒤 Hook이 호출되나, 알림 전송이 타임아웃으로 실패한다.
- Hook Failure Report `{ hookId: notify-replace, reason: timeout, blocking: false, lesson_candidate: 예 }`가 남는다. Replace의 결과는 성공 그대로다. 본 작업은 차단되지 않는다 (INV-2).

**예 3 — 결정적 순서**

- 같은 (event, phase) = (`agent.completionReport`, after)에 두 Hook.
  - `{ hookId: metrics, order: 10 }`, `{ hookId: archive, order: 20 }`.
- 실행 순서: order 오름차순으로 metrics → archive. order가 같았다면 Module 등록 순서, 그다음 hookId 사전순으로 결정된다 (INV-5). Hook은 비차단이므로 순서는 부수 동작 실행 순서에만 영향을 준다.

---

# §9. Open Questions

**Glossary 추가 요청** — 용어 5종(Event 이벤트 · Event Catalog 이벤트 카탈로그 · Phase(before/after) · Hook Binding · Hook Dispatch)은 00-glossary §3.2-J-08 정본 등재 완료(요청 5건 전부 Advisor 승인). 상세 정의·카탈로그의 정본은 이 spec(§3.1-D·§3.2-A/B/D)이 유지한다.

**타 spec 조율:**

- **03-loop 조율** — 해소(lifecycle 도메인 이벤트(§3.2-A)의 방출 경계는 03 §3.2-A 전이 이벤트 기록 시점과 대응 — 모순 없음 확인. Hooks는 전이 "이벤트"만 소비하고 단계 정의·전이 규칙은 침범하지 않았다 · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- **04-memory 조율** — 해소(`memory.recall`·`memory.record` 이벤트는 04 §3.1 Record/Recall 연산과 대응 — 모순 없음 확인. Hook은 단일 Port를 우회하지 않는다(INV-7) · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- **06-verifier 조율** — 해소(Hook은 Verify 판정을 대체·무효화하지 않으며(INV-7) `lifecycle.verify` 이벤트는 관찰만 한다. 06 판정 계약과 경계 정합 확인 완료).
- **09-skills 조율** — Skills와 Hooks는 상호 독립 서브시스템이다. 겹치는 계약을 가정하지 않는다.
- **10-plugins 조율** — 해소(Plugin이 번들해 배포하는 Hook의 등록도 본 spec의 Hook Binding·Runtime Module 등록 계약을 따른다. 배포 단위 소유·매니페스트 포맷은 10 소관 — 09 §9 동일 기록).

**설계 확인 요청 (Advisor 에스컬레이션):**

- **OQ-H1: 비차단 observer 결정** — 해소(승인 — v0.1 Hook은 비차단 observer 전용으로 확정(INV-2). 차단·veto·mutation은 역할 경계(02 §3.2-A)·Verify 판정(06)·Lifecycle 전이(03)와의 강한 조율을 요구하므로 v0.1 범위 제외. 향후 필요 시 재검토 · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- **OQ-H2: 이벤트 방출 주체** — 해소(승인 — 방출 주체는 §4 Adapter Binding 소관으로 확정, 계약 수준 고정 불필요. Core는 관찰 가능한 표면(카탈로그·Event Record·순서·격리)만 정의).
- **OQ-H3: 동률 순서 규칙** — 해소(승인 — `order` 동률 tie-breaker = "Module 등록 순서 → hookId 사전순" 확정. 규범 정본 = §3.1-D).

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 3.2(Modular, Module 교체)·5(스택)·5.1(Memory 단일 Port)·6(Component로서 Hooks)과 정렬한다. Cross-cutting Service는 Memory 하나라는 INV-2(Glossary §3.2-B)를 침범하지 않는다.

## 결정 기록 (Advisor — Wave 4 통합)

- OQ-H1 승인 — v0.1 Hook은 비차단 observer 전용으로 확정.
- OQ-H2 승인 — 이벤트 방출 주체는 §4(Adapter Binding) 소관으로 확정. 계약 수준 고정 불필요.
- OQ-H3 승인 — order 동률 tie-breaker(등록 순서 → hookId 사전순) 확정.
- 03/04 방출 경계: lifecycle 이벤트는 03 §3.2-A 전이 이벤트 기록 시점과, memory 이벤트는 04 §3.1 Record/Recall 연산과 대응 — 모순 없음 확인.
- Glossary 추가 요청 5건 승인 — Glossary §3.2-J 반영.

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 OQ(OQ-H1~H3)·타 spec 조율(03·04·06·10)의 원문+답 이중 잔존 1줄화, Glossary 추가 요청 블록의 등재 완료 1줄화, §2 stale 상태 표기(Review/Adopted → Frozen)·"동시 작성 중" 서술 현행 정정. 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — §3 전체(§3.2-A Event Catalog 포함)·§6·§7 무촉, dependents(§2 = 하드 의존 0 · 조율 09·10) 참조 영향 0(정책 §4-a·§4-c). 종전 문면 = git 앵커 90ca19c.
