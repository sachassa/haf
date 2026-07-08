# UAHF Session Handoff — v0.9 → 다음 세션

작성일: 2026-07-06
작성자: Worker (Advisor 위임, Task T14)
목적: 이 문서만 읽어도 새 세션이 다음 마일스톤(v1.0)을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v0.8.md, v0.7, v0.6, v0.5, v0.4, v0.3, v0.2, v0.1)
상태: v0.9 Baseline (CP2 첫 판정 Pass 20/0/0 — v0.5부터 5연속 · CP3 승인 · 사용자 승인 2026-07-06). 사용자 승인 반영 완료 — Advisor가 v0.9 산출물 전건에 Baseline 행 append·상태 라인 승격(Glossary 0.2 Frozen 승격 포함)을 수행하고 본 문서 이력에 기록했다.

---

## §9. 이력 (Revision History)

| 일자 | 변경 | 주체 |
|---|---|---|
| 2026-07-06 | 최초 작성 (사용자 승인 대기 상태) | Advisor 위임 — Worker (Task T14) |
| 2026-07-06 | v0.9 Baseline 확정 — 사용자 승인 반영 (전 산출물 상태 라인 승격·Baseline 행 append·Glossary 0.2 Frozen 승격) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행(v0.9 verification-report·promotion-review·transition-judgment·demo 동형). 이후 개정은 이 표에 append-only로 기록한다. 사용자 승인 반영은 별도 행으로 append한다.)

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v0.9 — Adapter Layer & Scaffold)

1. **세션 진입 절차 이행** — handoff v0.8 정독 → **Consult 실수행(6회째 실가동)**: index.jsonl 56라인(착수 시점) 스캔, 회수 집합 = Active Lesson 14건(L-01~L-14) + BP 4건(BP-01~03·BPD-06) → 정본·운용 문서 정독(ROADMAP v0.9·specs/11·12·13·structure.md·framework/adapters/claude/ 전 바인딩·framework/workflow/) → **착수 전 실측**(specs 15파일·framework 8경계·라이브 표면 상태·loop-data 9파일·memory 56/56).
2. **Execution Plan 수립** — Planner 초안(15 Task·8 Wave·OQ 다수) → **Advisor 채택**·OQ 해소 → **사용자 승인**(2026-07-06, 계획 모드 — 사용자 결정 3건: **DP-U1 형태 A 유지**·**DP-U2 Glossary 편입**·**DP-U3 경미 정합 3건**).
3. **Wave 실행 (W1~W8)** —
   - **W1**: adapter-conformance(T1)·spec-versioning-policy(T2, r2 1회 — § 포인터 오기 게이트 C 검출·교정 폐합) — 병렬 2종.
   - **W2 (5병렬)**: agent-binding+harness-binding(T3)·scaffold 3산출물(T4 — scaffold-binding·scaffold-template/ 13파일·install-guide)·Presentation 2산출물(T5 — uahf-status·getting-started)·Glossary 0.2 Draft(T6)·시점 스냅샷 4곳(T7 — plugins/hooks-binding·v0.8-demo-procedure·verify-p).
   - **W3**: structure.md §8(T8)·v0.9-demo-procedure(T9)·adapter-conformance r2(T15 — W2 정식화 실재 반영 격리 갱신) — 병렬 3종.
   - **W4**: **Scaffold 시연 실구동**(T10 — 신규 프로젝트 픽스처 설치 → VerifyInstall(CK-1~8) → Bootstrap(Ready) → Loop 1사이클 → 멱등·기존 파일 보호·Uninstall 단일 흐름·**독립 Verifier CP2 실위임**(verify-scaffold.md — 구현/검증 주체 분리)·**Merge 불필요**: 단일 Task 채택(과분해 금지)).
   - **W5**: Harness 전이 재판정(T11).
   - **W6**: 마일스톤 CP2(T12).
   - **W7**: 승격 심사(T13).
   - **W8**: 본 핸드오프(T14).
4. **검증 리포트** — docs/v0.9-verification-report.md: **첫 판정 Pass 20/0/0 (v0.5부터 5연속)**, 완료 조건 ② 경계 전수 스캔 직접 수행·완료 조건 ③ 시연 독립 재관측(VT-5)·CK-8 md5 재계산·거짓 완료 보고 0건·비차단 관찰 6건(§3.7).
5. **Memory Update 실가동 6회차** — 심사 등록 5건(mi-0057~0061): **L-15 Active 승격·BPD-11 Candidate 보류·재발 판정 2건(둘 다 Novel)**. **store 61파일·index 61라인**, 기존 56건 무변경(append-only·바이트 수준 MD5 대조).

## 1.2 v0.9 완료 조건 대조 (ROADMAP — 전건 충족, T12 §3·§4 근거)

| 완료 조건 | 판정 | 근거 |
|---|---|---|
| ① Adapter Interface 최종 확정 | 충족 | adapter-conformance §2 BP-1~17 커버리지·§3 Conformance Report 6필드 verdict=**Valid(Full)**·11 §3.2-A/B/D 셀 대조(재정의 0)·specs/11 Frozen 무변경 (verification-report item #2) |
| ② Core에 Claude 의존 요소 0건 (경계 검증) | 충족 | Verifier 직접 전수 스캔 — framework/core·runtime·loop·memory·verifier·workflow·plugins **7 디렉터리군** 2패스 매치 0건 + 설치본 Core부(new-project/framework/core·runtime) CK-6 재스캔 0건 (item #3·§3.3) |
| ③ 새 프로젝트에 Scaffold 설치·루프 동작 시연 | 충족 | v09-demo-scaffold.jsonl **7 line** 직접 파싱(seq 1→7 단조·outcome 전건 pass·retry 0·**actor=human 0**·Consult→…→Complete 완주)·CK-1~8 Pass(8/0/0)·Bootstrap **state=Ready**·CK-8 md5 IDENTICAL (item #4·§3.6) |
| ④ Spec versioning·하위호환 규칙 문서화 | 충족 | spec-versioning-policy §3(개정 유형 A/B)·§4(하위호환 4항)·§5(첫 적용) + Glossary 0.2 개정이 정책 절차 준수(버전 상승·이력 append·추가=하위호환) (item #5) |

산출물 6종 충족(item #6): adapters/claude/ 완성본·Adapter Interface 최종 규격(adapter-conformance)·Scaffold 도구+템플릿(scaffold-binding+scaffold-template/ 13파일)·Presentation 최소 기능(uahf-status+getting-started)·설치 가이드(v0.9-install-guide)·versioning 정책(spec-versioning-policy).

## 1.3 이번 세션의 설계 결정 (전부 확정·기록)

| 결정 | 내용 | 상태 |
|---|---|---|
| **DP-U1** | **사용자 결정 — 형태 A 유지.** Scaffold 3연산(Install/VerifyInstall/Uninstall)은 Bootstrap에서 형태 A 문서 절차로 실현·무인 실행기(형태 B) 미도입. 이로써 전이 조건 3 미충족은 계획 수용 범위(T11 §5) | **사용자 결정 (2026-07-06)** |
| **DP-U2** | **사용자 결정 — Glossary 편입.** Wave·Baseline·형태 A/B 표제어 3건을 Glossary §3.2-G에 추가(0.2 Draft) — versioning 정책 첫 적용(추가=하위호환) | **사용자 결정 (2026-07-06)** |
| **DP-U3** | **사용자 결정 — 경미 정합 3건.** (a) Frozen specs 계수 15 정본화 확정(종전 "16종"은 오기 — DP-U3(c)) (b) F-H1 manifest `contract: HookModule` 인스턴스 값 채택(v0.8 CP2 관찰 2 해소 — DP-U3(b)) 등 | **사용자 결정 (2026-07-06)** |
| **DP-A1** | conformance = 인스턴스 판정(adapter-conformance가 11 §3 계약을 재정의 않고 Claude 실현 커버리지·Conformance Report 인스턴스만 산출) | 확정 |
| **DP-A2** | `adapters/claude/` 표기 = 물리 경로 `framework/adapters/claude/` 축약 해소(Frozen 11 무변경) | 확정 |
| **DP-A3** | `framework/scaffold/` **미신설** — Scaffold는 Bootstrap 이전 설치 도구(12 §5)이지 Module 구현 디렉터리 아님. framework/ 하위 = 8경계 유지 | 확정 |
| **DP-A(구조)** | harness-binding을 agent-binding에서 **분리**(별도 파일)·T15 신설(conformance r2 격리 갱신)·T7 시점 스냅샷 ⓓ **후기 추기 방식**·OQ-T9-1 해소(시연 = **단일 사이클** + 설치본 실소비 근거)·OQ-T13-1 해소(**계수 실측 정본 확정** — 위임문 계수 편차는 실측값 기입·정직 표면화) | 확정 |

**주요 OQ 해소**: OQ-AC-1(정식화 실재 반영 T15)·OQ-T9-1(단일 사이클)·OQ-T13-1(계수 실측)·OQ-HB-1(전이 판정 T11 이연 이행)·OQ-TJ-1(Glossary v0.2 승인 무관 조건 1 충족).

## 1.4 검증 게이트 실동작 기록

- **마일스톤 수준**: 실서브에이전트 위임 다회(Planner·Worker·Verifier — Verifier·Planner 위임은 `model: opus` DP-E8) + **재개정 라우팅 1회**(T2 r2 — 문서 내 자기 참조 § 포인터 오기 "§3.3↔§3.4", 게이트 C 검출·교정 폐합) + **격리 갱신 1회**(T15 — W2 정식화 후 adapter-conformance §2·§4·§6 실재 반영, 재작업 아님). 거짓 완료 보고 0건. **CP2 첫 판정 Pass 20/0/0 — v0.5부터 5연속.**
- **시연 수준(실물)**: T10 Scaffold 시연 **단일 사이클** 실위임(Worker Execute + 독립 Verifier CP2 실위임 — 구현/검증 주체 분리 실증). loop-data v09-demo-scaffold.jsonl 7 line 전건 actor ∈ {Advisor, Worker, Verifier}, **actor=human 0건**.
- **T2 r2 결함**: spec-versioning-policy §9 하단 주석이 L-10 명문화 위치를 "§3.3"으로 지칭(실위치 §3.4 — §3.3은 상태 승격 절차) → Advisor 게이트 C 검출 → r2 교정 폐합 → **재발 판정 Novel**(기존 Active Lesson 매칭 없음, mi-0060).
- **Advisor 위임문 계수 편차(같은 세션 3회 실증)**: T7 input "10파일" ↔ 실측 32파일/7디렉터리 · T11 위임문 "4건" ↔ 열거 라벨 5종 · T13 위임 "기존 14/총 15" ↔ 실측 "기존 13/총 14". 각각 수임자가 추측 없이 실측 대조·open_questions 에스컬레이션으로 비차단 폐합 → **L-15 Active 승격**(mi-0058)·**재발 판정 Novel**(mi-0061 — L-12 존재 전제는 회수됐으나 계수·규모 전제 미커버 → RecallGap 아님·Novel).

## 1.5 Lesson·BP — 정식 등록 경로 처리 완료

- **Active 집합: Lesson 15건(L-01~L-15)·Best Practice 4건(BP-01·BP-02·BP-03·BPD-06)**, store 61파일·index 61라인.
- **L-15 Active**(mi-0057 Candidate → mi-0058 Active, supersedes mi-0057): "Advisor 위임문에 쓰는 계수·규모·상태 전제 값(파일 수·항목 수·집합 규모 등)은 발신 전 파일 시스템 실측으로 대조하라 — 존재 전제(L-12)·본문 문안(L-11)과 같은 깊이로." 승격 근거 = 동일 부류 **세션 내 3회 실증**(T7 10↔32·T11 4↔5·T13 14↔13)·기존 Active(L-11 문안·L-12 존재 전제) 미커버(계수·규모 축)·v0.8 L-14 즉시 승격 선례 동형. L-15가 등록되는 바로 그 T13 사이클에서 위임 input 계수 편차가 재현·폐합된 라이브 실증.
- **BPD-11 신규 Candidate 보류**(mi-0059): "신규 프로젝트 설치→Bootstrap→Loop 1사이클을 단일 흐름 시연으로 완주하고 설치본 문서를 사이클 실소비 입력으로 기록하면 설치 실증과 루프 실증이 한 사이클에서 성립한다." v0.8 BPD-07~10 관례 동형(시연 유래 Candidate 보류, 실무 동형 재발 시 재상정).
- **재발 판정 2건 — 둘 다 Novel**(mi-0060 T2 r1 § 포인터 오기·matched 없음 / mi-0061 위임문 계수 오기·matched 없음, was_recalled=L-12이나 계수 전제 미커버로 Novel).
- **DP-U3(b) 결정 기록**: F-H1 manifest `contract: HookModule` 인스턴스 값 채택(Memory Item append 대상 아님 — 결정 기록).
- **보류 Candidate 14건**: LD-01·02·03 · BPD-01~05 · BPD-07~11 · BP-04 — status=Candidate 필터로 Active 회수에서 자연 제외(기존 13 + 신규 BPD-11).

## 1.6 차기 개정 일괄 후보 (비차단 — 승계 + 신규, 9건)

1. **Glossary 0.2 Baseline 확정 시** — "Wave·Baseline·형태 A/B는 Glossary 표제어가 아니다" 류 서술의 전 문서 정합 개정(structure.md §0·신규 바인딩 문서들 포함). 0.2 승인 시 표제어 승격에 따른 인용 문면 정리.
2. **plugins-binding §7** framework/plugins/ 3문서 크기 표기 stale(+269B — v0.8 Baseline 행 append 결과, 양성·라이브 모순 아님).
3. **adapter-conformance §3** "자매 8문서" 계수 표현(현행 바인딩 11문서 — 자매 8 + agent/harness/scaffold-binding 3). 계수 표기 정합 후보.
4. **runtime-binding §3.2·lifecycle §5**의 전이 조건 서수 표기(조건 2 ↔ 정본 13 §3.2-B 조건 3). 자매 바인딩 내부 서수 정정(격리 갱신, T11 OQ-TJ-3).
5. **Presentation Layer 귀속 정본 확정**(Glossary §9-OQ6 흐름 — OQ-AC-2·OQ-T5-4). uahf-status·getting-started의 Presentation 귀속·BP-6 확장 관계 명문화.
6. **frameworkVersion "v0.9" 차기 릴리스 동기화**(OQ-SB-3 — Install Manifest frameworkVersion 값의 v1.0 릴리스 정합).
7. **DP-4 재상정·형태 B 잔여 5건**(전이 조건 3 충족 경로 — v1.0 이후): OQ-M5-2 · 경계 분할 OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2.
8. **getting-started·uahf-status §9 이력 미비**(Presentation 경량 관례 — 머리 상태 라인·§0 정본 경계·재정의 0은 보유하나 §9 이력 표 부재. Baseline 승격 시 이력 절 추가 재검토, T12 §3.7 관찰 6).
9. **v0.8 승계 기록만 사안** — 06 연산 실패 보고 reason 형식화·07 병렬 집합 well-formedness 보강·Memory 등록 주체 관례(Advisor 직접) 재정렬 등 handoff-v0.8 §1.6 잔여.

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1~v0.8 완료(기준선). **v0.9 CP2 첫 판정 Pass(20/0/0)·CP3 Advisor 승인 대기 — 사용자 승인 대기(Draft).** v0.9 승인 시 ROADMAP상 남은 트랙은 하나다: **v1.0 (Architecture Validation & Release)**.
- v0.9는 Adapter Layer & Scaffold 정식화의 완료다 — v0.2~v0.8 동안 Claude에 직접 바인딩된 표면이 Adapter 규격(adapter-conformance Valid(Full)) 뒤로 정식화되고, Scaffold(신규 프로젝트 설치)·Presentation 최소 기능이 실재하며, Core Claude 의존 0건이 경계 전수 스캔으로 실증됐다.

## 2.2 산출물 상태 (전부 v0.9 Draft — 사용자 승인 대기)

**신규**

| 파일 | 내용 | 비고 |
|---|---|---|
| `framework/adapters/claude/adapter-conformance.md` | Adapter Interface 커버리지 BP-1~17·Conformance Report 6필드 verdict=Valid(Full)·11 §3 재정의 0 | T1 (r2 — T15 정식화 실재 반영) |
| `framework/adapters/claude/agent-binding.md` | 02 §4.1 6행 BP-7~11 정식화·실행 모델(DP-E8 기록)·SP-1~5·분산 실현 통합 | T3 |
| `framework/adapters/claude/harness-binding.md` | 13 §4.1 조합 7행·최소 구성 5요소·§5 전이 판정 비수행(T11 소관) | T3 |
| `framework/adapters/claude/scaffold-binding.md` | 12 §4.1 10행·3연산 1:1·Install Manifest 6필드·CK-1~8 검사 방법·scaffold-template/ 정본 | T4 |
| `framework/adapters/claude/scaffold-template/` (13파일) | 설치 원본 — dot-claude/{AGENT·CLAUDE·agents 4종·settings.json.example}·framework/{core·runtime·adapters}/README·specs/README·install-manifest.template·README | T4 |
| `docs/v0.9-install-guide.md` | 신규 프로젝트 설치 절차·CK-1~8·Uninstall·Failure Report(§ 포인터) | T4 |
| `.claude/commands/uahf-status.md` | Presentation 진입 명령(BP-6 확장)·형태 A(실행 코드 0, DP-U1)·정본 포인터만 | T5 |
| `docs/getting-started.md` | 신규 참여자 진입점·4경계 지도·세션 진입 절차·정본 포인터·specs 15 표기 | T5 |
| `docs/spec-versioning-policy.md` | 개정 유형 A/B·버전 상승·이력 append·하위호환 4항·상태 승격 절차(§3.3)·첫 적용 | T2 (r2 1회) |
| `docs/v0.9-demo-procedure.md` | 시연 절차·커버리지 매핑(CK-1~8 + 12 §7 10건 + ROADMAP ③)·기대/실측 구분·단일 Task Work Graph | T9 |
| `docs/v0.9-demo.md` | Scaffold 시연 수행 기록(Install→CK-1~8→Bootstrap Ready→Loop 7 line→멱등·보호·Uninstall·CP2 Pass 8/0/0) | T10 |
| `docs/v0.9-demo-fixtures/` (37파일) | 신규 프로젝트 픽스처(new-project/·uninstall-copy·FIXTURE-NOTICE) + CP2 리포트(verify-scaffold.md) — 격리 경계 | T10 |
| `docs/v0.9-harness-transition-judgment.md` | Bootstrap → Formal 전이 재판정 — 조건 1·2·4 충족·**조건 3 미충족 → Bootstrap 유지** | T11 |
| `docs/v0.9-verification-report.md` | CP2 — 첫 판정 Pass 20/0/0·경계 직접 전수 스캔·시연 독립 재관측·비차단 관찰 6건 | T12 |
| `docs/v0.9-promotion-review.md` | 승격 심사 — L-15 Active 승격·BPD-11 Candidate·재발 판정 2(Novel)·DP-U3(b)·보류 13 | T13 |
| `docs/session-handoff-v0.9.md` | 본 핸드오프 | T14 |

**개정**

| 파일 | 개정 내용 | 비고 |
|---|---|---|
| `specs/00-glossary.md` | Version 0.1→**0.2 Draft**(Frozen v0.1 기준선 무해제)·§3.2-G 표제어 3건 추가(Wave·Baseline·형태 A/B)·Revision History append | T6 (DP-U2) |
| `framework/adapters/claude/plugins-binding.md` | 상태 "v0.9 Draft(개정 — §7 시연 후 상태 반영)"·bundle 원본/설치본 부재(Remove 잔여물 0) 반영·10 재정의 0 | T7 |
| `framework/adapters/claude/hooks-binding.md` | 상태 "v0.9 Draft(개정 — §7 시연 후 상태 반영)"·F-H1 실재·settings.json 부재 반영·08 재정의 0 | T7 |
| `docs/v0.8-demo-procedure.md` | 시점 스냅샷 후기 추기·직전 기준선 보존 | T7 |
| `docs/v0.8-demo-fixtures/verify-p.md` | 시점 스냅샷 후기 추기·판정 재정의 0 | T7 |
| `framework/core/structure.md` | §8 트리에 v0.9 신규 5산출물(agent/harness/scaffold-binding·adapter-conformance·scaffold-template/) 반영·§9 v0.9 Draft 행 append·01 §3 재정의 0 | T8 |

**물리 데이터 (append-only)**

| 대상 | 상태(착수 실측) | 비고 |
|---|---|---|
| `framework/adapters/claude/loop-data/` | +1파일 7 line(v09-demo-scaffold.jsonl) — **총 10파일 76 line**(기존 9파일 69 line 무변경) | T10, 실측 대조 완료 |
| `framework/adapters/claude/memory-data/` | store **61파일**(mi-0001~0061)·index **61라인** — 기존 56건 무변경 + 신규 5건(mi-0057~0061) | T13, store↔index 1:1·무결번·MD5 바이트 대조 실측 |

**무변경 (T12 실측)**

- Frozen specs(TEMPLATE 포함)·v0.3~v0.8 Baseline 여타 산출물·라이브 .claude 표면(신규 uahf-status.md 제외)·자매 바인딩 8문서 Baseline — mtime 타임라인·write-set·status 라인 실측(v0.9 창 밖).
- **Frozen specs 계수 = 15**(numbered 00~13 = 14 + TEMPLATE 1). specs/00-glossary.md T6 개정(0.2 Draft)이 유일한 의도된 spec 변경이며, Frozen v0.1 기준선을 무해제한다(DP-U3(c) 확정 — 종전 "16종"은 오기).

## 2.3 하네스 상태

**Bootstrap 유지**(13 §3.2-B). docs/v0.9-harness-transition-judgment.md(T11)가 13 §3.2-B 전이 조건 4건을 v0.9 현 시점 근거로 재판정한 결과다.

- **조건 1(관련 spec Frozen) = 충족** — 15종 전건 Frozen v0.1 기준선. Glossary 0.2 개정 Draft는 기준선 무해제(설치 Install Manifest specVersion "v0.1").
- **조건 2(환경 의존 실현 Adapter 격리·Core AI 의존 0) = 충족** — adapter-conformance C2 core_modifications 없음·4경계 격리·CK-6 0건(세 근거 대조).
- **조건 3(Runtime 정식 Module 호스팅) = 미충족** — 현 실현 = 형태 A(Module Manifest 6종 문서·규약·관행). 실행 Module·실행 Registry·실행 Bootstrap 미도입(형태 B).
- **조건 4(Scaffold 설치 대상) = 충족** — scaffold-binding·demo CK-1~8 전건·5요소 실물 배치.
- **종합 판정: Bootstrap 유지**(조건 3 미충족 → H-INV-7 조기 정식화 금지). 이는 **DP-U1(형태 A 유지)의 계획된 귀결**이며 v0.9 완료 조건(ROADMAP ①~④)을 막지 않는다. **사용자 보고 대상** — CP3 게이트에서 Advisor가 사용자에게 제시할 항목이며, transition-judgment 문서 자체가 그 보고의 실체다.

**Adapter Layer 정식화 실재**: Adapter Interface(11 §3.2-A BP-1~17)·Conformance Report(verdict=**Valid(Full)**)·정식화 3문서(agent/harness/scaffold-binding)·자매 바인딩 8문서·Scaffold 도구+템플릿·Presentation 진입 표면(uahf-status)·설치 시연 전건이 실재한다. **Adapter 실사용** — Core Claude 의존 0건이 경계 전수 스캔으로 실증됐고, 신규 프로젝트에 Scaffold로 설치·루프 1사이클 구동이 시연됐다. v1.0의 2nd Adapter 최소 구현(Valid(Minimal))이 이 Adapter Interface 위에서 이뤄진다.

**잔여 5건(조건 3 충족 경로 — v1.0 이후)**: OQ-M5-2(Record 원자성) + 형태 B 경계 분할 OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2. Formal 전이는 형태 B 실행 호스팅 도입(DP-4 재상정) 시 재판정한다 — 그 시점에 조건 1·2·4는 이미 충족되어 있다.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙

ROADMAP §4: v0.9 승인 완료로 남은 트랙은 **v1.0 (Architecture Validation & Release)** 하나다. 선행 조건 v0.9(Adapter Interface 확정·Scaffold·Core 경계 검증)가 충족됐다.

## 3.2 v1.0 목표·완료 조건 (ROADMAP — Architecture Validation & Release)

- **목표**: AI Agnostic Architecture를 실제로 증명한다. Claude Adapter는 완전 구현(Valid(Full))을 유지하고, **두 번째 Adapter(OpenAI 또는 Generic)를 최소 구현**해 Adapter Interface가 다른 AI에도 적용 가능함을 검증한다. 2nd Adapter는 기능 완성이 아니라 Architecture Validation을 위한 최소 구현이면 충분하다. Dogfooding과 문서화로 릴리스를 완성한다.
- **완료 조건**: ① 2nd Adapter로 핵심 루프가 1회 이상 통과(AI Agnostic 실증) ② UAHF를 사용해 실제 프로젝트 1개 개발 완료(Dogfooding) ③ 전체 스펙과 구현의 정합성 검증 통과 ④ Core의 Claude 의존 0건 유지 ⑤ README 포함 문서 세트 완성.
- **산출물**: adapters/openai/ 또는 adapters/generic/ 최소 구현·Adapter 호환성 리포트·Dogfooding 결과 보고서·README.md 및 사용자 문서 세트·v1.0 릴리스 노트.
- **정본**: ROADMAP.md v1.0. **specs/11-adapters.md §3.2-B(최소 바인딩 부분집합 — 필수 13개: BP-1·2·3·4·5·7·8·9·10·11·13·14·15 → verdict=Valid(Minimal))**. framework/adapters/claude/adapter-conformance.md(v0.9 판정 기준 — 2nd Adapter가 대조할 커버리지 정본).
- **병렬성 높음** — 2nd Adapter 최소 구현 / 문서화 / Dogfooding 3개 병렬 트랙, **최종 정합성 검증만 직렬(통합 판정)**.
- **주의**: Core Claude 의존 0건은 v1.0에서도 **유지 대상**이다(경계 전수 스캔 관행 지속). 2nd Adapter 산출물은 그 Adapter 경계(예: `framework/adapters/openai/`)에만 격리하며 Core를 침범하지 않는다(C-3·11 INV-3).

## 3.3 Memory 실사용 (모든 차기 세션 공통 — 갱신)

1. **Consult**: 착수 전 memory-binding.md §3.2로 회수. **Active 집합: Lesson 15건(L-01~L-15 — L-15 신규)·Best Practice 4건(BP-01~03 + BPD-06)**, store 61파일·index 61라인. Candidate 14건(LD-/BPD-/BP-04 — BPD-11 포함)은 status 필터에서 자연 제외.
2. **Memory Update**: Register Candidate + Advisor 승격 심사. append-only(신규 레코드/status 전이는 새 레코드로).
3. 재발 판정: was_recalled 입력은 Consult 전이 ref(사이클 구동 시) 또는 세션 회수 기록 수동 제공. Novel/RecallGap/Recurrence 3분류(lessons.md §4).

## 3.4 이월 사항

- §1.6 차기 개정 일괄 후보 9건(승계 + 신규).
- DP-4 재상정(v1.0 이후 — 형태 B 실행 호스팅 도입): 전이 조건 3 충족 경로·경계 분할 OQ 5건(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2).
- Glossary 0.2 Baseline 확정 시 표제어 승격에 따른 전 문서 인용 정합(§1.6-1).
- frameworkVersion "v0.9" 값의 v1.0 릴리스 동기화(§1.6-6, OQ-SB-3).

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — v1.0 가정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v0.9 (Adapter Layer & Scaffold)가 완료되었다.
이번 세션의 목표는 ROADMAP v1.0 (Architecture Validation & Release)이다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v0.9.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md §3.2
   절차로 Active Lesson(15건: L-01~L-15)·Best Practice(4건: BP-01~03 + BPD-06)를
   목적·최소 범위로 회수하고 회수 집합을 기록한다.
3. ARCHITECTURE.md, ROADMAP.md v1.0 섹션, specs/11-adapters.md(§3.2-B 최소 바인딩
   부분집합 13개 — 2nd Adapter Valid(Minimal) 기준), specs/12-scaffold.md·13-harness.md,
   framework/adapters/claude/adapter-conformance.md(v0.9 Valid(Full) 판정 — 2nd Adapter가
   대조할 커버리지 정본), framework/adapters/claude/ 자매 바인딩 전체(2nd Adapter가 참조할
   Claude 실현 표본), framework/core/structure.md(§8 트리·§5 C-3 경계),
   docs/v0.9-verification-report.md·docs/v0.9-demo.md(Adapter·Scaffold 실물 실증)를 정독한다.
4. .claude/AGENT.md, .claude/agents/ 4종, docs/delegation-protocol.md,
   docs/verification-checklist.md를 읽는다.
5. v1.0 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v0.9 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D) + framework/verifier/ 규격, 구현 Worker(Opus) 위임,
완료 보고 불신·독립 검증, Frozen spec 변경은 버전 상승+Revision History,
Architecture-Spec 충돌은 사용자 보고, C-1~C-3(+Module 구현 디렉터리 C-3 확장) 전 산출물 적용.
Core Claude 의존 0건은 v1.0에서도 유지 — 2nd Adapter 산출물은 그 Adapter 경계에만 격리한다.
위임문의 산출물 본문 문안(L-11)·존재 전제(L-12)와 함께
계수·규모·상태 전제 값(파일 수·항목 수·집합 규모)은 발신 전 파일 시스템 실측으로 대조한다 (L-15 신규).
기존 Baseline 문서의 개정 위임에는 상태 라인·이력 행 라벨의 기대 문면을 명시한다 (L-13).
Agent 기동 설정(.claude/agents/ 이하)의 개정은 사용자 직접 지시 권한 경로로 처리한다 (L-14).
Verifier·Planner 위임은 model opus를 명시한다 — v1.0 완료까지 영구 관행 (DP-E8).
Frozen 미명세 지점은 정본 문면 인스턴스로 해소하고 결정 기록으로 명문화한다 (BP-03).
개정 시 같은 상태 서술의 전 지점 전수 갱신(L-06)·상태 서술은 실측 후 기입(L-07·L-09).
큰 작업 분해·병렬 디스패치·병합은 framework/workflow/ 계약 인스턴스(C1~C4·R1~R4·5단계)와
확정 인터페이스 선행 Wave 배치(BP-02·BPD-06)를 사용한다.
세션 종료 시 Memory Update — Register Candidate + Advisor 승격 심사.
```

---

# 5. 주의사항

1. **물리 store·loop-data는 append-only다**(04 INV-6·03 INV-3) — memory-data/ **61파일·index 61라인**, loop-data/ **10파일 76 line** 수정·삭제 금지. 갱신은 새 레코드/새 전이 이벤트로만. 기존 56 store 파일은 MD5 바이트 무변경 실측(T13 §3.3).
2. **§9 이력 행은 시점 기록** — 문면 불변, append만(L-10). 단, 같은 세션에 자신이 append한 행의 교정은 위반 아님(T2 r2 선례 — § 포인터 오기 교정 시 r1 행 문면 보존).
3. **개정 시 전 지점 전수 갱신**(L-06) + **상태·시각 서술은 실측 후**(L-07·L-09) + **위임문 문안·존재 전제 사전 대조**(L-11·L-12) + **계수·규모·상태 전제 실측 대조**(L-15 신규) + **개정 위임의 상태 라인·라벨 기대 문면 명시**(L-13). ※ **L-15 신규 관행**: Advisor 위임문의 계수·규모·상태 전제 값은 발신 전 파일 시스템 실측으로 대조하라 — v0.9 세션 내 3회 실증(T7·T11·T13). 수임자는 위임문 계수와 실측이 어긋나면 추측 없이 실측값 기입·open_questions 에스컬레이션한다.
4. **승격 권한 Advisor 전속**(05 INV-4) — Active 승격 레코드는 승인 참조를 content(`approval`)에 자기완결 첨부(mi-0058 실측). Worker(승격 심사 문서 집행 주체)는 승격을 결정하지 않고 물리 집행만 한다.
5. **Module 구현 디렉터리 문서 본문에 특정 Adapter 문서명·물리 토큰 금지**(C-3 확장). framework/core·runtime·loop·memory·verifier·workflow·plugins 7 디렉터리군에 이 경계 적용(T12 §3.3 전수 스캔 매치 0 실측). **Core Claude 의존 0건은 v1.0에서도 유지 대상.**
6. **픽스처 경계** — docs/v0.5-demo-fixtures/·v0.6·v0.7·v0.8·**v0.9-demo-fixtures/**는 의도적 결함·환경 토큰 정당 보유 격리 지점(new-project/framework/adapters/README.md의 "Claude Code" 등). 전수 스캔 시 제외 명시(verifier_scope 관례). 단 v0.9 설치본 Core부(new-project/framework/core·runtime)의 CK-6 재스캔은 수행 대상이다(격리 예외).
7. **scaffold-template/은 설치 원본**(13파일 — 실측 확인) — 신규 프로젝트 설치가 이 원본을 복사·매핑(`dot-claude/*`→`.claude/*`)한다. **수정 시 Adapter Binding 정본 scaffold-binding.md §6(scaffold-template/ 필수 6요소 대응)과 정합 필수.** 설치 시연은 이 원본을 픽스처에 복사만 하며 원본을 수정하지 않는다(T10 소유 경계 준수).
8. **report-exporter 설치본은 Remove로 부재가 정상** — framework/plugins/ 현재 = module-manifest·plugin-manifest·plugin-lifecycle 3 md만(설치본 report-exporter/ 부재, Remove 잔여물 0 — 실측 확인). 재설치는 bundle 원본(docs/v0.8-demo-fixtures/report-exporter/)에서 한다.
9. **라이브 표면 위생(DP-E7)** — `.claude/hooks/`·`.claude/skills/`에는 정상 레퍼런스만 존치(F-H1·F-S1). v0.9가 추가한 라이브 표면은 `.claude/commands/uahf-status.md`(T5) 1건뿐이다. 결함 픽스처는 docs/v0.X-demo-fixtures/ 격리 경계에만 배치한다.
10. **DP-E8 영구 관행** — Verifier·Planner 위임은 `model: opus` 명시. v1.0 완료까지 유지. 계약(06) 변경이 아니라 실행 모델 바인딩(02 §4.1)이다. Agent 기동 설정(.claude/agents/ 이하) 개정은 사용자 직접 지시 권한 경로로만(L-14).
11. **시연 기록의 성격** — v0.9 시연은 **단일 사이클·단일 Task**(순차 단계 ①~⑤의 단일 흐름이므로 과분해 금지·Merge 불필요). 설치 실증과 루프 실증이 한 사이클에서 성립(BPD-11 후보). memory timestamp·loop-data `at`은 순서 값이며 물리 벽시계 시각이 아니다(L-09). Install Manifest `timestamp`도 순서 값.
12. **Glossary 0.2 Draft 승인 시 Frozen 승격 절차** — spec-versioning-policy.md **§3.3(상태 승격 절차)**: Draft → 사용자 승인으로 Frozen 확정(spec 경로) / Baseline 확정(framework 인스턴스 경로). 승인이 확정 게이트(Human Approval). 확정 후 재개정은 §3.1 대전제(버전 상승 + 이력 append). Glossary 0.2가 새 Frozen 기준선이 되어도 v0.1 기준선의 Frozen 지위를 소급 해제하지 않는다(T11 OQ-TJ-1).
13. **Frozen specs 계수 = 15**(numbered 00~13 = 14 + TEMPLATE 1 — DP-U3(c) 확정, 종전 "16종"은 오기). 전 v0.9 산출물이 15로 정합 표기(T12 item #16 — "16종" 잔여 0). 계수 표기 자리에는 15를 쓴다.
14. **하네스 Bootstrap 유지** — v0.9 종료 시점에도 부트스트랩 상태다(전이 조건 3 미충족, DP-U1 귀결). v1.0은 Formal 전이를 완료 요건으로 요구하지 않는다 — 2nd Adapter·Dogfooding·문서화는 Bootstrap 상태에서 성립한다. Formal 전이는 형태 B 실행 호스팅 도입 시로 유보(v1.0 이후 사안).
