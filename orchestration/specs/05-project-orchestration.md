# orchestration/specs/05-project-orchestration — Project Orchestration Specification

작성일: 2026-07-13
상태: v1.6 Baseline (CP2 5단계 전건 첫 판정 Pass — S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0 · CP3 승인 · 사용자 승인 2026-07-13)
상위 규약: AGENT.md (INV-1)
근거 정본:

- `docs/project-orchestration-design.md@cd9247b` (사용자 승인 2026-07-13 + **배치 재검증 게이트 확정 2026-07-13**) — 본 spec의 **설계 정본**. 계약 정본은 이 설계 문서가 아니라 아래 spec·프로토콜·바인딩이 소유한다(설계 §6 성격). 본 문서는 설계 §1~§4·§3.8(PO-INV 8건)을 provider·언어 중립 계약으로 형식화한다. 배치 결정: 소유·배치 = **UAF 레벨 신규 Layer `orchestration/`**(루트 §2.3 Agentic Runtime slot 실현) · UAHF 접촉 = **라이브러리 재사용**(무수정 import).
- 루트 `ARCHITECTURE.md` (v1.4 — 라우터) — UAF 상위 구조 정본. 특히 **§2.3**("Agentic Runtime (향후)" slot — 본 Layer가 실현하는 자리) · **§2.5**(의존 방향 단방향 — "상위만이 하위를 안다"·본 Layer의 substrate 소비가 허용 방향) · **§8**(UAF-INV ① 접점 원칙 · ⑤ 확정 게이트 = 사용자 승인) · **§11**("Layer 연결·오케스트레이션 정식화" 후속 트랙 예약 — 본 트랙이 그 실현). § 포인터로만 참조·재정의 0.
- `uahf/framework/runtime/step-hosting-protocol.md` (v1.5 Baseline) — **substrate 계약(무수정 재사용 대상)**. 본 Layer의 중립 코드는 이 Step Host의 중립 모듈을 **라이브러리로 무수정 import**하여 단일 run 실행을 위임한다(루트 §2.5 허용 방향). Step Host 위상(§2)·Step 계약(§3)·상태 파생·결정적 재개(§4)·검증 통합(§5)·진입/자율성(§6)·SH-INV 8건(§7.1)이 본 프로토콜이 상속·확장하는 모태다.
- `uahf/specs/07-workflow.md` §3.1-A(Decompose·실패 사유 코드)·§3.2-A(Work Graph·parallelSets)·§3.2-B(Task 필드)·§3.2-C(병렬 디스패치 R1~R4)·§3.2-D(Merge). 본 문서 §3이 **상위 입도로 무수정 재사용**하는 Work Graph·Task 계약.
- `uahf/specs/02-agent.md` §3.1(공통 의무 O1~O5·각 역할 Lifecycle)·§3.2-A(4역할 경계)·§3.2-B(위임 8필드)·§3.2-C(완료 보고 5필드)·§3.2-D(실패 보고)·§4.1(실행 모델 바인딩). 본 문서 §3.4가 병존시키는 4역할·할당 슬롯의 원천.
- `uahf/specs/03-loop.md` §3.1-D(사람 개입 5조건)·§3.2-A(전이 이벤트 스키마)·§3.2-B(단계 상태 5종 Pending/Active/Passed/Failed/Escalated). 본 문서 §3·§4가 재사용하는 이벤트·상태 어휘(**새 상태 열거 창설 0**).
- `uahf/specs/06-verifier.md` §3.1(독립 판정 V1~V6)·§3.2-C(최종 판정 도출)·§3.2-E(검증 유형 VT-1~VT-5). 본 문서 §3.3·§3.7이 재사용하는 검증 판정 계약.
- `planning/specs/04-solution-design.md` §3.2(복잡도 판정 Policy as Data)·§3.3(Expert Role = Capability 선언·개방 네임스페이스·최소 할당)·§3.4(협업 설계 프로토콜 State Machine·T8/T9/T10)·§3.8(SP-INV 1~8)·§3.9(확장 포인트). **본 Layer는 04-solution-design §3.9 확장 포인트 1(형태 B 실행 호스팅)·2(step 기반 실행기와의 연결)의 실현이다.**
- `planning/specs/03-project-contract.md` §3.4(인스턴스 거버넌스 — append-only·supersedes 계보·과거 문면 불변)·§3.6 PC-INV 9(인스턴스 이력 append-only). 본 문서 §3.2·§3.6이 계보 불변의 모태로 인용.
- `uahf/framework/core/structure.md` §4(실행 코드 배치 규칙 C-2·규칙 4 "형태 B 설계 시 확정")·§5(금지 토큰 규칙 C-3)·§7(Core Contract 불변 C-1). 본 Layer의 중립 코드가 **동형 준수**하는 조건.
- `uahf/specs/00-glossary.md` §3.3 INV-3(Layer 6·Cross-cutting 1·Core Component 13). 본 문서 §0이 준수하는 UAHF 계수 경계 — 본 Layer는 **UAF 레벨 물리 Layer**이며 UAHF 6-Layer 무촉(entry/discovery/planning 동형).

거버넌스: 이 문서는 `orchestration/` Layer 소속 UAF spec 정본이다(자매 = `entry/specs/01-entry.md`·`discovery/specs/02-discovery.md`·`planning/specs/03-project-contract.md`·`planning/specs/04-solution-design.md`). 본문은 특정 AI·언어·툴체인 비의존을 유지한다(`uahf/framework/core/structure.md` §5 C-3 동형·루트 §0 관행). Orchestrator의 구체 실현(직렬화 형식·물리 배치·게이트 큐 제시 채널·capability→물리 호출 매핑·모델/도구 정책 실값)은 **중립 모듈 경계·Adapter Binding 문서 소관**이며, 본 문서는 소관 포인터만 둔다(§5). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-13 | S1 Draft | 최초 작성(구 배치 = `uahf/framework/runtime/project-orchestration-protocol.md`). Project Orchestration provider·언어 중립 계약 신설 — 설계 정본 §1~§4·§3.8 형식화. 위상 선언(§2 — "PM Agent" 3분해)·Project Work Graph(§3.1)·Graph Revision Ledger(§3.2 — 신규 소유 RevisionEvent)·Gate Policy(§3.3 — 신규 소유 GatePolicyEntry·5종·단조성)·할당 계약(§3.4 — 신규 소유 AgentSpec·3층·4역할 병존)·Model Selection(§3.5 — OQ-SH-4)·Artifact Record(§3.6 — 신규 소유 ArtifactRecord)·독립 실행 Agent 모델(§3.7)·PO-INV 8건(§4). | Worker (Advisor 위임, Task S1) |
| 2026-07-13 | S1 Draft r2 | **배치 재검증 게이트(사용자 결정 2026-07-13) 반영** — 정본을 `orchestration/specs/05-project-orchestration.md`로 **이동**(UAF spec 번호 계보 01~04 승계·5번째). 재프레이밍: §0 위치 = **UAF 레벨 신규 Layer `orchestration/`**(루트 §2.3 Agentic Runtime slot 실현·자매 01~04 spec) · UAHF 관계 = **substrate 소비**(중립 모듈 라이브러리 무수정 import — 루트 §2.5 허용 방향·UAF-INV ① '무수정' 준수) · 근거 정본에 루트 §2.3·§2.5·§8·§11 추가 · step-hosting-protocol을 "substrate 계약(무수정 재사용 대상)"으로 인용 위치 조정 · uahf spec 인용을 cross-layer 전체 경로(`uahf/specs/NN-name.md §X`)로 정합(UAF 레벨 spec 관례 실측 동형) · INV-3 무촉 재프레이밍(UAF 레벨 Layer 신설이되 UAHF 6-Layer 무촉·v1.1 선례). **계약 내용(§3 계열·PO-INV 8·게이트 5종·할당 3층·Artifact Record) 무변.** 구 파일 삭제(untracked). | Worker (Advisor 재작업 지시, Task S1 r2) |
| 2026-07-13 | S1 확정 | CP2 첫 판정 **Pass**(점검 8 Met·0 Violated·0 Undetermined — 독립 토큰 전수·앵커 표본 15건 원문 대조·git 무촉 실측) · CP3 Advisor 승인. Advisor 재량 정정 1건: §6 자기 무촉 확인 수단 서술의 툴체인 토큰 1어 중립화(§7 절대 주장과의 자기 불일치 해소 — Verifier 관찰 1 회부분). Verifier 관찰 2(UAF-INV ① "접점 하나뿐" 조항 vs substrate import)는 2026-07-13 배치 게이트 사용자 결정으로 해소된 사항으로 판정·Baseline 게이트 재확인 항목으로 이월. 상태행 확정. Baseline 승격·루트 라우터 등재는 트랙 종단 사용자 게이트 유보. | Advisor |
| 2026-07-13 | v1.6 Baseline | 마일스톤 v1.6 「Project Orchestration / Dynamic Agent System」 사용자 승인 — 기준선 확정(Baseline 승격·상태행 승격·루트 `ARCHITECTURE.md` v1.5 §2.1 라우터 등재). S1~S5 전 단계 완료 — CP2 5단계 전건 첫 판정 Pass(S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0·커밋 fd112cd→ce0cdba→c65d20f→04b8f6e→745f26e→5e843dc)·CP3 승인. 본문 계약(§3 계열·PO-INV 8·게이트 5종·할당 3층·Artifact Record) 무변경. | Advisor |
| 2026-07-14 | T2 (Performance Tuning) | **§3.3 `review_required` 행만 재저술** — 재검증 Verifier 세션 재기동을 항상 수행하던 것에서 **유효 CP2 evidence(`cp2-pass`) 소비로 해소**(해소 마커가 근거 `cp2-pass`를 명시 참조·provenance 사슬)로 전환하고, 유효 evidence 부재·stale(재실행/retry · supersede/revision 영향 · 기록된 artifact 해시 불일치) 또는 정책 `requireIndependentReview` 요구 시 추가 독립 리뷰 단위 디스패치(Verifier·`uahf/specs/06-verifier.md` §3.2-E VT-1~5 재사용)를 **fallback 으로 존치**함을 명문화. 중립 코드 정합(`find_valid_cp2_evidence`·`_settle_review_gate`·`GatePolicyEntry.requireIndependentReview`·`gate-review` 마커 ref 가법 필드 `basis`/`mode`). **PO-INV 4(코드 하한 불변·`review_required`는 floor 게이트 아님)·상시 CP2(SH-INV-4)·PO-INV 1(판단 금지)·append-only·결정적 재개 무촉** — 게이트 존치·해소 근거만 변경. §3.3 이외 문면 일절 무변경. 사용자 승인 2026-07-14(Baseline 개정 게이트 통과). | Worker (Advisor 위임·T2) |
| 2026-07-17 | v1.6 (정합) | 루트 v1.7 UAF-INV ① 재정의(구 "무수정"[동결] 폐지·접점 원칙[Project Contract 단일 접점] 존치) 인용 정합 — 사용자 승인 하 Frozen 개정. ① 인용/근거 4곳(§0 근거정본 §8 포인터·§0 UAHF 관계·§6·§7)을 "①의 핵심=무수정"→"substrate 라이브러리 무수정 import는 §2.5 하향 소비로 UAF-INV ①(접점 원칙)과 병존(루트 §8 병존 주)"으로 재서술. 의미 3(substrate 무수정 import/재사용·§6 "무수정 경계" 표제·내용·라이브러리 무수정 인용) 존치. PO-INV 1~8·§3 계약·게이트 5종·§9 기존 행 무변. 참조 정합(시맨틱 개정 아님·버전 무상승). | Worker (Advisor 위임) |
| 2026-07-17 | v1.6 (정합) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — §0 근거정본(:8)의 삭제 산출물(설계 정본) 참조 앵커 전환(`docs/project-orchestration-design.md@cd9247b`). PO-INV·§3 계약·게이트·§ 포인터 문면 무변경(참조 정합·버전 무상승). | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-19 | v1.6 (명확화) | §DC-7 WBS(작업 분해) 소유 삼분 명확화 — §2.1 3분해 표 뒤에 명확화 문장 1개 append(관리=엔진 / 초안 분해=Planner Lifecycle 역할 / 실행=Worker · 2경로[a 엔진이 Planner-role proposal step 디스패치 / b Advisor 직접 위임 Planner 초안]). 위 §2.1 3분해·§3.4 2축 병존(4역할 Lifecycle 축 × Expert Role capability 축)의 인용 파생일 뿐 **재정의 0·새 계약/역할/용어 창설 0**("WBS"는 서술 라벨·정본 용어=Work Graph[Glossary J-07]). PO-INV·§3 계약·게이트·§9 기존 행 문면 무변경. | Worker (Advisor 위임) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, `entry/specs/01-entry.md` §9·`planning/specs/04-solution-design.md` §9 동형. 절 번호는 §9지만 배치는 머리다. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본 배치 (UAF 레벨 Layer 상세 계약).** 이 문서는 **`orchestration/` Layer의 상세 계약 정본**이다. `orchestration/`은 **UAF 레벨 신규 최상위 Layer**이며, 루트 `ARCHITECTURE.md` §2.3 "Agentic Runtime (향후)" slot의 실현이다(플랜 원안의 UAHF 내부 프레이밍을 대체 — 사용자 배치 재검증 게이트 2026-07-13). 자매 = `entry/specs/01-entry.md`·`discovery/specs/02-discovery.md`·`planning/specs/03-project-contract.md`·`planning/specs/04-solution-design.md`(UAF spec 번호 계보 01~04를 승계한 5번째). Layer 개관(무엇이 어디에 있고 어떻게 연결되는가)은 `orchestration/ARCHITECTURE.md`가 소유하고, 본 문서는 상세 계약을 소유한다.

- **UAHF와의 관계 = substrate 소비 (라이브러리 무수정 재사용).** 본 Layer의 중립 코드는 `uahf/framework/loop/step-host/` 중립 모듈을 **라이브러리로 무수정 import**하여 단일 run 실행을 substrate로 위임한다. 이는 루트 §2.5 "상위만이 하위를 안다"의 **허용 방향**(상위 UAF 컴포넌트가 하위 UAHF를 안다)이며, **substrate 라이브러리 무수정 import는 UAF-INV ①(접점 원칙)과 병존**하므로(루트 §8 병존 주 — substrate 소비는 §2.5 하향 방향) 읽기·라이브러리 재사용은 위반이 아니다. `uahf/` 정본·코드는 무촉이며, 본 트랙의 `uahf/` 트리 접촉은 정확히 2건(§5·§6 — Adapter 물리 경계 동거 바인딩 신설 + OQ-SH-4 1개소, 전부 비Frozen 경계)뿐이다.

- **정본은 인용된 각 spec의 §3 계약이다.** 이 문서는 `uahf/specs/07-workflow.md`·`uahf/specs/02-agent.md`·`uahf/specs/03-loop.md`·`uahf/specs/06-verifier.md`의 계약과 `04-solution-design` §3.3·§3.4·§3.8·`03-project-contract` §3.4·§3.6의 계약을 **재정의·확장하지 않는다**. 이들은 정본 § 포인터로만 참조한다. 상류(`02-discovery`·`03-project-contract`·`04-solution-design`) 인용은 UAF 레벨 컴포넌트가 자신의 상류 파이프라인 산출물을 인수하는 **정상 방향**이다(루트 §2.5 — 상위가 하위·상류를 안다). 별도 방어적 정당화가 필요치 않다.

- **본 프로토콜이 새로 소유하는 계약 영역 (정직 구분).** 본 문서는 기존 계약을 재사용하는 데 더해 **다음 4종의 신규 계약 레코드를 직접 소유**한다. 이 4종은 기존 spec 어디에도 필드가 실재하지 않는 신규 소유물임을 정직하게 표기한다(설계 constraint 2 — "새 계약 요소 0" 주장을 복제하지 않는다. 이번엔 신규 계약이 실재한다).

  | 신규 소유 계약 | 소유 절 | 무엇을 새로 정의하는가 | 기존 계약과의 관계 |
  |---|---|---|---|
  | **RevisionEvent** | §3.2 | `revisionSeq`·`kind`·`payload`·`basis` — 진행 중 그래프 확장의 append-only 원장 항목 | `payload`는 `uahf/specs/07-workflow.md` §3.2-B Task 전 필드를 담는다(Task 계약 재정의 0). 레코드는 신규. |
  | **GatePolicyEntry** | §3.3 | `target`·`gateKind`(5종) — 단위 유형·전이·artifact class별 게이트 정책 데이터 | `gateKind`는 CP2·`uahf/specs/03-loop.md` §3.1-D·`uahf/specs/06-verifier.md` 등 기존 게이트 계약으로 매핑(§3.3 표). Entry 스키마는 신규. |
  | **AgentSpec 레코드** | §3.4 | `specId`·capability selector·brief 참조·기본 constraints·tool/model policy class·버전 — 실행 프로파일 | Role 자체는 `04-solution-design` §3.3 Expert Role 인용(재정의 0). AgentSpec은 그 위의 신규 실행 프로파일. |
  | **ArtifactRecord** | §3.6 | `artifactId`·`version`·`supersedes`·`derivedFrom`·`producedBy`·`approvalState`·`location`·`contentHash` — 산출물 계보·provenance | 완료 보고 `artifacts`(`uahf/specs/02-agent.md` §3.2-C)·게이트 이벤트에서 파생. 계보 불변은 `03-project-contract` §3.4·PC-INV 9 동형. 레코드는 신규. |

  **재사용과 신규 소유를 혼동하지 않는다.** Work Graph·Task·parallelSets·R1~R4·Merge, 이벤트 스키마·단계 상태 5종, 위임 8필드·완료 보고·4역할, verdict·VT, Expert Role·복잡도 판정·협업 State Machine, supersedes 계보는 전부 **재사용(재정의 0)**이다. 위 표 4종만 **본 Layer 신규 소유**다.

- **INV-3 무촉 (UAF 레벨 Layer 신설이되 UAHF 6-Layer 무촉).** `orchestration/`은 UAF 파이프라인 축의 **최상위 물리 Layer**이며, UAHF 6-Layer 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter, `uahf/specs/00-glossary.md` §3.2-A)의 지층(stratum)이 **아니다**(`entry/`·`discovery/`·`planning/` 동형·v1.1 선례 = UAF 레벨 신설·UAHF 무수정). 따라서 Glossary INV-3("Layer는 정확히 6개다")는 **무촉**이며, 본 문서는 UAHF Layer 수를 늘리거나 새 UAHF Component·spec을 창설하지 않는다. **새 상태 열거도 창설하지 않는다**(`uahf/specs/03-loop.md` §3.2-B 5종 재사용 — §4).

- **경계 불가침 — 두 번째 Runtime·두 번째 Step Host 아님.** 본 Layer는 Step Host를 라이브러리로 무수정 재사용하며 별도 실행 엔진을 신설하지 않는다. **단일 run의 무인 관리는 Step Host가 완결 소유**하고, 본 Layer는 그 위에서 **run/작업 단위 입도**로 프로젝트 lifecycle(그래프 진화·게이트·할당·계보)을 조율한다 — 디스패치 입도는 run/작업 단위이지 개별 step이 아니다.

- **이 문서는 Core 문서 관행을 따른다.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명·실행 옵션 문자열을 두지 않는다(`uahf/framework/core/structure.md` §5 C-3 동형). 직렬화 형식·물리 배치·게이트 큐 제시 채널·capability→물리 호출 매핑·정책 실값은 중립 모듈 경계·Adapter Binding 문서 소관이며, 필요한 자리에는 소관 포인터만 둔다(§5).

---

## §1. 목적

Project Orchestration 계약의 책임은 여섯 가지다.

- Project Orchestrator의 **위상**을 확정한다 — UAF 레벨 상위 컴포넌트로서 무엇을 조율하고 무엇을 판단하지 않는가, Step Host와의 관계(§2).
- **Project Work Graph**를 정의한다 — `uahf/specs/07-workflow.md` §3.2-A Work Graph 스키마의 상위 입도 무수정 재사용(§3.1).
- **Graph Revision Ledger**를 정의한다 — 진행 중 그래프 확장의 append-only 실현과 결정성 조건(§3.2).
- **Gate Policy·할당·모델·Artifact 계약**을 확정한다 — 5종 게이트 어휘와 단조성, Role/AgentSpec/Instance 할당, 모델 선택 정책, 산출물 계보(§3.3~§3.7).
- **불변 PO-INV 8건**을 확정한다 — 전부 기존 정본 불변의 파생(§4).
- **Adapter 바인딩 지점·무수정 경계**를 확정한다(§5·§6).

이 계약은 루트 `ARCHITECTURE.md` §11이 후속 트랙에 예약한 "Layer 연결·오케스트레이션 정식화"의 실현이며, **04-solution-design §3.9 확장 포인트 1·2의 실현**(04-solution-design 무수정 인용)이다. 자매 step-hosting-protocol이 확립한 형태 B 패턴(deterministic 구동자 + LLM 국소화 + append-only + 게이트 코드 강제)의 프로젝트 레벨 확장이되, UAHF 내부 편입이 아니라 UAHF를 substrate로 소비하는 UAF 레벨 컴포넌트다. 계약을 바꾸어야만 성립하는 위반이 발견되면 구현하지 않고 Advisor에게 보고한다(`uahf/framework/core/structure.md` §7 규칙 4 동형).

---

## §2. 위상 선언 — Project Orchestrator는 UAF 레벨 상위 컴포넌트이자 판단하지 않는 기계 구동자

Project Orchestrator는 **Discovery·Solution Design 산출물을 인수해 프로젝트 완료까지 lifecycle을 관리하고 UAHF를 execution substrate로 소비하는 UAF 레벨 상위 컴포넌트**다(루트 §2.3 Agentic Runtime slot 실현·§2.5 단방향 의존). 동시에 그 조율 방식은 **판단하지 않는 기계 구동자**다 — 프로젝트 단위의 스케줄·게이트 강제·재시도·재개·기록·정책 평가·revision 검증·artifact 인덱스를 deterministic하게 구동할 뿐, 의미 판단을 하지 않는다(step-hosting-protocol SH-INV-1 동형 → PO-INV 1).

### 2.1 "PM Agent"의 3분해 — 중앙 조율 LLM은 소멸한다

모든 것을 읽고 지시하는 상주 조율 LLM("God PM Agent")은 창설하지 않는다. "PM Agent"의 책임은 셋으로 분해되어 소멸한다(설계 §1).

| 책임 | 소유 주체 | 성격 |
|---|---|---|
| **기계적 조율** — 스케줄(ready_set)·게이트 강제·재시도·재개·기록·정책 평가·revision 검증·artifact 인덱스 | **Project Orchestrator** (중립 코드) | deterministic · 판단 0 (SH-INV-1 동형) |
| **의미 판단** — 설계 Proposal·분해 제안·역할 할당 제안·리뷰 판정·모호성 해소 | 국소 fresh-context **Step** (`uahf/specs/02-agent.md` §3.1 4역할 Lifecycle 의무 + `04-solution-design` §3.3 Expert Role capability) | LLM — 격리 번들 입력·요약 반환 (step-hosting-protocol §3.2) |
| **확정 권위** — Contract 확정·성숙 승인·실행 착수·중대 결정 | **사용자** (UAF-INV ⑤ — 루트 §8) | 게이트 큐 경유 |

**WBS(작업 분해) 소유 명확화 (재정의 아님 — 위 3분해·§3.4 2축 인용).** 위 "의미 판단" 축의 **분해/설계 proposal step은 Planner Lifecycle 역할로 수행**된다 — 초안 분해는 `uahf/specs/02-agent.md` §3.2-A Planner capability이며(§3.4 "4역할=Lifecycle 의무 축, Expert Role=capability 내용 축, 직교 병존"), 엔진(기계적 조율)이 그 위 스케줄·게이트·원장·계보를 관리하고(위 표 1행), 확정 impl 단위의 실행은 Worker다(엔진 디스패치 단일 단위). 즉 **관리=엔진 / 초안 분해=Planner / 실행=Worker**의 삼분이며, 셋 다 위 3분해·§3.4 병존 축의 파생이다(신규 계약·새 역할 창설 0). 이 삼분이 실현되는 2경로 — (a) Contract 소비 프로젝트: 엔진 컴파일러가 **Planner-role proposal step**을 디스패치해 분해 초안을 산출하고 게이트 통과 후 `task_added` revision으로 합성(§3.2 RevisionEvent) · (b) Advisor 직접 위임 층: Planner가 분해 초안을 작성(`uahf/specs/02-agent.md` §3.2-A). 어느 경로든 수용은 게이트 소유·확정 권위는 사용자다(위 표 3행·§3.2 결정성 ①).

### 2.2 headless·사용자 채널 분리·substrate 라이브러리 재사용

- **Orchestrator는 headless다.** 사용자 대화 주체와 Orchestrator를 분리한다. 사용자 채널은 (i) 진입/대화 세션(형태 A — Discovery Eliciting·게이트 제시)과 (ii) **게이트 큐**(`Escalated` 이벤트 + gateKind + scoped question의 파생 뷰)뿐이다. 게이트가 이벤트로 영속하므로 Orchestrator 크래시에도 대화·게이트 상태가 보존된다(SH-INV-2 동형 → PO-INV 2·3).
- **Step Host 라이브러리 무수정 재사용.** 본 Layer의 중립 코드는 Step Host 중립 모듈(`uahf/framework/loop/step-host/`)을 import하여 그 이벤트 로그·상태 파생·결정적 재개(step-hosting-protocol §4)를 재사용한다. revision 원장과 step 이벤트 로그는 같은 append-only 원칙 위의 **이중 원장**이며(§3.2·PO-INV 2), 별도 상태 시스템을 신설하지 않는다.
- **재정의 0.** Orchestrator는 Step Host 위상(step-hosting-protocol §2), Loop(`uahf/specs/03-loop.md`) 단계 전이, Workflow(`uahf/specs/07-workflow.md`) R1~R4·Merge를 재정의하지 않고 **구동만** 한다. 단일 run의 무인 관리는 Step Host가 완결 소유하며 재구현하지 않는다.

---

## §3. 아키텍처

이 절의 계약은 특정 AI·모델·언어·직렬화 형식에 의존하지 않는다. 모든 물리 실현은 §5에 둔다.

### §3.1 Project Work Graph — `uahf/specs/07-workflow.md` 스키마의 상위 입도 재사용 (새 실행 단위 계약 0)

- **Project Work Graph = `uahf/specs/07-workflow.md` §3.2-A Work Graph 스키마 그대로다.** 필드(`goal`·`tasks`·`dependencies`·`parallelSets`·`completion`)·Task 필드(§3.2-B)·병렬 집합 도출 규칙을 **무수정 재사용**한다. 새 실행 단위 계약을 창설하지 않는다.
- **차이는 Task의 입도뿐이다.** Task의 입도가 코드 구현만이 아니라 **프로젝트 작업 단위**(예: discovery unit·maturation unit·decompose unit·implementation step 집합·review unit)다. 각 단위는 자매 Step(`uahf/specs/07-workflow.md` §3.2-B Task + `uahf/specs/02-agent.md` §3.2-B 위임 8필드 + role/capability/model 슬롯 — step-hosting-protocol §3.1)으로 직렬화된다.
- **작업 단위 유형 = 개방 네임스페이스·데이터.** 코어는 작업 단위 유형 카탈로그를 **열거하지 않는다**(고정 파이프라인 하드코딩 금지 — `04-solution-design` §3.3 개방 네임스페이스·SP-INV 5 동형). 위 예시는 예시일 뿐이며 유형 카탈로그는 비정본 부록 소관이다(§5). 어떤 작업 단위가 필요한가는 데이터다.
- **초기 구성은 데이터다.** 프로젝트 그래프의 초기 구성은 Entry Resolution 결과 + 복잡도 판정(`04-solution-design` §3.2)의 데이터다 — 단순 프로젝트는 단일 Work Graph 직행, 복잡 프로젝트만 다단 단위 구성. 코어는 어느 쪽도 강제하지 않는다.

### §3.2 Graph Revision Ledger — 동적 그래프의 append-only 실현 (본 Layer 신규 소유)

`uahf/specs/07-workflow.md` Work Graph는 Decompose 1회의 정적 산출이다. 진행 중 그래프 확장(설계 후 구현 task 확정 등)은 **Graph Revision Ledger**로 실현한다.

**프레이밍 — revision은 `07-workflow` 재정의가 아니다.** Graph Revision은 `07-workflow` 계약의 변경이 아니라 "**신규 발견 작업에 대한 Decompose(`uahf/specs/07-workflow.md` §3.1-A) 반복 실행 산출의 append-only 합성**"이다. 각 revision epoch가 낳는 파생 그래프는 §3.2-A Work Graph 1건을 **온전히 만족**한다 — parallelSets 도출·소유 경계 비중첩·순환 0을 그대로 지킨다. `07-workflow` 문면 계약은 변경 0이다.

```
RevisionEvent {              // ── 본 Layer 신규 소유 레코드
  revisionSeq                // 전순서 (단조 증가)
  kind                       // task_added | dependency_added | task_superseded
  payload                    // uahf/specs/07-workflow.md §3.2-B Task 전 필드 (Task 계약 재정의 0)
  basis {                    // 근거 없는 그래프 변경 0 (PO-INV 5)
    proposingStepRef         //   이 revision을 제안한 LLM step 참조
    gateEventRef             //   이 revision을 수용한 게이트 통과 이벤트 참조
  }
}
현재 그래프 = fold(RevisionEvent 목록, 초기 그래프)   // 파생 뷰
```

- **append-only·파생 뷰 (PO-INV 2).** revision 원장 자체가 append-only이며, "현재 그래프"는 별도의 mutable 상태가 아니라 원장의 **fold 파생 뷰**다. `task_superseded`는 삭제가 아니라 **superseding 포인터 append**이며 과거 문면은 불변이다(`03-project-contract` §3.4·PC-INV 9 동형).

- **결정성 조건 3건 (계약 필수 조항 — PO-INV 3, SH-INV-3 확장).**

  | # | 조건 | 내용 |
  |---|---|---|
  | ① | **전순서** | `revisionSeq` + `basis.gateEventRef`로 인과 고정 — 게이트 통과 이벤트가 append된 뒤에만 그 revision을 append할 수 있다. 근거 없는 그래프 변경 0. |
  | ② | **안정 정렬** | Orchestrator는 (`revisionSeq`, `payload` 선언 순서)로 step 집합을 공급해 ready_set 순서 결정성을 보존한다(`uahf/specs/07-workflow.md` §3.2-A parallelSets 도출 논리 재사용). |
  | ③ | **검증의 결정성** | revision 수용 검증(스키마 완전성·순환 0·같은 병렬 집합 내 `ownedBoundary` 비중첩)은 **순수 함수**다. 실패는 **`uahf/specs/07-workflow.md` §3.1-A 사유 코드 재사용**(`MissingCompletionCriteria`·`MissingInterfaceContract`·`OwnershipOverlap`·`DependencyCycle`). 의미 수용 여부는 게이트 소유(판단 0 보존). |

- **미래 task 선참조 금지.** `dependsOn`은 미래 task를 선참조할 수 없다(`uahf/specs/07-workflow.md` §3.2-C R2 추측 금지). 따라서 "설계 후 구현 task 확정" 패턴은 자연히 다음 인과 사슬이 된다 — **설계 단위 `Passed` → 산출 artifact 기반 구현 task 제안(LLM step) → 게이트 → revision append**. 동시 작성 중인 미완성 산출물은 추측·인용하지 않고 확정된 `interfaceContract`만 참조한다(R2·R4).

### §3.3 Gate Policy — 5종 어휘·데이터·단조성 (본 Layer 신규 소유)

```
GatePolicyEntry {            // ── 본 Layer 신규 소유 레코드
  target                     // (단위 유형 | 전이 | artifact class)
  gateKind                   // auto_continue | review_required | approval_required
                             //   | escalation_required | user_decision_required
}
```

- **5종 어휘와 기존 계약 매핑** (설계 §3.3). gateKind는 신규 어휘이되, 각각은 **기존 게이트 계약으로 매핑**되며 새 판정 주체를 창설하지 않는다.

  | gateKind | 기존 계약 매핑 |
  |---|---|
  | `auto_continue` | 추가 게이트 0 — 단 **CP2는 불변 하한**(step-hosting-protocol SH-INV-4 "CP2 우회 없음"). |
  | `review_required` | **검증 통과 확증 요구** — 유효 CP2 evidence(`cp2-pass`) 소비로 해소하며, 해소 마커가 근거 `cp2-pass`를 명시 참조한다(provenance 사슬). 유효 evidence 부재·stale(재실행/retry · supersede/revision 영향 · 기록된 artifact 해시 불일치 또는 확인 불가) 또는 정책의 독립 2차 검증 요구(`requireIndependentReview`) 시 CP2 외 **추가** 독립 리뷰 단위 디스패치(Verifier 역할·`uahf/specs/06-verifier.md` §3.2-E VT-1~5 재사용). |
  | `approval_required` | 경계에서 **CP3**(Advisor **역할** 승인 — 사람 아님·무인 양립, `uahf/specs/02-agent.md` §3.1) 강제. |
  | `escalation_required` | `Escalated` 정지 — Advisor/사람 해소 이벤트로 재개(`uahf/specs/03-loop.md` §3.1-D). |
  | `user_decision_required` | `Escalated` 정지 — **사용자 응답 이벤트만** 해소 가능(사용자 확정 권위 보존 — `04-solution-design` §3.4 T8/T9/T10의 물리화·UAF-INV ⑤). |

- **게이트 단조성 (PO-INV 4).** 정책은 **코드 소유 하한**이다. 다음 지점의 하한 — CP2 상시(SH-INV-4)·`uahf/specs/03-loop.md` §3.1-D 조건 2~5·Contract Ready/Matured·실행 착수(`04-solution-design` §3.1-D Handoff)의 `user_decision_required` — 을 **약화할 수 없고 강화만** 할 수 있다. GatePolicyEntry는 하한을 올릴 수는 있어도 내릴 수 없다.

- **Autonomy Policy와 직교.** Gate Policy는 Autonomy Policy 3값(`interactive`/`auto_approve`/`unrestricted` — 도구 실행 승인 프롬프트 축, step-hosting-protocol §6.2)과 **직교**한다. `unrestricted`에서도 5종 게이트는 전부 작동하며 Human Decision Gate는 `Escalated` 정지로 보존된다(SH-INV-4 확장). 자율성 축은 도구 승인만 제어하고 게이트 축은 의미 판단·확정 권위를 제어한다 — 두 축은 섞이지 않는다.

### §3.4 할당 계약 — Role / AgentSpec / Instance 3층 (AgentSpec 신규 소유)

할당은 세 층으로 분해되며, `uahf/specs/02-agent.md` §3.2-A 4역할과 병존한다.

| 층 | 정의 | 소유 |
|---|---|---|
| **Role** (논리) | `04-solution-design` §3.3 Expert Role {roleId·capability·inputContract·outputContract} — 개방 네임스페이스·최소 할당(SP-INV 8). **인용(재정의 0).** | `04-solution-design` (무수정 인용) |
| **AgentSpec** (실행 프로파일) | {`specId`·capability selector·brief 템플릿 참조·기본 constraints·tool policy class·model policy class}의 **버전 있는 데이터 레코드**. capability 선언으로 검색·선택(Capability First). 물리 실현 예(하네스 역할 정의 등)에는 코어가 **불투명 참조**만 둔다. | **본 Layer 신규 소유 스키마** + 실값은 Adapter 레지스트리 데이터 |
| **Instance** (비영속) | 한 Step attempt의 fresh-context 1회 실행 {`runId`·`stepId`·`attempt`}. **비영속** — 정체성은 이벤트 로그에만 존재. 상주 인스턴스·chat history 공유 없음(step-hosting-protocol SH-INV-8 동형). | 이벤트 로그 파생 |

- **4역할과 병존.** `uahf/specs/02-agent.md` §3.2-A 4역할(Advisor/Planner/Worker/Verifier)은 **Lifecycle 의무 축**으로 병존한다. Expert Role은 그 위의 **capability 내용 축**이다 — 두 축은 대체가 아니라 직교 병존이다(`04-solution-design` §3.3 동형).
- **제안·수용·평가의 3분리.** 할당 근거 = Contract/SD 산출 · 복잡도 판정(`04-solution-design` §3.2) · capability 매칭 · 최소 할당(SP-INV 8). 이때 **할당 "제안"은 LLM step이 산출**하고, **수용은 게이트가 소유**하며, Orchestrator는 **매칭 정책의 deterministic 평가**만 수행한다. Orchestrator는 capability 선언까지만 소비하고 AgentSpec의 물리 매핑(어느 실행 주체가 호스팅하는가)은 해석하지 않는다(PO-INV 6, `04-solution-design` M5 폐쇄성 동형).

### §3.5 Model Selection — Model Selection Policy as Data

- **입력 축 (Policy as Data).** 모델 선택은 `capability class × cost/latency/quality 가중 × fallback 체인`으로 결속된다. "역할을 처리할 수 있는 가장 약한 모델" 티어는 **정책 기본값 형태**로 채택하되, **모델 고유명은 Adapter 정책 실값에만** 둔다(코어 본문 0 — C-3). 정책은 데이터이며 엔진·계약 무변경으로 조정된다.
- **직렬화 시점 1회 고정 (hysteresis).** 모델 선택은 Step 직렬화(revision append) 시점에 1회 결정·슬롯 기록된다. **재선택 트리거는 정확히 2건으로 한정**된다 — (a) retry 한도 도달 후 에스컬레이션 해소 시 (b) 명시적 정책 이벤트. 과도한 스위칭이 일관성·비용·context continuity를 해치는 것을 정책으로 억제한다.
- **CP2 Verifier 모델 = 독립 정책 행 (OQ-SH-4 해소 계약).** CP2 검증 단위의 모델은 대상 step의 모델 슬롯을 **상속하지 않고 독립 정책 참조**로 지정된다. 이로써 검증 단위가 피검증 단위와 동일 모델에 묶이지 않는다. 물리 구현(코드 심볼·상속 지점 수정·테스트 갱신)은 **S4 구현 단계·Step Host 코드 1개소 수정**(`uahf/` 트리 접촉 2건 중 하나·§5·§6)이며 본 문서는 계약과 소관 포인터만 둔다.
- **책임 경계.** **Model Router**(정책 평가 — 무엇을 쓸지, deterministic·중립)와 **Provider Adapter**(물리 전달 — 어떻게 호출할지)를 분리한다. 선택 결과는 artifact provenance(§3.6 `producedBy`)에 기록되되 **소비 조건으로 쓰지 않는다**(`04-solution-design` SP-INV 3 동형 — provenance 불투명).

### §3.6 Artifact Record·Registry — 파생 인덱스 (본 Layer 신규 소유·제2 진리원천 아님)

```
ArtifactRecord {             // ── 본 Layer 신규 소유 레코드
  artifactId                 // 논리 식별자
  version                    // append-only 인스턴스 버전
  supersedes                 // 직전 버전 참조 — 기존 문면 불변 (03-project-contract §3.4·PC-INV 9 동형)
  derivedFrom[]              // 입력 artifact 참조 (07-workflow interfaceContract consumes의 실측치)
  producedBy                 // provenance {runId·stepId·attempt·role·capability·model} — 불투명 부속
  approvalState              // draft → verified(CP2 Pass) → approved(CP3) → user_approved(사용자 게이트)
                             //   — mutable 필드가 아니라 게이트 이벤트의 파생 뷰
  location                   // 워크스페이스 물리 경로 (Adapter 소관)
  contentHash                // 선택 — 문면 불변 증빙
}
```

- **approvalState = 게이트 이벤트 파생 뷰 (PO-INV 7).** `approvalState`는 mutable 필드가 아니라 게이트 이벤트의 파생 뷰다 — `verified`는 CP2 Pass 이벤트, `approved`는 CP3 이벤트, `user_approved`는 사용자 게이트 해소 이벤트에서 파생된다. 상태를 직접 쓰지 않는다.
- **레지스트리 = 파생 인덱스 (제2 진리원천 아님).** Artifact Registry는 완료 보고(`uahf/specs/02-agent.md` §3.2-C `artifacts`)와 게이트 이벤트에서 파생되는 **인덱스**다. 별도의 진리원천이 아니다.
- **번들 확정 참조는 정책 등급 이상만 해석.** Fresh Context 번들의 "확정 참조"(step-hosting-protocol §3.2·`uahf/specs/07-workflow.md` §3.2-C R2)는 이 레지스트리에서 `approvalState`가 **정책이 요구하는 등급 이상**인 버전만 해석한다. 미완성·미승인 산출물은 추측·인용하지 않는다.
- **계보 append-only.** `supersedes`는 삭제가 아니라 계보 append이며 과거 버전 문면은 불변이다. Artifact는 파일 경로만이 아니라 임의 형태(문서·구조화 레코드·코드·이미지·test evidence·decision record 등)를 수용하되, 형태는 `location`+`contentHash` 뒤의 불투명 내용이다.

### §3.7 독립 실행 Agent 모델 — 특별 취급 0 (04-solution-design §3.9 확장 포인트 실현)

- **일반 모델의 대표 사례.** 설계 단위(Design Agent)는 특별 취급 0이며 일반 실행 모델의 대표 사례다 — 충분 입력(Contract 인스턴스 + 확정 artifact + 위임 8필드) → Sufficiency 판정(step-hosting-protocol §6.1 재사용) → headless 실행 → 산출 Artifact → 게이트 정책(§3.3)에 따른 리뷰·사용자 게이트 → 피드백 = 게이트 해소 이벤트 → **rework revision으로 재실행**. 실행 단위에 사용자와의 직접 대화 채널은 없다 — 대화형 단위(Discovery Eliciting류)는 규칙의 예외가 아니라 "사용자 채널에 위임되는 capability"로 정책 데이터에 선언된다.
- **`04-solution-design` §3.4 협업 프로토콜의 호스팅 (04-solution-design §3.9 확장 포인트 1·2 실현 — 04-solution-design 무수정).** `Assessing`/`Proposing`/`Reconciling`/`Reviewing`은 headless step으로, `Validating`(T8/T9/T10)은 `user_decision_required` 게이트로 물리화된다. 설계 충돌 조정 = `04-solution-design` §3.4 Reconciling(Conflict Detection + Trade-off Resolution)·Reviewing 그대로다.
- **실행 병렬 결과 충돌.** 병렬 실행 산출의 상호 참조 불일치·소유 경계 사후 충돌은 `uahf/specs/07-workflow.md` §3.2-D Merge 5단계로 처리하며, 중재자는 Advisor 역할이다(`uahf/specs/07-workflow.md` INV-6). 신설 0.

---

## §4. 불변 PO-INV 8건 (전부 기존 정본의 파생)

아래 8건은 이 Layer가 준수를 서약하는 Orchestrator 의무이며, **전부 기존 정본 불변의 파생**이다. 각 행에 모태 불변을 명시한다. 새 Core Contract·새 상태·새 UAHF Component를 창설하지 않는다.

| # | 이름 | 내용 | 모태 불변 |
|---|---|---|---|
| **PO-INV 1** | 판단 금지 상속 | 중립 Orchestrator는 의미 판단 0 — 완료/실패/차단/검증/승인은 전부 기존 주체 소유(§2). | step-hosting-protocol **SH-INV-1** 동형 |
| **PO-INV 2** | 이중 원장 append-only | revision 원장·step 이벤트 로그 모두 append-only, 현재 그래프·상태는 파생 뷰(§3.2). | **SH-INV-2** 확장 (`uahf/specs/03-loop.md` §3.2-A) |
| **PO-INV 3** | 결정적 재개 | 동일 (revision 원장, 이벤트 로그) 쌍 → 동일 그래프 → 동일 ready_set(§3.2 결정성 3조건). | **SH-INV-3** 확장 (`uahf/specs/07-workflow.md` §3.2-A) |
| **PO-INV 4** | 게이트 단조성 | 코드 소유 하한 약화 불가·강화만. Autonomy 축과 직교(§3.3). | **SH-INV-4** 확장 (`uahf/specs/03-loop.md` §3.1-D) |
| **PO-INV 5** | revision 근거 필수 | 모든 revision은 `basis.proposingStepRef` + `basis.gateEventRef`를 갖는다. 근거 없는 그래프 변경 0(§3.2). | `uahf/specs/07-workflow.md` §3.2-C R3·**SH-INV-4** 계열 |
| **PO-INV 6** | 역할 추상 유지 | 할당기는 Capability 선언까지만 소비, AgentSpec 해석·물리 매핑은 Adapter(§3.4). | `04-solution-design` **SP-INV 6** 동형 |
| **PO-INV 7** | artifact 계보 | append-only + supersedes, provenance 불투명(§3.6). | `03-project-contract` **PC-INV 9** · `04-solution-design` **SP-INV 3** 동형 |
| **PO-INV 8** | 중립성·격리 | 중립 코드에 provider/모델/업스트림 Layer 고유명 토큰 0, 상위 반환은 요약만(§2·§5). | `uahf/framework/core/structure.md` **C-3** 확장 · **SH-INV-8** 동형 |

---

## §5. Adapter·구현 바인딩 지점 (본 문서 미확정 — 소관 포인터)

아래 지점은 본 계약이 계약만 두고 값·물리 실현을 미루는 자리다. 정확한 값·형식·경로·매핑은 지정된 경계가 소유한다. 특정 AI·모델·제품 기능·언어·툴체인·직렬화 형식·실행 옵션 문자열은 전부 이 경계 뒤에만 등장한다(C-3).

| 바인딩 지점 | 소관 경계 |
|---|---|
| 중립 Orchestrator 모듈 배치(원장·파생·게이트 평가·할당 매칭·artifact 인덱스 + 스키마 + 테스트) | `orchestration/framework/orchestrator/` **신설**(`uahf/framework/core/structure.md` §4 C-2 동형 규칙 — `uahf/framework/loop/step-host/` 중립 모듈 **라이브러리 무수정 import**). provider·언어·옵션 토큰 0 유지. |
| RevisionEvent·GatePolicyEntry·AgentSpec·ArtifactRecord 직렬화 형식 | Adapter Binding 문서 소관(직렬화 형식명은 정본에 0). |
| Adapter 물리 바인딩·게이트 큐 제시 채널·run 데이터 백엔드 경로 | `orchestration/adapters/<adapter>/project-orchestration-binding.md` **신설**(UAF 레벨 바인딩 5종째를 Adapter 물리 경계에 동거 — contract/entry/discovery/solution-design-binding 선례·`uahf/` 트리 접촉 2건 중 하나). dogfooding run 데이터 = `uahf/framework/adapters/<adapter>/orchestration-data/`(discovery-data·solution-design-data 선례 동거). |
| capability → 물리 호출 매핑·AgentSpec 실값 레지스트리 | Adapter Binding·정책 데이터 소관(PO-INV 6 — 코어는 capability 선언까지만). |
| Model Selection 정책 실값·CP2 모델 독립 지정의 물리 구현 | Model Router 정책 데이터 + Provider Adapter 소관. CP2 모델 독립 지정(OQ-SH-4 해소)의 코드 수정·테스트 갱신은 **S4 구현 단계·Step Host 코드 1개소**(`uahf/` 트리 접촉 2건 중 하나 — §3.5·§6). |
| Autonomy Policy 실값·provider 실행 옵션 매핑 | Adapter/정책 데이터 소관(step-hosting-protocol §6.2 — 실행 옵션 문자열은 해당 바인딩에만 등장). |
| 작업 단위 유형·조율 역할 예시 카탈로그 | 비정본 부록 소관(코어 밖 — `04-solution-design` SP-INV 5 동형). |

non-core 실행 경계 사이의 정확한 분할은 `uahf/framework/core/structure.md` §4 규칙 4가 "형태 B 설계 시 확정"으로 미룬 자리이며, 위 표가 그 프로젝트 오케스트레이션 축의 확정분이다.

---

## §6. 실측 대조·무수정 경계

본 문서(S1 r2)는 **계약만** 확정하며 실행 코드·데이터를 생성하지 않는다(자매 step-hosting-protocol W1 동형·L-07). §5가 가리키는 산출물의 실측 상태와 무수정 경계는 다음과 같다.

- **미존재를 실재로 쓰지 않는다(L-07).** §5의 중립 Orchestrator 모듈(`orchestration/framework/orchestrator/`)·직렬화·바인딩·run 데이터 백엔드·CP2 모델 독립 지정의 코드는 **현 시점 미존재**다. 후속 구현 단계(S2~S5)에서 생성 예정이며, 그때 provider·언어 토큰 0(전수 스캔)이 CP2 검증 대상이 된다(설계 §5).
- **무수정 경계.** 본 문서는 다음을 무수정으로 둔다 — `uahf/specs` 00~13 Frozen(07/02/03/06 포함)·`04-solution-design`·`03-project-contract`·루트 `ARCHITECTURE.md`·step-hosting-protocol 본문·`uahf/framework/loop/step-host/`(OQ-SH-4 1개소 제외)·기존 Adapter 바인딩 본문·append-only 데이터. 전부 § 포인터 인용·라이브러리 무수정 import만이다.
- **`uahf/` 트리 접촉은 정확히 2건.** (i) `uahf/framework/adapters/<adapter>/project-orchestration-binding.md` + `orchestration-data/` 신설(Adapter 물리 경계 동거 — UAF 레벨 바인딩 선례 4건 동형). (ii) Step Host 코드 1개소(CP2 검증 단위 모델 상속 지점) — CP2 Verifier 모델 독립 지정(OQ-SH-4 해소·S4·테스트 갱신 동반). 그 외 정본·중립 코드는 전부 `orchestration/` 신규 Layer 소유다. substrate 라이브러리 무수정 import는 UAF-INV ①(접점 원칙)과 병존하며(루트 §8 병존 주), 이 2건은 모두 비Frozen 경계의 신설·명시 변경이다.
- **트랙 종단 별도 결정(선전제 금지).** 루트 라우터 등재(`orchestration/` 1행 — 루트 문서버전 상승·사용자 게이트)·step-hosting-protocol §9 이력 append·Contract 성숙 재발행은 트랙 종단 별도 결정이다. 배치·프레이밍 자체는 2026-07-13 사용자 결정으로 해소되었다.
- **자기 무촉 확인.** 본 문서(및 자매 `orchestration/ARCHITECTURE.md`·`orchestration/ROADMAP.md`)의 신설이 기존 정본을 변경하지 않음은 형상 관리 상태 조회로 확인한다(CP1 자체 점검·CP2 독립 판정 대상).

---

## §7. 요약 (한눈에 보기)

- **Project Orchestrator = UAF 레벨 상위 컴포넌트 + 판단하지 않는 기계 구동자.** Discovery·Solution Design 산출물을 인수해 프로젝트 완료까지 lifecycle을 관리하고 UAHF를 execution substrate로 소비한다(루트 §2.3 Agentic Runtime slot 실현·§2.5 허용 방향). Step Host를 **라이브러리로 무수정 import**하며 두 번째 Runtime·두 번째 Step Host가 아니다. 단일 run 무인 관리는 Step Host 소관, 본 Layer는 run/작업 단위 입도로 조율한다. "PM Agent"는 기계 조율·의미 판단·확정 권위로 3분해되어 소멸한다(§2).
- **`orchestration/`은 UAF 레벨 신규 Layer**(entry/discovery/planning 동형·v1.1 선례)이며 UAHF 6-Layer 무촉(Glossary INV-3 무촉). 새 UAHF Component·spec·상태 열거 창설 0(§0).
- **UAHF 관계 = substrate 라이브러리 무수정 소비.** `uahf/` 트리 접촉은 정확히 2건(바인딩 신설·OQ-SH-4 1개소)뿐이며 substrate 소비로서 UAF-INV ①(접점 원칙)과 병존한다(루트 §8·§0·§6).
- **본 Layer가 새로 소유하는 계약 4종** — RevisionEvent(§3.2)·GatePolicyEntry(§3.3)·AgentSpec(§3.4)·ArtifactRecord(§3.6). 기존 계약(Work Graph·Task·이벤트·상태 5종·위임·verdict·Expert Role·supersedes 계보)은 전부 재사용(재정의 0)이다(§0).
- **Graph Revision Ledger** = Decompose 반복 실행 산출의 append-only 합성. fold 파생 뷰·결정성 3조건·`task_superseded` 문면 불변 포인터 append(§3.2). **Gate Policy** = 5종 어휘·기존 계약 매핑·게이트 단조성·Autonomy 직교(§3.3). **할당** = Role/AgentSpec/Instance 3층 + 4역할 병존(§3.4). **Model Selection** = Policy as Data·hysteresis·CP2 모델 독립(OQ-SH-4)(§3.5). **Artifact Record** = append-only 계보·approvalState 파생 뷰·레지스트리 파생 인덱스(§3.6).
- **PO-INV 8건은 전부 기존 정본(SH-INV/SP-INV/PC-INV/C-3)의 파생**이며 새 Core Contract 0이다(§4). 값·물리 실현은 `orchestration/framework/orchestrator/`·Adapter Binding 소관이고 현재 미존재(S2~S5 예정)다(§5·§6).
- 본문에 특정 AI·모델·제품 기능·언어·툴체인·직렬화 형식·실행 옵션 토큰은 0건이다(C-3). 본 Layer는 루트 §11 "Layer 연결·오케스트레이션 정식화"와 `04-solution-design` §3.9 확장 포인트 1·2의 실현이다.
