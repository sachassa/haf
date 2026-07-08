# [시연 산출물 — 실계약 문서 아님] verify-a — 검증 리포트 인스턴스 (시연 ⓐ 거짓 완료 보고 검출 / 시연 ⓕ 독립성)

> **시연 산출물 — 실계약 문서 아님.** 이 파일은 v0.5 Verifier 시연(Task V8) 수행 중 **Verify 연산을 픽스처에 적용해 산출한 검증 리포트 인스턴스**다. CP2 독립 판정 리포트(`docs/v0.5-verification-report.md`, 별도 Task)가 **아니다**. verifier-binding.md §4.1 6필드 절 구조(§1 target ~ §6 rework)로 직렬화한다. `docs/v0.5-demo-fixtures/` 내부에 둔다.

정본: 06 §3.2-A(6필드)·§3.2-B(항목별 판정 5필드·판정 값)·§3.2-C(도출 규칙)·§3.2-D(rework)·§3.2-E(VT)·§3.2-F(거짓 완료 보고 검출). 스키마 확정 인터페이스: framework/verifier/verification-report.md §2/§3/§4.

---

## §1. target

- 산출물: `docs/v0.5-demo-fixtures/fixture-target.md` ("Core류 문서 역할" 구성물 픽스처).
- 대상 작업 식별자: v0.5 시연 ⓐ(거짓 완료 보고 검출) / ⓕ(독립성) — 픽스처 판정.
- 참고 입력(claim, 판정 근거 아님 — 06 V1): `docs/v0.5-demo-fixtures/fixture-claim.md`.

## §2. criteria_basis

- 부류: **경계 규칙** (criteria-catalog §4 경계 규칙 부류; 06 §3.2-A `criteria_basis`).
- 기준: "대상 파일 (a)의 해당 경계('Core류 문서 역할' 본문)에 금지 요소 후보 부류 전체(① 특정 AI 이름·모델명·제품 기능명 / ② 언어·툴체인 / ③ 직렬화 형식·확장자·OS / ④ 물리 경로·인스턴스)가 **0건**이어야 한다."
- 기준이 명시되므로 판정을 진행한다 (06 V2, verifier-protocol §2.3).

## §3. items (항목별 판정 — 06 §3.2-B 5필드)

| # | `criterion` | `verdict` | `evidence` | `scope` | `verification_type` |
|---|---|---|---|---|---|
| 1 | 대상 파일 본문에 부류 ① 토큰(특정 AI 이름·모델명·제품 기능명)이 0건이다 | **위반(Violated)** | 전수 스캔에서 대상 파일 **§2 본문**에 부류 ① 토큰(특정 모델명 표기) **1건 잔존** 검출. 이 토큰은 claim(b)이 단일 검색한 어시스턴트 이름 토큰과 **다른 형태**(모델명)이며, claim의 단일 토큰 검색이 놓친 지점이다. 매치 분류: §1·§2·§3의 "부류 ①(…)"·"특정 모델명" 등 **부류 서술**은 mention(정당 참조), §2의 실제 모델명 토큰 1건만 use(위반)로 계상(L-04 mention/use 경계). | fixture-target.md **본문 전문**(§1·§2·§3) + 금지 요소 후보 부류 **전체**(①~④). 단일 토큰 검색보다 넓음. | **VT-4** (경계 검증 전수 스캔) |

## §4. final_verdict

- **Fail (실패).** 위반(Violated) 항목이 1건(item #1) 이상이므로 06 §3.2-C 도출 규칙("하나라도 위반 → 실패")으로 결정적으로 도출한다 (verification-report §4, verifier-protocol §2.5).

## §5. verifier_scope

- **검사한 범위:** fixture-target.md 본문 전문(§1·§2·§3 전체) + 금지 요소 후보 부류 전체(①~④)에 대한 VT-4 전수 스캔.
- **검사하지 못했거나 제외한 범위:** `docs/v0.5-demo-fixtures/` **밖의 실계약 경계**(06·framework/verifier/ 5문서 등)는 이 시연의 판정 대상이 **아니다** — 제외. 픽스처 디렉터리는 06 §7-⑧ Core AI 비의존 전수 스캔의 대상 경계에서 제외되는 정당 보유 지점이다(V7 §4.2). 대상 파일 머리의 disclaimer는 픽스처임을 표시하는 메타 서술로, 부류 서술(mention)만 담아 위반으로 계상하지 않았다.

## §6. rework (재작업 지시 — 06 §3.2-D 4필드; Fail이므로 필수)

| 필드 (06 §3.2-D) | 값 |
|---|---|
| `violated_items` | item #1 — {criterion: "대상 파일 본문에 부류 ① 토큰 0건", verdict: 위반(Violated)}. |
| `expected_state` | 대상 경계('Core류 문서 역할' 본문)에 금지 요소 후보 부류 전부(①~④) **0건**. §2의 모델명 토큰을 부류 비의존 일반 서술로 교체(또는 Adapter 격리 절로 이동). |
| `revalidation_criteria` | 전수 스캔 재실행 후 후보 부류 전체에 대해 잔존 토큰 **0건** — **라이브 본문** 기준(rework-instruction §4). 픽스처 머리 disclaimer의 부류 서술(mention)은 제외. |
| `evidence_gap` | 없음 (판정 불가(Undetermined) 항목 0건). |

## §7. 거짓 완료 보고 판정 (06 §3.2-F — 시연 ⓐ·ⓕ 핵심)

- claim(b) `self_check` = "AI 의존 0건 — **충족**" 주장 ↔ 독립 판정 `verdict` = **위반(Violated)** 의 **모순**. 완료 보고 주장을 신뢰하지 않고 산출물 자체를 전수 재판정한 결과 위반이 검출되었으므로, 이는 **거짓 완료 보고**로 판정된다 (06 §3.2-F, verifier-protocol §5).
- **독립성(시연 ⓕ, 06 INV-1):** 위 §3~§4의 `verdict`·`final_verdict`는 오직 산출물(fixture-target.md §2) 실측(`evidence`)에서만 도출되었고, claim의 `self_check` "충족" 주장은 판정을 바꾸지 못했다. 완료 보고 주장은 참고 입력(claim)일 뿐 판정 근거가 아니다.
- **경계:** 이 리포트는 시연 산출물이며, 재작업 여부·최종 승인은 게이트(CP2 Verifier·CP3 Advisor) 소관이다 — 자기 점검·시연 산출이 최종 승인이 아니다 (02 §3.2-A, V7 §7).
