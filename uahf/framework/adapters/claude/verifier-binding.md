# framework/adapters/claude/verifier-binding — Claude Code Verifier Adapter 바인딩

작성일: 2026-07-06
상태: v0.5 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/06-verifier.md §4.1 — Claude Code Binding 표(7행). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/06-verifier.md §4.2 — 이식 교체 지점 SP-1~SP-6. 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/06-verifier.md §3.1·§3.2·§3.3 — Verify 연산·검증 리포트/판정 값/재작업 지시/검증 유형/검출 계약·불변 규칙(INV-1~INV-10). 본 문서가 준수·대조하는 계약. 재정의하지 않고 § 포인터로만 인용한다.
- framework/verifier/verification-report.md (V1 확정본) — 검증 리포트 스키마 인스턴스(6필드·5필드·도출 규칙). 검증 리포트 직렬화 대상의 확정 인터페이스(§4). 정본은 06 §3.2-A/B/C.
- framework/verifier/module-manifest.md (V2 확정본) — Verifier Provider Module Manifest 인스턴스. `entrypoint` 추상 참조의 물리 해소 위임 지점(§4, 물리 해소가 본 문서 소관), `configSchema` 생략(DP-V2 — 물리 반영 대상 없음, §3.2).
- framework/verifier/verifier-protocol.md (V3 확정본) — Verify 연산 프로토콜 5단계 인스턴스. 형태 A 규약 실현의 절차 준수 대상(§3.1). 정본은 06 §3.1.
- framework/verifier/rework-instruction.md (V4 확정본) — 재작업 지시 4필드 포맷 인스턴스. 리포트 `rework` 절 직렬화 대상(§4.2). 정본은 06 §3.2-D.
- framework/verifier/criteria-catalog.md (V5 확정본) — 완료 판정 기준 카탈로그(VT-1~VT-5·대조 기준 4부류). 검사 도구 바인딩 소관 포인터(criteria-catalog.md §5 — 본 문서 §5가 그 물리 실현 정본). 정본은 06 §3.2-E.
- .claude/agents/verifier.md — Verifier 역할 Claude Code 바인딩 진입점(실물). 실행 모델 미지정(세션 상속) 명시. 본 문서는 참조만 하고 수정하지 않는다(06 §4.1 진입점 행·§4.2 SP-1·SP-6).
- framework/adapters/claude/runtime-binding.md · memory-binding.md — 자매 Adapter Binding 문서(관례 정본). 격리 방향 반전(§0)·형태 A/B 구분·실측 기반 상태 서술·교체 지점 표("교체되는 것/유지되는 것" 열)·entrypoint 물리 해소 관례·Register/Resolve 수행 방식의 선행 관례.
- docs/verification-checklist.md §7 — Advisor 검증 게이트 운용 바인딩(환경 의존 검사 도구 사용법). 본 문서 §5(검사 도구 바인딩 물리 실현 정본)와 정합하는 운용 지침. 재정의 0.
- `uahf/docs/v0.3-verification-report.md@cd9247b` · `uahf/docs/v0.4-verification-report.md@cd9247b` — 검증 리포트의 물리 직렬화·저장 실증 인스턴스 2건(각 CP2 독립 판정 산출물, Baseline 확정; 산출물 수명 정책으로 작업 트리에서 제거·아카이브). `docs/v0.X-verification-report.md` 명명 관례·6필드 절 구조·rework 절 직렬화·검사 도구 실사용의 실증 근거(§4·§5·§7).
- framework/core/structure.md §2·§5·§6 — 4경계 배치, C-3 금지 토큰 규칙(Adapter 경계는 격리 보유로 비적용), v0.3 산출물 표. 본 문서 경계의 근거.
- specs/01-runtime.md §4·§3.2-A·§3.2-B — Adapter Binding(Provider 등록·물리 진입점 해소)·Module Manifest 필드·Config 병합 규칙. § 포인터로만 참조.
- specs/00-glossary.md — 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- ROADMAP.md v0.5 (Verifier) — 산출물 "검증 리포트 스키마 / 재작업 지시 포맷 / 완료 판정 기준 카탈로그"의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 06 §3.3 INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로·검사 도구 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·memory-binding.md §0과 동형). 단 이 문서는 Core Contract(06 §3)와 그 인스턴스 문서(framework/verifier/ 5문서)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.5 Draft | 최초 작성. `framework/adapters/claude/` 경계의 세 번째 산출물(선행: runtime-binding.md·memory-binding.md). 06 §4.1 바인딩 표 **7행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정) 정직 구분(§2). V2 Manifest `entrypoint` 추상 참조의 물리 해소(형태 A = `.claude/agents/verifier.md` 진입점 + verifier-protocol.md 절차 준수 / 형태 B = 실행 코드 로케이터 defer) + `configSchema` 생략(DP-V2)으로 물리 반영 대상 부재 명시(Memory `recall.limit.max` 대응 절과의 차이 정직 기록, §3). 검증 리포트 직렬화·저장 위치 확정(docs/ 구조화 문서, `docs/v0.X-verification-report.md` 명명 관례 — v0.3·v0.4 2건 실증·실측) + 재작업 지시 rework 절 직렬화·재위임 전달(§4). VT-1~VT-5 검사 도구 바인딩(파일 조회·텍스트 검색·명령 실행) + verification-checklist.md §7 정본 소유 관계(§5). 06 §4.2 이식 교체 지점 SP-1~SP-6 대응 표("교체되는 것/유지되는 것" 열 — C-1 이식 불변 재확인, §6). 상태 서술 실측 대조 표(§7 — 실재 서술 전건 파일 시스템 실측 후 기입, L-07). 06 §3·framework/verifier/ 5문서 계약 재정의·창설 0, 새 바인딩 계약 0, Glossary 밖 새 용어 0. 동시 작성 시연 절차서(docs/v0.5-demo-procedure.md, V7) 내용 불인용(07 R2), 미래 산출물 실재 불주장(L-07). 이 1파일만 생성 — `.claude/agents/verifier.md`·framework/verifier/ 5문서·기존 Baseline 산출물·specs/ 무수정. | Worker (Advisor 위임, Task V6) |
| 2026-07-06 | v0.5 Baseline | v0.5 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 26/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지)·삭제 산출물(docs/v0.3·v0.4-verification-report.md 실사용 인스턴스 2건) 참조 @cd9247b 앵커 전환(§4·§7 실측 표 아카이브 표기). `docs/v0.X-verification-report.md` 명명 관례·계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/06-verifier.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)와 framework/verifier/ 5문서(verification-report.md·module-manifest.md·verifier-protocol.md·rework-instruction.md·criteria-catalog.md)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·필드·검증 유형·판정 값)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. framework/verifier/ 5문서가 "물리 직렬화·저장 위치·검사 도구·물리 진입점 해소는 Adapter Binding 문서 소관"이라며 미룬 **직렬화 형식·명명 관례·저장 위치·물리 진입점 해소·검사 도구 배선**이 실재하는(확정되는) 유일한 자리다(06 §4, verification-report.md §5, module-manifest.md §4, criteria-catalog.md §5, rework-instruction.md §5, verifier-protocol.md §0).
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리(`framework/verifier/` 등) 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 06 §3.3 INV-8). 이 문서는 그 **반대편**이다 — 구체 토큰(진입점 정의 파일 경로 `.claude/agents/…`, 직렬화 형식명 Markdown, 물리 경로 `docs/…`·`framework/adapters/claude/…`, 검사 도구명, 서브에이전트·세션 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(runtime-binding.md §0·memory-binding.md §0과 동형).
- **검증 리포트 직렬화·저장 위치 정본 선언(done 4).** 검증 리포트의 물리 직렬화 형식(구조화 Markdown 문서)·명명 관례(`docs/v0.X-verification-report.md`)·저장 위치(`docs/`)의 **물리 실현 정본은 이 문서(§4)다**. 검증 리포트는 은닉 백엔드(예: Memory Store)가 아니라 구체 토큰 인용이 허용되는 **구조화 검증 산출물 문서**이며(두 실사용 리포트 §0 거버넌스 동형), 06 §4.1 검증 리포트 직렬화 행이 "검증 산출물 위치"로 Adapter Binding 문서에 미룬 지점을 본 문서가 확정한다. 이 위치는 이미 **2건의 확정 실사용 인스턴스**(`uahf/docs/v0.3-verification-report.md@cd9247b`·`uahf/docs/v0.4-verification-report.md@cd9247b`, §7 실측 — 아카이브)로 실증되었다.
- **창설 금지.** 이 문서는 06 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.5 산출물(검증 리포트 스키마·재작업 지시 포맷·완료 판정 기준 카탈로그)의 물리 실현 매핑으로 한정한다. 새 검증 유형·판정 값·재작업 지시 필드·불변 규칙·검사 도구 계약을 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, runtime-binding.md §0, delegation-protocol.md §0). Verifier는 정식 실행 Module이 아니라 규약 문서(06·framework/verifier/ 5문서)와 관행(Advisor가 산출물을 정독해 판정을 구동, verification-checklist.md §2 게이트 C)으로 실현된다(형태 A). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(진입점 정의 파일·구현 디렉터리 5문서·확정 실사용 리포트 2건 — §7 실측)과, **실행 코드 도입 시 로딩될 지점**(형태 B — Verify 연산 실행 진입점·로더)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(done 1·7, L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(Active Lesson L-07 — 상태 서술은 실측 후 기록, A5 재발 방지). §2 "실재 여부" 열과 §7 실측 대조 표의 전 행은 파일 시스템 직접 실측에 근거한다 — 미존재를 실재로, 미래 산출물을 현재 실재로 쓰지 않는다.
- 용어는 specs/00-glossary.md 정본만 사용한다. 검증 리포트·검증 유형·재작업 지시·거짓 완료 보고는 Glossary §3.2-J 정본이며(06 §9 승격 4건), Verifier·검증·판정은 Glossary 기존 용어다. 본 문서는 새 용어를 신설하지 않는다. `형태 A/B`는 structure.md 서술 라벨의 인용이며 Glossary 표제어가 아니다.

---

## §1. 목적

이 문서는 06 §4.1(Verifier Claude Code Binding)을 이 환경 위에 **v0.5 시점의 구체 물리 실현**으로 매핑한다.

책임은 다섯 가지다.

- 06 §4.1 바인딩 표의 **7행 전부**를 물리 표면(진입점 정의 파일·구현 디렉터리·직렬화 형식·회수 채널·검사 도구·재작업 전달·실행 모델)으로 확정하고, Bootstrap 상태에서의 실재/규약 실현/형태 B 예정을 "실재 여부" 열로 정직하게 구분한다(§2, done 1·7).
- V2 Manifest `entrypoint` 추상 참조의 **물리 해소 지점**(형태 A 규약 실현 / 형태 B 실행 코드 로케이터)과, `configSchema` 생략(DP-V2)으로 인한 **물리 반영 대상 부재**를 명시한다(§3, runtime-binding.md·memory-binding.md 교체 지점 관례 동형, done 3).
- 검증 리포트의 **직렬화 형식·명명 관례·저장 위치**를 확정하고(docs/ 구조화 문서, `docs/v0.X-verification-report.md`), 재작업 지시의 리포트 `rework` 절 직렬화·재위임 전달 표면을 바인딩한다(§4, done 4).
- VT-1~VT-5 각각의 **검사 도구 바인딩**(파일 조회·텍스트 검색·명령 실행)을 확정하고, verification-checklist.md §7 운용 지침과의 **정본 소유 관계**를 명시한다(§5, done 5).
- 06 §4.2 이식 교체 지점 SP-1~SP-6 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§6, done 2). 그리고 상태 서술을 실측과 대조한다(§7, done 7).

이 문서는 06 §3·framework/verifier/ 5문서의 어떤 계약 요소도 재정의·확장하지 않는다(§0, done 6). 형태 A → 형태 B 전환 시에도 Core Contract(06 §3) 변경은 0이며(structure.md §7 C-1), 이 문서(§6의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 06 §4.1 바인딩 표 7행 물리 실현 (done 1·7)

06 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. 아래 표의 "06 §4.1 바인딩" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·형식·채널·절차를, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현/형태 B 예정을 정직하게 구분한다(§7 실측 대조). "실재" 서술은 전건 파일 시스템 실측 후 기입했다(L-07).

| # | §3 계약 요소 | 06 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Verifier Module 진입점 | `.claude/agents/verifier.md` — Runtime generic Module 계약의 Verifier Agent 구현 바인딩(01-runtime §4.1). 진입점 내부 역할 계약은 02 §4 소관. | Verifier Agent Module 정의 파일 = `.claude/agents/verifier.md`(실재). 활성화 = 서브에이전트 위임 시 이 정의 파일 로딩(Resolve, runtime-binding.md §3.2 Agent Module 동형). `entrypoint` 추상 참조의 물리 해소는 §3.1. 진입점 내부 역할 계약(입력·출력·판정 경계)은 02 §4·verifier.md 소관 — 포인터만. | 진입점 정의 파일 실재(§7 실측). 실행 진입점(형태 B)은 미도입. |
| 2 | Verifier 구현 디렉터리 | `framework/verifier/`(01-runtime §4.1 Module 구현 디렉터리). | `framework/verifier/` 디렉터리(실재)에 V1~V5 확정본 5문서 배치 — verification-report.md·module-manifest.md·verifier-protocol.md·rework-instruction.md·criteria-catalog.md. 계약 인스턴스 자리다(문서 본문 AI·형식 비의존 — C-3 확장). 실행 코드 배치는 형태 B(§3.1). | 디렉터리·5문서 실재(§7 실측). 실행 코드는 형태 B. |
| 3 | 검증 리포트(§3.2-A) 직렬화 | Markdown 리포트 파일 또는 구조화 파일. 검증 산출물 위치. | 구조화 Markdown 문서로 직렬화, `docs/v0.X-verification-report.md` 명명 관례로 `docs/`에 저장. 6필드(06 §3.2-A)를 절 구조로 담는다(§1 target … §6 rework). 형식·명명·위치의 물리 실현 정본은 §4. | 형식·명명·저장 위치 확정(정본). 2건 실증 실재(v0.3·v0.4, §7 실측). 개별 v0.5 인스턴스는 판정/시연 시 생성(시연 Task 소관·예정). |
| 4 | 판정 대상 회수 | 산출물 = 위임 output이 지정한 파일 경로. Worker 완료 보고 = 서브에이전트 최종 응답(02 §4.1). | 산출물 회수 = 파일 조회 도구로 위임 output 지정 경로를 전문 판독(§5 VT-1). Worker 완료 보고 회수 = 서브에이전트 최종 응답(delegation-protocol.md §3.2). 완료 보고는 검사 대상(claim)일 뿐 판정 근거가 아니다(06 V1/INV-1). | 회수 채널 규약 실현(형태 A, Bootstrap). 2건 실사용 실증. |
| 5 | 검사 도구 바인딩(VT-1~VT-5) | 존재 확인·전수 스캔·시연 실행에 쓰는 Claude Code 표면의 도구(파일 조회, 텍스트 검색, 명령 실행 등). | §5 — VT별 도구 바인딩(VT-1 존재 확인·VT-2/VT-3 정독 대조 = 파일 조회, VT-4 전수 스캔 = 텍스트 검색, VT-5 시연 = 명령 실행 + 파일 조회). verification-checklist.md §7(운용 지침)과 정합 — 물리 실현 정본은 §5. | 도구 표면 실재. 2건 실사용 실증(v0.3·v0.4). |
| 6 | 재작업 지시(§3.2-D) 전달 | Advisor/Loop가 Worker 서브에이전트에게 재위임 메시지로 전달한다. 전달·전이 채널은 03-loop·02 §4 소관. | 재작업 지시(06 §3.2-D 4필드)는 리포트 `rework` 절(§6)로 직렬화(§4.2, rework-instruction.md 인스턴스). 전달 = Advisor/Loop 재위임 메시지(delegation-protocol.md §3.1). 전달·전이 채널 정본은 03-loop·02 §4 — 본 문서는 직렬화·물리 전달 표면만 바인딩. | 직렬화 실재(2건 §6 실증). 전달 채널 규약 실현(형태 A). |
| 7 | 실행 모델 바인딩 | Verifier 역할의 실행 모델 지정은 02 §4 실행 모델 바인딩 영역이다. 06은 참조만 하고 지정하지 않는다. | 02 §4 소관(SP-6). `.claude/agents/verifier.md`는 실행 모델을 지정하지 않는다 — **세션 상속**(verifier.md 머리 명시). 본 문서도 지정하지 않고 참조만 한다. | 02 §4 소관. 본 문서 비지정(세션 상속 규약 — §7 실측). |

주:

- 위 7행은 06 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 06 §4.1 정본 표현을 이 환경의 구체 경로·형식·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **형태 A / 형태 B 구분(정직).** 행 1(진입점 정의 파일)·행 2(구현 디렉터리 5문서)·행 3(리포트 2건)은 물리 실재다. 행 4(회수)·행 6(전달)은 Bootstrap에서 **규약 실현(형태 A)**이다 — 서브에이전트 최종 응답·재위임 메시지로 수행되며, 별도 실행 채널 코드는 형태 B다. 행 5(검사 도구)는 도구 표면이 실재하고 2건 실사용으로 실증되었으나, 무인 도구 배선(트리거·오케스트레이션)은 형태 B/Loop 소관이다. 행 7(실행 모델)은 02 §4 소관으로 본 문서가 지정하지 않는다.
- **Verifier = Agent Module(회수 채널의 성격).** Verifier는 서브에이전트로 디스패치되는 Agent Module이므로, 판정 대상·완료 보고 회수(행 4)와 재작업 지시 전달(행 6)이 **서브에이전트 위임/최종 응답 채널**로 실현된다. 이는 단일 Port로 소비되는 Cross-cutting Service(Memory)의 Port 소비 경로와 다른 실현 방식이다(memory-binding.md §4.1 Register/Resolve 주와 대비 — §3.1).
- **미래 산출물 불주장(L-07).** v0.5 검증 리포트의 개별 인스턴스는 현 시점 **미존재**다(§7 실측). 행 3의 실재는 v0.3·v0.4 2건과 명명·형식·위치 관례에 대한 것이며, v0.5 인스턴스는 v0.5 판정(CP2) 또는 시연 Task 수행 시 생성될 **예정** 산출물이다. 본 문서는 그 미래 산출물의 실재를 주장하지 않는다.

---

## §3. entrypoint 물리 해소 · configSchema 물리 반영 대상 부재 (done 3)

module-manifest.md(V2 확정본)가 "물리 해소는 Adapter Binding 문서 소관"으로 미룬 `entrypoint` 지점을 확정하고, `configSchema` 생략(DP-V2)이 물리 반영 대상 부재로 귀결됨을 명시한다. runtime-binding.md §4·memory-binding.md §4의 교체 지점 관례(추상 참조 → 물리 실현, 형태 A/B 구분)와 동형으로 서술한다.

### §3.1 `entrypoint` 추상 참조의 물리 해소

module-manifest.md §2·§4 `entrypoint` = "추상 참조 — 판정 연산 Verify(06 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4)". 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Provider Module 활성화 진입 — 판정 연산 Verify(06 §3.1) 노출 | **형태 A(Bootstrap):** 활성화 진입은 규약으로 실현된다 — 진입점 = `.claude/agents/verifier.md`(Verifier 역할 정의 파일, 실재). 판정 연산 Verify는 verifier-protocol.md §2의 5단계 절차(입력 수령 → 기준 확인 → 항목별 판정 → 최종 판정 도출 → 리포트 산출) 준수로 수행되며, 산출물은 §4의 검증 리포트로 직렬화된다. 별도 실행 진입점 파일은 없다. | 규약 실현(형태 A) |
| 위 진입점의 실행 코드 로케이터 | **형태 B:** Verify 연산을 노출하는 실행 코드가 non-core 실행 경계(`framework/verifier/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 판정 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지). | 형태 B |

- **Register/Resolve 정합(runtime-binding.md §3.2 Agent Module 동형).** 이 Provider의 등록(Register)은 정의 파일 배치(`.claude/agents/verifier.md` 실재)로 규약 실현되며(형태 A), 해소(Resolve)는 서브에이전트 위임 시 이 역할의 활성 정의 파일이 로딩되는 것이다. Verifier는 서브에이전트로 디스패치되는 **Agent Module**이므로, Resolve가 Port 소비가 아니라 **서브에이전트 디스패치**로 실현된다(runtime-binding.md §3.2 Resolve/Replace — Agent Module은 위임 시 정의 파일 로딩). 이는 Memory(Cross-cutting Service, Port 소비 경로 Resolve — memory-binding.md §4.1)와 구별되는 실현 방식이다. 이 등록 경로는 이식 교체 지점 SP-1에 대응한다(§6).
- 진입점 내부의 역할 계약(위임 입력 in → 검증 리포트/연산 실패 보고 out, 판정 경계)은 verifier.md·02 §4 소관이며 본 문서는 재서술하지 않고 포인터만 둔다(06 §4.1 "진입점 내부 역할 계약은 02 §4 소관").

### §3.2 `configSchema` 물리 반영 대상 부재 (DP-V2 — Memory `recall.limit.max` 대응 절과의 차이)

module-manifest.md는 Advisor 결정 DP-V2로 `configSchema`를 **선언하지 않는다**(module-manifest.md §2·§3·§5 DP-V2 — 06 §3 판정 계약에 이 Provider가 소비하는 Config 의존 값이 없다). 따라서 본 문서에는 **물리 반영할 Config 값이 없다**.

- **정직한 차이 기록.** 자매 문서 memory-binding.md §4.2는 Memory Manifest의 `configSchema` 키 `recall.limit.max`(유한 양의 정수, 기본 20)의 물리 반영(값·기본값 선언 위치 → override 물리 소스 → 읽히는 지점 → 적용 방식)을 확정했다. Verifier Manifest에는 대응하는 `configSchema` 키가 없으므로(DP-V2 생략), 본 문서에는 그에 대응하는 **물리 반영 절이 존재하지 않는다.** 이 부재는 누락이 아니라 계약(module-manifest.md §5 DP-V2)의 정직한 반영이다.
- **경계(창설 금지).** `configSchema`에 의미(예: 판정 엄격 모드 `verify.strict`)를 부여해 물리 반영으로 끌어오지 않는다 — 그것은 06 §3.2-C 결정적 최종 판정 도출·§3.3 불변 규칙과 충돌하는 계약 창설이 된다(module-manifest.md §5 DP-V2 회피 규칙). 본 문서는 존재하지 않는 Config 값을 물리 반영으로 창설하지 않는다. `verify.strict`는 Config 병합 규칙의 예시 키일 뿐이며(01 §8 예2·framework/core/config-schema.md §6), 본 Adapter Binding은 이를 Verifier 판정 의미로 바인딩하지 않는다.
- **형태 구분.** v0.5 Bootstrap에서 Verifier의 Config 의존은 없다(형태 A·B 공통). 실행 로더(형태 B) 도입 시에도 Verifier Manifest가 `configSchema`를 선언하지 않는 한 effective config 병합 대상이 아니며, 이 부재의 계약(module-manifest.md §5 DP-V2)은 이식·형태 전환에도 불변이다(structure.md §7 C-1).

---

## §4. 검증 리포트 직렬화·저장 위치 확정 · 재작업 지시 전달 (done 4)

06 §4.1 "검증 리포트(§3.2-A) 직렬화 — Markdown 리포트 파일 또는 구조화 파일. 검증 산출물 위치"와 "재작업 지시(§3.2-D) 전달" 두 행의 물리 실현을 확정한다. 계약(06 §3.2-A/D)과 그 인스턴스(verification-report.md·rework-instruction.md)는 재정의하지 않고 § 포인터·문서명으로만 인용한다.

### §4.1 검증 리포트 직렬화·저장 위치 (정본 — 06 §4.1 검증 리포트 직렬화 행)

- **직렬화 형식.** 검증 리포트는 **구조화 Markdown 문서**로 직렬화된다. 06 §3.2-A의 6필드(`target`/`criteria_basis`/`items`/`final_verdict`/`verifier_scope`/`rework`)를 문서 절 구조로 담는다 — `§1 target` / `§2 criteria_basis` / `§3 items`(항목별 판정 표: `criterion`/`verdict`/`evidence`/`scope`/`verification_type` 열, 06 §3.2-B) / `§4 final_verdict` / `§5 verifier_scope` / `§6 rework`. 이 절 ↔ 필드 대응은 verification-report.md §6(v0.3·v0.4 실사용 필드 대응표, V1 확정본)이 이미 실증했으며, 본 문서는 그 구조를 물리 실현으로 인용만 한다(스키마 정본은 06 §3.2-A/B/C·verification-report.md).
- **명명 관례·저장 위치.** 저장 위치 = `docs/`, 명명 관례 = `docs/v0.X-verification-report.md`(X = 대상 마일스톤 버전). 이는 검증 산출물이 스캔·실측 결과 보고에 필요한 구체 토큰·물리 경로 인용을 정당하게 보유하는 **구조화 검증 산출물 문서**이기 때문이며(두 리포트 §0 거버넌스), 은닉 백엔드(Memory Store 같은 격리 데이터)가 아니다. 문서 머리에는 작성일·수행 주체·근거 정본·§9 이력 절을 둔다(docs 거버넌스 관례 동형).
- **실증(실측).** 이 형식·명명·위치는 **2건의 확정 실사용 인스턴스**로 실증된다 — `uahf/docs/v0.3-verification-report.md@cd9247b`(§7 실측 — 아카이브)·`uahf/docs/v0.4-verification-report.md@cd9247b`(§7 실측 — 아카이브). 각각 CP2 독립 판정 산출물이며 Baseline으로 확정되었다. 두 리포트가 6필드 절 구조·Fail→재검증 Pass 사이클·rework 절 직렬화를 실사용했다(verification-report.md §6·rework-instruction.md §6 대응표).
- **미래 인스턴스.** v0.5 검증 리포트의 개별 인스턴스는 현 시점 미존재이며(§7 실측), v0.5 판정(CP2) 또는 시연 Task 수행 시 이 관례대로 생성될 **예정**이다. 본 문서는 그 미래 산출물의 실재를 주장하지 않는다(L-07). 시연 절차·픽스처 상세는 시연 Task(동시 작성 중, 07 R2) 소관이며 본 문서가 서술하지 않는다.

### §4.2 재작업 지시 직렬화·전달 (정본 — 06 §4.1 재작업 지시 전달 행)

- **직렬화.** 재작업 지시(06 §3.2-D 4필드: `violated_items`/`expected_state`/`revalidation_criteria`/`evidence_gap`, rework-instruction.md 인스턴스)는 검증 리포트의 `rework` 절(문서 §6)로 직렬화된다. `final_verdict`가 Fail 또는 Conditional일 때 필수로 채워지고, Pass면 "없음"이다(06 §3.2-A `rework` 조건부·§3.2-C, rework-instruction.md §3). 두 실사용 리포트 §6이 발행(Fail)→이행→재검증(Pass)에서 `rework`가 "없음"으로 전이하는 사이클을 실증했다.
- **전달.** 전달은 Advisor/Loop가 Worker 서브에이전트에게 보내는 **재위임 메시지**로 실현된다(delegation-protocol.md §3.1 위임 디스패치, verification-checklist.md §7 "재작업 지시 전달"). 
- **경계(정본 유지).** 재작업 지시의 **전달·라우팅·전이 채널**은 03-loop·02 §4 소관이며(06 §4.1 "전달·전이 채널은 03-loop·02 §4 소관", rework-instruction.md §5), 본 문서는 리포트 내 직렬화 표면과 물리 전달 채널(재위임 메시지)만 바인딩한다. 재작업 루프의 구동·재시도 한도·시점·전이는 정의하지 않는다(06 INV-9).

---

## §5. VT-1~VT-5 검사 도구 바인딩 (done 5)

criteria-catalog.md §5가 "검사 도구·구체 토큰의 물리 실현은 Adapter Binding 문서 소관(06 §4.1 검사 도구 바인딩 행·§4.2 SP-3)"으로 미룬 지점을 확정한다. **이 문서는 Adapter 경계이므로 구체 도구·형식 토큰의 사용이 허용된다(§0 격리 지점).** VT-1~VT-5(06 §3.2-E, criteria-catalog.md §2) 각각을 이 환경의 검사 도구에 바인딩한다.

| 검증 유형 (06 §3.2-E) | 판정 방법 (정본 요지) | 검사 도구 바인딩 (claude 환경) | 확정 실사용 실증 (docs/ 리포트) |
|---|---|---|---|
| **VT-1 산출물 존재 검증** | 지정 산출물이 실제로 존재·접근 가능한지 확인 | **파일 조회 도구**로 위임 output 지정 경로의 실재·접근을 실측(부재·결손 검출). 필요 시 크기·라인 수 실측. | v0.3 §1(산출물 8종 실재·byte 실측)·v0.4 §1(문서 9종 + 물리 데이터 21파일·index 21라인 실측). |
| **VT-2 완료 조건 대조 검증** | 각 완료 조건(done)을 산출물과 항목별 대조 | **파일 조회 도구**로 산출물을 **전문** 정독(표본 금지) + 위임 done 항목별 1:1 대조. | v0.3 §2·items #2~#5·v0.4 §2·items #2~#5·#20~#30. |
| **VT-3 규격 준수 검증** | 규격의 각 항목을 산출물과 대조 | **파일 조회 도구**로 규격(TEMPLATE DoD·대상 spec §7·상위 계약 §3.2 스키마)과 산출물을 **셀 단위** 대조. | v0.3 items #4·#9·#11·v0.4 items #5·#9·#10·#27·#28. |
| **VT-4 경계 검증** | 금지 요소를 전수 스캔(exhaustive scan), 검사 범위를 해당 경계 전 범위로 명시 | **텍스트 검색 도구**로 금지 요소 후보 집합 **전체**를 검사 범위 **전 범위**에 대해 전수 스캔. 단일 대리 지표(단일 토큰 검색) 하나로 대체하지 않는다(06 §3.2-E 주의·INV-4). 매치는 금지 토큰/정당 참조로 분류. | v0.4 §3.3(후보 5부류 전수 스캔·매치 분류표)·v0.3 §3.2(Core 경계 후보 부류 전수 스캔). |
| **VT-5 시연 검증** | 시연 시나리오를 실제로 재현하고 결과를 관측 | **명령 실행 도구**로 시연 시나리오 재현·독립 재계산 + **파일 조회 도구**로 산출물 자체 재관측(관측 주장을 신뢰하지 않고 재판정). | v0.4 §3.2(물리 실데이터 직접 재관측·재계산)·v0.3 §3.3(시연 재현·도출 재계산). |

- **금지 요소 후보 토큰의 운용 목록.** VT-4 전수 스캔이 대상으로 삼는 금지 요소 후보 토큰의 **운용 목록**(특정 AI 이름·모델명·제품 기능명·`claude-*` 패턴 등)은 docs/verification-checklist.md §7이 이 프로젝트 표면에서 소유한다(운용 지침 — 게이트에서 무엇을 검색하는가). 이 문서는 Adapter 경계로서 그 구체 토큰 인용이 허용되나, 운용 목록을 복제하지 않고 checklist §7을 소관 포인터로 참조한다. 본 문서가 확정하는 것은 **VT ↔ 검사 도구의 물리 바인딩**(어떤 도구로 각 유형을 실현하는가)이다.
- **verification-checklist.md §7과의 정본 소유 관계(재정의 0).** verification-checklist.md §7은 Advisor 검증 게이트(게이트 C)에서 이 도구들을 **어떻게 쓰는가**를 규율하는 **운용 지침**이다("산출물 정독 = 파일 조회 도구로 전체", "전수 스캔 = 텍스트 검색 도구로 후보 집합 전체", "판정 기록 산출 = Markdown 등 구조화 파일" 등). 본 문서 §5는 06 §4.1 검사 도구 바인딩 행의 **물리 실현 정본**이다 — VT별 도구 배선의 확정 자리. 둘은 **정합**하며(같은 도구·같은 전수 스캔 원칙), 본 문서는 checklist §7 운용 지침을 재정의하지 않고, checklist §7은 본 문서의 물리 바인딩을 게이트 운용으로 적용한다. 재정의가 아니라 정본(물리 바인딩)/운용(게이트 사용법)의 소유 구분이다.
- **경계.** 검사 도구는 이식 교체 지점 SP-3이다(§6) — 대상 환경의 검사 도구로 교체되며, VT-1~VT-5 유형·판정 방법·충족 조건·전수 스캔 규칙(06 §3.2-E·INV-4, criteria-catalog.md §2·§3)은 유지된다. 무인 도구 배선(트리거·오케스트레이션)은 형태 B/Loop 소관이며 본 문서는 도구 표면 바인딩만 확정한다.

---

## §6. 06 §4.2 이식 교체 지점 SP-1~SP-6 대응 (done 2)

06 §4.2 이식 교체 지점 SP-1~SP-6 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인한다.

| # (06 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Verifier Module 진입점 파일 위치·포맷 → 대상 환경의 Agent 정의 메커니즘 | §2 #1, §3.1 | `.claude/agents/verifier.md` 진입점 정의 파일 위치·포맷, 서브에이전트 위임 시 로딩(Resolve), 형태 B 실행 코드 로케이터. | Verify 연산 계약(06 §3.1), 진입점 내부 역할 계약(02 §3.2-A·verifier.md), Provider 등록·해소 계약(01 §3.1-A·§4). |
| SP-2 | 검증 리포트 직렬화·저장 위치 → 대상 환경의 산출물 포맷 | §2 #3, §4.1 | 구조화 Markdown 문서 직렬화, `docs/v0.X-verification-report.md` 명명·저장 위치, 6필드 절 구조. | 검증 리포트 6필드(06 §3.2-A)·판정 값 3종(§3.2-B)·최종 판정 도출 규칙(§3.2-C). V1 확정본(verification-report.md) 인스턴스. |
| SP-3 | 검사 도구(존재 확인·전수 스캔·시연 실행) → 대상 환경의 검사 도구 | §2 #5, §5 | 파일 조회·텍스트 검색·명령 실행 도구, 금지 토큰 후보 운용 목록(checklist §7). | 검증 유형 카탈로그 VT-1~VT-5(06 §3.2-E), 검사 범위 정직·전수 스캔(V4/INV-4), 거짓 완료 보고 검출 계약(§3.2-F). V5 확정본(criteria-catalog.md). |
| SP-4 | 판정 대상·완료 보고 회수 채널(서브에이전트 최종 응답) → 대상 환경의 결과 반환 채널 | §2 #4, §5(VT-1) | 파일 조회로 산출물 회수, 서브에이전트 최종 응답으로 Worker 완료 보고 회수. | Verify 입력(산출물 + 대조 기준, 06 §3.1), 독립성(완료 보고는 판정 근거 아님 — V1/INV-1). |
| SP-5 | 재작업 지시 전달 채널 → 대상 환경의 재위임·오케스트레이션 메커니즘(03-loop 정식화) | §2 #6, §4.2 | 리포트 `rework` 절 직렬화 + 재위임 메시지 전달(서브에이전트 디스패치). | 재작업 지시 4필드(06 §3.2-D). 전달·전이 채널 정본은 03-loop·02 §4(본 문서는 참조만). V4 확정본(rework-instruction.md). |
| SP-6 | Verifier 실행 모델 지정 → 02 §4 소관. 06은 참조만 한다 | §2 #7 | 02 §4 실행 모델 바인딩 영역(예: 세션 상속 / 특정 실행 모델 지정). verifier.md는 미지정(세션 상속). | §3.2-A 역할 경계·메시지 필수 필드(02 §3). 06·본 문서는 지정하지 않고 참조만(02 §4.2 "유지되는 것"). |

- "유지되는 것" 열의 계약(검증 리포트·판정 값·최종 판정 도출·재작업 지시 4필드·검증 유형·거짓 완료 보고 검출 계약·§3.3 Invariants)은 다른 AI·환경으로 이식해도 바뀌지 않는다 — 06 §4.2 말미 "유지되는 것" 목록의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다. V1~V5 확정본(framework/verifier/ 5문서)이 그 계약의 인스턴스이며, 이식 시에도 이 인스턴스의 계약 요소는 불변이다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(06 §4.2 말미·runtime-binding.md §4·memory-binding.md §6 동형). 본 문서는 그 정식화를 선취하지 않고 v0.5 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 7 — A5/L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록 — A5 재작업 사례: 미존재 소스를 "실재"로 서술한 것을 파일 시스템 전수 대조로 검출한 데서 도출)에 따라, 본 문서의 "실재/존재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(Glob) + 파일 크기 직접 실측.**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — runtime-binding.md·memory-binding.md 존재 확인. |
| `framework/adapters/claude/runtime-binding.md` | 실재 (v0.3 Baseline, 자매 문서) | 실재 (32,973 bytes). |
| `framework/adapters/claude/memory-binding.md` | 실재 (v0.4 Baseline, 자매 문서) | 실재 (51,144 bytes). |
| `framework/adapters/claude/verifier-binding.md` | 실재 (본 문서 — 본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음. |
| `.claude/agents/verifier.md` (§2 #1 진입점) | 실재 (진입점 정의 파일, 실행 모델 미지정=세션 상속) | 실재 (11,357 bytes). 실행 모델 지정 없음 — 세션 상속(front-matter `model` 키 부재) 확인. |
| `framework/verifier/` 5문서 (§2 #2 구현 디렉터리) | 실재 (V1~V5 확정본) | 실재 — 5파일 확인: verification-report.md(19,656)·module-manifest.md(24,567)·verifier-protocol.md(33,523)·rework-instruction.md(27,306)·criteria-catalog.md(32,478). |
| `uahf/docs/v0.3-verification-report.md@cd9247b` (§4.1 직렬화 실증) | 아카이브 (실사용 인스턴스 1) | @cd9247b 시점 실재 (43,698 bytes) — 산출물 수명 정책으로 작업 트리에서 제거(열람 `git show`). |
| `uahf/docs/v0.4-verification-report.md@cd9247b` (§4.1 직렬화 실증) | 아카이브 (실사용 인스턴스 2) | @cd9247b 시점 실재 (51,649 bytes) — 산출물 수명 정책으로 작업 트리에서 제거(열람 `git show`). |
| v0.5 검증 리포트 인스턴스 (§4.1 미래 인스턴스) | **미존재** (v0.5 판정/시연 시 생성 예정 — 시연 Task 소관) | **미존재** — `docs/v0.5-*.md` 파일 열거 결과 0건. 미래 산출물로 실재 불주장. |
| 검사 도구 표면 (§5 — 파일 조회·텍스트 검색·명령 실행) | 실재 (현 환경 도구 표면) | 실재 — 본 검증 수행에 사용된 도구 표면(2건 리포트가 실사용 실증). |
| Verifier `configSchema` 물리 반영 대상 (§3.2) | **없음** (DP-V2 생략 — Memory `recall.limit.max` 대응 절 부재) | 부재 확인 — module-manifest.md §2·§5에서 `configSchema` "선언하지 않음(DP-V2)" 확인. 물리 반영할 Config 값 0. |
| Verify 연산 실행 진입점·실행 로더 (형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). `framework/verifier/`는 계약 문서 5건만 실재(실행 코드 0). |

- **핵심 구분.** 본 문서가 확정한 검증 리포트 직렬화·명명·저장 위치와 VT별 검사 도구 바인딩은 **정본**이며, v0.3·v0.4 확정 실사용 리포트 2건이 이 관례를 실증한다 — 실측이 정본과 일치한다(형식·명명·6필드 절 구조·rework 절·검사 도구 실사용). v0.5 개별 리포트 인스턴스는 미존재이며 시연/판정 Task 수행 시 생성될 예정이다(데이터 생성 주체는 본 문서 M6가 아님 — 구조·형식·관례·바인딩의 정본만 소유).
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로, 미래 산출물을 현재 실재로 쓰지 않았다(A5/L-07 재발 방지, L-01 상태 서술 전수 대조).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 6).** 본 문서의 모든 매핑은 06 §3·§4·framework/verifier/ 5문서의 물리 실현이다. 어떤 연산·데이터 계약·불변 규칙·검증 유형·판정 값·재작업 지시 필드도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 정본 §(06 §3·verification-report.md·module-manifest.md·verifier-protocol.md·rework-instruction.md·criteria-catalog.md)다. 새 바인딩 계약을 06 §4.1 표를 넘어 창설하지 않았고, 새 검증 유형·판정 값·reason·필드·Config 값을 추가하지 않았다.
- **계약 소유 명시.** 검증 리포트 스키마 = verification-report.md/06 §3.2-A/B/C, Manifest 필드·`entrypoint`·`configSchema` 결정 = module-manifest.md/01 §3.2-A, Verify 연산 절차 = verifier-protocol.md/06 §3.1, 재작업 지시 포맷 = rework-instruction.md/06 §3.2-D, 검증 유형·기준 부류 = criteria-catalog.md/06 §3.2-E/A. 본 문서는 이들의 **물리 실현**(직렬화 형식·명명·저장 위치·진입점 물리 해소·검사 도구 배선·회수/전달 물리 채널)만 확정한다. checklist §7은 게이트 운용 지침이며 본 문서 §5(물리 바인딩 정본)와 정합한다(재정의 0).
- **격리 토큰의 단일 자리.** 구체 진입점 경로(`.claude/agents/…`)·직렬화 형식(Markdown)·물리 경로(`docs/…`·`framework/adapters/claude/…`)·검사 도구명·서브에이전트/세션 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. framework/verifier/ 5문서(Module 구현 디렉터리 문서 본문)는 이 토큰을 "Adapter Binding 문서 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3 확장은 이 경계에 비적용 — 격리 보유, runtime-binding.md §5·memory-binding.md §8 동형).
- **동시 작성 문서 경계(07 R2) 및 미래 산출물(L-07).** 같은 Wave에서 동시 작성 중인 시연 절차서(docs/v0.5-demo-procedure.md, V7)의 내용을 인용·추측하지 않았다(07 R2 준수 — memory-binding.md가 동시 작성 demo-procedure를 불인용한 선례 동형). 시연 절차·픽스처 상세는 서술하지 않았고, 시연 수행 시 생성될 산출물(v0.5 검증 리포트 등)의 실재를 주장하지 않았다 — 미래 산출물은 "시연/판정 Task 소관·예정"으로 구분했다(L-07). 참조한 확정 정본은 06(정본)·framework/verifier/ 5문서(V1~V5 확정본)·.claude/agents/verifier.md(진입점 실물)·자매 Adapter Binding 2문서·docs/verification-checklist.md·확정 실사용 리포트 2건(v0.3·v0.4)·framework/core/structure.md·specs/00-glossary.md뿐이다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 이 1개 파일(`framework/adapters/claude/verifier-binding.md`)만 생성하며, `.claude/agents/verifier.md`·framework/verifier/ 5문서·기존 Baseline 산출물(runtime-binding.md·memory-binding.md·두 검증 리포트 등)·specs/·docs/를 수정·생성하지 않는다.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-VB-1 (checklist §7 참조 정합 — 비차단).** verification-checklist.md §7(게이트 운용 지침)은 검사 도구를 이미 바인딩하나, 06 §4.1 검사 도구 바인딩 행의 **물리 실현 정본**이 본 문서 §5임을 아직 § 포인터로 가리키지 않는다(checklist §7은 06 §4.1·§4.2 SP-3을 인용). 두 문서는 정합하나(같은 도구·같은 전수 스캔 원칙), checklist §7에 본 문서(§5)를 물리 실현 정본으로 명시하는 상호 참조를 추가할지는 Advisor 판단 대상이다. 본 Task 소유 경계는 이 1파일이므로 checklist §7을 수정하지 않았다(07 R4). 정본 소유 관계는 §5에 명시했으므로 계약 갭은 아니다 — 비차단.
- **OQ-VB-2 (형태 B 경계 분할 — 비차단).** Verify 연산 실행 코드(형태 B)가 `framework/verifier/` Module 구현 디렉터리와 `framework/adapters/claude/` 사이 어디에 분할 배치되는지는 형태 B 설계 시 확정 대상이다(§3.1, structure.md §4 규칙 4 defer). Bootstrap(형태 A)에서는 규약 실현이므로 이 분할이 필요하지 않으며, 계약(06 §3) 변경이 아니므로 비차단이다.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 세 번째 산출물(선행: runtime-binding.md·memory-binding.md). 06 §4.1(Verifier 바인딩 표 7행)의 **v0.5 물리 실현 매핑**. 정본 = 06 §3·§4 + framework/verifier/ 5문서(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 06 §4.1 표 **7행 전부**를 물리 표면으로 매핑("물리 실현" 열 + "실재 여부" 열, 형태 A/B 정직 구분). 진입점 정의 파일·구현 디렉터리 5문서·리포트 2건 = 실재; 회수·전달 = 규약 실현(형태 A); 실행 진입점·로더 = 형태 B 예정. Verifier = Agent Module(서브에이전트 회수 채널).
- **§3:** `entrypoint` 물리 해소(형태 A = `.claude/agents/verifier.md` + verifier-protocol.md 절차 준수 / 형태 B = 실행 코드 로케이터 defer, Register/Resolve = 서브에이전트 디스패치) + `configSchema` 생략(DP-V2)으로 **물리 반영 대상 부재** 명시(Memory `recall.limit.max` 대응 절과의 정직한 차이).
- **§4:** 검증 리포트 직렬화·저장 위치 확정(구조화 Markdown 문서, `docs/v0.X-verification-report.md` 명명, 6필드 절 구조 — v0.3·v0.4 2건 실증·실측) + 재작업 지시 `rework` 절 직렬화·재위임 전달(전달·전이 채널 정본은 03-loop·02 §4).
- **§5:** VT-1~VT-5 검사 도구 바인딩(존재 확인/정독 = 파일 조회, 전수 스캔 = 텍스트 검색, 시연 = 명령 실행) + verification-checklist.md §7 정본 소유 관계(§7 = 운용 지침, 본 문서 = 물리 실현 정본, 정합·재정의 0). 후보 토큰 운용 목록은 checklist §7 소유.
- **§6:** 06 §4.2 이식 교체 지점 SP-1~SP-6 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 이식 불변(C-1) 재확인(검증 리포트·판정 값·재작업 지시 필드·검증 유형·검출 계약·Invariants).
- **§7:** 실측 대조(2026-07-06 직접 실측) — 진입점·5문서·리포트 2건 실재, v0.5 리포트 미존재(미래 산출물), configSchema 물리 반영 대상 부재, 형태 B 미도입. 실측 불일치 0건(A5/L-07 재발 방지).
- 06·framework/verifier/ 5문서 계약 재정의 0, Glossary 용어 신설 0, 새 바인딩 계약 창설 0. 구체 AI·환경·형식·검사 도구 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 동시 작성 시연 절차서 불인용(07 R2), 미래 산출물 실재 불주장(L-07). 이 1파일만 생성.
