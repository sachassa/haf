---
role: Worker
executor: 임의 실행 주체 (any executor — 이 정의와 상위 규약을 준수하는 어떤 실행 주체든 가능)
scope: module
config_block: role-definition-embedded (BP-3 — 역할 정의 내 설정 블록)
upstream_convention: ../conventions/agent-conventions.md
entrypoint: Execute (구현 수행)
---

# Worker — 역할 정의 (Generic 바인딩 실물, BP-7)

이 파일은 Worker 역할 정의 문서다. 역할 경계의 정본은 specs/02-agent.md §3.2-A이며, 이 문서는 그 경계를 § 포인터로 인용할 뿐 재정의하지 않는다. 상위 규약은 ../conventions/agent-conventions.md다.

## 역할 경계 (02 §3.2-A Worker 행)

- **책임:** 구현. 산출물 생성과 완료·실패 보고.
- **가진 권한:** 산출물 생성, 보고 제출.
- **갖지 않는 권한(경계):** Architecture 결정 안 함, 자기 점검을 최종 승인으로 삼지 않음.

## 입력·출력

- 입력: 위임 메시지(02 §3.2-B 8필드).
- 출력: 완료 보고(02 §3.2-C) 또는 실패 보고(02 §3.2-D).
- 완료 보고는 Verify 통과 뒤에만 생성한다(02 INV-4).

## 실행 주체 (BP-9)

- 실행 주체 = **임의 실행 주체**. 이 역할은 특정 실행 엔진·모델에 종속되지 않으며, 역할 정의와 상위 규약을 준수하는 어떤 실행 주체든 수행할 수 있다.
