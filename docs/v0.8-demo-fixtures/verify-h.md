# verify-h — EX-DH(Hooks 확장 시연) CP2 독립 검증 리포트

작성일: 2026-07-06
상태: v0.8 PS-4 · Task EX-DH · CP2 (Verifier 독립 판정)
스키마 정본: specs/06-verifier.md §3.2-A/B/C (인스턴스: framework/verifier/verification-report.md)
판정 유형 정본: specs/06-verifier.md §3.2-E (인스턴스: framework/verifier/criteria-catalog.md)

**독립성 선언 (06 V1).** 이 리포트는 Worker 완료 보고·관측 기록(`ex-dh-observations.md`)의 `self_check`를 판정 근거로 삼지 않는다. 관측 기록의 주장은 검사 대상(claim)이며, 아래 판정은 전부 **산출물 직접 실측 + 독립 재구동·재관측**에 근거한다. 판정 대상·픽스처·loop-data·memory-data는 수정하지 않았다(06 INV-6) — 검증용 드라이버 재구동 산출은 전부 Verifier scratchpad로만 기록했다(픽스처 무오염).

---

## 1. target (판정 대상)

- **대상 작업:** UAHF v0.8 PS-4 병렬 집합 Task **EX-DH** (Hooks 확장 시연).
- **판정 대상 산출물 (실경로 — 직접 판독):**
  - 라이브 표면 F-H1: `.claude/hooks/audit-complete/manifest.md`, `.claude/hooks/audit-complete/audit.sh`
  - 픽스처 결함·보조: `docs/v0.8-demo-fixtures/f-h2-notify-fail/{manifest.md, action.sh}`, `f-h3-order-metrics/{manifest.md, action.sh}`, `f-h4-order-archive/{manifest.md, action.sh}`
  - Dispatch 드라이버(형태 A 호스트 절차): `docs/v0.8-demo-fixtures/ex-dh-dispatch-driver.sh`
  - Hook Registry 3상태: `docs/v0.8-demo-fixtures/ex-dh-registry-{a,b,c}.tsv`
  - 관측 산출 9파일: `docs/v0.8-demo-fixtures/ex-dh-observed/{demo-a-audit-log.txt, demo-a-dispatch.log, demo-b-audit-log.txt, demo-b-dispatch.log, demo-b-failure-reports.txt, demo-c-run1-dispatch.log, demo-c-run1-order-trace.txt, demo-c-run2-dispatch.log, demo-c-run2-order-trace.txt}`
  - 관측 기록(참고 입력 — claim): `docs/v0.8-demo-fixtures/ex-dh-observations.md`

## 2. criteria_basis (대조 기준 출처)

- **위임 완료 조건 (done 6항).** EX-DH 위임 done (1)~(6) — 본체 diff 0 / 감사 기록 실재 / 비차단 blocking=false / 순서 08 §3.1-D / 소유 경계·settings.json 부재 / 관측 실측 근거.
- **규격.** specs/08-hooks.md §3.1-D(순서 3단 기준)·§3.2-C(Event Record 5필드)·§3.2-D(Hook Binding 6필드)·§3.2-E(Hook Failure Report 6필드)·§8 예1·예2·예3; framework/adapters/claude/hooks-binding.md §4(직렬화·자기완결 경계)·§5(Dispatch 5단계·비차단). (Frozen 08 재정의 0 — 인스턴스만 대조.)
- **경계 규칙.** 소유 경계(절차서 §5.3, 07 R4·INV-2)·DP-E3(settings.json 미생성)·INV-1(본체 불가침)·INV-2(비차단)·INV-3(read-only)·INV-5(결정적 순서).
- **시연 기준.** 절차서 §8-D Hooks 판정 문장 6건의 예/아니오 환원·§6.6 본체 diff 0 측정 절차·§2.2 배정·§6.3 EX-DH 행·§8/§3.1 기록 포맷.
- **참고 입력 (판정 근거 아님, 06 V1).** `ex-dh-observations.md`의 self_check.

**Advisor 제공 사실 반영.** (i) planner.md·verifier.md 시연 창 내 변경 = 별도 사용자 지시 Task EX-R3(+Advisor 직접 수정, 선언된 동시 개정) → EX-DH 본체 diff-0 판정에서 제외. (ii) 픽스처 경계·라이브 표면의 물리 토큰·의도적 결함(F-H2)은 정당 보유 — verifier_scope 제외(DP-E7). (iii) AI 비의존 정적 스캔(specs/08 §3)·카탈로그 18행 도출(INV-6)·spec 일치는 마일스톤 CP2 소관 — 본 EX-DH CP2 판정 범위 아님.

---

## 3. items (항목별 판정)

### I1 — done(1) 본체 수정 0 시연: F-H1 등록만 → 본체 diff 0으로 감사 실행

| 필드 | 값 |
|---|---|
| `criterion` | F-H1(`lifecycle.complete`@after 감사 기록)을 `.claude/hooks/audit-complete/`에 등록만 하여, 이벤트 원천 코드·규격 diff = 0으로 `lifecycle.complete`@after에서 감사 로그가 실행됐는가(INV-1, §6.6)? |
| `verdict` | **충족 (Met)** |
| `evidence` | ① F-H1 실물 2파일 직접 판독 — `manifest.md`가 Module Manifest 7필드 + Hook Binding 6필드(hookId=audit-complete·event=lifecycle.complete·phase=after·order=0·action=./audit.sh·replaceable=true)를 담아 08 §8 예1과 필드 단위 일치. ② **감사 실행 독립 재구동** — Verifier가 repo 루트에서 `ex-dh-dispatch-driver.sh lifecycle.complete after ex-dh-registry-a.tsv 1`을 직접 실행(출력=scratchpad). 산출 감사 로그가 `demo-a-audit-log.txt`와 **바이트 동일**: `[audit] hookId=audit-complete eventId=lifecycle.complete phase=after sourceRef=loop-data:v08-demo-h.jsonl#lifecycle.complete contextView=read-only-projection(...) occurredAt=1`. ③ **본체 diff 0 corroboration** — `.claude/settings.json` 부재 실측(DP-E3); 저장소 전체 최근 수정 20파일 mtime 스캔 결과 전건이 demo-fixtures(EX-DH/DS/DP) 또는 Advisor 귀속 EX-R3(planner.md·verifier.md)이고 `specs/`·`framework/core/`·`framework/runtime/`·기존 loop-data·기존 memory-data 등 본체 파일 수정은 **0건**. EX-DH 기록은 자기 네임스페이스 밖으로 나가지 않음(경계 열거 — I5). |
| `scope` | F-H1 라이브 표면 2파일 직접 판독 + registry-a 독립 재구동 대조 + 저장소 전체 mtime 스캔 + settings.json 실측. **제외:** 시연 전 172파일 스냅샷(매니페스트 fingerprint `de20fda3…`)은 Worker의 역사적 측정으로, 본 저장소는 VCS 부재(env 실측)라 CP2 시점에 before-상태를 재도출할 수 없다 — 재도출 불가는 산출물의 근거 부족이 아니라 시점 제약이며, 기록 대조 + mtime 독립 corroboration + 경계 열거로 갈음했다. planner.md·verifier.md 동시 변경은 Advisor 귀속 EX-R3로 제외(§2). |
| `verification_type` | VT-5(시연 재구동) · VT-4(경계 diff 0) · VT-1(F-H1 산출물 존재) |

### I2 — done(2) 감사 기록 실재 (형태 A Dispatch 실수행)

| 필드 | 값 |
|---|---|
| `criterion` | `lifecycle.complete`@after 감사 기록이 형태 A Dispatch(hooks-binding §5.1 5단계)의 실수행 기록으로 실재하는가? |
| `verdict` | **충족 (Met)** |
| `evidence` | Verifier 독립 재구동 산출 dispatch 로그가 `demo-a-dispatch.log`와 **바이트 동일** — 형태 A 5단계 관측 가능: step1 관찰(occurredAt=1, 순서 값 L-09) → step2 해소[audit-complete] → step3 08 §3.1-D 정렬 → step4 격리 호출·성공 → "본 작업 결과 불변(INV-1)". Event Record 5필드는 드라이버가 `HOOK_EVENT_ID/PHASE/SOURCE_REF/CONTEXT_VIEW/OCCURRED_AT` 환경 변수(읽기 전용 투영)로 서브셸 격리 전달하고, `audit.sh`는 이를 **읽기만** 하고 자기 경계 산출물(감사 로그)에 append만 한다(INV-3 read-only — 소스 판독 확인, 이벤트 원천 상태 변경 0). |
| `scope` | registry-a 독립 재구동 dispatch 로그 대조 + audit.sh·드라이버 소스 직접 판독. 형태 B(하네스 native hook 실행)는 미도입(Bootstrap) — 판정 대상 아님. |
| `verification_type` | VT-5(시연 재구동) · VT-3(Event Record 5필드·형태 A 절차 규격) · VT-1 |

### I3 — done(3) 비차단: F-H2 실패 → blocking=false + 본 작업·F-H1 계속

| 필드 | 값 |
|---|---|
| `criterion` | F-H2 action을 의도적으로 실패시켜도 본 작업이 정상 완료되고 다른 Hook(F-H1)이 계속 실행되며 Hook Failure Report `blocking=false`인가(INV-2)? |
| `verdict` | **충족 (Met)** |
| `evidence` | Verifier가 `ex-dh-registry-b.tsv`(= {audit-complete order 0 regIndex 1, notify-fail order -10 regIndex 2})로 드라이버를 독립 재구동. ① **비차단**: `notify-fail`이 exit 1로 실패했음에도 드라이버 종료 **rc=0** — 본 작업(Dispatch)이 차단되지 않음을 직접 관측. ② **Hook Failure Report**: 재구동 산출이 `demo-b-failure-reports.txt`와 **바이트 동일** — `hookId: notify-fail / event: lifecycle.complete / phase: after / reason: action error (exit 1 …) / blocking: false / lesson_candidate: 예`(08 §3.2-E 6필드). ③ **다른 Hook 계속**: F-H2(order -10)가 F-H1(order 0)보다 **먼저** 실행돼 실패한 뒤에도, dispatch 로그(= `demo-b-dispatch.log`와 바이트 동일)가 `audit-complete` 호출·성공을 기록하고, 감사 로그(= `demo-b-audit-log.txt`와 바이트 동일, `occurredAt=2`)가 F-H1의 계속 실행을 실증. |
| `scope` | registry-b 독립 재구동 3산출(dispatch·failure·audit) 바이트 대조 + 드라이버 종료 코드 관측. F-H2의 의도적 결함은 정당 보유(DP-E7) — verifier_scope 제외 대상이나 비차단 실증 목적의 정당 입력. |
| `verification_type` | VT-5(시연 재구동) · VT-3(Hook Failure Report 6필드 규격) |

### I4 — done(4) 순서 결정성: F-H3(10)·F-H4(20) 08 §3.1-D + 반복 동일

| 필드 | 값 |
|---|---|
| `criterion` | 같은 (event, phase)의 F-H3·F-H4(order 10/20)가 08 §3.1-D 규칙(order 오름차순 → 등록 순서 → hookId 사전순)대로 결정적으로 실행되고 반복 실행에서 동일한가(INV-5)? |
| `verdict` | **충족 (Met)** |
| `evidence` | `ex-dh-registry-c.tsv`는 `archive`(order 20)를 **먼저** 나열(역순)하나, Verifier의 독립 재구동 order-trace = `metrics`↵`archive`로 `demo-c-run1-order-trace.txt`와 **바이트 동일** → 즉 등록 파일 나열 순서가 아니라 **order 1차 기준**이 순서를 결정(08 §3.1-D). dispatch 로그 step3 정렬도 `-> metrics (order=10) / -> archive (order=20)`. 드라이버 정렬 키 `sort -t TAB -k4,4n -k5,5n -k1,1` = 08 §3.1-D 3단(order asc → regIndex asc → hookId 사전순)의 충실한 실현. **결정성**: Verifier가 동일 registry로 2회 재구동한 order-trace가 서로 동일(C1≡C2)하며 `demo-c-run{1,2}-order-trace.txt`와도 바이트 동일. **범위 정직(관측 기록과 일치):** 이 짝은 order 10≠20이라 1차 기준에서 결정됐고, 2차(등록 순서)·3차(hookId 사전순) tie-breaker는 정렬 키에 구현됐으나 동률이 아니어서 발동되지 않았다. |
| `scope` | registry-c 2회 독립 재구동 order-trace·dispatch 로그 바이트 대조 + 드라이버 정렬 키 소스 대조. 3단 기준 중 1차만 실발동(동률 tie-breaker 미검증 — 이 짝의 값 구성상 도달 불가, 정직 명시). |
| `verification_type` | VT-5(시연 재구동) · VT-3(08 §3.1-D 규격 대조) |

### I5 — done(5) 소유 경계 안 + 경계 밖 수정 0 + settings.json 부재(DP-E3)

| 필드 | 값 |
|---|---|
| `criterion` | 전 산출이 EX-DH 소유 경계(절차서 §5.3) 안이고 경계 밖 수정이 0건이며 `.claude/settings.json`이 미존재하는가(DP-E3)? |
| `verdict` | **충족 (Met)** |
| `evidence` | **경계 전수 열거**: EX-DH 기록 전건이 `.claude/hooks/audit-complete/`(2파일) + `docs/v0.8-demo-fixtures/`의 EX-DH 네임스페이스(`ex-dh-dispatch-driver.sh`·`ex-dh-registry-{a,b,c}.tsv`·`ex-dh-observations.md`·`ex-dh-observed/`(9)·`f-h2-notify-fail/`(2)·`f-h3-order-metrics/`(2)·`f-h4-order-archive/`(2)) 안에 위치 — 형제(EX-DS `F-S*`·`ex-ds-*`·`mock-context-*`, EX-DP `report-exporter/`·`ex-dp-*`)와 파일 단위 교집합 0. **settings.json 부재** 실측(`ls` → No such file). **경계 밖 수정 0**: 저장소 mtime 스캔상 EX-DH가 `.claude/agents/`·`specs/`·`framework/` 등에 쓴 기록 0건 — planner.md·verifier.md는 EX-DH 연산이 아니라 Advisor 귀속 EX-R3(§2). |
| `scope` | `.claude/hooks/` + `docs/v0.8-demo-fixtures/` EX-DH 네임스페이스 전수 열거 + settings.json 실측 + 저장소 최근 수정 파일 mtime 스캔. VT-4 전수 스캔(단일 대리 지표 아님 — 후보 경계 전 범위). |
| `verification_type` | VT-4(경계 전수 스캔) |

### I6 — done(6) 관측이 실측 근거(실경로·실값) 기반 (거짓 완료 보고 부재)

| 필드 | 값 |
|---|---|
| `criterion` | 관측 기록의 근거가 실경로·실값 기반이며 관측 주장과 실제 산출물이 일치하는가(거짓 완료 보고 부재, 06 §3.2-F)? |
| `verdict` | **충족 (Met)** |
| `evidence` | Verifier가 실 action 스크립트·실 registry로 드라이버를 독립 재구동한 결과, 관측 산출 **9파일 전건**이 재구동 산출과 **바이트 동일**(일치 9 / 불일치 0): 감사 로그 2(demo-a·demo-b), dispatch 로그 4(demo-a·demo-b·demo-c-run1·demo-c-run2), failure report 1(demo-b), order-trace 2(demo-c-run1·run2). 즉 관측 기록의 주장이 실 산출물과 모순되지 않음을 독립 재관측으로 확인 — self_check가 정직하고 검사 범위도 실경로·실값에 부합(관측 기록 §0 실행 방식·§0.1 실경로 표와 정합). |
| `scope` | 관측 9파일 vs Verifier scratchpad 재구동 산출 바이트 대조(diff -q, 전건). 관측 기록의 서술적 결론(예: "충족")은 근거로 삼지 않고 실 산출 로그만 재판정 근거로 사용(06 V1). |
| `verification_type` | VT-5(재관측·재계산) |

### I7 — 절차서 §2.2·§6.3·§8/§3.1 기록 포맷 정합

| 필드 | 값 |
|---|---|
| `criterion` | 관측 기록이 절차서 §3.1 5필드 기록 포맷을 채우고, §2.2 Hooks 재현 배정·§6.3 EX-DH 행(기대 Pass·verifier_scope AI-scan 제외)과 정합하는가? |
| `verdict` | **충족 (Met)** |
| `evidence` | 관측 기록 §1의 6개 판정이 §3.1 공통 기록 포맷 5필드(판정 문장·관측 결과·근거·수행 단계 로그·수행 물리 지점)를 채움. 절차서 §2.2가 마일스톤 CP2로 배정한 두 문장 — 판정 4(카탈로그 도출 INV-6)·판정 6(§3 AI 비의존 INV-8) — 을 관측 기록이 **판정 불가(EX-DH 재현 범위 밖 — 마일스톤 CP2 소관)**로 정확히 라우팅(재현으로 위장하지 않음). §6.3 EX-DH 행의 verifier_scope(픽스처·라이브 표면 토큰 AI-scan 제외, DP-E7) 준수. |
| `scope` | 관측 기록 §0~§4 직접 판독 + 절차서 §2.2·§6.3·§3.1·§8 대조. 마일스톤 CP2 소관 문장(판정 4·6) 자체의 성립 여부는 본 EX-DH CP2 범위 아님(verifier_scope 제외). |
| `verification_type` | VT-3(기록 포맷 규격) · VT-2(배정 대조) |

### I8 — F-H1 Manifest 구조 vs hooks-binding §4 정본 구조 일치 (contract 인스턴스 값 확인)

| 필드 | 값 |
|---|---|
| `criterion` | F-H1 `manifest.md` 구조가 hooks-binding §4 정본 구조(자기완결 경계·Module Manifest 7필드 + Hook Binding 6필드 직렬화)와 일치하고, `contract: HookModule`이 계약 재정의가 아닌 인스턴스 값인가? |
| `verdict` | **충족 (Met)** |
| `evidence` | `manifest.md`가 `.claude/hooks/<hookModuleId>/` 자기완결 경계(hooks-binding §4.1) 안에 Module Manifest 7필드(01 §3.2-A: id·contract·version·requires·entrypoint·configSchema·replaceable)와 Hook Binding 6필드(08 §3.2-D: hookId·event·phase·order·action·replaceable, 필수/기본값 표기 보존)를 front-matter로 병치 — hooks-binding §4.2 직렬화 표기와 일치. `entrypoint: ./audit.sh`가 Hook Binding `action`과 정합(§4.4). **`contract: HookModule`**은 01 §3.2-A `contract` 필수 필드를 채우는 **인스턴스 값**이며(08·hooks-binding이 Hook Module 정본 contract 값을 규정하지 않음, OQ-EH2), 새 Glossary 용어·Frozen 08 계약 재정의가 아님 — 확인 완료. (인스턴스 값의 정식 채택은 CP3 거버넌스 항목이며 CP2 차단 사유 아님.) |
| `scope` | F-H1·F-H2/H3/H4 manifest 5건 직접 판독 + hooks-binding §4.1/§4.2/§4.4 대조. 형태 B 실행 훅 결선(OQ-EH3)은 미도입 — 대상 아님. |
| `verification_type` | VT-3(규격 준수) |

---

## 4. final_verdict (최종 판정 — 06 §3.2-C 결정적 도출)

- 항목별 판정: 충족(Met) **8** / 위반(Violated) **0** / 판정 불가(Undetermined) **0**.
- 06 §3.2-C 도출 규칙: 모든 항목이 충족(Met) → **통과(Pass)**.

### **final_verdict = 통과 (Pass)**

EX-DH의 done 6항 + 절차서 정합 + F-H1 구조 대조가 전 항목 충족됐다. 판정 근거는 전부 산출물 직접 실측과 Verifier 독립 재구동(드라이버 4회 재실행 → 관측 9파일 바이트 일치)·저장소 mtime 전수 스캔에 근거하며, Worker 관측 기록의 self_check는 판정 근거가 아닌 검사 대상으로만 취급했다(06 V1). 관측 주장과 실 산출물 간 모순(거짓 완료 보고)은 검출되지 않았다(06 §3.2-F).

**게이트 경계.** Pass는 CP2(독립 판정) 통과다. 마일스톤 최종 승인(CP3)·재량 판정은 Advisor 소관이며, 본 리포트는 재량 승인을 하지 않는다(06 §1 Non-Goals, 02 §3.2-A).

---

## 5. verifier_scope (검사·제외 범위 — 06 V4)

**검사한 범위 (직접 실측·재구동):**
- F-H1 라이브 표면 2파일 + F-H2/F-H3/F-H4 픽스처 6파일 + 드라이버 + registry 3 + 관측 9파일 직접 판독.
- 드라이버 **독립 재구동 4회**(registry-a 1 / registry-b 1 / registry-c 2회) — 산출을 Verifier scratchpad에 기록하고 관측 9파일과 바이트 대조(일치 9 / 불일치 0). 드라이버 종료 코드(비차단 rc=0)·결정성(C1≡C2) 관측.
- `.claude/settings.json` 부재 실측(DP-E3). 저장소(`specs`·`framework`·`.claude`·`docs`) 최근 수정 파일 mtime 전수 스캔.
- F-H1 manifest 구조 vs hooks-binding §4 대조.

**검사하지 못했거나 제외한 범위 (정직 기록):**
- **(a) 시연 전 172파일 본체 스냅샷(fingerprint `de20fda3…`)** — Worker의 역사적 측정으로, 본 저장소는 VCS 부재(env 실측)라 CP2 시점에 before-상태 바이트를 재도출할 수 없다. 이는 산출물의 근거 부족이 아니라 시점 제약이며, (i) F-H1 감사 실행 재구동, (ii) EX-DH 경계 전수 열거, (iii) settings.json 부재, (iv) 저장소 mtime 스캔(본체 파일 수정 0)으로 "EX-DH 기여분 본체 diff 0"을 독립 corroboration했다.
- **(b) planner.md·verifier.md 시연 창 내 변경** — Advisor 귀속 별도 Task EX-R3(선언된 동시 개정)이므로 EX-DH diff-0 판정에서 제외(Advisor 지시). **투명 기록:** 관측 기록 §2는 `planner.md` 1건만 명시했으나, mtime상 `verifier.md`(2026-07-06T16:34:07)도 동일 창에서 변경됐다. 둘 다 EX-DH 연산이 아니고(경계 열거상 EX-DH는 `.claude/agents/`에 쓰지 않음) Advisor 제외 대상이라 EX-DH 판정은 불변이나, 관측 기록의 해당 열거는 1건 누락(verifier.md 미기재)이 있었음을 기록한다 — 판정 영향 없음.
- **(c) AI 비의존 정적 스캔(specs/08 §3)·카탈로그 18행 도출(INV-6)·spec 일치(ROADMAP ③)** — 절차서 §2.2·Advisor 지시상 **마일스톤 CP2 소관**으로, 본 EX-DH CP2 판정 범위가 아니다(관측 기록도 판정 4·6을 판정 불가로 정확히 라우팅).
- **(d) 픽스처 경계·라이브 표면 물리 토큰(`.sh`·경로 등)** — 실계약 §3 AI-scan 대상에서 제외(DP-E7). 픽스처의 의도적 결함(F-H2)은 비차단 실증 목적의 정당 보유.
- **(e) 형태 B(하네스 native hook 실행·settings.json 실행 훅)** — 미도입(Bootstrap 상태) — 판정 대상 아님. 본 판정은 형태 A(호스트 절차 구동)만 대상으로 한다.

---

## 6. rework (재작업 지시)

**없음.** (final_verdict = Pass — 위반·판정 불가 항목 0건. 06 §3.2-A: Pass이면 "없음".)

---

## self-note (경계·무수정)

- 이 리포트는 06 §3.2-A 스키마(framework/verifier/verification-report.md 인스턴스)의 인스턴스이며 계약을 재정의하지 않는다. 판정 유형 라벨(VT-1~VT-5)·판정 값(충족/위반/판정 불가)·도출 규칙(통과/실패/조건부)은 06 §3.2 정본 어휘다.
- 본 판정으로 생성한 파일은 이 1개(`docs/v0.8-demo-fixtures/verify-h.md`)뿐이다. 판정 대상·픽스처·loop-data·memory-data를 수정하지 않았다(06 INV-6) — 검증 드라이버 재구동 산출은 전부 Verifier scratchpad로만 기록해 픽스처 경계를 오염시키지 않았다.
- Verify 단계의 시점·전이·시퀀싱은 정의하지 않는다(06 INV-9, 03-loop 소관). 최종 승인·재량은 Advisor(CP3) 소관이다.
