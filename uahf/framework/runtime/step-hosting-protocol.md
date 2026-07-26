# framework/runtime/step-hosting-protocol — Step 실행 호스팅 프로토콜 (형태 B)

작성일: 2026-07-13
상태: v1.5 Baseline (W1 CP2 재판정 Pass 5/0/0 · W3 E2E CP2 Pass 7/7 · CP3 승인 · 사용자 승인 2026-07-13)
상위 규약: AGENT.md
근거 정본:

- specs/00-glossary.md — 용어 정본·INV-3(Component·Layer 계수 경계).
- specs/03-loop.md §3.1-A — Lifecycle 7단계·검증 게이트 CP1/CP2/CP3·게이트-단계 매핑.
- specs/03-loop.md §3.1-B — 재작업 루프·retry_count·재시도 한도(§5.1).
- specs/03-loop.md §3.1-D — 사람 개입 5조건(§5·§6의 Escalated 정지 근거).
- specs/03-loop.md §3.2-A — 전이 이벤트 스키마·append-only 불변(§4가 동형 재사용).
- specs/03-loop.md §3.2-B — 단계 상태 5종(§4.1이 재사용하는 상태 어휘).
- specs/07-workflow.md §3.1-A·§3.2-A~D — Decompose·Work Graph/parallelSets·Task 필드·R1~R4·Merge.
- specs/02-agent.md §3.1(O4·O5)·§3.2-B·§3.2-C·§3.2-D — 위임 8필드·완료 보고·실패 보고.
- specs/06-verifier.md §3.1·§3.2-B/C·§3.2-D·§3.2-E — 독립 판정 의무·verdict 도출·재작업 지시·VT 카탈로그.
- specs/04-memory.md §3.1-B·§3.4 — Recall·소비자 계약(**Runtime은 소비자가 아니다** — §3.2).
- specs/01-runtime.md §3·§3.1-C·§3.2-B — Core Contract·Serve 구간 경계·Config 값 소유.
- discovery/specs/02-discovery.md §3.2 주 — P-D4(개입 최소)·P-D5(권한 보존) 비상충(§6.2 근거).
- planning/specs/04-solution-design.md §3.3 — 역할 할당 계약(§3.1 슬롯 값의 원천).
- framework/core/structure.md §4·§5·§7 — 실행 코드 배치 규칙(C-2)·금지 토큰 규칙(C-3)·Core Contract 불변(C-1).
- framework/runtime/lifecycle.md·module-manifest.md·module-registry.md — 자매 Core 문서(관례 관찰 대상).
- framework/adapters/<adapter>/loop-binding.md §4·workflow-binding.md §4 — 형태 B 예약 로케이터 2자리.
- `docs/form-b-step-hosting-design.md@cd9247b` — 본 프로토콜의 **설계 정본**(아카이브). 계약 정본은 위 spec·프로토콜·바인딩이 소유한다.

거버넌스: 이 문서는 `framework/runtime/` 소속 Core 문서다. 본문은 AI·언어·툴체인 비의존을 유지한다(structure.md §5 C-3). Step Host의 구체 실현(직렬화 형식·물리 실행 표면·정지 신호 값·정책 값 매핑)은 Module 구현 경계(`framework/loop/step-host/`)·Adapter Binding 문서 소관이며 본 문서는 소관 포인터만 둔다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-13 | W1 Draft | 최초 작성. 형태 B Step Execution Hosting 프로토콜 신설 — 설계 정본(docs/form-b-step-hosting-design.md) §3·§4·§5·§8을 provider-중립 계약으로 형식화. 위상 선언(§2)·Step 직렬화 축(§3.1)·Fresh Context Assembly(§3.2)·상태 파생·결정적 재개(§4)·재시도·피드백·검증 통합(§5)·Execution Readiness Clarification·Autonomy Policy·진입 모드(§6)·불변 SH-INV 8건·Adapter 바인딩 지점·실측 대조(§7). 01/02/03/06/07 Frozen spec·루트 ARCH·04 계약 재정의 0(§ 포인터 인용만), 새 상태·필드·Component 창설 0(C-1·Glossary INV-3 무촉), 본문 provider·언어·툴체인·플래그 토큰 0(C-3). | Worker (Advisor 위임, Task W1) |
| 2026-07-13 | W1 Draft r2 | CP2 재작업(F-1·O-1): cross-layer 앵커 3곳(§3.1 표·§3.1 주·§7.2 표) bare '04 §3.3' → '04-solution-design §3.3' 명시 정정 · 근거 정본 3건 등재(00-glossary·02-discovery §3.2·04-solution-design §3.3) | Worker (CP2 재작업 지시) |
| 2026-07-13 | W1 확정 | CP2 재판정 Pass(점검 5 Met·0 Violated·0 Undetermined — 1차 판정의 Fail 1[F-1]은 r2로 해소) · CP3 Advisor 승인 · 상태행 동결. Baseline 승격은 W3 사용자 게이트 유보. | Advisor |
| 2026-07-13 | W3 실증 (본문 무변경) | W2 구현·W3 dogfooding E2E 로 §7.2 소관 산출물이 전부 실재화됨 — `framework/loop/step-host/`(중립 Host·테스트 17)·`framework/adapters/claude/step-hosting-binding.md`·`step-invoker/`(테스트 19)·run 데이터 백엔드(`step-data/runs/` 8 run·E2E 7 시나리오 CP2 독립 Pass). §7.3 문면은 W1 시점 실측 스냅샷으로 보존한다(BPD-17 — 현행 실재는 본 행과 step-hosting-binding.md §6 이 기록). 본문 계약·SH-INV 무변경. | Advisor |
| 2026-07-13 | v1.5 Baseline | 마일스톤 v1.5 「형태 B Step Execution Hosting」 사용자 승인 — 기준선 확정(Baseline 승격 게이트 통과·상태행 승격). 본문 무변경. | Advisor |
| 2026-07-13 | v1.6 정합 (본문 무변경) | 프로젝트 레벨 소비자 실재 — orchestration Layer(마일스톤 v1.6·정본 `orchestration/specs/05-project-orchestration.md`)가 본 프로토콜의 중립 Host(`framework/loop/step-host/`)를 substrate로 **라이브러리 무수정 소비**한다(공유 EventStore·결정적 재개·SH-INV 전건 상속). 본문 계약·SH-INV 무변경. | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-XX·mi 유지)·삭제 산출물 참조 앵커 전환(@cd9247b·@004bfa9). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 3 — 비계약 격리 개정: 경계 중복·복제 절 포인터화·감사 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다. uaf-allow-legacy: §9 기존 행은 개정 시점의 이력 기록이므로 문면을 고치지 않고 보존한다 — W1 시점의 §7.3 미존재 스냅샷 문면도 위 W3 행이 이력으로 보존한다.)

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(다른 절에서 반복하지 않는다).

- **정본은 인용된 각 spec의 §3 계약이다.** 이 문서는 01 §3 Core Contract의 **인스턴스**이며 03/07/02/06/04의 계약(상태·전이·필드·연산·불변)을 재정의·확장하지 않는다(structure.md §7 C-1). 새 상태 열거·새 필드·새 Component·새 Layer를 창설하지 않는다(Glossary INV-3 무촉). 위반(형태 B가 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다.
- 이 문서는 **Step Host** — 03 사이클 구동과 07 디스패치·순서 규칙을 사람 없이 무인으로 트리거·반복하는 실행 코드(형태 B)의 provider-중립 계약을 서술한다.
- **Core 문서.** 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·실행 옵션 문자열)을 두지 않는다 — 규칙 정본은 structure.md §5 C-3다. Step 물리 형식·물리 실행 표면·백엔드 경로·정지 신호 값·정책 값 매핑은 Module 구현 경계(`framework/loop/step-host/`)·Adapter Binding 문서 소관이다(§7.2).
- **경계 불가침.** Runtime(01)의 Serve 구간 호스팅 계약을 재정의하지 않는다 — Step Host는 Loop Engine 구동의 형태 B 실현이며 **두 번째 Runtime이 아니다**(01 §3.1-C·INV-6). Agent Lifecycle 단계 전이 규칙은 정의하지 않는다(03 소관).
- 용어는 specs/00-glossary.md 정본만 사용한다. "형태 A / 형태 B"는 structure.md 확정 조건의 서술 라벨이며, "Step Host"·"Step Contract"는 설계 정본이 도입한 서술 명칭으로 기존 Task(07 §3.2-B)+delegation(02 §3.2-B)의 실행 시점 직렬화를 가리키는 라벨이지 새 Component가 아니다(§3.1).

---

## §1. 목적

이 프로토콜은 다섯 가지를 확정한다 — Step Host의 위상(§2) · 실행 단위 Step의 정의(§3) · 기록·상태·재개 규칙(§4) · 재시도·피드백·검증 통합(§5) · 진입 판정·자율성·진입 모드(§6). 형태 A(주 컨텍스트에서 규약으로 직접 실수행)와 **같은 계약의 두 번째 실현 형태**이며 형태 A는 그대로 유효하다. 전환에도 01/02/03/06/07 §3 Core Contract 변경은 0이다(C-1).

---

## §2. 위상 선언 — Step Host는 판단하지 않는 기계 구동자

Step Host는 **판단하지 않는 기계 구동자**다. 03 사이클 구동과 07 디스패치·순서 규칙(R1~R4·병합)을 **무인으로 트리거·반복**할 뿐 의미 판단을 하지 않는다.

- **의미 판단은 전부 기존 주체가 소유한다.** 완료·실패·차단 선언은 실행 단위(02 §3.2-C/D), 독립 검증 판정은 Verifier(06 §3.1), 최종 승인·재량 판정은 Advisor(02 §3.2-A), 사람 개입 결정은 사람(03 §3.1-D)이 소유한다. Host는 이 판단들을 오케스트레이션 순서로 배열·구동할 뿐 대신 내리지 않는다.
- **재정의 0.** Host는 01의 Bootstrap/Shutdown·Serve 호스팅 계약, 03의 단계 전이 규칙, 07의 R1~R4·병합 5단계를 재정의하지 않고 구동만 한다. Step Host는 형태 B 예약 로케이터(loop-binding §4·workflow-binding §4)가 예약한 두 자리의 실현이다.
- **두 번째 Runtime 아님·형태 A 병존.** 별도 Runtime을 신설하지 않으며(01 INV-6), 형태 A와 병렬 체계가 아니라 같은 계약의 다른 실현으로 양립한다.

---

## §3. Step 계약 — 실행 시점 직렬화 (새 계약 요소 0)

### §3.1 Step 직렬화 축

**Step**은 07 §3.2-B **Task**와 그 `delegation`(02 §3.2-B 위임 8필드)의 자기완결 직렬화다. 필요한 전 필드가 기존 계약에 실재하므로 새 필드·새 계약 요소가 0이다.

| Step에 직렬화되는 내용 | 소유 정본 (재사용) |
|---|---|
| id · task · done · interfaceContract · ownedBoundary · dependsOn | 07 §3.2-B Task 필드 그대로 |
| from · to · task · input · output · done · context · constraints | 02 §3.2-B 위임 8필드 그대로 |
| role/capability/model 슬롯 | 02 §4 실행 모델 바인딩·04-solution-design §3.3 Capability 선언 — Host는 **전달만** 하고 해석하지 않는다 |
| feedback (재시도 시에만) | 02 §3.2-D 실패 보고·06 §3.2-D 재작업 지시에서 파생(§5.1) |

- **유효성 = 착수 가능성.** Step의 유효성 검사는 02 §3.2-B의 "필드(input·output·done·context) 하나라도 누락 시 착수 불가"를 그대로 사용한다(02 INV-6). 필수 필드가 누락된 Step은 디스패치되지 않고 진입 Sufficiency 판정(§6.1)으로 넘긴다.
- **role/capability/model 슬롯은 선언의 전달자다.** 값의 원천은 기존 구조(하네스 역할 또는 04-solution-design §3.3 동적 Capability 선언)이며 Host는 전달만 한다 — 새 고정 Persona 세트·역할 카탈로그를 창설하지 않는다.
- **물리 형식은 Adapter 소관.** Step 파일의 직렬화 형식·물리 배치·필드의 물리 표현은 Adapter Binding 문서 소관이다(§7.2).

### §3.2 Fresh Context Assembly 계약

각 Step은 전체 컨텍스트를 상속하지 않고, 신규(격리된) 실행 컨텍스트에서 다음 번들만으로 실행된다.

**번들 = Step Contract(§3.1) + 확정 참조 + Memory 재료 + constraints + (재시도 시) feedback.**

- **확정 참조(R2 준수).** 번들의 참조는 input·interfaceContract가 가리키는 **확정된** 산출물뿐이다. 동시 진행 중인 다른 Step의 미완성 산출물은 추측·인용하지 않는다(07 R2·INV-4).
- **Host의 Memory 직접 접근 금지.** Host는 Memory Store·Index에 직접 접근하지 않는다 — 04 §3.4 소비자 목록에 Runtime이 없으며 Runtime은 배선만 한다(04 §3.4·INV-1, PortBypass 방지). Memory 재료는 두 경로로만 번들에 들어온다.
  - (a) **위임자(Advisor/Loop Consult 단계)가 Recall(purpose·scope·index-first — 04 §3.1-B)로 회수한 결과 요약을 Step의 `context`에 포함**(권장 기본 — 03 Consult 단계의 기존 책임 그대로).
  - (b) Step 실행 단위가 스스로 Consult 규약을 수행해 단일 Port로 Recall(04 §3.1-B 계약 준수).
- **새 Memory 체계·캐시 신설 0.** 번들 조립은 위 두 허용 경로 위에서만 성립한다.
- **반환 방향도 격리.** 격리는 유입(번들)만이 아니라 반환에도 적용된다 — Step 실행 상세·중간 기록·대량 산출물은 run 데이터 백엔드(§7.2)에 남고, 상위로는 완료 보고 5필드 수준의 요약·상태·검증 결과만 반환한다(02 §3.2-C 재사용). Host 자체는 어떤 내용도 주 컨텍스트에 누적하지 않는다(SH-INV-8).

---

## §4. 상태 모델·결정적 재개

### §4.1 상태 파생 규칙 — append-only 파생 뷰

Host의 상태는 03 §3.2-B **단계 상태 5종에 전건 흡수**된다 — 새 상태 열거 신설 0. 사용자·구현 편의의 검토 어휘는 **비정본 표기로 병기만** 한다.

| 비정본 검토 어휘 | 03 §3.2-B 상태 (정본) | 의미 |
|---|---|---|
| pending | `Pending` | 디스패치 대기(의존 미충족 포함) |
| running | `Active` | Step 실행 중 |
| completed | `Passed` | CP2 Pass 확정 후 |
| failed | `Failed` | 실패(재시도 잔여 시 재디스패치 대상) |
| blocked | `Escalated` | 사람/상위 개입 대기(03 §3.1-D) |

- **기록 = append-only 이벤트 로그.** 기록은 03 §3.2-A 전이 이벤트 스키마(cycle_id·seq·from/to·trigger·outcome·retry_count·actor·ref·at)를 **동형 재사용**한다. 기록은 append-only이며 기록된 뒤에 유효하다(03 INV-3). 이 로그만으로 재구성·검증할 수 있어야 한다.
- **현재 상태 = 로그 파생 뷰.** "현재 상태"는 별도의 mutable 상태 필드가 아니라 로그의 파생 뷰다 — 마지막 관련 이벤트가 상태를 결정한다. Host는 mutable 상태 필드를 두지 않는다.
- 전이 이벤트의 필드·의미·필수 표기의 정본은 03 §3.2-A이며 직렬화 형식·물리 표현은 Adapter Binding 소관이다(§7.2).

### §4.2 결정적 재개 규칙

크래시·중단 후 Host는 로그를 재생해 각 Task의 파생 상태를 복원하고 다음 디스패치 대상을 결정적으로 도출한다.

- **다음 대상 = "`Passed`가 아닌 Task 중 `dependsOn`이 전부 `Passed`인 최소 순번 집합".** 07 §3.2-A parallelSets 도출 규칙과 동일 논리이며 **순차 실행은 그 특수형**(집합 원소 1)이다. 같은 로그에서 항상 같은 재개 지점이 나온다.
- **`Escalated` 잔존 시 즉시 정지.** 해소되지 않은 `Escalated`가 하나라도 있으면 진행하지 않는다. 해소 이벤트가 append된 뒤에만 해당 Task가 위 규칙으로 재선택된다.
- **`Active` 잔존(중단 흔적) 처리.** 재생 결과 `Active`로 남은 채 종료된 Task는 결과가 미확정이므로 `Failed`(계기: 실행 중단) 이벤트를 append한 뒤 재시도 규칙(§5.1)을 적용한다(멱등).

### §4.3 실행 시퀀스 (4 국면)

각 국면의 상태 전이는 전부 §4.1 이벤트 로그에 append되며, 어느 국면도 검증되지 않은 결과를 완료로 기록하지 않는다.

| 국면 | 흐름 |
|---|---|
| 정상 | first-pending Task 선택(§4.2) → Step 직렬화(§3.1) → 신규 실행 컨텍스트 기동(§3.2) → Execute+CP1 → 완료 보고(5필드) 기록 → **CP2를 별도 독립 단위로 디스패치** → CP2 Pass → `Passed` append → 다음 Step |
| 실패/재시도 | CP1 실패 또는 CP2 Fail → `Failed` append(+`ref`) → `retry_count` < 한도이면 feedback 주입 재디스패치(§5.1) → 한도 초과 → `Escalated` |
| Blocked | 실행 단위의 차단 선언(O4) 또는 Clarification 필요(§6.1) → `Escalated` + 물리 정지 신호(값=Adapter 소관) → 사람/Advisor 해소 → 해소 이벤트 append → 재개(§4.2 재선택) |
| 크래시 재개 | Host 재기동 → 로그 재생 → §4.2 결정 규칙 → 이어서 실행. `Active` 잔존 Task는 `Failed`(실행 중단) append 후 재시도(멱등) |

이 4 국면은 새 상태·새 전이를 신설하지 않는다 — 전부 §4.1 상태 5종과 03 §3.2-A 이벤트 스키마 위에서 성립한다.

---

## §5. 재시도·피드백·검증 통합

### §5.1 재시도·피드백

- **재시도 조건·한도.** CP1 실패 또는 CP2 Fail 시 `Failed` 이벤트(관련 실패 보고·재작업 지시 `ref` 포함)를 append하고, `retry_count`가 재시도 한도 미만이면 재디스패치한다. `retry_count`·한도는 03 §3.1-B 소관이며 한도 값은 Config(01 §3.2-B)로 주어진다 — Host는 값의 소비자일 뿐 소유자가 아니다.
- **feedback 재주입.** 다음 fresh context(§3.2)의 feedback 슬롯에 **직전 실패 보고(02 §3.2-D — reason·repro)와 CP2 재작업 지시(06 §3.2-D)**에서 파생한 피드백을 주입한다. feedback은 append-only 로그에서 도출되며 별도 상태 시스템을 신설하지 않는다.
- **한도 초과 → Escalated.** 한도를 초과하면 `Escalated`로 정지한다(03 §3.1-D 조건 1). 실패·미완성은 로그와 보고에 반드시 남으며 은폐되지 않는다(02 O5·INV-5).

### §5.2 검증 통합 — CP1/CP2/CP3 보존 + AC 3형

검증 게이트 순서(CP1 → CP2 → CP3)는 03 §3.1-A가 소유하며 Host는 그 순서를 구동만 한다.

- **CP1 — 자체 점검.** Step 실행 단위가 Execute 종료 시 수행한다(02 §3.2-C self_check; 실행형 AC의 기계 실행 포함). 자체 점검은 최종 승인이 아니다(02 §3.2-A).
- **CP2 — 독립 판정.** Host는 CP2를 **별도 독립 실행 단위**(Verifier 역할)로 디스패치한다. 산출물 자체를 근거로 판정하며 완료 보고를 판정 근거로 삼지 않는다(06 §3.1 V1). **자가판정으로 완료를 확정하지 않는다** — CP1과 CP2는 같은 단위가 겸하지 않는다. `Passed` 이벤트는 CP2 Pass 확정 후에만 append된다.
- **CP3 — Advisor 역할 승인.** CP3는 사람 승인이 아니라 **Advisor 역할의 승인**(02 §3.1)이므로 무인 실행과 양립한다. Host는 사이클 Complete 전(또는 배치 종단에서 일괄) Advisor 역할 단위에 CP3를 디스패치한다. 06 거짓 완료 검출·final_verdict 도출 규칙은 그대로다.

**AC 3형** (06 무수정 — done 필드의 유형 표기 관행이며, 모든 AC를 실행형으로 강제하지 않는다):

| AC 유형 | 판정 물리화 | 06 대응 |
|---|---|---|
| 실행형(Executable) | 기계 실행 커맨드 — CP1에서 실행 단위가 실행하고 CP2가 재실행·재확인 | VT-2·VT-5의 물리화 |
| 독립 검토형(Review) | 독립 판정 단위의 검토로 판정 | VT-1~VT-5 그대로 |
| 사람 검토형(Human Review) | `Escalated` 게이트로 물리화(사람 해소 대기) | 03 §3.1-D 조건 5 |

(독립 검토형의 판정 단위가 어떤 provider·모델로 실현되는가는 Adapter Binding 소관이다 — §7.2.)

---

## §6. 진입 판정·자율성·진입 모드

### §6.1 Execution Readiness Clarification

기존 앵커(02 §3.2-B 착수 거부 · 02 O4 추측 금지 · 03 §3.1-D 사람 개입 5조건 · 상위 UAF 게이트 P-D4/P-D5)의 **명명·정식화 + Step Host의 blocked 신호와의 접속**이다. 새 Engine을 신설하지 않으며 3지점에서 작동한다.

- **진입 Sufficiency 판정.** 위임/Step 필드의 완전성을 검사한다 — 02 §3.2-B가 곧 판정 기준이다. 완전 → 즉시 Implementation Planning(03 Plan). 불완전 → 부족 필드를 지목한 **최소 범위 scoped 질의**로 위임자/사용자에게 반환한다. Discovery 전체 재실행을 하지 않는다.
- **실행 중 scoped 질의·blocked.** 실행 단위가 O4에 따라 차단을 선언하면(실패 보고 `blocking=차단됨`, 02 §3.2-D) Host는 `Escalated` 기록 + 물리 정지 신호(값은 Adapter 소관)로 정지한다. scoped question을 기록에 남기고 해소 후 재개한다(§4.2).
- **upstream 급 부족 → 명시적 Discovery 호출 fallback.** 무엇을 만들지 자체가 불명일 때는 추측으로 우회하지 않고 부족한 upstream 산출물을 명시적으로 획득하는 **Discovery Capability 호출 fallback**(게이트 통과 후)을 사용한다 — 중복 Interview가 아니다.

### §6.2 Autonomy Policy 어휘·게이트 등급 분리

- **정책 어휘(Policy as Data).** `interactive`(도구 실행 승인 프롬프트 유지) / `auto_approve`(선언된 허용 범위 내 자동 승인) / `unrestricted`(승인 프롬프트 전면 생략) 3값. 정책 값은 **데이터**이며 엔진·계약 무변경으로 조정된다. 실값·provider 실행 옵션 매핑은 Adapter/정책 데이터 소관이다(§7.2, 01 §3.2-B).
- **게이트 등급 분리(불가침).** 위 정책은 **도구 실행 승인 프롬프트 축만** 제어한다. **Human Decision Gate — Contract 변경·중대 Architecture Decision·파괴적 작업·해결 불가 불확실성(= 03 §3.1-D 조건 2~5 + UAF 레벨 게이트) — 는 어떤 policy 값에서도 `Escalated` 정지로 보존**된다. `unrestricted`에서도 이 게이트는 정지하며 CP2를 우회하지 않는다. 정본 근거: 개입 최소(P-D4)와 권한 보존(P-D5)은 상충하지 않는다(02-discovery §3.2 주).

### §6.3 Full UAF / Standalone 진입 시퀀스

Planning·실행 단계는 두 모드가 동일하며(03 Plan → 07 Decompose → Step 직렬화 → Host 구동) **차이는 진입 판정과 중복 실행 금지 규칙**에 있다.

| 국면 | Full UAF Mode | Standalone UAHF Mode |
|---|---|---|
| 입력 | 상위 산출물(Contract·상위 설계 산출) — **재사용, 재생성 금지** | 사용자 제공 입력(Contract·요구사항·기존 프로젝트·위임) |
| 진입 판정 | Consult 정독 후 즉시 Implementation Planning | Sufficiency 판정(§6.1): 충분 → 즉시 Planning / 불충분 → 최소 Clarification / upstream 부족 → 명시적 Discovery fallback(게이트 후) |
| 금지 | 상위 Interview·상위 Plan 재수행·재생성 | 무조건적 전체 Discovery 재실행 |

**중복 실행 금지 규칙.** Full UAF Mode는 상위 산출물을 재사용하며 상위 Interview/Plan을 재생성하지 않는다. Standalone UAHF Mode는 부족분에 한한 최소 Clarification만 수행한다. 두 규칙 모두 이벤트 로그에 상위 단계 재실행 흔적이 남지 않아야 한다.

---

## §7. 불변 SH-INV · Adapter·구현 바인딩 지점 · 실측 대조

### §7.1 불변 SH-INV

아래 불변은 이 프로토콜이 준수를 서약하는 Host 의무이며 **전부 기존 정본 계약의 파생**이다. 새 Core Contract·새 상태·새 필드·새 Component를 창설하지 않는다(C-1·Glossary INV-3 무촉).

- **SH-INV-1 (판단 금지).** Host는 의미 판단(완료/실패/차단/검증/승인)을 0건 수행한다. 판단은 전부 기존 주체 소유다(§2; 02 §3.2-A, 06 §3.1, 03 §3.1-D).
- **SH-INV-2 (append-only 파생 뷰).** 기록은 append-only 이벤트 로그이며, 현재 상태는 그 로그의 파생 뷰다. mutable 상태 필드를 두지 않는다(§4.1; 03 §3.2-A INV-3).
- **SH-INV-3 (결정적 재개).** 동일 로그는 항상 동일 재개 지점을 낸다(§4.2; 07 §3.2-A parallelSets 도출 논리).
- **SH-INV-4 (게이트 보존).** 어떤 policy 값에서도 Human Decision Gate는 `Escalated` 정지로 보존되며 CP2를 우회하지 않는다(§5.2·§6.2; 03 §3.1-D 조건 2~5, 06 V1, P-D4/P-D5).
- **SH-INV-5 (Memory 직접 접근 금지).** Host는 Memory Store·Index에 직접 접근하지 않는다 — 두 허용 경로만 경유한다(§3.2; 04 §3.4 Runtime 비소비자·INV-1).
- **SH-INV-6 (Core Contract 무변).** 이 프로토콜은 01/02/03/06/07 §3 계약을 구현만 하고 재정의 0이다(§0·§1; structure.md §7 C-1).
- **SH-INV-7 (provider·언어 중립).** 본 문서 본문과 중립 엔진 경계(`framework/loop/step-host/`)에 특정 AI·모델·제품 기능·언어·툴체인·실행 옵션 토큰이 0건이다(§7.2·§7.3; structure.md §5 C-3).
- **SH-INV-8 (컨텍스트 격리).** 각 Step은 전체 컨텍스트를 상속하지 않고 번들만으로 실행되며, 상위로는 완료 보고 5필드 수준의 요약·상태·검증 결과만 반환한다(§3.2; 02 §3.2-C, 07 R2).

### §7.2 Adapter·구현 바인딩 지점 (본 문서 미확정 — 소관 포인터)

아래 지점은 본 프로토콜이 계약만 두고 값·물리 실현을 미루는 자리다. 정확한 값·형식·경로·매핑은 지정된 경계가 소유한다.

| 바인딩 지점 | 소관 경계 |
|---|---|
| 중립 Step Host 엔진 배치(host 코드 + configSchema) | `framework/loop/step-host/`(loop-binding §4 형태 B 로케이터가 예약한 1순위 자리; structure.md §4 규칙 2). provider·언어·옵션 토큰 0 유지(C-3 확장). |
| invoker 인터페이스의 provider 구현 | `framework/adapters/<adapter>/step-invoker/`(AI·실행 환경 의존 격리 — structure.md §4 규칙 4). |
| Step 직렬화 형식·이벤트 로그 직렬화 형식 | Adapter Binding 문서 소관(직렬화 형식명은 Core 문서에 0). |
| run 데이터 백엔드 경로 | 이원화 — 일반 관례 = 소비 프로젝트 관례 경로 / dogfooding = `framework/adapters/<adapter>/step-data/`(워크스페이스 귀속). |
| 물리 정지 신호 값 | Adapter Binding 문서 소관(§6.1 blocked·정지의 물리 값). |
| Autonomy Policy 실값·provider 실행 옵션 매핑 | Adapter/정책 데이터 소관(§6.2 — 실행 옵션 문자열은 해당 바인딩에만 등장). |
| role/capability/model 슬롯의 실행 모델 지정 의미 | 02 §4 실행 모델 바인딩·04-solution-design §3.3 소관(Host는 전달만 — §3.1). |

non-core 실행 경계 사이의 정확한 분할은 structure.md §4 규칙 4가 "형태 B 설계 시 확정"으로 미룬 자리이며, 위 표가 그 확정분(step 실행 호스팅 축)이다.

### §7.3 실측 대조 (현행)

본 문서는 **계약만** 확정하며 실행 코드·데이터를 소유하지 않는다. §7.2가 가리키는 산출물의 현행 실측 상태는 다음과 같다.

- `framework/loop/step-host/`(중립 Host + `config_schema.json` + `tests/`)와 `framework/adapters/<adapter>/step-invoker/`, run 데이터 백엔드(`step-data/`)는 **실재한다** — W2 구현·W3 dogfooding E2E로 생성되었고(§9 W3 행) 이후 orchestration Layer가 중립 Host를 substrate로 무수정 소비한다(§9 v1.6 행). uaf-verified: 디렉터리 목록 실측(`framework/loop/step-host/` 및 adapters 하위 `step-invoker`·`step-data` 엔트리 존재 확인, 2026-07-26).
- 종전 W1 시점의 "미존재" 스냅샷 문면은 §9 W3 행이 이력으로 보존한다(BPD-17) — 라이브 본문은 현행 실재를 기술한다(미존재를 실재로 쓰지 않는 원칙의 반대 방향 적용: 실재를 미존재로 남기지 않는다).
- 계약·SH-INV 문면은 이 실재화로 변경되지 않는다. provider·언어 토큰 0(C-3)의 판정 대상은 중립 엔진 경계이며 그 검증은 CP2 소관이다.
