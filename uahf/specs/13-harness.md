# specs/13-harness — Harness Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05 · 2026-07-26 정합(격리 개정 — 슬림화 + §9-OQ-H5 상위 규약 실측 정정·앵커 90ca19c))
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Harness는 Agent가 스스로를 개발·운용하기 위한 최소 실행 골격이다 (Glossary §3.2-D). self-hosting의 기반이다.

## 이 컴포넌트가 해결하는 문제

- 최소 구성이 없으면 Framework가 스스로를 개발할 출발점이 없다.
- 어떤 요소가 필수인지 규정되지 않으면, 하네스가 임의로 축소되어 검증과 역할 분리가 무너진다.
- self-hosting에서 산출물이 곧 규격이 되는 순환이 관리되지 않으면, 미확정 규격이 정식으로 오인된다.

## 책임 (1~3문장)

Harness는 UAHF가 자기 자신 또는 임의 프로젝트를 개발·운용하기 위해 반드시 존재해야 하는 최소 구성 집합을 규정한다.

Harness는 그 구성이 항상 만족해야 할 무결성 규칙과, 부트스트랩 상태에서 정식 상태로의 전이 조건을 정의한다.

## Non-Goals

- Agent 역할의 내부 계약(역할 경계·위임/보고 메시지 포맷)을 정의하지 않는다 — specs/02-agent.md 소관이다.
- 실행 환경의 호스팅 계약(Module 등록·해소·교체·수명주기)을 정의하지 않는다 — specs/01-runtime.md 소관이다.
- 큰 작업의 분해·병렬 디스패치·병합을 정의하지 않는다 — specs/07-workflow.md 소관이다. Harness는 검증 게이트의 존재만 요구한다.
- 검증의 상세 판정 기준을 정의하지 않는다 — specs/06-verifier.md 소관이다. Harness는 게이트의 존재만 요구한다.
- 신규 프로젝트 설치 메커니즘을 정의하지 않는다 — specs/12-scaffold.md 소관이다. Harness는 설치 대상(최소 구성)만 규정한다.
- 특정 AI·파일 포맷·오케스트레이션 API를 정의하지 않는다 — Adapter Binding(§4) 소관이다.

---

# §2. Position

- 아키텍처 상 위치: Core Component "Harness" (Glossary §3.2-D)의 규격 문서다.
- Harness는 Component다. Cross-cutting Service가 아니다 (유일한 Cross-cutting Service는 Memory Service — Glossary INV-2, INV-3). Harness는 여러 Layer의 요소를 최소 부분집합으로 조합하지만, 이는 "구성(composition)"이지 스택을 관통하는 "능력(capability)"이 아니므로 Cross-cutting 판정 3조건(Glossary §3.2-B)을 충족하지 않는다.
- Layer 귀속: 단일 Layer에 고정되지 않는다. Harness는 상위 규약(governance)·Agent Layer의 역할·Runtime Layer의 호스팅 요소를 조합한다. 정본 Component→Layer 매핑은 Glossary §9-OQ6 흐름에 따라 Wave 3에서 Advisor가 확정한다. 이 spec은 자신의 조합적 성격만 선언한다.

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 3.2 Modular, 3.4 Verify Everything, 6 Core Components.
- specs/00-glossary.md (실재, Frozen) — 모든 용어의 정본. 특히 Harness 정의(§3.2-D), 역할 정의(§3.2-E).
- specs/TEMPLATE.md (실재, Frozen) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약. 부트스트랩 하네스의 상위 규약 실물.
- specs/01-runtime.md (실재, Frozen) — 호스팅 계약. Harness는 이 계약의 최소 부분집합 선택이다.
- specs/02-agent.md (실재, Frozen) — 역할 경계·위임/보고 프로토콜의 정본.
- ROADMAP.md v0.2(Agent Harness Bootstrap), v0.9(Adapter & Scaffold 정식화) (실재).

## 이 spec에 의존하는 spec (dependents)

- specs/12-scaffold.md — Scaffold가 신규 프로젝트에 설치하는 초기 형태가 Harness의 최소 구성(§3.2-A)이다. 의존 방향은 12 → 13이다. 설치 계약의 정밀 조율은 §9에 기록되며 해소되었다(§9-OQ-H1).

(상태 표기는 2026-07-26 현행 정합 — 규율 대상 15종(numbered spec 14 + TEMPLATE)이 전부 Frozen 확정이다. `uaf-verified: 00-glossary·01·02·12·TEMPLATE 머리 상태 라인·docs/spec-versioning-policy.md §2.2 대조`. 종전 "Review"·"Adopted"·"동시 작성 중" 표기는 작성 시점 기록이었다.)

## 순환 의존

없다. Harness는 01·02의 계약을 조합하고 참조한다(의존 방향 13 → 01, 13 → 02). 01·02는 Harness에 의존하지 않는다. Scaffold(12)는 Harness에 의존한다(12 → 13). 13은 12에 의존하지 않는다. 순환은 발생하지 않는다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 AI·환경 의존 실현은 §4에 둔다.

Harness는 "최소 구성의 선택과 무결성 규칙"만 소유한다. Agent 계약(역할 경계·위임/보고 메시지 포맷)은 specs/02-agent.md가 소유하고, 호스팅 계약(Module 등록·해소·교체·Bootstrap)은 specs/01-runtime.md가 소유한다. Harness는 이 둘을 재정의하지 않고 최소 부분집합으로 조합하며, 조합 전체가 만족해야 할 무결성 규칙(§3.3)만 추가로 정의한다.

Harness는 세 가지를 정의한다.

- 최소 구성 집합 (§3.1-A, §3.2-A)
- Harness 상태와 전이 (§3.1-B, §3.2-B)
- 무결성 규칙 (§3.3)

---

## 3.1 Interface

Harness는 다음 연산을 노출한다. 위임 메시지·완료 보고·실패 보고의 내용 포맷은 02 §3.2-B/C/D가 소유하며 여기서 재정의하지 않는다. 아래 연산은 그 메시지들을 조합하는 Harness 수준의 성립·점검 계약이다.

### A. 구성 확립 (Establish)

- 입력: 대상 프로젝트(자기 자신 또는 임의 프로젝트) + 최소 구성 집합(§3.2-A).
- 출력: 성립한 Harness — 위임 → 구현 → 검증 → 승인 사이클을 수행할 수 있는 최소 실행 골격. 상태는 §3.2-B(Bootstrap 또는 Formal)로 판정된다.
- 완료 조건: §3.2-A의 5개 필수 요소가 모두 존재하고, §3.3의 모든 무결성 규칙을 만족한다.
- 실패 보고: reason = `MissingElement`(결손된 필수 요소) | `IntegrityViolation`(위반된 무결성 규칙). location = 요소 식별자 또는 규칙 식별자(H-INV-n).

### B. 무결성 점검 (Check Integrity)

- 입력: 성립한 Harness.
- 출력: 무결성 점검 결과 — §3.3 각 규칙의 충족 여부.
- 완료 조건: §3.3의 모든 무결성 규칙이 충족된다.
- 실패 보고: reason = `IntegrityViolation`, location = 위반 규칙(H-INV-n)과 위반 지점.

---

## 3.2 Data Format

### A. 최소 구성 집합 (Minimal Composition Set)

Harness가 성립하기 위해 반드시 존재해야 하는 5개 요소다. 하나라도 없으면 Harness가 아니다. "부재 시 붕괴"는 그 요소가 없을 때 무엇이 무너지는지를 명시한다.

| 필수 요소 | 최소 역할 | 부재 시 붕괴 | 소유·근거 |
|---|---|---|---|
| 상위 규약 문서 (Governance) | 모든 Agent 행동의 최상위 기준. Architecture First·Spec First를 강제한다. | 역할 정의와 Agent 행동이 근거를 잃는다. 산출물이 규격에서 이탈하고, self-hosting 순환의 기준점이 사라진다. | AGENT.md, ARCHITECTURE.md |
| Agent 역할 정의 4종 | Advisor·Planner·Worker·Verifier의 책임과 경계를 확립한다. | 역할 경계(02 §3.2-A)가 없어 한 주체가 결정·구현·검증을 겸한다. 독립 검증이 불가능해지고 Verify Everything이 붕괴한다. | 02 §3.2-A, Glossary §3.2-E |
| 위임·완료/실패 보고 프로토콜 | 위임과 보고를 검증 가능한 형태로 흐르게 한다. | 위임이 완료 조건 없이 흐르고(02 INV-6 무력화), 완료·실패 보고가 형식 없이 은폐 가능해진다. 검증 대상이 불명확해진다. | 02 §3.2-B/C/D |
| 검증 게이트 (Verification Gate) | 완료 보고를 독립 검증 없이 승인하지 않는 통제 지점. | 완료 보고가 독립 검증 없이 승인된다. 거짓 완료가 통과하고, self-hosting 순환이 오류를 다음 사이클로 전파한다. | ARCHITECTURE 3.4, AGENT.md Verification, 02 INV-4 |
| 작업 추적 (Task Tracking) | 위임 사이클의 진행·완료 상태와 설계 결정을 기록·추적한다. | 사이클의 진행·완료 상태와 결정 기록이 소실된다. 재작업·회귀·승인 여부를 판단할 근거가 없다. | 본 spec H-INV-5 |

주의: 위 표의 "소유·근거" 열이 가리키는 상세 계약(역할 경계, 위임/보고 메시지 필드 등)은 각 소유 spec이 정본이다. Harness는 이 요소들의 "필수성"과 "조합"만 소유한다.

### B. Harness 상태와 전이 (Harness State)

Harness는 두 상태를 가진다. self-hosting에서 산출물이 곧 규격이 되는 순환은 이 상태로 관리된다.

| 상태 | 의미 | 실현 형태 (환경 의존 상세는 §4) | 로드맵 |
|---|---|---|---|
| Bootstrap (부트스트랩) | 관련 spec이 Frozen되기 전. 규약 문서 형태로 실현된 최소 하네스. 산출물이 곧 규격이 되는 self-hosting 순환 상태. | 상위 규약 문서 + 역할 정의 + 위임·검증 관행. Runtime의 정식 Module 구성으로 호스팅되지 않는다. | v0.2 |
| Formal (정식) | 관련 spec이 Frozen되고 Runtime(01)이 호스팅하는 정식 Module 구성으로 전이한 Harness. | Runtime 정식 Module 구성 + Adapter 뒤로 격리된 환경 바인딩. Scaffold 설치 대상. | v0.9 |

**전이 조건 (Bootstrap → Formal).** 다음 4개를 모두 충족할 때만 Formal로 전이한다.

1. Harness가 조합하는 관련 spec(13-harness, 02-agent, 01-runtime, 06-verifier 등)이 Frozen이다.
2. 최소 구성의 환경 의존 실현이 Adapter Binding(§4) 뒤로 이동해 Core에 특정 AI 의존이 0건이다 (ROADMAP v0.9 경계 검증).
3. Harness가 Runtime(01)의 정식 Module 구성으로 호스팅된다 (H-INV-6, 01 INV-2).
4. Scaffold(12)가 이 최소 구성을 신규 프로젝트 설치 대상으로 삼는다 (12 조율 — §9).

조건이 하나라도 미충족이면 Harness는 Bootstrap 상태를 유지한다 (H-INV-7).

### C. 실패 보고 참조

Harness 연산(Establish/Check Integrity)의 실패는 §3.1의 reason/location 구조로 보고한다. Harness 안에서 흐르는 위임·완료·실패 보고 메시지의 내용 포맷은 02 §3.2-B/C/D를 그대로 사용하며 여기서 재정의하지 않는다.

---

## 3.3 Invariants

Harness가 보장해야 할 무결성 규칙이다. §3.1-B "무결성 점검"의 판정 대상이다.

- **H-INV-1 (최소 구성 완비).** §3.2-A의 5개 필수 요소가 모두 존재해야 Harness가 성립한다. 하나라도 없으면 Harness가 아니다. 부트스트랩 상태에서도 5요소는 모두 필요하다.
- **H-INV-2 (역할 경계 유지).** Harness는 4개 역할의 경계를 유지한다 (02 §3.2-A). 한 주체가 결정·구현·검증을 겸하지 않는다. 특히 구현 주체와 검증 주체는 분리된다. 이 분리가 Verify Everything의 전제다.
- **H-INV-3 (완료 조건 포함 위임).** Harness 안의 모든 위임은 명확한 입력·출력·완료 조건·컨텍스트를 포함한다 (02 INV-6). 하나라도 누락되면 수임 Agent는 착수 전에 반환·질의한다.
- **H-INV-4 (독립 검증 게이트).** Harness 안의 모든 완료 보고는 독립 검증을 통과한 뒤에만 승인된다. 완료 보고를 그대로 신뢰하지 않는다 (ARCHITECTURE 3.4, AGENT.md Verification, 02 INV-4). 검증 주체는 구현 주체와 분리된다 (H-INV-2). 검증의 상세 판정 기준은 specs/06-verifier.md 소관이며, Harness는 게이트의 존재만 요구한다.
- **H-INV-5 (결정의 기록).** 모든 설계 결정과 미해소 사항은 기록된다. 결정은 결정 기록으로, 미해소는 Open Questions로 남긴다. 기록되지 않은 결정은 self-hosting 순환에서 소실되어 재작업·회귀 판단을 불가능하게 한다.
- **H-INV-6 (최소 부분집합).** Harness는 Runtime(01)이 호스팅하는 구성의 최소 부분집합이다 (01 INV-2). 필수 계약만 해소되면 기동하며, 선택 요소의 부재는 실패가 아니다. Harness는 이 부분집합의 "선택"만 소유하고, 호스팅 계약 자체는 01이 소유한다.
- **H-INV-7 (순환 관리).** 산출물이 곧 규격이 되는 self-hosting에서, 관련 spec이 Frozen되기 전의 Harness는 부트스트랩 상태다 (§3.2-B). Harness는 규격이 확정되기 전에 자신을 정식이라 선언하지 않는다.
- **H-INV-8 (Core AI 비의존).** §3의 어떤 Harness 계약도 특정 AI 모델·실행 환경에 의존하지 않는다. 부트스트랩의 환경 의존 실현은 전부 §4에 둔다.

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding

v0.x의 부트스트랩 Harness는 Claude Code 위에서 self-hosting으로 실현된다 (ROADMAP v0.2, ARCHITECTURE 3.1 "Claude는 첫 번째 Adapter"). §3의 추상 최소 구성을 Claude Code 표면에 다음과 같이 바인딩한다. 각 요소의 상세 바인딩 정본은 소유 spec(01·02)의 §4이며, Harness는 이들을 최소 구성으로 조합하는 지점만 명시한다.

| §3 구성 요소 | Claude Code 바인딩 | 상세 정본 |
|---|---|---|
| 상위 규약 문서 | `.claude/AGENT.md`(공통 규약), `.claude/CLAUDE.md`(Advisor 진입점 바인딩) | 02 §4.1 |
| Agent 역할 정의 4종 | `.claude/agents/{advisor,planner,worker,verifier}.md` | 02 §4.1 |
| 위임·보고 프로토콜 | 서브에이전트 위임(위임 메시지 전달) + 서브에이전트 최종 응답(보고 회수) | 02 §4.1 |
| 검증 게이트 | Advisor의 독립 재검증 — `.claude/CLAUDE.md` "Worker 완료 보고를 그대로 신뢰하지 않는다" | 02 §4.1, 06 |
| 작업 추적 | Wave 단위 위임·검증 사이클과 결정 기록(Open Questions·결정 기록 관행) | (부트스트랩 관행) |
| 실행 모델 지정 | Worker의 기본 실행 모델 = Opus 등 역할별 모델 지정 | 02 §4.1 (SP-3) |
| 호스트 프로세스 | Claude Code 세션/턴 = 사이클 실행 컨테이너 | 01 §4.1 |

## 4.2 이식 교체 지점 (Portability Swap Points)

다른 AI 환경으로 이식할 때 바뀌는 것 전부다. §3의 최소 구성과 무결성 규칙은 유지되고 아래만 교체된다. 각 항목의 정식화는 소유 spec이 담당한다.

1. 상위 규약 문서 위치·포맷(`.claude/*.md`) → 대상 환경의 규약·프롬프트 주입 방식 (02 SP-2).
2. Agent 역할 정의 파일(`.claude/agents/*.md`) → 대상 환경의 Agent 정의 메커니즘 (02 SP-1).
3. 위임·보고 채널(서브에이전트 위임/최종 응답) → 대상 환경의 오케스트레이션·결과 반환 API (02 SP-4, SP-5).
4. 실행 모델 지정(Worker = Opus 등) → 대상 환경의 모델·엔진 (02 SP-3).
5. 작업 추적·결정 기록 메커니즘(Wave/서브에이전트 관행) → 대상 환경의 추적·기록 메커니즘.
6. 호스트 프로세스/세션 수명주기 → 대상 환경의 실행 프로세스 (01 §4.2).

Harness 고유의 이식 불변 요소: 최소 구성 5요소의 "필수성"과 무결성 규칙(§3.3)은 어떤 환경에서도 유지된다. 바뀌는 것은 각 요소의 실현 형태뿐이다.

---

# §5. Memory Access (해당 시)

해당 없음 (직접 접근).

Harness는 Memory를 직접 읽거나 쓰지 않는다. ARCHITECTURE 5.1의 Memory 소비자 목록(Agent, Loop, Workflow, Verifier)에 Harness는 포함되지 않는다.

단서 (불변 규칙): Harness 안의 Agent가 Memory에 접근할 때는 Memory Service Interface(단일 Port)만 경유한다 (02 §5, 02 INV-8, ARCHITECTURE 5.1). 결정의 기록(H-INV-5)이 Memory Service로 영속화되는 경우에도 접근 경로는 이 단일 Port뿐이며, 영속성 백엔드는 Adapter Layer 뒤에 둔다. Harness는 이 접근을 요구할 뿐 경로를 새로 만들지 않는다.

---

# §6. Failure Modes

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| 필수 요소 결손 (5요소 중 하나 부재) | Establish 실패. reason=MissingElement. Harness 미성립 (H-INV-1). | 예 |
| 역할 겸직 (한 주체가 구현과 검증을 겸함) | 독립 검증 붕괴. H-INV-2 위반으로 판정. 구현 주체와 검증 주체를 분리한다. | 예 |
| 완료 조건 없는 위임 | H-INV-3 위반. 수임 Agent가 착수 전 반환·질의 (02 INV-6). | 예 |
| 검증 없는 승인 (완료 보고 맹신) | H-INV-4 위반. 거짓 완료가 통과한다. 독립 검증 게이트로 차단한다. | 예 |
| 결정 미기록 | H-INV-5 위반. self-hosting 순환에서 결정이 소실. 재작업·회귀 판단 불가. | 예 |
| 조기 정식화 선언 (관련 spec Frozen 전에 정식 선언) | H-INV-7 위반. 부트스트랩 상태 유지로 교정. | 예 |
| 순환 오염 (잘못된 산출물이 다음 사이클의 규격이 됨) | 검증 게이트(H-INV-4)로 각 산출물을 독립 검증해 오류 전파를 차단한다. | 예 |
| 선택 요소 부재 (필수 아닌 확장) | 실패 아님. 최소 부분집합으로 계속 기동 (H-INV-6, 01 INV-2). | 아니오 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.2 완료 조건("위임 → 구현 → 검증 → 승인 사이클 1회 이상 시연")과 정렬한다.

- **최소 구성 시연.** §3.2-A의 5개 필수 요소(상위 규약 문서, 역할 정의 4종, 위임·보고 프로토콜, 검증 게이트, 작업 추적)가 모두 존재함을 보인다 (H-INV-1).
- **역할 분리 시연.** 구현 주체(Worker)와 검증 주체(Verifier/Advisor)가 분리되어 있어, 구현자가 자신의 산출물을 최종 승인하지 못함을 보인다 (H-INV-2).
- **사이클 시연.** 위임 → 구현 → 검증 → 승인 사이클이 1회 이상 수행됨을 보인다 (ROADMAP v0.2, 02 §7과 동일 기준).
- **검증 게이트 시연.** 완료 보고가 독립 검증을 통과하기 전에는 승인되지 않음을 보인다 (H-INV-4).
- **상태 판정 시연.** 관련 spec의 Frozen 여부와 §3.2-B 전이 조건 4개를 대조해, 현재 Harness가 부트스트랩인지 정식인지 판정한다 (H-INV-7).
- **Core AI 비의존 시연.** §3 본문 전체를 스캔해 특정 AI 모델명·제품 기능 참조가 0건임을 보인다 (H-INV-8, DoD-3).

## 검증 방법

- Verifier가 최소 구성 5요소의 존재를 §3.2-A 체크리스트와 대조한다. 결손 0건이어야 한다.
- Verifier가 하나의 실제 위임 사이클(위임 메시지 → 완료 보고 → 독립 검증 → 승인)을 §8 예와 대조해, 검증 주체가 구현 주체와 분리되어 있음을 확인한다.
- Verifier가 §3.2-B 전이 조건 4개를 관련 spec 상태와 대조해 Harness 상태를 판정한다.
- Verifier가 §3 본문에서 특정 AI 의존 토큰(모델명·제품 기능명)이 0건임을 확인한다 (DoD-3).
- Advisor가 최종 승인한다.

---

# §8. Examples

**예 1 — self-hosting 위임 사이클 1회 (부트스트랩 하네스)**

이 spec(13-harness) 자체가 부트스트랩 Harness의 위임 사이클로 작성되었다. 사이클은 다음 4단계다 (역할·계약만으로 서술 — AI 비의존).

1. Advisor가 Worker에게 13-harness.md 신규 작성을 위임한다. 위임 메시지는 input(미작성 상태), output(TEMPLATE 준수 완성 spec), done(§0~§9 존재·DoD 8항목 충족·Glossary 용어만), context(읽어야 할 문서 목록)를 포함한다 (02 §3.2-B).
2. Worker가 산출물을 생성하고 완료 보고를 남긴다. 보고는 산출물 경로·자체 점검·실패/미완성·Open Questions를 포함한다 (02 §3.2-C).
3. Advisor가 완료 보고를 그대로 신뢰하지 않고 독립 재검증한다 — 검증 게이트 (H-INV-4).
4. 검증 통과 후 Advisor가 승인한다.

이 사이클은 최소 구성 5요소(상위 규약·역할 정의·위임·보고 프로토콜·검증 게이트·작업 추적)가 모두 존재해야 성립한다. 하나라도 없으면 §6의 대응 시나리오로 사이클이 무너진다. 예: 검증 게이트가 없으면 3단계가 사라져 거짓 완료가 통과한다 (H-INV-4 붕괴).

**예 2 — 부트스트랩 → 정식 전이 판정**

질문: 현재 Harness는 부트스트랩인가 정식인가?

→ §3.2-B 전이 조건 4개를 대조한다.
1. 관련 spec(13-harness=Draft, 02-agent=Review, 01-runtime=Review)이 아직 Frozen이 아니다. → 미충족.
2. 환경 의존 실현이 규약 문서 형태로 남아 있어 Adapter 뒤로 격리되지 않았다. → 미충족.
3. Runtime의 정식 Module 구성으로 호스팅되지 않는다. → 미충족.
4. Scaffold(12)가 설치 대상으로 삼는 계약이 아직 조율 중이다. → 미충족.

→ 4개 중 하나도 충족되지 않았다. 따라서 현재 Harness는 **부트스트랩 상태**다 (H-INV-7). v0.9에서 전이 조건 4개가 모두 충족되면 정식으로 전이한다.

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

**타 spec 조율:**

- **OQ-H1: Scaffold와 Harness의 설치 관계(12 조율)** — 해소(설치 대상 = 이 spec §3.2-A 최소 구성 집합. Harness는 "설치 대상 = 최소 구성 집합"만 선언하고 설치 메커니즘은 12 소관으로 남긴다. 전이 조건 4(§3.2-B)가 이 조율에 의존하며 충족 가능해졌다 — 12 §9-OQ-2 동일 결정 · 상세 = 결정 기록 소절·git 앵커 90ca19c).

- **OQ-H2: 검증 게이트와 병렬 오케스트레이션(07 경계 — 비차단)** — 해소(Harness는 위임 사이클에 검증 게이트가 존재할 것만 요구한다(H-INV-4). 분해·병렬 디스패치·병합·충돌 처리 상세는 07 소관 — 경계 정합 확인 완료, 비차단 유지).

- **OQ-H3: 검증 게이트의 판정 기준(06 경계 — 비차단)** — 해소(게이트의 상세 판정 기준·리포트 포맷은 06 소관. Harness는 게이트의 존재와 "구현 주체와 검증 주체의 분리"(H-INV-2)만 요구 — 경계 정합 확인 완료, 비차단 유지).

**Glossary 추가 요청:**

- **OQ-H4: Harness 소유 용어 4건** — 용어 4종(최소 구성 집합 Minimal Composition Set · Harness 상태(Bootstrap/Formal) · 검증 게이트 Verification Gate · 작업 추적 Task Tracking)은 00-glossary §3.2-J-13 정본 등재 완료(요청 4건 전부 Advisor 승인). 상세 필드·전이 조건의 정본은 이 spec §3.2-A/B가 유지한다.

**상위 규약 정합 확인 (비차단) — Planner와 최소 구성.**

- **OQ-H5: Planner와 최소 구성의 상위 규약 정합.** 원 질문 요지 = 최소 구성이 요구하는 "Agent 역할 정의 4종"(§3.2-A, Glossary §3.2-E)에 대해 작성 시점의 AGENT.md Delegation이 Planner를 명시하지 않아 갈리는지(02 §9-OQ-2·Glossary §9-OQ4와 동일 사안). — **해소(실측 2026-07-26): AGENT.md §Delegation·§Roles에 Planner 반영 확인**(§Delegation = "Planner는 계획·브리프 초안만 작성한다. 스스로 채택하지 못한다" · §Roles & Boundaries = `### Planner` 소절 실재). 최소 구성의 4역할 요구와 상위 규약이 정합한다. `uaf-verified: .claude/AGENT.md §Delegation·§Roles & Boundaries 직접 대조` · `uaf-allow-legacy: 앞의 "명시하지 않아 …갈리는지"는 해소된 원 질문의 작성 시점 요지 인용 — 현재형 주장 아님`

**ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE 3.2(Modular, 최소 부분집합)·3.4(Verify Everything)·6(Harness는 Core Component)과 Glossary §3.2-D 정의에 정렬한다.

## 결정 기록 (Advisor — Wave 4 통합)

- OQ-H1 해소: 12 완성 확인 — 위 12 OQ-2와 동일 결정 (설치 대상 = §3.2-A 최소 구성 집합).
- OQ-H2/OQ-H3: 07·06 완성 확인 — 경계 정합. 비차단 유지.
- OQ-H4 Glossary 추가 요청 4건 승인 — Glossary §3.2-J 반영.
- OQ-H5: 기존 사용자 승인 대기 제안(AGENT.md Delegation에 Planner 추가)과 동일 사안 — 유지.
- OQ-H5 해소(2026-07-26 실측) — AGENT.md 반영 확인. 위 Wave 4 기재는 그 시점의 기록으로 무수정 보존한다(`uaf-allow-legacy: Wave 4 시점의 승인 대기 상태 기록 — 정책 §3.4 append-only·시점 불변`). `uaf-verified: .claude/AGENT.md §Delegation·§Roles & Boundaries 직접 대조`

2026-07-26 정합(격리 개정 — 유형 (B), docs/spec-versioning-policy.md §3.2): md 슬림화 — §9 해소 OQ(OQ-H1~H4)의 원문+답 이중 잔존 1줄화, Glossary 추가 요청 블록의 등재 완료 1줄화, §2 stale 상태 표기(Review/Adopted → Frozen)·"동시 작성 중" 서술 현행 정정. OQ-H5는 같은 회차 자기 행 교정(정책 §3.4 예외)으로 해소 전환 — 그 전제("AGENT.md Delegation이 Planner를 명시하지 않는다")가 실측과 반대임을 확인했다(`uaf-allow-legacy: 괄호 안 문면은 정정 대상이 된 종전 전제의 인용 — 정정 사유 기록에 필요한 이력 인용이며 현재형 주장 아님`). 계약 요소(연산·데이터 포맷·필드·불변·완료 조건·의미) 무변경 — §3 전체·§6·§7·§8 규범-예시(self-hosting 위임 사이클·부트스트랩→정식 전이 워크스루) 무촉, dependents(§2 목록 = 12) 참조 영향 0(정책 §4-a·§4-c). §8 예1의 "미작성 상태" 서술은 당시 위임 시점의 사실 기록이므로 보존한다(`uaf-allow-legacy: §8 예1은 부트스트랩 하네스 self-hosting 사이클의 이력 인용 — 시점 기록 보존`). 종전 문면 = git 앵커 90ca19c.
