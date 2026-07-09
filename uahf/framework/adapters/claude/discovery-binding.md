# framework/adapters/claude/discovery-binding — Claude Code Project Discovery Adapter 바인딩

작성일: 2026-07-07
상태: v1.2 Baseline (CP2 첫 판정 Pass 16/0/0 · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: AGENT.md
근거 정본:

- discovery/specs/02-discovery.md §3(전문)·§4.1(### 4.1 바인딩 지점 — 표 4행 D1~D4)·§4.2(### 4.2 이식 교체 지점 — 4불릿 + "Module부 바인딩(§3.9~§3.16)" 문단 D5·D6). 특히 §3.3(State Machine 단일 정본 — 비종단 6·종단 5·전이 T1~T25)·§3.5(Event Model 15)·§3.6(Termination 4경로)·§3.7(Execution Ready 2축 판정)·§3.9(Module Structure 7모듈)·§3.10(Strategy Provider Interface·레퍼런스 Provider 1건)·§3.11(Discovery Dimension 5)·§3.12(Confidence)·§3.13(Adaptive Discovery)·§3.14(Question Budget soft/hard)·§3.15(Discovery Policy — Policy as Data)·§3.16(Metrics)·§5(Memory Access — v1.1 UAHF Memory 비활용)·DISC-INV 1~9. 본 문서가 물리 실현으로 바인딩하는 계약의 정본. **재정의·확장하지 않고 § 포인터로만 인용한다.**
- ARCHITECTURE.md §11(확장 포인트 경계 — Discovery 실행 호스팅은 **역할 추상까지만**·Discovery의 Memory 활용은 확장 포인트로만)·§12.2(Discovery Request 인터페이스 추상 3요소 {mode, inputs, policy})·§7.1(상시 불변 확인 2건)·§8(UAF-INV — ① UAHF 정본 무수정·유일 접점 Project Contract, ②③ Discovery 교체 가능·Strategy Invariance, ⑤ 확정 게이트 = 사용자 승인, ⑥ Framework는 방법론 모름). 근거 인용용·재정의 0.
- framework/adapters/claude/contract-binding.md §3(Contract 직렬화 = Markdown 본문 + YAML front-matter)·§4.2(본 저장소 Contract 격리 경로 `framework/adapters/claude/discovery-data/contracts/uahf/`·파일명 `project-contract.v<N>.md`)·§6(**"Provenance 컨테이너 내부 형식은 discovery-binding.md 소관" 명시 위임 — DP-X6**). 선행 확정 인터페이스(T-C 폐합). 본 문서 §10이 그 위임(DP-X6)을 해소한다.
- framework/adapters/claude/entry-binding.md §5.1(Discovery Request 직렬화 = {mode, inputs, policy} 자기서술 구조화 레코드)·§5.3(**"기록 백엔드 트리는 discovery-binding.md 소관" 명시 위임 — DP-X8**). 선행 확정 인터페이스(T-E 폐합). 본 문서 §4가 그 위임(DP-X8)을 해소한다.
- framework/adapters/claude/memory-binding.md — 자매 Adapter Binding 골격 선례(백엔드 격리 트리·append-only·실측 대조·형태 A/B 정직 구분·"지원 구조 — 시연 시 생성" L-07 관례). **memory-data/(UAHF Memory 백엔드)와 discovery-data/(Discovery Evidence Store 백엔드)의 네임스페이스 구분** 근거(02 §5).
- framework/adapters/claude/loop-binding.md §5.2 — 사람 개입 물리 채널(주 세션 사용자 제시·에스컬레이션 산출). 본 문서 §5(D2)의 선행 준거. §3.3(append-only 로그·`at` 순서 값 물리 표현, Active Lesson L-09)도 Event 로그 직렬화 관행 근거.
- framework/core/structure.md §2(4경계 배치 — `framework/adapters/<adapter>/` = 환경 의존 격리 경계)·§5(금지 토큰 규칙 C-3 — Adapter 경계는 격리 보유로 비적용). 본 문서 경계·격리 토큰 허용의 근거.
- specs/03-loop.md §3.2-A — append-only 전이 이벤트 로그·순서 값 물리 표현 관행(loop-data 선례의 정본). Event 로그 직렬화 관행 근거(재정의 0 — Discovery Event Model은 02 §3.5 소유).
- specs/00-glossary.md — UAHF 용어 정본. 본 문서는 새 용어를 신설하지 않는다. `형태 A/B`는 structure.md §4의 서술 라벨 인용이며 Glossary 표제어가 아니다.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core·UAF 계약을 특정 실행 환경·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 직렬화 형식·물리 경로·환경 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, 자매 contract-binding.md §0·entry-binding.md §0·memory-binding.md §0과 동형). 단 이 문서는 UAF 정본(discovery/specs/02-discovery.md §3·§4)과 UAHF 정본을 **재정의하지 않는다** — 계약(State Machine·Event Model·Termination·판정식·모듈 경계·Provider 계약·Policy as Data·불변)은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-07 | v1.2 Draft | 최초 작성. `framework/adapters/claude/` 경계의 **UAF 정본(uaf/specs/02-discovery) 바인딩** 산출물(자매 contract-binding.md·entry-binding.md와 같은 UAF 레벨 부류·접두 없음). 02 "### 4.1 바인딩 지점" 표 **4행(D1~D4)** + "### 4.2" 말미 "Module부 바인딩(§3.9~§3.16)" 문단 **2지점(D5·D6)**을 Claude 환경 물리 실현으로 확정(§2 — 실재/규약 실현(형태 A)/형태 B 3구분). **D1**(Event 로그 직렬화) = 02 §3.5 Event 15종 append-only 로그, 자기서술 구조화 레코드(1 Event = 1 레코드)·위치 `discovery-data/events/<mode>-<run-id>/`·순서 값 ↔ 물리 생성 시각 성격 구분(L-09)(§3). **discovery-data/ 백엔드 트리 정본 선언**(§4 — `events/`·`policy/`·`contracts/uahf/`(contract-binding §4.2 참조 인용)·`e2e-greenfield-project/`(DP-X3) + Discovery Request 기록 위치 확정(DP-X8 해소 — entry-binding §5.3 위임)). **D2**(사용자 확인·UserOverride 채널) = 주 세션 사용자 제시·응답 수령(loop-binding §5.2 동형·G1 Eliciting·G2 Validating·UserOverride 구분)(§5). **D3**(증거 스캔·프레이밍) = Greenfield 프레이밍/Brownfield 실 저장소 스캔(T2)/Incremental 결속의 형태 A 물리 절차(§6). **D4**(Strategy 실행 호스팅) = 주 세션(Advisor)이 Orchestrator 역할(§3.9)·레퍼런스 Provider(§3.10-C)를 **역할 추상까지만** 실현·물리 호스팅 설계 0(uaf/ARCHITECTURE §7 정합)(§7). **D5**(Policy 값 데이터 소스, DP-X5) = `discovery-data/policy/` 형식 + **E2E 구동용 최소 실값 1세트 정본 값 표**(§8 — Policy as Data). **DP-X6 해소**(§10 — Provenance 내부 = Discovery 실행 메타 형식·03 §3.2-D 불투명 계약 유지·UAHF must-ignore·Discovery 측 소비 전용). 상시 불변 자기 점검(§11 — Discovery 내부 개념 누출 0·mention/use 경계·Evidence Store ≠ UAHF Memory 네임스페이스 구분(02 §5)). 02 "### 4.2" 이식 교체 지점 대응 표(§12 — 유지되는 것 = §3.3·§3.5·§3.6·§3.7·§3.8·§3.9·§3.10·§3.15). 상태 서술 실측 대조(§13 — discovery-data/ 현 시점 미존재·자매 바인딩 실재, L-07). 실행 코드 0(형태 A, D-v1.2-1). 02 §3·§4·UAHF 정본 재정의 0·§ 포인터 인용만·새 계약 요소(Event·상태·전이·모듈·Provider·Policy 항목) 창설 0·방법론 고유명 0. 미완성 후속 산출물(E2E 데이터) 불인용·불추측(07 R2). | Worker (Advisor 위임, Task T-D) |
| 2026-07-07 | v1.2 Baseline | v1.2 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass 16/0/0; CP3 Advisor 승인) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, 자매 contract-binding.md §9·entry-binding.md §9·memory-binding.md §9·framework/core/structure.md §9 동형. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **UAF 정본 바인딩 선언(DP-X1).** 이 문서는 `framework/adapters/claude/` 경계의 Adapter Binding 문서이되, 그 **바인딩 대상 정본은 UAHF spec이 아니라 UAF 정본 `discovery/specs/02-discovery.md` §3·§4다.** 자매 바인딩 12문서(runtime·memory·verifier·loop·workflow·hooks·skills·plugins·agent·scaffold·harness-binding + adapter-conformance)가 UAHF spec(specs/01~13)을 바인딩하는 것과 달리, 본 문서는 UAF 레벨의 Project Discovery 정본을 바인딩한다(자매 contract-binding.md·entry-binding.md와 같은 부류). 파일명·골격 관례는 자매와 동형이다(접두 없음).

- **정본은 discovery/specs/02 §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소 — Compiler 프레이밍(§3.1)·State Machine 단일 정본(§3.3 — 비종단 6·종단 5·전이 T1~T25)·Event Model 15(§3.5)·Termination 4경로(§3.6)·Execution Ready 2축 판정(§3.7)·Invariants DISC-INV 1~9(§3.8)·Module Structure 7(§3.9)·Strategy Provider Interface(§3.10)·Discovery Dimension 5(§3.11)·Confidence(§3.12)·Adaptive Discovery(§3.13)·Question Budget(§3.14)·Discovery Policy(§3.15)·Metrics(§3.16) — 를 **재정의·확장하지 않는다.** 계약 요소는 정본 § 포인터로만 인용한다. 본 문서가 확정하는 것은 02 §4.1·§4.2가 "Adapter 소관"으로 미룬 물리 실현 — **D1 Event 로그 직렬화·D2 사용자 확인/UserOverride 채널·D3 증거 스캔/프레이밍·D5 Policy 값 데이터 소스·직렬화**와, Module부 문단의 **D6 Evidence Store 물리 저장(= D1과 동일)**, 그리고 **DP-X6 Provenance 내부 형식·DP-X8 백엔드 트리** 넷이다. **D4 Strategy 실행 호스팅은 역할 추상까지만** 확정하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE §11).

- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문, 그리고 UAF 정본(discovery/specs/02) 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이다(structure.md §5 C-3 확장·02 §3 도입 "§3에는 특정 AI 모델·실행 환경 의존 내용이 한 줄도 들어가지 않는다"). 이 문서는 그 **반대편**이다 — 구체 직렬화 형식·물리 경로(`framework/adapters/claude/…`)·파일 확장자의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(contract-binding.md §0·entry-binding.md §0·memory-binding.md §0과 동형). 단 **uaf/ 정본이 명명하지 않은 것을 uaf/ 정본 문면인 것처럼 서술하지 않는다** — 물리 확정은 전부 본 문서 소유임을 명시한다.

- **하네스 Bootstrap 전제(형태 A, D-v1.2-1).** 이 하네스는 현재 Bootstrap 상태다(Glossary J-13, 자매 바인딩 §0). 본 문서의 바인딩은 **실행 코드 0**이다 — Discovery의 State Machine(02 §3.3)·모듈(02 §3.9)·레퍼런스 Provider(02 §3.10-C)는 실행 스크립트가 아니라 **규약 절차·규약 역할**로 실현되며 주 세션이 실수행한다(D-v1.2-1). 따라서 매핑은 (i) 물리 실재 표면(자매 바인딩·정본 문서), (ii) 규약으로 확정된 정본 문면(형태 A — 직렬화 형식·백엔드 트리·채널·Policy 값), (iii) 실행 코드 도입 시 로딩될 지점(형태 B — Event 로거·직렬화기·관측 로더)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.

- **경계 분담 해소(DP-X6·DP-X8).** 두 선행 바인딩이 본 문서로 **명시 위임**한 두 지점을 본 문서가 해소한다 — (i) **DP-X6**: Contract Provenance 불투명 컨테이너의 **내부 형식**을 contract-binding §6이 "discovery-binding.md 소관"으로 미뤘고, 본 문서 §10이 Discovery 실행 메타 형식으로 확정한다(03 §3.2-D 불투명 계약 유지). (ii) **DP-X8**: Discovery Request 기록의 **백엔드 트리 위치**를 entry-binding §5.3이 "discovery-binding.md 소관"으로 미뤘고(직렬화 형식은 entry-binding §5.1 소유), 본 문서 §4가 위치를 확정한다. 두 해소 모두 선행 바인딩의 계약 표면(Provenance 외형·must-ignore 경계 = contract-binding §6 소유; Discovery Request 직렬화 형식 = entry-binding §5.1 소유)을 침범하지 않고 **본 문서 소관 지점만** 확정한다.

- **실측 기반 상태 서술(L-07).** "실재/미존재" 주장은 파일 시스템 확인 후에만 기입한다. 본 문서가 선언하는 `discovery-data/` 백엔드 트리는 **현 시점 미존재**이며, 그 물리 생성은 v1.2 E2E Task(T-XG·T-XB) 소관이다 — 본 문서는 경로·구조·형식·값의 **정본 문면만** 소유한다(memory-binding.md §2·§7 "지원 구조 — 시연 시 생성" 선례 동형). §13이 그 실측 대조 표다. 본 문서는 신규 1파일(discovery-binding.md)만 생성하며 어떤 디렉터리·데이터 파일도 생성하지 않는다.

- **네임스페이스·용어.** 본 문서가 확정하는 것은 물리 표기(직렬화 형식·경로·채널·Policy 값)뿐이며, 02가 소유하는 계약 용어(`DiscoveryStarted` 등 Event 15·상태·전이 T#·모듈명·Dimension·Confidence·Question Budget·Discovery Policy 등)는 02 정의를 § 포인터로 참조하고 재정의하지 않는다. 새 UAHF 용어·새 계약 요소(Event·상태·전이·모듈·Provider 필드·Policy 항목·불변)를 신설하지 않는다. Discovery 내부 파생 뷰 라벨(Lifecycle·Process·Workflow)은 UAHF Glossary 동명 용어와 네임스페이스로 구분된다(02 §0·§3.4).

---

## §1. 목적

이 문서는 discovery/specs/02 "### 4.1 바인딩 지점" 표 4행(D1~D4)과 "### 4.2" 말미 "Module부 바인딩" 문단의 2지점(D5·D6)을 이 환경 위에 **v1.2 시점의 구체 물리 실현**으로 매핑한다. Discovery의 산출(Project Contract)은 UAF↔UAHF 유일 접점이므로, 본 문서가 확정하는 Discovery 백엔드·채널·Policy 물리 실현은 v1.2 E2E·후속 작업의 물리 실현 기반이다.

책임은 여섯이다.

- 02 §4.1 바인딩 표 **4행(D1~D4)** + Module부 문단 **2지점(D5·D6)** 전부를 물리 실현으로 확정한다(§2 — 실재/규약 실현(형태 A)/형태 B 3구분).
- **D1**: Event 15종 append-only 로그의 직렬화 형식·위치·순서 값 성격을 확정한다(§3). **discovery-data/ 백엔드 트리**를 정본으로 선언하고 DP-X8(Discovery Request 기록 위치)을 해소한다(§4).
- **D2**: 사용자 확인·UserOverride 물리 채널을 확정한다(§5). **D3**: Greenfield/Brownfield/Incremental 증거 스캔·프레이밍의 형태 A 물리 절차를 확정한다(§6). **D4**: Strategy 실행 호스팅을 **역할 추상까지만** 확정한다(§7).
- **D5**: `discovery-data/policy/` 데이터 파일 형식 + **E2E 구동용 최소 실값 1세트**를 정본 값 표로 확정한다(§8, DP-X5). **DP-X6**: Provenance 컨테이너 내부 형식을 확정한다(§10).
- Discovery 내부 개념 누출 0·Stable Contract 훼손 0·Evidence Store ≠ UAHF Memory 네임스페이스 구분을 **상시 불변 자기 점검**으로 보인다(§11).
- 02 §4.2 이식 교체 지점(4불릿 + Module부 대응)에 본 문서의 대응을 명시하고(§12, "유지되는 것" 열 = 02 §3 불변 재확인), 상태 서술을 실측과 대조한다(§13).

이 문서는 02 §3·§4·UAHF 정본의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A → 형태 B 전환 시에도 02 §3 계약 변경은 0이며(structure.md §7 C-1 동형), §12의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 02 §4.1·§4.2 바인딩 지점 6건 물리 실현 (done 2)

02 "### 4.1 바인딩 지점" 표의 **4행(D1~D4)**과 "### 4.2" 말미 "Module부 바인딩(§3.9~§3.16)" 문단의 **2지점(D5·D6)**을 물리 표면으로 매핑한다. "02 바인딩 지점" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 형식·경로·채널·값을, "실재 여부" 열이 Bootstrap 상태에서의 **물리 실재 / 규약 실현(형태 A) / 형태 B**를 정직하게 구분한다(§13 실측 대조).

| # | 02 §3 계약 요소 (정본 §) | 02 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| **D1** | Event 로그 직렬화 (§3.5, §4.1 행1) | "append-only Event 기록의 저장 형식·위치." | Event 15종을 담는 append-only 로그 = 자기서술 구조화 레코드(1 Event = 1 레코드)·위치 `discovery-data/events/<mode>-<run-id>/`. 순서 값 ↔ 물리 생성 시각 성격 구분(L-09). 상세 §3. | 형식·위치 확정(정본, 형태 A). Event 로그 데이터·`discovery-data/` = 미존재(E2E Task 생성 예정). 로거·직렬화기 = 형태 B. |
| **D2** | 사용자 확인·`UserOverride` 채널 (§3.3 Validating·§3.6, §4.1 행2) | "사용자 승인/수정/강제 응답을 받는 개입 채널." | 주 세션 사용자 제시·응답 수령 채널(loop-binding §5.2 동형) — G1 Eliciting 질문/답변·G2 Validating 승인/수정·UserOverride 강제 구분. 각 개입은 Event로 기록(§3.5). 상세 §5. | 채널 확정(정본, 형태 A). 무인 자동 트리거 = 형태 B. |
| **D3** | Contextualizing 증거 스캔·프레이밍 (§3.3, §4.1 행3) | "Greenfield 프레이밍·Brownfield 증거 스캔의 물리 구현·증거 소스 접근." | Greenfield 프레이밍 / Brownfield 실 저장소 스캔(T2, 파일 시스템 실측) / Incremental 기존 Contract 결속의 형태 A 물리 절차(주 세션 수행·Evidence Store 기록). 상세 §6. | 절차 확정(정본, 형태 A). 스캔 로더 = 형태 B. |
| **D4** | Strategy 실행 호스팅 (§3.1 Front-end, §4.1 행4) | "Discovery 실행을 어느 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE.md §11)." | 주 세션(Advisor)이 Orchestrator 역할(§3.9)을 규약 절차로 수행·레퍼런스 Provider(§3.10-C)를 규약 역할로 실현. **물리 호스팅(실행 코드·자동 실행)은 설계 0**(ARCHITECTURE §11 정합). 상세 §7. | 역할 추상 확정(정본, 형태 A). 물리 호스팅 = **설계 안 함**(확장 포인트). 실행 코드 = 형태 B. |
| **D5** | Question Budget 예산·Discovery Policy 정책 값 데이터 소스·직렬화 (§3.14·§3.15, §4.2 Module부 문단) | "Question Engine의 예산·Discovery Policy의 정책 값(임계값·예산·경계 수치)의 **데이터 소스·직렬화**는 Adapter 소관이다(§3.14·§3.15)." | `discovery-data/policy/` 데이터 파일 형식 + **E2E 구동용 최소 실값 1세트 정본 값 표**(차원 임계·Budget 총량/차원별·soft/hard·종료 규칙·충돌 게이트). Policy as Data — 값 조정 = 데이터 정정(엔진·계약 무변경). 상세 §8. | 형식·값 정본 문면 확정(정본, 형태 A). 물리 데이터 파일(`policy/`) = 미존재(E2E Task 생성 예정). |
| **D6** | Evidence Store 물리 저장 (§3.9, §4.2 Module부 문단) | "Evidence Store의 물리 저장은 위 Event 로그 직렬화 바인딩과 **동일하다**(§3.9)." | Evidence Store의 물리 저장(증거 레코드 + Event 로그) = **D1과 동일 백엔드** `discovery-data/events/<mode>-<run-id>/`. 증거는 `EvidenceRecorded` Event 페이로드로 append. 상세 §3·§4. | D1과 동일(정본, 형태 A). 02 §4.2 문면 "동일하다"대로 별도 백엔드를 창설하지 않음. |

주:

- 위 6행은 02 "### 4.1" 표 4행(D1~D4) 전건과 "### 4.2" Module부 문단의 물리 실현 대상 2지점(D5·D6) 전건이다. Module부 문단의 나머지 지점 — **Strategy Provider 실행 호스팅(역할 추상까지만, §3.10)** — 은 §4.1 행4(D4)와 동일한 지점이므로 D4로 통합해 다룬다(중복 창설 방지). 각 행의 "물리 실현"은 02 정본 표현을 이 환경의 구체 형식·경로·채널·값으로 좁힌 것이며, **새 바인딩 계약을 창설하지 않는다**(§0). 특정 AI·모델·제품 기능·방법론 고유명은 여기서도 명명하지 않는다(02 §4.1 말미 동형) — 격리 대상은 직렬화 형식·물리 경로·Policy 값뿐이다.
- 02 §4.1·§4.2에 없는 계약 요소(§3.3 State Machine·§3.5 Event Model·§3.6 Termination·§3.7 판정식·§3.8 Invariants·§3.9 모듈 경계·§3.10 Provider 계약·§3.15 Policy as Data)는 **이식 시에도 유지되는 것**이며, 본 문서가 바인딩하지 않는다(§12 "유지되는 것" 열). 이들의 진위 판정 기준은 02 §3이다.

---

## §3. D1 — Event 로그 직렬화 확정 (done 3)

02 §4.1 행1("append-only Event 기록의 저장 형식·위치")의 물리 실현을 확정한다. Event Model(02 §3.5)·상태 전이(02 §3.3)·불변(DISC-INV-1·DISC-INV-3)은 재정의하지 않고 § 포인터로 인용하며, 물리 직렬화 형식·위치만 확정한다.

### §3.1 Event 15종 (02 §3.5 정본 재실측 열거 — 재정의 0)

append-only 로그가 담는 Event는 02 §3.5의 **정확히 15종**이다(본 문서가 02 §3.5에서 직접 재실측해 열거한다 — 정의·의미는 02 §3.5 소유, 재정의 0):

`DiscoveryStarted` · `ContextCaptured` · `QuestionAsked` · `AnswerReceived` · `EvidenceRecorded` · `ConfidenceUpdated` · `BudgetConsumed` · `DimensionSaturated` · `AssumptionRecorded` · `ValidationRequested` · `UserOverride` · `ContractCompiled` · `ExecutionReadyDeclared` · `DiscoverySuspended` · `DiscoveryAborted` (계 15).

- **모든 전이는 Event로만.** 모든 상태 전이는 위 15 Event로만 일어난다(DISC-INV-1, 02 §3.3 핵심 규칙 — 재정의 0·§ 포인터 인용). 기록되지 않은 전이는 없다(DISC-INV-3).

### §3.2 확정 — 자기서술 구조화 레코드 append-only 로그 (1 Event = 1 레코드)

**한 Discovery run 1건의 Event 로그 = 발생 순서대로 append되는 자기서술 구조화 레코드의 로그**로 직렬화한다. **1 Event = 1 레코드**이며, 레코드는 발생 순서대로만 추가된다(append-only, DISC-INV-3). 자매 바인딩의 append-only 로그 관례(loop-binding §3의 사이클당 append-log, memory-binding §2의 index append-log)와 동형이며, 구체 구조화 데이터 형식은 Adapter 선택이다(격리 지점 — 이식 교체 §12).

- **레코드 최소 표면.** 각 레코드는 최소한 (i) **Event 종류**(§3.1의 15종 중 하나), (ii) **순서 값**(아래 §3.3), (iii) **Event별 페이로드**를 담는다. Event별 페이로드의 내부 구조는 이 직렬화가 해석하지 않는 불투명 페이로드로 그대로 담긴다 — Event의 의미·유발 Guard는 02 §3.3-B 전이표·§3.5가 소유하며 본 직렬화가 재정의하지 않는다.
- **append-only 불변(DISC-INV-3).** 기록된 레코드는 재작성·삭제하지 않는다. 정정·후속 상태는 새 레코드 append로 표현된다. `DiscoverySuspended`(T24) 후 재개, `UserOverride`(T21~T23) 강제, 재작업 재진입(T17)도 각각 하나의 레코드로 append된다(02 §3.3-B·§3.5 — 재정의 0).
- **"기록만으로 run 재구성".** 로그의 레코드 순서(= append 순서 = 전이 순서)만으로 해당 run의 State Machine 진행(생성 `Initiated` → 전이 → 종단)이 재구성된다. Metrics는 별도 계측이 아니라 이 Event 로그에서만 파생된다(DISC-INV-4·02 §3.16 — 본 문서는 로그 물리 표면만 확정하고 Metrics 산식을 정의하지 않는다).

### §3.3 순서 값과 물리 생성 시각의 성격 구분 (L-09)

기록 필드의 **순서 값**과 **물리 생성 시각**의 성격을 형식에서 구분해 명시한다(Active Lesson L-09 — 기록의 순서 값은 순서를 확정하는 값이고, 물리 시각 주장은 실측 대조 후에만; loop-binding §3.3 `at` 순서 값 관례 동형).

- **순서 값(정본 표면).** 각 레코드는 단조 증가하는 **순서 값**을 갖는다. 이 값이 로그 내 레코드 순서(= 전이 순서)를 확정한다. 로그의 순서는 언제나 이 순서 값(= append 순서)에서 도출되며, 벽시계 시각에서 도출하지 않는다. append-only 로그에서 순서 값은 그 자체로 자기서술적이다(DISC-INV-3).
- **물리 생성 시각(별도 필드·실측 성격).** 레코드가 벽시계 생성 시각을 함께 담는 경우, 그것은 **순서 값과 별개의 필드**이며 그 값의 진위는 **실측 대조 후에만** 참으로 취급되는 측정 주장이다(L-09). 물리 생성 시각은 로그의 순서를 결정하지 않는다 — 순서 결정은 순서 값 전속이다. 이 성격 구분을 형식이 명시함으로써, 시각 필드의 부재·오차가 로그의 순서 정합(전이 재구성)을 훼손하지 않는다.

### §3.4 위치 — run 단위 격리

- **위치.** 한 Discovery run의 Event 로그는 `framework/adapters/claude/discovery-data/events/<mode>-<run-id>/` 아래에 둔다. `<mode>` = Discovery Request의 mode(greenfield/incremental/brownfield 등, ARCHITECTURE §12.2 확장 네임스페이스), `<run-id>` = 해당 run(= Discovery Request 결속으로 생성된 State Machine 인스턴스, 02 §3.3-A "생성은 인스턴스화")의 식별자. run 단위 디렉터리로 격리해 서로 다른 run의 로그가 섞이지 않게 한다.
- **레코드 파일 단위·명명(Adapter 재량).** 로그를 run 디렉터리 내 단일 append-log 파일로 두는지, 레코드 단위 파일로 두는지의 세부와 명명은 Adapter 재량이며(승인 계획 위임), 어느 경우에도 §3.2 append-only·§3.3 순서 값 성격은 유지된다. 정확한 물리 명명·샤딩 등 규모 대응은 형태 B/규모 사안으로 미룬다(선취·추측 금지).
- **D6 정합(Evidence Store = 동일 백엔드).** Evidence Store(02 §3.9 — "증거와 Event 로그를 append-only로 보관")의 물리 저장은 이 Event 로그 백엔드와 **동일**하다(02 §4.2 Module부 문단 "동일하다"). 증거는 `EvidenceRecorded` Event(§3.1)의 페이로드로 같은 run 디렉터리 로그에 append되며, 별도 증거 백엔드를 창설하지 않는다.

---

## §4. discovery-data/ 백엔드 트리 정본 선언 (done 4 · DP-X8 해소)

Discovery의 물리 백엔드 데이터 위치를 **Adapter 경계 이하 `framework/adapters/claude/discovery-data/`로 확정한다**(자매 memory-binding §0 memory-data/·loop-binding §0 loop-data/ 백엔드 격리 선언 동형). 이 위치는 Core 경계(`framework/core/`·`framework/runtime/`)·`specs/`·`docs/`·라이브 `.claude/` 규약 표면 **밖**이며, 발견 산출 데이터가 하네스 규약·Core와 혼입되지 않도록 격리한다(UAF-INV ① 안전 — contract-binding §4.2 격리 근거 동형). **트리는 문면 정본만이며, 물리 디렉터리·데이터 파일 생성은 v1.2 E2E Task(T-XG·T-XB) 소관이다(현 시점 미존재, §13 실측·L-07).**

### §4.1 백엔드 트리 (정본 문면 — 현 시점 미존재)

```
framework/adapters/claude/
└─ discovery-data/                          # ★ Discovery 백엔드 격리 루트 — 현 시점 미존재(E2E Task 생성 예정)
   ├─ events/                               # D1·D6 — run 단위 append-only Event 로그 + 증거(Evidence Store 물리 저장 = 동일 백엔드)
   │  ├─ greenfield-<run-id>/               #   Greenfield run 1건의 Event 로그 디렉터리
   │  │  ├─ <Event 로그 레코드…>            #     자기서술 구조화 레코드(1 Event = 1 레코드, append-only; §3)
   │  │  └─ <Discovery Request 기록>        #     이 run의 Discovery Request({mode,inputs,policy}) — 형식은 entry-binding §5.1 소유(DP-X8 해소, §4.2)
   │  ├─ brownfield-<run-id>/               #   Brownfield run 1건의 Event 로그 디렉터리(동일 구조)
   │  └─ …                                  #   run 단위 격리(<mode>-<run-id>/)
   ├─ policy/                               # D5 — Discovery Policy 데이터 파일(임계·예산·종료 규칙·충돌 게이트; 형식·값 정본 = §8)
   ├─ contracts/uahf/                       # contract-binding §4.2 정본 — 본 저장소 Contract 인스턴스 격리(참조 인용·재정의 0)
   │  └─ project-contract.v<N>.md           #     (직렬화·저장 위치 정본 = contract-binding §3·§4)
   └─ e2e-greenfield-project/               # DP-X3 — E2E Greenfield 대상 프로젝트(발견 대상)
```

- **`events/`(D1·D6, §3).** run 단위 append-only Event 로그와 증거(Evidence Store 물리 저장)를 보관한다. 위치·형식 정본은 §3.
- **`policy/`(D5, §8).** Discovery Policy 데이터 파일(임계값·예산·soft/hard 경계·종료 규칙·충돌 게이트)을 둔다. 형식·E2E 최소 실값 정본은 §8. Policy as Data이므로 값 조정은 데이터 정정일 뿐 엔진·계약 무변경이다(02 §3.15).
- **`contracts/uahf/`(참조 인용 — 재정의 금지).** 본 저장소 dogfooding Contract 인스턴스의 격리 배치 경로·파일명(`project-contract.v<N>.md`)은 **contract-binding §4.2가 소유한 정본**이다. 본 문서는 트리 완결성을 위해 **참조 인용**만 하며 Contract 직렬화·저장 위치·버저닝을 재정의하지 않는다(contract-binding §3·§4 소유·재정의 0).
- **`e2e-greenfield-project/`(DP-X3).** v1.2 E2E Greenfield 시나리오의 대상 프로젝트다(승인 계획 DP-X3). 이 디렉터리의 물리 생성·내용은 E2E Task 소관이며, 본 문서는 트리 위치만 선언한다(미완성 후속 산출물 내용 추측 금지, 07 R2).

### §4.2 Discovery Request 기록 위치 확정 (DP-X8 해소 — entry-binding §5.3 위임)

entry-binding §5.3은 Discovery Request의 물리 기록이 놓일 **백엔드 트리 위치**를 "discovery-binding.md 소관"으로 명시 위임했다(직렬화 형식·전달 방식은 entry-binding §5.1·§5.2 소유). 본 문서가 그 위치를 확정한다:

- **위치.** 한 run의 Discovery Request 기록({mode, inputs, policy} 자기서술 구조화 레코드, entry-binding §5.1)은 **그 run의 Event 로그 디렉터리(`discovery-data/events/<mode>-<run-id>/`) 안에 함께** 기록한다. Discovery Request는 그 run(= State Machine 인스턴스, 02 §3.3-A)을 결속·생성하는 입력이므로, run의 시작 기준선으로 run 디렉터리 루트에 두는 것이 자연 정합이다.
- **소유 경계.** 본 문서는 **위치만** 소유·확정하고, Discovery Request의 **직렬화 형식**은 entry-binding §5.1이 소유한다(재정의 0). 본 문서가 형식을 재서술하면 entry-binding 소관을 침범하므로 위치 확정에서 멈춘다. 이로써 entry-binding §5.3(OQ-TE-2)이 미룬 백엔드 트리 지점이 해소된다.

### §4.3 지원 구조 정직 구분 (L-07)

`discovery-data/` 트리·모든 하위 데이터는 본 문서가 확정한 **정본 문면(형태 A)**이며, 실제 디렉터리·데이터 파일 생성은 **v1.2 E2E Task(T-XG·T-XB) 소관**이다(memory-binding §2 "지원 구조 — 시연 시 생성" 선례 동형). 본 문서는 물리 데이터 자산을 생성하지 않는다 — 경로·구조·형식의 정본만 소유한다. §13이 그 실측 대조다.

---

## §5. D2 — 사용자 확인·UserOverride 채널 확정 (done 5)

02 §4.1 행2("사용자 승인/수정/강제 응답을 받는 개입 채널")의 물리 실현을 확정한다. State Machine의 사용자 개입 상태·전이(02 §3.3 Validating·§3.6·P-D5)와 관련 Event(02 §3.5)는 재정의하지 않고 § 포인터로 인용하며, 물리 개입 채널만 확정한다. **loop-binding §5.2 사람 개입 물리 채널(주 세션 사용자 제시·에스컬레이션)이 선행 관례이며, 본 절은 그와 동형으로 서술한다.**

### §5.1 물리 채널 — 주 세션 사용자 제시·응답 수령

- **제시·수령 채널.** Discovery의 모든 사용자 개입(질문 제시·확인 요청·승인/수정/강제 응답 수령)은 **주 세션**(Advisor 바인딩 — `.claude/CLAUDE.md`, advisor.md 머리 "주 세션은 기본적으로 Advisor로 동작")에서 **사용자에게 제시되고 사용자 응답을 수령**한다. 이는 loop-binding §5.2가 확정한 사람 개입 물리 채널(주 세션 사용자 제시)과 동형이다. 주 세션은 Orchestrator 역할(§7·02 §3.9)을 규약 절차로 수행하는 주체이기도 하므로, State Machine 구동과 사용자 개입 제시가 같은 주 세션 채널에서 정합한다.

### §5.2 개입 지점 3구분 (G1 Eliciting · G2 Validating · UserOverride)

세 개입 지점을 구분해 확정한다. 각 개입은 D1 Event 로그(§3)에 대응 Event로 append된다(정본 Event는 02 §3.5 실측 후 인용).

| 개입 지점 | 물리 채널 (이 환경 확정) | 대응 Event (02 §3.5) · 전이 (02 §3.3-B) |
|---|---|---|
| **G1 — Eliciting 질문/답변** | 주 세션이 적응 질문을 사용자에게 제시하고 답변을 수령한다(Eliciting 적응 질문 루프). | `QuestionAsked`(제시, T4 self) · `AnswerReceived`(응답 수령, T5 self) |
| **G2 — Validating 승인/수정** | 주 세션이 종합된 이해·가정·미해결 질문을 사용자에게 제시하고 승인/수정 응답을 수령한다(확정 게이트, P-D5). | `ValidationRequested`(확인 요청, T14 Synthesizing→Validating) · `AnswerReceived`[승인](T16 →Compiling) / [수정 요청](T17 →Eliciting) |
| **UserOverride — 사용자 강제** | 주 세션이 사용자의 강제 지시(일시중단·종료·에스컬레이션)를 수령해 State Machine에 반영한다. 사용자는 임의 비종단 상태에서 강제할 수 있다(P-D5). | `UserOverride`(T21 일시중단→Suspended / T22 종료→Aborted / T23 에스컬레이션→Escalated) |

- **확정 게이트 = 사용자 승인(불가침).** G2의 사용자 승인은 Execution Ready 확정 게이트다 — 사용자 승인 없이 `Ready`·`ReadyWithAssumptions` 종단에 도달하지 못한다(02 §3.7 Execution Ready 2축 판정의 사용자 승인 축·DISC-INV-6·ARCHITECTURE §8 UAF-INV ⑤). 본 채널 바인딩은 이 게이트를 물리 채널로 실현할 뿐 판정식을 재정의하지 않는다.
- **개입 기록.** 각 사용자 개입 발생은 D1 로그(§3)에 위 대응 Event 레코드로 남는다(02 §3.5, DISC-INV-1·DISC-INV-3). 무인 자동 개입 트리거·자동 제시 UI는 형태 B다(Bootstrap에서는 주 세션 규약 절차로 실현).
- **충돌·모호 입력 게이트 정합.** Discovery Request의 충돌·모호 입력에 대한 사용자 확인 게이트(Discovery Policy 충돌 게이트 정책, §8·02 §3.15)도 이 D2 채널(G2 계열 제시)로 실현된다 — 게이트 통과 없이 진행하지 않는다(P-D5).

---

## §6. D3 — 증거 스캔·프레이밍 물리 실현 (done 6)

02 §4.1 행3("Greenfield 프레이밍·Brownfield 증거 스캔의 물리 구현·증거 소스 접근")의 물리 실현을 확정한다. Contextualizing 상태의 mode 분기(02 §3.3-A)와 수렴(T2 self·T3 →Eliciting)은 재정의하지 않고 § 포인터로 인용하며, 물리 절차·증거 소스 접근만 확정한다. **모든 절차는 형태 A** — 주 세션이 Orchestrator 역할(§7)로 수행하고 산출 증거를 Evidence Store(= D1 백엔드, §3)에 `EvidenceRecorded` Event로 기록한다.

### §6.1 mode 분기별 물리 절차 (02 §3.3-A Contextualizing)

| mode | 물리 절차 (형태 A — 주 세션 수행) | 대응 (02 §3.3-A·§3.3-B) |
|---|---|---|
| **Greenfield** | 선재 산출물이 없으므로 **신규 문맥을 프레이밍**한다 — 프로젝트 맥락·범위를 신규로 구성하고, 실질 증거는 이어지는 Eliciting 적응 질문(§5 G1)으로 수집한다. | Greenfield 프레이밍 완료 → `ContextCaptured`(T3) → Eliciting |
| **Brownfield** | 워크스페이스의 **실 저장소 기존 산출물을 파일 시스템으로 스캔**해 증거를 수집한다(증거 소스 접근 = 파일 시스템 실측). 스캔으로 얻은 증거는 `EvidenceRecorded`로 기록된다. | Brownfield 증거 스캔 진행 → `EvidenceRecorded`(T2 self) → 스캔 완료 시 `ContextCaptured`(T3) → Eliciting |
| **Incremental** | **기존 Project Contract를 증거 기준선으로 결속**하는 스캔을 수행한다(기존 Contract 인스턴스를 증거로 결속). | Incremental 결속 스캔 → `ContextCaptured`(T3) → Eliciting (02 §3.3-A Contextualizing incremental 결속) |

세 분기는 모두 `ContextCaptured`(T3)로 수렴해 Eliciting으로 전이한다(02 §3.3-A·§3.3-B — 재정의 0).

### §6.2 증거 소스 접근 = 파일 시스템 실측 (본 저장소 dogfooding 예시)

- **증거 소스.** 이 환경에서 증거 소스 접근은 **파일 시스템 실측**이다(격리 지점이므로 구체 경로 허용). Brownfield/Incremental 스캔은 워크스페이스의 실 파일·문서·설정을 읽어 증거를 구성한다.
- **본 저장소 dogfooding 스캔 대상(예시).** 본 UAHF 저장소 자신을 Brownfield 대상으로 발견하는 dogfooding run에서, 스캔 대상은 저장소의 기존 프로젝트 콘텐츠 — `framework/`·`specs/`·`uaf/`·`docs/`·`ARCHITECTURE.md`·`ROADMAP.md` 등 — 이다(entry-binding §4.2·§6 예 B가 repository-presence = 유로 관측한 것과 동일한 콘텐츠). Entry가 **유/무만** 관측한 지점의 하류에서, Discovery는 그 콘텐츠를 **실제로 스캔·해석**한다(Brownfield Full Discovery).
- **Entry ↔ Discovery 경계.** Entry Resolution은 contract-presence·repository-presence의 **유/무만** 관측하고 증거를 수집·해석하지 않는다(entry-binding §4·01-entry EN-INV 1·2). 증거의 **실제 스캔·수집·해석**은 이 D3(Discovery Contextualizing)가 담당한다 — 두 계층은 "유무 관측(Entry)"과 "증거 스캔(Discovery)"으로 분리되며, 본 절은 후자의 물리 실현이다.
- **증거 기록.** 스캔 산출 증거는 Evidence Store(= D1 백엔드 `discovery-data/events/<mode>-<run-id>/`, §3·§4)에 `EvidenceRecorded` Event(02 §3.5)로 append된다. Evidence Store는 Discovery 내부 append-only 기록이며 UAHF Memory가 아니다(§11·02 §5 네임스페이스 구분).

---

## §7. D4 — Strategy 실행 호스팅 (역할 추상까지만) (done 7)

02 §4.1 행4의 물리 실현을 확정하되, 정본이 명시한 대로 **역할 추상까지만** 확정하고 물리 호스팅(실행 코드·자동 실행)은 **설계하지 않는다**. 02 §4.1 행4 정본: "Discovery 실행을 어느 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE.md §11)." Module부 문단도 "Strategy Provider 실행 호스팅은 **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(§3.10, ARCHITECTURE §11)"로 동일하다.

### §7.1 역할 추상 확정 (형태 A — 규약 절차·규약 역할)

- **Orchestrator 역할 = 주 세션 규약 절차.** State Machine(02 §3.3)을 구동하는 Orchestrator 모듈(02 §3.9)의 역할을 **주 세션(Advisor)이 규약 절차로 수행**한다 — Event를 받아 전이를 실행하고 현재 상태를 유지하며 종단 판정(02 §3.7)을 집행하는 것을 규약 절차로 실현한다. 전이 규칙을 새로 만들지 않는다(02 §3.3 정본 — 재정의 0).
- **레퍼런스 Provider = 규약 역할.** 02 §3.10-C가 싣는 유일 레퍼런스 Provider인 **기본 적응 질문 Provider(Default Adaptive Question Provider)**를 **규약 역할로 실현**한다 — 가장 확신이 낮은 미포화 차원을 골라 질문 집합을 내고, 모든 차원 포화·예산 소진 시 차원 포화 신호를 내는 절차(02 §3.10-C 정본)를 주 세션이 규약 역할로 수행한다. 방법론 고유명 없이 일반형 기본값으로만 실현한다(02 §3.10-D·UAF-INV ⑥ — 정본 청정).
- **물리 호스팅 = 설계 안 함(확장 포인트).** Discovery를 실행 코드로 자동 호스팅하는 물리 실행 주체·자동화는 **설계하지 않는다**. 물리 호스팅 설계는 ARCHITECTURE §11 확장 포인트("Discovery 실행 호스팅 — 역할 추상까지만 정의하고 물리 호스팅은 설계하지 않는다")를 침범하므로 금지된다. 실행 코드(사이클 구동 로더·자동 실행)는 형태 B로 미도입이며, 그 경계 간 분할은 형태 B 설계 시 확정한다(선취·추측 금지).

### §7.2 Strategy Invariance 훼손 0 (DISC-INV-7)

- **교체되는 것 = Provider뿐.** 교체 가능한 것은 Strategy Registry에 등록되는 Strategy Provider뿐이며(02 §3.9·§3.10), Orchestrator·Confidence Model·Contract Compiler·Discovery Policy의 계약과 출력(Project Contract 스키마·완결 기준)은 어떤 Provider에서도 불변이다(DISC-INV-7·ARCHITECTURE §8 UAF-INV ③). 본 절의 역할 추상 바인딩은 레퍼런스 Provider 1건을 규약 역할로 실현할 뿐, State Machine·Event·Contract 완결 기준을 바꾸지 않는다(02 §3.10-B 불변). 어떤 Strategy를 쓰든 산출은 동일한 Project Contract다 — Strategy Invariance 훼손 0.

---

## §8. D5 — Discovery Policy 값 데이터 소스·직렬화 + E2E 최소 실값 (done 8 · DP-X5)

02 §4.2 Module부 문단("Question Engine의 예산·Discovery Policy의 정책 값(임계값·예산·경계 수치)의 데이터 소스·직렬화는 Adapter 소관이다 — §3.14·§3.15")의 물리 실현을 확정한다. Discovery Policy 계약(02 §3.15 Policy as Data)·Question Budget 계약(02 §3.14)·Confidence 임계(02 §3.12)는 재정의하지 않고 § 포인터로 인용하며, 데이터 소스·직렬화 형식과 **E2E 구동용 최소 실값 1세트**만 확정한다.

### §8.1 데이터 소스·직렬화 형식

- **데이터 소스.** Discovery Policy 정책 값은 엔진에 하드코딩되지 않고 `framework/adapters/claude/discovery-data/policy/`의 **데이터 파일**에서 온다(Policy as Data, 02 §3.15). Discovery Request의 `policy` 요소(ARCHITECTURE §12.2)가 이 정책을 참조로 담는다(entry-binding §5.1 `policy: <Discovery Policy 참조>` 정합).
- **직렬화 형식.** 정책 파일은 자기서술 구조화 데이터로 직렬화한다(자매 바인딩의 구조화 데이터 관례 동형·구체 형식은 Adapter 선택, 격리 지점 §12). 물리 정책 데이터 파일(`policy/`)의 생성은 E2E Task 소관이며, 본 문서는 **형식·값 정본 문면만** 소유한다(L-07 — 미존재 정직 구분).

### §8.2 E2E 구동용 최소 실값 1세트 (정본 값 표 — DP-X5)

E2E 구동을 위한 **최소 실값 1세트**를 본 문서의 정본 값 표로 확정한다. 이 값들은 **Policy as Data**이므로 값 조정은 데이터 정정일 뿐 엔진·정본 계약을 변경하지 않는다(02 §3.15 — "정책 값 변경은 엔진(모듈 코드) 변경을 요구하지 않는다"). 4개 정책 항목(02 §3.15 표: 임계값·예산·종료 규칙·충돌 게이트)을 모두 채운 단일 기본 프로파일이다.

**(가) 임계값 정책 — 차원별 Confidence 포화·Ready 임계 θ (02 §3.11 5차원·§3.12 [0,1] 스칼라):**

| Discovery Dimension (02 §3.11) | 포화·Ready 임계 θ |
|---|---|
| Intent | 0.80 |
| Requirement | 0.75 |
| Constraint | 0.70 |
| Risk | 0.70 |
| Architecture | 0.75 |

**(나) 예산 정책 — Question Budget (02 §3.14 총량·차원별·soft/hard):**

| 항목 | 값 |
|---|---|
| 총량 예산 | 40 |
| 차원별 예산 (Intent / Requirement / Constraint / Risk / Architecture) | 10 / 10 / 6 / 6 / 8 (합 40) |
| soft 경계 | 30 (총량의 75%) — 초과 시 적응 압박, 잔여 예산 > 0이면 Eliciting 계속(T8) |
| hard 경계 | 40 (총량) — 소진 시 강제 Synthesize 전이(T11) |
| 재진입 보충 예산 상한 (T17 수정 요청 재진입, §3.14-A) | 10 (총량의 25%) — Policy 상한 아래에서 부여, 재진입 후에도 hard 경계 규칙(T11·T15) 적용 |

**(다) 종료 규칙 정책 (02 §3.6 Termination·§3.13 깊이 조정):**

| 경로 (02 §3.6) | 조건 (값) |
|---|---|
| ① 2축 게이트 충족 → `Ready` | Completeness ∧ 전 5차원 θ(위 (가)) 충족 ∧ 사용자 승인 (02 §3.7·T19) |
| ② 예산 소진 + Confidence 미달 | 필수 코어 필드 가정 충족 가능 → `ReadyWithAssumptions`(Assumption Ledger 필수, T20); 가정으로도 충족 불가 → `Escalated`(T15) |
| 깊이 조정 (02 §3.13) | 기본 프로파일 = 위 (가)·(나) 값. 규모·리스크 상향 시 해당 차원 목표 임계·예산 가산은 **Policy 데이터로 조정**(엔진 무변경) |

**(라) 충돌 게이트 정책 (02 §3.6·§3.15 충돌 게이트·P-D5):**

| 항목 | 값 |
|---|---|
| 충돌·모호 입력 게이트 | 충돌·모호 입력 감지 시 **사용자 확인 게이트 필수**(Validating 경유 — §5 G2/D2 채널) — 게이트 통과 없이 진행 불가(Preserve Human Authority, P-D5) |

- **Policy as Data 불변.** 위 값(임계·예산·경계·종료 규칙·게이트)은 전부 데이터이며, 값을 바꾸는 것만으로 Discovery 거동이 조정된다 — Confidence Model·Question Engine·Orchestrator 등 엔진(모듈)이나 정본 계약(State Machine·Event·완결 기준)은 변경되지 않는다(02 §3.15). 이 값 세트는 **E2E 구동을 위한 최소 실값**이며, 다른 임계·예산이 필요하면 `policy/` 데이터 정정으로 조정한다.
- **미존재 정직 구분(L-07).** 위 값은 본 문서가 소유하는 **정본 값 문면(형태 A)**이며, 물리 데이터 파일(`discovery-data/policy/`)은 현 시점 미존재로 E2E Task가 이 값 그대로 생성할 예정이다(§13 실측).

---

## §10. DP-X6 해소 — Provenance 컨테이너 내부 형식 (done 9)

contract-binding §6은 Contract 인스턴스 front-matter 내 분리 네임스페이스 `provenance` 컨테이너의 **외형·must-ignore 경계**만 확정하고, 그 **내부 직렬화 형식·필드**를 "discovery-binding.md(예정) 소관"으로 명시 위임했다(DP-X6, planning/specs/03 §3.2-D 불투명 부속 동형). 본 절이 그 내부 형식을 확정한다.

### §10.1 내부 형식 = Discovery 실행 메타

`provenance` 컨테이너 내부는 **Discovery 실행 메타**를 담는 자기서술 구조화 블록이다. 최소 구성:

| 내부 필드 (Discovery 실행 메타) | 값 형태 | 참조 대상 |
|---|---|---|
| run 식별자 | 문자열 — 해당 Discovery run(State Machine 인스턴스, 02 §3.3-A)의 `<run-id>` | `discovery-data/events/<mode>-<run-id>/`(§4) |
| Event 로그 참조 | 참조 — 이 run의 Event 로그 디렉터리 경로/참조(§3·§4) | D1 백엔드(§3) |
| mode | 문자열 — greenfield / incremental / brownfield 등(ARCHITECTURE §12.2 확장 네임스페이스) | Discovery Request `mode`(entry-binding §5.1) |
| Policy 참조 | 참조 — 이 run이 사용한 Discovery Policy 참조(§8) | `discovery-data/policy/`(§8·02 §3.15) |

- 위는 **최소 표면**이며, 감사·재현에 필요한 추가 Discovery 실행 메타(예: Readiness 선언 참조·Assumption Ledger 참조)를 담을 수 있다. 어느 필드도 경량 **참조**이며, Event 로그·증거 원문을 컨테이너에 중복 저장하지 않는다(loop-binding §5.3 경량 참조 관례 동형).

### §10.2 planning/specs/03 §3.2-D 불투명 계약 유지 — UAHF must-ignore 불변

- **must-ignore 경계 불변.** UAHF tolerant reader는 `provenance` 컨테이너(및 그 하위 전체)를 **must-ignore**한다 — 존재를 오류로 취급하지 않고 소비하지 않는다(contract-binding §6·planning/specs/03 §3.2-D·§3.3-C). 본 절이 내부 형식을 채워도 이 must-ignore 경계는 불변이다. 내부 필드는 **Discovery 측 소비 전용**(감사·재현·계보 추적)이며, UAHF는 이 컨테이너를 읽지 않는다.
- **누출 차단(DISC-INV-8).** Provenance 내부는 Contract **코어 스키마 밖**의 불투명 부속이다. Discovery 실행 메타(run 식별자·Event 로그 참조·mode·Policy 참조)는 코어 필드(Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger 등)로 새어나가지 않는다 — Discovery 내부 변경(기법·전략·예산·질문 방식)이 만드는 실행 메타는 `provenance`에만 반영되고 코어 스키마·UAHF 접점에 도달하지 못한다(contract-binding §6·PC-INV 2·10, DISC-INV-8). 이 컨테이너는 그 누출을 막는 격리 경계 뒤에 놓인다.
- **창설 금지.** 본 절은 planning/specs/03 §3.2-D 불투명 부속 계약을 재정의하지 않고 그 **내부 형식만** 채운다. Contract 코어 스키마·버저닝·tolerant reader 계약을 변경하지 않는다(contract-binding §3·§5·§6 소유·재정의 0). 이로써 contract-binding §11(OQ-TC-2)이 미룬 Provenance 내부 형식 지점이 해소된다.

---

## §11. 상시 불변 자기 점검 (done 10)

본 물리 바인딩이 상시 불변(ARCHITECTURE §7.1 2건·02 DISC-INV)을 훼손하지 않음을 자가 스캔으로 점검한다. 자체 점검은 최종 승인이 아니다 — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다(specs/02-agent.md §3.2-A — Agent 역할 경계; 본 문서에서 "02"는 달리 명시하지 않는 한 discovery/specs/02-discovery.md를 가리킨다).

### §11.1 상시 불변 ① — Discovery 교체 가능 Compiler (누출 0)

- **점검 대상(scope).** 본 문서가 확정하는 물리 실현부 — Event 로그(§3)·백엔드 트리(§4)·D2 채널(§5)·D3 스캔(§6)·D4 역할(§7)·Policy 값(§8)·Provenance 내부(§10) — 가 Discovery 내부 개념을 **Contract 코어 스키마·UAHF 접점**으로 누출시키는지 스캔한다.
- **다중 패턴 자가 스캔.** Discovery 내부 개념 다중 패턴 — { 질문 · 전략(Strategy) · 예산(Budget) · Capability } — 이 **Contract 코어 스키마·UAHF 접점 정의로 쓰인 지점 0건**이다. 본 문서에서 이 어휘는 오직 (i) 02 정본 § 포인터 인용, (ii) Discovery **내부** 실현 서술(Event 로그·Policy 값·레퍼런스 Provider 역할 — 전부 Discovery 측), (iii) 불변·경계·근거 서술(본 §11·§7.2·§10.2의 누출 차단 문면)에만 등장한다. Contract 코어 필드·UAHF 소비 표면을 정의·확장하는 자리에는 0건이다 — **mention(내부 실현·불변·경계 서술)과 use(Contract 코어/UAHF 접점 정의)의 경계**를 지킨다.
- **경계 문면 (Provenance 내부·Event 로그는 대상 아님).** Provenance 내부 형식(§10)·Event 로그(§3)·Evidence Store(§4)는 **Discovery 내부 기록**이며 must-ignore 경계·격리 경계 뒤에 있다(§10.2·02 §5). 이들은 Contract 코어 스키마·UAHF 접점이 아니므로 누출 스캔의 **대상이 아니다** — run 식별자·Event 참조·mode·Policy 참조를 담아도 그것은 Discovery 측 소비 전용 실행 메타이지 Contract 코어/UAHF로의 누출이 아니다. 이 경계 구분이 상시 불변 ①(Discovery 교체 가능·DISC-INV-7·8·ARCHITECTURE §7.1 ①)과 정합한다.

### §11.2 상시 불변 ② — Contract Stable Contract 훼손 0

- **Contract 스키마·버저닝 재정의 0.** 본 문서는 Project Contract의 스키마·필수 코어 필드·버저닝(SemVer·tolerant reader·필드 제거 금지)을 재정의하지 않는다 — 이는 planning/specs/03·contract-binding.md 소관이며, 본 문서는 `contracts/uahf/` 경로를 **참조 인용**만 하고(§4.1), Provenance는 **내부 형식만** 채우며 외형·must-ignore 경계는 contract-binding §6 소유대로 유지한다(§10). 장기 호환성 규칙 훼손 서술 0건 — Stable Contract(Public API) 지위 불변(ARCHITECTURE §7.1 ②·§8 UAF-INV ①②).

### §11.3 Evidence Store ≠ UAHF Memory 네임스페이스 구분 (02 §5)

- **네임스페이스 구분.** Discovery Event 로그·Evidence Store(§3·§4, `discovery-data/`)는 Discovery **내부 append-only 기록**이며 **UAHF Memory가 아니다**(02 §5 네임스페이스 구분). 물리적으로도 discovery-data/(Discovery 백엔드)와 memory-data/(UAHF Memory 백엔드, memory-binding.md)는 별개 격리 트리다 — 혼동·혼입하지 않는다.
- **Discovery의 Memory 비활용 유지(02 §5).** Discovery는 v1.1에서 UAHF Memory를 회수·활용하지 않는다(Memory Consult 비담당, ARCHITECTURE §10 비담당 ④). 본 문서는 Discovery의 Memory 활용 경로를 설계하지 않는다 — 그것은 확장 포인트로만 열려 있고(ARCHITECTURE §11), 본 바인딩은 이를 훼손하지 않는다. 어떤 §도 Discovery가 UAHF Memory를 회수·기록하는 물리 절차를 도입하지 않는다.

---

## §12. 02 §4.2 이식 교체 지점 대응 (done 11)

02 "### 4.2 이식 교체 지점"의 **4불릿** + "Module부 바인딩" 문단 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 02 §3 Core Contract 불변(structure.md §7 C-1 동형)을 재확인한다.

| 02 §4.2 교체 지점 (바뀌는 것) | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (02 §3 불변) |
|---|---|---|---|
| Event 로그 직렬화 포맷·저장 위치 → 대상 환경의 로깅 메커니즘 | §3, §4 | 자기서술 구조화 레코드 append-only 로그·`discovery-data/events/<mode>-<run-id>/` 위치·순서 값 물리 표현. | §3.3 State Machine·§3.5 Event Model 15·§3.6 Termination(전이·Event·종단 정본, DISC-INV-1·3). |
| 사용자 확인·Override 채널 → 대상 환경의 사람 개입 메커니즘 | §5 | 주 세션 사용자 제시·응답 수령 채널(G1·G2·UserOverride). | §3.3 Validating·§3.6·§3.7 사용자 승인 축(확정 게이트, DISC-INV-6·UAF-INV ⑤). |
| 증거 소스 접근·스캔 구현 → 대상 환경의 증거 수집 메커니즘 | §6 | Greenfield 프레이밍/Brownfield 파일 시스템 스캔/Incremental 결속의 형태 A 절차·파일 시스템 실측 접근. | §3.3-A Contextualizing mode 분기·수렴(T2·T3), Evidence Store append-only(§3.9, DISC-INV-3). |
| Strategy 실행 환경 → 대상 환경의 실행 주체 | §7 | 주 세션(Advisor) Orchestrator 역할·레퍼런스 Provider 규약 역할(역할 추상까지만). | §3.1 Strategy Invariance·§3.9 모듈 경계·§3.10 Provider 계약(DISC-INV-7·UAF-INV ③⑥). |
| **Module부 바인딩** — 예산·Policy 값 데이터 소스·직렬화 → 대상 환경의 데이터 소스; Evidence Store 물리 저장 = Event 로그 바인딩과 동일 | §8; §3·§4 (D6=D1) | `discovery-data/policy/` 형식·E2E 최소 실값; Evidence Store = Event 로그 백엔드(동일). | §3.14 Question Budget·§3.15 Policy as Data(정책 변경 ↔ 엔진 무변경); §3.9 Evidence Store 모듈 경계. |

- **"유지되는 것" 열의 이식 불변성.** 위 계약(§3.3 State Machine·§3.5 Event Model·§3.6 Termination·§3.7 판정식·§3.8 Invariants·§3.9 모듈 경계·§3.10 Provider 계약·§3.15 Policy as Data)은 다른 AI·실행 환경으로 이식해도 바뀌지 않는다 — 02 §4.2 "유지되는 것" 목록의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 본 문서는 02 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고, v1.2 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §13. 상태 서술 실측 대조 (L-07 — 미존재를 실재로 쓰지 않음)

본 문서의 "실재/미존재" 서술을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-07 작성 시 `ls`/`test` 직접 실측.** 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다.

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-07, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/discovery-binding.md` | 실재 (본 문서) | 실재 (이 파일 — 신규 생성). |
| `framework/adapters/claude/contract-binding.md` (선행 확정, T-C) | 실재 (§3·§4·§6 소비·위임 해소 대상) | 실재 — 확인(무수정, § 포인터·DP-X6 위임 해소 대상). |
| `framework/adapters/claude/entry-binding.md` (선행 확정, T-E) | 실재 (§5.1·§5.3 소비·위임 해소 대상) | 실재 — 확인(무수정, § 포인터·DP-X8 위임 해소 대상). |
| `framework/adapters/claude/memory-binding.md`·`loop-binding.md` (골격·채널 선례) | 실재 (자매 문서) | 실재 — 확인(무수정, §5.2 채널 선례·백엔드 격리 선례). |
| uaf/specs/02-discovery.md (바인딩 대상 정본) | 실재 (v1.1 Baseline) | 실재 — §3·§4 확인(무수정, § 포인터 대상). |
| uaf/ARCHITECTURE.md §7·§8.2 (경계·추상 정본) | 실재 (v1.1 Baseline) | 실재 — §7 확장 포인트·§8.2 Discovery Request 추상 확인(무수정). |
| `framework/adapters/claude/discovery-data/` (Discovery 백엔드 루트) | **지원 구조 — 현 시점 미존재, v1.2 E2E Task 생성 예정** | **미존재** — 디렉터리 부재 확인(delegation 전제 정합). 경로·구조·형식·값은 본 문서 정본 문면. 생성하지 않음. |
| `discovery-data/events/`·`policy/`·`e2e-greenfield-project/` 하위 데이터 | **미존재** (E2E Task 생성 예정) | **미존재** — 상위 `discovery-data/` 자체가 부재. |
| `discovery-data/contracts/uahf/` (contract-binding §4.2 참조 인용) | **미존재** (E2E Task 생성 예정; 경로 정본 = contract-binding §4.2) | **미존재** — 상위 `discovery-data/` 부재(contract-binding §10 실측과 정합). |
| 본 UAHF 저장소 기존 프로젝트 콘텐츠 (D3 Brownfield dogfooding 스캔 대상 예시) | 실재 (`framework/`·`specs/`·`uaf/`·`docs/` 등) | 실재 — 루트에 `ARCHITECTURE.md`·`framework`·`specs`·`uaf`·`docs`·`ROADMAP.md`·`README.md` 등 실측(entry-binding §10 repository-presence 유 근거와 정합). |
| 본 저장소 VCS 마커(`.git`) | 부재 (비git 저장소 — D3 스캔은 파일 시스템 실측, VCS 비의존) | 부재 — `.git` 없음 확인(entry-binding §10 실측과 정합). |
| Event 로거·직렬화기·스캔 로더(형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). |

- **핵심 구분.** 본 문서가 확정한 Event 로그 직렬화 형식·백엔드 트리·D2 채널·D3 절차·Policy 값·Provenance 내부 형식은 **정본 문면(형태 A)**이며, 물리 데이터 자산(`discovery-data/…`)은 **현 시점 미존재**로 v1.2 E2E Task(T-XG·T-XB)가 이 정본 구조·값 그대로 생성할 예정이다. 데이터 생성 주체는 E2E Task이며, 본 문서는 구조·형식·경로·값의 정본만 소유한다(memory-binding §2·§7 선례 동형, L-07).
- 실측과 불일치하는 서술은 0건이다 — 미존재(`discovery-data/`)를 실재로, 실재(자매 바인딩·02·uaf/ARCHITECTURE 정본·기존 프로젝트 콘텐츠)를 미존재로 쓰지 않았다.

---

## §14. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 discovery/specs/02 §3·§4의 물리 실현이다. 어떤 Event·상태·전이·모듈 경계·Provider 계약·Dimension·Confidence·Question Budget·Discovery Policy·불변(DISC-INV 1~9)도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 02 §3이다. 새 계약 요소(Event·상태·전이·모듈·Provider 필드·Policy 항목·불변)를 창설하지 않았다. 방법론 고유명 0건(02 §3.10-D·UAF-INV ⑥ — 정본 청정).
- **본 문서가 소유·확정하는 것.** 02 §4.1·§4.2가 "Adapter 소관"으로 미룬 지점 — ① D1 Event 로그 직렬화(§3) ② discovery-data/ 백엔드 트리(§4) ③ D2 사용자 확인/UserOverride 채널(§5) ④ D3 증거 스캔/프레이밍 절차(§6) ⑤ D4 Strategy 실행 호스팅 **역할 추상**(§7) ⑥ D5 Policy 값 데이터 소스·직렬화 + E2E 최소 실값(§8) ⑦ D6 Evidence Store 물리 저장(= D1) — 과, 선행 위임 해소 ⑧ DP-X6 Provenance 내부 형식(§10) ⑨ DP-X8 Discovery Request 기록 위치(§4.2)를 확정한다. D4 물리 호스팅은 **설계하지 않는다**(ARCHITECTURE §11 확장 포인트).
- **격리 토큰의 단일 자리.** 구체 직렬화 형식·물리 경로(`framework/adapters/claude/discovery-data/…`)·파일 확장자·Policy 수치는 이 Adapter 경계 문서에 둔다. UAF 정본(discovery/specs/02)은 이 토큰을 "Adapter 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3는 이 경계에 비적용 — 격리 보유).
- **동시 작성 문서 경계(07 R2·R4).** 본 산출은 이 1개 파일(`framework/adapters/claude/discovery-binding.md`)만 생성하며, 미완성 후속 산출물(E2E 데이터·`discovery-data/` 트리 내용)을 인용·추측하지 않았다 — 위치·구조·형식·값의 정본 문면만 소유했다(07 R2). 확정된 인터페이스 계약(discovery/specs/02 §3·§4·contract-binding §3·§4·§6·entry-binding §5.1·§5.3·ARCHITECTURE §11·§12.2)만 참조했다. uaf/ 정본·UAHF 정본·기존 바인딩(contract-binding·entry-binding 포함)·물리 데이터를 수정·생성하지 않았다(07 R4·INV-2). 불확실 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, specs/02-agent.md O4).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-TD-1 (Policy 최소 실값 수치 — 비차단).** §8.2 E2E 최소 실값 1세트(차원 임계 θ 0.70~0.80·총량 예산 40·차원별 배분·soft 30/hard 40·보충 상한 10)는 E2E 구동을 위한 본 문서의 Adapter 재량 확정이며(DP-X5가 "본 문서 정본 값 표로 확정"으로 위임), Policy as Data이므로 값 조정은 데이터 정정일 뿐 엔진·정본 계약(02 §3.12·§3.14·§3.15) 변경이 아니다. E2E 시나리오가 다른 임계·예산 프로파일을 요구하면 Advisor 재확정 또는 `policy/` 데이터 정정으로 조정 가능하다 — 계약 변경이 아니므로 비차단이다.
- **OQ-TD-2 (run-id·레코드 파일 단위 명명 — 후속/비차단).** §3.4·§4는 Event 로그를 `discovery-data/events/<mode>-<run-id>/` run 단위로 격리하고, run 디렉터리 내 레코드 파일 단위·명명 세부는 Adapter 재량으로 두었다(승인 계획 위임). 물리 생성 시(E2E Task) 정확한 run-id 발급 규칙·레코드 파일 명명의 물리 확정이 필요하다. append-only·순서 값 성격(§3.2·§3.3)은 어느 명명에서도 유지되므로 계약(02 §3.5·DISC-INV-3) 변경은 아니다 — 비차단이다.

---

## §15. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 **UAF 정본(discovery/specs/02-discovery) 바인딩** 산출물(DP-X1). 정본 = 02 §3·§4(본 문서는 물리 실현, 재정의 아님 — §0). 자매 contract-binding.md·entry-binding.md와 같은 UAF 레벨 바인딩·접두 없는 동형 파일명.
- **§2:** 02 "### 4.1" 표 **4행(D1~D4)** + "### 4.2" Module부 문단 **2지점(D5·D6)**을 물리 실현으로 매핑(실재/규약 실현(형태 A)/형태 B 3구분). D6 = D1과 동일 백엔드(02 §4.2 문면).
- **§3 (D1):** Event 15종(02 §3.5 재실측) append-only 로그 = 자기서술 구조화 레코드(1 Event = 1 레코드)·위치 `discovery-data/events/<mode>-<run-id>/`. 순서 값 ↔ 물리 생성 시각 성격 구분(L-09). 모든 전이는 Event로만(DISC-INV-1·3, § 포인터 인용).
- **§4:** discovery-data/ 백엔드 트리 정본 선언(`events/`·`policy/`·`contracts/uahf/`(contract-binding §4.2 참조 인용)·`e2e-greenfield-project/`(DP-X3)) + Discovery Request 기록 위치 = run Event 로그 디렉터리(DP-X8 해소·형식은 entry-binding §5.1 소유). 트리 문면 정본만·물리 생성은 E2E Task(L-07).
- **§5 (D2):** 주 세션 사용자 제시·응답 수령 채널(loop-binding §5.2 동형) — G1 Eliciting(QuestionAsked·AnswerReceived)·G2 Validating(ValidationRequested·AnswerReceived 승인/수정 T16·T17)·UserOverride(T21~T23) 구분. 각 개입은 Event로 기록. 사용자 승인 확정 게이트 불가침(DISC-INV-6).
- **§6 (D3):** Greenfield 프레이밍/Brownfield 파일 시스템 스캔(T2)/Incremental 결속의 형태 A 절차(주 세션 수행·Evidence Store 기록). 증거 소스 = 파일 시스템 실측(본 저장소 dogfooding 대상 예시). Entry 유무 관측 ↔ Discovery 증거 스캔 경계.
- **§7 (D4):** 주 세션(Advisor) Orchestrator 역할(§3.9)·레퍼런스 Provider(§3.10-C)를 **역할 추상까지만** 실현·물리 호스팅 설계 0(ARCHITECTURE §11). Strategy Invariance 훼손 0(DISC-INV-7).
- **§8 (D5):** `discovery-data/policy/` 형식 + **E2E 구동용 최소 실값 1세트 정본 값 표**(차원 임계 θ·Budget 총량 40/차원별·soft 30/hard 40·보충 10·종료 규칙·충돌 게이트). Policy as Data — 값 조정 = 데이터 정정(엔진·계약 무변경, 02 §3.15).
- **§10 (DP-X6):** Provenance 내부 = Discovery 실행 메타(run 식별자·Event 로그 참조·mode·Policy 참조). planning/specs/03 §3.2-D 불투명 계약 유지·UAHF must-ignore 불변·Discovery 측 소비 전용·누출 차단(DISC-INV-8).
- **§11:** 상시 불변 자기 점검 — Discovery 내부 개념(질문·전략·예산·Capability) Contract 코어/UAHF 접점 누출 0(다중 패턴·mention/use 경계; Provenance 내부·Event 로그는 Discovery 내부 기록이므로 대상 아님)·Stable Contract 훼손 0·Evidence Store ≠ UAHF Memory 네임스페이스 구분(02 §5).
- **§12:** 02 "### 4.2" 이식 교체 지점(4불릿 + Module부) 대응 표 — 유지 열 = §3.3·§3.5·§3.6·§3.7·§3.8·§3.9·§3.10·§3.15(C-1 동형).
- **§13:** 실측 대조 — `discovery-data/` 현 시점 미존재(E2E Task 생성 예정), 자매 바인딩·02·ARCHITECTURE 정본·기존 프로젝트 콘텐츠 실재, `.git` 부재. 미존재를 실재로 쓰지 않음(L-07).
- 02 §3·§4·UAHF 정본 재정의 0, Glossary 용어 신설 0, 새 계약 요소 창설 0, 방법론 고유명 0, 실행 코드 0(형태 A). 구체 직렬화 형식·물리 경로·Policy 값 토큰은 이 Adapter 경계에서 허용된다(격리 지점).
