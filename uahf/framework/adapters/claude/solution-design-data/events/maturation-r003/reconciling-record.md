# Reconciling Record — Reconcile 단계 (04-solution-design §3.5, maturation-r003)

> 대상: `proposal-data-layer-designer.md`(역할 `data-layer-designer`) × `proposal-ui-view-designer.md`(역할 `ui-view-designer`)
> 목적: 두 제안 사이의 인터페이스 경계(도메인 모델 ↔ UI 컴포넌트가 주고받는 데이터 형태, RSC/API route 경계)를 점검하고 조정 결정을 내려 하나의 병합된 설계로 수렴시킨다.

---

## 1. 두 제안 요약

### 1.1 `data-layer-designer` 제안 요약

Contract v1 `architectureDirection.decisions` 1항의 "파서/데이터 계층 ↔ 도메인 모델 ↔ UI 컴포넌트" 분리 중 파서/도메인 측을 구체화한다.

- **도메인 타입(§1)**: `NormalizedEvent`(`StepEvent`/`GateEvent`/`AnnotationEvent` 판별 유니온) · `Revision` · `Artifact` · `InvokeLog` · `RunSummary`(파생, 비영속). 각 타입은 TS 인터페이스 + zod 스키마 이중 정의.
- **이벤트 분류(§2)**: 명시 판별자 우선, 부재 시 필드 시그니처 추론(`gateId`→gate, `stepId`→step, 그 외→annotation 강등 + 파서 경고).
- **게이트 상태 판별(§3)**: `reduceGateStates(events): Map<gateId, "pending"|"resolved">` — seq를 유일한 진실 근원으로 삼아 동일 gateId의 마지막 레코드가 `resolved`가 아니면 무조건 `pending`(안전측 처리).
- **계보 변환(§4)**: `buildLineageGraph(revisions, artifacts)`로 역방향 포인터(`basis`/`derivedFrom`)를 정방향 인접 리스트(`forward: Map<parentId, childId[]>`)로 역전한 뒤, 루트(= 자식으로 한 번도 등장 안 한 노드)에서 DFS로 정방향 트리를 구성해 UI에 전달한다고 서술(단, 트리의 구체 타입/생성 함수는 미명명).
- **읽기 전용·인코딩 리스크 완화(§5)**: 쓰기 API import 자체를 배제하는 `fs-reader.ts` 게이트웨이, path 정규화 + 루트 이탈 방지, UTF-8/BOM 처리, CRLF 안전 라인 분리, 라인 단위 try/catch 드리프트 격리.
- **모듈 경계(§6)**: `lib/data/{parsers,domain}/` + `types.ts`. 단방향 의존(`parsers → domain → UI`). rule 6에서 UI는 `domain/*`의 출력 타입(`NormalizedEvent[]`, 게이트 상태 맵, 계보 트리, `RunSummary[]`)만 props/data 계약으로 소비한다고 명시.

### 1.2 `ui-view-designer` 제안 요약

Contract v1 `architectureDirection.decisions` 1항 중 "↔ UI 컴포넌트" 측과 `requirements.functional` 4항·`constraints`(Next.js/React/TS·Tailwind/shadcn·서버 읽기 전용)·`requirements.quality`(새로고침 기반 최신성)를 구체화한다. data-layer §6의 인터페이스 경계를 소비 계약으로 그대로 인용한다고 명시.

- **라우팅(§1)**: App Router 2라우트 — `app/page.tsx`(목록) · `app/runs/[runId]/page.tsx`(심층 뷰), 각자 `loading.tsx`/`not-found.tsx` 보유.
- **컴포넌트 분해(§2)**: `RunDetailPage`가 `RunHeader` · `EventTimelinePanel`(+`ParserWarningAlert`) · `LineagePanel`(재귀 `LineageTreeNode`) · `CostPanel`(`CostSummaryCards` + `CostBreakdownTable`) 4패널을 독립 데이터 인자로 조합.
- **인터페이스 계약(§3)**: RSC에서 `domain/*` 함수를 직접 `await` 호출 — API route 미사용(MVP). 소비 대상으로 `RunSummary[]`, `{events, gateStates}`, `LineageTree`, `CostAggregate`를 명시. 확장 시(polling/SSE) `app/api/runs/[runId]/route.ts`를 동일 `domain/*` 재사용으로 신설 가능하도록 경계만 예비.
- **shadcn/ui 매핑(§4)**: Table/Badge/ScrollArea/Collapsible(트리 재귀)/Card/Alert/Skeleton 등 요구사항별 컴포넌트 대응표.
- **쓰기 0 + 최신성(§5)**: RSC 서버 전용 실행 + API route 미생성의 이중 경계, `force-dynamic`으로 캐시 배제.
- **Wireframe**: 목록 뷰(테이블) · 심층 뷰(좌 타임라인/우 계보 2열 + 하단 비용 패널) 텍스트 스케치.

---

## 2. 발견한 상충/공백

전수 대조 방식: data-layer §6이 선언한 4개 소비 타입(`NormalizedEvent[]`, 게이트 상태 맵, 계보 트리, `RunSummary[]`)과 ui-view-designer §2·§3·§4·Wireframe이 실제로 참조하는 모든 데이터 식별자를 1:1로 맞춰봄. 범위: 두 제안 문서 본문 전체(코드 블록·표·Wireframe 포함) — 이 워크스페이스 밖 파일(예: 실제 구현 코드)은 아직 존재하지 않으므로 대조 대상이 아니다.

**상충은 없다** — 두 제안의 계층 분리 원칙(파서→도메인→UI 단방향 의존, 읽기 전용 이중 경계, seq 기반 인과, RunSummary 파생 뷰)은 서로 반대 방향으로 결정한 지점이 하나도 없다. 다만 아래 2건의 **공백**(정의 누락)을 발견했다 — 둘 다 "존재를 가정하고 소비하는 타입이 반대편 문서에 형식적으로 정의되어 있지 않은" 동일 패턴이다.

### 2.1 공백 A — `LineageTree`/`LineageTreeNode` 타입 미정의

- data-layer §4는 "각 루트에서 DFS로 정방향 트리를 구성해 UI 계보 뷰(트리 컴포넌트)에 전달한다"고 **절차만 서술**할 뿐, 그 결과 구조체의 TS 타입을 §1(도메인 타입 목록)에 넣지 않았다. §6 모듈 지도의 `domain/lineage.ts`도 "§4 그래프 변환"으로만 적혀 있고, 코드 예시(`buildLineageGraph`)의 반환값은 `{forward: Map<string,string[]>, nodeOf: Map<string, Revision|Artifact>}`로 — 이는 그래프(인접 리스트)이지 트리가 아니다. 2단계(루트 탐지 + DFS 트리화)를 수행하는 함수가 이름도 시그니처도 없다.
- ui-view-designer §2(`LineageTreeNode`가 "루트 배열 + 각 노드의 자식 목록"을 재귀 순회)와 §3(소비 대상으로 `LineageTree` 명시)은 이 트리 타입이 **이미 domain 계층 출력으로 존재한다고 전제**하지만, 그 전제의 근거가 되는 정의는 data-layer 문서 어디에도 형식화되어 있지 않다.
- 성격: 상충이 아니라 **양쪽 다 옳은 방향을 가리키는데 그 사이를 잇는 명명된 계약이 비어 있는 공백**이다.

### 2.2 공백 B — `CostAggregate`(모델별 집계) 타입 및 산출 함수 미정의

- ui-view-designer §3은 소비 대상으로 `CostAggregate`를 명시하고, §2/§4는 `CostSummaryCards`가 "모델별 총 토큰/총 비용 요약 카드 그룹"을 렌더한다고 서술한다.
- data-layer §1은 `InvokeLog`(원본 정규화, invocation 단위 레코드)와 `RunSummary.totalCostUsd`(run 전체 단일 합계, 목록 뷰용)만 정의한다 — **모델별로 그룹화한 집계**는 어느 도메인 타입에도 대응하지 않는다. §6 모듈 지도의 `domain/run-summary.ts`도 "RunSummary 파생 계산"만 언급할 뿐 모델별 비용 집계를 담당한다는 서술이 없다.
- 즉 `CostSummaryCards`가 그리려는 데이터를 만들어낼 domain 함수가 현재 어느 제안에도 존재하지 않는다. 이 공백을 방치하면 UI 계층이 `InvokeLog[]`를 직접 모델별로 `reduce`하게 되어, data-layer §6 rule 6("UI는 domain 출력 타입만 소비")과 rule 3("domain/*은 parsers/*를 import하지 않는다" — 역으로 집계 로직이 domain 밖 UI로 새는 것도 동일 원칙 위반)에 암묵적으로 어긋난다.
- 반면 `CostBreakdownTable`(invocation 단위 상세 테이블)은 `InvokeLog[]`를 그대로 행 단위로 렌더하면 되므로 공백이 아니다 — `InvokeLog`는 이미 data-layer §1에 정의된 도메인 타입이다.

### 2.3 확인 — 상충처럼 보였으나 상충이 아닌 지점 (RSC vs API route)

- data-layer §6 rule 6은 "API route/RSC 경계에서 이 도메인 타입을 그대로 직렬화해 전달한다"고 서술 — "API route"와 "RSC"를 나열형으로 언급해 얼핏 API route를 필수로 요구하는 것처럼 읽힐 소지가 있었다.
- ui-view-designer §3은 MVP에서 API route를 생성하지 않고 RSC가 `domain/*`을 직접 `await` 호출하기로 결정했다(Contract quality 요구사항 "새로고침 기반 최신성" 근거).
- 대조 결과: data-layer의 문구는 "API route **또는** RSC 중 어느 경계에서 소비되든 도메인 타입 그대로 전달된다"는 대안 나열이지, API route를 강제하는 단정문이 아니다 — data-layer §6 다른 어디에도 API route를 MVP에 요구하는 규칙이 없다. 따라서 ui-view-designer의 RSC 전용 결정은 data-layer가 허용한 선택지 내부의 구체화이며 상충이 아니다. 다만 원 문구가 모호했으므로 §3(통합 아키텍처)에서 명시적으로 확정해 문서화한다.

### 2.4 그 외 대조 항목 — 정합 확인(공백 없음)

- `NormalizedEvent`(`kind` 판별 유니온) ↔ `StepEventRow`/`GateEventRow`/`AnnotationEventRow` 분기: 판별 로직은 domain에서 종료, UI는 표시 분기만 — 일치.
- 게이트 상태 `Map<string, GateState>` ↔ `GateStateBadge`: 타입·의미 일치.
- `RunSummary.status`(`"완주"|"정지"|"게이트 대기"`) ↔ UI Badge variant 매핑(완주=default·게이트 대기=secondary·정지=destructive) 및 목록 Wireframe 컬럼: 3개 열거값이 철자 단위로 정확히 일치.
- `Artifact.approvalState` ↔ 계보 노드 Badge 매핑: 일치.
- seq 기반 정렬(≠ ts) 원칙: data-layer §3의 "seq가 유일한 진실 근원" ↔ UI Wireframe의 "seq 오름차순" — 일치.
- 읽기 전용 이중 경계: data-layer §5(파서 계층에 쓰기 API import 자체 없음) + UI §5(RSC 서버 전용 실행·API route 미생성·클라이언트에 mutation 핸들러 미주입) — 서로 다른 계층에서 독립적으로 성립하는 보강 관계이며 충돌 없음.
- runId 경로 검증: data-layer §5(경로 순회 방지·루트 하위 검증) ↔ UI `not-found.tsx`(존재하지 않는 runId 대응) — 계층이 다른 상호 보완, 충돌 없음.

---

## 3. 조정 결정

1. **공백 A 해소 — `LineageTree` 타입을 data-layer 소유 타입으로 정식 승격한다.**
   data-layer-designer의 §1 도메인 타입 목록에 아래를 추가하고, §6 모듈 지도의 `domain/lineage.ts`가 `buildLineageGraph`(기존, 그래프 구성) 외에 트리화 2단계를 수행하는 `toLineageTree` 함수를 **추가로 export**하도록 확정한다. 이는 data-layer §4가 이미 산문으로 서술한 절차를 형식화하는 것일 뿐, 두 역할 중 어느 쪽의 기존 결정도 뒤집지 않는다 — data-layer 소유로 귀속하는 이유는 §6 rule 3("domain/*은 도메인 타입만 입력받는다")·rule 1(원본 물리 형식은 parsers/*만 안다)과 동일한 계층 분리 원칙상 그래프/트리 변환이 UI가 아닌 domain 계층 책임이기 때문이다.

2. **공백 B 해소 — 모델별 비용 집계 도메인 함수를 data-layer §6 모듈 지도에 신설한다.**
   `domain/cost-aggregate.ts`(신설 파일, data-layer 소유)가 `InvokeLog[]`를 입력받아 `CostAggregate`(모델별 소계 + 전체 합계)를 산출하는 순수 함수를 export한다. `CostSummaryCards`는 이 `CostAggregate.byModel`을 props로 소비하고, `CostBreakdownTable`은 기존 `InvokeLog[]`를 그대로 소비한다(공백 아님, 변경 없음) — 이로써 UI 계층에 집계 로직이 새지 않는다.

3. **RSC 전용 경계를 확정 문서화한다.**
   ui-view-designer §3의 결정(API route 미생성, RSC가 `domain/*`을 직접 호출)을 이 성숙 run의 확정 결정으로 채택한다 — data-layer §6 rule 6의 "API route/RSC" 병기는 대안 나열이었을 뿐 API route를 요구하지 않았으므로 이 확정은 data-layer 쪽 어떤 결정도 변경하지 않는다. 확장 시 `app/api/runs/[runId]/route.ts` 신설 경로(ui-view-designer §3의 예비안)는 그대로 유지한다.

4. **소유권 원칙 재확인.** 위 1·2 모두 data-layer-designer의 기존 §6 모듈 경계 규칙(단방향 의존 `parsers → domain → UI`, 파일 1개 = 관심사 1개)을 그대로 적용해 신설했다 — ui-view-designer의 컴포넌트 분해(§2)·shadcn 매핑(§4)·Wireframe은 무수정으로 유지된다. 두 제안 중 어느 쪽도 폐기하거나 대체하지 않았다.

---

## 4. 통합 아키텍처 서술

### 4.1 계층 구조(확정)

```
lib/data/
  parsers/
    events-parser.ts       # events.jsonl → NormalizedEvent[]
    revisions-parser.ts    # revisions.jsonl → Revision[]
    artifacts-parser.ts    # artifacts.jsonl → Artifact[]
    invoke-log-parser.ts   # logs/invoke-*.json → InvokeLog[]
    fs-reader.ts           # 읽기 전용 게이트웨이 — 유일한 fs 접근점(쓰기 API import 0)
  domain/
    gate-state.ts          # reduceGateStates(events): Map<gateId, GateState>
    lineage.ts              # buildLineageGraph(...) → forward 그래프
                             # + toLineageTree(graph): LineageTree  ← 조정 결정 1 신설
    cost-aggregate.ts       # aggregateCosts(logs: InvokeLog[]): CostAggregate  ← 조정 결정 2 신설
    run-summary.ts          # RunSummary 파생 계산(목록 뷰용, 전체 run 단일 합계)
  types.ts                  # 도메인 타입 전체 + zod 스키마
                             #  = NormalizedEvent(StepEvent|GateEvent|AnnotationEvent)
                             #  | Revision | Artifact | InvokeLog | RunSummary
                             #  | LineageTreeNode / LineageTree   ← 신설
                             #  | ModelCostAggregate / CostAggregate ← 신설

app/
  page.tsx                  # 뷰 A: RSC, run-summary.ts를 직접 await 호출 → RunSummary[]
  loading.tsx
  runs/[runId]/
    page.tsx                # 뷰 B: RSC, 4개 domain 함수를 직접 await 호출
    loading.tsx
    not-found.tsx
```

의존 방향은 `parsers → domain → UI(app/)`로 단방향 고정이며, `domain/*` 신설 2개 파일도 기존 파일과 동일하게 `parsers/*`를 import하지 않는다(도메인 타입만 입출력).

### 4.2 신설 타입(조정 결정 1·2 반영)

```ts
// --- 계보 트리 (domain/lineage.ts 출력) ---
interface LineageTreeNode {
  id: string;                       // artifactId | revisionId
  node: Revision | Artifact;        // 원본 정규화 노드(approvalState 등 포함)
  children: LineageTreeNode[];
}
type LineageTree = LineageTreeNode[]; // 루트(= 파생물로 한 번도 등장하지 않은 노드) 배열

function toLineageTree(
  graph: { forward: Map<string, string[]>; nodeOf: Map<string, Revision | Artifact> }
): LineageTree {
  // §4 2단계: 루트 탐지 → 방문 집합으로 사이클 방어하며 DFS 트리화
  // 사이클 감지 시 해당 서브트리만 중단 + 파서 경고, 나머지는 부분 렌더 계속(§5 무음 손실 금지 원칙과 동일)
}

// --- 비용 집계 (domain/cost-aggregate.ts 출력) ---
interface ModelCostAggregate {
  model: string;
  tokensIn: number;
  tokensOut: number;
  costUsd: number;
  invocationCount: number;
}
interface CostAggregate {
  byModel: ModelCostAggregate[];
  totalTokensIn: number;
  totalTokensOut: number;
  totalCostUsd: number;
}

function aggregateCosts(logs: InvokeLog[]): CostAggregate {
  // model별 group-by 후 소계 + 전체 합계
}
```

### 4.3 데이터 계층 ↔ UI 최종 인터페이스 계약

| 패널(ui-view-designer §2) | 소비 데이터(domain 출력, 확정) | 산출처(domain 파일) |
|---|---|---|
| `RunHeader` | `RunSummary`(단건) | `run-summary.ts` |
| `EventTimelinePanel` | `{ events: NormalizedEvent[], gateStates: Map<string, GateState> }` | `events-parser.ts`(정규화) + `gate-state.ts`(리듀스) |
| `ParserWarningAlert` | 파서 경고 목록(§5 드리프트 대응 축적분) | 각 `parsers/*`가 축적 |
| `LineagePanel` → `LineageTreeNode`(재귀) | `LineageTree` | `lineage.ts`(`buildLineageGraph` + `toLineageTree`, 신설 확정) |
| `CostPanel.CostSummaryCards` | `CostAggregate.byModel` | `cost-aggregate.ts`(신설 확정) |
| `CostPanel.CostBreakdownTable` | `InvokeLog[]`(원본 정규화, 집계 없이 그대로) | `invoke-log-parser.ts` |
| 목록 뷰(`app/page.tsx`) | `RunSummary[]` | `run-summary.ts` |

**호출 경계(확정)**: `app/page.tsx`·`app/runs/[runId]/page.tsx`는 모두 Server Component로, 위 표의 `domain/*` 함수를 **직접 `await` 호출**한다 — API route는 MVP에서 생성하지 않는다(조정 결정 3). 클라이언트 컴포넌트 경계(`"use client"`)는 `LineageTreeNode`의 펼침/접힘처럼 순수 UI 상태가 필요한 최소 지점에만 긋고, 그 경계에도 이미 계산된 정적 데이터만 props로 전달하며 mutation 함수는 전달하지 않는다(ui-view-designer §3 원안 유지).

**단방향 의존 확정**: `parsers/*`(원본 물리 형식 인지) → `domain/*`(도메인 타입만 입출력, `cost-aggregate.ts`·`lineage.ts` 신설분 포함) → `app/*`(도메인 출력 타입만 props로 소비, 원본 파일·파서 존재를 모름). 드리프트 발생 시 수정 범위는 `parsers/*` 1개 파일 + 필요시 `types.ts`(스키마 안정 유지 시 무수정)로 국한되며, 이번 조정으로 신설된 `lineage.ts`의 `toLineageTree`·`cost-aggregate.ts`의 `aggregateCosts`도 이 보장 범위 안에 있다(원본 파일 형식과 무관하게 정규화된 도메인 타입만 입력받으므로).

**읽기 전용·최신성 이중 경계(변경 없음, 재확인)**: `fs-reader.ts`(쓰기 API import 0) + RSC 서버 전용 실행(클라이언트에 fs 접근 수단 자체 부재) + API route 미생성(mutation 수신 엔드포인트 자체 부재) + `force-dynamic`(캐시 배제) — 4중 보장이 두 제안 원안 그대로 유지된다.

---

## 결론

두 제안 사이에 상충은 없다. 발견한 공백 2건(`LineageTree`·`CostAggregate` 타입 미정의)은 모두 "한쪽이 이미 소비를 전제한 타입을 반대쪽이 형식적으로 정의하지 않은" 동일 패턴이며, data-layer-designer가 이미 확립한 모듈 소유 원칙(`domain/*` = 도메인 타입 산출 전담, 파일 1개 = 관심사 1개)을 그대로 확장해 신설 2개 파일(`domain/lineage.ts`의 `toLineageTree` 추가 export, `domain/cost-aggregate.ts` 신설)로 해소했다. RSC 대 API route 지점은 잠재 상충처럼 보였으나 대조 결과 상충이 아니며, 이번 기록에서 RSC 전용을 확정 문서화했다. 두 제안의 다른 모든 결정(도메인 타입, 이벤트 분류, 게이트 리듀서, 읽기 전용 경계, 라우팅, 컴포넌트 분해, shadcn 매핑, Wireframe)은 무수정으로 통합 아키텍처에 그대로 편입된다.
