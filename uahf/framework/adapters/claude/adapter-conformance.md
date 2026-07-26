# framework/adapters/claude/adapter-conformance — Claude Code Adapter 적합성(Conformance) 판정

작성일: 2026-07-06
상태: v1.2 Baseline (r4) — 개정 이력·직전 기준선·CP2/CP3 승인 기록의 정본은 **git 커밋(커밋 메시지·앵커)**이다(규범 = `docs/spec-versioning-policy.md` §3).
상위 규약: AGENT.md
근거 정본:

- specs/11-adapters.md §3.1(Judge Conformance C1~C3)·§3.2-A(BP-1~BP-17 바인딩 지점 목록)·§3.2-B(Valid(Full)/Valid(Minimal)·최소 바인딩 부분집합 13개)·§3.2-C(Adapter 구조 규격)·§3.2-D(Conformance Report 6필드)·§4.1(Claude Code 바인딩 값)·§3.3(INV-1~INV-8). **Frozen(v0.1 기준선). 본 문서가 실현·판정하는 계약의 정본이며, 재정의·확장하지 않고 § 포인터로만 인용한다.**
- specs/01-runtime.md §3.2-E(디렉터리/구조 규격)·§4.1(Claude Code Binding 표) — BP-1~5의 원천 계약·물리 정본. § 포인터로만 참조.
- specs/02-agent.md §3.2-A(역할 경계)·§4.1(Agent 정의 파일·공통 규약·실행 모델·위임/보고 채널)·§4.2(SP-1~SP-5) — BP-7~11 실현의 정본 근거(agent-binding.md가 정식화한 원천). § 포인터로만 참조.
- specs/12-scaffold.md §1·§2·§4.1·§5(DP-A3 근거) · specs/13-harness.md §4.1(harness-binding 배정 근거) · specs/00-glossary.md §3.2(Adapter Interface·바인딩 지점·Conformance·완전/최소 구현 Adapter·핵심 루프 표제어 정본 — 새 용어 신설 0). § 포인터로만 참조.
- framework/adapters/claude/ **자매 Adapter Binding 문서**(UAHF spec 바인딩): runtime·memory·verifier·loop·workflow·hooks·skills·plugins·agent·harness·scaffold-binding.md. 각 BP의 물리 실현 소스이며, 본 문서는 그 실현을 커버리지로 대조만 하고 재정의하지 않는다.
- framework/adapters/claude/ **UAF 정본(entry·discovery·planning/specs) 바인딩**: contract·entry·discovery·solution-design-binding.md. **이 집합은 위 자매 집합 계수에 합산하지 않는다** — UAF 정본의 물리 실현이며 specs/11 §3.2-A BP-1~17 커버리지 대상이 아니고, 본 문서 Conformance 판정(verdict·C1~C3·6필드)에 무영향이다(DP-X4). 실현 소스로 인용·대조하지 않는다.
- docs/delegation-protocol.md §3 — 위임/보고 물리 채널 운용(§3.1 위임·§3.2 최종 응답·§3.3 병렬 Wave·§3.4 반환·에스컬레이션). BP-10·BP-11 실현의 정본 근거(agent-binding.md §4가 정식화).
- .claude/AGENT.md(상위 규약)·.claude/CLAUDE.md(Advisor 진입점)·.claude/agents/ 4종(advisor·planner·verifier·worker.md) — BP-7·BP-8·BP-9의 실물 실측 대상.
- 판정 근거로 인용하던 삭제 산출물(검증 리포트·docs/ 시연 소산·loop-data 데모 데이터)은 산출물 수명 정책(docs/artifact-lifecycle-policy.md §7)으로 아카이브 — 앵커 `cd9247b` 열람. 해당 인용은 그 시점 스냅샷 기준이며 C1~C3 판정 논리·verdict는 불변이다.
- ROADMAP.md v0.9(Adapter Layer 정식화)·v1.0(Adapter Interface 최종 규격) — 완전 Adapter 판정 시연(11 §7)의 마일스톤 근거.

경계·거버넌스 전제(공통 4종 통합): 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서** = 격리 지점이므로 구체 AI·환경·직렬화 형식·물리 경로 토큰이 허용되고 C-3 금지 토큰 규칙이 비적용이다 · 하네스는 Bootstrap 상태이므로 실현을 형태 A(문서·규약)/형태 B(실행 코드)로 구분한다 · 용어는 specs/00-glossary.md 정본만 쓴다 · 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3). 이 허용은 Frozen specs/11 §3 문면을 바꿀 권한이 아니다(인용만). 근거 = `uahf/framework/core/structure.md` §5(C-3)·§2(4경계 배치·소유 계약)·§4(계약·문서 전용 경계·형태 A/B 라벨).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 Frozen specs/11-adapters.md §3(§3.1 Judge Conformance·§3.2-A 바인딩 지점 목록·§3.2-B 적합성 기준·§3.2-C 구조 규격·§3.2-D Conformance Report·§3.3 Invariants)와 §4.1(Claude Code 바인딩 값)이다.** 이 문서는 그 계약의 **환경 실현 커버리지 대조 + Conformance 판정 산출**이며, 계약 요소(바인딩 지점 정의·판정 조건 C1~C3·Report 필드·verdict 값·등급 기준·불변 규칙)를 **재정의·확장하지 않는다**. 계약 요소는 11 § 포인터로만 인용한다.
- **판정이 실재하는 유일한 자리.** 개별 바인딩 지점의 물리 실현 상세는 자매 바인딩 문서가 소유하고, 본 문서는 그 실현을 **17개 바인딩 지점 전체에 대해 하나의 커버리지 매트릭스로 통합·대조**해 Conformance Report를 낸다(11 §1).
- **창설 금지.** 11 §3.2-A **17개 바인딩 지점을 넘어서는 새 BP**를, 11 §3.2-D 6필드를 넘어서는 **새 Report 필드**를, 11 §3.2-B의 `Valid(Full)`/`Valid(Minimal)`/`Invalid`를 넘어서는 **새 verdict 값**을 만들지 않는다. Adapter Interface·Conformance 기준·등급 정의는 전부 11 §3이 소유하며 본 문서는 인스턴스 판정만 낸다.
- **판정 성격(최종 승인 아님).** §3 Conformance Report는 11 §3.1 Judge Conformance 연산의 출력 인스턴스다. **이 산출 자체는 최종 승인이 아니다** — 완료 조건 대조의 독립 판정(CP2 — Verifier, 11 §7)과 최종 승인(CP3 — Advisor, 11 §7)이 뒤따른다(02 §3.2-A, AGENT.md Verification). 본 문서는 verdict를 스스로 확정 승인하지 않고 근거와 함께 제시한다.
- **실측 기반 상태 서술(L-07)·“실재 여부” 3구분.** “실재/부재” 주장은 파일 시스템 확인 후에만 기입하며(§2 “실재 여부” 열·§6 대조 표), 미존재를 실재로·미래 산출물을 현재 실재로 쓰지 않는다. 구분은 물리 실재 / 규약 실현(형태 A) / 형태 B 예정(실행 코드 도입 시) 3종이다. C3(핵심 루프 통과)은 Bootstrap 상태에서 이미 반복 통과했으며(§3 loop_pass), Full/Minimal 판정은 기능 완성이 아니라 “다른 AI에 적용 가능함의 증명”을 목적으로 한다(11 §3.2-B).

---

## §1. 목적

이 문서는 Frozen specs/11의 Adapter Interface(§3.2-A)를 Claude Code Adapter 위에 대조하여 **완전성·불변·루프 통과를 판정**한다(11 §1·§3.1).

책임 = BP-1~BP-17 전건 커버리지 매트릭스(§2) · C1~C3 대조로 **Conformance Report 6필드** 산출(§3 — verdict = **Valid(Full)**) · 정식화 배정표(§4) · Advisor 결정 기록 DP-A2·DP-A3(§5) · 상태 서술 실측 대조(§6).

이 문서는 11 §3의 어떤 계약 요소도 재정의·확장하지 않는다(§0·§7). 새 바인딩 지점·새 Report 필드·새 verdict 값 창설 0건이다.

---

## §2. Adapter Interface 커버리지 매트릭스 — BP-1~BP-17 (done 1)

11 §3.2-A 바인딩 지점 목록의 **17행 전건**을 Claude 물리 실현으로 대조한다. “무엇을 바인딩하는가” 열은 11 §3.2-A 정본 표의 값을 그대로 인용하고, “필수/선택”은 11 §3.2-A 지위를 그대로 보존하며, “물리 실현 지점” 열이 실현 소스(자매 바인딩 문서·§ 포인터·실물 경로)를, “실재 여부” 열이 물리 실재/형태 A/형태 B를 구분한다. “실재” 서술은 파일 시스템 직접 실측 후에만 기입한다(L-07·§6).

| BP | 무엇을 바인딩하는가 (11 §3.2-A 정본 인용) | 필수/선택 | Claude 물리 실현 지점 (정본 문서·§ 포인터 · 실물 경로) | 실재 여부 |
|---|---|---|---|---|
| BP-1 | Module/Plugin Manifest를 대상 환경의 서술자 포맷으로 직렬화 | 필수 | runtime-binding.md §2 #1·§3.1 (Markdown + front-matter 직렬화, 11 §4.1 값). 실물: `.claude/agents/*.md` front-matter | 형식·정의 파일 실재. 7필드 완전 직렬화 인스턴스는 형태 B |
| BP-2 | Module 정의를 로드해 entrypoint를 해소하는 로더 | 필수 | runtime-binding.md §2 #2·§3.2 Resolve (파일 기반 정의 로딩, 11 §4.1 값). 서브에이전트 위임 시 활성 정의 파일 로딩 | 규약 실현(형태 A). 실행 로더는 형태 B |
| BP-3 | Global/Project/Module 스코프 Config의 물리 소스·위치·로딩 메커니즘 | 필수 | runtime-binding.md §2 #4~#6·§3.3 (Config 3스코프 물리 소스). 실물: `~/.claude/settings.json`(Global)·`.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`(Project)·정의 파일 설정 블록(Module) | Config 물리 소스 실재. effective config 로딩은 형태 B |
| BP-4 | Bootstrap~Serve~Shutdown 구간을 담는 실행 프로세스/세션 | 필수 | runtime-binding.md §2 #10·§3.4 (세션/턴 = Bootstrap~Serve~Shutdown 실행 컨테이너). 실물: 현 세션 | 컨테이너 실재(현 세션). 실행 Bootstrap/Shutdown은 형태 B |
| BP-5 | Adapter 산출물과 Core를 물리적으로 분리하는 디렉터리·배치 규약 | 필수 | structure.md §2·§3·§8·runtime-binding.md §5 (Core `framework/core/`·`framework/runtime/` / Adapter `framework/adapters/`·`.claude/`, 물리 비중첩). 실물: 위 4경계 | 실재(경계 물리 분리·비중첩 실측) |
| BP-6 | 확장 Module(확장점·능력·묶음)의 등록·발견·지연 로드·배포 표면 | **선택** | hooks-binding.md §2·§4 · skills-binding.md §2·§3 · plugins-binding.md §2·§3 · runtime-binding.md §2 #3. 실물: `.claude/hooks/`·`.claude/skills/`·`.claude/commands/`(Presentation 진입 표면) | 세 확장 표면 디렉터리 실재. 확장 실물은 v0.8 확장 3종 시연으로 실증. `.claude/commands/` 진입 표면 실재(§4·§6) |
| BP-7 | Advisor/Planner/Worker/Verifier 4역할 정의를 대상 환경 메커니즘으로 제공 | 필수 | **정식화 = agent-binding.md §2 행 1**. 정본 근거(병기): 02 §4.1(Agent 정의 파일) + runtime-binding.md §2 #2(Agent Module 진입점). 실물: `.claude/agents/{advisor,planner,worker,verifier}.md` | 실재(4역할 정의 파일 실측) |
| BP-8 | 공통 규약·시스템 프롬프트·오케스트레이터 진입점 주입 방식 | 필수 | **정식화 = agent-binding.md §2 행 2**. 정본 근거(병기): 02 §4.1(공통 규약 바인딩). 실물: `.claude/AGENT.md`(상위 규약)·`.claude/CLAUDE.md`(Advisor 진입점) | 실재(2파일 실측) |
| BP-9 | 각 Agent 역할의 실행 모델·엔진 지정 | 필수 | **정식화 = agent-binding.md §2 행 3·§3(DP-E8)**. 정본 근거(병기): 02 §4.1(실행 모델 바인딩·SP-3) + loop-binding.md §5.1(역할 실행 모델 참조). 실물: worker.md·planner.md·verifier.md front-matter `model: opus`; advisor.md 세션 상속 | 실재(`model: opus` 3파일·advisor 세션 상속 실측) |
| BP-10 | 위임 메시지를 Agent에 전달하는 호출·오케스트레이션 채널 (병렬 디스패치·재위임 포함) | 필수 | **정식화 = agent-binding.md §2 행 4·6·§4.1**. 정본 근거(병기): 02 §4.1(서브에이전트 위임) + delegation-protocol.md §3.1·§3.3 + workflow-binding.md §5.1(병렬 디스패치) | 규약 실현(형태 A). 병렬 작성 Wave로 실증 |
| BP-11 | 완료 보고·실패 보고를 반환하는 결과 채널 | 필수 | **정식화 = agent-binding.md §2 행 5·§4.2**. 정본 근거(병기): 02 §4.1(서브에이전트 최종 응답) + delegation-protocol.md §3.2·§3.4 | 규약 실현(형태 A). 반복 보고 회수로 실증 |
| BP-12 | Memory Service 영속성 백엔드 (단일 Port 뒤) | **선택** | memory-binding.md §2·§3 (파일 기반 store·index·직렬화·I/O, 단일 Port 격리). 실물: `framework/adapters/claude/memory-data/`(store/`<id>.json`·index/index.jsonl) | 실재(memory-data/ 백엔드·데이터 실측) |
| BP-13 | 구조화된 계약 산출물·상태 기록의 직렬화 및 작업 추적·결정 기록 메커니즘 | 필수 | loop-binding.md §3(loop-data 전이 이벤트) · verifier-binding.md §4(검증 리포트 직렬화) · workflow-binding.md §3(Work Graph·Merge Result 문서 형태) · scaffold-binding.md §4(Install Manifest 직렬화 — Markdown + front-matter 6필드). 실물: `framework/adapters/claude/loop-data/`·ROADMAP.md·`scaffold-template/install-manifest.template.md`; 검증 리포트·시연 소산은 앵커 `cd9247b` | 실재(loop-data/ 경로·계획 문서·Install Manifest 템플릿 실측). 검증 리포트 인용은 앵커 `cd9247b` 스냅샷 |
| BP-14 | 사람에게 승인·개입 요청을 제시하고 응답을 받는 채널 | 필수 | loop-binding.md §2 #6·§5.2 (사람 개입 채널). 실물: 주 세션 사용자 제시 + `.claude/CLAUDE.md` "Architecture/Spec 충돌 시 사용자 보고" 규칙(03 §3.1-D 조건 4 바인딩) | `.claude/CLAUDE.md` 조건 4 바인딩 실재. 세션 제시 규약 실현(형태 A) |
| BP-15 | 검증에 쓰이는 검사 도구 (존재 확인·전수 스캔·시연 실행) | 필수 | verifier-binding.md §5 (VT-1~VT-5 검사 도구 바인딩). 실물: 파일 조회·텍스트 검색·명령 실행 도구 표면 | 도구 표면 실재. 검증 리포트(앵커 `cd9247b`)가 실사용 실증 |
| BP-16 | 이벤트 원천의 계측·방출 지점과 확장 실행기(결정적 순서·격리)·원천 컨텍스트 전달 | **선택** | hooks-binding.md §3(이벤트 카탈로그 계측 지점)·§5(Hook Dispatch 물리 절차). 실물: `.claude/hooks/`(등록 표면) + `.claude/settings.json`(훅 선언·실행 배선 — `hooks.SessionStart` 2종·`hooks.PreToolUse` 2종. `uaf-verified: .claude/settings.json 직접 정독`) | 등록 표면·계측 지점·훅 선언 배선 실재. UAHF Dispatch 절차의 결정적 순서·격리 계약 자체는 규약 실현(형태 A) |
| BP-17 | 상황 서술자와 적용 조건의 대조 알고리즘 | **선택** | memory-binding.md §5.2 (applicability 매칭 구현 — 라벨 집합 겹침; 05 §4.1 SP-2). 실물: memory-data/ index `labels` 대조 | 실재(구현 선택 = 라벨 겹침). v0.4~v0.8 회수로 실증 |

주:

- 위 17행은 11 §3.2-A 목록의 전 행이다. 새 바인딩 지점을 창설하지 않는다(§0).
- **필수 13개 / 선택 4개(11 §3.2-B 정본).** 필수 = BP-1·2·3·4·5·7·8·9·10·11·13·14·15(최소 바인딩 부분집합 정본). 선택 = BP-6·12·16·17. 이 구분은 11 §3.2-B가 소유하며 본 표는 그 지위를 인용한다.
- **BP-7~11 정식화.** BP-7~11의 실현은 agent-binding.md(§2 행 1~6·§3 실행 모델·§4 위임/보고 채널·§5 SP-1~SP-5)가 종전 분산 실현(02 §4.1·`.claude/` 실물·runtime-binding.md §2 #2·delegation-protocol.md §3)을 한 문서로 통합·정식화한 것이며, 새 BP·새 계약 창설이 아니다(agent-binding.md §7). 분산 실현 소스는 정본 근거로 병기 유지한다.
- **물리 실재 / 형태 A / 형태 B 구분(정직).** 실물 파일·디렉터리·데이터는 물리 실재다. 위임/보고·역할 실행·Dispatch·사람 개입 등 오케스트레이션은 Bootstrap에서 규약 실현(형태 A)이며, 무인 자동 실행 채널·실행 로더는 형태 B다. 이 구분은 자매 바인딩 문서의 형태 A/B 구분과 정합한다.

---

## §3. Conformance Report (done 2 — 11 §3.2-D 6필드)

11 §3.1 Judge Conformance의 완료 조건 C1~C3을 §2 커버리지에서 대조하여, 11 §3.2-D의 6필드 구조로 Conformance Report를 산출한다. 각 필드의 정의는 11 §3.2-D가 소유하며, 아래는 그 인스턴스 값과 근거다(재정의 0).

| 필드 (11 §3.2-D) | 값 |
|---|---|
| `adapter` | **claude** — 첫 번째 Adapter(11 §4.1, ARCHITECTURE 3.1 "Claude는 첫 번째 Adapter일 뿐이다"). 배치 경로 `framework/adapters/claude/`(DP-A2 — §5). |
| `verdict` | **Valid(Full)** — C1·C2·C3(§3.1)을 모두 만족하고, 선택 바인딩(BP-6·12·16·17)까지 제공(11 §3.2-B 완전 Adapter). |
| `missing_bindings` | **없음** — C1 검사 결과(아래). 필수 13개(BP-1·2·3·4·5·7·8·9·10·11·13·14·15) 전건 실현(§2 커버리지 매트릭스). |
| `core_modifications` | **없음** — C2 검사 결과(아래). Core Contract 수정 0건. |
| `loop_pass` | **예** — C3 검사 결과(아래). 위임 → 구현 → 검증 → 승인 핵심 루프가 v0.2~v0.8 반복 통과. |
| `notes` | 선택 바인딩 4종(BP-6 확장 표면·BP-12 영속성 백엔드·BP-16 이벤트·Hook Dispatch·BP-17 적용 조건 매칭) **전건 제공** → 등급 = **완전 Adapter(Full Adapter)**(11 §3.2-B). |

### §3.1 C1~C3 검사 근거

- **C1 (필수 바인딩 완전성).** 11 §3.2-B 최소 바인딩 부분집합(필수 13개: BP-1·2·3·4·5·7·8·9·10·11·13·14·15)이 §2 매트릭스에서 전건 물리 실현 지점을 갖는다 — 누락 0건. 실현 소스는 자매 바인딩 문서이며(BP-7~11 = agent-binding.md 통합·정식화, BP-13 = scaffold-binding.md §4 병기), 실물 실재는 §6가 확인한다. 정식화는 실현 소스의 통합이지 완전성 판정의 변경이 아니다 — 따라서 `missing_bindings` = 없음(INV-2 충족·verdict 불변).
- **C2 (Core Contract 불변).** Adapter는 바인딩만 추가하고 어떤 Core Contract도 수정·확장·삭제하지 않는다. 근거: (a) 각 마일스톤 CP2 독립 판정이 Core 무변경(Frozen specs·`framework/core`·`framework/runtime` 본체 diff 0)을 실측 — 검증 리포트 열람 = 앵커 `cd9247b`. (b) Core 경계는 계약 문서만 보유하고 AI 의존 요소 0건이다(structure.md §5 C-3·01 §3.3 INV-4). 자매 바인딩 문서·본 문서는 `framework/adapters/claude/` 경계 안에서만 구체 토큰을 격리 보유한다(11 INV-3·INV-1). 따라서 `core_modifications` = 없음.
- **C3 (핵심 루프 통과).** 위임 → 구현 → 검증 → 승인 핵심 루프(Glossary·delegation-protocol.md §1)가 이 Adapter 위에서 1회 이상 통과한다. 근거: v0.2 이래 각 마일스톤이 위임(Advisor)→구현(Worker)→독립 검증(Verifier CP2)→최종 승인(Advisor CP3)을 반복 통과했고, 검증 리포트(앵커 `cd9247b` — v0.8 final_verdict = Pass, 충족 29/위반 0/판정 불가 0)와 각 Baseline 승인 기록이 실증한다. 따라서 `loop_pass` = 예.

### §3.2 등급 판정 (11 §3.2-B)

Claude Code Adapter는 C1~C3을 만족(Valid)하고 선택 바인딩 4종(BP-6·12·16·17)을 제공한다 — BP-6 = hooks/skills/plugins-binding.md + `.claude/{hooks,skills,commands}`, BP-12 = memory-binding.md + memory-data/, BP-16 = hooks-binding.md 계측·Dispatch + `.claude/settings.json` 실 배선(§6), BP-17 = memory-binding.md §5.2. 따라서 등급 = **완전 Adapter(Full Adapter)** · verdict = **Valid(Full)**(11 §3.2-B·§7).

### §3.3 판정 성격 재확인

11 §3.1·§7 및 02 §3.2-A 참조 선언 — 재정의 0. **verdict = Valid(Full)은 근거와 함께 제시된 것이며, 본 문서가 스스로 최종 승인 처리한 것이 아니다** — Verifier 독립 판정(CP2)·Advisor 최종 승인(CP3)이 뒤따른다. 조건부·재량 항목을 스스로 통과 처리하지 않는다(§0 판정 성격).

---

## §4. 정식화 배정표 (done 3)

BP-7~11의 정식화와 인접 표면(13 §4.1 조합·12 §4.1 Scaffold·Presentation 진입 표면)의 배정이다. 각 배정 대상은 W2(Task T3·T4·T5)에서 생성 완료되어 실재하고, §2·§6가 그 실물 § 포인터로 정합화되었다(격리 갱신 T15). 배정 대상의 계약 표면은 정본(02·13·12)이 소유하며 본 문서는 § 포인터로 대조만 한다(재정의 0).

| 배정 대상 (이행 — 실재) | 배정 BP·정본 § | 실현한 interfaceContract (§ 포인터) | 소유 경계 (ownedBoundary) | 이행 Task · 실물 § 포인터 |
|---|---|---|---|---|
| `agent-binding.md` | BP-7~BP-11 (02 §4.1 바인딩 표·§4.2 SP-1~SP-5) | Agent Component의 Claude 물리 실현 — Agent 정의 파일·상위 규약 바인딩·실행 모델 지정·서브에이전트 위임/최종 응답 채널(02 §4.1). 계약 표면은 02 소유. | `framework/adapters/claude/agent-binding.md` | T3 — §2(02 §4.1 표)·§3(실행 모델·DP-E8)·§4(위임/보고 채널)·§5(SP-1~SP-5). |
| `harness-binding.md` | 13 §4.1 조합 (7행) | Harness 최소 구성 5요소(13 §3.2-A)의 Claude 조합 물리 실현 — agent·runtime-binding 실현을 조합 참조. 계약 표면은 13·02·01 소유. | `framework/adapters/claude/harness-binding.md` | T3 — §2(조합 표)·§3(최소 구성 5요소)·§4(이식 교체 지점)·§5(전이 조건 판정 비수행 — T11 소관). |
| `scaffold-binding.md` · `scaffold-template/` | 12 §4.1 Scaffold 표면 (10행) | Scaffold 설치·초기화 표면의 Claude 물리 실현 + 프로젝트 템플릿(12 §3.2-A) 물리 자산. Scaffold는 Bootstrap 이전 설치 도구(DP-A3·§5). 계약 표면은 12 소유. | `framework/adapters/claude/scaffold-binding.md` + `.../scaffold-template/` | T4 — §2(12 §4.1 표)·§3(3연산)·§4(Install Manifest 직렬화)·§5(CK-1~CK-8)·§6(scaffold-template/ 정본). |
| `.claude/commands/` (Presentation 진입 표면) | BP-6 확장 (11 §3.2-A 확장 Module 표면) | 사용자 대면 명령 진입 표면의 물리 실현(Presentation Layer). 확장 계약 표면은 08·09·10 및 Presentation 소관. | `.claude/commands/` 이하 | T5 — `.claude/commands/` 실물(형태 A 문서 명령). §2 BP-6 행에 반영. |

주: 각 배정 대상의 소유 경계(ownedBoundary)는 파일·디렉터리 단위로 쌍별 교집합 0이다(07 R4·INV-2). BP-7~11은 최초 시점에도 분산 실현으로 물리적으로 완전했고 agent-binding.md가 그것을 통합·정식화했다 — 새 BP·새 계약 창설이 아니며 커버리지·verdict는 불변이다.

---

## §5. Advisor 결정 기록 (done 4 — DP-A2·DP-A3)

아래 두 결정의 **주체는 Advisor**이며, 본 문서는 그 결정을 **기록만** 한다(Worker는 Architecture·설계 결정을 하지 않는다 — 02 §3.2-A·INV-3). 두 결정은 Frozen specs/11·01을 **무변경**으로 유지하며 정본 문면의 표기·구조를 해소·확인하는 성격이다(계약 재정의 아님).

### DP-A2 — `adapters/claude/` 표기의 물리 경로 축약 해소

- **결정.** specs/11 §3.2-C·§4.1의 `adapters/<이름>/`·`adapters/claude/` 표기는 물리 경로 `framework/adapters/<이름>/`·`framework/adapters/claude/`의 **축약 표기로 해석한다.** Frozen 11 문면은 수정하지 않는다.
- **물리 정본.** 01 §4.1(Adapter Binding 산출물) · structure.md §2(Adapter 경계) · runtime-binding.md §5(`<adapter>` = `claude` 구체화). §2 BP-5 행이 이 물리 경로를 실물로 담는 자리다.

### DP-A3 — `framework/scaffold/` 미신설

- **결정.** `framework/scaffold/` 디렉터리를 **신설하지 않는다.** Scaffold의 물리 실현은 scaffold-binding.md·scaffold-template/(§4)와 12 §4.1 바인딩 값으로 실현한다.
- **근거.** 01 §4.1 Module 구현 디렉터리 5종 고정 열거 보존 · 12 §1·§2·§5(Scaffold = Runtime Bootstrap **이전**에 동작하는 설치 도구이며 Runtime이 호스팅하는 Module이 아니다). 결정 경위·동형 판례(v0.8 DP-E1·DP-W4·DP-E6) = git 앵커 90ca19c.
- **실측 정합(§6).** `framework/` 하위에 `scaffold/`는 부재이며 이 결정과 정합한다.

---

## §6. 상태 서술 실측 대조 (done 6 — A5/L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 본 문서의 “실재/부재” 서술을 파일 시스템과 직접 대조한 결과다. 표는 **불변 주장**만 담는다 — 날짜 박힌 byte·파일 수 스냅샷은 재기록하지 않는다(재stale 유형). 종전 스냅샷 판 = git 앵커 90ca19c.

| 대상 | 불변 주장 |
|---|---|
| `framework/adapters/claude/` 자매 바인딩 문서 (§2 실현 소스 — UAHF spec 바인딩) | 실재. 각 BP의 물리 실현 소스이며 본 문서는 커버리지 대조만 한다(재정의 0). |
| `framework/adapters/claude/` UAF 정본 바인딩 (contract·entry·discovery·solution-design-binding) | 실재하나 자매 집합 계수에 **미합산**(DP-X4). specs/11 BP-1~17 커버리지 대상 아님 · Conformance 판정 무영향. |
| `.claude/agents/` 4역할 정의 파일 (BP-7) | 실재 — advisor·planner·worker·verifier.md가 4역할과 1:1 대응. |
| `.claude/AGENT.md`·`.claude/CLAUDE.md` (BP-8) | 실재 — 상위 규약·Advisor 진입점. |
| 역할별 실행 모델 지정 (BP-9) | 실재 — worker·planner·verifier.md front-matter `model: opus`; advisor.md는 model 라인 부재(세션 상속). |
| `.claude/hooks/`·`.claude/skills/`·`.claude/commands/` (BP-6·BP-16) | 실재 — 세 확장 표면 디렉터리. |
| `.claude/settings.json` (BP-16 훅 선언·실행 표면) | **실재** — `hooks.SessionStart`(matcher `startup\|resume\|clear`)에 command 훅 2종, `hooks.PreToolUse`(matcher `Write\|Edit\|MultiEdit`)에 command 훅 2종이 배선되어 있다. 따라서 BP-16의 훅 선언·실행 표면은 형태 B 예정이 아니라 실 배선이다. `uaf-verified: .claude/settings.json 직접 정독` |
| `framework/adapters/claude/memory-data/` (BP-12) | 실재 — `store/`·`index/` Memory 백엔드. |
| `framework/adapters/claude/loop-data/` (BP-13) | 백엔드 경로는 계약 서술로 유지. 데모 사이클 데이터는 산출물 수명 정책으로 제거 — 앵커 `cd9247b` 열람. |
| 검증 리포트 (BP-13·C2·C3 근거) | 산출물 수명 정책으로 제거 — 앵커 `cd9247b` 열람. 판정 근거 정합은 불변. |
| `framework/core/`·`framework/runtime/` (C2 Core 경계) | 실재 — 계약 문서만 보유하고 AI 의존 요소 0건을 유지하는 대상. |
| `framework/scaffold/` (DP-A3) | **부재** — 미신설 결정과 정합. |
| §4 배정 대상 (agent·harness·scaffold-binding·scaffold-template/·`.claude/commands/`) | W2(T3·T4·T5) 이행으로 실재. §2·§4·§6가 실물 § 포인터로 정합. 종전 실측 스냅샷 = git 앵커 90ca19c. |

- **핵심 구분.** 실재를 주장하는 행은 파일 시스템 직접 실측 후에만 기입한다. 미존재를 실재로, 실재를 미존재로 쓰지 않는다(A5/L-07 재발 방지). 이 표의 불변 주장이 §2·§3·§5 판정의 근거가 실재함을 뒷받침한다.

---

## §7. 정본 경계·격리·계약 소유 (self-note)

- **소유 경계 = 인스턴스 판정뿐 (재정의·확장 0).** 본 문서의 모든 서술은 11 §3(Adapter Interface·Conformance·구조 규격)의 **인스턴스 대조·판정**이다. 바인딩 지점 정의·판정 조건(C1~C3)·Report 필드·verdict 값·등급 기준·불변 규칙의 정본은 11 §3이며, 개별 바인딩 지점의 물리 실현 상세는 자매 바인딩 문서가 소유한다. **새 BP·새 Report 필드·새 verdict 값·새 등급 창설 0건**이고 Frozen specs(11·01·02·12·13)를 수정하지 않았다.
- **격리 토큰의 단일 자리.** 구체 AI·환경·직렬화 형식·물리 경로 토큰은 이 Adapter 경계 문서에만 둔다 — Core 경계(`framework/core/`·`framework/runtime/`)·Module 구현 디렉터리·specs/11 §3은 이 토큰을 본문에 두지 않는다(structure.md §5 C-3, 11 INV-7). 이 문서는 그 격리의 반대편(허용 지점)이며, 그것이 11 §3 문면 재정의 권한을 뜻하지는 않는다(§0).
- **판정 성격.** §3 verdict = Valid(Full)은 근거와 함께 제시된 산출이며, Verifier 독립 판정(CP2)·Advisor 최종 승인(CP3)이 뒤따른다(02 §3.2-A).
- **작성 시점 감사 기록**(금지 토큰 자가 스캔 · 형제 Task 산출물 불인용(07 R2) · 단일 파일 수정(07 R4) · 추측 0·미존재 미기입) = git 앵커 90ca19c 열람.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-AC-1 — 해소·이행 완료.** §2 BP-7~11 실현 지점을 agent-binding.md § 포인터로 정합화하는 격리 갱신(T15)이 이행됐다. 실현 소스의 정식화이지 verdict 변경이 아니므로 비차단으로 해소됐다.
- **OQ-AC-2 (Presentation Layer 매핑 확정 — 비차단).** `.claude/commands/`(BP-6 확장)의 Layer 귀속은 12 §9-OQ1·13 §2가 Advisor 확정으로 미룬 사안과 인접한다(Glossary §9-OQ6 흐름). 본 문서는 BP-6 확장 표면의 Presentation 국면으로만 배정하고 Layer 귀속 정본을 단정하지 않는다 — Advisor 확정 대상.
