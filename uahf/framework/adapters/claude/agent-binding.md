# framework/adapters/claude/agent-binding — Claude Code Agent Adapter 바인딩

작성일: 2026-07-06
상태: v0.9 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본 (계약은 § 포인터로만 인용 — 재정의 0 선언은 §0 1곳):

- specs/02-agent.md — §3.1 공통 의무 O1~O5 · §3.2-A 역할 경계 · §3.2-B/C/D 위임·완료·실패 보고 메시지 · §3.3 INV-1~INV-8 · §4.1 Claude Code Binding 표 · §4.2 이식 교체 지점 SP-1~SP-5.
- framework/adapters/claude/adapter-conformance.md §2(BP-7~11 커버리지 매트릭스)·§4(정식화 배정표 — agent-binding.md(T3)에 BP-7~11·02 §4.1·§4.2 배정). **본 문서는 그 배정의 이행이다.**
- BP-7~11 현행 분산 실현의 소스 — runtime-binding.md §2 #2·§3.2(Agent Module 진입점·Register/Resolve) · verifier-binding.md §2·§3.1 · loop-binding.md §2·§5.1(역할 실행 물리 채널) · docs/delegation-protocol.md §3(위임 = 디스패치 §3.1 · 보고 = 최종 응답 §3.2 · 병렬 Wave §3.3 · 반환·에스컬레이션 §3.4).
- 실물 실측 대상(참조·실측만, 무수정) — `.claude/AGENT.md` · `.claude/CLAUDE.md` · `.claude/agents/{advisor,planner,worker,verifier}.md`.
- framework/core/structure.md §2·§5(4경계 배치·Adapter 경계 = 격리 지점) · specs/00-glossary.md(§3.2-E 역할·§3.2-A Layer 스택, 용어 신설 0) · ROADMAP.md v0.2·v0.9.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다 — Core 계약을 특정 실행 환경·AI·직렬화 형식·실행 모델에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 02 INV-7, 01 §3.2-E 규칙 3), 그 구체 토큰의 사용이 허용된다(C-3 비적용 — 자매 바인딩 §0 동형). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/02-agent.md §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며 계약 요소(공통 의무·역할 경계·메시지 필드·Invariants·바인딩 지점)를 **재정의·확장하지 않는다** — 계약은 § 포인터로만 인용한다. **이 재정의 0 선언은 문서 전체에 대해 여기 1곳에서만 선언되며**, 이하 각 절은 정본 §만 지목한다. 02 §4.1이 "각 spec §4에 분산 정의된 바인딩"으로 둔 Agent Component 물리 실현이 실재하는 자리이자, adapter-conformance.md §2·§4가 BP-7~11 통합·정식화로 배정한 지점의 이행이다.
- **격리 지점(C-3 비적용).** Core 경계·Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 하지만(structure.md §5 C-3 확장, 02 INV-7), 이 문서는 그 **반대편**이다 — 진입점 경로(`.claude/agents/…`)·규약 파일·front-matter·`model: opus`·서브에이전트·세션/턴 토큰이 허용된다. **단 02 §3 문면을 바꿀 권한은 아니다.**
- **창설 금지.** 02 §4.1 표를 넘어서는 새 바인딩 계약·새 역할·새 메시지 필드·새 Invariant·새 SP·새 실행 모델 의미를 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 4역할은 정식 실행 Module이 아니라 규약 문서(02·`.claude/agents/` 4종)와 관행(Advisor가 서브에이전트 위임으로 역할을 구동)으로 실현된다(형태 A — Glossary J-13·delegation-protocol.md §0·runtime-binding.md §0). 따라서 매핑은 **실재 표면**(4역할 정의·규약 2문서·실행 모델 지정)·**규약 수행**(위임·보고·컨텍스트 전달)·**형태 B 지점**(무인 자동 오케스트레이션·실행 로더)을 구분한다. `형태 A/B`는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템·front-matter 확인 후에만 기입하며, §2 "실재 여부" 열과 §6 표는 **재실측으로 참·거짓이 갈리는 형태**로만 쓴다(byte·계수·일자 스냅샷 불기재 — drift). **정정(2026-07-26): 정의 파일 본문의 `DP-E8` 문자열 명시는 0건이다** — `model: opus` 값 3건과 advisor의 세션 상속은 그대로 실재하나, 결정 라벨의 기록 소유처는 본 문서 §3이다(§6). `uaf-verified: .claude/agents/*.md front-matter 4파일 직접 열람 + grep -l DP-E8 → 매치 0`
- 용어는 specs/00-glossary.md 정본만 사용한다(4역할 = §3.2-E · Agent Layer = §3.2-A). `형태 A/B`는 structure.md 서술 라벨이고 `DP-E8`은 본 문서가 기록하는 Advisor 결정 라벨이다(§3). 새 용어 신설 0.

---

## §1. 목적

이 문서는 02 §4.1(Agent Claude Code Binding)을 이 환경의 구체 물리 실현으로 매핑하고, adapter-conformance.md §2의 BP-7~11 현행 분산 실현을 한 문서로 통합·정식화한다(§4 배정 이행). 절 지도 — §2 02 §4.1 전 항목 물리 실현 + BP-7~11 대응 · §3 실행 모델 실측 반영(DP-E8 기록) · §4 위임·보고·컨텍스트 물리 채널 · §5 02 §4.2 SP-1~SP-5 대응 · §6 실측 대조.

형태 A → 형태 B 전환 시에도 Core Contract(02 §3) 변경은 0이며(structure.md §7 C-1), §5의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 02 §4.1 바인딩 표 물리 실현 · BP-7~11 대응 (done 1)

02 §4.1 Claude Code Binding 표의 **전 항목**을 물리 표면으로 매핑한다. "02 §4.1 바인딩 (정본 인용)" 열은 정본 표현을 그대로 인용하고, "물리 실현" 열이 경로·형식·채널을(상세는 §3·§4 소유 — 여기서 재서술하지 않는다), "실재 여부" 열이 물리 실재/형태 A/형태 B를, "대응 BP" 열이 adapter-conformance.md §2 커버리지 매트릭스와의 대응을 명시한다(실측 §6).

| # | 02 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 | 대응 BP (adapter-conformance.md §2) |
|---|---|---|---|---|
| 1 | Agent 정의 파일 — 각 역할은 `.claude/agents/*.md`로 정의된다: advisor.md, planner.md, worker.md, verifier.md (ROADMAP v0.2 산출물). | 4역할 Agent Module 정의 파일 = `.claude/agents/{advisor,planner,worker,verifier}.md`. Markdown 본문 + YAML front-matter 직렬화(runtime-binding.md §2 #1 동형). 진입점 내부 역할 계약(위임 입력 in → 보고 out·역할 경계)은 각 정의 파일 + 02 §3.2-A 소관. 활성화 = 위임 시 해당 정의 파일 로딩(Resolve — §4 말미). | 4파일 실재(§6). 무인 자동 로더(형태 B) 미도입. | **BP-7** (4역할 정의 제공) |
| 2 | 공통 규약 바인딩 — `.claude/AGENT.md`가 모든 Agent 정의의 상위 규약이다. `.claude/CLAUDE.md`가 Advisor 역할을 프로젝트 진입점에 바인딩한다. | 상위 규약 = `.claude/AGENT.md` · 진입점 주입 = `.claude/CLAUDE.md`(Advisor를 주 세션 진입점에 바인딩). 각 정의 파일은 머리에서 상위 규약을 `.claude/AGENT.md`로, 계약 정본을 02로 지시한다(INV-1). | 2파일 실재(§6). | **BP-8** (공통 규약·시스템 프롬프트·진입점 주입) |
| 3 | 실행 모델 바인딩 — v0.x에서 Worker의 기본 실행 모델은 Opus로 지정한다(`.claude/CLAUDE.md` "Worker(Opus)"). 다른 역할의 모델 지정도 이 바인딩 영역에 속한다. | 역할별 실행 모델·엔진을 정의 파일 front-matter `model` 키로 바인딩(Module 스코프 Config — runtime-binding.md §3.3 동형). 실측 값·DP-E8 기록은 §3. | 4역할 지정 실재(§3·§6). | **BP-9** (역할 실행 모델·엔진 지정) |
| 4 | 위임 메커니즘 — Advisor는 서브에이전트 위임으로 §3.2-B 위임 메시지를 Worker/Planner/Verifier에게 전달한다. | 위임 = **서브에이전트 디스패치** 채널로 02 §3.2-B 위임 메시지 8필드 전달(delegation-protocol.md §3.1). 병렬 동시 위임·재위임 라우팅도 이 채널. 상세 = §4.1. | 규약 실현(형태 A). 무인 자동 디스패치(형태 B) 미도입. | **BP-10** (위임 메시지 전달·오케스트레이션 채널) |
| 5 | 보고 회수 — §3.2-C 완료 보고와 §3.2-D 실패 보고는 서브에이전트의 최종 응답으로 회수된다. | 보고 회수 = 서브에이전트 **최종 응답** 채널로 완료 보고 5필드 / 실패 보고 5필드 회수(delegation-protocol.md §3.2). 반환·에스컬레이션도 이 채널. Advisor는 회수한 보고를 그대로 신뢰하지 않는다(02 §3.2-A·INV-4). 상세 = §4.2. | 규약 실현(형태 A). 무인 자동 회수(형태 B) 미도입. | **BP-11** (완료 보고·실패 보고 반환 채널) |
| 6 | 컨텍스트 전달 — 위임 메시지의 context 필드는 읽어야 할 파일 경로 목록으로 전달된다. | context 필드(02 §3.2-B) = 착수 전 정독할 파일 경로 목록(상위 규약·Architecture·관련 spec·Memory 회수 범위). 병렬 집합에서는 확정 문서만 담는다(delegation-protocol.md §2.1·07 R2). 상세 = §4.3. | 규약 실현(형태 A). | **BP-10** 부속 (위임 메시지 컨텍스트 전달) |

주:

- 위 6행은 02 §4.1 표의 전 항목이며, "물리 실현"은 정본 표현을 이 환경의 구체 경로·형식·채널로 좁힌 것이다(새 바인딩 계약 창설 0 — §0).
- **BP-7~11 통합·정식화(무결성).** adapter-conformance.md §2가 BP-7~11을 "현행 분산 실현(02 §4.1 + `.claude/` 실물 + runtime-binding.md §2 #2 + delegation-protocol.md §3)"으로 매핑하고 §4가 본 문서로 배정했다 — BP-7(행 1)·BP-8(행 2)·BP-9(행 3)·BP-10(행 4·6)·BP-11(행 5)이 그 이행이며 **새 계약 창설이 아니라 분산 실현의 통합**이다(실물 실재 = §6, 후속 격리 갱신 = OQ-AB-1).
- **형태 구분 · 4역할 = Agent Module.** 행 1~3은 물리 실재, 행 4~6은 Bootstrap의 **규약 실현(형태 A)**이고 무인 자동 오케스트레이션·실행 로더는 형태 B다. 4역할은 서브에이전트로 디스패치되는 Agent Module이므로 위임·보고·재위임이 디스패치/최종 응답 채널로 실현된다 — Memory(단일 Port 소비)와 구별된다(§4).

---

## §3. 실행 모델 바인딩 실측 반영 (done 1 상세 — DP-E8 기록)

02 §4.1 실행 모델 바인딩 행(BP-9)의 역할별 지정을 front-matter 직접 실측으로 반영한다. **지정 값은 이 Adapter 경계가 소유하는 물리 실현이고, 그 지정의 의미·판정 계약은 02 §4가 소유한다.** 실행 모델 지정은 이식 교체 지점 SP-3이다(§5).

| 역할 | 정의 파일 | 실행 모델 지정 (실측 — front-matter `model` 키) | 근거 |
|---|---|---|---|
| Worker | `.claude/agents/worker.md` | `model: opus` (실측 — front-matter `model: opus`) | 02 §4.1 기저 바인딩 — "Worker의 기본 실행 모델은 Opus"(`.claude/CLAUDE.md` "Worker(Opus)"). |
| Planner | `.claude/agents/planner.md` | `model: opus` (실측) | **DP-E8**(§ 아래) — 종전 미지정(세션 상속)에서 Opus 명시로 전환. |
| Verifier | `.claude/agents/verifier.md` | `model: opus` (실측) | **DP-E8** + 06 §4.2 SP-6(실행 모델 지정은 02 §4 소관) — 종전 미지정에서 Opus 명시로 전환. |
| Advisor | `.claude/agents/advisor.md` | **미지정 — 세션 상속** (실측 — front-matter `model` 라인 부재) | 02 §4.1 실행 모델 바인딩 영역(Advisor 결정) — 주 세션 모델을 상속하므로 `model` 라인을 두지 않는다. |

**DP-E8 기록 (Advisor 결정 — 본 문서는 기록만).** planner.md·verifier.md의 `model: opus`는 Advisor 결정 **DP-E8**(사용자 결정 2026-07-06)이다 — 종전 미지정(세션 상속)에서 Opus 명시로 전환했고, 사유는 Fable 사용 한도 절약이며 **v1.0 완료까지 유지하는 영구 관행**이다. 결정 주체는 Advisor이고(02 §3.2-A·INV-3), 이 결정은 02 §4.1 실행 모델 바인딩 영역 안의 인스턴스로 02 §3 계약을 무변경으로 유지한다. **결정 라벨의 기록 소유처는 이 절이다** — 정의 파일 본문에 `DP-E8` 문자열은 현재 0건이다(§6 정정).

- **같은 표면의 추가 키.** front-matter에는 `model` 외에 `effort` 키가 있다(planner `medium`·worker `medium`·verifier `high`·advisor 부재 — §6). Module 스코프 Config 표면의 값이며 02 §3 계약 요소가 아니므로 존재만 기록한다.
- **경계.** 역할별 실행 모델 지정은 SP-3(§5)으로 교체되며, 02 §3.2-A 역할 경계·메시지 필수 필드·§3.3 Invariants는 유지된다.

---

## §4. 위임·보고·컨텍스트 물리 채널 (done 1 상세)

02 §4.1 위임 메커니즘(BP-10)·보고 회수(BP-11)·컨텍스트 전달 행의 물리 채널이다. **채널 상세는 delegation-protocol.md §3(운용)·02 §4.1(정본)이 소유하고, 메시지 필드는 02 §3.2-B/C/D가 소유한다** — 본 절은 물리 실현만 확정한다.

### §4.1 위임 디스패치 (BP-10)

- **채널.** Advisor는 **서브에이전트 디스패치**로 02 §3.2-B 위임 메시지 8필드(from/to/task/input/output/done/context/constraints)를 Worker/Planner/Verifier에게 전달한다(delegation-protocol.md §3.1). **필수 필드(input·output·done·context) 누락 위임은 발신하지 않으며, 누락 시 수임 Agent가 착수 전 반환·질의한다**(02 INV-6, delegation-protocol.md §2.4).
- **병렬 디스패치.** 한 병렬 집합의 여러 Task를 **동시 위임**으로 전달한다(delegation-protocol.md §3.3, 07 R1~R4) — 각 Worker는 소유 경계 밖 파일·계약을 수정하지 않고(R4) 동시 작성 산출물을 추측·인용하지 않는다(R2).
- **재위임.** CP2 판정이 Fail/Conditional이면 재작업 지시(06 §3.2-D)가 재위임 메시지로 Worker 서브에이전트에 라우팅된다(loop-binding.md §5.1·verifier-binding.md §4.2). 라우팅·전이 채널 정본은 03·02 §4다.

### §4.2 보고 회수 (BP-11)

- **채널.** 완료 보고 5필드(artifacts/self_check/failures/open_questions/verify_basis, 02 §3.2-C)와 실패 보고 5필드(reason/repro/attempted/lesson_candidate/blocking, 02 §3.2-D)는 서브에이전트 **최종 응답**으로 회수된다(delegation-protocol.md §3.2).
- **독립 검증 전제.** Advisor는 회수한 완료 보고를 **그대로 신뢰하지 않고** 산출물을 정독해 독립 재검증한다(02 §3.2-A·INV-4, `.claude/CLAUDE.md`) — 완료 보고는 Verify 통과(CP2 PASS) 뒤에만 유효하다.
- **반환·에스컬레이션.** 착수 불능·차단은 실패 보고(blocking=차단)로, 비차단 확인 필요는 완료 보고 open_questions로 같은 채널을 통해 Advisor에게 회수된다(delegation-protocol.md §3.4, 02 O4).

### §4.3 컨텍스트 전달

- **채널.** context 필드(02 §3.2-B)는 착수 전 정독할 **파일 경로 목록**(상위 규약·Architecture·관련 spec·Memory 회수 범위)으로 전달된다(delegation-protocol.md §2.1).
- **병렬 경계(R2).** 병렬 집합에서는 확정(Frozen/실재) 문서만 담고 동시 작성 산출물은 담지 않으며, 필요하면 인용하지 않고 R3로 Advisor에게 에스컬레이션한다(delegation-protocol.md §2.5).

- **Register/Resolve 정합.** 4역할의 Register는 정의 파일 배치로 규약 실현되고(형태 A), Resolve는 위임 시 해당 역할의 활성 정의 파일이 로딩되는 것이다 — 4역할은 서브에이전트로 디스패치되는 **Agent Module**이므로 Resolve가 Port 소비가 아니라 디스패치로 실현된다(Memory Cross-cutting Service의 단일 Port 경로와 구별; runtime-binding.md §3.2·verifier-binding.md §3.1 동형). 이 경로는 SP-1·SP-4·SP-5에 대응한다(§5).

---

## §5. 02 §4.2 이식 교체 지점 SP-1~SP-5 대응 (done 1)

02 §4.2 이식 교체 지점 SP-1~SP-5 각각의 대응 절과 "교체되는 것 / 유지되는 것"이다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인한다.

| # (02 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경(claude) 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Agent 정의 파일 위치·포맷(`.claude/agents/*.md`) → 대상 환경의 Agent 정의 메커니즘 | §2 행 1, §4(Register/Resolve) | `.claude/agents/{advisor,planner,worker,verifier}.md` 정의 파일 위치·포맷(Markdown + front-matter), 서브에이전트 위임 시 로딩(Resolve). | §3.2-A 역할 경계, 진입점 내부 역할 계약(02 §3.2-A), Provider 등록·해소 계약(01 §3.1-A). |
| SP-2 | 상위 규약 바인딩 파일(`.claude/AGENT.md`, `.claude/CLAUDE.md`) → 대상 환경의 규약·시스템 프롬프트 주입 방식 | §2 행 2 | `.claude/AGENT.md`(상위 규약)·`.claude/CLAUDE.md`(Advisor 진입점 바인딩)의 위치·포맷·주입 방식. | 공통 의무(O1~O5)·역할 경계(§3.2-A)·Invariants(§3.3). AGENT.md가 규정하는 공통 규약 자체. |
| SP-3 | 실행 모델 지정(Worker = Opus 등) → 대상 환경의 모델·엔진 | §2 행 3, §3 | 역할별 `model` 지정 — worker/planner/verifier `model: opus`(DP-E8 포함)·advisor 세션 상속. | §3.2-A 역할 경계·§3.2-B/C/D 메시지 필수 필드(02 §4.2 "유지되는 것"). 모델 값 자체는 환경 표면이며 계약이 아니다. |
| SP-4 | 위임 메커니즘(서브에이전트 위임) → 대상 환경의 Agent 호출·오케스트레이션 API | §2 행 4·6, §4.1 | 서브에이전트 위임(디스패치)·병렬 동시 위임·재위임 라우팅(delegation-protocol.md §3.1·§3.3). | 위임 메시지 8필드(§3.2-B)·INV-6(필수 필드 완전성). 병렬 규칙 R1~R4(07 §3.2-C). |
| SP-5 | 보고 회수 방식(서브에이전트 최종 응답) → 대상 환경의 결과 반환 채널 | §2 행 5, §4.2 | 서브에이전트 최종 응답으로 완료/실패 보고·반환·에스컬레이션 회수(delegation-protocol.md §3.2·§3.4). | 완료 보고 5필드(§3.2-C)·실패 보고 5필드(§3.2-D)·INV-4(Verify 통과 후 완료 보고)·INV-5(실패 은폐 금지). |

- "유지되는 것" 열의 계약(역할 경계·공통 의무·메시지 필수 필드·Invariants)은 다른 AI·환경으로 이식해도 바뀌지 않는다 — 02 §4.2 말미 유지 목록의 이식 불변성이며 structure.md §7 C-1과 정합한다. 이 목록의 정식화는 specs/11-adapters.md가 Adapter Interface(BP-7~11)로 담당하고 본 문서는 선취하지 않는다(창설 금지, §0).

---

## §6. 상태 서술 실측 대조 (L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 "실재/존재/부재" 서술을 파일 시스템·front-matter와 직접 대조한다. **일자 박힌 계수·byte 스냅샷은 두지 않는다**(drift — 종전 판의 Frozen specs 계수·형제 Task 불인용 스캔 행 제거; 감사 흔적은 §9 초판 행에 보존). 남기는 것은 재실측으로 참·거짓이 갈리는 주장뿐이다.

| 대상 | 실측 판정 (재실측 대상) |
|---|---|
| `.claude/agents/` 4역할 정의 파일 (§2 행 1, BP-7) | 실재 — advisor.md·planner.md·worker.md·verifier.md. |
| `.claude/AGENT.md`·`.claude/CLAUDE.md` (§2 행 2, BP-8) | 실재 — 2파일. `.claude/CLAUDE.md` 머리 "너는 메인 Advisor다"·"Worker(Opus)에게 위임" 확인. |
| worker/planner/verifier `model: opus` (§3, BP-9) | 실재 — 3파일 front-matter `model: opus`. **정정: 정의 파일 본문의 `DP-E8` 문자열 명시는 현재 0건이다**(종전 판은 planner·verifier 머리에 명시가 있다고 기록). 결정 기록의 소유처는 본 문서 §3이다. `uaf-verified: grep -l DP-E8 .claude/agents/*.md → 매치 0` |
| advisor.md 실행 모델 (§3) | **미지정 — 세션 상속.** front-matter `model` 라인 부재 + 본문 "실행 모델은 미지정이다 — 주 세션 모델을 상속한다" 확인. |
| front-matter `effort` 키 (§3 주) | 실재 — planner `medium`·worker `medium`·verifier `high`(advisor 부재). Module 스코프 Config 표면의 추가 키이며 02 §3 계약 요소가 아니다. |
| 자매 바인딩 문서 (§0·§2 관례 인용) | 실재 — runtime·verifier·loop-binding.md·adapter-conformance.md. byte 불기재. |
| `docs/delegation-protocol.md` (§4 물리 채널 소스) | 실재 — §3(물리 채널) 확인. |

- **핵심 구분.** 실재를 주장하는 행은 파일 시스템 직접 실측 후에만 기입한다 — 미존재를 실재로, 미래 산출물을 현재 실재로 쓰지 않는다(A5/L-07). BP-7~11 분산 실현 실물(4역할 정의·규약 2문서·실행 모델 지정)이 실측으로 확인되어 §2·§3 매핑의 근거가 실재한다.

---

## §7. 정본 경계·격리·계약 소유 (self-note)

- **계약 소유 지도(포인터).** 공통 의무·역할 경계·메시지 필드·Invariants = 02 §3 · 바인딩 지점 = 02 §4.1 · 이식 교체 지점 = 02 §4.2 · 위임/보고 운용 채널 = docs/delegation-protocol.md §3. 본 문서 소유는 그 물리 실현뿐이며(재정의 0 선언 = §0 1곳), BP-7~11 통합·정식화는 분산 실현을 한 문서로 모은 것이지 새 BP·새 계약의 창설이 아니다. Frozen specs(02·01·06·13)를 수정하지 않았고, DP-E8(§3)은 02 §4.1 영역 안의 결정 기록으로 02 §3 문면을 바꾸지 않는다. 환경 토큰의 격리 허용 지점도 이 문서다(structure.md §5 C-3, 02 INV-7).
- **판정 성격.** 물리 실현 매핑이며 독립 판정(CP2 — Verifier)·최종 승인(CP3 — Advisor)이 뒤따른다(02 §3.2-A). 자기 점검(CP1)을 최종 승인으로 삼지 않는다.
- **작성 경계 이력(포인터).** 초판(2026-07-06, Task T3)의 형제 Task(PS2) 불인용(07 R2)·인용 정본 목록·2파일 생성 범위(07 R4) 감사 흔적은 git 이력(초판 커밋)에 보존되어 있다. `uaf-allow-legacy: 초판 감사 흔적은 git 이력에 보존, 본문은 포인터 1줄`

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-AB-1 (adapter-conformance.md §2 커버리지 후속 격리 갱신 — 비차단).** 본 문서 생성으로 BP-7~11 통합·정식화 배정이 이행되었으므로, adapter-conformance.md §2 BP-7~11 행의 실현 지점을 본 문서 § 포인터로 정합화하는 격리 갱신(§4·OQ-AC-1이 예고한 T15)이 남아 있다. 커버리지·verdict 변경이 아니므로 비차단이며, 소유 경계상 본 문서는 그 파일을 수정하지 않는다.
- **OQ-AB-2 (실행 모델 실측 서술 후속 정합 — 비차단).** DP-E8은 v1.0까지의 영구 관행이다(§3). 관행 만료·변경 시 §3·§6의 실행 모델 서술을 재실측·정합화해야 한다 — 결정 변경 시점의 격리 갱신 사안으로 비차단이다.

---

## §10. 요약 (1줄)

- 이 문서 = 02 §4.1(Agent 바인딩 표 전 항목)의 물리 실현 매핑 + BP-7~11 분산 실현의 통합·정식화 — 절 지도는 §1, 정본 경계는 §0, 실행 모델 실측은 §3, 채널은 §4, 실측 대조는 §6이 소유하며 여기서 재서술하지 않는다.
