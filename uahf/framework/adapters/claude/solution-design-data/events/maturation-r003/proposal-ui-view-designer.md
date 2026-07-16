# Proposal — ui-view-designer (Propose 단계, maturation-r003)

> 역할: `ui-view-designer` (assessing-judgment.md 관심사 2: UI/뷰 아키텍처 설계).
> 근거: Project Contract v1(pc-uahf-control-plane-001) `architectureDirection.decisions` 1항("계층 분리 — 파서/데이터 계층 ↔ 도메인 모델 ↔ UI 컴포넌트") 중 "↔ UI 컴포넌트" 측을 구체 설계로 끌어올린다. `requirements.functional` 4항(run 목록 요약·이벤트 타임라인+게이트·revision/artifact 계보·토큰/비용 집계)과 `constraints`(Next.js+React+TS·Tailwind+shadcn/ui·서버 측 읽기 전용 직정독)·`requirements.quality`(관찰 전용·새로고침 기반 최신성)를 전제로 삼는다.
> 스코프: 관심사 2(UI/뷰 아키텍처)만 다룬다. 데이터/파싱/도메인 모델 설계는 `data-layer-designer` 역할의 산출물(`proposal-data-layer-designer.md`)에 위임하고, 본 문서는 그 산출물의 §6 인터페이스 경계(도메인 계층 출력 타입 — `NormalizedEvent[]`·게이트 상태 맵·계보 트리·`RunSummary[]`)를 소비 계약으로 그대로 인용한다.

---

## 1. 페이지/라우팅 구조

Next.js **App Router**(`app/`)를 사용해 Contract가 요구하는 두 뷰를 두 개의 독립 라우트로 분리한다.

```
app/
  page.tsx                    # 뷰 A: run 목록 요약 (functional 1항)
  loading.tsx                 # 목록 뷰 로딩 스켈레톤
  runs/
    [runId]/
      page.tsx                # 뷰 B: 단일 run 심층 뷰 (functional 2~4항 통합)
      loading.tsx              # 심층 뷰 로딩 스켈레톤
      not-found.tsx             # 존재하지 않는 runId 대응
```

**분리 근거**
- 두 뷰는 서로 다른 데이터 조합 비용을 가진다 — 목록 뷰는 `orchestration-data/runs/` 스캔 + 각 run당 경량 `RunSummary` 계산(§3의 gate-state 리듀서 1회씩)이지만, 심층 뷰는 단일 run에 대해 4개 도메인(이벤트·게이트 상태·계보 트리·비용 집계)을 전부 조합한다. 별도 route로 나누면 Next.js가 각각을 독립적인 로딩/에러/캐시 경계로 다룰 수 있어(각자의 `loading.tsx`/`error.tsx`), 심층 뷰의 무거운 조합이 목록 뷰의 응답성을 막지 않는다.
- 동적 세그먼트 `[runId]`는 Contract MVP 성공 기준("단일 run 심층 뷰")이 요구하는 "실재 orchestration run 1건을 열어" 동작과 URL 단위로 1:1 대응한다 — 특정 run을 북마크/공유 가능한 URL로 노출하는 부수 이익도 있다(요구사항 밖이지만 구조상 자연 발생).
- 확장 경로 예비(Contract architectureDirection 3항: "인프라 선구현 금지"): 향후 실시간 갱신(polling/SSE)이 도입되더라도 라우트 분리 자체는 그대로 유지된다 — 목록 뷰만 polling 대상으로 삼거나 심층 뷰만 SSE 구독으로 승격하는 선택이 라우트 재설계 없이 가능하다.

## 2. 단일 run 심층 뷰 내부 컴포넌트 분해

`app/runs/[runId]/page.tsx`(Server Component, 페이지 루트)가 아래 트리를 조합한다. 괄호는 소비하는 도메인 데이터(§3 참조).

```
RunDetailPage (app/runs/[runId]/page.tsx)
├── RunHeader                     (RunSummary 단건: runId·status·lastSeq·pendingGateCount)
│     └── RunStatusBadge          (status: 완주/정지/게이트 대기)
├── EventTimelinePanel            (NormalizedEvent[] + 게이트 상태 맵)
│     ├── EventTimelineList         # seq 오름차순 렌더 컨테이너
│     │     ├── StepEventRow        (kind: "step")
│     │     ├── GateEventRow        (kind: "gate") ── GateStateBadge(pending/resolved)
│     │     └── AnnotationEventRow  (kind: "annotation")
│     └── ParserWarningAlert        # data-layer §5 "N개 레코드 파싱 실패" 표면화(있는 경우만 렌더)
├── LineagePanel                   (계보 트리 — Revision/Artifact 정방향 트리)
│     └── LineageTreeNode (재귀)     # 각 노드 = artifact/revision 1개, approvalState 표시
│           └── LineageTreeNode ...  # 자식 파생물 재귀 렌더
└── CostPanel                      (InvokeLog[] 기반 집계)
      ├── CostSummaryCards           # 모델별 총 토큰/총 비용 상단 카드 그룹
      └── CostBreakdownTable         # invocation 단위 상세 테이블
```

**분해 원칙**
- 4개 패널(`EventTimelinePanel`·`LineagePanel`·`CostPanel`·`RunHeader`)은 Contract functional 2~4항 + run 식별 요약에 1:1 대응하며, 서로 독립적으로 렌더 가능하도록 각자 별개의 데이터 인자만 받는다(패널 간 props 공유 없음) — 한 패널의 데이터 이상(예: 파싱 실패)이 다른 패널 렌더를 막지 않는다.
- `EventTimelineList`는 kind 판별 유니온(`NormalizedEvent`)을 그대로 받아 내부에서 `kind`에 따라 `StepEventRow`/`GateEventRow`/`AnnotationEventRow`로 분기한다 — 판별 로직은 이미 도메인 계층에서 끝났으므로 컴포넌트는 표시 분기만 담당한다(관심사 분리 유지).
- `LineageTreeNode`는 자기 자신을 재귀 호출하는 단일 컴포넌트로 구현한다 — data-layer §4가 만든 정방향 트리 구조(루트 배열 + 각 노드의 자식 목록)를 그대로 재귀 순회하며, 트리 깊이가 컴포넌트 개수로 고정되지 않는다.

## 3. 데이터 계층 ↔ UI 컴포넌트 인터페이스 계약

**원칙 — RSC에서 도메인 계층 직접 소비, API route는 MVP에서 미사용.**

- `proposal-data-layer-designer.md` §6 경계 규칙 6항: "`ui-view-designer` 역할은 `domain/*`의 출력 타입(`NormalizedEvent[]`, 게이트 상태 맵, 계보 트리, `RunSummary[]`)만을 props/data 계약으로 소비한다"를 그대로 채택한다.
- `app/page.tsx`·`app/runs/[runId]/page.tsx`는 모두 **Server Component**로 작성하고, `lib/data/domain/*`의 함수(`run-summary.ts`·`gate-state.ts`·`lineage.ts`)를 서버 실행 컨텍스트에서 직접 `await` 호출한다. 즉 데이터 fetching이 클라이언트로 왕복하는 API route를 거치지 않고, 페이지 렌더 함수 내부에서 파서→도메인 파이프라인 결과를 곧바로 얻는다.
- **API route를 두지 않는 이유**: Contract quality 요구사항이 "새로고침 기반 최신성(실시간 스트리밍 제외)"으로 명시하므로, 클라이언트 측에서 별도 `fetch`로 데이터를 당겨올 필요가 없다 — 페이지 자체가 요청마다(§5) 서버에서 새로 렌더링되며 그 안에서 도메인 데이터를 직접 획득한다. API route를 경유시키는 것은 이 MVP에서 왕복 비용만 추가하는 불필요한 간접 계층이다.
- **확장 구조 예비**(architectureDirection 3항, "인프라 선구현 금지"이므로 코드는 만들지 않되 경계만 남긴다): 향후 polling/SSE 도입 시 `app/api/runs/[runId]/route.ts`를 신설해 동일한 `domain/*` 함수를 재사용하도록 설계하면 된다 — 이 라우트는 MVP에서 파일도 만들지 않는다(선구현 금지 원칙 준수). 도메인 계층이 이미 파서/UI 양측과 분리되어 있으므로 이 확장은 신규 파일 추가만으로 가능하고 기존 페이지·컴포넌트 수정을 요구하지 않는다.
- **각 뷰가 소비하는 데이터 형태**: 페이지 컴포넌트가 도메인 함수 호출로 얻은 구조체(`RunSummary[]`, `{ events: NormalizedEvent[], gateStates: Map<string,GateState> }`, `LineageTree`, `CostAggregate`)를 하위 패널 컴포넌트에 **props로 그대로 전달**한다. Server Component 간 전달이므로 직렬화 경계(클라이언트 번들 포함 여부)를 신경 쓸 필요가 있는 지점은 상호작용이 필요한 최소 요소뿐이다 — 예: `LineageTreeNode`의 펼침/접힘 로컬 상태처럼 순수 UI 상태만 필요한 경우에 한해 그 컴포넌트에만 `"use client"` 경계를 긋고, 그 경계에도 이미 서버에서 계산된 정적 데이터(트리 노드 값)만 props로 넘기지 mutation 함수는 넘기지 않는다.

## 4. shadcn/ui + Tailwind CSS 활용 전략

| 뷰/영역 | shadcn/ui 컴포넌트 | 비고 |
|---|---|---|
| run 목록 뷰 | `Table` | run별 행 — runId·status·lastSeq·pendingGateCount·totalCostUsd 컬럼 |
| run 목록 상태 표시 | `Badge` (variant: default/secondary/destructive) | 완주=default, 게이트 대기=secondary, 정지=destructive 매핑 |
| 이벤트 타임라인 | `ScrollArea` + Tailwind `border-l`(세로선) 커스텀 리스트 | shadcn에 전용 타임라인 컴포넌트가 없으므로 `ScrollArea` 컨테이너 + Tailwind 유틸리티(`border-l-2`·`pl-4`·`space-y-*`)로 세로 타임라인을 조립하고, 각 행에 `lucide-react`(shadcn 기본 동반 아이콘 세트) 아이콘으로 kind(step/gate/annotation) 구분 |
| 게이트 상태 | `Badge` + `Tooltip` | pending=outline 스타일(경고색), resolved=default(성공색); Tooltip으로 gateType·해소 seq 등 상세 노출 |
| 계보 뷰(트리) | `Collapsible` (재귀 조합) | shadcn에 트리/그래프 전용 컴포넌트가 없으므로 `Collapsible`(trigger=노드 라벨, content=자식 노드 재귀)을 `LineageTreeNode`가 재귀적으로 감싸는 방식으로 구현. Contract 요구사항은 "계보 **뷰**"이지 그래프 시각화 라이브러리 도입을 명시하지 않으므로, 별도 그래프 렌더링 의존성 추가는 MVP 범위를 벗어난다고 판단해 채택하지 않는다 |
| 계보 노드 승인 상태 | `Badge` | approvalState(pending/approved/rejected/superseded) 4종 variant 매핑 |
| 비용 패널 상단 | `Card` | 모델별 총 토큰/총 비용 요약 카드 그룹(`grid` + Tailwind `gap-4`) |
| 비용 패널 상세 | `Table` (+ 선택적 `Tabs`로 모델별 전환) | invocation 단위 상세 내역 |
| 로딩 상태 | `Skeleton` | 각 패널·목록 행의 loading.tsx에서 사용 |
| 파싱 경고 표면화 | `Alert` | data-layer §5 "N개 레코드 파싱 실패" 무음 손실 금지 원칙을 UI에서 가시화 |
| 레이아웃 전반 | Tailwind CSS grid/flex | 페이지 최상위는 `grid grid-cols-1 lg:grid-cols-2` 등으로 패널을 반응형 배치(§ Wireframe 참조), 다크/라이트는 shadcn 기본 테마 토큰 그대로 사용(별도 커스텀 팔레트 요구 없음) |

## 5. 관찰 전용(쓰기 조작 0) · 새로고침 기반 최신성 보장

**쓰기 조작 0 — UI 계층의 구조적 경계**
- 모든 데이터 fetching은 Server Component 내부 실행으로 국한된다 — Next.js RSC는 서버에서만 실행되고 그 코드가 브라우저 번들에 포함되지 않으므로, 클라이언트에는애초에 파일시스템/데이터 접근 API가 노출되지 않는다. 이는 data-layer-designer §5의 "읽기 전용 게이트웨이(fs-reader.ts)가 쓰기 API를 import하지 않는다"는 파서 계층 보장과 맞물려, "서버 쪽에 쓰기 함수 자체가 없음" + "클라이언트는 애초에 서버 파일시스템에 접근할 수단이 없음"이라는 2중 경계를 이룬다.
- MVP에서 `app/api/`에 어떤 라우트도 생성하지 않는다(§3) — mutation을 받을 엔드포인트 자체가 존재하지 않으므로, 프런트엔드에서 실수로 POST/PUT/DELETE를 보낼 대상이 물리적으로 없다.
- 클라이언트 컴포넌트(`"use client"` 경계, 예: `LineageTreeNode`의 펼침/접힘)에는 서버 데이터에 대한 mutation 핸들러를 일절 주입하지 않는다 — 오직 로컬 UI 상태(펼침 여부 같은 순수 표시 토글)만 `useState`로 다룬다.
- Contract MVP 제외 목록("Control 기능 도입은 MVP 밖")과 정합 — 향후 게이트 해소 등 쓰기 1종이 도입되더라도, 그 시점에 신규 API route + 신규 클라이언트 액션을 추가하는 것으로 계층 교체 없이 확장 가능하다(architectureDirection 3항).

**새로고침 기반 최신성**
- 두 페이지(`app/page.tsx`, `app/runs/[runId]/page.tsx`) 모두 `export const dynamic = "force-dynamic"`(또는 개별 fetch에 `cache: "no-store"`에 준하는 옵션)을 명시해, Next.js의 기본 정적/캐시 렌더링에 의해 오래된 데이터가 보일 가능성을 원천 차단한다. 이는 Contract quality 요구사항 "페이지 로드/새로고침 시 최신 데이터(실시간 스트리밍 제외)"를 코드 수준의 명시적 옵션으로 대응시키는 지점이다 — 캐싱을 "잊어서" 최신성이 깨지는 사고를 방지한다.
- 실시간 스트리밍(polling/SSE/WebSocket)에 해당하는 어떤 클라이언트 구독 로직도 MVP 컴포넌트 트리에 두지 않는다 — 최신성 확보 수단은 오직 "페이지 재방문/새로고침 시 서버 재렌더"뿐이며, 이는 architectureDirection의 "MVP = 읽기 전용 파생 뷰(새로고침 기반)" 결정과 1:1 대응한다.

---

## Wireframe

두 뷰(run 목록 뷰, 단일 run 심층 뷰)의 화면 레이아웃을 텍스트 기반으로 스케치한다. 실제 시각 디자인(간격·타이포그래피 등)이 아니라 §1~§4에서 결정한 컴포넌트 배치를 검증하기 위한 구조 스케치다.

### 뷰 A — run 목록 뷰 (`app/page.tsx`)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Header: "UAHF Control Plane" · (읽기 전용 배지)                        │
├──────────────────────────────────────────────────────────────────────┤
│  run 목록 테이블 (shadcn Table)                                        │
│  ┌────────────┬───────────────┬────────┬───────────────┬───────────┐  │
│  │ runId      │ status        │ lastSeq│ pendingGates  │ totalCost │  │
│  ├────────────┼───────────────┼────────┼───────────────┼───────────┤  │
│  │ r003       │ [Badge:정지]   │ 42     │ 1             │ $0.83     │  │
│  │ orch-m-... │ [Badge:완주]   │ 118    │ 0             │ $4.12     │  │
│  │ ...        │ [Badge:게이트] │ 7      │ 2             │ $0.05     │  │
│  └────────────┴───────────────┴────────┴───────────────┴───────────┘  │
│  (각 행 클릭 → /runs/[runId] 이동)                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 뷰 B — 단일 run 심층 뷰 (`app/runs/[runId]/page.tsx`)

```
┌──────────────────────────────────────────────────────────────────────┐
│  RunHeader: runId=r003  [Badge:상태]  lastSeq=42  pendingGates=1       │
├───────────────────────────────────┬────────────────────────────────┤
│  EventTimelinePanel (좌, 세로 흐름)  │  LineagePanel (우, 트리)         │
│  ──────────────────────────────    │  ────────────────────────────  │
│  │ seq1  [step]  started           │  ▸ artifact:proposal-...        │
│  │ seq2  [step]  completed         │    ├─ ▸ revision:rev-001        │
│  │ seq3  [gate]  [Badge:pending]   │    │    [Badge:approved]        │
│  │ seq4  [annot] "note text"       │    └─ ▸ artifact:derived-...    │
│  │ ...   (ScrollArea, seq 오름차순) │       [Badge:pending]           │
│  │ [Alert] 파싱 실패 N건 (있는 경우)  │  (Collapsible 재귀 노드)         │
├───────────────────────────────────┴────────────────────────────────┤
│  CostPanel (하단, 전체 폭)                                             │
│  ┌───────────────┐ ┌───────────────┐   ┌──────────────────────────┐ │
│  │ Card: model A  │ │ Card: model B  │   │ CostBreakdownTable        │ │
│  │ tokens/cost    │ │ tokens/cost    │   │ invocationId | tokens |  │ │
│  └───────────────┘ └───────────────┘   │ cost | model | ts        │ │
│                                          └──────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

**레이아웃 근거**: `EventTimelinePanel`(좌)과 `LineagePanel`(우)을 상단에서 좌우 2열(`grid-cols-1 lg:grid-cols-2`, 좁은 화면에서는 세로 스택)로 배치해 "이벤트 흐름"과 "파생 계보"라는 서로 다른 시간축(seq 순서 vs 파생 방향)을 시각적으로 분리하고, `CostPanel`은 두 패널과 독립적인 집계 정보이므로 하단 전체 폭으로 분리 배치한다. `RunHeader`는 페이지 최상단 고정 요약으로 Contract MVP 성공 기준("한 화면에" 렌더)이 요구하는 진입 시 즉시 파악 가능한 상태 요약 역할을 한다.

---

## 요약 — 5개 설계 결정 대응표

| 항목 | 절 |
|---|---|
| (1) 페이지/라우팅 구조 | §1 |
| (2) 단일 run 심층 뷰 컴포넌트 분해 | §2 |
| (3) 데이터 계층 ↔ UI 인터페이스 계약 | §3 |
| (4) shadcn/ui + Tailwind 활용 전략 | §4 |
| (5) 관찰 전용 + 새로고침 기반 최신성 보장 | §5 |
| (사용자 게이트 수정 요구) Wireframe | ## Wireframe |
