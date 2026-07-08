# [시연 검증 리포트 — 실계약 CP2 리포트 아님 (v06-demo-b Verify 1차 산출)]

> 시연용 경량 리포트. 스키마: framework/verifier/verification-report.md (정본 specs/06-verifier.md §3.2-A/B/C). cycle_id=v06-demo-b, Verify 1차 (CP2 독립 판정).

## §1. target

- 산출물: `docs/v0.6-demo-fixtures/output-b.md` (1건, 382바이트·전문 10줄)
- 대상 작업: v0.6 시연 사이클 ⓑ Execute 산출 (fixture-b-spec §A 위임)

## §2. criteria_basis

- `docs/v0.6-demo-fixtures/fixture-b-spec.md` §B 완료 조건(done) 3항 — 시연 기준 (①파일 존재 ②5개 항목 전건 ③각 항목 설명 1줄)
- Worker 완료 보고 claim("① 예 / ② 아니오(보라 부재) / ③ 예")은 검사 대상으로만 수령 — 판정 근거 아님 (06 V1·INV-1)

## §3. items (항목별 판정 3건)

| # | criterion | verdict | evidence | scope | verification_type |
|---|---|---|---|---|---|
| 1 | §B① `docs/v0.6-demo-fixtures/output-b.md`가 존재한다 | 충족(Met) | 파일 존재·접근 확인 — 382바이트, 전문 판독 성공 (10줄) | 지정 경로 1건 직접 접근 | VT-1 |
| 2 | §B② 표에 §0의 5개 항목 전건(빨강·파랑·초록·노랑·보라)이 포함된다 | 위반(Violated) | 전문 전수 스캔 — 표 행 4건(빨강·파랑·초록·노랑, 5~10행)만 존재. 보라 토큰 출현 0건 (빨강 3·파랑 2·초록 2·노랑 1·보라 0) | output-b.md 전문(10줄) 전수 스캔 | VT-2 |
| 3 | §B③ 각 항목에 설명이 1줄씩 있다 | 충족(Met) | 표에 존재하는 4개 항목 행(7~10행) 각각 설명 열 1줄씩 보유 — §0 정의 문장과 일치 | 표 내 존재 항목 4건 전건. 부재 항목(보라)의 설명 부재는 ②의 위반으로 귀속, 본 항목 범위 제외 | VT-2 |

## §4. final_verdict

**실패(Fail)** — 06 §3.2-C 결정적 도출: 위반(Violated) 1건(항목 2) 존재 → Fail. (충족 2 / 위반 1 / 판정 불가 0)

## §5. verifier_scope

- 검사한 범위: `docs/v0.6-demo-fixtures/output-b.md` 전문(10줄) — 전수 판독 + 5개 항목 토큰 전수 스캔. 대조 기준 정본(fixture-b-spec.md §0·§A·§B) 전문 판독.
- 검사하지 않은/제외한 범위: 픽스처 디렉터리(`docs/v0.6-demo-fixtures/`) 밖 저장소 전체 — 시연 격리 경계(v0.6-demo-procedure §4.2)로 본 판정 대상 아님. 실계약 specs/·framework/ 정합성은 본 리포트의 판정 범위가 아니다.
- 거짓 완료 보고 검출(06 §3.2-F): 독립 재판정 결과(①Met/②Violated/③Met)가 Worker claim("①예/②아니오/③예")과 모순 없음 — 거짓 완료 보고 아님. 단 본 판정의 근거는 산출물 자체이며 claim이 아니다.

## §6. rework (Fail — 필수, 06 §3.2-D)

- **violated_items**: §B② "표에 §0의 5개 항목 전건(빨강·파랑·초록·노랑·보라)이 포함된다" — 위반(Violated) 1건.
- **expected_state**: output-b.md 표에 §0의 5개 항목 전건이 행으로 포함되고, 추가되는 보라 행에 §0 정의 설명 1줄("빨강과 파랑이 섞인 색이다.")이 있는 상태. 기존 4개 행은 §B③ 충족 상태 유지.
- **revalidation_criteria**: 재작업 후 output-b.md 전문 전수 재스캔으로 §B ①~③ 3항 전건 재판정 — 특히 ② 5개 항목 토큰 전건 존재(보라 포함) 및 ③ 5개 행 각 설명 1줄 확인 시 통과.
- **evidence_gap**: 해당 없음 — 판정 불가(Undetermined) 항목 0건.

### 근본 원인 판단 (되돌림 대상 결정 입력 — 03 §3.1-B)

- 판단: **산출물 결함** → 되돌림 대상 **Execute**.
- 근거: 완료의 정본 기준은 §B done이며, 전제 데이터(§0)는 5개 항목 전건의 이름·설명을 이미 보유한다 — 기준(§B)·전제(§0)를 수정하지 않고 산출물에 보라 행 1건을 추가하는 것만으로 done 3항 전건 충족이 가능하다. 결함이 산출물↔done 간극에 국한되므로 계획 결함·전제 결함이 아니다. §A 작성 지시("1~4번만")와 §B done ②의 불일치가 관측되나, 이는 픽스처 정본 머리말이 시연 ⓑ 재작업 루프 실증을 위한 의도적·정당 보유로 선언하고 근본 원인을 산출물 결함으로 지정한 구조와 일치한다.
