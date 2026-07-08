---
meta:
  id: pc-uahf-quickstart-001
  schemaVersion: "1.0"
  instanceVersion: 1
  supersedes: null
intent: >-
  uahf-quickstart CLI — UAHF 설치 상태·하네스 상태를 점검해 주는 소형 CLI 도구
  (v1.0 dogfooding uahf-lessons CLI 계보). 성공 기준(사용자 진술 2026-07-07):
  UAHF 설치 프로젝트에서 명령 1번으로 설치 완전성·하네스 상태 요약을 출력하는
  "1명령 설치 진단" — 신규 사용자의 첫 점검 도구.
requirements:
  functional:
    - "설치 완전성 점검 — 설치본 필수 구성(규약 문서·Agent 정의·specs 등) 존재 대조"
    - "하네스 상태 표면화 — Bootstrap/Formal 상태·최신 핸드오프·마일스톤 요약 출력"
    - "데이터 계수 실측 — memory-data/·loop-data/ 등 물리 데이터 계수·store↔index 정합 점검"
    - "Contract 존재·버전 표시 — Project Contract 인스턴스 유무·최신 instanceVersion 표시(UAF 연계)"
  quality:
    - "읽기 전용 — 점검 대상을 수정하지 않는다"
    - "1명령 실행 — 단일 명령 호출로 전체 진단 완료"
    - "콘솔 출력 인코딩 명시 설정 — 한글 출력 안전(L-19 교훈 적용)"
constraints:
  - "Python 단일 파일 CLI"
  - "표준 라이브러리만 사용(외부 의존성 0)"
  - "점검 대상 무수정(읽기 전용)"
  - "콘솔 출력 인코딩 명시(UTF-8 재설정 — v1.0 실발생 결함 예방)"
risks:
  - "UAHF 정본·경로 구조 변경 시 CLI의 경로 전제 파손 — 대상 버전 추적 필요 (사용자 진술)"
  - "콘솔 인코딩(L-19 부류) — Windows 콘솔 한글 출력 UnicodeEncodeError, v1.0에서 실발생 (사용자 진술)"
architectureDirection:
  decisions:
    - "단일 파일 CLI(진입점 1개·서브커맨드 없이 1명령 진단)"
    - "읽기 전용 점검 — 파일 시스템 관측만, 대상 무수정"
    - "정본 경로 테이블 상수화 — 점검 대상 경로를 단일 테이블로 분리해 구조 변경 시 수정 지점 1곳으로 한정(리스크 ① 완화)"
  open:
    - "UAHF 버전별 경로 테이블 유지 전략(버전 감지 vs 수동 갱신)"
assumptionLedger: []
readiness:
  completeness: "필수 코어 필드 전건 충족 — id·schemaVersion·instanceVersion·Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger(빈 원장 — Ready 허용)"
  confidenceVector: { intent: 0.85, requirement: 0.80, constraint: 0.80, risk: 0.75, architecture: 0.75 }
  openQuestions:
    - "UAHF 버전별 경로 테이블 유지 전략"
  userApproval: "사용자 승인 2026-07-07 — G2 Validating 게이트(greenfield-r002 events.jsonl seq 27 AnswerReceived[승인], T16)"
provenance:
  runId: r002
  eventLog: "framework/adapters/claude/discovery-data/events/greenfield-r002/"
  mode: greenfield
  policy: default-policy
---

# Project Contract — uahf-quickstart CLI

> 신규 프로젝트 최초 Project Contract (순수 Greenfield — /new, 결정 테이블 행 1·P-C).
> 정본 스키마 = uaf/specs/03-project-contract.md §3.2 / 직렬화·저장 정본 = framework/adapters/claude/contract-binding.md §3·§4.1(소비 프로젝트 내 `.claude/project-contract/` — Scaffold 배치 소비 지점).

## Intent — 무엇을 왜

UAHF 설치 상태·하네스 상태를 점검하는 **소형 CLI**. 성공 기준 = **1명령 설치 진단** — 설치 프로젝트에서 명령 1번으로 설치 완전성과 하네스 상태 요약을 출력한다. 신규 사용자의 첫 점검 도구(사용자 진술).

## Requirements — 무엇을 만족해야

기능 4항: 설치 완전성 점검 · 하네스 상태 표면화 · 데이터 계수 실측 · Contract 존재/버전 표시. 품질 3항: 읽기 전용 · 1명령 · 인코딩 명시(front-matter 참조).

## Constraints — 무엇에 매여

Python 단일 파일 · 표준 라이브러리만 · 읽기 전용 · 인코딩 명시(front-matter 4항).

## Risks — 무엇이 어긋날 수 있나

정본 구조 변경 시 경로 전제 파손(버전 추적) · 콘솔 인코딩 L-19 부류(front-matter 2항 — 전부 사용자 진술).

## Architecture Direction — 어떻게 구성

결정 3항: 단일 파일 CLI · 읽기 전용 관측 · 경로 테이블 상수화. 미결 1항: 버전별 경로 테이블 유지 전략.

## Readiness

Completeness 전건 충족 · Confidence Vector 전 차원 θ 충족 · 가정 0(빈 원장) · 사용자 승인 2026-07-07 → **Ready** (2축 판정, uaf/specs/02 §3.7).
