# Baseline Performance & Cost Analysis — v1.7 Dogfooding E2E

작성: Advisor · 2026-07-14 · 분석 전용(코드·설정·스펙 무수정·미커밋)
대상: 마일스톤 v1.7 「첫 실제 신규 외부 소비 프로젝트(UAHF Control Plane) + OQ-PO-B4 해소」 전체 실행
근거: 물리 evidence 교차 검증 — invoke 로그 37건 전수 파싱(duration_ms·total_cost_usd·usage)·git 커밋 타임스탬프(양 저장소)·파일 mtime 앵커·events/revisions 원장 + 주 세션 실행 관측(하네스 서브에이전트 토큰/시간은 완료 통지 실측치)
수치 등급 표기: **[확인]** 물리 로그 실측 · **[계산]** 실측치 합산/도출 · **[근사]** mtime/관측 기반 추정 · **[불가]** 측정 수단 부재

---

## 1. Executive Summary

v1.7은 총 경과 약 **10.8시간** [근사] 중 **약 5.4시간(50%)이 야간 사용자 게이트 대기**(T8, 01:06→06:33)였고, 능동 처리 시간은 약 **5.3시간** [근사]이다. 능동 시간의 3대 소비처는 ① **하네스 서브에이전트(드라이버 저술 Worker 3회 + CP2 8회 + Memory 1회) ≈ 128분** [계산], ② **실 CLI step 세션 37개 ≈ 93분·$24.15** [확인], ③ 주 세션 조율·사용자 Q&A [불가]다.

최대 낭비 후보는 품질 보장과 무관한 **구조적 중복**이다: (a) review 게이트가 이미 CP2를 통과한 unit에 **동일 Verifier LLM 세션을 재기동**(9세션·17.4분·$4.51 = CLI 비용의 18.7%) — 게이트 판정은 기존 cp2-pass 이벤트 소비로 대체 가능(PO-INV 4 훼손 없음), (b) **CP2 모델이 step 모델을 추종**해 m/w의 전 검증이 sonnet으로 실행(k의 haiku CP2 대비 세션당 비용 약 10배 — OQ-SH-4로 이미 확보된 cp2 모델 슬롯 미활용), (c) **Task 스키마의 task↔delegation 문면 중복**이 번들·검증·원장 전반에서 토큰을 약 2배로 부풀림(cacheRead 총 28.0M의 주요 성분). 1회성 비용(드라이버 저술 3회 + 스모크 + Scaffold 검증 ≈ 능동 시간의 약 35%)을 제외하면, **반복 실행의 구조적 병목은 "게이트 대기 통지 부재 → 게이트 재검증 중복 → CP2 모델·깊이 정책 → 직렬 디스패치" 순**이며, 물리 동시 디스패치는 이번 실측 기준 4순위다(w run의 DAG가 본질적으로 직렬이라 이번 실행에서의 절감 여지는 m run propose 쌍 ~4.5분에 불과).

## 2. Baseline Facts

| 항목 | 값 | 등급 |
|---|---|---|
| 총 경과 (플랜 승인 ~21:55 → 마감 커밋 08:44) | ≈ 10.8 h | 근사 |
| 야간 T8 게이트 대기 (reviewing-record 01:06 → W3 완주 커밋 06:33) | ≈ 5.45 h | 계산(mtime·커밋) |
| 능동 처리 시간 | ≈ 5.3 h | 근사 |
| 실 CLI step 세션 (k+m+w) | **37개** | 확인 |
| CLI 세션 총 실행 시간 | **5,598 s = 93.3 min** | 확인 |
| CLI 총 비용 | **$24.15** (k $0.99 · m $8.31 · w $14.85) | 확인 |
| CLI 토큰 — output | **463,124** | 확인 |
| CLI 토큰 — input(비캐시) | 22,805 | 확인 |
| CLI 토큰 — cache read / write | **28,041,751 / 1,507,963** | 확인 |
| 하네스 서브에이전트 (Explore 3·Worker 5·Verifier 8·Memory 1) | **17개** | 확인(통지) |
| 하네스 서브에이전트 토큰 합 | ≈ **1,911k** (하네스 보고 단위) | 계산(통지 합산) |
| 하네스 서브에이전트 시간 합 | ≈ **7,923 s = 132 min** (일부 병렬 중첩) | 계산 |
| 사용자 게이트 (실 해소) | 6회 (k 1 · m 2 · w 1 · G2 1 · Baseline 1) + 계획/질문 게이트 | 확인 |
| CP2 독립 판정 (하네스 레벨) | 8회 전건 Pass | 확인 |
| 재시도 (rework 루프) | 1회 (w impl-plan — Worker+Verifier 재기동 341s·$1.87) | 확인 |
| 주 세션(Advisor) 토큰·비용 | — | 불가(하네스 미노출) |
| 하네스 서브에이전트 비용(USD) | — | 불가(토큰만 보고됨) |

## 3. E2E Critical Path

단계별 재구성 (시간 앵커 = 커밋·mtime·통지 실측):

| # | 단계 | 시간 | 세션 | LLM 호출 | 비용 | 사용자 대기 | 병렬화 | 반복성 | 1회성/구조 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 세션 진입(Entry Resolution·Consult) | ~10 min [근사] | 0 | 주 세션 | 불가 | — | — | — | 구조(경량) |
| 2 | 플랜 수립(Explore×3 병렬·질문 2회·이미지) | ~35 min [근사] | 3 | 3+주 세션 | 불가(322k tok) | 질문 응답 | 이미 병렬 | — | 1회성(트랙 계획) |
| 3 | W0 드라이버 저술+CP2 | 738+400 s [확인] | 2 | 2 | 불가(229k tok) | — | 순차(의존) | 드라이버 자산화 | **1회성** |
| 4 | W0 k run (Phase1+게이트+Phase2+replay) | ~11 min [계산: CLI 355 s+조율] | 8 CLI | 8 | $0.99 | 게이트 1 (~2 min) | p1 CP2와 impl 중첩 불가(직렬 DAG) | — | **1회성**(스모크) |
| 5 | W0 run CP2 ‖ W1 Discovery(질문 2라운드·G2) | 369 s ‖ ~25 min [근사] | 1 | 1+주 세션 | 불가 | Eliciting 응답 | **병렬 실행됨** | — | 구조(Discovery는 반복) |
| 6 | Contract v1 컴파일·프로젝트 생성·커밋 | ~8 min [근사] | 0 | 주 세션 | 불가 | — | — | — | 구조(경량) |
| 7 | W1 CP2 ‖ W2 Scaffold 설치 Worker | 349 ‖ 551 s [확인] | 2 | 2 | 불가(259k tok) | — | **병렬 실행됨** | — | W2=1회성/프로젝트 |
| 8 | W2 CP2 | 390 s [확인] | 1 | 1 | 불가(93k tok) | — | 순차 | — | 1회성/프로젝트 |
| 9 | W3 드라이버 저술+CP2 | 929+478 s [확인] | 2 | 2 | 불가(253k tok) | — | 순차 | 자산화 | **1회성** |
| 10 | m run Phase1 (assess+CP2) | 513 s [확인] | 2 CLI | 2 | $1.94 | — | 직렬(단일 task) | — | 구조 |
| 11 | 구조 게이트+resolve+supersede | ~7 min [근사] | 0 | 주 세션 | — | 게이트 1 (~4 min) | — | — | 구조 |
| 12 | m run Phase2 (propose×2→reconcile→review+CP2+게이트재검증) | 1,579 s [확인] | 11 CLI | 11 | $6.37 | — | **propose 쌍 병렬 가능(미실행)** | 게이트 재검증 3 중복 | 구조 |
| 13 | **T8 게이트 대기(야간)** | **~5.45 h** [계산] | 0 | 0 | $0 | **전부** | — | — | 구조(통지 부재) |
| 14 | v2 발행·SD 로그·커밋 | ~10 min [근사] | 0 | 주 세션 | — | T8 응답 | — | — | 구조(경량) |
| 15 | W3 run CP2 ‖ W4 드라이버 저술 | 616 ‖ 750 s [확인] | 2 | 2 | 불가(286k tok) | — | **병렬 실행됨** | — | CP2=구조·드라이버=1회성 |
| 16 | W4 드라이버 CP2 | 504 s [확인] | 1 | 1 | 불가(97k tok) | — | 순차 | — | 1회성 |
| 17 | w run Phase1 (impl-plan+CP2+재시도) | 813 s [확인] | 4 CLI | 4 | $3.66 | — | 직렬(재시도 포함) | 재시도=품질 루프 | 구조 |
| 18 | 계획 게이트+resolve | ~3 min [근사] | 0 | 주 세션 | — | 게이트 1 | — | — | 구조 |
| 19 | w run 구현 위상 (4 task+CP2+게이트재검증) | 2,337 s [확인] | 12 CLI | 12 | $11.19 | — | **DAG 직렬(병렬 여지 0)** — CP2↔차기 Worker 중첩만 가능 | 게이트 재검증 4 중복 | 구조 |
| 20 | MVP 실동작 확인(서버·curl) | ~3 min [확인] | 0 | 0 | ~$0 | — | — | — | 구조(경량) |
| 21 | W4 run CP2 | 890 s [확인] | 1 | 1 | 불가(155k tok) | — | 순차(커밋 게이트) | — | 구조 |
| 22 | 커밋·Handoff·ROADMAP·Memory Worker·Baseline 게이트 | ~35 min [근사] (Memory 705 s 포함) | 1 | 1+주 세션 | 불가(122k tok) | Baseline 응답 | 부분 병렬 실행됨 | — | 구조(마감) |

**Critical Path 요지**: 능동 시간의 최장 직렬 사슬 = 플랜(35) → W0 드라이버+CP2(19) → k run(11) → W1(25, CP2 병렬 처리됨) → 컴파일(8) → W2(9+6.5) → W3 드라이버+CP2(23.5) → m run(35+게이트) → v2(10) → W4 드라이버(12.5, W3 CP2 병렬)+CP2(8.4) → w run(52.5) → MVP 확인(3) → W4 CP2(15) → 마감(35) ≈ **약 5.2 h** — 능동 시간과 거의 일치(주 세션이 이미 병렬 위임을 3회 활용했음에도 대부분 구간이 직렬).

## 4. Top Bottlenecks (분류·상세는 §12~§14)

| 순위 | 병목 | 규모 | 분류 |
|---|---|---|---|
| 1 | **게이트 대기 통지 부재** (야간 T8 5.45 h — 총 경과의 50%) | 경과 시간 지배 | P0·구조 |
| 2 | **review 게이트 재검증 중복** (CP2 통과 unit에 Verifier 재기동 9세션·1,043 s·$4.51) | CLI 비용 18.7%·시간 18.6% | P0·구조 |
| 3 | **CP2 모델 정책 미활용** (m/w 검증 전부 sonnet — haiku CP2 대비 ~10배 비용·OQ-SH-4 슬롯 미사용) | 검증 세션 23개 중 21개 sonnet | P0·구조 |
| 4 | **하네스 CP2 깊이 균일** (드라이버 CP2 3회+run CP2 5회 전부 최대 깊이 — 결정적 검사를 LLM이 반복 재구현) | ~44분·~800k tok | P1·구조 |
| 5 | **Task 문면 중복(task≡delegation.task)** — 번들·원장·검증 전반 토큰 2배 성분 | cacheRead 28.0M의 주성분 | P1·구조 |
| 6 | 직렬 디스패치 (m propose 쌍·CP2↔차기 Worker 중첩 부재) | 이번 실측 절감 여지 ~9–12 min | P2·구조 |
| 7 | 드라이버 저술+검증 (3회·~63 min) | 능동 시간 ~20% | 1회성(자산화 완료) |

## 5. Time Analysis

- **경과 대비**: 게이트 대기(야간) 5.45 h(50%) ≫ 능동 5.3 h(50%).
- **능동 시간 분해** [계산/근사]: 하네스 서브에이전트 132 min(중첩 감안 임계 경로 기여 ~105 min) > CLI step 93 min > 주 세션 조율·문서·게이트 제시 ~60–80 min > 사용자 응답(주간) ~15 min.
- **CLI 시간 분해** [확인]: Worker 실행 3,017 s(54%) · CP2 검증 1,538 s(27%) · 게이트 재검증 1,043 s(19%). 최장 단일 세션 = ui-layer-panels Worker 435 s·data-layer 425 s·impl-plan 331 s·assess 337 s·review 305 s.
- **재시도**: impl-plan rework 루프 +341 s — 실 결함(delegation 문면 축약)을 잡은 품질 지출. 유지.
- **병렬화 실효**: 주 세션 레벨은 이미 3구간 병렬(W0CP2‖W1, W1CP2‖W2, W3CP2‖W4드라이버). run 내부는 전무 — m의 propose 쌍(ready_set 동시 2)이 직렬로 소비된 것이 유일한 실측 병렬 기회(추정 절감 269 s+CP2 중첩 ~4.5 min).

## 6. Token / Cost Analysis

- **CLI 비용 $24.15** [확인]: w $14.85(61%) > m $8.31(34%) > k $0.99(4%). 모델별 — sonnet 세션 31개 $23.9 · haiku 6개(k) $0.26. **k가 증명한 것**: 소형 task는 haiku Worker+haiku CP2로 세션당 $0.03–0.07에 처리 가능.
- **캐시 지배 구조**: 비캐시 input 22.8k에 불과하나 cacheRead 28.0M — fresh-context 세션마다 시스템 프롬프트+번들+파일 재독이 캐시로 흡수되나 캐시 읽기도 과금 대상. w run 평균 세션당 cacheRead 1.16M(최대 env-build-smoke Worker 3.32M — npm 출력·반복 파일 열람).
- **번들 중복 성분**: Task 스키마가 task 전문을 delegation.task에 재수록(delegation.done도 동일) — impl-plan.json·revisions.jsonl·steps 직렬화·CP2 입력 전부에서 문면 2배. w의 4 task 문면이 원장·번들·검증에 최소 3회 이상 재등장.
- **하네스 토큰** [계산]: 서브에이전트 합 ≈1,911k(보고 단위). 최대 소비 = W3 드라이버 Worker 157k·W4 run CP2 155k·W1 CP2 146k·W4 드라이버 Worker 147k. 검증 계열 합 ≈803k(42%).
- **비용 불가 항목**: 주 세션·서브에이전트 USD 환산(하네스 미노출) — telemetry 제안 §15.

## 7. Session / Context Analysis

- **37 CLI 세션의 구성** [확인]: Worker step 14(재시도 1 포함) · CP2 14(재검증 1 포함) · 게이트 재검증 9.
- **필수 fresh-context**: step Worker(설계·구현의 독립 판단)·CP2 Verifier(독립성 보장) — 이 격리는 UAHF 핵심 보장으로 유지 대상.
- **구조 때문에 반복된 fresh-context**: ① 게이트 재검증 9세션 — 동일 unit·동일 evidence를 CP2 직후 다시 읽는 신규 세션(독립성 이득 없음: 같은 Verifier 역할·같은 판정 기준·수 분 간격), ② 재검증 세션의 반복 원문 로딩(예: env-build-smoke 검증 2회가 각각 번들+워크스페이스 재독 — cR 1.23M+2.09M).
- **반복 원문 로딩**: Contract v2·reconciling-record는 w run에서 impl-plan(1회)+각 구현 task 문면 인용으로 소비 — 구현 step들은 원문 대신 task 문면 내 인용으로 충분했음(실제로 그렇게 설계됨 — 양호). 반면 검증 세션들은 매회 원장 원문 전체를 재독.
- **startup 비용**: 세션당 cacheWrite 평균 40.8k(시스템+번들 신규 캐시 등록) — 세션 수 자체가 곱해지는 고정비.
- **합칠 수 있는 것**: 게이트 재검증→CP2 결과 소비(세션 0개화)·소형 인접 검증(replay+위생 등 결정적 검사)→CLI 도구화. **합치면 안 되는 것**: Worker↔Verifier(독립성)·서로 다른 unit의 Worker(fresh-context 격리·오염 방지)·사용자 게이트.

## 8. Verification Analysis

- **CP2 집계**: 하네스 레벨 8회(드라이버 3·run 증거 5) ≈ 44 min·~803k tok [계산] + CLI 레벨 step CP2 14회 1,538 s·$7.0 [확인] + 게이트 재검증 9회 1,043 s·$4.51 [확인].
- **깊이 균일의 비효율**: 저위험 산출(setup 트리 실재·JSON 파싱·계수 일치·git 위생·seq 단조·해시 불변)이 고위험 산출(시나리오 계약 의미 정합·정직성 문면)과 동일하게 LLM 세션에서 검증됨. 8회의 하네스 CP2가 각자 bash/python 검사 스크립트를 **재작성**함 — 동일 검사 로직이 세션마다 재발명됨.
- **결정적 대체 가능 항목**(품질 동등·비용 급감): seq 단조/결락·이벤트 어휘 집합·게이트 순서(required→provenance→resolved)·simulated 라벨 스캔·revision basis 필수 필드·blob 해시 불변·git porcelain 위생·계수 정합(store↔index)·replay 2회 동일성. → 재사용 가능한 검증 CLI 1개면 8회 CP2의 아마도 40–60% 분량이 종료 코드 판정으로 대체 가능(LLM 검증은 의미 정합·정직성·계약 해석에 집중).
- **LLM Verifier가 반드시 필요한 부분**: 문면 계약 해석(프롬프트가 요구를 담는가)·설계-근거 정합·정직성 판단·완료 보고 대조.
- **risk-based 가능성**: 드라이버(1회성·자산)는 첫 CP2 후 재사용 시 재검증 불요(변경 시에만). run 증거는 결정적 검사 통과 + 표본 LLM 심층 검증(예: 신규 패턴 unit만)으로 계층화 가능.

## 9. Orchestration / Concurrency Analysis

- **현재 루프** [코드 실측]: fold→ready_set→**순차** dispatch(Worker→CP2→게이트 처리)→append→다음. 물리 병렬성 0.
- **이번 실행의 실제 병렬 기회**: m run에서 ready_set=["propose-data","propose-ui"] 동시 2 — 직렬 소비로 269 s(Worker)+α(CP2 중첩) 손실. w run DAG는 완전 직렬(scaffold→data→ui→env)이라 **task 병렬 여지 0**. k run도 직렬.
- **CP2 파이프라이닝**: task N의 CP2와 task N+1의 Worker는 의존 무관(CP2는 판정 기록·N+1은 N의 산출만 소비) — 중첩 시 m에서 ~500 s, w에서 ~540 s 임계 경로 단축 추정 [계산]. 단 게이트 정지 의미론(중간 Fail 시 N+1 무효화)·evidence append 경합(단일 events.jsonl append 직렬화 필요)·retry 의미론 재정의 필요 — 중위험.
- **판정**: **물리 동시 디스패치는 이번 evidence 기준 최우선 병목이 아니다.** 이번 파이프라인 유형(설계 사슬·구현 사슬)에서 절감 상한 ~9–12 min(능동 시간의 ~3–4%). 게이트 통지(경과 50%)·재검증 중복(19%)·모델 정책이 선행 순위. 단 **미래 다(多)관심사 프로젝트**(propose×3·독립 구현 task 다수)에서는 가치가 상승하므로 P2로 유지.

## 10. Tool / CLI / Skill Opportunity Analysis (향후 후보 — 이번 미구현)

| LLM이 수행했으나 결정적 도구가 적합했던 작업 | 발생 지점 | 후보 |
|---|---|---|
| 원장 스키마·순서·라벨 검사(seq·어휘·게이트 순서·simulated 스캔) | 하네스 CP2 8회·CLI 게이트 재검증 | `uahf-verify ledger <run-dir>` CLI |
| 해시 불변·git 위생·보호 경계 검사 | CP2 다수 | `uahf-verify hygiene` |
| replay 2회 대조 | CP2 3회 | 러너 내장 플래그(`--replay-check`) |
| store↔index 계수·byte 대조 (Memory) | Memory Worker+검증 | `uahf-memory verify` |
| done AC 일괄 실행 | run CP2들 | 러너가 AC 재실행 리포트 자동 산출 |
| 빌드/타입체크 재확인 | W4 CP2 | 이미 AC로 존재 — CP2에서 재실행 대신 결과 소비 |
| Scaffold 설치·VerifyInstall | W2 Worker/CP2 | Skill/CLI 캡슐화(12-scaffold 형태 B와 정합) |
| 반복 게이트 제시·해소 기록 | resolve_k/m/w 3벌 | 공통 `uahf-gate resolve` CLI(드라이버 중복 제거) |

Skill 캡슐화 후보(재사용 계열): scaffold-install · ledger-verify · run-report(요약 생성) · gate-resolve. 정보 손실 없는 요약 소비(예: 검증 세션에 원장 원문 대신 검증 CLI 리포트+표본 원문)도 여기 결합.

## 11. One-time vs Structural Cost

| 1회성 (이번 트랙 특수) | 규모 | 반복 실행 시 |
|---|---|---|
| 드라이버 k/m/w 저술 Worker 3회 | 2,417 s·~452k tok | **0** (자산 재사용) |
| 드라이버 CP2 3회 | 1,382 s·~273k tok | 0 (무변경 시) |
| W0 스모크 run 전체 | ~11 min·$0.99 | 0 |
| Scaffold 설치+CP2 | ~16 min·~206k tok | 프로젝트당 1회(도구화 시 분 단위) |
| 플랜 수립 Explore·트랙 설계 | ~35 min·322k tok | 트랙 성격별 축소 |
| Memory 관례 학습(Worker의 정독) | 705 s 중 상당분 | 도구화 시 급감 |
| **소계** | **능동 시간의 ~35–40%** | |

| 구조적 (반복 발생) | 규모/회 | 비고 |
|---|---|---|
| Discovery 질문 루프+G2 | ~25 min | 사용자 상호작용 본질 |
| 성숙 run (호스팅) | ~35 min·$8.3 | propose 병렬·모델 정책으로 단축 여지 |
| 구현 run | ~50 min·$14.9 | 규모 비례·재검증 중복 제거 여지 |
| run 증거 CP2 | 10–15 min·~150k tok/회 | 결정적 대체·위험 기반 계층화 여지 |
| 게이트 대기 | 사용자 가용성 의존 | 통지로 급감 가능 |
| 마감(핸드오프·Memory·커밋) | ~35 min | 부분 도구화 여지 |

## 12. Quick Wins

| 후보 | Impact | Effort | Risk | Measurability |
|---|---|---|---|---|
| QW-1 게이트 정지 시 **사용자 통지**(푸시/텔레그램 — exit 2 훅) | 경과 시간 최대(-수 시간) | 소 | 극소(보장 무촉) | 게이트 대기 시각 로그로 직접 |
| QW-2 **review 게이트의 CP2 결과 소비**(재검증 세션 제거 — gate_policy 데이터/드라이버 수준) | CLI -19% 시간·비용 | 소–중 | 소(게이트 판정 자체는 유지·근거=기존 cp2-pass 이벤트) | 세션 수·비용 직접 비교 |
| QW-3 **CP2 모델 슬롯 분리 적용**(model_selection cp2Slot=haiku, 고위험 unit만 sonnet) | 검증 비용 -50~70% | 소(정책 데이터) | 중(검증 품질 — 표본 대조로 완화) | CP2 비용·Fail 검출율 |
| QW-4 **task↔delegation 문면 중복 제거**(참조화 — 드라이버/제안 프롬프트 수준) | 번들·원장 토큰 -30%± | 소 | 소(스키마 소비자 확인 필요) | cacheRead/세션 |
| QW-5 러너 **run-summary 자동 산출**(세션·시간·비용·토큰 집계 JSON) | 측정 기반 확보 | 소 | 0 | 즉시 |

## 13. Structural Tuning Candidates

| 후보 | Impact | Effort | Risk | Measurability |
|---|---|---|---|---|
| ST-1 검증 계층화: 결정적 검증 CLI(`uahf-verify`) + 위험 기반 LLM 심층 검증 | 하네스 CP2 -40~60%·CLI CP2 일부 | 중 | 중(검증 누락 — 커버리지 맵으로 완화) | CP2 시간/토큰·검출율 |
| ST-2 CP2↔차기 Worker 파이프라이닝(orchestrator 비동기 1단) | run 임계 -15~25% | 중–대 | 중(append 직렬화·Fail 전파 의미론) | run wall-clock |
| ST-3 물리 동시 디스패치(ready_set 병렬 invoker) | 이번 유형 ~3–4%·다관심사 프로젝트에서 상승 | 대 | 중–대(evidence 경합·워크스페이스 격리[worktree Defer 승계]) | ready 동시성 활용율 |
| ST-4 context 계층화: 검증 세션에 원문 대신 검증 리포트+표본 | 검증 토큰 -30%± | 중 | 중(정보 손실 — 원문 접근권 유지로 완화) | cacheRead/검증 |
| ST-5 마감 도구화(Memory append·핸드오프 골격 생성 CLI) | 마감 -15 min | 중 | 소 | 마감 소요 |
| ST-6 게이트 큐 일괄 제시(다게이트 묶음) | 게이트 왕복 수 감소 | 중 | 중(승인 granularity 보존 필요) | 게이트 왕복 수 |

## 14. Prioritized Tuning Roadmap

1. **P0**: QW-1(게이트 통지) → QW-2(재검증 중복 제거) → QW-3(CP2 모델 정책) — 전부 게이트·검증 **보장 유지** 하에 경과 -50%±·CLI 비용 -30%± 기대.
2. **P1**: QW-4(문면 중복 제거)+QW-5(telemetry)+ST-1(검증 계층화 1단계 — 결정적 CLI 도입, LLM 검증은 의미 축 전담).
3. **P2**: ST-2(CP2 파이프라이닝) → ST-3(물리 동시 디스패치 — 다관심사 워크로드 확보 후 재평가) → ST-4.
4. **P3**: ST-5·ST-6·Skill 체계 도입(§10 카탈로그).

## 15. Before/After Measurement Plan

기준 지표(이번 Baseline 값 병기):

| 지표 | Baseline | 수집 방법(제안 telemetry) |
|---|---|---|
| Total wall-clock | ≈10.8 h | 트랙 시작/마감 커밋 타임스탬프 |
| Critical path duration(능동) | ≈5.3 h | 주 세션 단계 로그(신규) |
| Total LLM sessions (CLI/하네스) | 37 / 17 | 러너 run-summary + 하네스 통지 집계 |
| Fresh-context sessions | 37 | 동상 |
| Tokens in/out (CLI) | 22.8k / 463k | invoke 로그 집계(자동화) |
| Cache read/write (CLI) | 28.0M / 1.51M | 동상 |
| Total cost (CLI) | $24.15 | 동상 |
| CP2 count (하네스/CLI/게이트재검증) | 8 / 14 / 9 | run-summary·통지 |
| Verification cost 비율 | CLI의 46%(CP2+재검증) | 동상 |
| User gate waiting | ≈5.5 h(야간 포함)·게이트 6회 | **게이트 이벤트에 벽시계 ts 별도 필드**(L-09 정합 — 순서 값과 분리) |
| Parallelizable idle | m propose 쌍 269 s+α | ready_set 크기 vs 실제 동시 실행 로그 |
| Repeated context loading | cacheRead/세션 평균 758k | run-summary |
| Retry count | 1 (impl-plan) | events retry_count 집계 |
| Verification pass rate | CP2 첫판정 8/8·step CP2 rework 1 | 동상 |

**제안 telemetry(미구현·후보)**: ① 러너 종료 시 `run-summary.json`(세션·시간·비용·토큰·게이트 타임라인) 자동 append, ② 게이트 이벤트에 벽시계 ts 필드(순서 값 전속 원칙과 분리 명기), ③ 하네스 서브에이전트 비용 노출 수집 절차, ④ 주 세션 단계 마커 로그.

## 16. Unknowns / Missing Telemetry

- 주 세션(Advisor) 토큰·비용 — 하네스 미노출 [불가].
- 하네스 서브에이전트 USD 비용 — 토큰만 보고 [불가].
- 게이트 정지→해소 정밀 대기 시간 — 이벤트에 벽시계 부재(mtime 근사만) [근사].
- 세션 startup 고정비(모델 로드·캐시 등록)의 분리 계측 [불가].
- CLI cacheRead의 과금 단가 반영 정밀 비용 분해(총액만 확인) [계산 한계].
- Explore/플랜 단계 세부 시간(대화 로그 타임스탬프 미추출) [근사].

---

## ⭐ 가장 먼저 튜닝할 3가지

1. **게이트 정지 사용자 통지 (QW-1)** — 근거: 총 경과 10.8 h의 **50%(≈5.45 h)**가 단일 야간 게이트 대기였음(reviewing-record 01:06 → 해소 후 커밋 06:33 실측). exit 2 훅에 푸시/텔레그램 1건이면 품질 보장 무촉·최대 절감. 측정: 게이트 벽시계 ts 도입 후 대기 시간 직접 비교.
2. **review 게이트 재검증 중복 제거 (QW-2)** — 근거: CP2 통과 unit에 동일 역할 Verifier 세션이 재기동된 것이 **9/37 세션·1,043 s·$4.51(CLI 비용 18.7%)** [확인]. 게이트 판정을 기존 cp2-pass 이벤트 소비로 전환해도 PO-INV 4(게이트 하한)·독립 검증(CP2 자체)은 불변 — 같은 보장을 더 싸게.
3. **CP2 모델·깊이 정책 (QW-3 + ST-1 1단계)** — 근거: 검증이 CLI 시간의 46%를 차지하며 m/w의 검증 21세션이 전부 sonnet(세션당 $0.29–1.17)인 반면 k는 haiku CP2($0.03–0.07)로 동일 구조 검증을 통과시켰음 [확인]. OQ-SH-4로 이미 확보된 cp2 모델 슬롯 + 결정적 검사의 CLI화(원장 스키마·순서·해시·위생)로 검증 비용 50%± 절감, LLM 검증은 의미 정합에 집중 — 검출력은 표본 대조로 방어.

(물리 동시 디스패치는 이번 evidence 기준 4순위 — w run DAG가 본질 직렬이라 이번 유형 절감 상한 ~3–4%. 다관심사 워크로드가 생기는 시점에 ST-3로 재평가 권고.)
