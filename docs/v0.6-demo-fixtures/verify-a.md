시연 검증 리포트 — 실계약 CP2 리포트 아님 (v06-demo-a Verify 산출)

# verify-a — 시연 사이클 ⓐ 검증 리포트 (cycle_id: v06-demo-a)

프로토콜: framework/verifier/verifier-protocol.md 5단계 (입력 수령 → 기준 확인 → 항목별 판정 → 최종 판정 도출 → 리포트 산출). 스키마: framework/verifier/verification-report.md §2·§3·§4 (정본 06 §3.2-A/B/C). 시연 사이클용 경량 리포트.

## §1. target

- 산출물: docs/v0.6-demo-fixtures/output-a.md
- 대상 작업: v0.6 시연 사이클 ⓐ (cycle_id=v06-demo-a) Execute 산출물

## §2. criteria_basis

- 위임 완료 조건 — docs/v0.6-demo-fixtures/fixture-a-spec.md §B done 3항 (①②③).
- 참고 입력(판정 근거 아님, 06 V1): Worker 완료 보고 claim "done ①②③ 전건 예". 이 주장은 검사 대상으로만 취급하고, 아래 items는 산출물 자체를 근거로 독립 재판정한 결과다.

## §3. items (항목별 판정 3건)

| # | criterion | verdict | evidence | scope | verification_type |
|---|---|---|---|---|---|
| 1 | §B① `docs/v0.6-demo-fixtures/output-a.md`가 존재한다. | 충족(Met) | 디렉터리 실측에 해당 파일 존재, 파일 열람 성공(14줄, 내용 접근 가능). | docs/v0.6-demo-fixtures/ 디렉터리 전체 목록 실측 + 파일 본문 열람. | VT-1 (산출물 존재 검증) |
| 2 | §B② 표에 §0의 5개 항목이 전건(사과·바나나·포도·오렌지·딸기) 포함된다. | 충족(Met) | output-a.md 표 데이터 행 5건(본문 9~13행)에 사과·바나나·포도·오렌지·딸기 전건 존재. 누락 0, §0 밖 항목 0. | §0 항목 5건 후보 집합 전체 ↔ 산출물 표 전 행 전건 대조(전수). | VT-2 (완료 조건 대조 검증) |
| 3 | §B③ 각 항목에 설명이 1줄씩 있다. | 충족(Met) | 5개 행 각각의 설명 열에 1줄 설명 존재(예: 사과 — "붉은 껍질의 둥근 과일이다."). 빈 설명 0, 2줄 이상 0. | 산출물 표 5행 전 행의 설명 열 전수 검사. | VT-2 (완료 조건 대조 검증) |

## §4. final_verdict

**통과(Pass)** — 충족 3 / 위반 0 / 판정 불가 0. 도출: 모든 항목 충족 → 통과 (06 §3.2-C, 결정적 — INV-5).

거짓 완료 보고 검출(06 §3.2-F): Worker claim("done ①②③ 전건 예")을 신뢰하지 않고 동일 기준 3건을 산출물 실측으로 재판정한 결과, 주장과 재판정 간 모순 0건 — 거짓 완료 보고 미검출.

## §5. verifier_scope

- 검사한 범위: output-a.md 본문 전체(14줄, 표 5행 전 행), docs/v0.6-demo-fixtures/ 디렉터리 파일 목록, fixture-a-spec.md §0(대조용 원본 데이터)·§A·§B.
- 검사하지 않은·제외한 범위: 픽스처 디렉터리 밖 저장소 전체(specs/·framework/ 등 — 시연 격리, v0.6-demo-procedure §4.2에 따라 CP2 전수 스캔 제외), 시연 ⓑ·ⓒ 픽스처(fixture-b-spec.md·fixture-c-spec.md — 본 판정 대상 아님). 본 리포트의 판정은 이 검사 범위 안에서만 성립한다.
- 비구현(INV-6): 본 검증에서 생성한 저장소 파일은 이 리포트 1개뿐이며, 판정 대상 산출물은 수정하지 않았다.

## §6. rework

없음 (final_verdict = Pass).
