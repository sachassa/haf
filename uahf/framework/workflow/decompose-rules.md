# framework/workflow/decompose-rules — 분해(Decompose) 연산 규칙 인스턴스

작성일: 2026-07-06
상태: v0.7 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/07-workflow.md §3.1-A — Decompose(분해) 연산의 정본(입력: 큰 작업 1건 — 목표와 범위 / 출력: Work Graph 1건 / 완료 조건 3건 / 실패 보고 reason 4종). 본 문서가 인스턴스화하는 연산 계약이다. 입력·출력·완료 조건·실패 reason의 진위 판정 기준은 이 §가 유지한다.
- specs/07-workflow.md §3.2-A 말미 — 병렬 집합 도출 문면("병렬 집합은 의존 관계에서 도출된다…")의 정본. 본 문서 §4가 인스턴스화한다(문면 보존 + 검사 가능 전개).
- specs/07-workflow.md §3.3 INV-1(계약 강제)·INV-2(간섭 금지) — 완료 조건 검사가 준수·대조하는 불변. 본 문서 §3이 예/아니오 검사 규칙으로 전개한다(재정의 0).
- specs/07-workflow.md §3.2-E — 공통 Failure Report 4필드·reason 9종 열거의 정본. 본 문서는 그중 Decompose 4종 reason만 완료 조건에 결합하며, 포맷 자체는 framework/workflow/work-graph.md §4를 § 포인터로 소비한다(재게재·재정의 0).
- specs/07-workflow.md §6 — 실패 모드 표(Decompose 행 — 검사 실패↔reason↔재분해 대응). 본 문서 §3 검사 실패 처리의 대조 지점.
- specs/07-workflow.md §3.1-B(Dispatch)·§3.1-C(Merge) — **이 파일 소관이 아니다.** 각 연산 규칙의 인스턴스는 별도 소관 문서가 담당한다. 본 문서는 그 내용을 추측·인용하지 않고 일반 포인터만 둔다(07 R2, §0·§6).
- specs/07-workflow.md §4.1·§4.2 — Adapter Binding(Work Graph 직렬화 행·이식 교체 지점). 분해 수행 주체의 물리 채널·직렬화 형식·물리 위치의 소관 포인터(본 문서 §3·§6).
- framework/workflow/work-graph.md §2·§3·§4 — **WF1 확정본**(Advisor 게이트 C 검토 통과). Work Graph(§2)·Task(§3)·공통 Failure Report(§4) 포맷의 인스턴스 소유 문서다. 본 문서가 검사 규칙에서 참조하는 필드·reason 열거의 **확정 인터페이스**이며, 필드 표는 § 포인터로만 소비한다(정본은 07 §3.2-A/B/E가 유지).
- specs/02-agent.md §3.2-B — 위임 메시지(Delegation Message)의 정본. 분해가 산출한 Task의 `delegation` 필드가 § 포인터로만 인용한다(07 INV-3). 본 문서는 재정의하지 않는다.
- specs/00-glossary.md §3.2-J(J-07) — Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- framework/core/structure.md §2·§5 — 본 파일의 소속 경계(Module 구현 디렉터리 `framework/workflow/`), 금지 토큰 규칙(확정 조건 C-3 확장 — 문서 본문 비의존). §0 정본 경계 관례.
- framework/verifier/verifier-protocol.md §2 — 연산을 운용 절차(예/아니오 판정 규칙)로 전개하고 절차↔정본 § 1:1 대응표를 두되 진위 판정 기준은 정본 §에 두는 관례 표본.
- framework/loop/loop-protocol.md — 문서 머리 구조·§0 정본 경계·§9 이력 절 머리 배치·§ 포인터 표기·말미 요약 절 관례 표본.
- AGENT.md — 상위 규약.

거버넌스: 이 문서는 `framework/workflow/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 특정 AI·언어·툴체인·직렬화 형식·물리 경로 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장, 07 §3.3 INV-9). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.7 Draft | 최초 작성. Decompose 연산(07 §3.1-A)의 입력·출력·완료 조건 3건·실패 reason 4종을 인터페이스 인스턴스로 정본 그대로 보존(§2, 재정의·확장 0). 완료 조건 3건을 예/아니오 판정 가능한 검사 규칙 4개(C1 완료 조건 보유→`MissingCompletionCriteria` · C2 인터페이스 계약 보유→`MissingInterfaceContract` · C3 소유 경계 비중첩→`OwnershipOverlap` · C4 의존 비순환→`DependencyCycle`)로 전개하고, 각 검사 실패를 해당 reason 코드에 1:1 결합(§3, verifier-protocol §2 관례 동형 — 검사 규칙↔완료 조건·불변·reason 대응표 + 각 검사 예/아니오 절차·검사 범위). 병렬 집합 도출 문면(07 §3.2-A 말미) 보존 + 검사 가능 전개(D1 상호 비의존·D2 경계 비중첩, 새 reason 신설 0 — §4). Work Graph·Task·공통 Failure Report 포맷은 work-graph.md §2·§3·§4를 § 포인터로만 소비(필드 표 재게재·재정의 0, 이중 갱신 방지 — §5). Dispatch(07 §3.1-B)·Merge(07 §3.1-C)는 비소관(별도 인스턴스 문서 소관, 동시 작성 형제 불인용 — 07 R2), 물리 실현(분해 수행 주체 물리 채널·직렬화·물리 위치)은 Adapter Binding 소관 포인터. 07·02 계약 재정의 0, Glossary 밖 새 용어 0, 금지 토큰 0(자가 전수 스캔 — §6). | Worker (Advisor 위임, Task WF3) |
| 2026-07-06 | v0.7 Baseline | v0.7 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/07-workflow.md §3.1-A다.** 이 문서는 그 Decompose 연산 계약의 **인스턴스**이며, 연산·완료 조건·실패 reason을 재정의·확장하지 않는다. 계약 요소는 07의 해당 §를 § 포인터로 참조한다(framework/core/structure.md §7 확정 조건 C-1 정합 — 인스턴스는 계약 변경이 아니다; verifier-protocol.md §0·loop-protocol.md §0과 동형).
- 이 문서는 `framework/workflow/` 아래 **Decompose 연산의 규칙(운용 절차)**을 확정한다. 07 §3.1-A 연산의 완료 조건 3건을 이 프로젝트의 **예/아니오 판정 가능한 검사 규칙**으로 전개하되, 각 검사의 진위 판정 기준은 대응 정본 07 §(그리고 그 검사가 대조하는 포맷 필드의 정본 07 §3.2-A/B)가 유지한다(verifier-protocol.md §2.1 프로토콜 단계 표 관례 동형).
- **소비하는 포맷의 확정 인터페이스는 framework/workflow/work-graph.md(WF1 확정본)이다.** 검사 규칙이 참조하는 Work Graph 5필드·Task 7필드·공통 Failure Report 4필드와 reason 열거는 그 문서 §2·§3·§4의 스키마를 **§ 포인터로만 소비**한다. 필드 표를 재게재·중복 정의하지 않는다(이중 갱신 방지 — work-graph.md §4 인스턴스 소유 경계 관례 동형). 포맷 필드·reason 열거의 진위 판정 기준은 정본 07 §3.2-A/B/E가, 확정 인터페이스 인스턴스는 work-graph.md가 유지한다.
- **reason↔연산 결합의 소관이 본 문서다.** work-graph.md §4는 "각 `reason` 코드를 어느 연산이 언제 산출하는가(연산별 완료 조건과 실패 보고의 결합)는 07 §3.1과 그 규칙 인스턴스 문서 소관"이라 명시하고 포맷의 reason 열거만 소유한다. 본 문서가 바로 **Decompose 연산에 대한 그 규칙 인스턴스 문서**이며, Decompose 4종 reason(`MissingCompletionCriteria`·`MissingInterfaceContract`·`OwnershipOverlap`·`DependencyCycle`)이 어느 완료 조건 검사에서 언제 산출되는가만 결합·소유한다. reason 열거의 소유·포맷은 work-graph.md §4가 유지한다(본 문서는 4종을 값으로 인용할 뿐 새 코드를 신설하지 않는다).
- **소관 밖 경계.** Dispatch 연산(07 §3.1-B)·Merge 연산(07 §3.1-C)의 규칙은 이 파일 소관이 아니다 — 각각 07 §3.1-B·§3.1-C 소관 별도 인스턴스 문서 소관이며, 본 문서는 그 내용을 추측·인용하지 않고 일반 포인터만 둔다(07 R2). 분해가 산출한 Task를 실제로 디스패치하는 규칙은 Dispatch 소관이다.
- **위임 계약 불침범.** 분해가 산출한 Task의 `delegation` 필드는 02 §3.2-B 위임 메시지를 § 포인터로만 인용한다(07 INV-3). 위임 메시지·역할 경계 포맷은 02 소유이며 본 문서는 재정의하지 않는다.
- **물리 실현 비서술(경계).** 분해를 **수행하는 주체의 물리 채널**, 산출된 Work Graph의 **직렬화 형식·물리 위치**, 검사 규칙의 **물리 실행 방식**은 이 문서가 서술하지 않는다. 이는 **Adapter Binding 문서 소관**이다(07 §4.1 Work Graph 직렬화 행·§4.2 이식 교체 지점). 필요한 자리에는 "Adapter Binding 문서 소관" 포인터만 둔다.
- **07 내부 § 포인터·INV 참조 표기 관례.** 07 정본 요소를 가리킬 때 07의 내부 § 포인터·INV 참조는 `07 §…`·`07 INV-…` 접두로 명시하여 본 문서 자신의 절 번호와 구분한다. 이는 대상 지시를 명료화하는 표기이며 정본 내용(완료 조건·reason·필드)을 변경하지 않는다(work-graph.md §0·verifier-protocol.md §0의 표기 관례와 동형).
- 용어는 specs/00-glossary.md 정본(§3.2-J J-07)만 사용한다. 새 용어를 신설하지 않는다. "Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약"은 J-07 표제어이며, "Decompose·공통 Failure Report·reason 사유 코드"는 07 §3 정본이 정의한 연산·포맷·필드 명칭이지 본 문서 신설 용어가 아니다. 검사 라벨 C1~C4·D1~D2는 본 문서 서술 편의의 명명 규칙이며 계약 용어가 아니다.

---

## §1. 목적

`framework/workflow/`의 이 규격은 **Decompose 연산(07 §3.1-A)을 어떤 규칙으로 판정하는가**를 확정한다.

이 규격의 책임은 세 가지다.

- **연산 인터페이스 인스턴스** — Decompose 연산의 입력·출력·완료 조건 3건·실패 reason 4종을 07 §3.1-A 정본과 일치하게 옮긴 인스턴스로 전개한다(§2).
- **완료 조건 검사 규칙** — 완료 조건 3건을 각각 **예/아니오로 판정 가능한 검사 규칙**(C1~C4)으로 전개하고, 각 검사 실패를 해당 실패 reason 코드에 1:1 결합한다(§3, verifier-protocol §2 관례 동형).
- **병렬 집합 도출 규칙** — 07 §3.2-A 말미의 병렬 집합 도출 문면을 보존하고, 검사 가능한 운용 규칙(상호 비의존·경계 비중첩)으로 전개한다(§4).

이 규격은 07 §3.1-A Decompose 연산 계약의 **인스턴스**다. 연산·완료 조건·실패 reason을 재정의·확장하지 않는다. 형태 A(문서)에서 형태 B(실행 코드)로 전환되어도 07 §3 Core Contract 변경은 0이며, 위반(형태 B가 07 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다(structure.md §7 C-1과 같은 불변 원칙).

이 규격의 규칙은 이 프로젝트의 spec 병렬 작성 Wave가 이미 실증한 분해와 동형이다 — 07 §8 예1(00/01/02를 선행 Task로, 03~13을 병렬 Task로 분해)이 아래 검사 규칙(완료 조건 보유·경계 비중첩·비순환)을 실제로 밟은 분해다. 본 문서는 그 사례를 재정의하지 않고 규칙의 실증 근거로만 가리킨다.

---

## §2. Decompose 연산 인터페이스 인스턴스 (정본: 07 §3.1-A)

Decompose는 큰 작업 하나를 Work Graph 하나로 분해하는 연산이다(07 §3.1-A). 아래는 그 연산의 입력·출력·완료 조건·실패를 07 §3.1-A 정본과 일치하게 옮긴 인스턴스이며, 진위 판정 기준은 07 §3.1-A가 유지한다(§0). 본 절은 계약을 재정의하지 않는다.

| 요소 | 값 (정본: 07 §3.1-A) |
|---|---|
| **입력** | 큰 작업 1건 — 목표와 범위. |
| **출력** | Work Graph 1건. 포맷(5필드)의 정본은 07 §3.2-A이며 확정 인터페이스 인스턴스는 work-graph.md §2다 — 본 문서는 § 포인터로만 소비한다(§5). |
| **완료 조건** | (1) 모든 Task가 완료 조건(`done`)과 인터페이스 계약(`interfaceContract`)을 가진다 (07 INV-1). (2) 각 병렬 집합 내 Task들의 소유 경계(`ownedBoundary`)가 서로 겹치지 않는다 (07 INV-2). (3) 의존 관계에 순환이 없다. |
| **실패 보고** | reason = `MissingCompletionCriteria` \| `MissingInterfaceContract` \| `OwnershipOverlap` \| `DependencyCycle`. 공통 Failure Report 포맷(4필드)의 정본은 07 §3.2-E이며 확정 인터페이스 인스턴스는 work-graph.md §4다 — 본 문서는 § 포인터로만 소비한다(§5). |

- **완료 조건·실패 reason 정본 보존.** 완료 조건 3건과 실패 reason 4종은 07 §3.1-A를 **그대로 보존**한다(재정의 0, 새 조건·새 reason 0). 완료 조건 3건 → 검사 규칙 4개 → reason 4종의 대응은 §3이 전개한다.
- **완료 조건 성립 = 검사 전부 통과.** Decompose가 완료로 성립하려면 §3의 검사 C1~C4가 모두 "예"여야 한다. 하나라도 "아니오"이면 Decompose 실패이며 해당 검사의 reason으로 공통 Failure Report를 낸다(§3). 완료 조건 (1)이 두 요소(완료 조건·인터페이스 계약)를 요구하고 07 §3.2-E가 그 각각에 별도 reason을 두므로, 완료 조건 (1)은 검사 C1·C2 두 개로 분기한다(재정의가 아니라 정본의 두 요소·두 reason을 검사로 분해).
- 입력·출력·완료 조건·실패의 상세 정본은 07 §3.1-A가 유지한다. 본 표는 그 연산을 인스턴스화할 뿐 계약을 재정의하지 않는다.

---

## §3. 완료 조건 검사 규칙 ↔ reason 결합 (done 대상 — 예/아니오 판정 규칙)

완료 조건 3건(07 §3.1-A)을 각각 **예/아니오로 판정 가능한 검사 규칙**으로 전개한다. 각 검사는 산출된 Work Graph를 대상으로 하며, 판정 대상 필드의 정본은 07 §3.2-A/B(확정 인터페이스 인스턴스 work-graph.md §2·§3)이고, 검사 실패 시 산출하는 공통 Failure Report 포맷·reason 열거의 정본은 07 §3.2-E(확정 인터페이스 인스턴스 work-graph.md §4)다. 본 절은 그 필드·포맷을 재정의하지 않고 § 포인터로 소비하며, **어느 검사 실패가 어느 reason을 산출하는가의 결합만 소유**한다(§0).

### §3.1 검사 규칙 ↔ 완료 조건·불변·reason 1:1 대응표 (done 대상 — 1:1 대응)

| 검사 | 판정 형태 (예/아니오) | 대응 완료 조건 (07 §3.1-A) · 불변 | 판정 대상 필드 (정본 § / 확정 인터페이스) | 검사 실패(= 아니오) 시 reason (소유: work-graph.md §4 / 정본 07 §3.2-E) |
|---|---|---|---|---|
| **C1. 완료 조건 보유** | Work Graph의 모든 Task가 `done`을 가지는가? | 완료 조건 (1) · 07 INV-1 | Task `done` (07 §3.2-B / work-graph.md §3) | `MissingCompletionCriteria` |
| **C2. 인터페이스 계약 보유** | Work Graph의 모든 Task가 `interfaceContract`를 가지는가? | 완료 조건 (1) · 07 INV-1 | Task `interfaceContract` (07 §3.2-B / work-graph.md §3) | `MissingInterfaceContract` |
| **C3. 소유 경계 비중첩** | 각 병렬 집합 내 모든 Task 쌍의 `ownedBoundary` 교집합이 0인가? | 완료 조건 (2) · 07 INV-2 | Task `ownedBoundary` · Work Graph `parallelSets` (07 §3.2-A/B / work-graph.md §2·§3) | `OwnershipOverlap` |
| **C4. 의존 비순환** | `dependencies`를 방향 그래프로 볼 때 방향 순환이 없는가? | 완료 조건 (3) | Work Graph `dependencies` (07 §3.2-A / work-graph.md §2) | `DependencyCycle` |

- 이 표가 done의 "INV-1·INV-2 검사·순환 검출이 각각 예/아니오 판정 가능한 검사 규칙으로 전개되고 각 검사 실패가 해당 reason 코드로 연결된다"의 대조 지점이다(verifier-protocol §2.1 관례 동형). 각 검사 상세는 §3.2~§3.5다.
- **판정 결합 소유 경계.** 위 표의 마지막 두 열(판정 대상 필드·reason)에서, 필드 스키마와 reason 열거의 **소유·정본**은 07 §3.2-A/B/E와 work-graph.md §2·§3·§4에 있다. 본 표가 소유하는 것은 **검사↔완료 조건↔reason의 결합**이며, 이는 work-graph.md §4가 "규칙 인스턴스 문서 소관"으로 이연한 지점의 Decompose 몫이다(§0).
- **결정성.** 각 검사는 동일 Work Graph에 대해 동일한 "예/아니오"를 낸다 — 재량 개입이 없다. 이는 검사가 예/아니오 판정 규칙이라는 사실의 귀결이며, 도출 규칙의 결정성이지 검사 도구·실행 환경의 물리 결정성이 아니다(물리 실행은 Adapter Binding 소관, §6).
- **다중 실패 처리.** 한 Work Graph에서 둘 이상의 검사가 "아니오"일 수 있다. 이 경우 각 실패 지점마다 공통 Failure Report 1건씩을 산출하며, `location` 필드(work-graph.md §4)에 실패 지점(Task `id`·경계 항목·참조 위치)을 담는다. reason별 `location`의 지시 대상은 각 검사 상세(§3.2~§3.5)가 규정한다.

### §3.2 C1 — 완료 조건 보유 검사 (→ `MissingCompletionCriteria`)

1. **대상.** Work Graph의 `tasks` 전체(07 §3.2-A `tasks` — 분해된 하위 작업 전부, work-graph.md §2).
2. **절차(예/아니오).** 각 Task `t`에 대해, `t`가 `done`(완료 조건 — 검증 가능한 형태) 필드를 가지고 그 값이 비어 있지 않은가? — Task별 예/아니오.
3. **판정.** `tasks`의 모든 Task가 "예" → C1 = 예. 하나라도 "아니오"인 Task가 있으면 → C1 = 아니오.
4. **실패 결합.** C1 = 아니오이면 Decompose 실패. reason = `MissingCompletionCriteria`, `location` = `done`이 없는 Task의 `id`. 그 Work Graph는 디스패치되지 않는다(07 INV-1 — `done`·`interfaceContract` 중 하나라도 없으면 디스패치되지 않는다). 재분해로 누락 Task에 `done`을 부여한 뒤 재검사한다(07 §6 Decompose 행).
5. **검사 범위(정직).** `tasks` **전수**(모든 Task). 표본 Task 하나가 `done`을 가진다는 사실로 전체가 가진다는 결론을 내지 않는다(좁은 대리 지표 금지).

### §3.3 C2 — 인터페이스 계약 보유 검사 (→ `MissingInterfaceContract`)

1. **대상.** Work Graph의 `tasks` 전체(work-graph.md §2).
2. **절차(예/아니오).** 각 Task `t`에 대해, `t`가 `interfaceContract`(제공·소비하는 확정된 계약) 필드를 가지고 그 값이 비어 있지 않은가? — Task별 예/아니오.
3. **판정.** 모든 Task가 "예" → C2 = 예. 하나라도 "아니오" → C2 = 아니오.
4. **실패 결합.** C2 = 아니오이면 Decompose 실패. reason = `MissingInterfaceContract`, `location` = `interfaceContract`가 없는 Task의 `id`. 디스패치 차단(07 INV-1). 재분해로 누락 Task에 `interfaceContract`를 부여한 뒤 재검사(07 §6).
5. **검사 범위(정직).** `tasks` 전수. C1과 마찬가지로 표본 하나로 넓은 결론을 내지 않는다.

### §3.4 C3 — 소유 경계 비중첩 검사 (→ `OwnershipOverlap`)

1. **대상.** Work Graph의 `parallelSets` 각 병렬 집합 `P`와, `P`에 속한 Task들의 `ownedBoundary`(07 §3.2-A/B — work-graph.md §2·§3).
2. **절차(예/아니오).** 각 병렬 집합 `P`에 대해, `P`에 속한 서로 다른 Task 쌍 `(a, b)` **전부**에 대해 `ownedBoundary`(a) ∩ `ownedBoundary`(b) = 공집합인가? — 쌍별 예/아니오.
3. **판정.** 모든 병렬 집합의 모든 Task 쌍이 "예" → C3 = 예. 어느 한 쌍이라도 교집합이 공집합이 아니면 → C3 = 아니오.
4. **실패 결합.** C3 = 아니오이면 Decompose 실패. reason = `OwnershipOverlap`, `location` = 중첩된 경계 항목·해당 Task 쌍. 재분해로 경계를 분리한다(07 §6 — reason=OwnershipOverlap, 재분해로 경계 분리, 07 INV-2).
5. **검사 범위(정직).** 각 병렬 집합 내 **쌍별 전수**(모든 Task 쌍의 교집합). 대표 한 쌍만 검사하고 나머지를 통과로 간주하지 않는다 — 좁은 대리 지표 하나로 넓은 결론을 내면 경계 중첩을 놓친다(06 §8 예1이 규정한 "검사 범위 부족" 유형의 회피). 병렬 집합이 셋 이상의 Task를 가지면 교집합 검사는 모든 쌍에 대해 수행한다.

### §3.5 C4 — 의존 비순환 검사 (→ `DependencyCycle`)

1. **대상.** Work Graph의 `dependencies`(선행 Task id → 후행 Task id, 07 §3.2-A — work-graph.md §2).
2. **절차(예/아니오).** `dependencies`를 방향 그래프(선행 → 후행)로 볼 때, 어떤 Task에서 출발해 선행 관계를 따라가 자기 자신으로 되돌아오는 방향 순환이 존재하는가? 동치로: 모든 Task를 "선행이 후행보다 앞선다"는 조건으로 일렬로 세우는 순서가 존재하는가? — 그래프 전체에 대해 예/아니오.
3. **판정.** 방향 순환 없음(그런 순서가 존재) → C4 = 예. 방향 순환 존재(그런 순서가 존재하지 않음) → C4 = 아니오.
4. **실패 결합.** C4 = 아니오이면 Decompose 실패. reason = `DependencyCycle`, `location` = 순환에 포함된 Task 참조. 재분해로 순환을 끊은 뒤 재검사(07 §6 — reason=DependencyCycle).
5. **검사 범위(정직).** `dependencies` 관계 **전체**. 일부 경로만 보고 비순환으로 결론 내지 않는다.

### §3.6 검사 물리 실행 경계

- 위 C1~C4는 **예/아니오 판정 규칙**이다. 이 규칙을 **누가·어떤 물리 채널로 실행하는가**는 이 문서가 서술하지 않는다 — 분해 수행 주체의 물리 채널·검사 실행 방식은 Adapter Binding 문서 소관이다(07 §4.1·§4.2, §6).
- 검증 측면에서 이 검사들은 07 §7 검증 방법("Verifier가 Work Graph의 각 Task 필수 필드의 존재를 대조한다 / 병렬 집합 내 소유 경계의 쌍별 교집합이 0임을 확인한다")과 정합한다 — 본 문서는 그 판정 규칙을 확정하고, 판정 주체·시점·전이는 정의하지 않는다(06·03-loop 소관, 07 INV-8 경계 불가침).

---

## §4. 병렬 집합 도출 규칙 인스턴스 (정본: 07 §3.2-A 말미)

**도출 문면(정본 보존 — 07 §3.2-A 말미).** "병렬 집합은 의존 관계에서 도출된다. 선행 의존이 없는 Task들, 또는 공통 선행이 모두 완료된 Task들이 하나의 병렬 집합을 이룬다." 이 도출 규정의 정본은 07 §3.2-A 말미이며, 본 문서는 그 문면을 보존하고 검사 가능한 운용 규칙으로 전개할 뿐 도출 규칙을 재정의하지 않는다.

**검사 가능 전개.** 위 문면을 예/아니오 판정 가능한 도출·정합 규칙으로 옮긴다.

- **도출 자격(구성 규칙).** Task `t`가 하나의 병렬 집합에 들 자격을 가지는 조건은 둘 중 하나다 — (i) `t`에 선행 의존이 없다(`dependencies`에서 `t`로 들어오는 선행이 없다 — `dependsOn` 없음), 또는 (ii) `t`의 모든 선행이 완료·검증되었다(공통 선행이 모두 완료). 이 자격 규정은 07 §3.2-A 말미 문면의 두 경우를 그대로 옮긴 것이다.
- **정합 검사 D1 (상호 비의존, 예/아니오).** 같은 병렬 집합 `P`의 임의의 두 Task `a`, `b`에 대해, `dependencies`에 `a → b` 또는 `b → a`가 없는가? — 쌍별 예/아니오. 07 §3.2-A `parallelSets` 정의("같은 집합의 Task는 서로 의존하지 않고")를 검사로 옮긴 것이다.
- **정합 검사 D2 (경계 비중첩).** 07 §3.2-A `parallelSets` 정의("소유 경계가 겹치지 않는다")의 검사는 §3.4 C3와 동일하다. 병렬 집합이 정합하게 도출되면 C3가 통과한다.
- **정합 판정.** 하나의 병렬 집합이 정합하게 도출되었다는 것은 D1 = 예 그리고 D2(= C3) = 예임을 뜻한다. 두 정합 검사와 전체 그래프의 비순환(C4)이 함께 성립할 때, `parallelSets`는 07 §3.2-A 말미 문면대로 의존 관계에서 도출된 것이다.

**위반 처리와 reason 경계(재정의 0).**

- D1이 "아니오"(상호 의존하는 두 Task가 한 병렬 집합에 있음)이면 병렬 집합이 **잘못 도출된 것**이며, 재도출로 교정한다(의존하는 Task는 같은 집합에 두지 않는다 — 07 §3.2-A). 07 §3.1-A 실패 reason 4종은 이 상호 의존 자체를 위한 별도 코드를 두지 않으므로, 본 문서는 이를 위한 **새 reason을 신설하지 않는다**(정본 열거 보존). 상호 의존은 도출 규칙 위반으로서 재도출 대상이며, 그에 수반하는 소유 경계 중첩은 C3 → `OwnershipOverlap`으로, 의존 관계의 순환은 C4 → `DependencyCycle`로 각각 보고된다.
- 즉 병렬 집합 도출 규칙은 **올바른 도출을 위한 구성·정합 규칙**이고, 완료 조건 실패의 reason 산출은 §3의 C1~C4가 담당한다. 두 절은 층위가 다르며(도출 vs 완료 조건 판정) 모순 없이 접속한다.

**실증.** 이 도출 규칙은 07 §8 예1이 실증한다 — 00/01/02는 03~13의 공통 선행이므로 선행(직렬) Task로 두고, 03~13은 그 공통 선행이 모두 완료된 뒤 하나의 병렬 집합을 이룬다(도출 자격 (ii)). 각 병렬 Task의 소유 경계(자기 spec 파일 하나)가 겹치지 않아(D2 = C3) 병렬 집합이 정합하게 도출되었다. 본 문서는 그 사례를 재정의하지 않고 규칙의 실증으로 가리킨다.

---

## §5. 소비하는 정본 포맷 (§ 포인터 — 재게재 0)

본 문서의 검사 규칙(§3)과 도출 규칙(§4)이 참조하는 포맷은 전부 확정 인터페이스 work-graph.md(WF1 확정본)와 정본 07 §3.2가 소유한다. 본 문서는 필드 표를 **재게재·재정의하지 않고** § 포인터로만 소비한다(이중 갱신 방지).

| 소비 대상 포맷 | 확정 인터페이스 인스턴스 | 정본 § | 본 문서의 소비 지점 |
|---|---|---|---|
| Work Graph 포맷 (`goal`/`tasks`/`dependencies`/`parallelSets`/`completion`) | work-graph.md §2 | 07 §3.2-A | §2 출력, §3(C3·C4 판정 대상 — `parallelSets`·`dependencies`), §4 도출 |
| Task 포맷 (`id`/`task`/`done`/`interfaceContract`/`ownedBoundary`/`dependsOn`/`delegation`) | work-graph.md §3 | 07 §3.2-B | §3(C1·C2·C3 판정 대상 — `done`·`interfaceContract`·`ownedBoundary`), §4 도출 자격(`dependsOn`) |
| 공통 Failure Report 포맷 (`operation`/`target`/`reason`/`location`) + reason 9종 열거 | work-graph.md §4 | 07 §3.2-E | §3 실패 결합(Decompose 4종 reason 산출·`location` 지시) |

- **필드 표 비재게재.** 위 세 포맷의 필드 표(5필드·7필드·4필드)와 reason 9종 열거는 work-graph.md §2·§3·§4가 단일 소유한다. 본 문서는 검사·도출에 필요한 **필드명**을 § 포인터로 인용할 뿐, 필드 표를 다시 그리지 않는다.
- **reason 결합 소유는 본 문서.** 포맷의 reason 열거(9종) 소유는 work-graph.md §4이나, **Decompose 4종 reason이 어느 완료 조건 검사에서 산출되는가**의 결합은 본 문서 §3이 소유한다(§0 — work-graph.md §4가 규칙 인스턴스 문서로 이연한 지점). 본 문서는 4종을 값으로 인용할 뿐 새 reason 코드를 신설하지 않는다.
- **`delegation` 정본.** 분해가 산출한 각 Task의 `delegation` 매핑(위임 메시지)의 정본은 02 §3.2-B다(07 INV-3). 본 문서는 이를 재정의하지 않으며, `delegation`을 실제 디스패치에 사용하는 규칙은 Dispatch 연산(07 §3.1-B, 별도 인스턴스 문서 소관)이 소비한다.

---

## §6. 경계와 비의존 (재정의 0 · 07 R2 · 금지 토큰 · Glossary)

본 문서가 준수하는 경계를 한자리에 모은다. 검증 대조 지점이다.

- **07·02 계약 재정의·확장 0.** §2~§4의 모든 연산 인터페이스·검사 규칙·도출 규칙은 07 §3.1-A·§3.2-A의 인스턴스이며 § 포인터로만 참조한다. 완료 조건 3건·실패 reason 4종·병렬 집합 도출 문면은 정본을 그대로 보존했다(새 완료 조건·새 reason·새 도출 규칙 0). `delegation`의 위임 메시지 정본(02 §3.2-B)도 재정의하지 않았다(07 INV-3). 진위 판정 기준은 07 §3.1-A·§3.2-A/B/E와 02 §3.2-B가 유지한다. 위반(형태 B가 07·02 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다.
- **인스턴스화 대상 경계.** 본 문서의 인스턴스화 대상은 Decompose 연산(07 §3.1-A)과 병렬 집합 도출 문면(07 §3.2-A 말미)이다. **Dispatch(07 §3.1-B)·Merge(07 §3.1-C) 연산 규칙은 대상이 아니며**, 각각 07 §3.1-B·§3.1-C 소관 별도 인스턴스 문서 소관으로 일반 포인터만 두었다.
- **포맷 비재게재(이중 갱신 방지).** Work Graph·Task·공통 Failure Report 포맷은 work-graph.md §2·§3·§4를 § 포인터로만 소비했고 필드 표를 재게재·재정의하지 않았다(§5). reason 열거의 소유는 work-graph.md §4, Decompose reason↔검사 결합의 소유는 본 문서 §3이다.
- **07 R2 경계 — 동시 작성 형제 불인용.** 같은 Wave(v0.7)에서 동시 작성 중인 형제 산출물(Dispatch 프로토콜 인스턴스·Merge 규칙 인스턴스)의 미완성 내용은 인용·추측하지 않았다. 확정된 정본(07·02 spec, structure.md, Glossary)과 확정 인터페이스(work-graph.md WF1 확정본)만 참조했다. Dispatch·Merge는 "07 §3.1-B/§3.1-C 소관 별도 인스턴스 문서" 수준의 일반 포인터로만 지시했다.
- **물리 실현 비서술.** 분해를 수행하는 주체의 물리 채널, 산출된 Work Graph의 직렬화 형식·물리 위치, 검사 규칙의 물리 실행 방식은 서술하지 않고 **Adapter Binding 문서 소관**(07 §4.1 Work Graph 직렬화 행·§4.2 이식 교체 지점) 포인터로만 처리했다. 특정 Adapter Binding 문서명을 두지 않았으며, 필요한 자리에는 소관 포인터만 두었다.
- **금지 토큰 비의존(structure.md §5 C-3 확장, 07 INV-9) — 자가 전수 스캔 수행.** 본문 전체를 다음 후보 부류 **전체**로 전수 스캔하여 실증 0건임을 확인했다(단일 토큰 검색에 국한하지 않고 부류별 전수 대조) — { 특정 AI 이름·모델명·제품 기능명 } ∪ { 프로그래밍 언어명·툴체인명 } ∪ { 직렬화 형식명·확장자·OS 토큰 } ∪ { 물리 경로·Adapter 하위 인스턴스 토큰·특정 Adapter Binding 문서명 }. 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관(07 §4.1·§4.2)" 포인터를 두었다 — 금지 토큰의 예시조차 본문에 나열하지 않았다(mention/use 경계). 다음은 금지 토큰이 아니다: (i) 연산명(Decompose/Dispatch/Merge)·reason 열거 값(`MissingCompletionCriteria`·`MissingInterfaceContract`·`OwnershipOverlap`·`DependencyCycle` 및 07 §3.2-E의 나머지 reason 명칭) — 07 §3 정본의 평이한 열거 값; (ii) Glossary·AGENT.md 정본 어휘 — Work Graph·Task·병렬 집합·소유 경계·인터페이스 계약(Glossary §3.2-J J-07)과 역할 명칭(Advisor/Planner/Worker/Verifier); (iii) 계약 필드명 백틱 표기(`goal`·`tasks`·`dependencies`·`parallelSets`·`done`·`interfaceContract`·`ownedBoundary`·`dependsOn`·`delegation`·`operation`·`target`·`reason`·`location` — 07 §3.2 정본 어휘); (iv) 저장소 문서 식별자(`specs/…`·`framework/…`·`docs/…` 상호 참조 및 본 문서 자신의 식별자 `framework/workflow/decompose-rules.md`) — 문서 식별자이며 직렬화 형식·물리 경로 토큰이 아니다(work-graph.md §5·loop-protocol.md §7 분류 선례 동형). 검사·도출 라벨(C1~C4·D1~D2)은 본 문서 서술 편의의 명명 규칙이며 계약 용어·금지 토큰이 아니다.
- **Glossary 정본.** 사용 용어는 전부 specs/00-glossary.md §3.2-J(J-07) 정본 또는 Glossary 기존 어휘이거나 평이한 열거 값이다. 새 용어를 신설하지 않았다. "Decompose·공통 Failure Report·reason 사유 코드·병렬 집합 도출"은 07 §3 정본이 정의한 연산·포맷·서술 명칭이며 본 문서 신설 용어가 아니다.

---

## §7. 요약 (규격 한눈에 보기)

- 이 문서 = **Decompose 연산(07 §3.1-A)의 규칙 인스턴스**. 정본 = 07 §3.1-A(본 문서는 인스턴스, 재정의 아님 — C-1). 소비하는 포맷의 확정 인터페이스 = work-graph.md(WF1 확정본) §2·§3·§4.
- **연산 인터페이스(§2)** — 입력=큰 작업 1건(목표·범위), 출력=Work Graph 1건, 완료 조건 3건(모든 Task가 `done`·`interfaceContract` 보유 / 병렬 집합 내 소유 경계 비중첩 / 의존 비순환), 실패 reason 4종(`MissingCompletionCriteria`·`MissingInterfaceContract`·`OwnershipOverlap`·`DependencyCycle`). 정본 그대로 보존.
- **검사 규칙(§3)** — 완료 조건 3건 → 예/아니오 검사 4개. C1 완료 조건 보유→`MissingCompletionCriteria`, C2 인터페이스 계약 보유→`MissingInterfaceContract`(완료 조건 (1)이 두 요소·두 reason으로 분기), C3 소유 경계 쌍별 전수 비중첩→`OwnershipOverlap`, C4 의존 방향 비순환→`DependencyCycle`. Decompose 성립 = C1∧C2∧C3∧C4 전부 예. 각 검사는 전수 범위·결정적 판정. reason↔검사 결합이 본 문서 소유(work-graph.md §4가 이연한 지점).
- **병렬 집합 도출 규칙(§4)** — 07 §3.2-A 말미 문면 보존 + 검사 가능 전개(도출 자격 (i)·(ii), 정합 검사 D1 상호 비의존·D2 경계 비중첩=C3). 상호 의존은 재도출 대상이며 새 reason 신설 0.
- **포맷 소비(§5)** — Work Graph·Task·공통 Failure Report 포맷은 work-graph.md §2·§3·§4를 § 포인터로만 소비(필드 표 재게재·재정의 0). `delegation` 정본은 02 §3.2-B(07 INV-3).
- **경계(§6)** — 07·02 재정의·확장 0, Dispatch·Merge 비소관(07 R2 형제 불인용), 물리 실현 Adapter Binding 소관(07 §4.1·§4.2), 금지 토큰 0(자가 전수 스캔), Glossary §3.2-J J-07 정본만 사용.
- 모든 규칙은 07 §3.1-A의 인스턴스이며, 물리 실현은 Adapter Binding 소관이다. 형태 A(문서) → 형태 B(실행 코드) 전환에도 Core Contract 변경은 0이다.
