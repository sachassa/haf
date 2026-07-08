# framework/adapters/ — Adapter Layer 경계 (자리)

이 디렉터리는 Adapter Layer의 경계다. Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이다 (structure.md §2, 01 §3.2-E 규칙 3, 01 §4.1). AI·환경 의존 요소는 전부 여기로 격리한다.

이 경계는 Core 경계(`framework/core/`·`framework/runtime/`)의 AI 비의존 불변에서 제외된다 — 여기가 격리 지점이며, 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 허용된다.

## 설치 시 배치 안내

설치 시 대상 실행 환경의 Adapter Binding 산출물을 `framework/adapters/<adapter>/` 아래에 배치한다. `<adapter>`는 구체 어댑터명(하위 디렉터리 이름)이며 해당 Adapter Binding 문서가 소유한다.

Claude Code 환경에서는 `framework/adapters/claude/`가 그 경계다. 이 경계의 바인딩 문서가 각 Core 계약(Runtime·Memory·Verifier·Loop·Workflow·확장·Scaffold)의 물리 실현을 소유한다.

## 경계 규칙

- Core/Adapter는 물리적으로 비중첩이다 (01 §3.2-E 규칙 3).
- 이식 시 이 Adapter 경계만 교체된다 — Core Contract(specs/01~13 §3)는 유지된다 (specs/11-adapters.md).
