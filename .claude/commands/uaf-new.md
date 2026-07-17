---
description: UAF 공식 진입점 /new(순수 Greenfield 전용)의 물리 발화 형태 — Entry Resolution 규약 절차(엔진 5단계·결정 테이블)와 사용자 개입 지점을 정본 포인터로 안내한다.
---

# /new — UAF Greenfield 진입 (물리 발화: uaf-new 명령)

작성일: 2026-07-07
상태: v1.2 Baseline (CP2 첫 판정 Pass 16/0/0 · CP3 승인 · 사용자 승인 2026-07-07) · 2026-07-18 관측 수단 개정(사용자 폴더 주입) — CP2 통과·CP3 승인(OQ-2 = (a) spec 무변경) · 2026-07-18 형태 B 로더 도입(entry_resolve.py) — CP2 통과(결함 정정: 행 7 거짓게이트·게이트=policy 단일 소스)·CP3 승인
상위 규약: .claude/AGENT.md
성격: UAF 진입 명령 — 형태 A 문서 명령(이 파일 자체 실행 코드 0, D-v1.2-1) + 형태 B 로더 호출(entry_resolve.py·2026-07-18 도입·형태 A 폴백 공존)

---

## §0. 이 명령의 위치와 성격

- 이 파일은 `.claude/commands/` 아래의 **UAF 진입 표면**이다 — 논리 Entry `/new`(entry/specs/01-entry.md §3.1 등재; §0 "논리 식별자 주의")의 **물리 발화 형태**다. `/new`는 논리 식별자(name)이고, 그 물리 진입 형태를 어떤 명령으로 발화하는가는 Adapter 소관이다(01 §0·§4.1). 이 환경의 물리 발화 형태 = 이 `uaf-new` 명령으로 확정되어 있다(entry/adapters/claude/entry-binding.md §3). `uaf-` 접두는 UAF 네임스페이스를 표면에 드러내고 환경 빌트인 명령과의 충돌을 피하기 위한 것이다.
- `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰의 사용이 허용된다(uahf/framework/core/structure.md §2 Adapter 경계, uahf-status.md §0 선례 동형).
- **형태 A(문서 명령) — 이 명령 파일 자체는 실행 코드 0.** 이 명령 파일은 실행 스크립트를 포함하지 않는 문서 명령이다(D-v1.2-1). 다만 Entry Resolution 엔진(고정 5단계, 01 §3.2-A)의 실현은 이제 두 경로가 **공존**한다 — (i) **형태 B 로더**(권장): 결정적 실행 스크립트 `entry/adapters/claude/entry_resolve.py`를 호출해 해소 결과(JSON)를 수령한다(2026-07-18 도입, entry-binding §4.4·§5.2 — 엔트리 LLM 턴·메인 컨택스트 부하 제거). (ii) **형태 A 폴백**: 로더 미가용 시 주 세션이 규약 절차를 실수행한다. 어느 경로든 01 §3 계약·결정 테이블은 동일하다(structure.md §7 C-1). (`형태 A/B`는 structure.md §4 서술 라벨이다.)
- **정본 재정의 0.** 이 문서는 어떤 계약·판별 규칙도 스스로 확정하지 않는다. 아래 절차·결정 행·게이트는 전부 **정본 포인터**(01-entry·entry-binding)로만 안내하며 값을 하드코딩하지 않으므로, 정본이 진행돼도 이 명령은 낡지 않는다.

---

## §1. 목적

`/new` 호출 시 **순수 Greenfield 진입**의 Entry Resolution을 규약 절차로 수행하도록 안내한다 — 빈 워크스페이스에서 새 프로젝트를 시작하는 Discovery를 요청한다(기본 Discovery mode = `greenfield`, 01 §3.1). 출력은 **Discovery Request 하나까지**다 — Entry는 Discovery를 수행하지 않고 Project Contract를 생성하지 않는다(01 EN-INV 1·2).

---

## §2. 진입 절차 (Entry Resolution 규약 절차 — 정본 포인터)

호출되면 Entry Resolution 엔진 **고정 5단계**(01 §3.2-A)로 해소한다 — 아래 [형태 B 로더 호출]이 권장 경로이고 [규약 절차]가 폴백으로 공존한다. 각 단계·판별·게이트는 정본에서 회수한다(값 하드코딩 없음).

### 형태 B 로더 호출 (권장 경로 — 2026-07-18 도입)

주 세션은 결정적 실행 로더를 호출해 해소 결과(JSON)를 수령한다:

```
python entry/adapters/claude/entry_resolve.py --entry new --folder <대상 폴더> [--intent new]
```

- `--entry`는 슬래시 없는 `new`가 1차 형태다(주 세션 Bash 도구 호출 시 `/new`가 MSYS 경로로 변환되는 문제 회피·OQ-7 정정). `/new`도 허용·정규화된다.
- 사용자가 진입 시 **대상 폴더 + 신규/기존 의도**를 주입한다(entry-binding §4.0). `--intent` 미지정 시 `/new`는 `new`가 기본이다(entry-registry `defaultIntent`). `--intent`는 provenance 에코이며 게이트를 구동하지 않는다.
- 로더는 파일시스템을 **순수 판독**(contract-presence·repository-presence 유/무만·EN-INV 2 — 내용 파싱 0·폴더 생성 0·EN-INV 1)해 결정 테이블(01 §3.2-D)을 결정적으로 대조하고, 단일 Discovery Request `{mode, inputs, policy}` + 엔진 메타(`matchedRow`·`gate`)를 JSON 으로 방출한다(entry-binding §4.4·§5).
- **게이트는 canonical 결정 테이블 policy로만 구동한다.** 매칭 행의 **`policy.ref == user-confirmation-gate`**(canonical 행 2·3·4·5·방출 `gate: true`)이면 주 세션이 **사용자 확인 게이트를 제시**한다(아래 사용자 개입 지점·01 EN-INV 6). 게이트 이유는 `policy.conflict`(repository-present/contract-present/nothing-to-continue)에 있다. 로더는 canonical policy를 표면화만 하고 확정 결정을 내리지 않으며, **병행 conflict 신호를 두지 않는다**(Policy as Data 단일 소스).
- **형태 A 폴백.** 로더가 가용하지 않으면 주 세션이 아래 규약 절차(고정 5단계)를 직접 실수행한다 — 두 경로의 판별 결과는 동일하다(structure.md §7 C-1).

### 규약 절차 (고정 5단계 — 로더가 실현·폴백이 실수행)

1. **매칭.** 명시 Entry = `/new`의 Entry Descriptor를 Entry Registry에서 찾는다 (01 §3.2-A).
2. **증거 수집(관측).** 관측의 출발점은 **사용자 주입**이다 — 진입 시 사용자가 **대상 폴더(경로/폴더명)와 신규/기존 의도**를 주입하며, 이것이 `/new` Descriptor의 requiredEvidence(contract-presence·repository-presence) 관측의 위치·방식을 확정한다. 물리 판정 수단(탐지 절차)은 **entry-binding.md §4**에 있다(재정의 0) — **신규 폴더명 주입** 시 repository-presence = 무로 확정하고 그 폴더가 부재/빈 상태인지 확인하며 contract-presence도 그 폴더 기준 무; **기존 폴더 주입** 시 그 폴더로 스코프해 Contract 저장 위치(`<주입 폴더>/.claude/project-contract/` 등, contract-binding.md §4)의 인스턴스 파일(`project-contract.v<N>.md`) 유무를 스캔한다. 주입한 신규/기존 선언과 실제 폴더 상태가 상충하면 임의로 덮어쓰지 않고 사용자 확인 게이트로 안내한다(EN-INV 6, entry-binding.md §4 충돌 처리 note). **Entry는 유/무만 관측하며 Contract 내용을 해석하지 않는다**(01 EN-INV 2; §3.2-A 2단계 "관측만").
3. **우선순위 평가.** `/new`의 결정 행(01 §3.2-D 결정 테이블 행 1~4)을 관측 증거에 대조해 매칭되는 단일 결과 행을 선택한다.
4. **결정성 검증.** 관측 조합이 단일 행에만 매칭됨을 확인한다 (01 §3.2-A 4단계·EN-INV 3).
5. **방출.** 선택 결과를 단일 Discovery Request {mode, inputs, policy}로 방출한다(직렬화·전달 = entry-binding.md §5). **Entry는 여기서 멈춘다** — Discovery 수행·Contract 생성은 하지 않는다 (01 EN-INV 1·2).

### 사용자 개입 지점 (Preserve Human Authority, 01 EN-INV 6)

- `/new`는 **순수 Greenfield 전용**이므로, 관측 증거에 기존 Contract 또는 Repository가 나타나면 사용자 의도와 증거가 상충한다(01 §3.2-D 행 2·3·4). 이때 Entry는 **스스로 재라우팅·덮어쓰기를 결정하지 않고** policy에 **사용자 확인 게이트**를 표기한다(01 §3.2-D 판별 규칙 D3 ①·충돌 처리·EN-INV 6). 사용자가 `/continue`를 재발화하면 결정 테이블이 결정적으로 재해소된다(01 §8 예2).
- **주입 선언 ↔ 실제 폴더 상태 상충은 별도 게이트가 아니라 canonical 결정 테이블 policy에 포섭된다.** 주입한 "신규" 의도와 달리 그 폴더에 실질 콘텐츠가 존재하면 관측이 **행 2·4**로 해소되고 그 행의 canonical policy가 이미 사용자 확인 게이트다(repository-present/contract-present). 즉 하이브리드 선언↔상태 충돌은 결정 테이블 policy(행 2·3·4·5)로 구동되며 **별도 conflict 신호가 아니다**(entry-binding.md §4.2 충돌 처리 note 정합·Policy as Data 단일 소스). Entry는 관측값을 임의로 덮어쓰지 않는다(EN-INV 6). 물리 판정·게이트 표기 수단은 entry-binding.md §4 소관이다(재정의 0).
- 확정 게이트(사용자 승인)는 하류에서 존중된다 — Entry는 게이트를 데이터로 표기할 뿐 확정 결정을 내리지 않는다(01 EN-INV 6, ARCHITECTURE.md §8 UAF-INV ⑤).

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선하며, 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행).

| 안내 항목 | 정본 (가리키기만 함) |
|---|---|
| Entry `/new` 논리 정의·기본 mode(`greenfield`) | `entry/specs/01-entry.md` §3.1 |
| Entry Descriptor 등록 모델·Resolution 엔진 고정 5단계 | `entry/specs/01-entry.md` §3.2-A |
| 결정 테이블(행 1~4)·판별 규칙 D3 ①·충돌 처리 | `entry/specs/01-entry.md` §3.2-D |
| mode 네임스페이스(확장 가능) | `entry/specs/01-entry.md` §3.2-E |
| Evidence 관측 물리 판정 수단(탐지 절차) | `entry/adapters/claude/entry-binding.md` §4·§4.4 |
| 형태 B 결정적 실행 로더(권장 경로) | `entry/adapters/claude/entry_resolve.py` (엔진 5단계·LLM 0·순수 판독) |
| 결정 테이블 데이터(8조합·Evidence·게이트 policy·관측 규칙) | `entry/adapters/claude/entry-registry.json` (Policy as Data 단일 소스·정본 = 01 §3.2-D·재정의 0) |
| Contract 저장 위치·직렬화 | `planning/adapters/claude/contract-binding.md` §3·§4 |
| Discovery Request 직렬화·전달 | `entry/adapters/claude/entry-binding.md` §5 (기록 백엔드 트리 = `discovery-binding.md` 예정) |
| Eliciting 인터뷰 행동 규약 (하류 Discovery 진행 시) | `discovery/adapters/claude/discovery-binding.md` §7.1 |
| Entry 불변(EN-INV 1~6) | `entry/specs/01-entry.md` §3.3 |
| 논리 식별자 주의(물리 발화 형태 = Adapter 소관) | `entry/specs/01-entry.md` §0·§4.1 · `entry/adapters/claude/entry-binding.md` §3 |
| Discovery Request 상위 추상 {mode, inputs, policy} | `ARCHITECTURE.md` §12.2 |
| 진입 명령 골격 관례 | `.claude/commands/uahf-status.md` |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다.
