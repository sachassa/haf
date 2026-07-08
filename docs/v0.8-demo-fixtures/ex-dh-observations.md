# EX-DH — Hooks 확장 시연 관측 기록 (Execute 산출)

**시연 관측 기록 — 실계약 문서 아님.** 이 파일은 v0.8 PS-4 병렬 집합 Task **EX-DH**(Hooks 확장 시연)의 Worker Execute 관측 기록이다. 판정 값(충족/위반/판정 불가)의 **최종 판정은 CP2(Verifier — verify-h.md)·CP3(Advisor)** 소관이며, 이 기록은 그 입력이다. 자기 점검은 최종 승인이 아니다 (02 §3.2-A).

작성 시점 실측: 2026-07-06. 정본: specs/08-hooks.md §3·§7·§8, framework/adapters/claude/hooks-binding.md §4·§5. 계약 재정의 0(Frozen 08).

---

## §0. 실행 방식 — 형태 A / 형태 B 정직 구분 (L-07)

- Bootstrap 상태이므로 Hook Dispatch는 **형태 A**(호스트=주 세션 오케스트레이션 절차 구동, hooks-binding §5.1)로 **실수행**했다. 시연 드라이버 `ex-dh-dispatch-driver.sh`가 hooks-binding §5.1의 5단계를 실행 가능한 절차로 실현한다.
- 이 드라이버는 **하네스 native hook 실행 메커니즘(형태 B — `.claude/settings.json` 실행 훅)이 아니다**. `.claude/settings.json`은 생성·수정하지 않았다(DP-E3) — 실측 결과 여전히 미존재.
- `occurredAt`·순서 값은 논리 시각이며 벽시계 시각이 아니다 (L-09, hooks-binding §5.2). 아래 관측에 벽시계 시각 주장을 넣지 않았다.
- Hook action·감사 기록·Hook Failure Report·order-trace는 드라이버가 실제 action 스크립트를 실행해 **실재 생성**한 파일이다("수행했다" 서술이 아니라 실산출 — L-07).

## §0.1 산출물 실경로 (실측)

| 산출 | 실경로 |
|---|---|
| F-H1 레퍼런스 Hook Module (라이브 표면) | `.claude/hooks/audit-complete/manifest.md`, `.claude/hooks/audit-complete/audit.sh` |
| F-H2 비차단 실패 Hook (픽스처) | `docs/v0.8-demo-fixtures/f-h2-notify-fail/{manifest.md,action.sh}` |
| F-H3 순서 Hook `metrics` (픽스처) | `docs/v0.8-demo-fixtures/f-h3-order-metrics/{manifest.md,action.sh}` |
| F-H4 순서 Hook `archive` (픽스처) | `docs/v0.8-demo-fixtures/f-h4-order-archive/{manifest.md,action.sh}` |
| Dispatch 드라이버 (형태 A 호스트 절차) | `docs/v0.8-demo-fixtures/ex-dh-dispatch-driver.sh` |
| Hook Registry 상태 (승계 3상태) | `docs/v0.8-demo-fixtures/ex-dh-registry-{a,b,c}.tsv` |
| 관측 산출 (감사 기록·실패 보고·순서·dispatch 로그) | `docs/v0.8-demo-fixtures/ex-dh-observed/` |

---

## §1. 판정별 관측 (§3.1 공통 기록 포맷 · §8-D Hooks 판정 문장)

### 판정 1 — 본체 수정 0 시연 (08 §7 / INV-1 / done 1·2)

| 필드 | 내용 |
|---|---|
| **판정 문장** | F-H1(`lifecycle.complete`@after 감사 기록)을 `.claude/hooks/audit-complete/`에 등록만 하여, 이벤트 원천 코드·규격 diff = 0으로 `lifecycle.complete`@after에서 감사 로그가 실행됐는가(INV-1, §6.6)? (예 → 충족 / 아니오 → 위반) |
| **관측 결과** | **충족** (EX-DH 기여분 본체 diff 0 + 감사 기록 실재 생성). 단, 동시 실행 중인 PS-4 형제/Advisor 활동에 의한 `.claude/agents/planner.md` 동시 변경 1건을 §2에 은폐 없이 기록·에스컬레이션(내 소유 경계 밖·내 연산 아님). |
| **근거 (관측한 것)** | ① F-H1 Hook Module 등록만으로 확장 — `.claude/hooks/audit-complete/manifest.md`(Module Manifest 7필드 + Hook Binding 6필드: hookId=audit-complete·event=lifecycle.complete·phase=after·order=0·action=./audit.sh·replaceable=true) + `.claude/hooks/audit-complete/audit.sh`. 08 §8 예1 동형. ② **감사 기록 실재 생성** — `ex-dh-observed/demo-a-audit-log.txt` 실내용: `[audit] hookId=audit-complete eventId=lifecycle.complete phase=after sourceRef=loop-data:v08-demo-h.jsonl#lifecycle.complete contextView=read-only-projection(원천 spec 소유 — 08 §3.2-C) occurredAt=1`. 형태 A Dispatch 5단계 실수행 로그: `ex-dh-observed/demo-a-dispatch.log`(step1 관찰 → step2 해소[audit-complete] → step3 정렬 → step4 격리 호출·성공 → 본 작업 결과 불변). ③ 본체 diff 측정(§6.6, §2): 시연 전 172파일 스냅샷 대비 EX-DH 연산이 기존 파일 변경 0, 내 추가분 21건 전건이 선언된 EX-DH 산출물. |
| **수행 단계 로그** | §6.6 단계 1(시연 전 스냅샷 172파일 SHA-256, scratchpad/body-pre.manifest, fingerprint de20fda3…) → F-H1 Module 생성(Write) → 드라이버로 registry-a Dispatch 실행(occurredAt=1) → 감사 기록 생성 확인 → §6.6 단계 2·3 재열거·전수 대조. |
| **수행 물리 지점** | 라이브 표면 `.claude/hooks/audit-complete/`; 드라이버·registry·관측 = `docs/v0.8-demo-fixtures/`; 계측 지점 대응 = hooks-binding §3(`lifecycle.complete` → loop-binding §3 전이 이벤트 기록 지점, 형태 A 실계측 가능). |

### 판정 2 — 비차단 시연 (08 §7 / INV-2 / done 3)

| 필드 | 내용 |
|---|---|
| **판정 문장** | F-H2 action을 의도적으로 실패시켜도 본 작업이 정상 완료되고 다른 Hook이 계속 실행되며 Hook Failure Report `blocking=false`인가(INV-2)? (예 → 충족 / 아니오 → 위반) |
| **관측 결과** | **충족** |
| **근거 (관측한 것)** | Registry B = {F-H1(order 0), F-H2(order −10)}에서 (lifecycle.complete, after) Dispatch(occurredAt=2). ① **순서(step3 정렬)**: `ex-dh-observed/demo-b-dispatch.log` — `-> notify-fail (order=-10, regIndex=2)` 먼저, `-> audit-complete (order=0, regIndex=1)` 다음. ② **F-H2 실패·비차단**: step5 로그 `hookId=notify-fail 실패(rc=1) — Hook Failure Report(blocking=false) 기록. 본 작업·다른 Hook 계속 (INV-2)`. Hook Failure Report 실내용(`ex-dh-observed/demo-b-failure-reports.txt`): `hookId: notify-fail / event: lifecycle.complete / phase: after / reason: action error (exit 1 — 모사 timeout/오류) / blocking: false / lesson_candidate: 예`. ③ **다른 Hook(F-H1) 계속**: F-H2 실패 **이후에** F-H1이 호출·성공 → `ex-dh-observed/demo-b-audit-log.txt` 실내용 `[audit] hookId=audit-complete ... occurredAt=2` 실재. ④ **본 작업 결과 불변**: dispatch.log 말미 `본 작업 결과 불변 (INV-1) — Hook 결과와 독립`. 드라이버 종료 rc=0(비차단). |
| **수행 단계 로그** | registry-b 구성(F-H2 order −10로 F-H1보다 먼저 실행 → 실패 후 F-H1 계속 실증) → Dispatch 실행 → 실패 보고·감사 기록·dispatch 로그 3산출 대조. |
| **수행 물리 지점** | F-H1 라이브 표면 + F-H2 픽스처 경계(형태 A 규약 등록, 라이브 미오염 DP-E7); 관측 = `ex-dh-observed/demo-b-*`. |

### 판정 3 — 순서 결정성 시연 (08 §7 / INV-5 / done 4)

| 필드 | 내용 |
|---|---|
| **판정 문장** | 같은 (event, phase)의 F-H3·F-H4(order 10/20)가 08 §3.1-D 규칙(order 오름차순 → 등록 순서 → hookId 사전순)대로 결정적으로 실행됐는가(INV-5)? (예 → 충족 / 아니오 → 위반) |
| **관측 결과** | **충족** |
| **근거 (관측한 것)** | Registry C = {F-H3 `metrics` order 10 regIndex 1, F-H4 `archive` order 20 regIndex 2}에서 (agent.completionReport, after) Dispatch. **registry 파일에는 일부러 archive를 먼저 나열**(역순)했으나 관측 순서는 order로 결정됨. ① `ex-dh-observed/demo-c-run1-order-trace.txt` 실내용: `metrics` 다음 줄 `archive` → F-H3(order 10) → F-H4(order 20). ② `demo-c-run1-dispatch.log` step2 해소는 archive 먼저 수집했으나 step3 정렬은 `-> metrics (order=10) / -> archive (order=20)` → **1차 기준 order 오름차순이 입력/등록 순서를 이김**(08 §3.1-D). ③ **결정성 반복(INV-5)**: 동일 registry 2회 실행 → `demo-c-run2-order-trace.txt`도 `metrics`,`archive` 동일. 08 §8 예3 동형. **범위 정직**: F-H3/F-H4 짝은 order 10≠20이므로 **1차 기준에서 결정**됐다. 2차(등록 순서)·3차(hookId 사전순) tie-breaker는 드라이버 정렬 `sort -k4,4n -k5,5n -k1,1`에 구현됐으나 이 짝에서는 동률이 아니어서 발동되지 않았다(08 §3.1-D 3단 기준 중 1차만 실발동 — 정직 명시). |
| **수행 단계 로그** | registry-c(역순 나열) 구성 → Dispatch run1 → order-trace 관측 → 결정성 확인 위해 run2 재실행 → 동일 순서 대조. |
| **수행 물리 지점** | F-H3·F-H4 픽스처 경계(형태 A 규약 등록); 관측 = `ex-dh-observed/demo-c-run{1,2}-*`. |

### 판정 4 — 카탈로그 도출 시연 (08 §7 / INV-6 — 마일스톤 CP2 소관)

| 필드 | 내용 |
|---|---|
| **판정 문장** | 08 §3.2-A 카탈로그 18행 각 Event가 원천 계약 근거 열에서 도출되고 미도출 Event가 0건인가(INV-6)? |
| **관측 결과** | **판정 불가 (EX-DH 재현 범위 밖 — 마일스톤 CP2 소관)**. 절차서 §2.2가 이 문장을 **마일스톤 CP2**(specs/08 §3.2-A 18행 정적 대조)로 배정. EX-DH 재현이 아님. |
| **근거 (관측한 것)** | EX-DH가 소비한 Event(`lifecycle.complete`·`agent.completionReport`)는 08 §3.2-A 카탈로그·hooks-binding §3에 등재된 도출 Event다(각각 Glossary §3.2-F / 02 §3.2-C 원천). 18행 전건 도출 여부의 전수 대조는 CP2가 specs/08 §3.2-A 본문을 대상으로 수행한다. |
| **수행 단계 로그** | (해당 없음 — CP2 정적 판정 배정.) |
| **수행 물리 지점** | specs/08-hooks.md §3.2-A(CP2 대상). |

### 판정 5 — 경계 시연 (08 §7 / INV-3·INV-7 / done 5-일부)

| 필드 | 내용 |
|---|---|
| **판정 문장** | Hook이 Event Record를 변경하지 못하고(read-only, INV-3), Memory 접근 시 단일 Port만 경유하며(INV-7), 역할 경계·Verify 판정을 침범하지 않는가? |
| **관측 결과** | **충족** (재현 + 정적 보강; 경계 성질 정적 대조는 CP2 보강). |
| **근거 (관측한 것)** | ① **read-only(INV-3)**: 드라이버는 Event Record 5필드를 **환경 변수(읽기 전용 투영)**로만 전달(`HOOK_EVENT_ID`·`HOOK_PHASE`·`HOOK_SOURCE_REF`·`HOOK_CONTEXT_VIEW`·`HOOK_OCCURRED_AT`). action 스크립트(`audit.sh`·`f-h*/action.sh`)는 이 값을 **읽기만** 하고 이벤트 원천 상태를 변경하지 않는다(각 action 소스에 read-only 주석 명시). 부수 동작은 자기 경계 안 산출물(감사 로그·order-trace) 기록뿐(08 §3.1-B 할 수 있는 것). ② **Memory 단일 Port(INV-7)**: EX-DH의 어떤 Hook action도 Memory에 접근하지 않는다 — Memory 우회 0건(접근 자체가 0). 접근이 필요했다면 단일 Port만 경유해야 한다(08 §5). ③ **역할 경계·Verify 불침범(INV-7)**: Hook은 관찰·부수 동작만 하며 역할 경계(02 §3.2-A)를 행사하지 않고 Verify 판정을 대체·무효화하지 않는다. `lifecycle.verify`는 EX-DH 시연에서 바인딩하지 않았고(관찰만 대상), Verify 판정은 CP2 소관으로 불침범. |
| **수행 단계 로그** | action 스크립트 read-only 설계 확인 → Memory 미접근 확인 → 역할/Verify 불침범 설계 확인. |
| **수행 물리 지점** | action 스크립트 소스(`.claude/hooks/audit-complete/audit.sh`, `docs/v0.8-demo-fixtures/f-h*/action.sh`), 드라이버 격리 호출 블록. |

### 판정 6 — §3 AI 비의존 시연 (08 §7 / INV-8 — 마일스톤 CP2 소관)

| 필드 | 내용 |
|---|---|
| **판정 문장** | specs/08-hooks.md §3 본문에 특정 AI 모델명·제품 기능 토큰이 0건인가(INV-8, DoD-3 — 픽스처·라이브 표면 verifier_scope 제외)? |
| **관측 결과** | **판정 불가 (EX-DH 재현 범위 밖 — 마일스톤 CP2 소관)**. 절차서 §2.2가 specs/08 §3 전수 스캔을 CP2로 배정. |
| **근거 (관측한 것)** | EX-DH 픽스처·라이브 표면(`.claude/hooks/audit-complete/`·`docs/v0.8-demo-fixtures/` EX-DH 파일)의 물리 토큰(`.sh`·경로 등)은 **verifier_scope에서 제외**된다(절차서 §4.1, DP-E7) — 시연 물리 토큰이 실계약 §3 경계 위반으로 계상되지 않게 한다. §3 본문 AI 토큰 0건 전수 스캔은 CP2가 specs/08-hooks.md §3을 대상으로 직접 수행. |
| **수행 단계 로그** | (해당 없음 — CP2 정적 스캔 배정.) |
| **수행 물리 지점** | specs/08-hooks.md §3(CP2 대상). |

---

## §2. 본체 diff 0 측정 (§6.6 전수 대조 — done 1)

**측정 방법(§6.6 예/아니오 판정 가능 절차):** 시연 전 본체 스냅샷(SHA-256 전수) → 시연 후 재열거 → 경로 join 해시 대조.

- **단계 1 — 시연 전 스냅샷.** EX-DH 착수 전 저장소 전 파일 **172건** SHA-256 매니페스트 확보(scratchpad `body-pre.manifest`, 매니페스트 fingerprint `de20fda37f19b7ad0618ffbf38fde9357fe0e3d37f542fad9be43be8baa2dcf1`). 이 시점 실측: `docs/v0.8-demo-fixtures/` 미존재, `.claude/hooks/` 빈 디렉터리, `.claude/settings.json` 미존재, loop-data 6파일, memory-data 47건, framework/plugins/ 3문서.
- **단계 2·3 — 재열거·전수 대조(경로 join).** 시연 후 재열거 → 기존 172경로 삭제 **0건**, 기존 파일 내용 변경 검사 결과: **171건 바이트 동일**.
- **기존 파일 변경 1건 — 은폐 없이 기록(§8-F, L-07):** `.claude/agents/planner.md`(SHA-256 `d464…` → `e550…`). **이 변경은 EX-DH 연산이 아니다** — EX-DH는 `.claude/agents/`에 어떤 쓰기도 하지 않았다(내 Write·Bash 대상은 전부 `.claude/hooks/audit-complete/`·`docs/v0.8-demo-fixtures/` 뿐). 동시 실행 중인 PS-4 형제 Task 또는 Advisor 주 세션 활동(Planner 서브에이전트 디스패치는 PS-4 중 발생)에 의한 **동시 변경**으로, **내 소유 경계 밖**(07 R4)이다. planner.md는 손상되지 않음(정상 front-matter, 9,479 bytes 실측). 이 건은 마일스톤 CP2/CP3 판단 대상으로 에스컬레이션한다(완료 보고 open_questions — 비차단).
- **EX-DH 추가분 = 선언된 시연 산출물 21건(전건 소유 경계 안):** `.claude/hooks/audit-complete/`(2) + `docs/v0.8-demo-fixtures/{ex-dh-dispatch-driver.sh, ex-dh-registry-a/b/c.tsv, ex-dh-observed/*(9), f-h2-notify-fail/*(2), f-h3-order-metrics/*(2), f-h4-order-archive/*(2)}`(19). 전건이 절차서 §6.6 "허용되는 추가분(라이브 표면 레퍼런스·픽스처 경계)"에 해당.
- **형제(EX-DS/EX-DP) 동시 추가분 10건은 내 것이 아니다:** `.claude/skills/commit-message-writer/`·`docs/v0.8-demo-fixtures/{F-S2,F-S3,mock-context-*}`·`report-exporter/`·`framework/plugins/report-exporter/`. EX-DH는 이들을 생성·참조·수정하지 않았다(07 R2·R4).

**결론(EX-DH 기여분):** EX-DH의 F-H1 추가·시연 실행은 기존 본체 파일을 **0건 변경**했다(내 21추가분 전건이 선언된 산출물, 내 연산의 기존 파일 변경 0). 전 저장소 관측된 유일한 기존 파일 변경(planner.md)은 EX-DH 연산 밖 동시 변경으로 §8-F에 따라 은폐 없이 기록·에스컬레이션했다.

---

## §3. 경계 준수 (done 5 · 07 R4 / DP-E3 / R2)

- **소유 경계 안(07 R4):** 전 산출 21건이 `.claude/hooks/audit-complete/`·`docs/v0.8-demo-fixtures/`(EX-DH 네임스페이스 `ex-dh-*`·`f-h2/h3/h4-*`) 안. 경계 밖 파일 수정 0(§2 planner.md는 내 연산 아님).
- **DP-E3:** `.claude/settings.json` 생성·수정 0 — 실측 여전히 미존재.
- **불접촉 확인:** loop-data(Advisor 소관) 생성 0, memory-data 불접촉, `.claude/skills/`·framework/plugins/·기존 loop-data 6파일·기존 memory-data 47건 무수정. 결함 픽스처(F-H2)·순서 보조(F-H3/F-H4)는 픽스처 경계에만(라이브 표면 미배치 — DP-E7).
- **R2:** 동시 작성 중인 EX-DS·EX-DP 산출물을 참조·인용하지 않음 — 확정 정본(08 §3·§7·§8, hooks-binding, specs/01 §3.2-A)만 참조.

---

## §4. self-note (정본 경계)

Hook Binding 6필드·Event 카탈로그·순서 3단 기준·격리·비차단·Event Record 5필드·Hook Failure Report 6필드의 정본은 specs/08-hooks.md §3이며, 물리 실현은 hooks-binding §4·§5다. 이 기록과 산출물은 그 계약의 인스턴스이며 재정의·창설 0(Frozen 08). `contract: HookModule`은 01 §3.2-A `contract` 필수 필드 충족용 Worker 제안 인스턴스 값이며(hooks-binding OQ-EH2 — Advisor 채택 대상), 신규 Glossary 용어가 아니다.
