# framework/adapters/claude/entry-binding — Claude Code Entry Layer Adapter 바인딩

작성일: 2026-07-07
상태: v1.2 Baseline (CP2 첫 판정 Pass 16/0/0 · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: AGENT.md
근거 정본:

- entry/specs/01-entry.md §3.1(Interface — Entry & Entry Resolution 연산·Entry 2종 `/new`·`/continue`)·§3.2-A(Entry Descriptor 등록 모델 5필드·Resolution 엔진 고정 5단계)·§3.2-B(Discovery Request 매핑 — §12.2 정합 채움 규칙)·§3.2-C(Workspace Evidence & Evidence Source 확장 스키마 — contract-presence·repository-presence capability 선언·유/무 값 도메인)·§3.2-D(결정 테이블 전 8조합·판별 규칙 D3 ①②③)·§3.2-E(mode 네임스페이스)·§3.3(EN-INV 1~6)·§4.1(### §4.1 바인딩 대상, 불릿 3건)·§4.2(### §4.2 이식 교체 지점)·§8(Examples — 예1 결정 테이블 적용·예3 `/import` 등록). 본 문서가 물리 실현으로 바인딩하는 계약의 정본. **재정의·확장하지 않고 § 포인터로만 인용한다.**
- ARCHITECTURE.md §12.2(Discovery Request 인터페이스 추상 — 3요소 {mode, inputs, policy}). Entry Resolution 산출이 정합해야 하는 상위 데이터 계약 추상. 재정의 0.
- framework/adapters/claude/contract-binding.md §3(Contract 직렬화 = Markdown 본문 + YAML front-matter 단일 문서)·§4(저장 위치 이원화 — 일반 관례 `.claude/project-contract/`·본 저장소 인스턴스 `framework/adapters/claude/discovery-data/contracts/uahf/`·파일명 `project-contract.v<N>.md`)·§4.1(**"존재 판정 수단(탐지 실행)의 상세는 후속 entry-binding.md 소관"으로 명시 위임**). 선행 확정 인터페이스(T-C 폐합) — 본 문서 §4가 그 위임을 해소한다.
- framework/adapters/claude/memory-binding.md — 자매 Adapter Binding 골격 선례. 제목 라인 → 작성일·상태·상위 규약·근거 정본 → 거버넌스 문단 → §9 이력(머리 배치) → §0 정본 경계 → §1 목적 → 바인딩 표 물리 실현(실재/규약 실현/형태 B 3구분) → 물리 절차/매핑 절 → 이식 교체 지점 표("유지되는 것" 열 = C-1 재확인) → 실측 대조 절(L-07) → self-note·open_questions → 요약의 관례.
- .claude/commands/uahf-status.md — Presentation/진입 명령 골격 선례(형태 A·YAML front-matter `description:`·정본 포인터 전용·값 하드코딩 0). 본 문서가 확정하는 두 진입 명령(uaf-new·uaf-continue)의 골격 준거.
- framework/core/structure.md §2(4경계 배치 — `framework/adapters/<adapter>/` = 환경 의존 격리 경계, `.claude/` 진입 표면은 Adapter 성격)·§5(금지 토큰 규칙 C-3 — Adapter 경계는 격리 보유로 비적용). 본 문서 경계·격리 토큰 허용의 근거.
- specs/00-glossary.md — UAHF 용어 정본. 본 문서는 새 용어를 신설하지 않는다. `형태 A/B`는 structure.md §4의 서술 라벨 인용이며 Glossary 표제어가 아니다.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core·UAF 계약을 특정 실행 환경·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 직렬화 형식·물리 경로·환경 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, 자매 memory-binding.md §0·contract-binding.md §0과 동형). 단 이 문서는 UAF 정본(entry/specs/01-entry.md §3·§4)과 UAHF 정본을 **재정의하지 않는다** — 계약(Entry Descriptor 모델·엔진 5단계·결정 테이블·Evidence 스키마·EN-INV)은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-07 | v1.2 Draft | 최초 작성. `framework/adapters/claude/` 경계의 **UAF 정본(uaf/specs/01-entry) 바인딩** 산출물(자매 contract-binding.md와 동형·접두 없음). 01 "### §4.1 바인딩 대상" **3불릿 전건**을 Claude 환경 물리 실현으로 확정(§2 — 실재/규약 실현(형태 A)/형태 B 3구분). **E1**(진입 트리거 물리 형태) = 논리 Entry `/new`·`/continue`(01 §3.1·§0 논리 식별자)의 물리 발화 형태를 `.claude/commands/uaf-new.md`·`uaf-continue.md` 문서 명령으로 확정(§3 — uahf-status.md 선례 동형·형태 A·정본 포인터 전용). **E2**(Workspace Evidence 관측) = contract-presence 존재 판정 수단(탐지 절차 — contract-binding §4.1 위임 해소)·repository-presence 판정 수단(기존 프로젝트 콘텐츠 유무 — 01 §3.2-C capability 정합·비git 저장소 실측 해소) 확정(§4). **E3**(Discovery Request 직렬화) = {mode, inputs, policy} 구조화 레코드 직렬화·전달 방식 확정, 기록 백엔드 트리는 discovery-binding.md(예정) 포인터 위임(§5 — DP-X8). 결정 테이블 행 1(greenfield)·행 6(brownfield, D3 ②) 물리 관측 → 단일 Discovery Request 산출 예시(§6 — 01 §3.2-D 재정의 0·행 인용만). EN-INV 1·2·3·5 자기 점검(§7). 01 "### §4.2" 이식 교체 지점 대응 표(§8 — "유지되는 것" 열 = 01 §3 불변 재확인). 상태 서술 실측 대조(§10 — 신규 3파일 실재·uahf-status.md/contract-binding.md 실재·discovery-data/ 미존재·`.claude/project-contract/` 본 저장소 미존재·비git(.git 부재) 실측, L-07). 실행 코드 0(형태 A, D-v1.2-1). 01 §3·§4·UAHF 정본 재정의 0·§ 포인터 인용만·새 계약 요소(Descriptor 필드·연산·불변·kind) 창설 0. 동시 작성 병렬 산출물·미완성 후속 산출물(discovery-binding 등) 불인용(07 R2) — 포인터 위임만. | Worker (Advisor 위임, Task T-E) |
| 2026-07-07 | v1.2 Baseline | v1.2 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass 16/0/0; CP3 Advisor 승인) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, 자매 memory-binding.md §9·contract-binding.md §9·framework/core/structure.md §9 동형. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **UAF 정본 바인딩 선언(DP-X1).** 이 문서는 `framework/adapters/claude/` 경계의 Adapter Binding 문서이되, 그 **바인딩 대상 정본은 UAHF spec이 아니라 UAF 정본 `entry/specs/01-entry.md` §3·§4다.** 자매 바인딩 12문서(runtime·memory·verifier·loop·workflow·hooks·skills·plugins·agent·scaffold·harness-binding + adapter-conformance)가 UAHF spec(specs/01~13)을 바인딩하는 것과 달리, 본 문서는 UAF 레벨의 Entry Layer & Entry Resolution 정본을 바인딩한다(자매 contract-binding.md와 같은 부류). 파일명·골격 관례는 자매와 동형이다(접두 없음).
- **정본은 entry/specs/01 §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소 — Entry Descriptor 등록 모델·5필드(§3.2-A)·Resolution 엔진 고정 5단계(§3.2-A)·Discovery Request 매핑(§3.2-B)·Evidence Source 확장 스키마(§3.2-C)·결정 테이블 8조합·D3(§3.2-D)·mode 네임스페이스(§3.2-E)·불변 EN-INV 1~6(§3.3) — 를 **재정의·확장하지 않는다.** 계약 요소는 정본 § 포인터로만 인용한다. 본 문서가 확정하는 것은 01 §4.1이 "Adapter 소관"으로 미룬 **3불릿(E1 진입 트리거 물리 형태·E2 Evidence 관측 물리 실현·E3 Discovery Request 직렬화)**뿐이다(§2).
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문, 그리고 UAF 정본(entry/specs/01) 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이다(structure.md §5 C-3 확장·01 §0 Core 문서 관행). 이 문서는 그 **반대편**이다 — 구체 직렬화 형식·물리 경로(`framework/adapters/claude/…`·`.claude/…`)·파일 확장자·명령 이름의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(memory-binding.md §0·contract-binding.md §0과 동형). 단 **UAF 정본이 명명하지 않은 것을 UAF 정본 문면인 것처럼 서술하지 않는다** — 물리 확정은 전부 본 문서 소유임을 명시한다.
- **하네스 Bootstrap 전제(형태 A, D-v1.2-1).** 이 하네스는 현재 Bootstrap 상태다(Glossary J-13, 자매 바인딩 §0). 본 문서의 바인딩은 **실행 코드 0**이다 — Entry Resolution 엔진(고정 5단계)은 실행 스크립트가 아니라 **규약 절차**로 실현되며 주 세션이 실수행한다(D-v1.2-1). 따라서 매핑은 (i) 물리 실재 표면(신규 명령 파일 2개), (ii) 규약으로 확정된 정본 문면(형태 A — 판정 수단·직렬화 형식·전달 방식), (iii) 실행 코드 도입 시 로딩될 지점(형태 B — 관측 로더·직렬화기)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **경계 분담(DP-X8).** Discovery Request의 **직렬화 형식·전달 방식**은 본 문서(§5)가 소유·확정한다. 그 물리 기록이 놓일 **백엔드 트리(`discovery-data/` 하위 구조)**는 후속 **discovery-binding.md(예정) 소관**이며 본 문서는 포인터로만 위임한다(자매 contract-binding.md의 DP-X6 분담과 동형 패턴). 미완성 후속 산출물의 내부 구조를 추측·선취하지 않는다(07 R2).
- **실측 기반 상태 서술(L-07).** "실재/미존재" 주장은 파일 시스템 확인 후에만 기입한다. 본 문서가 물리 위임하는 `discovery-data/` 트리는 **현 시점 미존재**이며(생성 금지 — E2E Task 소관), 본 문서는 명령 파일 2개만 물리 생성한다. §10이 그 실측 대조 표다.
- **네임스페이스·용어.** 본 문서가 확정하는 것은 물리 표기(명령 파일 형태·판정 수단·직렬화 형식·전달 방식)뿐이며, 01이 소유하는 스키마 용어(`name`·`trigger`·`requiredEvidence`·`decisionRows`·`modeMapping`·`sourceType`·`capability`·`valueDomain` 등)는 01 정의를 § 포인터로 참조하고 재정의하지 않는다. 새 UAHF 용어·새 계약 요소(Descriptor 필드·연산·불변·kind)를 신설하지 않는다.

---

## §1. 목적

이 문서는 entry/specs/01 "### §4.1 바인딩 대상"의 **3불릿**을 이 환경 위에 **v1.2 시점의 구체 물리 실현**으로 매핑한다. Entry Resolution의 산출인 Discovery Request는 하류 Project Discovery의 선행 확정 인터페이스(ARCHITECTURE.md §12.2)이므로, 이 문서가 확정하는 물리 인터페이스는 v1.2 E2E·후속 작업의 물리 실현 기반이다.

책임은 셋이다.

- 01 §4.1 바인딩 표 **3불릿 전부**(E1 진입 트리거 물리 형태 · E2 Workspace Evidence 관측 물리 실현 · E3 Discovery Request 직렬화)를 물리 실현으로 확정한다(§2 — 실재/규약 실현/형태 B 3구분).
- **E1**: 논리 Entry `/new`·`/continue`의 물리 발화 형태를 진입 명령 문서로 확정한다(§3). **E2**: contract-presence·repository-presence의 존재 판정 수단(탐지 절차)을 확정한다(§4 — contract-binding §4.1 위임 해소·비git 저장소 실측 해소). **E3**: Discovery Request {mode, inputs, policy}의 직렬화 형식·전달 방식을 확정하고, 기록 백엔드 트리는 후속 바인딩에 위임한다(§5, DP-X8).
- 결정 테이블 실동작(행 1·행 6)을 예시하고(§6), EN-INV 준수를 자기 점검하며(§7), 01 §4.2 이식 교체 지점에 대응을 명시하고(§8), 상태 서술을 실측과 대조한다(§10).

이 문서는 01 §3·§4·UAHF 정본의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A → 형태 B 전환 시에도 01 §3 계약 변경은 0이며(structure.md §7 C-1 동형), §8의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 01 §4.1 바인딩 표 3불릿 물리 실현 (done 2)

01 "### §4.1 바인딩 대상"의 **3불릿 전부**를 물리 표면으로 매핑한다. "01 §4.1 바인딩 지점" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 형태·수단·형식을, "실재 여부" 열이 Bootstrap 상태에서의 **물리 실재 / 규약 실현(형태 A) / 형태 B**를 정직하게 구분한다(§10 실측 대조).

| # | 01 §3 계약 요소 (정본 §) | 01 §4.1 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| E1 | 진입 트리거 (Entry Descriptor `trigger` — §3.1·§3.2-A) | "진입 트리거의 물리 형태 … 그 물리 발화 형태(어떤 진입 명령·선택·추론으로 Entry가 발화되는가)는 Adapter가 바인딩한다. Core Contract는 논리 name·trigger만 소유한다." | 논리 Entry `/new`·`/continue`(01 §3.1·§0 논리 식별자)의 물리 발화 형태 = `.claude/commands/uaf-new.md`·`uaf-continue.md` **문서 명령**. 상세 §3. | **물리 실재**: 두 명령 파일 신규 생성(형태 A 문서 명령). **규약 실현(형태 A)**: Entry Resolution 엔진 고정 5단계 = 규약 절차(주 세션 실수행). **형태 B**: 진입 발화→해소 실행 로더 — 미도입. |
| E2 | Workspace Evidence 관측 (Evidence Source capability·유/무 값 도메인 — §3.2-C) | "Workspace Evidence 관측의 물리 실현 … contract-presence·repository-presence를 실제 환경에서 어떻게 탐지하는가(경로 관례·직렬화 형식·존재 판정 수단)는 Adapter 소관이다. Core Contract는 capability 선언과 유/무 값 도메인만 소유한다." | contract-presence = contract-binding §4 확정 저장 위치의 인스턴스 파일(`project-contract.v<N>.md`) 유무 실측(존재 판정 수단 = 본 문서 확정, §4.1). repository-presence = 워크스페이스 내 기존 프로젝트 콘텐츠 유무 실측(§4.2). Entry는 유/무만 관측(01 EN-INV 2). 상세 §4. | **규약 실현(형태 A)**: 판정 수단(탐지 절차) = 정본 문면 확정. **규약 실현(형태 A)**: 실제 관측 = 규약 절차(주 세션). **형태 B**: 탐지 로더 — 미도입. Contract 인스턴스 데이터·`discovery-data/` = 미존재(E2E Task 소관). |
| E3 | Discovery Request 산출 (§3.2-B 매핑·§3.2-E mode 네임스페이스) | "Discovery Request 직렬화. {mode, inputs, policy}의 물리 직렬화·전달 방식은 Adapter 소관이다." | {mode, inputs, policy} = 자기서술 **구조화 레코드**로 직렬화(§5.1)·전달(§5.2). ARCHITECTURE §12.2·01 §3.2-B 추상 정합·재정의 0. 기록 백엔드 트리(`discovery-data/` 하위)는 discovery-binding.md(예정) 위임(DP-X8). 상세 §5. | **규약 실현(형태 A)**: 직렬화 형식·전달 방식 = 정본 문면 확정. **형태 B**: 직렬화기/로더 — 미도입. 기록 데이터·백엔드 트리 = 미존재(후속 바인딩·E2E Task 소관). |

주:

- 위 3행은 01 "### §4.1 바인딩 대상" 표의 전 불릿(3건)이다. 각 행의 "물리 실현"은 01 §4.1 정본 표현을 이 환경의 구체 형태·수단·형식으로 좁힌 것이며, **새 바인딩 계약을 창설하지 않는다**(§0). 특정 AI·모델·제품 기능·방법론은 여기서도 명명하지 않는다(01 §4 말미 동형) — 격리 대상은 명령 파일 형태·판정 수단·직렬화 형식뿐이다.
- 01 §4.1 표에 없는 계약 요소(§3.2-A Descriptor 모델·엔진 5단계·§3.2-B 매핑·§3.2-C Evidence 선언 스키마·§3.2-D 결정 테이블·§3.2-E mode 네임스페이스·§3.3 EN-INV)는 **이식 시에도 유지되는 것**이며, 본 문서가 바인딩하지 않는다(§8 "유지되는 것" 열). 이들의 진위 판정 기준은 01 §3이다.

---

## §3. E1 — 진입 트리거 물리 형태 확정 (done 3)

01 §4.1 불릿 1("진입 트리거의 물리 형태 … 물리 발화 형태는 Adapter가 바인딩한다")의 물리 실현을 확정한다. 계약(01 §3.1 Entry 2종·§3.2-A Descriptor `trigger` 논리 서술)은 재정의하지 않고 § 포인터로 인용하며, 물리 발화 형태만 확정한다.

### §3.1 확정 — 두 진입 명령 문서

논리 Entry의 물리 발화 형태를 다음 두 문서 명령으로 확정한다.

| 논리 Entry (01 §3.1 name) | 물리 발화 형태 (이 환경 확정) | 성격 |
|---|---|---|
| `/new` (순수 Greenfield 전용) | `.claude/commands/uaf-new.md` | 형태 A 문서 명령 — Entry Resolution 규약 절차를 정본 포인터로 안내. |
| `/continue` (Incremental/Brownfield) | `.claude/commands/uaf-continue.md` | 형태 A 문서 명령 — Entry Resolution 규약 절차를 정본 포인터로 안내. |

- **논리 식별자 주의(01 §0).** `/new`·`/continue`는 Entry의 **논리 식별자(name)**이며, 물리 진입 형태(어떤 진입 명령·선택·추론으로 발화되는가)는 Adapter 소관이다(01 §0·§4.1). 이 환경의 물리 발화 형태가 위 `uaf-` 접두 명령임을 본 문서가 확정한다. `uaf-` 접두 = UAF 네임스페이스 표면화 + 환경 빌트인 명령과의 충돌 회피(DP-X1).

### §3.2 골격 준거·확정 근거

- **골격 준거.** 두 명령은 `.claude/commands/uahf-status.md` 선례와 동형이다 — (i) YAML front-matter(`description:`), (ii) 형태 A(실행 코드 0), (iii) **정본 포인터 전용**(값 하드코딩 0 — 정본이 진행돼도 명령이 낡지 않음). `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰이 허용된다(structure.md §2 Adapter 경계, uahf-status.md §0).
- **재정의 0.** 두 명령은 01·본 entry-binding 정본을 **재정의하지 않는다** — 안내 포인터만 담는다. 각 명령은 Entry Resolution **규약 절차**(엔진 고정 5단계·결정 테이블 대조)와 **사용자 개입 지점**(Preserve Human Authority 게이트)을 정본 § 포인터로 안내한다: `uaf-new.md`는 `/new` 결정 행(01 §3.2-D 행 1~4)·D3 ①을, `uaf-continue.md`는 `/continue` 결정 행(행 5~8)·D3 ②·③을 가리킨다.
- **엔진 실현 = 규약 절차(형태 A).** 명령은 실행 코드를 담지 않으므로, Entry Resolution 엔진 고정 5단계(01 §3.2-A)는 호출 시 **주 세션이 규약 절차로 실수행**한다(D-v1.2-1). 실행 로더는 형태 B로 미도입이다(§10).

---

## §4. E2 — Workspace Evidence 관측 물리 실현 (done 4)

01 §4.1 불릿 2("contract-presence·repository-presence를 실제 환경에서 어떻게 탐지하는가 — 경로 관례·직렬화 형식·존재 판정 수단 — 는 Adapter 소관")의 물리 실현을 확정한다. **capability 선언과 유/무 값 도메인은 01 §3.2-C가 소유**하며(재정의 0), 본 문서는 그 **존재 판정 수단(탐지 절차)**만 확정한다. Entry는 유/무만 관측하고 증거를 수집·해석하는 Discovery를 수행하지 않는다(01 §3.2-A 2단계 "관측만"·EN-INV 1·2).

### §4.1 contract-presence — 존재 판정 수단 (contract-binding §4.1 위임 해소)

- **capability(정본 소유).** "워크스페이스에 Project Contract가 존재하는가"를 관측한다. 값 도메인 = 유/무 (01 §3.2-C).
- **저장 위치(선행 확정 — contract-binding §4).** Contract 인스턴스는 `project-contract.v<N>.md` 파일로 직렬화되며(Markdown 본문 + YAML front-matter, contract-binding §3), 저장 위치는 이원화되어 있다 — 일반 관례 = 소비 프로젝트 내 `.claude/project-contract/`, 본 UAHF 저장소 인스턴스 = `framework/adapters/claude/discovery-data/contracts/uahf/`(contract-binding §4).
- **존재 판정 수단(본 문서 확정 — 탐지 절차).** contract-presence의 유/무는 위 저장 위치에 **인스턴스 파일(`project-contract.v<N>.md`)이 하나라도 존재하는지**의 실측으로 판정한다.
  - **유** — 해당 저장 위치(소비 프로젝트: `.claude/project-contract/`; 본 저장소: `framework/adapters/claude/discovery-data/contracts/uahf/`)에 `project-contract.v<N>.md` 인스턴스 파일이 하나 이상 존재한다.
  - **무** — 그러한 인스턴스 파일이 존재하지 않는다(디렉터리 부재 포함).
- **관측 한계(EN-INV 2).** Entry는 파일 **유무만** 관측한다 — front-matter·본문을 파싱·해석·생성하지 않는다. Contract 내용 해석·최신 인스턴스 해소(`instanceVersion`·`supersedes`)는 하류 소비(Advisor Consult·tolerant reader) 소관이며 Entry 관측 밖이다(01 EN-INV 2, contract-binding §3·§4). 이로써 contract-binding §4.1이 "존재 판정 수단(탐지 실행)의 상세는 후속 entry-binding.md 소관"으로 미룬 지점이 해소된다.

### §4.2 repository-presence — 존재 판정 수단 (비git 저장소 실측 해소)

- **capability(정본 소유).** "워크스페이스에 Repository가 존재하는가"를 관측한다. 값 도메인 = 유/무 (01 §3.2-C).
- **판정 수단의 정본 근거.** 01 §3.2-D 판별 규칙 **D3 ②**는 이 Evidence가 실현하는 결과를 "**기존 저장소가 있으나 아직 Contract가 없는 최초 도입**"의 Brownfield Full Discovery로 규정한다(행 6). 즉 이 맥락에서 "Repository 존재"는 **워크스페이스에 이어갈 기존 프로젝트 본체(기존 프로젝트 콘텐츠)가 실재하는가**를 뜻한다(Brownfield의 정의 — ARCHITECTURE.md §2.2 파이프라인·01 §3.1 `/continue` Brownfield). 본 문서는 이 capability를 재정의하지 않고, 그 정본 의미에 정합하는 **물리 판정 수단**을 확정한다(§4.1 불릿 2가 "존재 판정 수단"을 Adapter 소관으로 위임).
- **존재 판정 수단(본 문서 확정 — 탐지 절차).** repository-presence의 유/무는 **워크스페이스에 이어갈 기존 프로젝트 콘텐츠(선재하는 프로젝트 산출물의 비어 있지 않은 본체)가 실재하는지**의 실측으로 판정한다. 다음 지표 중 **하나라도 충족되면 유**다(충분 조건의 논리합):
  1. 워크스페이스에 선재하는 실질 프로젝트 콘텐츠(소스·문서·설정 등 프로젝트 산출물)가 빈/맨 초기화를 넘어 존재한다, 또는
  2. 워크스페이스에 버전 관리 저장소 마커가 존재한다.
  - **VCS 마커는 충분 지표일 뿐 필요 지표가 아니다.** repository-presence를 **VCS 마커 단독으로 정의하지 않는다** — 본 UAHF 저장소는 비git 저장소(`.git` 부재, §10 실측)이면서도 방대한 기존 프로젝트 콘텐츠(`framework/`·`specs/`·`uaf/`·`docs/` 등)를 실재로 보유하므로, VCS 마커 단독 정의는 이 저장소를 "무"로 오판해 결정 테이블 행 6(Brownfield)의 매칭을 깨뜨린다. 지표 1(기존 프로젝트 콘텐츠)이 1차 판정이며, VCS 마커는 그것을 보강하는 충분 지표다.
- **두 E2E 시나리오 실관측(문면 시연).**
  - **신규 빈 프로젝트 디렉터리 → 무.** 선재 프로젝트 콘텐츠 없음 ∧ VCS 마커 없음 → repository-presence = **무**.
  - **본 UAHF 저장소(기존 프로젝트 콘텐츠 실재) → 유.** 루트에 `ARCHITECTURE.md`·`framework/`·`specs/`·`uaf/`·`docs/`·`ROADMAP.md` 등 실질 프로젝트 콘텐츠 실재(지표 1 충족; VCS 마커는 부재해도 무방) → repository-presence = **유**(§10 실측).
- **관측 한계.** Entry는 콘텐츠의 **유무만** 관측하며 그 내용을 수집·해석하지 않는다(01 §3.2-A 2단계·EN-INV 1). 기존 프로젝트 콘텐츠의 실제 이해·분석은 하류 Project Discovery(Brownfield Full Discovery) 소관이다.

### §4.3 관측 결과의 소비

관측된 두 Evidence(contract-presence·repository-presence의 유/무)는 Entry Resolution 엔진 3단계(우선순위 평가, 01 §3.2-A)에서 명시 Entry의 결정 행(§3.2-D)에 대조되며, Discovery Request의 `inputs`(Evidence 참조 목록, §5·01 §3.2-B)에 확정 참조로 담긴다.

---

## §5. E3 — Discovery Request 직렬화·전달 확정 (done 5 · DP-X8)

01 §4.1 불릿 3("{mode, inputs, policy}의 물리 직렬화·전달 방식은 Adapter 소관")의 물리 실현을 확정한다. Discovery Request 추상(ARCHITECTURE.md §12.2 — 3요소)·매핑 채움 규칙(01 §3.2-B)·mode 네임스페이스(01 §3.2-E)는 재정의하지 않고 § 포인터로 인용하며, 물리 직렬화 형식·전달 방식만 확정한다.

### §5.1 확정 — 자기서술 구조화 레코드

**Discovery Request 1건 = {mode, inputs, policy} 3요소를 담는 자기서술 구조화 레코드**로 직렬화한다. 자매 바인딩의 구조화 데이터 관례(memory-binding.md의 자기서술 레코드·contract-binding.md의 YAML front-matter)와 동형이며, 구체 구조화 데이터 형식은 Adapter 선택이다(격리 지점 — 이식 교체 §8).

논리 골격 예시(물리 레코드 형태 — ARCHITECTURE §12.2·01 §3.2-B의 물리 렌더링; 3요소만 표현하며 새 계약 요소를 창설하지 않는다):

```
# Discovery Request (Entry Resolution 산출 — 구조화 레코드)
mode: <네임스페이스 값>            # greenfield / incremental / brownfield / … (확장 네임스페이스, 01 §3.2-E·§12.2)
inputs:                            # Evidence 참조 목록 — 확정 참조만 (01 §3.2-B·§12.2)
  - sourceType: contract-presence
    observed: <유|무>
  - sourceType: repository-presence
    observed: <유|무>
policy: <Discovery Policy 참조>     # Policy as Data. 충돌 조합은 사용자 확인 게이트를 포함하는 정책 번들 참조 (01 §3.2-B·§3.2-D·EN-INV 6)
```

- **§12.2 정합(재정의 0).** `mode` = modeMapping 적용 값(확장 네임스페이스), `inputs` = 관측된 Workspace Evidence의 확정 참조 목록(미완성·동시 작성 산출물 비참조), `policy` = Discovery Policy 참조 — 세 요소가 ARCHITECTURE §12.2·01 §3.2-B와 1:1 정합한다(EN-INV 5). Discovery Request는 Contract 자체를 담지 않고 Discovery 내부 개념(질문·전략)을 담지 않는다(§12.2 경계·01 §2.4 의존 방향).

### §5.2 전달 방식

- **형태 A(Bootstrap).** Discovery Request는 Entry Resolution 규약 절차(주 세션)가 5단계 방출(01 §3.2-A 5단계)에서 위 레코드로 산출하고, 하류 Project Discovery 소비자에게 전달한다. 전달은 요소 간 인터페이스(ARCHITECTURE §2.2 Entry Resolution → Project Discovery)의 구조화 레코드 이관이다.
- **형태 B(향후).** 직렬화기·로더 실행 코드가 도입되면 같은 레코드 형식을 방출·소비한다. 형태 B 도입 시에도 §12.2·01 §3.2-B 계약 변경은 0이다(structure.md §7 C-1 동형).

### §5.3 경계 분담(DP-X8) — 백엔드 트리 위임

- **본 문서 소유.** Discovery Request의 **직렬화 형식(§5.1)·전달 방식(§5.2)**은 본 문서가 확정한다.
- **후속 위임.** 그 물리 기록이 놓일 **백엔드 트리(`framework/adapters/claude/discovery-data/` 하위의 Discovery Request 기록 구조)**는 **discovery-binding.md(예정) 소관**이며, 본 문서는 포인터로만 위임한다(DP-X8). 이는 자매 contract-binding.md가 Provenance 내부 형식을 discovery-binding.md에 위임한 DP-X6 분담과 동형 패턴이다. 본 문서가 백엔드 트리 구조를 창설하면 후속 바인딩 소관을 침범하므로, 직렬화 형식·전달 방식 확정에서 멈춘다(07 R2 — 미완성 후속 산출물 추측 금지). `discovery-data/`는 현 시점 미존재이며 생성하지 않는다(§10).

---

## §6. 결정 테이블 실동작 예시 (done 6 — 행 1·행 6)

01 §3.2-D 결정 테이블을 **재정의하지 않고 행을 인용**하여, 물리 관측(§4) → 단일 Discovery Request 산출(§5)의 규약 절차를 두 행에 대해 예시한다. 각 조합이 정확히 한 결과로 해소됨(결정성 불변, EN-INV 3)을 보인다.

### 예 A — 결정 테이블 행 1 (contract 무 · repo 무 → greenfield)

**시나리오.** 신규 빈 프로젝트 디렉터리. 명시 Entry = `/new`(물리 발화: `uaf-new` 명령, §3).

**해소 (Resolution 엔진 5단계, 01 §3.2-A — 물리 관측).**

1. 매칭 — `/new` Descriptor를 Registry에서 찾는다.
2. 증거 수집(관측) — contract-presence: `.claude/project-contract/`에 `project-contract.v<N>.md` 없음 → **무**(§4.1); repository-presence: 선재 프로젝트 콘텐츠 없음 ∧ VCS 마커 없음 → **무**(§4.2).
3. 우선순위 평가 — 관측 {무, 무}을 `/new` 결정 행에 대조 → **01 §3.2-D 행 1** 매칭.
4. 결정성 검증 — 이 조합은 단일 행(1)에만 매칭.
5. 방출 — 단일 Discovery Request `{ mode: greenfield, inputs: [contract-presence(무), repository-presence(무)], policy: 기본 정책 참조 }`(§5.1 레코드).

**결과.** Greenfield 정상 경로(01 §3.2-D 행 1, 근거 P-C). Entry는 여기서 멈춘다 — Discovery 수행·Contract 생성은 하지 않는다(EN-INV 1·2).

### 예 B — 결정 테이블 행 6 (contract 무 · repo 유 → brownfield, D3 ②)

**시나리오.** 기존 프로젝트 콘텐츠가 실재하나 아직 Contract가 없는 워크스페이스(본 UAHF 저장소 dogfooding 포함). 명시 Entry = `/continue`(물리 발화: `uaf-continue` 명령, §3).

**해소 (Resolution 엔진 5단계, 01 §3.2-A — 물리 관측).**

1. 매칭 — `/continue` Descriptor를 Registry에서 찾는다.
2. 증거 수집(관측) — contract-presence: 두 저장 위치(`.claude/project-contract/` 및 `framework/adapters/claude/discovery-data/contracts/uahf/`)에 인스턴스 파일 없음 → **무**(§4.1); repository-presence: 워크스페이스에 실질 프로젝트 콘텐츠 실재(`framework/`·`specs/`·`uaf/`·`docs/` 등, §10 실측) → **유**(§4.2 — VCS 마커 부재와 무관, 지표 1 충족).
3. 우선순위 평가 — 관측 {무, 유}을 `/continue` 결정 행에 대조 → **01 §3.2-D 행 6** 매칭.
4. 결정성 검증 — 이 조합은 단일 행(6)에만 매칭.
5. 방출 — 단일 Discovery Request `{ mode: brownfield, inputs: [contract-presence(무), repository-presence(유)], policy: 기본 정책 참조 }`(§5.1 레코드).

**결과.** Brownfield Full Discovery, 최초 Project Contract 생성 요청(01 §3.2-D 행 6, 판별 규칙 **D3 ②**). Entry는 여기서 멈춘다 — 최초 Contract 생성은 하류 Project Discovery 소관이다(EN-INV 1·2). **이 예가 §4.2 판정 수단의 필요성을 실증한다** — repository-presence를 VCS 마커 단독으로 정의했다면 비git 저장소인 본 저장소가 "무"로 오판되어 행 5(P-D 충돌)로 잘못 해소되었을 것이나, 기존 프로젝트 콘텐츠 판정으로 "유"가 관측되어 행 6(Brownfield)로 결정적으로 해소된다.

---

## §7. EN-INV 자기 점검 (done 7)

본 물리 바인딩이 01 §3.3 EN-INV를 훼손하지 않음을 자가 점검한다. 자체 점검은 최종 승인이 아니다 — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다(02 §3.2-A).

- **EN-INV 1 — Entry Resolution만.** 본 문서는 진입 트리거(§3)·Evidence 관측(§4)·Discovery Request 직렬화(§5)의 **물리 실현만** 바인딩한다. Discovery 수행·Contract 생성의 물리 절차를 도입하지 않으며, 두 명령(§3)도 Discovery Request 산출까지만 안내한다. Entry 산출 = Discovery Request 하나(01 EN-INV 1). **준수 — 위반 서술 0.**
- **EN-INV 2 — Contract 직접 생성·해석 금지.** §4.1의 contract-presence 판정 수단은 인스턴스 파일 **유무만** 실측하며 front-matter·본문을 파싱·해석·생성하지 않는다. §4.2의 repository-presence도 콘텐츠 유무만 관측한다. Entry는 Contract를 Evidence(유/무)로만 관측한다(01 EN-INV 2). **준수 — 위반 서술 0.**
- **EN-INV 3 — 결정성.** §6 두 예시(행 1·행 6)에서 각 관측 조합이 01 §3.2-D 결정 테이블의 **단일 행**으로 해소됨을 보였다. 본 문서는 결정 테이블(8조합)을 재정의하지 않고 **행 인용만** 한다(01 §3.2-A 4단계·EN-INV 3). **준수 — 위반 서술 0.**
- **EN-INV 5 — Discovery Request 정합·재정의 0.** §5.1 레코드의 3요소({mode, inputs, policy})는 ARCHITECTURE §12.2·01 §3.2-B 추상에 1:1 정합하며 — `mode` = 확장 네임스페이스(01 §3.2-E), `inputs` = Evidence 참조 목록, `policy` = 참조 — 추상을 재정의·확장하지 않는다(01 EN-INV 5). **준수 — 위반 서술 0.**

(EN-INV 4 — Layer·엔진 불변 확장 — 는 신규 Entry·Evidence Source·mode 추가의 확장성 계약이며, 본 문서는 기존 2 Entry의 물리 실현만 다루므로 별도 확장 서술을 두지 않는다. EN-INV 6 — 확정 게이트 보존 — 은 두 명령(§3)이 사용자 확인 게이트를 정본 포인터로 안내함으로써 준수된다.)

---

## §8. 01 §4.2 이식 교체 지점 대응 (done 8)

01 "### §4.2 이식 교체 지점"의 3개 교체 지점 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 01 §3 Core Contract 불변(structure.md §7 C-1 동형)을 재확인한다.

| 01 §4.2 교체 지점 (바뀌는 것) | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (01 §3 불변) |
|---|---|---|---|
| 진입 트리거의 물리 형태 | §2 E1, §3 | `.claude/commands/uaf-new.md`·`uaf-continue.md` 문서 명령. | 01 §3.2-A Entry Descriptor 등록 모델(논리 name·`trigger` 논리 서술)·Resolution 엔진 고정 5단계, §3.1 Entry 논리 name `/new`·`/continue`. |
| Evidence 관측의 물리 수단 | §2 E2, §4 | contract-presence = 저장 위치 인스턴스 파일(`project-contract.v<N>.md`) 유무 실측·repository-presence = 기존 프로젝트 콘텐츠 유무 실측. | 01 §3.2-C Evidence Source 선언 스키마(sourceType·capability·valueDomain)·유/무 값 도메인·v1.1 Evidence 2종 capability. |
| Discovery Request의 직렬화 | §2 E3, §5 | {mode, inputs, policy} 자기서술 구조화 레코드 직렬화·전달. | 01 §3.2-B Discovery Request 매핑·§3.2-E mode 네임스페이스, ARCHITECTURE §12.2 Discovery Request 추상(mode 확장 네임스페이스·inputs Evidence 참조 목록·policy 참조). |

- "유지되는 것" 열의 계약은 다른 AI·실행 환경으로 이식해도 바뀌지 않는다 — 01 §3 Core Contract의 이식 불변성이며, 01 §4.2 "바뀌지 않는 것"(Entry Descriptor 등록 모델·Resolution 엔진의 고정 알고리즘·결정 테이블 데이터·Evidence Source 선언 스키마·Discovery Request 추상 정합)과 정합한다. structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 동형이다.
- 본 문서는 01 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고, v1.2 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §10. 상태 서술 실측 대조 (L-07 — 미존재를 실재로 쓰지 않음)

본 문서의 "실재/미존재" 서술을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-07 작성 시 `ls`/`test`/`git rev-parse` 직접 실측.** 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다.

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-07, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/entry-binding.md` | 실재 (본 문서) | 실재 (이 파일 — 신규 생성). |
| `.claude/commands/uaf-new.md` | 실재 (신규 진입 명령) | 실재 — 신규 생성. |
| `.claude/commands/uaf-continue.md` | 실재 (신규 진입 명령) | 실재 — 신규 생성. |
| `.claude/commands/uahf-status.md` (명령 골격 선례) | 실재 (자매 명령) | 실재 — 확인(무수정). |
| `framework/adapters/claude/contract-binding.md` (선행 확정 인터페이스, T-C) | 실재 (§3·§4 소비 대상) | 실재 — §3·§4·§4.1 확인(무수정, § 포인터·위임 해소 대상). |
| `entry/specs/01-entry.md` (바인딩 대상 정본) | 실재 (v1.1 Baseline) | 실재 — §3·§4 확인(무수정, § 포인터 대상). |
| `framework/adapters/claude/discovery-data/` (Discovery Request 기록 백엔드 루트) | **미존재 — discovery-binding.md(예정)·E2E Task 소관, 생성 금지** | **미존재** — 디렉터리 부재 확인. 생성하지 않음(백엔드 트리 위임, §5.3). |
| `.claude/project-contract/` (일반 관례 Contract 저장 위치) | 본 저장소 **미존재**(정상 — 일반 관례는 소비 프로젝트 배치 대상) | **미존재** — 본 저장소에 해당 경로 없음(정상). |
| 본 UAHF 저장소 VCS 마커(`.git`) | **부재**(비git 저장소) — repository-presence는 VCS 마커 비의존(§4.2) | **부재** — `.git` 없음·`git rev-parse` 실패 확인. |
| 워크스페이스 기존 프로젝트 콘텐츠 (repository-presence 유 근거) | 실재 (`framework/`·`specs/`·`uaf/`·`docs/` 등) | 실재 — 루트에 `ARCHITECTURE.md`·`framework`·`specs`·`uaf`·`docs`·`ROADMAP.md`·`README.md` 등 실측 → 본 저장소 repository-presence = **유**(§4.2·§6 예 B). |
| Entry Resolution 실행 로더·직렬화기 (형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). |

- **핵심 구분.** 본 문서가 확정한 진입 명령 형태·Evidence 판정 수단·Discovery Request 직렬화 형식·전달 방식은 **정본 문면(형태 A)**이며, 물리 생성물은 **명령 파일 2개**뿐이다. `discovery-data/` 백엔드 트리·Contract 인스턴스 데이터는 **현 시점 미존재**로, discovery-binding.md(예정)·v1.2 E2E Task 소관이다(§5.3). 본 문서는 백엔드 트리·물리 데이터를 생성하지 않는다.
- 실측과 불일치하는 서술은 0건이다 — 미존재(`discovery-data/`·`.claude/project-contract/`·`.git`)를 실재로, 실재(명령 파일·contract-binding·01 정본·기존 프로젝트 콘텐츠)를 미존재로 쓰지 않았다.

**재베이스라인 — 2026-07-09 재측정 (v1.2.1 리팩토링 후):** 위 2026-07-07 표·불릿은 작성 시점 스냅샷으로 상단에 역사 보존한다(byte 불변). 아래는 v1.2.1 Layer 중심 재구성(루트 `uaf/` 소멸·최상위 = `entry/`·`discovery/`·`planning/`·`knowledge/`·`uahf/`·`docs/`·`.claude/`·`ARCHITECTURE.md`) 이후 현시점 직접 실측 결과다(2026-07-09, HEAD `963076d` — `ls`/`test`/`git rev-parse`). 그간 상태가 바뀐 행(repository-presence 근거·`discovery-data/`·`.git`)만 재측정하며, 나머지 행의 계약·판정 논리는 불변이다.

| 대상 (현행 경로) | 2026-07-07 서술 | 재측정 결과 (2026-07-09, 직접 실측) |
|---|---|---|
| `uahf/framework/adapters/claude/discovery-data/` (Discovery Request 기록 백엔드 루트) | **미존재** (백엔드 트리 위임, §5.3) | **실재** — 디렉터리 확인. 하위 `contracts/uahf/project-contract.v1.md`·`policy/default-policy.yaml`·`events/{brownfield-r001,greenfield-r002}/events.jsonl`·`e2e-greenfield-project/.claude/project-contract/project-contract.v1.md` 실측(후속 discovery-binding·E2E Task 산출로 생성됨). 2026-07-07 미존재 → 현 실재로 전환. |
| 본 UAHF 저장소 VCS 마커(`.git`) | **부재** (비git 저장소) | **실재** — `.git` 디렉터리 존재·`git rev-parse --show-toplevel` 성공·HEAD `963076d` 확인. 2026-07-07 부재 → 현 git 저장소로 전환. **repository-presence 판정은 VCS 마커 비의존(§4.2)** 이므로 계약 무영향이며, 마커 실재는 충분 지표를 추가로 충족할 뿐이다. |
| 워크스페이스 기존 프로젝트 콘텐츠 (repository-presence 유 근거) | 실재 (`framework/`·`specs/`·`uaf/`·`docs/` 등) | **실재(유 불변)** — 루트 최상위 = `ARCHITECTURE.md`·`entry`·`discovery`·`planning`·`knowledge`·`uahf`·`docs`·`design`·`research`·`templates`·`tests`·`README.md`·`ROADMAP.md` 실측. **루트 `uaf/`·(루트)`specs/`·(루트)`framework/`는 부재**(v1.2.1에서 Layer 디렉터리로 분산·`framework/`·`specs/`는 `uahf/` 하위로 이동). repository-presence = **유**는 불변(§4.2·§6 예 B)이며 근거 경로 표기만 v1.2.1 구조로 갱신. |

- **판정 계약 불변.** 위 상태 전환(백엔드 트리·`.git` 실재화·루트 경로 재편)은 §4.2 repository-presence 판정 수단·EN-INV·결정 테이블을 바꾸지 않는다 — 관측 대상의 물리 상태·위치만 이동했다. 미존재를 실재로 쓰지 않는다는 L-07 규율은 재측정에도 동일 적용했다(전 행 `ls`/`test`/`git rev-parse` 직접 실측 후 기입).

---

## §11. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 entry/specs/01 §3·§4의 물리 실현이다. 어떤 Entry Descriptor 필드·Resolution 엔진 단계·결정 테이블 행·Evidence Source 선언·mode 네임스페이스·불변(EN-INV 1~6)도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 01 §3이다. 새 계약 요소(필드·연산·불변·kind)를 창설하지 않았다.
- **본 문서가 소유·확정하는 것.** 01 §4.1이 "Adapter 소관"으로 미룬 3불릿 — ① E1 진입 트리거 물리 형태(§3, 두 진입 명령) ② E2 Evidence 관측 판정 수단(§4 — contract-presence 탐지 절차·repository-presence 판정 수단) ③ E3 Discovery Request 직렬화·전달(§5) — 만 확정한다. Discovery Request 기록 백엔드 트리(`discovery-data/` 하위)는 discovery-binding.md(예정)에 포인터로 위임한다(DP-X8·추측 금지). 이로써 contract-binding §4.1이 미룬 **contract-presence 존재 판정 수단(탐지 실행)**이 본 문서 §4.1에서 해소된다.
- **격리 토큰의 단일 자리.** 구체 명령 이름(`uaf-new`·`uaf-continue`)·물리 경로(`.claude/commands/…`·`framework/adapters/claude/…`)·구조화 데이터 형식·파일 확장자는 이 Adapter 경계 문서에 둔다. UAF 정본(entry/specs/01)은 이 토큰을 "Adapter 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3는 이 경계에 비적용 — 격리 보유).
- **동시 작성 문서 경계(07 R2·R4).** 본 산출은 신규 3파일(entry-binding.md·uaf-new.md·uaf-continue.md)만 생성하며, 미완성 후속 산출물(discovery-binding.md·E2E 데이터·`discovery-data/` 트리)을 인용·추측하지 않았다 — 포인터 위임만 했다(07 R2). 확정된 인터페이스 계약(entry/specs/01 §3·§4·contract-binding §3·§4·ARCHITECTURE §12.2)만 참조했다. UAF 정본·UAHF 정본·기존 바인딩(contract-binding.md 포함)·물리 데이터를 수정·생성하지 않았다(07 R4·INV-2). 불확실 지점은 아래 open_questions로 에스컬레이션했다(추측 금지).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-TE-1 (repository-presence 콘텐츠 임계값 — 비차단).** §4.2는 repository-presence를 "기존 프로젝트 콘텐츠(비어 있지 않은 프로젝트 본체)의 유무"로 판정한다(정본 근거: D3 ② Brownfield 의미·01 §3.2-C capability). 위임된 두 E2E 시나리오(완전 빈 디렉터리 = 무, 실질 콘텐츠 실재 = 유)는 이 판정 수단으로 명확히 해소된다. 다만 극단적 엣지 케이스(예: 단일 README·숨김 설정만 있는 워크스페이스)에서 "빈/맨 초기화 vs 실질 콘텐츠"의 정밀 임계값은 Adapter 재량 여지가 있으며, 필요 시 Advisor가 재확정할 수 있다. 01 §3.2-C capability·유/무 값 도메인 변경은 아니므로 **비차단**이다.
- **OQ-TE-2 (Discovery Request 기록 백엔드 트리 — 후속 위임, 비차단).** Discovery Request의 물리 기록이 놓일 백엔드 트리(`discovery-data/` 하위 구조)는 §5.3에서 discovery-binding.md(예정)에 위임했다(DP-X8·추측 금지). 후속 바인딩 착수 시 이 지점의 물리 확정이 필요하다(자매 contract-binding.md OQ-TC-2의 discovery-binding 위임과 정합). ARCHITECTURE §12.2·01 §3.2-B 계약 변경은 아니므로 **비차단**이다.

---

## §12. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 **UAF 정본(entry/specs/01-entry) 바인딩** 산출물(DP-X1). 정본 = 01 §3·§4(본 문서는 물리 실현, 재정의 아님 — §0). 자매 contract-binding.md와 같은 UAF 레벨 바인딩·접두 없는 동형 파일명.
- **§2:** 01 "### §4.1 바인딩 대상" **3불릿 전건**(E1·E2·E3)을 물리 실현으로 매핑(실재/규약 실현(형태 A)/형태 B 3구분).
- **§3 (E1):** 논리 Entry `/new`·`/continue`(01 §3.1·§0 논리 식별자)의 물리 발화 형태 = `.claude/commands/uaf-new.md`·`uaf-continue.md` 문서 명령. uahf-status.md 선례 동형(YAML front-matter·형태 A·정본 포인터 전용)·재정의 0·Entry Resolution 규약 절차와 사용자 개입 지점을 정본 § 포인터로 안내.
- **§4 (E2):** contract-presence = contract-binding §4 저장 위치의 인스턴스 파일(`project-contract.v<N>.md`) 유무 실측(존재 판정 수단 확정 — contract-binding §4.1 위임 해소). repository-presence = 기존 프로젝트 콘텐츠 유무 실측(VCS 마커는 충분 지표일 뿐 필요 지표 아님 — 비git 저장소 실측 해소, D3 ② Brownfield 의미 정합). Entry는 유/무만 관측(EN-INV 2). 두 E2E 시나리오 실관측 문면 시연.
- **§5 (E3):** Discovery Request = {mode, inputs, policy} 자기서술 구조화 레코드 직렬화(§5.1)·전달(§5.2). §12.2·01 §3.2-B 추상 정합·재정의 0. 기록 백엔드 트리(`discovery-data/` 하위)는 discovery-binding.md(예정) 위임(§5.3, DP-X8).
- **§6:** 결정 테이블 행 1(greenfield)·행 6(brownfield, D3 ②) 물리 관측 → 단일 Discovery Request 산출 예시(01 §3.2-D 재정의 0·행 인용만·EN-INV 3 결정성). 행 6 예가 §4.2 판정 수단(비git 저장소 유 관측)의 필요성을 실증.
- **§7:** EN-INV 1·2·3·5 자기 점검(준수·위반 서술 0). 자체 점검은 최종 승인 아님(Verifier CP2·Advisor CP3 뒤따름).
- **§8:** 01 "### §4.2" 이식 교체 지점 3건 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 01 §3 불변(C-1 동형) 재확인.
- **§10:** 실측 대조 — 신규 3파일·uahf-status.md·contract-binding.md 실재, `discovery-data/`·`.claude/project-contract/`·`.git` 미존재/부재, 기존 프로젝트 콘텐츠 실재. 미존재를 실재로 쓰지 않음(L-07).
- 01 §3·§4·UAHF 정본 재정의 0, Glossary 용어 신설 0, 새 계약 요소 창설 0, 실행 코드 0(형태 A). 구체 명령 이름·물리 경로·직렬화 형식 토큰은 이 Adapter 경계에서 허용된다(격리 지점).
