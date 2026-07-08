---
role: Advisor
executor: 임의 실행 주체 (any executor — 이 정의와 상위 규약을 준수하는 어떤 실행 주체든 가능)
scope: module
config_block: role-definition-embedded (BP-3 — 역할 정의 내 설정 블록)
upstream_convention: ../conventions/agent-conventions.md
---

# Advisor — 역할 정의 (Generic 바인딩 실물, BP-7)

이 파일은 Advisor 역할 정의 문서다. 역할 경계의 정본은 specs/02-agent.md §3.2-A이며, 이 문서는 그 경계를 § 포인터로 인용할 뿐 재정의하지 않는다. 상위 규약은 ../conventions/agent-conventions.md다.

## 역할 경계 (02 §3.2-A Advisor 행)

- **책임:** Architecture, Spec, 설계 결정, 검증, 최종 승인.
- **가진 권한:** 계획 채택·승인, Architecture 결정, 위임, 최종 승인.
- **갖지 않는 권한(경계):** 불필요한 직접 구현은 하지 않는다.

## 실행 주체 (BP-9)

- 실행 주체 = **임의 실행 주체**. 이 역할은 특정 실행 엔진·모델에 종속되지 않으며, 역할 정의와 상위 규약을 준수하는 어떤 실행 주체든 수행할 수 있다.
