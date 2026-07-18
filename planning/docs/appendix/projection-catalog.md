# planning/docs/appendix/projection-catalog — Projection 유형 예시 레지스트리 (비정본 부록)

작성일: 2026-07-13
상태: v1.3 Baseline (비정본 부록 · 사용자 승인 2026-07-13)
성격: **비정본 부록 (Non-Canonical Appendix)**
상위 규약: AGENT.md (INV-1)
근거 정본:

- `planning/specs/04-solution-design.md` — Solution Design 단계 정본. 특히 §3.5(Projection — Contract=Source of Truth·파생 산출·동적 선택·워크스페이스 귀속)·§3.7(저장 스코프)·§3.8 SP-INV 5·7·§0(어휘 주의·D5). 본 부록은 이 정본을 **§ 포인터로만 참조하고 재정의하지 않는다**.
- `ARCHITECTURE.md` (루트) — UAF 상위 구조 정본. 특히 §8 UAF-INV ⑥. 본 부록은 이 불변의 성립 조건(Projection 유형 카탈로그 지식의 격리 지점)이다.
- `planning/ARCHITECTURE.md` — 소유 Layer 개관. §2 디렉터리 구성에 본 부록을 비정본으로 등재.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-13 | v1.3 Draft (CP2 대기) | 최초 작성 — Solution Design 마일스톤(W2d) 신설 **비정본 부록**. Projection 유형의 **예시** 개방 레지스트리: Contract=Source of Truth·Projection=파생 원칙(04 §3.5 포인터, §1)·유형 예시 표(PRD·ARCHITECTURE·ADR·UI Guide·API Spec·DB Schema·Deployment — 각 1줄 목적·"언제 유용한가", §3)·전 유형 강제 금지·동적 선택 원칙(§3.0)·ADR "What/Why/Trade-off 보존"·UI Guide "Design Principles·Tokens·Anti-patterns" 예시 세부(§3.1·§3.2)·**사용자 어휘 대응(비정본)** Draft≈Ready vN / Final≈superseding v(N+1)(D5·04 §0, §4)·산출물 워크스페이스 귀속(SP-INV 7, §5) 포인터. 정본(04 §3.5) 재정의 0(§ 포인터만)·계약/불변/용어 확정 0·특정 AI/벤더/모델/제품 기능명 0·방법론 고유명 0(자가 전수 스캔). | Worker (Advisor 위임, v1.3 W2d) |
| 2026-07-13 | v1.3 Baseline | Baseline 승격 — v1.3 마일스톤 사용자 Baseline 승인(비정본 부록). | Advisor (사용자 승인) |
| 2026-07-18 | v1.3 (정합) | §DC-1 Wave 2 — §3.3 신설: `default-policy.yaml` `defaultRequiredSet` 10종(국내 SI 산출물명·policy id·요건 클래스)을 권장 기본 세트 설명으로 등재(정본 = Policy·부록 = 설명). 예시 톤·SP-INV 5 무촉 유지·유형명 방법론 고유명 0. 사용자 결정 2026-07-18. | Worker (Advisor 위임) |

(이력 절은 문서 머리에 둔다 — UAF 관행 동형: `planning/specs/04-solution-design.md` §9·`planning/docs/appendix/methodology-mapping.md` §9. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 부록의 위치와 비정본 선언

**비정본 선언.** 정본은 `planning/specs/04-solution-design.md`뿐이며, 본 부록은 참고 카탈로그다. 어떤 계약·용어도 확정하지 않는다. 코어(04)는 본 부록의 내용을 알지 못한다(UAF-INV ⑥ 동형·SP-INV 5). 본 부록과 정본이 충돌하면 정본이 우선한다.

- **격리 지점.** 04 §3.5는 Projection을 **Contract=Source of Truth 하의 파생 산출**로만 정의하고 유형 목록을 **개방 레지스트리**로 두며 **유형 카탈로그를 열거하지 않는다**(SP-INV 5). 본 부록은 그 레지스트리에 얹을 수 있는 유형 예시를 보이는 참고 자료이며, 여기에 등장하는 유형명은 정본으로의 누출이 아니라 **격리 지점에서의 예시 보유**다.
- **효력 없음.** 본 부록의 어떤 표·서술도 유형을 표준화·등록·강제하지 않는다. 정본이 바뀌면 본 부록이 따르며 그 역은 성립하지 않는다.
- **읽는 순서.** 본 부록을 읽기 전에 04 §3.5(Projection)·§3.7(저장 스코프)·§0(어휘 주의)를 먼저 이해해야 한다.

---

## §1. 목적 (Purpose)

이 부록은 Solution Design이 산출할 수 있는 **Projection**(파생 산출 문서)의 유형을 **예시**로 보인다. 정본 원칙은 04 §3.5가 소유한다.

- **Contract = Source of Truth.** Project Contract가 유일한 진리원천이며, Projection은 이를 근거로 파생 생성되는 프로젝트별 산출 문서다(04 §3.5). Projection은 Contract 코어 스키마를 재정의하지 않는다.
- **파생·동적 선택.** Projection 유형은 개방 레지스트리이며 프로젝트 유형·복잡도에 따라 동적으로 선택된다. 본 부록은 유형을 **채택·권고·표준화하지 않는다** — 대응의 한 예시일 뿐이다.

---

## §2. 참조 축 (정본 § 포인터 — 재정의 0)

본 부록의 예시는 정본이 소유한 다음 축으로만 표현된다. 아래 정의는 모두 정본 소유이며 본 부록은 재정의하지 않는다.

- **Projection 관계.** Contract=Source of Truth → Projection=파생, 동적 선택, 전 유형 강제 금지 — 정의는 04 §3.5 소유.
- **워크스페이스 귀속.** 선택된 Projection 산출은 대상 프로젝트 워크스페이스에 귀속된다(Framework 상태 무오염) — 정의는 04 §3.7·§3.8 SP-INV 7 소유.
- **어휘 주의.** 통칭 "Draft/Final Contract"는 비정본 사용자 어휘이며 정본 표기가 아니다 — 정의는 04 §0 소유(§4에서 대응만 보인다).

---

## §3. Projection 유형 예시 표 (비정본 개방 레지스트리)

### 3.0 동적 선택·전 유형 강제 금지

아래 표는 파생될 수 있는 Projection 유형의 **예시**이며 강제 목록이 아니다. **모든 프로젝트에 모든 유형을 강제하지 않는다** — 프로젝트 유형·복잡도에 따라 필요한 유형만 동적으로 선택한다(04 §3.5). "언제 유용한가" 열은 규범이 아니라 예시적 조건이다.

| 유형(예시) | 1줄 목적 | 언제 유용한가(예시 조건) |
|---|---|---|
| PRD | 무엇을·왜 만드는지(요구·범위·성공 기준)를 서술한다. | 요구가 넓거나 이해관계자가 여럿일 때 |
| ARCHITECTURE | 시스템 구조·경계·주요 설계 결정의 지도를 제시한다. | 구성요소·경계가 여럿이라 구조 합의가 필요할 때 |
| ADR | 개별 설계 결정의 What/Why/Trade-off를 기록해 보존한다. | 되돌리기 어려운 결정·근거 추적이 중요할 때 |
| UI Guide | 인터페이스 설계 원칙·토큰·안티패턴을 담는다. | 사용자 인터페이스 표면이 있고 일관성이 중요할 때 |
| API Spec | 외부 계약(엔드포인트·입출력·오류)을 명세한다. | 외부·타 팀이 소비하는 인터페이스가 있을 때 |
| DB Schema | 데이터 모델·관계·제약을 정의한다. | 영속 데이터 모델이 복잡·핵심일 때 |
| Deployment | 배포·운영·환경 구성 지침을 제시한다. | 운영 환경·릴리스 절차가 비자명할 때 |

(위 유형명·조건은 예시적 판단이며 규범이 아니다. 어느 유형도 표준·필수가 아니다.)

### 3.1 ADR 예시 세부 (예시 어조)

ADR은 개별 설계 결정의 **What(무엇을 결정했나)·Why(왜)·Trade-off(어떤 대안을 어떤 비용으로 접었나)** 를 함께 보존하는 데 유용할 수 있다. Solution Design의 `Reconciling`에서 해소된 trade-off 결정(04 §3.4-D ③)을 결정 단위로 남길 자리가 필요한 프로젝트에서 예시적으로 선택될 수 있다.

### 3.2 UI Guide 예시 세부 (예시 어조)

UI Guide는 프로젝트별로 **Design Principles·Design Tokens·Anti-patterns**(예: "과도한 시각 효과 금지"처럼 해서는 안 될 것을 명시하는 규칙) 등을 담을 수 있다. 사용자 인터페이스 표면이 있고 시각·상호작용 일관성이 중요한 프로젝트에서 예시적으로 선택될 수 있다. 구체 원칙·토큰·금지 규칙의 내용은 대상 프로젝트가 정하며, 본 부록은 담길 수 있는 자리만 예시한다.

### 3.3 권장 기본 세트 — Solution Design 기본 필수 Projection 세트 (설명 · 비정본)

아래 10종은 국내 SI 관행의 **일반 문서 유형명**으로, **solution-design 기본 필수 세트**(`solution-design-data/policy/default-policy.yaml`의 `defaultRequiredSet`)로 채택된 **권장 세트**다. **정본은 Policy 데이터·바인딩 `solution-design-binding.md` §7.2 (다) 값 표이며, 본 부록은 그 설명일 뿐이다** — 부록이 이 세트를 표준화·등록·강제하지 않는다(§0 비정본 선언). 여전히 참고 성격이며, 실제 산출은 프로젝트 선언 범위·복잡도에 따른 동적 선택(기본값 opt-out)과 제외 규칙의 결과다(04 §3.5·§3.8 SP-INV 9). 아래 유형명은 방법론 고유명이 아니라 일반 문서 유형명이며 코어(04)로 누출되지 않는다(SP-INV 5 무촉 — 부록은 원래 유형 열거 허용, §0 격리 지점).

| 산출물명(국내 SI 관행) | policy id (`defaultRequiredSet`) | 요건 클래스 (`requirement`) |
|---|---|---|
| 프로젝트 계획서 | `project-plan` | `always` |
| 요구사항 정의서 | `requirements-def` | `always` |
| 업무 프로세스 | `business-process` | `always` |
| 기능 명세서 | `functional-spec` | `always` |
| 테이블 정의서 | `table-def` | `always` |
| 테스트 계획·케이스 | `test-plan-cases` | `always` |
| 화면 목록 | `screen-list` | `touchpoint` |
| 메뉴 구조도 | `menu-structure` | `touchpoint` |
| 화면 설계서 | `screen-design` | `touchpoint` |
| 인터페이스 명세서 | `interface-spec` | `interface` |

- **요건 클래스 의미(설명).** `always`=항상 default-required(제외는 명시 결정 + 사유 기록 + 사용자 확인) · `touchpoint`=접점(웹·앱·포털) 선언 시 required·미선언 시 자동 N/A · `interface`=외부 연계 선언 시 required·미연계 시 자동 N/A. 규칙 정본은 `default-policy.yaml`의 `requirementClasses`·`exclusionRule`·바인딩 §7.2 (다)다. 침묵 누락(산출도 제외 기록도 없이 구현 경계 넘기)은 금지된다(04 SP-INV 9).
- **여전히 강제 아님.** 이 10종은 성숙 경로의 **default-required**(기본값)이며, 접점/외부 연계 미선언 시 자동 N/A·정당화 제외가 가능하다 — 개방 레지스트리 전체 유형을 강제하는 것과 다르다(04 §3.5). 부록은 이 세트조차 표준화하지 않으며 정본(Policy)이 바뀌면 본 부록이 따른다.

---

## §4. 사용자 어휘 대응 (비정본 — D5 실현 지점)

사용자·이해관계자가 통칭하는 어휘를 정본 표기에 **대응**시키는 참고표다. 아래는 정본 용어가 아니며 04 §0을 참조한다.

| 통칭(비정본 사용자 어휘) | 정본 표기 대응(≈) | 정본 위치 |
|---|---|---|
| "Draft Contract" | Ready 인스턴스 vN | 04 §0·§3.1-B |
| "Final Contract" | superseding 성숙 인스턴스 v(N+1) | 04 §0·§3.1-C |

- **주의.** "Draft/Final Contract"는 정본 용어가 아니다 — 정본은 "Ready 인스턴스 vN / superseding 성숙 인스턴스 v(N+1)"이다(D5·M2·04 §0). 성숙은 단일 문서의 상태 변경이 아니라 supersedes 계보에 의한 **완결 인스턴스의 재발행**이므로(04 §3.6·03 §3.4), "Draft→Final"이라는 단일 문서 진화 은유는 정확하지 않다. 본 대응은 어휘 소통용이며 계약을 신설하지 않는다.

---

## §5. 산출물 귀속 (워크스페이스 — 포인터만)

- 선택된 Projection 산출물은 **대상 프로젝트 워크스페이스**에 귀속되며 Framework 자체 상태를 오염시키지 않는다(SP-INV 7·04 §3.7).
- 물리 배치 위치·경로 관례·직렬화 형식은 정의하지 않으며 Adapter 소관이다(04 §4). 본 부록은 귀속 원칙 포인터만 둔다.

---

## §6. 이 부록이 확정하지 않는 것 (경계)

본 부록은 참고 자료로서 다음을 **하지 않는다**.

- **유형 표준·등록·강제 없음.** 어떤 Projection 유형도 표준화·등록·강제하지 않는다. Projection 관계·선택 계약 정본은 04 §3.5다.
- **계약·불변·용어 신설 없음.** Source of Truth·파생·동적 선택·워크스페이스 귀속·SP-INV를 정의·변경·확장하지 않는다. "Draft/Final" 어휘도 정본화하지 않는다(D5).
- **전 유형 강제 아님.** §3의 유형은 예시이며 모든 프로젝트에 강제되지 않는다 — 동적 선택이 원칙이다(04 §3.5).
- **물리 배치 아님.** 산출물 물리 배치·직렬화는 Adapter 소관이다(04 §4·§3.7).
- **충돌 시 정본 우선.** 본 부록의 어떤 서술이 정본과 어긋나면 04가 우선한다(§0 비정본 선언).
