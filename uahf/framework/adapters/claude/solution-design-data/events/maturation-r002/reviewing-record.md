# Reviewing 기록 — maturation-r002 (Integrated Design Review · 단일 일관 결정 집합)

기록: Worker(Advisor 위임) · Orchestrator 규약 절차 · 2026-07-13 · 04 §3.4-D ④⑤(Integrated Design Review·최종 결정 소유권 — 확정 권위는 사용자 게이트)
입력: `proposal-arch-pipeline.md`(단일 역할) + `reconciling-record.md`(cross-role 0·내부 정합 I-1~I-8·T-1~T-6)
성격: 성숙 실행 메타(코어 밖 — SP-INV 2·3). **본 기록의 결정 집합은 확정 후보이며 확정 권한은 Validating 사용자 게이트(T8)다(04 §3.4-C·UAF-INV ⑤). 본 run은 Validating 진입까지이며 T8 미도달(사용자 응답 대기).**

## 1. 단일 일관 결정 집합 (RD-1~RD-9)

| # | 결정 | 출처·해소 | 게이트 성격 |
|---|---|---|---|
| RD-1 | `open[0]` 형태 B 경계 분할 **재기술** — OQ-LB-2 해소·OQ-WB-2 부분 해소(물리 동시 잔여)·OQ-SH-4 해소·SD 실행 호스팅 orchestration 실현·잔여 OQ-VB-2/M5-2/PB-2 | D-open1·위임 ① | **게이트 확정 ①(핵심)** |
| RD-2 | `open[1]` 정식 등재 **존치·미해소** + 명확화(orchestration substrate 소비 ≠ 정식 등재·UAF-INV ①·PC-INV 8) | D-open2·위임 ② | 확인 |
| RD-3 | `open[2]` step 실행기 계열 **갱신** — v1.5 Step Host·v1.6 orchestration Layer 실현(04 §3.9 확장 1·2)·잔여 진화 축(물리 동시·멀티프로젝트·대화형 형태 B·OQ-PO-B4·비용 미터링) open·설계 0 | D-open3·위임 ③ | **게이트 확정 ②(핵심)** |
| RD-4 | `readiness.openQuestions[0]` 현행화 — "형태 B 미착수"→"부분 실현(v1.5/v1.6)" (open[0] 그룹 8 미러) | D-oq0·정합 I-1 | 정합 승인 |
| RD-5 | `constraints[3]` append-only 데이터 열거 확장 — +`step-data/`·`orchestration-data/`(6종) | D-con3·정합 I-7·r001 D3 동형 | 정합 승인 |
| RD-6 | `constraints[4]`·`decisions[3]` 형태 posture 현행화 — "형태 A·실행 코드 0"→"코어 형태 A + 실행 호스팅 형태 B 부분 실현(중립 실행 코드·Core Contract 무변·C-1)" | D-con4·D-dec3·정합 I-3/I-4 | **게이트 확정 ③(posture)** |
| RD-7 | `decisions[1]` 최상위 Layer 현행화 — "5-Layer"→"6-Layer(+orchestration/)"·**제자리·결정 4항 카운트 유지** | D-dec1·T-4 | **게이트 옵션(이연 가능·OQ-R2-3)** |
| RD-8 | `risks[1]` 형태 B 전환 복잡성 계수 정합 — 부분 실현 반영·잔여 OQ 3건(VB-2/M5-2/PB-2)+물리 동시 | D-risk1·정합 I-2·r001 T-1 동형 | 정합 승인 |
| RD-9 | `meta`(instanceVersion 2→3·supersedes 1→2·schemaVersion "1.0" 유지)·`provenance`(maturation-r002·baseline 2·terminal pending)·`userApproval`(placeholder)·본문 미러 정합 | D-meta·D-prov·D-appr·D-body·정합 I-8 | 기계적 |

비변경 확정(전수): `meta.id` `pc-uahf-001` 유지(계보 동일성)·`schemaVersion` "1.0"(D4·PC-INV 4)·`intent` 무변·`requirements`(functional 5·quality 3) 무변·`assumptionLedger` `[]`·`readiness.confidenceVector` 전 차원 존치(T-2)·`readiness.completeness` 무변·`risks[0][2][3]` 무변(risks[2] 이월 계수 = 범위 밖 무촉·T-3)·`readiness.openQuestions[1][2]` 무변·`decisions[0][2]` 무변·`constraints[0][1][2]` 무변. **필드 제거 0(PC-INV 6)** — 모든 delta는 기존 필드 내 문면 정정.

## 2. v2 → v3 diff 요약표 (T8 게이트 제시용 · 위임 output 3·4)

| 필드(그룹) | v2 | v3 후보 | 변경 유형 |
|---|---|---|---|
| `meta.instanceVersion` | 2 | **3** | 성숙 계보 |
| `meta.supersedes` | 1 | **2** | 성숙 계보 |
| `meta.id`·`schemaVersion` | pc-uahf-001·"1.0" | 동일 | 무변(PC-INV 4·계보) |
| `intent` | (v2) | 동일 | 무변 |
| `requirements.*` | 5+3항 | 동일 | 무변 |
| `constraints[3]` | 데이터 4종 append-only | 데이터 **6종**(+step-data/·orchestration-data/) | 열거 확장(정합) |
| `constraints[4]` | 형태 A·**실행 코드 0** | 코어 형태 A + 실행 호스팅 **형태 B 부분 실현** | posture 현행화(게이트 ③) |
| `risks[1]` | 형태 B 전환(경계 OQ 4건+SD) | 부분 실현·잔여 OQ 3건+물리 동시 | 계수 정합 |
| `risks[0][2][3]` | (v2) | 동일 | 무변(risks[2] 범위 밖) |
| `decisions[1]` | 최상위 **5-Layer** | 최상위 **6-Layer**(+orchestration/) | 현행화(게이트 옵션·이연 가능) |
| `decisions[3]` | 현 실현 **형태 A** | 코어 형태 A + 실행 호스팅 형태 B 부분 | posture 현행화(게이트 ③) |
| `decisions[0][2]` | (v2) | 동일 | 무변 |
| `open[0]` | 경계 분할 5-OQ+SD·DP-4 | LB-2 해소·WB-2 부분·SH-4 해소·SD 실현·잔여 VB-2/M5-2/PB-2 | **재기술(게이트 ①)** |
| `open[1]` | 정식 등재 확장 포인트 | 존치·미해소+명확화 | 존치(②) |
| `open[2]` | step 실행기=진화 축·설계 0 | orchestration Layer 실현·잔여 축 open·설계 0 | **갱신(게이트 ②)** |
| `openQuestions[0]` | 형태 B **미착수** | 형태 B **부분 실현** | 현행화(정합) |
| `openQuestions[1][2]` | (v2) | 동일 | 무변 |
| `confidenceVector` | 5차원 값 | 동일 | 존치(T-2) |
| `userApproval` | 승인 2026-07-13(r001) | placeholder(r002 T8 대기) | 후보(미승인) |
| `provenance.maturation` | runId r001·baseline 1·Matured | runId **r002**·baseline **2**·terminal pending | 성숙 run 형식 |

- **PC-INV 준수 요약**: PC-INV 4(schemaVersion SemVer — 무변 "1.0"·파괴 변경 0)·PC-INV 5(tolerant reader — 코어 필드 스키마 무변·provenance must-ignore 유지)·PC-INV 6(**필드 제거 0** — 전 delta 기존 필드 내 정정)·PC-INV 9(append-only — supersedes 2·v2 문면 byte 불변). SP-INV 2·3(성숙 실행 메타는 이 run 디렉터리 파일에만·코어 필드 유입 0)·SP-INV 8(최소 할당 역할 1).

## 3. 게이트 제시 항목 (Validating — 사용자 확정 필요 · Advisor가 T8에 제시)

**본 run은 여기(Validating 진입)까지이며 T8 미도달.** 아래는 Advisor가 사용자 게이트(T8)에서 제시할 항목이다 — 승인 시 Advisor가 v3 발행(contract-binding §4.2 경로).

1. **결정 집합 전체 승인 여부**(RD-1~RD-9 — 승인 시 T8 → `Matured` → v3 발행).
2. **① open[0] 형태 B 경계 분할 재기술**(RD-1) · **② open[2] orchestration Layer 실현 갱신**(RD-3) · **③ 형태 posture 현행화**(RD-6 — constraints[4]·decisions[3]).
3. **게이트 옵션 — decision[1] 6-Layer 현행화 채택 vs 이연**(RD-7·OQ-R2-3): 실측(6 Layer)상 현행화 권고이나, orchestration Baseline 승격 유보 고려 시 이연(v2 "5-Layer" 유지·open[2]만 orchestration 반영) 선택 가능.
4. **확인 항목**: OQ-R2-1(SP-INV 1 — Matured 기준선 정합, 04 명확화 권고) · OQ-R2-2(OQ-SH-4 open[0] 편입 = 인접 해소 문맥, 목록 제거 아님) · OQ-R2-4(거버넌스/이월 축 범위 밖 — risks[2]·openQuestions[1] 무촉·별도 run 소관).
5. **Projection 신규 0건 확인**(policy (다) existingCanonical — ARCHITECTURE.md·ROADMAP.md·orchestration/ARCHITECTURE.md·orchestration/ROADMAP.md·uahf/ROADMAP.md 실재 → 전 유형 강제 금지·동적 선택 결과 0).
6. 수정 요청 시 T10(`Reviewing` 재진입)·중단/위임 시 T11(`Escalated`).

## 4. v3 후보 문면 소재

- **후보 전문** = `candidate/project-contract.v3.CANDIDATE.md`(본 run 디렉터리 내·contracts/uahf/ 밖·발행 아님). instanceVersion 3·supersedes 2·schemaVersion "1.0"·v2 문면 불변. 파일 머리에 **CANDIDATE 배너**·`userApproval`/`terminal` placeholder로 미발행 표기.
- r001은 초안 전문을 reviewing-record §2에 인라인 삽입했으나, r002는 위임 지시대로 후보를 **별도 파일**(`candidate/`)로 둔다. 본 기록은 결정 집합·diff·게이트 항목을 소유하고 후보 문면은 참조한다.
