# framework/core/structure — UAHF Framework 디렉터리 구조 규격

작성일: 2026-07-05
상태: v1.2 Baseline (개정 — §8 트리 갱신 · v1.2 UAF 정본 바인딩 3문서 반영 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-07). 직전 기준선: v1.0 Baseline (개정 — §8 트리 갱신 · 복수 Adapter 경계 실재 반영 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-E — 디렉터리/구조 규격 (계약 수준 3규칙). 본 문서가 인스턴스화하는 계약의 정본.
- specs/01-runtime.md §4.1 — 디렉터리 바인딩 표의 디렉터리 행 (물리 디렉터리 이름의 출처). 표 본문의 구체 바인딩 토큰은 Adapter Binding 문서 소관이므로 본 문서는 § 포인터로만 참조한다.
- specs/01-runtime.md §3.3 INV-4 — Core 디렉터리 AI 비의존 불변 규칙.
- ROADMAP.md v0.3 (Runtime & Core Kernel) — 산출물 목록: Core 모듈 디렉터리 구조(규격) / Runtime 프로토콜 구현물 / config 스키마 / 모듈 등록·교체 규칙 문서.

거버넌스: 이 문서는 `framework/core/` 소속 Core 문서다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.3 Draft | 최초 작성. framework/ 3경계 구조 규격, 01 §3.2-E 3규칙 대조, 확정 조건 C-1·C-2·C-3 명문화, v0.3 산출물 파일 목록 표. | Worker (Advisor 위임, Task A1) |
| 2026-07-05 | v0.3 Baseline | v0.3 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass, CP3 Advisor 승인). | Advisor |
| 2026-07-05 | v0.4 Draft | §2 경계 표에 Module 구현 디렉터리 경계 행 추가 (01 §4.1 도출 — `framework/{loop,memory,verifier,workflow,plugins}/`). 같은 상태를 서술하는 전 지점 전수 갱신 — 상태 머리말, §1 목적, §2 주, §3 규칙 1·2 경계 언급, §4 C-2 배치 규칙(형태 B 코드 경계에 Module 구현 디렉터리 포함·규칙 2·3·4), §5 C-3 확장(문서 본문 비의존을 Module 구현 디렉터리에 적용), §8 트리·요약. 01 §3 계약 재정의 0, Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task M1) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.5 Draft (개정 — §8 트리 갱신) | v0.5 Task V13 — Advisor 승인 하 격리 개정 (사용자 승인 v0.5 계획 — handoff §1.6 이월 후보 2 해소). §8 트리에 v0.4 `framework/memory/` 4문서·v0.5 `framework/verifier/` 5문서·`<adapter>` 이하 바인딩 문서(memory-binding.md·verifier-binding.md 파일명 추가)를 파일 시스템 직접 실측 후 반영(L-07) — 백엔드 물리 데이터는 이름을 명명하지 않고 소관 포인터로만 표기(C-3 확장 누출 금지). §6 표에 DP-V4 취지 주석 1문장 추가(표 자체 무변경 — v0.3 범위 유지). 같은 상태 서술 전 지점 전수 갱신(L-06): §2 주·§8 트리 주석의 '첫 실사용: memory/' 류를 실측 상태(memory/·verifier/ 실사용)로 정합화, §8 요약 계약 인스턴스 서술 정합화. C-3 금지 토큰 0(개정분 포함 자가 전수 스캔), 01 §3 계약 재정의 0, Glossary 밖 용어 신설 0. 근거: docs/v0.4-verification-report.md §3.4 관찰 2 해소. | Worker (Advisor 위임, Task V13) |
| 2026-07-06 | v0.5 Baseline | v0.5 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 26/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.6 Draft (개정 — §8 트리 갱신) | v0.6 Task L14 — Advisor 승인 하 격리 개정 (v0.5 V13 동형, 비차단 정합 개정). §8 트리에 v0.6 `framework/loop/` 4문서(module-manifest·loop-protocol·stage-transition-rules·loop-state-record)와 `<adapter>` 이하 loop-binding.md를 파일 시스템 직접 실측 후 반영(L-07) — 백엔드 물리 데이터는 이름을 명명하지 않고 기존 일반형 소관 포인터 행 유지(C-3 확장 누출 금지). {loop,workflow,plugins}/ 미실현 행을 {workflow,plugins}/ 미실현으로 실측 정합화. 같은 상태 서술 전 지점 전수 갱신(L-06): §2 주의 loop·workflow·plugins 미실현 서술을 실측 상태(v0.6 loop/ 실사용·4문서)로 정합화, §8 요약 계약 인스턴스 서술에 specs/03 추가. §6 표는 DP-V4대로 v0.3 산출물 범위 유지(무변경). C-3 금지 토큰 0(개정분 포함 자가 전수 스캔), 01 §3 계약 재정의 0, Glossary 밖 용어 신설 0. 근거: v0.6 framework/loop/ 4문서(W1·W2)·loop-binding.md(W3) 확정. | Worker (Advisor 위임, Task L14) |
| 2026-07-06 | v0.6 Baseline | v0.6 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.7 Draft (개정 — §8 트리 갱신) | v0.7 Task WF8 — Advisor 승인 하 격리 개정 (v0.5 V13·v0.6 L14 동형, 비차단 정합 개정). §8 트리에 v0.7 `framework/workflow/` 5문서(module-manifest·work-graph·decompose-rules·dispatch-protocol·merge-rules)와 `<adapter>` 이하 workflow-binding.md를 파일 시스템 직접 실측 후 반영(L-07) — 백엔드 물리 데이터는 이름을 명명하지 않고 기존 일반형 소관 포인터 행 유지(C-3 확장 누출 금지). {workflow,plugins}/ 미실현 행을 plugins/ 미실현으로 실측 정합화. 같은 상태 서술 전 지점 전수 갱신(L-06): §2 주의 실사용 인스턴스 열거에 v0.7 `framework/workflow/`(5문서) 추가·정본 specs/07-workflow.md 포인터 병기·미실현 서술을 plugins로 정합화, §8 요약 계약 인스턴스 서술에 specs/07 추가. §6 표는 DP-V4대로 v0.3 산출물 범위 유지(무변경). C-3 금지 토큰 0(개정분 포함 자가 전수 스캔), 01 §3 계약 재정의 0, Glossary 밖 용어 신설 0. 근거: v0.7 framework/workflow/ 5문서·workflow-binding.md 확정. | Worker (Advisor 위임, Task WF8) |
| 2026-07-06 | v0.7 Baseline | v0.7 개정분(§8 트리 갱신) 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.8 Draft (개정 — §8 트리 갱신) | v0.8 Task EX-C1 — Advisor 승인 하 격리 개정 (v0.5 V13·v0.6 L14·v0.7 WF8 동형, 비차단 정합 개정). §8 트리에 v0.8 `framework/plugins/` 3문서(module-manifest·plugin-manifest·plugin-lifecycle)와 `<adapter>` 이하 hooks-binding.md·skills-binding.md·plugins-binding.md를 파일 시스템 직접 실측 후 반영(L-07) — 백엔드 물리 데이터는 이름을 명명하지 않고 기존 일반형 소관 포인터 행 유지(C-3 확장 누출 금지). plugins/ 미실현 행을 실사용(v0.8)으로 실측 정합화. 같은 상태 서술 전 지점 전수 갱신(L-06): §2 주의 실사용 인스턴스 열거에 v0.8 `framework/plugins/`(3문서) 추가·정본 specs/10-plugins.md 포인터 병기·미실현 서술 해소, §8 요약 계약 인스턴스 서술에 specs/08·09·10 추가. §6 표는 DP-V4대로 v0.3 산출물 범위 유지(무변경). C-3 금지 토큰 0(개정분 포함 자가 전수 스캔), 01 §3 계약 재정의 0, Glossary 밖 용어 신설 0. 근거: v0.8 framework/plugins/ 3문서·확장 바인딩 3문서 확정. | Worker (Advisor 위임, Task EX-C1) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.9 Draft (개정 — §8 트리 갱신) | v0.9 Task T8 — Advisor 승인 하 격리 개정 (v0.5 V13·v0.6 L14·v0.7 WF8·v0.8 EX-C1 동형, 비차단 정합 개정). §8 트리 `framework/adapters/<adapter>/` 이하에 v0.9 신규 5산출물(agent-binding.md·adapter-conformance.md·harness-binding.md·scaffold-binding.md·scaffold-template/)을 파일 시스템 직접 실측 후 반영(L-07) — 각 바인딩 문서 1행 + 정본 § 포인터(agent=02·conformance=11·harness=13·scaffold=12 §4), scaffold-template/은 디렉터리 1행 + "구조·내용 정본은 Adapter Binding 문서 소관" 포인터(내부 파일 비열거 — C-3 확장 누출 금지, 백엔드 데이터 행과 동형). adapter-conformance.md 행은 "Adapter Interface 커버리지·Conformance 판정 인스턴스(11 §3)". 백엔드 물리 데이터는 이름 명명 없이 기존 일반형 소관 포인터 행 유지. 같은 상태 서술 전 지점 전수 갱신(L-06): §8 요약 계약 인스턴스 서술에 specs/02·11·12·13 추가(§2 주는 `<adapter>` 일반형·Module 구현 디렉터리 서술이므로 무변경 — 어댑터 바인딩 열거는 §8 트리 단일 소관, 자매 선례 v0.5~v0.8 동형). §6 표는 DP-V4대로 v0.3 산출물 범위 유지(무변경). C-3 금지 토큰 0(개정분 포함 자가 전수 스캔 — 구체 어댑터명은 `<adapter>` 일반형만 사용), 01 §3 계약 재정의 0, Glossary 밖 용어 신설 0. 근거: v0.9 framework/adapters/<adapter>/ 신규 5산출물(W1·W2) 확정. | Worker (Advisor 위임, Task T8) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v1.0 Draft (개정 — §8 트리 갱신) | v1.0 Task T8 — Advisor 승인 하 격리 개정 (v0.5 V13·v0.6 L14·v0.7 WF8·v0.8 EX-C1·v0.9 T8 동형, 비차단 정합 개정). §8 트리 `framework/adapters/` 아래에 두 번째 `<adapter>/` 노드(최소 구현 Adapter — 11 §3.2-B)를 추가해 **복수 Adapter 경계 실재**를 반영(파일 시스템 직접 실측, L-07) — 두 번째 경계는 파일 목록·바인딩 값 정본을 그 Adapter Binding 문서 소관으로 두고 **내부 파일 비열거**(scaffold-template/·백엔드 격리 데이터 행과 동형 — 열거는 즉시 stale 위험·C-3 확장 누출이므로 소관 포인터로 대체). 기존 첫 노드는 "첫 번째 Adapter 경계(완전 구현)" 성격 주석으로 정합화, `adapters/` 노드에 복수 경계 실재 주석 병기. 실명 0 — `<adapter>` 일반형만 사용. 같은 상태 서술 전 지점 전수 갱신(L-06): "Adapter 경계 단수" 하드 전제 서술 0건 확인(§2 주·§6 주·§8 요약 bullet 전부 `<adapter>` 일반형 또는 `adapters/` 범주 서술이므로 무변경 — §2 주는 이미 복수 바인딩 뿌리 실재 가능을 명시, 자매 선례 v0.5~v0.9 동형). §6 표는 DP-V4대로 v0.3 산출물 범위 유지(무변경). C-3 금지 토큰 0(개정분 포함 자가 전수 스캔 — 구체 어댑터명 두 이름 모두·특정 AI·모델명·제품 기능명·언어명·툴체인명 0), 01 §3 계약 재정의 0, Glossary 밖 용어 신설 0. 근거: v1.0 두 번째 Adapter 경계 신설 실측. | Worker (Advisor 위임, Task T8) |
| 2026-07-07 | v1.0 Baseline | v1.0 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 21/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-07 | v1.2 Draft (개정 — §8 트리 갱신) | v1.2 Task T-S — Advisor 승인 하 격리 개정 (v0.5 V13·v0.6 L14·v0.7 WF8·v0.8 EX-C1·v0.9 T8·v1.0 T8 동형, 비차단 정합 개정). §8 트리 첫 `<adapter>/` 경계(scaffold-binding.md 다음·scaffold-template/ 앞)에 v1.2 신규 UAF 정본 바인딩 3문서(contract-binding.md=uaf/specs/03 §4·entry-binding.md=uaf/specs/01 §4·discovery-binding.md=uaf/specs/02 §4)를 파일 시스템 직접 실측 후 반영(L-07) — 각 바인딩 문서 1행 + uaf/specs §4 물리 실현 § 포인터. 백엔드 격리 데이터 디렉터리는 트리에 추가하지 않고 기존 포괄 주석("백엔드 격리 데이터 — Core 문서 비서술")이 커버(타 Module 백엔드 데이터 디렉터리 미열거 선례 동형 · 물리 이름 비명명으로 C-3 확장 누출 금지). 상태 라인 v1.2 Draft 갱신 · 직전 기준선 v1.0 문면 보존. §6 v0.3 산출물 표는 DP-V4대로 무변경. C-3 금지 토큰 0(개정분 포함 자가 전수 스캔 — uaf/specs·UAF는 § 포인터·상위 프레임워크 네임스페이스 참조로 허용, 특정 AI·모델명·제품 기능명·언어·툴체인·직렬화 형식 토큰 0), 01 §3 계약 재정의 0, Glossary 밖 용어 신설 0. 근거: v1.2 `framework/adapters/<adapter>/` 신규 3바인딩 문서(W1~W3) 확정. | Worker (Advisor 위임, Task T-S) |
| 2026-07-07 | v1.2 Baseline | v1.2 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass 16/0/0; CP3 Advisor 승인) | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/01-runtime.md §3이다.** 이 문서는 그 Core Contract의 **인스턴스**이며, 계약을 재정의·확장하지 않는다. 계약 요소는 § 포인터로만 참조한다.
- 이 문서는 `framework/` 디렉터리 구조의 **규격(specification)**이다. 물리 경로 이름은 01 §4.1 디렉터리 행에서 도출하고, 그 경계 위에 배치·역할·소유 계약을 확정한다.
- **이 문서는 Core 문서다.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명을 두지 않는다 (01 §3.3 INV-4, 확정 조건 C-3, §5). 구체 인스턴스(구체 어댑터명·디렉터리명·직렬화 형식·환경 경로 관례)는 **Adapter Binding 문서 소관**이며, 필요한 자리에는 일반형 표기 `<adapter>`와 소관 포인터만 둔다.
- 용어는 specs/00-glossary.md 정본만 사용한다. 새 용어를 신설하지 않는다. "형태 A / 형태 B"는 아래 확정 조건 C-1·C-2에서 도입된 서술 라벨이며 Glossary 표제어가 아니다 — 정본 용어처럼 신설·확장하지 않고 확정 조건의 라벨로만 인용한다.

---

## §1. 목적

`framework/` 디렉터리는 UAHF의 Core Layer·Runtime Layer 규격, Module 자기완결 구현 경계, Adapter Layer 바인딩 산출물이 물리적으로 어디에 놓이는가를 규율한다.

이 규격의 책임은 세 가지다.

- Core 계약(AI 비의존)과 Adapter 바인딩(환경 의존)의 **물리 경계**를 분리한다 (ROADMAP 2.3, 01 §3.2-E 규칙 3).
- v0.3 산출물 각각이 01 §3의 어느 계약을 인스턴스화하는지 **경계와 소유**를 확정하여, 후속 병렬 Task의 소유 경계(specs/07-workflow.md §3.2-B)가 이 표에서 도출되게 한다.
- 실행 코드가 도입되어도(향후 형태 B) 01 §3 Core Contract 변경이 0으로 유지되는 **불변 조건**을 명문화한다 (확정 조건 C-1).

---

## §2. 4경계 배치·역할·소유 계약 (done 대상 — 4경계 표)

`framework/` 아래 네 경계의 배치·역할·소유와, 각 경계가 인스턴스화하는 01 § 계약이다. 물리 디렉터리 이름은 01 §4.1 디렉터리 행에서 도출한다.

| 경계 (디렉터리) | 배치 (귀속 Layer / 소속) | 역할 | 소유 (무엇을 소유하는가) | 인스턴스화하는 01 § 계약 |
|---|---|---|---|---|
| `framework/core/` | Core Layer | AI 비의존·언어/툴체인 비의존 **계약·스키마 문서**를 담는 경계. 실행 코드를 담지 않는다. | Core Contract 인스턴스 문서, Config 스키마 문서, 본 구조 규격 | 01 §3 (Core Contract 전체), §3.2 (Data Format — 스키마 수준), §3.2-E 규칙 1, §3.3 INV-4 |
| `framework/runtime/` | Runtime Layer | Runtime 호스팅·모듈 시스템 계약의 **프로토콜 문서**를 담는 경계. 문서 본문은 AI·언어/툴체인 비의존 (§4.1이 이 디렉터리를 AI 비의존으로 지정). 향후 형태 B 실행 코드의 실현 경계이기도 하다 (§4). | Module 시스템·수명주기 프로토콜 문서, (형태 B 시) 실행 코드 실현 | 01 §3.1 (Register/Resolve/Replace/Deregister · Bootstrap/Shutdown), §3.2-A·C·D, §3.2-E 규칙 2, §3.3 INV-1·INV-2·INV-3·INV-6·INV-7 |
| `framework/{loop,memory,verifier,workflow,plugins}/` | Module 자기완결 구현 경계 (단일 Layer 비고정). 각 Module의 귀속 Layer는 그 Module이 실현하는 Component를 따른다 (Glossary §3.2-D). Runtime이 호스팅하는 Module 단위의 실현 자리다. | 각 Module이 자신의 Manifest·구현·(있다면) configSchema를 한 경계 안에 두는 **자기완결 경계** (01 §3.2-E 규칙 2 인스턴스). 문서 본문은 AI·언어·툴체인 비의존 (C-3 확장 — §5). 향후 형태 B 실행 코드의 실현 경계이기도 하다 (§4 C-2). | 각 Module의 자기완결 단위 (Manifest·구현·(있다면) configSchema). 하위 디렉터리(군)는 01 §4.1이 지정한 물리 이름이자 Core Component 명칭이다. | 01 §3.2-E 규칙 2 (Module 자기완결 단위), §3.2-A (Module Manifest), §3.3 INV-4 |
| `framework/adapters/<adapter>/` | Adapter Layer | Core 계약을 특정 실행 환경·AI·언어·툴체인에 바인딩한 **산출물을 격리**하는 경계. AI·환경 의존 요소는 전부 여기로 격리한다. | Adapter Binding 산출물 (환경 의존 실현) | 01 §4 (Adapter Binding), §4.1 (바인딩 표), §4.2 (이식 교체 지점), §3.2-E 규칙 3 |

주 (경계 도출 근거):

- 네 물리 디렉터리(군) 이름은 01 §4.1 "디렉터리 바인딩 표"의 디렉터리 행에서 도출한다. §4.1은 `framework/core/`·`framework/runtime/`을 "Core 디렉터리 (AI 비의존)"으로, `framework/{loop,memory,verifier,workflow,plugins}/`를 "Module 구현 디렉터리"로, `framework/adapters/`를 "Adapter Binding 산출물" 격리 경계로 지정한다. §4.1 표 본문의 **구체 환경·제품·형식 바인딩 토큰은 Adapter Binding 문서 소관**이므로 본 Core 문서는 재현하지 않고 § 포인터로만 참조한다.
- **Module 구현 디렉터리의 지위.** `framework/{loop,memory,verifier,workflow,plugins}/`(Module 구현 디렉터리)는 §4.1이 "Core 디렉터리"로 명시한 두 경계(`framework/core/`·`framework/runtime/`)와는 **별개의 디렉터리 행**이다. 다만 그 **문서 본문**은 같은 AI·언어·툴체인 비의존을 유지한다 (C-3 확장 — §5, Advisor 확정 v0.4). 하위 디렉터리 이름(loop·memory·verifier·workflow·plugins)은 §4.1 도출 물리 이름이자 Core Component 명칭이므로 금지 토큰이 아니다 (§5). v0.4에서 `framework/memory/`(4문서)가, v0.5에서 `framework/verifier/`(5문서)가, v0.6에서 `framework/loop/`(4문서)가, v0.7에서 `framework/workflow/`(5문서)가, v0.8에서 `framework/plugins/`(3문서)가 이 경계의 실사용 인스턴스다 (계약 정본은 각각 specs/04-memory.md·specs/05-lessons.md와 specs/06-verifier.md와 specs/03-loop.md와 specs/07-workflow.md와 specs/10-plugins.md 소관 — § 포인터, 본 Core 문서는 그 내용을 재서술하지 않는다). 이로써 다섯 Module 구현 디렉터리(loop·memory·verifier·workflow·plugins)가 전부 실사용 상태이며(미실현 경계 0), 각 실측 파일 목록은 §8 트리에 열거한다.
- `<adapter>`는 일반형 표기다. 구체 어댑터명(하위 디렉터리 이름 포함)은 해당 Adapter Binding 문서가 소유한다 (§6, §0).
- `framework/adapters/` 외에 존재할 수 있는 여타 환경 의존 바인딩 뿌리 역시 Adapter Binding 문서 소관이며 본 Core 문서는 명명하지 않는다.

---

## §3. 01 §3.2-E 3규칙 충족 대조 (done 대상 — 규칙별 대조)

01 §3.2-E는 계약 수준 3규칙을 정의한다. 각 규칙이 §2 구조에서 어떻게 충족되는지 항목별로 대조한다.

### 규칙 1 — Core 디렉터리는 AI 비의존 계약만 담는다 (AI 의존 요소 0건, 01 §3.2-E, INV-4)

- **충족 방식.** `framework/core/`는 오직 AI 비의존 계약·스키마 문서만 담는다 (§2, 확정 조건 C-2 — §4). `framework/runtime/` 문서 본문도 같은 비의존 지위를 승계한다 (01 §4.1이 두 디렉터리를 함께 AI 비의존으로 지정).
- **강화.** 본 규격은 여기에 언어·툴체인 비의존까지 더한다 (확정 조건 C-3 — §5). 따라서 두 경계 문서 본문의 금지 대상은 { 특정 AI 요소 } ∪ { 특정 언어·툴체인 요소 }다. 이 금지 대상 집합은 `framework/{loop,memory,verifier,workflow,plugins}/`(Module 구현 디렉터리)의 **문서 본문**에도 확장 적용된다 (C-3 확장 — §5, Advisor 확정 v0.4). 이 경계는 §4.1이 "Core 디렉터리"로 명시한 두 경계에 포함되지는 않으나(§2 주), 문서 본문의 AI·언어·툴체인 비의존은 동일하게 유지한다.
- **검증 지점.** §5 금지 토큰 규칙 + §6 파일 목록의 "소속 경계" 열. AI·언어·툴체인 의존이 필요한 실현은 규칙 3에 따라 `framework/adapters/<adapter>/`로 격리된다.

### 규칙 2 — 각 Module은 자기완결(self-contained) 단위다 (01 §3.2-E)

- **충족 방식.** 각 Module은 자신의 Manifest·구현·(있다면) configSchema를 한 경계 안에 둔다 (01 §3.2-E). 이 자기완결 경계의 물리 자리가 `framework/{loop,memory,verifier,workflow,plugins}/`(Module 구현 디렉터리, §2 — 01 §4.1 도출)이며, 각 Module은 그 아래 자신의 한 경계에 요소를 모은다. 이와 별개로, Module 등록 서술자 계약(정본: 01 §3.2-A Module Manifest)이 자기완결 단위의 기준 인스턴스이며, `framework/runtime/module-manifest.md`(§6)가 그 서술자 계약을 인스턴스화한다.
- **형태 B 확장.** 실행 코드 도입 시 각 Module은 `framework/{loop,memory,verifier,workflow,plugins}/`(Module 구현 디렉터리, §2) 아래 **자신의 한 경계**에 Manifest·구현·configSchema를 함께 둔다. 한 Module의 요소가 여러 경계로 흩어지지 않는다. 이 경계의 실행 코드 실현은 형태 B 사안이며, v0.4 시점의 실현은 형태 A(문서)다 (§4 C-2, Advisor 확정).
- **검증 지점.** Manifest 서술자(01 §3.2-A)가 `id`·`contract`·`entrypoint` 등 자기완결 참조를 한 서술자에 묶는다는 점 — 필드 정본은 01 §3.2-A가 유지하며 본 문서는 재정의하지 않는다.

### 규칙 3 — Adapter Binding 산출물은 Core 디렉터리와 물리적으로 분리된 별도 경계에 둔다 (01 §3.2-E)

- **충족 방식.** Adapter Binding 산출물은 `framework/adapters/<adapter>/`로 물리 분리된다 (§2). 이 경계는 Core 경계(`framework/core/`·`framework/runtime/`)와 **겹치지 않는다**.
- **검증 지점.** §6 파일 목록에서 Adapter 바인딩 문서만 `framework/adapters/<adapter>/` 소속이고, 나머지 v0.3 산출물은 전부 `framework/core/`·`framework/runtime/` 소속이다 — 두 경계 집합이 비중첩임을 표로 확인할 수 있다. AI·실행 환경·백엔드 의존은 전부 Adapter Layer 뒤(이 경계)에 둔다 (INV-4).

---

## §4. 계약·문서 전용 경계와 실행 코드 배치 규칙 (확정 조건 C-2)

확정 조건 C-2를 명문화한다.

- **C-2.** `framework/core/`는 **계약·스키마 문서 전용**이다. 실행 코드(향후 형태 B)는 `framework/core/` 밖의 non-core 경계 — `framework/runtime/`, Module 구현 디렉터리(`framework/{loop,memory,verifier,workflow,plugins}/`), `framework/adapters/` 이하에만 추가된다.
- **C-2 적용 주 (Advisor 확정 v0.4).** Module 구현 디렉터리를 이 non-core 실행 코드 경계에 포함하는 것은 사용자 확정 조건 C-2("실행 코드는 Runtime·Adapter Layer에만, core/는 문서 전용")의 **불변 핵심을 보존**한다 — (i) `framework/core/`는 여전히 문서 전용이고, (ii) Module 구현 디렉터리는 Runtime이 호스팅하는 Module 실현 경계이므로 Runtime Layer 호스팅 실현의 일부다 (§2 배치; Runtime Layer는 모듈의 실행·수명주기를 관장한다 — Glossary §3.2-A Runtime Layer). Module의 **기능적** 귀속 Layer는 그 Module이 실현하는 Component를 따르지만(§2 배치, Glossary §3.2-D), 실행 코드가 놓이는 **호스팅** 경계는 Runtime 실현이다. 이는 아래 규칙 2가 종전에 "별도 Module 구현 경계"로만 지칭하던 자리를 명시화한 것이며, 계약 확장이 아니다.

세부 규칙:

1. `framework/core/`에는 실행 코드를 두지 않는다. Core Contract 인스턴스 문서와 스키마 문서(예: Config 스키마 문서)만 둔다.
2. 향후 실행 코드(형태 B)는 `framework/runtime/`, Module 구현 디렉터리(`framework/{loop,memory,verifier,workflow,plugins}/`, §2), 또는 `framework/adapters/<adapter>/` 이하에만 배치한다. `framework/core/`에는 어떤 형태 B 실행 코드도 두지 않는다.
3. **아티팩트 구분.** C-2(실행 코드 배치)와 §5의 C-3(문서 본문 비의존)은 서로 다른 아티팩트 부류에 작용한다 — C-3은 **문서 본문**(계약·프로토콜·스키마 문서)에, C-2는 **실행 코드**에 적용된다. 따라서 `framework/runtime/`과 Module 구현 디렉터리(`framework/{loop,memory,verifier,workflow,plugins}/`)는 문서 본문을 AI·언어/툴체인 비의존으로 유지하면서(§5, C-3 확장) 동시에 형태 B 실행 코드의 실현 경계가 될 수 있다.
4. **형태 B 실현의 격리 원칙.** 실행 코드가 도입될 때 AI·실행 환경·언어·툴체인 의존 부분은 01 §3.2-E 규칙 3·INV-4에 따라 `framework/adapters/<adapter>/` 뒤로 격리한다. non-core 실현 경계(`framework/runtime/`, Module 구현 디렉터리, `framework/adapters/<adapter>/`) 사이의 정확한 분할(무엇이 어느 경계에 남고 무엇이 adapter 경계로 가는가)은 형태 B가 실제로 설계될 때 확정한다. 본 규격은 이를 미리 추측·확정하지 않는다 (§0 정본 경계, 추측 금지).

---

## §5. 금지 토큰 규칙 (확정 조건 C-3)

확정 조건 C-3을 명문화한다.

- **C-3.** `framework/core/`·`framework/runtime/`은 AI 비의존이면서 특정 프로그래밍 언어·툴체인 비의존을 유지한다.
- **C-3 확장 (Advisor 확정, v0.4).** 같은 문서 본문 비의존을 Module 구현 디렉터리(`framework/{loop,memory,verifier,workflow,plugins}/`)의 **문서 본문**에도 적용한다. 이 경계는 §4.1이 "Core 디렉터리"로 명시한 두 경계에 포함되지는 않으나(§2 주), 그 문서 본문은 동일한 금지 대상 집합을 적용받는다. Adapter 경계(`framework/adapters/`)는 환경 의존 토큰을 격리 보유하므로 이 비의존 범위에서 제외된다.

규칙:

- C-3 적용 범위는 세 문서 본문 경계다 — `framework/core/`·`framework/runtime/`(C-3 본체) + Module 구현 디렉터리(`framework/{loop,memory,verifier,workflow,plugins}/`, C-3 확장). 이 **문서 본문**의 금지 대상은 다음 두 후보 집합을 **모두** 포함한다.
  1. 특정 AI 의존 요소 — 특정 AI 이름·모델명·제품 기능명 (01 §3.3 INV-4의 대상).
  2. 특정 언어·툴체인 의존 요소 — 특정 프로그래밍 언어명·툴체인명·환경 의존 요소 (본 규격이 C-3으로 추가하는 대상).
- 이 세 경계(C-3 적용 범위)의 어떤 문서도 위 두 집합의 토큰을 본문에 두지 않는다. 규칙을 서술하는 문안에서도 구체 예시 토큰을 나열하지 않는다 — 예시가 필요하면 **"구체 인스턴스는 Adapter Binding 문서 소관"** 포인터로 대체한다 (mention/use 경계: 금지 토큰의 예시도 Core 문서에서는 누출이다).
- 구체 인스턴스가 필요한 자리에는 일반형 표기와 소관 포인터만 둔다 (예: 어댑터 하위 경계는 `<adapter>`, 직렬화 형식·환경 경로 관례는 "Adapter Binding 문서 소관").
- 검증: 이 세 경계(C-3 적용 범위) 문서에 대해 위 후보 집합 **전체**(AI 이름·모델명·제품 기능명·언어명·툴체인명)로 전수 스캔하여 0건임을 확인한다. 단일 토큰 검색 하나로 넓은 결론을 내지 않는다.

---

## §6. v0.3 산출물 파일 목록 (done 대상 — 산출물 표)

v0.3 산출물 각 파일과 그것이 인스턴스화하는 01 § 계약, 소속 경계, 소유 경계다. 각 행이 후속 병렬 Task 하나의 소유 경계(specs/07-workflow.md §3.2-B ownedBoundary)를 도출한다 — 한 Task는 자신의 행 파일만 배타 소유·수정한다 (07 R4, INV-2 경계 불가침).

| 산출물 파일 | 소속 경계 | 인스턴스화하는 01 § 계약 | 대응 ROADMAP v0.3 산출물 | 후속 Task 소유 경계 |
|---|---|---|---|---|
| `framework/runtime/module-manifest.md` | `framework/runtime/` (Core, AI·언어/툴체인 비의존) | 01 §3.2-A (Module Manifest), §3.2-E 규칙 2 | Runtime 프로토콜 구현물 (일부) | 이 파일 1개 |
| `framework/runtime/module-registry.md` | `framework/runtime/` (Core, AI·언어/툴체인 비의존) | 01 §3.1-A (Register/Resolve/Replace/Deregister), §3.2-C (registry 필드), §3.3 INV-1·INV-3·INV-7 | 모듈 등록/교체 규칙 문서 | 이 파일 1개 |
| `framework/core/config-schema.md` | `framework/core/` (Core, 계약·스키마 문서 전용) | 01 §3.2-B (Config), §3.1-B (Load Config), §3.3 INV-5 | config 스키마 | 이 파일 1개 |
| `framework/runtime/lifecycle.md` | `framework/runtime/` (Core, AI·언어/툴체인 비의존) | 01 §3.1-C (Bootstrap/Shutdown), §3.2-C (Runtime Context), §3.2-D (Failure Report), §3.3 INV-2·INV-6 | Runtime 프로토콜 구현물 (일부) | 이 파일 1개 |
| `framework/adapters/<adapter>/runtime-binding.md` | `framework/adapters/<adapter>/` (Adapter, 환경 의존 격리) | 01 §4.1 (바인딩 표), §4.2 (이식 교체 지점) | (Adapter 바인딩 — Core 산출물의 환경 실현) | 이 파일 1개 |

주:

- 마지막 행의 경로는 **일반형**이다. `<adapter>`(하위 디렉터리 이름 = 구체 어댑터명)는 해당 Adapter Binding 문서가 소유한다. 본 Core 문서는 구체 어댑터명을 명명하지 않는다 (§0, §5).
- `config-schema.md`는 스키마 문서이므로 `framework/core/`에 둔다 (Config는 01 §3.2-B Core Contract 데이터 포맷이고, 스키마 문서는 C-2가 허용하는 "계약·스키마 문서"다). 나머지 프로토콜 문서는 Runtime 호스팅·모듈 시스템 계약(01 §3.1)의 인스턴스이므로 `framework/runtime/`에 둔다.
- 필드·연산의 상세 정본은 인용한 01 § 각각이 유지한다. 본 표는 계약을 재정의하지 않고 § 포인터로 소유를 배정할 뿐이다.
- **표 범위 (DP-V4, v0.5).** 이 표는 **v0.3 산출물** 범위로 유지하며, v0.4·v0.5 산출물의 버전별 소유 경계 기록은 각 버전 핸드오프·검증 리포트 관행이 담당하고(본 표에 버전별 산출물 표를 누적하지 않는다), 실측 파일 목록의 트리 반영은 §8이 담당한다.

---

## §7. Core Contract 불변 조건 (확정 조건 C-1)

확정 조건 C-1을 명문화한다.

- **C-1.** 형태 A → 형태 B 전환 시 Core Contract(01 §3) 변경이 발생하지 않는다. v0.3 문서는 01 §3의 **인스턴스**이며 계약 확장·수정이 아니다.

규칙:

1. 본 구조 규격과 §6의 v0.3 계약 문서들은 전부 01 §3 Core Contract의 **인스턴스**다. 어느 것도 01 §3의 계약 요소(연산·데이터 포맷·불변 규칙)를 재정의·확장하지 않는다.
2. 향후 실행 코드 확장(형태 A → 형태 B)은 §6의 계약 문서가 지정한 01 §3 계약을 **구현**할 뿐, 계약 자체를 수정하지 않는다.
3. 따라서 **Core Contract 변경 0**이 형태 A→B 전환의 불변 조건이다. 교체·확장 시에도 계약 소비자의 참조·규격 변경은 0이다 (01 §3.3 INV-1 교체 가능성과 정합).
4. 이 불변 조건 위반(형태 B가 01 §3 계약을 바꾸어야만 성립하는 경우)이 발견되면, 구현을 진행하지 않고 Advisor에게 보고한다 (상위 규약의 Architecture-Spec 충돌 보고 관행 — 충돌 시 구현하지 않고 상위에 보고). 계약 변경은 01의 버전 상승과 Revision History 기록이 필수다 (Glossary §3.2-G Spec Status: Frozen).

---

## §8. 요약 (경계 한눈에 보기)

```
framework/
├─ core/                         # Core Layer — 계약·스키마 문서 전용 (AI·언어/툴체인 비의존)
│  ├─ structure.md               #   (본 문서) 디렉터리 구조 규격
│  └─ config-schema.md           #   01 §3.2-B Config 스키마
├─ runtime/                      # Runtime Layer — 모듈 시스템·수명주기 프로토콜 문서 (문서 본문 AI·언어/툴체인 비의존)
│  ├─ module-manifest.md         #   01 §3.2-A Module Manifest
│  ├─ module-registry.md         #   01 §3.1-A 등록/해소/교체/해제 규칙
│  └─ lifecycle.md               #   01 §3.1-C Bootstrap/Shutdown
│   # loop·memory·verifier·workflow·plugins/ — Module 구현 디렉터리 (Module 자기완결 경계, 01 §3.2-E 규칙 2)
│   #   문서 본문 AI·언어/툴체인 비의존 (C-3 확장). 형태 A(문서) 실현; 형태 B 시 실행 코드 실현 (§4 C-2)
│   #   계약 정본은 각 Module의 spec 소관(§ 포인터) — 본 Core 문서는 재서술하지 않는다
├─ memory/                       # 실사용 (v0.4) — 정본 specs/04-memory.md·05-lessons.md 소관
│  ├─ module-manifest.md         #   01 §3.2-A Manifest 인스턴스 (Memory Service Provider)
│  ├─ memory-service.md          #   Memory Service Interface (단일 Port) 계약 인스턴스 (04 §3)
│  ├─ memory-store.md            #   Memory Store·인덱스 구조·포맷 (04 §3.2-A/C)
│  └─ lessons.md                 #   Lesson·Best Practice·재발 판정 특화 계약 인스턴스 (05 §3)
├─ verifier/                     # 실사용 (v0.5) — 정본 specs/06-verifier.md 소관
│  ├─ module-manifest.md         #   01 §3.2-A Manifest 인스턴스 (Verifier Provider)
│  ├─ verifier-protocol.md       #   Verify 연산 프로토콜 인스턴스 (06 §3.1)
│  ├─ verification-report.md     #   검증 리포트 스키마 인스턴스 (06 §3.2-A)
│  ├─ rework-instruction.md      #   재작업 지시 포맷 인스턴스 (06 §3.2-D)
│  └─ criteria-catalog.md        #   완료 판정 기준 카탈로그 인스턴스 (06 §3.2-E)
├─ loop/                         # 실사용 (v0.6) — 정본 specs/03-loop.md 소관
│  ├─ module-manifest.md         #   01 §3.2-A Manifest 인스턴스 (Loop Provider)
│  ├─ loop-protocol.md           #   사이클 구동 연산 오케스트레이션 인스턴스 (03 §3.1)
│  ├─ stage-transition-rules.md  #   단계 전이 규칙 인스턴스 (03 §3.1-A)
│  └─ loop-state-record.md       #   루프 상태 기록 포맷 인스턴스 (03 §3.2)
├─ workflow/                     # 실사용 (v0.7) — 정본 specs/07-workflow.md 소관
│  ├─ module-manifest.md         #   01 §3.2-A Manifest 인스턴스 (Workflow Provider)
│  ├─ work-graph.md              #   Work Graph·Task·공통 Failure Report 포맷 인스턴스 (07 §3.2-A/B/E)
│  ├─ decompose-rules.md         #   Decompose 연산 규칙 인스턴스 (07 §3.1-A)
│  ├─ dispatch-protocol.md       #   Dispatch 연산·병렬 디스패치 프로토콜 인스턴스 (07 §3.1-B·§3.2-C)
│  └─ merge-rules.md             #   Merge 연산·병합 결과·충돌 처리 규칙 인스턴스 (07 §3.1-C·§3.2-D)
├─ plugins/                      # 실사용 (v0.8) — 정본 specs/10-plugins.md 소관
│  ├─ module-manifest.md         #   01 §3.2-A Manifest 인스턴스 (Plugins Provider)
│  ├─ plugin-manifest.md         #   Plugin Manifest·공통 Failure Report 포맷 인스턴스 (10 §3.2-A/B)
│  └─ plugin-lifecycle.md        #   설치·활성화·비활성화·제거 연산 규칙 인스턴스 (10 §3.1)
└─ adapters/                     # Adapter Layer — 환경 의존 바인딩 산출물 격리 (복수 Adapter 경계 실재)
   ├─ <adapter>/                 #   첫 번째 Adapter 경계(완전 구현) — 구체 어댑터명은 Adapter Binding 문서 소관
   │  ├─ runtime-binding.md      #   01 §4.1/§4.2 이식 교체 지점 실현
   │  ├─ memory-binding.md       #   Memory 백엔드 바인딩 실현 (04 §4.1)
   │  ├─ verifier-binding.md     #   Verifier 바인딩 실현 (06 §4.1)
   │  ├─ loop-binding.md         #   Loop 바인딩 실현 (03 §4.1/§4.2 이식 교체 지점)
   │  ├─ workflow-binding.md     #   Workflow 바인딩 실현 (07 §4.1/§4.2 이식 교체 지점)
   │  ├─ hooks-binding.md        #   Hooks 바인딩 실현 (08 §4.1/§4.2 이식 교체 지점)
   │  ├─ skills-binding.md       #   Skills 바인딩 실현 (09 §4.1/§4.2 이식 교체 지점)
   │  ├─ plugins-binding.md      #   Plugins 바인딩 실현 (10 §4.1/§4.2 이식 교체 지점)
   │  ├─ agent-binding.md        #   Agent 바인딩 실현 (02 §4.1/§4.2 이식 교체 지점)
   │  ├─ adapter-conformance.md  #   Adapter Interface 커버리지·Conformance 판정 인스턴스 (11 §3)
   │  ├─ harness-binding.md      #   Harness 바인딩 실현 (13 §4.1/§4.2 이식 교체 지점)
   │  ├─ scaffold-binding.md     #   Scaffold 바인딩 실현 (12 §4.1/§4.2 이식 교체 지점)
   │  ├─ scaffold-template/      #   템플릿 실물 — 구조·내용 정본은 Adapter Binding 문서 소관
   │  └─ (백엔드 격리 데이터 — 물리 이름·직렬화 형식은 Adapter Binding 문서 소관, Core 문서 비서술)
   └─ <adapter>/                 #   두 번째 Adapter 경계(최소 구현 Adapter — 11 §3.2-B) — 파일 목록·바인딩 값 정본은 그 Adapter Binding 문서 소관 (내부 파일 비열거)
```

- Core 경계(`core/`·`runtime/`), Module 구현 경계(`{loop,memory,verifier,workflow,plugins}/`), Adapter 경계(`adapters/`)는 서로 물리적으로 비중첩이다 (01 §3.2-E 규칙 3).
- Core 경계와 Module 구현 경계의 문서 본문에는 특정 AI·언어·툴체인 토큰이 0건이다 (INV-4, C-3 및 그 확장, §5). Adapter 경계는 환경 의존 토큰을 격리 보유한다.
- 모든 파일은 자신이 인스턴스화하는 정본 계약(01 §3/§4, 또는 그 위의 Component/Module spec — specs/02·03·04·05·06·07·08·09·10·11·12·13 등)의 인스턴스이며, 형태 B 전환에도 Core Contract 변경은 0이다 (C-1, §7).
