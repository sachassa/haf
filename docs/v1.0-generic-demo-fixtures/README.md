# Generic Adapter 시연 픽스처 — 경계 고지

이 디렉터리는 Generic Adapter(2nd Adapter)의 **환경 중립 바인딩 값의 실물**을 담는 시연 픽스처다. framework/adapters/generic/generic-binding.md §2가 확정한 필수 13 바인딩 지점(BP)의 값을, 핵심 루프(위임→구현→검증→승인) 1사이클 실동작이 실제로 소비할 수 있는 파일·디렉터리·텍스트 실물로 배치한다(DP-V5 실동작 사이클).

## 정체성 제약 (DP-V6)

- 이 디렉터리 내부의 **모든 파일**은 특정 AI 이름·모델명·AI 벤더 제품/기능명을 **0건**으로 유지한다. Generic Adapter는 진정 환경 중립·추상이되 실행 가능한 실현이다(generic-binding.md §0·§4 DP-V6).
- 허용 표기: 일반 메커니즘(파일·디렉터리·텍스트·실행 세션·실행 주체·레코드)·개방 표준 포맷명·UAHF 자신의 계약 용어(Advisor/Planner/Worker/Verifier·Module·Manifest·Config·Bootstrap/Serve/Shutdown·Agent 등, specs/00-glossary.md 정본).
- 타 Adapter 경로는 명명하지 않는다 — 역할 기반 중립 참조만 사용한다(DP-V14).

## 경계

- 이 픽스처는 라이브 표면이 아니다. 실행 환경의 설정·정의를 오염하지 않으며, 오직 이 디렉터리 경계 안에 자기완결적으로 격리된다(11 §3.2-C 자기완결·물리 분리).
- 계약의 정본은 Frozen specs/11 §3(Adapter Interface·Conformance·구조 규격)·specs/02-agent.md §3(Agent 공통 계약)이다. 이 픽스처의 파일은 그 계약을 **재정의하지 않으며** § 포인터로만 참조한다.

## 구성 (환경 중립 바인딩 값 실물)

| 경로 | 실현하는 BP | 무엇인가 |
|---|---|---|
| `conventions/agent-conventions.md` | BP-8 | 상위 규약 문서 (공통 의무 02 §3.1 O1~O5 참조) |
| `conventions/orchestrator-entrypoint.md` | BP-8·BP-14 | 오케스트레이터 진입점 문서 (충돌 시 사람 보고 규칙 포함) |
| `roles/advisor.md`·`planner.md`·`worker.md`·`verifier.md` | BP-7·BP-9·BP-3 | 4역할 정의 문서 (실행 주체 = 임의 실행 주체, 설정 블록 포함) |
| `config/global-config.md`·`project-config.md` | BP-3 | 전역·프로젝트 스코프 설정 소스 |
| `manifests/agent-module.manifest.md` | BP-1 | Module Manifest 서술자 (머리말 메타데이터 블록 + 본문) |
| `channels/delegation-message.md` | BP-10 | 위임 메시지 파일 (호출 채널) |
| `channels/completion-report.md` | BP-11 | 완료 보고 파일 (결과 채널) |
| `artifacts/core-loop-summary-note.md` | 구현 산출 | 핵심 루프 4단계 요약 노트 (시연 artifact) |
| `reports/verification-report.md` | BP-13·BP-15 | 검증 리포트 파일 (독립 판정 산출) |
| `records/cycle-record.log` | BP-13 | 사이클 기록 파일 (append-only, 1행 = 1전이) |
| `records/approval-record.md` | BP-13 | 승인 기록 파일 |

내부 파일명·구조는 환경 중립 파일 시스템 규약으로만 지정했다. 시연 절차와 실측 대조는 docs/v1.0-generic-adapter-demo.md가 기록한다.
