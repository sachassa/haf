# framework/adapters/claude/step-hosting-binding — Claude Step Hosting Adapter 바인딩

작성일: 2026-07-13
상태: v1.5 Baseline (W2 CP2 Pass 9/0/0[실행 검증 포함] · W3 E2E CP2 Pass 7/7 · CP3 승인 · 사용자 승인 2026-07-13). 직전 기준선: 없음(신규 산출물 — 마일스톤 v1.5 형태 B Step Hosting)
상위 규약: AGENT.md
근거 정본 (계약은 § 포인터로만 인용 — 재정의 0 선언은 §0 1곳):

- framework/runtime/step-hosting-protocol.md (W1 확정) — Step 실행 호스팅의 provider-중립 계약 정본. §2 위상 · §3 Step 계약/Fresh Context · §4 상태 파생·결정적 재개·4 국면 · §5 재시도/피드백/CP1~CP3 · §6 진입 판정/Autonomy/게이트 등급 분리 · §7.1 SH-INV 8건 · **§7.2 바인딩 지점 표** = 본 문서와 `step-invoker/` 가 실현하는 자리.
- 실행 코드 — framework/loop/step-host/(중립 엔진: invoker.py Invoker/InvokeRequest/InvokeResult · events.py EventStore 추상 · host.py stop_handler · config_schema.json) · framework/adapters/claude/step-invoker/(claude_invoker.py ClaudeInvoker = §4·§5 의 실행 코드).
- specs — 03-loop.md §3.1-A/B/D·§3.2-A/B · 02-agent.md §3.2-B/C/D·§4 · 07-workflow.md §3.2-A/B · 00-glossary.md(용어 정본, 신설 0). framework/core/structure.md §4·§5(실행 코드 배치 규칙 4·금지 토큰 C-3).
- 자매 Adapter Binding — loop-binding.md §4.1·workflow-binding.md §4.1(형태 B 예약 로케이터 = 본 문서가 실현하는 두 자리) · verifier·runtime·memory-binding.md(형태 A/B 정직 구분·실측 대조 관례). Active Lesson L-07(상태 서술은 실측 후 기록 — §6 근거).
- `docs/form-b-step-hosting-design.md@cd9247b` §3.8·§4 — Autonomy 매핑·경계 3분리 설계 정본(아카이브; 열람 = `git show cd9247b:docs/form-b-step-hosting-design.md`). 계약 정본은 프로토콜·spec 소유(설계 §0.6).

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다 — Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 AI·환경·직렬화 형식·물리 경로·실행 옵션 토큰의 사용이 허용된다(C-3 비적용 — 자매 바인딩 §0 동형). 개정은 Advisor 승인 + §9 이력 기록으로만 이뤄진다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-13 | W2 Draft | 최초 작성. `framework/adapters/claude/` 경계의 신규 산출물(형태 B Step Hosting). step-hosting-protocol.md(W1) §7.2 바인딩 지점 8건을 claude 환경 실값으로 확정: 직렬화(Step=JSON·이벤트 로그=JSONL·config=JSON)·run 데이터 백엔드 이원화(§3)·invoker 의 claude 구현 로딩·Autonomy→CLI 권한 플래그 매핑(`interactive`=기본·`auto_approve`=`--permission-mode acceptEdits`·`unrestricted`=`--dangerously-skip-permissions` — 이 플래그 문자열은 이 문서·step-invoker/ 에만 등장)·게이트 등급 분리 명기·재시도 한도 기본 2·autonomy 기본 interactive(§4)·역할 실행/CP2 독립/CP3 Advisor 디스패치 물리 형태·물리 정지 신호=종료 코드 2·win32 실행 전제·타임아웃(§5). CLI 플래그는 `claude --help` 실측(2.1.207) 확인분만 기재(§6 실측 대조). 프로토콜·spec 재정의 0, 새 계약·새 용어 0. 신설 경로 밖 파일 무수정. | Worker (Advisor 위임, Task W2) |
| 2026-07-13 | W2 확정 | CP2 독립 판정 Pass(V1~V6 — Met 9·Violated 0·Undetermined 0; 테스트 36건 라이브 재실행 Pass·CLI 플래그 `claude --help` 실측 전건 부합·토큰 경계 2개 독립 도구 교차 스캔 0건·기존 파일 무수정 실측) · CP3 Advisor 승인 · 상태행 동결. 비차단 관찰 3건(invoker FileNotFound 분기의 blocking 라벨 불일치·CLI 실호출 미검증[W3 소관]·보고 추출 중괄호 파서 엣지)은 W3 이관. Baseline 승격은 W3 사용자 게이트 유보. | Advisor |
| 2026-07-13 | W3 실증 정합 | dogfooding E2E 필수 7 시나리오 전건 실증(실 CLI 21 세션·`step-data/runs/` 8 run — CP2 독립 판정 Pass: 시나리오 7/7·차원 4/4 Met·Violated 0) · §3.2 run 구조 제안이 실물로 실현(구조 확정) · §7 OQ-SH-1 해소(CP3=배치 종단 Advisor 디스패치 실증)·자매 바인딩 OQ append 완료·신규 관찰 OQ-SH-4(CP2 모델 슬롯 결합)·OQ-SH-5(해소 API 부재·해소=fail 계수) 등재 · W2 이관 관찰 중 O-1(blocking 라벨)은 s6 호스팅 실행이 실제 정정(`claude_invoker.py` 1행·hosted CP2 통과). OQ-SH-2·3 은 미실증 open 유지. Baseline 승격은 사용자 게이트 유보. | Advisor |
| 2026-07-13 | v1.5 Baseline | 마일스톤 v1.5 「형태 B Step Execution Hosting」 사용자 승인 — 기준선 확정(Baseline 승격 게이트 통과·상태행 승격). 본문 무변경. | Advisor |
| 2026-07-13 | v1.6 정합 (본문 무변경 — §7 OQ append) | §7 OQ-SH-4(CP2 모델 슬롯 결합) 해소 표기 append — 마일스톤 v1.6 Project Orchestration 이 중립 Host `cp2_model` 선택 파라미터(기본 `None`=기존 거동 바이트 동일)로 CP2 검증 모델 독립 지정을 실현(OQ-SH-1 해소 표기 관례 동형·원 문면 보존). `project-orchestration-binding.md` §4.3 참조. OQ-SH-2/3/5 무변·본문 계약·SH-INV 무변경·상태행 무상승(v1.5 Baseline 유지). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지)·form-b-step-hosting-design.md 설계 정본 @cd9247b 앵커·OQ-SH-1 run 인스턴스 증거 @cd9247b 앵커. step-data/runs 백엔드 경로 구조는 계약 서술로 유지. 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 2 — 비계약 격리 개정: 재서술·스냅샷·죽은 참조 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 framework/runtime/step-hosting-protocol.md(§2~§7)와 인용 spec(03/02/07/06/04) §3 계약이다.** 이 문서는 그 계약의 **claude 환경 실현 매핑**이며 계약 요소(위상·Step 직렬화 축·상태 파생 규칙·SH-INV·Autonomy 어휘·게이트 등급 분리)를 **재정의·확장하지 않는다** — **이 재정의 0 선언은 문서 전체에 대해 여기 1곳에서만 두며**, 이하 각 절은 반복 없이 정본 §만 지목한다.
- **소관 지점.** 프로토콜 §7.2 가 "직렬화 형식·run 데이터 백엔드 경로·정지 신호 값·Autonomy 실값·provider 실행 옵션 매핑·슬롯 지정 의미는 Adapter Binding 소관"이라며 미룬 자리를 이 문서가 확정한다.
- **격리 지점(C-3 비적용).** Core 경계와 중립 Module(`framework/loop/step-host/`)은 provider·실행 옵션 토큰 0건이어야 하지만(structure.md §5, SH-INV-7), 이 문서는 그 **반대편**이다 — 구체 토큰의 사용이 허용되며 그 격리가 이 경계의 존재 이유다.
- **`--dangerously-skip-permissions` 문자열의 유일 소재(정본 선언).** 이 권한 생략 플래그 문자열이 **문서 층에서 등장하도록 허용되는 유일한 자리는 이 문서**이며, 코드 층에서는 `framework/adapters/claude/step-invoker/` 뿐이다. Core·프로토콜·`framework/loop/step-host/` 에는 0건이다(§4.2·§6, SH-INV-7). **정정(2026-07-26, 2차):** 상위 오케스트레이션 바인딩에 있던 1건은 같은 날 md 슬림화 Wave 4b에서 이 문서 §0·§4.2 포인터로 대체되어 제거됐다 — 문서 층 소재는 다시 이 문서뿐이다. `uaf-verified: 저장소 전수 grep(dangerously-skip-permissions) — 3파일 11건(이 문서·step-invoker 코드/테스트), Core·프로토콜·step-host 0건 불변`
- **창설 금지.** 프로토콜 §7.2 표를 넘어서는 새 바인딩 계약·새 상태·새 필드·새 개입 조건·새 불변 규칙을 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 형태 B Step Hosting 은 **실행 코드가 실재**하는 첫 산출물이다 — 중립 Host 와 claude invoker 가 실재하고 자체 테스트가 통과하며(§6), 실 CLI dogfooding E2E(W3)로 run 데이터 백엔드도 실재화됐다(§3.2·§6 정정 지점).
- 용어는 specs/00-glossary.md 정본만 사용한다. "Step Host"·"Step Contract"·"형태 A/B" 는 프로토콜·structure.md 의 서술 라벨이다.

---

## §1. 목적

이 문서는 step-hosting-protocol.md §7.2 바인딩 지점을 claude 환경의 구체 물리 실현으로 매핑한다. 정본 경계·격리·창설 금지 선언은 §0에 1벌만 둔다.

절별 책임 — §2 §7.2 바인딩 지점 개관 · §3 직렬화 형식·run 데이터 백엔드(행 3·4) · §4 invoker claude 구현·Autonomy→CLI 권한 매핑·기본값·게이트 등급 분리(행 2·6·§6.2) · §5 역할 실행·CP2/CP3 디스패치·물리 정지 신호·슬롯·실행 전제(행 5·7·§5.2) · §6 실측 대조(L-07) · §7 Open Questions.

형태 A → 형태 B 전환에도 Core Contract(01/02/03/06/07 §3) 변경은 0이다(C-1).

---

## §2. 프로토콜 §7.2 바인딩 지점 → claude 물리 실현 (개관)

step-hosting-protocol.md §7.2 표(바인딩 지점 7행)를 claude 환경 실현으로 매핑한다. "실재 여부" 열은 파일 시스템 직접 실측에 근거한다(L-07).

| 프로토콜 §7.2 바인딩 지점 | claude 물리 실현 | 실재 여부 |
|---|---|---|
| 중립 Step Host 엔진 배치(host 코드 + configSchema) | `framework/loop/step-host/`(step.py·events.py·bundle.py·invoker.py·host.py·config_schema.json). provider·옵션 토큰 0. | **실재**(W2 신설 — §6 실측·자체 테스트 통과). |
| invoker 인터페이스의 provider 구현 | `framework/adapters/claude/step-invoker/claude_invoker.py`(ClaudeInvoker). | **실재**(W2 신설 — §6 실측·자체 테스트 통과). |
| Step 직렬화 형식·이벤트 로그 직렬화 형식 | Step 파일 = JSON(자기완결 번들)·이벤트 로그 = JSONL(1행 1이벤트, 03 §3.2-A 10필드)·config = JSON(§3). | 형식 확정(§3). 중립 Host 기본 EventStore = JSONL(JsonlEventStore). |
| run 데이터 백엔드 경로 | 이원화: 일반 = 소비 프로젝트 관례 경로(config 필수 지정) / dogfooding = `framework/adapters/claude/step-data/runs/<run-id>/`(§3.2). | 경로 정본 확정(§3.2). 데이터 **실재** — W3 E2E 가 생성(`runs/`·`e2e/` — §6 실측, 종전 "미생성" 서술 정정). |
| 물리 정지 신호 값 | 프로세스 종료 코드 **2**(blocked/Escalated 정지). Host 의 stop_handler 를 종료 코드 2로 바인딩한다(§5.3). | 값 확정(§5.3). |
| Autonomy Policy 실값·provider 실행 옵션 매핑 | `interactive`=기본 실행 / `auto_approve`=`--permission-mode acceptEdits` / `unrestricted`=`--dangerously-skip-permissions`(§4.2). | 매핑 확정(§4.2). `step-invoker/` 코드 실재. |
| role/capability/model 슬롯의 실행 모델 지정 의미 | `--model <slot>` 전달(값 의미는 02 §4 소관 — 전달만). 역할 = 서브에이전트/fresh 세션 브리프(§5.1). | 전달 경로 확정(§5.1). |

---

## §3. 직렬화 형식·run 데이터 백엔드 (프로토콜 §7.2 행 3·4)

### §3.1 직렬화 형식 정본

- **Step 파일 = JSON.** 각 Step(07 §3.2-B Task + 02 §3.2-B 위임 8필드 + 슬롯)의 자기완결 직렬화는 JSON 한 객체다. 중립 Host 의 `step.Step.from_dict` 가 이 매핑을 로드한다.
- **이벤트 로그 = JSONL.** run 의 append-only 이벤트 로그는 JSON Lines(1행 = 1 전이 이벤트)이며, 각 행은 03 §3.2-A 전이 이벤트 10필드(cycle_id·seq·from_stage·to_stage·trigger·outcome·retry_count·actor·ref·at)를 담는다. 기본 `events.JsonlEventStore` 가 이 형식을 실현하고 Adapter 는 EventStore 추상을 교체할 수 있다. loop-binding.md §3 의 `loop-data/<cycle_id>.jsonl`(사이클당 1파일) 관례와 다르다 — Step Host 의 run 로그는 **run 당 파일 1개**에 여러 Step 의 이벤트를 append 하며 `seq` 는 cycle_id 별 순번, `at` 은 run 전역 append 순서다(프로토콜 §4.1).
- **config = JSON.** `framework/loop/step-host/config_schema.json`(JSON Schema Draft-07)이 config 형태를 규정한다. 실값(invoker 모듈 경로·retry_limit·autonomy·run_data_dir·timeout)은 소비 프로젝트/Adapter config 데이터가 채운다.
- **직렬화 = 이식 교체 지점.** 위 형식 선택(JSON/JSONL)은 이식 시 대상 환경의 직렬화 메커니즘으로 교체된다. 프로토콜 §3·§4 의 필드·불변은 유지되고 물리 직렬화만 교체된다.

### §3.2 run 데이터 백엔드 경로 (이원화 — DP-X2 동형)

- **일반 관례.** 소비 프로젝트 내 관례 경로. config 의 `run_data_dir` 로 **필수 지정**한다(소비 프로젝트가 소유). Step Host 는 그 경로에 run 로그·Step 파일·실행 상세를 남긴다.
- **dogfooding.** 이 워크스페이스의 자기 실행(W3 E2E)은 `framework/adapters/claude/step-data/runs/<run-id>/` 에 귀속한다 — Adapter 경계 이하 격리(자매 `*-data/`(memory-data·loop-data) 동형). 이 경로는 Core 경계·`specs/`·`docs/` 밖이다.
- **실재 상태(정정 2026-07-26).** `framework/adapters/claude/step-data/` 는 **실재**한다 — W3 E2E 가 이 정본 구조(`runs/<run-id>/events.jsonl` + `steps/<step-id>.json` + `config.json`)대로 생성했다(§6 실측·§9 W3 행). W2 시점의 "미생성" 서술은 그 시점 사실이었고 현재는 사실이 아니다. 개별 run 원장은 산출물 수명 정책으로 제거되므로 잔여 run 개수를 계약 근거로 삼지 않으며, 중립 Host 자체 테스트는 임시 디렉터리를 쓴다.

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
| `unrestricted` | `--dangerously-skip-permissions` | 승인 프롬프트 전면 생략. **이 플래그 문자열의 소재는 §0이 전수 스캔 결과로 소유한다**(문서 층 = 이 문서뿐(2026-07-26 2차 정정 — §0) · 코드 층 = `step-invoker/` · Core·프로토콜·step-host 0건). |

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
- **산출물 실재.** `framework/loop/step-host/`(step.py·events.py·bundle.py·invoker.py·host.py·config_schema.json·README.md·tests/) 와 `framework/adapters/claude/step-invoker/`(claude_invoker.py·tests/) 는 파일 시스템 실재이며, 자체 테스트는 표준 라이브러리 `unittest` 만으로 통과한다(테스트 건수 스냅샷은 drift 이므로 불기재 — 재실행이 판정 근거).
- **provider 토큰 격리(불변 주장).** `framework/loop/step-host/` 소스에 provider·실행 옵션 토큰 0건. 권한 생략 플래그 문자열의 소재 전수 결과·정정은 §0 이 소유한다(재열거 없음).
- **run 데이터 백엔드 실재(정정 2026-07-26).** `step-data/` 는 미생성이 아니다 — `runs/`(`.gitkeep` + run 디렉터리)와 `e2e/`(드라이버 run_host.py·setup_run.py·scenarios.py·replay_check.py·s4_crash_driver.py·_e2e_common.py)가 실재한다. `uaf-verified: find uahf/framework/adapters/claude/step-data -maxdepth 3 직접 열거`

---

## §7. Open Questions

- **OQ-SH-1 (CP3 물리 형태 E2E) — 해소.** CP3 = **배치 종단 일괄** 디스패치 — run 완주 후 런처가 role=Advisor fresh 세션을 별도 디스패치해 `final_verdict` 를 회수·기록한다. 물리 증거 = `step-data/runs/e2e-s1-normal/logs/cp3-result.json@cd9247b`(Pass; run 원장은 산출물 수명 정책으로 작업 트리에서 제거).
- **OQ-SH-2 (`interactive` headless 의미 — open).** headless(`-p`)에는 대화 채널이 없어 `interactive` policy 의 승인 프롬프트 의미가 불명확하다(예: 승인 필요 도구 조우 시 blocked 에스컬레이션). 현재는 "기본 실행(권한 생략 플래그 없음)"으로만 바인딩한다.
- **OQ-SH-3 (`--output-format stream-json` 채택 — open).** `json`(단일 결과) vs `stream-json`(실시간) 선택은 관찰로 확정한다. 현재 기본은 `json`.
- **자매 바인딩 OQ append — 해소(W3 정합).** loop-binding §8 OQ-LB-2 해소 표기·workflow-binding §8 OQ-WB-2 부분 해소 표기 + 각 §9 이력 행 append 완료(버전 무상승·append-only).
- **OQ-SH-4 (CP2 모델 슬롯 결합) — 해소(v1.6 Project Orchestration).** 중립 Host 에 `StepHost(cp2_model=...)` 선택 파라미터가 추가되어(기본 `None` = 기존 거동 `model=step.model` 바이트 동일·`config_schema.json` 선택 필드 `cp2_model`) CP2 검증 단위 모델을 피검증 단위와 독립 지정할 수 있다. 계약·02 §4 슬롯 의미 무변 — `project-orchestration-binding.md` §4.3 참조.
- **OQ-SH-5 (Escalation 해소 API 부재·해소=fail 계수 결합 — open, 비차단).** `Escalated` 해소에 전용 이벤트 어휘가 없어, 해소는 "파생 상태를 Failed 로 되돌리는 `outcome=fail`(ref.kind=resolved) 이벤트의 수동 append"로 실현된다(프로토콜 §4.3 의 현행 물리 형태). 이 재사용 때문에 해소 이벤트가 `prior_failures` 재시도 예산을 소모한다(W3 s3 실측 — 중복 append 가 한도를 소모해 retry-limit-exceeded 조기 유발). 전용 해소 어휘(재시도 비계수) 도입은 후속 설계 판단. 부수 관찰: E2E 드라이버(`step-data/e2e/` — Host·바인딩 아님)의 invoke 로그 파일명이 프로세스별 순번이라 재기동 시 이전 원출력 로그가 덮어쓰일 수 있다(권위 기록 events.jsonl 무영향).
