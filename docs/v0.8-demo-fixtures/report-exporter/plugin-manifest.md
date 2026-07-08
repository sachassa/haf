# [시연 픽스처 — 실계약 문서 아님] report-exporter — Plugin Manifest 인스턴스 (F-P1 bundle 원본)

> **시연 픽스처 — 실계약 문서 아님.** 이 파일은 v0.8 Extension System 시연(Task EX-DP — Plugins 수명주기)의 레퍼런스 Plugin **F-P1**의 배포 서술자 인스턴스다. 실계약 문서가 아니다. 이 bundle 원본은 산출물 "레퍼런스 Plugin 1"의 정본 실물로 존치하며, 그 설치본은 시연 중 Install로 생성되었다가 Remove로 제거된다. 결함 없는 통과 케이스이므로 "의도적 결함 정당 보유"는 해당 없음이다.
>
> **포맷 정본 경계.** 이 파일은 Plugin Manifest **포맷을 재정의하지 않는다.** 6필드·필수/선택 표기의 진위 판정 기준 정본은 **10 §3.2-A**이며, 그 포맷 인스턴스 소유 규격이 스키마를 유지한다. 이 파일은 그 스키마를 이 레퍼런스 Plugin에 대한 구체 **값**으로 채운 배포 서술자 인스턴스일 뿐이다(Advisor 확정 DP-E2 · 10 §8 예1 동형).
>
> **자기완결 주의.** 이 배포 payload 본문은 선언(requires·dependsOn) 밖의 본체 내부 파일 경로에 의존하지 않는다 — 계약 정본은 spec 절 포인터(10 §3.2-A 등)로만 가리키며, 어떤 본체 내부 구현 파일에도 은닉 의존하지 않는다(I5 대조 지점). 등장하는 경로는 이 bundle 자신의 설치본 대상 위치뿐이다.

---

## Plugin Manifest 6필드 (정본 스키마: 10 §3.2-A)

| 필드 | 값 (이 Plugin 인스턴스) | 필수 (정본 표기 보존) |
|---|---|---|
| `id` | `report-exporter` | 예 |
| `version` | `1.0` | 예 |
| `provides` | `[ Module Manifest 1건 → core/report-exporter-module.md (contract=`ReportExporterInterface`) ]` (최소 1건 충족; 각 항목은 Module Manifest 01 §3.2-A 1건) | 예 |
| `requires` | `[]` (없음 — 활성화 시 Resolve할 contract id 없음) | 아니오(기본 없음) |
| `dependsOn` | `[]` (없음 — 선행 설치·활성화가 필요한 다른 Plugin 없음) | 아니오(기본 없음) |
| `frameworkCompat` | `>= v0.8` (현행 Framework 버전 v0.8 포함) | 예 |

- **필수/선택 표기 보존.** 6필드 중 4필드(`id`·`version`·`provides`·`frameworkCompat`)는 **예**, 2필드(`requires`·`dependsOn`)는 **아니오(기본 없음)**다 — 10 §3.2-A 정본 표기 그대로 보존(재정의 0, 새 필드 0).
- **`provides` 구성.** 이 Plugin은 **독립 Module 1개**를 번들한다(DP-E2 — Hook/Skill 미번들). `provides`의 유일 항목은 `core/report-exporter-module.md`(bundle 내부)가 서술하는 Module Manifest(contract=`ReportExporterInterface`) 1건이다. 확장 요소(Hook/Skill) 참조는 포함하지 않는다.
- **`requires`=`[]` 의미.** 이 개별 Plugin이 활성화(Activate)되기 위해 Runtime에서 Resolve되어야 하는 contract id가 없다(10 §3.2-A). 따라서 Activate 검사 A2(requires 해소)는 대상 0건에 대한 전수 해소이며 공진리(vacuously true)로 성립한다.
- **`dependsOn`=`[]` 의미.** 이 Plugin은 다른 Plugin에 선행 의존하지 않는다. Install 검사 I3(의존 Plugin 기설치)은 대상 0건 전수로 성립하고, Remove 검사 R2(의존 Plugin 부재)는 이 Plugin에 `dependsOn`으로 의존하는 다른 Plugin이 없으므로 성립한다.
- **`frameworkCompat` 의미.** 현행 Framework 버전(v0.8)을 포함하는 범위다. Install 검사 I2(Framework 호환)는 v0.8 ∈ `>= v0.8`이므로 성립한다.
- **새 Config scope 미도입(10 INV-7).** 이 Plugin Manifest는 새 Config scope를 도입하지 않는다. 포함 Module의 Config 스키마는 그 Module Manifest가 그대로 소유한다(포함 Module은 `configSchema` 미선언).
