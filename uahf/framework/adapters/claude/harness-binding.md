# framework/adapters/claude/harness-binding — Claude Code Harness Adapter 바인딩

작성일: 2026-07-06
상태: v0.9 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/13-harness.md §4.1 — Claude Code Binding 조합 표(7행: 상위 규약 문서·Agent 역할 정의 4종·위임/보고 프로토콜·검증 게이트·작업 추적·실행 모델 지정·호스트 프로세스). 본 문서가 물리 실현으로 인스턴스화하는 조합 바인딩 표의 정본.
- specs/13-harness.md §3.2-A — 최소 구성 집합(5개 필수 요소)·소유·근거. 본 문서가 물리 실물로 대조하는 최소 구성의 정본.
- specs/13-harness.md §3.2-B — Harness 상태(Bootstrap/Formal)·전이 조건 4개. 본 문서는 이 전이 조건의 **판정을 수행하지 않는다**(§5, T11 소관). § 포인터로만 인용한다.
- specs/13-harness.md §4.2 — 이식 교체 지점 1~6. 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/13-harness.md §3 서두·§3.3(H-INV-1~H-INV-8) — Harness는 02·01의 계약을 재정의하지 않고 최소 부분집합으로 조합하며 조합 전체의 무결성 규칙만 소유한다. 본 문서는 **조합 지점만** 소유하고 상세 계약은 02·01·06 § 포인터로 참조한다(재정의 0).
- specs/02-agent.md §3·§4.1 — 역할 경계(§3.2-A)·위임/완료/실패 보고 메시지(§3.2-B/C/D)·Claude Code Binding. 최소 구성 요소(상위 규약·역할 4종·위임/보고·실행 모델)의 상세 정본. § 포인터로만 참조.
- specs/01-runtime.md §4.1 — 호스트 프로세스(세션/턴 = Bootstrap~Serve~Shutdown 실행 컨테이너) 상세 정본. § 포인터로만 참조.
- specs/06-verifier.md §4.1 — 검증 게이트(독립 판정 CP2) 상세 정본. § 포인터로만 참조.
- framework/adapters/claude/agent-binding.md (Task T3 동반 산출) — Agent Component의 Claude 물리 실현(02 §4.1 바인딩 표 6행·SP-1~SP-5). 본 문서 §2 조합 표의 상위 규약·역할 4종·위임/보고·실행 모델 행은 이 문서의 실현을 **조합 참조**한다(재정의 0).
- framework/adapters/claude/runtime-binding.md (v0.3 Baseline) §2 #10·§3.4 — 세션/턴 호스트 프로세스(Bootstrap~Serve~Shutdown 실행 컨테이너)의 물리 실현. 본 문서 §2 호스트 프로세스 행은 이 문서의 실현을 조합 참조한다. framework/adapters/claude/verifier-binding.md (v0.5 Baseline)·loop-binding.md (v0.7 Baseline) — 검증 게이트·작업 추적(loop-data/·검증 리포트) 물리 실현·자매 바인딩 관례 표본.
- framework/adapters/claude/adapter-conformance.md (T1 확정본) §2·§4 — Adapter Interface 커버리지(BP-7~11·BP-13 등)·정식화 배정표(harness-binding.md(T3)에 13 §4.1 조합 배정). 본 문서는 그 배정의 이행이다.
- docs/delegation-protocol.md §3 — 위임/보고 물리 채널 운용 관행. 위임·보고 프로토콜 조합 요소의 실현 소스.
- .claude/AGENT.md(상위 규약)·.claude/CLAUDE.md(Advisor 진입점·검증 게이트 규칙)·.claude/agents/ 4종(역할 정의 실물) — 최소 구성 5요소의 실물 실측 대상. 본 문서는 참조·실측만 하고 수정하지 않는다.
- framework/core/structure.md §2·§5 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·금지 토큰 규칙. 본 문서 경계의 근거.
- specs/00-glossary.md — 용어 정본(Harness §3.2-D·Harness 상태 J-13·핵심 루프 J-11·역할 §3.2-E). 본 문서는 새 용어를 신설하지 않는다.
- ROADMAP.md v0.2(Agent Harness Bootstrap)·v0.9(Adapter & Scaffold 정식화). 본 문서의 정식화 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 13 H-INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로·실행 모델 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형). 단 이 문서는 Core Contract(13 §3, 그리고 조합 대상 02·01·06 §3)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용하고, Harness가 소유하는 **조합 지점**만 물리 실현한다(13 §3 서두). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.9 Draft | 최초 작성. `framework/adapters/claude/` 경계의 산출물 — 13 §4.1 조합 바인딩 표를 물리 실현으로 정식화(adapter-conformance.md §4 배정 이행). 13 §4.1 조합 바인딩 표 **7행 전건**(상위 규약 문서·역할 4종·위임/보고·검증 게이트·작업 추적·실행 모델·호스트 프로세스)을 물리 실현("물리 실현" 열 + "실재 여부" 열, 형태 A/B 정직 구분)으로 매핑하고, 상세 정본이 02·01·06 소유임을 § 포인터로 유지하며 **조합 지점만** 소유(§2, 13 §3 서두 — 재정의 0). 13 §3.2-A 최소 구성 5요소 각각의 물리 실물 존재 실측 대조(§3). 13 §4.2 교체 지점 1~6 대응 표("교체되는 것/유지되는 것" — Harness 고유 이식 불변 재확인, §4). **13 §3.2-B 전이 조건 판정 비수행 명시**(§5 — 전이 재판정은 후속 Task T11 소관, 본 문서는 형태 A/B 구분을 위해 기존 확정 문서의 Bootstrap 전제만 인용하고 조건 4개 대조·재판정을 수행하지 않음). 상태 서술 실측 대조 표(§6 — 실재 서술 전건 파일 시스템 직접 실측 후 기입, L-07). 13·02·01·06 §3 계약 재정의·확장 0·새 최소 구성 요소·새 무결성 규칙·새 전이 조건 창설 0·Frozen specs 계수 15·Glossary 밖 새 용어 0. 형제 Task(PS2) 산출물 불인용(07 R2). 이 1파일만 생성(agent-binding.md와 함께 Task T3 소산) — 자매 바인딩 문서·specs/·docs/·.claude/ 무수정(07 R4). | Worker (Advisor 위임, Task T3) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/13-harness.md §3·§4(§4.1 조합 바인딩 표·§4.2 이식 교체 지점)이며, 조합 대상 요소의 상세 계약 정본은 02·01·06이다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(최소 구성 5요소·상태·전이 조건·무결성 규칙·역할 경계·메시지 필드·호스팅 계약)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- **조합 지점만 소유(13 §3 서두).** Harness는 "최소 구성의 선택과 무결성 규칙"만 소유한다 — Agent 계약(역할 경계·위임/보고 메시지)은 02가, 호스팅 계약(세션/턴 수명주기)은 01이, 검증 판정 기준은 06이 소유한다(13 §3 서두, Non-Goals). 본 문서는 이 둘을 재정의하지 않고 **최소 부분집합으로 조합하는 물리 지점**만 확정하며, 개별 요소의 상세 물리 실현은 자매 바인딩 문서(agent-binding.md·runtime-binding.md·verifier-binding.md·loop-binding.md)를 **조합 참조**한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 13 §4.1이 "각 요소의 상세 바인딩 정본은 소유 spec(01·02)의 §4이며, Harness는 이들을 최소 구성으로 조합하는 지점만 명시한다"고 둔 그 **조합 지점의 물리 실현**이 실재하는 자리이며, adapter-conformance.md §4가 harness-binding.md(T3)로 배정한 지점의 이행이다.
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 13 H-INV-8). 이 문서는 그 **반대편**이다 — 구체 토큰(규약 파일 `.claude/AGENT.md`·`.claude/CLAUDE.md`, 정의 파일 `.claude/agents/…`, 실행 모델 `model: opus`, 세션/턴, 서브에이전트, 백엔드 경로 `framework/adapters/claude/…`·`docs/…` 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 바인딩 문서 §0과 동형). **단 이 허용은 13·02·01·06 §3 계약 문면을 바꿀 권한을 뜻하지 않는다** — 무변경, 인용만 한다.
- **창설 금지.** 이 문서는 13 §4.1 조합 표를 **넘어서는 새 조합 바인딩을 창설하지 않는다**. 새 최소 구성 요소·새 무결성 규칙(H-INV-n)·새 전이 조건·새 상태를 만들지 않는다.
- **하네스 상태 전제 · 전이 판정 비수행(§5).** 형태 A(문서·규약)/형태 B(실행 코드) 구분을 위해, 이 하네스가 현재 **Bootstrap 상태**라는 전제는 기존 확정 문서(Glossary J-13, delegation-protocol.md §0, 자매 바인딩 문서 §0)가 이미 기록한 것을 인용한다. **본 문서는 13 §3.2-B 전이 조건 4개의 대조·재판정을 수행하지 않는다** — 전이 재판정은 후속 Task(T11) 소관이다(§5). `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(session-handoff-v0.3.md §1.4 A5 사례·§1.5 Lesson 후보 3 재발 방지, Active Lesson L-07). §2 "실재 여부" 열·§3 실물 대조·§6 실측 대조 표의 전 행은 파일 시스템 직접 실측(2026-07-06)에 근거한다 — 미존재를 실재로, 미래 산출물을 현재 실재로 쓰지 않는다.
- 용어는 specs/00-glossary.md 정본만 사용한다. Harness·Harness 상태(Bootstrap/Formal)·핵심 루프·최소 구성 집합·검증 게이트·작업 추적은 Glossary §3.2-D·§3.2-J·J-11·J-13 정본이며, 4역할은 Glossary §3.2-E 정본이다. 본 문서는 그 물리 실현 조합 매핑만 낸다. `형태 A/B`는 structure.md 서술 라벨의 인용이며 Glossary 표제어가 아니다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 13 §4.1(Harness Claude Code Binding 조합 표)을 이 환경 위에 **v0.9 시점의 구체 물리 실현**으로 매핑하고, 최소 구성 5요소의 물리 실물을 실측 대조한다(§0, adapter-conformance.md §4 배정 이행).

책임은 다섯 가지다.

- 13 §4.1 조합 바인딩 표의 **7행 전건**을 물리 표면으로 확정하고, Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을 "실재 여부" 열로 정직하게 구분한다. 상세 정본이 02·01·06 소유임을 § 포인터로 유지하고 **조합 지점만** 소유한다(§2, 13 §3 서두 — 재정의 0).
- 13 §3.2-A 최소 구성 5요소 각각의 **물리 실물(존재 실측)**을 대조한다(§3).
- 13 §4.2 이식 교체 지점 1~6 각각에 본 문서의 대응과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§4).
- **13 §3.2-B 전이 조건의 판정은 수행하지 않는다** — 전이 재판정이 후속 Task(T11) 소관임을 명시한다(§5).
- 상태 서술을 실측과 대조한다(§6).

이 문서는 13·02·01·06 §3의 어떤 계약 요소도 재정의·확장하지 않는다(§0, §7). 형태 A → 형태 B 전환 시에도 Core Contract 변경은 0이며(structure.md §7 C-1), 이 문서(§4의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 13 §4.1 조합 바인딩 표 7행 물리 실현 (done 1)

13 §4.1 Claude Code Binding 조합 표의 **7행 전건**을 물리 표면으로 매핑한다. 아래 표의 "13 §4.1 조합 바인딩" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경) — 조합 참조" 열이 본 문서가 확정하는 **조합 지점**(자매 바인딩 문서·실물의 조합 참조)을, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을, "상세 정본" 열이 재정의 없이 인용하는 소유 spec을 명시한다(§6 실측 대조). "실재" 서술은 전건 파일 시스템 직접 실측 후 기입했다(L-07).

| # | 13 §4.1 §3 구성 요소 | 13 §4.1 조합 바인딩 (정본 인용) | 물리 실현 (claude 환경) — 조합 참조 | 실재 여부 | 상세 정본 |
|---|---|---|---|---|---|
| 1 | 상위 규약 문서 | `.claude/AGENT.md`(공통 규약), `.claude/CLAUDE.md`(Advisor 진입점 바인딩) | 상위 규약 = `.claude/AGENT.md`(실재)·Advisor 진입점 = `.claude/CLAUDE.md`(실재)의 조합. 물리 실현은 agent-binding.md §2 행 2 소유 — 본 문서는 최소 구성 요소로 **조합 참조**한다(재정의 0). | 2파일 실재(§6 실측). | 02 §4.1 (agent-binding.md §2 행 2) |
| 2 | Agent 역할 정의 4종 | `.claude/agents/{advisor,planner,worker,verifier}.md` | 4역할 정의 파일 = `.claude/agents/` 4종(실재)의 조합. 물리 실현은 agent-binding.md §2 행 1 소유 — 조합 참조. 4역할 경계 유지(H-INV-2)의 물리 실물이다. | 4파일 실재(§6 실측). | 02 §4.1·§3.2-A (agent-binding.md §2 행 1) |
| 3 | 위임·보고 프로토콜 | 서브에이전트 위임(위임 메시지 전달) + 서브에이전트 최종 응답(보고 회수) | 위임 = 서브에이전트 디스패치, 보고 = 최종 응답의 조합(delegation-protocol.md §3). 물리 실현은 agent-binding.md §4 소유 — 조합 참조. 완료 조건 포함 위임(H-INV-3)·독립 검증 전 보고 회수의 물리 채널이다. | 규약 실현(형태 A, Bootstrap). v0.2~v0.8 위임 사이클로 실증. | 02 §4.1·§3.2-B/C/D (agent-binding.md §4) |
| 4 | 검증 게이트 | Advisor의 독립 재검증 — `.claude/CLAUDE.md` "Worker 완료 보고를 그대로 신뢰하지 않는다" | 검증 게이트 = `.claude/CLAUDE.md`의 "Worker 완료 보고를 그대로 신뢰하지 않는다" 규칙(실재) + Verifier 독립 판정(CP2 — verifier-binding.md) + Advisor 최종 승인(CP3)의 조합. 구현 주체와 검증 주체 분리(H-INV-2·H-INV-4)의 물리 실물이다. 판정 기준 정본은 06. | `.claude/CLAUDE.md` 규칙 실재(§6 실측). 게이트 운용 규약 실현(형태 A). | 02 §4.1·06 §4.1 (verifier-binding.md) |
| 5 | 작업 추적 | Wave 단위 위임·검증 사이클과 결정 기록(Open Questions·결정 기록 관행) | 작업 추적 = Wave 단위 위임·검증 사이클(delegation-protocol.md §3.3) + 결정 기록·Open Questions 관행 + 루프 상태 기록 백엔드(`framework/adapters/claude/loop-data/` — loop-binding.md §3) + 검증 리포트(`docs/v0.X-verification-report.md` 6건 — verifier-binding.md §4)의 조합. 결정의 기록(H-INV-5)의 물리 실물이다. | Wave 사이클 규약 실현(형태 A). 백엔드(loop-data/)·검증 리포트 6건 실재(§6 실측). | 13 H-INV-5 (부트스트랩 관행 — loop-binding.md §3·verifier-binding.md §4) |
| 6 | 실행 모델 지정 | Worker의 기본 실행 모델 = Opus 등 역할별 모델 지정 | 역할별 실행 모델 지정 = worker/planner/verifier `model: opus`·advisor 세션 상속(실측)의 조합. 물리 실현은 agent-binding.md §3 소유 — 조합 참조(재정의 0). | 4역할 실행 모델 지정 실재(§6 실측). | 02 §4.1 SP-3 (agent-binding.md §3) |
| 7 | 호스트 프로세스 | Claude Code 세션/턴 = 사이클 실행 컨테이너 | 호스트 프로세스 = Claude Code **세션/턴**(Bootstrap~Serve~Shutdown 실행 컨테이너)의 조합 참조. 물리 실현은 runtime-binding.md §2 #10·§3.4 소유 — 조합 참조. 최소 부분집합 호스팅(H-INV-6)의 실행 컨테이너다. | 세션/턴 컨테이너 실재(현 세션). 실행 Bootstrap/Shutdown(형태 B)은 미도입. | 01 §4.1 (runtime-binding.md §2 #10·§3.4) |

주:

- 위 7행은 13 §4.1 조합 표의 전 행이다. 각 행의 "물리 실현"은 13 §4.1 정본 표현을 이 환경의 조합 지점으로 좁힌 것이며, **개별 요소의 상세 물리 실현은 자매 바인딩 문서가 소유하고 본 문서는 조합 참조만** 한다(13 §3 서두 — Harness는 조합만 소유). 새 조합 바인딩을 창설하지 않는다(§0).
- **조합 참조 = 재정의 0.** 행 1·2·6(상위 규약·역할 4종·실행 모델)은 agent-binding.md(Task T3 동반 산출)가, 행 3(위임/보고)은 agent-binding.md §4가, 행 4(검증 게이트)는 verifier-binding.md가, 행 5(작업 추적)는 loop-binding.md §3·verifier-binding.md §4가, 행 7(호스트 프로세스)은 runtime-binding.md §2 #10·§3.4가 상세 물리 실현을 소유한다. 본 문서는 이들을 **최소 구성 요소로 조합**하는 지점만 확정하고 그 실현 상세를 재서술하지 않는다.
- **물리 실재 / 형태 A / 형태 B 구분(정직).** 행 1(규약 2문서)·행 2(정의 4파일)·행 6(실행 모델 지정)·행 7(세션/턴 컨테이너)의 실재 표면과 행 4(`.claude/CLAUDE.md` 규칙)·행 5(loop-data/·검증 리포트 6건)의 백엔드·산출물은 물리 실재다. 행 3(위임/보고)·행 4(게이트 운용)·행 5(Wave 사이클)는 Bootstrap에서 **규약 실현(형태 A)**이다 — 서브에이전트 위임·최종 응답·독립 재검증으로 수행되며, 실행 Bootstrap/Shutdown·무인 자동 오케스트레이션은 형태 B다. 이 구분은 자매 바인딩 문서의 형태 A/B 구분과 정합한다.

---

## §3. 13 §3.2-A 최소 구성 5요소 물리 실물 대조 (done 1 상세)

13 §3.2-A 최소 구성 집합(5개 필수 요소 — H-INV-1)의 각 요소를 이 환경의 물리 실물로 존재 실측 대조한다. **각 요소의 상세 계약(역할 경계·메시지 필드·판정 기준 등)은 "소유·근거" 열의 정본이 소유하며, 본 표는 그 필수 요소의 물리 실물 존재만 대조한다(재정의 0).** 실물 존재는 전건 파일 시스템 직접 실측(2026-07-06) 후 기입했다(L-07).

| 필수 요소 (13 §3.2-A) | 소유·근거 (정본) | 물리 실물 (claude 환경) | 존재 실측 (2026-07-06) |
|---|---|---|---|
| 상위 규약 문서 (Governance) | AGENT.md, ARCHITECTURE.md | `.claude/AGENT.md`(공통 규약 실물) + ARCHITECTURE.md(최상위 기준). 모든 Agent 행동의 최상위 기준·Architecture First·Spec First 강제. | 실재 — `.claude/AGENT.md` 확인. ARCHITECTURE.md는 상위 규약 근거 정본. |
| Agent 역할 정의 4종 | 02 §3.2-A, Glossary §3.2-E | `.claude/agents/{advisor,planner,worker,verifier}.md` 4파일. 4역할 책임·경계 확립(H-INV-2 — 결정·구현·검증 분리). | 실재 — 4파일 확인. |
| 위임·완료/실패 보고 프로토콜 | 02 §3.2-B/C/D | 서브에이전트 위임(위임 메시지 8필드) + 최종 응답(완료 5필드·실패 5필드), delegation-protocol.md §2~§3 운용. 완료 조건 포함 위임(H-INV-3)·은폐 불가 보고. | 계약 실재(02 §3.2-B/C/D)·운용 지침 실재(delegation-protocol.md). 채널은 규약 실현(형태 A). |
| 검증 게이트 (Verification Gate) | ARCHITECTURE 3.4, AGENT.md Verification, 02 INV-4 | `.claude/CLAUDE.md` "Worker 완료 보고를 그대로 신뢰하지 않는다" 규칙 + Verifier 독립 판정(CP2, `.claude/agents/verifier.md`·verifier-binding.md) + Advisor 최종 승인(CP3). 완료 보고를 독립 검증 없이 승인하지 않는 통제 지점(H-INV-4). | `.claude/CLAUDE.md` 규칙 실재·`.claude/agents/verifier.md` 실재. 게이트 운용 규약 실현(형태 A). |
| 작업 추적 (Task Tracking) | 본 spec H-INV-5 | Wave 단위 위임·검증 사이클 + 결정 기록·Open Questions 관행 + `framework/adapters/claude/loop-data/`(루프 상태 기록 백엔드) + `docs/v0.X-verification-report.md`(검증 리포트 6건). 사이클 진행·완료·결정 기록(H-INV-5). | 백엔드(loop-data/)·검증 리포트 6건 실재(§6 실측). Wave 사이클은 규약 실현(형태 A). |

- **5요소 완비(H-INV-1 물리 근거).** 위 5요소는 전건 물리 실물(정의 파일·규약 문서·백엔드·검증 리포트) 또는 확정 계약(02 §3.2-B/C/D)으로 실현되며, 어느 하나도 부재가 아니다(§6 실측). 이는 13 §3.2-A "5개 필수 요소가 모두 존재해야 Harness가 성립한다"(H-INV-1)의 물리 실물 근거다. **단 본 문서는 이 실물 실측을 근거로 H-INV-1 충족을 대조 제시할 뿐, 13 §3.2-B 전이 조건(Bootstrap→Formal)을 재판정하지 않는다(§5).**
- **소유 구분(재정의 0).** 각 요소의 상세 계약은 "소유·근거" 열의 정본이 소유한다 — Harness는 이 5요소의 "필수성"과 "조합"만 소유하고(13 §3.2-A 주), 역할 경계·메시지 필드·판정 기준을 재정의하지 않는다.

---

## §4. 13 §4.2 이식 교체 지점 1~6 대응 (done 1)

13 §4.2 이식 교체 지점 1~6 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 최소 구성 5요소의 "필수성"과 무결성 규칙(§3.3) 불변(Harness 고유 이식 불변 요소)을 재확인한다.

| # (13 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경(claude) 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| 1 | 상위 규약 문서 위치·포맷(`.claude/*.md`) → 대상 환경의 규약·프롬프트 주입 방식 (02 SP-2) | §2 행 1, §3 | `.claude/AGENT.md`·`.claude/CLAUDE.md`의 위치·포맷·주입 방식(agent-binding.md §5 SP-2). | 최소 구성 요소 "상위 규약 문서"의 필수성(H-INV-1)·최상위 기준 지위. 공통 의무·역할 경계(02 §3). |
| 2 | Agent 역할 정의 파일(`.claude/agents/*.md`) → 대상 환경의 Agent 정의 메커니즘 (02 SP-1) | §2 행 2, §3 | `.claude/agents/{advisor,planner,worker,verifier}.md` 정의 파일 위치·포맷(agent-binding.md §5 SP-1). | 최소 구성 요소 "역할 4종"의 필수성·역할 경계 유지(H-INV-2). 02 §3.2-A. |
| 3 | 위임·보고 채널(서브에이전트 위임/최종 응답) → 대상 환경의 오케스트레이션·결과 반환 API (02 SP-4, SP-5) | §2 행 3, §3 | 서브에이전트 위임(디스패치)·최종 응답 채널(agent-binding.md §5 SP-4·SP-5). | 최소 구성 요소 "위임/보고 프로토콜"의 필수성·완료 조건 포함 위임(H-INV-3)·독립 검증 게이트(H-INV-4). 02 §3.2-B/C/D. |
| 4 | 실행 모델 지정(Worker = Opus 등) → 대상 환경의 모델·엔진 (02 SP-3) | §2 행 6 | 역할별 `model` 지정 — worker/planner/verifier `model: opus`·advisor 세션 상속(agent-binding.md §3·§5 SP-3). | 역할 경계·메시지 필수 필드(02 §4.2 "유지되는 것"). 모델 값은 환경 표면이며 계약이 아니다. |
| 5 | 작업 추적·결정 기록 메커니즘(Wave/서브에이전트 관행) → 대상 환경의 추적·기록 메커니즘 | §2 행 5, §3 | Wave 단위 사이클 + 결정 기록·Open Questions 관행 + loop-data/ 백엔드 + 검증 리포트 6건(loop-binding.md §3·verifier-binding.md §4). | 최소 구성 요소 "작업 추적"의 필수성·결정의 기록(H-INV-5). |
| 6 | 호스트 프로세스/세션 수명주기 → 대상 환경의 실행 프로세스 (01 §4.2) | §2 행 7 | Claude Code 세션/턴 = Bootstrap~Serve~Shutdown 실행 컨테이너(runtime-binding.md §2 #10·§3.4·§4 #4). | 최소 부분집합 호스팅(H-INV-6)·Runtime 호스팅 계약(01 §3.1-C). |

- **Harness 고유 이식 불변 요소(13 §4.2 말미).** 최소 구성 5요소의 "필수성"과 무결성 규칙(§3.3 H-INV-1~H-INV-8)은 어떤 환경에서도 유지된다 — 바뀌는 것은 각 요소의 실현 형태(위 "교체되는 것" 열)뿐이다. 이는 structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 각 교체 지점의 정식화는 소유 spec(02·01·06)이 담당하며(13 §4.2 "각 항목의 정식화는 소유 spec이 담당"), 본 문서는 그 정식화를 선취하지 않고 조합 지점의 v0.9 물리 실현에 한정한다(창설 금지, §0). 개별 SP(02 SP-1~SP-5)의 대응 상세는 agent-binding.md §5가 소유한다.

---

## §5. 13 §3.2-B 전이 조건 판정 비수행 (done 1 상세 — T11 소관)

13 §3.2-B는 Harness 상태(Bootstrap/Formal)와 Bootstrap→Formal 전이 조건 4개를 정의한다. **본 문서는 이 전이 조건의 판정(조건 1~4 대조·재판정)을 수행하지 않는다.**

- **비수행 범위.** 13 §3.2-B 전이 조건 4개 — (1) 관련 spec Frozen, (2) 환경 의존 실현의 Adapter Binding 이동·Core AI 의존 0건, (3) Runtime 정식 Module 호스팅, (4) Scaffold 설치 대상 — 각각에 대한 현 시점 충족/미충족 **대조·재판정은 본 문서의 소관이 아니다**. 이 전이 재판정은 **후속 Task(T11) 소관**이다.
- **형태 A/B 구분을 위한 Bootstrap 전제 인용(판정 아님).** 본 문서 §0·§2·§3의 형태 A/B 구분은 이 하네스가 현재 **Bootstrap 상태**라는 전제 위에서 이뤄진다. 이 전제는 본 문서가 새로 판정한 것이 아니라, 기존 확정 문서(Glossary J-13, delegation-protocol.md §0 "이 하네스는 현재 Bootstrap 상태다", 자매 바인딩 문서 §0)가 **이미 기록한 상태를 인용**한 것이다. 본 문서는 그 전제를 형태 A/B 라벨링에만 사용하며, 전이 조건 4개의 현 시점 대조를 수행하지 않는다(13 §3.2-B 판정은 T11).
- **경계 준수 근거.** 13 §7 "상태 판정 시연"은 "Verifier가 §3.2-B 전이 조건 4개를 관련 spec 상태와 대조해 Harness 상태를 판정한다"고 규정한다 — 즉 전이 조건 대조·판정은 검증 게이트(Verifier/후속 Task) 소관이다. 본 문서는 조합 지점의 물리 실현만 소유하므로(13 §3 서두), 이 판정을 선취하지 않는다. §3의 최소 구성 5요소 실물 실측은 H-INV-1(최소 구성 완비)의 물리 근거 대조일 뿐, 전이 조건 4개 판정이 아니다.

---

## §6. 상태 서술 실측 대조 (L-07 재발 방지)

session-handoff-v0.3.md §1.4(A5 사례 — 미존재를 "실재"로 서술 → 파일 시스템 전수 대조로 검출)·§1.5 Lesson 후보 3(상태 서술은 실측 후 기록, 이월 L-07)에 따라, 본 문서의 "실재/존재/부재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`) 직접 실측.**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `.claude/AGENT.md`·`.claude/CLAUDE.md` (§2 행 1·4, §3 상위 규약·검증 게이트) | 실재 (상위 규약·Advisor 진입점·검증 게이트 규칙) | 실재 — 2파일 확인. `.claude/CLAUDE.md` "Worker 완료 보고를 그대로 신뢰하지 않는다" 규칙 확인. |
| `.claude/agents/` 4역할 정의 파일 (§2 행 2, §3 역할 4종) | 실재 (advisor·planner·worker·verifier.md) | 실재 — 4파일 확인. |
| 실행 모델 지정 (§2 행 6) | 실재 (worker/planner/verifier `model: opus`·advisor 세션 상속) | 실재 — agent-binding.md §3·§6 실측과 정합(worker/planner/verifier front-matter `model: opus`·advisor `model` 라인 부재 확인). |
| `framework/adapters/claude/loop-data/` (§2 행 5, §3 작업 추적) | 실재 (루프 상태 기록 백엔드) | 실재 — loop-data/ 디렉터리 확인(loop-binding.md §3 소관 백엔드). |
| `docs/v0.X-verification-report.md` 6건 (§2 행 5, §3 작업 추적) | 실재 (검증 리포트 6건 — v0.3~v0.8) | 실재 — v0.3·v0.4·v0.5·v0.6·v0.7·v0.8-verification-report.md 6건 확인(verifier-binding.md §4 소관). |
| Claude Code 세션/턴 호스트 프로세스 (§2 행 7) | 실재 (현 세션이 실행 컨테이너) | 실재 — 현 세션이 그 컨테이너(runtime-binding.md §2 #10 소관). 실행 Bootstrap/Shutdown(형태 B)은 미도입. |
| `framework/adapters/claude/` 자매 바인딩 문서 (§0·§2 조합 참조) | 실재 (agent·runtime·verifier·loop-binding.md 등) | 실재 — agent-binding.md(본 Task 동반 산출)·runtime-binding.md·verifier-binding.md·loop-binding.md 확인. |
| `framework/adapters/claude/harness-binding.md` (본 문서) | 실재 (본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음(사전 실측 확인). |
| 13 §3.2-B 전이 조건 판정 (§5) | 비수행 (T11 소관) | 본 문서에 전이 조건 4개 대조·재판정 서술 0건 — 형태 A/B 구분용 Bootstrap 전제만 기존 문서 인용(§5). |
| Frozen specs 계수 | **15** (numbered 00~13 = 14 + TEMPLATE 1) | 실측 — specs/ = 00~13 numbered 14파일 + TEMPLATE.md = **15**. |
| 형제 Task(PS2) 산출물 (07 R2) | 불인용 (미완성 산출물) | 인용 0건 — scaffold-binding.md·scaffold-template/·.claude/commands/·hooks/plugins-binding §7 개정분 등 미인용 확인(§7). |

- **핵심 구분.** 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로, 미래 산출물을 현재 실재로 쓰지 않았다(A5/L-07 재발 방지). 최소 구성 5요소의 물리 실물(규약 2문서·역할 4파일·위임/보고 계약·검증 게이트 규칙·작업 추적 백엔드·검증 리포트 6건)이 전부 실측으로 확인되어 §2·§3 조합 매핑의 근거가 실재함을 입증한다. 전이 조건 판정은 수행하지 않았다(§5).

---

## §7. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 13 §3·§4의 물리 실현이며, 조합 대상 요소는 02·01·06 § 포인터로만 인용했다. 어떤 최소 구성 요소 정의·무결성 규칙(H-INV-n)·전이 조건·상태·역할 경계·메시지 필드도 이 문서에서 새로 확정되지 않는다 — 계약 기준은 13 §3(조합·무결성)과 02·01·06 §3(상세)이 소유한다. **13 §4.1 조합 표를 넘어서는 새 조합 바인딩·새 최소 구성 요소·새 H-INV·새 전이 조건·새 상태를 창설하지 않았다.**
- **조합 지점만 소유(13 §3 서두).** Harness는 최소 구성의 "선택"과 "조합"과 "무결성 규칙"만 소유한다. 본 문서는 그 조합 지점의 물리 실현만 확정하고, 개별 요소의 상세 물리 실현(상위 규약·역할 4종·위임/보고·실행 모델 = agent-binding.md, 검증 게이트 = verifier-binding.md, 작업 추적 = loop-binding.md·verifier-binding.md, 호스트 프로세스 = runtime-binding.md)은 자매 바인딩 문서를 **조합 참조**했다 — 재서술·재정의하지 않았다.
- **전이 판정 비수행(§5).** 13 §3.2-B 전이 조건 4개의 대조·재판정은 후속 Task(T11) 소관이며 본 문서는 수행하지 않았다. 형태 A/B 구분용 Bootstrap 전제는 기존 확정 문서를 인용만 했다.
- **Frozen 무변경.** specs/13(Frozen v0.1)·02·01·06(Frozen)을 수정하지 않았다. Frozen specs 계수를 표기할 자리에는 **15**(numbered 00~13 = 14 + TEMPLATE 1)로 표기했다.
- **격리 토큰의 단일 자리.** 구체 규약 파일(`.claude/AGENT.md`·`.claude/CLAUDE.md`)·정의 파일(`.claude/agents/…`)·실행 모델 지정(`model: opus`)·백엔드 경로(`framework/adapters/claude/loop-data/`·`docs/…`)·세션/턴·서브에이전트 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. 13 §3·02 §3·`framework/core/`·`framework/runtime/`은 이 토큰을 본문에 두지 않는다(structure.md §5 C-3, 13 H-INV-8). 이 문서는 그 격리의 반대편(허용 지점)이다 — 단 13·02·01·06 §3 문면 재정의 권한은 아니다(§0).
- **판정 성격.** 본 문서는 조합 지점의 물리 실현 매핑이며, 완료 조건 대조의 독립 판정(CP2 — Verifier)과 최종 승인(CP3 — Advisor)이 뒤따른다(02 §3.2-A). 자기 점검(CP1)을 최종 승인으로 삼지 않는다.
- **동시 작성 문서 경계(07 R2).** 같은 병렬 집합(PS2)에서 동시 작성 중인 형제 Task의 미완성 산출물(scaffold-binding.md·scaffold-template/·v0.9-install-guide.md·`.claude/commands/`·getting-started.md·specs/00-glossary.md 개정분·hooks-binding.md/plugins-binding.md §7 개정분)을 인용·추측하지 않았다(07 R2). 참조한 확정 정본은 Frozen specs(13·02·01·06·00)·Baseline 자매 바인딩 문서(runtime·verifier·loop-binding.md·adapter-conformance.md)·확정 실물(.claude/AGENT.md·CLAUDE.md·agents/ 4종)·delegation-protocol.md·structure.md·ROADMAP.md뿐이다. 자매 agent-binding.md는 본 Task(T3)의 동반 산출물이므로 확정 참조 대상이다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 이 파일(`framework/adapters/claude/harness-binding.md`)과 자매 agent-binding.md(같은 Task T3)만 생성하며, 자매 바인딩 문서·`framework/core`·`framework/runtime`·specs/·docs/·.claude/ 실물을 수정하지 않는다.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-HB-1 (전이 조건 재판정 후속 Task 정합 — 비차단).** 본 문서는 13 §3.2-B 전이 조건 판정을 수행하지 않았다(§5, T11 소관). T11이 전이 조건 4개를 재판정할 때, 본 문서 §2·§3의 조합 지점 물리 실현·5요소 실물 실측이 조건 2(환경 의존 실현의 Adapter Binding 이동)·조건 3(Runtime 정식 Module 호스팅)의 판정 입력이 될 수 있다. 본 문서는 그 입력의 실측 근거만 제공하고 판정은 T11에 남긴다 — 비차단.
- **OQ-HB-2 (adapter-conformance.md §4 배정 후속 격리 갱신 — 비차단).** adapter-conformance.md §4가 harness-binding.md(T3)를 13 §4.1 조합 배정으로 두고 후속 격리 갱신(T15)을 예고했다. 본 문서 생성으로 그 배정이 이행되었으므로, adapter-conformance.md의 관련 배정 서술을 본 문서 § 포인터로 정합화하는 격리 갱신이 필요할 수 있다. 이는 실현 소스의 정식화이지 커버리지·verdict 변경이 아니므로 비차단이다. 본 Task 소유 경계는 이 2파일이므로 adapter-conformance.md를 수정하지 않았다(07 R4).

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 산출물. 13 §4.1(Harness 조합 바인딩 표)의 **v0.9 물리 실현 매핑** + 13 §3.2-A 최소 구성 5요소 물리 실물 대조(adapter-conformance.md §4 배정 이행). 정본 = 13 §3·§4(조합·무결성)와 02·01·06 §3(상세). 본 문서는 **조합 지점만** 소유(재정의 0 — §0).
- **§2:** 13 §4.1 조합 표 **7행 전건**을 물리 표면으로 매핑("물리 실현 — 조합 참조" 열 + "실재 여부" 열 + "상세 정본" 열, 형태 A/B 정직 구분). 상위 규약·역할 4종·실행 모델(agent-binding.md)·검증 게이트(verifier-binding.md)·작업 추적(loop-binding.md·verifier-binding.md)·호스트 프로세스(runtime-binding.md)를 조합 참조.
- **§3:** 13 §3.2-A 최소 구성 5요소 물리 실물 대조 — 상위 규약 문서·역할 4종·위임/보고 프로토콜·검증 게이트·작업 추적 각각의 실물 존재 실측(H-INV-1 물리 근거). 상세 계약은 소유 정본(AGENT.md/ARCHITECTURE.md·02·06·13 H-INV-5)이 소유.
- **§4:** 13 §4.2 이식 교체 지점 1~6 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 최소 구성 5요소의 "필수성"·무결성 규칙 불변(Harness 고유 이식 불변) 재확인.
- **§5:** **13 §3.2-B 전이 조건 판정 비수행** — 전이 재판정은 후속 Task(T11) 소관. 본 문서는 형태 A/B 구분용 Bootstrap 전제를 기존 확정 문서에서 인용만 하고, 조건 4개 대조·재판정을 수행하지 않음.
- **§6:** 상태 서술 실측 대조(2026-07-06 직접 실측) — 규약 2문서·역할 4파일·실행 모델·loop-data/·검증 리포트 6건·세션/턴 실재; 실측 불일치 0건(A5/L-07 재발 방지).
- 13·02·01·06 §3 계약 재정의·확장 0 · 새 조합 바인딩·새 최소 구성 요소·새 H-INV·새 전이 조건 창설 0 · Frozen specs 계수 15 · Glossary 밖 새 용어 0. 구체 AI·환경·실행 모델 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 전이 판정 비수행(§5, T11). 형제 Task(PS2) 불인용(07 R2). 이 파일 + 자매 agent-binding.md(Task T3)만 생성(07 R4).
