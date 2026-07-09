# [시연 산출물 — 실계약 문서 아님] verify-b — 검증 리포트 인스턴스 (시연 ⓑ 스키마 완전성 + 결정적 생성)

> **시연 산출물 — 실계약 문서 아님.** v0.5 Verifier 시연(Task V8) 수행 중 Verify 연산으로 산출한 검증 리포트 인스턴스다. CP2 리포트가 아니다. verifier-binding.md §4.1 6필드 절 구조로 직렬화한다. 이 리포트는 재량·timestamp·순서 값 등 **입력 외 값이 0**이므로, 동일 입력{산출물+criteria}에 대해 문면이 결정적으로 동일하다 (DP-V3, 06 INV-5). 동일 입력 2회 수행의 두 산출(verify-b-run1 / verify-b-run2)은 이 성질에 따라 문면 동일해야 한다.

정본: 06 §3.2-A/B/C, verification-report.md §2/§3/§4, verifier-protocol.md §4(DP-V3).

---

## §1. target

- 산출물: `framework/verifier/verification-report.md` (V1 확정본 — 검증 리포트 스키마 인스턴스).
- 대상 작업 식별자: v0.5 시연 ⓑ — 검증 리포트 스키마 완전성 + 결정적 생성.

## §2. criteria_basis

- 부류: **규격** (criteria-catalog §4 규격 부류; 06 §3.2-A `criteria_basis`).
- 기준: "산출물이 06 §3.2-A 검증 리포트 6필드 스키마와 §3.2-B 항목별 판정 5필드 스키마를 각각 표로 인스턴스화하여 셀 단위로 보존한다."

## §3. items (항목별 판정 — 06 §3.2-B 5필드)

| # | `criterion` | `verdict` | `evidence` | `scope` | `verification_type` |
|---|---|---|---|---|---|
| 1 | 산출물이 실재하고 접근 가능하다 | 충족(Met) | 파일 조회로 전문 판독 성공 — verification-report.md 실재·접근 확인 | 산출물 파일 실재 | VT-1 |
| 2 | §2에 검증 리포트 6필드(target/criteria_basis/items/final_verdict/verifier_scope/rework) 표가 전건 존재하고 필수/조건부 표기를 보존한다 | 충족(Met) | verification-report.md §2 표 — 6행(target·criteria_basis·items·final_verdict·verifier_scope 필수, rework 조건부) | verification-report.md §2 | VT-3 |
| 3 | §3에 항목별 판정 5필드(criterion/verdict/evidence/scope/verification_type) 표와 판정 값 3종(충족/위반/판정 불가)이 전건 존재한다 | 충족(Met) | verification-report.md §3 표 — 5행 + 판정 값 3종 정의 | verification-report.md §3 | VT-3 |

## §4. final_verdict

- **Pass (통과).** 모든 항목(#1~#3)이 충족(Met)이므로 06 §3.2-C 도출 규칙("모든 항목 충족 → 통과")으로 결정적으로 도출한다.

## §5. verifier_scope

- **검사한 범위:** verification-report.md §2(6필드 표)·§3(5필드 표) + 파일 실재.
- **검사하지 못했거나 제외한 범위:** verification-report.md §4·§6 등 그 외 절, 및 다른 framework/verifier/ 문서 — 이 시연 항목의 대조 대상이 아니므로 제외.

## §6. rework

- 없음 (final_verdict = Pass — 06 §3.2-A 조건부 표기, §3.2-C).
