---
description: UAF 공식 진입점 /continue(기존 프로젝트 이어가기 — Incremental/Brownfield)의 물리 발화 형태 — Entry Resolution 규약 절차(엔진 5단계·결정 테이블)와 사용자 개입 지점을 정본 포인터로 안내한다.
---

# /continue — UAF 이어가기 진입 (물리 발화: uaf-continue 명령)

작성일: 2026-07-07
상태: v1.2 Baseline (CP2 첫 판정 Pass 16/0/0 · CP3 승인 · 사용자 승인 2026-07-07) · 2026-07-18 관측 수단 개정(사용자 폴더 주입) — CP2 통과·CP3 승인(OQ-2 = (a) spec 무변경)
상위 규약: .claude/AGENT.md
성격: UAF 진입 명령 — 형태 A(문서 명령), 실행 코드 0 (D-v1.2-1)

---

## §0. 이 명령의 위치와 성격

- 이 파일은 `.claude/commands/` 아래의 **UAF 진입 표면**이다 — 논리 Entry `/continue`(entry/specs/01-entry.md §3.1 등재; §0 "논리 식별자 주의")의 **물리 발화 형태**다. `/continue`는 논리 식별자(name)이고, 그 물리 진입 형태를 어떤 명령으로 발화하는가는 Adapter 소관이다(01 §0·§4.1). 이 환경의 물리 발화 형태 = 이 `uaf-continue` 명령으로 확정되어 있다(entry/adapters/claude/entry-binding.md §3). `uaf-` 접두는 UAF 네임스페이스를 표면에 드러내고 환경 빌트인 명령과의 충돌을 피하기 위한 것이다.
- `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰의 사용이 허용된다(uahf/framework/core/structure.md §2 Adapter 경계, uahf-status.md §0 선례 동형).
- **형태 A(문서 명령) — 실행 코드 0.** 이 명령은 실행 스크립트를 포함하지 않는다(D-v1.2-1). Entry Resolution 엔진(고정 5단계, 01 §3.2-A)은 규약 절차로 실현되며, 호출 시 **주 세션이 그 절차를 실수행**한다. (`형태 A/B`는 structure.md §4 서술 라벨이다.)
- **정본 재정의 0.** 이 문서는 어떤 계약·판별 규칙도 스스로 확정하지 않는다. 아래 절차·결정 행·게이트는 전부 **정본 포인터**(01-entry·entry-binding)로만 안내하며 값을 하드코딩하지 않으므로, 정본이 진행돼도 이 명령은 낡지 않는다.

---

## §1. 목적

`/continue` 호출 시 **기존 프로젝트를 이어가는 진입**의 Entry Resolution을 규약 절차로 수행하도록 안내한다 — 증거에 따라 **Incremental Discovery**(Project Contract 존재 시) 또는 **Brownfield Full Discovery**(Contract 부재·Repository 존재 시, 최초 Contract 생성)를 요청한다(01 §3.1). 출력은 **Discovery Request 하나까지**다 — Entry는 Discovery를 수행하지 않고 Project Contract를 생성하지 않는다(01 EN-INV 1·2).

---

## §2. 진입 절차 (Entry Resolution 규약 절차 — 정본 포인터)

호출되면 Entry Resolution 엔진 **고정 5단계**(01 §3.2-A)를 규약 절차로 수행한다. 각 단계·판별·게이트는 정본에서 회수한다(값 하드코딩 없음).

1. **매칭.** 명시 Entry = `/continue`의 Entry Descriptor를 Entry Registry에서 찾는다 (01 §3.2-A).
2. **증거 수집(관측).** 관측의 출발점은 **사용자 주입**이다 — 진입 시 사용자가 **대상 폴더(경로/폴더명)와 신규/기존 의도**를 주입하며, 이것이 `/continue` Descriptor의 requiredEvidence(contract-presence·repository-presence) 관측의 위치·방식을 확정한다. 물리 판정 수단(탐지 절차)은 **entry-binding.md §4**에 있다(재정의 0) — **기존 폴더 주입** 시 repository-presence = 유로 확정하고 그 폴더로 스코프해 Contract 저장 위치(`<주입 폴더>/.claude/project-contract/` 등, contract-binding.md §4)의 인스턴스 파일(`project-contract.v<N>.md`) 유무를 스캔한다(존재→incremental, 부재→brownfield); **신규 폴더명 주입** 시 repository-presence = 무로 확정하고 폴더 부재/빈 상태를 확인한다. 주입한 신규/기존 선언과 실제 폴더 상태가 상충하면 임의로 덮어쓰지 않고 사용자 확인 게이트로 안내한다(EN-INV 6, entry-binding.md §4 충돌 처리 note). **Entry는 유/무만 관측하며 Contract 내용을 해석하지 않는다**(01 EN-INV 2; §3.2-A 2단계 "관측만").
3. **우선순위 평가.** `/continue`의 결정 행(01 §3.2-D 결정 테이블 행 5~8)을 관측 증거에 대조해 매칭되는 단일 결과 행을 선택한다. Contract 존재가 우선한다 — 존재 시 `incremental`(행 7·8), 부재·Repository 존재 시 `brownfield`(행 6).
4. **결정성 검증.** 관측 조합이 단일 행에만 매칭됨을 확인한다 (01 §3.2-A 4단계·EN-INV 3).
5. **방출.** 선택 결과를 단일 Discovery Request {mode, inputs, policy}로 방출한다(직렬화·전달 = entry-binding.md §5). **Entry는 여기서 멈춘다** — Discovery 수행·Contract 생성은 하지 않는다 (01 EN-INV 1·2).

### 판별 요지 (정본 포인터)

- **Contract 존재 → Incremental** (01 §3.2-D 판별 규칙 D3 ③, 행 7·8). Repository 유무와 무관하게 Contract 존재가 우선한다.
- **Contract 부재 + Repository 존재 → Brownfield Full Discovery, 최초 Contract 생성** (01 §3.2-D 판별 규칙 D3 ②, 행 6).

### 사용자 개입 지점 (Preserve Human Authority, 01 EN-INV 6)

- 이어갈 증거가 부재(Contract 무 + Repository 무, 01 §3.2-D 행 5 — P-D)하면 사용자 의도와 증거가 상충한다. 이때 Entry는 **스스로 확정하지 않고** policy에 **사용자 확인 게이트**를 표기한다(01 §3.2-D 충돌 처리·EN-INV 6). 확정 게이트(사용자 승인)는 하류에서 존중된다(ARCHITECTURE.md §8 UAF-INV ⑤).
- **주입한 "기존" 의도 ↔ 실제 폴더 상태 상충도 게이트 대상이다.** 주입한 기존 의도와 달리 그 폴더가 부재·빈 상태(이어갈 콘텐츠 없음)이면, Entry는 관측값을 임의로 덮어쓰지 않고 policy에 사용자 확인 게이트를 표기한다(01 EN-INV 6, entry-binding.md §4 충돌 처리 note). 물리 판정·게이트 표기 수단은 entry-binding.md §4 소관이다(재정의 0).

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선하며, 발견되는 충돌은 Advisor에게 보고한다(상위 규약 관행).

| 안내 항목 | 정본 (가리키기만 함) |
|---|---|
| Entry `/continue` 논리 정의·mode(`incremental`/`brownfield`) | `entry/specs/01-entry.md` §3.1 |
| Entry Descriptor 등록 모델·Resolution 엔진 고정 5단계 | `entry/specs/01-entry.md` §3.2-A |
| 결정 테이블(행 5~8)·판별 규칙 D3 ②·D3 ③·충돌 처리 | `entry/specs/01-entry.md` §3.2-D |
| mode 네임스페이스(확장 가능) | `entry/specs/01-entry.md` §3.2-E |
| Evidence 관측 물리 판정 수단(탐지 절차) | `entry/adapters/claude/entry-binding.md` §4 |
| Contract 저장 위치·직렬화 | `planning/adapters/claude/contract-binding.md` §3·§4 |
| Discovery Request 직렬화·전달 | `entry/adapters/claude/entry-binding.md` §5 (기록 백엔드 트리 = `discovery-binding.md` 예정) |
| Eliciting 인터뷰 행동 규약 (하류 Discovery 진행 시) | `discovery/adapters/claude/discovery-binding.md` §7.1 |
| Entry 불변(EN-INV 1~6) | `entry/specs/01-entry.md` §3.3 |
| 논리 식별자 주의(물리 발화 형태 = Adapter 소관) | `entry/specs/01-entry.md` §0·§4.1 · `entry/adapters/claude/entry-binding.md` §3 |
| Discovery Request 상위 추상 {mode, inputs, policy} | `ARCHITECTURE.md` §12.2 |
| 진입 명령 골격 관례 | `.claude/commands/uahf-status.md` |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다.
