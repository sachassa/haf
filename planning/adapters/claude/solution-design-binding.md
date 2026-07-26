# planning/adapters/claude/solution-design-binding — Claude Code Solution Design Adapter 바인딩

상태: v1.4 Baseline · 상위 규약: AGENT.md
근거 정본(§ 포인터만·재정의 0): `planning/specs/04-solution-design.md` §3(전문 — 특히 §3.1 단계 계약·§3.2 복잡도 판정 Policy as Data·§3.3 역할 할당·개방 네임스페이스·§3.4 협업 프로토콜 State Machine(비종단 5·종단 3·T1~T11)·§3.5 Projection·§3.6 경계 기준·§3.7 저장 스코프·§3.8 SP-INV 1~9·§3.9 확장 포인트)·§4.1(바인딩 지점 표 4행)·§4.2(이식 교체 지점) · `planning/specs/03-project-contract.md` §3.1-B·§3.4·§3.5·§3.6 PC-INV 9 · 루트 `ARCHITECTURE.md` §6 원칙 11·§7.1·§8 UAF-INV ①⑤⑥ · `planning/adapters/claude/contract-binding.md` §4.1·§4.2·§5·§6(**superseding 인스턴스 저장·버전 표기·Provenance 외형 소유** — 참조 인용만) · `discovery/adapters/claude/discovery-binding.md` §3·§4·§5·§7·§8·§10·§13(**핵심 골격 선례** — Discovery 도메인 계약 차용 0) · `entry/adapters/claude/entry-binding.md`·`memory-binding.md`·`loop-binding.md` §5.2(자매 골격·채널·격리·append-only 선례) · `uahf/framework/core/structure.md` §2·§4(`형태 A/B` 서술 라벨)·§5(C-3 비적용)·§7(C-1) · `planning/ARCHITECTURE.md` §0·§7 · `uahf/specs/00-glossary.md`(용어 신설 0).

거버넌스: 이 문서는 `planning/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core·UAF 계약을 특정 실행 환경·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 직렬화 형식·물리 경로·환경 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — 자매 contract-binding.md §0·entry-binding.md §0·discovery-binding.md §0과 동형). 단 UAF 정본(04 §3·§4)과 자매 정본(03·02·루트)·UAHF 정본을 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인으로 이뤄진다.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계 (요지)

- **정본은 planning/specs/04 §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며 계약 요소(단계 계약·복잡도 판정·역할 할당·State Machine T1~T11·Projection·경계 기준·SP-INV 1~9)를 재정의·확장하지 않는다. 본 문서가 확정하는 것은 04 §4.1이 "Adapter 소관"으로 미룬 **네 지점** — ① Expert Role 실행 호스팅(역할 추상까지만) ② 사용자 게이트 제시·응답 채널 ③ 산출물 저장 위치·직렬화(실행 기록 포함) ④ Policy 실값 — 과, 그 저장의 부속으로 ⑤ 성숙 인스턴스 `provenance`의 **성숙 run 내부 형식**뿐이다(§2·§13).
- **격리 지점의 방향 반전(C-3 비적용)·형태 A 전제.** 이 문서는 Core·UAF 정본(토큰 0건)의 **반대편**이며 구체 직렬화 형식·물리 경로·Policy 값이 허용된다 — 단 특정 설계 방법론 고유명·고정 역할 카탈로그·타 AI 벤더·모델명은 여기서도 명명하지 않는다(UAF-INV ⑥). 바인딩은 **실행 코드 0**(형태 A)이며 State Machine·판정·역할 협업은 **규약 절차·규약 역할**로 주 세션이 실수행한다. 매핑은 (i) 물리 실재 (ii) 규약 확정 문면(형태 A) (iii) 형태 B 로딩 지점을 정직하게 구분한다(§12·L-07).
- **경계 분담 — 소유와 위임.** (i) **superseding 인스턴스 자체**(v(N+1) 문서·버전 표기·저장 경로·직렬화)는 **contract-binding §3·§4·§5 소유**다 — Contract 저장은 생산자와 무관하며(03 §3.1-B 생산자 2경로) 본 문서는 성숙 경로가 그 경로에 append됨만 참조 인용한다. (ii) `provenance` **외형·must-ignore 경계**는 **contract-binding §6 소유**이며 본 문서는 **성숙 run 내부 형식**만 확정한다(§8 — discovery-binding §10 동형·침범 0). (iii) 본 문서가 신설·소유하는 것은 **`solution-design-data/` 백엔드 트리**뿐이다.
- **책임 경계 문안 (Solution Design 활동 vs Contract Maturation 갱신 유형).**

  > **Solution Design은 활동이고, Contract Maturation은 그 활동이 산출하는 갱신 유형이다.** Solution Design(04)은 Ready vN을 입력으로 복잡도 판정·역할 협업·사용자 게이트를 수행하는 **UAF 레벨 활동**이며, 그 성숙 경로 종단(Matured)의 산출이 **Contract Maturation**(03 §3.4 갱신 유형) — 동일 append-only·supersedes 메커니즘에 의한 v(N+1) 재발행 — 이다. 활동 계약은 04가, 재발행 메커니즘·인스턴스 거버넌스는 03이 소유한다. 어느 쪽도 상대를 재정의하지 않는다.

  본 문서는 이 구분의 **물리 측면**만 확정한다 — 활동(04)의 실행 메타·게이트·Policy·호스팅은 `solution-design-data/`에, 갱신 유형이 낳는 superseding 인스턴스는 contract-binding §4.2 경로에 놓인다.
- **경로 표기·용어.** 백엔드 데이터 트리(`solution-design-data/`·`discovery-data/contracts/uahf/`)의 현행 물리 위치는 `uahf/framework/adapters/claude/…` 아래이며(최종 확정 = 2차 산출물 디커플링 트랙) 본문에서는 잎 이름으로 축약한다. `.claude/…`는 소비 프로젝트 상대 경로다. 04가 소유하는 계약 용어(상태·전이·Expert Role·Capability·Projection·SP-INV)는 § 포인터로만 참조하며, §4의 **레코드 종류 명칭**은 코어 계약 요소가 아니라 이 Adapter의 **기록 관례**로서 Discovery Event 15종 명칭을 차용하지 않는다.

---

## §1. 목적

planning/specs/04 "### 4.1 바인딩 지점" 표 4행을 이 환경 위에 **v1.4 시점의 구체 물리 실현**으로 매핑한다. 성숙 산출(superseding Contract 인스턴스)은 UAHF 구현 단계의 선택 입력(03 §3.5-A)이므로 여기서 확정하는 물리 인터페이스가 dogfooding E2E의 물리 실현 기반이다. 책임: **DP-1** `solution-design-data/` 백엔드 트리 정본 선언(§3) · **DP-2** run 단위 append-only 기록 로그 직렬화·레코드 어휘(§4) · **DP-4** 게이트 채널·T8~T11 실의미(§5) · **DP-3** Expert Role 실행 호스팅 역할 추상(§6) · **DP-5** Policy 데이터 소스 + 최소 실값 1세트(§7) · Provenance 성숙 run 내부 형식(§8) · 04 §4.2 이식 대응(§10). 그 위에 form-A 규약 3절(§7A 산출물 생산·§7B 다라운드 심의·§7C Visual Contract)이 얹힌다. 04·03·02·루트 정본의 어떤 계약 요소도 재정의·확장하지 않으며(§0), 형태 A → 형태 B 전환에도 04 §3 계약 변경은 0이다(structure.md §7 C-1).

---

## §2. 04 §4.1 바인딩 표 4행 물리 실현 (done 2)

"04 §4.1 바인딩 지점" 열은 정본 표현을 그대로 인용하고, "물리 실현" 열이 본 문서가 확정하는 형식·경로·채널·값을, "실재 여부" 열이 **물리 실재 / 규약 실현(형태 A) / 형태 B**를 정직하게 구분한다(§12).

| # | 04 §3 계약 요소 (정본 §) | 04 §4.1 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Expert Role 실행 호스팅 (§3.3) | "논리 Expert Role을 어느 실행 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(M5)." | 주 세션(Advisor)이 Orchestrator 역할을 규약 절차로 수행해 State Machine(04 §3.4)을 구동하고, Expert Role 수행은 **이 환경의 기존 위임 실행 관행**(서브에이전트 위임·완료 보고·독립 검증)을 재사용. 새 병렬 실행 프레임워크 창설 0·물리 호스팅(실행 코드·자동화) 설계 0. 상세 §6. | 역할 추상 확정(정본, 형태 A). 물리 호스팅 = **설계 안 함**(확장 포인트 04 §3.9). 실행 코드 = 형태 B. |
| 2 | 사용자 게이트 제시·응답 채널 (§3.4 `Validating`) | "성숙/스킵 결과 제시와 승인/확인/수정 응답을 받는 개입 채널(강제 일시중단·재개 semantics 포함)." | 주 세션 사용자 제시·응답 수령 채널(discovery-binding §5 동형) — 게이트 제시·응답 각각 레코드로 기록. T8(승인→Matured)·T9(확인→Skipped)·T10(수정→Reviewing 재진입)·T11(강제→Escalated) 실의미. 승인 전 Matured 도달 불가(SP-INV 4). 상세 §5. | 채널·기록 확정(정본, 형태 A). 무인 자동 제시 UI = 형태 B. |
| 3 | 산출물 저장 위치 (§3.7) | "Proposal·리뷰 기록·Projection·superseding 인스턴스가 워크스페이스에 배치·보관되는 물리 위치·경로 관례·직렬화 형식." | 성숙 실행 메타(이벤트 로그·Proposal·충돌/trade-off·리뷰 기록·Policy) = `solution-design-data/`(§3·§4); superseding 인스턴스 = contract-binding §4.2 경로 `discovery-data/contracts/uahf/project-contract.v<N>.md`에 append(참조 인용·재정의 0); Projection = 대상 워크스페이스 귀속(§3). 상세 §3·§4. | 경로·형식 정본 확정(형태 A). `solution-design-data/` 데이터 = 실재(§12). |
| 4 | 복잡도 판정·역할 선택·Projection 선택 Policy 실값 (§3.2·§3.3·§3.5) | "판정 임계·역할 선택 규칙·Projection 유형 선택 정책의 데이터 소스·직렬화(Policy as Data)." | `solution-design-data/policy/default-policy.yaml` 데이터 파일 + **최소 실값 1세트 정본 값 표**(§7.2). Policy as Data — 값 조정 = 데이터 정정. 상세 §7. | 형식·값 정본 확정(형태 A). 물리 데이터 파일(`policy/`) = 실재(§12). |

주: 위 4행은 04 §4.1 표의 전 행이며 각 "물리 실현"은 정본 표현을 좁힌 것으로 **새 바인딩 계약을 창설하지 않는다**(§0). 실행 기록 직렬화(§4)는 행 3의 일부이자 04 §3.2 "판정 근거 기록"·§3.7 위임의 실현이다. 04 §4.1 표에 없는 계약 요소(§3.1·§3.2 판정 형태·§3.3 역할 추상·§3.4 골격·§3.5 관계·§3.6·§3.8)는 **이식 시에도 유지되는 것**이며 본 문서가 바인딩하지 않는다(§10) — 진위 판정 기준은 04 §3이다. 특정 방법론 고유명·고정 역할 카탈로그·타 벤더·모델명은 여기서도 명명하지 않는다.

---

## §3. DP-1 — 저장 위치·백엔드 트리 정본 선언 (done 3)

04 §4.1 행3의 물리 실현을 확정한다. 저장 스코프 원칙(04 §3.7·SP-INV 7)은 § 포인터로만 인용하고 물리 위치·경로 관례만 확정한다.

### §3.1 성숙 실행 메타 백엔드 = `solution-design-data/` 신설 (DP-1)

Solution Design의 **성숙 실행 메타**(이벤트 로그·Proposal·충돌/trade-off·리뷰 기록·Policy)의 물리 백엔드를 **Adapter 경계 이하 `uahf/framework/adapters/claude/solution-design-data/`로 확정한다**(자매 `memory-data/`·`loop-data/`·`discovery-data/` 백엔드 격리 선언 동형).

- **신설 근거(UAF-INV ① 안전).** `discovery-data/`는 discovery-binding §4가 소유한 **Discovery 전용 백엔드 정본**이므로 성숙 실행 데이터를 혼입하면 책임 경계가 오염된다. 별도 루트가 최소 변경이며, 성숙 산출 데이터가 하네스 규약·Core와 혼입되지 않도록 격리한다(contract-binding §4.2 격리 근거 동형).
- **이원화(DP-X2 동형).** 위 격리 배치는 본 저장소 dogfooding 관례다. **일반 관례**(소비 프로젝트)에서 성숙 실행 메타는 `.claude/solution-design/` 아래에 귀속된다(04 §3.7 워크스페이스 귀속·contract-binding §4 이원화 동형). 두 경로 모두 본 문서가 정본으로 확정한다.

### §3.2 백엔드 트리 (정본 문면 · 물리 위치는 2차 산출물 디커플링 트랙에서 확정)

```
uahf/framework/adapters/claude/               # 물리 위치는 2차 산출물 디커플링 트랙에서 확정
└─ solution-design-data/                     # ★ SD 백엔드 격리 루트 — 성숙 run E2E로 실재
   ├─ events/                                # DP-2 — run 단위 append-only 기록 로그 + 실행 메타
   │  └─ maturation-<run-id>/                #   성숙 run 1건의 격리 디렉터리
   │     ├─ events.jsonl                     #     append-only 기록 로그(전이·게이트·산출·run 생애; §4)
   │     └─ <실행 메타 파일…>                #     Proposal·Reconciling(충돌/trade-off)·Reviewing 기록
   │                                         #     (SP-INV 2·3 — 코어 밖 실행 메타·Contract 코어 필드 유입 0)
   └─ policy/
      └─ default-policy.yaml                 # DP-5 — 최소 실값 1세트(§7)
```

- **`events/maturation-<run-id>/`(DP-2, §4).** 한 성숙 run의 append-only 기록 로그와 실행 메타 파일을 run 단위로 격리 보관한다. `<run-id>`는 해당 run(= Ready vN 결속으로 `Assessing`에 생성된 State Machine 인스턴스, 04 §3.4-A)의 식별자다. 로그 파일명·레코드 파일 단위의 세부는 Adapter 재량이며 어느 경우에도 §4 append-only·순서 값 성격은 유지된다(선취·추측 금지).
- **실행 메타 파일(SP-INV 2·3 — 코어 밖).** Proposal·충돌/trade-off·통합 리뷰 기록은 run 디렉터리 내 실행 메타 파일로 둔다 — **코어 밖의 불투명 실행 메타**이며 Contract 코어 필드로 유입되지 않고 UAHF가 소비하지 않는다(04 §3.8 SP-INV 2·3·§3.4-C 단일 인스턴스 수렴). Agent별 문서를 무한 생성하지 않고 단일 superseding 인스턴스로 수렴하는 04 §3.4-C 규칙을 물리 저장이 반영한다.
- **`policy/`(DP-5, §7).** 판정 기준·역할 선택 규칙·Projection 선택 정책의 데이터 파일을 둔다. Policy as Data이므로 값 조정은 데이터 정정일 뿐 규약 절차·정본 계약 무변경이다(04 §3.2).

### §3.3 superseding 인스턴스·Projection 저장 (참조 인용 — 재정의 0)

- **superseding 인스턴스(v(N+1))는 이 트리가 아니다.** 성숙 경로의 superseding 인스턴스(03 §3.4·§3.1-B (ii))는 **contract-binding §4.2가 소유한 Contract 저장 경로**에 append된다 — 본 저장소 dogfooding은 `uahf/framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v<N>.md`, 일반 관례는 `.claude/project-contract/project-contract.v<N>.md`(파일명·직렬화·버전 표기 정본 = contract-binding §3·§4·§5). Contract 저장은 생산자와 무관하게 contract-binding 소유이며 본 문서는 **참조 인용**만 한다. 예: Ground Truth `pc-uahf-001` v1을 기준선으로 성숙하면 v2는 같은 경로에 append되고 v1 문면은 byte 불변이다(PC-INV 9·append-only).
- **Projection 산출.** 동적 선택된 Projection(04 §3.5)은 **대상 프로젝트 워크스페이스에 귀속**된다(04 §3.7 SP-INV 7). Contract를 Source of Truth로 하는 파생 산출이며 물리 배치 세부는 산출 시 확정한다 — 본 문서는 귀속 원칙만 선언한다.
- **`solution-design-data/`는 지원 구조(성숙 run E2E로 실재).** 이 트리·하위 데이터의 **정본 문면(형태 A)**은 본 문서가 소유하며, 실제 디렉터리·데이터 파일은 성숙 run E2E로 생성되어 현행 위치에 실재한다(§12·L-07).

---

## §4. DP-2 — 실행 기록 직렬화·최소 레코드 어휘 확정 (done 4)

04 §3.2("판정 근거 기록")·§3.7(물리 배치 위임)의 실현으로 성숙 run의 **실행 기록** 직렬화 형식과 **최소 레코드 종류**를 확정한다. State Machine 상태·전이(04 §3.4)는 § 포인터로만 인용한다.

### §4.1 확정 — 자기서술 구조화 레코드 append-only 로그 (1 사건 = 1 레코드)

**한 성숙 run의 실행 기록 = 발생 순서대로 append되는 자기서술 구조화 레코드의 로그**로 직렬화한다(`events.jsonl` 동형 — discovery-binding §3.2 관례 동형). **1 사건 = 1 레코드**이며 append-only다. 구체 구조화 데이터 형식은 Adapter 선택이다(격리 지점 — 이식 교체 §10).

- **레코드 최소 표면.** 각 레코드는 최소한 (i) **레코드 종류**(§4.3), (ii) **순서 값**(§4.2), (iii) **레코드별 페이로드**를 담는다. 페이로드 내부는 이 직렬화가 해석하지 않는 불투명 페이로드다.
- **append-only 불변.** 기록된 레코드는 재작성·삭제하지 않고 정정·후속 상태는 새 레코드 append로 표현된다. T5 재제안·T7 잔여 충돌 재노출·T10 수정 재진입·T11 강제도 각각 하나의 레코드로 append된다(04 §3.4-B — 재정의 0).
- **"기록만으로 run 재구성".** 레코드 순서(= append 순서 = 전이 순서)만으로 해당 run의 State Machine 진행(`Assessing` 생성 → 전이 → 종단)이 재구성된다.

### §4.2 순서 값과 물리 생성 시각의 성격 구분 (L-09)

- **순서 값(정본 표면).** 각 레코드는 단조 증가하는 순서 값(`seq`)을 갖고, 로그의 순서는 언제나 이 값(= append 순서)에서 도출된다 — 벽시계 시각에서 도출하지 않는다.
- **물리 생성 시각(별도 필드·실측 성격).** 벽시계 생성 시각을 함께 담는 경우 그것은 **순서 값과 별개의 필드**이며, 그 값의 진위는 **실측 대조 후에만** 참으로 취급되는 측정 주장이다(L-09). 물리 생성 시각은 로그 순서를 결정하지 않는다.

### §4.3 최소 레코드 종류 (Adapter 기록 관례 — 새 코어 계약 요소 창설 0)

**이 명칭은 이 Adapter의 기록 관례일 뿐이며 04·03 코어 계약의 상태·전이·불변·필드·kind를 창설·재정의하지 않는다** — 상태·전이 라벨은 04 §3.4 정본을 payload에 인용할 뿐이다. **Discovery Event 15종(02 §3.5 소유)의 명칭은 차용하지 않는다** — 명칭 재사용이 곧 의미 파괴이므로 SD 고유 어휘로 명명한다.

| 레코드 종류 (기록 관례) | 담는 것 | 인용하는 04 정본 |
|---|---|---|
| `MaturationRunStarted` | run 시작·입력 결속 — 입력 인스턴스 경로(vN)·`instanceVersion`·사용한 policy 참조·초기 상태 `Assessing`. 별도 Request 형식을 신설하지 않고 이 레코드가 입력 결속을 담는다(최소 변경). | §3.1-B 입력(Ready\|ReadyWithAssumptions vN)·§3.4-A `Assessing` 생성 |
| `StateTransition` | 상태 전이 1건 — payload에 전이 라벨(T1~T11)·`from`/`to` 상태(`Assessing`·`Proposing`·`Reconciling`·`Reviewing`·`Validating`·`Matured`·`Skipped`·`Escalated`)를 **04 §3.4 정본 그대로 인용**. | §3.4-A 상태·§3.4-B 전이표 T1~T11 |
| `GatePresented` | 사용자 게이트 제시 — `Validating`에서 성숙 결과(또는 스킵 판정)를 사용자에게 제시한 사건. | §3.4-A `Validating`·§3.4-D ⑥ |
| `UserResponded` | 사용자 게이트 응답 — 승인/확인/수정/강제 응답 수령(T8/T9/T10/T11 유발). 제시와 응답을 각각 레코드로 남긴다. | §3.4-B T8·T9·T10·T11 |
| `OutputRecorded` | 산출 기록 — 종단 시 superseding 인스턴스 경로(contract-binding §4.2)·선택 Projection 목록 참조. Proposal·충돌/trade-off·리뷰 상세는 실행 메타 파일 참조로만 가리킨다(코어 밖·SP-INV 2·3). | §3.1-C 출력·§3.4-C 단일 인스턴스 수렴 |
| `MaturationRunConcluded` | run 종결 — 종단 상태(`Matured`/`Skipped`/`Escalated`)와 종결 사유. | §3.4-A 종단 3 |

- **의미 소유 경계.** 위 종류는 **직렬화 어휘**일 뿐이며 상태·전이·종단의 의미·Guard는 04 §3.4 전이표가 소유한다(재정의 0).
- **스킵 경로 기록.** 스킵 경로도 무기록이 아니다 — `StateTransition`(T2)·`GatePresented`/`UserResponded`(경량 확인)·`StateTransition`(T9)·`MaturationRunConcluded`가 남고, 스킵 판정 근거는 `Assessing` 판정 레코드(또는 실행 메타 파일)에 남는다(04 §3.2). 무산출이되 판정 기록은 남는다.

---

## §5. DP-4 — 사용자 게이트 제시·응답 채널 확정 (done 5)

04 §4.1 행2의 물리 실현을 확정한다. `Validating` 상태·전이(T8~T11)·SP-INV 4는 § 포인터로만 인용하고 물리 개입 채널만 확정한다(**discovery-binding §5가 선행 관례**).

### §5.1 물리 채널 — 주 세션 사용자 제시·응답 수령

Solution Design의 모든 사용자 개입(성숙 결과·스킵 판정 제시, 승인/확인/수정/강제 응답 수령)은 **주 세션**(Advisor 바인딩)에서 제시·수령한다(discovery-binding §5·loop-binding §5.2 계보 동형). 주 세션은 Orchestrator 역할(§6)로 State Machine을 구동하는 주체이기도 하므로 구동과 개입 제시가 같은 채널에서 정합한다.

### §5.2 게이트 전이 실의미 (T8·T9·T10·T11)

각 제시·응답은 §4 로그에 `GatePresented`·`UserResponded`로, 뒤이은 전이는 `StateTransition`으로 남는다.

| 사용자 응답 | 전이 (04 §3.4-B) | 실의미 |
|---|---|---|
| **승인** | T8 `Validating`→`Matured` | 성숙 경로 확정 — superseding v(N+1) 발행(contract-binding §4.2 경로) + 선택 Projection. `OutputRecorded`·`MaturationRunConcluded`(Matured). |
| **확인** | T9 `Validating`→`Skipped` | 스킵 경로 확정 — 무산출(vN이 곧 UAHF 소비 대상)·스킵 판정 기록만. `MaturationRunConcluded`(Skipped). |
| **수정 요청** | T10 `Validating`→`Reviewing` | 추가 설계 필요 — `Reviewing` 재진입. 종단 아님. |
| **강제** | T11 임의 비종단→`Escalated` | 사용자 강제(또는 자율 수렴 불가) — 상위(사람) 판단 위임. `MaturationRunConcluded`(Escalated·미완). |

- **승인 전 Matured 도달 불가(SP-INV 4·불가침).** `Matured`·`Skipped` 종단은 반드시 `Validating`의 사용자 응답(T8·T9)을 통과한다(04 §3.8 SP-INV 4·UAF-INV ⑤). 로그 순서상 `UserResponded`가 `StateTransition`(T8/T9)에 **선행**한다 — 이 순서가 게이트 불가침의 물리 증거다.
- **강제 일시중단·재개 semantics.** 04 §4.1 행2가 포함한 "강제 일시중단·재개 semantics"는 T11 `Escalated` 위임으로 실현된다 — 04 §3.4는 `Escalated`를 종단으로 두므로 물리 재개의 상세 semantics는 상위(사용자·Advisor) 판단 소관이며 본 문서는 별도 재개 상태기계를 신설하지 않는다(04 §3.1-D·§3.9·선취 금지).

---

## §6. DP-3 — Expert Role 실행 호스팅 (역할 추상까지만) (done 6)

04 §4.1 행1의 물리 실현을 확정하되 정본이 명시한 대로 **역할 추상까지만** 확정하고 물리 호스팅(실행 코드·자동화)은 **설계하지 않는다**. 정본: "논리 Expert Role을 어느 실행 주체가 호스팅하는가 — **역할 추상까지만** 정의하고 물리 호스팅은 설계하지 않는다(M5)." (**discovery-binding §7이 선행 관례**.)

### §6.1 역할 추상 확정 (형태 A — 규약 절차·기존 위임 관행 재사용)

- **Orchestrator 역할 = 주 세션 규약 절차.** State Machine(04 §3.4)을 구동하는 역할을 **주 세션(Advisor)이 규약 절차로 수행**한다 — Ready vN 결속으로 `Assessing`을 생성하고 복잡도 판정(§3.2)·역할 할당(§3.3)·전이 집행·종단 판정(§3.1-D)·사용자 게이트(§5)를 규약 절차로 실현한다. 전이 규칙을 새로 만들지 않는다(재정의 0).
- **Expert Role 수행 = 기존 위임 실행 관행 재사용.** 논리 Expert Role(04 §3.3)의 호스팅은 **이 환경의 기존 UAHF Agent 위임 실행 관행**(서브에이전트 위임·완료 보고·독립 검증)을 재사용해 실현한다 — `Proposing`의 역할별 Proposal 산출을 위임 실행으로, 회수를 완료 보고로, `Reconciling`·`Reviewing` 통합을 주 세션 규약 절차로 수행한다. **새 병렬 실행 프레임워크를 창설하지 않는다.**
- **최소 할당·개방 네임스페이스 유지.** 실행 주체 할당은 판정 결과가 식별한 관심사에서 파생된 **최소 구성만** 할당한다(04 §3.3·SP-INV 8). 고정 역할 팀을 상시 실행하는 구조를 만들지 않으며(SP-INV 5·8) 역할명은 개방 네임스페이스로 유지한다 — 본 절은 구체 역할명 카탈로그를 명명하지 않고, 구체 역할 예시는 비정본 부록 소관이다(SP-INV 5).
- **물리 호스팅 = 설계 안 함(확장 포인트).** Solution Design을 실행 코드로 자동 호스팅하는 물리 실행 주체·자동화(형태 B 실행 호스팅·step 실행기 연결)는 **설계하지 않는다** — 04 §3.9 확장 포인트이며 여기서 설계하면 04 §4.1 행1과 §3.9를 침범한다. 경계 간 분할은 형태 B 설계 시 확정한다(선취·추측 금지).

### §6.2 코어 문면 무촉·SP-INV 6 무촉

본 절의 물리 매핑은 04 §3.3이 "실행 주체 매핑은 Adapter 소관(M5)·코어는 역할 추상까지만"으로 위임한 지점에만 놓인다. 코어는 UAHF Agent·특정 하네스 실행 주체를 역참조하지 않으며(SP-INV 6·루트 §2.5 폐쇄성), 본 절이 그 위임 지점을 채워도 04 코어 문면(역할 추상)은 무촉이다. `Reviewing`의 통합·단일 일관 결정 집합 수렴·최종 결정 소유권(권위 = 사용자 게이트)은 04 §3.4-C 정본 그대로다.

---

## §7. DP-5 — Policy 데이터 소스·직렬화 + 최소 실값 (done 7 · DP-X5 동형)

04 §4.1 행4의 물리 실현을 확정한다. 복잡도 판정(04 §3.2)·역할 할당(§3.3)·Projection 동적 선택(§3.5)은 § 포인터로만 인용하고 데이터 소스·직렬화 형식과 **최소 실값 1세트**만 확정한다(**discovery-binding §8이 선행 관례**).

### §7.1 데이터 소스·직렬화 형식

- **데이터 소스.** Solution Design Policy 값은 규약 절차에 하드코딩되지 않고 `uahf/framework/adapters/claude/solution-design-data/policy/`의 **데이터 파일**(`default-policy.yaml`)에서 온다(Policy as Data, 04 §3.2). 값 조정은 데이터 정정일 뿐 규약 절차·정본 계약(04 §3.2·§3.3·§3.5)을 변경하지 않는다.
- **직렬화 형식.** 정책 파일은 자기서술 구조화 데이터로 직렬화한다(discovery-binding §8.1 관례 동형·구체 형식은 Adapter 선택, 격리 지점 §10). 물리 정책 데이터 파일은 실재하며(§12) 본 문서는 **형식·값 정본 문면**을 소유한다(L-07).

### §7.2 최소 실값 1세트 (정본 값 표 — DP-X5 동형)

E2E 구동을 위한 **최소 실값 1세트**를 본 문서의 정본 값 표로 확정한다. **단일 소스 규율:** 아래 (가)~(사)의 값은 `policy/default-policy.yaml`과 **한 벌**이다(정본 값 == policy 값·L-07) — 절마다 일치 선언을 반복하지 않으며, 값의 사본을 본 문서·부록의 다른 자리에 두지 않는다(부록은 포인터만·SP-INV 5). 값은 전부 **Policy as Data**이므로 조정은 데이터 정정일 뿐 정본 계약을 변경하지 않는다(04 §3.2).

**(가) 성숙/스킵 판정 기준 (04 §3.2 — 산출은 이진 분기, 판정 기준은 정책 데이터):**

아래 신호 중 하나라도 참이면 **성숙 필요**(→ 역할 할당·`Proposing`), 전부 부재이고 단일 관심사이면 **스킵**(→ `Validating` 경량 확인·T2→T9). 신호는 입력 인스턴스 vN(및 워크스페이스 증거)에서 판정된다.

| # | 성숙 필요 신호 | 근거 필드 (03 §3.2-A) |
|---|---|---|
| 1 | `architectureDirection.open` 비공집합 (미결 설계 결정 존재) | 그룹 6 Architecture Direction |
| 2 | `readiness.openQuestions` 비공집합 (미해결 질문 존재) | 그룹 8 Readiness |
| 3 | `assumptionLedger` 비공집합 (미해결 가정 존재 — ReadyWithAssumptions) | 그룹 7 Assumption Ledger |
| 4 | 다관심사 지표 (설계 관심사 2개 이상 교차) | 판정 근거 종합 |
| 스킵 | 위 1~4 전부 부재 ∧ 단일 관심사 | vN이 곧 UAHF 소비 대상 — T2 `Assessing`→`Validating`, T9 확인→`Skipped` |

**(나) 역할 선택 규칙 (04 §3.3 — Capability 선언·개방 네임스페이스·최소 할당·전체 커버리지 바닥):**

| 항목 | 값 (`roleSelection`) |
|---|---|
| 파생 근거 (`basis`) | 판정 근거가 식별한 설계 관심사(위 (가) 신호가 가리키는 미결 관심사)에서 역할을 파생 |
| 관심사당 역할 (`perConcern`) | 최소 1 (관심사당 최소 필요 역할만) |
| 전문 역할 수 상한 (`maxSpecialistRoles`) | **5** — 전문/관심사 역할만 상한(SP-INV 8). 기본 2(`baseSpecialists`) + 조건부 3(`conditionalSpecialists`)을 담는 값이며 전체 커버리지 바닥(`coverageFloor`)은 이 상한에 **불산입**·configurable(§DC-6). |
| 기본 역할 구성 (`defaultComposition`) | **강제 기본값(이탈 시 사유 기록)** — `coverageFloor`(커버리지 바닥 실현) + `baseSpecialists`(기획·아키텍처) + `conditionalSpecialists`(디자이너/`touchpoint` · DBA/`dataComplex` · 보안/`regulated` — 보안은 심의 참여·산출물 미소유). 조건부 역할은 사람용 산문 `when`과 **기계 신호 `whenSignal`을 병기**하며, form-B 로더(§7A.5)는 산문을 파싱하지 않고 **`whenSignal`을 기계 대조 매칭**해 결정적으로 활성/제외를 계산한다(산문 파싱 금지·결정성). 이는 **책임 있는 자율**(루트 §6 원칙 11 (a)(b))의 물리 실현 — 기본 구성을 비정본 부록이 아니라 **Policy 기본값으로 강제**하되 그것이 **강제 고정팀은 아니다**(`fixedTeam=금지`와 무모순·SP-INV 8 존치). 역할명은 개방 네임스페이스 예시·configurable(§DC-6)이며 예시 해설은 비정본 부록(expert-role-catalog.md §3.5) 소관이다(강제 근거 아님·SP-INV 5). |
| 이탈 규칙 (`deviationRule`) | **silentOmission 금지**(책임 있는 자율 (b)(c)) — 기본 구성에서 역할 추가/제거 시 **사유 기록**(`events/maturation-<run-id>/`) + **Validating 게이트 표면화·사용자 확인**(고임팩트 이탈은 즉시). "기본값이니 조용히 이탈"을 폐기한다. |
| 전체 커버리지 바닥 (`wholeScopeCoverage=required`) | **필수 바닥** — 선언된 전체 프로젝트 범위를 관장하는 커버리지 capability를 반드시 포함한다(04 §3.3·SP-INV 9). 최소 할당(SP-INV 8)의 예외가 아니라 그 위의 필수 바닥이며 전문 역할 상한에 **불산입**된다 — 두 원칙은 **층위가 다르다**(04 §3.3: 최소 할당은 좁은 관심사에 전문 역할을 필요 이상 늘리지 않음을, 커버리지 바닥은 선언 범위 전체가 관장 없이 비지 않음을 규율 — 모순 아님). 커버리지 capability도 고정 역할명이 아니라 Capability 선언으로 표현된다(SP-INV 5). |
| 역할→산출물 소유 맵 (`artifactOwnership`) | 각 `defaultRequiredSet` id의 소유 역할(작성 책임) — `defaultComposition`과 동일 개방 네임스페이스로 **(다) 13 id를 1:1 매핑**(표준 프로파일 기준)(소유 매핑 부재 = form-B 로더 `PolicyError`·교차 정합 강제). 조건부 보조(예: 데이터 복잡 시 `table-def` 정밀화 보조)는 소유가 아니다. 생산 프로토콜은 §7A. |
| 고정 팀 열거 (`fixedTeam`) | **금지** — 역할명은 개방 네임스페이스, 고정 역할 카탈로그 0(SP-INV 5·UAF-INV ⑥). `defaultComposition`은 이 금지의 예외가 아니라 "이탈 가능한 기본값"이므로 무모순. |

**(다) Projection 선택 정책 (04 §3.5 — 동적 선택 = 기본값 opt-out·전 유형 강제 금지·SP-INV 9 기본 필수 세트):**

| 항목 | 값 (`projectionSelection`) |
|---|---|
| 선택 방식 (`mode`) | 프로젝트 유형·복잡도에 따라 **동적 선택** — 04 §3.5의 '동적'은 기본값 opt-in이 아니라 **기본값으로부터의 정당화된 이탈(opt-out)**이다 |
| 전 유형 강제 (`forceAllTypes`) | **금지** — 개방 레지스트리의 모든 가능 유형을 강제하지 않는다. `defaultRequiredSet`(부분집합)의 default-required와 **무모순**(04 §3.5) |
| 정본 실재 시 (`existingCanonical`) | 대상 워크스페이스에 해당 유형 정본이 **이미 실재하면 신규 강제 0** |
| 유형 카탈로그 (`typeCatalog: open-registry`) | 코어(04)는 유형 카탈로그를 알지 않으나(SP-INV 5는 코어만 구속), 본 Adapter Policy는 격리 지점(§0)으로서 **기본 필수 세트를 구체 열거**한다(04 §4.1 행4 위임). 개방 레지스트리 전체 카탈로그는 부록 소관이며 `defaultRequiredSet`은 그중 성숙 경로 default-required 부분집합이다. |

**기본 필수 Projection 세트 (`defaultRequiredSet` — 13종·성숙 경로 default-required 부분집합):**

| id | 이름 (`name`) | 요건 클래스 (`requirement`) |
|---|---|---|
| `project-plan` | 프로젝트 계획서 | `always` |
| `requirements-def` | 요구사항 정의서 | `always` |
| `business-process` | 업무 프로세스 | `always` |
| `functional-spec` | 기능 명세서 | `always` |
| `table-def` | 테이블 정의서 | `always` |
| `test-plan-cases` | 테스트 계획·케이스 | `always` |
| `screen-list` | 화면 목록 | `touchpoint` |
| `menu-structure` | 메뉴 구조도 | `touchpoint` |
| `screen-design` | 화면 설계서 | `touchpoint` |
| `interface-spec` | 인터페이스 명세서 | `interface` |
| `design-tokens` | 디자인 토큰·톤앤매너 확정 기록 | `touchpoint` |
| `screen-mock` | 화면 mock(HTML) | `touchpoint` |
| `mock-convergence-record` | mock 수렴 확정 기록 | `touchpoint` |

(마지막 3종 = **Visual Contract 트랙** 가법 — 소유 = 디자이너((나) `artifactOwnership`). `design_completeness` 체커가 침묵 누락을 차단하고, 요소 단위 강제는 (바) `designElements`가 담당한다. 요소별 작성 가이드는 비정본 부록 `planning/docs/appendix/visual-contract-catalog.md` 소관이다 — 강제 근거 아님·SP-INV 5.)

**요건 클래스 (`requirementClasses`):**

| 클래스 | 의미 |
|---|---|
| `always` | 항상 default-required — 제외는 설계단계 명시 결정 + 사유 기록 + 사용자 확인만 |
| `touchpoint` | 접점(웹·앱·포털) 선언 시 required — 미선언 시 클래스 제외: 표면화·확인 필요(`classExclusions`) |
| `interface` | 외부 연계 선언 시 required — 미선언 시 클래스 제외: 표면화·확인 필요(`classExclusions`) |

**제외 규칙 (`exclusionRule` — SP-INV 9 침묵 누락 금지):**

| 규칙 | 값 |
|---|---|
| `silentOmission` | **금지** — 산출도 제외 기록도 없이 구현 경계를 넘기지 않는다(04 §3.8 SP-INV 9) |
| `classExclusionOnNonDeclaration` | 표면화 — `declaredTouchpoints`/`declaredInterfaces` 공집합으로 클래스가 제외되면 매니페스트 `classExclusions.<class>{reason,confirmedBy}` 필수. **조용한 자동 N/A 금지**(silentOmission 금지 동형). |
| `manualExclude` | `always` 클래스 제외 시 사유 기록 + 사용자 확인 — 성숙 run 기록(`events/maturation-<run-id>/`)에 남긴다 |

**경량 프로파일 (`lightweight-policy.yaml` — 절차 비례화 트랙 W1-a · 사용자 확정 Q-1):**

Solution Design Policy 프로파일은 **2종**이다 — 표준 `policy/default-policy.yaml`(위 13종) · 경량 `policy/lightweight-policy.yaml`(통합 설계 문서 1종). 둘 중 어느 파일을 대상 워크스페이스에 두는가의 절차는 **§7A.2-S**(workspace policy 시드)가 소유한다. 두 프로파일 공통 절의 **값 정본은 본 §7.2**이며, 표준 프로파일 값 개정 시 경량 파일의 공통 절도 동기 갱신 대상이다(드리프트 통제 지점).

| 항목 | 표준 프로파일 | 경량 프로파일 |
|---|---|---|
| `projectionSelection.defaultRequiredSet` 항목 수 | 13 | **1** |
| 그 항목 | 위 13종 표 | `{ id: solution-design, name: 통합 설계 문서, requirement: always }` |
| `artifactOwnership` | 13 id와 1:1 | **1 id와 1:1** — `solution-design` owner = `PM`(`coverageFloor` 역할 — 통합 문서가 선언 전체 범위를 한 문서로 관장하므로 전체 커버리지 관장 역할 소유·04 §3.3·SP-INV 9). 전문 역할은 소유 0·절 단위 기고·심의 참여 |
| `requirementClasses` | `always`·`touchpoint`·`interface` 3종 | **3종 동일 문면**(정의 삭제 0 — 경량 세트에 touchpoint/interface 클래스 항목이 0이라 두 클래스는 미발화하나, 프로젝트 policy 사본이 선언-조건부 항목을 가법 등재할 때 그대로 소비된다((바) 말미 편입 패턴)) |
| `exclusionRule` | `silentOmission` 금지 · `classExclusionOnNonDeclaration` 표면화 · `manualExclude` | **동일 문면**(제외 규칙 완화 0) |
| (가) 판정 신호 · (나) 역할 선택 · (라) 심의 · (바) 디자인 요소 · (사) 원칙 | 위 각 절의 값 | **표준과 동일 값**(신호·역할·상한·라운드·요소·원칙 축소 0) |

- **경량 = 산출물 종수 축소만이다.** 검증 하한은 무변경 — 경량 레인에서도 `design_completeness` **동일 체커**가 동일 규칙(침묵 누락 차단·정당화 제외 요건)으로 판정하며 새 체커·병행 게이트를 두지 않는다. 접점을 선언하면 (바) `designElements` 요소 단위 강제가 그대로 발화한다(통합 문서 1종 체제에서는 요소 `covered`의 `pointer`가 그 문서의 절을 지목한다).
- **id `solution-design`의 본문 경로 = `<workspace>/docs/solution-design.md`** (배치 규약 §7A.2). 이 값은 seed 프롬프트가 가정하는 SD 입력 경로와 정합한다(접합부 정합 판정은 W1-b 소관).
- **프로파일 파일은 완결이어야 한다(사본이 아니라 프로파일인 이유).** 체커·로더는 워크스페이스 고정 상대경로의 **단일 정책 파일**만 읽고 두 파일을 병합하지 않으며, 오버레이·include 기구가 코드에 **0**이다. `roleSelection`·`artifactOwnership` 부재는 `solution_design_resolve`의 `PolicyError`로 즉시 실패한다. 따라서 공통 절의 물리 중복은 회피 불가다.

(`uaf-verified:` 위 표·항목의 코드·데이터 주장은 `policy/default-policy.yaml`과 `policy/lightweight-policy.yaml` 키 트리 대조, `orchestration/adapters/claude/design_completeness.py`(`_load_policy_required`·`_check_design_elements`·클래스 제외 블록)와 `planning/adapters/claude/solution_design_resolve.py`(`load_policy`·`_compute_role_composition`·`_build_owner_map`·`_compute_artifact_plan`) 판독, 그리고 경량 프로파일 × 1종 매니페스트 실행 2건(산출 → `[DESIGN-COMPLETE]` exit 0 / 미산출 → `[DESIGN-INCOMPLETE]` exit 2)과 로더 실행 1건(exit 0·`artifactPlan` 1항·owner PM) 실측으로 얻었다. **검색 범위 = 위 4파일 + 두 policy 파일**이며, 그 밖(소비 프로젝트 워크스페이스 실 시드·엔진 run 경유 왕복·`pretooluse_design_guard` 라이브 발화)은 이 개정의 실측 범위 밖이다.)

**(라) 다라운드 심의 정책 (04 §3.4-C — §7B 규약 절차의 policy 측 파라미터·§DC-5):**

여기 (라)가 `deliberation` 실값의 정본 값 문면이며, **§7B.4는 소비 지점(어느 절이 어느 키를 읽는지)만** 둔다(분업: 소비 지점 표 = §7B.4 / 값 = 여기).

| 키 (`deliberation`) | 값 | 결정하는 것 |
|---|---|---|
| `maxRounds` | **3** | T5 재제안 라운드 상한(라운드 1 + 재제안 최대 2). 상한 도달 시 라운드를 더 열지 않고 잔여 충돌을 `Validating` 게이트에 표면화(§7B.5·configurable). |
| `convergence` | `unresolvedConflictsZero` | 수렴 기준 — 미해소 충돌 0으로 T4/T6 수렴을 인정(04 §3.4-B Guard의 policy 측 파라미터·§7B.3·§7B.5). |
| `peerVisibility` | `conflictParties` | 라운드 2+ 동료 Proposal 동봉 범위 기본값(충돌 당사자만·경량). 허용값 `conflictParties` 또는 `allActive`(전 활성 역할 동봉으로 상향 가능·configurable·§7B.2). |
| `deviationRule` | **silentOmission 금지** — 심의 기본값(위 3키)에서 이탈 시 사유 기록(`events/maturation-<run-id>/`) + `Validating` 게이트 표면화·사용자 확인(고임팩트 이탈은 즉시). `roleSelection.deviationRule` 문면 동형. |

**(바) 디자인 필수 요소 정책 (`designElements` — Visual Contract 트랙·책임 있는 자율 (a) 물리 실현):**

디자인 필수 요소를 **비정본 부록이 아니라 Policy 데이터 + 게이트로 강제**한다(루트 §6 원칙 11 (a)·§DC-1 동형 패턴). `projectionSelection`과 형제 레벨의 최상위 키이며 접점 선언 시에만 적용된다(`appliesWhen: touchpoint` — 미선언 시 비적용·`classExclusions` 경로가 커버).

| 키 (`designElements`) | 값 | 결정하는 것 |
|---|---|---|
| `appliesWhen` | `touchpoint` | 접점(`declaredTouchpoints`) 선언 시에만 적용. 미선언 시 섹션 전체 비적용. |
| `screenScope` (7종) | UI: `layout-structure`·`navigation`·`component-states`(기본·로딩·빈·오류·비활성 5종)·`data-rules`·`responsive`(브레이크포인트 최소 1) / UX: `error-recovery`(복구 경로)·`feedback-rules`(알림 방식) | **화면 단위** — 각 화면이 covered 또는 정당화 excluded 해야 하는 필수 요소. |
| `projectScope` (4종) | UI: `design-tokens-values`·`tone-and-manner`(스케일 선택·레퍼런스 앵커·금지 목록)·`accessibility-floor`(명도 대비·포커스 표시·터치 타겟) / UX: `user-journey-map`(핵심 여정) | **프로젝트 단위 1회** 필수 요소. |
| `exclusionRule.silentOmission` | **금지** | 요소 단위 제외 = `reason` + `confirmedBy` 필수(산출물 제외와 동형). |

- **체커 판정 경계.** `design_completeness` 체커는 활성 시 매니페스트 `designElements.{project,screens}`의 **선언 완전성만** 결정적으로 판정한다(projectScope 전 요소 + screens 비공집합 + 각 화면 × screenScope 전 요소가 covered/정당화 excluded). `covered`의 진위·화면 목록 대응 진위는 내용 파싱 없이 불가하므로 **CP2/사용자 게이트(mock 리뷰) 몫**이다(design-manifest.schema.md 경계 문면 동형). 하위호환: 정책에 `designElements` 부재 시 검사 전면 비적용.
- **책임 있는 자율 정합.** 필수 요소 커버는 Policy + 게이트로 강제하고(원칙 (a)), 요소 단위 제외는 `reason`+`confirmedBy`로 사유 기록(원칙 (b)), Validating 게이트에서 일괄 표면화한다(원칙 (c)·§7A.4). 요소별 작성 방법론·예시는 비정본 부록 — **강제 근거 아님**(SP-INV 5).
- **`accessibility-floor.criteria`(접근성 실값·정보성).** 선택 필드 `criteria`(문자열 목록)로 접근성 실값을 병기한다: 본문 명도 대비 ≥ 4.5:1(WCAG AA)·대형 텍스트 ≥ 3:1·터치 타겟 ≥ 44×44px·키보드 탐색·포커스 표시·의미 있는 대체 텍스트. `criteria`는 **검증 게이트(사람 판정)의 기준 문면**이며 체커는 판정하지 않는다(체커는 선언 완전성만·추가 키 tolerant). 접근성 원칙 중 기계 판정 가능분의 물리화 지점이다((사) `accessibility`와 상호 참조).
- **UX 요소 경계(중복 오해 방지).** `component-states`(상태 화면의 **존재**) vs `feedback-rules`(알림·피드백 **방식**) vs `error-recovery`(복구 **경로**)는 서로 다른 축이다.
- **제품 의존 항목은 기본 필수에 넣지 않는다(오버엔지니어링 방지·사용자 결정 2026-07-19).** 기본 필수는 결함-인접·보편 항목만 둔다 — **제품 의존 항목(온보딩·사용자 유형 상세·UX 카피·다국어 등)은 기본 필수 세트에 넣지 않는다**(형식적 제외 기록 양산 방지). 인터뷰·설계에서 필요가 선언되면 **해당 프로젝트의 policy 사본에 데이터로 추가**(Policy as Data·프레임워크 무변경)하여 그 프로젝트에서만 required가 된다 — 기존 `touchpoint`/`interface` **선언-조건부 패턴과 동형**이다. 편입 후보 목록·절차는 비정본 부록 소관이다.

**(사) 디자인·사용성 원칙 (`designPrinciples` — designElements 형제·Policy as Data):**

디자이너 역할이 화면을 설계할 때 따르고 mock 수렴 리뷰(§7C)·검증 게이트가 대조하는 **UI 디자인 원칙 7종 + UX 사용성 휴리스틱 10종 = 17종**을 Policy 데이터로 등재한다. `gist`는 자체 문면이며(원문 전재 아님) 출처는 참고 앵커로만 인용한다(UI: https://www.figma.com/ko-kr/resource-library/ui-design-principles/ · UX: https://www.nngroup.com/articles/ten-usability-heuristics/ · UAF-INV ⑥ 정합·방법론 고유명 0). 해설·예/반례는 비정본 부록 소관이며 **강제 근거가 아니다**(SP-INV 5).

| id | 이름 (`name`) | 요지 (`gist`) |
|---|---|---|
| `hierarchy` | 계층 구조 | 크기·두께·색·간격으로 정보 우선순위를 시각적으로 유도한다. |
| `progressive-disclosure` | 점진적 공개 | 단계당 적정 정보량만 노출하고 진행 상황을 명시한다. |
| `consistency` | 일관성 | 패턴을 전체에서 동일하게 유지하고, 이탈은 근거를 요구한다. |
| `contrast` | 대비 | 중요 동작·정보에 시각적 우선순위를 부여한다. |
| `accessibility` | 접근성 | 모두가 지각·조작 가능하게 한다. 기계 판정분은 `accessibility-floor.criteria`로 물리화(상호 참조). |
| `proximity` | 근접성 | 관련 있는 요소를 가까이 배치해 관계를 드러낸다. |
| `alignment` | 정렬 | 그리드 기반으로 요소를 정렬해 질서·스캔 가능성을 만든다. |
| `visibility-of-system-status` | 시스템 상태 가시성 | 지금 무슨 일이 일어나는지 적시 피드백으로 알린다. |
| `match-real-world` | 실세계 일치 | 사용자 언어·개념·순서로 말한다(시스템 용어 강요 금지). |
| `user-control-freedom` | 사용자 제어와 자유 | 실수 후 나갈 비상구·되돌리기/다시하기를 제공한다. |
| `consistency-standards` | 일관성과 표준 | 같은 것을 같게 표현하고 플랫폼 관례를 따른다. (UI 원칙 `consistency`와 계열 상이 — 중복·상충 조정은 리뷰 게이트 몫·상호 참조) |
| `error-prevention` | 오류 예방 | 오류 메시지보다, 오류가 나지 않도록 설계로 막는다. |
| `recognition-over-recall` | 회상보다 인지 | 필요 정보를 노출해 기억 부담을 줄인다. |
| `flexibility-efficiency` | 유연성과 효율 | 초보·숙련 모두를 위해 단축 경로를 제공한다. |
| `aesthetic-minimalism` | 미니멀리즘 | 관련 없는 정보를 덜어 신호 대 잡음을 높인다. |
| `error-recognition-recovery` | 오류 인식·진단·복구 | 오류를 평이한 말로 알리고 원인·해결책을 제시한다. |
| `help-documentation` | 도움말·문서 | 필요 시 찾기 쉬운 도움말·구체 절차를 제공한다. |

- **강제 지점(라우팅).** 원칙의 강제는 **Policy `designPrinciples` + 브리프/리뷰 배선**에 있다 — (1) 디자이너 역할 브리프에 `designPrinciples` **전체** 주입 + 화면설계서에 원칙별 적용 근거를 **문서 단위 1회**(원칙별 1줄 개요 절·화면마다 반복 금지) 기록 요구(§7A.1·침묵 생략 불가·원칙 (b)), (2) §7C mock 리뷰의 리뷰 차원 = `designPrinciples` **전체** 대조. 배선이 전체를 참조하므로 종수 증가에 **배선 문면 변경 없이 자동 편입**된다(Policy as Data). 해설·예/반례는 비정본 부록 — **강제 근거 아님**(SP-INV 5).

---

## §7A. 산출물 생산 프로토콜 (form-A 규약 — 주 세션이 따르는 절차)

Solution Design이 **기본 필수 Projection 세트(§7.2 (다))를 어떻게 생산하는가**의 절차를 form-A 규약으로 확정한다. 이 절은 **실행 코드가 아니라 주 세션(Advisor)이 따르는 규약 절차**이며(§0 형태 A), 04 §3.3·§3.4·§3.5·SP-INV 7·9를 재정의하지 않고 § 포인터로 인용한다. 물리 실현은 §6·§7·§4·§5 위에 얹힌다. 절 번호를 `§7A`로 둔 것은 이후 §8~§13 번호·교차참조를 보존하기 위한 무침습 삽입이다.

**책임 있는 자율 정합(루트 §6 원칙 11).** (a) 필수 산출·전 범위 커버를 Policy(§7.2 (다))와 게이트(§5·`design_completeness`)로 강제하고, (b) 남은 자율은 Policy 기본값(§7.2 (나)) + 이탈 시 사유 기록(`deviationRule`)으로 두며, (c) 이탈·제외를 Validating 게이트에서 일괄 표면화한다. 부록은 **예시 문서일 뿐 강제 근거가 아니다**(원칙 (a)).

### §7A.1 위임 산출 (역할별 소유 산출물 · 컨택스트 위생)

- **각 역할 = 위임 서브에이전트가 자기 소유 산출물 작성.** `Proposing`(04 §3.4-A)에서 각 Expert Role(§7.2 (나))은 **fresh-context 위임 서브에이전트**로 수행되어 `artifactOwnership`이 지정한 **자기 소유 산출물만** 작성한다. §6.1이 확정한 "Expert Role 수행 = 기존 위임 실행 관행 재사용"의 산출물 생산 국면 실현이다.
- **주 세션은 조율·검증만·내용 직접 작성 안 함.** 주 세션은 Orchestrator 규약 절차(§6.1)로 역할 파생·디스패치·`Reconciling`/`Reviewing` 통합·게이트만 수행하고 **산출물 본문을 직접 작성하지 않는다** — 컨택스트 위생. 이는 04 §3.4-C 최종 결정 소유권(권위 = 사용자 게이트)과 무모순이다.
- **최소 할당 존치.** 위임 대상 역할은 `defaultComposition` 기본값에서 복잡도 판정이 요구하는 만큼만 편입되며(조건부 역할은 신호 충족 시) 이탈은 `deviationRule`로 기록된다(SP-INV 8).
- **디자인 원칙 주입(§7.2 (사)).** 디자이너 역할 브리프에 Policy `designPrinciples` **전체**(종수 증가 시 자동 편입)를 **주입**한다(brief-template 원칙 주입 슬롯). 화면 설계 산출물(`screen-design`)에는 각 원칙의 **적용 근거를 원칙별 1줄로, 화면설계서 문서 단위 1회**(원칙별 1줄 개요 절) 기록하도록 요구한다 — **화면마다 반복하지 않는다**(마찰 상한·형식적 보일러플레이트 방지·사용자 결정 2026-07-19). 원칙을 **침묵 생략하지 않는다**(silentOmission 금지 동형; 문서 전체에 비적용인 원칙은 "해당 없음 + 사유"를 남긴다). 이 기록은 §7C mock 리뷰·검증 게이트가 대조하는 근거가 된다.

### §7A.2 형식·배치 (Markdown 본문 + 기계 색인 매니페스트)

- **본문 = Markdown(사람+AI 겸용·중복 0).** 각 산출물 본문은 단일 Markdown 문서로 `<workspace>/docs/*.md`에 배치한다(같은 내용을 다른 형식으로 중복 저장하지 않는다).
- **기계 색인 = `design-manifest.json`.** 산출/제외 상태의 기계 판독 색인은 `design-manifest.json`(`orchestration/adapters/claude/design-manifest.schema.md` 스키마)이며 `artifacts[].id`는 `defaultRequiredSet[].id`와 대응한다. 소유 역할 매핑의 정본은 Policy `artifactOwnership`이고 매니페스트는 각 id의 `produced`/`excluded` 상태를 기록한다(체커 소비 표면).
- **구조화 사이드카 = 다운스트림 소비 시에만.** 구조화 사이드카(예: `table-def`의 `schema.json`)는 **다운스트림 코드생성이 실제 소비할 때에만** 산출한다(불필요 산출 방지·Markdown 본문이 1차 정본).
- **배치 스코프(SP-INV 7 워크스페이스 귀속).** 본문은 `<workspace>/docs/`, 매니페스트는 `<workspace>/.claude/solution-design/design-manifest.json`에 둔다 — **대상 워크스페이스 귀속**이며 성숙 run 디렉터리가 아니다(04 §3.7). run 디렉터리에는 실행 메타·이벤트 로그만(§3·§4).

**§7A.2-S — workspace policy 시드 (절차 항 · form-A · 절차 비례화 트랙 W1-a 신설).**

체커·로더는 정책을 워크스페이스 **고정 상대경로**에서 읽고 그 경로는 config 키·환경변수로 바꿀 수 없다. 그러므로 프로파일 선택은 **그 자리에 어느 프로파일 파일을 놓는가**로 환원된다. 성숙 run 착수 전에 주 세션이 아래 3항을 수행한다.

| # | 항 | 내용 |
|---|---|---|
| (S1) | **표준/경량 선택** | 프로파일은 2종 중 하나다 — 레인 값 `standard` → 표준 `uahf/framework/adapters/claude/solution-design-data/policy/default-policy.yaml`(13종) · 레인 값 `lightweight` → 경량 `.../policy/lightweight-policy.yaml`(통합 설계 문서 1종·§7.2 (다) 경량 값표). 선택은 이진이며 제3의 값을 두지 않는다. 선택 주체·판별식은 레인 판별 소관(이 절은 판별하지 않고 **소비**한다)이고 미판정·선언 부재는 `standard`로 귀결한다(안전측). |
| (S2) | **대상 경로에 배치** | 선택한 프로파일 파일을 `<workspace>/.claude/solution-design/policy/default-policy.yaml`에 **파일명 `default-policy.yaml`으로** 둔다(체커·로더가 읽는 고정 상대경로 — 경량을 선택해도 원본 파일명 `lightweight-policy.yaml`을 그 자리에 쓰지 않는다). 배치 후 `design_completeness.py <그 경로> <design-manifest.json>` 이 정책 부재로 차단하지 않음을 확인한다. |
| (S3) | **원장 기록** | 시드한 프로파일을 성숙 run 원장에 남긴다 — `MaturationRunStarted`의 "사용한 policy 참조"(§4.3)와 성숙 인스턴스 `provenance`의 "Policy 참조"(§8.1)에 **원본 프로파일 파일명 + 프로파일 종류(표준/경량)**를 기록한다. 신규 레코드 종류·신규 필드는 0이다. 기록 없는 시드는 금지다(설계 산출 원장 기록 의무). 표준 기본값에서 경량으로 이탈한 경우는 `deviationRule` 동형으로 **사유를 함께 기록**하고 `Validating` 게이트에서 표면화한다(silentOmission 금지·§7A.4 (iii)). |

(`uaf-verified:` 고정 상대경로 주장은 `orchestration/adapters/claude/resolve_gate.py`의 `SD_DATA_REL` 상수와 `pretooluse_design_guard.py`의 동일 문면 상수, 그리고 `design_completeness.py` `_load_policy_required`의 정책 부재 차단 분기를 직접 판독해 얻었다 — 두 상수는 별도 선언이며 config 키·환경변수 경유 재정의 지점은 두 파일에서 발견되지 않았다. **검색 범위 = 위 3파일 + `solution_design_resolve.py` `load_policy`**이며, 소비 프로젝트 워크스페이스에서의 실제 시드 실행은 이 개정의 실측 범위 밖이다(미검증).)

**§7A.2-L — 경량 프로파일 본문 경로 규약 (절차 항 · form-A · 절차 비례화 트랙 W1-b 신설).**

경량 프로파일(§7.2 (다) 경량 값표 · 시드 절차 §7A.2-S)의 필수 산출물 1종 `solution-design` 의 **본문 경로와 매니페스트 `path` 값**을 확정한다. 위 배치 스코프의 특수화 1항이며 새 규약을 창설하지 않는다.

| 항목 | 값 |
|---|---|
| 본문 실경로 | `<workspace>/docs/solution-design.md` — 위 배치 스코프(`<workspace>/docs/*.md`)의 파일명 = id + `.md`. 이 절대경로는 엔진 seed 프롬프트가 SD 입력으로 가정하는 경로(`orchestration/adapters/claude/contract_to_graph.py` `_solution_design_path` = `<project_root>/docs/solution-design.md` · `project_root` = `config.workspace_dir`)와 **동일 파일을 지목**한다 — 접합부 정합. |
| 매니페스트 `path` 값 | **`../../docs/solution-design.md`** — `path` 해석은 매니페스트 디렉터리 기준 상대이며(`design-manifest.schema.md`) 매니페스트는 `<workspace>/.claude/solution-design/` 에 있으므로 본문까지 2단 상향이다. |
| 쓰지 않는 값 | `docs/solution-design.md` — `<workspace>/.claude/solution-design/docs/solution-design.md` 로 해석되어 `design_completeness` 가 `path 부재` 로 차단한다(실측 exit 2). 스키마 구예시 표기이며 이 배치에서는 틀린 값이다. |
| 코드 개정 | **0** — 경량 레인은 `contract_to_graph.py` 무수정으로 정합한다(diff hunk 0 실측). |
| 표준 레인 | **미해소** — 표준 프로파일 13종의 seed 입력 가정 결함(`contract_to_graph.py` `_solution_design_path` 단일 파일 가정)은 이 항의 범위 밖이다(후속 트랙 소관 · 좌표 = `docs/proportionality-track-ledger.md` §6.3 항 1). 이 항은 경량 레인만 정합시킨다. 부기: 함께 좌표로 적었던 `design-manifest.schema.md` **예시 2종의 `artifacts[].path` 구표기**는 절차 비례화 트랙 Wave 5(2026-07-27)가 `../../docs/<id>.md` 로 제자리 정정해 **해소**됐다(uaf-allow-legacy: W1-b 시점 미해소 좌표의 이력 인용 — 상태 갱신 표기). |

실동작 예시(JSON 1건)와 해석식 대조표의 정본은 `orchestration/adapters/claude/design-manifest.schema.md` §경량 프로파일 예시이며, 본 절은 값의 사본을 두지 않고 **경로 규약만** 확정한다(단일 소스 규율·§7.2 머리 동형).

(`uaf-verified:` 위 표의 경로·차단 주장은 임시 워크스페이스 1건(경량 policy 시드 + `docs/solution-design.md` 실물 + 매니페스트)에 `design_completeness.py` 를 2회 실행한 실측(`../../docs/…` → `[DESIGN-COMPLETE]` exit 0 / `docs/…` → `[DESIGN-INCOMPLETE]` exit 2)과, `contract_to_graph._solution_design_path` 산출 절대경로 대 매니페스트 `path` 해석 절대경로의 문자 단위 동일 대조(True·len 168), 그리고 `git diff --stat` 상 `contract_to_graph.py` hunk 0 확인으로 얻었다. **검색 범위 = `design_completeness.py`·`contract_to_graph.py`·경량 policy 1파일 + 임시 워크스페이스 1건**이며, 소비 프로젝트에서의 엔진 run 경유 실왕복과 표준 레인 정정은 이 개정의 실측 범위 밖이다(미검증·미해소).)

### §7A.3 검증 3층 (CP1→CP2→CP3 + 사용자 게이트)

산출물 검증은 3층으로 쌓이며(`uahf/specs/02-agent.md` §3.2 CP1·CP2·CP3 동형) 각 층의 검사 범위(scope)는 정직하게 구분된다.

| 층 | 주체 | 검사 대상·근거 |
|---|---|---|
| **CP1** | 각 역할(위임 서브에이전트) | 자기 소유 산출물 자체점검 — 소유 산출물의 done 항목 충족. 자체 점검은 최종 승인이 아니다. |
| **CP2** | 전체 커버리지 역할(`coverageFloor`) + `design_completeness` 결정적 체커 | 횡단 완결성 판정 — 선언 범위(접점·연계) 대비 기본 필수 세트 커버/정당화 제외를 매니페스트 기준으로 결정적 검증(침묵 누락 차단·SP-INV 9). |
| **CP3** | Advisor(주 세션) | 최종 승인 — 매니페스트·커버리지 리포트 기반 승인이며 **전 산출물 전수 정독이 아니다**(컨택스트 위생·CP2 결정적 판정에 위임). |

- 3층 위에 **Validating 사용자 게이트**(§5·04 §3.4 T8~T11)가 놓인다 — 최종 성숙/스킵은 사용자 응답을 통과한다(SP-INV 4·불가침).
- CP2의 결정적 체커는 매니페스트를 **판독만** 한다(산출은 SD·검증은 오케스트레이션).

### §7A.4 사용자 컨펌 시점 (책임 있는 자율 (c) 정합)

| # | 시점 | 실현 |
|---|---|---|
| (i) | **제외 발생 시 inline** | `always` 클래스 산출물을 제외할 때 매니페스트 `confirmedBy`에 사용자 확인을 즉시 기록(`excluded` 요건·§7.2 `manualExclude`). |
| (ii) | **Validating 게이트 일괄** | 성숙 종단 직전 Validating(§5)에서 **전체 산출물 + 매니페스트를 일괄 제시·승인**(`deviationRule.surface`). |
| (iii) | **고임팩트 이탈 즉시** | 기본 구성·필수 세트에서의 고임팩트 이탈은 (ii)를 기다리지 않고 즉시 표면화(원칙 11 (c)). **접점/연계 미선언에 의한 touchpoint/interface 클래스 전체 제외는 고임팩트 이탈이므로 표면화·확인**(`classExclusions.<class>{reason,confirmedBy}`·`classExclusionOnNonDeclaration`) — 없으면 `design_completeness` 체커가 차단. |

이 세 지점은 silentOmission 금지(SP-INV 9)의 사용자 개입 실현이며 04 §3.4·SP-INV 4·9를 재정의하지 않는다.

### §7A.5 form-B 배선 흐름 (결정적 부분 물리화 — 실행 호스팅은 여전히 미설계)

§7A.1~§7A.4의 form-A 규약 중 **결정적으로 계산 가능한 부분**(어떤 역할을 띄우고·각자 무엇을 소유하며·접점/연계/데이터복잡 선언에 따라 무엇이 필수인지)을 form-B 로더 `planning/adapters/claude/solution_design_resolve.py`로 물리화한다. 이 로더는 `entry_resolve.py`·`design_completeness.py`와 **동일 성격**이다 — LLM 0·결정적·오프라인 안전·순수 판독·계산해서 방출까지만(실행 안 함).

| # | 단계 | 주체 | 성격 |
|---|---|---|---|
| (1) | SD 복잡도 판정에서 **접점/연계/데이터복잡 신호 확정** — 입력 인스턴스 vN·워크스페이스 증거에서 판정(§7.2 (가)). 03에 접점 구조필드가 없으므로 주 세션이 주입한다(entry_resolve `--folder` 주입 동형·§DC-8). | 주 세션(Advisor) | 규약 절차(form-A) |
| (2) | `solution_design_resolve.py --policy <policy.yaml> [--touchpoints …] [--interfaces …] [--data-complex]` 호출 → `roleComposition`(활성/제외 근거)·`artifactPlan`(id·name·owner·requirement·required)·`manifestScaffold` 수령. | form-B 로더 | 결정적·LLM 0 |
| (3) | 브리프 템플릿(`solution-design-brief-template.md`)을 `artifactPlan`으로 채워 **역할별 위임 브리프 발부** — 각 역할을 fresh-context 서브에이전트로 소환(주 세션 form-A·§6.1). **로더가 소환하지 않는다.** | 주 세션(Advisor) | 규약 절차(form-A) |
| (4) | 각 역할이 **자기 소유 산출물 작성**(`<workspace>/docs/<id>.md`) + `design-manifest.json` 해당 artifact `status`를 `pending`→`produced`(또는 정당화 `excluded`)로 갱신·CP1 자체점검. | 역할 서브에이전트 | 위임 실행 |
| (5) | CP2 — `design_completeness.py <policy.yaml> <design-manifest.json>` 결정적 체커로 횡단 완결성 판정(침묵 누락 차단·SP-INV 9). | 커버리지 역할 + 결정적 체커 | 결정적 |
| (6) | Validating 사용자 게이트(§5·04 §3.4 T8~T11) — 성숙/스킵은 사용자 응답 통과(SP-INV 4·불가침). | 주 세션 + 사용자 | 게이트 |

- **실행 호스팅은 여전히 미설계(04 §3.9).** form-B 로더는 (2)의 **계산·방출까지만** 한다 — 역할 서브에이전트를 자동 소환·구동하거나 본문을 자동 생성하는 실행 코드는 **설계하지 않는다**(§6.2가 명시 유보). (3)의 소환은 주 세션이 form-A로 수행하는 **기존 위임 관행 재사용**이다. 로더가 subagent를 spawn하거나 Agent/Task API를 호출하면 경계 위반이다.
- **결정적/비결정적 분담.** (1)·(3)·(4)·(6)은 판단·실행을 요하는 form-A 규약이며 (2) 역할 구성/소유/필수 계산과 (5) 완성도 판정만이 결정적 form-B로 물리화된다 — §0 형태 A→B 공존(structure.md §7 C-1)과 정합한다.
- **manifestScaffold는 뼈대일 뿐.** 로더가 방출하는 `status="pending"`은 **작업중 placeholder**이며 체커는 `produced`/`excluded`만 인정한다.

---

## §7B. 다라운드 심의 규약 절차 (form-A 규약 — 주 세션이 구동하는 T5·T7 라운드)

04 §3.4-C가 규정한 **다라운드 심의**(단일 라운드 블라인드 병렬이 아니라 전문가가 서로의 Proposal을 검토·반응하며 수렴 — T5 재제안·T7 잔여충돌 재노출이 그 경로다)를 **바인딩 규약 절차 층**으로 물리 실현한다. 이 절은 **실행 코드가 아니라 주 세션이 Orchestrator 규약 절차(§6.1)로 따르는 form-A 규약**이며, 04 §3.4-A 상태·§3.4-B 전이(T3~T7)·§3.4-C·SP-INV 8을 **재정의하지 않고 § 포인터로만 인용한다**.

**불침범 경계(선취·추측 금지).** 이 절이 물리화하는 것은 **라운드 진행·브리프 발부·동료 Proposal 동봉·종료 판정·표면화**뿐이다. **실행 호스팅**(형태 B step 실행기·역할 자동 소환·라운드 자동 구동·본문 자동 생성)은 04 §3.9 확장 포인트로 **여전히 미설계**이며(§6.1·§6.2·§7A.5 말미) 이 절은 그것을 침범하지 않는다 — 라운드는 기존 위임 실행 관행을 반복 적용하는 것이지 새 실행 프레임워크가 아니다(§6.1 "새 병렬 실행 프레임워크를 창설하지 않는다" 보존).

### §7B.1 라운드 1 = 초기 위임 (전 활성 역할 form-A 참여 브리프 — 비소유 역할 포함)

- **라운드 1 = 기존 §7A 위임.** 첫 라운드는 §7A.1·§7A.5 (3)이 확정한 `Proposing` 초기 위임 그대로다 — 각 Expert Role(활성 조건부 역할 포함)이 fresh-context 서브에이전트로 자기 Proposal을 산출한다. T3(`Proposing`→`Reconciling`)은 **할당 역할 전원 Proposal 제출** Guard이므로 브리프가 발부되지 않은 활성 역할이 있으면 이 Guard가 결착 불가(공백)에 빠진다.
- **전 활성 역할에 브리프 발부(비소유 역할 포함 — 결착 공백 차단).** 발부 대상은 **`roleComposition`이 활성화한 전 역할**이며, **산출물을 소유하지 않는 활성 역할(예: 횡단 리뷰 관심사)에도 form-A 참여 브리프를 발부한다**. 이는 §7A.5 (3)의 form-B 유래 소유 브리프(로더 `artifactPlan[].owner` 필터)와 병존한다 — **form-B 소유 브리프는 owner 기준을 유지**하고, 비소유 활성 역할에는 **소유 산출물 없이 심의에 참여**(자기 관심사 Proposal·충돌 지적·커버리지 점검)하는 참여 브리프를 별도 발부한다. 소유 산출물이 없다는 이유로 브리프가 미발부되면 그 역할의 관심사가 심의에 결착되지 않는 **공백**이 생기므로(T3 Guard·04 §3.4-C 병렬 권위 없음의 취지) 이 절이 그 공백을 규정으로 차단한다. 대상 목록은 `roleComposition` 활성 집합이며 소유/비소유 구분은 `artifactOwnership` 대조로 판별한다.
- **컨택스트 위생·주 세션 비작성 유지.** 비소유 참여 역할도 §7A.1의 컨택스트 위생을 따른다 — 주 세션은 조율·통합만 하고 심의 본문을 직접 작성하지 않으며, 각 역할은 fresh-context에서 Proposal/리뷰 의견을 산출해 완료 보고로만 반환한다.

### §7B.2 라운드 2+ 재제안 심의 (Reconciling 충돌 감지 → T5 · 동료 Proposal 동봉)

- **충돌 감지 = 주 세션 Reconciling 규약 절차.** 주 세션은 `Reconciling`(Conflict Detection + Trade-off Resolution)에서 Proposal 집합 간 충돌을 검출한다. 잔여 충돌 0 ∧ trade-off 결정 기록이면 T4(→`Reviewing`), **충돌 해소를 위해 추가 Proposal이 필요하면 T5**(→`Proposing`)로 **재제안 라운드(라운드 2+)**를 연다. 상태·전이·Guard는 04 §3.4-B 소유이며 본 절은 인용만 한다.
- **라운드 2+ 브리프에 동료 Proposal 동봉(블라인드 해소·fresh-context 유지).** 재제안 라운드의 브리프에는 **충돌 당사자 역할의 동료 Proposal(해당 라운드 산출)을 동봉**한다. 각 역할은 여전히 fresh-context 서브에이전트로 수행되므로 이전 라운드 컨텍스트를 갖지 않으나, **브리프에 동봉된 동료 Proposal을 입력으로 받아** 04 §3.4-C의 "전문가가 서로의 Proposal을 검토·반응"을 실현한다 — 즉 **fresh-context를 유지하면서 단일 라운드 블라인드를 브리프 동봉으로 해소**한다. 동봉 범위는 policy `deliberation.peerVisibility`가 정한다(값 = §7.2 (라)·소비 지점 = §7B.4).
- **재제안은 새 프레임워크가 아니다.** T5 라운드는 §7A.5 (3) 위임 절차를 **동료 Proposal 동봉만 추가해 반복**하는 것이다. 브리프 양식은 `solution-design-brief-template.md`의 라운드 2+ 동봉 필드를 사용한다.

### §7B.3 수렴·잔여 충돌 재노출 (Reviewing → T6 / 미해소 → T7)

- **Reviewing 수렴 → T6.** 잔여 충돌 0에 이르면 T4로 `Reviewing`(Integrated Design Review)에 진입하고, 해소된 결정을 **단일 일관 결정 집합**으로 수렴시키면 T6로 사용자 게이트(§5)에 넘긴다. 최종 결정 소유권은 개별 역할이 아니라 `Reviewing` 통합이며 확정 권위는 사용자 게이트다(04 §3.4-C·SP-INV 4 — 재정의 0).
- **미해소 충돌 발견 → T7 재노출.** `Reviewing` 중 미해소 충돌이 발견되면 T7로 **잔여 충돌을 `Reconciling`에 재노출**한다 — 다시 §7B.2의 재제안 심의로 이어질 수 있다. T5·T7의 왕복이 04 §3.4-C 다라운드 심의 경로의 물리 구동이며, 각 전이는 §4 로그에 `StateTransition`(T4·T5·T6·T7 라벨·`from`/`to` 04 정본 인용) 레코드로 남는다(새 레코드 종류 창설 0).
- **커버리지 역할의 라운드별 점검.** 전체 범위 커버리지 역할(`coverageFloor`)은 각 라운드에서 선언 범위 대비 커버리지 공백(빠진 기능·화면·프로세스 영역)을 지적한다 — 이는 CP2 결정적 체커의 침묵 누락 차단(SP-INV 9)과 층위가 다른, 심의 라운드 내 사람/역할 판단 층이다.

### §7B.4 policy `deliberation.*` 소비 지점 (포인터만 · 실값 정본 = §7.2 (라))

라운드 상한·수렴 기준·동료 가시성은 규약 절차에 하드코딩하지 않고 **policy `deliberation.*` 데이터**(Policy as Data·04 §3.2·§7.1)에서 온다. **본 절은 소비 지점만 명시하고 값을 두지 않는다** — 실값 정본 문면은 §7.2 (라)이며 `policy/default-policy.yaml` `deliberation` 블록과 한 벌이다(단일 소스 규율·§7.2 머리).

| policy 키 (포인터) | 소비 지점 (본 절) | 결정하는 것 |
|---|---|---|
| `deliberation.maxRounds` | §7B.5 종료 조건 | T5 재제안 라운드 상한 — 이 횟수에 도달하면 라운드를 더 열지 않고 종료 판정에 들어간다. |
| `deliberation.convergence` | §7B.5 종료 조건·§7B.3 수렴 | 수렴 기준 — "미해소 충돌 0"으로 T4/T6 수렴을 인정하는 판정 기준(04 §3.4-B Guard의 policy 측 파라미터). |
| `deliberation.peerVisibility` | §7B.2 동료 Proposal 동봉 | 동봉 가시성 범위 — 라운드 2+ 브리프에 어느 역할의 Proposal을 동봉하는지(충돌 당사자만 vs 전 활성 역할). |

**Policy as Data 불변.** 위 값 조정은 데이터 정정일 뿐 본 규약 절차·04 §3.4 상태/전이/Guard·SP-INV를 변경하지 않는다.

### §7B.5 종료 조건 (미해소 충돌 0 또는 라운드 상한 도달 — 상한 도달 시 Validating 표면화)

- **정상 종료 = 미해소 충돌 0.** `deliberation.convergence` 기준으로 **미해소 충돌 0**에 이르러 T4→(Reviewing)→T6로 `Validating`에 수렴하는 것이 정상 종료다(04 §3.4-B·C).
- **상한 도달 종료 = 잔여 충돌을 Validating 게이트에 표면화.** T5 라운드가 `deliberation.maxRounds` 상한에 도달했는데도 미해소 충돌이 남으면 **라운드를 더 열지 않고 종료하되 잔여 충돌을 은폐하지 않는다** — 잔여 충돌 목록을 `Validating` 사용자 게이트(§5)에 **표면화해 사용자 판단에 제시**한다. 사용자는 수용(T8)·수정 요청(T10)·강제 위임(T11) 중 하나로 응답한다(§5.2 — 재정의 0). 상한 도달로 인한 종료가 곧 자동 성숙이 아니며 승인 전 `Matured` 도달은 여전히 불가하다(SP-INV 4·불가침).
- **표면화 기록.** 상한 도달·잔여 충돌 표면화는 §4 로그에 남고(`StateTransition` + `GatePresented`의 잔여 충돌 페이로드 참조) 상세는 실행 메타 파일(코어 밖·SP-INV 2·3)에 둔다. 침묵 종료(잔여 충돌을 제시 없이 삼키는 것)는 금지된다 — silentOmission 금지의 심의 층 동형이다.

### §7B.6 심의 이탈·역할 cap 초과 제외의 Validating 게이트 일괄 표면화 (책임 있는 자율 (c))

- **일괄 표면화 접점.** 심의 중 발생한 기본값 이탈은 §7A.4 (ii)(iii)의 컨펌 시점 규약에 연결된다 — per-round 상시 질문이 아니라 **Validating에서 한 번에 제시·확인**받는다(루트 §6 원칙 11 (c)). 표면화 대상은 (i) 기본 역할 구성 이탈(`deviationRule`), (ii) 라운드 상한 도달 잔여 충돌(§7B.5), (iii) 아래 역할 cap 초과 제외다.
- **역할 cap 초과 제외(`excludedByCap`).** 활성 후보 역할이 `maxSpecialistRoles` cap을 초과해 심의 편입에서 제외되는 경우의 표기·판정은 **`excludedByCap`이 소유**하며 **본 절은 그것을 정의하지 않고 표면화 접점만 규정한다**(경계 침범·선취 금지). `excludedByCap` 제외 목록은 deliberation 이탈·잔여 충돌과 **함께 Validating 게이트에서 일괄 표면화·사용자 확인**된다 — cap으로 제외된 관심사가 조용히 사라지지 않도록(silentOmission 금지) 게이트에서 제시된다.
- **04 §3.4·SP-INV 재정의 0.** 위 표면화 규약은 04 §3.4 상태/전이·§3.4-C 최종 결정 소유권·SP-INV 4·8·9를 재정의하지 않고 물리 개입 시점(§5·§7A.4)에 연결할 뿐이다. 진위 판정 기준은 04 §3이다.

---

## §7C. Visual Contract — mock 생성·사용자 수렴 규약 (form-A 규약 — SD 종단·구현 진입 전)

기획 산출물(메뉴·화면·와이어프레임)이 확정된 뒤 **사용자가 구현 착수 전에 목표 이해를 시각적으로 확인**하고 피드백으로 수렴시키는 절차를 form-A 규약으로 확정한다. 이 절은 **04 §3.9 확장 포인트(UI/UX Visual Contract 협의 프로토콜)의 물리화**이며 04 §3.9·§3.4 `Validating`·SP-INV 4·9를 재정의하지 않는다(별도 파이프라인 요소 신설 0).

### §7C.1 배치 — SD 종단·Validating(사용자 게이트) 앞·구현 오케스트레이션 진입 전

- **위치.** mock 수렴은 성숙 산출(§7A)이 끝난 뒤, `Validating` 사용자 게이트(§5) 직전, 그리고 구현 오케스트레이션(`/uaf-implement` → `orchestration/adapters/claude/orchestrate_project.py`) **진입 전**에 놓인다. mock 수렴 종료가 곧 구현 진입 자격이며, 그 뒤 `design_completeness` 게이트(§7A.3 CP2)가 최후 방어로 재확인한다.
- **입력 소비 순서(불변).** 입력 = 확정 기획 산출물(`menu-structure`·`screen-list`·`screen-design`·와이어프레임)과 `design-tokens`다. **기획 산출물 확정 전 mock 생성 금지** — 정본이 확정되지 않은 상태의 mock은 drift의 근원이다.

### §7C.2 정본/파생 규율 — mock = 파생 뷰 (append-only 계보)

- **정본 = 설계 산출물 + 토큰, mock = 파생.** `screen-mock`(HTML)은 확정 와이어프레임·`design-tokens`를 소비해 생성한 **파생 뷰**다. 정본은 언제나 설계 산출물(`<workspace>/docs/*.md`)과 토큰이다.
- **피드백은 정본을 먼저 갱신.** 사용자 피드백은 **정본 설계 산출물을 먼저 갱신(append-only 계보·§4 기록)한 뒤 mock을 재생성**한다. **mock 파일을 직접 수정해 피드백을 소화하는 것은 금지**한다 — 설계↔mock drift 방지(§7A.2 "본문이 1차 정본" 동형).

### §7C.3 톤 수렴 프로토콜 — 대표 1화면 × 3안 → 토큰 확정 → 일괄 생성

- **최초 mock = 대표 1화면 × 톤 변형 3안.** 톤앤매너 수렴을 위해 대표 화면 1개를 톤 변형 3안으로 제시한다 → 사용자 선택·피드백 → `design-tokens` 확정.
- **잔여 화면 일괄 생성.** `design-tokens` 확정 후 잔여 화면을 **확정 토큰을 소비해 일괄 생성**한다. 이후 토큰 변경이 필요하면 **토큰 갱신 → 재생성**(§7C.2).

### §7C.3a mock 리뷰 차원 = `designPrinciples` 대조 (Visual Contract Wave 2)

- **같은 기준으로 점검.** mock 수렴 각 라운드에서 검증자·사용자 수렴 게이트는 Policy `designPrinciples` **전체**(§7.2 (사))를 **리뷰 차원**으로 삼아 mock을 대조한다 — 화면설계서에 기록된 원칙별 적용 근거(§7A.1)와 mock의 실제 표현을 원칙 단위로 점검한다(원칙 목록은 Policy가 소유하므로 여기서 열거하지 않는다).
- **접근성 실값 대조.** `accessibility` 원칙의 기계 판정 가능분은 `accessibility-floor.criteria`(§7.2 (바))를 기준으로 대조한다 — 단 이는 사람 판정 리뷰 차원이며 `design_completeness` 체커의 결정적 판정 대상이 아니다.
- **원칙 위반은 정본 갱신으로 소화.** 리뷰에서 발견된 위반은 §7C.2 규율대로 **정본 설계 산출물 갱신 → mock 재생성**으로 소화한다(mock 직접 수정 금지).

### §7C.4 수렴 종료 → `mock-convergence-record` → 오케스트레이션 진입

- **종료 조건.** 사용자 확정(잔여 피드백 0)에 이르면 `mock-convergence-record` 산출물을 산출한다 — **확인자·라운드 수·잔여 피드백 0**을 기록(§4 로그·매니페스트 `produced`). 이 산출물은 `defaultRequiredSet`(§7.2 (다)) touchpoint 클래스이며 접점 선언 프로젝트에서 required다.
- **진입.** 수렴 종료 후 구현 오케스트레이션에 진입하며, `design_completeness` 게이트가 Visual Contract 산출물 3종과 `designElements`(§7.2 (바)) 요소 완전성을 최후 방어로 재확인한다(기존 게이트·CP2).

### §7C.5 환경 표면 — 리포 HTML 직접 열람 또는 Artifact 발행(선택)

- **열람 = 리포 HTML 브라우저 직접 열람(도구 설치 0).** `screen-mock`은 리포 내 자기완결 HTML로 두고 브라우저에서 직접 연다. 필요 시 Artifact 발행(선택)으로 공유 가능하다.
- **외부 디자인 도구 사용 시.** 외부 도구를 쓰더라도 **정본은 리포 텍스트(설계 산출물+토큰)**이며 외부 링크는 앵커 인용만 남긴다(비강제 관행).

### §7C.6 04 §3.9 무수정·재정의 0 (포인터)

본 §7C는 04 §3.9 "UI/UX Visual Contract 협의 프로토콜"(명칭만·설계 0)의 물리 규약화이며 04 코어 문면을 촉하지 않는다(재정의 0). 협의 시점 = Solution Design 사용자 게이트(§3.4 `Validating`·구현 착수 전)라는 04 §3.9 문면과 정합하며 별도 파이프라인 요소를 신설하지 않는다(SP-INV 5·UAF-INV ⑥ 정합).

---

## §8. Provenance 성숙 run 내부 형식 확정

contract-binding §6은 `provenance` 컨테이너의 **외형·must-ignore 경계**만 확정하고 discovery-binding §10은 그 내부를 **Discovery run** 실행 메타로 확정했다. superseding **성숙 인스턴스**의 `provenance`는 성숙 run에서 유래하므로 본 절이 그 **성숙 run 내부 형식**을 확정한다(discovery-binding §10 동형·경계 침범 0).

### §8.1 성숙 run 내부 형식 (최소 표면)

| 내부 필드 (성숙 run 실행 메타) | 값 형태 | 참조 대상 |
|---|---|---|
| run 식별자 | 문자열 — 해당 성숙 run(State Machine 인스턴스, 04 §3.4-A)의 `<run-id>` | `solution-design-data/events/maturation-<run-id>/`(§3·§4) |
| 이벤트 로그 참조 | 참조 — 이 run의 append-only 기록 로그 디렉터리 경로/참조(§4) | DP-2 백엔드(§4) |
| 기준선 vN 참조 | 참조 — 성숙의 기준선이 된 Ready 인스턴스 vN(= `meta.supersedes`가 가리키는 인스턴스) | contract-binding §4.2·§5 `supersedes` |
| Policy 참조 | 참조 — 이 run이 사용한 Solution Design Policy 참조(§7) | `solution-design-data/policy/`(§7) |

위는 **최소 표면**이며 감사·재현에 필요한 추가 실행 메타(종단 상태·역할 구성 요약 참조 등)를 담을 수 있다. 어느 필드도 경량 **참조**이며 이벤트 로그·Proposal 원문을 컨테이너에 중복 저장하지 않는다(loop-binding §5.3 경량 참조 관례 동형).

### §8.2 contract-binding §6 외형·must-ignore 경계 유지 (재정의 0)

- **must-ignore 경계 불변.** UAHF tolerant reader는 `provenance`(및 하위 전체)를 **must-ignore**한다(contract-binding §6·03 §3.2-D·§3.3-C·PC-INV 3·5). 본 절이 내부 형식을 채워도 이 경계는 불변이며 내부 필드는 **성숙 활동 측 소비 전용**(감사·재현·계보 추적)이다.
- **누출 차단(SP-INV 2·3).** 성숙 run 실행 메타는 Contract **코어 필드**로 새어나가지 않는다 — 성숙 내부 개념(복잡도 판정·역할 구성·Proposal·충돌 기록)은 코어 밖 불투명 실행 메타이며(SP-INV 2·3·PC-INV 2·10) `provenance`와 실행 메타 파일에만 반영된다.
- **창설 금지.** 본 절은 03 §3.2-D 불투명 부속 계약·contract-binding §6 경계를 재정의하지 않고 그 **성숙 run 내부 형식만** 채운다. Contract 코어 스키마·버저닝·tolerant reader 계약을 변경하지 않는다.

---

## §10. 04 §4.2 이식 교체 지점 대응 (done 8)

04 "### 4.2 이식 교체 지점"의 각 지점에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다(정본 문면 = 04 §4.2 — 여기서 축자 인용하지 않고 § 포인터로 가리킨다). "유지되는 것" 열이 이식 축에서 04 §3 Core Contract 불변(structure.md §7 C-1 동형)을 재확인한다.

| 04 §4.2 교체 지점 (바뀌는 것) | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (04 §3 불변) |
|---|---|---|---|
| 실행 호스팅 → 대상 환경의 실행 메커니즘 | §6 | 주 세션(Advisor) Orchestrator 규약 절차·Expert Role 수행 = 기존 위임 실행 관행 재사용(역할 추상까지만). | §3.3 역할 추상·개방 네임스페이스·최소 할당(SP-INV 5·8), §3.4-C 최종 결정 소유권. |
| 게이트 채널 → 대상 환경의 개입 메커니즘 | §5 | 주 세션 사용자 제시·응답 수령 채널·T8~T11 게이트 전이 실의미·제시/응답 각 레코드. | §3.1 단계 계약(출력 2경로·사용자 게이트), §3.4 `Validating`·전이표, §3.8 SP-INV 4(UAF-INV ⑤). |
| 저장 위치 → 대상 환경의 저장 메커니즘 | §3, §4 | `solution-design-data/`(실행 메타·이벤트 로그·Policy)·`.claude/solution-design/`(일반 관례)·superseding 인스턴스는 contract-binding §4.2 경로 append(참조 인용). | §3.7 저장 스코프 원칙(워크스페이스 귀속·SP-INV 7), §3.4-C 단일 인스턴스 수렴(SP-INV 2·3), §3.5 Projection 관계. |
| Policy 실값 → 대상 환경의 정책 메커니즘 | §7 | `solution-design-data/policy/default-policy.yaml` 형식·최소 실값 1세트(§7.2). | §3.2 판정 형태(Policy as Data), §3.3 역할 추상, §3.5 Projection 동적 선택, §3.6 경계 기준. |

- **"유지되는 것" 열의 이식 불변성.** 위 계약은 다른 AI·실행 환경으로 이식해도 바뀌지 않는다 — 04 §4.2 "유지되는 것" 목록의 이식 불변성이며 structure.md §7 C-1과 정합한다.
- 본 문서는 04 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고 v1.4 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §11. 상시 불변 자기 점검 (요지 — 판정 기준은 04 §3.8)

자체 점검은 최종 승인이 아니다 — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다. 본 문서에서 "02"는 달리 명시하지 않는 한 `discovery/specs/02-discovery.md`를 가리키며 Agent 역할 경계는 `uahf/specs/02-agent.md`다.

- **재정의 0·창설 0.** 모든 매핑은 04 §3·§4의 물리 실현이며 어떤 상태·전이(T1~T11)·SP-INV·단계 계약·판정 형태·역할 추상·Projection 관계·경계 기준도 이 문서에서 진위가 새로 확정되지 않는다(판정 기준 = 04 §3). §4 레코드 종류 명칭은 **직렬화 기록 관례**이고 §7 Policy 값·§8 Provenance 내부 필드는 데이터·부속 형식일 뿐 코어 계약 요소가 아니다.
- **Discovery Event 15종 명칭 차용 0.** §4의 6종은 02 §3.5 Event 15종 어느 명칭과도 일치하지 않는다 — 게이트는 `ValidationRequested`가 아니라 `GatePresented`/`UserResponded`, 강제는 `UserOverride`가 아니라 T11 `StateTransition`으로 명명해 재사용을 회피했다(mention/use 경계).
- **방법론·카탈로그·타 벤더·모델명 0(UAF-INV ⑥).** `uaf-verified:` 검색 범위 = 본 문서 본문 문면 — 특정 설계 방법론 고유명·타 AI 벤더·모델명은 등장하지 않는다. §7.2 (나)·§7A가 인용하는 Policy 기본 역할 구성·소유 맵의 **일반 역할명**은 (다)의 Projection id 열거와 **동형의 격리 지점 등재**다 — **SP-INV 5는 코어(04)만 구속**하며 Adapter Policy가 기본값 데이터로 일반 역할명을 두는 것은 위반이 아니다(04 코어 문면은 여전히 역할명 0·§6.2 무촉). 직렬화 형식·물리 경로·"주 세션"·"Advisor"·"서브에이전트 위임"은 이 Adapter 환경 자체의 토큰이므로 배제 대상이 아니다(C-3 비적용).
- **SP-INV 정합.** SP-INV 1(§4 `MaturationRunStarted` 입력 결속)·2·3(§3.2·§8.2)·4(§5.2)·5(위 항목)·6(§6.2)·7(§3.1·§3.3·§7A.2)·8(§6.1·§7.2 (나))·9(§7.2 (나)·(다)·(바))를 물리 실현으로 훼손하지 않는다. 진위 판정 기준은 04 §3.8이다.

---

## §12. 상태 서술 실측 대조 (L-07 — 미존재를 실재로 쓰지 않음)

"실재/미존재" 서술은 파일 시스템 직접 실측 후에만 기입한다(L-07). 현행 물리 위치: 본 문서는 `planning/adapters/claude/`에, 본 문서가 선언·소유하는 백엔드 데이터 트리는 `uahf/framework/adapters/claude/…` 아래에 있다(최종 확정 = 2차 산출물 디커플링 트랙).

- **실재.** 본 문서 · 자매 바인딩(contract·discovery·entry·memory·loop) · 정본 04·03 · Ground Truth `discovery-data/contracts/uahf/project-contract.v1.md`(성숙 입력 기준선)와 성숙 산출 `project-contract.v2.md`(v1 문면 byte 불변·PC-INV 9) · `solution-design-data/` 루트와 `policy/default-policy.yaml`·`events/` 표면 · form-B 로더 `planning/adapters/claude/solution_design_resolve.py`와 그 테스트 · 브리프 양식 `solution-design-brief-template.md`.
- **아카이브.** run 인스턴스(`solution-design-data/events/maturation-r001…r003/`)는 산출물 수명 정책(`docs/artifact-lifecycle-policy.md`)에 따라 앵커 보존으로 전환됐다(git 앵커 `@cd9247b`·ARCHIVE.md 원장).
- **미존재(정상).** 소비 프로젝트 `.claude/solution-design/`(일반 관례는 소비 프로젝트 배치 대상). **미도입.** 성숙 실행 규약 절차 기록기·실행 호스팅(역할 자동 소환·본문 자동 생성) — 04 §3.9 확장 포인트로 미설계(§6.2·§7A.5).
- **핵심 구분.** 본 문서가 확정한 백엔드 트리·기록 어휘·게이트 채널·Policy 값·Provenance 내부 형식은 **정본 문면(형태 A)**이며, 물리 데이터 자산은 성숙 run E2E로 생성됐다. 본 문서는 구조·형식·경로·값의 정본 문면을 소유하고 물리 위치의 최종 확정은 2차 산출물 디커플링 트랙 소관이다(L-07).

---

## §13. 정본 경계·소유 (self-note) · open_questions

- **소유·확정하는 것.** 04 §4.1이 "Adapter 소관"으로 미룬 지점 — ① Expert Role 실행 호스팅 **역할 추상**(§6) ② 사용자 게이트 제시·응답 채널(§5) ③ `solution-design-data/` 백엔드 트리·기록 직렬화(§3·§4) ④ Policy 값 데이터 소스·직렬화 + 최소 실값(§7) — 과 저장의 부속으로 ⑤ Provenance 성숙 run 내부 형식(§8). Expert Role 물리 호스팅은 **설계하지 않는다**(04 §3.9). superseding 인스턴스 저장·버전 표기·Provenance 외형·must-ignore 경계는 contract-binding §3·§4·§5·§6 소유이며 참조 인용만 한다(재정의 0). 격리 토큰(직렬화 형식·물리 경로·Policy 값)의 단일 자리가 이 문서다(structure.md §5 C-3 비적용).
- **OQ-SD-1 (Policy 최소 실값 — 비차단).** §7.2 최소 실값 1세트는 E2E 구동을 위한 본 문서의 Adapter 재량 확정이며(DP-5 위임·DP-X5 동형), Policy as Data이므로 값 조정은 데이터 정정일 뿐 정본 계약(04 §3.2·§3.3·§3.5) 변경이 아니다. 다른 상한·판정 신호가 필요하면 Advisor 재확정 또는 `policy/` 데이터 정정으로 조정 가능하다 — 계약 변경이 아니므로 비차단이다.
- **OQ-SD-2 (백엔드 데이터 트리 물리 위치 — 비차단·2차 트랙).** 본 문서는 planning 레이어 어댑터 경계로 이동했으나 본 문서가 선언·소유하는 백엔드 데이터 트리(`solution-design-data/`·성숙 산출 `discovery-data/contracts/uahf/`)는 1차 이동 범위 밖으로 현행 `uahf/framework/adapters/claude/…` 아래에 잔류한다. 최종 물리 위치 확정은 2차 산출물 디커플링 트랙 소관이며 계약 내용 변경이 아니므로 비차단이다.
