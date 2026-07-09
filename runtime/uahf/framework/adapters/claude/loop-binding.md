# framework/adapters/claude/loop-binding — Claude Code Loop Adapter 바인딩

작성일: 2026-07-06
상태: v0.7 Baseline (개정 — §2 행 2 정본 인용 탈락어 복원·loop-data 시연 후 실재 상태 전수 반영(관찰 2·4 해소) · 사용자 승인 2026-07-06). 직전 기준선: v0.6 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/03-loop.md §4.1 — Claude Code Binding 표(7행). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/03-loop.md §4.2 — 이식 교체 지점 SP-1~SP-5. 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/03-loop.md §3.1·§3.1-A·§3.1-B·§3.1-C·§3.1-D·§3.2·§3.3 — 사이클 구동 연산·단계 전이 규칙·재작업 루프·종료 규칙·사람 개입 지점·데이터 포맷·불변 규칙. 본 문서가 준수·대조하는 계약. 재정의하지 않고 § 포인터로만 인용한다.
- specs/03-loop.md §3.2-A — 전이 이벤트(Transition Event) 10필드 스키마와 append-only 불변. 본 문서 §3이 직렬화하는 대상 계약(재정의 0).
- specs/03-loop.md §5 — Memory 접근(Consult 회수·Memory Update 기록, 단일 Port 경유, INV-7). 본 문서 §5가 물리 실현 참조하는 접근 경로.
- framework/loop/loop-state-record.md (W1 확정본) — 전이 이벤트 스키마 인스턴스(§2)·회수 이력 기록 방식(§6 DP-L5, Consult `ref`)·직렬화·저장 위치를 Adapter Binding 소관으로 위임(§7). 본 문서 §3이 그 물리 실현 정본. 정본은 03 §3.2.
- framework/loop/module-manifest.md (W1 확정본) — Loop Provider Module 등록 서술자(`id`=`loop-provider`·`contract`=`LoopInterface`·`requires`=`MemoryServiceInterface`·`entrypoint` 추상 참조). `entrypoint`·`requires` 물리 해소를 Adapter Binding 소관으로 위임(§4). 본 문서 §4가 그 물리 해소.
- framework/loop/stage-transition-rules.md (W2 확정본) — 03 §3.1-A 단계 전이 규칙 인스턴스. 전이 기록 의무(§4). § 포인터로만 참조(재정의 0).
- framework/loop/loop-protocol.md (W2 확정본) — 사이클 구동 연산 오케스트레이션 인스턴스. 재작업 지시 라우팅(§5.1)·Verify 트리거(§5.2)·Memory 접근 시점(§5.3)·종료/사람 개입(§5.4)의 물리 채널을 Adapter Binding 소관으로 위임. 본 문서 §4·§5가 그 물리 채널.
- framework/adapters/claude/memory-binding.md (v0.4 Baseline) — 자매 Adapter Binding 문서(관례 정본). 격리 지점 방향 반전(§0)·7행 물리 실현 표 관례(§2)·1:1 절차 대응(§3)·실측 대조 표 관례(§7)·M5 draft 시점 "데이터 미생성, 시연 시 생성 예정" 관례. **Memory 백엔드(`framework/adapters/claude/memory-data/`)의 물리 실현 정본** — 본 문서 §5(Memory 접근 행)는 그 백엔드 경유를 참조만 하고 재정의하지 않는다.
- framework/adapters/claude/runtime-binding.md (v0.3 Baseline) — 자매 Adapter Binding. §2 #10 세션/턴 수명주기 컨테이너·§3.2 Register/Resolve 수행 방식·§3.3 Config 스코프 물리 소스(`~/.claude/`·`.claude/`)와 `retry.limit` Global 소스·§3.4 Bootstrap~Serve~Shutdown 매핑의 선행 관례.
- framework/adapters/claude/verifier-binding.md (v0.5 Baseline) — 자매 Adapter Binding. §2·§3.1 Agent Module = 서브에이전트 디스패치(Register/Resolve) 관례·§7 실측 대조 관례·형태 A/B 정직 구분.
- framework/core/config-schema.md §7 — 재시도 한도 추상 키 `retry.limit`(기본값 2·Global 스코프 기본 + Project/Module override)의 **값·스코프 소유 소재**. 본 문서는 값을 재선언하지 않고 소유 포인터 + 물리 소스만 바인딩한다.
- framework/core/structure.md §2·§8 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·§8 트리(`framework/adapters/<adapter>/` 이하 바인딩 문서·백엔드 격리 데이터 소관 포인터). 본 문서 경계의 근거.
- specs/01-runtime.md §3.1-C·§3.2-B·§4 — Serve 구간·Config 병합 규칙·Adapter Binding(Provider 등록·물리 진입점 해소). § 포인터로만 참조.
- docs/delegation-protocol.md §3 — 이 프로젝트의 물리 채널 바인딩 관행(위임 = 서브에이전트 디스패치 §3.1, 보고 = 최종 응답 §3.2, 반환·에스컬레이션 = 최종 응답 §3.4). 물리 채널 서술의 관행 근거.
- .claude/agents/ 4종(advisor.md·planner.md·verifier.md·worker.md) — 역할 실행(CP1~CP3)의 물리 실체(실측). 본 문서는 참조만 하고 수정하지 않는다.
- specs/00-glossary.md — 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- docs/session-handoff-v0.3.md §1.4·§1.5(A5·L-07 — 상태 서술은 실측 후 기록) 및 Active Lesson L-09(기록 timestamp = 순서 값, 시각 주장은 실측 대조 후에만). 본 문서 §3.3·§7의 근거.
- ROADMAP.md v0.6 (Loop Engine) — 산출물 "루프 상태 기록 포맷·단계 전이 규칙·재작업 루프·Learn 트리거"의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 03 §3.3 INV-9, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·memory-binding.md §0·verifier-binding.md §0과 동형). 단 이 문서는 Core Contract(03 §3)와 그 인스턴스 문서(framework/loop/ 4문서)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.6 Draft | 최초 작성. `framework/adapters/claude/` 경계의 네 번째 산출물(선행: runtime-binding.md·memory-binding.md·verifier-binding.md). 03 §4.1 바인딩 표 **7행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정)/데이터 미생성(loop-data/) 정직 구분(§2). 루프 상태 기록 물리 백엔드 정본 확정(§3, DP-L4 — 위치 `framework/adapters/claude/loop-data/`, 사이클당 파일 1개·1 line = 1 전이 이벤트 append-log 구조 제안·근거, 03 §3.2-A 10필드 직렬화·append-only·seq/at 순서·"기록만으로 사이클 재구성" 물리 보장, `at` 순서 값 물리 표현(L-09)·`ref` 회수 집합 참조(DP-L5) 물리 표현). Loop Provider `entrypoint`·`requires` 물리 해소(형태 A/B) + 재시도 한도 Config 물리 소스(runtime-binding §3.3 동형, `retry.limit` 값·스코프는 config-schema.md §7 소유 참조)(§4). 역할 실행(CP1=Worker·CP2=Verifier·CP3=Advisor)·전이 유발·사람 개입 물리 채널(서브에이전트 위임·최종 응답·에스컬레이션) + Memory 접근 물리 실현(memory-binding.md 백엔드 경유 참조, 재정의 0)(§5). 03 §4.2 이식 교체 지점 SP-1~5 대응 표("교체되는 것/유지되는 것" — C-1 이식 불변 재확인, §6). 상태 서술 실측 대조 표(§7 — 실재 서술 전건 파일 시스템 실측 후 기입, L-07; loop-data/ 미생성·시연 Task 생성 예정, L-07). 03 §3·framework/loop/ 4문서 계약 재정의·창설 0, 새 바인딩 계약 0, Glossary 밖 새 용어 0. 동시 작성 시연 절차서(후속 W4 L9)·시연(W5 L10) 내용 불인용(07 R2), 미래 산출물(loop-data/ 데이터) 실재 불주장(L-07). 이 1파일만 생성 — framework/loop/ 4문서·.claude/agents/ 4종·기존 Baseline 산출물·specs/·docs/ 무수정. | Worker (Advisor 위임, Task L8) |
| 2026-07-06 | v0.6 Baseline | v0.6 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.7 Draft (개정) | 관찰 2·4 해소 (WF13). **(1) 개정 ① (관찰 2)** — §2 바인딩 표 행 2 정본 인용 셀에서 03 §4.1 원문 대비 탈락한 단어 **"지정"** 복원(specs/03-loop.md §4.1 원문과 문자 단위 대조 후 — "…(Opus 등) 지정은 02 §4 소관…"). **(2) 개정 ② (관찰 4)** — loop-data/ 상태 서술 **전수 갱신**: L8 draft 시점 "미생성/미존재/생성 예정" 서술(§0·§1·§2 표 행 4·행 4 주·§7 실측 대조 표·§8·§10 — `grep`으로 "미생성"·"미존재"·"생성 예정"·"loop-data" 전수 열거)을, 시연 Task(L10, docs/v0.6-demo.md)가 이 정본 구조대로 생성한 **실측 실재**(3파일 — `v06-demo-a.jsonl` 7 line·`v06-demo-b.jsonl` 9 line·`v06-demo-c.jsonl` 11 line, 본 개정 시 `ls`+`wc -l`+`grep -c cycle_id` 직접 재실측)로 갱신(memory-binding.md r2가 M5 draft "미생성"을 M7 시연 후 실재로 전수 갱신한 관례 동형). §3 물리 백엔드 정본·§4·§5·§6 계약 서술 무변경, 03 §3·framework/loop/ 4문서 계약 재정의 0. **비차단 관찰(Advisor 판단 대상 — 완료 보고 open_questions 에스컬레이션):** 문자 단위 대조 결과 정본 인용 열 행 1·2·3·5·7이 원문의 참조 앞 공백(" (NN §X)")을 house-style로 정규화해 byte 단위 불일치(탈자 아님) — 공백 복원은 "지정" 탈락어 복원 범위 밖이라 본 개정은 미수행. 근거: docs/v0.6-verification-report.md §3.7 관찰 2·4 해소 (v0.7 편입 개정, 사용자 승인 2026-07-06). | Worker (Advisor 위임, Task WF13) |
| 2026-07-06 | v0.7 Baseline | v0.7 개정분(관찰 2·4 해소·상태 라인 정합·이력 라벨 일관화) 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/03-loop.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)와 framework/loop/ 4문서(loop-state-record.md·module-manifest.md·stage-transition-rules.md·loop-protocol.md)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·필드·전이 이벤트 스키마·단계 전이 규칙)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. framework/loop/ 4문서가 "물리 직렬화·저장 위치·물리 경로·물리 진입점 해소·물리 채널은 Adapter Binding 문서 소관"이라며 미룬 **직렬화 형식·파일 구조·저장 위치·`at`/`ref` 물리 표현·진입점 물리 해소·역할 실행·사람 개입 물리 채널**이 실재하는(확정되는) 유일한 자리다(loop-state-record.md §0·§7, module-manifest.md §4, stage-transition-rules.md §4, loop-protocol.md §5·§7, 03 §4.1).
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리(`framework/loop/` 등) 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 03 §3.3 INV-9). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형식명, 물리 경로 `framework/adapters/claude/…`·`.claude/…`·`~/.claude/…`, 파일 확장자, 세션/턴, 서브에이전트 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(runtime-binding.md §0·memory-binding.md §0·verifier-binding.md §0과 동형).
- **루프 상태 기록 물리 백엔드 위치 정본 선언(done 2 — Advisor 결정 DP-L4).** 루프 상태 기록의 물리 데이터 위치는 **Adapter 경계 이하 `framework/adapters/claude/loop-data/`로 확정한다**(Advisor 결정 DP-L4 — 물리 백엔드는 Adapter 경계 이하; memory-binding.md §0 memory-data/ 선언 동형). 이 위치는 Core 경계(`framework/core/`·`framework/runtime/`·`framework/loop/` 등)·`specs/`·`docs/` **밖**이다. **정확한 하위 경로·파일 구조·직렬화 형식·`at`/`ref` 물리 표현의 정본은 이 문서(§3)다.** framework/loop/ 4문서는 이 물리 위치를 "Adapter Binding 문서 소관" 포인터로만 미뤘고(loop-state-record.md §7·03 §4.1 SP-3), 본 문서가 그 소유자로서 확정한다.
- **창설 금지.** 이 문서는 03 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.6 산출물(루프 상태 기록 포맷·단계 전이 규칙·재작업 루프·Learn 트리거)의 물리 실현 매핑으로 한정한다. 새 단계·새 전이·새 전이 이벤트 필드·새 개입 조건·새 불변 규칙을 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, runtime-binding.md §0, delegation-protocol.md §0). Loop는 정식 실행 Module이 아니라 규약 문서(03·framework/loop/ 4문서)와 관행(Advisor가 사이클을 오케스트레이션, 서브에이전트 위임·최종 응답으로 역할 실행)으로 실현된다(형태 A — loop-protocol.md §6 DP-L3). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(자매 바인딩 3문서·framework/loop/ 4문서·.claude/agents/ 4종 — §7 실측)과, **시연 Task(L10)가 이 정본 구조대로 생성해 현재 실재하는 데이터**(loop-data/ — §7 재실측), **실행 코드 도입 시 로딩될 지점**(형태 B — 사이클 구동 연산 실행 진입점·로더)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(done 4, L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(session-handoff-v0.3.md §1.4 A5 사례·§1.5 Lesson 후보 3 재발 방지, Active Lesson L-07). §2 "실재 여부" 열과 §7 실측 대조 표의 전 행은 파일 시스템 직접 실측에 근거한다 — 미존재를 실재로 쓰지 않고, 실재는 실측 후에만 기입한다. loop-data/는 **시연 Task(L10)가 이 정본 구조대로 생성해 현재 실재**한다(본 개정 시 §7 재실측 — memory-binding.md §7이 M5 draft 시점 "데이터 미생성"을 M7 시연 후 실재로 전환한 관례 동형).
- 용어는 specs/00-glossary.md 정본만 사용한다. 루프 상태 기록·단계 전이·재작업 루프는 Glossary §3.2-J(J-03) 정본이며, `LoopInterface`·`loop-provider`는 module-manifest.md가 확정한 `contract`·`id` 필드 **값**이지 Glossary 표제어의 신설이 아니다. `형태 A/B`는 structure.md 서술 라벨의 인용이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 03 §4.1(Loop Claude Code Binding)을 이 환경 위에 **v0.6 시점의 구체 물리 실현**으로 매핑한다.

책임은 다섯 가지다.

- 03 §4.1 바인딩 표의 **7행 전부**를 물리 표면(세션/턴 호스팅·서브에이전트 역할 실행·위임/보고 채널·루프 상태 기록 직렬화·재시도 한도 Config·사람 개입 채널·Memory 접근)으로 확정하고, Bootstrap 상태에서의 물리 실재(loop-data/ 데이터 포함 — 시연 Task L10 생성)/규약 실현(형태 A)/형태 B 예정을 "실재 여부" 열로 정직하게 구분한다(§2, done 1·4).
- 루프 상태 기록의 **물리 백엔드 정본**을 확정한다(§3, done 2 — DP-L4) — 위치 `framework/adapters/claude/loop-data/`, 사이클당 파일 1개·1 line = 1 전이 이벤트 append-log 구조(제안·근거), 03 §3.2-A 10필드 직렬화·append-only·seq/at 순서·"기록만으로 사이클 재구성"의 물리 보장, `at`(순서 값 — L-09)·`ref`(회수 집합 참조 — DP-L5) 물리 표현.
- Loop Provider Module의 `entrypoint`·`requires` 추상 참조의 **물리 해소 지점**(형태 A 규약 실현 / 형태 B 실행 코드)과 재시도 한도 Config의 **물리 소스**를 명시한다(§4, runtime-binding.md 교체 지점 관례 동형, done 1 상세).
- 역할 실행(CP1~CP3)·전이 유발·사람 개입의 **물리 채널**(서브에이전트 위임·최종 응답·에스컬레이션)과 Memory 접근의 **물리 실현**(memory-binding.md 백엔드 경유)을 확정한다(§5, done 1 상세).
- 03 §4.2 이식 교체 지점 SP-1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§6, done 3). 그리고 상태 서술을 실측과 대조한다(§7, done 4).

이 문서는 03 §3·framework/loop/ 4문서의 어떤 계약 요소도 재정의·확장하지 않는다(§0, done 5). 형태 A → 형태 B 전환 시에도 Core Contract(03 §3) 변경은 0이며(structure.md §7 C-1), 이 문서(§6의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 03 §4.1 바인딩 표 7행 물리 실현 (done 1·4)

03 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. 아래 표의 "03 §4.1 바인딩" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·구조·형식·채널·절차를, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재(loop-data/ 데이터 포함 — 시연 Task L10 생성)/규약 실현(형태 A)/형태 B 예정을 정직하게 구분한다(§7 실측 대조). "실재" 서술은 전건 파일 시스템 실측 후 기입했다(L-07).

물리 백엔드 디렉터리 구조(본 문서 정본 — DP-L4; 데이터 실재 — 시연 Task L10 생성, §7 재실측):

```
framework/adapters/claude/
├─ runtime-binding.md          # 실재 (v0.3 Baseline)
├─ memory-binding.md           # 실재 (v0.4 Baseline)
├─ verifier-binding.md         # 실재 (v0.5 Baseline)
├─ loop-binding.md             # 실재 (본 문서)
├─ memory-data/                # 실재 — Memory 백엔드 (memory-binding.md 소관)
└─ loop-data/                  # ★ 루프 상태 기록 백엔드 격리 루트 — 실재 (시연 Task L10 생성 — 3파일, §7 재실측)
   └─ <cycle_id>.jsonl         #   사이클당 파일 1개 = 전이 이벤트 append-log (1 line = 1 전이 이벤트; §3)
```

| # | §3 계약 요소 (정본 §) | 03 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Loop 호스팅 (Serve 구간, 03 §3.1·§2) | Claude Code 세션/턴이 Runtime의 Bootstrap~Serve~Shutdown 구간을 호스팅한다(01 §4.1). Loop는 이 Serve 구간에서 구동된다. | Loop 사이클 구동 연산(03 §3.1)은 Claude Code **세션/턴**을 실행 컨테이너로 삼아 **Serve 구간(01 §3.1-C = 턴 진행)**에서 구동된다(runtime-binding.md §2 #10·§3.4 동형). Loop는 이 구간을 **소비만** 하고 Bootstrap/Shutdown을 재정의하지 않는다(03 INV-8). Loop Provider Module `entrypoint`의 물리 해소는 §4.1. | 세션/턴 컨테이너 실재(현 세션이 그 컨테이너). 사이클 구동 실행 진입점(형태 B)은 미도입. |
| 2 | 역할 실행 (CP1/CP2/CP3, 03 §3.1-A) | 각 역할은 `.claude/agents/*.md` 서브에이전트로 실행된다(02 §4.1). CP1=Worker, CP2=Verifier, CP3=Advisor. Worker 기본 실행 모델(Opus 등) 지정은 02 §4 소관이며 이 spec은 참조만 한다. | 검증 게이트 세 체크포인트의 역할이 `.claude/agents/` 서브에이전트로 실행된다 — **CP1=Worker**(`worker.md`, 실측 `model: opus`)·**CP2=Verifier**(`verifier.md`, 실측 실행 모델 미지정=세션 상속)·**CP3=Advisor**(`advisor.md`, 주 세션 바인딩). Planner(`planner.md`)는 Plan 초안 역할. 활성화 = 서브에이전트 위임 시 정의 파일 로딩(Resolve — verifier-binding.md §3.1 Agent Module 동형, §5.1). 실행 모델 지정 의미는 02 §4 소관 — 참조만(§5.1). | `.claude/agents/` 4종 정의 파일 실재(§7 실측). 무인 자동 역할 구동(형태 B)은 미도입. |
| 3 | 단계 전이 유발 (03 §3.1-A) | 위임·보고는 서브에이전트 위임과 최종 응답으로 흐른다(02 §4.1). | 전이를 유발하는 위임·보고가 **서브에이전트 위임**(위임 메시지 02 §3.2-B, delegation-protocol.md §3.1)·**최종 응답**(완료/실패 보고 02 §3.2-C/D, delegation-protocol.md §3.2)으로 흐른다. 재작업 지시(loop-protocol.md §5.1) 라우팅 = 재위임 메시지. 각 전이는 §3의 루프 상태 기록에 남는다(03 INV-3). 물리 채널 상세는 §5.1. | 위임·최종 응답 채널 규약 실현(형태 A, Bootstrap). 무인 자동 트리거(형태 B)는 미도입. |
| 4 | 루프 상태 기록 직렬화 (03 §3.2-A) | §3.2-A 추상 스키마를 파일 기반 기록(구조화 로그/마크다운 등)으로 직렬화한다. 구체 경로·문법은 이 바인딩이 정한다. | `framework/adapters/claude/loop-data/<cycle_id>.jsonl` — 사이클당 파일 1개, 1 line = 1 전이 이벤트(append-only). 전이 이벤트 10필드(03 §3.2-A)를 각 line에 직렬화한다. 물리 구조·형식·경로·`at`/`ref` 물리 표현의 정본은 §3(DP-L4). | 형식·경로 구조 확정(정본, §3). 데이터 실재 — 시연 Task(L10)가 이 정본대로 생성(§7 재실측: 3파일 — v06-demo-a/b/c.jsonl 각 7/9/11 line). |
| 5 | 재시도 한도 Config (03 §3.1-B) | 재시도 한도 값은 effective config(01 §3.2-B)로 주어진다. v0.x에서 `.claude/CLAUDE.md`·설정 파일이 Project scope Config를 제공한다(01 §4.1). | 재시도 한도 추상 키 `retry.limit`(값 2·기본 스코프 Global)의 **값·스코프 소유는 framework/core/config-schema.md §7**이며, 물리 소스는 Config 스코프별 소스(runtime-binding.md §3.3 동형): Global 기본값 소속 = `~/.claude/settings.json`, Project override = `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`, Module scope = 형태 B. Loop는 이 값의 **소비자**일 뿐 소유자가 아니다(module-manifest.md DP-L2). 물리 소스 상세는 §4.2. | Config 물리 소스 실재(`~/.claude/settings.json`·`.claude/` 실재 소스). effective config 로딩(형태 B)은 미도입 — 값은 config-schema.md §7 결정 기록으로 실현(형태 A). |
| 6 | 사람 개입 채널 (03 §3.1-D) | §3.1-D 사람 승인 요청은 Claude Code 세션에서 사용자에게 제시된다. `.claude/CLAUDE.md`의 "Architecture와 Spec 충돌 시 사용자 보고"가 조건 4의 바인딩이다. | 사람 승인 요청(에스컬레이션 산출 — 사람 승인 요청 및/또는 실패 보고 02 §3.2-D)이 **주 세션**(Advisor 바인딩, `.claude/CLAUDE.md`)에서 **사용자에게 제시**된다(delegation-protocol.md §3.4 반환·에스컬레이션 물리 채널). `.claude/CLAUDE.md`의 "Architecture와 Spec 충돌 시 사용자 보고"가 03 §3.1-D 조건 4의 바인딩이다(실측 — §7). `actor` = human 전이는 §3의 루프 상태 기록에 남는다. 물리 채널 상세는 §5.2. | 세션 제시 채널 규약 실현(형태 A). `.claude/CLAUDE.md` 조건 4 바인딩 실재(§7 실측). 무인 개입 트리거(형태 B)는 미도입. |
| 7 | Memory 접근 (03 §5) | Memory Update의 단일 Port 경유는 Runtime이 배선한 Memory Service Interface Module을 Resolve하여 실현한다(01 §5, 02 §4). | Loop의 Memory 접근(Consult 회수·Memory Update 기록, 03 §5·INV-7)은 **memory-binding.md가 확정한 백엔드**(`framework/adapters/claude/memory-data/`)를 단일 Port(memory-service.md §7) 경유로 실현한다. Loop는 소비자이며(memory-service.md §7), 본 문서는 그 물리 실현을 **참조만** 하고 재정의하지 않는다(재정의 0). 접근 시점·회수 집합 기록은 §5.3. | Memory 백엔드(memory-data/) 실재(memory-binding.md §7 실측). 단일 Port 경유 규약 실현(형태 A). |

주:

- 위 7행은 03 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 03 §4.1 정본 표현을 이 환경의 구체 경로·형식·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **물리 실재 / 형태 A / 형태 B 구분(정직).** 행 1(세션/턴)·행 2(진입점 4파일)·행 5·6(Config·`.claude/CLAUDE.md` 소스)·행 7(memory-data 백엔드)의 실재 표면은 물리 실재다. 행 3(전이 유발)·행 6(사람 개입 제시)은 Bootstrap에서 **규약 실현(형태 A)**이다 — 서브에이전트 위임·최종 응답·에스컬레이션으로 수행되며, 무인 자동 실행 채널은 형태 B다(loop-protocol.md §6 DP-L3). 행 4(루프 상태 기록)는 구조·형식·경로가 정본으로 확정되고 **데이터(loop-data/)는 시연 Task(L10)가 이 정본대로 생성해 현재 실재**한다(§7 재실측 — memory-binding.md §7이 M5 draft 미생성을 M7 시연 후 실재로 전환한 관례 동형).
- **역할 실행 = Agent Module(서브에이전트 채널).** CP1~CP3 역할은 서브에이전트로 디스패치되는 Agent Module이므로(verifier-binding.md §3.1 동형), 위임·보고·재작업 지시 전달이 **서브에이전트 위임/최종 응답 채널**로 실현된다. 이는 단일 Port로 소비되는 Cross-cutting Service(Memory, 행 7)의 Port 소비 경로와 다른 실현 방식이다(§5.1·§5.3).
- **데이터 실재 · 생성 주체 구분(L-07).** loop-data/의 데이터(사이클 기록 파일)는 시연 Task(L10)가 이 정본 구조대로 생성해 현재 **실재**한다(§7 재실측). 행 4의 정본성은 구조·형식·경로·`at`/`ref` 물리 표현 **관례**에 대한 것이며, 실제 데이터는 시연 Task(W4 시연 절차서 L9·W5 시연 L10)가 생성했다 — 본 문서(L8)는 그 데이터를 생성하지 않고 구조·형식 정본만 소유한다(생성 주체 구분, L-07).

---

## §3. 루프 상태 기록 물리 백엔드 정본 확정 (done 2 — DP-L4)

loop-state-record.md가 "루프 상태 기록의 직렬화 형식·저장 위치·물리 경로·`at`/`seq`/회수 집합 참조의 물리 표현·append-only의 물리 실현은 전부 Adapter Binding 문서 소관"(loop-state-record.md §7, 03 §4.1·§4.2 SP-3)으로 미룬 지점을 확정한다. **이 문서는 Adapter 경계이므로 구체 직렬화 형식·물리 경로 토큰의 사용이 허용된다(§0 격리 지점).** 계약 요소(전이 이벤트 10필드·의미·필수 표기·append-only 불변·회수 이력 기록 위치)의 정본은 loop-state-record.md §2~§6·03 §3.2-A이며, 본 절은 그 물리 실현만 확정한다(재정의 0).

### §3.1 물리 백엔드 위치·디렉터리 구조 (DP-L4 + 구조 제안·근거)

- **물리 위치 정본(Advisor 결정 DP-L4).** 루프 상태 기록의 물리 데이터 위치는 `framework/adapters/claude/loop-data/`로 확정한다 — Adapter 경계 이하 격리(memory-binding.md §0 memory-data/ 선언 동형). Core 경계·`specs/`·`docs/` 밖이다. 소비자(Advisor·Worker·Verifier 역할, Loop 오케스트레이션)는 이 경로·형식을 직접 참조하지 않으며, 루프 상태 기록은 이 백엔드로 격리된다(03 §4.2 SP-3).
- **구조 제안(Worker 제안 — DP-L4 위치 내 하위 구조).** 각 사이클의 전이 로그를 **사이클당 파일 1개**로 두고, 그 파일을 **1 line = 1 전이 이벤트의 append-log**로 직렬화한다: `loop-data/<cycle_id>.jsonl`. 파일명 = 전이 이벤트 `cycle_id`(03 §3.2-A — "하나의 위임 = 하나의 사이클"), 각 line = 그 사이클의 전이 이벤트 1건.
- **제안 근거.**
  - **(a) 재구성 단위와의 정합(03 §7).** 03 §3.2-A·§7은 "이 로그만으로 **사이클 전체를 재구성·검증할 수 있어야 한다"고 규정한다. 재구성의 단위는 **사이클**이며(cycle_id로 식별), 사이클당 파일 1개는 그 재구성을 **파일 1개 판독으로 자기완결**시킨다 — 한 사이클의 단계 경로·재작업 되돌림·에스컬레이션·회수 참조가 그 파일 안에 모두 있다. 이는 memory-data/가 교차 사이클 전역 로그(index.jsonl 1개)를 쓰는 것과 사실 관계가 다르다 — Memory Index의 조회 단위는 scope(교차 사이클)이나, 루프 상태 기록의 재구성 단위는 단일 사이클이다.
  - **(b) append-only의 물리 실현(03 INV-3).** 1 line = 1 전이 이벤트 append-log는 append-only 불변(loop-state-record.md §5·03 INV-3 — "기록된 뒤에 유효하다, 기록되지 않은 전이는 없다")을 **파일 끝 line 추가**로 물리 실현한다. 기존 line은 재작성·삭제하지 않는다 — 갱신·정정은 기존 line을 바꾸지 않고 **새 전이 이벤트 line을 추가**한다(loop-state-record.md §5). 이는 memory-data/ index.jsonl의 line-per-entry append-log 관례(memory-binding.md §2 #4)와 동형이다.
  - **(c) 순서 확정(03 §3.2-A).** append 순서(파일 내 line 순서)가 사이클 내 전이 순서와 정합한다 — `seq` 단조 증가(03 §3.2-A)와 `at` 순서 값(§3.3)이 line 순서를 확정한다. 재작업 되돌림(03 §3.1-B, `outcome` = fail·`retry_count` 증가)과 에스컬레이션(`outcome` = escalated·`actor` = human)도 각각 하나의 line으로 append된다(loop-state-record.md §5, 03 §3.2-A 불변).
- **직렬화 형식 = Adapter 선택.** line 구분 로그(JSON Lines)를 사이클 기록에, 각 line 안의 전이 이벤트를 자기서술적 데이터 형식(JSON 객체)으로 직렬화한다. 이 형식 선택은 03 §4.2 SP-3의 교체 지점이며, 이식 시 대상 환경 로깅 메커니즘으로 교체된다(§6). 규모 대응(파일 회전·샤딩 등)은 형태 B/규모 사안으로 미룬다(추측·선취 금지 — structure.md §4 규칙 4 defer).

### §3.2 전이 이벤트 10필드 직렬화 · append-only · 재구성 보장 (정본: 03 §3.2-A / loop-state-record.md §2·§5)

각 line은 전이 이벤트 10필드(loop-state-record.md §2, 정본 03 §3.2-A)를 JSON 객체로 직렬화한다. **필드명·의미·필수 표기의 정본은 loop-state-record.md §2·03 §3.2-A이며, 본 표는 그 물리 직렬화 표기만 확정한다**(재정의 0, 새 필드 0).

| 전이 이벤트 필드 (정본 loop-state-record.md §2 / 03 §3.2-A) | 필수 | 물리 직렬화 (이 Adapter 확정 — line 내 JSON 필드) |
|---|---|---|
| `cycle_id` | 예 | 문자열 — 파일명 `<cycle_id>`와 동일 값(사이클당 파일 1개이므로 파일명이 그 자체로 사이클 식별 매체). |
| `seq` | 예 | 사이클 내 단조 증가 정수. append 순서(line 순서)와 정합. |
| `from_stage` | 아니오 | 문자열(단계 명칭). 사이클 시작 전이(첫 line)에는 생략(정본 "사이클 시작 시 없음"). |
| `to_stage` | 예 | 문자열(단계 명칭 — Consult/Plan/Execute/Verify/Learn/Memory Update/Complete). |
| `trigger` | 예 | 문자열 — 정본 열거(완료 조건 충족 / Verify 실패 / 재작업 되돌림 / 에스컬레이션) 값. |
| `outcome` | 예 | 문자열 — 정본 열거(pass / fail / escalated) 값. |
| `retry_count` | 예 | 비음의 정수 — 현재까지 재작업 되돌림 횟수(03 §3.1-B). |
| `actor` | 예 | 문자열 — 정본 열거(Advisor/Planner/Worker/Verifier/human) 값. |
| `ref` | 아니오 | 참조 값 — 관련 산출물·보고 참조. 물리 표현은 §3.3(회수 집합 참조 포함). 관련 산출물이 없는 전이에서 생략 가능. |
| `at` | 예 | 순서 보장용 값 — 물리 표현은 §3.3(순서 값, L-09). |

- **필수 표기 보존(정본).** 10필드 중 8필드는 필수, 2필드(`from_stage`·`ref`)는 아니오다(loop-state-record.md §2). 직렬화는 이 필수/선택 지위를 바꾸지 않는다 — 필수 필드는 모든 line에 존재하고, 선택 필드는 해당 전이에서 생략 가능하다. 열거 값(`outcome` 3종·`trigger` 4종·`actor` 5종)은 정본이며 재정의·추가하지 않는다.
- **재구성 보장의 물리 실현(03 §7).** 한 사이클 파일의 line 집합은 그 사이클의 단계 경로·재작업 되돌림·에스컬레이션·회수 참조를 복원하기에 충분하다(loop-state-record.md §5) — 각 line의 `from_stage`→`to_stage` 연쇄가 단계 경로를, `outcome`=fail·`retry_count` 증가 line이 재작업 되돌림을, `outcome`=escalated·`actor`=human line이 에스컬레이션을, Consult line의 `ref`(§3.3)가 회수 참조를 복원한다. Verifier는 이 파일을 파싱해 전이 순서·완료 조건 충족·append-only 여부를 확인한다(03 §7 검증 방법, loop-state-record.md §5).
- **정합 대조(검증 지점).** 사이클 파일 내 `seq`의 단조 증가와 line 순서의 일치, 첫 line의 `from_stage` 부재, 각 재작업 line의 `retry_count` 단조 증가가 append-only·순서 확정의 물리 대조 지점이다.

### §3.3 `at`(순서 값 — L-09) · `ref`(회수 집합 참조 — DP-L5) 물리 표현

loop-state-record.md §2·§6이 "`at`의 물리 시각 표현, 회수 집합 참조의 물리 표현은 Adapter Binding 소관"으로 미룬 두 지점을 확정한다.

- **`at` 물리 표현 = 순서 값(L-09 준수).** `at`은 loop-state-record.md §2가 "순서 보장용 **추상 시각**"으로 정의하고 물리 표현을 Adapter Binding에 위임한 필드다. 물리 표현: `at`은 사이클 내에서 **단조 증가하는 순서 값**으로 직렬화한다 — `seq`와 함께 전이 순서를 확정하는 값이며, **물리 벽시계 시각(wall-clock)이 아니다**. Active Lesson **L-09**(기록 timestamp = 순서 값, 물리 생성 시각과 구분; 시각 주장은 실측 대조 후에만) 준수: `at`에 순서 값을 기록하되, 그 값을 **물리 시각으로 주장하지 않는다**. 실제 물리 시각이 필요하면 파일·line의 물리 생성 시각(예: mtime)을 **실측**해 별도로 공개한다(L-09 자체 준수 실증 — session-handoff-v0.5.md §48, memory-data/ timestamp가 순서 값으로 쓰인 것과 동형). 순서 값의 구체 형식(정수 서수·정렬 가능 토큰 등)은 Adapter 선택이며 이식 교체 지점 SP-3에 속한다(§6).
- **`ref` 물리 표현 = 참조 토큰(회수 집합 참조 포함).** `ref`은 "관련 산출물·보고 참조"(loop-state-record.md §2 / 03 §3.2-A)를 담는 선택 필드다. 물리 표현: line 내 JSON 값으로 **참조 토큰**을 담는다 — 위임/완료/실패 보고·Verifier 판정 참조의 경우 그 산출물·보고의 식별 참조(예: 저장소 문서 식별자 또는 보고 식별자)를, **Consult 전이 이벤트의 회수 집합 참조(DP-L5)**의 경우 그 사이클에서 회수된 Memory Item id 집합의 참조(예: memory-data/ store id 스킴 `mi-<정렬가능토큰>`의 배열 — memory-binding.md §2)를 담는다.
  - **회수 집합 참조의 소관 경계(DP-L5).** "Consult 전이 이벤트의 `ref`에 회수 집합 참조를 기록한다"는 **기록 위치**는 loop-state-record.md §6(Advisor 결정 DP-L5)이 소유한다 — 본 절은 그 참조가 line 안에서 어떤 형식으로 직렬화되는가(물리 표현)만 확정한다. 회수 집합의 **내용**(무엇이 회수되었는가)·회수 정책·회수 집합의 **소비**(05 재발 판정의 `was_recalled` 입력)는 03 §5·04·05 소관이며(loop-state-record.md §6), 본 문서는 재서술하지 않는다.
  - **경량 참조(최소 Context).** `ref`은 회수된 Memory Item의 `content` 원문을 담지 않고 그 **id 참조**만 담는다 — 원문이 필요하면 그 id로 Memory 백엔드에서 Recall한다(memory-binding.md §3.2 index-first, 04 INV-4 최소 Context와 정합). 이는 루프 상태 기록이 Memory content를 중복 저장하지 않게 한다.
- **물리 백엔드 격리.** `at`·`ref`의 위 물리 표현은 전부 `framework/adapters/claude/loop-data/` 뒤로 격리된다 — 소비자는 루프 상태 기록을 Loop 오케스트레이션 경유로만 소비하며 이 표현을 직접 참조하지 않는다(03 §4.2 SP-3). 이식 시 §3.2 필드·§3.3 표현은 유지되고 물리 직렬화만 교체된다(03 §4.2, §6).

---

## §4. Loop Provider `entrypoint`·`requires` 물리 해소 · 재시도 한도 Config 물리 소스 (done 1 상세)

module-manifest.md(W1 확정본)가 "`entrypoint`·`requires`의 물리 해소는 Adapter Binding 문서 소관(§4)"으로 미룬 지점과, 03 §4.1 재시도 한도 Config 행의 물리 소스를 확정한다. runtime-binding.md §3.2·§3.3·memory-binding.md §4의 교체 지점 관례(추상 참조 → 물리 실현, 형태 A/B 구분)와 동형으로 서술한다.

### §4.1 `entrypoint`·`requires` 물리 해소

module-manifest.md §2·§4 `entrypoint` = "추상 참조 — 사이클 구동 연산(03 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관". `requires` = `MemoryServiceInterface`. 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Loop Provider Module 활성화 진입 — 사이클 구동 연산(03 §3.1) 노출 | **형태 A(Bootstrap):** 활성화 진입은 규약으로 실현된다 — 사이클 구동 연산은 loop-protocol.md §3의 오케스트레이션 절차(위임 수령 → Consult → … → Complete/에스컬레이션)에 따라 세션/턴(§2 #1)에서 구동되며, 각 단계 역할은 서브에이전트 위임으로 실행된다(§5.1). 별도 실행 진입점 파일은 없다. | 규약 실현(형태 A) |
| 위 진입점의 실행 코드 로케이터 | **형태 B:** 사이클 구동 연산을 사람 없이 자동으로 트리거·반복하는 실행 코드가 non-core 실행 경계(`framework/loop/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지, loop-protocol.md §6 DP-L3). | 형태 B |
| `requires` = `MemoryServiceInterface` 물리 해소 | Loop Provider가 Resolve될 때 함께 해소되어야 하는 Memory Service Interface 계약(01 §3.1-A Resolve 완료 조건)의 물리 실현은 **memory-binding.md가 확정한 백엔드**(`framework/adapters/claude/memory-data/`)이다. Loop의 Memory Update(모든 사이클의 불가피 단계 — 03 INV-5·INV-7)는 이 백엔드를 단일 Port 경유로 소비한다(§5.3). 본 문서는 그 물리 배선을 재정의하지 않고 참조만 한다. | memory-binding.md 소관(참조) |

- **Register/Resolve 정합(verifier-binding.md §3.1 Agent Module 동형).** Loop Provider의 등록(Register)은 Manifest(framework/loop/module-manifest.md) + 본 바인딩 배치로 규약 실현되며(형태 A), 해소(Resolve)는 소비자(03 dependents — Workflow의 다중 사이클 오케스트레이션 등, 03 §2)가 `contract` `LoopInterface`로 사이클 구동을 요청할 때 이 Provider로 해소되는 것이다. 검증 게이트의 역할 실행(CP1~CP3)은 module Resolve가 아니라 서브에이전트 디스패치이며(module-manifest.md §3 `requires` 주 — 역할 실행은 requires에 넣지 않음), 그 물리 채널은 §5.1이다. 이 등록 경로는 이식 교체 지점 SP-1·SP-2에 대응한다(§6).

### §4.2 재시도 한도 Config 물리 소스 — `retry.limit` (config-schema.md §7 소유 참조)

03 §3.1-B은 "재시도 한도 값은 Config로 주어진다. Loop는 한도 초과 판정 규칙만 정의한다"고 규정하고, 그 값·스코프 소유는 framework/core/config-schema.md §7이다(module-manifest.md DP-L2 — Loop는 소비자, `configSchema` 생략). 그 물리 소스:

| 관점 | 물리 실현 (claude 환경) | 형태 |
|---|---|---|
| **값·기본값·스코프 소유** | 추상 키 `retry.limit`, 기본값 **2**, 기본 스코프 **Global**(Project/Module override 허용)의 선언은 framework/core/config-schema.md §7이 소유한다(실재 — DP-1 결정 기록). 본 문서는 재선언하지 않는다(값 이중화 방지). | 실재(형태 A 선언, config-schema.md §7) |
| **물리 소스(스코프별)** | runtime-binding.md §3.3 동형: Global 기본값(2) 소속 = `~/.claude/settings.json`(실재), Project override = `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`(실재), Module scope = 형태 B(실행 코드 도입 시 Loop Provider 설정 블록). 병합은 Module > Project > Global(01 §3.2-B, config-schema.md §4.2). | Global/Project 소스 실재, Module 소스는 형태 B |
| **읽히는 지점(read)** | 재작업 루프 구동 시 읽힌다 — 소비 지점은 loop-protocol.md §4(재시도 한도 초과 판정 → 에스컬레이션). Loop는 effective config의 소비자다(01 §3.2-B). | 규약 실현(형태 A) / 형태 B 로더 |
| **적용 방식(apply)** | `retry_count`가 `retry.limit`을 초과하면 에스컬레이션한다(loop-protocol.md §4·03 §3.1-B, §3.1-D 조건 1). 한도 초과 **판정 규칙**은 03 §3.1-B 소관으로 불변이며, 본 문서는 값의 물리 소스·읽힘만 바인딩한다. | 03 §3.1-B 판정 규칙(불변) |

- **형태 구분.** v0.6 Bootstrap에서 이 값은 config-schema.md §7 결정 기록(기본 2·Global)으로 실현(형태 A)되며, 실행 로더(형태 B) 도입 시 effective config(Module > Project > Global 병합)로 로딩되어 재작업 루프가 loop-protocol.md §4로 적용한다. 한도의 **존재·의미**(03 §3.1-B) 계약은 불변이며, 본 문서는 값 원천·읽힘·적용의 물리 지점만 바인딩한다(config-schema.md §7·module-manifest.md DP-L2 재정의 0).

---

## §5. 역할 실행·전이 유발·사람 개입 물리 채널 · Memory 접근 물리 실현 (done 1 상세)

03 §4.1 역할 실행(행 2)·단계 전이 유발(행 3)·사람 개입 채널(행 6)·Memory 접근(행 7)의 물리 채널을 확정한다. loop-protocol.md §5(이연 해소 4건 — 재작업 지시 라우팅·Verify 트리거·Memory 접근 시점·종료/사람 개입)가 "물리 채널·직렬화·물리 실행은 Adapter Binding 문서 소관"(loop-protocol.md §5 서두·§7)으로 미룬 지점의 물리 실현이다.

### §5.1 역할 실행 · 전이 유발 · 재작업 지시 라우팅 물리 채널 (03 §4.1 행 2·3)

- **역할 실행(CP1~CP3) = 서브에이전트 디스패치.** 검증 게이트 세 체크포인트의 역할이 `.claude/agents/` 서브에이전트로 실행된다 — CP1=Worker(`worker.md`), CP2=Verifier(`verifier.md`), CP3=Advisor(`advisor.md`). 활성화 = 서브에이전트 위임 시 정의 파일 로딩(Resolve — verifier-binding.md §3.1 Agent Module 동형). Worker 실행 모델(실측 `model: opus`)·Verifier/Advisor 세션 상속의 **지정 의미**는 02 §4 소관이며 본 문서는 참조만 한다(03 §4.1 "Worker 기본 실행 모델 … 이 spec은 참조만").
- **전이 유발 = 위임·최종 응답.** 단계 전이를 유발하는 위임·보고가 **서브에이전트 위임**(위임 메시지 02 §3.2-B — delegation-protocol.md §3.1)·**최종 응답**(완료 보고 02 §3.2-C / 실패 보고 02 §3.2-D — delegation-protocol.md §3.2)으로 흐른다. 각 전이는 §3의 루프 상태 기록(loop-data/)에 append된다(03 INV-3).
- **재작업 지시 라우팅(loop-protocol.md §5.1 물리 실현).** CP2 판정이 Fail 또는 Conditional이면, 검증 리포트의 재작업 지시(`rework` — 06 §3.2-D, verifier-binding.md §4.2)가 근본 원인별 되돌림 단계(loop-protocol.md §4)의 **재위임 메시지**(02 §3.2-B, delegation-protocol.md §3.1)에 실려 흐른다. 재작업 지시 포맷 정본은 06·rework-instruction.md이며 본 문서는 물리 전달 채널(재위임 서브에이전트 위임)만 바인딩한다(loop-protocol.md §5.1 경계, verifier-binding.md §4.2 동형).
- **Verify 트리거(loop-protocol.md §5.2 물리 실현).** Execute 완료(산출물 + 자체 점검 CP1) 시점에 Loop 오케스트레이션이 CP2 판정을 위한 입력{산출물 + criteria}을 구성해 Verifier 서브에이전트에 위임(구동)한다. 판정 연산의 절차·기준·리포트는 06·verifier-binding.md 소관이며 본 문서는 구동 채널(서브에이전트 위임)만 바인딩한다. 무인 자동 트리거는 형태 B(loop-protocol.md §6 DP-L3).

### §5.2 사람 개입 물리 채널 (03 §4.1 행 6 / §3.1-D)

- **제시 채널.** 사람 승인이 필요한 5조건(03 §3.1-D, loop-protocol.md §5.4) 발생 시, 에스컬레이션 산출(사람 승인 요청 및/또는 실패 보고 02 §3.2-D)이 **주 세션**(Advisor 바인딩 — `.claude/CLAUDE.md`, advisor.md 머리 "주 세션은 기본적으로 Advisor로 동작")에서 **사용자에게 제시**된다. 물리 채널 = 서브에이전트 최종 응답으로 Advisor에게 회수된 뒤 사용자에게 제시(delegation-protocol.md §3.4 반환·에스컬레이션 물리 채널).
- **조건 4 바인딩(실측).** 03 §3.1-D 조건 4(상위 규약·Architecture 충돌)의 이 환경 바인딩은 `.claude/CLAUDE.md`의 "Architecture와 Spec이 충돌하면 Spec을 수정하지 말고 사용자에게 보고한다"이다(03 §4.1 정본 인용, §7 실측 확인). advisor.md 금지 사항 "Architecture와 Spec 충돌 시 … 사용자에게 보고한다(03 §3.1-D 조건 4)"가 이를 역할 정의에서 재확인한다.
- **개입 기록.** 각 사람 개입 발생은 §3의 루프 상태 기록에 `actor` = human 전이(§3.2 표)로 남는다(03 §3.1-D·§3.2-A, loop-protocol.md §5.4). 무인 자동 개입 트리거는 형태 B다(loop-protocol.md §6 DP-L3).

### §5.3 Memory 접근 물리 실현 (03 §4.1 행 7 / §5) — memory-binding.md 백엔드 경유 (재정의 0)

- **접근 경로.** Loop의 Memory 접근(Consult 회수 · Memory Update 기록, 03 §5·INV-7)은 **memory-binding.md가 확정한 백엔드**(`framework/adapters/claude/memory-data/`)를 단일 Port(memory-service.md §7 소비자 계약 — Loop는 소비자) 경유로 실현한다. 물리 저장·직렬화·Record/Recall 물리 절차는 memory-binding.md §2·§3이 소유하며, **본 문서는 그 물리 실현을 재정의하지 않고 참조만 한다**(재정의 0 — done 5).
  - **회수(Recall) 시점 = Consult 구동.** 착수 전 관련 Lessons·이전 결정·컨텍스트를 회수한다(loop-protocol.md §5.3). 회수 절차(purpose·scope 필수, bounded, 전량 로드 금지)의 물리 실현은 memory-binding.md §3.2(index-first)다.
  - **기록(Record) 시점 = Memory Update 구동.** Learn이 도출한 후보(Lesson 후보 / Best Practice 후보, 03 §3.2-C)를 기록한다. 기록 절차(Item 파일 쓰기 + Index line append 정합, INV-7)의 물리 실현은 memory-binding.md §3.1이다.
- **회수 집합 기록의 접속.** Consult 회수 집합의 참조는 §3의 루프 상태 기록 Consult 전이 이벤트 `ref`에 기록된다(loop-state-record.md §6 DP-L5, 물리 표현 §3.3). 이는 loop-data/(루프 상태 기록)와 memory-data/(Memory 백엔드)를 잇는 지점이다 — `ref`은 memory-data/ store id 참조를 담을 뿐, Memory content를 loop-data/에 중복 저장하지 않는다(§3.3 경량 참조).
- **단일 Port 경유(INV-7).** 회수·기록의 모든 접근은 Memory Service Interface(단일 Port) 경유다. 영속성 백엔드에 직접 접근하지 않는다(03 INV-7). 물리 배선은 memory-binding.md 소관이다.

---

## §6. 03 §4.2 이식 교체 지점 SP-1~5 대응 (done 3)

03 §4.2 이식 교체 지점 SP-1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인한다.

| # (03 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Loop 호스트 프로세스 → 대상 환경의 실행 프로세스 | §2 #1, §4.1 | Claude Code 세션/턴 실행 컨테이너, Loop Provider 형태 A 규약 실현·형태 B 실행 코드 로케이터. | 03 §3.1 사이클 구동 연산, Serve 구간 소비 계약(01 §3.1-C), 경계 불가침(03 INV-8). |
| SP-2 | 역할 실행 모델·서브에이전트 위임 → 대상 환경의 Agent 오케스트레이션 | §2 #2·#3, §5.1 | `.claude/agents/` 서브에이전트 디스패치·최종 응답, `worker.md` `model: opus`, 재위임 메시지. | 03 §3.1-A 검증 게이트 CP1/CP2/CP3 역할 구분·단계 전이 규칙(stage-transition-rules.md); 역할 내부 계약 02 §3(02 §4.2 SP-3/SP-4). |
| SP-3 | 루프 상태 기록 직렬화 포맷·저장 위치 → 대상 환경의 로깅 메커니즘 | §2 #4, §3 | `loop-data/<cycle_id>.jsonl` append-log, 10필드 JSON 직렬화, `at` 순서 값·`ref` 참조 물리 표현. | 03 §3.2-A 전이 이벤트 10필드 스키마·append-only 불변·재구성 요건(§7); loop-state-record.md 인스턴스·회수 이력 기록 방식(§6 DP-L5). |
| SP-4 | 재시도 한도 등 Config 소스 → 대상 환경의 Config 메커니즘 | §2 #5, §4.2 | Config 스코프 물리 소스(`~/.claude/settings.json`·`.claude/`), `retry.limit` 물리 소스 배치. | 03 §3.1-B 재작업 루프·한도 초과 판정 규칙; `retry.limit` 값·스코프 소유(config-schema.md §7); 03 §3.2-C Learn 트리거. |
| SP-5 | 사람 승인 채널 → 대상 환경의 사람 개입 메커니즘 | §2 #6, §5.2 | 주 세션 사용자 제시·에스컬레이션 산출 채널, `.claude/CLAUDE.md` 조건 4 바인딩. | 03 §3.1-D 사람 개입 5조건·INV-6(사람 개입 최소); 03 §3.1-C 종료 규칙(종료 전 Learn 불가피 INV-5). |

- **"유지되는 것" 열의 이식 불변성.** 위 계약(03 §3.1-A 단계 전이 규칙·§3.1-B 재작업 루프·§3.1-C 종료 규칙·§3.1-D 사람 개입 조건·§3.2-A 루프 상태 기록 스키마·§3.2-C Learn 트리거)은 다른 AI·환경으로 이식해도 바뀌지 않는다 — 03 §4.2 말미 "유지되는 것" 목록의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다. framework/loop/ 4문서가 그 계약의 인스턴스이며, 이식 시에도 이 인스턴스의 계약 요소는 불변이다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(03 §4.2 말미·runtime-binding.md §4·memory-binding.md §6·verifier-binding.md §6 동형). 본 문서는 그 정식화를 선취하지 않고 v0.6 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 4 — A5/L-07 재발 방지)

session-handoff-v0.3.md §1.4(A5 사례 — 미존재 소스를 "실재"로 서술 → 파일 시스템 전수 대조로 검출)·§1.5 Lesson 후보 3(상태 서술은 실측 후 기록, Active Lesson L-07)에 따라, 본 문서의 "실재/존재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`) + 파일 크기·front-matter 직접 실측. loop-data/ 행은 본 개정(WF13) 시 `ls`+`wc -l`+`grep -c cycle_id`로 직접 재실측했다(L8 draft 미생성 → 시연 Task L10 생성 후 실재).**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — runtime/memory/verifier-binding.md·memory-data/ 존재 확인. |
| `framework/adapters/claude/runtime-binding.md` | 실재 (v0.3 Baseline, 자매) | 실재 (32,973 bytes). |
| `framework/adapters/claude/memory-binding.md` | 실재 (v0.4 Baseline, 자매) | 실재 (51,144 bytes). |
| `framework/adapters/claude/verifier-binding.md` | 실재 (v0.5 Baseline, 자매) | 실재 (46,449 bytes). |
| `framework/adapters/claude/loop-binding.md` | 실재 (본 문서 — 본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음. |
| `.claude/agents/` 4종 (§2 #2 진입점) | 실재 (advisor/planner/verifier/worker.md — 역할 실행 물리 실체) | 실재 — 4파일: advisor.md(7,152)·planner.md(9,232)·verifier.md(11,357)·worker.md(7,134). |
| `.claude/agents/worker.md` 실행 모델 (§2 #2·§5.1) | 실재 `model: opus` (지정 의미는 02 §4 소관) | 실재 — front-matter `model: opus` 확인. |
| advisor/planner/verifier.md 실행 모델 (§5.1) | 세션 상속 (미지정) | 실재 — 세 파일 front-matter `model` 라인 부재 확인(세션 상속). |
| `framework/loop/` 4문서 (W1·W2 확정본 — 계약 인스턴스, § 포인터 대상) | 실재 (loop-state-record·module-manifest·stage-transition-rules·loop-protocol) | 실재 — 4파일: loop-state-record.md(24,976)·module-manifest.md(31,949)·stage-transition-rules.md(26,899)·loop-protocol.md(44,162). 무수정. |
| `framework/adapters/claude/loop-data/` (§2 #4·§3 백엔드 루트) | **실재** (DP-L4 위치 — 시연 Task L10 생성) | **실재** — 3파일: `v06-demo-a.jsonl`(7 line·1,656 bytes)·`v06-demo-b.jsonl`(9 line·2,338 bytes)·`v06-demo-c.jsonl`(11 line·3,087 bytes). 본 개정 시 `ls`+`wc -l`+`grep -c cycle_id` 직접 재실측(L8 draft 미생성 → 실재). |
| `framework/adapters/claude/memory-data/` (§2 #7·§5.3 Memory 백엔드) | 실재 (memory-binding.md 확정 백엔드, 자매) | 실재 — `memory-data/store/`·`memory-data/index/` 존재 확인(memory-binding.md §7 실측 대상). |
| `.claude/CLAUDE.md` 조건 4 바인딩 (§2 #6·§5.2) | 실재 ("Architecture와 Spec 충돌 시 사용자 보고") | 실재 — `.claude/CLAUDE.md` "Architecture와 Spec이 충돌하면 Spec을 수정하지 말고 사용자에게 보고한다" 확인. |
| `retry.limit` 값·스코프 (§4.2) | 실재 (형태 A 선언, config-schema.md §7 — 기본 2·Global) | 실재 — config-schema.md §7 결정 기록(기본값 2·Global 스코프) 확인. |
| Config 물리 소스 (§4.2) | 실재 `~/.claude/settings.json`·`.claude/` (runtime-binding.md §3.3 동형) | 실재(자매 문서 실측 승계) — runtime-binding.md §3.3 소스 목록 참조. |
| 사이클 구동 실행 진입점·실행 로더 (형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). `framework/loop/`는 계약 문서 4건만 실재(실행 코드 0). |

- **핵심 구분.** 본 문서가 확정한 루프 상태 기록의 **경로·파일 구조·직렬화 형식·`at`/`ref` 물리 표현은 정본**(§3)이며, 그 **데이터(loop-data/)는 시연 Task(L10)가 이 정본 구조대로 생성해 현재 실재**한다(§7 재실측). 이는 memory-binding.md의 전환(M5 draft 시점 데이터 미생성 → M7 시연 후 실재)과 동형이다 — loop-binding도 L8 draft 시점엔 미생성이었고 시연 Task(L10) 후 실재로 전환했으며, 본 개정이 그 실재를 반영한다. loop-data/ 데이터의 생성 주체는 **시연 Task**(W4 시연 절차서 L9·W5 시연 L10)이며, 본 문서(L8)는 구조·형식·표기의 정본만 소유한다 — 데이터를 생성·수정하지 않는다.
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다(loop-data/ 실재는 본 개정 시 직접 재실측). 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로 쓰지 않았다(A5/L-07 재발 방지). 순서 값·시각 서술은 L-09 준수(§3.3 — `at` 순서 값, 시각 주장은 실측 후에만).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 5).** 본 문서의 모든 매핑은 03 §3·§4·framework/loop/ 4문서의 물리 실현이다. 어떤 연산·데이터 계약·불변 규칙·전이 이벤트 필드·단계 전이 규칙·개입 조건도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 정본 §(03 §3·loop-state-record.md·module-manifest.md·stage-transition-rules.md·loop-protocol.md)다. 새 바인딩 계약을 03 §4.1 표를 넘어 창설하지 않았고, 새 단계·새 전이·새 필드·새 개입 조건·새 불변 규칙을 추가하지 않았다.
- **계약 소유 명시.** 전이 이벤트 스키마·append-only 불변·회수 이력 기록 방식(DP-L5) = loop-state-record.md/03 §3.2; 단계 전이 규칙·게이트-단계 매핑 = stage-transition-rules.md/03 §3.1-A; 사이클 구동 연산·재작업 루프·종료·사람 개입 오케스트레이션 = loop-protocol.md/03 §3.1; Manifest 필드·`entrypoint`·`requires` = module-manifest.md/01 §3.2-A; `retry.limit` 값·스코프 = config-schema.md §7. Memory 백엔드 물리 실현 = memory-binding.md/04 §4. 본 문서는 이들의 **물리 실현**(루프 상태 기록 직렬화 형식·경로·`at`/`ref` 물리 표현·진입점 물리 해소·역할 실행/전이/사람 개입 물리 채널·Config 물리 소스)만 확정한다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형식(JSON Lines·JSON)·물리 경로(`framework/adapters/claude/loop-data/…`·`.claude/…`·`~/.claude/…`)·파일 확장자·세션/턴·서브에이전트 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. framework/loop/ 4문서(Module 구현 디렉터리 문서 본문)는 이 토큰을 "Adapter Binding 문서 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3 확장은 이 경계에 비적용 — 격리 보유, runtime-binding.md §5·memory-binding.md §8·verifier-binding.md §8 동형).
- **동시 작성 문서 경계(07 R2) 및 데이터 생성 주체 구분(L-07).** 후속 Wave에서 작성될 시연 절차서(W4, L9)·시연(W5, L10)의 내용을 인용·추측하지 않았다(07 R2 준수 — memory-binding.md가 동시 작성 demo-procedure를 불인용한 선례 동형). 시연 절차·픽스처 상세는 서술하지 않았고, L8 draft 시점엔 시연 수행으로 생성될 산출물(loop-data/ 데이터)의 실재를 주장하지 않고 생성 주체를 시연 Task로 구분했다(L-07); 그 데이터는 이후 시연 Task(L10)가 생성해 현재 실재하며(§7 재실측) 본 개정이 이를 반영한다. 참조한 확정 정본은 03(정본)·framework/loop/ 4문서(W1·W2 확정본)·자매 Adapter Binding 3문서·framework/core/config-schema.md·structure.md·.claude/agents/ 4종(진입점 실물)·.claude/CLAUDE.md·docs/delegation-protocol.md·specs/00-glossary.md뿐이다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 이 1개 파일(`framework/adapters/claude/loop-binding.md`)만 생성하며, framework/loop/ 4문서·.claude/agents/ 4종·기존 Baseline 산출물(runtime/memory/verifier-binding.md·memory-data/)·specs/·docs/를 수정·생성하지 않는다. loop-data/ 데이터도 생성하지 않는다(구조·형식 정본만 소유).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-LB-1 (loop-data 하위 구조 = Worker 제안, Advisor 채택 대상 — 비차단).** DP-L4는 물리 **위치**(`framework/adapters/claude/loop-data/`)를 확정했으나, 그 **하위 구조**(사이클당 파일 1개·1 line = 1 전이 이벤트 append-log)는 본 문서 §3.1의 **Worker 제안**이다(근거 (a)~(c) 명시). 이 구조는 03 §3.2-A(10필드·append-only)·§7(재구성)을 물리적으로 보장하나, 대안(교차 사이클 전역 append-log 1개 — memory-data/ index.jsonl 동형)도 계약을 위반하지 않는다. 사이클당 파일 채택 여부는 Advisor 채택 대상이다. 시연 Task(L10)는 이 사이클당 파일 구조(`<cycle_id>.jsonl`)대로 loop-data/를 생성했다(§7 재실측 — v06-demo-a/b/c.jsonl 3건). 계약(03 §3.2-A) 변경이 아니므로 비차단이다.
- **OQ-LB-2 (형태 B 경계 분할 — 비차단).** 사이클 구동 연산 실행 코드(형태 B)가 `framework/loop/` Module 구현 디렉터리와 `framework/adapters/claude/` 사이 어디에 분할 배치되는지는 형태 B 설계 시 확정 대상이다(§4.1, structure.md §4 규칙 4 defer, loop-protocol.md §6 DP-L3·verifier-binding.md OQ-VB-2 동형). Bootstrap(형태 A)에서는 규약 실현이므로 이 분할이 필요하지 않으며, 계약(03 §3) 변경이 아니므로 비차단이다.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 네 번째 산출물(선행: runtime-binding.md·memory-binding.md·verifier-binding.md). 03 §4.1(Loop 바인딩 표 7행)의 **v0.6 물리 실현 매핑**. 정본 = 03 §3·§4 + framework/loop/ 4문서(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 03 §4.1 표 **7행 전부**를 물리 표면으로 매핑("물리 실현" 열 + "실재 여부" 열, 물리 실재/형태 A/형태 B 정직 구분). 세션/턴 호스팅·진입점 4파일·Config 소스·memory-data 백엔드 = 실재; 전이 유발·사람 개입 = 규약 실현(형태 A); 루프 상태 기록 데이터(loop-data/) = 실재(시연 Task L10 생성 — 3파일 7/9/11 line, 본 개정 재실측); 실행 진입점·로더 = 형태 B.
- **§3 (DP-L4):** 루프 상태 기록 물리 백엔드 정본 — 위치 `framework/adapters/claude/loop-data/`(Adapter 경계 이하 격리), 사이클당 파일 1개·1 line = 1 전이 이벤트 append-log(`<cycle_id>.jsonl`) 구조 제안·근거((a) 재구성 단위 = 사이클/(b) append-only 물리 실현/(c) 순서 확정), 10필드 JSON 직렬화(필수 표기 보존), `at` = 순서 값(**L-09** — 시각 주장은 실측 후에만)·`ref` = 참조 토큰(회수 집합 참조 DP-L5 물리 표현, 경량 id 참조).
- **§4:** Loop Provider `entrypoint` 물리 해소(형태 A 규약/형태 B 실행 코드)·`requires`=`MemoryServiceInterface` 물리 해소(memory-binding.md 백엔드 참조) + 재시도 한도 Config 물리 소스(runtime-binding.md §3.3 동형, `retry.limit` 값·스코프는 config-schema.md §7 소유 — 재선언 0).
- **§5:** 역할 실행(CP1=Worker·CP2=Verifier·CP3=Advisor = `.claude/agents/` 서브에이전트)·전이 유발·재작업 지시 라우팅·Verify 트리거 물리 채널(서브에이전트 위임·최종 응답, delegation-protocol.md §3) + 사람 개입 물리 채널(주 세션 사용자 제시, `.claude/CLAUDE.md` 조건 4) + Memory 접근 물리 실현(memory-binding.md 백엔드 경유 — 재정의 0).
- **§6:** 03 §4.2 이식 교체 지점 SP-1~5 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 이식 불변(C-1) 재확인(단계 전이 규칙·재작업 루프·종료 규칙·사람 개입 조건·루프 상태 기록 스키마·Learn 트리거).
- **§7:** 실측 대조(2026-07-06 직접 실측) — 자매 바인딩 3문서·framework/loop/ 4문서·.claude/agents/ 4종·memory-data/·config-schema.md §7 실재; **loop-data/ 실재**(시연 Task L10 생성 — 3파일 각 7/9/11 line, 본 개정 재실측); 실행 진입점·로더 미도입(형태 B). 실측 불일치 0건(A5/L-07 재발 방지, L-09 시각 구분).
- 03·framework/loop/ 4문서 계약 재정의 0, Glossary 용어 신설 0, 새 바인딩 계약 창설 0. 구체 AI·환경·형식 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 동시 작성/후속 시연 산출물 불인용(07 R2); loop-data/ 데이터는 시연 Task(L10) 생성으로 실재(§7 재실측, 생성 주체 구분 — L-07). 이 1파일만 생성.
