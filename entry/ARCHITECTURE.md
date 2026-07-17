# entry — Architecture (진입 / Entry Resolution Layer)

작성일: 2026-07-12
상태: v1.3 정합 · 완전 저술 (스텁 대체)
상위 규약: 루트 `ARCHITECTURE.md` (라우터) · `AGENT.md`
근거 정본 (각 § 포인터로만 참조 — 재정의·복제 0):

- `entry/specs/01-entry.md` — entry Layer & Entry Resolution의 **상세 계약 정본**. 본 문서가 개관하고 위임하는 대상. 특히 §3.1(Interface)·§3.2-A~E(Data Format)·§3.3(EN-INV 1~6)·§4(Adapter Binding)·§6(Failure Modes).
- 루트 `ARCHITECTURE.md` (라우터) — UAF 상위 구조 정본. 특히 §2.1(최상위 Layer 지도 — Entry Resolution = `entry/`)·§2.2(6요소 파이프라인 의미론)·§2.5(의존 방향)·§3(Layer 연결 계약)·§7(P1)·§8(UAF-INV)·§12.1(용어)·§12.2(Discovery Request 추상).
- `uahf/specs/00-glossary.md` §3.3 — UAHF 용어 정본. INV-3("Layer는 정확히 6개다") 무촉 근거. § 포인터로만 참조한다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-12 | v1.3 정합 | 스텁→완전 저술. entry Layer 개관 정본 신설(라우터 ↔ 하위 spec 사이의 **Layer 개관 고도**). 상세 계약(결정 테이블 8행·Entry Descriptor 필드 표·판별 규칙 D3 문면·EN-INV 문면 등)은 `entry/specs/01-entry.md`가 소유하고 본 문서는 § 포인터로만 위임(재정의·복제 0). 루트 §2.1 지도(T-D1 정정, Entry Resolution = `entry/`)와 정합(C1). 새 설계 결정 창설 0 · UAHF 정본 무수정(UAF-INV ①) · 특정 AI/모델/제품 기능명 0. | Worker (Advisor 위임, T-a W1 T-entry) |
| 2026-07-17 | v1.3 정합 | 루트 v1.7 UAF-INV ① 재정의(무수정 폐지·접점 원칙 존치) 정합 — 보호 문면 제거·인용 라벨 갱신, 접점·§ 포인터·계약 무변경·substrate 소비 서술 존치. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, 루트 `ARCHITECTURE.md` §9·`entry/specs/01-entry.md` §9 동형. 절 번호는 §9지만 배치는 머리다. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **개관 고도 선언.** 이 문서는 루트 `ARCHITECTURE.md`(라우터)와 하위 spec `entry/specs/01-entry.md`(상세 계약) **사이의 Layer 개관**이다. "무엇이 어디에 있고 어떻게 연결되는가"를 서술하며, "그것이 정확히 무엇인가"의 상세 계약 — 결정 테이블 전개·Entry Descriptor 필드 표·판별 규칙 문면·불변 문면 — 은 01이 소유한다. 본 문서는 그 계약을 **§ 포인터로만 참조**하고 재정의·복제하지 않는다(재정의 0).
- **접점 원칙 (UAF-INV ①).** UAF와 UAHF의 접점은 Project Contract 하나뿐이며, UAHF 계약 요소는 재정의·복제 없이 § 포인터로만 참조한다 (루트 §8 UAF-INV ①).
- **INV-3 무촉 (Layer 어휘 주의).** "Entry **Layer**"의 "Layer"는 UAHF 6-Layer 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter)의 지층(stratum)이 아니라, UAF 파이프라인의 한 **단계(stage)** 명칭이다 (루트 §0 용어 주의·§2.4). 최상위 물리 Layer `entry/` 역시 UAF 파이프라인 축의 지도 단위이며 UAHF 수직 스택과 직교한다. 본 문서는 UAHF Layer 수를 늘리는 어떤 서술도 두지 않으며, Glossary INV-3("Layer는 정확히 6개다", `uahf/specs/00-glossary.md` §3.3)는 무촉이다.
- **Core 문서 관행.** 본문 전체에 특정 AI 이름·모델명·제품 기능명을 두지 않는다 (루트 §0·01 §0 동형). 진입 명령의 물리 형태·Evidence 탐지 수단·직렬화 형식 등 환경 구체는 Adapter Binding 소관이며, 필요한 자리에는 일반형 표기와 소관 포인터만 둔다.
- **C1 — Entry Resolution 귀속.** Entry Layer와 Entry Resolution의 물리 귀속은 `entry/`이며(정본 = 본 문서 `entry/ARCHITECTURE.md` + `entry/specs/01-entry.md`), Project Discovery(`discovery/`)와 구분된다. 이는 루트 §2.1 지도(T-D1 정정)와 일관하며, spec `entry/specs/01-entry.md`의 물리 배치·P1·루트 §12.1과 정합한다.

---

## §1. 목적 (Purpose)

entry Layer는 UAF 공식 진입점을 수용하여, 명시 진입과 Workspace Evidence를 평가해 **Discovery Request를 산출**하는 데까지를 책임진다(개관). Entry는 **Entry Resolution만** 수행하고 Discovery를 수행하지 않으며, 출력은 Discovery Request까지다 (루트 §7 P1·§8 UAF-INV ④).

이 책임의 상세 계약(연산 정의·등록 모델·결정 테이블·Evidence 스키마·불변)은 `entry/specs/01-entry.md`가 소유하며, 본 문서는 그 지도를 개관 고도로 제시한다. 상세 목적·Non-Goals 정본은 01 §1이다.

---

## §2. Layer 내부 구조 (개관 + 위임)

entry Layer의 내부는 다음 요소로 구성된다. 각 요소의 상세 계약은 01이 소유하며, 여기서는 1~2문장 개관과 § 포인터만 둔다(표·규칙·불변 문면 복제 금지).

- **Entry / Entry Resolution 연산.** Entry는 사용자 입력을 수용하는 추상 연산이고, Entry Layer가 수행하는 유일한 연산은 Entry Resolution(명시 진입 × Workspace Evidence → Discovery Request 하나)이다. 연산 계약(입력·출력·완료 조건·Entry 2종)의 정본: 01 §3.1.
- **Entry Descriptor 등록 모델·Resolution 엔진.** Entry는 코드 고정 열거가 아니라 Entry Registry의 데이터 레코드(Entry Descriptor)이며, 엔진은 그 레코드를 평가하는 고정 알고리즘만 갖는다(Policy as Data). Descriptor 필드 표와 엔진 고정 5단계 알고리즘의 정본: 01 §3.2-A.
- **결정 테이블·판별 규칙.** 입력 조합은 결정 테이블에서 정확히 한 결과로 해소되며(결정성), 판별 규칙이 그 근거를 고정한다. 8조합 전수 열거와 판별 규칙 문면의 정본: 01 §3.2-D.
- **Discovery Request 매핑.** Entry Resolution 산출의 3요소는 상위 Discovery Request 추상(루트 §12.2)에 정합하도록 채워진다. 채움 규칙의 정본: 01 §3.2-B.
- **Evidence Source 확장 스키마.** Workspace Evidence는 Capability 선언형 Evidence Source로 등록·확장된다. 등록 스키마와 초기 등재 Evidence의 정본: 01 §3.2-C.
- **mode 네임스페이스.** Discovery Request의 mode는 닫힌 열거가 아니라 확장 네임스페이스다. 네임스페이스 정본: 01 §3.2-E (루트 §12.2 정합).
- **Layer 디렉터리 구성 (실측 — 2026-07-12 파일 시스템 직접 확인).**
  - `entry/ARCHITECTURE.md` — 본 문서(Layer 개관 정본).
  - `entry/specs/01-entry.md` — 상세 계약 정본.
  - `entry/.claude/README.md` — override 설정 표면(명찰); 현재 override 없음 (루트 §5 Global Default/override 경계 — `.claude`는 디렉터리 관례 명칭).
  - `entry/README.md`·`entry/ROADMAP.md` — Layer 소개·로드맵.
  - `entry/docs/` — 자리 표시자만 존재(`.gitkeep`; 콘텐츠 없음).

---

## §3. 입출력 연결 계약 (Inter-Layer Connection)

- **produces — Discovery Request.** entry Layer는 Entry Resolution의 산출로 **Discovery Request**({mode, inputs, policy}) 하나를 생산한다. 이는 하류 `discovery/`(Project Discovery)의 입력이 되는 요소 간 데이터 계약이다 (루트 §3 연결 계약·§2.2 파이프라인 순서).
- **의존 방향.** 연결은 `entry ──[Discovery Request]──▶ discovery` **단방향**이며, entry는 하류를 역참조하지 않는다 (루트 §2.5). Discovery 수행·Contract 생성은 하류 소관이다.
- **스키마 소유.** Discovery Request 3요소 추상의 정본은 루트 §12.2이고, entry 측 채움 규칙은 01 §3.2-B다. 본 문서는 그 추상을 재정의하지 않는다(재정의 0). 연결 payload는 서술(narrative)이 아니라 **타입 계약(schema)**이며(루트 §3), 계약이 파일로 남으므로 하류가 독립적으로 파싱·소비한다.

---

## §4. Layer 고유 절 — 파이프라인 위상 (Entry Resolution)

- **파이프라인 위상.** entry Layer는 UAF 6요소 파이프라인의 **최상류 단계**다 — 사용자 입력을 수용해(진입점) Discovery Request를 방출하는 데서 멈춘다 (루트 §2.2). 내부적으로 Entry Resolution은 고정된 위상 순서 **매칭 → 증거 관측 → 우선순위 평가 → 결정성 검증 → 방출**로 흐른다. 이 5단계 위상은 "이 Layer가 파이프라인에서 차지하는 자리"를 가리키는 표지이며, 각 단계의 알고리즘 상세는 01 §3.2-A가 소유한다(본 문서는 복제하지 않는다).
- **관측만·비수행 경계.** 증거 관측 단계는 Evidence의 유/무를 확정 관측할 뿐, 증거를 수집·해석하는 Discovery를 수행하지 않는다 (01 §3.2-A 2단계·§3.3). Entry는 Discovery Request 방출에서 멈춘다.
- **Adapter 바인딩 (포인터만).** 진입 트리거의 물리 발화 형태·Workspace Evidence의 물리 탐지 수단·Discovery Request의 직렬화·전달은 전부 Adapter 소관이다. 소관 정본: 01 §4(바인딩 대상·이식 교체 지점) 및 해당 실행 환경 Adapter의 진입 바인딩(`entry/adapters/<adapter>/entry-binding.md`). 본 문서는 물리 형태를 지시하지 않는다.

---

## §5. 불변 (Invariants — 개관)

entry Layer의 불변은 **EN-INV 1~6**(정본: 01 §3.3)이 소유한다. 아래는 명칭·번호 인용과 1줄 요지이며, 문면 정본은 01 §3.3이다(복제 아님).

- **EN-INV 1 — Entry Resolution만.** 산출은 Discovery Request 하나로 한정된다(Discovery 비수행).
- **EN-INV 2 — Contract 직접 생성 금지.** Contract를 생성·수정하지 않고 유/무 증거로만 관측한다.
- **EN-INV 3 — 결정성.** 동일 (명시 진입 × Workspace Evidence) 입력은 항상 단일 결과로 해소된다.
- **EN-INV 4 — Layer·엔진 불변 확장.** 신규 Entry·Evidence Source·mode는 Registry 행·Policy 데이터 추가만으로 확장되고 Layer·엔진은 불변이다.
- **EN-INV 5 — Discovery Request 정합·재정의 0.** 산출은 상위 Discovery Request 추상에 정합하며 그 추상을 재정의·확장하지 않는다.
- **EN-INV 6 — 확정 게이트 보존.** 충돌·모호 입력은 임의 확정 대신 사용자 확인 게이트로 표기한다.

**상위 불변 정합.** 위 EN-INV는 상위 UAF 불변·원칙을 Entry 수준에서 구속한다 — 특히 **P1**(Entry = Entry Resolution만, 루트 §7)·**UAF-INV ④**(Entry는 Discovery를 수행하지 않는다, 루트 §8)·루트 **§12.2**(Discovery Request 추상)와 정합한다. 확정 게이트 = 사용자 승인의 상위 원칙은 **UAF-INV ⑤**(Preserve Human Authority, 루트 §8)다.

---

## §6. 경계 · Non-Goals (Layer 관점)

entry Layer는 다음을 **수행하지 않는다**(경계). 각 항목은 하류·타 소관이며, 중복 서술이 아니라 Layer 관점의 경계 재확인이다.

- **Discovery 수행 제외** — 증거 수집·확신 판정·적응적 진행은 Project Discovery 소관이다 (루트 §10 책임 경계표, UAF-INV ④).
- **Project Contract 생성 제외** — Contract 생성은 `discovery/` 소관이며 entry는 Contract를 유/무 증거로만 관측한다 (EN-INV 2).
- **Discovery Request 추상 재정의 제외** — 3요소 추상 정본은 루트 §12.2이며 entry는 채움 규칙만 갖는다 (EN-INV 5).
- **물리 실현(Adapter) 제외** — 진입 명령의 물리 형태·Evidence 탐지·직렬화는 Adapter 소관이다 (§4).

상세 Non-Goals 정본은 01 §1(Non-Goals)이고, 상위 Non-Goals는 루트 §11이다.

---

## §7. 정본 포인터 표 (Routing)

값을 하드코딩하지 않고 정본 위치로만 라우팅한다.

| 항목 | 정본 |
|---|---|
| entry Layer 상세 계약(연산·등록 모델·결정 테이블·Evidence 스키마·불변) | `entry/specs/01-entry.md` §3·§4 |
| Entry & Entry Resolution 연산 · Entry 2종 | `entry/specs/01-entry.md` §3.1 |
| Entry Descriptor 등록 모델 · Resolution 엔진 5단계 | `entry/specs/01-entry.md` §3.2-A |
| Discovery Request 매핑(채움 규칙) | `entry/specs/01-entry.md` §3.2-B |
| Workspace Evidence · Evidence Source 확장 스키마 | `entry/specs/01-entry.md` §3.2-C |
| 결정 테이블 8조합 · 판별 규칙 | `entry/specs/01-entry.md` §3.2-D |
| mode 네임스페이스 | `entry/specs/01-entry.md` §3.2-E |
| 불변 EN-INV 1~6 | `entry/specs/01-entry.md` §3.3 |
| Adapter Binding(대상·이식 교체 지점) | `entry/specs/01-entry.md` §4 · `entry/adapters/<adapter>/entry-binding.md` |
| 최상위 Layer 지도 · Entry Resolution 귀속 | 루트 `ARCHITECTURE.md` §2.1 |
| 6요소 파이프라인 의미론 · 의존 방향 | 루트 `ARCHITECTURE.md` §2.2 · §2.5 |
| Layer 연결 계약(Discovery Request · Project Contract) | 루트 `ARCHITECTURE.md` §3 |
| Discovery Request 3요소 추상 | 루트 `ARCHITECTURE.md` §12.2 |
| 사용자 고정 원칙 P1 · 불변 UAF-INV | 루트 `ARCHITECTURE.md` §7 · §8 |
| `.claude` Global Default / override 경계 | 루트 `ARCHITECTURE.md` §5 |
| Layer 어휘(INV-3 무촉) 근거 | `uahf/specs/00-glossary.md` §3.3 |
| 상위 규약 | `AGENT.md` |
