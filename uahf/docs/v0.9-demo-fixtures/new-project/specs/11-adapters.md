# specs/11-adapters — Adapters Specification

Version: 0.1
Status: Frozen (v0.1 기준선 — 사용자 승인, 2026-07-05)
근거: ARCHITECTURE.md 0.2
상위 규약: AGENT.md

---

# §1. Purpose

Adapters Component는 Core 계약을 특정 AI·실행 환경·영속성 백엔드에 바인딩하는 규격을 정의한다.

UAHF는 AI Agnostic Architecture다 (ARCHITECTURE.md 3.1). 그러나 "AI에 종속되지 않는다"는 선언만으로는 검증할 수 없다.

이 spec은 그 선언을 검증 가능한 계약으로 확정한다. 하나의 Adapter가 반드시 제공해야 하는 바인딩의 전체 목록과, 어떤 구현이 "유효한 Adapter"인지의 적합성 판정 기준을 정의한다.

## 이 컴포넌트가 해결하는 문제

- 바인딩 지점 목록이 없으면 각 컴포넌트 §4에 흩어진 이식 교체 지점이 통합되지 않는다.
- 적합성 기준이 없으면 "이식되었다"를 판정할 수 없다.
- 최소 구현의 정의가 없으면 새로운 AI로의 이식 검증(Architecture Validation)의 합격선이 모호해진다.
- 구조 규격이 없으면 Adapter 산출물이 Core를 오염시킨다.

## 책임 (1~3문장)

이 컴포넌트는 Adapter Interface(하나의 Adapter가 제공해야 하는 바인딩 지점의 전체 집합), Adapter 적합성 판정 기준(Conformance), Adapter 산출물의 구조 규격을 소유한다.

각 컴포넌트의 이식 교체 지점을 하나의 바인딩 지점 목록으로 통합하고, 그 목록에 대한 완전성·불변·루프 통과를 판정한다.

## Non-Goals

- 각 컴포넌트의 Core Contract 내용을 정의하지 않는다 — 각 담당 spec 소유다. Adapters는 바인딩 지점의 목록과 적합성만 소유한다.
- Runtime의 Module·Config·수명주기 계약을 정의하지 않는다 — specs/01-runtime.md 소관이다.
- Agent 역할의 공통 계약을 정의하지 않는다 — specs/02-agent.md 소관이다.
- Memory의 기록·회수 계약이나 Memory 내용을 정의·접근하지 않는다 — specs/04-memory.md 소관이다. 영속성 백엔드의 "바인딩 지점"만 목록에 둔다(§5 구분).
- 특정 AI를 강제하지 않는다. 첫 번째 Adapter의 실명 바인딩은 §4에 격리한다.

---

# §2. Position

- 아키텍처 상 위치: Adapter Layer (Glossary §3.2-A). Core Component "Adapters" (Glossary §3.2-D)의 규격 문서다.
- Adapter Layer는 Presentation → Workflow → Agent → Runtime → Core → **Adapter** 스택의 최하위 경계 계층이다. 이식 시 이 계층만 교체한다 (Glossary §3.2-A, ARCHITECTURE.md 3.1·8).

## 의존하는 문서 (이 spec을 읽기 전에 이해가 필요한 것)

- ARCHITECTURE.md 0.2 (실재) — 최상위 기준. 특히 3.1 AI Agnostic, 5.1 Memory Service(단일 Port·영속성 백엔드), 7 Non Goals, 8 Future Direction.
- specs/00-glossary.md (실재, Review) — 모든 용어의 정본. 특히 Adapter Layer, Adapter Binding, 이식 교체 지점(Portability Swap Point), Core Contract, Port.
- specs/TEMPLATE.md (실재, Adopted) — 문서 구조와 DoD.
- .claude/AGENT.md (실재) — Agent 공통 규약.
- specs/01-runtime.md (실재, Review) — §4.2 이식 교체 지점 7개의 출처.
- specs/02-agent.md (실재, Review) — §4.2 SP-1~SP-5의 출처.
- ROADMAP.md v0.9·v1.0 (실재) — Adapter Layer 정식화, Adapter Interface 최종 규격, 2nd Adapter 최소 구현 판정 조건.

## 이 spec에 의존하는 spec (dependents)

- 각 컴포넌트 spec(01, 02, 그리고 Wave 3의 03~10, 12, 13)의 §4는 자신의 바인딩을 소유하고, 이 spec이 그 지점들을 하나의 목록으로 통합한다. 의존 방향은 11 → (각 spec의 §4)이다.
- 인용 가능 범위(00·01·02)에서 이 spec을 Core Contract 상 dependent로 요구하는 spec은 없다. specs/12-scaffold.md 등이 Adapter 설치를 참조하면 Wave 3에서 dependents로 등재한다 (§9-OQ-1).

## 순환 의존

없다. 이 spec은 01·02의 §4(Adapter Binding)를 통합 대상으로 읽으므로 11 → 01, 11 → 02 방향이다. 01 §4.2와 02 §4.2가 "specs/11-adapters.md가 정식화한다"고 언급하는 것은 통합 위임을 알리는 전방 참조(forward pointer)이며, 01·02의 Core Contract(§3)가 11에 의존하는 것이 아니다. 따라서 Core Contract 수준의 순환은 없다.

---

# §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 첫 번째 Adapter의 실명 바인딩 값은 전부 §4에 둔다.

Adapters는 세 가지 계약을 정의한다.

- Adapter Interface — 바인딩 지점의 전체 목록 (§3.2-A)
- Conformance — 적합성 판정 기준 (§3.1, §3.2-B, §3.2-D)
- Adapter 구조 규격 (§3.2-C)

---

## 3.1 Interface

Adapters Component는 하나의 Adapter 구현을 입력으로 받아 적합성 판정을 출력한다.

**Judge Conformance**
- 입력: 하나의 Adapter 산출물(바인딩 지점별 바인딩 값의 집합) + 대상 실행 환경.
- 출력: Conformance Report (§3.2-D) — 판정(Valid(Full) / Valid(Minimal) / Invalid)과 근거.
- 완료 조건: 다음 세 조건(C1~C3)을 모두 검사한다.
  - **C1 필수 바인딩 완전성** — §3.2-A에서 필수(mandatory)로 표시된 모든 바인딩 지점을 제공한다.
  - **C2 Core Contract 불변** — Core Contract 수정 0건. Adapter는 바인딩만 추가하고 어떤 Core Contract도 수정·확장·삭제하지 않는다.
  - **C3 핵심 루프 통과** — 위임 → 구현 → 검증 → 승인 핵심 루프가 이 Adapter 위에서 1회 이상 통과한다 (ROADMAP v0.2·v1.0).
- 실패 보고 포맷: Conformance Report(§3.2-D)의 verdict=Invalid. 누락 바인딩(C1)·Core 수정(C2)·루프 실패 지점(C3)을 명시한다.

세 조건을 모두 만족하면 유효한 Adapter다. 하나라도 실패하면 Invalid다.

---

## 3.2 Data Format

### 3.2-A Adapter Interface (바인딩 지점 목록)

Adapter Interface는 하나의 Adapter가 제공해야 하는 바인딩 지점의 전체 집합이다.

각 바인딩 지점은 Glossary의 "이식 교체 지점(Portability Swap Point)"에 대응하며, 정확히 하나의 Core Contract 요소를 실현한다. 각 지점에 대해: 무엇을 바인딩하는가 / 어느 Core Contract를 실현하는가 / 필수·선택 / 출처.

아래 목록은 01 §4.2 이식 교체 지점 7개, 02 §4.2 SP-1~SP-5, ARCHITECTURE.md 5.1의 영속성 백엔드 지점, 그리고 Wave 3에서 확정된 specs/03~10, 12, 13의 §4.2 이식 교체 지점을 전부 통합·정식화한 것이다. 중복·대응 지점은 기존 BP에 병합하고 출처를 병기했으며(예: BP-9), 어느 기존 BP로도 환원되지 않는 새 바인딩 표면만 BP-13~BP-17로 추가했다.

| BP | 무엇을 바인딩하는가 | 실현하는 Core Contract | 필수/선택 | 출처 |
|---|---|---|---|---|
| BP-1 | Module/Plugin Manifest를 대상 환경의 서술자 포맷으로 직렬화 | Runtime Module 시스템 계약 (01 §3.1-A Register, §3.2-A) | 필수 | 01 §4.2 #1; 10 §4.2-1 |
| BP-2 | Module 정의를 로드해 entrypoint를 해소하는 로더 | Runtime Resolve 연산 (01 §3.1-A) | 필수 | 01 §4.2 #3; 04 §4.2-5 |
| BP-3 | Global/Project/Module 스코프 Config의 물리 소스·위치·로딩 메커니즘 | Runtime Config 계약 (01 §3.1-B, §3.2-B) | 필수 | 01 §4.2 #2; 03 §4.2 SP-4, 12 §4.2-3 |
| BP-4 | Bootstrap~Serve~Shutdown 구간을 담는 실행 프로세스/세션 | Runtime 수명주기 호스팅 계약 (01 §3.1-C) | 필수 | 01 §4.2 #4; 03 §4.2 SP-1, 12 §4.2-7, 13 §4.2-6 |
| BP-5 | Adapter 산출물과 Core를 물리적으로 분리하는 디렉터리·배치 규약 | Runtime 디렉터리/구조 규격 (01 §3.2-E) | 필수 | 01 §4.2 #5; 10 §4.2-1/3, 12 §4.2-4 |
| BP-6 | 확장 Module(확장점·능력·묶음)의 등록·발견·지연 로드·배포 표면 | Runtime 확장 Module 등록 (01 §3.1-A) + 확장 계약 (08·09·10) | 선택 | 01 §4.2 #6; 08 §4.2 SP-1, 09 §4.2 SP-1~5, 10 §4.2-2/3/4/5 |
| BP-7 | Advisor/Planner/Worker/Verifier 4역할 정의를 대상 환경 메커니즘으로 제공 | Agent 역할 경계 (02 §3.2-A) | 필수 | 02 §4.2 SP-1; 06 §4.2 SP-1, 12 §4.2-2, 13 §4.2-2 |
| BP-8 | 공통 규약·시스템 프롬프트·오케스트레이터 진입점 주입 방식 | Agent 공통 의무 (02 §3.1 O1~O5) | 필수 | 02 §4.2 SP-2; 07 §4.2-4, 12 §4.2-1, 13 §4.2-1 |
| BP-9 | 각 Agent 역할의 실행 모델·엔진 지정 | Agent 실행 모델 지정 (02 §4, Glossary §3.2-E); Runtime은 참조만 (01 §4.2 #7) | 필수 | 01 §4.2 #7 ≡ 02 §4.2 SP-3 (병합); 03 §4.2 SP-2, 05 §4.2 SP-4, 06 §4.2 SP-6, 13 §4.2-4 |
| BP-10 | 위임 메시지를 Agent에 전달하는 호출·오케스트레이션 채널 (병렬 디스패치·재위임 포함) | Agent 입력 계약 (02 §3.1, §3.2-B); Runtime entrypoint 입력 (01 §9 조율) | 필수 | 02 §4.2 SP-4; 03 §4.2 SP-2, 05 §4.2 SP-3, 06 §4.2 SP-5, 07 §4.2-2/3, 13 §4.2-3 |
| BP-11 | 완료 보고·실패 보고를 반환하는 결과 채널 | Agent 출력 계약 (02 §3.1, §3.2-C/D); Runtime entrypoint 출력 | 필수 | 02 §4.2 SP-5; 05 §4.2 SP-3, 06 §4.2 SP-4, 07 §4.2-3, 13 §4.2-3 |
| BP-12 | Memory Service 영속성 백엔드 (단일 Port 뒤) | Memory Service Interface 뒤의 저장 메커니즘 (ARCHITECTURE 5.1) | 선택 | ARCHITECTURE 5.1; 01 §5 단서; 04 §4.2-1~4, 05 §4.2 SP-1 |
| BP-13 | 구조화된 계약 산출물·상태 기록의 직렬화 및 작업 추적·결정 기록 메커니즘 | 루프 상태·전이 기록 (03 §3.2-A, INV-3), 검증 리포트 (06 §3.2-A), Work Graph (07 §3.2-A), Install Manifest (12 §3.2-B), 작업 추적 (13 §3.2-A) | 필수 | 03 §4.2 SP-3, 06 §4.2 SP-2, 07 §4.2-1, 12 §4.2-5/6, 13 §4.2 SP-5 |
| BP-14 | 사람에게 승인·개입 요청을 제시하고 응답을 받는 채널 | Loop 사람 개입·에스컬레이션 종료 조건 (03 §3.1-D) | 필수 | 03 §4.2 SP-5 |
| BP-15 | 검증에 쓰이는 검사 도구 (존재 확인·전수 스캔·시연 실행) | Verifier 검출·검증 계약 (06 §3.2-E/F) | 필수 | 06 §4.2 SP-3 |
| BP-16 | 이벤트 원천의 계측·방출 지점과 확장 실행기(결정적 순서·격리)·원천 컨텍스트 전달 | Hooks 이벤트 방출·Dispatch 계약 (08 §3.1-D/E, §3.2-A/C) | 선택 | 08 §4.2 SP-2/3/4/5 |
| BP-17 | 상황 서술자와 적용 조건의 대조 알고리즘 | Lessons 회수·적용 조건 매칭 (05 §3.1-B) | 선택 | 05 §4.2 SP-2 |

병합 근거:
- BP-9: 01 §4.2 #7("Agent 역할 실행 모델 지정")은 01이 "02 §4 소관"으로 위임한 지점이고 02 §4.2 SP-3과 동일 대상이므로 하나로 병합한다.
- BP-13: 03 SP-3(루프 상태 기록)·06 SP-2(검증 리포트)·07 §4.2-1(Work Graph)·12 §4.2-5/6(Install Manifest·버전 값)·13 SP-5(작업 추적·결정 기록)는 모두 "구조화된 계약 산출물·기록을 대상 환경의 서술자·기록 포맷으로 직렬화·추적"하는 동일 바인딩 표면이다. BP-6이 확장 계약 여럿을 하나의 등록 표면으로 실현하는 것과 같은 방식으로, BP-13은 각 spec이 소유하는 §3.2 산출물 스키마(내용은 INV-5에 따라 각 spec 소유)를 실현 대상으로 병기하여 하나의 직렬화·기록 표면으로 통합한다.
- BP-16: 08 SP-2(계측·방출)·SP-3(Dispatch 실행기)·SP-4(순서·격리·비차단)·SP-5(Event Record 직렬화·컨텍스트 전달)는 이벤트 방출·실행이라는 단일 실행 표면의 국면들이므로 하나로 병합한다.
- BP-6 흡수: 08 SP-1(Hook 정의 위치)·09 SP-1~5(Skill 정의·메타/본문 분리·트리거 평가·지연 로드·등록)·10 §4.2-2/3/4/5(포함 Module 등록·install·배포·확장 요소)는 확장 Module의 등록·발견·지연 로드·배포 표면(BP-6)의 상세다. 새 지점을 만들지 않고 BP-6에 흡수하고 출처를 병기한다.

출처 정합성: 01 §4.2 7개 지점과 02 §4.2 SP-1~SP-5는 종전대로 BP-1~BP-11에 반영된다. Wave 3의 §4.2도 전부 반영된다 — 03 SP-1~5(BP-4 / BP-9·BP-10 / BP-13 / BP-3 / BP-14), 04 1~5(BP-12×4 / BP-2), 05 SP-1~4(BP-12 / BP-17 / BP-10·BP-11 / BP-9), 06 SP-1~6(BP-7 / BP-13 / BP-15 / BP-11 / BP-10 / BP-9), 07 1~4(BP-13 / BP-10 / BP-10·BP-11 / BP-8), 08 SP-1~5(BP-6 / BP-16×4), 09 SP-1~5(BP-6×5), 10 1~5(BP-1·BP-5 / BP-6 / BP-5·BP-6 / BP-6 / BP-6), 12 1~7(BP-8 / BP-7 / BP-3 / BP-5 / BP-13 / BP-13 / BP-4), 13 SP-1~6(BP-8 / BP-7 / BP-10·BP-11 / BP-9 / BP-13 / BP-4). 누락 0건.

통합 완료 (Wave 4): 이 목록은 인용 가능 spec(01·02)·ARCHITECTURE.md 5.1에 더해 Wave 3에서 확정된 specs/03~10, 12, 13의 §4.2 이식 교체 지점을 전부 통합·정식화한 것이다. 기존 BP-1~BP-12에 대응하는 지점은 해당 BP 행의 출처에 병기했고, 어느 기존 BP로도 환원되지 않는 새 바인딩 표면만 BP-13~BP-17로 추가했다. 이로써 §9-OQ-1이 해소된다.

### 3.2-B Conformance Criteria (적합성 판정 기준)

**유효한 Adapter (Valid)**
C1·C2·C3(§3.1)을 모두 만족하는 구현이다. 즉 필수 바인딩 전부 제공 + Core Contract 수정 0건 + 핵심 루프 1회 통과.

Adapter는 등급을 갖는다.

**완전 Adapter (Full Adapter)**
C1~C3을 만족하고, 선택 바인딩(BP-6 확장 표면, BP-12 영속성 백엔드, BP-16 이벤트·Hook Dispatch, BP-17 적용 조건 매칭)까지 기능 완성 수준으로 제공한다.

**최소 구현 Adapter (Minimal Adapter)**
C1~C3을 만족하되, 각 필수 바인딩의 내용은 핵심 루프 1회 통과에 필요한 최소 수준이면 된다. 선택 바인딩(BP-6, BP-12, BP-16, BP-17)은 생략할 수 있다.

- 목적: Adapter Interface가 실제로 다른 AI에 적용 가능함을 증명하는 것이다. 기능 완성이 아니다 (ROADMAP v1.0).
- **최소 바인딩 부분집합(정본)**: BP-1, BP-2, BP-3, BP-4, BP-5, BP-7, BP-8, BP-9, BP-10, BP-11, BP-13, BP-14, BP-15 (필수 13개). BP-6·BP-12·BP-16·BP-17은 제외 가능하다.
- 판정 용도: v1.0의 2nd Adapter 판정이 이 기준으로 이루어진다. 이 부분집합을 전부 제공하고 C2·C3을 만족하면 유효(최소)로 판정한다.

부분집합 재검토 완료 (Wave 4): Wave 3 통합에서, 핵심 루프(위임→구현→검증→승인) 1회 통과에 필수인 BP-13(계약 산출물·기록 직렬화 및 작업 추적; 근거 03 INV-3 모든 전이 기록·13 §3.2-A 작업 추적 필수)·BP-14(사람 승인·개입 채널; 근거 03 §3.1-D 사람 개입 종료 조건)·BP-15(검사 도구; 근거 06 검증 노드 수행에 필수)가 최소 바인딩 부분집합에 편입되어 정본 부분집합이 10개에서 13개로 확대되었다. BP-16·BP-17은 확장·회수 표면으로 선택에 남는다. 이 변경은 v1.0 2nd Adapter 판정 기준에 반영된다.

### 3.2-C Adapter 구조 규격

- **자기완결성(self-contained)**: 하나의 Adapter는 자신의 모든 바인딩을 하나의 경계 안에 둔다.
- **물리적 분리**: Adapter 산출물은 Core 디렉터리와 물리적으로 분리된 별도 경계에 둔다 (01-runtime §3.2-E). Core 디렉터리에는 AI 의존 요소 0건이 유지된다 (01-runtime INV-4).
- **명명·배치**: Adapter는 `adapters/<이름>/` 아래에 배치한다. `<이름>`은 안정적 식별자다. 첫 번째 Adapter의 실명 경로는 §4·§8에 둔다.

### 3.2-D Conformance Report

Adapter 적합성 판정의 공통 보고 구조다.

| 필드 | 의미 |
|---|---|
| `adapter` | 판정 대상 Adapter 이름. |
| `verdict` | `Valid(Full)` / `Valid(Minimal)` / `Invalid`. |
| `missing_bindings` | 누락된 필수 바인딩 지점 목록 (C1 검사 결과). 유효하려면 비어 있어야 한다. |
| `core_modifications` | 발견된 Core Contract 수정 목록 (C2 검사 결과). 유효하려면 0건이어야 한다. |
| `loop_pass` | 핵심 루프 통과 여부와 근거 (C3 검사 결과). |
| `notes` | 선택 바인딩(BP-6·BP-12·BP-16·BP-17) 제공 여부 등 등급 판정 부가 정보. |

---

## 3.3 Invariants

- **INV-1 (Core 불변).** Adapter는 Core Contract를 수정하지 않는다. 바인딩만 추가한다. Core Contract 수정이 1건이라도 발견되면 Invalid다 (C2).
- **INV-2 (필수 완전성).** 필수(mandatory) 바인딩 지점을 전부 제공해야 유효한 Adapter다 (C1).
- **INV-3 (물리적 분리).** Adapter 산출물은 Core 디렉터리와 물리적으로 분리된다 (01-runtime §3.2-E). Core 디렉터리에 AI 의존 요소는 0건이다 (01-runtime INV-4).
- **INV-4 (지점당 단일 표면 실현).** 각 바인딩 지점은 Glossary "이식 교체 지점"에 대응하며, 정확히 하나의 계약 표면(contract surface)을 실현한다. 하나의 표면은 동일 성격의 Core Contract 요소 집합을 묶을 수 있다 (예: BP-6 확장 표면, BP-13 기록 직렬화, BP-16 이벤트 실행 — §9 결정 기록 참조).
- **INV-5 (경계 불가침).** Adapters는 각 컴포넌트의 Core Contract 내용을 정의하지 않는다. 바인딩 지점의 목록과 적합성만 소유한다. 타 컴포넌트 계약은 인용만 한다.
- **INV-6 (자기완결).** Adapter는 자기완결적이다. 모든 바인딩을 `adapters/<이름>/` 경계 안에 둔다.
- **INV-7 (§3 AI 비의존).** §3의 어떤 내용도 특정 AI 모델·실행 환경에 의존하지 않는다. 첫 번째 Adapter의 실명 바인딩은 §4에만 둔다.
- **INV-8 (동일 계약 실현).** 동일 Core Contract는 두 Adapter 모두에서 그대로 실현된다. Adapter 교체가 Core를 바꾸지 않는다 (ARCHITECTURE.md 3.1).

---

# §4. Adapter Binding (환경 의존)

## 4.1 Claude Code Binding — 첫 번째 Adapter

Claude Code Adapter는 UAHF의 첫 번째 Adapter다 (ARCHITECTURE.md 3.1 "Claude는 첫 번째 Adapter일 뿐이다"). 배치 경로는 `adapters/claude/`이며, v0.9에서 v0.2~v0.8 동안 각 spec §4에 분산 정의된 바인딩들이 이 규격 아래로 정식화된다 (ROADMAP v0.9).

아래는 §3.2-A 각 바인딩 지점의 Claude Code 바인딩 값이다. 값은 01 §4.1과 02 §4.1에서 통합한다.

| BP | Claude Code Adapter 바인딩 값 | 출처 |
|---|---|---|
| BP-1 | Markdown + front-matter 파일로 Manifest 직렬화 | 01 §4.1 |
| BP-2 | 파일 기반 정의 로딩 (`.claude/` 하위 정의 파일 로더) | 01 §4.1 |
| BP-3 | Global: 사용자·환경 전역 설정 파일 / Project: `.claude/CLAUDE.md`, `.claude/AGENT.md`, `settings.json` 등 / Module: 각 정의 파일 내부 설정 블록 | 01 §4.1 |
| BP-4 | Claude Code 세션/턴 = Bootstrap~Serve~Shutdown 실행 컨테이너 | 01 §4.1 |
| BP-5 | Core: `framework/core/`, `framework/runtime/` (AI 의존 0건) / Adapter 산출물: `framework/adapters/`, `.claude/` | 01 §4.1 |
| BP-6 | `.claude/commands/`, `.claude/hooks/`, `.claude/skills/` (상세 08·09·10) | 01 §4.1 |
| BP-7 | `.claude/agents/{advisor,planner,worker,verifier}.md` | 02 §4.1 |
| BP-8 | `.claude/AGENT.md`(상위 규약), `.claude/CLAUDE.md`(Advisor 진입점 바인딩) | 02 §4.1 |
| BP-9 | Worker 기본 실행 모델 = Opus; 기타 역할의 모델 지정 | 02 §4.1 |
| BP-10 | 서브에이전트 위임으로 위임 메시지(02 §3.2-B) 전달 | 02 §4.1 |
| BP-11 | 서브에이전트 최종 응답으로 완료·실패 보고(02 §3.2-C/D) 회수 | 02 §4.1 |
| BP-12 | 파일 기반 store·index·직렬화·I/O를 단일 Port 뒤 `framework/adapters/`에 격리 | ARCHITECTURE 5.1; 04-memory §4.1 |
| BP-13 | 구조화 파일 기반 기록 — 루프 상태 로그/마크다운, 검증 리포트 파일, 계획·로드맵 문서(Work Graph), 설치 매니페스트 파일; 작업 추적은 Wave 단위 위임·검증 사이클과 Open Questions·결정 기록 관행 | 03 §4.1, 06 §4.1, 07 §4.1, 12 §4.1, 13 §4.1 |
| BP-14 | Claude Code 세션에서 사용자에게 승인·개입 요청 제시; `.claude/CLAUDE.md`의 "Architecture/Spec 충돌 시 사용자 보고" 규칙 | 03 §4.1 |
| BP-15 | Claude Code 표면의 검사 도구 — 파일 조회, 텍스트 검색, 명령 실행 등(존재 확인·전수 스캔·시연 실행) | 06 §4.1 |
| BP-16 | Claude Code 세션/턴의 이벤트 원천 계측 + 하네스 hook 실행 메커니즘(결정적 순서·격리) + 원천 컨텍스트의 읽기 전용 전달 (`.claude/hooks/`, `.claude/settings.json` hooks) | 08 §4.1 |
| BP-17 | 상황 서술자 ↔ `applicability` 대조 알고리즘 (키워드·의미 검색 등) — Adapter/04 구현 선택 | 05 §4.1 |

Claude Code Adapter는 선택 바인딩(BP-6·BP-12·BP-16·BP-17)까지 포함하므로 완전 Adapter(Full Adapter)를 목표로 한다.

## 4.2 이식 교체 지점 (Portability Swap Points)

이 spec은 이식 교체 지점의 통합 정본이다. §3.2-A의 바인딩 지점 목록 자체가 모든 이식 교체 지점을 통합한 것이다.

다른 AI 환경으로 이식할 때 §4.1의 Claude 바인딩 값을 §3.2-A 각 지점의 대상 환경 값으로 교체한다. Core Contract(§3)는 유지된다.

두 번째 Adapter는 `adapters/openai/` 또는 `adapters/generic/`에 배치한다 (ROADMAP v1.0). 최소 구현 Adapter는 §3.2-B의 최소 바인딩 부분집합(BP-1~5, BP-7~11, BP-13~15)만 대상 환경 값으로 교체하고, 선택 바인딩(BP-6·BP-12·BP-16·BP-17)은 생략할 수 있다.

---

# §5. Memory Access (해당 시)

해당 없음.

Adapters spec은 Memory를 읽거나 쓰지 않는다. Memory Service Interface(단일 Port)에 접근하지 않으며, Memory 내용을 다루지 않는다.

구분 (불변): BP-12는 Memory Service의 영속성 백엔드를 단일 Port 뒤에 바인딩하는 "바인딩 지점"이다. 이는 Memory "내용" 접근이 아니라 저장 메커니즘의 바인딩이다. Adapter는 백엔드를 배치·바인딩할 뿐 Memory 내용을 회수·기록하지 않는다. 이 구분은 01-runtime §5 단서(Runtime은 Memory Service를 배선만 하고 내용에 접근하지 않음)와 동일하다.

---

# §6. Failure Modes

대표 실패 시나리오와 대응이다. 모두 Lesson 후보다.

| 실패 시나리오 | 대응 | Lesson 후보 |
|---|---|---|
| Adapter가 Core Contract를 수정해 이식 | INV-1 위반. Conformance Invalid(core_modifications 명시). | 예 |
| 필수 바인딩 지점 누락 | INV-2 위반. Conformance Invalid(missing_bindings 명시). | 예 |
| Adapter 산출물이 Core 디렉터리에 침투(AI 의존 요소 혼입) | INV-3, 01-runtime INV-4 위반. 경계 검증(§7) 실패. | 예 |
| Adapters spec이 타 컴포넌트 Core Contract를 임의로 정의 | INV-5 위반. 바인딩 지점 목록·적합성만 소유하도록 교정. | 예 |
| 바인딩 지점이 실제 Core Contract 요소를 실현하지 못함 | INV-4 위반. 지점과 계약 요소의 대응을 재확인. | 예 |
| 최소 구현 Adapter를 완전 Adapter로 오판(또는 그 반대) | §3.2-B 등급 기준으로 판정. notes에 선택 바인딩 제공 여부 기록. | 예 |
| 핵심 루프 미통과 상태로 유효 판정 | C3 위반. loop_pass 근거 없이는 Valid 불가. | 예 |

---

# §7. Verification

## 완료 기준 (시연 가능 문장)

ROADMAP v0.9·v1.0 완료 조건과 정렬한다.

- **완전 Adapter 판정 시연.** 첫 번째 Adapter가 §3.2-A의 필수 바인딩 전부 + 선택 바인딩을 제공하고, Core 수정 0건이며, 핵심 루프가 1회 통과함을 보여 verdict=Valid(Full)로 판정됨을 시연한다.
- **최소 구현 Adapter 판정 시연.** 두 번째 Adapter가 최소 바인딩 부분집합(BP-1~5, BP-7~11, BP-13~15)만 제공하고 BP-6·BP-12·BP-16·BP-17을 생략하며, Core 수정 0건, 핵심 루프 1회 통과로 verdict=Valid(Minimal)로 판정됨을 시연한다 (ROADMAP v1.0 2nd Adapter 판정).
- **Core 무수정 시연.** 두 Adapter 교체 전후 Core 디렉터리 diff가 0이고, Core에 AI 의존 요소가 0건임을 보인다 (ARCHITECTURE 3.1, ROADMAP v0.9·v1.0 경계 검증).
- **동일 Core Contract 시연.** 같은 위임 → 구현 → 검증 → 승인 핵심 루프가 두 Adapter 모두에서 통과함을 보인다 (INV-8, "Adapter만 교체하면 이식된다" 실증).
- **경계 시연.** §3 본문에 특정 AI 모델·실행 환경 의존 토큰이 0건임을 보인다 (INV-7).

## 검증 방법

- Verifier가 Adapter별로 §3.2-A 필수 바인딩 지점 체크리스트를 대조한다(C1).
- Verifier가 Adapter 적용 전후 Core 디렉터리를 diff 하고 금지 토큰(특정 AI·모델명·제품 기능)을 스캔해 수정·오염 0건을 확인한다(C2, INV-3).
- Verifier가 두 Adapter에서 동일 핵심 루프 통과 기록을 대조한다(C3, INV-8).
- Verifier가 §3 본문을 스캔해 AI 의존 토큰이 0건임을 확인한다 (DoD-3, INV-7).
- Advisor가 Conformance Report를 검토해 최종 승인한다.

---

# §8. Examples

**예 1 — 최소 구현 Adapter 판정 (2nd Adapter, ROADMAP v1.0)**

대상: 두 번째 Adapter (`adapters/openai/` 또는 `adapters/generic/`).

- 제공한 바인딩: BP-1, BP-2, BP-3, BP-4, BP-5, BP-7, BP-8, BP-9, BP-10, BP-11, BP-13, BP-14, BP-15 (최소 부분집합 전부). BP-6(확장 표면)·BP-12(영속성 백엔드)·BP-16(이벤트·Hook Dispatch)·BP-17(적용 조건 매칭) 생략.
- Core 수정: 0건.
- 핵심 루프: 위임 → 구현 → 검증 → 승인 1회 통과.

Conformance Report:
- `adapter`: 2nd Adapter
- `verdict`: Valid(Minimal)
- `missing_bindings`: 없음 (필수 전부 제공)
- `core_modifications`: 없음
- `loop_pass`: 예 — 핵심 루프 1회 통과 로그
- `notes`: 선택 바인딩 BP-6·BP-12·BP-16·BP-17 미제공 (최소 구현)

판정: 유효(최소). Adapter Interface가 다른 AI에 적용 가능함을 실증하여 Architecture Validation을 충족한다.

**예 2 — Core 무수정 교체 검증**

동일한 위임 → 구현 → 검증 → 승인 핵심 루프를 첫 번째 Adapter(완전)와 두 번째 Adapter(최소) 각각에서 실행한다.

- Core 디렉터리(`framework/core/`, `framework/runtime/`) diff = 0. 두 Adapter 실행 사이 Core 변경 없음.
- 동일 Core Contract(위임 메시지·완료 보고의 필수 필드, 역할 경계, Runtime Module 계약)가 두 Adapter 모두에서 그대로 실현됨.
- 교체 대상은 §3.2-A 바인딩 지점의 값(§4.1 → 대상 환경 값)뿐이었음.

결론: "Adapter만 교체하면 이식된다"가 성립한다 (ARCHITECTURE.md 3.1, INV-8).

---

# §9. Open Questions

Advisor 에스컬레이션 대상.

- **OQ-1 (해소 완료 — Wave 4) — 03~10·12·13 §4 바인딩 지점 통합.**
  해소 완료(Wave 4): 03~13 §4.2를 §3.2-A에 통합 반영했다. 기존 BP-1~BP-12에 대응하는 지점은 각 BP 행의 출처에 병기했고, 어느 기존 BP로도 환원되지 않는 새 바인딩 표면만 BP-13(계약 산출물·기록 직렬화 및 작업 추적), BP-14(사람 승인·개입 채널), BP-15(검사 도구), BP-16(이벤트 계측·방출 및 Hook Dispatch 실행), BP-17(적용 조건 매칭)으로 추가했다. **최소 부분집합 변경:** BP-13·BP-14·BP-15가 필수로 편입되어 최소 바인딩 부분집합이 10개(BP-1~5, BP-7~11)에서 13개(+BP-13·BP-14·BP-15)로 확대되었다 (근거: 03 INV-3 모든 전이 기록, 03 §3.1-D 사람 개입 종료, 06 검증 노드의 검사 도구, 13 §3.2-A 작업 추적 필수). BP-16·BP-17은 선택으로 남는다. dependents(§2) 재검토: 03~13은 §4.2에서 11을 "정식화 주체"로 가리키는 전방 참조만 두며 각 Core Contract(§3)가 11에 의존하지 않으므로 새 Core Contract dependent는 없다(§1 순환 의존 논거와 동일). 이 항목은 더 이상 Frozen을 막지 않는다.

- **OQ-2 (Glossary 추가 요청) — 신설 개념의 정본화.**
  이 spec이 형식화하지만 Glossary §3.2에 정본 항목이 없는 용어. Glossary §9-OQ6 흐름(각 spec 선언 → Advisor 통합)에 따라 추가를 요청한다. 확정 전까지 새 정의를 만들지 않고 아래 표현을 잠정 사용한다.
  - Glossary 추가 요청: Adapter Interface — 하나의 Adapter가 반드시 제공해야 하는 바인딩 지점의 전체 집합. (ROADMAP v0.9·v1.0에서 사용되나 Glossary 정본 없음.)
  - Glossary 추가 요청: 바인딩 지점 (Binding Point) — Adapter가 하나의 이식 교체 지점을 실제로 바인딩하는 단위. 정확히 하나의 Core Contract 요소를 실현한다.
  - Glossary 추가 요청: Conformance (적합성 판정) — 어떤 구현이 유효한 Adapter인지의 판정 (필수 바인딩 완전성 + Core 불변 + 핵심 루프 통과).
  - Glossary 추가 요청: 완전 Adapter (Full Adapter) / 최소 구현 Adapter (Minimal Adapter) — Conformance 등급 두 종. 최소 구현 Adapter의 정의는 §3.2-B가 정본이다.
  - Glossary 추가 요청: 핵심 루프 (Core Loop) — 위임 → 구현 → 검증 → 승인 사이클. (ROADMAP v0.2·v1.0에서 사용되나 Glossary 정본 없음.)

- **OQ-3 (인용 정합성 주의 — 비차단) — "INV-4" 중복 참조.**
  "Core 디렉터리 AI 비의존" 불변을 참조할 때 이 spec은 01-runtime INV-4를 지칭하며, Glossary INV-4(모든 spec은 Glossary 용어만 사용)와 구분한다. 충돌이 아니라 동명(同名) 식별자다. 이 spec은 인용 시 소속 spec을 명시했다(예: "01-runtime INV-4"). Advisor가 다른 spec에서도 동일 표기를 유지하는지 확인할 것을 권한다.

- **OQ-4 (경계 확인 — 비차단) — 타 컴포넌트 계약 소유권.**
  Adapters는 각 컴포넌트 Core Contract 내용을 소유하지 않는다(INV-5). BP-6(확장 표면)의 상세는 08·09·10 §4가, BP-12(영속성 백엔드)의 상세는 04-memory §4가 확정한다. 이 spec은 지점 목록만 갱신하고 계약 내용은 인용만 한다. 이 항목은 Frozen을 막지 않는다.

- **ARCHITECTURE 충돌:** 발견되지 않음. §3은 ARCHITECTURE.md 3.1(AI Agnostic)·5.1(Memory 단일 Port·영속성 백엔드)·7(Non Goals)·8(Adapter 확장)에 정렬한다. Spec 수정 대상 충돌 없음.

## 결정 기록 (Advisor — Wave 4 통합)

- BP-13~BP-17 신설과 기존 BP로의 병합·출처 병기를 승인한다. **최소 바인딩 부분집합 10개 → 13개(BP-13/14/15 편입) 확정** — v1.0 2nd Adapter 판정 기준은 이 13개가 정본이다.
- 재량 판정 1 승인: BP-13·BP-16의 복합 실현은 INV-4를 "지점당 단일 계약 표면 실현"으로 정밀화하여 해소했다. 하나의 표면은 동일 성격의 Core Contract 요소 집합을 묶을 수 있다.
- 재량 판정 2 승인: 13 §4.2 SP-5(작업 추적·결정 기록)의 BP-13 병합 — 03 INV-3(모든 전이 기록)과 13 §3.2-A(작업 추적은 최소 구성 필수)가 동일한 기록·추적 표면을 요구하므로 타당하다.
- 재량 판정 3 승인: Plugin 배포 채널(10 §4.2-4)의 BP-6 흡수 — 배포는 확장 표면의 한 국면이다. v0.8 구현에서 분리 필요성이 확인되면 재검토한다.
