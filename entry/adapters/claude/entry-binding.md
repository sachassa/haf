# entry/adapters/claude/entry-binding — Claude Code Entry Layer Adapter 바인딩

작성일: 2026-07-07
상태: Baseline · 2026-07-18 관측 수단 개정(Evidence 관측 = 사용자 폴더 주입 하이브리드) — CP2 통과(충족 9/위반 0/판정불가 1: OQ-2)·CP3 승인(OQ-2 = (a) Adapter 물리 addressing·spec 무변경 확정) · 2026-07-18 형태 B 도입(`entry_resolve.py` 결정적 실행 로더·`entry-registry.json` 결정 테이블 데이터 — E1/E2/E3 예약 슬롯 실현·형태 A 공존·01 §3 계약 변경 0·structure.md §7 C-1) · 2026-07-18 CP2 정정(게이트 = canonical 결정 테이블 policy 단일 소스 — 병행 imperative conflict 판정 제거·행 7 거짓 게이트 정정; `--entry new|continue` 정규화·OQ-7) · CP2 재판정 통과·CP3 승인(2026-07-18 — 게이트 행 {2,3,4,5}=01 §3.2-D 1:1·mode/policy 8/8·entry 22 pass·baseline 236 회귀 0·01 무접촉)
상위 규약: AGENT.md
근거 정본: `entry/specs/01-entry.md` §3.1·§3.2-A·§3.2-B·§3.2-C·§3.2-D·§3.2-E·§3.3·§4.1·§4.2·§8(바인딩 대상 정본) · `ARCHITECTURE.md` §12.2 · `planning/adapters/claude/contract-binding.md` §3·§4·§4.1(존재 판정 수단을 본 문서로 명시 위임) · `uahf/framework/adapters/claude/memory-binding.md`(자매 바인딩 골격 선례) · `.claude/commands/uahf-status.md`(진입 명령 골격 선례) · `uahf/framework/core/structure.md` §2·§4·§5·§7 · `uahf/specs/00-glossary.md`. 계약 요소는 § 포인터로만 인용하며 재정의·확장하지 않는다.

---

## §0. 이 문서의 위치와 정본 경계

- **바인딩 대상 정본 = `entry/specs/01-entry.md` §3·§4.** 본 문서는 그 계약(Entry Descriptor 등록 모델·Resolution 엔진 고정 5단계·Discovery Request 매핑·Evidence Source 스키마·결정 테이블 8조합·판별 규칙 D3·mode 네임스페이스·EN-INV 1~6)의 **물리 실현 매핑**이며 재정의·확장하지 않는다. 본 문서가 확정하는 것은 01 §4.1이 Adapter 소관으로 미룬 **3불릿(E1 진입 트리거 물리 형태·E2 Evidence 관측 물리 실현·E3 Discovery Request 직렬화)**뿐이다.
- **격리 지점(C-3 비적용).** 이 경계는 구체 직렬화 형식·물리 경로(`entry/adapters/claude/…`·`.claude/…`)·명령 이름 토큰의 사용이 허용되는 자리이며 그 격리가 존재 이유다(structure.md §2·§5·자매 memory-binding.md §0·contract-binding.md §0 동형). UAF 정본이 명명하지 않은 것을 UAF 정본 문면인 것처럼 서술하지 않는다 — 물리 확정은 전부 본 문서 소유다. **단 격리 대상은 명령 파일 형태·판정 수단·직렬화 형식뿐이며, 특정 AI·모델·제품 기능·방법론은 여기서도 명명하지 않는다**(방법론 축의 정본 근거 = 루트 `ARCHITECTURE.md` §8 UAF-INV ⑥ "Framework는 특정 방법론을 모른다"; AI·모델·제품 기능 축은 이 경계에 대해 어느 정본도 금지를 소유하지 않으므로 — structure.md §5 C-3은 Adapter 경계를 명시 제외한다 — 본 문서 소유 규범으로 둔다).
- **형태 A/B 공존.** 판정 수단(§4)·직렬화(§5)는 규약 절차(형태 A·주 세션 실수행)로 확정되고, 같은 판정을 실행 코드(형태 B — `entry_resolve.py` 결정적 실행 로더·`entry-registry.json` 결정 테이블 데이터)가 실현한다. 형태 A는 폴백으로 유지되며 전환에도 01 §3 계약 변경은 0이다(structure.md §7 C-1).
- **경계 분담·실측 규율.** Discovery Request의 직렬화 형식·전달 방식은 본 문서(§5) 소유이고, 그 물리 기록이 놓일 백엔드 트리 위치는 본 문서 밖(2차 산출물 디커플링 트랙) 소관이다. "실재/미존재" 주장은 파일 시스템 확인 후에만 기입한다(L-07·§10). 01이 소유하는 스키마 용어는 재정의하지 않으며 새 계약 요소·새 UAHF 용어를 신설하지 않는다.

---

## §2. 01 §4.1 바인딩 표 3불릿 물리 실현 (done 2)

"01 §4.1 바인딩 지점" 열은 정본 표현을 그대로 인용한다. "물리 실현" 열이 본 문서 확정분, "실재 여부" 열이 물리 실재 / 규약 실현(형태 A) / 형태 B 구분이다(§10 실측 대조).

| # | 01 §3 계약 요소 (정본 §) | 01 §4.1 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| E1 | 진입 트리거 (Entry Descriptor `trigger` — §3.1·§3.2-A) | "진입 트리거의 물리 형태 … 그 물리 발화 형태(어떤 진입 명령·선택·추론으로 Entry가 발화되는가)는 Adapter가 바인딩한다. Core Contract는 논리 name·trigger만 소유한다." | 논리 Entry `/new`·`/continue`(01 §3.1·§0 논리 식별자)의 물리 발화 형태 = `.claude/commands/uaf-new.md`·`uaf-continue.md` **문서 명령**(§3). | 물리 실재: 명령 파일 2개. 형태 A: 엔진 5단계 = 규약 절차. 형태 B: `entry_resolve.py`(결정적 실행 로더·LLM 0) — 명령이 이 로더를 호출해 해소 결과를 수령. |
| E2 | Workspace Evidence 관측 (Evidence Source capability·유/무 값 도메인 — §3.2-C) | "Workspace Evidence 관측의 물리 실현 … contract-presence·repository-presence를 실제 환경에서 어떻게 탐지하는가(경로 관례·직렬화 형식·존재 판정 수단)는 Adapter 소관이다. Core Contract는 capability 선언과 유/무 값 도메인만 소유한다." | §4.0 사용자 주입 폴더 + 신규/기존 의도로 관측 로커스 확정(구 ambient 자동 스캔 대체). contract-presence = 주입 폴더로 스코프한 Contract 저장 위치의 인스턴스 파일 유무 실측(§4.1). repository-presence = 사용자 신규/기존 선언 + 확인 관측(§4.2). Entry는 유/무만 관측(EN-INV 2). | 형태 A: 판정 수단·실제 관측 = 정본 문면·규약 절차. 형태 B: `entry_resolve.py`가 §4 판정 수단을 파일시스템 실측으로 실행(순수 판독·유/무만·내용 파싱 0), 경로·직교 관측 규칙은 `entry-registry.json` observation 데이터로 소비(§4.4). |
| E3 | Discovery Request 산출 (§3.2-B 매핑·§3.2-E mode 네임스페이스) | "Discovery Request 직렬화. {mode, inputs, policy}의 물리 직렬화·전달 방식은 Adapter 소관이다." | {mode, inputs, policy} = 자기서술 **구조화 레코드**로 직렬화(§5.1)·전달(§5.2). ARCHITECTURE §12.2·01 §3.2-B 추상 정합·재정의 0. | 형태 A: 형식·전달 방식 = 정본 문면. 형태 B: `entry_resolve.py`가 구조화 JSON(stdout) 방출 — matchedRow·gate(= `policy.ref == user-confirmation-gate` 투영·별도 판정 아님)는 엔진 메타로 병기(Discovery Request 자체 아님). 기록 백엔드 트리 위치는 본 문서 밖. |

- 위 3행이 01 "### §4.1 바인딩 대상" 표의 불릿 3건이다. 각 행의 물리 실현은 정본 표현을 이 환경의 구체 형태·수단·형식으로 좁힌 것이며 새 바인딩 계약을 창설하지 않는다.
- 01 §4.1 표에 없는 계약 요소(§3.2-A~E·§3.3)는 이식 시에도 유지되는 것이며 본 문서가 바인딩하지 않는다(§8). 진위 판정 기준은 01 §3이다.

---

## §3. E1 — 진입 트리거 물리 형태 확정 (done 3)

01 §4.1 불릿 1의 물리 실현. 계약(01 §3.1 Entry 2종·§3.2-A `trigger`)은 § 포인터 인용이며 물리 발화 형태만 확정한다.

### §3.1 확정 — 두 진입 명령 문서

| 논리 Entry (01 §3.1 name) | 물리 발화 형태 (이 환경 확정) | 성격 |
|---|---|---|
| `/new` (순수 Greenfield 전용) | `.claude/commands/uaf-new.md` | 형태 A 문서 명령 — Entry Resolution 규약 절차를 정본 포인터로 안내. |
| `/continue` (Incremental/Brownfield) | `.claude/commands/uaf-continue.md` | 형태 A 문서 명령 — Entry Resolution 규약 절차를 정본 포인터로 안내. |

- **논리 식별자 주의(01 §0).** `/new`·`/continue`는 Entry의 **논리 식별자(name)**이며 물리 진입 형태는 Adapter 소관이다. 이 환경의 물리 발화 형태가 위 `uaf-` 접두 명령임을 본 문서가 확정한다(`uaf-` = UAF 네임스페이스 표면화 + 환경 빌트인 명령 충돌 회피).

### §3.2 골격 준거·확정 근거

- **골격 준거.** 두 명령은 `.claude/commands/uahf-status.md` 선례와 동형이다 — YAML front-matter(`description:`)·형태 A(실행 코드 0)·**정본 포인터 전용**(값 하드코딩 0).
- **재정의 0.** 두 명령은 안내 포인터만 담는다 — Entry Resolution 규약 절차(엔진 5단계·결정 테이블 대조)와 사용자 개입 지점(Preserve Human Authority 게이트)을 정본 § 포인터로 가리킨다: `uaf-new.md` → `/new` 결정 행(01 §3.2-D 행 1~4)·D3 ①, `uaf-continue.md` → 행 5~8·D3 ②③.
- **엔진 실현.** 엔진 고정 5단계(01 §3.2-A)는 형태 B 로더 `entry_resolve.py` 호출로 실현되며, 로더 미가용 시 주 세션이 규약 절차로 실수행한다(형태 A 폴백). 어느 경로든 판별 결과·01 §3 계약은 동일하다.

---

## §4. E2 — Workspace Evidence 관측 물리 실현 (done 4)

01 §4.1 불릿 2의 물리 실현. **capability 선언과 유/무 값 도메인은 01 §3.2-C 소유**(재정의 0)이며 본 문서는 **존재 판정 수단(탐지 절차)**만 확정한다. Entry는 유/무만 관측하고 증거를 수집·해석하지 않는다(01 §3.2-A 2단계·EN-INV 1·2).

### §4.0 Workspace-target 주입 — 관측 로커스 확정 (하이브리드)

- **주입 입력(물리 addressing).** 진입 시 사용자가 **대상 폴더(경로/폴더명) + 신규/기존 의도**를 주입하며, 이 주입이 §4.1·§4.2 관측의 *위치와 방식*을 확정한다. 구 암묵적 ambient 스캔(워크스페이스 자동 탐색)을 **대체**한다 — 주 세션은 자동 탐색하지 않고 주입된 폴더로 관측을 스코프한다.
- **논리 입력 불변(재정의 0).** 주입은 01 §3.2-C Workspace Evidence를 재정의하지 않는다 — Evidence를 *어디서·어떻게* 관측할지의 물리 addressing일 뿐이다. 논리 입력·유/무 값 도메인·결정 테이블 8조합·mode 매핑은 무변경이다(EN-INV 3).
- **폴더 생성 의미 없음(EN-INV 1).** 주입된 "신규 폴더명"은 **의도의 기록**일 뿐이다 — Entry는 폴더를 생성·scaffold하지 않으며 실제 생성·초기화는 하류 Discovery 소관이다.
- **의도 분기.** "신규 폴더명" 주입 → repository-presence = **무**로 기대하고 그 폴더의 부재·빈/맨 초기화 상태를 *확인*만 한다(자동 탐색 아님)·contract-presence도 그 폴더 기준 무. "기존 폴더" 주입 → repository-presence 기대값 **유**이며 그 폴더로 스코프를 좁혀 contract-presence를 스캔한다(§4.3·§6).

### §4.1 contract-presence — 존재 판정 수단 (contract-binding §4.1 위임 해소)

- **capability(정본 소유).** "워크스페이스에 Project Contract가 존재하는가". 값 도메인 = 유/무(01 §3.2-C).
- **저장 위치(선행 확정 — contract-binding §3·§4).** Contract 인스턴스 = `project-contract.v<N>.md`(Markdown 본문 + YAML front-matter). 저장 위치 이원화 — 일반 관례 = 소비 프로젝트 내 `.claude/project-contract/`, 본 UAF 저장소 인스턴스 = `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`.
- **존재 판정 수단(본 문서 확정 — 탐지 절차·§4.0 주입 스코프).** contract-presence의 유/무는 주입된 대상 폴더로 **스코프를 좁혀** 그 폴더의 Contract 저장 위치에 **인스턴스 파일(`project-contract.v<N>.md`)이 하나라도 존재하는지**의 실측으로 판정한다(구 ambient 전역 스캔 아님).
  - **기존 의도 주입 시** — 주입 폴더의 Contract 저장 위치(소비 프로젝트: `<주입 폴더>/.claude/project-contract/`; 본 저장소 dogfooding: `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`)에 인스턴스 파일이 하나 이상이면 **유**, 없으면 **무**(디렉터리 부재 포함). 이 유/무가 incremental(유) vs brownfield(무·repo 유)를 가른다.
  - **신규 의도 주입 시** — 주입 폴더는 부재/빈 상태 확인으로 인스턴스가 없으므로 **무**.
- **관측 한계(EN-INV 2).** Entry는 파일 **유무만** 관측한다 — front-matter·본문을 파싱·해석·생성하지 않는다. 내용 해석·최신 인스턴스 해소(`instanceVersion`·`supersedes`)는 하류 소비 소관이다. 이로써 contract-binding §4.1이 미룬 존재 판정 수단이 해소된다.

### §4.2 repository-presence — 존재 판정 수단 (사용자 신규/기존 선언 기반)

- **capability(정본 소유).** "워크스페이스에 Repository가 존재하는가". 값 도메인 = 유/무(01 §3.2-C).
- **판정 수단의 정본 근거.** 01 §3.2-D 판별 규칙 **D3 ②**는 이 Evidence의 결과를 "기존 저장소가 있으나 아직 Contract가 없는 최초 도입"의 Brownfield Full Discovery로 규정한다(행 6). 즉 "Repository 존재" = **이어갈 기존 프로젝트 본체가 실재하는가**다(ARCHITECTURE.md §2.2·01 §3.1 `/continue` Brownfield). 본 문서는 그 정본 의미에 정합하는 물리 판정 수단만 확정한다.
- **존재 판정 수단(본 문서 확정 — §4.0 주입이 로커스·기대값 설정).** 사용자 신규/기존 선언이 관측 로커스와 기대값을 설정하고, 유/무는 에이전트가 그 폴더 상태를 **확인 관측**한 결과로 확정된다(구 ambient 콘텐츠 휴리스틱 대체). **선언은 관측을 대체하지 않는다** — 확정은 확인 관측이며(01 §3.2-A 2단계 "관측만"), 선언과 확인 관측이 상충하면 아래 충돌 처리 note로 라우팅된다.
  - **"신규 폴더명" 선언(기대값 무)** → 폴더의 부재/빈·맨 초기화 상태(이어갈 콘텐츠 없음) 확인 관측 시 **무**.
  - **"기존 폴더" 선언(기대값 유)** → 그 폴더에 이어갈 실질 프로젝트 콘텐츠(소스·문서·설정 등 빈/맨 초기화를 넘는 본체) 실재 확인 관측 시 **유**.
- **D3 ② Brownfield 정합.** "기존 폴더" 선언(repo 유)이면서 Contract 인스턴스가 없으면(§4.1 무) 결정 테이블 행 6(Brownfield Full Discovery)으로 정합한다. Entry는 유/무만 관측한다(EN-INV 2).
- **관측 한계.** Entry는 콘텐츠의 **유무만** 관측하며 내용을 수집·해석하지 않는다(EN-INV 1). 기존 콘텐츠의 실제 이해·분석은 하류 Project Discovery 소관이다.

**충돌 처리 note — 선언 ↔ 실제 상태 상충은 canonical 결정 테이블 policy에 포섭 (EN-INV 6).** §4.0 주입 선언과 실제 폴더 상태가 상충할 수 있다 — 예: "신규" 선언인데 주입 폴더에 실질 콘텐츠 존재 / "기존" 선언인데 주입 폴더가 부재·빈 상태. 이 충돌은 **별도 신호가 아니라 확인 관측이 해소되는 canonical 결정 테이블 행의 policy로 구동**된다(Policy as Data 단일 소스) — "신규인데 콘텐츠"는 확인 관측이 **행 2·4**로 해소되어 그 canonical policy(repository-present/contract-present)가 이미 사용자 확인 게이트이고, "기존인데 이어갈 실체 전무(Contract 무·Repo 무)"는 **행 5**(nothing-to-continue)로 해소된다. **단 Contract가 존재하면(행 7·8) repo 유무와 무관하게 incremental·게이트 없음이다**(D3 ③ — Contract 자체가 이어갈 대상; "기존 선언인데 repo 무"라도 거짓 게이트를 만들지 않는다). Entry는 관측값을 **임의로 덮어쓰지 않으며**(01 §3.2-D 충돌 처리·EN-INV 6), 게이트를 canonical policy로 표면화만 하고 확정 결정을 내리지 않는다(ARCHITECTURE.md §8 UAF-INV ⑤). **병행 imperative conflict 판정을 두지 않는다**(행 7 거짓 게이트 정정·CP2 — 정정 경위 = git 앵커 90ca19c). 충돌 해소 과정에서도 Entry는 폴더를 생성·scaffold하지 않는다(EN-INV 1).

### §4.3 관측 결과의 소비

관측된 두 Evidence의 유/무는 엔진 3단계(우선순위 평가, 01 §3.2-A)에서 명시 Entry의 결정 행(§3.2-D)에 대조되며, Discovery Request의 `inputs`(Evidence 참조 목록, §5·01 §3.2-B)에 확정 참조로 담긴다.

### §4.4 형태 B 실현 — 판정 수단의 실행 코드화 (가법·재정의 0)

§4.0~§4.3의 판정 수단 정본 문면은 그대로 유지되며, 아래는 그 form-B 실현 경로다.

- **실현 산출물.** `entry/adapters/claude/entry_resolve.py`(결정적 실행 로더·LLM 0·순수 판독)가 §4 판정 수단을 실행한다. 경로 관례·직교 관측 규칙은 코드에 하드코딩하지 않고 `entry-registry.json`의 `observation` 데이터로 소비한다(Policy as Data).
- **contract-presence(§4.1 실현).** `observation.contractLocations`(주입 폴더 기준 상대 glob — `.claude/project-contract/project-contract.v*.md` 및 dogfooding `.../discovery-data/contracts/*/project-contract.v*.md`)에 인스턴스 파일이 하나라도 실재하면 유, 없으면 무. **파일 유무만 실측하며 front-matter·본문을 파싱하지 않는다**(EN-INV 2).
- **repository-presence(§4.2 실현).** 주입 폴더에 '이어갈 실질 프로젝트 본체' 파일이 하나라도 실재하면 유, 부재/빈/맨 초기화면 무. **Contract 저장 위치·`.git/`·OS 메타데이터는 본체에서 제외**(`observation.repositoryBody.excludePrefixes`·`ignoreBasenames`)해 두 축을 직교로 유지한다(D3 ② '프로젝트 본체' 의미·01 §3.2-C 2축 독립). 엣지 임계값(단일 README 등)은 Adapter 재량이며 상충 시 사용자 확인 게이트로 라우팅된다(§11 OQ-TE-1).
- **게이트 = canonical 결정 테이블 policy(별도 conflict 신호 아님·§4.2 note 실현).** 게이트는 매칭 행의 **`policy.ref == user-confirmation-gate`**(canonical 결정 테이블 행 2·3·4·5·정본 = 01 §3.2-D)로만 구동되며, 게이트 이유는 그 행의 `policy.conflict`(repository-present/contract-present/nothing-to-continue)에 있다. 로더는 이 값을 방출 필드 `gate`(policy.ref 의 투영)로 표면화만 하고 확정 결정을 내리지 않는다(게이트 제시는 주 세션 소관·EN-INV 6). **하이브리드 선언↔상태 충돌(§4.2 note)은 별도 imperative 판정이 아니라 이 canonical policy에 포섭된다** — "신규인데 콘텐츠 존재"=행 2·4, "기존인데 이어갈 실체 전무"=행 5. **Contract 존재 시(행 7·8)는 D3 ③에 따라 incremental·게이트 없음**이다(거짓 게이트 방지). 병행 imperative conflict 판정을 두지 않는다(Policy as Data 단일 소스).
- **불변.** 로더는 폴더를 생성·scaffold 하지 않으며(순수 판독·EN-INV 1), 결정 테이블·mode 매핑·게이트를 재정의하지 않는다(전부 `entry-registry.json` 데이터·정본 = 01 §3.2-D). 형태 A(규약 절차)는 폴백으로 유지된다.

---

## §5. E3 — Discovery Request 직렬화·전달 확정 (done 5)

01 §4.1 불릿 3의 물리 실현. Discovery Request 추상(ARCHITECTURE.md §12.2)·매핑 채움 규칙(01 §3.2-B)·mode 네임스페이스(01 §3.2-E)는 § 포인터 인용이며 물리 직렬화 형식·전달 방식만 확정한다.

### §5.1 확정 — 자기서술 구조화 레코드

**Discovery Request 1건 = {mode, inputs, policy} 3요소를 담는 자기서술 구조화 레코드**로 직렬화한다. 자매 바인딩의 구조화 데이터 관례와 동형이며 구체 형식은 Adapter 선택이다(격리 지점 — 이식 교체 §8).

논리 골격 예시(3요소만 표현하며 새 계약 요소를 창설하지 않는다):

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

- **§12.2 정합(재정의 0).** `mode` = modeMapping 적용 값(확장 네임스페이스), `inputs` = 관측된 Workspace Evidence의 확정 참조 목록(미완성·동시 작성 산출물 비참조), `policy` = Discovery Policy 참조 — 세 요소가 ARCHITECTURE §12.2·01 §3.2-B와 1:1 정합한다(EN-INV 5). Discovery Request는 Contract 자체를 담지 않고 Discovery 내부 개념(질문·전략)을 담지 않는다.

### §5.2 전달 방식

- **형태 A(Bootstrap).** 규약 절차(주 세션)가 5단계 방출(01 §3.2-A)에서 위 레코드를 산출해 하류 Project Discovery 소비자에게 전달한다(요소 간 인터페이스의 구조화 레코드 이관).
- **형태 B.** 직렬화기·로더 `entry_resolve.py`가 같은 레코드 형식을 구조화 JSON(stdout)으로 방출하고, matchedRow·gate(= canonical `policy.ref == user-confirmation-gate` 투영·별도 판정 아님)를 엔진 메타로 병기한다(엔진 메타는 Discovery Request 자체가 아니다 — §5.1 3요소만이 Discovery Request다). 도입에도 §12.2·01 §3.2-B 계약 변경은 0이다(structure.md §7 C-1).

### §5.3 경계 분담 — 백엔드 트리 위치 확정 위임

- **본 문서 소유** = 직렬화 형식(§5.1)·전달 방식(§5.2).
- **후속 위임** = 물리 기록이 놓일 백엔드 트리(`uahf/framework/adapters/claude/discovery-data/` 하위 Discovery Request 기록 구조)의 물리 위치는 2차 산출물 디커플링 트랙 소관이다. 본 문서가 트리 구조·물리 위치를 창설하면 그 트랙의 소관을 선취하므로 여기서 멈춘다.

---

## §6. 결정 테이블 실동작 예시 (done 6 — 행 1·행 6)

01 §3.2-D 결정 테이블을 재정의하지 않고 행을 인용해, 물리 관측(§4) → 단일 Discovery Request 산출(§5)을 두 행에 대해 예시한다. 각 조합이 정확히 한 결과로 해소됨(결정성·EN-INV 3)을 보인다. 엔진 5단계 = 매칭 → 증거 수집(관측) → 우선순위 평가(결정 행 대조) → 결정성 검증(단일 행) → 방출(01 §3.2-A).

| 예 | 시나리오 (명시 Entry·주입) | 관측 (§4.0 스코프) | 매칭 행 | 방출 Discovery Request (§5.1) |
|---|---|---|---|---|
| A | `/new`(물리 발화 `uaf-new`) · **신규 폴더명 주입**(예: `./my-product`) | repository-presence **무**(폴더 부재/빈 확인·§4.2) · contract-presence **무**(그 폴더에 인스턴스 없음·§4.1). UAF 저장소 ambient 스캔 개입 0. | 01 §3.2-D **행 1**(단일 매칭) | `{ mode: greenfield, inputs: [contract-presence(무), repository-presence(무)], policy: 기본 정책 참조 }` — Greenfield 정상 경로(근거 P-C). |
| B | `/continue`(물리 발화 `uaf-continue`) · **기존 폴더 주입**(기존 프로젝트 콘텐츠는 실재하나 그 폴더의 Contract 저장 위치에 인스턴스가 없는 폴더) | repository-presence **유**(실질 프로젝트 콘텐츠 실재 확인·§4.2) · contract-presence **무**(주입 폴더로 스코프한 Contract 저장 위치에 인스턴스 없음·§4.1) | 01 §3.2-D **행 6**(단일 매칭·판별 규칙 **D3 ②**) | `{ mode: brownfield, inputs: [contract-presence(무), repository-presence(유)], policy: 기본 정책 참조 }` — Brownfield Full Discovery·최초 Contract 생성 요청. |

- Entry는 두 예 모두 여기서 멈춘다 — Discovery 수행·Contract 생성은 하지 않는다(EN-INV 1·2).
- **예 B가 §4.0 주입 방식의 필요성을 보인다.** 구 ambient 자동 스캔은 방대한 기존 콘텐츠·비표준 Contract 저장 위치를 가진 워크스페이스에서 "이 저장소를 이어갈지 vs 하위 새 폴더에서 시작할지"의 사용자 의도를 분간하지 못하나, "기존 폴더" 주입 선언으로 repository-presence = 유가 확정되어 행 6으로 결정적으로 해소된다.

---

## §8. 01 §4.2 이식 교체 지점 대응 (done 8)

"교체되는 것"이 이 환경 바인딩이고, "유지되는 것"은 01 §3 Core Contract(이식 불변·structure.md §7 C-1 동형)이므로 정본 § 포인터로만 가리킨다.

| 01 §4.2 교체 지점 (바뀌는 것) | 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 §) |
|---|---|---|---|
| 진입 트리거의 물리 형태 | §2 E1, §3 | `.claude/commands/uaf-new.md`·`uaf-continue.md` 문서 명령. | 01 §3.1·§3.2-A |
| Evidence 관측의 물리 수단 | §2 E2, §4 | **§4.0 사용자 주입 폴더로 스코프한 유/무 관측** — contract-presence = 인스턴스 파일(`project-contract.v<N>.md`) 유무 실측 · repository-presence = 신규/기존 선언 + 확인 관측. 구 ambient 자동 스캔 대체. | 01 §3.2-C |
| Discovery Request의 직렬화 | §2 E3, §5 | {mode, inputs, policy} 자기서술 구조화 레코드 직렬화·전달. | 01 §3.2-B·§3.2-E, ARCHITECTURE §12.2 |

- 본 문서는 01 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고 물리 실현 매핑에 한정한다(§0).

---

## §10. 상태 서술 실측 대조 (L-07)

물리 생성물 = 진입 명령 파일 2개(`.claude/commands/uaf-new.md`·`uaf-continue.md`) + 형태 B 산출물 2개(`entry/adapters/claude/entry_resolve.py`·`entry-registry.json`) + 결정적 테스트(`entry/adapters/claude/tests/`). §3~§5가 확정한 것은 정본 문면(형태 A)이고 §4.4·§5.2가 그 form-B 실현 경로이며 01 §3 계약 변경은 0이다. Discovery Request 기록의 백엔드 데이터 트리는 `uahf/framework/adapters/claude/discovery-data/`이며 그 물리 위치 확정은 2차 산출물 디커플링 트랙 소관이다(로더는 stdout 방출까지이며 백엔드 기록 위치를 창설하지 않는다). form-B 산출물의 실재·동작은 8조합 실행(행 1~8 각 단일 결과·mode·게이트 = canonical policy)과 행 7(contract 유·repo 무 → incremental·게이트 없음) 거짓 게이트 부재 회귀로 확인되었다. "실재/미존재" 주장은 파일 시스템 직접 실측 후에만 기입한다.

`uaf-verified:` 위 물리 생성물 실재 = `entry/adapters/claude/` 및 `.claude/commands/` 디렉터리 목록 실측(2026-07-26). 검색 범위 = 두 디렉터리의 직접 항목이며 하위 내용 정독은 아니다.

---

## §11. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 모든 매핑은 01 §3·§4의 물리 실현이다. Descriptor 필드·엔진 단계·결정 테이블 행·Evidence Source 선언·mode 네임스페이스·EN-INV 1~6의 진위는 이 문서에서 새로 확정되지 않는다 — 판정 기준은 01 §3이다.
- **본 문서 소유·확정분** = 01 §4.1이 미룬 3불릿(E1 §3 · E2 §4 · E3 §5)뿐이며, 그 안에서 contract-binding §4.1이 미룬 contract-presence 존재 판정 수단이 §4.1에서 해소된다. Discovery Request 기록 백엔드 트리 위치는 2차 산출물 디커플링 트랙에 위임한다.
- **격리 토큰의 단일 자리.** 구체 명령 이름·물리 경로·구조화 데이터 형식·파일 확장자는 이 Adapter 경계 문서에 둔다(structure.md §5 C-3 비적용 — 격리 보유).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-TE-1 (신규/기존 확인 시 "빈/맨 초기화 vs 실질 콘텐츠" 임계값 — 비차단).** 확인 단계 엣지(예: 단일 README·숨김 설정만 있는 폴더를 "신규"로 선언)의 정밀 임계값은 Adapter 재량이며 상충 시 §4.2 충돌 처리 note의 사용자 확인 게이트(EN-INV 6)로 라우팅된다. 01 §3.2-C capability·값 도메인 변경이 아니므로 비차단.
- **OQ-TE-2 (Discovery Request 기록 백엔드 트리 물리 위치 — 후속 트랙·비차단).** §5.3에서 2차 산출물 디커플링 트랙에 위임했다. ARCHITECTURE §12.2·01 §3.2-B 계약 변경이 아니므로 비차단. (기록 위치 자체는 discovery-binding.md §4.2가 이미 확정했다.)

---

## §13. 개정 이력

- **2026-07-26 (정합) md 슬림화 Wave 4** — 비계약 격리 개정: 메타 템플릿·해소 OQ·경위 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c. Advisor 위임.
