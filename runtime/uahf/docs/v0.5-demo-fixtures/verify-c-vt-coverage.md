# [시연 산출물 — 실계약 문서 아님] verify-c — 검증 리포트 인스턴스 (시연 ⓒ 검증 유형 VT-1~VT-5 적용)

> **시연 산출물 — 실계약 문서 아님.** v0.5 Verifier 시연(Task V8) 수행 중 Verify 연산으로 산출한 검증 리포트 인스턴스다. CP2 리포트가 아니다. verifier-binding.md §4.1 6필드 절 구조로 직렬화한다. `docs/v0.5-demo-fixtures/` 내부에 둔다.

정본: 06 §3.2-E(VT-1~VT-5), criteria-catalog.md §2, verification-report.md §2/§3.

---

## §1. target

- 산출물: `framework/verifier/verification-report.md`·`framework/verifier/criteria-catalog.md`(실계약 확정본) + 시연 ⓑ 결정성 재현(verify-b-run1/run2).
- 대상 작업 식별자: v0.5 시연 ⓒ — VT-1~VT-5 각각 최소 1개 판정 항목 적용.

## §2. criteria_basis

- 부류: **규격 / 위임 완료 조건 / 경계 규칙 / 시연 기준** (criteria-catalog §4 — VT별 대응 부류; 06 §3.2-A).
- 기준: "VT-1(산출물 존재)·VT-2(완료 조건 대조)·VT-3(규격 준수)·VT-4(경계)·VT-5(시연) 각각이 최소 1개 판정 항목에 적용되고, 유형별 판정 방법(criteria-catalog §2 정본 셀)대로 verdict가 도출된다."

## §3. items (항목별 판정 — 06 §3.2-B 5필드; VT-1~VT-5 각 1건 이상)

| # | `criterion` | `verdict` | `evidence` | `scope` | `verification_type` |
|---|---|---|---|---|---|
| 1 | framework/verifier/verification-report.md 산출물이 실재·접근 가능 | 충족(Met) | 파일 조회로 실재·전문 판독 확인 | 산출물 파일 실재 | **VT-1** |
| 2 | V1 문서가 위임 완료 조건(검증 리포트 6필드·5필드·도출 규칙 인스턴스화)을 충족 | 충족(Met) | verification-report.md §2(6필드)·§3(5필드)·§4(도출 규칙) 표가 done 항목과 1:1 대조 | verification-report.md §2/§3/§4 | **VT-2** |
| 3 | criteria-catalog.md §2가 06 §3.2-E VT-1~VT-5 5행을 판정 대상·판정 방법·충족 조건 셀 단위로 보존 | 충족(Met) | criteria-catalog.md §2 표 5행 셀 단위 대조 — 재정의·확장 0 | criteria-catalog.md §2 | **VT-3** |
| 4 | framework/verifier/criteria-catalog.md 본문에 금지 요소 후보 부류 전체(①~④) 0건 | 충족(Met) | 본문 전수 스캔 — 매치 분류: 저장소 문서 식별자(specs/…·framework/…·docs/…)·정본 열거 어휘(충족/위반/판정 불가·VT-1~VT-5)만, 부류 ①~④ 금지 토큰 실증 0건 | criteria-catalog.md 본문 전문 + 후보 부류 전체 | **VT-4** |
| 5 | 시연 ⓑ 결정적 생성(동일 입력 2회 → 문면 동일)이 기대대로 재현 | 충족(Met) | verify-b-run1 / verify-b-run2 내용 해시 동일(명령 실행 도구 재관측) — 시연 시나리오 실제 재현·독립 재확인 | verify-b 2파일 대조 | **VT-5** |

- **다중 유형 대응(06 §3.2-E 도입).** 한 항목이 둘 이상 유형에 대응할 수 있다(예: item #2는 완료 조건 대조이자 규격 대조 성격 — VT-2 주, VT-3 병기 가능). 본 리포트는 각 유형이 최소 1건 적용됨을 보이기 위해 유형별 대표 항목을 배정했다.

## §4. final_verdict

- **Pass (통과).** 모든 항목(#1~#5)이 충족(Met)이므로 06 §3.2-C("모든 항목 충족 → 통과")로 결정적으로 도출한다.

## §5. verifier_scope

- **검사한 범위:** 위 §3 각 항목의 scope 열(각 산출물의 지정 절 + VT-4 항목의 본문 전문·후보 부류 전체 + VT-5 항목의 2파일 해시 대조).
- **검사하지 못했거나 제외한 범위:** 대상 산출물의 위 지정 절 외 부분은 이 시연 항목의 대조 대상이 아니므로 제외.

## §6. rework

- 없음 (final_verdict = Pass).
