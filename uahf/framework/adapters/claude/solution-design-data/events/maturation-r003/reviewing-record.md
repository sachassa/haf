# Reviewing Record — Review 단계 (04-solution-design §3.6, maturation-r003)

> 대상: `reconciling-record.md`(통합 아키텍처, data-layer-designer × ui-view-designer 조정 결과)
> 대조 기준: 원본 Project Contract v1(`pc-uahf-control-plane-001`, 절대경로 `C:\my-claude-project\uahf-control-plane\.claude\project-contract\project-contract.v1.md`, 읽기 전용)
> 목적: 통합 설계가 Contract v1의 intent·requirements·constraints·risks와 정합적인지, SP-INV 8 최소 할당 원칙이 지켜졌는지, 설계 공백이 남아있지 않은지 검토하고 최종 승인/보류를 판단한다.

---

## 1. 검토 범위·방법(완전성 주장 전 스윕 범위 명시)

이 워크스페이스 내 5개 문서(assessing-judgment.md·proposal-data-layer-designer.md·proposal-ui-view-designer.md·reconciling-record.md·stage-plan.json) 전문과 원본 Contract v1 전문을 대상으로 다음 두 방식을 병행했다.

1. **reconcile 자체 감사 재확인** — reconciling-record.md §2가 수행한 "data-layer §6 선언 4개 소비 타입 ↔ ui-view-designer 참조 식별자" 1:1 대조(§2.1~§2.4)를 원 제안 문서 두 편과 대조해 재현·검증했다.
2. **독립 교차검증** — reconcile이 다루지 않은 축, 즉 *각 제안 문서 내부의* 타입 선언과 실제 산출/소비 경로 사이의 자기 정합성을 별도로 훑었다(reconcile의 대조축은 "문서 A ↔ 문서 B 경계"였고, "문서 A 내부 필드 하나가 문서 A 자신의 다른 절과 일치하는가"는 별도 축이므로 반복 스캔이 아니다).

**한계**: 이 성숙 run 워크스페이스에는 실제 구현 코드·zod 스키마·런타임이 아직 존재하지 않는다(reconciling-record.md §2 서두가 명시한 대로 "이 워크스페이스 밖 파일은 대조 대상이 아님"과 동일 경계). 아래 판정은 **문서 수준 설계 정합성**에 한정되며, 구현 단계에서 드러날 수 있는 새로운 공백까지 배제하지 않는다. 또한 원본 Contract v1의 `provenance`·`readiness` 필드(front-matter 전용, 서술 위주 본문에는 축약)까지 포함해 대조했으나, Contract v1이 참조하는 `greenfield-r003` 이벤트 로그 자체는 이 리뷰 범위 밖이다(Contract v1 문면 자체를 정본으로 삼았다).

---

## 2. 정합성 판정 — Contract v1 대조표

| Contract v1 항목 | reconciling-record.md 대응 | 판정 |
|---|---|---|
| Intent — "단일 run 심층 뷰"(타임라인·게이트·계보·비용 한 화면) | §4.3 4패널(EventTimelinePanel·LineagePanel·CostPanel·RunHeader) 1페이지 조합 | 정합 |
| functional 1 — run 목록 요약 | `app/page.tsx` ← `RunSummary[]`(run-summary.ts) | 정합 |
| functional 2 — 이벤트 타임라인+게이트(seq 순) | `{events, gateStates}` ← events-parser + gate-state.ts(seq 기반 reduceGateStates) | 정합 |
| functional 3 — revision·artifact 계보 | `LineageTree` ← `buildLineageGraph`+`toLineageTree`(신설, 조정 결정 1) | 정합 |
| functional 4 — 토큰/비용 모델별 집계 | `CostAggregate.byModel` ← `aggregateCosts`(신설, 조정 결정 2) | 정합 — 이 항목이 바로 reconcile 공백 B의 해소 대상이었다 |
| quality — 관찰 전용(쓰기 0) | §4.3 "읽기 전용·최신성 이중 경계" 4중 보장(fs-reader.ts 쓰기 API import 0 + RSC 서버 전용 + API route 미생성 + force-dynamic) | 정합 |
| quality — 새로고침 기반 최신성 | 상동(force-dynamic) | 정합 |
| quality — MVP 제외 목록(실시간·ETA/velocity·CPU/메모리·멀티프로젝트) | 통합 설계 어디에도 이 4항목을 도입하는 결정이 없음(부재 확인) | 정합(위반 없음 — 배제 항목은 "설계하지 않음"이 곧 준수) |
| constraints — Next.js/React/TS·Tailwind/shadcn | ui-view-designer §1·§4 그대로 채택, 무수정 편입 | 정합 |
| constraints — 서버 측 읽기 전용 직정독(env 경로) | data-layer §5(fs-reader.ts, 루트 경로 설정 1곳 주입) | 정합 |
| constraints — 데이터 소스 = orchestration-data/runs/만 | 통합 설계가 참조하는 4개 원본이 모두 이 범위 내(events/revisions/artifacts.jsonl·logs/invoke-*.json) | 정합 |
| risks — 데이터 형식 드리프트(완화=파서 계층 격리) | §4.3 "드리프트 발생 시 수정 범위는 parsers/* 1개 파일(+필요시 types.ts)로 국한" — 신설 2개 파일도 이 보장 범위 안 | 정합 |
| risks — 범위 크리프(완화=제외 목록 준수) | 위 quality 행과 동일 근거 | 정합 |
| risks — Windows 경로/인코딩(완화=UTF-8·정규화) | data-layer §5(UTF-8/BOM 처리, CRLF `\r?\n` 분리, path 정규화+루트 이탈 방지) | 정합 |
| risks — 사용자 게이트 의존 | 아키텍처 설계 범위 밖(프로세스 리스크) — 통합 설계가 이를 악화·완화하지 않음, 중립 | 해당 없음(설계 대상 아님, 위반 아님) |
| architectureDirection.decisions 1(계층 분리) | 통합 설계 전체가 이 결정 1항을 구체화한 것 — 원 결정과 방향 일치, 대체 아님 | 정합 |
| architectureDirection.decisions 2(읽기 전용 파생 뷰) | 상동 | 정합 |
| architectureDirection.decisions 3(확장 경로 예비, 인프라 선구현 금지) | ui-view-designer §3 "app/api/.../route.ts 예비"— 파일 미생성, 경계만 예비 | 정합 |
| architectureDirection.open 2항(실시간 메커니즘·Control 권한) | 통합 설계가 손대지 않음(MVP 밖 스코프 유지, assessing-judgment.md도 이를 성숙 대상에서 명시 제외) | 정합(이월 유지, 이번 run의 대상 아님) |

**결론**: 17개 대조 행 전건에서 상충·역행 없음. 이는 위 §1의 명시된 범위(문서 수준, 이 워크스페이스+Contract v1 전문) 내에서의 전수 대조 결과이며, 구현 코드 수준의 정합성까지 보증하지 않는다.

---

## 3. SP-INV 8 최소 할당 원칙 검토

- 할당 역할 수 = 2 (`data-layer-designer`, `ui-view-designer`) — 최소 할당 범위(1~3) 내.
- assessing-judgment.md §4가 3번째 역할(예: 리스크 전담)을 별도로 두지 않은 근거를 명시(Contract v1 `architectureDirection.decisions` 1항이 이미 "파서/데이터 계층 ↔ 도메인 모델 ↔ UI 컴포넌트"의 2분할을 선언했고, 두 역할이 이와 1:1 대응)로 제시했다 — 사후적으로도 이 판단은 유지된다: 실제 두 제안·조정 과정에서 세 번째 관심사(예: 리스크 자체를 별도로 설계해야 할 필요)가 새로 드러나지 않았고, risks 4항 중 아키텍처로 완화 가능한 2항(드리프트·인코딩)은 모두 data-layer-designer 역할에 자연 흡수되었다.
- 판정: **SP-INV 8 준수**.

---

## 4. 설계 공백 검토

### 4.1 reconcile 자체 식별 공백 2건 — 해소 확인

- **공백 A(`LineageTree` 타입 미정의)**: 조정 결정 1로 `domain/lineage.ts`에 `toLineageTree` 함수를 추가 export하도록 확정, §4.2에 `LineageTreeNode`/`LineageTree` 타입이 명시적으로 정의됨 — **해소 확인**. 사이클 방어(방문 집합)까지 절차 서술에 포함되어 있어 안전성 결손 없음.
- **공백 B(`CostAggregate` 미정의)**: 조정 결정 2로 `domain/cost-aggregate.ts`(`aggregateCosts`) 신설, §4.2에 `ModelCostAggregate`/`CostAggregate` 타입 정의 — **해소 확인**. `CostBreakdownTable`(비집계 원본 그대로)과의 경계도 명확히 구분되어 있어 UI로의 로직 유출 없음.
- RSC vs API route 잠재 상충(§2.3)은 대조 결과 상충이 아니었고 이번 기록에서 확정 문서화됨 — 별도 조치 불필요.

### 4.2 독립 교차검증에서 발견한 잔여 사항 — `GateEvent.state` 필드의 생산·소비 경로 불명확 (경미, 비차단)

- `proposal-data-layer-designer.md` §1의 `GateEvent` 인터페이스는 `state: GateState`(주석: "§3 판별 로직의 산출")를 필드로 선언한다. 그러나 §3의 `reduceGateStates(events: GateEvent[]): Map<string, GateState>`는 **동일 `gateId`를 가진 이벤트 배열 전체**를 훑어 마지막 레코드 기준으로 상태를 도출하는 리듀서이지, 개별 `GateEvent` 레코드 하나에 상태를 채워 넣는 함수가 아니다. §2의 분류 함수 `classifyEvent(record: unknown): NormalizedEvent`도 레코드 1건만 입력받으므로, 형식상 이 함수가 `GateEvent.state`를 채우려면 같은 `gateId`의 다른 레코드들을 알아야 하는데 그 경로가 어디에도 서술되어 있지 않다.
- 소비 측(§4.3 인터페이스 계약, `proposal-ui-view-designer.md` §2·§3)도 `GateStateBadge`가 **별도의** `gateStates: Map<string, GateState>`(이벤트와 분리된 두 번째 데이터 인자)를 소비하도록 확정되어 있다 — 즉 확정된 실제 데이터 흐름은 `GateEvent.state` 필드를 전혀 참조하지 않는다.
- 결과적으로 `GateEvent.state` 필드는 (a) 명확한 생산 경로가 없고 (b) 확정된 소비 경로에서도 쓰이지 않는 **선언되었으나 생산자·소비자가 없는 필드**다. reconcile §2의 대조축은 "data-layer §6 선언 출력 ↔ ui-view-designer 참조"(모듈 간 경계)였기 때문에 이 문제(같은 문서 내부의 타입 필드 하나가 그 문서 자신의 다른 절과 불일치)는 그 대조망에 걸리지 않았다.
- **영향 평가**: 확정된 인터페이스 계약(§4.3의 `{events, gateStates}` 분리 형태)이 이미 이 필드 없이도 완결되어 있으므로, 이 잔여 사항은 **구현을 막지 않는다**. 다만 다음 구현 단계에서 혼선을 막기 위해 `GateEvent.state`를 (i) 타입 선언에서 제거하거나 (ii) "표시 편의용 caching 필드 — `reduceGateStates` 산출 후 이벤트 목록에 역주입하는 후처리 1패스"로 명시적으로 재정의하는 정리가 필요하다. 이 성숙 run의 산출 범위(reconciling-record.md는 읽기 전용, 수정 금지)를 넘으므로 본 리뷰에서는 **정정하지 않고 관찰 사항으로만 기록**한다.

### 4.3 그 외 — 잔여 공백 없음

- `GateState`(`"pending"|"resolved"`) 타입 자체는 §3에 명시 정의되어 있어 정의 누락이 아니다(§4.2의 이슈는 그 타입을 참조하는 특정 필드의 생산 경로 문제이지, 타입 자체의 부재가 아니다).
- 그 외 도메인 타입(`NormalizedEvent`·`Revision`·`Artifact`·`InvokeLog`·`RunSummary`)과 UI 소비 지점은 reconcile §2.4의 대조 결과와 본 리뷰의 재확인 결과가 일치하며 추가 공백을 발견하지 못했다(§1의 범위·한계 내에서).

---

## 5. 최종 판단

**승인(v2 CANDIDATE 발행)** — 아래 근거로 이 통합 설계를 Contract v2 후보 문면의 architectureDirection 확장 근거로 채택한다.

1. Contract v1의 intent·requirements(functional 4·quality 3)·constraints(5)·risks(4)·기존 architectureDirection(결정 3·open 2) 전 항목과 상충 없음(§2 대조표, 17행 전건 정합).
2. SP-INV 8 최소 할당 원칙 준수 확인(§3).
3. reconcile 자체 식별 공백 2건 모두 해소 확인(§4.1).
4. 독립 교차검증에서 발견한 잔여 사항 1건(`GateEvent.state` 생산·소비 경로 불명확, §4.2)은 확정된 인터페이스 계약을 무효화하지 않는 **비차단 관찰 사항**이며, 승인을 보류할 사유가 아니다 — 구현 단계 정리 항목으로 이월한다.
5. 이 승인은 **아키텍처 확장 결정의 채택**에 한정되며, Contract v2 자체의 발행(사용자 승인)은 별도 게이트다 — candidate/project-contract.v2.CANDIDATE.md는 `readiness.userApproval`·`provenance.terminal`을 명시적으로 미확정 상태로 유지한 미발행 후보 문면으로 작성했다.

### 이월 항목(다음 단계로)

- `GateEvent.state` 필드 정리(§4.2) — 구현 착수 시 또는 다음 정정 라운드에서 처리.
- Contract v1 architectureDirection.open 2항(실시간 갱신 메커니즘·Control 권한 경계)은 이번 성숙 run 범위 밖으로 그대로 이월(변경 없음).
