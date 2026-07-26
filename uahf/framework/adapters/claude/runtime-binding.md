# framework/adapters/claude/runtime-binding — Claude Code Runtime Adapter 바인딩

작성일: 2026-07-05
상태: v0.3 Baseline (CP2 Pass[재작업 1회] · CP3 승인 · 사용자 승인 2026-07-05)
상위 규약: AGENT.md
근거 정본 (계약은 § 포인터로만 인용 — 재정의 0 선언은 §0 1곳):

- specs/01-runtime.md — §3 Core Contract(연산·데이터 포맷·불변 규칙) · §4.1 Claude Code Binding 표 · §4.2 이식 교체 지점 1~7.
- Core 산출물 4종(확정) — framework/runtime/module-manifest.md · module-registry.md · lifecycle.md · framework/core/config-schema.md. "추상 계약 → 물리 실현" 매핑의 대상.
- framework/core/structure.md §2·§6(3경계 배치·일반형 `<adapter>` — 본 문서가 `claude`로 구체화, §5) · specs/02-agent.md §4.1(진입점 내부 계약·실행 모델 = 02 소관, 포인터만) · docs/delegation-protocol.md §3 · specs/00-glossary.md(용어 신설 0) · ROADMAP.md v0.3.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다 — Core 계약을 특정 실행 환경·AI·형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식 토큰의 사용이 허용된다. 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/01-runtime.md §3·§4와 Core 산출물 4종이다.** 이 문서는 그 계약의 **환경 실현 매핑**이며 계약 요소(연산·데이터 포맷·불변 규칙·필드)를 **재정의·확장하지 않는다** — 계약은 § 포인터로만 인용한다. **이 재정의 0 선언은 문서 전체에 대해 여기 1곳에서만 선언되며**, 이하 각 절은 정본 §만 지목한다. Core 4종이 "구체 인스턴스는 Adapter Binding 문서 소관"이라며 미룬 구체 어댑터명·직렬화 형식·물리 경로·환경 토큰이 실재하는 유일한 자리가 이 문서다.
- **격리 지점(방향 반전).** Core 경계 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 하지만(structure.md §5 C-3, 01 §3.3 INV-4), 이 문서는 그 **반대편**이며 그 격리가 이 경계의 존재 이유다.
- **창설 금지.** 01 §4.1 표를 넘어서는 새 바인딩 계약·새 Runtime 연산·필드·불변 규칙을 만들지 않는다.
- **용어 신설 0.** 용어는 specs/00-glossary.md 정본만 사용한다. `C-1`~`C-3`(structure.md)·`DP-1`(config-schema.md)·`SP-1`~`SP-5`(02 §4.2)·`형태 A/B`(structure.md §4)는 **서술 참조 라벨**이며 Glossary 표제어가 아니다.
- **하네스 상태 전제(Bootstrap).** Runtime 연산·수명주기가 정식 실행 Module이 아니라 규약 문서와 관행으로 실현된다(Glossary J-13·delegation-protocol.md §0·13 §3.2-B). 따라서 매핑은 **물리 실재 표면**(디렉터리·정의 파일)·**규약 수행 연산**(형태 A)·**실행 코드 도입 지점**(형태 B)을 구분한다.
- **실측 기반 상태 서술.** "실재/미존재" 주장은 파일 시스템 확인 후에만 기입하며, 재실측으로 참·거짓이 갈리는 형태로만 쓴다(byte·계수 스냅샷 불기재 — drift). **정정(2026-07-26):** 확장 표면 3디렉터리(`.claude/commands/`·`hooks/`·`skills/`)와 Module 구현 5디렉터리는 더 이상 비어 있지 않고, Project 스코프 선택 소스 `.claude/settings.json`은 미존재에서 **실재**로 바뀌었다(§2 #3·#4·#8, §3.3). `uaf-verified: .claude/{commands,hooks,skills}·framework/{loop,memory,verifier,workflow,plugins}·설정 파일 6종을 find/ls로 직접 열거`

---

## §1. 목적

이 문서는 01 §4(Adapter Binding)를 Claude Code 환경 위의 구체 매핑으로 실현한다. 절 지도 — §2 01 §4.1 바인딩 표 10행 전건 매핑 · §3 Core 산출물 4종의 "추상 계약 → 물리 실현"(§3.1 Manifest·§3.2 Registry 4연산·§3.3 Config 3스코프·§3.4 수명주기) · §4 01 §4.2 교체 지점 1~7 대응 · §5 `<adapter>` = `claude` 구체화 · §6 Advisor 조율 결정 2건 정합. 형태 A → 형태 B 전환에도 01 §3 Core Contract 변경은 0이며(structure.md §7 C-1), §4의 "유지되는 것" 열이 그 불변을 재확인한다.

---

## §2. 01 §4.1 바인딩 표 실현 — v0.3 구체 매핑 (done 1)

01 §4.1 Claude Code Binding 표의 **모든 행**을 구체 표면으로 매핑한다. "01 §4.1 바인딩 (정본 인용)" 열은 정본 값을 그대로 인용하고, "v0.3 구체 매핑" 열이 이 환경의 실재 표면·수행 방식을, "실재 여부" 열이 물리 실재/규약 실현(형태 A)/형태 B 예정을 구분한다.

| # | §3 계약 요소 | 01 §4.1 바인딩 (정본 인용) | v0.3 구체 매핑 (claude 환경) | v0.3 실재 여부 |
|---|---|---|---|---|
| 1 | Module Manifest(§3.2-A) 직렬화 | Markdown + front-matter 파일. 예: `.claude/agents/*.md`. | 직렬화 **형식** = Markdown 본문 + YAML front-matter. Manifest 7필드의 물리 표기는 §3.1 소관. | 형식 실재. 7필드 완전 직렬화 인스턴스는 형태 B. |
| 2 | Agent Module 진입점 | `.claude/agents/{advisor,planner,worker,verifier}.md` — Runtime generic Module 계약의 Agent 구현 바인딩. 진입점 내부 계약은 specs/02-agent.md §4 소관. | `entrypoint`(01 §3.2-A) = 해당 역할의 정의 파일. 활성화·해소 = 위임 시 활성 정의 파일 로딩(§3.2 Resolve). **진입점 내부 계약(위임 메시지 in → 보고 out)은 02 §4.1 소관 — 포인터만 둔다.** | 실재(4파일). |
| 3 | 확장 Module 표면 | `.claude/commands/`, `.claude/hooks/`, `.claude/skills/` — 확장 Module 등록 바인딩. 상세는 specs/08·09·10 소관. | 세 확장 디렉터리가 확장 Module 등록 표면. **등록·트리거·디스패치 상세 계약은 08·09·10 소관 — 포인터만 둔다.** 본 문서는 표면 위치 매핑에 한정한다(창설 금지, §0). | 실재 — 세 디렉터리 모두 실재하며 **등록물이 있다**(commands: `/uaf-*`·`/uahf-status` · hooks: `binary_state_guard.py` 등 · skills: `commit-message-writer/`·`discovery-interview/`). 종전 판의 "현재 비어 있음"은 2026-07-05 시점 실측이며 현재는 사실이 아니다(§0 정정). |
| 4 | Config — Project scope | `.claude/CLAUDE.md`, `.claude/AGENT.md`, 프로젝트 설정 파일(settings.json 등). | Project 스코프 물리 소스 = `.claude/CLAUDE.md`(프로젝트 지침), `.claude/AGENT.md`(공통 규약), `.claude/settings.local.json`·`.claude/settings.json`(설정). 병합 포함 규칙은 존재하는 소스 전건이다. | 실재 — 4소스 전건(`.claude/settings.json`은 종전 판 미존재에서 실재로 전환 — §0 정정). |
| 5 | Config — Global scope | 사용자·환경 전역 설정 파일. | Global 스코프 물리 소스 = 사용자 전역 설정 파일 `~/.claude/settings.json`(실재). 환경이 지원하는 선택적 Global 소스 `~/.claude/CLAUDE.md`(사용자 전역 지침)는 **미존재** — 존재 시 병합에 포함. **재시도 한도 `retry.limit`(기본값 2)의 Global 기본값이 실재 소스 `~/.claude/settings.json`에 소속된다(§3.3).** | 실재: `~/.claude/settings.json`. `~/.claude/CLAUDE.md`는 미존재(지원 소스). 프레임워크 config 로딩(형태 B)은 미도입. |
| 6 | Config — Module scope | 각 Module 정의 파일 내부의 설정 블록. | Module 스코프 물리 소스 = 각 Module 정의 파일 내부 설정 블록. 실재 예: `.claude/agents/worker.md` front-matter `model: opus`(역할-모델 **의미**는 02 §4 소관 — 포인터). | 실재. |
| 7 | Core 디렉터리 (AI 비의존) | `framework/core/`, `framework/runtime/`. AI 의존 요소 0건 유지 대상. | `framework/core/`·`framework/runtime/` — 이 두 경계 문서 본문은 AI·언어·툴체인·형식 토큰 0건 유지 대상(structure.md §5 C-3). | 실재(두 디렉터리 + Core 4종 문서). |
| 8 | Module 구현 디렉터리 | `framework/{loop,memory,verifier,workflow,plugins}/`. | 동명 5개 디렉터리가 각 Module 구현(형태 B)의 실현 경계. 계약·프로토콜 문서가 각 디렉터리에 배치되어 있고, 실행 코드 배치 형태는 형태 B에서 확정된다(structure.md §4). | 실재 — 5디렉터리 모두 실재하며 문서가 배치되어 있다. 종전 판의 "현재 비어 있음"은 2026-07-05 시점 실측이며 현재는 사실이 아니다(§0 정정). |
| 9 | Adapter Binding 산출물 | `framework/adapters/`, `.claude/`. AI·환경 의존 요소는 여기로 격리. | `framework/adapters/claude/`와 `.claude/`가 환경 의존 토큰 격리 경계 — 구체 어댑터명 `claude`는 §5에서 확정된다. | 실재. |
| 10 | 수명주기 호스트 프로세스 | Claude Code 세션/턴 = Bootstrap~Serve~Shutdown 구간의 실행 컨테이너. | 호스트 프로세스 = Claude Code **세션/턴** — 세션 개시 = Bootstrap, 턴 진행 = Serve, 세션 종료 = Shutdown 구간(§3.4). | 실재(현 세션이 그 컨테이너). |

주:

- 위 10행은 01 §4.1 표의 모든 행이다(Config는 3스코프로 3행). 각 행의 "v0.3 구체 매핑"은 정본 표현을 이 환경의 실재 표면으로 좁힌 것이며 새 바인딩 계약을 창설하지 않는다(§0). "실재 여부" 열은 **실재**(파일·디렉터리 물리 존재) / **규약 실현**(형태 A) / **형태 B 예정**(실행 코드 도입 시)의 3구분이며, 이 구분이 조기 완료·과대 주장을 막는다.

---

## §3. v0.3 Core 산출물 4종 물리 실현 매핑 (done 2)

Core 산출물 4종 각각의 "**추상 계약 → 이 환경의 물리 실현 지점**" 매핑이다. "추상 계약" 열은 각 Core 문서가 인스턴스화한 01 § 계약을 포인터로 인용하고, "물리 실현" 열이 실현 지점을, "형태" 열이 실재/규약/형태 B를 구분한다 — 진위 판정 기준은 항상 인용된 01 § 및 Core 문서다.

### §3.1 Module Manifest — framework/runtime/module-manifest.md (정본 01 §3.2-A)

| 추상 계약 (§ 포인터) | 이 환경의 물리 실현 지점 | 형태 |
|---|---|---|
| Manifest 직렬화 형식 (01 §4.1, module-manifest.md §0) | Markdown 본문 + YAML front-matter 파일. | 실재(형식) |
| `id`(식별자, 필수) | 정의 파일의 안정 식별자. 예: `.claude/agents/*.md` front-matter `name`(교체 전후 안정 — INV-7). | 실재(예: `name`) |
| `contract`(식별자, 필수) | Module이 구현하는 역할/Port 식별자. Agent Module의 경우 역할명(Advisor/Planner/Worker/Verifier)이 계약 식별자로 소비된다(02 §3.2-A 역할 경계). | 규약 실현 |
| `version`(버전 문자열, 필수) | 정의 파일의 버전 표기(front-matter 또는 문서 머리 상태 라인). | 형태 B(전용 필드), 현재 상태 라인으로 대용 |
| `requires`(식별자 목록, 선택) | 의존 contract id 목록의 물리 표기. | 형태 B |
| `entrypoint`(추상 참조, 필수) | 정의 파일 자체(활성화 진입). 서브에이전트 위임 시 로딩되는 파일 경로. | 실재(정의 파일) |
| `configSchema`(추상 참조, 선택) | 정의 파일이 참조하는 설정 스키마(Module 네임스페이스). SchemaViolation 대조 출처와 연결(§6-a). | 형태 B(실행 검증기) |
| `replaceable`(불리언, 선택·기본 true) | 정의 파일을 동일 계약의 다른 파일로 교체 가능한지(기본 true). | 규약 실현 |

- 직렬화 형식(Markdown + front-matter)은 실재하나 **7필드 완전 직렬화 인스턴스**는 형태 B다 — 현재 `.claude/agents/*.md`는 이 형식으로 역할 적합 부분집합(`name`→`id`, `model`→Module 스코프 config)을 실현한다. 필드 계약의 정본은 01 §3.2-A(작성 지침 module-manifest.md)이며, 위 표는 그 계약의 이 환경 표기만 바인딩한다.

### §3.2 Registry 4연산 — framework/runtime/module-registry.md (정본 01 §3.1-A)

Registry 4연산이 이 환경에서 수행되는 방식. Bootstrap 상태에서 등록부는 실행 코드가 아니라 **정의 파일 배치 + Advisor 오케스트레이션 규약**으로 실현된다(형태 A).

| 연산 (정본 § 포인터) | 이 환경의 수행 방식 | 형태 |
|---|---|---|
| Register (01 §3.1-A, module-registry.md §2.1) | Module 정의 파일을 해당 디렉터리에 배치한다(예: `.claude/agents/{role}.md`). front-matter `name`이 `id`이며, `id` 유일성은 파일명·`name` 충돌 없음으로 보장(DuplicateId 방지). | 규약 실현(파일 배치) |
| Resolve (01 §3.1-A, module-registry.md §2.2) | 대상 계약(역할)의 활성 정의 파일을 로딩한다. 서브에이전트 위임 시 해당 역할의 활성 파일이 정확히 1개 로딩된다(계약당 단일 바인딩 INV-3). 활성 정의 2개면 DuplicateBinding. | 규약 실현(위임 시 로딩) |
| Replace (01 §3.1-A, module-registry.md §2.3) | 동일 계약(역할)을 만족하는 다른 정의 파일로 교체한다(파일 교체). 소비자(위임자)는 **역할명(contract id)**을 참조하므로 참조 변경 0(INV-1). 실재 예: `.claude/agents/worker.md`의 `model: opus` 교체 — 소비자는 여전히 "Worker" 역할을 위임한다. | 규약 실현(파일 교체) |
| Deregister (01 §3.1-A, module-registry.md §2.4) | 대상 정의 파일을 디렉터리에서 제거한다. 그 계약에 의존하는 다른 활성 Module이 있으면 제거 거부(DependentExists). | 규약 실현(파일 제거) |

- 실패 reason 코드(ContractMismatch/DuplicateId/UnresolvedContract/DuplicateBinding/DependencyCycle/NotReplaceable/DependentExists/NotRegistered)와 공통 Failure Report 구조(operation/target/reason/location)의 정본은 01 §3.2-D·module-registry.md §5다 — 본 문서는 수행 방식만 바인딩한다. 형태 B 도입 시 위 규약 수행은 실행 Registry로 실현되고 01 §3.1-A 계약 변경은 0이다(module-registry.md §4 C-1; 13 §3.2-B 전이 조건 2의 진전 대상).

### §3.3 Config 3스코프 — framework/core/config-schema.md (정본 01 §3.2-B·§3.1-B)

Config Global/Project/Module 스코프 각각의 **물리 소스 파일**과 Load Config 수행. 스코프·우선순위·결정성 계약은 config-schema.md(정본 01 §3.2-B)가 소유하고 본 문서는 물리 소스만 바인딩한다.

| 추상 계약 (§ 포인터) | 이 환경의 물리 소스 | 형태 |
|---|---|---|
| Global scope — Framework 전역 기본값, 최저 우선순위 (config-schema.md §3, 01 §3.2-B) | `~/.claude/settings.json`(사용자 전역 설정, 실재). 지원되는 선택적 소스 `~/.claude/CLAUDE.md`(사용자 전역 지침)는 미존재 — 존재 시 병합에 포함. | `~/.claude/settings.json` 실재; `~/.claude/CLAUDE.md` 미존재(지원 소스). 로딩 형태 B |
| Project scope — 프로젝트 단위 override, 중간 우선순위 (config-schema.md §3) | `.claude/CLAUDE.md`, `.claude/AGENT.md`, `.claude/settings.local.json`, `.claude/settings.json`(4소스 전건 실재 — §0 정정). | 4소스 실재. 로딩 형태 B |
| Module scope — `target`(module id) 네임스페이스, 최고 우선순위 (config-schema.md §3) | 각 Module 정의 파일 내부 설정 블록. 예: `.claude/agents/worker.md` front-matter `model: opus`(`target` = `worker`). | 실재(worker.md `model: opus`) |
| 로딩 순서 Global → Project → Module (config-schema.md §4.1) | 위 세 소스를 이 순서로 읽는다(형태 B 로더). | 형태 B |
| 우선순위 Module > Project > Global (config-schema.md §4.2, 01 §9 OQ-R1) | 결정적 병합. 방향·결정성 정본은 config-schema.md §4·01 §3.3 INV-5. 본 문서는 방향을 재정의하지 않는다. | 계약 불변 |
| Load Config: 입력=스코프별 소스 집합 / 출력=effective config / 실패=SchemaViolation+location (config-schema.md §5, 01 §3.1-B·§3.2-D) | 세 물리 소스 집합을 입력받아 effective config를 병합 산출. 실패 시 Failure Report(operation=LoadConfig, reason=SchemaViolation, location=스코프·키). | 형태 B(실행 로더) |

**`retry.limit` 물리 소스 위치 (DP-1, config-schema.md §7).**

- **결정 인용(config-schema.md §7).** 재시도 한도 추상 키 `retry.limit`, 기본값 **2**, 기본값 스코프 **Global**(Project/Module override 허용). 물리 표기·명명 관례는 Adapter Binding 문서 소관이다.
- **물리 소스 지시.** `retry.limit`의 Global 기본값(2)은 Global 스코프 소스 = `~/.claude/settings.json`(§2 #5)에 소속된다 — 물리 표기는 그 소스의 프레임워크 설정 네임스페이스 아래 `retry.limit` 항목(값 2)이다. Project/Module override는 §2 #4·#6 소스가 담당하고 우선순위 Module > Project > Global(config-schema.md §4.2)로 병합된다.
- **형태 구분.** Bootstrap에서 이 값은 config-schema.md §7 결정 기록으로 실현(형태 A)되고, 실행 로더(형태 B) 도입 시 위 소스에서 로딩된다. 한도 초과 판정 규칙 자체는 03 §3.1-B 소관으로 불변이다.

### §3.4 Bootstrap/Shutdown 수명주기 — framework/runtime/lifecycle.md (정본 01 §3.1-C)

Bootstrap~Serve~Shutdown의 **실행 컨테이너(세션/턴)** 매핑. 연산·상태·Serve 경계의 정본은 lifecycle.md(정본 01 §3.1-C·§3.2-C·INV-2·INV-6)다.

| 추상 계약 (§ 포인터) | 이 환경의 실행 컨테이너·수행 | 형태 |
|---|---|---|
| Bootstrap — 입력(effective config + 등록 Module 집합) → Runtime Context(state=Ready\|Degraded) (lifecycle.md §2.1, 01 §3.1-C) | Claude Code **세션 개시** 구간. 세션 시작 시 Config 소스(§3.3)와 정의 파일 집합(§3.2)이 로딩되어 작업 가능(Ready) 상태가 된다. 필수 계약 미해소 시 Failed(MissingRequired). | 규약 실현(세션 개시), 실행 Bootstrap은 형태 B |
| Serve 구간 — Config·계약 해소·자원 제공(호스팅 표면 유지); 단계 오케스트레이션은 Loop 소관 (lifecycle.md §4, INV-6) | Claude Code **턴 진행** 구간. 세션 내 각 턴에서 Config 조회·Resolve(위임 시 정의 파일 로딩)·자원(서브에이전트) 호스팅이 유지된다. **단계 전이는 정의하지 않는다**(Loop 소관, 03). | 규약 실현(턴 진행) |
| Shutdown — 활성 Module 활성화 역순 Deactivate → 종료 결과 (lifecycle.md §2.2, 01 §3.1-C) | Claude Code **세션 종료** 구간. 세션 종료 시 활성 서브에이전트·자원이 해제된다. 실패 시 ShutdownIncomplete + location(module id). | 규약 실현(세션 종료), 실행 Shutdown은 형태 B |
| Runtime Context state = Ready\|Degraded\|Failed; 선택 계약 부재는 Degraded(INV-2) (lifecycle.md §3, 01 §3.2-C) | 필수 계약(진입점 정의·필수 Config)만 해소되면 부분 집합으로 기동(Degraded 허용). 선택 확장 Module(§2 #3) 부재는 Failed가 아니다. | 계약 불변 |

- Serve 구간의 Agent Lifecycle 단계 오케스트레이션 주체는 Loop Engine이다(lifecycle.md §4, INV-6) — 본 문서는 단계 전이를 서술하지 않고 세션/턴을 실행 컨테이너로만 매핑한다(경계 불가침). 실행 Bootstrap/Shutdown(형태 B)은 13 §3.2-B 전이 조건 2 진전 시 실현되며 01 §3.1-C 계약 변경은 0이다(lifecycle.md §5 C-1).

---

## §4. 01 §4.2 이식 교체 지점 실현 — 무엇이 교체되고 무엇이 유지되는가 (done 3)

01 §4.2 이식 교체 지점 1~7 각각의 대응이다. "이 환경(claude) 바인딩" = 이식 시 **교체되는 것**, "유지되는 것" = 이식 시에도 바뀌지 않는 Core Contract·산출물 계약이며, 유지 열이 structure.md §7 C-1을 이식 축에서 재확인한다.

| # (01 §4.2) | 교체 지점 | 이 환경(claude) 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|
| 1 | Manifest 직렬화 | Markdown + YAML front-matter 파일(예: `.claude/agents/*.md`)의 필드 물리 표기(§3.1). | Module Manifest 7필드 계약 (01 §3.2-A, module-manifest.md). |
| 2 | Config 소스·위치 | 실재 소스 `~/.claude/settings.json`, `.claude/CLAUDE.md`, `.claude/AGENT.md`, `.claude/settings.local.json`, `.claude/settings.json`, 정의 파일 설정 블록; 지원되나 미존재인 선택적 소스 `~/.claude/CLAUDE.md`(§3.3). | Config 3스코프·로딩 순서·우선순위·결정성·누락 처리 (01 §3.2-B, config-schema.md §3~§6). |
| 3 | 진입점 해소 | 파일 기반 정의 로딩 — 서브에이전트 위임 시 활성 정의 파일 로딩(§3.2 Resolve). | Register/Resolve/Replace/Deregister 4연산 계약 (01 §3.1-A, module-registry.md §2). |
| 4 | 호스트 프로세스/세션 수명주기 | Claude Code 세션/턴 = Bootstrap~Serve~Shutdown 실행 컨테이너(§3.4). | Bootstrap/Shutdown·Runtime Context·Serve 경계·부분 집합 기동 (01 §3.1-C·§3.2-C·INV-2·INV-6, lifecycle.md). |
| 5 | 바인딩 디렉터리 | `.claude/`, `framework/adapters/claude/`(본 문서 경계). | Core/Adapter 물리 분리 규칙, 3경계 배치 (01 §3.2-E 규칙 3, structure.md §2·§3). |
| 6 | 확장 표면 | `.claude/commands/`, `.claude/hooks/`, `.claude/skills/`(§2 #3). 상세 08·09·10 소관. | 확장 Module 등록 계약 (01 §3.1-A 위 확장; 상세 정본 08·09·10). |
| 7 | Agent 역할 실행 모델 지정 | `.claude/agents/worker.md`의 `model: opus` 등(실재). **정의·소관은 02 §4(SP-3) — Runtime은 참조만 한다.** | §3.2-A 역할 경계·메시지 필수 필드 (02 §3, 02 §4.2 "유지되는 것"). |

주:
- 교체 지점 7(Agent 역할 실행 모델 지정)은 01 §4.2가 "specs/02-agent.md §4 소관 — Runtime은 참조만 하고 정의하지 않는다"고 못박은 항목이다. 본 문서는 실재 표면(`model: opus`)을 **참조로만** 표기하며 02 §4.1 SP-3이 정본이다.
- "유지되는 것" 열의 계약은 다른 AI 환경으로 이식해도 바뀌지 않는다 — 01 §3 Core Contract·Core 4종 산출물 계약의 이식 불변성이며 structure.md §7 C-1과 정합한다. 이 목록의 정식화는 specs/11-adapters.md 소관이고 본 문서는 선취하지 않는다(§0).

---

## §5. 구조 규격 연결 — `<adapter>` = `claude` 구체화 (done 4)

- **일반형 → 구체화.** structure.md §2·§6·§8은 Adapter 경계를 일반형 `framework/adapters/<adapter>/`로 표기하고 **구체 어댑터명은 해당 Adapter Binding 문서가 소유한다**고 둔다. **이 문서가 그 소유자이며 `<adapter>` = `claude`로 구체화한다** — 물리 경로 `framework/adapters/claude/runtime-binding.md`(= 본 파일).
- **토큰 격리의 단일 자리 · 비중첩.** 구체 어댑터명 `claude`와 환경 토큰(Markdown·front-matter·`.claude/…`·`~/.claude/settings.json`·세션/턴·Opus·서브에이전트)은 이 경계에만 존재하고, Core 4종은 "구체 인스턴스는 Adapter Binding 문서 소관" 포인터만 둔다(structure.md §5 C-3, 01 §3.3 INV-4). Core 경계와 Adapter 경계는 물리적으로 비중첩이므로(structure.md §3 규칙 3·§8, 01 §3.2-E 규칙 3) 이 문서가 구체 토큰을 담아도 Core 디렉터리 AI 비의존 불변(INV-4)을 침해하지 않고 그 격리를 완성한다. 초판의 1파일 생성 소유 경계(07 R4) 감사 흔적은 git 이력(초판 커밋)에 보존되어 있다. `uaf-allow-legacy: 초판 감사 흔적은 git 이력에 보존, 본문은 포인터 1줄`

---

## §6. Advisor 조율 결정 2건 정합 (done 5)

Advisor 조율 결정 2건(config-schema.md §5 주·§7)과 본 문서의 정합을 확인한다 — 두 결정을 재정의하지 않고 **물리 실현으로만** 바인딩한다.

- **(a) SchemaViolation 대조 스키마 출처(config-schema.md §5 주).** 결정 = Module scope 값은 대상 Module Manifest의 `configSchema`(부재 시 §2 구조 규칙), Global/Project scope 값은 Module 네임스페이스 키면 그 Module의 `configSchema`·Framework 수준 키는 구조 규칙(01 §3.2-A·§3.2-B의 조합, 새 계약 아님). 이 환경의 물리 출처는 그 결정을 그대로 따른다 — Module scope = 정의 파일 설정 블록(§3.3), Framework 수준 키 = config-schema.md §2 구조 규칙. **본 문서는 물리 출처만 지시하고 어느 스키마로 대조하는가의 판정 규칙은 config-schema.md §5가 소유한다** → 모순 0.
- **(b) `retry.limit` 물리 소스 위치(config-schema.md §7 DP-1).** 결정 = 기본값 2·기본값 스코프 Global. 그 기본값은 실재 소스 `~/.claude/settings.json`(§2 #5)에 소속되며(§3.3 지시), `~/.claude/CLAUDE.md`는 지원되나 미존재이므로 소속 소스가 아니다. 값·기본값 스코프·override 우선순위(Module > Project > Global)는 전부 config-schema.md §7·§4.2 인용이고, 한도 초과 판정 규칙은 03 §3.1-B 소관으로 불변이다 → 재정의 0.

---

## §7. 요약 (1줄)

- 이 문서 = 01 §4(바인딩 표 10행·교체 지점 1~7)의 환경 실현 매핑 + Core 4종의 "추상 계약 → 물리 실현" — 절 지도는 §1, 정본 경계·정정 이력은 §0이 소유하며 여기서 재서술하지 않는다.
