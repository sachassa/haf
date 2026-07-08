---
meta:
  id: pc-uahf-001
  schemaVersion: "1.0"
  instanceVersion: 1
  supersedes: null
intent: >-
  UAHF(Universal Agentic Harness Framework) — AI 비의존 에이전틱 하네스 프레임워크.
  계약 우선·문서 정본 설계로 6-Layer(Presentation~Adapter)+Memory Cross-cutting 구조와
  UAF 레벨 진입 파이프라인(Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF)을
  정의하고, 하네스 자신의 개발에 하네스를 적용(dogfooding)해 검증한다.
  지향(사용자 진술 2026-07-07): 실용화 — 형태 B 실행 호스팅 도입과 실제 외부 프로젝트 적용으로 실용성을 입증한다.
requirements:
  functional:
    - "Agent 역할 4종(Advisor·Planner·Worker·Verifier) 운용과 위임 8필드/완료 보고 5필드 프로토콜"
    - "Memory Record/Recall(단일 Port·index-first)·Lessons 재발 판정·승격 심사"
    - "Loop 사이클(CP1~CP3)·Workflow 분해 C1~C4/디스패치 R1~R4/병합 5단계·Verifier VT-1~5 독립 판정"
    - "Scaffold 설치(Project Template·Install Manifest)·Adapter Conformance(BP-1~17)"
    - "UAF 파이프라인: Entry Resolution(결정 테이블 8조합)·Project Discovery(Compiler)·Project Contract(Stable Contract)"
  quality:
    - "마일스톤 풀 프로토콜(Planner 초안→Advisor 채택→Wave 병렬→CP2 독립 검증→CP3→핸드오프→Baseline)"
    - "완료 보고 불신·산출물 직접 실측 독립 검증·거짓 완료 검출"
    - "Frozen spec 개정 규율(버전 상승+Revision History)·재발 판정 3분류(Novel/RecallGap/Recurrence)"
constraints:
  - "UAHF 정본 무수정 — UAF와의 접점은 Project Contract 하나(UAF-INV ①)"
  - "C-1(형태 A→B 전환에도 Core Contract 변경 0)·C-2·C-3(Core 경계 금지 토큰 0)"
  - "Core AI 의존 0 — 환경 의존은 Adapter 경계에만 격리"
  - "물리 데이터(memory-data/·loop-data/·discovery-data/) append-only"
  - "하네스 Bootstrap 상태 — 형태 A(문서·규약) 실현, 실행 코드 0"
risks:
  - "문서 규모·복잡도 증가 — 정본·계약 문서 증가에 따른 정합 유지 비용 급증 (사용자 진술)"
  - "형태 B 전환 복잡성 — 형태 A 규약과의 정합·원자성(OQ-M5-2 외 경계 분할 OQ 4건) 해소 난이도 (사용자 진술)"
  - "이월 개정 후보 누적(stale 계수·서수 표기 등 비차단 8+1건) — 방치 시 정합 부채화 (정본 실측)"
  - "E2E·마일스톤의 사용자 게이트 실시간 의존 — 승인·답변 대기 병목 (정본 실측)"
architectureDirection:
  decisions:
    - "6-Layer 스택 + Memory Cross-cutting Service·13 Core Component"
    - "4경계 물리 배치(core/runtime/module-dirs/adapters)·Adapter 격리(claude 완전 구현 + generic 최소 구현)"
    - "UAF 레벨 파이프라인은 UAHF 6-Layer 외부 — 접점은 Project Contract 하나"
    - "현 실현 = 형태 A(문서 절차·규약·관행)"
  open:
    - "형태 B 실행 호스팅의 경계 분할(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2) — DP-4 재상정 시"
    - "UAHF 측 Contract 정식 등재(uaf/specs/03 §3.5-C 확장 포인트)"
assumptionLedger: []
readiness:
  completeness: "필수 코어 필드 전건 충족 — id·schemaVersion·instanceVersion·Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger(빈 원장 — Ready 허용)"
  confidenceVector: { intent: 0.85, requirement: 0.80, constraint: 0.85, risk: 0.75, architecture: 0.90 }
  openQuestions:
    - "형태 B 전이(실행 호스팅 도입) 착수 시점"
    - "이월 개정 일괄(차기 개정 후보 8+1건) 처리 시점"
    - "Contract의 UAHF 정식 등재(03 §3.5-C) 채택 여부"
  userApproval: "사용자 승인 2026-07-07 — G2 Validating 게이트(brownfield-r001 events.jsonl seq 28 AnswerReceived[승인], T16)"
provenance:
  runId: r001
  eventLog: "framework/adapters/claude/discovery-data/events/brownfield-r001/"
  mode: brownfield
  policy: default-policy
---

# Project Contract — UAHF (Universal Agentic Harness Framework)

> 본 저장소 최초 Project Contract (Brownfield Full Discovery — /continue 최초 도입, 결정 테이블 행 6·D3 ②).
> 정본 스키마 = uaf/specs/03-project-contract.md §3.2 / 직렬화·저장 정본 = framework/adapters/claude/contract-binding.md §3·§4.2.

## Intent — 무엇을 왜

UAHF는 **AI 비의존 에이전틱 하네스 프레임워크**다. 특정 AI·환경에 결합되지 않는 계약(Core Contract)을 문서 정본으로 설계하고, 환경 의존은 Adapter 경계에 격리한다. 6-Layer + Memory 횡단 구조 위에 v1.1부터 UAF 레벨 진입 파이프라인(Entry → Discovery → Contract)을 신설했으며, 하네스 자신의 개발에 하네스를 적용(dogfooding)해 실증한다. **지향 = 실용화** — 형태 B 실행 호스팅 도입, 실제 외부 프로젝트 적용으로 실용성 입증(사용자 진술).

## Requirements — 무엇을 만족해야

기능: Agent 4종 운용·위임/보고 프로토콜·Memory·Loop·Workflow·Verifier·Scaffold·Conformance·UAF 파이프라인(front-matter functional 5항). 품질: 마일스톤 풀 프로토콜·독립 검증·Frozen 규율·재발 판정(quality 3항).

## Constraints — 무엇에 매여

UAHF 정본 무수정(접점 = Contract 하나)·C-1~C-3·Core AI 의존 0·append-only 데이터·Bootstrap 형태 A (front-matter 5항).

## Risks — 무엇이 어긋날 수 있나

문서 규모·복잡도 증가 / 형태 B 전환 복잡성 (이상 사용자 진술) / 이월 개정 후보 누적 / 사용자 게이트 실시간 의존 (이상 정본 실측) — front-matter 4항.

## Architecture Direction — 어떻게 구성

결정 4항(6-Layer+Memory·4경계·UAF 외부 파이프라인·형태 A) / 미결 2항(형태 B 경계 분할·정식 등재) — front-matter 참조.

## Readiness

Completeness 전건 충족 · Confidence Vector 전 차원 θ 충족 · 가정 0(빈 원장) · 사용자 승인 2026-07-07 → **Ready** (2축 판정, uaf/specs/02 §3.7).
