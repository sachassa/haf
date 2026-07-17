# entry/adapters/claude/entry-binding — Claude Code Entry Layer Adapter 바인딩

작성일: 2026-07-07
상태: Baseline · 2026-07-18 관측 수단 개정(Evidence 관측 = 사용자 폴더 주입 하이브리드) — CP2 통과(충족 9/위반 0/판정불가 1: OQ-2)·CP3 승인(OQ-2 = (a) Adapter 물리 addressing·spec 무변경 확정) · 2026-07-18 형태 B 도입(`entry_resolve.py` 결정적 실행 로더·`entry-registry.json` 결정 테이블 데이터 — E1/E2/E3 예약 슬롯 실현·형태 A 공존·01 §3 계약 변경 0·structure.md §7 C-1) · 2026-07-18 CP2 정정(게이트 = canonical 결정 테이블 policy 단일 소스 — 병행 imperative conflict 판정 제거·행 7 거짓 게이트 정정; `--entry new|continue` 정규화·OQ-7) · CP2 재판정 통과·CP3 승인(2026-07-18 — 게이트 행 {2,3,4,5}=01 §3.2-D 1:1·mode/policy 8/8·entry 22 pass·baseline 236 회귀 0·01 무접촉)
상위 규약: AGENT.md
근거 정본:

- entry/specs/01-entry.md §3.1(Interface — Entry & Entry Resolution 연산·Entry 2종 `/new`·`/continue`)·§3.2-A(Entry Descriptor 등록 모델 5필드·Resolution 엔진 고정 5단계)·§3.2-B(Discovery Request 매핑 — §12.2 정합 채움 규칙)·§3.2-C(Workspace Evidence & Evidence Source 확장 스키마 — contract-presence·repository-presence capability 선언·유/무 값 도메인)·§3.2-D(결정 테이블 전 8조합·판별 규칙 D3 ①②③)·§3.2-E(mode 네임스페이스)·§3.3(EN-INV 1~6)·§4.1(### §4.1 바인딩 대상, 불릿 3건)·§4.2(### §4.2 이식 교체 지점)·§8(Examples — 예1 결정 테이블 적용·예3 `/import` 등록). 본 문서가 물리 실현으로 바인딩하는 계약의 정본. **재정의·확장하지 않고 § 포인터로만 인용한다.**
- ARCHITECTURE.md §12.2(Discovery Request 인터페이스 추상 — 3요소 {mode, inputs, policy}). Entry Resolution 산출이 정합해야 하는 상위 데이터 계약 추상. 재정의 0.
- planning/adapters/claude/contract-binding.md §3(Contract 직렬화 = Markdown 본문 + YAML front-matter 단일 문서)·§4(저장 위치 이원화 — 일반 관례 `.claude/project-contract/`·본 저장소 인스턴스 `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`·파일명 `project-contract.v<N>.md`)·§4.1(**"존재 판정 수단(탐지 실행)의 상세는 entry-binding.md 소관"으로 명시 위임**). 선행 확정 인터페이스 — 본 문서 §4가 그 위임을 해소한다.
- uahf/framework/adapters/claude/memory-binding.md — 자매 Adapter Binding 골격 선례. 제목 라인 → 작성일·상태·상위 규약·근거 정본 → §0 정본 경계 → §1 목적 → 바인딩 표 물리 실현(실재/규약 실현/형태 B 3구분) → 물리 절차/매핑 절 → 이식 교체 지점 표("유지되는 것" 열 = C-1 재확인) → 실측 대조 절(L-07) → self-note·open_questions → 요약의 관례.
- .claude/commands/uahf-status.md — Presentation/진입 명령 골격 선례(형태 A·YAML front-matter `description:`·정본 포인터 전용·값 하드코딩 0). 본 문서가 확정하는 두 진입 명령(uaf-new·uaf-continue)의 골격 준거.
- uahf/framework/core/structure.md §2(4경계 배치 — `framework/adapters/<adapter>/` = 환경 의존 격리 경계, `.claude/` 진입 표면은 Adapter 성격)·§5(금지 토큰 규칙 C-3 — Adapter 경계는 격리 보유로 비적용). 본 문서 경계·격리 토큰 허용의 근거.
- uahf/specs/00-glossary.md — UAHF 용어 정본. 본 문서는 새 용어를 신설하지 않는다. `형태 A/B`는 structure.md §4의 서술 라벨 인용이며 Glossary 표제어가 아니다.

거버넌스: 이 문서는 `entry/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core·UAF 계약을 특정 실행 환경·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 직렬화 형식·물리 경로·환경 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, 자매 memory-binding.md §0·contract-binding.md §0과 동형). 단 이 문서는 UAF 정본(entry/specs/01-entry.md §3·§4)과 UAHF 정본을 **재정의하지 않는다** — 계약(Entry Descriptor 모델·엔진 5단계·결정 테이블·Evidence 스키마·EN-INV)은 § 포인터로만 인용한다.

---

## §0. 이 문서의 위치와 정본 경계

- **바인딩 대상 정본 선언.** 이 문서는 entry 레이어 자신의 Claude 어댑터 바인딩(`entry/adapters/claude/entry-binding.md`)이며, 그 **바인딩 대상 정본은 `entry/specs/01-entry.md` §3·§4다.** 본 문서는 그 Entry Layer & Entry Resolution 정본을 이 환경 위의 물리 실현으로 바인딩한다.
- **정본은 entry/specs/01 §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소 — Entry Descriptor 등록 모델·5필드(§3.2-A)·Resolution 엔진 고정 5단계(§3.2-A)·Discovery Request 매핑(§3.2-B)·Evidence Source 확장 스키마(§3.2-C)·결정 테이블 8조합·D3(§3.2-D)·mode 네임스페이스(§3.2-E)·불변 EN-INV 1~6(§3.3) — 를 **재정의·확장하지 않는다.** 계약 요소는 정본 § 포인터로만 인용한다. 본 문서가 확정하는 것은 01 §4.1이 "Adapter 소관"으로 미룬 **3불릿(E1 진입 트리거 물리 형태·E2 Evidence 관측 물리 실현·E3 Discovery Request 직렬화)**뿐이다(§2).
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`uahf/framework/core/`·`uahf/framework/runtime/`)와 Module 구현 디렉터리 문서 본문, 그리고 UAF 정본(entry/specs/01) 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이다(structure.md §5 C-3 확장·01 §0 Core 문서 관행). 이 문서는 그 **반대편**이다 — 구체 직렬화 형식·물리 경로(`entry/adapters/claude/…`·`.claude/…`)·파일 확장자·명령 이름의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(memory-binding.md §0·contract-binding.md §0과 동형). 단 **UAF 정본이 명명하지 않은 것을 UAF 정본 문면인 것처럼 서술하지 않는다** — 물리 확정은 전부 본 문서 소유임을 명시한다.
- **하네스 Bootstrap 전제(형태 A, D-v1.2-1).** 이 하네스는 현재 Bootstrap 상태다(Glossary J-13, 자매 바인딩 §0). 본 문서의 바인딩은 (초기) **실행 코드 0**으로 확정되었다 — Entry Resolution 엔진(고정 5단계)은 실행 스크립트가 아니라 **규약 절차**로 실현되며 주 세션이 실수행한다(D-v1.2-1). 따라서 매핑은 (i) 물리 실재 표면(신규 명령 파일 2개), (ii) 규약으로 확정된 정본 문면(형태 A — 판정 수단·직렬화 형식·전달 방식), (iii) 실행 코드 도입 시 로딩될 지점(형태 B — 관측 로더·직렬화기)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **형태 B 도입(2026-07-18 — 예약 슬롯 실현).** 위 (iii)의 예약 슬롯이 `entry/adapters/claude/entry_resolve.py`(Entry Resolution 결정적 실행 로더·LLM 0·순수 판독)와 `entry/adapters/claude/entry-registry.json`(결정 테이블 8조합·Evidence 2종·관측 규칙의 물리 직렬화·Policy as Data)으로 실현되어 형태 A와 **공존**한다. 형태 B는 형태 A(규약 절차)를 대체하지 않고 그 판정 수단(§4)·직렬화(§5)를 실행 코드로 실현하며, 규약 절차는 폴백으로 유지된다. **형태 A→B 전환에도 01 §3 Core Contract(Descriptor 모델·엔진 5단계·결정 테이블·Evidence 스키마·EN-INV) 변경은 0이다**(structure.md §7 C-1 동형·§8 "유지되는 것" 열). 실현 상세는 §2 "실재 여부" 열·§4.4·§5.2·§10에 있다.
- **경계 분담.** Discovery Request의 **직렬화 형식·전달 방식**은 본 문서(§5)가 소유·확정한다. 그 물리 기록이 놓일 **백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위 구조; 물리 위치는 2차 산출물 디커플링 트랙에서 확정)**는 본 문서 밖이며, 본 문서는 직렬화 형식·전달 방식 확정에서 멈춘다.
- **실측 기반 상태 서술(L-07).** "실재/미존재" 주장은 파일 시스템 확인 후에만 기입한다. 본 문서가 참조하는 `uahf/framework/adapters/claude/discovery-data/` 트리의 상태는 §10에서 확인한다.
- **네임스페이스·용어.** 본 문서가 확정하는 것은 물리 표기(명령 파일 형태·판정 수단·직렬화 형식·전달 방식)뿐이며, 01이 소유하는 스키마 용어(`name`·`trigger`·`requiredEvidence`·`decisionRows`·`modeMapping`·`sourceType`·`capability`·`valueDomain` 등)는 01 정의를 § 포인터로 참조하고 재정의하지 않는다. 새 UAHF 용어·새 계약 요소(Descriptor 필드·연산·불변·kind)를 신설하지 않는다.

---

## §1. 목적

이 문서는 entry/specs/01 "### §4.1 바인딩 대상"의 **3불릿**을 이 환경 위에 **v1.2 시점의 구체 물리 실현**으로 매핑한다. Entry Resolution의 산출인 Discovery Request는 하류 Project Discovery의 선행 확정 인터페이스(ARCHITECTURE.md §12.2)이므로, 이 문서가 확정하는 물리 인터페이스는 v1.2 E2E·후속 작업의 물리 실현 기반이다.

책임은 셋이다.

- 01 §4.1 바인딩 표 **3불릿 전부**(E1 진입 트리거 물리 형태 · E2 Workspace Evidence 관측 물리 실현 · E3 Discovery Request 직렬화)를 물리 실현으로 확정한다(§2 — 실재/규약 실현/형태 B 3구분).
- **E1**: 논리 Entry `/new`·`/continue`의 물리 발화 형태를 진입 명령 문서로 확정한다(§3). **E2**: contract-presence·repository-presence의 존재 판정 수단(탐지 절차)을 확정한다(§4 — §4.0 사용자 폴더 주입으로 관측 로커스 확정·contract-binding §4.1 위임 해소·repository-presence 사용자 신규/기존 선언 기반). **E3**: Discovery Request {mode, inputs, policy}의 직렬화 형식·전달 방식을 확정하고, 기록 백엔드 트리의 물리 위치는 2차 산출물 디커플링 트랙에서 확정한다(§5).
- 결정 테이블 실동작(행 1·행 6)을 예시하고(§6), EN-INV 준수를 자기 점검하며(§7), 01 §4.2 이식 교체 지점에 대응을 명시하고(§8), 상태 서술을 실측과 대조한다(§10).

이 문서는 01 §3·§4·UAHF 정본의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A → 형태 B 전환 시에도 01 §3 계약 변경은 0이며(structure.md §7 C-1 동형), §8의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 01 §4.1 바인딩 표 3불릿 물리 실현 (done 2)

01 "### §4.1 바인딩 대상"의 **3불릿 전부**를 물리 표면으로 매핑한다. "01 §4.1 바인딩 지점" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 형태·수단·형식을, "실재 여부" 열이 Bootstrap 상태에서의 **물리 실재 / 규약 실현(형태 A) / 형태 B**를 정직하게 구분한다(§10 실측 대조).

| # | 01 §3 계약 요소 (정본 §) | 01 §4.1 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| E1 | 진입 트리거 (Entry Descriptor `trigger` — §3.1·§3.2-A) | "진입 트리거의 물리 형태 … 그 물리 발화 형태(어떤 진입 명령·선택·추론으로 Entry가 발화되는가)는 Adapter가 바인딩한다. Core Contract는 논리 name·trigger만 소유한다." | 논리 Entry `/new`·`/continue`(01 §3.1·§0 논리 식별자)의 물리 발화 형태 = `.claude/commands/uaf-new.md`·`uaf-continue.md` **문서 명령**. 상세 §3. | **물리 실재**: 두 명령 파일 신규 생성(형태 A 문서 명령). **규약 실현(형태 A)**: Entry Resolution 엔진 고정 5단계 = 규약 절차(주 세션 실수행). **형태 B**: 진입 발화→해소 실행 로더 — **도입**: `entry/adapters/claude/entry_resolve.py`(결정적 실행 로더·LLM 0). 명령(§3)이 이 로더를 호출해 해소 결과를 수령한다. |
| E2 | Workspace Evidence 관측 (Evidence Source capability·유/무 값 도메인 — §3.2-C) | "Workspace Evidence 관측의 물리 실현 … contract-presence·repository-presence를 실제 환경에서 어떻게 탐지하는가(경로 관례·직렬화 형식·존재 판정 수단)는 Adapter 소관이다. Core Contract는 capability 선언과 유/무 값 도메인만 소유한다." | §4.0 사용자가 주입한 대상 폴더 + 신규/기존 의도로 관측 로커스 확정(구 ambient 자동 스캔 대체). contract-presence = 주입 폴더로 스코프한 Contract 저장 위치의 인스턴스 파일(`project-contract.v<N>.md`) 유무 실측(존재 판정 수단 = 본 문서 확정, §4.1). repository-presence = 사용자 신규/기존 선언 기반 유/무(§4.2). Entry는 유/무만 관측(01 EN-INV 2). 상세 §4. | **규약 실현(형태 A)**: 판정 수단(탐지 절차) = 정본 문면 확정. **규약 실현(형태 A)**: 실제 관측 = 규약 절차(주 세션). **형태 B**: 탐지 로더 — **도입**: `entry_resolve.py`가 §4 판정 수단을 실행 — contract-presence·repository-presence 를 파일시스템 실측(순수 판독·유/무만·내용 파싱 0·EN-INV 2)하고 경로·직교 관측 규칙은 `entry-registry.json` observation 데이터로 소비(§4.4). Contract 인스턴스 데이터·`uahf/framework/adapters/claude/discovery-data/`는 본 문서 밖(§10 실측). |
| E3 | Discovery Request 산출 (§3.2-B 매핑·§3.2-E mode 네임스페이스) | "Discovery Request 직렬화. {mode, inputs, policy}의 물리 직렬화·전달 방식은 Adapter 소관이다." | {mode, inputs, policy} = 자기서술 **구조화 레코드**로 직렬화(§5.1)·전달(§5.2). ARCHITECTURE §12.2·01 §3.2-B 추상 정합·재정의 0. 기록 백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위)의 물리 위치는 2차 산출물 디커플링 트랙에서 확정. 상세 §5. | **규약 실현(형태 A)**: 직렬화 형식·전달 방식 = 정본 문면 확정. **형태 B**: 직렬화기/로더 — **도입**: `entry_resolve.py`가 {mode, inputs, policy}(§5.1 레코드)를 구조화 JSON 으로 방출(stdout)한다 — matchedRow·gate(= `policy.ref == user-confirmation-gate` 의 투영·별도 판정 아님) 는 엔진 메타로 병기(Discovery Request 자체 아님). 기록 백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위)의 물리 위치는 본 문서 밖·2차 산출물 디커플링 트랙(§10 실측). |

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

- **논리 식별자 주의(01 §0).** `/new`·`/continue`는 Entry의 **논리 식별자(name)**이며, 물리 진입 형태(어떤 진입 명령·선택·추론으로 발화되는가)는 Adapter 소관이다(01 §0·§4.1). 이 환경의 물리 발화 형태가 위 `uaf-` 접두 명령임을 본 문서가 확정한다. `uaf-` 접두 = UAF 네임스페이스 표면화 + 환경 빌트인 명령과의 충돌 회피.

### §3.2 골격 준거·확정 근거

- **골격 준거.** 두 명령은 `.claude/commands/uahf-status.md` 선례와 동형이다 — (i) YAML front-matter(`description:`), (ii) 형태 A(실행 코드 0), (iii) **정본 포인터 전용**(값 하드코딩 0 — 정본이 진행돼도 명령이 낡지 않음). `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰이 허용된다(structure.md §2 Adapter 경계, uahf-status.md §0).
- **재정의 0.** 두 명령은 01·본 entry-binding 정본을 **재정의하지 않는다** — 안내 포인터만 담는다. 각 명령은 Entry Resolution **규약 절차**(엔진 고정 5단계·결정 테이블 대조)와 **사용자 개입 지점**(Preserve Human Authority 게이트)을 정본 § 포인터로 안내한다: `uaf-new.md`는 `/new` 결정 행(01 §3.2-D 행 1~4)·D3 ①을, `uaf-continue.md`는 `/continue` 결정 행(행 5~8)·D3 ②·③을 가리킨다.
- **엔진 실현 = 형태 B 로더 + 규약 절차 폴백.** 명령 파일 자체는 실행 코드를 담지 않으나, Entry Resolution 엔진 고정 5단계(01 §3.2-A)는 이제 형태 B 로더 `entry_resolve.py`(2026-07-18 도입·§4.4·§5.2) 호출로 실현되며, 로더 미가용 시 **주 세션이 규약 절차로 실수행**한다(형태 A 폴백·D-v1.2-1). 어느 경로든 판별 결과·01 §3 계약은 동일하다(§10).

---

## §4. E2 — Workspace Evidence 관측 물리 실현 (done 4)

01 §4.1 불릿 2("contract-presence·repository-presence를 실제 환경에서 어떻게 탐지하는가 — 경로 관례·직렬화 형식·존재 판정 수단 — 는 Adapter 소관")의 물리 실현을 확정한다. **capability 선언과 유/무 값 도메인은 01 §3.2-C가 소유**하며(재정의 0), 본 문서는 그 **존재 판정 수단(탐지 절차)**만 확정한다. Entry는 유/무만 관측하고 증거를 수집·해석하는 Discovery를 수행하지 않는다(01 §3.2-A 2단계 "관측만"·EN-INV 1·2).

### §4.0 Workspace-target 주입 — 관측 로커스 확정 (하이브리드)

- **주입 입력(물리 addressing).** 진입 시 사용자가 **대상 폴더(경로/폴더명) + 신규/기존 의도**를 주입하며, 이 주입이 §4.1·§4.2 관측의 *위치와 방식*을 확정한다. 이는 구 암묵적 ambient 스캔(워크스페이스 자동 탐색)을 **대체**한다 — 주 세션은 워크스페이스를 자동 탐색하지 않고, 주입된 폴더로 관측을 스코프·확인한다.
- **논리 입력 불변(재정의 0).** 이 주입은 01 §3.2-C의 Workspace Evidence(contract-presence·repository-presence, 유/무 값 도메인)를 **재정의하지 않는다** — 사용자 주입은 그 Evidence를 *어디서·어떻게* 관측할지의 물리 addressing(01 §4.1이 Adapter에 위임한 "경로 관례·존재 판정 수단")일 뿐이다. 논리 입력·유/무 값 도메인은 불변이며, 결정 테이블(8조합)·mode 매핑도 무변경이다(EN-INV 3).
- **폴더 생성 의미 없음(EN-INV 1).** 주입된 "신규 폴더명"은 **의도의 기록**일 뿐이다 — Entry는 폴더를 생성·scaffold하지 않으며, 실제 폴더 생성·초기화는 하류 Discovery 소관이다(01 EN-INV 1). 주입은 관측 로커스를 확정할 뿐 워크스페이스를 변경하지 않는다.
- **의도 분기(관측 방식 — 상세 §4.1·§4.2).**
  - **"신규 폴더명" 주입** → repository-presence = **무**로 확정하고, 에이전트는 그 폴더가 부재이거나 빈/맨 초기화 상태인지 *확인*만 한다(자동 탐색 아님). contract-presence도 그 폴더 기준 무.
  - **"기존 폴더" 주입** → repository-presence = **유**. 에이전트는 그 폴더로 **스코프를 좁혀** contract-presence를 스캔한다(incremental vs brownfield 판정용, §4.3·§6).

### §4.1 contract-presence — 존재 판정 수단 (contract-binding §4.1 위임 해소)

- **capability(정본 소유).** "워크스페이스에 Project Contract가 존재하는가"를 관측한다. 값 도메인 = 유/무 (01 §3.2-C).
- **저장 위치(선행 확정 — contract-binding §4).** Contract 인스턴스는 `project-contract.v<N>.md` 파일로 직렬화되며(Markdown 본문 + YAML front-matter, contract-binding §3), 저장 위치는 이원화되어 있다 — 일반 관례 = 소비 프로젝트 내 `.claude/project-contract/`, 본 UAF 저장소 인스턴스 = `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`(contract-binding §4).
- **존재 판정 수단(본 문서 확정 — 탐지 절차, §4.0 주입 스코프).** contract-presence의 유/무는 §4.0에서 주입된 대상 폴더로 **스코프를 좁혀**, 그 폴더의 Contract 저장 위치에 **인스턴스 파일(`project-contract.v<N>.md`)이 하나라도 존재하는지**의 실측으로 판정한다(구 ambient 전역 스캔이 아니라 주입 폴더 국소 관측).
  - **기존 의도 주입 시** — 주입된 폴더의 Contract 저장 위치(소비 프로젝트: `<주입 폴더>/.claude/project-contract/`; 본 저장소 dogfooding: `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`)에 `project-contract.v<N>.md` 인스턴스 파일이 하나 이상 존재하면 **유**, 존재하지 않으면 **무**(디렉터리 부재 포함). 이 유/무가 incremental(유) vs brownfield(무·repo 유) 판정을 가른다(§4.3·§6).
  - **신규 의도 주입 시** — 주입된 폴더는 부재/빈 상태 확인으로 Contract 인스턴스가 없으므로 contract-presence = **무**.
- **관측 한계(EN-INV 2).** Entry는 파일 **유무만** 관측한다 — front-matter·본문을 파싱·해석·생성하지 않는다. Contract 내용 해석·최신 인스턴스 해소(`instanceVersion`·`supersedes`)는 하류 소비(Advisor Consult·tolerant reader) 소관이며 Entry 관측 밖이다(01 EN-INV 2, contract-binding §3·§4). 이로써 contract-binding §4.1이 "존재 판정 수단(탐지 실행)의 상세는 후속 entry-binding.md 소관"으로 미룬 지점이 해소된다.

### §4.2 repository-presence — 존재 판정 수단 (사용자 신규/기존 선언 기반)

- **capability(정본 소유).** "워크스페이스에 Repository가 존재하는가"를 관측한다. 값 도메인 = 유/무 (01 §3.2-C).
- **판정 수단의 정본 근거.** 01 §3.2-D 판별 규칙 **D3 ②**는 이 Evidence가 실현하는 결과를 "**기존 저장소가 있으나 아직 Contract가 없는 최초 도입**"의 Brownfield Full Discovery로 규정한다(행 6). 즉 이 맥락에서 "Repository 존재"는 **워크스페이스에 이어갈 기존 프로젝트 본체(기존 프로젝트 콘텐츠)가 실재하는가**를 뜻한다(Brownfield의 정의 — ARCHITECTURE.md §2.2 파이프라인·01 §3.1 `/continue` Brownfield). 본 문서는 이 capability를 재정의하지 않고, 그 정본 의미에 정합하는 **물리 판정 수단**을 확정한다(§4.1 불릿 2가 "존재 판정 수단"을 Adapter 소관으로 위임).
- **존재 판정 수단(본 문서 확정 — §4.0 주입이 관측 로커스·기대값 설정).** §4.0에서 주입된 **사용자 신규/기존 선언**은 관측 로커스(어느 폴더인가)와 기대값을 설정하고, repository-presence의 유/무는 에이전트가 그 폴더 상태를 **확인 관측**한 결과로 확정된다(구 ambient 콘텐츠 휴리스틱을 대체 — 워크스페이스 자동 탐색·VCS 마커 논리가 아니라 사용자가 지정한 폴더의 확인 관측이 판정 근거다). **선언은 관측을 대체하지 않는다** — 유/무의 확정은 확인 관측이며(01 §3.2-A 2단계 "관측만"·"유무 값의 확정 관측" 정합), 선언과 확인 관측이 상충하면 아래 충돌 처리 note로 라우팅된다.
  - **"신규 폴더명" 선언 → (기대값 무).** 에이전트가 그 폴더의 부재/빈·맨 초기화 상태(이어갈 기존 프로젝트 콘텐츠 없음)를 확인 관측하면 repository-presence = **무**로 확정한다.
  - **"기존 폴더" 선언 → (기대값 유).** 에이전트가 그 폴더에 이어갈 실질 프로젝트 콘텐츠(소스·문서·설정 등 빈/맨 초기화를 넘는 본체)가 실재함을 확인 관측하면 repository-presence = **유**로 확정한다.
- **D3 ② Brownfield 정합.** "기존 폴더" 선언(repo 유)이면서 그 폴더에 Contract 인스턴스가 없으면(§4.1 무) 결정 테이블 행 6(Brownfield Full Discovery — 기존 저장소 있으나 Contract 부재)로 정합한다. 본 UAF 저장소도 `entry/`·`discovery/`·`planning/`·`orchestration/`·`knowledge/`·`uahf/`·`docs/` 등 방대한 기존 프로젝트 콘텐츠를 실재로 보유하므로, 이 저장소를 "기존 폴더"로 주입하면 repo = 유로 확정된다. Entry는 유/무만 관측한다(EN-INV 2).
- **두 E2E 시나리오 실관측(문면 시연).**
  - **신규 폴더 주입 → 무.** 사용자가 신규 폴더명 주입 → repository-presence = **무**(폴더 부재/빈 상태 확인).
  - **기존 폴더 주입 → 유.** 사용자가 기존 폴더 주입 → repository-presence = **유**(그 폴더의 실질 프로젝트 콘텐츠 실재 확인; 예: 본 UAF 저장소를 주입하면 유, §10 실측).
- **관측 한계.** Entry는 콘텐츠의 **유무만** 관측하며 그 내용을 수집·해석하지 않는다(01 §3.2-A 2단계·EN-INV 1). 기존 프로젝트 콘텐츠의 실제 이해·분석은 하류 Project Discovery(Brownfield Full Discovery) 소관이다.

**충돌 처리 note — 선언 ↔ 실제 상태 상충은 canonical 결정 테이블 policy에 포섭 (EN-INV 6).** §4.0 주입 선언과 실제 폴더 상태가 상충할 수 있다 — 예: "신규" 선언인데 주입 폴더에 실질 콘텐츠 존재 / "기존" 선언인데 주입 폴더가 부재·빈 상태. 이 충돌은 **별도 신호가 아니라 확인 관측이 해소되는 canonical 결정 테이블 행의 policy로 구동**된다(Policy as Data 단일 소스) — "신규인데 콘텐츠"는 확인 관측이 **행 2·4**로 해소되어 그 canonical policy(repository-present/contract-present)가 이미 사용자 확인 게이트이고, "기존인데 이어갈 실체 전무(Contract 무·Repo 무)"는 **행 5**(nothing-to-continue)로 해소된다. **단 Contract가 존재하면(행 7·8) repo 유무와 무관하게 incremental·게이트 없음이다**(D3 ③ — Contract 자체가 이어갈 대상; "기존 선언인데 repo 무"라도 거짓 게이트를 만들지 않는다). Entry는 관측값을 **임의로 덮어쓰지 않으며**(01 §3.2-D 충돌 처리·EN-INV 6), 게이트를 canonical policy로 표면화만 하고 확정 결정을 내리지 않는다(ARCHITECTURE.md §8 UAF-INV ⑤). **병행 imperative conflict 판정을 두지 않는다**(행 7 거짓 게이트 정정·CP2). 충돌 해소 과정에서도 Entry는 폴더를 생성·scaffold하지 않는다(EN-INV 1) — "신규 폴더명"은 의도 기록일 뿐 실제 생성은 하류 Discovery 소관이다.

### §4.3 관측 결과의 소비

관측된 두 Evidence(contract-presence·repository-presence의 유/무)는 Entry Resolution 엔진 3단계(우선순위 평가, 01 §3.2-A)에서 명시 Entry의 결정 행(§3.2-D)에 대조되며, Discovery Request의 `inputs`(Evidence 참조 목록, §5·01 §3.2-B)에 확정 참조로 담긴다.

### §4.4 형태 B 실현 — 판정 수단의 실행 코드화 (가법·재정의 0)

본 §4가 확정한 판정 수단(§4.0 주입 로커스·§4.1 contract-presence 탐지·§4.2 repository-presence 판정)의 **정본 문면은 그대로 유지**되며, 아래는 그 form-B 실현 경로를 가법으로 명시한다(정본 재정의·확장 0 — 이 절은 §4.0~§4.3의 판정 수단 정의를 실행 코드로 실현하는 경로만 기록한다).

- **실현 산출물.** `entry/adapters/claude/entry_resolve.py`(결정적 실행 로더·LLM 0·순수 판독)가 §4 판정 수단을 실행한다. 경로 관례·직교 관측 규칙은 코드에 하드코딩하지 않고 `entry-registry.json`의 `observation` 데이터로 소비한다(Policy as Data).
- **contract-presence(§4.1 실현).** `observation.contractLocations`(주입 폴더 기준 상대 glob — `.claude/project-contract/project-contract.v*.md` 및 dogfooding `.../discovery-data/contracts/*/project-contract.v*.md`)에 인스턴스 파일이 하나라도 실재하면 유, 없으면 무. **파일 유무만 실측하며 front-matter·본문을 파싱하지 않는다**(EN-INV 2).
- **repository-presence(§4.2 실현).** 주입 폴더에 '이어갈 실질 프로젝트 본체' 파일이 하나라도 실재하면 유, 부재/빈/맨 초기화면 무. **Contract 저장 위치·`.git/`·OS 메타데이터는 본체에서 제외**(`observation.repositoryBody.excludePrefixes`·`ignoreBasenames`)하여 contract·repo 두 축을 직교로 유지한다(D3 ② '프로젝트 본체' 의미·01 §3.2-C 2축 독립). 엣지 임계값(단일 README 등)은 여전히 Adapter 재량이며 상충 시 사용자 확인 게이트로 라우팅된다(§11 OQ-TE-1).
- **게이트 = canonical 결정 테이블 policy(별도 conflict 신호 아님·§4.2 note 실현).** 게이트는 매칭 행의 **`policy.ref == user-confirmation-gate`**(canonical 결정 테이블 행 2·3·4·5·정본 = 01 §3.2-D)로만 구동되며, 게이트 이유는 그 행의 `policy.conflict`(repository-present/contract-present/nothing-to-continue)에 있다. 로더는 이 값을 방출 필드 `gate`(policy.ref 의 투영)로 표면화만 하고 확정 결정을 내리지 않는다(게이트 제시는 주 세션 소관·EN-INV 6). **하이브리드 선언↔상태 충돌(§4.2 note)은 별도 imperative 판정이 아니라 이 canonical policy에 포섭된다** — "신규인데 콘텐츠 존재"=행 2·4, "기존인데 이어갈 실체 전무"=행 5. **Contract 존재 시(행 7·8)는 D3 ③에 따라 incremental·게이트 없음**이다(거짓 게이트 방지·CP2 정정). 병행 imperative conflict 판정을 두지 않는다(Policy as Data 단일 소스).
- **불변.** 로더는 폴더를 생성·scaffold 하지 않으며(순수 판독·EN-INV 1), 결정 테이블·mode 매핑·게이트를 재정의하지 않는다(전부 `entry-registry.json` 데이터·정본 = 01 §3.2-D). 형태 A(규약 절차)는 폴백으로 유지된다.

---

## §5. E3 — Discovery Request 직렬화·전달 확정 (done 5)

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
- **형태 B(도입 — 2026-07-18).** 직렬화기·로더 실행 코드 `entry_resolve.py`가 도입되어 같은 레코드 형식을 방출한다 — {mode, inputs, policy}를 구조화 JSON(stdout)으로 산출하고, matchedRow·gate(= canonical `policy.ref == user-confirmation-gate` 의 투영·별도 판정 아님) 를 엔진 메타로 병기한다(엔진 메타는 Discovery Request 자체가 아니다 — §5.1 3요소만이 Discovery Request다). 형태 B 도입에도 §12.2·01 §3.2-B 계약 변경은 0이다(structure.md §7 C-1 동형). 형태 A(규약 절차 방출)는 폴백으로 유지된다.

### §5.3 경계 분담 — 백엔드 트리 위치 확정 위임

- **본 문서 소유.** Discovery Request의 **직렬화 형식(§5.1)·전달 방식(§5.2)**은 본 문서가 확정한다.
- **후속 위임.** 그 물리 기록이 놓일 **백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위의 Discovery Request 기록 구조)의 물리 위치는 2차 산출물 디커플링 트랙에서 확정**하며, 본 문서는 직렬화 형식·전달 방식 확정에서 멈춘다. 본 문서가 백엔드 트리 구조·물리 위치를 창설하면 그 트랙의 소관을 선취하므로, 여기서 멈춘다.

---

## §6. 결정 테이블 실동작 예시 (done 6 — 행 1·행 6)

01 §3.2-D 결정 테이블을 **재정의하지 않고 행을 인용**하여, 물리 관측(§4) → 단일 Discovery Request 산출(§5)의 규약 절차를 두 행에 대해 예시한다. 각 조합이 정확히 한 결과로 해소됨(결정성 불변, EN-INV 3)을 보인다.

### 예 A — 결정 테이블 행 1 (contract 무 · repo 무 → greenfield)

**시나리오.** 사용자가 **신규 폴더명 주입**(예: `./my-product`). 명시 Entry = `/new`(물리 발화: `uaf-new` 명령, §3). 주입된 폴더는 부재/빈 상태.

**해소 (Resolution 엔진 5단계, 01 §3.2-A — 물리 관측).**

1. 매칭 — `/new` Descriptor를 Registry에서 찾는다.
2. 증거 수집(관측, §4.0 주입 스코프) — 사용자가 신규 폴더명을 주입 → repository-presence: 신규 선언 → **무**(폴더 부재/빈 상태 확인, §4.2); contract-presence: 그 폴더에 `project-contract.v<N>.md` 없음 → **무**(§4.1). UAF 저장소 ambient 스캔이 개입하지 않는다(§4.0).
3. 우선순위 평가 — 관측 {무, 무}을 `/new` 결정 행에 대조 → **01 §3.2-D 행 1** 매칭.
4. 결정성 검증 — 이 조합은 단일 행(1)에만 매칭.
5. 방출 — 단일 Discovery Request `{ mode: greenfield, inputs: [contract-presence(무), repository-presence(무)], policy: 기본 정책 참조 }`(§5.1 레코드).

**결과.** Greenfield 정상 경로(01 §3.2-D 행 1, 근거 P-C). Entry는 여기서 멈춘다 — Discovery 수행·Contract 생성은 하지 않는다(EN-INV 1·2).

### 예 B — 결정 테이블 행 6 (contract 무 · repo 유 → brownfield, D3 ②)

**시나리오.** 사용자가 **기존 폴더 주입**(기존 프로젝트 콘텐츠가 실재하나 아직 Contract가 없는 폴더 — 본 UAF 저장소 dogfooding 포함). 명시 Entry = `/continue`(물리 발화: `uaf-continue` 명령, §3).

**해소 (Resolution 엔진 5단계, 01 §3.2-A — 물리 관측).**

1. 매칭 — `/continue` Descriptor를 Registry에서 찾는다.
2. 증거 수집(관측, §4.0 주입 스코프) — 사용자가 기존 폴더를 주입 → repository-presence: 기존 선언 → **유**(그 폴더의 실질 프로젝트 콘텐츠 실재 확인; 예: `entry/`·`discovery/`·`planning/`·`orchestration/`·`knowledge/`·`uahf/`·`docs/` 등, §10 실측, §4.2); contract-presence: 주입된 폴더로 스코프한 Contract 저장 위치(`uahf/framework/adapters/claude/discovery-data/contracts/uahf/` 등)에 인스턴스 파일 없음 → **무**(§4.1).
3. 우선순위 평가 — 관측 {무, 유}을 `/continue` 결정 행에 대조 → **01 §3.2-D 행 6** 매칭.
4. 결정성 검증 — 이 조합은 단일 행(6)에만 매칭.
5. 방출 — 단일 Discovery Request `{ mode: brownfield, inputs: [contract-presence(무), repository-presence(유)], policy: 기본 정책 참조 }`(§5.1 레코드).

**결과.** Brownfield Full Discovery, 최초 Project Contract 생성 요청(01 §3.2-D 행 6, 판별 규칙 **D3 ②**). Entry는 여기서 멈춘다 — 최초 Contract 생성은 하류 Project Discovery 소관이다(EN-INV 1·2). **이 예가 §4.0 주입 방식의 필요성을 실증한다** — 구 ambient 자동 스캔이었다면 이 저장소처럼 방대한 기존 콘텐츠·비표준 Contract 저장 위치를 가진 워크스페이스에서 "이 저장소를 이어갈지 vs 하위 새 폴더에서 시작할지"의 사용자 의도를 분간하지 못하나, 사용자의 "기존 폴더" 주입 선언으로 repository-presence = **유**가 확정되어 행 6(Brownfield)로 결정적으로 해소된다.

---

## §7. EN-INV 자기 점검 (done 7)

본 물리 바인딩이 01 §3.3 EN-INV를 훼손하지 않음을 자가 점검한다. 자체 점검은 최종 승인이 아니다 — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다(02 §3.2-A).

- **EN-INV 1 — Entry Resolution만.** 본 문서는 진입 트리거(§3)·Evidence 관측(§4)·Discovery Request 직렬화(§5)의 **물리 실현만** 바인딩한다. Discovery 수행·Contract 생성의 물리 절차를 도입하지 않으며, 두 명령(§3)도 Discovery Request 산출까지만 안내한다. **§4.0 주입의 "신규 폴더명"은 의도 기록일 뿐이며 Entry는 폴더를 생성·scaffold하지 않는다** — 실제 폴더 생성·초기화는 하류 Discovery 소관이다(충돌 처리 note 재확인). Entry 산출 = Discovery Request 하나(01 EN-INV 1). **준수 — 위반 서술 0.**
- **EN-INV 2 — Contract 직접 생성·해석 금지.** §4.1의 contract-presence 판정 수단은 §4.0 주입 폴더로 스코프한 인스턴스 파일 **유무만** 실측하며 front-matter·본문을 파싱·해석·생성하지 않는다. §4.2의 repository-presence도 사용자 신규/기존 선언 기반의 콘텐츠 **유무만** 관측한다(값 도메인 유/무 불변 — 관측 수단이 사용자 주입으로 바뀌어도 관측되는 값은 유/무 그대로). Entry는 Contract를 Evidence(유/무)로만 관측한다(01 EN-INV 2). **준수 — 위반 서술 0.**
- **EN-INV 3 — 결정성.** §6 두 예시(행 1·행 6)에서 각 관측 조합이 01 §3.2-D 결정 테이블의 **단일 행**으로 해소됨을 보였다. 본 문서는 결정 테이블(8조합)을 재정의하지 않고 **행 인용만** 한다(01 §3.2-A 4단계·EN-INV 3). **준수 — 위반 서술 0.**
- **EN-INV 5 — Discovery Request 정합·재정의 0.** §5.1 레코드의 3요소({mode, inputs, policy})는 ARCHITECTURE §12.2·01 §3.2-B 추상에 1:1 정합하며 — `mode` = 확장 네임스페이스(01 §3.2-E), `inputs` = Evidence 참조 목록, `policy` = 참조 — 추상을 재정의·확장하지 않는다(01 EN-INV 5). **준수 — 위반 서술 0.**
- **EN-INV 6 — 확정 게이트 보존.** 두 명령(§3)이 사용자 확인 게이트를 정본 포인터로 안내하며, 게이트는 **canonical 결정 테이블 policy(`policy.ref == user-confirmation-gate`·행 2·3·4·5) 단일 소스**로만 구동된다(§4.2 note·§4.4). §4.0 선언↔실제 상태 상충(예: "신규"인데 콘텐츠 존재=행 2·4 / "기존"인데 이어갈 실체 전무=행 5)은 별도 신호가 아니라 그 canonical policy에 포섭되며, Contract 존재 시(행 7·8)는 incremental·게이트 없음이다(거짓 게이트 방지·CP2 정정). 로더는 관측값을 임의로 덮어쓰지 않고 canonical policy를 `gate`(policy.ref 투영)로 표면화만 한다(01 EN-INV 6·§3.2-D 충돌 처리·ARCHITECTURE.md §8 UAF-INV ⑤·병행 imperative 판정 없음). **준수 — 위반 서술 0.**

(EN-INV 4 — Layer·엔진 불변 확장 — 는 신규 Entry·Evidence Source·mode 추가의 확장성 계약이며, 본 문서는 기존 2 Entry의 물리 실현만 다루므로 별도 확장 서술을 두지 않는다.)

---

## §8. 01 §4.2 이식 교체 지점 대응 (done 8)

01 "### §4.2 이식 교체 지점"의 3개 교체 지점 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 01 §3 Core Contract 불변(structure.md §7 C-1 동형)을 재확인한다.

| 01 §4.2 교체 지점 (바뀌는 것) | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (01 §3 불변) |
|---|---|---|---|
| 진입 트리거의 물리 형태 | §2 E1, §3 | `.claude/commands/uaf-new.md`·`uaf-continue.md` 문서 명령. | 01 §3.2-A Entry Descriptor 등록 모델(논리 name·`trigger` 논리 서술)·Resolution 엔진 고정 5단계, §3.1 Entry 논리 name `/new`·`/continue`. |
| Evidence 관측의 물리 수단 | §2 E2, §4 | **§4.0 사용자 주입 폴더로 스코프한 유/무 관측** — contract-presence = 주입 폴더의 Contract 저장 위치 인스턴스 파일(`project-contract.v<N>.md`) 유무 실측·repository-presence = 사용자 신규/기존 선언 기반 유/무(신규→무·기존→유). 구 ambient 자동 스캔 대체. | 01 §3.2-C Evidence Source 선언 스키마(sourceType·capability·valueDomain)·유/무 값 도메인·v1.1 Evidence 2종 capability. |
| Discovery Request의 직렬화 | §2 E3, §5 | {mode, inputs, policy} 자기서술 구조화 레코드 직렬화·전달. | 01 §3.2-B Discovery Request 매핑·§3.2-E mode 네임스페이스, ARCHITECTURE §12.2 Discovery Request 추상(mode 확장 네임스페이스·inputs Evidence 참조 목록·policy 참조). |

- "유지되는 것" 열의 계약은 다른 AI·실행 환경으로 이식해도 바뀌지 않는다 — 01 §3 Core Contract의 이식 불변성이며, 01 §4.2 "바뀌지 않는 것"(Entry Descriptor 등록 모델·Resolution 엔진의 고정 알고리즘·결정 테이블 데이터·Evidence Source 선언 스키마·Discovery Request 추상 정합)과 정합한다. structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 동형이다.
- 본 문서는 01 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고, v1.2 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §10. 상태 서술 실측 대조 (L-07 — 미존재를 실재로 쓰지 않음)

본 문서는 `entry/adapters/claude/`에 실재하며, 물리 생성물은 진입 명령 파일 2개(`.claude/commands/uaf-new.md`·`.claude/commands/uaf-continue.md`)와 **형태 B 실행 산출물 2개(`entry/adapters/claude/entry_resolve.py` 결정적 실행 로더·`entry/adapters/claude/entry-registry.json` 결정 테이블 데이터)**, 그리고 결정적 테스트(`entry/adapters/claude/tests/`)다. 본 문서가 확정한 진입 명령 형태(§3)·Evidence 판정 수단(§4)·Discovery Request 직렬화 형식·전달 방식(§5)은 정본 문면(형태 A)이며, §4.4·§5.2가 그 form-B 실현 경로다 — 형태 A와 공존하며 01 §3 계약 변경은 0이다(structure.md §7 C-1). Discovery Request 기록의 백엔드 데이터 트리는 `uahf/framework/adapters/claude/discovery-data/`이며, 그 물리 위치는 2차 산출물 디커플링 트랙에서 확정한다(로더는 stdout 방출까지이며 백엔드 기록 위치를 창설하지 않는다). "실재/미존재" 주장은 파일 시스템 직접 실측 후에만 기입한다 — 미존재를 실재로 쓰지 않는다(L-07). 위 form-B 산출물의 실재·동작은 8조합 실행(행 1~8 각 단일 결과·mode·게이트 = canonical policy)과 행 7(contract 유·repo 무 → incremental·게이트 없음) 거짓 게이트 부재 회귀로 확인되었다(CP2 정정 트랙 실측).

---

## §11. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 entry/specs/01 §3·§4의 물리 실현이다. 어떤 Entry Descriptor 필드·Resolution 엔진 단계·결정 테이블 행·Evidence Source 선언·mode 네임스페이스·불변(EN-INV 1~6)도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 01 §3이다. 새 계약 요소(필드·연산·불변·kind)를 창설하지 않았다.
- **본 문서가 소유·확정하는 것.** 01 §4.1이 "Adapter 소관"으로 미룬 3불릿 — ① E1 진입 트리거 물리 형태(§3, 두 진입 명령) ② E2 Evidence 관측 판정 수단(§4 — contract-presence 탐지 절차·repository-presence 판정 수단) ③ E3 Discovery Request 직렬화·전달(§5) — 만 확정한다. Discovery Request 기록 백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위)의 물리 위치 확정은 2차 산출물 디커플링 트랙에 위임한다. 이로써 contract-binding §4.1이 미룬 **contract-presence 존재 판정 수단(탐지 실행)**이 본 문서 §4.1에서 해소된다.
- **격리 토큰의 단일 자리.** 구체 명령 이름(`uaf-new`·`uaf-continue`)·물리 경로(`.claude/commands/…`·`entry/adapters/claude/…`)·구조화 데이터 형식·파일 확장자는 이 Adapter 경계 문서에 둔다. UAF 정본(entry/specs/01)은 이 토큰을 "Adapter 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3는 이 경계에 비적용 — 격리 보유).
- **동시 작성 문서 경계(07 R2·R4).** 본 산출은 작성 당시 신규 3파일(entry-binding.md·uaf-new.md·uaf-continue.md)만 생성하며, 당시 미완성이던 후속 산출물(E2E 데이터·`uahf/framework/adapters/claude/discovery-data/` 트리 등)을 인용·추측하지 않았다 — 포인터 위임만 했다(07 R2). 확정된 인터페이스 계약(entry/specs/01 §3·§4·contract-binding §3·§4·ARCHITECTURE §12.2)만 참조했다. UAF 정본·UAHF 정본·기존 바인딩(contract-binding.md 포함)·물리 데이터를 수정·생성하지 않았다(07 R4·INV-2). 불확실 지점은 아래 open_questions로 에스컬레이션했다(추측 금지).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-TE-1 (신규/기존 확인 시 "빈/맨 초기화 vs 실질 콘텐츠" 임계값 — 비차단).** §4.2는 repository-presence를 §4.0 사용자 신규/기존 선언으로 확정하고, 에이전트는 선언과 주입 폴더 상태의 정합을 *확인*한다(정본 근거: D3 ② Brownfield 의미·01 §3.2-C capability). 위임된 두 E2E 시나리오(신규 폴더 주입 = 무, 기존 폴더 주입 = 유)는 이 방식으로 명확히 해소된다. 다만 확인 단계의 극단적 엣지 케이스(예: 단일 README·숨김 설정만 있는 폴더를 "신규"로 선언 — 빈/맨 초기화로 볼지 실질 콘텐츠로 볼지)의 정밀 임계값은 Adapter 재량 여지가 있으며, 상충 시 §4.2 말미 충돌 처리 note의 사용자 확인 게이트(EN-INV 6)로 라우팅된다. 필요 시 Advisor가 재확정할 수 있다. 01 §3.2-C capability·유/무 값 도메인 변경은 아니므로 **비차단**이다.
- **OQ-TE-2 (Discovery Request 기록 백엔드 트리 물리 위치 — 후속 트랙, 비차단).** Discovery Request의 물리 기록이 놓일 백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위 구조)의 물리 위치는 §5.3에서 2차 산출물 디커플링 트랙에 위임했다. 그 트랙 착수 시 이 지점의 물리 위치 확정이 필요하다. ARCHITECTURE §12.2·01 §3.2-B 계약 변경은 아니므로 **비차단**이다.

---

## §12. 요약 (한눈에 보기)

- 이 문서 = entry 레이어 자신의 Claude 어댑터 바인딩(`entry/adapters/claude/entry-binding.md`)이며, 바인딩 대상 정본 = `entry/specs/01-entry.md` §3·§4(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 01 "### §4.1 바인딩 대상" **3불릿 전건**(E1·E2·E3)을 물리 실현으로 매핑(실재/규약 실현(형태 A)/형태 B 3구분).
- **§3 (E1):** 논리 Entry `/new`·`/continue`(01 §3.1·§0 논리 식별자)의 물리 발화 형태 = `.claude/commands/uaf-new.md`·`uaf-continue.md` 문서 명령. uahf-status.md 선례 동형(YAML front-matter·형태 A·정본 포인터 전용)·재정의 0·Entry Resolution 규약 절차와 사용자 개입 지점을 정본 § 포인터로 안내.
- **§4 (E2):** §4.0 진입 시 사용자가 **대상 폴더 + 신규/기존 의도를 주입**해 관측 로커스를 확정(구 ambient 자동 스캔 대체·논리 입력 재정의 0). contract-presence = 주입 폴더로 스코프한 Contract 저장 위치의 인스턴스 파일(`project-contract.v<N>.md`) 유무 실측(§4.1 — contract-binding §4.1 위임 해소). repository-presence = 사용자 신규/기존 선언 기반(신규→무·기존→유, §4.2 — D3 ② Brownfield 의미 정합). 선언 ↔ 실제 상태 상충은 사용자 확인 게이트(EN-INV 6)로 라우팅(§4.2 말미 note). Entry는 유/무만 관측(EN-INV 2). 두 E2E 시나리오(신규 폴더 주입→무·기존 폴더 주입→유) 실관측 문면 시연.
- **§5 (E3):** Discovery Request = {mode, inputs, policy} 자기서술 구조화 레코드 직렬화(§5.1)·전달(§5.2). §12.2·01 §3.2-B 추상 정합·재정의 0. 기록 백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위)의 물리 위치는 2차 산출물 디커플링 트랙에서 확정(§5.3).
- **§6:** 결정 테이블 행 1(greenfield, 신규 폴더 주입)·행 6(brownfield, D3 ②, 기존 폴더 주입) 물리 관측 → 단일 Discovery Request 산출 예시(01 §3.2-D 재정의 0·행 인용만·EN-INV 3 결정성). 행 6 예가 §4.0 주입 방식(기존 폴더 주입→repo 유)의 필요성을 실증.
- **§7:** EN-INV 1·2·3·5·6 자기 점검(준수·위반 서술 0). 자체 점검은 최종 승인 아님(Verifier CP2·Advisor CP3 뒤따름).
- **§8:** 01 "### §4.2" 이식 교체 지점 3건 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 01 §3 불변(C-1 동형) 재확인.
- **§10:** 실측 대조(L-07) — 본 문서는 `entry/adapters/claude/`에 실재, 물리 생성물 = 진입 명령 파일 2개. 백엔드 데이터 트리 `uahf/framework/adapters/claude/discovery-data/`의 물리 위치는 2차 산출물 디커플링 트랙에서 확정. 미존재를 실재로 쓰지 않음.
- 01 §3·§4·UAHF 정본 재정의 0, Glossary 용어 신설 0, 새 계약 요소 창설 0. **형태 B 도입(2026-07-18)** — `entry_resolve.py`(결정적 실행 로더·LLM 0)·`entry-registry.json`(결정 테이블 데이터)이 §2 E1/E2/E3 예약 슬롯을 실현하며 형태 A(규약 절차)와 공존한다(01 §3 계약 변경 0·§4.4·§5.2·§10). 구체 명령 이름·물리 경로·직렬화 형식·실행 코드 토큰은 이 Adapter 경계에서 허용된다(격리 지점).
