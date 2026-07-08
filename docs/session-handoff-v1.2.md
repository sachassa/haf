# UAHF Session Handoff — v1.2 → 다음 세션

작성일: 2026-07-07
작성자: Worker (Advisor 위임, Task T-H)
목적: 이 문서만 읽어도 새 세션이 v1.2 이후 작업을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v1.1.md, v1.0, v0.9, v0.8, v0.7, v0.6, v0.5, v0.4, v0.3, v0.2, v0.1)
상태: v1.2 Baseline (CP2 첫 판정 Pass 16/0/0 — v0.5부터 8연속 · CP3 승인 · 사용자 승인 2026-07-07). 사용자 승인 반영 완료 — Advisor가 v1.2 산출물 전건(신규 문서 5 + docs 3 + 개정 3)에 Baseline 행 append·상태 라인 승격을 수행하고 본 문서 이력에 기록했다. 다음 트랙 = **미정** — 다음 세션에서 사용자 결정 (§3·§4 Bootstrap Prompt).

---

## §9. 이력 (Revision History)

| 일자 | 변경 | 주체 |
|---|---|---|
| 2026-07-07 | 최초 작성 (사용자 승인 대기 상태) | Worker (Advisor 위임, Task T-H) |
| 2026-07-07 | v1.2 Baseline 확정 — 사용자 승인 반영 (전 산출물 상태 라인 승격·Baseline 행 append: 신규 문서 5 + docs 3 + 개정 3). 다음 트랙 사용자 결정 = 미정(다음 세션 결정 — §4 Bootstrap Prompt 구조 유지) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행(v1.2 verification-report·promotion-review·v1.1 handoff 동형). 이후 개정은 이 표에 append-only로 기록한다. 사용자 승인 반영은 별도 행으로 append한다 — §5 Baseline 승격 절차 참조.)

---

# 1. 이번 세션 요약 — v1.2 (Project Discovery Implementation)

v1.2는 v1.1이 UAF 레벨에 **설계만** 한 Entry Architecture를 Claude Adapter 경계에 **형태 A(문서·데이터, 실행 코드 0)**로 물리화하고, Greenfield/Brownfield 두 경로를 실입력으로 완주해 검증한 **UAF 레벨 실현 트랙**이다. UAHF Core Component 트랙이 아니므로 ROADMAP #6 Principle Coverage·#7 Component Coverage에는 v1.2 행이 추가되지 않았다(v1.1 선례 동형).

1. **세션 진입.** handoff v1.1 정독 → **Consult 실수행(9회째)**: index 75라인 스캔·회수 Active 20건(L-01~L-15 · BP-01~03 · BPD-06 · BPD-11) detail=full · Candidate 20 자연 제외.

2. **트랙 채택.** v1.1 핸드오프에 기록된 사용자 결정(v1.2 = 후보 (a))을 재상정 없이 채택. 계획 = Planner(opus) 초안(스트림 중단 1회 → 재개 프로토콜로 결함 0 완결 — **BPD-13 실증**) → Advisor 검증·채택(OQ 6건 해소 DP-X1~X6) → **사용자 계획 승인 + 사용자 범위 결정 4건(D-v1.2-1~4)**:
   - ① **형태 A만**(실행 코드 0 · Bootstrap 유지 — v1.2 = Architecture End-to-End Validation, 형태 B는 후속 분리).
   - ② **UAHF 명시 개정 3건만**(ROADMAP · structure.md §8 · adapter-conformance 계수).
   - ③ **E2E = 신규 테스트 프로젝트(Greenfield) + 본 저장소(Brownfield dogfooding)**.
   - ④ **이월 유지**(02 §3.3-B Guard 예시 범위 밖).

3. **Wave 실행 (11 Task · 7 Wave).**
   - **W1** T-C contract-binding(r2 1회 — § 오귀속 교정)
   - **W2** T-E entry-binding + 진입 명령 2(첫 통과)
   - **W3** T-D discovery-binding(첫 통과) [바인딩 선형 사슬 — BP-02 선행 확정 · 07 R2]
   - **W4** T-XG ∥ T-XB E2E(주 세션 State Machine 규약 구동 · 사용자 게이트 G1/G2 실수행 · 두 경로 Ready 종단 · Contract 2건 컴파일)
   - **W5** T-R(r2 1회 — 절 명칭 정정) ∥ T-S ∥ T-A 명시 개정 3
   - **W6** T-V CP2(Verifier opus)
   - **W7** T-P 승격 심사 → T-H 본 핸드오프(직렬 — DP-W1 선례)

4. **E2E 실동작 (검증 중점 5건 전건 실증).**
   - **Brownfield r001** — 실관측(contract 무 · repo 유, 비git이나 기존 콘텐츠 실재) → 행 6(D3 ②) → T2 실 스캔 → G1 실 Q&A(Intent 실용화 지향 · Risk 2건 — 사용자 진술) → G2 승인 → pc-uahf-001(instanceVersion 1 · 가정 0) → T19 Ready, **30 Event**.
   - **Greenfield r002** — 빈 디렉터리 실관측(무 · 무) → 행 1(P-C) → 프레이밍 → G1 2라운드(uahf-quickstart CLI: 1명령 설치 진단 · 기능 4 · Python 단일 파일 · 리스크 2) → G2 승인 → pc-uahf-quickstart-001을 신규 프로젝트 `.claude/project-contract/`에 배치(Scaffold 소비 지점 (b) 실현) → T19 Ready, **29 Event** · Budget 5/40.
   - **UAHF 소비 (a)**: Advisor가 pc-uahf-001 Consult 소비(차기 세션 Consult 대상 등재 — §3).

5. **검증.** **CP2 첫 판정 Pass 16/0/0(v0.5부터 8연속)** — 완료 조건 10 + 상시 불변 2 + 거짓 완료 검출 + 존재 + 격리 + § 정합, Event 로그 ↔ 전이표 전수 대조 · Contract ↔ 스키마 대조 · 무수정 mtime 삼중 실측. **재작업 라우팅 2회**(T-C r2 · T-R r2 — 전부 Advisor 게이트 C/판정 검출·폐합) · **거짓 완료 0**.

6. **Memory Update (10회째).** 심사 등록 6건(mi-0076~0081):
   - **재발 판정 3건** — Novel 2(T-C r1 산출물 `contract-binding.md` 본문 § 오귀속 mi-0076 · T-R r1 산출물 `ROADMAP.md` v1.2 절 명칭 오지칭 mi-0077) / **Recurrence 1**(T-A input 자매 바인딩 문서 버전 상태 전제 3건 stale — matched **L-15**, mi-0078).
   - **승격 2건** — L-20 Candidate→Active(mi-0079, 재상정 — v1.2 동형 재발 2건 supersedes mi-0073) · BPD-13 Candidate→Active(mi-0080, 재상정 — Planner 중단 재개 실증 supersedes mi-0074).
   - **신규 Candidate 1** — BPD-14(mi-0081 — 형태 A 실동작 검증 패턴, 1회 발생 보류).
   - 기존 75건 MD5 바이트 무변경(append-only · 프리픽스 해시 실측 대조).

7. **Advisor 결정 DP-X1~X12** (전부 확정·기록):

| 결정 | 내용 |
|---|---|
| **DP-X1** | 명명 — `uaf-` 접두 명령 · 접두 없는 바인딩 · §0에서 UAF 정본 바인딩 구분 |
| **DP-X2** | Contract 저장 이원화 — `.claude/project-contract/`(일반 관례) · `discovery-data/contracts/uahf/`(본 저장소 dogfooding) |
| **DP-X3** | Greenfield 위치 — 저장소 내부(`discovery-data/e2e-greenfield-project/`) |
| **DP-X4** | conformance 자매 11 정정 + UAF 3종(바인딩) 구분 — 자매 계수 **비합산** |
| **DP-X5** | Policy 최소 실값 — θ 0.70~0.80 · Budget 40 · soft 30/hard 40 · 보충 10 |
| **DP-X6** | Provenance 분담 — 외형=contract-binding · 내부=discovery-binding |
| **DP-X7** | (= DP-X2 내 일반 관례 경로 수용) |
| **DP-X8** | Request 분담 — 형식·전달=entry-binding · 기록 위치=discovery-binding |
| **DP-X9** | (Policy 수치 수용 — OQ-TD-1) |
| **DP-X10** | run-id `r###` 순차 · `events.jsonl` 단일 append-log · 벽시계 시각 비기재(L-09) |
| **DP-X11** | structure.md §8 요약 bullet에 `uaf/specs` 미삽입(네임스페이스 구분) |
| **DP-X12** | conformance "아홉 번째" 서수 = 생성 시점 사실 유지 |

8. **이월 후보 처리.**
   - **해소** — v1.1 §1.6-b #3(conformance "자매 8문서" 계수) 해소(T-A) + 부수 해소(hooks·plugins·scaffold 버전 라벨 드리프트 실측 정정).
   - **승계** — Glossary 정합 · plugins-binding §7 크기 · 서수 표기 · Presentation 귀속 · uahf-status §9 · v0.8 승계 · 형태 B OQ 5건 + v1.1-a Guard 예시.
   - **신규 비차단 관찰(CP2)** — 바인딩 §10/§13 "미존재" 서술 = 작성 시점 스냅샷(향후 개정 시 시점 명기 유지 권고) · 진입 명령 §9 이력 부재(uahf-status 동형 관례).

---

# 2. 현재 프로젝트 상태

## 2.1 버전

v0.1~v1.1 완료(Baseline). **v1.2 CP2 Pass · CP3 승인 — 사용자 승인 대기(Draft).** ROADMAP에 v1.2 등재됨(v1.2 등재 Draft). v1.2 이후 트랙 미정(§3).

## 2.2 산출물 상태 (전부 v1.2 Draft — 사용자 승인 대기)

- **신규 문서 5** — 바인딩 3(`contract-binding.md` · `entry-binding.md` · `discovery-binding.md`) + 진입 명령 2(`.claude/commands/uaf-new.md` · `uaf-continue.md`).
- **E2E 데이터 7** — `discovery-data/`: events 2 run(brownfield-r001 30라인 · greenfield-r002 29라인) + discovery-request 2 + policy 1(`default-policy.yaml`) + Contract 2(`contracts/uahf/project-contract.v1.md` = pc-uahf-001 · `e2e-greenfield-project/.claude/project-contract/project-contract.v1.md` = pc-uahf-quickstart-001).
- **docs 3** — `v1.2-verification-report.md` · `v1.2-promotion-review.md` · 본 핸드오프.
- **개정 3** — ROADMAP("v1.2 등재 Draft") · structure.md §8("v1.2 Draft") · adapter-conformance("v1.2 Draft").
- **Memory append 6** — mi-0076~0081(store/index).

**산술 검산(L-15·mi-0078 준수 — 파생·합산 계수 검산 축).** store 75 + 6 = **81** · Active 20 + 2 = **22** · Candidate 20 − 2 + 1 = **19** · Event 30 + 29 = **59** · 신규 산출물 5(문서) + 7(데이터) + 3(docs) = **15**. 전 계수 산출물·Memory 실측 일치.

## 2.3 하네스 상태

**Bootstrap 유지** — v1.2도 형태 A(실행 코드 0), 전이 조건 3(Runtime 정식 Module 호스팅) 미충족 승계. **UAF 실현 상태**: uaf/ 정본 4문서의 §4 바인딩 지점 **11건 전부 형태 A 물리화 완료** · 본 저장소가 자신의 Project Contract(pc-uahf-001)를 보유한다.

## 2.4 Memory 심사 후 집합 (실측)

- store **81** · index **81** / kind: lesson **39** · best-practice **24** · recurrence-judgment **18**.
- **Active 22** = Lesson **16**(L-01~L-15 · **L-20**) + Best Practice **6**(BP-01 · BP-02 · BP-03 · BPD-06 · BPD-11 · **BPD-13**).
- **Candidate 19** = Lesson **7**(L-16~L-19 · LD-01~03) + Best Practice **12**(BP-04 · BPD-01~05 · BPD-07~10 · BPD-12 · **BPD-14**). status 필터로 Active 회수에서 자연 제외.
- loop-data **11파일 83라인 무변경**.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙 — 미정 (사용자 결정 필요)

ROADMAP은 v1.2를 마지막 등재 트랙으로 정의하며, v1.2 이후 트랙은 정의되어 있지 않다. 다음 세션의 트랙은 **사용자 결정 대상**이다. 이 핸드오프는 차기 트랙을 선취해 확정하지 않는다.

**후보(사용자 선택 대상 — 선취 아님):**

- **(a) 형태 B 실행 호스팅 · DP-4 재상정** — pc-uahf-001 Intent "실용화 지향"과 정합 · OQ 5건 재판정.
- **(b) uahf-quickstart CLI 구현** — pc-uahf-quickstart-001의 실현 · Contract→Execution 첫 실사례.
- **(c) 유지보수** — 이월 잔여 일괄(§3.3).
- **(d) 신규 로드맵** — 새 목표 트랙 정의.

## 3.2 Memory 실사용 (모든 차기 세션 공통 — 갱신)

1. **Consult**: 착수 전 memory-binding.md §3.2로 회수. **Active 22건**(Lesson 16 · BP 6) · store 81 · index 81. Candidate 19건은 status 필터에서 자연 제외.
2. **신규 Consult 대상**: 본 저장소 Project Contract(`framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v1.md`, pc-uahf-001)를 **프로젝트 정의 정본으로 착수 정독**한다(03 §3.5-B (a) 실소비 관행 — v1.2 확립).
3. **Memory Update**: Register Candidate + Advisor 승격 심사. append-only(신규 레코드/status 전이는 새 레코드로).

## 3.3 이월 사항

- **① 승계(§1-8 잔여)** — Glossary 0.2 인용 정합 · plugins-binding §7 크기 표기 · 서수 표기 · Presentation 귀속 · uahf-status §9 이력 절 · v0.8 승계 기록 · 형태 B/DP-4 재상정 OQ 5건(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2) · v1.1-a 02-discovery §3.3-B Guard 예시 문면(incremental·신규 mode 병기).
- **② 신규 비차단 관찰(CP2)** — 바인딩 §10/§13 "미존재" 서술 = 작성 시점 스냅샷(향후 개정 시 측정 시점 명기 유지 권고) · 진입 명령 §9 이력 부재(uahf-status 동형 관례).
- **③ 확장 포인트** — 형태 B 실행 호스팅 · Discovery의 Memory 활용 · UAHF 측 Contract 정식 등재(03 §3.5-C) · Contract 스키마 상세의 Adapter Binding 직렬화(논리 스키마만 v1.1 정본).

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — 다음 트랙 미정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v1.2 (Project Discovery Implementation)가 완료되었다 — v1.1이 UAF
레벨에 설계한 Entry Architecture를 Claude Adapter 경계에 형태 A(문서·데이터, 실행
코드 0)로 물리화하고(바인딩 3 + 진입 명령 2 + E2E 데이터), Greenfield/Brownfield 두
경로를 실입력으로 완주해 검증 중점 5건을 실동작 검증했다. UAHF 정본은 명시 개정 3건
(ROADMAP·structure.md §8·adapter-conformance 계수)에 한정해 개정됐고, 그 외 UAHF·
uaf/ 정본은 무수정이다. 하네스는 Bootstrap 유지(형태 A). v1.2 이후 트랙은 ROADMAP에
정의되어 있지 않다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v1.2.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md
   §3.2 절차로 Active Lesson(16건: L-01~L-15 + L-20)·Best Practice(6건: BP-01~03 +
   BPD-06 + BPD-11 + BPD-13) = 22건을 목적·최소 범위로 회수하고 회수 집합을 기록한다
   (store 81파일·index 81라인. Candidate 19건은 status 필터로 자연 제외).
   추가 Consult 대상 — 본 저장소 Project Contract를 프로젝트 정의 정본으로 착수 정독한다:
   framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v1.md
   (pc-uahf-001 — 03 §3.5-B (a) 실소비 관행, v1.2 확립).
3. 다음 트랙을 스스로 채택하지 말고 사용자에게 결정을 요청한다.
   ROADMAP v1.2까지 등재된 트랙이 완료되었으므로 다음 트랙은 미정이다. 후보를 제시하되
   (a) 형태 B 실행 호스팅 도입·DP-4 재상정(pc-uahf-001 Intent "실용화 지향"과 정합·OQ 5건 재판정)
   (b) uahf-quickstart CLI 구현(pc-uahf-quickstart-001 실현·Contract→Execution 첫 실사례)
   (c) 유지보수 운용(이월 잔여 일괄 정리)
   (d) 신규 로드맵
   채택은 사용자 결정 사항이다. 차기 트랙을 선취해 착수하지 않는다.
4. 사용자가 트랙을 결정하면, 필요한 정본을 정독하고
   (ARCHITECTURE.md, ROADMAP.md, 관련 specs, framework/adapters/ 바인딩,
   framework/core/structure.md, 직전 검증·승격 리포트,
   uaf/ 정본 4문서: uaf/ARCHITECTURE.md·uaf/specs/01-entry.md·uaf/specs/02-discovery.md·
   uaf/specs/03-project-contract.md,
   v1.2 바인딩 3: framework/adapters/claude/contract-binding.md·entry-binding.md·discovery-binding.md,
   진입 명령 2: .claude/commands/uaf-new.md·uaf-continue.md),
   .claude/AGENT.md·.claude/agents/ 4종·docs/delegation-protocol.md·
   docs/verification-checklist.md를 읽고, 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v1.2 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D) + framework/verifier/ 규격, 구현 Worker(Opus) 위임,
완료 보고 불신·독립 검증, Frozen spec 변경은 버전 상승+Revision History,
Architecture-Spec 충돌은 사용자 보고, C-1~C-3 전 산출물 적용.
Core Claude 의존 0건은 유지 대상이며 2nd Adapter 이후 산출물은 그 Adapter 경계에만 격리한다.
uaf/ 정본 4문서 본문은 특정 AI 실명·모델명·제품 기능명 0(C-3 동형) — 물리 실현은
Adapter Binding 소관이며 바인딩·진입 명령은 Adapter 경계(격리 지점)이므로 환경 토큰 정당 허용.
UAF 바인딩 3종(contract·entry·discovery-binding)은 adapter-conformance 자매 계수에 비합산한다(DP-X4).
산출물 본문의 외부 정본 § 포인터·절 라벨은 기입 전 대상 정본 직접 실측 대조하고,
복합 인용은 각 문구의 실제 소유 절까지 귀속 대조하며(교차 참조 괄호를 소속 절로 오독 금지),
외부 문서 절 명칭 지칭도 실명칭 실측 대조한다. CP1 전수 스캔에 § 포인터 대조 포함
(L-20 — 이제 Active. Candidate 아님. v1.1 T1·v1.2 T-C·T-R 3회 축적으로 승격).
위임문의 산출물 본문 문안(L-11)·존재 전제(L-12)·계수/규모/상태 전제(L-15)·
§ 라벨/절 번호 지칭(L-20)은 발신 전 파일 시스템 실측으로 대조한다.
위임문 done의 파생·합산 계수(기존 N + 신규 M 등)는 산술 검산으로 재계산하고, 상태 전제는
대상 문서의 stale 문면 인용이 아니라 각 대상 문서 머리를 개별 실측한다
(L-15 — mi-0078 Recurrence: 자매 바인딩 버전 라벨을 adapter-conformance stale 문면에서
인용한 재발 확인. 상태 전제 = 개별 실측).
장시간 집필 Task의 실행 중단(스트림/API 오류 등) 후 재개는 재개 프로토콜을 따른다
(① 산출물·조사 상태 전체 실측 재확인 ② 미완 완성 ③ 전 검증 스캔 재수행 ④ 완료 보고 —
BPD-13, 이제 Active. v1.1 T4·v1.2 Planner 초안 2회 실증).
형태 A(문서·규약) Architecture의 실동작 검증은 규약 절차 구동·사용자 게이트·append-only
Event 로그로 실행 코드 0 실동작을 검증하고 CP2 전수 대조 물리 증거를 남긴다
(BPD-14 Candidate 취지 — 실무 동형 재발 시 재상정).
기존 Baseline 문서의 개정 위임에는 상태 라인·이력 행 라벨의 기대 문면을 명시한다 (L-13).
Agent 기동 설정(.claude/agents/ 이하)의 개정은 사용자 직접 지시 권한 경로로 처리한다 (L-14).
Verifier·Planner 위임은 model opus를 명시한다 (DP-E8 — 차기 세션 재확인 대상으로 승계).
Frozen 미명세 지점은 정본 문면 인스턴스로 해소하고 결정 기록으로 명문화한다 (BP-03).
개정 시 같은 상태 서술의 전 지점 전수 갱신(L-06)·상태·시각 서술은 실측 후 기입(L-07·L-09).
uaf/ 문서 구조 관행 = §9 이력 머리 배치·완료 보고 채널로 Open Questions 대체.
큰 작업 분해·병렬 디스패치·병합은 framework/workflow/ 계약 인스턴스(C1~C4·R1~R4·5단계)와
확정 인터페이스 선행 Wave 배치(BP-02·BPD-06·BPD-11)를 사용한다.
UAF 관련 트랙이면 상시 불변 확인 2건을 매 게이트에 적용한다 — ① Discovery는 교체 가능한
Compiler(내부 개념 Contract 코어/UAHF 접점 누출 0) ② Contract는 장기 호환 Stable Contract
(SemVer·tolerant reader·필드 제거 금지 훼손 0).
append-only 계수 유지 — memory store 81·index 81·loop-data 11파일 83라인(무변경)·
discovery-data events append-only(1 line = 1 레코드·순서 값 seq 전속·벽시계 시각 비주장 L-09).
세션 종료 시 Memory Update — Register Candidate + Advisor 승격 심사.
```

---

# 5. 주의사항

1. **물리 store·loop-data·discovery-data는 append-only다**(04 INV-6·INV-7·03 INV-3) — memory-data/ **81파일·index 81라인**, loop-data/ **11파일 83라인** 수정·삭제 금지. 갱신은 새 레코드/새 전이 이벤트로만. 기존 75 store 파일은 MD5 바이트 무변경 실측(promotion-review §3.2·§3.3). v1.2 승격 append(mi-0076~0081)는 CP2 이후 정상 append이며 "UAHF 정본 무수정" 판정과 무관하다. **discovery-data events.jsonl도 append-only** — 1 line = 1 레코드, 순서는 seq 값에 전속하고 timestamp는 물리 벽시계 시각을 주장하지 않는다(L-09·DP-X10).
2. **§9 이력 행은 시점 기록** — 문면 불변, append만(L-10). 사용자 승인 반영은 별도 행으로 append한다(§5-9 Baseline 승격 절차).
3. **L-20 Active 문면(산출물 본문 § 포인터·복합 인용 귀속 실측)** — L-20은 이제 **Active**(mi-0079 재상정 승격, Candidate 아님). 산출물 **본문**의 외부 정본 § 포인터·절 라벨은 기입 전 대상 정본 파일 직접 실측으로 대조하고, **복합 인용(정의 인용 + 위임/규칙 문구 병기)은 각 문구의 실제 소유 절까지 귀속 대조**한다 — 교차 참조 괄호를 소속 절로 오독하지 마라. 외부 문서의 절 명칭 지칭도 실명칭 실측 대조 대상이다. CP1 자체 점검 전수 스캔에 § 포인터 대조를 포함한다(v1.1 T1 § 포인터 오기 → v1.2 T-C § 오귀속 → v1.2 T-R 절 명칭 오지칭 3회 축적으로 승격).
4. **L-15 확장 — 파생 합산 계수 + 상태 전제 개별 실측(mi-0078 Recurrence)** — 위임문 done의 계수는 단일 실측값(store 규모 등)뿐 아니라 **파생 합산·차감 계수(기존 N + 신규 M)도 발신 전 산술 검산**으로 대조한다. 나아가 **상태 전제(자매·참조 문서 버전 라벨 등)는 대상 문서의 stale 문면을 그대로 인용하지 말고 각 대상 문서 머리를 개별 실측**한다 — v1.2 T-A에서 위임 input이 자매 바인딩 버전을 `adapter-conformance.md` line 12 stale 문면에서 인용해 실측(hooks/plugins v0.9·scaffold v1.0)과 상이했고, 수임 Worker가 재실측·투명 에스컬레이션·비차단 폐합(재작업 0)했다.
5. **재개 프로토콜(BPD-13 Active)** — 장시간 집필 Task의 실행 중단(스트림/API 오류 등) 후 재개 시: ① 산출물·조사 상태 전체 실측 재확인(done 항목별) ② 미완 지점 완성 ③ 전 검증 스캔 재수행 ④ 완료 보고. v1.1 T4 최초·v1.2 Planner 초안 Task 재발로 실증(중단 후 결함 0)되어 Active 승격(mi-0080 supersedes mi-0074).
6. **BPD-14 Candidate 취지(형태 A 실동작 검증 패턴)** — 주 세션(Advisor)이 State Machine을 규약 절차로 구동하고, 사용자 게이트(질문 답변·Ready 승인)를 실사용자와 수행하며, 전 상태 전이를 append-only Event 로그로 기록하면 실행 코드 0으로 문서 설계의 실동작 검증이 성립하고 로그가 독립 검증(CP2) 전수 대조 물리 증거가 된다. 1회 발생(v1.2 T-XG·T-XB)이므로 Candidate 보류 — 실무 동형 재발 시 재상정.
7. **승격 권한 Advisor 전속**(05 INV-4) — Candidate 등록·재발 판정은 승격이 아니다(`approval`·`supersedes` 필드 없이 등록). Active 승격 시에만 승인 참조를 content(`approval`)에 자기완결 첨부. v1.2 승격 2건(L-20·BPD-13 재상정)의 mi-0079·mi-0080은 `approval`·`supersedes` 보유를 실측 확인했다. Worker(승격 심사 문서 집행 주체)는 승격을 결정하지 않고 물리 집행만 한다.
8. **UAHF 정본 무수정(UAF-INV ①) — 명시 3건 예외 완료** — v1.2의 UAHF 정본 개정은 ROADMAP·structure.md §8·adapter-conformance 계수 **3건에 한정**됐고 그 외 UAHF·uaf/ 정본 수정 0(mtime 창 전수 스캔 실측, verification-report item #10). UAF와 UAHF의 접점은 **Project Contract 하나뿐**이며 Contract는 UAHF의 **선택 입력**(부재 시 기존 운용 불변)이다.
9. **Baseline 승격 절차(사용자 승인 시 Advisor가 수행할 목록)** —
   - 신규 문서 5 + docs 3의 상태 라인 "v1.2 Draft" → "v1.2 Baseline" 승격 · 이력 행 append.
   - ROADMAP Status "v1.2 등재 Draft" → Baseline 반영.
   - structure.md · adapter-conformance "v1.2 Draft" → "v1.2 Baseline".
   - 본 핸드오프 §9 이력에 승인 행 append.
10. **하네스 Bootstrap 유지** — v1.2는 형태 A(실행 코드 0)이며 전이 조건 3(Runtime 정식 Module 호스팅) 미충족 승계. Formal 전이(형태 B)는 실행 호스팅 도입 시로 유보(후보 §3.1-a). uaf/ §4 바인딩 지점 11건은 전부 형태 A로 물리화 완료됐다.
11. **상시 불변 확인 2건 (UAF 관련 트랙 매 게이트 판정)** — ① Project Discovery는 단일 기능이 아니라 **Project Contract를 생성하는 Compiler**다(Discovery 교체 가능 · 내부 개념 Contract 코어/UAHF 접점 누출 0). ② Project Contract는 UAF↔UAHF 공식 **Stable Contract(Public API)**다(SemVer·tolerant reader·필드 제거 금지 훼손 0). 두 확인을 통과하지 못한 산출물은 승인하지 않는다.
12. **다음 트랙 미정 — 선취 금지** — ROADMAP v1.2까지 등재 트랙 완료로 다음 트랙은 사용자 결정 사항이다(§3.1). 차기 세션은 트랙을 스스로 채택하지 말고 사용자에게 결정을 요청한다(§4 Bootstrap Prompt 구조). 후보 4종 제시(형태 B/DP-4·uahf-quickstart CLI·유지보수·신규 로드맵)는 선취가 아니다.
13. **계수 갱신 요약(실측)** — memory store **81파일**/index **81라인** · loop-data **11파일/83라인**(무변경) · Memory Active **22**(Lesson 16 + BP 6) · Candidate **19**(Lesson 7 + BP 12) · kind 분포 81(lesson 39 · best-practice 24 · recurrence-judgment 18) · v1.2 신규 문서 **5** · E2E 데이터 **7** · docs **3** · 개정 **3** · Memory append **6**(mi-0076~0081) · 바인딩 지점 **11 물리화** · Event **59**(brownfield 30 + greenfield 29) · 사용자 게이트 **4회**(G1×2 · G2×2 — AskUserQuestion 3회 · 승인 2건).
