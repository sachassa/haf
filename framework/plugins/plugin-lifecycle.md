# framework/plugins/plugin-lifecycle — Plugin 수명주기 4연산 규칙 인스턴스

작성일: 2026-07-06
상태: v0.8 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/10-plugins.md §3.1 — Install/Activate/Deactivate/Remove 네 연산의 정본(각 연산의 입력·출력·완료 조건·실패 reason 전건). 본 문서가 인스턴스화하는 연산 계약이다. 입력·출력·완료 조건·실패 reason의 진위 판정 기준은 이 §가 유지한다.
- specs/10-plugins.md §3.1 주의 — 개별 Module의 등록 해제(Deregister)가 Plugin 제거의 전제이며, Deactivate/Remove가 요구하는 이 연산의 소유·정합이 §9 조율 항목이었음. 본 문서 §4가 Deregister 기반 성립을 § 포인터로 명시하는 근거.
- specs/10-plugins.md §3.3 INV-1(본체 불가침)·INV-2(Register/Resolve 경유)·INV-3(잔여물 0)·INV-4/5/6(격리 불변)·INV-8(자기완결성) — 완료 조건 검사가 준수·대조하는 불변. 본 문서 §3이 예/아니오 검사 규칙으로 전개한다(재정의 0).
- specs/10-plugins.md §3.2-B — 공통 Failure Report 4필드·`reason` 11종 열거의 정본. 본 문서는 그중 각 연산의 reason만 완료 조건에 결합하며, 포맷 자체는 framework/plugins/plugin-manifest.md §3을 § 포인터로 소비한다(재게재·재정의 0).
- specs/10-plugins.md §6 — 실패 모드 표(각 실패 시나리오↔대응↔reason). 본 문서 §3 검사 실패 처리의 대조 지점이며, `NotSelfContained`(INV-8)·`IsolationViolation`(INV-4/5/6)의 산출 근거.
- specs/01-runtime.md §3.1-A — Register/Resolve/Replace/**Deregister** 연산. Activate가 소비하는 Register/Resolve, Deactivate/Remove가 소비하는 Deregister의 정본. Register 실패 사유(`ContractMismatch`|`DuplicateId`)·Resolve 실패 사유(`UnresolvedContract` 등)·Deregister 완료 조건의 원천.
- specs/01-runtime.md §9 결정 기록 — §3.1-A에 Deregister 연산 추가(Registry 수명주기는 Runtime 소유이므로 Plugins가 우회 정의하지 않고 01이 소유). Deactivate/Remove가 이 연산 위에서 성립함의 원문. specs/10-plugins.md §9 결정 기록 — 01 Deregister 조율 해소 승인.
- specs/01-runtime.md §4 — Adapter Binding(구체 직렬화·bundle 배치·배포 채널·물리 실행 소관). 본 문서 §3·§6이 § 포인터로만 참조.
- framework/plugins/plugin-manifest.md §2·§3 — **함께 확정되는 포맷 인스턴스 소유 문서**. Plugin Manifest 6필드(§2)·공통 Failure Report 4필드+`reason` 11종(§3) 포맷의 인스턴스 소유 문서다. 본 문서가 검사 규칙에서 참조하는 필드·reason 열거의 **소비 인터페이스**이며, 필드 표는 § 포인터로만 소비한다(정본은 10 §3.2-A/B가 유지, 재게재 0 — 이중 갱신 방지).
- framework/plugins/module-manifest.md — Plugins Provider Module의 등록 서술자. 네 연산을 노출하는 Provider의 `entrypoint`(추상 참조)·`contract`(`PluginsInterface`) 소유 문서. 본 문서는 그 연산을 규칙으로 전개하되 Provider Manifest를 재정의하지 않는다.
- framework/workflow/decompose-rules.md §2·§3 — 연산 규칙 인스턴스 관례 표본(연산 인터페이스 인스턴스 표·완료 조건→예/아니오 검사→reason 1:1 결합표·검사 범위 정직·포맷은 § 포인터로만 소비·물리 실행 경계 서술·§0 정본 경계·§9 이력 절 머리 배치·말미 요약 절).
- framework/core/structure.md §2·§5·§7 — 본 파일의 소속 경계(Module 구현 디렉터리 `framework/plugins/`), 금지 토큰 규칙(C-3 확장), Core Contract 불변 조건(C-1).
- specs/00-glossary.md §3.2-J(J-10)·§3.2-D — Plugin·Plugin Manifest·Plugins 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- AGENT.md — 상위 규약.

거버넌스: 이 문서는 `framework/plugins/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 특정 AI·언어·툴체인·직렬화 형식·물리 경로 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장, 10 §3.3 INV-10). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. Install/Activate/Deactivate/Remove 네 연산(10 §3.1)의 입력·출력·완료 조건·실패 reason을 인터페이스 인스턴스로 정본 그대로 보존(§2, 재정의·확장 0). 각 연산 완료 조건을 예/아니오 판정 가능한 검사 규칙으로 전개하고 검사 실패↔reason 1:1 결합(§3 — Install I1~I5(본체 수정 0→`BodyMutation`·frameworkCompat 포함→`IncompatibleFramework`·dependsOn 기설치→`MissingDependency`·id 유일→`DuplicateId`·자기완결→`NotSelfContained`)·Activate A1~A2(provides Register→`ContractMismatch`\|`DuplicateId`·requires Resolve→`UnresolvedContract`)·Deactivate D1(비활성화·바인딩 해제 완결→`DeactivateIncomplete`)·Remove R1~R2(잔여물 0→`ResidueDetected`·dependent 부재→`DependentExists`), 격리 가드→`IsolationViolation`, decompose-rules §3 관례 동형 — 각 검사 예/아니오 절차·검사 범위 정직). Deactivate/Remove가 01 §3.1-A Deregister(10·01 §9 결정 기록으로 추가 승인) 위에서 성립함을 § 포인터로 명시(§4). Plugin Manifest 6필드·공통 Failure Report 포맷은 plugin-manifest.md §2·§3을 § 포인터로만 소비(필드 표 재게재·재정의 0, 이중 갱신 방지 — §5). 물리 실현(bundle 배치·배선·배포 채널·물리 실행)은 Adapter Binding 소관 포인터. 10·01 계약 재정의 0, Glossary 밖 새 용어 0, 금지 토큰 0(자가 부류별 전수 스캔 — §6). | Worker (Advisor 위임, Task EX-P1) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/10-plugins.md §3.1이다.** 이 문서는 그 네 연산(Install/Activate/Deactivate/Remove) 계약의 **인스턴스**이며, 연산·완료 조건·실패 reason을 재정의·확장하지 않는다. 계약 요소는 10 §3.1을 § 포인터로 참조한다(framework/core/structure.md §7 확정 조건 C-1 정합 — 인스턴스는 계약 변경이 아니다; decompose-rules.md §0과 동형). 진위 판정 기준은 정본 10 §3.1이 유지한다.
- 이 문서는 `framework/plugins/` 아래 **네 연산의 규칙(운용 절차)**을 확정한다. 10 §3.1 각 연산의 완료 조건을 이 프로젝트의 **예/아니오 판정 가능한 검사 규칙**으로 전개하되, 각 검사의 진위 판정 기준은 대응 정본 10 §(그리고 그 검사가 대조하는 포맷 필드의 정본 10 §3.2-A/B)가 유지한다(decompose-rules.md §2 관례 동형).
- **소비하는 포맷의 소비 인터페이스는 framework/plugins/plugin-manifest.md이다.** 검사 규칙이 참조하는 Plugin Manifest 6필드·공통 Failure Report 4필드와 `reason` 11종 열거는 그 문서 §2·§3의 스키마를 **§ 포인터로만 소비**한다. 필드 표를 재게재·중복 정의하지 않는다(이중 갱신 방지 — plugin-manifest.md §3 인스턴스 소유 경계 관례 동형). 포맷 필드·reason 열거의 진위 판정 기준은 정본 10 §3.2-A/B가, 그 인스턴스 소유는 plugin-manifest.md가 유지한다.
- **reason↔연산 결합의 소관이 본 문서다.** plugin-manifest.md §3은 "각 `reason` 코드를 어느 연산이 언제 산출하는가(연산별 완료 조건과 실패 보고의 결합)는 10 §3.1과 그 규칙 인스턴스 문서 소관"이라 명시하고 포맷의 reason 열거만 소유한다. 본 문서가 바로 **네 연산에 대한 그 규칙 인스턴스 문서**이며, 각 reason이 어느 연산의 어느 완료 조건 검사에서 언제 산출되는가만 결합·소유한다. reason 열거의 소유·포맷은 plugin-manifest.md §3이 유지한다(본 문서는 reason을 값으로 인용할 뿐 새 코드를 신설하지 않는다).
- **Deregister 기반 성립.** Deactivate의 contract 바인딩 해제와 Remove의 등록 Module 제거는 01 §3.1-A **Deregister** 연산 위에서 성립한다(10 §3.1 주의, 10·01 §9 결정 기록으로 추가 승인). Registry 수명주기는 Runtime 소유이므로 Plugins는 이 연산을 우회 정의하지 않고 01의 Deregister를 소비한다. 상세는 §4.
- **소관 밖 경계.** 개별 Plugin Manifest·공통 Failure Report의 **포맷 정의**(필드 표·reason 열거)는 이 파일 소관이 아니다 — plugin-manifest.md §2·§3 소관이며 본 문서는 § 포인터로만 소비한다(재게재 0). Plugins Provider Module의 등록 서술자(Module Manifest 7필드)는 module-manifest.md 소관이며 본 문서는 재정의하지 않는다.
- **물리 실현 비서술(경계).** 네 연산을 **수행하는 주체의 물리 채널**, Plugin bundle의 **직렬화·물리 위치·배치·배포 채널**, 검사 규칙의 **물리 실행 방식**, 포함 확장 요소의 **등록 표면 바인딩**은 이 문서가 서술하지 않는다. 이는 **Adapter Binding 문서 소관**이다(01 §4, 10 §4.1·§4.2; 확장 요소 표면은 08·09 §4 소관). 필요한 자리에는 "Adapter Binding 문서 소관" 포인터만 둔다.
- **10 내부 § 포인터·INV 참조 표기 관례.** 10 정본 요소를 가리킬 때 10의 내부 § 포인터·INV 참조는 `10 §…`·`10 INV-…` 접두로, 01 요소는 `01 §…`·`01 INV-…` 접두로 명시하여 본 문서 자신의 절 번호와 구분한다. 이는 대상 지시를 명료화하는 표기이며 정본 내용(완료 조건·reason·필드)을 변경하지 않는다(decompose-rules.md §0의 표기 관례와 동형).
- 용어는 specs/00-glossary.md 정본(§3.2-J J-10·§3.2-D)만 사용한다. 새 용어를 신설하지 않는다. "Plugin·Plugin Manifest"는 J-10 표제어, "Plugins"는 §3.2-D 표제어이며, "Install·Activate·Deactivate·Remove·공통 Failure Report·reason 사유 코드"는 10 §3 정본이 정의한 연산·포맷·필드 명칭이지 본 문서 신설 용어가 아니다. 검사 라벨 I1~I5·A1~A2·D1·R1~R2·IG는 본 문서 서술 편의의 명명 규칙이며 계약 용어가 아니다.

---

## §1. 목적

`framework/plugins/`의 이 규격은 **네 연산(Install/Activate/Deactivate/Remove, 10 §3.1)을 어떤 규칙으로 판정하는가**를 확정한다.

이 규격의 책임은 세 가지다.

- **연산 인터페이스 인스턴스** — 네 연산의 입력·출력·완료 조건·실패 reason을 10 §3.1 정본과 일치하게 옮긴 인스턴스로 전개한다(§2).
- **완료 조건 검사 규칙** — 각 연산의 완료 조건을 **예/아니오로 판정 가능한 검사 규칙**으로 전개하고, 각 검사 실패를 해당 실패 reason 코드에 1:1 결합한다(§3, decompose-rules §3 관례 동형).
- **Deregister 기반 성립 명시** — Deactivate/Remove가 01 §3.1-A Deregister 위에서 성립함을 § 포인터로 명시한다(§4).

이 규격은 10 §3.1 네 연산 계약의 **인스턴스**다. 연산·완료 조건·실패 reason을 재정의·확장하지 않는다. 형태 A(문서)에서 형태 B(실행 코드)로 전환되어도 10 §3 Core Contract 변경은 0이며, 위반(형태 B가 10·01 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다(structure.md §7 C-1과 같은 불변 원칙).

이 규격의 규칙은 10 §7 완료 기준·§8 예1이 실증하는 수명주기와 동형이다 — 레퍼런스 Plugin 1개를 Install·Activate하여 새 기능(contract 바인딩)이 동작하고, Remove 후 잔여물 0으로 본체가 설치 이전과 동일함을 보이는 시연이 아래 검사 규칙(본체 수정 0·frameworkCompat 포함·Register/Resolve 경유·잔여물 0)을 실제로 밟는다. 본 문서는 그 사례를 재정의하지 않고 규칙의 실증 근거로만 가리킨다.

---

## §2. 네 연산 인터페이스 인스턴스 (정본: 10 §3.1)

아래는 네 연산의 입력·출력·완료 조건·실패 reason을 10 §3.1 정본과 일치하게 옮긴 인스턴스이며, 진위 판정 기준은 10 §3.1이 유지한다(§0). 본 절은 계약을 재정의하지 않는다. 실패 reason의 공통 Failure Report 포맷(4필드·reason 11종 열거)의 정본은 10 §3.2-B이며 소비 인터페이스 인스턴스는 plugin-manifest.md §3이다 — 본 문서는 § 포인터로만 소비한다(§5).

| 연산 | 입력 (정본: 10 §3.1) | 출력 (정본: 10 §3.1) | 완료 조건 (정본: 10 §3.1) | 실패 reason (정본: 10 §3.1) |
|---|---|---|---|---|
| **Install** | self-contained Plugin bundle 1건 + Plugin Manifest(10 §3.2-A). | 설치 결과 — 설치된 plugin id. 상태는 registered-but-inactive. | (1) 본체 수정 0건 (10 INV-1). (2) Manifest의 `frameworkCompat`가 현재 Framework 버전을 포함한다. (3) `dependsOn` Plugin이 모두 이미 설치되어 있다. (4) `id`가 유일하다. | `IncompatibleFramework` \| `MissingDependency` \| `DuplicateId` \| `BodyMutation` \| `NotSelfContained`. |
| **Activate** | 설치된 plugin id. | 활성화 결과 — 등록된 module id 목록. | `provides`의 각 Module Manifest가 Runtime Register(01 §3.1-A)로 등록되고, `requires` contract가 모두 Resolve(01)된다. 활성화는 Register/Resolve 계약으로만 성립한다 (10 INV-2). | `ContractMismatch` \| `UnresolvedContract` \| `DuplicateId`. |
| **Deactivate** | 활성 plugin id. | 비활성화 결과. | `provides`의 각 Module이 활성화의 역순으로 비활성화되고, 그 contract 바인딩이 해제된다. 계약 소비자 참조가 다른 Plugin이 제공한 것이면 침범하지 않는다. | `DeactivateIncomplete`, location = 실패한 module id. |
| **Remove** | 설치된(가능하면 비활성) plugin id. | 제거 결과. | Plugin이 설치·활성화 중 추가한 모든 산출물(등록 Module, 배치 파일, 배선)이 제거되고 잔여물 0. 본체는 설치 이전 상태와 동일하다 (10 INV-3). 다른 Plugin이 이 Plugin에 `dependsOn`으로 의존하면 제거를 거부한다. | `ResidueDetected` \| `DependentExists`. |

- **완료 조건·실패 reason 정본 보존.** 네 연산의 입력·출력·완료 조건·실패 reason은 10 §3.1을 **그대로 보존**한다(재정의 0, 새 조건·새 reason 0). 각 완료 조건 → 검사 규칙 → reason의 대응은 §3이 전개한다.
- **완료 조건 성립 = 해당 연산의 검사 전부 통과.** 한 연산이 완료로 성립하려면 §3의 그 연산 검사가 모두 "예"여야 한다. 하나라도 "아니오"이면 연산 실패이며 해당 검사의 reason으로 공통 Failure Report를 낸다(§3). 한 완료 조건이 여러 요소·여러 reason을 포함하면(예: Activate의 Register 성공이 `ContractMismatch`·`DuplicateId` 두 reason을 가짐) 그 완료 조건은 복수 검사·복수 reason으로 분기한다(재정의가 아니라 정본의 요소·reason을 검사로 분해).
- **Register/Resolve/Deregister 소비.** Activate는 01 §3.1-A Register/Resolve를, Deactivate/Remove는 01 §3.1-A Deregister를 소비한다(10 INV-2, §4). 이 소비 연산의 실패 사유(01 §3.2-D)와 Plugins가 표면화하는 reason(10 §3.2-B)의 대응은 §3이 결합한다.
- 입력·출력·완료 조건·실패의 상세 정본은 10 §3.1이 유지한다. 본 표는 그 연산을 인스턴스화할 뿐 계약을 재정의하지 않는다.

---

## §3. 완료 조건 검사 규칙 ↔ reason 결합 (done 대상 — 예/아니오 판정 규칙)

각 연산의 완료 조건(10 §3.1)을 **예/아니오로 판정 가능한 검사 규칙**으로 전개한다. 각 검사는 대상 Plugin(및 그 Plugin Manifest·bundle)을 대상으로 하며, 판정 대상 필드의 정본은 10 §3.2-A(소비 인터페이스 plugin-manifest.md §2)이고, 검사 실패 시 산출하는 공통 Failure Report 포맷·reason 열거의 정본은 10 §3.2-B(소비 인터페이스 plugin-manifest.md §3)다. 본 절은 그 필드·포맷을 재정의하지 않고 § 포인터로 소비하며, **어느 검사 실패가 어느 reason을 산출하는가의 결합만 소유**한다(§0).

### §3.1 검사 규칙 ↔ 연산·완료 조건·불변·reason 1:1 대응표 (done 대상 — 1:1 대응)

| 검사 | 판정 형태 (예/아니오) | 대응 연산·완료 조건 (10 §3.1) · 불변 | 판정 대상 (정본 § / 소비 인터페이스 plugin-manifest.md) | 검사 실패(= 아니오) 시 reason (소유: plugin-manifest.md §3 / 정본 10 §3.2-B) |
|---|---|---|---|---|
| **I1. 본체 불가침** | 설치가 본체(기존 계약·spec·Module)를 수정하지 않는가? | Install 완료 조건 (1) · 10 INV-1 | 본체 경계(Core 디렉터리·기존 spec·기존 Module) | `BodyMutation` |
| **I2. Framework 호환** | Manifest의 `frameworkCompat`가 현재 Framework 버전을 포함하는가? | Install 완료 조건 (2) | Plugin Manifest `frameworkCompat` (10 §3.2-A / plugin-manifest.md §2) | `IncompatibleFramework` |
| **I3. 의존 Plugin 기설치** | `dependsOn`의 각 Plugin이 모두 이미 설치되어 있는가? | Install 완료 조건 (3) | Plugin Manifest `dependsOn` (10 §3.2-A / plugin-manifest.md §2) | `MissingDependency` |
| **I4. plugin id 유일** | 설치될 `id`가 유일한가(기설치 Plugin과 충돌하지 않는가)? | Install 완료 조건 (4) | Plugin Manifest `id` (10 §3.2-A / plugin-manifest.md §2) | `DuplicateId` |
| **I5. 자기완결** | bundle이 선언되지 않은 본체 내부 경로에 은닉 의존하지 않는가? | Install 입력 요건(self-contained bundle, 10 §3.1) · 10 INV-8 · §6 실패 모드 | 선언되지 않은 본체 내부 경로 (의존은 `requires`·`dependsOn`으로만 — 10 INV-8) | `NotSelfContained` |
| **A1. provides 등록** | `provides`의 각 Module Manifest가 Runtime Register(01 §3.1-A)로 등록되는가? | Activate 완료 조건 · 10 INV-2 · 01 Register | Plugin Manifest `provides`의 각 Module Manifest (10 §3.2-A·01 §3.2-A / plugin-manifest.md §2) | `ContractMismatch` \| `DuplicateId` |
| **A2. requires 해소** | Plugin Manifest의 `requires` contract가 모두 Runtime Resolve(01 §3.1-A)로 해소되는가? | Activate 완료 조건 · 10 INV-2 · 01 Resolve | Plugin Manifest `requires` (10 §3.2-A / plugin-manifest.md §2) | `UnresolvedContract` |
| **D1. 비활성화 완결** | `provides`의 각 Module이 활성화 역순으로 비활성화되고 contract 바인딩(01 Deregister)이 해제되며, 다른 Plugin이 제공한 계약 소비자 참조를 침범하지 않는가? | Deactivate 완료 조건 · 01 Deregister(§4) | `provides`의 각 module id (10 §3.2-A / plugin-manifest.md §2) | `DeactivateIncomplete` |
| **R1. 잔여물 0** | Plugin이 추가한 모든 산출물(등록 Module·배치 파일·배선)이 제거되고 본체가 설치 이전 상태와 동일한가? | Remove 완료 조건 · 10 INV-3 · 01 Deregister(§4) | 추가 산출물·본체 상태 | `ResidueDetected` |
| **R2. 의존 Plugin 부재** | 다른 Plugin이 이 Plugin에 `dependsOn`으로 의존하지 않는가? | Remove 완료 조건 | 다른 Plugin의 `dependsOn` (10 §3.2-A / plugin-manifest.md §2) | `DependentExists` |
| **IG. 격리 불변 준수** | 포함 Module·요소가 Memory 단일 Port를 우회하지 않고(INV-5), Core 디렉터리에 AI 의존 요소를 주입하지 않으며(INV-4), 역할 경계를 재정의·우회하지 않는가(INV-6)? | Install/Activate 격리 가드 · 10 §3.3 INV-4/5/6 · §6 실패 모드 | 포함 Module·요소의 Memory 접근 경로·Core 배치·역할 경계 | `IsolationViolation` |

- 이 표가 done의 "각 연산의 완료 조건이 예/아니오 판정 가능한 검사로 전개되고 각 검사 실패가 해당 reason 코드로 1:1 연결된다"의 대조 지점이다(decompose-rules §3.1 관례 동형). 각 검사 상세는 §3.2~§3.6이다.
- **완료 조건과 입력 요건·격리 가드의 구분(정직).** I1~I4는 Install의 **번호 매겨진 완료 조건 (1)~(4)**(10 §3.1)에 1:1 대응한다. I5(`NotSelfContained`)는 Install의 **입력 요건**("self-contained Plugin bundle", 10 §3.1)과 10 INV-8·§6 실패 모드에서 산출되는 검사이며, 번호 매겨진 완료 조건 (1)~(4) 중 하나가 아니라 입력 자기완결성 요건에 결합한다 — 이는 decompose-rules §3이 완료 조건 (1)의 두 요소를 두 검사로 분해한 것과 대칭으로, 정본 Install이 5종 reason을 두므로 입력 요건 검사(I5)를 별도로 세워 5종 reason 전건을 1:1 결합한 것이다(reason 신설 0). IG(`IsolationViolation`)는 어느 연산의 번호 매겨진 완료 조건도 아니라 10 §3.2-B가 정의한 **격리 불변(INV-4/5/6) 위반의 공통 사유 코드**이며(§6 실패 모드), Install/Activate 시 포함 요소의 격리 위반을 걸러내는 가드로 산출된다 — 본 문서는 이를 완료 조건으로 창설하지 않고 §3.2-B/§6 정본이 정의한 격리 사유로만 결합한다(상세 §3.6).
- **판정 결합 소유 경계.** 위 표의 마지막 두 열(판정 대상·reason)에서, 필드 스키마와 reason 열거의 **소유·정본**은 10 §3.2-A/B와 plugin-manifest.md §2·§3에 있다. 본 표가 소유하는 것은 **검사↔연산·완료 조건↔reason의 결합**이며, 이는 plugin-manifest.md §3이 "규칙 인스턴스 문서 소관"으로 이연한 지점이다(§0).
- **결정성.** 각 검사는 동일 대상(Plugin·Manifest·bundle·Registry 상태)에 대해 동일한 "예/아니오"를 낸다 — 재량 개입이 없다. 이는 검사가 예/아니오 판정 규칙이라는 사실의 귀결이며, 도출 규칙의 결정성이지 검사 도구·실행 환경의 물리 결정성이 아니다(물리 실행은 Adapter Binding 소관, §6).
- **다중 실패 처리.** 한 연산에서 둘 이상의 검사가 "아니오"일 수 있다. 이 경우 각 실패 지점마다 공통 Failure Report 1건씩을 산출하며, `location` 필드(plugin-manifest.md §3)에 실패 지점(Manifest 필드·module id·침범 경계)을 담는다. reason별 `location`의 지시 대상은 각 검사 상세(§3.2~§3.6)가 규정한다.

### §3.2 Install 검사 (I1~I5)

Install 완료 조건 (1)~(4)(10 §3.1)와 입력 자기완결 요건을 예/아니오 검사로 전개한다. 대상은 설치될 Plugin의 bundle + Plugin Manifest(10 §3.2-A, plugin-manifest.md §2)와 현재 본체·기설치 Plugin 집합이다.

1. **I1 — 본체 불가침 (→ `BodyMutation`).** 절차: 설치가 본체(Core 디렉터리의 기존 계약·기존 spec·이미 등록된 Module)를 수정하는가? — 예/아니오. 본체 수정이 0이면 I1 = 예. 하나라도 수정이 있으면 I1 = 아니오 → Install 실패, reason = `BodyMutation`, `location` = 침범된 본체 경계(10 §6, 10 INV-1). 검사 범위(정직): 확장은 오직 추가로만 이뤄지는가를 본체 경계 **전체**에 대해 대조한다 — 표본 한 파일의 무변경으로 전체 무변경을 결론 내지 않는다.
2. **I2 — Framework 호환 (→ `IncompatibleFramework`).** 절차: Manifest의 `frameworkCompat` 범위가 현재 Framework 버전을 포함하는가? — 예/아니오. 포함하면 I2 = 예. 범위 밖이면 I2 = 아니오 → Install 거부, reason = `IncompatibleFramework`, `location` = `frameworkCompat` 필드(10 §6).
3. **I3 — 의존 Plugin 기설치 (→ `MissingDependency`).** 절차: `dependsOn`의 각 Plugin id가 모두 이미 설치되어 있는가? — id별 예/아니오. 전부 기설치이면 I3 = 예. 하나라도 미설치이면 I3 = 아니오 → Install/Activate 거부, reason = `MissingDependency`, `location` = 미설치 Plugin id(10 §6). 검사 범위(정직): `dependsOn` **전수**(모든 의존 Plugin). 표본 하나의 존재로 전체 존재를 결론 내지 않는다.
4. **I4 — plugin id 유일 (→ `DuplicateId`).** 절차: 설치될 `id`가 기설치 Plugin의 어느 `id`와도 충돌하지 않는가? — 예/아니오. 유일하면 I4 = 예. 충돌하면 I4 = 아니오 → Install 거부, reason = `DuplicateId`, `location` = 충돌 plugin id(10 §6). `id`는 안정적이어야 설치·제거·의존 해소의 기준이 된다(10 INV-9).
5. **I5 — 자기완결 (→ `NotSelfContained`).** 절차: bundle이 선언되지 않은 본체 내부 경로·구현에 은닉 의존하지 않는가(의존은 Manifest의 `requires`·`dependsOn`으로만 선언되었는가)? — 예/아니오. 은닉 의존이 0이면 I5 = 예. 선언되지 않은 본체 내부 경로 은닉 의존이 있으면 I5 = 아니오 → Install 거부, reason = `NotSelfContained`, `location` = 은닉 의존 지점(10 §6, 10 INV-8). 이 검사는 Install 입력 요건("self-contained Plugin bundle", 10 §3.1)의 예/아니오 전개이며, 번호 매겨진 완료 조건이 아니라 입력 자기완결성에 결합한다(§3.1 구분 주). 검사 범위(정직): 선언된 의존(`requires`·`dependsOn`) 밖의 본체 내부 경로 참조를 bundle **전체**에 대해 대조한다 — 일부 요소만 보고 자기완결로 결론 내지 않는다.

**Install 성립 = I1 ∧ I2 ∧ I3 ∧ I4 ∧ I5 전부 예.** 성립 시 출력은 설치된 plugin id이며 상태는 registered-but-inactive(10 §3.1). 이 시점에 IG(격리 가드, §3.6)도 함께 걸리면 `IsolationViolation`을 산출한다.

### §3.3 Activate 검사 (A1~A2)

Activate 완료 조건(10 §3.1)을 예/아니오 검사로 전개한다. 대상은 설치된 plugin id와 그 Plugin Manifest의 `provides`·`requires`(plugin-manifest.md §2)다. 활성화는 Register/Resolve 계약으로만 성립하며 독자적 등록·해소 경로를 만들지 않는다(10 INV-2).

1. **A1 — provides 등록 (→ `ContractMismatch` | `DuplicateId`).** 절차: `provides`의 각 Module Manifest가 Runtime Register(01 §3.1-A)로 등록되는가? — 항목별 예/아니오. 전부 등록 성공이면 A1 = 예. 하나라도 실패하면 A1 = 아니오 → Activate 실패. Register의 실패 사유(01 §3.1-A Register: reason = `ContractMismatch` | `DuplicateId`)를 그대로 표면화한다 — Manifest가 Module Interface 계약을 만족하지 않으면 `ContractMismatch`, module id가 Registry에서 유일하지 않으면 `DuplicateId`. `location` = 실패한 module id. 검사 범위(정직): `provides`의 **각 Module Manifest 전수**. 표본 하나의 등록 성공으로 전체 성공을 결론 내지 않는다.
2. **A2 — requires 해소 (→ `UnresolvedContract`).** 절차: Plugin Manifest의 `requires` contract가 모두 Runtime Resolve(01 §3.1-A)로 해소되는가? — contract별 예/아니오. 전부 해소되면 A2 = 예. 하나라도 미해소이면 A2 = 아니오 → Activate 실패, reason = `UnresolvedContract`(01 §3.2-D 재사용, 10 §3.2-B), `location` = 미해소 contract id(10 §6). 여기서의 `requires`는 **처리 대상 개별 Plugin의 Plugin Manifest `requires`**이지 Plugins Provider Module 자신의 `requires`가 아니다(plugin-manifest.md §2 구분, module-manifest.md §3 requires). 검사 범위(정직): `requires` **전수**.

**Activate 성립 = A1 ∧ A2 전부 예.** 성립 시 출력은 등록된 module id 목록(10 §3.1). Register/Resolve 경유가 활성화의 유일한 성립 경로다(10 INV-2).

### §3.4 Deactivate 검사 (D1)

Deactivate 완료 조건(10 §3.1)을 예/아니오 검사로 전개한다. 대상은 활성 plugin id와 그 `provides`의 각 Module이다. contract 바인딩 해제는 01 §3.1-A Deregister 위에서 성립한다(§4).

1. **D1 — 비활성화 완결 (→ `DeactivateIncomplete`).** 절차(복합 예/아니오): (i) `provides`의 각 Module이 활성화의 **역순**으로 비활성화되는가? (ii) 각 Module의 contract 바인딩이 해제되는가(01 §3.1-A Deregister 경유)? (iii) 다른 Plugin이 제공한 계약 소비자 참조를 침범하지 않는가? — 세 하위 조건 모두 예이면 D1 = 예. 하나라도 아니오이면 D1 = 아니오 → Deactivate 실패, reason = `DeactivateIncomplete`, `location` = 실패한 module id(10 §3.1). 검사 범위(정직): `provides`의 **각 Module 전수**를 역순 대조하고, 다른 Plugin 제공 계약 소비자와의 경계 침범 여부를 **전수** 대조한다 — 표본 한 Module의 비활성화 성공으로 전체 완결을 결론 내지 않는다.

**Deactivate 성립 = D1 = 예.** 계약 소비자 참조가 다른 Plugin이 제공한 것이면 침범하지 않는다는 경계 조건은 D1의 하위 조건 (iii)로 검사한다(10 §3.1).

### §3.5 Remove 검사 (R1~R2)

Remove 완료 조건(10 §3.1)을 예/아니오 검사로 전개한다. 대상은 설치된(가능하면 비활성) plugin id다. 등록 Module 제거는 01 §3.1-A Deregister 위에서 성립한다(§4).

1. **R2 — 의존 Plugin 부재 (→ `DependentExists`).** 절차: 다른 Plugin이 이 Plugin에 `dependsOn`으로 의존하는가? — 예/아니오. 의존하는 Plugin이 없으면 R2 = 예. 하나라도 의존하면 R2 = 아니오 → Remove 거부, reason = `DependentExists`, `location` = 의존하는 Plugin id(10 §6). 이 검사는 제거 착수 전의 거부 게이트다(의존이 있으면 제거하지 않는다). 검사 범위(정직): 기설치 Plugin 집합의 `dependsOn` **전수**를 대상 Plugin에 대해 대조한다.
2. **R1 — 잔여물 0 (→ `ResidueDetected`).** 절차: Plugin이 설치·활성화 중 추가한 모든 산출물(등록 Module·배치 파일·배선)이 제거되고 본체가 설치 이전 상태와 동일한가(잔여물 0)? — 예/아니오. 잔여물이 0이면 R1 = 예. 잔여물이 있으면 R1 = 아니오 → Remove 미완료, reason = `ResidueDetected`, `location` = 잔여물 지점(10 §6, 10 INV-3). 등록 Module 제거는 01 §3.1-A Deregister로 이뤄진다(§4). 검사 범위(정직): 추가 산출물(등록 Module·배치 파일·배선) **전 부류 전수**를 스캔한다 — 한 부류(예: 등록 Module)만 제거 확인하고 다른 부류(배선)를 통과로 간주하지 않는다(좁은 대리 지표 금지, 06 §8 예1 유형 회피).

**Remove 성립 = R2 ∧ R1 전부 예.** 논리 순서는 R2(의존 부재 게이트) → 제거 수행 → R1(잔여물 0 확인)이다. 성립 시 본체는 설치 이전 상태와 동일하다(10 INV-3).

### §3.6 격리 불변 가드 (IG → `IsolationViolation`)

- `IsolationViolation`은 10 §3.2-B가 정의한 **격리 불변(INV-4/5/6) 위반의 공통 사유 코드**다. 이는 네 연산 중 어느 것의 **번호 매겨진 완료 조건**도 아니며(§3.1 구분 주), Install/Activate 시 포함 Module·요소가 격리 불변을 위반할 때 걸러내는 **가드**로 산출된다(10 §6 실패 모드).
- 절차(복합 예/아니오): (INV-5) 포함하는 어떤 Module도 Memory Service Interface(단일 Port)를 우회해 영속성 백엔드에 직접 접근하지 않는가? (INV-4) 포함 요소가 Core 디렉터리에 AI 의존 요소를 주입하지 않는가? (INV-6) Plugin이 Agent 역할 경계(02 §3.2-A)를 재정의·우회하지 않는가? — 세 하위 조건 모두 예이면 IG = 예. 하나라도 아니오이면 IG = 아니오 → 격리 위반, reason = `IsolationViolation`, `location` = 침범 경계(Memory 접근 경로·Core 배치 지점·역할 경계)(10 §6).
- **소유 경계.** reason `IsolationViolation`의 열거·포맷 소유는 plugin-manifest.md §3이며, 본 문서는 이 격리 가드가 산출하는 결합만 소유한다. 이 가드는 10 §3.3 INV-4/5/6·§6 실패 모드를 예/아니오 검사로 옮긴 것이지 새 완료 조건·새 reason의 창설이 아니다(재정의 0).
- 검사 범위(정직): 포함 Module·요소 **전수**에 대해 세 격리 불변을 각각 대조한다 — 한 요소의 준수로 전체 준수를 결론 내지 않는다.

### §3.7 검사 물리 실행 경계

- 위 I1~I5·A1~A2·D1·R1~R2·IG는 **예/아니오 판정 규칙**이다. 이 규칙을 **누가·어떤 물리 채널로 실행하는가** — 설치·제거 수행 주체의 물리 채널, bundle 배치·배선·제거 방식, 검사 실행 방식, 배포 채널 — 은 이 문서가 서술하지 않는다. 이는 Adapter Binding 문서 소관이다(01 §4, 10 §4.1·§4.2, §6).
- 검증 측면에서 이 검사들은 10 §7 검증 방법("Verifier가 Install 전후 본체 diff = 0을 확인 / Activate 시 Register/Resolve 호출과 반환 핸들을 확인 / Remove 후 잔여물 스캔 = 0을 확인 / 포함 요소의 Memory 접근 경로가 단일 Port임을 확인")과 정합한다 — 본 문서는 그 판정 규칙을 확정하고, 판정 주체·시점·전이는 정의하지 않는다(06·03-loop 소관, 10 §3.3 경계 정합).

---

## §4. Deregister 기반 성립 (Deactivate/Remove)

- **개별 Module의 등록 해제(Deregister)는 Plugin 비활성화·제거의 전제다.** 10 §3.1 주의는 Deactivate/Remove가 요구하는 개별 Module 등록 해제 연산의 소유·정합이 조율 항목이었음을 기록하고, 10·01 §9 결정 기록은 그 조율을 **01 §3.1-A에 Deregister 연산을 추가**하는 것으로 해소했다. Registry 수명주기는 Runtime 소유이므로 Plugins가 우회 정의하지 않고 01의 Deregister를 소비한다(01 §9 결정 기록).
- **Deactivate의 성립.** D1(§3.4)의 하위 조건 (ii) "각 Module의 contract 바인딩 해제"는 01 §3.1-A **Deregister**(대상 Module을 Deactivate한 후 Registry에서 제거하고 그 contract 바인딩을 해제)로 실현된다. Deregister의 완료 조건(다른 활성 Module의 requires가 그 contract에 의존 중이면 해제를 거부)은 D1의 하위 조건 (iii) "다른 Plugin이 제공한 계약 소비자 참조 비침범"과 정합한다(01 §3.1-A Deregister).
- **Remove의 성립.** R1(§3.5)의 "등록 Module 제거"는 01 §3.1-A **Deregister**로 실현된다. Plugin이 추가한 등록 Module 각각이 Deregister되어야 잔여물 0(10 INV-3)이 성립한다. 배치 파일·배선의 물리 제거는 Adapter Binding 소관이다(§3.7, 10 §4.1·§4.2).
- **경계.** Deregister 연산 자체의 입력·출력·완료 조건·실패 reason(`DependentExists` | `NotRegistered`)의 정본은 01 §3.1-A가 유지한다. 본 문서는 그 연산을 재정의하지 않고 Deactivate/Remove가 그 위에서 성립함을 § 포인터로 명시할 뿐이다. Plugins가 표면화하는 reason(`DeactivateIncomplete`·`ResidueDetected`, 10 §3.2-B)과 01 Deregister의 실패 사유의 대응은 §3이 결합하고, 그 물리 실현은 Adapter Binding 소관이다.

---

## §5. 소비하는 정본 포맷 (§ 포인터 — 재게재 0)

본 문서의 검사 규칙(§3)이 참조하는 포맷은 전부 소비 인터페이스 plugin-manifest.md(§2·§3)와 정본 10 §3.2가 소유한다. 본 문서는 필드 표를 **재게재·재정의하지 않고** § 포인터로만 소비한다(이중 갱신 방지).

| 소비 대상 포맷 | 소비 인터페이스 인스턴스 | 정본 § | 본 문서의 소비 지점 |
|---|---|---|---|
| Plugin Manifest 포맷 (`id`/`version`/`provides`/`requires`/`dependsOn`/`frameworkCompat`) | plugin-manifest.md §2 | 10 §3.2-A | §2 입력·완료 조건, §3(I2·I3·I4·A1·A2·D1·R2 판정 대상 — `frameworkCompat`·`dependsOn`·`id`·`provides`·`requires`) |
| 공통 Failure Report 포맷 (`operation`/`target`/`reason`/`location`) + reason 11종 열거 | plugin-manifest.md §3 | 10 §3.2-B | §2 실패 reason, §3 실패 결합(각 연산 reason 산출·`location` 지시) |
| Module Manifest 포맷 (Provider 등록 서술자 7필드) | module-manifest.md §2 | 01 §3.2-A | §0·§2 — `provides`의 각 Module Manifest(01 §3.2-A) 참조, Provider의 `entrypoint`·`contract` 소유 지시 |

- **필드 표 비재게재.** 위 포맷의 필드 표(6필드·4필드·reason 11종 열거·7필드)는 plugin-manifest.md §2·§3와 module-manifest.md §2가 단일 소유한다. 본 문서는 검사·결합에 필요한 **필드명·reason 값**을 § 포인터로 인용할 뿐, 필드 표를 다시 그리지 않는다.
- **reason 결합 소유는 본 문서.** 포맷의 reason 열거(11종) 소유는 plugin-manifest.md §3이나, **각 reason이 어느 연산의 어느 검사에서 산출되는가**의 결합은 본 문서 §3이 소유한다(§0 — plugin-manifest.md §3이 규칙 인스턴스 문서로 이연한 지점). 본 문서는 reason을 값으로 인용할 뿐 새 코드를 신설하지 않는다.
- **Deregister 정본.** Deactivate/Remove가 소비하는 01 §3.1-A Deregister 연산의 정본은 01 §3.1-A가, 그 추가 승인 결정 기록은 10·01 §9가 유지한다(§4). 본 문서는 이를 재정의하지 않는다.

---

## §6. 경계와 비의존 (재정의 0 · 07 R2 · 금지 토큰 · Glossary)

본 문서가 준수하는 경계를 한자리에 모은다. 검증 대조 지점이다.

- **10·01 계약 재정의·확장 0.** §2~§4의 모든 연산 인터페이스·검사 규칙은 10 §3.1·§3.2-A/B와 01 §3.1-A의 인스턴스이며 § 포인터로만 참조한다. 네 연산의 입력·출력·완료 조건·실패 reason은 정본을 그대로 보존했다(새 완료 조건·새 reason·새 연산 0). 01 §3.1-A Register/Resolve/Deregister도 재정의하지 않았다. 진위 판정 기준은 10 §3.1·§3.2-A/B와 01 §3.1-A가 유지한다. 위반(형태 B가 10·01 계약을 바꾸어야만 성립하는 경우)이 발견되면 구현하지 않고 Advisor에게 보고한다.
- **인스턴스화 대상 경계.** 본 문서의 인스턴스화 대상은 네 연산(10 §3.1)의 규칙(완료 조건 검사·reason 결합·Deregister 기반 성립)이다. **개별 Plugin Manifest·공통 Failure Report의 포맷 정의는 대상이 아니며**(plugin-manifest.md §2·§3 소관), **Provider 등록 서술자(Module Manifest 7필드)도 대상이 아니다**(module-manifest.md 소관) — 모두 § 포인터로만 소비한다.
- **포맷 비재게재(이중 갱신 방지).** Plugin Manifest·공통 Failure Report·Module Manifest 포맷은 plugin-manifest.md §2·§3·module-manifest.md §2를 § 포인터로만 소비했고 필드 표를 재게재·재정의하지 않았다(§5). reason 열거의 소유는 plugin-manifest.md §3, 각 reason↔연산·검사 결합의 소유는 본 문서 §3이다.
- **07 R2 경계 — 동시 작성 형제 불인용.** 같은 병렬 집합(v0.8 PS-1)에서 동시 작성 중인 형제 산출물(Adapter Binding 바인딩 문서·시연 절차서)의 미완성 내용은 인용·추측하지 않았다. 확정된 정본(10·01 spec, structure.md, Glossary)과 소비 인터페이스(함께 확정되는 plugin-manifest.md·module-manifest.md), 기존 Baseline(framework/runtime/·workflow/·core/ 문서)만 참조했다. 물리 실현(bundle 배치·배선·배포 채널·물리 실행)은 "Adapter Binding 문서 소관" 수준의 일반 포인터로만 지시했다(특정 문서명 비기입).
- **물리 실현 비서술.** 설치·제거 수행 주체의 물리 채널, bundle의 직렬화·물리 위치·배치·배포 채널, 검사 규칙의 물리 실행 방식은 서술하지 않고 **Adapter Binding 문서 소관**(01 §4, 10 §4.1·§4.2) 포인터로만 처리했다. 특정 Adapter Binding 문서명을 두지 않았다.
- **금지 토큰 비의존(structure.md §5 C-3 확장, 10 INV-10) — 자가 부류별 전수 스캔 수행.** 본문 전체를 다음 후보 부류 **전체**로 전수 대조하여 실증 0건임을 확인했다(단일 토큰 검색에 국한하지 않고 부류별 전수 대조) — { 특정 AI 이름·모델명·제품 기능명 } ∪ { 프로그래밍 언어명·툴체인명 } ∪ { 직렬화 형식명·확장자·OS 토큰 } ∪ { 물리 경로·bundle 물리 위치·배포 채널명·Adapter 하위 인스턴스 토큰·특정 Adapter Binding 문서명 }. 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관(01 §4, 10 §4.1·§4.2)" 포인터를 두었다 — 금지 토큰의 예시조차 본문에 나열하지 않았다(mention/use 경계). 다음은 금지 토큰이 아니다: (i) 연산명(Install/Activate/Deactivate/Remove·Register/Resolve/Deregister)·reason 열거 값(`BodyMutation`·`IncompatibleFramework`·`MissingDependency`·`DuplicateId`·`NotSelfContained`·`ContractMismatch`·`UnresolvedContract`·`DeactivateIncomplete`·`ResidueDetected`·`DependentExists`·`IsolationViolation`) — 10 §3 정본의 평이한 열거 값; (ii) Glossary·AGENT.md 정본 어휘 — Plugin·Plugin Manifest·Plugins(Glossary §3.2-J J-10·§3.2-D)·Module·Register/Resolve/Deregister와 역할 명칭(Advisor/Planner/Worker/Verifier); (iii) 계약 필드명 백틱 표기(`id`·`version`·`provides`·`requires`·`dependsOn`·`frameworkCompat`·`operation`·`target`·`reason`·`location`·`contract`·`entrypoint` — 10 §3.2·01 §3.2 정본 어휘)와 상태 라벨(registered-but-inactive — 10 §3.1 정본 어휘); (iv) 저장소 문서 식별자(`specs/…`·`framework/…` 상호 참조 및 본 문서 자신의 식별자 `framework/plugins/plugin-lifecycle.md`) — 문서 식별자이며 직렬화 형식·물리 경로 토큰이 아니다(structure.md §5·decompose-rules §6 분류 선례 동형). 검사 라벨(I1~I5·A1~A2·D1·R1~R2·IG)은 본 문서 서술 편의의 명명 규칙이며 계약 용어·금지 토큰이 아니다.
- **Glossary 정본.** 사용 용어는 전부 specs/00-glossary.md §3.2-J(J-10)·§3.2-D 정본 또는 Glossary 기존 어휘이거나 평이한 열거 값이다. 새 용어를 신설하지 않았다. "Install·Activate·Deactivate·Remove·공통 Failure Report·reason 사유 코드"는 10 §3 정본이 정의한 연산·포맷·서술 명칭이며 본 문서 신설 용어가 아니다.

---

## §7. 요약 (규격 한눈에 보기)

- 이 문서 = **네 연산(Install/Activate/Deactivate/Remove, 10 §3.1)의 규칙 인스턴스**. 정본 = 10 §3.1(본 문서는 인스턴스, 재정의 아님 — C-1). 소비하는 포맷의 소비 인터페이스 = plugin-manifest.md(§2·§3)·module-manifest.md(§2).
- **연산 인터페이스(§2)** — 네 연산의 입력·출력·완료 조건·실패 reason을 10 §3.1 정본 그대로 보존. Activate는 01 Register/Resolve, Deactivate/Remove는 01 Deregister를 소비(10 INV-2, §4).
- **검사 규칙(§3)** — 각 연산 완료 조건 → 예/아니오 검사 + reason 1:1 결합. Install I1 본체 불가침→`BodyMutation`·I2 Framework 호환→`IncompatibleFramework`·I3 의존 기설치→`MissingDependency`·I4 id 유일→`DuplicateId`·I5 자기완결→`NotSelfContained`(입력 요건·INV-8); Activate A1 provides Register→`ContractMismatch`\|`DuplicateId`·A2 requires Resolve→`UnresolvedContract`; Deactivate D1 비활성화 완결→`DeactivateIncomplete`; Remove R2 의존 부재→`DependentExists`·R1 잔여물 0→`ResidueDetected`; 격리 가드 IG(INV-4/5/6)→`IsolationViolation`(§6 실패 모드). 각 연산 성립 = 그 연산 검사 전부 예. 각 검사는 전수 범위·결정적 판정. reason↔검사 결합이 본 문서 소유(plugin-manifest.md §3이 이연한 지점).
- **Deregister 기반 성립(§4)** — Deactivate의 바인딩 해제·Remove의 등록 Module 제거는 01 §3.1-A Deregister 위에서 성립(10 §3.1 주의, 10·01 §9 결정 기록). Registry 수명주기는 Runtime 소유, Plugins는 소비만.
- **포맷 소비(§5)** — Plugin Manifest·공통 Failure Report·Module Manifest 포맷은 plugin-manifest.md §2·§3·module-manifest.md §2를 § 포인터로만 소비(필드 표 재게재·재정의 0).
- **경계(§6)** — 10·01 재정의·확장 0, 포맷 정의 비소관(plugin-manifest.md·module-manifest.md 소관), 07 R2 형제 불인용, 물리 실현 Adapter Binding 소관(01 §4, 10 §4.1·§4.2), 금지 토큰 0(자가 부류별 전수 스캔), Glossary §3.2-J J-10·§3.2-D 정본만 사용.
- 모든 규칙은 10 §3.1의 인스턴스이며, 물리 실현은 Adapter Binding 소관이다. 형태 A(문서) → 형태 B(실행 코드) 전환에도 Core Contract 변경은 0이다.
