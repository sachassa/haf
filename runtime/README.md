# runtime — 하네스 실행 Layer

상태: v1.2.1 스텁 (구조 이동 산출물 — 완전 저술은 후속 트랙)
상위: Universal Agentic Framework (root README/ARCHITECTURE 참조)

## 역할
runtime은 하네스를 실제로 실행하는 Layer다. UAHF 구현체(`runtime/uahf/`)와 외부 하네스 연동 자리(`runtime/external/`)를 담는다. Planning이 확정한 Project Contract를 받아 실행한다. UAHF는 이 Runtime Layer의 구현체이며, 저장소 최상위 프로젝트가 아니다.

## 정본 포인터
정본: `runtime/uahf/` — 그 하위 `framework/`·`specs/` 및 `runtime/uahf/ARCHITECTURE.md`·`README.md`·`ROADMAP.md`가 UAHF 워크스페이스의 자기완결 정본이다. 참조 기준은 UAHF 서브루트(해석 a)로, uahf 내부 문서의 `framework/…`·`specs/…` 포인터는 그 서브루트 상대로 유효하다.

## 이 문서의 지위
스텁이다. 내용은 후속 트랙에서 완전 저술된다.
