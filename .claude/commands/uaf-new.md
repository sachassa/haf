---
description: UAF 공식 진입점 /new(순수 Greenfield 전용)의 물리 발화 형태 — Entry Resolution 규약 절차(엔진 5단계·결정 테이블)와 사용자 개입 지점을 정본 포인터로 안내한다.
---

# /new — UAF Greenfield 진입 (물리 발화: uaf-new 명령)

상태: v1.2 Baseline + 형태 B 로더(entry_resolve.py)
상위 규약: .claude/AGENT.md

---

## §0. 이 명령의 위치와 성격

- **물리 발화 형태** — 논리 Entry `/new`(entry/specs/01-entry.md §3.1 등재)의 물리 진입 형태다. 논리 식별자와 물리 발화의 분리는 Adapter 소관이며(01 §0·§4.1), 이 환경의 확정 발화 = `uaf-new`(entry/adapters/claude/entry-binding.md §3). `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰 사용이 허용된다(structure.md §2).
- **형태 A/B 공존** — 이 파일 자체는 실행 코드 0(형태 A 문서 명령)이고, Entry Resolution 엔진(고정 5단계, 01 §3.2-A)은 (i) 형태 B 로더 `entry/adapters/claude/entry_resolve.py`(권장 경로) 또는 (ii) 주 세션이 규약 절차를 실수행하는 형태 A 폴백으로 실현된다. 두 경로의 계약·결정 테이블은 동일하다(structure.md §7 C-1).
- **정본 재정의 0** — 절차·결정 행·게이트는 전부 정본 포인터(01-entry·entry-binding)로만 안내하며 값을 하드코딩하지 않는다.

---

## §1. 목적

`/new` 호출 시 **순수 Greenfield 진입**의 Entry Resolution을 수행하도록 안내한다 — 빈 워크스페이스에서 새 프로젝트를 시작하는 Discovery를 요청한다(기본 Discovery mode = `greenfield`, 01 §3.1). 출력은 **Discovery Request 하나까지**다 — Entry는 Discovery를 수행하지 않고 Project Contract를 생성하지 않는다(01 EN-INV 1·2).

---

## §2. 진입 절차 (Entry Resolution — 정본 포인터)

### 형태 B 로더 호출 (권장 경로)

```
python entry/adapters/claude/entry_resolve.py --entry new --folder <대상 폴더> [--intent new]
```

- `--entry`는 슬래시 없는 `new`가 1차 형태다(주 세션 Bash 도구 호출 시 `/new`가 MSYS 경로로 변환되는 문제 회피). `/new`도 허용·정규화된다.
- 사용자가 진입 시 **대상 폴더 + 신규/기존 의도**를 주입한다(entry-binding §4.0). `--intent` 미지정 시 `/new`는 `new`가 기본이다(entry-registry `defaultIntent`). `--intent`는 provenance 에코이며 게이트를 구동하지 않는다.
- 로더는 파일시스템을 **순수 판독**(contract-presence·repository-presence 유/무만 — 내용 파싱 0·폴더 생성 0·EN-INV 1·2)해 결정 테이블(01 §3.2-D)을 결정적으로 대조하고, 단일 Discovery Request `{mode, inputs, policy}` + 엔진 메타(`matchedRow`·`gate`)를 JSON으로 방출한다(entry-binding §4.4·§5).
- **형태 A 폴백** — 로더가 가용하지 않으면 주 세션이 아래 고정 5단계를 직접 실수행한다.

### 고정 5단계 (로더가 실현·폴백이 실수행)

1. **매칭.** `/new`의 Entry Descriptor를 Entry Registry에서 찾는다(01 §3.2-A).
2. **증거 수집(관측).** 출발점은 **사용자 주입**이다 — 주입된 대상 폴더·신규/기존 의도가 requiredEvidence(contract-presence·repository-presence) 관측의 로커스를 확정한다. 물리 판정 수단(폴더 스코프·Contract 인스턴스 파일 스캔·충돌 처리)은 `entry/adapters/claude/entry-binding.md` §4.0~§4.2 소관이다(재정의 0). **Entry는 유/무만 관측하며 Contract 내용을 해석하지 않는다**(01 EN-INV 2).
3. **우선순위 평가.** `/new`의 결정 행(01 §3.2-D 행 1~4)을 관측 증거에 대조해 단일 결과 행을 선택한다.
4. **결정성 검증.** 관측 조합이 단일 행에만 매칭됨을 확인한다(01 §3.2-A 4단계·EN-INV 3).
5. **방출.** 단일 Discovery Request {mode, inputs, policy}로 방출한다(직렬화·전달 = entry-binding.md §5). **Entry는 여기서 멈춘다** — Discovery 수행·Contract 생성은 하지 않는다(01 EN-INV 1·2).

### 게이트 규칙과 사용자 개입 지점 (Preserve Human Authority, 01 EN-INV 6)

- **게이트는 canonical 결정 테이블 policy로만 구동한다.** 매칭 행의 **`policy.ref == user-confirmation-gate`**(canonical 행 2·3·4·5·방출 `gate: true`)이면 주 세션이 **사용자 확인 게이트를 제시**한다. 게이트 이유는 `policy.conflict`(repository-present/contract-present/nothing-to-continue)에 있다. 로더는 canonical policy를 표면화만 하고 확정 결정을 내리지 않으며, **병행 conflict 신호를 두지 않는다**(Policy as Data 단일 소스).
- `/new`는 **순수 Greenfield 전용**이므로 관측 증거에 기존 Contract 또는 Repository가 나타나면 사용자 의도와 증거가 상충한다(행 2·3·4). 이때 Entry는 **스스로 재라우팅·덮어쓰기를 결정하지 않고** policy에 사용자 확인 게이트를 표기한다(D3 ①·EN-INV 6). 사용자가 `/continue`를 재발화하면 결정 테이블이 결정적으로 재해소된다(01 §8 예2).
- **주입 선언 ↔ 실제 폴더 상태 상충은 별도 게이트가 아니라 canonical policy에 포섭된다** — 주입한 "신규" 의도와 달리 그 폴더에 실질 콘텐츠가 존재하면 관측이 행 2·4로 해소되고 그 canonical policy가 이미 사용자 확인 게이트다.
- Entry는 관측값을 임의로 덮어쓰지 않으며 게이트를 데이터로 표기할 뿐 확정 결정을 내리지 않는다(EN-INV 6·ARCHITECTURE.md §8 UAF-INV ⑤). 물리 판정·게이트 표기 수단은 entry-binding.md §4 소관이다(재정의 0).

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선하며, 발견되는 충돌은 Advisor에게 보고한다.

| 안내 항목 | 정본 (가리키기만 함) |
|---|---|
| Entry `/new` 논리 정의·기본 mode(`greenfield`) | `entry/specs/01-entry.md` §3.1 |
| Entry Descriptor 등록 모델·Resolution 엔진 고정 5단계 | `entry/specs/01-entry.md` §3.2-A |
| 결정 테이블(행 1~4)·판별 규칙 D3 ①·충돌 처리 | `entry/specs/01-entry.md` §3.2-D |
| mode 네임스페이스(확장 가능) | `entry/specs/01-entry.md` §3.2-E |
| Entry 불변(EN-INV 1~6) | `entry/specs/01-entry.md` §3.3 |
| 결정 테이블 데이터(8조합·Evidence·게이트 policy·관측 규칙) | `entry/adapters/claude/entry-registry.json` (Policy as Data 단일 소스) |
| Contract 저장 위치·직렬화 | `planning/adapters/claude/contract-binding.md` §3·§4 |
| Eliciting 인터뷰 행동 규약 (하류 Discovery 진행 시) | `discovery/adapters/claude/discovery-binding.md` §7.1 |
| Discovery Request 상위 추상 {mode, inputs, policy} | `ARCHITECTURE.md` §12.2 |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다.
