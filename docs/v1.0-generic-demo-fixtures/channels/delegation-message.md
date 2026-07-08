# 위임 메시지 — Generic 바인딩 실물 (BP-10, 위임 채널)

이 파일은 위임 메시지(02 §3.2-B 8필드)를 담은 텍스트 파일(레코드)이다. 대상 실행 주체(Worker)가 이 파일을 읽어 착수한다 — 파일 기반 위임 채널의 환경 중립 실현(BP-10). 필드 정의의 정본은 specs/02-agent.md §3.2-B다.

## 위임 (8필드)

- **from:** Advisor
- **to:** Worker
- **task:** 픽스처 내 소형 문서 artifact 1건(핵심 루프 4단계 요약 노트) 작성
- **input:** 상위 규약 문서·역할 정의 문서(픽스처 내) — `../conventions/agent-conventions.md`, `../roles/worker.md`
- **output:** 픽스처 내 artifact 파일 1개 — `../artifacts/core-loop-summary-note.md`
- **done:**
  1. 핵심 루프 4단계(위임→구현→검증→승인) 각각 1문장 이상 서술
  2. 위임 메시지 필수 필드 7종(from/to/task/input/output/done/context) 열거 포함
  3. 파일 1개만 생성
- **context:** 픽스처 상위 규약(`../conventions/agent-conventions.md`)·역할 정의(`../roles/worker.md`)
- **constraints:** 픽스처 밖 무접촉

이 위임은 사이클 기록 파일(`../records/cycle-record.log`) seq 1에 전이로 기록된다(actor = Advisor).
