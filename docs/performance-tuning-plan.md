# Performance Tuning Plan — v1.7 Baseline 기반 (2차 보완 분석 포함)

작성: Advisor · 2026-07-14 · **분석·계획 전용(구현 0·커밋 0)**
관계: `docs/baseline-performance-cost-analysis.md`(1차 분석)를 **보존·기반**으로 한다 — 폐기·재분석 아님. 1차 분석의 실측치는 본 문서에서 재인용만 하며, 2차 보완에서 새로 확보한 evidence는 [2차] 로 표기한다.
자매 문서: `docs/post-tuning-improvement-backlog.md`(성능 튜닝과 분리된 개선 백로그).

---

## 1. 지표 체계 재정의 — 시간 관점 분리 (1차 분석 보정)

세 지표를 **항상 분리 관리**한다. 1차 분석 Executive Summary의 "경과 -40~50%" 표현은 아래 A에만 해당하며 **B(엔진 처리 속도)의 개선이 아니다** — 이 보정을 본 계획의 공식 해석으로 확정한다.

| 지표 | 정의 | v1.7 Baseline |
|---|---|---|
| **A. Total Elapsed Time** | 트랙 시작→마감, 사용자 대기 포함 | ≈10.8 h [근사] |
| **B. Active Processing Time** | UAHF/LLM/CLI/Agent 실작업 시간 | ≈5.3 h [근사] |
| **C. User Gate Waiting Time** | 게이트 정지→해소 대기 합 | ≈5.6 h (T8 317 min [2차·실측] + 주간 게이트 3건 3~4 min씩) |

- Gate Notification(T5)은 **C만** 개선한다. B의 개선은 T2~T4가 담당한다. Before/After 보고는 세 지표를 항상 병기한다.
- [2차 실측] 게이트별 대기: k 4 min · m T8 317 min · w 3 min (stop-signal↔resolution mtime — 기존 파일 산출). m 구조 게이트는 stop-signal **덮어쓰기**로 정지 시각 소실(§T1 보완 근거).

## 2. 튜닝 항목 3그룹 분류

| 그룹 | 항목 | 측정 지표 |
|---|---|---|
| **A. Core Performance Tuning** (지금) | T0 Freeze · T1 Telemetry · T2 재검증 중복 제거 · T3 검증 아키텍처 · T4 Context Payload | B(능동)·비용·토큰 |
| **B. Operational UX** (병행 가능·별도 측정) | T5 Gate Notification | C(대기)·A(경과) |
| **C. Post-Tuning Framework Improvements** (이후) | 백로그 문서 참조(게이트 UX·Visual Contract·Execution Modes·Global Skill Routing 등) | 별도 |

## 3. Reuse First 원칙 (본 튜닝부터 적용)

신규 CLI/Script/Skill/Tool 작성 전 **Reuse Assessment 필수**: ① 프로젝트 내부 기존 자산 → ② 설치된 CLI/Tool → ③ 사용 가능한 Skill → ④ 검증된 외부 오픈소스 → ⑤ 얇은 Adapter — 전부 불충분할 때만 신규 구현. 각 튜닝 항목에 "Reuse Assessment Required?" 필드를 두고, T3에는 명시적 Reuse Assessment 단계를 선행 배치했다. **이번 세션에서는 설치·구현 없음.**

[2차] 즉시 식별된 기존 자산(신규 구현 전 1순위 재사용 대상):
- 결정적 검증: `replay_k.py`(결정성)·`resolve_m/w.py`의 `validate_stage_plan`/`validate_impl_plan`(스키마 검증기)·중립 `validate_revision`/`fold`(원장 무결)·pytest 165(중립 코드)·python stdlib(hash/json/git porcelain).
- 게이트 대기 측정: 기존 stop-signal·gate-resolution-record **mtime**(신규 계측 불요 — §T1).
- 하네스 표준 기능: 서브에이전트 완료 통지의 토큰/시간 실측치(수집 절차만 필요)·`/verify` 등 기존 skill(MVP 실동작류 검증에 적용 검토).

---

## 4. 튜닝 항목 상세

### T0 — Baseline Freeze (Phase 0)

- **Problem**: Before/After 비교 기준이 고정되지 않으면 튜닝 효과 판정 불가.
- **Baseline Evidence**: 1차 분석 문서 + 물리 evidence(run 3종·maturation-r003·greenfield-r003·invoke 37로그)는 커밋 `ad451ee`(UAHF)·`dd2fd73`(consumer)에 이미 동결됨. **미커밋 = 분석 문서 2종(1차·본 문서·백로그)**.
- **Freeze 조건(정의)**: ① 분석 문서 3종을 문면 그대로 커밋(다음 세션·사용자 승인 후 — 지금 미커밋), ② 기준 앵커 = UAHF `ad451ee`·consumer `dd2fd73`(선택: 태그 `v1.7-baseline` — 사용자 승인 후), ③ Baseline run 디렉터리(orch-k/m/w·maturation-r003·greenfield-r003)는 이후 **무수정**(신규 run은 새 runId — append-only 관례 그대로), ④ 집계 재현성 = 1차 분석의 추출 방법(invoke 로그 파싱 스크립트)을 T1 산출물로 고정해 동일 산식 재실행 가능하게.
- **Invariants**: append-only(이미 보장)·기존 커밋 불변.
- **Impact**: 측정 신뢰의 전제. **Risk**: 없음. **Measurement**: freeze 체크리스트 4항 충족. **Rollback**: 해당 없음. **Order**: 0(다음 세션 최초 작업 — 사용자 커밋 승인 게이트 포함).

### T1 — Minimal Telemetry / Measurement Foundation (Phase 1)

- **Problem**: 튜닝 효과를 지표로 판정할 자동 집계가 없다(1차 분석은 수동 스크립트).
- **Baseline Evidence**: 1차 §15 지표표. [2차] **게이트 대기는 기존 파일 mtime만으로 산출됨을 실증**(k 4 min·T8 317 min) — 신규 계측 대부분 불요. 단 2개 갭: (a) stop-signal.json 덮어쓰기로 다중 게이트 run의 선행 게이트 정지 시각 소실 [2차 실측: m 구조 게이트 -28 min 오산], (b) 하네스 서브에이전트 USD 미노출(토큰만 통지).
- **Proposed Direction**: **신규 시스템 금지 — 기존 evidence 집계 우선.** ① 집계 스크립트 1개(드라이버 격리 지점 e2e/): invoke 로그·mtime·git 타임스탬프에서 §15 지표 전부를 `run-metrics.json`으로 산출(1차 분석 산식 고정) — 순수 판독·원장 무수정. ② 최소 보완 1건: stop-signal을 위상 번호 부여(`stop-signal-<n>.json`) 또는 정지 기록 append 파일로 — 러너(드라이버 격리 지점) 수준, 중립 코드 무촉 옵션 우선 검토. ③ 하네스 서브에이전트 수치는 Advisor가 트랙 마감 시 통지 실측치를 metrics 파일에 절차적으로 전사(시스템 신설 없음). ④ ready_set 동시성: replay 파생값으로 이미 산출 가능(각 epoch ready_set 크기) — 러너 stdout에 이미 노출, 집계에 포함.
- **측정 대상(최소)**: elapsed/active/gate-wait 분리 3종·critical path·세션 수(전체/fresh/모델별)·모델별 토큰/비용·검증 시간/비용(결정적 vs 의미론 분리)·CP2 수·게이트 재검증 수·cache r/w·retry 수·ready_set 동시성.
- **Reuse Assessment Required?**: 예(완료) — python stdlib+기존 로그로 충분, 외부 도구 불요.
- **Invariants**: 원장 무수정·순수 판독·L-09(순서 값 전속 — 벽시계는 별도 필드/파일).
- **Expected Impact**: 이후 전 항목의 측정 가능성. **Risk**: 극소. **Measurement**: Baseline 값을 스크립트가 1차 분석 수치와 ±오차 없이 재산출. **Rollback**: 스크립트 미사용. **Order**: 1.

### T2 — Review Re-verification Elimination → **유효 기존 검증 결과 재사용** (Phase 2)

- **Problem**: 독립 CP2를 통과한 unit에 review 게이트가 **동일 역할 Verifier LLM 세션을 재기동**.
- **Baseline Evidence**: 9/37 세션·1,043 s·$4.51(CLI 비용 18.7%) [1차 확인]. 재검증 세션과 CP2 세션의 판정 기준·역할·근거 evidence 동일(수 분 간격) — 독립성 이득 0.
- **Proposed Direction**: "재검증 제거"가 아니라 **evidence 재사용**: `Worker → 독립 CP2 → PASS evidence(append) → review 게이트가 그 evidence를 소비해 해소`(해소 이벤트가 근거 cp2-pass 이벤트를 명시 참조 — provenance 사슬 유지). **stale 방지 규칙(필수)**: cp2-pass 이후 해당 unit에 (a) 재실행/retry, (b) task_superseded/revision 영향, (c) 산출 artifact 변경(해시 기록 시 불일치)이 있으면 **재검증 강제**. 정책 데이터로 unit별 "독립 2차 검증 요구" 옵션 유지(고위험 unitType 대비).
- **Reuse Assessment Required?**: 예 — 게이트 판정은 중립 gates/orchestrator 소유(코드 변경 필요 범위 최소화 검토: 정책 데이터로 표현 가능한지 우선, 불가 시 중립 코드 개정 + pytest 보강 + 05 문면 정합 확인[review_required 의미론은 "검증 통과 필요"이므로 spec 개정 불요로 예상 — 구현 트랙에서 확정, 필요 시 Baseline 개정 게이트].
- **Invariants to Preserve**: **PO-INV 4**(게이트 하한 — 게이트 자체는 존치·해소 근거만 변경) · 독립 CP2 존치 · evidence provenance(해소→cp2-pass 참조) · append-only.
- **Expected Impact**: CLI 세션 -24%·시간 -19%·비용 -19% [1차 실측 상한]. **Risk**: 중(경계 조건 — stale 규칙 누락 시 미검증 통과) — 완화 = stale 규칙 3종 + pytest 경계 테스트 + 첫 적용 run에서 재검증-병행 섀도 대조. **Measurement**: 게이트 재검증 세션 수(9→0 목표)·검출율 불변. **Rollback Condition**: 섀도 대조에서 재검증이 신규 결함을 검출하면 해당 unitType은 독립 2차 검증 옵션으로 복귀. **Order**: 2.

### T3 — Verification Architecture Tuning (Phase 3: Reuse Assessment → 분해 → Risk-based Routing)

- **Problem**: 검증이 CLI 시간의 46%·하네스 서브에이전트의 42%를 차지하며, 깊이·모델이 위험도와 무관하게 균일(m/w 검증 21세션 전부 sonnet)이고, 결정적 검사를 8회의 CP2가 매번 LLM+임시 스크립트로 재발명.
- **Baseline Evidence**: [1차] CP2 분해표·k의 haiku CP2 실증($0.03–0.07 vs sonnet $0.29–1.17). **주의(2차 보정): k의 haiku 성공은 "저비용 모델 가능성"의 증거이지 m/w급 의미 검증의 품질 동등성 증명이 아니다 — 균일 haiku 고정 금지.**
- **Proposed Direction — Risk-based Verification Routing** (Verification Type × Risk × Complexity × Artifact Type):
  1. **Deterministic**(schema·seq·hash·hygiene·count·어휘·게이트 순서·replay·build/tsc/AC 결과) → **CLI/Script/기존 Tool** — LLM 0. [Reuse 1순위: validate_stage_plan/validate_impl_plan·replay_k·validate_revision·pytest·stdlib — "uahf-verify 신규 제작"을 전제하지 않고 기존 검증기 조합(얇은 러너)으로 시작.]
  2. **Low-risk Semantic**(산출-계획 대응·형식 서술 정합) → 저비용 모델(haiku) 후보.
  3. **High-risk Semantic**(시나리오 계약 해석·정직성/거짓 완료 검출·설계-근거 정합) → sonnet 유지.
  4. **Critical**(Contract/Spec 충돌·보안·아키텍처 위험) → 상위 모델/사용자 게이트.
- 라우팅 실현 위치: model_selection 정책(OQ-SH-4로 확보된 cp2 슬롯)+gate policy 데이터 — Policy as Data 우선, 엔진 무변경 목표.
- **검출력 보호(필수)**: 모델 하향 적용 unit에 **표본 섀도 검증**(동일 대상 상위 모델 병행 n%)으로 판정 일치율 측정 — 일치율 저하 시 해당 유형 상향 복귀. 하네스 CP2에도 동일 원칙(결정적 검사는 스크립트 소비·LLM은 의미 축 전담·브리프에 기존 검증기 사용 명시 = 코드 0의 즉시 절감).
- **Reuse Assessment Required?**: **예 — 선행 단계로 계획에 포함**(기존 검증기 커버리지 맵 작성 → 갭만 신규).
- **Invariants**: 독립 검증 존치·완료 보고 불신 원칙·검출력 비희생(섀도 대조 게이트).
- **Expected Impact**: 검증 비용 -50%±(CLI CP2 $7.0 중 결정적 대체분 + 모델 라우팅) · 하네스 CP2 시간 -40%±. **Risk**: 중(검출 누락) — 섀도 대조·커버리지 맵으로 완화. **Measurement**: 검증 비용/시간·rework 검출율·섀도 일치율. **Rollback**: 유형별 상위 모델 복귀(정책 데이터 1행). **Order**: 3.

### T4 — Context Payload Architecture Tuning (Phase 4)

- **Problem**: fresh-context 고정비×세션 수 + 문면 중복이 cacheRead 28.0M의 주성분.
- **Baseline Evidence**: [1차] cacheRead 28.0M·세션당 평균 758k. **[2차 확정 — 인과 사슬]**: w run rework 사유 원문 = "delegation.task가 상위 task와 동일하지 않음(요약본으로 축약됨)… byte-identical 교체" — 즉 (i) 프롬프트 규칙이 전문 복사를 강제 → (ii) LLM이 자연스럽게 참조형으로 축약 → (iii) CP2가 규칙대로 Fail → **재시도 +341 s·$1.87** → (iv) 이후 9,767자 중복이 원장·번들·검증 재독에 배수 반영. 반면 **m run은 참조형("위 task 필드와 동일")으로 설계되어 통과** — 수정 지점이 프롬프트/검증기(격리 지점) 수준임이 실증됨.
- **Proposed Direction** — 원칙: **Minimal Default Context + On-demand Retrieval + Full Source Availability**(원문 접근권 유지·기본 payload만 축소·정보 부족 최적화 금지):
  1. delegation 문면 = **정본 참조형 표준화**(m 방식) — 제안 프롬프트·검증기(validate_*)·CP2 브리프 3면 정합(재시도 원인 동시 제거).
  2. 역할별 payload 차등: Worker=task+입력 경로 / Verifier=AC+대상 artifact+결정적 검증 리포트(T3 산출)+표본 원문 / 게이트 해소=요약+근거 참조. 원문은 Read 접근권으로 상시 열람 가능(정보 손실 0).
  3. 반복 원장 원문 로딩 축소: 검증 세션 기본 입력을 "T1 metrics+T3 결정적 리포트+지정 구간 원문"으로 — 전체 재독은 요구 시.
  4. Advisor(주 세션) context: 위임 브리프에 정본 §포인터 우선(전문 인용 최소) — 기존 관행 유지·강화.
- **Reuse Assessment Required?**: 부분(요약 생성은 T1/T3 산출물 재사용 — 신규 요약 시스템 불요).
- **Invariants**: fresh-context 격리 유지·원문 가용성 유지·검증 품질 비희생.
- **Expected Impact**: cacheRead/세션 -30%±·재시도 1건 유형 원천 제거. **Risk**: 소–중(참조형이 하류 소비자[step-host 번들·검증기]와 정합하는지 확인 필요 — m run이 이미 무사 통과한 실증 있음). **Measurement**: cacheRead/세션(역할별)·rework 수. **Rollback**: 프롬프트/검증기 규칙 원복(데이터 수준). **Order**: 4 (①은 T3와 동일 웨이브 탑재 가능한 소형 변경).

### T5 — Gate Notification (Phase 5 · **그룹 B — Operational UX·별도 측정**)

- **Problem**: 게이트 정지를 사용자가 알 수 없어 대기가 무한정(야간 T8 317 min 실측).
- **Baseline Evidence**: C 지표 ≈5.6 h — A(경과)의 ~50%. **B(능동)와 무관 — 엔진 속도 개선으로 집계 금지.**
- **Proposed Direction**: **Port/Adapter 분리 — 특정 서비스 하드코딩 금지**: `게이트 정지 이벤트(exit 2/stop-signal) → Notification Hook(Port — 설정 데이터로 명령/대상 지정) → Adapter(CLI 벨·데스크톱 알림·Telegram 등 기존 채널)`. 최소 구현 범위 = 러너/드라이버(격리 지점)의 정지 경로에서 설정된 알림 명령 1회 실행 — Core·중립 코드 무촉 옵션 우선. Telegram은 사용자 기보유 채널의 **Adapter 후보 중 하나**일 뿐 Core 종속 없음.
- **Reuse Assessment Required?**: 예 — OS 알림 도구·기존 Telegram 봇·하네스 알림 기능 등 기존 채널 우선.
- **Invariants**: 게이트 의미론 무변(정지·사용자 전속 해소 그대로)·알림 실패가 run을 실패시키지 않음(best-effort).
- **Expected Impact**: C -80%±(사용자 가용 시간 내 응답 가정). **Risk**: 극소. **Measurement**: 게이트별 대기 시간(T1 산출)·A 지표. **Rollback**: 설정 해제. **Order**: 5(독립적이므로 앞당겨도 다른 항목과 무간섭 — 단 측정 분리 유지).

### T6 — Benchmark 재실행·Before/After (Phase 6~7)

- **Problem**: 튜닝 효과는 동형 워크로드 재실행으로만 증명된다.
- **Proposed Direction**: 비교 가능 벤치마크 정의 — 후보: uahf-control-plane 소형 개선 1건(예: 백로그의 not-found 404 정정)을 **동일 파이프라인 형상**(제안 step→게이트→구현 task 1~2·CP2)으로 실행하는 신규 runId. Baseline 대응치 = w run의 task당 평균(세션 3.2·비용 $2.97·시간 9.8 min/task [계산]). 규모 차는 task당 정규화 지표로 흡수. 1차와 동일 산식(T1 스크립트)으로 산출·병기(A/B/C 3지표 분리).
- **Order**: 6~7. **Risk**: 벤치마크가 제품 변경을 수반(소형·백로그 항목으로 유용성 확보). **Rollback**: 해당 없음(측정 행위).

### T7 — Concurrency / Physical Dispatch 재평가 (Phase 8)

- **Problem**: 물리 동시 디스패치는 이번 evidence로는 4순위(w DAG 본질 직렬·절감 상한 ~3–4%) — 그러나 다관심사 워크로드에서 가치 상승 가능.
- **Proposed Direction**: T1의 ready_set 동시성 텔레메트리 + T6 벤치마크 이후, "동시 ready 발생율×평균 step 시간"으로 기대 절감을 산출해 착수 여부 재판정. CP2↔차기 Worker 파이프라이닝(ST-2)도 동일 게이트에서 함께 재평가(중위험 — append 직렬화·Fail 전파 의미론 설계 필요).
- **Order**: 8(데이터 확보 후). **Invariants**: evidence append 원자성·워크스페이스 격리(worktree Defer 승계)·게이트 정지 의미론.

---

## 5. 최종 구현 순서 (사용자 제안 0~9 검토 결과)

**제안 순서를 타당한 것으로 확정**하되 근거·수정 2건을 명시한다:

```
0. Baseline Freeze  (분석 문서 커밋 = 사용자 승인 게이트)
1. Minimal Telemetry (기존 로그 집계 스크립트 + stop-signal 위상 보완 1건)
2. Review Re-verification → Evidence 재사용 (stale 규칙 3종·섀도 대조 1회)
3. Verification Architecture (Reuse Assessment → Deterministic 분리 → Risk Routing + 섀도)
4. Context Payload (delegation 참조형 표준화[소형·3과 동일 웨이브 가능] + 역할별 payload)
5. Gate Notification (그룹 B — 순서 무관 독립·측정 분리. 원하면 1 직후로 앞당김 가능)
6. 동형 Benchmark 재실행
7. Before/After 분석 (A/B/C 3지표 분리 보고)
8. Concurrency/Physical Dispatch 재평가 (ready_set 데이터 근거)
9. Post-Tuning Framework Improvement Track 개시 (백로그 문서)
```

- 수정 1: T4-①(delegation 참조형)은 재시도 원인 제거를 겸하므로 T3 웨이브에 탑재 가능한 소형 변경으로 앞당김 허용 [2차 인과 실증 근거].
- 수정 2: T5는 기술적 의존이 없어 어느 시점이든 무간섭 — 단 "엔진 개선"과 측정을 섞지 않는 조건으로 조기 실행 허용.
- 검증 관점: 순서 0→1이 없으면 2~4의 효과 주장이 [근사]로 떨어짐 — 측정 우선 원칙이 실측 근거상 타당(1차 분석 자체가 수동 추출로 재현성 취약했음).

## 6. 다음 세션 착수 절차 (즉시 실행 가능 형태)

1. T0: 분석 문서 3종 커밋(사용자 승인) + 앵커 확정(`ad451ee`/`dd2fd73`).
2. T1: 집계 스크립트(격리 지점) 작성·Baseline 수치 재산출 대조 → CP2(결정적 검증 우선 적용의 첫 사례로 자기 적용).
3. T2 설계·구현: stale 규칙 3종 문면 확정 → Reuse Assessment(정책 데이터 표현 가능성) → 구현+pytest → 섀도 대조 run.
4. 이후 §5 순서.

각 웨이브는 기존 관행(위임 8필드·CP2 독립 판정·CP2 후 커밋[L-28 후보 준수]·사용자 게이트) 유지.
