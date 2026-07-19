# docs/roles-quick-reference — UAHF 역할 빠른 참조

근거: uahf/specs/02-agent.md §3.2-A (역할 경계 정본), AGENT.md (Planner 조항 포함), 검증 통과 agent 역할 정의 4개
정본: uahf/specs/02-agent.md §3 (역할 계약), 특히 §3.2-A (역할 경계 표)
상위 규약: AGENT.md

---

# 0. 이 문서의 위치

**정본은 uahf/specs/02-agent.md다. 이 문서는 사람용 한 장 요약이다.**

역할 경계·메시지 필드·불변 규칙의 정본은 uahf/specs/02-agent.md가 소유한다.

이 문서는 그 계약을 요약하고, 상세는 § 포인터로 연결한다.

이 문서는 다음을 하지 않는다.

- 02의 역할 경계·메시지 필드를 재정의·확장하지 않는다. § 포인터로 참조만 한다.
- 새 용어를 만들지 않는다. 용어 정본은 uahf/specs/00-glossary.md다.
- 단계 전이(03 소관)·검증 판정 기준(06 소관)·작업 분해(07 소관)를 정의하지 않는다.

충돌이 발견되면 이 문서를 정본으로 삼지 않는다. 02를 따르고 Advisor에게 보고한다.

**구성.** §1~§4는 AI 비의존 역할 계약 요약이다 (Core Contract — 02 §3; §4 WBS/작업 분해 소유 포함). §5는 실행 환경 바인딩이다 (02 §4.1). Core 섹션(§1~§4, §6)에는 특정 AI 모델명·제품 기능명이 등장하지 않는다 (02 INV-7, DoD-3).

**포인터 표기.** 별도 표기가 없으면 `02 §…`=uahf/specs/02-agent.md, `03 §…`=uahf/specs/03-loop.md, `06 §…`=uahf/specs/06-verifier.md, `07 §…`=uahf/specs/07-workflow.md, `Glossary §…`=uahf/specs/00-glossary.md.

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

# 4. WBS / 작업 분해 소유 (요약 — 포인터만)

"작업 분해"의 정본 용어는 **Work Graph**다 (Glossary J-07 · 정본 07 §3.2-A). "WBS"는 서술 라벨이며 새 용어가 아니다. 이 절은 소유 주체를 요약할 뿐 07·02·05의 계약을 재정의하지 않는다 (§0 규약).

작업 분해 소유는 세 주체로 나뉜다 (삼분).

| 주체 | 무엇을 | 정본 포인터 |
|---|---|---|
| 관리 = **오케스트레이션 엔진** | 분해 결과 그래프의 스케줄·게이트·재개·원장(RevisionEvent)·계보 등 기계적 조율 | 05 §2.1 (기계적 조율 = Project Orchestrator) |
| 초안 분해 = **Planner** | 구현 계획·작업 분해 **초안** 작성 (Lifecycle 역할) | 02 §3.2-A · 05 §3.4 (4역할 = Lifecycle 의무 축) |
| 실행 = **Worker** | 엔진이 디스패치한 확정 단일 단위 실행 | 05 §2.1 · AGENT.md (단위 실행) |

이 삼분이 실현되는 **2경로**:

- **경로 (a) — Contract 소비 프로젝트:** 엔진 컴파일러가 **Planner-role proposal step**을 디스패치해 분해 초안을 산출하고, 게이트 통과 후 `task_added` revision으로 합성한다 (05 §2.1 의미 판단 축 · §3.2 RevisionEvent).
- **경로 (b) — Advisor 직접 위임 층:** Planner가 분해 초안을 작성한다 (02 §3.2-A · AGENT.md Delegation).

어느 경로든 초안의 **수용은 게이트**, 확정 권위는 **사용자**다 (05 §2.1). 엔진(관리)과 Worker(실행) 사이의 **중간 축이 Planner(초안 분해)**다.

§ 포인터: 05 §2.1 · 05 §3.4 · 07 §3.2 · 02 §3.2-A · Glossary Work Graph J-07.

---

# 5. Adapter Binding (환경 의존 — 본문과 분리)

§1~§4 역할 계약은 AI 비의존이다 (Core Contract, 02 §3). 아래는 v0.x 실행 환경 바인딩이다 (02 §4.1). 이식 시 이 절만 교체된다. 역할 경계·메시지 필수 필드·Invariants는 유지된다 (02 §4.2).

- 역할 정의 파일: 각 역할은 `.claude/agents/`의 정의 파일로 바인딩된다 — `advisor.md` / `planner.md` / `worker.md` / `verifier.md`.
- 상위 규약 바인딩: `.claude/AGENT.md`가 모든 역할 정의의 상위 규약이다. `.claude/CLAUDE.md`가 Advisor를 프로젝트 진입점(주 세션)에 바인딩한다.
- 실행 모델: Worker의 기본 실행 모델은 Opus로 지정된다 (02 §4.1). 그 외 역할은 세션 모델을 상속한다.
- 위임·보고 채널: 위임 메시지와 완료·실패 보고는 서브에이전트 위임과 그 최종 응답으로 흐른다 (02 §4.1).

---

# 6. 정본과 포인터

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
| 용어 | uahf/specs/00-glossary.md |
| 상위 규약 | AGENT.md |

이 문서는 요약이다. 상세·정본은 위 포인터를 따른다. 충돌 시 정본이 우선한다.
