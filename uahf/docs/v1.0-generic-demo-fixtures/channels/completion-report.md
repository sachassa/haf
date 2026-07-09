# 완료 보고 — Generic 바인딩 실물 (BP-11, 결과 채널)

이 파일은 Worker가 산출한 완료 보고(02 §3.2-C 5필드)를 담은 텍스트 파일(레코드)이다 — 파일 기반 보고 채널의 환경 중립 실현(BP-11). 필드 정의의 정본은 specs/02-agent.md §3.2-C다. **이 보고는 Verify 통과 전 참고 입력일 뿐이며, 판정 근거가 아니다**(02 INV-4·§3.2-A — 검증 주체가 독립 판정).

## 완료 보고 (5필드)

- **artifacts:** `../artifacts/core-loop-summary-note.md` (1개).
- **self_check:** 위임 done 항목별 자체 점검 (CP1 — 최종 승인 아님):
  1. 핵심 루프 4단계 각각 1문장 이상 서술 — **충족**. 근거: artifact §1에 위임·구현·검증·승인 4단계가 각 1문장 이상으로 서술됨. 검사 범위: artifact §1 4개 불릿 전수.
  2. 위임 메시지 필수 필드 7종(from/to/task/input/output/done/context) 열거 포함 — **충족**. 근거: artifact §2에 7종이 번호 목록으로 전건 열거됨(constraints는 선택 필드로 구분 명시). 검사 범위: artifact §2 목록 1~7 전수.
  3. 파일 1개만 생성 — **충족**. 근거: output 지정 경로 1개(`../artifacts/core-loop-summary-note.md`)만 생성. 검사 범위: 이 구현 단계 산출 파일 목록.
- **failures:** 없음.
- **open_questions:** 없음.
- **verify_basis:** BP-2 로드 실증 — 구현 착수 시 Module Manifest(`../manifests/agent-module.manifest.md`) entrypoint를 통해 역할 정의 파일(`../roles/worker.md`)과 상위 규약(`../conventions/agent-conventions.md`)을 로드하고 역할 경계·공통 의무를 확인했다. artifact를 위임 done 3항목에 대조해 자체 점검(CP1)을 남겼다. 최종 판정은 독립 Verifier(CP2)와 Advisor 승인(CP3) 소관이다.
