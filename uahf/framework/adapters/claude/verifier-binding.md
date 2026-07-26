# framework/adapters/claude/verifier-binding — Claude Code Verifier Adapter 바인딩

작성일: 2026-07-06
상태: v0.5 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본 (계약 요소는 § 포인터로만 인용 — 재정의 0 선언은 §0 1곳):

- specs/06-verifier.md — §3.1 Verify 연산 · §3.2-A 검증 리포트 6필드 · §3.2-B 판정 값 3종 · §3.2-C 최종 판정 도출 · §3.2-D 재작업 지시 4필드 · §3.2-E 검증 유형 VT-1~VT-5 · §3.2-F 거짓 완료 보고 검출 · §3.3 INV-1~INV-10 · §4.1 Claude Code Binding 표 7행 · §4.2 이식 교체 지점 SP-1~SP-6.
- framework/verifier/ 5문서(V1~V5 확정본 — 계약 인스턴스, 본 문서가 물리 실현만 확정) — verification-report.md(리포트 스키마·§6 실사용 필드 대응표) · module-manifest.md(`entrypoint` 추상 참조의 물리 해소 위임 · `configSchema` 생략 = DP-V2) · verifier-protocol.md(Verify 5단계) · rework-instruction.md(재작업 지시 4필드) · criteria-catalog.md(§2 VT 카탈로그·§5 검사 도구 바인딩 소관 포인터).
- `.claude/agents/verifier.md` — Verifier 역할 진입점 실물. 참조만·무수정(06 §4.1 진입점 행·SP-1·SP-6). 실행 모델 지정 여부는 02 §4 소관이며 본 문서는 그 값을 규정하지 않는다(§2 #7·§7 실측).
- docs/verification-checklist.md §7 — Advisor 검증 게이트 운용 바인딩(환경 의존 검사 도구 사용법·금지 토큰 후보 운용 목록 소유). 본 문서 §5(물리 실현 정본)와 정합.
- `uahf/docs/v0.3-verification-report.md@cd9247b` · `uahf/docs/v0.4-verification-report.md@cd9247b` — 검증 리포트 물리 직렬화·저장의 확정 실사용 인스턴스 2건(각 CP2 독립 판정 산출물, 산출물 수명 정책으로 작업 트리에서 제거·아카이브). 명명 관례·6필드 절 구조·rework 절 직렬화·검사 도구 실사용의 실증 근거(§4·§5·§7).
- specs/01-runtime.md §3.2-A/B·§4(Module Manifest·Config 병합·Provider 등록·물리 진입점 해소) · specs/00-glossary.md(용어 정본 — 신설 0) · framework/core/structure.md §2·§5·§6(Adapter 경계 = 격리 지점) · 자매 Adapter Binding runtime-binding.md·memory-binding.md(관례 정본) · ROADMAP.md v0.5.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다 — Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 06 §3.3 INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로·검사 도구 토큰의 사용이 허용된다(C-3 비적용 — 자매 2문서 §0 동형). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.5 Draft | 최초 작성. `framework/adapters/claude/` 경계의 세 번째 산출물(선행: runtime-binding.md·memory-binding.md). 06 §4.1 바인딩 표 **7행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정) 정직 구분(§2). V2 Manifest `entrypoint` 추상 참조의 물리 해소(형태 A = `.claude/agents/verifier.md` 진입점 + verifier-protocol.md 절차 준수 / 형태 B = 실행 코드 로케이터 defer) + `configSchema` 생략(DP-V2)으로 물리 반영 대상 부재 명시(Memory `recall.limit.max` 대응 절과의 차이 정직 기록, §3). 검증 리포트 직렬화·저장 위치 확정(docs/ 구조화 문서, `docs/v0.X-verification-report.md` 명명 관례 — v0.3·v0.4 2건 실증·실측) + 재작업 지시 rework 절 직렬화·재위임 전달(§4). VT-1~VT-5 검사 도구 바인딩(파일 조회·텍스트 검색·명령 실행) + verification-checklist.md §7 정본 소유 관계(§5). 06 §4.2 이식 교체 지점 SP-1~SP-6 대응 표("교체되는 것/유지되는 것" 열 — C-1 이식 불변 재확인, §6). 상태 서술 실측 대조 표(§7 — 실재 서술 전건 파일 시스템 실측 후 기입, L-07). 06 §3·framework/verifier/ 5문서 계약 재정의·창설 0, 새 바인딩 계약 0, Glossary 밖 새 용어 0. 동시 작성 시연 절차서(docs/v0.5-demo-procedure.md, V7) 내용 불인용(07 R2), 미래 산출물 실재 불주장(L-07). 이 1파일만 생성 — `.claude/agents/verifier.md`·framework/verifier/ 5문서·기존 Baseline 산출물·specs/ 무수정. | Worker (Advisor 위임, Task V6) |
| 2026-07-06 | v0.5 Baseline | v0.5 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 26/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지)·삭제 산출물(docs/v0.3·v0.4-verification-report.md 실사용 인스턴스 2건) 참조 @cd9247b 앵커 전환(§4·§7 실측 표 아카이브 표기). `docs/v0.X-verification-report.md` 명명 관례·계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 2 — 비계약 격리 개정: 재서술·스냅샷·죽은 참조 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/06-verifier.md §3·§4와 framework/verifier/ 5문서다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·필드·검증 유형·판정 값)를 **재정의·확장하지 않는다** — 정본 § 포인터로만 인용한다. **이 재정의 0 선언은 문서 전체에 대해 여기 1곳에서만 선언되며**, 이하 각 절은 이를 반복 선언하지 않고 정본 §만 지목한다.
- **소관 지점.** framework/verifier/ 5문서가 "물리 직렬화·저장 위치·검사 도구·물리 진입점 해소는 Adapter Binding 문서 소관"이라며 미룬 **직렬화 형식·명명 관례·저장 위치·물리 진입점 해소·검사 도구 배선**이 확정되는 유일한 자리가 이 문서다(06 §4, verification-report.md §5, module-manifest.md §4, criteria-catalog.md §5, rework-instruction.md §5, verifier-protocol.md §0).
- **격리 지점(C-3 비적용).** Core 경계와 Module 구현 디렉터리(`framework/verifier/` 등) 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 하지만(structure.md §5 C-3 확장, 06 §3.3 INV-8), 이 문서는 그 **반대편**이다 — 진입점 경로(`.claude/agents/…`)·직렬화 형식명·물리 경로(`docs/…`)·검사 도구명·서브에이전트/세션 토큰의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다.
- **검증 리포트 직렬화·저장 위치 정본 선언(done 4).** 검증 리포트의 물리 직렬화 형식(구조화 Markdown 문서)·명명 관례(`docs/v0.X-verification-report.md`)·저장 위치(`docs/`)의 **물리 실현 정본은 §4**다. 검증 리포트는 은닉 백엔드(예: Memory Store)가 아니라 구체 토큰 인용이 허용되는 **구조화 검증 산출물 문서**이며, 06 §4.1이 "검증 산출물 위치"로 Adapter Binding에 미룬 지점을 본 문서가 확정한다. 이 위치는 확정 실사용 인스턴스 2건으로 실증되었다(§7).
- **창설 금지.** 06 §4.1 표를 넘어서는 새 바인딩 계약·새 검증 유형·판정 값·재작업 지시 필드·불변 규칙·검사 도구 계약·Config 값을 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 Bootstrap 상태다(Glossary J-13). Verifier는 정식 실행 Module이 아니라 규약 문서(06·framework/verifier/ 5문서)와 관행(Advisor가 산출물을 정독해 판정을 구동 — verification-checklist.md §2 게이트 C)으로 실현되며(형태 A), 본 문서의 매핑은 **이미 실재하는 표면**(진입점 정의 파일·구현 디렉터리 5문서·확정 실사용 리포트 2건 — §7)과 **실행 코드 도입 시 로딩될 지점**(형태 B — Verify 실행 진입점·로더)을 구분한다. `형태 A/B`는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(done 1·7, L-07) · 용어.** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다. §2 "실재 여부" 열·§7 표가 그 대상이며, 두 곳 모두 **재실측으로 참·거짓이 갈리는 형태**로만 쓴다(byte·계수 스냅샷 불기재 — drift). 미래 산출물을 현재 실재로 쓰지 않는다. 용어는 Glossary 정본만 사용한다(검증 리포트·검증 유형·재작업 지시·거짓 완료 보고 = §3.2-J, 06 §9 승격 4건) — 신설 0.

---

## §1. 목적

이 문서는 06 §4.1(Verifier Claude Code Binding)을 이 환경 위의 구체 물리 실현으로 매핑한다. 정본 경계·격리·창설 금지·실측 규율 선언은 §0에 1벌만 둔다.

절별 책임 — §2 06 §4.1 바인딩 표 7행 전건의 물리 표면 확정 · §3 `entrypoint` 물리 해소 + `configSchema` 생략(DP-V2)에 따른 물리 반영 대상 부재 · §4 검증 리포트 직렬화·명명·저장 위치 + 재작업 지시 `rework` 절 직렬화·전달 · §5 VT-1~VT-5 검사 도구 바인딩 + verification-checklist.md §7과의 정본/운용 소유 관계 · §6 06 §4.2 SP-1~SP-6 대응 · §7 상태 서술 실측 대조.

형태 A → 형태 B 전환 시에도 Core Contract(06 §3) 변경은 0이며(structure.md §7 C-1), §6의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 06 §4.1 바인딩 표 7행 물리 실현 (done 1·7)

06 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. "06 §4.1 바인딩 (정본 인용)" 열은 정본 표현을 그대로 인용하고, "물리 실현" 열이 본 문서가 확정하는 경로·형식·채널·절차를(상세는 §3~§5 소유), "실재 여부" 열이 물리 실재/형태 A/형태 B를 구분한다(§7).

| # | §3 계약 요소 | 06 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Verifier Module 진입점 | `.claude/agents/verifier.md` — Runtime generic Module 계약의 Verifier Agent 구현 바인딩(01-runtime §4.1). 진입점 내부 역할 계약은 02 §4 소관. | Verifier Agent Module 정의 파일 = `.claude/agents/verifier.md`(실재). 활성화 = 서브에이전트 위임 시 이 정의 파일 로딩(Resolve, runtime-binding.md §3.2 Agent Module 동형). `entrypoint` 추상 참조의 물리 해소는 §3.1. 진입점 내부 역할 계약(입력·출력·판정 경계)은 02 §4·verifier.md 소관 — 포인터만. | 진입점 정의 파일 실재(§7 실측). 실행 진입점(형태 B)은 미도입. |
| 2 | Verifier 구현 디렉터리 | `framework/verifier/`(01-runtime §4.1 Module 구현 디렉터리). | `framework/verifier/` 디렉터리(실재)에 V1~V5 확정본 5문서 배치 — verification-report.md·module-manifest.md·verifier-protocol.md·rework-instruction.md·criteria-catalog.md. 계약 인스턴스 자리다(문서 본문 AI·형식 비의존 — C-3 확장). 실행 코드 배치는 형태 B(§3.1). | 디렉터리·5문서 실재(§7 실측). 실행 코드는 형태 B. |
| 3 | 검증 리포트(§3.2-A) 직렬화 | Markdown 리포트 파일 또는 구조화 파일. 검증 산출물 위치. | 구조화 Markdown 문서로 직렬화, `docs/v0.X-verification-report.md` 명명 관례로 `docs/`에 저장. 6필드(06 §3.2-A)를 절 구조로 담는다(§1 target … §6 rework). 형식·명명·위치의 물리 실현 정본은 §4. | 형식·명명·저장 위치 확정(정본). 2건 실증 실재(v0.3·v0.4, §7 실측). 개별 v0.5 인스턴스는 판정/시연 시 생성(시연 Task 소관·예정). |
| 4 | 판정 대상 회수 | 산출물 = 위임 output이 지정한 파일 경로. Worker 완료 보고 = 서브에이전트 최종 응답(02 §4.1). | 산출물 회수 = 파일 조회 도구로 위임 output 지정 경로를 전문 판독(§5 VT-1). Worker 완료 보고 회수 = 서브에이전트 최종 응답(delegation-protocol.md §3.2). 완료 보고는 검사 대상(claim)일 뿐 판정 근거가 아니다(06 V1/INV-1). | 회수 채널 규약 실현(형태 A, Bootstrap). 2건 실사용 실증. |
| 5 | 검사 도구 바인딩(VT-1~VT-5) | 존재 확인·전수 스캔·시연 실행에 쓰는 Claude Code 표면의 도구(파일 조회, 텍스트 검색, 명령 실행 등). | §5 — VT별 도구 바인딩(VT-1 존재 확인·VT-2/VT-3 정독 대조 = 파일 조회, VT-4 전수 스캔 = 텍스트 검색, VT-5 시연 = 명령 실행 + 파일 조회). verification-checklist.md §7(운용 지침)과 정합 — 물리 실현 정본은 §5. | 도구 표면 실재. 2건 실사용 실증(v0.3·v0.4). |
| 6 | 재작업 지시(§3.2-D) 전달 | Advisor/Loop가 Worker 서브에이전트에게 재위임 메시지로 전달한다. 전달·전이 채널은 03-loop·02 §4 소관. | 재작업 지시(06 §3.2-D 4필드)는 리포트 `rework` 절(§6)로 직렬화(§4.2, rework-instruction.md 인스턴스). 전달 = Advisor/Loop 재위임 메시지(delegation-protocol.md §3.1). 전달·전이 채널 정본은 03-loop·02 §4 — 본 문서는 직렬화·물리 전달 표면만 바인딩. | 직렬화 실재(2건 §6 실증). 전달 채널 규약 실현(형태 A). |
| 7 | 실행 모델 바인딩 | Verifier 역할의 실행 모델 지정은 02 §4 실행 모델 바인딩 영역이다. 06은 참조만 하고 지정하지 않는다. | 02 §4 소관(SP-6). 실행 모델 값은 `.claude/agents/verifier.md` front-matter가 보유하며 그 지정·변경 권한은 02 §4에 있다 — 본 문서는 값을 지정·규정하지 않고 참조만 한다. | 02 §4 소관. 본 문서 비지정. 현재 실물 값은 §7 실측(`model: opus`). |

주:

- 위 7행은 06 §4.1 표의 전 행이며, "물리 실현"은 정본 표현을 구체 경로·형식·채널로 좁힌 것이다(새 바인딩 창설 0 — §0).
- **형태 A / 형태 B 구분(정직).** 행 1(진입점 정의 파일)·행 2(구현 디렉터리 5문서)·행 3(리포트 실사용 인스턴스)은 물리 실재다. 행 4(회수)·행 6(전달)은 Bootstrap에서 **규약 실현(형태 A)** — 서브에이전트 최종 응답·재위임 메시지로 수행되며 별도 실행 채널 코드는 형태 B다. 행 5(검사 도구)는 도구 표면이 실재하고 실사용으로 실증되었으나 무인 도구 배선(트리거·오케스트레이션)은 형태 B/Loop 소관이다. 행 7(실행 모델)은 02 §4 소관으로 본 문서가 지정하지 않는다.
- **Verifier = Agent Module(회수 채널의 성격).** Verifier는 서브에이전트로 디스패치되는 Agent Module이므로 판정 대상·완료 보고 회수(행 4)와 재작업 지시 전달(행 6)이 **서브에이전트 위임/최종 응답 채널**로 실현된다 — 단일 Port로 소비되는 Cross-cutting Service(Memory)의 Port 소비 경로와 다른 실현 방식이다(§3.1).
- **미래 산출물 불주장(L-07).** v0.5 검증 리포트의 개별 인스턴스는 미존재다(§7). 행 3의 실재는 확정 실사용 리포트 2건과 명명·형식·위치 관례에 대한 것이며, 본 문서는 미래 산출물의 실재를 주장하지 않는다.

---

## §3. entrypoint 물리 해소 · configSchema 물리 반영 대상 부재 (done 3)

module-manifest.md(V2 확정본)가 "물리 해소는 Adapter Binding 문서 소관"으로 미룬 `entrypoint` 지점을 확정하고, `configSchema` 생략(DP-V2)이 물리 반영 대상 부재로 귀결됨을 명시한다(자매 2문서 §4의 교체 지점 관례 동형).

### §3.1 `entrypoint` 추상 참조의 물리 해소

module-manifest.md §2·§4 `entrypoint` = "추상 참조 — 판정 연산 Verify(06 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4)". 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Provider Module 활성화 진입 — 판정 연산 Verify(06 §3.1) 노출 | **형태 A(Bootstrap):** 활성화 진입은 규약으로 실현된다 — 진입점 = `.claude/agents/verifier.md`(Verifier 역할 정의 파일, 실재). 판정 연산 Verify는 verifier-protocol.md §2의 5단계 절차(입력 수령 → 기준 확인 → 항목별 판정 → 최종 판정 도출 → 리포트 산출) 준수로 수행되며, 산출물은 §4의 검증 리포트로 직렬화된다. 별도 실행 진입점 파일은 없다. | 규약 실현(형태 A) |
| 위 진입점의 실행 코드 로케이터 | **형태 B:** Verify 연산을 노출하는 실행 코드가 non-core 실행 경계(`framework/verifier/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 판정 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지). | 형태 B |

- **Register/Resolve 정합(runtime-binding.md §3.2 Agent Module 동형).** 등록(Register)은 정의 파일 배치(`.claude/agents/verifier.md`)로 규약 실현되며(형태 A), 해소(Resolve)는 서브에이전트 위임 시 이 역할의 활성 정의 파일이 로딩되는 것이다. Verifier는 **Agent Module**이므로 Resolve가 Port 소비가 아니라 **서브에이전트 디스패치**로 실현된다 — Memory(Cross-cutting Service의 Port 소비 경로 Resolve — memory-binding.md §4.1)와 구별된다. 이 등록 경로는 SP-1에 대응한다(§6). 진입점 내부의 역할 계약(위임 입력 → 검증 리포트/연산 실패 보고, 판정 경계)은 verifier.md·02 §4 소관이며 본 문서는 포인터만 둔다.

### §3.2 `configSchema` 물리 반영 대상 부재 (DP-V2 — Memory `recall.limit.max` 대응 절과의 차이)

module-manifest.md는 Advisor 결정 DP-V2로 `configSchema`를 **선언하지 않는다**(06 §3 판정 계약에 이 Provider가 소비하는 Config 의존 값이 없다). 따라서 본 문서에는 **물리 반영할 Config 값이 없다**.

- **정직한 차이 기록.** 자매 memory-binding.md §4.2는 `recall.limit.max`(기본 20)의 물리 반영(선언 위치 → override 물리 소스 → 읽히는 지점 → 적용 방식)을 확정했다. Verifier Manifest에는 대응 키가 없으므로 본 문서에 그 대응 절이 **존재하지 않는다** — 누락이 아니라 계약(module-manifest.md §5 DP-V2)의 정직한 반영이다.
- **경계(창설 금지).** `configSchema`에 의미(예: 판정 엄격 모드 `verify.strict`)를 부여해 물리 반영으로 끌어오지 않는다 — 06 §3.2-C 결정적 최종 판정 도출·§3.3 불변 규칙과 충돌하는 계약 창설이 된다. `verify.strict`는 Config 병합 규칙의 예시 키일 뿐이며(01 §8 예2·config-schema.md §6) 본 바인딩은 이를 Verifier 판정 의미로 바인딩하지 않는다. 실행 로더(형태 B) 도입 시에도 Manifest가 `configSchema`를 선언하지 않는 한 effective config 병합 대상이 아니며, 이 부재는 이식·형태 전환에도 불변이다(structure.md §7 C-1).

---

## §4. 검증 리포트 직렬화·저장 위치 확정 · 재작업 지시 전달 (done 4)

06 §4.1의 "검증 리포트(§3.2-A) 직렬화 — Markdown 리포트 파일 또는 구조화 파일. 검증 산출물 위치"와 "재작업 지시(§3.2-D) 전달" 두 행의 물리 실현을 확정한다. 계약(06 §3.2-A/D)과 그 인스턴스(verification-report.md·rework-instruction.md)는 § 포인터·문서명으로만 인용한다.

### §4.1 검증 리포트 직렬화·저장 위치 (정본 — 06 §4.1 검증 리포트 직렬화 행)

- **직렬화 형식.** 검증 리포트는 **구조화 Markdown 문서**로 직렬화되며, 06 §3.2-A의 6필드(`target`/`criteria_basis`/`items`/`final_verdict`/`verifier_scope`/`rework`)를 문서 절 구조로 담는다 — `§1 target` / `§2 criteria_basis` / `§3 items`(항목별 판정 표: `criterion`/`verdict`/`evidence`/`scope`/`verification_type` 열, 06 §3.2-B) / `§4 final_verdict` / `§5 verifier_scope` / `§6 rework`. 이 절 ↔ 필드 대응은 verification-report.md §6(V1 확정본 실사용 대응표)이 실증했고, 스키마 정본은 06 §3.2-A/B/C·verification-report.md다.
- **명명 관례·저장 위치.** 저장 위치 = `docs/`, 명명 관례 = `docs/v0.X-verification-report.md`(X = 대상 마일스톤 버전). 검증 산출물은 스캔·실측 결과 보고에 필요한 구체 토큰·물리 경로 인용을 정당하게 보유하는 **구조화 검증 산출물 문서**이며 은닉 백엔드가 아니다. 문서 머리에는 작성일·수행 주체·근거 정본·상태 라인을 둔다(docs 거버넌스 관례 동형). **산출물 파일 안에 이력 절을 두지 않는다** — 리포트의 개정 기록은 git 커밋이다(규범 = `docs/spec-versioning-policy.md` §3).
- **실증·미래 인스턴스.** 이 형식·명명·위치는 확정 실사용 인스턴스 2건(`uahf/docs/v0.3-verification-report.md@cd9247b`·`uahf/docs/v0.4-verification-report.md@cd9247b` — 각 CP2 독립 판정 산출물, 6필드 절 구조·Fail→재검증 Pass 사이클·rework 절 직렬화를 실사용)으로 실증된다. v0.5 개별 인스턴스는 미존재이며(§7) 판정·시연 시 이 관례대로 생성될 예정이다 — 본 문서는 미래 산출물의 실재를 주장하지 않고 시연 절차·픽스처 상세를 서술하지 않는다.

### §4.2 재작업 지시 직렬화·전달 (정본 — 06 §4.1 재작업 지시 전달 행)

- **직렬화.** 재작업 지시(06 §3.2-D 4필드: `violated_items`/`expected_state`/`revalidation_criteria`/`evidence_gap`, rework-instruction.md 인스턴스)는 검증 리포트의 `rework` 절(문서 §6)로 직렬화된다. `final_verdict`가 Fail 또는 Conditional일 때 필수로 채워지고 Pass면 "없음"이다(06 §3.2-A·§3.2-C, rework-instruction.md §3). 실사용 리포트 2건의 §6이 발행(Fail)→이행→재검증(Pass)에서 `rework`가 "없음"으로 전이하는 사이클을 실증했다.
- **전달·경계.** 전달은 Advisor/Loop가 Worker 서브에이전트에게 보내는 **재위임 메시지**로 실현된다(delegation-protocol.md §3.1, verification-checklist.md §7). 재작업 지시의 **전달·라우팅·전이 채널**은 03-loop·02 §4 소관이며(rework-instruction.md §5), 본 문서는 리포트 내 직렬화 표면과 물리 전달 채널만 바인딩한다 — 재작업 루프의 구동·재시도 한도·시점·전이는 정의하지 않는다(06 INV-9).

---

## §5. VT-1~VT-5 검사 도구 바인딩 (done 5)

criteria-catalog.md §5가 "검사 도구·구체 토큰의 물리 실현은 Adapter Binding 문서 소관(06 §4.1 검사 도구 바인딩 행·SP-3)"으로 미룬 지점을 확정한다. VT-1~VT-5(06 §3.2-E, criteria-catalog.md §2) 각각을 이 환경의 검사 도구에 바인딩한다.

| 검증 유형 (06 §3.2-E) | 판정 방법 (정본 요지) | 검사 도구 바인딩 (claude 환경) | 확정 실사용 실증 (docs/ 리포트) |
|---|---|---|---|
| **VT-1 산출물 존재 검증** | 지정 산출물이 실제로 존재·접근 가능한지 확인 | **파일 조회 도구**로 위임 output 지정 경로의 실재·접근을 실측(부재·결손 검출). 필요 시 크기·라인 수 실측. | v0.3 §1(산출물 8종 실재·byte 실측)·v0.4 §1(문서 9종 + 물리 데이터 21파일·index 21라인 실측). |
| **VT-2 완료 조건 대조 검증** | 각 완료 조건(done)을 산출물과 항목별 대조 | **파일 조회 도구**로 산출물을 **전문** 정독(표본 금지) + 위임 done 항목별 1:1 대조. | v0.3 §2·items #2~#5·v0.4 §2·items #2~#5·#20~#30. |
| **VT-3 규격 준수 검증** | 규격의 각 항목을 산출물과 대조 | **파일 조회 도구**로 규격(TEMPLATE DoD·대상 spec §7·상위 계약 §3.2 스키마)과 산출물을 **셀 단위** 대조. | v0.3 items #4·#9·#11·v0.4 items #5·#9·#10·#27·#28. |
| **VT-4 경계 검증** | 금지 요소를 전수 스캔(exhaustive scan), 검사 범위를 해당 경계 전 범위로 명시 | **텍스트 검색 도구**로 금지 요소 후보 집합 **전체**를 검사 범위 **전 범위**에 대해 전수 스캔. 단일 대리 지표(단일 토큰 검색) 하나로 대체하지 않는다(06 §3.2-E 주의·INV-4). 매치는 금지 토큰/정당 참조로 분류. | v0.4 §3.3(후보 5부류 전수 스캔·매치 분류표)·v0.3 §3.2(Core 경계 후보 부류 전수 스캔). |
| **VT-5 시연 검증** | 시연 시나리오를 실제로 재현하고 결과를 관측 | **명령 실행 도구**로 시연 시나리오 재현·독립 재계산 + **파일 조회 도구**로 산출물 자체 재관측(관측 주장을 신뢰하지 않고 재판정). | v0.4 §3.2(물리 실데이터 직접 재관측·재계산)·v0.3 §3.3(시연 재현·도출 재계산). |

- **금지 요소 후보 토큰의 운용 목록 = docs/verification-checklist.md §7 소유.** VT-4 전수 스캔 대상 토큰 목록(특정 AI 이름·모델명·제품 기능명·`claude-*` 패턴 등)은 checklist §7이 이 프로젝트 표면에서 소유한다(게이트에서 무엇을 검색하는가). 본 문서는 그 목록을 복제하지 않고 소관 포인터로 참조하며, 확정하는 것은 **VT ↔ 검사 도구의 물리 바인딩**이다.
- **verification-checklist.md §7과의 소유 관계(재정의 0).** checklist §7 = Advisor 검증 게이트(게이트 C)에서 도구를 **어떻게 쓰는가**의 **운용 지침** / 본 문서 §5 = 06 §4.1 검사 도구 바인딩 행의 **물리 실현 정본**(VT별 도구 배선의 확정 자리). 둘은 같은 도구·같은 전수 스캔 원칙으로 **정합**하며, 재정의가 아니라 정본(물리 바인딩)/운용(게이트 사용법)의 소유 구분이다.
- **경계.** 검사 도구는 이식 교체 지점 SP-3이다(§6) — 대상 환경 도구로 교체되며, VT-1~VT-5 유형·판정 방법·충족 조건·전수 스캔 규칙(06 §3.2-E·INV-4, criteria-catalog.md §2·§3)은 유지된다. 무인 도구 배선은 형태 B/Loop 소관이며 본 문서는 도구 표면 바인딩만 확정한다.

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
| SP-6 | Verifier 실행 모델 지정 → 02 §4 소관. 06은 참조만 한다 | §2 #7 | 02 §4 실행 모델 바인딩 영역(세션 상속 / 특정 실행 모델 지정 중 어느 쪽이든 02 §4가 정한다). 현재 실물 값은 §7 실측. | §3.2-A 역할 경계·메시지 필수 필드(02 §3). 06·본 문서는 지정하지 않고 참조만(02 §4.2 "유지되는 것"). |

- "유지되는 것" 열의 계약(검증 리포트·판정 값·최종 판정 도출·재작업 지시 4필드·검증 유형·거짓 완료 보고 검출 계약·§3.3 Invariants)은 다른 AI·환경으로 이식해도 바뀌지 않는다(06 §4.2 말미 유지 목록 = structure.md §7 C-1). V1~V5 확정본이 그 계약의 인스턴스이며 이식 시에도 계약 요소는 불변이다. 이 목록의 Adapter Interface 정식화는 specs/11-adapters.md 소관이며 본 문서는 선취하지 않는다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 7 — A5/L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 본 문서의 "실재/존재" 서술을 파일 시스템과 직접 대조한다. **byte 스냅샷은 두지 않는다** — 자매 문서·진입점·5문서·리포트의 크기는 개정마다 변하는 drift이며(종전 판의 byte 5종 이상을 2026-07-26 슬림화에서 제거), 남기는 것은 재실측으로 참·거짓이 갈리는 불변 주장뿐이다.

| 대상 | 실측 판정 (재실측 대상) |
|---|---|
| `framework/adapters/claude/` 경계 · 자매 runtime-binding.md·memory-binding.md | 실재. byte 불기재. |
| `.claude/agents/verifier.md` (§2 #1 진입점) | 실재. **정정(2026-07-26): front-matter가 `model: opus`(+`effort: high`)를 지정한다** — 종전 판의 "실행 모델 미지정 = 세션 상속(`model` 키 부재)" 서술은 2026-07-06 시점 실측이며 현재는 사실이 아니다. 실행 모델 지정 권한이 02 §4 소관이라는 규범(§2 #7·SP-6)은 무변경이고 바뀐 것은 실물 값뿐이다. `uaf-verified: .claude/agents/verifier.md front-matter 직접 열람 + model 선언 행 계수(grep -c)` |
| `framework/verifier/` 5문서 (§2 #2 구현 디렉터리) | 실재 — verification-report·module-manifest·verifier-protocol·rework-instruction·criteria-catalog **5건 전건**이며 실행 코드는 0이다(계약 문서만). `uaf-verified: framework/verifier/ 디렉터리 전수 열거` |
| 확정 실사용 검증 리포트 2건 (§4.1 직렬화 실증) | 아카이브 — `uahf/docs/v0.3-verification-report.md@cd9247b`·`uahf/docs/v0.4-verification-report.md@cd9247b`. 산출물 수명 정책으로 작업 트리에서 제거되었고 열람은 `git show <앵커>:<경로>`다. |
| v0.5 검증 리포트 인스턴스 (§4.1 미래 인스턴스) | **미존재** — `docs/v0.5-*` 열거 0건(2026-07-26 재확인). 미래 산출물로 실재 불주장. |
| docs/verification-checklist.md (§5 운용 지침 소유자) | 실재 — 리포지토리 루트 `docs/` 이하. §5의 소관 포인터가 유효하다. |
| 검사 도구 표면 (§5 — 파일 조회·텍스트 검색·명령 실행) | 실재 — 실사용 리포트 2건이 실증. |
| Verifier `configSchema` 물리 반영 대상 (§3.2) | **부재** — module-manifest.md §2·§5에서 `configSchema` "선언하지 않음(DP-V2)" 확인. 물리 반영할 Config 값 0. |
| Verify 연산 실행 진입점·실행 로더 (형태 B) | 미도입 — Bootstrap 상태(형태 A). |

- **핵심 구분.** 본 문서가 확정한 검증 리포트 직렬화·명명·저장 위치와 VT별 검사 도구 바인딩은 **정본**이며, 확정 실사용 리포트 2건이 그 관례를 실증한다. 개별 리포트 인스턴스의 생성 주체는 판정·시연 Task이고 본 문서는 구조·형식·관례·바인딩의 정본만 소유한다. 실재를 주장하는 행은 전건 파일 시스템 직접 실측 후에만 기입한다(A5/L-07 재발 방지).

---

## §8. 정본 경계·격리·계약 소유 (self-note — 1줄 + 소유 지도)

- **재정의 0·창설 0·격리 선언은 §0이 1벌로 소유한다.** 이 절은 그 선언을 반복하지 않고 계약 소유 지도만 둔다.
- **계약 소유 지도.** 검증 리포트 스키마 = verification-report.md / 06 §3.2-A/B/C · Manifest 필드·`entrypoint`·`configSchema` 결정(DP-V2) = module-manifest.md / 01 §3.2-A · Verify 연산 절차 = verifier-protocol.md / 06 §3.1 · 재작업 지시 포맷 = rework-instruction.md / 06 §3.2-D · 검증 유형·기준 부류 = criteria-catalog.md / 06 §3.2-E·§3.2-A · 전달·전이 채널 = 03-loop·02 §4 · 실행 모델 = 02 §4. 본 문서가 소유하는 정본은 **직렬화 형식·명명·저장 위치(§4)·진입점 물리 해소(§3)·검사 도구 배선(§5)·회수/전달 물리 채널(§2)** 뿐이며, docs/verification-checklist.md §7은 게이트 운용 지침으로 §5와 정합한다.
- **작성 경계 이력(포인터).** 초판(2026-07-06, Task V6)의 동시 작성 시연 절차서 불인용(07 R2)·1파일 생성 범위(07 R4)·미래 산출물 실재 불주장(L-07) 감사 흔적은 git 이력(초판·개정 커밋)에 보존되어 있다. `uaf-allow-legacy: 초판 감사 흔적은 git 이력에 보존, 본문은 포인터 1줄`

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-VB-1 (checklist §7 상호 참조 — 비차단).** docs/verification-checklist.md §7은 검사 도구를 이미 바인딩하나, 06 §4.1 검사 도구 바인딩 행의 **물리 실현 정본이 본 문서 §5임**을 § 포인터로 가리키지 않는다(checklist §7은 06 §4.1·SP-3을 인용). 두 문서는 정합하며 정본/운용 소유 관계는 §5에 명시했으므로 계약 갭은 아니다 — checklist §7에 상호 참조를 추가할지는 Advisor 판단 대상이다(본 문서 소유 경계 밖이므로 수정하지 않았다).
- **OQ-VB-2 (형태 B 경계 분할 — 비차단).** Verify 실행 코드(형태 B)가 `framework/verifier/`와 `framework/adapters/claude/` 사이 어디에 분할 배치되는지는 형태 B 설계 시 확정 대상이다(§3.1, structure.md §4 규칙 4 defer). 형태 A에서는 규약 실현이므로 이 분할이 필요하지 않고, 계약(06 §3) 변경이 아니므로 비차단이다.

---

## §10. 요약 (1줄)

- 이 문서 = 06 §4.1(Verifier 바인딩 표 7행)의 물리 실현 매핑이며, 검증 리포트 직렬화·명명·저장 위치(구조화 Markdown·`docs/v0.X-verification-report.md`)와 VT-1~VT-5 검사 도구 바인딩이 본 문서 소유 정본이다 — 절 지도는 §1, 정본 경계는 §0, 상태는 §7이 소유하며 여기서 재서술하지 않는다.
