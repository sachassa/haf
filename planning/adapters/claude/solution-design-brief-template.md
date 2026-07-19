# Solution Design 역할 위임 브리프 — 템플릿 (form-A 데이터 문서)

상태: v1.4 정합 (§DC-1 Wave 5-B)
상위 규약: `planning/adapters/claude/solution-design-binding.md` §6(역할 호스팅)·§7A(산출물 생산 프로토콜)·§7A.5(form-B 배선)
성격: **데이터 문서(양식)** — 실행 코드가 아니다. 주 세션(Advisor)이 `Proposing`(04 §3.4-A)에서 각 역할 서브에이전트를 **form-A로 소환**할 때 발부하는 지시서 양식이다.

---

## 이 문서의 위치

이 템플릿은 `solution_design_resolve.py`(form-B 로더·§7A.5) 출력을 주 세션이 손으로 채워 역할별 위임 브리프를 만드는 **양식**이다. 로더는 계산·방출까지만 하고 **소환하지 않는다** — 실제 위임(서브에이전트 소환)은 주 세션이 이 양식으로 수행한다(binding §6.1 "기존 위임 관행 재사용"·실행 호스팅 미설계 04 §3.9). 이 문서는 **구체 산출물 내용 스펙(유형별 필수 항목 카탈로그)을 담지 않는다** — 그것은 비정본 부록(expert-role-catalog.md §3.5) 소관이며(SP-INV 5), 이 양식은 역할·소유·배치·형식·컨택스트 위생까지만 정한다.

---

## 브리프 양식 (플레이스홀더를 주 세션이 채운다)

> **역할 (Role): {ROLE}**
>
> 너는 Solution Design 성숙 run의 `{ROLE}` 역할을 수행하는 fresh-context 위임 서브에이전트다. 아래 **자기 소유 산출물만** 작성한다.
>
> ### 소유 산출물 (Owned Artifacts)
> {OWNED_ARTIFACTS}
> *(로더 `artifactPlan` 에서 `owner == {ROLE}` 인 항목의 `id`·`name` 목록)*
>
> ### 출력 경로 (Output Paths)
> {OUTPUT_PATHS}
> *(각 소유 산출물 본문 = `<workspace>/docs/<id>.md` · 단일 Markdown 문서 — 같은 내용을 다른 형식으로 중복 저장하지 않는다·binding §7A.2)*
>
> ### 컨택스트 위생 규칙 (binding §7A.1)
> - **자기 소유 산출물만 작성한다.** 다른 역할 소유 산출물을 작성·수정하지 않는다.
> - **주 세션 컨택스트를 오염시키지 않는다.** 산출물 본문은 이 서브에이전트 컨택스트에서 작성하고, 주 세션에는 완료 보고(산출물 경로·상태)만 반환한다. 본문 전문을 주 세션으로 되돌리지 않는다.
> - **자기 소유 범위 밖은 추측하지 않는다.** 다른 역할·상위 설계 결정에 의존하는 불확실은 완료 보고의 open_questions로 에스컬레이션한다(추측 금지).
>
> ### 출력 형식 (binding §7A.2)
> - **본문:** 각 소유 산출물을 `<workspace>/docs/<id>.md` 에 사람+AI 겸용 단일 Markdown 문서로 작성한다.
> - **기계 색인:** `<workspace>/.claude/solution-design/design-manifest.json` 의 해당 `artifacts[].id` 항목 `status` 를 작성 완료 시 `pending`→`produced` 로 갱신한다(정당화 제외 시 `excluded` + `reason` + `confirmedBy`). `id` 는 `defaultRequiredSet[].id` 와 대응한다.
> - **구조화 사이드카(예: `table-def` 의 `schema.json`)는 다운스트림 코드생성이 실제 소비할 때에만** 산출한다 — 무조건 산출하지 않는다(불필요 산출 방지·Markdown 본문이 1차 정본).
>
> ### CP1 자체점검 (binding §7A.3)
> 산출 종료 시 자기 소유 산출물의 done 항목 충족 여부를 항목별로 점검하고, 각 점검의 검사 범위(scope)를 정직하게 명시한다. **자체 점검은 최종 승인이 아니다** — CP2(커버리지 역할 + `design_completeness` 결정적 체커)·CP3(Advisor)·Validating 사용자 게이트가 뒤따른다.
>
> ### 완료 보고 (주 세션 반환)
> - artifacts: 작성한 소유 산출물 경로 목록.
> - manifest_update: 갱신한 `design-manifest.json` artifact id·status.
> - self_check(CP1): done 항목별 충족 여부 + 검사 범위.
> - open_questions: 불확실·상위 의존 사항(없으면 "없음").

---

## 로더 출력 → 플레이스홀더 매핑

form-B 로더(`solution_design_resolve.py`·§7A.5) 출력이 이 양식의 어느 플레이스홀더를 채우는지 명시한다.

| 플레이스홀더 | 채우는 로더 출력 | 산출 방법 |
|---|---|---|
| `{ROLE}` | `roleComposition.roles[]` 의 각 역할 | `roles` 목록의 각 역할마다 브리프 1건 발부 |
| `{OWNED_ARTIFACTS}` | `artifactPlan[]` 중 `owner == {ROLE}` 이고 `required == true` 인 항목의 `id`·`name` | 역할별 필터·목록화 |
| `{OUTPUT_PATHS}` | 위 소유 산출물 각 `id` | `<workspace>/docs/<id>.md` 로 전개 |

- **활성/제외 역할.** `roleComposition.activatedConditional`(활성·근거 `by`)만 브리프를 발부한다. `excludedConditional`(제외·근거 `reason`)은 발부하지 않으며, 그 이탈은 `deviationRule`에 따라 성숙 run 기록에 사유로 남기고 Validating 게이트에서 표면화한다(binding §7.2 (나)·§7A.4).
- **required=false 산출물.** `artifactPlan[]` 중 `required == false` 인 항목(접점/연계 미선언 클래스)은 브리프에 포함하지 않으며, `manifestScaffold.classExclusions.<class>{reason,confirmedBy}` 를 사용자 확인으로 채워 표면화한다(binding §7A.4 (iii)·`design_completeness` 체커 차단 근거).
- **owner 정본.** 소유 역할 매핑의 정본은 Policy `artifactOwnership` 이다(binding §7.2 (나)·(라)). 이 양식은 로더가 그 매핑을 읽어 방출한 `artifactPlan[].owner` 를 소비할 뿐, 소유 관계를 재정의하지 않는다.
