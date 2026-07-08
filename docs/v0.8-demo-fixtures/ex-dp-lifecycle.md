# [시연 픽스처 — 실계약 문서 아님] EX-DP 관측 기록 — Plugins 수명주기 (F-P1 report-exporter)

> **시연 픽스처 — 실계약 문서 아님.** 이 파일은 v0.8 Extension System 시연의 Task **EX-DP**(Plugins 수명주기) Execute 관측 기록이다. 실계약 문서가 아니다. 결함 없는 통과 케이스 관측이므로 "의도적 결함 정당 보유"는 해당 없음이다.
>
> **소관·경계.** 이 기록은 EX-DP 소유 경계(v0.8-demo-procedure §5.3 EX-DP 열)만 다룬다. 동시 병렬 집합 PS-4 의 형제 Task(EX-DH·EX-DS) 산출물은 참조·인용하지 않는다(07 R2). CP2 검증 리포트(verify-p.md)·loop-data(v08-demo-p.jsonl)는 각각 Verifier·Advisor 소관이며 이 Task 가 생성하지 않는다.
>
> **실측 기반(L-07).** 아래 모든 상태 서술은 파일 시스템 직접 실측(md5sum·find·grep) 후 기입했다. md5·경로·건수는 실측 값이다.

---

## §0. 대상·정본

- **레퍼런스 Plugin F-P1** = report-exporter (Advisor 확정 DP-E2 · 10 §8 예1 동형). id=report-exporter · version=1.0 · provides=[Module Manifest(contract=ReportExporterInterface)] 1건 · requires=[] · dependsOn=[] · frameworkCompat=">= v0.8"(현행 포함). 독립 Module 1개 번들(Hook/Skill 미번들).
- **정본:** 연산 규칙 = plugin-lifecycle.md §3(I1~I5·A1~A2·D1·R1~R2·IG), 물리 실현 = plugins-binding §3~§5, 포맷 = plugin-manifest.md §2·§3 / 10 §3.2, Register/Resolve/Deregister 방식 = runtime-binding §3.2. 이 기록은 계약을 재정의하지 않고 검사 관측 결과만 남긴다.

## §1. 설치 이전 스냅샷 (본체 기준선 — 10 INV-3)

framework/plugins/ 실측 파일 목록(baseline):

| 파일 | md5 (설치 이전) |
|---|---|
| framework/plugins/module-manifest.md | 43e33be776fd37597285388c7f9986b1 |
| framework/plugins/plugin-lifecycle.md | b7a60fa185ad2ce49f7459bb2e1fe921 |
| framework/plugins/plugin-manifest.md | 41787425813df444f9c928ca46a1915d |

- 하위 디렉터리: 0개 (설치본 자리 report-exporter/ 부재).

## §2. bundle 원본 (존치 산출물 — 레퍼런스 Plugin 1 정본 실물)

docs/v0.8-demo-fixtures/report-exporter/ (self-contained, 내부 Core/Adapter 경계 유지):

| 파일 | 역할 | md5 |
|---|---|---|
| plugin-manifest.md | Plugin Manifest 6필드 배포 서술자 | 4398a34c7cba727f03f847c3dbd5181c |
| core/report-exporter-module.md | 포함 Module (AI 비의존, contract=ReportExporterInterface) — Core 경계 | ed56b664647f938c9ecf05687dabc560 |
| bundle-note.md | 자기완결 선언 + Core/Adapter 경계 안내(픽스처 메타) | b801d451a4429abfab787846059d4f19 |

- Adapter 경계: 미사용 — AI 비의존 문서형이라 AI 의존 바인딩 산출물 없음(DP-E2, plugins-binding §3.1 ⓓ 구조만 확정).
- 배포 payload: plugin-manifest.md + core/report-exporter-module.md (bundle-note.md 는 픽스처 메타로 payload 아님).

## §3. INSTALL — 검사 관측 (I1~I5·IG) · 본체 diff 0

| 검사 | 판정 | 관측 근거 (실값) |
|---|---|---|
| I2 Framework 호환 | 예 | frameworkCompat=">= v0.8" 이 현행 v0.8 포함. |
| I3 의존 Plugin 기설치 | 예 | dependsOn=[] 전수 0건 → 공진리 성립. |
| I4 plugin id 유일 | 예 | 설치본 디렉터리명 report-exporter 가 기설치 하위 디렉터리(baseline 0개)와 충돌 없음. |
| I5 자기완결 | 예 | 배포 payload(plugin-manifest.md+core/) 전수 스캔: 선언(requires·dependsOn) 밖 본체 내부 파일 경로 은닉 의존 0건. 계약 정본은 spec 절 포인터로만 지시. (검사 범위 정직 — §7 주.) |
| IG 격리 불변 | 예 | (INV-5) Memory 백엔드 직접 접근 토큰 0 — 포함 Module 은 Memory 미소비(우회 불가·공진리). (INV-4) AI 모델명·제품 기능 토큰 0 — Core 배치 AI 비의존. (INV-6) 역할 경계 재정의·우회 지시 0(§3 문장은 준수 선언 부정문). |
| I1 본체 불가침 | 예 | 설치본 framework/plugins/report-exporter/{plugin-manifest.md, core/report-exporter-module.md} 배치(새 하위 디렉터리 추가만). 기존 3문서 md5 무변경, framework/core·framework/runtime·specs 무접촉. |

- Install 성립 = I1∧I2∧I3∧I4∧I5 전부 예 + IG 예. 상태 = registered-but-inactive.

## §4. ACTIVATE — Register/Resolve 경유 (A1·A2) · 새 contract 바인딩 동작 (INV-2)

| 검사 | 판정 | 관측 근거 (실값) |
|---|---|---|
| A1 provides 등록 (Register) | 예 | provides Module 정의 파일 배치 = Register 규약 실현(runtime-binding §3.2). module id report-exporter-module 유일성: 기존 등록 Provider Module id {memory-service-provider, verifier-provider, loop-provider, workflow-provider, plugins-provider}와 충돌 0. 반환 핸들 = {id=report-exporter-module, contract=ReportExporterInterface}. |
| A2 requires 해소 (Resolve) | 예 | Plugin Manifest requires=[] → 해소 대상 0건 → 전수 해소 공진리(vacuously true) 성립. UnresolvedContract 미발생. |

- INV-2 Register/Resolve 경유 — 새 기능 동작: Activate 후 Resolve(ReportExporterInterface) 가 활성 바인딩 정확히 1개(report-exporter-module)로 반환. 설치본에서 Module Manifest contract 필드로 ReportExporterInterface 를 선언한 정의 파일 = 1개(계약당 단일 바인딩 INV-3 정합). plugin-manifest.md 는 provides 에서 참조만(활성 바인딩 아님).
- 동작 실증(worked example, 형태 A): export(records, spec) 적용 — records=[{a,X,3},{b,Y,5},{c,X,2}], spec={정렬 value desc, 그룹 category, 요약 value 합계} → report: group X: a(3),c(2) 요약 sum=5 · group Y: b(5) 요약 sum=5. 완료 조건 (1)정렬 (2)그룹핑 (3)그룹별 요약 1줄 충족 → 새 contract 바인딩 실제 동작.

## §5. DEACTIVATE — D1 (역순 Deregister 바인딩 해제·비침범)

| 검사 | 판정 | 관측 근거 |
|---|---|---|
| D1 비활성화 완결 | 예 | (i) provides=[report-exporter-module] 1개 역순 비활성화(단일 Module 역순 자명). (ii) contract 바인딩 해제(01 Deregister) → ReportExporterInterface 이후 Resolve 대상 아님. (iii) 비침범: ReportExporterInterface 에 requires 로 의존하는 다른 활성 Module 0건 → Deregister 거부 조건 미해당. |

- 상태 → registered-but-inactive. 설치본 파일은 Remove 까지 잔존(비활성화 ≠ 파일 삭제).

## §6. REMOVE — R2 게이트 → 제거 → R1 잔여물 0 (설치 이전 목록 전수 대조)

| 검사 | 판정 | 관측 근거 (실값) |
|---|---|---|
| R2 의존 Plugin 부재 | 예 | report-exporter 에 dependsOn 으로 의존하는 다른 Plugin Manifest 0건(정밀 재검사). (검사 범위 정직 — §7 주.) |
| R1 잔여물 0 | 예 | 설치본 rm -rf 후 설치 이전 목록과 전수 대조 차집합 = 0. |

R1 전수 대조 (plugins-binding §3.3 · DP-E6 ⓒ):

- (1) 설치 이전 = {module-manifest.md, plugin-lifecycle.md, plugin-manifest.md}, 하위 디렉터리 0.
- (2) 제거 후 재열거 = {module-manifest.md, plugin-lifecycle.md, plugin-manifest.md}, 하위 디렉터리 0.
- (3) 차집합(추가 잔여물 / 소실 본체) = 0 / 0 (총 0항목).
- (4) 전 부류 전수: 배치 파일 → framework/plugins/report-exporter/ 부재(제거됨); 등록 Module → framework/plugins/ 내 ReportExporterInterface 정의 0건; 배선 → .claude/ AI 의존 산출물 미생성(DP-E2)이라 배선 잔여 0.
- (5) 기존 3문서 md5 무변경(43e33be7…/b7a60fa1…/41787425… 일치).
- Remove 성립 = R2∧R1 전부 예. 본체 = 설치 이전 상태와 동일(잔여물 0, INV-3).

## §6.6 본체 diff 0 — 최종 전수 대조 (ROADMAP ② · 10 INV-1)

- 본체 부류 전수: framework/plugins/ 3문서 md5 무변경 · framework/core·framework/runtime·specs 무접촉(세션 시작 이후 변경 0) · loop-data 6파일만 실재(v08-demo-p.jsonl 미생성) · memory-data 47건 무변경 · .claude/hooks·.claude/skills 무접촉.
- 순증가 판정: 설치본 framework/plugins/report-exporter/ 는 Install 로 추가되었다가 Remove 로 제거되어 최종 순증가 0. 존치 추가분은 선언된 시연 산출물(bundle 원본 + 본 관측 기록)뿐이며 기존 파일 변경 0 → 본체 diff = 0(예).

## §7. 정직 주 (검사 범위 정직·경계·false positive 처리)

- I5 정본 citation 처리. bundle 초안의 문서형 정본 파일 경로 citation 을 자기완결 스캔이 표면화했다. 문서 식별자(provenance 포인터)이지 기능적 은닉 의존이 아니나(plugin-manifest.md §4 분류), 모호성 제거를 위해 배포 payload 에서 파일 경로 형태를 제거하고 spec 절 포인터로 대체해 은닉 의존 0을 확정했다. provenance 서술은 bundle-note.md(픽스처 메타·payload 아님)에만 남는다.
- IG INV-6 / R2 false positive. 초기 느슨한 정규식 스캔이 (a) Module 준수 선언 부정문("재정의·우회하지 않는다")과 (b) 절차서의 F-P1 서술 라인을 표면화했다. 정밀 재검사로 둘 다 실제 위반/의존이 아님을 확정했다(단일 스캔 하나로 결론 내지 않고 부류·문맥 재대조).
- 공유 픽스처 경계. docs/v0.8-demo-fixtures/ 는 PS-4 세 Task 공유이나 파일 단위 소유 비중첩(§5.3). 이 Task 생성/수정 파일은 report-exporter/ 서브트리(+본 기록)뿐이며 형제 Task 의 ex-dh-*·ex-ds-*·f-h*·F-S*·mock-context* 파일은 생성·수정하지 않았다(R4·R2).
- 자기 점검은 최종 승인이 아니다. 이 기록은 CP1(Worker 자체 점검) 산출이며, 독립 판정은 CP2(Verifier·verify-p.md), 최종 승인은 CP3(Advisor) 소관이다(02 §3.2-A).
