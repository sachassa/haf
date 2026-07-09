# [시연 산출물 — 실계약 문서 아님] verify-d — 검증 리포트 인스턴스 (시연 ⓓ Conditional 분기 / 시연 ⓔ Conditional rework)

> **시연 산출물 — 실계약 문서 아님.** v0.5 Verifier 시연(Task V8) 수행 중 Verify 연산으로 산출한 검증 리포트 인스턴스다. CP2 리포트가 아니다. verifier-binding.md §4.1 6필드 절 구조로 직렬화한다. `docs/v0.5-demo-fixtures/` 내부에 둔다.

정본: 06 §3.2-C(도출 규칙 — 조건부)·§3.2-D(rework)·§8 예2, verification-report.md §4, rework-instruction.md §2/§3.

이 리포트는 최종 판정 결정성 3집합(시연 ⓓ)의 **Conditional 집합(집합 3 — 위반 0·판정 불가 ≥1)** 인스턴스다. Pass 집합(집합 1)은 verify-b(final_verdict=Pass), Fail 집합(집합 2)은 verify-a(final_verdict=Fail)가 실증하며, 이 세 리포트가 06 §3.2-C 3분기(통과/실패/조건부)의 결정적 도출을 보인다.

---

## §1. target

- 산출물: 시연 판정 집합(합성) — Conditional 분기 실증용 항목별 판정 집합 (V7 §12-B 합성 집합 허용).
- 대상 작업 식별자: v0.5 시연 ⓓ(집합 3 Conditional) / ⓔ(Conditional rework 4필드).

## §2. criteria_basis

- 부류: **규격 + 위임 완료 조건** (도출 규칙 06 §3.2-C 대조 + 해소 여부 대조; criteria-catalog §4).
- 기준: "위반(Violated)이 0이고 판정 불가(Undetermined)가 1건 이상인 항목별 판정 집합에서, 06 §3.2-C 도출 규칙이 final_verdict = Conditional을 결정적으로 도출한다."

## §3. items (항목별 판정 — 06 §3.2-B 5필드; 위반 0·판정 불가 1)

| # | `criterion` | `verdict` | `evidence` | `scope` | `verification_type` |
|---|---|---|---|---|---|
| 1 | 검증 리포트 스키마 6필드가 대상 산출물에 존재(규격) | 충족(Met) | verification-report.md §2 표 6행 존재 | verification-report.md §2 | VT-3 |
| 2 | 어떤 Open Question(예: 형태 B 실행 코드 경계 분할 — verifier-binding §3.1 OQ-VB-2)이 현 산출물에서 **해소**되었는가 | **판정 불가(Undetermined)** | 현 산출물에 형태 B 설계가 **부재**(Bootstrap 형태 A) — 해소 여부를 확정할 근거가 없음. 근거 부족으로 충족/위반 확정 불가 (06 §8 예2 유형). 충족으로 취급하지 않음(06 V6). | 현 산출물 범위(형태 B 미도입 구간) | VT-2 |

## §4. final_verdict

- **Conditional (조건부).** 위반(Violated) 0건, 판정 불가(Undetermined) 1건(item #2)이므로 06 §3.2-C 도출 규칙("위반 없고 판정 불가 존재 → 조건부")으로 결정적으로 도출한다. **조건부는 완료가 아니다** — 판정 불가 항목의 해소로 통과 전이하거나, 완료를 막지 않는다는 **Advisor 최종 판정(재량)** 을 받아야 한다. 재량 판정은 Verifier가 하지 않는다 (06 §3.2-C, 02 §3.2-A, verifier-protocol §2.5).

## §5. verifier_scope

- **검사한 범위:** item #1(스키마 6필드 존재) + item #2(형태 B 해소 여부 — 현 산출물 범위).
- **검사하지 못했거나 제외한 범위:** 형태 B 실행 코드(미도입)는 물리적으로 부재하여 검사 불능 — 이 부재가 item #2의 판정 불가 근거다. 제외가 아니라 근거 부족을 정직하게 판정 불가로 표기한다(06 V4/V6).

## §6. rework (재작업 지시 — 06 §3.2-D 4필드; Conditional이므로 필수)

| 필드 (06 §3.2-D) | 값 |
|---|---|
| `violated_items` | item #2 — {criterion: "형태 B 경계 분할 Open Question의 해소 여부", verdict: 판정 불가(Undetermined)}. (Conditional에서는 판정 불가 항목이 담긴다 — rework-instruction §3.) |
| `expected_state` | item #2가 **해소**됨 — 형태 B 설계가 확정되어 충족/위반이 근거로 확정되거나, 이 항목이 완료를 막지 않는다는 Advisor 최종 판정을 받는다. |
| `revalidation_criteria` | 근거(형태 B 설계) 확보 후 재판정 시 item #2가 충족/위반으로 확정되고, 도출 규칙이 Pass 또는 Fail로 재도출된다. |
| `evidence_gap` | **유내용** — 형태 B 실행 코드·설계가 현 산출물에 부재하여 item #2의 해소 여부를 확정할 근거가 없음(근거 부족·검사 범위 한계). 이는 은폐 없이 명시된다(06 V6·§3.2-D "판정 불가 항목에 한함"). |

## §7. 경계

- 이 리포트는 시연 산출물이며, Conditional의 최종 처리(해소 대기 / Advisor 재량 판정)는 게이트(CP3 Advisor) 소관이다. Verifier·시연 산출은 스스로 통과 처리하지 않는다 (06 §8 예2, 02 §3.2-A).
