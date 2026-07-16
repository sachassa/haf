# Proposal — governance-consistency (maturation-r001 · `Proposing`)

- **roleId**: `governance-consistency`
- **capability**: 요구·리스크·정합 부채·라벨 정확성에 대한 설계 결정 (assessing-judgment.md §3).
- **입력 결속**: 입력 인스턴스 = `discovery-data/contracts/uahf/project-contract.v1.md`(pc-uahf-001·instanceVersion 1·Ready) + 대상 spec 실측(라벨 검증) + v1.3 §6 이월 인벤토리. Policy = default-policy. 상태 = 04 §3.4-A `Proposing`(T1 진입, assessing-judgment 판정 = 성숙 필요).
- **작성**: 2026-07-13 · Worker(Advisor 위임) · 산출 = 본 파일 단일(타 파일 무촉).
- **경계**: D4 스키마 무변경(새 필드·그룹 0)·v1 무수정·모든 판정 실측 근거·arch-pipeline 산출 추측·인용 0(07 R2). 본 proposal은 담당 관심사(Requirements·Risks·Constraints·Readiness 거버넌스 축)의 v2 delta 제안이며, 확정 권한은 Reviewing→사용자 게이트다(04 §3.4-C).

---

## 1. 라벨 전수 실측 검증 (임무 1 — L-25·L-24)

### 1.1 검증 방법·범위·한계 (정직 명시)

- **방법**: v1 requirements(functional 5항·quality 3항)의 모든 계수·라벨을 개별 grep + 해당 § 정독으로 대상 정본에서 실측. 각 라벨 = ① v1 문면 ② 대상 정본 실측(파일·§·실제 표현) ③ 판정 ④ 정정 시 제안.
- **직접 정독/실측한 정본**: `uahf/specs/02-agent.md`(§3.1·§3.2 전문)·`03-loop.md`(grep+§3.1-A)·`06-verifier.md`(grep+§3.2-E)·`07-workflow.md`(grep 전수)·`framework/workflow/decompose-rules.md`(전문)·`04-memory.md`(grep)·`05-lessons.md`(grep)·`12-scaffold.md`(grep)·`11-adapters.md`(grep)·`entry/specs/01-entry.md`(grep)·`planning/specs/03-project-contract.md`(전문)·`00-glossary.md`(grep).
- **한계(scope)**: (a) `Project Discovery(Compiler)` 라벨은 `discovery/specs/02-discovery.md`를 직접 열지 않고 03/04 spec의 근거 정본 상호참조("02-discovery §3.1 Compiler·불완전 출력 금지")로 **간접 실측** — 직접 grep 미수행. (b) grep 검증은 검색 패턴 커버리지에 의존한다 — 각 라벨의 핵심 토큰을 개별 grep했으나 문면 전량 정독은 위 "직접 정독" 정본에 한정. (c) `마일스톤 풀 프로토콜`은 단일 정본이 7단계를 명명 열거하지 않는 **composite 관행 라벨** — 구성 sub-label 각각은 실측했으나 연쇄 전체의 단일 정본 열거는 부재.

### 1.2 검증 표 (24 라벨 — 유지 23 / 정정 1)

| # | v1 문면 (라벨) | 대상 정본 실측 (파일·§·실제 표현) | 판정 |
|---|---|---|---|
| f1-a | functional① Agent 역할 4종(Advisor·Planner·Worker·Verifier) | 02-agent §3.2-A "4개 역할" 표 = Advisor·Planner·Worker·Verifier | 유지 |
| f1-b | functional① 위임 8필드 | 02-agent §3.2-B = from·to·task·input·output·done·context·constraints = **8** | 유지 |
| f1-c | functional① 완료 보고 5필드 | 02-agent §3.2-C = artifacts·self_check·failures·open_questions·verify_basis = **5** | 유지 |
| f2-a | functional② Memory Record/Recall | 04-memory §3.1-A Record·§3.1-B Recall | 유지 |
| f2-b | functional② 단일 Port | 04-memory §3.1·INV-1 "Memory Service Interface 하나뿐" | 유지 |
| f2-c | functional② index-first | 04-memory INV-4 "기본 회수 세분도는 index"·§3.1-B 기본값 `index` | 유지 (특성화 — spec 어휘 = "기본값 index"/"최소 Context 우선") |
| f2-d | functional② Lessons 재발 판정 | 05-lessons §3.1-C Judge Recurrence | 유지 |
| f2-e | functional② 승격 심사 | 05-lessons §3.1-A Promote(Candidate→Active)·승격 규칙 | 유지 |
| f3-a | functional③ Loop 사이클(CP1~CP3) | 03-loop §3.1-A 검증 게이트 CP1(자체 점검)·CP2(독립 판정)·CP3(승인) | 유지 |
| **f3-b** | **functional③ Workflow 분해 C1~C4** | **07-workflow.md grep(`C1~C4\|C1\|C2\|C3\|C4`) = No matches.** 07 §3.1-A Decompose 정본 = 완료 조건 **3건**·실패 reason **4종**. "C1~C4"는 `framework/workflow/decompose-rules.md` §3의 **검사 규칙 라벨**이며, 동 문서 §0가 "검사 라벨 C1~C4·D1~D2는 본 문서 서술 편의의 명명 규칙이며 **계약 용어가 아니다**"로 명시 | **정정** ⚠️ |
| f3-c | functional③ 디스패치 R1~R4 | 07-workflow §3.2-C 병렬 디스패치 프로토콜 = R1(위임 전용)·R2(미완성 불추측)·R3(조율 에스컬레이션)·R4(경계 준수) = **4** | 유지 |
| f3-d | functional③ 병합 5단계 | 07-workflow §3.1-C/§3.2-D Merge, 충돌 처리 순서 = 수합→상호 참조 정합성 검증→충돌 검출→Advisor 중재→병합 성립 = **5단계** | 유지 (특성화 — spec이 "5단계"로 명명하진 않으나 계수 정확) |
| f3-e | functional③ Verifier VT-1~5 독립 판정 | 06-verifier §3.2-E = VT-1(존재)·VT-2(완료 조건 대조)·VT-3(규격 준수)·VT-4(경계)·VT-5(시연) = **5** | 유지 |
| f4-a | functional④ Scaffold Project Template | 12-scaffold §3.2-A Project Template | 유지 |
| f4-b | functional④ Install Manifest | 12-scaffold §3.2-B Install Manifest | 유지 |
| f4-c | functional④ Adapter Conformance | 11-adapters §3.2-B Conformance Criteria(Valid(Full)/Valid(Minimal)/Invalid) | 유지 |
| f4-d | functional④ BP-1~17 | 11-adapters §3.2-A 바인딩 표 = BP-1 … BP-17(필수 13 + 선택 4) | 유지 |
| f5-a | functional⑤ Entry Resolution 결정 테이블 8조합 | 01-entry §3.2-D "전 8조합 전수 열거"·"Entry 2종 × Contract 유무 × Repository 유무 = 8조합" | 유지 |
| f5-b | functional⑤ Project Discovery(Compiler) | 03/04 spec 근거 정본 상호참조 = "02-discovery §3.1 Compiler·불완전 출력 금지" (간접 실측 — §1.1 한계 (a)) | 유지 (scope 주) |
| f5-c | functional⑤ Project Contract(Stable Contract) | 03-project-contract §3.1-A "UAF↔UAHF 공식 Stable Contract(Public API)" | 유지 |
| q1 | quality① 마일스톤 풀 프로토콜(Planner 초안→Advisor 채택→Wave 병렬→CP2→CP3→핸드오프→Baseline) | composite: Planner 초안·Advisor 채택(02 §3.1)·Wave 병렬(07 병렬 디스패치)·CP2/CP3(03 §3.1-A·06)·핸드오프(session-handoff 문서)·Baseline(spec §9 Revision History 승격) — sub-label 각각 실측 | 유지 (composite·scope 주 — 단일 정본 7단계 열거 부재) |
| q2 | quality② 완료 보고 불신·산출물 직접 실측 독립 검증·거짓 완료 검출 | 06-verifier §0 "완료 보고를 그대로 신뢰하지 않고 산출물 자체를 근거로 독립 판정"·§3.2-F 거짓 완료 보고 검출·VT-4 전수 스캔 | 유지 |
| q3-a | quality③ Frozen spec 개정 규율(버전 상승+Revision History) | 00-glossary §3.2-G "이후 변경은 spec 버전 상승과 Revision History 기록이 필수"·03 §3.3-E | 유지 |
| q3-b | quality③ 재발 판정 3분류(Novel/RecallGap/Recurrence) | 05-lessons §3.1-C "판정 결과 ∈ { Novel, RecallGap, Recurrence }"·§3.2-E | 유지 |

**정정 라벨 1건 = f3-b (Workflow 분해 C1~C4).** v1.3 §6(2026-07-13)이 이미 "pc-uahf-001·Memory의 'Workflow 분해 C1~C4' 라벨이 07-workflow.md에 부재하는 의심(**요확인**)"으로 기록한 부수 검출을, 본 role의 독립 재실측(07 전수 grep = No matches + decompose-rules.md §0 명시)으로 **확정**한다. 이는 L-25 커널("분류 라벨 전사" — 라벨을 소재 정본과 대조 없이 전사)의 재발 유형이다.

---

## 2. delta 표 (임무 2 — v1 이후 현행화)

각 항목: ① 필드 경로(03 §3.2-A 그룹) ② v1 현행 문면(인용) ③ 제안 v2 문면 ④ 근거(실측). 전 항목 D4 스키마 무변경(기존 필드 내 문면 정정만·새 필드/그룹 0).

### D1 — requirements.functional[3항째] (그룹 3 Requirements) · 라벨 정정

- **v1**: `"Loop 사이클(CP1~CP3)·Workflow 분해 C1~C4/디스패치 R1~R4/병합 5단계·Verifier VT-1~5 독립 판정"`
- **v2 (제안)**: `"Loop 사이클(CP1~CP3)·Workflow 분해(Decompose 완료 조건 3건·reason 4종)/디스패치 R1~R4/병합 5단계·Verifier VT-1~5 독립 판정"`
- **근거**: §1.2 f3-b. 07 §3.1-A Decompose 정본은 완료 조건 3건·reason 4종이며 "C1~C4" 라벨은 spec에 부재(계약 용어 아님). spec-anchored 정확 표현으로 교체. (문면은 front-matter functional 3항째에만 등장 — 본문 §Requirements 요약(line 71)은 "Loop·Workflow·Verifier" 일반형이라 무촉.)
- **대안 문면(Reviewing 위임)**: (b) `"Workflow 분해(Decompose)"` 일반형 / (c) `"Workflow 분해 C1~C4(decompose-rules.md 검사 규칙 라벨)"` 재수식 — 셋 다 "C1~C4를 07 spec 계약 라벨로 오귀속"을 해소. 최소 정정 원칙상 (a) 권장.

### D2 — risks[3항째] (그룹 5 Risks) · 계수·문면 현행화

- **v1**: `"이월 개정 후보 누적(stale 계수·서수 표기 등 비차단 8+1건) — 방치 시 정합 부채화 (정본 실측)"`
- **v2 (제안)**: `"이월 개정 후보 누적(라벨 결함·bare § 접두 미부기·stale 표기·자기 불일치 등 비차단 7건 — v1.3 §6 실측: 부수 검출 4 + W2 CP2 관찰 3) — 방치 시 정합 부채화. 일부는 v1.4 W3(discovery-data 미존재 계열)·maturation-r001(Workflow 'C1~C4' 라벨)에서 정정 진행 (정본 실측)"`
- **근거**: v1.3 §6 이월·비차단 인벤토리 실측 = 부수 검출 **4건**(① contract-binding §4·§10 "discovery-data 미존재" stale ② "C1~C4" 라벨 ③ 02 §3.7 자기 불일치 ④ CP1~CP3 인용 앵커) + W2 CP2 관찰 **3건**((i) 03 §3.1-B bare "§3.7" (ii) 루트 §12.1 flat "Project Discovery의 산출" (iii) 03 §7 done-11 "v1.1 Draft" stale) = **7건**. v1 "8+1건"은 v1-era(2026-07-07 brownfield-r001) 계수로 stale. 또한 "stale 계수·서수 표기 등"은 실제 인벤토리(라벨 결함·자기 불일치·인용 앵커·접두 미부기 포함)보다 좁은 특성화 → 현행화.

### D3 — constraints[4항째] (그룹 4 Constraints) · append-only 데이터 열거 현행화 ⚠️ cross-cutting

- **v1**: `"물리 데이터(memory-data/·loop-data/·discovery-data/) append-only"`
- **v2 (제안)**: `"물리 데이터(memory-data/·loop-data/·discovery-data/·solution-design-data/) append-only"`
- **근거**: v1.4 DP-1(solution-design-data/ 신설 — 자매 *-data/ 격리 관례 동형)·DP-2(events.jsonl append-only). 본 maturation-r001 run이 `solution-design-data/events/maturation-r001/`를 실생성하므로 append-only 물리 데이터 열거가 불완전. **동일 append-only 원칙의 열거 확장이며 새 제약 창설 아님**(constraints[3] "append-only 데이터"·본문 §Constraints line 75와 정합 — 본문은 열거 미포함이라 무촉, front-matter만 정정).
- **cross-cutting 주의**: solution-design-data/ 백엔드 신설 **결정**은 DP-1(저장/아키텍처) 소관 = arch-pipeline과 교차. 열거 현행화(정합)는 governance-consistency 소관이나, 백엔드 존재 근거는 arch/pipeline. → §3 잠재 충돌 1.

### D4 — readiness.openQuestions[2항째] (그룹 8 Readiness) · 계수 현행화 (D2 동반)

- **v1**: `"이월 개정 일괄(차기 개정 후보 8+1건) 처리 시점"`
- **v2 (제안)**: `"이월 개정 일괄(차기 개정 후보 7건 — v1.3 §6 실측; 일부 v1.4 W3·maturation-r001 정정 진행) 처리 시점"`
- **근거**: risks[3항째]와 **동일 계수(8+1건)**를 인용하므로 D2와 동반 현행화 필요(두 필드 간 계수 불일치 방지). 근거 실측은 D2와 동일(v1.3 §6 = 7건).

### 비-delta 판정 (현행 유효성 확인 — delta 불요)

| 필드 | 판정 | 실측 근거 |
|---|---|---|
| risks[1항째] 문서 규모·복잡도 증가 | 존속 | v1.4가 04-solution-design·바인딩 추가로 규모 증가 지속 — 문면 여전히 참 |
| risks[2항째] 형태 B 전환 복잡성(OQ 4건) | 존속 | 형태 B 미도입(v1.4 §1 형태 A 유지)·architectureDirection.open 4 OQ 존속 |
| risks[4항째] 사용자 게이트 실시간 의존 | 존속 | v1.4 W2 Validating 실승인 대기가 오히려 재강화 — 문면 유효 |
| constraints[5항째] Bootstrap 형태 A·실행 코드 0 | 존속 | v1.4 §2 "tests/ 빈 디렉터리·형태 A"·DP-3(새 병렬 Framework 0)·DP-5(Policy Engine 0). scope 주: 근거 = v1.4 설계 정본 assertion + 본 run 산출이 .md/.jsonl 데이터·규약 문서에 국한(실행 코드 0) |
| quality 완전성 주장 규율(L-24) | 실질 포섭 → delta 불요 | 핵심 facet(검사 범위 정직·전수 스캔)이 06 VT-4/V4/INV-4로 프레임워크 기능 실재·quality② "산출물 직접 실측 독립 검증·거짓 완료 검출"에 포섭. Optional 미세 delta 후보(§4 OQ-G2)만 표면화 |
| quality 동결 개정 규율 | 명시 포섭 → delta 불요 | quality③ "Frozen spec 개정 규율(버전 상승+Revision History)"에 이미 명시 |

---

## 3. 잠재 충돌 지점 (Reconciling 대비 — 타 관심사 교차)

1. **`readiness.openQuestions` 공유 배열.** 본 role은 openQuestions[2항째]("이월 개정 일괄")만 수정(D4). openQuestions[1항째]("형태 B 착수 시점")·[3항째]("정식 등재 채택 여부")는 architectureDirection.open 미러로 **arch-pipeline 관심사**. 동일 배열의 서로 다른 원소를 두 role이 수정 → Reconciling에서 배열 병합 정합 필요(원소 충돌 아님·같은 리스트 동시 편집).
2. **D3 constraints solution-design-data/ 열거.** 백엔드 신설 근거(DP-1)는 arch/pipeline 소관과 교차(§2 D3 cross-cutting 주). 열거 현행화는 governance이나, arch-pipeline이 architectureDirection.decisions에 solution-design-data/ 배치를 반영한다면 두 필드 간 정합 필요.
3. **`intent`·`architectureDirection` 현행화.** arch-pipeline 소관. v1 이후 확정 결정(v1.2.1 Layer 재구성·Solution Design 성숙 루프 신설·루트 문서버전 v1.4)을 architectureDirection.decisions에 반영 시, 본 role의 requirements 라벨 검증(§1)이 그 근거 컨텍스트를 제공 — 라벨 정확성과 아키텍처 결정 문면이 어긋나지 않도록 교차 확인.
4. **`readiness.confidenceVector.risk`(0.75).** 본 role의 risks 현행화(D2)가 리스크 필드 불확실성을 감소시켜 risk confidence 상향 여지 발생. 단 confidenceVector 재선언은 **Readiness 재선언·사용자 게이트 결속**이므로 본 proposal은 변경 제안하지 않음(Reviewing/게이트 소관). arch-pipeline 또는 통합 리뷰가 조정 시 정합 필요.

---

## 4. open (open_questions — Reviewing/게이트 위임)

- **OQ-G1**: D1 v2 문면 최종 선택 — (a) "분해(Decompose 완료 조건 3건·reason 4종)" spec-anchored[권장] vs (b) "분해(Decompose)" 일반형 vs (c) "C1~C4" 유지 + decompose-rules.md 검사 규칙 재수식. 셋 다 오귀속 해소·의미 동등. Reviewing 결정.
- **OQ-G2**: 완전성 주장 규율(L-24)의 quality 명시화 여부 — 본 role 판정 = 실질 포섭(delta 불요). 명시 강화를 원하면 quality②에 "검사 범위 정직·전수 스캔(06 VT-4/INV-4)" 미세 delta 가능. 게이트/Reviewing 판단.
- **OQ-G3**: confidenceVector.risk 상향 여부(§3-4) — Readiness 재선언 결속. 본 role 비결정.
- **OQ-G4 (비차단·이월)**: 02 §3.7 자기 불일치·03 §3.1-B bare "§3.7"·03 §7 done-11 stale·CP1~CP3 인용 앵커·루트 §12.1 flat 정의 — 02·03·루트 spec 무수정 원칙에 따라 **Contract 필드 밖 이월**(v1.4 §8 동형). Contract 요구 라벨 검증 범위 밖(본 role 무처리·기록만).
