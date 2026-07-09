# specs/09-skills — Skills Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05)
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Skills는 재사용 가능한 작업 능력 단위다 (Glossary §3.2-D).

Skill은 하나의 작업 능력을 정의·등록·발견·호출하는 계약이다.

## 이 컴포넌트가 해결하는 문제

- 능력이 Agent 정의나 Framework 본체에 하드코딩되면 재사용할 수 없다. 프로젝트마다 같은 능력을 중복 작성한다.
- 능력을 추가하려면 본체를 수정해야 한다. 확장이 본체를 오염시킨다.
- 필요 없을 때에도 모든 능력의 지시가 Context에 상주한다. Token이 낭비된다.

## 책임 (1~3문장)

Skills는 재사용 가능한 작업 능력 단위의 정의·등록·발견·호출 계약을 정의한다.

Skills는 본체 수정 없이 능력을 추가하고, 여러 프로젝트에서 재사용하며, 필요할 때만 본문을 로드하는 규격이다.

## Non-Goals

- Agent 역할·경계·위임/보고 메시지 계약을 정의하지 않는다 — specs/02-agent.md 소관이다. Skill은 그 경계 안에서만 실행된다.
- Module의 등록·해소·교체 generic 계약을 정의하지 않는다 — specs/01-runtime.md 소관이다. Skill은 이를 확장점으로 사용만 한다.
- Hooks(이벤트 기반 확장점)의 계약을 정의하지 않는다 — specs/08-hooks.md 소관이다.
- Plugins(기능 묶음 배포 단위)의 계약을 정의하지 않는다 — specs/10-plugins.md 소관이다.
- Memory·Lessons의 기록·회수 내부 포맷을 정의하지 않는다 — specs/04-memory.md, specs/05-lessons.md 소관이다.
- Agent Lifecycle 7단계의 단계 전이를 정의하지 않는다 — specs/03-loop.md 소관이다.
- 특정 AI·직렬화 포맷·저장 백엔드를 정의하지 않는다 — Adapter Binding(§4) 소관이다.

---

# §2. Position

- 아키텍처 상 위치: Core Component "Skills"(Glossary §3.2-D)의 규격 문서다. Skills는 독립 Layer가 아니다. Runtime Layer의 Module 시스템(01 §3.1-A) 위에 확장 Module로 등록되어 Agent Layer가 소비하는 확장 서브시스템이다.
- Component→Layer 최종 매핑은 Glossary §9-OQ6 흐름에 따라 Wave 3에서 Advisor가 통합한다. 이 §2 선언은 그 통합 대상이며 위 정의와 모순될 수 없다 (§9 기록).

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 3.2 Modular, 3.6 Token Efficiency, 6 (Skills = Component), 8 (본체 재작성 없는 확장).
- specs/00-glossary.md (실재, Review) — 모든 용어의 정본. Skills = 재사용 가능한 작업 능력 단위.
- specs/01-runtime.md (실재, Review) — Module 등록/해소/교체 계약. Skill은 이 계약을 확장점으로 사용한다 (01 §2 dependents에 09 명시).
- specs/02-agent.md (실재, Review) — Agent 역할 경계(§3.2-A), 위임/보고 메시지, Lifecycle 책임. Skill은 이 경계를 우회할 수 없다.
- specs/TEMPLATE.md (실재, Adopted) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약(상위 규약).
- ROADMAP.md v0.8 (실재) — Extension System 완료 조건과 산출물.

## 이 spec에 의존하는 spec (dependents)

- 현재 확정된 것 없음.
- Plugins(specs/10)이 Skill을 배포 단위에 포함할 가능성, Hooks(specs/08)가 Skill 호출을 이벤트로 트리거할 가능성은 상호 독립 서브시스템 간 조율 항목이다. 추측하지 않는다 (§9 08/10 조율).

## 순환 의존

없다. Skills의 Core Contract(§3)는 01(Module 계약)과 02(역할 경계)에 의존한다. 01·02는 Skills에 의존하지 않는다. 의존 방향은 항상 09 → {01, 02}이다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 AI·환경 의존 실현은 §4에 둔다.

Skills는 세 가지를 정의한다.

- Skill 서술 계약 — 무엇이 하나의 Skill을 구성하는가 (§3.2-A, §3.2-B).
- Skill 수명 연산 — 등록·발견·로드·호출 (§3.1).
- Skill 불변 규칙 — 어떤 구현에서도 지켜야 할 규칙 (§3.3).

Skill은 01의 Module의 특화(specialization)다. 등록·해소·교체·안정 식별자 규칙은 01의 Module 계약을 그대로 구현하며 재정의하지 않는다.

---

## 3.1 Interface

Skills가 정의하는 연산이다. 모든 연산의 실패는 Skill Failure Report(§3.2-C) 구조로 보고한다.

### A. Register (등록)

- 입력: Skill Manifest(§3.2-A) 1건.
- 출력: 등록 결과 — 등록된 skill id.
- 완료 조건: Manifest가 01 §3.2-A Module Manifest 계약과 Skill 필수 필드(§3.2-A)를 모두 만족하고, skill id가 Registry에서 유일하다.
- 실패 보고: reason = `ContractMismatch`(Module/Skill 계약 불일치) | `DuplicateId`(01 Register 계약 상속).

### B. Discover & Select (발견·선택)

- 입력: 작업 컨텍스트 — 현재 task 요약 또는 트리거 신호.
- 출력: 트리거가 매칭된 Skill 후보 목록과 선택 결과(0개 이상). 후보 0은 유효한 빈 결과다.
- 완료 조건: 각 등록된 Skill의 Trigger(§3.2-A)가 작업 컨텍스트에 대해 평가되고, 매칭된 Skill만 후보가 된다. 동일 컨텍스트는 동일 후보 집합을 낸다 (결정적, INV-7).
- 제약: 발견·선택은 경량 메타데이터(id / name / purpose / trigger)만 사용한다. Skill 본문(§3.2-A body)은 이 단계에서 로드하지 않는다 (Token Efficiency, INV-4).
- 실패 보고: reason = `AmbiguousSelection`(다수 매칭에서 결정적 선택 불가). 후보 0은 실패가 아니며 `NoMatchingSkill`로 구분되는 빈 결과다.

### C. Load (로드)

- 입력: 선택된 skill id.
- 출력: 해당 Skill의 본문(§3.2-A body)과 필요 자원(§3.2-A resources) 참조.
- 완료 조건: 선택된 Skill에 한해 본문이 로드된다. 미선택 Skill의 본문은 로드되지 않는다 (INV-4).
- 실패 보고: reason = `SkillBodyUnavailable` | `ResourceUnresolved`.

### D. Invoke (호출)

- 입력: 로드된 Skill 본문 + Skill 입력 계약(§3.2-B)에 맞는 입력 + 호출 Agent의 역할.
- 출력: Skill 출력 계약(§3.2-B)에 맞는 산출물. 이 산출물은 호출 Agent의 완료 보고(02 §3.2-C) 또는 실패 보고(02 §3.2-D)에 반영된다.
- 완료 조건: Skill 지시가 호출 Agent의 역할 경계(02 §3.2-A) 안에서 수행되고, 상위 규약과 충돌 없이 실행된다.
- 충돌 처리: Skill 지시가 역할 경계를 벗어나거나 상위 규약과 충돌하면, 우선순위 규칙(§3.3 INV-2·INV-3)에 따라 상위 규약이 이기고 해당 Skill 지시는 무시되며 충돌이 보고된다.
- 실패 보고: reason = `RoleBoundaryViolation` | `PrecedenceConflict` | `InputContractMismatch`.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)은 Adapter Binding(§4)이 정한다.

### A. Skill Manifest

Skill의 등록 서술자다. 01 §3.2-A Module Manifest의 특화다. Module Manifest 필드를 상속하고 Skill 고유 필드를 추가한다.

"로드 계층"은 그 필드가 언제 Context에 로드되는가를 규정한다. 메타데이터는 발견·선택 시 항상 열람되고, 본문은 선택된 뒤에만 로드된다 (INV-4).

| 필드 | 의미 | 필수 | 로드 계층 |
|---|---|---|---|
| `id` | Skill 고유 식별자(= Module id). 안정적이어야 교체·해소의 기준이 된다 (01 INV-7). | 예 | 메타데이터 |
| `contract` | 구현하는 계약 식별자. Skill은 공통 Skill 계약을 구현한다 (§9 Glossary 추가 요청: SkillInterface). 교체는 동일 `contract` 내에서만 성립한다. | 예 | 메타데이터 |
| `version` | Skill 버전 (01 상속). | 예 | 메타데이터 |
| `name` | 사람이 읽는 Skill 이름. | 예 | 메타데이터 |
| `purpose` | 이 Skill이 수행하는 작업의 목적(1~2문장). 발견 단계에서 사용한다. | 예 | 메타데이터 |
| `trigger` | 트리거 조건 — 언제 이 Skill이 적용되는가. 발견·선택의 평가 대상(§3.1-B). | 예 | 메타데이터 |
| `io` | 입력/출력 계약(§3.2-B) — 무엇을 받고 무엇을 내는가. | 예 | 메타데이터 |
| `body` | 지시 본문 — 수행 절차. 선택된 뒤에만 로드된다. | 예 | 본문 |
| `resources` | 필요 자원 — 수행에 필요한 파일·도구·다른 계약 참조. | 아니오 | 본문 |
| `requires` | 의존하는 contract id 목록 (01 상속). Resolve 시 모두 해소되어야 한다. | 아니오 | 메타데이터 |
| `replaceable` | 교체 가능 여부. 기본 `true` (01 상속, ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 아니오(기본 true) | 메타데이터 |

### B. Skill I/O Contract (입력/출력 계약)

`io` 필드의 구조다. 재사용성의 기반이다.

| 필드 | 의미 |
|---|---|
| `input` | Skill이 받는 입력의 형태·의미. 호출 Agent가 제공한다. |
| `output` | Skill이 내는 산출물의 형태·의미·위치. 호출 Agent의 완료 보고(02 §3.2-C)에 반영된다. |

입력/출력이 프로젝트 비의존으로 정의되면 한 Skill은 여러 프로젝트에서 재사용된다. 프로젝트 특정 값은 Config(01 §3.2-B)나 `input`으로 주입되고 `body`에 하드코딩되지 않는다 (INV-5).

### C. Skill Failure Report

모든 Skill 연산의 공통 실패 보고 구조다. 01 §3.2-D Failure Report의 필드 구조를 재사용한다.

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Register / Discover&Select / Load / Invoke). |
| `target` | 대상 (skill id, contract id, 작업 컨텍스트 참조). |
| `reason` | 사유 코드 (ContractMismatch / DuplicateId / AmbiguousSelection / SkillBodyUnavailable / ResourceUnresolved / RoleBoundaryViolation / PrecedenceConflict / InputContractMismatch). |
| `location` | 실패 지점 참조 (Manifest 필드, 트리거, 본문 지시). |

주의: Register의 사유 코드(ContractMismatch, DuplicateId)는 01 §3.2-D enum을 상속한다. Skill 특화 연산(Discover&Select / Load / Invoke)의 사유 코드는 이 spec이 소유한다. 두 enum의 소유 경계는 §9에 01 조율 항목으로 기록한다.

---

## 3.3 Invariants

- **INV-1 (본체 불가침 — 확장만으로 능력 추가).** Skill 등록만으로 능력이 확장된다. Framework 본체 코드·규격 수정은 0이다 (ROADMAP v0.8, ARCHITECTURE 8). Skill 제거 시 본체는 Skill 부재 전 상태로 되돌아간다.
- **INV-2 (역할 경계 불침범).** Skill은 호출 Agent의 역할 경계(02 §3.2-A)를 확장하거나 우회할 수 없다. Skill은 그 Agent가 이미 가진 권한 안에서만 실행된다 (02 INV-3). 역할 경계 밖을 지시하는 Skill 지시는 무효다.
- **INV-3 (상위 규약 우선 — Precedence).** Skill 지시가 상위 규약과 충돌하면 상위 규약이 이긴다. 우선순위는 다음 순서로 고정된다 (높음 → 낮음).
  1. ARCHITECTURE.md (최우선)
  2. AGENT.md (상위 규약)
  3. 담당 spec의 계약(예: 02 역할 경계) 및 위임 메시지 제약(02 §3.2-B constraints, O1 위임 범위)
  4. Skill 지시 (최하위)

  충돌하는 Skill 지시는 무시되고, 충돌은 `PrecedenceConflict`로 보고된다.
- **INV-4 (Token Efficiency — 지연 로드).** Skill 본문(body/resources)은 필요할 때만 로드된다. 발견·선택은 메타데이터(id/name/purpose/trigger/io)만 사용한다. 미선택 Skill 본문은 Context에 로드되지 않는다 (ARCHITECTURE 3.6).
- **INV-5 (재사용성).** Skill의 I/O 계약과 본문은 프로젝트 비의존으로 작성된다. 한 Skill은 여러 프로젝트에서 재등록만으로 재사용된다. 프로젝트 특정 값은 Config나 입력으로 주입되고 본문에 하드코딩되지 않는다.
- **INV-6 (Module 계약 준수).** Skill은 01의 Module 계약을 구현한다. 등록·해소·교체(01 §3.1-A)와 안정 식별자(01 INV-7), 교체 가능(01 INV-1) 규칙을 그대로 따른다. Skill은 이 계약을 재정의하지 않는다.
- **INV-7 (결정적 발견).** 동일 작업 컨텍스트에 대한 발견·선택은 결정적이다. 동일 입력은 동일 후보 집합을 낸다.
- **INV-8 (AI 비의존).** §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 트리거 평가 방식·본문 표현·로드 메커니즘의 실현은 §4에 둔다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다. Skill 표면은 01 §4.1의 확장 Module 표면(`.claude/skills/`)에 정렬한다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Skill Manifest(§3.2-A) 직렬화 | `.claude/skills/` 하위의 Markdown + front-matter 파일 (01 §4.1 확장 Module 표면과 정렬). 메타데이터 필드는 front-matter, `body`는 Markdown 본문. |
| Skill 등록(§3.1-A) | Runtime의 Module Register 바인딩(01 §4.1) 위에 Skill 표면으로 등록된다. |
| Skill 발견·선택(§3.1-B) | 작업 컨텍스트에 대한 front-matter의 `trigger` 평가로 후보를 선정한다. |
| Skill 로드(§3.1-C, 지연) | 선택된 Skill의 Markdown 본문만 Context에 로드한다. front-matter는 항상 열람 가능, 본문은 선택 시 로드. |
| Skill 호출(§3.1-D) | 로드된 본문 절차를 호출 Agent가 자신의 역할 경계(02 §4) 안에서 수행한다. |
| 필요 자원(`resources`) | Skill 경계 안의 파일·도구 참조. |
| Config 주입 | 01 §3.2-B Config로 프로젝트 특정 값을 주입한다 (하드코딩 금지, INV-5). |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부다. §3 Core Contract는 유지되고 아래만 교체된다.

- SP-1: Skill 정의 위치·포맷 (`.claude/skills/`, Markdown + front-matter) → 대상 환경의 Skill 정의 메커니즘.
- SP-2: 메타데이터/본문 저장 분리 (front-matter vs 본문) → 대상 환경의 경량 메타데이터·본문 분리 표현.
- SP-3: 트리거 평가 메커니즘 → 대상 환경의 Skill 매칭·선택 방식.
- SP-4: 지연 로드 메커니즘 (선택된 본문의 Context 주입) → 대상 환경의 지연 로드 방식.
- SP-5: 등록 표면 (Runtime Module Register 바인딩 경유) → 01 §4.2 이식 교체 지점을 상속한다.

유지되는 것: §3.2-A Manifest 필수 필드, §3.2-B I/O 계약, §3.3 Invariants(특히 INV-2 역할 경계, INV-3 우선순위, INV-4 지연 로드). 이들은 이식 시 바뀌지 않는다.

이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다.

---

# §5. Memory Access (해당 시)

해당 없음. Skills Component 자체는 Memory를 직접 읽거나 쓰지 않는다.

이유: ARCHITECTURE 5.1의 Memory 소비자 목록(Agent, Loop, Workflow, Verifier)에 Skills는 포함되지 않는다. Skill을 호출한 Agent가 자신의 Memory 접근(02 §5)을 수행할 뿐이다.

단서 (불변 규칙): Skill 사용 이력(어떤 작업에 어떤 Skill이 선택되었는가, Skill 호출 실패 등)의 기록이 필요하다고 판단되는 경우에도, 그 기록은 호출 Agent가 Memory Service Interface(단일 Port)를 통해서만 수행한다 (ARCHITECTURE 5.1, 02 INV-8). Skills는 Memory로 향하는 두 번째 경로를 열지 않는다. Skill 호출 실패는 Lesson 후보이며, 그 기록은 호출 Agent의 실패 보고(02 §3.2-D)와 Memory Update(02 §5)를 경유한다.

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다.

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| Skill이 역할 경계 밖 행위를 지시 (Agent 권한 초과) | INV-2로 차단. reason=RoleBoundaryViolation. Skill 지시 무효. | 예 |
| Skill 지시 ↔ 상위 규약 충돌 | INV-3 우선순위로 상위 규약이 이김. reason=PrecedenceConflict. Skill 지시 무시. | 예 |
| 미선택 Skill 본문까지 로드 (Token 낭비) | INV-4 위반. 검증(§7) 실패로 판정. | 예 |
| Skill 등록으로 능력 확장 실패 (본체 수정 필요) | INV-1 위반. ROADMAP v0.8 완료 조건 미달. | 예 |
| 프로젝트 특정 값을 본문에 하드코딩 → 타 프로젝트 재사용 불가 | INV-5 위반. Config·입력 주입으로 교정. | 예 |
| Skill id 중복 / 계약 불일치 등록 | 01 Register 실패 상속. reason=DuplicateId \| ContractMismatch. | 예 |
| 트리거 매칭 후보 0 | 실패 아님. 빈 결과(NoMatchingSkill). Agent는 Skill 없이 진행. | 아니오 |
| 다수 Skill이 동일 트리거로 매칭, 결정적 선택 불가 | reason=AmbiguousSelection. 선택 규칙 필요 — §9 조율. | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.8 완료 조건과 정렬한다.

- **확장 시연.** Skill 1개를 서드파티 형태로 등록만 하여, 본체 코드·규격 수정 0으로 능력이 확장됨을 보인다 (INV-1, ROADMAP v0.8).
- **지연 로드 시연.** 여러 Skill이 등록된 상태에서, 발견·선택이 메타데이터만 사용하고, 선택된 Skill의 본문만 로드되며 미선택 본문은 로드되지 않음을 보인다 (INV-4, Token Efficiency).
- **역할 경계 시연.** Skill이 호출 Agent의 역할 경계 밖 행위를 지시할 때 차단됨을 보인다 (INV-2).
- **우선순위 시연.** Skill 지시가 상위 규약과 충돌할 때 상위 규약이 이기고 Skill 지시가 무시됨을 보인다 (INV-3).
- **재사용 시연.** 동일 Skill을 다른 프로젝트에 재등록만으로 재사용하고, 프로젝트 특정 값이 Config·입력으로 주입됨을 보인다 (INV-5).
- **결정적 발견 시연.** 동일 컨텍스트에 대한 발견 결과가 반복 실행에서 동일함을 보인다 (INV-7).
- **AI 비의존 시연.** §3 본문에 특정 AI 모델명·제품 기능 참조가 0건임을 보인다 (INV-8, DoD-3).

## 검증 방법

- Verifier가 Skill 등록 전후 본체 diff = 0을 확인한다.
- Verifier가 로드된 Context에 미선택 Skill 본문이 없음을 확인한다.
- Verifier가 역할 경계·우선순위 위반 케이스를 02 §3.2-A 표와 §3.3과 대조해 판정한다.
- Verifier가 발견 연산을 반복 실행해 후보 집합이 동일함을 확인한다.
- Verifier가 §3 본문에서 금지 토큰(AI 모델명·제품 기능) 0건을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 등록만으로 능력 확장 + 지연 로드**

Skill "commit-message-writer"를 등록한다. Manifest: name="Commit Message Writer", purpose="변경 사항에서 커밋 메시지 초안 작성", trigger="커밋 생성 작업", io(input=변경 요약, output=커밋 메시지 초안), body(작성 절차).

→ 발견: Worker의 현재 task="변경 커밋"에 대해 trigger를 평가 → 매칭. 이 단계는 메타데이터만 사용하고 body는 로드하지 않는다.
→ 로드: 선택된 Skill의 body만 Context에 로드한다.
→ 호출: Worker가 자신의 역할 경계 안에서 body 절차를 수행하고, 산출물을 완료 보고(02 §3.2-C)에 반영한다.
→ 본체 수정은 0이다 (INV-1). 다른 프로젝트에도 재등록만으로 재사용된다 (INV-5).

**예 2 — 우선순위 충돌 (Precedence)**

Skill body가 "검증 없이 바로 완료 보고하라"고 지시한다.

→ 이 지시는 상위 규약(02 INV-4: 완료 보고는 Verify 통과 뒤에만 생성)과 충돌한다.
→ INV-3 우선순위: 상위 규약이 이긴다. Skill 지시는 무시된다. reason=PrecedenceConflict로 보고한다.
→ Worker는 Verify 통과 뒤에만 완료 보고를 남긴다.

**예 3 — 역할 경계 (Role Boundary)**

Skill body가 Worker에게 "이 Architecture 결정을 확정하라"고 지시한다.

→ Architecture 결정은 Advisor의 권한이다 (02 §3.2-A). Skill은 역할 경계를 확장할 수 없다 (INV-2).
→ reason=RoleBoundaryViolation. Skill 지시는 무효다.
→ Worker는 추측하지 않고 Advisor에게 에스컬레이션한다 (02 O4).

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**Glossary 추가 요청** (본 spec이 정의·형식화하지만 Glossary §3.2에 정본 항목이 없는 용어. Glossary §9-OQ6 흐름에 따라 정본화 요청):

- Glossary 추가 요청: Skill Manifest — Skill의 등록 서술자. 01 §3.2-A Module Manifest의 특화. 필드의 정본은 specs/09-skills §3.2-A.
- Glossary 추가 요청: Trigger (트리거 조건) — 언제 이 Skill이 적용되는가를 선언하는 조건. 발견·선택의 평가 대상. 경량 메타데이터다.
- Glossary 추가 요청: Skill Body (지시 본문) — Skill 수행 절차. 선택된 뒤에만 로드된다.
- Glossary 추가 요청: Skill I/O Contract (입력/출력 계약) — Skill이 받는 입력과 내는 출력의 계약. 재사용성의 기반.
- Glossary 추가 요청: SkillInterface — Skill이 구현하는 공통 계약 식별자. 교체는 동일 계약 내에서만 성립한다.

**타 spec 조율:**

- **08/10 조율 필요 — Plugin 배포에 포함된 Skill.** Plugin이 Skill을 배포 단위에 포함하는 경우(ROADMAP v0.8, ARCHITECTURE 8)의 경계 정합이 필요하다. Skill의 정의·등록·발견·호출 계약은 09가 소유하고, 배포·번들 계약은 10이 소유한다. 겹치는 지점(Plugin에 번들된 Skill의 등록 경로)의 정확한 형태는 specs/10-plugins.md와 조율한다. 10의 내용을 추측하지 않았다.
- **08/10 조율 필요 — 이벤트 기반 Skill 호출.** Hooks(이벤트 기반 확장)와 Skills(능력 단위)는 상호 독립 서브시스템이다 (ROADMAP v0.8). Skill 호출이 이벤트로 트리거되는 경계가 존재한다면 specs/08-hooks.md와 조율한다. 08의 내용을 추측하지 않았다.
- **01 조율 필요 — Failure Report enum 소유 경계.** Skill 특화 연산(Discover&Select / Load / Invoke)의 사유 코드는 09가 소유하고, 등록 실패 사유(ContractMismatch, DuplicateId)는 01 §3.2-D enum을 상속한다(§3.2-C). 01 §3.2-D enum을 Skill 사유로 확장할지, 09가 별도 enum을 소유할지 specs/01-runtime.md와 정합 확인이 필요하다. 현재 설계는 구조 재사용 + Skill 사유 코드 09 소유다.

**내부 미확정:**

- **OQ-S1 (비차단) — 발견 모호성 해소 규칙.** 다수 Skill이 동일 트리거로 매칭될 때의 선택 규칙(우선순위·명시 호출 등) 상세는 미확정이다. 결정적이어야 한다는 제약(INV-7)과 실패 사유(AmbiguousSelection)만 확정했다. 상세 규칙은 Advisor 결정 대상이며, 이 항목은 Draft를 막지 않는다.

**Component→Layer 매핑:**

- 이 spec은 §2에서 Skills를 "Runtime Layer의 Module 시스템 위 확장 서브시스템, Agent Layer가 소비"로 선언했다. 최종 Component→Layer 매핑은 Glossary §9-OQ6 흐름에 따라 Wave 3에서 Advisor가 통합·검증한다.

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 3.2(Modular), 3.6(Token Efficiency), 6(Skills = Component), 8(본체 재작성 없는 확장)과 01·02의 계약에 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

- OQ-S1 결정: 모호성 해소 순서 = 명시 호출 > 가장 구체적인 트리거 매칭 > 그래도 모호하면 AmbiguousSelection 실패·에스컬레이션. 상세 규칙은 v0.8 구현 시 정밀화 가능 (계약 골격 확정).
- Failure Report enum 소유 결정: 구조는 01 §3.2-D 재사용, 연산별 사유 코드는 각 spec 소유. 01 enum은 01 연산 전용으로 유지 (01과 정합 확인).
- 08/10 조율: Plugin에 번들된 Skill의 등록 경로는 10 §3.1 Activate가 01 Register를 경유하므로 09 등록 계약과 동일 — 모순 없음.
- Glossary 추가 요청 5건 승인 — Glossary §3.2-J 반영.
