# framework/plugins/plugin-manifest — Plugin Manifest·공통 Failure Report 포맷 인스턴스

작성일: 2026-07-06
상태: v0.8 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/10-plugins.md §3.2-A — Plugin Manifest(배포 서술자) 6필드 스키마(`id`/`version`/`provides`/`requires`/`dependsOn`/`frameworkCompat`)와 필수/선택 표기, 그리고 새 Config scope 미도입 주의(INV-7)의 정본. 본 문서 §2가 인스턴스화하는 계약. 필드명·의미·필수/선택 표기의 진위 판정 기준은 이 §가 유지한다.
- specs/10-plugins.md §3.2-B — 공통 Failure Report 4필드(`operation`/`target`/`reason`/`location`)와 `reason` 11종 열거의 정본, 그리고 01 §3.2-D 재사용·IsolationViolation 격리 사유 코드 주석의 정본. 본 문서 §3이 인스턴스화하는 계약.
- specs/10-plugins.md §3.3 INV-7 — Config scope 불변(Plugin은 새 Config scope를 도입하지 않는다; 포함 Module은 자신의 configSchema를 그대로 소유). 본 문서 §2가 보존·대조하는 불변. INV-8 — 자기완결성(의존은 `requires`·`dependsOn`으로만 선언). INV-9 — 안정 식별자. INV-1/3/4/5/6 — Failure Report `reason`이 위반 시 산출되는 격리·본체 불변(§3 소관 경계로 참조).
- specs/10-plugins.md §3.1 — 네 연산(Install/Activate/Deactivate/Remove)의 규칙. **이 파일 소관이 아니다** — 각 `reason`을 어느 연산이 언제 산출하는가(연산별 완료 조건과 실패 보고 결합)는 연산 규칙 인스턴스 문서(framework/plugins/plugin-lifecycle.md) 소관이다. 본 문서 §0·§3이 경계로 참조.
- specs/01-runtime.md §3.2-A — Module Manifest 7필드. Plugin Manifest `provides`의 각 항목이 참조하는 Module Manifest의 정본이자, Plugin Manifest(개별 배포 서술자)와 구분되는 Module Manifest(Provider 등록 서술자, framework/plugins/module-manifest.md)의 정본. 본 문서는 § 포인터로만 참조한다.
- specs/01-runtime.md §3.2-D — Runtime 공통 Failure Report. `ContractMismatch`/`UnresolvedContract`/`DuplicateId`가 이 정본의 사유 코드를 그대로 재사용함의 원천(10 §3.2-B 주석). 본 문서 §3이 § 포인터로 참조.
- specs/00-glossary.md §3.2-J(J-10) — Plugin·Plugin Manifest 용어 정본. §3.2-D — Plugins (Component). 본 문서는 새 용어를 신설하지 않는다.
- framework/core/structure.md §2 — 본 파일의 소속 경계(Module 구현 디렉터리 `framework/plugins/`). §5 — 금지 토큰 규칙(확정 조건 C-3 확장). §7 — Core Contract 불변 조건(C-1). 본 문서 본문 준수 대상.
- framework/workflow/work-graph.md — 포맷 인스턴스 **소유 문서 관례 표본**(정본 셀 보존·필수 표기 보존·Failure Report 포맷 인스턴스 소유 선언·reason↔연산 결합은 연산 규칙 인스턴스 문서로 이연·비소관 경계 서술·§0 정본 경계·§9 이력 절 머리 배치·말미 요약 절·자가 전수 스캔 기록 형식).
- AGENT.md — 상위 규약.

거버넌스: 이 문서는 `framework/plugins/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 특정 AI·언어·툴체인·직렬화 형식·물리 경로 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장, 10 §3.3 INV-10). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. Plugin Manifest 6필드(10 §3.2-A — `id`/`version`/`provides`/`requires`/`dependsOn`/`frameworkCompat`)·공통 Failure Report 4필드+`reason` 11종(10 §3.2-B)을 전건 § 포인터 인용으로 인스턴스화(필드명·의미·필수/선택 표기·`reason` 열거·순서 정본 그대로 보존, 재정의 0·새 필드 0·새 reason 0). Plugin Manifest의 새 Config scope 미도입 주의(INV-7)·`ContractMismatch`/`UnresolvedContract`/`DuplicateId`의 01 §3.2-D 재사용·`IsolationViolation` 격리 사유 코드 주석 보존. 이 문서가 두 포맷의 **인스턴스 소유 문서**임과 "각 reason을 어느 연산이 언제 산출하는가는 연산 규칙 인스턴스 문서(plugin-lifecycle.md) 소관"임을 선언. 개별 Plugin 배포 서술자(Plugin Manifest)와 Provider 등록 서술자(Module Manifest, module-manifest.md)의 구분 명시. 연산 규칙(10 §3.1) 비소관(포맷만 소유), 직렬화·물리 위치·배포 채널 비서술(Adapter Binding 소관 포인터). 10·01 계약 재정의·확장 0, 새 필드·새 reason 0, Glossary 밖 새 용어 0, 금지 토큰 0(자가 부류별 전수 스캔 — §4). | Worker (Advisor 위임, Task EX-P1) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/10-plugins.md §3.2다.** 이 문서는 그 Core Contract의 **인스턴스**이며, 계약을 재정의·확장하지 않는다. 계약 요소는 § 포인터로만 참조한다(framework/core/structure.md §7 C-1과 같은 인스턴스 원칙). 두 포맷의 필드·의미·필수/선택 표기·`reason` 열거의 **진위 판정 기준은 정본 10 §3.2-A/B가 유지한다.**
- 이 문서는 `framework/plugins/` 아래 **Plugin 배포 서술자 포맷**과 **공통 Failure Report 포맷**을 확정한다. 10 §3.2-A(Plugin Manifest)·§3.2-B(공통 Failure Report) 두 포맷을 이 경계 위에 배치·대조한다.
- **두 서술자의 구분(혼동 방지).** 이 문서가 소유하는 **Plugin Manifest**(10 §3.2-A 6필드)는 **개별 Plugin(하나 이상의 Module·확장 요소를 묶은 자기완결 배포 단위, Glossary §3.2-J J-10)의 배포 서술자**다. 이는 **Plugins Provider Module**(이 확장·배포 규격을 실현해 Runtime에 등록되는 Module)의 등록 서술자인 **Module Manifest**(01 §3.2-A 7필드 — framework/plugins/module-manifest.md 소관)와 **다른 서술자**다. Plugin Manifest는 배포되는 개별 단위를, Module Manifest는 그 배포를 관장하는 Provider Module을 서술한다. 필드 구성도 다르다(Plugin Manifest 6필드 vs Module Manifest 7필드).
- **Failure Report 포맷 인스턴스 소유 선언.** 이 문서가 공통 Failure Report 포맷(10 §3.2-B)의 **인스턴스 소유 문서**다. 각 연산(Install/Activate/Deactivate/Remove)의 규칙 인스턴스 문서(framework/plugins/plugin-lifecycle.md — 10 §3.1 연산 규칙의 인스턴스)는 실패 보고를 낼 때 이 포맷을 **§ 포인터로 참조**한다. 각 `reason` 코드를 어느 연산이 언제 산출하는가(연산별 완료 조건·실패 보고 결합)는 10 §3.1과 그 규칙 인스턴스 문서(plugin-lifecycle.md) 소관이며, 본 문서는 포맷의 `reason` 11종 열거만 소유·보존한다(상세 §3).
- **소관 밖 경계.** 분해·연산 규칙의 전개 — 네 연산(10 §3.1)의 입력·출력·완료 조건·실패 보고 결합 — 은 이 파일 소관이 아니다. **plugin-lifecycle.md(연산 규칙 인스턴스) 소관**이며, 본 문서는 그 결합을 추측·전개하지 않고 포맷만 소유한다.
- **재정의·확장 0 선언.** 두 포맷의 6필드·4필드·`reason` 11종은 10 §3.2-A/B의 인스턴스이며 § 포인터로만 참조한다. 스키마 표는 정본을 그대로 보존한다(재정의 0, 새 필드 0, 새 `reason` 0, 순서 정본 유지). 진위 판정 기준은 정본 10 §3.2-A/B가 유지한다. 위반(형태 B가 10 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다.
- **물리 실현 비서술(경계).** 두 포맷의 **물리 형식·직렬화·물리 위치·물리 경로·배포 채널**은 이 문서가 서술하지 않는다. 이는 **Adapter Binding 문서 소관**이다(10 §4.1·§4.2). 필요한 자리에는 "Adapter Binding 문서 소관" 포인터만 둔다(§4).
- **10 내부 § 포인터·INV 참조 표기 관례.** 10 정본 셀을 보존할 때, 10의 내부 § 포인터·INV 참조는 `10 §…`·`10 INV-…` 접두로 명시하여 본 문서 자신의 절 번호와 구분한다. 이는 셀의 대상 지시를 명료화하는 표기이며 셀 내용(필드명·의미·필수/선택 표기·`reason` 열거)을 변경하지 않는다(work-graph.md §0의 표기 관례와 동형).
- 용어는 specs/00-glossary.md 정본(§3.2-J J-10·§3.2-D)만 사용한다. 새 용어를 신설하지 않는다. "Plugin·Plugin Manifest"는 J-10 표제어, "Plugins (Component)"는 §3.2-D 표제어이며, "공통 Failure Report·`reason` 사유 코드"는 10 §3.2-B 정본이 정의한 포맷·필드 명칭이지 본 문서 신설 용어가 아니다.

---

## §1. 목적

`framework/plugins/`의 이 규격은 두 가지를 확정한다.

- **Plugin Manifest 포맷** — 개별 Plugin(자기완결 배포 단위)의 배포 서술자의 6필드와 각 필드의 필수 표기, 그리고 새 Config scope 미도입 주의(INV-7)(§2).
- **공통 Failure Report 포맷** — 모든 Plugins 연산(Install/Activate/Deactivate/Remove)의 공통 실패 보고 4필드와 `reason` 11종 사유 코드, 그리고 이 파일이 그 포맷의 인스턴스 소유 문서라는 선언(§3).

이 규격은 10 §3.2-A·§3.2-B Core Contract의 **인스턴스**다. 계약 요소(필드·필수 표기·`reason` 열거)를 재정의·확장하지 않는다. 형태 A(문서)에서 형태 B(실행 코드)로 전환되어도 10 §3 Core Contract 변경은 0이며, 위반(형태 B가 10 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다(structure.md §7 C-1과 같은 불변 원칙).

---

## §2. Plugin Manifest 포맷 인스턴스 (정본: 10 §3.2-A)

Plugin Manifest는 Plugin의 배포 서술자다. 개별 Plugin(하나 이상의 Module·확장 요소를 묶은 자기완결 배포 단위)이 무엇을 포함하고 무엇에 의존하며 어느 Framework 버전과 호환되는가를 담는다(10 §3.2-A). 필드는 01 §3.2-A Module Manifest와 정합을 유지한다(10 §3.2-A). 아래 필드·의미·필수 표기는 10 §3.2-A 정본을 **그대로 보존**한다(재정의 0, 새 필드 0, 순서 정본 유지). 필드명뿐 아니라 필수 속성 표기(예/아니오)와 그 괄호 단서까지 정본과 일치시킨다.

| 필드 | 의미 | 필수 |
|---|---|---|
| `id` | Plugin 고유 식별자. 안정적(stable)이어야 설치·제거·의존 해소의 기준이 된다. Module Manifest `id`와 동일한 안정성 규칙(01 INV-7). | 예 |
| `version` | Plugin 버전. | 예 |
| `provides` | 이 Plugin이 포함·배포하는 요소 목록. 최소 1건. 각 항목은 Module Manifest(01 §3.2-A) 1건, 또는 확장 요소(Hook/Skill 등) 참조다. 확장 요소의 상세 서술은 08/09 소관이며 여기서는 "포함 요소" 수준으로만 참조한다. | 예 |
| `requires` | 이 Plugin이 활성화되기 위해 Runtime에서 Resolve되어야 하는 contract id 목록. Module Manifest `requires`와 동일 의미(contract id 목록). | 아니오(기본 없음) |
| `dependsOn` | 의존하는 다른 Plugin id 목록. 해당 Plugin이 먼저 설치·활성화되어야 한다. | 아니오(기본 없음) |
| `frameworkCompat` | 호환 Framework 버전 범위. 이 범위 밖에서는 Install을 거부한다. | 예 |

**새 Config scope 미도입 주의(정본 보존 — 10 §3.2-A 주의, INV-7).** Plugin Manifest는 새로운 Config scope를 도입하지 않는다. 포함 Module의 Config 스키마(`configSchema`)는 각 Module Manifest가 그대로 소유하며, Config는 Global/Project/Module(01 §3.2-B)로 유지된다(10 INV-7). 이 주의의 정본은 10 §3.2-A 말미이며, 본 문서는 그 문면을 인스턴스로 보존할 뿐 Config 계약을 재정의하지 않는다.

- **필수 표기(정본 보존).** 6필드 중 4필드(`id`·`version`·`provides`·`frameworkCompat`)는 **예**, 2필드(`requires`·`dependsOn`)는 **아니오(기본 없음)**다. 필수/선택 표기와 그 괄호 단서를 정본 그대로 유지한다 — 표기 누락은 계약 변경으로 읽히므로 보존이 필수다.
- **개별 Plugin `requires`의 의미(구분).** 이 `requires`는 **개별 Plugin이 활성화되기 위해 Resolve되어야 하는 contract id 목록**이며(10 §3.2-A), Plugins Provider Module 자신의 `requires`(01 §3.2-A — module-manifest.md 소관, 그 값은 선언하지 않음)와는 다른 층위다. Activate 연산(10 §3.1)이 Resolve하는 대상은 이 Plugin Manifest의 `requires`이지 Provider Module의 것이 아니다.
- **`provides`의 확장 요소 경계.** `provides`의 각 항목이 Module Manifest(01 §3.2-A) 1건이거나 확장 요소(Hook/Skill) 참조라는 점은 정본대로 보존하되, **확장 요소의 등록 표면·이벤트·능력 계약 상세는 08/09 소관**이며 본 문서는 "포함 요소" 수준으로만 참조한다(10 §3.2-A, §2 예2 정합). 번들된 확장 요소의 등록 계약은 08 §3.1-C·09 §3.1-A가 소유하고 10은 배포·제거만 소유한다(10 §9 결정 기록).
- 필드의 상세 정본은 10 §3.2-A가 유지한다. 본 표는 그 스키마를 인스턴스화할 뿐 계약을 재정의하지 않는다.

---

## §3. 공통 Failure Report 포맷 인스턴스 (정본: 10 §3.2-B)

Failure Report는 모든 Plugins 연산의 공통 실패 보고 구조다(10 §3.2-B). 01 §3.2-D Failure Report와 필드 정합을 유지한다(10 §3.2-B). 아래 필드·의미는 10 §3.2-B 정본을 **그대로 보존**한다(재정의 0, 새 필드 0). 정본 표는 필수 열을 두지 않으므로 본 인스턴스도 두지 않는다(정본 구조 보존).

| 필드 | 의미 |
|---|---|
| `operation` | 실패한 연산 (Install / Activate / Deactivate / Remove). |
| `target` | 대상 (plugin id, module id, contract id). |
| `reason` | 사유 코드 (IncompatibleFramework / MissingDependency / DuplicateId / BodyMutation / NotSelfContained / ContractMismatch / UnresolvedContract / DeactivateIncomplete / ResidueDetected / DependentExists / IsolationViolation). |
| `location` | 실패 지점 참조 (Manifest 필드, module id, 침범 경계). |

**`reason` 열거 11종(정본 10 §3.2-B 그대로 보존).** 공통 Failure Report의 `reason`은 다음 11종 사유 코드다. 정본 열거를 그대로 보존한다(재정의 0, 추가 0, 순서 정본 유지):

1. `IncompatibleFramework`
2. `MissingDependency`
3. `DuplicateId`
4. `BodyMutation`
5. `NotSelfContained`
6. `ContractMismatch`
7. `UnresolvedContract`
8. `DeactivateIncomplete`
9. `ResidueDetected`
10. `DependentExists`
11. `IsolationViolation`

**재사용·격리 사유 코드 주석(정본 보존 — 10 §3.2-B).** `ContractMismatch`·`UnresolvedContract`·`DuplicateId`는 01 §3.2-D의 사유 코드를 **그대로 재사용**한다(10 §3.2-B). `IsolationViolation`은 10 §3.3 격리 불변(INV-4/5/6) 위반의 **공통 사유 코드**다(10 §3.2-B). 이 주석의 정본은 10 §3.2-B이며, 본 문서는 그 문면을 인스턴스로 보존할 뿐 사유 코드의 의미를 재정의하지 않는다.

**이 문서의 Failure Report 포맷 인스턴스 소유 선언.** 이 문서가 공통 Failure Report 포맷(10 §3.2-B)의 **인스턴스 소유 문서**다. 각 연산(Install/Activate/Deactivate/Remove)의 규칙 인스턴스 문서(framework/plugins/plugin-lifecycle.md — 10 §3.1 연산 규칙의 인스턴스)는 실패 보고를 낼 때 이 포맷을 **§ 포인터로 참조**한다. 각 `reason` 코드를 어느 연산이 언제 산출하는가(연산별 완료 조건과 실패 보고의 결합)는 **10 §3.1 연산 규칙과 그 규칙 인스턴스 문서(plugin-lifecycle.md) 소관**이며, 본 문서는 포맷의 `reason` 11종 열거만 소유·보존하고 그 결합 규칙을 전개하지 않는다(포맷만 소유). 필드의 상세 정본은 10 §3.2-B가 유지한다.

---

## §4. 경계와 비의존 (직렬화·물리 위치 · 재정의 0 · 07 R2 · 금지 토큰 · Glossary)

본 문서가 준수하는 경계를 한자리에 모은다. 검증 대조 지점이다.

**직렬화·물리 위치·배포 채널 경계 (Adapter Binding 소관 포인터):**

- 두 포맷(Plugin Manifest·공통 Failure Report)의 **직렬화 형식·물리 위치·물리 경로·배포 채널**은 이 문서가 **일절 확정하지 않는다.** Core Contract(10 §3.2)는 추상 스키마이며, 직렬화 형식(파일 형태·문법)과 물리 배포 채널은 Adapter Binding이 정한다(10 §3.2 도입, §4.1·§4.2).
- 두 포맷의 물리 실현은 전부 **Adapter Binding 문서 소관**이다(10 §4.1·§4.2 이식 교체 지점). 이식 시 §2~§3의 필드·필수 표기·`reason` 열거는 유지되고 물리 실현만 교체된다(10 §4.2). 필요한 자리에는 "Adapter Binding 문서 소관" 포인터만 둔다.

**재정의 0 · 인스턴스화 대상 경계:**

- **10·01 계약 재정의·확장 0.** §2~§3의 모든 필드·의미·필수/선택 표기·`reason` 열거는 10 §3.2-A/B의 인스턴스이며 § 포인터로만 참조한다. 스키마 표는 정본을 그대로 보존한다(재정의 0, 새 필드·새 사유 코드 0, 순서 정본 유지). `provides`가 참조하는 Module Manifest(01 §3.2-A)·`ContractMismatch` 등이 재사용하는 01 §3.2-D 사유 코드도 재정의하지 않고 § 포인터로만 참조한다. 진위 판정 기준은 정본 10 §3.2-A/B가 유지한다. 위반이 발견되면 구현하지 않고 Advisor에게 보고한다.
- **인스턴스화 대상 경계.** 본 문서의 인스턴스화 대상은 두 데이터 포맷(10 §3.2-A Plugin Manifest·§3.2-B 공통 Failure Report)과 그에 부속된 주의 문면(새 Config scope 미도입 — 10 §3.2-A 주의·INV-7, 01 §3.2-D 재사용·IsolationViolation 격리 사유 코드 — 10 §3.2-B)이다.
- **연산 규칙(10 §3.1) 비소관.** 네 연산 규칙의 전개(연산별 입력·출력·완료 조건·실패 보고 결합)는 이 파일 소관이 아니다 — **포맷만 소유한다.** 연산 규칙 인스턴스 문서(plugin-lifecycle.md)가 본 Failure Report 포맷·Plugin Manifest 필드를 § 포인터로 참조하고, 각 `reason`↔연산 결합을 소유한다(§3).
- **두 서술자 구분.** Plugin Manifest(개별 배포 단위 서술자, 본 문서)와 Module Manifest(Plugins Provider Module 등록 서술자, module-manifest.md)는 서로 다른 서술자다. 본 문서는 Provider Module의 Module Manifest를 재정의하지 않으며, 그 필드는 module-manifest.md·01 §3.2-A 소관이다(§0·§2).

**동시·후속 작성 경계 (07 R2·INV-4):**

- 같은 병렬 집합(v0.8 PS-1)에서 후속·동시 작성 중인 형제 산출물(Adapter Binding 바인딩 문서·시연 절차서 등)의 미완성 내용은 인용·추측하지 않는다. 확정된 정본(10·01 spec·structure.md·Glossary)과 기존 Baseline 문서만 참조한다(07 R2·INV-4). 함께 작성되는 형제 산출물 중 연산 규칙 결합을 소유하는 plugin-lifecycle.md는 "각 reason을 어느 연산이 산출하는가는 그 문서 소관" 수준의 소관 지시로만 참조하고, 그 내부 전개 내용을 인용하지 않는다. 직렬화·물리 위치·배포 채널은 "Adapter Binding 문서 소관(10 §4.1·§4.2)" 수준의 일반 포인터로만 지시한다.

**금지 토큰 비의존(structure.md §5 C-3 확장, 10 INV-10):**

- 본 문서 본문에는 특정 AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로·확장자·배포 채널명 토큰을 두지 않는다. 금지 토큰의 예시조차 본문에 나열하지 않는다 — 구체 인스턴스가 필요한 자리에는 "Adapter Binding 문서 소관(10 §4.1·§4.2)" 포인터만 둔다(mention/use 경계).
- 다음은 금지 토큰이 아니다: **(i)** Failure Report 필드 값의 열거 명칭 — `operation` 값(Install / Activate / Deactivate / Remove) 및 `reason` 11종(IncompatibleFramework 등) — 10 §3.2-B 정본의 평이한 열거 값; **(ii)** Glossary·AGENT.md 정본 어휘 — Plugin·Plugin Manifest(Glossary §3.2-J J-10)·Plugins(§3.2-D)·Module·Module Manifest·Register/Resolve/Deregister와 역할 명칭(Advisor / Planner / Worker / Verifier); **(iii)** 계약 필드명 백틱 표기(`id`·`version`·`provides`·`requires`·`dependsOn`·`frameworkCompat`·`operation`·`target`·`reason`·`location`·`configSchema` — 10 §3.2·01 §3.2 정본 어휘); **(iv)** 저장소 문서 식별자(`specs/…`·`framework/…` 상호 참조 및 본 문서 자신의 식별자 `framework/plugins/plugin-manifest.md`) — 문서 식별자이며 직렬화 형식·물리 경로 토큰이 아니다(structure.md §5·work-graph.md §5 분류 선례 동형).
- **자가 부류별 전수 스캔.** 위 후보 부류 전체(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로·확장자·배포 채널명·특정 Adapter Binding 문서명)로 본문을 **부류별 전수 대조**하여 실증 0건임을 확인했다(단일 토큰 검색 하나로 넓은 결론을 내지 않고, 후보 부류별 전수 대조). 직렬화 형식·물리 위치·배포 채널이 필요한 자리는 전부 "Adapter Binding 문서 소관(10 §4.1·§4.2)" 포인터로 대체했다.

**Glossary 정본:**

- 사용 용어는 전부 specs/00-glossary.md §3.2-J(J-10: Plugin·Plugin Manifest)·§3.2-D(Plugins) 정본 또는 Glossary 기존 어휘다. 새 용어를 신설하지 않는다. "공통 Failure Report·`reason` 사유 코드" 등은 10 §3.2-B 정본이 정의한 포맷·필드·서술 명칭이며 본 문서 신설 용어가 아니다.

---

## §5. 요약 (규격 한눈에 보기)

- **Plugin Manifest(§2)** — 6필드(`id`/`version`/`provides`/`requires`/`dependsOn`/`frameworkCompat`). 10 §3.2-A 스키마 인스턴스, 필수 표기(4 예·2 아니오 — `requires`·`dependsOn`이 아니오, 괄호 단서 보존) 정본 보존. 새 Config scope 미도입 주의(10 §3.2-A·INV-7) 보존. 개별 Plugin 배포 서술자이며 Provider 등록 서술자(Module Manifest, module-manifest.md)와 구분.
- **공통 Failure Report(§3)** — 4필드(`operation`/`target`/`reason`/`location`), `reason` 11종. 10 §3.2-B 인스턴스(정본 필수 열 부재 구조 보존, 순서 정본 유지). `ContractMismatch`/`UnresolvedContract`/`DuplicateId`의 01 §3.2-D 재사용·`IsolationViolation` 격리(INV-4/5/6) 사유 코드 주석 보존. 이 문서가 포맷 인스턴스 소유 문서 — 연산 규칙 인스턴스 문서(plugin-lifecycle.md, 10 §3.1 소관)가 § 포인터로 참조. `reason`↔연산 결합 규칙은 plugin-lifecycle.md 소관(포맷만 소유).
- **경계(§4)** — 직렬화 형식·물리 위치·물리 경로·배포 채널 비서술(Adapter Binding 소관, 10 §4.1·§4.2). 연산 규칙(10 §3.1) 비소관(포맷만 소유). 10·01 재정의 0, 07 R2 경계, 금지 토큰 0(자가 부류별 전수 스캔), Glossary §3.2-J J-10·§3.2-D 정본만 사용.
- 모든 스키마는 10 §3.2의 인스턴스이며, 물리 실현은 Adapter Binding 소관이다. 형태 A(문서) → 형태 B(실행 코드) 전환에도 Core Contract 변경은 0이다.
