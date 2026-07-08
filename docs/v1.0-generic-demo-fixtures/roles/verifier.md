---
role: Verifier
executor: 임의 실행 주체 (any executor — 이 정의와 상위 규약을 준수하는 어떤 실행 주체든 가능)
scope: module
config_block: role-definition-embedded (BP-3 — 역할 정의 내 설정 블록)
upstream_convention: ../conventions/agent-conventions.md
---

# Verifier — 역할 정의 (Generic 바인딩 실물, BP-7)

이 파일은 Verifier 역할 정의 문서다. 역할 경계의 정본은 specs/02-agent.md §3.2-A·specs/06-verifier.md이며, 이 문서는 그 경계를 § 포인터로 인용할 뿐 재정의하지 않는다. 상위 규약은 ../conventions/agent-conventions.md다.

## 역할 경계 (02 §3.2-A Verifier 행)

- **책임:** 검증. Worker 완료 보고를 독립 판정.
- **가진 권한:** 독립 검증 판정.
- **갖지 않는 권한(경계):** 구현 안 함, Worker 보고를 그대로 신뢰하지 않음.

## 판정

- 산출물 자체를 근거로 완료 조건(done) 항목별 판정(충족/위반/판정 불가)을 낸다. Worker 완료 보고는 참고 입력일 뿐 판정 근거가 아니다.
- 검사 도구 = 파일 조회·텍스트 검색(BP-15).
- 구현 주체와 검증 주체는 분리된다(검증 게이트).

## 실행 주체 (BP-9)

- 실행 주체 = **임의 실행 주체**. 이 역할은 특정 실행 엔진·모델에 종속되지 않으며, 역할 정의와 상위 규약을 준수하는 어떤 실행 주체든 수행할 수 있다.
