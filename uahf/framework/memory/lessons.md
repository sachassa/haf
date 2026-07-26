# framework/memory/lessons — Lesson·Best Practice·재발 판정 특화 계약 인스턴스

작성일: 2026-07-05
상태: v0.7 Baseline (개정 — 05 INV-4 괄호 주해 어휘 정밀화(관찰 3 해소) · 사용자 승인 2026-07-06). 직전 기준선: v0.6 Baseline (개정 — §3.2 승격(Candidate→Active) 레코드의 Advisor 승인 기록 참조 content 자기완결 첨부 관례 명시 편입 · Advisor 승인 하 격리 개정 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/05-lessons.md §3 — 본 문서가 인스턴스화하는 정본(§3.1-A~D 연산 · §3.2-A~F 스키마 · §3.3 INV-1~9 · §9 결정 기록). 재정의 0.
- specs/04-memory.md §3.2-A·§3.1-C·§3.2-B·§3.4·§3.3 INV-5·§9 결정 기록 — Memory Item 표면·회수 정책·scope·특화 계약 탑승·kind/content 불투명·투영 및 소관 배정 근거.
- specs/02-agent.md §3.2-C·§3.2-D — 생성 연산의 입력 포맷 정본(입력으로만 소비, 재정의 0).
- framework/core/structure.md §2·§5·§7 — 소속 경계(`framework/memory/`)·금지 토큰 규칙(C-3 확장)·Core Contract 불변 C-1.
- ROADMAP.md v0.4 (Memory & Lessons) — 학습 사이클 완료 조건과 산출물.

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다. 본문은 AI·언어·툴체인 비의존을 유지한다(structure.md §5 C-3). 이 문서는 05 Core Contract의 인스턴스이며 05·04·02 계약을 재정의·확장하지 않는다(structure.md §7 C-1). 개정은 Advisor 승인 + **git 커밋 기록**(취지·범위를 커밋 메시지에)으로만 이뤄진다 — 기록 locus 정본 = `docs/spec-versioning-policy.md` §3.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(다른 절에서 반복하지 않는다).

- **정본은 specs/05-lessons.md §3이다.** 이 문서는 그 Lessons Core Contract(생성·승격·회수·효과 추적·Best Practice 대칭)의 **인스턴스**이며 스키마 필드·연산·불변 규칙을 재정의·확장하지 않는다(structure.md §7 C-1).
- 이 문서는 Lessons 특화 계약이 `framework/memory/` 경계에서 어떤 형태로 인스턴스화되는가를 규율한다. Lessons는 Layer가 아니라 Memory Service 위의 특화 계약이다(05 INV-2, 05 §2).
- **Module 구현 디렉터리 문서.** 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명)을 두지 않는다 — 규칙·분류 정본은 structure.md §5 C-3(및 05 INV-9, 04 INV-8)이다. 작성 시점의 동시 작성 형제 불인용(07 R2)·추측 0(07 R4) 준수 서술 = 종전 문면 git 앵커 90ca19c(정본 = uahf/specs/07-workflow.md §3.2-C). 저장 위치·직렬화·인덱스·매칭 알고리즘·라벨 키 물리 표기는 Adapter Binding 문서 소관이다(05 §4, 04 §4) — 특정 Adapter Binding 문서명을 명명하지 않는다(이식 불변 — 04 §4.2).
- **Memory 계약 표면과의 경계.** Memory Service Interface(단일 Port)·Memory Item·Memory Index의 상세 정본은 specs/04-memory.md §3이며 § 포인터로만 인용한다.
- 용어는 specs/00-glossary.md 정본만 사용한다(Lesson·Best Practice·회수 정책·Memory Service Interface = §3.2-C; 적용 조건·승격·재발 = §3.2-J). §5의 `kind` 값 3종은 05가 `kind` 값을 소유한다는 결정(04 §9·05 §9) 안의 값 명명이며 용어 신설이 아니다.

---

## §1. 목적·책임

Lessons 인스턴스의 책임은 세 가지다(05 §1) — 실패를 Lesson으로·성공을 Best Practice로 기록해 회수 가능하게 함 · "같은 실수의 반복"을 판정 가능한 계약으로 환원(ARCHITECTURE 3.5, 05 INV-7) · 세 기록이 Memory Item의 `kind`로 단일 Port 위에 올라타는 경계 확정(05 INV-1, 04 §3.4).

- **규율한다:** 스키마 인스턴스(§2), 생성·승격 규칙(§3), 재발 판정 3분류(§4), `kind` 값과 투영 규칙(§5).
- **규율하지 않는다:** Memory store 내부 구조·인덱스·직렬화·영속성(04·Adapter 소관), 적용 조건 매칭 알고리즘(Adapter 소관 — 05 §3.2-C·§4 SP-2), Learn·Memory Update 단계 전이(03 소관), 완료·실패 보고 포맷 자체(02 소관 — 입력으로만 소비), 역할 경계(02 §3.2-A).

---

## §2. 데이터 포맷 인스턴스

정본 = `uahf/specs/05-lessons.md §3.2-A~F`(재정의 0 · 필드 의미·필수/선택 표기의 문면은 정본 참조). 아래는 필드 인벤토리와 이 문서가 참조하는 값 집합만 둔다. 직렬화 형식은 Adapter/04 소관이다(05 §4 SP-1).

### §2.1 Lesson (교훈) — 8필드 (정본: 05 §3.2-A)

필드 = `id` · `status`(`Candidate` / `Active` / `Superseded` / `Retired`) · `failure` · `cause` · `lesson` · `applicability`(§2.3) · `provenance`(§2.4) — 이상 필수 · `supersedes` — 선택.

### §2.2 Best Practice (모범 사례) — 7필드 (정본: 05 §3.2-B)

필드 = `id` · `status` · `success` · `practice` · `applicability` · `provenance` — 이상 필수 · `supersedes` — 선택.

대칭 대응(05 §3.2-B): `Lesson.failure` ↔ `BestPractice.success`, `Lesson.cause`+`Lesson.lesson` ↔ `BestPractice.practice`. `id`·`status`·`applicability`·`provenance`는 두 스키마가 동일한 형태를 공유한다(05 INV-8).

### §2.3 Applicability Condition (적용 조건) (정본: 05 §3.2-C)

회수 매칭의 기준이 되는 추상 signature다 — 상황 유형(situation type)과 트리거 서술의 집합이며, 회수 시 현재 작업의 상황 서술자와 대조되어 관련성이 산출된다. 계약은 대조 요구만 두고 **대조 알고리즘은 규정하지 않는다**(Adapter 소관 — 05 §3.2-C·§4 SP-2). `labels`·`kind`로의 투영 규칙은 §5가 정의한다.

### §2.4 Provenance (출처) — 4필드 (정본: 05 §3.2-D)

필드 = `task_ref` · `report_ref` · `origin_role`(후보를 제출한 역할과 승격을 승인한 역할) · `ordering_ref`(재발 판정의 "기존 Lesson이 착수 전에 존재했는가" 판정 기준 — 구체 시간 포맷은 Adapter/04 소관). 출처 없는 Lesson·Best Practice는 성립하지 않는다(05 INV-5).

### §2.5 Recurrence Judgment (재발 판정 레코드) — 5필드 (정본: 05 §3.2-E)

효과 추적 연산(§4)의 산출물이다. 필드 = `failure_signature` · `matched_lesson_id`(매칭된 기존 Active Lesson의 안정 `id`, 있으면) · `was_recalled`(그 Lesson이 해당 작업의 회수 집합에 포함되었는가) · `verdict`(`Novel` / `RecallGap` / `Recurrence` — §4) · `follow_up`.

### §2.6 Failure Report (Lessons 연산 공통) — 4필드 (정본: 05 §3.2-F)

필드 = `operation` · `reason` · `target` · `location`. 02 §3.2-D 실패 보고(Agent 보고)와 소속이 다르며 혼입하지 않는다.

- `operation` 값 = RegisterCandidate / Promote / Recall / JudgeRecurrence / RegisterBestPractice.
- `reason` 값 = InvalidSource / MissingProvenance / PromotionCriteriaUnmet / NotApproved / PortReadFailed / PortWriteFailed / ScopeExceeded / SignatureUnmatchable.

---

## §3. 생성·승격 규칙 (정본: 05 §3.1-A·§3.1-D, §3.2-A 승격 규칙)

모든 저장·회수는 Memory Service Interface(단일 Port)를 경유한다(05 INV-1, §6). 단계 전이 시점(언제 호출되는가)은 03 소관이다.

### §3.1 Register Candidate (후보 등록) — 입력: 02 §3.2-D 실패 보고

- **입력.** 02 §3.2-D 실패 보고 1건(`reason`·`repro`·`attempted`·`lesson_candidate`·`blocking` + 출처 작업 참조) — 입력으로 소비할 뿐 재정의하지 않는다.
- **`lesson_candidate.여부 = 예`인 실패:** 정확히 하나의 Lesson Candidate(status=`Candidate`)로 **즉시 등록**되고 provenance(§2.4)가 채워지며 Port를 통해 기록된다(05 §3.1-A 완료 조건).
- **`lesson_candidate.여부 = 아니오`인 실패:** 자동 등록되지는 않으나 **후보 자격은 유지된다** — 승격 심사에서 재평가 대상이다(05 INV-3 보편 후보 자격, AGENT.md "모든 실패는 Lesson 후보").
- **실패 보고(§2.6):** reason = `InvalidSource` / `MissingProvenance` / `PortWriteFailed`.

### §3.2 Promote (승격 — Candidate → Active): 3조건 + Advisor 전속 권한

**승격 3조건 (05 §3.2-A 승격 규칙).** 다음을 **모두** 만족해야 Candidate가 Active로 승격된다.

1. `failure`·`cause`·`lesson`·`applicability`·`provenance`가 모두 채워져 있다 (검증 가능성, 05 INV-5).
2. Verifier의 Learn 입력(독립 판정)이 실패의 실재를 뒷받침한다 (02 §3.1 Verify 단계 산출물).
3. Advisor가 승격을 승인한다.

**승격 권한 = Advisor 전속 (05 INV-4).** 승격(`Candidate → Active`)은 Advisor 승인으로만 성립한다. Worker는 후보를 제출하고, Verifier는 Learn 입력(근거)을 제공하며, **승격 결정 권한은 Advisor에 있다**(역할 경계 02 §3.2-A). Worker의 자기 점검은 최종 승인이 아니다.

- **출력.** 정식 Lesson(status=`Active`) — 안정적 `id`와 매칭 가능한 `applicability`(§2.3)를 갖는다.
- **Advisor 승인 없는 승격은 거부된다:** reason = `NotApproved`. 그 밖의 승격 실패 reason = `PromotionCriteriaUnmet` / `PortWriteFailed`.
- **승인 기록 참조의 content 자기완결 첨부 (승격 레코드 관례).** 승격으로 기록되는 Active 레코드는 그 승격을 성립시킨 **Advisor 승인 기록의 참조**를 자신의 **`content` 페이로드 안에 자기완결적으로 첨부한다** — 05 INV-4 충족을 외부 기록 경유 없이 레코드 자체로 확인·검증할 수 있게 한다. 세 항목의 정본 귀속은 서로 다르다: (a) INV-4 정본 문면 = "승격(`Candidate → Active`)은 Advisor 승인으로만 성립한다"(05 §3.3), (b) 승인 없는 승격의 거부 코드 `NotApproved` = 05 §6 실패 모드(§2.6 reason 코드) 소속, (c) "승인 기록 참조"의 `content` 첨부 = 본 절이 도입한 **관례**로 provenance(§2.4 `origin_role`)를 보강하는 content 담김이며 **새 필수 필드의 신설이 아니다**(05 §3.2-A 필수 필드 전건 보존 — §6). 승인 참조를 담는 라벨 키·물리 표기·직렬화 형태는 규정하지 않으며 Adapter Binding 문서 소관이다.
- **Best Practice 대칭.** 위 승격 3조건·전속 권한·승인 기록 참조 관례는 Best Practice 승격에도 대칭 적용된다(§3.3).

### §3.3 Best Practice 대칭 (정본: 05 §3.1-D, INV-8) — 입력: 02 §3.2-C 완료 보고

- **입력.** 02 §3.2-C 완료 보고 1건(`artifacts`·`self_check`·`verify_basis` + 출처 작업 참조) — 재정의하지 않는다.
- **Verify 통과 전제.** 완료 보고는 Verify 통과 후에만 생성되므로(02 INV-4) Best Practice 후보는 Verify를 통과한 완료 보고에서만 도출되며, 후보 자격은 그 전체에 보편적으로 성립한다.
- **승격.** Candidate → Active 승격은 Lesson과 **동일한 권한·절차**를 따른다(05 INV-4·INV-9) — Advisor 전속 승인, provenance 필수, 승인 기록 참조의 content 자기완결 첨부 관례(§3.2)도 대칭 적용된다. 실패 보고 코드 집합은 §2.6과 동일하다.
- 02 §3.2-C에는 `lesson_candidate`와 대칭인 명시 필드가 없다. 추가 여부는 02의 결정 사항이며(05 §9·04 §9 결정 기록) 본 문서는 02를 수정·추측하지 않는다.

---

## §4. 재발 판정 (정본: 05 §3.1-C — Judge Recurrence)

효과 추적 연산은 새 실패를 세 결과 중 정확히 하나로 분류해 ARCHITECTURE 3.5 "같은 실수를 반복하지 않는다"를 검증 가능한 판정으로 환원한다(05 INV-7).

- **입력.** 새 실패의 signature + 그 작업에서 회수된 Lesson 집합(회수 이력) + `applicability`가 매칭되는 기존 Active Lesson(Port 조회).
- **회수 이력의 소속 경계.** "작업별 회수 집합"의 저장·기록 주체는 **03 루프 상태 기록 소관**이며 이 연산은 회수 이력을 **입력으로 받는다**(05 §9·04 §9 결정 기록). 본 문서는 회수 이력을 생성·저장하지 않는다.
- **출력.** 판정 결과 + 재발 판정 레코드(§2.5). Port를 통해 기록된다.

**3분류와 후속 조치 (05 §3.1-C):**

| 판정 | 조건 | 후속 조치 (`follow_up`, §2.5) |
|---|---|---|
| `Novel` | 매칭되는 기존 Active Lesson이 없다. | 신규 후보 등록 대상 → Register Candidate(§3.1). (실패 아님.) |
| `RecallGap` | 매칭되는 Lesson이 **존재했으나** 그 작업의 회수 집합에 **없었다**. | **회수 규칙/적용 조건의 결함**이며 Lesson 내용 결함이 아니다 → `applicability`(§2.3) 또는 회수 규칙을 조정한다. |
| `Recurrence` | 매칭되는 Lesson이 존재하고 **회수되었음에도** 같은 실패가 발생했다. | **"같은 실수 반복"**이며 Lesson 효과 미달이다 → Lesson을 강화하거나 supersede하는 새 Lesson(§2.1 `supersedes`)을 만든다. |

- **실패 보고(§2.6):** reason = `SignatureUnmatchable` / `PortReadFailed` / `PortWriteFailed`.

---

## §5. Memory Item `kind` 값 확정과 applicability 투영 (정본 정합: 04 §9, 05 §3.2-C·§9)

Lesson·Best Practice·재발 판정 레코드는 별도 저장 경로를 갖지 않는다. 셋 모두 **Memory Item의 `kind`로 단일 Port 위에 올라탄다**(04 §3.4·§8 예3). Memory는 `kind`·`content`를 불투명하게 다루며(04 INV-5) `kind` 값·`content` 상세 스키마는 05(이 인스턴스)가 소유한다(04 §9·05 §9 결정 기록).

### §5.1 `kind` 값 3종 (AI·언어 비의존 확정)

| 특화 기록 (스키마) | 확정 `kind` 값 | `content` 상세 스키마 소유 |
|---|---|---|
| Lesson (§2.1) | `lesson` | 본 문서 §2.1 (05 §3.2-A 정본) |
| Best Practice (§2.2) | `best-practice` | 본 문서 §2.2 (05 §3.2-B 정본) |
| 재발 판정 레코드 (§2.5) | `recurrence-judgment` | 본 문서 §2.5 (05 §3.2-E 정본) |

- 세 값은 서로 구별되는 안정 분류자이며 Memory는 이를 불투명 분류자로만 취급한다(04 INV-5). **구체 직렬화 표기**(구분자·대소문자·물리 인코딩)는 Adapter 직렬화 소관이다(05 §4 SP-1, 04 §4).
- `content`에는 각 스키마(§2)의 필드가 담기고 그 상세는 05가 소유한다. 단, 회수·상태 해소·재발 판정 조회를 위해 `content`의 일부 필드(Lesson·BP의 안정 `id`·`status`, 재발 판정 레코드의 `verdict`·`matched_lesson_id`)는 `labels`로도 투영된다(§5.2) — index 단계 후보 축소용 태그 부여이며 Memory가 `content`를 해석하는 것이 아니다.

### §5.2 Memory Item `labels`·`kind` 투영 규칙 (applicability·안정 `id`·`status`·재발 판정 `verdict`·`matched_lesson_id` — 04 §9 결정 기록 정합)

회수(05 §3.1-B)는 Memory Item의 `labels`·`kind`로 후보 범위를 index 단계에서 좁힌 뒤 Port 위에서 관련성을 산출한다.

- **기록 종류 투영 → `kind`.** Lesson인지 Best Practice인지는 §5.1의 `kind` 값으로 구분되고, Recall scope의 `kind` 차원(04 §3.2-B)이 이를 해소한다.
- **적용 조건 투영 → `labels`.** applicability(§2.3)의 상황 유형·트리거 서술을 `labels`로 투영한다. Recall scope의 `labels` 차원이 후보를 좁힌다("applicability는 `labels`·`kind`로 투영 가능" — 04 §9 결정 기록 정합).
- **안정 식별 투영 → `labels`.** Lesson·BP의 **안정 `id`**(§2.1/§2.2)를 `labels`로 투영한다. 재발 판정(§4)·supersede·최신 상태 해소의 index 단계 후보 축소에 쓰인다. 이 안정 `id`는 Record가 매 기록에 유일 할당하는 Memory Item `id`(04 §3.2-A)와 구별되며, 여러 Memory Item이 같은 안정 `id`를 `labels`로 공유할 수 있다.
- **상태 투영 → `labels`.** `status`(`Candidate`/`Active`/`Superseded`/`Retired`)를 `labels`로 투영해, 05 §3.1-B 회수 출력(Active 최소 집합)을 index 단계에서 필터할 수 있게 한다. `labels`는 Index Entry(04 §3.2-C)에도 실리므로 `content` 원문 로드(`detail = full`) 없이 `Active`만 걸러진다(04 INV-4·05 INV-6 정합).
- **최신 상태 해소 규칙.** 기록은 불변이므로(04 INV-6) `status` 전이는 기존 Item을 변경하지 않고 **새 Memory Item 기록으로 표현된다**. 따라서 같은 안정 `id`로 투영된 Item 중 **`timestamp` 최신 항목**이 현재 상태를 나타내며, 회수(05 §3.1-B)와 재발 판정의 Active Lesson 조회는 이 최신 항목을 기준으로 한다.
- **재발 판정 레코드 투영 → `labels`.** 재발 판정 레코드(§2.5)의 `verdict`·`matched_lesson_id`를 `labels`로 투영해, `kind=recurrence-judgment` 레코드를 `content` 원문 로드 없이 index 단계에서 조회·축소할 수 있게 한다(04 INV-4·05 INV-6 정합). 두 필드의 의미 정본은 §2.5(05 §3.2-E)이며 본 규칙은 **무엇에 투영하는가**만 확정한다.
- **Port의 역할 = 범위 조회만.** Port는 `kind`/`labels`/`timeRange`/`source` 범위 조회만 제공하며 이를 위해 04 계약을 변경하지 않는다. 회수 정책(필요할 때만·목적 명시·최소 범위)은 Port가 강제하고 전량 로드는 금지된다(04 INV-2/3/4, 05 INV-6).
- **최종 대조는 Port 위에서.** 상황 서술자 ↔ `applicability` 최종 대조는 Port가 좁힌 후보 위에서 수행된다. **매칭 계약 표면은 05 소유, 매칭 구현(대조 알고리즘)은 Adapter 소관**이다(05 §3.2-C·§4 SP-2, 04 §9 결정 기록).
- **매칭 알고리즘·라벨 물리 표기는 정의하지 않는다.** 대조 알고리즘(키워드·의미 검색·임베딩 등)과 위 투영 **전부**의 **라벨 키 물리 표기**(이름·직렬화 형태)는 Adapter 소관이며(05 §4 SP-1, 04 §4; 물리 표기 정본은 Adapter Binding 문서 소관) 본 문서는 "무엇을 `labels`에 투영하는가"만 확정한다.

**근거 (Advisor 결정 — v0.4 OQ-M5-1 해소 · v0.5 `uahf/docs/v0.4-verification-report.md@cd9247b` §3.4 관찰 1 해소).** 안정 `id`·`status` 투영과 최신 상태 해소 규칙은 05 §3.1-B 회수 출력(Active 최소 집합)의 index 단계 해소를 위해 추가되었다 — 전량 로드로만 `Active`를 거르면 최소 Context 원칙(05 INV-6, 04 INV-4)과 상충한다. 재발 판정 레코드의 `verdict`·`matched_lesson_id` 투영 2건은 v0.4부터 운용되어 왔으나 "무엇을 투영하는가는 05가 소유한다"는 원칙상 본 절에 명시되어야 하므로 v0.5에서 명시 편입했다. `labels`는 04 §3.2-A의 **자유 태그 집합**이므로 두 보강 모두 `labels` 사용 방식의 확정일 뿐 **04·05 계약 변경이 아니다**(structure.md §7 C-1 계약 재정의 0 유지). 라벨 키 물리 표기는 Adapter Binding 문서가 소유하며 본 개정은 이를 재서술하지 않는다.

---

## §6. 단일 Port·경계·계약 재정의 0 (정본: 05 INV-1)

- **단일 Port (05 INV-1).** 모든 Lesson·Best Practice·재발 판정 레코드의 저장(§3·§4)과 회수(05 §3.1-B Recall, §4 매칭 조회)는 Memory Service Interface(단일 Port)를 경유한다. 영속성 백엔드 직접 접근은 위반이다(04 INV-1).
- **쓰기 시점·조건.** 기록은 Memory Update 단계에서 일어나며(단계 전이는 03 소관) 모든 기록은 provenance(§2.4)를 포함한다(05 §5, INV-5).
- **읽기 시점·범위.** 회수는 Consult 단계에서 회수 정책에 따라 **최소 범위**로 일어난다. 적용 조건이 매칭되는 최소 집합만 읽고 전량 로드하지 않는다(05 INV-6, 04 INV-3/INV-4).
- **계약 재정의 0.** §2 스키마는 05 §3.2의 인용이고, Memory Item·Port·Index 참조는 04 § 포인터, 완료·실패 보고 입력은 02 § 포인터로만 연결한다(structure.md §7 C-1). 필드 소속을 § 포인터로 명시해 다른 계약의 필드와 혼입되지 않게 한다. §3.2 승격 레코드의 승인 기록 참조 첨부는 **content 담김 관례**일 뿐 새 필수 필드가 아니며 05 §3.2-A 필수 필드는 전건 보존된다 — INV-4 정본 문면, 거부 코드 `NotApproved`(05 §6 실패 모드), 이 관례(§3.2)는 서로 소속이 다른 별개 항목이다.
- 그 밖의 경계(금지 토큰 규칙과 비대상 분류·07 R2 형제 불인용·Glossary 정본·Adapter 소관 물리 표기)는 §0이 소유한다 — 금지 토큰 규칙 정본은 structure.md §5 C-3, 07 R2·R4 정본은 uahf/specs/07-workflow.md §3.2-C, 용어 정본은 uahf/specs/00-glossary.md다.
