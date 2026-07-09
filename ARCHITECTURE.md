# Universal Agentic Framework — Architecture

상태: v1.2.1 스텁 (구조 이동 산출물 — 완전 저술은 후속 트랙)

## 이 문서의 범위
root ARCHITECTURE는 **Layer 관계와 전체 구조만** 설명한다. 각 Layer의 내부 아키텍처는 해당 Layer의 `ARCHITECTURE.md`가 정본이다.

## 두 개의 "Layer" 축 — 직교(구분 필수)
"Layer"라는 단어는 이 저장소에서 **서로 다른 두 축**에 쓰인다. 혼동을 막기 위해 명문으로 구분한다.

1. **UAF 최상위 구조 축 (파이프라인 단계)** — `entry` → `discovery` → `planning` → `runtime` 의 진행 축이다. `knowledge`는 이 축의 단계가 아니라 모든 단계가 Consult하는 공용 Base다(원칙 10). 이 축은 UAF 파이프라인(Entry Resolution → Project Discovery → Project Contract → UAHF 실행 → Execution)에 대응한다.

2. **UAHF 내부 6-Layer 축** — `runtime/uahf/` 안의 하네스 구현 축이다: Presentation → Workflow → Agent → Runtime → Core → Adapter (+ Memory cross-cutting). 이 6-Layer는 UAHF 내부 아키텍처(정본 `runtime/uahf/ARCHITECTURE.md`)에 속하며, UAF 최상위 구조 축과 **다른 축**이다. 최상위 Layer는 이 6-Layer 수를 늘리지 않는다.

주의: 경로 `runtime/uahf/framework/runtime/`에는 "runtime"이 두 번 나오지만 의미가 다르다 — 앞의 `runtime`은 UAF 파이프라인의 실행 단계 Layer, 뒤의 `runtime`은 UAHF 6-Layer 중 하나(모듈 시스템·수명주기)다.

## Layer 관계 개요
- `entry`·`discovery`·`planning`은 UAF 레벨 파이프라인이며, UAHF 6-Layer의 **외부**에 있다. UAF 파이프라인과 UAHF의 접점은 Project Contract 하나다(`planning` → `runtime/uahf`).
- `runtime/uahf`는 Project Contract를 받아 실행하는 UAHF 구현체다.
- `knowledge`는 전 Layer 공용 Knowledge Base다.

## 이 문서의 지위
스텁이다. 내용은 후속 트랙에서 완전 저술된다.
