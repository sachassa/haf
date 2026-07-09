---
id: agent-worker-module
kind: Module
contract: agent-role
entrypoint: ../roles/worker.md
executor: 임의 실행 주체 (any executor)
serialization: 개방 표준 구조화 텍스트 (머리말 메타데이터 블록 + 본문)
---

# Module Manifest — Generic 바인딩 실물 (BP-1)

이 파일은 Module Manifest 서술자를 대상 환경의 서술자 포맷으로 직렬화한 실물이다(BP-1 — 서술자 필드를 담는 일반 구조화 텍스트 파일: **머리말 메타데이터 블록 + 본문**). Module 시스템 계약의 정본은 specs/01-runtime.md §3.1-A·§3.2-A이며, 이 Manifest는 그 계약을 재정의하지 않는다. Manifest 필드 정의는 specs/00-glossary.md §3.2-I(Module Manifest)·01 §3.2-A가 정본이다.

## 본문 (일반 구조화 텍스트)

- **id:** `agent-worker-module` — Module의 안정적 식별자.
- **kind:** `Module` — Runtime이 등록·해소·교체하는 기능 단위.
- **contract:** `agent-role` — 이 Module이 구현하는 계약(Agent 역할).
- **entrypoint:** `../roles/worker.md` — Module 정의를 로드해 해소하는 진입점(활성 역할 정의). 로더는 이 경로의 역할 정의 파일을 읽어 entrypoint를 해소한다(BP-2).
- **executor:** 임의 실행 주체 — 이 Module을 수행하는 실행 주체는 특정 엔진·모델에 강제되지 않는다(BP-9).
- **serialization:** 개방 표준 구조화 텍스트 직렬화 형식(머리말 메타데이터 블록 + 본문). 특정 직렬화 제품·형식을 강제하지 않는다.

이 Manifest는 서술자 포맷 직렬화(BP-1)와 entrypoint 해소 로더(BP-2)의 환경 중립 실물이다. 시연의 구현 단계에서 실행 주체가 이 Manifest의 entrypoint(`../roles/worker.md`)를 로드해 Worker 역할 정의를 해소한다.
