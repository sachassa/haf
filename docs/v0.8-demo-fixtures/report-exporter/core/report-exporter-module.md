# [시연 픽스처 — 실계약 문서 아님] report-exporter-module — 포함 Module (contract: ReportExporterInterface)

> **시연 픽스처 — 실계약 문서 아님.** 이 파일은 F-P1 bundle의 **포함 Module**(AI 비의존 문서형 구현)이며, 실계약 문서가 아니다. bundle의 Core 경계에 놓여 AI·언어·툴체인·직렬화 형식·물리 경로 비의존을 유지한다. 결함 없는 통과 케이스이므로 "의도적 결함 정당 보유"는 해당 없음이다.
>
> **정본 경계.** 이 파일은 Module Manifest 계약(01 §3.2-A 7필드)을 재정의하지 않는다 — 그 값 인스턴스일 뿐이다. 진위 판정 기준 정본은 01 §3.2-A(계약)와 Module Manifest 형식 규격(형식)이 유지한다.
>
> **자기완결 주의.** 이 배포 payload 본문은 선언(requires·dependsOn) 밖의 본체 내부 파일 경로를 참조하지 않는다 — 계약 정본은 spec 절 포인터(01 §3.2-A)로만 가리키며, 어떤 본체 내부 구현 파일에도 은닉 의존하지 않는다(I5 대조 지점).

---

## §1. Module Manifest 7필드 인스턴스 (정본: 01 §3.2-A)

| 필드 | 값 (이 Module 인스턴스) | 필수 (정본 표기 보존) |
|---|---|---|
| `id` | `report-exporter-module` (역할 기반 안정 식별자) | 예 |
| `contract` | `ReportExporterInterface` | 예 |
| `version` | `1.0` | 예 |
| `requires` | 선언하지 않음 (기본 없음 — 해소해야 할 다른 contract 의존이 없다) | 아니오(기본 없음) |
| `entrypoint` | 추상 참조 — `ReportExporterInterface`가 노출하는 리포트 내보내기 연산의 논리 진입점. 물리 해소는 Adapter Binding 문서 소관. | 예 |
| `configSchema` | 선언하지 않음 (소비하는 Config 값이 없다) | 아니오 |
| `replaceable` | 기본 `true` (생략) | 아니오(기본 true) |

- 필수 4필드(`id`·`contract`·`version`·`entrypoint`), 선택 3필드(`requires`·`configSchema`·`replaceable`) — 01 §3.2-A 필수/선택 표기 그대로 보존.

## §2. contract 시그니처 — ReportExporterInterface (언어 중립·AI 비의존)

`ReportExporterInterface`는 **입력 레코드 집합을 정렬된 리포트 문서로 변환**하는 하나의 연산을 노출하는 Port다. 순수한 자료 변환이며, 어떤 AI 모델·실행 환경·영속성 백엔드에도 의존하지 않는다.

- **연산:** `export(records, spec) -> report`
  - **입력 records** — 레코드의 순서 없는 집합. 각 레코드는 이름 있는 필드들의 모음이다(예: name, category, value).
  - **입력 spec** — 리포트 명세. (a) 정렬 키(어느 필드로, 오름/내림차순), (b) 그룹 키(어느 필드로 그룹핑), (c) 각 그룹의 요약 규칙(예: value 합계)을 담는다.
  - **출력 report** — 정렬·그룹핑된 레코드 목록과 그룹별 요약 줄을 포함하는 리포트 산출물. 동일 (records, spec) 입력에 대해 항상 동일한 report를 낸다(결정적 변환).
- **완료 조건(연산 성립):** 출력 리포트가 (1) spec의 정렬 키 순서를 지키고, (2) spec의 그룹 키로 그룹핑되며, (3) 각 그룹 말미에 요약 규칙이 계산한 요약 줄을 정확히 1개 둔다.

## §3. 자기완결·격리 준수 (I5·IG 대조 지점)

- **자기완결(I5).** 이 Module은 선언(requires 미선언·상위 Plugin Manifest dependsOn=[]) 밖의 본체 내부 경로·구현에 **은닉 의존하지 않는다.** 변환 연산은 입력 records·spec만으로 성립하며, bundle 밖의 Core 계약·기존 Module·기존 spec 구현을 참조하지 않는다(계약 정본은 spec 절 포인터로만 가리킨다).
- **격리 — Memory 단일 Port 우회 0 (IG · INV-5).** 이 Module은 영속성 백엔드에 접근하지 않는다 — Memory Service Interface든 그 백엔드든 소비 지점이 없다. 접근 자체가 없으므로 단일 Port 우회가 발생할 수 없다(우회 0, 공진리 성립).
- **격리 — Core AI 의존 주입 0 (IG · INV-4).** 이 Module 구현 본문에는 특정 AI 모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로 토큰이 없다(순수 자료 변환 서술). Core 배치에 AI 의존 요소를 주입하지 않는다.
- **격리 — 역할 경계 재정의 0 (IG · INV-6).** 이 Module은 Agent 역할 경계(02 §3.2-A)를 재정의·우회하지 않는다. 리포트 변환 능력만 제공하며 Advisor·Worker·Verifier의 권한 경계나 Verify 판정을 건드리지 않는다.
