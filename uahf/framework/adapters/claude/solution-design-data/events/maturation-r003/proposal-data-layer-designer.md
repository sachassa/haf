# Proposal — data-layer-designer (Propose 단계, maturation-r003)

> 역할: `data-layer-designer` (assessing-judgment.md 관심사 1: 데이터/파싱/도메인 모델 설계).
> 근거: Project Contract v1(pc-uahf-control-plane-001) `architectureDirection.decisions` 1항("계층 분리 — 파서/데이터 계층(UAHF 물리 형식 격리) ↔ 도메인 모델 ↔ UI 컴포넌트") 및 `requirements.functional` 4항·`risks` 중 데이터 형식 드리프트/Windows 경로·인코딩 항목을 구체 설계로 끌어올린다.
> 스코프: 관심사 1(데이터/파싱/도메인 모델)만 다룬다. UI/뷰 컴포넌트 분해는 `ui-view-designer` 역할의 산출물(별도 파일)에 위임하고 본 문서에서는 그 인터페이스 경계(§6)만 제시한다.

---

## 1. 도메인 모델 (타입/스키마)

원본 4개 데이터 소스(`events.jsonl`·`revisions.jsonl`·`artifacts.jsonl`·`logs/invoke-*.json`)를 UI 계층이 직접 알 필요가 없도록 다음 정규화 도메인 타입으로 수렴시킨다. 타입은 TypeScript 인터페이스로 표기하되, 실제로는 zod(또는 동등 런타임 스키마)로 이중 정의해 파싱 시점 검증에 사용한다(§5 참조).

```ts
// 공통 식별자
type RunId = string;          // orchestration-data/runs/<runId>
type Seq = number;            // events.jsonl 내 단조 증가 순번

// --- 이벤트 도메인 (events.jsonl → 판별 유니온) ---
interface EventBase {
  runId: RunId;
  seq: Seq;
  ts: string;           // ISO 8601, 원본이 비-ISO면 파서 계층에서 정규화
  raw: unknown;         // 원본 레코드 보존(디버그·드리프트 감사용, UI 미노출)
}

interface StepEvent extends EventBase {
  kind: "step";
  stepId: string;
  role?: string;
  status: "started" | "completed" | "failed";
}

interface GateEvent extends EventBase {
  kind: "gate";
  gateId: string;
  gateType: string;         // 예: G1~G5 등 Adapter 정의
  action: "opened" | "responded" | "resolved";
  state: GateState;         // §3 판별 로직의 산출
}

interface AnnotationEvent extends EventBase {
  kind: "annotation";
  targetId?: string;    // 주석이 참조하는 step/gate/artifact id(있는 경우)
  note: string;
}

type NormalizedEvent = StepEvent | GateEvent | AnnotationEvent;

// --- Revision 도메인 (revisions.jsonl) ---
interface Revision {
  runId: RunId;
  revisionId: string;
  targetArtifactId?: string;
  basis: string[];          // 인과 사슬 — 선행 revisionId/eventSeq 참조 목록
  createdAtSeq: Seq;
  raw: unknown;
}

// --- Artifact 도메인 (artifacts.jsonl) ---
type ApprovalState = "pending" | "approved" | "rejected" | "superseded";

interface Artifact {
  runId: RunId;
  artifactId: string;
  path: string;             // 정규화된 상대 경로(§5)
  derivedFrom: string[];    // 파생 사슬 — 선행 artifactId 목록(복수 소스 병합 허용)
  approvalState: ApprovalState;
  createdAtSeq: Seq;
  raw: unknown;
}

// --- 비용/토큰 도메인 (logs/invoke-*.json) ---
interface InvokeLog {
  runId: RunId;
  invocationId: string;     // 파일명(invoke-<id>.json)에서 도출
  model: string;
  tokensIn: number;
  tokensOut: number;
  costUsd: number;
  ts: string;
  raw: unknown;
}

// --- run 목록 요약(파생 뷰, 저장되지 않고 계산됨) ---
interface RunSummary {
  runId: RunId;
  status: "완주" | "정지" | "게이트 대기";
  lastSeq: Seq;
  pendingGateCount: number;
  totalCostUsd: number;
}
```

설계 의도: 4개 원본 파일은 각각 **독립적으로** 위 타입으로 매핑되고, `raw` 필드로 원본을 보존해 드리프트 발생 시 UI 재작업 없이 파서만 교체할 수 있게 한다(§6). `RunSummary`는 영속 타입이 아니라 나머지 4종을 조합해 요청 시점에 계산되는 파생 뷰다.

---

## 2. 이벤트 분류 판별 로직 (step / 게이트 / annotation)

Contract v1은 events.jsonl의 물리 형식을 "Adapter 재량(정본 아님)"으로 명시한다 — 즉 레코드에 항상 명시적 `kind` 필드가 있다고 가정할 수 없다. 따라서 분류는 2단계 전략을 취한다.

1. **1순위 — 명시 판별자 존재 시 신뢰**: 원본 레코드에 `type`/`kind`/`recordType` 등으로 해석 가능한 필드가 있고 그 값이 `{step, gate, annotation}` 중 하나로 매핑되면 그대로 채택한다.
2. **2순위 — 필드 시그니처 기반 추론**(명시 판별자 부재 시 폴백):
   - `gateId` 또는 `gateType` 필드 존재 → `GateEvent`
   - `stepId` 필드 존재(및 `gateId` 부재) → `StepEvent`
   - 위 둘 다 부재하고 자유 텍스트(`note`/`message`류 필드)만 존재 → `AnnotationEvent`
   - 어느 시그니처에도 매칭되지 않으면 `AnnotationEvent`로 강등하되 `raw`를 보존하고 파서 경고 카운터를 증가시킨다(무음 손실 금지 — §5 드리프트 대응과 동일 원칙).

분류 함수는 순수 함수 `classifyEvent(record: unknown): NormalizedEvent`로 구현하고, 판별 규칙 자체를 데이터 테이블(우선순위 배열)로 분리해 향후 Adapter가 필드명을 바꾸더라도 규칙 테이블만 갱신하면 되도록 한다(§6의 파서 격리 경계와 연결).

---

## 3. 게이트 pending vs 해소 상태 판별 로직

단일 게이트 레코드만으로는 상태를 알 수 없다 — 동일 `gateId`를 공유하는 **복수 이벤트**(예: opened → responded → resolved, 또는 Contract v1 provenance에 나타난 "UserResponded가 T8에 선행"과 같은 순서 제약)를 seq 순으로 접합해야 상태가 확정된다. 설계:

```ts
type GateState = "pending" | "resolved";

function reduceGateStates(events: GateEvent[]): Map<string, GateState> {
  const byGate = new Map<string, GateEvent[]>();
  for (const e of events) {           // events는 이미 seq 오름차순 정렬 가정
    const list = byGate.get(e.gateId) ?? [];
    list.push(e);
    byGate.set(e.gateId, list);
  }
  const result = new Map<string, GateState>();
  for (const [gateId, seq] of byGate) {
    const last = seq[seq.length - 1];
    result.set(gateId, last.action === "resolved" ? "resolved" : "pending");
  }
  return result;
}
```

원칙:
- **seq 순서가 유일한 진실 근원**이다 — 벽시계(`ts`)가 아닌 append-only `seq`로 정렬해 인과를 재구성한다(동시성/시계 왜곡에 영향받지 않도록).
- 동일 `gateId`의 마지막 레코드가 `action: "resolved"`가 아니면 무조건 `pending`으로 간주한다 — "opened만 있고 그 뒤가 없음"과 "responded까지만 있고 resolved 없음"을 모두 안전측(pending)으로 처리해, 미해소 게이트를 해소로 오판하는 사고를 구조적으로 차단한다(관찰 전용 요구사항과 정합 — 오판정으로 인한 잘못된 "완주" 표시 방지).
- 이 리듀서는 `RunSummary.pendingGateCount`·`RunSummary.status`(완주/정지/게이트 대기) 계산의 유일한 입력이 된다.

---

## 4. Revision basis 인과 사슬 · Artifact derivedFrom 파생 사슬 → 계보 그래프/트리 변환

`Revision.basis`와 `Artifact.derivedFrom`은 둘 다 **"파생물 → 원천"** 방향의 역방향 포인터(자식이 부모를 가리킴)다. 계보 뷰는 반대로 "원천 → 파생물"의 정방향 트리로 렌더해야 사람이 읽기 쉬우므로, 변환은 2단계다.

1. **그래프 구성(역방향 인접 리스트 → 정방향 인접 리스트로 역전)**
   ```ts
   function buildLineageGraph(revisions: Revision[], artifacts: Artifact[]) {
     const forward = new Map<string, string[]>();  // 원천id → 파생물id[]
     const nodeOf = new Map<string, Revision | Artifact>();
     for (const r of revisions) {
       nodeOf.set(r.revisionId, r);
       for (const parent of r.basis) {
         forward.set(parent, [...(forward.get(parent) ?? []), r.revisionId]);
       }
     }
     for (const a of artifacts) {
       nodeOf.set(a.artifactId, a);
       for (const parent of a.derivedFrom) {
         forward.set(parent, [...(forward.get(parent) ?? []), a.artifactId]);
       }
     }
     return { forward, nodeOf };
   }
   ```
2. **트리/DAG 렌더링 순회**: append-only 원장 전제상 사이클은 논리적으로 발생하지 않아야 하지만, 데이터 드리프트(§5) 가능성에 대비해 순회 시 **방문 집합(visited set)으로 사이클을 방어적으로 차단**한다 — 사이클이 감지되면 해당 노드에서 순회를 중단하고 파서 경고로 표면화하되 나머지 트리 렌더링은 계속한다(부분 렌더 우선, 전체 크래시 금지).
   - 루트 후보 = `forward`의 값(자식)으로 한 번도 등장하지 않는 노드(= 원천 노드, 즉 최초 artifact/revision).
   - 각 루트에서 DFS로 정방향 트리를 구성해 UI 계보 뷰(트리 컴포넌트)에 전달한다.

이 변환 함수는 도메인 계층에 위치하며(파서 계층이 아님) — 파서가 넘긴 정규화된 `Revision[]`/`Artifact[]`만 입력으로 받으므로 원본 파일 형식과 완전히 분리된다.

---

## 5. 읽기 전용 안전성 + Windows 경로/UTF-8/CRLF 리스크 완화 (파서 계층)

Contract v1 risks의 "데이터 형식 드리프트"(완화=파서 계층 격리)와 "Windows 경로/인코딩"(완화=UTF-8 강제·경로 정규화)을 파서 계층에서 다음과 같이 구체화한다.

**읽기 전용 보장(쓰기 조작 0)**
- 파서 모듈은 파일시스템 접근을 오직 하나의 내부 게이트웨이(`lib/data/fs-reader.ts`류)로 제한하고, 이 게이트웨이는 `readFile`/`readdir`/`stat` 등 읽기 API만 **재노출(re-export)**한다 — `writeFile`/`appendFile`/`unlink`/`rename`은 모듈에서 아예 import하지 않는다. 이는 런타임 검사가 아니라 모듈 경계 자체로 강제되는 정적 보장이다(코드 리뷰·정적 분석으로 "이 모듈에 쓰기 API import 0" 확인 가능).
- API route/RSC 계층도 이 게이트웨이만 통하도록 강제해, 상위 계층에서 실수로 fs 쓰기 API를 직접 호출할 경로 자체를 차단한다.

**Windows 경로 정규화**
- Contract v1 constraint("UAHF 저장소 경로를 env/config로 받아 서버 측에서 읽기 전용 직정독")에 따라 루트 경로는 설정값 1곳에서만 주입받는다.
- 모든 하위 경로 조합에 `path.join`/`path.resolve`(Windows 백슬래시·POSIX 슬래시 혼용 안전)를 사용하고, 최종 resolve된 경로가 설정된 `orchestration-data/runs/` 루트 하위에 있는지 검증한다(`..` 경로 순회로 루트 밖 파일에 접근하는 것을 방지 — runId가 파일명/URL 파라미터에서 유래할 수 있으므로 방어적 검증 필수).

**UTF-8/BOM**
- 모든 파일 읽기는 `encoding: "utf-8"` 명시. 한글 등 비-ASCII 콘텐츠(Contract v1 자체가 한글 문서)를 다루므로 인코딩 누락은 즉시 깨짐으로 나타난다.
- 파일 선두 BOM(`﻿`) 존재 시 파싱 전 스트립한다.

**CRLF**
- JSONL 라인 분리는 `\n` 단독 가정을 금지하고 `/\r?\n/`로 분리한다(Windows 저장 파일은 CRLF일 수 있음 — 이 프로젝트 자체의 기존 교훈["Git Bash CR 카운트 함정"]과 동일 계열의 리스크).
- 분리 후 각 라인 끝의 잔여 `\r`을 trim해 JSON.parse에 전달한다.

**드리프트 내성(파싱 실패 격리)**
- JSONL의 각 라인은 **개별적으로** `try/catch`로 파싱한다 — 한 줄의 형식 오류가 전체 파일/전체 run 뷰를 크래시시키지 않도록, 실패한 라인은 건너뛰고 파서 경고 목록에 축적해 UI에 "N개 레코드 파싱 실패" 형태로 노출한다(무음 손실 금지, 관찰 전용 요구사항과 정합 — 데이터가 있는데 안 보이는 것보다 부분 데이터+명시적 경고가 우월).

---

## 6. 파서 계층 격리 원칙 — 인터페이스 경계

Contract v1 architectureDirection 1항("파서/데이터 계층 ↔ 도메인 모델 ↔ UI 컴포넌트")을 물리 모듈 경계로 실현한다.

```
lib/data/
  parsers/
    events-parser.ts       # events.jsonl → NormalizedEvent[] (§2 분류 로직 포함)
    revisions-parser.ts    # revisions.jsonl → Revision[]
    artifacts-parser.ts    # artifacts.jsonl → Artifact[]
    invoke-log-parser.ts   # logs/invoke-*.json → InvokeLog[]
    fs-reader.ts           # 읽기 전용 게이트웨이(§5) — 유일한 fs 접근점
  domain/
    gate-state.ts          # §3 리듀서
    lineage.ts             # §4 그래프 변환
    run-summary.ts         # RunSummary 파생 계산
  types.ts                 # §1 도메인 타입 + zod 스키마(런타임 검증 쌍)
```

**경계 규칙**
1. `parsers/*`만 원본 파일의 물리 형식(필드명·중첩 구조·Adapter별 변형)을 안다. 이 디렉터리 밖 어떤 코드도 `raw` 필드 내부 구조를 들여다보지 않는다(디버그 표시 목적의 opaque 통과만 허용).
2. `parsers/*`의 공개 export는 오직 §1의 도메인 타입만이다 — 원본 JSON 형(shape)을 반환하는 함수는 모듈 밖으로 export하지 않는다.
3. `domain/*`(게이트 상태·계보 그래프·run 요약)은 도메인 타입만 입력받는다 — `parsers/*`를 import하지 않는다(단방향 의존: parsers → domain → UI).
4. UAHF 측 물리 형식이 바뀌면(드리프트 리스크 실현) 수정 범위는 원칙적으로 `parsers/*` 1개 파일에 한정된다 — `types.ts`의 도메인 스키마가 안정적으로 유지되는 한 `domain/*`·UI 컴포넌트는 무수정이다.
5. 각 파서의 출력은 `types.ts`의 zod 스키마로 즉시 검증한다(파싱 직후 1회) — 이는 "파서가 도메인 계약을 지켰는가"를 파서 자신에게 강제하는 계약 테스트 지점이며, 드리프트가 발생해 파서가 갱신되지 않은 채 방치되면 이 검증에서 조기 실패해 드러난다(무음 스키마 붕괴 방지).
6. `ui-view-designer` 역할(UI/뷰 컴포넌트 분해)은 `domain/*`의 출력 타입(`NormalizedEvent[]`, 게이트 상태 맵, 계보 트리, `RunSummary[]`)만을 props/data 계약으로 소비한다 — API route/RSC 경계에서 이 도메인 타입을 그대로 직렬화해 전달하며, UI 계층은 파서·원본 파일 존재를 알 필요가 없다.
