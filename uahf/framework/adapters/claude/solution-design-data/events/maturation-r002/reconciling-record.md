# Reconciling 기록 — maturation-r002 (충돌 검출 + Trade-off 해소)

기록: Worker(Advisor 위임) · Orchestrator 규약 절차 · 2026-07-13 · 04 §3.4-D ②③(Conflict Detection·Trade-off Resolution)
입력: `proposal-arch-pipeline.md`(단일 역할 — D-open1/2/3·D-oq0·D-con3/4·D-dec1/3·D-risk1·D-meta/prov/appr/body·OQ-R2-1~4)
성격: 성숙 실행 메타(코어 밖 — SP-INV 2·3).

## 1. 충돌 검출 (cross-role 실충돌 0 명시)

- **단일 역할 run**: 본 run은 `arch-pipeline` **단일 역할**이다(assessing-judgment §3 — 관심사 1·최소 할당 SP-INV 8). 동시 작성 병렬 산출물이 **부재**하므로 **역할 간 상충(cross-role conflict) 대상이 0건**이다. 04 §3.4-B의 T5(재제안 필요)·T7(잔여 충돌 재노출) 유발 조건(다중 Proposal 상충)은 성립하지 않는다.
- 따라서 Reconciling은 04 §3.4-D ②(Conflict Detection)를 **내부 정합 검증**으로 수행한다 — 형태 B 실현 파급 delta들이 v3 후보 내부에서 **자기모순 없이** 정합하는지 확인한다(단일 인스턴스 수렴·04 §3.4-C).

### 1.1 내부 정합 점검 (v3 후보 자기무모순)

| # | 점검 지점 | 결과 |
|---|---|---|
| I-1 | `open[0]`(형태 B 부분 실현) ↔ `openQuestions[0]`(형태 B 부분 실현·그룹 8 미러) | 정합 — 둘 다 "부분 실현·물리 동시/OQ-PO-B4 잔여". 모순 0. |
| I-2 | `open[0]`(LB-2 해소·WB-2 부분·잔여 VB-2/M5-2/PB-2) ↔ `risks[1]`(형태 B 전환 복잡성·잔여 OQ 3건) | 정합 — risks[1] 잔여 계수(3건 VB-2/M5-2/PB-2)가 open[0] 잔여와 일치. v2 내부 계수 불일치 신설 0. |
| I-3 | `constraints[4]`(코어 형태 A + 실행 호스팅 형태 B 부분) ↔ `decisions[3]`(동일) | 정합 — 쌍으로 동일 posture. 모순 0. |
| I-4 | `constraints[1]` C-1(Core Contract 무변) ↔ D-con4/D-dec3(형태 B 부분) | 정합 — 형태 B는 **실행 호스팅**(중립 모듈)·Core Contract 무변 명시 → C-1 훼손 0(불변 보전). |
| I-5 | `open[2]`(orchestration 진화 축·잔여) ↔ `decisions[1]`(orchestration/ 최상위 Layer·구조) | 정합·비중복 — decisions[1]=구조/존재(6 Layer)·open[2]=진화 축/잔여 OQ. 서로 다른 관점, 모순 0. |
| I-6 | `open[0]`(SD 실행 호스팅 "실현") ↔ `open[2]`(OQ-PO-B4 완전 성숙 run 잔여) | 정합·이중 등재 회피 — open[0]은 "형태 B 호스팅 실현"만·완전 비픽스처 run 상세는 open[2] OQ-PO-B4로 단일 소재. |
| I-7 | `constraints[3]`(6 데이터 디렉터리 append-only) ↔ 실측(6 디렉터리 실재) | 정합 — 열거 = 실측. 새 제약 창설 0(동일 append-only 원칙 확장). |
| I-8 | `meta`(instanceVersion 3·supersedes 2·schemaVersion "1.0") ↔ PC-INV 4·6·9 | 정합 — 파괴 변경 0·필드 제거 0·supersedes 계보·schemaVersion 무변. |

**내부 실충돌 0** — 전 delta가 "형태 B 실현(v1.5/v1.6)" 단일 사실의 정합적 파급이며 자기모순 신설 0.

## 2. Trade-off 결정 기록 (04 §3.4-D ③)

| # | 선택지 | 결정 | 근거 |
|---|---|---|---|
| T-1 | 정합 파급 전량 반영 vs 최소분만 | **최소분만(내부 모순 방지 필수분)** | "최소 성숙" 원칙(위임). 핵심 성숙(open 3항) + 그와 **자기모순을 유발하는** 필드(openQuestions[0]·constraints[3][4]·decisions[3]·risks[1])만 정합. 비파급 필드(intent·requirements·confidenceVector·risks[2]·openQuestions[1]) 무촉. |
| T-2 | `confidenceVector` 상향 vs 존치 | **존치(무변)** | 무근거 조정 금지 — 성숙 run은 Confidence Model(Discovery 소관) 미구동·값은 종단 판정 산출 기록. orchestration 실현이 architecture confidence 상향 여지를 주나 모델 근거 없는 상향은 무근거. r001 T-2 동형. |
| T-3 | 거버넌스/이월 축(risks[2]·openQuestions[1]) 재감사 vs 무촉 | **무촉(범위 밖)** | 본 run = 단일 아키텍처 역할. 이월 계수(7건) 재산정은 라벨/이월 전수 재감사를 요하며 이는 governance-consistency 유형 역할·별도 run 소관(추측 재산정 금지 — O4). 범위 한계 정직 명시(OQ-R2-4). |
| T-4 | `decisions[1]` 6-Layer 현행화 채택 vs 이연 | **후보 채택(제자리·카운트 무변) + 게이트 이연 옵션 제시** | 실측(6 Layer)상 v2 "5-Layer" stale → 현행화가 정확. 단 orchestration Baseline 승격 유보 고려 → **가장 이연 가능한 게이트 옵션**으로 제시(사용자가 이연 시 v2 "5-Layer" 유지·open[2]만 orchestration 반영). OQ-R2-3. |
| T-5 | OQ-SH-4 open[0] 문맥 편입 vs 엄격 5-OQ 목록 유지 | **문맥 편입(인접 해소) + 게이트 확인** | SH-4는 형태 B/Step Host 축 인접 진척. v2 5-OQ 목록의 "제거"가 아니라 "인접 해소 문맥"임을 명시. 엄격주의 대안은 게이트 선택(OQ-R2-2). |
| T-6 | v3 발행 vs 후보 정지 | **후보 정지(Validating 대기)** | 위임 제약 — v3 발행(contracts/uahf/ 파일 생성)은 T8 승인 후 Advisor 소관. 본 run은 Validating에서 정지·후보는 run 디렉터리 `candidate/`에만. |

## 3. 종결 판정

- **cross-role 실충돌 0**(단일 역할) ∧ **내부 정합 실충돌 0**(I-1~I-8) ∧ trade-off 결정 기록 완료(T-1~T-6) → **T4 Guard 충족** (`Reconciling`→`Reviewing`).
- 재제안 필요(T5 경로) 항목 0 — 단일 Proposal이 담당 관심사를 완결하며 추가 Proposal 불요.
- 게이트 이월 항목(사용자 최종 확정): open 3항 성숙(핵심)·정합 파급 승인·decision[1] 6-Layer 채택/이연(OQ-R2-3)·OQ-SH-4 편입 확인(OQ-R2-2)·SP-INV 1 정합(OQ-R2-1)·거버넌스 범위 밖 확인(OQ-R2-4) — Validating에서 제시(단, 본 run은 제시 직전 Validating 진입까지·T8 미도달).
