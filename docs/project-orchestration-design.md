# Project Orchestration / Dynamic Agent System — 설계 정본

작성: Advisor · 2026-07-13
상태: 설계 확정 (사용자 승인 2026-07-13 — Phase A~E 플랜 게이트 통과 · 구조 대안 3안 중 대안 B 채택) + **배치 재검증 게이트 확정 (사용자 결정 2026-07-13)**: ① 소유·배치 = **UAF 레벨 신규 Layer `orchestration/`** (루트 §2.3 "Agentic Runtime (향후)" slot의 실현로 귀속 — 플랜 원안의 UAHF 내부 v1.6 프레이밍을 대체) ② UAHF 접촉 = **라이브러리 재사용** (step-host 중립 모듈 무수정 import — 루트 §2.5 "상위만이 하위를 안다"의 허용 방향) + **v1.6 Baseline 확정(2026-07-13 사용자 승인 · 번호 v1.6 부여 · 루트 `ARCHITECTURE.md` v1.5 §2.1 라우터 등재 · ROADMAP 등재)**
입력: 사용자 지시 13절(2026-07-13 — Project Orchestration 설계 착수 요청) · 저장소 Ground Truth 실측(Explore 2기: 상류 계층·실행 계층 + Advisor 하중 앵커 교차 재확인) · Superpowers v6.1.1 웹 조사(Adopt/Adapt/Reject/Defer Matrix 16항)
성격: 마일스톤 설계 정본. 계약 정본은 이 문서가 아니라 각 spec·프로토콜 문서·바인딩이 소유한다(재정의 0 — 충돌 시 정본 우선·Advisor 보고). 버전 번호 = **v1.6**(2026-07-13 Baseline 사용자 게이트에서 부여).

---

## §0. 목적 — 파이프라인 종단과 실행 계층을 잇는 오케스트레이션 공백을 기존 구조 위에서 메운다

새 Workflow Engine·Planning Engine·Runtime을 만들지 않는다. 다음 두 실측 공백(Phase A Ground Truth 판정)만 v1.5 확장 패턴(Frozen spec 무수정 + `runtime/` 프로토콜 + `framework/` 중립 코드 + adapter 바인딩)으로 메운다:

1. **파이프라인 종단 연결의 부재** — 04-solution-design §3.1-D는 종단(Matured/Skipped) 이후 UAHF 착수를 사용자 소관으로 남겼고(형태 A에서는 사람이 handoff를 나름), 루트 ARCHITECTURE.md §11은 "Layer 연결·오케스트레이션 정식화"를 후속 트랙에 예약했다. 본 트랙이 그 후속 트랙이며, 04 §3.9 확장 포인트 1(형태 B 실행 호스팅)·2(step 기반 실행기와의 연결)의 실현이다.
2. **프로젝트 단위 동적 조율의 부재** — 현행 최상위 스케줄 단위는 단일 Work Graph(1 run)다. 진행 중 새 Task 발견(설계 후 구현 task 확정)을 표현할 표면·Expert Role→실행 주체 매핑·게이트 정책 데이터·Artifact 계보·모델 선택 정책이 없다.

목표 실행 흐름(사용자 §1 — 단, **고정 파이프라인으로 하드코딩하지 않는다**. 어떤 작업 단위가 필요한가는 데이터다):
```
User Intent → Discovery/Clarification → Project Contract → [Solution Design 성숙 루프]
→ Work Decomposition → Dynamic Role/Agent Allocation → 독립/협업 작업(fresh context)
→ Artifact Handoff → Review/Gate → 기존 Step Host 실행 계층
```

우선순위(사용자 고정): God PM Agent 금지 · 고정 파이프라인 금지 · Agent-모델 결합 금지 · Chat history 공유 기본 협업 금지 · 기존 기능 재구현 금지 · 최소 신규 추상화 · 검증 가능한 순서.

## §1. 채택 구조 — 대안 B: Deterministic Project Orchestrator + LLM 판단의 Step 국소화

3안 비교(플랜 Phase C — A: 중앙 Coordinator Agent = God PM 저촉으로 기각 · C: Phase Coordinator 연합 = 국면 데이터화 시 B로 수렴하여 흡수) 후 채택. **v1.5 Step Host 패턴("판단하지 않는 기계 구동자")의 프로젝트 레벨 확장**이다 — 단, 이는 **패턴**(deterministic 구동자 + LLM 국소화 + append-only + 게이트 코드 강제)의 확장이지 **UAHF 내부로의 편입이 아니다**. Project Orchestration은 Discovery·Planning 산출물을 인수하여 프로젝트 완료까지 전체 lifecycle을 관리하며 UAHF를 execution substrate로 소비하는 **UAF 레벨 상위 컴포넌트**다(루트 §2.5 단방향 의존 — 상위만이 하위를 안다·§2.3 Agentic Runtime slot). 디스패치 입도는 run/작업 단위이지 개별 step이 아니다 — 단일 run의 무인 관리는 Step Host가 완결 소유하며 재구현하지 않는다.

"PM Agent"는 3분해되어 소멸한다:

| 책임 | 소유 주체 | 성격 |
|---|---|---|
| 기계적 조율 — 스케줄(ready_set)·게이트 강제·재시도·재개·기록·정책 평가·revision 검증·artifact 인덱스 | **Project Orchestrator** (중립 Runtime 컴포넌트) | deterministic·판단 0 (SH-INV-1 동형) |
| 의미 판단 — 설계 Proposal·분해 제안·역할 할당 제안·리뷰 판정·모호성 해소 | 국소 fresh-context **Step** (02 4역할 Lifecycle 의무 + 04 §3.3 Expert Role capability) | LLM — 격리 번들 입력·요약 반환 |
| 확정 권위 — Contract 확정·성숙 승인·실행 착수·중대 결정 | **사용자** (UAF-INV ⑤) | 게이트 큐 경유 |

**사용자 대화 주체와 orchestrator는 분리한다.** orchestrator는 headless다. 사용자 채널은 (i) 진입/대화 세션(형태 A — Discovery Eliciting·게이트 제시), (ii) **게이트 큐**(Escalated 이벤트 + gateKind + scoped question의 파생 뷰)뿐이다. 게이트가 이벤트로 영속하므로 orchestrator 크래시에도 대화 상태가 보존된다.

## §2. 충돌 검증 결과 (기존 spec·불변·예약 지점 대조)

**판정: 차단 충돌 0. 프레이밍·배치 결정은 사용자 게이트 2회로 확정(플랜 게이트 + 배치 재검증 게이트).**

| 대조 대상 | 근거 | 판정 |
|---|---|---|
| UAF-INV ① (UAHF 무수정) + 루트 §2.5 (UAHF는 상류를 모른다) | 정본·중립 코드는 **UAF 레벨 신규 Layer `orchestration/`** 소유 — uahf/ 정본·코드 무촉(v1.1 선례: UAF 레벨 신설·UAHF 무수정). uahf/ 트리 접촉은 정확히 2건만: (i) `project-orchestration-binding.md` 신설 — UAF 레벨 바인딩 5종째를 Adapter 물리 경계에 동거(contract/entry/discovery/solution-design-binding 선례·DP-X4 비합산) (ii) OQ-SH-4 해소 1개소(host.py — 플랜 게이트 승인분). 프로토콜 의미론이 상류(Discovery·SD)를 아는 것은 **UAF 레벨 문서이므로 정합**(uahf/ 내부였다면 §2.5 위반 외양) | 사용자 결정(2026-07-13)으로 해소 — 본 트랙 = **UAF 레벨 트랙** |
| uahf/specs 00~13 Frozen | 개정 0건 — 07 Work Graph·Task·02 위임 8필드·03 이벤트 스키마·06 CP2 전부 § 포인터 인용만 | 충돌 0 |
| 04-solution-design (Baseline v1.3) | 04 무수정 — §3.9 확장 포인트 1·2를 외부 프로토콜·바인딩이 실현(v1.5 처리 동형) | 충돌 0 |
| step-hosting-protocol·step-host/ | 프로토콜 본문 무변(§9 이력 append 후보만) · 코드는 **OQ-SH-4 해소 1개소만 수정**(`_dispatch_cp2` — 비Frozen Module 경계·테스트 갱신 동반·명시 변경으로 표기) | 변경 최소·명시 |
| 07 Frozen에 그래프 변경 연산 부재 | Graph Revision은 07 재정의가 아니라 "신규 발견 작업에 대한 **Decompose 반복 실행 산출의 append-only 합성**" — 각 revision epoch의 파생 그래프는 07 §3.2-A를 온전히 만족하는 Work Graph 1건 | 신규 프로토콜 영역으로 프레이밍(§3.2) — 07 문면 계약 변경 0 |
| 루트 §2.5 "UAHF는 Discovery를 모른다" | 중립 orchestrator 코드에 업스트림 Layer 고유명 토큰 0 — capability 문자열은 불투명 데이터. 프로토콜 **문서**의 상류 인용은 step-hosting-protocol이 02-discovery·04를 근거 정본으로 인용한 선례로 허용 | 충돌 0 |
| Glossary INV-3 (Component 13·Layer 6) | 새 Component·Layer·spec 창설 0 — Orchestrator는 07 다중 사이클 오케스트레이션 + 01 Serve 구간의 형태 B 실현이며 Step Host의 자매(두 번째 Runtime 아님) | 충돌 0 |
| SH-INV 1~8 | 전건 상속·확장(PO-INV로 동형 승계 — §3.8) | 충돌 0 |
| Memory INV-1 (단일 Port) | orchestrator 중립 코드의 Memory 직접 접근 0 — 기존 두 경로(위임자 Recall→context / 실행 단위 자체 Consult)만 (SH-INV-5 동형) | 충돌 0 |
| UAF-INV ⑤·SH-INV-4 | Gate Policy는 코드 소유 하한을 약화 불가(단조성 — §3.3). Autonomy 3값(도구 승인 축)과 직교 유지 | 충돌 0 |

## §3. 아키텍처

### §3.1 Project Work Graph — 07 스키마의 상위 입도 재사용 (새 실행 단위 계약 0)

**Project Work Graph = 07 §3.2-A Work Graph 스키마 그대로.** 단 Task의 입도가 코드 구현만이 아니라 **프로젝트 작업 단위**(예: discovery unit·maturation unit·decompose unit·implementation step 집합·review unit)다. 작업 단위 **유형은 개방 네임스페이스·데이터**이며 코어는 유형 카탈로그를 열거하지 않는다(고정 파이프라인 하드코딩 금지 — 예시는 비정본 부록 소관, SP-INV 5 동형). 각 단위는 v1.5 Step(07 Task + 02 위임 8필드 + role/capability/model 슬롯)으로 직렬화된다.

프로젝트 그래프의 초기 구성(어떤 단위가 필요한가)은 Entry Resolution 결과 + 복잡도 판정(04 §3.2)의 **데이터**다 — 단순 프로젝트는 단일 Work Graph 직행(성숙 스킵 경로 동형), 복잡 프로젝트만 다단 단위 구성.

### §3.2 Graph Revision Ledger — 동적 그래프의 append-only 실현

07 Work Graph는 Decompose 1회의 정적 산출이다. 진행 중 그래프 확장은 **Graph Revision Ledger**로 실현한다:

```
RevisionEvent {
  revisionSeq   // 전순서
  kind          // task_added | dependency_added | task_superseded
  payload       // 07 §3.2-B Task 전 필드 (계약 재정의 0)
  basis         // { proposingStepRef, gateEventRef } — 근거 없는 그래프 변경 0 (PO-INV 5)
}
현재 그래프 = fold(revision events, 초기 그래프)
```

- **SH-INV-2 양립**: revision ledger 자체가 append-only·현재 그래프는 파생 뷰. `task_superseded`는 삭제가 아니라 superseding 포인터 append(과거 문면 불변 — PC-INV 9 동형).
- **SH-INV-3 양립 조건 3건 (프로토콜 필수 조항)**: ① 전순서 — revisionSeq + gateEventRef 인과 고정(게이트 통과 이벤트 append 후에만 revision append 가능) ② 안정 정렬 — orchestrator는 (revisionSeq, payload 선언 순서)로 step 집합을 공급해 ready_set 순서 결정성 보존 ③ 검증의 결정성 — revision 수용 검증(스키마 완전성·순환 0·같은 병렬 집합 내 ownedBoundary 비중첩)은 순수 함수이며 실패는 07 §3.1-A 사유 코드 재사용. 의미 수용 여부는 게이트 소유(판단 0 보존).
- `dependsOn`은 미래 task를 선참조할 수 없으므로(07 R2 추측 금지) "설계 후 구현 task 확정" 패턴은 자연히 "설계 단위 Passed → 산출 artifact 기반 구현 task 제안(LLM step) → 게이트 → revision append"의 인과 사슬이 된다.

### §3.3 Gate Policy — 5종 어휘·데이터·단조성

```
GatePolicyEntry { target: (단위 유형 | 전이 | artifact class), gate: gateKind }
gateKind ∈ { auto_continue, review_required, approval_required,
             escalation_required, user_decision_required }
```

| gateKind | 기존 계약 매핑 |
|---|---|
| `auto_continue` | 추가 게이트 0 — 단 CP2는 불변 하한(SH-INV-4 "CP2 우회 없음") |
| `review_required` | CP2 외 **추가** 독립 리뷰 단위 디스패치(Verifier 역할·VT-1~5 재사용) |
| `approval_required` | 경계에서 CP3(Advisor **역할** 승인 — 사람 아님·무인 양립) 강제 |
| `escalation_required` | `Escalated` 정지 — Advisor/사람 해소 이벤트로 재개(03 §3.1-D) |
| `user_decision_required` | `Escalated` 정지 — **사용자 응답 이벤트만** 해소 가능(UAF-INV ⑤·04 T8/T9/T10의 물리화) |

**게이트 단조성(PO-INV 4)**: 정책은 코드 소유 하한 — CP2 상시·03 §3.1-D 조건 2~5·Contract Ready/Matured·실행 착수(04 §3.1-D Handoff) 지점의 `user_decision_required` — 을 **약화할 수 없고 강화만** 할 수 있다. Autonomy Policy 3값(interactive/auto_approve/unrestricted — 도구 승인 축)과 직교: `unrestricted`에서도 5종 게이트는 전부 작동한다(v1.5 E2E s5 확장 실증 대상).

### §3.4 Dynamic Agent Allocation — Role / AgentSpec / Instance 3층 + 02 4역할 병존

| 층 | 정의 | 소유 |
|---|---|---|
| **Role** (논리) | 04 §3.3 Expert Role {roleId, capability, inputContract, outputContract} — 개방 네임스페이스·최소 할당(SP-INV 8). 02 4역할(Advisor/Planner/Worker/Verifier)은 **Lifecycle 의무 축**으로 병존 — Expert Role은 그 위의 capability 내용 축 | 04 (무수정 인용) |
| **AgentSpec** (실행 프로파일) | {specId, capability selector, brief 템플릿 참조, 기본 constraints, tool policy class, model policy class}의 **버전 있는 데이터 레코드**. capability 선언으로 검색·선택(Capability First). 물리 실현 예 = 하네스 역할 정의 파일이나 코어는 불투명 참조만 | 신규 스키마(중립 모듈) + 실값은 adapter 레지스트리 데이터 |
| **Instance** | 한 Step attempt의 fresh-context 1회 실행 {runId, stepId, attempt}. **비영속** — 정체성은 이벤트 로그에만 존재. 상주 인스턴스·chat history 공유 없음(SH-INV-8) | 이벤트 로그 파생 |

할당 근거 = Contract/SD 산출 · 복잡도 판정(04 §3.2) · capability 매칭 · 최소 할당(SP-INV 8). **할당 "제안"은 LLM step이 산출하고, 수용은 게이트가 소유한다** — orchestrator는 매칭 정책의 deterministic 평가만 수행한다.

### §3.5 Dynamic Model Allocation — Model Selection Policy as Data

- 입력 축: capability class(예: 기계적/통합/설계·최종리뷰 — Superpowers "역할을 처리할 수 있는 가장 약한 모델" 티어를 **정책 기본값 형태**로 채택하되 **모델 고유명은 adapter 정책 실값에만** 둔다) × cost/latency/quality 가중 × fallback 체인(호출 실패 시 차상위).
- **직렬화 시점 1회 고정(hysteresis)** — 모델 선택은 Step 직렬화(revision append) 시점에 결정·슬롯 기록. 재선택 트리거는 (a) retry 한도 도달 후 에스컬레이션 해소 시 (b) 명시적 정책 이벤트뿐(과도한 스위칭이 일관성·비용·context continuity를 해치는 것을 정책으로 억제).
- **CP2 Verifier 모델 = 독립 정책 행** — OQ-SH-4 해소. `_dispatch_cp2`의 `model=step.model` 상속 1개소를 정책 참조로 수정(테스트 갱신 동반).
- **책임 경계**: Model Router = 정책 평가(무엇을 쓸지 — deterministic·중립) / Provider Adapter(invoker) = 슬롯 값의 물리 전달(어떻게 호출할지 — 기존 `--model <slot>` 경로 재사용). 선택 결과는 artifact provenance에 기록되되 소비 조건으로 쓰지 않는다(SP-INV 3 동형).

### §3.6 Artifact Record·Registry — 파생 인덱스 (제2 진리원천 아님)

```
ArtifactRecord {
  artifactId      // 논리 식별자
  version         // append-only 인스턴스 버전
  supersedes      // 직전 버전 참조 — 기존 문면 불변 (PC-INV 9 동형)
  derivedFrom[]   // 입력 artifact 참조 (07 interfaceContract consumes의 실측치)
  producedBy      // provenance {runId, stepId, attempt, role, capability, model} — 불투명 부속(SP-INV 3 동형)
  approvalState   // draft → verified(CP2 Pass) → approved(CP3) → user_approved(사용자 게이트)
                  //   — mutable 필드가 아니라 게이트 이벤트의 파생 뷰
  location        // 워크스페이스 물리 경로 (Adapter 소관 — SP-INV 7 귀속)
  contentHash     // 선택 — 문면 불변 증빙
}
```

레지스트리 = 완료 보고(02 §3.2-C `artifacts`)와 게이트 이벤트에서 파생되는 **인덱스**다. Fresh Context 번들의 "확정 참조"(SH §3.2·07 R2)는 이 레지스트리에서 `approvalState`가 정책이 요구하는 등급 이상인 버전만 해석한다. Artifact는 파일 경로만이 아니라 Markdown/JSON/code/image/test evidence/decision record 등 임의 형태를 수용한다(형태는 location+contentHash 뒤의 불투명 내용).

### §3.7 독립 실행 Agent 모델 — Design Agent는 특별 취급 0 (일반 모델의 대표 사례)

충분 입력(Contract 인스턴스 + 확정 artifact + delegation 8필드) → Sufficiency 판정(step-hosting-protocol §6.1 재사용) → headless 실행 → 산출 Artifact → 게이트 정책(`review_required`/`user_decision_required`)에 따른 리뷰·사용자 게이트 → 피드백 = 게이트 해소 이벤트 → rework revision으로 재실행. 사용자와의 직접 대화 채널은 없다 — 대화형 단위(Discovery Eliciting류)는 규칙의 예외가 아니라 "사용자 채널에 위임되는 capability"로 정책 데이터에 선언된다.

04 §3.4 협업 프로토콜의 호스팅: Assessing/Proposing/Reconciling/Reviewing = headless step · Validating(T8/T9/T10) = `user_decision_required` 게이트 물리화 — **04 §3.9 확장 포인트 1·2의 정확한 실현(04 무수정)**. 설계 충돌 조정 = 04 §3.4 Reconciling(Conflict Detection + Trade-off Resolution)·Reviewing 그대로. 실행 병렬 결과 충돌 = 07 Merge 5단계·중재자 = Advisor 역할(07 INV-6). 신설 0.

### §3.8 불변 초안 PO-INV 8건 (전부 기존 정본의 파생 — 프로토콜이 확정 소유)

| # | 이름 | 내용 (모태) |
|---|---|---|
| PO-INV 1 | 판단 금지 상속 | 중립 orchestrator는 의미 판단 0 (SH-INV-1 동형) |
| PO-INV 2 | 이중 원장 append-only | revision ledger·step 이벤트 로그 모두 append-only, 현재 그래프·상태는 파생 뷰 (SH-INV-2 확장) |
| PO-INV 3 | 결정적 재개 | 동일 (revision ledger, event log) 쌍 → 동일 그래프 → 동일 ready_set (SH-INV-3 확장) |
| PO-INV 4 | 게이트 단조성 | §3.3 — 코드 소유 하한 약화 불가·강화만. Autonomy 축과 직교 (SH-INV-4 확장) |
| PO-INV 5 | revision 근거 필수 | 모든 revision은 proposingStepRef + gateEventRef를 갖는다. 근거 없는 그래프 변경 0 |
| PO-INV 6 | 역할 추상 유지 | 할당기는 Capability 선언까지만 소비, AgentSpec 해석·물리 매핑은 Adapter (SP-INV 6 동형) |
| PO-INV 7 | artifact 계보 | append-only + supersedes, provenance 불투명 (PC-INV 9·SP-INV 3 동형) |
| PO-INV 8 | 중립성·격리 | 중립 코드에 provider/모델/업스트림 Layer 고유명 토큰 0 (C-3 확장), 상위 반환은 요약만 (SH-INV-8 동형) |

## §4. 배치 (v1.5 D-2 책임 3분리 동형)

| # | 산출물 | 배치 | 성격 |
|---|---|---|---|
| ⓪ | **orchestration Layer 골격** — 개관 ARCHITECTURE.md(스켈레톤 A 동형·§ 위임) + ROADMAP.md 스텁 | `orchestration/` 신설 (최상위 Layer 6번째 — 루트 §2.3 Agentic Runtime slot 실현) | Layer 개관 — 하위 spec 복제 0 (T-a 관례) |
| ① | **Project Orchestration Spec** — Work Graph 소비 계약(07 무수정 인용)·Revision Ledger 계약·Gate Policy 5종+단조성·Role→AgentSpec→Instance→Model 할당 계약·Artifact Record 계약·PO-INV 8건 | `orchestration/specs/05-project-orchestration.md` 신설 (UAF spec 번호 계보 01~04 승계) | provider·언어 중립 계약 문서 (01~04 자매 + step-hosting-protocol 관례 참조 — C-3 동형·§ 포인터만) |
| ② | **중립 Orchestrator 모듈** — revision.py(원장·파생)·orchestrator.py(StepHost **라이브러리 무수정 import** 래퍼)·gates.py(정책 평가)·allocation.py(capability 매칭·모델 정책)·artifacts.py(파생 인덱스) + JSON 스키마 + 테스트 | `orchestration/framework/orchestrator/` 신설 (C-2 동형 규칙 — `uahf/framework/loop/step-host/` 무수정 import) | 중립 실행 코드 — 금지 토큰 0 (전수 스캔 AC) |
| ③ | **Claude 바인딩** — 직렬화(JSONL/JSON)·capability→물리 호출 매핑·게이트 큐 제시 채널·run 데이터 백엔드 경로 | `uahf/framework/adapters/claude/project-orchestration-binding.md` 신설 — **UAF 레벨 바인딩 5종째를 Adapter 물리 경계에 동거**(contract/entry/discovery/solution-design-binding 선례·DP-X4 비합산. uahf/ 트리 접촉 2건 중 하나 — §2 표) | 격리 지점 (step-hosting-binding 동형) |
| ④ | **정책·스키마 데이터** — gate/allocation/model-selection policy·artifact-record 스키마 + run 데이터(E2E 시 생성) | ② 내 스키마 + `uahf/framework/adapters/claude/orchestration-data/`(dogfooding — discovery-data·solution-design-data 선례 동형) | Policy as Data |
| ⑤ | (선택·비정본) 작업 단위 유형·조율 역할 예시 카탈로그 | `planning/docs/appendix/` | SP-INV 5 준수 — 코어 밖 |

**UAHF 접촉 방식 (사용자 결정)**: **라이브러리 재사용** — orchestrator.py가 `uahf/framework/loop/step-host/` 중립 모듈을 코드 수준에서 무수정 import. 루트 §2.5 "상위만이 하위를 안다"의 허용 방향이며, UAF-INV ①의 핵심은 '무수정'이므로 읽기 재사용은 위반이 아님을 spec ①에 명시한다. 추후 블랙박스 호출 경계 도입 시에도 계약 변경 0.

## §5. 구현 단계 (S1~S5 — 각 단계 독립 CP2·Baseline 승격은 S5 후 사용자 게이트)

| 단계 | 산출 | E2E 실증 시나리오 |
|---|---|---|
| **S1** Layer 골격 + spec 정본 | ⓪ orchestration/ 골격 + ① spec 저술 → CP2 → CP3 | 전이·불변 전수성 검증, Frozen 무촉 git 실측, 금지 토큰 스캔 0건 (v1.5 W1 동형) |
| **S2** Revision Ledger + Orchestrator | revision.py·orchestrator.py + 테스트 | (a) 2-task 그래프 실행 중 산출이 task 3 제안 → 게이트 승인 → revision append → 이어 실행 (b) 강제 종료 후 재기동 — 동일 2원장 → 동일 재개 지점 (c) 순환 유발 revision → 사유 코드 차단 |
| **S3** Gate Policy 5종 + 게이트 큐 | gates.py + 정책 스키마 + 바인딩 §(게이트 제시 채널) | (d) 같은 그래프에 gateKind별 상이 거동 — auto_continue 무정지 / user_decision_required 정지·사용자 해소 이벤트로만 재개 (e) Autonomy `unrestricted`에서도 5종 게이트 전부 정지(단조성 실증) |
| **S4** Allocation + Model Selection + AgentSpec 레지스트리 | allocation.py + 정책 스키마 + OQ-SH-4 해소(1개소 수정) | (f) capability class가 다른 두 단위에 상이 모델 슬롯이 직렬화 시점 기록·전달 실측 (g) retry 한도 도달 시에만 fallback 재선택(스위칭 억제) (h) CP2 Verifier 모델 독립 지정 |
| **S5** Artifact Registry + 통합 dogfooding | artifacts.py + ③ 바인딩 완성 + run 데이터 | (i) artifact v1 → rework v2 supersedes 계보·derivedFrom 기록·소비 번들이 approved 버전만 참조 (j) **축소판 종단 흐름**: Contract 인스턴스(기존 계보 재사용) → maturation unit(headless·T8 사용자 게이트) → decompose unit → 구현 step → review 게이트 → 완료. 이벤트 로그에 상류 재실행 흔적 0 |

## §6. 무수정 경계 (본 트랙이 지키는 것)

- **uahf/specs 00~13 Frozen · 04-solution-design · 루트 ARCHITECTURE.md · step-hosting-protocol 본문 · framework/loop/step-host/ (OQ-SH-4 1개소 제외) · 기존 바인딩 본문** — 전부 무수정. § 포인터 인용만.
- **uahf/ 트리 접촉은 정확히 2건**: (i) `project-orchestration-binding.md`+`orchestration-data/` 신설(Adapter 물리 경계 동거 — UAF 레벨 바인딩 선례 4건 동형·DP-X4) (ii) `framework/loop/step-host/host.py` `_dispatch_cp2` 1개소 — CP2 Verifier 모델 독립 지정(OQ-SH-4 해소·테스트 갱신 동반). 그 외 정본·중립 코드는 전부 `orchestration/` 신규 Layer 소유.
- 루트 ARCHITECTURE.md 라우터 포인터 1행 추가·step-hosting-protocol §9 이력 append·Contract v3 성숙 재발행은 **트랙 종단 별도 결정**(사용자 게이트·선전제 금지).
- Append-only 데이터(memory-data/·loop-data/·discovery-data/·solution-design-data/·step-data/runs/) 무촉.

## §7. Reject (하지 않는 것 — 사용자 금지 + 비교 판정)

1. **God PM Agent** — 모든 것을 읽고 지시하는 중앙 LLM 상주 조율자 (대안 A 기각).
2. **새 Workflow/Planning/Interview Engine** — 07·03·02-discovery 재사용 강제.
3. **Agent-모델 고정 결합** — 모델은 정책 데이터가 Step 슬롯에 채우는 값일 뿐.
4. **고정 Agent 목록·고정 파이프라인** — 작업 단위 유형·역할 전부 개방 네임스페이스·데이터.
5. **Chat history 공유 기본 협업** — Fresh Context 번들 + Artifact handoff만.
6. **방법론 코어 유입** — TDD 등 Superpowers 규율 팩은 UAF-INV ⑥에 따라 코어 밖(비정본 부록/Strategy Provider 소재로 이월).
7. **모델 규율 의존 게이트 강제** — 게이트는 deterministic 코드가 강제(SH-INV-4 계열).

## §8. Superpowers 반영 경계 (Matrix 16항 중 즉시 반영 3건만)

- **즉시 Adapt**: ① "가장 약한 모델" 티어 → Model Selection Policy 기본값 형태(§3.5) ② Coordinator 최소 집합 → 책임 3분해 근거(§1) ③ placeholder 금지·정확한 완료 조건 → Step 직렬화 품질 규율(비정본 부록 후보).
- 기존재 확인 6건(컨텍스트 큐레이션·ledger·검증 규율·brainstorm 게이트·핸드오프 artifact·병렬 규율)은 채택 불요 — UAF가 이미 동형 이상을 보유.
- 나머지는 Reject(§7) 또는 Defer(worktree·git automation·방법론 팩). 이름·파일 구조·명령 복제 0.

## §9. Open Questions (본 설계로 미해소 — 이월)

1. 물리 동시 디스패치(OQ-WB-2 잔여) — 순차 상속, 병렬 invoker는 후속.
2. 멀티프로젝트 오케스트레이션 — 최상위 단위는 단일 프로젝트(1 ledger).
3. Escalation 해소 어휘(OQ-SH-5) — S3에서 최소 형태만, 계약 승격 별도.
4. 대화형 단위의 형태 B 호스팅 — 다중 턴 Eliciting은 형태 A 위임으로 우회.
5. 비용/토큰 실측 미터링·실행 예산 — 미설계.
6. 루트 라우터 등재(신규 Layer `orchestration/` 1행 — 문서버전 상승·사용자 게이트)·step-hosting-protocol §9 append — 트랙 종단 별도 결정. (배치·프레이밍 자체는 2026-07-13 사용자 결정으로 해소됨.)
7. Contract v3 재발행 연계 — 트랙 완료 후 별도 성숙 run.
8. AgentSpec tie-break 규칙 기본값 — S4에서 데이터로 두되 기본값 결정 필요.
