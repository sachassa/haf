# design-manifest.json — 설계 매니페스트 스키마 (§DC-1 Wave 3)

설계완성도 게이트(`orchestration/adapters/claude/design_completeness.py`)가 소비하는 매니페스트의
스키마·필드 의미·예시를 정의한다. 이 문서는 어댑터 경계(orchestration/adapters/claude/) 소속이며,
프레임워크 코어의 정책 스키마(04-solution-design SP-INV 9·바인딩 §7.2 (다))를 재정의하지 않는다.

## 소유 경계

- **Solution Design 이 산출한다** — SD 단계가 선언 접점·연계와 산출/제외 결정을 반영해
  `design-manifest.json` 을 워크스페이스에 배치한다.
- **오케스트레이션이 검증한다** — 엔진(resolve_gate.resolve_structural)이 impl 단위를 그래프에
  편입(task_added 승격)하기 직전, `check_design_completeness` 로 침묵 누락을 결정적으로 차단한다.

산출과 검증의 소유가 분리된다. 이 체커는 매니페스트를 **판독만** 한다(수정·생성 0).

## 배치 위치 (소비 프로젝트)

```
<workspace>/.claude/solution-design/policy/default-policy.yaml   # 필수 산출물 정책(SD 데이터로 시드)
<workspace>/.claude/solution-design/design-manifest.json         # 이 문서의 대상
```

`<workspace>` = run config.json 의 `workspace_dir`(부재 시 `<run_dir>/workspace`). SD 데이터 관례상
정책·매니페스트는 워크스페이스의 `.claude/solution-design/` 아래에 둔다.

## 스키마

```jsonc
{
  // 접점(웹·앱·포털 등) 선언. 비공집합이면 정책 requirementClasses.touchpoint 항목이 required 가 된다.
  // 미선언(빈 배열/생략)이고 정책에 touchpoint 항목이 있으면 클래스 전체 제외 —
  // 아래 classExclusions.touchpoint 확인이 필요하다(없으면 차단·자동 N/A 폐기).
  "declaredTouchpoints": [ "<접점 식별자>", ... ],

  // 외부 연계 선언. 비공집합이면 requirementClasses.interface 항목이 required 가 된다.
  // 미선언(빈 배열/생략)이고 정책에 interface 항목이 있으면 클래스 전체 제외 —
  // 아래 classExclusions.interface 확인이 필요하다(없으면 차단·자동 N/A 폐기).
  "declaredInterfaces": [ "<연계 식별자>", ... ],

  // 접점/연계 클래스가 미선언(declaredTouchpoints/declaredInterfaces 공집합)으로 전체 제외될 때,
  // 그 클래스 드롭을 표면화·확인한 기록(고임팩트 이탈·원칙 11 (c)). 클래스가 선언(트리거)되면 불필요.
  "classExclusions": {
    "touchpoint": { "reason": "<제외 사유·비공백>", "confirmedBy": "<확인 주체>" },
    "interface":  { "reason": "<제외 사유·비공백>", "confirmedBy": "<확인 주체>" }
  },

  // 필수 산출물별 상태. id 는 정책 projectionSelection.defaultRequiredSet[].id 와 대응한다.
  "artifacts": [
    {
      "id": "<defaultRequiredSet 의 id>",   // 필수·비공백 문자열. 중복 금지.
      "status": "produced" | "excluded",     // 필수.
      "path": "<산출물 경로>",               // status=produced 시 선택. 주어지면 존재 검사(매니페스트 기준 상대/절대).
      "reason": "<제외 사유>",               // status=excluded 시 필수·비공백.
      "confirmedBy": "<확인 주체>"           // status=excluded 시 필수(정당화 제외의 사용자 확인 기록).
    }
  ],

  // (선택·Visual Contract 트랙) 디자인 필수 요소 커버리지. 정책 designElements 섹션이 활성일 때만
  // (= 정책에 designElements 존재 AND declaredTouchpoints 비공집합) 검사된다. 정책 부재/접점 미선언 시
  // 이 키는 무시된다(하위호환). project = 프로젝트 단위 요소, screens = 화면별 요소.
  "designElements": {
    "project": {
      "<elementId>": { "status": "covered", "pointer": "<산출물 내 위치/경로>" }
      // 또는 { "status": "excluded", "reason": "<비공백>", "confirmedBy": "<확인 주체>" }
    },
    "screens": {
      "<screenId>": {
        "<elementId>": { "status": "covered", "pointer": "..." }   // 동일 형태(covered|excluded)
      }
    }
  }
}
```

### designElements 판정 규칙 (체커 — 선언 완전성만)

정책 `designElements` 섹션이 **활성**(정책에 섹션 존재 **AND** `declaredTouchpoints` 비공집합·`appliesWhen: touchpoint`)일 때만 검사한다. 활성 시:

- **(a) projectScope 전 요소** 가 매니페스트 `designElements.project` 에 `covered` 또는 정당화 `excluded` 여야 한다.
- **(b) screens 비공집합** 필수 — 접점 선언인데 화면 요소 선언이 하나도 없으면 오류(silentOmission).
- **(c) 각 화면 × screenScope 전 요소** 가 `designElements.screens.<screenId>` 에 `covered`/정당화 `excluded` 여야 한다.
- **(d) `excluded`** 는 `reason` 비공백 **AND** `confirmedBy` 필수(산출물 `excluded` 요건 동형).
- **(e) 미선언 요소** 또는 `covered`/`excluded` 아닌 status = 침묵 누락 오류.

| 요소 status | 통과 조건 | 위반 시 |
|-------------|-----------|---------|
| `covered`   | 무조건 통과(선언 완전성 충족) | — |
| `excluded`  | `reason` 비공백 **AND** `confirmedBy` 존재 | 둘 중 하나 결여 → 요건 미충족 오류 |
| (부재/기타) | — | 침묵 누락 오류(silentOmission 금지) |

**정책 요소의 `criteria`(정보성 — 체커 미판정).** 정책 `designElements` 요소(예: `accessibility-floor`)는 선택 필드 `criteria`(문자열 목록·접근성 실값 등)를 병기할 수 있다. `criteria` 는 **검증 게이트(사람 판정)의 기준 문면**이며 `design_completeness` 체커는 이를 판정하지 않는다(체커는 매니페스트의 covered/정당화 excluded 선언 완전성만 본다). 정책의 추가 키에 체커는 tolerant 하다(하위호환).

**결정성·경계.** 검사 순서는 projectScope(정책 정의 순서) → 화면(매니페스트 삽입 순서) × screenScope(정책 정의 순서)로 결정적이다. 체커는 **선언 완전성만** 판정한다 — `covered` 의 진위(실제로 그 요소가 화면에 반영됐는지)와 `screens` 키가 실제 화면 목록과 대응하는지의 진위는 내용 파싱 없이는 판정 불가하므로 **CP2/사용자 게이트(mock 리뷰) 몫**이다(기존 "결정적 슬라이스·최종 승인은 게이트" 문면 동형). 접점 미선언 시 이 섹션은 비적용이며, touchpoint 클래스 전체 제외는 `classExclusions.touchpoint` 경로가 표면화한다.

### status 판정 규칙 (체커)

| status     | 통과 조건                                             | 위반 시                          |
|------------|-------------------------------------------------------|----------------------------------|
| `produced` | (path 미지정) 무조건 통과 · (path 지정) 파일 존재     | path 지정인데 부재 → 오류        |
| `excluded` | `reason` 비공백 **AND** `confirmedBy` 존재            | 둘 중 하나라도 결여 → 요건 미충족 오류 |
| (부재)     | —                                                     | 침묵 누락 오류(silentOmission 금지) |
| (기타 값)  | —                                                     | 침묵 누락 오류                    |

### 클래스 전체 제외 규칙 (touchpoint/interface 미선언)

정책에 touchpoint(또는 interface) 클래스 항목이 있는데 매니페스트가 해당 클래스를 **미선언**
(declaredTouchpoints/declaredInterfaces 공집합/생략)하면, 그 클래스 항목 전체가 제외된다. 이는
**고임팩트 이탈**이므로 조용한 자동 N/A 대신 `classExclusions.<class>` 확인을 요구한다.

| 조건 | 통과 조건 | 위반 시 |
|------|-----------|---------|
| 클래스 미선언 + 정책에 클래스 항목 존재 | `classExclusions.<class>` 에 `reason` 비공백 **AND** `confirmedBy` 존재 | 없거나 요건 미충족 → 차단(원칙 11 (c)·silentOmission 금지) |
| 클래스 선언(트리거) | per-item(produced/excluded) 검사 | 개별 항목 규칙 적용 |
| 정책에 클래스 항목 없음 | 무조건 통과 | — |

`classExclusions` 검사는 결정적 고정 순서(touchpoint→interface)로 수행된다.

### Contract 포인터 정합 규칙 (백로그 K)

**활성 조건.** `contract_dir`(체커 3번째 선택 인자 · 미지정 시 매니페스트 기준 파생
`<manifest 부모의 부모>/project-contract`, 즉 배치 규약상 `<workspace>/.claude/project-contract/`)에
`project-contract.v<N>.md` 형태 파일이 1건 이상 실재할 때 활성이다. 파일명 관례 정본 =
`planning/adapters/claude/contract-binding.md` §4.1(인스턴스 1건 = 파일 1개 · 현재 인스턴스 = 최고 `N`).
디렉터리 부재 또는 매칭 0건이면 이 검사는 비적용(오류 0건)이다 — Contract 계보가 없는 워크스페이스의
기존 거동을 그대로 둔다.

**검사 대상.** 매니페스트 `artifacts` 중 `status: produced` **AND** `path` 비공백 **AND** 그 경로의 파일
실재 **AND** 확장자 `.md` 인 항목. `path` → 실경로 해석은 위 `produced` 존재 검사와 동일한 식
(`절대경로면 그대로 · 아니면 매니페스트 디렉터리 기준 상대`)을 재사용한다. 대상 파일 본문에서 정규식
`project-contract\.v([0-9]+)\.md` 로 참조 버전을 수집해 그 **최고값**을 현재 인스턴스와 비교한다.

| 조건 | 판정 | 오류 문면 |
|------|------|-----------|
| `max(참조) == 현재 vN` | 통과 | — |
| `max(참조) < 현재 vN` | 오류 | 정본 포인터 낡음(stale) — superseded 인스턴스를 근거 정본으로 지목 |
| `max(참조) > 현재 vN` | 오류 | 정본 포인터 실재 부재(dangling) — 실재하지 않는 인스턴스 참조 |
| 참조 0건 | 비적용 | — |
| 확장자 `.md` 아님 | 비적용 | — |
| Contract 계보 부재(디렉터리 없음 / 매칭 0건) | 비적용 | — |
| 계보 디렉터리 실재 · 판독 실패 | 차단 | Contract 계보 판독 실패 — 포인터 정합 판정 불가(차단) |
| 산출물 본문 판독 실패 | 차단 | 산출물 판독 실패 — 포인터 정합 판정 불가 |

**비적용과 차단의 경계.** 정당한 부재(계보 디렉터리 없음·매칭 0건·참조 0건·비-md)는 비적용이다. 반면
판독 실패는 현재 인스턴스나 참조 집합이 **미확정**인 상태이며, 미확정을 통과로 처리하면 이 규칙이 막으려던
"실패 없이 조용히 틀림"을 그대로 재생산한다. 판정 불가는 통과가 아니라 차단이다(이진 상태 원칙 — 정책
파싱 실패를 오류로 표면화하는 이 체커의 기존 관례와 동형). 계보 판독이 실패하면 현재 인스턴스가 없으므로
포인터 검사를 중단하고 그 오류 1건만 낸다.

`max` 를 쓰는 이유: 문서가 계보 이력을 병기해 옛 버전을 함께 인용하는 것은 이력 보존상 정당하다. 판정 기준은
그 문서가 지목한 **최고** 인스턴스다.

**이탈 채널.** artifact 에 `"contractRefPinned": { "reason": "<비공백>", "confirmedBy": "<확인 주체>" }` 를
두면 해당 산출물의 포인터 검사를 스킵한다(원칙 11 (b) — 기본값 이탈 시 사유 기록). `reason`/`confirmedBy`
요건을 채우지 못한 핀은 핀이 아니다 — 요건 미충족 오류를 내고 포인터 정합 검사를 그대로 수행한다.

**경계 2건.**

- **포인터 존재 강제는 이 체커 소관 밖이다.** 산출물이 Contract 포인터를 아예 적지 않은 경우(참조 0건)는
  비적용으로 둔다. "Projection 산출물은 정본 포인터를 기재한다"는 요구의 소유는 04-solution-design spec 이다.
- **참조 문면의 시맨틱 진위는 게이트 몫이다.** 이 체커는 파일명 토큰(`project-contract.v<N>.md`)의 버전
  정합만 본다. 그 문서 내용이 실제로 해당 인스턴스와 정합하는지는 내용 판정이므로 CP2/사용자 게이트가 판정한다
  (`designElements` 의 `covered` 진위 경계와 동형).

uaf-verified: 위 규칙 표의 8행은 `design_completeness._check_contract_pointers` 와 `_current_contract_version` 의 분기(계보 판독 실패 조기 반환 · 계보 None 조기 반환 · status/path/존재/suffix 스킵 4종 · 산출물 판독 실패 · refs 공집합 스킵 · `==`/`<`/`>` 3분기)를 코드에서 1:1 대조해 열거함. 검색 범위 = 두 함수 본문.

### 매니페스트 부재

`design-manifest.json` 파일 자체가 없으면 게이트는 **즉시 차단**한다("design-manifest absent —
Solution Design에서 설계 산출 필요"). 이것이 설계 미완 프로젝트(예: SD projection 미실행)를 구현
편입 직전 막는 핵심이다.

## 예시 — 접점 3개·연계 있는 프로젝트(일부 produced·일부 정당화 제외)

```json
{
  "declaredTouchpoints": ["web-portal", "admin-console", "mobile-app"],
  "declaredInterfaces": ["payment-gateway"],
  "artifacts": [
    { "id": "project-plan",     "status": "produced", "path": "../../docs/project-plan.md" },
    { "id": "requirements-def", "status": "produced", "path": "../../docs/requirements.md" },
    { "id": "business-process", "status": "produced", "path": "../../docs/process.md" },
    { "id": "functional-spec",  "status": "produced", "path": "../../docs/functional-spec.md" },
    { "id": "table-def",        "status": "produced", "path": "../../docs/table-def.md" },
    { "id": "test-plan-cases",  "status": "produced", "path": "../../docs/test-plan.md" },
    { "id": "screen-list",      "status": "produced", "path": "../../docs/screen-list.md" },
    { "id": "menu-structure",   "status": "produced", "path": "../../docs/menu.md" },
    { "id": "screen-design",    "status": "excluded",
      "reason": "MVP 범위에서 상세 화면설계는 후속 스프린트로 이연(와이어프레임만 확정)",
      "confirmedBy": "user" },
    { "id": "interface-spec",   "status": "produced", "path": "../../docs/interface-spec.md" },
    { "id": "design-tokens",           "status": "produced", "path": "../../docs/design-tokens.md" },
    { "id": "screen-mock",             "status": "produced", "path": "../../mocks/index.html" },
    { "id": "mock-convergence-record", "status": "produced", "path": "../../docs/mock-convergence.md" }
  ],
  "designElements": {
    "project": {
      "design-tokens-values": { "status": "covered", "pointer": "docs/design-tokens.md#values" },
      "tone-and-manner":      { "status": "covered", "pointer": "docs/design-tokens.md#tone" },
      "accessibility-floor":  { "status": "covered", "pointer": "docs/design-tokens.md#a11y" }
    },
    "screens": {
      "home": {
        "layout-structure": { "status": "covered", "pointer": "mocks/home.html" },
        "navigation":       { "status": "covered", "pointer": "mocks/home.html#gnb" },
        "component-states":  { "status": "covered", "pointer": "docs/screen-design.md#home-states" },
        "data-rules":        { "status": "covered", "pointer": "docs/functional-spec.md#home" },
        "responsive":        { "status": "covered", "pointer": "docs/design-tokens.md#breakpoints" }
      }
    }
  }
}
```

이 예에서 always 6종 + touchpoint 6종(접점 선언 — 화면 3종 + Visual Contract 3종)이 required 이며 대부분
produced, `screen-design` 1종만 사용자 확인을 받아 정당화 제외되었다. interface 선언이 있으므로
`interface-spec` 도 required 이며 produced 다. 접점 선언으로 `designElements` 가 활성이므로 projectScope 3종 +
`home` 화면 × screenScope 5종이 모두 covered 다. 침묵 누락 0 → 게이트 통과(단, `covered` 진위·화면 목록
대응은 CP2/사용자 게이트 mock 리뷰가 판정한다).

## 예시 — 접점·연계 미선언 프로젝트(클래스 전체 제외 확인)

배치/파이프라인처럼 UI 접점·외부 연계가 없는 프로젝트는 touchpoint·interface 클래스를 미선언한다.
이때 두 클래스의 전체 제외를 `classExclusions` 로 표면화·확인해야 always 6종만으로 게이트를 통과한다.

```json
{
  "declaredTouchpoints": [],
  "declaredInterfaces": [],
  "classExclusions": {
    "touchpoint": { "reason": "UI 접점 없는 배치/데이터 파이프라인 — 화면 클래스 전체 제외", "confirmedBy": "user" },
    "interface":  { "reason": "외부 시스템 연계 없음 — 인터페이스 클래스 전체 제외", "confirmedBy": "user" }
  },
  "artifacts": [
    { "id": "project-plan",     "status": "produced", "path": "../../docs/project-plan.md" },
    { "id": "requirements-def", "status": "produced", "path": "../../docs/requirements.md" },
    { "id": "business-process", "status": "produced", "path": "../../docs/process.md" },
    { "id": "functional-spec",  "status": "produced", "path": "../../docs/functional-spec.md" },
    { "id": "table-def",        "status": "produced", "path": "../../docs/table-def.md" },
    { "id": "test-plan-cases",  "status": "produced", "path": "../../docs/test-plan.md" }
  ]
}
```

접점·연계 미선언이지만 두 클래스 드롭이 `classExclusions{reason,confirmedBy}` 로 확인되었고 always 6종이
전부 produced 이므로 게이트 통과다. `classExclusions` 가 없으면(조용한 제외) 체커가 차단한다.

## 예시 — 경량 프로파일(통합 설계 문서 1종) · `path` 실동작 예시 (절차 비례화 트랙 W1-b)

절차 비례화 트랙(`docs/proportionality-track-ledger.md` §4 W1-b)의 **경량 레인**은 필수 산출물이
**통합 설계 문서 1종**(`id: solution-design`·`requirement: always`)이다. 정책 파일 =
`uahf/framework/adapters/claude/solution-design-data/policy/lightweight-policy.yaml`, 값표 정본 =
`planning/adapters/claude/solution-design-binding.md` §7.2 (다) 경량 프로파일, 워크스페이스 시드 절차 =
같은 문서 §7A.2-S. 본문 경로 규약 정본 = 같은 문서 §7A.2.

**실동작 값은 두 단계를 올라가는 `../../docs/<id>.md` 다.**

```json
{
  "declaredTouchpoints": [],
  "declaredInterfaces": [],
  "artifacts": [
    { "id": "solution-design", "status": "produced", "path": "../../docs/solution-design.md" }
  ]
}
```

| 항목 | 값 | 근거 |
|---|---|---|
| 매니페스트 실경로 | `<workspace>/.claude/solution-design/design-manifest.json` | 이 문서 §배치 위치 |
| `manifest_dir` | `<workspace>/.claude/solution-design/` | `design_completeness.check_design_completeness` — `manifest_path.resolve().parent` |
| 본문 실경로 | `<workspace>/docs/solution-design.md` | binding §7A.2 배치 스코프 · 경량 레인 본문 경로 규약 |
| 실동작 `path` | `../../docs/solution-design.md` | 위 두 값의 상대차 2단 |
| 틀린 `path` | `docs/solution-design.md` | `<workspace>/.claude/solution-design/docs/solution-design.md` 로 해석 → 부재 오류 |
| `classExclusions` | 불요 | 경량 정책 `defaultRequiredSet` 에 `touchpoint`/`interface` 클래스 항목이 0이므로 클래스 전체 제외 규칙이 미발화(위 §클래스 전체 제외 규칙 표 3행 "정책에 클래스 항목 없음 → 무조건 통과") |

**소비 측 접합.** 이 `path` 가 해석되는 절대경로는 엔진 seed 프롬프트가 SD 입력으로 가정하는 경로
(`orchestration/adapters/claude/contract_to_graph.py` `_solution_design_path` = `<project_root>/docs/solution-design.md`,
`project_root` = `config.workspace_dir` = 소비 프로젝트 루트)와 **동일 파일을 지목한다**. 즉 경량 레인은
`contract_to_graph.py` 개정 없이 산출 측과 소비 측이 정합한다.

**남는 것(`path` 표기 정정의 범위 밖).**

- **표준 레인 발견 2(seed 단일파일 가정)는 여전히 미해소다** — `contract_to_graph.py` `_solution_design_path`
  가 SD 입력을 `<project_root>/docs/solution-design.md` 단일 파일로 가정하는 결함은 개별 Projection
  7~13종을 산출하는 표준 레인에서 그대로 남는다(경량 레인에서만 정합). 이 정정은 **매니페스트 `path` 표기**만
  고쳤고 seed 가정은 건드리지 않았다. 좌표 = `docs/proportionality-track-ledger.md` §6.3 항 1 ·
  `orchestration/adapters/claude/contract_to_graph.py` `_solution_design_path`.
- **`designElements` 의 `pointer` 값은 정정 대상이 아니다** — 체커는 `pointer` 의 파일 존재를 검사하지
  않는다(`design_completeness` 는 요소에 대해 **선언 완전성만** 판정하며 `covered` 진위는 CP2/사용자 게이트
  몫이다·위 §designElements 판정 규칙). 존재 검사 대상은 `artifacts[].status == produced` 의 `path` 뿐이다.

uaf-verified: 위 정정 범위 주장은 (1) 정정 후 이 문서에서 `"path":` 를 키로 하는 값 전건이
`../../` 접두를 갖는지 재판독, (2) `design_completeness.py` 의 `path` 존재 검사 지점(`produced` 분기의
`target = p if p.is_absolute() else (manifest_dir / path)`)과 `designElements` 판정 함수에 `pointer` 존재
검사 분기가 부재함을 코드에서 확인, (3) `contract_to_graph.py` `_solution_design_path` 의 단일 파일 가정이
무변경임을 diff hunk 0 으로 확인해 얻었다. 검색 범위 = 이 문서 본문 + 그 2개 python 파일이며, 소비
프로젝트가 이미 복사해 간 구표기 매니페스트의 소급 정정은 이 개정의 범위 밖이다(미해소).

uaf-verified: 위 표의 경로·해석식 주장은 (1) `design_completeness.py` 의 `manifest_dir = manifest_path.resolve().parent` 와 `target = p if p.is_absolute() else (manifest_dir / path)` 2지점 판독, (2) `contract_to_graph.py` `_solution_design_path` 및 `compile`→`build_seed_graph` 의 `project_root` 전달 경로 판독, (3) 임시 워크스페이스에 경량 정책·본문·매니페스트를 실제로 배치해 체커를 2회 실행한 실측(`path: ../../docs/solution-design.md` → `[DESIGN-COMPLETE]` exit 0 / `path: docs/solution-design.md` → `[DESIGN-INCOMPLETE]` exit 2 · 오류 문면 "path 부재: docs/solution-design.md"), (4) 두 경로 문자열의 `resolve()` 후 문자 단위 동일 대조(len 168 == 168 · True) 로 얻었다. 검색 범위 = 위 2개 python 파일 + 경량 policy 1파일 + 임시 워크스페이스 1건이며, 소비 프로젝트에서의 엔진 run 경유 실왕복과 표준 레인 예시 2종의 정정은 이 개정의 실측 범위 밖이다(미검증·미해소).
