# UAHF Session Handoff — v1.0 → 다음 세션

작성일: 2026-07-07
작성자: Worker (Advisor 위임, Task T12)
목적: 이 문서만 읽어도 새 세션이 v1.0 이후 작업을 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v0.9.md, v0.8, v0.7, v0.6, v0.5, v0.4, v0.3, v0.2, v0.1)
상태: v1.0 Baseline (CP2 첫 판정 Pass 21/0/0 — v0.5부터 6연속 · CP3 승인 · 사용자 승인 2026-07-07). 사용자 승인 반영 완료 — Advisor가 v1.0 산출물 전건에 Baseline 행 append·상태 라인 승격을 수행하고 본 문서 이력에 기록했다. ROADMAP v0.1→v1.0 전 트랙 완료.

---

## §9. 이력 (Revision History)

| 일자 | 변경 | 주체 |
|---|---|---|
| 2026-07-07 | 최초 작성 (사용자 승인 대기 상태) | Worker (Advisor 위임, Task T12) |
| 2026-07-07 | v1.0 Baseline 확정 — 사용자 승인 반영 (전 산출물 상태 라인 승격·Baseline 행 append) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행(v1.0 verification-report·release-notes·promotion-review·v0.9 handoff 동형). 이후 개정은 이 표에 append-only로 기록한다. 사용자 승인 반영은 별도 행으로 append한다.)

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v1.0 — Architecture Validation & Release)

1. **세션 진입 절차 이행** — handoff v0.9 정독 → **Consult 실수행(7회째 실가동)**: index.jsonl **61라인**(착수 시점) 스캔, 회수 집합 = Active Lesson 15건(L-01~L-15) + Best Practice 4건(BP-01~03·BPD-06) = **19건**(detail=full) → 정본·운용 문서 정독(ROADMAP v1.0·specs/11 §3.2-B·12·13·adapter-conformance.md·framework/adapters/claude/ 자매 바인딩·structure.md·v0.9-verification-report·v0.9-demo) → **착수 전 실측**(L-12·L-15 — 위임문 계수·규모·상태 전제의 발신 전 파일 시스템 실측 대조).
2. **Execution Plan 수립** — Planner 초안(`model: opus`, DP-E8) → **Advisor 채택**·OQ 10건 해소 → **사용자 승인**(2026-07-06, 계획 모드 — 사용자 결정 3건: **DP-V1 2nd Adapter = Generic**·**DP-V2 Dogfooding = 소형 CLI**·**DP-V3 릴리스 문서 = 한국어 본문 + 영어 요약**).
3. **Wave 실행 (W1~W6, 13 Task = T1~T12 + T8b)** —
   - **W1 (3병렬)**: generic-binding(T1)·v1.0-dogfooding-spec(T2, r2 1회)·scaffold-binding frameworkVersion 동기화(T3, r2 1회).
   - **W2 (3병렬)**: generic Adapter 시연(T4 — demo + generic-demo-fixtures/)·Dogfooding(T5 — uahf-lessons CLI 개발·설치·루프)·README+user-guide(T6).
   - **W3 (3병렬)**: generic-adapter-conformance + 호환성 리포트(T7)·structure.md §8(T8)·getting-started 개정(T8b — W3 편입).
   - **W4 (직렬)**: 마일스톤 CP2(T9 — 독립 Verifier `model: opus`, DP-E8).
   - **W5 (2병렬)**: v1.0 릴리스 노트(T10 — CP2 후 산출, DP-V8)·승격 심사(T11).
   - **W6**: 본 핸드오프(T12).
4. **검증 리포트** — docs/v1.0-verification-report.md: **첫 판정 Pass 21/0/0 (v0.5부터 6연속)**. 완료 조건 ② CLI 직접 재실행·완료 조건 ④ 경계 직접 전수 스캔(7 디렉터리군 25파일 0건)·C1 3자 셀 대조·거짓 완료 검출 0건·비차단 관찰 4건(§3.8).
5. **Memory Update 실가동 7회차** — 심사 등록 10건(mi-0062~0071): **재발 판정 4건(전건 Novel)·L-16~L-19 Candidate 등록·보류·BPD-11 Active 재상정 승격·BPD-12 Candidate 등록·보류**. **store 71파일·index 71라인**, 기존 61건 무변경(append-only·바이트 수준 MD5 대조).

## 1.2 v1.0 완료 조건 대조 (ROADMAP §5 — 전건 충족, T9 §4 근거)

| 완료 조건 | 판정 | 근거 (CP2 § 포인터) |
|---|---|---|
| ① 2nd Adapter로 핵심 루프가 1회 이상 통과 (AI Agnostic 실증) | 충족 | Generic verdict=**Valid(Minimal)**(generic-adapter-conformance §3 6필드)·C1 필수 13 BP 3자 셀 대조 재정의 0(item #3)·demo `cycle-record.log` **4전이** 완주(위임→구현→검증→승인·human 0)·독립 Verifier Pass 3/3·두 Adapter INV-8 동일 Core Contract (item #2~#5·§3.5) |
| ② UAHF로 실제 프로젝트 1개 개발 완료 (Dogfooding) | 충족 | `uahf-lessons` CLI a **61**·b **19**·c **9**·d **exit 2**·e 읽기 전용(CP2 직접 실행 §3.4)·loop-data `v10-dogfooding.jsonl` **7 line**·human **0**·설치 CK-1~8·CK-6 설치본 Core 7파일 **0**·독립 Verifier **Pass 14/0/0**·stdlib only (item #6~#11) |
| ③ 전체 스펙-구현 정합성 검증 통과 | 충족 | C1 3자 셀 대조(item #3)·관행 규격(상태 라인·§9 이력·재정의 0·§ 포인터 실재, item #14)·structure.md §8 복수 Adapter 반영(item #15)·scaffold-binding frameworkVersion **"v1.0"** 동기화·specVersion "v0.1" 무변경(item #16) |
| ④ Core의 Claude 의존이 0건으로 유지 | 충족 | 7 디렉터리군 **25파일** 2패스+광역 전수 스캔 매치 **0건**(item #12)·generic 경계 2파일 특정 AI 실명 **0**·타 Adapter 경로 **0**(DP-V6·DP-V14, item #13)·설치본 Core 7파일 **0**(item #10) |
| ⑤ README를 포함한 문서 세트 완성 | 충족 | README.md(영/한 개요)+docs/v1.0-user-guide.md+docs/getting-started.md(§9 이력 절 신설·stale 2지점 해소) 실재·구성·verdict 선취 **0** (item #14·§5) |

산출물 5종 충족(ROADMAP §5): adapters/generic/ 최소 구현(Valid(Minimal))·Adapter 호환성 리포트·Dogfooding 결과 보고서·README 및 사용자 문서 세트·v1.0 릴리스 노트.

## 1.3 이번 세션의 설계 결정 (전부 확정·기록 — 사용자 3건 + Advisor 11건)

| 결정 | 내용 | 상태 |
|---|---|---|
| **DP-V1** | **사용자 결정 — 2nd Adapter = Generic.** 두 번째 Adapter는 Generic(환경 중립)으로 최소 구현하며 경계는 `framework/adapters/generic/` | **사용자 결정 (2026-07-06)** |
| **DP-V2** | **사용자 결정 — Dogfooding = 소형 CLI.** 실제 프로젝트는 소형 CLI(`uahf-lessons`)이며 경계는 `dogfooding/uahf-lessons/` | **사용자 결정 (2026-07-06)** |
| **DP-V3** | **사용자 결정 — 릴리스 문서 = 한국어 본문 + 영어 요약.** 릴리스 노트는 한국어 본문에 영어 요약(Release Summary)을 병기 | **사용자 결정 (2026-07-06)** |
| **DP-V4** | uahf-lessons = 외부 열람 유틸리티 — 04 단일 Port(Memory Service Interface) 적용 대상 밖(하네스 Memory 백엔드가 아니라 index.jsonl을 읽기 전용으로 조회하는 외부 CLI) | 확정 |
| **DP-V5** | generic C3(핵심 루프 통과) 실증 = 실동작 사이클·물리 주체 투명 기재(위임/구현/검증/승인 4전이·actor 역할명·human 0) | 확정 |
| **DP-V6** | generic 정체성 = 환경 중립 — generic 경계 문서 본문에 특정 AI 실명·모델명·벤더 제품명 토큰 0 | 확정 |
| **DP-V7** | generic 시연 = 픽스처 격리·단일 문서(demo 1문서 + generic-demo-fixtures/ 격리 경계) | 확정 |
| **DP-V8** | 릴리스 노트 = CP2 후 산출(T10 — 완료 조건 ①~⑤에 릴리스 노트 미포함이므로 CP2가 막지 않음) | 확정 |
| **DP-V9** | structure.md §8 트리에 복수 Adapter 경계 반영 — 두 번째 `<adapter>/` 일반형·실명 0 | 확정 |
| **DP-V10** | Install Manifest frameworkVersion "v0.9"→**"v1.0"** 동기화 — OQ-SB-3 해소·specVersion "v0.1" 무변경 | 확정 |
| **DP-V11** | v1.0 명세·리포트 문서 위치 = docs/ | 확정 |
| **DP-V12** | 문서 세트 = README + user-guide 신규·getting-started는 확인만 → 실측상 stale 검출로 **T8b 개정으로 전환**(§9 이력 절 신설·stale 2지점 해소) | 확정 |
| **DP-V13** | CP2 verifier_scope 격리 예외 — 픽스처·Adapter 경계·docs/·설치본 응용부는 C-3 AI 스캔 제외하되 설치본 Core CK-6·generic 정체성·픽스처 중립성은 검사 | 확정 |
| **DP-V14** | generic 경계 산출물은 타 Adapter 경로 불명명 — 역할 기반 중립 참조만. 어댑터 간 명명·대조는 docs/ 소속 문서 소관(docs/ 문서는 두 Adapter 자유 명명·경로 인용 허용) | 확정 |

**주요 OQ 해소**: OQ-SB-3(frameworkVersion v1.0 동기화 — DP-V10)·OQ-W1(위임문 전칭 불변 규칙 과잉 포섭 → Advisor 재량 해소·근거 괄호 `(ROADMAP v1.0)` 정합, T3 r2) 외 Advisor 채택 시 OQ 10건 해소.

## 1.4 검증 게이트 실동작 기록

- **마일스톤 수준**: 실서브에이전트 위임 다회(Planner·Worker·Verifier — Verifier·Planner 위임은 `model: opus` DP-E8) + **재개정 라우팅 2회**. 거짓 완료 보고 0건. **CP2 첫 판정 Pass 21/0/0 — v0.5부터 6연속·재작업 0회.**
- **재개정 라우팅 2회**:
  - **T2 r2** — 산출물(docs/v1.0-dogfooding-spec.md) 파일 말미 **도구 구문 잔여물 2줄**을 Advisor 게이트 C 검출·r2 폐합. 신규 Lesson 후보 **L-16**(mi-0063 Candidate)·재발 판정 **Novel**(mi-0062).
  - **T3 r2** — 위임문 "불변 유지" 전칭 규칙이 값 결합 근거 괄호까지 과잉 포섭(**OQ-W1**) → 근거 괄호 `(ROADMAP v0.9)` 잔존 → Advisor 재량 해소·`(ROADMAP v1.0)` 정합. 신규 Lesson 후보 **L-17**(mi-0065 Candidate)·재발 판정 **Novel**(mi-0064).
- **CP2 직접 수행 근거**: 완료 보고를 그대로 신뢰하지 않고(06 V1) CLI 직접 재실행(a~e + 보조 7종)·경계 직접 전수 스캔(7 디렉터리군 25파일 0건)·loop-data/generic 사이클 기록 직접 파싱·C1 3자 셀 대조·mtime 타임라인 실측으로 재판정. 전 산출물 실질 주장 ↔ 직접 실측 전 지점 일치, 거짓 완료 검출 0건.

## 1.5 Lesson·BP — 정식 등록 경로 처리 완료 (심사 등록 10건 mi-0062~0071)

- **재발 판정 4건 — 전건 Novel**(kind=recurrence-judgment): mi-0062(T2 r1 산출물 도구 구문 잔여물)·mi-0064(T3 r1 위임문 전칭 불변 규칙 과잉 포섭)·mi-0066(T3 r1 위임문 § 라벨 오기)·mi-0068(T5 CLI 콘솔 인코딩 결함 — 실행 관측 검출). 각 `matched_lesson_id` 부재(Novel 정상). was_recalled = 회수 집합 19건 참조.
- **Lesson Candidate 등록·보류 4건**(각 1회 발생 — 승격 없이 Candidate 보류): **L-16**(mi-0063 — 산출물 생성 직후 CP1 자체 점검에 파일 말미·전체 도구 구문 잔여물 실측 확인)·**L-17**(mi-0065 — 위임문 전칭 불변 규칙 사용 시 값 결합 요소 적용/제외 구분 명시)·**L-18**(mi-0067 — 위임문 § 라벨·절 번호 지칭 시 발신 전 실측 대조)·**L-19**(mi-0069 — 콘솔 출력 산출물은 대상 환경 기본 인코딩 실행 관측·출력 인코딩 명시 설정).
- **BPD-11 Active 재상정 승격**(mi-0070, supersedes mi-0059) — v0.9 보류 조건("실무 동형 재발 시 재상정")이 v1.0 T5 Dogfooding(실제 프로젝트 개발·CP2 Pass)으로 충족. 승인 참조 content(`approval`) 자기완결 첨부(05 INV-4). BPD-06 승격 선례 동형.
- **BPD-12 신규 Candidate 등록·보류**(mi-0071) — generic 시연(T4) 유래 최소 구현 Adapter C3 실증 관례. 시연 유래이므로 실무 동형 재발 시 재상정.
- **승격 권한 Advisor 전속(05 INV-4)**: 판정·승격·등록 결정은 전부 Advisor 확정. docs/v1.0-promotion-review.md(Worker 집행)는 문서화·물리 집행만 수행.
- **기존 보류 Candidate 13건 승계 유지**(LD-01·02·03 · BPD-01~05 · BPD-07~10 · BP-04). 기존 14 − BPD-11(Active 승격) + 신규 5(L-16~19·BPD-12) = **Candidate 18건**. status 필터로 Active 회수에서 자연 제외.

## 1.6 차기 개정 일괄 후보 (비차단 — 승계 + 신규)

**(a) v0.9 §1.6 이월 후보 중 유보 잔여:**

1. **Glossary 0.2 표제어 인용 정합** — "Wave·Baseline·형태 A/B는 Glossary 표제어가 아니다" 류 서술의 전 문서 정합 개정(0.2 Frozen 승격에 따른 인용 문면 정리).
2. **plugins-binding §7** framework/plugins/ 3문서 크기 표기 stale(양성·라이브 모순 아님).
3. **adapter-conformance §3** "자매 8문서" 계수 표현(현행 바인딩 12문서 — 자매 8 + agent/harness/scaffold-binding 3 + adapter-conformance 자신) 계수 표기 정합.
4. **runtime-binding §3.2·lifecycle §5** 전이 조건 서수 표기(자매 바인딩 내부 서수 정정, 격리 갱신).
5. **Presentation Layer 귀속 정본 확정**(uahf-status·getting-started의 Presentation 귀속·BP-6 확장 관계 명문화).
6. **uahf-status §9 이력 절**(Presentation 경량 관례 — 머리 상태 라인 보유하나 §9 이력 표 부재. 실개정 시 추가 재검토).
7. **v0.8 승계 기록만 사안** — 06 연산 실패 보고 reason 형식화·07 병렬 집합 well-formedness 보강 등 handoff-v0.8 §1.6 잔여.

**(b) v1.0 신규 관찰(CP2 §3.8 비차단 4건 및 부수):**

1. **설치본 Core부 시점 스냅샷 divergence** — dogfooding 설치본 `framework/core/structure.md`(23:30 배치)가 라이브 structure.md(T8가 23:56 개정)와 상이. 설치 시점 스냅샷 의미론으로 **Advisor 수용**(설치 결함·거짓 완료 아님 — 재설치 시 갱신 선택지). CK-6(설치본 Core AI 0)은 불변.
2. **memory source 라벨 관례** — 신규 10건 source를 `v1.0-review`로 기입(위임 input에 고유 Task 번호 미명시·L-15상 미확인 Task 번호 미주장). Task 번호 표기 관례 미확정 — 필요 시 확정.
3. **이력 행 Task 라벨 버전 접두 관례** — "v1.0 Task T8" 표기 선례(개정 이력 행의 Task 라벨에 버전 접두).
4. Glossary 0.2 승인·uahf-status 갱신은 v0.9 클로즈아웃 창(v1.0 창 개시 전 22:12~22:15). 릴리스 노트 CP2 후 산출(DP-V8 예정대로 T10 완료). Dogfooding Lesson/BP append 유보는 T11 승격 심사에서 집행 완료.

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1~v0.9 완료(기준선). **v1.0 CP2 첫 판정 Pass(21/0/0)·CP3 Advisor 승인 대기 — 사용자 승인 대기(Draft).** v1.0 승인 시 **ROADMAP v0.1→v1.0 전 트랙이 완료**된다 — 다음 트랙은 ROADMAP에 정의되어 있지 않다(§3.1).
- v1.0은 Architecture Validation & Release다 — AI Agnostic Architecture가 실제로 증명됐다. Claude Adapter는 완전 구현(Valid(Full))을 유지하고, 두 번째 Adapter(Generic)가 최소 구현(Valid(Minimal))되어 Adapter Interface가 다른 실행 환경에도 적용 가능함이 검증됐다. Dogfooding(uahf-lessons CLI 개발)과 문서 세트(README 포함)로 릴리스가 완성됐으며, Core Claude 의존 0건이 경계 전수 스캔으로 유지 실증됐다.

## 2.2 산출물 상태 (전부 v1.0 Draft — 사용자 승인 대기)

**신규 (13 — 실측 대조 완료)**

| 파일 | 내용 | 비고 |
|---|---|---|
| `framework/adapters/generic/generic-binding.md` | 11 §3.2-B 필수 13 BP 바인딩 값 문서·환경 중립(AI 실명 0, DP-V6)·타 Adapter 경로 0(DP-V14) | T1 |
| `framework/adapters/generic/generic-adapter-conformance.md` | Conformance Report 6필드 verdict=**Valid(Minimal)**·§2.1 커버리지 13행·11 §3 재정의 0 | T7 |
| `docs/v1.0-dogfooding-spec.md` | Dogfooding CLI 명세·완료 기준 a~e·§4.1 보조 케이스 | T2 (r2 1회) |
| `docs/v1.0-generic-adapter-demo.md` (+ `docs/v1.0-generic-demo-fixtures/` 16파일 격리 evidence) | generic 핵심 루프 시연 기록(4전이·독립 Verifier Pass 3/3)·픽스처 격리 경계(DP-V5·V7) | T4 |
| `docs/v1.0-dogfooding-report.md` | uahf-lessons 개발·실행 관측·개발 사이클 CP2 Pass 14/0/0·CK-1~8 | T5 |
| `docs/v1.0-user-guide.md` | 운용 안내(§ 포인터·verdict 선취 0) | T6 |
| `docs/v1.0-adapter-compatibility-report.md` | 두 Adapter 대조(claude Valid(Full)↔generic Valid(Minimal))·INV-8·Core 무수정 | T7 |
| `docs/v1.0-verification-report.md` | CP2 — 첫 판정 Pass 21/0/0·CLI 직접 실행·경계 직접 전수 스캔·비차단 관찰 4건 | T9 |
| `docs/v1.0-release-notes.md` | v1.0 릴리스 노트(영어 Release Summary + 한국어 본문, DP-V3·V8) | T10 |
| `docs/v1.0-promotion-review.md` | 승격 심사 — 재발 4(Novel)·L-16~19 Candidate·BPD-11 Active·BPD-12 Candidate | T11 |
| `docs/session-handoff-v1.0.md` | 본 핸드오프 | T12 |
| `README.md`(루트) | 영어 개요 + 한국어 프로젝트 소개·문서 세트 진입점(DP-V3) | T6 |
| `dogfooding/uahf-lessons/` (35파일) | Dogfooding 실제 프로젝트 — 설치본 31 + install-manifest.md + src/uahf_lessons.py + README.md + verify-uahf-lessons.md, DP-V2 | T5 |

(신규 13 = generic 경계 2 + docs 9(dogfooding-spec·generic-adapter-demo·dogfooding-report·user-guide·adapter-compatibility-report·verification-report·release-notes·promotion-review·session-handoff-v1.0) + README 1 + dogfooding/uahf-lessons/ 1. generic-demo-fixtures/(16파일)는 generic-adapter-demo의 격리 evidence로 그 행에 병기(DP-V7 단일 문서·CP2 §1 T4 그룹핑 동형). 물리 파일 계수는 실측 — fixtures 16·dogfooding 35.)

**개정 (4)**

| 파일 | 개정 내용 | 비고 |
|---|---|---|
| `framework/adapters/claude/scaffold-binding.md` | 상태 "v1.0 Draft (개정 r2)"·Install Manifest frameworkVersion "v0.9"→**"v1.0"** 동기화(6지점)·specVersion "v0.1" 무변경·OQ-SB-3 해소·근거 괄호 `(ROADMAP v1.0)` 정합(r2)·12 §3 재정의 0 | T3 (r2 1회, DP-V10) |
| `framework/adapters/claude/scaffold-template/install-manifest.template.md` | front-matter frameworkVersion **"v1.0"**·specVersion "v0.1" 무변경 | T3 (DP-V10) |
| `framework/core/structure.md` | §8 트리에 복수 Adapter 경계 반영(두 번째 `<adapter>/` 일반형·실명 0)·§9 v1.0 Draft(T8) 행 append·01 §3 재정의 0 | T8 (DP-V9) |
| `docs/getting-started.md` | §9 이력 절 **신설**(v0.9 리포트 비차단 관찰 해소)·stale 2지점 정합·직전 v0.9 Baseline 행 보존 | T8b (DP-V12) |

**물리 데이터 (append-only — 실측 대조 완료)**

| 대상 | 상태(실측) | 비고 |
|---|---|---|
| `framework/adapters/claude/loop-data/` | +1파일 7 line(v10-dogfooding.jsonl) — **총 11파일 83 line**(기존 10파일 76 line 무변경) | T5, 파일 수·행 수 직접 계수 |
| `framework/adapters/claude/memory-data/` | store **71파일**(mi-0001~0071)·index **71라인** — 기존 61건 무변경 + 신규 10건(mi-0062~0071) | T11, store↔index 1:1·무결번·MD5 바이트 대조 |

**Memory 심사 후 집합 (실측 대조 완료 — L-07·L-15)**

- **Active 20건** = Lesson **15건**(L-01~L-15) + Best Practice **5건**(BP-01·BP-02·BP-03·BPD-06·**BPD-11**). BPD-11은 mi-0070으로 Active 재상정 승격.
- **Candidate 18건** = LD-01·02·03 · BPD-01~05 · BPD-07~10 · BP-04 · **L-16·L-17·L-18·L-19·BPD-12** (기존 14 − BPD-11 + 신규 5). status 필터로 Active 회수에서 자연 제외.
- **kind 분포(71)**: lesson **37** · best-practice **21** · recurrence-judgment **13** (합 71 — 직접 실측).

**무변경 (CP2 실측)**

- Frozen specs(TEMPLATE 포함) **15종**·v0.3~v0.9 Baseline 여타 산출물·라이브 `.claude` 표면·framework/adapters/claude 자매 바인딩 12문서 — v1.0 창(23:09~00:02) 밖. Glossary 0.2 승인·uahf-status 갱신은 v0.9 클로즈아웃(v1.0 창 개시 전).
- **Frozen specs 계수 = 15**(numbered 00~13 = 14 + TEMPLATE 1 — 직접 실측). Glossary 0.2 Frozen(v0.9 승격 유지)은 v0.1 기준선을 소급 해제하지 않는다.

## 2.3 하네스 상태

**Bootstrap 유지**(13 §3.2-B). v1.0은 Formal(형태 B) 전이를 완료 요건으로 요구하지 않는다 — 2nd Adapter·Dogfooding·문서화는 Bootstrap 상태에서 성립했다.

- **전이 조건 3(Runtime 정식 Module 호스팅) = 미충족** — 현 실현 = 형태 A(문서 절차·규약·관행). 이는 DP-U1(v0.9, 형태 A 유지)의 승계된 귀결이다.
- 조건 1(관련 spec Frozen)·2(환경 의존 실현 Adapter 격리·Core AI 의존 0)·4(Scaffold 설치 대상)는 v0.9 시점에 이미 충족되어 있으며 v1.0에서 유지됐다(Core Claude 의존 0건 경계 전수 스캔 지속).
- **주(하네스 vs 유틸리티 구분)**: Dogfooding으로 개발한 `uahf-lessons` CLI 자체는 형태 B 실행 코드(Python stdlib)로 직접 실행 관측됐으나, 이는 Dogfooding 대상 유틸리티이지 하네스 실행 Module 전환이 아니다 — 하네스는 Bootstrap 유지.

**Adapter Layer 실사용 실증**: 두 Adapter(claude 완전·generic 최소)가 동일 Core Contract를 소비하며 Valid(Full)↔Valid(Minimal)로 대조됐고(compatibility 리포트 §2·§3·INV-8), generic Adapter 위에서 핵심 루프가 4전이로 1회 통과했다(demo·독립 Verifier Pass 3/3). Core Claude 의존 0건은 v1.0에서도 경계 전수 스캔으로 유지 실증됐다.

**Formal 전이 잔여(v1.0 이후 사안)**: DP-4 재상정 경로 — OQ-M5-2(Record 원자성) + 형태 B 경계 분할 OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2 (5건). 형태 B 실행 호스팅 도입 시 재판정하며, 그 시점에 조건 1·2·4는 이미 충족되어 있다.

---

# 3. 다음 세션에서 수행할 작업

## 3.1 트랙 — **미정 (사용자 결정 필요)**

**ROADMAP v0.1→v1.0 전 트랙이 완료**되었다(v1.0 사용자 승인 가정). ROADMAP.md는 v1.0을 마지막 트랙으로 정의하며, **다음 트랙은 정의되어 있지 않다**. 다음 세션의 트랙은 **사용자 결정 대상**이다. 이 핸드오프는 차기 마일스톤을 선취해 확정하지 않는다.

**후보(사용자 선택 대상 — 선취 아님):**

- **형태 B 실행 호스팅 도입 / DP-4 재상정** — Formal 전이 경로. 전이 조건 3 충족 경로·경계 분할 OQ 5건(OQ-M5-2·OQ-VB-2·OQ-LB-2·OQ-WB-2·OQ-PB-2).
- **유지보수 운용** — 릴리스 후 개정·이월 후보(§1.6) 정리·Glossary 0.2 인용 정합 등.
- **신규 로드맵 v2** — 새 목표 트랙 정의.

## 3.2 Memory 실사용 (모든 차기 세션 공통 — 갱신)

1. **Consult**: 착수 전 memory-binding.md §3.2로 회수. **Active 집합: Lesson 15건(L-01~L-15)·Best Practice 5건(BP-01~03 + BPD-06 + BPD-11)** = **20건**, store 71파일·index 71라인. Candidate 18건(LD-/BPD-/BP-04 + L-16~19·BPD-12)은 status 필터에서 자연 제외.
2. **Memory Update**: Register Candidate + Advisor 승격 심사. append-only(신규 레코드/status 전이는 새 레코드로).
3. 재발 판정: was_recalled 입력은 Consult 회수 기록. Novel/RecallGap/Recurrence 3분류(lessons.md §4).

## 3.3 이월 사항

- §1.6 차기 개정 일괄 후보(승계 + 신규).
- Formal 전이 경로(DP-4 재상정 — 형태 B 실행 호스팅 도입 시): 전이 조건 3 충족·경계 분할 OQ 5건.
- v1.0 신규 관찰(§1.6-b): 설치본 Core부 시점 스냅샷 divergence(수용)·memory source 라벨 관례·이력 행 Task 라벨 버전 접두 관례.

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt — 다음 트랙 미정)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v1.0 (Architecture Validation & Release)이 완료되었다.
이로써 ROADMAP v0.1→v1.0 전 트랙이 완료되었다 — 다음 트랙은 ROADMAP에 정의되어 있지 않다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v1.0.md를 정독한다 (직전 세션 결정·상태의 정본).
2. Consult — Memory 회수를 실제 수행한다: framework/adapters/claude/memory-binding.md §3.2
   절차로 Active Lesson(15건: L-01~L-15)·Best Practice(5건: BP-01~03 + BPD-06 + BPD-11)
   = 20건을 목적·최소 범위로 회수하고 회수 집합을 기록한다
   (store 71파일·index 71라인. Candidate 18건은 status 필터로 자연 제외).
3. 다음 트랙을 스스로 채택하지 말고 사용자에게 결정을 요청한다.
   ROADMAP v1.0까지 전 트랙이 완료되었으므로 다음 트랙은 미정이다. 후보를 제시하되
   (형태 B 실행 호스팅 도입·DP-4 재상정 / 유지보수 운용 / 신규 로드맵 v2)
   채택은 사용자 결정 사항이다. 차기 마일스톤을 선취해 착수하지 않는다.
4. 사용자가 트랙을 결정하면, 필요한 정본을 정독하고
   (ARCHITECTURE.md, ROADMAP.md, 관련 specs, framework/adapters/ 바인딩,
   framework/core/structure.md, 직전 검증·릴리스 리포트),
   .claude/AGENT.md·.claude/agents/ 4종·docs/delegation-protocol.md·
   docs/verification-checklist.md를 읽고, 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v1.0 확립 관행 유지 — 위임/보고 delegation-protocol.md, 검증
verification-checklist.md(게이트 A~D) + framework/verifier/ 규격, 구현 Worker(Opus) 위임,
완료 보고 불신·독립 검증, Frozen spec 변경은 버전 상승+Revision History,
Architecture-Spec 충돌은 사용자 보고, C-1~C-3(+Module 구현 디렉터리 C-3 확장) 전 산출물 적용.
Core Claude 의존 0건은 유지 대상이며 2nd Adapter 이후 산출물은 그 Adapter 경계에만 격리한다.
generic 경계 문서는 특정 AI 실명·타 Adapter 경로 불명명(DP-V6·DP-V14) — 어댑터 간 명명은 docs/ 소관.
위임문의 산출물 본문 문안(L-11)·존재 전제(L-12)·계수/규모/상태 전제(L-15)·
§ 라벨/절 번호 지칭(L-18 Candidate)은 발신 전 파일 시스템 실측으로 대조한다.
기존 Baseline 문서의 개정 위임에는 상태 라인·이력 행 라벨의 기대 문면을 명시한다 (L-13).
Agent 기동 설정(.claude/agents/ 이하)의 개정은 사용자 직접 지시 권한 경로로 처리한다 (L-14).
Verifier·Planner 위임은 model opus를 명시한다 (DP-E8 — v1.0 완료로 "영구 관행" 문구는
차기 세션 재확인 대상으로 승계).
Frozen 미명세 지점은 정본 문면 인스턴스로 해소하고 결정 기록으로 명문화한다 (BP-03).
개정 시 같은 상태 서술의 전 지점 전수 갱신(L-06)·상태 서술은 실측 후 기입(L-07·L-09).
큰 작업 분해·병렬 디스패치·병합은 framework/workflow/ 계약 인스턴스(C1~C4·R1~R4·5단계)와
확정 인터페이스 선행 Wave 배치(BP-02·BPD-06·BPD-11)를 사용한다.
세션 종료 시 Memory Update — Register Candidate + Advisor 승격 심사.
```

---

# 5. 주의사항

1. **물리 store·loop-data는 append-only다**(04 INV-6·03 INV-3) — memory-data/ **71파일·index 71라인**, loop-data/ **11파일 83 line** 수정·삭제 금지. 갱신은 새 레코드/새 전이 이벤트로만. 기존 61 store 파일은 MD5 바이트 무변경 실측(T11 §3.3).
2. **§9 이력 행은 시점 기록** — 문면 불변, append만(L-10). 단, 같은 세션에 자신이 append한 행의 교정은 위반 아님(T3 r2 선례 — 근거 괄호 정합 시 r1 이력 행 문면 보존).
3. **개정 시 전 지점 전수 갱신**(L-06) + **상태·시각 서술은 실측 후**(L-07·L-09) + **위임문 문안·존재 전제·계수 전제 사전 대조**(L-11·L-12·L-15) + **개정 위임의 상태 라인·라벨 기대 문면 명시**(L-13). ※ **L-15 관행**: Advisor 위임문의 계수·규모·상태 전제 값은 발신 전 파일 시스템 실측으로 대조하라 — v1.0 세션은 위임 done(6) 명시값과 실측이 전건 일치(편차 0). 수임자는 위임문 계수와 실측이 어긋나면 추측 없이 실측값 기입·open_questions 에스컬레이션한다.
4. **승격 권한 Advisor 전속**(05 INV-4) — Active 승격 레코드는 승인 참조를 content(`approval`)에 자기완결 첨부(mi-0070 실측). Worker(승격 심사 문서 집행 주체)는 승격을 결정하지 않고 물리 집행만 한다.
5. **Module 구현 디렉터리 문서 본문에 특정 Adapter 문서명·물리 토큰 금지**(C-3 확장). framework/core·runtime·loop·memory·verifier·workflow·plugins **7 디렉터리군**(25파일)에 이 경계 적용(T9 §3.3 전수 스캔 매치 0 실측). **Core Claude 의존 0건은 유지 대상.** **generic 경계**(framework/adapters/generic/ 2파일)에는 특정 AI 실명·타 Adapter 경로 불명명 경계(DP-V6·DP-V14, 매치 0 실측).
6. **픽스처 경계** — docs/v0.5~v0.9-demo-fixtures/ + **docs/v1.0-generic-demo-fixtures/**(16파일)·**dogfooding/uahf-lessons/**(35파일, 응용 코드부·언어 토큰 정당 보유)는 정당 보유 격리 지점(DP-V13). 전수 스캔 시 제외 명시(verifier_scope 관례). 단 설치본 Core부(dogfooding framework/core·runtime 7파일)의 CK-6 재스캔·generic 경계 2파일 정체성 스캔은 수행 대상이다(격리 예외).
7. **scaffold-template/은 설치 원본**(13파일) — 신규 프로젝트 설치가 이 원본을 복사·매핑(`dot-claude/*`→`.claude/*`)한다. **수정 시 scaffold-binding.md §6과 정합 필수.** install-manifest.template.md front-matter는 frameworkVersion **"v1.0"**·specVersion "v0.1"(v1.0 T3 DP-V10 동기화).
8. **설치본 시점 스냅샷 의미론** — dogfooding 설치본 `framework/core/structure.md`는 배치 시점(23:30) 원본의 충실한 스냅샷이며, 사후 라이브 개정(T8 23:56)과의 divergence는 설치 결함·거짓 완료가 아니다(Advisor 수용). 재설치 시 갱신 선택지. CK-6(설치본 Core AI 0)은 불변.
9. **라이브 표면 위생(DP-E7)** — `.claude/hooks/`·`.claude/skills/`에는 정상 레퍼런스만 존치. 결함 픽스처는 격리 경계에만 배치한다. v1.0이 추가한 라이브 지점은 선언 산출물(scaffold-binding·scaffold-template·structure.md·generic 경계 2파일·loop-data v10)뿐 — 무단 산출·경계 밖 수정 0.
10. **DP-E8** — Verifier·Planner 위임은 `model: opus` 명시. v1.0 완료로 "영구 관행" 문구는 **차기 세션 재확인 대상으로 승계**(계약(06) 변경이 아니라 실행 모델 바인딩(02 §4.1)). Agent 기동 설정(.claude/agents/ 이하) 개정은 사용자 직접 지시 권한 경로로만(L-14).
11. **시연·개발 기록의 성격** — v1.0 Dogfooding은 **단일 사이클·단일 흐름**(설치→Bootstrap→루프 1사이클으로 실제 프로젝트 개발 완주, BPD-11 Active). memory timestamp·loop-data `at`·Install Manifest `timestamp`는 순서 값이며 물리 벽시계 시각이 아니다(L-09). memory source 라벨은 `v1.0-review`(Task 번호 표기 관례 미확정 — §1.6-b).
12. **Glossary 0.2 Frozen 유지** — v0.9 승격으로 Frozen(사용자 승인). v0.1 기준선의 Frozen 지위를 소급 해제하지 않는다. 재개정은 spec-versioning-policy §3.1 대전제(버전 상승 + 이력 append).
13. **Frozen specs 계수 = 15**(numbered 00~13 = 14 + TEMPLATE 1 — 직접 실측). 계수 표기 자리에는 15를 쓴다.
14. **하네스 Bootstrap 유지** — v1.0 종료 시점에도 부트스트랩 상태다(전이 조건 3 미충족, DP-U1 승계 귀결). Formal 전이는 형태 B 실행 호스팅 도입 시로 유보(v1.0 이후 사안·§2.3).
15. **계수 갱신 요약(실측)** — loop-data **11파일/83 line** · memory store **71파일**/index **71라인** · Frozen specs **15** · framework/adapters/ **2 Adapter**(claude·generic) · framework/adapters/claude/ **15엔트리**(바인딩 12 .md + loop-data·memory-data·scaffold-template) · framework/adapters/generic/ **2파일** · 바인딩 문서 **12+2** · Memory Active **20**(Lesson 15 + BP 5)·Candidate **18**.
16. **다음 트랙 미정 — 선취 금지** — ROADMAP v1.0까지 완료로 다음 트랙은 사용자 결정 사항이다(§3.1). 차기 세션은 트랙을 스스로 채택하지 말고 사용자에게 결정을 요청한다(§4 Bootstrap Prompt 구조).
