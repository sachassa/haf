# Proposal — arch-pipeline (maturation-r001 · Proposing/T1)

- **roleId**: `arch-pipeline` (Expert Role · Capability 선언 · 개방 네임스페이스 — 04 §3.3)
- **capability**: 파이프라인 구조·Layer 배치·`architectureDirection` 미결(open) 해소 방향에 대한 설계 결정.
- **입력 결속 (inputContract)**:
  - **기준선 인스턴스**: `framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v1.md` — pc-uahf-001 · instanceVersion 1 · supersedes null · 종단 `Ready`(사용자 승인 2026-07-07). 성숙 기준선(SP-INV 1 충족).
  - **v1 이후 확정 결정 집합(저장소 실측)**: (i) v1.2.1 최상위 5-Layer 재구성 — `ls` 실측 `entry/·discovery/·planning/·uahf/·knowledge/`(+ 지원 dir design/docs/research/templates/tests)·루트 ARCHITECTURE §0·§2.1. (ii) 루트 ARCHITECTURE 문서버전 v1.4 — §2.2 Contract 요소 내부 성숙 루프(Δ1)·6요소 불변·§12.1 용어 4건. (iii) `planning/specs/04-solution-design.md` v1.3 Baseline 신설 — 단계 계약·SP-INV 1~8. (iv) `planning/specs/03-project-contract.md` v1.2 Baseline — 생산자 2경로(§3.1-B)·Contract Maturation 갱신 유형(§3.4). (v) planning/ 이중 책임(04 §0·planning/ARCHITECTURE). (vi) `solution-design-binding.md` v1.4 Draft 신설(형태 A Adapter Binding·§8 provenance 성숙 run 내부 형식). (vii) `uahf/ROADMAP.md` §3 v1.3 마일스톤 행 등재. (viii) 본 run 실측 — `events.jsonl` seq 1(MaturationRunStarted)·seq 2(T1 성숙 필요·역할 2 할당)·`assessing-judgment.md`.
  - **잔여 미결(architecture 축)**: 형태 B 실행 호스팅 경계 분할·UAHF Contract 정식 등재·형태 B 착수 시점·정식 등재 채택 여부.
- **작성**: 2026-07-13 · 담당 관심사 한정 v2 delta 제안(§3.4-D ① Proposal). 본 문서는 코어 밖 실행 메타다(SP-INV 2·3) — Contract 코어 필드로 유입되지 않는다.
- **동시 작성 경계(07 R2)**: 동시 작성 중인 `governance-consistency` 산출을 인용·추측하지 않았다. 확정된 인터페이스 계약(04 §3·03 §3.2-A·§3.4·루트 §2.2·solution-design-binding §8)과 저장소 실측만 참조했다.

---

## 1. 담당 관심사 경계 (선언)

이 Proposal은 **파이프라인 서술·Layer 배치·`architectureDirection`(decisions·open)·`readiness.openQuestions`의 아키텍처 축·`provenance` 경로 관례**에 한정한다. 요구·리스크 문면·이월 부채·비아키텍처 라벨 정확성은 `governance-consistency` 관심사이며, 겹칠 수 있는 delta는 §4 잠재 충돌 지점에 명시한다.

**전건 제약 준수 (자기 점검)**: D4 스키마 무변경(9그룹·필수 코어 필드 외 새 필드·새 그룹 제안 0·schemaVersion "1.0" 유지) / v1 무수정(delta는 본 제안 문서에만) / 6요소 파이프라인 유지 / planning rename 0 / Draft·Final mutable 어휘 0 / 제외 범위(step executor·Script Runtime·Workflow Engine 등)는 open 등재까지만·설계 0.

---

## 2. Delta 표 (축 1~5 · v1 기준선 → v2 제안)

각 delta: ① 필드 경로(03 §3.2-A 그룹) ② v1 현행 문면(인용) ③ 제안 v2 문면 ④ 판정. 근거 상세는 §3.

| # | 축 · 필드 경로(그룹) | v1 현행 문면 (인용) | 제안 v2 문면 | 판정 |
|---|---|---|---|---|
| **A1** | intent — 파이프라인 서술 (그룹 2 Intent) | front-matter: "…UAF 레벨 진입 파이프라인(Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF)을 정의하고, 하네스 자신의 개발에…" | "…UAF 레벨 진입 파이프라인(Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF)을 정의하고 — **Project Contract 요소 내부에는 Ready 인스턴스 vN을 복잡도에 따라 superseding v(N+1)로 성숙시키는 Solution Design 루프가 있다(파이프라인 6요소 불변·루트 §2.2·정본 planning/specs/04)** —, 하네스 자신의 개발에…" | **현행화(성숙 루프 반영)**. v1.2.1 물리 재구성은 intent에 넣지 않고 A2 decisions에 배치(권고). |
| **A2** | architectureDirection.decisions (그룹 6) | 결정 2: "4경계 물리 배치(core/runtime/module-dirs/adapters)·Adapter 격리(claude 완전 구현 + generic 최소 구현)" / 결정 3: "UAF 레벨 파이프라인은 UAHF 6-Layer 외부 — 접점은 Project Contract 하나" / (결정 1·4 무변) | 결정 2 → "**최상위 5-Layer 물리 구성(entry/·discovery/·planning/·uahf/·knowledge/ — v1.2.1)에서 UAHF는 uahf/ 아래 Runtime Layer 구현이며, 그 내부는** 4경계 물리 배치(core/runtime/module-dirs/adapters)·Adapter 격리(claude 완전 구현 + generic 최소 구현)를 유지한다". 결정 3 → "UAF 레벨 파이프라인은 UAHF 6-Layer 외부 — 접점은 Project Contract 하나. **Project Contract 요소는 planning/ Layer가 이중 책임(스키마 소유 + Solution Design 성숙 활동 소유)으로 소유하며, 성숙은 요소 내부 루프(Ready vN → superseding v(N+1))로 파이프라인 요소 수를 늘리지 않는다(6요소 불변).**" | **현행화(제자리 · 결정 4항 카운트 유지)**. 5번째 항 신설은 대안(§5). |
| **A3** | architectureDirection.open (그룹 6) | open 1: "형태 B 실행 호스팅의 경계 분할(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2) — DP-4 재상정 시" / open 2: "UAHF 측 Contract 정식 등재(**uaf/specs/03** §3.5-C 확장 포인트)" | open 1 → "형태 B 실행 호스팅의 경계 분할(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2 **+ Solution Design 실행 호스팅** — 04 §3.9·solution-design-binding §6) — DP-4 재상정 시". open 2 → "UAHF 측 Contract 정식 등재(**planning/specs/03** §3.5-C 확장 포인트)". **신규 open 3(후보·등재만)** → "step 기반 실행기 계열(Script Executor·Step Runtime·fresh context·Retry/Resume/Blocked·Progress·Git automation) = UAHF Execution/Runtime 진화 축 — 04 §3.9 연결만·별도 분석 트랙 후보(설계 0)". | open 1·2 **현행화**(2 stale 경로 정정·형태 B 범위 확대). open 3 = **후보 등재**(사용자 게이트 수락 필요 — §6). |
| **A4** | readiness.openQuestions — 아키텍처 축 (그룹 8) | "형태 B 전이(실행 호스팅 도입) 착수 시점" / "Contract의 UAHF 정식 등재(03 §3.5-C) 채택 여부" (+ "이월 개정 일괄…" = 비아키텍처) | OQ(형태 B) → "형태 B 전이(실행 호스팅 도입) 착수 시점 — **v1.3/v1.4는 형태 A 유지(Solution Design Adapter Binding 신설·dogfooding E2E 형태 A)·형태 B 미착수**". OQ(정식 등재) → "Contract의 UAHF 정식 등재(**planning/specs/03** §3.5-C 확장 포인트) 채택 여부 — **미채택 유지**". | **존속 + 문면 현행화만**. 두 항 모두 **해소 불가**(해소할 실제 결정 부재 — 실측). "이월 개정 일괄" OQ는 governance-consistency 소관(무촉·§4). |
| **A5** | provenance — 경로 관례 (그룹 9 · 불투명 부속) | front-matter: `eventLog: "framework/adapters/claude/discovery-data/events/brownfield-r001/"` (저장소-루트 상대·`uahf/` 접두 없음) | **방향 1문**: v2의 `provenance`는 solution-design-binding §8 성숙 run 내부 형식(run 식별자 `maturation-r001`·이벤트 로그 참조 `solution-design-data/events/maturation-r001/`·기준선 v1 참조[=`supersedes`]·Policy 참조)을 따르되, **v1이 이미 쓰는 저장소-루트 상대 표기(라이브 `events.jsonl` payload와 동일 관례)를 그대로 유지**하며 v1 provenance는 무촉(PC-INV 3 must-ignore·03 §3.4 append-only)이다. | **방향 제안**(형식은 solution-design-binding §8 소유 — 재정의 0). v1 무촉. |

---

## 3. 근거 상세 (축별 · 저장소 실측·정본 § 포인터)

### A1 — intent 파이프라인 서술 현행화

- **근거**: 루트 ARCHITECTURE §2.2 Δ1("Project Contract 불릿에 Contract 요소 내부 성숙 루프 서술 추가 + '파이프라인은 6요소 그대로다' 명시")·04 §2·§3.1-A(단계 정의)·03 §3.4(성숙=supersedes 계보). assessing-judgment §2 신호 4 실측: "v1 이후 확정 결정 미반영: … Solution Design 성숙 루프 신설". v1 intent는 이 성숙 루프를 담지 않는다.
- **6요소 유지 준수**: 성숙 루프를 **Contract 요소 내부 루프**로만 서술하고 새 파이프라인 요소로 열거하지 않는다(루트 §2.2·§2.4 INV-3 무촉·D2·04 §2). "파이프라인 6요소 불변" 명시로 6요소 카운트를 보전한다.
- **v1.2.1 배치 판단(권고)**: v1 intent의 파이프라인 5-요소 나열(Execution 압축 생략)과 "6-Layer(Presentation~Adapter)" 서술은 **UAHF 수직 스택**(INV-3 = 정확히 6개)이며 v1.2.1(최상위 물리 5-Layer)과 별개 네임스페이스다(루트 §0 "두 'Layer' 축"). 최상위 5-Layer 물리 재구성은 **구조 결정**이므로 intent 서술이 아니라 `architectureDirection.decisions`(A2)에 두는 것이 필드 귀속상 정확하고 최소 변경이다. 따라서 intent에는 성숙 루프만 반영하고 v1.2.1 물리 재구성 서술은 넣지 않기를 권고한다(대안은 §5·§6).
- **본문 프로세스 미러**: front-matter가 스키마 정본이나, 본문 `## Intent`(v1: "6-Layer + Memory 횡단 구조 위에 v1.1부터 UAF 레벨 진입 파이프라인(Entry → Discovery → Contract)을 신설했으며…") 문장에 "v1.3부터 Project Contract 요소 내부에 Solution Design 성숙 루프(Ready vN → superseding v(N+1))를 신설했다" 한 구를 append해 front-matter와 정합시킬 것을 권고(문면만·의미 무변).

### A2 — architectureDirection.decisions 현행화

- **결정 2 근거**: `ls` 실측 최상위 = `entry/·discovery/·planning/·uahf/·knowledge/`(5 Layer). 루트 §0("신 물리 실재 = 최상위 5 Layer … UAHF = `uahf/` 아래 Runtime Layer 구현체")·§2.1(라우터 표). structure.md §2(4경계 배치 = `framework/adapters/<adapter>/` 등 = 환경 격리). v1 결정 2("4경계 물리 배치")는 **여전히 유효**하나 그 4경계가 v1.2.1 이후 최상위 `uahf/` Runtime Layer **아래** 있음을 명기해 최상위 Layer 중심 구성과 정합시킨다. UAHF 6-Layer 스택·13 Core Component(결정 1)는 무변(INV-3 무촉).
- **결정 3 근거**: 루트 §2.1(planning 행: "Project Contract · Solution Design(성숙 루프)")·§2.2(Contract 요소 내부 성숙 루프)·04 §0("planning/ Layer는 이중 책임 — (i) Project Contract 스키마 소유 + (ii) Solution Design 성숙 활동 소유")·planning/ARCHITECTURE. 성숙=요소 내부 루프이므로 접점(Project Contract 하나·UAF-INV ①) 불변·6요소 불변을 함께 명시한다. planning rename 0(이중 책임을 rename 없이 서술 — 04 §0·D1 정합).
- **결정 4("현 실현 = 형태 A") 무변 근거(실측)**: `tests/` 빈 디렉터리·runtime 실행 코드 0·solution-design-binding §0(Bootstrap 형태 A). v1.4가 신설한 solution-design-binding도 **형태 A Adapter Binding**(실행 코드 0)이므로 "형태 A" 결정은 존속. 무변.
- **카운트 규율(L-25)**: 결정 3에 planning 이중 책임 구를 **제자리 현행화**하여 결정 항 수 4를 유지한다 → 본문 `## Architecture Direction`의 "결정 4항" 재계수 무변. (5번째 항 신설 대안은 §5.)

### A3 — architectureDirection.open 현행화 + 신규 후보

- **open 1 근거**: 04 §3.9("형태 B 실행 호스팅 … 물리 호스팅은 후속")·solution-design-binding §6.1("물리 호스팅 = 설계 안 함 — 04 §3.9 확장 포인트"). v1.4가 Solution Design 실행 주체를 형태 A 규약 절차로만 실현했으므로, 형태 B 경계 분할 미결에 **Solution Design 실행 호스팅**을 합류시킨다(기존 M5/VB/LB/WB/PB 경계와 동류·설계 0).
- **open 2 근거(stale 경로 정정)**: v1 문면 "uaf/specs/03 §3.5-C"의 `uaf/` 경계는 v1.2.1에서 **물리 소멸**했다(루트 §0 "과거 `uaf/`는 v1.2.1 구조 이동에서 물리적으로 소멸"). 현행 정본 실측 = `planning/specs/03-project-contract.md` §3.5-C("정식 등재는 확장 포인트 … 여기서 설계하면 UAF-INV ① 위반"·PC-INV 8). 경로만 현행화·의미 무변.
- **open 3(신규 후보·등재만·설계 0) 근거**: v1.3 §5.5 Defer 실측("step 기반 Script Executor·Step Runtime·fresh context·Retry/Resume/Blocked·Progress·Git automation = **UAHF Execution/Runtime 진화 축**(Solution Design 아님 — 04 §3.9 확장 포인트로 연결만 확보·별도 분석 트랙 후보)")·04 §3.9("step 기반 실행기와의 연결 … 명칭만·설계 금지")·v1.4 §1 제외 범위. 이는 아키텍처 방향의 실재 미결이므로 open 등재가 정합하되, **제외 범위 준수로 등재까지만·어떤 설계·구조 제안도 없음**. 등재는 open 집합을 확장하므로 사용자 게이트(Validating) 수락 전제 — §6에서 에스컬레이션.
- **본문 재계수 주의(L-25·조건부)**: open 3이 수락되면 본문 `## Architecture Direction`의 "미결 2항"이 "미결 3항"으로 재계수되어야 한다(front-matter open 3항과 정합). open 3 미수락 시 "미결 2항" 유지. governance-consistency의 카운트 정합과 겹침(§4).

### A4 — readiness.openQuestions 아키텍처 축 (해소 불가·존속)

- **형태 B OQ 존속 근거(실측)**: 형태 B 실행 호스팅은 **미착수**다 — `tests/` 빈·runtime 실행 코드 0·solution-design-binding §0(형태 A). v1.4는 형태 A Adapter Binding(solution-design-binding)과 형태 A dogfooding E2E만 진행. 형태 B 착수 결정이 **실재하지 않으므로 해소 금지**(허위 해소 불가). 문면에 형태 A 진척 실측만 append(현행화).
- **정식 등재 OQ 존속 근거(실측)**: 03 v1.2 §3.5-C 실측 = "확장 포인트로만 … 정식 등재를 여기서 설계하면 UAF-INV ① 위반"(PC-INV 8). 정식 등재 채택 결정이 실재하지 않으므로 **존속**·경로만 현행화(`planning/specs/03`). open 2와 동일 관심사이므로 문면을 정합시킨다.
- **판정 규율**: "해소는 실제 결정이 실재할 때만"(위임)·L-24(완전성 주장 시 스윕 범위 명시). 아키텍처 축 2개 OQ 전수 검토 결과 **해소 대상 0**(스윕 범위 = v1 readiness.openQuestions 3항 중 아키텍처 축 2항). 비아키텍처 OQ("이월 개정 일괄 처리 시점")는 본 관심사 밖 — governance-consistency 소관으로 무촉.

### A5 — provenance 경로 관례 (방향 1문·v1 무촉)

- **경로 표기 실측**: v1 `provenance.eventLog` = `framework/adapters/claude/discovery-data/events/brownfield-r001/`(저장소-루트 상대·`uahf/` 접두 없음). 라이브 `events.jsonl` seq 1 payload `input` = `framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v1.md`(동일 관례). 현행 물리 절대 경로는 `uahf/framework/adapters/claude/…`(v1.2.1 이후). 이 차이는 **저장소-루트 상대 표기 vs cwd 절대 표기의 표기 차**이며 의미 결함이 아니다(solution-design-binding §0 OQ-SD-2 = 경로 이중성 비차단 후속).
- **방향**: v2 provenance는 (i) 내부 형식 = solution-design-binding §8.1 성숙 run 내부 형식(run 식별자·이벤트 로그 참조·기준선 vN 참조·Policy 참조)을 따르고 — 이 형식의 **소유는 solution-design-binding §8**이므로 본 제안은 재정의가 아니라 포인터다 —, (ii) 경로 표기는 v1·라이브 데이터와 동일한 저장소-루트 상대 관례를 유지한다. **v1은 무촉**(PC-INV 9 append-only·v1 문면 byte 불변·03 §3.4). 전 자매 바인딩의 이중 표기 통일은 마일스톤 밖 후속(OQ-SD-2).
- **실제 v2 provenance 블록 자체는 v2 발행(Matured) 시 산출**되며 본 축은 그 방향만 제안한다(설계 선취 금지).

---

## 4. 잠재 충돌 지점 (governance-consistency와 겹칠 수 있는 delta — Reconciling 대비)

| # | 겹침 지점 | 본 역할 주장 | governance-consistency 소관 추정 | Reconciling 제안 |
|---|---|---|---|---|
| C1 | **stale 경로 라벨** (open 2 `uaf/specs/03`→`planning/specs/03`·OQ 정식 등재 `03 §3.5-C`) | architectureDirection.open·readiness.openQuestions 아키텍처 축의 경로 참조는 본 역할이 정정 제안 | 저장소 전반 라벨 정확성 스윕(요구·리스크·provenance mode·"Workflow 분해 C1~C4" 라벨 의심 등)은 governance 소관 | 경로 정정의 **소유 배분**: 아키텍처 필드 내 경로 = arch-pipeline / 그 외 라벨 = governance. 동일 규율(v1.2.1 `uaf/` 소멸) 공유 |
| C2 | **intent 필드 공동 편집** | 성숙 루프 구 삽입(구조 서술) | intent의 요구·dogfooding·실용화 문면 현행화 가능 | intent는 단일 scalar → 두 delta를 Reconciling에서 **병합**(구조 구 + 문면 구 동시 반영·중복 0) |
| C3 | **이월 개정 일괄 OQ**(readiness.openQuestions 비아키텍처 항) | 본 역할 **무촉**(아키텍처 축 아님) | governance 소관(이월 부채 처리) | 누락 방지 — governance가 이 OQ의 존속/현행화를 담당함을 명시 |
| C4 | **risk 문면**("형태 B 전환 복잡성"·"이월 개정 후보 누적") | 본 역할은 형태 B open/OQ만 다룸(risk 문면 무촉) | risk 문면 현행화는 governance 소관 | 형태 B open(A3)과 risk "형태 B 전환 복잡성"의 **주제 정합** 확인(모순 0) |
| C5 | **본문 카운트 재계수**("결정 4항"·"미결 2항") | A2는 결정 4항 유지 권고(카운트 무변)·A3 open 3 수락 시 "미결 2항→3항" | 본문 재계수·카운트 정합(L-25)은 governance와 공유 | open 3 수락 여부 확정 후 본문 "미결 N항" **최종 재계수**를 governance와 공동 확정 |
| C6 | **readiness.confidenceVector.architecture(0.90)** | 아키텍처 결정 현행화로 재확인 가능(존치 권고) | confidenceVector·completeness 프레이밍은 readiness(그룹 8) 공유 관심 | 값 변경 없이 존치 권고 — 변경 필요 시 Reviewing에서 공동 판단 |

---

## 5. 대안 (Reviewing 선택지)

- **A1 대안**: intent에 v1.2.1 최상위 5-Layer 서술까지 반영(fuller). 권고안(§3 A1)은 최소 변경·필드 귀속 정확성 위해 **미반영**하고 A2 decisions에 배치. Reviewing이 intent 서술 강화를 선호하면 fuller 채택 가능(단 6-Layer 수직 스택 서술과 최상위 5-Layer 네임스페이스 혼동 방지 문구 필수 — 루트 §0).
- **A2 대안**: 결정 3 제자리 현행화 대신 **5번째 결정 항 신설**("Project Contract 요소 = planning/ 이중 책임·Solution Design 성숙 루프 내부"). D4상 새 필드가 아니라 기존 list 항 추가라 허용되나, 본문 "결정 4항" 재계수(→5항)를 유발하므로 **제자리 현행화(4항 유지)를 권고**.

---

## 6. open (불확실·에스컬레이션 필요 — Validating 게이트 대비)

- **OQ-AP-1 (신규 open 3 등재 — 사용자 게이트 필요)**: A3 open 3(step 기반 실행기 계열 = UAHF Execution/Runtime 진화 축)은 v1.3 §5.5 Defer·v1.4 §1 제외 범위에 속한다. open 항목 등재는 미결 집합을 확장하므로 **사용자 승인 게이트(Validating·UAF-INV ⑤) 수락이 전제**다. 등재만·설계 0 원칙 준수. 사용자가 등재를 원치 않으면 open 2건 유지(현행화만).
- **OQ-AP-2 (A1 v1.2.1 배치 판단)**: intent에 최소(성숙 루프만) vs fuller(v1.2.1 물리 재구성 포함) 중 선택은 Reviewing 판단. 권고 = 최소 + A2 배치.
- **OQ-AP-3 (경로 정정 소유 배분)**: C1의 stale 경로(`uaf/` 소멸) 정정을 arch-pipeline과 governance-consistency 중 누가 어느 필드에서 소유하는지 Reconciling에서 확정 필요(중복 편집·누락 방지).
- **비차단 확인**: 위 3건은 전부 Reconciling/Reviewing/Validating에서 해소 가능한 조율 항목이며, 본 Proposal 산출을 차단하지 않는다(추측 우회 0 — 02-agent O4).
