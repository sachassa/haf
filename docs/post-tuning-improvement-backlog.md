# Post-Tuning Improvement Backlog — v1.7 이후 프레임워크 개선 백로그

작성: Advisor · 2026-07-14 · 계획 전용(구현 0·커밋 0)
지위: `docs/performance-tuning-plan.md@cd9247b`(Core Performance Tuning · 산출물 수명 정책에 따라 아카이브 — 열람: `git show cd9247b:docs/performance-tuning-plan.md`)와 **명확히 분리**된 사용자/프레임워크 개선 백로그. 성능 튜닝 트랙에 혼입 금지 — 각 항목은 튜닝 완료·Baseline 재측정 후 독립 트랙으로 상정한다.
중복 방지: 기존 이월 인벤토리(`docs/next-session-prompt.md@ad451ee` v1.7 마감본 — 현행 핸드오프 = `docs/session-handoff.md`·uahf-control-plane README 이월 절)와 겹치는 항목은 본 문서가 상위 프레이밍을 소유하고 개별 결함(not-found 404·GateEvent.state 정리 등)은 기존 이월 목록에 남긴다.

**등재 형식 규율 (2026-07-26 신설 — AGENT.md §Invariants 「강제 없는 규율 신설 금지」 운용)**: 신규 항목(`## X.` 헤딩)은 **「강제 지점」 행**을 포함한다 — 기계 강제 지점(게이트·훅·체커)을 명시하거나, 미도입이면 그 사유를 항목 안에 기록한다. 등재는 본 파일이 원장이다 — 핸드오프 갱신 블록에만 기록된 "신설"은 등재가 아니다(P·Q·R 전입 경위 참조). 물리 강제 = `.claude/hooks/binary_state_guard.py`(본 파일에 「강제 지점」 행 없는 신규 항목 헤딩을 추가하는 쓰기를 차단).

---

## A. User-facing Gate / Explanation UX

- **Problem / Motivation**: v1.7의 게이트 제시가 내부 전문용어(unitType·revision·basis·CP2 등)를 그대로 노출 — 사용자가 알아야 할 것은 「왜 멈췄나·무엇을 결정해야 하나·승인하면 무엇이 일어나나·추천과 이유」 4가지다.
- **Desired Outcome**: 게이트 제시 표면의 3층 분리 — Internal(원장 어휘) / Developer(현재 수준) / User-facing(결정 중심 요약+추천). 물리 게이트 의미론은 무변.
- **Why Not in Current Tuning Track**: 표현 계층 개선이며 성능 지표(A/B/C)와 무관 — 섞으면 튜닝 효과 측정이 오염됨.
- **Dependency**: 게이트 제시 채널 정본(OQ-PO-B1 제시 표면 문법·B3 headless 제시 브리지와 접점).
- **Suggested Future Track**: 「Gate Presentation UX」 소형 트랙(Control Plane의 게이트 뷰와 결합 가능).

## B. UI/UX Visual Contract [해소 2026-07-19]

- **해소 2026-07-19 (Visual Contract 트랙)** — 정본 = `uahf/framework/adapters/claude/solution-design-binding.md` §7A·§7C(mock 수렴 규약) + policy 데이터(`designElements` 11종 · 필수 산출물 3종). 상세 경위·검증 근거 = git 앵커 `90ca19c`(본 파일 해소 서술). **잔여(미해소)**: Discovery Eliciting 시각 선호 차원 · Interactive Prototype(조건 발동형) · 실 파일럿(다음 소비 프로젝트). **강제 지점**: 코드 — `design_completeness` 요소 검사(fail-closed) + policy 필수 산출물 데이터.

## C. UI Design Principles (품질 기준) [해소 2026-07-19]

- **해소 2026-07-19 (Visual Contract 트랙)** — 정본 = policy `designPrinciples` 17종(Figma UI 7 + Nielsen UX 10) + `solution-design-binding.md` §7A.1·§7C.3a + accessibility-floor criteria 실값(WCAG AA). 해설 카탈로그는 비정본 부록 유지. 상세 = git 앵커 `90ca19c`. **강제 지점**: 코드 — 디자이너 브리프 주입 + `design_completeness` 근거 기록 검사.

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

## H. Continuous Telemetry / Lifecycle Observability (사용자 지시 등재 2026-07-14 — 기록만·구현 보류)

- **Problem / Motivation**: 현행 성능 측정 인프라는 **단발성 분석/벤치마크·orchestration run 중심**이다 — invoke 원자료 자동 기록은 CLI invoker 경유 orchestration run에 한정(`LoggingClaudeInvoker`), `collect_metrics.py`는 수동 실행, run-metrics/aggregate는 자동 누적되지 않으며, Interview/Discovery는 원자료 부재(CLI invoker 미경유·해당 데이터 트리에 실행 코드 0), 주 세션·하네스 서브에이전트는 하네스 미노출(불가). **UAHF 전체 실사용 lifecycle의 지속적 누적 관측은 아직 완성되지 않았다.**
- **Desired Outcome**: UAHF를 실제로 사용하면서 성능 데이터를 지속 누적하고, **충분한 실사용 데이터에서 반복 관찰되는 병목을 근거로** 성능 튜닝을 재개할 수 있는 관측 기반. 가능하면 전체 lifecycle을 관측 범위로 검토: `/new·/continue → Entry/Bootstrap/State Resolution → Discovery/Interview → Contract/Design → Orchestration → Worker/Verifier/CP2/Retry/Gate → Handoff/Closing`.
- **후보 방향(검토 대상·미확정)**: **Telemetry Session Skill**(lifecycle/trace 관리) + **deterministic script/CLI**(결정적 기록·집계)의 이원 구조. 기존 invoke 원자료·`collect_metrics.py`·run-metrics 구조를 최대 재사용.
- **불변 요구(설계 제약)**: 추가 LLM 호출 0 · 측정 실패가 본 작업을 실패시키지 않음(failure isolation — 섀도 장치 선례 `_orch_common.py`의 try/except→error 기록 패턴) · 원자료 보존·사후 재집계 가능 · measured/derived/unavailable(확인/계산/불가) 등급 구분 유지.
- **미해결 질문(향후 별도 설계에서 결정)**:
  1. 집계 경계 — orchestration run 종료 vs commit vs 전체 lifecycle trace. (2026-07-14 조사 실측: run 완주의 유일 결정 신호 = 러너 `result.completed` 분기[`run_k.py:67-69`·`run_orchestration.py:69-71`]; `collect_run(run_dir)` 단일-run 빌더 기존재; **함정 — `collect_metrics.main()`은 aggregate.run-metrics.json을 무조건 덮어써[:699-707] 순진한 자동 호출은 baseline aggregate를 파괴.**)
  2. `/new`·`/continue`에서 telemetry lifecycle을 자동/필수로 시작하는 방식 — 단 Entry 명령 자체 탑재는 부적합(EN-INV 1·2 — 관측만·정지), lifecycle 연결 지점의 별도 정의 필요.
  3. 세션 비정상 종료·`/continue` 재개·복수 orchestration run·복수 commit을 **하나의 trace로 연결**하는 의미론.
  4. 주 세션·하네스 서브에이전트(하네스 미노출 — 불가 항목)·Interview/Discovery(원자료 부재)의 커버 방법 — CLI 호스팅화 등 구조 변경 선행 필요 여부.
  5. step-data(형태 B step 호스팅) 동형 이식 — `run_host.py:125` 동형 완주 분기 실재하나 collect_metrics는 orchestration-data 전용(경로 배선 별도).
- **Why Not Now**: Core Performance Tuning 종료 결정(2026-07-14 — T6/T7 미실시·측정 인프라 유지·실사용 누적·병목 재관찰 시 별도 트랙 재개)에 따라 **지금은 기록만 남긴다.** 최소 연결(러너 완주 분기 자동 집계)도 구현 보류(사용자 결정 2026-07-14).
- **Dependency**: T1 산출물(collect_metrics·run-metrics·bundle_payload 지표)·invoke 원자료 스키마·(Skill 방향 채택 시) G(Skill Routing)와 접점.
- **Suggested Future Track**: 「Continuous Telemetry / Lifecycle Observability」 독립 개선 트랙. 재개 트리거 = 실사용 병목 반복 관찰(Measurement First — 느낌 기반 재개 금지). 기존 확정 우선순위(B+C→D→G→A+F→E)에는 미배정 — 순위 편입은 사용자 결정.

## I. 다라운드 심의 라이브 대화형 호스팅 (사용자 지시 등재 2026-07-19 — 기록만·트랙 후보)

- **Problem / Motivation**: 현행 다라운드 심의는 **형태 A 서면 왕복**이다 — 각 라운드가 fresh-context 서브에이전트 재소환이고, "전문가가 서로의 Proposal을 검토·반응"(04 §3.4-C)은 **브리프에 동료 Proposal을 동봉**하는 방식으로, 충돌 감지·중계는 Advisor(주 세션)가 규약 절차로 수행한다(solution-design-binding §7B — 실행 호스팅은 04 §3.9 확장 포인트로 의도적 미설계·§6.1 line 200). **사용자의 원래 설계 방향은 에이전트 간 라이브 대화형 심의**였다 — 서면 왕복은 라운드당 재소환·중계 오버헤드가 있고, 실시간 상호 반박·즉석 수렴의 심의 밀도가 낮다. 실측 선례: cheongryong-bubble maturation-r001(2026-07-19) — 라운드 1(4역할 병렬) → 독립 검증자 교차 검출 → 라운드 2 서면 재제안의 Advisor 중계 패턴.
- **Desired Outcome**: 04 §3.9 확장 포인트(Expert Role 실행 호스팅)의 **호스팅 설계**로서 라이브 대화형 심의를 도입 — 역할 에이전트들이 하나의 심의 세션(또는 상호 메시징)에서 Proposal을 직접 교환·반박·수렴. **계약은 유지, 호스팅만 교체**: 심의 의미론(04 §3.4 상태·전이 T3~T7·수렴 Guard)·게이트(Validating·SP-INV 4)·원장(append-only events·StateTransition 기록)·Policy(deliberation.maxRounds·convergence·peerVisibility)는 무변이며, §7B 규약 절차 층의 "브리프 동봉 서면 왕복" 실현만 라이브 호스팅으로 대체된다(structure.md §7 C-1 동형 — 형태 A→호스팅 전환에도 Core Contract 변경 0).
- **Why Not Now**: 실행 호스팅은 04 §3.9가 의도적으로 미설계로 유보한 확장 포인트이며(§6.1 "새 병렬 실행 프레임워크 창설 0"), 라이브 호스팅은 새 실행 인프라(에이전트 간 대화 채널·심의 세션 관리·원장 기록 브리지) 설계가 필요한 Framework Capability다. 현행 형태 A는 동작 실증됨(maturation-r001) — 교체는 비용·효과 측정 위에서.
- **Dependency**: 04 §3.9(확장 포인트 정본)·solution-design-binding §6·§7B(현행 form-A 규약 — 교체 대상 층)·환경의 멀티에이전트 대화 capability(에이전트 간 메시징/공유 세션) 가용성·G(Skill & Capability Routing)와 접점. 원장 기록(§4 레코드 어휘)은 라이브 심의 중에도 유지되어야 함(라운드·전이 재구성 가능성 보존).
- **Suggested Future Track**: 「Live Deliberation Hosting」 — 호스팅 계층 교체 트랙. 기존 확정 우선순위(B+C→D→G→A+F→E)에는 미배정 — 순위 편입은 사용자 결정(H 선례 동형).

## J. 오케스트레이션 에스컬레이션 해소·재작업 경로 (실측 등재 2026-07-20) [해소 2026-07-26]

- **해소 2026-07-26** — Desired ①(모든 정지 사유에서 stop-signal 일관 갱신)·②(해소→재작업 재진입·해소 1건 = 추가 시도 1회) 정본 = `orchestration/adapters/claude/project-orchestration-binding.md` §3.4 · Desired ③(단위 규모 대비 타임아웃) = 같은 binding §5.8 (g)(§L Desired 4 와 공통 구현) · `recover_gate --gate-id`(다중 pending 특정 지목) = §3.2·§3.4. 상세 경위·실측 근거(재발 실측 2건·`gate_id` 부재 좌표·`--retry-limit` 무효 실측·거버넌스 충돌 판정)는 git 앵커 `90ca19c` 보존 — 본 파일 해소 서술 + `docs/backlog-k-delegation-b-ledger.md` §5-A + `docs/rca-prescriptions-ledger.md` W-J(둘 다 `ARCHIVE.md` 등재·같은 앵커). **강제 지점**: 코드(엔진 게이트 발급·런처 stop-signal 기록·`resolve_gate`·테스트).

---

## K. Solution Design 성숙 시 Projection 정본 포인터 갱신 누락 (실측 등재 2026-07-21) [해소 2026-07-26]

- **해소 2026-07-26 (Desired ③)** — 정본 = `orchestration/adapters/claude/design-manifest.schema.md` §Contract 포인터 정합 규칙(`design_completeness` 체커 — 산출물의 최고 Contract 참조 == 계보 현재 인스턴스 · 미달=stale · 초과=dangling · 판독 실패=차단 · 이탈 채널 `contractRefPinned{reason,confirmedBy}`). Desired ①(성숙 경로 강제)·②(간접 참조)는 미도입 — 사유 = 04 spec 개정 거버넌스 무게·append-only 인용 관행 전면 변경(원 사유 문면 = git 앵커 `90ca19c`). 상세 = 같은 앵커. **강제 지점**: 코드 — `resolve_gate` task_added 승격 직전 fail-closed + `pretooluse_design_guard` 백스톱(동일 코드 재사용) + scaffold 미러 상속.

---

## L. Run Observability — Heartbeat · Failure Record · 종료코드 규약 (등재 2026-07-21) [해소 2026-07-26]

- **해소 2026-07-26** — Desired 1(`logs/heartbeat.json`)·2(`logs/failure.json` 6필드·재raise)·3(종료코드 규약 `0`=완료/`2`=게이트 정지/그 외=실패)·4-b(`fold_slug` 48자+sha8)·5(`--resume` 부재 오류의 실존 후보 목록 + `uaf-implement.md` §2 예시 정정) 정본 = binding §5.8 · Desired 4(per-unit timeout — impl-plan 선택 `timeout` 키 + 검증 게이트 fail-closed + `UnitTimeoutInvoker` 재기입) = binding §5.8 (g). 상세 경위·계약 필드 확정 사유(heartbeat 필드가 원 문면과 다른 이유 포함)는 git 앵커 `90ca19c` 보존(본 파일 해소 서술 + `docs/rca-prescriptions-ledger.md` W-L + `docs/backlog-k-delegation-b-ledger.md` §5-A). **잔여 관측 좌표**: 실 LLM run 에서 단위 예산 재기입 실증. **강제 지점**: 코드(런처·컴파일러·검증 게이트·래퍼 invoker·테스트).

---

## M. 횡단 결함 검지 — Cross-Unit Defect Sweep (실측 등재 2026-07-21) [해소 2026-07-26]

- **해소 2026-07-26 (Desired 2·3 + Desired 1 의 기계 부분)** — 정본 = binding §5.8 (h)(milestone done AC 의 단위 간 계약 정합 검사 최소 1건 의무 · 런처 `[REWORK-NOTE]` · 신규 form-B `sweep_units.py` 읽기 전용 스윕). Desired 1 의 자동 되돌림 미도입 — 사유: 결함 패턴 추출은 내용 판단이라 엔진 소유 불가(PO-INV 1)·Passed 단위의 기계 되돌림은 fold 상태 어휘 변경 필요. 재심 좌표 = Verifier 구조화 verdict 도입 시(§R 계열). 상세 = git 앵커 `90ca19c`. **강제 지점**: 코드(런처 관측·도구·테스트) + Planner 프롬프트 층(밀스톤 의무) + CP2 Verifier AC 적정성 축(§O 와 결합).

---

## N. 조건부 승인의 하류 전달 배선 부재 (실측 등재 2026-07-21) [해소 2026-07-26]

- **해소 2026-07-26 (Desired 1)** — 정본 = binding §3.3(구조 게이트 해소의 비공백 `--response` → 승격 payload 사본의 `delegation.context` 조건 주입 · `impl-plan.json` 바이트 무변조 · 주입 불가 형 = 원장 append 전 비영 종료 · `[CONDITION]`/`[CONDITION-NOTE]` 관측). Desired 2 미도입 — 사유: 05 §3.3 게이트 어휘 개정 거버넌스 무게이며 Desired 1 이 조건의 물리 도달을 성립시킨다. Desired 3 미도입 — 사유: 채널 신설로 수기 편집 관행의 필요가 소멸(명문화는 원장 밖 편집을 정당화하는 역효과). 상세 = git 앵커 `90ca19c`. **강제 지점**: 코드(주입 불가 형 fail-closed·관측 출력·테스트).

---

## O. AC 실출력 픽스처 규율 · 자기출제 구조 (실측 등재 2026-07-21) [해소 2026-07-26]

- **해소 2026-07-26 (Desired 1 + 2 최소형 + 3 수행)** — 정본 = seed 프롬프트의 실출력 픽스처 규율(외부 도구 호출 단위는 실출력 캡처 픽스처를 고정하고 AC 가 소비 · 이진: 캡처했거나 완료 보고에 「미검증 외부 계약」으로 신고했거나) + CP2 Verifier 역할 브리프의 AC 적정성 판정 축(`claude_invoker._ROLE_BRIEFS` — 합성 대체 여부·assert 실값·"통과가 판별력 있는 증거인가"·부적정이면 Fail + AC 결함 명시) + binding §8 이력. Desired 2 완전형(AC 스크립트 소유 분리) 미도입 — 사유: 단위 소유 재배치는 Planner 분해 정책 재설계이며 재심 = 실 run 에서 AC 적정성 축의 Fail 실측 후. Desired 3(인코딩 스윕) 수행 — 대상 47파일·수정 2·오탐 6·해당 없음 39(콘솔 코드페이지 출력 도구는 utf-8 강제가 신규 결함이라 `locale.getpreferredencoding(False)`+`errors="replace"` 예외 조항). 상세 = git 앵커 `90ca19c`. **강제 지점**: CP2 역할 브리프(전 CP2 디스패치 자동 적재) + Planner 프롬프트 층 + 코드(인코딩 명시·테스트).

---

## P. 런처 입력 검증 부재 — `_slug` 길이 무제한 크래시 (실측 등재 2026-07-21) [해소 2026-07-26]

- **해소 2026-07-26** — 정본 = binding §5.8(`contract_to_graph.fold_slug` 48자+sha8 접기 · `_slug`/`slugify_run_id` 양쪽 적용 · 48자 이하 바이트 동일 하위호환 · 긴 phase `prepare_run` 성공 실증 테스트). §L Desired 4-b(원장 git 커밋 불가)와 같은 뿌리·같은 해법. 상세(등재 경위·긴 ASCII phase 한정 발현 실측) = git 앵커 `90ca19c`. **강제 지점**: 코드(컴파일러·테스트).

---

## Q. proposal seed 제약 ↔ 브리프 실행 AC 요구의 충돌 조정 부재 (실측 등재 2026-07-24 · 원장 전입 2026-07-26)

- **등재 경위**: 핸드오프 갱신 2026-07-24(12) ④가 "신설"로 기록 — 본 원장에는 부재(위 P와 같은 스윕으로 확인) → 전입.
- **Problem / Motivation**: seed proposal의 "done = 오프라인 안전 검사만" 제약과 Advisor 브리프의 "실증형 AC — 실제 대상 실행" 요구가 정면 충돌하면, Planner가 구현 task done에 실제 장시간 실행을 넣어 실행 타임아웃 반복 → retry 소진 → Escalated(yt-stt M3 실측 — escalated-1). 무거운 실행 검증이 필요한 phase에서 브리프 작성자가 seed 제약을 모르면 구조적으로 재발한다.
- **Desired Outcome**: seed 제약을 브리프 작성 규율에 명시하거나, 게이트에서 브리프↔seed 제약을 대조.
- **강제 지점**: 미도입 — 사유: 대조 게이트는 브리프 렌더 구조와 결합돼 별도 설계가 필요하다. 절차 층 대응 = `docs/delegation-protocol.md` §2.1 접합부 왕복 지침(2026-07-26 신설)이 이 충돌 축(브리프↔seed)을 위임 작성 시 열거 대상으로 만든다. 기계 강제는 미해소로 남는다.

---

## R. 정적 CP2의 done AC 간 동적 상충 무검출 (실측 등재 2026-07-24 · 원장 전입 2026-07-26)

- **등재 경위**: 핸드오프 갱신 2026-07-24(12) ④가 "신설"로 기록 — 본 원장에는 부재(위 P와 같은 스윕으로 확인) → 전입.
- **Problem / Motivation**: done AC 간 **동적 상충**(completion gate의 realtime 임계 20x ↔ 스텁 즉시 반환 elapsed → 40x 거짓양성)을 정적 CP2(문면 검사)가 통과시켰고, Worker 실행 시점에야 드러나 Escalated(yt-stt M3 실측 — escalated-2). Worker가 sleep/clamp 위조를 거부하고 정직하게 escalate한 것은 이진 원칙의 실행층 작동 실증.
- **Desired Outcome**: CP2에 "게이트 임계 ↔ 테스트 시나리오 정합" 점검 축 추가 또는 done AC 상호 실행 대조.
- **관련**: M(횡단 결함)·O(AC 실출력 픽스처)와 같은 검증 구조 계열 — M=단위 간 공간 전파, O=AC 입력의 실물성, R=**AC 간 실행 시점 상충**. 셋은 서로를 대체하지 않는다.
- **강제 지점**: 미도입 — 사유: 엔진 Verifier CP2 판정 축 확장(코드·브리프 개정)이 필요해 별도 트랙이다. 절차 층 대응 = `docs/verification-checklist.md` §5.8(검증 축 도출·2026-07-26 신설)이 축 누락을 미검증 축 목록으로 표면화. 기계 강제는 미해소로 남는다.

---

## 우선 관계 요약

현행 미해소 9항 기준(2026-07-26 정정): **A·F**(표현 계층 — Control Plane 뷰와 결합) → **D·G**(외부 capability 수용 경로 · Skill/Capability Routing) → **E**(Execution Modes — Baseline 재측정 선행) / **H·I**(지속 관측 · 라이브 심의 호스팅)와 **Q·R**(검증 구조 계열의 기계 강제 잔여)은 순위 미배정(사용자 결정). 종전 확정 순서 `B+C→D→G→A+F→E` 와 2026-07-14 Dogfooding Evidence 표는 B·C 종결로 효력 소멸 — 원 문면은 git 앵커 `90ca19c` 보존(`ARCHIVE.md` 등재).
