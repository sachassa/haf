# specs/01-runtime — Runtime Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05)
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Runtime은 UAHF의 실행 환경이다.

Runtime은 세 가지 문제를 해결한다.

- 기능이 서로 얽혀 교체할 수 없는 문제. 모든 기능을 교체 가능한 Module로 만든다.
- 설정이 프로젝트마다 흩어지고 우선순위가 불명확한 문제. Config를 스코프와 우선순위로 규격화한다.
- Agent와 Module의 시작·실행·종료가 제각각인 문제. 실행 환경의 기동·호스팅·종료 계약을 통일한다.

## 책임 (1~3문장)

Runtime은 Module 시스템·Config·수명주기(시작·실행·종료)를 관장하는 실행 환경 규격이다.

Runtime은 Loop Engine이 Agent Lifecycle을 구동할 "환경"을 제공하며, 그 위에서 Module을 등록·해소·교체한다.

## Non-Goals

- Agent Lifecycle 7단계(Consult ~ Complete)의 단계별 계약을 정의하지 않는다 — specs/03-loop.md 소관이다 (Glossary §9-OQ2).
- Agent 역할의 내부 계약(입력/출력/실행 모델)을 정의하지 않는다 — specs/02-agent.md 소관이다.
- Memory의 기록·회수 계약을 정의하지 않는다 — specs/04-memory.md 소관이다.
- 특정 AI·직렬화 포맷·저장 백엔드를 정의하지 않는다 — Adapter Binding(§4) 소관이다.

---

# §2. Position

- 아키텍처 상 위치: Runtime Layer (Glossary §3.2-A). Core Component "Runtime" (Glossary §3.2-D)의 규격 문서다.
- Runtime Layer는 Presentation → Workflow → Agent → **Runtime** → Core → Adapter 스택에서 Agent Layer 아래, Core Layer 위에 위치한다.
- Loop Engine은 이 Layer에서 Lifecycle을 구동한다 (Glossary §9-OQ2). Runtime은 그 구동 "환경"만 정의하고, 루프 자체는 침범하지 않는다.

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 3.2 Modular, 5 스택, 5.1 Memory Service.
- specs/00-glossary.md (실재, Review) — 모든 용어의 정본.
- specs/TEMPLATE.md (실재, Adopted) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약.
- ROADMAP.md v0.3 (실재) — Runtime & Core Kernel 완료 조건과 산출물.

## 이 spec에 의존하는 spec (dependents)

- specs/02-agent.md — Agent는 Runtime이 호스팅하는 실행 단위다. Agent 진입점 계약은 Runtime의 generic Module 계약을 구현한다. 의존 방향은 02 → 01이다 (§9 조율 항목 참조).
- specs/03-loop.md — Loop Engine은 Runtime 환경 위에서 구동된다.
- specs/08-hooks.md, specs/09-skills.md, specs/10-plugins.md — 확장 시스템은 Runtime의 Module 등록/교체 계약을 확장점으로 사용한다 (ROADMAP v0.8 선행 조건 = v0.3).
- specs/11-adapters.md — Runtime의 이식 교체 지점(§4.2)을 Adapter 규격으로 정식화한다.

## 순환 의존

없다. Runtime의 Core Contract(§3)는 위 dependents 중 어느 것에도 의존하지 않는다. Runtime은 AI·역할 비의존의 generic "hosted unit" 계약만 정의하며, Agent·Loop·확장 규격이 이 계약을 구현하는 방향(하위 → 01)이다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 의존 내용이 한 줄도 들어가지 않는다. 모든 AI·환경 의존 실현은 §4에 둔다.

Runtime은 세 가지 계약을 정의한다.

- Module 시스템 계약 (§3.1-A, §3.2-A)
- Config 계약 (§3.1-B, §3.2-B)
- 수명주기 호스팅 계약 (§3.1-C, §3.2-C)

---

## 3.1 Interface

Runtime은 다음 연산을 노출한다. 모든 연산의 실패는 공통 Failure Report(§3.2-D) 구조로 보고한다.

### A. Module 시스템 연산

**Register**
- 입력: Module Manifest(§3.2-A) 1건.
- 출력: 등록 결과 — 등록된 module id.
- 완료 조건: Manifest가 Module Interface 계약을 만족하고, id가 Registry에서 유일하다.
- 실패 보고: reason = `ContractMismatch` | `DuplicateId`.

**Resolve**
- 입력: contract id (또는 module id).
- 출력: 해당 계약의 활성 Module 핸들(정확히 1개).
- 완료 조건: 대상 계약에 활성 바인딩이 정확히 하나 존재하고, 그 requires가 모두 해소된다.
- 실패 보고: reason = `UnresolvedContract` | `DuplicateBinding` | `DependencyCycle`.

**Replace**
- 입력: 대상 contract id + 새 Module Manifest.
- 출력: 교체 결과 — 이전 module id → 새 module id.
- 완료 조건: 새 Module이 동일 contract를 만족하며 활성화되고, 이전 Module이 비활성화되며, 계약 소비자의 참조는 변경되지 않는다.
- 실패 보고: reason = `ContractMismatch` | `NotReplaceable`.

**Deregister**
- 입력: 대상 module id.
- 출력: 등록 해제 결과 — 해제된 module id.
- 완료 조건: 대상 Module이 비활성화(Deactivate)된 후 Registry에서 제거되고, 그 contract 바인딩이 해제된다. 다른 활성 Module의 requires가 그 contract에 의존 중이면 해제를 거부한다.
- 실패 보고: reason = `DependentExists` | `NotRegistered`.

### B. Config 연산

**Load Config**
- 입력: 스코프별 Config 소스 집합(Global / Project / Module).
- 출력: effective config(§3.2-B) — 우선순위대로 병합된 유효 설정.
- 완료 조건: 모든 존재하는 스코프가 정의된 우선순위(§3.2-B)로 결정적(deterministic)으로 병합된다. 누락 스코프는 건너뛴다.
- 실패 보고: reason = `SchemaViolation`, location = 스코프/키.

### C. 수명주기 호스팅 연산

**Bootstrap**
- 입력: effective config + 등록된 Module 집합.
- 출력: Runtime Context(§3.2-C) — 하위 컴포넌트가 구동될 수 있는 상태(Ready).
- 완료 조건: 모든 필수(required) 계약이 Resolve된다. 선택 계약만 누락되면 상태는 Degraded로 Ready에 준한다.
- 실패 보고: reason = `MissingRequired` | `UnresolvedContract`.

**Shutdown**
- 입력: Runtime Context.
- 출력: 종료 결과.
- 완료 조건: 활성 Module이 활성화의 역순으로 Deactivate되고 자원이 해제된다.
- 실패 보고: reason = `ShutdownIncomplete`, location = 실패한 module id.

주의: Bootstrap과 Shutdown 사이의 "Serve" 구간에서 Agent Lifecycle 7단계를 오케스트레이션하는 주체는 Loop Engine이다. Runtime은 그 구간에 Config·계약 해소·자원을 제공할 뿐, 단계 전이를 정의하지 않는다 (Non-Goals, Glossary §9-OQ2).

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)은 Adapter Binding(§4)이 정한다.

### A. Module Manifest

Module의 등록 서술자다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Module 고유 식별자. 안정적(stable)이어야 교체의 기준이 된다. | 예 |
| `contract` | 이 Module이 구현하는 계약(Port/Interface) 식별자. 교체는 동일 `contract` 내에서만 성립한다. | 예 |
| `version` | Module 버전. | 예 |
| `requires` | 의존하는 contract id 목록. Resolve 시 모두 해소되어야 한다. | 아니오(기본 없음) |
| `entrypoint` | 실행 진입점의 추상 참조. 구체 바인딩은 §4가 해소한다. | 예 |
| `configSchema` | 이 Module의 Config 스키마. | 아니오 |
| `replaceable` | 교체 가능 여부. 기본 `true` (ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 아니오(기본 true) |

### B. Config

Config는 스코프를 가진 key→value 트리다.

- **Global scope** — Framework 전역 기본값. 모든 대상에 적용. 최저 우선순위.
- **Project scope** — 프로젝트 단위 override. 모든 대상에 적용.
- **Module scope** — 특정 Module(`target` = module id) 네임스페이스에 국한된 설정.

**로딩 순서와 우선순위**

- 로딩 순서: Global → Project → Module.
- 우선순위(높음 → 낮음): **Module > Project > Global**. 같은 키가 겹치면 높은 우선순위가 이긴다(last-writer-wins by precedence).
- effective config는 결정적이다. 동일 입력은 항상 동일 결과를 낸다.
- 존재하지 않는 스코프는 병합에서 건너뛴다.

주의: 위 Project ↔ Module 우선순위 방향은 ARCHITECTURE·ROADMAP이 명시하지 않은 Runtime 설계 결정이다. §9에 확인 항목으로 기록한다.

### C. Runtime Context

Bootstrap의 산출물이자 호스팅 상태다.

| 필드 | 의미 |
|---|---|
| `effectiveConfig` | §3.2-B의 병합 결과. |
| `registry` | contract id → 활성 module id 바인딩과 등록된 Manifest 집합. |
| `state` | `Ready` (필수 계약 전부 해소) / `Degraded` (선택 계약 일부 누락) / `Failed` (필수 계약 미해소). |

### D. Failure Report

모든 Runtime 연산의 공통 실패 보고 구조다.

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Register / Resolve / Replace / Deregister / LoadConfig / Bootstrap / Shutdown). |
| `target` | 대상 (contract id, module id, config 스코프·키). |
| `reason` | 사유 코드 (SchemaViolation / ContractMismatch / DuplicateId / UnresolvedContract / DuplicateBinding / DependencyCycle / NotReplaceable / DependentExists / NotRegistered / MissingRequired / ShutdownIncomplete). |
| `location` | 실패 지점 참조 (스코프·키·Manifest 참조). |

### E. 디렉터리/구조 규격 (계약 수준)

물리 경로는 §4가 정한다. 여기서는 AI 비의존 규칙만 정의한다.

- Core 디렉터리는 AI 비의존 계약만 담는다. AI 의존 요소 0건이 불변 규칙이다 (INV-4).
- 각 Module은 자기완결적(self-contained) 단위다. 자신의 Manifest·구현·(있다면) configSchema를 한 경계 안에 둔다.
- Adapter Binding 산출물은 Core 디렉터리와 물리적으로 분리된 별도 경계에 둔다.

---

## 3.3 Invariants

- **INV-1 (교체 가능).** 모든 Module은 교체 가능하다 (ARCHITECTURE 3.2). 동일 `contract`를 만족하는 Module로 교체할 때 계약 소비자의 코드·규격 변경은 0이다. `replaceable=false`는 명시적 예외이며 근거를 요구한다.
- **INV-2 (단독 사용).** Runtime은 필수 계약만 해소되면 Module의 부분 집합만으로 기동할 수 있다 (ARCHITECTURE 3.2). 선택 Module의 부재는 Degraded일 뿐 Failed가 아니다.
- **INV-3 (계약당 단일 바인딩).** 한 contract에는 활성 Module이 정확히 하나 바인딩된다. Resolve는 항상 유일한 핸들을 반환한다.
- **INV-4 (Core AI 비의존).** Core 디렉터리에 AI 의존 요소는 0건이다 (ROADMAP v0.3). AI·실행 환경·백엔드 의존은 전부 Adapter Layer 뒤에 둔다.
- **INV-5 (결정적 Config).** Config 병합은 결정적이며 우선순위 순서(§3.2-B)는 고정된다.
- **INV-6 (경계 불가침).** Runtime은 Agent Lifecycle 7단계를 정의하지 않는다 (Loop 소관). Agent 역할 내부 계약을 정의하지 않는다 (02 소관). Runtime은 호스팅 계약만 정의한다.
- **INV-7 (안정 식별자).** Module `id`와 `contract` id는 안정적이어야 한다. 교체·해소는 이 안정성에 의존한다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x 구현 형태는 하이브리드다. Runtime은 Claude Code 위에서 self-hosting한다. §3의 추상 계약을 Claude Code 표면에 다음과 같이 바인딩한다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Module Manifest(§3.2-A) 직렬화 | Markdown + front-matter 파일. 예: `.claude/agents/*.md`. |
| Agent Module 진입점 | `.claude/agents/{advisor,planner,worker,verifier}.md` — Runtime generic Module 계약의 Agent 구현 바인딩. 진입점 내부 계약은 specs/02-agent.md §4 소관. |
| 확장 Module 표면 | `.claude/commands/`, `.claude/hooks/`, `.claude/skills/` — 확장 Module 등록 바인딩. 상세는 specs/08·09·10 소관. |
| Config — Project scope | `.claude/CLAUDE.md`, `.claude/AGENT.md`, 프로젝트 설정 파일(settings.json 등). |
| Config — Global scope | 사용자·환경 전역 설정 파일. |
| Config — Module scope | 각 Module 정의 파일 내부의 설정 블록. |
| Core 디렉터리 (AI 비의존) | `framework/core/`, `framework/runtime/`. AI 의존 요소 0건 유지 대상. |
| Module 구현 디렉터리 | `framework/{loop,memory,verifier,workflow,plugins}/`. |
| Adapter Binding 산출물 | `framework/adapters/`, `.claude/`. AI·환경 의존 요소는 여기로 격리. |
| 수명주기 호스트 프로세스 | Claude Code 세션/턴 = Bootstrap~Serve~Shutdown 구간의 실행 컨테이너. |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부. Core Contract(§3)는 유지되고 아래만 교체된다.

1. **Manifest 직렬화** — `.claude/*.md` + front-matter → 대상 환경의 서술자 포맷.
2. **Config 소스·위치** — `.claude/CLAUDE.md`, `.claude/AGENT.md`, 설정 파일 → 대상 환경의 Config 메커니즘.
3. **진입점 해소** — 파일 기반 정의 로딩 방식 → 대상 환경의 Module 로더.
4. **호스트 프로세스/세션 수명주기** — Claude Code 세션/턴 → 대상 환경의 실행 프로세스.
5. **바인딩 디렉터리** — `.claude/`, `framework/adapters/` → 대상 환경의 규약.
6. **확장 표면** — `.claude/{commands,hooks,skills}` → 대상 환경의 확장 메커니즘 (상세 08·09·10).
7. **Agent 역할 실행 모델 지정** — specs/02-agent.md §4 소관. Runtime은 참조만 하고 정의하지 않는다.

이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다.

---

# §5. Memory Access (해당 시)

해당 없음.

Runtime은 Memory를 직접 읽거나 쓰지 않는다. ARCHITECTURE 5.1의 Memory 소비자 목록(Agent, Loop, Workflow, Verifier)에 Runtime은 포함되지 않는다.

단서 (불변 규칙): Runtime이 Memory Service를 하나의 교체 가능한 Module로 등록·배선(wiring)하는 경우에도, 그 접근 경로는 Memory Service Interface(단일 Port) 하나뿐이며 영속성 백엔드는 Adapter Layer 뒤에 둔다. Runtime은 배선만 하고 Memory 내용에는 접근하지 않는다.

---

# §6. Failure Modes

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| Config 스키마 위반 / 스코프 충돌 | Load Config 실패. Failure Report(reason=SchemaViolation, location=스코프·키) 보고. | 예 |
| 필수 계약 미해소 (required Module 미등록) | Bootstrap 실패(state=Failed). reason=MissingRequired. | 예 |
| 한 계약에 활성 Module 2개 (INV-3 위반) | Resolve 실패. reason=DuplicateBinding. | 예 |
| Module 의존 순환 | Resolve 실패. reason=DependencyCycle. | 예 |
| 교체 불가/계약 불일치 Module 교체 시도 | Replace 거부. reason=NotReplaceable | ContractMismatch. | 예 |
| 의존 중인 contract의 Module 등록 해제 시도 | Deregister 거부. reason=DependentExists. | 예 |
| Core 디렉터리에 AI 의존 요소 혼입 (INV-4 위반) | 경계 위반. 검증(§7) 실패로 판정. | 예 |
| 선택 Module 부재 | 실패 아님. state=Degraded로 계속 (INV-2). | 아니오 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.3 완료 조건과 정렬한다.

- **단독 사용 시연.** 필수 계약만 만족하는 최소 Module 집합만 등록한 Runtime이 Bootstrap되어 state=Ready(또는 Degraded)로 기동됨을 보인다 (INV-2).
- **교체 시연.** 한 contract의 Module A를 동일 contract의 Module B로 Replace해도, 계약 소비자의 코드·규격 변경 0으로 Resolve가 Module B를 반환하고 동작이 유지됨을 보인다 (INV-1, ARCHITECTURE 3.2 Modular 검증).
- **Core AI 비의존 시연.** Core 디렉터리 전체를 스캔해 AI 모델명·제품 기능 참조가 0건임을 보인다 (INV-4).
- **Config 일치 시연.** 선언한 스코프(Global/Project/Module)가 우선순위(Module > Project > Global)대로 병합되어 effective config가 §3.2-B 규격과 일치함을 보인다 (INV-5).
- **경계 시연.** Runtime이 Agent Lifecycle 7단계를 정의하지 않고 호스팅 계약만 노출함을 보인다 (INV-6).

## 검증 방법

- Verifier가 최소 집합 Bootstrap을 실행해 상태와 Resolve 결과를 확인한다.
- Verifier가 Replace 전후 소비자 참조 diff가 0임을 확인한다.
- Verifier가 Core 디렉터리 전체에서 금지 토큰(특정 AI·모델명·제품 기능) 0건을 확인한다.
- Verifier가 effective config를 스펙 스키마와 대조한다.
- Verifier가 §3에 AI 의존 요소 0건임을 확인한다 (DoD-3).

---

# §8. Examples

**예 1 — Module 교체 (동일 contract, 백엔드 스왑)**

Memory Service Provider가 `contract = MemoryServiceInterface`를 구현하는 Module로 등록되어 있다.
→ 저장 백엔드가 다른 새 Provider Module(같은 `contract`)의 Manifest로 Replace를 호출한다.
→ Runtime은 이전 Module을 Deactivate하고 새 Module을 Activate한다. `contract`는 동일하므로 계약 소비자(Agent, Loop 등)의 참조는 그대로다.
→ 이후 Resolve(MemoryServiceInterface)는 새 Module 핸들을 반환한다.
→ Runtime은 등록·배선만 수행하며 Memory 내용에는 접근하지 않는다 (§5).

**예 2 — Config 스코프 병합**

키 `verify.strict`에 대해:
- Global scope: `false` (Framework 기본값)
- Project scope: `true` (이 프로젝트는 엄격 검증)
- Module scope(target = 특정 Verifier Module): 미지정

→ effective config의 `verify.strict` = `true`. 우선순위 Module > Project > Global에서 Module이 미지정이므로 Project가 이긴다.

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**Glossary 추가 요청** (본 spec이 정의·형식화하지만 Glossary §3.2에 정본 항목이 없는 용어. Glossary §9-OQ6 흐름에 따라 정본화 요청):

- Glossary 추가 요청: Module (모듈) — 독립적으로 사용·교체 가능한 기능 단위. 안정적 `id`와 구현 `contract`를 가지며 Runtime이 등록·해소·교체한다.
- Glossary 추가 요청: 모듈 시스템 (Module System) — Module의 정의·등록·해소·교체 규칙의 총체. Runtime Component가 관장한다. (현재 Glossary에서 참조만 되고 정본 정의가 없음.)
- Glossary 추가 요청: Module Manifest — Module의 등록 서술자. 필드는 specs/01-runtime §3.2-A.
- Glossary 추가 요청: Config (설정) — 스코프(Global/Project/Module)와 우선순위를 가진 key→value 설정 트리. (현재 Glossary에서 참조만 되고 정본 정의가 없음.)
- Glossary 추가 요청: Runtime Context — Bootstrap 산출물이자 호스팅 상태. 필드는 specs/01-runtime §3.2-C.

결정(Advisor): 5건 전부 승인. Glossary §3.2-I "Runtime 계약 용어"로 추가되었다. 상세 필드의 정본은 이 spec §3.2가 유지한다.

**설계 확인 요청:**

- OQ-R1 (결정 완료) — Config 우선순위 방향.
  결정(Advisor): **Module > Project > Global**로 확정한다. 근거 — Module scope는 모듈 자체의 기본값이 아니라 특정 Module을 겨냥해 작성되는 가장 좁은 override이므로, 좁은 스코프 우선(specificity) 원칙이 결정성과 예측 가능성을 높인다. Module 자체의 기본값은 configSchema 기본값으로서 병합 최하위에 위치하므로, "Project가 모듈 기본값을 덮는" 요구는 Project scope로 이미 충족된다.

**타 spec 조율:**

- 02-agent 조율 필요 — Runtime이 Agent를 Bootstrap·Shutdown하려면 Agent 진입점(entrypoint) 계약이 필요하다. Runtime은 generic "hosted unit / Module" 진입점 계약만 정의했다. Agent가 이 계약을 어떻게 구현하는지(입력/출력/실행 진입점 시그니처)는 specs/02-agent.md가 정의해야 하며, 두 계약이 정합해야 한다. 02의 내용을 추측·인용하지 않았다.
  결정(Advisor — 조율 확정): Agent Module의 entrypoint는 위임 메시지(specs/02-agent.md §3.2-B)를 입력으로 받고, 완료 보고(02 §3.2-C) 또는 실패 보고(02 §3.2-D)를 출력으로 반환한다. 메시지 계약은 02가 소유하고, 호스팅 계약(등록·해소·교체·Bootstrap)은 01이 소유하며, 메시지가 흐르는 물리 채널은 각 spec의 §4 Adapter Binding 소관이다. 두 spec 모두 이 경계와 모순되지 않음을 확인했다.
- 03-loop 조율 필요 — Runtime의 "Serve" 구간에서 Loop Engine이 소비하는 호스팅 계약(Config·계약 해소·자원 제공)의 정확한 노출 표면은 specs/03-loop.md와 정합 확인이 필요하다. Runtime은 호스팅 계약만 정의하고 루프 단계는 정의하지 않았다 (Glossary §9-OQ2 준수).

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 3.2(Modular)·5(스택)·5.1(Memory 단일 Port)과 Glossary §9-OQ1 결정에 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

결정(Advisor — Wave 4 통합): specs/10-plugins.md §9의 요청에 따라 §3.1-A에 Deregister 연산을 추가했다. Registry 수명주기는 Runtime 소유이므로 Plugins가 우회 정의하지 않고 01이 소유한다. Plugin의 Deactivate/Remove(잔여물 0)는 이 연산 위에서 성립한다.
