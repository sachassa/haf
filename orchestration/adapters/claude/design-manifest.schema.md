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
  // 미선언(빈 배열/생략)이면 touchpoint 항목은 자동 N/A(스킵).
  "declaredTouchpoints": [ "<접점 식별자>", ... ],

  // 외부 연계 선언. 비공집합이면 requirementClasses.interface 항목이 required 가 된다.
  // 미연계(빈 배열/생략)이면 interface 항목은 자동 N/A(스킵).
  "declaredInterfaces": [ "<연계 식별자>", ... ],

  // 필수 산출물별 상태. id 는 정책 projectionSelection.defaultRequiredSet[].id 와 대응한다.
  "artifacts": [
    {
      "id": "<defaultRequiredSet 의 id>",   // 필수·비공백 문자열. 중복 금지.
      "status": "produced" | "excluded",     // 필수.
      "path": "<산출물 경로>",               // status=produced 시 선택. 주어지면 존재 검사(매니페스트 기준 상대/절대).
      "reason": "<제외 사유>",               // status=excluded 시 필수·비공백.
      "confirmedBy": "<확인 주체>"           // status=excluded 시 필수(정당화 제외의 사용자 확인 기록).
    }
  ]
}
```

### status 판정 규칙 (체커)

| status     | 통과 조건                                             | 위반 시                          |
|------------|-------------------------------------------------------|----------------------------------|
| `produced` | (path 미지정) 무조건 통과 · (path 지정) 파일 존재     | path 지정인데 부재 → 오류        |
| `excluded` | `reason` 비공백 **AND** `confirmedBy` 존재            | 둘 중 하나라도 결여 → 요건 미충족 오류 |
| (부재)     | —                                                     | 침묵 누락 오류(silentOmission 금지) |
| (기타 값)  | —                                                     | 침묵 누락 오류                    |

required 아님(touchpoint/interface 클래스인데 미선언)인 항목은 매니페스트에 없어도 자동 N/A·통과다.

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
    { "id": "project-plan",     "status": "produced", "path": "docs/project-plan.md" },
    { "id": "requirements-def", "status": "produced", "path": "docs/requirements.md" },
    { "id": "business-process", "status": "produced", "path": "docs/process.md" },
    { "id": "functional-spec",  "status": "produced", "path": "docs/functional-spec.md" },
    { "id": "table-def",        "status": "produced", "path": "docs/table-def.md" },
    { "id": "test-plan-cases",  "status": "produced", "path": "docs/test-plan.md" },
    { "id": "screen-list",      "status": "produced", "path": "docs/screen-list.md" },
    { "id": "menu-structure",   "status": "produced", "path": "docs/menu.md" },
    { "id": "screen-design",    "status": "excluded",
      "reason": "MVP 범위에서 상세 화면설계는 후속 스프린트로 이연(와이어프레임만 확정)",
      "confirmedBy": "user" },
    { "id": "interface-spec",   "status": "produced", "path": "docs/interface-spec.md" }
  ]
}
```

이 예에서 always 6종 + touchpoint 3종(접점 선언)이 required 이며 대부분 produced, `screen-design`
1종만 사용자 확인을 받아 정당화 제외되었다. interface 선언이 있으므로 `interface-spec` 도 required 이며
produced 다. 침묵 누락 0 → 게이트 통과.
