# framework/workflow/work-graph — UAHF Workflow 정의 포맷 인스턴스

작성일: 2026-07-06
상태: v0.7 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/07-workflow.md §3.2-A — Work Graph(작업 그래프) 5필드 스키마와 병렬 집합 도출 문면의 정본. 본 문서 §2가 인스턴스화하는 계약.
- specs/07-workflow.md §3.2-B — Task(하위 작업) 7필드 스키마와 `done`·`interfaceContract`의 ROADMAP v0.7 완료 조건 대응 문면의 정본. 본 문서 §3이 인스턴스화하는 계약.
- specs/07-workflow.md §3.2-E — 공통 Failure Report 4필드와 `reason` 9종 열거의 정본. 본 문서 §4가 인스턴스화하는 계약.
- specs/07-workflow.md §3.3 INV-3 — 위임 계약 불침범(위임 메시지·역할 경계 포맷은 02 소유이며 Workflow는 인용). 본 문서 §0·§3이 준수·대조하는 불변.
- specs/07-workflow.md §3.1 — 분해·디스패치·병합 연산 규칙(각 연산의 완료 조건·실패 보고 결합). 이 파일 소관이 아니다(포맷만 소유). 연산 규칙의 인스턴스 문서(별도 소관)가 본 Failure Report 포맷을 § 포인터로 참조한다. 본 문서 §0·§4가 경계로 참조.
- specs/07-workflow.md §3.2-D — Merge Result(병합 결과). 이 파일 소관이 아니다 — 07 §3.2-D 소관 별도 인스턴스 문서(병합 규칙) 소관. 본 문서 §0·§5가 경계로 참조(추측·인용 없음).
- specs/07-workflow.md §4.1·§4.2 — Adapter Binding(직렬화 행)·이식 교체 지점. 직렬화 형식·물리 위치의 소관 포인터(본 문서 §5).
- specs/02-agent.md §3.2-B — 위임 메시지(Delegation Message)의 정본. Task의 `delegation` 필드가 § 포인터로만 인용한다(07 INV-3). 본 문서 §3.
- specs/00-glossary.md §3.2-J(J-07) — Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- framework/core/structure.md §2 — 본 파일의 소속 경계(Module 구현 디렉터리 `framework/{loop,memory,verifier,workflow,plugins}/` 중 `framework/workflow/`). 본 파일이 이 경계의 첫 실사용 인스턴스다(structure.md §8 트리 — workflow는 종전 미실현·빈 디렉터리).
- framework/core/structure.md §5 — 금지 토큰 규칙(확정 조건 C-3 확장). 본 문서 본문 준수 대상.
- framework/loop/loop-state-record.md — 데이터 포맷 인스턴스 문서 관례 표본(문서 머리 구조·§9 이력 절 머리 배치·§0 정본 경계·§ 포인터 표기 관례·말미 요약 절·자가 전수 스캔 기록 형식).
- AGENT.md — 상위 규약.

거버넌스: 이 문서는 `framework/workflow/` 소속 Module 구현 디렉터리 문서다. 문서 본문은 특정 AI·언어·툴체인·직렬화 형식·물리 경로 비의존을 유지한다(structure.md §5, C-3 확장). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.7 Draft | 최초 작성. Work Graph 5필드(07 §3.2-A)·Task 7필드(07 §3.2-B)·공통 Failure Report 4필드+`reason` 9종(07 §3.2-E)을 전건 § 포인터 인용으로 인스턴스화(필드명·의미·필수/선택 표기·`reason` 열거 정본 그대로 보존). 병렬 집합 도출 문면(07 §3.2-A 말미)·`done`·`interfaceContract`의 ROADMAP v0.7 대응 문면(07 §3.2-B 말미) 보존, `delegation`의 02 §3.2-B 인용(07 INV-3). Failure Report 포맷 인스턴스 소유 선언(§0·§4 — 연산 규칙 인스턴스 문서가 § 포인터로 참조). Merge Result(07 §3.2-D)·연산 규칙(07 §3.1) 비소관(포맷만 소유), 직렬화·물리 위치 비서술(Adapter Binding 소관 포인터). 07 계약 재정의·확장 0, 새 필드 0, Glossary 밖 새 용어 0, 물리 경로·형식 토큰 0(자가 전수 스캔 — §5). | Worker (Advisor 위임, Task WF1) |
| 2026-07-06 | v0.7 Baseline | v0.7 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/07-workflow.md §3.2다.** 이 문서는 그 Core Contract의 **인스턴스**이며, 계약을 재정의·확장하지 않는다. 계약 요소는 § 포인터로만 참조한다(structure.md §7 C-1과 같은 인스턴스 원칙). 세 포맷의 필드·의미·필수/선택 표기·`reason` 열거의 **진위 판정 기준은 정본 07 §3.2-A/B/E가 유지한다.**
- 이 문서는 `framework/workflow/` 아래 **Workflow 정의 포맷**을 확정한다. 07 §3.2-A(Work Graph)·§3.2-B(Task)·§3.2-E(공통 Failure Report) 세 포맷을 이 경계 위에 배치·대조한다.
- **이 문서는 Module 구현 디렉터리 문서다.** `framework/workflow/`는 structure.md §2가 지정한 Module 구현 디렉터리 경계이며, 이 문서가 그 경계의 **첫 실사용 인스턴스**다(structure.md §8 트리에서 workflow는 종전 미실현·경계만 확보된 빈 디렉터리였다 — `framework/memory/`가 v0.4에, `framework/verifier/`가 v0.5에, `framework/loop/`가 v0.6에 자기 경계의 첫 실사용 인스턴스가 된 것과 동형). 이 문서 본문은 특정 AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로·확장자를 두지 않는다(structure.md §5 C-3 확장, 07 §3.3 INV-9).
- **Failure Report 포맷 인스턴스 소유 선언.** 이 문서가 공통 Failure Report 포맷(07 §3.2-E)의 **인스턴스 소유 문서**다. 각 연산(분해·디스패치·병합)의 규칙 인스턴스 문서(별도 소관 — 07 §3.1 연산 규칙의 인스턴스)는 실패 보고를 낼 때 이 포맷을 **§ 포인터로 참조**한다. 각 `reason` 코드를 어느 연산이 언제 산출하는가(연산별 완료 조건·실패 보고 결합)는 07 §3.1과 그 규칙 인스턴스 문서 소관이며, 본 문서는 포맷의 `reason` 열거만 소유·보존한다(상세 §4).
- **소관 밖 경계.** Merge Result(07 §3.2-D)는 이 파일 소관이 아니다 — **07 §3.2-D 소관 별도 인스턴스 문서(병합 규칙) 소관**이며, 본 문서는 그 내용을 추측·인용하지 않고 일반 포인터만 둔다(07 R2). 분해·디스패치·병합 연산 규칙(07 §3.1)의 전개도 이 파일 소관이 아니다 — **포맷만 소유한다.**
- **위임 계약 불침범.** `delegation` 필드는 02 §3.2-B 위임 메시지를 **§ 포인터로만 인용**한다(07 INV-3). 위임 메시지·역할 경계 포맷은 02 소유이며 본 문서는 재정의하지 않는다.
- **물리 실현 비서술(경계).** 세 포맷의 **물리 형식·직렬화·물리 위치·물리 경로**는 이 문서가 서술하지 않는다. 이는 **Adapter Binding 문서 소관**이다(07 §4.1 직렬화 행·§4.2 이식 교체 지점). 필요한 자리에는 "Adapter Binding 문서 소관" 포인터만 둔다(§5).
- **07 내부 § 포인터·INV 참조 표기 관례.** 07 정본 셀을 보존할 때, 07의 내부 § 포인터·INV 참조는 `07 §…`·`07 INV-…` 접두로 명시하여 본 문서 자신의 절 번호와 구분한다. 이는 셀의 대상 지시를 명료화하는 표기이며 셀 내용(필드명·의미·필수/선택 표기)을 변경하지 않는다(loop-state-record §0·verification-report §0의 표기 관례와 동형).
- 용어는 specs/00-glossary.md 정본(§3.2-J J-07)만 사용한다. 새 용어를 신설하지 않는다. "Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약"은 J-07 표제어이며, "공통 Failure Report·`reason` 사유 코드" 등은 07 §3.2-E 정본이 정의한 포맷·필드 명칭이지 본 문서 신설 용어가 아니다.

---

## §1. 목적

`framework/workflow/`의 이 규격은 세 가지를 확정한다.

- **Work Graph 포맷** — 큰 작업의 분해 결과를 담는 정의 포맷의 5필드와 각 필드의 필수 표기, 병렬 집합 도출 규정(§2).
- **Task 포맷** — 분해의 최소 단위의 7필드와 각 필드의 필수 표기, `done`·`interfaceContract`의 ROADMAP v0.7 완료 조건 대응, `delegation`의 02 §3.2-B 인용(§3).
- **공통 Failure Report 포맷** — 모든 Workflow 연산의 공통 실패 보고 4필드와 `reason` 9종 사유 코드, 그리고 이 파일이 그 포맷의 인스턴스 소유 문서라는 선언(§4).

이 규격은 07 §3.2-A·§3.2-B·§3.2-E Core Contract의 **인스턴스**다. 계약 요소(필드·필수 표기·`reason` 열거)를 재정의·확장하지 않는다. 형태 A(문서)에서 형태 B(실행 코드)로 전환되어도 07 §3 Core Contract 변경은 0이며, 위반(형태 B가 07 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다(structure.md §7 C-1과 같은 불변 원칙).

---

## §2. Work Graph 포맷 인스턴스 (정본: 07 §3.2-A)

Work Graph는 Workflow의 정의 포맷이다. 큰 작업의 분해 결과를 담는다(07 §3.2-A). 아래 필드·의미·필수 표기는 07 §3.2-A 정본을 **그대로 보존**한다(재정의 0, 새 필드 0). 필드명뿐 아니라 필수 속성 표기(예/아니오)와 그 괄호 단서까지 정본과 일치시킨다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `goal` | 워크플로 전체의 목표와 범위. | 예 |
| `tasks` | Task(07 §3.2-B) 목록. 분해된 하위 작업 전부. | 예 |
| `dependencies` | Task 간 의존 관계 — 선행 Task id → 후행 Task id. 순환이 없어야 한다. | 아니오(없으면 전부 독립) |
| `parallelSets` | 병렬 집합 목록. 각 집합은 동시에 디스패치 가능한 Task id 그룹이다. 같은 집합의 Task는 서로 의존하지 않고 소유 경계가 겹치지 않는다. | 예 |
| `completion` | 워크플로 전체의 완료 조건 — 모든 Task가 완료·검증되고 병합이 성립하는 조건. | 예 |

- **필수 표기(정본 보존).** 5필드 중 4필드(`goal`·`tasks`·`parallelSets`·`completion`)는 **예**, 1필드(`dependencies`)는 **아니오(없으면 전부 독립)**다. 필수/선택 표기와 그 괄호 단서를 정본 그대로 유지한다 — 표기 누락은 계약 변경으로 읽히므로 보존이 필수다.
- **병렬 집합 도출 문면(정본 보존 — 07 §3.2-A 말미).** 병렬 집합은 의존 관계에서 도출된다. 선행 의존이 없는 Task들, 또는 공통 선행이 모두 완료된 Task들이 하나의 병렬 집합을 이룬다. 이 도출 규정의 정본은 07 §3.2-A 말미이며, 본 문서는 그 문면을 인스턴스로 보존할 뿐 도출 규칙을 재정의하지 않는다.
- 필드의 상세 정본은 07 §3.2-A가 유지한다. 본 표는 그 스키마를 인스턴스화할 뿐 계약을 재정의하지 않는다.

---

## §3. Task 포맷 인스턴스 (정본: 07 §3.2-B)

Task는 분해의 최소 단위다. 각 Task는 다음을 반드시 가진다 — 없으면 디스패치되지 않는다(07 INV-1). 아래 필드·의미·필수 표기는 07 §3.2-B 정본을 **그대로 보존**한다(재정의 0, 새 필드 0).

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Task 고유 식별자. 의존·병렬 집합·핸들이 이 id로 참조한다. | 예 |
| `task` | 작업 요약. | 예 |
| `done` | 완료 조건 — 검증 가능한 형태 (ROADMAP v0.7 완료 조건). | 예 |
| `interfaceContract` | 인터페이스 계약 — 이 Task가 제공(produces)하고 소비(consumes)하는 확정된 계약. 다른 Task는 이 계약만 참조할 수 있다. | 예 |
| `ownedBoundary` | 소유 경계 — 이 Task가 배타적으로 소유하는 파일·계약 집합. 같은 병렬 집합의 다른 Task와 겹치지 않는다 (07 INV-2). | 예 |
| `dependsOn` | 선행 Task id 목록. 모두 완료·검증되어야 디스패치된다. | 아니오(기본 없음) |
| `delegation` | 이 Task를 디스패치할 때 사용하는 위임 메시지(02 §3.2-B) 매핑. | 예 |

- **필수 표기(정본 보존).** 7필드 중 6필드(`id`·`task`·`done`·`interfaceContract`·`ownedBoundary`·`delegation`)는 **예**, 1필드(`dependsOn`)는 **아니오(기본 없음)**다. 필수/선택 표기와 그 괄호 단서를 정본 그대로 유지한다.
- **`done`·`interfaceContract`의 ROADMAP v0.7 완료 조건 대응(정본 보존 — 07 §3.2-B 말미).** `done`과 `interfaceContract`는 ROADMAP v0.7의 "작업 분해 결과에 완료 조건과 인터페이스 계약이 포함된다" 완료 조건을 충족한다. 이 대응 관계의 정본은 07 §3.2-B 말미이며, 본 문서는 그 문면을 인스턴스로 보존할 뿐 완료 조건을 재정의하지 않는다.
- **`delegation` 필드 — 02 §3.2-B 인용(재정의 0, 07 INV-3).** `delegation`의 의미 셀은 위임 메시지의 정본을 **02 §3.2-B로 § 포인터 인용**한다. 위임 메시지의 필드(from·to·task·input·output·done·context·constraints)는 02 §3.2-B가 소유하며, 본 문서는 이를 재정의·재서술하지 않는다(07 INV-3 — Workflow는 위임 메시지·역할 경계 포맷을 재정의하지 않고 인용한다). Task 포맷은 각 Task가 디스패치 시 이 위임 메시지 매핑을 갖는다는 사실만 규정하고, 그 필드 정본은 02가 유지한다.
- 필드의 상세 정본은 07 §3.2-B가 유지한다. 본 표는 그 스키마를 인스턴스화할 뿐 계약을 재정의하지 않는다.

---

## §4. 공통 Failure Report 포맷 인스턴스 (정본: 07 §3.2-E)

Failure Report는 모든 Workflow 연산의 공통 실패 보고 구조다(07 §3.2-E). 아래 필드·의미는 07 §3.2-E 정본을 **그대로 보존**한다(재정의 0, 새 필드 0). 정본 표는 필수 열을 두지 않으므로 본 인스턴스도 두지 않는다(정본 구조 보존).

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Decompose / Dispatch / Merge). |
| `target` | 대상 (Work Graph, Task id, 병렬 집합, 충돌 항목). |
| `reason` | 사유 코드 (MissingCompletionCriteria / MissingInterfaceContract / OwnershipOverlap / DependencyCycle / IncompleteDelegation / UnmetDependency / UnverifiedResult / CrossReferenceMismatch / UnresolvedConflict). |
| `location` | 실패 지점 참조 (Task id, 경계 항목, 참조 위치). |

**`reason` 열거 9종(정본 07 §3.2-E 그대로 보존).** 공통 Failure Report의 `reason`은 다음 9종 사유 코드다. 정본 열거를 그대로 보존한다(재정의 0, 추가 0, 순서 정본 유지):

1. `MissingCompletionCriteria`
2. `MissingInterfaceContract`
3. `OwnershipOverlap`
4. `DependencyCycle`
5. `IncompleteDelegation`
6. `UnmetDependency`
7. `UnverifiedResult`
8. `CrossReferenceMismatch`
9. `UnresolvedConflict`

**이 문서의 Failure Report 포맷 인스턴스 소유 선언.** 이 문서가 공통 Failure Report 포맷(07 §3.2-E)의 **인스턴스 소유 문서**다. 각 연산(분해·디스패치·병합)의 규칙 인스턴스 문서(별도 소관 — 07 §3.1 연산 규칙의 인스턴스)는 실패 보고를 낼 때 이 포맷을 **§ 포인터로 참조**한다. 각 `reason` 코드를 어느 연산이 언제 산출하는가(연산별 완료 조건과 실패 보고의 결합)는 **07 §3.1 연산 규칙과 그 규칙 인스턴스 문서 소관**이며, 본 문서는 포맷의 `reason` 열거만 소유·보존하고 그 결합 규칙을 전개하지 않는다(포맷만 소유). 필드의 상세 정본은 07 §3.2-E가 유지한다.

---

## §5. 경계와 비의존 (직렬화·물리 위치 · 재정의 0 · 07 R2 · 금지 토큰 · Glossary)

본 문서가 준수하는 경계를 한자리에 모은다. 검증 대조 지점이다.

**직렬화·물리 위치 경계 (Adapter Binding 소관 포인터):**

- 세 포맷(Work Graph·Task·공통 Failure Report)의 **직렬화 형식·물리 위치·물리 경로**는 이 문서가 **일절 확정하지 않는다.** Core Contract(07 §3.2)는 추상 스키마이며, 직렬화 형식(파일 형태·문법)은 Adapter Binding이 정한다(07 §3.2 도입, §4.1 직렬화 행).
- 세 포맷의 물리 실현은 전부 **Adapter Binding 문서 소관**이다(07 §4.1 직렬화 행·§4.2 이식 교체 지점). 이식 시 §2~§4의 필드·필수 표기·`reason` 열거는 유지되고 물리 실현만 교체된다(07 §4.2). 필요한 자리에는 "Adapter Binding 문서 소관" 포인터만 둔다.

**재정의 0 · 인스턴스화 대상 경계:**

- **07 계약 재정의·확장 0.** §2~§4의 모든 필드·의미·필수/선택 표기·`reason` 열거는 07 §3.2-A/B/E의 인스턴스이며 § 포인터로만 참조한다. 스키마 표는 정본을 그대로 보존한다(재정의 0, 새 필드·새 사유 코드 0). 진위 판정 기준은 정본 07 §3.2-A/B/E가 유지한다. 위반이 발견되면 구현하지 않고 Advisor에게 보고한다.
- **인스턴스화 대상 경계.** 본 문서의 인스턴스화 대상은 세 정의 포맷(07 §3.2-A Work Graph·§3.2-B Task·§3.2-E 공통 Failure Report)과 그에 부속된 두 문면(병렬 집합 도출 — 07 §3.2-A 말미, `done`·`interfaceContract`의 ROADMAP v0.7 대응 — 07 §3.2-B 말미)이다.
- **Merge Result(07 §3.2-D) 비소관.** Merge Result는 이 파일 소관이 아니다 — **07 §3.2-D 소관 별도 인스턴스 문서(병합 규칙) 소관**이다. 본 문서는 그 내용(수합·상호 참조 정합성·충돌 목록·중재 결과 등)을 추측·인용하지 않으며 일반 포인터만 둔다.
- **연산 규칙(07 §3.1) 비소관.** 분해·디스패치·병합 연산 규칙의 전개(연산별 입력·출력·완료 조건·실패 보고 결합)도 이 파일 소관이 아니다 — **포맷만 소유한다.** 연산 규칙과 그 인스턴스 문서는 본 Failure Report 포맷을 § 포인터로 참조한다(§4).
- **위임 계약 불침범.** `delegation` 필드는 02 §3.2-B 위임 메시지를 § 포인터로만 인용한다(07 INV-3). 위임 메시지·역할 경계 포맷은 02 소유이며 본 문서는 재정의하지 않는다(§3).

**동시·후속 작성 경계 (07 R2·INV-4):**

- 같은 Wave(v0.7)에서 후속·동시 작성 중인 형제 산출물(병합 규칙 인스턴스·연산 규칙 인스턴스 등)의 미완성 내용은 인용·추측하지 않는다. 확정된 정본(07·02·structure.md·Glossary)과 기존 Baseline 문서만 참조한다(07 R2·INV-4). Merge Result·연산 규칙 결합은 "07 §3.2-D / §3.1 소관 별도 인스턴스 문서" 수준의 일반 포인터로만 지시한다.

**금지 토큰 비의존(structure.md §5 C-3 확장, 07 INV-9):**

- 본 문서 본문에는 특정 AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로·확장자 토큰을 두지 않는다. 금지 토큰의 예시조차 본문에 나열하지 않는다 — 구체 인스턴스가 필요한 자리에는 "Adapter Binding 문서 소관(07 §4.1·§4.2)" 포인터만 둔다(mention/use 경계).
- 다음은 금지 토큰이 아니다: **(i)** Failure Report 필드 값의 열거 명칭 — `operation` 값(Decompose / Dispatch / Merge) 및 `reason` 9종(MissingCompletionCriteria 등) — 07 §3.2-E 정본의 평이한 열거 값; **(ii)** Glossary·AGENT.md 정본 어휘 — Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약(Glossary §3.2-J J-07 표제어)과 역할 명칭(Advisor / Planner / Worker / Verifier); **(iii)** 저장소 문서 식별자(`specs/…`·`framework/…`·`docs/…` 상호 참조 및 본 문서 자신의 식별자 `framework/workflow/work-graph.md`) — 문서 식별자이며 직렬화 형식·물리 경로 토큰이 아니다(structure.md §5·loop-state-record §7·verification-report §7 분류 선례 동형).
- **자가 전수 스캔.** 위 후보 부류 전체(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로·확장자·특정 Adapter Binding 문서명)로 본문을 **부류별 전수 대조**하여 0건임을 확인했다(단일 토큰 검색 하나로 넓은 결론을 내지 않고, 후보 부류별 전수 대조). 직렬화 형식·물리 위치가 필요한 자리는 전부 "Adapter Binding 문서 소관(07 §4.1·§4.2)" 포인터로 대체했다.

**Glossary 정본:**

- 사용 용어는 전부 specs/00-glossary.md §3.2-J(J-07: Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약) 정본이다. 새 용어를 신설하지 않는다. "공통 Failure Report·`reason` 사유 코드·병렬 디스패치" 등은 07 §3.2 정본이 정의한 포맷·필드·서술 명칭이며 본 문서 신설 용어가 아니다.

---

## §6. 요약 (규격 한눈에 보기)

- **Work Graph(§2)** — 5필드(`goal`/`tasks`/`dependencies`/`parallelSets`/`completion`). 07 §3.2-A 스키마 인스턴스, 필수 표기(4 예·1 아니오 — `dependencies`가 아니오, 괄호 단서 보존) 정본 보존. 병렬 집합 도출 문면(07 §3.2-A 말미) 보존.
- **Task(§3)** — 7필드(`id`/`task`/`done`/`interfaceContract`/`ownedBoundary`/`dependsOn`/`delegation`). 07 §3.2-B 인스턴스, 필수 표기(6 예·1 아니오 — `dependsOn`이 아니오, 괄호 단서 보존) 정본 보존. `done`·`interfaceContract`의 ROADMAP v0.7 대응(07 §3.2-B 말미) 보존, `delegation`은 02 §3.2-B 인용(07 INV-3, 재정의 0).
- **공통 Failure Report(§4)** — 4필드(`operation`/`target`/`reason`/`location`), `reason` 9종. 07 §3.2-E 인스턴스(정본 필수 열 부재 구조 보존). 이 문서가 포맷 인스턴스 소유 문서 — 연산 규칙 인스턴스 문서(07 §3.1 소관)가 § 포인터로 참조. `reason`↔연산 결합 규칙은 07 §3.1 소관(포맷만 소유).
- **경계(§5)** — 직렬화 형식·물리 위치·물리 경로 비서술(Adapter Binding 소관, 07 §4.1·§4.2). Merge Result(07 §3.2-D)·연산 규칙(07 §3.1) 비소관(포맷만 소유). 07 재정의 0, 07 R2 경계, 금지 토큰 0(자가 전수 스캔), Glossary §3.2-J J-07 정본만 사용.
- 모든 스키마는 07 §3.2의 인스턴스이며, 물리 실현은 Adapter Binding 소관이다. 형태 A(문서) → 형태 B(실행 코드) 전환에도 Core Contract 변경은 0이다.
