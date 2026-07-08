# UAHF Session Handoff — v0.8 → 다음 세션

작성일: 2026-07-06
작성자: Worker (Advisor 위임, Task EX-M2)
목적: 이 문서만 읽어도 새 세션이 다음 마일스톤을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v0.7.md, v0.6, v0.5, v0.4, v0.3, v0.2, v0.1)
상태: v0.8 Baseline (CP2 첫 판정 Pass 29/0/0 · CP3 승인 · 사용자 승인 2026-07-06). 사용자 승인 반영 완료 — Advisor가 v0.8 산출물 전건에 Baseline 행 append·상태 라인 승격을 수행하고 본 문서 이력에 기록했다.

---

## §9. 이력 (Revision History)

| 일자 | 변경 | 주체 |
|---|---|---|
| 2026-07-06 | 최초 작성 (사용자 승인 대기 상태) | Advisor 위임 — Worker (Task EX-M2) |
| 2026-07-06 | v0.8 Baseline 확정 — 사용자 승인 반영 (상태 서술 전 지점 정합화) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행(v0.8 verification-report·promotion-review·demo 동형). 이후 개정은 이 표에 append-only로 기록한다. 사용자 승인 반영은 별도 행으로 append한다.)

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v0.8 — Extension System, Track D — Hooks·Skills·Plugins)

1. **세션 진입 절차 이행** — handoff v0.7 정독 → **Consult 실수행(5회째 실가동)**: index.jsonl 47라인 스캔, 회수 집합 = Active Lesson 13건(L-01~L-13) + BP 3건(BP-01~BP-03), detail=index → 정본·운용 문서 정독 → **착수 전 실측**(01 §4.1 문면·확장 표면 빈 디렉터리·plugins/ 빈 경계·사전 명명 0건).
2. **Execution Plan 수립** — Planner 초안(14 Task·8 Wave·OQ 9건) → **Advisor 채택**(C1~C4·D1·D2 통과)·OQ 전건 해소 → **사용자 승인**(2026-07-06, 계획 모드 — 사용자 결정 2건: **DP-E1 Frozen 무변경 배치**·**경미 정합만 편입**).
3. **Wave 실행 (W1~W8 + EX-R3)** —
   - **W1**: hooks-binding(EX-H1, r2 1회)·skills-binding(EX-S1)·framework/plugins/ 3문서(EX-P1) — 병렬 3종.
   - **W2**: plugins-binding(EX-P2)·격리 개정 2종(EX-R1 dispatch-protocol "세션" 어휘 중립화·EX-R2 workflow-binding §7 실재 반영 + OQ-WB-1 해소) — 병렬 3종.
   - **W3**: structure.md §8 개정(EX-C1)·시연 절차서(EX-D1 — 배정표 40건) — 병렬.
   - **W4**: **시연 병렬 집합 PS-4**(EX-DH·EX-DS·EX-DP — **3 Worker 동시 디스패치**·Loop 사이클 실구동·Task별 CP2 3건 전부 첫 판정 Pass(verify-h 8/0/0·verify-s 11/0/0·verify-p 12/0/0)·**Merge 성립**: collected 3/3·crossRefStatus=Consistent·**conflicts 0 → merge-rules §4.4 단계 4 생략 분기 첫 실증**).
   - **W5**: 시연 수행 기록(EX-D2).
   - **W6**: 마일스톤 CP2(EX-V1).
   - **W7**: 승격 심사(EX-M1).
   - **W8**: 본 핸드오프(EX-M2).
   - **+ EX-R3**(사용자 지시 편입 — 아래 DP-E8): planner.md=Worker 개정·verifier.md=권한 차단으로 Advisor 직접 수정.
4. **검증 리포트** — docs/v0.8-verification-report.md: **첫 판정 Pass 29/0/0 (v0.5부터 4연속)**, VT-5 독립 재현·정적 판정 직접 수행·본체 무변경 실측·거짓 완료 보고 0건·비차단 관찰 4건(§3.7).
5. **Memory Update 실가동 5회차** — 시연 유래 append 4건(mi-0048~0051 = BPD-07~10) + 심사 등록 5건(mi-0052~0056): **L-14 Active 승격·재발 판정 Recurrence(L-06 매칭·회수됨)·BP-04 Candidate 보류·BPD-06 재상정 Active 승격**(§2.3 실무 동형 조건 — v0.8 실행 자체가 그 사례). **store 56파일·index 56라인**, 기존 51건 무변경(append-only).

## 1.2 v0.8 완료 조건 대조 (ROADMAP — 전건 충족, EX-V1 근거)

| 완료 조건 | 판정 | 근거 |
|---|---|---|
| Hook·Skill·Plugin 각 1개 서드파티 추가만으로 동작 확장 시연 | 충족 | F-H1(`.claude/hooks/audit-complete/`)·F-S1(`.claude/skills/commit-message-writer/`)·F-P1(report-exporter bundle, Install·Activate·**Remove 수명주기 완주**) (verification-report items #2·#5·#26~#28) |
| 본체 코드·규격 수정 0으로 확장 완료 | 충족 | mtime 타임라인 실측 — v0.8 쓰기 창(15:15~17:12) 수정 파일이 선언 산출물과 1:1·무단 산출 0·framework/plugins/ 3문서 md5 무변경 (items #3·#16·#17) |
| 각 규격이 specs/08·09·10과 일치 | 충족 | 셀 단위 대조 — 08 §4.1 5행·09 §4.1 7행·10 §3.1 4연산·§3.2-A 6필드·§3.2-B reason 11종·§4.1 8행, 재정의·새 필드·새 reason 0 (items #4·#9~#12) |

산출물 3종 충족(EX-V1 item #5): Hooks 규격+이벤트 카탈로그(08 §3.2-A 18행)+F-H1 / Skills 규격+F-S1 / Plugins 규격+매니페스트 포맷(plugin-manifest.md)+F-P1.

## 1.3 이번 세션의 설계 결정 (전부 확정·기록)

| 결정 | 내용 | 상태 |
|---|---|---|
| **DP-E1** | 물리 배치 — framework/hooks\|skills/ 미신설·규격=바인딩 2종+확장 표면 실물·Plugins=framework/plugins/ | **사용자 승인** |
| **DP-E2** | 레퍼런스 Plugin=독립 Module 번들 — report-exporter·ReportExporterInterface(10 §8 예1 값) | 확정 |
| **DP-E3** | settings.json 비접촉 — 실행 훅 선언 형태 B 구분 | 확정 |
| **DP-E4** | 시연 = 마일스톤 병렬 집합 PS-4 그 자체 — Workflow 계약의 실무 소비 | 확정 |
| **DP-E5** | Plugins Provider — PluginsInterface·id=plugins-provider·requires 없음·configSchema 생략 | 확정 |
| **DP-E6** | bundle 원본 = 픽스처 경계 존치·설치본 = framework/plugins/&lt;id&gt;/·Remove 잔여물 0 | 확정 |
| **DP-E7** | 라이브 표면 위생 — 정상 레퍼런스만 존치·결함 픽스처 격리 | 확정 |
| **DP-E8** | **사용자 결정 — Verifier·Planner 실행 모델 Opus 명시.** `.claude/agents/verifier.md`·`planner.md` frontmatter `model: opus` 개정, **v1.0 완료까지 영구 관행**. 동기: Fable 주간 한도 절약. 06 계약은 모델 비의존 — **계약 변경 아님**(02 §4.1 Adapter Binding 영역·SP-3). EX-R3로 반영: planner.md=Worker 개정·verifier.md=권한 차단으로 Advisor 직접 수정(사용자 직접 지시 권한 경로) | **사용자 결정 (2026-07-06)** |

**OQ 해소 8건**: OQ-4(18행 매핑 정직 구분)·OQ-5(재사용 모사 재현)·OQ-6(충돌 유도 없음 — conflicts 0)·OQ-SB-1(skill 하위 디렉터리)·OQ-EH2(hook 자기완결 경계)·OQ-EXDH-2(contract=HookModule 값)·OQ-DP-1(형태 A granularity)·OQ-DP-2(관측 기록 존치).

## 1.4 검증 게이트 실동작 기록

- **마일스톤 수준**: 실서브에이전트 위임 총 **17회**(Planner 1·Worker 12·Verifier 4) + 재개정 라우팅 1회(EX-H1 r2 — 계수 표기, 게이트 C 검출) + **EX-R3 권한 차단 1회**(Worker 우회 부작위·정직 반환 → Advisor 직접 수정 — L-14·BP-04 유래). 거짓 완료 보고 0건. **CP2 첫 판정 Pass 29/0/0 — v0.5부터 4연속.**
- **시연 수준(실물)**: PS-4 실위임 7회(Worker 3·Verifier 3·기록 1). actor=human **0건**(21 line 전건 actor ∈ {Advisor, Worker, Verifier}).
- **EX-H1 r1 결함**: 같은 유지 목록을 §6은 "5항"·§10 요약은 "6항"으로 계수(같은 상태 서술 문서 내 두 지점 갈림) → Advisor 게이트 C 검출 → r2 교정 폐합 → **재발 판정 Recurrence(matched L-06·was_recalled=true)**.
- **EX-R3 권한 차단**: verifier.md 개정이 권한 시스템 [Self-Modification] 거부로 차단(planner.md는 통과 — 판정 편차 관측). **Worker가 셸 우회를 시도하지 않고 실패 보고(blocking)로 정직 반환**, Advisor가 사용자 직접 지시 근거로 직접 수정 완결 → **L-14 Active 승격·BP-04 Candidate 등록**.

## 1.5 Lesson·BP — 정식 등록 경로 처리 완료

- **Active 집합: Lesson 14건(L-01~L-14)·Best Practice 4건(BP-01·BP-02·BP-03·BPD-06)**, store 56파일·index 56라인.
- **L-14 Active**(mi-0052 Candidate → mi-0054 Active, supersedes mi-0052): Agent 기동 설정 파일(.claude/agents/ 이하)의 개정은 Worker 위임 권한만으로 권한 시스템에 차단될 수 있다 — 승인 근거가 위임 메시지가 아니라 **사용자 본인의 지시**여야 하는 부류. 사용자 직접 지시 근거로 주 세션(Advisor)이 직접 수행하거나, 착수 전 권한 경로를 확보한 뒤 위임한다.
- **BPD-06 재상정 Active 승격**(mi-0056, supersedes v0.7 Candidate mi-0043): 계약을 분해 시점에 확정하고 소유 경계를 파일 단위로 분리하면 3개 이상 Task를 한 병렬 집합으로 동시 디스패치·개별 검증·병합할 수 있다. **v0.8 실행 자체**가 v0.7-promotion-review §2.3 재상정 조건(실무 동형 사례)의 충족 — 승격 근거.
- **재발 판정 Recurrence**(mi-0053, matched L-06, was_recalled=true): L-06은 Active 유지(강화·supersede 없음 — 회수 성립·교정 폐합).
- **BP-04 Candidate 보류**(mi-0055): 권한 시스템 거부는 우회하지 않고 차단 보고로 반환, 해소는 권한 소유자 경로로. 실무 동형 재발 시 재상정.
- **보류 Candidate 13건**: LD-01·02·03 · BPD-01~05 · BPD-07~10 · BP-04 — status=Candidate 필터로 Active 회수에서 자연 제외.

## 1.6 차기 개정 일괄 후보 (비차단 — 승계 + 신규)

**(승계)**

1. Glossary 일괄 개정("Wave" 표제어 승격 등) — Frozen 버전 상승 사안.
2. 06 연산 실패 보고 reason 형식화 여부.
3. 기록만 사안 3건 승계 관찰.
4. 07 병렬 집합 well-formedness(상호 비의존 위반) Decompose reason 커버리지 보강 여부.
5. Memory 등록 주체 관례(Advisor 직접) 재정렬 여부.

**(신규 — v0.8 CP2 §3.7 비차단 관찰 4건)**

6. binding·절차서·수행 기록의 시점-스코프 "미생성" 스냅샷 4곳(plugins-binding §7·hooks-binding §7·demo-procedure §0·verify-p §5) — 시연 후 상태(실재/Remove 잔여물 0) 반영 후보(기록만·라이브 모순 아님).
7. F-H1 manifest `contract: HookModule` 인스턴스 값의 정본화 여부(08 버전 상승 사안 관찰 — CP3 거버넌스 항목, item #26 판정 불변).
8. EX-DH 관측 기록(ex-dh-observations.md)이 시연 창 내 동시 변경 열거에서 verifier.md(16:34) 누락 — verify-h 투명 플래그(기록만·판정 불변).
9. memory timestamp 필드 값(2026-07-05T22:20:3x)과 물리 mtime(2026-07-06 16:57) 불일치 = 생성기 배정 순서 값 정합 신호(L-09, 기록만).
10. **(본 핸드오프 착수 실측 발견)** Frozen spec 계수 편차 — 아래 §2.2 주 참조.

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1~v0.7 완료(기준선). **v0.8 CP2 첫 판정 Pass(29/0/0)·CP3 Advisor 승인 대기 — 사용자 승인 대기(Draft).** v0.8 승인 시 ROADMAP상 남은 트랙은 하나다: **v0.9 (Adapter Layer & Scaffold)** → v1.0.
- v0.8은 Track D(Extension System — 마지막 병렬 트랙)의 완료다. v0.4·v0.5·v0.7·v0.8 트랙이 전건 폐합되어 v0.9 선행 조건(v0.6 필수·v0.7·v0.8 완료 권장)이 전부 충족됐다.

## 2.2 산출물 상태 (전부 v0.8 Draft — 사용자 승인 대기)

**신규**

| 파일 | 내용 | 비고 |
|---|---|---|
| `framework/adapters/claude/hooks-binding.md` | 08 §4.1 5행 물리 실현·Hook Binding 6필드·순서 08 §3.1-D 3단·§3 계측 매핑 18행 | EX-H1 (r2 1회) |
| `framework/adapters/claude/skills-binding.md` | 09 §4.1 7행 재현·Skill Manifest 11필드·로드 계층·8사유 코드 | EX-S1 |
| `framework/plugins/module-manifest.md` | Plugins Provider — PluginsInterface·id=plugins-provider·requires/configSchema 미선언(DP-E5) | EX-P1 |
| `framework/plugins/plugin-manifest.md` | Plugin Manifest 6필드·Failure Report reason 11종(10 §3.2-A/B) | EX-P1 |
| `framework/plugins/plugin-lifecycle.md` | 수명주기 검사 I1~I5·A1~A2·D1·R1~R2·IG ↔ reason 1:1(10 §3.1) | EX-P1 |
| `framework/adapters/claude/plugins-binding.md` | 10 §4.1 8행 정본 인용·bundle 원본/설치본/Remove 잔여물 0 | EX-P2 |
| `docs/v0.8-demo-procedure.md` | 시연 절차·배정표 40건·기대 기록 명세·픽스처 명세·PS-4 Work Graph 인스턴스 | EX-D1 |
| `docs/v0.8-demo.md` | 시연 수행 기록(Work Graph·Merge Result 실물·loop-data 21 line 원문·CP2 3건 요지) | EX-D2 |
| `docs/v0.8-demo-fixtures/` | 픽스처(f-h2/h3/h4·F-S2/F-S3·mock-context 2·report-exporter bundle 3 등) + 관측 기록 3(ex-dh/ds/dp) + CP2 리포트 3(verify-h/s/p) — 격리 경계(DP-E7) | EX-DH·EX-DS·EX-DP |
| `.claude/hooks/audit-complete/` (F-H1: manifest.md·audit.sh) | 라이브 표면 정상 레퍼런스 Hook — event=lifecycle.complete@after·order 0 | EX-DH |
| `.claude/skills/commit-message-writer/SKILL.md` (F-S1) | 라이브 표면 정상 레퍼런스 Skill — front-matter 9 메타데이터·body 하드코딩 0 | EX-DS |
| `docs/v0.8-verification-report.md` | CP2 — 첫 판정 Pass 29/0/0·VT-5 독립 재현·정적 판정 직접 수행·비차단 관찰 4건 | EX-V1 |
| `docs/v0.8-promotion-review.md` | 승격 심사 — 승인 1(L-14)·재상정 승격 1(BPD-06)·재발 판정 1(L-06)·신규 Candidate 1(BP-04)·보류 13 | EX-M1 |
| `docs/session-handoff-v0.8.md` | 본 핸드오프 | EX-M2 |

**개정**

| 파일 | 개정 내용 | 비고 |
|---|---|---|
| `framework/workflow/dispatch-protocol.md` | v0.7 §3.7-⑶ "세션" 어휘 중립화(본문 잔여 0·§9 이력 행에만 경위 기록) | EX-R1 |
| `framework/adapters/claude/workflow-binding.md` | v0.7 §3.7-⑷ "시연 문서 미생성"→실재 반영 + OQ-WB-1 해소 | EX-R2 |
| `framework/core/structure.md` | §8 트리·§2/§4/§5에 framework/plugins/ 3문서·확장 바인딩 3문서 반영(plugins "미실현"→"실사용 v0.8") | EX-C1 |
| `.claude/agents/planner.md` | frontmatter `model: opus` 명시(DP-E8) — Worker 개정 | EX-R3 |
| `.claude/agents/verifier.md` | frontmatter `model: opus` 명시(DP-E8) — **권한 차단으로 Advisor 직접 수정** | EX-R3 |

**물리 데이터 (append-only)**

| 대상 | 상태(착수 실측) | 비고 |
|---|---|---|
| `framework/adapters/claude/loop-data/` | +3파일 21 line(v08-demo-h/s/p.jsonl 각 7) — **총 9파일 69 line**(기존 6파일 48 line 무변경) | EX-D2, 실측 대조 완료 |
| `framework/adapters/claude/memory-data/` | store **56파일**(mi-0001~0056)·index **56라인** — 기존 51건 무변경 + 신규 5건(mi-0052~0056) | EX-M1, store↔index 1:1·무결번 실측 |

**무변경 (EX-V1 실측)**

- Frozen specs(TEMPLATE 포함)·v0.3~v0.7 Baseline 여타 산출물 — mtime 타임라인 실측(v0.8 창 밖).
- ※ **착수 실측 주(비차단 §1.6-10)**: `specs/*.md` 물리 파일 = **15개**(numbered 00–13 = 14 + TEMPLATE 1). 이전 baseline(v0.7 §2.2 "16개(TEMPLATE 포함)")·EX-V1 리포트 item #16 표기 "Frozen specs 16종"과 **1건 편차**. 무변경 판정 자체(mtime v0.8 창 밖)는 유효하며, 편차는 계수 표기 사안이다(예: ARCHITECTURE.md를 spec 계수에 포함하는지 여부 등 — 추측 없이 Advisor 재확인 대상, open_questions).

## 2.3 하네스 상태

**Bootstrap 유지**(13 §3.2-B). **Memory Service 실가동 5세션째** — Consult·Memory Update 전체 사이클 + 재발 판정 + 재상정 승격 실사용. **Verifier 실가동 4세션째** — CP2 4연속 첫 판정 Pass + 시연 Task별 CP2 3회 + **DP-E8 Opus 명시**. **Loop 실가동 3세션째** — 시연 3사이클이 loop-protocol 오케스트레이션·loop-data 기록·Consult ref 회수 집합 기록을 그대로 사용. **Workflow 첫 실무 소비** — v0.8 마일스톤 실행 자체가 분해·병렬 디스패치·병합 계약의 실무 소비였다(BPD-06 Active 승격 근거).

**Extension System 실재**: Hooks/Skills/Plugins 규격(specs/08·09·10 Frozen 인스턴스)·물리 바인딩 3문서·framework/plugins/ 3문서·레퍼런스(F-H1·F-S1·F-P1)·시연 전건이 실재한다. **확장 표면 실사용** — F-S1 배치 직후 라이브 하네스가 `commit-message-writer`를 발견 가능 능력으로 표면화한 것이 등록 표면 실동작의 부수 실증이다(DP-E7 위생 결정의 방증). 차기 세션은 Hook·Skill·Plugin을 추가만으로 확장할 수 있다. 형태 B(실행 훅 선언·무인 실행 코드)는 v0.9 전후 사안.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙

ROADMAP §4: v0.8 승인 완료로 남은 트랙은 **v0.9 (Adapter Layer & Scaffold)** 하나다. 선행 조건 v0.6(필수)·v0.7·v0.8(완료 권장 — Adapter가 감싸야 할 표면 확정)이 전부 충족됐다.

## 3.2 v0.9 목표·완료 조건 (ROADMAP — Adapter Layer & Scaffold)

- **목표**: Adapter Layer 정식화 — v0.2~v0.8 동안 Claude에 직접 바인딩된 부분을 모두 Adapter 규격 뒤로 이동. Scaffold(신규 프로젝트 부트스트랩)·Presentation 최소 기능 구축.
- **완료 조건**: ① Adapter Interface 최종 확정 ② Core에 Claude 의존 요소 0건(경계 검증) ③ 새 프로젝트에 Scaffold로 UAHF 설치·루프 동작 시연 ④ Spec versioning·하위호환 규칙 문서화.
- **산출물**: adapters/claude/ 완성본·Adapter Interface 최종 규격·Scaffold 도구와 프로젝트 템플릿·Presentation 최소 기능·신규 프로젝트 설치 가이드·Spec versioning 정책 문서.
- **정본**: specs/11-adapters.md·specs/12-scaffold.md(Frozen 실재 확인). specs/13-harness.md §3.2-B(전이 조건).
- **병렬성 높음** — Adapter 정식화 / Scaffold / Presentation 3개 병렬 트랙, Adapter Interface 확정(직렬)만 선행.

## 3.3 Memory 실사용 (모든 차기 세션 공통 — 갱신)

1. **Consult**: 착수 전 memory-binding.md §3.2로 회수. **Active 집합: Lesson 14건(L-01~L-14 — L-14 신규)·Best Practice 4건(BP-01~BP-03 + BPD-06 신규 Active)**, store 56파일·index 56라인. Candidate 13건(LD-/BPD-/BP-04)은 status 필터에서 자연 제외.
2. **Memory Update**: Register Candidate + Advisor 승격 심사. append-only.
3. 재발 판정: was_recalled 입력은 Consult 전이 ref(사이클 구동 시) 또는 세션 회수 기록 수동 제공.

## 3.4 이월 사항

- §1.6 차기 개정 일괄 후보 10건(승계 5 + 신규 5).
- DP-4 재상정(v0.9 전후 — 형태 B 물리 분할): Record 원자성(OQ-M5-2), 형태 B 코드 물리 분할(OQ-VB-2·OQ-LB-2·OQ-WB-2).
- 13 §3.2-B 전이 조건 재판정·Adapter Interface 정식화 — v0.9.
- §2.2 Frozen spec 계수 편차(§1.6-10) 재확인.

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — v0.9 가정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v0.8 (Extension System — Hooks·Skills·Plugins)이 완료되었다.
이번 세션의 목표는 ROADMAP v0.9 (Adapter Layer & Scaffold)이다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v0.8.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md §3.2
   절차로 Active Lesson(14건: L-01~L-14)·Best Practice(4건: BP-01~BP-03 + BPD-06)를
   목적·최소 범위로 회수하고 회수 집합을 기록한다.
3. ARCHITECTURE.md(0.2), ROADMAP.md v0.9 섹션, specs/11-adapters.md·specs/12-scaffold.md,
   specs/13-harness.md(§3.2-B 전이 조건), framework/core/structure.md(§8 트리),
   framework/adapters/claude/ 전체(v0.9가 정식화·이동시킬 바인딩 표면 — hooks/skills/
   plugins/workflow/loop/memory/verifier-binding),
   framework/workflow/ 5문서(큰 작업 분해·병렬 디스패치·병합 시 그대로 사용할 계약 인스턴스),
   docs/v0.8-verification-report.md·docs/v0.8-demo.md(Extension System 실물 실증)를 정독한다.
4. .claude/AGENT.md, .claude/agents/ 4종, docs/delegation-protocol.md,
   docs/verification-checklist.md를 읽는다.
5. v0.9 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v0.8 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D) + framework/verifier/ 규격, 구현 Worker(Opus) 위임,
완료 보고 불신·독립 검증, Frozen spec 변경은 버전 상승+Revision History,
Architecture-Spec 충돌은 사용자 보고, C-1~C-3(+Module 구현 디렉터리 C-3 확장) 전 산출물 적용.
위임문의 산출물 본문 문안(L-11)과 존재 전제(L-12)는 발신 전 실측 대조하고,
기존 Baseline 문서의 개정 위임에는 상태 라인·이력 행 라벨의 기대 문면을 명시한다 (L-13).
Agent 기동 설정(.claude/agents/ 이하)의 개정은 Worker 위임 권한만으로 차단될 수 있으므로
사용자 직접 지시 경로로 처리하거나 착수 전 권한 경로를 확보한다 (L-14).
Verifier·Planner 위임은 model opus를 명시한다 — v1.0 완료까지 영구 관행 (DP-E8).
Frozen 미명세 지점은 정본 문면 인스턴스로 해소하고 결정 기록으로 명문화한다 (BP-03).
큰 작업 분해·병렬 디스패치·병합은 framework/workflow/ 계약 인스턴스(C1~C4·R1~R4·5단계)와
확정 인터페이스 선행 Wave 배치(BP-02·BPD-06)를 사용한다.
세션 종료 시 Memory Update — Register Candidate + Advisor 승격 심사.
```

---

# 5. 주의사항

1. **물리 store·loop-data는 append-only다**(04 INV-6·03 INV-3) — memory-data/ **56파일·index 56라인**, loop-data/ **9파일 69 line** 수정·삭제 금지. 갱신은 새 레코드/새 전이 이벤트로만.
2. **§9 이력 행은 시점 기록** — 문면 불변, append만(L-10). 단, 같은 세션에 자신이 append한 행의 교정은 위반 아님(v0.7 r2/r3 판정 선례).
3. **개정 시 전 지점 전수 갱신**(L-06) + **상태·시각 서술은 실측 후**(L-07·L-09) + **위임문 문안·존재 전제 사전 대조**(L-11·L-12) + **개정 위임의 상태 라인·라벨 기대 문면 명시**(L-13). ※ EX-H1 r1(§6 "5항"↔§10 "6항")이 L-06 재발(Recurrence)로 판정됨 — 같은 상태 서술(계수·목록 항 수)의 전 지점 정합을 게이트 재확인 관행으로 유지.
4. **승격 권한 Advisor 전속**(05 INV-4) — Active 승격 레코드는 승인 참조를 content(`approval`)에 자기완결 첨부(mi-0054·mi-0056 실측).
5. **Module 구현 디렉터리 문서 본문에 특정 Adapter 문서명·물리 토큰 금지**(C-3 확장). framework/plugins/ 3문서도 이 경계 적용(EX-V1 item #15 매치 0 실측).
6. **픽스처 경계** — docs/v0.5-demo-fixtures/·v0.6-demo-fixtures/·v0.7-demo-fixtures/·**v0.8-demo-fixtures/**는 의도적 결함 정당 보유 격리 지점(f-h2-notify-fail·F-S2-violation-skill·F-S3-unselected-skill 등). 전수 스캔 시 제외 명시(verifier_scope 관례).
7. **C-2 실효는 형태 B(v0.9 전후) 시점** — Module 구현 디렉터리에 실행 코드를 두는 결정은 아직 없다. settings.json 실행 훅 선언(형태 B)은 DP-E3로 비접촉 유지.
8. **라이브 표면 위생(DP-E7)** — `.claude/hooks/`·`.claude/skills/`에는 **정상 레퍼런스만** 존치한다(F-H1·F-S1). 결함 픽스처(F-H2·F-S2 등)는 docs/v0.8-demo-fixtures/ 격리 경계에만 배치하며 라이브 표면에 두지 않는다.
9. **report-exporter 설치본은 Remove로 부재가 정상** — framework/plugins/ 현재 = module-manifest·plugin-manifest·plugin-lifecycle 3 md만(설치본 report-exporter/ 부재, Remove 잔여물 0). 재설치는 bundle 원본(docs/v0.8-demo-fixtures/report-exporter/)에서 한다.
10. **DP-E8 영구 관행** — Verifier·Planner 위임은 `model: opus` 명시. v1.0 완료까지 유지. 계약(06) 변경이 아니라 실행 모델 바인딩(02 §4.1)이다. Agent 기동 설정 개정은 사용자 직접 지시 권한 경로로만(L-14).
11. **시연 기록의 성격** — v0.8 시연은 conflicts 0(상호 독립 서브시스템)이 기대이자 관측이며 merge-rules §4.4 "0건 → 단계 4 생략" 분기의 첫 정합 인스턴스다(v0.7의 충돌 1건 검출·중재와 대비 — 둘 다 정당). memory timestamp·loop-data `at`은 순서 값이며 물리 벽시계 시각이 아니다(L-09).
12. **§2.2 Frozen spec 계수 편차(비차단, §1.6-10)** — 착수 실측 `specs/*.md` = 15파일이 baseline 표기 "16종"과 1건 다르다. "무변경" 판정(mtime)은 유효하나 계수 표기는 Advisor 재확인 대상이다(추측 없이 open_questions로 이관).
