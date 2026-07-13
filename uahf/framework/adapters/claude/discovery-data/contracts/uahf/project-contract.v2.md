---
meta:
  id: pc-uahf-001
  schemaVersion: "1.0"
  instanceVersion: 2
  supersedes: 1
intent: >-
  UAHF(Universal Agentic Harness Framework) — AI 비의존 에이전틱 하네스 프레임워크.
  계약 우선·문서 정본 설계로 6-Layer(Presentation~Adapter)+Memory Cross-cutting 구조와
  UAF 레벨 진입 파이프라인(Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF)을
  정의하고 — Project Contract 요소 내부에는 Ready 인스턴스 vN을 복잡도에 따라 superseding v(N+1)로
  성숙시키는 Solution Design 루프가 있다(파이프라인 6요소 불변·루트 §2.2·정본 planning/specs/04) —,
  하네스 자신의 개발에 하네스를 적용(dogfooding)해 검증한다.
  지향(사용자 진술 2026-07-07): 실용화 — 형태 B 실행 호스팅 도입과 실제 외부 프로젝트 적용으로 실용성을 입증한다.
requirements:
  functional:
    - "Agent 역할 4종(Advisor·Planner·Worker·Verifier) 운용과 위임 8필드/완료 보고 5필드 프로토콜"
    - "Memory Record/Recall(단일 Port·index-first)·Lessons 재발 판정·승격 심사"
    - "Loop 사이클(CP1~CP3)·Workflow 분해(Decompose 완료 조건 3건·reason 4종)/디스패치 R1~R4/병합 5단계·Verifier VT-1~5 독립 판정"
    - "Scaffold 설치(Project Template·Install Manifest)·Adapter Conformance(BP-1~17)"
    - "UAF 파이프라인: Entry Resolution(결정 테이블 8조합)·Project Discovery(Compiler)·Project Contract(Stable Contract)·Solution Design(성숙 — Ready vN → superseding v(N+1), 정본 planning/specs/04)"
  quality:
    - "마일스톤 풀 프로토콜(Planner 초안→Advisor 채택→Wave 병렬→CP2 독립 검증→CP3→핸드오프→Baseline)"
    - "완료 보고 불신·산출물 직접 실측 독립 검증·거짓 완료 검출"
    - "Frozen spec 개정 규율(버전 상승+Revision History)·재발 판정 3분류(Novel/RecallGap/Recurrence)"
constraints:
  - "UAHF 정본 무수정 — UAF와의 접점은 Project Contract 하나(UAF-INV ①)"
  - "C-1(형태 A→B 전환에도 Core Contract 변경 0)·C-2·C-3(Core 경계 금지 토큰 0)"
  - "Core AI 의존 0 — 환경 의존은 Adapter 경계에만 격리"
  - "물리 데이터(memory-data/·loop-data/·discovery-data/·solution-design-data/) append-only"
  - "하네스 Bootstrap 상태 — 형태 A(문서·규약) 실현, 실행 코드 0"
risks:
  - "문서 규모·복잡도 증가 — 정본·계약 문서 증가에 따른 정합 유지 비용 급증 (사용자 진술)"
  - "형태 B 전환 복잡성 — 형태 A 규약과의 정합·원자성(OQ-M5-2 외 경계 분할 OQ 4건 + Solution Design 실행 호스팅[v1.4 합류]) 해소 난이도 (사용자 진술)"
  - "이월 개정 후보 누적(라벨 결함·bare § 접두 미부기·stale 표기·자기 불일치 등 비차단 7건 — v1.3 §6 실측: 부수 검출 4 + W2 CP2 관찰 3) — 방치 시 정합 부채화. 일부는 v1.4 W3(discovery-data 미존재 계열)·maturation-r001(Workflow 'C1~C4' 라벨)에서 정정 진행 (정본 실측)"
  - "E2E·마일스톤의 사용자 게이트 실시간 의존 — 승인·답변 대기 병목 (정본 실측)"
architectureDirection:
  decisions:
    - "6-Layer 스택 + Memory Cross-cutting Service·13 Core Component"
    - "최상위 5-Layer 물리 구성(entry/·discovery/·planning/·uahf/·knowledge/ — v1.2.1)에서 UAHF는 uahf/ 아래 Runtime Layer 구현이며, 그 내부는 4경계 물리 배치(core/runtime/module-dirs/adapters)·Adapter 격리(claude 완전 구현 + generic 최소 구현)를 유지한다"
    - "UAF 레벨 파이프라인은 UAHF 6-Layer 외부 — 접점은 Project Contract 하나. Project Contract 요소는 planning/ Layer가 이중 책임(스키마 소유 + Solution Design 성숙 활동 소유)으로 소유하며, 성숙은 요소 내부 루프(Ready vN → superseding v(N+1))로 파이프라인 요소 수를 늘리지 않는다(6요소 불변)"
    - "현 실현 = 형태 A(문서 절차·규약·관행)"
  open:
    - "형태 B 실행 호스팅의 경계 분할(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2 + Solution Design 실행 호스팅 — 04 §3.9·solution-design-binding §6) — DP-4 재상정 시"
    - "UAHF 측 Contract 정식 등재(planning/specs/03 §3.5-C 확장 포인트)"
    - "step 기반 실행기 계열(Script Executor·Step Runtime·fresh context·Retry/Resume/Blocked·Progress·Git automation) = UAHF Execution/Runtime 진화 축 — 04 §3.9 연결만·별도 분석 트랙 후보(설계 0)"
assumptionLedger: []
readiness:
  completeness: "필수 코어 필드 전건 충족 — id·schemaVersion·instanceVersion·Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger(빈 원장 — Ready 허용)"
  confidenceVector: { intent: 0.85, requirement: 0.80, constraint: 0.85, risk: 0.75, architecture: 0.90 }
  openQuestions:
    - "형태 B 전이(실행 호스팅 도입) 착수 시점 — v1.3/v1.4는 형태 A 유지(Solution Design Adapter Binding 신설·dogfooding E2E 형태 A)·형태 B 미착수"
    - "이월 개정 일괄(차기 개정 후보 7건 — v1.3 §6 실측; 일부 v1.4 W3·maturation-r001 정정 진행) 처리 시점"
    - "Contract의 UAHF 정식 등재(planning/specs/03 §3.5-C 확장 포인트) 채택 여부 — 미채택 유지"
  userApproval: "사용자 승인 2026-07-13 — Solution Design Validating 게이트(maturation-r001 events.jsonl seq 7 UserResponded[승인], T8)"
provenance:
  maturation:
    runId: maturation-r001
    eventLog: "framework/adapters/claude/solution-design-data/events/maturation-r001/"
    baseline: 1
    policy: default-policy
    terminal: Matured
---

# Project Contract — UAHF (Universal Agentic Harness Framework)

> 성숙 재발행 인스턴스 v2 — Solution Design 성숙 경로(maturation-r001) 산출. supersedes = v1(문면 불변 보존·03 §3.4 Contract Maturation·PC-INV 9).
> 정본 스키마 = planning/specs/03-project-contract.md §3.2 / 직렬화·저장 정본 = framework/adapters/claude/contract-binding.md §3·§4.2 / 성숙 단계 정본 = planning/specs/04-solution-design.md / 성숙 실행 메타 = framework/adapters/claude/solution-design-data/events/maturation-r001/.

## Intent — 무엇을 왜

UAHF는 **AI 비의존 에이전틱 하네스 프레임워크**다. 특정 AI·환경에 결합되지 않는 계약(Core Contract)을 문서 정본으로 설계하고, 환경 의존은 Adapter 경계에 격리한다. 6-Layer + Memory 횡단 구조 위에 v1.1부터 UAF 레벨 진입 파이프라인(Entry → Discovery → Contract)을 신설했으며, v1.3부터 Project Contract 요소 내부에 Solution Design 성숙 루프(Ready vN → superseding v(N+1), 정본 planning/specs/04)를 신설했다 — 파이프라인 6요소 불변. 하네스 자신의 개발에 하네스를 적용(dogfooding)해 실증한다. **지향 = 실용화** — 형태 B 실행 호스팅 도입, 실제 외부 프로젝트 적용으로 실용성 입증(사용자 진술).

## Requirements — 무엇을 만족해야

기능: Agent 4종 운용·위임/보고 프로토콜·Memory·Loop·Workflow·Verifier·Scaffold·Conformance·UAF 파이프라인(front-matter functional 5항). 품질: 마일스톤 풀 프로토콜·독립 검증·Frozen 규율·재발 판정(quality 3항).

## Constraints — 무엇에 매여

UAHF 정본 무수정(접점 = Contract 하나)·C-1~C-3·Core AI 의존 0·append-only 데이터·Bootstrap 형태 A (front-matter 5항).

## Risks — 무엇이 어긋날 수 있나

문서 규모·복잡도 증가 / 형태 B 전환 복잡성 (이상 사용자 진술) / 이월 개정 후보 누적 / 사용자 게이트 실시간 의존 (이상 정본 실측) — front-matter 4항.

## Architecture Direction — 어떻게 구성

결정 4항(6-Layer+Memory·최상위 5-Layer 내 4경계·UAF 외부 파이프라인+planning 이중 책임·형태 A) / 미결 3항(형태 B 경계 분할·정식 등재·Execution/Runtime 진화 축) — front-matter 참조.

## Readiness

Completeness 전건 충족 · Confidence Vector 존치(전 차원 θ 충족 — Discovery 산출 기록 승계·성숙 run은 Confidence Model 미구동) · 가정 0(빈 원장) · 사용자 승인 2026-07-13(T8 게이트) → **성숙 인스턴스 v2** (Contract Maturation — 03 §3.4·정본 planning/specs/04).
