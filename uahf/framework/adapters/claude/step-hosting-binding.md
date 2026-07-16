# framework/adapters/claude/step-hosting-binding — Claude Step Hosting Adapter 바인딩

작성일: 2026-07-13
상태: v1.5 Baseline (W2 CP2 Pass 9/0/0[실행 검증 포함] · W3 E2E CP2 Pass 7/7 · CP3 승인 · 사용자 승인 2026-07-13). 직전 기준선: 없음(신규 산출물 — 마일스톤 v1.5 형태 B Step Hosting)
상위 규약: AGENT.md
근거 정본:

- framework/runtime/step-hosting-protocol.md (W1 확정 — CP2 Pass·CP3 승인, 2026-07-13) — Step 실행 호스팅의 provider-중립 계약 정본. 본 문서가 물리 실현으로 인스턴스화하는 대상. §2 위상·§3 Step 계약/Fresh Context·§4 상태 파생/결정적 재개/4 국면·§5 재시도/피드백/CP1~CP3·§6 진입 판정/Autonomy/게이트 등급 분리·§7.1 SH-INV 8건·§7.2 바인딩 지점. 재정의하지 않고 § 포인터로만 인용한다.
- framework/runtime/step-hosting-protocol.md §7.2 — 본 문서가 확정하는 바인딩 지점 표(중립 엔진 배치·invoker provider 구현·직렬화 형식·run 데이터 백엔드·정지 신호 값·Autonomy 실값 매핑·슬롯 지정 의미). 이 자리들이 본 문서·`step-invoker/` 가 실현한다.
- framework/loop/step-host/ (W2 신설 — 중립 Step Host) — 본 문서가 provider 구현을 붙이는 중립 엔진. `invoker.py` 의 Invoker/InvokeRequest/InvokeResult 계약·`events.py` 의 EventStore 추상·`host.py` 의 stop_handler·`config_schema.json` 의 config 형태. 본 문서는 그 추상을 claude 실값으로 바인딩한다.
- framework/adapters/claude/step-invoker/ (W2 신설 — invoker 의 claude 구현) — `claude_invoker.py` 의 ClaudeInvoker. 본 문서 §4·§5 가 서술하는 CLI 호출·권한 매핑·결과 파싱의 실행 코드.
- specs/03-loop.md §3.1-A·§3.1-B·§3.1-D·§3.2-A·§3.2-B — Agent Lifecycle·검증 게이트 CP1/CP2/CP3·재작업 루프·재시도 한도·사람 개입 5조건·전이 이벤트 10필드·단계 상태 5종. § 포인터로만 참조(재정의 0).
- specs/02-agent.md §3.2-B(위임 8필드)·§3.2-C(완료 보고 5필드)·§3.2-D(실패 보고)·§4(실행 모델 바인딩) — Step 직렬화·보고 회수·모델 슬롯의 정본. 참조만.
- specs/07-workflow.md §3.2-A(Work Graph·parallelSets)·§3.2-B(Task 필드) — 다중 Step 스케줄 논리의 정본. 참조만.
- framework/adapters/claude/loop-binding.md §4.1 — 형태 B 예약 로케이터("사이클 구동 연산을 사람 없이 자동으로 트리거·반복하는 실행 코드가 non-core 실행 경계에 배치")·자매 바인딩 골격 관례(§0 격리 지점 방향 반전·§2 물리 실현 표·§3 구조 제안·근거·§7 실측 대조·형태 A/B 정직 구분·L-07). 본 문서 산출물이 이 예약 자리의 실현이다.
- framework/adapters/claude/workflow-binding.md §4.1 — 형태 B 예약 로케이터("무인 병렬 오케스트레이션 실행 진입점·로더")·자매 관례. 본 문서가 실현하는 두 번째 예약 자리.
- framework/adapters/claude/verifier-binding.md·runtime-binding.md·memory-binding.md — 자매 Adapter Binding. Agent Module = 서브에이전트 디스패치(Register/Resolve)·세션/턴 수명주기·형태 A/B 정직 구분·실측 대조 관례의 선행 표본.
- framework/core/structure.md §4·§5 — 실행 코드 배치 규칙(규칙 4: AI·실행 환경 의존은 adapters/ 격리)·금지 토큰 규칙(C-3). Adapter 경계 = 격리 지점(C-3 비적용)의 근거.
- docs/form-b-step-hosting-design.md (W0 확정 — 사용자 승인 2026-07-13) §3.8·§4 — Autonomy Policy 매핑·경계 분할 확정(책임 3분리). 설계 정본. 계약 정본은 프로토콜·spec 이 소유한다(설계 §0.6).
- specs/00-glossary.md — 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- docs/session-handoff-v0.3.md §1.4·§1.5(A5·L-07 — 상태 서술은 실측 후 기록). 본 문서 §6 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 AI·환경·직렬화 형식·물리 경로·실행 옵션 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, 자매 바인딩 §0 동형). 단 이 문서는 프로토콜(step-hosting-protocol.md)·인용 spec 의 계약을 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-13 | W2 Draft | 최초 작성. `framework/adapters/claude/` 경계의 신규 산출물(형태 B Step Hosting). step-hosting-protocol.md(W1) §7.2 바인딩 지점 8건을 claude 환경 실값으로 확정: 직렬화(Step=JSON·이벤트 로그=JSONL·config=JSON)·run 데이터 백엔드 이원화(§3)·invoker 의 claude 구현 로딩·Autonomy→CLI 권한 플래그 매핑(`interactive`=기본·`auto_approve`=`--permission-mode acceptEdits`·`unrestricted`=`--dangerously-skip-permissions` — 이 플래그 문자열은 이 문서·step-invoker/ 에만 등장)·게이트 등급 분리 명기·재시도 한도 기본 2·autonomy 기본 interactive(§4)·역할 실행/CP2 독립/CP3 Advisor 디스패치 물리 형태·물리 정지 신호=종료 코드 2·win32 실행 전제·타임아웃(§5). CLI 플래그는 `claude --help` 실측(2.1.207) 확인분만 기재(§6 실측 대조). 프로토콜·spec 재정의 0, 새 계약·새 용어 0. 신설 경로 밖 파일 무수정. | Worker (Advisor 위임, Task W2) |
| 2026-07-13 | W2 확정 | CP2 독립 판정 Pass(V1~V6 — Met 9·Violated 0·Undetermined 0; 테스트 36건 라이브 재실행 Pass·CLI 플래그 `claude --help` 실측 전건 부합·토큰 경계 2개 독립 도구 교차 스캔 0건·기존 파일 무수정 실측) · CP3 Advisor 승인 · 상태행 동결. 비차단 관찰 3건(invoker FileNotFound 분기의 blocking 라벨 불일치·CLI 실호출 미검증[W3 소관]·보고 추출 중괄호 파서 엣지)은 W3 이관. Baseline 승격은 W3 사용자 게이트 유보. | Advisor |
| 2026-07-13 | W3 실증 정합 | dogfooding E2E 필수 7 시나리오 전건 실증(실 CLI 21 세션·`step-data/runs/` 8 run — CP2 독립 판정 Pass: 시나리오 7/7·차원 4/4 Met·Violated 0) · §3.2 run 구조 제안이 실물로 실현(구조 확정) · §7 OQ-SH-1 해소(CP3=배치 종단 Advisor 디스패치 실증)·자매 바인딩 OQ append 완료·신규 관찰 OQ-SH-4(CP2 모델 슬롯 결합)·OQ-SH-5(해소 API 부재·해소=fail 계수) 등재 · W2 이관 관찰 중 O-1(blocking 라벨)은 s6 호스팅 실행이 실제 정정(`claude_invoker.py` 1행·hosted CP2 통과). OQ-SH-2·3 은 미실증 open 유지. Baseline 승격은 사용자 게이트 유보. | Advisor |
| 2026-07-13 | v1.5 Baseline | 마일스톤 v1.5 「형태 B Step Execution Hosting」 사용자 승인 — 기준선 확정(Baseline 승격 게이트 통과·상태행 승격). 본문 무변경. | Advisor |
| 2026-07-13 | v1.6 정합 (본문 무변경 — §7 OQ append) | §7 OQ-SH-4(CP2 모델 슬롯 결합) 해소 표기 append — 마일스톤 v1.6 Project Orchestration 이 중립 Host `cp2_model` 선택 파라미터(기본 `None`=기존 거동 바이트 동일)로 CP2 검증 모델 독립 지정을 실현(OQ-SH-1 해소 표기 관례 동형·원 문면 보존). `project-orchestration-binding.md` §4.3 참조. OQ-SH-2/3/5 무변·본문 계약·SH-INV 무변경·상태행 무상승(v1.5 Baseline 유지). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 framework/runtime/step-hosting-protocol.md(§2~§7)와 인용 spec(03/02/07/06/04) §3 계약이다.** 이 문서는 그 계약의 **claude 환경 실현 매핑**이며, 계약 요소(위상·Step 직렬화 축·상태 파생 규칙·SH-INV·Autonomy 어휘·게이트 등급 분리)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 프로토콜 §7.2 가 "직렬화 형식·run 데이터 백엔드 경로·정지 신호 값·Autonomy 실값·provider 실행 옵션 매핑·슬롯 지정 의미는 Adapter Binding 문서 소관"이라며 미룬 지점이 실재하는(확정되는) 자리다.
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리(`framework/loop/step-host/`) 본문·코드는 특정 AI·provider·실행 옵션 토큰이 0건이어야 한다(structure.md §5, 프로토콜 SH-INV-7). 이 문서는 그 **반대편**이다 — 구체 토큰(`claude` CLI·`--dangerously-skip-permissions` 등 실행 옵션·물리 경로·직렬화 형식명)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 바인딩 §0 동형).
- **`--dangerously-skip-permissions` 문자열의 유일 소재.** 저장소 전수 스캔 AC: 이 권한 생략 플래그 문자열은 **이 문서와 `framework/adapters/claude/step-invoker/` 코드에만** 존재해야 한다. Core·프로토콜·`framework/loop/step-host/` 에는 0건이다(§4.2·§6).
- **창설 금지.** 이 문서는 프로토콜 §7.2 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. 새 상태·새 필드·새 개입 조건·새 불변 규칙을 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 Bootstrap 상태다. 그러나 형태 B Step Hosting 은 **실행 코드가 실재**하는 첫 산출물이다 — 중립 Host(`framework/loop/step-host/`, W2 신설)와 그 claude invoker(`step-invoker/`, W2 신설)는 파일 시스템에 실재하며 자체 테스트가 통과한다(§6 실측). 실제 CLI 실호출로 구동하는 dogfooding E2E 는 W3 소관이다(run 데이터 백엔드는 그때 생성 — L-07 정직 구분).
- 용어는 specs/00-glossary.md 정본만 사용한다. "Step Host"·"Step Contract"·"형태 A/B" 는 프로토콜·structure.md 의 서술 라벨이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 step-hosting-protocol.md(§7.2 바인딩 지점)를 claude 환경 위에 **W2 시점의 구체 물리 실현**으로 매핑한다.

책임은 다섯 가지다.

- 직렬화 형식(Step 파일·이벤트 로그·config)과 run 데이터 백엔드 경로를 확정한다(§3, 프로토콜 §7.2 행 3·4).
- invoker 인터페이스의 claude 구현 로딩·Autonomy Policy→CLI 권한 플래그 매핑·재시도 한도·autonomy 기본값을 확정하고, 게이트 등급 분리를 명기한다(§4, 프로토콜 §7.2 행 2·6·§6.2).
- 역할 실행(CP1 Worker)·CP2 독립 디스패치·CP3 Advisor 승인의 물리 형태와 물리 정지 신호 값·모델/역할 슬롯 전달·win32 실행 전제·타임아웃을 확정한다(§5, 프로토콜 §7.2 행 5·7·§5.2).
- CLI 플래그를 `claude --help` 실측으로 대조하고 상태 서술을 실측과 대조한다(§6, L-07).
- 미확정 잔여를 Open Questions 로 명시한다(§7).

이 문서는 프로토콜·인용 spec 의 어떤 계약 요소도 재정의·확장하지 않는다. 형태 A → 형태 B 전환에도 Core Contract(01/02/03/06/07 §3) 변경은 0이다(C-1).

---

## §2. 프로토콜 §7.2 바인딩 지점 → claude 물리 실현 (개관)

step-hosting-protocol.md §7.2 표(바인딩 지점 7행)를 claude 환경 실현으로 매핑한다. "실재 여부" 열은 파일 시스템 직접 실측에 근거한다(L-07).

| 프로토콜 §7.2 바인딩 지점 | claude 물리 실현 | 실재 여부 |
|---|---|---|
| 중립 Step Host 엔진 배치(host 코드 + configSchema) | `framework/loop/step-host/`(step.py·events.py·bundle.py·invoker.py·host.py·config_schema.json). provider·옵션 토큰 0. | **실재**(W2 신설 — §6 실측·자체 테스트 통과). |
| invoker 인터페이스의 provider 구현 | `framework/adapters/claude/step-invoker/claude_invoker.py`(ClaudeInvoker). | **실재**(W2 신설 — §6 실측·자체 테스트 통과). |
| Step 직렬화 형식·이벤트 로그 직렬화 형식 | Step 파일 = JSON(자기완결 번들)·이벤트 로그 = JSONL(1행 1이벤트, 03 §3.2-A 10필드)·config = JSON(§3). | 형식 확정(§3). 중립 Host 기본 EventStore = JSONL(JsonlEventStore). |
| run 데이터 백엔드 경로 | 이원화: 일반 = 소비 프로젝트 관례 경로(config 필수 지정) / dogfooding = `framework/adapters/claude/step-data/runs/<run-id>/`(§3.2). | 경로 정본 확정(§3.2). 데이터는 **미생성** — W3 E2E 시 생성(L-07). |
| 물리 정지 신호 값 | 프로세스 종료 코드 **2**(blocked/Escalated 정지). Host 의 stop_handler 를 종료 코드 2로 바인딩한다(§5.3). | 값 확정(§5.3). |
| Autonomy Policy 실값·provider 실행 옵션 매핑 | `interactive`=기본 실행 / `auto_approve`=`--permission-mode acceptEdits` / `unrestricted`=`--dangerously-skip-permissions`(§4.2). | 매핑 확정(§4.2). `step-invoker/` 코드 실재. |
| role/capability/model 슬롯의 실행 모델 지정 의미 | `--model <slot>` 전달(값 의미는 02 §4 소관 — 전달만). 역할 = 서브에이전트/fresh 세션 브리프(§5.1). | 전달 경로 확정(§5.1). |

---

## §3. 직렬화 형식·run 데이터 백엔드 (프로토콜 §7.2 행 3·4)

### §3.1 직렬화 형식 정본

- **Step 파일 = JSON.** 각 Step(07 §3.2-B Task + 02 §3.2-B 위임 8필드 + 슬롯)의 자기완결 직렬화는 JSON 한 객체다. 중립 Host 의 `step.Step.from_dict` 가 이 매핑을 로드한다.
- **이벤트 로그 = JSONL.** run 의 append-only 이벤트 로그는 JSON Lines(1행 = 1 전이 이벤트)다. 각 행은 03 §3.2-A 전이 이벤트 10필드(cycle_id·seq·from_stage·to_stage·trigger·outcome·retry_count·actor·ref·at)를 담는다. 중립 Host 의 기본 `events.JsonlEventStore` 가 이 형식을 실현하며, Adapter 는 EventStore 추상을 교체할 수 있다. loop-binding.md §3 의 `loop-data/<cycle_id>.jsonl`(사이클당 파일 1개) 관례와 사실 관계가 다르다 — Step Host 의 run 로그는 **run 당 파일 1개**에 여러 Step(사이클)의 이벤트를 append 하며, `seq` 는 cycle_id 별 순번, `at` 은 run 전역 append 순서다(프로토콜 §4.1).
- **config = JSON.** `framework/loop/step-host/config_schema.json`(JSON Schema Draft-07)이 config 형태를 규정한다. 실값(invoker 모듈 경로·retry_limit·autonomy·run_data_dir·timeout)은 소비 프로젝트/Adapter config 데이터가 채운다.
- **직렬화 = 이식 교체 지점.** 위 형식 선택(JSON/JSONL)은 이식 시 대상 환경의 직렬화 메커니즘으로 교체된다. 프로토콜 §3·§4 의 필드·불변은 유지되고 물리 직렬화만 교체된다.

### §3.2 run 데이터 백엔드 경로 (이원화 — DP-X2 동형)

- **일반 관례.** 소비 프로젝트 내 관례 경로. config 의 `run_data_dir` 로 **필수 지정**한다(소비 프로젝트가 소유). Step Host 는 그 경로에 run 로그·Step 파일·실행 상세를 남긴다.
- **dogfooding.** 이 워크스페이스의 자기 실행(W3 E2E)은 `framework/adapters/claude/step-data/runs/<run-id>/` 에 귀속한다 — Adapter 경계 이하 격리(자매 `*-data/`(memory-data·loop-data) 동형). 이 경로는 Core 경계·`specs/`·`docs/` 밖이다.
- **실재 상태(L-07).** `framework/adapters/claude/step-data/` 는 **W3 소관이며 현 시점 미생성**이다. 본 문서(W2)는 그 경로·구조 정본만 소유하고 데이터를 생성하지 않는다(L-07 — 미존재를 실재로 쓰지 않는다). 중립 Host 의 자체 테스트는 임시 디렉터리를 사용한다(§6).
- **run 로그 구조(구조 제안).** `runs/<run-id>/events.jsonl`(run 이벤트 로그) + `runs/<run-id>/steps/<step-id>.json`(Step 직렬화) + `runs/<run-id>/config.json`. 정확한 하위 구조는 W3 E2E 가 이 제안대로 생성해 실현·확정한다(loop-binding.md §3.1 "구조 제안·근거" 관례 동형).

---

## §4. invoker claude 구현·Autonomy 매핑·기본값 (프로토콜 §7.2 행 2·6·§6.2)

### §4.1 invoker 구현 로딩

- 중립 Host 는 invoker 구현체 이름을 하드코딩하지 않고 config 의 모듈 경로 문자열로 로드한다(`invoker.load_invoker`). claude 환경의 config 는 이 값을 다음으로 지정한다:

  ```
  "invoker": { "module": "claude_invoker:ClaudeInvoker", "options": { "cli": "claude" } }
  ```

  (모듈 탐색은 `framework/adapters/claude/step-invoker/` 를 로드 경로에 두는 것을 전제로 한다 — claude_invoker.py 는 임포트 시 중립 Host 의 invoker 계약 경로를 sys.path 에 추가한다.)
- `ClaudeInvoker` 는 Invoker 계약(invoke(request) → InvokeResult)을 구현한다: 직렬화 번들 → claude CLI headless 호출(subprocess·shell=False) → 완료/실패/차단 보고 회수.

### §4.2 Autonomy Policy → CLI 권한 플래그 매핑 (Advisor 확정값)

프로토콜 §6.2 정책 어휘 3값을 claude CLI 권한 실행 옵션으로 매핑한다(실측 플래그 — §6):

| policy(데이터) | claude CLI 실현 | 의미 |
|---|---|---|
| `interactive`(**기본값**) | 별도 권한 생략 플래그 없음(`-p` headless 기본 실행) | 도구 실행 승인 프롬프트 유지 축. |
| `auto_approve` | `--permission-mode acceptEdits` | 선언된 허용 범위(편집) 내 자동 승인. 필요 시 `--allowedTools` 로 허용 범위를 함께 선언한다. |
| `unrestricted` | `--dangerously-skip-permissions` | 승인 프롬프트 전면 생략. **이 플래그 문자열은 이 문서와 `step-invoker/` 코드에만 존재한다**(§0·전수 스캔 AC). |

- **게이트 등급 분리(불가침 — SH-INV-4 명기).** 위 매핑은 **도구 실행 승인 프롬프트 축만** 제어한다. **Human Decision Gate — Contract 변경·중대 Architecture Decision·파괴적 작업·해결 불가 불확실성(03 §3.1-D 조건 2~5 + UAF 레벨 게이트) — 는 어떤 policy 값에서도 `Escalated` 정지로 보존**된다. `unrestricted` 에서도 이 게이트는 정지하며 **CP2 를 우회하지 않는다**. 이 강제는 **중립 Host 코드가 소유**한다(host.py — policy 무관하게 CP2 를 별도 디스패치하고 Escalated 시 정지). `ClaudeInvoker` 는 policy 를 CLI 플래그로 매핑만 하며 이 게이트를 우회할 수 없다. 자체 테스트로 실증됨(step-host 시나리오 ⑦ — §6).

### §4.3 기본값 (Advisor 확정값)

- **재시도 한도 기본값 = 2.** 03 §3.1-B·framework/core/config-schema.md §7 의 `retry.limit` 기본값(2)과 정합한다. Step Host 는 이 값의 소비자이며(01 §3.2-B), config 의 `retry_limit` 로 override 가능하다. 중립 Host 의 `DEFAULT_RETRY_LIMIT` 도 2다.
- **autonomy 기본값 = `interactive`.** config 에 autonomy 미지정 시 `interactive` 로 구동한다(권한 보존 기본 — P-D5).

---

## §5. 역할 실행·CP2/CP3 디스패치·정지 신호·슬롯·실행 전제 (프로토콜 §7.2 행 5·7·§5.2)

### §5.1 역할 실행·모델/역할 슬롯 전달

- **CP1 = Worker fresh 세션.** Step 은 신규(격리) claude 세션에서 실행된다 — `ClaudeInvoker` 가 `-p`(headless) 로 Worker 브리프(`--append-system-prompt`)와 직렬화 번들(프롬프트)을 전달한다. Worker 는 Execute + CP1 자체 점검을 수행하고 완료/실패 보고(JSON)를 최종 메시지로 낸다(02 §3.2-C/D).
- **모델 슬롯 전달.** Step 의 `model` 슬롯 값이 있으면 `--model <slot>` 으로 전달한다. 값의 의미(모델 지정)는 02 §4 소관이며 Host·invoker 는 전달만 한다(프로토콜 §3.1·§3.9). 슬롯이 없으면 세션 기본 모델을 상속한다.
- **역할 슬롯.** 역할 브리프(Worker/Verifier/Advisor)는 `--append-system-prompt` 로 주입한다. 이는 자매 바인딩의 "역할 = 서브에이전트 디스패치" 관례(verifier-binding.md §3.1)의 무인 실행 형태다 — 무인 fresh 세션 브리프.

### §5.2 CP2 독립 디스패치·CP3 Advisor 승인

- **CP2 = 별도 독립 fresh 세션(Verifier).** 완료 보고 회수 후, 중립 Host 가 CP2 를 **별도 invoke 호출**(role=Verifier)로 디스패치한다 — CP1 과 같은 세션이 겸하지 않는다(자가판정 완료 확정 금지, 06 V1). Verifier 는 산출물(artifacts) 자체를 근거로 criteria(done) 충족을 독립 판정하고 `{"verdict":"Pass|Fail","rework":...}` 를 낸다. "Passed" 이벤트는 CP2 Pass 확정 후에만 append 된다.
- **CP3 = Advisor 역할 승인.** CP3 는 사람 승인이 아니라 Advisor 역할의 승인(02 §3.1)이므로 무인 실행과 양립한다. claude 실현은 role=Advisor fresh 세션 디스패치이며, 사이클 Complete 전 또는 배치 종단에서 일괄 수행한다(프로토콜 §5.2). W2 자체 테스트 범위는 CP1→CP2→Passed 이며, CP3 디스패치 물리 형태의 E2E 실증은 W3 소관이다.

### §5.3 물리 정지 신호 값 (Advisor 확정값)

- **정지 신호 = 프로세스 종료 코드 2.** blocked(차단 선언) 또는 Escalated 정지 시, Step Host 를 구동하는 런처 프로세스는 **종료 코드 2**로 종료한다. 중립 Host 는 정지를 `stop_handler` 콜백으로만 위임하며 특정 값을 두지 않는다(프로토콜 §7.2). claude 런처는 이 stop_handler 를 `sys.exit(2)` 로 바인딩한다. (원본 harness 의 exit 2 blocker 관례 동형 — 설계 §3.5.) 종료 코드 2 는 정상 종료(0)·일반 실패(1)와 구분되는 "사람/상위 개입 대기" 신호다.

### §5.4 win32 실행 전제·타임아웃 (실측)

- **실행 전제(실측 2026-07-13).** win32 · Python **3.14.4**(`python` 런처) · claude CLI **2.1.207**. subprocess 는 `shell=False` 로 argv 직접 전달(인젝션 방지)하며 경로는 `pathlib` 으로 win32/POSIX 양립한다.
- **타임아웃.** config 의 `timeout`(초)이 각 invoke 의 subprocess 타임아웃으로 전달된다. 타임아웃 초과는 **차단이 아니라 실패**로 처리되어 재시도 규칙(프로토콜 §5.1)을 탄다 — 정지 신호는 Host 의 Escalated 판정이 소유한다. `null` = 무제한.

---

## §6. 실측 대조 (L-07)

- **CLI 플래그 실측(`claude --help`, 2.1.207).** 본 문서·`step-invoker/` 가 쓰는 플래그는 전부 실측 확인분이다: `-p, --print`(headless) · `--output-format <text|json|stream-json>` · `--model <alias|full>` · `--permission-mode <acceptEdits|auto|bypassPermissions|manual|dontAsk|plan>` · `--dangerously-skip-permissions` · `--append-system-prompt <prompt>` · `--add-dir <dirs...>`. 추측 플래그 0.
- **산출물 실재.** `framework/loop/step-host/`(step.py·events.py·bundle.py·invoker.py·host.py·config_schema.json·README.md·tests/) 와 `framework/adapters/claude/step-invoker/`(claude_invoker.py·tests/) 는 W2 에 파일 시스템 실재로 생성됐다. 자체 테스트는 표준 라이브러리 `unittest` 만으로 통과한다(중립 Host 17건·claude invoker 19건).
- **provider 토큰 스캔.** `framework/loop/step-host/` 소스에 provider·실행 옵션 토큰 0건(전수 스캔). `--dangerously-skip-permissions` 문자열은 이 문서와 `step-invoker/` 에만 존재한다.
- **미생성 구분.** `framework/adapters/claude/step-data/`(run 데이터 백엔드)는 **미생성**이다 — W3 E2E 가 §3.2 정본 구조대로 생성한다. 본 문서는 그 실재를 주장하지 않는다(L-07).

---

## §7. Open Questions

- **OQ-SH-1 (CP3 물리 형태 E2E) — 해소됨 (W3 dogfooding E2E, 2026-07-13).** CP3(Advisor 역할) 디스패치의 물리 형태(사이클 Complete 전 개별 vs 배치 종단 일괄)는 W2 자체 테스트 범위 밖이며 W3 E2E 에서 실증·확정한다. **W3 실증: 배치 종단 일괄** — run 완주 후 런처가 role=Advisor fresh 세션을 별도 디스패치해 `final_verdict` 를 회수·기록한다(`step-data/runs/e2e-s1-normal/logs/cp3-result.json` = Pass — 물리 증거).
- **OQ-SH-2 (`interactive` headless 반의어).** headless(`-p`) 실행에서 `interactive` policy 의 도구 승인 프롬프트는 대화 채널이 없으므로 실질적으로 승인 대기 없이 진행 제약을 받을 수 있다. `interactive` 의 headless 의미(예: 승인 필요 도구 만나면 blocked 로 에스컬레이션)의 정밀 정의는 W3 E2E 관찰로 확정한다. 현재는 "기본 실행(권한 생략 플래그 없음)"으로만 바인딩한다.
- **OQ-SH-3 (`--output-format stream-json` 채택).** 대량 산출·진행 표시가 필요한 E2E 에서 `json`(단일 결과) vs `stream-json`(실시간)의 선택은 W3 관찰로 확정한다. 현재 기본은 `json`.
- **자매 바인딩 OQ append(비차단) — 해소됨 (W3 정합, 2026-07-13).** loop-binding §9·workflow-binding §9·OQ 에 "형태 B 부분 실현(Step Host)" 사실을 append 하는 정합 작업은 W3 소관이다(설계 §6·BPD-17 규율). 본 문서 범위 밖. **W3 정합 완료: loop-binding §8 OQ-LB-2 해소 표기·workflow-binding §8 OQ-WB-2 부분 해소 표기 + 각 §9 이력 행 append(버전 무상승·append-only).**
- **OQ-SH-4 (CP2 모델 슬롯 결합 — W3 관찰·비차단) — 해소됨 (마일스톤 v1.6 Project Orchestration, 2026-07-13).** 중립 Host(`host.py _dispatch_cp2`)는 CP2 Verifier 를 `model=step.model` 로 디스패치한다 — Verifier 가 검증 전용 모델을 독립 지정할 수 없고 Step 슬롯을 상속한다(W3 실측: e2e-s6 은 Worker=sonnet 이라 CP2 도 sonnet). Worker/Verifier 모델 독립 지정 여부는 후속 설계 판단(중립 Host 개정 사안 — 계약 무변, 02 §4 소관 슬롯 의미는 그대로). **해소(v1.6): 중립 Host `StepHost(cp2_model=...)` 선택 파라미터 추가(기본 `None` = 기존 거동 `model=step.model` 바이트 동일)로 CP2 검증 단위 모델을 피검증 단위와 독립 지정 가능해졌다 — `config_schema.json` 선택 필드 `cp2_model`·step-host 회귀 전건 무손상·`project-orchestration-binding.md` §4.3 참조.**
- **OQ-SH-5 (Escalation 해소 API 부재·해소=fail 계수 결합 — W3 관찰·비차단).** blocked/재시도 한도 초과 `Escalated` 의 해소에 전용 이벤트 어휘·연산이 없어, 해소는 "파생 상태를 Failed 로 되돌리는 `outcome=fail`(ref.kind=resolved) 이벤트의 수동 append"로 실현된다(W3 s3 실측 — 프로토콜 §4.3 해소 이벤트의 현행 물리 형태). 이 재사용 때문에 해소 이벤트가 `prior_failures` 재시도 예산을 소모한다(s3 에서 해소 이벤트 중복 append 가 한도 1 을 소모해 retry-limit-exceeded 를 조기 유발 — 로그만으로 전 과정 재구성 가능·append-only 보존). 전용 해소 어휘(재시도 비계수) 도입 여부는 후속 설계 판단. 부수 관찰: E2E 드라이버(`step-data/e2e/` — Host/바인딩 아님)의 invoke 로그 파일명이 프로세스별 순번이라 재기동 시 이전 프로세스의 원출력 로그가 덮어쓰일 수 있음(권위 기록 events.jsonl 은 무영향).
