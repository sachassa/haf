---
description: UAF 공식 진입점 /continue(기존 프로젝트 이어가기 — Incremental/Brownfield)의 물리 발화 형태 — Entry Resolution 규약 절차(엔진 5단계·결정 테이블)와 사용자 개입 지점을 정본 포인터로 안내한다.
---

# /continue — UAF 이어가기 진입 (물리 발화: uaf-continue 명령)

상태: v1.2 Baseline + 형태 B 로더(entry_resolve.py)
상위 규약: .claude/AGENT.md

---

## §0. 이 명령의 위치와 성격

- **물리 발화 형태** — 논리 Entry `/continue`(entry/specs/01-entry.md §3.1 등재)의 물리 진입 형태다. 논리 식별자와 물리 발화의 분리는 Adapter 소관이며(01 §0·§4.1), 이 환경의 확정 발화 = `uaf-continue`(entry/adapters/claude/entry-binding.md §3). `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰 사용이 허용된다(structure.md §2).
- **형태 A/B 공존** — 이 파일 자체는 실행 코드 0(형태 A 문서 명령)이고, Entry Resolution 엔진(고정 5단계, 01 §3.2-A)은 (i) 형태 B 로더 `entry/adapters/claude/entry_resolve.py`(권장 경로) 또는 (ii) 주 세션이 규약 절차를 실수행하는 형태 A 폴백으로 실현된다. 두 경로의 계약·결정 테이블은 동일하다(structure.md §7 C-1).
- **정본 재정의 0** — 절차·결정 행·게이트는 전부 정본 포인터(01-entry·entry-binding)로만 안내하며 값을 하드코딩하지 않는다.

---

## §1. 목적

`/continue` 호출 시 **기존 프로젝트를 이어가는 진입**의 Entry Resolution을 수행하도록 안내한다 — 증거에 따라 **Incremental Discovery**(Project Contract 존재 시) 또는 **Brownfield Full Discovery**(Contract 부재·Repository 존재 시, 최초 Contract 생성)를 요청한다(01 §3.1). 출력은 **Discovery Request 하나까지**다 — Entry는 Discovery를 수행하지 않고 Project Contract를 생성하지 않는다(01 EN-INV 1·2).

---

## §2. 진입 절차 (Entry Resolution — 정본 포인터)

### 형태 B 로더 호출 (권장 경로)

```
python entry/adapters/claude/entry_resolve.py --entry continue --folder <대상 폴더> [--intent existing]
```

- `--entry`는 슬래시 없는 `continue`가 1차 형태다(주 세션 Bash 도구 호출 시 `/continue`가 MSYS 경로로 변환되는 문제 회피). `/continue`도 허용·정규화된다.
- 사용자가 진입 시 **대상 폴더 + 신규/기존 의도**를 주입한다(entry-binding §4.0). `--intent` 미지정 시 `/continue`는 `existing`이 기본이다(entry-registry `defaultIntent`). `--intent`는 provenance 에코이며 게이트를 구동하지 않는다.
- 로더는 파일시스템을 **순수 판독**(contract-presence·repository-presence 유/무만 — 내용 파싱 0·폴더 생성 0·EN-INV 1·2)해 결정 테이블(01 §3.2-D)을 결정적으로 대조하고, 단일 Discovery Request `{mode, inputs, policy}` + 엔진 메타(`matchedRow`·`gate`)를 JSON으로 방출한다(entry-binding §4.4·§5).
- **형태 A 폴백** — 로더가 가용하지 않으면 주 세션이 아래 고정 5단계를 직접 실수행한다.

### 고정 5단계 (로더가 실현·폴백이 실수행)

1. **매칭.** `/continue`의 Entry Descriptor를 Entry Registry에서 찾는다(01 §3.2-A).
2. **증거 수집(관측).** 출발점은 **사용자 주입**이다 — 주입된 대상 폴더·신규/기존 의도가 requiredEvidence(contract-presence·repository-presence) 관측의 로커스를 확정한다. 물리 판정 수단(폴더 스코프·Contract 인스턴스 파일 스캔·충돌 처리)은 `entry/adapters/claude/entry-binding.md` §4.0~§4.2 소관이다(재정의 0). **Entry는 유/무만 관측하며 Contract 내용을 해석하지 않는다**(01 EN-INV 2).
3. **우선순위 평가.** 결정 행(01 §3.2-D 행 5~8)을 관측 증거에 대조해 단일 결과 행을 선택한다 — **Contract 존재 → Incremental**(D3 ③, 행 7·8; Repository 유무와 무관하게 우선), **Contract 부재 + Repository 존재 → Brownfield Full Discovery·최초 Contract 생성**(D3 ②, 행 6).
4. **결정성 검증.** 관측 조합이 단일 행에만 매칭됨을 확인한다(01 §3.2-A 4단계·EN-INV 3).
5. **방출.** 단일 Discovery Request {mode, inputs, policy}로 방출한다(직렬화·전달 = entry-binding.md §5). **Entry는 여기서 멈춘다** — Discovery 수행·Contract 생성은 하지 않는다(01 EN-INV 1·2).

### 게이트 규칙과 사용자 개입 지점 (Preserve Human Authority, 01 EN-INV 6)

- **게이트는 canonical 결정 테이블 policy로만 구동한다.** 매칭 행의 **`policy.ref == user-confirmation-gate`**(`/continue`에서는 **행 5**뿐: 이어갈 실체 전무·nothing-to-continue·방출 `gate: true`)이면 주 세션이 **사용자 확인 게이트를 제시**한다. 로더는 canonical policy를 표면화만 하고 확정 결정을 내리지 않으며, **병행 conflict 신호를 두지 않는다**(Policy as Data 단일 소스).
- **주입 의도 ↔ 실제 폴더 상태 상충은 별도 게이트가 아니라 canonical policy에 포섭된다.** Contract 무 + Repository 무면 관측이 행 5로 해소되고 그 policy가 사용자 확인 게이트다. 반면 **Contract가 존재하면(행 7·8) repo 유무와 무관하게 incremental·게이트 없음**이다 — Contract 자체가 이어갈 대상이므로(D3 ③). 즉 "기존 선언인데 repo 무"라도 Contract가 있으면 거짓 게이트를 만들지 않는다(**행 7 = 게이트 없음**).
- Entry는 관측값을 임의로 덮어쓰지 않는다(EN-INV 6). 확정 게이트(사용자 승인)는 하류에서 존중된다(ARCHITECTURE.md §8 UAF-INV ⑤). 물리 판정·게이트 표기 수단은 entry-binding.md §4 소관이다(재정의 0).

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선하며, 발견되는 충돌은 Advisor에게 보고한다.

| 안내 항목 | 정본 (가리키기만 함) |
|---|---|
| Entry `/continue` 논리 정의·mode(`incremental`/`brownfield`) | `entry/specs/01-entry.md` §3.1 |
| Entry Descriptor 등록 모델·Resolution 엔진 고정 5단계 | `entry/specs/01-entry.md` §3.2-A |
| 결정 테이블(행 5~8)·판별 규칙 D3 ②·D3 ③·충돌 처리 | `entry/specs/01-entry.md` §3.2-D |
| mode 네임스페이스(확장 가능) | `entry/specs/01-entry.md` §3.2-E |
| Entry 불변(EN-INV 1~6) | `entry/specs/01-entry.md` §3.3 |
| 결정 테이블 데이터(8조합·Evidence·게이트 policy·관측 규칙) | `entry/adapters/claude/entry-registry.json` (Policy as Data 단일 소스) |
| Contract 저장 위치·직렬화 | `planning/adapters/claude/contract-binding.md` §3·§4 |
| Eliciting 인터뷰 행동 규약 (하류 Discovery 진행 시) | `discovery/adapters/claude/discovery-binding.md` §7.1 |
| Discovery Request 상위 추상 {mode, inputs, policy} | `ARCHITECTURE.md` §12.2 |
| 구현 단계 진입(Contract 확정 후·다운스트림 발화) | `.claude/commands/uaf-implement.md` — Entry는 Discovery Request까지 멈추고(EN-INV 1), 구현 orchestration은 `/uaf-implement`로 별도 발화한다(자동 체이닝 아님) |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다.
