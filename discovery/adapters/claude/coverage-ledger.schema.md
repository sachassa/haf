# coverage-ledger.json — 커버리지 원장 스키마 (커버리지 강제 트랙 Wave 1)

Discovery 종단 판정 축 4(Coverage — `discovery/specs/02-discovery.md` §3.7)의 근거가 되는 **Coverage 원장**의
물리 형식·필드 의미·경로 규약·정책 결속을 정의한다. 02 §3.7 말미가 "Coverage 원장의 물리 파일 형식·경로·
직렬화는 정의하지 않는다 — Adapter 소관이다"로 위임한 지점의 실현이며, 어댑터 경계
(`discovery/adapters/claude/`) 소속이다. 정본 계약(02 §3.3 상태·§3.5 Event·§3.7 판정식·§3.8 DISC-INV-10)을
재정의하지 않는다. 선례 = `orchestration/adapters/claude/design-manifest.schema.md`(스키마는 md·원장은 JSON).

## 소유 경계

- **인터뷰 수행 측이 산출한다** — 축을 심문하거나 제외 결정을 내린 주체가 이 원장에 상태를 기록한다.
- **판정 측이 검증한다** — 미심문 0 대조와 그에 따른 종단 판정(`Ready`/`ReadyWithAssumptions`/`Escalated`)은
  체커·Orchestrator 소관이다.
- **이 문서는 형식과 계약만 규정한다** — 판정 로직을 소유하지 않는다. `design-manifest.schema.md` 의
  "체커는 매니페스트를 판독만 한다 / 선언 완전성만 판정한다" 경계 처리와 동형이다.

## 축 실값의 소유 (사본 금지)

필수 질문 축의 **실값**(축 `id`·`label`·`dimension`·`highImpact`)은 Discovery Policy 데이터
(`uahf/framework/adapters/claude/discovery-data/policy/<ref>-policy.yaml` 의 `coverage.requiredAxes`)가
**단독 소유**한다. 본 문서는 축 실값을 열거하지 않는다 — 열거하면 드리프트 지점이 신설된다. 구성 요건의
정본 문면은 `discovery/adapters/claude/discovery-binding.md` §8.2 (마)이며, 축 집합이 정본 본문이 아니라
데이터에 있어야 하는 근거는 DISC-INV-7·루트 §8 UAF-INV ⑥(Strategy Provider마다 다른 축 집합)이다.

## 배치 위치

원장은 그 판정이 정당화하는 **Contract 인스턴스와 같은 디렉터리**에 병치한다.

```
<Contract 인스턴스 디렉터리>/coverage-ledger.json
```

Contract 인스턴스 디렉터리는 `planning/adapters/claude/contract-binding.md` §4.1·§4.2 가 소유하는 이원화
경로다 — 소비 프로젝트 일반 관례 `<workspace>/.claude/project-contract/` · 본 저장소 dogfooding 격리
`uahf/framework/adapters/claude/discovery-data/contracts/<project>/`. 원장은 그 각각의 디렉터리에 놓인다.

- **파일 1건 = Contract 인스턴스 디렉터리 1건.** 원장은 그 디렉터리의 **현재** Contract 발행을 뒷받침하는
  판정 근거이며 갱신 대상 파일이다. 어느 run 에서 도출됐는지는 원장 자신의 `mode`·`runId` 필드가
  선언하므로(§스키마) 경로가 run 을 식별하지 않아도 자기서술로 확정된다.
- **이력 손실 0 — 원장은 파생 뷰다.** 원장은 append-only Event 로그를 대체하지 않는다. 상태 변화의
  이력은 Event 로그(`QuestionAsked`·`AnswerReceived` 등 02 §3.5)가 `discovery-binding.md` §3.4 의
  `events/<mode>-<run-id>/` 에서 계속 단독 소유하고, 원장은 **그 이력에서 도출된 축별 현재 상태의
  판정 근거 표면**이다. 파생 뷰가 정본 로그를 떠나 판정 지점 옆에 놓이는 것은 이력 손실이 아니다 —
  run 단위 격리(§3.4)도, 다중 run 이력도 무촉이다.
- **배치 근거 = 결정적 도출.** 판정 근거를 판정 대상 옆에 두면 Contract 파일 경로에서 원장 경로가
  **탐색·추정 0**으로 확정된다(같은 디렉터리). 이 결속이 없으면 Contract 쓰기 시점의 기계 검사가
  성립하지 않는다 — 전역 run 트리 배치에서는 Contract 경로에 run 좌표가 0건이라 원장을 결정적으로
  지목할 수 없고, Contract **내용**에서 run 을 읽는 우회는 피심문 텍스트가 자기 검사 여부를 결정하는
  자기신고 구조가 되어 강제가 성립하지 않는다. 소비 지점 = `pretooluse_coverage_guard.py`.
- **dogfooding 격리 보존.** 본 저장소 인스턴스의 원장은 `discovery-data/contracts/<project>/` 안에
  머무르며 라이브 `.claude/` 규약 표면으로 나오지 않는다(contract-binding §4.2 격리 근거·UAF-INV ① 유지).
- **경로 해석.** 원장 내부에는 파일 경로 필드가 0건이므로 매니페스트 선례에서 문제가 됐던 "기준
  디렉터리 상대/절대" 해석 분기가 이 원장에는 존재하지 않는다. 유일한 외부 참조인 `policyRef` 는
  `discovery-binding.md` §8.3 (a) 규약으로 하네스 트리의 정책 프로파일에 해소되며, 그 해소 기준은
  소비 워크스페이스가 아니라 하네스 트리다(정책 프로파일의 소유자가 하네스이기 때문).

uaf-verified: 위 배치 개정의 "이력 손실 0" 논거는 본 문서 직전 문면("원장은 그 이력에서 도출된 축별
현재 상태의 판정 근거 표면"·"append-only Event 로그를 대체하지 않는다")과 `discovery-binding.md`
§3.4(Event 로그 run 단위 격리 — 본 개정으로 무촉)를 대조해 성립을 확인했다. Contract 디렉터리 이원화는
`contract-binding.md` §4.1·§4.2 직독과 `find . -name "project-contract*"` 저장소 전수 실행으로 확인했다.
**검색 범위** = 그 3개 문서 절과 저장소 작업 트리의 그 이름 패턴이며, 이 저장소 밖 소비 프로젝트의
실배치는 실측 범위 밖이다.

## 스키마

```jsonc
{
  // 스키마 식별자. 필수·비공백. 형식 변경 시 이 값으로 세대를 구분한다.
  "schema": "coverage-ledger/v1",

  // 이 원장이 속한 run. 배치 경로의 <mode>-<run-id> 와 동일 값이어야 한다(경로↔내용 자기정합).
  "mode": "<greenfield | incremental | brownfield | …>",   // 필수. 02 §3.3-A Discovery Request 의 mode.
  "runId": "<run 식별자>",                                  // 필수·비공백.

  // 축 집합의 출처가 된 정책 프로파일 참조. 해소 규약 정본 = discovery-binding.md §8.3 (a):
  // <ref> → uahf/framework/adapters/claude/discovery-data/policy/<ref>-policy.yaml
  "policyRef": "<ref>",                                     // 필수·비공백. 예: "default" | "lightweight".

  // 정책 coverage.requiredAxes 의 각 원소에 대해 1건씩. 정책 축 id 와 1:1 대응한다.
  "axes": [
    {
      "id": "<정책 coverage.requiredAxes[].id>",  // 필수·비공백. 정책에 없는 id 는 미상응 항목이다. 중복 금지.
      "status": "interrogated" | "excluded" | "unasked",   // 필수. 아래 상태 어휘 표.

      // status=interrogated 시 필수: 이 축을 향한 질문·응답의 근거.
      "evidenceGrade": "user-stated" | "inferred" | "assumed",  // 근거 등급 02 §3.12 (사용자 진술 > 추론 > 가정).

      // status=excluded 시 필수 2필드(정책 coverage.exclusionRule.requiredFields 와 결속).
      "reason": "<제외 사유·비공백>",
      "confirmedBy": "<확인 주체>",

      // status=excluded 이고 정책이 그 축을 highImpact: true 로 선언한 경우 필수.
      // 값 = 즉시 표면화가 이뤄진 지점(승인 게이트까지 미루지 않았다는 기록).
      "surfacedAt": "<즉시 표면화 지점>"
    }
  ]
}
```

### 상태 어휘 (3값 — 02 §3.7 축 4)

| 기계 값 | 라벨 | 뜻 | 요건 |
|---|---|---|---|
| `interrogated` | 심문됨 | 그 축을 향한 질문이 제시되고 응답이 도착했다 | `evidenceGrade` 동반. `assumed`·`inferred` 는 심문됨의 근거가 되지 못한다(아래 규칙 (c)) |
| `excluded` | 사유 기록 제외 | 이 프로젝트에 해당 없음·불필요로 판단하고 그 판단을 기록했다 | `reason` 비공백 **AND** `confirmedBy` 존재 |
| `unasked` | 미심문 | 아직 묻지 않았다 | 양 종단 진입 전에 `interrogated` 또는 `excluded` 로 귀결해야 한다 |

제3의 상태 값을 창설하지 않는다. 어휘를 기계 값(ASCII)과 라벨(한국어)로 분리하는 이유는 축 `id` 를 ASCII 로
두는 이유와 같다 — 라벨 표기 변경이 데이터 결속을 깨뜨리지 않게 한다.

### 판정 규칙 (형식 계약 — 판정 수행 주체는 체커)

이 절은 **무엇이 충족인가**의 계약이며, 그 대조를 수행하는 코드는 이 문서 밖(체커)이 소유한다.

| 조건 | 충족 | 미충족 시 |
|---|---|---|
| 정책 `requiredAxes` 의 각 축 id 가 원장 `axes` 에 1건씩 존재 | 대응 완전 | 원장에 없는 축 = **미심문**과 동치(침묵 생략 금지·DISC-INV-10) |
| `status == "unasked"` 인 항목 수 | **0** | 1건 이상이면 축 4 미충족 — `Ready`·`ReadyWithAssumptions` 어느 종단에도 도달하지 못한다 |
| `status == "excluded"` 항목 | `reason` 비공백 **AND** `confirmedBy` 존재 | 둘 중 하나라도 결여 → 제외로 성립하지 않고 **미심문**으로 계수 |
| `status == "excluded"` **AND** 정책 `highImpact: true` | `surfacedAt` 존재 | 결여 → 즉시 표면화 기록 부재(원칙 11 (c) 미이행) |
| `status == "interrogated"` **AND** `evidenceGrade` 가 `inferred`/`assumed` | — | 추론·가정 충족은 심문됨이 아니라 **미심문**으로 계수(02 §3.7 축 4 "추론 충족 불가") |
| 원장 `axes` 에 정책에 없는 id | — | 미상응 항목 — 정책이 축 집합의 단일 소유자이므로 원장이 축을 창설하지 못한다 |
| 정책 축 1건에 대응하는 원장 항목 수 | **정확히 1** | 2건 이상이면 **중복 위반** — 아래 「축 id 중복」 |

#### 축 id 중복 (계약 명시)

위 §스키마의 `id` 주석("중복 금지")이 요구하는 1:1 대응이 깨진 경우의 거동을 이진으로 확정한다.

- **판정 = 위반이다.** 정책 축 1건에 대응하는 원장 항목이 2건 이상이면 그 축은 게이트를 통과하지 못한다.
  통과 경로(첫 항목 채택·마지막 항목 채택·병합)는 **0**이다.
- **상태 판정은 수행하지 않는다.** 중복 항목들의 `status`·`evidenceGrade`·제외 요건은 대조하지 않는다 —
  **어느 항목이 정본인지가 미확정**이므로 상태 대조 자체가 성립하지 않는다. 중복은 상태 미충족과 별개의
  독립 위반 사유이며, "중복이지만 둘 다 `interrogated` 이니 통과"로 흡수되지 않는다.
- **관대 해석 금지 근거.** 중복 중 하나를 임의 선택하면 같은 원장이 선택 규칙에 따라 다른 판정을 낼 수
  있어 결정성이 깨지고, 미심문 항목을 심문됨 항목으로 가리는 경로가 열린다(DISC-INV-10 침묵 생략 금지).
- **정책 측 중복도 동형이다.** 정책 `coverage.requiredAxes` 에 같은 축 `id` 가 2건 이상이면 축 집합 자체가
  미확정이므로 대조 이전에 차단한다.

uaf-verified: 위 4항은 `discovery/adapters/claude/coverage_check.py` 의 `check_coverage`(정책 축 순회 중
`len(found) > 1` 분기 — 오류 append 후 `continue` 로 `_check_axis_entry` 미호출)와 `load_policy_axes`
(`aid in seen` 분기 — 오류 append 후 `continue`) 직독으로 확인했고, `tests/test_coverage_check.py`
`test_N7_duplicate_id_in_ledger` 가 그 거동을 고정함을 확인했다. **검색 범위** = 그 2개 파일이며, 본 절은
코드가 이미 수행하는 거동을 계약으로 승격한 것이고 판정 규칙을 새로 창설하지 않는다.

- **가정 대체 불가.** 축 2(Confidence)와 달리 이 축은 `ReadyWithAssumptions` 경로에서도 가정으로 대체되지
  않는다(02 §3.7 축 4·T20 Guard). 예산 소진 시점에 `unasked` 가 남으면 귀결은 `Escalated` 다(T15).
- **판정 불가는 통과가 아니다.** 원장 파일 부재·판독 실패·정책 판독 실패는 축 4 판정이 **미확정**인 상태이며,
  미확정을 통과로 처리하면 이 축이 막으려는 침묵 생략을 그대로 재생산한다(이진 상태 원칙 ·
  `design-manifest.schema.md` §비적용과 차단의 경계 동형).
- **내용 진위는 게이트 몫이다.** 이 계약은 **선언 완전성**만 규정한다 — `interrogated` 로 선언된 축이 실제로
  실질 심문을 받았는지, `reason` 이 타당한지의 진위는 내용 판정이므로 사용자 승인 게이트(축 3)·검증이
  판정한다(`design-manifest.schema.md` 의 `covered` 진위 경계와 동형).

## 예시 — 축 1건 제외(고임팩트) · 나머지 심문됨

```jsonc
{
  "schema": "coverage-ledger/v1",
  "mode": "greenfield",
  "runId": "20260729-001",
  "policyRef": "default",
  "axes": [
    { "id": "why-strategic-motivation", "status": "interrogated", "evidenceGrade": "user-stated" },
    { "id": "structure-delivery-direction", "status": "excluded",
      "reason": "사내 배치 파이프라인 — 사용자 대면 전달 플랫폼·외부 API 연동이 0으로 확정",
      "confirmedBy": "user",
      "surfacedAt": "Eliciting 중 즉시 제시(고임팩트 축 — 승인 게이트 대기 0)" }
    // … 정책 coverage.requiredAxes 의 나머지 원소도 각각 1건씩 둔다.
    //     실값 열거는 정책 데이터가 소유하므로 이 예시는 형식 예시이며 축 목록 사본이 아니다.
  ]
}
```

**이 예시의 값이 본 문서 규약대로 해석되는지 (선례의 함정 회피).**

| 항목 | 값 | 해석 근거 |
|---|---|---|
| 원장 실경로 (소비 프로젝트) | `<workspace>/.claude/project-contract/coverage-ledger.json` | 위 §배치 위치 — Contract 인스턴스 디렉터리 병치. `mode`·`runId` 필드가 도출 run 을 자기서술한다 |
| 원장 실경로 (본 저장소 dogfooding) | `uahf/framework/adapters/claude/discovery-data/contracts/uahf/coverage-ledger.json` | 동일 규약 + contract-binding §4.2 격리 경로 |
| `policyRef` 해소 | `uahf/framework/adapters/claude/discovery-data/policy/default-policy.yaml` | `discovery-binding.md` §8.3 (a) ref 해소 규약(`<ref>` → `<ref>-policy.yaml`) |
| 축 `id` 대조 | 위 2건은 그 파일 `coverage.requiredAxes[].id` 에 실재 | 정책 데이터가 축 집합의 단일 소유자 |
| `highImpact` 축 판정 | `structure-delivery-direction` = `true` → `surfacedAt` 필수 → 예시에 존재 | 위 판정 규칙 표 4행 |

uaf-verified: 위 표 4행은 (1) `discovery-binding.md` §3.4 run 디렉터리 규약·§4.2 run 루트 배치 관례 판독,
(2) `discovery-binding.md` §8.3 (a) ref 해소 규약 판독, (3) `default-policy.yaml` 을 `yaml.safe_load` 로
적재해 `coverage.requiredAxes` 의 `id` 집합에 예시 2건이 실재함과 `structure-delivery-direction` 의
`highImpact == true` 를 대조, (4) 그 파일이 위 해소 경로에 실재함을 파일 열람으로 확인해 얻었다.
**검색 범위** = 그 2개 파일(binding·default-policy.yaml)이며, 실 run 에서 이 원장을 생성·소비하는
왕복(체커 실행 포함)은 이 문서의 실측 범위 밖이다 — 체커는 별 Wave 소관이다.

## 원장 부재

`coverage-ledger.json` 이 없으면 축 4는 **미확정**이며 종단 판정은 진행하지 못한다(위 "판정 불가는 통과가
아니다"). 부재를 "제외 0·미심문 0"으로 해석하는 경로는 두지 않는다 — 그 해석이 곧 침묵 생략이다.
