# framework/adapters/claude/runtime-binding — Claude Code Runtime Adapter 바인딩

작성일: 2026-07-05
상태: v0.3 Baseline (CP2 Pass[재작업 1회] · CP3 승인 · 사용자 승인 2026-07-05)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §4.1 — Claude Code Binding 표. 본 문서가 v0.3 시점의 구체 매핑으로 실현하는 바인딩 표의 정본.
- specs/01-runtime.md §4.2 — 이식 교체 지점(1~7). 본 문서가 v0.3 산출물 기준으로 대응을 명시하는 교체 지점의 정본.
- specs/01-runtime.md §3 — Core Contract(연산·데이터 포맷·불변 규칙). 본 문서가 실현하는 추상 계약의 정본. 본 문서는 이 계약을 재정의하지 않고 § 포인터로만 인용한다.
- v0.3 Core 산출물 4종 (확정): framework/runtime/module-manifest.md, framework/runtime/module-registry.md, framework/core/config-schema.md, framework/runtime/lifecycle.md — 본 문서가 "추상 계약 → 물리 실현" 매핑의 대상으로 삼는 확정 문서.
- framework/core/structure.md §2·§6 — 3경계 배치와 v0.3 산출물 표. 특히 일반형 `<adapter>` 표기와 마지막 행 `framework/adapters/<adapter>/runtime-binding.md`. 본 문서가 `<adapter>` = `claude`로 구체화하는 대상.
- specs/02-agent.md §4.1 — Agent 정의 파일·위임 메커니즘·실행 모델 바인딩. 본 문서는 Agent 진입점 내부 계약·실행 모델 지정을 이 § 포인터로만 참조한다(02 소관).
- docs/delegation-protocol.md §3 — 이 프로젝트의 물리 채널 바인딩 관행(서브에이전트 위임/최종 응답). 물리 채널 서술의 관행 근거.
- specs/00-glossary.md — 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- ROADMAP.md v0.3 (Runtime & Core Kernel) — 산출물 "Adapter 바인딩(Core 산출물의 환경 실현)"의 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식 토큰의 사용이 **허용**된다(여기가 격리 지점이다). 단 이 문서는 Core Contract(01 §3·Core 4종 문서)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.3 Draft | 최초 작성. `framework/adapters/` 경계의 첫 산출물. 01 §4.1 바인딩 표 10행의 v0.3 구체 매핑(§2), Core 산출물 4종의 "추상 계약 → 물리 실현" 매핑(§3), 01 §4.2 이식 교체 지점 1~7 대응(§4), structure.md `<adapter>` = `claude` 구체화(§5), Advisor 조율 결정 2건(SchemaViolation·retry.limit) 정합(§6). | Worker (Advisor 위임, Task A5) |
| 2026-07-05 | v0.3 Draft r2 | CP2 재작업 — 상태 서술 교정. 미존재 Config 소스 2건(`~/.claude/CLAUDE.md` Global, `.claude/settings.json` Project)을 "실재"에서 "환경 지원 선택적 소스 — 현 시점 미존재"로 구분 표기(§2 #4·#5, §3.3, §4 #2, §6-b). `retry.limit` Global 기본값 소속 소스를 실재 소스 `~/.claude/settings.json`으로 명확화. 문서 내 모든 "실재/존재" 서술을 파일 시스템과 전수 대조(불일치 0건 확인). | Worker (Advisor CP2 재작업 지시, Task A5) |
| 2026-07-05 | v0.3 Baseline | v0.3 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass, CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/01-runtime.md §4(§4.1 바인딩 표·§4.2 이식 교체 지점)와 §3(Core Contract), 그리고 v0.3 Core 산출물 4종이다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·필드)를 **재정의·확장하지 않는다**. 계약 요소는 01 §3·Core 4종 문서의 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. Core 4종 문서(structure/config-schema/module-manifest/module-registry/lifecycle)가 "구체 인스턴스는 Adapter Binding 문서 소관"이라며 미룬 **구체 어댑터명·직렬화 형식·물리 경로·환경 토큰**이 실재하는 유일한 자리다(structure.md §0·§5, 각 Core 문서 §0).
- **격리 지점의 방향 반전.** Core 경계(`framework/core/`·`framework/runtime/`) 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3, 01 §3.3 INV-4). 이 문서는 그 **반대편**이다 — 구체 토큰(Claude Code, Markdown, front-matter, `.claude/…`, settings 파일, 세션/턴, Opus 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다.
- **창설 금지.** 이 문서는 01 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.3 산출물의 실현 매핑으로 한정한다. Core Contract를 재정의하지 않으며, 새 Runtime 연산·필드·불변 규칙을 만들지 않는다.
- **용어 신설 없음.** 용어는 specs/00-glossary.md 정본만 사용한다(Glossary §3.3 INV-4). 본 문서가 인용하는 `C-1`~`C-3`(structure.md 확정 조건)·`DP-1`(config-schema.md 결정 지점)·`SP-1`~`SP-5`(02 §4.2)·`형태 A/형태 B`(structure.md 서술 라벨)는 **서술 참조 라벨**이며 Glossary 표제어가 아니다 — 정본 용어처럼 신설·확장하지 않고 참조 라벨로만 인용한다.
- **하네스 상태 전제.** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, delegation-protocol.md §0, 13 §3.2-B). 즉 Runtime 연산·수명주기가 정식 실행 Module이 아니라 규약 문서와 관행으로 실현된다. 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(디렉터리·정의 파일)과, **규약으로 수행되는 연산**(현재 형태 A), **실행 코드 도입 시 로딩될 지점**(형태 B)을 정직하게 구분한다. `형태 A`(문서·규약)와 `형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.

---

## §1. 목적

이 문서는 01 §4(Adapter Binding)를 Claude Code 환경 위에 **v0.3 시점의 구체 매핑**으로 실현한다.

책임은 네 가지다.

- 01 §4.1 바인딩 표의 **모든 행**을 v0.3의 실재 표면으로 매핑한다(§2).
- v0.3 Core 산출물 4종 각각의 **추상 계약을 이 환경의 물리 실현 지점**으로 매핑한다(§3).
- 01 §4.2 이식 교체 지점 1~7 각각에 v0.3 산출물 기준의 대응(**무엇이 교체되고 무엇이 유지되는가**)을 명시한다(§4).
- structure.md의 일반형 `<adapter>`를 `claude`로 **구체화**하고, 구체 토큰이 이 경계에만 존재함을 서술한다(§5). 그리고 Advisor 조율 결정 2건과의 정합을 확인한다(§6).

이 문서는 01 §3·Core 4종의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A(문서·규약) → 형태 B(실행 코드) 전환 시에도 01 §3 Core Contract 변경은 0이며(structure.md §7 C-1), 이 문서(§4의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 01 §4.1 바인딩 표 실현 — v0.3 구체 매핑 (done 1)

01 §4.1 Claude Code Binding 표의 **모든 행**을 v0.3 시점의 구체 표면으로 매핑한다. 아래 표의 "01 §4.1 바인딩" 열은 정본 표의 값을 그대로 인용하고, "v0.3 구체 매핑" 열이 이 환경의 실재 표면·수행 방식을, "v0.3 실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현/형태 B 예정을 정직하게 구분한다.

| # | §3 계약 요소 | 01 §4.1 바인딩 (정본 인용) | v0.3 구체 매핑 (claude 환경) | v0.3 실재 여부 |
|---|---|---|---|---|
| 1 | Module Manifest(§3.2-A) 직렬화 | Markdown + front-matter 파일. 예: `.claude/agents/*.md`. | 직렬화 **형식** = Markdown 본문 + YAML front-matter. Manifest 7필드(01 §3.2-A)의 물리 표기 규약은 이 문서 소관(§3.1). 현재 `.claude/agents/*.md` front-matter(`name`/`description`/`model`)가 이 형식을 예시한다. | 형식 실재(정의 파일 실재). 7필드 완전 직렬화 인스턴스는 형태 B. |
| 2 | Agent Module 진입점 | `.claude/agents/{advisor,planner,worker,verifier}.md` — Runtime generic Module 계약의 Agent 구현 바인딩. 진입점 내부 계약은 specs/02-agent.md §4 소관. | `entrypoint`(01 §3.2-A) = 해당 역할의 정의 파일(4개 실재). 활성화·해소 = 서브에이전트 위임 시 활성 정의 파일 로딩(§3.2 Resolve). **진입점 내부 계약(위임 메시지 in → 보고 out)은 02 §4.1 소관 — 포인터만 둔다.** | 실재(advisor/planner/worker/verifier.md 4개 파일). |
| 3 | 확장 Module 표면 | `.claude/commands/`, `.claude/hooks/`, `.claude/skills/` — 확장 Module 등록 바인딩. 상세는 specs/08·09·10 소관. | 세 확장 디렉터리가 확장 Module 등록 표면. **등록·트리거·디스패치 상세 계약은 08·09·10 소관 — 포인터만 둔다.** 본 문서는 표면 위치 매핑에 한정한다(창설 금지, §0). | 실재(세 디렉터리 존재, 현재 비어 있음). |
| 4 | Config — Project scope | `.claude/CLAUDE.md`, `.claude/AGENT.md`, 프로젝트 설정 파일(settings.json 등). | Project 스코프 물리 소스 = `.claude/CLAUDE.md`(프로젝트 지침), `.claude/AGENT.md`(공통 규약), `.claude/settings.local.json`(설정). 환경이 지원하는 선택적 소스 `.claude/settings.json`은 **현 시점 미존재** — 존재 시 병합에 포함. | 실재: `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`. `.claude/settings.json`은 미존재(지원 소스). |
| 5 | Config — Global scope | 사용자·환경 전역 설정 파일. | Global 스코프 물리 소스 = 사용자 전역 설정 파일 `~/.claude/settings.json`(실재). 환경이 지원하는 선택적 Global 소스 `~/.claude/CLAUDE.md`(사용자 전역 지침)는 **현 시점 미존재** — 존재 시 병합에 포함. **재시도 한도 `retry.limit`(기본값 2)의 Global 기본값이 실재 소스 `~/.claude/settings.json`에 소속된다(§3.3, done 5b).** | 실재: `~/.claude/settings.json`. `~/.claude/CLAUDE.md`는 미존재(지원 소스). 프레임워크 config 로딩(형태 B)은 미도입. |
| 6 | Config — Module scope | 각 Module 정의 파일 내부의 설정 블록. | Module 스코프 물리 소스 = 각 Module 정의 파일 내부 설정 블록. 실재 예: `.claude/agents/worker.md` front-matter `model: opus`(역할-모델 **의미**는 02 §4 실행 모델 바인딩 소관 — 포인터). | 실재(worker.md `model: opus`). |
| 7 | Core 디렉터리 (AI 비의존) | `framework/core/`, `framework/runtime/`. AI 의존 요소 0건 유지 대상. | `framework/core/`(structure.md, config-schema.md), `framework/runtime/`(module-manifest.md, module-registry.md, lifecycle.md). 이 두 경계 문서 본문은 AI·언어·툴체인·형식 토큰 0건 유지 대상(structure.md §5 C-3). | 실재(두 디렉터리 + Core 4종 중 4문서). |
| 8 | Module 구현 디렉터리 | `framework/{loop,memory,verifier,workflow,plugins}/`. | 동명 5개 디렉터리가 각 Module 구현(형태 B)의 실현 경계. 현재 비어 있음 — 계약·프로토콜 문서는 `framework/runtime/`·`framework/core/`에 있고, 실행 코드 배치는 형태 B에서 확정(structure.md §4). | 실재(5개 디렉터리, 현재 비어 있음). |
| 9 | Adapter Binding 산출물 | `framework/adapters/`, `.claude/`. AI·환경 의존 요소는 여기로 격리. | `framework/adapters/claude/`(**본 문서가 최초 생성한 경계**)와 `.claude/`가 환경 의존 토큰 격리 경계. 구체 어댑터명 `claude`는 여기서 확정된다(§5). | 실재(`framework/adapters/` + `.claude/`; `claude/`는 본 산출물로 신규). |
| 10 | 수명주기 호스트 프로세스 | Claude Code 세션/턴 = Bootstrap~Serve~Shutdown 구간의 실행 컨테이너. | 호스트 프로세스 = Claude Code **세션/턴**. 세션 개시 = Bootstrap 구간, 턴 진행 = Serve 구간, 세션 종료 = Shutdown 구간의 실행 컨테이너(§3.4). | 실재(현 세션이 그 컨테이너). |

주:

- 위 10행은 01 §4.1 표의 모든 행이다(Config는 3스코프로 3행). 각 행의 "v0.3 구체 매핑"은 01 §4.1 정본 표현을 이 환경의 실재 표면으로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- "v0.3 실재 여부" 열은 Bootstrap 상태의 정직한 구분이다 — **실재**(파일·디렉터리가 물리적으로 존재), **규약 실현**(형태 A로 수행), **형태 B 예정**(실행 코드 도입 시). 이 구분은 조기 완료·과대 주장을 방지한다.

---

## §3. v0.3 Core 산출물 4종 물리 실현 매핑 (done 2)

Core 산출물 4종 각각에 대해 "**추상 계약 → 이 환경의 물리 실현 지점**" 매핑을 제시한다. "추상 계약" 열은 각 Core 문서가 인스턴스화한 01 § 계약을 § 포인터로 인용하고, "물리 실현" 열이 이 환경의 실현 지점을, "형태" 열이 Bootstrap 상태에서의 실재/규약/형태 B 예정을 구분한다. 계약 요소의 진위 판정 기준은 항상 인용된 01 § 및 Core 문서다(재정의 없음).

### §3.1 Module Manifest — framework/runtime/module-manifest.md (정본 01 §3.2-A)

| 추상 계약 (§ 포인터) | 이 환경의 물리 실현 지점 | 형태 |
|---|---|---|
| Manifest 직렬화 형식 (01 §4.1, module-manifest.md §0) | Markdown 본문 + YAML front-matter 파일. | 실재(형식) |
| `id`(식별자, 필수) | 정의 파일의 안정 식별자. 예: `.claude/agents/*.md` front-matter `name`(교체 전후 안정 — INV-7). | 실재(예: `name`) |
| `contract`(식별자, 필수) | Module이 구현하는 역할/Port 식별자. Agent Module의 경우 역할명(Advisor/Planner/Worker/Verifier)이 계약 식별자로 소비된다(02 §3.2-A 역할 경계). | 규약 실현 |
| `version`(버전 문자열, 필수) | 정의 파일의 버전 표기(front-matter 또는 문서 이력). | 형태 B(전용 필드), 현재 이력 절로 대용 |
| `requires`(식별자 목록, 선택) | 의존 contract id 목록의 물리 표기. | 형태 B |
| `entrypoint`(추상 참조, 필수) | 정의 파일 자체(활성화 진입). 서브에이전트 위임 시 로딩되는 파일 경로. | 실재(정의 파일) |
| `configSchema`(추상 참조, 선택) | 정의 파일이 참조하는 설정 스키마(Module 네임스페이스). SchemaViolation 대조 출처와 연결(§6-a). | 형태 B(실행 검증기) |
| `replaceable`(불리언, 선택·기본 true) | 정의 파일을 동일 계약의 다른 파일로 교체 가능한지(기본 true). | 규약 실현 |

- 직렬화 형식(Markdown + front-matter)은 실재하나, **7필드 완전 직렬화 인스턴스**(예: 명시적 `contract`/`version`/`requires` 필드를 갖춘 Manifest)는 형태 B다. 현재 `.claude/agents/*.md`는 이 형식으로 역할 적합 부분집합(`name`→`id`, `model`→Module 스코프 config)을 실현한다.
- 필드 계약의 정본은 01 §3.2-A(작성 지침 module-manifest.md)다. 위 물리 표기는 그 계약을 재정의하지 않고 이 환경의 표기로 바인딩한 것이다.

### §3.2 Registry 4연산 — framework/runtime/module-registry.md (정본 01 §3.1-A)

Registry 4연산이 **이 환경에서 어떻게 수행되는가**. Bootstrap 상태에서 등록부는 실행 코드가 아니라 **정의 파일 배치 + Advisor 오케스트레이션 규약**으로 실현된다(형태 A).

| 연산 (정본 § 포인터) | 이 환경의 수행 방식 | 형태 |
|---|---|---|
| Register (01 §3.1-A, module-registry.md §2.1) | Module 정의 파일을 해당 디렉터리에 배치한다(예: `.claude/agents/{role}.md`). front-matter `name`이 `id`이며, `id` 유일성은 파일명·`name` 충돌 없음으로 보장(DuplicateId 방지). | 규약 실현(파일 배치) |
| Resolve (01 §3.1-A, module-registry.md §2.2) | 대상 계약(역할)의 활성 정의 파일을 로딩한다. 서브에이전트 위임 시 해당 역할의 활성 파일이 정확히 1개 로딩된다(계약당 단일 바인딩 INV-3). 활성 정의 2개면 DuplicateBinding. | 규약 실현(위임 시 로딩) |
| Replace (01 §3.1-A, module-registry.md §2.3) | 동일 계약(역할)을 만족하는 다른 정의 파일로 교체한다(파일 교체). 소비자(위임자)는 **역할명(contract id)**을 참조하므로 참조 변경 0(INV-1). 실재 예: `.claude/agents/worker.md`의 `model: opus` 교체 — 소비자는 여전히 "Worker" 역할을 위임한다. | 규약 실현(파일 교체) |
| Deregister (01 §3.1-A, module-registry.md §2.4) | 대상 정의 파일을 디렉터리에서 제거한다. 그 계약에 의존하는 다른 활성 Module이 있으면 제거 거부(DependentExists). | 규약 실현(파일 제거) |

- 실패 reason 코드(ContractMismatch/DuplicateId/UnresolvedContract/DuplicateBinding/DependencyCycle/NotReplaceable/DependentExists/NotRegistered)와 공통 Failure Report 구조(operation/target/reason/location)의 정본은 01 §3.2-D·module-registry.md §5다. 본 문서는 코드를 재정의하지 않고 수행 방식만 바인딩한다.
- 형태 B(실행 코드) 도입 시, 위 규약 수행은 실행 Registry로 실현되며 01 §3.1-A 계약 변경은 0이다(module-registry.md §4 C-1). 13 §3.2-B 전이 조건 2(Runtime 정식 Module 호스팅)의 진전 대상이다(session-handoff-v0.2 §5-3).

### §3.3 Config 3스코프 — framework/core/config-schema.md (정본 01 §3.2-B·§3.1-B)

Config Global/Project/Module 스코프 **각각의 물리 소스 파일**과 Load Config 수행. 스코프·우선순위·결정성 계약은 config-schema.md(정본 01 §3.2-B)가 유지하며 본 문서는 물리 소스만 바인딩한다.

| 추상 계약 (§ 포인터) | 이 환경의 물리 소스 | 형태 |
|---|---|---|
| Global scope — Framework 전역 기본값, 최저 우선순위 (config-schema.md §3, 01 §3.2-B) | `~/.claude/settings.json`(사용자 전역 설정, 실재). 지원되는 선택적 소스 `~/.claude/CLAUDE.md`(사용자 전역 지침)는 현 시점 미존재 — 존재 시 병합에 포함. | `~/.claude/settings.json` 실재; `~/.claude/CLAUDE.md` 미존재(지원 소스). 로딩 형태 B |
| Project scope — 프로젝트 단위 override, 중간 우선순위 (config-schema.md §3) | `.claude/CLAUDE.md`, `.claude/AGENT.md`, `.claude/settings.local.json`(실재). 지원되는 선택적 소스 `.claude/settings.json`은 현 시점 미존재. | `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json` 실재; `.claude/settings.json` 미존재(지원 소스) |
| Module scope — `target`(module id) 네임스페이스, 최고 우선순위 (config-schema.md §3) | 각 Module 정의 파일 내부 설정 블록. 예: `.claude/agents/worker.md` front-matter `model: opus`(`target` = `worker`). | 실재(worker.md `model: opus`) |
| 로딩 순서 Global → Project → Module (config-schema.md §4.1) | 위 세 소스를 이 순서로 읽는다(형태 B 로더). | 형태 B |
| 우선순위 Module > Project > Global (config-schema.md §4.2, 01 §9 OQ-R1) | 결정적 병합. 방향·결정성 정본은 config-schema.md §4·01 §3.3 INV-5. 본 문서는 방향을 재정의하지 않는다. | 계약 불변 |
| Load Config: 입력=스코프별 소스 집합 / 출력=effective config / 실패=SchemaViolation+location (config-schema.md §5, 01 §3.1-B·§3.2-D) | 세 물리 소스 집합을 입력받아 effective config를 병합 산출. 실패 시 Failure Report(operation=LoadConfig, reason=SchemaViolation, location=스코프·키). | 형태 B(실행 로더) |

**`retry.limit` 물리 소스 위치 (DP-1, config-schema.md §7 — done 5b).**

- config-schema.md §7 결정 기록: 재시도 한도 추상 키 `retry.limit`, **기본값 2**, **기본값 스코프 Global**(Project/Module override 허용). 물리 표기·명명 관례는 Adapter Binding 문서 소관(config-schema.md §7).
- **물리 소스 위치 지시:** `retry.limit`의 Global 기본값(2)은 **Global 스코프 소스**(§2 #5 행 = `~/.claude/settings.json`)에 소속된다. 물리 표기 예 — Global 스코프 소스의 프레임워크 설정 네임스페이스 아래 `retry.limit` 항목(값 2). Project/Module override는 각각 §2 #4·#6 행의 소스가 담당하며, 우선순위 Module > Project > Global(config-schema.md §4.2)로 병합된다.
- **형태 구분:** v0.3 Bootstrap에서 이 값은 config-schema.md §7 **결정 기록으로 실현(형태 A)**된다. 실행 로더(형태 B) 도입 시 위 Global 스코프 물리 소스에서 로딩되며, 한도 초과 판정 규칙 자체는 03 §3.1-B 소관으로 불변이다(config-schema.md §7).

### §3.4 Bootstrap/Shutdown 수명주기 — framework/runtime/lifecycle.md (정본 01 §3.1-C)

Bootstrap~Serve~Shutdown의 **실행 컨테이너(세션/턴)** 매핑. 연산·상태·Serve 경계의 정본은 lifecycle.md(정본 01 §3.1-C·§3.2-C·INV-2·INV-6)다.

| 추상 계약 (§ 포인터) | 이 환경의 실행 컨테이너·수행 | 형태 |
|---|---|---|
| Bootstrap — 입력(effective config + 등록 Module 집합) → Runtime Context(state=Ready\|Degraded) (lifecycle.md §2.1, 01 §3.1-C) | Claude Code **세션 개시** 구간. 세션 시작 시 Config 소스(§3.3)와 정의 파일 집합(§3.2)이 로딩되어 작업 가능(Ready) 상태가 된다. 필수 계약 미해소 시 Failed(MissingRequired). | 규약 실현(세션 개시), 실행 Bootstrap은 형태 B |
| Serve 구간 — Config·계약 해소·자원 제공(호스팅 표면 유지); 단계 오케스트레이션은 Loop 소관 (lifecycle.md §4, INV-6) | Claude Code **턴 진행** 구간. 세션 내 각 턴에서 Config 조회·Resolve(위임 시 정의 파일 로딩)·자원(서브에이전트) 호스팅이 유지된다. **단계 전이는 정의하지 않는다**(Loop 소관, 03). | 규약 실현(턴 진행) |
| Shutdown — 활성 Module 활성화 역순 Deactivate → 종료 결과 (lifecycle.md §2.2, 01 §3.1-C) | Claude Code **세션 종료** 구간. 세션 종료 시 활성 서브에이전트·자원이 해제된다. 실패 시 ShutdownIncomplete + location(module id). | 규약 실현(세션 종료), 실행 Shutdown은 형태 B |
| Runtime Context state = Ready\|Degraded\|Failed; 선택 계약 부재는 Degraded(INV-2) (lifecycle.md §3, 01 §3.2-C) | 필수 계약(진입점 정의·필수 Config)만 해소되면 부분 집합으로 기동(Degraded 허용). 선택 확장 Module(§2 #3) 부재는 Failed가 아니다. | 계약 불변 |

- Serve 구간에서 Agent Lifecycle 단계 오케스트레이션 주체는 Loop Engine이다(lifecycle.md §4, INV-6, Glossary §9-OQ2). 본 문서는 단계 전이를 서술하지 않으며, 세션/턴을 실행 컨테이너로만 매핑한다(경계 불가침).
- 실행 Bootstrap/Shutdown(형태 B)은 13 §3.2-B 전이 조건 2 진전 시 실현되며 01 §3.1-C 계약 변경은 0이다(lifecycle.md §5 C-1).

---

## §4. 01 §4.2 이식 교체 지점 실현 — 무엇이 교체되고 무엇이 유지되는가 (done 3)

01 §4.2 이식 교체 지점 1~7 각각에 v0.3 산출물 기준의 대응을 명시한다. "이 환경(claude) 바인딩" = 이식 시 **교체되는 것**, "유지되는 것(정본 § 불변)" = 이식 시에도 바뀌지 않는 Core Contract·산출물 계약. 유지 열이 structure.md §7 C-1(형태·환경 전환에도 Core Contract 변경 0)을 이식 축에서 재확인한다.

| # (01 §4.2) | 교체 지점 | 이 환경(claude) 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|
| 1 | Manifest 직렬화 | Markdown + YAML front-matter 파일(예: `.claude/agents/*.md`)의 필드 물리 표기(§3.1). | Module Manifest 7필드 계약 (01 §3.2-A, module-manifest.md). |
| 2 | Config 소스·위치 | 실재 소스 `~/.claude/settings.json`, `.claude/CLAUDE.md`, `.claude/AGENT.md`, `.claude/settings.local.json`, 정의 파일 설정 블록; 지원되나 현 시점 미존재인 선택적 소스 `.claude/settings.json`·`~/.claude/CLAUDE.md`(§3.3). | Config 3스코프·로딩 순서·우선순위·결정성·누락 처리 (01 §3.2-B, config-schema.md §3~§6). |
| 3 | 진입점 해소 | 파일 기반 정의 로딩 — 서브에이전트 위임 시 활성 정의 파일 로딩(§3.2 Resolve). | Register/Resolve/Replace/Deregister 4연산 계약 (01 §3.1-A, module-registry.md §2). |
| 4 | 호스트 프로세스/세션 수명주기 | Claude Code 세션/턴 = Bootstrap~Serve~Shutdown 실행 컨테이너(§3.4). | Bootstrap/Shutdown·Runtime Context·Serve 경계·부분 집합 기동 (01 §3.1-C·§3.2-C·INV-2·INV-6, lifecycle.md). |
| 5 | 바인딩 디렉터리 | `.claude/`, `framework/adapters/claude/`(본 문서 경계). | Core/Adapter 물리 분리 규칙, 3경계 배치 (01 §3.2-E 규칙 3, structure.md §2·§3). |
| 6 | 확장 표면 | `.claude/commands/`, `.claude/hooks/`, `.claude/skills/`(§2 #3). 상세 08·09·10 소관. | 확장 Module 등록 계약 (01 §3.1-A 위 확장; 상세 정본 08·09·10). |
| 7 | Agent 역할 실행 모델 지정 | `.claude/agents/worker.md`의 `model: opus` 등(실재). **정의·소관은 02 §4(SP-3) — Runtime은 참조만 한다.** | §3.2-A 역할 경계·메시지 필수 필드 (02 §3, 02 §4.2 "유지되는 것"). |

주:

- 교체 지점 7(Agent 역할 실행 모델 지정)은 01 §4.2가 "specs/02-agent.md §4 소관. Runtime은 참조만 하고 정의하지 않는다"고 못박은 항목이다. 본 문서는 실재 표면(`model: opus`)을 **참조로만** 표기하고 정의하지 않는다. 02 §4.1 SP-3·session-handoff-v0.2 §1.3(worker.md만 `model: opus`, 나머지는 세션 상속)이 정본이다.
- "유지되는 것" 열의 계약은 이식 시(다른 AI 환경으로) 바뀌지 않는다 — 이것이 01 §3 Core Contract와 Core 4종 산출물 계약의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(01 §4.2 말미). 본 문서는 그 정식화를 선취하지 않고 v0.3 실현 매핑에 한정한다(창설 금지, §0).

---

## §5. 구조 규격 연결 — `<adapter>` = `claude` 구체화 (done 4)

- **일반형 → 구체화.** structure.md §2·§6·§8은 Adapter 경계를 일반형 `framework/adapters/<adapter>/`로, 그 산출물을 `framework/adapters/<adapter>/runtime-binding.md`로 표기한다. `<adapter>`는 일반형 표기이며 **구체 어댑터명(하위 디렉터리 이름)은 해당 Adapter Binding 문서가 소유한다**(structure.md §0·§5·§6 주). **이 문서가 그 소유자이며, `<adapter>` = `claude`로 구체화한다.** 물리 경로: `framework/adapters/claude/runtime-binding.md`(= 본 파일). 이 산출로 `framework/adapters/` 경계 아래 `claude/` 하위 경계가 최초 생성되었다.
- **토큰 격리의 단일 자리.** 구체 어댑터명 `claude`와 이 환경의 구체 토큰(Markdown, front-matter, `.claude/…`, `~/.claude/settings.json`, 세션/턴, Opus, 서브에이전트 등)은 **이 문서(`framework/adapters/` 경계)에만 존재한다**. Core 4종 문서(structure/config-schema/module-manifest/module-registry/lifecycle)는 이 토큰들을 본문에 두지 않고 "구체 인스턴스는 Adapter Binding 문서 소관"이라는 **소관 포인터만** 둔다(structure.md §5 C-3, 각 Core 문서 §0·§6 self-note, 01 §3.3 INV-4).
- **비중첩 재확인.** Core 경계(`framework/core/`·`framework/runtime/`)와 Adapter 경계(`framework/adapters/claude/`)는 물리적으로 비중첩이다(structure.md §3 규칙 3·§8, 01 §3.2-E 규칙 3). 본 문서는 Core 경계 밖(Adapter 경계)에 위치하므로, 구체 토큰을 담아도 Core 디렉터리 AI 비의존 불변(INV-4)을 침해하지 않는다 — 오히려 그 격리를 완성한다.
- **소유 경계 준수(07 R4).** 본 산출은 이 1개 파일(`framework/adapters/claude/runtime-binding.md`)만 생성한다. structure.md §6 표의 마지막 행(`framework/adapters/<adapter>/runtime-binding.md`)이 본 Task의 소유 경계이며, Core 4종 문서를 포함한 다른 파일은 수정하지 않는다.

---

## §6. Advisor 조율 결정 2건 정합 (done 5)

Advisor 조율 결정 2건(config-schema.md §5 주·§7 기록)과 본 문서의 정합을 확인한다. 본 문서는 두 결정을 재정의하지 않고 **물리 실현으로만** 바인딩한다.

### (a) SchemaViolation 대조 스키마 출처 (config-schema.md §5 주 조율 결정)

- **조율 결정 인용(config-schema.md §5).** `SchemaViolation`의 대조 기준: Module scope 값 → 대상 Module Manifest의 `configSchema`(01 §3.2-A, 선택 필드), 부재 시 §2 구조 규칙; Global/Project scope 값 → Module 네임스페이스 키면 그 Module의 `configSchema`, Framework 수준 키는 구조 규칙. 이는 01 §3.2-A·§3.2-B의 조합이며 새 계약이 아니다.
- **물리 실현 바인딩(모순 없음).** 이 환경에서 대조 스키마의 물리 출처는 위 결정을 그대로 따른다 — Module scope 값의 대조 스키마 = 해당 Module 정의 파일이 참조하는 `configSchema`(물리 소스 = §3.3 Module 스코프 소스 = 정의 파일 설정 블록). Framework 수준 키의 대조 = config-schema.md §2 구조 규칙(스코프 태깅·`target` 유효성·트리 형태). **본 문서는 대조 스키마의 물리 출처만 지시하며, 어느 스키마로 대조하는가의 판정 규칙은 config-schema.md §5 결정이 소유한다.**
- **정합 판정.** 본 문서의 SchemaViolation 서술은 config-schema.md §5 주의 조율 결정과 **모순되지 않는다** — 대조 출처를 Module의 `configSchema` 또는 구조 규칙으로 이원화한 §5 결정을, 물리 소스(정의 파일 설정 블록 / 구조 규칙) 매핑으로 그대로 반영한다.

### (b) `retry.limit` 물리 소스 위치 (config-schema.md §7 DP-1 결정)

- **결정 인용:** `retry.limit`, 기본값 2, 기본값 스코프 Global(config-schema.md §7).
- **물리 소스 지시(§3.3 재확인):** `retry.limit`의 Global 기본값(2)은 Config **Global 스코프 소스** 중 실재 소스 `~/.claude/settings.json`(§2 #5)에 소속됨을 §3.3에서 지시했다. (`~/.claude/CLAUDE.md`는 지원되는 선택적 Global 소스이나 현 시점 미존재이므로 기본값 소속 소스가 아니다.) 물리 표기 규약(Global 소스 프레임워크 설정 네임스페이스 아래 `retry.limit` = 2)은 이 Adapter Binding 문서 소관(config-schema.md §7 "물리 표기·명명 관례는 Adapter Binding 문서 소관")으로서 여기서 확정했다.
- **정합 판정.** 값(2)·기본값 스코프(Global)·override 우선순위(Module > Project > Global)는 전부 config-schema.md §7·§4.2를 인용만 하며 재정의하지 않는다. 한도 초과 판정 규칙은 03 §3.1-B 소관으로 불변임을 명시했다.

---

## §7. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 첫 산출물. 01 §4(§4.1 바인딩 표·§4.2 이식 교체 지점)의 **v0.3 환경 실현 매핑**. 정본 = 01 §3·§4 + Core 4종(본 문서는 인스턴스 매핑, 재정의 아님 — §0).
- §2: 01 §4.1 표 **10행 전부**를 v0.3 구체 표면으로 매핑(실재/규약/형태 B 구분).
- §3: Core 4종 각각의 "추상 계약 → 물리 실현" — Manifest 직렬화(§3.1)·Registry 4연산(§3.2)·Config 3스코프+`retry.limit`(§3.3)·Bootstrap~Shutdown 세션/턴(§3.4).
- §4: 01 §4.2 교체 지점 1~7의 "교체되는 것 / 유지되는 것(정본 § 불변)". 유지 열이 이식 불변성(C-1)을 재확인.
- §5: structure.md `<adapter>` = `claude` 구체화. 구체 토큰은 이 경계에만, Core 4종엔 소관 포인터만.
- §6: Advisor 조율 결정 2건(SchemaViolation 대조 출처·`retry.limit` Global 소스)과 정합 — 둘 다 재정의 없이 물리 실현으로만 바인딩.
- 하네스는 Bootstrap 상태(형태 A) — Registry·수명주기는 규약 실현이며, 형태 B(실행 코드) 전환에도 01 §3 Core Contract 변경은 0이다(structure.md §7 C-1).
- Glossary 용어 신설 0건. 새 바인딩 계약 창설 0건(§0). 구체 AI·환경·형식 토큰은 이 Adapter 경계에서 허용된다.
