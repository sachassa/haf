# uaf/appendix/methodology-mapping — 방법론 → Strategy Provider Capability 대응표 (비정본 부록)

작성일: 2026-07-07
상태: v1.1 Baseline (CP2 첫 판정 Pass 15/0/0 · CP3 승인 · 사용자 승인 2026-07-07)
성격: **비정본 부록 (Non-Canonical Appendix)**
상위 규약: AGENT.md (INV-1)
근거 정본:

- 사용자 승인 v1.1 실행 계획 (Project Discovery & Entry Layer Architecture) — 본 부록의 격리 결정. 특히 결정 D2③("방법론 분석(grill-me·JTBD·Shape Up·Design Sprint·Event Storming)은 **비정본 부록** 격리, 정본은 Strategy Provider Interface만")과 §"산출물"의 `uaf/appendix/methodology-mapping.md ← 비정본` 표기.
- `uaf/specs/02-discovery.md` v1.1 Draft — Strategy Provider Interface 정본. 특히 §3.10(Capability 선언·입출력 계약·레퍼런스 Provider·§3.10-D 방법론 대응 비정본 위임)·§3.11(Discovery Dimension 5)·§3.2(Discovery Principles 5). 본 부록은 이 정본을 **§ 포인터로만 참조하고 재정의하지 않는다**.
- `uaf/ARCHITECTURE.md` v1.1 Draft (r2) — UAF 상위 구조 정본. 특히 §5 UAF-INV ⑥(Framework는 특정 방법론을 모른다 — 방법론은 교체 가능한 Strategy Provider만이 안다). 본 부록은 이 불변의 성립 조건(방법론 지식의 격리 지점)이다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-07 | v1.1 Draft | 최초 작성 — `uaf/appendix/` 경계 최초 산출물. **비정본 부록**: 발견·설계 방법론 5종(grill-me·JTBD·Shape Up·Design Sprint·Event Storming)의 핵심 장점을 **Strategy Provider Capability 선언** 관점(`uaf/specs/02-discovery.md` §3.10-A 스키마)으로 대응시키는 참고 표. §0 비정본 선언(정본 우선·계약/용어 미확정 명시)·§2 참조 축(§3.10-A·§3.11 § 포인터·재정의 0)·§3 방법론 5종 대응표(각 방법론이 강한 Discovery Dimension·질문 산출 특징·흡수 원칙)·§4 흡수 원칙 종합·§5 UAF-INV ⑥ 정합(방법론 지식은 Provider 구현·본 부록에만·정본 청정)·§6 확정하지 않는 것 확정. 정본 재정의 0(Strategy Provider Interface·Dimension·Capability 스키마는 § 포인터만)·특정 AI 실명·모델명·제품 기능명 0(방법론 고유명은 비정본 격리 지점의 정당 보유)·자가 전수 스캔. | Worker (Advisor 위임, v1.1 W5 T6) |
| 2026-07-07 | v1.1 Baseline | v1.1 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass — 충족 15/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — uaf/ 관행 동형: `uaf/ARCHITECTURE.md` §9·`uaf/specs/02-discovery.md` §9·framework/core/structure.md §9. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 부록의 위치와 비정본 선언

**비정본 선언.** 정본은 Strategy Provider Interface(`uaf/specs/02-discovery.md` §3.10)뿐이며, 본 부록은 참고 대응표다. 본 부록과 정본이 충돌하면 정본이 우선하며, 본 부록은 어떤 계약·용어도 확정하지 않는다.

- **격리 지점.** 본 부록은 `uaf/specs/02-discovery.md` §3.10-D가 방법론 대응을 위임한 **비정본 격리 지점**이다. 정본(§3.10)은 특정 방법론 고유명을 0건으로 유지하고, 방법론 대응은 여기서만 다룬다. 따라서 본 부록에 등장하는 방법론 고유명(grill-me·JTBD·Shape Up·Design Sprint·Event Storming)은 정본으로의 누출이 아니라 **격리 지점에서의 정당 보유**다(§5, UAF-INV ⑥).
- **효력 없음.** 본 부록의 어떤 표·서술도 계약(Capability 스키마·입출력 계약)·용어(Dimension·Principle)를 신설·변경·확정하지 않는다. 정본이 바뀌면 본 부록이 따르며, 그 역은 성립하지 않는다.
- **읽는 순서.** 본 부록을 읽기 전에 `uaf/specs/02-discovery.md` §3.10(Strategy Provider Interface)·§3.11(Discovery Dimension 5)·§3.2(Discovery Principles 5)를 먼저 이해해야 한다. 본 부록은 그 정본 계약에 방법론을 얹어 보이는 참고 자료다.

---

## §1. 목적 (Purpose)

이 부록은 널리 알려진 발견·설계 방법론 5종이, 정본이 이미 정의한 **Strategy Provider Capability 선언**(§3.10-A)과 **Discovery Dimension**(§3.11)의 언어로 어떻게 표현될 수 있는지를 예시한다.

목적은 두 가지다.

- **흡수 시연.** 각 방법론의 핵심 장점이 정본의 일반 계약(교체 가능한 Strategy Provider + Discovery Principles)에 **이미 흡수됨**을 보인다. 즉 Framework가 방법론 고유명을 알지 않고도 그 가치를 담을 수 있음을 예시한다.
- **격리 시연.** 방법론 지식이 Provider 구현(그리고 본 비정본 부록)에만 머물고 Framework 정본으로 새지 않음을 명확히 한다(§5, UAF-INV ⑥).

이 부록은 방법론을 **채택·권고·표준화하지 않는다**. 어느 방법론을 어떤 Provider로 구현할지는 구현 버전과 Provider 저자의 선택이며, 본 부록은 대응의 한 예시일 뿐이다.

---

## §2. 참조 축 (정본 § 포인터 — 재정의 0)

본 부록의 대응은 정본이 소유한 다음 축으로만 표현된다. 아래 정의는 모두 정본 소유이며, 본 부록은 재정의하지 않고 포인터만 둔다.

- **Capability 선언 스키마.** `{providerId, capability, inputContract, outputContract}` — 정의는 `uaf/specs/02-discovery.md` §3.10-A 소유.
- **입출력 계약(전 Provider 불변).** 입력 `{Evidence, Confidence Vector, 잔여 Budget}`, 출력 `{다음 질문 집합}` 또는 `{차원 포화 신호}` 택일 — 정의는 §3.10-B 소유.
- **Discovery Dimension 5.** Intent / Requirement / Constraint / Risk / Architecture — 정의는 §3.11 소유.
- **Discovery Principles 5.** P-D1 One Discovery Many Techniques / P-D2 Confidence Driven / P-D3 Adaptive / P-D4 Minimize Human Intervention / P-D5 Preserve Human Authority — 정의는 §3.2 소유. 관련 기제: 적응 규칙 §3.13 · Question Budget §3.14 · Discovery Policy §3.15 · Validating·사용자 승인 게이트 §3.3·§3.7.

### 2.1 대응의 핵심 관찰 (Strategy Invariance)

정본 §3.10-B에 따르면 **입력 계약과 출력 계약의 형태는 모든 Provider에서 불변**이다. 따라서 방법론이 실제로 바꾸는 것은 다음 두 가지뿐이다.

1. **`capability`** — 어느 Discovery Dimension(§3.11)에 대해 증거를 강하게 끌어올리는가.
2. **질문의 성격** — `{다음 질문 집합}`(§3.10-B 출력)을 어떤 방식으로 구성하는가.

State Machine(§3.3)·Event Model(§3.5)·Contract 완결 기준은 어느 방법론에서도 불변이다(§3.8 DISC-INV-7 Strategy Invariance). 즉 방법론은 **Front-end의 질문 방식만 바꾸며 산출 Contract를 바꾸지 않는다**. 아래 대응표의 "Capability 선언(예시)" 블록에서 inputContract·outputContract를 불변으로 표기하는 이유가 이것이다.

---

## §3. 방법론 5종 대응표

### 3.0 요약 대응표

| 방법론 | 핵심 장점(요약) | 강한 Discovery Dimension(§3.11) | 질문 산출 특징 | 흡수 원칙(§3.2 기제) |
|---|---|---|---|---|
| **grill-me** | 계획·설계를 집요하게 반문해 숨은 가정·약점·공백을 노출하는 적대적 스트레스 테스트. | Risk(강) · Constraint(중) · Intent·Requirement(보조) | 약점 후속 반문 연쇄 — 가장 취약·저확신 지점 집중 | P-D3 Adaptive(§3.13) · P-D2 Confidence Driven · P-D5 Preserve Human Authority |
| **JTBD** | 표면 기능 요청 이면의 "해결하려는 진짜 일(Job)"·상황·진척을 드러내 근본 동기를 확정. | Intent(강) · Requirement(파생) | 상황·진척·동기 중심 질문 | P-D2 Confidence Driven(Intent 우선) · P-D1 One Discovery Many Techniques |
| **Shape Up** | 착수 전 적정 추상에서 작업을 shaping — appetite로 범위 고정, rabbit hole(위험)·no-go(범위 밖) 사전 식별. | Constraint(강) · Risk(강) · Architecture(기여) | appetite로 경계 지어진 범위·경계 설정 질문 | P-D3 Adaptive 깊이 조정(§3.13) · Question Budget(§3.14) · Policy as Data(§3.15) |
| **Design Sprint** | 시간 상자 안에서 이해→발산→수렴→검증을 구조화된 단계로 빠르게 정렬·검증. | Architecture(강) · Intent·Requirement 검증(강) | 단계별·시간 상자 수렴 질문 | P-D4 Minimize Human Intervention + P-D5 사용자 확인 게이트(§3.3 Validating·§3.7 축3) · Question Budget(§3.14) |
| **Event Storming** | 도메인 이벤트·커맨드·정책·경계를 타임라인에 펼쳐 도메인 복잡성·아키텍처 이음새를 협업적으로 노출. | Architecture(강) · Constraint(중) · Requirement(기여) | 이벤트·커맨드·경계 식별 중심 도메인 탐색 질문 | P-D2 Confidence Driven(Architecture 집중) · P-D1 One Discovery Many Techniques |

아래 §3.1~§3.5는 각 방법론의 대응을 §3.10-A 스키마로 풀어 보인다. 모든 "Capability 선언"은 **예시·비정본**이며 실제 Provider 등록이 아니다.

---

### 3.1 grill-me

- **핵심 장점.** 계획이나 설계를 집요하게 반문하여 숨은 가정·약점·미결 공백을 강제로 드러내는 적대적 스트레스 테스트 인터뷰다. 착수 전 가장 약한 지점을 파고들어 이해를 단단하게 만든다.
- **Capability 선언(예시·비정본 — §3.10-A 스키마).**

  | 선언 항목(§3.10-A) | 예시 값 |
  |---|---|
  | providerId | (예시) 적대적 반문 Provider |
  | capability | Risk 강 · Constraint 중 · Intent·Requirement 정밀화 보조 |
  | inputContract | `{Evidence, Confidence Vector, 잔여 Budget}` — 전 Provider 불변(§3.10-B) |
  | outputContract | `{다음 질문 집합 = 약점 반문 연쇄}` \| `{차원 포화 신호}` — 형태 불변(§3.10-B) |

- **어느 Provider가 되는가.** Confidence Vector에서 **가장 확신이 낮은/취약한 차원**(특히 Risk·Constraint)에 반문을 집중하는 Provider가 된다. 답변의 약점을 다시 파고드는 후속 질문 연쇄로 해당 차원의 확신을 끌어올린다.
- **흡수 원칙.** P-D3 Adaptive(약점 집중 = 단위 Budget당 기대 확신 이득 최대화, §3.13) · P-D2 Confidence Driven(약점 차원이 임계에 이를 때까지 반문) · P-D5 Preserve Human Authority(사용자를 인터뷰하며 최종 판단은 사용자에게 남김). 이 방법론의 가치는 정본의 적응 규칙(§3.13)과 근거 등급(§3.12, 사용자 진술 > 추론 > 가정)에 이미 흡수된다.

---

### 3.2 JTBD (Jobs To Be Done)

- **핵심 장점.** 표면적 기능 요청 이면에서 사용자가 "해결하려는 진짜 일(Job)"과 그 상황·진척을 파고들어 프로젝트의 근본 동기를 드러낸다. 무엇을 만들지보다 **왜·무엇을 위해**를 먼저 확정한다.
- **Capability 선언(예시·비정본 — §3.10-A 스키마).**

  | 선언 항목(§3.10-A) | 예시 값 |
  |---|---|
  | providerId | (예시) Job 중심 의도 발굴 Provider |
  | capability | Intent 강 · Requirement 파생 기여 |
  | inputContract | `{Evidence, Confidence Vector, 잔여 Budget}` — 불변(§3.10-B) |
  | outputContract | `{다음 질문 집합 = 상황·진척·동기 질문}` \| `{차원 포화 신호}` — 불변(§3.10-B) |

- **어느 Provider가 되는가.** **Intent 차원**("무엇을 왜 하는가", §3.11)에 특히 강한 Provider가 된다. 확정된 Job에서 기능·품질 요구가 파생되므로 Requirement 차원에도 부수적으로 기여한다.
- **흡수 원칙.** P-D2 Confidence Driven(Intent 차원의 확신을 우선 임계까지 끌어올림) · P-D1 One Discovery Many Techniques(하나의 교체 가능 Strategy로서 참여). Intent 우선 발굴이라는 이 방법론의 강점은 정본의 차원별 Confidence(§3.12)와 적응 스킵(§3.13, 포화 차원 스킵) 위에서 그대로 표현된다.

---

### 3.3 Shape Up

- **핵심 장점.** 착수 전 적정 추상 수준에서 작업을 "shaping" 한다 — 투입 상한(appetite)으로 범위를 고정하고(고정 시간·가변 범위), 파고들면 시간을 삼키는 rabbit hole(위험)과 손대지 않을 no-go(범위 밖)를 사전에 식별한다.
- **Capability 선언(예시·비정본 — §3.10-A 스키마).**

  | 선언 항목(§3.10-A) | 예시 값 |
  |---|---|
  | providerId | (예시) 범위·경계 shaping Provider |
  | capability | Constraint 강 · Risk 강 · Architecture 방향 기여 |
  | inputContract | `{Evidence, Confidence Vector, 잔여 Budget}` — 불변(§3.10-B) |
  | outputContract | `{다음 질문 집합 = 범위·경계·appetite 질문}` \| `{차원 포화 신호}` — 불변(§3.10-B) |

- **어느 Provider가 되는가.** **Constraint**(appetite = 시간·자원 제약, no-go = 범위 경계)와 **Risk**(rabbit hole = 실패·지연 가능 지점)에 강한 Provider가 된다. shaped 방향 스케치는 Architecture 차원에도 기여한다.
- **흡수 원칙.** appetite는 정본의 **Question Budget**(§3.14, 총량·차원별 예산·soft/hard 경계)과 직접 대응하고, 규모·리스크에 따른 깊이 조정은 P-D3 Adaptive(§3.13 규모·리스크별 깊이 조정)에 대응한다. appetite·경계 값이 엔진이 아니라 **데이터**라는 점은 Policy as Data(§3.15)에 흡수된다 — 즉 이 방법론의 예산·경계 감각은 별도 계약 없이 Discovery Policy 데이터로 표현 가능하다.

---

### 3.4 Design Sprint

- **핵심 장점.** 시간 상자(time-box) 안에서 문제 이해 → 발산 → 수렴 → 검증에 이르는 구조화된 단계로 빠르게 정렬하고, 이해를 사용자 검증으로 확인한다. 짧은 주기에 방향 결정과 검증을 압축한다.
- **Capability 선언(예시·비정본 — §3.10-A 스키마).**

  | 선언 항목(§3.10-A) | 예시 값 |
  |---|---|
  | providerId | (예시) 수렴·검증 지향 Provider |
  | capability | Architecture 강 · Intent·Requirement 검증 강 |
  | inputContract | `{Evidence, Confidence Vector, 잔여 Budget}` — 불변(§3.10-B) |
  | outputContract | `{다음 질문 집합 = 단계별 수렴 질문}` \| `{차원 포화 신호}` — 불변(§3.10-B) |

- **어느 Provider가 되는가.** 여러 차원에 걸치되 특히 **Architecture**(방향 결정)와 Intent·Requirement의 **사용자 검증(수렴)**에 강한 Provider가 된다. 발산 후 수렴하는 성격상 질문은 단계적이고 시간 상자로 절제된다.
- **흡수 원칙.** 결정(decide)·검증 게이트는 정본의 **Validating 상태와 사용자 승인 게이트**(§3.3 Validating·§3.7 축3·§3.2 P-D5)에 대응하고, 일상 진행의 자동화는 P-D4 Minimize Human Intervention에 대응한다. time-box는 Question Budget(§3.14)으로 표현된다.
- **경계(재정의 0).** 이 방법론의 "단계" 진행은 정본 **State Machine(§3.3)을 재정의하지 않는다**. Design Sprint의 단계 감각은 Provider의 질문 배열 방식일 뿐이며, 상태·전이·종단은 §3.3 정본만이 정의한다(§3.8 DISC-INV-2).

---

### 3.5 Event Storming

- **핵심 장점.** 도메인 이벤트·커맨드·정책·집계·경계를 타임라인에 펼쳐 놓아, 도메인의 복잡성과 아키텍처 이음새(경계·bounded context)를 협업적으로 빠르게 드러낸다. 도메인 구조를 눈에 보이게 만든다.
- **Capability 선언(예시·비정본 — §3.10-A 스키마).**

  | 선언 항목(§3.10-A) | 예시 값 |
  |---|---|
  | providerId | (예시) 도메인 이음새 발굴 Provider |
  | capability | Architecture 강 · Constraint 중 · Requirement 기여 |
  | inputContract | `{Evidence, Confidence Vector, 잔여 Budget}` — 불변(§3.10-B) |
  | outputContract | `{다음 질문 집합 = 이벤트·경계 식별 질문}` \| `{차원 포화 신호}` — 불변(§3.10-B) |

- **어느 Provider가 되는가.** **Architecture**("어떻게 구성할 것인가" — 방향·설계 결정·경계, §3.11)에 특히 강한 Provider가 된다. 도메인 규칙·정책은 Constraint에, 도메인 행위는 Requirement에 기여한다.
- **흡수 원칙.** P-D2 Confidence Driven(Architecture 차원 확신 집중) · P-D1 One Discovery Many Techniques.
- **네임스페이스 주의(혼동 금지).** Event Storming이 다루는 **"도메인 이벤트"는 정본 §3.5 Discovery Event Model의 이벤트(발견 상태 전이 이벤트: `DiscoveryStarted`·`QuestionAsked` 등)와 전혀 별개다.** 전자는 이 Provider가 사용자와 함께 발굴하는 **증거의 주제(도메인 사실)**이고, 후자는 발견 자체의 **상태 전이 계약**이다. 본 부록은 이 둘을 결코 동일시하지 않으며, §3.5 Event Model은 정본만이 소유한다.

---

## §4. 흡수 원칙 종합 (Discovery Principles 접점)

아래 표는 각 방법론이 접점을 갖는 정본 원칙·기제를 한눈에 모은 것이다. 어느 칸도 정본을 새로 정의하지 않는다 — 정본이 이미 가진 원칙(§3.2)·기제(§3.12~§3.15·§3.3·§3.7)에 방법론을 대응시킨 것이다.

| 방법론 | P-D1 Many Techniques | P-D2 Confidence Driven | P-D3 Adaptive(§3.13) | Question Budget(§3.14) | Policy as Data(§3.15) | P-D5 사용자 게이트(§3.3·§3.7) |
|---|---|---|---|---|---|---|
| grill-me | ○ | ● (약점 차원) | ● (약점 집중) | ○ | · | ○ (인터뷰) |
| JTBD | ● | ● (Intent 우선) | ○ (포화 스킵) | · | · | · |
| Shape Up | ○ | ○ | ● (깊이 조정) | ● (appetite) | ● (경계=데이터) | · |
| Design Sprint | ○ | ○ | ○ | ● (time-box) | · | ● (결정 게이트) |
| Event Storming | ● | ● (Architecture) | ○ | · | · | · |

(● 강한 접점 · ○ 부수 접점 · · 두드러지지 않음 — 예시적 판단이며 규범이 아니다.)

**핵심 관찰.** 다섯 방법론 어느 것도 정본에 **새 원칙·새 상태·새 이벤트·새 계약을 요구하지 않는다.** 각 방법론의 가치는 (i) `capability` 선언(어느 차원에 강한가)과 (ii) 질문 산출 방식으로 표현되며, 그 위의 State Machine·Event·Confidence·Budget·Contract 완결 기준은 §3.2~§3.16 정본이 이미 제공한다. 이것이 P-D1 One Discovery Many Techniques의 실증이다 — 하나의 Discovery가 여럿의 기법을 흡수한다(§3.8 DISC-INV-7).

---

## §5. UAF-INV ⑥ 정합 (방법론 지식의 격리)

`uaf/ARCHITECTURE.md` §5 UAF-INV ⑥은 다음을 규정한다 — **Framework는 특정 방법론을 모른다. 방법론은 교체 가능한 Strategy Provider만이 안다. 방법론 지식이 Framework 정본으로 새지 않는다.**

본 부록은 이 불변을 위반하지 않으며, 오히려 그 **성립 조건**이다.

- **정본 청정.** 방법론 고유명(grill-me·JTBD·Shape Up·Design Sprint·Event Storming)은 `uaf/specs/02-discovery.md` §3.10 정본에 0건이다(§3.10-D가 이를 명시하고 대응을 본 부록으로 위임했다). 방법론 지식은 (i) 각 Strategy Provider의 **구현**과 (ii) 참고용 **비정본 부록**(본 문서)에만 존재한다.
- **정당 보유.** 따라서 본 부록에 방법론 고유명이 등장하는 것은 정본으로의 누출이 아니라, 정본이 지정한 **비정본 격리 지점에서의 정당한 보유**다. 정본 계약(§3.10 Interface·§3.11 Dimension·§3.10-A Capability 스키마)은 방법론 고유명 없이 순수하게 유지되고, 본 부록이 사라져도 정본은 완결적이다.
- **교체 가능성 보존.** 방법론은 `capability` 선언과 질문 방식으로만 표현되므로, 방법론(=Provider)을 교체해도 출력 Project Contract는 불변이다(§3.8 DISC-INV-7 Strategy Invariance, §3.10-B 입출력 계약 불변). Framework는 어떤 방법론이 뒤에 있는지 알 필요가 없다 — 이것이 UAF-INV ⑥이 성립하는 방식이다.

---

## §6. 이 부록이 확정하지 않는 것 (경계)

본 부록은 참고 자료로서 다음을 **하지 않는다**.

- **계약·용어 신설 없음.** Capability 스키마·입출력 계약·Discovery Dimension·Discovery Principles를 정의·변경·확장하지 않는다. 이들의 정본은 `uaf/specs/02-discovery.md` §3.10-A·§3.10-B·§3.11·§3.2가 소유한다.
- **Provider 등록 아님.** §3의 "Capability 선언(예시)" 블록은 실제 Provider 등록이 아니라 대응 예시다. 실제 Provider 등록·선택은 Strategy Registry(§3.9)와 구현 버전 소관이다.
- **방법론 표준·권고 아님.** 어느 방법론을 채택·권고·표준화하지 않는다. 방법론과 Dimension의 대응(강·중·보조) 판단은 예시적이며 규범이 아니다.
- **레퍼런스 Provider 아님.** 정본이 싣는 레퍼런스 Provider는 §3.10-C의 **기본 적응 질문 Provider 1건**뿐이다. 본 부록의 방법론별 예시는 그 레퍼런스를 대체하거나 증설하지 않는다.
- **충돌 시 정본 우선.** 본 부록의 어떤 서술이 정본과 어긋나면 정본(§3.10·§3.11·§3.2)이 우선한다(§0 비정본 선언).
