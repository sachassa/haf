# planning — Architecture (Project Contract / 설계 Layer)

작성일: 2026-07-12 (개정 2026-07-13)
상태: v1.3 정합 · 이중 책임 반영 (Project Contract 설계 + Solution Design 성숙 활동 등재)
상위 규약: 루트 `ARCHITECTURE.md` (라우터) · `AGENT.md`
근거 정본 (각 § 포인터로만 참조 — 재정의·복제 0):

- `planning/specs/03-project-contract.md` — Project Contract의 **상세 계약 정본**(지위·논리 스키마·버저닝·인스턴스 거버넌스·UAHF Interface·불변). 본 문서가 개관하고 위임하는 대상. 특히 §0·§1·§3.1(Interface)·§3.2(Data Format)·§3.3(버저닝)·§3.4(인스턴스 거버넌스)·§3.5(UAHF Interface)·§3.6(PC-INV 1~12)·§4(Adapter Binding).
- `planning/specs/04-solution-design.md` — Solution Design 단계(성숙 활동)의 **상세 계약 정본**(단계 계약·복잡도 판정·역할 할당·협업 설계 프로토콜·Projection·경계 기준·불변 SP-INV). 본 문서가 개관하고 위임하는 **이중 책임의 성숙 활동 측** 대상이다. 특히 §0(C2 3항)·§3.1(단계 계약)·§3.2(복잡도 판정)·§3.3(역할 할당)·§3.4(협업 프로토콜)·§3.5(Projection)·§3.6(경계 기준)·§3.8(SP-INV)·§4(Adapter Binding).
- 루트 `ARCHITECTURE.md` (라우터) — UAF 상위 구조 정본. 특히 §2.1(최상위 Layer 지도 — Project Contract = `planning/`)·§2.2(6요소 파이프라인 의미론·Contract 이중 지위)·§2.5(의존 방향)·§3(Layer 연결 계약)·§5(`.claude` 경계)·§7(P2·P3·P5)·§7.1(상시 불변 확인 2건)·§8(UAF-INV ①②③⑤)·§10(책임 경계표 — 비담당② 구현 Planning)·§11(Non-Goals)·§12(용어).
- `uahf/specs/00-glossary.md` §3.3 — UAHF 용어 정본. INV-3("Layer는 정확히 6개다") 무촉 근거. § 포인터로만 참조한다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-12 | v1.3 정합 | 스텁→완전 저술. planning Layer(Project Contract 설계 계약) 개관 정본 신설(라우터 ↔ 하위 spec 사이의 **Layer 개관 고도**). 상세 계약(논리 스키마 필드 그룹 표·필수 코어 필드 목록·Dimension 매핑 표·버저닝 규칙 문면·UAHF Interface·PC-INV 문면 등)은 `planning/specs/03-project-contract.md`가 소유하고 본 문서는 § 포인터로만 위임(재정의·복제 0). Project Contract의 **이중 지위**(Discovery 산출 요소 ∧ UAF↔UAHF 공식 Stable Contract·유일 접점) 개관(루트 §2.2 정합). **C2 네임스페이스 구분** §0 명시 — `planning/` Layer(= Project Contract 설계 계약) ≠ UAHF Advisor/Planner의 구현 Planning(루트 §10 비담당②). 루트 §2.1 지도(Project Contract = `planning/`)와 정합. 새 설계 결정 창설 0 · UAHF 정본 무수정(UAF-INV ①) · 특정 AI/모델/제품 기능명 0. | Worker (Advisor 위임, T-a W2 T-planning) |
| 2026-07-13 | v1.3 · 이중 책임 정합 | Solution Design 마일스톤(W2c) 개정 — planning Layer를 **이중 책임**(① Project Contract 설계[데이터 계약·정본 03] + ② Solution Design 성숙 활동[정본 04])으로 정합. **Δ1** §0 C2 2항→**3항** 재서술(①②③ — 04 §0 정합, ② Solution Design ≠ ③ UAHF 구현 Planning)·§6 구현 Planning 문면 3항 정합. **Δ2** §1 목적 이중 책임 선언·근거 정본에 04 등재·§6 Memory 문면 04 §5 정합(성숙 활동도 v1.3 Memory 무접근). **Δ3** §2 구조 실측 재확인(2026-07-13) — `specs/04-solution-design.md`·부록 2종(`docs/appendix/expert-role-catalog.md`·`projection-catalog.md`) 등재. **Δ4** §7 정본 포인터 표에 04 라우팅 5행·부록 2행 추가. **Δ5** 본 이력 append·상태/작성 라인 갱신. 새 계약·불변·용어 창설 0(전부 04 § 포인터)·UAHF 정본 무수정(UAF-INV ①)·특정 AI/모델/제품 기능명·방법론 고유명 0·기존 §9 행 byte 불변(L-22). | Worker (Advisor 위임, v1.3 W2c) |
| 2026-07-13 | v1.3 · 보완 C-2 등재 | Gap Analysis(사용자 Target Architecture 대조, 옵션 2 승인) 보완 — §2 디렉터리 실측·§7 라우팅 표에 `docs/appendix/review-dimension-catalog.md`(Integrated Design Review 관점 차원 예시 **비정본 부록**) 등재. 새 계약·불변·용어 창설 0·기존 §9 행 byte 불변. | Advisor (사용자 승인) |
| 2026-07-13 | v1.3 · v1.4 바인딩 라우팅 등재 | v1.4 W3 — §7 라우팅 표에 **Solution Design Adapter Binding** 1행 추가(정본 = 04 §4 · `uahf/framework/adapters/<adapter>/solution-design-binding.md` — v1.4 W1 신설·CP2 Pass의 등재 반영). 새 계약·불변·용어 창설 0(라우팅 1행만)·기존 §9 행 byte 불변. | Advisor (v1.4 W3) |
| 2026-07-17 | v1.3 · 참조 정합 | 루트 v1.7 UAF-INV ① 재정의(무수정 폐지·접점 원칙 존치) 정합 — 보호 문면 제거·인용 라벨 갱신, 접점·§ 포인터·계약 무변경·substrate 소비 서술 존치. §0 접점 절·§3 폐쇄성·§5 상위 불변 정합 라벨을 접점 원칙으로 갱신하고 PC-INV 8·UAHF Interface·역참조 금지(의미 2)는 존치. 기존 §9 행 byte 불변·버전 무상승. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-19 | v1.3 · Visual Contract 부록 등재 | Visual Contract 트랙(디자인 필수 요소·원칙 Policy 데이터화 + mock 수렴 규약 §7A/§7C) 마감 등재 — §2 디렉터리·§7 라우팅 표에 `docs/appendix/visual-contract-catalog.md`(**비정본 부록** — 강제 지점은 Policy·게이트·binding) 추가. 새 계약·불변·용어 창설 0·기존 §9 행 byte 불변. | Advisor (사용자 지시 2026-07-19) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, 루트 `ARCHITECTURE.md` §9·`planning/specs/03-project-contract.md` §9·`entry/ARCHITECTURE.md` §9 동형. 절 번호는 §9지만 배치는 머리다. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **개관 고도 선언.** 이 문서는 루트 `ARCHITECTURE.md`(라우터)와 하위 spec `planning/specs/03-project-contract.md`(상세 계약) **사이의 Layer 개관**이다. "무엇이 어디에 있고 어떻게 연결되는가"를 서술하며, "그것이 정확히 무엇인가"의 상세 계약 — 논리 스키마 필드 그룹 표·필수 코어 필드 목록·Dimension 매핑 표·버저닝 규칙 문면·불변 문면 — 은 03이 소유한다. 본 문서는 그 계약을 **§ 포인터로만 참조**하고 재정의·복제하지 않는다(재정의 0).

- **접점 원칙 (UAF-INV ①).** UAF와 UAHF의 접점은 **Project Contract 하나뿐**이며(유일 접점), 본 문서가 다루는 UAHF Interface(Contract가 어떻게 소비되는가)는 UAHF spec의 어떤 연산·필드·불변도 추가·변경하지 않고 재정의·복제 없이 **§ 포인터로만 참조**한다 (루트 §8 UAF-INV ①; 상세 정본 03 §3.5). Contract가 UAHF 접점이라는 특성상 이 재정의 0 규율은 특히 엄격히 유지된다.

- **INV-3 무촉 (Layer 어휘 주의).** "planning **Layer**"의 "Layer"는 UAHF 6-Layer 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter)의 지층(stratum)이 아니라, UAF 파이프라인의 한 **요소(Project Contract)** 를 소유하는 최상위 물리 Layer 명칭이다. Project Contract는 UAHF 6-Layer의 **외부·상류의 UAF 레벨 구조**이며(루트 §0·§2.4), `planning/` 물리 Layer 역시 UAF 파이프라인 축의 지도 단위로 UAHF 수직 스택과 직교한다. 본 문서는 UAHF Layer 수를 늘리는 어떤 서술도 두지 않으며, Glossary INV-3("Layer는 정확히 6개다", `uahf/specs/00-glossary.md` §3.3)는 무촉이다.

- **Core 문서 관행.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·방법론 고유명을 두지 않는다 (루트 §0·03 §0 동형). Contract의 직렬화 형식·물리 포맷·저장 위치 등 환경 구체는 Adapter Binding 소관이며(§7 라우팅·03 §4), 필요한 자리에는 일반형 표기와 소관 포인터만 둔다.

- **C2 — 이름 충돌 해소 (3항 네임스페이스 구분).** 이 `planning/` Layer는 **Project Contract 요소와 그 성숙 활동을 소유하는 물리 Layer**다. planning/ 문맥에서 다음 셋을 혼동하지 않는다(04 §0 C2 정합).
  - ① **Project Contract 설계 (데이터 계약)** — Project Contract의 지위·논리 스키마·버저닝을 소유한다(정본: `planning/specs/03-project-contract.md`). "무엇을 계약으로 고정하는가."
  - ② **Solution Design (성숙 활동)** — Ready 종단 Contract 인스턴스를 실행 가능한 솔루션 설계로 성숙시켜 superseding 인스턴스를 재발행하는 UAF 레벨 활동이다(정본: `planning/specs/04-solution-design.md`). "미결을 어떻게 해소하고 신규 설계 결정을 창출하는가." 정식 명칭은 **Solution Design**이며 "Planning" 계열로 표기하지 않는다(D1·04 §0).
  - ③ **UAHF 구현 Planning (비담당)** — 확정 작업의 구현 계획·작업 분해·병렬 디스패치다(UAHF Advisor/Planner·Workflow 소관, 루트 `ARCHITECTURE.md` §10 책임 경계표의 **비담당②** "**Planning**(구현 계획·작업 분해 — UAHF Advisor/Planner 소관)"). "확정된 것을 어떻게 구현 분해·실행하는가." 본 Layer가 수행하지 않으며 § 포인터로만 가른다.
  - 이 `planning/` Layer는 ①·②를 소유하고 ③은 소유하지 않는다. 특히 **② Solution Design ≠ ③ UAHF 구현 Planning**이며, "Planning"의 3중 의미[①②③] 충돌을 회피하기 위해 성숙 활동을 "Solution Design"으로 표기한다(C2 보전·D1). 이 3항 구분이 본 Layer 저술의 핵심 경계다.

---

## §1. 목적 (Purpose)

planning Layer는 UAF 파이프라인의 **Project Contract 요소(데이터 계약)와 그 성숙 활동(Solution Design)**을 소유하는 물리 Layer다(이중 책임 — 04 §0·§2). 한편으로 Project Contract가 무엇을 담고(논리 스키마), 어떻게 UAF와 UAHF를 잇는 **공식 Stable Contract(Public API)**로서 장기 호환을 유지하며, UAHF가 이를 어떻게 **선택 입력**으로 소비하는가의 **지도**를 개관한다 (루트 §2.2·§8 UAF-INV ①, P3). 다른 한편으로 Ready 종단 Contract 인스턴스를 실행 가능한 솔루션 설계로 성숙시켜 superseding 인스턴스를 재발행하는 **Solution Design 단계**(성숙 활동)를 소유한다(파이프라인 6요소 유지 — Contract 요소 내부의 성숙 루프, 루트 §2.2·04 §0).

이 이중 책임의 상세 계약은 두 spec이 나눠 소유한다 — (i) Project Contract 설계(지위 명문화·논리 스키마 필드 그룹·필수 코어 필드·Discovery Dimension→필드 매핑·버저닝 전략·인스턴스 거버넌스·UAHF Interface·불변 PC-INV)는 `planning/specs/03-project-contract.md`가, (ii) Solution Design 성숙 활동(단계 계약·복잡도 판정·역할 할당·협업 설계 프로토콜·Projection·경계 기준·불변 SP-INV)은 `planning/specs/04-solution-design.md`가 소유한다. 본 문서는 두 계약의 지도를 개관 고도로 제시하며, 상세 목적·Non-Goals 정본은 각각 03 §1·04 §1이다.

---

## §2. Layer 내부 구조 (개관 + 위임)

planning Layer의 내부는 다음 요소로 구성된다. 각 요소의 상세 계약은 03이 소유하며, 여기서는 1~2문장 개관과 § 포인터만 둔다(스키마 표·필드 목록·규칙·불변 문면 복제 금지).

- **Project Contract 지위·연산 계약.** Contract는 UAF↔UAHF 공식 Stable Contract(Public API)이자 유일 접점이며, 생산자(Discovery의 Back-end Compiler)·소비자(UAHF tolerant reader)·완결 기준을 갖는다. 지위와 연산 계약(생산자·소비자·완결 기준·불변 준수)의 정본: 03 §3.1.
- **논리 스키마(필드 그룹·필수 코어 필드·Dimension 매핑).** Contract의 논리 스키마는 필드 그룹(총 9종)으로 구성되고, 유효 Ready Contract가 충족해야 할 **필수 코어 필드**와 Discovery Dimension→필드 그룹 **컴파일 방향 매핑**을 갖는다. 필드 그룹 표·필수 코어 필드 목록·매핑 표의 정본: 03 §3.2 (본 문서는 표·목록을 복제하지 않는다).
- **버저닝 전략.** 스키마 버전과 인스턴스 버전을 분리(`schemaVersion`/`instanceVersion`)하고 SemVer 규율·tolerant reader·필드 제거 금지·스키마 개정 거버넌스를 둔다. 버저닝 규칙 문면의 정본: 03 §3.3.
- **인스턴스 거버넌스.** 특정 Contract 인스턴스의 갱신은 append-only 이력·`supersedes` 계보로 관리된다. 정본: 03 §3.4.
- **UAHF Interface.** Contract가 존재할 때 UAHF가 이를 소비하는 방식 — 선택 입력(하위 호환)·두 소비 지점·정식 등재 확장 포인트. **UAHF spec의 연산·필드·불변을 변경하지 않는다(UAF-INV ①).** 정본: 03 §3.5.
- **불변 PC-INV.** Layer 불변 **PC-INV 1~12**(정본: 03 §3.6). 개관은 §5.
- **Layer 디렉터리 구성 (실측 — 2026-07-13 파일 시스템 직접 재확인).**
  - `planning/ARCHITECTURE.md` — 본 문서(Layer 개관 정본).
  - `planning/specs/03-project-contract.md` — 상세 계약 정본.
  - `planning/specs/04-solution-design.md` — **Solution Design 단계(성숙 활동) 상세 계약 정본**(이중 책임의 성숙 활동 측 — 04 §0). 단계 계약·복잡도 판정·역할 할당·협업 프로토콜·Projection·경계 기준·불변 SP-INV의 소유 정본이다.
  - `planning/contracts/` — Contract 인스턴스 산출 표면. **현재 `.gitkeep`만 존재(콘텐츠 없음 — 자리 표시자)**; Contract 인스턴스는 미배치. 물리 배치·직렬화는 Adapter 소관이다(03 §4).
  - `planning/docs/appendix/methodology-mapping.md` — 방법론 대응 **비정본 부록**(Non-Canonical Appendix). P5 설계 순서의 결정 기록·UAF-INV ⑥(방법론은 교체 가능한 Strategy Provider만이 안다)에 따른 방법론 지식 격리 지점이다.
  - `planning/docs/appendix/expert-role-catalog.md` — Expert Role 예시 **비정본 부록**. Solution Design의 개방 역할 네임스페이스에 대한 참고 카탈로그이며 어떤 계약·용어도 확정하지 않는다(정본: 04 §3.3·SP-INV 5·UAF-INV ⑥ 동형).
  - `planning/docs/appendix/projection-catalog.md` — Projection 유형 예시 **비정본 부록**. Contract=Source of Truth 하의 파생 산출 유형 개방 레지스트리에 대한 참고 카탈로그이며 어떤 계약·용어도 확정하지 않는다(정본: 04 §3.5·SP-INV 5·UAF-INV ⑥ 동형).
  - `planning/docs/appendix/review-dimension-catalog.md` — Integrated Design Review 관점 차원 예시 **비정본 부록**. 통합 리뷰(04 §3.4-D ④)의 검토 관점 차원에 대한 참고 카탈로그이며 어떤 계약·용어도 확정하지 않는다(정본: 04 §3.4·SP-INV 5·UAF-INV ⑥ 동형).
  - `planning/docs/appendix/visual-contract-catalog.md` — Visual Contract(디자인 필수 요소·원칙·mock 수렴) 해설 **비정본 부록**. 사람용 해설·예시·출처 앵커이며 어떤 계약도 확정하지 않는다 — 강제 지점은 Policy 데이터(`solution-design-data/policy/default-policy.yaml` designElements·designPrinciples)와 게이트(design_completeness)·binding §7A/§7C 배선이다(정본: 04 §3.5·§3.9·SP-INV 5·UAF-INV ⑥ 동형).
  - `planning/.claude/README.md` — override 설정 표면(명찰); 현재 override 없음 (루트 §5 Global Default/override 경계 — `.claude`는 디렉터리 관례 명칭).
  - `planning/README.md`·`planning/ROADMAP.md` — Layer 소개·로드맵(현재 스텁).

---

## §3. 입출력 연결 계약 (Inter-Layer Connection)

- **이 Layer의 요소 = Project Contract.** planning Layer는 UAF 파이프라인의 **Project Contract** 요소를 소유한다. Contract는 (i) 상류 Project Discovery(Compiler)의 **산출**이자 (ii) 하류 UAHF의 **선택 입력**이라는 이중 지위를 갖는다 (루트 §2.2·§3). 위상의 상세 개관은 §4.
- **produces (하류 방향) — Project Contract → UAHF (선택 입력).** planning Layer의 요소인 Project Contract는 하류 UAHF에 **선택 입력**으로 주어진다. **부재 시 UAHF는 기존 방식으로 운용된다(하위 호환)** — Contract 없이도 UAHF 운용은 불변이다. 이것이 UAF↔UAHF의 **유일 접점**이다 (루트 §3·§2.2, P3·UAF-INV ①②; 채움 상세 03 §3.5-A).
- **consumes (상류 방향) — Discovery 산출.** Project Contract 인스턴스는 상류 Project Discovery의 Back-end(Contract Compiler)가 planning이 소유한 **단일 타깃 스키마**로 컴파일해 산출한다. **어떤 Discovery Strategy를 쓰든 산출은 동일한 Contract다**(Strategy Invariance) (루트 §2.2·§8 UAF-INV ③, P2; 상세 03 §3.1-B·§3.2-C).
- **의존 방향.** 연결은 위→아래 **단방향**이며, planning(Contract)은 하류 UAHF를 역참조하지 않고, Contract는 Discovery 내부 개념(질문·전략·예산)을 역참조하지 않는다 (루트 §2.5; 03 §3.6 PC-INV 2). 이 폐쇄성이 Discovery 교체 가능성과 접점 원칙(UAHF 인터페이스 안정)을 함께 성립시킨다.
- **스키마 소유.** Project Contract 논리 스키마·버저닝·UAHF Interface의 정본은 03 §3이며, 본 문서는 그 계약을 재정의하지 않는다(재정의 0). 연결 payload는 서술(narrative)이 아니라 **타입 계약(schema)**이므로(루트 §3), 계약이 파일로 남아 하류가 독립적으로 파싱·소비한다.

---

## §4. Layer 고유 절 — 이중 지위 · 파이프라인 위상 (Project Contract)

- **이중 지위.** Project Contract는 (i) 파이프라인의 한 **요소**(Discovery의 산출)이면서 동시에 (ii) UAF↔UAHF의 **계약 접점**(Stable Contract·Public API·유일 접점)이다 (루트 §2.2 "Project Contract의 이중 지위 주의"·§8 UAF-INV ①). 이 이중 지위의 상세(정본 배치·논리 스키마 전용 경계)는 03 §0·§3.1이 소유한다.
- **파이프라인 위상.** planning Layer(Project Contract 요소)는 파이프라인의 **접점 단계**다 — 상류 Discovery의 종단 산출을 받아 하류 UAHF의 선택 입력으로 흐르며, 이 지점에서 UAF와 UAHF가 만난다 (루트 §2.2). 이 위상은 "이 Layer가 파이프라인에서 차지하는 자리"를 가리키는 표지이며, 계약의 알고리즘·필드 상세는 03이 소유한다(본 문서는 복제하지 않는다).
- **버저닝 위상 (개관).** Contract는 Public API로서 **장기 호환을 유지**한다 — 이것이 이 Layer의 위상적 책임이다. 버전 규율(schemaVersion/instanceVersion 분리·SemVer·tolerant reader·필드 제거 금지)의 상세 계약은 03 §3.3·§3.4가 소유하고, 본 문서는 요지와 포인터까지만 둔다 (루트 §7.1 ②).
- **Adapter 바인딩 (포인터만).** Contract의 직렬화 형식·물리 포맷·저장 위치·버전 표기·Provenance 물리 형식은 전부 Adapter 소관이다. 소관 정본: 03 §4(바인딩 대상·이식 교체 지점) 및 해당 실행 환경 Adapter의 Contract 바인딩(`planning/adapters/<adapter>/contract-binding.md`). 본 문서는 물리 형태를 지시하지 않는다.

---

## §5. 불변 (Invariants — 개관)

planning Layer의 불변은 **PC-INV 1~12**(정본: 03 §3.6)가 소유한다. 아래는 명칭·번호 인용과 1줄 요지이며, 문면 정본은 03 §3.6이다(복제 아님).

- **PC-INV 1 — Stable Contract·논리 스키마 전용.** Contract는 공식 Stable Contract(Public API)이며 논리 스키마만 정의하고, 직렬화·물리 포맷·저장 위치는 Adapter 소관이다.
- **PC-INV 2·3 — 역참조 금지·Provenance 불투명.** 코어 스키마 본문에 Discovery 내부 개념이 새지 않으며(0건), Provenance는 UAHF가 must-ignore하는 불투명 부속이다.
- **PC-INV 4·5·6 — SemVer·tolerant reader·필드 제거 금지.** Public API 장기 호환 규율(MINOR 후방 호환 추가만·MAJOR 원칙 금지·미지 필드 must-ignore·확정 필드 제거 금지).
- **PC-INV 7 — Completeness 불가침.** 필수 코어 필드는 모든 Ready 종단에서 전건 충족(실측 또는 가정)되며, Compiler는 불완전 Contract를 산출하지 않는다.
- **PC-INV 8 — UAHF 무수정.** Contract 소비는 UAHF spec의 연산·필드·불변을 변경하지 않는다(접점 하나·정식 등재는 확장 포인트).
- **PC-INV 9 — 인스턴스 이력 append-only.** 인스턴스 갱신은 append-only이며 새 `instanceVersion` + `supersedes` 계보로 기록된다.
- **PC-INV 10·11 — 상시 불변 2건 반영.** Discovery 교체 가능성 보존·장기 호환 훼손 0(루트 §7.1 ①②).
- **PC-INV 12 — AI 비의존.** 계약은 특정 AI 모델·실행 환경·방법론에 의존하지 않으며, 환경 바인딩은 Adapter 소관이다.

**상위 불변 정합.** 위 PC-INV는 상위 UAF 불변·원칙을 Project Contract 수준에서 구속한다 — 특히 **P3**(Contract = UAF↔UAHF 공식 Stable Contract, 루트 §7)·**UAF-INV ①②**(접점 원칙·Contract 교체 불가, 루트 §8)와 정합한다. **역참조 금지·Provenance 불투명**(PC-INV 2·3)은 **P2·UAF-INV ③**(Strategy Invariance)의 스키마 측 성립 조건이다. Contract가 Execution Ready로 확정되는 게이트가 **사용자 승인**이라는 원칙은 **UAF-INV ⑤**(Preserve Human Authority, 루트 §8)다. **P5**(설계 순서 — Contract는 마지막 고정 지점, 루트 §7)에 따라 방법론 상세는 정본이 아니라 비정본 부록(`planning/docs/appendix/`, UAF-INV ⑥) 소관이다. 상시 불변 확인 2건(루트 §7.1 — Discovery 교체 가능성 보존·장기 호환 훼손 0)은 PC-INV 10·11이 반영한다.

---

## §6. 경계 · Non-Goals (Layer 관점)

planning Layer는 다음을 **수행하지 않는다**(경계). 각 항목은 하류·타 소관이며, 중복 서술이 아니라 Layer 관점의 경계 재확인이다.

- **직렬화·물리 포맷·저장 위치 비정의** — Contract의 물리 표현은 Adapter 소관이며 본 Layer는 논리 스키마만 소유한다 (03 §4).
- **Discovery 내부 설계 비정의** — State Machine·Strategy·Confidence·Question Budget 등 Discovery 오케스트레이션은 `discovery/specs/02-discovery.md` 소관이며, 본 Layer는 Discovery의 **산출 계약**만 소유한다 (03 §1 Non-Goals).
- **UAHF 계약 변경 비수행** — UAHF의 연산·필드·불변을 추가·변경하지 않는다. 접점은 Contract 하나이며 정식 등재는 확장 포인트로만 남긴다 (03 §3.5, UAF-INV ①).
- **구현 Planning 비수행 (C2 재확인)** — 구현 계획·작업 분해·병렬 디스패치는 UAHF Advisor/Planner·Workflow 소관이다(루트 §10 비담당②③). 이는 이 `planning/` Layer가 소유하는 ① Project Contract 설계·② Solution Design 성숙 활동과는 다른 ③ 구현 Planning이며, 별개 네임스페이스다(§0 C2 3항).
- **Memory 활용 비설계** — Contract는 데이터 계약 스키마이므로 Memory Service에 접근하지 않으며(03 §5), Solution Design 성숙 활동도 v1.3에서 Memory를 회수·기록하지 않는다(04 §5 — 해당 없음). 향후 활용은 단일 Port 경유 확장 포인트로만 열린다 (03 §5·04 §5).

상세 Non-Goals 정본은 03 §1(Non-Goals)이고, 상위 Non-Goals는 루트 §11이다.

---

## §7. 정본 포인터 표 (Routing)

값을 하드코딩하지 않고 정본 위치로만 라우팅한다.

| 항목 | 정본 |
|---|---|
| planning Layer 상세 계약(지위·논리 스키마·버저닝·인스턴스 거버넌스·UAHF Interface·불변) | `planning/specs/03-project-contract.md` §3 |
| Contract 지위(Stable Contract·Public API) · 연산 계약 | `planning/specs/03-project-contract.md` §3.1 |
| 논리 스키마(필드 그룹 9종·필수 코어 필드·Dimension 매핑) | `planning/specs/03-project-contract.md` §3.2 |
| 버저닝 전략(schemaVersion/instanceVersion·SemVer·tolerant reader·필드 제거 금지) | `planning/specs/03-project-contract.md` §3.3 |
| 인스턴스 거버넌스(append-only·supersedes 계보) | `planning/specs/03-project-contract.md` §3.4 |
| UAHF Interface(선택 입력·두 소비 지점·정식 등재 확장 포인트) | `planning/specs/03-project-contract.md` §3.5 |
| 불변 PC-INV 1~12 | `planning/specs/03-project-contract.md` §3.6 |
| Adapter Binding(직렬화·저장 위치·버전 표기·Provenance 물리 형식) | `planning/specs/03-project-contract.md` §4 · `planning/adapters/<adapter>/contract-binding.md` |
| Solution Design 단계(성숙 활동) 상세 계약 — 단계 계약·복잡도 판정·협업 프로토콜 | `planning/specs/04-solution-design.md` §3 |
| 역할 할당(Expert Role·Capability 선언·개방 네임스페이스·최소 할당) | `planning/specs/04-solution-design.md` §3.3 |
| Projection(Contract=Source of Truth·파생 산출·동적 선택·워크스페이스 귀속) | `planning/specs/04-solution-design.md` §3.5 |
| 성숙 경계 기준(vs Discovery — 미결 해소·신규 설계 결정 창출) | `planning/specs/04-solution-design.md` §3.6 |
| 불변 SP-INV 1~8 | `planning/specs/04-solution-design.md` §3.8 |
| Solution Design Adapter Binding(실행 호스팅·게이트 채널·저장 위치·Policy 실값·성숙 run provenance) | `planning/specs/04-solution-design.md` §4 · `planning/adapters/<adapter>/solution-design-binding.md` |
| 방법론 대응(비정본 부록 — P5·UAF-INV ⑥) | `planning/docs/appendix/methodology-mapping.md` |
| Expert Role 예시 카탈로그(비정본 부록 — 계약·용어 미확정) | `planning/docs/appendix/expert-role-catalog.md` |
| Projection 유형 예시 카탈로그(비정본 부록 — 계약·용어 미확정) | `planning/docs/appendix/projection-catalog.md` |
| Integrated Design Review 관점 차원 예시 카탈로그(비정본 부록 — 계약·용어 미확정) | `planning/docs/appendix/review-dimension-catalog.md` |
| Visual Contract 해설 카탈로그(비정본 부록 — 강제 지점 = Policy designElements/designPrinciples·게이트·binding §7A/§7C) | `planning/docs/appendix/visual-contract-catalog.md` |
| 최상위 Layer 지도 · Project Contract 귀속 | 루트 `ARCHITECTURE.md` §2.1 |
| 6요소 파이프라인 의미론 · Contract 이중 지위 · 의존 방향 | 루트 `ARCHITECTURE.md` §2.2 · §2.5 |
| Layer 연결 계약(Discovery Request · Project Contract) | 루트 `ARCHITECTURE.md` §3 |
| 사용자 고정 원칙 P2·P3·P5 · 상시 불변 확인 2건 | 루트 `ARCHITECTURE.md` §7 · §7.1 |
| UAF 불변 UAF-INV(①②③⑤ 등) | 루트 `ARCHITECTURE.md` §8 |
| 책임 경계표(구현 Planning = 비담당② — C2 대조) | 루트 `ARCHITECTURE.md` §10 |
| `.claude` Global Default / override 경계 | 루트 `ARCHITECTURE.md` §5 |
| Layer 어휘(INV-3 무촉) 근거 | `uahf/specs/00-glossary.md` §3.3 |
| 상위 규약 | `AGENT.md` |
