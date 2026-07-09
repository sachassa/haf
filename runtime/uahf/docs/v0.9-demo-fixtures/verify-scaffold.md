# v0.9 Scaffold 시연 — CP2 독립 검증 리포트 (verify-scaffold.md)

> **시연 픽스처 CP2 검증 리포트 — 실계약 문서·라이브 설정 표면 아님.**
> 이 리포트는 `docs/v0.9-demo-fixtures/` 경계 안의 격리된 설치 시연 픽스처에 대한 독립 판정이다.
> 판정 대상은 라이브 `.claude/`·라이브 계약 문서(`framework/`·`specs/` 정본)·라이브 하네스 상태가 아니다.
> 검증 주체(Verifier, model: opus)는 구현 주체(설치를 수행한 Worker, seq4)와 분리된다. Worker 완료 보고(seq4)의
> "충족" 주장은 판정 근거로 삼지 않았다 — 산출물 자체를 정독·재스캔한 실측만 근거다 (06 V1, L-07).

- 검증 게이트 위치: CP2 (Worker 자체 점검 CP1 뒤, Advisor 최종 승인 CP3 앞) — 03 §3.1-A.
- 사이클: `v09-demo-scaffold` (seq5, Verify→Learn 전이의 산출).
- 판정 시각 기준: order 값(VCS 부재 시점 제약, L-09) — 물리 벽시계 시각 주장 아님.

---

## 1. target (판정 대상)

| 대상 | 경로 | 성격 |
|---|---|---|
| ① Install + ⑤ 재설치 후 설치본 | `docs/v0.9-demo-fixtures/new-project/` | 실물 설치 구조 (`.claude/*`, `framework/{core,runtime,adapters}/`, `specs/`, `install-manifest.md`, `README.md`) |
| ① 최초 설치 스냅샷 | `docs/v0.9-demo-fixtures/install-manifest-initial.md` | preservedPaths `[]` (빈 프로젝트) |
| ⑤ 재설치 후 매니페스트 | `docs/v0.9-demo-fixtures/new-project/install-manifest.md` | preservedPaths `[README.md]` |
| ⑤ Uninstall 결과 | `docs/v0.9-demo-fixtures/new-project-uninstall-copy/` | 잔여물 판정 대상 |
| 루프 상태 기록 | `framework/adapters/claude/loop-data/v09-demo-scaffold.jsonl` | 7 line |

대상 작업 식별자: `t-sd` (v0.9 단일 Task Work Graph — 설치 시연 오케스트레이션 사이클).

---

## 2. criteria_basis (대조 기준 출처 — 재정의 없음, 인용만)

- **정본 CK-1~CK-8**: `specs/12-scaffold.md §3.2-C` (설치 검증 체크리스트). 라이브 정본과 byte 동일한 설치본 `specs/12-scaffold.md`로 교차 확인.
- **Bootstrap 계약**: `specs/01-runtime.md §3.1-C` (Bootstrap 입력·완료 조건·state=Ready/Degraded).
- **최소 구성 집합**: `specs/13-harness.md §3.2-A` (5 필수 요소 — 상위 규약 문서·Agent 역할 4종·위임/보고 프로토콜·검증 게이트·작업 추적).
- **Config 스키마**: `specs/01-runtime.md §3.2-B` (3스코프·우선순위 Module>Project>Global·결정성). 설치본 `framework/core/config-schema.md`가 그 인스턴스.
- **Scaffold 불변 규칙**: `specs/12-scaffold.md §3.3` INV-3(기존 파일 보호)·INV-4(멱등성)·INV-5(제거 안전)·INV-6(Core AI 비의존)·INV-7(버전 정합).
- **금지 토큰 규칙**: `01 §3.3 INV-4` / 설치본 `framework/core/structure.md §5` (확정 조건 C-3).

검증 방법(scaffold-binding §5): 존재·정독=파일 조회(Read/Glob), 전수 스캔(CK-6)=텍스트 검색(Grep 금지 토큰 후보 전 범위), byte 동일성=md5 해시 대조(Bash).

---

## 3. items (CK-1 ~ CK-8 항목별 판정)

### CK-1 — Project Template 필수 6요소의 설치 대상 경로 실재 · verdict: **충족(Met)** · verification_type: VT-1

**evidence (실측 파일 조회):**
1. 규약 문서: `new-project/.claude/AGENT.md`·`.claude/CLAUDE.md` 실재.
2. Agent 정의 4종: `.claude/agents/{advisor,planner,worker,verifier}.md` 4개 모두 실재.
3. Config: `.claude/settings.json` 실재 (+ Project scope 소스 CLAUDE.md·AGENT.md).
4. specs 자리: `new-project/specs/` 실재 — 00~13 (14개) + `TEMPLATE.md` + `README.md`.
5. Core/Adapter 경계: `framework/core/`·`framework/runtime/`·`framework/adapters/` 3경계 모두 실재.
6. Install Manifest: `new-project/install-manifest.md` 실재.

`installedArtifacts` 목록 12항 전체가 파일 시스템에 실재함을 대조 확인 — 매니페스트 주장과 실물 불일치 0건 (거짓 완료 보고 검출 결과 없음).
**scope:** `new-project/` 트리 전수 파일 조회. 6요소 = 12 §3.2-A 표(Config 2행을 delegation 표기대로 1요소로 집계).

### CK-2 — installedModules `[runtime,agent,verifier]`가 최소 필수 집합 포함 · "필요한 모듈만" · verdict: **충족(Met)** · verification_type: VT-2

**evidence:**
- 두 매니페스트의 `installedModules` = `runtime` · `agent` · `verifier` (실측).
- 13 §3.2-A 5요소 대응: `agent` → Agent 역할 4종 + 위임/보고 프로토콜(02 §3.2-B/C/D); `verifier` → 검증 게이트(06); `runtime` → 호스팅 환경(01 §3.1-C Bootstrap). 상위 규약 문서·작업 추적은 설치된 규약 문서(`.claude/AGENT.md`)·루프 상태 기록으로 실현 — Bootstrap 필수 계약을 완비.
- "필요한 모듈만": 선택 Module(memory·loop·workflow·plugins)의 구현 디렉터리는 `installedArtifacts`에도 실물 `new-project/framework/`에도 부재. 실물 framework 하위는 `core/`·`runtime/`·`adapters/` 3경계뿐 — 선택 Module 0건 (12 INV-2 Modular).
**scope:** 두 매니페스트 front-matter + 실물 framework 디렉터리 구성 대조.

### CK-3 — Config Project scope 소스 실재 · 01 §3.2-B 스키마 정합 · verdict: **충족(Met)** · verification_type: VT-3

**evidence:**
- Project scope 소스 3종 실재: `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.json`.
- `settings.json`: `framework.retry.limit = 2` 표기, 주석에 "기본값 2는 Global scope 소속·Project override 가능" 명시 — config-schema.md §7 DP-1 해소값(기본값 2, Global scope + Project/Module override)과 정합.
- 우선순위: `.claude/CLAUDE.md`가 "Config 우선순위는 Module > Project > Global (01 §3.2-B)" 명시 — 01 §3.2-B 스키마 방향과 일치.
- Global scope는 사용자·환경 전역 설정 소관이며 Scaffold 미덮어쓰기 — CLAUDE.md·12 §4.1과 정합(픽스처 경로 대상 아님).
**scope:** `.claude/settings.json`·CLAUDE.md·AGENT.md 정독 대조. Global scope 물리 소스(사용자 환경)는 픽스처 경계 밖 — verifier_scope 제외.

### CK-4 — 설치 직후 Runtime Bootstrap 성공(Ready/Degraded) · verdict: **충족(Met)** · verification_type: VT-5(형태 A 문서 절차)

**evidence (형태 A 완비 판정 — 01 §3.1-C 필수 계약 Resolve 가능성):**
- 필수 계약 완비: 호스팅(runtime 프로토콜 문서 3종 `lifecycle.md`·`module-manifest.md`·`module-registry.md` 실재) + Agent 역할 4종(agents/*.md 4개) + 검증 게이트(verifier.md + 06 spec) 모두 존재하여 Resolve 가능.
- 01 §3.1-C 완료 조건("모든 필수 계약이 Resolve → Ready"): 필수 계약 미해소 요소 0건.
- **state 결과: `Ready`** (선택 계약 누락으로 인한 Degraded 강등 요인도 판정 대상 아님 — 최소 집합이 필수 계약을 완비).
**scope:** 설치된 구조의 필수 계약 완비 여부를 형태 A(문서 절차) 관점에서 판정. 라이브 런타임 실행 관측 아님 — 시점 제약(DP-E7). 판정 근거는 구조 완비성이며 물리 실행 트레이스가 아니다(정직 명시).

### CK-5 — Bootstrap 이후 Loop 최소 1 사이클 구동 · verdict: **충족(Met)** · verification_type: VT-5

**evidence (`v09-demo-scaffold.jsonl` 7 line 실측):**
- 7단계 완주: seq1 Consult → seq2 Plan → seq3 Execute → seq4 Verify → seq5 Learn → seq6 Memory Update → seq7 Complete (Consult→…→Complete 전 단계 통과).
- `retry_count`: 7 line 전부 `0` (실측 grep — retry_count:0 ×7).
- 구현 주체/검증 주체 분리: seq4 `actor:Worker`(completion-report-cp1), seq5 `actor:Verifier`(verification-report) — 분리 확인.
- `actor=human` 0건 (실측 grep count = 0). 전이 actor 분포: Advisor×4·Verifier×2·Worker×1.
- 최소 구성 집합 지지: 규약 문서·Agent 4종(Advisor·Worker·Verifier 전이 actor + Planner seq2 ref)·검증 게이트(seq5 CP2)가 핵심 루프를 지지.
**scope:** 루프 상태 기록 아티팩트 7 line 전수 정독. 기록의 내부 정합성 판정이며 라이브 루프 엔진 실행 재현 아님.

### CK-6 — 설치된 Core 디렉터리 AI 의존 요소 0건 · **전수 스캔** · verdict: **충족(Met)** · verification_type: VT-4(경계 — 전수 스캔)

**evidence (금지 토큰 후보 집합 전 범위 전수 스캔 — 단일 대리 지표 대체 아님):**
- 스캔 대상: `new-project/framework/core/`(README·config-schema·structure) + `new-project/framework/runtime/`(README·lifecycle·module-manifest·module-registry) 전 문서.
- 스캔 후보 집합(Grep, case-insensitive):
  - AI 이름·모델명: `claude|anthropic|openai|gpt|chatgpt|gemini|copilot|llama|mistral|cohere|bard|opus|sonnet|haiku` → **0건** (core·runtime 양쪽).
  - 언어·툴체인·직렬화 형식: `python|javascript|typescript|golang|rust|kotlin|swift|ruby|php|scala|haskell|node(.js)|npm|pnpm|yarn|cargo|gradle|maven|webpack|json|yaml|yml|toml|xml|protobuf` → **0건** (core·runtime 양쪽).
  - 환경·제품: `docker|kubernetes|k8s|aws|gcp|azure|linux|unix|posix|windows|macos|sqlite|postgres|mysql|redis|grpc|graphql|bash|powershell|markdown|jsonl|.py/.js/.ts/.rs/.go` → **0건** (runtime), core는 `.md` 문서 파일명 참조만(config-schema.md·structure.md 등).
- 잔여 `AI` 문자열은 전부 카테고리 명("특정 AI 이름·모델명…")·규칙 서술("AI 비의존") — delegation 명시상 금지 토큰 아님. 컴포넌트/문서 파일명(config-schema.md 등)·`<adapter>` 일반형 placeholder도 금지 토큰 아님.
- 8개 문서 전문 정독으로 교차 확인 — 구체 인스턴스 자리는 전부 "Adapter Binding 문서 소관" 포인터·`<adapter>` 일반형으로 대체됨.
**scope:** `framework/core/`·`framework/runtime/`만(CK-6 정의 경계). `framework/adapters/`는 격리 지점이므로 CK-6 범위 밖 — adapters/README.md의 구체 어댑터명은 정상 격리(위반 아님).

### CK-7 — Install Manifest 존재 + front-matter frameworkVersion·specVersion 표기 · verdict: **충족(Met)** · verification_type: VT-3

**evidence (front-matter 실측):**
- `new-project/install-manifest.md`: `frameworkVersion: "v0.9"` · `specVersion: "v0.1"` 표기.
- `install-manifest-initial.md`: 동일 표기 `frameworkVersion: "v0.9"` · `specVersion: "v0.1"`.
- 두 매니페스트 모두 존재하고 필수 버전 2필드 표기 — 12 INV-7 정합.
**scope:** 두 매니페스트 front-matter 정독. 버전 값의 릴리스 정합성은 Adapter Binding 소관(값 표기 존재만 판정).

### CK-8 — 기존 파일 보존 + preservedPaths 정합 + 멱등성 diff 0 + Uninstall 잔여물 0 · verdict: **충족(Met)** · verification_type: VT-4 + VT-2

**evidence:**
- **보존(INV-3):** `new-project/README.md`와 `new-project-uninstall-copy/README.md` md5 동일 = `d2594c91c1d471bfc193dc87d6a8035f`. 사용자 고정 마커 `USER-OWNED-CONTENT-v0.9-DEMO-PRESERVE-MARKER-7f3a` 양쪽 실재. README 무변경 대조.
- **preservedPaths 정합:** 최초(빈 프로젝트) `preservedPaths: []`, 재설치 후 `preservedPaths: [README.md]` — 실제 상태(사전 배치 사용자 파일 README.md 존치)와 일치.
- **멱등성 diff 0(INV-4):** 두 매니페스트의 `installedModules`+`installedArtifacts` 블록 diff 결과 유일 차이는 `preservedPaths`뿐(설치 산출물 descriptor 동일). 실물 설치 산출물 byte 동일성 표본 대조:
  - `.claude/{AGENT,CLAUDE}.md`·`agents/{advisor,planner,worker,verifier}.md`·`settings.json` → scaffold-template 원본과 md5 **전부 IDENTICAL**.
  - `framework/{core,runtime,adapters}/README.md` → scaffold-template와 md5 **전부 IDENTICAL**.
  - `framework/core/{structure,config-schema}.md`·`framework/runtime/{module-manifest,module-registry,lifecycle}.md` → 라이브 기준선과 md5 **전부 IDENTICAL**.
  - `specs/` 00~13 (14개) + TEMPLATE.md → 라이브 기준선과 md5 **전부 IDENTICAL**. `specs/README.md`는 scaffold-template placeholder와 IDENTICAL(라이브 specs/README.md 부재 — 템플릿 자리 문서, 예상된 출처).
- **Uninstall 잔여물 0(INV-5):** `new-project-uninstall-copy/` 실물 파일 = `README.md` **단 1건**. installedArtifacts만 제거되고 preservedPath(README.md)만 잔존 — 잔여물 0, README hash 무변경.
**scope:** md5 해시 표본 대조 + uninstall-copy 트리 전수 파일 조회 + 두 매니페스트 diff.

---

## 4. final_verdict (최종 판정 — 06 §3.2-C 결정적 도출)

**충족(Met) 8 / 위반(Violated) 0 / 판정 불가(Undetermined) 0**

모든 대조 기준 항목(CK-1 ~ CK-8)이 충족(Met)이며, 위반·판정 불가 0건이다.
06 §3.2-C 규칙("모든 항목 충족 → 통과") 적용 →

# **final_verdict: 통과 (Pass)**

동일 항목별 판정 집합은 항상 동일한 최종 판정을 낸다(INV-5 결정성). 거짓 완료 보고 검출 결과: 매니페스트 주장 대비 실물 불일치 0건.

---

## 5. verifier_scope (실제 검사 범위 · 제외 경계 명시)

**검사한 범위:**
- `new-project/` 전 산출물 정독(파일 조회) + `.claude/`·`framework/{core,runtime,adapters}/`·`specs/` byte 동일성 md5 대조.
- CK-6 전수 스캔: `framework/core/`·`framework/runtime/` 8문서, 금지 토큰 후보 3집합(AI·언어/툴체인/형식·환경/제품) 전 범위.
- `v09-demo-scaffold.jsonl` 7 line 전수 정독 + retry_count·actor·human 실측 grep.
- 두 매니페스트 front-matter + installedArtifacts/Modules diff + uninstall-copy 트리 전수.

**제외 경계(판정 대상 아님):**
- **픽스처 경계 한정** — 이 리포트는 `docs/v0.9-demo-fixtures/` 격리 시연본만 판정한다. 라이브 `.claude/`·라이브 계약 정본(`framework/`·`specs/`)·라이브 하네스 상태는 대상이 아니다.
- **라이브 표면·픽스처의 물리 토큰 정적 스캔 제외(DP-E7)** — CP2 §3 정적 스캔 verifier_scope 제외 관행에 따라, `framework/adapters/` 경계(격리 지점)의 구체 어댑터·환경 토큰은 CK-6 판정 대상에서 제외. adapters/README.md의 구체 어댑터명 표기는 정상 격리이며 위반이 아니다.
- **CK-4/CK-5는 형태 A(문서 절차·기록 아티팩트) 관점 판정** — 라이브 Runtime Bootstrap 실행·라이브 Loop Engine 구동의 물리 실행 트레이스는 관측하지 않았다. 시점 제약(VCS 부재, L-09) 하에서 구조 완비성·기록 정합성을 근거로 판정했으며, 이를 물리 실행 관측으로 과대주장하지 않는다.
- **버전 값·직렬화 형식의 릴리스 정합성** — Adapter Binding 소관. 필수 필드의 표기 존재만 판정(값의 대외 정확성 아님).
- **Global scope Config 물리 소스** — 사용자·환경 전역 설정(픽스처 경계 밖). 존재·정합 판정 대상 아님.

---

## 6. rework (재작업 지시)

**없음** — final_verdict = Pass. 위반·판정 불가 항목이 0건이므로 재작업 지시 대상이 없다.

---

*작성: Verifier (UAHF Verifier Agent, model: opus) · CP2 독립 판정 · 사이클 v09-demo-scaffold seq5.*
*판정 근거는 전부 실측(경로·md5 해시·Grep 스캔 결과·line 카운트)이며, 근거 없는 "충족"은 기록하지 않았다(L-07). Worker 완료 보고(seq4)는 검사 대상(claim)일 뿐 판정 근거로 삼지 않았다(06 V1).*
