# planning/docs/appendix/methodology-mapping — 방법론 → Strategy Provider Capability 대응표 (비정본 부록)

성격: **비정본 부록 (Non-Canonical Appendix)** · 상위 규약: AGENT.md (INV-1)
근거 정본(§ 포인터만·재정의 0): `discovery/specs/02-discovery.md` §3.10(Strategy Provider Interface — §3.10-A Capability 스키마·§3.10-B 입출력 계약·§3.10-C 레퍼런스 Provider·§3.10-D 방법론 대응 비정본 위임)·§3.11(Discovery Dimension 5)·§3.2(Discovery Principles 5)·§3.3·§3.5·§3.7·§3.9·§3.12~§3.16·§3.8 DISC-INV-2·7·8 · 루트 `ARCHITECTURE.md` §8 UAF-INV ⑥ · `planning/ARCHITECTURE.md` §2·§7(본 부록 비정본 등재).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 비정본 선언

정본은 Strategy Provider Interface(`discovery/specs/02-discovery.md` §3.10)뿐이며 본 부록은 참고 대응표다 — 계약·용어 확정 0, 충돌 시 정본이 우선한다. 02 §3.10-D가 방법론 대응을 위임한 **비정본 격리 지점**이 여기이므로, 본 부록에 등장하는 방법론 고유명(grill-me·JTBD·Shape Up·Design Sprint·Event Storming)은 정본 누출이 아니라 격리 지점에서의 정당 보유다(§5·UAF-INV ⑥). 읽기 전에 02 §3.10·§3.11·§3.2를 먼저 이해해야 한다.

---

## §1. 목적

널리 알려진 발견·설계 방법론 5종이, 정본이 이미 정의한 **Strategy Provider Capability 선언**(02 §3.10-A)과 **Discovery Dimension**(§3.11)의 언어로 어떻게 표현될 수 있는지를 예시한다. 목적은 (i) 각 방법론의 핵심 장점이 정본의 일반 계약에 **이미 흡수됨**을 보이는 흡수 시연과, (ii) 방법론 지식이 Provider 구현과 본 부록에만 머물고 Framework 정본으로 새지 않음을 보이는 격리 시연이다. 방법론을 채택·권고·표준화하지 않는다.

---

## §2. 참조 축 (정본 § 포인터 — 재정의 0)

본 부록의 대응은 정본 소유 축으로만 표현된다 — **Capability 선언 스키마**(02 §3.10-A) · **입출력 계약**(§3.10-B — 입력 `{Evidence, Confidence Vector, 잔여 Budget}` / 출력 `{다음 질문 집합}` 또는 `{차원 포화 신호}` 택일) · **Discovery Dimension 5**(§3.11 — Intent/Requirement/Constraint/Risk/Architecture) · **Discovery Principles 5**(§3.2 — P-D1~P-D5) 및 관련 기제(적응 규칙 §3.13·Question Budget §3.14·Discovery Policy §3.15·Validating 게이트 §3.3·§3.7). 정의는 모두 정본 소유이며 여기서 재기재·재정의하지 않는다.

### 2.1 대응의 핵심 관찰 (Strategy Invariance)

02 §3.10-B에 따라 **입출력 계약의 형태는 모든 Provider에서 불변**이다. 따라서 방법론이 실제로 바꾸는 것은 (i) `capability`(어느 Dimension의 증거를 강하게 끌어올리는가)와 (ii) 질문의 성격(`{다음 질문 집합}`을 어떻게 구성하는가) 둘뿐이다. State Machine(§3.3)·Event Model(§3.5)·Contract 완결 기준은 어느 방법론에서도 불변이다(§3.8 DISC-INV-7). **아래 §3의 모든 대응에서 `inputContract`·`outputContract`는 이 불변 형태이므로 방법론별로 재기재하지 않는다** — 방법론별로 달라지는 것은 `capability`와 질문 성격뿐이다.

---

## §3. 방법론 5종 대응표 (예시·비정본 — 실제 Provider 등록 아님)

| 방법론 | 핵심 장점(요약) | `capability`(예시 — 강한 Dimension·§3.11) | 질문 산출 특징(= outputContract의 질문 집합 성격) |
|---|---|---|---|
| **grill-me** | 계획·설계를 집요하게 반문해 숨은 가정·약점·공백을 노출하는 적대적 스트레스 테스트. | Risk 강 · Constraint 중 · Intent·Requirement 정밀화 보조 | 약점 후속 반문 연쇄 — 가장 취약·저확신 지점 집중 |
| **JTBD** | 표면 기능 요청 이면의 "해결하려는 진짜 일(Job)"·상황·진척을 드러내 근본 동기를 확정. | Intent 강 · Requirement 파생 기여 | 상황·진척·동기 중심 질문 |
| **Shape Up** | 착수 전 적정 추상에서 작업을 shaping — appetite로 범위 고정, rabbit hole(위험)·no-go(범위 밖) 사전 식별. | Constraint 강 · Risk 강 · Architecture 방향 기여 | appetite로 경계 지어진 범위·경계 설정 질문 |
| **Design Sprint** | 시간 상자 안에서 이해→발산→수렴→검증을 구조화된 단계로 빠르게 정렬·검증. | Architecture 강 · Intent·Requirement 검증 강 | 단계별·시간 상자 수렴 질문 |
| **Event Storming** | 도메인 이벤트·커맨드·정책·경계를 타임라인에 펼쳐 도메인 복잡성·아키텍처 이음새를 협업적으로 노출. | Architecture 강 · Constraint 중 · Requirement 기여 | 이벤트·커맨드·경계 식별 중심 도메인 탐색 질문 |

각 방법론이 "어느 Provider가 되는가"와 흡수 접점은 다음과 같다(예시적 판단·규범 아님).

- **grill-me.** Confidence Vector에서 **가장 확신이 낮은/취약한 차원**(특히 Risk·Constraint)에 반문을 집중하고 답변의 약점을 다시 파고드는 Provider다. 가치는 정본의 적응 규칙(§3.13 — 단위 Budget당 기대 확신 이득 최대화)과 근거 등급(§3.12 — 사용자 진술 > 추론 > 가정)에 이미 흡수된다.
- **JTBD.** **Intent 차원**에 특히 강하고, 확정된 Job에서 요구가 파생되므로 Requirement에도 부수 기여한다. Intent 우선 발굴은 차원별 Confidence(§3.12)와 포화 차원 스킵(§3.13) 위에서 그대로 표현된다.
- **Shape Up.** appetite = 시간·자원 제약(Constraint), rabbit hole = 실패·지연 지점(Risk)에 강하다. appetite는 **Question Budget**(§3.14 — 총량·차원별 예산·soft/hard 경계)에 직접 대응하고, 규모·리스크별 깊이 조정은 P-D3(§3.13)에, 경계 값이 엔진이 아니라 **데이터**라는 점은 Policy as Data(§3.15)에 흡수된다.
- **Design Sprint.** **Architecture**(방향 결정)와 Intent·Requirement의 **사용자 검증(수렴)**에 강하다. 결정·검증 게이트는 **Validating 상태와 사용자 승인 게이트**(§3.3·§3.7 축3·P-D5)에, 일상 진행의 자동화는 P-D4에, time-box는 Question Budget(§3.14)에 대응한다. **경계(재정의 0):** 이 방법론의 "단계" 진행은 정본 State Machine(§3.3)을 재정의하지 않는다 — 단계 감각은 Provider의 질문 배열 방식일 뿐이며 상태·전이·종단은 §3.3만이 정의한다(§3.8 DISC-INV-2).
- **Event Storming.** **Architecture**(방향·설계 결정·경계)에 특히 강하고 도메인 규칙·정책은 Constraint, 도메인 행위는 Requirement에 기여한다. **네임스페이스 주의(혼동 금지):** Event Storming이 다루는 "도메인 이벤트"는 정본 §3.5 Discovery Event Model의 이벤트(`DiscoveryStarted`·`QuestionAsked` 등 발견 상태 전이 이벤트)와 **전혀 별개**다 — 전자는 발굴되는 **증거의 주제**, 후자는 발견 자체의 **상태 전이 계약**이며 §3.5는 정본만이 소유한다.

---

## §4. 흡수 원칙 종합 (Discovery Principles 접점)

아래 표는 각 방법론이 접점을 갖는 정본 원칙·기제를 모은 것이며, 어느 칸도 정본을 새로 정의하지 않는다.

| 방법론 | P-D1 Many Techniques | P-D2 Confidence Driven | P-D3 Adaptive(§3.13) | Question Budget(§3.14) | Policy as Data(§3.15) | P-D5 사용자 게이트(§3.3·§3.7) |
|---|---|---|---|---|---|---|
| grill-me | ○ | ● (약점 차원) | ● (약점 집중) | ○ | · | ○ (인터뷰) |
| JTBD | ● | ● (Intent 우선) | ○ (포화 스킵) | · | · | · |
| Shape Up | ○ | ○ | ● (깊이 조정) | ● (appetite) | ● (경계=데이터) | · |
| Design Sprint | ○ | ○ | ○ | ● (time-box) | · | ● (결정 게이트) |
| Event Storming | ● | ● (Architecture) | ○ | · | · | · |

(● 강한 접점 · ○ 부수 접점 · · 두드러지지 않음 — 예시적 판단이며 규범이 아니다.)

**핵심 관찰.** 다섯 방법론 어느 것도 정본에 새 원칙·새 상태·새 이벤트·새 계약을 요구하지 않는다. 각 방법론의 가치는 `capability` 선언과 질문 산출 방식으로 표현되며, 그 위의 State Machine·Event·Confidence·Budget·Contract 완결 기준은 02 §3.2~§3.16 정본이 이미 제공한다 — 이것이 P-D1 One Discovery Many Techniques의 실증이다(§3.8 DISC-INV-7).

---

## §5. UAF-INV ⑥ 정합 (방법론 지식의 격리)

- **정본 청정·정당 보유.** 방법론 고유명은 02 §3.10 정본에 등장하지 않으며(§3.10-D가 대응을 본 부록으로 위임했다), 방법론 지식은 각 Strategy Provider의 **구현**과 참고용 **비정본 부록**(본 문서)에만 존재한다. 따라서 본 부록의 고유명은 누출이 아니라 정당 보유이며, 본 부록이 사라져도 정본은 완결적이다. (`uaf-verified:` 정본 청정 판정의 근거는 02 §3.10-D의 위임 문면 자체이며, 본 부록은 정본 파일을 재판정하지 않는다.)
- **교체 가능성 보존.** 방법론은 `capability`와 질문 방식으로만 표현되므로 Provider를 교체해도 출력 Project Contract는 불변이다(§3.8 DISC-INV-7·§3.10-B). Framework는 어떤 방법론이 뒤에 있는지 알 필요가 없다 — 이것이 UAF-INV ⑥이 성립하는 방식이다.

---

## §6. 이 부록이 확정하지 않는 것 (경계)

계약·용어 신설 0(Capability 스키마·입출력 계약·Dimension·Principles의 정본은 02 §3.10-A·§3.10-B·§3.11·§3.2) · Provider 등록 0(§3의 대응은 예시이며 등록·선택은 Strategy Registry §3.9와 구현 버전 소관) · 방법론 표준·권고 0(강·중·보조 판단은 예시적) · 레퍼런스 Provider 증설 0(정본이 싣는 레퍼런스는 §3.10-C의 기본 적응 질문 Provider 1건뿐) · 충돌 시 정본 우선(§0).
