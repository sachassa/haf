# planning/adapters/claude/solution-design-binding — Claude Code Solution Design Adapter 바인딩

상태: v1.4 Baseline
상위 규약: AGENT.md
근거 정본:

- planning/specs/04-solution-design.md §3(전문 — Core Contract)·§4.1(### 4.1 바인딩 지점 — 표 4행)·§4.2(### 4.2 이식 교체 지점). 본 문서가 물리 실현으로 바인딩하는 계약의 정본. **재정의·확장하지 않고 § 포인터로만 인용한다.** 특히 §3.1(단계 계약)·§3.2(복잡도 판정 — Policy as Data)·§3.3(역할 할당·개방 네임스페이스)·§3.4(협업 프로토콜 State Machine — 비종단 5·종단 3·전이 T1~T11)·§3.5(Projection)·§3.6(경계 기준)·§3.7(저장 스코프)·§3.8(SP-INV 1~9 — SP-INV 9 = 설계 커버리지 완성도, 2026-07-18 신설).
- planning/specs/03-project-contract.md §3.1-B(생산자 2경로 — (ii) superseding 성숙 인스턴스)·§3.4(인스턴스 거버넌스 — append-only·supersedes·**Contract Maturation 갱신 유형**)·§3.5(UAHF Interface — 선택 입력·소비 지점)·§3.6 PC-INV 9(인스턴스 이력 append-only). 성숙 재발행이 소비·산출하는 스키마·거버넌스의 정본. **참조 인용만·재정의 0.**
- ARCHITECTURE.md (루트, v1.3 — 라우터) §8 UAF-INV ①(접점 원칙·유일 접점)·⑤(확정 게이트 = 사용자 승인)·⑥(Framework는 방법론·역할 카탈로그 모름)·§7.1(상시 불변 확인 2건). 근거 인용용·재정의 0.
- planning/adapters/claude/contract-binding.md §4.1(저장 위치)·§4.2(저장 이원화 — 일반 관례 `.claude/project-contract/`·본 저장소 `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`·파일명 `project-contract.v<N>.md`, DP-X2)·§5(버전 표기 — `schemaVersion`·`instanceVersion`·`supersedes`)·§6(Provenance 불투명 컨테이너 외형·must-ignore 경계 — DP-X6). **superseding 인스턴스 저장·버전 표기·Provenance 외형은 contract-binding 소유** — 본 문서는 참조 인용만 하고 재정의하지 않는다.
- discovery/adapters/claude/discovery-binding.md §3(append-only 레코드 로그·1 사건 = 1 레코드·§3.3 순서 값/물리 시각 성격 구분 L-09)·§4(백엔드 트리 정본 선언·run 단위 격리)·§5(주 세션 사용자 제시·응답 채널)·§7(역할 추상 호스팅 — 형태 A 규약 절차·물리 호스팅 설계 0)·§8(Policy 데이터 소스·최소 실값 1세트 정본 값 표 DP-X5)·§10(성숙 아닌 Discovery run 내부 형식 확정 — Provenance 내부 형식 소유 경계 선례)·§13(실측 대조 L-07). **핵심 골격 선례.** 본 문서는 이 골격과 동형으로 서술하되 Discovery 도메인 계약(Event 15종·State Machine·Dimension·Budget)을 차용하지 않는다.
- entry/adapters/claude/entry-binding.md 머리·§0·memory-binding.md·loop-binding.md §5.2 — 자매 Adapter Binding 골격·사람 개입 채널·백엔드 격리·append-only 선례. `형태 A/B` 서술 라벨 인용 출처(structure.md §4).
- uahf/framework/core/structure.md §2(4경계 배치 — `framework/adapters/<adapter>/` = 환경 의존 격리 경계)·§5(금지 토큰 규칙 C-3 — Adapter 경계는 격리 보유로 비적용). 본 문서 경계·격리 토큰 허용의 근거.
- planning/ARCHITECTURE.md §0·§7 — 소유 Layer 개관(planning 이중 책임 — 성숙 활동 측). § 포인터로만 참조.
- uahf/specs/00-glossary.md — UAHF 용어 정본. 본 문서는 새 용어를 신설하지 않는다. `형태 A/B`는 structure.md §4의 서술 라벨 인용이며 Glossary 표제어가 아니다.

거버넌스: 이 문서는 `planning/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core·UAF 계약을 특정 실행 환경·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 직렬화 형식·물리 경로·환경 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — 자매 contract-binding.md §0·entry-binding.md §0·discovery-binding.md §0과 동형). 단 이 문서는 UAF 정본(planning/specs/04-solution-design.md §3·§4)과 자매 정본(03·02·루트 ARCHITECTURE)·UAHF 정본을 **재정의하지 않는다** — 계약(단계 계약·복잡도 판정·역할 할당·협업 프로토콜 State Machine·Projection·경계 기준·SP-INV)은 § 포인터로만 인용한다. 개정은 Advisor 승인으로 이뤄진다(docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-18 | v1.4 (정합) | §DC-1 Wave 2 — 기본 필수 Projection 세트 10종·전체 커버리지 바닥·제외 규칙을 §7.2 Policy 값으로 등재, SP-INV 교차 참조 8건→9건(1~9) 갱신. 사용자 결정 2026-07-18. | Worker (Advisor 위임) |
| 2026-07-19 | v1.4 (정합) | §DC-1 Wave 5-A — 산출물 생산 프로토콜 형식화(form-A). §7.2 (나)에 기본 역할 구성(`defaultComposition`)·이탈 규칙(`deviationRule`)·역할→산출물 소유 맵(`artifactOwnership`) 등재·`maxSpecialistRoles` 3→4. §7A(산출물 생산 프로토콜 — 위임 산출·Markdown+매니페스트·검증 3층·컨펌 3시점) 신설. §11.3 역할 기본값 격리 지점 등재 정합(SP-INV 5는 코어만 구속). 책임 있는 자율(루트 §6 원칙 11) 물리 실현. 사용자 결정 2026-07-19. | Worker (Advisor 위임) |

(이력 절은 문서 머리에 둔다 — UAF 관행 동형: `planning/specs/04-solution-design.md` §9·자매 부록 §9. 절 번호는 §9지만 배치는 머리다. 본 이력 표는 이번 개정에서 신설되었으며, 이전 개정 계보는 git에 있다. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **바인딩 대상 정본 선언.** 이 문서는 planning 레이어 자신의 Claude 어댑터 바인딩이며 `planning/specs/04-solution-design.md` §3·§4를 바인딩한다. 바인딩 대상 정본은 UAHF spec(uahf/specs/01~13)이 아니라 UAF 정본 `planning/specs/04-solution-design.md`이며, 본 문서는 그 계약 요소를 재정의·확장하지 않고 § 포인터로만 인용한다. 자매 어댑터 바인딩(contract-binding = `planning/specs/03`·entry-binding = `entry/specs/01`·discovery-binding = `discovery/specs/02`)과 파일명·골격 관례는 동형이다.

- **정본은 planning/specs/04 §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소 — 단계 계약(§3.1)·복잡도 판정(§3.2)·역할 할당·개방 네임스페이스(§3.3)·협업 프로토콜 State Machine(§3.4 — 비종단 5·종단 3·전이 T1~T11)·Projection(§3.5)·경계 기준(§3.6)·저장 스코프(§3.7)·SP-INV 1~9(§3.8 — SP-INV 9 = 설계 커버리지 완성도) — 를 **재정의·확장하지 않는다.** 계약 요소는 정본 § 포인터로만 인용한다. 본 문서가 확정하는 것은 04 §4.1이 "Adapter 소관"으로 미룬 **네 지점 — ① Expert Role 실행 호스팅(역할 추상까지만) ② 사용자 게이트 제시·응답 채널 ③ 산출물 저장 위치·직렬화(실행 기록 포함) ④ Policy 실값** 과, 그 저장의 부속으로 성숙 인스턴스 `provenance` 컨테이너의 **성숙 run 내부 형식**뿐이다(§2).

- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문, 그리고 UAF 정본(planning/specs/04) 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이다(structure.md §5 C-3 확장·04 §3 도입 "이 섹션에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다"). 이 문서는 그 **반대편**이다 — 구체 직렬화 형식·물리 경로(`planning/adapters/claude/…`·`.claude/…`)·파일 확장자의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(contract-binding.md §0·discovery-binding.md §0과 동형). 단 **UAF 정본이 명명하지 않은 것을 UAF 정본 문면인 것처럼 서술하지 않는다** — 물리 확정은 전부 본 문서 소유임을 명시한다. 특정 설계 방법론 고유명·고정 역할 카탈로그·타 AI 벤더·모델명은 여기서도 명명하지 않는다(04 §4.1 말미·UAF-INV ⑥ 동형 — 격리 대상은 직렬화 형식·물리 경로·Policy 값뿐이다).

- **하네스 Bootstrap 전제(형태 A).** 이 하네스는 현재 Bootstrap 상태다(자매 바인딩 §0). 본 문서의 바인딩은 **실행 코드 0**이다 — Solution Design의 협업 프로토콜 State Machine(04 §3.4)·복잡도 판정(04 §3.2)·역할 협업(04 §3.3)은 실행 스크립트가 아니라 **규약 절차·규약 역할**로 실현되며 주 세션이 실수행한다. 따라서 매핑은 (i) 물리 실재 표면(자매 바인딩·정본 문서·Ground Truth 인스턴스), (ii) 규약으로 확정된 정본 문면(형태 A — 백엔드 트리·기록 어휘·게이트 채널·Policy 값), (iii) 실행 코드 도입 시 로딩될 지점(형태 B — 로그 기록기·직렬화기·Policy 로더)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.

- **경계 분담 — 소유와 위임.** 성숙 산출이 걸치는 자매 정본과의 경계를 명시한다. (i) **superseding 인스턴스 자체**(v(N+1) 문서·버전 표기·저장 경로 `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`·직렬화 = Markdown 본문 + YAML front-matter)는 **contract-binding §3·§4·§5 소유**다 — 03 v1.2 생산자 2경로(§3.1-B)상 Contract 저장은 생산자와 무관하며, 본 문서는 성숙 경로가 그 경로에 append됨만 참조 인용한다(재정의 0). (ii) `provenance` 컨테이너의 **외형·must-ignore 경계**는 **contract-binding §6 소유**다 — 본 문서는 성숙 run에 해당하는 **내부 형식**만 확정한다(§8, discovery-binding §10이 Discovery run 내부 형식을 확정한 것과 동형·경계 침범 0). (iii) 본 문서가 신설·소유하는 것은 **`solution-design-data/` 백엔드 트리**(성숙 실행 메타 — 이벤트 로그·실행 메타 파일·Policy)뿐이다.

- **책임 경계 문안 (Solution Design 활동 vs Contract Maturation 갱신 유형).** 본 문서가 물리화하는 대상을 다음 문안으로 못박는다(W0 §4.5·04 §0·03 §3.4 정합):

  > **Solution Design은 활동이고, Contract Maturation은 그 활동이 산출하는 갱신 유형이다.** Solution Design(04)은 Ready vN을 입력으로 복잡도 판정·역할 협업·사용자 게이트를 수행하는 **UAF 레벨 활동**이며, 그 성숙 경로 종단(Matured)의 산출이 **Contract Maturation**(03 §3.4 갱신 유형) — 동일 append-only·supersedes 메커니즘에 의한 v(N+1) 재발행 — 이다. 활동 계약은 04가, 재발행 메커니즘·인스턴스 거버넌스는 03이 소유한다. 어느 쪽도 상대를 재정의하지 않는다.

  본 문서는 이 구분의 **물리 측면**만 확정한다 — 활동(04)의 실행 메타·게이트·Policy·호스팅은 `solution-design-data/`(본 문서)에, 갱신 유형(03 §3.4)이 낳는 superseding 인스턴스는 contract-binding §4.2 경로에 놓인다. 두 물리 자리가 활동/갱신 유형의 구분을 그대로 반영한다.

- **실측 기반 상태 서술(L-07).** "실재/미존재" 주장은 파일 시스템 확인 후에만 기입한다. 본 문서가 선언하는 `solution-design-data/` 백엔드 트리는 성숙 run E2E로 이미 실재하며, 현행 물리 위치는 `uahf/framework/adapters/claude/solution-design-data/`다(물리 위치는 2차 산출물 디커플링 트랙에서 확정). 본 문서는 경로·구조·형식·값의 **정본 문면만** 소유하고, §12가 그 실측 대조 표다.

- **경로 표기 관례.** 본 문서 자신은 `planning/adapters/claude/solution-design-binding.md`(planning 레이어 어댑터 경계)에 있다. 본 문서가 선언·소유하는 백엔드 데이터 트리(`solution-design-data/`·`discovery-data/contracts/uahf/`)의 현행 물리 위치는 `uahf/framework/adapters/claude/…` 아래이며(물리 위치는 2차 산출물 디커플링 트랙에서 확정), 본문에서는 그 잎 이름(`solution-design-data/` 등)으로 축약해 가리킨다. 소비 프로젝트 일반 관례 경로(`.claude/…`)는 소비 프로젝트 상대 경로다.

- **네임스페이스·용어.** 본 문서가 확정하는 것은 물리 표기(백엔드 트리·기록 어휘·게이트 채널·Policy 값·Provenance 성숙 run 내부 형식)뿐이며, 04가 소유하는 계약 용어(`Assessing`·`Proposing`·`Reconciling`·`Reviewing`·`Validating`·`Matured`·`Skipped`·`Escalated`·전이 T1~T11·Expert Role·Capability·Projection·SP-INV 등)는 04 정의를 § 포인터로 참조하고 재정의하지 않는다. 새 UAHF 용어·새 계약 요소(상태·전이·불변·필드·kind)를 신설하지 않는다. 본 문서가 명명하는 **레코드 종류 명칭**(§4)은 04·03 코어 계약 요소가 아니라 이 Adapter의 **기록 관례**이며, Discovery Event 15종(02 §3.5 소유)의 명칭을 차용하지 않는다.

---

## §1. 목적

이 문서는 planning/specs/04 "### 4.1 바인딩 지점" 표 4행을 이 환경 위에 **v1.4 시점의 구체 물리 실현**으로 매핑한다. Solution Design의 성숙 산출(superseding Contract 인스턴스)은 UAHF 구현 단계의 선택 입력(03 §3.5-A)이므로, 본 문서가 확정하는 물리 인터페이스는 v1.4 W2 dogfooding E2E의 물리 실현 기반이다.

책임은 다섯이다.

- 04 §4.1 바인딩 표 **4행 전부**(① 실행 호스팅 ② 게이트 채널 ③ 저장 위치 ④ Policy 실값) + 실행 기록 직렬화(③의 일부 — 04 §3.2 "판정 근거 기록"·§3.7 물리 배치 Adapter 위임의 실현)를 물리 실현으로 확정한다(§2 — 실재/규약 실현(형태 A)/형태 B 3구분).
- **DP-1**: `solution-design-data/` 백엔드 트리를 정본으로 선언하고, superseding 인스턴스가 contract-binding §4.2 경로에 append됨을 참조 인용한다(§3). **DP-2**: run 단위 append-only 기록 로그의 직렬화·순서 값 성격·최소 레코드 어휘를 확정한다(§4).
- **DP-4**: 사용자 게이트 제시·응답 물리 채널과 T8~T11 실의미를 확정한다(§5). **DP-3**: Expert Role 실행 호스팅을 **역할 추상까지만** 확정한다(§6).
- **DP-5**: `solution-design-data/policy/` 데이터 소스·직렬화 + **최소 실값 1세트**를 정본 값 표로 확정한다(§7). **Provenance**: 성숙 run 내부 형식을 확정한다(§8).
- 04·03·02·루트 재정의 0·새 계약 요소 창설 0·Discovery Event 명칭 차용 0을 **상시 불변 자기 점검**으로 보이고(§11), 04 §4.2 이식 교체 지점에 대응을 명시하며(§10), 상태 서술을 실측과 대조한다(§12).

이 문서는 04 §3·§4·자매 정본(03·02·루트)·UAHF 정본의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A → 형태 B 전환 시에도 04 §3 계약 변경은 0이며(structure.md §7 C-1 동형), §10의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 04 §4.1 바인딩 표 4행 물리 실현 (done 2)

04 "### 4.1 바인딩 지점" 표의 **4행 전부**를 물리 표면으로 매핑한다. "04 §4.1 바인딩 지점" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 형식·경로·채널·값을, "실재 여부" 열이 Bootstrap 상태에서의 **물리 실재 / 규약 실현(형태 A) / 형태 B**를 정직하게 구분한다(§12 실측 대조).

| # | 04 §3 계약 요소 (정본 §) | 04 §4.1 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Expert Role 실행 호스팅 (§3.3) | "논리 Expert Role을 어느 실행 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(M5)." | 주 세션(Advisor)이 Orchestrator 역할을 규약 절차로 수행해 State Machine(04 §3.4)을 구동하고, Expert Role 수행은 **이 환경의 기존 위임 실행 관행**(서브에이전트 위임·완료 보고·독립 검증)을 재사용. 새 병렬 실행 프레임워크 창설 0·물리 호스팅(실행 코드·자동화) 설계 0. 상세 §6. | 역할 추상 확정(정본, 형태 A). 물리 호스팅 = **설계 안 함**(확장 포인트 04 §3.9). 실행 코드 = 형태 B. |
| 2 | 사용자 게이트 제시·응답 채널 (§3.4 `Validating`) | "성숙/스킵 결과 제시와 승인/확인/수정 응답을 받는 개입 채널(강제 일시중단·재개 semantics 포함)." | 주 세션 사용자 제시·응답 수령 채널(discovery-binding §5 동형) — 게이트 제시·응답 각각 레코드로 기록. T8(승인→Matured)·T9(확인→Skipped)·T10(수정→Reviewing 재진입)·T11(강제→Escalated) 실의미. 승인 전 Matured 도달 불가(SP-INV 4). 상세 §5. | 채널·기록 확정(정본, 형태 A). 무인 자동 제시 UI = 형태 B. |
| 3 | 산출물 저장 위치 (§3.7) | "Proposal·리뷰 기록·Projection·superseding 인스턴스가 워크스페이스에 배치·보관되는 물리 위치·경로 관례·직렬화 형식." | 성숙 실행 메타(이벤트 로그·Proposal·충돌/trade-off·리뷰 기록·Policy) = `solution-design-data/`(§3·§4); superseding 인스턴스 = contract-binding §4.2 경로 `discovery-data/contracts/uahf/project-contract.v<N>.md`에 append(참조 인용·재정의 0); Projection = 대상 워크스페이스 귀속(§3). 상세 §3·§4. | 경로·형식 정본 확정(형태 A). `solution-design-data/` 데이터 = 실재(현행 `uahf/framework/adapters/claude/…`, §12). |
| 4 | 복잡도 판정·역할 선택·Projection 선택 Policy 실값 (§3.2·§3.3·§3.5) | "판정 임계·역할 선택 규칙·Projection 유형 선택 정책의 데이터 소스·직렬화(Policy as Data)." | `solution-design-data/policy/default-policy.yaml` 데이터 파일 + **최소 실값 1세트 정본 값 표**(성숙/스킵 판정 기준·역할 선택 규칙·Projection 선택 정책). Policy as Data — 값 조정 = 데이터 정정. 상세 §7. | 형식·값 정본 확정(형태 A). 물리 데이터 파일(`policy/`) = 실재(§12). |

주:

- 위 4행은 04 "### 4.1 바인딩 지점" 표의 전 행이다. 각 행의 "물리 실현"은 04 §4.1 정본 표현을 이 환경의 구체 형식·경로·채널·값으로 좁힌 것이며, **새 바인딩 계약을 창설하지 않는다**(§0). 실행 기록 직렬화(§4)는 행 3(저장 위치·직렬화 형식)의 일부이자 04 §3.2 "판정 근거 기록"·§3.7 물리 배치 Adapter 위임의 실현이며, 별도 바인딩 지점을 창설하지 않는다.
- 04 §4.1 표에 없는 계약 요소(§3.1 단계 계약·§3.2 판정 형태·§3.3 역할 추상·§3.4 프로토콜 골격·§3.5 Projection 관계·§3.6 경계 기준·§3.8 SP-INV)는 **이식 시에도 유지되는 것**이며, 본 문서가 바인딩하지 않는다(§10 "유지되는 것" 열). 이들의 진위 판정 기준은 04 §3이다.
- 특정 설계 방법론 고유명·고정 역할 카탈로그·타 AI 벤더·모델명은 여기서도 명명하지 않는다(04 §4.1 말미·UAF-INV ⑥ 동형).

---

## §3. DP-1 — 저장 위치·백엔드 트리 정본 선언 (done 3)

04 §4.1 행3("Proposal·리뷰 기록·Projection·superseding 인스턴스가 … 배치·보관되는 물리 위치·경로 관례·직렬화 형식")의 물리 실현을 확정한다. 저장 스코프 원칙(04 §3.7 — 워크스페이스 귀속·SP-INV 7)은 재정의하지 않고 § 포인터로 인용하며, 물리 위치·경로 관례만 확정한다.

### §3.1 성숙 실행 메타 백엔드 = `solution-design-data/` 신설 (DP-1)

Solution Design의 **성숙 실행 메타**(이벤트 로그·Proposal·충돌/trade-off·리뷰 기록·Policy)의 물리 백엔드를 **Adapter 경계 이하 `uahf/framework/adapters/claude/solution-design-data/`로 확정한다**(자매 memory-binding §0 `memory-data/`·loop-binding §0 `loop-data/`·discovery-binding §4 `discovery-data/` 백엔드 격리 선언 동형).

- **신설 근거(UAF-INV ① 안전).** `discovery-data/`는 discovery-binding §4가 소유한 **Discovery 전용 백엔드 정본**이다 — 여기에 성숙 실행 데이터를 혼입하면 책임 경계가 오염된다. 자매 `*-data/` 격리 관례 동형으로 별도 루트를 두는 것이 최소 변경이며, 성숙 산출 데이터가 하네스 규약·Core와 혼입되지 않도록 격리한다(UAF-INV ① 안전 — contract-binding §4.2 격리 근거 동형).
- **이원화(DP-X2 동형).** 위 격리 배치는 본 UAF 저장소 자신을 대상으로 하는 dogfooding 인스턴스의 관례다. **일반 관례**(소비 프로젝트)에서 성숙 실행 메타는 소비 프로젝트 내 `.claude/solution-design/` 아래에 귀속된다(04 §3.7 워크스페이스 귀속·contract-binding §4의 `.claude/project-contract/` 이원화 동형). 두 경로 모두 본 문서가 정본으로 확정한다.

### §3.2 백엔드 트리 (정본 문면 · 물리 위치는 2차 산출물 디커플링 트랙에서 확정)

```
uahf/framework/adapters/claude/               # 물리 위치는 2차 산출물 디커플링 트랙에서 확정
└─ solution-design-data/                     # ★ SD 백엔드 격리 루트 — 성숙 run E2E로 실재
   ├─ events/                                # DP-2 — run 단위 append-only 기록 로그 + 실행 메타
   │  └─ maturation-<run-id>/                #   성숙 run 1건의 격리 디렉터리
   │     ├─ events.jsonl                     #     append-only 기록 로그(전이·게이트·산출·run 생애; §4)
   │     └─ <실행 메타 파일…>                #     Proposal·Reconciling(충돌/trade-off)·Reviewing 기록
   │                                         #     (SP-INV 2·3 — 코어 밖 실행 메타·Contract 코어 필드 유입 0)
   └─ policy/
      └─ default-policy.yaml                 # DP-5 — 최소 실값 1세트(§7)
```

- **`events/maturation-<run-id>/`(DP-2, §4).** 한 성숙 run 1건의 append-only 기록 로그(`events.jsonl` 동형)와 실행 메타 파일을 run 단위로 격리 보관한다. `<run-id>`는 해당 성숙 run(= Ready 인스턴스 vN 결속으로 `Assessing`에 생성된 State Machine 인스턴스, 04 §3.4-A)의 식별자다. run 단위 디렉터리로 격리해 서로 다른 run의 기록이 섞이지 않게 한다(discovery-binding §3.4 run 단위 격리 동형). 로그 파일명·레코드 파일 단위의 세부는 Adapter 재량이며, 어느 경우에도 §4 append-only·순서 값 성격은 유지된다(선취·추측 금지).
- **실행 메타 파일(SP-INV 2·3 — 코어 밖).** Proposal·충돌/trade-off·통합 리뷰 기록은 run 디렉터리 내 실행 메타 파일로 둔다. 이들은 **코어 밖의 불투명 실행 메타**이며 Contract 코어 필드로 유입되지 않고 UAHF가 소비하지 않는다(04 §3.8 SP-INV 2·3·§3.4-C 단일 인스턴스 수렴). Agent별 문서를 무한 생성하지 않고 단일 superseding 인스턴스로 수렴하는 04 §3.4-C 규칙을 물리 저장이 그대로 반영한다.
- **`policy/`(DP-5, §7).** 복잡도 판정 기준·역할 선택 규칙·Projection 선택 정책의 데이터 파일을 둔다. Policy as Data이므로 값 조정은 데이터 정정일 뿐 Orchestrator 규약 절차·정본 계약 무변경이다(04 §3.2).

### §3.3 superseding 인스턴스·Projection 저장 (참조 인용 — 재정의 0)

- **superseding 인스턴스(v(N+1))는 이 트리가 아니다.** 성숙 경로의 superseding Contract 인스턴스(03 §3.4·§3.1-B (ii))는 `solution-design-data/`가 아니라 **contract-binding §4.2가 소유한 Contract 저장 경로**에 append된다 — 본 저장소 dogfooding은 `uahf/framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v<N>.md`, 일반 관례는 `.claude/project-contract/project-contract.v<N>.md`(파일명·직렬화·버전 표기 정본 = contract-binding §3·§4·§5). Contract 저장은 생산자(Discovery / Solution Design)와 무관하게 contract-binding 소유이며(03 v1.2 생산자 2경로·§3.1-B), 본 문서는 이 경로를 **참조 인용**만 하고 재정의하지 않는다. 예: Ground Truth `pc-uahf-001` v1을 기준선으로 성숙하면 v2는 `project-contract.v2.md`로 같은 경로에 append되고 v1 문면은 byte 불변이다(PC-INV 9·03 §3.4·append-only).
- **Projection 산출.** 동적 선택된 Projection(04 §3.5)은 **대상 프로젝트 워크스페이스에 귀속**된다(04 §3.7 SP-INV 7). 본 저장소 dogfooding에서 Projection이 산출되는 경우 그 물리 배치도 워크스페이스 귀속 원칙을 따르며, Contract를 Source of Truth로 하는 파생 산출이다(04 §3.5 — Contract 코어 스키마 재정의 0). 물리 배치 세부는 산출 시(E2E) 확정하며 본 문서는 귀속 원칙만 선언한다.
- **`solution-design-data/`는 지원 구조(성숙 run E2E로 실재).** 이 트리·모든 하위 데이터의 **정본 문면(형태 A)**은 본 문서가 소유하며, 실제 디렉터리·데이터 파일은 성숙 run E2E로 생성되어 현행 `uahf/framework/adapters/claude/solution-design-data/` 아래 실재한다(§12 실측 대조·L-07 · 물리 위치는 2차 산출물 디커플링 트랙에서 확정). 본 문서는 경로·구조·형식의 정본 문면을 소유한다.

---

## §4. DP-2 — 실행 기록 직렬화·최소 레코드 어휘 확정 (done 4)

04 §3.2("판정 근거 기록")·§3.7(물리 배치 Adapter 위임)의 실현으로, 성숙 run의 **실행 기록**을 append-only 로그로 직렬화하는 형식과 **최소 레코드 종류**를 확정한다. State Machine 상태·전이(04 §3.4)는 재정의하지 않고 § 포인터로 인용하며, 물리 직렬화 형식·레코드 어휘만 확정한다.

### §4.1 확정 — 자기서술 구조화 레코드 append-only 로그 (1 사건 = 1 레코드)

**한 성숙 run 1건의 실행 기록 = 발생 순서대로 append되는 자기서술 구조화 레코드의 로그**로 직렬화한다(`events.jsonl` 동형 — discovery-binding §3.2 append-only 로그 관례 동형). **1 사건 = 1 레코드**이며, 레코드는 발생 순서대로만 추가된다(append-only). 구체 구조화 데이터 형식은 Adapter 선택이다(격리 지점 — 이식 교체 §10).

- **레코드 최소 표면.** 각 레코드는 최소한 (i) **레코드 종류**(§4.3의 어휘 중 하나), (ii) **순서 값**(아래 §4.2), (iii) **레코드별 페이로드**를 담는다. 페이로드 내부 구조는 이 직렬화가 해석하지 않는 불투명 페이로드로 그대로 담긴다.
- **append-only 불변.** 기록된 레코드는 재작성·삭제하지 않는다. 정정·후속 상태는 새 레코드 append로 표현된다. `Reconciling`→`Proposing` 재제안(T5), `Reviewing`→`Reconciling` 잔여 충돌 재노출(T7), `Validating`→`Reviewing` 수정 재진입(T10), 임의 비종단→`Escalated`(T11)도 각각 하나의 레코드로 append된다(04 §3.4-B — 재정의 0).
- **"기록만으로 run 재구성".** 로그의 레코드 순서(= append 순서 = 전이 순서)만으로 해당 성숙 run의 State Machine 진행(`Assessing` 생성 → 전이 → 종단)이 재구성된다.

### §4.2 순서 값과 물리 생성 시각의 성격 구분 (L-09)

기록 필드의 **순서 값**과 **물리 생성 시각**의 성격을 형식에서 구분해 명시한다(Active Lesson L-09 — discovery-binding §3.3 `seq` 순서 값 관례 동형).

- **순서 값(정본 표면).** 각 레코드는 단조 증가하는 **순서 값**(`seq`)을 갖는다. 이 값이 로그 내 레코드 순서(= 전이 순서)를 확정한다. 로그의 순서는 언제나 이 순서 값(= append 순서)에서 도출되며, 벽시계 시각에서 도출하지 않는다.
- **물리 생성 시각(별도 필드·실측 성격).** 레코드가 벽시계 생성 시각을 함께 담는 경우, 그것은 **순서 값과 별개의 필드**이며 그 값의 진위는 **실측 대조 후에만** 참으로 취급되는 측정 주장이다(L-09). 물리 생성 시각은 로그의 순서를 결정하지 않는다 — 순서 결정은 순서 값 전속이다.

### §4.3 최소 레코드 종류 (Adapter 기록 관례 — 새 코어 계약 요소 창설 0)

성숙 run의 실행 기록을 담는 **최소 레코드 종류**를 이 Adapter의 **기록 관례**로 명명 확정한다. **이 명칭은 이 Adapter의 기록 관례일 뿐이며 04·03 코어 계약의 상태·전이·불변·필드·kind를 창설·재정의하지 않는다** — 상태·전이 라벨은 04 §3.4 정본을 payload에 인용할 뿐이다. **Discovery Event 15종(02 §3.5 소유·Discovery 도메인 전속)의 명칭은 차용하지 않는다** — 명칭 재사용이 곧 의미 파괴이므로 SD 고유 어휘로 명명한다.

| 레코드 종류 (기록 관례) | 담는 것 | 인용하는 04 정본 |
|---|---|---|
| `MaturationRunStarted` | run 시작·입력 결속 — 입력 인스턴스 경로(vN)·`instanceVersion`·사용한 policy 참조·초기 상태 `Assessing`. 별도 Request 형식을 신설하지 않고 이 레코드가 입력 결속을 담는다(최소 변경). | §3.1-B 입력(Ready\|ReadyWithAssumptions vN)·§3.4-A `Assessing` 생성 |
| `StateTransition` | 상태 전이 1건 — payload에 전이 라벨(T1~T11)·`from`/`to` 상태(`Assessing`·`Proposing`·`Reconciling`·`Reviewing`·`Validating`·`Matured`·`Skipped`·`Escalated`)를 **04 §3.4 정본 그대로 인용**. | §3.4-A 상태·§3.4-B 전이표 T1~T11 |
| `GatePresented` | 사용자 게이트 제시 — `Validating`에서 성숙 결과(또는 스킵 판정)를 사용자에게 제시한 사건. | §3.4-A `Validating`·§3.4-D ⑥ |
| `UserResponded` | 사용자 게이트 응답 — 승인/확인/수정/강제 응답 수령(T8/T9/T10/T11 유발). 제시(`GatePresented`)와 응답을 각각 레코드로 남긴다. | §3.4-B T8·T9·T10·T11 |
| `OutputRecorded` | 산출 기록 — 성숙 경로 종단 시 superseding 인스턴스 경로(contract-binding §4.2)·선택 Projection 목록 참조. Proposal·충돌/trade-off·리뷰 상세는 실행 메타 파일 참조로만 가리킨다(코어 밖·SP-INV 2·3). | §3.1-C 출력·§3.4-C 단일 인스턴스 수렴 |
| `MaturationRunConcluded` | run 종결 — 종단 상태(`Matured`/`Skipped`/`Escalated`)와 종결 사유. | §3.4-A 종단 3 |

- **의미 소유 경계.** 위 레코드 종류는 **직렬화 어휘**일 뿐이며, 상태·전이·종단의 의미·Guard는 04 §3.4 전이표가 소유한다(재정의 0). 본 어휘는 04 상태·전이를 payload에 인용해 담을 뿐 새 상태·전이·종단을 창설하지 않는다.
- **스킵 경로 기록.** 스킵 경로도 무기록이 아니다 — `Assessing`에서 스킵 판정 시 `StateTransition`(T2 `Assessing`→`Validating`)·`GatePresented`/`UserResponded`(경량 확인)·`StateTransition`(T9 →`Skipped`)·`MaturationRunConcluded`가 남고, 스킵 판정 근거는 `Assessing` 판정 레코드(또는 실행 메타 파일)에 남는다(04 §3.2 "스킵 판정과 그 근거는 기록으로 남긴다"). 무산출이되 판정 기록은 남는다.

---

## §5. DP-4 — 사용자 게이트 제시·응답 채널 확정 (done 5)

04 §4.1 행2("성숙/스킵 결과 제시와 승인/확인/수정 응답을 받는 개입 채널")의 물리 실현을 확정한다. `Validating` 상태·전이(04 §3.4 T8~T11)·SP-INV 4는 재정의하지 않고 § 포인터로 인용하며, 물리 개입 채널만 확정한다. **discovery-binding §5 사용자 확인 채널(주 세션 제시·응답)이 선행 관례이며, 본 절은 그와 동형으로 서술한다.**

### §5.1 물리 채널 — 주 세션 사용자 제시·응답 수령

- **제시·수령 채널.** Solution Design의 모든 사용자 개입(`Validating`에서 성숙 결과·스킵 판정 제시, 승인/확인/수정/강제 응답 수령)은 **주 세션**(Advisor 바인딩)에서 사용자에게 제시되고 사용자 응답을 수령한다. 이는 discovery-binding §5(loop-binding §5.2 계보)가 확정한 사람 개입 물리 채널과 동형이다. 주 세션은 Orchestrator 역할(§6)로 State Machine을 구동하는 주체이기도 하므로, State Machine 구동과 사용자 개입 제시가 같은 주 세션 채널에서 정합한다.

### §5.2 게이트 전이 실의미 (T8·T9·T10·T11)

`Validating`의 사용자 응답이 유발하는 네 전이의 물리 실의미를 확정한다. 각 제시·응답은 §4 로그에 `GatePresented`·`UserResponded` 레코드로 남고, 뒤이은 전이는 `StateTransition` 레코드로 남는다.

| 사용자 응답 | 전이 (04 §3.4-B) | 실의미 |
|---|---|---|
| **승인** | T8 `Validating`→`Matured` | 성숙 경로 확정 — superseding v(N+1) 발행(contract-binding §4.2 경로) + 선택 Projection. `OutputRecorded`·`MaturationRunConcluded`(Matured). |
| **확인** | T9 `Validating`→`Skipped` | 스킵 경로 확정 — 무산출(vN이 곧 UAHF 소비 대상)·스킵 판정 기록만. `MaturationRunConcluded`(Skipped). |
| **수정 요청** | T10 `Validating`→`Reviewing` | 추가 설계 필요 — `Reviewing` 재진입. 종단 아님. |
| **강제** | T11 임의 비종단→`Escalated` | 사용자 강제(또는 자율 수렴 불가) — 상위(사람) 판단 위임. `MaturationRunConcluded`(Escalated·미완). |

- **승인 전 Matured 도달 불가(SP-INV 4·불가침).** `Matured`·`Skipped` 종단은 반드시 `Validating`의 사용자 응답(T8·T9)을 통과한다 — 사용자 승인/확인 게이트 없이 성숙·스킵 종단에 도달하지 않는다(04 §3.8 SP-INV 4·UAF-INV ⑤). 로그 순서상 `UserResponded`(승인/확인) 레코드가 `StateTransition`(T8/T9 →Matured/Skipped)에 **선행**한다 — 이 순서가 게이트 불가침의 물리 증거다. 본 채널 바인딩은 이 게이트를 물리 채널로 실현할 뿐 판정식·전이표를 재정의하지 않는다.
- **강제 일시중단·재개 semantics.** 04 §4.1 행2가 포함한 "강제 일시중단·재개 semantics"는 T11 `Escalated` 위임으로 실현된다 — 04 §3.4는 `Escalated`를 종단으로 두므로, 물리 재개(에스컬레이션 이후 재착수)의 상세 semantics는 상위(사용자·Advisor) 판단 소관이며 본 문서는 별도 재개 상태기계를 신설하지 않는다(04 §3.1-D Handoff 의미론·§3.9 확장 포인트 정합·선취 금지).

---

## §6. DP-3 — Expert Role 실행 호스팅 (역할 추상까지만) (done 6)

04 §4.1 행1의 물리 실현을 확정하되, 정본이 명시한 대로 **역할 추상까지만** 확정하고 물리 호스팅(실행 코드·자동화)은 **설계하지 않는다**. 04 §4.1 행1 정본: "논리 Expert Role을 어느 실행 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(M5)." **discovery-binding §7(Strategy 실행 호스팅 역할 추상)이 선행 관례이며, 본 절은 그와 동형으로 서술한다.**

### §6.1 역할 추상 확정 (형태 A — 규약 절차·기존 위임 관행 재사용)

- **Orchestrator 역할 = 주 세션 규약 절차.** State Machine(04 §3.4)을 구동하는 역할을 **주 세션(Advisor)이 규약 절차로 수행**한다 — Ready 인스턴스 vN 결속으로 `Assessing`을 생성하고, 복잡도 판정(04 §3.2)·역할 할당(04 §3.3)·전이 집행·종단 판정(04 §3.1-D)·사용자 게이트(§5)를 규약 절차로 실현한다. 전이 규칙을 새로 만들지 않는다(04 §3.4 정본 — 재정의 0).
- **Expert Role 수행 = 기존 위임 실행 관행 재사용.** 논리 Expert Role(04 §3.3 — Capability 선언·개방 네임스페이스)을 어느 실행 주체가 호스팅하는가는, **이 환경의 기존 UAHF Agent 위임 실행 관행**(서브에이전트 위임·완료 보고·독립 검증)을 재사용해 실현한다 — `Proposing`의 역할별 Proposal 산출을 위임 실행으로, 산출 회수를 완료 보고로, `Reconciling`·`Reviewing`의 통합을 주 세션 Orchestrator 규약 절차로 수행한다. **새 병렬 실행 프레임워크를 창설하지 않는다** — 기존 위임 관행의 재사용이다.
- **최소 할당·개방 네임스페이스 유지.** 실행 주체 할당은 복잡도 판정 결과가 식별한 관심사에서 파생된 **최소 구성만** 할당한다(04 §3.3 최소 할당·§3.8 SP-INV 8). 고정 역할 팀을 상시 실행하는 구조를 만들지 않으며(SP-INV 5·8), 역할명은 개방 네임스페이스로 유지한다 — 본 절은 구체 역할명 카탈로그를 명명하지 않는다(04 §3.3·UAF-INV ⑥ — 정본 청정). 구체 역할 예시는 비정본 부록 소관이다(04 §3.8 SP-INV 5).
- **물리 호스팅 = 설계 안 함(확장 포인트).** Solution Design을 실행 코드로 자동 호스팅하는 물리 실행 주체·자동화(형태 B 실행 호스팅·step 실행기 연결)는 **설계하지 않는다** — 이는 04 §3.9 확장 포인트이며, 여기서 설계하면 04 §4.1 행1("물리 호스팅은 설계하지 않는다")과 04 §3.9를 침범한다. 실행 코드는 형태 B로 미도입이며, 그 경계 간 분할은 형태 B 설계 시 확정한다(선취·추측 금지).

### §6.2 코어 문면 무촉·SP-INV 6 무촉

- **04 코어 문면(역할 추상) 무촉.** 본 절의 물리 매핑은 04 §3.3 "실행 주체 매핑은 Adapter 소관(M5)·코어는 역할 추상까지만"이 위임한 지점에만 놓인다. 코어는 UAHF Agent·특정 하네스 실행 주체를 역참조하지 않으며(04 §3.8 SP-INV 6·루트 §2.5 폐쇄성), 본 절이 그 위임 지점을 채워도 04 코어 문면(역할 추상)은 무촉이다 — 물리 매핑은 이 격리 지점에만 존재한다. `Reviewing`의 통합·단일 일관 결정 집합 수렴·최종 결정 소유권(권위 = 사용자 게이트)은 04 §3.4-C 정본 그대로이며, 본 절은 그 실행 주체 매핑만 확정한다.

---

## §7. DP-5 — Policy 데이터 소스·직렬화 + 최소 실값 (done 7 · DP-X5 동형)

04 §4.1 행4("판정 임계·역할 선택 규칙·Projection 유형 선택 정책의 데이터 소스·직렬화 — Policy as Data")의 물리 실현을 확정한다. 복잡도 판정(04 §3.2 Policy as Data)·역할 할당(04 §3.3)·Projection 동적 선택(04 §3.5)은 재정의하지 않고 § 포인터로 인용하며, 데이터 소스·직렬화 형식과 **최소 실값 1세트**만 확정한다. **discovery-binding §8(Policy 값 데이터 소스·최소 실값)이 선행 관례이며, 본 절은 그와 동형으로 서술한다.**

### §7.1 데이터 소스·직렬화 형식

- **데이터 소스.** Solution Design Policy 값은 규약 절차에 하드코딩되지 않고 `uahf/framework/adapters/claude/solution-design-data/policy/`의 **데이터 파일**(`default-policy.yaml`)에서 온다(Policy as Data, 04 §3.2). 값 조정은 데이터 정정일 뿐 Orchestrator 규약 절차·정본 계약(04 §3.2·§3.3·§3.5)을 변경하지 않는다.
- **직렬화 형식.** 정책 파일은 자기서술 구조화 데이터로 직렬화한다(자매 discovery-binding §8.1 구조화 데이터 관례 동형·구체 형식은 Adapter 선택, 격리 지점 §10). 물리 정책 데이터 파일(`policy/default-policy.yaml`)은 성숙 run E2E로 실재하며, 본 문서는 **형식·값 정본 문면**을 소유한다(L-07).

### §7.2 최소 실값 1세트 (정본 값 표 — DP-X5 동형)

E2E 구동을 위한 **최소 실값 1세트**를 본 문서의 정본 값 표로 확정한다. 이 값들은 **Policy as Data**이므로 값 조정은 데이터 정정일 뿐 정본 계약을 변경하지 않는다(04 §3.2). 04 §4.1 행4가 위임한 세 정책(복잡도 판정·역할 선택·Projection 선택)을 채운 단일 기본 프로파일이다.

**(가) 성숙/스킵 판정 기준 (04 §3.2 — 산출은 이진 분기, 판정 기준은 정책 데이터):**

아래 신호 중 하나라도 참이면 **성숙 필요**(→ 역할 할당·`Proposing`), 전부 부재이고 단일 관심사이면 **스킵**(→ `Validating` 경량 확인·T2→T9). 신호는 입력 인스턴스 vN(및 워크스페이스 증거)에서 판정된다.

| # | 성숙 필요 신호 | 근거 필드 (03 §3.2-A) |
|---|---|---|
| 1 | `architectureDirection.open` 비공집합 (미결 설계 결정 존재) | 그룹 6 Architecture Direction |
| 2 | `readiness.openQuestions` 비공집합 (미해결 질문 존재) | 그룹 8 Readiness |
| 3 | `assumptionLedger` 비공집합 (미해결 가정 존재 — ReadyWithAssumptions) | 그룹 7 Assumption Ledger |
| 4 | 다관심사 지표 (설계 관심사 2개 이상 교차) | 판정 근거 종합 |
| 스킵 | 위 1~4 전부 부재 ∧ 단일 관심사 | vN이 곧 UAHF 소비 대상 — T2 `Assessing`→`Validating`, T9 확인→`Skipped` |

**(나) 역할 선택 규칙 (04 §3.3 — Capability 선언·개방 네임스페이스·최소 할당·전체 커버리지 바닥):**

| 항목 | 값 (`roleSelection`) |
|---|---|
| 파생 근거 (`basis`) | 판정 근거가 식별한 설계 관심사(위 (가) 신호가 가리키는 미결 관심사) — 관심사에서 역할을 파생 |
| 관심사당 역할 (`perConcern`) | 최소 1 (관심사당 최소 필요 역할만) |
| 전문 역할 수 상한 (`maxSpecialistRoles`) | **4** — 전문/관심사 역할만 상한, 불필요한 다중 역할 구성을 강제하지 않는다(SP-INV 8). 기본 2(`baseSpecialists`) + 조건부 2(`conditionalSpecialists`)를 담을 여유값이며, 전체 커버리지 바닥(`coverageFloor`)은 이 상한에 **불산입**(§DC-6 configurable). |
| 기본 역할 구성 (`defaultComposition`) | **강제 기본값(이탈 시 사유 기록)** — `coverageFloor`(전체 커버리지 바닥 실현) + `baseSpecialists`(기본 전문역할) + `conditionalSpecialists`(조건부 편입: 접점 선언·데이터 복잡 등 신호 충족 시). 이는 **책임 있는 자율**(루트 ARCHITECTURE.md §6 원칙 11 (a)(b))의 물리 실현 — 빠지면 안 되는 기본 구성을 비정본 부록이 아니라 **Policy 기본값으로 강제**하되, 그것이 **고정 고정팀은 아니다**(`fixedTeam=금지`와 무모순 — 기본값이지 강제 고정팀이 아님·SP-INV 8 최소할당 존치). 역할명은 **개방 네임스페이스 예시**이며 configurable(§DC-6). 구체 역할 예시·소유 산출물은 비정본 부록(expert-role-catalog.md §3.5) 소관이다(SP-INV 5). |
| 이탈 규칙 (`deviationRule`) | **silentOmission 금지**(책임 있는 자율 (b)(c)) — 기본 구성에서 역할 추가/제거 시 **사유 기록**(성숙 run 기록 `events/maturation-<run-id>/`) + **Validating 게이트 표면화·사용자 확인**(고임팩트 이탈은 즉시). "기본값이니 조용히 이탈"을 폐기한다. |
| 전체 커버리지 바닥 (`wholeScopeCoverage=required`) | **필수 바닥** — 선언된 전체 프로젝트 범위를 관장하는 커버리지 capability를 반드시 포함한다(04 §3.3·§3.8 SP-INV 9). `defaultComposition.coverageFloor`(PM 예시)가 이 바닥을 실현한다. 최소 할당(SP-INV 8)의 예외가 아니라 그 위의 필수 바닥이며 전문 역할 상한에 **불산입**된다 — 두 원칙은 **층위가 다르다**(04 §3.3 인용: 최소 할당은 각 좁은 관심사에 대해 전문 역할을 필요 이상으로 늘리지 않음을, 커버리지 바닥은 그와 독립적으로 선언 범위 전체가 관장 없이 비는 일이 없음을 규율 — 모순 아님). 커버리지 capability도 고정 역할명이 아니라 Capability 선언으로 표현된다(개방 네임스페이스·SP-INV 5). |
| 역할→산출물 소유 맵 (`artifactOwnership`) | 각 `defaultRequiredSet` id의 소유 역할(작성 책임) — `defaultComposition`과 동일 개방 네임스페이스 예시로 10 id를 1:1 매핑(PM=project-plan+횡단 완결성 / 기획=requirements-def·business-process·functional-spec·test-plan-cases / 아키텍처=table-def·interface-spec, DBA 보조 / 디자이너=screen-list·menu-structure·screen-design). 생산 프로토콜은 §7A. |
| 고정 팀 열거 (`fixedTeam`) | **금지** — 역할명은 개방 네임스페이스, 고정 역할 카탈로그 0(SP-INV 5·UAF-INV ⑥). `defaultComposition`은 이 금지의 예외가 아니라 "이탈 가능한 기본값"이므로 무모순(위 참조). |

**(다) Projection 선택 정책 (04 §3.5 — 동적 선택 = 기본값 opt-out·전 유형 강제 금지·SP-INV 9 기본 필수 세트):**

| 항목 | 값 (`projectionSelection`) |
|---|---|
| 선택 방식 (`mode`) | 프로젝트 유형·복잡도에 따라 **동적 선택** — 04 §3.5의 '동적'은 기본값 opt-in이 아니라 **기본값으로부터의 정당화된 이탈(opt-out)**이다 |
| 전 유형 강제 (`forceAllTypes`) | **금지** — 개방 레지스트리의 모든 가능 유형을 강제하지 않는다. `defaultRequiredSet`(부분집합)의 default-required와 **무모순**(04 §3.5) |
| 정본 실재 시 (`existingCanonical`) | 대상 워크스페이스에 해당 유형 정본이 **이미 실재하면 신규 강제 0**(04 §3.5 동적 선택) |
| 유형 카탈로그 (`typeCatalog: open-registry`) | 코어(04)는 유형 카탈로그를 알지 않으나(SP-INV 5는 코어만 구속), 본 Adapter Policy는 격리 지점(§0)으로서 **기본 필수 세트를 구체 열거**한다(04 §4.1 행4 Policy as Data 위임). 개방 레지스트리 전체 카탈로그는 여전히 부록 소관이며, `defaultRequiredSet`은 그중 성숙 경로 default-required 부분집합(04 §3.5 opt-out·SP-INV 9)이다. |

**기본 필수 Projection 세트 (`defaultRequiredSet` — 성숙 경로 default-required 부분집합 · `policy/default-policy.yaml`과 정확히 일치):**

| id | 이름 (`name`) | 요건 클래스 (`requirement`) |
|---|---|---|
| `project-plan` | 프로젝트 계획서 | `always` |
| `requirements-def` | 요구사항 정의서 | `always` |
| `business-process` | 업무 프로세스 | `always` |
| `functional-spec` | 기능 명세서 | `always` |
| `table-def` | 테이블 정의서 | `always` |
| `test-plan-cases` | 테스트 계획·케이스 | `always` |
| `screen-list` | 화면 목록 | `touchpoint` |
| `menu-structure` | 메뉴 구조도 | `touchpoint` |
| `screen-design` | 화면 설계서 | `touchpoint` |
| `interface-spec` | 인터페이스 명세서 | `interface` |

**요건 클래스 (`requirementClasses`):**

| 클래스 | 의미 |
|---|---|
| `always` | 항상 default-required — 제외는 설계단계 명시 결정 + 사유 기록 + 사용자 확인만 |
| `touchpoint` | 접점(웹·앱·포털) 선언 시 required — 미선언 시 자동 N/A |
| `interface` | 외부 연계 선언 시 required — 미연계 시 자동 N/A |

**제외 규칙 (`exclusionRule` — SP-INV 9 침묵 누락 금지):**

| 규칙 | 값 |
|---|---|
| `silentOmission` | **금지** — 산출도 제외 기록도 없이 구현 경계를 넘기지 않는다(04 §3.8 SP-INV 9) |
| `autoExclude` | touchpoint/interface 미충족 → 자동 N/A |
| `manualExclude` | `always` 클래스 제외 시 사유 기록 + 사용자 확인 — 성숙 run 기록(`events/maturation-<run-id>/`)에 남긴다 |

- **Policy as Data 불변.** 위 값(판정 신호·역할 선택 상한·Projection 정책)은 전부 데이터이며, 값을 바꾸는 것만으로 성숙 거동이 조정된다 — Orchestrator 규약 절차나 정본 계약(04 §3.2·§3.3·§3.5·SP-INV)은 변경되지 않는다. 이 값 세트는 **E2E 구동을 위한 최소 실값**이며, 다른 임계·상한이 필요하면 `policy/` 데이터 정정으로 조정한다.
- **실측 기반 구분(L-07).** 위 값은 본 문서가 소유하는 **정본 값 문면(형태 A)**이며, 물리 데이터 파일(`solution-design-data/policy/default-policy.yaml`, 현행 `uahf/framework/adapters/claude/…`)은 성숙 run E2E로 이 값 기반으로 실재한다(§12 실측).

---

## §7A. 산출물 생산 프로토콜 (form-A 규약 — 주 세션이 따르는 절차)

Solution Design이 **기본 필수 Projection 세트(§7.2 (다))를 어떻게 생산하는가**의 절차를 form-A 규약으로 확정한다. 이 절은 **실행 코드가 아니라 주 세션(Advisor)이 따르는 규약 절차**이며(§0 형태 A), 04 §3.3 역할 할당·§3.4 협업 프로토콜·§3.5 Projection·§3.8 SP-INV 7·9를 재정의하지 않고 § 포인터로 인용한다. 물리 실현은 §6(역할 추상 호스팅)·§7(Policy)·§4(기록)·§5(게이트) 위에 얹힌다. 절 번호를 `§7A`로 둔 것은 이후 §8~§14 번호·교차참조를 보존하기 위한 무침습 삽입이다.

**책임 있는 자율 정합(루트 ARCHITECTURE.md §6 원칙 11).** 이 프로토콜은 (a) 필수 산출·전 범위 커버를 Policy(§7.2 (다) `defaultRequiredSet`·`requirementClasses`)와 게이트(§5·`design_completeness` 체커)로 강제하고, (b) 남은 자율은 Policy 기본값(§7.2 (나) `defaultComposition`·`artifactOwnership`) + 이탈 시 사유 기록(`deviationRule`)으로 두며, (c) 이탈·제외를 Validating 게이트에서 일괄 표면화한다. 부록(expert-role-catalog.md)은 **예시 문서일 뿐 강제 근거가 아니다**(원칙 (a)).

### §7A.1 위임 산출 (역할별 소유 산출물 · 컨택스트 위생)

- **각 역할 = 위임 서브에이전트가 자기 소유 산출물 작성.** `Proposing`(04 §3.4-A)에서 각 Expert Role(§7.2 (나) `defaultComposition`)은 **fresh-context 위임 서브에이전트**로 수행되어, `artifactOwnership`(§7.2 (나)·Policy (라))이 지정한 **자기 소유 산출물만** 작성한다. 이는 §6.1이 확정한 "Expert Role 수행 = 기존 위임 실행 관행 재사용(서브에이전트 위임·완료 보고·독립 검증)"의 산출물 생산 국면 실현이다.
- **주 세션은 조율·검증만·내용 직접 작성 안 함.** 주 세션(Advisor)은 Orchestrator 규약 절차(§6.1)로 역할 파생·디스패치·`Reconciling`/`Reviewing` 통합·게이트만 수행하고, **산출물 본문을 직접 작성하지 않는다** — 컨택스트 위생(§6.1 역할 추상 호스팅 정합·주 세션 컨택스트를 산출물 본문 생성으로 오염시키지 않음). 이는 04 §3.4-C 최종 결정 소유권(권위 = 사용자 게이트)과 무모순이다 — 주 세션은 통합·수렴만, 본문 생산은 위임.
- **최소 할당 존치.** 위임 대상 역할은 `defaultComposition` 기본값에서 복잡도 판정이 요구하는 만큼만 편입되며(조건부 역할은 신호 충족 시), 이탈은 `deviationRule`로 기록된다(SP-INV 8·§7.2 (나)).

### §7A.2 형식·배치 (Markdown 본문 + 기계 색인 매니페스트)

- **본문 = Markdown(사람+AI 겸용·중복 0).** 각 산출물 본문은 사람과 AI가 함께 읽는 단일 Markdown 문서로 `<workspace>/docs/*.md`에 배치한다(같은 내용을 다른 형식으로 중복 저장하지 않는다).
- **기계 색인 = `design-manifest.json`.** 산출/제외 상태의 기계 판독 색인은 `design-manifest.json`(orchestration/adapters/claude/design-manifest.schema.md 스키마)이며, `artifacts[].id`는 `defaultRequiredSet[].id`와 대응한다. 소유 역할 매핑의 정본은 Policy `artifactOwnership`이고, 매니페스트는 각 id의 `produced`/`excluded` 상태를 기록한다(체커 소비 표면).
- **구조화 사이드카 = 다운스트림 소비 시에만.** 구조화 사이드카(예: `table-def`의 `schema.json`)는 **다운스트림 코드생성이 실제 소비할 때에만** 산출한다 — 무조건 산출하지 않는다(불필요 산출 방지·Markdown 본문이 1차 정본).
- **배치 스코프(SP-INV 7 워크스페이스 귀속).** 본문은 `<workspace>/docs/`, 매니페스트는 `<workspace>/.claude/solution-design/design-manifest.json`에 둔다 — **대상 워크스페이스 귀속**이며 성숙 run 디렉터리(`solution-design-data/events/…`)가 아니다(04 §3.7 SP-INV 7·design-manifest.schema.md 배치 위치 정합). run 디렉터리에는 실행 메타·이벤트 로그만(§3·§4), 산출물 본문·매니페스트는 워크스페이스에.

### §7A.3 검증 3층 (CP1→CP2→CP3 + 사용자 게이트)

산출물 검증은 3층으로 쌓이며(02-agent §3.2 CP1·CP2·CP3 동형), 각 층의 검사 범위(scope)는 정직하게 구분된다.

| 층 | 주체 | 검사 대상·근거 |
|---|---|---|
| **CP1** | 각 역할(위임 서브에이전트) | 자기 소유 산출물 자체점검 — 소유 산출물의 done 항목 충족. 자체 점검은 최종 승인이 아니다. |
| **CP2** | 전체 커버리지 역할(PM 예시·`coverageFloor`) + `design_completeness` 결정적 체커 | 횡단 완결성 판정 — 선언 범위(접점·연계) 대비 기본 필수 세트 커버/정당화 제외를 매니페스트 기준으로 결정적 검증(침묵 누락 차단·SP-INV 9). |
| **CP3** | Advisor(주 세션) | 최종 승인 — 매니페스트·커버리지 리포트 기반 승인이며 **전 산출물 전수 정독이 아니다**(컨택스트 위생·CP2 결정적 판정에 위임). |

- 3층 위에 **Validating 사용자 게이트**(§5·04 §3.4 T8~T11)가 놓인다 — 최종 성숙/스킵은 사용자 응답을 통과한다(SP-INV 4·불가침).
- CP2의 `design_completeness` 결정적 체커는 매니페스트를 **판독만** 한다(design-manifest.schema.md 소유 경계 — 산출은 SD, 검증은 오케스트레이션).

### §7A.4 사용자 컨펌 시점 (책임 있는 자율 (c) 정합)

기본 필수 세트로부터의 이탈·제외에 대한 사용자 확인 시점을 세 지점으로 확정한다.

| # | 시점 | 실현 |
|---|---|---|
| (i) | **제외 발생 시 inline** | `always` 클래스 산출물을 제외할 때 매니페스트 `confirmedBy`에 사용자 확인을 즉시 기록(design-manifest.schema.md `excluded` 요건·§7.2 `manualExclude`). |
| (ii) | **Validating 게이트 일괄** | 성숙 종단 직전 Validating(§5)에서 **전체 산출물 + 매니페스트를 일괄 제시·승인**(§7.2 `deviationRule.surface`). |
| (iii) | **고임팩트 이탈 즉시** | 기본 구성·필수 세트에서의 고임팩트 이탈은 (ii)를 기다리지 않고 즉시 표면화(원칙 11 (c) "고임팩트는 즉시"). |

이 세 지점은 silentOmission 금지(SP-INV 9·`exclusionRule.silentOmission=금지`)의 사용자 개입 실현이며, 04 §3.4·§3.8 SP-INV 4·9를 재정의하지 않는다.

---

## §8. Provenance 성숙 run 내부 형식 확정

contract-binding §6은 Contract 인스턴스 front-matter 내 분리 네임스페이스 `provenance` 컨테이너의 **외형·must-ignore 경계**만 확정하고, discovery-binding §10은 그 내부를 **Discovery run** 실행 메타로 확정했다. superseding **성숙 인스턴스**의 `provenance`는 성숙 run에서 유래하므로, 본 절이 그 **성숙 run 내부 형식**을 확정한다(discovery-binding §10이 Discovery run 내부 형식을 확정한 것과 동형·경계 침범 0).

### §8.1 성숙 run 내부 형식 (최소 표면)

성숙 경로로 재발행되는 superseding 인스턴스 v(N+1)의 `provenance` 컨테이너 내부는 **성숙 run 실행 메타**를 담는 자기서술 구조화 블록이다. 최소 구성:

| 내부 필드 (성숙 run 실행 메타) | 값 형태 | 참조 대상 |
|---|---|---|
| run 식별자 | 문자열 — 해당 성숙 run(State Machine 인스턴스, 04 §3.4-A)의 `<run-id>` | `solution-design-data/events/maturation-<run-id>/`(§3·§4) |
| 이벤트 로그 참조 | 참조 — 이 run의 append-only 기록 로그 디렉터리 경로/참조(§4) | DP-2 백엔드(§4) |
| 기준선 vN 참조 | 참조 — 성숙의 기준선이 된 Ready 인스턴스 vN(= `meta.supersedes`가 가리키는 인스턴스) | contract-binding §4.2·§5 `supersedes` |
| Policy 참조 | 참조 — 이 run이 사용한 Solution Design Policy 참조(§7) | `solution-design-data/policy/`(§7) |

- 위는 **최소 표면**이며, 감사·재현에 필요한 추가 성숙 실행 메타(예: 종단 상태·역할 구성 요약 참조)를 담을 수 있다. 어느 필드도 경량 **참조**이며, 이벤트 로그·Proposal 원문을 컨테이너에 중복 저장하지 않는다(loop-binding §5.3 경량 참조 관례 동형).

### §8.2 contract-binding §6 외형·must-ignore 경계 유지 (재정의 0)

- **must-ignore 경계 불변.** UAHF tolerant reader는 `provenance` 컨테이너(및 그 하위 전체)를 **must-ignore**한다 — 존재를 오류로 취급하지 않고 소비하지 않는다(contract-binding §6·03 §3.2-D·§3.3-C·PC-INV 3·5). 본 절이 성숙 run 내부 형식을 채워도 이 must-ignore 경계는 불변이다. 내부 필드는 **성숙 활동 측 소비 전용**(감사·재현·계보 추적)이며, UAHF는 이 컨테이너를 읽지 않는다.
- **누출 차단(SP-INV 2·3).** 성숙 run 실행 메타(run 식별자·이벤트 로그 참조·기준선 vN 참조·Policy 참조)는 Contract **코어 필드**(Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger)로 새어나가지 않는다 — 성숙 내부 개념(복잡도 판정·역할 구성·Proposal·충돌 기록)은 코어 밖 불투명 실행 메타이며(04 §3.8 SP-INV 2·3·PC-INV 2·10), `provenance`와 실행 메타 파일에만 반영된다.
- **창설 금지.** 본 절은 03 §3.2-D 불투명 부속 계약·contract-binding §6 외형·must-ignore 경계를 재정의하지 않고 그 **성숙 run 내부 형식만** 채운다. Contract 코어 스키마·버저닝·tolerant reader 계약을 변경하지 않는다(contract-binding §3·§5·§6 소유·재정의 0).

---

## §10. 04 §4.2 이식 교체 지점 대응 (done 8)

04 "### 4.2 이식 교체 지점"의 교체 지점 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 04 §3 Core Contract 불변(structure.md §7 C-1 동형)을 재확인한다. 04 §4.2 정본: "실행 호스팅·게이트 채널·저장 위치·Policy 실값 → 대상 환경의 실행/개입/저장/정책 메커니즘. **유지되는 것**: §3.1 단계 계약, §3.2 판정 형태, §3.3 역할 추상, §3.4 프로토콜 골격, §3.5 Projection 관계, §3.6 경계 기준, §3.8 SP-INV."

| 04 §4.2 교체 지점 (바뀌는 것) | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (04 §3 불변) |
|---|---|---|---|
| 실행 호스팅 → 대상 환경의 실행 메커니즘 | §6 | 주 세션(Advisor) Orchestrator 규약 절차·Expert Role 수행 = 기존 위임 실행 관행 재사용(역할 추상까지만). | §3.3 역할 추상·개방 네임스페이스·최소 할당(SP-INV 5·8), §3.4-C 최종 결정 소유권. |
| 게이트 채널 → 대상 환경의 개입 메커니즘 | §5 | 주 세션 사용자 제시·응답 수령 채널·T8~T11 게이트 전이 실의미·제시/응답 각 레코드. | §3.1 단계 계약(출력 2경로·사용자 게이트), §3.4 `Validating`·전이표, §3.8 SP-INV 4(UAF-INV ⑤). |
| 저장 위치 → 대상 환경의 저장 메커니즘 | §3, §4 | `solution-design-data/`(실행 메타·이벤트 로그·Policy)·`.claude/solution-design/`(일반 관례)·superseding 인스턴스는 contract-binding §4.2 경로 append(참조 인용). | §3.7 저장 스코프 원칙(워크스페이스 귀속·SP-INV 7), §3.4-C 단일 인스턴스 수렴(SP-INV 2·3), §3.5 Projection 관계. |
| Policy 실값 → 대상 환경의 정책 메커니즘 | §7 | `solution-design-data/policy/default-policy.yaml` 형식·최소 실값 1세트(성숙 판정·역할 선택·Projection 선택). | §3.2 판정 형태(Policy as Data), §3.3 역할 추상, §3.5 Projection 동적 선택, §3.6 경계 기준. |

- **"유지되는 것" 열의 이식 불변성.** 위 계약(§3.1 단계 계약·§3.2 판정 형태·§3.3 역할 추상·§3.4 프로토콜 골격·§3.5 Projection 관계·§3.6 경계 기준·§3.8 SP-INV)은 다른 AI·실행 환경으로 이식해도 바뀌지 않는다 — 04 §4.2 "유지되는 것" 목록의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 본 문서는 04 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고, v1.4 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §11. 상시 불변 자기 점검 (done 9)

본 물리 바인딩이 04 §3·자매 정본 불변을 훼손하지 않음을 자가 스캔으로 점검한다. 자체 점검은 최종 승인이 아니다 — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다(02-agent §3.2-A). 본 문서에서 "02"는 달리 명시하지 않는 한 discovery/specs/02-discovery.md를 가리키며, Agent 역할 경계는 uahf/specs/02-agent.md다.

### §11.1 재정의 0·새 계약 요소 창설 0

- **04·03·02·루트 재정의 0.** 본 문서의 모든 매핑은 04 §3·§4의 물리 실현이다. 어떤 상태·전이(T1~T11)·SP-INV·단계 계약·복잡도 판정 형태·역할 추상·Projection 관계·경계 기준도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 04 §3이다. 03 스키마·PC-INV, 02 계약, 루트 UAF-INV는 § 포인터로만 인용한다.
- **새 계약 요소 창설 0.** 새 상태·전이·불변·필드·kind를 창설하지 않았다. §4의 레코드 종류 명칭(`MaturationRunStarted`·`StateTransition`·`GatePresented`·`UserResponded`·`OutputRecorded`·`MaturationRunConcluded`)은 이 Adapter의 **직렬화 기록 관례**이며 04·03 코어 계약 요소가 아니다 — 04 상태·전이는 payload에 인용될 뿐이다(§4.3). §7의 Policy 값·§8의 Provenance 성숙 run 내부 필드도 데이터·부속 형식일 뿐 코어 계약 요소가 아니다.

### §11.2 Discovery Event 15종 명칭 차용 0

- **점검 대상(scope).** §4 레코드 종류 어휘 전건.
- **자가 스캔.** §4가 명명한 6종 레코드 종류는 Discovery Event 15종(02 §3.5: `DiscoveryStarted`·`ContextCaptured`·`QuestionAsked`·`AnswerReceived`·`EvidenceRecorded`·`ConfidenceUpdated`·`BudgetConsumed`·`DimensionSaturated`·`AssumptionRecorded`·`ValidationRequested`·`UserOverride`·`ContractCompiled`·`ExecutionReadyDeclared`·`DiscoverySuspended`·`DiscoveryAborted`) 중 **어느 명칭과도 일치하지 않는다** — 특히 게이트 레코드는 Discovery의 `ValidationRequested`가 아니라 SD 고유 `GatePresented`/`UserResponded`로, 강제는 `UserOverride`가 아니라 T11 `StateTransition`으로 명명해 명칭 재사용을 회피했다. Discovery Event 15종 명칭은 본 문서에서 오직 **본 §11.2의 배제 대조**와 근거 정본 § 포인터에만 등장하며(mention), SD 레코드 어휘 정의(use)에는 0건이다.

### §11.3 방법론·역할 카탈로그·타 벤더·모델명 0 (UAF-INV ⑥)

- **자가 전수 스캔.** 본문 전체에 특정 설계 방법론 고유명·타 AI 벤더·모델명이 **0건**임을 자가 스캔했다. §6은 역할을 개방 네임스페이스·Capability 파생으로만 다루고 구체 역할명을 명명하지 않는다(SP-INV 5·6·8·UAF-INV ⑥).
- **역할 기본값의 격리 지점 등재(구체 역할명 ≠ 코어 카탈로그).** §7.2 (나)·§7A는 Policy 기본 역할 구성(`defaultComposition`: PM·기획·아키텍처·디자이너·DBA)과 소유 맵(`artifactOwnership`)의 일반 역할명을 **Policy 데이터·예시로** 인용한다. 이는 §7.2 (다)가 이미 구체 Projection id(`project-plan` 등)를 Policy 데이터로 열거한 것과 **동형의 격리 지점 등재**다 — **SP-INV 5(코어 유형/역할 카탈로그 0)는 코어(04)만 구속**하며, Adapter Policy(격리 지점 §0)가 기본값 데이터로 일반 역할명을 두는 것은 SP-INV 5 위반이 아니다(04 코어 문면은 여전히 역할명 0·§6.2 무촉). 그 역할명은 (i) **강제 고정팀이 아니라 이탈 가능 기본값**(`deviationRule`·`fixedTeam=금지` 무모순), (ii) **개방 네임스페이스 예시·configurable**(§DC-6), (iii) 특정 방법론·벤더·모델 고유명이 아닌 **일반 역할명**이다. 방법론명·벤더·모델명은 Policy 값·본문 어디에도 0건이다.
- **격리 지점 허용 토큰.** 직렬화 형식·물리 경로 `planning/adapters/claude/…`·`uahf/framework/adapters/claude/…`·`.claude/…`·"주 세션"·"Advisor"·"Worker"·"서브에이전트 위임"·Policy 기본값 일반 역할명은 이 Adapter 환경 자체의 토큰이므로 배제 대상이 아니다(C-3 비적용·자매 동형).

### §11.4 mention/use 경계·SP-INV 정합

- **mention/use 경계.** 성숙 내부 개념 어휘(복잡도 판정·역할 구성·Proposal·충돌 기록)는 본 문서에서 오직 (i) 04 정본 § 포인터 인용, (ii) 성숙 **내부** 실현 서술(실행 메타 파일·기록 어휘·Policy 값), (iii) 불변·경계·근거 서술(본 §11·§6.2·§8.2 누출 차단 문면)에만 등장한다. Contract **코어 필드·UAHF 접점**을 정의·확장하는 자리에는 0건이다 — mention과 use의 경계를 지킨다(04 §3.8 SP-INV 2·3·PC-INV 2 동형).
- **SP-INV 정합(전건).** 본 바인딩은 SP-INV 1(입력 Ready 불변 — §4 `MaturationRunStarted` 입력 결속이 Ready vN만 결속)·2·3(코어 유입·실행 메타 불투명 — §3.2 실행 메타 파일·§8.2 누출 차단)·4(사용자 승인 게이트 — §5.2 승인 전 Matured 불가)·5(방법론·카탈로그 불인지 — §11.3)·6(UAHF 무수정·역참조 금지 — §6.2)·7(산출물 워크스페이스 귀속 — §3.1·§3.3)·8(최소 할당 — §6.1·§7.2 (나))·9(설계 커버리지 완성도 — §7.2 (나) 전체 커버리지 바닥·(다) `defaultRequiredSet`·`requirementClasses`·`exclusionRule`)을 물리 실현으로 훼손하지 않는다. 진위 판정 기준은 04 §3.8이다.

---

## §12. 상태 서술 실측 대조 (L-07 — 미존재를 실재로 쓰지 않음)

본 문서의 "실재/미존재" 서술은 파일 시스템 직접 실측 후에만 기입한다(L-07). 현행 물리 위치: 본 문서는 `planning/adapters/claude/`(planning 레이어 어댑터 경계)에, 본 문서가 선언·소유하는 백엔드 데이터 트리는 `uahf/framework/adapters/claude/…` 아래에 있다(물리 위치는 2차 산출물 디커플링 트랙에서 확정).

| 대상 (현행 물리 경로) | 본 문서 서술 | 실측 결과 |
|---|---|---|
| `planning/adapters/claude/solution-design-binding.md` | 실재 (본 문서) | 실재 (이 파일). |
| `planning/adapters/claude/contract-binding.md` (저장·버전·Provenance 외형 소유) | 실재 (§3·§4·§5·§6 참조·경계 인용 대상) | 실재 — § 포인터 대상(무수정). |
| `discovery/adapters/claude/discovery-binding.md` (핵심 골격 선례) | 실재 (§3·§4·§5·§7·§8·§10 골격 선례) | 실재 — § 포인터 대상(무수정). |
| `entry/adapters/claude/entry-binding.md`·`uahf/framework/adapters/claude/`(memory·loop-binding 등) (채널·격리 선례) | 실재 | 실재 — § 포인터 대상(무수정). |
| `planning/specs/04-solution-design.md` (바인딩 대상 정본) | 실재 (v1.3 Baseline) | 실재 — §3·§4 확인(무수정). |
| `planning/specs/03-project-contract.md` (참조 정본) | 실재 (v1.2 Baseline) | 실재 — §3.1-B·§3.4·§3.5·§3.6 확인(무수정). |
| `uahf/framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v1.md` (성숙 기준선 = Ground Truth) | 실재 (pc-uahf-001·instanceVersion 1·supersedes null·Ready — 성숙 입력) | 실재 — 성숙 경로 v1→v2의 입력 기준선. |
| `uahf/framework/adapters/claude/solution-design-data/` (SD 백엔드 루트) | 실재 (정본 문면 소유) | 실재 — 루트·`policy/default-policy.yaml`·`events/`(표면, `.gitkeep`) 실측. run 인스턴스 `events/maturation-r001…r003/`은 산출물 수명 정책에 따라 아카이브 `@cd9247b`(ARCHIVE.md 원장 — 물리 위치는 2차 산출물 디커플링 트랙에서 확정). |
| `…/solution-design-data/events/maturation-<run-id>/events.jsonl`·`policy/default-policy.yaml` | 실재 (형식·값 정본 문면 소유) | 형식·값 정본 문면 실재(본 문서 소유) — 물리 인스턴스(maturation-r001…r003)는 성숙 run E2E로 생성 후 아카이브 `@cd9247b`. `policy/default-policy.yaml`은 실재. |
| `uahf/framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v2.md` (성숙 산출 — superseding 인스턴스) | 실재 (경로 정본 = contract-binding §4.2) | 실재 — 성숙 경로 v1→v2 append(v1 문면 byte 불변, PC-INV 9). |
| 소비 프로젝트 `.claude/solution-design/` (일반 관례) | 경로 관례 확정(정본) | 본 저장소에는 미존재(정상 — 일반 관례는 소비 프로젝트 배치 대상). |
| 성숙 실행 규약 절차 로더·기록기·Policy 로더(형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). |

- **핵심 구분.** 본 문서가 확정한 백엔드 트리·기록 직렬화 어휘·게이트 채널·Policy 값·Provenance 성숙 run 내부 형식은 **정본 문면(형태 A)**이며, 물리 데이터 자산은 성숙 run E2E로 생성되었다 — run 원장 인스턴스(`solution-design-data/events/…`)는 산출물 수명 정책(`docs/artifact-lifecycle-policy.md`)에 따라 앵커 보존 `@cd9247b`로 전환되었고, superseding v2 계약 인스턴스는 실재를 유지한다. 본 문서는 구조·형식·경로·값의 정본 문면을 소유하고, 그 물리 위치(현행 `uahf/framework/adapters/claude/…`)의 최종 확정은 2차 산출물 디커플링 트랙 소관이다(L-07).
- 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로 쓰지 않는다(L-07).

---

## §13. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 planning/specs/04 §3·§4의 물리 실현이다. 어떤 상태·전이·SP-INV·단계 계약·판정 형태·역할 추상·Projection 관계·경계 기준도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 04 §3이다. 새 계약 요소(상태·전이·불변·필드·kind)를 창설하지 않았다. 방법론 고유명·고정 역할 카탈로그·타 AI 벤더·모델명 0건(UAF-INV ⑥ — 정본 청정).
- **본 문서가 소유·확정하는 것.** 04 §4.1이 "Adapter 소관"으로 미룬 지점 — ① Expert Role 실행 호스팅 **역할 추상**(§6) ② 사용자 게이트 제시·응답 채널(§5) ③ `solution-design-data/` 백엔드 트리·기록 직렬화(§3·§4) ④ Policy 값 데이터 소스·직렬화 + 최소 실값(§7) — 과, 저장의 부속으로 ⑤ Provenance 성숙 run 내부 형식(§8)을 확정한다. Expert Role 물리 호스팅은 **설계하지 않는다**(04 §3.9 확장 포인트). superseding 인스턴스 저장·버전 표기·Provenance 외형·must-ignore 경계는 contract-binding §3·§4·§5·§6 소유이며 참조 인용만 한다(재정의 0).
- **격리 토큰의 단일 자리.** 구체 직렬화 형식·물리 경로(`uahf/framework/adapters/claude/solution-design-data/…`·`.claude/solution-design/…`)·파일 확장자·Policy 값은 이 Adapter 경계 문서에 둔다. UAF 정본(planning/specs/04)은 이 토큰을 "Adapter 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3는 이 경계에 비적용 — 격리 보유).
- **동시 작성 문서 경계(07 R2·R4).** 본 문서는 `planning/adapters/claude/solution-design-binding.md` 1개 파일이며, 위치·구조·형식·값의 정본 문면을 소유한다(07 R2). 확정된 인터페이스 계약(planning/specs/04 §3·§4·03 §3.1-B·§3.4·§3.5·§3.6·contract-binding §4.2·§5·§6·discovery-binding §3·§4·§5·§7·§8·§10·루트 UAF-INV)만 참조했다. UAF 정본·UAHF 정본·기존 바인딩·물리 데이터를 수정·생성하지 않았다(07 R4·INV-2). 불확실 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02-agent O4).

### open_questions (Advisor 에스컬레이션 — 전건 비차단)

- **OQ-SD-1 (Policy 최소 실값 — 비차단).** §7.2 최소 실값 1세트(성숙 신호 4종·역할 상한 4·기본 역할 구성 `defaultComposition`·Projection 동적 선택)는 E2E 구동을 위한 본 문서의 Adapter 재량 확정이며(DP-5가 "최소 실값 1세트 정본 값 표로 확정"으로 위임·DP-X5 동형), Policy as Data이므로 값 조정은 데이터 정정일 뿐 정본 계약(04 §3.2·§3.3·§3.5) 변경이 아니다. W2 E2E 시나리오가 다른 상한·판정 신호를 요구하면 Advisor 재확정 또는 `policy/` 데이터 정정으로 조정 가능하다 — 계약 변경이 아니므로 비차단이다.
- **OQ-SD-2 (백엔드 데이터 트리 물리 위치 — 비차단·2차 트랙).** 본 문서는 planning 레이어 어댑터 경계(`planning/adapters/claude/`)로 이동했으나, 본 문서가 선언·소유하는 백엔드 데이터 트리(`solution-design-data/`·성숙 산출 `discovery-data/contracts/uahf/`)는 1차 이동 범위 밖으로 현행 `uahf/framework/adapters/claude/…` 아래에 잔류한다. 그 최종 물리 위치 확정은 2차 산출물 디커플링 트랙 소관이며(본문 인라인 플래그와 정합), 계약 내용 변경이 아니므로 비차단이다.

---

## §14. 요약 (한눈에 보기)

- 이 문서 = planning 레이어 자신의 Claude 어댑터 바인딩(`planning/adapters/claude/solution-design-binding.md`)이며 `planning/specs/04-solution-design.md` §3·§4를 바인딩한다. 정본 = 04 §3·§4(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 04 "### 4.1 바인딩 지점" 표 **4행 전건**(호스팅·게이트 채널·저장 위치·Policy 실값)을 물리 실현으로 매핑(실재/규약 실현(형태 A)/형태 B 3구분). 실행 기록 직렬화는 행3의 일부(04 §3.2·§3.7 실현).
- **§3 (DP-1):** `solution-design-data/` 백엔드 트리 정본 선언(events/maturation-<run-id>/·policy/)·실행 메타 파일은 코어 밖(SP-INV 2·3)·이원화(`.claude/solution-design/`, DP-X2 동형). superseding 인스턴스는 contract-binding §4.2 경로 append(참조 인용·재정의 0). 성숙 run E2E로 실재(현행 `uahf/framework/adapters/claude/…`, 물리 위치는 2차 산출물 디커플링 트랙에서 확정 — L-07).
- **§4 (DP-2):** append-only 기록 로그(`events.jsonl` 동형·1 사건 = 1 레코드·seq 순서 값 전속·물리 시각 별도 실측 성격 L-09). 최소 레코드 6종(`MaturationRunStarted`·`StateTransition`·`GatePresented`·`UserResponded`·`OutputRecorded`·`MaturationRunConcluded`) = Adapter 기록 관례·04 §3.4 상태/전이 T1~T11 payload 인용·Discovery Event 15종 명칭 차용 0·새 코어 계약 요소 0.
- **§5 (DP-4):** 주 세션 사용자 제시·응답 채널(discovery-binding §5 동형)·T8(→Matured)·T9(→Skipped)·T10(→Reviewing 재진입)·T11(→Escalated) 실의미·제시/응답 각 레코드. 승인 전 Matured 불가(SP-INV 4 — `UserResponded`가 T8/T9 전이에 선행).
- **§6 (DP-3):** 주 세션(Advisor) Orchestrator 규약 절차·Expert Role 수행 = 기존 위임 실행 관행 재사용·새 병렬 프레임워크 0·물리 호스팅 설계 0(04 §3.9). 역할 추상까지만·최소 할당·개방 네임스페이스(SP-INV 5·6·8). 04 코어 문면 무촉.
- **§7 (DP-5):** `solution-design-data/policy/default-policy.yaml` 형식 + **최소 실값 1세트 정본 값 표**((가) 성숙/스킵 판정 신호 4종 (나) 역할 선택 상한 4·기본 역할 구성(`defaultComposition`)·이탈 규칙(`deviationRule`)·역할→산출물 소유 맵(`artifactOwnership`)·고정 팀 금지 (다) Projection 동적 선택·전 유형 강제 금지). Policy as Data — 값 조정 = 데이터 정정.
- **§7A (산출물 생산 프로토콜 — form-A):** 위임 산출(역할별 소유 산출물·주 세션 조율/검증만·컨택스트 위생)·형식(Markdown 본문 `<workspace>/docs/` + 기계 색인 `design-manifest.json`·구조화 사이드카는 다운스트림 소비 시에만)·검증 3층(CP1 역할 자체점검→CP2 커버리지 역할+`design_completeness` 결정적 체커→CP3 Advisor 매니페스트 기반·전수 정독 X + Validating 사용자 게이트)·사용자 컨펌 3시점(제외 inline·Validating 일괄·고임팩트 즉시). 책임 있는 자율(루트 §6 원칙 11) 정합·04 §3.3~3.5·SP-INV 7·9 재정의 0.
- **§8:** Provenance 성숙 run 내부 형식(run 식별자·이벤트 로그 참조·기준선 vN 참조·Policy 참조)만 확정. 외형·must-ignore 경계는 contract-binding §6 소유(재정의 0·discovery-binding §10 경계 동형)·성숙 활동 측 소비 전용·누출 차단(SP-INV 2·3).
- **§10:** 04 "### 4.2" 이식 교체 지점 대응 표 — 유지 열 = §3.1·§3.2·§3.3·§3.4·§3.5·§3.6·§3.8(C-1 동형).
- **§11:** 상시 불변 자기 점검 — 재정의 0·새 계약 요소 창설 0·Discovery Event 15종 명칭 차용 0(mention/use 경계)·방법론·역할 카탈로그·타 벤더·모델명 0·SP-INV 1~9 정합(9 = 설계 커버리지 완성도).
- **§12:** 실측 대조 — `solution-design-data/`·superseding v2 실재(성숙 run E2E 생성, 현행 `uahf/framework/adapters/claude/…`), 바인딩·04·03 정본·Ground Truth v1 실재. 실측과 불일치 서술 0(L-07).
- 04·03·02·루트 재정의 0, Glossary 용어 신설 0, 새 계약 요소 창설 0, 실행 코드 0(형태 A). 구체 직렬화 형식·물리 경로·Policy 값 토큰은 이 Adapter 경계에서 허용된다(격리 지점).
