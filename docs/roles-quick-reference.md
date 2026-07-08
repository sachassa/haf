# docs/roles-quick-reference — UAHF 역할 빠른 참조

근거: specs/02-agent.md §3.2-A (역할 경계 정본), AGENT.md (Planner 조항 포함), 검증 통과 agent 역할 정의 4개
정본: specs/02-agent.md §3 (역할 계약), 특히 §3.2-A (역할 경계 표)
상위 규약: AGENT.md

---

# 0. 이 문서의 위치

**정본은 specs/02-agent.md다. 이 문서는 사람용 한 장 요약이다.**

역할 경계·메시지 필드·불변 규칙의 정본은 specs/02-agent.md가 소유한다.

이 문서는 그 계약을 요약하고, 상세는 § 포인터로 연결한다.

이 문서는 다음을 하지 않는다.

- 02의 역할 경계·메시지 필드를 재정의·확장하지 않는다. § 포인터로 참조만 한다.
- 새 용어를 만들지 않는다. 용어 정본은 specs/00-glossary.md다.
- 단계 전이(03 소관)·검증 판정 기준(06 소관)·작업 분해(07 소관)를 정의하지 않는다.

충돌이 발견되면 이 문서를 정본으로 삼지 않는다. 02를 따르고 Advisor에게 보고한다.

**구성.** §1~§3은 AI 비의존 역할 계약 요약이다 (Core Contract — 02 §3). §4는 실행 환경 바인딩이다 (02 §4.1). Core 섹션(§1~§3, §5)에는 특정 AI 모델명·제품 기능명이 등장하지 않는다 (02 INV-7, DoD-3).

**포인터 표기.** 별도 표기가 없으면 `02 §…`=specs/02-agent.md, `03 §…`=specs/03-loop.md, `06 §…`=specs/06-verifier.md, `07 §…`=specs/07-workflow.md, `Glossary §…`=specs/00-glossary.md.

---

# 1. 역할 경계 (02 §3.2-A)

UAHF는 4개 Agent 역할로 작업을 수행한다 (Glossary §3.2-E).

역할 분담 기준: Architecture 결정 = Advisor, 구현 = Worker, 검증 = Verifier (AGENT.md Delegation).

| 역할 | 책임 | 가진 권한 | 갖지 않는 권한 (경계) |
|---|---|---|---|
| Advisor | Architecture·Spec·설계 결정, 검증, 최종 승인 | 계획 채택·승인, Architecture 결정, 위임, 최종 승인 | 불필요한 직접 구현은 하지 않는다 |
| Planner | Advisor 위임 하에 구현 계획·작업 분해 초안 작성 | 초안 작성·제안 | 계획 채택·승인 권한 없음, Architecture 결정 권한 없음 |
| Worker | 구현 — 산출물 생성과 완료·실패 보고 | 산출물 생성, 보고 제출 | Architecture 결정 안 함, 자기 점검을 최종 승인으로 삼지 않음 |
| Verifier | 검증 — Worker 완료 보고를 독립 판정 | 독립 검증 판정 | 구현 안 함, Worker 보고를 그대로 신뢰하지 않음 |

Planner 초안 범위 (AGENT.md Delegation): 작업 계획 · 작업 분해 · Wave 설계 · Worker 브리프(02 §3.2-B 위임 메시지 초안) · 병렬 작업 계획. 모두 초안(draft)이며, 계획 채택·최종 승인·정책 변경은 Advisor 소관이다 (AGENT.md, 02 INV-3).

---

# 2. 역할별 입력·출력

역할 계약의 표준 입력은 위임 메시지, 표준 출력은 보고다 (02 §3.1). Advisor는 예외적으로 위임을 **발신**하고 보고를 **수신·승인**하는 주체다 (02 §3.2-A 위임·최종 승인 권한, §3.1).

| 역할 | 입력 | 출력 |
|---|---|---|
| Advisor | 사용자 지시·상위 규약(Architecture 등); 수신하는 완료 보고(02 §3.2-C)·실패 보고(02 §3.2-D) | 위임 메시지 발신(02 §3.2-B); 최종 승인/반려 판정(§3 검증 게이트 CP3) |
| Planner | Advisor의 위임 메시지(02 §3.2-B) | 계획·분해·Wave 초안(Advisor 채택 대기); 완료 보고(02 §3.2-C) 또는 실패 보고(02 §3.2-D) |
| Worker | 위임 메시지(02 §3.2-B) | 완료 보고(02 §3.2-C) 또는 실패 보고(02 §3.2-D) |
| Verifier | 판정 대상 = 산출물 + 대조 기준(criteria); 참고로 Worker 완료 보고 | 검증 리포트(06 §3.2-A); 판정 불능 시 연산 실패 보고(02 §3.2-D) |

메시지 필수 필드 (정본: 02 §3.2-B/C/D):

- 위임 메시지: `from`·`to`·`task`·`input`·`output`·`done`·`context` (`constraints` 선택). 하나라도 누락되면 수임 역할은 착수하지 않고 반환·질의한다 (02 INV-6).
- 완료 보고: `artifacts`·`self_check`·`failures`·`open_questions`·`verify_basis`.
- 실패 보고: `reason`·`repro`·`attempted`(선택)·`lesson_candidate`·`blocking`.
- 완료 보고는 Verify 통과 후에만 생성된다 (02 INV-4).

---

# 3. 검증 게이트 — CP1 → CP2 → CP3

검증 게이트는 완료 보고를 독립 검증 없이 승인하지 않는 통제 지점이다 (Glossary §3.2-J). 세 체크포인트의 순서는 Loop가 불변으로 소유한다. 정본: 03 §3.1-A.

| 체크포인트 | 주체 | 내용 | 배치 단계 |
|---|---|---|---|
| CP1 | Worker | 자체 점검(self_check). 최종 승인이 아니다. | Execute 종료 → Verify 입력 |
| CP2 | Verifier | 독립 판정. Worker 완료 보고를 그대로 신뢰하지 않는다. | Verify |
| CP3 | Advisor | 최종 승인. 사이클을 닫는다. | Complete 진입 게이트 |

- "Verify 통과" = CP2 PASS. 완료 보고는 Verify 통과 후에만 생성된다 (02 INV-4, 03 INV-2).
- CP1 또는 CP2 실패 시 재작업 루프로 되돌린다 (03 §3.1-B).
- 판정 기준·검증 방법의 정본은 06(Verifier)이다. 단계 전이·시퀀싱의 정본은 03 §3.1-A다. Loop는 순서만 소유한다.

---

# 4. Adapter Binding (환경 의존 — 본문과 분리)

§1~§3 역할 계약은 AI 비의존이다 (Core Contract, 02 §3). 아래는 v0.x 실행 환경 바인딩이다 (02 §4.1). 이식 시 이 절만 교체된다. 역할 경계·메시지 필수 필드·Invariants는 유지된다 (02 §4.2).

- 역할 정의 파일: 각 역할은 `.claude/agents/`의 정의 파일로 바인딩된다 — `advisor.md` / `planner.md` / `worker.md` / `verifier.md`.
- 상위 규약 바인딩: `.claude/AGENT.md`가 모든 역할 정의의 상위 규약이다. `.claude/CLAUDE.md`가 Advisor를 프로젝트 진입점(주 세션)에 바인딩한다.
- 실행 모델: Worker의 기본 실행 모델은 Opus로 지정된다 (02 §4.1). 그 외 역할은 세션 모델을 상속한다.
- 위임·보고 채널: 위임 메시지와 완료·실패 보고는 서브에이전트 위임과 그 최종 응답으로 흐른다 (02 §4.1).

---

# 5. 정본과 포인터

| 대상 | 정본 |
|---|---|
| 역할 경계 | 02 §3.2-A |
| 위임 메시지 | 02 §3.2-B |
| 완료 보고 | 02 §3.2-C |
| 실패 보고 | 02 §3.2-D |
| 역할별 Lifecycle 책임 | 02 §3.1 |
| 검증 게이트 (CP1→CP2→CP3) | 03 §3.1-A |
| Verifier 검증 리포트 | 06 §3.2-A |
| 작업 분해·Task·병렬 집합 | 07 §3.2 |
| 용어 | specs/00-glossary.md |
| 상위 규약 | AGENT.md |

이 문서는 요약이다. 상세·정본은 위 포인터를 따른다. 충돌 시 정본이 우선한다.
