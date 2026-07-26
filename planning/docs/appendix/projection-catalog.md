# planning/docs/appendix/projection-catalog — Projection 유형 예시 레지스트리 (비정본 부록)

성격: **비정본 부록 (Non-Canonical Appendix)** · 상위 규약: AGENT.md (INV-1)
근거 정본(§ 포인터만·재정의 0): `planning/specs/04-solution-design.md` §3.5(Projection — Contract=Source of Truth·파생·동적 선택)·§3.7(저장 스코프)·§3.8 SP-INV 5·7·9·§0(어휘 주의 D5) · 루트 `ARCHITECTURE.md` §8 UAF-INV ⑥ · `planning/ARCHITECTURE.md` §2(본 부록 비정본 등재).
**정책 값 정본**(기본 필수 세트·요건 클래스·제외 규칙): `uahf/framework/adapters/claude/solution-design-data/policy/default-policy.yaml` + `planning/adapters/claude/solution-design-binding.md` §7.2 (다). 본 부록은 값 사본을 두지 않는다.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 비정본 선언

정본은 `planning/specs/04-solution-design.md`뿐이며 본 부록은 참고 카탈로그다 — 계약·용어·강제 확정 0, 코어(04)는 본 부록을 알지 못하고(UAF-INV ⑥·SP-INV 5), 충돌 시 정본이 우선한다. 04 §3.5는 Projection을 **Contract=Source of Truth 하의 파생 산출**로만 정의하고 유형 목록을 **개방 레지스트리**로 두며 유형을 열거하지 않는다 — 본 부록이 그 격리 지점의 예시 보유다. 읽기 전에 04 §3.5·§3.7·§0을 먼저 이해해야 한다.

---

## §1. 목적·참조 축 (포인터만)

Solution Design이 산출할 수 있는 **Projection**(파생 산출 문서) 유형을 **예시**로 보인다. 아래 축의 정의는 전부 정본 소유이며 본 부록은 재정의하지 않는다.

- **Projection 관계.** Contract = Source of Truth → Projection = 파생, 동적 선택, 전 유형 강제 금지 — 04 §3.5.
- **워크스페이스 귀속.** 선택된 Projection 산출은 대상 프로젝트 워크스페이스에 귀속되고 Framework 상태를 오염시키지 않으며, 물리 배치·직렬화는 Adapter 소관이다 — 04 §3.7·§3.8 SP-INV 7·§4.
- **어휘 주의.** 통칭 "Draft/Final Contract"는 비정본 사용자 어휘이며 정본 표기가 아니다 — 04 §0(대응은 §3).

---

## §2. Projection 유형 예시 표 (비정본 개방 레지스트리)

아래 표는 파생될 수 있는 유형의 **예시**이며 강제 목록이 아니다 — 모든 프로젝트에 모든 유형을 강제하지 않고 유형·복잡도에 따라 필요한 유형만 동적 선택한다(04 §3.5). "언제 유용한가" 열은 규범이 아니라 예시적 조건이다.

| 유형(예시) | 1줄 목적 | 언제 유용한가(예시 조건) |
|---|---|---|
| PRD | 무엇을·왜 만드는지(요구·범위·성공 기준)를 서술한다. | 요구가 넓거나 이해관계자가 여럿일 때 |
| ARCHITECTURE | 시스템 구조·경계·주요 설계 결정의 지도를 제시한다. | 구성요소·경계가 여럿이라 구조 합의가 필요할 때 |
| ADR | 개별 설계 결정의 What/Why/Trade-off를 기록해 보존한다. | 되돌리기 어려운 결정·근거 추적이 중요할 때 |
| UI Guide | 인터페이스 설계 원칙·토큰·안티패턴을 담는다. | 사용자 인터페이스 표면이 있고 일관성이 중요할 때 |
| API Spec | 외부 계약(엔드포인트·입출력·오류)을 명세한다. | 외부·타 팀이 소비하는 인터페이스가 있을 때 |
| DB Schema | 데이터 모델·관계·제약을 정의한다. | 영속 데이터 모델이 복잡·핵심일 때 |
| Deployment | 배포·운영·환경 구성 지침을 제시한다. | 운영 환경·릴리스 절차가 비자명할 때 |

- **ADR 예시 세부.** What(무엇을 결정했나)·Why(왜)·Trade-off(어떤 대안을 어떤 비용으로 접었나)를 함께 보존하는 데 유용할 수 있다 — `Reconciling`에서 해소된 trade-off 결정(04 §3.4-D ③)을 결정 단위로 남길 자리가 필요한 프로젝트의 예시 선택지다.
- **UI Guide 예시 세부.** Design Principles·Design Tokens·Anti-patterns(예: "과도한 시각 효과 금지") 등을 담을 수 있다. 구체 내용은 대상 프로젝트가 정하며 본 부록은 담길 자리만 예시한다.

### 2.1 기본 필수 Projection 세트 (값 사본 없음 — 포인터)

성숙 경로의 **기본 필수 세트**(국내 SI 관행 문서 유형명 기반 **13종**)는 개방 레지스트리 중 default-required **부분집합**이다. **id·이름·요건 클래스의 값 정본은 `default-policy.yaml` `projectionSelection.defaultRequiredSet` + 바인딩 §7.2 (다)이며, 본 부록은 값 사본을 두지 않는다**(중복 사본이 실제로 종수 불일치를 낳았다 — 위 §9 2026-07-26 행). 부록은 이 세트를 표준화·등록·강제하지 않는다(§0).

- **요건 클래스 의미(설명 — 규칙 정본은 `requirementClasses`·`exclusionRule`·바인딩 §7.2 (다)).** `always` = 항상 default-required(제외는 명시 결정 + 사유 기록 + 사용자 확인) · `touchpoint` = 접점(웹·앱·포털) 선언 시 required · `interface` = 외부 연계 선언 시 required.
- **미선언 시 자동 N/A는 폐기됐다.** 접점·연계 미선언으로 `touchpoint`/`interface` 클래스가 전체 제외될 때 **조용한 자동 N/A는 금지**이며, 매니페스트 `classExclusions.<class>{reason,confirmedBy}`로 **표면화·사용자 확인**해야 한다(`exclusionRule.classExclusionOnNonDeclaration`·고임팩트 이탈). 침묵 누락(산출도 제외 기록도 없이 구현 경계 넘기)도 금지다(04 SP-INV 9).
- **여전히 강제 아님.** 기본 필수 세트는 **기본값(opt-out)**이며 정당화된 제외가 가능하다 — 개방 레지스트리 전체 유형을 강제하는 것과 다르다(04 §3.5). 정본(Policy)이 바뀌면 본 부록이 따른다.

---

## §3. 사용자 어휘 대응 (비정본 — D5 실현 지점)

| 통칭(비정본 사용자 어휘) | 정본 표기 대응(≈) | 정본 위치 |
|---|---|---|
| "Draft Contract" | Ready 인스턴스 vN | 04 §0·§3.1-B |
| "Final Contract" | superseding 성숙 인스턴스 v(N+1) | 04 §0·§3.1-C |

**주의.** 위 통칭은 정본 용어가 아니다. 성숙은 단일 문서의 상태 변경이 아니라 supersedes 계보에 의한 **완결 인스턴스의 재발행**이므로(04 §3.6·03 §3.4) "Draft→Final" 단일 문서 진화 은유는 정확하지 않다. 이 대응은 어휘 소통용이며 계약을 신설하지 않는다.

---

## §4. 이 부록이 확정하지 않는 것 (경계)

유형 표준·등록·강제 0 · 계약·불변·용어 신설 0("Draft/Final" 어휘 정본화 0·D5) · 전 유형 강제 0(동적 선택이 원칙) · 물리 배치·직렬화 확정 0(Adapter 소관·04 §4·§3.7) · **정책 값 확정 0**(값 정본 = 위 머리 포인터). 본 부록의 서술이 정본과 어긋나면 04와 Policy가 우선한다(§0).
