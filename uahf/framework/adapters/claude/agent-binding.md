# framework/adapters/claude/agent-binding — Claude Code Agent Adapter 바인딩

작성일: 2026-07-06
상태: v0.9 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/02-agent.md §4.1 — Claude Code Binding 표(Agent 정의 파일·공통 규약 바인딩·실행 모델 바인딩·위임 메커니즘·보고 회수·컨텍스트 전달). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/02-agent.md §4.2 — 이식 교체 지점 SP-1~SP-5. 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/02-agent.md §3.1·§3.2·§3.3 — 공통 의무(O1~O5)·역할 경계(§3.2-A)·위임/완료/실패 보고 메시지(§3.2-B/C/D)·Invariants(INV-1~INV-8). 본 문서가 준수·대조하는 계약. 재정의하지 않고 § 포인터로만 인용한다.
- framework/adapters/claude/adapter-conformance.md (T1 확정본) §2(BP-7~11 커버리지 매트릭스)·§4(정식화 배정표 — agent-binding.md(T3)에 BP-7~11·02 §4.1·§4.2 배정). **본 문서는 그 배정의 이행이다.** BP-7~11의 현행 분산 실현을 한 문서로 통합·정식화하는 배정 대상.
- framework/adapters/claude/runtime-binding.md (v0.3 Baseline) §2 #2·§3.2 — Agent Module 진입점(= Runtime generic Module 계약의 Agent 구현 바인딩)·Register/Resolve 수행 방식(서브에이전트 위임 시 활성 정의 파일 로딩)의 선행 관례. BP-7~11 현행 분산 실현 소스의 하나.
- framework/adapters/claude/verifier-binding.md (v0.5 Baseline) §2·§3.1 — Agent Module = 서브에이전트 디스패치(Register/Resolve) 관례·형태 A/B 정직 구분·실측 대조(§7) 관례. framework/adapters/claude/loop-binding.md (v0.7 Baseline) §2·§5.1 — 역할 실행(CP1=Worker·CP2=Verifier·CP3=Advisor) 물리 채널·전이 유발 위임/최종 응답 관례. 자매 바인딩 관례 표본.
- docs/delegation-protocol.md §3 — 이 프로젝트의 물리 채널 바인딩 관행(위임 = 서브에이전트 디스패치 §3.1, 보고 = 최종 응답 §3.2, 병렬 Wave §3.3, 반환·에스컬레이션 §3.4). BP-10·BP-11의 현행 분산 실현 소스.
- .claude/AGENT.md(상위 규약)·.claude/CLAUDE.md(Advisor 진입점 바인딩)·.claude/agents/{advisor,planner,worker,verifier}.md(4역할 정의 실물) — BP-7·BP-8·BP-9의 실물 실측 대상. 본 문서는 참조·실측만 하고 수정하지 않는다.
- framework/core/structure.md §2·§5 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·금지 토큰 규칙. 본 문서 경계·격리 방향 반전의 근거.
- specs/00-glossary.md — 용어 정본(역할 정의 §3.2-E·Layer 스택 §3.2-A). 본 문서는 새 용어를 신설하지 않는다.
- ROADMAP.md v0.2(Agent Harness Bootstrap — Agent 정의 파일 산출물)·v0.9(Adapter Layer 정식화). 본 문서의 정식화 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 02 INV-7, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로·실행 모델 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형). 단 이 문서는 Core Contract(02 §3)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.9 Draft | 최초 작성. `framework/adapters/claude/` 경계의 산출물 — BP-7~11의 현행 분산 실현(02 §4.1 + `.claude/` 실물 + runtime-binding.md §2 #2 + delegation-protocol.md §3)을 한 문서로 통합·정식화(adapter-conformance.md §4 배정 이행). 02 §4.1 바인딩 표 **전 항목**(Agent 정의 파일 4종·공통 규약 바인딩 2문서·실행 모델 바인딩·위임 메커니즘·보고 회수·컨텍스트 전달)을 물리 실현("물리 실현" 열 + "실재 여부" 열, 형태 A/B 정직 구분)으로 매핑하고 BP-7~11 각각과의 대응 명시(§2, adapter-conformance.md §2 인용). 실행 모델 행 **실측 반영**(§3) — worker.md `model: opus`(02 §4.1 Worker=Opus 기저 바인딩)·planner.md/verifier.md `model: opus`(DP-E8 — 사용자 결정 2026-07-06, v1.0까지 영구 관행)·advisor.md 세션 상속(model 라인 부재). 위임·보고·컨텍스트 물리 채널(Agent Module = 서브에이전트 디스패치·최종 응답, delegation-protocol.md §3)(§4). 02 §4.2 이식 교체 지점 SP-1~SP-5 대응 표("교체되는 것/유지되는 것" — 자매 관례 동형, §5). 상태 서술 실측 대조 표(§6 — 실재 서술 전건 파일 시스템 직접 실측 후 기입, L-07). 02 §3 계약 재정의·확장 0·새 바인딩 계약 창설 0·Frozen specs 계수 15·Glossary 밖 새 용어 0. 형제 Task(PS2) 산출물 불인용(07 R2). 이 1파일만 생성(harness-binding.md와 함께 Task T3 소산) — 자매 바인딩 문서·specs/·docs/·.claude/ 무수정(07 R4). | Worker (Advisor 위임, Task T3) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지). 삭제 산출물 참조 없음(§7 "불인용" 스캔 노트의 v0.9-install-guide 언급은 시점 기록으로 유지). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/02-agent.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(공통 의무·역할 경계·메시지 필드·Invariants·바인딩 지점)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 02 §4.1이 "각 spec §4에 분산 정의된 바인딩"으로 둔 Agent Component의 물리 실현이 실재하는 자리이며, adapter-conformance.md §2가 "BP-7~11은 현행 분산 실현"으로 명시하고 §4가 "agent-binding.md(T3)로 통합·정식화"로 배정한 지점의 이행이다. 개별 실물(정의 파일·규약 문서)의 존재는 실물 파일이 소유하고, 본 문서는 그 실물을 02 §4.1 바인딩 표·BP-7~11 위에 **하나의 물리 실현 매핑으로 통합·대조**한다.
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 02 INV-7). 이 문서는 그 **반대편**이다 — 구체 토큰(진입점 정의 파일 경로 `.claude/agents/…`, 규약 파일 `.claude/AGENT.md`·`.claude/CLAUDE.md`, 직렬화 형식 front-matter, 실행 모델 지정 `model: opus`, 서브에이전트·세션/턴 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(runtime-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형). **단 이 허용은 02 §3 계약 문면을 바꿀 권한을 뜻하지 않는다** — 02는 무변경, 인용만 한다.
- **창설 금지.** 이 문서는 02 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. BP-7~11의 현행 분산 실현을 통합·정식화하는 매핑으로 한정한다. 새 역할·새 메시지 필드·새 Invariant·새 SP·새 실행 모델 의미를 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, delegation-protocol.md §0, runtime-binding.md §0). 4역할은 정식 실행 Module이 아니라 규약 문서(02·`.claude/agents/` 4종)와 관행(Advisor가 서브에이전트 위임으로 역할을 구동, delegation-protocol.md §3)으로 실현된다(형태 A). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(4역할 정의 파일·규약 2문서·실행 모델 지정 — §6 실측)과, **규약으로 수행되는 위임·보고·컨텍스트 전달**(형태 A), **실행 코드 도입 시 로딩될 지점**(형태 B — 무인 자동 오케스트레이션·실행 로더)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(Active Lesson L-07 — 상태 서술은 실측 후 기록, A5 재발 방지). §2 "실재 여부" 열과 §6 실측 대조 표의 전 행은 파일 시스템 직접 실측(2026-07-06)에 근거한다 — 미존재를 실재로, 미래 산출물을 현재 실재로 쓰지 않는다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Advisor·Planner·Worker·Verifier 4역할은 Glossary §3.2-E 정본이며, Agent Layer는 Glossary §3.2-A 스택 정본이다. 본 문서는 그 물리 실현 매핑만 낸다. `형태 A/B`는 structure.md 서술 라벨의 인용이며 Glossary 표제어가 아니다. `DP-E8`은 본 문서가 기록하는 Advisor 결정 라벨이다(§3). 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 02 §4.1(Agent Claude Code Binding)을 이 환경 위에 **v0.9 시점의 구체 물리 실현**으로 매핑하고, adapter-conformance.md §2의 BP-7~11 현행 분산 실현을 한 문서로 통합·정식화한다(§0, adapter-conformance.md §4 배정 이행).

책임은 다섯 가지다.

- 02 §4.1 바인딩 표의 **전 항목**(Agent 정의 파일 4종·공통 규약 바인딩 2문서·실행 모델 바인딩·위임 메커니즘·보고 회수·컨텍스트 전달)을 물리 표면으로 확정하고, Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을 "실재 여부" 열로 정직하게 구분하며, **BP-7~11 각각과의 대응**을 명시한다(§2, adapter-conformance.md §2 인용).
- 실행 모델 바인딩을 **실측 반영**한다(§3) — worker.md·planner.md·verifier.md `model: opus`, advisor.md 세션 상속. Advisor 결정 DP-E8(planner·verifier 실행 모델)을 **기록만** 한다.
- 위임·보고·컨텍스트 전달의 **물리 채널**(Agent Module = 서브에이전트 디스패치·최종 응답)을 확정한다(§4, delegation-protocol.md §3).
- 02 §4.2 이식 교체 지점 SP-1~SP-5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§5). 그리고 상태 서술을 실측과 대조한다(§6).

이 문서는 02 §3의 어떤 계약 요소도 재정의·확장하지 않는다(§0, §7). 형태 A → 형태 B 전환 시에도 Core Contract(02 §3) 변경은 0이며(structure.md §7 C-1), 이 문서(§5의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 02 §4.1 바인딩 표 물리 실현 · BP-7~11 대응 (done 1)

02 §4.1 Claude Code Binding 표의 **전 항목**을 물리 표면으로 매핑한다. 아래 표의 "02 §4.1 바인딩" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·형식·채널을, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을 정직하게 구분하며(§6 실측 대조), "대응 BP" 열이 adapter-conformance.md §2 커버리지 매트릭스의 바인딩 지점과의 대응을 명시한다. "실재" 서술은 전건 파일 시스템 직접 실측 후 기입했다(L-07).

| # | 02 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 | 대응 BP (adapter-conformance.md §2) |
|---|---|---|---|---|
| 1 | Agent 정의 파일 — 각 역할은 `.claude/agents/*.md`로 정의된다: advisor.md, planner.md, worker.md, verifier.md (ROADMAP v0.2 산출물). | 4역할 Agent Module 정의 파일 = `.claude/agents/{advisor,planner,worker,verifier}.md`(실재). Markdown 본문 + YAML front-matter 직렬화(runtime-binding.md §2 #1 동형). 진입점 내부 역할 계약(위임 입력 in → 보고 out, 역할 경계)은 각 정의 파일 + 02 §3.2-A 소관. 활성화 = 서브에이전트 위임 시 해당 역할 정의 파일 로딩(Resolve — runtime-binding.md §3.2·verifier-binding.md §3.1 Agent Module 동형). | 4역할 정의 파일 실재(§6 실측). 무인 자동 로더(형태 B)는 미도입. | **BP-7** (4역할 정의 제공) |
| 2 | 공통 규약 바인딩 — `.claude/AGENT.md`가 모든 Agent 정의의 상위 규약이다. `.claude/CLAUDE.md`가 Advisor 역할을 프로젝트 진입점에 바인딩한다. | 상위 규약(공통 시스템 프롬프트) = `.claude/AGENT.md`(실재, 모든 정의 파일의 상위 규약). 오케스트레이터 진입점 주입 = `.claude/CLAUDE.md`(실재, Advisor 역할을 주 세션 진입점에 바인딩 — "너는 메인 Advisor다"). 각 `.claude/agents/*.md`는 머리에서 상위 규약을 `.claude/AGENT.md`로, 계약 정본을 02로 지시한다(INV-1). | 2파일 실재(§6 실측). | **BP-8** (공통 규약·시스템 프롬프트·진입점 주입) |
| 3 | 실행 모델 바인딩 — v0.x에서 Worker의 기본 실행 모델은 Opus로 지정한다(`.claude/CLAUDE.md` "Worker(Opus)"). 다른 역할의 모델 지정도 이 바인딩 영역에 속한다. | 역할별 실행 모델·엔진 지정을 정의 파일 front-matter `model` 키로 바인딩한다(Module 스코프 Config — runtime-binding.md §3.3 동형). 실측: worker.md `model: opus`(02 §4.1 Worker=Opus 기저)·planner.md `model: opus`·verifier.md `model: opus`(DP-E8)·advisor.md `model` 라인 부재(세션 상속). 상세는 §3. | 4역할 실행 모델 지정 실재(§3·§6 실측). | **BP-9** (역할 실행 모델·엔진 지정) |
| 4 | 위임 메커니즘 — Advisor는 서브에이전트 위임으로 §3.2-B 위임 메시지를 Worker/Planner/Verifier에게 전달한다. | 위임 = **서브에이전트 위임(디스패치)** 채널로 02 §3.2-B 위임 메시지 8필드를 전달(delegation-protocol.md §3.1). 병렬 디스패치(동시 위임)와 재위임(재작업 지시 라우팅)도 이 채널(delegation-protocol.md §3.3, loop-binding.md §5.1). 상세는 §4. | 규약 실현(형태 A, Bootstrap). v0.2~v0.8 위임 사이클·spec 병렬 작성 Wave로 실증. 무인 자동 디스패치(형태 B)는 미도입. | **BP-10** (위임 메시지 전달·오케스트레이션 채널) |
| 5 | 보고 회수 — §3.2-C 완료 보고와 §3.2-D 실패 보고는 서브에이전트의 최종 응답으로 회수된다. | 보고 회수 = 서브에이전트 **최종 응답** 채널로 02 §3.2-C 완료 보고 5필드 / 02 §3.2-D 실패 보고 5필드를 회수(delegation-protocol.md §3.2). 반환·에스컬레이션(비차단 open_questions·차단 실패 보고)도 이 채널(delegation-protocol.md §3.4). Advisor는 회수한 보고를 그대로 신뢰하지 않는다(02 §3.2-A·INV-4). 상세는 §4. | 규약 실현(형태 A). v0.2~v0.8 보고 회수로 실증. 무인 자동 회수(형태 B)는 미도입. | **BP-11** (완료 보고·실패 보고 반환 채널) |
| 6 | 컨텍스트 전달 — 위임 메시지의 context 필드는 읽어야 할 파일 경로 목록으로 전달된다. | 위임 메시지 context 필드(02 §3.2-B) = 착수 전 정독할 파일 경로 목록(상위 규약·Architecture·관련 spec·Memory 회수 범위). 병렬 집합에서는 확정(Frozen/실재) 문서만 담고 동시 작성 산출물은 담지 않는다(delegation-protocol.md §2.1·07 R2). | 규약 실현(형태 A). 위임 메시지 관행으로 실증. | **BP-10** 부속 (위임 메시지 컨텍스트 전달) |

주:

- 위 6행은 02 §4.1 표의 전 항목이다. 각 행의 "물리 실현"은 02 §4.1 정본 표현을 이 환경의 구체 경로·형식·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **BP-7~11 통합·정식화(무결성).** adapter-conformance.md §2가 BP-7~11을 "현행 분산 실현(02 §4.1 + `.claude/` 실물 + runtime-binding.md §2 #2 + delegation-protocol.md §3)"으로 매핑하고 §4가 agent-binding.md(T3)로 통합·정식화 배정했다. 본 §2가 그 이행이다 — BP-7(행 1)·BP-8(행 2)·BP-9(행 3)·BP-10(행 4·6)·BP-11(행 5)을 한 문서에 통합했다. 이는 **새 계약 창설이 아니라 분산 실현의 통합**이며, 실물 실재는 §6 실측으로 확인된다. adapter-conformance.md §2·§4가 배정 대상 생성 후 예고한 후속 격리 갱신(T15)의 대상이다(비차단 — §7 OQ-AB-1).
- **물리 실재 / 형태 A / 형태 B 구분(정직).** 행 1(4정의 파일)·행 2(규약 2문서)·행 3(실행 모델 지정)은 물리 실재다. 행 4(위임)·행 5(보고 회수)·행 6(컨텍스트 전달)은 Bootstrap에서 **규약 실현(형태 A)**이다 — 서브에이전트 위임/최종 응답으로 수행되며, 무인 자동 오케스트레이션·실행 로더는 형태 B다. 이 구분은 자매 바인딩 문서(runtime·verifier·loop-binding.md)의 형태 A/B 구분과 정합한다.
- **4역할 = Agent Module(서브에이전트 채널).** 4역할은 서브에이전트로 디스패치되는 Agent Module이므로(verifier-binding.md §3.1·loop-binding.md §2 동형), 위임·보고·재위임 전달이 **서브에이전트 위임/최종 응답 채널**로 실현된다. 이는 단일 Port로 소비되는 Cross-cutting Service(Memory)의 Port 소비 경로와 다른 실현 방식이다(§4).

---

## §3. 실행 모델 바인딩 실측 반영 (done 1 상세 — DP-E8 기록)

02 §4.1 실행 모델 바인딩 행(BP-9)의 역할별 지정을 파일 시스템 직접 실측(2026-07-06)으로 반영한다. **역할별 실행 모델 지정 값은 이 Adapter 경계가 소유하는 물리 실현이며(격리 지점 — §0), 그 지정의 의미·판정 계약은 02 §4가 소유한다(재정의 0).** 실행 모델 지정은 이식 교체 지점 SP-3이다(§5).

| 역할 | 정의 파일 | 실행 모델 지정 (실측 — front-matter `model` 키) | 근거 |
|---|---|---|---|
| Worker | `.claude/agents/worker.md` | `model: opus` (실측 — front-matter `model: opus`) | 02 §4.1 기저 바인딩 — "Worker의 기본 실행 모델은 Opus"(`.claude/CLAUDE.md` "Worker(Opus)"). |
| Planner | `.claude/agents/planner.md` | `model: opus` (실측 — front-matter `model: opus`) | **DP-E8**(§ 아래) — 종전 미지정(세션 상속)에서 Opus 명시로 전환. |
| Verifier | `.claude/agents/verifier.md` | `model: opus` (실측 — front-matter `model: opus`) | **DP-E8** + 06 §4.2 SP-6(실행 모델 지정은 02 §4 소관) — 종전 미지정(세션 상속)에서 Opus 명시로 전환. |
| Advisor | `.claude/agents/advisor.md` | **미지정 — 세션 상속** (실측 — front-matter `model` 라인 부재) | 02 §4.1 실행 모델 바인딩 영역(Advisor 결정) — 주 세션 모델을 상속하므로 `model` 라인을 두지 않는다. |

**DP-E8 기록 (Advisor 결정 — Worker는 기록만).** planner.md·verifier.md의 `model: opus` 지정은 Advisor 결정 **DP-E8**(사용자 결정 2026-07-06)이다 — Planner·Verifier의 위임 실행 모델을 Opus로 명시 지정한다(종전: 미지정·세션 상속). 사유는 Fable 사용 한도 절약이며, **v1.0 완료까지 유지하는 영구 관행**이다(planner.md 머리·verifier.md 머리 명시). 본 문서는 이 결정을 **기록만** 하며, 결정 주체는 Advisor다(02 §3.2-A·INV-3 — Worker는 Architecture·설계 결정을 하지 않는다). DP-E8은 02 §4.1 실행 모델 바인딩 영역 안의 인스턴스 결정이며 02 §3 계약을 무변경으로 유지한다(실행 모델 지정은 §4 Adapter Binding 소관 — 02 §4.1).

- **경계.** 역할별 실행 모델 지정은 SP-3(§5) — 대상 환경의 모델·엔진으로 교체되며, 02 §3.2-A 역할 경계·메시지 필수 필드·§3.3 Invariants는 유지된다. worker/planner/verifier의 `opus`·advisor의 세션 상속은 이 환경 표면의 물리 값이며, 다른 AI 환경으로 이식 시 그 환경의 모델·엔진 지정으로 바뀐다(02 §4.2 SP-3 "유지되는 것" 불변).

---

## §4. 위임·보고·컨텍스트 물리 채널 (done 1 상세)

02 §4.1 위임 메커니즘(BP-10)·보고 회수(BP-11)·컨텍스트 전달 행의 물리 채널을 확정한다. **채널 상세는 delegation-protocol.md §3(운용 지침)·02 §4.1(정본)이 소유하며, 본 절은 그 물리 실현을 대조·인용만 한다(재정의 0).** 위임 메시지 필드(02 §3.2-B)·완료/실패 보고 필드(02 §3.2-C/D)는 02 §3이 소유한다.

### §4.1 위임 디스패치 (BP-10 — 02 §4.1 위임 메커니즘 행)

- **채널.** Advisor는 **서브에이전트 위임(디스패치)** 으로 02 §3.2-B 위임 메시지 8필드(from/to/task/input/output/done/context/constraints)를 Worker/Planner/Verifier에게 전달한다(delegation-protocol.md §3.1). 필수 필드(input·output·done·context) 누락 위임은 발신하지 않으며, 누락 시 수임 Agent가 착수 전 반환·질의한다(02 INV-6, delegation-protocol.md §2.4).
- **병렬 디스패치.** 한 병렬 집합(Parallel Set)의 여러 Task를 서브에이전트 **동시 위임**으로 여러 Worker에게 동시에 전달한다(delegation-protocol.md §3.3, 07 R1~R4). 각 Worker는 소유 경계 밖 파일·계약을 수정하지 않고(R4), 동시 작성 산출물을 추측·인용하지 않는다(R2). 이 프로젝트의 spec 병렬 작성 Wave가 이 구조의 실사용 형태다.
- **재위임(재작업 지시 라우팅).** CP2 판정이 Fail/Conditional이면 재작업 지시(06 §3.2-D)가 재위임 메시지에 실려 Worker 서브에이전트로 라우팅된다(loop-binding.md §5.1, verifier-binding.md §4.2). 라우팅·전이 채널 정본은 03-loop·02 §4다.

### §4.2 보고 회수 (BP-11 — 02 §4.1 보고 회수 행)

- **채널.** 02 §3.2-C 완료 보고 5필드(artifacts/self_check/failures/open_questions/verify_basis)와 02 §3.2-D 실패 보고 5필드(reason/repro/attempted/lesson_candidate/blocking)는 서브에이전트 **최종 응답**으로 회수된다(delegation-protocol.md §3.2).
- **독립 검증 전제.** Advisor는 회수한 완료 보고를 **그대로 신뢰하지 않고** 산출물을 정독해 독립 재검증한다(검증 게이트 — 02 §3.2-A·INV-4, `.claude/CLAUDE.md` "Worker 완료 보고를 그대로 신뢰하지 않는다"). 완료 보고는 Verify 통과(CP2 PASS) 뒤에만 유효하다(02 INV-4).
- **반환·에스컬레이션.** 착수 불능·차단은 실패 보고(02 §3.2-D, blocking=차단)로, 비차단 확인 필요는 완료 보고 open_questions로 최종 응답 채널을 통해 Advisor에게 회수된다(delegation-protocol.md §3.4, 02 O4).

### §4.3 컨텍스트 전달 (02 §4.1 컨텍스트 전달 행)

- **채널.** 위임 메시지의 context 필드(02 §3.2-B)는 착수 전 정독할 **파일 경로 목록**으로 전달된다(delegation-protocol.md §2.1 context). 상위 규약·Architecture·관련 spec·Memory 회수 범위를 담는다.
- **병렬 경계(R2).** 병렬 집합에서는 context에 확정(Frozen/실재) 문서만 담고, 동시 작성 중인 산출물은 담지 않는다(delegation-protocol.md §2.5 R2). 동시 작성 파일이 필요하면 인용하지 않고 R3로 Advisor에게 에스컬레이션한다.

- **Register/Resolve 정합(runtime-binding.md §3.2·verifier-binding.md §3.1 Agent Module 동형).** 4역할의 등록(Register)은 정의 파일 배치(`.claude/agents/*.md`)로 규약 실현되며(형태 A), 해소(Resolve)는 서브에이전트 위임 시 해당 역할의 활성 정의 파일이 로딩되는 것이다. 4역할은 서브에이전트로 디스패치되는 **Agent Module**이므로, Resolve가 Port 소비가 아니라 서브에이전트 디스패치로 실현된다(Memory Cross-cutting Service의 단일 Port 소비 경로와 구별). 이 등록·회수 경로는 이식 교체 지점 SP-1·SP-4·SP-5에 대응한다(§5).

---

## §5. 02 §4.2 이식 교체 지점 SP-1~SP-5 대응 (done 1)

02 §4.2 이식 교체 지점 SP-1~SP-5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인한다.

| # (02 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경(claude) 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Agent 정의 파일 위치·포맷(`.claude/agents/*.md`) → 대상 환경의 Agent 정의 메커니즘 | §2 행 1, §4(Register/Resolve) | `.claude/agents/{advisor,planner,worker,verifier}.md` 정의 파일 위치·포맷(Markdown + front-matter), 서브에이전트 위임 시 로딩(Resolve). | §3.2-A 역할 경계, 진입점 내부 역할 계약(02 §3.2-A), Provider 등록·해소 계약(01 §3.1-A). |
| SP-2 | 상위 규약 바인딩 파일(`.claude/AGENT.md`, `.claude/CLAUDE.md`) → 대상 환경의 규약·시스템 프롬프트 주입 방식 | §2 행 2 | `.claude/AGENT.md`(상위 규약)·`.claude/CLAUDE.md`(Advisor 진입점 바인딩)의 위치·포맷·주입 방식. | 공통 의무(O1~O5)·역할 경계(§3.2-A)·Invariants(§3.3). AGENT.md가 규정하는 공통 규약 자체. |
| SP-3 | 실행 모델 지정(Worker = Opus 등) → 대상 환경의 모델·엔진 | §2 행 3, §3 | 역할별 `model` 지정 — worker/planner/verifier `model: opus`(DP-E8 포함)·advisor 세션 상속. | §3.2-A 역할 경계·§3.2-B/C/D 메시지 필수 필드(02 §4.2 "유지되는 것"). 모델 값 자체는 환경 표면이며 계약이 아니다. |
| SP-4 | 위임 메커니즘(서브에이전트 위임) → 대상 환경의 Agent 호출·오케스트레이션 API | §2 행 4·6, §4.1 | 서브에이전트 위임(디스패치)·병렬 동시 위임·재위임 라우팅(delegation-protocol.md §3.1·§3.3). | 위임 메시지 8필드(§3.2-B)·INV-6(필수 필드 완전성). 병렬 규칙 R1~R4(07 §3.2-C). |
| SP-5 | 보고 회수 방식(서브에이전트 최종 응답) → 대상 환경의 결과 반환 채널 | §2 행 5, §4.2 | 서브에이전트 최종 응답으로 완료/실패 보고·반환·에스컬레이션 회수(delegation-protocol.md §3.2·§3.4). | 완료 보고 5필드(§3.2-C)·실패 보고 5필드(§3.2-D)·INV-4(Verify 통과 후 완료 보고)·INV-5(실패 은폐 금지). |

- "유지되는 것" 열의 계약(역할 경계·공통 의무·메시지 필수 필드·Invariants)은 다른 AI·환경으로 이식해도 바뀌지 않는다 — 02 §4.2 말미 "유지되는 것: §3.2-A 역할 경계, §3.2-B/C/D 메시지의 필수 필드, §3.3 Invariants"의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface(BP-7~11)로 정식화한다(runtime-binding.md §4·verifier-binding.md §6 동형). 본 문서는 그 정식화를 선취하지 않고 v0.9 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §6. 상태 서술 실측 대조 (L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록 — A5 재작업 사례: 미존재를 "실재"로 서술한 것을 파일 시스템 전수 대조로 검출한 데서 도출)에 따라, 본 문서의 "실재/존재/부재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`) + front-matter 직접 실측.**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `.claude/agents/` 4역할 정의 파일 (§2 행 1, BP-7) | 실재 (advisor·planner·worker·verifier.md) | 실재 — 4파일 확인(advisor.md·planner.md·worker.md·verifier.md). |
| `.claude/AGENT.md`·`.claude/CLAUDE.md` (§2 행 2, BP-8) | 실재 (상위 규약·Advisor 진입점) | 실재 — 2파일 확인. `.claude/CLAUDE.md` 머리 "너는 메인 Advisor다"·"Worker(Opus)에게 위임" 확인. |
| worker.md `model: opus` (§3, BP-9) | 실재 (02 §4.1 Worker=Opus 기저) | 실재 — front-matter `model: opus` 확인. |
| planner.md `model: opus` (§3, DP-E8) | 실재 (DP-E8) | 실재 — front-matter `model: opus` 확인. 머리에 DP-E8 명시 확인. |
| verifier.md `model: opus` (§3, DP-E8·06 SP-6) | 실재 (DP-E8) | 실재 — front-matter `model: opus` 확인. 머리에 DP-E8 명시 확인. |
| advisor.md 실행 모델 (§3) | **미지정 — 세션 상속** | 확인 — front-matter `model` 라인 부재. 머리에 "실행 모델은 미지정 — 주 세션 모델을 상속" 명시 확인. |
| `framework/adapters/claude/` 자매 바인딩 문서 (§0·§2 관례 인용) | 실재 (runtime·verifier·loop-binding.md 등 Baseline) | 실재 — runtime-binding.md·verifier-binding.md·loop-binding.md·adapter-conformance.md 등 확인. |
| `framework/adapters/claude/agent-binding.md` (본 문서) | 실재 (본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음(사전 실측 확인). |
| `docs/delegation-protocol.md` (§4 물리 채널 소스) | 실재 (위임/보고 운용 지침) | 실재 — §3(Adapter 바인딩 물리 채널) 확인. |
| Frozen specs 계수 | **15** (numbered 00~13 = 14 + TEMPLATE 1) | 실측 — specs/ = 00~13 numbered 14파일 + TEMPLATE.md = **15**. |
| 형제 Task(PS2) 산출물 (07 R2) | 불인용 (미완성 산출물) | 인용 0건 — scaffold-binding.md·scaffold-template/·.claude/commands/·hooks/plugins-binding §7 개정분 등 미인용 확인(§7). |

- **핵심 구분.** 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로, 미래 산출물을 현재 실재로 쓰지 않았다(A5/L-07 재발 방지). BP-7~11의 현행 분산 실현 실물(4역할 정의·규약 2문서·실행 모델 지정)이 전부 실측으로 확인되어 §2·§3 매핑의 근거가 실재함을 입증한다.

---

## §7. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 02 §3·§4의 물리 실현이다. 어떤 공통 의무·역할 경계·메시지 필드·Invariant·바인딩 지점 정의도 이 문서에서 새로 확정되지 않는다 — 계약 기준은 02 §3·§4가 소유한다. **02 §4.1 표를 넘어서는 새 바인딩 계약·새 역할·새 메시지 필드·새 SP·새 실행 모델 의미를 창설하지 않았다.** BP-7~11의 통합·정식화는 분산 실현을 한 문서로 모은 것이지 새 BP·새 계약의 창설이 아니다(adapter-conformance.md §2 커버리지 무결성 주와 정합).
- **Frozen 무변경.** specs/02(Frozen v0.1)·01·06·13(Frozen)을 수정하지 않았다. DP-E8(§3)은 02 §4.1 실행 모델 바인딩 영역 안의 Advisor 결정 기록이며 02 §3 문면을 바꾸지 않는다. Frozen specs 계수를 표기할 자리에는 **15**(numbered 00~13 = 14 + TEMPLATE 1)로 표기했다.
- **격리 토큰의 단일 자리.** 구체 진입점 경로(`.claude/agents/…`)·규약 파일(`.claude/AGENT.md`·`.claude/CLAUDE.md`)·직렬화 형식(Markdown·front-matter)·실행 모델 지정(`model: opus`)·서브에이전트/세션 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. 02 §3·`framework/core/`·`framework/runtime/`은 이 토큰을 본문에 두지 않는다(structure.md §5 C-3, 02 INV-7). 이 문서는 그 격리의 반대편(허용 지점)이다 — 단 02 §3 문면 재정의 권한은 아니다(§0).
- **판정 성격.** 본 문서는 물리 실현 매핑이며, 완료 조건 대조의 독립 판정(CP2 — Verifier)과 최종 승인(CP3 — Advisor)이 뒤따른다(02 §3.2-A). 자기 점검(CP1)을 최종 승인으로 삼지 않는다.
- **동시 작성 문서 경계(07 R2).** 같은 병렬 집합(PS2)에서 동시 작성 중인 형제 Task의 미완성 산출물(scaffold-binding.md·scaffold-template/·v0.9-install-guide.md·`.claude/commands/`·getting-started.md·specs/00-glossary.md 개정분·hooks-binding.md/plugins-binding.md §7 개정분)을 인용·추측하지 않았다(07 R2). 참조한 확정 정본은 Frozen specs(02·01·06·13·00)·Baseline 자매 바인딩 문서(runtime·verifier·loop-binding.md·adapter-conformance.md)·확정 실물(.claude/AGENT.md·CLAUDE.md·agents/ 4종)·delegation-protocol.md·structure.md·ROADMAP.md뿐이다. 자매 harness-binding.md는 본 Task(T3)의 동반 산출물이다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 이 파일(`framework/adapters/claude/agent-binding.md`)과 자매 harness-binding.md(같은 Task T3)만 생성하며, 자매 바인딩 문서·`framework/core`·`framework/runtime`·specs/·docs/·.claude/ 실물을 수정하지 않는다.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-AB-1 (adapter-conformance.md §2 커버리지 후속 격리 갱신 — 비차단).** adapter-conformance.md §2가 BP-7~11을 "현행 분산 실현(02 §4.1 + `.claude/` + runtime-binding §2 #2 + delegation-protocol §3)"으로 매핑하고 §4·OQ-AC-1이 "agent-binding.md(T3) 생성 후 그 문서 § 포인터로 정합화하는 격리 갱신(T15)"을 예고했다. 본 문서 생성으로 그 배정이 이행되었으므로, adapter-conformance.md §2 BP-7~11 행의 실현 지점을 본 문서 § 포인터로 정합화하는 격리 갱신이 필요하다. 이는 실현 소스의 정식화이지 커버리지·verdict 변경이 아니므로 비차단이다. 본 Task 소유 경계는 이 2파일이므로 adapter-conformance.md를 수정하지 않았다(07 R4).
- **OQ-AB-2 (실행 모델 실측 서술 후속 정합 — 비차단).** DP-E8(planner·verifier `model: opus`)은 사용자 결정 2026-07-06·v1.0까지 영구 관행이다(§3). 관행 만료(v1.0) 또는 변경 시 §3 실측 표·§6 실측 대조 표의 실행 모델 서술을 재실측·정합화해야 한다. 현재 실측(2026-07-06)은 정본과 일치하며, 재정합은 결정 변경 시점의 격리 갱신 사안으로 비차단이다.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 산출물. 02 §4.1(Agent 바인딩 표)의 **v0.9 물리 실현 매핑** + BP-7~11의 현행 분산 실현 통합·정식화(adapter-conformance.md §4 배정 이행). 정본 = 02 §3·§4(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 02 §4.1 표 **전 항목**을 물리 표면으로 매핑("물리 실현" 열 + "실재 여부" 열, 형태 A/B 정직 구분) + BP-7~11 대응. Agent 정의 4파일(BP-7)·규약 2문서(BP-8)·실행 모델 지정(BP-9) = 실재; 위임(BP-10)·보고 회수(BP-11)·컨텍스트 전달 = 규약 실현(형태 A). 4역할 = Agent Module(서브에이전트 채널).
- **§3:** 실행 모델 실측 반영 — worker.md `model: opus`(02 §4.1 기저)·planner.md/verifier.md `model: opus`(**DP-E8** — 사용자 결정 2026-07-06·v1.0까지 영구, Worker는 기록만)·advisor.md 세션 상속(`model` 라인 부재). DP-E8은 02 §3 무변경.
- **§4:** 위임(서브에이전트 디스패치·병렬·재위임)·보고 회수(최종 응답·독립 검증 전제)·컨텍스트 전달(파일 경로 목록·R2 경계)의 물리 채널(delegation-protocol.md §3·02 §4.1 소유, 재정의 0).
- **§5:** 02 §4.2 이식 교체 지점 SP-1~SP-5 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 이식 불변(C-1) 재확인(역할 경계·공통 의무·메시지 필수 필드·Invariants).
- **§6:** 상태 서술 실측 대조(2026-07-06 직접 실측) — 4역할 정의·규약 2문서·실행 모델 지정 실재; 실측 불일치 0건(A5/L-07 재발 방지).
- 02 §3 계약 재정의·확장 0 · 새 바인딩 계약·새 SP·새 실행 모델 의미 창설 0 · Frozen specs 계수 15 · Glossary 밖 새 용어 0. 구체 AI·환경·실행 모델 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 형제 Task(PS2) 불인용(07 R2). 이 파일 + 자매 harness-binding.md(Task T3)만 생성(07 R4).
