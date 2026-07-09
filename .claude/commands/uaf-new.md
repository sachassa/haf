---
description: UAF 공식 진입점 /new(순수 Greenfield 전용)의 물리 발화 형태 — Entry Resolution 규약 절차(엔진 5단계·결정 테이블)와 사용자 개입 지점을 정본 포인터로 안내한다.
---

# /new — UAF Greenfield 진입 (물리 발화: uaf-new 명령)

작성일: 2026-07-07
상태: v1.2 Baseline (CP2 첫 판정 Pass 16/0/0 · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: .claude/AGENT.md
성격: UAF 진입 명령 — 형태 A(문서 명령), 실행 코드 0 (D-v1.2-1)

---

## §0. 이 명령의 위치와 성격

- 이 파일은 `.claude/commands/` 아래의 **UAF 진입 표면**이다 — 논리 Entry `/new`(entry/specs/01-entry.md §3.1 등재; §0 "논리 식별자 주의")의 **물리 발화 형태**다. `/new`는 논리 식별자(name)이고, 그 물리 진입 형태를 어떤 명령으로 발화하는가는 Adapter 소관이다(01 §0·§4.1). 이 환경의 물리 발화 형태 = 이 `uaf-new` 명령으로 확정되어 있다(runtime/uahf/framework/adapters/claude/entry-binding.md §3). `uaf-` 접두는 UAF 네임스페이스를 표면에 드러내고 환경 빌트인 명령과의 충돌을 피하기 위한 것이다.
- `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰의 사용이 허용된다(runtime/uahf/framework/core/structure.md §2 Adapter 경계, uahf-status.md §0 선례 동형).
- **형태 A(문서 명령) — 실행 코드 0.** 이 명령은 실행 스크립트를 포함하지 않는다(D-v1.2-1). Entry Resolution 엔진(고정 5단계, 01 §3.2-A)은 규약 절차로 실현되며, 호출 시 **주 세션이 그 절차를 실수행**한다. (`형태 A/B`는 structure.md §4 서술 라벨이다.)
- **정본 재정의 0.** 이 문서는 어떤 계약·판별 규칙도 스스로 확정하지 않는다. 아래 절차·결정 행·게이트는 전부 **정본 포인터**(01-entry·entry-binding)로만 안내하며 값을 하드코딩하지 않으므로, 정본이 진행돼도 이 명령은 낡지 않는다.

---

## §1. 목적

`/new` 호출 시 **순수 Greenfield 진입**의 Entry Resolution을 규약 절차로 수행하도록 안내한다 — 빈 워크스페이스에서 새 프로젝트를 시작하는 Discovery를 요청한다(기본 Discovery mode = `greenfield`, 01 §3.1). 출력은 **Discovery Request 하나까지**다 — Entry는 Discovery를 수행하지 않고 Project Contract를 생성하지 않는다(01 EN-INV 1·2).

---

## §2. 진입 절차 (Entry Resolution 규약 절차 — 정본 포인터)

호출되면 Entry Resolution 엔진 **고정 5단계**(01 §3.2-A)를 규약 절차로 수행한다. 각 단계·판별·게이트는 정본에서 회수한다(값 하드코딩 없음).

1. **매칭.** 명시 Entry = `/new`의 Entry Descriptor를 Entry Registry에서 찾는다 (01 §3.2-A).
2. **증거 수집(관측).** `/new` Descriptor의 requiredEvidence(contract-presence·repository-presence)를 관측한다. 물리 판정 수단(탐지 절차)은 **entry-binding.md §4**에 있다 — contract-presence = 저장 위치(`.claude/project-contract/` 등, contract-binding.md §4)의 인스턴스 파일(`project-contract.v<N>.md`) 유무; repository-presence = 워크스페이스 내 기존 프로젝트 콘텐츠 유무. **Entry는 유/무만 관측하며 Contract 내용을 해석하지 않는다**(01 EN-INV 2; §3.2-A 2단계 "관측만").
3. **우선순위 평가.** `/new`의 결정 행(01 §3.2-D 결정 테이블 행 1~4)을 관측 증거에 대조해 매칭되는 단일 결과 행을 선택한다.
4. **결정성 검증.** 관측 조합이 단일 행에만 매칭됨을 확인한다 (01 §3.2-A 4단계·EN-INV 3).
5. **방출.** 선택 결과를 단일 Discovery Request {mode, inputs, policy}로 방출한다(직렬화·전달 = entry-binding.md §5). **Entry는 여기서 멈춘다** — Discovery 수행·Contract 생성은 하지 않는다 (01 EN-INV 1·2).

### 사용자 개입 지점 (Preserve Human Authority, 01 EN-INV 6)

- `/new`는 **순수 Greenfield 전용**이므로, 관측 증거에 기존 Contract 또는 Repository가 나타나면 사용자 의도와 증거가 상충한다(01 §3.2-D 행 2·3·4). 이때 Entry는 **스스로 재라우팅·덮어쓰기를 결정하지 않고** policy에 **사용자 확인 게이트**를 표기한다(01 §3.2-D 판별 규칙 D3 ①·충돌 처리·EN-INV 6). 사용자가 `/continue`를 재발화하면 결정 테이블이 결정적으로 재해소된다(01 §8 예2).
- 확정 게이트(사용자 승인)는 하류에서 존중된다 — Entry는 게이트를 데이터로 표기할 뿐 확정 결정을 내리지 않는다(01 EN-INV 6, ARCHITECTURE.md §5 UAF-INV ⑤).

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선하며, 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행).

| 안내 항목 | 정본 (가리키기만 함) |
|---|---|
| Entry `/new` 논리 정의·기본 mode(`greenfield`) | `entry/specs/01-entry.md` §3.1 |
| Entry Descriptor 등록 모델·Resolution 엔진 고정 5단계 | `entry/specs/01-entry.md` §3.2-A |
| 결정 테이블(행 1~4)·판별 규칙 D3 ①·충돌 처리 | `entry/specs/01-entry.md` §3.2-D |
| mode 네임스페이스(확장 가능) | `entry/specs/01-entry.md` §3.2-E |
| Evidence 관측 물리 판정 수단(탐지 절차) | `runtime/uahf/framework/adapters/claude/entry-binding.md` §4 |
| Contract 저장 위치·직렬화 | `runtime/uahf/framework/adapters/claude/contract-binding.md` §3·§4 |
| Discovery Request 직렬화·전달 | `runtime/uahf/framework/adapters/claude/entry-binding.md` §5 (기록 백엔드 트리 = `discovery-binding.md` 예정) |
| Entry 불변(EN-INV 1~6) | `entry/specs/01-entry.md` §3.3 |
| 논리 식별자 주의(물리 발화 형태 = Adapter 소관) | `entry/specs/01-entry.md` §0·§4.1 · `runtime/uahf/framework/adapters/claude/entry-binding.md` §3 |
| Discovery Request 상위 추상 {mode, inputs, policy} | `ARCHITECTURE.md` §8.2 |
| 진입 명령 골격 관례 | `.claude/commands/uahf-status.md` |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다.
