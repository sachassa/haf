# [시연 픽스처 — 실계약 문서 아님] report-exporter — bundle 자기완결 선언 (F-P1)

> **시연 픽스처 — 실계약 문서 아님.** 이 파일은 F-P1 bundle 원본의 자기완결 선언·내부 경계 안내이며, 실계약 문서가 아니다. 결함 없는 통과 케이스이므로 "의도적 결함 정당 보유"는 해당 없음이다.

---

## bundle 구성 (self-contained 배포 단위)

이 bundle(`docs/v0.8-demo-fixtures/report-exporter/`)은 레퍼런스 Plugin `report-exporter`의 self-contained 배포 단위 원본이다(plugins-binding §3.1 DP-E6 ⓐ). 하나의 경계 안에 배포 서술자와 포함 Module 구현을 묶는다.

| 구성 요소 | 파일 | 성격 (내부 Core/Adapter 경계) |
|---|---|---|
| Plugin Manifest (배포 서술자, 6필드) | `plugin-manifest.md` | 배포 서술자 — bundle 루트 |
| 포함 Module 구현 (contract=`ReportExporterInterface`) | `core/report-exporter-module.md` | **Core 경계** — AI 비의존 Module 구현 |
| (AI 의존 바인딩) | 없음 | **Adapter 경계** — 미사용 (이 Plugin은 AI 비의존 문서형이므로 Adapter 경계 산출물이 없다, DP-E2·plugins-binding §3.1 ⓓ 구조만 확정) |
| bundle 자기완결 선언 | `bundle-note.md` (이 파일) | bundle 메타(픽스처 전용 — 배포 payload 아님) |

## 내부 Core/Adapter 경계 유지 (10 §4.1 말미)

- **Core 경계(`core/`).** AI 비의존 Module 구현을 담는다. 특정 AI·언어·툴체인·직렬화 형식·물리 경로 토큰이 없다.
- **Adapter 경계.** AI 의존 바인딩이 있다면 `.claude/` 경계로 격리되어야 하나(plugins-binding §3.1 ⓓ, 10 INV-4), 이 레퍼런스 Plugin은 AI 비의존이라 산출물이 없다 — 경로 구조만 확정하고 미사용한다.

## 자기완결성 (I5 대조 지점)

- 이 bundle은 선언(Plugin Manifest `requires`=`[]`·`dependsOn`=`[]`, 포함 Module `requires` 미선언) 밖의 본체 내부 경로에 **은닉 의존하지 않는다.** 포함 Module의 변환 연산은 입력만으로 성립하며, bundle 밖 Core 계약·기존 Module·기존 spec을 참조하지 않는다.

## 배포 payload 경계 (Install 대상)

- Install이 설치본(`framework/plugins/report-exporter/`)으로 배치하는 **배포 payload** = `plugin-manifest.md` + `core/report-exporter-module.md` (배포 서술자 + 포함 Module 구현).
- `bundle-note.md`(이 파일)는 bundle 원본의 픽스처 전용 메타 문서이며 배포 payload에 포함되지 않는다.
