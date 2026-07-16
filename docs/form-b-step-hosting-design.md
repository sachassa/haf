# 형태 B Step Execution Hosting — 설계 정본 (초안)

작성: Advisor · 2026-07-13
상태: W0 확정 (사용자 승인 2026-07-13 — 설계 방향·D-1·D-3 승인 · D-2 재검증 반영[§4]·W3 E2E 필수 7 시나리오 편입[§8]) · D-2 최종 확정 + §6 ③ stale 배치 표기 정정(§4 표 기준 — 사용자 게이트·정정 승인 2026-07-13)
입력: 사용자 지시 16항(2026-07-13) · [후속-A] 비교 분석 보고서(Option D·Adopt/Adapt 6·Reject 3·Scope Matrix) · 저장소 Ground Truth 실측(Explore 3기 + Advisor 교차 — §2 충돌 검증)
성격: 마일스톤 설계 정본 후보. 계약 정본은 이 문서가 아니라 각 spec·프로토콜 문서·바인딩이 소유한다(재정의 0 — 충돌 시 정본 우선·Advisor 보고). 버전 번호는 미확정(사용자 원칙 9 — 버전 선전제 금지).

---

## §0. 목적 — 두 공백을 기존 구조 위에서 메운다

새 Interview·Planning·Runtime 체계를 만들지 않는다. 기존 UAHF의 Runtime/Workflow/Loop/Planner/Decompose/Adapter/Memory/Verification 구조를 보존하면서, 다음 두 실측 공백([후속-A] Scope Matrix 판정)만 최소 구조 변경으로 메운다:

1. **Runtime Step/Task Scheduling / Execution Hosting** (Planning scope 5 — "미구현·설계 0") → **Step Host** (§3).
2. **Execution Readiness Clarification** (Interview scope 3 — "공백·부분 대체만") → 기존 앵커의 명명·정식화 (§3.7).

우선순위(사용자 고정): 최소 변경 · 기존 구조 재사용 · AI-agnostic · deterministic resume · context isolation.

목표 실행 흐름(사용자 §5):
```
Existing Plan → Decompose → Work Graph/Task → Executable Step → Fresh Context Assembly
→ Adapter-mediated Execution → Result Capture → Verification → Retry/Block/Resume/Next Step
```

## §1. Ground Truth 설계 제약 (지시 1~4 — 정본 앵커 확정)

| # | 제약 (사용자 확정) | 정본 앵커 (실측) |
|---|---|---|
| 1 | Planning은 신규 Capability 아님 — 기존 재사용 | 03-loop §3.1-A Plan(Planner 초안+Advisor 채택)·02 §3.2-A Planner·07 §3.1-A Decompose·§3.2-A/B Work Graph·Task. 전부 Frozen v0.1 실재 — **새 Planning Engine 0** |
| 2 | 4계 역할 분리 | Project/Product Discovery=discovery Eliciting(02-discovery) / Solution Planning=04 SD / **UAHF Implementation Planning=03 Plan+07 Decompose** / **Execution Readiness Clarification=본 설계 §3.7**(신규 명명·기존 앵커) |
| 3 | Full UAF Mode = 상위 산출물 재사용·재 Interview/Plan 생성 금지 | SP-INV 1·04 §3.6(재Discovery·번복 차단)·EN-INV 1/2·02 §3.3-A incremental 기준선·중복 방지 규칙 9건([후속-A] K) |
| 4 | Standalone UAHF Mode 지속 지원 | 루트 §3 "uahf 단독 실행 내장(UAF-INV ①)"·03 §3.5-A 선택 입력·13-harness 최소 5요소(Contract 불포함). 부족 시 최소 Clarification·필요 시 **명시적 Discovery 호출 fallback**(Layer 단독 실행 — 중복 Interview 아님) |

## §2. 충돌 검증 결과 (기존 spec·불변·conformance·예약 지점 대조 — 저장소 실측)

**판정: 차단 충돌 0. 본 설계가 쓰는 자리는 전부 기존 정본이 명시 예약한 지점이다.**

| 대조 대상 | 원문 근거 | 판정 |
|---|---|---|
| 실행 코드 배치 | structure.md §4 C-2: "실행 코드(향후 형태 B)는 framework/runtime/·Module 구현 디렉터리·framework/adapters/ 이하에만" · **규칙 4: "AI·실행 환경·언어·툴체인 의존 부분은 adapters/<adapter>/ 뒤로 격리 … 정확한 분할은 형태 B가 실제로 설계될 때 확정"** | 본 설계 = 그 "실제 설계" 시점. Python(언어 의존) 실행 코드는 규칙 4에 따라 **adapter 경계 격리가 정본 명령** — 충돌 0 (§4) |
| C-1 | "형태 A→B 전환 시 Core Contract(01 §3) 변경 0" | 본 설계는 01/02/03/06/07 §3 계약을 **구현**만 한다 — 개정 0건 (§6) |
| C-3 | framework/core·runtime은 언어/툴체인 비의존 | 실행 코드를 core·runtime에 두지 않음. runtime에는 **언어 비의존 프로토콜 문서**만 신설 (§4·§6) |
| 01-runtime INV-6·§3.1-C | "Serve 구간 오케스트레이션 주체 = Loop Engine·Runtime은 호스팅 계약만" | Step Host = Loop Engine 구동의 형태 B 실현 — Runtime 계약 재정의 0·**두 번째 Runtime 아님** |
| 형태 B 예약 로케이터 | loop-binding §4 "사이클 구동을 사람 없이 자동 트리거·반복하는 실행 코드"·workflow-binding "무인 병렬 오케스트레이션 실행 진입점(형태 B 예정)" | Step Host가 정확히 이 두 예약 자리의 실현 |
| OQ 5건 (형태 B 경계 분할) | OQ-M5-2·VB-2·LB-2·WB-2·PB-2 | §4에서 실행 호스팅 축만 부분 해소(LB-2·WB-2 해당분)·나머지 축은 명시 유지 — OQ 문면 계약 변경 0 |
| Glossary INV-3 | "Layer 6·Cross-cutting 1·Core Component 13" | **새 Component·새 Layer·새 spec 창설 0** — Step Host는 기존 Loop/Workflow 연산의 형태 B 실현 (§3.1) |
| 04 §3.9 | "step 기반 실행기와의 연결 — 명칭만·설계 금지" | 04 무수정. 연결은 프로토콜 문서·바인딩이 소유(04 §3.9는 명칭 포인터 그대로) |
| Memory INV-1~4 | 단일 Port·purpose/scope·index-first·소비자에 Runtime 없음 | **Host는 Memory에 직접 접근하지 않는다**(PortBypass 방지) — §3.3 |
| UAF-INV ⑤·P-D4/P-D5 | "확정 게이트=사용자 승인"·"일상 자동화 vs 확정 게이트 보존은 상충하지 않음"(02-discovery §3.2 주) | Autonomy Policy가 정확히 이 구분 위에 놓임 — §3.8. 저장소 "dangerously" 현 0건 → Core·정본 0건 유지 |
| adapter-conformance | UAF 레벨 바인딩 비합산(DP-X4)·BP-1~17 무영향 | 신규 바인딩·실행 코드는 conformance 판정 무영향(notes 병기 후보만) |

## §3. 아키텍처

### §3.1 위상 — Step Host = 기존 예약 자리의 얇은 형태 B 실현 (새 Runtime 아님)

**Step Host**는 "판단하지 않는 기계 구동자"다: 03-loop 사이클 구동과 07-workflow 디스패치·순서 규칙을 **무인으로 트리거·반복**하는 실행 코드(형태 B). 의미 판단(완료/실패/차단·검증 판정·승인)은 전부 기존 주체(Agent 세션·Verifier·Advisor·사람)에 남는다. Runtime(01)의 호스팅 계약·Loop(03)의 전이 규칙·Workflow(07)의 R1~R4·병합 5단계를 **재정의하지 않고 구동만** 한다. 기존 형태 A(주 세션 규약 실수행)와 병렬 체계가 아니라 **같은 계약의 두 번째 실현 형태**이며, 형태 A는 그대로 유효하다(C-1).

### §3.2 Step 계약 — 새 계약 요소 0 (Task의 실행 시점 직렬화)

**Executable Step = 07 §3.2-B Task + 그 `delegation`(02 §3.2-B 위임 8필드)의 자기완결 직렬화**다. 필요한 전 필드가 기존 계약에 실재한다:

| Step 파일 내용 | 소유 정본 (재사용) |
|---|---|
| id·task·done(검증 가능 완료 조건)·interfaceContract·ownedBoundary·dependsOn | 07 §3.2-B Task 필드 그대로 |
| from·to·task·input·output·done·context·constraints | 02 §3.2-B 위임 8필드 그대로 ("하나라도 누락 시 착수 불가"가 Step 유효성 검사) |
| role/capability/model 슬롯 (§3.9) | 02 §4.1 실행 모델 바인딩·04 §3.3 Capability 선언 |
| feedback (재시도 시에만) | 02 §3.2-D 실패 보고·06 §3.2-D 재작업 지시에서 파생 (§3.5) |

직렬화 형식·파일 배치는 Adapter 소관(바인딩). 원본의 "step 설계 원칙"(자기완결·실행 가능 AC 등)은 **Step 저술 관행**(비정본 부록 후보)으로 흡수 — 계약 창설 없음.

### §3.3 Fresh Context Assembly — 세션 전체 상속 없음

각 Step은 신규 세션에서 다음 번들만으로 실행된다: **Step Contract(§3.2) + 확정 Artifact 참조(input·interfaceContract — R2: 미완성 산출물 불추측) + Memory 재료 + Constraints + (재시도 시) feedback.**

**Memory 재료 규칙 (병렬 Memory 금지·INV-1 준수):** Host는 Memory Store·Index에 **직접 접근하지 않는다**(04 §3.4 소비자 목록에 Runtime 없음 — PortBypass 방지). 두 경로만 허용: (a) **위임자(Advisor/Loop Consult 단계)가 Recall(purpose·scope·index-first)로 회수한 결과 요약을 Step의 `context`에 포함**(권장 기본 — 03 Consult 단계의 기존 책임 그대로) (b) Step 세션이 스스로 Consult 규약을 수행(Recall 계약 준수). 새 Memory 체계·캐시 신설 0.

### §3.4 상태 모델·결정적 재개 — 기존 어휘 재사용·append-only 파생 뷰

사용자 검토 상태(pending/running/blocked/failed/completed)는 **03-loop §3.2-B 기존 단계 상태 5종에 전건 흡수**된다 — 새 상태 열거 신설 0:

| 검토 상태 | 03-loop 상태 (정본) | 의미 |
|---|---|---|
| pending | `Pending` | 디스패치 대기(의존 미충족 포함) |
| running | `Active` | Step 세션 실행 중 |
| completed | `Passed` | CP2 Pass 확정 후 |
| failed | `Failed` | 실패(재시도 잔여 시 재디스패치 대상) |
| blocked | `Escalated` | 사람/상위 개입 대기 (03 §3.1-D 5조건·blocked 선언) |

**기록 = append-only Step 이벤트 로그** — 03 §3.2-A 전이 이벤트 스키마(cycle_id·seq·from/to·trigger·outcome·retry_count·actor·ref·at) **동형 재사용**. "현재 상태"는 별도 mutable 필드가 아니라 **로그의 파생 뷰**다(마지막 관련 이벤트가 상태를 결정 — v1.4 maturation-r001·loop-data 선례 동형). 원본의 mutable `index.json` 갱신 모델은 **판독 계약만 흡수**하고 기록은 append-only 유지([후속-A] G-2).

**Deterministic resume (first-pending 일반화):** 크래시·중단 후 재실행 시 Host는 로그를 재생해 각 Task의 파생 상태를 복원하고, **"Passed가 아닌 Task 중 dependsOn이 전부 Passed인 최소 순번 집합"**을 다음 디스패치 대상으로 결정한다(07 §3.2-A parallelSets 도출 규칙과 동일 논리 — 순차 실행은 그 특수형). 같은 로그에서 항상 같은 재개 지점이 나온다. `Escalated` 잔존 시 즉시 정지(해소 전 진행 금지 — 원본 blocker 검사 동형).

### §3.5 실행 시퀀스 (4 시나리오)

**정상:** Host가 first-pending Task 선택 → Step 직렬화(위임자 사전 준비 or 조립기) → 신규 세션 기동(Adapter-mediated·§3.8 policy 적용) → Step 세션이 Execute+CP1(Executable AC 실행 포함) → 완료 보고(5필드)를 산출·기록 → Host가 **CP2를 별도 독립 세션(Verifier 역할)으로 디스패치** → CP2 Pass → `Passed` 이벤트 append → 다음 Step. (CP2 판정 계약 06 그대로 — 자가판정 완료 확정 금지 = Reject 3.)

**실패/재시도:** CP1 실패 또는 CP2 Fail → `Failed` 이벤트(+실패 보고/재작업 지시 ref) → retry_count < 한도(01 Config — Policy 데이터)이면 재디스패치. **다음 fresh context의 feedback 슬롯에 직전 실패 보고(reason·repro)와 CP2 재작업 지시를 주입**(02 §3.2-D·06 §3.2-D 파생 — append-only 로그에서 도출·별도 상태 시스템 0). 한도 초과 → `Escalated`(03 §3.1-D 조건 1).

**Blocked:** Step 세션이 O4(추측 금지)에 따라 차단 선언(실패 보고 `blocking=차단됨`) 또는 §3.7 Clarification 필요 판정 → Host는 `Escalated` 기록 + **물리 정지 신호**(원본 exit 2 동형 — 값은 Adapter) → 사람/Advisor 해소 → 해소 이벤트 append 후 재실행(§3.4 재개 규칙이 해당 Task를 재선택).

**크래시 재개:** Host 재기동 → 로그 재생 → §3.4 결정 규칙 → 이어서 실행. `Active`로 남은 채 종료된 Task는 결과 미확정이므로 `Failed(계기: 실행 중단)` append 후 재시도 규칙 적용(멱등 — 이벤트 중복 없이 재구성 가능).

### §3.6 검증 통합 — CP1/CP2/CP3 보존 + AC 3형

- **AC 3형** (06 Core 무수정 — done 필드 표기 관행 + VT 매핑): **Executable AC**(기계 실행 커맨드 — Step 세션이 CP1에서 실행하고 CP2가 재실행/재확인, VT-2·VT-5의 물리화) / **LLM Review AC**(Verifier 독립 세션 판정 — VT-1~5 그대로) / **Human Review AC**(`Escalated` 게이트로 물리화 — 03 §3.1-D 조건 5). 모든 AC를 executable로 강제하지 않는다 — done 필드에 유형 표기 관행만.
- **CP3(Advisor 승인)**: 사람 승인이 아니라 **Advisor 역할의 승인**(02 §3.1)이므로 무인 실행과 양립한다 — Host가 사이클 Complete 전에 Advisor 역할 세션에 CP3를 디스패치(또는 배치 종단에서 일괄). 06 거짓 완료 검출·final_verdict 도출 규칙(Pass/Fail/Conditional) 그대로.

### §3.7 Execution Readiness Clarification (공백 1 해소 — 신규 Engine 아님)

기존 앵커(02 위임 8필드 착수 거부 · 02 O4 추측 금지 · 03 §3.1-D 사람 개입 5조건 · P-D4/P-D5 구분)의 **명명·정식화 + Step Host의 blocked 신호와의 접속**이다:

- **진입 Sufficiency 판정(Standalone 필수·Full 재확인):** 위임/Step 필드 완전성 검사(02 §3.2-B — 기존 계약이 곧 판정 기준). 완전 → 즉시 Implementation Planning(03 Plan). 불완전 → **최소 범위 scoped 질의**(부족 필드를 지목해 위임자/사용자에게 — 02 반환·질의 관행의 정식화). Discovery 전체 재실행 금지.
- **Upstream artifact 급 부족**(무엇을 만들지 자체가 불명): **명시적 Discovery Capability 호출 fallback**(Layer 단독 실행 + Contract 산출 후 재진입) — 중복 Interview가 아니라 부족한 upstream artifact의 명시적 획득. 호출 여부는 게이트(사용자/위임자 확인) 통과.
- **실행 중:** Step 세션의 차단 선언(§3.5 Blocked)이 이 Clarification의 실행 중 형태다 — scoped question을 기록에 남기고 정지, 해소 후 재개.

### §3.8 Permission/Autonomy Policy (Core = provider-agnostic·Adapter = 매핑)

- **Core 어휘(Policy as Data — 루트 §6 원칙 8):** `interactive`(모든 도구 실행 승인 프롬프트 유지) / `auto_approve`(선언된 허용 범위 내 도구 실행 자동 승인) / `unrestricted`(도구 실행 승인 프롬프트 전면 생략). 정책 값은 데이터(step-hosting policy 파일)이며 엔진·계약 무변경으로 조정된다.
- **게이트 등급 분리(불가침):** 위 policy는 **도구 실행 승인 프롬프트 축만** 제어한다. **Human Decision Gate — Contract 변경·중대 Architecture Decision·파괴적 작업·해결 불가 불확실성(= 03 §3.1-D 조건 2~5 + UAF 레벨 게이트[UAF-INV ⑤·T8/T16 계열]) — 는 어떤 policy 값에서도 `Escalated` 정지로 보존**된다. 정본 근거: P-D4(개입 최소)와 P-D5(권한 보존)는 상충하지 않는다(02-discovery §3.2 주 — 기존 문면 그대로).
- **Adapter 매핑:** provider별 실제 실행 옵션 변환은 바인딩 소관. Claude adapter는 `auto_approve`/`unrestricted` 선택 시 해당 CLI의 권한 생략 실행 방식으로 매핑한다 — **구체 플래그 문자열은 바인딩 문서에만 등장(Core·본 설계 정본 하드코딩 0** — 저장소 현행 "dangerously" 0건 유지).

### §3.9 Expert Role seam (고정 Persona 0)

Step 직렬화에 **role 선언 슬롯**(roleId·capability·model)만 둔다 — 값의 원천은 기존 구조 그대로: 하네스 4역할(02 §4.1 front-matter `model` 실측 관례) 또는 동적 Expert Role(04 §3.3 Capability 4필드 선언·최소 할당). Step Host는 선언을 **전달만** 하고 해석하지 않는다. 새 고정 Persona 세트·역할 카탈로그 창설 0(SP-INV 5 동형).

### §3.10 Main Context 최소화

Step 실행 상세·중간 로그·대량 Artifact는 run 디렉터리(백엔드)에 남고, 상위(주 세션/호출자)로는 **완료 보고 5필드 수준의 요약·상태·검증 결과만** 반환한다(02 §3.2-C 재사용). Host 자체는 어떤 내용도 주 세션 컨텍스트에 누적하지 않는다(프로세스 분리).

## §4. 경계 분할 확정 (structure.md §4 규칙 4의 "실제 설계 시 확정" — 이번 트랙의 답)

**이번 확정(step 실행 호스팅 축에 한정 — D-2 사용자 재검증 지시[2026-07-13] 반영: 책임 3분리):**

| # | 책임 | 배치 | 근거 |
|---|---|---|---|
| 1 | **Step Hosting Protocol**(provider-agnostic 계약 — Step 직렬화 축·상태 파생 규칙·판독 계약·Host 의무·Autonomy 어휘·Clarification 계약) | `uahf/framework/runtime/step-hosting-protocol.md` **신설** | D-1 승인. C-3 준수(언어 비의존 문서)·§2 "runtime = 프로토콜 문서 경계"·01 §3 계약의 인스턴스(C-1) |
| 2 | **Generic Step Host**(provider-중립 실행 호스팅 — Python은 구현 수단·Claude 비종속) | `uahf/framework/loop/step-host/` **신설**(host 코드+configSchema — 규칙 2 구성) | **loop-binding §4 형태 B 로케이터가 명시 예약한 1순위 자리**("framework/loop/ Module 구현 디렉터리 또는 adapters/")·structure.md §4 규칙 2(형태 B 시 Module 자기 경계에 구현)·C-2 열거 포함·**C-3 언어 중립 제약은 core/runtime에만 적용**(Module 디렉터리 비대상)·07 §9 "Lifecycle 구동은 Loop Engine 소관". **AI·provider 토큰 0**(코드·주석 포함 — CP2 전수 스캔 대상)·provider 호출은 invoker 인터페이스로 추상. 서술 문서는 프로토콜(중립)과 바인딩(구체)이 분담 — Module 경계 문서 본문 언어 중립 관행 유지 |
| 3 | **Claude-specific Invocation / Permission Mapping** | `uahf/framework/adapters/claude/step-hosting-binding.md` **신설**(직렬화·run 백엔드·정지 신호 값·autonomy→CLI 옵션 매핑[`unrestricted` → `--dangerously-skip-permissions` — **이 문자열은 이 바인딩에만 등장**]·모델 지정 전달) + `uahf/framework/adapters/claude/step-invoker/` **신설**(CLI 호출 얇은 모듈 = invoker 인터페이스의 claude 구현) | 규칙 4(AI·실행 환경 의존은 adapter 격리)·자매 바인딩 관례(conformance 비합산 notes 병기) |
| — | run 데이터(step 파일·이벤트 로그·정책) | 이원화(DP-X2 동형): 일반 관례 = 소비 프로젝트 내 관례 경로 / dogfooding = `adapters/claude/step-data/` | SP-INV 7 동형(워크스페이스 귀속)·자매 *-data 격리 |

**경계선 확정 문면(규칙 4의 이연 질문에 대한 이번 답):** AI·실행 환경 의존 → adapter 경계 / 언어만 의존하는 중립 엔진 → Module 구현 디렉터리(규칙 2 예정 자리) / 계약 서술 → runtime 프로토콜 문서(언어 중립).

**`adapters/generic/step-host/` 대안 기각 근거(사용자 지시 검증 결과):** `adapters/generic/`은 물리 실재하나 정체성이 "제2 실행 환경의 최소 구현 Adapter"(11 §4-2nd·conformance 판정 대상)다. 공용 엔진을 그 안에 두면 11 INV-6(자기완결 — "모든 바인딩을 adapters/<이름>/ 경계 안에") 하에서 claude adapter가 타 adapter 경계 코드에 실행 의존하는 선례 없는 결합이 생기고 generic conformance 의미가 오염된다. 기존 확장 지점(loop-binding §4 로케이터)이 우선한다.

**OQ 5건 처리:** OQ-LB-2의 "사이클 구동 실행 코드 분할" 축은 위 확정으로 **해소**(중립 엔진 = framework/loop/step-host/·provider 의존 = adapters/claude/step-invoker/). OQ-WB-2는 "무인 병렬 오케스트레이션 구동 = step-host가 Work Graph(07 §3.2-A)를 데이터로 소비"로 **부분 해소**. Module별 연산 코드(Verify 연산·Record/Recall·Install — OQ-VB-2·M5-2·PB-2)의 분할은 **계속 이연**(이번 스코프 밖 — OQ 문면 무수정, 바인딩 §9·OQ에 해소 사실만 append).

## §5. Full UAF Mode vs Standalone UAHF Mode (진입 차이)

| 단계 | Full UAF Mode | Standalone UAHF Mode |
|---|---|---|
| 입력 | Contract v(최고 instanceVersion)·SD 성숙 산출(있으면) — **재사용, 재생성 금지** | 사용자 제공 입력(Contract·요구사항·기존 프로젝트·위임) |
| 진입 판정 | Consult 정독(03 §3.5-B (a) 관행) 후 즉시 Implementation Planning | **Sufficiency 판정(§3.7)**: 충분 → 즉시 Implementation Planning / 불충분 → 최소 Clarification / upstream 부족 → 명시적 Discovery fallback(게이트 후) |
| Planning | 03 Plan(Planner 초안→Advisor 채택) → 07 Decompose(Work Graph/Task) — **기존 그대로** | 동일(자기완결 — 13-harness 최소 5요소) |
| 실행 | Step 직렬화 → Step Host 구동(§3.5) | 동일 |
| 금지 | Project/Product Discovery Interview 재수행·상위 Plan 재생성(제약 3) | 무조건적 전체 Discovery 재실행(제약 4) |

## §6. 변경 파일 범위 (구현 마일스톤 — 승인 후)

**신설 (4±1):** ① `uahf/framework/runtime/step-hosting-protocol.md`(계약 — AI/언어 비의존) ② `uahf/framework/adapters/claude/step-hosting-binding.md`(물리) ③ `uahf/framework/loop/step-host/`(중립 Host — Python 실행 코드 + configSchema + 자체 테스트) + `uahf/framework/adapters/claude/step-invoker/`(invoker 인터페이스의 claude 구현) ④ run 데이터 백엔드(E2E 시 생성 — L-07 정직 구분) ⑤ (선택·비정본) Step 저술 관행 부록.

**기존 정본 개정: 0건 목표** — 01/02/03/06/07 Frozen spec·루트 ARCH·04·구조 규격 전부 무수정(§ 포인터 재사용·C-1). 경미 append 후보(비차단·구현 마일스톤 W3급): loop/workflow-binding §9·OQ에 "형태 B 부분 실현" 사실 append(BPD-17 규율) · adapter-conformance notes 병기 · Contract 성숙 재발행(v3 — open 1·3항 부분 해소 반영)은 **구현·E2E 완주 후 별도 성숙 run으로**(선전제 금지).

## §7. 채택/기각/보류 (지시 15·16 + [후속-A] G표 매핑)

**채택(Adopt/Adapt 6):** fresh-context step 단위(G-1·§3.2~3.3) · 상태 판독 계약—기록은 append-only(G-2·§3.4) · 실패 피드백 재주입(G-3·§3.5) · 실행 가능 AC 규율(G-4·§3.6 — 3형 중 1형으로) · first-pending 멱등 재개(G-8·§3.4) · blocked 물리 정지 신호(G-5·§3.5).

**기각(Reject — 지시 16 전건):** 독립 두 번째 Runtime(§3.1 — 기존 계약의 형태 B 실현으로 대체) · 새 Planning Engine(§1 제약 1) · 새 Interview Engine(§3.7 — 기존 앵커 명명) · 고정 Persona 체계(§3.9) · 무조건적 Discovery 재실행(§5 — 명시적 fallback만) · Claude 플래그 Core 하드코딩(§3.8 — 바인딩 격리) · Superpowers 전체 흡수(보류 항으로).

**보류(Defer):** Superpowers Brainstorming/Planning UX Gap Analysis(상위 작업 이후 — 지시 15) · git 자동화·진행 표시기 세부(G-9·10 — 바인딩/구현 세부로 재상정) · Module별 연산 코드의 형태 B 분할(§4 — OQ 잔여 축) · UAHF 진입 Sufficiency의 **계약 승격**(03 §3.5-C 정식 등재 = v2 open 2항과 결부 — 이번엔 프로토콜 문서 수준, spec 등재는 별도 결정) · Contract v3 성숙 재발행(E2E 후).

## §8. 구현 마일스톤 Wave·검증 계획 (D-3 승인 — 단일 마일스톤 W0→W3)

- **W0** 설계 정본 확정(본 문서·본 커밋) → **W1** step-hosting-protocol.md 저술(Worker→CP2→CP3→동결) → **W2** loop/step-host(중립 Python Host)+adapters/claude/{step-hosting-binding.md·step-invoker/} 구현+자체 테스트(**실행 코드 첫 도입 — CP2에 실제 실행 검증 포함**) → **W3** dogfooding E2E(BPD-14/BPD-20 패턴 확장)+정합(바인딩 OQ append·ROADMAP·핸드오프·Memory)+**Baseline 후보 보고(승격 = 사용자 게이트)**.

- **W3 E2E 필수 시나리오 7건 (사용자 확정 2026-07-13 — 전건 실증·물리 증거):**
  1. 정상 Step 실행·완료 (CP1 Executable AC → CP2 독립 → Passed)
  2. Step 실패 → retry feedback(직전 실패 보고·CP2 재작업 지시) → fresh-context 재실행
  3. blocked/escalated → scoped clarification 또는 기존 게이트 연결(사람 해소 → 재개)
  4. 실행 중단(강제 종료) 후 **deterministic resume**(동일 로그 → 동일 재개 지점 재현 실측)
  5. permission policy `unrestricted` → Claude Adapter의 `--dangerously-skip-permissions` 매핑 실증(단 게이트 등급 분리 — `Escalated`는 unrestricted에서도 정지함을 함께 실증)
  6. **Full UAF Mode**: 기존 Contract v2·SD 산출 재사용으로 진입 — upstream Interview/Planning **중복 실행 0** 실측(이벤트 로그에 Discovery/SD 재실행 흔적 0)
  7. **Standalone UAHF Mode**: 충분한 입력 → 즉시 Plan 진입 / 부족한 입력 → 최소 clarification만 수행(전체 Discovery 재실행 0)

- 핵심 AC(그 외): 목표 흐름(§0) 전 구간 실주행 / CP2 독립 세션(자가판정 완료 확정 0) / **framework/loop/step-host/ 코드·주석에 AI·provider 토큰 0 + Core·정본·프로토콜 문서에 provider 플래그 문자열 0(전수 스캔)** / Frozen spec 개정 0 / 기존 형태 A 경로 무손상(회귀).

## §9. 결정 지점 처리 결과 (2026-07-13 사용자 확정)

- **D-1 승인** — `framework/runtime/step-hosting-protocol.md`.
- **D-2 재검증 후 확정** — 책임 3분리·§4 표(중립 Host = `framework/loop/step-host/`·Claude 매핑 = `adapters/claude/`·`adapters/generic/` 안 기각).
- **D-3 승인** — 단일 마일스톤 W0→W3.
