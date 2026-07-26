# 절차 비례화(Process Proportionality) 트랙 — 원장 (채택본)

작성: Planner (Advisor 위임) · 2026-07-26 · **Advisor 채택 2026-07-26**(§9 채택 대상 8건 전건 — 하중 사실 6건[F-1·F-3·F-7·F-10·F-12·F-13] Advisor 코드 실물 재확인 후)
지위: **채택된 트랙 계획·원장**(수명 등급 = 트랙 live 문서·종결 시 아카이브). 이하 본문의 "초안(draft)" 자기 지칭은 작성 시점 표기로 보존한다(uaf-allow-legacy: 작성 시점 지위 문면의 이력 보존 — 채택 지위는 본 헤더가 정본).

## 게이트 확정 기록 (Wave 0 종결 — 2026-07-26)

| # | 결정 | 확정값 | 주체 |
|---|---|---|---|
| Q-1 | 통합 설계 문서 1종 | id `solution-design` · `<workspace>/docs/solution-design.md` (§6.1 (a)) | 사용자 카드 |
| Q-2 | CP2 차등의 의미 | (a) CP2 디스패치 유지 + 판정 근거 스크립트 AC + 모델 저티어 차등 — (b)는 기확정 불변("검증 하한 유지"·사용자 게이트 1차)과 정면 충돌이라 재론 불가 | Advisor(기확정 귀결) |
| Q-3 | 레인 로더·레지스트리 배치 | `orchestration/adapters/claude/` (게이트·강제 계열 동거) | Advisor(설계 결정) |
| Q-4 | SD 스킵 경로 | **폐기 방향 확정** · 실행은 경량 프로파일 실증(Wave 5) 후 별도 04 정본 개정 트랙(유형 A·버전 상승·사용자 승인) | 사용자 카드 |
| Q-5 | 경량 인터뷰 예산 | 총 **20**문 · soft **15** · hard **20** (차원 5종 전부 유지·Contract 완전성 무면제 불변) | 사용자 카드 |
| Q-6 | 최종 응답 상한 | **5,000자 AND 40줄** · 보고 파일 경로 1건 필수 | 사용자 카드 |
| Q-7 | 상한 수치 소유 | **옵션 B** — AGENT.md 무촉·delegation-protocol(운용 지침) + 역할 정의 3종 소유 | 사용자 카드 |

착수 편성(Advisor): Wave 1·2 = 최소 성립 집합 우선 착수(K-10) · W1-a↔W1-b는 같은 문서(§7A.2) append 충돌 회피를 위해 **순차**(W1-a → W1-b — 병렬 집합 문면 중 동시 실행만 조정·브리프 내용 무변) · Wave 2는 W2-a ∥ W2-b 병렬(파일 무교차·lane 어휘 "standard"|"lightweight" 고정 선전달).

`uaf-verified:` 본 초안의 사실 주장은 아래 §0 근거 표의 파일을 직접 판독하고, 코드 경로 4건(`design_completeness.py`·`resolve_gate.py`·`contract_to_graph.py`·`gates.py`)과 정책 데이터 3건(`solution-design-data/policy/default-policy.yaml`·`discovery-data/policy/default-policy.yaml`·`orchestration-data/e2e/policy/allocation.json`)을 좌표 단위로 대조해 얻었다. **스윕 범위 = 위임 §조사 대상 표면 + 그로부터 파생 추적된 호출·참조 지점**이며, 그 밖(소비 프로젝트 워킹트리·`uahf/specs/` 00~13 전문·테스트 스위트 실행)은 이 초안의 범위 밖이다. 범위 밖 항목은 §7 미검증 축 목록에 열거한다.

---

## [착수 전 점검]

필수 필드 7/7 존재 · done 6/6 이진 판정 가능 · context 11/11 실재

- **필드 7/7**: from(Advisor·위임 문면상 명시) · to(Planner) · task("절차 비례화 트랙 분해 초안 작성") · input(확정 사용자 결정 2건 + 유지 불변 5건 + 조사 대상 표면 9항) · output(본 파일 절대경로 1부) · done("초안에 반드시 포함할 것" 6항) · context(조사 대상 표면 목록 = 착수 전 정독 대상).
- **done 6/6 이진**: 6항 전부 "…이 초안에 존재한다"로 대조 가능(편성 판정 존재·Wave 설계 존재·원장 물리 형태 제안 존재·판별 물리 지점 제안 존재·개정 유형 표 존재·리스크/미결 목록 존재). 각 항에 판정 문장을 붙여 검증 가능성을 올렸다.
- **context 11/11 실재**: `.claude/CLAUDE.md` · `planning/specs/04-solution-design.md` · `planning/adapters/claude/solution-design-binding.md`(위임 문면의 `orchestration/adapters/claude/solution-design-binding.md`는 **미실재** — 실경로는 `planning/adapters/claude/`. 경로 오기를 실경로로 해석해 착수했다. §7 미검증 축 1) · `orchestration/adapters/claude/design_completeness.py` · `orchestration/specs/05-project-orchestration.md` · `uahf/framework/adapters/claude/orchestration-data/e2e/policy/{allocation.json,README.md}` · `discovery/adapters/claude/discovery-binding.md` · 메모리 2건 · `docs/session-handoff.md`.

**이탈 선언**: 위 context 경로 오기 1건을 실경로로 치환해 착수한 것(반환 대신 진행 — 오기가 결정적으로 복원 가능하고 위임 취지가 명백). 그 외 이탈 없음.

---

## §0. 근거 표 (좌표 — 이후 절이 인용)

| # | 사실 | 좌표 | 근거 |
|---|---|---|---|
| F-1 | manifest **부재** 시 차단 | `design_completeness.py:451` `"design-manifest absent — Solution Design에서 설계 산출 필요"` | 확인함 |
| F-2 | policy **부재** 시 차단 | `design_completeness.py:122-123` `"design policy 부재 — 필수 산출물 세트 판정 불가"` | 확인함 |
| F-3 | 체커가 읽는 policy·manifest 경로는 **workspace 기준 고정 상대경로**이며 config 키·env로 바꿀 수 없다 | `resolve_gate.py:107-109` `SD_DATA_REL=.claude/solution-design` / `pretooluse_design_guard.py:51-52` (동일 문면 별도 상수) | 확인함 |
| F-4 | 체커는 `projectionSelection.defaultRequiredSet` 만 읽는다 — 항목 수·id는 데이터 | `design_completeness.py:135-161` | 확인함 |
| F-5 | 체커 호출 지점은 정확히 2 + 벤더링 미러 1 (`resolve_gate.resolve_structural` · PreToolUse 훅) | `resolve_gate.py:104·537` / `pretooluse_design_guard.py:156·160` / `.claude/settings.json` PreToolUse | 확인함 |
| F-6 | 체커는 `user_decision_required` 해소 경로에서만 발화하고 escalation 해소 경로에는 없다 | `resolve_gate.py:751-752` → `resolve_structural` | 확인함 |
| F-7 | `gate_policy()`는 인자 0·리터럴 반환 — **데이터 파일을 읽지 않는다** | `contract_to_graph.py:430-445` | 확인함 |
| F-8 | 복잡도 분기 코드 0 — `compile`은 분기 없는 직선, `build_seed_graph`는 항상 단일 proposal 노드 | `contract_to_graph.py:479-505·419-424` | 확인함 |
| F-9 | seed 프롬프트가 가정하는 SD 입력 = `<root>/docs/solution-design.md` **하드코딩** | `contract_to_graph.py:332-334` | 확인함 |
| F-10 | CP2 실행은 policy·gate 무관 무조건 디스패치 — 우회 경로 부재 | `uahf/framework/loop/step-host/host.py:280` + `gates.py:93-95` 주석 | 확인함 |
| F-11 | CP2에서 데이터로 조절되는 것은 **모델 슬롯뿐**, 실행 여부 아님 | `host.py:326-332` (`cp2_model_resolver` > `cp2_model` > `step.model`) | 확인함 |
| F-12 | `allocation_file` 소비 슬롯은 실재하나 런처가 **생산·전달하지 않는다**(현행 런처 경로에서 allocation 항상 None) | `_orch_common.py:248-264` 소비 / `contract_to_graph.build_config:465-473` 7키에 부재 / `orchestrate_project.py:199` `build_orchestrator_k(run_dir, invoker)` 무전달 | 확인함 |
| F-13 | `userActorClass`는 **데이터로 치환 가능** — `"Advisor"`로 두면 Advisor가 구조 게이트를 해소한다. floor로 막혀 있지 않다 | `gates.py:230-241·258·120` | 확인함 |
| F-14 | 게이트 하한 클램프 = `effective_gate = max_gate(floor, policy.evaluate)`, 소비 1지점 | `gates.py:275-281` / `orchestrator.py:690` | 확인함 |
| F-15 | 컴파일러 기본 정책의 target은 `unitType`뿐이라 floor는 발화하지 않는다(`floor({"unitType":…}) == auto_continue`) | `gates.py:98-112`·`tests/test_gates.py:142` | 확인함 |
| F-16 | SD policy에 프로파일 키 부재 — 실재하는 분기는 (a) `skipRule` 이진 (b) `requirementClasses` 선언-조건부 (c) 프로젝트별 policy 사본 | `solution-design-data/policy/default-policy.yaml` 키 트리 · `solution-design-binding.md:284` "해당 프로젝트의 policy 사본에 데이터로 추가" | 확인함 |
| F-17 | `defaultRequiredSet` id = 13 (always 6 / touchpoint 6 / interface 1), `artifactOwnership` 13과 1:1 | 같은 yaml | 확인함 |
| F-18 | Discovery policy 단일 파일 — θ 5축 + `budget{total 40, soft 30, hard 40, perDimension, reentryTopUpMax 10}` | `discovery-data/policy/default-policy.yaml` | 확인함 |
| F-19 | 02 §3.13 "규모·리스크별 깊이 조정 파라미터는 Discovery Policy 데이터다" · §3.15 "정책 값 변경은 엔진 변경을 요구하지 않는다" | `discovery/specs/02-discovery.md` §3.13·§3.15 | 확인함 |
| F-20 | 차원 5개는 spec 고정, Contract Completeness는 "타협 불가·전건 충족" — **Policy로 축소 불가** | 02 §3.11·§3.7 | 확인함 |
| F-21 | Entry 결정 테이블 행 6(brownfield)의 `policy:{"ref":"default"}` — mode별 정책 분기 신호가 Discovery로 전달되지 않는다 | `entry/adapters/claude/entry-registry.json` 행 6 · `entry_resolve.py:243·249` | 확인함 |
| F-22 | 인터뷰 커버리지 10축은 **스킬 body 텍스트 하드코딩**(Policy 데이터 아님) + 스킬이 02 §3.13과의 충돌을 자기 신고 | `.claude/skills/discovery-interview/SKILL.md` 축 표·"미해소 — 02 §3.13 충돌" | 확인함 |
| F-23 | RevisionEvent·ArtifactRecord·GatePolicy 스키마는 `additionalProperties:false` 닫힌 스키마. RevisionEvent `basis`는 `{proposingStepRef,gateEventRef}` 문자열 2개 필수 | `revision_schema.json`·`artifact_record_schema.json`·`gate_policy_schema.json` | 확인함 |
| F-24 | 스킵 판정→manifest 변환 브리지 코드 0 (`resolve_m.py`는 skip 시 revision 0건으로 즉시 종료) | `orchestration-data/e2e/resolve_m.py:355-358` · 전수 grep(`whole-exclusion`·`assessing-judgment`·`skipRule`) | 확인함 |
| F-25 | 04 spec은 Projection 기본 세트의 구체 유형 목록·제외 규칙을 **Policy·비정본 부록 소관**으로 위임 | 04 §3.5·§3.8 SP-INV 9 | 확인함 |
| F-26 | 02-discovery 문서 상태 = **v1.1 Baseline**(자기 상태 라인에 Frozen 표기 없음) | 02 상태 라인 | 확인함 |

---

## §1. 편성 판정 — SD 스킵 브리지는 경량 레인의 전제가 아니다 (핸드오프 §A ★1 유의 사항의 반전)

### §1.1 판정

| # | 항목 | 판정 (이진) | 편성 |
|---|---|---|---|
| J-1 | SD 스킵 브리지(스킵↔구현 게이트 충돌)가 경량 레인의 **전제인가** | **아니다** | 선행 Wave 아님. 비례화 Wave에 **설계 판정 1건**(코드 작업 0)으로만 동반 |
| J-2 | SD manifest 배선 3건 중 **발견 3(workspace policy 시드 절차 누락)**이 경량 레인의 전제인가 | **그렇다** | **Wave 1에 필수 동반** |
| J-3 | 같은 3건 중 **발견 2(seed 단일파일 가정 `docs/solution-design.md`)**가 경량 레인과 맞물리는가 | **그렇다** | Wave 1에 동반(동시 해소 가능 — §1.4) |
| J-4 | 같은 3건 중 **발견 1(스키마 예시 path 모순)**이 경량 레인의 전제인가 | **아니다** | Wave 5(문서 정합)로 후행 |

### §1.2 J-1의 근거 — 경량 레인은 스킵 경로를 쓰지 않는다

경량 레인의 SD 축(사용자 결정 ①)은 "**통합 설계 문서 1종 프로파일**"이다. 이것은 04 §3.1-C의 **성숙 경로**(산출 있음)이며 **스킵 경로**(무산출)가 아니다.

- 구현 게이트가 차단하는 조건은 manifest **부재**다(F-1). 경량 프로파일은 `defaultRequiredSet`을 1종으로 줄인 policy로 manifest를 **산출한다** → 차단 조건 미성립.
- 스킵↔구현 게이트 충돌(F-24)은 `Skipped` 종단(무산출)에서만 발생한다. 경량 레인은 그 종단에 도달하지 않는다.
- 따라서 "스킵 브리지 없이는 경량 레인이 성립하지 않는다"는 명제는 **거짓**이다.

부수 효과(설계 지렛대): 경량 프로파일이 존재하면 스킵 경로는 **필요가 없어진다** — "단순 프로젝트이므로 산출 0"이 아니라 "단순 프로젝트이므로 통합 문서 1종"이 된다. 이는 메모리 `uaf-solution-design-skip-gap`이 기록한 사용자 입장("Solution Design은 무조건 있어야 한다")과 정합한다. 스킵 경로를 폐기하면 브리지 코드는 **0줄로 해소**된다. 이 폐기 여부는 사용자 게이트 대상이다(§6 카드 Q-4).

### §1.3 J-2의 근거 — 진짜 전제는 workspace policy 시드다

체커는 `<workspace>/.claude/solution-design/policy/default-policy.yaml` 을 고정 상대경로로 읽고, 그 경로는 config 키·env로 바꿀 수 없다(F-3). 경량 프로파일을 적용하는 유일한 물리 수단은 **그 경로에 경량 policy를 시드하는 것**이다. 그런데 SD 성숙 run이 policy를 workspace에 자동 시드하는 단계는 없다(메모리 `uaf-design-manifest-path-defect` 발견 3 — 본 초안이 F-3으로 재확인). 시드 절차가 없으면 경량 프로파일은 **적용될 자리가 없다**. 그러므로 발견 3은 경량 레인의 전제다.

이 제약은 동시에 **최소 침습 설계 경로**를 준다 — 경로가 고정이므로 프로파일 선택은 **그 자리에 어느 policy 파일을 놓는가**로 환원되고, 체커 코드·스키마·04 spec은 무촉이다(F-4·F-25). 04 §3.5·SP-INV 9가 "기본 세트의 구체 유형 목록은 Policy 소관"이라고 이미 위임했고, binding §7.2 (바)가 "프로젝트별 policy 사본에 데이터로 추가"라는 확장 패턴을 이미 정본 문면으로 승인했다(F-16).

### §1.4 J-3의 근거 — 통합 문서 1종의 id를 seed 가정과 정합시킨다

seed 프롬프트는 SD 입력을 `<root>/docs/solution-design.md` 로 하드코딩한다(F-9). 표준 레인(7~13종 개별 Projection)에서는 그 파일이 존재하지 않아 발견 2의 결함이 된다. **경량 프로파일의 통합 문서 1종을 id `solution-design`·본문 경로 `<workspace>/docs/solution-design.md` 로 정의하면 seed 가정과 정확히 일치**한다 → 경량 레인에서 발견 2는 발생하지 않는다. 표준 레인의 발견 2는 별도로 남으므로, Wave 1은 "경량 레인에서 접합부 왕복 통과"만 done으로 삼고 표준 레인 해소는 후속 트랙으로 분리한다(범위 팽창 방지).

---

## §2. 레인 판별의 물리 지점 제안

### §2.1 판별식 (결정적)

사용자 결정 ① = 접점 기준 + 사용자 override 양방향. 접점 = **Contract·게이트·정본 문서·스키마**.

```
lane(declaredTargets, override) =
  override != null                       -> override            (사유 원장 기록 필수)
  declaredTargets == null | 공집합       -> standard             (fail-closed)
  any(t in declaredTargets: touches(t))  -> standard
  else                                   -> lightweight
```

`touches(t)`는 경로 패턴 집합에 대한 순수 술어다. 패턴 집합은 **데이터**로 두고 코드에 넣지 않는다(Policy as Data). 초기 패턴 후보(확정은 Advisor·사용자 소관):

| 접점 클래스 | 패턴 후보 | 근거 |
|---|---|---|
| Contract | `**/project-contract/project-contract.v*.md` | contract-binding §4.2 경로 |
| 게이트 | `orchestration/framework/orchestrator/gates.py` · `**/gate_policy.json` · `orchestration/adapters/claude/{resolve_gate,contract_to_graph,design_completeness,pretooluse_design_guard}.py` | F-5·F-7·F-14 |
| 정본 문서 | `*/specs/*.md` · `ARCHITECTURE.md` · `*/ARCHITECTURE.md` · `.claude/AGENT.md` | 정본 소유 경계 |
| 스키마 | `**/*.schema.json` · `**/*.schema.md` · `**/*_schema.json` | F-23 |
| 정책 데이터 | `**/policy/*.yaml` · `**/policy/*.json` | Policy as Data 단일 소스 보호 |

### §2.2 판정 시점 2개 — 선언 시점(사전) + Write 시점(사후)

| 시점 | 주체 | 성격 | 미충족 시 |
|---|---|---|---|
| (i) 착수 전 | 신규 form-B 로더 `lane_resolve.py` (LLM 0·결정적·순수 판독·계산·방출까지만) | 선언된 대상 집합 → lane + 근거 + 사유 기록 요구 여부 | 선언 부재·패턴 매칭 불가 → **standard**(fail-closed) |
| (ii) Write 시점 | PreToolUse 훅(신규 또는 `pretooluse_design_guard` 확장) | 경량 레인 run이 접점 파일을 실제로 건드리면 **deny** | deny + 승급 지시 |

- (i)의 성격·경계는 `entry_resolve.py`·`solution_design_resolve.py` 선례와 동형이다(binding §7A.5: "LLM 0·결정적·오프라인 안전·순수 판독·계산해서 방출까지만"). 로더는 lane을 **적용**하지 않고 **계산**만 한다 — 적용(policy 시드·위임 발부)은 주 세션 form-A다.
- (ii)는 강제 지점이다. 「강제 없는 규율 신설 금지」를 (ii)로 충족한다. 훅 배선은 상대경로로 쓴다(`.claude/CLAUDE.md` 이진 원칙 절) 그리고 **실제 도구 호출로 차단을 확인**한다 — 단위 테스트만으로 배선 생존을 판정하지 않는다.
- (ii)의 알려진 취약: 핸드오프 §B-2 "PreToolUse 훅 상대경로 ↔ Bash 지속 CWD" — 훅이 스크립트를 못 찾으면 침묵 통과가 아니라 Write **차단**으로 나타난다. Wave 브리프 constraints에 "`cd`는 서브셸 한정" 명시.

### §2.3 fail-closed의 이진 표기

레인은 두 값만 갖는다: `standard` 또는 `lightweight`. 세 번째 값을 두지 않는다 — 판정에 필요한 선언이 없으면 `standard`로 귀결한다(안전측). 이는 allocation 정책의 `defaultSlot: sonnet`(안전측 귀결) 선례와 동형이다.

---

## §3. 경량 원장의 물리 형태 제안 (기존 백엔드·기존 스키마 재사용 · 신규 포맷 발명 0)

원장 0건 금지는 두 레인 공통이다. 경량 레인은 **원장을 줄이지 않고 조율 주체를 바꾼다**(엔진 → Advisor 직접 위임).

### §3.1 설계 층 원장 = 기존 SD 원장 그대로

- 위치: `solution-design-data/events/maturation-<run-id>/events.jsonl` (binding §3.2).
- 레코드 어휘: 기존 6종 그대로(`MaturationRunStarted`·`StateTransition`·`GatePresented`·`UserResponded`·`OutputRecorded`·`MaturationRunConcluded` — binding §4.3). **신규 레코드 종류 0**.
- 경량 프로파일 적용 사실은 `MaturationRunStarted`의 "사용한 policy 참조"와 provenance §8.1의 "Policy 참조" 필드가 이미 담는다 — **필드 신설 0**.
- form-A 수기 append 허용(`.claude/CLAUDE.md` 설계 층 원장 절).

### §3.2 구현 층 원장 = 05 §3.2·§3.6 스키마 재사용 + 수기 append

경량 레인은 엔진을 돌리지 않으므로 엔진이 자동 생성하는 원장이 없다. 그러나 **스키마는 이미 있다**. 새 포맷을 발명하지 않고 닫힌 스키마(F-23)를 그대로 채운다.

제안 위치: `orchestration-data/runs/<run-id>-lite/` (기존 `runs/` 트리 안·형제 배치 — 신규 루트 0)

| 파일 | 스키마 | 최소 필드 | 채우는 값(경량 레인) |
|---|---|---|---|
| `revisions.jsonl` | `revision_schema.json` (닫힘) | `revisionSeq`·`kind`·`payload`·`basis{proposingStepRef,gateEventRef}` | `kind=task_added`; `payload`=07 Task 전 필드(위임 8필드 포함); `proposingStepRef`=Planner/Advisor 분해 초안 파일 참조; `gateEventRef`=사용자·Advisor 게이트 기록 참조 |
| `artifacts.jsonl` | `artifact_record_schema.json` (닫힘) | `artifactId`·`version`·`approvalState` (+`location`·`producedBy`·`contentHash` 선택) | `approvalState`=`verified`(CP2 Pass)→`approved`(CP3)→`user_approved` |
| `events.jsonl` | (기존 run 이벤트 관례) | 게이트 요구·provenance·해소 3단 순서 | `verify_run.py` (a) 원장 위생 축이 그대로 검사 |

**스키마 개정 0으로 성립하는가 = 성립한다.** `basis`의 두 필드는 타입이 `string`이고 의미는 "참조"이므로 엔진 step ref가 아닌 브리프 파일 참조를 담아도 스키마 위반이 아니다(F-23). 단 05 §3.2 결정성 조건 ①("게이트 통과 이벤트가 append된 뒤에만 그 revision을 append")은 수기 경로에서도 지켜야 하며, 그 검사는 §3.3의 검증 스크립트가 담당한다.

### §3.3 경량 원장의 검증 = 기존 결정적 러너 재사용

`orchestration-data/e2e/verify_run.py` 는 이미 `events.jsonl`·`revisions.jsonl`·`artifacts.jsonl`·`graph.json` 을 순수 판독으로 검사하며 축 (a) 원장 위생(seq 단조·게이트 순서 required→provenance→resolved)·(b) revision 무결(중립 `validate_revision`/`fold` 재사용)·(e) 계수 정합을 이미 갖는다. 경량 run 디렉터리를 같은 러너에 먹여 **원장 0건·순서 위반·근거 결손을 결정적으로 검출**한다 — 새 검증기 신설 0.

**강제 지점**: 경량 레인 종결 조건에 `verify_run.py <run-dir>` 통과(findings 0)를 둔다. 이것이 "경량 레인에서도 원장 0건 금지"의 기계 강제다.

---

## §4. Wave 설계

원칙: 각 Wave 경계에서 **접합부 왕복 검증**(`docs/verification-checklist.md` §5.7)을 수행한다 — 단위 검증 통과가 접합부 정합을 뜻하지 않는다(오케스트레이션 트랙 교훈). 각 브리프의 done 축은 **정본 열거에서 도출**하고 좌표를 병기한다(§5.8 축 발명 금지).

### Wave 0 — 게이트 (작업 아님)

§6 미결정 카드 Q-1~Q-5 + §8.9 카드 Q-6·Q-7(총 7건)을 사용자에게 제시·확정. Q-1·Q-2·Q-3·Q-5·Q-6·Q-7은 Wave 1~4의 입력이므로 **미해소 시 하류 차단**이다(미해소는 하류를 막는다). Q-4만 비차단이다.

### Wave 1 — SD 경량 프로파일 (병렬 2)

의존: Wave 0(Q-1 확정).

#### W1-a · 경량 policy 프로파일 데이터 + workspace 시드 절차

```
from: Advisor          to: Worker
task: SD 경량 프로파일 policy 데이터 신설 + workspace 시드 절차 물리화(발견 3 해소)
input:
  - 정본: planning/specs/04-solution-design.md §3.2·§3.5·§3.8 SP-INV 9 (Policy 소관 위임 문면)
  - 바인딩: planning/adapters/claude/solution-design-binding.md §7.1·§7.2 (다)·§7.2 (바) 말미(프로젝트별 policy 사본 패턴)
  - 표준 policy: uahf/framework/adapters/claude/solution-design-data/policy/default-policy.yaml (키 트리 = 본 초안 F-16)
  - 체커 경로 계약: orchestration/adapters/claude/resolve_gate.py:107-109 · pretooluse_design_guard.py:51-52
  - 사용자 결정: 절차 두께 4축 ① (경량 = 통합 설계 문서 1종 프로파일) · Q-1 확정 문면
output:
  1) uahf/framework/adapters/claude/solution-design-data/policy/lightweight-policy.yaml (신규 1파일)
  2) planning/adapters/claude/solution-design-binding.md §7.2 (다) 하위에 경량 프로파일 값표 append + §9 이력 1행 append
  3) 시드 절차: solution-design-binding.md §7A.2 에 "workspace policy 시드" 절차 항 신설(form-A) — 표준/경량 어느 프로파일을 <workspace>/.claude/solution-design/policy/default-policy.yaml 에 놓는가
done:
  1) lightweight-policy.yaml 의 projectionSelection.defaultRequiredSet 항목 수 == 1 이고 그 id 가 Q-1 확정값과 일치한다
  2) 그 항목의 requirement == "always" 이며 requirementClasses 3종 정의가 표준과 동일 문면으로 존재한다
  3) artifactOwnership 이 위 1 id 와 1:1 대응한다(개수 1·id 일치)
  4) exclusionRule.silentOmission == 금지 · classExclusionOnNonDeclaration == 표면화 가 표준과 동일하게 존재한다
  5) design_completeness.py 를 lightweight-policy.yaml + 1종 produced 매니페스트에 실행해 exit 0 이다(실행 로그 첨부)
  6) 같은 체커를 1종 미산출 매니페스트에 실행해 비영 종료다(음성 대조 1건 — 검증기가 실제로 거부를 낼 수 있음을 증명)
  7) design_completeness.py · resolve_gate.py · pretooluse_design_guard.py · solution_design_resolve.py 의 diff hunk 가 0 이다(코드 무촉)
  8) planning/specs/04-solution-design.md 의 diff hunk 가 0 이다(spec 무촉)
  9) 시드 절차 항이 "표준/경량 선택 → 대상 경로 → 원장 기록(MaturationRunStarted policy 참조)" 3항을 명시한다
context:
  .claude/AGENT.md · .claude/CLAUDE.md · docs/delegation-protocol.md §2 · docs/verification-checklist.md §5.7·§5.8
  · planning/specs/04-solution-design.md · planning/adapters/claude/solution-design-binding.md
  · orchestration/adapters/claude/design_completeness.py · docs/spec-versioning-policy.md §3.2
constraints:
  - 신규 파일 1 + 기존 md 2절 append 만. python 파일 수정 0. spec 수정 0.
  - Policy as Data 단일 소스 — 값의 사본을 부록·다른 절에 두지 않는다(binding §7.2 머리 단일 소스 규율).
  - 정책 데이터 옆 병행 게이트 신설 금지(Entry 형태 B 트랙 교훈). 새 체커를 만들지 않고 기존 design_completeness 를 그대로 쓴다.
  - 중간 강도 표기 금지 — 필수(1) 또는 비요구(0) 이진으로만 쓴다(.claude/AGENT.md §Invariants).
동료 계약 블록:
  동료 Task = W1-b.
  교차 소비 지점 = ① 본 Task가 확정하는 defaultRequiredSet 의 단일 id 문자열을 W1-b 가 seed 가정 정합 판정의 입력으로 소비한다
                   ② 본 Task가 신설하는 파일명(lightweight-policy.yaml)을 W1-b 가 문서 참조로 인용한다
  이 두 값이 바뀌면 W1-b 에 [동료 영향] 으로 선언한다.
```

#### W1-b · 통합 문서 1종 ↔ seed 가정 접합부 정합(발견 2의 경량 레인 측 해소)

```
from: Advisor          to: Worker
task: 경량 프로파일 통합 문서 1종을 seed 프롬프트 입력 가정과 접합부 왕복으로 정합시킨다
input:
  - 접합부 생산 측: 경량 프로파일 산출물 1종의 본문 경로 규약(solution-design-binding.md §7A.2 배치 스코프)
  - 접합부 소비 측: orchestration/adapters/claude/contract_to_graph.py:332-334 _solution_design_path (= <root>/docs/solution-design.md 하드코딩) · :215-221 프롬프트 문면 · :377-380 delegation.input · :400 interfaceContract.consumes
  - 스키마: orchestration/adapters/claude/design-manifest.schema.md (path 해석 = 매니페스트 기준 상대)
  - 결함 기록: 메모리 uaf-design-manifest-path-defect 발견 2
output:
  1) design-manifest.schema.md 에 경량 프로파일 1종 항목의 path 실동작 예시 append(매니페스트 기준 상대)
  2) solution-design-binding.md §7A.2 에 경량 프로파일의 본문 경로 규약 1항 append
  3) 접합부 왕복 실측 기록(별도 산출물 아님 — 완료 보고 verify_basis 에 기재)
done:
  1) 경량 프로파일 매니페스트 1건을 실제로 작성해 design_completeness.py 에 먹여 exit 0 이며, 그 매니페스트의 path 가 실재 파일로 해석됨을 체커가 확인한다(접합부 왕복 — 예시가 아니라 실물)
  2) 같은 매니페스트의 path 를 스키마 구예시 형태(docs/<id>.md)로 바꾸면 비영 종료다(음성 대조 — 발견 2가 실재함을 증명)
  3) contract_to_graph.py 가 가정하는 절대경로 문자열과 (1)의 실재 본문 경로가 문자 단위로 일치함을 대조 출력으로 남긴다
  4) contract_to_graph.py 의 diff hunk 가 0 이다(경량 레인은 코드 개정 없이 정합함을 증명)
  5) 표준 레인의 발견 2 잔존을 미해소로 명시 기록한다(해소 주장 금지 — 후속 트랙 좌표 병기)
context: (W1-a 와 동일 + orchestration/adapters/claude/contract_to_graph.py · design-manifest.schema.md)
constraints:
  - md 2파일 append 만. python 수정 0.
  - 표준 레인 발견 2 해소를 이 Task 범위로 끌어오지 않는다(범위 팽창 금지).
동료 계약 블록:
  동료 Task = W1-a.
  교차 소비 지점 = ① W1-a 가 확정하는 단일 id 문자열을 본 Task가 path·매니페스트에 그대로 쓴다
                   ② W1-a 가 확정하는 시드 절차 항 번호를 본 Task가 교차 참조한다
  이 두 값이 바뀌면 W1-a 에 [동료 영향] 으로 선언한다.
```

### Wave 2 — 레인 판별 + 경량 원장 (병렬 2)

의존: Wave 0(Q-3 확정). Wave 1과 독립(SD policy 파일에 닿지 않음).

#### W2-a · 레인 판별 form-B 로더 + PreToolUse 강제

```
from: Advisor          to: Worker
task: 레인 판별 결정적 로더 신설 + Write 시점 강제 훅 배선
input:
  - 사용자 결정 ①(접점 기준 + override 양방향 + 이탈 사유 원장 기록) · Q-3 확정 배치
  - 선례 계약: planning/adapters/claude/solution-design-binding.md §7A.5(form-B 로더 성격 — LLM 0·결정적·계산·방출까지만) · entry/adapters/claude/entry_resolve.py(Policy as Data 단일 소스 문면 :52-54)
  - 강제 선례: orchestration/adapters/claude/pretooluse_design_guard.py 전문 · .claude/settings.json PreToolUse 블록
  - 접점 패턴 후보: 본 초안 §2.1 표(확정은 Advisor 소관)
output:
  1) <Q-3 확정 경로>/lane_resolve.py (신규)
  2) <Q-3 확정 경로>/lane-registry.json (신규 — 패턴은 데이터·코드 하드코딩 0)
  3) PreToolUse 훅 1건(신규 스크립트 또는 pretooluse_design_guard 확장 — Q-3 확정) + .claude/settings.json 배선
  4) 테스트 스위트 1건
done:
  1) lane_resolve 가 접점 파일 1건을 포함한 입력에 lane=="standard" 를 반환한다
  2) 접점 0 입력에 lane=="lightweight" 를 반환한다
  3) 선언 부재·빈 입력에 lane=="standard" 를 반환한다(fail-closed)
  4) override 지정 시 override 값을 반환하고 사유 기록 요구 플래그가 true 다
  5) override 지정 + 사유 부재 시 비영 종료다(음성 대조)
  6) 로더가 LLM·네트워크·서브에이전트를 호출하지 않는다(import 목록·grep 전수 근거 제시)
  7) 로더 연속 2회 실행 결과가 byte 동일하다(결정성)
  8) 패턴 문자열이 .py 에 0건이며 전부 lane-registry.json 에 있다(grep 전수 근거)
  9) 훅이 경량 레인 표기 하에 접점 파일 Write 를 **실제 도구 호출로** 차단함을 확인했다(단위 테스트가 아니라 라이브 차단 1건 — .claude/CLAUDE.md 훅 배선 절)
  10) 훅 자체 오류(stdin 파싱 실패·import 실패)가 fail-open 임을 4케이스로 확인했다(자기-DoS 방지 — 기존 가드 선례 동형)
  11) 훅 미배선·미발화 시의 침묵을 보고에 명시했다(침묵의 성공 해석 금지)
context: .claude/AGENT.md · .claude/CLAUDE.md(이진 원칙·관측 배선 2절) · docs/delegation-protocol.md §2
  · planning/adapters/claude/solution-design-binding.md §7A.5 · entry/adapters/claude/entry_resolve.py
  · orchestration/adapters/claude/pretooluse_design_guard.py · .claude/settings.json · docs/verification-checklist.md §5.8
constraints:
  - 훅 배선 경로는 상대경로($CLAUDE_PROJECT_DIR 금지 — 이 환경 실측). Bash 의 cd 는 서브셸 (cd … && cmd) 한정.
  - 로더는 lane 을 적용하지 않는다 — 계산·방출까지만. policy 시드·위임 발부·게이트 해소를 수행하면 경계 위반이다.
  - 게이트 하한(gates.py)·userActorClass 를 건드리지 않는다.
  - python 호출에 PYTHONIOENCODING=utf-8 명시.
동료 계약 블록:
  동료 Task = W2-b.
  교차 소비 지점 = ① 본 Task가 방출하는 lane 값 어휘 2종("standard"|"lightweight")과 사유 기록 필드명을 W2-b 가 원장 payload 에 기록한다
  이 어휘가 바뀌면 W2-b 에 [동료 영향] 으로 선언한다.
```

#### W2-b · 경량 원장 물리 형태 + 결정적 검증 재사용

```
from: Advisor          to: Worker
task: 경량 레인 구현 원장을 05 §3.2·§3.6 기존 스키마 재사용으로 확정하고 verify_run.py 로 검증 가능함을 실증
input:
  - 정본: orchestration/specs/05-project-orchestration.md §3.2(RevisionEvent·결정성 3조건)·§3.6(ArtifactRecord·approvalState 파생 뷰)·§4 PO-INV 2·5·7
  - 닫힌 스키마: orchestration/framework/orchestrator/{revision_schema.json,artifact_record_schema.json}
  - 검증기: uahf/framework/adapters/claude/orchestration-data/e2e/verify_run.py (축 a·b·e)
  - 불변: .claude/AGENT.md §Invariants(Run 조율 우회 금지의 "원장 없는" 조건절·설계 산출 원장 기록 의무)
  - 본 초안 §3.2 표(제안 — 확정은 Advisor)
output:
  1) orchestration/adapters/claude/project-orchestration-binding.md 에 "경량 레인 원장" 절 신설(form-A 수기 append 규약·최소 필드·배치 경로) + §9 이력 append
  2) 경량 원장 표본 1건(run 디렉터리 — ephemeral 등급)
  3) 테스트 또는 실행 로그
done:
  1) 표본 원장이 revision_schema.json · artifact_record_schema.json 검증을 통과한다(스키마 개정 0 — 두 스키마 파일 diff hunk 0)
  2) verify_run.py 를 표본 run 디렉터리에 실행해 findings 0 이며 exit 0 이다(실행 로그 첨부·EXIT= 보존)
  3) 게이트 순서(required→provenance→resolved)를 의도적으로 어긴 표본에 같은 러너를 실행하면 findings 비공집합이다(음성 대조)
  4) basis.proposingStepRef 가 위임 브리프 실파일 경로를, gateEventRef 가 게이트 기록 실참조를 담으며 둘 다 실재 경로로 해석된다(접합부 왕복)
  5) approvalState 가 verified→approved→user_approved 3전이를 게이트 기록에서 파생함을 표본으로 보인다(직접 기입 아님 — PO-INV 7)
  6) 신규 레코드 종류·신규 필드·신규 원장 루트가 0 이다(어휘·스키마·트리 재사용 근거 제시)
  7) verify_run.py · 중립 orchestrator 모듈의 diff hunk 가 0 이다
context: (W2-a 와 동일 상위 규약 + orchestration/specs/05-project-orchestration.md
  · orchestration/adapters/claude/project-orchestration-binding.md · orchestration-data/e2e/verify_run.py
  · docs/artifact-lifecycle-policy.md §3(산출물 등급))
constraints:
  - 스키마 파일 수정 0. 중립 코드 수정 0. 새 원장 포맷·새 루트 디렉터리 신설 0.
  - 파이프 금지 — cmd > <로그> 2>&1; echo "EXIT=$?" >> <로그> 로 흘리고 파일을 읽는다. Bash timeout 명시.
동료 계약 블록:
  동료 Task = W2-a.
  교차 소비 지점 = ① W2-a 가 확정하는 lane 어휘·사유 필드명을 본 Task가 원장 payload 문면에 쓴다
  이 어휘가 바뀌면 W2-a 에 [동료 영향] 으로 선언한다.
```

### Wave 3 — W3-a · CP2 차등 (§8.6에서 병렬 집합 2조로 확장 — 동료 = W3-b)

의존: Wave 0(Q-2 확정 — CP2 차등의 의미 확정이 선행) · Wave 2(원장 어휘 확정 후).
동료 계약 블록(§8.6): 동료 Task = W3-b. 교차 소비 지점 = **없음**(표면 무교차·값 무공유).

```
from: Advisor          to: Worker
task: 저위험 단위 CP2 차등을 기존 cp2ModelSlots 장치로 실현하고 런처 배선 결손 3지점을 잇는다
input:
  - 기존 장치: uahf/framework/adapters/claude/orchestration-data/e2e/policy/{allocation.json,README.md}(cp2ModelSlots 가법 필드·descriptor-aware CP2)
  - 소비 슬롯: orchestration-data/e2e/_orch_common.py:248-264 resolve_allocation
  - 배선 결손: contract_to_graph.build_config:465-473(7키에 allocation_file 부재) · orchestrate_project.py:555-571(CLI 표면) · orchestrate_project.py:199 build_orchestrator_k(run_dir, invoker) 무전달
  - 코드 하한: uahf/framework/loop/step-host/host.py:280(무조건 CP2 디스패치)·:326-332(모델 슬롯만 데이터) · orchestration/framework/orchestrator/gates.py:93-95·275-281
  - 정본: 05 §3.3(게이트 단조성 PO-INV 4)·§3.5(CP2 = 독립 정책 행)
  - 사용자 결정 ③(저위험 = 실행형 스크립트 AC 판정·cp2ModelSlots 기존 장치 활용) + Q-2 확정 문면
output:
  1) allocation_file 배선 3지점 개정(config 키 생산 + CLI 표면 + build_orchestrator_k 전달)
  2) 경량 레인용 allocation 정책 데이터 1건
  3) 테스트 + 실행 로그
done:
  1) config.json 에 allocation_file 키가 생산되고, 미지정 시 allocation==None 으로 현행 거동이 byte 동일하게 보존된다(무회귀 — 기존 baseline run 대조 1건)
  2) allocation_file 지정 시 저위험 capability class 의 CP2 모델 슬롯이 저티어로 해소된다(invoke 원장 실물로 관측 — logs/invoke-*.json)
  3) 고위험·미매칭 capability 의 CP2 슬롯이 defaultSlot(안전측)으로 귀결한다(음성 대조)
  4) CP2 디스패치 자체가 어떤 정책 값에서도 우회되지 않음을 확인한다(host.py:280 무분기 근거 + 저위험 경로에서도 cp2-pass ref 가 append 됨을 원장 실물로 확인) — SH-INV-4·PO-INV 4 무촉
  5) gates.py · host.py 의 게이트 하한 상수(_FLOOR_* · userActorClass 기본값)의 diff hunk 가 0 이다
  6) 스크립트 AC 를 CP2 판정 근거로 주는 경로가 브리프 층(done 축)에만 있고 CP2 실행 여부를 바꾸지 않음을 문면으로 명시한다
  7) allocation_file 상대경로 해석 기준(현행 = orchestration-data/e2e/ 기준)을 문서에 명시하거나 run_dir 기준으로 정합시킨다(접합부 — 어느 쪽이든 실측 대조 1건 첨부)
context: .claude/AGENT.md · .claude/CLAUDE.md · orchestration/specs/05-project-orchestration.md §3.3·§3.5·§4
  · orchestration-data/e2e/policy/README.md · orchestration/framework/orchestrator/{gates.py,allocation.py,model_selection_schema.json}
  · uahf/framework/loop/step-host/host.py · docs/verification-checklist.md §5.7·§5.8
constraints:
  - CP2 실행 자체를 제거·조건화하지 않는다(SH-INV-4 코드 하한 — 위반 시 즉시 중단·Advisor 보고).
  - gates.py floor 테이블·userActorClass 를 건드리지 않는다.
  - 스키마 additionalProperties:false 를 열지 않는다. 필요하면 가법 등재(model_selection_schema cp2ModelSlots 선례 동형).
  - 새 게이트·새 판정 주체 신설 0.
```

### Wave 4 — Discovery 경량 인터뷰 (단일)

의존: Wave 0(Q-5 확정).

```
from: Advisor          to: Worker
task: 성숙 brownfield 경로의 인터뷰 최소 문항을 Discovery Policy 데이터 + Entry 결정 테이블 참조로 실현
input:
  - 정본 위임 문면: discovery/specs/02-discovery.md §3.13("규모·리스크별 깊이 조정 파라미터는 Discovery Policy 데이터다")·§3.15("정책 값 변경은 엔진 변경을 요구하지 않는다")
  - 불가 경계: 02 §3.11(차원 5 고정)·§3.7(Contract Completeness 타협 불가·전건 충족)
  - 정책 데이터: uahf/framework/adapters/claude/discovery-data/policy/default-policy.yaml (θ 5축·budget total 40/soft 30/hard 40/perDimension/reentryTopUpMax 10)
  - 참조 배선: entry/adapters/claude/entry-registry.json 행 6(brownfield·policy.ref="default") · entry_resolve.py:243·249
  - 바인딩: discovery/adapters/claude/discovery-binding.md §7.1·§8
  - 제약 실측: .claude/skills/discovery-interview/SKILL.md — 커버리지 10축이 body 하드코딩이며 02 §3.13 과의 충돌을 자기 신고 상태
  - Q-5 확정 실값
output:
  1) discovery-data/policy/<경량 프로파일 파일명> (신규 — 예산·θ 재배분)
  2) entry-registry.json 행 6 의 policy.ref 를 경량 프로파일로 지정(데이터 1행)
  3) discovery-binding.md §8 에 프로파일 2종 값표 append + 이력 append
done:
  1) 경량 프로파일의 budget.total·soft·hard 가 Q-5 확정값과 일치하고, perDimension 합이 total 이하다(산술 대조)
  2) θ 5축이 **전부 존재**하며 차원 삭제가 0 이다(02 §3.11 무촉 — 차원 수 5 대조)
  3) Contract Completeness 필수 코어 필드 면제 문면이 0 이다(02 §3.7 축1 무촉 — grep 전수)
  4) entry_resolve.py 를 brownfield 입력으로 실행해 Discovery Request 의 policy 참조가 경량 프로파일을 가리킨다(실행 출력 첨부)
  5) entry_resolve.py · 02 spec 의 diff hunk 가 0 이다(데이터만으로 실현됨을 증명)
  6) 실제 문항 수를 좌우하는 커버리지 10축이 스킬 body 하드코딩이라 이 프로파일이 문항 수를 직접 줄이지 않음을 **미해소로 명시 기록**한다(해소 주장 금지 — 커버리지 강제 결함 트랙 좌표 병기)
  7) 침묵 생략 금지 규율(스킬 body)이 이 프로파일로 약화되지 않음을 문면 대조로 확인한다
context: discovery/specs/02-discovery.md §3.7·§3.11·§3.13·§3.14·§3.15 · discovery/adapters/claude/discovery-binding.md §7.1·§8
  · entry/adapters/claude/{entry_resolve.py,entry-registry.json} · .claude/skills/discovery-interview/SKILL.md
  · .claude/AGENT.md · docs/spec-versioning-policy.md §3.2·§4
constraints:
  - 02 spec 수정 0(Baseline 개정은 사용자 게이트 사안). 충돌 발견 시 수정하지 않고 Advisor 보고(Spec 임의 수정 금지).
  - 스킬 body 의 커버리지 축 목록·침묵 생략 금지 조항을 삭제·약화하지 않는다.
  - Policy as Data 단일 소스 — 값을 스킬 body·바인딩 본문에 사본으로 두지 않는다.
```

### Wave 5 — 통합·문서 정합·E2E 실증 (단일)

의존: Wave 1~4 전부.

```
from: Advisor          to: Worker
task: 레인 규율을 운용 문서에 정합시키고 경량 레인 1건을 E2E 로 실주행해 실증
output:
  1) .claude/CLAUDE.md 「구현 단계 = 2층」 라우팅 기본값 절 개정(§5 표 R-1 문안 초안 기반)
  2) design-manifest.schema.md 구예시 정정(발견 1 — J-4)
  3) docs/session-handoff.md §A·§B 갱신(제자리 교체)
  4) 경량 레인 실주행 1건의 원장 + 검증 리포트
done:
  1) CLAUDE.md 개정 문면이 "원장 0건 금지는 두 레인 공통"을 명시하고 AGENT.md §Invariants 를 재정의하지 않는다(§ 포인터만 — 재정의 0 대조)
  2) 개정 문면에 값 하드코딩이 0 이며 레인 패턴·프로파일 값은 데이터 포인터로만 가리킨다
  3) 경량 레인 실주행 1건이 (a) 레인 판별 로더 (b) 경량 policy 시드 (c) SD 통합 문서 1종 산출 (d) design_completeness exit 0 (e) 직접 위임 구현 1단위 (f) 경량 원장 append (g) verify_run.py findings 0 (h) CP2 Pass 원장 실물 — 8지점 전부를 통과한다
  4) 같은 주행에서 접점 파일 Write 시도가 훅으로 실제 차단된다(라이브 1건)
  5) 표준 레인 회귀 — 기존 baseline run 을 재검증해 무회귀다(verify_run.py findings 0 · 기존 테스트 스위트 전건 Pass·각 EXIT=0)
  6) 미해소 항목(표준 레인 발견 2·커버리지 축 Policy화·스킵 경로 존치 여부·K-1·K-5·K-8)을 전부 명시 열거한다(집계 숫자 금지 — 내용 기록)
constraints:
  - 정본(spec) 수정 0. 개정은 운용 문서·바인딩·데이터·스키마 문서에 한정.
  - E2E 는 소비 프로젝트 워킹트리를 파괴하지 않는다(삭제·스캐폴드 금지).
```

### Wave 6 — 후속(조건부·본 트랙 범위 밖)

Q-4가 "스킵 경로 폐기"로 확정되면 브리지 **작업 0**(브리지 코드 불필요·단 04 정본 개정은 유형 A 사안). "존치"로 확정되면 SD 스킵 브리지 구현을 별 트랙으로 연다.

### 의존 그래프

```
Wave 0 (게이트 — 카드 7건)
  ├─→ Wave 1 [W1-a ∥ W1-b]            (Q-1)
  ├─→ Wave 2 [W2-a ∥ W2-b]            (Q-3)   ← Wave 1 과 독립·동시 가능
  ├─→ Wave 3 [W3-a ∥ W3-b]            (Q-2·Q-6·Q-7 · Wave 2 후 — §8.6 확장)
  └─→ Wave 4 (경량 인터뷰)             (Q-5)   ← Wave 1~3 과 독립
Wave 1 ∧ 2 ∧ 3 ∧ 4 ─→ Wave 5 (통합·실증)
Q-4 ─→ Wave 6 (조건부)
```

병렬 집합 **3개**(Wave 1·2·3) 각 2조. 소유 경계 비중첩:
- Wave 1 = SD policy·SD binding·design-manifest 스키마 문서
- Wave 2 = 신규 로더·lane 레지스트리·settings.json·orchestration binding
- Wave 3 = W3-a: orchestration 코드(`contract_to_graph`·`orchestrate_project`·allocation 데이터) / W3-b: `AGENT.md`·`delegation-protocol.md`·`agents/` 3종

교차 0. 단 Wave 2 ↔ Wave 3 은 순차다(W3-b 가 W2-b 의 원장 배치 규칙을 상속 — §8.6).

---

## §5. 개정 유형 판정 표

기준 = `docs/spec-versioning-policy.md` §3.2 유형 (A) 계약 변경(버전 상승) / (B) 비계약 정합·격리 개정(이력 append + 상태 라인 갱신), §4 하위호환 (a) 추가=호환.

| # | 접촉 문서·자산 | 현재 상태 | 개정 유형 판정 | 버전 상승 | 근거 |
|---|---|---|---|---|---|
| R-1 | `.claude/CLAUDE.md` 「구현 단계 = 2층」 | 운용 배선 문서(정본 아님·버전 없음) | 문면 개정(유형 구분 대상 밖) | 해당 없음 | 라우팅 기본값 절의 재저술. 불변 자체는 AGENT.md 소유·재정의 0 |
| R-2 | `.claude/AGENT.md` §Invariants | 정본(공통 규약) | **개정 불필요** | 없음 | "Run 조율 우회 금지"의 금지 대상은 **"원장(RevisionEvent/ArtifactRecord·게이트 큐) 없는 임시 Worker 직접 디스패치"**다 — 조건절이 "원장 없는"이다. 경량 원장(§3.2)을 남기는 직접 위임은 이 금지에 걸리지 않는다. "엔진 경유가 기본이다"는 **기본값** 문면이며 책임 있는 자율 (b)(기본값+이탈 사유 기록)와 정합한다 |
| R-3 | `planning/specs/04-solution-design.md` | v1.3 Baseline → DC-1 Draft | **개정 불필요(무촉)** | 없음 | 경량 프로파일은 §3.1-C **성숙 경로 내부**의 Projection 세트 선택이다. 판정 산출의 이진 분기(성숙 필요/스킵)·출력 2경로 계약 무촉. §3.5·SP-INV 9가 "기본 세트의 구체 유형 목록·제외 규칙은 Policy·비정본 부록 소관"으로 이미 위임(F-25) |
| R-4 | `planning/adapters/claude/solution-design-binding.md` §7.2·§7A.2 | v1.4 Baseline | **(B) 비계약 정합** — 값표 append + 절차 항 append | 무상승(이력 append + 상태 라인 갱신) | 추가만·기존 값 문면 무변경 → §4 (a) 하위호환. 정본 계약 요소(단계 계약·State Machine·SP-INV) 무촉 |
| R-5 | `solution-design-data/policy/lightweight-policy.yaml`(신규) | 데이터 | **Policy 데이터** — 개정 유형 대상 아님 | 해당 없음 | Policy as Data(04 §3.2). SD policy 스키마 파일이 부재하므로(스윕 = `**/*schema*` 6건 열거·SD policy 스키마 없음) 스키마 개정 0 |
| R-6 | `orchestration/specs/05-project-orchestration.md` | v1.6 Baseline | **개정 불필요(무촉)** | 없음 | 경량 원장은 §3.2·§3.6 스키마·PO-INV 2·5·7을 **그대로 채운다**. 게이트 하한(PO-INV 4)·CP2 상시(SH-INV-4)를 약화하지 않는다. §3.1은 이미 "초기 구성은 데이터다 — 단순 프로젝트는 단일 Work Graph 직행"을 문면으로 소유 |
| R-7 | `orchestration/adapters/claude/project-orchestration-binding.md` | 현행 | **(B) 비계약 정합** — 경량 레인 원장 절 신설(무침습 삽입) | 무상승(이력 append) | 추가만. 기존 절 번호·교차 참조 보존(binding §7A/§7B/§7C 무침습 삽입 선례 동형) |
| R-8 | `revision_schema.json`·`artifact_record_schema.json` | 닫힌 스키마 | **개정 불필요(무촉)** | 없음 | `basis` 두 필드가 `string` 참조이므로 브리프·게이트 기록 참조를 담아도 스키마 유효(F-23) |
| R-9 | `contract_to_graph.py` `gate_policy()` | 코드 리터럴(F-7) | **코드 개정**(spec 계약 변경 아님) | 해당 없음(spec 아님) | Wave 3 범위. 개정하면 **하위호환 필수**: 미지정 시 현행 리터럴 폴백(allocation_file 선례 동형·기존 baseline run byte 동일). 새 병행 게이트 장치를 만들지 않고 기존 gate_policy 표면을 데이터화한다 |
| R-10 | `discovery/specs/02-discovery.md` | **v1.1 Baseline**(자기 상태 라인에 Frozen 표기 0 — F-26) | **개정 불필요(무촉)** | 없음 | §3.13·§3.15가 "깊이 조정 파라미터 = Policy 데이터"·"정책 값 변경은 엔진 변경 불요"를 이미 위임(F-19). 차원 수·Contract Completeness는 건드리지 않는다(F-20) |
| R-11 | `discovery/adapters/claude/discovery-binding.md` §8 | 현행 | **(B) 비계약 정합** — 프로파일 값표 append | 무상승(이력 append) | 추가만 |
| R-12 | `entry/adapters/claude/entry-registry.json` 행 6 | 데이터(Policy as Data 단일 소스) | **데이터 변경** | 해당 없음 | `policy.ref` 값 1개 교체. `entry_resolve.py` 무촉(F-21) |
| R-13 | `.claude/settings.json` PreToolUse | 환경 설정 | 배선 추가 | 해당 없음 | 기존 2훅에 형제 추가. **라이브 차단 실증 필수**(단위 검증으로 갈음 금지) |
| R-14 | `design-manifest.schema.md` | 스키마 문서 | **(B) 비계약 정합** — 실동작 예시 append + 구예시 정정 | 무상승 | 기존 문면 보존(append-only) + 경량 프로파일 예시 추가. 구예시 정정은 Wave 5 |
| R-15 | `docs/session-handoff.md` | 단일 live | 제자리 교체 | 해당 없음 | §C 갱신 규율 — 블록 누적 아님 |

**표의 요지**: 이 트랙은 **정본 spec 4종(04·05·02·03) 전부 무촉**으로 성립한다. 개정은 (i) Policy·레지스트리 데이터, (ii) Adapter 바인딩의 유형 (B) append, (iii) Adapter 코드(gate_policy 데이터화·allocation 배선), (iv) 운용 문서 문면에 한정된다. 정본 개정이 필요하다는 판정이 Wave 실행 중 나오면 **구현하지 않고 Advisor에게 보고**한다(Spec 임의 수정 금지). 유일한 예외 후보는 Q-4가 "스킵 경로 폐기"로 확정될 때이며 그것은 04 유형 (A)·버전 상승·사용자 승인 사안이다.

---

## §6. 리스크·미결정 목록 + 사용자 게이트 카드 초안

### §6.1 사용자 게이트 카드 (Wave 0 — 미해소 시 하류 차단)

**Q-1. 경량 프로파일의 통합 설계 문서 1종을 무엇으로 정의합니까?**
- (a) id `solution-design` · 경로 `<workspace>/docs/solution-design.md` — seed 프롬프트 하드코딩 가정과 일치해 발견 2가 경량 레인에서 발생하지 않는다(§1.4). 최소 침습.
- (b) 새 id(예: `unified-design`) · 별 경로 — 명명은 갈리지 않으나 seed 가정 불일치가 남아 `contract_to_graph.py` 개정을 유발한다.
- Planner 판정: (a)가 코드 개정 0. 확정 권위는 사용자.
- 종속: W1-a done 1·W1-b 전부.

**Q-2. "저위험 단위는 실행형 스크립트 AC 판정"은 다음 중 무엇을 뜻합니까?**
- 실측 제약: CP2 **실행 자체**는 policy·gate 무관 무조건 디스패치이며 우회 경로가 코드에 존재하지 않는다(F-10). 데이터로 조절되는 것은 모델 슬롯뿐이다(F-11).
- (a) CP2 LLM 디스패치를 유지하되 ① 판정 근거를 결정적 스크립트 AC로 좁히고(브리프 done 축) ② 모델을 저티어로 차등한다(`cp2ModelSlots`) — 코드 하한 무촉.
- (b) 저위험 단위는 CP2 LLM 디스패치를 아예 생략하고 스크립트 통과로 갈음한다 — **SH-INV-4·PO-INV 4 위반**이며 `host.py` 코드 하한 개정을 요구한다.
- Planner 판정: (b)는 유지 불변("검증 하한 유지")과 정면 충돌하므로 초안은 (a)를 전제로 Wave 3을 구성했다. (b)를 원하면 별 게이트가 필요하다.
- 종속: Wave 3 전부.

**Q-3. 레인 판별 로더·레지스트리의 물리 배치는 어디입니까?**
- 후보: (a) `orchestration/adapters/claude/`(게이트·강제 계열 동거) (b) `entry/adapters/claude/`(진입 판정 계열 동거) (c) `.claude/hooks/`(운용 훅 계열).
- 판단 요소: 레인은 "구현 라우팅"이므로 (a)가 계열 정합이나, 판정 시점이 착수 전이라 (b)도 성립한다.
- Planner 판정 없음 — 배치는 Architecture 결정이며 Advisor·사용자 소관.
- 종속: W2-a output 1·2·3.

**Q-4. SD 스킵 경로를 존치합니까, 폐기합니까?**
- 경량 프로파일이 도입되면 스킵 경로("단순하니 산출 0")의 역할은 경량 프로파일("단순하니 통합 문서 1종")이 대체한다(§1.2).
- (a) 폐기 — 스킵↔구현 게이트 충돌이 **코드 0줄로 해소**된다. 04 §3.1-C·§3.4 T2/T9·SP-INV 4가 스킵 종단을 소유하므로 폐기는 **정본 개정(유형 A·버전 상승·사용자 승인)**을 요구한다.
- (b) 존치 — 브리지 코드를 후속 트랙에서 구현한다(Wave 6). 정본 무촉.
- Planner 판정: 비례화 트랙 자체는 어느 쪽에서도 성립한다(§1.1 J-1). 이 카드는 비례화의 **차단 요인이 아니다**.

**Q-5. brownfield 경량 인터뷰의 예산 실값은 얼마입니까?**
- 현행 표준 = total 40 / soft 30 / hard 40 / perDimension(intent 10·requirement 10·constraint 6·risk 6·architecture 8) / reentryTopUpMax 10 (F-18).
- 실측 성공 사례 = auto-percenty brownfield 4문/40(핸드오프 §A).
- 제약: 차원 5개 삭제 불가·Contract Completeness 면제 불가(F-20). 예산·θ 재배분만 가능.
- Planner 판정 없음 — 임계값은 사용자 확정 사안이다(임계값 없이 케이스를 닫지 않는다).
- 종속: Wave 4 output 1·done 1.

### §6.2 리스크

| # | 리스크 | 성격 | 대응 |
|---|---|---|---|
| K-1 | **`userActorClass`가 데이터로 치환 가능**(F-13) — `"Advisor"`로 두면 Advisor가 사용자 구조 게이트를 해소한다. floor로 막혀 있지 않다 | 게이트 확정 권위 불변의 **기계 보호 결손**(본 트랙과 독립·본 초안 조사에서 신규 포착) | 본 트랙 constraints에 "건드리지 않는다" 명시 + **별 결함 항목으로 원장 등재**(강제 지점 = `gates.py` floor 테이블 또는 스키마 enum 고정. 도입 또는 미도입은 Advisor 이진 결정) |
| K-2 | 경량 레인이 "원장을 줄이는 것"으로 오해되어 원장 0건이 발생 | 불변 위반 | Wave 2 done 2·Wave 5 done 3(g)에 `verify_run.py` findings 0 을 기계 강제로 배치 |
| K-3 | 레인 판별 훅이 배선 실패로 침묵 통과 | 강제 소실(훅 실패는 조용하다) | W2-a done 9(라이브 차단 1건)·done 11(침묵 명시). 배선 이동 시 재실증 |
| K-4 | 경량 policy를 workspace에 시드하는 절차가 form-A 수기라 누락 가능 | 강제 없는 규율 | 누락 시 체커가 policy 부재로 **차단**한다(F-2) — 침묵 통과가 아니라 실패로 나타난다. 즉 이 지점은 이미 fail-closed |
| K-5 | 두 체커가 같은 경로 상수를 **중복 정의**한다(`resolve_gate.py:107-109` ↔ `pretooluse_design_guard.py:51-52`) | 접합부 drift 위험 | 본 트랙에서 통합하지 않는다(범위 밖). 미해소로 기록 — 한쪽만 바꾸면 게이트와 훅이 갈린다 |
| K-6 | 경량 인터뷰 프로파일이 실제 문항 수를 줄이지 못한다 — 문항 수를 좌우하는 커버리지 10축이 스킬 body 하드코딩이고 스킬 자신이 02 §3.13과의 충돌을 미해소로 신고 중(F-22) | 효과 미달 | Wave 4 done 6에 미해소 명시를 강제. 실효 확보는 커버리지 강제 결함 트랙 소관 |
| K-7 | `allocation_file` 상대경로 기준이 `orchestration-data/e2e/` 라 run_dir·workspace와 어긋난다(F-12) | 접합부 | Wave 3 done 7 |
| K-8 | 컴파일러 기본 정책의 target이 `unitType`뿐이어서 floor가 발화하지 않는다(F-15) — 하한 보호가 실질적으로 정책 entry에 의존 | 하한 실효 약화 | 본 트랙에서 gate_policy를 데이터화할 때 **하한 강화만** 가능함을 테스트로 고정(Wave 3 done 5). 근본 정합은 범위 밖·미해소 기록 |
| K-9 | 경량 레인 도입이 "간소화하고 넘어감"의 새 통로가 된다 | 책임 있는 자율 (a) 훼손 | 이탈·제외는 전부 사유 기록 + 게이트 일괄 표면화. 경량 레인은 **기본값**이며 침묵 skip 경로가 아니다 |
| K-10 | 비례화 트랙 자체가 6 Wave·브리프 6건으로 커져 비례화 취지에 반한다 | 자기모순 | Wave 1·2가 이 트랙의 **최소 성립 집합**이다(경량 SD + 레인 판별 + 경량 원장). Wave 3·4는 독립 분리 가능. Advisor가 Wave 1·2만 채택하고 나머지를 후속으로 미루는 선택지가 존재한다 |

### §6.3 미해소 목록 (내용 기록 — 집계 금지)

1. 표준 레인의 발견 2(seed 단일파일 가정 ↔ 개별 Projection 7~13종) — 경량 레인에서만 정합. 후속 트랙 좌표 = `contract_to_graph.py:332-334`.
2. 발견 1(스키마 예시 path `docs/<id>.md` ↔ 매니페스트 기준 상대 해석)의 표준 레인 예시 정정 — Wave 5 output 2로 편성했으나 Wave 5 미실행 시 미해소로 남는다.
3. 커버리지 10축의 Policy 데이터화(스킬 body 하드코딩) — K-6.
4. `userActorClass` 하한 미보호 — K-1(본 초안 신규 포착).
5. 경로 상수 중복 정의 — K-5.
6. floor 테이블 ↔ 컴파일러 target 어휘 불일치 — K-8.
7. SD 스킵 경로 존치 또는 폐기 — Q-4.

---

## §7. 이 초안의 검사 범위·미검증 축 (정직 명시)

- **미검증 축 1**: 위임 context의 `orchestration/adapters/claude/solution-design-binding.md` 는 미실재이며 실경로는 `planning/adapters/claude/solution-design-binding.md` 다. 오기로 판정해 실경로를 읽었다. 위임 문면 정정이 필요하다(결함 귀속 = 위임).
- **미검증 축 2**: 테스트 스위트를 **실행하지 않았다**(초안 단계·구현 금지). 모든 코드 주장은 정독 근거이며 실행 근거가 아니다.
- **미검증 축 3**: `solution-design-binding.md` 는 §0~§13 전문(533행)을 정독했다. 그 밖 planning 바인딩 자매 문서(`contract-binding.md`)는 § 포인터 인용만 확인하고 전문을 읽지 않았다.
- **미검증 축 4**: 소비 프로젝트(auto-percenty·yt-stt) 워킹트리를 열지 않았다. 경량 레인의 실제 비용 절감 폭은 실주행(Wave 5) 전까지 **추정**이다.
- **미검증 축 5**: `uahf/specs/` 00~13 전문을 읽지 않았다. R-2·R-6의 하한 판정은 05·AGENT.md·`gates.py`·`host.py` 문면 근거이며 `uahf/specs/03-loop.md`·`06-verifier.md` 원문 대조는 미수행.
- **미검증 축 6**(증보): `.claude/agents/verifier.md`·`planner.md` 전문을 축자 대조하지 않았다 — 삽입 지점("## 출력 (Output)" 절)은 `worker.md` 전문 정독 + 두 파일의 행수 실측으로 확인했다. W3-b done 6이 실행 층에서 3자 축자 정합을 검사한다.
- **성능 주장 부재**: "경량 레인이 N% 빠르다"·"컨텍스트 N% 절감"류 수치를 이 초안은 제시하지 않는다 — 측정 없이 임계를 발명하지 않는다. 축 ⑤의 절감 폭도 Pass 경로 실주행 전까지 **추정**이다.

---

## §8. 증보 — 추가 축 ⑤ 보고-파일 역전 · ⑥ 보고 상한 수치화 (Advisor 범위 추가 2026-07-26)

기존 4축·요구사항은 무변이며 본 절이 2축을 편입한다. 추가 조사 표면 정독: `.claude/agents/worker.md`(65행 전문) · `docs/delegation-protocol.md` §2.2·§2.3·§2.7·§3.2 · `.claude/AGENT.md` §Communication Rules·§Invariants.
`uaf-verified:` 추가 스윕 범위 = 위 4파일 + `.claude/agents/` 4파일 행수 실측(advisor 31·planner 53·verifier 94·worker 65). `verifier.md`·`planner.md`는 "출력" 절 구조가 `worker.md`와 동형임을 행수·헤딩 수준에서 확인했고 전문 축자 대조는 미수행(§7 미검증 축 6).

### §8.1 근거 표 (증보)

| # | 사실 | 좌표 | 근거 |
|---|---|---|---|
| F-27 | 현행 회수 채널의 물리 수명 = 세션. "서브에이전트 최종 응답은 세션 컨텍스트에만 존재한다" | `docs/delegation-protocol.md` §3.2 | 확인함 |
| F-28 | 원장 승격 대상은 **다음 사이클이 소비할 것으로 한정**되며 산출물 원문 덤프가 아니다 | `.claude/AGENT.md` §Invariants 위임 산출 유실 금지 부수 규칙 3 · delegation-protocol §2.7 | 확인함 |
| F-29 | 승격 위치 규칙이 이미 2분기로 존재 — "소비 프로젝트 작업이면 그 프로젝트 트리에, 하네스 자체 작업이면 해당 트랙 문서 옆에" | delegation-protocol §2.7 | 확인함 |
| F-30 | 승격분 수명 등급 = `evidence`, 정본 = `docs/artifact-lifecycle-policy.md` §2·§3·§5 | delegation-protocol §2.7 | 확인함 |
| F-31 | Artifact Registry는 "완료 보고와 게이트 이벤트에서 파생되는 **인덱스**이며 별도의 진리원천이 아니다" | 05 §3.6 | 확인함 |
| F-32 | CP3의 정독 대상은 **산출물**이다 — "산출물을 정독해 독립 검증한 뒤 최종 승인한다". 보고 전문 정독은 요구가 아니다 | `.claude/AGENT.md` §Verification & Gate CP3 | 확인함 |
| F-33 | `failures`·`open_questions`는 "없음까지 명시"가 불변이며 빈칸은 은폐로 간주된다 | `.claude/AGENT.md` §Communication Rules · delegation-protocol §2.2 | 확인함 |
| F-34 | 현행 보고 상한 문면은 정성(수치 0) — "결론·근거·경로 위주로 압축하고 산출물 원문·파일 전량 덤프를 지양한다" | `.claude/AGENT.md` §Communication Rules 보고 상한 | 확인함 |
| F-35 | §3.2 반려 장치가 이미 실재 — 점검 블록 부재·이탈 선언 블록 부재 시 "수리하지 않고 반려·재보고를 요구한다" | delegation-protocol §3.2 | 확인함 |
| F-36 | 반려 장치의 자동 차단 미도입 사유가 이미 기록됨 — "위임·보고는 도구 호출이 아니어서 도구 호출 차단 장치가 개입할 표면이 없다" | delegation-protocol §2.4 강제 지점·§2.5 동형 | 확인함 |
| F-37 | 역할 정의 3종의 삽입 지점 = 각 파일 "## 출력 (Output)" 절. `worker.md`는 완료·실패 보고 5필드를 그 절에 열거한다 | `.claude/agents/worker.md` 출력 절 | 확인함 |
| F-38 | 엔진 경로는 이미 파일 원장이다 — 단위 실행의 request/response가 `runs/<run-id>/logs/invoke-*.json`에 남는다 | 핸드오프 §A(invoke 원장 16파일·`timeout` 필드 가법) · `/uaf-implement` 명령 §2 run 관측 파일 | 확인함 |

### §8.2 핵심 판정 — 보고 파일은 원장의 일부가 아니라 원장이 가리키는 산출물이다

| # | 질문 | 판정 (이진) | 근거 |
|---|---|---|---|
| J-5 | 보고 전문 파일이 **제2 진리원천 신설**인가 | **아니다** | 보고는 현행에서도 진리원천이었다(§2.7이 그것을 승격 대상으로 삼는다). 변경되는 것은 보고의 **물리 수명·위치**(세션 → 파일)뿐이고 지위는 불변이다(F-27). 원장은 05 §3.6대로 그 파일을 가리키는 **인덱스**로 남는다(F-31) |
| J-6 | 보고 파일이 §3(경량 원장)과 **같은 백엔드를 공유**할 수 있는가 | **그렇다** | 배치 = 원장 run 디렉터리 하위 `reports/`. 보고 파일은 `ArtifactRecord.location`이 지시하는 artifact 1건이 된다(05 §3.6 `location`·`contentHash`). **신규 트리·신규 스키마·신규 레코드 종류 0** |
| J-7 | 보고 파일 도입으로 §2.7 **원장 승격이 불필요해지는가** | **아니다** | 두 층은 수명·목적이 다르다 — 보고 전문 = `evidence` 등급(아카이브·삭제 대상·F-30), 승격분 = "다음 사이클이 소비할 것"의 압축(F-28). 승격을 폐지하면 evidence 아카이브 시 미결이 함께 사라진다. **§2.7 존치** |
| J-8 | 컨텍스트 절감이 **실제로 실현되는가** | **조건부 아님 — 두 경로로 갈린다(이진)** | Pass 경로: 실현된다. CP3의 정독 대상은 산출물이고 보고 전문 정독은 요구가 아니다(F-32). Fail·반려 경로: 실현되지 않는다 — 결함 귀속 판정(verification-checklist §5.6)에 전문이 필요해 Advisor가 파일을 연다. 즉 절감은 **Pass 경로 한정**이며 이를 과대 주장하지 않는다 |
| J-9 | 이 개정의 대상 층은 어디인가 | **Advisor 직접 위임 층(서브에이전트 회수)에 한정** | 엔진 경로의 단위 실행은 이미 파일 원장이다(F-38) → 엔진 층은 이미 충족이며 개정 대상이 아니다. 개정 표면 = delegation-protocol **§3(Adapter 바인딩)** + §2.2·§2.3 형식 + 역할 정의 3종 |
| J-10 | 상한 초과 반려에 **신규 차단 장치**가 필요한가 | **아니다** | §3.2 반려 장치를 3번째 항으로 확장한다(F-35). 자동 차단 미도입 사유는 기존 기록을 승계한다(F-36) — 「강제 없는 규율 신설 금지」의 강제 지점 명시 요건 충족 |
| J-11 | 상한 판정이 **결정적**인가 | **그렇다** | 최종 응답의 문자 수·줄 수는 회수 시점에 세어 참·거짓이 갈린다. 점검 블록 부재 반려(존재/부재 이진)와 동급의 결정적 판정이다 |

### §8.3 최종 응답 형식 제안 (축 ⑤ — 파일 먼저·포인터 회수)

수임 Agent는 (1) 보고 **전문을 파일에 먼저 쓰고** (2) 최종 응답을 아래로 한정한다.

```
[착수 전 점검] 필수 필드 7/7 존재 · done N/N 이진 판정 가능 · context M/M 실재
[이탈 선언] (병렬 집합만) 없음 | <목록>
[판정] 완료 | 실패                                   ← 이진 1줄
[요약] 3~5줄 (결론·근거 종류·산출물 개수)
[보고 파일] <절대경로>                                ← 전문 위치
[failures] 없음 | N건 → 보고 파일 <절 지시>
[open_questions] 없음 | N건 → 보고 파일 <절 지시>
```

- `failures`·`open_questions`의 **존재·부재는 최종 응답에 이진으로 남기고 내용은 파일**에 둔다 — "없음까지 명시" 불변(F-33)을 최종 응답 층에서 충족하면서 전문을 컨텍스트에서 뺀다.
- `artifacts`·`self_check`·`verify_basis`는 전문 파일에만 둔다(AGENT.md §Communication Rules 5필드는 **보고**의 필드이며 보고의 물리 위치를 규정하지 않는다 — 재정의 0).
- 보고 파일 위치 규칙은 §2.7 승격 위치 2분기를 그대로 승계한다(F-29): 원장 run이 있으면 `<run-dir>/reports/<unit>-<role>-<attempt>.md`, 하네스 자체 작업이면 해당 트랙 문서 옆. **신규 위치 규칙 발명 0**.

### §8.4 수치 상한 제안 (축 ⑥) — 확정은 사용자 게이트 Q-6

| 항목 | 제안값 | 근거 |
|---|---|---|
| 최종 응답 문자 수 상한 | **5,000자** | 실측 앵커 = `/uahf-status` 형태 B 로더가 15KB 정독을 4,946B 표적 출력으로 대체(핸드오프 §A·커밋 a4f0c2f). 그 실측 크기를 상한 앵커로 승계한다 |
| 최종 응답 줄 수 상한 | **40줄** | §8.3 형식 합산(점검 1 + 이탈 최대 5 + 판정 1 + 요약 5 + 경로 1 + failures/open_questions 2 ≈ 15줄)의 2배 여유 |
| 판정식 | 두 상한을 **AND**로 충족 | 줄 수만 세면 긴 줄로 우회되고 문자 수만 세면 형식 붕괴를 못 막는다 |
| 보고 파일 경로 | **1건 필수** | 경로 부재 = 전문 소실 = 위임 산출 유실 금지 위반 |

**임계값 없이 케이스를 닫지 않는다** — 위 수치는 Planner 제안이며 확정 권위는 사용자다. 미확정 상태로 Wave를 착수하면 상한 없는 검증이 되어 관성 통과한다.

### §8.5 정본 소유 경계 — 두 옵션 (사용자 지시와 재정의 0의 충돌 표면화)

사용자 지시는 "`.claude/AGENT.md` §Communication Rules 보고 상한을 수치 상한으로 구체화"다. 그런데 수치를 정본에 두는 것은 **선택 요소의 필수화**이며 `docs/spec-versioning-policy.md` §4 (b) 비호환 변경에 해당한다(전 dependents 영향 판정 + 사용자 승인 필수). dependents = 역할 정의 4종 + delegation-protocol. 두 옵션을 그대로 올린다.

| 옵션 | 정본 개정 | 절차 비용 | 정합성 |
|---|---|---|---|
| **A** — AGENT.md §Communication Rules에 수치 등재(지시 문면 그대로) | AGENT.md 개정 1건(§4 (b) 비호환) | dependents 5종 영향 판정 + 사용자 승인 | 지시 문면과 일치. 단 값이 정본에 하드코딩되어 조정 시 매번 정본 개정 |
| **B** — AGENT.md 무촉. 수치는 delegation-protocol §2.2·§2.3(운용 지침)과 역할 정의 3종에만 등재 | 0 | 유형 (B) append만 | delegation-protocol §0 "정본을 재정의하지 않고 그 계약을 **채우는 법**만 정의한다"에 정합. Policy as Data 취지(값은 정본 밖)와도 정합 |

Planner 판정: **B가 재정의 0·값 하드코딩 금지 불변과 정합**하다. 다만 지시 문면은 A를 가리키므로 임의 해석하지 않고 카드로 올린다(Q-7). 확정 권위는 사용자다.

### §8.6 Wave 편성 — 기존 Wave 3을 병렬 집합 2조로 확장

- ⑤⑥은 **두 레인 공통**이며 경량 레인에 종속되지 않는다. 그러나 보고 파일 배치가 §3.2 경량 원장 run 디렉터리 규칙을 **상속**하므로 W2-b 이후다.
- ⑤⑥을 Wave 2의 3번째 조로 붙이지 않는다 — W2-b와 배치 규칙을 동시에 정하면 소유 경계가 겹친다.
- 기존 Wave 3(CP2 차등)과는 표면 교차가 0이다(Wave 3 = orchestration 코드·allocation 데이터 / ⑤⑥ = AGENT.md·delegation-protocol·agents 3종). 따라서 **Wave 3을 2조 병렬 집합으로 확장**한다.

```
Wave 3 [W3-a ∥ W3-b]   의존 = Wave 0(Q-2·Q-6·Q-7) ∧ Wave 2
  W3-a = 기존 Wave 3 브리프(CP2 차등) — 문면 무변, 동료 계약 블록만 추가
  W3-b = 보고-파일 역전 + 보고 상한 수치화 (신규 브리프 — §8.7)
```

W3-a의 동료 계약 블록(추가분): 동료 Task = W3-b. 교차 소비 지점 = **없음**(표면 무교차·값 무공유). 이 판정 자체를 블록에 명시한다(delegation-protocol §2.5 "없으면 없음 명시").

### §8.7 W3-b 브리프 초안

```
from: Advisor          to: Worker
task: 보고-파일 역전 규약 개정(축 ⑤) + 보고 상한 수치화·초과 반려 배선(축 ⑥)
input:
  - 정본: .claude/AGENT.md §Communication Rules(보고 5필드·보고 상한)·§Invariants(위임 산출 유실 금지·강제 없는 규율 신설 금지)·§Verification & Gate(CP3 정독 대상 = 산출물)
  - 운용 지침: docs/delegation-protocol.md §2.2(완료 보고 5필드)·§2.3(실패 보고 5필드)·§2.7(원장 승격·위치 2분기·수명 등급)·§3.2(회수·반려 장치)·§2.4·§2.5(강제 지점·자동 차단 미도입 사유 문면)
  - 역할 정의 삽입 지점: .claude/agents/{worker,verifier,planner}.md 의 "## 출력 (Output)" 절
  - 배치 규칙 상속원: W2-b 가 확정한 경량 레인 원장 run 디렉터리 규칙 + 05 §3.6 ArtifactRecord(location·contentHash)
  - 수명 등급: docs/artifact-lifecycle-policy.md §2·§3·§5
  - 확정 입력: Q-6(수치 실값) · Q-7(정본 소유 옵션 A 또는 B)
  - 본 초안 §8.2 판정 7건(J-5~J-11) · §8.3 형식 · §8.4 수치 제안
output:
  1) docs/delegation-protocol.md — §2.2·§2.3 에 "보고 전문 파일 우선 기록 + 최종 응답 한정 형식" 항 append · §3.2 에 "상한 초과 보고 반려" 항 append · §2.7 에 보고 전문 파일과 승격분의 층위 구분 1항 append
  2) .claude/agents/{worker,verifier,planner}.md — 각 "출력" 절에 최종 응답 상한·보고 파일 경로 필수 문면 append (3파일)
  3) (Q-7 == A 인 경우에만) .claude/AGENT.md §Communication Rules 보고 상한 수치화
  4) 회귀 대조 기록
done:
  1) delegation-protocol §2.2·§2.3 에 보고 전문 파일 위치 규칙이 존재하고, 그 규칙이 §2.7 위치 2분기 문면을 인용하며 새 위치 규칙을 발명하지 않는다(문면 대조)
  2) 최종 응답 한정 형식이 §8.3 의 7블록을 전부 열거하고, failures·open_questions 의 "없음까지 명시"가 최종 응답 층에서 충족됨을 문면으로 확인한다(AGENT.md §Communication Rules 무촉)
  3) §3.2 반려 항이 3개(점검 블록 부재 · 이탈 선언 블록 부재 · 상한 초과)이며 각 항의 판정이 이진 술어로 쓰여 있다
  4) 상한 초과 반려 항에 강제 지점이 명시되고, 자동 차단 미도입 사유가 §2.4·§2.5 의 기존 사유를 승계 인용한다(신규 차단 장치 발명 0 — 새 스크립트·훅 신설 파일 수 0)
  5) 수치 상한이 Q-6 확정값과 일치하며 문자 수·줄 수 두 상한이 AND 로 결합된다(문면 대조)
  6) 역할 정의 3파일 각각의 "출력" 절에 상한 문면이 존재하고, 3파일의 문면이 서로 갈리지 않는다(3자 축자 대조 — L-06 전 지점 전수 갱신)
  7) Q-7 == B 이면 .claude/AGENT.md 의 diff hunk 가 0 이다. Q-7 == A 이면 AGENT.md 개정 1건 + dependents 5종(역할 정의 4 + delegation-protocol) 영향 판정 기록이 존재한다
  8) 개정 전후로 §2.7 원장 승격 절차가 존치됨을 확인한다(삭제·약화 0 — J-7)
  9) 실측 회귀 1건 — 본 개정 문면대로 작성한 보고 표본 1건이 (a) 문자 수·줄 수 두 상한 이내 (b) 보고 파일 경로 1건 존재 (c) 전문 파일에 5필드 전건 존재 를 충족한다
  10) 음성 대조 1건 — 상한을 초과한 보고 표본이 반려 판정을 받음을 §3.2 문면에 대조해 보인다(반려가 실제로 발화 가능함을 증명)
  11) 컨텍스트 절감이 Pass 경로 한정임을 문면에 명시한다(Fail·반려 시 Advisor 가 전문을 연다 — 과대 주장 금지·J-8)
context: .claude/AGENT.md · .claude/CLAUDE.md · docs/delegation-protocol.md 전문 · .claude/agents/{worker,verifier,planner,advisor}.md
  · docs/verification-checklist.md §5.6·§5.7·§5.8 · docs/artifact-lifecycle-policy.md §2·§3·§5
  · docs/spec-versioning-policy.md §3.2·§4 · orchestration/specs/05-project-orchestration.md §3.6
constraints:
  - 신규 차단 스크립트·훅 신설 0(기존 §3.2 반려 장치 재사용 — 사용자 지시 명시).
  - 제2 진리원천 신설 0 — 보고 파일은 원장이 가리키는 artifact 이며 새 원장 트리·새 레코드 종류·새 스키마를 만들지 않는다.
  - AGENT.md 보고 5필드·"없음까지 명시" 불변을 삭제·약화하지 않는다. 위치만 이동한다.
  - §2.7 원장 승격을 폐지·축소하지 않는다.
  - Q-6·Q-7 미확정 시 착수하지 않고 반환한다(임계값·소유 경계 미확정 = 필수 입력 누락).
  - 중간 강도 표기 금지 — 필수(1) 또는 비요구(0) 이진으로만 쓴다.
동료 계약 블록:
  동료 Task = W3-a(CP2 차등).
  교차 소비 지점 = 없음 — 표면 무교차(W3-a = orchestration 코드·allocation 데이터 / 본 Task = AGENT.md·delegation-protocol·agents 3종), 값 무공유.
  단 W3-a 가 산출하는 CP2 판정 근거 문면(스크립트 AC)이 보고 형식을 요구하게 되면 [동료 영향] 으로 선언한다.
```

### §8.8 개정 유형 판정 표 (증보 — R-16~R-20)

| # | 접촉 문서·자산 | 현재 상태 | 개정 유형 판정 | 버전 상승 | 근거 |
|---|---|---|---|---|---|
| R-16 | `.claude/AGENT.md` §Communication Rules 보고 상한 | 정본(공통 규약) | **Q-7 종속** — 옵션 A = 선택 요소의 필수화 → §4 **(b) 비호환**(dependents 5종 영향 판정 + 사용자 승인 필수) / 옵션 B = **개정 불필요** | 옵션 A만 해당 | F-34(현행 정성 문면)·spec-versioning-policy §4 (b) |
| R-17 | `.claude/AGENT.md` §Invariants 위임 산출 유실 금지 | 정본 | **개정 불필요** | 없음 | 보고 파일 우선 기록은 이 불변을 **강화**한다(회수 채널 소멸 위험 제거 — F-27). 승격 존치로 부수 규칙 3건 무촉(J-7) |
| R-18 | `docs/delegation-protocol.md` §2.2·§2.3·§2.7·§3.2 | 운용 지침(v — 상태 라인 없음) | **(B) 비계약 정합** — 항 append 4건 | 무상승 | 정본(02·07·AGENT.md) 재정의 0. §0 "그 계약을 채우는 법만 정의한다"에 정합 |
| R-19 | `.claude/agents/{worker,verifier,planner}.md` | 역할 정의(바인딩) | **(B) 비계약 정합** — "출력" 절 문면 append 3건 | 무상승 | 추가만. AGENT.md 재정의 0. **3파일 축자 정합 필수**(L-06) |
| R-20 | 보고 전문 파일(신규 산출물 유형) | 신규 artifact | **개정 유형 대상 아님** — 스키마·원장 무촉 | 해당 없음 | J-5·J-6. `ArtifactRecord.location` 이 가리키는 artifact 1건. 수명 등급 = `evidence`(F-30) |

**증보 후 요지 갱신**: 옵션 B 확정 시 이 트랙은 여전히 **정본 spec 4종 + AGENT.md 전부 무촉**으로 성립한다. 옵션 A 확정 시 AGENT.md 비호환 개정 1건이 추가되고 사용자 승인이 필수가 된다.

### §8.9 카드 증보 (Q-6·Q-7)

**Q-6. 최종 응답 상한 실값을 확정해 주십시오.**
- Planner 제안: 문자 5,000자 **AND** 40줄, 보고 파일 경로 1건 필수(§8.4).
- 근거 앵커: `/uahf-status` 형태 B 실측 4,946B 표적 출력.
- 미확정 시 결과: 상한 없는 검증은 관성 통과한다 → W3-b 착수 불가(constraints에 반환 규정).
- 종속: W3-b done 5·9.

**Q-7. 수치 상한을 어디가 소유합니까 — AGENT.md(옵션 A) 또는 운용 지침·역할 정의(옵션 B)?**
- 옵션 A = 사용자 지시 문면 그대로. 절차 비용 = AGENT.md 비호환 개정 + dependents 5종 영향 판정 + 사용자 승인.
- 옵션 B = AGENT.md 무촉·유형 (B) append만. 값 하드코딩을 정본 밖에 두어 Policy as Data 취지와 정합.
- Planner 판정: B가 재정의 0 불변과 정합. 단 지시 문면은 A를 가리키므로 임의 해석하지 않고 올린다.
- 종속: W3-b output 3·done 7.

### §8.10 리스크 증보

| # | 리스크 | 성격 | 대응 |
|---|---|---|---|
| K-11 | 보고 전문이 파일로 가면서 **Advisor가 읽지 않아 검증이 얕아진다** | 검증 하한 훼손 | CP3의 정독 대상은 원래 **산출물**이며 보고 전문이 아니다(F-32). 그러나 결함 귀속 판정(§5.6)은 위임 문면·보고 전문을 요구한다 → W3-b done 11에 "Fail·반려 시 전문을 연다"를 문면 강제 |
| K-12 | 보고 파일이 원장과 별개로 흩어져 **제2 진리원천화**된다 | 불변 위반 | 배치를 원장 run 디렉터리 하위로 고정(J-6) + `ArtifactRecord.location` 으로만 지시. 하네스 자체 작업은 §2.7 위치 2분기를 승계(F-29) |
| K-13 | 상한이 **요약 품질 저하**를 유발해 이진 판정·미결 존재 여부가 최종 응답에서 누락된다 | 은폐로 귀결 | 형식 7블록 중 `[판정]`·`[failures]`·`[open_questions]` 를 **필수 블록**으로 두고 부재 시 §3.2 반려(점검 블록 부재와 동급). 즉 상한은 요약 길이를 줄이되 **필수 블록을 줄이지 못한다** |
| K-14 | 보고 파일이 `evidence` 등급으로 아카이브·삭제되면서 미결이 함께 사라진다 | 위임 산출 유실 | §2.7 승격 존치(J-7)가 이 리스크의 대응이다. W3-b done 8이 존치를 검사 |

### §8.11 미해소 증보

8. `verifier.md`·`planner.md` 전문 축자 대조 미수행 — 삽입 지점은 행수·헤딩 수준으로만 확인(§7 미검증 축 6). W3-b done 6이 3자 축자 정합을 검사하므로 실행 층에서 해소된다. **[해소 2026-07-27]** W3-b 실행이 3파일 공통 블록 축자 동일(1,969B)을 실측했고 Advisor가 독립 재확인했다(planner.md 는 "출력" 절 부재로 신설 — F-37 전제 부분 오류의 실행 층 정정).
9. 엔진 경로(`logs/invoke-*.json`)와 직접 위임 경로(`reports/*.md`)의 **보고 표면 2종 병존** — 통합 여부는 본 트랙 범위 밖(J-9로 층을 갈랐을 뿐 통합하지 않았다).
10. **(W3-b 완료 보고 승격 2026-07-27)** delegation-protocol §4 정본 포인터 표에 보고 전문 파일 행 미추가 — 저임팩트·Wave 5 문서 정합 후보.
11. **(W3-b 완료 보고 승격 2026-07-27)** `advisor.md` 상한 미적용 — 수임 Agent 3종에만 상한을 걸었고 Advisor→사용자 보고 층은 미확정. 층이 다르다(사용자 소통은 회수 채널이 아님) — 적용 여부는 별도 Advisor·사용자 판단 대상.

---

## §9. 채택 요청

본 문서는 **초안**이며 Advisor의 채택을 요구하는 상태다. 채택 대상은 다음 8건이다.

1. §1 편성 판정 4건(J-1~J-4) — 특히 J-1(스킵 브리지 비전제)·J-2(발견 3이 진짜 전제)가 핸드오프 §A ★1의 유의 문면을 정정한다.
2. §2 레인 판별 물리 지점(2시점·fail-closed).
3. §3 경량 원장 물리 형태(기존 스키마·기존 러너 재사용).
4. §4 Wave 설계 + 브리프 — §8.6 확장 반영 시 6 Wave·브리프 7건·병렬 집합 3개(Wave 1·2·3). K-10의 최소 성립 집합(Wave 1·2) 축소 선택지 포함.
5. §5 개정 유형 판정 표 15행 + §8.8 증보 5행 = 20행 — 정본 spec 4종 무촉 판정 포함(AGENT.md 무촉 여부는 Q-7 종속).
6. §6 카드 5건 + §8.9 카드 2건 = **사용자 게이트 7건**.
7. §8.2 판정 7건(J-5~J-11) — 특히 J-5·J-6(제2 진리원천 신설 아님·같은 백엔드 공유 가능)·J-8(절감은 Pass 경로 한정)·J-9(개정 대상은 직접 위임 층 한정).
8. 리스크 14건·미해소 9건의 원장 등재.

채택·발신(디스패치)·최종 승인은 Advisor 권한이며, Q-1~Q-7의 확정 권위는 사용자다.
