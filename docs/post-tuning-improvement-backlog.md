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

## B. UI/UX Visual Contract

> **[실체화 완결 2026-07-19 — Visual Contract 트랙]** 디자인 필수 요소(designElements 11종)·필수 산출물 3종(토큰·mock·수렴 기록·touchpoint)·mock 수렴 규약(binding §7A/§7C — 기획 확정→1화면 3안 톤 수렴→정본 우선 갱신→사용자 수렴 기록→오케스트레이션 진입)을 Policy 데이터+design_completeness 게이트로 강제. 잔여: Discovery Eliciting 시각 선호 차원(부분 — 인터뷰 표면화 시 편입 메커니즘으로 커버)·Interactive Prototype(조건 발동형)·실 파일럿(다음 소비 프로젝트).

- **Problem / Motivation**: 사용자는 구현 전에 LLM이 최종 목표를 정확히 이해했는지 **눈으로** 확인할 수 있어야 한다. v1.7에서 Wireframe이 사용자 수정 요구로 사후 주입됐고, 톤앤매너는 침묵 디폴트됐다(mi-0107 Novel) — UI/UX 산출은 단순 디자인 산출물이 아니라 **요구 이해를 검증하는 Visual Contract**다.
- **Desired Outcome**: `Interview → Requirement Discovery → UX Flow/IA → Wireframe → UI Mockup → (필요 시) Interactive Prototype → User Validation → Final Approval → Autonomous TDD Implementation` 흐름을 성숙 run 프로토콜(04) 위에 UI 제품 유형의 표준 경로로 정식화. Discovery Eliciting에 제품 유형 함의 차원(시각 디자인 선호) 포함.
- **Why Not in Current Tuning Track**: 기능 확장(파이프라인 단계 추가)이며 성능 튜닝과 직교. 비용을 늘리는 방향이므로 튜닝 후 Baseline 위에서 가치·비용을 측정해야 함.
- **Dependency**: 성숙 run 호스팅(v1.7 실증 자산)·디자인 협업 라운드(사용자 관심 기표명)·Contract v2 open(실시간·Control과 별개).
- **Suggested Future Track**: 「Design Collaboration & Visual Contract」 — uahf-control-plane v2→v3 성숙 run을 파일럿으로.

## C. UI Design Principles (품질 기준)

> **[실체화 완결 2026-07-19 — Visual Contract 트랙]** designPrinciples 17종(Figma UI 7 + Nielsen UX 10·gist 자체 문면) Policy 데이터 등재 + 디자이너 브리프 강제 주입 + 화면설계서 문서 단위 근거 기록 + mock 리뷰 차원(§7C.3a). 접근성 기계 판정분은 accessibility-floor criteria 실값(WCAG AA). 해설 카탈로그 = 비정본 부록(visual-contract-catalog.md — 관례 준수).

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

## J. 오케스트레이션 에스컬레이션 해소·재작업 경로 (실측 등재 2026-07-20 — 기록만·결함성 공백)

- **Problem / Motivation**: cheongryong-bubble impl-s14-15 run 실측 — 대형 통합 단위가 실행 타임아웃(config timeout=900s)×3으로 `Escalated` 종단 후, ① **stop-signal.json이 에스컬레이션 정지 시 갱신되지 않아** 낡은(이미 해소된) user_decision 게이트를 담고 있고 `resolve_gate.py --gate-kind escalation`이 "게이트 없음"으로 거부(해소 채널 물리 단절), ② **Escalated가 fold에서 종단**이라 `--resume`이 재디스패치하지 않음(timeout 상향·재작업 지시의 엔진 경로 부재) — 에스컬레이션의 설계 의미(상위 위임)는 맞으나, 상위가 "조건 변경 후 재작업"을 지시할 물리 경로가 없어 Advisor 대역 완수(원장 밖 위임)로 우회하게 됨.
- **Desired Outcome**: ① 모든 정지 사유에서 stop-signal 일관 갱신(escalation_required 게이트 포함), ② 에스컬레이션 해소 응답에 재작업 지시(retry 카운터 리셋·config 패치 반영) 경로 추가 — 해소 이벤트 append → resume 시 해당 단위 Execute 재진입, ③ (예방) 단위 규모 대비 타임아웃 산정 — Planner 브리프에 invoke 예산 힌트 또는 per-unit timeout.
- **Why Not Now**: 05 spec/게이트 코드 변경이며 현재 개발 run 진행 중 — Advisor 대역 완수+원장 기록으로 우회 가능. 완료 후 독립 트랙.
- **재발 실측 (2026-07-25 · yt-stt `impl-yt-stt-m4afix2`)**: `uaf-verified:` 같은 결함이 다른 소비 프로젝트에서 재발했다(proposal step 이 timeout=900 초과 3회 → retry-limit(2) 소진 → Escalated). **검색 범위** = 이 run 의 events/logs + `resolve_gate.py`·`orchestrate_project.py` 소스 + `DEFAULT_TIMEOUT`·`timeout=900` 저장소 스윕. 위 ①②에 더해 다음 좌표를 확정했다.
  - **`escalated` 이벤트에 `gate_id` 필드가 없다** — `cycle_id`(step id)만 있다. `recover_gate` 는 `stop-signal.json` 의 `pending_gates[].gate_id` 를 요구하고 주석이 "추측 0" 을 명시하므로, stop-signal 을 손으로 만들려면 **없는 gate_id 를 발명**해야 한다. 즉 ①은 파일 부재 문제가 아니라 **좌표 자체의 부재**다.
  - **런처의 stop-signal 미기록은 의도된 설계다** — `orchestrate_project.py:18-19` 가 `stop_reason=="gate"` 일 때만 기록하도록 명시한다(Escalated 는 그 외 분기). 즉 ①의 수정 지점은 런처이며 버그가 아니라 계약 불일치다(`resolve_gate.py` 가 파일 존재를 무조건 전제).
  - **`--retry-limit` 상향으로도 부활하지 않는다** — 실측: `--resume --retry-limit 5` 가 `INVOKES=0` 으로 즉시 재정지(원장 fold 가 Escalated 를 종단으로 확정). ②의 "timeout 상향·재작업 지시 경로 부재"가 CLI 우회로도 메워지지 않음을 확인.
  - **⚠ "우회 가능"의 실제 비용**: J 가 제시한 우회(Advisor 대역 완수)는 **엔진 밖 처리**를 뜻한다. 그것은 `.claude/CLAUDE.md`·`AGENT.md` 「Run 조율 우회 금지」에 저촉되므로, 원장을 보존하려면 **현 run 을 폐기하고 새 run-id 로 재실행**하는 것이 유일한 경로다(이번 세션이 택한 길 — `m4afix3`). 즉 J 는 "우회 가능"하되 그 우회가 거버넌스 불변과 충돌한다. **폐기된 `m4afix2` 원장은 이 증거로 보존한다.**
  - **부수 예방 조치(별건 수행)**: `DEFAULT_TIMEOUT` 900→2400 상향(커밋 `96c07f6`). 원장 실측 5건 근거(cheongryong-bubble `impl-s14-15-ui-sound` 3회 연속·`impl-s16-18-final`·`impl-s04-08-core`·yt-stt `m4afix2`). 이는 위 ③(타임아웃 산정)의 부분 완화이며 J 본체(해소 채널)는 미해소다.
- **Dependency**: `orchestration/framework/orchestrator/gates.py`·런처 stop-signal 기록부·resolve_gate.py·05 §3.3.
- **Suggested Future Track**: 「Escalation Rework Path」 소형 트랙. 우선순위 미배정(사용자 결정). **2026-07-25 재발로 우선순위 상향 후보** — 소비 프로젝트 2곳에서 발현했고 회피책이 거버넌스 불변과 충돌한다.
- **[본체 해소 2026-07-26 — RCA 처방 1]** Desired ①(모든 정지 사유에서 stop-signal 일관 갱신 — escalated 정지도 게이트 분기와 같은 계약 4필드)·②(해소→재작업 재진입 — 엔진이 escalated 정지에 gate_id `gate-unit-<id>::exec-escalation` 요구를 발급하고, 적격 해소 소비 시 되돌림 이벤트 append로 **해소 1건=추가 시도 1회**·재실패 시 새 요구 발급으로 이전 해소 소진) 구현·Advisor CP2 Pass(3트리 312건 독립 재실행·접합부 왕복 실물 검증). 레거시 escalated run도 `--resume` 1회로 해소 가능 상태가 된다. 정본 = `orchestration/adapters/claude/project-orchestration-binding.md` §3.4. ~~잔여(미해소): Desired ③ per-unit timeout 산정~~ → **Desired ③ 해소 2026-07-26**(백로그 §L Desired 4 와 공통 구현 — impl-plan 선택 `timeout` 키 + 검증 게이트 + `UnitTimeoutInvoker` 재기입·정본 = binding §5.8 (g)·상세 = 아래 §L Desired 4 해소 항). 설계 조사 이력 보존: 전역 `DEFAULT_TIMEOUT` 2400 완화는 기반영·`InvokeRequest.timeout` per-request 필드 실재·StepHost 는 uahf 무수정 경계라 orchestration 층 래퍼 invoker 경로가 무접촉 해법 후보·`Step.from_dict` 필드 보존은 화이트리스트(탈락)로 실측 확정 — 좌표 = `docs/backlog-k-delegation-b-ledger.md` §5-A. ~~`recover_gate` 다중 pending 특정 지목~~ → **해소 2026-07-26**: `--gate-id` 옵션 + 무지목 다중 매칭 시 후보 열거·원장 무변경 비영 종료(침묵 첫-선택 제거) + 렌더 항목별 `resolve_command` 가 자기 gate_id 상시 지목 + `uaf-implement.md`·binding §3.2/§3.4 문면 동기화. `uaf-verified:` 런처 실산출 stop-signal → 렌더 문면 → 실행 → 재렌더 왕복 + 테스트 3트리 138+175+42(검색 범위 = orchestration 2트리+uahf 2트리). 강제 지점: 코드(엔진·런처·테스트).

---

## K. Solution Design 성숙 시 Projection 정본 포인터 갱신 누락 (실측 등재 2026-07-21 — 기록만·stale 결함)

- **Problem / Motivation**: yt-stt Contract v3 개정 세션 실측 — Solution Design 성숙 run이 Contract v1→v2 superseding 인스턴스를 산출했으나, **그 성숙 run이 만든 Projection 7종 전부의 헤더 근거 정본 포인터가 `project-contract.v1.md`를 그대로 가리킨 채 남았다**(`docs/{project-plan,requirements-def,business-process,functional-spec,table-def,interface-spec,test-plan-cases}.md` 4행 · 전수 grep 확증). 즉 Projection은 v2 성숙의 산출물인데 자기 근거로는 v1을 지목한다. `docs/solution-design.md`(인덱스)만 v2를 가리켜 문서군 내부에서 포인터가 갈렸다. v3 개정 시점에는 격차가 두 버전으로 벌어질 참이었고, 사람이 별건 스윕에서 우연히 발견해 수동 정정했다(사용자 승인 범위 이탈로 처리·v3 provenance.scopeDeviation 기록).
- **왜 결함인가**: 하류 구현 task는 "설계 결정 앵커를 인용하라"는 지시를 받고 Projection 헤더의 정본 포인터를 따라간다. 포인터가 낡으면 **이미 superseded 된 인스턴스의 결정을 앵커로 삼는다** — append-only 계보(PC-INV 9)가 옛 인스턴스를 보존하고 있으므로 파일은 실재하고, 따라서 **실패하지 않고 조용히 틀린다**. 탐지 수단이 사람의 우연한 스윕뿐이다.
- **Desired Outcome**: ① 성숙 경로(`Matured` 전이)가 superseding 인스턴스 산출 시 **Projection 헤더 정본 포인터 갱신을 강제**하거나, ② Projection이 버전을 하드코딩하지 않고 "최신 vN"을 가리키는 간접 참조를 쓰게 하거나, ③ design-manifest CP2 결정적 체커에 **포인터 정합 검사**(각 artifact 헤더의 Contract 참조 == 현재 인스턴스)를 추가한다. ③이 가장 저렴하고 기존 체커 자리에 들어간다.
- **Why Not Now**: 04 spec 성숙 경로 또는 design_completeness 체커 개정이며, 이번 세션 범위(yt-stt 설계 반영)를 벗어난다. 소비 프로젝트 측 stale은 이미 수동 해소됨.
- **Dependency**: `planning/specs/04-solution-design.md` 성숙 경로(`Matured` 산출 규정) · design-manifest CP2 체커 · `planning/specs/03-project-contract.md` §3.4(append-only·supersedes).
- **관련**: [[uaf-design-manifest-path-defect]] 계열(design-manifest ↔ 실제 산출물 배선 결함)과 같은 축 — 매니페스트가 산출물의 **경로**는 알지만 산출물이 **어느 인스턴스에 귀속되는지**는 검사하지 않는다.
- **Suggested Future Track**: 「Projection Provenance Integrity」 소형 트랙. 우선순위 미배정(사용자 결정).
- **[해소 2026-07-26 — Desired ③]** `design_completeness` 결정적 체커에 Contract 포인터 정합 검사 신설 — produced·실재·`.md` 산출물의 최고 `project-contract.v<N>.md` 참조 == 계보 현재 인스턴스(최고 vN). 미달=stale·초과=dangling·계보/산출물 판독 실패=차단(판정 불가는 통과가 아니다)·계보 정당 부재/참조 0건/비-md=비적용. 이탈 채널 = `contractRefPinned{reason,confirmedBy}`. path 해석은 기존 produced 존재 검사와 동일 식 재사용(해석 이원화 금지·RC-2 재발 방지). `uaf-verified:` 실물 yt-stt 워크스페이스 왕복 양방향(현행 v4 → 통과 EXIT=0 / 합성 v5 주입 → stale 7건 EXIT=2·검색 범위 = yt-stt 매니페스트 등재 7종) + 테스트 3트리 129+175+42 재실행. 정본 = `orchestration/adapters/claude/design-manifest.schema.md` §Contract 포인터 정합 규칙. Desired ①(성숙 경로 강제)·②(간접 참조)는 미도입 — 사유: ③이 구현 편입 게이트에서 stale 을 차단하므로 하류 소비 전 검출이 성립하며, ①은 04 spec 개정(거버넌스 무게)·②는 append-only 계보 인용 관행 전면 변경이 필요하다. 트랙 원장 = `docs/backlog-k-delegation-b-ledger.md`. 강제 지점: 코드 — `resolve_gate` task_added 승격 직전 fail-closed + `pretooluse_design_guard` 백스톱 동일 코드 재사용 + 테스트 15건 + scaffold 미러 상속.

---

## L. Run Observability — Heartbeat · Failure Record · 종료코드 규약 (사용자 지시 등재 2026-07-21 — 기록만·운영 결함)

- **Problem / Motivation**: 사용자 실측(복수 세션 반복) — 백그라운드 스크립트·서브에이전트가 **오류를 내거나 대기 상태에 오래 빠져도 주 세션도 사용자도 모른 채 계속 대기**했고, 사용자가 물어봐야 확인하는 일이 반복됐다. 실패 모드 3종의 위험도가 다르다: **F1 죽음**(exception·crash — 프로세스가 끝나므로 완료 알림이 온다) / **F2 매달림**(hang·무한대기 — **종료 이벤트가 없어 알림이 원리적으로 안 온다**) / **F3 오해석**(정상 게이트 정지 `exit 2` 를 실패로, 또는 그 반대). **진짜 병목은 F2** 이며, "예외를 상위에 전달"만으로는 해결되지 않는다 — 침묵이 "진행 중"인지 "멈춤"인지 구분하려면 **진행의 능동적 증거(하트비트)** 가 필요하다.
- **실증(2026-07-21 · yt-stt impl-yt-stt-m1 run)**: 런처를 `... 2>&1 | tail -40` 로 발사한 결과 ① 종료 전까지 진행 출력이 0(파이프가 관측 창을 막음), ② 엔진의 실제 종료 코드 `exit 2`(게이트 정지)가 파이프라인에 삼켜져 하네스에 **exit 0** 으로 보고됨 — 엔진이 실패(exit 1)했어도 동일하게 exit 0 으로 보였을 것이다(F3 실물). 발사 규율 측 대응은 [[feedback-background-task-watchdog]] 로 고정했고, 아래는 **엔진 측 계약** 소관이다.
- **Desired Outcome**:
  1. **`logs/heartbeat.json`** — `{ts, current_unit, stage, elapsed_s, invokes}` 를 주기 갱신. **F2 탐지의 유일한 수단** — 외부 감시자가 "마지막 진행 시각"으로 정체를 판정할 수 있게 한다.
  2. **`logs/failure.json`** — top-level `except` 에서 트레이스백 + 실행 컨텍스트(run_id·current_unit·stage·config)를 구조화 기록. 기존 `stop-signal.json` 규약과 동형으로 얹는다.
  3. **종료 코드 규약 명문화** — `0`=완료 / `2`=게이트 정지(정상) / 그 외=실패. 현재 `exit 2` 가 정상 정지라는 사실을 매 세션 문서에서 되찾아야 한다.
  4. **per-unit timeout** — 현재 config `timeout` 은 전역이며, 단위 규모 대비 산정이 없다(백로그 J 의 예방책 ③과 동일 지점).
  4-b. **unit id 슬러그 길이 무제한 → 원장이 커밋 불가해진다**(실측 2026-07-21 · `impl-yt-stt-m1fix2`). `--phase` 문자열이 seed unit id 로 슬러그화되고 그 id 가 `logs/invoke-NN-<Role>-<unitId>.json`·`steps/<unitId>.json` 파일명에 **그대로** 들어간다. phase 에 결함 요약을 담는 것은 이미 관례인데(선례 `impl-yt-stt-m1fix`), 이번엔 파일명 **239자**·전체 경로 **367자**가 되어 **git 이 `Filename too long` 으로 인덱싱을 거부**했다 — 즉 **run 원장을 커밋할 수 없다**. 직전 run 은 118자로 우연히 통과했을 뿐이다(경계에 걸쳐 있었다). 우회는 `git config core.longpaths true`(이번에 적용)이나, 근본 해법은 **unit id 슬러그에 길이 상한 + 해시 접미**(예: 앞 48자 + `-<sha8>`)를 두어 id 유일성과 파일명 안전을 함께 만족시키는 것이다. 원장 보존이 UAF 의 핵심 산출인 만큼 **조용한 유실 경로**로 취급해야 한다.
  5. **`--resume` 의 run-id 재파생 함정**(2026-07-21 실측) — `--resume` 은 **기존 run_dir 을 쓰는 명령인데도 `--run-id` 를 다시 요구**한다. 생략하면 런처가 run-id 를 compile 기본값에서 재파생해(`--phase` 기본 'Phase 1' 결합) 실제 run(`impl-yt-stt-m1`)이 아닌 **존재하지 않는 경로**(`orch-yt-stt-Phase-1`)를 찾고 `[ERR] --resume 대상 run_dir 부재` 로 종료한다. 원 run_id 를 모르는 상태에서 resume 하면 조용히 엉뚱한 곳을 본다. **개선안**: `--resume` 시 (a) run_dir 을 명시 인자로 받거나, (b) 직전 run 을 자동 해소하거나, (c) 최소한 후보 run_dir 목록을 오류 메시지에 제시. 현재는 오류 메시지가 "부재"만 알리고 **실재하는 run 이 옆에 있다는 사실을 알려주지 않는다**.
     - **재발 실측(2026-07-21 · `impl-yt-stt-m1fix2`)**: 등재 뒤 같은 세션에서 **다시 밟았다**. 그리고 근본 원인 하나가 더 드러났다 — **`.claude/commands/uaf-implement.md` §2 의 재개 예시가 `python orchestrate_project.py <project_root> --resume` 로만 표기**되어 런처 계약(`_resolve_slug(args.run_id, args.phase, root.name)`)과 어긋난다. `--run-id` 를 준 run 은 그 예시대로 하면 **반드시 실패**한다. 즉 이 함정은 코드 결함인 동시에 **명령 문서가 틀린 사용법을 가르치는** 문서 결함이다. 개선안 (a)~(c) 중 무엇을 택하든 **`uaf-implement.md` §2 예시 정정은 코드 변경 0 으로 즉시 가능**하다.
- **Why Not Now**: 런처·오케스트레이터 코드 변경이며, 등재 시점에 M1 run 이 진행 중이었다(진행 중 run 과 충돌 위험). 발사 규율(층 1)·행동 규율(층 3)은 코드 변경 0 으로 즉시 적용해 당면 사고는 막았다.
- **Dependency**: `orchestration/adapters/claude/orchestrate_project.py`(런처 stop-signal 기록부) · `orchestration/framework/orchestrator/` 실행 루프 · 05 §3.3.
- **관련 — J 와의 상하류 구분(우선순위 판단용)**: **J = 타임아웃이 걸린 *뒤*의 복구 경로**(Escalated 후 재작업 지시 채널 부재). **L = 타임아웃조차 안 걸리고 매달리는 *앞* 구간**(정체 자체를 아무도 모름). L 이 상류이며, L 없이는 J 가 발동할 기회조차 관측되지 않는다. H(Continuous Telemetry)와도 구분된다 — H = 누적 계측·분석, L = **장애 탐지**.
- **Suggested Future Track**: 「Run Observability」 소형 트랙. 우선순위 미배정(사용자 결정) — 단 J 착수 시 L 을 선행으로 묶는 것을 권고.
- **[핵심 해소 2026-07-26 — RCA 처방 1·J와 동일 트랙]** Desired 1(heartbeat — 계약 필드는 `{ts, stage, invokes, request_hint, pid}`로 확정: 런처는 단위 경계·경과시간을 소유하지 않으며 F2 탐지의 실사용은 "마지막 ts와 현재 시각의 차"이므로 `elapsed_s`·`current_unit`은 관측자 파생값이다 — 원 문면과의 차이 사유는 `docs/rca-prescriptions-ledger.md` W-L) · 2(failure.json 계약 6필드·재raise 은폐 0) · 3(종료코드 규약 명문화 — `uaf-implement.md` §2 표 + binding §5.8) · 4-b(슬러그 상한 `fold_slug` 48+sha8 — §P와 공통 해소·원장 커밋 불가 경로 차단) · 5(`--resume` 부재 오류에 실존 후보 목록 + `uaf-implement.md` §2 예시 `--run-id` 정정) 구현·Advisor CP2 Pass. 정본 = binding §5.8. ~~미해소 잔존: Desired 4(per-unit timeout)~~ → 해소(아래 항). 강제 지점: 코드(런처·컴파일러·테스트 17건).
- **[Desired 4 해소 2026-07-26 — per-unit timeout]** impl-plan task 의 **선택 12번째 키 `timeout`**(실행 예산 초·양의 정수·부재 = 전역 fallback·`REQUIRED_TASK_KEYS` 11키 무변) + `resolve_gate.validate_impl_plan_adapter` fail-closed 검증(bool·0·음수·실수·문자열 거부 — 불량값이 task_added 로 승격되지 않고 원장 무오염) + 중립 엔진 `orchestrator.UnitTimeoutInvoker`(`active_graph()` 파생 맵 단일 원천·`request.bundle.step_contract.id` 매칭·`dataclasses.replace` 재기입·원본 무변조·비매칭 원 객체 통과·`__getattr__` 투과) — 한 단위의 **exec·CP2·게이트 디스패치 3경로 균일 적용**, 맵 공집합 = 래핑 0(기존 거동 보존), seed proposal 노드는 timeout 미부여(값 발명 금지·전역 fallback). `uaf-verified:` 4트리 재실행 186+144+23+19 EXIT=0×4 + 실물 왕복 테스트(impl-plan→검증→승격→fold→엔진 run→`request.timeout` 실측) + Advisor 독립 음성 대조(래퍼 항등 패치 시 전역 회귀 — 재기입 인과 격리). 검색 범위 = orchestration 2트리 + uahf step-host·step-invoker 트리. 정본 = binding §5.8 (g)·트랙 원장 = `docs/backlog-k-delegation-b-ledger.md` §5-A. 잔여 관측 좌표 = 실 LLM run 에서 재기입 예산 실증(코드 경로 정독까지 — `claude_invoker.py` 가 `request.timeout` 을 subprocess timeout 으로 소비). 강제 지점: 코드 — 검증기(fail-closed) + 래퍼 배선 + 테스트 17건(11+6).

---

## M. 횡단 결함 검지 — Cross-Unit Defect Sweep (실측 등재 2026-07-21 — 기록만·검증 구조 공백)

- **Problem / Motivation**: yt-stt `impl-yt-stt-m1` run 실측 — CP2(Verifier)가 `m1-pipeline-orchestrator` 단위에서 실제 결함을 정확히 잡아 rework 시켰다(`glob.glob(os.path.join(video_dir, "video.720p.*"))` 에서 보관 규약상 폴더명 `<제목> [<영상ID>]` 의 **리터럴 대괄호가 glob 문자 클래스로 오인**되어 파일이 존재해도 매치가 절대 성공하지 않음 → 자산 스킵·재개가 항상 무력화 → HTTP 429 재발). **그런데 완전히 동일한 결함이 선행 단위 `m1-acquisition-ytdlp`(`acquisition.py`)에 4곳 있었고, 그 단위는 이미 CP2 를 통과해 Complete 로 확정된 상태였다** — 그중 1곳(`video.720p.*`)은 지적받은 코드와 **글자 그대로 동일**하다.
- **구조적 사실**: **CP2 는 단위별 검증이다.** 같은 원인이 여러 단위에 퍼져 있으면 **먼저 통과한 단위는 그대로 남는다.** 엔진은 지적된 단위만 rework 하고 동료 단위를 다시 보지 않는다. 이는 엔진 버그가 아니라 **단위별 검증의 본질적 한계**이며, 현재 이 한계를 메우는 것은 Advisor 의 통합 검증뿐인데 **그 층도 같은 턴에 이 결함을 놓쳤다**(검사할 축을 미리 정해두고 그 축만 본 결과 — 무음 게이트 존중 여부는 짚었으나 glob 대괄호는 못 봄).
- **왜 위험한가**: 횡단 결함은 **각 단위의 AC 를 개별적으로는 전부 통과한다**(구문 유효·파일 존재·구조 assert). 실패가 통합 실행 시점에만 드러나는데, 오프라인 AC 환경에서는 그 시점이 오지 않는다. 게다가 이번 사례처럼 **상위 설계가 심은 재발방지 요건을 하위 구현이 조용히 무력화**하는 형태를 띤다.
- **Desired Outcome**:
  1. **결함 패턴 전파 스윕** — CP2 가 어느 단위에서 결함을 확정(rework)하면, 그 **결함 패턴(정규식·심볼·API 사용형)을 run 내 이미 Complete 인 동료 단위에 자동 재스윕**하고, 히트가 있으면 해당 단위를 rework 대상으로 되돌린다(원장에 근거 이벤트 append). 최소 구현은 rework verdict 문면에서 코드 패턴을 추출해 `grep` 하는 수준으로도 유효하다.
  2. **milestone 단위의 통합 AC 강화** — phase 경계 milestone 이 개별 파일 존재·구문 검사에 머물지 말고 **단위 간 계약 정합·공통 결함 패턴 검사**를 포함하도록 Planner 브리프에 요구.
  3. (경량 대안) rework 발생 시 **Advisor 게이트로 표면화**해 사람이 동료 단위 스윕을 지시할 수 있게 한다 — 자동화 전 단계.
- **Why Not Now**: gates.py/오케스트레이터 rework 경로 변경이며, 등재 시점에 M1 run 이 진행 중이었다. 소비 프로젝트 측 결함 4건은 **후속 수정 run 으로 조치**(사용자 결정 2026-07-21) — 원장 밖 직접 수정을 택하지 않아 2층 규율을 지켰다.
- **Dependency**: `orchestration/framework/orchestrator/gates.py`(CP2 verdict 처리·rework 되돌림) · `contract_to_graph.py`(milestone 브리프 생성부) · 05 §3.3.
- **관련**: [[uaf-orchestration-wiring-gap]] 의 교훈 "Wave 경계 계약 통합검증 필수"의 **재발**이다 — 교훈은 기록돼 있었으나 **기계 강제가 없어** 같은 유형이 다시 났다(책임 있는 자율 (a): 빠지면 안 되는 것은 비정본 교훈이 아니라 Core·게이트로 강제해야 한다).
- **Suggested Future Track**: 「Cross-Unit Defect Sweep」 소형 트랙. 우선순위 미배정(사용자 결정).

---

## N. 조건부 승인의 하류 전달 배선 부재 (실측 등재 2026-07-21 — 기록만·게이트 표현력 공백)

- **Problem / Motivation**: 사용자 구조 게이트(`user_decision_required`)는 사실상 **승인/거부 이진**이다. 실제 사용자 결정은 "조건부 승인 — 이러이러한 보강을 넣고 진행"인 경우가 흔한데, **그 조건을 하류 Worker 에게 전달할 배선이 없다.**
- **실증(2026-07-21 · `impl-yt-stt-m1fix2`)**: 사용자가 3 task 계획을 **조건부 승인**(보강 2건: ① 측정 실패≠무음 구분 기록 필수화 ② `run_acquisition` 시그니처 호환 실검증)했다. 그러나 `resolve_gate.py` 의 `--response` 는 `_append_provenance`/`_write_record` 로 **원장에 기록만** 되고, 실제 승격되는 것은 `impl-plan.json` 본문이다(`resolve_structural` → `task_added` revision). 즉 **응답 텍스트는 Worker 프롬프트에 도달하지 않는다.** 보강을 실제로 반영하려면 Advisor 가 **Worker 산출물인 `impl-plan.json` 을 직접 편집**해야 했다(원본은 `impl-plan.json.pre-advisor-augment` 로 보존하고 편집 사실을 `--response` 에 기록해 provenance 는 남겼다).
- **왜 문제인가**: (a) **원장 무결성 훼손** — ArtifactRecord 상 "proposal step 산출"과 실제 내용이 어긋난다. Advisor 편집분과 Worker 산출분이 사후에 구분되지 않는다. (b) **우회가 규약화되지 않음** — 이번엔 백업+provenance 기록으로 정직하게 처리했으나, 이는 **관행이지 강제가 아니다**. 다른 세션은 조용히 덮어쓸 수 있다. (c) 대안인 "게이트 거부 후 재수립"은 조건이 seed 에 전달될 경로도 없어 같은 문제로 되돌아온다.
- **Desired Outcome**:
  1. `--response` 를 **하류 주입 채널로 승격** — 해소 응답을 `task_added` 되는 각 task 의 delegation context 에 **추가 지시로 주입**(원 산출물은 불변 유지). 원장에는 "원 산출 + 게이트 조건"이 분리 보존된다.
  2. 또는 **`conditional-approval` 해소 종류 신설** — 조건 목록을 구조화 필드로 받아 승격 시 병합하고, 조건 미반영을 CP2 가 검사할 수 있게 한다.
  3. 최소 대안: Advisor 산출물 편집을 **정식 절차로 명문화**(백업 파일명 규약·provenance 필수 필드). 지금은 이번 run 의 임시 관행일 뿐이다.
- **Why Not Now**: `resolve_gate.py`·05 §3.3 게이트 어휘 변경이며, 등재 시점에 해당 run 이 진행 중이었다.
- **Dependency**: `orchestration/adapters/claude/resolve_gate.py`(`resolve_structural`·`_append_provenance`) · `contract_to_graph.py`(delegation context 조립) · 05 §3.3.
- **관련**: CP3 비-Pass 시의 `escalation_required` 경로(백로그 J)와 **같은 계열의 표현력 문제**다 — J 는 "거부 후 재작업 지시 채널 부재", N 은 "**승인하면서** 조건 붙일 채널 부재".
- **[해소 2026-07-26 — Desired 1 채택]** 구조 게이트 해소의 비공백 `--response` 를 **승격되는 모든 task 의 `delegation.context` 조건 항목으로 주입**(`resolve_gate.format_condition`·`build_promotion_payloads` — 결정적 문면 `[게이트 조건 — <gate_id> 해소(actor=<actor>)] <원문>`). 원장 3면 분리 보존 = `impl-plan.json` 바이트 무변조(원 산출) + provenance 이벤트 `ref.response`(조건 원문·기성립) + revision payload(하류 소비 뷰). 타입 규칙 = list append·str 2원소 승격·부재 신설(+`[CONDITION-NOTE]` 관측 신호 — 종전 Escalated 경로를 가리지 않도록 id 열거·차단 아님)·그 외 형 = **원장 append 전 비영 종료**(조건의 침묵 탈락 금지). 하류 도달 = 번들 `memory_material`(Worker)+`step_contract.delegation`(CP2 Verifier) 실물 왕복 실측. 게이트 어휘·05 spec 무변경(어댑터 층 해소 — "Why Not Now" 의 어휘 변경 우려는 Desired 1 채택으로 회피). `uaf-verified:` 4트리 재실행 186+161+23+19 EXIT=0×4·신규 테스트 17케이스(실 argv 관통 왕복 포함)·검색 범위 = orchestration 2트리+uahf step-host·step-invoker 트리. 정본 = binding §3.3·트랙 원장 = `docs/backlog-k-delegation-b-ledger.md` §5-A. **Desired 2 미도입** — 사유: 05 §3.3 게이트 어휘 개정(거버넌스 무게)이고 Desired 1 이 조건의 물리 도달을 성립·조건 미반영 판정 축은 백로그 R 계열로 유보(재심 = 균일 주입의 조건 오귀속 실측 시). **Desired 3 미도입** — 사유: 채널 신설로 수기 편집 관행의 필요 소멸(명문화는 원장 밖 편집을 정당화하는 역효과). 강제 지점: 코드 — 주입 불가 형 fail-closed + `[CONDITION]`/`[CONDITION-NOTE]` 관측 + 테스트 17건.

---

## O. AC 실출력 픽스처 규율 · 자기출제 구조 (실측 등재 2026-07-21 — 기록만·검증 구조 공백)

- **Problem / Motivation**: 두 겹이다. **(가) 오프라인 AC 가 "합성 입력 AC" 로 잘못 번역되면 외부 도구 계약이 통째로 검증 밖에 난다.** **(나) Worker 가 자기 검증 스크립트를 소유하면 자기 시험지를 자기가 출제한다.**
- **실증(2026-07-21 · yt-stt M1)**: 1차 수정 run(`impl-yt-stt-m1fix`)은 **rework 0 · CP3 Pass** 로 끝났고 AC 도 "실증형"(tempfile 로 대괄호 폴더 생성 + 몽키패치로 함수 실호출)이었다. 그럼에도 Advisor 실기 검증에서 **결함 3계열이 살아 있었다**:
  - `_parse_list_subs_output` 이 실제 yt-dlp 헤더(`[info] Available automatic captions for <id>:`)를 `startswith("Available …")` 로 검사해 **입력이 무엇이든 항상 빈 목록**을 반환(M0 프로브는 `search()` 라 정상 동작 — **재작성 회귀**).
  - `subprocess.run(..., text=True)` 가 cp949 로 디코딩해 한글 경로 stderr 에서 `UnicodeDecodeError` → **reader 스레드에서 터져 주 흐름은 `rc==0` 수신**, stderr 만 유실 → 측정 미매치 → `-90.0` 폴백 → 동률 시 `max()` 가 dict 첫 키 `mono`(위상 상쇄 채널) 선택 → **정상 오디오를 무음 실패로 오판**.
  - 파서 수정이 **잠복 결함을 깨우는** 관계도 있었다(자막 157종 전량 `--sub-langs` 투입 → 429). 결함 간 의존이 AC 설계에 반영돼 있지 않았다.
- **구조적 사실**: "실증형 AC" 라는 라벨은 **충분조건이 아니다.** 몽키패치로 *내 함수를 실제 호출*하는 것과 **외부 프로세스의 실제 출력을 실제로 먹이는 것**은 다른 층위다. 전자만 하면 외부 도구 계약(출력 포맷·인코딩·종료 동작)은 영원히 가정으로 남는다.
- **Desired Outcome**:
  1. **실출력 픽스처 규율** — 외부 도구를 호출하는 단위는 그 도구의 **실제 출력을 캡처해 리포에 고정**하고 AC 가 그것을 소비하도록 요구한다(네트워크 없이 실계약 검증). 2차 수정 run 에서 실제로 이 방식을 썼고(`yt-stt/fixtures/yt-dlp.list-subs.*.txt` 2건) **결함이 재현·해소됐다** — 규율의 유효성은 실증됐다. 브리프 생성부(`contract_to_graph.py`)나 Policy 에서 강제할 지점을 정할 것.
  2. **검증 스크립트 소유 분리(자기출제 해소)** — 구현 단위와 그 AC 스크립트를 **다른 단위가 소유**하게 하거나, 최소한 milestone/CP2 가 AC 자체의 적정성(합성 대체 여부·assert 실값 유무)을 판정하게 한다. 2차 run 은 **명세가 assert 실값을 못박고**(157종·`ko`/`ko-orig`·영상ID 미유출·±1.0dB·`selected=='right'`) **Advisor 가 독립 검증을 별도 작성**해 덮었으나(6/6 PASS), 둘 다 **사람 개입이지 기계 강제가 아니다**.
  3. **인코딩 회귀 스윕** — `subprocess` 출력 디코딩을 로케일에 맡기는 패턴은 한국어 경로 환경에서 **관측 경로 유실**을 낳는다. 규율은 `.claude/AGENT.md` §Invariants(관측 경로 유실 금지)·`.claude/CLAUDE.md`(배선)로 고정했으나, **UAF 자체 스크립트 전수 스윕은 미실시**다(이 세션에서 `graph.json` 출력이 `UnicodeEncodeError` 로 깨진 실측 있음).
- **Why Not Now**: 브리프 생성부·게이트 판정 변경이며, 등재 시점에 해당 run 이 막 종결됐다.
- **Dependency**: `contract_to_graph.py`(task/AC 브리프 조립) · `orchestration/framework/orchestrator/gates.py`(CP2 판정 축) · 05 §3.3.
- **관련**: **M(횡단 결함 검지)과 인접하나 별건**이다 — M 은 "같은 결함이 여러 단위에 퍼졌을 때 먼저 통과한 단위가 남는다", O 는 "**AC 의 입력이 가짜라서 단위 하나조차 제대로 검증되지 않는다**". M 을 고쳐도 O 는 남는다.

---

## P. 런처 입력 검증 부재 — `_slug` 길이 무제한 크래시 (실측 등재 2026-07-21 · 원장 전입 2026-07-26)

- **등재 경위**: 핸드오프 갱신 2026-07-21(8) ⑤가 "백로그 P 신설"로 기록했으나 본 백로그 원장에는 항목이 없었다. `uaf-verified:` 2026-07-26 본 파일 전문 정독 + `^## [PQR]\.` 패턴 스윕(검색 범위 = 이 파일)으로 부재 확인 — 원장 이원화(핸드오프에만 존재)의 실사례이며 본 전입으로 해소.
- **Problem / Motivation**: `orchestrate_project.py`의 seed 노드 id = `"impl-plan-" + _slug(phase_scope)`가 그대로 파일명이 되는데 `_slug`에 길이 상한이 없어, 긴 `--phase` 문자열에서 Windows 경로 한계로 `OSError: [Errno 22]` 크래시(실측 2026-07-21 · 크래시가 게이트·원장 이전 단계라 원장 오염 0). 성격 = 관측(L) 계열이 아니라 **입력 검증 부재**.
- **부수 실측(2026-07-23)**: `_slug`가 한글을 제거하므로 긴 한글 phase는 미저촉(`impl-plan-m2-1-m2-brief-md.json` 31자로 접힘) — 긴 **ASCII** phase에서만 발현.
- **관련**: 백로그 L §Desired 4-b(슬러그 길이 → 원장 git 커밋 불가)와 같은 뿌리(슬러그 상한 부재). 해법 공유 = 길이 상한 + 해시 접미(예: 앞 48자 + `-<sha8>`).
- **강제 지점**: 코드 — **해소 2026-07-26**(`contract_to_graph.fold_slug` 48자+sha8 접기·`_slug`/`slugify_run_id` 양쪽 적용·48자 이하 바이트 동일 하위호환·긴 phase `prepare_run` 성공 실증 테스트). 정본 = binding §5.8.

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
[성능 튜닝 트랙 T0~T7]  ← 종료(2026-07-14 — T6/T7 미실시·측정 인프라 유지)
   └→ T3 Reuse Assessment 산출물 ──┐
[Baseline 재측정 (T6~T7)]           │
   └→ E(Execution Modes) 선행 조건   │
[Post-Tuning]                        ▼
   A(게이트 UX) ·F(View Modes) → Control Plane 확장과 결합
   B(Visual Contract)+C(Design Principles) → v2→v3 성숙 run 파일럿
   D(External Capability)·G(Skill Routing) → Framework Capability Track
```
