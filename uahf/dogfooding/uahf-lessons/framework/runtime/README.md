# framework/runtime/ — Runtime Layer 경계 (자리)

이 디렉터리는 Runtime Layer의 경계다. Runtime 호스팅·모듈 시스템 계약의 **프로토콜 문서**를 담는다. 문서 본문은 AI 비의존·언어/툴체인 비의존을 유지한다 (structure.md §2·§5, 01 §3.2-E 규칙 2). 향후 실행 코드(형태 B)의 실현 경계이기도 하다.

## 설치 시 배치 안내

설치 시 spec 기준선(specs/)의 Runtime 프로토콜 인스턴스 문서를 이 경계에 배치한다. 기준선 구성:

- `module-manifest.md` — Module 등록 서술자 (01 §3.2-A 인스턴스).
- `module-registry.md` — 등록·해소·교체·해제 규칙 (01 §3.1-A 인스턴스).
- `lifecycle.md` — Bootstrap·Shutdown 수명주기 (01 §3.1-C 인스턴스).

Module 자기완결 구현 경계(`framework/{loop,memory,verifier,workflow,plugins}/` 등)는 각 Module의 spec이 소유하며, 설치 시 선택된 Module만 배치된다 (moduleSelection, 12 §3.3 INV-2, ARCHITECTURE 3.2 Modular).

## 불변 규칙

- 이 경계의 문서 본문에도 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (structure.md §5 C-3, 01 §3.3 INV-4). CK-6의 판정 대상이다.
- 실행 환경·AI 의존 실현은 Adapter Binding 경계(`framework/adapters/<adapter>/`)로 격리한다 (01 §3.2-E 규칙 3).
- Runtime Contract의 정본은 specs/01-runtime.md §3이다. 이 경계의 문서는 그 계약의 인스턴스이며 계약을 재정의하지 않는다.

이 안내 파일 자체도 AI 비의존을 유지한다.
