# UAHF Session Handoff — v1.1 → 다음 세션

작성일: 2026-07-07
작성자: Worker (Advisor 위임, Task T11)
목적: 이 문서만 읽어도 새 세션이 v1.1 이후 작업을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v1.0.md, v0.9, v0.8, v0.7, v0.6, v0.5, v0.4, v0.3, v0.2, v0.1)
상태: v1.1 Baseline (CP2 첫 판정 Pass 15/0/0 — v0.5부터 7연속 · CP3 승인 · 사용자 승인 2026-07-07). 사용자 승인 반영 완료 — Advisor가 v1.1 산출물 전건(신규 9 + ROADMAP 개정)에 Baseline 행 append·상태 라인 승격을 수행하고 본 문서 이력에 기록했다. 다음 트랙 = **v1.2 (Project Discovery 구현)** — 사용자 결정 2026-07-07 (§3.1의 후보 (a) 채택).

---

## §9. 이력 (Revision History)

| 일자 | 변경 | 주체 |
|---|---|---|
| 2026-07-07 | 최초 작성 (사용자 승인 대기 상태) | Worker (Advisor 위임, Task T11) |
| 2026-07-07 | v1.1 Baseline 확정 — 사용자 승인 반영 (전 산출물 상태 라인 승격·Baseline 행 append). 다음 트랙 사용자 결정 기록: v1.2 (Project Discovery 구현 — Architecture의 실동작 검증, 검증 중점 5건) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행(v1.1 verification-report·promotion-review·v1.0 handoff 동형). 이후 개정은 이 표에 append-only로 기록한다. 사용자 승인 반영은 별도 행으로 append한다.)

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v1.1 — Project Discovery & Entry Layer)

v1.1은 **UAF 레벨 Architecture 설계만** 수행한다(구현 0). UAHF 6-Layer 컴포넌트 트랙이 아니라 그 상위의 UAF 레벨 신설 트랙이며, 신규 최상위 경계 `uaf/`에 UAF 정본을 두고 **UAHF 정본은 무수정**으로 유지한다(접점 = Project Contract 하나).

1. **세션 진입 절차 이행** — handoff v1.0 정독 → **Consult 실수행(8회째 실가동)**: index.jsonl **71라인**(착수 시점) 스캔, 회수 집합 = Active Lesson 15건(L-01~L-15) + Active Best Practice 5건(BP-01·BP-02·BP-03·BPD-06·BPD-11) = **20건**(detail=full).
2. **비판적 검토 선행(사용자 지시)** — 설계 착수 전 v1.1 목표·경계를 비판적으로 검토 → **수정안 사용자 승인** → 사용자가 Architecture 고정 원칙 P1~P5 + 확인 3건(C1~C3)을 추가 확정.
3. **Execution Plan 수립** — Planner 초안(`model: opus`, DP-E8) → **Advisor 채택**·OQ 6건 해소 → **사용자 승인**(계획 모드 — 사용자 결정 D1~D6 + 상시 불변 확인 2건 확정, 및 `docs/v1.1-review-brief.md` 삭제 지시).
4. **Wave 실행 (W1~W7, 11 Task = T1~T11)** —
   - **W1 [Layer]**: `uaf/ARCHITECTURE.md`(T1 — § 포인터 오기 폐합 r2 1회).
   - **W2 [Workflow] (2병렬)**: `uaf/specs/01-entry.md`(T2)·`uaf/specs/02-discovery.md` Workflow부(T3).
   - **W3 [Module]**: `uaf/specs/02-discovery.md` Module부(T4 — 실행 중단[스트림] 후 재개 프로토콜로 결함 0 복구, BPD-13 실증. T3 산출에 이어 같은 문서 완성).
   - **W4 [Contract]**: `uaf/specs/03-project-contract.md`(T5 — 스키마·버저닝·UAHF Interface 최종 고정).
   - **W5 (3병렬)**: 부록 `uaf/appendix/methodology-mapping.md`(T6, 비정본)·`docs/v1.1-scenario-walkthrough.md`(T7 — 시나리오 3건)·`ROADMAP.md` v1.1 등재 개정(T8).
   - **W6 [직렬]**: 마일스톤 CP2(T9 — 독립 Verifier `model: opus`, DP-E8).
   - **W7 [직렬화 — DP-W1]**: 승격 심사(T10 — mi-0075 보충 등록 r2 1회) → 본 핸드오프(T11).
5. **검증 리포트** — docs/v1.1-verification-report.md: **첫 판정 Pass 15/0/0 (v0.5부터 7연속)**. 완료 조건 9건 + 상시 불변 2건 + 거짓 완료 검출 + 산출물 존재 + 방법론 격리 = 항목별 판정 15건 전건 충족. Worker self_check 비근거(06 V1) — 산출물 직접 실측(다중 패턴 grep·mtime·정본 대조)으로 독립 재판정, 거짓 완료 검출 0건.
6. **Memory Update 실가동 8회차** — 심사 등록 4건(mi-0072~0075): **재발 판정 2건(Novel 1·Recurrence 1)·L-20/BPD-13 Candidate 등록·보류·승격 0건**. **store 75파일·index 75라인**, 기존 71건 무변경(append-only·MD5 바이트 대조).

## 1.2 v1.1 완료 조건 대조 (ROADMAP §5 / 승인 계획 §검증 — 전건 충족, T9 §3·§4 근거)

| 완료 조건 | 판정 | 근거 (CP2 § 포인터) |
|---|---|---|
| ① 채택 범위 전 항목이 `uaf/` 정본에 정의 | 충족 | 계획 §설계 골격 4개 문서 bullet ↔ 산출물 § 전수 대조 누락 0(item #2 — ARCHITECTURE §2~§8·01 §3·02 §3·03 §3 매핑) |
| ② 사용자 고정 원칙 5건(P1~P5) 정본 문면 존재 | 충족 | ARCHITECTURE §4 P1~P5 문면 실재·§5 UAF-INV·§6 책임 경계표(담당 4·비담당 5)·P5 설계 순서는 02-discovery Workflow부→Module부 2단계 완성으로 프로세스 실현(item #3) |
| ③ Contract 스키마 코어 필드 Discovery 내부 개념 역참조 0 | 충족 | 03 다중 패턴 grep 실측 — 코어 필드 그룹 1~7에 질문/전략/예산/Strategy/Capability 0건, Readiness는 종단 판정 산출 기록(Open Questions)으로 §3.2-A 경계 명시(item #4) |
| ④ Entry Resolution 결정 테이블 8조합 전수·단일 결과 | 충족 | 01 §3.2-D 표 행 1~8이 `/new`×4·`/continue`×4 전수 열거·각 단일 `→ mode`(중복·누락 0)·§3.2-A 결정성 검증 EN-INV 3(item #5) |
| ⑤ UAHF 정본 무수정 (명시 개정 = ROADMAP 1건) | 충족 | 루트 ARCHITECTURE.md·specs/ 15종·framework/ 문서 전체·.claude/ 표면 mtime·상태 라인·콘텐츠 성격 실측 — v1.1 Wave 착수 이후 수정 0, ROADMAP만 명시 예외. 운영 데이터(memory-data/·loop-data/) v1.1 append 0(정상, DP-W3)(item #6) |
| ⑥ 시나리오 워크스루 3건 통과 | 충족 | (A) Greenfield /new·(B) Brownfield /continue 최초 도입 State Machine 완주(Ready 종단·2축 판정식)·(C) 가상 /import 무변경 대조(Layer·엔진·State Machine·Event Model·Contract 무변경 — 변경=데이터 추가 4건). 인용 전이·행·필드 정본 일치(item #7) |
| ⑦ 사용자 확인 3건(C1·C2·C3) 정본 문면 존재 | 충족 | C1 Entry Descriptor 등록 모델·고정 엔진(01 §3.2-A·§8 예3)·C2 SemVer+tolerant reader+필드 제거 금지(03 §3.3-B/C/D)·C3 Ready 2축 판정식·Completeness 타협 불가(02 §3.7)(item #8) |
| ⑧ `uaf/` 정본 본문 특정 AI 실명·모델명·제품 기능명 0 | 충족 | uaf/ 트리 전체 다중 패턴 case-insensitive grep 매치 0·각 §0 AI 비의존 선언·물리 실현 §4 Adapter Binding 격리(item #9) |
| ⑨ 전 산출물 관행 규격(상태 라인·§9 이력·§ 포인터 재정의 0) 보유 | 충족 | 7개 산출물 머리 상태 라인 "v1.1 Draft" + §9(또는 #8) 이력 표 + §0/근거 정본 절 § 포인터 재정의 0 실측(item #10) |

상시 불변 확인 2건(매 게이트 공통 판정)도 충족: ① Discovery 교체 가능성 보존(내부 개념 Contract 코어/UAHF 접점 누출 0 — item #11)·② Contract 장기 호환 규칙(SemVer·tolerant reader·필드 제거 금지) 훼손 0(item #12).

## 1.3 이번 세션의 설계 결정 (사용자 6건 + 상시 불변 2건 + Advisor 12건)

**사용자 결정 (계획 모드 승인 — D1~D6):**

| 결정 | 내용 |
|---|---|
| **D1** | **위상·정본 배치.** Entry Layer·Project Discovery는 UAHF 6-Layer **외부**의 **UAF 레벨 구조**. 신규 최상위 경계 `uaf/`에 UAF 정본 신설. **UAHF 정본(ARCHITECTURE.md·specs 15종·framework/·.claude/) 무수정**(Glossary INV-3 무촉). 접점은 **Project Contract 하나뿐** |
| **D2** | **범위 수정안 전부 수용.** ① State Machine **단일 정본** + 파생 뷰 3(Lifecycle=단계·Process=역할/책임·Workflow=오케스트레이션) ② Metrics는 **원칙 수준**(Event 파생 가능 + 최소 분류) — 상세 스키마 구현 이연 ③ 방법론 분석(grill-me·JTBD·Shape Up·Design Sprint·Event Storming)은 **비정본 부록** 격리, 정본은 Strategy Provider Interface만 ④ 추가 6건(Contract 버저닝·Ready 게이트·실패/중단 경로·하위 호환·Brownfield 판별·완료 조건) ⑤ Non-Goal 2건(Discovery 실행 호스팅·Memory 활용은 확장 포인트만) |
| **D3** | **Entry 판별.** 기존 저장소 + Contract 부재(최초 도입) = **/continue 소관** Brownfield Full Discovery. /new는 순수 Greenfield 전용. /new + Contract 존재 = **사용자 확인**(Human Authority) |
| **D4** | **프로세스.** v0.1~v1.0 확립 마일스톤 풀 프로토콜(Planner 초안 → Advisor 채택 → Wave 병렬 Worker → Verifier CP2 → CP3 → 핸드오프 → 사용자 승인 Baseline). Verifier·Planner 위임 `model: opus`(DP-E8) |
| **D5** | **고정 Architecture 원칙 P1~P5.** P1 Entry=Resolution만·Discovery 비수행 / P2 Discovery=Project Contract 생성 Compiler + **Strategy Invariance** / P3 Contract=UAF↔UAHF 공식 **Stable Contract(Public API)** / P4 책임 담당 4·비담당 5 경계표 / P5 설계 순서 = **Layer → Workflow → Module → Contract** |
| **D6** | **사용자 확인 3건(설계 반영 확약).** C1 Entry Resolution 확장성(Entry Descriptor 등록 모델 + Evidence Source 확장 스키마 + 가상 /import 워크스루로 검증) / C2 Contract Versioning(schemaVersion SemVer 규율·tolerant reader·필드 제거 금지) / C3 Execution Ready 2축 판정(Completeness ∧ Confidence ∧ 사용자 승인·Completeness 타협 불가) |

**상시 불변 확인 2건(사용자 재확인 지시 — 매 게이트 판정 공통):** ① Project Discovery는 단일 기능이 아니라 **Project Contract를 생성하는 Compiler**다 — 산출물이 Discovery를 언제든 교체 가능하게 유지하는가(내부 개념 누출 0). ② Project Contract는 UAF↔UAHF 공식 **Stable Contract(Public API)**다 — 장기 호환 규칙이 훼손되지 않는가. 이 두 확인을 통과하지 못한 산출물은 승인하지 않는다.

**Advisor 결정 12건 (DP-W1~DP-W12 — 전부 확정·기록):**

| 결정 | 내용 |
|---|---|
| **DP-W1** | W7 직렬화 — 계획 병렬 2(T10·T11)를 직렬(T10 승격 심사 → T11 핸드오프)로 전환. 핸드오프는 승격 심사의 확정 계수를 입력으로 하므로 선후 고정 |
| **DP-W2** | `structure.md` 무개정 — §8 트리가 `framework/` 하위만 열거(루트 미열거) 실측 → 계획의 조건부 개정("저장소 루트 전체 열거 시 uaf/ 추가") 미발동. structure.md 무수정이 정당 |
| **DP-W3** | append-only 운영 데이터(memory-data/·loop-data/)는 "UAHF 정본 무수정" 판정 제외 — 승격 append(mi-0072~0075)는 CP2 이후 정상 append이며 무수정 위반 아님(v1.0 CP2 선례 동형) |
| **DP-W4** | C-3 동형 스캔 대상 = uaf/ 정본 4문서 본문. 부록은 방법론 고유명 정당 보유 격리(스캔 제외). 특정 AI 실명·모델명·제품 기능명은 부록·워크스루 포함 전 산출물 0건 |
| **DP-W5** | 가상 /import 워크스루 스코프 분리 — 01-entry §8 예3 = **등록 모델**(변경=Registry 행·Policy 추가뿐), walkthrough §4 = **사용자 흐름**(무변경 대조) |
| **DP-W6** | uaf/ 문서 구조 관행 = §9 이력 **머리 배치**·TEMPLATE §9 Open Questions는 **완료 보고 채널**로 대체(uaf/ 경계 관행) |
| **DP-W7** | 결정 테이블 D3 밖 행 2·5 = 충돌 사용자 확인 게이트 P-D 원칙으로 도출(P-C/P-D 도출 원칙 단일 해소) |
| **DP-W8** | 결정 테이블 행 8 = Contract 우선 incremental |
| **DP-W9** | 신규 mode의 State Machine 무변경 판독 기준 = 02 §3.3-B 전이표(단일 정본)·mode는 확장 네임스페이스(§3.3-A "세 분기"는 시점 서술이지 닫힌 열거 아님) |
| **DP-W10** | 필수 코어 필드 충족 의미 — 명시적 공집합·미결 명시=충족·Provenance 비코어 |
| **DP-W11** | Assumption Ledger 위상 — 독립 그룹 #7 + Readiness 참조 |
| **DP-W12** | T10 계수 실측 20 정본 — Advisor 위임문 "Candidate 21"은 18+2의 +1 산술 오기(실측 20이 정본), Worker L-15 준거 처리 승인. 이 결함을 재발 판정 대상 확정 → mi-0075 Recurrence(matched L-15) 등록 |

**주요 OQ 해소**: Advisor 채택 시 OQ 6건 해소. T10 r1 open_questions 1건(계수 편차)은 DP-W12로 판정(실측 20 정본·L-15 준거 승인·재발 판정 대상 확정).

## 1.4 검증 게이트 실동작 기록

- **마일스톤 수준**: 실서브에이전트 위임 다회(Planner·Worker·Verifier — Verifier·Planner 위임은 `model: opus` DP-E8) + **재작업 라우팅 2회**. 거짓 완료 보고 0건. **CP2 첫 판정 Pass 15/0/0 — v0.5부터 7연속.**
- **재작업 라우팅 2회**:
  - **T1 r2** — 산출물(`uaf/ARCHITECTURE.md`) 본문의 외부 정본 § 포인터 오기 1건(Glossary "핵심 루프"를 §3.2-I로 오인용 — 정본은 §3.2-J)을 **Advisor 게이트 C 검출**·동종 전수 재대조(BP-01) 후 r2 폐합. 재발 판정 **Novel**(mi-0072)·신규 Lesson 후보 **L-20**(mi-0073 Candidate).
  - **T10 r2** — r1 완료 보고 open_questions 1(계수 편차)에 대한 **Advisor 판정 반영**(실측 20 정본·위임 "21"은 산술 오기·L-15 준거 처리 승인) + 이 결함의 재발 판정 대상 확정 → mi-0075 **Recurrence**(matched L-15) 보충 등록.
- **T4 실행 중단·재개**: 장시간 집필 Task(`uaf/specs/02-discovery.md` Module부)가 실행 중단(스트림 중단) 후 **재개 프로토콜**(산출물 전체 실측 재확인 → 미완 지점 완성 → 전 검증 스캔 재수행 → 완료 보고)로 결함 0 복구. 최종 산출물은 독립 Verifier CP2 판정에 포함되어 결함 0 확인(BPD-13 실증).
- **CP2 직접 수행 근거**: 완료 보고를 그대로 신뢰하지 않고(06 V1) 산출물 직접 실측(uaf/ 트리 다중 패턴 grep·mtime 타임라인·store/index 실측·정본 원문 표본 재대조)으로 독립 재판정. 전 산출물 실질 주장 ↔ 직접 실측 전 지점 일치, 거짓 완료 검출 0건.

## 1.5 Lesson·BP — 정식 등록 경로 처리 완료 (심사 등록 4건 mi-0072~0075)

- **재발 판정 2건**(kind=recurrence-judgment): **mi-0072 Novel**(T1 r1 산출물 본문 외부 정본 § 포인터 오기 — 회수 20건에 "산출물 본문 § 포인터 대조" 국면 커버 Active Lesson 부재·매칭 없음 → Novel)·**mi-0075 Recurrence**(T10 위임문 done 1 파생 합산 계수 오기 — matched **L-15**, 회수됐음에도 파생·합산 계수 검산 축에서 재발). 각 was_recalled = 회수 집합 20건 참조.
- **Lesson Candidate 등록·보류 1건 — L-20**(mi-0073): "산출물 본문의 외부 정본 § 포인터·절 라벨은 기입 전 대상 정본 파일 직접 실측으로 대조하고, CP1 자체 점검의 전수 스캔 범위에 § 포인터 대조를 포함한다(위임문 대상 L-18과 같은 깊이의 산출물 본문 축)." 1회 발생 — 승격 없이 Candidate 보류.
- **Best Practice Candidate 등록·보류 1건 — BPD-13**(mi-0074): "장시간 집필 Task의 실행 중단(스트림 중단 등) 후 재개 시 재개 프로토콜(① 산출물 전체 실측 재확인 ② 미완 지점 완성 ③ 전 검증 스캔 재수행 ④ 완료 보고)을 따른다. v1.1 T4에서 실증(중단 후 결함 0 복구)." 1회 발생 — 실무 동형 재발 시 재상정.
- **승격 0건** — 이번 심사는 전건 Candidate 보류(Active 전이 없음). Active 재사용 실증 기록만: BP-02(확정 인터페이스 선행 Wave 배치 — T1 §8.2 Discovery Request 추상 선행 확정 → W2 병렬 성공)·BPD-06(병렬 분해·디스패치·병합 — W2 2병렬 + W5 3병렬 무충돌 완주).
- **승격 권한 Advisor 전속(05 INV-4)**: 판정·등록 결정은 전부 Advisor 확정. docs/v1.1-promotion-review.md(r2, Worker 집행)는 문서화·물리 집행만 수행.
- **기존 보류 Candidate 18건 승계 유지**(LD-01~03 · BPD-01~05 · BPD-07~10 · BP-04 · L-16~19 · BPD-12). 기존 18 + 신규 2(L-20·BPD-13) = **Candidate 20건**. status 필터로 Active 회수에서 자연 제외.

## 1.6 차기 개정 일괄 후보 (비차단 — 승계 + 신규)

**(a) v1.1 신규 관찰(비차단):**

1. **02-discovery §3.3-B T2·T3 Guard 예시 문면** — 전이 T2·T3의 Guard 예시가 Greenfield/Brownfield만 예시하고 **incremental·신규 mode를 병기하지 않는다**. 그러나 §3.3-A Contextualizing 상태 정의가 incremental 분기를 명시하고 세 분기의 `ContextCaptured` 수렴을 규정하므로 **하드 모순이 아니다**(CP2 판정 기준 (나) — §3.3-B 전이표 단일 정본·§3.3-A 세 분기 닫힌 열거 아님). **Advisor 사전 수용** — 차기 개정 일괄 후보로 이관.

**(b) v1.0 §1.6 이월 후보 승계(유보 잔여):**

1. **Glossary 0.2 표제어 인용 정합** — "Wave·Baseline·형태 A/B는 Glossary 표제어가 아니다" 류 서술의 전 문서 정합 개정.
2. **plugins-binding §7** framework/plugins/ 3문서 크기 표기 stale(양성·라이브 모순 아님).
3. **adapter-conformance §3** "자매 8문서" 계수 표현 정합.
4. **runtime-binding §3.2·lifecycle §5** 전이 조건 서수 표기(자매 바인딩 내부 서수 정정).
5. **Presentation Layer 귀속 정본 확정**(uahf-status·getting-started의 Presentation 귀속·BP-6 확장 관계 명문화).
6. **uahf-status §9 이력 절**(머리 상태 라인 보유하나 §9 이력 표 부재 — 실개정 시 추가 재검토).
7. **v0.8 승계 기록만 사안** — 06 연산 실패 보고 reason 형식화·07 병렬 집합 well-formedness 보강 등.
8. **형태 B / DP-4 재상정 OQ 5건** — Formal 전이 경로(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2), 형태 B 실행 호스팅 도입 시 재판정.

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1~v1.0 완료(기준선). **v1.1 CP2 첫 판정 Pass(15/0/0)·CP3 Advisor 승인(2026-07-07) — 사용자 승인 대기(Draft).** ROADMAP은 v1.1을 v1.0 완료 이후 직렬로 이어지는 **UAF 레벨 신설 트랙**으로 등재했다(v1.1 등재 Draft). v1.1 승인 후의 다음 트랙은 ROADMAP에 정의되어 있지 않다(§3.1).
- v1.1은 Project Discovery & Entry Layer다 — **Execution 이전의 공식 Entry Architecture**(Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF → Execution)를 UAF 레벨에 **설계만** 했다(구현 0). 신규 최상위 경계 `uaf/`에 UAF 정본 4문서 + 비정본 부록 1을 신설했고, UAHF 정본은 무수정으로 유지됐다(접점 = Project Contract 하나). 핵심 사용자 원칙 P1~P5·확인 C1~C3이 정본 문면으로 고정됐다.

## 2.2 산출물 상태 (전부 v1.1 Draft — 사용자 승인 대기)

**신규 (9 — 실측 대조 완료)**

| 파일 | 내용 | 비고 |
|---|---|---|
| `uaf/ARCHITECTURE.md` | UAF 상위 구조 정본 — 6요소 구조·slot 2·의존 방향 단방향·원칙 9·P1~P5·상시 불변 2·UAF-INV 6·책임 경계표·Non-Goals·용어 절(§8.2 Discovery Request 추상 확정) | T1 (r2 1회, DP-W6) |
| `uaf/specs/01-entry.md` | Entry Layer & Entry Resolution — Entry Descriptor 등록 모델(C1)·결정 테이블 8조합(§3.2-D)·판별 규칙 D3·Evidence Source 확장 스키마·Registry 확장 포인트·/import 워크스루(§8 예3) | T2 |
| `uaf/specs/02-discovery.md` | Project Discovery(Workflow부 + Module부) — Compiler 프레이밍(P2)·State Machine 단일 정본(§3.3)·Event Model·Termination·Execution Ready 2축(§3.7·C3)·Module Structure·Strategy Provider Interface·Confidence·Budget·Policy·Metrics | T3(Workflow부)+T4(Module부, 중단 후 재개) |
| `uaf/specs/03-project-contract.md` | Project Contract(Stable Contract) — 스키마 9그룹·필수 코어 필드·버저닝(§3.3 C2)·역참조 금지(PC-INV 2)·UAHF Interface(§3.5·정식 등재 §3.5-C 확장 포인트) | T5 |
| `uaf/appendix/methodology-mapping.md` | **비정본 부록** — 방법론 5종 → Strategy Capability 대응. 방법론 고유명 정당 보유 격리 지점(정본 청정, UAF-INV ⑥) | T6 (DP-W4) |
| `docs/v1.1-scenario-walkthrough.md` | 시나리오 워크스루 3건(Greenfield /new·Brownfield /continue 최초 도입·가상 /import 확장) — CP2 입력물·State Machine 완주·무변경 대조(DP-W5) | T7 |
| `docs/v1.1-verification-report.md` | CP2 — 첫 판정 Pass 15/0/0·산출물 직접 실측·다중 패턴 전수 스캔·비차단 관찰 1건 | T9 |
| `docs/v1.1-promotion-review.md` | 승격 심사(r2) — 재발 2(Novel·Recurrence)·L-20/BPD-13 Candidate·승격 0·mi-0072~0075 | T10 (r2 1회, DP-W12) |
| `docs/session-handoff-v1.1.md` | 본 핸드오프 | T11 |

(신규 9 = uaf/ 정본 4 + 비정본 부록 1 + docs 4(scenario-walkthrough·verification-report·promotion-review·session-handoff-v1.1). CP2 판정 대상 7건 = uaf/ 정본 4 + 부록 1 + walkthrough 1 + ROADMAP 개정 1 — verification-report·promotion-review·handoff는 CP2 산출·이후 산출물이므로 판정 대상 밖.)

**개정 (1)**

| 파일 | 개정 내용 | 비고 |
|---|---|---|
| `ROADMAP.md` | 상태 라인 "v1.1 등재 Draft"·#3 표 v1.1 행·#4 맵 v1.1 직렬·#5 v1.1 절(목표·완료 조건 9·산출물)·**#8 이력 절 신설**(말미 배치 — 루트 ARCHITECTURE.md #9 관행 동형). #6 Principle Coverage·#7 Component Coverage는 v1.1 행 미추가(UAF 레벨 신설이므로) | T8 |

**삭제 (1)**

| 파일 | 사유 |
|---|---|
| `docs/v1.1-review-brief.md` | 사용자 지시 — 이름 오기된 v1.0 정리 문서(삭제 완료) |

**물리 데이터 (append-only — 실측 대조 완료)**

| 대상 | 상태(실측) | 비고 |
|---|---|---|
| `framework/adapters/claude/memory-data/` | store **75파일**(mi-0001~0075)·index **75라인** — 기존 71건 무변경 + 신규 4건(mi-0072~0075) | T10(r2), store↔index 1:1·무결번·MD5 바이트 대조. CP2 이후 정상 append(DP-W3) |
| `framework/adapters/claude/loop-data/` | **11파일 83 line 무변경** — v1.1은 문서 설계만이므로 루프 실행 append 0 | 실측 |

**Memory 심사 후 집합 (실측 대조 완료 — L-07)**

- **Active 20건** = Lesson **15건**(L-01~L-15) + Best Practice **5건**(BP-01·BP-02·BP-03·BPD-06·BPD-11). **v1.1 승격 0건 — Active 무변경.**
- **Candidate 20건** = Lesson 8(L-16~L-20·LD-01~03) + Best Practice 12(BP-04·BPD-01~05·BPD-07~10·BPD-12·BPD-13) — 기존 18 + 신규 2(L-20·BPD-13). status 필터로 Active 회수에서 자연 제외.
- **kind 분포(75)**: lesson **38** · best-practice **22** · recurrence-judgment **15** (합 75 — 직접 실측).

**무변경 (CP2 실측)**

- UAHF 정본 전체 — 루트 ARCHITECTURE.md·specs/ 15종(numbered 00~13 + TEMPLATE)·framework/ 문서 전체·.claude/ 표면. v1.1 Wave 착수(2026-07-07T04:00) 이후 수정 0. ROADMAP.md만 명시 개정 예외.
- structure.md §8 트리는 `framework/` 하위만 열거(루트 미열거) → 계획의 조건부 개정 미발동·무수정 정당(DP-W2).

## 2.3 하네스 상태

**Bootstrap 유지**. v1.1은 **UAF 레벨 Architecture 문서 설계만** 수행했으므로(구현 0) 하네스 상태 전이와 무관하다 — 형태 B(Formal) 전이는 v1.1의 완료 요건이 아니며, v1.0 종료 시점의 Bootstrap 상태가 그대로 유지된다.

- **전이 조건 3(Runtime 정식 Module 호스팅) = 미충족** — 현 실현 = 형태 A(문서 절차·규약·관행). DP-U1(v0.9)의 승계된 귀결이며 v1.1에서 변동 없음.
- 조건 1(관련 spec Frozen)·2(환경 의존 실현 Adapter 격리·Core AI 의존 0)·4(Scaffold 설치 대상)는 v1.0까지 충족 상태를 유지한다. Core Claude 의존 0건은 v1.1에서도 경계 스캔으로 유지 실증됐고, UAF 신규 산출물(uaf/ 정본 4문서)도 특정 AI 실명·모델명·제품 기능명 0건이다(CP2 item #9).
- **UAF 위상 주(하네스 vs UAF)**: v1.1이 신설한 `uaf/`는 UAHF 6-Layer 스택의 **외부** UAF 레벨 구조다(Glossary INV-3 무촉). UAHF와 UAF의 접점은 Project Contract 하나이며, Project Contract는 UAHF의 **선택 입력**(부재 시 기존 운용 불변)이므로 하네스 상태를 바꾸지 않는다.

**Formal 전이 잔여(v1.1 이후 사안)**: DP-4 재상정 경로 — OQ-M5-2(Record 원자성) + 형태 B 경계 분할 OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2 (5건). 형태 B 실행 호스팅 도입 시 재판정하며, 그 시점에 조건 1·2·4는 이미 충족되어 있다.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙 — **미정 (사용자 결정 필요)**

ROADMAP은 v1.1을 마지막 등재 트랙으로 정의하며, **v1.1 이후 트랙은 정의되어 있지 않다**. 다음 세션의 트랙은 **사용자 결정 대상**이다. 이 핸드오프는 차기 트랙을 선취해 확정하지 않는다.

**후보(사용자 선택 대상 — 선취 아님):**

- **(a) v1.2 — Project Discovery 실현** — uaf/ 스펙의 형태 A/B 실현·Adapter 바인딩·진입 명령 물리화(v1.1 설계의 구현 버전).
- **(b) 형태 B 실행 호스팅 도입 / DP-4 재상정** — UAHF Formal 전이 경로. 전이 조건 3 충족 경로·경계 분할 OQ 5건.
- **(c) 유지보수 운용** — 릴리스 후 개정·차기 개정 일괄 후보(§1.6) 정리.
- **(d) 신규 로드맵** — 새 목표 트랙 정의.

## 3.2 Memory 실사용 (모든 차기 세션 공통 — 갱신)

1. **Consult**: 착수 전 memory-binding.md §3.2로 회수. **Active 집합: Lesson 15건(L-01~L-15)·Best Practice 5건(BP-01~03 + BPD-06 + BPD-11)** = **20건**, store 75파일·index 75라인. Candidate 20건(L-16~20·LD-01~03·BP-04·BPD-01~05·BPD-07~10·BPD-12·BPD-13)은 status 필터에서 자연 제외.
2. **Memory Update**: Register Candidate + Advisor 승격 심사. append-only(신규 레코드/status 전이는 새 레코드로).
3. 재발 판정: was_recalled 입력은 Consult 회수 기록. Novel/RecallGap/Recurrence 3분류(lessons.md §4). **파생·합산 계수도 검산 대상**(mi-0075 Recurrence 확인 — L-15 적용 범위에 파생 합산 계수 축 포함).

## 3.3 이월 사항

- ① **02-discovery §3.3-B T2·T3 Guard 예시 문면** — incremental·신규 mode 병기(비차단 — Advisor 수용·차기 개정 일괄 후보, §1.6-a).
- ② **v1.0 handoff §1.6 이월 후보 승계**(§1.6-b) — Glossary 0.2 인용 정합·plugins-binding 크기 표기·conformance 계수·서수 표기·Presentation 귀속·uahf-status 이력 절·v0.8 승계 기록·형태 B/DP-4 재상정 OQ 5건.
- ③ **UAHF 측 Contract 정식 등재** = 구현 버전 확장 포인트(03 §3.5-C — UAHF spec에 필수 입력·명명 산출물로 등재하는 경로는 UAHF 정본 확장이므로 v1.1 미설계).
- ④ **Discovery 실행 호스팅·Discovery의 Memory 활용** = 확장 포인트(uaf/ARCHITECTURE §7 — 역할 추상까지만·물리 호스팅 미설계).
- ⑤ **Contract 스키마 상세(schemaVersion 표기 등)의 Adapter Binding** = 구현 버전(논리 스키마만 v1.1 정본, 직렬화·물리 포맷은 Adapter 소관).

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — 다음 트랙 미정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v1.1 (Project Discovery & Entry Layer)이 완료되었다 — UAF 레벨
Architecture 설계만 수행(구현 0)하여 신규 `uaf/` 경계에 UAF 정본 4문서 + 비정본
부록 1을 신설했고, UAHF 정본은 무수정으로 유지됐다(접점 = Project Contract 하나).
v1.1 이후 트랙은 ROADMAP에 정의되어 있지 않다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v1.1.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md §3.2
   절차로 Active Lesson(15건: L-01~L-15)·Best Practice(5건: BP-01~03 + BPD-06 + BPD-11)
   = 20건을 목적·최소 범위로 회수하고 회수 집합을 기록한다
   (store 75파일·index 75라인. Candidate 20건은 status 필터로 자연 제외).
3. 다음 트랙을 스스로 채택하지 말고 사용자에게 결정을 요청한다.
   ROADMAP v1.1까지 등재된 트랙이 완료되었으므로 다음 트랙은 미정이다. 후보를 제시하되
   (a) v1.2 Project Discovery 실현(uaf/ 스펙의 형태 A/B 실현·Adapter 바인딩·진입 명령 물리화)
   (b) 형태 B 실행 호스팅 도입·DP-4 재상정
   (c) 유지보수 운용(차기 개정 일괄 후보 정리)
   (d) 신규 로드맵
   채택은 사용자 결정 사항이다. 차기 트랙을 선취해 착수하지 않는다.
4. 사용자가 트랙을 결정하면, 필요한 정본을 정독하고
   (ARCHITECTURE.md, ROADMAP.md, 관련 specs, framework/adapters/ 바인딩,
   framework/core/structure.md, 직전 검증·승격 리포트,
   그리고 uaf/ 정본 4문서: uaf/ARCHITECTURE.md·uaf/specs/01-entry.md·
   uaf/specs/02-discovery.md·uaf/specs/03-project-contract.md),
   .claude/AGENT.md·.claude/agents/ 4종·docs/delegation-protocol.md·
   docs/verification-checklist.md를 읽고, 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v1.1 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D) + framework/verifier/ 규격, 구현 Worker(Opus) 위임,
완료 보고 불신·독립 검증, Frozen spec 변경은 버전 상승+Revision History,
Architecture-Spec 충돌은 사용자 보고, C-1~C-3(+Module 구현 디렉터리 C-3 확장) 전 산출물 적용.
Core Claude 의존 0건은 유지 대상이며 2nd Adapter 이후 산출물은 그 Adapter 경계에만 격리한다.
uaf/ 정본 4문서 본문은 특정 AI 실명·모델명·제품 기능명 0(C-3 동형) — 물리 실현은 Adapter Binding 소관.
위임문의 산출물 본문 문안(L-11)·존재 전제(L-12)·계수/규모/상태 전제(L-15)·
§ 라벨/절 번호 지칭(L-18 Candidate)은 발신 전 파일 시스템 실측으로 대조한다.
산출물 본문의 외부 정본 § 포인터·절 라벨도 기입 전 대상 정본 직접 실측 대조하고
CP1 자체 점검 전수 스캔에 § 포인터 대조를 포함한다 (L-20 Candidate 취지 — T1 r2 유래).
위임문 done의 파생·합산 계수(기존 N + 신규 M 등)는 산술 검산으로 재계산해 대조한다
(mi-0075 Recurrence — L-15 적용 범위에 파생 합산 계수 축 포함 확인).
기존 Baseline 문서의 개정 위임에는 상태 라인·이력 행 라벨의 기대 문면을 명시한다 (L-13).
Agent 기동 설정(.claude/agents/ 이하)의 개정은 사용자 직접 지시 권한 경로로 처리한다 (L-14).
Verifier·Planner 위임은 model opus를 명시한다 (DP-E8 — 차기 세션 재확인 대상으로 승계).
Frozen 미명세 지점은 정본 문면 인스턴스로 해소하고 결정 기록으로 명문화한다 (BP-03).
개정 시 같은 상태 서술의 전 지점 전수 갱신(L-06)·상태 서술은 실측 후 기입(L-07·L-09).
uaf/ 문서 구조 관행 = §9 이력 머리 배치·완료 보고 채널로 Open Questions 대체(DP-W6).
큰 작업 분해·병렬 디스패치·병합은 framework/workflow/ 계약 인스턴스(C1~C4·R1~R4·5단계)와
확정 인터페이스 선행 Wave 배치(BP-02·BPD-06·BPD-11)를 사용한다.
UAF 관련 트랙이면 상시 불변 확인 2건을 매 게이트에 적용한다 — ① Discovery는 교체 가능한
Compiler(내부 개념 누출 0) ② Contract는 장기 호환 Stable Contract(SemVer·tolerant reader·필드 제거 금지).
세션 종료 시 Memory Update — Register Candidate + Advisor 승격 심사.
```

---

# 5. 주의사항

1. **물리 store·loop-data는 append-only다**(04 INV-6·03 INV-3) — memory-data/ **75파일·index 75라인**, loop-data/ **11파일 83 line** 수정·삭제 금지. 갱신은 새 레코드/새 전이 이벤트로만. 기존 71 store 파일은 MD5 바이트 무변경 실측(T10 §3.3). v1.1 승격 append(mi-0072~0075)는 CP2 이후 정상 append이며 "UAHF 정본 무수정" 판정과 무관하다(DP-W3).
2. **§9 이력 행은 시점 기록** — 문면 불변, append만(L-10). 단, 같은 세션에 자신이 append한 행의 교정은 위반 아님(T1 r2 선례 — 근거 괄호/§ 포인터 정합 시 문면 보존).
3. **개정 시 전 지점 전수 갱신**(L-06) + **상태·시각 서술은 실측 후**(L-07·L-09) + **위임문 문안·존재 전제·계수 전제 사전 대조**(L-11·L-12·L-15) + **개정 위임의 상태 라인·라벨 기대 문면 명시**(L-13). ※ **L-15 관행 확장(mi-0075 Recurrence)**: 위임문 done의 계수는 단일 실측값(store 규모 등)뿐 아니라 그로부터 **파생되는 합산·차감 계수(기존 N + 신규 M)도 발신 전 산술 검산**으로 대조하라 — v1.1 T10에서 위임 "Candidate 21"이 18+2의 +1 산술 슬립이었고 수임 Worker 독립 재계산으로 실측 20을 정본화·에스컬레이션했다(DP-W12).
4. **L-20 Candidate 취지(산출물 본문 § 포인터 실측)** — 산출물 **본문**의 외부 정본 § 포인터·절 라벨은 기입 전 대상 정본 파일 직접 실측으로 대조하고, CP1 자체 점검 전수 스캔 범위에 § 포인터 대조를 포함한다(T1 r2 유래 — Glossary "핵심 루프" §3.2-I→§3.2-J 오기 폐합). L-18(위임문 축)과 같은 원칙의 산출물 본문 축 대응이다.
5. **승격 권한 Advisor 전속**(05 INV-4) — Candidate 등록·재발 판정은 승격이 아니다(`approval`·`supersedes` 필드 없이 등록). Active 승격 시에만 승인 참조를 content(`approval`)에 자기완결 첨부. v1.1은 승격 0건이다. Worker(승격 심사 문서 집행 주체)는 승격을 결정하지 않고 물리 집행만 한다.
6. **UAHF 정본 무수정(UAF-INV ①)** — UAF 신설·확장은 UAHF 정본(루트 ARCHITECTURE.md·specs/ 15종·framework/ 문서 전체·.claude/ 표면)을 변경하지 않는다. UAF와 UAHF의 접점은 **Project Contract 하나뿐**이며, Contract는 UAHF의 **선택 입력**(부재 시 기존 운용 불변)이다. UAF 정본은 UAHF 계약 요소를 § 포인터로만 참조하고 재정의 0이다.
7. **INV-3 무촉 (UAF 위상)** — Entry Layer·Entry Resolution·Project Discovery·Project Contract는 UAHF 6-Layer 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter)의 **외부** UAF 레벨 구조다. "Entry Layer"의 "Layer"는 UAHF Layer 지층이 아니라 UAF 파이프라인의 한 **단계(stage)** 명칭이며 네임스페이스가 분리된다(uaf/ARCHITECTURE §0·§8). Glossary INV-3("Layer는 정확히 6개다")는 무촉이다.
8. **uaf/ 정본 본문 특정 AI 실명·모델명·제품 기능명 0**(C-3 동형) — uaf/ 정본 4문서 본문에 특정 AI 실명·모델명·제품 기능명 금지(CP2 item #9 매치 0 실측). 물리 실현(진입 명령 형태·직렬화·환경 경로)은 Adapter Binding 소관·일반형 표기(`<adapter>`)만. **부록(uaf/appendix/)은 방법론 고유명 정당 보유 격리 지점**(정본 청정, UAF-INV ⑥·DP-W4) — 방법론 5종은 부록에만 존재하고 정본 4문서에 0건.
9. **structure.md 무수정(DP-W2)** — §8 트리가 `framework/` 하위만 열거(루트 미열거)하므로 계획의 조건부 개정("저장소 루트 전체 열거 시 uaf/ 추가")이 미발동했다. structure.md 무수정이 정당하다. 향후 §8 트리가 루트를 열거하도록 개정되면 uaf/ 추가 여부 재검토(버전 상승 + 이력 append).
10. **DP-E8** — Verifier·Planner 위임은 `model: opus` 명시. "영구 관행" 문구는 **차기 세션 재확인 대상으로 승계**(계약(06) 변경이 아니라 실행 모델 바인딩(02 §4.1)). Agent 기동 설정(.claude/agents/ 이하) 개정은 사용자 직접 지시 권한 경로로만(L-14).
11. **재개 프로토콜(BPD-13 Candidate)** — 장시간 집필 Task의 실행 중단(스트림 중단 등) 후 재개 시: ① 산출물 전체 실측 재확인(done 항목별) ② 미완 지점 완성 ③ 전 검증 스캔 재수행 ④ 완료 보고. v1.1 T4에서 실증(중단 후 결함 0 복구). 1회 발생이므로 Candidate 보류 — 실무 동형 재발 시 재상정.
12. **상시 불변 확인 2건 (UAF 관련 트랙 매 게이트 판정)** — ① Project Discovery는 단일 기능이 아니라 **Project Contract를 생성하는 Compiler**다(Discovery 교체 가능·내부 개념 Contract 코어/UAHF 접점 누출 0). ② Project Contract는 UAF↔UAHF 공식 **Stable Contract(Public API)**다(SemVer·tolerant reader·필드 제거 금지 훼손 0). 두 확인을 통과하지 못한 산출물은 승인하지 않는다.
13. **Discovery Request 선행 확정 인터페이스** — uaf/ARCHITECTURE §8.2가 확정한 Discovery Request 3요소 추상{mode(확장 네임스페이스)·inputs(Evidence 참조 목록)·policy(Policy 참조)}이 후속 병렬 작업(01-entry·02-discovery)의 선행 확정 인터페이스다(BP-02 실증). 병렬 작성 중 미완성 산출물이 아니라 확정된 참조만 담는다(07 R2).
14. **하네스 Bootstrap 유지** — v1.1은 UAF 레벨 문서 설계만이므로 하네스 상태 전이와 무관하다(전이 조건 3 미충족·DP-U1 승계 귀결). Formal 전이는 형태 B 실행 호스팅 도입 시로 유보(§2.3).
15. **계수 갱신 요약(실측)** — memory store **75파일**/index **75라인** · loop-data **11파일/83 line**(무변경) · Frozen specs **15**(numbered 00~13 = 14 + TEMPLATE 1) · Memory Active **20**(Lesson 15 + BP 5)·Candidate **20**(Lesson 8 + BP 12) · kind 분포 75(lesson 38·best-practice 22·recurrence-judgment 15) · v1.1 신규 산출물 **9** + 개정 **1**(ROADMAP) + 삭제 **1**(v1.1-review-brief) · uaf/ 정본 **4** + 비정본 부록 **1**.
16. **다음 트랙 미정 — 선취 금지** — ROADMAP v1.1까지 등재 트랙 완료로 다음 트랙은 사용자 결정 사항이다(§3.1). 차기 세션은 트랙을 스스로 채택하지 말고 사용자에게 결정을 요청한다(§4 Bootstrap Prompt 구조). 후보 4종 제시(v1.2 실현·형태 B/DP-4·유지보수·신규 로드맵)는 선취가 아니다.
