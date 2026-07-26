# planning/docs/appendix/visual-contract-catalog — Visual Contract 요소 작성 가이드 (비정본 부록)

성격: **비정본 부록 (Non-Canonical Appendix)** · 상위 규약: AGENT.md (INV-1)
근거 정본(§ 포인터만·재정의 0): `planning/adapters/claude/solution-design-binding.md` §7.2 (다)·(바)·(사)·§7A.1·§7C · `uahf/framework/adapters/claude/solution-design-data/policy/default-policy.yaml`(`designElements`·`designPrinciples`·`defaultRequiredSet` 실값) · `orchestration/adapters/claude/design_completeness.py`·`design-manifest.schema.md`(결정적 게이트·매니페스트 스키마) · `planning/specs/04-solution-design.md` §3.9·§3.4 `Validating`·§3.8 SP-INV 5·9 · 루트 `ARCHITECTURE.md` §6 원칙 11·§8 UAF-INV ⑥.
**요소·원칙 목록의 값 정본은 위 Policy yaml + 바인딩 §7.2이며, 본 부록은 값 사본(요소 목록·요지 문면)을 두지 않는다** — 본 부록이 담는 것은 "어떻게 잘 만드는가"의 방법·예/반례뿐이다.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 비정본 선언·강제와 참고의 분리

정본은 바인딩(§7.2·§7C)·Policy(`designElements`·`designPrinciples`)·게이트(`design_completeness`)이며 본 부록은 참고 카탈로그다 — 계약·용어·강제 확정 0, 코어(04)는 본 부록을 알지 못하고(UAF-INV ⑥·SP-INV 5), 충돌 시 정본이 우선한다. 빠지면 안 되는 것(요소 커버·요소 단위 제외 사유 기록)은 **Policy + 게이트**가 강제하고(책임 있는 자율 (a)), 본 부록은 "**어떻게 잘 만드는가**"만 제공한다 — 여기의 어떤 항목도 게이트 통과 조건이 아니다(게이트는 covered/정당화 excluded 선언 완전성만 본다).

---

## §1. projectScope 요소 작성 가이드 (프로젝트 단위 1회)

요소 id·필수 여부의 정본은 Policy `designElements.projectScope`다. 아래는 각 요소를 **잘 만드는 법**과 커버 앵커 예시(`pointer`)뿐이다.

| 요소 id | 잘 만드는 법(참고) | 커버 앵커 예시 |
|---|---|---|
| `design-tokens-values` | 하드코딩 값을 토큰 이름으로 승격(예: `color.primary`, `space.4`, `radius.md`). 팔레트·타입스케일·스페이싱 스케일을 표로 고정. | `docs/design-tokens.md#values` |
| `tone-and-manner` | 톤 축(예: 정보 밀도 高↔低, 뉘앙스 정적↔활기)에서 선택값을 명시. 레퍼런스는 링크 앵커만 인용(정본은 리포 텍스트). "하지 말 것"(금지 목록)을 함께 적어 drift를 막는다. | `docs/design-tokens.md#tone` |
| `accessibility-floor` | 본문/큰 텍스트 대비 기준, 키보드 포커스 가시성, 최소 터치 타겟 크기를 수치로 고정. 최소선이므로 "이보다 낮으면 실패"의 하한만. **criteria 실값은 Policy에**(바인딩 §7.2 (바)). | `docs/design-tokens.md#a11y` |
| `user-journey-map` | 대표 태스크 2~3개의 시작점·단계·완료 조건·이탈점을 단계 흐름으로 정리. | `docs/user-journey.md` |

- **디자인 토큰이 mock의 소비 정본이다.** `screen-mock`(HTML)은 이 토큰 실값을 소비해 생성된다(바인딩 §7C.2). 토큰 변경은 토큰 갱신 → mock 재생성이지, mock 직접 수정이 아니다.

## §2. screenScope 요소 작성 가이드 (각 화면이 커버)

| 요소 id | 잘 만드는 법(참고) |
|---|---|
| `layout-structure` | 화면을 영역(헤더/사이드/본문/푸터 등)으로 구획하고 그리드 컬럼을 명시. 와이어프레임과 1:1 대응. |
| `navigation` | GNB/LNB 등 위치, 이 화면으로의 진입 경로와 이탈(다음 화면) 경로를 화면 흐름도와 연결. |
| `component-states` | 상태를 갖는 컴포넌트마다 5종(기본·로딩·빈·오류·비활성)을 모두 정의. "빈 상태"·"오류 상태"를 특히 빠뜨리지 않는다. |
| `data-rules` | 목록 기본 정렬 키, 페이지 크기, 날짜·통화·수치 포맷을 기능 명세와 연결. |
| `responsive` | 최소 1개 브레이크포인트에서의 레이아웃 변화(예: 사이드 접힘)를 명시. |
| `error-recovery` | 실패 상태에서 어디로·어떻게 복구하는지(재시도·이전 단계·홈)를 명시. |
| `feedback-rules` | 각 결과를 어떤 방식(토스트·인라인·모달)·지속시간으로 알리는지 규칙화. |

**요소 경계(중복 오해 방지).** `component-states`(상태 화면의 **존재**) / `feedback-rules`(알림·피드백 **방식**) / `error-recovery`(복구 **경로**)는 서로 다른 축이다 — 한 화면이 세 요소를 각각 별개로 커버한다.

- **요소 단위 제외.** 특정 화면에서 어떤 요소가 해당 없을 때(예: 정적 안내 화면의 `data-rules`)는 조용히 빠뜨리지 말고 매니페스트에서 `{"status":"excluded","reason":"...","confirmedBy":"..."}`로 사유+확인을 기록한다(Policy `designElements.exclusionRule.silentOmission=금지`·게이트 강제). 이것이 "책임 있는 자율 (b)"의 요소 층 실현이다.

### §2a. 인터뷰 표면화 시 편입 항목 (기본 필수 아님 — 제품 의존)

아래 항목은 **제품 의존적**이라 기본 필수 세트에 넣지 않는다(넣으면 형식적 제외 기록만 양산·사용자 결정 2026-07-19). **인터뷰·설계에서 필요가 선언되면** 그때 편입한다.

- **편입 절차(Policy as Data·프레임워크 무변경).** 필요가 선언되면 **해당 프로젝트의 policy 사본** `designElements.projectScope`/`screenScope`에 요소를 **데이터로 추가**한다 → 그 프로젝트에서만 required가 된다. 기존 `touchpoint`/`interface` 선언-조건부 패턴과 동형이며(선언 시 required·미선언 시 비적용) 프레임워크 기본 정책·체커·게이트는 변경하지 않는다.

| 편입 후보 | 무엇을 | 언제 편입 |
|---|---|---|
| `onboarding-flow` | 온보딩·첫 사용 흐름(초기 설정·빈 상태 유도) | 첫 사용 경험이 제품 성패에 중요하다고 선언될 때 |
| `user-types` | 사용자 유형·권한 상세(역할별 목표·권한) | 다중 역할·권한 분기가 선언될 때 |
| `ux-copy` | UX 카피 규칙(오류 메시지 형식·톤·빈 상태 안내문) | 카피 일관성·보이스톤이 요구로 선언될 때 |
| 다국어(i18n) | 다국어·로케일 규칙(번역 키·방향성·포맷) | 다국어 지원이 요구로 선언될 때 |

(참고 후보이며 강제 세트가 아니다. 편입 여부·시점은 인터뷰·설계 판단과 사용자 확인 몫이다.)

## §3. Visual Contract 산출물 3종 작성 가이드

산출물 id·요건 클래스의 정본은 Policy `defaultRequiredSet`·바인딩 §7.2 (다)다.

| 산출물 id | 잘 만드는 법(참고) |
|---|---|
| `design-tokens` | §1의 projectScope 요소를 담는 단일 문서. mock 생성의 입력 정본. |
| `screen-mock` | 확정 와이어프레임 + 토큰을 소비한 **클릭 가능 자기완결 HTML**. 파생 뷰이므로 정본(설계+토큰) 갱신 후 재생성(§7C.2). 브라우저 직접 열람 또는 Artifact 발행(선택·§7C.5). |
| `mock-convergence-record` | 사용자 수렴 종료 기록 — **확인자·라운드 수·잔여 피드백 0**. 이 산출이 구현 진입 자격의 표식(§7C.4). |

## §4. mock 수렴 진행 (참고 — 규약 정본은 바인딩 §7C)

1. 기획 산출물 확정 → 대표 1화면 × 톤 3안 제시(§7C.3).
2. 사용자 선택·피드백 → `design-tokens` 확정.
3. 잔여 화면 일괄 생성(확정 토큰 소비).
4. 피드백(예: "GNB/LNB 추가·가입 스텝 변경")은 **정본 설계 산출물 먼저 갱신 → mock 재생성**(mock 직접 수정 금지·§7C.2).
5. 잔여 피드백 0 → `mock-convergence-record` 산출 → 구현 오케스트레이션 진입(`design_completeness` 최후 방어).

---

## §5. UI 디자인 원칙 해설 — 적용 예/반례 (참고)

**강제 지점(라우팅).** 원칙의 강제는 본 부록이 아니라 (1) Policy `designPrinciples`(값·요지 정본 = `default-policy.yaml` (사)·바인딩 §7.2 (사)), (2) 디자이너 브리프 주입 + 화면설계서 원칙별 근거 기록(바인딩 §7A.1·brief-template `{DESIGN_PRINCIPLES}` 슬롯), (3) mock 수렴 리뷰 차원 대조(바인딩 §7C.3a), (4) 접근성 기계 판정분(Policy `accessibility-floor.criteria`·바인딩 §7.2 (바))에 있다. 본 절은 해설·예/반례만 제공한다(강제 근거 아님·SP-INV 5).

출처(참고 앵커): https://www.figma.com/ko-kr/resource-library/ui-design-principles/ (아래 예/반례는 자체 서술이며 원문 전재가 아니다). 각 원칙의 **요지 문면(`gist`)은 Policy가 소유하므로 여기서 재기재하지 않는다**.

| id (읽기용 라벨) | 적용 예 | 반례 |
|---|---|---|
| `hierarchy` (계층 구조) | 페이지 제목 24pt bold, 섹션 제목 18pt, 본문 14pt로 스캔 순서가 자명. | 모든 텍스트가 같은 크기·두께라 어디를 먼저 볼지 알 수 없음. |
| `progressive-disclosure` (점진적 공개) | 가입을 3스텝으로 나누고 "2/3" 진행 표시. | 한 화면에 20개 필드를 한꺼번에 요구해 이탈 유발. |
| `consistency` (일관성) | 저장 버튼이 모든 화면에서 우하단·같은 색. | 화면마다 기본 버튼 색·위치가 달라 학습이 무효화됨. |
| `contrast` (대비) | 주요 CTA만 채움 버튼, 보조는 외곽선 버튼. | 삭제·저장이 같은 회색이라 위험 동작이 구분 안 됨. |
| `accessibility` (접근성) | 본문 대비 4.5:1 이상·키보드 포커스 링 표시·터치 타겟 44px. | 연회색 위 흰 글씨(대비 2:1)·포커스 표시 제거. |
| `proximity` (근접성) | 라벨과 입력 필드를 붙이고 그룹 간 간격을 넓힘. | 라벨이 엉뚱한 필드에 붙어 보이도록 균일 간격 배치. |
| `alignment` (정렬) | 폼 라벨·입력이 좌측 정렬 그리드에 맞춰 정돈. | 요소마다 들쭉날쭉한 좌표라 시선이 흩어짐. |

- **원칙 위반의 소화 경로.** mock 리뷰에서 위반이 발견되면 mock을 직접 고치지 말고 **정본 설계 산출물(화면설계서·토큰)을 갱신 → mock 재생성**한다(바인딩 §7C.2·§7C.3a). 본 표의 예/반례는 판단 보조일 뿐 게이트 판정 기준이 아니다.

---

## §6. UX 사용성 휴리스틱 해설 — 적용 예/반례 (참고)

§5와 **동일 라우팅**으로 강제된다(강제 지점 = Policy `designPrinciples` + 브리프/리뷰 배선). 출처(참고 앵커): https://www.nngroup.com/articles/ten-usability-heuristics/ (아래는 자체 서술·원문 전재 아님). 요지 문면은 Policy 소유.

| id (읽기용 라벨) | 적용 예 | 반례 |
|---|---|---|
| `visibility-of-system-status` (상태 가시성) | 업로드 진행률 바·"저장됨" 표시. | 버튼을 눌러도 아무 반응이 없어 재클릭 유발. |
| `match-real-world` (실세계 일치) | "장바구니"·"결제" 같은 친숙어 사용. | "트랜잭션 커밋" 같은 내부 용어를 UI에 노출. |
| `user-control-freedom` (제어와 자유) | 삭제 후 "실행 취소" 스낵바. | 확인 없이 즉시 영구 삭제되고 복구 불가. |
| `consistency-standards` (일관성과 표준) | 파괴적 동작은 항상 빨강·확인 요구. | 화면마다 "확인/취소" 버튼 좌우 순서가 뒤바뀜. |
| `error-prevention` (오류 예방) | 날짜 선택기로 잘못된 형식 입력 차단. | 자유 입력만 두고 형식 오류를 사후 거부. |
| `recognition-over-recall` (회상보다 인지) | 최근 선택·자동완성 제시. | 이전 화면의 코드값을 외워 다시 입력하게 함. |
| `flexibility-efficiency` (유연성과 효율) | 숙련자용 키보드 단축키·일괄 작업. | 모든 사용자가 매번 같은 다단계만 강제됨. |
| `aesthetic-minimalism` (미니멀리즘) | 핵심 지표만 대시보드 상단에. | 한 화면에 모든 옵션을 나열해 핵심이 묻힘. |
| `error-recognition-recovery` (오류 인식·복구) | "비밀번호는 8자 이상이어야 합니다" + 입력 포커스. | "오류 코드 0x5" 만 표시하고 해결책 없음. |
| `help-documentation` (도움말·문서) | 필드 옆 도움말 툴팁·검색 가능한 가이드. | 도움말이 없거나 실제 화면과 불일치. |

- **UI 원칙과의 경계.** UX 휴리스틱 `consistency-standards`와 UI 원칙 `consistency`는 **계열이 다르다**(사용성 휴리스틱 vs 시각 디자인 원칙). 중복·상충 조정은 리뷰 게이트(사람 판정) 몫이며 체커 판정 대상이 아니다(바인딩 §7.2 (사) 상호 참조 주석).
