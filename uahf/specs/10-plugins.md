# specs/10-plugins — Plugins Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05 · 2026-07-26 정합(격리 개정 — 슬림화·앵커 90ca19c))
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Plugins는 UAHF의 배포 단위다.

ARCHITECTURE.md 8은 "새로운 기술은 Adapter 또는 Plugin만 추가하면 된다"고 선언한다. Plugins는 그 "추가"의 규격이다.

## 이 컴포넌트가 해결하는 문제

- 새 기능을 넣으려면 본체를 고쳐야 하는 문제. 본체 수정 없이 추가로만 확장한다.
- 여러 Module과 확장 요소가 흩어져 함께 배포되지 못하는 문제. 하나의 자기완결(self-contained) 단위로 묶는다.
- 확장이 프로젝트마다 재구현되는 문제. contract에만 의존하는 재사용 가능한 배포 단위를 만든다.

## 책임 (1~3문장)

Plugins는 하나 이상의 Module(및 확장 요소)을 묶어 배포하는 단위의 규격이다.

Plugins는 설치·활성화·제거 계약을 정의하며, 활성화는 Runtime의 Register/Resolve 계약(specs/01-runtime.md §3.1-A)을 경유한다.

## Non-Goals

- Module 시스템(등록·해소·교체)을 정의하지 않는다 — specs/01-runtime.md 소관이다. Plugins는 그 계약을 확장점으로 소비한다.
- Hook의 이벤트 계약을 정의하지 않는다 — specs/08-hooks.md 소관이다.
- Skill의 능력 계약을 정의하지 않는다 — specs/09-skills.md 소관이다.
- Agent 역할 경계를 정의하지 않는다 — specs/02-agent.md 소관이다. Plugins는 그 경계를 침범하지 않는 제약만 진다.
- 특정 AI·패키지 포맷·배포 채널을 정의하지 않는다 — Adapter Binding(§4) 소관이다.

---

# §2. Position

- 아키텍처 상 위치: Core Component "Plugins" (Glossary §3.2-D)의 규격 문서다. Plugins는 특정 Layer의 지층이 아니라 Runtime의 Module 계약 위에서 동작하는 확장·배포 규격이다.
- Plugins는 Runtime Layer의 Module 등록/교체 계약을 확장점으로 사용한다 (01 §2 dependents 기록과 정합).

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 8 Future Direction("Adapter 또는 Plugin만 추가"), 3.2 Modular, 5.1 Memory 단일 Port.
- specs/00-glossary.md (실재, Frozen) — 모든 용어의 정본. 특히 §3.2-D Plugins, §3.2-I Runtime 계약 용어.
- specs/TEMPLATE.md (실재, Frozen) — 문서 구조와 DoD.
- specs/01-runtime.md (실재, Frozen) — Module 시스템·Manifest·Register/Resolve/Replace·Config·INV-4. Plugins가 소비하는 계약의 정본.
- specs/02-agent.md (실재, Frozen) — 역할 경계(§3.2-A)와 Memory 단일 Port(INV-8). Plugins가 침범하지 못하는 경계.
- .claude/AGENT.md (실재) — Agent 공통 규약.
- ROADMAP.md v0.8 (실재) — Extension System 완료 조건과 산출물.

(상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·01·02·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`. 종전 "Review"·"Adopted" 표기는 작성 시점 기록이었다.)

## 이 spec에 의존하는 spec (dependents)

- 현재 이 spec에 의존하는 spec은 식별되지 않는다.
- specs/08-hooks.md, specs/09-skills.md는 상호 독립 확장 서브시스템이며 Plugins의 dependents가 아니다. Plugin이 Hook·Skill을 "포함 요소"로 배포하는 시나리오의 상세 정합은 §9 조율 항목이다.

## 순환 의존

없다. Plugins는 01·02에 의존하고(10 → 01, 10 → 02), 01·02는 10에 의존하지 않는다. 의존은 항상 확장 규격 → 기반 계약 방향이다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 AI·환경 의존 실현은 §4에 둔다.

Plugins는 두 가지 계약을 정의한다.

- Plugin 수명주기 계약 — 설치·활성화·제거 (§3.1)
- Plugin Manifest 계약 — 배포 서술자 (§3.2-A)

"본체"는 이 spec에서 다음을 뜻한다: Core 디렉터리의 기존 계약, 기존 spec, 이미 등록된 Module. Plugin 설치는 본체를 수정하지 않고 오직 추가로만 확장한다.

---

## 3.1 Interface

Plugins는 다음 연산을 노출한다. 모든 연산의 실패는 공통 Failure Report(§3.2-B) 구조로 보고한다.

**Install**
- 입력: self-contained Plugin bundle 1건 + Plugin Manifest(§3.2-A).
- 출력: 설치 결과 — 설치된 plugin id. 상태는 registered-but-inactive.
- 완료 조건: (1) 본체 수정 0건 (INV-1). (2) Manifest의 `frameworkCompat`가 현재 Framework 버전을 포함한다. (3) `dependsOn` Plugin이 모두 이미 설치되어 있다. (4) `id`가 유일하다.
- 실패 보고: reason = `IncompatibleFramework` | `MissingDependency` | `DuplicateId` | `BodyMutation` | `NotSelfContained`.

**Activate**
- 입력: 설치된 plugin id.
- 출력: 활성화 결과 — 등록된 module id 목록.
- 완료 조건: `provides`의 각 Module Manifest가 Runtime Register(01 §3.1-A)로 등록되고, `requires` contract가 모두 Resolve(01)된다. 활성화는 Register/Resolve 계약으로만 성립한다 (INV-2).
- 실패 보고: reason = `ContractMismatch` | `UnresolvedContract` | `DuplicateId`.

**Deactivate**
- 입력: 활성 plugin id.
- 출력: 비활성화 결과.
- 완료 조건: `provides`의 각 Module이 활성화의 역순으로 비활성화되고, 그 contract 바인딩이 해제된다. 계약 소비자 참조가 다른 Plugin이 제공한 것이면 침범하지 않는다.
- 실패 보고: reason = `DeactivateIncomplete`, location = 실패한 module id.

**Remove**
- 입력: 설치된(가능하면 비활성) plugin id.
- 출력: 제거 결과.
- 완료 조건: Plugin이 설치·활성화 중 추가한 모든 산출물(등록 Module, 배치 파일, 배선)이 제거되고 잔여물 0. 본체는 설치 이전 상태와 동일하다 (INV-3). 다른 Plugin이 이 Plugin에 `dependsOn`으로 의존하면 제거를 거부한다.
- 실패 보고: reason = `ResidueDetected` | `DependentExists`.

주의: 개별 Module의 등록 해제(Deregister)는 Plugin 제거의 전제다. 01 §3.1-A는 Register/Resolve/Replace와 Shutdown(전체 역순 Deactivate)만 정의하고 Plugin 단위의 개별 Module 등록 해제 연산을 노출하지 않는다. Deactivate/Remove가 요구하는 이 연산의 소유·정합은 §9 조율 항목이다.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)과 물리 배포 채널은 Adapter Binding(§4)이 정한다.

### A. Plugin Manifest

Plugin의 배포 서술자다. 필드는 01 §3.2-A Module Manifest와 정합을 유지한다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Plugin 고유 식별자. 안정적(stable)이어야 설치·제거·의존 해소의 기준이 된다. Module Manifest `id`와 동일한 안정성 규칙(01 INV-7). | 예 |
| `version` | Plugin 버전. | 예 |
| `provides` | 이 Plugin이 포함·배포하는 요소 목록. 최소 1건. 각 항목은 Module Manifest(01 §3.2-A) 1건, 또는 확장 요소(Hook/Skill 등) 참조다. 확장 요소의 상세 서술은 08/09 소관이며 여기서는 "포함 요소" 수준으로만 참조한다. | 예 |
| `requires` | 이 Plugin이 활성화되기 위해 Runtime에서 Resolve되어야 하는 contract id 목록. Module Manifest `requires`와 동일 의미(contract id 목록). | 아니오(기본 없음) |
| `dependsOn` | 의존하는 다른 Plugin id 목록. 해당 Plugin이 먼저 설치·활성화되어야 한다. | 아니오(기본 없음) |
| `frameworkCompat` | 호환 Framework 버전 범위. 이 범위 밖에서는 Install을 거부한다. | 예 |

주의: Plugin Manifest는 새로운 Config scope를 도입하지 않는다. 포함 Module의 Config 스키마(`configSchema`)는 각 Module Manifest가 그대로 소유하며, Config는 Global/Project/Module(01 §3.2-B)로 유지된다 (INV-7).

### B. Failure Report

모든 Plugins 연산의 공통 실패 보고 구조다. 01 §3.2-D Failure Report와 필드 정합을 유지한다.

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Install / Activate / Deactivate / Remove). |
| `target` | 대상 (plugin id, module id, contract id). |
| `reason` | 사유 코드 (IncompatibleFramework / MissingDependency / DuplicateId / BodyMutation / NotSelfContained / ContractMismatch / UnresolvedContract / DeactivateIncomplete / ResidueDetected / DependentExists / IsolationViolation). |
| `location` | 실패 지점 참조 (Manifest 필드, module id, 침범 경계). |

`ContractMismatch` / `UnresolvedContract` / `DuplicateId`는 01 §3.2-D의 사유 코드를 그대로 재사용한다. `IsolationViolation`은 §3.3 격리 불변(INV-4/5/6) 위반의 공통 사유 코드다.

---

## 3.3 Invariants

- **INV-1 (본체 불가침).** Plugin 설치·활성화·제거는 본체(Core 디렉터리의 기존 계약, 기존 spec, 기존 Module)를 수정하지 않는다 (ROADMAP v0.8 "본체 코드/규격 수정 없이 확장"). 확장은 오직 추가로만 이뤄진다.
- **INV-2 (Register/Resolve 경유).** Plugin 활성화는 포함 Module을 Runtime Register로 등록하고 그 contract를 Resolve하는 것으로만 성립한다 (01 §3.1-A). Plugins는 독자적 등록·해소 경로를 만들지 않는다.
- **INV-3 (잔여물 0).** Plugin 제거 후, 그 Plugin이 추가한 모든 산출물이 사라지고 본체는 설치 이전 상태와 동일하다.
- **INV-4 (Core AI 비의존 유지).** Plugin은 Core 디렉터리에 AI 의존 요소를 주입하지 않는다 (01 INV-4). AI 의존 실현은 Adapter 경계에 둔다.
- **INV-5 (Memory 단일 Port).** Plugin이 포함하는 어떤 Module도 Memory Service Interface(단일 Port)를 우회해 영속성 백엔드에 직접 접근하지 않는다 (ARCHITECTURE 5.1, 02 INV-8).
- **INV-6 (역할 경계 불가침).** Plugin은 Agent 역할 경계(02 §3.2-A)를 재정의·우회하지 않는다. 포함된 Agent Module도 02의 역할 계약과 Invariants를 그대로 따른다.
- **INV-7 (Config scope 불변).** Plugin은 새로운 Config scope를 도입하지 않는다. Config는 Global/Project/Module(01 §3.2-B)로 유지되고, 포함 Module은 자신의 configSchema를 그대로 소유한다.
- **INV-8 (자기완결성).** Plugin은 자신의 Manifest·포함 요소를 하나의 경계 안에 두고, 선언되지 않은 본체 내부 경로·구현에 은닉 의존하지 않는다. 의존은 Manifest의 `requires`(contract)·`dependsOn`(plugin)으로만 선언된다.
- **INV-9 (안정 식별자).** Plugin `id`는 안정적이어야 한다. 설치·제거·의존 해소가 이 안정성에 의존한다 (01 INV-7과 정합).
- **INV-10 (AI 비의존 계약).** §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 실현은 §4에 둔다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다. §3의 추상 계약을 Claude Code 표면에 다음과 같이 바인딩한다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| Plugin bundle | Claude Code plugin 디렉터리 — self-contained 배포 단위. |
| Plugin Manifest(§3.2-A) 직렬화 | Markdown + front-matter 또는 설정 파일. Module Manifest 직렬화(01 §4.1)와 동일 관례. |
| 포함 Module 등록 (Activate) | 01 §4.1의 Register 바인딩 경유 — `.claude/agents/`, `.claude/commands/`, `.claude/hooks/`, `.claude/skills/` 확장 표면에 등록. |
| Install | Plugin 디렉터리 배치 (본체 파일 미수정). |
| Deactivate / Remove | 등록 배선 해제와 Plugin 디렉터리 제거. |
| 포함 Module의 AI 비의존 구현 | Core-side module 디렉터리(예: `framework/plugins/`, 01 §4.1)에 위치. AI 의존 요소 0건 유지. |
| AI 의존 산출물 | `.claude/` 등 Adapter 경계로 격리 (INV-4). |
| 배포 채널 | Claude Code plugin 설치 메커니즘(marketplace 등). |

Plugin bundle은 그 내부에서도 Core/Adapter 경계를 유지한다. AI 비의존 Module 구현과 AI 의존 바인딩을 물리적으로 분리해 담는다.

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부. §3 Core Contract는 유지되고 아래만 교체된다.

1. **Plugin bundle/Manifest 직렬화** — Claude Code plugin 디렉터리 + front-matter → 대상 환경의 패키지·서술자 포맷.
2. **포함 Module 등록 표면** — `.claude/{agents,commands,hooks,skills}` → 대상 환경의 Module 로더·확장 등록 메커니즘.
3. **Install/Activate/Deactivate/Remove의 물리 실현** — 디렉터리 배치·배선·제거 → 대상 환경의 패키지 매니저.
4. **배포 채널** — Claude Code plugin 설치 메커니즘 → 대상 환경의 배포·레지스트리 채널.
5. **확장 요소(Hook/Skill) 표면 바인딩** — 08/09의 §4 소관. Plugins는 참조만 하고 정의하지 않는다.

이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다.

---

# §5. Memory Access (해당 시)

해당 없음.

Plugins는 Memory를 직접 읽거나 쓰지 않는다. Plugins는 배포·수명주기 계약이며, ARCHITECTURE 5.1의 Memory 소비자 목록(Agent, Loop, Workflow, Verifier)에 포함되지 않는다.

단서 (불변 규칙): Plugin이 포함하는 Module이 Memory에 접근할 수는 있으나, 그 경우에도 접근 경로는 Memory Service Interface(단일 Port) 하나뿐이다 (INV-5, 02 INV-8). 그 접근 계약은 02·04 소관이며, Plugins spec은 Memory 내용에 접근하지 않는다.

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다. 모두 Lesson 후보다.

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| 설치가 본체(기존 계약·spec·Module)를 수정 | Install 거부. Failure Report(reason=BodyMutation). INV-1 위반. | 예 |
| `frameworkCompat` 범위 밖 설치 시도 | Install 거부. reason=IncompatibleFramework. | 예 |
| `dependsOn` Plugin 미설치 | Install/Activate 거부. reason=MissingDependency. | 예 |
| `requires` contract 미해소 | Activate 실패. reason=UnresolvedContract (01 재사용). | 예 |
| plugin id 충돌 | Install 거부. reason=DuplicateId. | 예 |
| 제거 후 잔여물 발견 | Remove 미완료. reason=ResidueDetected. INV-3 위반. | 예 |
| 의존하는 다른 Plugin이 존재하는데 제거 시도 | Remove 거부. reason=DependentExists. | 예 |
| 포함 Module이 Memory 단일 Port 우회 | 격리 위반. reason=IsolationViolation. INV-5 위반. | 예 |
| 포함 요소가 Core 디렉터리에 AI 의존 요소 주입 | 격리 위반. reason=IsolationViolation. INV-4 위반. | 예 |
| Plugin이 역할 경계를 재정의·우회 | 격리 위반. reason=IsolationViolation. INV-6 위반. | 예 |
| 선언되지 않은 본체 내부 경로에 은닉 의존 | 배포 규격 위반. reason=NotSelfContained. INV-8 위반. | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.8 완료 조건("본체 코드/규격 수정 없이 확장", "추가만 하여 동작이 확장")과 정렬한다.

- **추가만 확장 시연.** 레퍼런스 Plugin 1개를 Install·Activate만 하여 새 기능(contract 바인딩)이 동작함을 보인다. 본체(Core 디렉터리·기존 spec·기존 Module)의 diff가 0건임을 보인다 (INV-1).
- **Register/Resolve 경유 시연.** Activate 시 포함 Module이 Runtime Register로 등록되고, 그 contract가 Resolve로 반환됨을 보인다 (INV-2, 01 §3.1-A).
- **잔여물 0 시연.** Remove 후 파일·등록·배선이 설치 이전 상태와 동일(잔여물 0)함을 보인다 (INV-3).
- **격리 시연.** Plugin이 Core 디렉터리에 AI 의존 요소를 주입하지 않고(INV-4), 포함 Module의 Memory 접근이 단일 Port만 경유하며(INV-5), 역할 경계를 재정의하지 않음(INV-6)을 보인다.
- **자기완결 시연.** Plugin 경계 밖 본체 내부 경로에 대한 은닉 의존이 0건임을 보인다 (INV-8).
- **AI 비의존 시연.** §3 본문에 특정 AI 모델·실행 환경 의존 토큰이 0건임을 보인다 (INV-10, DoD-3).

## 검증 방법

- Verifier가 Install 전후 본체(Core 디렉터리·기존 spec·기존 Module) diff = 0을 확인한다.
- Verifier가 Activate 시 Runtime Register/Resolve 호출과 반환 핸들을 확인한다.
- Verifier가 Remove 후 잔여물 스캔 = 0을 확인한다.
- Verifier가 포함 요소의 Memory 접근 경로가 단일 Port임을, Core 배치 요소가 AI 비의존임을 확인한다.
- Verifier가 §3 본문을 스캔해 AI 의존 토큰(모델명·제품 기능명)이 0건임을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 단일 Module을 묶은 Plugin의 전체 수명주기**

새 능력(예: 새 contract `ReportExporterInterface`)을 제공하는 Plugin이 있다.

- Plugin Manifest: `id` = report-exporter, `version` = 1.0, `provides` = [Module Manifest(contract=ReportExporterInterface)], `requires` = [], `dependsOn` = [], `frameworkCompat` = 현재 Framework 버전 포함.
- Install: bundle을 배치한다. 본체 파일은 수정되지 않는다 (INV-1). frameworkCompat 만족, id 유일 → 성공(registered-but-inactive).
- Activate: `provides`의 Module Manifest를 Runtime Register(01)로 등록한다. 이후 Resolve(ReportExporterInterface)가 그 Module 핸들을 반환한다 (INV-2). 새 기능이 동작한다.
- Remove: 등록을 해제하고 bundle을 제거한다. 본체는 설치 이전과 동일, 잔여물 0 (INV-3).

**예 2 — 여러 요소를 묶은 Plugin (포함 요소 추상)**

한 Plugin이 Module 1개와 확장 요소(Hook 또는 Skill) 1개를 함께 배포한다.

- Plugin Manifest: `provides` = [Module Manifest 1건, 확장 요소 참조 1건].
- Plugins spec은 이 확장 요소를 "포함 요소" 수준으로만 다룬다. 확장 요소의 등록·이벤트·능력 계약 상세는 specs/08-hooks.md, specs/09-skills.md 소관이며 정합은 §9 조율 항목이다.
- Activate 시 Module 부분은 Runtime Register(01)로 등록되고, 확장 요소 부분의 등록 표면 바인딩은 08/09의 §4가 정의한다. Plugins는 묶어 배포하고 함께 제거(잔여물 0)하는 계약만 소유한다.

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**Glossary 추가 요청** — 용어 2종(Plugin 개별 배포 단위 · Plugin Manifest)은 00-glossary §3.2-J-10 정본 등재 완료(요청 2건 전부 Advisor 승인). 상세 필드의 정본은 이 spec §3·§3.2-A가 유지한다.

**타 spec 조율:**

- 01-runtime 조율 — Plugin 제거가 요구하는 개별 Module 등록 해제(Deregister) 연산 — 해소(01 §3.1-A에 Deregister 연산 추가 승인·반영 — Registry 수명주기는 Runtime 소유이므로 01이 소유하고 Plugins는 우회 정의하지 않는다. Plugins의 Deactivate/Remove(잔여물 0, INV-3)는 이 연산 위에서 성립한다. 01 §9 결정 기록 동일 기재 · 상세 = 결정 기록 소절·git 앵커 90ca19c).
- 08-hooks / 09-skills 조율 — 해소(번들된 Hook/Skill의 등록은 각각 08 §3.1-C·09 §3.1-A 계약을 따르며 10은 배포·제거만 소유 — 모순 없음 확인. 이 spec은 `provides`의 확장 요소를 "포함 요소" 수준으로만 추상 정의했고, 등록 표면·이벤트·능력 계약은 08·09 소관이다 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

**설계 확인 요청:**

- OQ-P1: Config scope에 Plugin scope 부재 — 해소(승인 — Plugin scope 미도입 확정. Config는 Global/Project/Module(01 §3.2-B) 유지(INV-7)이며 포함 Module의 configSchema는 각 Module Manifest가 소유한다. 01 Config 계약과 모순 없음 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 8(Adapter/Plugin 확장)·3.2(Modular)·5.1(Memory 단일 Port), 01 INV-4, 02 §3.2-A/INV-8과 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

- 01 Deregister 조율 해소: 01 §3.1-A에 Deregister 연산 추가 승인·반영 (01 §9 결정 기록 참조). Deactivate/Remove는 이 연산 위에서 성립한다.
- OQ-P1 승인 — Plugin scope 미도입(Config는 Global/Project/Module 유지) 확정. 01 Config 계약과 모순 없음.
- 08/09 조율: 번들된 Hook/Skill의 등록은 각각 08 §3.1-C·09 §3.1-A 계약을 따르며 10은 배포·제거만 소유 — 모순 없음 확인.
- Glossary 추가 요청 2건 승인 — Glossary §3.2-J 반영.

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 항목(01 Deregister 조율 · 08/09 조율 · OQ-P1)의 원문+답 이중 잔존 1줄화, Glossary 추가 요청 블록의 등재 완료 1줄화, §2 stale 상태 표기(Review/Adopted → Frozen)·"동시 작성 중" 서술 현행 정정. 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — §3 전체·§6·§7·§8 무촉, dependents(§2 = 식별된 dependent 0 · 조율 08·09) 참조 영향 0(정책 §4-a·§4-c). 종전 문면 = git 앵커 90ca19c.
