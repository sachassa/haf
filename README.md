# Universal Agentic Framework (UAF)

상태: v1.2.1 스텁 (구조 이동 산출물 — 완전 저술은 후속 트랙)

## 개요
Universal Agentic Framework(UAF)는 에이전트 기반 프로젝트를 진입부터 실행까지 관통하는 Layer 중심 프레임워크다. 각 Layer는 독립적으로 사용할 수 있고, 자신의 `.claude/`(override)·`README`·`ARCHITECTURE`·`ROADMAP`를 가진다. 최상위 `.claude/`는 Global Default다.

## 구성
- `entry/` — 진입 / Entry Resolution Layer
- `discovery/` — Project Discovery Layer
- `planning/` — Project Contract / 설계 Layer
- `uahf/` — 하네스 실행 Layer (UAHF 구현체)
- `knowledge/` — 공용 Knowledge Base (Layer 아님. 모든 Layer가 Consult)

UAHF는 저장소 최상위 프로젝트가 아니라 하나의 Layer(하네스 실행)다. UAHF 정본은 `uahf/`(그 하위 `uahf/framework/`·`uahf/specs/` 및 `README`·`ARCHITECTURE`·`ROADMAP`)에 있다.

## 정본 포인터
- 전체 구조: root `ARCHITECTURE.md`
- 전체 로드맵: root `ROADMAP.md`
- UAHF 하네스: `uahf/README.md`

## 이 문서의 지위
스텁이다. 내용은 후속 트랙에서 완전 저술된다.
