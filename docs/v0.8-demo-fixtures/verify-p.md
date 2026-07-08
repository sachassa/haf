# docs/v0.8-demo-fixtures/verify-p — EX-DP(Plugins 수명주기) CP2 독립 검증 리포트

작성일: 2026-07-06
상태: v0.9 Baseline (개정 — 시점 스냅샷 후기 추기 · 사용자 승인 2026-07-06). 직전 기준선: CP2 독립 판정 산출물 (v0.8 PS-4 · Task EX-DP)
상위 규약: AGENT.md
스키마 정본: specs/06-verifier.md §3.2-A(리포트 6필드)·§3.2-B(항목별 판정 5필드·판정 값 3종)·§3.2-C(최종 판정 결정적 도출)·§3.2-E(검증 유형 VT-1~VT-5)·§3.2-F(거짓 완료 보고 검출). framework/verifier/verification-report.md 인스턴스.
판정 대상 정본: specs/10-plugins.md §3·§7·§8 예1, framework/plugins/plugin-manifest.md·plugin-lifecycle.md, framework/adapters/claude/plugins-binding.md §3~§5, docs/v0.8-demo-procedure.md §2.4·§5.3·§6.3·§8.

> **이 리포트는 CP2 독립 판정 산출물이다.** Worker self_check(docs/v0.8-demo-fixtures/ex-dp-lifecycle.md, CP1)를 판정 근거로 삼지 않고 검사 대상(claim)으로만 받았으며(06 V1·INV-1), 산출물 자체를 직접 실측(find·md5sum·grep)해 독립 재판정했다(06 §3.2-F). 최종 승인(CP3)은 Advisor 소관이며 이 리포트는 그 입력이다(02 §3.2-A). `final_verdict = Pass`는 Verifier의 정상 완료 출력이다.

---

## §1. target (판정 대상)

- **대상 작업 식별자:** EX-DP (v0.8 Extension System 시연 병렬 집합 PS-4 — Plugins 수명주기 확장 시연).
- **판정 대상 산출물:**
  - `docs/v0.8-demo-fixtures/report-exporter/` (F-P1 bundle 원본, 존치 산출물):
    - `plugin-manifest.md` (Plugin Manifest 6필드 배포 서술자)
    - `core/report-exporter-module.md` (포함 Module, contract=ReportExporterInterface — bundle 내부 Core 경계)
    - `bundle-note.md` (자기완결 선언 + Core/Adapter 경계 안내 — 픽스처 메타)
  - `docs/v0.8-demo-fixtures/ex-dp-lifecycle.md` (EX-DP Execute 관측 기록 — CP1 self_check, 참고 입력)
  - `framework/plugins/report-exporter/` **부재** (Remove 산출물 — 부재 자체가 판정 대상, criterion 3)
- **참고 입력(판정 근거 아님):** ex-dp-lifecycle.md의 완료 주장(§1~§6.6). 06 V1에 따라 claim으로만 받고 직접 재실측으로 판정했다.

---

## §2. criteria_basis (대조 기준 출처)

위임 input이 지정한 EX-DP 완료 조건(done) 6항 + 정합 확인 4건. 판정 기준의 정본은 아래 출처이며 본 리포트는 재정의하지 않는다(06 INV-2 — 기준 있는 판정).

| 부류 | 대조 기준 | 출처 정본 |
|---|---|---|
| 완료 조건 (done) | EX-DP done 6항 (§3 C-1~C-6) | 위임 input · docs/v0.8-demo-procedure.md §6.3·§8-D(Plugins) · specs/10-plugins.md §7 |
| 규격 정합 | Plugin Manifest 6필드 포맷 | framework/plugins/plugin-manifest.md §2 · specs/10-plugins.md §3.2-A |
| 규격 정합 | 네 연산 검사 I1~I5·A1~A2·D1·R1~R2·IG | framework/plugins/plugin-lifecycle.md §3 · specs/10-plugins.md §3.1 |
| 물리 실현 정합 | 형태 A granularity·물리 절차 | framework/adapters/claude/plugins-binding.md §3~§5 (Advisor 승인 OQ-DP-1) |
| 시연 절차 정합 | §2.4·§6.3 EX-DP 행 | docs/v0.8-demo-procedure.md §2.4·§5.3·§6.3·§8 |
| 경계 규칙 | bundle 내부 Core/Adapter 경계 AI 비의존(INV-4)·격리(INV-5/6)·자기완결(INV-8) | specs/10-plugins.md §3.3 INV-1~INV-10 |

**Advisor 제공 사실(판정 조정 반영):** (a) `.claude/agents/planner.md`·`verifier.md` 변경 = EX-R3 귀속 → 본 diff 판정에서 제외. (b) 픽스처 경계(`docs/v0.8-demo-fixtures/`) 물리 토큰은 정당 보유 → verifier_scope 제외. (c) specs/10 §3 본문 AI 비의존 전수 스캔은 마일스톤 CP2 소관 → 본 리포트 대상 아님. 단 **bundle 내 `core/` 파일의 AI 비의존(INV-4·bundle 내부 Core/Adapter 경계)은 본 판정 대상**이다.

---

## §3. items (항목별 판정)

각 항목: `criterion` / `verdict`(충족 Met · 위반 Violated · 판정 불가 Undetermined) / `evidence`(근거) / `scope`(검사 범위) / `verification_type`(VT-1~VT-5). 판정은 Verifier 직접 실측에 근거한다.

| # | criterion | verdict | verification_type |
|---|---|---|---|
| C-1a | 본체 diff 0 — `framework/plugins/` 기존 3문서 무변경(실측) | 충족(Met) | VT-1·VT-4 |
| C-1b | Install·Activate만으로 ReportExporterInterface 바인딩 동작 — Register 기록·Resolve 반환·worked example(형태 A) | 충족(Met) | VT-2·VT-5 |
| C-2 | Activate = 01 Register/Resolve 규약 경유(A1·A2, requires=[] 공진리) | 충족(Met) | VT-2·VT-3 |
| C-3 | Remove 후 잔여물 0 — 설치 이전 목록 전수 대조 + 현재 3문서만 잔존(직접 재실측) | 충족(Met) | VT-1·VT-4 |
| C-4a | bundle 자기완결(I5) — payload 은닉 의존 0 | 충족(Met) | VT-4 |
| C-4b | 격리 IG — INV-4 Core AI 비의존 + INV-5 Memory 단일 Port + INV-6 역할 경계 | 충족(Met) | VT-4 |
| C-5 | 전 산출 EX-DP 경계 안(§5.3)·경계 밖 수정 0 | 충족(Met) | VT-4 |
| C-6 | 실측 근거 기반 — 관측 기록 md5·건수 주장 재검증 | 충족(Met) | VT-2 |
| J-A | F-P1 plugin-manifest.md ↔ framework/plugins/plugin-manifest.md §2·10 §3.2-A 6필드 포맷 정합 | 충족(Met) | VT-3 |
| J-B | F-P1 관측 기록 ↔ plugin-lifecycle.md §3 검사 I1~I5·A1~A2·D1·R1~R2·IG 정합 | 충족(Met) | VT-3 |
| J-C | 절차서 §2.4·§6.3 EX-DP 행 정합 | 충족(Met) | VT-3 |
| J-D | 형태 A granularity(Install=배치·비활성/Activate=바인딩 활성/Deactivate=해제/Remove=삭제) OQ-DP-1 정합 확인 | 충족(Met) | VT-3 |

### 항목별 근거·범위 상세

**C-1a — 본체 diff 0 (framework/plugins/ 3문서 무변경).** verdict = 충족(Met).
- evidence: Verifier가 `framework/plugins/`를 직접 재열거·md5 측정 — 3파일이 관측 기록 §1 baseline과 **정확히 일치**: `module-manifest.md`=43e33be776fd37597285388c7f9986b1, `plugin-lifecycle.md`=b7a60fa185ad2ce49f7459bb2e1fe921, `plugin-manifest.md`=41787425813df444f9c928ca46a1915d. 하위 디렉터리 0개. 추가로 `framework/`·`.claude/` 전역에 `report-exporter` 참조 0건(grep) → Install/Remove가 본체에 남긴 흔적 0. INV-1(본체 불가침) 충족.
- scope: `framework/plugins/` 전 파일 md5 대조(직접 재실측) + `framework/`·`.claude/` report-exporter 문자열 전수 스캔. framework/core·runtime·specs의 세션 시작 대비 byte-level diff는 버전 이력 부재로 독립 재측정 불가 — 단 위임이 C-1의 본체 diff를 "framework/plugins/ 3문서 무변경 실측"으로 명시 한정했고, report-exporter 누출 0으로 교차 확인함(§5 참조).

**C-1b — Install·Activate 바인딩 동작.** verdict = 충족(Met).
- evidence: Register 기록 — 관측 기록 §4 A1이 report-exporter-module 등록·반환 핸들 {id=report-exporter-module, contract=ReportExporterInterface} 기록. Resolve 반환 — Resolve(ReportExporterInterface)가 활성 바인딩 정확히 1개(report-exporter-module) 반환. worked example — §4가 export(records, spec) 적용을 서술: records=[{a,X,3},{b,Y,5},{c,X,2}], spec={정렬 value desc·그룹 category·요약 value 합계}. **Verifier 재계산 검산:** 그룹 X={a(3),c(2)} value desc 정렬 3>2 ✓, 합계 3+2=5 ✓; 그룹 Y={b(5)} 합계 5 ✓ → 관측 결과 "group X: a(3),c(2) sum=5 · group Y: b(5) sum=5"와 일치. core/report-exporter-module.md §2 완료 조건(정렬·그룹핑·그룹별 요약 1줄)과 정합.
- scope: 관측 기록 §4 Register/Resolve 서술 + worked example 산술 독립 검산. **형태 A(Bootstrap) 명시:** 이 "동작"은 라이브 코드 실행이 아니라 규약 실현(형태 A) 상의 문서화된 worked example이다(plugins-binding §0, OQ-DP-1 Advisor 승인). 형태 A 수준에서 Register 기록·Resolve 반환·worked example 세 요소가 모두 존재하고 내부 정합하므로 충족. 라이브 실행 관측은 형태 B 도입 시점 대상(검사 범위 밖 — 정직 명시).

**C-2 — Activate Register/Resolve 경유.** verdict = 충족(Met).
- evidence: 관측 기록 §4 — A1(provides Register): provides Module 정의 배치 = Register 규약 실현(runtime-binding §3.2), module id 유일성(기존 Provider id {memory-service-provider, verifier-provider, loop-provider, workflow-provider, plugins-provider}와 충돌 0). A2(requires Resolve): Plugin Manifest requires=[] → 해소 대상 0건 → 전수 해소 **공진리(vacuously true)** 성립, UnresolvedContract 미발생. INV-2(Register/Resolve 경유) 충족. plugin-lifecycle.md §3.3 A1·A2 규칙과 정합.
- scope: 관측 기록 §4 A1·A2 서술 ↔ plugin-lifecycle.md §3.3·specs/10 §3.1 Activate 완료 조건 대조. requires=[] 값은 bundle plugin-manifest.md §2에서 직접 확인.

**C-3 — Remove 잔여물 0.** verdict = 충족(Met). (**직접 재실측 — 최강 근거**)
- evidence: **Verifier 직접 재열거:** `framework/plugins/` = {module-manifest.md, plugin-lifecycle.md, plugin-manifest.md} 3파일만, 하위 디렉터리 0개, `report-exporter/` 설치본 **부재**. 관측 기록 §6 R1 전수 대조((1) 설치 이전 3문서 = (2) 제거 후 3문서 → (3) 차집합 0/0)의 결과 상태와 **정확히 일치**. 3문서 md5 무변경(C-1a). 추가로 `framework/` 전역 report-exporter 참조 0건(등록 Module·배선 잔여 부류 전수 스캔) → 전 부류(배치 파일·등록 Module·배선) 잔여물 0. INV-3(잔여물 0) 충족.
- scope: `framework/plugins/` 하위 전수 재열거(직접) + `framework/`·`.claude/` report-exporter 전수 grep(등록·배선 부류). 좁은 대리 지표 아님 — 배치 파일(디렉터리 부재)·등록/배선(문자열 0건) 두 부류를 각각 실측(06 V4·VT-4).

**C-4a — bundle 자기완결(I5).** verdict = 충족(Met).
- evidence: 배포 payload(plugin-manifest.md + core/report-exporter-module.md) Verifier 직접 스캔 — core/ 파일은 본체 내부 경로(framework/·specs/·.claude/·docs/) 참조 0건(grep 무매칭). bundle plugin-manifest.md는 본체 내부 파일 경로 대신 spec 절 포인터(10 §3.2-A·01 §3.2-A 등, provenance)만 사용하고, 유일한 파일 경로는 `core/report-exporter-module.md`(bundle **내부** 자기 설치본 대상, 은닉 의존 아님)뿐. 선언(requires·dependsOn) 밖 본체 내부 경로 은닉 의존 0 → INV-8 충족. plugin-lifecycle.md §3.2 I5와 정합.
- scope: payload 2파일 전체 grep(본체 내부 경로 패턴 전수). bundle-note.md는 픽스처 메타(payload 아님)이므로 I5 payload 검사 대상 밖 — 정직 구분.

**C-4b — 격리 IG (INV-4/5/6).** verdict = 충족(Met).
- evidence: **INV-4 (Core AI 비의존, 본 판정 대상):** `core/report-exporter-module.md` Verifier 직접 전수 스캔 — AI 모델명·제품 기능명·언어명·툴체인명·직렬화 형식명·물리 경로·확장자 토큰 **0건**(grep 무매칭). 순수 자료 변환 서술만 존재. **INV-5 (Memory 단일 Port):** core 모듈은 영속성 백엔드 접근 지점 0(Memory 미소비) → 우회 발생 불가·공진리 성립. **INV-6 (역할 경계):** core §3이 Agent 역할 경계 재정의·우회 0을 부정문으로 선언, 리포트 변환 능력만 제공. IG = INV-4∧INV-5∧INV-6 전부 예 → IsolationViolation 0. plugin-lifecycle.md §3.6과 정합. (bundle-note.md line 21의 `.claude/` 토큰은 픽스처 메타의 mention — "AI 의존 바인딩이 있다면 격리되어야 하나 이 Plugin은 AI 비의존이라 산출물 없음" — Core payload 아님, use 아님.)
- scope: core/ 파일 AI 의존 토큰 부류별 전수 grep + Memory 접근 지점·역할 경계 서술 판독. 판정 대상은 bundle 내부 Core 경계(Advisor 지정). specs/10 §3 본문 AI 스캔은 마일스톤 CP2 소관(제외).

**C-5 — 전 산출 EX-DP 경계 안·경계 밖 수정 0.** verdict = 충족(Met).
- evidence: EX-DP 실 산출 = `docs/v0.8-demo-fixtures/report-exporter/` 서브트리 + `ex-dp-lifecycle.md` — 둘 다 §5.3 EX-DP 소유 열 안(직접 열거 확인). 경계 밖: framework/plugins/ 3문서 md5 무변경(C-1a), framework/·.claude/ report-exporter 누출 0(C-3). 형제 픽스처(ex-dh-*·ex-ds-*·f-h2/3/4·F-S2/F-S3·mock-context-*)는 실재하나 파일명 네임스페이스가 EX-DP 산출과 비중첩(쌍별 교집합 0, §5.3) — EX-DP 산출이 형제 네임스페이스에 침범한 흔적 0. `.claude/agents/planner.md`·verifier.md 변경은 EX-R3 귀속(Advisor 제공 사실 — 제외).
- scope: docs/v0.8-demo-fixtures/ 전 파일 열거로 EX-DP 산출 경계 봉쇄 확인 + framework/plugins/ md5 + report-exporter 누출 grep. **정직 한계:** 형제 소유 픽스처 파일의 byte-level 무수정은 버전 이력 부재로 독립 재측정 불가 — 단 파일 소유 경계 비중첩(네임스페이스 분리)과 EX-DP 산출의 경계 내 봉쇄는 실측 확인됨. 경계 밖 수정의 실측 대상(본체 framework/plugins/)은 무변경 확정.

**C-6 — 실측 근거 기반.** verdict = 충족(Met).
- evidence: 관측 기록의 상태 서술(md5·경로·건수)을 Verifier가 독립 재실측한 결과 **전부 일치**: §1 baseline md5 3건 일치, §2 bundle md5 3건(4398a34c…·ed56b664…·b801d451…) 일치, §6 R1 제거 후 3문서만 잔존 상태 일치. 즉 관측 기록은 실측 기반(L-07 준수)이며 조작·과장 없음. 거짓 완료 보고 아님(06 §3.2-F — claim ↔ 실측 모순 0).
- scope: 관측 기록 §1·§2·§6 정량 주장(md5 6건·파일 건수·차집합) 전건 재측정 대조.

**J-A — Plugin Manifest 6필드 포맷 정합.** verdict = 충족(Met).
- evidence: bundle plugin-manifest.md 6필드 = {id, version, provides, requires, dependsOn, frameworkCompat}, 필수 표기 4예(id·version·provides·frameworkCompat)·2아니오(requires·dependsOn 기본 없음). framework/plugins/plugin-manifest.md §2·specs/10 §3.2-A 정본 표와 필드명·순서·필수/선택 표기 **완전 일치**. 값: id=report-exporter, version=1.0, provides=[Module 1건→core/report-exporter-module.md contract=ReportExporterInterface], requires=[], dependsOn=[], frameworkCompat=">= v0.8" — specs/10 §8 예1 인스턴스와 동형. 새 Config scope 미도입(INV-7) 준수.
- scope: bundle plugin-manifest.md ↔ 포맷 정본 2건 필드·표기 대조.

**J-B — 네 연산 검사 I1~IG 정합.** verdict = 충족(Met).
- evidence: 관측 기록 §3~§6이 I1(본체 불가침)·I2(frameworkCompat 포함)·I3(dependsOn=[] 공진리)·I4(id 유일)·I5(자기완결)·IG(격리)·A1(provides Register)·A2(requires=[] Resolve 공진리)·D1(역순 Deactivate·바인딩 해제·비침범)·R2(dependent 부재)·R1(잔여물 0)을 각각 예로 관측한 근거가 plugin-lifecycle.md §3.1~§3.6 각 검사 규칙·판정 형태·reason 결합과 정합. 각 검사의 "예" 판정이 대응 완료 조건(10 §3.1)과 1:1 대응.
- scope: 관측 기록 11개 검사 서술 ↔ plugin-lifecycle.md §3 검사표 대조.

**J-C — 절차서 §2.4·§6.3 EX-DP 행 정합.** verdict = 충족(Met).
- evidence: 절차서 §2.4(EX-DP: F-P1 Install·Activate + 본체 diff 0·Register/Resolve·Remove R1 잔여물 0·IG·I5)·§6.3(EX-DP 기대 Pass — Install I1~I5·IG·Activate A1/A2 반환 핸들·Remove R1 잔여물 0 전수 대조 충족; verifier_scope = F-P1 bundle 원본·설치본·v08-demo-p.jsonl; AI 비의존 스캔 대상 specs/10 §3·픽스처 경계 제외)의 EX-DP 기대와 관측 기록·본 판정 결과가 정합. 절차서 기대 판정(Pass)과 본 리포트 도출(Pass) 일치.
- scope: 절차서 §2.4·§6.3 EX-DP 행 ↔ 관측 기록·본 판정 대조.

**J-D — 형태 A granularity 정합 확인 (OQ-DP-1).** verdict = 충족(Met).
- evidence: 관측 기록 4연산 granularity — Install=설치본 배치·registered-but-inactive(§3), Activate=Register/Resolve 바인딩 활성(§4), Deactivate=바인딩 해제·registered-but-inactive(§5), Remove=삭제·잔여물 0(§6) — 이 plugins-binding §3.2 물리 절차·plugin-lifecycle.md §2 연산 인터페이스와 정합. Advisor 승인 사항(OQ-DP-1)이므로 재평가가 아닌 **정합 확인만** 수행 — 관측 granularity가 승인된 형태와 일치함을 확인.
- scope: 관측 기록 §3~§6 연산 서술 ↔ plugins-binding §3.2·plugin-lifecycle.md §2 대조(정합 확인 한정, 재평가 아님).

---

## §4. final_verdict (최종 판정 — 결정적 도출, 06 §3.2-C·INV-5)

**Pass (통과).**

도출: items 12건 전부 충족(Met) → 06 §3.2-C "모든 항목이 충족 → 통과(Pass)" 규칙으로 결정적 도출. 위반(Violated) 0건, 판정 불가(Undetermined) 0건.

| 판정 값 | 건수 |
|---|---|
| 충족(Met) | 12 |
| 위반(Violated) | 0 |
| 판정 불가(Undetermined) | 0 |
| **합계** | **12** |

**거짓 완료 보고 검출(06 §3.2-F) 결과: 검출 0건.** Worker self_check(ex-dp-lifecycle.md) 주장을 신뢰하지 않고 md5 6건·파일 건수·차집합·worked example 산술·core AI 비의존을 독립 재측정한 결과, claim과 실측의 모순 0. 관측 기록은 정직한 실측 기반(L-07 준수)이며, 그 검사 범위를 넘어선 Verifier 전수 스캔(framework/·.claude/ report-exporter 누출 0, core/ AI 토큰 0)도 위반을 검출하지 않았다.

---

## §5. verifier_scope (실제 검사 범위 · 제외 범위)

**직접 실측·검사한 범위:**
- `framework/plugins/` 전 파일 재열거 + md5 측정(직접) — 3문서 무변경·report-exporter/ 부재 확인.
- `docs/v0.8-demo-fixtures/report-exporter/` bundle 3파일 md5 측정(직접) — 관측 기록 §2와 일치.
- `core/report-exporter-module.md` AI 의존 토큰 부류별 전수 grep — 0건(INV-4).
- bundle payload(plugin-manifest.md + core/) 본체 내부 경로 참조 전수 grep — 은닉 의존 0(I5).
- `framework/`·`.claude/`·`specs/` report-exporter 문자열 전수 grep — 본체 누출 0(specs/10 §8 예1 선재 참조 1건은 EX-DP 산출 아님).
- worked example(export) 산술 독립 재계산.
- 관측 기록 §1·§2·§6 정량 주장 전건 재측정 대조.
- bundle plugin-manifest.md ↔ 포맷 정본(framework/plugins/plugin-manifest.md §2·10 §3.2-A) 필드 대조.
- 관측 기록 검사 서술 ↔ plugin-lifecycle.md §3·plugins-binding §3~§5·절차서 §2.4·§6.3 정합 대조.

**검사하지 못했거나 제외한 범위(정직 명시 — 06 V4·INV-4):**
- **픽스처 경계·설치본 물리 토큰:** `docs/v0.8-demo-fixtures/` 픽스처 경계와 설치본 경로의 물리 토큰(경로·형식)은 정당 보유로 verifier_scope 제외(Advisor 제공 사실 b·DP-E7).
- **specs/10 §3 본문 AI 비의존 전수 스캔:** 마일스톤 CP2 소관(Advisor 제공 사실 c) — 본 리포트 대상 아님. 본 리포트의 AI 비의존 판정은 bundle 내 core/ 파일에 한정(INV-4).
- **`.claude/agents/planner.md`·verifier.md 변경:** EX-R3 귀속(Advisor 제공 사실 a) — diff 판정 제외.
- **framework/core·runtime·specs의 세션 시작 대비 byte-level diff:** 버전 이력 부재로 독립 재측정 불가. 위임이 C-1 본체 diff를 framework/plugins/ 3문서로 한정했고 report-exporter 누출 0으로 교차 확인함(C-1a·C-5). 이 범위 밖 본체 무변경은 확정하지 않는다.
- **형제 소유 픽스처(ex-dh-*·ex-ds-*·f-h*·F-S*·mock-context-*)의 byte-level 무수정:** 버전 이력 부재로 독립 재측정 불가. 파일 소유 경계 비중첩·EX-DP 산출 경계 봉쇄는 실측 확인(C-5).
- **라이브 실행 관측(형태 B):** 이 시연은 Bootstrap 형태 A 규약 실현이므로 Register/Resolve·export 동작은 문서화된 worked example로 판정(C-1b). 라이브 코드 실행은 형태 B 도입 시점 대상 — 검사 범위 밖.
- **EX-DP 미소산 파일:** `framework/adapters/claude/loop-data/v08-demo-p.jsonl`(Advisor 소관)·`verify-p.md`(본 리포트) 자체는 EX-DP Execute 산출물이 아니며 판정 대상 아님(관측 기록 §5 header note). loop-data는 v06/v07 6파일만 실재(v08-demo-p 미생성) 실측 확인.
- ※ **[v0.9 T7 개정 추기 — 관찰 1 해소·DP-U3(a)]** 위 "EX-DP 미소산 파일" 항의 실측("loop-data는 v06/v07 6파일만 실재·v08-demo-p 미생성")은 **EX-DP CP2 판정 시점**(시연 진행 중 — `v08-demo-p.jsonl`은 Advisor 소관으로 아직 미소산) 스냅샷이며, 판정 시점 무결성을 위해 문면을 보존한다(L-10). 시연(PS-4) 완결 후 직접 재실측(2026-07-06): `framework/adapters/claude/loop-data/`에 `v08-demo-h/s/p.jsonl` 3파일 **실재**(각 7 line — `v08-demo-p.jsonl` 포함, 기존 v06/v07 6파일과 병존). 이 파일은 CP2 판정 대상(EX-DP Execute 산출물)이 아니라 Advisor 소관 소산이므로, 본 리포트의 판정 결과(**final_verdict = Pass** · C-3 Remove 잔여물 0 · items 12/0/0)는 **불변**이다.

---

## §6. rework (재작업 지시)

**없음.** `final_verdict = Pass`이므로 재작업 지시가 필요하지 않다(06 §3.2-A·§3.2-D — Pass면 "없음"). 위반·판정 불가 항목 0건.

---

## §7. Lesson 후보 입력 (Learn 단계 제공 — 03 §3.2-C)

- 검출된 위반·거짓 완료 보고 0건 → 재발 방지 Lesson 후보 없음.
- **성공 패턴 후보(BP):** F-P1 단일 Module 번들 Plugin의 Install→Activate(바인딩 동작)→Deactivate→Remove(잔여물 0) 전 수명주기를 형태 A로 실측 기반 무결점 통과(CP2 첫 판정 Pass·충족 12/위반 0/판정 불가 0). 특히 잔여물 0을 Verifier 직접 재열거로 재검증한 절차(설치 이전 목록 전수 대조 + report-exporter 누출 grep 이중 확인)는 좁은 대리 지표 회피(06 V4)의 실증 — Best Practice 후보 입력. (Lesson 생성·회수 상세는 specs/05-lessons.md 소관·Memory Update는 Advisor 소관.)
