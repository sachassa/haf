# framework/memory/lessons — Lesson·Best Practice·재발 판정 특화 계약 인스턴스

작성일: 2026-07-05
상태: v0.7 Baseline (개정 — 05 INV-4 괄호 주해 어휘 정밀화(관찰 3 해소) · 사용자 승인 2026-07-06). 직전 기준선: v0.6 Baseline (개정 — §3.2 승격(Candidate→Active) 레코드의 Advisor 승인 기록 참조 content 자기완결 첨부 관례 명시 편입 · Advisor 승인 하 격리 개정 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/05-lessons.md §3 (Core Contract) — 본 문서가 인스턴스화하는 정본. §3.1-A/B/C/D (Register Candidate·Promote·Recall·Judge Recurrence·Best Practice 대칭 연산), §3.2-A~F (Lesson·Best Practice·Applicability·Provenance·재발 판정 레코드·Failure Report 스키마), §3.3 INV-1~9, §9 결정 기록. 스키마 필드·연산·불변 규칙의 정본은 05가 유지하며 본 문서는 재정의하지 않는다.
- specs/04-memory.md §3.2-A (Memory Item — `kind`·`labels` 표면), §3.1-C (회수 정책), §3.2-B (Recall Request scope), §3.4 (특화 계약은 kind로 Port 위에 올라탐), §3.3 INV-5 (kind·content 불투명), §9 결정 기록 ("applicability는 labels·kind로 투영 가능", "매칭의 계약 표면은 05 소유·구현은 Adapter 소관", "회수 이력은 03 루프 상태 기록 소관, 05는 입력으로 받는다"). Port·Memory Item·Memory Index의 상세 정본은 04가 유지하며 본 문서는 § 포인터로만 참조한다.
- specs/02-agent.md §3.2-C (완료 보고 5필드)·§3.2-D (실패 보고 5필드) — 생성 연산의 입력 포맷 정본. 본 문서는 입력으로 소비할 뿐 재정의하지 않는다.
- framework/core/structure.md §2 (Module 구현 디렉터리 경계 — `framework/{loop,memory,verifier,workflow,plugins}/`), §5 (금지 토큰 규칙 C-3 확장 — Module 구현 디렉터리 문서 본문 비의존), §7 (Core Contract 불변 조건 C-1). 본 파일은 `framework/memory/` 경계의 첫 실사용 인스턴스다 (structure.md §2 주).
- ROADMAP.md v0.4 (Memory & Lessons) — 학습 사이클 완료 조건과 산출물.

거버넌스: 이 문서는 `framework/memory/` 소속 Module 구현 디렉터리 문서다. 문서 본문은 AI·언어·툴체인 비의존을 유지한다 (structure.md §5 C-3 확장). 이 문서는 05 Core Contract의 인스턴스이며 05·04·02 계약을 재정의·확장하지 않는다 (structure.md §7 C-1). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. 05 §3.2-A~F 6개 스키마의 인스턴스 절(필수/선택 표기 정본 보존), 생성·승격 규칙(Register Candidate 입력=02 §3.2-D, 승격 3조건·Advisor 전속 권한, Best Practice 대칭=02 §3.2-C), 재발 판정 3분류·회수 이력 03 소관 입력 명시, Memory Item kind 값 3종 확정·applicability의 labels·kind 투영 규칙(04 §9 정합, 매칭 알고리즘 미정의), 단일 Port·계약 재정의 0·금지 토큰 0 대조. 05·04·02 계약 재정의 0, 동시 작성 Memory 계약 문서 인용 0. | Worker (Advisor 위임, Task M4) |
| 2026-07-05 | v0.4 Draft (r2) | OQ-M5-1 해소 (Advisor 개정 지시). §5.2에 투영 규칙 2건(안정 `id` 투영·`status` 투영)과 최신 상태 해소 규칙 1건 추가 — 05 §3.1-B 회수 출력(Active 최소 집합)의 index 단계 해소용(04 INV-4/INV-6 정합, 전량 로드 없이 Active 필터). §5.2 헤딩·§5.1 content 필드 투영 주석·§7 요약(투영·회수 서술, 요약 bullet) 정합 전수 갱신. `labels` 자유 태그 사용 방식 확정 — 04·05 계약 재정의 0 유지. 라벨 물리 표기는 Adapter 소관 포인터 유지. 금지 토큰 0 재확인. | Worker (Advisor 개정 지시, Task M4 r2) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.5 Draft (개정) | v0.5 Task V12 (r3) — Advisor 승인 하 격리 개정 (사용자 승인 v0.5 계획 — handoff §1.6 이월 후보 1 해소). §5.2에 재발 판정 레코드 투영 2건 명시 편입: `verdict` → `labels`, `matched_lesson_id` → `labels` (무엇을 투영하는가만 — 필드 의미 정본은 §2.5/05 §3.2-E 포인터 유지, 라벨 키 물리 표기는 Adapter Binding 문서 소관 유지). `labels`는 04 §3.2-A 자유 태그 집합이므로 계약 변경 아님(v0.4 결정 승계, 05 계약 재정의 0). 같은 상태 서술 전 지점 전수 갱신(L-06): §5.2 헤딩·§5.1 note·신규 투영 bullet·물리 표기 규칙 bullet·§5.2 근거·§6 스캔 주해·§7 요약·다이어그램. 금지 토큰 0(C-3 확장) 개정분 포함 재확인, Glossary 밖 용어 신설 0. 근거: docs/v0.4-verification-report §3.4 관찰 1 해소. | Worker (Advisor 위임, Task V12 r3) |
| 2026-07-06 | v0.5 Draft (개정) | v0.5 Task V12 (r4) — 일반형 Adapter 포인터 관행 정합 (Advisor 위임문 문안 교정). r3이 §5.2 물리 표기 규칙 bullet·v0.5 근거 절에 넣었던 특정 Adapter Binding 문서명·절 번호 참조를 제거하고 일반형 "Adapter Binding 문서 소관" 포인터로 교정. 사유: Module 구현 디렉터리 문서 본문의 규범 서술이 특정 Adapter Binding 문서명을 명명하면 이식 시 "Adapter만 교체·Core/Module 무변경"(04 §4.2 이식 불변, structure.md §7 C-1)이 깨지는 환경 결합이 생긴다 — framework/memory/ 문서의 일반형 포인터 관행과 정합. §6 스캔 주해도 해당 자가 분류를 정리하고 일반형 포인터·이식 불변 정합을 명기. 본문의 특정 Adapter Binding 문서명 토큰 잔존 0건 전수 확인(§9 r3 행에도 없음 — 시점 기록 불변). 투영 bullet·기존 3건 투영·최신 상태 해소·근거 절 나머지 문안 무변경, L-06 정합 재확인. 금지 토큰 0 재확인. `docs/v0.4-verification-report` 참조는 결정 기록 근거로 유지(session-handoff 참조와 동류). | Worker (Advisor 위임, Task V12 r4) |
| 2026-07-06 | v0.5 Baseline | v0.5 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 26/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.6 Draft (개정) | v0.6 Task L5 — Advisor 승인 하 격리 개정 (handoff §1.6 이월 후보 4 편입 · 사용자 승인 2026-07-06 · v0.5 V12 r3/r4 격리 개정 동형). §3.2 승격 규칙에 **승격(Candidate→Active) 레코드가 그 승격을 성립시킨 Advisor 승인 기록 참조를 `content` 페이로드 안에 자기완결적으로 첨부**하는 관례를 명시 편입 — 05 INV-4(승인 기록 참조 없는 승격은 `NotApproved`)와 § 포인터 연결. 이는 **새 필수 필드의 신설이 아니라** provenance(§2.4)를 보강하는 content 담김 관례이며 05 §3.2-A 필수 필드는 전건 보존됨을 본문 명기(계약 재정의·확장 0, §6). 승인 참조를 담는 라벨 키·물리 표기·직렬화 형태는 규정하지 않고 일반형 "Adapter Binding 문서 소관" 포인터 유지(§5.1·§5.2 물리 표기 규칙 동형 — 특정 Adapter 문서명 미명명, L-11·V12 r4 관행). 같은 상태 서술 전 지점 전수 갱신(L-06): 상태 라인·§3.2·§3.3 BP 대칭·§7 요약·다이어그램·§6 계약 재정의·금지 토큰 주해. 금지 토큰 0(C-3 확장) 개정분 포함 자가 전수 스캔 재확인, Glossary 밖 용어 신설 0. | Worker (Advisor 위임, Task L5) |
| 2026-07-06 | v0.6 Baseline | v0.6 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.7 Draft (개정) | v0.7 Task WF14 — Advisor 승인 하 비차단 정합 개정. 근거: docs/v0.6-verification-report.md §3.7 관찰 3 해소 (v0.7 편입 개정, 사용자 승인 2026-07-06). 라이브 본문이 05 INV-4를 "승인 기록 참조 없는 승격은 `NotApproved`"로 귀속시키던 괄호 주해를, 정본 소속대로 분리 정밀화 — INV-4 인용은 정본 문면("승격(`Candidate → Active`)은 Advisor 승인으로만 성립한다")으로, `NotApproved`는 05 §6 실패 모드(§2.6 reason 코드) 소속으로, "승인 기록 참조" content 첨부는 관례(§3.2) 소속으로 각각 귀속 분리 표기. 전 지점 전수 갱신(L-06 — 검색으로 열거): §3.2 승격 관례 절·§6 계약 재정의 절·§7 다이어그램 2행·§7 요약(총 5지점). §3.2 승격 권한 문장(line 156)·§3.2 NotApproved 거부 문장(line 159)·§3.3 BP 대칭·§2.6 reason 표 등 이미 정본 정합한 지점은 열거 후 무변경 확인. 05·04·02 계약 재정의·확장 0(개정은 주해 문언 정밀화로 한정 — 스키마 필드·투영 규칙·승격 규칙 무변경, "새 필수 필드 아님·05 §3.2-A 전건 보존" 기존 명기 보존). 금지 토큰 0(C-3 확장) 개정분 포함 자가 전수 재스캔(§6 금지 토큰 절에 WF14 스캔 기록 추가). §9 기존 행 문면 불변(시점 기록 — L-10) + 본 행 append. | Worker (Advisor 위임, Task WF14) |
| 2026-07-06 | v0.7 Baseline | v0.7 개정분(관찰 3 해소·상태 라인 정합) 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-XX·mi 유지)·삭제 산출물 참조 앵커 전환(@cd9247b·@004bfa9). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/05-lessons.md §3이다.** 이 문서는 그 Lessons Core Contract(생성·승격·회수·효과 추적·Best Practice 대칭)의 **인스턴스**이며, 스키마 필드·연산·불변 규칙을 **재정의·확장하지 않는다**. 계약 요소는 05의 해당 §를 § 포인터로만 참조한다 (structure.md §7 C-1).
- 이 문서는 Lessons 특화 계약이 이 프로젝트의 `framework/memory/` 경계에서 **어떤 형태로 인스턴스화되는가**를 규율한다 — Lesson·Best Practice·재발 판정 레코드의 포맷 인스턴스, 생성·승격 규칙, 재발 판정, 그리고 세 기록이 Memory Item의 `kind`로 단일 Port 위에 올라타는 방식이다. Lessons는 Layer가 아니라 Memory Service 위의 특화 계약이다 (05 INV-2, 05 §2).
- **이 문서는 Module 구현 디렉터리 문서다.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (structure.md §5 C-3 확장, 05 INV-9, 04 INV-8). 저장 위치·직렬화·인덱스·매칭 알고리즘의 구체 실현은 **Adapter Binding 문서 소관**(05 §4, 04 §4)이며, 필요한 자리에는 소관 포인터만 둔다.
- **Memory 계약 표면과의 경계.** Memory Service Interface(단일 Port), Memory Item, Memory Index의 상세는 **Memory 계약 문서 소관**이며 그 정본은 specs/04-memory.md §3이다. 본 문서는 04의 해당 §를 포인터로만 인용하고, 같은 Wave에서 동시 작성 중인 Memory 계약 문서의 내용을 인용·추측하지 않는다 (07 R2). Port·Item·Index의 상세가 필요한 자리에는 04 § 포인터 또는 "Memory 계약 문서 소관" 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Lesson·Best Practice·회수 정책·Memory Service Interface는 Glossary §3.2-C가, 적용 조건·승격·재발은 Glossary §3.2-J(05 §9 승인 반영)가 정본이다. 새 용어를 정본처럼 신설하지 않는다. §5의 `kind` 값 3종은 Advisor 확정 위임 범위 안의 값 명명이며(05가 `kind` 값 소유 — 04 §9·05 §9 결정 기록), 용어 신설이 아니다.

---

## §1. 목적·책임

Lessons 인스턴스의 책임은 세 가지다 (05 §1).

- 실패를 교훈(Lesson)으로, 성공을 모범 사례(Best Practice)로 기록해 다음 작업에서 회수 가능하게 한다 — 반복 실수 방지와 성공 재사용.
- "같은 실수의 반복"을 판정 가능한 계약(재발 판정)으로 환원한다 (ARCHITECTURE 3.5, 05 INV-7).
- 위 세 기록이 Memory Service Interface(단일 Port) 위에 Memory Item의 `kind`로 올라타는 경계를 확정한다 (05 INV-1, 04 §3.4).

이 문서가 규율하는 것과 규율하지 않는 것의 경계는 다음과 같다.

- **규율한다:** Lesson·Best Practice·재발 판정 레코드의 스키마 인스턴스(§2), 생성·승격 규칙(§3), 재발 판정 3분류(§4), `kind` 값과 applicability의 labels·kind 투영 규칙(§5).
- **규율하지 않는다:** Memory store 내부 구조·인덱스·직렬화·영속성(04·Adapter 소관), 적용 조건 매칭 알고리즘(Adapter 소관 — 05 §3.2-C, §4 SP-2), Learn·Memory Update 단계 전이(03 소관 — 05 §2 Non-Goals), 완료·실패 보고 포맷 자체(02 소관 — 입력으로만 소비), 역할 경계(02 §3.2-A).

---

## §2. 데이터 포맷 인스턴스 (정본: 05 §3.2)

아래 여섯 스키마는 05 §3.2-A~F의 **인용·대조**다. 필드·의미의 상세 정본은 05 §3.2가 유지하며, 본 문서는 재정의하지 않는다(재정의 없음). **필수/선택 표기는 정본과 그대로 보존한다** (v0.2 Lesson 후보 §1.5-2 "필수/선택 표기 보존" 적용). 직렬화 형식은 Adapter/04 소관이다 (05 §3.2 서두, §4 SP-1).

### §2.1 Lesson (교훈) — 8필드 (정본: 05 §3.2-A)

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Lesson 고유·안정 식별자. 회수·재발 판정·supersede의 기준. | 예 |
| `status` | `Candidate` / `Active` / `Superseded` / `Retired`. | 예 |
| `failure` | 무엇이 실패했는가 — 실패 현상 서술. 출처 실패 보고의 `reason`·`repro`에서 도출. | 예 |
| `cause` | 원인 — 왜 실패했는가 (근본 원인). | 예 |
| `lesson` | 교훈 — 다음에 무엇을 다르게 할 것인가. 실행 가능한 지시. | 예 |
| `applicability` | 적용 조건 — 언제 이 Lesson이 회수되어야 하는가. 회수 매칭 signature(§2.3). | 예 |
| `provenance` | 출처 — 어느 작업·실패 보고에서 생성됐는가(§2.4). | 예 |
| `supersedes` | 이 Lesson이 대체하는 이전 Lesson `id`. 재발 대응 시 사용. | 아니오 |

### §2.2 Best Practice (모범 사례) — 7필드 (정본: 05 §3.2-B)

Lesson과 대칭이다 (05 INV-8, Glossary §3.2-C).

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | 고유·안정 식별자. | 예 |
| `status` | `Candidate` / `Active` / `Superseded` / `Retired`. | 예 |
| `success` | 무엇이 성공했는가 — 성공 현상·맥락. 출처 완료 보고에서 도출. | 예 |
| `practice` | 모범 사례 — 재사용 가능한 방법. 다음에 무엇을 반복할 것인가. 실행 가능한 지시. | 예 |
| `applicability` | 적용 조건 — 언제 회수되어야 하는가(§2.3). | 예 |
| `provenance` | 출처 — 어느 작업·완료 보고에서 생성됐는가(§2.4). | 예 |
| `supersedes` | 대체하는 이전 Best Practice `id`. | 아니오 |

대칭 대응(05 §3.2-B): `Lesson.failure` ↔ `BestPractice.success`, `Lesson.cause`+`Lesson.lesson` ↔ `BestPractice.practice`. `id`·`status`·`applicability`·`provenance`는 두 스키마가 동일한 형태를 공유한다.

### §2.3 Applicability Condition (적용 조건) (정본: 05 §3.2-C)

회수 매칭의 기준이 되는 추상 signature다.

- 구성: 상황 유형(situation type)과 트리거 서술(어떤 맥락·작업 특성에서 이 기록이 관련되는가)의 집합.
- 회수 시 현재 작업의 상황 서술자(situation descriptor)와 대조되어 관련성(relevance)이 산출된다.
- 계약은 "적용 조건과 상황 서술자를 대조해 관련성을 산출한다"만 요구한다. 대조 알고리즘은 규정하지 않는다 — Adapter/04 소관이다 (05 §3.2-C, §4 SP-2). Memory Item의 `labels`·`kind`로의 투영 규칙은 §5가 정의한다.

### §2.4 Provenance (출처) — 4필드 (정본: 05 §3.2-D)

출처 없는 Lesson·Best Practice는 성립하지 않는다 (05 INV-5).

| 필드 | 의미 |
|---|---|
| `task_ref` | 어느 작업에서 생성됐는가. |
| `report_ref` | 원천 보고 참조 — 실패 보고(02 §3.2-D) 또는 완료 보고(02 §3.2-C). |
| `origin_role` | 후보를 제출한 역할(예: Worker)과 승격을 승인한 역할(Advisor). |
| `ordering_ref` | 생성 순서를 판정할 수 있는 순서 기준. 재발 판정의 "기존 Lesson이 작업 착수 전에 존재했는가"에 사용. 구체 시간 포맷은 직렬화(Adapter/04) 소관. |

### §2.5 Recurrence Judgment (재발 판정 레코드) — 5필드 (정본: 05 §3.2-E)

효과 추적 연산(§4)의 산출물이다.

| 필드 | 의미 |
|---|---|
| `failure_signature` | 판정 대상 새 실패의 signature. |
| `matched_lesson_id` | 매칭된 기존 Active Lesson의 `id`(있으면). |
| `was_recalled` | 그 Lesson이 해당 작업의 회수 집합에 포함되었는가. |
| `verdict` | `Novel` / `RecallGap` / `Recurrence`(§4). |
| `follow_up` | 후속 조치 참조 — 신규 후보 등록 / 회수 규칙·적용 조건 조정 / Lesson 강화·supersede. |

### §2.6 Failure Report (Lessons 연산 공통) — 4필드 (정본: 05 §3.2-F)

모든 Lessons 연산의 공통 실패 보고 구조다. 02 §3.2-D 실패 보고(Agent 보고)와 소속이 다르며 혼입하지 않는다 — 이 구조는 05 §3.2-F에 소속된다 (v0.2 Lesson 후보 §1.5-1 "필드 계약 혼입" 방지 적용).

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (RegisterCandidate / Promote / Recall / JudgeRecurrence / RegisterBestPractice). |
| `reason` | 사유 코드 (InvalidSource / MissingProvenance / PromotionCriteriaUnmet / NotApproved / PortReadFailed / PortWriteFailed / ScopeExceeded / SignatureUnmatchable). |
| `target` | 대상 (Candidate/Lesson/Best Practice `id`, 또는 출처 보고 참조). |
| `location` | 실패 지점 참조. |

---

## §3. 생성·승격 규칙 (정본: 05 §3.1-A·§3.1-D, §3.2-A 승격 규칙)

모든 저장·회수는 Memory Service Interface(단일 Port)를 경유한다 (05 INV-1, §6). 아래는 05 연산 계약의 운용 인스턴스이며, 단계 전이 시점(언제 호출되는가)은 03 소관이다 (05 §3.1-A 주의, §2 Non-Goals).

### §3.1 Register Candidate (후보 등록) — 입력: 02 §3.2-D 실패 보고

- **입력.** 02 §3.2-D 실패 보고 1건 — `reason`·`repro`·`attempted`·`lesson_candidate`·`blocking` + 출처 작업 참조 (05 §3.1-A). 이 5필드는 02 §3.2-D 소속이며 본 문서는 입력으로 소비할 뿐 재정의하지 않는다.
- **`lesson_candidate.여부 = 예`인 실패:** 정확히 하나의 Lesson Candidate(§2.1, status=`Candidate`)로 **즉시 등록**되고, provenance(§2.4)가 채워지며, Port를 통해 기록된다 (05 §3.1-A 완료 조건).
- **`lesson_candidate.여부 = 아니오`인 실패:** 자동 등록되지는 않으나 **후보 자격은 유지된다** — 승격 심사에서 재평가 대상이 된다 (05 INV-3 보편 후보 자격, AGENT.md "모든 실패는 Lesson 후보"). 여부=아니오는 후보 자격을 소멸시키지 않는다.
- **실패 보고(§2.6):** reason = `InvalidSource`(실패 보고 형식 아님) / `MissingProvenance` / `PortWriteFailed`.

### §3.2 Promote (승격 — Candidate → Active): 3조건 + Advisor 전속 권한

**승격 3조건 (05 §3.2-A 승격 규칙).** 다음을 **모두** 만족해야 Candidate가 Active로 승격된다.

1. `failure`·`cause`·`lesson`·`applicability`·`provenance`가 모두 채워져 있다 (검증 가능성, 05 INV-5).
2. Verifier의 Learn 입력(독립 판정)이 실패의 실재를 뒷받침한다 (02 §3.1 Verify 단계 산출물).
3. Advisor가 승격을 승인한다.

**승격 권한 = Advisor 전속 (05 INV-4).** 승격(`Candidate → Active`)은 Advisor 승인으로만 성립한다. Worker는 후보를 제출하고, Verifier는 Learn 입력(근거)을 제공하며, **승격 결정 권한은 Advisor에 있다** (역할 경계 02 §3.2-A). Worker의 자기 점검은 최종 승인이 아니다.

- **출력.** 정식 Lesson(status=`Active`) — 안정적 `id`와 매칭 가능한 `applicability`(§2.3)를 갖는다.
- **Advisor 승인 없는 승격은 거부된다:** 실패 보고(§2.6) reason = `NotApproved`. 그 밖의 승격 실패 reason = `PromotionCriteriaUnmet` / `PortWriteFailed`.
- **승인 기록 참조의 content 자기완결 첨부 (승격 레코드 관례).** 승격으로 기록되는 Active 레코드는 그 승격을 성립시킨 **Advisor 승인 기록의 참조**(위 조건 3의 승인 — 승격 심사 기록 등 승인 원본을 가리키는 참조)를 자신의 **`content` 페이로드 안에 자기완결적으로 첨부한다.** 이로써 05 INV-4(정본 문면: "승격(`Candidate → Active`)은 Advisor 승인으로만 성립한다" — 05 §3.3)의 충족을 **레코드 자체로** 확인·검증할 수 있으며, 별도의 외부 기록을 경유하지 않고 자기완결적으로 성립한다. 여기서 세 항목의 정본 귀속은 서로 다르다 — (a) INV-4 정본 문면은 위 인용대로 "Advisor 승인으로만 성립"이고, (b) 승인 없는 승격을 거부하는 실패 코드 `NotApproved`는 INV-4 문면이 아니라 **05 §6 실패 모드(§2.6 reason 코드 — INV-4 위반 시 발부되는 코드)** 소속이며, (c) 그 승인의 **"기록 참조"를 `content`에 첨부하는 것**은 본 절이 도입한 **관례(§3.2)의 표현**이지 INV-4 정본 문면도 새 필수 필드도 아니다. 이 관례는 provenance(§2.4 — 특히 `origin_role`의 "승격을 승인한 역할")를 보강하는 **content 담김 관례**이며, **새 필수 필드의 신설이 아니다** — 05 §3.2-A 필수 필드는 전건 보존되고 05·04·02 계약은 재정의·확장되지 않는다(§6). 승인 참조를 담는 **라벨 키·물리 표기·직렬화 형태**는 본 문서의 다른 물리 표기와 동일하게 규정하지 않으며, 그 정본은 Adapter Binding 문서 소관이다(§5.1·§5.2 물리 표기 규칙 동형).
- **Best Practice 대칭.** 위 승격 3조건·전속 권한·승인 기록 참조 관례는 Best Practice 승격에도 대칭 적용된다 (§3.3).

### §3.3 Best Practice 대칭 (정본: 05 §3.1-D, INV-8) — 입력: 02 §3.2-C 완료 보고

Best Practice는 Lesson과 **대칭**이며 동일한 저장·회수·승격 계약을 따른다 (05 INV-8). 실패에서 Lesson이, 성공에서 Best Practice가 도출된다.

- **입력.** 02 §3.2-C 완료 보고 1건 — `artifacts`·`self_check`·`verify_basis` + 출처 작업 참조 (05 §3.1-D). 이 필드들은 02 §3.2-C 소속이며 재정의하지 않는다.
- **Verify 통과 전제.** 완료 보고는 Verify 단계를 통과한 뒤에만 생성되므로(02 INV-4), Best Practice 후보는 Verify를 통과한 완료 보고에서만 도출된다. "모든 성공은 Best Practice 후보"(AGENT.md)이므로 후보 자격은 Verify를 통과한 모든 완료 보고에 보편적으로 성립한다.
- **승격.** Candidate → Active 승격은 Lesson과 **동일한 권한·절차**를 따른다 (05 INV-4·INV-9) — Advisor 전속 승인, provenance(§2.4) 필수, **승인 기록 참조의 content 자기완결 첨부 관례(§3.2)도 대칭 적용**된다. 실패 보고 코드 집합은 §2.6과 동일하다.
- 02 §3.2-C 완료 보고에는 `lesson_candidate`와 대칭인 명시 필드가 없다. 명시 필드 추가 여부는 02의 결정 사항이며(05 §9·04 §9 결정 기록: v0.2 이후 재검토, 보편 후보 자격으로 충족), 본 문서는 02를 수정하지 않고 추측하지 않는다.

---

## §4. 재발 판정 (정본: 05 §3.1-C — Judge Recurrence)

효과 추적 연산은 새 실패를 세 결과 중 정확히 하나로 분류한다. 이 연산이 ARCHITECTURE 3.5 "같은 실수를 반복하지 않는다"를 검증 가능한 판정으로 환원한다 (05 INV-7).

- **입력.** 새 실패의 signature(실패 보고에서 도출) + 그 작업에서 회수된 Lesson 집합(회수 이력) + `applicability`가 매칭되는 기존 Active Lesson(Port 조회) (05 §3.1-C).
- **회수 이력의 소속 경계.** "작업별 회수 집합(회수 이력)"의 저장·기록 주체는 **03 루프 상태 기록 소관**이며, 이 연산은 회수 이력을 **입력으로 받는다** (05 §9 결정 기록·04 §9 결정 기록: "회수 이력은 03 소관, 05는 입력으로 받는다"). 본 문서는 회수 이력을 생성·저장하지 않는다.
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

Lesson·Best Practice·재발 판정 레코드는 별도 저장 경로를 갖지 않는다. 셋 모두 **Memory Item의 `kind`로 단일 Port 위에 올라탄다** (04 §3.4, 04 §8 예3). Memory는 `kind`·`content`를 불투명하게 다루며(04 INV-5), `kind` 값·`content` 상세 스키마는 05(이 인스턴스)가 소유한다 (04 §9 결정 기록, 05 §9 결정 기록 (a)).

### §5.1 `kind` 값 3종 (AI·언어 비의존 확정)

세 특화 기록에 대해 다음 세 개의 안정 분류자(`kind`) 값을 확정한다. 이 값들은 Glossary 개념(Lesson·Best Practice·재발)을 지칭하는 개념 분류자이며, 특정 AI·언어·툴체인·직렬화 형식에 의존하지 않는다.

| 특화 기록 (스키마) | 확정 `kind` 값 | `content` 상세 스키마 소유 |
|---|---|---|
| Lesson (§2.1) | `lesson` | 본 문서 §2.1 (05 §3.2-A 정본) |
| Best Practice (§2.2) | `best-practice` | 본 문서 §2.2 (05 §3.2-B 정본) |
| 재발 판정 레코드 (§2.5) | `recurrence-judgment` | 본 문서 §2.5 (05 §3.2-E 정본) |

- 세 값은 서로 구별되는 안정 분류자다. Memory는 이를 불투명 분류자로만 취급한다 (04 INV-5, 04 §3.2-A `kind` 행).
- 이 값들의 **구체 직렬화 표기**(구분자·대소문자·물리 인코딩)는 Adapter 직렬화 소관이다 (05 §4 SP-1, 04 §4). 본 문서는 분류자의 안정적 정체성만 확정하고 물리 표기를 규정하지 않는다.
- `content`에는 각 스키마(§2)의 필드가 담기며, 그 상세는 05가 소유한다. Memory는 `content` 내부를 해석하지 않는다 (04 INV-5). 단, 회수·상태 해소·재발 판정 조회를 위해 `content`의 일부 필드(Lesson·Best Practice의 안정 `id`·`status`, 재발 판정 레코드의 `verdict`·`matched_lesson_id`)는 Memory Item의 `labels`로도 투영된다 (§5.2) — 이는 index 단계 후보 축소용 태그 부여이며 Memory가 `content`를 해석하는 것이 아니다.

### §5.2 Memory Item `labels`·`kind` 투영 규칙 (applicability·안정 `id`·`status`·재발 판정 `verdict`·`matched_lesson_id` — 04 §9 결정 기록 정합)

회수(05 §3.1-B)는 Memory Item의 `labels`·`kind`를 통해 후보 범위를 index 단계에서 좁힌 뒤 Port 위에서 관련성을 산출한다. 투영 규칙은 다음과 같다.

- **기록 종류 투영 → `kind`.** 회수 대상이 Lesson인지 Best Practice인지는 §5.1의 `kind` 값으로 구분된다. Recall scope의 `kind` 차원(04 §3.2-B)이 이 구분을 해소한다.
- **적용 조건 투영 → `labels`.** applicability(§2.3)의 상황 유형·트리거 서술은 Memory Item의 `labels`로 투영된다. Recall scope의 `labels` 차원(04 §3.2-B)이 회수 후보를 좁힌다. "applicability는 `labels`·`kind`로 투영 가능하다"(04 §9 결정 기록)와 정합한다.
- **안정 식별 투영 → `labels`.** Lesson·Best Practice의 **안정 `id`**(§2.1/§2.2의 `id` 필드 — `content`에 담긴 안정 식별자)를 Memory Item의 `labels`로 투영한다. 재발 판정(§4)·supersede(§2.1 `supersedes`)·최신 상태 해소(아래)의 index 단계 후보 축소에 쓰인다. 이 안정 `id`는 Record가 매 기록에 유일 할당하는 Memory Item `id`(04 §3.2-A)와 구별되며, 여러 Memory Item이 같은 안정 `id`를 `labels`로 공유할 수 있다.
- **상태 투영 → `labels`.** `status`(§2.1/§2.2 — `Candidate`/`Active`/`Superseded`/`Retired`)를 Memory Item의 `labels`로 투영한다. 05 §3.1-B 회수 출력("`applicability`가 매칭되는 **Active** Lesson·Active Best Practice의 최소 집합")을 index 단계에서 필터할 수 있게 한다. `labels`는 Index Entry(04 §3.2-C)에도 실리므로, `content` 원문 로드(`detail = full`) 없이 index 단계에서 `Active`만 걸러진다 (04 INV-4 최소 Context 우선 정합, 05 INV-6).
- **최신 상태 해소 규칙.** 기록은 불변이다(04 INV-6, append-only). `status` 전이(예: `Candidate → Active`, §3.2)는 기존 Memory Item을 변경하지 않고 **새 Memory Item 기록으로 표현된다**. 따라서 같은 안정 `id`로 투영된 Memory Item 중 **`timestamp`(04 §3.2-A) 최신 항목**이 그 Lesson·Best Practice의 **현재 상태**를 나타낸다. 회수(05 §3.1-B)와 재발 판정(§4의 매칭 Active Lesson 조회)은 이 최신 항목을 기준으로 한다.
- **재발 판정 레코드 투영 → `labels`.** 재발 판정 레코드(§2.5)의 `verdict`(§2.5)와 `matched_lesson_id`(§2.5)를 Memory Item의 `labels`로 투영한다. 재발 판정 레코드(`kind=recurrence-judgment`, §5.1)를 `content` 원문 로드(`detail = full`) 없이 index 단계에서 조회·후보 축소할 수 있게 한다 — `labels`는 Index Entry(04 §3.2-C)에도 실리므로 index 단계에서 걸러지고, 최소 Context 원칙(04 INV-4, 05 INV-6)과 정합한다. 이 두 필드의 의미 정본은 §2.5(05 §3.2-E)이며(`verdict` ∈ `Novel`/`RecallGap`/`Recurrence`, `matched_lesson_id`는 매칭된 Active Lesson의 안정 `id` — 있으면), 본 규칙은 그 필드를 **무엇에 투영하는가**만 확정한다. 라벨 키의 물리 표기는 다른 투영과 동일하게 규정하지 않는다(아래 "매칭 알고리즘·라벨 물리 표기는 정의하지 않는다" 규칙 — Adapter Binding 문서 소관).
- **Port의 역할 = 범위 조회만.** Port는 `kind`/`labels`/`timeRange`/`source` **범위 조회만** 제공하며 이를 위해 04 계약을 변경하지 않는다 (04 §9 결정 기록, 04 §3.1-C 회수 정책). 회수 정책(필요할 때만·목적 명시·최소 범위)은 Port가 강제하며, 전량 로드는 금지된다 (04 INV-2/INV-3/INV-4, 05 INV-6).
- **최종 대조는 Port 위에서.** 상황 서술자 ↔ `applicability` 최종 대조(관련성 산출)는 Port가 좁힌 후보 위에서 수행된다. 이 **매칭 계약 표면은 05가 소유하고, 매칭 구현(대조 알고리즘)은 Adapter 소관이다** (05 §3.2-C, §4 SP-2, 04 §9 결정 기록).
- **매칭 알고리즘·라벨 물리 표기는 정의하지 않는다.** 본 문서는 상황 서술자와 `applicability`를 어떤 알고리즘(키워드·의미 검색·임베딩 등)으로 대조하는지 규정하지 않는다 — Adapter 소관이다 (05 §3.2-C). 위 투영(적용 조건·안정 `id`·`status`·재발 판정 `verdict`·`matched_lesson_id`) **전부**에서 **라벨 키의 물리 표기**(라벨 키 이름·직렬화 형태) 역시 Adapter 소관이며(05 §4 SP-1, 04 §4; 물리 표기 정본은 Adapter Binding 문서 소관), 본 문서는 "무엇을 `labels`에 투영하는가"만 확정한다. Memory store 내부 구조·인덱스·직렬화는 Memory 계약 문서(04) 및 Adapter 소관이다.

**근거 (Advisor 결정 — v0.4, OQ-M5-1 해소).** 안정 `id`·`status` 투영과 최신 상태 해소 규칙은 05 §3.1-B 회수 출력(Active 최소 집합)의 index 단계 해소를 위해 추가되었다 — 전량 로드(`detail = full`)로만 `Active`를 거르면 최소 Context 원칙(05 INV-6, 04 INV-4)과 상충한다. `labels`는 04 §3.2-A의 **자유 태그 집합**이며 무엇을 투영하는가는 특화 계약(05·본 문서)이 소유하므로, 이 보강은 `labels` 사용 방식의 확정일 뿐 **04·05 계약 변경이 아니다** (04 §9 결정 기록 "applicability는 labels·kind로 투영 가능"의 확장선, structure.md §7 C-1 계약 재정의 0 유지).

**근거 (Advisor 결정 — v0.5, `uahf/docs/v0.4-verification-report.md@cd9247b` §3.4 관찰 1 해소).** 재발 판정 레코드(`kind=recurrence-judgment`)의 `verdict`·`matched_lesson_id`는 v0.4부터 index 단계 조회용으로 `labels`에 투영되어 왔으나, "무엇을 투영하는가는 05가 소유한다"는 원칙에 비추어 그 투영 결정 자체가 본 절(05 소유 투영 규칙)에 명시되지 않았다. v0.5에서 이 투영 2건을 본 절에 명시 편입해 완결성을 회복한다. `verdict`·`matched_lesson_id`는 §2.5(05 §3.2-E)가 소유하는 재발 판정 레코드 필드이고 `labels`는 04 §3.2-A의 **자유 태그 집합**이므로, 이 편입은 안정 `id`·`status` 투영과 동일하게 `labels` 사용 방식의 확정일 뿐 **04·05 계약 변경이 아니다** (v0.4 결정 승계 — 04 §9 결정 기록 "applicability는 labels·kind로 투영 가능"의 확장선, structure.md §7 C-1 계약 재정의 0 유지). 라벨 키의 물리 표기는 위 물리 표기 규칙대로 Adapter Binding 문서가 소유하며, 본 개정은 그 물리 표기를 재서술·확정하지 않는다.

---

## §6. 단일 Port·경계·계약 재정의 0 (정본: 05 INV-1)

- **단일 Port (05 INV-1).** 모든 Lesson·Best Practice·재발 판정 레코드의 저장(§3 생성·승격, §4 판정 레코드 기록)과 회수(§3.1-B Recall, §4 매칭 Lesson 조회)는 **Memory Service Interface(단일 Port)를 경유한다**. Lessons 인스턴스는 영속성 백엔드에 직접 접근하지 않는다 (04 INV-1). 우회 접근은 위반이다.
- **쓰기 시점·조건.** 기록 대상(Lesson Candidate, 승격된 Active Lesson·Best Practice, 재발 판정 레코드)의 기록은 Memory Update 단계에서 일어나며(단계 전이는 03 소관), 모든 기록은 provenance(§2.4)를 포함한다 (05 §5, INV-5).
- **읽기 시점·범위.** 회수는 Consult 단계에서 회수 정책에 따라 **최소 범위**로 일어난다(단계 전이는 03 소관). 적용 조건이 매칭되는 최소 집합만 읽고 전량 로드하지 않는다 (05 INV-6, 04 INV-3/INV-4).
- **계약 재정의 0.** 본 문서는 05·04·02 계약을 재정의·확장하지 않는다. §2 스키마는 05 §3.2의 인용(재정의 없음), Memory Item·Port·Index 참조는 04 § 포인터, 완료·실패 보고 입력은 02 § 포인터로만 연결한다 (structure.md §7 C-1). 필드 소속을 § 포인터로 명시해 다른 계약의 필드와 혼입되지 않게 한다 (v0.2 Lesson 후보 §1.5-1 적용). §3.2 승격 레코드의 승인 기록 참조 첨부는 **content 담김 관례(§3.2)**일 뿐 새 필수 필드의 신설이 아니며 05 §3.2-A 필수 필드는 전건 보존된다 — 이는 05 INV-4(정본 문면: "승격은 Advisor 승인으로만 성립한다")의 충족을 레코드 자체로 자기완결 검증하도록 돕는 관례이지 계약 요소의 재정의·확장이 아니다. INV-4 정본 문면과, 승인 없는 승격의 거부 코드 `NotApproved`(05 §6 실패 모드·§2.6 reason 코드)와, 이 "승인 기록 참조" content 첨부 관례(§3.2)는 서로 소속이 다른 별개 항목이다.
- **동시 작성 문서 불인용 (07 R2).** 같은 Wave에서 동시 작성 중인 Memory 계약 문서(Port·store)의 내용을 인용·추측하지 않았다. Port·Memory Item·Memory Index의 상세는 04 § 포인터 또는 "Memory 계약 문서 소관" 포인터로만 참조했다.
- **금지 토큰 0 (structure.md §5 C-3 확장).** 본문 전체를 후보 집합 **전체**(특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명)로 전수 스캔한 결과 0건이다(v0.6 개정분 포함 재스캔 — §3.2 승격 승인 기록 참조 관례 편입분 포함. 승인 참조의 라벨 키·물리 표기·직렬화 형태는 명명하지 않고 일반형 "Adapter Binding 문서 소관" 포인터만 두었다). §5.1의 `kind` 값 3종(`lesson`·`best-practice`·`recurrence-judgment`)은 Glossary 개념을 지칭하는 분류자 값이며, 승인된 Advisor 위임 범위 안의 값 명명(05가 `kind` 값 소유)으로 금지 토큰 부류에 속하지 않는다. `status`·`verdict`·`matched_lesson_id`·reason 코드 등 나머지 리터럴은 05 §3.2 정본에서 그대로 인용한 계약 값이다. §5.2 근거·§9의 프로젝트 문서명 참조(검증 리포트 `docs/v0.4-verification-report`)는 결정 기록의 근거로 인용한 저장소 내부 상호 참조이며(session-handoff 참조와 동류) 금지 토큰 부류(AI·언어·툴체인·직렬화 형식)에 속하지 않는다. 물리 표기·매칭 구현이 필요한 자리에는 특정 Adapter Binding 문서명을 명명하지 않고 일반형 "Adapter Binding 문서 소관" 포인터만 두어 이식 불변(structure.md §7 C-1, 04 §4.2 — Adapter만 교체·Core/Module 무변경)과 정합한다 — 어댑터 하위 경로·백엔드 데이터 경로 등 물리 경로·인스턴스 토큰은 인용하지 않았다. 구체 인스턴스(직렬화 표기·저장 위치·매칭 알고리즘)가 필요한 자리에는 소관 포인터만 두었다. v0.7 Task WF14 관찰 3 해소 주해 정밀화분(INV-4 정본 문면 인용·`NotApproved`의 05 §6 실패 모드 소속·"승인 기록 참조" 관례의 §3.2 소속을 분리 표기)도 본문 전수 재스캔했고 금지 토큰 0을 유지한다 — 인용된 `NotApproved`·`Active`·INV-4·§ 번호는 05 정본에서 인용한 계약 값·소관 포인터이며 금지 토큰 부류(AI·언어·툴체인·직렬화 형식)가 아니다.

---

## §7. 요약 (Lessons 인스턴스 한눈에 보기)

```
실패 보고(02 §3.2-D)          완료 보고(02 §3.2-C, Verify 통과)
      │ lesson_candidate            │ 보편 후보 자격
      ▼                             ▼
Register Candidate(§3.1)      Register BP Candidate(§3.3)
      │  status=Candidate            │  status=Candidate
      ▼                             ▼
Promote(§3.2) ── 3조건 + Advisor 전속 승인(05 INV-4 정본 문면) ── 미승인 시 거부: NotApproved(05 §6 실패 모드)
        · Active 레코드는 승인 기록 참조를 content에 자기완결 첨부(관례 §3.2 — 새 필수 필드 아님; 05 INV-4 충족을 레코드 자체로 확인)
      ▼                             ▼
Active Lesson(§2.1)           Active Best Practice(§2.2)
      │  kind=lesson                 │  kind=best-practice
      └─────────────┬───────────────┘
                    ▼
        단일 Port(05 INV-1) — labels·kind 투영(Lesson·BP): applicability·안정 id·status(§5.2)
                    ▼
   Consult 회수(Active 최소 집합·최신 status, 05 §3.1-B·INV-6) → 다음 작업에서 같은 실수 회피
                    │
                    ▼
   Judge Recurrence(§4) → Novel / RecallGap / Recurrence
        · 회수 이력은 03 소관, 입력으로 받음(05 §9)
        · 재발 판정 레코드 kind=recurrence-judgment; verdict·matched_lesson_id → labels 투영(§5.2)
```

- 세 특화 기록(Lesson·Best Practice·재발 판정 레코드)은 Memory Item의 `kind`(`lesson`·`best-practice`·`recurrence-judgment`)로 단일 Port 위에 올라탄다 (§5.1, 05 INV-1·INV-2, 04 §3.4).
- 승격은 Advisor 전속 권한이다 (05 INV-4 정본 문면: "승격은 Advisor 승인으로만 성립한다"; §3.2). 자기 점검·독립 판정은 승격 근거이지 승격 결정이 아니다. 승격으로 기록되는 Active 레코드는 그 **Advisor 승인 기록 참조를 `content`에 자기완결적으로 첨부**해 그 INV-4 충족을 레코드 자체로 확인 가능하게 한다 (§3.2 관례 — 새 필수 필드 신설 아님·05 §3.2-A 전건 보존; 승인 없는 승격의 거부 코드 `NotApproved`는 05 §6 실패 모드 소속, 라벨 키·물리 표기는 Adapter Binding 문서 소관).
- 재발 판정 3분류가 "같은 실수를 반복하지 않는다"를 검증 가능화한다 (§4, 05 INV-7). 회수 이력은 03 소관이며 입력으로 받는다 (§4, 05 §9).
- applicability·안정 `id`·`status`(Lesson·Best Practice)와 `verdict`·`matched_lesson_id`(재발 판정 레코드)가 Memory Item의 `labels`·`kind`로 투영되고, 같은 안정 `id` 중 최신 `timestamp` 항목이 현재 `status`를 해소해 05 §3.1-B의 **Active 최소 집합**을 index 단계에서 필터한다 (§5.2, OQ-M5-1·v0.4 검증 §3.4 관찰 1 해소, 04 INV-4·INV-6 정합). 매칭 계약 표면은 05 소유·구현은 Adapter 소관이며, 매칭 알고리즘·라벨 물리 표기·store 내부·직렬화는 본 문서가 정의하지 않는다.
- 본문에 특정 AI·언어·툴체인·직렬화 형식 토큰은 0건이며, 05·04·02 계약 재정의는 0건이다 (§6).
