# Post-Tuning Improvement Backlog — v1.7 이후 프레임워크 개선 백로그

작성: Advisor · 2026-07-14 · 계획 전용(구현 0·커밋 0)
지위: `docs/performance-tuning-plan.md`(Core Performance Tuning)와 **명확히 분리**된 사용자/프레임워크 개선 백로그. 성능 튜닝 트랙에 혼입 금지 — 각 항목은 튜닝 완료·Baseline 재측정 후 독립 트랙으로 상정한다.
중복 방지: 기존 이월 인벤토리(`docs/next-session-prompt.md` v1.7 마감본·uahf-control-plane README 이월 절)와 겹치는 항목은 본 문서가 상위 프레이밍을 소유하고 개별 결함(not-found 404·GateEvent.state 정리 등)은 기존 이월 목록에 남긴다.

---

## A. User-facing Gate / Explanation UX

- **Problem / Motivation**: v1.7의 게이트 제시가 내부 전문용어(unitType·revision·basis·CP2 등)를 그대로 노출 — 사용자가 알아야 할 것은 「왜 멈췄나·무엇을 결정해야 하나·승인하면 무엇이 일어나나·추천과 이유」 4가지다.
- **Desired Outcome**: 게이트 제시 표면의 3층 분리 — Internal(원장 어휘) / Developer(현재 수준) / User-facing(결정 중심 요약+추천). 물리 게이트 의미론은 무변.
- **Why Not in Current Tuning Track**: 표현 계층 개선이며 성능 지표(A/B/C)와 무관 — 섞으면 튜닝 효과 측정이 오염됨.
- **Dependency**: 게이트 제시 채널 정본(OQ-PO-B1 제시 표면 문법·B3 headless 제시 브리지와 접점).
- **Suggested Future Track**: 「Gate Presentation UX」 소형 트랙(Control Plane의 게이트 뷰와 결합 가능).

## B. UI/UX Visual Contract

- **Problem / Motivation**: 사용자는 구현 전에 LLM이 최종 목표를 정확히 이해했는지 **눈으로** 확인할 수 있어야 한다. v1.7에서 Wireframe이 사용자 수정 요구로 사후 주입됐고, 톤앤매너는 침묵 디폴트됐다(mi-0107 Novel) — UI/UX 산출은 단순 디자인 산출물이 아니라 **요구 이해를 검증하는 Visual Contract**다.
- **Desired Outcome**: `Interview → Requirement Discovery → UX Flow/IA → Wireframe → UI Mockup → (필요 시) Interactive Prototype → User Validation → Final Approval → Autonomous TDD Implementation` 흐름을 성숙 run 프로토콜(04) 위에 UI 제품 유형의 표준 경로로 정식화. Discovery Eliciting에 제품 유형 함의 차원(시각 디자인 선호) 포함.
- **Why Not in Current Tuning Track**: 기능 확장(파이프라인 단계 추가)이며 성능 튜닝과 직교. 비용을 늘리는 방향이므로 튜닝 후 Baseline 위에서 가치·비용을 측정해야 함.
- **Dependency**: 성숙 run 호스팅(v1.7 실증 자산)·디자인 협업 라운드(사용자 관심 기표명)·Contract v2 open(실시간·Control과 별개).
- **Suggested Future Track**: 「Design Collaboration & Visual Contract」 — uahf-control-plane v2→v3 성숙 run을 파일럿으로.

## C. UI Design Principles (품질 기준)

- **Problem / Motivation**: 시각 산출물의 품질 기준(톤앤매너·레이아웃·접근성 원칙)이 정본에 없음 — v1.7은 shadcn 기본값으로 디폴트.
- **Desired Outcome**: UI/UX 산출물의 **품질 기준**으로서의 디자인 원칙(기능 추가 아님·특정 디자인 도구 기능의 UAHF 재구현 금지). Visual Contract(B)의 판정 기준 역할.
- **Why Not in Current Tuning Track**: 품질 기준 정의는 성능과 무관.
- **Dependency**: B와 동시 설계가 자연스러움.
- **Suggested Future Track**: B 트랙의 비정본 부록(카탈로그는 비정본 관례 준수 — expert-role 부록 선례).

## D. External Capability Reuse (예: dev-browser)

- **Problem / Motivation**: 웹 실동작 검증을 v1.7에서는 curl 마커 검사로 수행 — 실제 브라우저 렌더/상호작용 검증은 검증된 외부 도구(dev-browser류)를 재구현 없이 Adapter/Skill로 활용해야 한다(Reuse First의 프레임워크 차원 확장).
- **Desired Outcome**: 외부 capability의 표준 수용 경로(Adapter 경계·격리 지점) 정의 + 브라우저 검증 1종 파일럿.
- **Why Not in Current Tuning Track**: 신규 capability 도입(외부 도구 설치 포함)은 이번 금지사항이며 성능 병목도 아님.
- **Dependency**: Reuse First 원칙(튜닝 계획 §3에서 이번부터 적용)·Skill Routing(G).
- **Suggested Future Track**: 「External Capability Adapter」 — Control Plane E2E 검증을 파일럿으로.

## E. Execution Modes (Simple / Standard / Deep / Auto)

- **Problem / Motivation**: 작업 성격별로 파이프라인 깊이(검증 횟수·성숙 여부·게이트 수)를 조절하고 싶은 수요. **단, 비효율적 Core Pipeline을 그대로 둔 채 모드로 작업을 생략하는 방식은 금지** — 순서는 Core Tuning → Baseline 재측정 → 그 후 모드 분리.
- **Desired Outcome**: 튜닝된 파이프라인 위에서 모드별 정책 프로파일(Policy as Data — 임계·검증 깊이·게이트 구성)로 실현. 품질 보장 하한(게이트·독립 검증)은 모드와 무관하게 유지.
- **Why Not in Current Tuning Track**: 튜닝 전 모드 도입은 "생략으로 빨라짐"과 "구조 개선으로 빨라짐"을 구분 불가능하게 만들어 측정을 오염시킴.
- **Dependency**: T1~T6 완료·Before/After 확보.
- **Suggested Future Track**: 「Execution Mode Profiles」 — risk-based routing(T3)의 자연 확장.

## F. Information View Modes (Simple / Developer / Debug View)

- **Problem / Motivation**: Execution Depth와 별개로, 같은 실행을 보는 **정보 표면**의 깊이 선택이 필요(사용자 보고는 Simple, 개발 검토는 Developer, 원장 추적은 Debug).
- **Desired Outcome**: Control Plane 뷰 모드 + 주 세션 보고 표면의 계층화. A(게이트 UX)와 표면 계층을 공유.
- **Why Not in Current Tuning Track**: 표현 계층 — 성능 무관.
- **Dependency**: Control Plane MVP(실재)·A 항목.
- **Suggested Future Track**: Control Plane 확장 트랙에 흡수 가능.

## G. Global Skill Routing

- **Problem / Motivation**: 현재 UAHF는 CLI는 orchestration에서 적극 활용하나 Skill은 실행 자원으로 거의 미활용. 장기적으로 `Task → Capability 분석 → Role Routing → Model Routing → Skill Routing → Tool/CLI Routing → Execution`의 전 경로가 필요하다. **단 이번 Baseline의 직접 P0 병목은 아님**(1차 분석 §10 — Skill 부재로 인한 실측 손실은 검증기 재발명·게이트 resolve 3벌 중복 등이며, 이는 T3의 Reuse First로 우선 흡수).
- **Desired Outcome**: ① (즉시 — 튜닝 트랙에 이미 반영) Reuse First 원칙 상시화, ② (후속) capability→skill/tool 라우팅의 정식 스키마(allocation 3층의 확장 — 05 §3.4 인접 개방점)·Skill 카탈로그(v1.7 식별 후보: ledger-verify·gate-resolve·scaffold-install·run-report·memory-verify).
- **Why Not in Current Tuning Track**: 시스템 전체 설계가 필요한 Framework Capability이며, P0 병목 3종(통지·재검증·검증 라우팅)과 독립. 억지 편입 시 튜닝 트랙 비대화.
- **Dependency**: T3 Reuse Assessment 산출물(기존 자산 커버리지 맵)이 Skill 카탈로그의 씨앗.
- **Suggested Future Track**: 「Skill & Capability Routing」 Framework Capability Track — T3 완료 후.

---

## 실사용 Dogfooding Evidence (2026-07-14 — 사용자 직접 사용·확인 실측)

v1.7 산출물(uahf-control-plane)을 **사용자가 실제로 사용하며 발견한** 문제들 — 본 백로그 A~G의 실측 근거로 보존한다. 이번 성능 튜닝 트랙에서는 구현·수정하지 않는다. 물리 흔적(consumer 저장소 워킹트리 미커밋 변경 — EventTimelinePanel.tsx key 수정·check-error.js·package.json)은 **그대로 보존** 방침 확정(2026-07-14 사용자 승인·앵커 dd2fd73 무결).

| # | 발견 (사용자 실측) | 물리/기록 증거 | 연결 |
|---|---|---|---|
| 1 | Interview/Requirement Discovery가 얕음 — 최종 사용 목적·실사용 경험 질문 부족, 질문·설명이 내부 프레임워크 용어 중심 | greenfield-r003 질문 8건(스택·뷰·리스크 중심) | A·B |
| 2 | UI/UX 사전 협의 부족 — 디자인 방향·톤앤매너 협의 부재, UI 라이브러리 기본 스타일이 암묵 디폴트 | mi-0107(Novel)·shadcn 기본 토큰 적용 | B·C |
| 3 | Wireframe과 최종 구현 화면의 상당한 괴리 — 구현 전 최종 결과에 가까운 Mockup 미확인(대형 프로젝트였다면 재개발 비용) | maturation-r003 Wireframe vs 실제 렌더 | B |
| 4 | Visual Contract 부재 — 사용자가 승인한 시각 결과와 실제 구현을 연결하는 계약 없음 | 상동 | B·C |
| 5 | 실제 Runtime/Browser 검증 부족 — **상세 화면에서 실제 오류 발생**(React key 중복) | consumer 워킹트리: EventTimelinePanel.tsx key 수정 흔적(`kind-seq`→`runId-kind-seq-idx`)·**사용자 작성 check-error.js**(Playwright 콘솔 오류 검사) | D |
| 6 | 완료 판정 한계 — build pass·curl·정적 마커로는 UI 제품 완료 증명 불가. 필요: 실제 실행→브라우저 접속→핵심 User Journey→렌더/전환/상호작용→콘솔·런타임 오류→Visual Contract 대조 | 상동 + w run AC 구성(빌드·마커 중심) | B·D |
| 7 | Skill/외부 capability 활용 부족 — 반복 검증·브라우저 검증에 기존 도구 미활용 | 1차 분석 §10 | D·G |

**Post-Tuning 잠정 우선순위(사용자 확정 2026-07-14)**: 1순위 **B+C**(Design Collaboration & Visual Contract — Interview→Discovery→UX Flow/IA→Wireframe→Mockup→(필요 시)Prototype→User Validation→Final Approval→Autonomous TDD) → 2순위 **D**(Real Runtime/Browser/User Journey Validation — TDD/Unit→Build→실행→브라우저→Journey→렌더/상호작용/콘솔→Visual/Behavioral Contract 대조→완료 판정) → 3순위 **G**(Global Skill & Capability Routing) → 4순위 **A+F**(User/Developer/Debug 표현 계층) → 5순위 **E**(Execution Modes — Core 튜닝·재측정 후 Policy as Data로만).

## 우선 관계 요약

```
[성능 튜닝 트랙 T0~T7]  ← 지금
   └→ T3 Reuse Assessment 산출물 ──┐
[Baseline 재측정 (T6~T7)]           │
   └→ E(Execution Modes) 선행 조건   │
[Post-Tuning]                        ▼
   A(게이트 UX) ·F(View Modes) → Control Plane 확장과 결합
   B(Visual Contract)+C(Design Principles) → v2→v3 성숙 run 파일럿
   D(External Capability)·G(Skill Routing) → Framework Capability Track
```
