---
meta:
  id: pc-uahf-control-plane-001
  schemaVersion: "1.0"
  instanceVersion: 2
  supersedes: 1
intent: >-
  uahf-control-plane — UAHF 하네스 운영을 관찰하는 웹 대시보드(UAHF Control Plane).
  UAHF의 첫 실제 신규 외부 소비 프로젝트이자 dogfooding 대상(사용자 지시 2026-07-13).
  MVP 성공 기준(사용자 진술): "단일 run 심층 뷰" — 실재 orchestration run 1건을 열어
  이벤트 타임라인·게이트·revision/artifact 계보·토큰/비용을 정확히 한 화면에 렌더.
  장기 비전(참고 자료 — 구현 명세 아님): 실시간 Control Plane(프로세스 플로우·게이트 해소·
  에이전트 상태·비용 모니터링, 레퍼런스 이미지 3장).
requirements:
  functional:
    - "run 목록 요약 — orchestration-data/runs/ 스캔, run별 상태(완주/정지/게이트 대기) 요약 테이블"
    - "이벤트 타임라인+게이트 — events.jsonl을 seq 순으로 렌더(step/게이트/annotation 구분), pending/해소 게이트 표시"
    - "revision·artifact 계보 — revisions.jsonl(basis 인과 사슬)·artifacts.jsonl(derivedFrom·approvalState 파생) 계보 뷰"
    - "토큰/비용 집계 — logs/invoke-*.json의 실측 토큰·cost_usd·모델별 집계 패널"
  quality:
    - "관찰 전용 — 쓰기 조작 0·UAHF 저장소 무수정(읽기 전용 접근)"
    - "새로고침 기반 최신성 — 페이지 로드/새로고침 시 최신 데이터(실시간 스트리밍 제외)"
    - "MVP 제외 목록 준수 — 쓰기 조작·실시간 스트리밍·ETA/velocity 예측·CPU/메모리 지표·멀티프로젝트 제외(사용자 승인 범위 경계 2026-07-13)"
constraints:
  - "Next.js + React + TypeScript 웹 애플리케이션, Tailwind CSS + shadcn/ui (사용자 진술)"
  - "데이터 접근 = UAHF 저장소 경로를 env/config로 받아 서버 측(API route/RSC)에서 읽기 전용 직정독 — 복사 0·UAHF 측 export 추가 0"
  - "데이터 소스 범위 = orchestration-data/runs/ 만(MVP)"
  - "실행 환경 = 로컬 Node (실측 2026-07-13: Node v24.15.0·npm 11.12.1 가용)"
  - "독립 디렉터리 C:\\my-claude-project\\uahf-control-plane\\ · 독립 git 저장소 — UAHF 저장소 밖"
risks:
  - "데이터 형식 드리프트 — orchestration-data 내부 형식은 Adapter 재량(정본 아님), UAHF 측 형식 변경 시 파서 파손 가능. 완화 = 파서 계층 격리 (사용자 진술)"
  - "범위 크리프 — 실시간/Control 기능 유혹으로 MVP 비대화. 완화 = 승인된 제외 목록 준수·확장은 구조로만 예비 (사용자 진술)"
  - "Windows 경로/인코딩 — 절대경로·한글 UTF-8·CRLF 특수성. 완화 = UTF-8 강제·경로 정규화 (사용자 진술)"
  - "사용자 게이트 의존 — 파이프라인 진행이 사용자 승인 대기에 종속(pc-uahf-001 v3 risk 동형) (사용자 진술)"
architectureDirection:
  decisions:
    - "계층 분리 — 파서/데이터 계층(UAHF 물리 형식 격리) ↔ 도메인 모델 ↔ UI 컴포넌트"
    - "MVP = 읽기 전용 파생 뷰(새로고침 기반) — append-only 원장(events/revisions/artifacts)의 파생 렌더링"
    - "확장 경로 예비 — 향후 실시간(polling/SSE)·Control(게이트 해소 조작)은 계층 교체/추가로 도입 가능한 구조(MVP에서 인프라 선구현 금지)"
    - "도메인 모델 정규화 — events.jsonl·revisions.jsonl·artifacts.jsonl·logs/invoke-*.json을 판별 유니온 NormalizedEvent(StepEvent|GateEvent|AnnotationEvent)·Revision·Artifact·InvokeLog·파생 RunSummary 타입으로 수렴(TS 인터페이스 + zod 스키마 이중 정의, raw 필드로 원본 보존) (maturation-r003 확정)"
    - "이벤트 분류 판별 — 명시 판별자(type/kind/recordType) 우선 채택, 부재 시 필드 시그니처 추론(gateId→gate, stepId→step, 그 외→annotation 강등+파서 경고)으로 폴백하는 classifyEvent 함수 (maturation-r003 확정)"
    - "게이트 상태 판별 — reduceGateStates(events): Map<gateId, \"pending\"|\"resolved\">, seq를 유일한 진실 근원으로 삼아 동일 gateId의 마지막 레코드가 resolved가 아니면 무조건 pending으로 안전측 처리 (maturation-r003 확정)"
    - "계보 그래프/트리 변환 — buildLineageGraph(역방향 basis/derivedFrom 포인터 → 정방향 인접 리스트)와 toLineageTree(루트 탐지 + DFS 트리화, 사이클 방어)를 domain/lineage.ts가 소유 (maturation-r003 확정)"
    - "모델별 비용 집계 — domain/cost-aggregate.ts의 aggregateCosts(InvokeLog[]): CostAggregate(byModel 소계 + 전체 합계)를 신설, CostSummaryCards가 이를 소비하고 CostBreakdownTable은 InvokeLog[] 원본을 그대로 소비 (maturation-r003 확정)"
    - "모듈 경계 및 단방향 의존 — lib/data/{parsers,domain}/ + types.ts, parsers→domain→app(UI) 단방향 의존 고정. parsers/*만 원본 물리 형식을 알고 공개 export는 도메인 타입만; domain/*은 parsers/*를 import하지 않음; 드리프트 시 수정 범위는 parsers/* 1개 파일(+필요시 types.ts)로 국한 (maturation-r003 확정)"
    - "읽기 전용 4중 보장 — fs-reader.ts(쓰기 API import 0 게이트웨이) + 경로 정규화(루트 이탈 방지) + RSC 서버 전용 실행(클라이언트 fs 접근 수단 부재) + API route 미생성(mutation 수신 엔드포인트 부재) + force-dynamic(캐시 배제) (maturation-r003 확정)"
    - "UI 라우팅 — Next.js App Router 2라우트: app/page.tsx(목록, RunSummary[]) · app/runs/[runId]/page.tsx(심층 뷰, 4패널 통합), 각자 loading.tsx 보유 (maturation-r003 확정)"
    - "UI 컴포넌트 분해 — RunDetailPage가 RunHeader·EventTimelinePanel(+ParserWarningAlert)·LineagePanel(재귀 LineageTreeNode)·CostPanel(CostSummaryCards+CostBreakdownTable) 4패널을 독립 데이터 인자로 조합 (maturation-r003 확정)"
    - "데이터~UI 인터페이스 계약 — RSC(app/page.tsx·app/runs/[runId]/page.tsx)가 domain/* 함수를 직접 await 호출, API route는 MVP에서 미생성(확장 시 app/api/runs/[runId]/route.ts를 domain/* 재사용으로 신설 가능하도록 경계만 예비) (maturation-r003 확정)"
    - "shadcn/ui 매핑 — Table(목록·비용 상세)·Badge(상태·게이트·승인 상태)·ScrollArea+Tailwind(타임라인)·Collapsible(계보 트리 재귀)·Card(비용 요약)·Alert(파싱 경고)·Skeleton(로딩) (maturation-r003 확정)"
  open:
    - "실시간 갱신 메커니즘 선택(polling vs SSE vs 파일 워처) — MVP 밖·확장 시 결정"
    - "Control 기능(게이트 해소 등 쓰기 1종) 도입 시점·권한 경계 — MVP 밖"
assumptionLedger: []
readiness:
  completeness: "필수 코어 필드 전건 충족 — id·schemaVersion·instanceVersion·Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger(빈 원장 — Ready 허용)"
  confidenceVector: { intent: 0.85, requirement: 0.80, constraint: 0.75, risk: 0.75, architecture: 0.80 }
  openQuestions:
    - "실시간 갱신 메커니즘 선택(확장 시)"
    - "Control 기능 도입 시점·권한 경계(확장 시)"
  userApproval: "<미확정 — 사용자 승인 대기>"
provenance:
  runId: r003
  eventLog: "uahf/framework/adapters/claude/discovery-data/events/greenfield-r003/ (UAHF 저장소 내)"
  mode: greenfield
  policy: default-policy
  terminal: "<미확정 — 종결 상태 대기>"
---

# Project Contract — uahf-control-plane (UAHF Control Plane / Dashboard)

> ⚠️ CANDIDATE(미발행) — 사용자 승인 전 후보 문면.

> 신규 프로젝트 최초 Project Contract (순수 Greenfield — /new, 결정 테이블 행 1·P-C)의 성숙 후보(v1 → v2, maturation-r003).
> 정본 스키마 = planning/specs/03-project-contract.md §3.2 / 직렬화·저장 정본 = uahf/framework/adapters/claude/contract-binding.md §3·§4.1(소비 프로젝트 내 `.claude/project-contract/` — Scaffold 배치 소비 지점). 두 정본 모두 UAHF 저장소 소재.

## Intent — 무엇을 왜

UAHF 하네스 운영을 관찰하는 **웹 대시보드**. UAHF의 **첫 실제 신규 외부 소비 프로젝트**이자 dogfooding 대상 — UAHF가 자신의 파이프라인(Entry→Discovery→성숙→Orchestration 구현)으로 이 프로젝트를 생성하는 것을 검증한다. MVP 성공 기준 = **단일 run 심층 뷰**(타임라인·게이트·계보·비용 한 화면). 장기 비전 = 실시간 Control Plane(참고 자료·구현 명세 아님).

## Requirements — 무엇을 만족해야

기능 4항: run 목록 요약 · 이벤트 타임라인+게이트(seq 정렬) · revision/artifact 계보 · 토큰/비용 집계. 품질 3항: 관찰 전용(UAHF 무수정) · 새로고침 최신성 · MVP 제외 목록 준수(front-matter 참조).

## Constraints — 무엇에 매여

Next.js/React/TS·Tailwind+shadcn/ui · 읽기 전용 직정독(env 경로·복사 0) · orchestration runs만 · 로컬 Node(v24 실측) · 독립 디렉터리/독립 git(front-matter 5항).

## Risks — 무엇이 어긋날 수 있나

데이터 형식 드리프트(파서 격리 완화) · 범위 크리프(제외 목록 준수) · Windows 경로/인코딩(UTF-8 강제) · 사용자 게이트 의존(front-matter 4항 — 전부 사용자 진술).

## Architecture Direction — 어떻게 구성

**v1 원 결정 3항**(무수정 유지): 계층 분리(파서 ↔ 도메인 ↔ UI) · 읽기 전용 파생 뷰 · 확장 경로 예비(인프라 선구현 금지).

**maturation-r003 신규 확정 11항**(Solution Design 성숙 run — Propose[data-layer-designer·ui-view-designer] → Reconcile → Review, reconciling-record.md 통합 아키텍처 반영): 도메인 모델 정규화(NormalizedEvent/Revision/Artifact/InvokeLog/RunSummary, TS+zod 이중 정의) · 이벤트 분류 판별(classifyEvent, 명시 판별자 우선+필드 시그니처 폴백) · 게이트 상태 판별(reduceGateStates, seq 기반 안전측 pending 처리) · 계보 그래프/트리 변환(buildLineageGraph+toLineageTree, domain/lineage.ts) · 모델별 비용 집계(aggregateCosts, domain/cost-aggregate.ts 신설) · 모듈 경계·단방향 의존(parsers→domain→app) · 읽기 전용 4중 보장(fs-reader.ts+경로 정규화+RSC 서버 전용+API route 미생성+force-dynamic) · UI 라우팅(App Router 2라우트) · UI 컴포넌트 분해(RunHeader·EventTimelinePanel·LineagePanel·CostPanel 4패널) · 데이터~UI 인터페이스 계약(RSC 직접 await, API route MVP 미생성) · shadcn/ui 매핑. 전체 목록은 front-matter `architectureDirection.decisions` 참조.

**미결 2항**(v1과 동일, 이번 성숙 run 범위 밖 — 변경 없음): 실시간 메커니즘 · Control 도입 시점(전부 MVP 밖).

## Readiness

Completeness 전건 충족 · Confidence Vector 전 차원 θ 충족(v1과 동일 벡터 — 이번 성숙 run은 architectureDirection만 확장하며 confidence 재산정은 별도 게이트) · 가정 0(빈 원장) · 사용자 승인 = **<미확정 — 사용자 승인 대기>**(본 candidate 문면은 미발행 후보이며, 이 필드는 사용자가 v2를 승인하는 시점에 확정된다) → readiness 판정 보류(2축 판정, discovery/specs/02 §3.7 — completeness·confidence는 충족했으나 userApproval 미확정이므로 아직 Ready 선언 불가).
