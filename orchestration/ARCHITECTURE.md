# orchestration — Architecture (프로젝트 오케스트레이션 Layer)

작성일: 2026-07-13
상태: v1.6 Baseline (CP2 5단계 전건 첫 판정 Pass — S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0 · CP3 승인 · 사용자 승인 2026-07-13)
상위 규약: 루트 `ARCHITECTURE.md` (라우터) · `AGENT.md`
근거 정본 (각 § 포인터로만 참조 — 재정의·복제 0):

- `orchestration/specs/05-project-orchestration.md` — orchestration Layer의 **상세 계약 정본**. 본 문서가 개관하고 위임하는 대상. 특히 §2(위상)·§3.1~§3.7(Project Work Graph·Revision Ledger·Gate Policy·할당·Model Selection·Artifact Record·독립 실행 모델)·§4(PO-INV 1~8)·§5(Adapter 바인딩)·§6(무수정 경계).
- 루트 `ARCHITECTURE.md` (라우터) — UAF 상위 구조 정본. 특히 §2.3("Agentic Runtime (향후)" slot — 본 Layer가 실현)·§2.5(의존 방향 — substrate 소비의 허용 방향)·§8(UAF-INV ① 무수정·⑤ 사용자 승인)·§11("Layer 연결·오케스트레이션 정식화" 후속 트랙 예약 — 본 트랙이 실현).
- `uahf/framework/runtime/step-hosting-protocol.md` — substrate 계약(무수정 재사용 대상). 단일 run 무인 관리의 정본이며, 본 Layer는 그 중립 모듈을 라이브러리로 무수정 재사용한다.
- `uahf/specs/00-glossary.md` §3.3 — UAHF 용어 정본. INV-3("Layer는 정확히 6개다") 무촉 근거. § 포인터로만 참조하며 UAHF 정본을 변경하지 않는다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-13 | S1 Draft r2 | 신규 저술(배치 재검증 게이트 확정 2026-07-13). orchestration Layer 개관 정본 신설(라우터 ↔ 하위 spec 사이의 **Layer 개관 고도**). 상세 계약(Revision Ledger·Gate Policy 5종·할당 3층·Artifact Record·PO-INV 문면)은 `orchestration/specs/05-project-orchestration.md`가 소유하고 본 문서는 § 포인터로만 위임(재정의·복제 0). 루트 §2.3 Agentic Runtime slot 실현·자매 01~04 Layer 정합. UAF 레벨 신규 Layer이되 UAHF 6-Layer 무촉(INV-3)·UAHF 정본 무수정(UAF-INV ① — substrate 라이브러리 무수정 재사용)·특정 AI/모델/제품 기능명 0. | Worker (Advisor 위임, Task S1 r2) |
| 2026-07-13 | v1.6 Baseline | 마일스톤 v1.6 「Project Orchestration / Dynamic Agent System」 사용자 승인 — 기준선 확정(Baseline 승격·상태행 승격·루트 `ARCHITECTURE.md` v1.5 §2.1 라우터 등재). S1~S5 전 단계 완료 — CP2 5단계 전건 첫 판정 Pass(S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0)·CP3 승인. 개관 본문 무변경(상세 계약 정본 = `orchestration/specs/05-project-orchestration.md`). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, 루트 `ARCHITECTURE.md` §9·`entry/ARCHITECTURE.md` §9 동형. 절 번호는 §9지만 배치는 머리다. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **개관 고도 선언.** 이 문서는 루트 `ARCHITECTURE.md`(라우터)와 하위 spec `orchestration/specs/05-project-orchestration.md`(상세 계약) **사이의 Layer 개관**이다. "무엇이 어디에 있고 어떻게 연결되는가"를 서술하며, "그것이 정확히 무엇인가"의 상세 계약 — Revision Ledger 결정성 조건·Gate Policy 5종 매핑·할당 3층·Artifact Record 필드·PO-INV 문면 — 은 05가 소유한다. 본 문서는 그 계약을 **§ 포인터로만 참조**하고 재정의·복제하지 않는다(재정의 0).
- **UAF 레벨 Layer·Agentic Runtime slot 실현.** `orchestration/`은 UAF 파이프라인 축의 **최상위 물리 Layer**이며, 루트 §2.3 "Agentic Runtime (향후)" slot의 실현이다(자매 = `entry/`·`discovery/`·`planning/`). Discovery·Solution Design 산출물을 인수해 프로젝트 완료까지 lifecycle을 관리하며 UAHF를 execution substrate로 소비한다(§4).
- **UAHF 정본 무수정 (UAF-INV ①).** 본 Layer는 UAHF 정본(`uahf/`·상위 규약)을 변경하지 않는다. UAHF와의 관계는 **substrate 소비**다 — 중립 모듈(`uahf/framework/loop/step-host/`)을 **라이브러리로 무수정 재사용**하며, 이는 루트 §2.5 "상위만이 하위를 안다"의 허용 방향이다(UAF-INV ①의 핵심 = '무수정'). `uahf/` 트리 접촉은 정확히 2건(바인딩 신설·OQ-SH-4 1개소, 05 §5·§6)뿐이다.
- **INV-3 무촉 (Layer 어휘 주의).** "orchestration **Layer**"의 "Layer"는 UAHF 6-Layer 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter)의 지층(stratum)이 아니라, UAF 파이프라인 축의 지도 단위다(루트 §0 용어 주의·§2.4). 본 Layer는 UAHF 수직 스택에 편입되지 않으며, Glossary INV-3("Layer는 정확히 6개다", `uahf/specs/00-glossary.md` §3.3)는 무촉이다.
- **Core 문서 관행.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·언어·툴체인·직렬화 형식을 두지 않는다(루트 §0·05 §0 동형). 직렬화 형식·물리 배치·게이트 큐 채널·정책 실값 등 환경 구체는 Adapter Binding 소관이며, 필요한 자리에는 일반형 표기와 소관 포인터만 둔다.

---

## §1. 목적 (Purpose)

orchestration Layer는 Discovery·Solution Design이 산출한 프로젝트 정의(Project Contract 인스턴스)를 인수하여, 프로젝트 완료까지 **동적 작업 그래프·게이트·역할/모델 할당·산출물 계보를 무인으로 조율**하는 데까지를 책임진다(개관). 조율 방식은 **판단하지 않는 기계 구동자**이며, 단일 run의 무인 실행은 UAHF Step Host를 substrate로 위임하고 재구현하지 않는다(루트 §2.3·§2.5).

이 책임의 상세 계약(Work Graph 소비·Revision Ledger·Gate Policy·할당·Model Selection·Artifact Record·불변)은 `orchestration/specs/05-project-orchestration.md`가 소유하며, 본 문서는 그 지도를 개관 고도로 제시한다. 상세 목적·경계 정본은 05 §0·§1이다.

---

## §2. Layer 내부 구조 (개관 + 위임)

orchestration Layer의 내부는 다음 요소로 구성된다. 각 요소의 상세 계약은 05가 소유하며, 여기서는 1~2문장 개관과 § 포인터만 둔다(표·규칙·불변 문면 복제 금지).

- **위상 — UAF 레벨 상위 컴포넌트 + 기계 구동자.** "PM Agent"는 기계 조율(Orchestrator)·의미 판단(국소 Step)·확정 권위(사용자)로 3분해되어 소멸한다. Orchestrator는 headless이며 사용자 채널은 대화 세션·게이트 큐뿐이다. 정본: 05 §2.
- **Project Work Graph.** `uahf/specs/07-workflow.md` §3.2-A Work Graph 스키마를 상위 입도(프로젝트 작업 단위)로 무수정 재사용한다. 작업 단위 유형은 개방 네임스페이스·데이터다. 정본: 05 §3.1.
- **Graph Revision Ledger.** 진행 중 그래프 확장을 append-only RevisionEvent 원장 + fold 파생 뷰로 실현한다(결정성 3조건). 정본: 05 §3.2.
- **Gate Policy·할당·Model Selection·Artifact Record.** 5종 게이트 어휘와 단조성, Role/AgentSpec/Instance 3층 할당, 모델 선택 정책(hysteresis), 산출물 계보 인덱스. 정본: 05 §3.3~§3.6.
- **독립 실행 Agent 모델.** 설계 단위는 특별 취급 0인 일반 실행 모델이며, `04-solution-design` §3.4 협업 프로토콜을 headless step + 사용자 게이트로 호스팅한다. 정본: 05 §3.7.
- **Layer 디렉터리 구성 (실측 — 2026-07-13 파일 시스템 직접 확인).**
  - `orchestration/ARCHITECTURE.md` — 본 문서(Layer 개관 정본).
  - `orchestration/specs/05-project-orchestration.md` — 상세 계약 정본.
  - `orchestration/ROADMAP.md` — Layer 로드맵(스텁).
  - (후속) 중립 코드 `orchestration/framework/orchestrator/`·README·설정 표면 명찰·`docs/`는 본 트랙(S1) 범위 밖이며 후속 단계(S2~)에서 생성된다.

---

## §3. 입출력 연결 계약 (Inter-Layer Connection)

- **consumes — Project Contract 인스턴스.** orchestration Layer는 상류 `planning/`(Project Contract·Solution Design 성숙 계보, 루트 §2.2)의 산출인 **Ready/Matured Contract 인스턴스 + 확정 artifact**를 실행 위임(execution mandate)으로 인수한다. 이는 `04-solution-design` §3.1-D가 사용자 소관으로 남긴 Handoff 지점을 무인 조율로 잇는 요소 간 연결이다.
- **substrate 소비 — UAHF.** orchestration Layer는 각 작업 단위(run)를 UAHF Step Host(`uahf/framework/runtime/step-hosting-protocol.md`)를 substrate로 하여 실행한다. 이는 파이프라인 하류 실행 계층의 **라이브러리 무수정 재사용**이다(05 §0·§2.2).
- **의존 방향.** 연결은 `planning ──[Project Contract]──▶ orchestration ──[substrate 소비]──▶ uahf` **단방향**이며, orchestration은 상위(상류 Contract)를 인수하고 하위(UAHF)를 substrate로 소비하되, 어느 쪽도 orchestration을 역참조하지 않는다(루트 §2.5 — 상위만이 하위를 안다).
- **스키마 소유.** Project Contract 스키마 정본은 `planning/specs/03-project-contract.md`이고, 본 Layer는 그것을 tolerant reader로 소비만 하며 재정의하지 않는다(재정의 0). 본 Layer가 신규 소유하는 연결·기록 계약(RevisionEvent·GatePolicyEntry·AgentSpec·ArtifactRecord)의 정본은 05 §3이다.

---

## §4. Layer 고유 절 — 파이프라인 위상 (Agentic Runtime slot 실현)

- **파이프라인 위상.** orchestration Layer는 루트 §2.3 "Agentic Runtime (향후)" slot을 실현하는 UAF 레벨 컴포넌트다 — 상류 산출물을 인수해 프로젝트 완료까지 실행 lifecycle을 무인 조율하는 자리다(루트 §2.2 파이프라인 하류·§2.3). UAHF의 Runtime Layer(`uahf/specs/00-glossary.md` §3.2-A)와는 **별개 네임스페이스**다(루트 §2.3 주의·§12).
- **단일 run 무인 관리는 Step Host 소관·재구현 0.** 본 Layer는 단일 run의 사이클 구동·상태 파생·결정적 재개를 신설하지 않고 UAHF Step Host에 위임한다(05 §2.2). 디스패치 입도는 run/작업 단위이지 개별 step이 아니다.
- **대화 주체 분리 — Discovery 대화를 흡수하지 않음.** Orchestrator는 headless이며 사용자 대화 주체와 분리된다. 대화형 단위(Discovery Eliciting류)는 규칙의 예외가 아니라 "사용자 채널에 위임되는 capability"로 정책 데이터에 선언된다 — 본 Layer가 Discovery 대화를 흡수·재수행하지 않는다(05 §2.2·§3.7).
- **Adapter 바인딩 (포인터만).** 직렬화 형식·물리 배치·게이트 큐 제시 채널·capability→물리 호출 매핑·정책 실값은 전부 Adapter 소관이다. 소관 정본: 05 §5 및 `orchestration/adapters/<adapter>/project-orchestration-binding.md`(신설 예정). 본 문서는 물리 형태를 지시하지 않는다.

---

## §5. 불변 (Invariants — 개관)

orchestration Layer의 불변은 **PO-INV 1~8**(정본: 05 §4)이 소유한다. 아래는 명칭·번호 인용과 1줄 요지이며, 문면·모태 대응 정본은 05 §4다(복제 아님). 전 8건은 기존 정본 불변(SH-INV/SP-INV/PC-INV/C-3)의 파생이며 새 Core Contract를 창설하지 않는다.

- **PO-INV 1 — 판단 금지 상속.** 중립 Orchestrator는 의미 판단 0.
- **PO-INV 2 — 이중 원장 append-only.** revision 원장·step 이벤트 로그 모두 append-only·현재 상태는 파생 뷰.
- **PO-INV 3 — 결정적 재개.** 동일 원장 쌍 → 동일 그래프 → 동일 ready_set.
- **PO-INV 4 — 게이트 단조성.** 코드 소유 하한 약화 불가·강화만·Autonomy 축과 직교.
- **PO-INV 5 — revision 근거 필수.** 모든 revision은 proposingStepRef + gateEventRef를 갖는다.
- **PO-INV 6 — 역할 추상 유지.** 할당기는 Capability 선언까지만 소비·물리 매핑은 Adapter.
- **PO-INV 7 — artifact 계보.** append-only + supersedes·provenance 불투명.
- **PO-INV 8 — 중립성·격리.** 중립 코드에 provider/모델/상류 Layer 고유명 토큰 0·상위 반환은 요약만.

**상위 불변 정합.** 위 PO-INV는 상위 UAF 불변을 orchestration 수준에서 구속한다 — 특히 **UAF-INV ①**(UAHF 무수정, 루트 §8)·**UAF-INV ⑤**(확정 게이트 = 사용자 승인, 루트 §8 — PO-INV 4 `user_decision_required`)와 정합한다.

---

## §6. 경계 · Non-Goals (Layer 관점)

orchestration Layer는 다음을 **수행하지 않는다**(경계). 각 항목은 상류·하류·타 소관이며, 중복 서술이 아니라 Layer 관점의 경계 재확인이다.

- **단일 run 실행 엔진 신설 제외** — 사이클 구동·상태 파생·결정적 재개는 UAHF Step Host 소관이며 재구현하지 않는다 (05 §2.2, 두 번째 Runtime 아님).
- **의미 판단 제외** — 완료/실패/검증/승인 판정은 기존 주체(Worker·Verifier·Advisor·사용자) 소관이다 (PO-INV 1).
- **Discovery·Solution Design 재수행 제외** — 상류 산출물은 인수하며 재생성하지 않는다 (루트 §2.5, `04-solution-design` 소관).
- **UAHF 정본 수정 제외** — UAHF와의 관계는 라이브러리 무수정 재사용이다. `uahf/` 트리 접촉은 정확히 2건(바인딩 신설·OQ-SH-4 1개소)뿐 (UAF-INV ①, 05 §6).
- **물리 실현(Adapter) 제외** — 직렬화·물리 배치·게이트 큐 채널·정책 실값은 Adapter 소관이다 (§4, 05 §5).

상세 무수정 경계·실측 대조 정본은 05 §6이고, 상위 Non-Goals는 루트 §11이다.

---

## §7. 정본 포인터 표 (Routing)

값을 하드코딩하지 않고 정본 위치로만 라우팅한다.

| 항목 | 정본 |
|---|---|
| orchestration Layer 상세 계약(위상·그래프·게이트·할당·모델·artifact·불변) | `orchestration/specs/05-project-orchestration.md` §2~§6 |
| Project Work Graph(상위 입도 재사용) | `orchestration/specs/05-project-orchestration.md` §3.1 · `uahf/specs/07-workflow.md` §3.2-A |
| Graph Revision Ledger(RevisionEvent·결정성 3조건) | `orchestration/specs/05-project-orchestration.md` §3.2 |
| Gate Policy 5종·단조성 | `orchestration/specs/05-project-orchestration.md` §3.3 |
| 할당 3층(Role/AgentSpec/Instance) · Model Selection | `orchestration/specs/05-project-orchestration.md` §3.4 · §3.5 |
| Artifact Record·Registry | `orchestration/specs/05-project-orchestration.md` §3.6 |
| 불변 PO-INV 1~8 | `orchestration/specs/05-project-orchestration.md` §4 |
| Adapter Binding(바인딩 지점·무수정 경계) | `orchestration/specs/05-project-orchestration.md` §5 · §6 · `orchestration/adapters/<adapter>/project-orchestration-binding.md` |
| substrate 계약(단일 run 무인 관리) | `uahf/framework/runtime/step-hosting-protocol.md` |
| Agentic Runtime slot · 의존 방향 | 루트 `ARCHITECTURE.md` §2.3 · §2.5 |
| Layer 연결·오케스트레이션 정식화 예약 | 루트 `ARCHITECTURE.md` §11 |
| 불변 UAF-INV(무수정·사용자 승인) | 루트 `ARCHITECTURE.md` §8 |
| Layer 어휘(INV-3 무촉) 근거 | `uahf/specs/00-glossary.md` §3.3 |
| 상위 규약 | `AGENT.md` |
