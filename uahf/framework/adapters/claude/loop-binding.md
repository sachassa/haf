# framework/adapters/claude/loop-binding — Claude Code Loop Adapter 바인딩

작성일: 2026-07-06
상태: v0.7 Baseline (개정 — §2 행 2 정본 인용 탈락어 복원·loop-data 시연 후 실재 상태 전수 반영(관찰 2·4 해소) · 사용자 승인 2026-07-06). 직전 기준선: v0.6 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본 (계약은 § 포인터로만 인용 — 재정의 0):

- specs/03-loop.md §3.1·§3.1-A~§3.1-D·§3.2·§3.2-A·§3.3·§4.1·§4.2·§5 — 사이클 구동 연산·단계 전이 규칙·재작업 루프·종료 규칙·사람 개입 지점·데이터 포맷·전이 이벤트 10필드 스키마와 append-only 불변·불변 규칙·Claude Code Binding 표(7행)·이식 교체 지점 SP-1~SP-5·Memory 접근(INV-7). 본 문서가 물리 실현으로 인스턴스화·준수하는 계약 정본.
- framework/loop/ 4문서(W1·W2 확정본) — loop-state-record.md·module-manifest.md·stage-transition-rules.md·loop-protocol.md. 이들이 "물리 직렬화·저장 위치·물리 진입점 해소·물리 채널은 Adapter Binding 문서 소관"으로 위임한 지점이 본 문서 §3·§4·§5다(위임 좌표 = §0).
- 자매 Adapter Binding — memory-binding.md(관례 정본 + **Memory 백엔드 `framework/adapters/claude/memory-data/`의 물리 실현 정본** — 본 문서 §5.3은 그 백엔드 경유를 참조만 하고 재정의하지 않는다)·runtime-binding.md(§2 #10 세션/턴 수명주기 컨테이너·§3.3 Config 스코프 물리 소스·§3.4 Bootstrap~Serve~Shutdown 매핑)·verifier-binding.md(§3.1 Agent Module = 서브에이전트 디스패치·§7 실측 대조 관례).
- framework/core/config-schema.md §7(`retry.limit` 기본값 2·Global 스코프 — 값·스코프 소유 소재이며, 본 문서는 값을 재선언하지 않고 소유 포인터 + 물리 소스만 바인딩한다)·framework/core/structure.md §2·§4·§5·§7·§8(4경계 배치·형태 A/B 서술 라벨·금지 토큰 C-3·Core Contract 불변 C-1·트리)·specs/01-runtime.md §3.1-A·§3.1-C·§3.2-B·§4·specs/00-glossary.md(용어 정본)·docs/delegation-protocol.md §3(위임·보고·에스컬레이션 물리 채널 관행)·.claude/agents/ 4종(역할 실행 물리 실체 — 참조만 하고 수정하지 않는다)·Active Lesson L-07·L-09(§3.3·§7 근거)·ROADMAP.md v0.6(Loop Engine).

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계·격리(구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 허용되는 지점 = C-3 비적용)·Bootstrap 전제·용어 사용(glossary 정본만·새 용어 신설 없음)·개정 절차(Advisor 승인 + 본 문서 §9 이력 append)의 근거는 `framework/core/structure.md` §5·§2·§4이며(03 §3.3 INV-9·01 §3.2-E 규칙 3 정합), 자매 바인딩 문서(runtime/memory/verifier-binding.md §0)와 동형이다. 이 문서는 Core Contract(03 §3)와 그 인스턴스 문서(framework/loop/ 4문서)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.6 Draft | 최초 작성. `framework/adapters/claude/` 경계의 네 번째 산출물(선행: runtime-binding.md·memory-binding.md·verifier-binding.md). 03 §4.1 바인딩 표 **7행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정)/데이터 미생성(loop-data/) 정직 구분(§2). 루프 상태 기록 물리 백엔드 정본 확정(§3, DP-L4 — 위치 `framework/adapters/claude/loop-data/`, 사이클당 파일 1개·1 line = 1 전이 이벤트 append-log 구조 제안·근거, 03 §3.2-A 10필드 직렬화·append-only·seq/at 순서·"기록만으로 사이클 재구성" 물리 보장, `at` 순서 값 물리 표현(L-09)·`ref` 회수 집합 참조(DP-L5) 물리 표현). Loop Provider `entrypoint`·`requires` 물리 해소(형태 A/B) + 재시도 한도 Config 물리 소스(runtime-binding §3.3 동형, `retry.limit` 값·스코프는 config-schema.md §7 소유 참조)(§4). 역할 실행(CP1=Worker·CP2=Verifier·CP3=Advisor)·전이 유발·사람 개입 물리 채널(서브에이전트 위임·최종 응답·에스컬레이션) + Memory 접근 물리 실현(memory-binding.md 백엔드 경유 참조, 재정의 0)(§5). 03 §4.2 이식 교체 지점 SP-1~5 대응 표("교체되는 것/유지되는 것" — C-1 이식 불변 재확인, §6). 상태 서술 실측 대조 표(§7 — 실재 서술 전건 파일 시스템 실측 후 기입, L-07; loop-data/ 미생성·시연 Task 생성 예정, L-07). 03 §3·framework/loop/ 4문서 계약 재정의·창설 0, 새 바인딩 계약 0, Glossary 밖 새 용어 0. 동시 작성 시연 절차서(후속 W4 L9)·시연(W5 L10) 내용 불인용(07 R2), 미래 산출물(loop-data/ 데이터) 실재 불주장(L-07). 이 1파일만 생성 — framework/loop/ 4문서·.claude/agents/ 4종·기존 Baseline 산출물·specs/·docs/ 무수정. | Worker (Advisor 위임, Task L8) |
| 2026-07-06 | v0.6 Baseline | v0.6 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.7 Draft (개정) | 관찰 2·4 해소 (WF13). **(1) 개정 ① (관찰 2)** — §2 바인딩 표 행 2 정본 인용 셀에서 03 §4.1 원문 대비 탈락한 단어 **"지정"** 복원(specs/03-loop.md §4.1 원문과 문자 단위 대조 후 — "…(Opus 등) 지정은 02 §4 소관…"). **(2) 개정 ② (관찰 4)** — loop-data/ 상태 서술 **전수 갱신**: L8 draft 시점 "미생성/미존재/생성 예정" 서술(§0·§1·§2 표 행 4·행 4 주·§7 실측 대조 표·§8·§10 — `grep`으로 "미생성"·"미존재"·"생성 예정"·"loop-data" 전수 열거)을, 시연 Task(L10, docs/v0.6-demo.md)가 이 정본 구조대로 생성한 **실측 실재**(3파일 — `v06-demo-a.jsonl` 7 line·`v06-demo-b.jsonl` 9 line·`v06-demo-c.jsonl` 11 line, 본 개정 시 `ls`+`wc -l`+`grep -c cycle_id` 직접 재실측)로 갱신(memory-binding.md r2가 M5 draft "미생성"을 M7 시연 후 실재로 전수 갱신한 관례 동형). §3 물리 백엔드 정본·§4·§5·§6 계약 서술 무변경, 03 §3·framework/loop/ 4문서 계약 재정의 0. **비차단 관찰(Advisor 판단 대상 — 완료 보고 open_questions 에스컬레이션):** 문자 단위 대조 결과 정본 인용 열 행 1·2·3·5·7이 원문의 참조 앞 공백(" (NN §X)")을 house-style로 정규화해 byte 단위 불일치(탈자 아님) — 공백 복원은 "지정" 탈락어 복원 범위 밖이라 본 개정은 미수행. 근거: docs/v0.6-verification-report.md §3.7 관찰 2·4 해소 (v0.7 편입 개정, 사용자 승인 2026-07-06). | Worker (Advisor 위임, Task WF13) |
| 2026-07-06 | v0.7 Baseline | v0.7 개정분(관찰 2·4 해소·상태 라인 정합·이력 라벨 일관화) 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-13 | (OQ 해소 정합 — 버전 무상승) | §8 OQ-LB-2 해소 표기 append — 형태 B Step Hosting 마일스톤이 §4.1 예약 로케이터("사이클 구동을 사람 없이 자동 트리거·반복하는 실행 코드")를 실현: 중립 엔진 = `framework/loop/step-host/`·provider 의존 = `framework/adapters/claude/step-invoker/`·물리 매핑 = `step-hosting-binding.md`·계약 = `framework/runtime/step-hosting-protocol.md`(D-2 사용자 게이트 2026-07-13·dogfooding E2E 7 시나리오 실증). 본문 매핑·계약 무변경(참조 정합=시맨틱 개정 아님 — 버전 미상승 선례·BPD-17 append-only). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07·L-09 유지)·loop-data/ 데모 데이터(v06-demo-*) 실재 서술을 @cd9247b 앵커로 전환(§0 커버리지 노트·§7 실측 표; 백엔드 위치·구조 정본 DP-L4는 계약 서술로 유지). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 2 — 비계약 격리 개정: 재서술·감사 서술·죽은 참조 압축, 계약 문면 무변경. 종전 문면 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/03-loop.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)와 framework/loop/ 4문서(loop-state-record.md·module-manifest.md·stage-transition-rules.md·loop-protocol.md)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·필드·전이 이벤트 스키마·단계 전이 규칙)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- framework/loop/ 4문서가 "물리 직렬화·저장 위치·물리 경로·물리 진입점 해소·물리 채널은 Adapter Binding 문서 소관"이라며 미룬 **직렬화 형식·파일 구조·저장 위치·`at`/`ref` 물리 표현·진입점 물리 해소·역할 실행·사람 개입 물리 채널**이 확정되는 유일한 자리가 이 문서다(loop-state-record.md §0·§7, module-manifest.md §4, stage-transition-rules.md §4, loop-protocol.md §5·§7, 03 §4.1).
- **루프 상태 기록 물리 백엔드 위치 정본 선언(done 2 — Advisor 결정 DP-L4).** 루프 상태 기록의 물리 데이터 위치는 **Adapter 경계 이하 `framework/adapters/claude/loop-data/`로 확정한다**(Core 경계·`specs/`·`docs/` 밖 — memory-binding.md §0 memory-data/ 선언 동형). **하위 경로·파일 구조·직렬화 형식·`at`/`ref` 물리 표현의 정본은 이 문서 §3이며**, framework/loop/ 4문서는 이 물리 위치를 "Adapter Binding 문서 소관" 포인터로만 미뤘다(loop-state-record.md §7·03 §4.1 SP-3).
- **창설 금지.** 이 문서는 03 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.6 산출물(루프 상태 기록 포맷·단계 전이 규칙·재작업 루프·Learn 트리거)의 물리 실현 매핑으로 한정한다. 새 단계·새 전이·새 전이 이벤트 필드·새 개입 조건·새 불변 규칙을 만들지 않는다.
- **실측 기반 상태 서술(done 4, L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(L-07 — 상태 서술은 실측 후 기록) — 미존재를 실재로 쓰지 않고, 실재는 실측 후에만 기입한다. §2 "실재 여부" 열과 §7 실측 대조 표가 그 대조 자리다. 이 하네스는 Bootstrap 상태이므로(Glossary J-13) 본 문서의 매핑은 이미 물리적으로 실재하는 표면과 실행 코드 도입 시 로딩될 지점을 형태 A(문서·규약)/형태 B(실행 코드) 라벨로 구분한다(라벨 = structure.md §4).
- **loop-data/ 데모 데이터 아카이브.** loop-data/ 데모 사이클 데이터(`v06-demo-*.jsonl`)는 산출물 수명 정책(루트 `docs/artifact-lifecycle-policy.md` §7)으로 작업 트리에서 제거되었다 — 파일 구조·line·byte 상세는 앵커 `cd9247b` 열람(`git show cd9247b:uahf/framework/adapters/claude/loop-data/`). loop-data/ **백엔드 위치·구조 정본**(DP-L4·§3)은 계약 서술로 유지된다. `uaf-allow-legacy: 아카이브된 데모 데이터의 종전 "실재" 서술을 이력·앵커 인용으로 보존`

---

## §1. 목적

이 문서는 03 §4.1(Loop Claude Code Binding)을 이 환경 위의 구체 물리 실현으로 매핑한다 — 바인딩 표 7행의 물리 표면 확정과 물리 실재/형태 A/형태 B 구분(§2, done 1·4), 루프 상태 기록 물리 백엔드 정본(§3, done 2 — DP-L4), Loop Provider `entrypoint`·`requires` 물리 해소와 재시도 한도 Config 물리 소스(§4), 역할 실행(CP1~CP3)·전이 유발·사람 개입 물리 채널과 Memory 접근 물리 실현(§5), 03 §4.2 이식 교체 지점 SP-1~5 대응(§6, done 3), 상태 서술 실측 대조(§7, done 4).

이 문서는 03 §3·framework/loop/ 4문서의 어떤 계약 요소도 재정의·확장하지 않는다(§0, done 5). 형태 A → 형태 B 전환 시에도 Core Contract(03 §3) 변경은 없으며(structure.md §7 C-1), §6의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 03 §4.1 바인딩 표 7행 물리 실현 (done 1·4)

03 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. "03 §4.1 바인딩" 열은 정본 표현을 그대로 인용하고, "물리 실현" 열이 이 환경의 경로·구조·형식·채널을, "실재 여부" 열이 물리 실재/규약 실현(형태 A)/형태 B를 구분한다(§7 실측 대조, L-07).

물리 백엔드 디렉터리 구조(본 문서 정본 — DP-L4):

```
framework/adapters/claude/
├─ runtime-binding.md          # 자매 바인딩
├─ memory-binding.md           # 자매 바인딩 — Memory 백엔드 소관
├─ verifier-binding.md         # 자매 바인딩
├─ loop-binding.md             # 본 문서
├─ memory-data/                # Memory 백엔드 (memory-binding.md 소관)
└─ loop-data/                  # ★ 루프 상태 기록 백엔드 격리 루트 — 백엔드 위치 정본(DP-L4); 데모 데이터는 앵커 cd9247b 열람(§0·§7)
   └─ <cycle_id>.jsonl         #   사이클당 파일 1개 = 전이 이벤트 append-log (1 line = 1 전이 이벤트; §3)
```

| # | §3 계약 요소 (정본 §) | 03 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Loop 호스팅 (Serve 구간, 03 §3.1·§2) | Claude Code 세션/턴이 Runtime의 Bootstrap~Serve~Shutdown 구간을 호스팅한다(01 §4.1). Loop는 이 Serve 구간에서 구동된다. | Loop 사이클 구동 연산(03 §3.1)은 Claude Code **세션/턴**을 실행 컨테이너로 삼아 **Serve 구간(01 §3.1-C = 턴 진행)**에서 구동된다(runtime-binding.md §2 #10·§3.4 동형). Loop는 이 구간을 **소비만** 하고 Bootstrap/Shutdown을 재정의하지 않는다(03 INV-8). Loop Provider `entrypoint`의 물리 해소는 §4.1. | 세션/턴 컨테이너 실재(현 세션이 그 컨테이너). 사이클 구동 실행 진입점은 형태 B(§8 OQ-LB-2). |
| 2 | 역할 실행 (CP1/CP2/CP3, 03 §3.1-A) | 각 역할은 `.claude/agents/*.md` 서브에이전트로 실행된다(02 §4.1). CP1=Worker, CP2=Verifier, CP3=Advisor. Worker 기본 실행 모델(Opus 등) 지정은 02 §4 소관이며 이 spec은 참조만 한다. | 검증 게이트 세 체크포인트의 역할이 `.claude/agents/` 서브에이전트로 실행된다 — **CP1=Worker**(`worker.md`, 실측 `model: opus`)·**CP2=Verifier**(`verifier.md`, 실측 `model: opus`)·**CP3=Advisor**(`advisor.md`, 주 세션 바인딩). Planner(`planner.md`)는 Plan 초안 역할. 물리 채널 상세는 §5.1(실행 모델 지정 의미는 02 §4 소관 — 참조만). | `.claude/agents/` 4종 정의 파일 실재(§7 실측). 무인 자동 역할 구동(형태 B)은 미도입. |
| 3 | 단계 전이 유발 (03 §3.1-A) | 위임·보고는 서브에이전트 위임과 최종 응답으로 흐른다(02 §4.1). | 전이를 유발하는 위임·보고가 **서브에이전트 위임**(위임 메시지 02 §3.2-B)·**최종 응답**(완료/실패 보고 02 §3.2-C/D)으로 흐른다(delegation-protocol.md §3.1·§3.2). 재작업 지시(loop-protocol.md §5.1) 라우팅 = 재위임 메시지. 각 전이는 §3의 루프 상태 기록에 남는다(03 INV-3). 물리 채널 상세는 §5.1. | 위임·최종 응답 채널 규약 실현(형태 A, Bootstrap). 무인 자동 트리거(형태 B)는 미도입. |
| 4 | 루프 상태 기록 직렬화 (03 §3.2-A) | §3.2-A 추상 스키마를 파일 기반 기록(구조화 로그/마크다운 등)으로 직렬화한다. 구체 경로·문법은 이 바인딩이 정한다. | `framework/adapters/claude/loop-data/<cycle_id>.jsonl` — 사이클당 파일 1개, 1 line = 1 전이 이벤트(append-only). 전이 이벤트 10필드(03 §3.2-A)를 각 line에 직렬화한다. 물리 구조·형식·경로·`at`/`ref` 물리 표현의 정본은 §3(DP-L4). | 형식·경로 구조 확정(정본, §3). 데모 데이터는 앵커 cd9247b 아카이브 — 작업 트리 제거(§0·§7). |
| 5 | 재시도 한도 Config (03 §3.1-B) | 재시도 한도 값은 effective config(01 §3.2-B)로 주어진다. v0.x에서 `.claude/CLAUDE.md`·설정 파일이 Project scope Config를 제공한다(01 §4.1). | 재시도 한도 추상 키 `retry.limit`(값 2·기본 스코프 Global)의 **값·스코프 소유는 framework/core/config-schema.md §7**이며, 물리 소스는 Config 스코프별 소스(runtime-binding.md §3.3 동형 — Global = `~/.claude/settings.json`, Project override = `.claude/`, Module scope = 형태 B)다. Loop는 이 값의 **소비자**일 뿐 소유자가 아니다(module-manifest.md DP-L2). 물리 소스 상세는 §4.2. | Config 물리 소스 실재. effective config 로딩(형태 B)은 미도입 — 값은 config-schema.md §7 결정 기록으로 실현(형태 A). |
| 6 | 사람 개입 채널 (03 §3.1-D) | §3.1-D 사람 승인 요청은 Claude Code 세션에서 사용자에게 제시된다. `.claude/CLAUDE.md`의 "Architecture와 Spec 충돌 시 사용자 보고"가 조건 4의 바인딩이다. | 사람 승인 요청(에스컬레이션 산출 — 사람 승인 요청 및/또는 실패 보고 02 §3.2-D)이 **주 세션**(Advisor 바인딩, `.claude/CLAUDE.md`)에서 **사용자에게 제시**된다(delegation-protocol.md §3.4). `.claude/CLAUDE.md`의 "Architecture와 Spec 충돌 시 사용자 보고"가 03 §3.1-D 조건 4의 바인딩이다(실측 — §7). `actor` = human 전이는 §3의 루프 상태 기록에 남는다. 물리 채널 상세는 §5.2. | 세션 제시 채널 규약 실현(형태 A). `.claude/CLAUDE.md` 조건 4 바인딩 실재(§7 실측). |
| 7 | Memory 접근 (03 §5) | Memory Update의 단일 Port 경유는 Runtime이 배선한 Memory Service Interface Module을 Resolve하여 실현한다(01 §5, 02 §4). | Loop의 Memory 접근(Consult 회수·Memory Update 기록, 03 §5·INV-7)은 **memory-binding.md가 확정한 백엔드**(`framework/adapters/claude/memory-data/`)를 단일 Port(memory-service.md §7) 경유로 실현한다 — Loop는 소비자이며 본 문서는 그 물리 실현을 **참조만** 하고 재정의하지 않는다(재정의 0). 접근 시점·회수 집합 기록은 §5.3. | Memory 백엔드(memory-data/) 실재(memory-binding.md §7 실측). 단일 Port 경유 규약 실현(형태 A). |

주:

- 위 7행은 03 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 정본 표현을 이 환경의 구체 경로·형식·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **역할 실행 = Agent Module(서브에이전트 채널).** CP1~CP3 역할은 서브에이전트로 디스패치되는 Agent Module이므로(verifier-binding.md §3.1 동형), 위임·보고·재작업 지시 전달이 **서브에이전트 위임/최종 응답 채널**로 실현된다. 이는 단일 Port로 소비되는 Cross-cutting Service(Memory, 행 7)의 Port 소비 경로와 다른 실현 방식이다(§5.1·§5.3).
- **데이터 생성 주체 구분(L-07).** 행 4의 정본성은 구조·형식·경로·`at`/`ref` 물리 표현 **관례**에 대한 것이며, loop-data/ 데모 데이터는 시연 Task가 이 정본 구조대로 생성했다(현재는 앵커 cd9247b 아카이브 — §0). 본 문서는 그 데이터를 생성·수정하지 않고 구조·형식 정본만 소유한다.

---

## §3. 루프 상태 기록 물리 백엔드 정본 확정 (done 2 — DP-L4)

loop-state-record.md §7·03 §4.1·§4.2 SP-3이 "루프 상태 기록의 직렬화 형식·저장 위치·물리 경로·`at`/`seq`/회수 집합 참조의 물리 표현·append-only의 물리 실현은 전부 Adapter Binding 문서 소관"으로 미룬 지점을 확정한다. 계약 요소(전이 이벤트 10필드·의미·필수 표기·append-only 불변·회수 이력 기록 위치)의 정본은 loop-state-record.md §2~§6·03 §3.2-A이며, 본 절은 그 물리 실현만 확정한다(재정의 0).

### §3.1 물리 백엔드 위치·디렉터리 구조 (DP-L4 + 구조 제안·근거)

- **물리 위치 정본(Advisor 결정 DP-L4).** 루프 상태 기록의 물리 데이터 위치는 `framework/adapters/claude/loop-data/`로 확정한다 — Adapter 경계 이하 격리(memory-binding.md §0 memory-data/ 동형)이며 Core 경계·`specs/`·`docs/` 밖이다. 소비자(역할·Loop 오케스트레이션)는 이 경로·형식을 직접 참조하지 않는다 — 루프 상태 기록은 이 백엔드로 격리된다(03 §4.2 SP-3).
- **구조 제안(Worker 제안 — DP-L4 위치 내 하위 구조).** 각 사이클의 전이 로그를 **사이클당 파일 1개**로 두고, 그 파일을 **1 line = 1 전이 이벤트의 append-log**로 직렬화한다: `loop-data/<cycle_id>.jsonl`. 파일명 = 전이 이벤트 `cycle_id`(03 §3.2-A — "하나의 위임 = 하나의 사이클"), 각 line = 그 사이클의 전이 이벤트 1건.
- **제안 근거.** **(a) 재구성 단위 정합(03 §3.2-A·§7).** 정본이 요구하는 "이 로그만으로 사이클 전체를 재구성·검증"의 단위는 `cycle_id`로 식별되는 **사이클**이며, 사이클당 파일 1개는 그 재구성을 **파일 1개 판독으로 자기완결**시킨다(단계 경로·재작업 되돌림·에스컬레이션·회수 참조가 한 파일 안에 있다). 교차 사이클 전역 로그를 쓰는 memory-data/와는 재구성 단위가 다르다. **(b) append-only의 물리 실현(03 INV-3).** append-log는 append-only 불변(loop-state-record.md §5)을 **파일 끝 line 추가**로 실현한다 — 기존 line은 재작성·삭제하지 않고, 갱신·정정도 **새 전이 이벤트 line 추가**로만 한다. **(c) 순서 확정(03 §3.2-A).** 파일 내 line 순서가 사이클 내 전이 순서와 정합한다 — `seq` 단조 증가와 `at` 순서 값(§3.3)이 순서를 확정하며, 재작업 되돌림(`outcome`=fail·`retry_count` 증가)·에스컬레이션(`outcome`=escalated·`actor`=human)도 각각 하나의 line으로 append된다.
- **직렬화 형식 = Adapter 선택.** 사이클 기록은 line 구분 로그(JSON Lines), 각 line의 전이 이벤트는 자기서술적 데이터 형식(JSON 객체)으로 직렬화한다. 이 선택은 03 §4.2 SP-3의 교체 지점이며 이식 시 대상 환경 로깅 메커니즘으로 교체된다(§6). 규모 대응(파일 회전·샤딩)은 형태 B 사안으로 미룬다(structure.md §4 규칙 4 defer).

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
- **재구성 보장의 물리 실현(03 §7).** 한 사이클 파일의 line 집합은 그 사이클의 단계 경로(각 line의 `from_stage`→`to_stage` 연쇄)·재작업 되돌림(`outcome`=fail·`retry_count` 증가 line)·에스컬레이션(`outcome`=escalated·`actor`=human line)·회수 참조(Consult line의 `ref`, §3.3)를 복원하기에 충분하다(loop-state-record.md §5). Verifier는 이 파일을 파싱해 전이 순서·완료 조건 충족·append-only 여부를 확인한다(03 §7 검증 방법).
- **정합 대조(검증 지점).** 사이클 파일 내 `seq`의 단조 증가와 line 순서의 일치, 첫 line의 `from_stage` 부재, 각 재작업 line의 `retry_count` 단조 증가가 append-only·순서 확정의 물리 대조 지점이다.

### §3.3 `at`(순서 값 — L-09) · `ref`(회수 집합 참조 — DP-L5) 물리 표현

loop-state-record.md §2·§6이 "`at`의 물리 시각 표현, 회수 집합 참조의 물리 표현은 Adapter Binding 소관"으로 미룬 두 지점을 확정한다.

- **`at` 물리 표현 = 순서 값(L-09 준수).** `at`은 loop-state-record.md §2가 "순서 보장용 **추상 시각**"으로 정의하고 물리 표현을 Adapter Binding에 위임한 필드다. 물리 표현: `at`은 사이클 내에서 **단조 증가하는 순서 값**으로 직렬화한다 — `seq`와 함께 전이 순서를 확정하는 값이며, **물리 벽시계 시각(wall-clock)이 아니다**. L-09 준수: 순서 값을 기록하되 그 값을 **물리 시각으로 주장하지 않는다**. 실제 물리 시각이 필요하면 파일·line의 물리 생성 시각(mtime 등)을 **실측**해 별도로 공개한다. 순서 값의 구체 형식(정수 서수·정렬 가능 토큰 등)은 Adapter 선택이며 이식 교체 지점 SP-3에 속한다(§6).
- **`ref` 물리 표현 = 참조 토큰(회수 집합 참조 포함).** `ref`은 "관련 산출물·보고 참조"(loop-state-record.md §2 / 03 §3.2-A)를 담는 선택 필드다. 물리 표현: line 내 JSON 값으로 **참조 토큰**을 담는다 — 위임/완료/실패 보고·Verifier 판정 참조는 그 산출물·보고의 식별 참조를, **Consult 전이 이벤트의 회수 집합 참조(DP-L5)**는 그 사이클에서 회수된 Memory Item id 집합의 참조(memory-data/ store id 스킴 `mi-<정렬가능토큰>`의 배열 — memory-binding.md §2)를 담는다.
  - **회수 집합 참조의 소관 경계(DP-L5).** "Consult 전이 이벤트의 `ref`에 회수 집합 참조를 기록한다"는 **기록 위치**는 loop-state-record.md §6(Advisor 결정 DP-L5)이 소유한다 — 본 절은 그 참조가 line 안에서 어떤 형식으로 직렬화되는가(물리 표현)만 확정한다. 회수 집합의 **내용**(무엇이 회수되었는가)·회수 정책·회수 집합의 **소비**(05 재발 판정의 `was_recalled` 입력)는 03 §5·04·05 소관이며(loop-state-record.md §6), 본 문서는 재서술하지 않는다.
  - **경량 참조(최소 Context).** `ref`은 회수된 Memory Item의 `content` 원문을 담지 않고 그 **id 참조**만 담는다 — 원문이 필요하면 그 id로 Memory 백엔드에서 Recall한다(memory-binding.md §3.2 index-first, 04 INV-4 최소 Context와 정합). 이는 루프 상태 기록이 Memory content를 중복 저장하지 않게 한다.
- **물리 백엔드 격리.** `at`·`ref`의 위 물리 표현은 전부 `framework/adapters/claude/loop-data/` 뒤로 격리된다 — 소비자는 루프 상태 기록을 Loop 오케스트레이션 경유로만 소비하며 이 표현을 직접 참조하지 않는다(03 §4.2 SP-3). 이식 시 §3.2 필드·§3.3 표현은 유지되고 물리 직렬화만 교체된다(03 §4.2, §6).

---

## §4. Loop Provider `entrypoint`·`requires` 물리 해소 · 재시도 한도 Config 물리 소스 (done 1 상세)

module-manifest.md §4가 "`entrypoint`·`requires`의 물리 해소는 Adapter Binding 문서 소관"으로 미룬 지점과, 03 §4.1 재시도 한도 Config 행의 물리 소스를 확정한다. runtime-binding.md §3.2·§3.3·memory-binding.md §4의 교체 지점 관례(추상 참조 → 물리 실현, 형태 A/B 구분)와 동형이다.

### §4.1 `entrypoint`·`requires` 물리 해소

module-manifest.md §2·§4 `entrypoint` = "추상 참조 — 사이클 구동 연산(03 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관". `requires` = `MemoryServiceInterface`. 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Loop Provider Module 활성화 진입 — 사이클 구동 연산(03 §3.1) 노출 | **형태 A(Bootstrap):** 활성화 진입은 규약으로 실현된다 — 사이클 구동 연산은 loop-protocol.md §3의 오케스트레이션 절차(위임 수령 → Consult → … → Complete/에스컬레이션)에 따라 세션/턴(§2 #1)에서 구동되며, 각 단계 역할은 서브에이전트 위임으로 실행된다(§5.1). 별도 실행 진입점 파일은 없다. | 규약 실현(형태 A) |
| 위 진입점의 실행 코드 로케이터 | **형태 B:** 사이클 구동 연산을 사람 없이 자동으로 트리거·반복하는 실행 코드가 non-core 실행 경계(`framework/loop/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지, loop-protocol.md §6 DP-L3). | 형태 B |
| `requires` = `MemoryServiceInterface` 물리 해소 | Loop Provider가 Resolve될 때 함께 해소되어야 하는 Memory Service Interface 계약(01 §3.1-A Resolve 완료 조건)의 물리 실현은 **memory-binding.md가 확정한 백엔드**(`framework/adapters/claude/memory-data/`)이다. Loop의 Memory Update(모든 사이클의 불가피 단계 — 03 INV-5·INV-7)는 이 백엔드를 단일 Port 경유로 소비한다(§5.3). 본 문서는 그 물리 배선을 재정의하지 않고 참조만 한다. | memory-binding.md 소관(참조) |

- **Register/Resolve 정합(verifier-binding.md §3.1 Agent Module 동형).** Loop Provider의 등록(Register)은 Manifest(framework/loop/module-manifest.md) + 본 바인딩 배치로 규약 실현되며(형태 A), 해소(Resolve)는 소비자(03 §2 dependents)가 `contract` `LoopInterface`로 사이클 구동을 요청할 때 이 Provider로 해소되는 것이다. 역할 실행(CP1~CP3)은 module Resolve가 아니라 서브에이전트 디스패치이며(module-manifest.md §3 `requires` 주), 그 물리 채널은 §5.1이다. 이 등록 경로는 이식 교체 지점 SP-1·SP-2에 대응한다(§6).

### §4.2 재시도 한도 Config 물리 소스 — `retry.limit` (config-schema.md §7 소유 참조)

03 §3.1-B은 "재시도 한도 값은 Config로 주어진다. Loop는 한도 초과 판정 규칙만 정의한다"고 규정하고, 그 값·스코프 소유는 framework/core/config-schema.md §7이다(module-manifest.md DP-L2 — Loop는 소비자, `configSchema` 생략). 그 물리 소스:

| 관점 | 물리 실현 (claude 환경) | 형태 |
|---|---|---|
| **값·기본값·스코프 소유** | 추상 키 `retry.limit`, 기본값 **2**, 기본 스코프 **Global**(Project/Module override 허용)의 선언은 framework/core/config-schema.md §7이 소유한다(실재 — DP-1 결정 기록). 본 문서는 재선언하지 않는다(값 이중화 방지). | 실재(형태 A 선언, config-schema.md §7) |
| **물리 소스(스코프별)** | runtime-binding.md §3.3 동형: Global 기본값(2) 소속 = `~/.claude/settings.json`(실재), Project override = `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`(실재), Module scope = 형태 B(실행 코드 도입 시 Loop Provider 설정 블록). 병합은 Module > Project > Global(01 §3.2-B, config-schema.md §4.2). | Global/Project 소스 실재, Module 소스는 형태 B |
| **읽히는 지점(read)** | 재작업 루프 구동 시 읽힌다 — 소비 지점은 loop-protocol.md §4(재시도 한도 초과 판정 → 에스컬레이션). Loop는 effective config의 소비자다(01 §3.2-B). | 규약 실현(형태 A) / 형태 B 로더 |
| **적용 방식(apply)** | `retry_count`가 `retry.limit`을 초과하면 에스컬레이션한다(loop-protocol.md §4·03 §3.1-B, §3.1-D 조건 1). 한도 초과 **판정 규칙**은 03 §3.1-B 소관으로 불변이며, 본 문서는 값의 물리 소스·읽힘만 바인딩한다. | 03 §3.1-B 판정 규칙(불변) |

- **형태 구분.** Bootstrap에서 이 값은 config-schema.md §7 결정 기록(기본 2·Global)으로 실현(형태 A)되며, 실행 로더(형태 B) 도입 시 effective config(Module > Project > Global 병합)로 로딩되어 재작업 루프가 loop-protocol.md §4로 적용한다. 한도의 **존재·의미**(03 §3.1-B) 계약은 불변이며, 본 문서는 값 원천·읽힘·적용의 물리 지점만 바인딩한다(config-schema.md §7·module-manifest.md DP-L2 재정의 0).

---

## §5. 역할 실행·전이 유발·사람 개입 물리 채널 · Memory 접근 물리 실현 (done 1 상세)

03 §4.1 역할 실행(행 2)·단계 전이 유발(행 3)·사람 개입 채널(행 6)·Memory 접근(행 7)의 물리 채널을 확정한다 — loop-protocol.md §5(이연 4건: 재작업 지시 라우팅·Verify 트리거·Memory 접근 시점·종료/사람 개입)·§7이 "물리 채널·직렬화·물리 실행은 Adapter Binding 문서 소관"으로 미룬 지점의 물리 실현이다.

### §5.1 역할 실행 · 전이 유발 · 재작업 지시 라우팅 물리 채널 (03 §4.1 행 2·3)

- **역할 실행(CP1~CP3) = 서브에이전트 디스패치.** 검증 게이트 세 체크포인트의 역할이 `.claude/agents/` 서브에이전트로 실행된다 — CP1=Worker(`worker.md`), CP2=Verifier(`verifier.md`), CP3=Advisor(`advisor.md`). 활성화 = 서브에이전트 위임 시 정의 파일 로딩(Resolve — verifier-binding.md §3.1 Agent Module 동형). Worker·Planner·Verifier 실행 모델(실측 `model: opus`)·Advisor 세션 상속(미지정)의 **지정 의미**는 02 §4 소관이며 본 문서는 참조만 한다.
- **전이 유발 = 위임·최종 응답.** 단계 전이를 유발하는 위임·보고가 **서브에이전트 위임**(위임 메시지 02 §3.2-B — delegation-protocol.md §3.1)·**최종 응답**(완료 보고 02 §3.2-C / 실패 보고 02 §3.2-D — delegation-protocol.md §3.2)으로 흐른다. 각 전이는 §3의 루프 상태 기록(loop-data/)에 append된다(03 INV-3).
- **재작업 지시 라우팅(loop-protocol.md §5.1 물리 실현).** CP2 판정이 Fail 또는 Conditional이면, 검증 리포트의 재작업 지시(`rework` — 06 §3.2-D, verifier-binding.md §4.2)가 근본 원인별 되돌림 단계(loop-protocol.md §4)의 **재위임 메시지**(02 §3.2-B, delegation-protocol.md §3.1)에 실려 흐른다. 재작업 지시 포맷 정본은 06·rework-instruction.md이며 본 문서는 물리 전달 채널(재위임 서브에이전트 위임)만 바인딩한다(loop-protocol.md §5.1 경계, verifier-binding.md §4.2 동형).
- **Verify 트리거(loop-protocol.md §5.2 물리 실현).** Execute 완료(산출물 + 자체 점검 CP1) 시점에 Loop 오케스트레이션이 CP2 판정을 위한 입력{산출물 + criteria}을 구성해 Verifier 서브에이전트에 위임(구동)한다. 판정 연산의 절차·기준·리포트는 06·verifier-binding.md 소관이며 본 문서는 구동 채널(서브에이전트 위임)만 바인딩한다. 무인 자동 트리거는 형태 B(loop-protocol.md §6 DP-L3).

### §5.2 사람 개입 물리 채널 (03 §4.1 행 6 / §3.1-D)

- **제시 채널.** 사람 승인이 필요한 5조건(03 §3.1-D, loop-protocol.md §5.4) 발생 시, 에스컬레이션 산출(사람 승인 요청 및/또는 실패 보고 02 §3.2-D)이 **주 세션**(Advisor 바인딩 — `.claude/CLAUDE.md`)에서 **사용자에게 제시**된다. 물리 채널 = 서브에이전트 최종 응답으로 Advisor에게 회수된 뒤 사용자에게 제시(delegation-protocol.md §3.4).
- **조건 4 바인딩(실측).** 03 §3.1-D 조건 4(상위 규약·Architecture 충돌)의 이 환경 바인딩은 `.claude/CLAUDE.md`의 "Architecture와 Spec이 충돌하면 Spec을 수정하지 말고 사용자에게 보고한다"이다(03 §4.1 정본 인용, §7 실측 확인). advisor.md 금지 사항이 이를 역할 정의에서 재확인한다.
- **개입 기록.** 각 사람 개입 발생은 §3의 루프 상태 기록에 `actor` = human 전이(§3.2 표)로 남는다(03 §3.1-D·§3.2-A, loop-protocol.md §5.4). 무인 자동 개입 트리거는 형태 B다(loop-protocol.md §6 DP-L3).

### §5.3 Memory 접근 물리 실현 (03 §4.1 행 7 / §5) — memory-binding.md 백엔드 경유 (재정의 0)

- **접근 경로.** Loop의 Memory 접근(Consult 회수 · Memory Update 기록, 03 §5·INV-7)은 **memory-binding.md가 확정한 백엔드**(`framework/adapters/claude/memory-data/`)를 단일 Port(memory-service.md §7 — Loop는 소비자) 경유로 실현한다. 물리 저장·직렬화·Record/Recall 물리 절차는 memory-binding.md §2·§3이 소유하며, **본 문서는 재정의하지 않고 참조만 한다**(재정의 0 — done 5).
  - **회수(Recall) 시점 = Consult 구동.** 착수 전 관련 Lessons·이전 결정·컨텍스트를 회수한다(loop-protocol.md §5.3). 회수 절차(purpose·scope 필수, bounded, 전량 로드 금지)의 물리 실현은 memory-binding.md §3.2(index-first)다.
  - **기록(Record) 시점 = Memory Update 구동.** Learn이 도출한 후보(Lesson 후보 / Best Practice 후보, 03 §3.2-C)를 기록한다. 기록 절차(Item 파일 쓰기 + Index line append 정합, INV-7)의 물리 실현은 memory-binding.md §3.1이다.
- **회수 집합 기록의 접속.** Consult 회수 집합의 참조는 §3의 루프 상태 기록 Consult 전이 이벤트 `ref`에 기록된다(loop-state-record.md §6 DP-L5, 물리 표현 §3.3) — loop-data/와 memory-data/를 잇는 지점이며, `ref`은 memory-data/ store id 참조만 담고 Memory content를 loop-data/에 중복 저장하지 않는다(§3.3 경량 참조).
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

- **"유지되는 것" 열의 이식 불변성.** 위 계약(03 §3.1-A 단계 전이 규칙·§3.1-B 재작업 루프·§3.1-C 종료 규칙·§3.1-D 사람 개입 조건·§3.2-A 루프 상태 기록 스키마·§3.2-C Learn 트리거)은 다른 AI·환경으로 이식해도 바뀌지 않는다 — 03 §4.2 말미 "유지되는 것" 목록의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다. framework/loop/ 4문서가 그 계약의 인스턴스이며 이식 시에도 불변이다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다 — 본 문서는 그 정식화를 선취하지 않고 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 4 — A5/L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 본 문서의 "실재/존재" 서술을 파일 시스템과 직접 대조한 결과다. **byte·line 수 스냅샷은 이 표에 재기록하지 않는다** — 시점 박힌 수치는 곧 낡아 stale 서술의 원천이 되기 때문이며, 종전 판의 수치 문면은 git 앵커 90ca19c에서 열람한다. 아래 표는 구조·1:1 대응·실재/미도입 등 **불변 주장**만 담는다.

| 대상 | 본 문서 서술 | 실측 결과 |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — 자매 바인딩 문서·memory-data/ 존재 확인. |
| `framework/adapters/claude/runtime-binding.md` | 실재 (자매) | 실재. |
| `framework/adapters/claude/memory-binding.md` | 실재 (자매) | 실재. |
| `framework/adapters/claude/verifier-binding.md` | 실재 (자매) | 실재. |
| `framework/adapters/claude/loop-binding.md` | 실재 (본 문서) | 실재 (이 파일). |
| `.claude/agents/` 4종 (§2 #2 진입점) | 실재 (advisor/planner/verifier/worker.md — 역할 실행 물리 실체) | 실재 — 4파일 존재, §2 #2 역할 4종과 1:1 대응. |
| `.claude/agents/worker.md` 실행 모델 (§2 #2·§5.1) | 실재 `model: opus` (지정 의미는 02 §4 소관) | 실재 — front-matter `model: opus` 확인. |
| advisor/planner/verifier.md 실행 모델 (§5.1) | planner·verifier = `model: opus` 지정 · advisor = 세션 상속(미지정) | 실재 — planner.md·verifier.md front-matter `model: opus` 확인, advisor.md는 `model` 라인 0건. `uaf-verified: .claude/agents/*.md front-matter grep — 스윕 범위 = .claude/agents/ 4파일` |
| `framework/loop/` 4문서 (W1·W2 확정본 — 계약 인스턴스, § 포인터 대상) | 실재 (loop-state-record·module-manifest·stage-transition-rules·loop-protocol) | 실재 — 4파일 존재·무수정, §0 정본 4문서와 1:1 대응. |
| `framework/adapters/claude/loop-data/` (§2 #4·§3 백엔드 루트) | 백엔드 위치 정본(DP-L4) — 데모 데이터 아카이브 | 백엔드 경로는 DP-L4 정본(§3, 계약 서술로 유지). 데모 사이클 데이터는 산출물 수명 정책으로 작업 트리에서 제거 — 앵커 `cd9247b` 열람(`git show cd9247b:uahf/framework/adapters/claude/loop-data/`). |
| `framework/adapters/claude/memory-data/` (§2 #7·§5.3 Memory 백엔드) | 실재 (memory-binding.md 확정 백엔드, 자매) | 실재 — `memory-data/store/`·`memory-data/index/` 존재 확인. |
| `.claude/CLAUDE.md` 조건 4 바인딩 (§2 #6·§5.2) | 실재 ("Architecture와 Spec 충돌 시 사용자 보고") | 실재 — `.claude/CLAUDE.md` "Architecture와 Spec이 충돌하면 Spec을 수정하지 말고 사용자에게 보고한다" 확인. |
| `retry.limit` 값·스코프 (§4.2) | 실재 (형태 A 선언, config-schema.md §7 — 기본 2·Global) | 실재 — config-schema.md §7 결정 기록(기본값 2·Global 스코프) 확인. |
| Config 물리 소스 (§4.2) | 실재 `~/.claude/settings.json`·`.claude/` (runtime-binding.md §3.3 동형) | 실재(자매 문서 실측 승계) — runtime-binding.md §3.3 소스 목록 참조. |
| 사이클 구동 실행 진입점·실행 로더 (형태 B) | 형태 B 실행 코드는 Step Hosting 마일스톤이 도입 (§8 OQ-LB-2 해소) | 실재 — `framework/loop/step-host/`에 사이클 구동 실행 코드가 존재하고 provider 의존 호출은 `framework/adapters/claude/step-invoker/`에 있다(§8 OQ-LB-2). 형태 A(규약 실현) 경로는 병존 유효. |

- **핵심 구분.** 본 문서가 확정한 루프 상태 기록의 **경로·파일 구조·직렬화 형식·`at`/`ref` 물리 표현은 정본**(§3)이며, 데이터의 생성 주체는 시연 Task다 — 본 문서는 loop-data/ 데이터를 생성·수정하지 않고 구조·형식·표기의 정본만 소유한다(생성 주체 구분, L-07).
- 실재를 주장하는 행은 파일 시스템 직접 실측 후에만 기입했다 — 미존재를 실재로, 실재를 미존재로 쓰지 않는다(A5/L-07 재발 방지). 순서 값·시각 서술은 L-09 준수(§3.3 — `at` 순서 값, 시각 주장은 실측 후에만). `uaf-verified: 위 표 대상 경로를 파일 시스템 열거(ls)로 확인 — 스윕 범위 = 이 표에 열거된 경로에 한정`
- **정정 이력(2026-07-26).** 마지막 행은 종전 판에서 "미도입 — `framework/loop/`는 계약 문서 4건만 실재(실행 코드 0)"였으나 실측과 어긋나 정정했다(step-host/ 실행 코드 실재). §2 표 "실재 여부" 열의 형태 B 관련 서술은 계약·매핑 문면이므로 본 개정에서 바꾸지 않았다 — 재검토는 Advisor 판단 대상이다.

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 5).** 본 문서의 모든 매핑은 03 §3·§4·framework/loop/ 4문서의 물리 실현이다. 어떤 연산·데이터 계약·불변 규칙·전이 이벤트 필드·단계 전이 규칙·개입 조건도 이 문서에서 새로 확정되지 않는다 — 판정 기준은 정본 §(03 §3·loop-state-record.md·module-manifest.md·stage-transition-rules.md·loop-protocol.md)다. 새 바인딩 계약·새 단계·새 전이·새 필드·새 개입 조건·새 불변 규칙을 추가하지 않았다. `uaf-verified: 본 문서 전 절을 정본 § 포인터 대조로 훑음 — 스윕 범위 = 이 문서 §0~§8`
- **계약 소유 경계.** 전이 이벤트 스키마·append-only 불변·회수 이력 기록 방식(DP-L5) = loop-state-record.md/03 §3.2 · 단계 전이 규칙·게이트-단계 매핑 = stage-transition-rules.md/03 §3.1-A · 사이클 구동 연산·재작업 루프·종료·사람 개입 오케스트레이션 = loop-protocol.md/03 §3.1 · Manifest 필드·`entrypoint`·`requires` = module-manifest.md/01 §3.2-A · `retry.limit` 값·스코프 = config-schema.md §7 · Memory 백엔드 물리 실현 = memory-binding.md/04 §4. 본 문서는 이들의 **물리 실현**(루프 상태 기록 직렬화 형식·경로·`at`/`ref` 물리 표현·진입점 물리 해소·역할 실행/전이/사람 개입 물리 채널·Config 물리 소스)만 확정한다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형식(JSON Lines·JSON)·물리 경로(`framework/adapters/claude/loop-data/…`·`.claude/…`·`~/.claude/…`)·파일 확장자·세션/턴·서브에이전트 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. framework/loop/ 4문서는 이 토큰을 "Adapter Binding 문서 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(근거·경계 = 머리 거버넌스 절).
- 작성 시점 감사 서술(동시 작성 문서 불인용 07 R2·참조 정본 열거·추측 0 07 R4·산출 파일 범위 선언)은 종전 판 문면 = git 앵커 90ca19c.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-LB-1 (loop-data 하위 구조 = Worker 제안, Advisor 채택 대상 — 비차단).** DP-L4는 물리 **위치**를 확정했으나 그 **하위 구조**(사이클당 파일 1개·1 line = 1 전이 이벤트 append-log)는 §3.1의 **Worker 제안**이다(근거 (a)~(c)). 대안(교차 사이클 전역 append-log 1개 — memory-data/ index.jsonl 동형)도 계약을 위반하지 않으므로 채택 여부는 Advisor 판단 대상이며, 계약(03 §3.2-A) 변경이 아니므로 비차단이다. 시연 Task는 이 사이클당 파일 구조(`<cycle_id>.jsonl`)대로 loop-data/를 생성했다(앵커 cd9247b).
- **OQ-LB-2 (형태 B 경계 분할 — 비차단) — 해소됨 (형태 B Step Hosting 마일스톤, 2026-07-13).** 사이클 구동 연산 실행 코드(형태 B)의 `framework/loop/`·`framework/adapters/claude/` 간 분할이 확정·실현됐다 — 중립 사이클 구동 엔진 = `framework/loop/step-host/`(§4.1 예약 로케이터의 자리·provider 토큰 0)·provider 의존 호출 = `framework/adapters/claude/step-invoker/`·물리 매핑 = `step-hosting-binding.md`·계약 = `framework/runtime/step-hosting-protocol.md`. 계약(03 §3) 변경 0·형태 A 병존 유효(게이트·실증 경위 = §9 이력 2026-07-13 행).
