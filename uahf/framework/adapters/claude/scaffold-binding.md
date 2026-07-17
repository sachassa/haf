# framework/adapters/claude/scaffold-binding — Claude Code Scaffold Adapter 바인딩

작성일: 2026-07-06
상태: v1.0 Baseline (개정 r2 — §4 frameworkVersion v1.0 동기화·근거 괄호 정합 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-07 · 직전 기준선: v0.9 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/12-scaffold.md §3(Core Contract — §3.1 Install/VerifyInstall/Uninstall 3연산·§3.2-A Project Template 필수 6요소·§3.2-B Install Manifest 6필드·§3.2-C 설치 검증 체크리스트 CK-1~CK-8·§3.2-D Failure Report·§3.3 Invariants INV-1~INV-8)와 §4.1(Claude Code 바인딩 표 10행)·§4.2(이식 교체 지점 1~7). **Frozen(v0.1 기준선). 본 문서가 실현하는 계약의 정본이며, 재정의·확장하지 않고 § 포인터로만 인용한다.**
- framework/adapters/claude/adapter-conformance.md (T1 확정본) §4(정식화 배정표 — 본 Task가 `scaffold-binding.md`·`scaffold-template/` 배정의 이행)·§5(Advisor 결정 DP-A3 — `framework/scaffold/` 미신설). 본 문서는 이 배정을 이행하고 DP-A3을 준수한다.
- specs/13-harness.md §3.2-A(최소 구성 집합 5요소 — Scaffold 설치 대상, 12 §9 OQ-2 결정·13 §3.2-B 전이 조건 4). Install moduleSelection 최소 집합의 성립 대상. § 포인터로만 참조.
- specs/01-runtime.md §3.1-C(Bootstrap 계약 — 설치 결과가 충족해야 할 상태 Ready/Degraded)·§3.2-B(Config 스코프·우선순위)·§4.1(디렉터리 바인딩 표). BP·물리 정본. § 포인터로만 참조.
- framework/adapters/claude/runtime-binding.md §3.3(Config 3스코프 물리 소스)·§3.4(세션/턴 = Bootstrap~Serve~Shutdown 수명주기). Config·Bootstrap 호스트의 선행 관례.
- framework/adapters/claude/memory-binding.md §3 — 정본 프로토콜의 물리 절차 1:1 단계 대응 관례(§3의 3연산 절차 대응이 이 관례 동형).
- framework/adapters/claude/verifier-binding.md §5 — VT-1~VT-5 검사 도구 바인딩 관례(§5의 CK 물리 검사 방법이 이 관례 참조).
- framework/adapters/claude/loop-binding.md §2 — Loop 사이클 구동(핵심 루프)의 세션/턴·서브에이전트 채널 실현(CK-5 대응 참조). Baseline 자매 문서.
- framework/core/structure.md §2·§5·§8 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·금지 토큰 규칙·§8 트리. 본 문서 경계·물리 분리의 근거.
- specs/00-glossary.md §3.2-D(Component→Layer 매핑 — Scaffold = Presentation Layer, 12 §9-OQ1 결정)·§3.2-J(J-12 — Project Template·Install Manifest·설치 검증 체크리스트 표제어 정본). 본 문서는 새 용어를 신설하지 않는다.
- .claude/AGENT.md·.claude/CLAUDE.md·.claude/agents/ 4종(advisor·planner·worker·verifier.md) — 템플릿 초기본의 원형(현행 라이브 실물). 본 문서는 참조만 하고 수정하지 않는다(07 R4).
- Active Lesson L-07 (상태 서술은 실측 후 기록 — A5 재작업 사례에서 도출). §8 실측 대조의 근거.
- ROADMAP.md v0.9(Adapter Layer & Scaffold — "Scaffold 도구와 프로젝트 템플릿"·"신규 프로젝트 설치 가이드" 산출물)·Component Coverage(Scaffold v0.9 정식화). 완료 조건 "설치 → 루프 동작"의 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 12 §3.3 INV-6, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, 자매 바인딩 8문서 §0과 동형). 단 이 문서는 Core Contract(12 §3)를 **재정의·확장하지 않는다** — 계약(연산·데이터 포맷·체크리스트·불변 규칙)은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.9 Draft | 최초 작성. `framework/adapters/claude/` 경계의 Scaffold 물리 실현 산출물(선행 자매 바인딩 8문서: runtime·memory·verifier·loop·workflow·hooks·skills·plugins-binding.md + 적합성 판정 adapter-conformance.md에 이음). adapter-conformance.md §4 배정표의 T4 배정(scaffold-binding.md·scaffold-template/) 이행. 12 §4.1 바인딩 표 **10행 전건**을 물리 실현("물리 실현" + "실재 여부" 열, 형태 A/B 정직 구분 — 설치 절차는 형태 A 문서 절차, DP-U1)으로 매핑(§2). Install/VerifyInstall/Uninstall 3연산의 물리 절차를 12 §3.1과 **1:1 단계 대응**으로 확정(memory-binding.md §3 관례 동형, §3). Install Manifest 직렬화 확정 — Markdown + front-matter 형식·6필드 물리 표기·`frameworkVersion`=`v0.9`·`specVersion`=`v0.1`(기준선) 값(§4). CK-1~CK-8 각각의 물리 검사 방법(검사 도구 바인딩 — verifier-binding.md §5 VT 관례 참조, §5). scaffold-template/의 구조·내용 목록을 정본으로 확정(13파일, `dot-claude/`→`.claude/` 매핑, Core부 CK-6 자체 전수 스캔 0건, §6). 12 §4.2 이식 교체 지점 1~7 대응 표("교체되는 것/유지되는 것", §7). 상태 서술 실측 대조 표(§8 — 실재 서술 전건 파일 시스템 직접 실측 후 기입, L-07). Advisor 결정 DP-A3(`framework/scaffold/` 미신설) 준수·DP-U1(설치 절차 = 형태 A 문서 절차) 기록. 12 §3 계약 재정의·확장 0·§ 포인터 인용만·Frozen specs 계수 15·Glossary 밖 새 용어 0. 형제 Task(agent-binding·harness-binding·.claude/commands/·getting-started·Glossary 개정분·hooks/plugins-binding §7 개정분) 불인용(07 R2). 라이브 표면(.claude/·framework/core/·framework/runtime/ 실물) 무수정 — 이 3산출물(scaffold-binding.md·scaffold-template/·docs/v0.9-install-guide.md)만 생성(07 R4). | Worker (Advisor 위임, Task T4) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v1.0 Draft (개정 — frameworkVersion 동기화) | Install Manifest `frameworkVersion` 값을 `"v0.9"`→`"v1.0"`으로 동기화. **갱신 지점(값 서술 6지점):** §1 목적·§2 표 행8·§4 필드 표·§4 버전 정합 주·§7 이식 교체 지점 표 행6·§11 요약 + `scaffold-template/install-manifest.template.md` front-matter 1지점. §9 OQ-SB-3에 해소 표기(v1.0 T3) 병기(§10 open_questions). **`specVersion`=`"v0.1"`은 무변경**(spec 기준선 Frozen 고정 — OQ-SB-3 문면). **불변 유지:** 문서 버전·§9 이력 행(L-10)·"v0.9 시점"/"v0.9 산출물" 시점 기록·근거 정본 ROADMAP.md v0.9 참조·§4 필드 표 "(ROADMAP v0.9)" 근거 표기·`docs/v0.9-install-guide.md` 파일명. 12 §3 계약(6필드·CK-1~8·INV·사유 코드) 재정의 0 · scaffold-template/ 나머지 12파일·자매 바인딩 문서·specs/·docs/ 무수정(07 R4). 유형 (B) 비계약 정합·격리 개정(spec-versioning-policy §3.2 — 이력 append + 상태 라인 갱신). Advisor 결정 DP-V10(사용자 승인 2026-07-06 계획). | Worker (Advisor 위임, Task T3) |
| 2026-07-06 | v1.0 Draft (r2 — 근거 괄호 정합) | OQ-W1 Advisor 재량 해소 — 값에 결합된 근거 괄호는 값 서술의 일부이며 시점 기록이 아니다. §4 필드 표 frameworkVersion 행의 근거 괄호 `(ROADMAP v0.9)`→`(ROADMAP v1.0)` 갱신(값이 v1.0이 된 지금 "현 릴리스"의 근거 = ROADMAP v1.0 섹션). **동종 전수 대조(L-06·BP-01 — `ROADMAP v0.9` 3지점):** line 138 값 결합 근거 괄호 = 갱신 / line 20 근거 정본 목록(문서 유래)·line 32 r1 이력 행(시점 기록) = 불변(L-10). 그 외 무변경 — `specVersion`=`"v0.1"` 불변·install-manifest.template.md 무접촉(이 사안 해당 없음). r1 위임문 "ROADMAP v0.9 참조 갱신 대상 아님" 규칙의 과잉 전칭을 Advisor 소관 결함으로 정정(값 결합 근거 괄호는 그 규칙 적용 대상 아님). 12 §3 계약 재정의 0. | Worker (Advisor 개정 지시, Task T3 r2) |
| 2026-07-07 | v1.0 Baseline | v1.0 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 21/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지)·삭제 산출물 참조(docs/v0.9-install-guide.md §8 실측 행) @cd9247b 앵커 전환. scaffold-template/·framework 경로는 계약·라이브로 유지. 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/12-scaffold.md §3(§3.1 3연산·§3.2 데이터 포맷·§3.3 Invariants)과 §4(§4.1 바인딩 표·§4.2 이식 교체 지점)다.** 이 문서는 그 계약의 **환경 실현 매핑 + 프로젝트 템플릿(scaffold-template/) 정본**이며, 계약 요소(연산·필드·체크리스트 항목·불변 규칙·사유 코드)를 **재정의·확장하지 않는다**. 계약 요소는 12 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 12 §4.1이 "규약 문서·Agent 정의·Config·specs·Core/Adapter 경계·Install Manifest·버전 값·Bootstrap/Loop 구동 확인"의 구체 물리 경로·직렬화 형식을 이 바인딩에 미룬 지점, 그리고 12 §3.2-A Project Template의 **물리 자산(scaffold-template/)** 이 실재하는(확정되는) 유일한 자리다. 개별 계약의 정본은 12 §3이며, 본 문서는 그 물리 실현만 확정한다.
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3, 12 §3.3 INV-6). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형식명, 물리 경로 `framework/adapters/claude/…`·`.claude/…`·`~/.claude/…`·`specs/…`·`docs/…`, 세션/턴, 서브에이전트 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 바인딩 8문서 §0과 동형). **단 이 허용은 Frozen 12 §3 계약 문면을 바꿀 권한이 아니다** — 12는 무변경, 인용만 한다.
- **프로젝트 템플릿(scaffold-template/) 물리 정본 선언(done 2).** 12 §3.2-A Project Template의 물리 자산은 **Adapter 경계 이하 `framework/adapters/claude/scaffold-template/`로 확정한다**. **구조·내용 목록·`dot-claude/`→`.claude/` 이름 변경 매핑의 정본은 이 문서(§6)다.** 12 §4.1은 이 물리 위치를 "Adapter Binding 문서 소관"으로 미뤘고, 본 문서가 그 소유자로서 확정한다. 이 템플릿의 Core부(`framework/core`·`framework/runtime` 대응 자리)는 AI 의존 토큰 0건이며(§6, CK-6 자체 전수 스캔), 이는 그 물리 위치가 Adapter 경계 이하임(격리 지점, C-3 허용)과 무관하게 **설치된 Core 디렉터리가 CK-6을 통과하도록** 의도된 것이다.
- **창설 금지.** 이 문서는 12 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.9 산출물(Scaffold 설치·초기화 표면·프로젝트 템플릿·설치 가이드)의 물리 실현 매핑으로 한정한다. 새 연산·필드·CK 항목·사유 코드·불변 규칙을 만들지 않는다.
- **하네스 상태 전제(Bootstrap) + DP-U1.** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, 자매 바인딩 §0, delegation-protocol.md §0). Scaffold는 정식 실행 Module이 아니라 규약 문서(12·본 문서)와 관행으로 실현된다(형태 A). **Advisor 결정 DP-U1(본 위임에서 지시됨):** Install/VerifyInstall/Uninstall 3연산은 Bootstrap에서 **형태 A 문서 절차**로 실현되며, 무인 실행기(형태 B)는 미도입이다. 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(scaffold-template/ 자산·라이브 원형 실물 — §8 실측)과, **실행 코드 도입 시 로딩될 지점**(형태 B — 설치 실행기·검증 실행기)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **DP-A3 준수.** Advisor 결정 DP-A3(adapter-conformance.md §5)에 따라 `framework/scaffold/` 디렉터리를 신설하지 않는다. Scaffold의 물리 실현은 이 문서 + scaffold-template/ + 12 §4.1 바인딩 값(`.claude/*`·`specs/`·`framework/` 초기화)으로 실현한다. Scaffold는 Runtime이 호스팅하는 Module이 아니라 Bootstrap 이전 설치 도구다(12 §2·§5). `framework/scaffold/` 부재는 §8 실측으로 확인한다.
- **실측 기반 상태 서술(L-07).** "실재/존재/부재" 주장은 파일 시스템 확인 후에만 기입한다(Active Lesson L-07 — 상태 서술은 실측 후 기록, A5 재발 방지). §2 "실재 여부" 열·§8 실측 대조 표의 전 행은 파일 시스템 직접 실측(2026-07-06)에 근거한다 — 미존재를 실재로, 미래 산출물(설치 시 배치되는 대상 프로젝트 파일)을 현재 실재로 쓰지 않는다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Project Template·Install Manifest·설치 검증 체크리스트는 Glossary §3.2-J(J-12) 정본이며(12 §9 승격), Scaffold는 Glossary §3.2-D 기존 용어다. `형태 A/B`는 structure.md 서술 라벨의 인용이며 Glossary 표제어가 아니다. `DP-U1`은 본 문서가 기록하는 Advisor 결정 라벨(설치 절차 형태 A), `DP-A3`은 adapter-conformance.md §5가 기록한 Advisor 결정 라벨이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 Frozen specs/12의 Scaffold 계약(§3)을 Claude Code 환경 위에 **v0.9 시점의 구체 물리 실현**으로 매핑하고, 프로젝트 템플릿의 **물리 자산(scaffold-template/)** 을 정본으로 확정한다.

책임은 여섯 가지다.

- 12 §4.1 바인딩 표의 **10행 전건**을 물리 실현(경로·직렬화·설치 대상·구동 확인)으로 확정하고, Bootstrap 상태에서의 실재/규약 실현(형태 A)/형태 B 예정을 "실재 여부" 열로 정직하게 구분한다(§2, done 1).
- Install/VerifyInstall/Uninstall 3연산의 물리 절차를 12 §3.1 계약과 **1:1 단계 대응**으로 확정한다(§3, memory-binding.md §3 관례 동형, done 1).
- Install Manifest의 **직렬화 형식·6필드 물리 표기·버전 값**(`frameworkVersion`=`v1.0`·`specVersion`=`v0.1`)을 확정한다(§4, done 1).
- CK-1~CK-8 각각의 **물리 검사 방법**(검사 도구 바인딩)을 확정한다(§5, verifier-binding.md §5 VT 관례 참조, done 1).
- scaffold-template/의 **구조·내용 목록**을 정본으로 확정하고, 12 §3.2-A 필수 6요소와의 대응·`dot-claude/`→`.claude/` 매핑·Core부 CK-6 자체 전수 스캔 결과를 명시한다(§6, done 2).
- 12 §4.2 이식 교체 지점 1~7 각각에 "교체되는 것 / 유지되는 것"을 표로 명시한다(§7, done 1). 그리고 상태 서술을 실측과 대조한다(§8, L-07).

이 문서는 12 §3·§4의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A → 형태 B 전환 시에도 12 §3 Core Contract 변경은 0이며(structure.md §7 C-1), 이 문서(§7의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 12 §4.1 바인딩 표 10행 물리 실현 (done 1)

12 §4.1 Claude Code Binding 표의 **10행 전건**을 물리 표면으로 매핑한다. "12 §4.1 바인딩" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·형식·설치 대상·구동 방식을, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을 정직하게 구분한다(§8 실측 대조). **설치 절차 자체는 형태 A 문서 절차다(DP-U1).** "실재" 서술은 전건 파일 시스템 실측 후 기입했다(L-07).

| # | §3 계약 요소 (12 §3.2-A) | 12 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | 규약 문서 설치 | `.claude/AGENT.md`, `.claude/CLAUDE.md` 초기화 | 템플릿 원본 `scaffold-template/dot-claude/AGENT.md`·`dot-claude/CLAUDE.md`(초기본, §6) → 설치 시 대상 프로젝트 `.claude/AGENT.md`·`.claude/CLAUDE.md`로 배치. 계약 정본은 02(공통 규약)·CLAUDE.md 진입점 바인딩(02 §4.1). | 템플릿 원본 실재(§8 실측). 설치 실행기(형태 B)는 미도입 — 배치는 형태 A 문서 절차(DP-U1). |
| 2 | Agent 정의 설치 | `.claude/agents/{advisor,planner,worker,verifier}.md` (02 §4.1) | 템플릿 `scaffold-template/dot-claude/agents/{advisor,planner,worker,verifier}.md`(초기본 4파일) → 대상 `.claude/agents/*.md`. 실행 모델 지정(worker·planner·verifier `model: opus`, advisor 세션 상속)은 현행 실물 관행을 따르되, 그 의미 정본은 02 §4.1(실행 모델 바인딩)이다. | 템플릿 4파일 실재(§8 실측). |
| 3 | Config — Global scope 초기화 | 사용자·환경 전역 설정 파일 (01 §4.1) | Global scope(Framework 전역 기본값·병합 최저 우선순위)의 물리 소스는 사용자 전역 설정(`~/.claude/settings.json` 등, runtime-binding.md §3.3)으로 **사용자 환경 소관**이다. Scaffold는 이를 덮어쓰지 않고(INV-3 정신), Framework 전역 기본값을 문서 기본값(예: `retry.limit` 기본 2 — config-schema.md §7 소유)으로 제공한다. | 물리 소스는 사용자 환경 소관(Scaffold 미배치). 기본값 제공은 형태 A(문서 기본값). |
| 4 | Config — Project scope 초기화 | `.claude/CLAUDE.md`, `.claude/AGENT.md`, 프로젝트 설정 파일(settings.json 등) (01 §4.1) | 템플릿 `dot-claude/CLAUDE.md`(Project 지침·Config 안내)·`dot-claude/AGENT.md`·`dot-claude/settings.json.example` → 대상 `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.json`. 우선순위 Module > Project > Global(01 §3.2-B). | 템플릿 원본 실재(§8 실측). |
| 5 | specs 디렉터리 설치 | `specs/` 디렉터리 생성 | 템플릿 `scaffold-template/specs/`(자리 + 배치 안내 `specs/README.md`) → 대상 `specs/` 생성 후 spec 기준선(v0.1 Frozen, 15건 — numbered 00~13 + TEMPLATE) 배치. 배치 안내 정본 = 템플릿 `specs/README.md`. | 템플릿 자리·배치 안내 실재(§8 실측). 기준선 실배치는 설치 시(형태 A 절차). |
| 6 | Core / Adapter 경계 설치 | `framework/core/`, `framework/runtime/` (Core), `framework/adapters/`, `.claude/` (Adapter Binding) (01 §4.1) | 템플릿 `scaffold-template/framework/{core,runtime,adapters}/`(자리 README) → 대상 `framework/core/`·`framework/runtime/`·`framework/adapters/`; `.claude/`는 `dot-claude/` 배치로 실현. Core부 자리 문서는 AI 비의존(CK-6 대상, §6 자체 전수 스캔 0건). | 템플릿 자리 실재(§8 실측). Core부 CK-6 clean(§6). |
| 7 | Install Manifest 직렬화 (§3.2-B) | 프로젝트 내 매니페스트 파일 (Markdown + front-matter 또는 설정 파일) | 템플릿 `scaffold-template/install-manifest.template.md`(Markdown + front-matter, 6필드) → 설치 시 값 채워 대상 매니페스트 파일 배치. 직렬화 형식·필드 물리 표기 정본은 §4. | 템플릿 실재(§8 실측). 값 채움은 설치 시. |
| 8 | 버전 값 (`frameworkVersion` / `specVersion`) | 릴리스 시점의 Framework·spec 버전 문자열 | `frameworkVersion` = 문자열 `"v1.0"`(현 릴리스), `specVersion` = 문자열 `"v0.1"`(spec 기준선, Frozen). §4에서 확정·템플릿 front-matter에 표기. | 값 확정(정본, §4). |
| 9 | Runtime Bootstrap 호출 (CK-4) | Claude Code 세션/턴에서 Runtime Bootstrap 실행 (01 §4.1 수명주기 호스트) | 설치 직후 세션/턴을 실행 컨테이너로 삼아 Bootstrap을 수행(runtime-binding.md §3.4 — 세션 개시 = Bootstrap 구간). 필수 계약 해소 시 `state=Ready`, 선택 계약 일부 누락 시 `Degraded`. 구동 계약은 01 §3.1-C 소관 — Scaffold는 결과(state)만 판정(§5 CK-4). | 세션/턴 컨테이너 실재(현 세션). 실행 Bootstrap(형태 B)은 미도입 — 규약 실현(형태 A). |
| 10 | Loop 1 사이클 구동 확인 (CK-5) | Loop Engine 구동 (구동 계약은 03 소관) | Bootstrap 이후 Loop Engine이 핵심 루프(위임 → 구현 → 검증 → 승인)를 1 사이클 구동(loop-binding.md §2 — 서브에이전트 위임·최종 응답 채널로 실현). 구동 계약은 03 소관 — Scaffold는 사이클 통과 결과만 판정(§5 CK-5). | 핵심 루프 규약 실현(형태 A) — self-hosting 사이클로 반복 실증. 무인 자동 구동(형태 B)은 미도입. |

주:

- 위 10행은 12 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 12 §4.1 정본 표현을 이 환경의 구체 경로·형식·구동 방식으로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **물리 실재 / 형태 A / 형태 B 구분(정직).** scaffold-template/ 자산(행 1·2·4·5·6·7)은 물리 실재다. 설치·검증·제거 연산 자체(§3)와 Bootstrap/Loop 구동(행 9·10)은 Bootstrap에서 **규약 실현(형태 A)**이며(DP-U1), 무인 설치 실행기·검증 실행기·자동 구동 채널은 형태 B다. 행 3(Global scope)의 물리 소스는 사용자 환경 소관이라 Scaffold가 배치하지 않는다.
- **Layer 귀속.** Scaffold의 사용자 대면 호출 표면은 Presentation Layer에 귀속하고, 산출물(설치 구조)은 전 Layer에 걸치는 설치 도구 성격을 병기한다(Glossary §3.2-D, 12 §9-OQ1 결정). 본 문서는 이 매핑을 인용만 하며 재정의하지 않는다.

---

## §3. Install/VerifyInstall/Uninstall 3연산 물리 절차 — 12 §3.1 1:1 단계 대응 (done 1)

12 §3.1의 세 연산 계약을 이 환경의 물리 절차로 **단계 1:1** 대응시킨다(memory-binding.md §3의 프로토콜 단계 1:1 대응 관례 동형). 계약의 진위 판정 기준은 12 §3.1(완료 조건·Failure Report 사유 코드)이며, 본 절은 각 단계를 물리 절차로 실현할 뿐 재정의하지 않는다. **Bootstrap에서 이 절차는 형태 A 문서 절차로 수행된다(DP-U1)** — 무인 실행기(형태 B) 도입 시에도 12 §3.1 완료 조건·사유 코드 계약 변경은 0이다(structure.md §7 C-1).

### §3.1 Install 물리 절차

| 12 §3.1 Install 계약 단계 | 물리 실현 (claude 환경) | reason (실패 시) |
|---|---|---|
| **1** — 입력 접근성·`moduleSelection` 검사 | 대상 프로젝트 경로의 쓰기 가능 여부를 확인하고, `moduleSelection`이 Runtime Bootstrap 필수 계약 + 최소 구성 집합(13 §3.2-A 5요소)을 만족하는 최소 집합을 포함하는지 확인한다. 미달이면 어떤 파일도 배치하지 않고 거부한다. | `TargetNotWritable` / `ModuleSelectionInvalid` (INV-2) |
| **2** — 기존 파일 처리(`options` 보존 기본) | 대상에 충돌하는 기존 사용자 파일이 있으면 **보존**하고 `preservedPaths`에 기록한다. 강제 옵션 없으면 덮어쓰지 않는다(INV-3). 강제 옵션 시 경고와 함께 진행. | `ConflictWithExisting` (강제 시 경고 — INV-3) |
| **3** — Project Template 배치 | scaffold-template/ 자산을 대상 경로로 배치한다: `dot-claude/*` → `.claude/*`(이름 변경, §6), `framework/{core,runtime,adapters}/` → 동명 경계, `specs/` → `specs/`(+ 기준선 배치). 이미 존재하는 Scaffold 산출물은 재생성하지 않는다(멱등성 INV-4). | — |
| **4** — Install Manifest 생성 | §4 형식으로 매니페스트를 대상에 배치한다 — `frameworkVersion`·`specVersion`·`installedModules`(moduleSelection 해소)·`installedArtifacts`·`preservedPaths` 기록(INV-7). | — |
| **5** — 완료 조건 판정 | 설치 직후 Runtime Bootstrap(01 §3.1-C)이 `Ready`(또는 선택 계약 일부 누락 시 `Degraded`)로 성공하고, 설치 검증 체크리스트(§5, CK-1~CK-8) 전 항목을 통과해야 Install 완료. 미충족이면 설치 무효. | `BootstrapWouldFail` (INV-1) |

### §3.2 VerifyInstall 물리 절차

| 12 §3.1 VerifyInstall 계약 단계 | 물리 실현 (claude 환경) | reason (실패 시) |
|---|---|---|
| **1** — 입력 수령 | 설치된 프로젝트 구조 + Install Manifest를 대상으로 삼는다. | — |
| **2** — 체크리스트 항목별 실행 | CK-1~CK-8을 각각 §5의 검사 도구로 실행해 항목별 통과 여부를 판정한다(존재 확인·전수 스캔·시연). | — |
| **3** — 완료 조건 판정 | 체크리스트 전 항목이 통과하면 VerifyInstall 완료. 산출물 누락이 있으면 실패(location = 실패한 CK 항목). Bootstrap 필수 계약 미충족이면 `BootstrapWouldFail`. | `IncompleteInstall` / `BootstrapWouldFail` |

### §3.3 Uninstall 물리 절차

| 12 §3.1 Uninstall 계약 단계 | 물리 실현 (claude 환경) | reason (실패 시) |
|---|---|---|
| **1** — 입력 수령 | 설치된 구조 + Install Manifest를 대상으로 삼는다. | — |
| **2** — `installedArtifacts`만 제거 | Manifest의 `installedArtifacts`에 기록된 산출물만 제거한다. `preservedPaths`(사용자 소유 기존 파일)는 보존한다(INV-5). | — |
| **3** — 잔여물 보고 | 제거 후 남은 항목(Manifest 소유이나 제거되지 않은 것)이 있으면 잔여 경로를 보고한다. | `UninstallResidue` (INV-5) |

- reason 코드(TargetNotWritable/ConflictWithExisting/ModuleSelectionInvalid/BootstrapWouldFail/IncompleteInstall/UninstallResidue)와 공통 Failure Report 구조(operation/target/reason/location)의 정본은 12 §3.2-D다. 본 문서는 코드를 재정의하지 않고 물리 절차에 대응만 시킨다.
- **멱등성·제거 안전의 물리 보장(INV-4·INV-5).** Install 재실행 시 이미 존재하는 산출물은 재생성하지 않고(단계 3), 사용자 수정본을 덮어쓰지 않는다(단계 2). 제거는 `installedArtifacts`만 대상으로 하고 `preservedPaths`는 보존한다(§3.3 단계 2). Bootstrap(형태 A)에서 이 보장은 절차 준수 + 완료 후 대조(Manifest ↔ 실제 상태)로 성립하며, 더 강한 원자성은 형태 B 실행기 소관이다(추측·확정하지 않음).

---

## §4. Install Manifest 직렬화 확정 (done 1 — 12 §3.2-B)

12 §4.1 "Install Manifest 직렬화 — 프로젝트 내 매니페스트 파일 (Markdown + front-matter 또는 설정 파일)"의 물리 실현을 확정한다. 계약(12 §3.2-B 6필드·INV-7)은 재정의하지 않고 § 포인터로 인용하며, 물리 표기만 확정한다.

- **직렬화 형식.** Install Manifest는 **Markdown 본문 + front-matter** 문서로 직렬화한다(12 §4.1 두 선택지 중 첫째). 물리 원본 = 템플릿 `scaffold-template/install-manifest.template.md`(§6). 설치 시 front-matter의 값이 채워져 대상 프로젝트의 매니페스트 파일로 배치된다.
- **6필드 물리 표기 (12 §3.2-B).**

| 필드 (12 §3.2-B) | 필수 | 물리 표기 (front-matter) | 값·근거 |
|---|---|---|---|
| `frameworkVersion` | 예 (INV-7) | 문자열 | `"v1.0"` — 현 릴리스 Framework 버전(ROADMAP v1.0). |
| `specVersion` | 예 (INV-7) | 문자열 | `"v0.1"` — 설치 기준 spec 기준선 버전(Frozen v0.1). |
| `installedModules` | 예 | 문자열 목록 | `moduleSelection` 해소 결과. 최소 필수 집합(runtime·agent·verifier 등 — 13 §3.2-A + Bootstrap 필수 계약) 포함, 선택 Module은 선택에 따라 추가. |
| `installedArtifacts` | 예 | 경로 목록 | Scaffold가 생성·소유한 산출물(배치된 `.claude/*`·`framework/*`·`specs/*`·매니페스트 자신). 제거·멱등성 판정 기준(INV-4·INV-5). |
| `preservedPaths` | 예 | 경로 목록 | 설치 시 보존된 기존 사용자 파일(INV-3). 빈 프로젝트면 빈 목록. |
| `timestamp` | 아니오 | 문자열 | 설치 시점(선택). |

- **버전 정합(INV-7).** `frameworkVersion`·`specVersion` 표기는 필수다(12 INV-7, CK-7). 두 값의 구체 문자열(`"v1.0"`·`"v0.1"`)은 이 릴리스의 값이며, 형식(버전 문자열 표기)은 이식 교체 지점(§7-6)이다.
- 계약(6필드 의미·필수 여부·INV-7)의 정본은 12 §3.2-B이며, 본 절은 직렬화 형식과 이 릴리스의 값만 확정한다(재정의 0).

---

## §5. CK-1~CK-8 물리 검사 방법 — 검사 도구 바인딩 (done 1)

12 §3.2-C 설치 검증 체크리스트 CK-1~CK-8 각각을 이 환경의 검사 도구에 바인딩한다(verifier-binding.md §5 VT-1~VT-5 검사 도구 바인딩 관례 참조 — 존재 확인·정독 대조 = 파일 조회, 전수 스캔 = 텍스트 검색, 시연 = 명령 실행 + 파일 조회). **이 문서는 Adapter 경계이므로 구체 도구 토큰의 사용이 허용된다(§0 격리 지점).** CK 항목의 판정 기준 정본은 12 §3.2-C이며, 본 절은 물리 검사 방법(어떤 도구로 각 항목을 실현하는가)만 확정한다.

| 항목 (12 §3.2-C) | 판정 대상 (정본 요지) | 물리 검사 방법 (검사 도구 바인딩) | 대응 VT (06 §3.2-E) |
|---|---|---|---|
| **CK-1** | Project Template 모든 필수 구성 요소 존재 | **파일 조회 도구**로 §6 필수 6요소(규약 문서·Agent 4종·Config·specs 자리·Core/Adapter 경계·Install Manifest)의 설치 대상 경로 실재를 실측. | VT-1 산출물 존재 |
| **CK-2** | `moduleSelection`이 Bootstrap 필수 계약 최소 집합 포함 (01 §3.1-C) | **파일 조회 도구**로 Manifest `installedModules`와 최소 구성 집합(13 §3.2-A 5요소)·Bootstrap 필수 계약을 항목별 대조. | VT-2/VT-3 |
| **CK-3** | Config Global·Project 스코프 초기화 + 01 §3.2-B 스키마 일치 | **파일 조회 도구**로 Project scope 소스(`.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.json`)·Global 기본값 제공을 01 §3.2-B 스키마(스코프·우선순위)와 셀 단위 대조. | VT-3 규격 준수 |
| **CK-4** | 설치 직후 Bootstrap `Ready`/`Degraded` 성공 (01 §3.1-C) | **명령 실행 도구**로 세션/턴 Bootstrap을 재현(runtime-binding.md §3.4) + **파일 조회 도구**로 `state` 결과 관측(필수 계약 해소 → Ready, 선택 일부 누락 → Degraded). | VT-5 시연 |
| **CK-5** | Bootstrap 이후 Loop 최소 1 사이클 구동 (03 소관) | **명령 실행 도구**로 핵심 루프(위임 → 구현 → 검증 → 승인) 1 사이클을 재현(loop-binding.md §2) + 통과 결과 관측. 구동 계약은 03 소관 — 결과만 판정. | VT-5 시연 |
| **CK-6** | 설치된 Core 디렉터리 AI 의존 요소 0건 (01 INV-4) | **텍스트 검색 도구**로 `framework/core/`·`framework/runtime/` 전 범위에 금지 요소 후보 집합(특정 AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명) **전수 스캔**. 단일 대리 지표 하나로 대체하지 않는다(06 V4·INV-4). 매치는 금지 토큰/정당 참조(컴포넌트·문서명)로 분류. | VT-4 경계 |
| **CK-7** | Install Manifest 존재 + `frameworkVersion`·`specVersion` 표기 (INV-7) | **파일 조회 도구**로 매니페스트 파일 실재 + front-matter의 두 버전 필드 표기(§4)를 실측. | VT-1 + VT-3 |
| **CK-8** | 기존 사용자 파일 보존 — `preservedPaths`와 실제 상태 일치 (INV-3) | **파일 조회 도구**로 Manifest `preservedPaths`의 각 경로가 실제로 보존(무변경)되었는지 대조 + 재설치 전후 구조 diff 0(멱등성). | VT-2/VT-5 |

- **금지 요소 후보 토큰의 운용 목록(CK-6).** CK-6 전수 스캔이 대상으로 삼는 금지 요소 후보 토큰(특정 AI 이름·모델명·제품 기능명·`claude-*` 패턴 등)의 운용 목록은 이 프로젝트 표면에서 verifier-binding.md §5·docs/verification-checklist.md §7이 소유한다(운용 지침). 본 문서는 CK ↔ 검사 도구의 물리 바인딩만 확정하고, 운용 목록을 복제하지 않는다.
- **본 산출물의 CK-6 자체 전수 스캔.** 본 Task는 scaffold-template/의 Core부(`scaffold-template/framework/core/`·`scaffold-template/framework/runtime/`)를 위 CK-6 방법으로 자체 전수 스캔했고, 금지 요소 후보 집합 전 범위에서 **instance 토큰 0건**을 확인했다(§6·§8). 카테고리 명(예: "AI 이름")과 컴포넌트·문서 파일명(예: `config-schema.md`)은 금지 토큰이 아니다(structure.md §2 주·§5).
- **경계.** 검사 도구는 이식 교체 지점(§7 — 대상 환경 검사 도구로 교체)이며, CK-1~CK-8 항목·판정 기준(12 §3.2-C)은 유지된다. 무인 검증 실행기(형태 B)는 도구 배선의 형태 B 사안이며, 본 문서는 도구 표면 바인딩만 확정한다.

---

## §6. scaffold-template/ 구조·내용 목록 정본 (done 2)

12 §3.2-A Project Template의 물리 자산 정본이다. 위치 = `framework/adapters/claude/scaffold-template/`. **구조·내용 목록·`dot-claude/`→`.claude/` 이름 변경 매핑의 정본은 이 절**이다(§0). 아래 트리·표는 파일 시스템 직접 실측(§8)에 근거한다.

물리 템플릿 디렉터리 구조(본 문서 정본 — 데이터 실재, §8 실측):

```
framework/adapters/claude/scaffold-template/
├─ README.md                       # 템플릿 개요·설치 대상 매핑 (§6 정본의 사용자 안내)
├─ install-manifest.template.md    # Install Manifest 템플릿 (Markdown + front-matter, 6필드 — §4)
├─ dot-claude/                     # → 설치 시 대상 프로젝트의 .claude/ 로 배치 (이름 변경)
│  ├─ AGENT.md                     #   규약 문서 초기본 (Governance)
│  ├─ CLAUDE.md                    #   Advisor 진입점 + Config Project scope 초기값·안내
│  ├─ settings.json.example        #   Config Project scope 초기값 (선택) → .claude/settings.json
│  └─ agents/
│     ├─ advisor.md                #   Advisor 정의 초기본 (실행 모델 미지정 = 세션 상속)
│     ├─ planner.md                #   Planner 정의 초기본 (model: opus)
│     ├─ worker.md                 #   Worker 정의 초기본 (model: opus)
│     └─ verifier.md               #   Verifier 정의 초기본 (model: opus)
├─ framework/
│  ├─ core/README.md               # Core 경계 자리 (AI 비의존 — CK-6 대상)
│  ├─ runtime/README.md            # Runtime 경계 자리 (AI 비의존 — CK-6 대상)
│  └─ adapters/README.md           # Adapter 경계 자리 (격리 지점)
└─ specs/README.md                 # spec 기준선 배치 자리·안내 (v0.1 Frozen 15건)
```

### §6.1 12 §3.2-A 필수 6요소 대응

| 12 §3.2-A 필수 요소 | 템플릿 자산 | 설치 대상 경로 | 근거 |
|---|---|---|---|
| 규약 문서 (Convention docs) | `dot-claude/AGENT.md`·`dot-claude/CLAUDE.md` | `.claude/AGENT.md`·`.claude/CLAUDE.md` | 12 §3.2-A(AGENT.md·진입 규약), 02 §4.1 |
| Agent 정의 (4종) | `dot-claude/agents/{advisor,planner,worker,verifier}.md` | `.claude/agents/*.md` | 12 §3.2-A, 02 §4.1 |
| Config — Global scope 초기화 | (문서 기본값 제공 — 물리 소스는 사용자 환경 소관) | 사용자 전역 설정 (미배치) | 12 §3.2-A, 01 §3.2-B |
| Config — Project scope 초기화 | `dot-claude/CLAUDE.md`·`dot-claude/AGENT.md`·`dot-claude/settings.json.example` | `.claude/*`·`.claude/settings.json` | 12 §3.2-A, 01 §3.2-B |
| specs 디렉터리 | `specs/README.md`(자리·배치 안내) | `specs/`(+ 기준선 배치) | 12 §3.2-A |
| Core / Adapter 경계 | `framework/{core,runtime,adapters}/README.md`(자리) | `framework/core/`·`framework/runtime/`·`framework/adapters/` | 12 §3.2-A, 01 §3.2-E |
| Install Manifest (§3.2-B) | `install-manifest.template.md` | 프로젝트 내 매니페스트 파일 | 12 §3.2-B, §4 |

### §6.2 정직 구분·규칙

- **`dot-claude/` → `.claude/` 이름 변경.** 템플릿의 `dot-claude/`는 설치 시 대상 프로젝트의 `.claude/`로 배치된다. 템플릿 자산이 라이브 설정 표면(현행 프로젝트의 `.claude/`)으로 오인·중복 로드되지 않도록 `dot-claude/` 이름을 쓴다(스캐폴드 관례). 이 매핑의 정본은 이 절이다.
- **Module scope Config는 초기화 대상 아님.** 각 Module이 소유한다(12 §3.2-A 주). 템플릿은 Module scope Config를 배치하지 않는다.
- **Global scope은 사용자 환경 소관.** Global scope(Framework 전역 기본값)의 물리 소스는 사용자·환경 전역 설정이며 Scaffold가 초기화·덮어쓰지 않는다(§2 행 3). 템플릿은 Global 기본값을 문서 기본값으로만 제공한다.
- **Core부 AI 비의존(CK-6 자체 전수 스캔).** 템플릿의 Core부(`framework/core/README.md`·`framework/runtime/README.md`)는 AI 의존 토큰 0건으로 작성되었다. 본 Task가 CK-6 방법(텍스트 검색 전수 스캔, §5)으로 금지 요소 후보 집합 전 범위를 자체 스캔한 결과 **instance 토큰 0건**이다(§8 실측 — 카테고리 명·컴포넌트/문서 파일명은 금지 토큰이 아니다). 이는 설치된 Core 디렉터리가 CK-6을 통과하도록 의도된 것이며, 템플릿이 물리적으로 Adapter 경계 이하(격리 지점, C-3 허용)에 있음과 무관하다. `framework/adapters/README.md`(Adapter 경계 자리)는 격리 지점이므로 CK-6 대상이 아니다.
- **초기본의 성격.** 4역할 정의·규약 문서는 **초기본(starter)**이며, 계약 정본(02 §4.1·Glossary §3.2-E)을 재정의하지 않고 참조·바인딩한다. 실행 모델 지정은 현행 실물 관행(worker·planner·verifier `model: opus`, advisor 세션 상속)을 따르되 그 의미 정본이 02 §4.1임을 각 파일이 주석한다. 대상 프로젝트는 이를 시작점으로 삼아 자기 프로젝트 규약을 얹는다.

---

## §7. 12 §4.2 이식 교체 지점 1~7 대응 (done 1)

12 §4.2 이식 교체 지점 1~7 각각에 "이 환경 바인딩 = 교체되는 것"과 "유지되는 것(정본 § 불변)"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인한다.

| # (12 §4.2) | 교체 지점 | 이 환경(claude) 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|
| 1 | 규약 문서 위치·포맷 | `dot-claude/AGENT.md`·`dot-claude/CLAUDE.md` → 대상 `.claude/*.md`(§2 행 1·§6). | §3.1 연산·§3.2-A Project Template 추상 구성(규약 문서 요소). 02 SP-2. |
| 2 | Agent 정의 위치·포맷 | `dot-claude/agents/*.md`(실행 모델 지정 포함) → 대상 `.claude/agents/*.md`(§2 행 2). | §3.2-A Project Template(Agent 정의 4종 요소). 02 SP-1. |
| 3 | Config 소스·위치 | 전역·프로젝트 설정 물리 소스(`~/.claude/…`·`.claude/…`·`dot-claude/settings.json.example`)(§2 행 3·4). | §3.2-A Config 2스코프 초기화·01 §3.2-B 스코프·우선순위·결정성. 01 §4.2-2. |
| 4 | Core / Adapter 디렉터리 규약 | `framework/`·`.claude/` 경계 배치(§2 행 6·§6). | §3.2-A Core/Adapter 경계 요소·01 §3.2-E 물리 분리 규칙. 01 §4.2-5. |
| 5 | Install Manifest 직렬화 포맷 | Markdown + front-matter 매니페스트 파일 형태(§4). | §3.2-B Install Manifest 6필드·INV-7 버전 정합. |
| 6 | 버전 값 표기 형식 | 버전 문자열 형식(`"v1.0"`·`"v0.1"`)(§4). | §3.2-B `frameworkVersion`·`specVersion` 필드·INV-7. |
| 7 | Bootstrap·Loop 구동 호출 방식 | 세션/턴 Bootstrap·서브에이전트 핵심 루프 구동(§2 행 9·10). | §3.1 완료 조건(Bootstrap Ready/Degraded)·CK-4·CK-5. 01 §4.2-4, 03 소관. |

- "유지되는 것" 열의 계약(§3.1 3연산·§3.2-A Project Template 추상 구성·§3.2-B Install Manifest 필드·§3.2-C 설치 검증 체크리스트·§3.3 Invariants)은 다른 AI·환경으로 이식해도 바뀌지 않는다 — 12 §4.2 말미 "유지되는 것" 목록의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(12 §4.2 말미). 본 문서는 그 정식화를 선취하지 않고 v0.9 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §8. 상태 서술 실측 대조 (L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록 — A5 재작업 사례: 미존재를 "실재"로 서술한 것을 파일 시스템 전수 대조로 검출한 데서 도출)에 따라, 본 문서의 "실재/존재/부재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`/`find`) + 텍스트 검색(전수 스캔) 직접 실측.**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 자매 바인딩 8문서 + adapter-conformance.md | 실재 | 실재 — runtime·memory·verifier·loop·workflow·hooks·skills·plugins-binding.md 8파일 + adapter-conformance.md 확인. |
| `framework/adapters/claude/scaffold-binding.md` (본 문서) | 실재 (본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음(사전 실측 확인). |
| `framework/adapters/claude/scaffold-template/` (프로젝트 템플릿) | 실재 (본 산출로 생성 — 13파일) | 실재 — 13파일 확인: README.md·install-manifest.template.md·dot-claude/{AGENT.md·CLAUDE.md·settings.json.example·agents/4종}·framework/{core,runtime,adapters}/README.md·specs/README.md. |
| scaffold-template/ Core부 AI 의존 토큰 (CK-6 자체 전수 스캔) | 0건 (instance 토큰) | 0건 — `scaffold-template/framework/{core,runtime}/`에 대해 금지 요소 후보 집합 전수 스캔, instance 토큰 0. (카테고리 명·문서 파일명 매치는 금지 토큰 아님.) |
| `.claude/agents/` 4종 (템플릿 원형) | 실재 (advisor·planner·worker·verifier.md) | 실재 — 4파일 확인. 본 문서는 참조만·무수정. |
| `.claude/AGENT.md`·`.claude/CLAUDE.md` (템플릿 원형) | 실재 | 실재 — 2파일 확인. 무수정. |
| worker·planner·verifier.md `model: opus` / advisor.md 세션 상속 (원형·초기본) | 실재 (역할별 모델 지정 관행) | 실재 — 라이브 원형 3파일 `model: opus`·advisor.md model 라인 부재 확인; 템플릿 초기본 4파일 동일 관행 반영. |
| `framework/core/`·`framework/runtime/` (라이브 Core 경계) | 실재 (계약 문서만·AI 비의존) | 실재 — core/(structure.md·config-schema.md)·runtime/(module-manifest·module-registry·lifecycle) 확인. 무수정. |
| `docs/v0.9-install-guide.md` (본 산출로 생성 — 아카이브) | 아카이브 (산출물 수명 정책으로 제거) | `uahf/docs/v0.9-install-guide.md@cd9247b` — 본 Task 생성(설치 가이드), 산출물 수명 정책(docs/artifact-lifecycle-policy.md §7)으로 작업 트리에서 제거(열람: `git show cd9247b:uahf/docs/v0.9-install-guide.md`). |
| `framework/scaffold/` (DP-A3) | **부재** (미신설 결정) | **부재** — `framework/` 하위 = adapters·core·loop·memory·plugins·runtime·verifier·workflow 8경계, `scaffold/` 없음 확인. |
| `.claude/settings.json` (Config Project scope 지원 소스) | **미존재** (라이브 — settings.local.json만) | **미존재** — `.claude/settings.local.json`만 실재. `.claude/settings.json` 부재 확인(템플릿은 `settings.json.example`로 제공). |
| specs/ Frozen 계수 | **15** (numbered 00~13 = 14 + TEMPLATE 1) | 실측 — 00~13 numbered 14파일 + TEMPLATE.md = **15**. |

- **핵심 구분.** 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로, 미래 산출물(설치 시 대상 프로젝트에 배치되는 파일)을 현재 실재로 쓰지 않았다(A5/L-07 재발 방지). 본 산출은 scaffold-binding.md·scaffold-template/(13파일)·docs/v0.9-install-guide.md 3산출물만 생성하며, 라이브 표면(.claude/·framework/core/·framework/runtime/ 실물)·자매 바인딩 문서·specs/·기존 docs/를 수정·생성하지 않았다(07 R4).

---

## §10. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 12 §3·§4의 물리 실현이다. 어떤 연산·데이터 계약·체크리스트 항목·불변 규칙·사유 코드도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 12 §3이다. 12 §4.1 표를 넘어서는 새 바인딩 계약, 12 §3.2-C를 넘어서는 새 CK 항목, 12 §3.2-D를 넘어서는 새 사유 코드를 창설하지 않았다.
- **프로젝트 템플릿 정본 소유(done 2).** scaffold-template/의 구조·내용 목록·`dot-claude/`→`.claude/` 매핑·Core부 AI 비의존은 본 문서(§6)가 정본으로 소유한다. 12 §3.2-A Project Template의 추상 구성(필수 6요소)은 12가 소유하며, 본 문서는 그 물리 자산만 확정한다(계약 표면 재정의 0).
- **격리 토큰의 단일 자리.** 구체 직렬화 형식(Markdown·front-matter)·물리 경로(`.claude/…`·`framework/adapters/claude/…`·`~/.claude/…`·`specs/…`·`docs/…`)·세션/턴·서브에이전트 등 환경 토큰은 이 Adapter 경계 문서와 scaffold-template/(격리 지점) 안에만 둔다. 12 §3(Frozen)은 이 토큰을 본문에 두지 않으며, 본 문서는 그 격리의 반대편(허용 지점)이다 — 단 12 §3 문면 재정의 권한은 아니다(§0).
- **Advisor 결정 기록(Worker는 기록만).** DP-U1(설치 절차 = 형태 A 문서 절차, 본 위임에서 지시)·DP-A3(`framework/scaffold/` 미신설, adapter-conformance.md §5)의 주체는 Advisor이며, 본 문서는 그 결정을 준수·기록만 한다(Worker는 Architecture·설계 결정을 하지 않는다 — 02 §3.2-A·INV-3). 두 결정은 Frozen 12·01을 무변경으로 유지한다.
- **동시 작성 문서 경계(07 R2).** 같은 병렬 집합(PS2)에서 동시 작성 중인 형제 Task 산출물(agent-binding.md·harness-binding.md·`.claude/commands/`·getting-started·Glossary 개정분·hooks-binding.md/plugins-binding.md §7 개정분)을 인용·추측하지 않았다(07 R2). 참조한 확정 정본은 Frozen specs(12·13·01·00)·adapter-conformance.md(T1 확정본)·Baseline 자매 바인딩(runtime·memory·verifier·loop-binding.md 관례)·structure.md·ROADMAP.md·라이브 원형 실물(.claude/ 4역할+규약 2문서)뿐이다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 3산출물(scaffold-binding.md·scaffold-template/·docs/v0.9-install-guide.md)만 생성하며, framework/core·framework/runtime·specs/·기존 docs/·.claude/ 라이브 실물·자매 바인딩 문서를 수정·생성하지 않는다.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-SB-1 (Presentation 진입 표면 정합 — 비차단).** 12 §4.1 행 없음 — Scaffold의 사용자 대면 호출 표면(Presentation Layer, Glossary §3.2-D)의 명령 진입점 물리 실현은 형제 Task(`.claude/commands/`, PS2)가 소유한다. 본 문서는 그 표면을 인용·선취하지 않았고(07 R2), 설치 절차의 물리 실현만 확정했다. 설치 가이드(docs/v0.9-install-guide.md)와 명령 진입 표면의 상호 참조 정합은 Advisor 통합 판단 대상이다 — 비차단.
- **OQ-SB-2 (형태 B 설치 실행기 경계 — 비차단).** Install/VerifyInstall/Uninstall의 실행 코드(형태 B)가 어느 경계(설치 도구 실행기)에 배치되는지는 형태 B 설계 시 확정 대상이다(§3, DP-U1은 현재 형태 A 규정). Bootstrap에서는 문서 절차로 실현되므로 이 배치가 필요하지 않으며, 계약(12 §3.1) 변경이 아니므로 비차단이다.
- **OQ-SB-3 (기준선 버전 표기 동기화 — 비차단) — 해소됨 (v1.0 T3).** `frameworkVersion`=`"v0.9"`는 현 릴리스 값이다. v1.0 이후 릴리스에서 이 값은 상승하며, 템플릿 `install-manifest.template.md`·본 문서 §4의 값 동기화는 후속 릴리스 격리 갱신 대상이다(자매 바인딩의 버전별 격리 갱신 관례 동형). `specVersion`=`"v0.1"`은 spec 기준선(Frozen)으로 고정이다 — 비차단. **해소 (v1.0 T3, Advisor 결정 DP-V10):** v1.0 릴리스에 맞춰 본 개정이 위 예고대로 `frameworkVersion` 값 서술 전 지점(§1 목적·§2 표 행8·§4 필드 표·§4 버전 정합 주·§7 이식 교체 지점 표 행6·§11 요약 = 6지점 + 템플릿 `install-manifest.template.md` front-matter 1지점)을 `"v1.0"`으로 동기화하고, `specVersion`=`"v0.1"`은 무변경으로 유지했다(§9 이력 행). 위 서술의 "v0.9"·"현 릴리스"는 OQ 제기 시점(v0.9) 기준 기록으로 보존한다(기존 문면 불변).

---

## §11. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 Scaffold 물리 실현 산출물(선행 자매 바인딩 8문서 + adapter-conformance.md에 이음). Frozen specs/12 Scaffold 계약(§3·§4.1)의 **Claude 물리 실현 매핑 + 프로젝트 템플릿(scaffold-template/) 정본**. 정본 = 12 §3·§4(본 문서는 인스턴스 매핑, 재정의 아님 — §0). adapter-conformance.md §4 배정표 T4 이행·DP-A3 준수·DP-U1 기록.
- **§2:** 12 §4.1 표 **10행 전건**을 물리 실현으로 매핑("물리 실현" + "실재 여부" 열, 형태 A/B 정직 구분, DP-U1). 규약 문서·Agent 4종·Config·specs·Core/Adapter 경계·Install Manifest·버전 값·Bootstrap 호출·Loop 1사이클 구동.
- **§3:** Install/VerifyInstall/Uninstall 3연산 물리 절차를 12 §3.1과 **1:1 단계 대응**(memory-binding.md §3 관례) — reason 코드 대응·멱등성(INV-4)·제거 안전(INV-5) 물리 보장. 형태 A 문서 절차(DP-U1).
- **§4:** Install Manifest 직렬화 — Markdown + front-matter, 6필드 물리 표기, `frameworkVersion`=`"v1.0"`·`specVersion`=`"v0.1"`(INV-7).
- **§5:** CK-1~CK-8 물리 검사 방법(검사 도구 바인딩 — 존재 확인/정독 = 파일 조회, 전수 스캔 = 텍스트 검색, 시연 = 명령 실행; verifier-binding.md §5 VT 관례). CK-6 자체 전수 스캔 결과 포함(instance 토큰 0).
- **§6:** scaffold-template/ 구조·내용 목록 정본(13파일 트리·12 §3.2-A 필수 6요소 대응·`dot-claude/`→`.claude/` 매핑·Global scope 사용자 환경 소관·Module scope 미초기화·Core부 AI 비의존 CK-6 clean).
- **§7:** 12 §4.2 이식 교체 지점 1~7 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 이식 불변(C-1) 재확인.
- **§8:** 상태 서술 실측 대조(2026-07-06 직접 실측) — 자매 8문서+adapter-conformance·scaffold-template/ 13파일·Core부 CK-6 0건·라이브 원형 실물 실재; `framework/scaffold/`·`.claude/settings.json` 부재; specs 15. 실측 불일치 0건(A5/L-07 재발 방지).
- 12 §3 계약 재정의·확장 0 · 새 바인딩·새 CK·새 사유 코드 창설 0 · Frozen specs 계수 15 · Glossary 밖 새 용어 0. 구체 AI·환경·형식 토큰은 이 Adapter 경계·scaffold-template/(격리 지점)에서 허용된다. 형제 Task(PS2) 불인용(07 R2). 라이브 표면 무수정 — 3산출물만 생성(07 R4).
