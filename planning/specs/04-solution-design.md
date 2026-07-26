# planning/specs/04-solution-design — Solution Design Specification

작성일: 2026-07-13
상태: v1.3 Baseline → DC-1 Draft (Wave 1 [04]: CP2 Pass·Advisor CP3 승인 2026-07-18 — 트랙 진행 중) (기준선 = v1.3 Baseline[CP2 Pass — W1 재검증·W2 교차 8/8 · CP3 승인 · 사용자 Baseline 승인 2026-07-13]; 설계완성도 강제 트랙 §DC-1 개정 진행 중 — 버전 라벨/Baseline 승격은 트랙 완료·사용자 승인 소관) · v1.4 개정(done 12 관행 규격의 개정 기록 locus 를 git 으로 이전 — 사용자 결정 2026-07-27)
상위 규약: AGENT.md (INV-1)
근거 정본:

- `docs/v1.3-context-and-design.md@cd9247b` — v1.3 마일스톤 설계 정본(W0). 본 문서의 **고정 입력**이다. 특히 §2(채택 아키텍처 — planning/ 이중 책임)·§3(결정 D1~D10·필수 수정 M1~M6)·§4(선행 확정 인터페이스 — 단계 정의·입출력 추상·신규 용어 4건·경계 기준 문안·SP-INV 축 8). 계약 정본은 이 문서가 아니라 각 spec이 소유한다(재정의 0 — 충돌 시 spec 우선, Advisor 보고).
- `planning/specs/03-project-contract.md` — Project Contract **상세 계약 정본**(v1.1 Baseline). 논리 스키마·필수 코어 필드·버저닝·인스턴스 거버넌스·불변 PC-INV의 소유 정본이다. 특히 §3.1(Interface)·§3.2-B(필수 코어 필드)·§3.4(인스턴스 거버넌스 — append-only·supersedes)·§3.6(PC-INV 1~12). **본 문서는 03을 재정의·확장하지 않고 § 포인터로만 참조한다.**
- `discovery/specs/02-discovery.md` — Project Discovery 정본(v1.1 Baseline). 본 문서 입력의 상류다. 특히 §3.3(State Machine·종단 5)·§3.7(Execution Ready 2축 판정)·§3.10(Strategy Provider Interface — 방법론 격리 패턴)·§3.11(Discovery Dimension·Architecture 차원 — 경계 대조 대상). **본 문서는 02를 무수정으로 일방 참조한다.**
- `ARCHITECTURE.md` (루트, v1.3 — 라우터) — UAF 상위 구조 정본. 특히 §2.2(6요소 파이프라인·Contract 이중 지위)·§2.5(의존 방향 단방향·폐쇄성)·§8(UAF-INV ①~⑥)·§10(책임 경계표 — 비담당② 구현 Planning)·§12(용어 네임스페이스). § 포인터로만 참조·재정의 0.
- `planning/ARCHITECTURE.md` — 소유 Layer 개관 정본. 특히 §0(C2 네임스페이스 구분)·§7(정본 포인터 표). planning/ Layer의 **성숙 활동 측** 정본이 본 문서다(개관 정합은 후속).
- `uahf/specs/00-glossary.md` 0.2 — UAHF 용어 정본. 네임스페이스 분리의 대조 기준. § 포인터로만 참조.
- `uahf/specs/TEMPLATE.md` 0.1 — spec 문서 구조(§0~§9)·품질 기준 관행.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본 배치 (성숙 활동 측).** 이 문서는 **planning/ Layer의 Solution Design 단계 정본**이다. planning/ Layer는 W0(모델 P·D2)로 **이중 책임**을 갖는다 — (i) Project Contract 스키마 소유(정본 = `planning/specs/03-project-contract.md`) · (ii) **Solution Design 성숙 활동 소유(본 문서)**.

- **C2 — 3항 네임스페이스 구분 (핵심 경계).** planning/ 문맥에서 다음 셋을 혼동하지 않는다.
  - ① **Contract 설계** — Project Contract의 지위·논리 스키마·버저닝(정본: 03). "무엇을 계약으로 고정하는가."
  - ② **Solution Design** — Ready 인스턴스를 실행 가능한 솔루션 설계로 성숙시키는 UAF 레벨 활동(**본 문서**). "미결을 어떻게 해소하고 신규 설계 결정을 창출하는가."
  - ③ **UAHF 구현 Planning** — 확정 작업의 구현 계획·작업 분해·병렬 디스패치(UAHF Advisor/Planner·Workflow 소관, 루트 §10 비담당②③). "확정된 것을 어떻게 구현 분해·실행하는가."
  - 정식 명칭은 **Solution Design**이다 — 이 단계를 "Planning" 계열 명칭으로 표기하지 않는다("Planning"의 3중 의미[①·②·③] 충돌 회피·C2 보전, D1). ②는 ①·③과 다른 네임스페이스이며, ③은 § 포인터로만 가른다(루트 §10).

- **파이프라인 위상 = 6요소 유지 (D2·M6).** Solution Design은 파이프라인에 **새 요소를 추가하지 않는다**. 이것은 Project Contract 요소 **내부의 성숙 루프**다 — Ready 인스턴스 vN을 입력으로 superseding v(N+1)을 재발행한다. 루트 §2.2의 6요소 파이프라인 위상은 불변이며, 본 문서는 요소 수·순서를 바꾸지 않는다.

- **신규 용어 4건 (작업 정의 — 정식 등재는 루트 §12.1 후속).** 본 문서가 사용하는 신규 용어의 작업 정의는 다음과 같다. 정식 등재 지점은 루트 `ARCHITECTURE.md` §12.1이며 등재는 후속 소관이다(W0 §4.3).
  - **Solution Design** — Ready 종단 Contract 인스턴스를 입력으로, 프로젝트 복잡도에 따라 동적으로 구성된 전문가 역할 협업으로 솔루션 설계 결정을 성숙시켜, 사용자 승인 하에 superseding Contract 인스턴스를 재발행하는 UAF 레벨 활동. 소유 = planning/.
  - **Expert Role** — Solution Design에서 Capability 선언으로 정의되는 **논리 역할**. 고정 Agent Class가 아니며 **개방 네임스페이스**다. 프로젝트 특성·복잡도에 따라 최소 필요 역할만 동적 구성된다. 실행 주체 매핑은 Adapter 소관이다(코어는 역할 추상까지 — M5).
  - **Projection** — Project Contract를 Source of Truth로 하여 파생 생성되는 프로젝트별 산출 문서. 대상 프로젝트 워크스페이스에 귀속되며, 유형 목록은 개방 레지스트리(비정본 부록)다.
  - **Contract Maturation(성숙)** — Ready 인스턴스 vN을 기준선으로 새 설계 결정을 반영한 v(N+1)을 supersedes 계보로 재발행하는 것. 단일 문서의 상태 변경이 아니라 **완결 인스턴스의 재발행**이다(03 §3.4 정합).
  - **어휘 주의.** 통칭 "Draft Contract"/"Final Contract"는 **비정본 사용자 어휘**다 — 정본 표기는 "Ready 인스턴스 vN"/"superseding 성숙 인스턴스 v(N+1)"이다(M2·D5).

- **UAF·UAHF 상위 정본 § 포인터 참조 (재정의·확장 0) · INV-3 무촉.** 본 문서는 UAF 상위 구조(루트 `ARCHITECTURE.md`)·자매 정본(02·03·`planning/ARCHITECTURE.md`)·UAHF 정본(`uahf/`·상위 규약)을 **재정의·확장하지 않고 § 포인터로만 참조**하며, Contract 스키마·PC-INV·UAHF 연산/필드/불변을 신설·변경하지 않는다(UAF-INV ① 접점 원칙). "planning Layer"의 "Layer"는 UAHF 6-Layer 스택(`uahf/specs/00-glossary.md` §3.2-A)의 지층이 아니라 UAF 파이프라인 요소를 소유하는 최상위 물리 Layer 명칭이므로(루트 §0·§2.4), Glossary INV-3("Layer는 정확히 6개다")는 무촉이다.

- **AI 비의존.** 본문 전체(특히 §3 Core Contract)에 특정 AI 이름·모델명·제품 기능명·방법론 고유명·고정 역할 카탈로그를 두지 않고(루트 §0·03 §0 동형), 구체 실현(실행 호스팅·게이트 제시 채널·저장 위치·Policy 실값)은 Adapter Binding 소관 포인터로만 가리킨다(§4).

---

## §1. 목적 (Purpose)

이 문서는 **Discovery 이후·UAHF 이전에, Ready 종단 Contract 인스턴스를 실행 가능한 Solution Design으로 어떻게 성숙시키는가**의 상세 계약을 확정한다. 책임은 다섯 가지다 — (i) **단계 계약**(입력·출력 2경로·완료·실패) 확정(§3.1), (ii) **복잡도 판정**과 스킵 게이트를 Policy as Data로 확정(§3.2), (iii) **역할 할당 계약**(Expert Role·Capability 선언·개방 네임스페이스·최소 할당)과 **협업 설계 프로토콜** 골격 확정(§3.3·§3.4), (iv) **Projection**(Contract = Source of Truth·파생 산출)과 **경계 기준**(vs Discovery) 확정(§3.5·§3.6), (v) 저장 스코프 원칙과 불변 **SP-INV** 확정(§3.7·§3.8).

### 본 문서가 실현하는 정본 결정

- **P3·UAF-INV ①② (루트 §7·§8).** 성숙은 Contract 스키마(Public API)를 흔들지 않는다 — 성숙 산출은 03 스키마를 타깃으로 하는 새 인스턴스이며(필드 추가 없음, D4), 성숙 실행 내부 개념은 코어로 새지 않는다(§3.8 SP-INV 2·3).
- **UAF-INV ⑤ (루트 §8).** 성숙·스킵 두 종단 모두 사용자 승인 게이트를 통과한다(§3.1·§3.4, D6).
- **UAF-INV ⑥ (루트 §8).** 코어는 특정 설계 방법론·역할 카탈로그를 알지 않는다 — 방법론·역할·Projection 유형 카탈로그는 Provider·비정본 부록만 안다(§3.3·§3.5·§3.8 SP-INV 5, D9).

### Non-Goals

- **Contract 스키마 재정의 제외.** 필드·필수 코어 필드·PC-INV·버저닝은 03 소관이다. 본 문서는 성숙 입출력을 03 스키마의 **인스턴스**로 다루며 스키마를 확장하지 않는다(D4).
- **Discovery 내부 설계 제외.** State Machine·Strategy·Confidence·Question Budget은 02 소관이다. 본 문서는 Discovery의 **종단 산출**(Ready 인스턴스)만 소비한다.
- **UAHF 계약 변경 제외.** UAHF 연산·필드·불변을 추가·변경하지 않는다. 역할 추상까지만 정의하고 UAHF Agent·특정 하네스 개념을 역참조하지 않는다(M5·UAF-INV ①).
- **설계 기법·역할 카탈로그·Projection 유형 카탈로그 비정의.** 이들은 **비정본 부록**(`planning/docs/appendix/`) 소관이며, 본 문서는 프로세스 골격만 정본으로 두고 그 소유 지점을 § 포인터로 표기한다(M3·D9).
- **실행 호스팅·물리 저장 비설계.** 실행 주체 호스팅·산출물 물리 배치·직렬화는 Adapter 소관이다(§4).
- **실행 코드 0 (형태 A).** 본 문서는 설계 계약만 확정한다. Adapter Binding 물리화·dogfooding E2E는 **v1.4 이월**이다(D8).

---

## §2. Position

- **아키텍처 상 위치.** UAF 파이프라인의 **Project Contract 요소 내부의 성숙 활동**이다(루트 §2.2, D2). UAHF 6-Layer 스택의 지층이 아니라 그 외부·상류의 UAF 레벨 활동이며(루트 §2.4), planning/ Layer가 소유한다. Discovery의 Ready 산출을 입력받아 superseding 인스턴스를 산출한 지점에서 멈춘다(하류 UAHF 실행은 비담당).

- **의존하는 정본 (읽기 전 이해 필요).**
  - `docs/v1.3-context-and-design.md@cd9247b` (W0 확정·산출물 수명 정책에 따라 아카이브) — 마일스톤 설계 정본·고정 입력. §2·§3·§4.
  - `planning/specs/03-project-contract.md` (실재, v1.1 Baseline) — Contract 상세 계약. 성숙 입출력이 소비·산출하는 스키마·인스턴스 거버넌스. §3.1·§3.2-B·§3.4·§3.6.
  - `discovery/specs/02-discovery.md` (실재, v1.1 Baseline) — Discovery 종단(입력 상류)·경계 대조. §3.3·§3.7·§3.10·§3.11.
  - `ARCHITECTURE.md` (루트, 실재, v1.3) — UAF 구조·의존 방향·불변·책임 경계·용어. §2.2·§2.5·§8·§10·§12.
  - `planning/ARCHITECTURE.md` (실재, v1.3 정합) — 소유 Layer 개관·C2. §0·§7.
  - `uahf/specs/00-glossary.md` (실재, Frozen 0.2)·`uahf/specs/TEMPLATE.md` (실재, Frozen 0.1) — 용어 네임스페이스·문서 구조.

- **이 문서에 의존하는 문서 (dependents).**
  - `planning/docs/appendix/` 비정본 부록(실재) — 설계 기법·역할 카탈로그·Projection 유형 레지스트리. 본 문서가 개방 네임스페이스·개방 레지스트리를 정의함으로써 그 격리 지점이 성립한다(§3.3·§3.5·§3.10-D 선례 동형).
  - `planning/specs/03-project-contract.md` v1.2 Baseline(실재 — 2026-07-13 승인) — 생산자 문면에 성숙 주체 등재·인스턴스 갱신 유형에 Maturation 추가가 반영되었다(03 §3.1-B·§3.4). 본 문서는 03을 § 포인터로만 참조하며 03 스키마를 확장하지 않는다(무촉).

- **순환 의존 없음.** 의존은 본 문서 → 루트 `ARCHITECTURE.md`·03·02 방향이다. 성숙 활동은 하류 요소(UAHF·Execution)나 Discovery 내부 개념을 역참조하지 않는다(루트 §2.5, §3.8 SP-INV 6).

---

## §3. Core Contract (AI 비의존)

이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다. 모든 환경 의존 실현은 §4에 둔다.

### 3.1 단계 계약 (Interface)

#### 3.1-A 단계 정의 (한 문장)

Solution Design은 **Ready 종단 Contract 인스턴스를 입력으로, 프로젝트 복잡도에 따라 동적으로 구성된 전문가 역할 협업으로 솔루션 설계 결정을 성숙시켜, 사용자 승인 하에 superseding Contract 인스턴스를 재발행하는 UAF 레벨 활동**이다(W0 §4.1). UAHF 구현 Planning과 별개 네임스페이스다(§0 C2).

#### 3.1-B 입력

- **입력 = Ready 또는 ReadyWithAssumptions 종단의 Project Contract 인스턴스 vN** (+ 선택: 대상 워크스페이스 증거). `Ready`·`ReadyWithAssumptions`는 Discovery의 종단 상태이며 완전한 Contract를 산출한다(02 §3.3-A 종단 5·§3.7).
- **비Ready 입력 금지.** 비Ready 종단(`Suspended`·`Escalated`·`Aborted`)은 Contract를 산출하지 않으므로(02 §3.3-A) 성숙의 입력이 될 수 없다. Ready 종단이 아닌 인스턴스는 성숙되지 않는다(§3.8 SP-INV 1).
- **가정 해소 여지.** `ReadyWithAssumptions` 인스턴스는 Assumption Ledger(03 §3.2-A 그룹 7)에 미해결 가정을 담는다. 성숙은 이 가정과 Architecture Direction의 미결(03 §3.2-A 그룹 6)을 새 설계 결정으로 해소할 수 있으며, 해소 결과는 superseding v(N+1)에 반영된다(§3.6 경계 기준). 다만 두 Ready 종단 모두 동등하게 유효 입력이며, 가정 해소는 성숙의 **결과**이지 입력 전제가 아니다.

#### 3.1-C 출력 (두 경로 — 둘 다 사용자 게이트 통과)

| 경로 | 산출 | 사용자 게이트 |
|---|---|---|
| **성숙 경로** | superseding Contract 인스턴스 v(N+1)(supersedes = vN·append-only·vN 문면 불변 — 03 §3.4) + 선택된 Projection 산출 목록(§3.5). 대상 프로젝트 워크스페이스 귀속(§3.7). | 사용자 승인(§3.4 T8) |
| **스킵 경로** | **무산출** — vN이 곧 UAHF 소비 대상이다. 스킵 판정 기록(§3.2)만 남긴다. | 경량 사용자 확인(§3.4 T9, D6) |

- 두 경로 모두 사용자 게이트를 통과한다(UAF-INV ⑤ 동형·스킵 포함 D6). 게이트 없는 종단은 없다(§3.8 SP-INV 4).
- 성숙 경로의 superseding 인스턴스는 **03 스키마의 인스턴스**다 — 새 필드·새 스키마 버전을 요구하지 않는다(D4). 성숙은 03 §3.4 supersedes 계보 메커니즘으로 표현된다.

#### 3.1-D 완료 조건·실패 보고

- **완료 조건.** 협업 프로토콜(§3.4)이 종단(`Matured`·`Skipped`)에 이르고, 종단이 사용자 게이트를 통과했을 때 단계가 완료된다. `Matured`는 단일 일관 superseding 인스턴스(+선택 Projection)를 남긴다.
- **실패·에스컬레이션.** 자율 수렴 불가(잔여 충돌 미해소·의존 계약 미확정·권위 충돌)나 사용자 강제 시 `Escalated`로 종단하여 상위(사람) 판단에 위임한다(§3.4 T11). 추측으로 우회하지 않는다.
- **Handoff 의미론 (기존 메커니즘 재사용 — 별도 상태기계 없음).** `Matured`·`Skipped` 종단 이후 UAHF 착수 시점·여부는 **사용자 소관**이다 — Contract는 UAHF의 **선택 입력**(03 §3.5-A)이므로 종단이 실행을 즉시 강제하지 않으며, 보류(defer) 시 Ready 인스턴스가 파일로 존속해 소비 대기한다. 수정 재진입은 T10, 중단·상위 위임은 T11이 담당한다(§3.4-B). 본 문서는 Execution Decision을 위한 별도 상태기계·게이트를 신설하지 않는다.

### 3.2 복잡도 판정 (Complexity Assessment — Policy as Data)

- **판정의 형태만 정본.** 본 문서는 복잡도 **판정 계약의 형태**만 확정한다 — 판정은 입력 Contract vN(및 워크스페이스 증거)을 근거로 **성숙 필요** 또는 **스킵**을 산출한다. 구체 판정 기준(임계·가중·규칙)은 엔진에 하드코딩되지 않고 **정책 데이터**다(Policy as Data — 루트 §6 원칙 8, 02 §3.15 선례 동형). 정책 값의 데이터 소스·직렬화는 Adapter 소관이다(§4).
- **판정 계약의 형태.** 판정은 다음으로 결속된다. 산출은 이진 분기(성숙 필요 / 스킵)이며 판정 기준 자체는 담지 않는다.

  | 항목 | 계약 |
  |---|---|
  | 입력 | Ready 인스턴스 vN + (선택) 대상 워크스페이스 증거 |
  | 판정 기준 | 정책 데이터(임계·가중·규칙) — 코어에 하드코딩 0(Policy as Data) |
  | 산출 | `성숙 필요`(→ 역할 할당·§3.3) 또는 `스킵`(→ 경량 확인·§3.4 T9) + 판정 근거 기록 |

- **스킵 게이트 (D6).** 판정이 "스킵"이면 성숙을 수행하지 않고 vN을 그대로 UAHF 소비 대상으로 둔다. 다만 스킵도 **경량 사용자 확인**을 거친다(§3.4 T9). 스킵 판정과 그 근거는 기록으로 남긴다(무산출이되 판정 기록은 남는다).
- **경계.** 복잡도 판정 자체는 성숙 실행 메타이며 Contract 코어 필드로 유입되지 않는다(§3.8 SP-INV 2·3). 판정 기준 카탈로그·기법은 비정본 부록 소관이다(§3.8 SP-INV 5).

### 3.3 역할 할당 계약 (Expert Role Allocation)

- **Expert Role = Capability 선언 기반 논리 역할.** 역할은 고정 열거가 아니라 **Capability 선언**으로 정의·선택된다(Capability First — 루트 §6 원칙 7, 02 §3.10-A 선례 동형). 하나의 역할은 "어느 설계 관심사에 대해 설계 결정을 끌어올릴 수 있는가"를 선언한다.
- **Capability 선언 형태.** 하나의 Expert Role은 다음을 선언한다 — 고정 역할명 없이 논리 선언만이며, 선언 항목의 형태는 모든 역할에서 불변이다(02 §3.10-A·B 선언 패턴 동형).

  | 선언 항목 | 정의 |
  |---|---|
  | `roleId` | Expert Role의 논리 식별자(개방 네임스페이스 — 구체 역할명 카탈로그는 코어 밖). |
  | `capability` | 이 역할이 **어느 설계 관심사에 대해 설계 결정을 끌어올릴 수 있는가**의 선언. 할당기는 이 선언으로 최소 역할을 선택한다. |
  | `inputContract` | 입력 — 입력 인스턴스 vN·현재 결정 집합·잔여 미결. |
  | `outputContract` | 출력 — 담당 관심사의 설계 Proposal(§3.4-D ①). |

  역할이 바꾸는 것은 `capability`와 Proposal의 성격뿐이며, 협업 프로토콜(§3.4)·SP-INV·산출 인스턴스 스키마는 어느 역할 구성에서도 불변이다.
- **개방 네임스페이스·고정 열거 0.** 역할명은 **개방 네임스페이스**다. 본 코어는 구체 역할명 카탈로그를 열거하지 **않는다**(고정 팀 열거 0). 신규 역할은 코어·엔진 변경 없이 선언 등록만으로 참여한다. 구체 역할 예시가 필요하면 **비정본 부록**(`planning/docs/appendix/`, 실재) 소관이다(§3.8 SP-INV 5, D9).
- **최소 할당 원칙.** 프로젝트 특성·복잡도가 요구하는 **필요 역할만** 할당한다. 불필요한 다중 역할 구성을 강제하지 않는다 — 불필요한 Multi-Agent 비용을 방지한다(§3.8 SP-INV 8).
- **전체 범위 커버리지 바닥.** 패널은 선언된 **전체 프로젝트 범위를 관장하는 커버리지 capability를 반드시 포함한다** — 좁은 관심사 역할들의 합으로 전체 설계 완성도를 대체하지 않는다. 이 커버리지 capability는 최소 할당(SP-INV 8)의 예외가 아니라 그 위의 **필수 바닥**이며, 전문 역할은 그와 별개로 최소 할당·상한 정책을 따른다. 두 원칙은 층위가 다르다 — 최소 할당은 각 좁은 관심사에 대해 **필요 이상으로 전문 역할을 늘리지 않음**을 규율하고, 커버리지 바닥은 그와 독립적으로 **선언 범위 전체가 관장 없이 비는 일이 없음**을 규율한다(모순 아님). 이 바닥은 개방 네임스페이스를 닫지 않는다 — 커버리지 capability도 고정 역할명이 아니라 Capability 선언으로 표현되며, 구체 역할명·상한 실값은 Policy·비정본 부록 소관이다(SP-INV 5). 성숙 경로에서 이 커버리지가 선언 범위를 어떻게 필수 세트로 결착시키는지는 §3.8 SP-INV 9가 규율한다.
- **실행 주체 매핑은 Adapter 소관 (M5·폐쇄성).** 논리 Expert Role을 어느 실행 주체가 호스팅하는가는 코어가 정의하지 않는다 — **코어는 역할 추상까지만**이다. UAHF Agent·특정 하네스 개념을 역참조하지 않는다(루트 §2.5, §3.8 SP-INV 6). 물리 호스팅은 §4·확장 포인트(§3.9).

### 3.4 협업 설계 프로토콜 (Collaborative Design Protocol — 골격)

협업 설계는 **단일 정본 State Machine**의 골격으로 정의된다. 상태 수는 절제하되 종단/비종단 구분과 사용자 게이트를 엄밀히 명시한다(02 §3.3 관행 동형). 산출은 **Agent별 문서를 무한 생성하지 않고 단일 일관 Contract 인스턴스로 수렴**한다.

#### 3.4-A 상태 (비종단 5 · 종단 3)

**비종단 상태(5).** 기계는 Ready 인스턴스 vN이 결속될 때 `Assessing`으로 생성된다.

| 상태 | 의미 |
|---|---|
| `Assessing` | 복잡도 판정(§3.2)과 역할 할당(§3.3)을 수행하는 상태. 판정 결과로 성숙 경로 또는 스킵 경로로 분기한다. |
| `Proposing` | 할당된 각 Expert Role이 담당 관심사의 설계 **Proposal**을 산출하는 상태. |
| `Reconciling` | **Conflict Detection + Trade-off Resolution**. Proposal 간 충돌을 검출하고 상충을 해소하며 trade-off 결정을 기록한다. |
| `Reviewing` | **Integrated Design Review**. 해소된 결정을 통합해 **단일 일관 결정 집합**으로 수렴시킨다(최종 결정 소유권 — 아래 규칙). |
| `Validating` | **사용자 게이트**. 성숙 결과(또는 스킵 판정)를 사용자에게 제시하고 승인/확인/수정 응답을 받는다(UAF-INV ⑤). |

**종단 상태(3).**

| 종단 | 의미 | 산출 |
|---|---|---|
| `Matured` | 사용자 승인으로 성숙이 확정됨. | superseding v(N+1) + 선택 Projection(§3.5) |
| `Skipped` | 복잡도 스킵이 사용자 확인으로 확정됨. | 무산출(vN이 소비 대상) + 스킵 판정 기록 |
| `Escalated` | 자율 수렴 불가·사용자 강제로 상위 판단에 위임됨. | 없음(미완) |

#### 3.4-B 전이 전수 열거표 (정본)

| # | From | 계기(Trigger) | Guard | To |
|---|---|---|---|---|
| T1 | `Assessing` | 복잡도 판정 완료 | 성숙 필요 ∧ 역할 할당 완료 | `Proposing` |
| T2 | `Assessing` | 복잡도 판정 완료 | 스킵(경량 확인 요청) | `Validating` |
| T3 | `Proposing` | Proposal 수집 완료 | 할당 역할 전원 Proposal 제출 | `Reconciling` |
| T4 | `Reconciling` | 충돌 해소 | 잔여 충돌 0 ∧ trade-off 결정 기록 | `Reviewing` |
| T5 | `Reconciling` | 재제안 필요 | 충돌 해소 위해 추가 Proposal 필요 | `Proposing` |
| T6 | `Reviewing` | 통합 리뷰 수렴 | 단일 일관 결정 집합으로 수렴 | `Validating` |
| T7 | `Reviewing` | 잔여 충돌 재노출 | 리뷰 중 미해소 충돌 발견 | `Reconciling` |
| T8 | `Validating` | 사용자 응답 | 승인(성숙 경로) | `Matured` |
| T9 | `Validating` | 사용자 응답 | 확인(스킵 경로) | `Skipped` |
| T10 | `Validating` | 사용자 응답 | 수정 요청(추가 설계 필요) | `Reviewing` |
| T11 | 임의 비종단 | 자율 수렴 불가 ∨ 사용자 강제 | 에스컬레이션 | `Escalated` |

주(전수성 확인):

- **종단 도달성.** 3 종단이 모두 도달 가능하다 — `Matured`(T8)·`Skipped`(T9)·`Escalated`(T11).
- **비종단 진출성.** 5 비종단 상태가 모두 진출 전이를 가진다 — `Assessing`(T1·T2)·`Proposing`(T3)·`Reconciling`(T4)·`Reviewing`(T6)·`Validating`(T8·T9). 여기에 더해 모든 비종단 상태는 T11로 `Escalated`에 이를 수 있다(사용자 강제 일시중단·종료의 물리 재개 semantics는 Adapter 소관, §4).
- **사용자 게이트 명시.** 성숙(T8)·스킵(T9) 두 종단은 모두 `Validating`의 사용자 응답을 통과한다 — 게이트 없는 성숙/스킵 종단은 없다(§3.8 SP-INV 4·UAF-INV ⑤).

#### 3.4-C 최종 결정 소유권·단일 인스턴스 수렴 (규칙)

- **병렬 권위 없음.** 개별 Expert Role은 Proposal·논증만 하고 각자 최종 결정 권한을 갖지 않는다. `Reviewing`이 통합해 **단일 일관 결정 집합**으로 수렴시키며, 확정 권한(게이트)은 **사용자 승인**이다(T8, UAF-INV ⑤).
- **단일 인스턴스로 수렴.** 성숙 산출은 Agent별 문서를 무한 생성하지 않고 **단일 superseding Contract 인스턴스**로 수렴한다(Proposal·충돌·trade-off 기록은 코어 밖 실행 메타·워크스페이스 산출물이며 Contract 코어 필드로 유입되지 않는다 — §3.8 SP-INV 2·3).
- **다라운드 심의.** 협업은 단일 라운드 블라인드 병렬(전문가가 서로를 보지 않음)이 아니라, 전문가가 서로의 Proposal을 검토·반응하며 수렴하는 **다라운드 심의**로 수행된다(T5 재제안·T7 잔여충돌 재노출이 그 다라운드 경로다 — 상태·전이는 §3.4-A·B가 소유하며 여기서 인용만 한다). 전체 범위 커버리지 역할(§3.3)은 각 라운드에서 선언 범위 대비 **커버리지 공백**(빠진 기능·화면·프로세스 영역)을 지적한다.

#### 3.4-D 협업 단계 계약 (Phase Contracts)

프로토콜의 6개 명명 단계는 아래 계약으로 결속된다. 각 단계는 산출을 다음 단계의 입력으로 넘긴다. 단계 내부의 구체 기법(Proposal 작성법·충돌 검출 휴리스틱·trade-off 판단 규칙)은 코어가 알지 않으며 비정본 부록·Provider 소관이다(§3.8 SP-INV 5, D9).

| 단계 | 결속 상태(§3.4-A) | 입력 | 산출 | 종료 |
|---|---|---|---|---|
| ① Proposal | `Proposing` | 할당 Expert Role 집합·입력 인스턴스 vN | 역할별 설계 Proposal | 할당 역할 전원 제출(T3) |
| ② Conflict Detection | `Reconciling` | 역할별 Proposal 집합 | 검출된 충돌 목록 | 충돌 목록 확정 |
| ③ Trade-off Resolution | `Reconciling` | 검출된 충돌 목록 | 상충 해소 결정·근거 기록 | 잔여 충돌 0(T4) ∨ 재제안 필요(T5) |
| ④ Integrated Design Review | `Reviewing` | 해소된 결정 집합 | 단일 일관 결정 집합 | 수렴(T6) ∨ 잔여 충돌 재노출(T7) |
| ⑤ 최종 결정 소유권 | `Reviewing`→`Validating` | 단일 일관 결정 집합 | 확정 후보(권위 = 사용자) | 게이트 제시(T6) |
| ⑥ 사용자 승인 | `Validating` | 확정 후보(또는 스킵 판정) | 승인/확인/수정 응답 | 성숙(T8)·스킵(T9)·수정 재진입(T10) |

- **단계 = 상태 골격의 표현.** 위 6단계는 §3.4-A 상태·§3.4-B 전이의 관점 표현이며 상태·전이·종단을 새로 정의하지 않는다. 단계와 상태 골격이 어긋나면 §3.4-A·B가 우선한다.

### 3.5 Projection (파생 산출)

- **Contract = Source of Truth.** Project Contract가 유일한 진리원천이다. **Projection**은 이를 근거로 파생 생성되는 프로젝트별 산출 문서다(예: PRD·ARCHITECTURE·ADR·UI Guide — **예시일 뿐** 강제 목록이 아니다).
- **개방 레지스트리·비정본 부록 소관.** Projection 유형 목록은 **개방 레지스트리**이며 그 카탈로그는 비정본 부록 소관이다(§3.8 SP-INV 5, D9). 코어는 유형 카탈로그를 열거하지 않는다.
- **동적 선택·전 유형 강제 금지.** Projection은 프로젝트 유형·복잡도에 따라 **동적으로 선택**된다. 모든 프로젝트에 모든 유형을 강제하지 않는다. 단, **Policy가 정의한 기본 필수 세트는 성숙 경로의 기본값(default-required)** 이다 — 프로젝트별로 산출하거나 정당화 제외(사유 기록·사용자 확인)한다(§3.8 SP-INV 9). 여기서 '동적 선택'은 기본값을 opt-in으로 두는 것이 아니라, **기본값으로부터의 정당화된 이탈**(opt-out)을 뜻한다. '전 유형 강제 금지'는 개방 레지스트리의 모든 가능 유형을 강제하지 않는다는 뜻이며, Policy 기본 세트(부분집합)의 default-required와 모순되지 않는다. 스킵 경로(§3.2)는 사용자 경량 확인으로 기본 세트 전체가 제외되는 축퇴 케이스다(§3.4 T9). 기본 세트의 구체 유형 목록은 Policy·비정본 부록 소관이다(SP-INV 5).
- **워크스페이스 귀속.** 선택된 Projection 산출은 대상 프로젝트 워크스페이스에 귀속된다(§3.7). Contract와 Projection의 관계는 원천→파생이며, Projection이 Contract 코어 스키마를 재정의하지 않는다.

### 3.6 경계 기준 (vs Discovery — 04 소유 문안)

Discovery(02)와 Solution Design(04)의 책임 경계를 다음 문안으로 명문화한다. **이 문안은 04가 소유하며**, `discovery/specs/02-discovery.md`는 무수정이다(04가 일방 참조).

> **Discovery는 아키텍처 방향·기존 결정·미결 사항을 이해로 기록하고, 미결의 해소와 신규 설계 결정의 창출은 Solution Design 소관이다.**

- **대조 대상.** Discovery의 Architecture 차원(02 §3.11 5번 차원 — "아키텍처 방향과 주요 설계 결정·미결 사항")은 방향·결정·미결을 **이해로 기록**한다. Solution Design은 그 **미결을 해소**하고 **신규 설계 결정을 창출**한다.
- **차단하는 두 위험.** (i) Discovery Strategy가 설계를 심화하는 **스코프 크리프**, (ii) Discovery 사용자 승인(02 §3.7 축 3)에서 확정된 결정을 성숙 단계가 무단 번복하는 **권위 충돌**. 이 둘을 위 기준 + supersedes 계보(03 §3.4·append-only·vN 문면 불변) + 사용자 게이트(§3.4)로 차단한다.
- **번복이 아니라 재발행.** 성숙은 vN을 고쳐 쓰지 않는다 — vN을 기준선으로 새 결정을 반영한 v(N+1)을 supersedes 계보로 재발행한다(PC-INV 9 동형·03 §3.4). vN 문면은 보존된다.

### 3.7 저장 스코프 (Storage Scope — 원칙만)

- **워크스페이스 귀속 원칙.** 성숙 산출물(Proposal·충돌/trade-off 기록·Integrated Review 기록·Projection·superseding 인스턴스)은 **대상 프로젝트 워크스페이스**에 귀속된다. Framework 자체의 상태를 오염시키지 않는다(§3.8 SP-INV 7).
- **물리 배치·직렬화는 Adapter 소관.** 산출물의 물리 배치 위치·경로 관례·직렬화 형식은 정의하지 않으며 Adapter 소관이다(§4, 03 §4 관례 동형). 본 문서는 귀속 원칙만 선언한다(Scenario A 귀결 — D10).

### 3.8 Invariants (SP-INV)

Solution Design은 어떤 구현·복잡도에서도 다음 9건을 유지한다. SP-INV 1~8은 W0 §4.5의 축 고정에서 유래하고, SP-INV 9는 설계완성도 강제 트랙(2026-07-18 사용자 결정)에서 신설되었다(W0 §4.5 유래 아님). 아래 표가 전수 열거다.

| # | 명칭 | 정의 |
|---|---|---|
| **SP-INV 1** | 입력 Ready 불변 | 성숙의 입력은 `Ready`·`ReadyWithAssumptions` 종단 인스턴스뿐이다. 비Ready 인스턴스는 성숙되지 않는다(§3.1-B). |
| **SP-INV 2** | 코어 유입 금지 | 성숙 내부 개념(복잡도 판정·역할 구성·Proposal·충돌 기록 등)은 Contract 코어 필드로 유입되지 않는다(PC-INV 2 동형, 03 §3.6). |
| **SP-INV 3** | 실행 메타 불투명 | 역할 구성·Proposal·충돌·trade-off 기록은 코어 밖의 불투명 실행 메타이며 UAHF는 이를 소비하지 않는다(PC-INV 3 동형). |
| **SP-INV 4** | 사용자 승인 게이트 | 사용자 승인/확인 게이트 없이 성숙·스킵 종단에 도달하지 않는다(UAF-INV ⑤ 동형·스킵 포함 D6, §3.4). |
| **SP-INV 5** | 방법론·카탈로그 불인지 | 코어는 특정 설계 방법론·구체 역할 카탈로그·Projection 유형 카탈로그를 알지 않는다. 이들은 Provider·비정본 부록만 안다(UAF-INV ⑥ 동형). |
| **SP-INV 6** | UAHF 무수정·역참조 금지 | 코어는 UAHF spec을 수정하지 않고 하류(UAHF Agent·특정 하네스 개념)를 역참조하지 않는다 — 역할 추상까지만 정의한다(루트 §2.5 폐쇄성·UAF-INV ①). |
| **SP-INV 7** | 산출물 워크스페이스 귀속 | 성숙 산출물은 대상 프로젝트 워크스페이스에 귀속되며 Framework 상태를 오염시키지 않는다(§3.7). |
| **SP-INV 8** | 최소 할당 | 필요한 역할만 할당한다 — 불필요한 다중 역할 구성을 강제하지 않는다(§3.3). |
| **SP-INV 9** | 설계 커버리지 완성도 | 성숙 경로(`Matured`)에서, 입력 Contract가 선언한 범위(요구·선언된 접점·외부 연계)는 UAHF 구현 인계 전에 **Policy가 정의한 기본 필수 Projection 세트로 커버되거나, 각 미산출 항목이 정당화된 제외(사유 기록 + 사용자 확인)로 처리**되어야 한다. 산출도 제외 기록도 없는 침묵 누락으로 구현 경계를 넘지 않으며, 선언 범위의 일부(좁은 조각)만 하류로 넘기지 않는다. 스킵 경로(§3.2·단순 프로젝트)는 사용자 경량 확인으로 전체-제외가 승인되는 축퇴 케이스다(§3.4 T9). 기본 세트의 구체 유형 카탈로그·제외 규칙은 코어가 알지 않으며 Policy(§4)·비정본 부록 소관이다(SP-INV 5·UAF-INV ⑥ 정합). |

### 3.9 확장 포인트 (설계 0)

다음 항목은 **자리(명칭)만 표기**하고 본 문서에서 설계하지 않는다.

- **형태 B 실행 호스팅.** 논리 Expert Role·협업 프로토콜을 실제 실행 주체로 호스팅하는 물리 합성(형태 B). 명칭만 — 물리 호스팅은 후속.
- **step 기반 실행기와의 연결.** 자족적 Step·Summary 인계로 성숙 프로토콜을 구동하는 실행기와의 결속. 명칭만·설계 금지.
- **물리 재배치 퇴로 (대안 (a)).** `planning/`을 `contract/`(스키마) + `solution-design/`(성숙 활동)으로 분리하는 종국 지향 재배치. v1.3에서는 수행하지 않고 퇴로만 기록한다(W0 §2 기각 대안 (a)).
- **Solution Design Strategy Provider (방법론 격리).** 설계 방법론을 교체 가능한 Provider로 격리하는 경로(UAF-INV ⑥·02 §3.10 선례 동형). 방법론 지식이 코어로 새지 않도록 하는 확장 지점. 명칭만.
- **UI/UX Visual Contract 협의 프로토콜.** 선언된 접점(웹·앱·포털)의 시각 설계를 사용자와 반복 협의·검증하는 프로토콜 — 사용자가 구현 전에 목표 이해를 시각적으로 확인하는 확장 지점. 협의 시점 = Solution Design 사용자 게이트(§3.4 `Validating`·구현 착수 전)이며 별도 파이프라인 요소를 신설하지 않는다. 명칭만 — 구체 협의 산출물·라운드 설계는 후속 소관이며 코어는 유형 카탈로그를 알지 않는다(SP-INV 5·UAF-INV ⑥ 정합).

---

## §4. Adapter Binding (환경 의존)

### 4.1 바인딩 지점 (v1.4 물리화 대상 — 설계 아님)

§3 Core Contract는 AI·환경 비의존이다. 다음 실현은 Adapter Binding 소관이며 **v1.4에서 물리화**된다(D8 — 지점만 열거, 설계 없음).

| §3 계약 요소 | 바인딩 지점(일반형) |
|---|---|
| Expert Role 실행 호스팅(§3.3) | 논리 Expert Role을 어느 실행 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(M5). |
| 사용자 게이트 제시·응답 채널(§3.4 `Validating`) | 성숙/스킵 결과 제시와 승인/확인/수정 응답을 받는 개입 채널(강제 일시중단·재개 semantics 포함). |
| 산출물 저장 위치(§3.7) | Proposal·리뷰 기록·Projection·superseding 인스턴스가 워크스페이스에 배치·보관되는 물리 위치·경로 관례·직렬화 형식. |
| 복잡도 판정·역할 선택·Projection 선택 Policy 실값(§3.2·§3.3·§3.5) | 판정 임계·역할 선택 규칙·Projection 유형 선택 정책의 데이터 소스·직렬화(Policy as Data). |

특정 AI·모델·제품 기능·직렬화 형식·환경 경로·역할 고유명은 여기서도 명명하지 않는다. 구체 인스턴스는 해당 Adapter Binding 문서 소관이다(02 §4·03 §4 동형).

### 4.2 이식 교체 지점 (Portability Swap Points)

- 실행 호스팅·게이트 채널·저장 위치·Policy 실값 → 대상 환경의 실행/개입/저장/정책 메커니즘.
- **유지되는 것**: §3.1 단계 계약, §3.2 판정 형태, §3.3 역할 추상, §3.4 프로토콜 골격, §3.5 Projection 관계, §3.6 경계 기준, §3.8 SP-INV. 이들은 이식 시 바뀌지 않는다.

---

## §5. Memory Access

**해당 없음 (v1.3).** Solution Design은 v1.3에서 UAHF Memory / UAF 레벨 `knowledge/`를 회수·기록하지 않는다. Memory Consult는 UAHF 소관의 비담당이며(루트 §10 비담당④), 본 문서는 형태 A 설계 계약이므로 Memory에 접근하지 않는다(02 §5·03 §5 동형).

- **확장 포인트(설계 안 함).** 향후 성숙 활동이 기억을 활용한다면, 접근은 **Memory Service Interface(단일 Port)** 경유만 허용되며 영속성 백엔드에 직접 접근하지 않는다(`uahf/specs/00-glossary.md` §3.2-C). v1.3은 이 경로를 설계하지 않는다.

---

## §6. Failure Modes

| 실패 시나리오 | 대응 | 위반 불변 / Lesson |
|---|---|---|
| 비Ready 인스턴스(Suspended/Escalated/Aborted)를 성숙 입력으로 시도 | 차단. 입력은 Ready 종단 인스턴스뿐. | SP-INV 1 위반 · Lesson 후보 |
| 사용자 승인/확인 게이트 없이 성숙·스킵 종단 선언 | 무효·차단. 게이트 없는 종단 없음. | SP-INV 4 위반(UAF-INV ⑤) · Lesson 후보 |
| 성숙 내부 개념(역할·Proposal·충돌)이 Contract 코어 필드로 유입 | 차단·교정. 실행 메타는 코어 밖·불투명. | SP-INV 2·3 위반 · Lesson 후보 |
| Discovery가 승인한(G3 사용자 승인) 결정을 성숙이 무단 번복(vN 문면 수정) | 차단. 번복이 아니라 supersedes 재발행 — vN 문면 불변(§3.6). | 경계 기준·PC-INV 9 위반 · Lesson 후보 |
| 방법론 고유명·고정 역할 카탈로그·Projection 유형 카탈로그가 코어에 유입 | 차단·교정. 이들은 Provider·비정본 부록만 안다. | SP-INV 5 위반(UAF-INV ⑥) · Lesson 후보 |
| Agent별 문서 무한 생성(다중 산출물 분산) | 차단. 산출은 단일 일관 superseding 인스턴스로 수렴(§3.4-C). | SP-INV 2·3 정합 · Lesson 후보 |
| 코어가 UAHF Agent·특정 하네스 실행 주체를 역참조 | 차단. 코어는 역할 추상까지만(폐쇄성). | SP-INV 6 위반(UAF-INV ①) · Lesson 후보 |
| 의존 계약 미확정·경계 충돌을 추측으로 우회 | 차단. 추측 금지 — `Escalated`로 상위 판단 위임(§3.4 T11). | 에스컬레이션 규율 · Lesson 후보 |

---

## §7. Verification

### 완료 기준 (시연 가능 문장)

판정은 아래 항목을 지목 절 문면과 직접 대조해 내린다(여기서 §3을 재서술하지 않는다). 괄호는 원 done 번호다.

1. 단계 계약 — 입력(Ready\|ReadyWithAssumptions 종단 vN·비Ready 금지)·출력 2경로·두 경로의 사용자 게이트 통과 — §3.1 (done 1·2)
2. 복잡도 판정 = Policy as Data · 스킵 게이트(D6 경량 확인) — §3.2 (done 3)
3. 역할 할당 — Capability 선언·개방 네임스페이스·코어 역할 카탈로그 0건(스캔)·최소 할당·실행 주체 매핑 Adapter 위임 — §3.3 (done 4)
4. 협업 프로토콜 — 비종단 5·종단 3 열거 · 전이표의 종단 도달성·비종단 진출성 · 성숙/스킵의 `Validating` 게이트 통과 — §3.4-A·B (done 5)
5. Projection — Contract = Source of Truth · 파생(예시로만)·동적 선택·전 유형 강제 금지·워크스페이스 귀속 — §3.5 (done 6)
6. SP-INV 1~9 열거(표 9행) — §3.8 (done 7)
7. 경계 기준 — W0 §4.4 문안의 04 소유 · 02 무수정 — §3.6 (done 8)
8. 저장 스코프 — 귀속 원칙만 선언·물리 배치 Adapter 위임 — §3.7 (done 9)
9. Adapter 바인딩 지점 열거(설계 0) — §4.1 (done 10)
10. 확장 포인트 5건을 명칭만·설계 0으로 표기 — §3.9 (done 11)
11. 관행 규격(상태 라인·개정 기록 = git 커밋[규범 `docs/spec-versioning-policy.md` §3]·§ 포인터 재정의 0 · 방법론 고유명·특정 AI/모델/제품 기능명·고정 역할 카탈로그 0건 스캔) (done 12)
12. 설계 커버리지 완성도 — SP-INV 9(선언 범위의 기본 필수 세트 커버 또는 정당화 제외)·§3.3 커버리지 바닥·§3.4-C 다라운드 심의·§3.5 default-required opt-out, 넷 모두 구체 유형명·역할명 0(Policy·비정본 부록 포인터만) (done 13)

### 검증 방법 (Verifier)

- Verifier가 §3.4 전이표를 파싱해 3 종단 도달성·5 비종단 진출성·사용자 게이트(T8·T9) 통과를 확인한다.
- Verifier가 §3.8 SP-INV 표 행 수(9)를 센다. SP-INV 1~8은 W0 §4.5 8축과 대조하고, **SP-INV 9(신설)는 설계완성도 강제 트랙 근거와 대조**한다.
- Verifier가 §3.6 경계 문안을 W0 §4.4와 대조하고, `discovery/specs/02-discovery.md`가 무수정임을 `git status --short`로 확인한다.
- Verifier가 본문 전체를 방법론 고유명·특정 AI 실명·모델명·제품 기능명·고정 역할 팀 명칭 다중 패턴으로 전수 스캔해 0건을 확인한다(구체 패턴 목록은 Verifier가 보유 — 코어 본문에 예시 나열 0).
- Verifier가 §3이 03 스키마 필드 신설·PC-INV 재정의·UAHF 연산/필드/불변 변경 서술을 포함하지 않음을(§ 포인터만) 확인한다.
- Verifier가 산출 파일이 `planning/specs/04-solution-design.md` 단일이며 다른 파일 무촉임을 `git status --short`로 확인한다.
- 판정 순서는 UAHF 검증 게이트 관행과 동형이다 — CP1 Worker 자체 점검 → CP2 Verifier 독립 판정 → CP3 Advisor 승인(`uahf/specs/00-glossary.md` §3.2-E·§3.2-F). 자체 점검은 최종 승인이 아니다.

---

## §8. Examples

예시는 **프로세스 골격**만 보인다. 물리 실행 호스팅·저장 위치는 Adapter 소관이며(§4) 여기서 명명하지 않는다. 역할 예시는 비정본 부록 소관이므로 구체 역할명을 쓰지 않는다.

### 예 1 — 성숙 경로 (복잡 프로젝트 → `Matured`)

입력: Ready 인스턴스 v1(Discovery 종단, 02 §3.7).

`Assessing`[복잡도 판정 = 성숙 필요 ∧ 최소 필요 Expert Role 할당(Capability 선언)] → (T1) `Proposing`[할당 역할별 설계 Proposal 산출] → (T3) `Reconciling`[충돌 검출·trade-off 해소·결정 기록] → (T4) `Reviewing`[통합 리뷰 — 단일 일관 결정 집합 수렴] → (T6) `Validating`[사용자에게 성숙 결과 제시] → (T8, 사용자 승인) `Matured`.

산출: superseding 인스턴스 **v2**(supersedes = v1·v1 문면 불변·03 §3.4) + 동적 선택된 Projection 산출(대상 워크스페이스 귀속). Proposal·충돌 기록은 코어 밖 실행 메타로 남고 Contract 코어 필드로 유입되지 않는다(SP-INV 2·3).

### 예 2 — 스킵 경로 (단순 프로젝트 → `Skipped`)

입력: Ready 인스턴스 v1.

`Assessing`[복잡도 판정 = 스킵] → (T2) `Validating`[경량 사용자 확인 요청] → (T9, 사용자 확인) `Skipped`.

산출: 무산출 — v1이 곧 UAHF 소비 대상이다(스킵 판정 기록만 남는다). 스킵도 사용자 게이트를 통과한다(D6·SP-INV 4).

### 예 3 — 수정 요청 재진입 / 에스컬레이션

`Reviewing` → (T6) `Validating`[결과 제시] → (T10, 사용자 수정 요청) `Reviewing`[추가 설계]. 자율 수렴이 불가하거나(잔여 충돌 미해소·의존 계약 미확정) 사용자가 강제하면 임의 비종단에서 (T11) `Escalated`로 상위 판단에 위임한다 — 추측으로 우회하지 않는다.

주: 완전한 dogfooding E2E 워크스루(pc-uahf-001 v1→v2 실증)는 **v1.4 이월**이다(D8). 본 예시는 프로토콜 최소 예시다.

(정본 형제 관례 동형 — §9 절 번호는 문서 머리의 **이력(Revision History)**이 사용하며 본문은 §8에서 종결한다: `discovery/specs/02-discovery.md`·`planning/specs/03-project-contract.md`·`entry/specs/01-entry.md`. 미해결·후속 항목[03 v1.2 델타·planning 개관 정합·루트 §12 용어 등재·Adapter Binding v1.4 이월]은 본문 인라인 주석[§0·§2·§4]과 완료 보고 open_questions로 표면화하며 전부 비차단이다.)
