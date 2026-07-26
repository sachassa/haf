# specs/02-agent — Agent Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05 · 2026-07-26 정합(격리 개정 — 슬림화 + §9-OQ-2 상위 규약 실측 정정·앵커 90ca19c))
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Agent Component는 모든 Agent가 따르는 공통 계약을 정의한다.

AGENT.md는 Agent의 원칙을 선언한다. 그러나 원칙만으로는 검증할 수 없다.

이 spec은 그 원칙을 검증 가능한 계약으로 구체화한다.

## 이 컴포넌트가 해결하는 문제

- 공통 계약이 없으면 역할마다 행동이 달라진다.
- 역할 경계가 없으면 서로의 권한을 침범한다.
- 포맷이 없으면 위임과 보고가 검증 불가능해진다.
- 계약이 없으면 실패가 은폐된다.

## 책임

이 컴포넌트는 Advisor / Planner / Worker / Verifier의 공통 계약을 정의한다.

역할 경계, 위임 프로토콜, 완료·실패 보고 프로토콜, Memory 접근 규칙을 검증 가능한 형태로 확정한다.

## Non-Goals

- Agent Lifecycle의 단계 전이 규칙을 정의하지 않는다. specs/03-loop.md 소관이다.
- Verifier의 상세 판정 기준을 정의하지 않는다. specs/06-verifier.md 소관이다.
- Workflow의 분해·병렬 디스패치·병합을 정의하지 않는다. specs/07-workflow.md 소관이다.
- Memory와 Lessons의 내부 포맷·생성 규칙을 정의하지 않는다. specs/04-memory.md, specs/05-lessons.md 소관이다.
- 설계 원칙을 재정의하지 않는다. ARCHITECTURE.md를 참조로만 연결한다.

---

# §2. Position

- 아키텍처 상 위치: Agent Layer (Component: Agent). Glossary §3.2-D의 Agent (Component) 규격이다.
- 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것):
  - ARCHITECTURE.md 0.2 (실재)
  - specs/00-glossary.md (실재, Status: Frozen)
  - specs/TEMPLATE.md (실재, Status: Frozen)
  - AGENT.md (실재) — 상위 규약
  - ROADMAP.md v0.2 (실재)
- 이 spec에 의존하는 spec:
  - specs/03-loop.md — Loop가 Agent Lifecycle을 구동한다.
  - specs/06-verifier.md — Verifier는 Agent 역할이며 이 spec의 역할 경계를 따른다.
  - specs/07-workflow.md — Workflow는 Agent에게 작업을 디스패치한다.
- specs/01-runtime.md 관계: Runtime Layer가 Agent의 실행·수명주기·config를 관장한다. 01-runtime은 Frozen 확정 상태다(종전 "동시 작성 중" 표기는 작성 시점 기록 — 2026-07-26 현행 정정). 이 spec은 01의 내용에 의존하지 않으며, 계약 필드만 정의하고 실행 채널은 침범하지 않는다. 조율 지점은 §9에 기록한다.
- (위 상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·01-runtime·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`.)
- specs/04-memory.md, specs/05-lessons.md 관계: 이 spec의 §5와 §3.2-D는 Memory 접근 상세와 Lesson 생성 규칙을 04·05에 위임한다. 위임 방향의 참조이며 순환이 아니다 (04 §2·05 §2와 정합).
- 순환 의존: 없다. 이 spec은 03/06/07에 의존하지 않는다. 의존은 항상 그들 → 02 방향이다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다.

실행 모델 바인딩은 §4에 위치한다.

## 3.1 Interface

Agent 공통 계약은 위임을 입력으로, 보고를 출력으로 갖는다.

### 공통 의무 (AGENT.md Responsibilities의 검증 가능한 구체화)

- O1 자신의 책임만 수행 — 위임된 입력·출력·완료 조건의 범위 안에서만 작업한다.
- O2 역할 불침범 — 다른 역할의 권한을 행사하지 않는다. 역할 경계는 §3.2-A에 정의된다.
- O3 검증 가능한 결과 — 모든 산출물은 완료 조건에 대해 검증 가능한 형태로 남긴다.
- O4 추측 금지 — 불확실은 임의로 해석하지 않고 Open Question으로 남겨 에스컬레이션한다.
- O5 실패 은폐 금지 — 실패·미완성은 완료 보고와 실패 보고에 반드시 명시한다.

### 인터페이스

- 입력: 위임 메시지 (§3.2-B).
- 출력: 완료 보고 메시지 (§3.2-C) 또는 실패 보고 메시지 (§3.2-D).
- 완료 조건: 위임된 완료 조건이 충족되고, Lifecycle의 Verify 단계를 통과한 상태.
- 실패 보고 포맷: 실패 보고 메시지 (§3.2-D).

완료 보고는 Verify 단계를 통과한 뒤에만 생성된다 (AGENT.md Verification).

### 각 역할의 Lifecycle 책임

모든 Agent는 Agent Lifecycle(Consult → Plan → Execute → Verify → Learn → Memory Update → Complete)을 따른다.

아래는 각 역할이 Lifecycle에서 갖는 책임이다. 단계 전이 규칙은 정의하지 않는다 (specs/03-loop.md 소관).

- Advisor: Consult에서 상위 규약·Architecture 참조를 주도하고, Plan 초안을 채택하며, Complete를 최종 승인한다.
- Planner: Plan 단계의 초안 작성만 수행한다. 채택 권한은 없다.
- Worker: Execute를 수행하고, Verify 통과 후 완료 보고를 남긴다.
- Verifier: Verify 단계에서 독립 판정을 수행하고 Learn 입력을 제공한다.

## 3.2 Data Format

### 3.2-A 역할 경계 (Role Boundary)

4개 역할의 책임과 권한 경계다. Glossary §3.2-E 정의와 일치한다.

| 역할 | 책임 | 가진 권한 | 갖지 않는 권한 (경계) |
|---|---|---|---|
| Advisor | Architecture, Spec, 설계 결정, 검증, 최종 승인 | 계획 채택·승인, Architecture 결정, 위임, 최종 승인 | 불필요한 직접 구현은 하지 않는다 |
| Planner | Advisor 위임 하에 구현 계획·작업 분해 초안 작성 | 초안 작성·제안 | 계획 채택·승인 권한 없음, Architecture 결정 권한 없음 |
| Worker | 구현. 산출물 생성과 완료·실패 보고 | 산출물 생성, 보고 제출 | Architecture 결정 안 함, 자기 점검을 최종 승인으로 삼지 않음 |
| Verifier | 검증. Worker 완료 보고를 독립 판정 | 독립 검증 판정 | 구현 안 함, Worker 보고를 그대로 신뢰하지 않음 |

역할 분담 기준: Architecture 결정 = Advisor, 구현 = Worker, 검증 = Verifier (AGENT.md Delegation).

### 3.2-B 위임 메시지 (Delegation Message)

위임 시 반드시 전달한다. 하나라도 누락되면 수임 Agent는 착수하지 않는다 (§3.3 INV-6).

- from: 위임하는 역할.
- to: 수임하는 역할.
- task: 작업 요약.
- input: 명확한 입력 — 무엇을 대상으로 하는가.
- output: 명확한 출력 — 기대 산출물과 위치.
- done: 완료 조건 — 검증 가능한 형태.
- context: 착수 전 읽어야 할 문서 목록 — 상위 규약, Architecture, 관련 spec, Memory 회수 범위.
- constraints: 금지·경계 사항 (선택).

이는 AGENT.md Communication Rules(명확한 입력·명확한 출력·완료 조건·실패 이유)의 포맷 구체화다.

### 3.2-C 완료 보고 메시지 (Completion Report Message)

Verify 단계를 통과한 뒤에만 생성된다.

- artifacts: 산출물 경로 목록.
- self_check: 자체 점검 결과 — 완료 조건 항목별 충족 여부.
- failures: 실패·미완성 사항 — 없으면 "없음"을 명시한다.
- open_questions: Open Questions — 없으면 "없음"을 명시한다.
- verify_basis: Verify 단계 통과의 근거.

### 3.2-D 실패 보고 메시지 (Failure Report Message)

- reason: 실패 이유.
- repro: 재현 조건 — 어떤 입력·상태에서 재현되는가.
- attempted: 시도한 것과 결과 (선택).
- lesson_candidate: Lesson 후보 표시 — 여부와 한 줄 요약.
- blocking: 차단 여부 — 계속 진행 가능한가, 차단되었는가.

모든 실패는 Lesson 후보가 된다 (AGENT.md Memory). Lesson의 생성·회수는 §5와 specs/05-lessons.md가 정의한다.

## 3.3 Invariants

- INV-1: 모든 Agent는 AGENT.md 공통 규약을 따른다. 이 spec의 계약은 AGENT.md를 구체화할 뿐 확장·수정하지 않는다.
- INV-2: 모든 Agent는 Agent Lifecycle(Consult → Complete)을 따른다. 단계 전이 규칙은 이 spec이 정의하지 않는다 (specs/03-loop.md).
- INV-3: 역할 경계는 침범되지 않는다. Architecture 결정 = Advisor, 구현 = Worker, 검증 = Verifier. Planner는 결정 권한을 갖지 않는다.
- INV-4: 완료 보고는 Verify 단계를 통과한 뒤에만 생성된다. 검증되지 않은 결과는 완료가 아니다 (ARCHITECTURE.md 3.4).
- INV-5: 실패·미완성은 은폐되지 않는다. 완료 보고와 실패 보고에 반드시 명시된다.
- INV-6: 모든 위임은 명확한 입력·출력·완료 조건·컨텍스트를 포함한다. 하나라도 누락되면 수임 Agent는 착수 전에 반환·질의한다.
- INV-7: §3의 어떤 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 실행 모델 바인딩은 §4에 위치한다.
- INV-8: Agent는 Memory에 Memory Service Interface(단일 Port)를 통해서만 접근한다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x는 Claude Code 위 self-hosting으로 §3의 계약을 실현한다 (ROADMAP v0.2, ARCHITECTURE.md 3.1 "Claude는 첫 번째 Adapter").

- Agent 정의 파일: 각 역할은 `.claude/agents/*.md`로 정의된다 — advisor.md, planner.md, worker.md, verifier.md (ROADMAP v0.2 산출물).
- 공통 규약 바인딩: `.claude/AGENT.md`가 모든 Agent 정의의 상위 규약이다. `.claude/CLAUDE.md`가 Advisor 역할을 프로젝트 진입점에 바인딩한다.
- 실행 모델 바인딩 (Glossary §3.2-E와 §4.1이 이 spec §4를 지목): v0.x에서 Worker의 기본 실행 모델은 Opus로 지정한다 (ROADMAP·`.claude/CLAUDE.md` "Worker(Opus)"). 다른 역할의 모델 지정도 이 바인딩 영역에 속한다.
- 위임 메커니즘: Advisor는 Claude Code의 서브에이전트 위임으로 §3.2-B 위임 메시지를 Worker/Planner/Verifier에게 전달한다.
- 보고 회수: §3.2-C 완료 보고와 §3.2-D 실패 보고는 서브에이전트의 최종 응답으로 회수된다.
- 컨텍스트 전달: 위임 메시지의 context 필드는 읽어야 할 파일 경로 목록으로 전달된다.

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부다. §3 Core Contract는 유지된다.

- SP-1: Agent 정의 파일 위치·포맷(`.claude/agents/*.md`) → 대상 환경의 Agent 정의 메커니즘.
- SP-2: 상위 규약 바인딩 파일(`.claude/AGENT.md`, `.claude/CLAUDE.md`) → 대상 환경의 규약·시스템 프롬프트 주입 방식.
- SP-3: 실행 모델 지정(Worker = Opus 등) → 대상 환경의 모델·엔진.
- SP-4: 위임 메커니즘(서브에이전트 위임) → 대상 환경의 Agent 호출·오케스트레이션 API.
- SP-5: 보고 회수 방식(서브에이전트 최종 응답) → 대상 환경의 결과 반환 채널.

유지되는 것: §3.2-A 역할 경계, §3.2-B/C/D 메시지의 필수 필드, §3.3 Invariants. 이들은 이식 시 바뀌지 않는다.

---

# §5. Memory Access (해당 시)

Agent는 Memory에 Memory Service Interface(단일 Port)를 통해서만 접근한다 (ARCHITECTURE.md 5.1, INV-8).

## 읽기 (Recall)

- 목적: 착수 전 관련 Lessons·이전 결정·컨텍스트를 회수한다 (Consult 단계).
- 범위: 회수 정책(Recall Policy)에 따라 최소 범위로. 현재 작업에 필요한 것만 읽는다.
- 시점: 필요할 때만. 매 사이클 전량을 무조건 로드하지 않는다 (Token Efficiency, ARCHITECTURE.md 3.6).

## 쓰기 (Record)

- 기록 대상: 작업 결과·결정·상태 중 다음 사이클에 필요한 것 (Memory Update 단계).
- Lesson 생성 조건: 모든 실패는 Lesson 후보가 된다 (AGENT.md Memory). §3.2-D 실패 보고에서 lesson_candidate로 표시된 항목이 Lesson 생성 대상이다. 성공은 Best Practice 후보가 된다 (AGENT.md Memory — §9 용어 참조).

상세 포맷·생성 규칙은 specs/04-memory.md, specs/05-lessons.md가 정의한다. 이 spec은 접근 경로 계약만 정의한다.

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다. 모두 Lesson 후보다.

- 역할 침범: Worker가 Architecture를 결정하거나, Planner가 계획을 스스로 채택한다. 대응 — INV-3으로 차단. Advisor에게 반환.
- 위임 불완전: 입력·출력·완료 조건·컨텍스트 중 하나가 누락된 위임. 대응 — INV-6에 따라 수임 Agent가 착수 전 반환·질의.
- 조기 완료 보고: Verify 통과 전에 완료를 보고한다. 대응 — INV-4로 차단. Verify 통과 전 완료 보고는 무효.
- 실패 은폐: 실패·미완성을 보고에서 누락한다. 대응 — INV-5 위반. Verifier가 산출물과 보고의 불일치로 검출.
- 추측: 불확실을 Open Question으로 남기지 않고 임의 해석한다. 대응 — O4 위반. 추측 결과는 무효.
- Memory 우회 접근: Memory Service Interface를 거치지 않고 영속성 백엔드에 직접 접근한다. 대응 — INV-8 위반. 단일 Port 경유로 교정.

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

- 임의의 위임을 열어, §3.2-B 필수 필드(입력·출력·완료 조건·컨텍스트)가 모두 존재함을 보인다.
- 임의의 완료 보고를 열어, 산출물 경로·자체 점검·실패/미완성·Open Questions 필드가 모두 존재하고, 그 보고가 Verify 통과 이후 생성되었음을 보인다.
- 임의의 실패 보고를 열어, 실패 이유·재현 조건·Lesson 후보 표시가 존재함을 보인다.
- 4개 역할 각각에 대해, 권한 경계를 벗어난 행위(예: Worker의 Architecture 결정)가 차단됨을 시연한다.
- Agent가 Memory에 접근하는 모든 경로가 Memory Service Interface임을 보인다.
- 위임 → 구현 → 검증 → 승인 사이클을 1회 이상 시연한다 (ROADMAP v0.2 완료 조건).
- §3 본문에 특정 AI 모델·실행 환경 의존 토큰이 0건임을 보인다.

## 검증 방법

- Verifier가 위임/완료/실패 메시지의 필수 필드 존재를 §3.2-B/C/D와 대조한다.
- Verifier가 역할 경계 위반 케이스를 §3.2-A 표와 대조해 판정한다.
- Verifier가 완료 보고 생성 시점이 Verify 이후임을 확인한다 (INV-4).
- Verifier가 §3 본문을 스캔해 AI 의존 토큰(모델명·제품 기능명)이 0건임을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — 위임과 완료 보고 (Advisor → Worker)**

위임 메시지:
- from: Advisor / to: Worker
- task: specs/02-agent.md 신규 작성
- input: placeholder 상태의 specs/02-agent.md
- output: TEMPLATE.md를 준수한 완성 spec 1개 (해당 파일)
- done: §0~§9 존재, DoD 8항목 충족, Glossary 용어만 사용
- context: ARCHITECTURE.md 0.2, TEMPLATE.md, specs/00-glossary.md, AGENT.md, ROADMAP.md v0.2

완료 보고 메시지 (Verify 통과 후):
- artifacts: specs/02-agent.md
- self_check: §0~§9 존재(충족), DoD-3 §3 AI 의존 0건(충족)
- failures: 없음
- open_questions: §9 참조
- verify_basis: §7 완료 기준 항목별 대조

**예 2 — 역할 경계 (Planner)**

Planner가 작업 분해 초안을 작성한다. Planner는 초안을 스스로 채택하지 못한다.

채택·승인은 Advisor가 수행한다 (INV-3, Glossary §9-OQ4). Planner가 채택을 시도하면 §6 "역할 침범"으로 차단된다.

**예 3 — 실패 보고 (Worker)**

Worker가 구현 중 필요한 인터페이스가 아직 확정되지 않았음을 발견한다.

실패 보고 메시지:
- reason: 의존 인터페이스 미확정
- repro: 해당 작업 착수 시점에 재현
- attempted: 대체 경로 탐색 → 계약 부재로 진행 불가
- lesson_candidate: 여부 = 예 — "의존 계약 미확정 시 착수 전 조율 필요"
- blocking: 차단됨

Worker는 추측하지 않고 (O4) Advisor에게 에스컬레이션한다.

---

# §9. Open Questions

- **OQ-1: Agent 실행 채널(01-runtime 조율)** — 해소(Agent는 Runtime의 generic Module(hosted unit) 계약을 구현한다. entrypoint = 이 spec §3.2-B 위임 메시지 입력 → §3.2-C/D 보고 출력. 메시지 계약 = 이 spec 소유, 호스팅 계약 = 01-runtime §3 소유, 물리 전달 채널 = 각 spec §4 소관. 01-runtime §9 동일 기록 · 상세 = git 앵커 90ca19c).

- **OQ-2: 상위 규약 잠재 불일치 보고 — AGENT.md Delegation의 Planner 취급.** 원 질문 요지 = 작성 시점의 AGENT.md Delegation이 Planner를 명시하지 않아 Glossary §3.2-E의 4역할 정의와 갈리는지. — **해소(실측 2026-07-26): AGENT.md §Delegation·§Roles에 Planner 반영 확인**(§Delegation = "Planner는 계획·브리프 초안만 작성한다. 스스로 채택하지 못한다" · §Roles & Boundaries = `### Planner` 소절 실재). 이 spec이 따른 Glossary §3.2-E 4역할 정의와 상위 규약이 정합하며 불일치는 남지 않는다. `uaf-verified: .claude/AGENT.md §Delegation·§Roles & Boundaries 직접 대조` · `uaf-allow-legacy: 앞의 "명시하지 않아 …갈리는지"는 해소된 원 질문의 작성 시점 요지 인용 — 현재형 주장 아님`

- **OQ-3: Glossary 추가 요청 — Best Practice.** 용어 1종(Best Practice)은 00-glossary §3.2-C 정본 등재 완료(Advisor 승인). 이 spec §5 참조는 유효하다.

- **OQ-4 (비차단 — 경계 명시) — Verify 주체·순서.**
  Lifecycle Verify 단계의 자체 점검, Verifier 역할의 독립 판정, Advisor의 최종 승인 사이의 정확한 시퀀싱은 specs/03-loop.md와 specs/06-verifier.md 소관이다. 이 spec은 "완료 보고는 Verify 통과 이후에만 생성된다"는 의무(INV-4)만 정의하고 단계 전이·판정 상세는 침범하지 않았다. 이 항목은 Frozen을 막지 않는다.

## 결정 기록 (Advisor)

(이 spec은 Wave 4 통합 시점에 별도 결정 기록 소절을 두지 않았다 — 아래는 그 자리에 append하는 격리 개정 이력이다. append-only.)

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 OQ(OQ-1·OQ-2·OQ-3)의 원문+답 이중 잔존 1줄화, §2 stale 상태 표기(Review·"동시 작성 중" → Frozen) 현행 정정. 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — dependents(§2 목록 = 03·06·07) 참조 영향 0(정책 §4-a·§4-c). 종전 문면 = git 앵커 90ca19c.

2026-07-26 OQ-2 해소(같은 회차 자기 행 교정 — 정책 §3.4 예외, 위 행에 OQ-2를 포함시켜 정합): OQ-2의 전제("AGENT.md Delegation이 Planner를 명시하지 않는다")가 실측과 반대임을 확인해 해소 상태로 전환했다 — AGENT.md §Delegation·§Roles & Boundaries 양쪽에 Planner가 반영되어 있다. 상위 규약과 Glossary §3.2-E 4역할 정의는 정합하며 이 spec의 계약(§3.2-A 역할 경계 등)은 무변경이다. `uaf-verified: .claude/AGENT.md §Delegation·§Roles & Boundaries 직접 대조` · `uaf-allow-legacy: 괄호 안 문면은 정정 대상이 된 종전 전제의 인용 — 정정 사유 기록에 필요한 이력 인용이며 현재형 주장 아님`
