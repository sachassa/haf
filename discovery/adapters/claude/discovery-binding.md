# discovery/adapters/claude/discovery-binding — Claude Code Project Discovery Adapter 바인딩

상태: 현행 · discovery 레이어 Claude 어댑터 바인딩 (자기 홈 `discovery/adapters/claude/`)
상위 규약: AGENT.md
근거 정본: `discovery/specs/02-discovery.md` §3(전문 — 특히 §3.3·§3.5·§3.6·§3.7·§3.9~§3.16·DISC-INV 1~9)·§4.1(표 4행 D1~D4)·§4.2(4불릿 + Module부 문단 D5·D6)·§5 · `ARCHITECTURE.md` §7.1·§8(UAF-INV)·§11(확장 포인트 경계)·§12.2 · `planning/adapters/claude/contract-binding.md` §3·§4.2·§6(Provenance 내부 형식을 본 문서로 명시 위임 — DP-X6) · `entry/adapters/claude/entry-binding.md` §5.1·§5.3(기록 백엔드 트리를 본 문서로 명시 위임 — DP-X8) · `uahf/framework/adapters/claude/memory-binding.md`(백엔드 격리 트리·형태 A/B 정직 구분 선례) · `uahf/framework/adapters/claude/loop-binding.md` §3.3·§5.2(사람 개입 채널·`at` 순서 값 관례) · `uahf/framework/core/structure.md` §2·§4·§5·§7 · `uahf/specs/03-loop.md` §3.2-A(append-only 로그 관행) · `uahf/specs/00-glossary.md`. 계약 요소는 § 포인터로만 인용하며 재정의·확장하지 않는다.

---

## §0. 이 문서의 위치와 정본 경계

- **바인딩 대상 정본 = `discovery/specs/02-discovery.md` §3·§4.** 본 문서는 그 계약(Compiler 프레이밍·State Machine·Event Model 15·Termination·Execution Ready 판정·DISC-INV 1~9·Module Structure·Strategy Provider Interface·Dimension·Confidence·Adaptive Discovery·Question Budget·Discovery Policy·Metrics)의 **환경 실현 매핑**이며 재정의·확장하지 않는다. 본 문서가 확정하는 것은 02 §4.1·§4.2가 Adapter 소관으로 미룬 물리 실현 — **D1 Event 로그 직렬화·D2 사용자 확인/UserOverride 채널·D3 증거 스캔/프레이밍·D5 Policy 값 데이터 소스·직렬화·D6 Evidence Store 물리 저장(= D1)** — 과 선행 위임 **DP-X6 Provenance 내부 형식·DP-X8 백엔드 트리**다. **D4 Strategy 실행 호스팅은 역할 추상까지만** 확정하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE §11).
- **격리 지점(C-3 비적용).** 이 경계는 구체 직렬화 형식·물리 경로(`discovery/adapters/claude/…`·`uahf/framework/adapters/claude/discovery-data/…`)·파일 확장자·Policy 수치 토큰의 사용이 허용되는 자리이며 그 격리가 존재 이유다(structure.md §2·§5·자매 contract-binding.md §0·entry-binding.md §0·memory-binding.md §0 동형). UAF 정본이 명명하지 않은 것을 UAF 정본 문면인 것처럼 서술하지 않는다 — 물리 확정은 전부 본 문서 소유다.
- **형태 A/B 구분.** 본 문서 바인딩은 실행 코드 0이다 — State Machine(02 §3.3)·모듈(02 §3.9)·레퍼런스 Provider(02 §3.10-C)는 규약 절차·규약 역할로 실현되며 주 세션이 실수행한다(D-v1.2-1). 매핑은 물리 실재 / 규약 확정 문면(형태 A) / 실행 코드 도입 시 로딩 지점(형태 B)을 정직하게 구분하며, 전환에도 02 §3 계약 변경은 0이다(structure.md §7 C-1).
- **경계 분담 해소.** **DP-X6** = contract-binding §6이 미룬 Provenance 컨테이너 **내부 형식**을 §10이 확정한다(planning/specs/03 §3.2-D 불투명 계약 유지). **DP-X8** = entry-binding §5.3이 미룬 Discovery Request 기록 **백엔드 트리 위치**를 §4가 확정한다(직렬화 형식은 entry-binding §5.1 소유). 두 해소 모두 선행 바인딩의 계약 표면을 침범하지 않는다. "실재/미존재" 주장은 파일 시스템 확인 후에만 기입한다(L-07·§13). 02가 소유하는 계약 용어는 재정의하지 않으며 새 계약 요소·새 UAHF 용어를 신설하지 않는다.

---

## §2. 02 §4.1·§4.2 바인딩 지점 6건 물리 실현 (done 2)

"02 바인딩 지점" 열은 정본 표현을 그대로 인용한다. "물리 실현" 열이 본 문서 확정분, "실재 여부" 열이 물리 실재 / 규약 실현(형태 A) / 형태 B 구분이다(§13 실측 대조).

| # | 02 §3 계약 요소 (정본 §) | 02 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| **D1** | Event 로그 직렬화 (§3.5, §4.1 행1) | "append-only Event 기록의 저장 형식·위치." | Event 15종을 담는 append-only 로그 = 자기서술 구조화 레코드(1 Event = 1 레코드)·위치 `uahf/framework/adapters/claude/discovery-data/events/<mode>-<run-id>/`. 순서 값 ↔ 물리 생성 시각 성격 구분(L-09). 상세 §3. | 형식·위치 확정(정본, 형태 A). `discovery-data/events/` = 실재(§13 실측). 로거·직렬화기 = 형태 B. |
| **D2** | 사용자 확인·`UserOverride` 채널 (§3.3 Validating·§3.6, §4.1 행2) | "사용자 승인/수정/강제 응답을 받는 개입 채널." | 주 세션 사용자 제시·응답 수령 채널(loop-binding §5.2 동형) — G1 Eliciting 질문/답변·G2 Validating 승인/수정·UserOverride 강제 구분. 각 개입은 Event로 기록(§3.5). 상세 §5. | 채널 확정(정본, 형태 A). 무인 자동 트리거 = 형태 B. |
| **D3** | Contextualizing 증거 스캔·프레이밍 (§3.3, §4.1 행3) | "Greenfield 프레이밍·Brownfield 증거 스캔의 물리 구현·증거 소스 접근." | Greenfield 프레이밍 / Brownfield 실 저장소 스캔(T2, 파일 시스템 실측) / Incremental 기존 Contract 결속의 형태 A 물리 절차(주 세션 수행·Evidence Store 기록). 상세 §6. | 절차 확정(정본, 형태 A). 스캔 로더 = 형태 B. |
| **D4** | Strategy 실행 호스팅 (§3.1 Front-end, §4.1 행4) | "Discovery 실행을 어느 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE.md §11)." | 주 세션(Advisor)이 Orchestrator 역할(§3.9)을 규약 절차로 수행·레퍼런스 Provider(§3.10-C)를 규약 역할로 실현. **물리 호스팅(실행 코드·자동 실행)은 설계 0**(ARCHITECTURE §11 정합). 상세 §7. | 역할 추상 확정(정본, 형태 A). 물리 호스팅 = **설계 안 함**(확장 포인트). 실행 코드 = 형태 B. |
| **D5** | Question Budget 예산·Discovery Policy 정책 값 데이터 소스·직렬화 (§3.14·§3.15, §4.2 Module부 문단) | "Question Engine의 예산·Discovery Policy의 정책 값(임계값·예산·경계 수치)의 **데이터 소스·직렬화**는 Adapter 소관이다(§3.14·§3.15)." | `uahf/framework/adapters/claude/discovery-data/policy/` 데이터 파일 형식 + **E2E 구동용 최소 실값 1세트 정본 값 표**(차원 임계·Budget 총량/차원별·soft/hard·종료 규칙·충돌 게이트). Policy as Data — 값 조정 = 데이터 정정(엔진·계약 무변경). 상세 §8. | 형식·값 정본 문면 확정(정본, 형태 A). 물리 정책 데이터 파일 = 실재(프로파일 2종 — `policy/default-policy.yaml`·`policy/lightweight-policy.yaml`·§8.3·§13 실측). |
| **D6** | Evidence Store 물리 저장 (§3.9, §4.2 Module부 문단) | "Evidence Store의 물리 저장은 위 Event 로그 직렬화 바인딩과 **동일하다**(§3.9)." | Evidence Store의 물리 저장(증거 레코드 + Event 로그) = **D1과 동일 백엔드** `uahf/framework/adapters/claude/discovery-data/events/<mode>-<run-id>/`. 증거는 `EvidenceRecorded` Event 페이로드로 append. 상세 §3·§4. | D1과 동일(정본, 형태 A). 02 §4.2 문면 "동일하다"대로 별도 백엔드를 창설하지 않음. |

- 위 6행은 02 "### 4.1" 표 4행(D1~D4)과 "### 4.2" Module부 문단의 물리 실현 대상 2지점(D5·D6)이다. Module부 문단의 나머지 지점(Strategy Provider 실행 호스팅 — 역할 추상까지만, §3.10)은 §4.1 행4와 동일 지점이므로 D4로 통합해 다룬다(중복 창설 방지). 각 행의 물리 실현은 정본 표현을 이 환경의 구체 형식·경로·채널·값으로 좁힌 것이며 새 바인딩 계약을 창설하지 않는다.
- 02 §4.1·§4.2에 없는 계약 요소(§3.3·§3.5·§3.6·§3.7·§3.8·§3.9·§3.10·§3.15)는 이식 시에도 유지되는 것이며 본 문서가 바인딩하지 않는다(§12). 진위 판정 기준은 02 §3이다.

---

## §3. D1 — Event 로그 직렬화 확정 (done 3)

02 §4.1 행1의 물리 실현. Event Model(02 §3.5)·상태 전이(02 §3.3)·불변(DISC-INV-1·3)은 § 포인터 인용이며 물리 직렬화 형식·위치만 확정한다.

### §3.1 Event 15종 (02 §3.5 정본 재실측 열거 — 재정의 0)

append-only 로그가 담는 Event는 02 §3.5의 **정확히 15종**이다(정의·의미는 02 §3.5 소유):

`DiscoveryStarted` · `ContextCaptured` · `QuestionAsked` · `AnswerReceived` · `EvidenceRecorded` · `ConfidenceUpdated` · `BudgetConsumed` · `DimensionSaturated` · `AssumptionRecorded` · `ValidationRequested` · `UserOverride` · `ContractCompiled` · `ExecutionReadyDeclared` · `DiscoverySuspended` · `DiscoveryAborted` (계 15).

- **모든 전이는 Event로만.** 모든 상태 전이는 위 15 Event로만 일어나며 기록되지 않은 전이는 없다(DISC-INV-1·3, 02 §3.3 — 재정의 0).

### §3.2 확정 — 자기서술 구조화 레코드 append-only 로그 (1 Event = 1 레코드)

**한 Discovery run 1건의 Event 로그 = 발생 순서대로 append되는 자기서술 구조화 레코드의 로그**로 직렬화한다. **1 Event = 1 레코드**이며 레코드는 발생 순서대로만 추가된다(append-only, DISC-INV-3). 자매 바인딩의 append-only 로그 관례(loop-binding §3·memory-binding §2)와 동형이며 구체 구조화 데이터 형식은 Adapter 선택이다(격리 지점 — 이식 교체 §12).

- **레코드 최소 표면.** 각 레코드는 최소한 (i) **Event 종류**(§3.1의 15종 중 하나), (ii) **순서 값**(§3.3), (iii) **Event별 페이로드**를 담는다. 페이로드 내부 구조는 이 직렬화가 해석하지 않는 불투명 페이로드로 담긴다 — Event의 의미·유발 Guard는 02 §3.3-B·§3.5 소유다.
- **append-only 불변(DISC-INV-3).** 기록된 레코드는 재작성·삭제하지 않는다. 정정·후속 상태는 새 레코드 append로 표현된다 — `DiscoverySuspended`(T24) 후 재개, `UserOverride`(T21~T23) 강제, 재작업 재진입(T17)도 각각 하나의 레코드로 append된다(02 §3.3-B·§3.5).
- **"기록만으로 run 재구성".** 로그의 레코드 순서(= append 순서 = 전이 순서)만으로 그 run의 State Machine 진행(`Initiated` → 전이 → 종단)이 재구성된다. Metrics는 이 Event 로그에서만 파생된다(DISC-INV-4·02 §3.16 — 본 문서는 로그 물리 표면만 확정하고 산식을 정의하지 않는다).

### §3.3 순서 값과 물리 생성 시각의 성격 구분 (L-09)

- **순서 값(정본 표면).** 각 레코드는 단조 증가하는 **순서 값**을 갖고, 이 값이 로그 내 레코드 순서(= 전이 순서)를 확정한다. 로그의 순서는 언제나 이 순서 값(= append 순서)에서 도출되며 벽시계 시각에서 도출하지 않는다(loop-binding §3.3 `at` 관례 동형).
- **물리 생성 시각(별도 필드·실측 성격).** 레코드가 벽시계 생성 시각을 담는 경우 그것은 **순서 값과 별개 필드**이며 그 값의 진위는 실측 대조 후에만 참으로 취급되는 측정 주장이다(L-09). 물리 생성 시각은 로그의 순서를 결정하지 않는다 — 순서 결정은 순서 값 전속이다. 따라서 시각 필드의 부재·오차가 로그의 순서 정합(전이 재구성)을 훼손하지 않는다.

### §3.4 위치 — run 단위 격리

- **위치.** 한 Discovery run의 Event 로그는 `uahf/framework/adapters/claude/discovery-data/events/<mode>-<run-id>/` 아래에 둔다. `<mode>` = Discovery Request의 mode(greenfield/incremental/brownfield 등·ARCHITECTURE §12.2 확장 네임스페이스), `<run-id>` = 해당 run(= Discovery Request 결속으로 생성된 State Machine 인스턴스·02 §3.3-A)의 식별자. run 단위 디렉터리로 격리해 서로 다른 run의 로그가 섞이지 않게 한다.
- **레코드 파일 단위·명명(Adapter 재량).** run 디렉터리 내 단일 append-log 파일인지 레코드 단위 파일인지의 세부와 명명은 Adapter 재량이며(승인 계획 위임), 어느 경우에도 §3.2 append-only·§3.3 순서 값 성격은 유지된다. 물리 명명·샤딩 등 규모 대응은 형태 B/규모 사안으로 미룬다.
- **D6 정합(Evidence Store = 동일 백엔드).** Evidence Store(02 §3.9)의 물리 저장은 이 Event 로그 백엔드와 **동일**하다(02 §4.2 Module부 문단). 증거는 `EvidenceRecorded` Event 페이로드로 같은 run 디렉터리 로그에 append되며 별도 증거 백엔드를 창설하지 않는다.

---

## §4. discovery-data/ 백엔드 트리 정본 선언 (done 4 · DP-X8 해소)

Discovery의 물리 백엔드 데이터 위치를 **Adapter 경계 이하 `uahf/framework/adapters/claude/discovery-data/`로 확정한다**(자매 memory-binding §0 memory-data/·loop-binding §0 loop-data/ 격리 선언 동형). 이 위치는 Core 경계(`uahf/framework/core/`·`uahf/framework/runtime/`)·`specs/`·`docs/`·라이브 `.claude/` 규약 표면 **밖**이며, 발견 산출 데이터가 하네스 규약·Core와 혼입되지 않도록 격리한다(UAF-INV ① 안전·contract-binding §4.2 격리 근거 동형). **트리 구조·경로·형식·값은 본 문서 소유 정본이며, 물리 위치는 2차 산출물 디커플링 트랙에서 확정한다**(현행 실재 상태 = §13 실측·L-07).

### §4.1 백엔드 트리 (정본 문면)

```
uahf/framework/adapters/claude/
└─ discovery-data/                          # ★ Discovery 백엔드 격리 루트 (물리 위치는 2차 산출물 디커플링 트랙에서 확정)
   ├─ events/                               # D1·D6 — run 단위 append-only Event 로그 + 증거(Evidence Store 물리 저장 = 동일 백엔드)
   │  ├─ greenfield-<run-id>/               #   Greenfield run 1건의 Event 로그 디렉터리
   │  │  ├─ <Event 로그 레코드…>            #     자기서술 구조화 레코드(1 Event = 1 레코드, append-only; §3)
   │  │  └─ <Discovery Request 기록>        #     이 run의 Discovery Request({mode,inputs,policy}) — 형식은 entry-binding §5.1 소유(DP-X8 해소, §4.2)
   │  ├─ brownfield-<run-id>/               #   Brownfield run 1건의 Event 로그 디렉터리(동일 구조)
   │  └─ …                                  #   run 단위 격리(<mode>-<run-id>/)
   ├─ policy/                               # D5 — Discovery Policy 데이터 파일(임계·예산·종료 규칙·충돌 게이트; 형식·값 정본 = §8)
   ├─ contracts/uahf/                       # contract-binding §4.2 정본 — 본 저장소 Contract 인스턴스 격리(참조 인용·재정의 0)
   │  └─ project-contract.v<N>.md           #     (직렬화·저장 위치 정본 = contract-binding §3·§4)
   └─ e2e-greenfield-project/               # DP-X3 — E2E Greenfield 대상 프로젝트(발견 대상)
```

- **`events/`(D1·D6, §3).** run 단위 append-only Event 로그와 증거(Evidence Store 물리 저장)를 보관한다. 위치·형식 정본은 §3.
- **`policy/`(D5, §8).** Discovery Policy 데이터 파일(임계값·예산·soft/hard 경계·종료 규칙·충돌 게이트)을 둔다. 형식·E2E 최소 실값 정본은 §8. Policy as Data이므로 값 조정은 데이터 정정일 뿐 엔진·계약 무변경이다(02 §3.15).
- **`contracts/uahf/`(참조 인용 — 재정의 금지).** 본 저장소 dogfooding Contract 인스턴스의 격리 배치 경로·파일명은 **contract-binding §4.2가 소유한 정본**이다. 본 문서는 트리 완결성을 위해 참조 인용만 하며 Contract 직렬화·저장 위치·버저닝을 재정의하지 않는다.
- **`e2e-greenfield-project/`(DP-X3).** E2E Greenfield 시나리오의 대상 프로젝트다. 이 디렉터리의 물리 생성·내용은 E2E Task 소관이며 본 문서는 트리 위치만 선언한다(§13 실측 — 현재 미실재).

### §4.2 Discovery Request 기록 위치 확정 (DP-X8 해소 — entry-binding §5.3 위임)

entry-binding §5.3은 Discovery Request의 물리 기록이 놓일 **백엔드 트리 위치**를 본 문서 소관으로 명시 위임했다(직렬화 형식·전달 방식은 entry-binding §5.1·§5.2 소유). 본 문서가 그 위치를 확정한다:

- **위치.** 한 run의 Discovery Request 기록({mode, inputs, policy} 자기서술 구조화 레코드·entry-binding §5.1)은 **그 run의 Event 로그 디렉터리(`.../discovery-data/events/<mode>-<run-id>/`) 안에 함께** 기록한다. Discovery Request는 그 run(= State Machine 인스턴스·02 §3.3-A)을 결속·생성하는 입력이므로 run의 시작 기준선으로 run 디렉터리 루트에 둔다.
- **소유 경계.** 본 문서는 **위치만** 확정하고 **직렬화 형식**은 entry-binding §5.1이 소유한다(재정의 0). 이로써 entry-binding §5.3이 미룬 백엔드 트리 지점이 해소된다.

### §4.3 물리 데이터 생성 주체 (L-07)

`discovery-data/` 트리·형식·값은 본 문서가 확정한 **정본 문면(형태 A)**이며, 실제 디렉터리·데이터 파일 생성은 **E2E·실 run Task 소관**이다(memory-binding §2 "지원 구조 — 시연 시 생성" 선례 동형). 본 문서는 물리 데이터 자산을 생성하지 않고 경로·구조·형식의 정본만 소유한다. 현행 실재 상태 = §13.

---

## §5. D2 — 사용자 확인·UserOverride 채널 확정 (done 5)

02 §4.1 행2의 물리 실현. State Machine의 사용자 개입 상태·전이(02 §3.3 Validating·§3.6·P-D5)와 관련 Event(02 §3.5)는 § 포인터 인용이며 물리 개입 채널만 확정한다. **loop-binding §5.2 사람 개입 물리 채널이 선행 관례이며 본 절은 그와 동형이다.**

### §5.1 물리 채널 — 주 세션 사용자 제시·응답 수령

- **제시·수령 채널.** Discovery의 모든 사용자 개입(질문 제시·확인 요청·승인/수정/강제 응답 수령)은 **주 세션**(Advisor 바인딩 — `.claude/CLAUDE.md`)에서 사용자에게 제시되고 응답이 수령된다. 주 세션은 Orchestrator 역할(§7·02 §3.9)을 규약 절차로 수행하는 주체이기도 하므로 State Machine 구동과 사용자 개입 제시가 같은 채널에서 정합한다.

### §5.2 개입 지점 3구분 (G1 Eliciting · G2 Validating · UserOverride)

| 개입 지점 | 물리 채널 (이 환경 확정) | 대응 Event (02 §3.5) · 전이 (02 §3.3-B) |
|---|---|---|
| **G1 — Eliciting 질문/답변** | 주 세션이 적응 질문을 사용자에게 제시하고 답변을 수령한다(Eliciting 적응 질문 루프). | `QuestionAsked`(제시, T4 self) · `AnswerReceived`(응답 수령, T5 self) |
| **G2 — Validating 승인/수정** | 주 세션이 종합된 이해·가정·미해결 질문을 사용자에게 제시하고 승인/수정 응답을 수령한다(확정 게이트, P-D5). | `ValidationRequested`(확인 요청, T14 Synthesizing→Validating) · `AnswerReceived`[승인](T16 →Compiling) / [수정 요청](T17 →Eliciting) |
| **UserOverride — 사용자 강제** | 주 세션이 사용자의 강제 지시(일시중단·종료·에스컬레이션)를 수령해 State Machine에 반영한다. 사용자는 임의 비종단 상태에서 강제할 수 있다(P-D5). | `UserOverride`(T21 일시중단→Suspended / T22 종료→Aborted / T23 에스컬레이션→Escalated) |

- **확정 게이트 = 사용자 승인(불가침).** G2의 사용자 승인은 Execution Ready 확정 게이트다 — 사용자 승인 없이 `Ready`·`ReadyWithAssumptions` 종단에 도달하지 못한다(02 §3.7 2축 판정의 사용자 승인 축·DISC-INV-6·ARCHITECTURE §8 UAF-INV ⑤). 본 채널 바인딩은 게이트를 물리 채널로 실현할 뿐 판정식을 재정의하지 않는다.
- **개입 기록.** 각 사용자 개입 발생은 D1 로그(§3)에 위 대응 Event 레코드로 남는다(DISC-INV-1·3). 무인 자동 개입 트리거·자동 제시 UI는 형태 B다.
- **충돌·모호 입력 게이트 정합.** Discovery Request의 충돌·모호 입력에 대한 사용자 확인 게이트(Discovery Policy 충돌 게이트 정책, §8·02 §3.15)도 이 D2 채널(G2 계열 제시)로 실현된다 — 게이트 통과 없이 진행하지 않는다(P-D5).
- **제시 형식(가독성·구조화).** G1 질문 제시는 추천 답을 **구조화 선택지**로 렌더하고(멀티 선택 가능·'기타(직접)' 항상 포함), 종합·구간 recap은 **시각 형식**(표·흐름·근거 등급 배지)으로 제시한다(프로즈·포인터 나열 지양). G2 사용자 승인은 **명시 최종 확정** 행위로 받는다(승인 전 미확정 — DISC-INV-6). 이는 제시 채널(형태 A)의 물리 실현이며 판정식·출력 계약(02 §3.7·§3.10-B)을 재정의하지 않는다.

---

## §6. D3 — 증거 스캔·프레이밍 물리 실현 (done 6)

02 §4.1 행3의 물리 실현. Contextualizing 상태의 mode 분기(02 §3.3-A)와 수렴(T2 self·T3 →Eliciting)은 § 포인터 인용이며 물리 절차·증거 소스 접근만 확정한다. **모든 절차는 형태 A** — 주 세션이 Orchestrator 역할(§7)로 수행하고 산출 증거를 Evidence Store(= D1 백엔드·§3)에 `EvidenceRecorded` Event로 기록한다.

### §6.1 mode 분기별 물리 절차 (02 §3.3-A Contextualizing)

| mode | 물리 절차 (형태 A — 주 세션 수행) | 대응 (02 §3.3-A·§3.3-B) |
|---|---|---|
| **Greenfield** | 선재 산출물이 없으므로 **신규 문맥을 프레이밍**한다 — 프로젝트 맥락·범위를 신규로 구성하고, 실질 증거는 이어지는 Eliciting 적응 질문(§5 G1)으로 수집한다. | Greenfield 프레이밍 완료 → `ContextCaptured`(T3) → Eliciting |
| **Brownfield** | 워크스페이스의 **실 저장소 기존 산출물을 파일 시스템으로 스캔**해 증거를 수집한다(증거 소스 접근 = 파일 시스템 실측). 스캔 증거는 `EvidenceRecorded`로 기록된다. | Brownfield 증거 스캔 진행 → `EvidenceRecorded`(T2 self) → 스캔 완료 시 `ContextCaptured`(T3) → Eliciting |
| **Incremental** | **기존 Project Contract를 증거 기준선으로 결속**하는 스캔을 수행한다. | Incremental 결속 스캔 → `ContextCaptured`(T3) → Eliciting |

세 분기는 모두 `ContextCaptured`(T3)로 수렴해 Eliciting으로 전이한다(02 §3.3-A·§3.3-B — 재정의 0).

### §6.2 증거 소스 접근 = 파일 시스템 실측

- **증거 소스.** 이 환경에서 증거 소스 접근은 **파일 시스템 실측**이다(격리 지점이므로 구체 경로 허용). Brownfield/Incremental 스캔은 워크스페이스의 실 파일·문서·설정을 읽어 증거를 구성한다.
- **본 저장소 dogfooding 스캔 대상(예시).** 본 UAF 저장소 자신을 Brownfield 대상으로 발견하는 run에서 스캔 대상은 저장소의 기존 프로젝트 콘텐츠(`entry/`·`discovery/`·`planning/`·`orchestration/`·`uahf/`·`docs/`·루트 정본 문서 등)다 — entry-binding §4.2·§6이 repository-presence = 유로 관측한 것과 같은 콘텐츠다.
- **Entry ↔ Discovery 경계.** Entry Resolution은 contract-presence·repository-presence의 **유/무만** 관측하고 증거를 수집·해석하지 않는다(entry-binding §4·01-entry EN-INV 1·2). 증거의 **실제 스캔·수집·해석**은 이 D3(Discovery Contextualizing)가 담당한다.
- **증거 기록.** 스캔 산출 증거는 Evidence Store(= D1 백엔드 `.../discovery-data/events/<mode>-<run-id>/`·§3·§4)에 `EvidenceRecorded` Event로 append된다. Evidence Store는 Discovery 내부 append-only 기록이며 UAHF Memory가 아니다(02 §5 네임스페이스 구분).

---

## §7. D4 — Strategy 실행 호스팅 (역할 추상까지만) (done 7)

02 §4.1 행4의 물리 실현을 확정하되, 정본이 명시한 대로 **역할 추상까지만** 확정하고 물리 호스팅(실행 코드·자동 실행)은 **설계하지 않는다**. 02 §4.1 행4 정본: "Discovery 실행을 어느 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(ARCHITECTURE.md §11)." Module부 문단도 "Strategy Provider 실행 호스팅은 **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(§3.10, ARCHITECTURE §11)"로 동일하다.

### §7.1 역할 추상 확정 (형태 A — 규약 절차·규약 역할)

- **Orchestrator 역할 = 주 세션 규약 절차.** State Machine(02 §3.3)을 구동하는 Orchestrator 모듈(02 §3.9)의 역할을 **주 세션(Advisor)이 규약 절차로 수행**한다 — Event를 받아 전이를 실행하고 현재 상태를 유지하며 종단 판정(02 §3.7)을 집행한다. 전이 규칙을 새로 만들지 않는다(02 §3.3 정본).
- **레퍼런스 Provider = 규약 역할.** 02 §3.10-C의 유일 레퍼런스 Provider인 **기본 적응 질문 Provider**를 규약 역할로 실현한다 — 가장 확신이 낮은 미포화 차원을 골라 질문 집합을 내고, 모든 차원 포화·예산 소진 시 차원 포화 신호를 내는 절차를 주 세션이 수행한다. 방법론 고유명 없이 일반형 기본값으로만 실현한다(02 §3.10-D·UAF-INV ⑥).
- **레퍼런스 Provider 인터뷰 행동 = discovery-interview 스킬이 물리 실현.** 위 Provider를 규약 역할로 수행할 때의 인터뷰 행동 규약(기준 골격 + 자율 2층)은 `.claude/skills/discovery-interview/` body가 소유·실현한다(SkillInterface = skills-binding.md §3). Contextualizing~Eliciting 구간 진입 시 스킬 `trigger`로 발동해 body가 주입되며(지연 로드 INV-4) 인터뷰 프레임에만 적용된다. body는 02 §3.5·§3.7·§3.10-B/C·§3.11·§3.12·§3.13·DISC-INV-6·본 문서 §5·§6을 § 포인터로 인용·조립한다(재정의 0·방법론 중립·형태 A). 본 문서는 그 물리 실현을 가리키며 행동 텍스트를 재정의·재서술하지 않는다.
- **물리 호스팅 = 설계 안 함(확장 포인트).** Discovery를 실행 코드로 자동 호스팅하는 물리 실행 주체·자동화는 설계하지 않는다 — ARCHITECTURE §11 확장 포인트를 침범하므로 금지된다. 실행 코드는 형태 B로 미도입이며 그 경계 간 분할은 형태 B 설계 시 확정한다.

### §7.2 Strategy Invariance 훼손 0 (DISC-INV-7)

- **교체되는 것 = Provider뿐.** 교체 가능한 것은 Strategy Registry에 등록되는 Strategy Provider뿐이며(02 §3.9·§3.10), Orchestrator·Confidence Model·Contract Compiler·Discovery Policy의 계약과 출력(Project Contract 스키마·완결 기준)은 어떤 Provider에서도 불변이다(DISC-INV-7·ARCHITECTURE §8 UAF-INV ③). 본 절의 역할 추상 바인딩은 레퍼런스 Provider 1건을 규약 역할로 실현할 뿐 State Machine·Event·Contract 완결 기준을 바꾸지 않는다 — 어떤 Strategy를 쓰든 산출은 동일한 Project Contract다.

---

## §8. D5 — Discovery Policy 값 데이터 소스·직렬화 + E2E 최소 실값 (done 8 · DP-X5)

02 §4.2 Module부 문단("Question Engine의 예산·Discovery Policy의 정책 값(임계값·예산·경계 수치)의 데이터 소스·직렬화는 Adapter 소관이다 — §3.14·§3.15")의 물리 실현. Discovery Policy 계약(02 §3.15 Policy as Data)·Question Budget 계약(02 §3.14)·Confidence 임계(02 §3.12)는 § 포인터 인용이며 데이터 소스·직렬화 형식과 **E2E 구동용 최소 실값 1세트**만 확정한다.

### §8.1 데이터 소스·직렬화 형식

- **데이터 소스.** Discovery Policy 정책 값은 엔진에 하드코딩되지 않고 `uahf/framework/adapters/claude/discovery-data/policy/`의 **데이터 파일**에서 온다(Policy as Data·02 §3.15). Discovery Request의 `policy` 요소(ARCHITECTURE §12.2)가 이 정책을 참조로 담는다(entry-binding §5.1 `policy: <Discovery Policy 참조>` 정합).
- **직렬화 형식.** 정책 파일은 자기서술 구조화 데이터로 직렬화한다(자매 바인딩 관례 동형·구체 형식은 Adapter 선택·격리 지점 §12). 본 문서는 형식·값 정본 문면을 소유하고 물리 파일 생성은 E2E·실 run Task 소관이다(§13 실측).

### §8.2 E2E 구동용 최소 실값 1세트 (정본 값 표 — DP-X5)

E2E 구동을 위한 **최소 실값 1세트**를 본 문서의 정본 값 표로 확정한다. 이 값들은 **Policy as Data**이므로 값 조정은 데이터 정정일 뿐 엔진·정본 계약을 변경하지 않는다(02 §3.15). 4개 정책 항목(02 §3.15 표: 임계값·예산·종료 규칙·충돌 게이트)을 모두 채운 단일 기본 프로파일이다.

**(가) 임계값 정책 — 차원별 Confidence 포화·Ready 임계 θ (02 §3.11 5차원·§3.12 [0,1] 스칼라):**

| Discovery Dimension (02 §3.11) | 포화·Ready 임계 θ |
|---|---|
| Intent | 0.85 |
| Requirement | 0.80 |
| Constraint | 0.75 |
| Risk | 0.75 |
| Architecture | 0.80 |

**θ 값 드리프트 정정(절차 비례화 트랙 Wave 5 · 2026-07-27).** 위 표는 §DC-5 대안 A 적용 **전** 값
(Intent 0.80 / Requirement 0.75 / Constraint 0.70 / Risk 0.70 / Architecture 0.75)을 보이고 있었고,
물리 데이터 `policy/default-policy.yaml` 의 `thresholds` 는 적용 **후** 값이었다
(uaf-allow-legacy: 정정 전 값의 이력 인용 — 드리프트 경위 보존이 목적). 정본은 **물리 데이터 실측값**이므로
위 표를 데이터에 맞춰 갱신했다(§8.3 표준 열과도 정합). 값 조정은 Policy as Data 정정이며 02 §3.12·§3.15
계약은 무변경이다. 이 정정으로 §8.3 말미의 "§8.2 (가) θ 드리프트 미정정" 항은 해소된다.

**(나) 예산 정책 — Question Budget (02 §3.14 총량·차원별·soft/hard):**

| 항목 | 값 |
|---|---|
| 총량 예산 | 40 |
| 차원별 예산 (Intent / Requirement / Constraint / Risk / Architecture) | 10 / 10 / 6 / 6 / 8 (합 40) |
| soft 경계 | 30 (총량의 75%) — 초과 시 적응 압박, 잔여 예산 > 0이면 Eliciting 계속(T8) |
| hard 경계 | 40 (총량) — 소진 시 강제 Synthesize 전이(T11) |
| 재진입 보충 예산 상한 (T17 수정 요청 재진입, §3.14-A) | 10 (총량의 25%) — Policy 상한 아래에서 부여, 재진입 후에도 hard 경계 규칙(T11·T15) 적용 |

**(다) 종료 규칙 정책 (02 §3.6 Termination·§3.13 깊이 조정):**

| 경로 (02 §3.6) | 조건 (값) |
|---|---|
| ① 2축 게이트 충족 → `Ready` | Completeness ∧ 전 5차원 θ(위 (가)) 충족 ∧ 사용자 승인 (02 §3.7·T19) |
| ② 예산 소진 + Confidence 미달 | 필수 코어 필드 가정 충족 가능 → `ReadyWithAssumptions`(Assumption Ledger 필수, T20); 가정으로도 충족 불가 → `Escalated`(T15) |
| 깊이 조정 (02 §3.13) | 기본 프로파일 = 위 (가)·(나) 값. 규모·리스크 상향 시 해당 차원 목표 임계·예산 가산은 **Policy 데이터로 조정**(엔진 무변경) |

**(라) 충돌 게이트 정책 (02 §3.6·§3.15 충돌 게이트·P-D5):**

| 항목 | 값 |
|---|---|
| 충돌·모호 입력 게이트 | 충돌·모호 입력 감지 시 **사용자 확인 게이트 필수**(Validating 경유 — §5 G2/D2 채널) — 게이트 통과 없이 진행 불가(Preserve Human Authority, P-D5) |

- **Policy as Data 불변.** 위 값(임계·예산·경계·종료 규칙·게이트)은 전부 데이터이며 값을 바꾸는 것만으로 Discovery 거동이 조정된다 — Confidence Model·Question Engine·Orchestrator 등 엔진이나 정본 계약(State Machine·Event·완결 기준)은 변경되지 않는다(02 §3.15). 이 값 세트는 **E2E 구동을 위한 최소 실값**이며 다른 임계·예산이 필요하면 `policy/` 데이터 정정으로 조정한다.

### §8.3 프로파일 2종 값표 — 표준 / 경량 (절차 비례화 트랙 Wave 4 · 사용자 확정 Q-5)

Discovery Policy 프로파일은 **2종**이다 — 표준 `policy/default-policy.yaml`(§8.2 값 세트) · 경량 `policy/lightweight-policy.yaml`. 경량은 성숙 brownfield 등 **경량 레인**의 인터뷰 예산을 비례화하기 위한 프로파일이며, 어느 프로파일을 참조하는가는 Entry 결정 테이블 데이터(`entry/adapters/claude/entry-registry.json` `decisionRows[*].policy.ref`)가 정한다. 두 프로파일 공통 절의 **값 정본은 본 §8.2·§8.3**이며, 표준 프로파일 값 개정 시 경량 파일의 공통 절도 동기 갱신 대상이다(드리프트 통제 지점 · `planning/adapters/claude/solution-design-binding.md` §7.2 경량 프로파일 관례 동형).

**(a) ref 해소 규약(물리 관례 — Adapter 소관·§8.1 데이터 소스의 특수화 1항).** Discovery Request 의 `policy` 참조 값 `<ref>` 는 `uahf/framework/adapters/claude/discovery-data/policy/<ref>-policy.yaml`(그 파일의 `policyId` = `<ref>-policy`)로 해소한다. 기존 값 `default` → `default-policy.yaml`(`policyId: default-policy`)에 그대로 성립하므로 신규 규칙 창설이 아니라 **기존 데이터에서 귀납한 관례의 명문화**다. 참조는 **단일 프로파일 1건**을 가리키며 두 파일을 병합하는 오버레이·include 는 **0**이다(그래서 프로파일 파일은 완결이어야 한다).

**(b) 값 대조표.**

| 항목 | 표준 프로파일 (`default-policy.yaml`) | 경량 프로파일 (`lightweight-policy.yaml`) |
|---|---|---|
| `budget.total` | 40 | **20** |
| `budget.perDimension` (Intent / Requirement / Constraint / Risk / Architecture) | 10 / 10 / 6 / 6 / 8 (합 40) | **5 / 5 / 3 / 3 / 4 (합 20)** — 표준의 산술 절반·비율 보존·합 = `total` |
| `budget.soft` | 30 (총량의 75%) | **15** (총량의 75% — 비율 동일) |
| `budget.hard` | 40 (총량) | **20** (총량 — 규칙 동일: 소진 시 강제 Synthesize T11) |
| `budget.reentryTopUpMax` | 10 (총량의 25%) | **5** (총량의 25% — 비율 동일) |
| `thresholds` 차원 수 | 5 (02 §3.11 5차원) | **5 — 동일**(차원 삭제 0) |
| `thresholds` 값 (Intent / Requirement / Constraint / Risk / Architecture) | 0.85 / 0.80 / 0.75 / 0.75 / 0.80 (§DC-5 대안 A +0.05 상향·사용자 결정 2026-07-19) | **동일 값**(θ 하향 0 — 품질 하한 무변경) |
| `termination` (ready · budgetExhausted) | §8.2 (다) | **동일 문면**(완결 기준 완화 0 · 필수 코어 필드 면제 문면 **0**) |
| `conflictGate` | §8.2 (라) | **동일 문면**(게이트 완화 0) |

- **경량 = 질문 예산 축소만이다.** θ(확신 하한)·종료 규칙·충돌 게이트·완결 기준은 무변경이다 — 02 §3.7 축1 Completeness 불가침(DISC-INV-5)에 대한 예외·면제는 경량 프로파일에 **0**이며, 경량 레인에서도 동일 판정식이 집행된다. 새 종료 경로·새 상태·새 Event 를 두지 않는다(02 §3.3·§3.5 무촉).
- **설계된 트레이드오프.** 예산이 절반이고 θ 가 동일하므로 θ 미충족 상태로 hard 경계에 닿는 빈도가 표준보다 높다 → 그 경로는 §8.2 (다) 규칙대로 `ReadyWithAssumptions`(Assumption Ledger 필수, T20) 또는 `Escalated`(T15)로 귀결한다. 이는 우회가 아니라 정본 종료 규칙의 정상 경로이며, 가정 항목은 원장에 남아 게이트에 표면화된다.
- **참조 배선(현행 데이터 상태).** `decisionRows` 행 6(`/continue` + Contract 무 + Repo 유 → `brownfield`)의 `policy.ref` = `lightweight` 이고, 그 밖의 비충돌 행(1·7·8)은 `default` 다. 충돌 행(2·3·4·5)의 `user-confirmation-gate` 는 게이트 정책 참조이므로 본 절의 프로파일 축과 직교한다(§8 프로파일은 게이트 판정에 관여하지 않는다). 값 변경은 그 데이터 1행 교체로 이뤄지며 `entry_resolve.py`·02 spec 은 무촉이다.

**(c) 미해소 — 이 프로파일이 해소하지 않는 것(해소 주장 금지).**

- **문항 수 직접 감소 아님.** 실제 문항 수를 좌우하는 **필수 커버리지 축 목록**은 `.claude/skills/discovery-interview/SKILL.md` Part 1 커버리지 맵(표 10행 = Discovery 소유 9축 + 하류 위임 경계 1행)이 **body 하드코딩**으로 소유하며 Policy 데이터가 아니다. 따라서 경량 프로파일은 **예산 상한만** 낮추고 최소 심문 대상 축 수를 낮추지 못한다. 커버리지 축의 Policy 데이터화·체커화는 별 트랙 소관이다(좌표 = 메모리 `uaf-coverage-enforcement-gap` · `docs/proportionality-track-ledger.md` §4 Wave 4 done 6 · 스킬 body 27행 자기신고 충돌 플래그).
- **침묵 생략 금지 무약화.** 스킬 body 의 침묵 생략 금지 규율(Part 1 head·⑦ (ii)·⑨·⑪ — "축을 조용히 지나치는 것은 제외가 아니라 미심문"·제외는 사유 기록 + 게이트 일괄 표면화)은 이 프로파일로 약화되지 않는다. **예산 소진은 축 제외의 사유가 되지 못한다** — 예산은 질문 수의 상한이고 커버리지는 별개 축이다(θ ≠ 커버리지 역설·SKILL.md ⑦ 말미). 본 개정은 스킬 body 를 수정하지 않는다(diff hunk 0).
- **§8.2 (가) 표와 데이터 파일의 θ 드리프트 — 해소(2026-07-27 · 절차 비례화 트랙 Wave 5).** Wave 4 시점에는 §8.2 (가) 표가 상향 전 값(0.80/0.75/0.70/0.70/0.75)을 보이고 물리 데이터 `default-policy.yaml` `thresholds` 는 §DC-5 대안 A 적용 후 값(0.85/0.80/0.75/0.75/0.80)이어서 미정정으로 남았다(uaf-allow-legacy: 정정 전 상태의 이력 인용 — 경위 보존). Wave 5 가 §8.2 (가) 표를 물리 데이터 실측값으로 갱신해 드리프트를 없앴다. 본 §8.3 표의 표준 열은 처음부터 실측값이었으므로 무변경이다.

(`uaf-verified:` 위 표·항목의 값·배선 주장은 `discovery-data/policy/default-policy.yaml`·`lightweight-policy.yaml` 두 파일의 키 트리·값 직접 대조, `entry/adapters/claude/entry-registry.json` `decisionRows` 8행 `policy` 전수 판독, `entry_resolve.py` 판독(`load_registry`·`verify_determinism`·`resolve` — `policy` 는 행 값을 그대로 방출하며 `ref` 값 도메인 검증·프로파일 파일 적재는 코드에 0), `.claude/skills/discovery-interview/SKILL.md` 커버리지 맵·침묵 생략 조항 판독, 그리고 `entry_resolve.py --entry continue` brownfield 실행 1건(exit 0 · `policy.ref == lightweight` · `matchedRow` 6)·`pytest entry/adapters/claude/tests` 전건 Pass·`git diff --stat` 상 `entry_resolve.py`·`discovery/specs/02-discovery.md`·`SKILL.md` hunk 0 실측으로 얻었다. **검색 범위 = 위 6파일 + 02 spec `§3.7`/`§3.11`/`§3.13`/`§3.14`/`§3.15` 절 판독 + 저장소 전체 `default-policy`·`policy.ref` grep**이며, 그 밖(실제 인터뷰 세션에서의 문항 수 실측·소비 프로젝트 실 run 왕복·`entry-binding.md` 표 행 B 문면 정합)은 이 개정의 실측 범위 밖이다.)

---

## §10. DP-X6 해소 — Provenance 컨테이너 내부 형식 (done 9)

contract-binding §6은 Contract 인스턴스 front-matter 내 분리 네임스페이스 `provenance` 컨테이너의 **외형·must-ignore 경계**만 확정하고 그 **내부 직렬화 형식·필드**를 본 문서 소관으로 명시 위임했다(DP-X6·planning/specs/03 §3.2-D 불투명 부속 동형). 본 절이 그 내부 형식을 확정한다.

### §10.1 내부 형식 = Discovery 실행 메타

`provenance` 컨테이너 내부는 **Discovery 실행 메타**를 담는 자기서술 구조화 블록이다. 최소 구성:

| 내부 필드 (Discovery 실행 메타) | 값 형태 | 참조 대상 |
|---|---|---|
| run 식별자 | 문자열 — 해당 Discovery run(State Machine 인스턴스, 02 §3.3-A)의 `<run-id>` | `.../discovery-data/events/<mode>-<run-id>/`(§4) |
| Event 로그 참조 | 참조 — 이 run의 Event 로그 디렉터리 경로/참조(§3·§4) | D1 백엔드(§3) |
| mode | 문자열 — greenfield / incremental / brownfield 등(ARCHITECTURE §12.2 확장 네임스페이스) | Discovery Request `mode`(entry-binding §5.1) |
| Policy 참조 | 참조 — 이 run이 사용한 Discovery Policy 참조(§8) | `.../discovery-data/policy/`(§8·02 §3.15) |

- 위는 **최소 표면**이며 감사·재현에 필요한 추가 실행 메타(예: Readiness 선언 참조·Assumption Ledger 참조)를 담을 수 있다. 어느 필드도 경량 **참조**이며 Event 로그·증거 원문을 컨테이너에 중복 저장하지 않는다(loop-binding §5.3 경량 참조 관례 동형).

### §10.2 planning/specs/03 §3.2-D 불투명 계약 유지 — UAHF must-ignore 불변

- **must-ignore 경계 불변.** UAHF tolerant reader는 `provenance` 컨테이너(및 그 하위 전체)를 **must-ignore**한다 — 존재를 오류로 취급하지 않고 소비하지 않는다(contract-binding §6·planning/specs/03 §3.2-D·§3.3-C). 내부 형식을 채워도 이 경계는 불변이며 내부 필드는 **Discovery 측 소비 전용**(감사·재현·계보 추적)이다.
- **누출 차단(DISC-INV-8).** Provenance 내부는 Contract **코어 스키마 밖**의 불투명 부속이다. Discovery 실행 메타는 코어 필드(Intent·Requirements·Constraints·Risks·Architecture Direction·Readiness·Assumption Ledger 등)로 새어나가지 않는다 — Discovery 내부 변경(기법·전략·예산·질문 방식)이 만드는 실행 메타는 `provenance`에만 반영되고 코어 스키마·UAHF 접점에 도달하지 못한다(contract-binding §6·PC-INV 2·10·DISC-INV-8).
- **창설 금지.** 본 절은 planning/specs/03 §3.2-D 불투명 부속 계약을 재정의하지 않고 **내부 형식만** 채운다. Contract 코어 스키마·버저닝·tolerant reader 계약을 변경하지 않는다. 이로써 contract-binding §11(OQ-TC-2)이 미룬 Provenance 내부 형식 지점이 해소된다.

---

## §12. 02 §4.2 이식 교체 지점 대응 (done 11)

"교체되는 것"이 이 환경 바인딩이고, "유지되는 것"은 02 §3 Core Contract(이식 불변·structure.md §7 C-1 동형)이므로 정본 § 포인터로만 가리킨다.

| 02 §4.2 교체 지점 (바뀌는 것) | 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 §) |
|---|---|---|---|
| Event 로그 직렬화 포맷·저장 위치 → 대상 환경의 로깅 메커니즘 | §3, §4 | 자기서술 구조화 레코드 append-only 로그·`.../discovery-data/events/<mode>-<run-id>/` 위치·순서 값 물리 표현. | 02 §3.3·§3.5·§3.6 (DISC-INV-1·3) |
| 사용자 확인·Override 채널 → 대상 환경의 사람 개입 메커니즘 | §5 | 주 세션 사용자 제시·응답 수령 채널(G1·G2·UserOverride). | 02 §3.3 Validating·§3.6·§3.7 (DISC-INV-6·UAF-INV ⑤) |
| 증거 소스 접근·스캔 구현 → 대상 환경의 증거 수집 메커니즘 | §6 | Greenfield 프레이밍/Brownfield 파일 시스템 스캔/Incremental 결속의 형태 A 절차·파일 시스템 실측 접근. | 02 §3.3-A(T2·T3)·§3.9 (DISC-INV-3) |
| Strategy 실행 환경 → 대상 환경의 실행 주체 | §7 | 주 세션(Advisor) Orchestrator 역할·레퍼런스 Provider 규약 역할(역할 추상까지만). | 02 §3.1·§3.9·§3.10 (DISC-INV-7·UAF-INV ③⑥) |
| **Module부 바인딩** — 예산·Policy 값 데이터 소스·직렬화 → 대상 환경의 데이터 소스; Evidence Store 물리 저장 = Event 로그 바인딩과 동일 | §8; §3·§4 (D6=D1) | `.../discovery-data/policy/` 형식·E2E 최소 실값; Evidence Store = Event 로그 백엔드(동일). | 02 §3.14·§3.15·§3.9 |

- 본 문서는 02 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고 물리 실현 매핑에 한정한다(§0).

---

## §13. 상태 서술 실측 대조 (L-07 — 미존재를 실재로 쓰지 않음)

본 문서가 확정한 Event 로그 직렬화(§3)·백엔드 트리(§4)·D2 채널(§5)·D3 절차(§6)·Policy 값(§8)·Provenance 내부 형식(§10)은 **정본 문면(형태 A)**이며, 본 문서는 구조·형식·경로·값의 정본만 소유하고 물리 데이터를 생성하지 않는다. 백엔드 데이터 트리의 현행 실재 상태:

| 경로 (`uahf/framework/adapters/claude/discovery-data/`) | 실측 상태 |
|---|---|
| `events/` | 실재 — run 디렉터리 `brownfield-r004/`·`brownfield-r005/`(각 `discovery-request.yaml`·`events.jsonl`) |
| `policy/` | 실재 — 프로파일 **2종**: `default-policy.yaml`(§8.2 값 표의 물리 직렬화) · `lightweight-policy.yaml`(§8.3 경량 열의 물리 직렬화) |
| `contracts/uahf/` | 실재 — `project-contract.v1.md`·`v2.md`·`v3.md`(정본 = contract-binding §4.2) |
| `e2e-greenfield-project/` | 미실재 — §4.1 트리 선언만 있고 물리 생성은 E2E Task 소관 |

`uaf-verified:` 위 표 = `uahf/framework/adapters/claude/discovery-data/` 재귀 디렉터리 목록 실측(2026-07-26). 검색 범위 = 그 트리의 디렉터리·파일명이며 파일 내용 정독은 아니다. 그 물리 위치(트리가 `uahf/` 아래 잔류하는가)는 2차 산출물 디커플링 트랙에서 확정한다.

---

## §14. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 모든 매핑은 02 §3·§4의 물리 실현이다. Event·상태·전이·모듈 경계·Provider 계약·Dimension·Confidence·Question Budget·Discovery Policy·DISC-INV 1~9의 진위는 이 문서에서 새로 확정되지 않는다 — 판정 기준은 02 §3이다. 방법론 고유명 0(02 §3.10-D·UAF-INV ⑥).
- **본 문서 소유·확정분** = D1 Event 로그 직렬화(§3) · discovery-data/ 백엔드 트리(§4) · D2 채널(§5) · D3 절차(§6) · D4 역할 추상(§7) · D5 Policy 값·E2E 최소 실값(§8) · D6 Evidence Store 물리 저장(= D1) · DP-X6 Provenance 내부 형식(§10) · DP-X8 Discovery Request 기록 위치(§4.2). D4 물리 호스팅은 설계하지 않는다(ARCHITECTURE §11).
- **상시 불변 경계.** Discovery 내부 개념(질문·전략·예산·Capability)은 Contract 코어 스키마·UAHF 접점을 정의하는 자리에 쓰이지 않는다 — 본 문서에서 그 어휘는 02 § 포인터 인용·Discovery 내부 실현 서술·불변/경계 서술에만 등장한다(mention/use 경계·DISC-INV-7·8·ARCHITECTURE §7.1 ①). Contract 스키마·필수 코어 필드·버저닝은 재정의하지 않으므로 Stable Contract 지위는 불변이다(§7.1 ②·UAF-INV ①②). Provenance 내부(§10)·Event 로그(§3)·Evidence Store(§4)는 Discovery 내부 기록이며 must-ignore·격리 경계 뒤에 있다.
- **Evidence Store ≠ UAHF Memory(02 §5).** `discovery-data/`(Discovery 백엔드)와 `memory-data/`(UAHF Memory 백엔드)는 별개 격리 트리다. Discovery는 UAHF Memory를 회수·활용하지 않으며(ARCHITECTURE §10 비담당 ④) 본 문서는 그 활용 경로를 설계하지 않는다(ARCHITECTURE §11 확장 포인트로만 열려 있다).
- **격리 토큰의 단일 자리.** 구체 직렬화 형식·물리 경로·파일 확장자·Policy 수치는 이 Adapter 경계 문서에 둔다(structure.md §5 C-3 비적용 — 격리 보유).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-TD-1 (Policy 최소 실값 수치 — 비차단).** §8.2 값 세트는 본 문서의 Adapter 재량 확정이며 Policy as Data이므로 조정은 데이터 정정일 뿐 계약(02 §3.12·§3.14·§3.15) 변경이 아니다.
- **OQ-TD-2 (run-id·레코드 파일 단위 명명 — 후속/비차단).** run-id 발급 규칙·레코드 파일 명명 세부는 Adapter 재량이며(§3.4) append-only·순서 값 성격은 어느 명명에서도 유지되므로 계약 변경이 아니다.

---

## §15. 개정 이력

- **2026-07-27 (정합) 절차 비례화 트랙 Wave 4** — Discovery 경량 프로파일 신설 + Entry 참조 배선 1행. `policy/lightweight-policy.yaml` 신설(`budget` total 20/soft 15/hard 20/perDimension 5·5·3·3·4(합 20)/reentryTopUpMax 5 = 사용자 확정 Q-5 + 표준의 산술 절반·비율 보존 · `thresholds` 5축 전부 존재·표준과 **동일 값**(θ 하향 0·차원 삭제 0) · `termination`·`conflictGate` 표준과 동일 문면 — 필수 코어 필드 면제 문면 0). **§8.3 신설**(무침습 append — §8.1·§8.2 문면 무변경·§10 이하 절 번호 보존): ref 해소 규약 `<ref>` → `policy/<ref>-policy.yaml`(기존 `default` 에서 귀납·창설 0) · 프로파일 2종 값 대조표 · 설계된 트레이드오프(예산 절반 × θ 동일 → hard 경계 시 T20/T15 정상 경로) · 미해소 3항(문항 수 직접 감소 아님·침묵 생략 금지 무약화·§8.2 (가) θ 드리프트 미정정). 동반 정정 = §2 D5 행·§13 표의 `policy/` 실재 상태를 프로파일 2종으로 갱신(L-07 실측 서술). 데이터 배선 = `entry/adapters/claude/entry-registry.json` 행 6(brownfield) `policy.ref` `default` → `lightweight`(값 1개 교체·행 6 외 무촉) + 그 값에 결합된 테스트 단정 1줄 동기(`test_entry_resolve.py` `test_case3`). 실측: `entry_resolve.py --entry continue` brownfield 실행 exit 0(`matchedRow` 6 · `policy.ref` `lightweight`) · `pytest entry/.../tests` 22 passed exit 0 · `entry_resolve.py`·`discovery/specs/02-discovery.md`·`discovery-interview/SKILL.md` diff hunk **0**. 02 spec 수정 0(계약 무변경·가법). 사용자 확정 Q-5(2026-07-26). | Worker (Advisor 위임)
- **2026-07-26 (정합) md 슬림화 Wave 4** — 비계약 격리 개정: 메타 템플릿·해소 OQ·경위 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c. Advisor 위임. 동반 정정 = §2·§4·§8·§13의 `discovery-data/` 미존재 서술을 실측 상태로 갱신(§13 표).
