# Proposal — arch-pipeline (maturation-r002 · Proposing/T1)

- **roleId**: `arch-pipeline` (Expert Role · Capability 선언 · 개방 네임스페이스 — 04 §3.3)
- **capability**: 파이프라인 구조·orchestration Layer 실현·`architectureDirection`(open·decisions) 및 그 형태 B 실현 파급(constraints·risks·openQuestions 정합)에 대한 설계 결정.
- **입력 결속 (inputContract)**:
  - **기준선 인스턴스**: `framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v2.md` — pc-uahf-001 · instanceVersion 2 · supersedes 1 · maturation-r001 종단 `Matured`(사용자 승인 2026-07-13). 성숙 기준선(SP-INV 1 정합은 OQ-R2-1로 표면화 — assessing-judgment §1).
  - **v2 이후 확정/실현 집합(저장소·커밋 실측)**: 커밋 사슬 `fd112cd`(orchestration S1)→`ce0cdba`(S2)→`c65d20f`(S3)→`745f26e`(S4·OQ-SH-4 해소)→`5e843dc`(S5·기반 커밋). 설계 정본 `docs/project-orchestration-design.md`(사용자 승인 2026-07-13)·정본 `orchestration/specs/05-project-orchestration.md`. v1.5 형태 B Step Hosting Baseline(step-hosting-protocol·step-host 실행 코드). 실측 표면: 최상위 6 Layer(`entry/·discovery/·planning/·uahf/·knowledge/·orchestration/`)·실행 코드(`uahf/framework/loop/step-host/*.py` 5·`orchestration/framework/orchestrator/*.py` 6)·데이터 디렉터리(`step-data/`·`orchestration-data/`).
  - **잔여 미결(architecture 축)**: 형태 B 잔여 경계 분할(OQ-VB-2·M5-2·PB-2)·물리 동시 디스패치(OQ-WB-2 잔여)·Contract 정식 등재·orchestration 진화 잔여 축(멀티프로젝트·대화형 형태 B·OQ-PO-B4·비용 미터링).
- **작성**: 2026-07-13 · 담당 관심사 한정 v3 delta 제안(§3.4-D ① Proposal). 본 문서는 코어 밖 실행 메타다(SP-INV 2·3) — Contract 코어 필드로 유입되지 않는다.
- **단일 역할 run**: 본 run은 `arch-pipeline` 단일 역할이다(assessing-judgment §3). 동시 작성 병렬 산출물 부재 → 07 R2 인용·추측 대상 0. 확정된 인터페이스 계약(04 §3·03 §3.2-A·§3.4·§3.6·루트 §2.2·§2.3·§2.5·§11·solution-design-binding §8·05 §0·§3·§5·project-orchestration-binding·contract-binding §4.2·§5·§6)과 저장소·커밋 실측만 참조.

---

## 1. 담당 관심사 경계 (선언)

이 Proposal은 **`architectureDirection`(decisions·open)·그 형태 B 실현이 파급하는 연동 필드(`constraints`·`risks`·`readiness.openQuestions`·본문 미러)**의 v3 현행화에 한정한다. 위임(2026-07-13)이 지정한 성숙 대상 = **open 3항 성숙**이며, 그 성숙과 **내부 정합**을 위해 필요한 최소 파급만 포함한다(내부 모순 방지 — v2가 "형태 B 실현"을 open에 쓰면서 constraints에 "실행 코드 0"을 유지하면 자기모순).

**전건 제약 준수 (자기 점검)**: D4 스키마 무변경(9그룹·필수 코어 필드 외 새 필드·새 그룹 0·`schemaVersion` "1.0" 유지) / **필드 제거 0(PC-INV 6)** / v2 무수정(delta는 본 제안·후보 문면에만·v2 byte 불변·PC-INV 9) / **supersedes 2(03 §3.4 계보)** / 6요소 파이프라인 유지 / Draft·Final mutable 어휘 0 / 거버넌스 라벨 재감사·이월 계수 재산정 **미수행**(범위 밖 — risks[2]·openQuestions[1] 무촉).

**범위 밖(무촉) 명시**: (i) `intent`·`requirements`(functional/quality)·`assumptionLedger`·`readiness.confidenceVector`·`readiness.completeness` = 성숙 범위 밖 필드로 **v2 현행 유지(byte 무변)**. (ii) `risks[2]`(이월 개정 누적 7건)·`readiness.openQuestions[1]`(이월 개정 일괄) = 거버넌스/이월 축으로 **본 run 재감사 미수행 → 무촉**. (iii) `decisions[0]`(6-Layer 스택+13 Component)·`decisions[2]`(UAF 외부 파이프라인+planning 이중 책임) = 여전히 참 → 무변.

---

## 2. Delta 표 (v2 기준선 → v3 제안)

각 delta: ① 필드 경로(03 §3.2-A 그룹) ② v2 현행 문면(요약) ③ 제안 v3 문면(요약) ④ 판정·근거. 전 delta는 **기존 필드 내 문면 정정**이며 새 필드/그룹/스키마 버전 0(D4). 완전 문면은 `candidate/project-contract.v3.CANDIDATE.md`.

### 2.1 핵심 성숙 (위임 지정 — open 3항)

| # | 축·필드(그룹) | v2 → v3 | 판정·근거 |
|---|---|---|---|
| **D-open1** | `architectureDirection.open[0]` (그룹 6) 형태 B 경계 분할 | "…경계 분할(OQ-M5-2·VB-2·LB-2·WB-2·PB-2 + SD 실행 호스팅) — DP-4 재상정 시" → **재기술**: OQ-LB-2 **해소**(v1.5 Step Host)·OQ-WB-2 **부분 해소**(순차 실증·물리 동시[병렬 invoker] 잔여)·OQ-SH-4 **해소**(v1.6 CP2 모델 독립)·SD 실행 호스팅 orchestration 형태 B 호스팅으로 실현(05 §3.7)·잔여 = **OQ-VB-2·OQ-M5-2·OQ-PB-2** | **위임 ① 정확 반영**. 근거 실측: step-hosting-binding §172·verifier-binding §3.1 OQ-VB-2·design §9.1. LB-2/SH-4는 해소이나 **OQ 문면 계약(각 자매 바인딩 소유)은 무수정** — Contract open 서술만 현행화. |
| **D-open2** | `architectureDirection.open[1]` (그룹 6) 정식 등재 | "UAHF 측 Contract 정식 등재(planning/specs/03 §3.5-C 확장 포인트)" → **존치·미해소** + 명확화(orchestration은 Contract를 substrate로 소비하되 정식 등재 아님·UAF-INV ①·PC-INV 8) | **위임 ② 정확 반영(존치)**. 근거 실측: 05 §0(라이브러리 무수정 재사용)·§6(uahf/ 접촉 2건, 정식 등재 아님). 정식 등재 채택 결정 부재 → 해소 금지(허위 해소 불가). |
| **D-open3** | `architectureDirection.open[2]` (그룹 6) step 실행기 계열 | "step 기반 실행기 계열(…) = UAHF Execution/Runtime 진화 축 — 04 §3.9 연결만·별도 분석 트랙 후보(설계 0)" → **갱신**: v1.5 Step Host·v1.6 orchestration Layer(orchestration/ 신설·05 spec·중립 orchestrator·바인딩 — 04 §3.9 확장 포인트 1·2 실현)로 **실현**. 잔여 진화 축(open): 물리 동시·멀티프로젝트·대화형 형태 B·OQ-PO-B4·비용 미터링 | **위임 ③ 정확 반영**. 근거 실측: design §0·§4·§9·05 §7·project-orchestration-binding §7 OQ-PO-B4. "설계 0" 원칙 유지 — 잔여 축은 **등재만**. |

### 2.2 정합 파급 (핵심 성숙과의 내부 모순 방지 — 최소분만)

| # | 축·필드(그룹) | v2 → v3 | 판정·근거 |
|---|---|---|---|
| **D-oq0** | `readiness.openQuestions[0]` (그룹 8) 형태 B 착수 시점 | "형태 B 전이 착수 시점 — …형태 B **미착수**" → "형태 B 부분 실현(v1.5/v1.6·착수 완료·부분)·잔여 = 물리 동시·OQ-PO-B4 등" | **필수 정합**(open[0]의 그룹 8 미러). v2 "형태 B 미착수"는 실측 stale(착수·부분 실현). |
| **D-con3** | `constraints[3]` (그룹 4) append-only 데이터 열거 | "…(memory-data/·loop-data/·discovery-data/·solution-design-data/)…" → **+ step-data/·orchestration-data/** (6종) | **필수 정합**(열거 확장·**동일 append-only 원칙**·새 제약 창설 0). 근거 실측: 6 데이터 디렉터리 실재·design §6. r001 D3(solution-design-data/ 추가) 동형. |
| **D-con4** | `constraints[4]` (그룹 4) Bootstrap 형태 A | "Bootstrap 상태 — 형태 A 실현, **실행 코드 0**" → "코어·정본 형태 A 유지(C-1); 실행 호스팅 v1.5/v1.6 형태 B **부분 실현**(중립 실행 코드 도입·Core Contract 무변)" | **필수 정합**(v2 "실행 코드 0"은 실측 **거짓** — step-host 5·orchestrator 6 .py 실재). C-1(Core Contract 무변) 명시로 불변 보전. |
| **D-dec1** | `architectureDirection.decisions[1]` (그룹 6) 최상위 Layer | "최상위 **5-Layer**(entry/·discovery/·planning/·uahf/·knowledge/ — v1.2.1)…" → "최상위 **6-Layer**(… + orchestration/ [v1.6·루트 §2.3 slot·05 spec])…" | **정합(게이트 옵션)**. 실측: 6 최상위 Layer. **제자리 현행화(결정 4항 카운트 유지·L-25)**. orchestration Baseline 승격 유보 고려 → **가장 이연 가능한 게이트 옵션**(§5). |
| **D-dec3** | `architectureDirection.decisions[3]` (그룹 6) 현 실현 형태 A | "현 실현 = **형태 A**(문서 절차·규약·관행)" → "코어 형태 A + 실행 호스팅 형태 B **부분 실현**(v1.5/v1.6·중립 실행 코드·Core Contract 무변, C-1)" | **필수 정합**(con4와 쌍·open과 정합). |
| **D-risk1** | `risks[1]` (그룹 5) 형태 B 전환 복잡성 | "형태 B 전환 복잡성 …(OQ-M5-2 외 경계 분할 OQ 4건 + SD 실행 호스팅[v1.4 합류])…" → 부분 실현 반영(LB-2/WB-2/SH-4 진척)·잔여 OQ 3건(VB-2·M5-2·PB-2)+물리 동시 | **정합**(open[0]과 계수 정합·내부 불일치 방지). r001 T-1(risks[2] 최소 부기) 동형. |

### 2.3 기계적/발행 부속 (성숙 산출 표현)

| # | 필드 | v2 → v3 | 근거 |
|---|---|---|---|
| **D-meta** | `meta.instanceVersion`·`supersedes` | instanceVersion 2→**3**·supersedes 1→**2** | 03 §3.4 supersedes 계보·PC-INV 9. id·schemaVersion "1.0" 무변(PC-INV 4·계보 동일성). |
| **D-prov** | `provenance.maturation` | runId maturation-r002·eventLog …/maturation-r002/·baseline 2·terminal `<pending·Validating 대기>` | solution-design-binding §8.1 성숙 run 내부 형식(외형·must-ignore는 contract-binding §6 소유·재정의 0). **terminal·userApproval·발행일은 T8 후 확정**(현재 후보). |
| **D-appr** | `readiness.userApproval` | v2 승인 문면 → `<사용자 승인 maturation-r002 T8 — 승인 시 확정 기입·현재 Validating 대기>` | SP-INV 4 — 승인 전 Matured 불가. 후보는 미승인 표기. |
| **D-body** | 본문 `## Constraints`·`## Architecture Direction`·`## Readiness` 미러 | front-matter 정합 현행화(형태 A→부분 형태 B·5→6 Layer·v2→v3·승인 placeholder)·**결정 4항·미결 3항 카운트 유지** | 본문=front-matter 미러 정합(RD-10 계열·L-25). |

---

## 3. 근거 상세 (실측·정본 § 포인터)

### D-open1 — 형태 B 경계 분할 재기술 (해소·부분·잔여의 정직 구분)

- **OQ-LB-2 해소**: `step-hosting-binding.md §172` "W3 정합 완료: loop-binding §8 OQ-LB-2 해소 표기". loop 형태 B 코드가 v1.5 중립 Step Host로 실현. **해소는 자매 바인딩(loop-binding §8)이 소유 표기**하며 Contract는 open 서술에 그 사실만 반영(계약 무수정).
- **OQ-WB-2 부분 해소**: `step-hosting-binding.md §172` "workflow-binding §8 OQ-WB-2 부분 해소" + `project-orchestration-design §9.1` "물리 동시 디스패치(OQ-WB-2 잔여) — 순차 상속, 병렬 invoker는 후속". → 순차 실증분 해소·**물리 동시 디스패치(병렬 invoker) 잔여**를 정직 구분.
- **OQ-SH-4 해소**: `orchestration/specs/05 §3.5`·`design §3.5` "CP2 Verifier 모델 = 독립 정책 행 — OQ-SH-4 해소"·`host.py:315`(`cp2_model`)·커밋 745f26e. **주의: OQ-SH-4는 v2 open[0]의 명시 5-OQ 목록에는 없었다**(v2 목록 = M5-2·VB-2·LB-2·WB-2·PB-2). 형태 B/Step Host 축의 인접 진척으로서 **문맥 반영**하며, "5-OQ 목록에서의 제거"가 아님을 §5·OQ-R2-2로 표면화한다.
- **SD 실행 호스팅**: v2 open[0]의 "+ Solution Design 실행 호스팅[v1.4 합류]"은 `design §3.7`·§140·`05 §3.7`로 실현(04 §3.4 협업 프로토콜 = headless step + `user_decision_required` 게이트). 완전 비픽스처 성숙 run(OQ-PO-B4)은 open[2] 잔여 축으로 이월 — 이중 등재 방지 위해 open[0]은 "실현"만 서술·상세는 open[2].
- **잔여 경계 분할 OQ-VB-2·M5-2·PB-2**: `verifier-binding §3.1 OQ-VB-2`(Verify 실행 코드 형태 B 분할 미확정)·OQ-M5-2(Record 원자성·session-handoff 계열)·OQ-PB-2(Presentation 경계). **미해소 존치**(형태 B 완전 분할 미도입 축).

### D-open2 — 정식 등재 존치 (허위 해소 금지)

- `05 §0` "Step Host를 라이브러리로 무수정 import"·`§6` "uahf/ 트리 접촉은 정확히 2건(바인딩 신설·OQ-SH-4 1개소)". orchestration은 Contract·상류 산출을 **substrate로 소비**하되 UAHF spec에 Contract를 정식 등재하지 **않는다**(UAF-INV ①·PC-INV 8 — 정식 등재는 확장 포인트). → 정식 등재 채택 결정 **부재** → 존치. 위임 ② "존치(미해소)" 정확 반영.

### D-open3 — orchestration Layer 실현 갱신 (설계 0 유지)

- `design §0`·`§4 ⓪~④`·`05 §7`: orchestration/ = UAF 레벨 신규 Layer(루트 §2.3 Agentic Runtime slot 실현·§11 오케스트레이션 정식화)·04 §3.9 확장 포인트 1·2 실현. 중립 orchestrator(revision/gates/allocation/artifacts) + step-host 라이브러리 무수정 import.
- **잔여 진화 축(open·등재만·설계 0)**: `design §9`(물리 동시·멀티프로젝트·대화형 형태 B·비용 미터링)·`project-orchestration-binding §7 OQ-PO-B4`(실 LLM 제안 비픽스처 완전 성숙 run — 후속 트랙). v2 문면 "별도 분석 트랙 후보(설계 0)"의 "설계 0" 원칙을 **잔여 축에 그대로 승계**.

### D-con4·D-dec3 — 형태 A → 부분 형태 B 현행화 (C-1 보전)

- **실측**: `uahf/framework/loop/step-host/{bundle,events,host,invoker,step}.py`(5)·`orchestration/framework/orchestrator/{allocation,artifacts,gates,orchestrator,revision,stephost_bridge}.py`(6) 실재. → v2 "실행 코드 0" **거짓**.
- **C-1 보전(핵심)**: 형태 B 실행 코드는 **실행 호스팅**(Step Host·Orchestrator — 중립 모듈)이며, **Core Contract**(`framework/core/`·정본 spec·AI 비의존)는 무변이다(C-1 "형태 A→B 전환에도 Core Contract 변경 0"·constraint[1] 무변). 현행화는 "코어 형태 A 유지 + 실행 호스팅 형태 B 부분"으로 이 구분을 명문화 — 불변 훼손 0.

### D-dec1 — 최상위 6-Layer (게이트 옵션·이연 가능)

- **실측**: 최상위 Layer = `entry/·discovery/·planning/·uahf/·knowledge/·orchestration/` = 6(지원 dir design/·docs/·research/·templates/·tests/ 제외). v2 "5-Layer" 실측 stale.
- **제자리 현행화(카운트 규율 L-25)**: decision[1] 문면 내 "5-Layer→6-Layer" 제자리 정정 → 결정 **4항 카운트 유지**(5번째 결정 신설 아님). 본문 미러 "결정 4항"·"최상위 6-Layer" 동반 정정.
- **게이트 옵션 성격**: orchestration Baseline 승격은 트랙 종단 사용자 게이트 유보(design §6·binding 상태). decision 필드는 통상 확정 결정 표면 → 6-Layer 현행화는 **사용자가 이연 선택 가능한 가장 이연 가능한 delta**로 게이트 제시(§5·OQ-R2-3).

---

## 4. 잠재 충돌 지점 (Reconciling 대비)

- **단일 역할 run** — 동시 작성 타 역할 부재 → **cross-role 실충돌 대상 0**. Reconciling은 **내부 정합**만 검증한다(형태 B 실현 파급이 open·openQuestions·constraints·risks·decisions·본문에 모순 없이 반영되는지). 상세 = `reconciling-record.md`.
- 내부 정합 점검 대상: (a) open[0]↔openQuestions[0] 미러 일치 (b) open[0]↔risks[1] 형태 B 계수 일치 (c) con4↔dec3 형태 B posture 일치 (d) open[2]↔dec1 orchestration 언급 정합(중복 아님: dec1=구조/존재·open[2]=진화 축/잔여) (e) open[0]↔open[2] SD 실행 호스팅 이중 등재 방지.

---

## 5. open (open_questions — Reviewing/게이트 위임 · 추측 우회 0)

- **OQ-R2-1 (SP-INV 1 — Matured 기준선 정합·비차단)**: 04 §3.1-B는 성숙 입력을 `Ready`|`ReadyWithAssumptions`로 한정하나 v2는 `Matured` 종단이다. 03 §3.4 supersedes 계보 연쇄·본 위임이 v2를 유효 기준선으로 지시. 판단: Matured 인스턴스(완전성·사용자 승인 보유)는 성숙 기준선으로 유효하되 04 §3.1-B 문면 정합은 **04 정본 소관·Advisor 에스컬레이션**. 04에 "성숙 기준선은 직전 Matured 인스턴스를 포함한다"는 명확화 권고. 비차단(위임 명시 지시).
- **OQ-R2-2 (OQ-SH-4의 open[0] 편입 정당성·비차단)**: OQ-SH-4는 v2 open[0]의 5-OQ 목록에 부재. 형태 B/Step Host 축 인접 진척으로 문맥 반영했으나, "목록 제거"가 아니라 "인접 해소 문맥"임을 게이트에서 확인 요청. 대안: open[0]에서 SH-4 언급 제외(엄격 5-OQ 목록만) — Reviewing/사용자 선택.
- **OQ-R2-3 (decision[1] 6-Layer 현행화 채택 여부·게이트 옵션)**: orchestration Baseline 승격 유보 상태에서 decision 필드에 6-Layer를 확정할지, 아니면 decision[1]은 v2 "5-Layer" 유지하고 orchestration은 open[2](진화 축)에만 둘지 사용자 선택. 권고 = 실측 현행화(6-Layer·제자리·카운트 무변)이나 이연 허용.
- **OQ-R2-4 (거버넌스/이월 축 범위 밖·비차단)**: risks[2]·openQuestions[1](이월 개정 7건)은 **본 run 재감사 미수행**으로 무촉했다. v1.5/v1.6로 이월 인벤토리가 변했을 수 있으나(예: OQ-SH-4·OQ-LB-2 해소분), 본 아키텍처 run 범위 밖이다. 거버넌스 라벨/이월 재감사는 별도 run(r001의 governance-consistency 역할 유형)·별도 트랙 소관.
- **비차단 확인**: 위 4건은 전부 Reconciling/Reviewing/Validating에서 해소 가능한 조율 항목이며, 본 Proposal 산출을 차단하지 않는다(추측 우회 0 — 02-agent O4·O5).
