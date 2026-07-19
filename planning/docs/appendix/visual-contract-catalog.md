# planning/docs/appendix/visual-contract-catalog — Visual Contract 요소 작성 가이드 (비정본 부록)

작성일: 2026-07-19
상태: v1.0 Draft (비정본 부록)
성격: **비정본 부록 (Non-Canonical Appendix)**
상위 규약: AGENT.md (INV-1)
근거 정본:

- `planning/adapters/claude/solution-design-binding.md` — Solution Design Adapter 바인딩. 특히 §7.2 (다) `defaultRequiredSet`(Visual Contract 3종)·(바) `designElements`·§7C(mock 생성·사용자 수렴 규약). **강제는 이 바인딩과 Policy·게이트에 있으며, 본 부록은 참고 문서일 뿐 강제 근거가 아니다.**
- `uahf/framework/adapters/claude/solution-design-data/policy/default-policy.yaml` — `designElements`·`defaultRequiredSet` 실값(Policy as Data). 요소 목록·강제 여부의 정본은 이 Policy다.
- `orchestration/adapters/claude/design_completeness.py`·`design-manifest.schema.md` — 선언 완전성 결정적 게이트·매니페스트 스키마.
- `planning/specs/04-solution-design.md` — Solution Design 단계 정본. 특히 §3.9(UI/UX Visual Contract 협의 프로토콜 확장 포인트)·§3.4 `Validating`·§3.8 SP-INV 5·9. 본 부록은 이 정본을 **§ 포인터로만 참조하고 재정의하지 않는다**.
- `ARCHITECTURE.md`(루트) §6 원칙 11(책임 있는 자율)·§8 UAF-INV ⑥. 본 부록은 그 격리 지점(요소별 방법론 지식)이다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-19 | v1.0 Draft | 최초 작성 — Visual Contract 트랙 비정본 부록 신설. `designElements` screenScope 5종·projectScope 3종 + 산출물 3종(`design-tokens`·`screen-mock`·`mock-convergence-record`) 각각의 "무엇을·잘 만드는 법·예시"를 참고 카탈로그로 등재. 강제 근거 아님 명기(SP-INV 5)·정본(바인딩·Policy·게이트) § 포인터만·재정의 0·특정 AI/벤더/모델/제품 기능명 0·방법론 고유명 0(자가 전수 스캔). | Worker (Advisor 위임) |
| 2026-07-19 | v1.1 Draft | Visual Contract Wave 2 — §5(UI 디자인 원칙 7종 해설) 추가: 각 원칙 자체 재서술 + 적용 예/반례 1쌍 + 라우팅 표(강제 지점 = Policy `designPrinciples` + 브리프/리뷰 배선·부록은 참고). 출처 앵커(Figma UI design principles). 강제 근거 아님·원문 전재 0·방법론 고유명 0. | Worker (Advisor 위임) |
| 2026-07-19 | v1.2 Draft | Visual Contract Wave 3(UX) — §1/§2 요소 카탈로그에 UX 기본 필수 3종(`user-journey-map`·`error-recovery`·`feedback-rules`) 해설 추가·요소 경계(component-states/feedback-rules/error-recovery) 주석. §2a(인터뷰 표면화 시 편입 항목 — onboarding-flow·user-types·ux-copy·다국어·편입 절차=프로젝트 policy 사본 데이터 추가·선언-조건부 동형) 신설. §6(Nielsen 사용성 휴리스틱 10종 해설 — 자체 재서술·예/반례·출처 앵커). 범위 감량(6→3 기본 필수·오버엔지니어링 방지·사용자 결정 2026-07-19). 강제 근거 아님. | Worker (Advisor 위임) |

(이력 절은 문서 머리에 둔다 — UAF 관행 동형: `planning/docs/appendix/projection-catalog.md` §9. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 부록의 위치와 비정본 선언

**비정본 선언.** 정본은 바인딩(§7.2·§7C)·Policy(`designElements`)·게이트(`design_completeness`)이며, 본 부록은 **참고 카탈로그**다. 어떤 계약·용어·강제도 확정하지 않는다. 코어(04)는 본 부록의 내용을 알지 못한다(UAF-INV ⑥ 동형·SP-INV 5). 본 부록과 정본이 충돌하면 정본이 우선한다.

**강제와 참고의 분리(책임 있는 자율 (a)).** 빠지면 안 되는 것(요소 커버·요소 단위 제외 사유 기록)은 **Policy `designElements` + 게이트**가 강제한다. 본 부록은 "**어떻게 잘 만드는가**"의 방법·예시만 제공한다 — 여기의 어떤 항목도 게이트 통과 조건이 아니다(게이트는 covered/정당화 excluded 선언 완전성만 본다).

---

## §1. projectScope 요소 (프로젝트 단위 1회)

| 요소 id | 무엇을 | 잘 만드는 법(참고) | 커버 앵커 예시(`pointer`) |
|---|---|---|---|
| `design-tokens-values` | 색·타이포 위계·간격·radius의 **실값** | 하드코딩 값을 토큰 이름으로 승격(예: `color.primary`, `space.4`, `radius.md`). 팔레트·타입스케일·스페이싱 스케일을 표로 고정. | `docs/design-tokens.md#values` |
| `tone-and-manner` | 톤앤매너 확정 — **스케일 선택·레퍼런스 앵커·금지 목록** | 톤 축(예: 정보 밀도 高↔低, 뉘앙스 정적↔활기)에서 선택값을 명시. 레퍼런스는 링크 앵커만 인용(정본은 리포 텍스트). "하지 말 것"(금지 목록)을 함께 적어 drift를 막는다. | `docs/design-tokens.md#tone` |
| `accessibility-floor` | 접근성 최소선 — **명도 대비·포커스 표시·터치 타겟** | 본문/큰 텍스트 대비 기준, 키보드 포커스 가시성, 최소 터치 타겟 크기를 수치로 고정. 최소선이므로 "이보다 낮으면 실패"의 하한만. criteria 실값은 Policy에. | `docs/design-tokens.md#a11y` |
| `user-journey-map` (UX) | 핵심 사용자 여정 맵 — 주요 태스크별 진입→완료 단계 | 대표 태스크 2~3개의 시작점·단계·완료 조건·이탈점을 단계 흐름으로 정리. | `docs/user-journey.md` |

- **디자인 토큰이 mock의 소비 정본이다.** `screen-mock`(HTML)은 이 토큰 실값을 소비해 생성된다(§7C.2). 토큰 변경은 토큰 갱신 → mock 재생성이지, mock 직접 수정이 아니다.

## §2. screenScope 요소 (각 화면이 커버)

| 요소 id | 무엇을 | 잘 만드는 법(참고) |
|---|---|---|
| `layout-structure` | 레이아웃 구조 — 그리드·주요 영역 구획 | 화면을 영역(헤더/사이드/본문/푸터 등)으로 구획하고 그리드 컬럼을 명시. 와이어프레임과 1:1 대응. |
| `navigation` | 네비게이션 위치·진입/이탈 경로 | GNB/LNB 등 위치, 이 화면으로의 진입 경로와 이탈(다음 화면) 경로를 화면 흐름도와 연결. |
| `component-states` | 컴포넌트 상태 5종 — 기본·로딩·빈·오류·비활성 | 데이터 목록·폼 등 상태를 갖는 컴포넌트마다 5종을 모두 정의. "빈 상태"·"오류 상태"를 특히 빠뜨리지 않는다. |
| `data-rules` | 데이터 표시 규칙 — 정렬·페이징·포맷 | 목록 기본 정렬 키, 페이지 크기, 날짜·통화·수치 포맷을 기능 명세와 연결. |
| `responsive` | 반응형 기준 — 브레이크포인트 최소 1 | 최소 1개 브레이크포인트에서의 레이아웃 변화(예: 사이드 접힘)를 명시. |
| `error-recovery` (UX) | 오류 복구 경로 — 실패 시 이동·되돌리기 | 실패 상태에서 어디로·어떻게 복구하는지(재시도·이전 단계·홈)를 명시. `component-states`의 오류 "상태"와 달리 복구 "경로"다. |
| `feedback-rules` (UX) | 피드백 규칙 — 로딩·성공·실패 알림 방식 | 각 결과를 어떤 방식(토스트·인라인·모달)·지속시간으로 알리는지 규칙화. 상태의 "존재"가 아니라 알림 "방식". |

**요소 경계(중복 오해 방지).** `component-states`(상태 화면의 **존재**) / `feedback-rules`(알림·피드백 **방식**) / `error-recovery`(복구 **경로**)는 서로 다른 축이다 — 한 화면이 세 요소를 각각 별개로 커버한다.

- **요소 단위 제외.** 특정 화면에서 어떤 요소가 해당 없을 때(예: 정적 안내 화면의 `data-rules`)는 조용히 빠뜨리지 말고 매니페스트에서 `{"status":"excluded","reason":"...","confirmedBy":"..."}`로 사유+확인을 기록한다(Policy `designElements.exclusionRule.silentOmission=금지`·게이트 강제). 이것이 "책임 있는 자율 (b)"의 요소 층 실현이다.

### §2a. 인터뷰 표면화 시 편입 항목 (기본 필수 아님 — 제품 의존)

아래 항목은 **제품 의존적**이라 기본 필수 세트에 넣지 않는다(넣으면 형식적 제외 기록만 양산·오버엔지니어링·사용자 결정 2026-07-19). **인터뷰·설계에서 필요가 선언되면** 그때 편입한다.

- **편입 절차(Policy as Data·프레임워크 무변경).** 필요가 선언되면 **해당 프로젝트의 policy 사본** `designElements.projectScope`/`screenScope`에 요소를 **데이터로 추가**한다 → 그 프로젝트에서만 required가 된다. 기존 `touchpoint`/`interface` 선언-조건부 패턴과 동형이다(선언 시 required·미선언 시 비적용). 프레임워크 기본 정책·체커·게이트는 변경하지 않는다.

| 편입 후보 | 무엇을 | 언제 편입 |
|---|---|---|
| `onboarding-flow` | 온보딩·첫 사용 흐름(초기 설정·빈 상태 유도) | 첫 사용 경험이 제품 성패에 중요하다고 인터뷰에서 선언될 때 |
| `user-types` | 사용자 유형·권한 상세(역할별 목표·권한) | 다중 역할·권한 분기가 선언될 때 |
| `ux-copy` | UX 카피 규칙(오류 메시지 형식·톤·빈 상태 안내문) | 카피 일관성·보이스톤이 요구로 선언될 때 |
| 다국어(i18n) | 다국어·로케일 규칙(번역 키·방향성·포맷) | 다국어 지원이 요구로 선언될 때 |

(이 목록은 참고 후보이며 강제 세트가 아니다. 편입 여부·시점은 인터뷰·설계 판단과 사용자 확인 몫이다.)

## §3. Visual Contract 산출물 3종 (`defaultRequiredSet` touchpoint 클래스)

| 산출물 id | 무엇을 | 잘 만드는 법(참고) |
|---|---|---|
| `design-tokens` | 디자인 토큰·톤앤매너 확정 기록 | §1의 projectScope 3요소를 담는 단일 문서. mock 생성의 입력 정본. |
| `screen-mock` | 화면 mock(HTML) | 확정 와이어프레임 + 토큰을 소비한 **클릭 가능 자기완결 HTML**. 파생 뷰이므로 정본(설계+토큰) 갱신 후 재생성(§7C.2). 브라우저 직접 열람 또는 Artifact 발행(선택·§7C.5). |
| `mock-convergence-record` | mock 수렴 확정 기록 | 사용자 수렴 종료 기록 — **확인자·라운드 수·잔여 피드백 0**. 이 산출이 구현 진입 자격의 표식(§7C.4). |

## §4. mock 수렴 진행(참고 — 규약 정본은 §7C)

1. 기획 산출물 확정 → 대표 1화면 × 톤 3안 제시(§7C.3).
2. 사용자 선택·피드백 → `design-tokens` 확정.
3. 잔여 화면 일괄 생성(확정 토큰 소비).
4. 피드백(예: "GNB/LNB 추가·가입 스텝 변경")은 **정본 설계 산출물 먼저 갱신 → mock 재생성**(mock 직접 수정 금지·§7C.2).
5. 잔여 피드백 0 → `mock-convergence-record` 산출 → 구현 오케스트레이션 진입(`design_completeness` 최후 방어).

---

## §5. UI 디자인 원칙 7종 해설 (참고 — 정본은 Policy `designPrinciples`·바인딩 §7.2 (사))

**강제 지점(라우팅).** 아래 7원칙의 강제는 본 부록이 아니라 아래 두 지점에 있다. 본 절은 해설·예/반례만 제공한다(강제 근거 아님·SP-INV 5).

| 무엇 | 어디서 강제/배선되는가(정본) |
|---|---|
| 원칙 목록·요지(값) | Policy `designPrinciples` 7종 (`default-policy.yaml` (사)) · 바인딩 §7.2 (사) |
| 디자이너 브리프 주입 + 화면설계서 원칙별 근거 기록 요구 | 바인딩 §7A.1 · brief-template `{DESIGN_PRINCIPLES}` 슬롯 |
| mock 수렴 리뷰 차원 대조 | 바인딩 §7C.3a |
| 접근성 기계 판정분(실값) | Policy `designElements.projectScope.accessibility-floor.criteria` · 바인딩 §7.2 (바) |

출처(참고 앵커): https://www.figma.com/ko-kr/resource-library/ui-design-principles/ (아래 요지·예/반례는 자체 재서술이며 원문 전재가 아니다).

| id | 요지(자체 문면) | 적용 예 | 반례 |
|---|---|---|---|
| `hierarchy` (계층 구조) | 크기·두께·색·간격으로 정보 우선순위를 유도한다. | 페이지 제목 24pt bold, 섹션 제목 18pt, 본문 14pt로 스캔 순서가 자명. | 모든 텍스트가 같은 크기·두께라 어디를 먼저 볼지 알 수 없음. |
| `progressive-disclosure` (점진적 공개) | 단계당 적정 정보량만 노출하고 진행 상황을 명시한다. | 가입을 3스텝으로 나누고 "2/3" 진행 표시. | 한 화면에 20개 필드를 한꺼번에 요구해 이탈 유발. |
| `consistency` (일관성) | 패턴을 전체에서 동일하게 유지하고, 이탈은 근거를 요구한다. | 저장 버튼이 모든 화면에서 우하단·같은 색. | 화면마다 기본 버튼 색·위치가 달라 학습이 무효화됨. |
| `contrast` (대비) | 중요 동작·정보에 시각적 우선순위를 부여한다. | 주요 CTA만 채움 버튼, 보조는 외곽선 버튼. | 삭제·저장이 같은 회색이라 위험 동작이 구분 안 됨. |
| `accessibility` (접근성) | 모두가 지각·조작 가능하게 한다(기계 판정분 = `accessibility-floor.criteria`). | 본문 대비 4.5:1 이상·키보드 포커스 링 표시·터치 타겟 44px. | 연회색 위 흰 글씨(대비 2:1)·포커스 표시 제거. |
| `proximity` (근접성) | 관련 있는 요소를 가까이 배치해 관계를 드러낸다. | 라벨과 입력 필드를 붙이고 그룹 간 간격을 넓힘. | 라벨이 엉뚱한 필드에 붙어 보이도록 균일 간격 배치. |
| `alignment` (정렬) | 그리드 기반으로 요소를 정렬해 질서·스캔 가능성을 만든다. | 폼 라벨·입력이 좌측 정렬 그리드에 맞춰 정돈. | 요소마다 들쭉날쭉한 좌표라 시선이 흩어짐. |

- **원칙 위반의 소화 경로.** mock 리뷰에서 원칙 위반이 발견되면 mock을 직접 고치지 말고 **정본 설계 산출물(화면설계서·토큰)을 갱신 → mock 재생성**한다(바인딩 §7C.2·§7C.3a). 본 표의 예/반례는 판단 보조일 뿐 게이트 판정 기준이 아니다.

---

## §6. UX 사용성 휴리스틱 10종 해설 (참고 — 정본은 Policy `designPrinciples`·바인딩 §7.2 (사))

§5와 **동일 라우팅**으로 강제된다(강제 지점 = Policy `designPrinciples` + 브리프/리뷰 배선). 본 절은 해설·예/반례만 제공한다(강제 근거 아님). 출처(참고 앵커): https://www.nngroup.com/articles/ten-usability-heuristics/ (아래는 자체 재서술·원문 전재 아님).

| id | 요지(자체 문면) | 적용 예 | 반례 |
|---|---|---|---|
| `visibility-of-system-status` (상태 가시성) | 지금 무슨 일이 일어나는지 적시 피드백. | 업로드 진행률 바·"저장됨" 표시. | 버튼을 눌러도 아무 반응이 없어 재클릭 유발. |
| `match-real-world` (실세계 일치) | 사용자 언어·개념·순서로 말한다. | "장바구니"·"결제" 같은 친숙어 사용. | "트랜잭션 커밋" 같은 내부 용어를 UI에 노출. |
| `user-control-freedom` (제어와 자유) | 비상구·되돌리기/다시하기 제공. | 삭제 후 "실행 취소" 스낵바. | 확인 없이 즉시 영구 삭제되고 복구 불가. |
| `consistency-standards` (일관성과 표준) | 같은 것을 같게·플랫폼 관례 준수. | 파괴적 동작은 항상 빨강·확인 요구. | 화면마다 "확인/취소" 버튼 좌우 순서가 뒤바뀜. |
| `error-prevention` (오류 예방) | 오류가 나지 않도록 설계로 막는다. | 날짜 선택기로 잘못된 형식 입력 차단. | 자유 입력만 두고 형식 오류를 사후 거부. |
| `recognition-over-recall` (회상보다 인지) | 필요 정보를 노출해 기억 부담 감소. | 최근 선택·자동완성 제시. | 이전 화면의 코드값을 외워 다시 입력하게 함. |
| `flexibility-efficiency` (유연성과 효율) | 초보·숙련 모두에 단축 경로. | 숙련자용 키보드 단축키·일괄 작업. | 모든 사용자가 매번 같은 다단계만 강제됨. |
| `aesthetic-minimalism` (미니멀리즘) | 관련 없는 정보를 덜어낸다. | 핵심 지표만 대시보드 상단에. | 한 화면에 모든 옵션을 나열해 핵심이 묻힘. |
| `error-recognition-recovery` (오류 인식·복구) | 평이한 말로 원인·해결책 제시. | "비밀번호는 8자 이상이어야 합니다" + 입력 포커스. | "오류 코드 0x5" 만 표시하고 해결책 없음. |
| `help-documentation` (도움말·문서) | 찾기 쉬운 도움말·구체 절차. | 필드 옆 도움말 툴팁·검색 가능한 가이드. | 도움말이 없거나 실제 화면과 불일치. |

- **UI 원칙과의 경계.** UX 휴리스틱 `consistency-standards`(일관성과 표준)와 UI 원칙 `consistency`(일관성)는 **계열이 다르다**(사용성 휴리스틱 vs 시각 디자인 원칙). 중복·상충 조정은 리뷰 게이트(사람 판정) 몫이며 체커 판정 대상이 아니다(바인딩 §7.2 (사) 상호 참조 주석).

---

**참고 문서 종료.** 위 내용은 전부 참고이며 강제 근거가 아니다. 강제는 Policy `designElements`·`designPrinciples`·`defaultRequiredSet`과 `design_completeness` 게이트, 규약은 바인딩 §7C·§7.2에 있다.
