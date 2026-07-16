# Reconciling 기록 — maturation-r001 (충돌 검출 + Trade-off 해소)

기록: 주 세션(Advisor) Orchestrator 규약 절차 · 2026-07-13 · 04 §3.4-D ②③(Conflict Detection·Trade-off Resolution)
입력: `proposal-arch-pipeline.md`(A1~A5·C1~C6·OQ-AP-1~3) · `proposal-governance-consistency.md`(D1~D4·비-delta 6·충돌 1~4·OQ-G1~4)
성격: 성숙 실행 메타(코어 밖 — SP-INV 2·3).

## 1. 충돌 검출 (양측 선언 충돌 후보 전수 대조)

두 Proposal이 각자 선언한 잠재 충돌 후보(arch C1~C6·gov 1~4)를 상호 대조했다. 실제 delta 편집 지점 대조 결과 **동일 필드·동일 원소를 상충 방향으로 편집하는 실충돌은 0건**이며, 전부 배분·정합·병합 사안이다.

| # | 후보 (출처) | 판정 | 해소 |
|---|---|---|---|
| R-1 | stale 경로 정정 소유 배분 (C1·OQ-AP-3) | 비충돌(배분) | 아키텍처 필드 내 경로(`uaf/specs/03`→`planning/specs/03`) = arch-pipeline delta / 요구 라벨(f3-b) = governance delta. 실제 편집 지점 대조: 중복 0·누락 0. 동일 규율(v1.2.1 `uaf/` 물리 소멸) 공유 — v2 본문 미러의 잔여 stale 경로(v1 본문 헤더 "uaf/specs/03"·Readiness "uaf/specs/02")도 같은 규율로 Reviewing에서 일괄 처리(RD-10). |
| R-2 | intent 공동 편집 (C2·gov 3) | 불성립 | governance Proposal에 intent delta 부재(실측) → arch A1 단독. 병합 불요. |
| R-3 | readiness.openQuestions 배열 병합 (C3·gov 1) | 비충돌(병합) | 원소 소유 분리 — [1 형태 B]·[3 정식 등재] = arch(A4) / [2 이월 개정] = governance(D4). 3원소 병합 정합 확인·원소 충돌 0. |
| R-4 | 형태 B open 확대 vs risks[2] 문면 (C4) | 경미 정합 필요 → **T-1** | arch A3이 open 1에 "Solution Design 실행 호스팅"을 합류시키는데 governance는 risks[2]를 무변 존속 판정 — 두 필드 간 범위 서술 어긋남. **Trade-off T-1**: risks[2]에 최소 부기 "(… OQ 4건 **+ Solution Design 실행 호스팅[v1.4 합류]**)"로 정합(§2). |
| R-5 | 본문 "미결 N항" 재계수 (C5) | 조건부 | open 3(신규 등재) 채택 여부에 결속 — Reviewing 권고 = 채택(사용자 게이트 최종 확정). 채택 시 본문 "미결 2항"→"미결 3항" 재계수(L-25). |
| R-6 | confidenceVector 조정 여부 (C6·OQ-G3) | 결정 필요 → **T-2** | **Trade-off T-2**: 전 차원 존치(0.85/0.80/0.85/0.75/0.90 무변). 근거 — 성숙 run은 Confidence Model(Discovery 소관)을 구동하지 않았고 값은 종단 판정 산출 기록이므로 모델 근거 없는 상향은 무근거 조정. 재선언은 동일 값 + 새 userApproval 기록으로 표현. |
| R-7 | constraints D3 열거 확장 vs A2 decisions (gov 2) | 비충돌(정합 확인) | A2 결정 2는 4경계 유지 서술·solution-design-data/는 Adapter 경계 이하 데이터 — 충돌 0. D3 채택 가능. |

## 2. Trade-off 결정 기록 (04 §3.4-D ③)

| # | 선택지 | 결정 | 근거 |
|---|---|---|---|
| T-1 | risks[2] 무변 vs 최소 부기 | **최소 부기** | open 1(A3)과 risks[2]의 형태 B 미결 범위 서술 정합 — 두 필드가 서로 다른 계수를 시사하면 v2 내부 불일치 신설. 최소 변경(부기 1구). |
| T-2 | confidenceVector 상향 vs 존치 | **존치(무변)** | 무근거 조정 금지 — 모델 미구동·산출 기록 성격. |
| T-3 | A1 intent 최소안 vs fuller(v1.2.1 포함) (OQ-AP-2) | **최소안** | 필드 귀속 정확성(구조 결정은 decisions 소관)·최소 변경·6-Layer 수직 스택과 최상위 5-Layer의 네임스페이스 혼동 방지(루트 §0). v1.2.1은 A2(decisions)에 배치. |
| T-4 | A2 제자리 현행화 vs 5번째 결정 항 신설 | **제자리 현행화(4항 유지)** | 본문 "결정 4항" 재계수 무변(L-25)·최소 변경. |
| T-5 | D1 문면 (a) spec-anchored vs (b) 일반형 vs (c) 재수식 (OQ-G1) | **(a)** "분해(Decompose 완료 조건 3건·reason 4종)" | 라벨을 07 정본 실측 표현에 정박 — 동종 결함(L-25 커널)의 재발을 문면 자체가 차단. |
| T-6 | OQ-G2 L-24 quality 명시화 | **delta 불요(포섭 판정 수용)** | governance 실측 판정 수용 — 기존 quality②가 실질 포섭. 미세 delta는 이득 대비 문면 팽창. |

## 3. 종결 판정

- **잔여 충돌 0** ∧ trade-off 결정 기록 완료(T-1~T-6) → **T4 Guard 충족** (`Reconciling`→`Reviewing`).
- 재제안 필요(T5 경로) 항목 0 — 두 Proposal의 delta는 상호 보완적이며 추가 Proposal 없이 통합 가능.
- 게이트 이월 항목(사용자 최종 확정): open 3 신규 등재(OQ-AP-1)·통합 리뷰의 정합 완결 추가(RD-11, Reviewing에서 식별) — Validating에서 제시.
