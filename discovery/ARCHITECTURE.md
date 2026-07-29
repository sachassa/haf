# discovery — Architecture (발견 / Project Discovery Layer)

작성일: 2026-07-12
상태: v1.3 정합 · 완전 저술 (스텁 대체)
상위 규약: 루트 `ARCHITECTURE.md` (라우터) · `AGENT.md`
근거 정본 (각 § 포인터로만 참조 — 재정의·복제 0):

- `discovery/specs/02-discovery.md` — discovery Layer & Project Discovery의 **상세 계약 정본**. 특히 §3.1·§3.2·§3.3·§3.4·§3.5·§3.6·§3.7·§3.8(DISC-INV-1~10)·§3.9~§3.16(Module부)·§4·§5.
- 루트 `ARCHITECTURE.md` (라우터) — UAF 상위 구조 정본. 특히 §2.1·§2.2·§2.5·§3·§6(원칙 6·7·8)·§7(P2·P4)·§8(UAF-INV ②③⑤⑥)·§10·§11·§12.2.
- `uahf/specs/00-glossary.md` §3.3 — UAHF 용어 정본. INV-3 무촉 근거.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **개관 고도.** 이 문서는 루트 `ARCHITECTURE.md`(라우터)와 `discovery/specs/02-discovery.md`(상세 계약) **사이의 Layer 개관**이다 — "무엇이 어디에 있고 어떻게 연결되는가"만 서술하고, 상세 계약(Compiler 3부 전개·State Machine 전이표·Event Model 문면·판정식·모듈 표·불변 문면)은 02가 소유한다(§ 포인터만·재정의 0). 접점 원칙·INV-3 무촉·Layer 어휘 주의·Core 문서 관행(특정 AI·모델·제품 기능명 0)은 루트 §0·§2.4·§8 UAF-INV ①을 그대로 따르며 여기서 재서술하지 않는다.
- **C1 — Entry Resolution 상류 참조 / C3 — 범위 한정.** Entry Layer·Entry Resolution의 물리 귀속은 `entry/`이며 discovery는 그 산출(Discovery Request)을 **소비만** 한다(소유·재서술 0). 본 문서의 개관 범위는 **Project Discovery(Compiler·State Machine) 위상**으로 한정되고, 하류 Project Contract의 스키마 상세는 `planning/` 소관이다(§3·§6).

---

## §1. 목적 (Purpose)

discovery Layer는 상류가 산출한 **Discovery Request(+증거)를 입력으로, 단일 타깃 형식인 Project Contract를 산출하는 Compiler**의 위상을 책임진다(개관). Project Discovery는 단일 기능이 아니라 Compiler이며, 어떤 Discovery Strategy를 쓰든 결과는 항상 동일한 Project Contract다 (루트 §7 P2·§8 UAF-INV ③, Strategy Invariance).

이 책임의 상세 계약(Compiler 3부 구조·State Machine 단일 정본·Event Model·Termination·Execution Ready 판정식·모듈 구성·불변)은 `discovery/specs/02-discovery.md`가 소유하며, 상세 목적·Non-Goals 정본은 02 §1이다.

---

## §2. Layer 내부 구조 (개관 + 위임)

discovery Layer의 내부는 다음 요소로 구성된다. 각 요소의 상세 계약은 02가 소유하며, 여기서는 1~2문장 개관과 § 포인터만 둔다(표·전이·판정식·불변 문면 복제 금지).

- **Compiler 3부 구조.** Discovery는 Front-end(교체 가능한 증거 수집 Strategy) · Middle(Confidence 측정·Synthesis) · Back-end(Project Contract Compiler)의 3부로 구성된다. Front-end가 바뀌어도 Middle·Back-end의 출력 스키마·완결 기준은 불변이다(Strategy Invariance). 3부 구조·활성 구간의 정본: 02 §3.1.
- **State Machine 단일 정본.** Discovery의 진행은 단일 정본 State Machine으로 정의되며, 비종단 6상태·종단 5상태로 구성되고 모든 전이는 Event로만 일어난다. 상태·전이 **전수** 열거표·파생 뷰 3의 정본: 02 §3.3·§3.4. `uaf-verified: 전이표의 전수 열거 의무를 discovery/specs/02-discovery.md §3.3·§3.8 DISC-INV-1(Event 없는 전이 없음)에서 확인 · 검색 범위 = 02 §3.3·§3.8.`
- **Event Model·Metrics 파생.** 모든 상태 전이를 유발하는 Event는 15종이며 append-only로 기록되고, 관측 지표(Metrics)는 별도 계측이 아니라 이 Event 로그에서만 파생된다(Event Driven). 정본: 02 §3.5·§3.16 (루트 §6 원칙 6).
- **Module Structure(7 모듈).** Compiler 3부는 Orchestrator·Strategy Registry+Provider Interface·Question Engine·Evidence Store·Confidence Model·Contract Compiler·Discovery Policy의 7개 논리 모듈로 실현되며, 모듈은 State Machine을 구동할 뿐 재정의하지 않는다. 정본: 02 §3.9.
- **Strategy Provider Interface·확신 축.** 증거 수집 Front-end는 Capability 선언으로 등록·선택되는 교체 가능한 Strategy Provider이며(Capability First), Discovery는 5개 Discovery Dimension에 대해 차원별 Confidence를 측정하고 Question Budget을 집행한다. 정본: 02 §3.10~§3.14 (루트 §6 원칙 7·8).
- **Termination·Execution Ready·Discovery Policy.** Discovery는 4경로로 종단에 이르고, 종단 판정 Execution Ready는 Completeness ∧ Confidence ∧ 사용자 승인의 2축(+게이트) 판정식으로 정의되며, 임계값·예산·종료 규칙은 데이터로 외부화된다(Policy as Data). 정본: 02 §3.6·§3.7·§3.15.
- **Layer 디렉터리 구성.** `discovery/ARCHITECTURE.md`(본 문서·Layer 개관 정본) · `discovery/specs/02-discovery.md`(상세 계약 정본) · `discovery/.claude/README.md`(override 설정 표면 명찰; 현재 override 없음 — 루트 §5) · `discovery/README.md`·`discovery/ROADMAP.md`(Layer 소개·로드맵) · `discovery/docs/`(자리 표시자).

---

## §3. 입출력 연결 계약 (Inter-Layer Connection)

- **consumes — Discovery Request.** discovery Layer는 상류 `entry/`(Entry Resolution)가 생산한 **Discovery Request**({mode, inputs, policy}) 하나를 입력으로 소비한다. 이는 요소 간 데이터 계약이며, discovery는 이 확정 추상만 소비한다 (루트 §3 연결 계약·§2.2 파이프라인 순서). Entry Resolution의 상세는 상류(`entry/`) 소관이며 discovery는 재정의하지 않는다(C1).
- **produces — Project Contract.** discovery Layer는 Discovery의 산출로 **Project Contract**를 생산한다. 이는 하류 `planning/`·`uahf/`의 **선택 입력**이 되는 공식 Stable Contract(Public API)이며, UAF↔UAHF의 유일 접점이다 (루트 §3·§2.2, P3·UAF-INV ①②).
- **의존 방향.** 연결은 `entry ──[Discovery Request]──▶ discovery ──[Project Contract]──▶ planning/uahf` **단방향**이며, discovery는 상류(entry)를 역참조하지 않고 하류(UAHF·Execution)도 역참조하지 않는다 (루트 §2.5). 이 폐쇄성이 각 요소의 교체 가능성을 성립시킨다.
- **스키마 소유.** Discovery Request 3요소 추상의 정본은 루트 §12.2이고(discovery는 이 추상을 재정의하지 않는다 — 재정의 0), Project Contract의 스키마·버저닝·완결 기준 정본은 `planning/specs/03-project-contract.md`다. discovery는 "필수 코어 필드"·"완결 기준"을 추상으로만 참조한다(C3). 연결 payload는 서술(narrative)이 아니라 **타입 계약(schema)**이며(루트 §3), 계약이 파일로 남으므로 하류가 독립적으로 파싱·소비한다.

---

## §4. Layer 고유 절 — 파이프라인 위상 (Project Discovery Compiler)

- **파이프라인 위상.** discovery Layer는 UAF 6요소 파이프라인의 **중류 단계**다 — Discovery Request(+증거)를 입력받아 Project Contract로 컴파일하는 Compiler 단계다 (루트 §2.2). 내부적으로 State Machine은 고정된 위상 순서 **Contextualizing → Eliciting → Synthesizing → Validating → Compiling**(비종단 6상태)으로 흐르며 종단(Ready 등)에 이른다. 이 위상 순서는 "이 Layer가 파이프라인에서 차지하는 자리"를 가리키는 표지이며, 각 상태·전이·가드의 알고리즘 상세는 02 §3.3이 소유한다(본 문서는 전이표를 복제하지 않는다).
- **Compiler 위상·Strategy Invariance 경계.** Front-end(Strategy)는 교체 가능한 증거 수집 계층이지만, 어떤 Strategy를 쓰든 Middle·Back-end의 출력 스키마·완결 기준은 불변이며 산출은 항상 동일한 Project Contract다 (02 §3.1, 루트 §8 UAF-INV ③). 방법론 지식은 교체 가능한 Strategy Provider만이 알고 Framework 정본으로 새지 않는다 (루트 §8 UAF-INV ⑥).
- **확정 게이트 위상·비수행 경계.** Discovery는 `Validating` 단계의 **사용자 승인 게이트**를 통과해야만 Ready 종단에 이르며(02 §3.7 축3, 루트 §8 UAF-INV ⑤), 승인 없이는 어떤 Ready 종단에도 도달하지 않는다. discovery는 Project Contract를 산출한 지점에서 멈추고, 하류의 Agent 실행·Planning·Workflow 실행을 수행하지 않는다(§6).
- **Adapter 바인딩 (포인터만).** Event 로그의 직렬화·저장, 사용자 확인·강제(Override) 채널, Contextualizing 증거 스캔·프레이밍의 물리 구현, Strategy 실행 호스팅은 전부 Adapter 소관이다. 소관 정본: 02 §4(바인딩 지점·이식 교체 지점) 및 해당 실행 환경 Adapter의 발견 바인딩(`discovery/adapters/<adapter>/discovery-binding.md`). 본 문서는 물리 형태를 지시하지 않는다.

---

## §5. 불변 (Invariants — 개관)

discovery Layer의 불변은 **DISC-INV-1~10**이며 문면 정본은 `discovery/specs/02-discovery.md` §3.8이 소유한다 — 요지 요약을 이 문서에 복제하지 않는다. 상위 정합 좌표는 루트 §7 P2·P4 · §7.1 상시 불변 확인 2건(DISC-INV-7·8이 그 반영) · §8 UAF-INV ②③⑤⑥다.

---

## §6. 경계 · Non-Goals (Layer 관점)

discovery Layer의 비수행 경계(하류 UAHF 책임 5건 · Entry Resolution 수행·재서술 · Project Contract 스키마 정의 · Memory 회수·활용 · 물리 실현)는 상위·상류·하류 정본이 소유한다 — 정본 = 루트 §10 책임 경계표(비담당 5) · 루트 §11 Non-Goals · `discovery/specs/02-discovery.md` §1(Non-Goals)·§3.8(DISC-INV-8)·§5(Memory 확장 포인트) · `planning/specs/03-project-contract.md`(스키마) · 본 문서 §4(Adapter 소관)·§0(C1·C3).

---

## §7. 정본 포인터 표 (Routing)

값을 하드코딩하지 않고 정본 위치로만 라우팅한다. §2가 이미 가리키는 02 하위 § 포인터는 여기서 재열거하지 않는다.

| 항목 | 정본 |
|---|---|
| discovery Layer 상세 계약 전체(Compiler·State Machine·Event·판정식·모듈) | `discovery/specs/02-discovery.md` §3 |
| Discovery Principles P-D1~P-D5 | `discovery/specs/02-discovery.md` §3.2 |
| Invariants DISC-INV-1~10 | `discovery/specs/02-discovery.md` §3.8 |
| Adapter Binding(바인딩 지점·이식 교체 지점) | `discovery/specs/02-discovery.md` §4 · `discovery/adapters/<adapter>/discovery-binding.md` |
| Memory 활용(확장 포인트) | `discovery/specs/02-discovery.md` §5 |
| 최상위 Layer 지도 · Project Discovery 귀속 | 루트 `ARCHITECTURE.md` §2.1 |
| 6요소 파이프라인 의미론 · 의존 방향 | 루트 `ARCHITECTURE.md` §2.2 · §2.5 |
| Layer 연결 계약(Discovery Request · Project Contract) | 루트 `ARCHITECTURE.md` §3 |
| Discovery Request 3요소 추상 | 루트 `ARCHITECTURE.md` §12.2 |
| 사용자 고정 원칙 P2·P4 · 불변 UAF-INV ②③⑤⑥ | 루트 `ARCHITECTURE.md` §7 · §8 |
| 책임 경계표(담당 4·비담당 5) | 루트 `ARCHITECTURE.md` §10 |
| Project Contract 스키마·완결 기준 | `planning/specs/03-project-contract.md` |
| `.claude` Global Default / override 경계 | 루트 `ARCHITECTURE.md` §5 |
| Layer 어휘(INV-3 무촉) 근거 | `uahf/specs/00-glossary.md` §3.3 |
| 상위 규약 | `AGENT.md` |
