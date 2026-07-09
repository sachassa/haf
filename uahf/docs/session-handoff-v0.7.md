# UAHF Session Handoff — v0.7 → 다음 세션

작성일: 2026-07-06
작성자: Advisor (v0.7 세션)
목적: 이 문서만 읽어도 새 세션이 다음 마일스톤을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v0.6.md, v0.5, v0.4, v0.3, v0.2, v0.1)
상태: v0.7 Baseline (CP2 첫 판정 Pass 29/0/0 · CP3 승인 · 사용자 승인 2026-07-06). 사용자 승인 반영 완료 — Advisor가 v0.7 산출물 전건에 Baseline 행 append·상태 라인 승격을 수행하고 본 문서 이력에 기록했다.

이력:
| 2026-07-06 | 최초 작성 (사용자 승인 대기 상태) | Advisor |
| 2026-07-06 | v0.7 Baseline 확정 — 사용자 승인 반영 (상태 서술 전 지점 정합화) | Advisor |

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v0.7 — Workflow & Parallel Orchestration, Track C)

1. **세션 진입 절차 이행** — handoff v0.6 정독 → **Consult 실수행**(4회째 실가동: index.jsonl 39라인 스캔, 회수 집합 = Active Lesson 12건 L-01~L-12 + BP 3건 BP-01~BP-03, detail=index) → 정본 정독 → 운용 문서 정독.
2. **Execution Plan 수립** — Planner 초안(12 Task·8 Wave·OQ 10건) → Advisor 채택 + OQ 전건 해소(DP-W1~W5·파일 분할·충돌 시연·OQ-9 동형) → 사용자 승인 (2026-07-06, 계획 모드 — 사용자 결정 2건: **v0.7 단독**(v0.8 병행 없음)·**경미 정합 개정만 편입**(WF13~15 격리 Task 3건 추가 — 총 15 Task)).
3. **Wave 실행 (WF1~WF15)** — W1: work-graph(WF1, **공유 인터페이스** — BP-02)·Manifest(WF2)·편입 3건(WF13~15) 병렬 5종 → W2: decompose-rules·dispatch-protocol·merge-rules 병렬 3종(확정 WF1만 소비 — R2; 이 Wave 자체가 3-Task 병렬 집합 보조 실증) → W3: workflow-binding(WF6) → W4: 시연 절차서(WF7)·structure.md 트리(WF8) 병렬 → W5: 시연 실물(WF9) → W6: CP2(WF10) → W7: 승격 심사·등록(WF11) → W8: 본 핸드오프(WF12).
4. **시연 실물 수행 (모의 아님)** — 큰 작업 1건("용어 카드 3부작", 픽스처 자기완결)을 Decompose(Planner 초안 + Advisor C1~C4·D1·D2 대조 채택 — **Work Graph 인스턴스 실물**, docs/v0.7-demo.md §4.3) → **3 Task 한 병렬 집합 {wf-t1, wf-t2, wf-t3} 동시 디스패치**(서로 다른 Worker 서브에이전트, R1~R4) → **각 Task = Loop 사이클 실구동**(DP-W5 — loop-data `v07-demo-t1/t2/t3.jsonl` 각 7 line·rc=0·actor=human 0건·Consult ref 회수 집합 실기록 DP-L5) → **Task별 CP2 3건 전부 첫 판정 Pass**(verify-t1 3/0/0·t2 4/0/0·t3 4/0/0) → **Merge**(collected 3건 전건 Pass — INV-5 / crossRefStatus=Consistent / **충돌 1건 검출** — wf-t2 실현 A(등장 순) ↔ 확정 계약 Y 문면(가나다 순), 같은 계약을 다르게 실현 / **Advisor arbitration 3항 해소** — INV-6 / 병합 성립) → Learn→Memory Update(**append 5건** mi-0040~0044: BPD-03~06·LD-03, source=v0.7-demo-WF9 — DP-W6). WF9 내 실위임 9회(픽스처 1·Planner 1·Worker 3·Verifier 3·demo.md 1).
5. **검증 리포트** — docs/v0.7-verification-report.md: 항목 판정 29건, VT-5 독립 재현·재계산(loop-data 21 line 재파싱·Work Graph 재파싱·경계 쌍별 교집합 재계산·시연 CP2 3건 final_verdict 독립 재도출·회수 집합 2종 index 재도출·memory 5건 store↔index 정합), 07 §3 본문 AI 비의존 전수 스캔 0건(07 §7-⑥ CP2 직접 수행), 기존 Baseline 무변경 mtime 실측, 거짓 완료 보고 0건. **첫 판정 Pass (충족 29/위반 0/판정 불가 0) — v0.5·v0.6에 이어 3연속 첫 판정 통과.**
6. **Memory Update (실가동 4회차)** — 심사 docs/v0.7-promotion-review.md(승인 1: **L-13** / 보류 9: 시연 유래 5 + v0.6 유래 4 / 재발 판정 1: **Recurrence — L-08 매칭·회수됨**) → 물리 등록 mi-0045~0047. **store 47파일·index 47라인**, 기존 44건 무변경(append-only).

## 1.2 v0.7 완료 조건 대조 (ROADMAP)

| 완료 조건 | 판정 | 근거 |
|---|---|---|
| 3개 이상의 작업이 병렬로 수행되고 각각 검증까지 완료되는 Workflow 시연 | 충족 | 3 Task 한 병렬 집합 동시 디스패치 + Task별 CP2 3건 Pass + 병합 성립 (검증 리포트 — loop-data 21 line·verify-t1~t3 독립 재도출) |
| 작업 분해 결과에 완료 조건과 인터페이스 계약이 포함된다 | 충족 | Work Graph 실물 — 3 Task 전건 done·interfaceContract·ownedBoundary 보유 (WF1 포맷 강제 + WF3 C1·C2 검사 + CP2 재파싱 대조) |
| 병합 시 충돌 처리 규칙이 동작한다 | 충족 | 충돌 1건 검출 → Advisor arbitration 해소 → 병합 성립 (merge-rules §4 5단계 실기록 — demo.md §6, CP2 재확인) |

07 §7 시연 가능 문장 6건 + 검증 방법 5항목 전건 배정·충족 (demo-procedure §2 배정표 14건 — ⑥ AI 비의존은 CP2 직접 수행).

## 1.3 이번 세션의 설계 결정 (전부 확정·기록)

| 결정 | 내용 | 기록 위치 |
|---|---|---|
| **DP-W1** | `contract`=`WorkflowInterface`·`id`=`workflow-provider` (사전 명명 0건 실측, Glossary 어휘+관례 접미 — DP-L1·V1 동형) | module-manifest.md §5 |
| **DP-W2** | `requires`=**`LoopInterface` 단독** — 병합(INV-5)은 각 Task의 사이클 구동 완결을 요구(계약적 필수, 03 §2 dependents). Memory는 07 §5 조건부 소비(Verifier 선례 동형 제외), 역할 실행은 module Resolve 아님 | module-manifest.md §3·§5 |
| **DP-W3** | `configSchema` 생략 — 07 §3에 Workflow 소유 Config 소비 지점 부재 (DP-V2 동형·DP-L2와 근거 상이) | module-manifest.md §5 |
| **DP-W4** | Work Graph·Merge Result·Failure Report 직렬화 = **문서 형태(docs/ 시연 소산)** — 07 §4.1 행 1 정본 문면("계획·로드맵 문서")의 인스턴스(BP-03). **workflow-data/ 신설 없음**(DP-L4와 사실 관계 상이 — 03은 경로 개방·07은 문서 형태 지정) | workflow-binding.md §3 |
| **DP-W5** | 시연 병렬 Task를 Loop 사이클로 실구동 — loop-data `v07-demo-*.jsonl` append (07이 소비하는 단일 사이클 계약 실증) | demo-procedure §5.2·demo.md |
| **DP-W6** | 시연 Memory 입도 — per-task 성공 BP 후보 3건(BPD-03~05) + Workflow 수준 07 §5 Record 2건(BPD-06 분해·병합 패턴·LD-03 충돌 중재) = 5건 | demo.md §0·§8·promotion-review §1 |
| 파일 분할 | framework/workflow/ = 규격 4파일(ROADMAP 산출물 4종 1:1: work-graph·decompose-rules·dispatch-protocol·merge-rules) + Manifest 1. Failure Report는 work-graph.md 소유+각 연산 파일 § 포인터 | 계획 승인 |
| 충돌 시연 | 픽스처 1건 — 두 Task가 같은 계약 Y를 다르게 실현(T2 등장 순 ↔ 확정 문면 가나다 순) → Merge 단계 3 검출 → 중재 해소. 음성 케이스 비시연(07 §7 요구 없음) | demo-procedure §4.3 |
| OQ-WB-1 채택 | 시연 소산 물리 구조(Work Graph·Merge Result = 시연 문서 내 구조화 섹션) Advisor 채택 | workflow-binding §3.2·demo-procedure §5 |
| WF3 D1 해석 | 병렬 집합 상호 비의존 위반 = 재도출 대상(새 reason 신설 0 — 정본 열거 보존). 07 well-formedness reason 커버리지 보강 여부는 차기 후보 | decompose-rules §4·§1.6-6 |
| WF5 보수 처리 | CrossReferenceMismatch 사후 재병합 루프 비창설 — 중재 소관까지만 기술, 재시도 오케스트레이션은 상위 소관 포인터 | merge-rules §4.2·§5.2 |
| WF13 OQ 판정 | loop-binding §2 정본 인용 열의 참조 앞 공백 = house-style 수용(무실질·v0.6 CP2 기승인 문면). done(1)은 의미 토큰 단위 일치로 해석 | WF13 보고·§1.6-5 |
| 편입 3건 | v0.6 CP2 관찰 2·3·4 + criteria-catalog "병기" 용례 해소 (WF13~15) — Glossary 개정·reason 형식화는 이월 | **사용자 결정 (2026-07-06)** |
| v0.8 병행 없음 | v0.7 단독 수행 | **사용자 결정 (2026-07-06)** |

## 1.4 검증 게이트 실동작 기록

- **마일스톤 수준**: 실 서브에이전트 위임 총 22회(Planner 2·Worker 16·Verifier 4) + 재개정 라우팅 4회(WF15 r2·WF14 r2·WF13 r2·WF13 r3 — 전부 기존 에이전트 재개·Advisor 지시·정상 폐합). 거짓 완료 보고 0건. **CP2 첫 판정 Pass(29/0/0) — 재작업 0회, 3연속.**
- **시연 수준(실물)**: WF9 실위임 9회. Task별 CP2 3회(전부 첫 판정 Pass — 기대 경로). 사람 개입 0건(21 line 전건 actor ∈ {Advisor, Worker, Verifier}).
- **r2×3+r3 사례**: 편입 개정 3건의 상태 라인·이력 라벨 관례 처리 편차 — Advisor 위임문의 관례 기대 문면 미명시가 원인. **Advisor 소관 결함으로 기록 → L-13 등록·재발 판정 Recurrence(L-08 매칭·회수됨)**. Wave 4(WF8)부터 위임문 선반영으로 재개정 0회(예방 실증).
- **성공 요인**: BP-02(공유 인터페이스 WF1 선행 Wave 격리) 재실증 + BP-03(DP-W4 — 07 §4.1 문면 인스턴스 해소) 재실증.

## 1.5 Lesson·BP — 정식 등록 경로 처리 완료

- **L-13 Active** (mi-0045/0047): 기존 Baseline 문서의 개정 위임에는 상태 라인·이력 행 라벨의 기대 문면을 done/constraints에 명시 — 관례 의존 지시는 수임자마다 갈린다 (재발 판정 mi-0046: verdict=**Recurrence**, matched=L-08, was_recalled=true — 회수 이력은 세션 회수 기록에서 수동 도출, 세션 자체는 루프 상태 기록 미구동).
- **Active 집합: Lesson 13건(L-01~L-13)·BP 3건(BP-01~BP-03)**, store 47파일·index 47라인.
- **보류 9건 (Candidate 유지)**: 시연 유래 v0.7 5건(BPD-03~06·LD-03) + v0.6 4건(LD-01·02·BPD-01·02) — 실무 동형 사례 발생 시 재상정 (promotion-review §2.3).

## 1.6 차기 개정 일괄 후보 (비차단 — 승계·신규)

1. **(승계)** Glossary 일괄 개정("Wave" 표제어 승격 등) + config-schema.md 경미 어휘 정리 — Frozen 버전 상승 사안.
2. **(승계)** 06 연산 실패 보고 reason 형식화 여부 관찰.
3. **(승계)** v0.6 CP2 관찰 1(verify-a.md 계수 표기 — 시연 산출물, 기록만). ※ 관찰 2·3·4는 v0.7 편입 개정(WF13~15)으로 해소 완료.
4. **(신규 — v0.7 CP2 관찰 ⑵⑶⑷, verification-report §3.7)**: ⑵ loop-binding §2 정본 인용 열 참조 앞 공백 house-style byte 불일치(Advisor 수용 판정 — 기록만) ⑶ dispatch-protocol "세션" 어휘 3건 문언 정밀화 후보 ⑷ workflow-binding §7 "v0.7 시연 문서 미생성"의 시연 후 상태 반영(시점-스코프 기록 — v0.6 관찰 4 동형). ※ 관찰 ⑴(WF13 행 라벨)은 r3로 해소 완료.
5. **(신규)** v0.6 검증 리포트 §3.7-2 전제("나머지 6행 문자 단위 일치")의 byte 수준 부정확 — WF13 실측 발견, 기록만(리포트는 시점 기록·무수정).
6. **(신규)** 07 병렬 집합 well-formedness(상호 비의존 위반)의 Decompose reason 커버리지 보강 여부 — Frozen 07 버전 상승 사안 (WF3 관찰).
7. **(신규)** 시연 유래 Candidate 9건의 재상정·통합 심사 + Memory 등록 주체 관례(Advisor 직접) 재정렬 여부 (승계 관찰 유지).

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1~v0.6 완료(기준선). **v0.7 CP2 첫 판정 Pass(29/0/0)·CP3 Advisor 승인 — 사용자 승인 완료(2026-07-06)·Baseline 확정.** 이 승인으로 ROADMAP상 다음이 개방되었다: **v0.8 (Extension System, Track D — 마지막 병렬 트랙)** → v0.9 (Adapter Layer & Scaffold — 선행 v0.6 필수·v0.7/v0.8 완료 권장) → v1.0.

## 2.2 산출물 상태 (전부 v0.7 Baseline — 사용자 승인 2026-07-06 반영)

| 파일 | 내용 | 비고 |
|---|---|---|
| `framework/workflow/work-graph.md` | Work Graph 5필드·Task 7필드·공통 Failure Report 4필드+reason 9종 인스턴스 (07 §3.2-A/B/E) | WF1 — 공유 인터페이스 |
| `framework/workflow/module-manifest.md` | Workflow Provider Manifest — `WorkflowInterface`(DP-W1)·requires=`LoopInterface`(DP-W2)·configSchema 생략(DP-W3) | WF2 |
| `framework/workflow/decompose-rules.md` | Decompose 연산 인스턴스 — C1~C4 검사·병렬 집합 도출 D1·D2 (07 §3.1-A) | WF3 |
| `framework/workflow/dispatch-protocol.md` | Dispatch 연산+R1~R4 인스턴스 — delegation-protocol §2.5와 소유 구분 (07 §3.1-B·§3.2-C) | WF4 |
| `framework/workflow/merge-rules.md` | Merge 연산+Merge Result 4필드+충돌 처리 5단계 인스턴스 (07 §3.1-C·§3.2-D) | WF5 |
| `framework/adapters/claude/workflow-binding.md` | 07 §4.1 7행 물리 실현 — DP-W4(문서 형태·workflow-data 미신설)·SP1~4·실측 대조 | WF6 |
| `docs/v0.7-demo-procedure.md` | 시연 절차·배정 14건·기대 기록 명세·픽스처 명세 | WF7 |
| `framework/core/structure.md` (개정) | §8 트리 v0.7 실측 반영 (workflow/ 5문서·workflow-binding) | WF8 |
| `framework/adapters/claude/loop-binding.md` (개정) | v0.6 관찰 2·4 해소 (인용 1어 복원·loop-data 실재 반영) | WF13 (r2·r3) |
| `framework/memory/lessons.md` (개정) | v0.6 관찰 3 해소 (05 INV-4 주해 귀속 3분리) | WF14 (r2) |
| `framework/verifier/criteria-catalog.md` (개정) | §4 "병기" 용례 실표기 정합 | WF15 (r2) |
| `docs/v0.7-demo.md` + `docs/v0.7-demo-fixtures/` (9파일) | 시연 수행 기록(Work Graph·Merge Result 실물 수록) + 픽스처·산출물·Task별 CP2 리포트 3건 (격리 경계) | WF9 |
| `framework/adapters/claude/loop-data/` (+3파일·21 line) | `v07-demo-t1/t2/t3.jsonl` — 총 6파일 48 line (기존 3파일 무변경) | WF9, append-only |
| `framework/adapters/claude/memory-data/` | **store 47파일·index 47라인** (+8: 시연 5 + 심사 등록 3) — L-13 Active | WF9·WF11, append-only |
| `docs/v0.7-verification-report.md` | CP2 — 첫 판정 Pass 29/0/0, VT-5 독립 재현·재계산 | WF10 |
| `docs/v0.7-promotion-review.md` | 승격 심사 (승인 1/보류 9 + 재발 판정 Recurrence) | WF11 |
| Frozen specs 16개(TEMPLATE 포함)·v0.3~v0.6 Baseline 여타 산출물 | 무변경 (CP2 mtime 실측) | |

## 2.3 하네스 상태

**Bootstrap 유지** (13 §3.2-B). **Memory Service 실가동 4세션째** — Consult·Memory Update 전체 사이클 + 재발 판정 실사용. **Verifier 실가동 3세션째** — CP2 3연속 첫 판정 Pass + 시연 Task별 CP2 3회. **Loop 실가동 2세션째** — 시연 3사이클이 loop-protocol §3 오케스트레이션·loop-data 기록·Consult ref 회수 집합 기록을 그대로 사용(v0.6 계약의 첫 소비 실증). **Workflow는 이제 계약 인스턴스(5문서)·물리 바인딩·실물 구동 기록(Work Graph·병렬 디스패치·병합·충돌 중재)이 전부 실재한다** — 차기 세션은 큰 작업 분해 시 decompose-rules C1~C4·D1·D2, 디스패치 시 dispatch-protocol R1~R4, 병합 시 merge-rules 5단계를 계약 인스턴스로 그대로 사용할 수 있다. 형태 B(무인 실행 코드)는 로드맵대로 v0.9 전후 사안.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙 (사용자 결정 사안)

ROADMAP §4: v0.7 승인 완료로 남은 트랙은 **v0.8 (Extension System, Track D)** 하나다 (선행 조건 v0.3뿐 — 즉시 착수 가능). v0.8 완료 후 v0.9 (Adapter Layer & Scaffold — v0.7·v0.8 완료 권장 조건 충족).

## 3.2 v0.8 목표·완료 조건 (ROADMAP — Extension System)

Hooks(이벤트 확장점)·Skills(재사용 작업 능력)·Plugins(기능 묶음 배포 단위) 3종 구축: Hook·Skill·Plugin 각 1개씩 서드파티 형태 추가만으로 동작 확장 시연 / 본체 코드·규격 수정 없이 확장 완료 / 각 규격이 specs/08·09·10과 일치. 산출물: Hooks 규격+이벤트 카탈로그+레퍼런스 Hook 1 / Skills 규격+레퍼런스 Skill 1 / Plugins 규격+매니페스트 포맷+레퍼런스 Plugin 1. 실현 경계: framework/plugins/ (경계만 확보·빈 디렉터리 — structure.md §8 실측). 정본: specs/08-hooks.md·09-skills.md·10-plugins.md. **병렬성 높음** — 3 서브시스템 상호 독립·완전 병렬 개발 가능.

## 3.3 Memory 실사용 (모든 차기 세션 공통 — 갱신)

1. **Consult**: 착수 전 memory-binding.md §3.2로 회수. **Active 집합: Lesson 13건(L-01~L-13 — L-13 신규)·BP 3건(BP-01~BP-03)**, store 47파일·index 47라인. 시연 유래 Candidate 9건(LD-/BPD-)은 status=Active 필터에서 자연 제외.
2. **Memory Update**: Register Candidate + Advisor 승격 심사. append-only.
3. 재발 판정: was_recalled 입력은 Consult 전이 ref(사이클 구동 시) 또는 세션 회수 기록 수동 제공.

## 3.4 이월 사항

- §1.6 차기 개정 일괄 후보 7건.
- DP-4 재상정(v0.9 전후): Record 원자성(OQ-M5-2), 형태 B 코드 물리 분할(OQ-VB-2·OQ-LB-2·OQ-WB-2).
- 13 §3.2-B 전이 조건 재판정·Adapter Interface 정식화 — v0.9 (승계).

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — v0.8 가정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v0.7 (Workflow & Parallel Orchestration)이 완료되었다.
이번 세션의 목표는 ROADMAP v0.8 (Extension System, Track D — Hooks·Skills·Plugins)이다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v0.7.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md §3.2
   절차로 Active Lesson(13건: L-01~L-13)·BP(3건: BP-01~BP-03)를 목적·최소 범위로 회수하고
   회수 집합을 기록한다.
3. ARCHITECTURE.md(0.2), ROADMAP.md v0.8 섹션, specs/08-hooks.md·specs/09-skills.md·
   specs/10-plugins.md, framework/core/structure.md(§8 트리 — plugins/ 경계),
   framework/workflow/ 5문서와 framework/adapters/claude/workflow-binding.md(큰 작업
   분해·병렬 디스패치·병합 시 그대로 사용할 계약 인스턴스 — 3 서브시스템 병렬 개발에 적용),
   docs/v0.7-verification-report.md·docs/v0.7-demo.md(Workflow 실물 실증)를 정독한다.
4. .claude/AGENT.md, .claude/agents/ 4종, docs/delegation-protocol.md,
   docs/verification-checklist.md를 읽는다.
5. v0.8 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v0.7 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D) + framework/verifier/ 규격, 구현 Worker(Opus) 위임,
완료 보고 불신·독립 검증, Frozen spec 변경은 버전 상승+Revision History,
Architecture-Spec 충돌은 사용자 보고, C-1~C-3(+Module 구현 디렉터리 C-3 확장) 전 산출물 적용.
위임문의 산출물 본문 문안(L-11)과 존재 전제(L-12)는 발신 전 실측 대조하고,
기존 Baseline 문서의 개정 위임에는 상태 라인·이력 행 라벨의 기대 문면을 명시한다 (L-13).
Frozen 미명세 지점은 정본 문면 인스턴스로 해소하고 결정 기록으로 명문화한다 (BP-03).
큰 작업 분해·병렬 디스패치·병합은 framework/workflow/ 계약 인스턴스(C1~C4·R1~R4·5단계)를 사용한다.
세션 종료 시 Memory Update — Register Candidate + Advisor 승격 심사.
```

---

# 5. 주의사항

1. **물리 store·loop-data는 append-only다** (04 INV-6·03 INV-3) — memory-data/ 47파일·index 47라인, loop-data/ 6파일 48 line 수정·삭제 금지. 갱신은 새 레코드/새 전이 이벤트로만.
2. **§9 이력 행은 시점 기록** — 문면 불변, append만 (L-10). 단, 같은 세션에 자신이 append한 행의 교정은 위반 아님 (v0.7 r2/r3 판정 선례).
3. **개정 시 전 지점 전수 갱신** (L-06) + **상태·시각 서술은 실측 후** (L-07·L-09) + **위임문 문안·존재 전제 사전 대조** (L-11·L-12) + **개정 위임의 상태 라인·라벨 기대 문면 명시** (L-13).
4. **승격 권한 Advisor 전속** (05 INV-4) — Active 승격 레코드는 승인 참조를 content에 자기완결 첨부.
5. **Module 구현 디렉터리 문서 본문에 특정 Adapter 문서명·물리 토큰 금지** (C-3 확장).
6. **픽스처 경계** — docs/v0.5-demo-fixtures/·v0.6-demo-fixtures/·**v0.7-demo-fixtures/**는 의도적 결함 정당 보유 격리 지점. 전수 스캔 시 제외 명시 (verifier_scope 관례).
7. **C-2 실효는 형태 B(v0.9 전후) 시점** — Module 구현 디렉터리에 실행 코드를 두는 결정은 아직 없다.
8. **시연 기록의 성격** — v0.7 시연의 충돌(wf-t2 실현 A ↔ 확정 Y 문면)은 픽스처가 의도적으로 유도한 정당 보유물이며, out-t2.md의 "계약 이탈 실현"은 실계약 결함이 아니다 (arbitration 기록으로 해소 완료 — 후속 조치 불요).
