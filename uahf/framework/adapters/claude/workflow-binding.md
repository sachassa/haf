# framework/adapters/claude/workflow-binding — Claude Code Workflow Adapter 바인딩

작성일: 2026-07-06
상태: v0.8 Baseline (개정 — §7 시연 소산 실재 반영 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06). 직전 기준선: v0.7 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/07-workflow.md §4.1 — Claude Code Binding 표(7행). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/07-workflow.md §4.2 — 이식 교체 지점 SP-1~SP-4와 "유지되는 것" 목록. 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/07-workflow.md §3.1·§3.2·§3.3 — 분해·디스패치·병합 연산·데이터 포맷(Work Graph·Task·Parallel Dispatch Protocol·Merge Result·공통 Failure Report)·불변 규칙(INV-1~INV-9). 본 문서가 준수·대조하는 계약. 재정의하지 않고 § 포인터로만 인용한다.
- framework/workflow/work-graph.md (WF1 확정본) — Work Graph(07 §3.2-A)·Task(07 §3.2-B)·공통 Failure Report(07 §3.2-E) 세 정의 포맷의 인스턴스 소유 문서. 세 포맷의 직렬화 형식·물리 위치·물리 경로를 Adapter Binding 문서 소관으로 위임(§5). 본 문서 §3이 그 물리 정본(문서 형태).
- framework/workflow/module-manifest.md (WF2 확정본) — Workflow Provider Module 등록 서술자(`id`=`workflow-provider`·`contract`=`WorkflowInterface`·`requires`=`LoopInterface`·`entrypoint` 추상 참조). `entrypoint`(분해·디스패치·병합 연산 노출)·`requires`=`LoopInterface` 물리 해소를 Adapter Binding 소관으로 위임(§4). 본 문서 §4가 그 물리 해소.
- framework/workflow/decompose-rules.md (WF3 확정본) — Decompose 연산(07 §3.1-A) 규칙 인스턴스. 분해 수행 주체의 물리 채널·산출 Work Graph의 직렬화 형식·물리 위치를 Adapter Binding 소관으로 위임(§3·§6). 본 문서 §4·§5가 그 물리 채널.
- framework/workflow/dispatch-protocol.md (WF4 확정본) — Dispatch 연산(07 §3.1-B)·병렬 디스패치 프로토콜(07 §3.2-C R1~R4) 규칙 인스턴스. 핸들(Task id → 수임 Agent 매핑)의 물리 실현·병렬 동시 위임의 물리 디스패치 채널을 Adapter Binding 소관으로 위임(§2.3·§4). 본 문서 §5가 그 물리 채널.
- framework/workflow/merge-rules.md (WF5 확정본) — Merge 연산(07 §3.1-C)·Merge Result(07 §3.2-D)·충돌 처리 순서 규칙 인스턴스. 병합 결과 수합·상호 참조 대조·충돌 중재 진입점의 물리 채널·직렬화·물리 위치를 Adapter Binding 소관으로 위임(§4.4·§6). 본 문서 §3·§5가 그 물리 채널·직렬화 정본.
- framework/adapters/claude/loop-binding.md (v0.6 Baseline · 현행 v0.7 Draft 개정) — 자매 Adapter Binding 문서(관례 정본). 격리 지점 방향 반전(§0)·7행 물리 실현 표 관례(§2)·구조 제안·근거 서술 관례(§3.1)·`entrypoint`·`requires` 물리 해소 표 관례(§4)·SP 대응 표 관례(§6)·실측 대조 표 관례(§7). **`LoopInterface` 물리 해소(Loop Provider `entrypoint` = 사이클 구동 연산의 형태 A 규약 실현)의 정본**(loop-binding.md §4.1) — 본 문서 §4.2(`requires`=`LoopInterface` 행)는 그 실현을 참조만 하고 재정의하지 않는다.
- framework/adapters/claude/memory-binding.md (v0.4 Baseline) — 자매 Adapter Binding. **Memory 백엔드(`framework/adapters/claude/memory-data/`)의 물리 실현 정본** — 본 문서 §5(Memory 접근)는 그 백엔드 경유를 참조만 하고 재정의하지 않는다. M5 draft 시점 "데이터 미생성, 시연 시 생성 예정" 관례.
- framework/adapters/claude/verifier-binding.md (v0.5 Baseline) — 자매 Adapter Binding. Agent Module = 서브에이전트 디스패치(Register/Resolve) 관례·형태 A/B 정직 구분·실측 대조 관례. **개별 검증(Verifier 판정) 표면의 물리 실현 정본**(06 §4 바인딩) — 본 문서 §5(검증 통합 행)는 참조만 한다.
- framework/adapters/claude/runtime-binding.md (v0.3 Baseline) — 자매 Adapter Binding. 세션/턴 수명주기 컨테이너·Register/Resolve 수행 방식·형태 A/B 서술 관례의 선행 표본.
- framework/loop/module-manifest.md — `contract`=`LoopInterface` 확정 지점(이 Manifest의 `requires` 값이 참조하는 기존 contract id의 출처). framework/loop/loop-protocol.md §3 — 단일 사이클 오케스트레이션(Dispatch가 소비할 각 Task의 사이클 계약). § 포인터로만 참조.
- docs/delegation-protocol.md §3 — 이 프로젝트의 물리 채널 바인딩 관행(위임 = 서브에이전트 디스패치 §3.1, 보고 회수 = 최종 응답 §3.2, **병렬 Wave 물리 실현 = 서브에이전트 동시 위임·수합·중재 §3.3**, 반환·에스컬레이션 = 최종 응답 §3.4). 물리 채널 서술의 관행 근거.
- .claude/agents/ 4종(advisor.md·planner.md·verifier.md·worker.md) — 역할 실행(Advisor·Planner·Worker·Verifier)의 물리 실체(실측). 본 문서는 참조만 하고 수정하지 않는다.
- .claude/CLAUDE.md — Advisor를 프로젝트 진입점(주 세션)에 바인딩하는 지점(07 §4.1 행 6 중재 진입점 대응 + 07 §4.2 SP-4). 실측 대상. .claude/AGENT.md — 상위 규약.
- framework/core/structure.md §2·§5·§8 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·§8 트리(백엔드 격리 데이터 소관). 본 문서 경계의 근거.
- specs/00-glossary.md — 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- Active Lesson L-07 (상태 서술은 실측 후 기록 — A5 재작업 사례에서 도출). ROADMAP.md v0.7 (Workflow & Parallel Orchestration) — 산출물의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 07 §3.3 INV-9), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·memory-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형). 단 이 문서는 Core Contract(07 §3)와 그 인스턴스 문서(framework/workflow/ 5문서)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.7 Draft | 최초 작성. `framework/adapters/claude/` 경계의 다섯 번째 산출물(선행: runtime-binding.md·memory-binding.md·verifier-binding.md·loop-binding.md). 07 §4.1 바인딩 표 **7행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정)/데이터 미생성(시연 소산 예정) 정직 구분(§2). Work Graph·Merge Result·공통 Failure Report 직렬화 물리 정본 확정(§3, DP-W4 — 직렬화 = **문서 형태**, `workflow-data/` 등 새 데이터 백엔드 디렉터리 **신설 없음**; 07 §4.1 행 1 정본 문면이 문서 형태를 지정하므로 그 인스턴스로 해소; 시연 소산의 docs/ 물리 위치·문서 구조를 구조 제안·근거로 확정, 미래 산출물 실재 불주장 — L-07). Workflow Provider `entrypoint`(Decompose=Planner 초안+Advisor 채택 / Dispatch=서브에이전트 동시 위임 / Merge=Advisor 수합·중재) 물리 해소(형태 A/형태 B 구분) + `requires`=`LoopInterface` 물리 해소는 loop-binding.md §4.1 실현을 **참조만**(재정의 0)(§4). 역할 실행(Advisor·Planner·Worker·Verifier)·병렬 디스패치·결과 회수·수합·중재 물리 채널(서브에이전트 동시 위임·최종 응답·주 세션 Advisor 제시, delegation-protocol.md §3) + 검증 통합(verifier-binding.md 참조) + Memory 접근(memory-binding.md 백엔드 경유 참조, 재정의 0)(§5). 07 §4.2 이식 교체 지점 SP-1~4 대응 표("교체되는 것/유지되는 것" — 유지 열이 07 §4.2 유지 목록(Work Graph 필드·Task 필수 필드·R1~R4·Invariants) 전건 커버, §6). 상태 서술 실측 대조 표(§7 — 실재 서술 전건 파일 시스템 직접 실측 후 기입, L-07; docs/v0.7 시연 소산 미생성·후속 Task 생성 예정). 07 §3·framework/workflow/ 5문서 계약 재정의·창설 0, 새 바인딩 계약 0, Glossary 밖 새 용어 0. 동시/후속 작성 시연 절차서·시연 실물 내용 불인용(07 R2), 미래 산출물(시연 소산) 실재 불주장(L-07). 이 1파일만 생성 — framework/workflow/ 5문서·자매 바인딩·loop-data/·memory-data/·docs/ 무수정. | Worker (Advisor 위임, Task WF6) |
| 2026-07-06 | v0.7 Baseline | v0.7 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.8 Draft (개정 — 시연 소산 실재 반영) | v0.8 Task EX-R2 — Advisor 승인 하 격리 개정 (v0.7 CP2 §3.7-4 관찰 해소, 사용자 승인 2026-07-06 편입 범위). v0.7 시연 소산의 "미생성·생성 예정" 라이브 서술 전 지점을 파일 시스템 직접 실측 후 실재 상태로 정합화(L-06·L-07) — docs/v0.7-demo.md(§4.3 Work Graph 인스턴스·§6.2 Merge Result)·v0.7-demo-procedure.md·v0.7-demo-fixtures/ 9파일·loop-data 3파일 실재 반영, §8 OQ-WB-1 해소됨 표기(§3.2 구조 제안이 시연 실물로 채택·실현 — demo.md §0.1). 계약·바인딩 확정 내용(DP-W4·SP 대응·물리 채널) 무변경, 시점 명시 스냅샷·기존 이력 행 문면 불변(L-10·V4 §4). | Worker (Advisor 위임, Task EX-R2) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-13 | (OQ 부분 해소 정합 — 버전 무상승) | §8 OQ-WB-2 부분 해소 표기 append — 형태 B Step Hosting 마일스톤이 §4.1 예약 로케이터("무인 병렬 오케스트레이션 실행 진입점")를 부분 실현: 중립 Step Host(`framework/loop/step-host/`)가 Work Graph(07 §3.2-A)를 데이터로 소비(ready_set=parallelSets 논리·dogfooding E2E 실증). 물리 동시 디스패치는 동시성 invoker 후속 과제로 이연(스케줄 논리 실현·물리 병렬 잔여). 본문 매핑·계약 무변경(참조 정합=버전 미상승 선례·BPD-17 append-only). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지)·docs/v0.7 시연 소산(demo·demo-procedure·demo-fixtures) 실재 서술을 @cd9247b 앵커로 전환(§0 커버리지 노트·§7 실측 표; DP-W4 직렬화 정본·workflow-data 미신설·loop-data/memory-data 백엔드는 계약으로 유지). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/07-workflow.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)와 framework/workflow/ 5문서(work-graph.md·module-manifest.md·decompose-rules.md·dispatch-protocol.md·merge-rules.md)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(세 연산·데이터 포맷·불변 규칙·필드·R1~R4·Manifest 필드)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. framework/workflow/ 5문서가 "직렬화 형식·물리 위치·물리 경로·물리 진입점 해소·역할 실행·병렬 디스패치·수합·중재의 물리 채널은 Adapter Binding 문서 소관"이라며 미룬 지점이 실재하는(확정되는) 유일한 자리다(work-graph.md §5, module-manifest.md §4, decompose-rules.md §6, dispatch-protocol.md §2.3, merge-rules.md §6, 07 §4.1).
- **격리 지점의 방향 반전(C-3 비적용).** Module 구현 디렉터리 문서(framework/workflow/ 5문서) 본문은 특정 AI·언어·툴체인·직렬화 형식·물리 경로 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 07 §3.3 INV-9). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형태 서술, 물리 경로 `framework/adapters/claude/…`·`.claude/…`·`docs/…`, 세션/턴, 서브에이전트 동시 위임 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(runtime-binding.md §0·memory-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형).
- **직렬화 물리 정본 선언 — 문서 형태(Advisor 결정 DP-W4).** Work Graph(07 §3.2-A)·Merge Result(07 §3.2-D)·공통 Failure Report(07 §3.2-E)의 물리 직렬화는 **문서 형태(계획·로드맵 문서 및 docs/ 시연 소산)로 확정한다**(Advisor 결정 DP-W4). **`framework/adapters/claude/workflow-data/` 등 새 데이터 백엔드 디렉터리를 신설하지 않는다.** 이는 loop-binding.md §3의 DP-L4(루프 상태 기록 → `framework/adapters/claude/loop-data/` 신설 백엔드)와 **사실 관계가 다르다** — 03 §4.1은 구체 경로·문법을 바인딩에 열어 뒀으나(loop-state-record.md §7·03 §4.1 SP-3), **07 §4.1 행 1 정본 문면("계획·로드맵 문서")은 이미 물리 형태를 문서로 지정**하므로 본 문서는 그 인스턴스로 해소한다. 시연 실물(Work Graph 인스턴스·Merge Result 기록)의 물리 위치·문서 구조 정본은 §3이 구조 제안+근거로 확정한다(loop-binding.md §3.1의 "구조 제안·근거" 관례 동형). **시연 소산은 시연 후(WF9) 이 정본 구조대로 생성되어 실재하며, §3·§7이 그 실측을 반영한다**(v0.8 개정 — 이전 "미래 산출물 실재 불주장" 서술을 시연 후 실측 실재로 갱신; WF6 작성 시점에는 미생성이었다, L-07).
- **창설 금지.** 이 문서는 07 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.7 산출물(작업 그래프 분해·병렬 디스패치·병합 충돌 처리·검증 통합)의 물리 실현 매핑으로 한정한다. 새 필드·새 연산·새 `reason`·새 불변 규칙을 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, runtime-binding.md §0, delegation-protocol.md §0). Workflow는 정식 실행 Module이 아니라 규약 문서(07·framework/workflow/ 5문서)와 관행(Advisor가 분해·디스패치·병합을 오케스트레이션, 서브에이전트 동시 위임·최종 응답으로 역할 실행)으로 실현된다(형태 A). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(자매 바인딩 4문서·framework/workflow/ 5문서·.claude/agents/ 4종·.claude/CLAUDE.md·ROADMAP.md — §7 실측)과, **실행 코드 도입 시 로딩될 지점**(형태 B — 무인 병렬 오케스트레이션 실행 진입점·로더), 그리고 **후속 시연 Task(WF9)가 이 정본 구조대로 생성한 시연 소산**(docs/ 시연 실물 — 시연 후 실재, §7 실측; WF6 draft 시점에는 미생성이었다 — 시점 스냅샷)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(Active Lesson L-07 — 상태 서술은 실측 후 기록, A5 재발 방지). §2 "실재 여부" 열과 §7 실측 대조 표의 전 행은 파일 시스템 직접 실측에 근거한다 — 미존재를 실재로 쓰지 않고, 실재는 실측 후에만 기입한다. docs/v0.7 시연 소산은 후속 시연 Task(WF9)가 §3 정본 구조대로 생성했다(시연 후 직접 재실측, §7 — docs/v0.7-demo.md §4.3·§6.2·v0.7-demo-procedure.md·v0.7-demo-fixtures/ 9파일·loop-data 3파일). WF6 작성 시점 실측에서는 미생성이었다(시점 스냅샷 — 그 시점 docs/ 아래 v0.7 시연 문서 부재; V4 §4 시점 명시 스냅샷). memory-binding.md §7이 M5 draft "데이터 미생성"을 시연 후 실재로 전수 갱신한 관례 동형이다.
- **docs/v0.7 시연 소산 아카이브(산출물 수명 정책 정합, 2026-07-17).** 위 docs/v0.7 시연 소산(`docs/v0.7-demo.md`·`docs/v0.7-demo-procedure.md`·`docs/v0.7-demo-fixtures/`)은 산출물 수명 정책(docs/artifact-lifecycle-policy.md §7)으로 작업 트리에서 제거되었다 — 본문·§2·§3·§7의 docs/v0.7 시연 소산 "실재/생성" 서술은 **cd9247b 시점 스냅샷** 기준이며, 앵커 `uahf/docs/v0.7-demo.md@cd9247b`로 참조한다(`git show cd9247b:uahf/docs/v0.7-demo.md`). DP-W4의 **직렬화 정본(문서 형태·`workflow-data/` 미신설)**·§3.2 구조 제안·`framework/workflow/` 5문서는 계약 서술로 유지되고, `loop-data/`·`memory-data/` 백엔드 경로도 계약으로 유지된다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약은 Glossary §3.2-J(J-07) 정본이며, `WorkflowInterface`·`workflow-provider`·`LoopInterface`는 module-manifest.md가 확정한 `contract`·`id`·`requires` 필드 **값**이지 Glossary 표제어의 신설이 아니다. `형태 A/B`는 structure.md 서술 라벨의 인용이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 07 §4.1(Workflow Claude Code Binding)을 이 환경 위에 **v0.7 시점의 구체 물리 실현**으로 매핑한다.

책임은 다섯 가지다.

- 07 §4.1 바인딩 표의 **7행 전부**를 물리 표면(작업 그래프 문서 직렬화·Task 정의·병렬 디스패치·위임 메시지 전달·결과 회수·수합/중재·검증 통합)으로 확정하고, Bootstrap 상태에서의 물리 실재(시연 소산 포함 — 시연 후 실측)/규약 실현(형태 A)/형태 B 예정을 "실재 여부" 열로 정직하게 구분한다(§2, done 1·4).
- Work Graph·Merge Result·공통 Failure Report의 **직렬화 물리 정본**을 확정한다(§3, done 2 — DP-W4) — 형태 = **문서**(계획·로드맵 문서 및 docs/ 시연 소산), `workflow-data/` 등 새 백엔드 디렉터리 **신설 없음**, 시연 소산의 물리 위치·문서 구조(구조 제안·근거 — 시연 후 시연 실물로 실현), 시연 소산 실재(시연 후 실측).
- Workflow Provider Module의 `entrypoint`(분해·디스패치·병합 연산 노출)·`requires`=`LoopInterface`의 **물리 해소 지점**(형태 A 규약 실현 / 형태 B 실행 코드)을 명시하고, `LoopInterface` 물리 해소는 loop-binding.md §4.1이 확정한 실현을 **참조만** 한다(§4, done 3, 재정의 0).
- 역할 실행(Advisor·Planner·Worker·Verifier)·병렬 디스패치·결과 회수·수합·중재의 **물리 채널**(서브에이전트 동시 위임·최종 응답·주 세션 Advisor 제시)과 검증 통합·Memory 접근의 **물리 실현**(verifier-binding.md·memory-binding.md 참조)을 확정한다(§5, done 1 상세).
- 07 §4.2 이식 교체 지점 SP-1~4 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§6, done 4). 그리고 상태 서술을 실측과 대조한다(§7, done 5).

이 문서는 07 §3·framework/workflow/ 5문서의 어떤 계약 요소도 재정의·확장하지 않는다(§0, done 5). 형태 A → 형태 B 전환 시에도 Core Contract(07 §3) 변경은 0이며(structure.md §7 C-1), 이 문서(§6의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 07 §4.1 바인딩 표 7행 물리 실현 (done 1·4)

07 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. 아래 표의 "07 §4.1 바인딩(정본 인용)" 열은 정본 표현을 **원문 그대로** 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·형태·채널·절차를, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재(시연 소산 포함 — 시연 후 실측)/규약 실현(형태 A)/형태 B 예정을 정직하게 구분한다(§7 실측 대조). "실재" 서술은 전건 파일 시스템 실측 후 기입했다(L-07 — v0.8 개정 시 재실측).

Adapter 경계 디렉터리 구조(본 문서 실측 — DP-W4: 새 데이터 백엔드 없음):

```
framework/adapters/claude/
├─ runtime-binding.md          # 실재 (v0.3 Baseline)
├─ memory-binding.md           # 실재 (v0.4 Baseline)
├─ verifier-binding.md         # 실재 (v0.5 Baseline)
├─ loop-binding.md             # 실재 (v0.6 Baseline · v0.7 Draft 개정)
├─ workflow-binding.md         # 실재 (본 문서)
├─ memory-data/                # 실재 — Memory 백엔드 (memory-binding.md 소관)
└─ loop-data/                  # 실재 — 루프 상태 기록 백엔드 (loop-binding.md 소관)
   # ★ workflow-data/ 없음 — Workflow 직렬화는 문서 형태(DP-W4), 새 백엔드 디렉터리 신설 없음. §3.
```

| # | §3 계약 요소 (정본 §) | 07 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Work Graph(07 §3.2-A) 직렬화 | Work Graph(§3.2-A) 직렬화 · 계획·로드맵 문서. 예: ROADMAP.md의 Wave 분해와 Parallel Track Map(§4). | Work Graph 직렬화 = **문서 형태**(DP-W4) — 기존 계획·로드맵 문서(ROADMAP.md의 Wave 분해·Parallel Track Map)가 실사용 인스턴스이며, 시연 소산의 Work Graph 인스턴스는 docs/ 시연 문서 내 구조화 섹션으로 직렬화한다. 새 데이터 백엔드 디렉터리를 두지 않는다. 포맷 정본은 work-graph.md §2, 물리 위치·문서 구조 정본은 §3. | ROADMAP.md(Wave 분해·Parallel Track Map) 실재. 시연 소산(Work Graph 인스턴스, docs/v0.7-demo.md §4.3) = **실재**(시연 후 실측 — 후속 시연 Task WF9 생성). |
| 2 | Task(07 §3.2-B) 정의 | Task(§3.2-B) 정의 · 로드맵 Wave 내 개별 작업 항목(예: 각 spec 작성). `done`·`interfaceContract`는 TEMPLATE DoD와 각 spec §2 Position 선언에 대응. | Task 정의 = 로드맵 Wave 내 개별 작업 항목 + 그 Task의 `delegation`(02 §3.2-B 위임 메시지). `done`은 TEMPLATE DoD, `interfaceContract`는 각 spec §2 Position 선언에 대응한다(07 §4.1 정본). 포맷 정본은 work-graph.md §3(재정의 0). | ROADMAP.md Wave 항목·TEMPLATE.md DoD·spec §2 Position 실재. 위임 메시지 채널 규약 실현(형태 A). 시연 Task 인스턴스(docs/v0.7-demo.md §4.3 Task 7필드) = **실재**(시연 후 실측). |
| 3 | 병렬 디스패치(07 §3.2-C) | 병렬 디스패치(§3.2-C) · Advisor가 서브에이전트 동시 위임으로 한 병렬 집합의 Task들을 여러 Worker에게 동시에 전달한다. 위임 메시지 전달 메커니즘은 02 §4.1을 재사용한다. | 주 세션 Advisor가 **서브에이전트 동시 위임**으로 한 병렬 집합의 Task들을 여러 Worker에게 동시에 전달한다(delegation-protocol.md §3.3 병렬 Wave 물리 실현). 위임 메시지는 02 §3.2-B, 전달 메커니즘은 02 §4.1 재사용(채널 새로 정의 0). 물리 채널 상세는 §5.1. | 서브에이전트 동시 위임 채널 규약 실현(형태 A) — 본 Task(WF6)를 포함한 v0.7 병렬 집합 디스패치·spec 병렬 작성 Wave(07 §8 예1)가 실증. 무인 자동 병렬 오케스트레이션(형태 B)은 미도입. |
| 4 | 위임 메시지 전달 | 위임 메시지 전달 · 02 §4.1 위임 메커니즘(서브에이전트 위임) 재사용. Workflow는 채널을 새로 정의하지 않는다. | 위임 메시지 전달 = **서브에이전트 위임**(02 §4.1, delegation-protocol.md §3.1). Workflow는 이 채널을 **재사용만** 하고 새로 정의하지 않는다 — 채널·필드 정본은 02 소유(07 INV-3). 물리 채널 상세는 §5.2. | 서브에이전트 위임 채널 규약 실현(형태 A). `.claude/agents/` 4종 정의 파일 실재(§7 실측). |
| 5 | 결과 회수(07 §3.2-D collected) | 결과 회수(§3.2-D collected) · 각 서브에이전트의 최종 응답 = 완료 보고(02 §3.2-C). 02 §4.1 보고 회수 재사용. | 각 서브에이전트의 **최종 응답 = 완료 보고**(02 §3.2-C)로 회수된다(delegation-protocol.md §3.2). 회수된 결과는 Merge Result `collected`(07 §3.2-D — 개별 검증 통과 결과만, INV-5)를 채운다. 02 §4.1 보고 회수 재사용. 물리 채널 상세는 §5.2. | 최종 응답 회수 채널 규약 실현(형태 A). Merge Result 기록(시연 소산, 문서 형태 §3 — docs/v0.7-demo.md §6.2) = **실재**(시연 후 실측). |
| 6 | 상호 참조 정합성·충돌 중재 | 상호 참조 정합성·충돌 중재 · Advisor(`.claude/CLAUDE.md` 진입점)가 병렬 결과를 수합·대조하고 충돌을 중재한다. | **주 세션 Advisor**(`.claude/CLAUDE.md` 진입점, advisor.md)가 병렬 결과를 수합·대조하고 상호 참조 정합성(`crossRefStatus`)을 판정하며 충돌을 중재한다(07 INV-6 중재자=Advisor, merge-rules.md §4·delegation-protocol.md §3.3). 중재 진입점 = 주 세션 Advisor 바인딩. 물리 채널 상세는 §5.3. | `.claude/CLAUDE.md` Advisor 진입점 바인딩 실재(§7 실측). 수합·대조·중재 규약 실현(형태 A). 무인 자동 중재(형태 B)는 미도입. |
| 7 | 검증 통합 | 검증 통합 · 각 Task 결과는 개별 검증(Verifier 판정)을 거친 뒤 병합된다. 판정 표면은 06-verifier §4 소관. | 각 Task 결과는 개별 검증(Verifier CP2 독립 판정)을 거친 뒤에만 병합된다(07 INV-5, merge-rules.md §4.1·§5). 판정 표면(무엇이 통과인가)의 물리 실현은 **verifier-binding.md**(06 §4 바인딩)가 소유하며, 본 문서는 그 통과 결과를 병합 선행 조건으로 소비할 뿐 판정을 재정의하지 않는다(재정의 0). 물리 실현 상세는 §5.4. | Verifier(`.claude/agents/verifier.md`)·verifier-binding.md 실재(§7 실측). 판정 통합 규약 실현(형태 A). |

주:

- 위 7행은 07 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 07 §4.1 정본 표현을 이 환경의 구체 경로·형태·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **물리 실재 / 형태 A / 형태 B 구분(정직).** 행 1의 ROADMAP.md 인스턴스·행 2의 TEMPLATE/spec §2·행 4의 `.claude/agents/`·행 6의 `.claude/CLAUDE.md`·행 7의 verifier-binding.md는 물리 실재다. 행 3(병렬 디스패치)·행 4(위임 전달)·행 5(결과 회수)·행 6(수합·중재)·행 7(검증 통합)의 오케스트레이션은 Bootstrap에서 **규약 실현(형태 A)**이다 — 서브에이전트 동시 위임·최종 응답·주 세션 Advisor 제시로 수행되며, 무인 자동 병렬 오케스트레이션 채널은 형태 B다. **행 1·행 5의 시연 소산(Work Graph 인스턴스·Merge Result 기록)은 문서 형태로 직렬화되며(DP-W4, §3), 후속 시연 Task(WF9)가 §3 정본 구조대로 생성하여 실재한다**(시연 후 실측 — docs/v0.7-demo.md §4.3·§6.2, §7; WF6 draft 시점에는 미생성이었다 — 시점 스냅샷, L-07).
- **역할 실행 = Agent Module(서브에이전트 채널).** Advisor·Planner·Worker·Verifier 역할은 서브에이전트로 디스패치되는 Agent Module이므로(verifier-binding.md §3.1·loop-binding.md §5.1 동형), 위임·보고·재위임 전달이 **서브에이전트 위임/최종 응답 채널**로 실현된다(§5.1·§5.2). 병렬 디스패치는 이 채널의 **동시** 사용이다(delegation-protocol.md §3.3).
- **직렬화 = 문서 형태 · 새 백엔드 없음(DP-W4, L-07 실측).** loop-data/·memory-data/는 실재하나 `workflow-data/`는 **없다**(본 작성 시 `ls` 실측). 이는 오류가 아니라 DP-W4의 귀결이다 — 07 §4.1 행 1 정본 문면이 문서 형태를 지정하므로 Workflow 직렬화는 새 데이터 백엔드가 아니라 문서(계획·로드맵 문서·docs/ 시연 소산)로 실현된다(§3). loop-binding.md §3(DP-L4, 새 백엔드 신설)과의 사실 관계 차이는 §3.1에 서술한다.

---

## §3. Work Graph·Merge Result·공통 Failure Report 직렬화 물리 정본 확정 (done 2 — DP-W4)

work-graph.md가 "세 포맷(Work Graph·Task·공통 Failure Report)의 직렬화 형식·물리 위치·물리 경로는 이 문서가 일절 확정하지 않는다 … Adapter Binding 문서 소관"(work-graph.md §5)으로 미룬 지점과, merge-rules.md가 "병합 결과 수합·중재 진입점의 물리 채널·직렬화·물리 위치는 Adapter Binding 문서 소관"(merge-rules.md §6)으로 미룬 Merge Result 직렬화를 확정한다. **이 문서는 Adapter 경계이므로 구체 직렬화 형태·물리 경로 토큰의 사용이 허용된다(§0 격리 지점).** 계약 요소(필드·의미·필수 표기·`reason` 열거·병렬 집합 도출 문면)의 정본은 work-graph.md §2~§4·merge-rules.md §3·07 §3.2이며, 본 절은 그 물리 실현만 확정한다(재정의 0).

### §3.1 직렬화 물리 형태 정본 — 문서 형태 (DP-W4 + 사실 관계 구분)

- **물리 형태 정본(Advisor 결정 DP-W4).** Work Graph(07 §3.2-A)·Merge Result(07 §3.2-D)·공통 Failure Report(07 §3.2-E)의 물리 직렬화는 **문서 형태**로 확정한다 — 기존 계획·로드맵 문서(ROADMAP.md 등)와 docs/ 시연 소산이 그 매체다. **`framework/adapters/claude/workflow-data/` 등 새 데이터 백엔드 디렉터리를 신설하지 않는다.**
- **loop-binding.md DP-L4와의 사실 관계 차이(핵심).** loop-binding.md §3은 루프 상태 기록을 `framework/adapters/claude/loop-data/` **신설 백엔드**로 격리했다(DP-L4). 그 근거는 03 §4.1이 구체 경로·문법을 바인딩에 **열어 뒀기** 때문이다(loop-state-record.md §7이 직렬화 형식·저장 위치·물리 경로를 "전부 Adapter Binding 문서 소관"으로 미룸, 03 §4.1 SP-3). **그러나 07 §4.1 행 1 정본 문면은 다르다** — "Work Graph(§3.2-A) 직렬화 · **계획·로드맵 문서**. 예: ROADMAP.md의 Wave 분해와 Parallel Track Map"이라며 **물리 형태를 문서로 이미 지정**한다. 따라서 본 문서는 새 데이터 백엔드를 창설하지 않고, 정본 문면이 지정한 문서 형태의 인스턴스로 해소한다(DP-W4). 07 §4.2 SP-1도 "Work Graph 직렬화 — **계획·로드맵 문서 포맷** → 대상 환경의 작업 그래프 서술자"로 문서 형태를 교체 지점의 이 환경 바인딩으로 명시한다(§6).
- **정합 근거.**
  - **(a) 정본 문면 준수.** 07 §4.1 행 1이 "계획·로드맵 문서", 07 §4.2 SP-1이 "계획·로드맵 문서 포맷"을 이 환경 바인딩으로 지정한 이상, 새 백엔드 디렉터리 신설은 정본 문면을 초과하는 창설이다(§0 창설 금지). 문서 형태는 정본 문면의 직접 인스턴스다.
  - **(b) 실사용 인스턴스 존재.** Work Graph 직렬화의 실사용 인스턴스는 이미 실재한다 — ROADMAP.md의 Wave 분해(`tasks`·`dependencies` 대응)와 Parallel Track Map(`parallelSets` 대응)이 그것이다(07 §4.1 행 1 예시, 07 §8 예1 실증). 이 프로젝트의 spec 병렬 작성 Wave가 그 실사용 형태다.
  - **(c) 격리 불필요 vs. 격리 필요의 사실 차이.** 루프 상태 기록은 사이클마다 기계 생성되는 append-only 로그라 소비자 경로에서 격리할 백엔드가 필요했다(loop-binding.md §3.1 근거). Work Graph·Merge Result는 Advisor·Worker가 계획·수합·중재 과정에서 서술하는 **문서 산출물**이며, 그 매체가 곧 계획·로드맵 문서·시연 소산이다 — 별도 격리 백엔드가 아니라 문서가 정본 매체다.
- **문서 형태 = Adapter 선택.** 문서 형태(계획·로드맵 문서·시연 소산 내 구조화 서술) 선택은 07 §4.2 SP-1의 교체 지점이며, 이식 시 대상 환경의 작업 그래프 서술자로 교체된다(§6). Work Graph·Task·공통 Failure Report의 필드·필수 표기·`reason` 9종 열거(work-graph.md §2~§4)와 Merge Result 4필드(merge-rules.md §3)는 이식 시 유지되고 문서 직렬화만 교체된다(07 §4.2 유지 목록, §6).

### §3.2 시연 소산의 물리 위치·문서 구조 (구조 제안·근거 — 시연 후 시연 실물로 채택·실현, OQ-WB-1 해소)

DP-W4가 "시연 실물(Work Graph 인스턴스·Merge Result 기록)의 정확한 물리 위치·문서 구조는 본 문서가 정본으로 확정한다 — 구조 제안+근거로 서술"로 위임한 지점이다. loop-binding.md §3.1의 "구조 제안·근거" 관례와 동형으로 서술한다. **이 구조 제안은 시연 후(WF9) 시연 실물로 채택·실현되었다**(§7 실측 — docs/v0.7-demo.md §0.1이 "workflow-binding §3.2 정본, OQ-WB-1 해소"를 명시; WF6 작성 시점에는 미생성이었다 — 시점 스냅샷, L-07).

- **물리 위치(구조 제안).** v0.7 Workflow 시연 소산은 **`docs/` 아래 v0.7 시연 문서**(시연 절차서·수행 기록 성격의 구조화 문서)에 배치한다 — v0.7 시연 소산의 docs/ 배치 원칙(시연 절차서·수행 기록·시연 픽스처 경계 내 구조화 문서) 준수. 이는 loop 시연 소산이 `docs/` 아래 v0.6 시연 문서(loop-binding.md §9 이력이 참조한 시연 Task 산출)로 배치된 관례와 동형이다. **본 문서(WF6)가 확정하는 것은 그 소산이 따를 물리 위치·구조 원칙**이며, WF6 작성 시점에는 동시/후속 작성될 시연 절차서·시연 실물의 문서명·내용을 확정·인용하지 않았다(07 R2 준수 — 당시 시연 소산 미생성). 그 원칙대로 생성된 시연 실물(docs/v0.7-demo.md)은 시연 후 실재하며, demo.md §0.1이 이 §3.2를 정본으로 인용한다(§7 실측).
- **문서 구조(구조 제안).**
  - **Work Graph 인스턴스** — 시연 문서 내 하나의 구조화 섹션으로 직렬화한다: `goal`·`tasks`(각 Task의 `id`·`task`·`done`·`interfaceContract`·`ownedBoundary`·`dependsOn`·`delegation`)·`dependencies`·`parallelSets`·`completion`의 5필드(work-graph.md §2)와 Task 7필드(work-graph.md §3)를 서술한다. 병렬 집합 도출(선행 의존 없는/공통 선행 완료된 Task들이 한 병렬 집합)을 명시한다(work-graph.md §2 정본 문면).
  - **Merge Result 기록** — 시연 수행 기록 내 구조화 서술로 직렬화한다: `collected`(개별 검증 통과 결과만 — INV-5)·`crossRefStatus`(`Consistent`/`Mismatch`)·`conflicts`·`arbitration`(중재자 = Advisor)의 4필드(merge-rules.md §3)와 충돌 처리 순서(수합 → 상호 참조 정합성 검증 → 충돌 검출 → (충돌 시) Advisor 중재 → 병합 성립, merge-rules.md §4)를 서술한다.
  - **공통 Failure Report** — 연산 실패 발생 시 `operation`(Decompose/Dispatch/Merge)·`target`·`reason`(9종, work-graph.md §4)·`location` 4필드를 구조화 서술로 직렬화한다. Dispatch 실패(`IncompleteDelegation`·`UnmetDependency`)는 수임 Agent의 반환·질의(02 INV-6)와 함께 최종 응답으로도 회수된다(§5.2, delegation-protocol.md §3.4).
- **구조 제안 근거.**
  - **(a) 재구성 단위 = 워크플로 전체.** 07 §7 완료 기준은 "3개 이상의 Task가 하나의 병렬 집합으로 디스패치되고, 각 Task가 개별 검증을 통과한 뒤 병합이 성립하는 Workflow를 시연"하는 것이다. 한 시연 문서 안에 Work Graph 인스턴스 + 병렬 디스패치 기록 + 각 Task 검증 결과 + Merge Result를 두면 그 시연을 문서 1건 판독으로 자기완결 재구성할 수 있다.
  - **(b) 정본 문면과의 정합.** Work Graph를 계획·로드맵 문서 형태로 두는 것은 07 §4.1 행 1·SP-1 정본 문면의 직접 실현이며(§3.1), 시연 소산도 같은 문서 형태를 따른다 — 별도 백엔드가 아니라 구조화 문서 섹션이다.
  - **(c) 소유 경계 교집합 0 시연.** 07 §7 "간섭 금지 시연"(한 병렬 집합 내 모든 Task의 `ownedBoundary` 교집합이 0, INV-2)은 Work Graph 인스턴스의 각 Task `ownedBoundary`를 문서에 나열해 쌍별 교집합 0을 대조로 보이면 성립한다(Verifier 검증 방법 07 §7).
- **실재 상태(L-07).** 위 물리 위치·문서 구조는 **정본(제안·근거)**이며, 그에 따른 **시연 소산은 시연 후(WF9) 실재한다**(§7 실측 — docs/v0.7-demo.md §4.3 Work Graph 인스턴스·§6.2 Merge Result·v0.7-demo-procedure.md·v0.7-demo-fixtures/ 9파일·loop-data 3파일; WF6 작성 시점에는 미생성이었다 — 시점 스냅샷, V4 §4). 생성 주체는 **후속 시연 Task(WF9)**이며, 본 문서(WF6)는 구조·위치의 정본만 소유한다 — 시연 실물을 생성·수정하지 않았다(생성 주체 구분, L-07; loop-binding.md §3이 loop-data/ 데이터의 생성 주체를 시연 Task로 구분한 관례 동형). **이 구조 제안은 시연 실물로 채택·실현되었다 — OQ-WB-1 해소**(demo.md §0.1이 "workflow-binding §3.2 정본, OQ-WB-1 해소" 명시, §8).

---

## §4. Workflow Provider `entrypoint`·`requires` 물리 해소 (done 3)

module-manifest.md(WF2 확정본)가 "`entrypoint`·`requires`의 물리 해소는 Adapter Binding 문서 소관(§4)"으로 미룬 지점을 확정한다. loop-binding.md §4.1의 `entrypoint`·`requires` 물리 해소 표 관례(추상 참조 → 물리 실현, 형태 A/B 구분)와 동형으로 서술한다.

### §4.1 `entrypoint` 물리 해소 (분해·디스패치·병합 연산 노출)

module-manifest.md §2·§4 `entrypoint` = "추상 참조 — 분해(Decompose)·디스패치(Dispatch)·병합(Merge) 연산(07 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관". 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Decompose(07 §3.1-A) 노출 — 큰 작업 1건을 Work Graph로 분해 | **형태 A(Bootstrap):** 주 세션 오케스트레이션으로 실현된다 — **Planner 초안(`.claude/agents/planner.md` — Wave 설계·분해·Worker 브리프 초안) + Advisor 채택**. 분해 검사 규칙(C1~C4, decompose-rules.md §3)은 Planner 초안이 만족하고 Advisor가 채택 시 대조한다. 산출 Work Graph는 문서 형태로 직렬화된다(§3). 별도 실행 진입점 파일은 없다. | 규약 실현(형태 A) |
| Dispatch(07 §3.1-B) 노출 — 병렬 집합을 여러 Agent에게 디스패치 | **형태 A(Bootstrap):** 주 세션 Advisor가 **서브에이전트 동시 위임**으로 한 병렬 집합의 Task들을 여러 Worker에게 동시 전달한다(delegation-protocol.md §3.3, §5.1). 핸들(Task id → 수임 Agent 매핑, dispatch-protocol.md §2.3)은 그 동시 위임의 논리 대응이다. | 규약 실현(형태 A) |
| Merge(07 §3.1-C) 노출 — 완료·검증된 결과 수합·정합성·충돌 처리 | **형태 A(Bootstrap):** 주 세션 **Advisor가 수합·대조·중재**한다 — 각 서브에이전트 최종 응답을 `collected`로 수합, 상호 참조 정합성 판정(`crossRefStatus`), 충돌 검출·중재(INV-6)(merge-rules.md §4, §5.3). Merge Result는 문서 형태로 직렬화된다(§3). | 규약 실현(형태 A) |
| 위 세 연산의 실행 코드 로케이터 | **형태 B:** 분해·디스패치·병합을 사람 없이 자동으로 트리거·반복·수합하는 실행 코드가 non-core 실행 경계(`framework/workflow/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지, loop-binding.md §4.1 형태 B 관례 동형). | 형태 B |

- **Register/Resolve 정합(loop-binding.md §4.1 동형).** Workflow Provider의 등록(Register)은 Manifest(framework/workflow/module-manifest.md) + 본 바인딩 배치로 규약 실현되며(형태 A), 해소(Resolve)는 소비자(07 dependents — 스택상 Presentation 진입점 등, 07 §2)가 `contract` `WorkflowInterface`로 오케스트레이션을 요청할 때 이 Provider로 해소되는 것이다. 역할 실행(Advisor·Planner·Worker·Verifier)은 module Resolve가 아니라 서브에이전트 디스패치이며(module-manifest.md §3 — 역할 디스패치는 requires에 넣지 않음), 그 물리 채널은 §5.1·§5.2다. 이 등록 경로는 이식 교체 지점 SP-2에 대응한다(§6).

### §4.2 `requires` = `LoopInterface` 물리 해소 (loop-binding.md §4.1 참조 — 재정의 0)

module-manifest.md §2·§3·§5(DP-W2) `requires` = `LoopInterface`(병합은 각 Task의 사이클 구동 완결을 요구 — 07 §3.1-C·INV-5). 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| `requires` = `LoopInterface` 물리 해소 — Workflow Provider가 Resolve될 때 함께 해소되어야 하는 단일 사이클 구동 계약(01 §3.1-A Resolve 완료 조건) | Workflow가 병렬 Task 각각에 대해 소비하는 사이클 구동 계약 `LoopInterface`의 물리 실현은 **loop-binding.md가 확정한 Loop Provider 실현**이다 — loop-binding.md §4.1이 `LoopInterface`를 구현하는 Loop Provider `entrypoint`의 물리 해소(형태 A: 사이클 구동 연산은 loop-protocol.md §3 오케스트레이션에 따라 세션/턴에서 구동, 각 단계 역할은 서브에이전트 위임 — CP1=Worker·CP2=Verifier·CP3=Advisor)를 소유한다. 각 Task의 Verify 게이트 통과(개별 검증 완결)가 곧 그 사이클 구동의 완결이며, 그 통과 결과가 병합 선행 조건(07 INV-5)이다. **본 문서는 이 물리 실현을 재정의하지 않고 참조만 한다**(재정의 0 — done 3·5). | loop-binding.md 소관(참조) |

- **경계.** `LoopInterface`는 framework/loop/module-manifest.md가 확정한 **기존 contract id**(신설 아님)이며, 그 Loop Provider 물리 실현은 loop-binding.md §4·§5가 소유한다. 본 문서는 Workflow가 그 계약의 **소비자**임(07 §3.1-C·INV-5·module-manifest.md §5 DP-W2)만 물리 채널 측면에서 확인하고, 사이클 구동의 물리 실현(단계 전이·재작업 루프·역할 실행 채널)을 재서술하지 않는다. 이 소비 관계의 물리 접점은 §5.4(검증 통합)다 — 각 Task의 사이클이 CP2(Verifier 독립 판정) Pass로 완결된 뒤에만 그 결과가 병합된다.
- **Memory 제외 재확인.** module-manifest.md §3·§5(DP-W2)가 Memory를 hard `requires`에서 제외한 근거(07 §5 Recall "필요할 때만"의 선택적 보강)는 불변이다. Workflow의 Memory 접근은 `requires` 게이트가 아니라 단일 Port 경유 소비이며(07 INV-7), 그 물리 실현은 memory-binding.md 백엔드 경유다(§5.5, 참조만).

---

## §5. 역할 실행·병렬 디스패치·수합·중재·검증·Memory 물리 채널 (done 1 상세)

07 §4.1 병렬 디스패치(행 3)·위임 메시지 전달(행 4)·결과 회수(행 5)·수합·중재(행 6)·검증 통합(행 7)의 물리 채널을 확정한다. decompose-rules.md §6·dispatch-protocol.md §2.3·merge-rules.md §6가 "분해 수행 주체 물리 채널·핸들 물리 실현·수합·중재 진입점 물리 채널은 Adapter Binding 문서 소관"으로 미룬 지점의 물리 실현이다.

### §5.1 병렬 디스패치 물리 채널 (07 §4.1 행 3, dispatch-protocol.md §2.3)

- **병렬 디스패치 = 서브에이전트 동시 위임.** 주 세션 Advisor가 한 병렬 집합(07 §3.2-A)의 Task들을 **서브에이전트 동시 위임**으로 여러 Worker에게 동시에 전달한다(delegation-protocol.md §3.3 병렬 Wave 물리 실현 — "Advisor가 서브에이전트 동시 위임으로 한 병렬 집합의 Task들을 여러 Worker에게 동시에 전달한다"). 각 Task는 서로 다른 Worker(서브에이전트)에게 전달된다(07 §3.2-C R1, dispatch-protocol.md §2.1 완료 조건 (iii)).
- **핸들의 물리 표현(dispatch-protocol.md §2.3 물리 실현).** Dispatch 출력의 "디스패치된 Task 핸들 집합 — Task id → 수임 Agent 매핑"(07 §3.1-B)은 그 동시 위임의 논리 대응이다. 물리 표현: 각 서브에이전트 위임이 그 Task id를 수임 Worker(서브에이전트 인스턴스)에 대응시키며, 회수 배선은 각 서브에이전트의 최종 응답(§5.2)이다. 핸들·회수 배선의 물리 실현은 이 Adapter 경계에 격리된다(dispatch-protocol.md §2.3).
- **경계 준수·불추측(R4·R2).** 각 Worker는 자신의 `ownedBoundary` 밖 파일·계약을 수정하지 않고(07 R4·INV-2), 동시 진행 중인 다른 Task의 미완성 산출물을 추측·인용하지 않으며 확정된 `interfaceContract`만 참조한다(07 R2·INV-4, dispatch-protocol.md §3). 실무상 위임 context 필드에는 확정(Frozen/실재) 문서만 넣는다(delegation-protocol.md §2.5·§3.1). **본 Task(WF6) 자신이 이 규칙의 실증**이다 — 확정된 framework/workflow/ 5문서·자매 바인딩만 참조하고 동시/후속 시연 산출물을 추측하지 않으며(07 R2), 이 1파일만 생성한다(07 R4).
- **실증 사례.** 이 프로젝트의 spec 병렬 작성 Wave(07 §8 예1, delegation-protocol.md §3.3)와 v0.7 Workflow Wave의 병렬 집합 디스패치가 서브에이전트 동시 위임의 실사용 형태다. 무인 자동 병렬 오케스트레이션은 형태 B(§4.1)다.

### §5.2 위임 메시지 전달·결과 회수 물리 채널 (07 §4.1 행 4·5)

- **위임 메시지 전달 = 서브에이전트 위임.** 전이를 유발하는 위임이 **서브에이전트 위임**(위임 메시지 02 §3.2-B, delegation-protocol.md §3.1)으로 흐른다. Workflow는 이 채널을 **재사용만** 하고 새로 정의하지 않는다(07 §4.1 행 4, INV-3 — 위임 메시지·역할 경계 포맷은 02 소유). 위임 필수 필드(from/to/task/input/output/done/context) 누락 시 수임 Agent는 착수하지 않고 반환·질의한다(02 INV-6, dispatch-protocol.md §2.2 `IncompleteDelegation`).
- **결과 회수 = 최종 응답.** 각 서브에이전트의 **최종 응답 = 완료 보고**(02 §3.2-C — artifacts·self_check·failures·open_questions·verify_basis)로 회수된다(07 §4.1 행 5, delegation-protocol.md §3.2). 회수된 결과 중 개별 검증(CP2)을 통과한 것만 Merge Result `collected`를 채운다(07 §3.2-D·INV-5, merge-rules.md §4.1). 실패·차단 시 실패 보고(02 §3.2-D)로 회수된다(delegation-protocol.md §3.4).
- **Advisor 재검증.** Advisor는 회수한 완료 보고를 그대로 신뢰하지 않고 독립 재검증(검증 게이트)을 거친다(delegation-protocol.md §3.2, `.claude/CLAUDE.md` "Worker 완료 보고를 그대로 신뢰하지 않는다"). 개별 검증 판정 자체는 Verifier CP2 소관이다(§5.4).

### §5.3 상호 참조 정합성·충돌 중재 물리 채널 (07 §4.1 행 6, merge-rules.md §6)

- **중재 진입점 = 주 세션 Advisor.** 병렬 결과의 수합·상호 참조 대조·충돌 중재는 **주 세션 Advisor**(`.claude/CLAUDE.md` 진입점, advisor.md 머리 "주 세션은 기본적으로 Advisor로 동작")에서 수행된다(07 §4.1 행 6 — "Advisor(`.claude/CLAUDE.md` 진입점)가 병렬 결과를 수합·대조하고 충돌을 중재한다", delegation-protocol.md §3.3). 물리 채널 = 각 서브에이전트 최종 응답으로 회수·수합된 뒤 주 세션에서 Advisor가 대조·중재.
- **수합·대조·중재 절차(merge-rules.md §4 물리 실현).** ⓐ **수합** — 각 결과에 완료 보고 동반 + 개별 검증 통과(CP2 Pass)를 확인해 `collected`를 채운다(§5.2·§5.4). ⓑ **상호 참조 정합성 검증** — Task 간 참조(한 Task가 참조하는 다른 Task의 확정된 `interfaceContract`·산출물)의 실제 일치를 대조해 `crossRefStatus`(`Consistent`/`Mismatch`)를 판정한다. ⓒ **충돌 검출** — 두 Task가 같은 계약을 다르게 실현했거나 소유 경계가 사후 충돌한 경우를 검출한다. ⓓ **충돌 시 Advisor 중재** — 해소 결정은 Advisor가 내린다(07 INV-6, merge-rules.md §4.4·§5). Merge Result는 문서 형태로 직렬화된다(§3).
- **검출·보고 = Workflow 소관 / 해소 결정 = Advisor 소관.** 상호 참조 불일치·충돌의 검출·보고까지가 Workflow 소관이고, 어떤 실현을 채택·기각할지의 재량 결정은 Advisor 중재 소관이다(merge-rules.md §5·§6, INV-6). 중재 진입점의 물리 채널이 곧 이 주 세션 Advisor 바인딩이다.
- **조율 에스컬레이션(R3).** 병렬 Task 진행 중 계약 불명확·경계 충돌 조짐·의존 계약 미확정을 발견하면 추측 없이 Advisor에게 에스컬레이션한다(07 R3·INV-6, dispatch-protocol.md §3.3). 차단 시 실패 보고(02 §3.2-D), 비차단 시 완료 보고 open_questions(02 §3.2-C)로 올린다(delegation-protocol.md §3.4·§2.6).

### §5.4 검증 통합 물리 실현 (07 §4.1 행 7 / INV-5) — verifier-binding.md 참조 (재정의 0)

- **개별 검증 = Verifier CP2 독립 판정.** 각 Task 결과는 개별 검증(Verifier 독립 판정, CP2)을 거친 뒤에만 병합된다(07 INV-5, merge-rules.md §4.1·§5). Verifier 역할은 `.claude/agents/verifier.md` 서브에이전트로 실행되며, 판정 표면(무엇이 통과인가·검증 리포트 최종 판정 Pass/Fail/Conditional)의 물리 실현은 **verifier-binding.md**(06 §4 바인딩)가 소유한다. **본 문서는 그 통과 결과(최종 판정 Pass)를 병합 선행 조건으로 소비할 뿐 판정을 재정의하지 않는다**(재정의 0 — 07 INV-8·Non-Goals, merge-rules.md §5.1).
- **소비 접점.** 병합 단계 1(수합, merge-rules.md §4.1)은 각 결과가 완료 보고 동반 + 개별 검증 통과(06 §3.2-C 최종 판정 Pass)를 확인하는 지점이다. 이것이 `requires`=`LoopInterface`(§4.2)의 물리 접점이기도 하다 — 각 Task의 사이클이 CP2 Pass로 완결된 뒤에만 그 결과가 `collected`에 든다. Merge는 검증을 재수행하지 않는다(merge-rules.md §4.1 경계).

### §5.5 Memory 접근 물리 실현 (07 §5 / INV-7) — memory-binding.md 백엔드 경유 (재정의 0)

- **접근 경로.** Workflow의 Memory 접근(Recall 회수·Record 기록, 07 §5·INV-7)은 **memory-binding.md가 확정한 백엔드**(`framework/adapters/claude/memory-data/`)를 단일 Port(memory-service.md §7 소비자 계약 — Workflow는 소비자) 경유로 실현한다. **본 문서는 그 물리 실현을 재정의하지 않고 참조만 한다**(재정의 0 — done 5).
  - **회수(Recall) 시점.** 착수(분해) 전, 유사 작업의 분해 패턴·과거 충돌·간섭 Lessons를 회수해 분해 품질을 높인다(07 §5 — "필요할 때만" 최소 범위, 전량 로드 금지). 물리 실현은 memory-binding.md §3.2(index-first)다.
  - **기록(Record) 시점.** 분해 결정·작업 이력·충돌 해소 결과 중 다음 사이클에 필요한 것을 기록한다(07 §5). 병렬 작업 간 간섭·상호 참조 불일치·병합 충돌은 Lesson 후보, 성공한 분해 패턴은 Best Practice 후보다(07 §5, AGENT.md). 물리 실현은 memory-binding.md §3.1이다.
- **단일 Port 경유(INV-7).** 회수·기록의 모든 접근은 Memory Service Interface(단일 Port) 경유다. 영속성 백엔드에 직접 접근하지 않는다(07 INV-7). 물리 배선은 memory-binding.md 소관이다.

---

## §6. 07 §4.2 이식 교체 지점 SP-1~4 대응 (done 4)

07 §4.2 이식 교체 지점 SP-1~4 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인하며, 07 §4.2 말미 "유지되는 것" 목록(§3.2-A Work Graph 필드·§3.2-B Task 필수 필드·§3.2-C R1~R4·§3.3 Invariants)을 전건 커버한다.

| # (07 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Work Graph 직렬화 — 계획·로드맵 문서 포맷 → 대상 환경의 작업 그래프 서술자 | §2 #1·#5, §3 | 문서 형태 직렬화(계획·로드맵 문서·docs/ 시연 소산), 새 백엔드 미신설(DP-W4), 시연 소산 문서 구조. | **§3.2-A Work Graph 필드**(`goal`·`tasks`·`dependencies`·`parallelSets`·`completion`)·병렬 집합 도출 문면(work-graph.md §2); **§3.2-E 공통 Failure Report 4필드·`reason` 9종**(work-graph.md §4); **§3.2-D Merge Result 4필드**(merge-rules.md §3). |
| SP-2 | 병렬 디스패치 메커니즘 — 서브에이전트 동시 위임 → 대상 환경의 병렬 오케스트레이션 API | §2 #3, §4.1(Dispatch 행), §5.1 | 서브에이전트 동시 위임, 핸들(Task id → 수임 Agent 매핑)의 물리 표현·회수 배선, Workflow Provider 형태 A 규약 실현·형태 B 실행 코드 로케이터. | **§3.1-B Dispatch 연산**(입력=병렬 집합+위임 메시지, 출력=핸들 집합, 완료 조건, 실패 `reason` 2종, dispatch-protocol.md §2); **§3.2-C R1~R4**(병렬 디스패치 프로토콜, dispatch-protocol.md §3); **INV-1~INV-4**. |
| SP-3 | 위임/보고 채널 — 서브에이전트 위임·최종 응답 → 대상 환경의 Agent 호출·결과 반환 채널 (02 §4.2 SP-4/SP-5 재사용, 이 spec은 참조만) | §2 #4·#5, §5.2 | 서브에이전트 위임(위임 메시지 전달)·최종 응답(완료/실패 보고 회수). 02 §4.2 SP-4/SP-5 재사용(참조만). | **§3.2-C R1(위임 메시지 전용)·INV-3(위임 계약 불침범)**; 위임 메시지·완료/실패 보고 필드는 02 §3.2-B/C/D 소유(재정의 0); **§3.1-C Merge 입력**(완료 보고 동반 결과). |
| SP-4 | 중재 진입점 — Advisor 바인딩(`.claude/CLAUDE.md`) → 대상 환경의 오케스트레이터 진입점 | §2 #6, §5.3 | 주 세션 Advisor 바인딩(`.claude/CLAUDE.md`) 수합·대조·중재 진입점, Merge Result 중재 결과 문서 직렬화. | **§3.1-C Merge 완료 조건**(개별 검증 통과·상호 참조 정합·충돌 해소)·**§3.2-D `crossRefStatus`·`conflicts`·`arbitration`**(merge-rules.md §3·§4); **INV-5(검증 후 병합)·INV-6(중재자=Advisor)**. |

- **"유지되는 것" 열의 이식 불변성 · 07 §4.2 유지 목록 전건 커버.** 위 유지 열은 07 §4.2 말미 "유지되는 것" 4항목을 전건 커버한다 — (i) **§3.2-A Work Graph 필드** = SP-1 유지 열, (ii) **§3.2-B Task 필수 필드** = SP-2·SP-3 유지 열(Task 필수 필드는 Dispatch 입력·위임 메시지 매핑으로 유지; work-graph.md §3 7필드), (iii) **§3.2-C R1~R4** = SP-2·SP-3 유지 열, (iv) **§3.3 Invariants(INV-1~INV-9)** = 각 SP 유지 열(INV-1~4 SP-2, INV-3 SP-3, INV-5~6 SP-4, INV-7~9 전반). 이들은 다른 AI·환경으로 이식해도 바뀌지 않는다(structure.md §7 C-1 — 형태 A→B 및 환경 전환에도 Core Contract 변경 0). framework/workflow/ 5문서가 그 계약의 인스턴스이며, 이식 시에도 이 인스턴스의 계약 요소는 불변이다.
- **Task 필수 필드 유지 명시(07 §4.2 유지 목록 (ii)).** SP-1(Work Graph 직렬화)이 교체되어도 Work Graph 안의 각 Task 7필드(`id`·`task`·`done`·`interfaceContract`·`ownedBoundary`·`dependsOn`·`delegation`, work-graph.md §3)는 유지된다 — 직렬화 매체(문서 → 대상 환경 서술자)만 교체되고 필드는 불변이다. `done`·`interfaceContract`의 존재 요건(07 INV-1)도 이식 불변이다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(07 §4.2 말미·loop-binding.md §6·verifier-binding.md §6 동형). 본 문서는 그 정식화를 선취하지 않고 v0.7 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 5 — A5/L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록 — A5 재작업 사례: 미존재 소스를 "실재"로 서술한 것을 파일 시스템 전수 대조로 검출한 데서 도출)에 따라, 본 문서의 "실재/존재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`) + 파일 크기·front-matter 직접 실측(v0.8 개정 시 재실측). workflow-data/ 부재는 여전히 직접 실측했고(DP-W4 정합), docs/v0.7 시연 소산은 시연 후 실재로 직접 재실측했다(L-06·L-07).**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — runtime/memory/verifier/loop-binding.md·memory-data/·loop-data/ 존재 확인. |
| `framework/adapters/claude/runtime-binding.md` | 실재 (v0.3 Baseline, 자매) | 실재 (32,973 bytes). |
| `framework/adapters/claude/memory-binding.md` | 실재 (v0.4 Baseline, 자매) | 실재 (51,144 bytes). |
| `framework/adapters/claude/verifier-binding.md` | 실재 (v0.5 Baseline, 자매) | 실재 (46,449 bytes). |
| `framework/adapters/claude/loop-binding.md` | 실재 (v0.6 Baseline · v0.7 Draft 개정, 자매 — `LoopInterface`·Memory 백엔드 참조원) | 실재 (63,750 bytes). |
| `framework/adapters/claude/workflow-binding.md` | 실재 (본 문서 — 본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음. |
| `framework/adapters/claude/workflow-data/` (DP-W4 — 신설 안 함) | **부재** (문서 형태 직렬화, 새 백엔드 미신설 — §3) | **부재** — `ls framework/adapters/claude/`에 loop-data/·memory-data/만 존재, workflow-data/ 없음(DP-W4 정합, 오류 아님). |
| `framework/workflow/` 5문서 (WF1~WF5 확정본 — 계약 인스턴스, § 포인터 대상) | 실재 (work-graph·module-manifest·decompose-rules·dispatch-protocol·merge-rules) | 실재 — 5파일: work-graph.md(22,406)·module-manifest.md(37,709)·decompose-rules.md(34,360)·dispatch-protocol.md(34,092)·merge-rules.md(37,329). 무수정. |
| `.claude/agents/` 4종 (역할 실행 물리 실체 — §5.1·§5.2) | 실재 (advisor/planner/verifier/worker.md) | 실재 — 4파일: advisor.md(7,152)·planner.md(9,232)·verifier.md(11,357)·worker.md(7,134). |
| `.claude/agents/worker.md` 실행 모델 (§4.1 Dispatch·§5.1) | 실재 `model: opus` (Worker 기본 실행 모델, 02 §4.1) | 실재 — front-matter `model: opus` 확인. |
| advisor/planner/verifier.md 실행 모델 (§4.1·§5) | 세션 상속 (미지정) | 실재 — 세 파일 front-matter `model` 라인 부재 확인(세션 상속). |
| `.claude/CLAUDE.md` Advisor 진입점·중재 바인딩 (§2 #6·§5.3) | 실재 (주 세션 Advisor 바인딩 + "Worker 완료 보고를 그대로 신뢰하지 않는다") | 실재 — `.claude/CLAUDE.md` "너는 … 메인 Advisor다"·"Worker 완료 보고를 그대로 신뢰하지 않는다" 확인(07 §4.1 행 6·SP-4 진입점). |
| `framework/adapters/claude/memory-data/` (§5.5 Memory 백엔드) | 실재 (memory-binding.md 확정 백엔드, 자매) | 실재 — `memory-data/store/`(mi-0001~0039)·`memory-data/index/` 존재 확인(memory-binding.md §7 실측 대상). |
| `framework/adapters/claude/loop-data/` (§4.2 `LoopInterface` 참조원 백엔드) | 실재 (loop-binding.md 확정 백엔드, 자매) | 표면 실재(`loop-data/`·`.gitkeep`) — 데모 인스턴스 3파일(v06-demo-a/b/c.jsonl)은 아카이브 `@cd9247b`(loop-binding.md §7 아카이브 참조). |
| ROADMAP.md (Work Graph 실사용 인스턴스 — §2 #1·§3.1) | 실재 (Wave 분해·Parallel Track Map — Work Graph 직렬화 실사용) | 실재 — ROADMAP.md 참조(07 §4.1 행 1 예시·07 §8 예1 실증). |
| docs/ v0.7 시연 소산 (Work Graph 인스턴스·Merge Result 기록, §3.2) | 문서 형태 소산(§3.2 구조대로 — 후속 시연 Task WF9 생성) — 데모 소산 아카이브 | 산출물 수명 정책으로 작업 트리에서 제거 — 앵커 `uahf/docs/v0.7-demo.md@cd9247b`·`uahf/docs/v0.7-demo-fixtures/@cd9247b`. cd9247b 시점 실측: docs/v0.7-demo.md(66,584 · §4.3 Work Graph 인스턴스·§6.2 Merge Result)·v0.7-demo-procedure.md(84,263)·v0.7-demo-fixtures/ 9파일. §3.2 구조 제안이 시연 실물로 채택·실현(OQ-WB-1 해소). 열람: `git show cd9247b:…`. (loop-data v07-demo-* 3파일은 loop-binding.md §7 아카이브 참조.) |
| 무인 병렬 오케스트레이션 실행 진입점·로더 (형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). `framework/workflow/`는 계약 문서 5건만 실재(실행 코드 0). |

- **핵심 구분.** 본 문서가 확정한 직렬화의 **물리 형태(문서)·시연 소산의 물리 위치·문서 구조는 정본(제안·근거)**(§3)이며, 그 **시연 실물(Work Graph 인스턴스·Merge Result 기록)은 시연 후(WF9) 실재한다**(docs/v0.7-demo.md §4.3·§6.2 — v0.8 개정 시 직접 재실측; WF6 작성 시점에는 미생성이었다 — 시점 스냅샷, V4 §4). WF6 작성 시점의 "미생성" 정직 구분은 memory-binding.md M5 draft("데이터 미생성, 시연 시 생성 예정")·loop-binding.md L8 draft 시점과 동형이었고, 그 소산이 시연 후 실재로 전이한 것 또한 두 자매 문서(memory-binding r2·loop-binding WF13)의 시연 후 실재 전수 갱신과 동형이다. 시연 소산의 생성 주체는 **후속 시연 Task(WF9)**이며, 본 문서(WF6)는 물리 형태·위치·구조의 정본만 소유한다 — 시연 실물을 생성·수정하지 않았다.
- **workflow-data/ 부재는 오류가 아니라 DP-W4의 귀결.** loop-data/·memory-data/와 달리 workflow-data/가 없는 것은 정합이다 — 07 §4.1 행 1 정본 문면이 문서 형태를 지정하므로 새 데이터 백엔드를 신설하지 않는다(§3.1). 이 사실 관계 차이(03 §4.1은 경로를 열어 둠 vs. 07 §4.1은 문서 형태를 지정)를 §3.1이 명시한다.
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로 쓰지 않았다(A5/L-07 재발 방지). docs/v0.7 시연 소산 실재·workflow-data/ 부재는 v0.8 개정 시 직접 재실측으로 확인했다(L-06·L-07).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 5).** 본 문서의 모든 매핑은 07 §3·§4·framework/workflow/ 5문서의 물리 실현이다. 어떤 연산·데이터 계약·불변 규칙·필드·R1~R4·Manifest 필드도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 정본 §(07 §3·work-graph.md·module-manifest.md·decompose-rules.md·dispatch-protocol.md·merge-rules.md)다. 새 바인딩 계약을 07 §4.1 표를 넘어 창설하지 않았고, 새 필드·새 연산·새 `reason`·새 불변 규칙을 추가하지 않았다.
- **계약 소유 명시.** 세 정의 포맷(Work Graph·Task·공통 Failure Report) = work-graph.md/07 §3.2-A/B/E; Dispatch 연산·R1~R4 = dispatch-protocol.md/07 §3.1-B·§3.2-C; Decompose 연산 = decompose-rules.md/07 §3.1-A; Merge 연산·Merge Result·충돌 처리 = merge-rules.md/07 §3.1-C·§3.2-D; Manifest 필드·`entrypoint`·`requires` = module-manifest.md/01 §3.2-A; `LoopInterface` 물리 실현 = loop-binding.md/03 §4; 개별 검증 판정 = verifier-binding.md/06 §4; Memory 백엔드 = memory-binding.md/04 §4. 본 문서는 이들의 **물리 실현**(직렬화 문서 형태·시연 소산 위치·구조·`entrypoint`·`requires` 물리 해소·병렬 디스패치/수합/중재 물리 채널)만 확정한다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형태 서술(문서 형태·구조화 섹션)·물리 경로(`framework/adapters/claude/…`·`.claude/…`·`docs/…`)·세션/턴·서브에이전트 동시 위임 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. framework/workflow/ 5문서(Module 구현 디렉터리 문서 본문)는 이 토큰을 "Adapter Binding 문서 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3 확장은 이 경계에 비적용 — 격리 보유, runtime-binding.md §5·memory-binding.md §8·verifier-binding.md §8·loop-binding.md §8 동형).
- **동시 작성 문서 경계(07 R2) 및 생성 주체 구분(L-07).** WF6 작성 시점에는 후속·동시 작성될 시연 절차서·시연 실물(docs/ 시연 소산)의 내용을 인용·추측하지 않았다(07 R2 준수 — loop-binding.md가 동시 작성 demo를 불인용한 선례 동형). 시연 절차·픽스처 상세는 서술하지 않았고, 그 시점 시연 소산(Work Graph 인스턴스·Merge Result 기록)의 실재를 주장하지 않으며 생성 주체를 후속 시연 Task로 구분했다(L-07). 시연 후(WF9) 그 시연 소산은 §3.2 정본 구조대로 생성되어 실재하며(§7 실측), 본 v0.8 개정이 그 라이브 상태 서술을 실재로 정합화했다 — 생성 주체(후속 시연 Task WF9)는 불변이다. 본 문서가 확정하는 것은 그 소산이 따를 **물리 형태·위치·구조 정본**이다. 참조한 확정 정본은 07(정본)·framework/workflow/ 5문서(WF1~WF5 확정본)·자매 Adapter Binding 4문서(runtime/memory/verifier/loop-binding)·framework/loop/module-manifest.md·loop-protocol.md·structure.md·.claude/agents/ 4종(역할 실행 실물)·.claude/CLAUDE.md·docs/delegation-protocol.md·specs/00-glossary.md뿐이다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 이 1개 파일(`framework/adapters/claude/workflow-binding.md`)만 생성하며, framework/workflow/ 5문서·.claude/agents/ 4종·기존 Baseline 산출물(runtime/memory/verifier/loop-binding.md·memory-data/·loop-data/)·specs/·docs/를 수정·생성하지 않는다. 시연 소산(docs/)도 생성하지 않는다(물리 형태·위치·구조 정본만 소유).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-WB-1 (시연 소산 docs/ 물리 위치·문서 구조 = Worker 제안, Advisor 채택 대상) — 해소됨 (v0.8 개정 — 시연 실물이 §3.2 정본 구조대로 생성·채택됨, demo.md §0.1 명시).** DP-W4는 직렬화 물리 **형태**(문서 형태·새 백엔드 미신설)를 확정했고, 그 위임에 따라 시연 소산의 **물리 위치**(docs/ 아래 v0.7 시연 문서)·**문서 구조**(Work Graph 인스턴스·Merge Result 기록의 구조화 섹션)를 §3.2가 구조 제안·근거로 확정했다. 이 위치·구조는 07 §4.1 행 1·SP-1(문서 형태)·07 §7(시연 완료 기준)을 물리적으로 만족한다. **후속 시연 Task(WF9)가 이 구조 제안을 그대로 채택·실현했다** — docs/v0.7-demo.md §4.3(Work Graph 인스턴스)·§6.2(Merge Result)가 그 구조화 섹션이며, demo.md §0.1이 "workflow-binding §3.2 정본, OQ-WB-1 해소"를 명시한다(§7 실측). 계약(07 §3.2) 변경이 아니었으므로 채택은 비차단으로 진행됐다(loop-binding.md OQ-LB-1이 loop-data/ 하위 구조를 Worker 제안·Advisor 채택 대상으로 남긴 것과 동형, memory-binding.md §8 OQ-M5-1 "해소됨" 표기 선례 동형).
- **OQ-WB-2 (형태 B 경계 분할 — 비차단) — 부분 해소 (형태 B Step Hosting 마일스톤, 2026-07-13).** 무인 병렬 오케스트레이션 실행 코드(형태 B)가 `framework/workflow/` Module 구현 디렉터리와 `framework/adapters/claude/` 사이 어디에 분할 배치되는지는 형태 B 설계 시 확정 대상이다(§4.1, structure.md §4 규칙 4 defer, loop-binding.md OQ-LB-2·verifier-binding.md OQ-VB-2 동형). Bootstrap(형태 A)에서는 규약 실현이므로 이 분할이 필요하지 않으며, 계약(07 §3) 변경이 아니므로 비차단이다. **부분 해소(형태 B Step Hosting 마일스톤)** — 무인 구동 실행 진입점은 `framework/loop/step-host/`(중립 Step Host)가 실현하며 Work Graph(07 §3.2-A)를 데이터로 소비한다(ready_set = parallelSets 도출 논리·순차는 그 특수형 — dogfooding E2E 실증 `step-data/runs/`). provider 의존 = `framework/adapters/claude/step-invoker/`·물리 매핑 = `step-hosting-binding.md`. **물리 동시 디스패치**(병렬 집합 원소의 동시 실행)는 동시성 invoker 후속 과제로 이연 — 스케줄 논리는 실현·물리 병렬은 잔여(그래서 부분 해소). 계약(07 §3) 변경 0.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 다섯 번째 산출물(선행: runtime-binding.md·memory-binding.md·verifier-binding.md·loop-binding.md). 07 §4.1(Workflow 바인딩 표 7행)의 **v0.7 물리 실현 매핑**. 정본 = 07 §3·§4 + framework/workflow/ 5문서(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 07 §4.1 표 **7행 전부**를 물리 표면으로 매핑("정본 인용" 열 원문 그대로 + "물리 실현" 열 + "실재 여부" 열, 물리 실재(시연 소산 포함 — 시연 후 실측)/형태 A/형태 B 정직 구분). ROADMAP.md·TEMPLATE·spec §2·`.claude/agents/`·`.claude/CLAUDE.md`·verifier-binding = 실재; 병렬 디스패치·위임·회수·수합·중재·검증 통합 = 규약 실현(형태 A); Work Graph 인스턴스·Merge Result 기록 = **실재**(시연 후 실측 — docs/v0.7-demo.md §4.3·§6.2).
- **§3 (DP-W4):** Work Graph·Merge Result·공통 Failure Report 직렬화 물리 정본 = **문서 형태**(계획·로드맵 문서·docs/ 시연 소산), **`workflow-data/` 등 새 백엔드 디렉터리 미신설** — 07 §4.1 행 1 정본 문면이 문서 형태를 지정(loop-binding.md DP-L4의 새 백엔드 신설과 사실 관계 상이). 시연 소산의 물리 위치(docs/ v0.7 시연 문서)·문서 구조(Work Graph 인스턴스·Merge Result 기록 구조화 섹션)를 구조 제안·근거로 확정 — 시연 후 시연 실물로 채택·실현(OQ-WB-1 해소, demo.md §0.1; 시연 소산 실재 — 시연 후 실측, L-07).
- **§4:** Workflow Provider `entrypoint` 물리 해소(형태 A: Decompose=Planner 초안+Advisor 채택 / Dispatch=서브에이전트 동시 위임 / Merge=Advisor 수합·중재; 형태 B: 무인 실행 코드 이연)·`requires`=`LoopInterface` 물리 해소(loop-binding.md §4.1 Loop Provider 실현 참조만 — 재정의 0).
- **§5:** 역할 실행(Advisor·Planner·Worker·Verifier = `.claude/agents/` 서브에이전트)·병렬 디스패치(서브에이전트 동시 위임, delegation-protocol.md §3.3)·위임/회수(위임·최종 응답, §3.1·§3.2)·수합·중재(주 세션 Advisor, `.claude/CLAUDE.md`, §3.3)·검증 통합(verifier-binding.md 참조)·Memory 접근(memory-binding.md 백엔드 경유 — 재정의 0).
- **§6:** 07 §4.2 이식 교체 지점 SP-1~4 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 07 §4.2 유지 목록(Work Graph 필드·Task 필수 필드·R1~R4·Invariants)을 **전건 커버**, 이식 불변(C-1) 재확인.
- **§7:** 실측 대조(2026-07-06 직접 실측) — 자매 바인딩 4문서·framework/workflow/ 5문서·.claude/agents/ 4종·.claude/CLAUDE.md·memory-data/·loop-data/·ROADMAP.md 실재; **workflow-data/ 부재**(DP-W4 정합)·**docs/v0.7 시연 소산 실재**(후속 시연 Task WF9 생성 — §3.2 구조대로, 시연 후 실측). 실측 불일치 0건(A5/L-07 재발 방지).
- 07·framework/workflow/ 5문서 계약 재정의 0, Glossary 용어 신설 0, 새 바인딩 계약 창설 0. 구체 AI·환경·형태 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 동시/후속 작성 형제 산출물 불인용(07 R2); 시연 소산은 후속 시연 Task(WF9)가 생성하여 실재(§3·§7, 생성 주체 구분 — L-07). 이 1파일만 생성·개정(v0.8 개정도 이 파일만 수정 — 시연 소산·loop-data·픽스처·자매 문서 무수정).
