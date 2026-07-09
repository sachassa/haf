# framework/adapters/claude/adapter-conformance — Claude Code Adapter 적합성(Conformance) 판정

작성일: 2026-07-06
상태: v1.2 Baseline (개정 — 자매 바인딩 계수 실측 정합 · UAF 정본 바인딩 3종 구분 표기 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-07). 직전 기준선: v0.9 Baseline (r2 — W2 정식화 실재 반영 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/11-adapters.md §3.1(Judge Conformance C1~C3)·§3.2-A(BP-1~BP-17 바인딩 지점 목록)·§3.2-B(Valid(Full)/Valid(Minimal)·최소 바인딩 부분집합 13개)·§3.2-C(Adapter 구조 규격)·§3.2-D(Conformance Report 6필드)·§4.1(Claude Code 바인딩 값)·§3.3(INV-1~INV-8). **Frozen(v0.1 기준선). 본 문서가 실현·판정하는 계약의 정본이며, 재정의·확장하지 않고 § 포인터로만 인용한다.**
- specs/01-runtime.md §3.2-E(디렉터리/구조 규격)·§4.1(Claude Code Binding 표·디렉터리 행). BP-1~5의 원천 계약·물리 정본. § 포인터로만 참조.
- specs/02-agent.md §3.2-A(역할 경계)·§4.1(Agent 정의 파일·공통 규약·실행 모델·위임/보고 채널)·§4.2(SP-1~SP-5). BP-7~11 실현의 정본 근거(agent-binding.md가 정식화한 원천 — r2). § 포인터로만 참조.
- framework/core/structure.md §2·§5·§8 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·금지 토큰 규칙·§8 트리. 본 문서 경계·물리 분리(BP-5)의 근거.
- framework/adapters/claude/ **자매 Adapter Binding 문서 11종**(UAHF spec 바인딩 — 전부 Baseline). 그중 8종: runtime-binding.md(v0.3)·memory-binding.md(v0.4)·verifier-binding.md(v0.5)·loop-binding.md(v0.7)·workflow-binding.md(v0.8)·hooks-binding.md(v0.9)·skills-binding.md(v0.8)·plugins-binding.md(v0.9); 나머지 3종(agent·harness·scaffold-binding)은 아래 W2 정식화 산출물 행. 각 BP의 물리 실현 소스. 본 문서는 그 실현을 커버리지로 대조만 하고 재정의하지 않는다.
- framework/adapters/claude/ W2 정식화 산출물 3종(위 자매 11종의 잔여 3종 — 현행 Baseline) — agent-binding.md(v0.9 Baseline · BP-7~11·02 §4.1 표·SP-1~5, T3)·harness-binding.md(v0.9 Baseline · 13 §4.1 조합, T3)·scaffold-binding.md(v1.0 Baseline · 12 §4.1·scaffold-template/ 정본, T4). BP-7~11·13 §4.1 조합·12 §4.1 Scaffold 표면의 정식화 실현 소스(§2·§4가 § 포인터로 대조 — r2 반영). 계약 표면은 02·13·12가 소유하며 본 문서는 재정의하지 않는다.
- framework/adapters/claude/ **UAF 정본(uaf/specs) 바인딩 3종**(전부 v1.2 Draft) — contract-binding.md(uaf/specs/03 Project Contract)·entry-binding.md(uaf/specs/01 Entry Layer)·discovery-binding.md(uaf/specs/02 Project Discovery). **비고: 이 3종은 위 "자매 11종" 계수에 합산하지 않는다** — uaf/ 정본의 물리 실현이며 specs/11-adapters.md §3.2-A BP-1~17 커버리지 대상이 아니고, 본 문서 Conformance 판정(verdict·C1~C3·6필드)에 무영향이다(DP-X4). 본 문서는 이 3종을 실현 소스로 인용·대조하지 않는다.
- docs/delegation-protocol.md §3 — 위임/보고 물리 채널 운용(서브에이전트 위임 §3.1·최종 응답 §3.2·병렬 Wave §3.3·반환·에스컬레이션 §3.4). BP-10·BP-11 실현의 정본 근거 소스(agent-binding.md §4가 정식화 — r2).
- .claude/AGENT.md(상위 규약)·.claude/CLAUDE.md(Advisor 진입점)·.claude/agents/ 4종(advisor·planner·verifier·worker.md) — BP-7·BP-8·BP-9의 실물 실측 대상.
- specs/00-glossary.md §3.2 — Adapter Interface·바인딩 지점(Binding Point)·Conformance·완전/최소 구현 Adapter·핵심 루프(Core Loop) 표제어 정본. 본 문서는 새 용어를 신설하지 않는다.
- docs/v0.8-verification-report.md §4(final_verdict = Pass, 충족 29/위반 0/판정 불가 0)·§5·§3.5(Core 무변경·핵심 루프 통과 실증). C2·C3 근거 인용.
- specs/12-scaffold.md §1·§2·§4.1·§5 — Scaffold의 설치 도구 성격·Bootstrap 이전 동작. DP-A3 근거. § 포인터로만 참조.
- specs/13-harness.md §4.1 — Harness 최소 구성 Claude 조합 바인딩. harness-binding 배정(§4)의 근거. § 포인터로만 참조.
- ROADMAP.md v0.9(Adapter Layer 정식화)·v1.0(Adapter Interface 최종 규격·2nd Adapter 최소 구현 판정). 완전 Adapter 판정 시연(11 §7)의 마일스톤 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 11 §3.3 INV-3, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — 자매 바인딩 11문서 §0과 동형). 단 이 문서는 Core Contract 특히 **Frozen specs/11 §3(Adapter Interface·Conformance·구조 규격)을 재정의·확장하지 않는다** — 계약(바인딩 지점·판정 기준·Report 필드·불변 규칙)은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.9 Draft | 최초 작성. `framework/adapters/claude/` 경계의 아홉 번째 산출물(선행 자매 8문서: runtime·memory·verifier·loop·workflow·hooks·skills·plugins-binding.md). Adapter Interface(11 §3.2-A BP-1~BP-17)의 Claude 물리 실현 **커버리지 매트릭스 17행 전건**(§2 — BP 번호 / 무엇을 바인딩하는가(11 §3.2-A 정본 인용) / 필수·선택 / 물리 실현 지점(정본 문서·§ 포인터·실물 경로) / 실재 여부). BP-7~11은 현행 분산 실현(02 §4.1 + .claude/ 실물 + runtime-binding.md §2 #2 + delegation-protocol.md §3) 명시. **Conformance Report(11 §3.2-D 6필드)** 산출(§3 — adapter=claude·verdict=Valid(Full)·missing_bindings 없음(C1)·core_modifications 없음(C2)·loop_pass 예(C3)·notes 선택 4종 전건 제공). 정식화 배정표(§4 — agent-binding.md(T3)·harness-binding.md(T3)·scaffold-binding.md·scaffold-template/(T4)·.claude/commands/(T5); 작성 시점 스냅샷·후속 격리 갱신 T15 예정, L-07). Advisor 결정 기록 2건 명문화(§5 — DP-A2 `adapters/claude/` 축약 표기 해소·DP-A3 `framework/scaffold/` 미신설; Worker는 기록만, 결정 주체=Advisor·사용자 승인 2026-07-06). 상태 서술 실측 대조 표(§6 — 실재 서술 전건 파일 시스템 직접 실측 후 기입, L-07). specs/11 §3 계약 재정의·확장 0·새 BP·새 필드·새 verdict 값 창설 0·Frozen specs 계수 = 15(numbered 00~13 = 14 + TEMPLATE 1, DP-U3(c))·Glossary 밖 새 용어 0. 형제 Task(spec-versioning-policy.md) 내용 불인용(07 R2). 이 1파일만 생성 — 자매 바인딩 8문서·specs/·docs/·.claude/ 무수정(07 R4). | Worker (Advisor 위임, Task T1) |
| 2026-07-06 | v0.9 Draft (r2 — 정식화 실재 반영) | W2 정식화 산출물 실재 반영(OQ-AC-1·§4 예고 T15 갱신 이행). (1) §2 커버리지 매트릭스 정합화 — BP-7~11 행 "물리 실현 지점"을 현행 분산 실현 서술에서 **정식화 완료(agent-binding.md §2·§3·§4, 2026-07-06 T3)**로 갱신하고 분산 실현 소스(02 §4.1 등)는 정본 근거로 병기 유지; BP-6 행에 `.claude/commands/` 실물(uahf-status.md — Presentation 진입 표면) 실재 반영; BP-13 행에 scaffold-binding.md §4(Install Manifest 직렬화) 병기. (2) §4 배정표 전수 갱신(L-06) — 4행 전건 "예정 — 미존재"→"이행 — 실재(2026-07-06)"·각 실물 § 포인터 병기·§4 주 이행 완료 서술. (3) §6 실측 대조 표 갱신 — 배정 대상 4종 "실재"(직접 재실측)·agent/harness-binding·scaffold-template/(13파일)·.claude/commands/uahf-status.md 신규 실물 행 추가; §0·§1·§10 요약 같은 상태 서술 전 지점 전수 갱신(L-06 grep 열거 후 지점별 판정). (4) **Conformance 판정 불변** — verdict=Valid(Full)·C1~C3 판정·6필드 값 무변경(§3 표 무변경; C1 근거에 정식화 문서 병기만). (5) 상태 라인·§9 r2 행(직전 문면 병기 보존, L-13). 기존 T1 행 문면 불변(L-10). 형제 Task(PS3: structure.md 개정분·v0.9-demo-procedure.md) 불인용(07 R2). specs/11 무변경·새 BP·새 verdict 창설 0. 이 1파일만 수정(07 R4). | Worker (Advisor 위임, Task T15) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-07 | v1.2 Draft (개정 — 계수 실측 정합) | 자매 바인딩 계수 표현 8→**11** 실측 정합(이월 후보 해소 — 핸드오프 v1.1 §1.6-b#3 "자매 8문서 계수 표현 정합"). 갱신 지점: 상태 라인·§0 근거 정본(자매 11종 목록+W2 3종 Baseline 라벨)·거버넌스 문단·§0 격리 문단·§1 목적·§2 주(형태 A/B)·C2 근거·§6 실측 대조 표 등 전 지점의 "자매 8문서/8파일"을 실측 11종(runtime·memory·verifier·loop·workflow·hooks·skills·plugins·agent·harness·scaffold-binding.md — 각 문서 머리 버전 직접 실측 병기: hooks·plugins v0.9·scaffold v1.0 정정 포함)으로 갱신. UAF 정본(uaf/specs) 바인딩 3종(contract·entry·discovery-binding, v1.2 Draft)을 "자매 11종" 계수와 **구분되는 비고**로 표기 — specs/11 §3.2-A BP-1~17 커버리지 대상 아님·Conformance 판정 무영향(DP-X4). **verdict(Valid(Full))·BP-1~17 매트릭스·C1~C3 판정 논리·6필드·specs/11 계약 인용 일절 불변** — 계수·열거 표현만 정합. 기존 이력 행 문면 불변(L-10 — T1 행의 "선행 자매 8문서"는 T1 창작 시점 사실로 보존). 병렬 집합 형제 Task(ROADMAP.md·structure.md) 불인용(07 R2). 이 1파일만 수정(07 R4). | Worker (Advisor 위임, Task T-A) |
| 2026-07-07 | v1.2 Baseline | v1.2 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass 16/0/0; CP3 Advisor 승인) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 Frozen specs/11-adapters.md §3(§3.1 Judge Conformance·§3.2-A 바인딩 지점 목록·§3.2-B 적합성 기준·§3.2-C 구조 규격·§3.2-D Conformance Report·§3.3 Invariants)와 §4.1(Claude Code 바인딩 값)이다.** 이 문서는 그 계약의 **환경 실현 커버리지 대조 + Conformance 판정 산출**이며, 계약 요소(바인딩 지점 정의·판정 조건 C1~C3·Report 필드·verdict 값·등급 기준·불변 규칙)를 **재정의·확장하지 않는다**. 계약 요소는 11 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 11 §4.1이 "각 spec §4에 분산 정의된 바인딩들이 v0.9에서 이 규격 아래로 정식화된다"고 예고하고, 11 §3.2-C·§4·§8이 구체 어댑터명·실명 경로를 §4·§8에 격리한 지점의, **Adapter 전체에 대한 완전성·불변·루프 통과 판정이 실재하는(산출되는) 유일한 자리**다. 개별 바인딩 지점의 물리 실현 상세는 자매 11문서가 소유하며, 본 문서는 그 실현을 **17개 바인딩 지점 전체에 대해 하나의 커버리지 매트릭스로 통합·대조**하고 Conformance Report를 낸다(11 §1 "그 목록에 대한 완전성·불변·루프 통과를 판정한다").
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 01 §3.3 INV-4). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형식명, 물리 경로 `framework/adapters/claude/…`·`.claude/…`·`~/.claude/…`·`docs/…`, 세션/턴, 서브에이전트, Opus 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 바인딩 11문서 §0과 동형). **단 이 허용은 specs/11(Frozen)의 §3 계약 문면을 바꿀 권한을 뜻하지 않는다** — 11은 무변경, 인용만 한다.
- **창설 금지.** 이 문서는 11 §3.2-A **17개 바인딩 지점을 넘어서는 새 바인딩 지점(새 BP)을 창설하지 않는다**. 11 §3.2-D 6필드를 넘어서는 **새 Report 필드**를, 11 §3.2-B의 `Valid(Full)`/`Valid(Minimal)`/`Invalid`를 넘어서는 **새 verdict 값**을 만들지 않는다. Adapter Interface·Conformance 기준·등급 정의는 전부 11 §3이 소유하며 본 문서는 인스턴스 판정만 낸다.
- **판정 성격(최종 승인 아님).** 본 문서가 산출하는 Conformance Report(§3)는 11 §3.1 Judge Conformance 연산의 출력 인스턴스이자, Adapter 자기완결 커버리지의 근거 정리다. 그러나 **이 산출 자체는 최종 승인이 아니다** — 완료 조건 대조의 독립 판정(CP2 — Verifier, 11 §7 "Verifier가 필수 바인딩 체크리스트를 대조")과 최종 승인(CP3 — Advisor, 11 §7 "Advisor가 Conformance Report를 검토해 최종 승인")이 뒤따른다(02 §3.2-A, AGENT.md Verification). 본 문서는 verdict를 스스로 확정 승인하지 않고 근거와 함께 제시한다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, delegation-protocol.md §0). 다수 바인딩 지점은 정식 실행 Module이 아니라 규약 문서·관행으로 실현된다(형태 A). 따라서 커버리지 매트릭스의 "실재 여부" 열은 **물리 실재**(파일·디렉터리·데이터가 존재)와 **규약 실현(형태 A)**과 **형태 B 예정**(실행 코드 도입 시)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다. C3(핵심 루프 통과)은 이 Bootstrap 상태에서 이미 반복 통과했으며(§3 loop_pass), Full/Minimal 판정은 기능 완성이 아니라 "다른 AI에 적용 가능함의 증명"을 목적으로 한다(11 §3.2-B).
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(session-handoff-v0.3.md §1.4 A5 사례·§1.5 Lesson 후보 3, Active Lesson L-07). §2 "실재 여부" 열·§6 실측 대조 표의 전 행은 파일 시스템 직접 실측에 근거한다 — 미존재를 실재로, 미래 산출물을 현재 실재로 쓰지 않는다. **r2(2026-07-06) 재실측:** 최초(T1) 작성 시점에 "예정 — 미존재"였던 §4 배정 대상 4종(agent-binding.md·harness-binding.md·scaffold-binding.md·scaffold-template/·`.claude/commands/`)은 W2(T3·T4·T5) 이행으로 **실재로 전환**되었으며, 본 r2가 §2·§4·§6의 관련 서술을 그 실재로 직접 재실측 후 전수 갱신했다(L-06).
- 용어는 specs/00-glossary.md 정본만 사용한다. Adapter Interface·바인딩 지점(Binding Point)·Conformance·완전/최소 구현 Adapter·핵심 루프(Core Loop)는 Glossary §3.2 정본이며(11 §9 OQ-2 승격), 본 문서는 그 물리 실현 판정만 낸다. `형태 A/B`는 structure.md 서술 라벨의 인용이며 Glossary 표제어가 아니다. `DP-A2`·`DP-A3`는 본 문서가 기록하는 Advisor 결정 라벨이다(§5). 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 Frozen specs/11의 Adapter Interface(§3.2-A)를 Claude Code Adapter 위에 대조하여 **완전성·불변·루프 통과를 판정**한다(11 §1·§3.1).

책임은 네 가지다.

- 11 §3.2-A **바인딩 지점 17개(BP-1~BP-17) 전건**에 대해, 각 지점을 Claude 환경에서 실현하는 물리 지점(정본 문서·§ 포인터·실물 경로)과 실재 여부를 하나의 커버리지 매트릭스로 통합한다(§2, done 1). BP-7~11은 **정식화 완료(agent-binding.md §2·§3·§4·§5, 2026-07-06 T3)**를 실현 지점으로 명시하고, 그 정식화가 통합한 분산 실현 소스(02 §4.1 + .claude/ 실물 + runtime-binding.md §2 #2 + delegation-protocol.md §3)를 정본 근거로 병기한다(r2 정합화).
- 커버리지에서 C1~C3(11 §3.1)을 대조해 **Conformance Report(11 §3.2-D 6필드)**를 산출한다(§3, done 2) — verdict = **Valid(Full)**.
- BP-7~11·13 §4.1 조합·12 §4.1 Scaffold 표면·Presentation 진입 표면(BP-6 확장)의 **정식화 배정**을 표로 명시한다(§4, done 3) — r2 시점에 배정 대상 4종은 W2(T3·T4·T5)로 **이행 완료·실재**이며, 본 문서 §2·§6가 그 실물 § 포인터로 정합화(격리 갱신 T15)되었음을 명시한다(L-06·L-07).
- Advisor 결정 기록 2건(DP-A2·DP-A3)을 명문화한다(§5, done 4) — Worker는 **기록만** 하며 결정 주체는 Advisor다(사용자 승인 2026-07-06 계획). 그리고 상태 서술을 실측과 대조한다(§6, done 6).

이 문서는 11 §3의 어떤 계약 요소도 재정의·확장하지 않는다(§0·§7, done 5). 새 바인딩 지점·새 Report 필드·새 verdict 값 창설 0건이다.

---

## §2. Adapter Interface 커버리지 매트릭스 — BP-1~BP-17 (done 1)

11 §3.2-A 바인딩 지점 목록의 **17행 전건**을 Claude 물리 실현으로 대조한다. "무엇을 바인딩하는가" 열은 11 §3.2-A 정본 표의 값을 그대로 인용하고, "필수/선택"은 11 §3.2-A 지위를 그대로 보존하며, "물리 실현 지점" 열이 그 지점을 실현하는 자매 바인딩 문서·§ 포인터·실물 경로를, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을 정직하게 구분한다(§6 실측 대조). "실재" 서술은 전건 파일 시스템 직접 실측 후 기입했다(L-07).

| BP | 무엇을 바인딩하는가 (11 §3.2-A 정본 인용) | 필수/선택 | Claude 물리 실현 지점 (정본 문서·§ 포인터 · 실물 경로) | 실재 여부 |
|---|---|---|---|---|
| BP-1 | Module/Plugin Manifest를 대상 환경의 서술자 포맷으로 직렬화 | 필수 | runtime-binding.md §2 #1·§3.1 (Markdown + front-matter 직렬화, 11 §4.1 값). 실물: `.claude/agents/*.md` front-matter | 형식·정의 파일 실재. 7필드 완전 직렬화 인스턴스는 형태 B |
| BP-2 | Module 정의를 로드해 entrypoint를 해소하는 로더 | 필수 | runtime-binding.md §2 #2·§3.2 Resolve (파일 기반 정의 로딩, 11 §4.1 값). 서브에이전트 위임 시 활성 정의 파일 로딩 | 규약 실현(형태 A). 실행 로더는 형태 B |
| BP-3 | Global/Project/Module 스코프 Config의 물리 소스·위치·로딩 메커니즘 | 필수 | runtime-binding.md §2 #4~#6·§3.3 (Config 3스코프 물리 소스). 실물: `~/.claude/settings.json`(Global)·`.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`(Project)·정의 파일 설정 블록(Module) | Config 물리 소스 실재. effective config 로딩은 형태 B |
| BP-4 | Bootstrap~Serve~Shutdown 구간을 담는 실행 프로세스/세션 | 필수 | runtime-binding.md §2 #10·§3.4 (세션/턴 = Bootstrap~Serve~Shutdown 실행 컨테이너). 실물: 현 세션 | 컨테이너 실재(현 세션). 실행 Bootstrap/Shutdown은 형태 B |
| BP-5 | Adapter 산출물과 Core를 물리적으로 분리하는 디렉터리·배치 규약 | 필수 | structure.md §2·§3·§8·runtime-binding.md §5 (Core `framework/core/`·`framework/runtime/` / Adapter `framework/adapters/`·`.claude/`, 물리 비중첩). 실물: 위 4경계 | 실재(경계 물리 분리·비중첩 실측) |
| BP-6 | 확장 Module(확장점·능력·묶음)의 등록·발견·지연 로드·배포 표면 | **선택** | hooks-binding.md §2·§4 · skills-binding.md §2·§3 · plugins-binding.md §2·§3 · runtime-binding.md §2 #3. 실물: `.claude/hooks/`·`.claude/skills/`·`.claude/commands/`(Presentation 진입 표면 — `uahf-status.md` 실물) | 세 확장 표면 디렉터리 실재. 확장 실물은 v0.8 시연(F-H1/F-S1/F-P1)으로 실증. `.claude/commands/uahf-status.md` 실재(2026-07-06 T5, §4·§6) |
| BP-7 | Advisor/Planner/Worker/Verifier 4역할 정의를 대상 환경 메커니즘으로 제공 | 필수 | **정식화 완료 — agent-binding.md §2 행 1(2026-07-06 T3)**. 정본 근거(병기): 02 §4.1(Agent 정의 파일) + runtime-binding.md §2 #2(Agent Module 진입점). 실물: `.claude/agents/{advisor,planner,worker,verifier}.md` | 실재(4역할 정의 파일 실측). 정식화 이행 완료 — agent-binding.md §2 행 1(§4·§6) |
| BP-8 | 공통 규약·시스템 프롬프트·오케스트레이터 진입점 주입 방식 | 필수 | **정식화 완료 — agent-binding.md §2 행 2(2026-07-06 T3)**. 정본 근거(병기): 02 §4.1(공통 규약 바인딩). 실물: `.claude/AGENT.md`(상위 규약)·`.claude/CLAUDE.md`(Advisor 진입점) | 실재(2파일 실측). 정식화 이행 완료 — agent-binding.md §2 행 2(§4·§6) |
| BP-9 | 각 Agent 역할의 실행 모델·엔진 지정 | 필수 | **정식화 완료 — agent-binding.md §2 행 3·§3(2026-07-06 T3)**. 정본 근거(병기): 02 §4.1(실행 모델 바인딩·SP-3) + loop-binding.md §5.1(역할 실행 모델 참조). 실물: worker.md·planner.md·verifier.md front-matter `model: opus`; advisor.md 세션 상속 | 실재(3파일 `model: opus`·advisor 세션 상속 실측). 정식화 이행 완료 — agent-binding.md §3(DP-E8 기록, §4·§6) |
| BP-10 | 위임 메시지를 Agent에 전달하는 호출·오케스트레이션 채널 (병렬 디스패치·재위임 포함) | 필수 | **정식화 완료 — agent-binding.md §2 행 4·6·§4.1(2026-07-06 T3)**. 정본 근거(병기): 02 §4.1(서브에이전트 위임) + delegation-protocol.md §3.1·§3.3 + workflow-binding.md §5.1(병렬 디스패치) | 규약 실현(형태 A). spec 병렬 작성 Wave(07 §8 예1)로 실증. 정식화 이행 완료 — agent-binding.md §4.1(§4·§6) |
| BP-11 | 완료 보고·실패 보고를 반환하는 결과 채널 | 필수 | **정식화 완료 — agent-binding.md §2 행 5·§4.2(2026-07-06 T3)**. 정본 근거(병기): 02 §4.1(서브에이전트 최종 응답) + delegation-protocol.md §3.2·§3.4 | 규약 실현(형태 A). v0.2~v0.8 보고 회수로 실증. 정식화 이행 완료 — agent-binding.md §4.2(§4·§6) |
| BP-12 | Memory Service 영속성 백엔드 (단일 Port 뒤) | **선택** | memory-binding.md §2·§3 (파일 기반 store·index·직렬화·I/O, 단일 Port 격리). 실물: `framework/adapters/claude/memory-data/`(store/`<id>.json`·index/index.jsonl) | 실재(memory-data/ 백엔드·데이터 실측) |
| BP-13 | 구조화된 계약 산출물·상태 기록의 직렬화 및 작업 추적·결정 기록 메커니즘 | 필수 | loop-binding.md §3(loop-data 전이 이벤트) · verifier-binding.md §4(검증 리포트 직렬화) · workflow-binding.md §3(Work Graph·Merge Result 문서 형태) · scaffold-binding.md §4(Install Manifest 직렬화 — Markdown + front-matter 6필드, 2026-07-06 T4). 실물: `framework/adapters/claude/loop-data/`(9 jsonl)·`docs/v0.X-verification-report.md`(6건)·ROADMAP.md·docs/ 시연 소산·`scaffold-template/install-manifest.template.md` | 실재(loop-data/·검증 리포트 6건·계획 문서·Install Manifest 템플릿 실측) |
| BP-14 | 사람에게 승인·개입 요청을 제시하고 응답을 받는 채널 | 필수 | loop-binding.md §2 #6·§5.2 (사람 개입 채널). 실물: 주 세션 사용자 제시 + `.claude/CLAUDE.md` "Architecture/Spec 충돌 시 사용자 보고" 규칙(03 §3.1-D 조건 4 바인딩) | `.claude/CLAUDE.md` 조건 4 바인딩 실재. 세션 제시 규약 실현(형태 A) |
| BP-15 | 검증에 쓰이는 검사 도구 (존재 확인·전수 스캔·시연 실행) | 필수 | verifier-binding.md §5 (VT-1~VT-5 검사 도구 바인딩). 실물: 파일 조회·텍스트 검색·명령 실행 도구 표면 | 도구 표면 실재. v0.3~v0.8 검증 리포트 6건이 실사용 실증 |
| BP-16 | 이벤트 원천의 계측·방출 지점과 확장 실행기(결정적 순서·격리)·원천 컨텍스트 전달 | **선택** | hooks-binding.md §3(이벤트 카탈로그 18행 계측 지점)·§5(Hook Dispatch 물리 절차). 실물: `.claude/hooks/`(등록 표면); 형태 B 자리: `.claude/settings.json`(미존재) | 등록 표면·계측 지점 참조 실재. Dispatch 규약 실현(형태 A). native hook 실행 메커니즘은 형태 B |
| BP-17 | 상황 서술자와 적용 조건의 대조 알고리즘 | **선택** | memory-binding.md §5.2 (applicability 매칭 구현 — 라벨 집합 겹침; 05 §4.1 SP-2). 실물: memory-data/ index `labels` 대조 | 실재(구현 선택 = 라벨 겹침). v0.4~v0.8 회수로 실증 |

주:

- 위 17행은 11 §3.2-A 바인딩 지점 목록의 전 행이다. 각 행의 "무엇을 바인딩하는가"·"필수/선택"은 11 §3.2-A 정본 표를 그대로 보존하며(재정의 0), "물리 실현 지점"은 그 지점의 실현을 소유한 자매 바인딩 문서(BP-7~11은 정식화 문서 agent-binding.md·정본 근거 소스 — r2)로 대조 배정한 것이다. 새 바인딩 지점을 창설하지 않는다(§0).
- **필수 13개 / 선택 4개(11 §3.2-B 정본).** 필수 = BP-1·2·3·4·5·7·8·9·10·11·13·14·15(최소 바인딩 부분집합 정본). 선택 = BP-6·12·16·17. 이 구분은 11 §3.2-B가 소유하며 본 표는 그 지위를 인용한다.
- **정식화 완료(BP-7~11) — r2 갱신.** BP-7~11은 v0.9 W2(Task T3)에서 전용 바인딩 문서 **agent-binding.md**로 정식화되었다(§2 행 1~6·§3 실행 모델·§4 위임/보고 채널·§5 SP-1~SP-5). 이 문서가 종전 분산 실현(02 §4.1(Agent Component Adapter Binding)·`.claude/` 실물·runtime-binding.md §2 #2(Agent Module 진입점 = Runtime generic Module 계약의 Agent 구현 바인딩)·delegation-protocol.md §3(위임/보고 물리 채널 운용))을 한 문서로 **통합·정식화**한 것이며, 새 BP·새 계약 창설이 아니다(agent-binding.md §7). 분산 실현 소스는 정본 근거로 병기 유지하며, §4가 그 배정의 이행을 명시한다.
- **물리 실재 / 형태 A / 형태 B 구분(정직).** 실물 파일·디렉터리·데이터(예: `.claude/agents/` 4파일·memory-data/·loop-data/·검증 리포트 6건·4경계 분리)는 물리 실재다. 위임/보고·역할 실행·Dispatch·사람 개입 등 오케스트레이션은 Bootstrap에서 규약 실현(형태 A)이며, 무인 자동 실행 채널·실행 로더·native hook 실행은 형태 B다. 이 구분은 자매 11문서의 형태 A/B 구분과 정합한다.

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

- **C1 (필수 바인딩 완전성 — 11 §3.1).** 11 §3.2-B 최소 바인딩 부분집합(필수 13개: BP-1·2·3·4·5·7·8·9·10·11·13·14·15)이 §2 커버리지 매트릭스에서 전건 물리 실현 지점을 갖는다 — 누락(missing) 0건. 각 지점의 실현 소스는 자매 바인딩 문서(BP-7~11은 종전 분산 실현이 정식화 문서 **agent-binding.md**(2026-07-06 T3)로 통합·정식화됨 — r2 정합화; BP-13은 scaffold-binding.md §4 Install Manifest 직렬화 병기 포함)이며, 실물 실재는 §6 실측으로 확인된다. 정식화는 실현 소스의 통합이지 필수 완전성 판정의 변경이 아니다 — 따라서 `missing_bindings` = 없음(INV-2 필수 완전성 충족, verdict 불변).
- **C2 (Core Contract 불변 — 11 §3.1).** Adapter는 바인딩만 추가하고 어떤 Core Contract도 수정·확장·삭제하지 않는다. 근거: (a) v0.3~v0.8 각 마일스톤 CP2 독립 판정이 Core 무변경을 실측했다 — 예 docs/v0.8-verification-report.md item #3·#16·§3.5(Frozen specs·`framework/core`·`framework/runtime` 기준선이 각 쓰기 창 밖·본체 diff 0). (b) 본 작성 시점 실측(§6): `framework/core/`(structure.md·config-schema.md 2문서)·`framework/runtime/`(module-manifest·module-registry·lifecycle 3문서)가 계약 문서만 보유하고 AI 의존 요소 0건(structure.md §5 C-3, 01 §3.3 INV-4). 자매 11문서·본 문서 모두 `framework/adapters/claude/` 경계 안에서만 구체 토큰을 격리 보유하며 Core 경계를 침범하지 않는다(11 INV-3·INV-1). 따라서 `core_modifications` = 없음.
- **C3 (핵심 루프 통과 — 11 §3.1).** 위임 → 구현 → 검증 → 승인 핵심 루프(Glossary 핵심 루프·delegation-protocol.md §1)가 이 Adapter 위에서 1회 이상 통과한다. 근거: v0.2 Agent Harness Bootstrap 이래 v0.3~v0.8 각 마일스톤이 위임(Advisor)→구현(Worker)→독립 검증(Verifier CP2)→최종 승인(Advisor CP3)의 핵심 루프를 반복 통과했고, 그 통과가 docs/v0.3~v0.8-verification-report.md 6건과 각 Baseline 승인 기록으로 실증된다. 가장 최근 v0.8은 final_verdict = Pass(충족 29 / 위반 0 / 판정 불가 0, docs/v0.8-verification-report.md §4). 따라서 `loop_pass` = 예.

### §3.2 등급 판정 (11 §3.2-B)

Claude Code Adapter는 C1~C3을 만족(Valid)하고, 선택 바인딩 4종(BP-6·12·16·17)을 기능 완성 수준으로 제공한다 — BP-6은 hooks/skills/plugins-binding.md + `.claude/{hooks,skills,commands}` 표면과 v0.8 확장 3종 시연(F-H1/F-S1/F-P1), BP-12는 memory-binding.md + memory-data/ 백엔드, BP-16은 hooks-binding.md 계측 18행·Dispatch, BP-17은 memory-binding.md §5.2 매칭 구현. 따라서 등급은 **완전 Adapter(Full Adapter)**이며 verdict = **Valid(Full)**이다(11 §3.2-B·§7 완전 Adapter 판정 시연). 이는 11 §7 "완전 Adapter 판정 시연"과 정렬한다.

### §3.3 판정 성격 재확인

본 Conformance Report는 11 §3.1 Judge Conformance의 출력 인스턴스이자 근거 정리다. **verdict = Valid(Full)은 근거와 함께 제시된 것이며, 본 문서가 스스로 최종 승인 처리한 것이 아니다.** Verifier의 독립 판정(CP2 — 11 §7 필수 바인딩 체크리스트 대조·Core diff·루프 통과 기록 대조)과 Advisor의 최종 승인(CP3 — 11 §7 Conformance Report 검토)이 뒤따른다(02 §3.2-A). 조건부·재량 항목을 스스로 통과 처리하지 않는다(§0 판정 성격).

---

## §4. 정식화 배정표 (done 3)

BP-7~11의 정식화와 인접 표면(13 §4.1 조합·12 §4.1 Scaffold·Presentation 진입 표면)의 정식화 배정이다. **각 행의 배정 대상은 W2(Task T3·T4·T5)에서 생성 완료되어 실재하며(2026-07-06 직접 재실측 — §6), 본 r2가 §2 커버리지 매트릭스의 실현 지점·실재 서술을 그 실물 § 포인터로 정합화(격리 갱신 T15)했다**(memory-binding.md §9 r2·loop-binding.md·workflow-binding.md가 시연·정식화 후 격리 개정한 관례 동형). 각 배정 대상이 실현한 interfaceContract·소유 경계(ownedBoundary)의 계약 표면은 정본이 소유하며, 본 문서는 § 포인터로 대조만 한다(재정의 0 — 정식화이지 판정 변경이 아니다).

| 배정 대상 (이행 — 실재 2026-07-06) | 배정 BP·정본 § | 실현한 interfaceContract (§ 포인터 — 실물 정합) | 소유 경계 (ownedBoundary) | 이행 Task · 실물 § 포인터 |
|---|---|---|---|---|
| `agent-binding.md` | BP-7·BP-8·BP-9·BP-10·BP-11 (02 §4.1 바인딩 표·§4.2 SP-1~SP-5) | Agent Component의 Claude 물리 실현 — Agent 정의 파일·상위 규약 바인딩·실행 모델 지정·서브에이전트 위임/최종 응답 채널(02 §4.1). 종전 분산 실현(02 §4.1 + .claude/ 실물 + runtime-binding.md §2 #2 + delegation-protocol.md §3)을 한 문서로 통합·정식화. 계약 표면은 02 소유(재정의 0). | `framework/adapters/claude/agent-binding.md` 1파일 | **이행 — 실재(2026-07-06 T3).** 실물 § 포인터: agent-binding.md §2(02 §4.1 표 6행)·§3(실행 모델 실측·DP-E8)·§4(위임/보고 채널)·§5(SP-1~SP-5). |
| `harness-binding.md` | 13 §4.1 조합 (7행) — 상위 규약·역할 4종·위임/보고·검증 게이트·작업 추적·실행 모델·호스트 프로세스 | Harness 최소 구성 5요소(13 §3.2-A)의 Claude 조합 물리 실현(13 §4.1). Harness는 02·01 계약의 최소 부분집합 조합만 소유(13 §3 서두)이므로 agent-binding.md·runtime-binding.md 실현을 조합 참조. 계약 표면은 13·02·01 소유(재정의 0). | `framework/adapters/claude/harness-binding.md` 1파일 | **이행 — 실재(2026-07-06 T3).** 실물 § 포인터: harness-binding.md §2(13 §4.1 조합 7행)·§3(최소 구성 5요소 실측)·§4(이식 교체 지점 1~6)·§5(전이 조건 판정 비수행 — T11 소관). |
| `scaffold-binding.md` · `scaffold-template/` | 12 §4.1 Scaffold 표면 (10행) — 규약 문서·Agent 정의·Config·specs/·Core/Adapter 경계 초기화·Install Manifest·버전 값·Bootstrap/Loop 구동 확인 | Scaffold 설치·초기화 표면의 Claude 물리 실현(12 §4.1) + 프로젝트 템플릿(12 §3.2-A Project Template)의 물리 자산. Scaffold는 Bootstrap 이전 설치 도구(DP-A3·§5). 계약 표면은 12 소유(재정의 0). | `framework/adapters/claude/scaffold-binding.md` + `framework/adapters/claude/scaffold-template/` | **이행 — 실재(2026-07-06 T4).** 실물 § 포인터: scaffold-binding.md §2(12 §4.1 표 10행)·§3(3연산)·§4(Install Manifest 직렬화)·§5(CK-1~CK-8)·§6(scaffold-template/ 정본); scaffold-template/ 13파일 실재(§6). |
| `.claude/commands/` (Presentation 진입 표면) | Presentation 진입 표면 (BP-6 확장 — 11 §3.2-A BP-6 확장 Module 표면) | 사용자 대면 명령 진입 표면의 물리 실현(Presentation Layer, Glossary §3.2-A 스택 최상위). BP-6 확장 표면(`.claude/commands/`)의 Presentation 국면. 확장 계약 표면은 08·09·10 및 Presentation 소관(재정의 0). | `.claude/commands/` 이하 | **이행 — 실재(2026-07-06 T5).** 실물: `.claude/commands/uahf-status.md`(Presentation 진입 명령 — 형태 A 문서 명령, 실행 코드 0). §2 BP-6 행에 반영. |

주:

- **이행 완료·실측 정합(L-06·L-07) — r2 갱신.** 위 배정 대상 4종은 W2(Task T3·T4·T5)에서 생성 완료되어 **실재**한다(§6 실측: agent-binding.md·harness-binding.md·scaffold-binding.md·scaffold-template/ 13파일·`.claude/commands/uahf-status.md` 전건 확인, 2026-07-06 직접 재실측). 최초(T1) 작성 시점에 "예정 — 미존재"였던 이 표는 본 r2에서 이행·실재로 전수 갱신했고, §2 커버리지 매트릭스의 실현 지점·§6 실측 대조 표를 그 실물 § 포인터로 정합화(격리 갱신 T15)했다. 실재를 파일 시스템 재실측 후에만 기입했고, 배정 대상의 계약 표면을 재정의하지 않았다(재정의 0).
- **소유 경계 비중첩.** 각 배정 대상의 소유 경계(ownedBoundary)는 파일·디렉터리 단위로 쌍별 교집합 0이다(07 R4·INV-2) — agent-binding.md·harness-binding.md·scaffold-binding.md는 서로 다른 파일, scaffold-template/·.claude/commands/는 서로 다른 디렉터리. W2 각 Task(T3·T4·T5) 위임 시 각 소유 경계가 그 Task의 배타 소유였고, 본 r2(T15)는 이 파일(adapter-conformance.md) 1개만 수정한다(07 R4).
- **BP-7~11 커버리지 무결성(정식화 후).** BP-7~11은 최초 시점에도 분산 실현으로 물리적으로 완전했고(실물 실재), 이제 agent-binding.md가 그 분산 실현을 한 문서로 **통합·정식화**했다 — 새 BP·새 계약 창설이 아니며(agent-binding.md §7), 커버리지·verdict는 불변이다. §2 BP-7~11 행이 그 정식화 문서 § 포인터로 정합화되었다(r2).

---

## §5. Advisor 결정 기록 (done 4 — DP-A2·DP-A3)

아래 두 결정의 **주체는 Advisor**이며(사용자 승인 2026-07-06 계획), 본 문서는 그 결정을 **기록만** 한다(Worker는 Architecture·설계 결정을 하지 않는다 — 02 §3.2-A·INV-3). 두 결정은 Frozen specs/11·01을 **무변경**으로 유지하며, 정본 문면의 표기·구조를 재해석·확인하는 성격이다(계약 재정의 아님).

### DP-A2 — `adapters/claude/` 표기의 물리 경로 축약 해소

- **결정.** specs/11 §3.2-C(구조 규격 "Adapter는 `adapters/<이름>/` 아래에 배치한다")·§4.1(첫 번째 Adapter "배치 경로는 `adapters/claude/`")의 `adapters/<이름>/`·`adapters/claude/` 표기는, 물리 경로 `framework/adapters/<이름>/`·`framework/adapters/claude/`의 **축약 표기로 해석한다.**
- **물리 정본.** 물리 경로의 정본은 (a) 01 §4.1(Adapter Binding 산출물 = `framework/adapters/`·`.claude/`), (b) structure.md §2(Adapter 경계 = `framework/adapters/<adapter>/`), (c) runtime-binding.md §5(`<adapter>` = `claude` 구체화 = `framework/adapters/claude/`)이다. §2 커버리지의 BP-5(디렉터리·배치 규약) 행이 이 물리 경로를 실물로 담는 자리다.
- **Frozen 11 무변경.** 이 결정은 Frozen specs/11의 §3.2-C·§4.1 문면을 **수정하지 않는다** — 11의 `adapters/claude/`는 11 §3.2-C가 명시하듯 "첫 번째 Adapter의 실명 경로는 §4·§8에 둔다"의 상대 표기이며, 그 물리 정본(`framework/` 접두)은 01·structure.md·runtime-binding.md가 이미 소유한다. 정본 문면의 표기 인스턴스(§3.2-C·§4.1의 `adapters/claude/`)를 물리 경로로 해소했을 뿐, 계약을 재정의하지 않았다.

### DP-A3 — `framework/scaffold/` 미신설

- **결정.** `framework/scaffold/` 디렉터리를 **신설하지 않는다.** Scaffold의 물리 실현은 scaffold-binding.md·scaffold-template/(T4 이행·실재 2026-07-06, §4)와 12 §4.1 바인딩 값(`.claude/*`·`specs/`·`framework/` 초기화)으로 실현한다.
- **근거.** (a) 01 §4.1 "Module 구현 디렉터리"는 `framework/{loop,memory,verifier,workflow,plugins}/`로 **5종을 고정 열거**하며(structure.md §2 주 — "다섯 Module 구현 디렉터리 전부 실사용"), Scaffold는 이 열거에 없다 — 이 고정 열거를 보존한다. (b) 12 §1·§2·§5는 Scaffold를 "신규 프로젝트에 UAHF를 부트스트랩(설치·초기화)하는 도구"이자 "프로젝트의 Runtime Bootstrap **이전**에 동작"하는 설치 단계 도구로 규정한다(12 §5) — Scaffold는 Runtime이 호스팅하는 Module이 아니라 설치 도구이므로(12 §2·Non-Goals: "Scaffold는 설치 도구, Harness는 설치되는 실행 골격"), Module 구현 디렉터리를 신설할 대상이 아니다. (c) v0.8 DP-E1 동형 — v0.8도 새 백엔드/디렉터리 신설 없이 정본 문면의 인스턴스로 해소했다(workflow-binding.md §3 DP-W4 "`workflow-data/` 신설 없음", plugins-binding.md §3 DP-E6 "설치본 = 정본 문면의 직접 인스턴스").
- **실측 정합(§6).** 본 작성 시점 실측에서 `framework/` 하위는 adapters·core·loop·memory·plugins·runtime·verifier·workflow의 8경계이며 `scaffold/`는 **부재**다 — 이 결정과 정합한다.

주: 두 결정 모두 Advisor 소관(02 §3.2-A·INV-3, CLAUDE.md "Architecture·설계 결정은 Advisor")이며, 본 문서는 결정의 실재와 정본 정합(재정의 0)을 기록한다. 결정의 재평가·창설은 수행하지 않는다.

---

## §6. 상태 서술 실측 대조 (done 6 — A5/L-07 재발 방지)

session-handoff-v0.3.md §1.4(A5 사례 — 미존재를 "실재"로 서술 → 파일 시스템 전수 대조로 검출)·§1.5 Lesson 후보 3(상태 서술은 실측 후 기록, 이월 L-07)에 따라, 본 문서의 "실재/존재/부재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: r2(2026-07-06) 파일 열거(`ls`/`find`) 직접 재실측.** r2에서 최초(T1) 시점 "예정 — 미존재"였던 §4 배정 대상 4종을 재실측해 실재로 전환된 상태를 반영했다(L-06). **v1.2(2026-07-07) 계수 실측 정합 개정 시 자매 11문서 행·UAF 정본 바인딩 3종 행은 그 시점 직접 재실측으로 갱신·추가했다(각 행에 "2026-07-07" 명기; hooks·plugins v0.9·scaffold v1.0 버전 라벨 실측 반영).**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 자매 바인딩 11문서 (§2 실현 소스 — UAHF spec 바인딩) | 실재 (전부 Baseline) | 실재 — runtime·memory·verifier·loop·workflow·hooks·skills·plugins·agent·harness·scaffold-binding.md 11파일 확인(agent·harness·scaffold는 §4 배정·아래 별도 행 상세; 직접 재실측 2026-07-07). |
| `framework/adapters/claude/` UAF 정본 바인딩 3종 (contract·entry·discovery-binding) | 실재하나 자매 11종 계수에 **미합산**(DP-X4) | 실재 — contract·entry·discovery-binding.md 3파일 확인(전부 v1.2 Draft, 직접 재실측 2026-07-07). specs/11 BP-1~17 커버리지 대상 아님·Conformance 판정 무영향. |
| `framework/adapters/claude/adapter-conformance.md` (본 문서) | 실재 (본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음(사전 실측 확인). |
| `.claude/agents/` 4역할 정의 파일 (BP-7) | 실재 (advisor·planner·worker·verifier.md) | 실재 — 4파일 확인(advisor.md·planner.md·worker.md·verifier.md). |
| `.claude/AGENT.md`·`.claude/CLAUDE.md` (BP-8) | 실재 (상위 규약·Advisor 진입점) | 실재 — 2파일 확인. |
| worker.md·planner.md·verifier.md `model: opus` / advisor.md 세션 상속 (BP-9) | 실재 (역할별 모델 지정) | 실재 — worker.md·planner.md·verifier.md front-matter `model: opus`; advisor.md는 model 라인 부재(세션 상속) 확인. |
| `.claude/hooks/`·`.claude/skills/`·`.claude/commands/` (BP-6·BP-16) | 실재 (확장 표면 디렉터리) | 실재 — 세 디렉터리 확인. `.claude/commands/`에 `uahf-status.md` 실재(2026-07-06 T5 — 아래 별도 행; 최초 T1 시점엔 빈 디렉터리였음). |
| `.claude/settings.json` (BP-16 형태 B 자리) | **미존재** (형태 B 실행 훅 선언 자리) | **미존재** — `.claude/settings.local.json`만 실재. `.claude/settings.json` 부재 확인(hooks-binding.md DP-E3 정합). |
| `framework/adapters/claude/memory-data/` (BP-12) | 실재 (Memory 백엔드) | 실재 — `store/`·`index/` 확인. |
| `framework/adapters/claude/loop-data/` (BP-13) | 실재 (루프 상태 기록 백엔드) | 실재 — 9 jsonl 파일 확인(v06-demo-a/b/c·v07-demo-t1/t2/t3·v08-demo-h/p/s). |
| `docs/v0.X-verification-report.md` (BP-13·C3 근거) | 실재 (6건 — v0.3~v0.8) | 실재 — v0.3·v0.4·v0.5·v0.6·v0.7·v0.8-verification-report.md 6건 확인. |
| `framework/core/`·`framework/runtime/` (C2 Core 경계) | 실재 (계약 문서만·AI 의존 0건 유지 대상) | 실재 — core/(structure.md·config-schema.md 2문서)·runtime/(module-manifest·module-registry·lifecycle 3문서) 확인. |
| `framework/scaffold/` (DP-A3) | **부재** (미신설 결정) | **부재** — `framework/` 하위 = adapters·core·loop·memory·plugins·runtime·verifier·workflow 8경계, `scaffold/` 없음 확인. |
| specs/ Frozen 계수 (done 5) | **15** (numbered 00~13 = 14 + TEMPLATE 1) | 실측 — 00~13 numbered 14파일 + TEMPLATE.md = **15**. |
| `framework/adapters/claude/agent-binding.md` (§4 배정 T3 — BP-7~11 정식화) | 실재 (2026-07-06 이행 — r2 재실측) | 실재 — 파일 확인. §2(02 §4.1 표 6행)·§3(실행 모델 실측·DP-E8)·§4(위임/보고 채널)·§5(SP-1~SP-5) 구성 확인. |
| `framework/adapters/claude/harness-binding.md` (§4 배정 T3 — 13 §4.1 조합) | 실재 (2026-07-06 이행 — r2 재실측) | 실재 — 파일 확인. §2(13 §4.1 조합 7행)·§3(최소 구성 5요소)·§5(전이 조건 판정 비수행 — T11 소관) 구성 확인. |
| `framework/adapters/claude/scaffold-binding.md` (§4 배정 T4 — 12 §4.1) | 실재 (2026-07-06 이행 — r2 재실측) | 실재 — 파일 확인. §2(12 §4.1 표 10행)·§4(Install Manifest 직렬화)·§5(CK-1~CK-8)·§6(scaffold-template/ 정본) 구성 확인. |
| `framework/adapters/claude/scaffold-template/` (§4 배정 T4 — 프로젝트 템플릿) | 실재 (2026-07-06 이행 — 13파일) | 실재 — 13파일 확인: README.md·install-manifest.template.md·dot-claude/{AGENT.md·CLAUDE.md·settings.json.example·agents/4종}·framework/{core,runtime,adapters}/README.md·specs/README.md. |
| `.claude/commands/uahf-status.md` (§4 배정 T5 — Presentation 진입 표면, BP-6) | 실재 (2026-07-06 이행) | 실재 — 파일 확인(Presentation 진입 명령 — 형태 A 문서 명령, 실행 코드 0). 최초(T1) 시점 `.claude/commands/`는 빈 디렉터리였음. |

- **핵심 구분.** 실재를 주장하는 모든 행은 파일 시스템 직접 실측(r2: 2026-07-06 재실측) 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로 쓰지 않았다(A5/L-07 재발 방지). 최초(T1) 시점 "예정 — 미존재"였던 §4 배정 대상 4종은 r2 재실측에서 **실재로 확인**되어 이 표에 반영했다(agent/harness/scaffold-binding·scaffold-template/ 13파일·`.claude/commands/uahf-status.md`). BP-7~11 정식화 문서(agent-binding.md)·현행 실물(`.claude/agents/`·`.claude/AGENT.md`·`.claude/CLAUDE.md`), 선택 바인딩 백엔드(memory-data/·loop-data/), C2·C3 근거(core/·runtime/·검증 리포트 6건), DP-A3 근거(`framework/scaffold/` 부재)가 전부 실측으로 확인되어 §2·§3·§5 판정의 근거가 실재함을 입증한다.

---

## §7. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 5).** 본 문서의 모든 서술은 11 §3(Adapter Interface·Conformance·구조 규격)의 **인스턴스 대조·판정**이다. 어떤 바인딩 지점 정의·판정 조건(C1~C3)·Report 필드·verdict 값·등급 기준·불변 규칙도 이 문서에서 새로 확정되지 않는다 — 판정 기준의 정본은 11 §3이다. **11 §3.2-A 17개 목록을 넘어서는 새 바인딩 지점·11 §3.2-D 6필드를 넘어서는 새 Report 필드·11 §3.2-B 3종(Valid(Full)/Valid(Minimal)/Invalid)을 넘어서는 새 verdict 값·새 등급을 창설하지 않았다.** 개별 바인딩 지점의 물리 실현 상세도 재정의하지 않고 자매 바인딩 문서(BP-7~11은 정식화 문서 agent-binding.md — r2 정합화)·정본 근거 소스의 § 포인터로만 대조 배정했다.
- **Frozen 무변경.** specs/11(Frozen v0.1)·specs/01·02·12·13(Frozen)을 수정하지 않았다. DP-A2·DP-A3(§5)은 정본 문면의 표기·구조를 물리 경로/디렉터리로 해소·확인하는 Advisor 결정 기록이며 Frozen 문면 자체를 바꾸지 않는다(§5). Frozen specs 계수를 표기할 자리에는 **15**(numbered 00~13 = 14 + TEMPLATE 1, DP-U3(c))로 표기했다.
- **격리 토큰의 단일 자리.** 구체 AI·환경·직렬화 형식·물리 경로 토큰(Markdown·front-matter·`.claude/…`·`~/.claude/…`·`framework/adapters/claude/…`·`docs/…`·세션/턴·서브에이전트·Opus 등)은 이 Adapter 경계 문서에만 둔다. Core 경계(`framework/core/`·`framework/runtime/`)·Module 구현 디렉터리·specs/11 §3은 이 토큰을 본문에 두지 않는다(structure.md §5 C-3, 11 INV-7 §3 AI 비의존). 이 문서는 그 격리의 반대편(허용 지점)이다 — 단 11 §3 문면 재정의 권한은 아니다(§0).
- **판정 성격(최종 승인 아님).** §3 Conformance Report의 verdict = Valid(Full)은 근거와 함께 제시된 산출이며, Verifier 독립 판정(CP2 — 11 §7)·Advisor 최종 승인(CP3 — 11 §7)이 뒤따른다. 본 문서는 스스로 최종 승인 처리하지 않았다(02 §3.2-A).
- **동시 작성 문서 경계(07 R2).** (최초 T1: 같은 Wave 형제 Task(spec-versioning-policy.md, T2)의 미완성 산출물을 인용·추측하지 않았다.) **r2(T15):** 같은 병렬 집합 PS3에서 동시 작성 중인 형제 Task 산출물(structure.md 개정분·v0.9-demo-procedure.md 신규)을 인용·추측하지 않았다(07 R2). 참조한 확정 정본은 Frozen specs(11·01·02·12·13·00)·Baseline 자매 바인딩 문서·**W2 확정 산출물(agent-binding.md·harness-binding.md·scaffold-binding.md·scaffold-template/·`.claude/commands/uahf-status.md` — 완료된 선행 Wave, 직접 재실측)**·확정 실사용 산출물(.claude/ 실물·memory-data/·loop-data/·검증 리포트 6건)·ROADMAP.md·structure.md·delegation-protocol.md뿐이다.
- **추측 0 / 소유 경계 준수 (07 R4·INV-2).** (최초 T1: §4 배정 대상은 "예정"으로만 서술하고 미존재를 실재로 쓰지 않았다.) **r2(T15):** §4 배정 대상 4종(agent-binding.md 등)은 W2 이행으로 실재하며, 파일 시스템 직접 재실측 후에만 실재로 기입했다(L-06·L-07). 배정 대상의 계약 표면을 추측·재정의하지 않았다(R2). 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 r2 산출은 이 1개 파일(`framework/adapters/claude/adapter-conformance.md`)만 수정하며, 자매 바인딩 문서·framework/core·framework/runtime·specs/·docs/·.claude/ 실물을 수정·생성하지 않는다(07 R4).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-AC-1 (§2 커버리지 후속 격리 갱신 — 해소·이행 완료 r2).** BP-7~11은 최초(T1) 시점에 현행 분산 실현(02 §4.1 + .claude/ + runtime-binding §2 #2 + delegation-protocol §3)으로 매핑됐고, §4 배정대로 agent-binding.md(T3)가 생성되면 §2 BP-7~11 행의 실현 지점을 그 문서 § 포인터로 정합화하는 격리 갱신(T15)이 예고됐었다. **본 r2(T15)가 그 갱신을 이행했다** — §2 BP-7~11 행·§4 배정표·§6 실측 대조 표를 agent-binding.md § 포인터로 정합화(직접 재실측). 실현 소스의 정식화이지 판정(verdict) 변경이 아니므로 비차단으로 해소됐다.
- **OQ-AC-2 (Presentation Layer 매핑 확정 — 비차단).** §4의 Presentation 진입 표면(`.claude/commands/`, BP-6 확장)의 Layer 귀속은 12 §9-OQ1·13 §2가 Wave 3 Advisor 확정으로 미룬 사안과 인접한다(Glossary §9-OQ6 흐름). 본 문서는 BP-6 확장 표면의 Presentation 국면으로만 배정했고 Layer 귀속 정본을 단정하지 않았다 — Advisor 확정 대상, 비차단.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 아홉 번째 산출물. Frozen specs/11 Adapter Interface(§3.2-A BP-1~17)의 **Claude 물리 실현 커버리지 매트릭스 + Conformance 판정**. 정본 = 11 §3·§4.1(본 문서는 인스턴스 대조·판정, 재정의 아님 — §0).
- **§2:** 11 §3.2-A **17개 바인딩 지점 전건**의 커버리지 매트릭스(BP 번호 / 무엇을 바인딩하는가(정본 인용) / 필수·선택 / 물리 실현 지점(정본 문서·§ 포인터·실물 경로) / 실재 여부). 필수 13 / 선택 4. BP-7~11은 **정식화 완료(agent-binding.md §2·§3·§4·§5, 2026-07-06 T3)**·분산 실현 소스 정본 근거 병기(r2). BP-6에 `.claude/commands/uahf-status.md`(Presentation 진입 표면)·BP-13에 scaffold-binding.md §4(Install Manifest 직렬화) 반영.
- **§3:** Conformance Report(11 §3.2-D 6필드) — adapter=**claude** · verdict=**Valid(Full)** · missing_bindings=**없음**(C1 필수 13 전건 실현) · core_modifications=**없음**(C2 v0.3~v0.8 CP2 Core 무변경 + 본 작성 실측) · loop_pass=**예**(C3 v0.2~v0.8 핵심 루프 반복 통과·검증 리포트 6건) · notes=선택 4종 전건 제공 → **완전 Adapter**. 최종 승인 아님(CP2/CP3 후속).
- **§4:** 정식화 배정표 — agent-binding.md(BP-7~11, T3)·harness-binding.md(13 §4.1 조합, T3)·scaffold-binding.md·scaffold-template/(12 §4.1, T4)·.claude/commands/uahf-status.md(Presentation·BP-6 확장, T5). **전건 이행·실재(2026-07-06, r2 재실측)**·각 실물 § 포인터 병기·격리 갱신 T15 이행 완료(L-06), 배정 대상 계약 표면 재정의 0(07 R2).
- **§5:** Advisor 결정 기록 2건(Worker는 기록만) — DP-A2(`adapters/claude/` = `framework/adapters/claude/` 축약 해소, 물리 정본 01 §4.1·structure.md §2·runtime-binding.md §5, Frozen 11 무변경) · DP-A3(`framework/scaffold/` 미신설, 01 §4.1 Module 구현 디렉터리 5종 고정 열거 보존·12 §5 Scaffold=Bootstrap 이전 설치 도구·v0.8 DP-E1 동형).
- **§6:** 상태 서술 실측 대조(r2: 2026-07-06 직접 재실측) — 자매 바인딩 문서·.claude/ 4역할+규약 2문서·model 지정·memory-data/·loop-data/ 9파일·검증 리포트 6건·core/·runtime/ 실재; **§4 배정 대상 4종(agent/harness/scaffold-binding·scaffold-template/ 13파일·`.claude/commands/uahf-status.md`) 실재로 전환 반영**; `.claude/settings.json`·`framework/scaffold/` 부재; specs 15. 실측 불일치 0건(A5/L-07 재발 방지).
- specs/11 §3 계약 재정의·확장 0 · 새 BP·새 필드·새 verdict 값 창설 0 · Frozen specs 계수 15(DP-U3(c)) · Glossary 밖 새 용어 0. 구체 AI·환경·형식 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 형제 Task 불인용(07 R2). 이 1파일만 생성(07 R4).
