# runtime — Architecture (하네스 실행 Layer)

상태: v1.2.1 스텁 (구조 이동 산출물 — 완전 저술은 후속 트랙)
상위: Universal Agentic Framework (root README/ARCHITECTURE 참조)

## 역할
runtime Layer의 내부 구조·경계를 규정한다. `uahf/`(구현체)와 `external/`(외부 하네스 연동)의 관계, Project Contract 수신 접점을 다룬다.

주의: 여기서 말하는 "runtime"(UAF 파이프라인의 실행 단계 Layer)과 UAHF 내부 6-Layer 중 하나인 "Runtime Layer"(`runtime/uahf/framework/runtime/`, 모듈 시스템·수명주기)는 **다른 축의 서로 다른 개념**이다. 경로 `runtime/uahf/framework/runtime/`에 "runtime"이 두 번 등장하지만 의미가 다르다.

## 정본 포인터
정본: `runtime/uahf/ARCHITECTURE.md` (UAHF 6-Layer 아키텍처 정본) 및 그 하위 `framework/`·`specs/`.

## 이 문서의 지위
스텁이다. 내용은 후속 트랙에서 완전 저술된다.
