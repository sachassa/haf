시연 CP2 리포트 — v0.7 시연 wf-t3

# verify-t3 — Task wf-t3 검증 리포트 (CP2 독립 판정)

스키마: framework/verifier/verification-report.md §2·§3·§4 (정본 06 §3.2-A/B/C). 시연용 경량 리포트.

## §1. target

- 산출물: docs/v0.7-demo-fixtures/out-t3.md
- 대상 작업: v0.7 시연 3-Task 병렬 집합의 T3 (wf-t3, consumes 확정 계약 Y) Execute 산출물

## §2. criteria_basis

- 위임 완료 조건 — docs/v0.7-demo-fixtures/fixture-t3-spec.md §B done 4항 (①②③④).
- 판정 기준은 T3 자기 spec(§B)뿐이다. out-t2.md 실물과의 대조는 본 판정 대상이 아니다(위임 input 명시 — Merge 소관).
- 참고 입력(판정 근거 아님, 06 V1): Worker self_check. 검사 대상(claim)으로만 취급하고, 아래 items는 산출물 자체 실측(문면 대조·줄 계수)으로 독립 재판정한 결과다.

## §3. items (항목별 판정 4건)

| # | criterion | verdict | evidence | scope | verification_type |
|---|---|---|---|---|---|
| 1 | §B① 확정 계약 Y 문면("out-t2.md는 2열 표로 용어 3개를 가나다 순(감마 → 베타 → 알파)으로 나열한다")의 인용이 존재한다. | 충족(Met) | out-t3.md 9행(§1 인용 블록)에 계약 Y 문면 전문이 문자 단위로 일치하는 인용으로 존재 — exact-string 대조 1건 검출. spec §B①의 요구 문장과 문면 동일. | out-t3.md 본문 전체(21줄)에 대한 계약 Y 문면 exact-string 전수 대조 + 본문 열람. | VT-2 (완료 조건 대조 검증) |
| 2 | §B② "색인은 가나다 순(감마 → 베타 → 알파)으로 정렬되어 있다"는 사용 문장이 존재한다. | 충족(Met) | out-t3.md 13행(§2 사용 안내) 문두에 요구 문장이 문자 단위로 일치하여 존재 — exact-string 대조 1건 검출. | out-t3.md 본문 전체(21줄)에 대한 사용 문장 exact-string 전수 대조. | VT-2 (완료 조건 대조 검증) |
| 3 | §B③ 용어 3개(감마·베타·알파) 각각의 색인 참조 줄 3개가 존재한다. | 충족(Met) | out-t3.md 19·20·21행(§3 색인 참조)에 감마(19행)·베타(20행)·알파(21행) 각 1줄씩 색인 참조 줄 총 3개 존재 — 줄 계수 실측 3/3, 용어별 누락 0·중복 0. | out-t3.md 본문 전체(21줄)에서 색인 참조 줄 패턴 전수 검색 — 검출 3행이 용어 3개 후보 집합 전체와 1:1 대응. | VT-2 (완료 조건 대조 검증) |
| 4 | §B④ 산출 위치가 `docs/v0.7-demo-fixtures/out-t3.md`다. | 충족(Met) | docs/v0.7-demo-fixtures/ 디렉터리 실측 목록에 out-t3.md 존재, 해당 경로 파일 열람 성공(21줄, 내용 접근 가능). | docs/v0.7-demo-fixtures/ 디렉터리 전체 목록 실측 + 해당 경로 파일 본문 열람. | VT-1 (산출물 존재 검증) |

## §4. final_verdict

**통과(Pass)** — 충족 4 / 위반 0 / 판정 불가 0. 도출: 모든 항목 충족 → 통과 (06 §3.2-C, 결정적 — INV-5).

거짓 완료 보고 검출(06 §3.2-F): Worker self_check를 판정 근거로 삼지 않고(V1) §B done 4항 전건을 산출물 실측으로 독립 재판정한 결과, 완료 주장과 모순되는 실측 0건 — 거짓 완료 보고 미검출.

## §5. verifier_scope

- 검사한 범위: out-t3.md 본문 전체(21줄 — §1 인용·§2 사용 안내·§3 색인 참조 전 절), docs/v0.7-demo-fixtures/ 디렉터리 파일 목록 실측, fixture-t3-spec.md(§A 작성 지시·계약 문면 절·§B done 4항 — 대조 기준 원본).
- 검사하지 않은·제외한 범위: out-t2.md 실물과의 대조(위임 input 명시 제외 — Merge 소관; 계약 Y 문면의 사실성, 즉 out-t2.md가 실제로 그렇게 나열하는지는 본 판정 범위 밖), out-t1.md·fixture-t1-spec.md·fixture-t2-spec.md(본 판정 대상 아님), 픽스처 디렉터리 밖 저장소 전체(specs/·framework/ 등 — 시연 격리, fixture-t3-spec 머리말·v0.7-demo-procedure §4.1에 따라 CP2 전수 스캔 제외). 본 리포트의 판정은 이 검사 범위 안에서만 성립한다.
- 비구현(INV-6): 본 검증에서 생성한 저장소 파일은 이 리포트 1개뿐이며, 판정 대상 산출물·픽스처는 수정하지 않았다.

## §6. rework

없음 (final_verdict = Pass).
