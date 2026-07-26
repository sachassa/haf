# orchestration — Architecture (프로젝트 오케스트레이션 Layer)

작성일: 2026-07-13
상태: v1.6 Baseline (CP2 5단계 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-13 — 단계별 판정 수치는 git 이력)
상위 규약: 루트 `ARCHITECTURE.md` (라우터) · `AGENT.md`
근거 정본 (각 § 포인터로만 참조 — 재정의·복제 0):

- `orchestration/specs/05-project-orchestration.md` — orchestration Layer의 **상세 계약 정본**. 특히 §2·§3.1~§3.7·§4(PO-INV 1~8)·§5·§6.
- 루트 `ARCHITECTURE.md` (라우터) — UAF 상위 구조 정본. 특히 §2.3(Agentic Runtime slot — 본 Layer가 실현)·§2.5(substrate 소비의 허용 방향)·§8(UAF-INV ①·⑤)·§11.
- `uahf/framework/runtime/step-hosting-protocol.md` — substrate 계약(무수정 재사용 대상). 단일 run 무인 관리의 정본.
- `uahf/specs/00-glossary.md` §3.3 — UAHF 용어 정본. INV-3 무촉 근거.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **개관 고도.** 이 문서는 루트 `ARCHITECTURE.md`(라우터)와 `orchestration/specs/05-project-orchestration.md`(상세 계약) **사이의 Layer 개관**이다 — "무엇이 어디에 있고 어떻게 연결되는가"만 서술하고, 상세 계약(Revision Ledger 결정성 조건·Gate Policy 5종 매핑·할당 3층·Artifact Record 필드·PO-INV 문면)은 05가 소유한다(§ 포인터만·재정의 0). INV-3 무촉·Layer 어휘 주의·Core 문서 관행(특정 AI·모델·제품 기능명·언어·툴체인·직렬화 형식 0)은 루트 §0·§2.4를 그대로 따르며 여기서 재서술하지 않는다.
- **UAF 레벨 Layer·Agentic Runtime slot 실현.** `orchestration/`은 UAF 파이프라인 축의 **최상위 물리 Layer**이며, 루트 §2.3 Agentic Runtime slot의 실현이다(자매 = `entry/`·`discovery/`·`planning/`). Discovery·Solution Design 산출물을 인수해 프로젝트 완료까지 lifecycle을 관리하며 UAHF를 execution substrate로 소비한다(§4).
- **접점 원칙 (UAF-INV ①).** UAHF와의 관계는 **substrate 소비**다 — 중립 모듈(`uahf/framework/loop/step-host/`)을 **라이브러리로 무수정 재사용**하며, 이는 루트 §2.5 "상위만이 하위를 안다"의 허용 방향이다(UAF-INV ① 접점 원칙과 병존하는 하향 소비 — 루트 §8 주). `uahf/` 트리 접촉은 정확히 2건(바인딩 신설·OQ-SH-4 1개소, 05 §5·§6)뿐이다.

---

## §1. 목적 (Purpose)

orchestration Layer는 Discovery·Solution Design이 산출한 프로젝트 정의(Project Contract 인스턴스)를 인수하여, 프로젝트 완료까지 **동적 작업 그래프·게이트·역할/모델 할당·산출물 계보를 무인으로 조율**하는 데까지를 책임진다(개관). 조율 방식은 **판단하지 않는 기계 구동자**이며, 단일 run의 무인 실행은 UAHF Step Host를 substrate로 위임하고 재구현하지 않는다(루트 §2.3·§2.5).

이 책임의 상세 계약(Work Graph 소비·Revision Ledger·Gate Policy·할당·Model Selection·Artifact Record·불변)은 `orchestration/specs/05-project-orchestration.md`가 소유하며, 상세 목적·경계 정본은 05 §0·§1이다.

---

## §2. Layer 내부 구조 (개관 + 위임)

orchestration Layer의 내부는 다음 요소로 구성된다. 각 요소의 상세 계약은 05가 소유하며, 여기서는 1~2문장 개관과 § 포인터만 둔다(표·규칙·불변 문면 복제 금지).

- **위상 — UAF 레벨 상위 컴포넌트 + 기계 구동자.** "PM Agent"는 기계 조율(Orchestrator)·의미 판단(국소 Step)·확정 권위(사용자)로 3분해되어 소멸한다. Orchestrator는 headless이며 사용자 채널은 대화 세션·게이트 큐뿐이다. 정본: 05 §2.
- **Project Work Graph.** `uahf/specs/07-workflow.md` §3.2-A Work Graph 스키마를 상위 입도(프로젝트 작업 단위)로 무수정 재사용한다. 작업 단위 유형은 개방 네임스페이스·데이터다. 정본: 05 §3.1.
- **Graph Revision Ledger.** 진행 중 그래프 확장을 append-only RevisionEvent 원장 + fold 파생 뷰로 실현한다(결정성 3조건). 정본: 05 §3.2.
- **Gate Policy·할당·Model Selection·Artifact Record.** 5종 게이트 어휘와 단조성, Role/AgentSpec/Instance 3층 할당, 모델 선택 정책(hysteresis), 산출물 계보 인덱스. 정본: 05 §3.3~§3.6.
- **독립 실행 Agent 모델.** 설계 단위는 특별 취급 0인 일반 실행 모델이며, `04-solution-design` §3.4 협업 프로토콜을 headless step + 사용자 게이트로 호스팅한다. 정본: 05 §3.7.
- **Layer 디렉터리 구성.** `orchestration/ARCHITECTURE.md`(본 문서·Layer 개관 정본) · `orchestration/specs/05-project-orchestration.md`(상세 계약 정본) · `orchestration/ROADMAP.md`(Layer 로드맵) · `orchestration/framework/`(중립 Orchestrator 코드) · `orchestration/adapters/`(환경 바인딩·데이터 격리). `uaf-verified: orchestration/ 1단계 하위를 ls -A로 열거해 대조 — S1 시점 "후속 생성" 표기를 실재 반영으로 정정. 검색 범위 = orchestration/ 1단계 하위.`

---

## §3. 입출력 연결 계약 (Inter-Layer Connection)

- **consumes — Project Contract 인스턴스.** orchestration Layer는 상류 `planning/`(Project Contract·Solution Design 성숙 계보, 루트 §2.2)의 산출인 **Ready/Matured Contract 인스턴스 + 확정 artifact**를 실행 위임(execution mandate)으로 인수한다. 이는 `04-solution-design` §3.1-D가 사용자 소관으로 남긴 Handoff 지점을 무인 조율로 잇는 요소 간 연결이다.
- **substrate 소비 — UAHF.** orchestration Layer는 각 작업 단위(run)를 UAHF Step Host(`uahf/framework/runtime/step-hosting-protocol.md`)를 substrate로 하여 실행한다. 이는 파이프라인 하류 실행 계층의 **라이브러리 무수정 재사용**이다(05 §0·§2.2).
- **의존 방향.** 연결은 `planning ──[Project Contract]──▶ orchestration ──[substrate 소비]──▶ uahf` **단방향**이며, orchestration은 상위(상류 Contract)를 인수하고 하위(UAHF)를 substrate로 소비하되, 어느 쪽도 orchestration을 역참조하지 않는다(루트 §2.5 — 상위만이 하위를 안다).
- **스키마 소유.** Project Contract 스키마 정본은 `planning/specs/03-project-contract.md`이고, 본 Layer는 그것을 tolerant reader로 소비만 하며 재정의하지 않는다(재정의 0). 본 Layer가 신규 소유하는 연결·기록 계약(RevisionEvent·GatePolicyEntry·AgentSpec·ArtifactRecord)의 정본은 05 §3이다.

---

## §4. Layer 고유 절 — 파이프라인 위상 (Agentic Runtime slot 실현)

- **파이프라인 위상.** orchestration Layer는 루트 §2.3 Agentic Runtime slot을 실현하는 UAF 레벨 컴포넌트다 — 상류 산출물을 인수해 프로젝트 완료까지 실행 lifecycle을 무인 조율하는 자리다(루트 §2.2 파이프라인 하류·§2.3). UAHF의 Runtime Layer(`uahf/specs/00-glossary.md` §3.2-A)와는 **별개 네임스페이스**다(루트 §2.3 주의·§12).
- **단일 run 무인 관리는 Step Host 소관·재구현 0.** 본 Layer는 단일 run의 사이클 구동·상태 파생·결정적 재개를 신설하지 않고 UAHF Step Host에 위임한다(05 §2.2). 디스패치 입도는 run/작업 단위이지 개별 step이 아니다.
- **대화 주체 분리 — Discovery 대화를 흡수하지 않음.** Orchestrator는 headless이며 사용자 대화 주체와 분리된다. 대화형 단위(Discovery Eliciting류)는 규칙의 예외가 아니라 "사용자 채널에 위임되는 capability"로 정책 데이터에 선언된다 — 본 Layer가 Discovery 대화를 흡수·재수행하지 않는다(05 §2.2·§3.7).
- **Adapter 바인딩 (포인터만).** 직렬화 형식·물리 배치·게이트 큐 제시 채널·capability→물리 호출 매핑·정책 실값은 전부 Adapter 소관이다. 소관 정본: 05 §5 및 `orchestration/adapters/<adapter>/project-orchestration-binding.md`. 본 문서는 물리 형태를 지시하지 않는다.

---

## §5. 불변 (Invariants — 개관)

orchestration Layer의 불변은 **PO-INV 1~8**이며 문면·모태 대응 정본은 `orchestration/specs/05-project-orchestration.md` §4가 소유한다 — 요지 요약을 이 문서에 복제하지 않는다. 8건은 기존 정본 불변(SH-INV/SP-INV/PC-INV/C-3)의 파생이며 새 Core Contract를 창설하지 않는다. 상위 정합 좌표는 루트 §8 UAF-INV ①(접점 원칙)·⑤(확정 게이트 = 사용자 승인 — PO-INV 4 `user_decision_required`)다.

---

## §6. 경계 · Non-Goals (Layer 관점)

orchestration Layer의 비수행 경계(단일 run 실행 엔진 신설 · 의미 판단 · Discovery·Solution Design 재수행 · UAHF 정본 재정의·복제 · 물리 실현)는 상류·하류·타 정본이 소유한다 — 정본 = `orchestration/specs/05-project-orchestration.md` §2.2·§4(PO-INV 1)·§5·§6(무수정 경계·실측 대조) · `planning/specs/04-solution-design.md`(상류 소관) · 루트 §11 Non-Goals · 루트 §8 UAF-INV ① · 본 문서 §4(Adapter 소관).

---

## §7. 정본 포인터 표 (Routing)

값을 하드코딩하지 않고 정본 위치로만 라우팅한다. §2가 이미 가리키는 05 하위 § 포인터는 여기서 재열거하지 않는다.

| 항목 | 정본 |
|---|---|
| orchestration Layer 상세 계약 전체(위상·그래프·게이트·할당·모델·artifact) | `orchestration/specs/05-project-orchestration.md` §2~§3 |
| 불변 PO-INV 1~8 | `orchestration/specs/05-project-orchestration.md` §4 |
| Adapter Binding(바인딩 지점·무수정 경계) | `orchestration/specs/05-project-orchestration.md` §5 · §6 · `orchestration/adapters/<adapter>/project-orchestration-binding.md` |
| Work Graph 스키마(상위 입도 재사용 모태) | `uahf/specs/07-workflow.md` §3.2-A |
| substrate 계약(단일 run 무인 관리) | `uahf/framework/runtime/step-hosting-protocol.md` |
| Agentic Runtime slot · 의존 방향 | 루트 `ARCHITECTURE.md` §2.3 · §2.5 |
| Layer 연결·오케스트레이션 정식화 예약 | 루트 `ARCHITECTURE.md` §11 |
| 불변 UAF-INV(접점 원칙·사용자 승인) | 루트 `ARCHITECTURE.md` §8 |
| Layer 어휘(INV-3 무촉) 근거 | `uahf/specs/00-glossary.md` §3.3 |
| 상위 규약 | `AGENT.md` |
