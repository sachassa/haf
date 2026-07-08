시연 CP2 리포트 — v0.7 시연 wf-t1 (실계약 CP2 리포트 아님)

# verify-t1 — v0.7 시연 Task wf-t1 검증 리포트

스키마: framework/verifier/verification-report.md §2·§3·§4 (정본 06 §3.2-A/B/C). v0.6 시연 CP2 리포트(docs/v0.6-demo-fixtures/verify-a.md) 동형의 경량 형식 — 마일스톤 CP2 아님.

## §1. target

- 산출물: docs/v0.7-demo-fixtures/out-t1.md
- 대상 작업: v0.7 시연 Task wf-t1 (3-Task 병렬 집합 T1 — produces 계약 X) Execute 산출물

## §2. criteria_basis

- 위임 완료 조건 — docs/v0.7-demo-fixtures/fixture-t1-spec.md §B done 3항 (①②③).
- 참고 입력(판정 근거 아님, 06 V1): Worker 완료 보고 self_check "①②③ 충족" 주장. 이 주장은 검사 대상(claim)으로만 취급하고, 아래 items는 산출물 자체를 근거로 독립 재판정한 결과다.

## §3. items (항목별 판정 3건)

| # | criterion | verdict | evidence | scope | verification_type |
|---|---|---|---|---|---|
| 1 | §B① out-t1.md에 `## 용어: 베타`·`## 용어: 알파`·`## 용어: 감마` 3개 헤더가 베타 → 알파 → 감마 등장 순서로 존재한다. | 충족(Met) | 산출물 전 행 헤더 패턴 전수 추출 결과 `##` 헤더는 정확히 3건 — 3행 `## 용어: 베타`, 6행 `## 용어: 알파`, 9행 `## 용어: 감마`. 등장 순서 베타(3행) → 알파(6행) → 감마(9행) 일치, 그 외 헤더 0건. | out-t1.md 본문 전체(10줄)의 헤더 행 전수 스캔. | VT-2 (완료 조건 대조 검증) |
| 2 | §B② 각 헤더 바로 아래에 `- 정의:` 로 시작하는 줄이 정확히 1개씩 있다. | 충족(Met) | 산출물 전 행에서 `- 정의:` 시작 줄은 정확히 3건 — 4행·7행·10행. 각각 헤더 바로 다음 행(3→4, 6→7, 9→10)이며, 헤더당 1개(누락 0, 초과 0, 헤더와 정의 사이 개입 행 0). | out-t1.md 본문 전체(10줄)의 `- 정의:` 시작 행 전수 스캔 + 헤더-정의 인접성 행 번호 대조. | VT-2 (완료 조건 대조 검증) |
| 3 | §B③ 산출 위치가 `docs/v0.7-demo-fixtures/out-t1.md`다. | 충족(Met) | 디렉터리 실측에 docs/v0.7-demo-fixtures/out-t1.md 존재(425바이트), 해당 경로 파일 열람 성공(10줄, 내용 접근 가능). | docs/v0.7-demo-fixtures/ 디렉터리 전체 목록 실측 + 해당 경로 파일 본문 열람. | VT-1 (산출물 존재 검증) |

## §4. final_verdict

**통과(Pass)** — 충족 3 / 위반 0 / 판정 불가 0. 도출: 모든 항목 충족 → 통과 (06 §3.2-C, 결정적 — INV-5).

거짓 완료 보고 검출(06 §3.2-F): Worker self_check("①②③ 충족")를 신뢰하지 않고 동일 기준 3건을 산출물 실측(라인 인용·개수·순서 대조)으로 재판정한 결과, 주장과 재판정 간 모순 0건 — 거짓 완료 보고 미검출.

## §5. verifier_scope

- 검사한 범위: out-t1.md 본문 전체(10줄 — 헤더 행·`- 정의:` 행 전수 스캔, 행 번호 기반 인접성·순서 대조), docs/v0.7-demo-fixtures/ 디렉터리 파일 목록 실측, fixture-t1-spec.md §A·계약 X·§B(대조 기준 원천).
- 검사하지 않은·제외한 범위: 픽스처 디렉터리 밖 저장소 전체(specs/·framework/ 등 — 시연 격리, CP2 전수 스캔 제외 verifier_scope), 형제 Task 픽스처·산출물(fixture-t2-spec.md·fixture-t3-spec.md·out-t2.md·out-t3.md — 본 판정 대상 아님), 픽스처 spec 자체의 의도적 결함 정당 보유 명시(판정 대상 아님 — 위임 constraints; 단 fixture-t1-spec §B는 T1 자기 파일에 심긴 결함 없음을 명시하며, 본 판정은 산출물 실측으로만 성립한다). 본 리포트의 판정은 이 검사 범위 안에서만 성립한다.
- 비구현(INV-6): 본 검증에서 생성한 저장소 파일은 이 리포트 1개뿐이며, 판정 대상 산출물·픽스처·다른 파일은 수정하지 않았다.

## §6. rework

없음 (final_verdict = Pass).
