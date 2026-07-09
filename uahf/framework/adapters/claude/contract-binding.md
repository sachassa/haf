# framework/adapters/claude/contract-binding — Claude Code Project Contract Adapter 바인딩

작성일: 2026-07-07
상태: v1.2 Baseline (CP2 첫 판정 Pass 16/0/0 · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: AGENT.md
근거 정본:

- planning/specs/03-project-contract.md §3.1(지위·논리 스키마·입출력)·§3.2-A(필드 그룹 9종)·§3.2-B(필수 코어 필드)·§3.2-C(Dimension→필드 매핑 — 컴파일 방향)·§3.2-D(Provenance 불투명 부속)·§3.3(버저닝 A~E)·§3.4(인스턴스 거버넌스)·§3.5(UAHF Interface)·§3.6(PC-INV 1~12) — 본 문서가 물리 실현으로 바인딩하는 계약의 정본. **재정의·확장하지 않고 § 포인터로만 인용한다.**
- planning/specs/03-project-contract.md §4.1(### 4.1 바인딩 대상 — 표 4행)·§4.2(### 4.2 이식 교체 지점). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표와, 대응을 명시하는 교체 지점의 정본.
- framework/adapters/claude/memory-binding.md — 자매 Adapter Binding 문서(골격 선례). 제목 라인 → 작성일·상태·상위 규약·근거 정본 → 거버넌스 문단 → §9 이력(머리 배치) → §0 정본 경계 → §1 목적 → 바인딩 표 물리 실현(실재/규약 실현/형태 B 3구분) → 물리 절차/매핑 절 → 이식 교체 지점 표("유지되는 것" 열 = C-1 재확인) → 실측 대조 절 → 요약의 관례, 그리고 append-only 새 파일 갱신·"지원 구조 — 시연 시 생성" 정직 구분(L-07)의 선행 관례.
- framework/adapters/claude/scaffold-binding.md §4 — 자매 바인딩. "Markdown 본문 + front-matter" 프로젝트 배치 문서 직렬화의 선행 관례.
- framework/core/structure.md §2(4경계 배치 — `framework/adapters/<adapter>/` = 환경 의존 격리 경계)·§5(금지 토큰 규칙 C-3 — Adapter 경계는 격리 보유로 비적용). 본 문서 경계·물리 분리·격리 토큰 허용의 근거.
- ARCHITECTURE.md §7(사용자 고정 원칙 P1~P5·§7.1 상시 불변 확인 2건)·§8(UAF-INV ①~⑥ — 특히 ① UAHF 정본 무수정·유일 접점, ② Discovery 교체 가능·Contract 교체 불가, ③ Strategy Invariance). 근거 인용용(재정의 0).
- entry/specs/01-entry.md §4.1(### §4.1 바인딩 대상, 불릿 2 — "contract-presence·repository-presence를 실제 환경에서 어떻게 탐지하는가(**경로 관례·직렬화 형식·존재 판정 수단**)는 Adapter 소관이다. Core Contract는 capability 선언과 유/무 값 도메인만 소유한다")·§3.2-C(Workspace Evidence & Evidence Source 확장 스키마 — contract-presence Evidence 정의·유/무 값 도메인 소유)·EN-INV 2. 본 문서 §3·§4가 §4.1이 Adapter 소관으로 미룬 물리 실현임의 근거.
- specs/12-scaffold.md §3.2-A(Project Template) — Contract가 신규 프로젝트 설치 시 배치되는 정본 문서로 성립하는 소비 지점(03 §3.5-B (b))의 근거. § 포인터로만 참조.
- specs/00-glossary.md — UAHF 용어 정본. 본 문서는 새 용어를 신설하지 않는다. `형태 A/B`는 structure.md §4의 서술 라벨 인용이며 Glossary 표제어가 아니다.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core·UAF 계약을 특정 실행 환경·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 직렬화 형식·물리 경로·환경 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, 자매 memory-binding.md §0·scaffold-binding.md §0과 동형). 단 이 문서는 UAF 정본(planning/specs/03-project-contract.md §3·§4)과 UAHF 정본을 **재정의하지 않는다** — 계약(필드 그룹·코어 필드·버저닝·불변)은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-07 | v1.2 Draft | 최초 작성. `framework/adapters/claude/` 경계의 **UAF 정본(uaf/specs/03) 바인딩** 산출물(자매 바인딩 관례 동형·접두 없음). 03 "### 4.1 바인딩 대상" 표 **4행 전건**을 Claude 환경 물리 실현으로 확정(§2 — 실재/규약 실현/형태 B 3구분). ⓐ Contract 직렬화 = **Markdown 본문 + YAML front-matter 단일 문서**로 확정(§3 — 9그룹·필수 코어 필드 10 표현·tolerant reader 정합·Provenance 분리 컨테이너·append-only 표현 요건 충족 문면). ⓑ 저장 위치 이원화 확정(§4 — 일반 관례 `.claude/project-contract/`·본 저장소 인스턴스 `framework/adapters/claude/discovery-data/contracts/uahf/`, DP-X2, 01-entry §3.2-C 물리 실현). ⓒ `schemaVersion`(SemVer 점표기 문자열)·`instanceVersion`(단조 증가 정수) 표기 형식 확정(§5 — MAJOR 원칙 금지·필드 제거 금지·deprecated 마킹 물리 훼손 0, PC-INV 4·5·6). ⓓ Provenance 불투명 컨테이너 외형·must-ignore 경계만 확정, 내부 형식은 후속 discovery-binding.md(예정) 위임(§6, DP-X6, 03 §3.2-D 동형). 상시 불변 자기 점검(§7 — 코어 필드 직렬화에 Discovery 내부 개념 0·다중 패턴 자가 스캔·Stable Contract 규율 훼손 0). 03 "### 4.2" 이식 교체 지점 대응 표(§8 — "유지되는 것" 열 = 03 §3 불변 재확인). 상태 서술 실측 대조(§10 — discovery-data/ 현 시점 미존재·v1.2 E2E Task 생성 예정 정직 구분, L-07). 실행 코드 0(형태 A, D-v1.2-1). 03 §3·§4·UAHF 정본 재정의 0·§ 포인터 인용만·새 계약 요소(필드·연산·불변·kind) 창설 0·특정 방법론 고유명 0. 동시 작성 중인 병렬 산출물 불인용(07 R2). | Worker (Advisor 위임, Task T-C) |
| 2026-07-07 | v1.2 Draft (r2 — § 라벨 오귀속 정정) | **Advisor 게이트 C 검출 결함 1건 교정** (T1 r2 동형 부류). **결함 요지:** "contract-presence 탐지의 경로 관례·직렬화 형식·존재 판정 수단은 Adapter 소관" 위임 문구를 **01-entry §3.2-C에 오귀속**했으나, 실측 대조 결과 이 위임 문구의 실제 소유 절은 **01-entry §4.1(### §4.1 바인딩 대상, 불릿 2)**이다 — §3.2-C는 Evidence Source 등록 스키마(sourceType·capability·valueDomain)·v1.1 Evidence 2종(contract-presence·repository-presence, 유/무 값 도메인)만 소유하며 Adapter 위임 문구를 담지 않는다. 라이브 본문 오귀속 지점의 원인 = §4.1 불릿 말미 교차 참조 "(§3.2-C)"를 소속 절로 오독. **교정 내용:** 라이브 본문 6지점(근거 정본 01-entry 불릿·§2 표 행2·§4 도입 문단·§4.1 근거 문단·§11 OQ-TC-2·§12 요약)에서 위임 귀속을 §4.1로 정정하고 §3.2-C는 "contract-presence Evidence 관측 정의·유/무 값 도메인 소유"로만 인용. **동종 결함 전수 재대조(BP-01):** 본문·근거 정본 목록의 전 외부 정본 § 귀속(01-entry·03·specs/12·structure.md·uaf/ARCHITECTURE·Glossary·02·07·02-discovery)을 대상 정본 파일 직접 실측 재대조 — 그 외 동종 결함 0건. r1 이력 행 문면 불변(L-10 — 이력 행은 시점 기록, 재대조 대상 제외). 산출물 1개 파일만 수정, 다른 파일 무수정. | Worker (Advisor 게이트 C 재작업 지시, Task T-C r2) |
| 2026-07-07 | v1.2 Baseline | v1.2 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass 16/0/0; CP3 Advisor 승인) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, 자매 memory-binding.md §9·framework/core/structure.md §9 동형. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **UAF 정본 바인딩 선언(DP-X1).** 이 문서는 `framework/adapters/claude/` 경계의 Adapter Binding 문서이되, 그 **바인딩 대상 정본은 UAHF spec이 아니라 UAF 정본 `planning/specs/03-project-contract.md` §3·§4다.** 자매 바인딩 12문서(runtime·memory·verifier·loop·workflow·hooks·skills·plugins·agent·scaffold·harness-binding + adapter-conformance)가 UAHF spec(specs/01~13)을 바인딩하는 것과 달리, 본 문서는 UAF 레벨의 Project Contract 정본을 바인딩한다. 파일명·골격 관례는 자매와 동형이다(접두 없음).

- **정본은 planning/specs/03 §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소 — 필드 그룹 9종(§3.2-A)·필수 코어 필드(§3.2-B)·Dimension 매핑(§3.2-C)·버저닝 규율(§3.3)·인스턴스 거버넌스(§3.4)·UAHF Interface(§3.5)·불변 PC-INV 1~12(§3.6) — 를 **재정의·확장하지 않는다.** 계약 요소는 정본 § 포인터로만 인용한다. 본 문서가 확정하는 것은 03 §4.1이 "Adapter 소관"으로 미룬 **직렬화 형식·저장 위치·버전 표기·Provenance 물리 형식** 넷뿐이다(§2).

- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장). UAF 정본(planning/specs/03) 본문도 같은 AI 비의존이다(03 §3 도입·PC-INV 12). 이 문서는 그 **반대편**이다 — 구체 직렬화 형식(문서형·구조화 데이터 형식명)·물리 경로(`framework/adapters/claude/…`·`.claude/…`)·파일 확장자의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(memory-binding.md §0·scaffold-binding.md §0과 동형). 단 **UAF 정본이 명명하지 않은 것을 UAF 정본 문면인 것처럼 서술하지 않는다** — 물리 확정은 전부 본 문서 소유임을 명시한다.

- **하네스 Bootstrap 전제(형태 A, D-v1.2-1).** 이 하네스는 현재 Bootstrap 상태다(Glossary J-13, 자매 바인딩 §0). 본 문서의 바인딩은 **실행 코드 0**이다 — Contract를 컴파일·직렬화·소비하는 실행 코드는 도입되지 않았다. 따라서 매핑은 (i) 물리 실재 표면, (ii) 규약으로 확정된 정본 문면(형태 A — 경로·형식·표기 규격), (iii) 실행 코드 도입 시 로딩될 지점(형태 B — 컴파일러·tolerant reader 파서)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.

- **실측 기반 상태 서술(L-07).** "실재/미존재" 주장은 파일 시스템 확인 후에만 기입한다. 본 문서가 확정하는 물리 경로(`discovery-data/…`)의 데이터 자산은 **현 시점 미존재**이며, 그 생성은 v1.2 E2E Task(T-XG·T-XB) 소관이다 — 본 문서는 경로·구조·형식의 **정본 문면만** 소유한다(memory-binding.md §7 "지원 구조 — 시연 시 생성" 선례 동형). §10이 그 실측 대조 표다.

- **네임스페이스·용어.** 본 문서가 확정하는 것은 물리 표기(직렬화 형식·경로·버전 값 형태·라벨)뿐이며, 03이 소유하는 스키마 용어(`schemaVersion`·`instanceVersion`·`supersedes`·tolerant reader·opaque annex 등)는 03 정의를 § 포인터로 참조하고 재정의하지 않는다. 새 UAHF 용어·새 계약 요소(필드·연산·불변·kind)를 신설하지 않는다.

---

## §1. 목적

이 문서는 planning/specs/03 "### 4.1 바인딩 대상" 표 4행을 이 환경 위에 **v1.2 시점의 구체 물리 실현**으로 매핑한다. Contract는 UAF↔UAHF 유일 접점·Stable Contract(Public API, 03 §3.1-A)이므로, 이 문서가 확정하는 물리 인터페이스는 v1.2 후속 작업의 **선행 확정 인터페이스**다.

책임은 넷이다.

- 03 §4.1 바인딩 표 **4행 전부**(① 직렬화·물리 포맷 ② 저장 위치 ③ `schemaVersion`·`instanceVersion` 표기 ④ Provenance 부속 물리 형식)를 물리 실현으로 확정한다(§2 — 실재/규약 실현/형태 B 3구분).
- Contract 인스턴스의 **직렬화 포맷**을 확정하고(§3), **저장 위치 관례**를 이원화 확정하며(§4), **버전 표기 형식**을 확정한다(§5). Provenance는 **불투명 컨테이너 외형·must-ignore 경계만** 확정하고 내부 형식은 후속 바인딩에 위임한다(§6).
- 코어 필드 직렬화에 Discovery 내부 개념이 0건임과 Stable Contract 규율이 훼손되지 않음을 **상시 불변 자기 점검**으로 보인다(§7, PC-INV 2·11).
- 03 §4.2 이식 교체 지점에 본 문서의 대응을 명시하고(§8, "유지되는 것" 열 = 03 §3 불변 재확인), 상태 서술을 실측과 대조한다(§10).

이 문서는 03 §3·§4·UAHF 정본의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A → 형태 B 전환 시에도 03 §3 계약 변경은 0이며(structure.md §7 C-1 동형), §8의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 03 §4.1 바인딩 표 4행 물리 실현 (done 3)

03 "### 4.1 바인딩 대상" 표의 **4행 전부**를 물리 표면으로 매핑한다. "03 §4.1 바인딩 지점" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 형식·경로·표기를, "실재 여부" 열이 Bootstrap 상태에서의 **물리 실재 / 규약 실현(형태 A) / 형태 B**를 정직하게 구분한다(§10 실측 대조).

| # | 03 §3 계약 요소 (정본 §) | 03 §4.1 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Contract 직렬화·물리 포맷 (§3.1·§3.2) | 논리 스키마를 실제 문서·레코드로 표현하는 직렬화 형식. | **Markdown 본문 + YAML front-matter 단일 문서.** front-matter가 9그룹·필수 코어 필드 10의 자기서술 구조를, 본문이 인간 가독 렌더링을 담는다. Provenance는 분리 네임스페이스 컨테이너. 상세 §3. | 형식 확정(정본, 규약 실현/형태 A). Contract 인스턴스 데이터 미존재 — v1.2 E2E Task 생성 예정. 컴파일러·파서는 형태 B. |
| 2 | Contract 저장 위치 (§3.2) | Contract 인스턴스가 프로젝트에 배치·보관되는 물리 위치·경로 관례. | **이원화 확정**: 일반 관례 = 소비 프로젝트 내 `.claude/project-contract/`; 본 UAHF 저장소 인스턴스(Brownfield dogfooding) = `framework/adapters/claude/discovery-data/contracts/uahf/`(격리). 상세 §4. 01-entry §4.1이 Adapter 소관으로 미룬 contract-presence 탐지 경로의 실현(§3.2-C는 contract-presence Evidence 관측 정의·유/무 도메인만 소유). | 경로 관례 확정(정본, 형태 A). `discovery-data/` 데이터 자산 미존재 — E2E Task 생성 예정(§10). |
| 3 | `schemaVersion`·`instanceVersion` 표기 형식 (§3.3·§3.4) | 버전 값의 물리 표기·직렬화. | front-matter 스칼라 — `schemaVersion` = SemVer 점표기 문자열(예 형태 `"1.0"`), `instanceVersion` = 단조 증가 정수, `supersedes` = 이전 인스턴스 참조. 상세 §5. | 표기 형식 확정(정본, 형태 A). 값 채움은 인스턴스 생성 시(E2E Task). |
| 4 | Provenance 부속 물리 형식 (§3.2-D) | 불투명 부속의 물리 저장 형식 — Discovery 측·Adapter 측 소관(내부 구조 비정의). | front-matter 내 **분리 네임스페이스 `provenance` 컨테이너**(불투명 블록) — 외형·must-ignore 경계만 본 문서가 확정. 내부 형식은 후속 discovery-binding.md(예정) 소관. 상세 §6. | 컨테이너 외형·경계 확정(정본, 형태 A). 내부 형식·데이터는 후속 바인딩·E2E Task 소관. |

주:

- 위 4행은 03 "### 4.1 바인딩 대상" 표의 전 행이다. 각 행의 "물리 실현"은 03 §4.1 정본 표현을 이 환경의 구체 형식·경로로 좁힌 것이며, **새 바인딩 계약을 창설하지 않는다**(§0). 특정 AI·모델·제품 기능·방법론은 여기서도 명명하지 않는다(03 §4.1 말미 동형) — 격리 대상은 직렬화 형식·물리 경로뿐이다.
- 03 §4.1 표에 없는 계약 요소(§3.1 지위·§3.2-A 필드 그룹·§3.2-B 필수 코어 필드·§3.2-C Dimension 매핑·§3.3 버저닝 규율·§3.4 인스턴스 거버넌스·§3.5 UAHF Interface·§3.6 불변)는 **이식 시에도 유지되는 것**이며, 본 문서가 바인딩하지 않는다(§8 "유지되는 것" 열). 이들의 진위 판정 기준은 03 §3이다.

---

## §3. Contract 직렬화 포맷 확정 (done 4)

03 §4.1 행 1("논리 스키마를 실제 문서·레코드로 표현하는 직렬화 형식")의 물리 실현을 확정한다. 계약(03 §3.2 논리 스키마)은 재정의하지 않고 § 포인터로 인용하며, 물리 직렬화만 확정한다.

### §3.1 확정 — Markdown 본문 + YAML front-matter 단일 문서

**Contract 인스턴스 1건 = Markdown 본문 + YAML front-matter 단일 문서 파일 1개**로 직렬화한다.

- **YAML front-matter** — 9 필드 그룹(03 §3.2-A)과 필수 코어 필드(03 §3.2-B)의 **기계 파싱 가능한 자기서술 구조**를 담는다. tolerant reader가 소비하는 표면이다.
- **Markdown 본문** — 같은 정의의 **인간 가독 렌더링**을 담는다. Advisor Consult 정독(03 §3.5-B (a))이 읽는 프로젝트 정의 정본 문서의 본문이다.

### §3.2 확정 근거 (rationale)

- **소비 형태 정합.** Contract는 03 §3.5-B에서 "프로젝트 정의의 정본 문서"로 두 지점에서 소비된다 — (a) Advisor가 착수 전 정독하는 Consult 대상 문서, (b) Scaffold가 프로젝트에 배치하는 정본 문서(specs/12-scaffold.md §3.2-A). 사람이 정독하는 정의 문서이므로 **인간 가독 문서형(Markdown)이 자연 정합**이며, 기계 소비를 위한 구조화 표면(front-matter)을 겸비한다. 자매 선례: scaffold-binding.md §4 Install Manifest = "Markdown 본문 + front-matter" 프로젝트 배치 문서. 동형 관례다.
- **격리 지점 허용.** 이 구체 직렬화 형식(문서형·구조화 데이터 형식)의 명명은 Adapter 경계에서 허용된다(C-3 비적용, §0). 이식 시 대상 환경 포맷으로 교체된다(§8).

### §3.3 03 §3.2 논리 스키마의 표현 요건 충족

본 직렬화가 다음 요건을 충족함을 문면으로 보인다.

- **ⓐ 9그룹·필수 코어 필드 10 표현 가능.** front-matter 중첩 key로 9 필드 그룹(03 §3.2-A: `meta`·`intent`·`requirements`·`constraints`·`risks`·`architectureDirection`·`assumptionLedger`·`readiness`·`provenance`)을 표현하고, 필수 코어 필드 **10**(03 §3.2-B: `id`·`schemaVersion`·`instanceVersion`·Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger)을 그 아래 key로 담는다. 각 필드의 충족 의미(03 §3.2-B)는 물리 표현에서 보존된다 — 예: `constraints`·`risks`는 명시적 공집합(빈 목록)도 충족으로 표현되고(03 §3.2-B), `architectureDirection`은 결정·미결을 담으며(미결의 명시도 충족), `assumptionLedger`는 구조 요소로 존재하되 `Ready`에서 빈 원장이 허용되고 `ReadyWithAssumptions`에서는 비어 있을 수 없다(03 §3.2-B).
- **ⓑ tolerant reader 정합(03 §3.3-C).** YAML front-matter는 미지 key를 오류 없이 무시 가능한 **자기서술 key-value/중첩 구조**다. UAHF tolerant reader는 필수 코어 필드 key에만 의존하고, 미지 필드·부속 네임스페이스(`provenance` 포함)는 must-ignore한다(03 §3.3-C, PC-INV 5). 이로써 Discovery 내부 변경이 만드는 선택 필드·부속은 tolerant reader에 도달하지 못한다(상시 불변 ②, §7).
- **ⓒ Provenance 분리 불투명 컨테이너.** Provenance는 front-matter 내 **분리 네임스페이스 `provenance` key**(불투명 블록)로 표현된다 — 코어 필드와 물리적으로 구분되고, tolerant reader가 must-ignore하는 경계에 놓인다(§6, 03 §3.2-D). 내부 구조는 본 문서가 정의하지 않는다.
- **ⓓ append-only 인스턴스 거버넌스 표현(03 §3.4).** 인스턴스 갱신은 **새 `instanceVersion` 문서 파일 추가**로 표현된다 — 기존 인스턴스 파일은 재작성하지 않으며(append-only·PC-INV 9), 새 파일의 `meta.supersedes`가 이전 인스턴스를 참조한다(§5). 이전 인스턴스는 계보로 보존된다. memory-binding.md의 append-only "기록된 파일 재작성 금지, 갱신은 새 파일 추가" 관례와 동형이다.

### §3.4 논리 골격 예시 (물리 front-matter 형태)

아래는 03 §8 예1(Ready Contract 논리 골격)의 물리 front-matter 렌더링 예시다. **9 그룹·필수 코어 필드만** 표현하며 새 계약 요소를 창설하지 않는다. 코어 필드 정의에 Discovery 내부 개념은 0건이다(§7).

```
---
meta:
  id: <인스턴스 논리 식별자>
  schemaVersion: "1.0"        # SemVer 점표기 문자열 (§5)
  instanceVersion: 1          # 단조 증가 정수 (§5)
  supersedes: null            # 이전 인스턴스 참조 (없으면 null)
intent: <프로젝트 의도 — 비어 있을 수 없음>
requirements:
  functional: [ ... ]         # 최소 기능 요구 포함
  quality: [ ... ]
constraints: [ ... ]          # 명시적 공집합(빈 목록)도 충족
risks: [ ... ]                # 명시적 공집합(빈 목록)도 충족
architectureDirection:
  decisions: [ ... ]
  open: [ ... ]               # 미결의 명시도 충족
assumptionLedger: [ ]         # Ready에서 빈 원장 허용
readiness:
  completeness: <필수 코어 필드 전건 충족 판정>
  confidenceVector: <종단 판정 산출 기록>      # 03 §3.2-A 경계 — 산출 기록(결과), Discovery 내부 개념 아님
  openQuestions: [ ]          # 미해결 질문 목록 — Contract가 남기는 미해결 사항(산출 기록)
  userApproval: <사용자 승인 기록>
provenance: <불투명 컨테이너 — UAHF must-ignore; 내부 형식은 discovery-binding.md(예정) 소관, §6>
---

# Project Contract — <프로젝트명>
(위 front-matter 필드의 인간 가독 렌더링 — Advisor Consult 정독 대상, 03 §3.5-B (a))
```

- **경계 문면(중요).** 위 `readiness`의 `confidenceVector`·`openQuestions`는 03 §3.2-A "Readiness 구성의 경계 문면"이 규정한 종단 판정의 **산출 기록**이며, Discovery의 **내부 개념**(질문 선택·전략·예산·Strategy·Capability)이 **아니다**. 특히 `openQuestions`의 '질문'은 Contract가 남기는 미해결 사항이며 Discovery 내부의 질문 선택 기계와 다르다(03 §3.2-A). 따라서 이 산출 기록은 PC-INV 2 역참조 금지의 대상이 아니다(§7).
- 이 예시는 03 §8 "논리 스키마 골격"의 물리 렌더링일 뿐이며, 물리 직렬화·저장 위치를 확정하는 것은 본 문서다(03 §8 도입 문면 정합).

---

## §4. 저장 위치 관례 확정 (done 5 · DP-X2)

03 §4.1 행 2("Contract 인스턴스가 프로젝트에 배치·보관되는 물리 위치·경로 관례")의 물리 실현을 **이원화**로 확정한다. 두 경로 모두 본 문서가 정본으로 확정한다(DP-X2). 이는 01-entry §4.1(### §4.1 바인딩 대상)이 "contract-presence 탐지의 경로 관례·직렬화 형식·존재 판정 수단은 Adapter 소관"으로 미룬 지점의 물리 실현이기도 하다(§3.2-C는 contract-presence Evidence 관측 정의·capability 선언·유/무 값 도메인만 소유하며, Adapter 위임 문구를 담지 않는다).

### §4.1 일반 관례 — 소비 프로젝트 내 배치

- **경로.** 소비 프로젝트 내 `.claude/project-contract/` 디렉터리에 인스턴스 문서를 배치한다.
- **파일명.** 인스턴스 1건 = 파일 1개, `project-contract.v<N>.md`(N = `instanceVersion` 정수, §5). 현재 인스턴스 = 후행 인스턴스에 의해 supersede되지 않은 최고 `instanceVersion` 파일. 인스턴스 갱신은 새 `v<N+1>` 파일 추가로 표현된다(append-only, §3.3 ⓓ).
- **근거.** Contract는 프로젝트 정의 정본 문서로서 (a) Advisor Consult 정독·(b) Scaffold 배치 대상이다(03 §3.5-B). Claude 환경에서 하네스 규약·정의 문서의 관례 홈은 `.claude/`이며(자매 scaffold-template의 `dot-claude/` — AGENT.md·CLAUDE.md·agents/ 배치, scaffold-binding.md §6), Scaffold(specs/12-scaffold.md §3.2-A)가 관리하는 경계다. Contract를 그 아래 전용 하위 디렉터리에 두어 Advisor가 규약 문서와 함께 정독하고 Scaffold가 함께 배치하도록 정합시킨다. Entry의 contract-presence 관측(01-entry §3.2-C Evidence 정의·EN-INV 2 — 유/무 관측)은 이 well-known 경로의 인스턴스 파일 유무로 유/무를 판정한다. 그 **탐지의 경로 관례·직렬화 형식·존재 판정 수단**을 Adapter 소관으로 미룬 절은 01-entry §4.1(불릿 2)이며 — 그중 **존재 판정 수단(탐지 실행)의 상세**는 후속 entry-binding.md(예정) 소관이고, 본 문서는 03 §4.1 행 2가 소유하는 Contract **저장 경로 관례**를 확정한다(추측·선취 금지).

### §4.2 본 UAHF 저장소 인스턴스 — 격리 배치 (Brownfield dogfooding)

- **경로.** 본 UAHF 저장소 자신을 대상 프로젝트로 발견하는 dogfooding 인스턴스는 `framework/adapters/claude/discovery-data/contracts/uahf/`에 격리 배치한다. 파일명 관례는 §4.1과 동일(`project-contract.v<N>.md`).
- **근거(UAF-INV ① 안전).** 본 저장소의 dogfood Contract를 라이브 `.claude/` 규약 표면(하네스 자신의 AGENT.md·CLAUDE.md 등)이나 Core 경계에 섞으면 하네스 규약과 발견 산출 데이터가 혼입된다. 이를 Adapter 경계 이하 `discovery-data/`로 격리하면 데이터 자산이 격리 지점 뒤에 놓여, UAHF 정본 무수정(ARCHITECTURE.md §8 UAF-INV ①)과 정합한다. 이는 자매 `memory-data/`·`loop-data/`가 Adapter 경계 이하로 백엔드 데이터를 격리한 선례(memory-binding.md §0·§2)와 동형이다.
- **`discovery-data/`는 지원 구조(현 시점 미존재).** 이 경로·구조는 본 문서가 확정한 정본 문면이며, 실제 디렉터리·인스턴스 데이터 생성은 **v1.2 E2E Task(T-XG·T-XB) 소관**이다(§10 실측 대조). 본 문서는 물리 데이터 자산을 생성하지 않는다 — 경로·구조·형식의 정본만 소유한다(memory-binding.md §2 주 "지원 구조 — 시연 시 생성" 선례 동형, L-07).

---

## §5. schemaVersion · instanceVersion 표기 형식 확정 (done 6)

03 §4.1 행 3("버전 값의 물리 표기·직렬화")의 물리 실현을 확정한다. 버저닝 규율(03 §3.3)·인스턴스 거버넌스(03 §3.4)는 재정의하지 않고 § 포인터로 인용하며, 물리 표기만 확정한다.

### §5.1 표기 형식

| 값 | 소속 그룹 (03 §3.2-A) | 물리 표기 (이 Adapter 확정) | 근거 계약 |
|---|---|---|---|
| `schemaVersion` | Meta | **SemVer 점표기 문자열** — `meta.schemaVersion`에 `"MAJOR.MINOR"` 형태 문자열(예 형태 `"1.0"`; 03 §8 예2가 `1.0`→`1.1` MINOR 상승 예시). MINOR·MAJOR 자리의 정수 상승으로 표기. | 03 §3.3-B SemVer 규율 |
| `instanceVersion` | Meta | **단조 증가 정수** — `meta.instanceVersion`에 `1`, `2`, … 정수(03 §8 예3이 `1`→`2` 예시). 갱신마다 1씩 증가하며 파일명 `v<N>`과 정합. | 03 §3.4 인스턴스 거버넌스 |
| `supersedes` | Meta | **이전 인스턴스 참조** — `meta.supersedes`에 이전 `instanceVersion`(또는 그 인스턴스 문서 참조). 최초 인스턴스는 `null`. | 03 §3.4 supersedes 계보 |

### §5.2 물리 표기가 버저닝 불변을 훼손하지 않음 (PC-INV 4·5·6)

- **MINOR = 후방 호환 추가만 (PC-INV 4).** 선택 필드·부속 네임스페이스 추가는 `schemaVersion` MINOR 자리 상승으로 표기된다. front-matter는 자기서술 구조이므로 tolerant reader가 추가된 미지 key를 must-ignore한다(§3.3 ⓑ) — 기존 소비 거동 불변. 물리 표기(문자열 정수 상승)는 이 규율을 있는 그대로 담을 뿐 훼손하지 않는다.
- **MAJOR = 파괴 변경(원칙 금지) (PC-INV 4).** 필수 코어 필드 제거·의미 변경 등 MAJOR는 **원칙적으로 금지**되며, 불가피 시 마이그레이션 경로 + 거버넌스 개정 절차가 필수다(03 §3.3-B). 이는 물리 표기 사안이 아니라 거버넌스 사안이므로, 본 문서의 표기 형식은 MAJOR를 물리적으로 "허용"하거나 자동화하지 않는다 — MAJOR 상승 자체가 03 §3.3-E 스키마 개정 거버넌스(spec 버전 상승 + Revision History)를 거친다.
- **필드 제거 금지·deprecated 마킹 (PC-INV 6).** 확정 필드는 제거하지 않는다. 사용 중단이 필요하면 해당 front-matter key에 `deprecated: true` 성격의 마킹을 부기하고 **key를 유지**한다(03 §3.3-D). 자기서술 구조에서 deprecated 필드는 tolerant reader가 계속 안전하게 무시·소비할 수 있으므로(§3.3 ⓑ), 물리 표기가 deprecated 마킹을 훼손 없이 담는다. 물리적으로 key를 삭제하는 것은 파괴 변경(MAJOR)이며 위 거버넌스 대상이다.

### §5.3 스키마 개정 거버넌스의 물리 반영

- 본 스키마(코어 필드·버저닝 규칙)의 개정은 정본 planning/specs/03의 spec 버전 상승 + §9 Revision History append로만 이뤄지고(03 §3.3-E), 그와 별개로 **본 바인딩 문서(직렬화·경로·표기)의 개정**은 본 문서 §9 이력 append + Advisor 승인으로 이뤄진다(거버넌스 문단). 두 거버넌스는 구분된다 — 03 §3 논리 스키마 개정 ≠ 본 문서 물리 바인딩 개정. 인스턴스 갱신(§5.1 `instanceVersion`)은 또 별개의 append-only 인스턴스 거버넌스다(03 §3.4).

---

## §6. Provenance 불투명 컨테이너 외형·must-ignore 경계 (DP-X6)

03 §4.1 행 4("불투명 부속의 물리 저장 형식 — Discovery 측·Adapter 측 소관, 내부 구조 비정의")의 물리 실현 중 **컨테이너 외형·must-ignore 경계만** 확정한다. 내부 내용은 후속 바인딩에 위임한다(DP-X6, 03 §3.2-D 동형).

- **외형 확정.** Provenance는 Contract 인스턴스 front-matter 내 **분리 네임스페이스 `provenance` key**(불투명 블록)로 놓인다. 코어 필드 그룹(§3.2-A 그룹 1~8)과 물리적으로 구분되는 top-level key 하나로 격리된다.
- **must-ignore 경계 확정.** UAHF tolerant reader는 `provenance` 컨테이너(및 그 하위 전체)를 **must-ignore**한다 — 존재를 오류로 취급하지 않고 소비하지 않는다(03 §3.2-D·§3.3-C, PC-INV 3·5). 이 경계로 Discovery 내부 변경(기법·전략·예산·질문 방식)이 만드는 실행 메타는 `provenance`와 `instanceVersion`에만 반영되고 `schemaVersion`·코어 스키마에 도달하지 못한다(03 §3.4·§3.2-D, PC-INV 2·10).
- **내부 형식 비정의 — 후속 위임.** `provenance` 컨테이너의 **내부 직렬화 형식·필드**(Event 로그 참조 등)는 본 문서가 정의하지 않는다. 03 §3.2-D가 지정한 Discovery 측 소관(discovery/specs/02-discovery.md §3.5 Event 로그·§3.16 Metrics)과 Adapter 측 후속 바인딩 **discovery-binding.md(예정)**에 포인터로만 위임한다. 본 문서가 내부 구조를 창설하면 03 §3.2-D 불투명 부속 계약을 침범하므로, 외형·경계 확정에서 멈춘다.

---

## §7. 상시 불변 자기 점검 (done 7)

본 물리 바인딩이 03 §3.6 불변을 훼손하지 않음을 자가 스캔으로 점검한다. 자체 점검은 최종 승인이 아니다 — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다(02 §3.2-A).

### §7.1 코어 필드 직렬화에 Discovery 내부 개념 0건 (PC-INV 2)

- **점검 대상(scope).** 코어 필드 직렬화를 정의하는 절 — §3(직렬화 포맷, §3.4 예시 front-matter의 그룹 1~8 코어 필드부 포함)과 §5(버전 표기). 즉 03 §3.2-A 그룹 1~8에 대응하는 물리 코어 필드 정의부다. Provenance(§6, 그룹 9)와 Readiness의 산출 기록은 03 §3.2-A 경계 문면·PC-INV 2대로 **제외**한다.
- **다중 패턴 자가 스캔.** 위 scope의 코어 필드 정의부에 대해 Discovery 내부 개념 다중 패턴 — { 질문 선택 · 전략 · 예산 · Strategy · Capability } — 을 스캔한 결과 **0건**이다. 코어 필드 front-matter key(`meta`·`intent`·`requirements`·`constraints`·`risks`·`architectureDirection`·`assumptionLedger`·`readiness`)는 자기완결적으로 정의되며 Discovery 내부 개념을 import하지 않는다.
- **경계 확인(Readiness 산출 기록).** §3.4 예시의 `readiness.confidenceVector`·`readiness.openQuestions`는 종단 판정의 **산출 기록**(결과)이며 Discovery 내부 개념이 아니다(03 §3.2-A 경계 문면). `openQuestions`의 '질문'은 Contract가 남기는 미해결 사항이지 Discovery의 질문 선택 기계가 아니다. 따라서 이는 PC-INV 2 역참조 금지 대상이 아니며, 위 0건 판정에서 정당하게 제외된다.
- **스캔 패턴의 등장 위치(전수).** 위 패턴 어휘({질문 선택·전략·예산·Strategy·Capability})는 본 문서에서 오직 **불변·경계·근거를 서술하는 문안**에만 등장한다 — 구체적으로 근거 정본 인용(머리말의 UAF-INV ③ "Strategy Invariance")·§3.4 경계 문면(이들이 코어 필드가 **아님**을 명시하는 배제 설명)·§6 must-ignore 근거 서술·본 §7 스캔 서술·§12 요약의 §7 재서술이다. 이는 03 §3.2-A 경계 문면·§3.6 PC-INV 2 자체가 이 어휘를 배제·불변 문면에 담는 것과 동형이다. **코어 필드 정의부**(§3.4 예시 front-matter의 그룹 1~8 코어 필드 key + §5 버전 표기 표)에는 0건이다 — mention(불변·경계·근거 서술)과 use(코어 필드 정의)의 경계를 지킨다. 03 §7 Verifier 방법(코어 필드 정의 그룹 1~8 대상 grep)과 동일 scope다.

### §7.2 Stable Contract 규율 훼손 0 (PC-INV 11)

- **SemVer (PC-INV 4).** `schemaVersion` 물리 표기(§5.1)는 SemVer 점표기 문자열이며, MINOR = 후방 호환 추가·MAJOR = 원칙 금지(거버넌스 사안) 규율을 있는 그대로 담는다 — 표기가 규율을 자동 완화·훼손하지 않는다(§5.2).
- **tolerant reader (PC-INV 5).** front-matter 자기서술 구조는 필수 코어 필드 key만 의존, 미지 필드·`provenance` must-ignore를 지원한다(§3.3 ⓑ·§6). 물리 형식이 must-ignore를 가능케 한다.
- **필드 제거 금지 (PC-INV 6).** deprecated 마킹 후 key 유지로 표현되며, 물리 삭제는 MAJOR 거버넌스 대상이다(§5.2). 물리 표기가 제거 금지 규율을 훼손하지 않는다.
- **판정.** 위 세 규율의 물리 훼손 서술 0건 — 본 문서의 물리 바인딩은 Public API 장기 호환성을 훼손하지 않는다(PC-INV 11, ARCHITECTURE.md §7.1 ②·§8 UAF-INV ①②).

### §7.3 UAHF 무수정·창설 금지 (PC-INV 8·UAF-INV ①)

- 본 문서는 UAHF spec의 연산·필드·불변을 추가·변경하지 않는다. Contract의 UAHF 소비(tolerant reader·Consult 정독·Scaffold 배치)는 기존 UAHF 관행으로 성립하며(03 §3.5-B·PC-INV 8), 정식 등재는 03 §3.5-C 확장 포인트로 남는다 — 본 문서는 그 등재를 설계하지 않는다.
- 새 계약 요소(필드·연산·불변·kind)를 창설하지 않았다 — 본 문서는 직렬화 형식·경로·버전 표기·Provenance 컨테이너 외형 넷의 물리 실현만 확정한다.

---

## §8. 03 §4.2 이식 교체 지점 대응 (done 8)

03 "### 4.2 이식 교체 지점"의 3개 교체 지점 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 03 §3 Core Contract 불변(structure.md §7 C-1 동형)을 재확인한다.

| 03 §4.2 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (03 §3 불변) |
|---|---|---|---|
| Contract 직렬화 형식 → 대상 환경의 문서·레코드 포맷 | §2 행1, §3 | Markdown 본문 + YAML front-matter 단일 문서, §3.4 물리 front-matter 형태. | 03 §3.1 지위·논리 스키마, §3.2-A 필드 그룹 9종·§3.2-B 필수 코어 필드·§3.2-C Dimension 매핑(PC-INV 1). |
| Contract 저장 위치·경로 관례 → 대상 환경의 배치 메커니즘 | §2 행2, §4 | 일반 `.claude/project-contract/`·본 저장소 `framework/adapters/claude/discovery-data/contracts/uahf/`, `project-contract.v<N>.md` 파일명. | 03 §3.4 인스턴스 거버넌스(append-only·supersedes 계보), §3.5 UAHF Interface(선택 입력·두 소비 지점, PC-INV 9). |
| 버전 표기·Provenance 물리 형식 → 대상 환경의 표기·기록 메커니즘 | §2 행3·4, §5, §6 | `schemaVersion` SemVer 점표기 문자열·`instanceVersion` 정수·`supersedes` 참조, `provenance` 분리 컨테이너 외형. | 03 §3.3 버저닝 규율(SemVer·tolerant reader·필드 제거 금지), §3.2-D Provenance 불투명·§3.6 Invariants PC-INV 3·4·5·6·10·11. |

- "유지되는 것" 열의 계약은 다른 AI·저장 환경으로 이식해도 바뀌지 않는다 — 03 §3 Core Contract의 이식 불변성이며, 03 §4.2 "유지되는 것"(§3.1 지위·논리 스키마, §3.2 필드 그룹·필수 코어 필드·Dimension 매핑, §3.3 버저닝 규율, §3.4 인스턴스 거버넌스, §3.5 UAHF Interface, §3.6 Invariants)과 정합한다(03 §4.2 PC-INV 1). structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 동형이다.
- 본 문서는 03 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고, v1.2 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §10. 상태 서술 실측 대조 (L-07 — 미존재를 실재로 쓰지 않음)

본 문서의 "실재/미존재" 서술을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-07 작성 시 `ls`/`find` 직접 실측.** 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다.

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-07, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계, 격리 지점) | 실재 — 자매 바인딩 문서 다수·`memory-data/`·`loop-data/`·`scaffold-template/` 존재 확인. |
| `framework/adapters/claude/contract-binding.md` | 실재 (본 문서) | 실재 (이 파일 — 신규 생성). |
| `framework/adapters/claude/memory-binding.md` (골격 선례) | 실재 (자매 문서) | 실재 — 확인(무수정). |
| `framework/adapters/claude/scaffold-binding.md` (직렬화 선례) | 실재 (자매 문서) | 실재 — 확인(무수정). |
| planning/specs/03-project-contract.md (바인딩 대상 정본) | 실재 (v1.1 Baseline) | 실재 — §3·§4 확인(무수정, § 포인터 대상). |
| `framework/adapters/claude/discovery-data/` (Contract 배치 백엔드 루트) | **지원 구조 — 현 시점 미존재, v1.2 E2E Task 생성 예정** | **미존재** — `discovery-data/` 디렉터리 부재 확인(delegation 전제 정합). 경로·구조·형식은 본 문서 정본 문면. |
| `discovery-data/contracts/uahf/` 인스턴스 데이터 | **미존재** (E2E Task 생성 예정) | **미존재** — 상위 `discovery-data/` 자체가 부재. |
| 소비 프로젝트 `.claude/project-contract/` (일반 관례) | 경로 관례 확정(정본); 인스턴스 데이터는 설치·발견 시 배치 | 본 저장소에는 해당 경로 미존재(정상 — 일반 관례는 소비 프로젝트 배치 대상). |
| Contract 컴파일러·tolerant reader 파서(형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). |

- **핵심 구분.** 본 문서가 확정한 직렬화 형식·저장 경로·버전 표기·Provenance 컨테이너 외형은 **정본 문면(형태 A)**이며, 물리 데이터 자산(`discovery-data/…`·`.claude/project-contract/…` 인스턴스 파일)은 **현 시점 미존재**로 v1.2 E2E Task(T-XG·T-XB)가 이 정본 구조 그대로 생성할 예정이다. 데이터 생성 주체는 E2E Task이며, 본 문서는 구조·형식·경로·표기의 정본만 소유한다(memory-binding.md §2·§7 "지원 구조 — 시연 시 생성" 선례 동형, L-07).
- 실측과 불일치하는 서술은 0건이다 — 미존재(`discovery-data/`)를 실재로, 실재(자매 바인딩·03 정본)를 미존재로 쓰지 않았다.

---

## §11. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 planning/specs/03 §3·§4의 물리 실현이다. 어떤 필드 그룹·코어 필드·버저닝 규율·인스턴스 거버넌스·불변(PC-INV 1~12)도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 03 §3이다. 새 계약 요소(필드·연산·불변·kind)를 창설하지 않았다.
- **본 문서가 소유·확정하는 것.** 03 §4.1이 "Adapter 소관"으로 미룬 넷 — ① 직렬화 형식(§3, Markdown 본문 + YAML front-matter) ② 저장 위치(§4, 이원화) ③ 버전 표기(§5) ④ Provenance 컨테이너 외형·must-ignore 경계(§6) — 만 확정한다. Provenance 내부 형식은 discovery-binding.md(예정)에, contract-presence 존재 판정 실행은 entry-binding.md(예정)에 포인터로 위임한다(추측·선취 금지).
- **격리 토큰의 단일 자리.** 구체 직렬화 형식(문서형·구조화 데이터 형식)·물리 경로(`framework/adapters/claude/…`·`.claude/…`)·파일 확장자·버전 값 형태는 이 Adapter 경계 문서에 둔다. UAF 정본(planning/specs/03)은 이 토큰을 "Adapter 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3는 이 경계에 비적용 — 격리 보유).
- **동시 작성 문서 경계(07 R2·R4).** 본 산출은 이 1개 파일(`framework/adapters/claude/contract-binding.md`)만 생성하며, 동시 작성 중일 수 있는 병렬 Task의 미완성 산출물(예: discovery-binding.md·entry-binding.md·E2E 데이터)을 인용·추측하지 않았다(07 R2). 확정된 인터페이스 계약(planning/specs/03 §3·§4)만 참조했다. UAF 정본·UAHF 정본·기존 바인딩·물리 데이터를 수정·생성하지 않았다(07 R4·INV-2). 불확실 지점은 §11 open_questions로 에스컬레이션했다(추측 금지).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-TC-1 (저장 위치 일반 관례 경로 — 비차단).** §4.1은 일반 관례 경로를 `.claude/project-contract/`로 확정했다(근거: 하네스 규약·정의 문서 홈 = `.claude/`, Scaffold 관리 경계, Advisor Consult 정독 정합). 이는 자매 관례·03 §3.5-B 정합에 근거한 본 문서의 Adapter 재량 확정이며(DP-X2가 "구체 경로 관례는 본 문서가 확정"으로 위임), 03·specs/12는 구체 경로를 명명하지 않는다. 다른 소비 프로젝트 배치 관례(예: 프로젝트 루트 배치)를 선호한다면 Advisor 재확정이 가능하다 — 계약(03 §3.4·§3.5) 변경은 아니므로 비차단이다.
- **OQ-TC-2 (Provenance 내부 형식·contract-presence 탐지 — 후속 위임, 비차단).** Provenance 컨테이너 내부 형식(§6)과 contract-presence 존재 판정 실행 수단(§4.1)은 본 문서가 외형·경로까지만 확정하고 내부·실행은 후속 바인딩(discovery-binding.md·entry-binding.md, 예정)에 위임했다(추측 금지). 후속 바인딩 착수 시 이 두 지점의 물리 확정이 필요하다. 03 §3.2-D·01-entry §4.1(Adapter 위임)·§3.2-C(Evidence 정의) 계약 변경은 아니므로 비차단이다.

---

## §12. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 **UAF 정본(planning/specs/03) 바인딩** 산출물(DP-X1). 정본 = 03 §3·§4(본 문서는 물리 실현, 재정의 아님 — §0). 자매 바인딩 12문서(UAHF spec 바인딩)와 구분되는 UAF 레벨 바인딩·접두 없는 동형 파일명.
- **§2:** 03 "### 4.1 바인딩 대상" 표 **4행 전건**을 물리 실현으로 매핑(실재/규약 실현/형태 B 3구분).
- **§3:** 직렬화 = **Markdown 본문 + YAML front-matter 단일 문서** — ⓐ 9그룹·필수 코어 필드 10 표현 ⓑ tolerant reader 정합(자기서술·미지 must-ignore) ⓒ Provenance 분리 불투명 컨테이너 ⓓ append-only 인스턴스(새 파일 + `supersedes`) 표현. scaffold-binding.md §4 관례 동형.
- **§4:** 저장 위치 이원화(DP-X2) — 일반 관례 `.claude/project-contract/`(Advisor 정독·Scaffold 배치 정합, 03 §3.5-B) + 본 저장소 격리 `framework/adapters/claude/discovery-data/contracts/uahf/`(UAF-INV ① 안전). 01-entry §4.1 Adapter 위임의 물리 실현(§3.2-C = contract-presence Evidence 정의). `discovery-data/`는 현 시점 미존재·E2E Task 생성 예정.
- **§5:** 버전 표기 — `schemaVersion` SemVer 점표기 문자열·`instanceVersion` 단조 증가 정수·`supersedes` 참조. MAJOR 원칙 금지·필드 제거 금지·deprecated 마킹이 물리 표기에서 훼손 0(PC-INV 4·5·6).
- **§6:** Provenance = 분리 네임스페이스 `provenance` 컨테이너 외형·must-ignore 경계만 확정. 내부 형식은 discovery-binding.md(예정) 위임(DP-X6, 03 §3.2-D 동형).
- **§7:** 상시 불변 자기 점검 — 코어 필드 직렬화(§3 그룹 1~8·§5)에 Discovery 내부 개념(질문 선택·전략·예산·Strategy·Capability) 0건(다중 패턴 자가 스캔; Readiness 산출 기록·Provenance 제외), Stable Contract 규율(SemVer·tolerant reader·필드 제거 금지) 훼손 0(PC-INV 2·11).
- **§8:** 03 "### 4.2" 이식 교체 지점 3건 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 03 §3 불변(C-1 동형) 재확인.
- **§10:** 실측 대조 — `discovery-data/` 현 시점 미존재(E2E Task 생성 예정), 자매 바인딩·03 정본 실재. 미존재를 실재로 쓰지 않음(L-07).
- 03 §3·§4·UAHF 정본 재정의 0, Glossary 용어 신설 0, 새 계약 요소 창설 0, 실행 코드 0(형태 A). 구체 직렬화 형식·물리 경로 토큰은 이 Adapter 경계에서 허용된다(격리 지점).
