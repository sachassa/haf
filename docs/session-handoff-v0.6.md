# UAHF Session Handoff — v0.6 → 다음 세션

작성일: 2026-07-06
작성자: Advisor (v0.6 세션)
목적: 이 문서만 읽어도 새 세션이 다음 마일스톤을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v0.5.md, v0.4, v0.3, v0.2, v0.1)
상태: v0.6 Baseline (CP2 첫 판정 Pass 29/0/0 · CP3 승인 · 사용자 승인 2026-07-06). 사용자 승인 반영 완료 — Advisor가 v0.6 산출물 전건에 Baseline 행 append·상태 라인 승격을 수행하고 본 문서 이력에 기록했다.

이력:
| 2026-07-06 | 최초 작성 (사용자 승인 대기 상태) | Advisor |
| 2026-07-06 | v0.6 Baseline 확정 — 사용자 승인 반영 (상태 서술 전 지점 정합화) | Advisor |

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v0.6 — Loop Engine, 통합점)

1. **세션 진입 절차 이행** — handoff v0.5 정독 → **Consult 실수행**(3회째 실가동: index.jsonl 30라인 스캔, 회수 집합 = Active Lesson 11건 L-01~L-11 + BP 2건, detail=index) → 정본 정독 → 운용 문서 정독.
2. **Execution Plan 수립** — Planner 초안(13 Task·7 Wave·OQ 9건) → Advisor 채택 + OQ 전건 해소(DP-L1~L5·OQ-6~9) → 사용자 승인 (2026-07-06, 계획 모드 — 사용자 결정 2건: 이월 후보 경미 3건 편입·v0.8 병행 없음). 실행 중 L14(structure.md §8 트리) 격리 Task 1건 추가(총 14 Task).
3. **Wave 실행 (L1~L14)** — W1: loop-state-record(L1, **공유 인터페이스** — BP-02)·Manifest(L2)·편입 3건(L3~L5) 병렬 5종 → W2: stage-transition-rules(L6)·loop-protocol(L7) 병렬(확정 L1만 소비 — R2) → W3: loop-binding(L8) → W4: 시연 절차서(L9)·structure.md 트리(L14) 병렬 → W5: 시연 실물 3사이클(L10) → W6: CP2(L11) → W7: 승격 심사·등록(L12)·본 핸드오프(L13).
4. **시연 3사이클 실물 수행 (모의 아님 — Planner·Worker·Verifier 실제 서브에이전트 위임)** — ⓐ 정상 사이클(7전이·retry_count=0·actor=human 0건·CP2 첫 판정 Pass·CP3 후 완료 보고) / ⓑ 재작업 루프(9전이·CP2 Fail→재작업 지시 4필드→Execute 되돌림 rc=1→재판정 Pass — 03 §8 예2 실증) / ⓒ 한도 초과 에스컬레이션(11전이·CP2 Fail 3회 ②↔③ 진동·되돌림 결정 rc=3 > retry.limit 2·종료 전 Learn→Memory Update(INV-5)·**사용자 실개입 1회**(03 §3.1-D 조건 1)·to_stage=에스컬레이션·완료 보고 미생성 — 03 §8 예3 실증). 루프 상태 기록 실물 = `framework/adapters/claude/loop-data/` 3파일(27 line). Learn 실생성 = mi-0031~0034(LD-/BPD- 시연 네임스페이스, source=v0.6-demo-L10). **회수 이력 자동 기록 실증** — 각 사이클 Consult 전이 `ref`에 회수 집합(mi-id 배열) 실기록(DP-L5 — 05 §9 이연 해소).
5. **검증 리포트** — docs/v0.6-verification-report.md: 항목 판정 29건, VT-5 독립 재현·재계산(loop-data 27 line 재파싱·rc 재계산·시연 CP2 리포트 6건 final_verdict 독립 재도출·회수 집합 재도출), VT-4 후보 5부류 전수 스캔(+03 §3 본문 AI 비의존 — 03 §7-⑦), 거짓 완료 보고 0건. **첫 판정 Pass (충족 29/위반 0/판정 불가 0) — v0.5에 이어 2연속 재작업 0회 첫 판정 통과.**
6. **Memory Update (실가동 3회차)** — 심사 docs/v0.6-promotion-review.md(승인 2/보류 4 + 재발 판정 1) → 물리 등록 mi-0035~0039. store 39파일·index 39라인, 기존 34건 무변경(append-only), INV-7 전수 대조 diff 0.

## 1.2 v0.6 완료 조건 대조 (ROADMAP)

| 완료 조건 | 판정 | 근거 |
|---|---|---|
| 단일 작업이 사람 개입 최소로 전체 Lifecycle 통과 | 충족 | 시연 ⓐ — 7전이·actor=human 0건·rc=0·Complete (검증 리포트 — loop-data 독립 파싱) |
| 루프의 각 단계 전이가 기록으로 남는다 | 충족 | loop-data 3파일 27 line — seq 단조·append-only·기록만으로 3사이클 재구성(CP2 독립 재현) |
| Verify 실패 시 재작업 루프가 동작한다 | 충족 | 시연 ⓑ(되돌림 rc 0→1·재판정 Pass)·ⓒ(되돌림 2회·rc 1·2·3·초과 3>2 재계산) |
| Learn 단계에서 Lesson이 실제로 생성된다 | 충족 | LD-01(mi-0032)·LD-02(mi-0034) 실기록 — ⓒ는 종료 전 Learn(INV-5) 실증 |

03 §7 시연 가능 문장 7건 + 검증 방법 5항목 전건 배정·충족 (demo-procedure §2 배정표 16건 — ⑦ AI 비의존은 CP2 직접 수행).

## 1.3 이번 세션의 설계 결정 (전부 확정·기록)

| 결정 | 내용 | 기록 위치 |
|---|---|---|
| **DP-L1** | Loop Provider `id`=`loop-provider`·`contract`=`LoopInterface` (사전 명명 0건 실측, Glossary 어휘+관례 접미, "Engine" 배제) | module-manifest.md §5 |
| **DP-L2** | `configSchema` 생략 — `retry.limit`은 config-schema.md §7 소유 Framework 수준 키(소유 이중화 방지) | module-manifest.md §5 |
| **DP-L3** | "오케스트레이션 규격·구현물"의 형태 A 해석 = 규격 + 실물 사이클 구동 시연. 무인 실행 코드는 형태 B 이연 | loop-protocol.md §6 |
| **DP-L4** | 루프 상태 기록 물리 위치 = `framework/adapters/claude/loop-data/` + 사이클당 파일 1개(`<cycle_id>.jsonl`, 1 line=1 전이 이벤트 — OQ-LB-1 채택) | loop-binding.md §3 |
| **DP-L5** | 03 §3.2-A `ref` 괄호 열거 = 예시(비한정) — Consult 전이 `ref`에 회수 집합 참조 기록(03 확장 0, 04/05 §9 소관 배정의 해소 지점) | loop-state-record.md §6 |
| OQ-6 | Manifest `requires`=`MemoryServiceInterface` (Memory Update 필수 단계 — Verifier 선례와 사실 관계 상이; 역할 실행은 requires 아님) | module-manifest.md §3·§5 (Advisor 확인) |
| OQ-7 | 시연 = Advisor 주관 구동 + Worker/Verifier 실위임 (모의 금지 — L-07) | demo-procedure §6 |
| OQ-8 | 예3 actor=human = 사용자 실개입 1회(확인 응답) — §3.1-D 조건 1 정당 개입 | demo-procedure §11·demo.md |
| OQ-9 | 시연 Memory 기록 = 정식 memory-data append + `source` 시연 유래 표기(v0.4 선례 동형) + 시연 네임스페이스 LD-/BPD-(회수 오염 방지 — Advisor 확인) | demo-procedure §5·promotion-review |
| L9 OQ-1 | 에스컬레이션 종료 전이 `to_stage`="에스컬레이션" — 03 §3.1-A Memory Update 행 실패 경로 전이 목적지의 인스턴스(신설 아님) | demo-procedure §12.2 |
| L9 OQ-2 | 한도 초과 표기 = 되돌림 결정 시점 rc 증가(3차 Fail 시 rc=3) — 초과 조건이 기록 필드로 참(03 §7 재구성 요건) | demo-procedure §12.2 |
| 이월 후보 편입 | handoff v0.5 §1.6 중 경미 3건(②③④) 편입 — L3·L4·L5 격리 Task. ①Glossary·⑤reason 형식화는 이월 유지 | **사용자 결정 (2026-07-06)** |
| v0.8 병행 없음 | v0.6 단독 수행 | **사용자 결정 (2026-07-06)** |
| 파일 분할 | framework/loop/ = 규격 3파일(state-record·transition-rules·protocol — ROADMAP 산출물 3종 1:1) + Manifest 1파일 | 계획 승인 |
| 등록 주체 이탈 | L12 물리 등록을 Advisor가 직접 수행(근거 기록 — 관례 재정렬 여부 차기 판단) | promotion-review §5 |

## 1.4 검증 게이트 실동작 기록

- **마일스톤 수준**: 위임 총 14 Task + 재개정 라우팅 2회(기존 에이전트 재개 — L3 r2·L9 r2, 둘 다 Advisor 지시·정상 폐합). 거짓 완료 보고 0건. **CP2 첫 판정 Pass(29/0/0) — 재작업 0회.**
- **시연 사이클 수준(실물)**: 서브에이전트 실위임 16회(Planner 3·Worker 6·Verifier 6·demo.md 1) + 픽스처 준비 1. CP2 판정 6회(Pass 2·Fail 4 — 전부 기대 경로). 사람 개입 1회(ⓒ — 조건 1 정당).
- **L3 r1 검출 사례**: Advisor 위임문의 존재 전제(이력 절)가 대상 실상과 불일치 — Worker 실측 검출·에스컬레이션(02 O4 정상 동작) → r2 재개정. **Advisor 소관 결함으로 기록 → L-12 등록·재발 판정 Recurrence(L-07 매칭·회수됨)** — L-07 계열 3연속 재발이므로 게이트 A에 "done 존재 전제 실측 대조"를 관행 추가.
- **성공 요인**: BP-02(공유 인터페이스 L1 선행 Wave 확정) 재실증 + BP-03(Frozen 미명세 지점의 정본 문면 인스턴스 해소 — 신규 등록).

## 1.5 Lesson·BP — 정식 등록 경로 처리 완료

- **L-12 Active** (mi-0035/0038): 위임 done의 존재 전제는 발신 전 실측 대조 — 위임문의 존재 전제도 실측 대상 (L3 r1 사례. 재발 판정 mi-0036: verdict=**Recurrence**, matched=L-07, was_recalled=true — 회수 이력은 이번까지 수동 제공, 차기부터 Consult 전이 `ref` 도출 가능).
- **BP-03 Active** (mi-0037/0039): Frozen 미명세 지점은 정본 자신의 문면이 지정하는 값의 인스턴스로 해소 + 결정 기록 명문화 (DP-L5·OQ-1·OQ-2 실증).
- **보류 4건 (Candidate 유지)**: LD-01·LD-02·BPD-01·BPD-02 — 시연 유래(픽스처 기반), 실무 동형 사례 발생 시 재상정 (promotion-review §3).
- **오기 정정**: handoff v0.5 §3.4·§4의 "Active Lesson 12건(L-01~L-11)"은 실측상 **11건**이었다(stable_id 11개 — 본 세션 Consult 실측). 현재는 L-12 추가로 **12건이 맞다**.

## 1.6 차기 개정 일괄 후보 (비차단 — 승계·신규)

1. **(승계)** Glossary 일괄 개정("Wave" 표제어 승격 등) + config-schema.md 경미 어휘 정리 — Frozen 버전 상승 사안.
2. **(승계)** 06 연산 실패 보고 reason 형식화 여부 관찰.
3. **(신규 — CP2 관찰 4건, v0.6-verification-report §3.7)**: ⑴ verify-a.md 계수 표기 오차(시연 산출물 — 기록만) ⑵ loop-binding.md §2 행 2 정본 인용 1어 탈락 ⑶ lessons.md의 05 INV-4 괄호 주해 어휘 정밀화 ⑷ loop-binding.md §7 "loop-data 미생성"의 시연 후 상태 반영(v0.5 관찰 2 동형 — 시점-스코프 기록이라 비위반).
4. **(신규)** criteria-catalog.md §4 "병기" 용례 정밀화 여부 (L4 관찰 — 개념 대응 표현이라 비차단).
5. **(신규)** 시연 유래 Candidate 4건의 재상정·통합 심사 (promotion-review §3).
6. **(신규)** Memory 등록 주체 관례(Advisor 직접 vs Worker) 재정렬 여부 (promotion-review §5).

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1~v0.5 완료(기준선). **v0.6 CP2 첫 판정 Pass(29/0/0)·CP3 Advisor 승인 완료 — 사용자 승인 완료(2026-07-06)·Baseline 확정.** 이 승인으로 ROADMAP상 다음이 개방되었다: **{v0.7 (Workflow & Parallel Orchestration, Track C) ∥ v0.8 (Extension System, Track D)}** — v0.6 → {v0.7 ∥ v0.8(완료)} → v0.9 → v1.0.

## 2.2 산출물 상태 (전부 v0.6 Baseline — 사용자 승인 2026-07-06 반영)

| 파일 | 내용 | 비고 |
|---|---|---|
| `framework/loop/loop-state-record.md` | 루프 상태 기록 포맷 인스턴스 (03 §3.2-A/B/C) + 회수 이력 기록(DP-L5) | L1 — 공유 인터페이스 |
| `framework/loop/module-manifest.md` | Loop Provider Manifest — `LoopInterface`(DP-L1)·requires=`MemoryServiceInterface`·configSchema 생략(DP-L2) | L2 |
| `framework/loop/stage-transition-rules.md` | 03 §3.1-A 7단계·게이트-단계 매핑 인스턴스 | L6 |
| `framework/loop/loop-protocol.md` | 03 §3.1 사이클 구동 오케스트레이션 + 재작업 루프 + 이연 해소 4건 + DP-L3 | L7 |
| `framework/adapters/claude/loop-binding.md` | 03 §4.1 7행 물리 실현 — loop-data/ 정본(DP-L4)·SP-1~5·실측 대조 | L8 |
| `docs/verification-checklist.md` (개정) | §7 verifier-binding §5 상호 참조 + 이력 절 신설 (편입 ②) | L3 r2 |
| `framework/verifier/criteria-catalog.md` (개정) | §2.1 VT-2 문언 정밀화 (편입 ③) | L4 |
| `framework/memory/lessons.md` (개정) | 승격 승인 참조 content 자기완결 관례 명시 (편입 ④) | L5 |
| `framework/core/structure.md` (개정) | §8 트리 v0.6 실측 반영 (loop/ 4문서·loop-binding) | L14 |
| `docs/v0.6-demo-procedure.md` | 시연 3종 절차·배정 16건·픽스처 명세·L9 OQ-1/OQ-2 결정 기록 | L9 r2 |
| `docs/v0.6-demo.md` + `docs/v0.6-demo-fixtures/` (12파일) | 시연 수행 기록 + 픽스처·output·시연 CP2 리포트 6건 (격리 경계) | L10 |
| `framework/adapters/claude/loop-data/` (3파일·27 line) | **루프 상태 기록 실물** — v06-demo-a(7)·b(9)·c(11) | L10, append-only |
| `framework/adapters/claude/memory-data/` | store 39파일·index 39라인 (+9: 시연 4 + 심사 등록 5) — L-12·BP-03 Active | L10·L12, append-only |
| `docs/v0.6-verification-report.md` | CP2 — 첫 판정 Pass 29/0/0, VT-5 독립 재현·재계산 | L11 |
| `docs/v0.6-promotion-review.md` | 승격 심사 (승인 2/보류 4 + 재발 판정 Recurrence) | L12 |
| Frozen specs 16개(TEMPLATE 포함)·v0.3~v0.5 Baseline 여타 산출물 | 무변경 (CP2 실측 — mtime 타임라인·memory-data 기존분 불변) | |

## 2.3 하네스 상태

**Bootstrap 유지** (13 §3.2-B). **Memory Service 실가동 3세션째** — Consult·Memory Update 전체 사이클 + 재발 판정 3분류 실사용. **Verifier 실가동 2세션째** — CP2 2연속 첫 판정 Pass + 시연 사이클 CP2 6회 실판정. **Loop는 이제 계약 인스턴스·물리 바인딩·실물 구동 기록(3사이클)이 전부 실재한다** — 차기 세션은 사이클 구동 시 loop-protocol §3 오케스트레이션·loop-data 기록·Consult `ref` 회수 집합 기록을 그대로 사용할 수 있다(회수 이력 수동 제공 종료 가능). 형태 B(무인 실행 코드)는 로드맵대로 v0.9 전후 사안.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙 선택 (사용자 결정 사안)

ROADMAP §4: v0.6 승인으로 {v0.7 (Workflow) ∥ v0.8 (Extension System)}가 개방되었다. **권장: v0.7** — Loop(단일 사이클)를 다중 사이클 분해·병렬 디스패치·병합으로 확장하는 다음 통합 단계이며 v0.9의 선행 권장 조건. v0.8은 상호 독립(선행 v0.3뿐)이라 병행·선행 모두 가능.

## 3.2 v0.7 목표·완료 조건 (ROADMAP — Workflow & Parallel Orchestration)

큰 작업 분해·병렬 디스패치·결과 병합: 3개 이상 작업 병렬 수행+각각 검증 완료 시연 / 분해 결과에 완료 조건·인터페이스 계약 포함 / 병합 충돌 처리 규칙 동작. 산출물: Workflow 정의 포맷 / 작업 분해 규칙 / 병렬 디스패치 프로토콜 / 병합·충돌 처리 규칙. 실현 경계: framework/workflow/ (경계 확보됨·빈 디렉터리). 정본: specs/07-workflow.md.

## 3.3 v0.7 참고 (v0.6에서 마련된 것)

- 07의 Work Graph·R1~R4는 이미 세션 관행으로 실사용 중(delegation-protocol §2.5) — v0.7은 이를 계약 인스턴스로 정식화.
- Loop 사이클(03)이 실물로 실재 — 07의 "여러 Loop 사이클의 분해·병렬 디스패치·병합"이 소비할 단일 사이클 계약·기록 포맷·물리 백엔드가 전부 확정됨.
- Module 경계 관례 4회 확립(memory/·verifier/·loop/): manifest+규격 인스턴스+바인딩. framework/workflow/도 동형 예상. BP-03(Frozen 미명세 지점 해소 방식) 적용 가능.

## 3.4 Memory 실사용 (모든 차기 세션 공통 — 갱신)

1. **Consult**: 착수 전 memory-binding.md §3.2로 회수. **Active 집합: Lesson 12건(L-01~L-12 — L-12 신규)·BP 3건(BP-01~BP-03 — BP-03 신규)**, store 39파일·index 39라인. 시연 유래 Candidate 4건(LD-/BPD-)은 승격 전이므로 status=Active 필터에서 자연 제외된다.
2. **Memory Update**: Register Candidate + Advisor 승격 심사(promotion-review 관례). append-only.
3. 재발 판정: Judge Recurrence 3분류 — **was_recalled 입력은 이제 Consult 전이 이벤트 `ref`(DP-L5)에서 도출 가능** (세션 자체를 루프 상태 기록으로 구동하는 경우; 아니면 세션 회수 기록 수동 제공).

## 3.5 이월 사항

- §1.6 차기 개정 일괄 후보 6건.
- DP-4 재상정(v0.9 전후): Record 원자성(OQ-M5-2), 형태 B 코드 물리 분할(OQ-VB-2·OQ-LB-2).
- 13 §3.2-B 전이 조건 재판정·Adapter Interface 정식화 — v0.9 (승계).

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — v0.7 가정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v0.6 (Loop Engine — 통합점)이 완료되었다.
이번 세션의 목표는 ROADMAP v0.7 (Workflow & Parallel Orchestration, Track C)이다.
(v0.8 Extension System과 병렬 개방 — 트랙 선택·병행 여부는 사용자 결정.)

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v0.6.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md §3.2
   절차로 Active Lesson(12건: L-01~L-12)·BP(3건: BP-01~BP-03)를 목적·최소 범위로 회수하고
   회수 집합을 기록한다.
3. ARCHITECTURE.md(0.2), ROADMAP.md v0.7 섹션, specs/07-workflow.md,
   framework/core/structure.md(§8 트리 — workflow/ 경계), framework/loop/ 4문서와
   framework/adapters/claude/loop-binding.md(다중 사이클이 소비할 단일 사이클 계약),
   docs/v0.6-verification-report.md·docs/v0.6-demo.md(Loop 실물 실증)를 정독한다.
4. .claude/AGENT.md, .claude/agents/ 4종, docs/delegation-protocol.md,
   docs/verification-checklist.md를 읽는다.
5. v0.7 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v0.6 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D) + framework/verifier/ 규격, 구현 Worker(Opus) 위임,
완료 보고 불신·독립 검증, Frozen spec 변경은 버전 상승+Revision History,
Architecture-Spec 충돌은 사용자 보고, C-1~C-3(+Module 구현 디렉터리 C-3 확장) 전 산출물 적용.
위임문의 산출물 본문 문안(L-11)과 존재 전제(L-12)는 발신 전 실측 대조한다.
Frozen 미명세 지점은 정본 문면 인스턴스로 해소하고 결정 기록으로 명문화한다 (BP-03).
세션 종료 시 Memory Update — Register Candidate + Advisor 승격 심사.
```

---

# 5. 주의사항

1. **물리 store·loop-data는 append-only다** (04 INV-6·03 INV-3) — memory-data/ 기존 39파일·index 39라인, loop-data/ 기존 3파일 27 line 수정·삭제 금지. 갱신은 새 레코드/새 전이 이벤트로만.
2. **§9 이력 행은 시점 기록** — 문면 불변, append만. 재검증 전칭 기준은 라이브 본문에만 (L-10, rework-instruction §4).
3. **개정 시 전 지점 전수 갱신** (L-06) + **상태·시각 서술은 실측 후** (L-07·L-09 — timestamp·at은 순서 값) + **위임문의 문안·존재 전제 사전 대조** (L-11·L-12).
4. **승격 권한 Advisor 전속** (05 INV-4) — Active 승격 레코드는 승인 참조를 content에 자기완결 첨부 (lessons.md §3.2 관례, v0.6 편입 ④).
5. **Module 구현 디렉터리 문서 본문에 특정 Adapter 문서명·물리 토큰 금지** (C-3 확장·L-11).
6. **픽스처 경계** — docs/v0.5-demo-fixtures/·docs/v0.6-demo-fixtures/는 의도적 결함 정당 보유 격리 지점. 전수 스캔 시 제외 명시 (verifier_scope 관례).
7. **C-2 실효는 형태 B(v0.9 전후) 시점** — Module 구현 디렉터리에 실행 코드를 두는 결정은 아직 없다.
8. **에스컬레이션 종료 사이클(v06-demo-c)은 "사람 승인 대기" 상태로 종료된 시연 기록**이다 — 실계약 미완 작업이 아니며 후속 조치 불요 (시연 목적 달성).
