# specs/12-scaffold — Scaffold Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05)
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Scaffold는 신규 프로젝트에 UAHF를 부트스트랩(설치·초기화)하는 도구다 (Glossary §3.2-D).

## 이 컴포넌트가 해결하는 문제

- UAHF를 손으로 설치하면 프로젝트마다 구조가 제각각이 된다.
- 규약 문서·Agent 정의·Config·specs 디렉터리 중 하나만 누락되어도 Runtime Bootstrap이 실패한다.
- 사람이 매번 동일한 설치 절차를 반복한다.
- 기존 프로젝트에 설치할 때 사용자 파일을 덮어쓸 위험이 있다.

## 책임 (1~3문장)

Scaffold는 대상 프로젝트에 UAHF를 설치·초기화하여, 설치 직후 Runtime Bootstrap(specs/01-runtime.md §3.1-C)이 성공하고 루프가 동작할 수 있는 프로젝트 구조를 만든다.

Scaffold는 그 구조가 유효함을 스스로 검증하고, 재실행 시 멱등하며, 제거 시 안전하다.

## Non-Goals

- Runtime Bootstrap 계약을 정의하지 않는다 — specs/01-runtime.md §3.1-C 소관이다. Scaffold는 Bootstrap이 성공할 수 있는 상태만 만든다.
- Agent 역할의 내부 계약(입력/출력/보고 포맷)을 정의하지 않는다 — specs/02-agent.md 소관이다. Scaffold는 정의의 설치 자리만 만든다.
- 루프의 단계 전이·구동 계약을 정의하지 않는다 — specs/03-loop.md 소관이다.
- Plugin 설치를 정의하지 않는다 — specs/10-plugins.md 소관이다. Scaffold는 초기 설치만 담당한다.
- Harness 실행 골격의 내부를 정의하지 않는다 — specs/13-harness.md 소관이다. Scaffold는 설치 도구, Harness는 설치되는 실행 골격이다 (§9-OQ2).
- 물리 경로·직렬화 포맷·특정 AI 실행 환경을 정의하지 않는다 — Adapter Binding(§4) 소관이다.

---

# §2. Position

- 아키텍처 상 위치: Core Component "Scaffold" (Glossary §3.2-D)의 규격 문서다.
- Layer 귀속: 사용자 대면 호출 표면을 Presentation Layer에 귀속하는 것을 제안한다. 근거 — ROADMAP v0.9가 Scaffold를 Presentation 최소 기능과 함께 묶는다. 단, Scaffold의 산출물(설치 구조)은 Runtime이 Bootstrap하는 대상이므로 실행 스택의 한 위치에 고정되지 않는 설치 단계 도구라는 해석도 가능하다. Layer 확정은 Glossary §9-OQ6 흐름에 따라 §9-OQ1에서 Advisor에게 에스컬레이션한다. 이 spec은 확정 전까지 Layer를 단정하지 않는다.

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 3.2 Modular, 5 스택, 6 Core Components.
- specs/00-glossary.md (실재, Review) — 모든 용어의 정본. 특히 §3.2-D Scaffold 정의.
- specs/TEMPLATE.md (실재, Adopted) — 문서 구조와 DoD.
- specs/01-runtime.md (실재, Review) — Bootstrap 계약(§3.1-C)과 Config 스코프(§3.2-B).
- specs/02-agent.md (실재, Review) — Agent 정의의 계약과 역할 경계.
- .claude/AGENT.md (실재) — Agent 공통 규약.
- ROADMAP.md v0.9 (실재) — Scaffold 완료 조건("설치 → 루프 동작")과 산출물.

## 이 spec에 의존하는 spec (dependents)

- 현재 확정된 hard dependent는 없다.
- specs/11-adapters.md — 이 spec의 이식 교체 지점(§4.2)을 Adapter Interface로 정식화한다 (11 조율, §9).
- specs/13-harness.md — Scaffold가 Harness를 설치하는 관계. 조율 중이다 (§9-OQ2). 13의 내용을 추측·인용하지 않았다.

## 순환 의존

없다. 이 spec의 참조 방향은 12 → 01, 12 → 02(설치 대상 계약을 참조)이며, 01·02는 12에 의존하지 않는다. 01의 dependents 목록에도, 02의 dependents 목록에도 12는 없다. 따라서 순환은 형성되지 않는다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 환경 의존 실현은 §4에 둔다.

Scaffold는 세 연산과 세 데이터 계약을 정의한다.

- 설치·검증·제거 연산 (§3.1)
- Project Template · Install Manifest · 설치 검증 체크리스트 (§3.2)

---

## 3.1 Interface

Scaffold는 다음 연산을 노출한다. 모든 연산의 실패는 공통 Failure Report(§3.2-D) 구조로 보고한다.

### Install (설치·부트스트랩)

- 입력:
  - `target` — 대상 프로젝트. 빈 프로젝트 또는 기존 프로젝트.
  - `moduleSelection` — 설치할 Module 집합. Modular 원칙에 따라 필요한 모듈만 선택한다 (ARCHITECTURE 3.2). 이 집합은 Runtime Bootstrap 필수 계약을 만족하는 최소 집합을 반드시 포함해야 한다 (§3.3 INV-2).
  - `options` — 설치 옵션. 기존 파일 처리 정책(보존/강제 덮어쓰기)을 포함한다. 기본은 보존이다.
- 출력: UAHF가 설치된 프로젝트 구조와 Install Manifest(§3.2-B).
- 완료 조건: 설치 직후 Runtime Bootstrap(01 §3.1-C)이 `state = Ready`(또는 필수 계약만 충족되고 선택 계약이 일부 누락되면 `Degraded`)로 성공하고, 설치 검증 체크리스트(§3.2-C) 전 항목을 통과한다.
- 실패 보고: Failure Report. reason = `TargetNotWritable` | `ConflictWithExisting` | `ModuleSelectionInvalid` | `BootstrapWouldFail`.

### VerifyInstall (설치 자가 검증)

- 입력: 설치된 프로젝트 구조와 Install Manifest.
- 출력: 설치 검증 결과 — 체크리스트(§3.2-C) 항목별 통과 여부.
- 완료 조건: 체크리스트 전 항목이 통과한다.
- 실패 보고: Failure Report. reason = `IncompleteInstall` | `BootstrapWouldFail`, location = 실패한 체크 항목.

### Uninstall (제거)

- 입력: 설치된 프로젝트 구조와 Install Manifest.
- 출력: 제거 결과 — 제거된 산출물 목록과 잔여물 목록.
- 완료 조건: Install Manifest의 `installedArtifacts`만 제거되고, `preservedPaths`(사용자 소유 기존 파일)는 보존되며, 잔여물이 보고된다.
- 실패 보고: Failure Report. reason = `UninstallResidue`, location = 잔여 경로.

---

## 3.2 Data Format

포맷은 추상 스키마로 정의한다. 직렬화 형식(파일 형태·문법)과 물리 경로는 Adapter Binding(§4)이 정한다.

### A. Project Template (프로젝트 템플릿)

Scaffold가 설치하는 구조의 추상 정의다. 물리 경로는 §4가 정한다. 여기서는 AI 비의존 구성 요소만 규정한다.

| 템플릿 구성 요소 | 의미 | 필수 | 정합 기준 |
|---|---|---|---|
| 규약 문서 (Convention docs) | Agent 행동을 규율하는 상위 규약과 프로젝트 진입 규약. | 예 | AGENT.md, 프로젝트 진입 규약 (물리 경로는 §4) |
| Agent 정의 (Agent definitions) | Advisor / Planner / Worker / Verifier 역할 정의의 초기 설치 자리. | 예 | 02 §4.1 |
| Config — Global scope 초기화 | Framework 전역 기본값. 병합 최저 우선순위. | 예 | 01 §3.2-B |
| Config — Project scope 초기화 | 프로젝트 단위 override의 초기값. | 예 | 01 §3.2-B |
| specs 디렉터리 | spec 문서 배치 자리. | 예 | — |
| Core / Adapter 경계 | AI 비의존 Core 디렉터리와, 그와 물리적으로 분리된 Adapter Binding 산출물 경계. | 예 | 01 §3.2-E |

주의: Module scope Config는 각 Module이 소유하므로 Scaffold의 초기화 대상이 아니다 (01 §3.2-B). Scaffold는 Global·Project 두 스코프만 초기화한다.

### B. Install Manifest (설치 매니페스트)

Scaffold가 설치한 내용의 서술자다. 멱등성(INV-4)과 제거(INV-5)의 기준이 된다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `frameworkVersion` | 설치된 UAHF Framework 버전. | 예 |
| `specVersion` | 설치 기준이 된 spec 기준선 버전. | 예 |
| `installedModules` | `moduleSelection` 해소 결과 — 실제 설치된 Module 집합. | 예 |
| `installedArtifacts` | Scaffold가 생성·소유한 산출물 목록. 제거·멱등성 판정의 기준. | 예 |
| `preservedPaths` | 설치 시 보존된 기존 사용자 파일 목록. | 예 |
| `timestamp` | 설치 시점. | 아니오 |

`frameworkVersion`과 `specVersion`의 표기는 필수다 (INV-7). 두 값의 직렬화 형식과 구체 값은 §4 소관이다.

### C. 설치 검증 체크리스트 (Install Verification Checklist)

설치 결과가 유효함을 판정하는 계약이다. VerifyInstall(§3.1)이 이 체크리스트를 실행한다.

- **CK-1.** Project Template(§3.2-A)의 모든 필수 구성 요소가 존재한다.
- **CK-2.** `moduleSelection`이 Runtime Bootstrap 필수 계약을 만족하는 최소 집합을 포함한다 (01 §3.1-C).
- **CK-3.** Config Global·Project 스코프가 초기화되어 있고 01 §3.2-B 스키마와 일치한다.
- **CK-4.** 설치 직후 Runtime Bootstrap(01 §3.1-C)이 `Ready` 또는 `Degraded`로 성공한다.
- **CK-5.** Bootstrap 이후 Loop Engine이 최소 1 사이클을 구동한다 (ROADMAP v0.9 "루프 동작"). 구동 계약은 03 소관이며, Scaffold는 그 호출 결과만 판정한다.
- **CK-6.** 설치된 Core 디렉터리에 AI 의존 요소가 0건이다 (01 INV-4와 정합).
- **CK-7.** Install Manifest가 존재하고 `frameworkVersion`·`specVersion`을 표기한다.
- **CK-8.** 기존 사용자 파일이 보존되었다 — `preservedPaths`와 실제 상태가 일치한다.

### D. Failure Report (실패 보고)

모든 Scaffold 연산의 공통 실패 보고 구조다.

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Install / VerifyInstall / Uninstall). |
| `target` | 대상 (프로젝트, 경로, module id, config 스코프). |
| `reason` | 사유 코드 (TargetNotWritable / ConflictWithExisting / ModuleSelectionInvalid / BootstrapWouldFail / IncompleteInstall / UninstallResidue). |
| `location` | 실패 지점 참조 (경로·체크 항목·module id). |

---

## 3.3 Invariants

- **INV-1 (Bootstrap 성공 상태 생성).** 성공한 Install의 결과는 항상 Runtime Bootstrap(01 §3.1-C)이 성공할 수 있는 상태다. Scaffold는 Bootstrap 계약을 재정의하지 않는다 (01 소유).
- **INV-2 (필요한 모듈만 / Modular).** Scaffold는 `moduleSelection`이 지정한 Module만 설치한다 (ARCHITECTURE 3.2). 단, 그 집합은 Runtime Bootstrap 필수 계약을 만족하는 최소 집합을 포함해야 한다. 미달이면 `ModuleSelectionInvalid`로 거부한다.
- **INV-3 (기존 파일 보호).** 기존 프로젝트에 설치할 때 Scaffold는 사용자 소유 기존 파일을 덮어쓰지 않는다. 충돌하는 파일은 보존하고 `preservedPaths`에 기록한다. 강제 덮어쓰기는 명시적 `options`를 요구한다.
- **INV-4 (멱등성).** 동일 입력으로 Install을 재실행하면 결과 구조는 동일하다. 이미 존재하는 Scaffold 산출물은 재생성하지 않으며, 사용자 수정본을 덮어쓰지 않는다.
- **INV-5 (제거 안전).** Uninstall은 `installedArtifacts`만 제거하고 `preservedPaths`는 보존한다. 제거 후 남는 잔여물은 `UninstallResidue`로 보고한다.
- **INV-6 (Core AI 비의존).** Scaffold가 설치하는 Core 디렉터리에 AI 의존 요소는 0건이다 (01 INV-4와 정합). AI·환경 의존 산출물은 Adapter Binding 경계(§4)에만 둔다.
- **INV-7 (버전 정합).** 모든 설치는 설치된 Framework 버전과 spec 기준선 버전을 Install Manifest에 표기한다.
- **INV-8 (경계 불가침).** Scaffold는 Bootstrap 계약(01), 루프 단계(03), Plugin 설치(10), Harness 실행 골격(13)을 정의하지 않는다. 이들이 성립할 수 있는 초기 구조만 설치한다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x 구현 형태는 Claude Code 위 self-hosting이다 (ROADMAP v0.9, ARCHITECTURE.md 3.1 "Claude는 첫 번째 Adapter"). §3의 추상 계약을 Claude Code 표면에 다음과 같이 바인딩한다.

| §3 계약 요소 | Claude Code 바인딩 |
|---|---|
| 규약 문서 설치 (§3.2-A) | `.claude/AGENT.md`, `.claude/CLAUDE.md` 초기화. |
| Agent 정의 설치 (§3.2-A) | `.claude/agents/{advisor,planner,worker,verifier}.md` (02 §4.1). |
| Config — Global scope 초기화 | 사용자·환경 전역 설정 파일 (01 §4.1). |
| Config — Project scope 초기화 | `.claude/CLAUDE.md`, `.claude/AGENT.md`, 프로젝트 설정 파일(settings.json 등) (01 §4.1). |
| specs 디렉터리 설치 | `specs/` 디렉터리 생성. |
| Core / Adapter 경계 설치 | `framework/core/`, `framework/runtime/` (Core), `framework/adapters/`, `.claude/` (Adapter Binding) (01 §4.1). |
| Install Manifest 직렬화 (§3.2-B) | 프로젝트 내 매니페스트 파일 (Markdown + front-matter 또는 설정 파일). |
| 버전 값 (`frameworkVersion` / `specVersion`) | 릴리스 시점의 Framework·spec 버전 문자열. |
| Runtime Bootstrap 호출 (CK-4) | Claude Code 세션/턴에서 Runtime Bootstrap 실행 (01 §4.1 수명주기 호스트). |
| Loop 1 사이클 구동 확인 (CK-5) | Loop Engine 구동 (구동 계약은 03 소관). |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부. §3 Core Contract는 유지되고 아래만 교체된다.

1. **규약 문서 위치·포맷** — `.claude/AGENT.md`, `.claude/CLAUDE.md` → 대상 환경의 규약·시스템 프롬프트 주입 방식 (02 SP-2).
2. **Agent 정의 위치·포맷** — `.claude/agents/*.md` → 대상 환경의 Agent 정의 메커니즘 (02 SP-1).
3. **Config 소스·위치** — 전역·프로젝트 설정 파일 → 대상 환경의 Config 메커니즘 (01 §4.2-2).
4. **Core / Adapter 디렉터리 규약** — `framework/`, `.claude/` → 대상 환경의 규약 (01 §4.2-5).
5. **Install Manifest 직렬화 포맷** — 매니페스트 파일 형태 → 대상 환경의 서술자 포맷.
6. **버전 값 표기 형식** — Framework·spec 버전 문자열의 형식 → 대상 환경의 버전 규약.
7. **Bootstrap·Loop 구동 호출 방식** — 세션/턴 실행 → 대상 환경의 실행 프로세스 (01 §4.2-4, 03 소관).

유지되는 것: §3.1 Install/VerifyInstall/Uninstall 연산, §3.2-A Project Template 추상 구성, §3.2-B Install Manifest 필드, §3.2-C 설치 검증 체크리스트, §3.3 Invariants.

이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다.

---

# §5. Memory Access (해당 시)

해당 없음.

Scaffold는 Memory를 읽거나 쓰지 않는다. Scaffold는 설치·초기화 도구로서 프로젝트의 Runtime Bootstrap 이전에 동작하며, 이 시점에는 Memory Service가 아직 구동되지 않는다. ARCHITECTURE 5.1의 Memory 소비자 목록(Agent, Loop, Workflow, Verifier)에 Scaffold는 포함되지 않는다.

단서 (불변 규칙, 01 §5 패턴 참조): Scaffold가 Memory Service를 하나의 Module로 설치·배선하는 경우에도, Scaffold는 배선만 수행하고 Memory 내용에는 접근하지 않는다. 접근 경로는 Memory Service Interface(단일 Port) 하나뿐이며 영속성 백엔드는 Adapter Layer 뒤에 둔다.

---

# §6. Failure Modes

모두 Lesson 후보다 (표의 마지막 열).

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| 대상에 쓸 수 없음 | Install 실패. Failure Report(reason=TargetNotWritable). | 예 |
| 요청 Module 집합이 필수 최소 집합 미달 | Install 거부. reason=ModuleSelectionInvalid (INV-2). | 예 |
| 기존 사용자 파일과 충돌 | 보존하고 preservedPaths 기록. 강제 옵션 없으면 덮어쓰지 않음 (INV-3). 강제 시 reason=ConflictWithExisting로 경고. | 예 |
| 설치 산출물 누락 | VerifyInstall 실패. reason=IncompleteInstall. | 예 |
| 설치 결과가 Bootstrap 필수 계약 미충족 | reason=BootstrapWouldFail. 설치 무효 판정 (INV-1). | 예 |
| 재실행 시 사용자 수정본 덮어쓰기 위험 | 멱등 규칙(INV-4)으로 재생성 회피. 사용자 수정본 보존. | 예 |
| 제거 후 잔여물 존재 | reason=UninstallResidue로 보고 (INV-5). | 예 |
| Core 디렉터리에 AI 의존 요소 혼입 | 경계 위반 (INV-6). CK-6 실패로 판정. | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.9 완료 조건("설치 → 루프 동작")과 정렬한다.

- **설치 → Bootstrap 시연.** 빈 프로젝트에 Install을 실행하면, 설치 직후 Runtime Bootstrap(01 §3.1-C)이 `Ready`(또는 `Degraded`)로 성공함을 보인다 (INV-1, CK-4).
- **루프 동작 시연.** Bootstrap 이후 Loop Engine이 최소 1 사이클을 구동함을 보인다 (ROADMAP v0.9; 구동 계약은 03 소관, CK-5).
- **필요한 모듈만 시연.** 요청한 `moduleSelection`만 설치되고, 그 집합이 Bootstrap 필수 계약을 만족함을 보인다 (INV-2, CK-2, Modular).
- **기존 파일 보호 시연.** 기존 프로젝트에 설치할 때 사용자 소유 파일이 보존되고 `preservedPaths`에 기록됨을 보인다 (INV-3, CK-8).
- **멱등성 시연.** 동일 입력으로 Install을 재실행해도 구조가 동일하고 사용자 수정본이 덮어써지지 않음을 보인다 (INV-4).
- **제거 안전 시연.** Uninstall이 `installedArtifacts`만 제거하고 `preservedPaths`를 보존하며 잔여물을 보고함을 보인다 (INV-5).
- **설치 검증 시연.** VerifyInstall이 체크리스트(§3.2-C) 전 항목 통과를 보고함을 보인다.
- **버전 표기 시연.** Install Manifest에 `frameworkVersion`·`specVersion`이 표기됨을 보인다 (INV-7, CK-7).
- **Core AI 비의존 시연.** 설치된 Core 디렉터리 전체를 스캔해 AI 모델명·제품 기능 참조가 0건임을 보인다 (INV-6, CK-6).
- **§3 AI 비의존 시연.** §3 본문에 특정 AI 모델·실행 환경 의존 토큰이 0건임을 보인다 (DoD-3).

## 검증 방법

- Verifier가 빈 프로젝트에 Install을 실행하고 곧바로 Runtime Bootstrap을 호출해 `state`를 확인한다.
- Verifier가 Bootstrap 이후 Loop 1 사이클 구동 결과를 확인한다 (03 계약 호출).
- Verifier가 VerifyInstall을 실행해 체크리스트(§3.2-C)를 항목별로 대조한다.
- Verifier가 Install 재실행 전후 구조 diff가 0이고 사용자 수정본이 보존됨을 확인한다.
- Verifier가 Uninstall 후 잔여물 목록과 `preservedPaths` 보존을 확인한다.
- Verifier가 Install Manifest의 `frameworkVersion`·`specVersion` 표기를 확인한다.
- Verifier가 설치된 Core 디렉터리에서 금지 토큰(특정 AI·모델명·제품 기능) 0건을 확인한다.
- Verifier가 §3 본문에 AI 의존 요소 0건임을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 빈 프로젝트 설치 → Bootstrap → 루프 동작 (ROADMAP v0.9 완료 조건)**

Install 입력:
- target: 빈 프로젝트
- moduleSelection: 최소 필수 집합 (Runtime Bootstrap 필수 계약 만족)
- options: 기본 (기존 파일 없음)

Install 결과:
- Project Template(§3.2-A) 전 구성 요소 설치 — 규약 문서, Agent 정의, Config(Global·Project 초기화), specs 디렉터리, Core/Adapter 경계.
- Install Manifest 생성 — frameworkVersion·specVersion·installedModules·installedArtifacts 기록.

설치 직후:
- Runtime Bootstrap(01 §3.1-C) 호출 → state=Ready.
- Loop Engine 최소 1 사이클 구동 → 통과.
→ ROADMAP v0.9 완료 조건 "설치 → 루프 동작" 충족.

**예 2 — 기존 프로젝트에 설치 (기존 파일 보호 + 멱등성)**

target에 사용자 소유 `README.md`와 기존 `specs/` 일부가 있다.
- Scaffold는 기존 파일을 덮어쓰지 않고 보존한다 (INV-3). 보존 대상은 preservedPaths에 기록된다.
- 누락된 UAHF 구성 요소만 추가 설치한다.
- 동일 입력으로 재실행하면 이미 설치된 산출물은 재생성하지 않는다 (INV-4). 구조 diff = 0.

**예 3 — 제거 (잔여물 처리)**

Uninstall 입력: 설치된 프로젝트 구조 + Install Manifest.
- Manifest.installedArtifacts만 제거한다.
- preservedPaths(사용자 파일)는 보존한다 (INV-5).
- 제거 후 남은 항목이 있으면 reason=UninstallResidue로 보고한다.

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

- **OQ-1 (Layer 귀속 확인 — Glossary §9-OQ6 흐름) — Scaffold의 Layer 귀속.**
  Scaffold는 Core Component(Glossary §3.2-D)다. 그러나 6개 Layer 중 어디에 귀속되는지는 Glossary가 아직 확정하지 않았다(§9-OQ6). 이 spec은 ROADMAP v0.9가 Scaffold를 Presentation 최소 기능과 함께 묶은 점에 근거해, Scaffold의 사용자 대면 호출 표면을 Presentation Layer에 귀속하는 것을 제안한다. 단, Scaffold의 산출물(설치 구조)은 Runtime이 Bootstrap하는 대상이므로 실행 스택의 특정 위치에 고정되지 않는 설치 단계 도구라는 해석도 가능하다. Advisor 확정을 요청한다. 확정 전까지 §2는 Layer를 단정하지 않는다.

- **OQ-2 (13-harness 조율 필요) — Scaffold와 Harness의 관계.**
  Scaffold는 설치 도구이고 Harness(specs/13-harness.md)는 설치되는 실행 골격이다. Scaffold의 설치 산출물 중 어디까지가 Harness의 최소 실행 골격에 해당하는지, 그리고 Scaffold가 Harness를 어떤 계약으로 설치하는지는 13과 조율이 필요하다. 13은 동시 작성 중이므로 이 spec은 13의 내용을 추측·인용하지 않았다. 관계 정의는 13 완성 후 확정한다.

- **OQ-3 (10-plugins 경계 확인) — 초기 설치 vs Plugin 설치.**
  Scaffold는 초기 설치만 담당하고 이후 Plugin 설치는 specs/10-plugins.md 소관이다. `moduleSelection`이 초기 설치 대상 Module 집합과 Plugin으로 추가되는 기능 묶음 사이의 경계를 어디에 두는지는 10과 조율이 필요하다. 10은 동시 작성 중이므로 이 spec은 10의 내용을 추측하지 않았다. 이 항목은 Frozen을 막지 않는다.

- **OQ-4 (03-loop 조율 — 비차단) — 설치 직후 루프 구동 진입점.**
  §3.2-C CK-5와 §7이 "설치 직후 루프가 동작함"을 완료 기준으로 삼는다. 루프의 구동·단계 전이 계약은 specs/03-loop.md 소관이다. 이 spec은 루프 구동 결과(1 사이클 통과)만 판정 대상으로 삼고 루프 내부를 정의하지 않았다. "설치 직후 루프 구동" 진입점의 정합을 03과 확인할 필요가 있다. 이 항목은 Frozen을 막지 않는다.

- **Glossary 추가 요청** (본 spec이 정의·형식화하지만 Glossary §3.2에 정본 항목이 없는 Scaffold 고유 계약 용어. Glossary §9-OQ6 흐름에 따라 정본화 요청):
  - Glossary 추가 요청: Project Template (프로젝트 템플릿) — Scaffold가 설치하는 구조의 추상 정의. 구성은 이 spec §3.2-A. (ROADMAP v0.9 산출물 "프로젝트 템플릿"의 정본화.)
  - Glossary 추가 요청: Install Manifest (설치 매니페스트) — Scaffold 설치 내용의 서술자. 필드는 이 spec §3.2-B. 멱등성·제거의 기준.
  - Glossary 추가 요청: 설치 검증 체크리스트 (Install Verification Checklist) — 설치 유효성 판정 계약. 항목은 이 spec §3.2-C.
  확정 전까지 이 spec §3.2가 세 용어 정의의 정본을 유지한다. 사유 코드(§3.2-D)는 국소 열거값이므로 Glossary 대상이 아니다 (01 §3.2-D reason 코드 선례와 동일).

- **ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 3.2(Modular), 6(Core Components에 Scaffold 포함), 5.1(Memory 단일 Port)과 Glossary §3.2-D 정의에 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

- OQ-1 결정: Scaffold의 사용자 대면 호출 표면은 Presentation Layer에 귀속한다. 산출물은 전 Layer에 걸치는 설치 도구 성격을 병기한다 (Glossary 매핑표 반영). §2의 "Layer를 단정하지 않는다"는 이 결정으로 해소된다.
- OQ-2 해소: 13 완성 확인 — 설치 대상 = 13 §3.2-A 최소 구성 집합. 설치 메커니즘·계약은 12 소유, 최소 구성의 정의는 13 소유. 13 §3.2-B 전이 조건 4가 이 조율의 완성으로 충족 가능해진다.
- OQ-3: 경계 확정 — 초기 설치(moduleSelection)는 12, 이후 추가 기능 묶음은 10 소관. 모순 없음.
- OQ-4: 03 완성 확인 — CK-5의 "루프 1 사이클 구동"은 03 §3.1의 단일 사이클 연산 호출로 정합.
- Glossary 추가 요청 3건 승인 — Glossary §3.2-J 반영.
