# ARCHITECTURE — Universal Agentic Framework 상위 구조 정본 (라우터)

작성일: 2026-07-07 (v1.3 완전 재저술: 2026-07-09 · v1.4 Solution Design 성숙 루프 개정: 2026-07-13 · v1.5 orchestration Layer 등재: 2026-07-13)
상태: v1.7 — §8 UAF-INV ① 재정의("무수정"[동결] 폐지·UAHF→UAF 승격 이행 완료로 보호 장치 해제·접점 원칙[Project Contract 단일 접점] 존치·불변 번호 ① 유지·①~⑥ 순서/카운트 무변·내용만 재정의; §0·§2.2·§2.5·§6·§10 라이브 본문 정합·사용자 결정 2026-07-17) · §5 `.claude` 거버넌스 분리 명문화(UAF 관리 vs UAHF 하네스·v1.5 이하 논지 무변) · v1.5 orchestration Layer 등재 (§2.1 라우터 표 `orchestration/` 행·§2.3 Agentic Runtime slot 실현 표기·§2.5 의존 방향 1항·§8 UAF-INV ① 병존 주·§11 Non-Goals 실현 표기·최상위 Layer 5→6 정합). v1.4 논지(Solution Design 성숙 루프·라우터 모델·6요소 파이프라인 의미론·UAF-INV ①~⑥·P1~P5·INV-3 무촉·책임 경계표 담당4/비담당5 카운트·Discovery Request 추상) 무변. 직전 Baseline: v1.1 (사용자 승인 2026-07-07) → v1.2.1 구조 이동 (사용자 승인 2026-07-09) → v1.3 완전 재저술 (2026-07-09) → v1.4 성숙 루프 (2026-07-13).
상위 규약: AGENT.md (INV-1)
근거 정본:

- `docs/v1.2.1-context-and-design.md@cd9247b` — v1.2.1 통합 이해 정본. 특히 §3(두 "Layer" 축·"루트=라우터, 각 Layer 독립 ARCHITECTURE"·UAHF=`uahf/` 아래 Runtime Layer 구현체·knowledge는 Layer 아닌 횡단 Base)·§4(Layer 연결=타입 계약 파이프). 본 재저술의 라우터 모델·§0 재프레이밍·knowledge 편입 근거.
- `docs/tier2-claude-override-design.md` — `.claude` Global Default/override 설계 정본. 특히 §2(개념 모델: G/U 정의·dogfooding 이중역할·개념귀속≠물리위치·형태 A/B)·§3(네이티브 로딩 경계)·§4(합성 3연산 ADD/REPLACE/MERGE·12항목 귀속표). §5 `.claude` 절의 근거이며, 상세 계약은 이 정본에 위임한다.
- `uahf/ARCHITECTURE.md` 0.2 (UAHF 정본) — UAF는 UAHF를 늘리지 않고, 접점은 Project Contract 하나뿐이다. UAHF 계약 요소는 § 포인터로만 참조한다.
- `uahf/specs/00-glossary.md` 0.2 (UAHF 용어 정본) — INV-3(Layer 정확히 6개)·용어 네임스페이스 분리의 근거. UAF 신규 용어의 소유 지점은 본 문서 §12다.
- 각 Layer 독립 정본 — `entry/ARCHITECTURE.md`·`discovery/ARCHITECTURE.md`·`planning/ARCHITECTURE.md`·`uahf/ARCHITECTURE.md`·`knowledge/ARCHITECTURE.md`. 라우터인 본 문서가 가리키는 분기 정본이며, 각 Layer의 상세는 해당 정본이 소유한다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-07 | v1.1 Draft | 최초 작성 — `uaf/` 경계 최초 산출물. UAF 상위 구조 정본 신설: 6요소 구조(Entry Layer → Entry Resolution → Project Discovery → Project Contract → UAHF → Execution)·slot 2종(Agentic Runtime 향후·Extension System 기존)·의존 방향 단방향(§2.4)·설계 원칙 9종(§3)·사용자 고정 원칙 P1~P5와 상시 불변 확인 2건(§4)·UAF 불변 UAF-INV 6건(§5)·책임 경계표 P4(§6)·Non-Goals(§7)·UAF 용어 절(§8 — Discovery Request 인터페이스 추상 {mode, inputs, policy} 확정). UAHF 정본 무수정(§ 포인터만·재정의 0)·INV-3 무촉(Entry·Discovery는 UAHF 6-Layer 외부의 UAF 레벨 구조)·특정 AI 실명·모델명·제품 기능명 0(자가 전수 스캔). | Worker (Advisor 위임, v1.1 W1 T1) |
| 2026-07-07 | v1.1 Draft (r2) | § 포인터 오기 1건 정정 — §2.1 Execution 불릿의 핵심 루프 인용 `specs/00-glossary.md §3.2-I` → `§3.2-J`(정본 실측: 핵심 루프(Core Loop)는 §3.2 카테고리 J "컴포넌트 계약 용어" J-11 소속, Glossary line 403; §3.2-I는 "Runtime 계약 용어"로 오기였다). + 동종 결함 전수 재대조(BP-01) — 문서 내 전 § 포인터를 대상 정본 직접 실측 대조, 그 외 오기 0. 본문 그 외 문면 무변경·소유 경계 유지(uaf/ARCHITECTURE.md 1개). | Worker (Advisor 재작업 지시, v1.1 W1 T1 r2) |
| 2026-07-07 | v1.1 Baseline | v1.1 마일스톤 사용자 승인 — 기준선 확정 (CP2 첫 판정 Pass — 충족 15/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-09 | v1.2.1 | uaf/ARCHITECTURE.md → 루트 ARCHITECTURE.md 이관(경로 참조 정합·물리 Layer 매핑 추가). 논지 무변경. | Worker(Advisor 위임, Phase 2) |
| 2026-07-09 | v1.3 | 완전 재저술 — 라우터 모델(각 Layer 독립 ARCHITECTURE 분기·물리 Layer 매핑을 §2 본문 골격으로 승격)·§0 개념 프레이밍 재서술(uaf/ 소멸·신 물리 실재=최상위 5 Layer·UAF=상위 프레임워크/UAHF=Runtime Layer 구현체)·knowledge 횡단 Base 편입(설계 원칙 9종→10종)·.claude Global Default/override 절 신설(tier2 §2·§4 인용)·내부 stale uaf/ 정합. 불변 콘텐츠(UAF-INV ①~⑥·P1~P5·INV-3 무촉·6요소 의미론·책임 경계표·Discovery Request 추상) 논지 보존. 새 설계 결정 창설 0. | Worker(Advisor 위임) |
| 2026-07-09 | v1.3 (정합) | 라우터 내부 정합 — (a) **Entry Resolution 물리 귀속 정정**: §2.1 지도 행·§2.2 태그를 Entry Resolution = `entry/`(정본 `entry/ARCHITECTURE.md`)·Project Discovery = `discovery/`로 정정(spec `entry/specs/01-entry.md` 배치·P1·§12.1과 정합 — 라우터 내부 불일치 해소). (b) 실재 spec(01/02/03) 대상 `(예정)` 마커 **13곳 제거**(§ 포인터 유지). 참조 정합·defect 정정 — 시맨틱 개정 아님·**버전 무상승**, 불변 콘텐츠 논지 보존. | Advisor (T-D1) |
| 2026-07-13 | v1.4 | Solution Design 성숙 루프 반영 (v1.3 마일스톤 W2b) — (Δ1) §2.2 Project Contract 불릿에 Contract 요소 **내부 성숙 루프**(Ready vN → superseding v(N+1)·정본 `planning/specs/04-solution-design.md`·단순하면 스킵) 서술 추가 + "파이프라인은 6요소 그대로다" 명시. (Δ2) §2.2 이중 지위 괄호 소폭 개정 "(Discovery의 산출)" → "(Discovery가 컴파일한 최초 인스턴스와 그 성숙 계보)". (Δ3) §2.1 라우터 표 planning 행 파이프라인 요소 칸 "Project Contract · Solution Design(성숙 루프)"로 갱신(행 수·Layer 수 무변). (Δ4) §10 주석 1문 추가(성숙=Discovery 비수행 활동·planning/ 소관·비담당②와 별개 네임스페이스) — 표·담당4/비담당5 카운트 무변. (Δ5) §12.1 용어 4건 추가(Solution Design·Expert Role·Projection·Contract Maturation). (Δ6) 본 행 append + 머리 상태 라인 v1.4 갱신. 재량: §3 연결 계약 Project Contract 불릿에 성숙 계보 한 구 추가(연결 payload 불변 명시). 6요소 카운트·UAF-INV 6건·P1~P5 문면 무변·새 설계 결정/새 연결 계약 창설 0. | Worker (Advisor 위임, v1.3 W2b) |
| 2026-07-13 | v1.5 | orchestration Layer 등재 (마일스톤 v1.6 「Project Orchestration / Dynamic Agent System」 — 사용자 승인 2026-07-13) — (Δ1) §2.1 라우터 표에 `orchestration/` 1행 추가(정본 `orchestration/specs/05-project-orchestration.md`) + 최상위 물리 Layer 5→6 정합(§0·§1·§2.1 "최상위 5 Layer"→"6 Layer"·`orchestration/` 열거 추가). (Δ2) §2.3 "Agentic Runtime (향후)" slot을 실현 표기로 갱신(orchestration/ Layer가 실현·UAHF Runtime Layer와 별개 네임스페이스 주의 유지). (Δ3) §2.5 의존 방향에 orchestration substrate 소비 1항 append(하향 방향·UAHF 무수정 재사용·UAHF 코드 역참조 0 실측). (Δ4) §8 UAF-INV ① 병존 주(注) 1문 append(substrate 라이브러리 무수정 import는 §2.5 하향 소비이며 '무수정'과 병존 — 규범 문면 무변경). (Δ5) §11 "Layer 연결·오케스트레이션 정식화" 항목을 v1.6 실현 표기로 갱신(원 예약 취지 보존). 본문 규범 문면(UAF-INV ①~⑥·P1~P5·6요소 파이프라인 카운트·책임 경계표 담당4/비담당5) 무변·새 설계 결정/새 연결 계약 창설 0·§9 이력 append-only. | Worker (Advisor 위임, W-A) |
| 2026-07-17 | v1.6 | §5 `.claude` 절에 "UAF 관리 거버넌스 vs UAHF 하네스 거버넌스 (별개)" 명문화 1건 추가 — 루트 `.claude/` Agent 거버넌스(AGENT.md·agents)=UAF-레벨 총괄 관리, UAHF 하네스 거버넌스=그 배포 `.claude/`(scaffold-template 유래)로 분리 서술(4-역할 구조 차용·상호 무참조·self-host 개발/배포 실행 구분). 상위-레벨 UAHF 명칭 잔재 정리(root `.claude/` AGENT.md·agents·CLAUDE.md UAF 재귀속·ROADMAP:24)와 짝. 파이프라인 6요소·UAF-INV·P1~P5·§10/§11 규범 문면 무변·새 설계 결정 0. | Advisor |
| 2026-07-17 | v1.7 | §8 UAF-INV ① 재정의 — "무수정"(동결) 폐지(UAHF→UAF 승격 이행 완료로 보호 장치 해제)·접점 원칙(Project Contract 단일 접점) 존치·불변 번호 ① 유지(재번호 0·①~⑥ 순서·카운트 무변·내용만 재정의). 라이브 본문 정합 8곳: §0 근거 정본(:10)·§0 접점 절 표제(:42)·§2.2 다이어그램 태그(:105)·§2.2 UAHF 불릿(:115)·§2.5 병존 주(:138)·§6 Stable Core(:193)·§8 UAF-INV ① 본문(:228)·§10 주(:253). §9 이력 행·§8 폐지 경위 주석 제외 라벨 잔존 0. P1~P5·6요소 파이프라인·책임 경계표 담당4/비담당5·§ 포인터 참조 원칙 무변·새 설계 결정 0. 사용자 결정 2026-07-17. | Advisor (사용자 결정) |
| 2026-07-17 | v1.7 (정합) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — §0 근거 정본(:8)·§0 라우터 선언(:38)의 삭제 산출물 참조 앵커 전환(`docs/v1.2.1-context-and-design.md@cd9247b`, 2곳). 논지·계약·규범 문면 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-19 | v1.7 (Draft) | §6 설계 원칙 11(책임 있는 자율) 신설 — 비정본 거버넌스: 필수는 Core/Policy 강제·자율은 기본값+사유기록·이탈은 게이트 표면화. §6·§1 카운트 10→11 정합. 사용자 결정 2026-07-19. | Worker (Advisor 위임) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행, uahf/framework/core/structure.md §9 동형. 절 번호는 §9지만 배치는 머리다. 이후 개정은 이 표에 append-only로 기록한다. 표 내 옛 행의 `uaf/ARCHITECTURE.md`·`§3`·`9종` 등 표기는 그 개정 시점의 정확한 이력 기록이므로 그대로 둔다.)

---

## §0. 이 문서의 위치와 정본 경계 (라우터 선언)

- **라우터 정본.** 이 문서는 **UAF(Universal Agentic Framework) 상위 구조의 라우터 정본**(루트 `ARCHITECTURE.md`)이다. 최상위 물리 Layer들의 **지도**를 제공하고, 각 Layer의 독립 `ARCHITECTURE.md`를 § 포인터로 가리키며, **Layer 사이의 관계(연결)만** 서술한다. 각 Layer의 내부 상세는 그 Layer의 독립 정본이 소유한다 (`docs/v1.2.1-context-and-design.md@cd9247b` §3 "루트=라우터, 각 Layer 독립 ARCHITECTURE").

- **신 물리 실재 = 최상위 6 Layer.** 이 저장소의 최상위 물리 구조는 **`entry/ · discovery/ · planning/ · uahf/ · knowledge/ · orchestration/`** 다(`orchestration/`은 v1.6에서 §2.3 Agentic Runtime slot을 실현하며 등재된 6번째 최상위 Layer — 문서버전 v1.5·§2.1). 과거 `uaf/`(별개 네임스페이스 디렉터리)는 v1.2.1 구조 이동에서 물리적으로 **소멸**했고, 그 내용은 위 Layer들로 분산되었다(파이프라인 관계 → 이 라우터, 요소별 → 각 Layer ARCHITECTURE). 따라서 "`uaf/` vs UAHF 별개 디렉터리"라는 과거 프레이밍은 폐기한다.

- **UAF와 UAHF의 관계.** **UAF = 최상위 6 Layer를 아우르는 상위 프레임워크**(프로젝트를 이해 → 계약 → 실행하는 파이프라인 + 실행 lifecycle 오케스트레이션[`orchestration/`, §2.3] + 횡단 knowledge)다. **UAHF(Universal Agentic Harness Framework) = `uahf/` 아래의 Runtime Layer 구현체**다 — 최상위가 아니라 파이프라인 하류에서 실행(Execution)을 담당하는 한 Layer의 구현이다 (context-and-design §3, 사용자 원칙 11). UAF 용어와 UAHF Glossary는 별개 네임스페이스로 유지한다(§12 용어 네임스페이스 분리) — 개념은 유지하되 물리 서술만 재정렬했다.

- **접점 원칙 (Project Contract 단일 접점).** UAF와 UAHF의 유일한 접점은 **Project Contract 하나**다 (UAF-INV ①, §8). 본 문서는 UAHF 계약 요소(`uahf/ARCHITECTURE.md`·`uahf/specs/`·`uahf/framework/`·상위 규약)를 재정의·확장하지 않고 **§ 포인터로만 참조**한다.

- **INV-3 무촉 (핵심 경계 선언).** Entry Layer·Entry Resolution·Project Discovery·Project Contract는 UAHF의 6-Layer 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter, `uahf/specs/00-glossary.md` §3.2-A)에 **새 Layer로 추가되지 않는다**. 이들은 UAHF 6-Layer의 **외부**, 그보다 상위의 **UAF 레벨 구조**다. 따라서 Glossary INV-3("Layer는 정확히 6개다")는 무촉이며, 본 문서는 UAHF Layer 수를 늘리는 어떤 서술도 두지 않는다.
  - 용어 주의: "**Entry Layer**"의 "Layer"는 UAHF Layer 스택의 지층(stratum)이 아니라, UAF 파이프라인의 한 **단계(stage)** 를 가리키는 명칭이다. 또한 최상위 물리 "Layer"(`entry/`·`discovery/`·`planning/`·`uahf/`·`knowledge/`)는 UAF 파이프라인 축의 지도 단위이지 UAHF 수직 스택의 지층이 아니다. UAHF Glossary §3.2-A의 Layer 정의와는 별개 네임스페이스다(§12 용어 네임스페이스 분리).

- **Core 문서 관행.** 본문 전체에 특정 AI 이름·모델명·제품 기능명을 두지 않는다 (`uahf/framework/core/structure.md` §5 C-3 동형). 구체 실현(진입 명령의 물리 형태·직렬화 형식·환경 경로 관례)은 Adapter Binding 소관이며, 필요한 자리에는 일반형 표기와 소관 포인터만 둔다.

- **정본 위임.** 이 라우터는 상위 구조(Layer 지도·Layer 연결·횡단 Base·`.claude` 합성 경계·원칙·불변·경계·용어)만 확정한다. 각 요소의 상세 계약(Entry Resolution 결정 테이블·Discovery State Machine·Contract 스키마·Layer 내부 구조)은 각 Layer의 `ARCHITECTURE.md`와 후속 `<layer>/specs/` 정본이 소유하며, 본 문서는 그 소유 지점을 포인터로만 표기한다.

---

## §1. 목적 (Purpose)

이 문서는 UAF가 **Execution 이전에 어떤 순서로 프로젝트를 이해하고 계약으로 고정하는가**의 상위 구조를 확정하고, 그 구조를 물리 Layer 지도로 라우팅한다.

책임은 다섯 가지다.

- 최상위 6 Layer의 **지도**를 제공하고 각 Layer 독립 정본으로 라우팅한다 (§2).
- UAF 구조 6요소의 **순서와 위상**, 요소 간 **의존 방향**을 단방향으로 명문화한다 (§2).
- Layer 사이를 잇는 **연결 계약**(Discovery Request·Project Contract)을 서술한다 (§3).
- **knowledge 횡단 Base**(§4)와 **`.claude` Global Default/override 합성 경계**(§5)를 선언한다.
- UAF가 따르는 **설계 원칙 11종**·**사용자 고정 원칙 P1~P5**·**불변 규칙 UAF-INV 6건**·**책임 경계**·**용어**를 확정한다 (§6~§12). 특히 후속 병렬 작업의 선행 확정 인터페이스인 **Discovery Request 추상**을 §12에서 고정한다.

이 문서는 상위 구조의 정본(라우터)이다. 각 Layer의 구현·내부 계약을 정의하지 않는다 — 그것은 각 Layer 정본 소관이다.

---

## §2. UAF 구조 — 라우터·6요소·의존 방향 (Router · Structure · Dependency)

### §2.1 라우터 — 최상위 Layer 지도

루트 `ARCHITECTURE.md`는 **라우터**다. 최상위 6 Layer를 가리키고 그 관계만 서술한다. 각 Layer는 **독립 `ARCHITECTURE.md`** 를 가지며 자신의 내부를 스스로 소유한다.

| 파이프라인 요소 (§2.2) | 물리 Layer 디렉터리 | Layer 독립 정본 (분기 포인터) |
|---|---|---|
| Entry Layer · Entry Resolution | `entry/` | `entry/ARCHITECTURE.md` |
| Project Discovery | `discovery/` | `discovery/ARCHITECTURE.md` |
| Project Contract · Solution Design(성숙 루프) | `planning/` | `planning/ARCHITECTURE.md` |
| UAHF | `uahf/` | `uahf/ARCHITECTURE.md` |
| Execution | `uahf/` (실행 단계 — 별도 디렉터리 없음) | `uahf/ARCHITECTURE.md` |
| Project Orchestration · Dynamic Agent Allocation·Model Selection·Artifact 계보·Gate Policy (§2.3 Agentic Runtime slot 실현) | `orchestration/` | `orchestration/ARCHITECTURE.md` (정본 = `orchestration/specs/05-project-orchestration.md`) |
| (횡단) Knowledge Base | `knowledge/` | `knowledge/ARCHITECTURE.md` (§4 — 파이프라인 단계 아님) |

- **라우터의 책임 한계.** 이 표 이상으로 각 Layer 내부를 서술하지 않는다. 라우터는 **어떤 Layer가 있고, 그것들이 어떻게 연결되는가**(§2.2 순서·§2.5 의존 방향·§3 연결 계약)만 다룬다.
- `knowledge/`는 파이프라인 단계가 아니라 **모든 Layer가 Consult하는 횡단 공용 Knowledge Base**다 (§4, 설계 원칙 10, `knowledge/ARCHITECTURE.md`).

### §2.2 6요소 파이프라인 의미론

UAF는 사용자 입력에서 UAHF 실행에 이르는 파이프라인을 다음 **6요소**로 정의한다. 순서는 위(입력)에서 아래(실행)로 흐르며, 각 요소는 §2.1 지도의 물리 Layer에 대응한다.

```
Entry Layer          — UAF 공식 진입점 (사용자 입력 수용)                 [entry/]
      │
      ▼
Entry Resolution     — 진입 판별 → Discovery Request 산출 (Discovery 비수행) [entry/]
      │  (Discovery Request: {mode, inputs, policy} — §12에서 확정)
      ▼
Project Discovery    — Discovery Request(+증거) → Project Contract 산출 (Compiler) [discovery/]
      │
      ▼
Project Contract     — UAF↔UAHF 공식 Stable Contract (Public API) — 유일 접점  [planning/]
      │  (UAHF의 선택 입력 — 부재 시 기존 UAHF 운용 불변)
      ▼
UAHF                 — 기존 UAHF 6-Layer Framework (본 문서 § 포인터 참조 대상) [uahf/]
      │
      ▼
Execution            — UAHF 핵심 루프 구동 (위임 → 구현 → 검증 → 승인)        [uahf/]
```

- **Entry Layer** — UAF의 공식 진입점. 사용자 입력을 수용하는 추상 연산이다. 물리 실현(진입 명령의 형태)은 Adapter 소관이다 (AI-Agnostic, §6). 상세 정본: `entry/ARCHITECTURE.md`·`entry/specs/01-entry.md`.
- **Entry Resolution** — Entry Layer가 수행하는 유일한 연산. 명시 진입과 Workspace Evidence를 평가해 **Discovery Request**를 산출한다. Discovery를 직접 수행하지 않는다 (P1, UAF-INV ④).
- **Project Discovery** — Discovery Request를 입력으로 **Project Contract를 산출하는 Compiler**다 (P2). 어떤 Discovery Strategy를 쓰든 결과는 항상 동일한 Project Contract다 (Strategy Invariance, UAF-INV ③). 상세 정본: `discovery/ARCHITECTURE.md`·`discovery/specs/02-discovery.md`.
- **Project Contract** — UAF와 UAHF의 **공식 Stable Contract(Public API)**이자 **유일한 접점**이다 (P3, UAF-INV ①). UAHF에는 **선택 입력**으로 주어진다 — 부재 시 UAHF는 기존 방식으로 운용된다(하위 호환). Contract 요소 내부에서, Ready 인스턴스 vN은 프로젝트 복잡도에 따라 Solution Design(planning/ 소유, 정본 `planning/specs/04-solution-design.md`)에 의해 superseding 인스턴스 v(N+1)로 성숙될 수 있다(단순하면 스킵 — vN이 곧 소비 대상). 파이프라인은 6요소 그대로다. 상세 정본: `planning/ARCHITECTURE.md`·`planning/specs/03-project-contract.md`.
- **UAHF** — 기존 Universal Agentic Harness Framework 전체(6-Layer + Cross-cutting Memory Service, `uahf/ARCHITECTURE.md` §5·§5.1). 본 문서는 이를 § 포인터로만 참조한다.
- **Execution** — UAHF가 Project Contract(있으면)를 참조하여 핵심 루프(Core Loop: 위임 → 구현 → 검증 → 승인, `uahf/specs/00-glossary.md` §3.2-J 핵심 루프)를 구동하는 실행 단계다.

**Project Contract의 이중 지위 주의.** Project Contract는 (i) 파이프라인의 한 요소(Discovery가 컴파일한 최초 인스턴스와 그 성숙 계보)이면서 동시에 (ii) UAF↔UAHF의 계약 접점이다. 데이터 계약인 **Discovery Request**는 Entry Resolution의 출력이자 Project Discovery의 입력인 요소 간 인터페이스이며, 그 추상은 §12에서 확정된다. 요소 간 연결 계약의 통합 서술은 §3에 둔다.

### §2.3 slot (설계 제외 — 자리 표기만)

다음 두 요소를 UAF 구조상 표기한다. **Extension System**은 자리(slot)만 표기하고 본 문서에서 설계하지 않으며, **Agentic Runtime**은 v1.6에서 `orchestration/` Layer로 실현되어 정본 포인터로 라우팅한다.

- **Agentic Runtime — `orchestration/` Layer가 실현 (v1.6 Baseline, 2026-07-13).** UAF 레벨 에이전트 실행 기반의 자리이며, 마일스톤 v1.6 「Project Orchestration / Dynamic Agent System」이 이를 UAF 레벨 신규 최상위 Layer `orchestration/`으로 실현했다 — Discovery·Solution Design 산출물을 인수해 프로젝트 완료까지 동적 작업 그래프·게이트·역할/모델 할당·산출물 계보를 무인 조율하고 UAHF를 execution substrate로 소비한다. 정본 = `orchestration/specs/05-project-orchestration.md` · 개관 = `orchestration/ARCHITECTURE.md` · 라우터 표 §2.1. (주의: UAHF의 Runtime Layer, `uahf/specs/00-glossary.md` §3.2-A와는 **별개 네임스페이스**다 — §12.)
- **Extension System (기존)** — UAHF의 기존 확장 서브시스템(Hooks / Skills / Plugins, `uahf/specs/00-glossary.md` §3.2-D)을 가리키는 자리. UAF는 이를 재설계하지 않으며, § 포인터로만 참조한다. 설계 제외 (Non-Goals, §11).

### §2.4 UAF 레벨 위상 (INV-3 무촉 재확인)

§2.2의 6요소 중 Entry Layer·Entry Resolution·Project Discovery·Project Contract는 **UAHF 6-Layer 스택의 외부**에 위치한다. 이들은 UAHF Layer를 늘리지 않고, UAHF의 수직 스택(Presentation → Workflow → Agent → Runtime → Core → Adapter)에 편입되지도 않는다. UAHF와 Execution은 파이프라인의 하류에서 **기존 그대로** 소비되는 요소다. 이로써 Glossary INV-3("Layer는 정확히 6개다")는 UAF 신설로도 무촉이다. 최상위 물리 Layer(§2.1)는 UAF 파이프라인 축의 지도 단위이며 UAHF 수직 스택과 직교한다(두 "Layer" 축, context-and-design §3).

### §2.5 의존 방향 (Dependency Direction)

UAF의 요소 간 의존은 **위→아래 단방향**이다. 하위 요소는 상위 요소를 알지 못하며, 상위 요소만이 하위 요소를 안다.

- **UAHF는 Entry·Entry Resolution·Project Discovery를 모른다.** UAHF가 아는 것은 자신에게 주어질 수 있는 선택 입력, 즉 Project Contract 하나뿐이다. Entry·Discovery는 UAHF의 인지 밖(상류)에 있다.
- **Entry는 Project Contract를 직접 만들지 않는다 (P1).** Entry Layer의 책임은 **Entry Resolution만**이다 — 진입을 판별해 Discovery Request를 산출하는 데서 멈춘다. Project Contract를 생성하는 것은 Project Discovery의 책임이며, Entry는 Discovery를 수행하지 않는다 (UAF-INV ④).
- **의존의 폐쇄성.** Discovery는 Entry로 역참조하지 않고, Contract는 Discovery 내부 개념(질문·전략·예산)으로 역참조하지 않는다. 이 폐쇄성이 각 요소의 교체 가능성을 성립시킨다 (Strategy Invariance의 구조 측 조건, §8 UAF-INV ③).
- **orchestration은 UAHF를 substrate로 소비한다 (v1.6 — 하향 방향).** UAF 레벨 상위 컴포넌트 `orchestration/`(§2.3 Agentic Runtime slot 실현)은 하위 UAHF의 중립 실행 모듈을 라이브러리로 **무수정 재사용**(import)하여 실행을 위임한다. 이는 "상위만이 하위를 안다"의 허용 방향이며(UAHF는 orchestration을 모른다 — UAHF 중립 코드·정본 spec의 orchestration 역참조 0 실측), UAF-INV ①(접점 원칙)과 병존한다(§8). 정본: `orchestration/specs/05-project-orchestration.md` §0·§2.2.

의존 방향을 단방향으로 고정함으로써, 상위 요소(Entry·Discovery)의 교체가 하위 요소(UAHF·Execution)에 파급되지 않는다. 파급을 차단하는 유일 접점이 Project Contract다.

---

## §3. Layer 연결 계약 (Inter-Layer Connection Contracts)

Layer는 **입력 계약을 소비하고 출력 계약을 생산**함으로써 연결된다. 그 계약이 이음새다. 라우터는 이미 확정된 두 연결 계약의 **위상**만 서술하며, 각 계약의 스키마 상세는 소유 정본에 위임한다.

```
entry ──[Discovery Request]──▶ discovery ──[Project Contract]──▶ planning/uahf ──▶ execution
       {mode, inputs, policy}              (Discovery 산출·Stable Contract·유일 접점)
```

- **Discovery Request** — Entry Resolution의 출력이자 Project Discovery의 입력인 데이터 계약(3요소 {mode, inputs, policy}). 이 인터페이스 추상은 본 라우터 §12.2에서 확정되며, 후속 병렬 작업(`entry/specs/01-entry.md`·`discovery/specs/02-discovery.md`)의 선행 확정 인터페이스다.
- **Project Contract** — Project Discovery의 출력이자 UAHF의 **선택 입력**인 공식 Stable Contract(Public API). UAF↔UAHF의 유일 접점이다 (P3, UAF-INV ①②). planning/ 성숙 루프(Solution Design, §2.2)로 최초 인스턴스가 superseding 계보를 이룰 수 있으나, 연결 payload(Contract 스키마)는 불변이다. 스키마·버저닝·UAHF Interface 상세 정본: `planning/specs/03-project-contract.md`.
- **연결의 성질 (라우터 수준 선언).** 연결 payload는 **타입 계약(schema)**이지 서술(narrative)이 아니다 — 그래야 LLM 교체·Layer 독립 실행 시 다음 Layer가 안정적으로 파싱·소비한다(AI-Agnostic·Layer별 LLM 선택과 직결, context-and-design §4). 계약이 파일로 남으므로 앞 Layer 없이 계약만 있으면 뒤 Layer가 실행 가능하다(독립 실행) — Contract가 UAHF의 선택 입력이라 uahf 단독 실행이 이미 설계에 내장되어 있다(UAF-INV ①).
- **정본 위임·범위 경계.** Layer 계약 저장 위치(대상 프로젝트 `.claude/`)·호출 표면(`uaf:<layer>`)·체이닝/오케스트레이션의 **정식화**는 본 라우터가 확정하지 않는다 — 그것은 각 Layer 정본 및 후속 Layer 연결/오케스트레이션 트랙 소관이다(Non-Goals, §11; context-and-design §4·§5·§8). 라우터는 이미 확정된 두 계약의 위상만 고정한다.

---

## §4. knowledge — 횡단 Knowledge Base (Cross-cutting)

`knowledge/`는 **파이프라인 단계가 아니다**. 모든 Layer가 Consult하는 **횡단 공용 Knowledge Base**다 (context-and-design §3·§4, 사용자 원칙 10).

```
knowledge ◀──Consult── 모든 Layer   (횡단 — 파이프라인 파이프 아님)
```

- **위상.** knowledge는 §2.2의 6요소 순서에 들어가지 않는다. Entry·Discovery·Planning·UAHF·Execution 어느 Layer든 필요 시 knowledge를 회수(Consult)하되, knowledge는 파이프라인 payload를 앞뒤 Layer로 흘려보내지 않는다(파이프가 아님). 세 메커니즘을 혼동하지 않는다 — **knowledge = 공유 지식(횡단)** / **Layer 연결 계약 = 파이프(파이프라인 축, §3)** / session handoff = 시간축 연속.
- **내용.** 장기 공유 지식(Lessons·패턴 등)을 담는 공용 Base다. 표면 구조와 각 Layer의 Consult 경로 상세 정본: `knowledge/ARCHITECTURE.md`.
- **UAHF Memory Service와의 관계.** UAHF 내부에는 6-Layer를 관통하는 자체 Cross-cutting **Memory Service**(단일 Port, `uahf/ARCHITECTURE.md` §5.1)가 있다. 그 UAHF 내부 횡단 서비스와 UAF 레벨 횡단 `knowledge/` Base의 결합 상세는 UAHF 정본·`knowledge/ARCHITECTURE.md` 소관이며, 본 라우터는 knowledge가 UAF 레벨 횡단 Base라는 위상만 선언하고 재정의하지 않는다.

---

## §5. `.claude` — Global Default(G) vs override(U) 합성 경계

이 저장소는 UAF **도구를 개발하는 저장소**이면서 동시에 **UAF를 자신에게 적용하는 dogfooding 프로젝트**다. 그래서 루트 `.claude/`가 두 성격을 겸재한다. 그 개념 경계와 합성 계약을 이 절에서 선언하며, **정의·명찰·합성 3연산·형태 A/B·귀속표의 상세 정본은 `docs/tier2-claude-override-design.md` §2(개념 모델)·§4(합성 3연산·12항목 귀속표)에 위임**하고 여기서 재정의하지 않는다(인용).

- **Global Default (G) = 루트 `.claude/`.** UAF 도구가 설치 시 배포하는 **무상태·프로젝트 비의존 기본값**(공통 Agent 역할 body·공통 진입 명령·프로젝트 비의존 레퍼런스·공통 규약). 어떤 프로젝트에 설치되든 동일하게 배포되는 뼈대다 (tier2 §2.1).
- **override (U) = `<layer>/.claude/`.** Global Default의 특정 요소를 좁은 문맥에서 재정의하는 **델타(차이만)**. 전체 복제가 아니라 "무엇이 GD와 다른가"만 담는다 (tier2 §2.1).
- **합성.** `유효 .claude = GD ⊕ Layer override`. `⊕`는 **합성 3연산 — ADD(override-only 파일 추가) / REPLACE(같은 상대경로 파일 통째 교체) / MERGE(선언 필드만 override, body는 GD 상속)** 로 실현된다 (tier2 §4.1 정본).
- **개념 귀속 ≠ 물리 위치.** "이 요소가 G인가 U인가"(귀속)와 "지금 디스크 어디에 두는가"(위치)는 다르다. 귀속은 명찰로 확정하고(형태 A), 물리 재배치는 형태 B가 존재할 때 수행한다 — 둘의 어긋남은 결함이 아니라 형태 A/B 분리의 정상 상태다 (tier2 §2.3·§2.4).
- **환경 네이티브 로딩 경계 (정직한 제약).** 실행 환경은 **루트 `.claude/`만** 네이티브로 로드한다. 하위 `<layer>/.claude/` override는 환경이 자동 소비하지 않는 **UAF 논리 구성물**이지 환경 기능이 아니다. 따라서 override의 참된 발화(GD를 델타로 덮어 유효 설정을 만드는 `⊕` 합성)는 **형태 B(합성·스캐폴드)** 를 요구한다 (tier2 §3). 형태 B와 그 Open Questions는 후속 트랙 소관이다(Non-Goals, §11).
- **UAF 관리 거버넌스 vs UAHF 하네스 거버넌스 (별개 — 혼동 방지).** 이 repo 루트 `.claude/AGENT.md`·`agents/*`는 **UAF-레벨 총괄 관리 에이전트**(UAF 프레임워크를 개발·감독)의 자립 정본이다. 이와 **별개로** UAHF 하네스는 자기 에이전트 거버넌스를 가지며, 그 실물은 하네스가 소비 프로젝트에 설치하는 `.claude/`(`uahf/framework/adapters/claude/scaffold-template/dot-claude/` 유래·UAHF 명)다. 하네스 spec(`uahf/specs/02-agent`·`13-harness` Minimal Composition)이 요구하는 "상위 규약 `.claude/AGENT.md`"는 **그 하네스 배포 거버넌스**를 가리킨다. 둘은 같은 4-역할 구조를 차용하되 **별개이며 서로 참조하지 않는다** — UAF가 UAHF를 self-host로 개발하고(개발은 UAF 관리 거버넌스를 따름), UAHF는 자기 배포 거버넌스로 런타임 실행한다. 역사적으로 이 둘이 루트에서 겸재해 매 세션 혼동을 유발했던 것을 분리·명문화한다.
- **UAF-level 거버넌스 form-B 스크립트의 물리 홈 = 저장소 루트 `adapters/claude/`.** 루트 `.claude/`의 UAF-level 에이전트(`AGENT.md`·`agents/*`)를 뒷받침하는 **결정적 실행 스크립트**(예: Verifier의 VT-1 산출물 존재·VT-4 경계 전수 스캔 체커)는, 환경이 로드하는 **설정 디렉터리 `.claude/`가 아니라** 저장소 루트 `adapters/claude/`에 둔다. `<layer>/adapters/claude/`(예 `entry/adapters/claude/entry_resolve.py`) 패턴을 **레이어 없는 UAF 거버넌스 루트**에 동형 적용한 것으로, 설정(config)과 실행 스크립트(script)를 분리한다. 이 스크립트는 `agents/verifier.md`의 VT 계약(형태 A)을 **결정적 실행(entry-resolve 동형 form-B)** 으로 승격한 것이며, 이 절 위 항목의 **override 합성 form-B(§11 후속 유보)와는 다른 의미의 form-B**다(용어 중복 주의). 하류 `uahf/framework/adapters/claude/`에는 두지 않는다(과거 오배치 결함 재발 금지). 이 스크립트는 config가 아니므로 tier2 §4.2 12항목 귀속표(루트 `.claude/` config 항목)에 들어가지 않는다.

---

## §6. 설계 원칙 (Design Principles — 11종)

UAF는 다음 11종 원칙을 따른다. UAHF와 동형인 원칙은 UAHF 정본을 § 포인터로 참조하며 재정의하지 않는다.

1. **AI-Agnostic** — UAF는 특정 AI 모델·실행 환경에 종속되지 않는다. Entry·Discovery의 물리 실현은 Adapter 소관이다 (`uahf/ARCHITECTURE.md` §3.1 동형 원칙을 UAF 레벨에 적용).
2. **Stable Contract** — Project Contract는 장기 호환을 유지하는 공식 계약(Public API)이다. Discovery 내부 변경과 독립적으로 안정을 유지한다 (P3, §7).
3. **Stable Core** — UAHF는 안정 코어(Core)이며, UAF는 이를 Contract 단일 접점으로 감싼다. UAF와 UAHF의 접점은 Project Contract 하나다 (UAF-INV ①, §8).
4. **Layer Separation** — Entry·Resolution·Discovery·Contract·UAHF·Execution은 서로 독립된 관심사로 분리된다. 한 요소의 내부 변경이 다른 요소의 규격으로 새지 않는다 (`uahf/ARCHITECTURE.md` §3.2 Modular 동형).
5. **Dependency Direction** — 의존은 위→아래 단방향이다. 하위는 상위를 모른다 (§2.5).
6. **Event Driven** — Discovery의 상태 전이는 Event로만 일어나고, 관측 지표(Metrics)는 그 Event에서 파생된다. (전이·이벤트·지표의 상세 정본은 `discovery/specs/02-discovery.md` 소관 — 본 문서는 원칙만 선언한다.)
7. **Capability First** — Strategy·Entry의 확장 대상은 고정 열거가 아니라 **Capability 선언**으로 선택된다. 신규 능력은 선언을 등록하면 참여한다.
8. **Policy as Data** — 진입 판별의 결정 테이블, Discovery의 임계값·예산·종료 규칙은 코드가 아니라 **데이터(Policy)**다. 정책 변경이 엔진 변경을 요구하지 않는다.
9. **Future Extensibility** — 신규 Entry·Strategy·Runtime은 Layer·엔진 변경 없이 **Registry 행·Policy 데이터 추가만으로** 확장된다. Framework 전체를 다시 쓰지 않는다 (`uahf/ARCHITECTURE.md` §8 동형 지향을 UAF 레벨에 적용).
10. **Knowledge Consult (횡단)** — `knowledge/`는 파이프라인 단계가 아니라 **모든 Layer가 Consult하는 횡단 공용 Knowledge Base**다. 어느 Layer든 knowledge를 회수해 결정을 뒷받침하되, knowledge는 파이프라인 payload를 흘려보내지 않는다 (§4, context-and-design §3·§4, `knowledge/ARCHITECTURE.md`).
11. **책임 있는 자율 (Accountable Autonomy).** 자율을 주되 **침묵 이탈**을 금한다. (a) 빠지면 안 되는 것(필수 산출·전 영역 커버·불가침 절차)은 비정본 부록이 아니라 **Core·Policy·게이트로 강제**한다 — 비정본 부록은 참고 문서일 뿐 강제 근거가 아니다. (b) 남은 자율은 **Policy 기본값 + 이탈 시 사유 기록**이다(silentOmission 금지). (c) 이탈·제외는 **사용자 게이트에서 일괄 표면화·확인**한다(고임팩트는 즉시). "비정본=선택=조용히 skip"을 폐기한다(운영 정본: `.claude/CLAUDE.md` §비정본 거버넌스).

---

## §7. 사용자 고정 Architecture 원칙 (P1~P5)

다음 5건은 사용자가 고정한 UAF Architecture 원칙이며, 본 문서의 정본 문면이다. 후속 전 산출물이 이를 훼손해서는 안 된다.

- **P1 — Entry = Entry Resolution만.** Entry Layer는 UAF 공식 진입점으로서 사용자 입력으로 진입 종류를 판별하고 **Entry Resolution만 담당**한다. Discovery를 수행하지 않으며, 출력은 Discovery Request까지다 (§2.5, UAF-INV ④).
- **P2 — Discovery = Project Contract를 생성하는 Compiler.** Project Discovery는 단일 기능이 아니라 **Compiler**다. 어떤 Discovery Strategy를 쓰든 결과는 항상 **동일한 Project Contract**다 (**Strategy Invariance**, UAF-INV ③). Strategy는 교체 가능한 증거 수집 Front-end이고, Contract 산출 형식은 단일 타깃이다.
- **P3 — Project Contract = UAF↔UAHF 공식 Stable Contract(Public API).** Project Contract는 UAF와 UAHF를 잇는 **공식 안정 계약**이다. Discovery는 교체 가능하되 Contract는 장기 유지된다. UAF와 UAHF의 접점은 이 계약 하나뿐이다 (UAF-INV ①②).
- **P4 — Discovery 책임 경계.** Project Discovery가 담당하는 것과 담당하지 않는 것을 명확히 가른다. 담당 4건·비담당 5건의 정본 경계표는 §10에 둔다.
- **P5 — 설계 순서 = Layer → Workflow → Module → Contract.** UAF의 설계는 상위 구조(Layer)를 먼저 고정하고, 그다음 오케스트레이션(Workflow), 모듈 구성(Module), 마지막에 계약 상세(Contract)를 고정하는 순서로 진행한다.
  - **결정 기록.** Contract의 지위(공식 Stable Contract)와 스키마 안정성 불변은 상위 구조(Layer 단계)에서 선언되므로 인터페이스 방향성은 선행 확보되고, Contract의 상세 스키마는 마지막 단계에서 고정한다. 이 설계 순서는 사용자 고정 원칙(P5)이며, 방법론 상세는 정본이 아니라 비정본 부록 소관이다 (Non-Goals, §11; UAF-INV ⑥).

### §7.1 상시 불변 확인 2건

다음 2건은 후속 모든 산출물이 통과해야 하는 상시 확인 항목이다. 통과하지 못한 산출물은 승인 대상이 아니다.

- **① Project Discovery는 단일 기능이 아니라 Project Contract를 생성하는 Compiler다.** 산출물은 Discovery를 **언제든 교체 가능하게** 유지해야 한다 — Strategy·Discovery 내부 개념(질문·전략·예산)이 Contract 코어 스키마나 UAHF 접점으로 새어나가서는 안 된다 (P2, UAF-INV ②③).
- **② Project Contract는 UAF↔UAHF 공식 Stable Contract(Public API)다.** 장기 호환성 규칙(스키마 버전 규율·소비자의 관용적 읽기·필드 제거 금지)이 훼손되어서는 안 된다. 규칙의 상세 정본은 `planning/specs/03-project-contract.md`가 소유하며, 본 문서는 지위와 원칙만 선언한다 (P3, UAF-INV ①②).

---

## §8. UAF 불변 (UAF-INV — 6건)

UAF는 어떤 구현·확장에서도 다음 6건을 유지한다.

- **UAF-INV ①** — **접점 원칙 (Project Contract 단일 접점).** UAF와 UAHF의 접점은 **Project Contract 하나뿐**이다. UAHF 계약 요소는 재정의·복제 없이 **§ 포인터로만 참조**하며, Contract 소비는 UAHF spec의 연산·필드·불변을 변경하지 않는다(정식 등재는 확장 포인트). (주: `orchestration/` Layer의 substrate 소비(step-host 라이브러리 무수정 import)는 §2.5 하향 방향의 소비이며 본 불변과 병존한다 — 2026-07-13 사용자 결정·v1.6. 구 문면 "UAHF 정본 무수정"(동결)은 승격 이행기의 보호 장치로 도입되었다가 이행 완료로 폐지되었다 — 2026-07-17 사용자 결정.)
- **UAF-INV ②** — **Discovery 교체 가능·Project Contract 교체 불가.** Project Discovery(및 그 Strategy)는 언제든 교체될 수 있으나, Project Contract의 스키마는 안정성을 유지한다(교체 불가). 안정 계약이 교체 가능한 생산자를 흡수한다.
- **UAF-INV ③** — **Strategy Invariance.** 어떤 Discovery Strategy를 쓰든 산출 결과는 항상 **동일한 Project Contract**(동일 스키마·동일 완결 기준)다. Front-end가 바뀌어도 출력 계약은 불변이다.
- **UAF-INV ④** — **Entry는 Discovery를 수행하지 않는다.** Entry Layer의 책임은 Entry Resolution까지이며, Discovery Request를 산출하는 데서 멈춘다. Contract 생성은 Project Discovery의 책임이다.
- **UAF-INV ⑤** — **확정 게이트 = 사용자 승인 (Preserve Human Authority).** Project Contract가 Execution Ready로 확정되는 게이트는 **사용자 승인**이다. 사용자 승인 없이 Ready 종단에 도달하지 않는다.
- **UAF-INV ⑥** — **Framework는 특정 방법론을 모른다.** UAF는 특정 발견·설계 방법론을 알지 않는다. 방법론은 교체 가능한 **Strategy Provider**만이 안다. 방법론 지식이 Framework 정본으로 새지 않는다.

---

## §10. 책임 경계표 (Responsibility Boundary — P4)

Project Discovery가 **담당하는 것(4)**과 **담당하지 않는 것(5)**의 정본 경계다. 비담당 5건은 하류(UAHF 및 그 Execution)의 책임이며, Discovery는 Project Contract를 산출한 지점에서 멈춘다.

| 구분 | 항목 |
|---|---|
| **담당 (4)** | ① 프로젝트 이해 (대상 프로젝트의 의도·요구·제약·리스크·방향 파악) |
| | ② Discovery 수행 (증거 수집·확신 판정·적응적 진행) |
| | ③ Execution Ready 판단 (계약 완결성·확신·사용자 승인의 종단 판정) |
| | ④ Project Contract 생성 (단일 타깃 형식으로의 컴파일) |
| **비담당 (5)** | ① Agent 실행 (UAHF Agent Layer 소관) |
| | ② Planning (구현 계획·작업 분해 — UAHF Advisor/Planner 소관) |
| | ③ Workflow 실행 (분해·병렬 디스패치·병합 — UAHF Workflow Layer 소관) |
| | ④ Memory Consult (기억 회수 — UAHF Memory Service 소관) |
| | ⑤ UAHF Execution (핵심 루프 구동 — UAHF 하류 소관) |

주: 비담당 5건은 전부 **하류 UAHF의 책임**이다. Discovery가 이들을 수행하지 않음으로써 의존 방향(§2.5)과 접점 원칙(UAF-INV ①)이 함께 성립한다. 비담당 항목의 상세 계약 정본은 각 UAHF spec(`uahf/specs/02-agent.md`·`uahf/specs/07-workflow.md`·`uahf/specs/04-memory.md` 등)이 소유하며, 본 표는 § 포인터로만 경계를 가른다. Contract 성숙(Solution Design)은 Discovery가 수행하지 않는 활동으로서 planning/ 소관이다(정본 `planning/specs/04-solution-design.md`) — 비담당②의 UAHF 구현 Planning과는 별개 네임스페이스다.

---

## §11. Non-Goals

UAF 상위 구조 정본(이 라우터)은 다음을 **설계하지 않는다**.

- **Agent Runtime 설계 제외** — 에이전트 실행 기반은 UAHF Agent/Runtime Layer 소관이며, UAF는 이를 재설계하지 않는다.
- **Memory 설계 제외** — 기억의 기록·회수는 UAHF Memory Service(Cross-cutting) 소관이다 (`uahf/ARCHITECTURE.md` §5.1). UAF 레벨 `knowledge/` 횡단 Base의 내부 표면은 `knowledge/ARCHITECTURE.md` 소관이다(§4).
- **Execution Engine 설계 제외** — 핵심 루프 구동은 UAHF 하류 소관이다.
- **Workflow Engine 설계 제외** — 작업 분해·오케스트레이션은 UAHF Workflow Layer 소관이다.
- **Extension System 설계 제외** — UAHF의 기존 확장 서브시스템(Hooks/Skills/Plugins)은 자리(slot)로만 표기하고 재설계하지 않는다 (§2.3).
- **`.claude` 형태 B 설계 제외** — Global Default/override의 물리 합성(스캐폴드/설치기)과 그 Open Questions는 `docs/tier2-claude-override-design.md`가 관장하는 후속 형태 B 트랙 소관이다. 이 라우터는 개념 경계와 합성 계약의 위상만 선언한다(§5).
- **Layer 연결·오케스트레이션 정식화 (오케스트레이션 실현 · 연결 정식화 잔여).** 오케스트레이션 정식화는 마일스톤 v1.6 「Project Orchestration / Dynamic Agent System」이 `orchestration/` Layer로 **실현**했다(정본 `orchestration/specs/05-project-orchestration.md`·§2.1·§2.3 — 프로젝트 완료까지 동적 작업 그래프·게이트·역할/모델 할당·산출물 계보의 무인 조율). 잔여인 Layer 계약 저장 관례·`uaf:<layer>` 호출 표면·체이닝의 정식 spec화는 계속 후속 트랙 소관이다(§3, context-and-design §4·§5·§8).

다음은 **확장 포인트로만** 열어두고 본문에서 설계하지 않는다.

- **Discovery 실행 호스팅** — Discovery를 어느 실행 주체가 호스팅하는가는 **역할 추상까지만** 정의하고, 물리 호스팅은 설계하지 않는다.
- **Discovery의 knowledge 활용** — Discovery가 UAF 레벨 `knowledge/` 또는 UAHF Memory를 회수·활용하는 경로는 **확장 포인트로만** 표기하고, 본문에서 설계하지 않는다.

---

## §12. UAF 용어 (Glossary — 네임스페이스 분리)

UAF 신규 용어의 **소유 지점**은 이 절(및 각 Layer의 `<layer>/specs/` 정본)이다.

- **네임스페이스 분리.** UAF 용어는 UAHF Glossary(`uahf/specs/00-glossary.md`)에 신설·병합하지 않는다. 같은 단어가 양쪽에서 쓰이면(예: "Layer" — §0 용어 주의, "Runtime" — §2.3, "Policy") **네임스페이스로 구분**한다. UAHF 용어는 Glossary 정본을 § 포인터로 참조하고 재정의하지 않는다.
- **향후 분권.** 아래 용어 중 상세 계약을 요하는 항목의 정본은 각 Layer `<layer>/specs/`가 이어받는다. 본 절은 상위 구조 수준의 정의와, **선행 확정이 필요한 인터페이스 추상**을 고정한다.

### §12.1 용어 정의

- **Entry** — UAF 공식 진입점. 사용자 입력을 수용하는 추상 연산이다. 물리 실현(진입 명령의 형태)은 Adapter 소관이다. 상세 정본: `entry/specs/01-entry.md`.
- **Entry Resolution** — Entry가 명시 진입과 Workspace Evidence를 결정 테이블(Policy as Data)로 평가해 **Discovery Request**를 산출하는 연산. Discovery를 수행하지 않는다 (P1, UAF-INV ④). 상세 정본: `entry/specs/01-entry.md`.
- **Discovery Request** — Entry Resolution의 출력이자 Project Discovery의 입력인 데이터 계약. 3요소 구조(§12.2에서 확정).
- **Project Discovery** — Discovery Request(+증거)를 입력으로 **Project Contract를 산출하는 Compiler**. 상세 정본: `discovery/specs/02-discovery.md`.
- **Discovery Dimension** — Discovery가 확신을 측정하는 축. 상세(차원 목록·판정)의 정본: `discovery/specs/02-discovery.md`.
- **Confidence** — Discovery Dimension별 확신도. 상세(척도·근거 등급·임계)의 정본: `discovery/specs/02-discovery.md`.
- **Question Budget** — 질문의 총량·차원별 예산. Policy as Data. 상세 정본: `discovery/specs/02-discovery.md`.
- **Execution Ready** — Discovery의 종단 판정. 계약 완결성 ∧ 확신 ∧ **사용자 승인**의 결합이다 (UAF-INV ⑤). 상세(판정식·종단 종류)의 정본: `discovery/specs/02-discovery.md`.
- **Project Contract** — UAF↔UAHF 공식 **Stable Contract(Public API)**. Project Discovery의 산출이자 UAHF의 선택 입력이다 (P3, UAF-INV ①②). 상세(스키마·버저닝·UAHF Interface)의 정본: `planning/specs/03-project-contract.md`.
- **Strategy / Strategy Provider** — 교체 가능한 증거 수집 Front-end와 그 제공자. Capability 선언 기반으로 선택된다 (Capability First). 특정 방법론은 이 Provider만이 안다 (UAF-INV ⑥). 상세 정본: `discovery/specs/02-discovery.md`.
- **Knowledge Base (`knowledge/`)** — 모든 Layer가 Consult하는 UAF 레벨 횡단 공용 지식 Base. 파이프라인 단계가 아니다 (§4). 상세 정본: `knowledge/ARCHITECTURE.md`.
- **Solution Design** — Ready 종단 Contract 인스턴스를 입력으로, 프로젝트 복잡도에 따라 동적으로 구성된 전문가 역할 협업으로 솔루션 설계 결정을 성숙시켜, 사용자 승인 하에 superseding Contract 인스턴스를 재발행하는 UAF 레벨 활동. 소유 = `planning/`. UAHF 구현 Planning(§10 비담당②)과 별개 네임스페이스다. 상세 정본: `planning/specs/04-solution-design.md`.
- **Expert Role** — Solution Design에서 Capability 선언으로 정의되는 논리 역할. 고정 Agent Class가 아니며 개방 네임스페이스다. 프로젝트 특성·복잡도에 따라 최소 필요 역할만 동적으로 구성된다. 실행 주체 매핑은 Adapter 소관(코어는 역할 추상까지 — M5). 상세 정본: `planning/specs/04-solution-design.md`.
- **Projection** — Project Contract를 Source of Truth로 하여 파생 생성되는 프로젝트별 산출 문서(예: PRD·ARCHITECTURE·ADR·UI Guide). 대상 프로젝트 워크스페이스에 귀속되며, 유형 목록은 개방 레지스트리(비정본 부록)다. 모든 프로젝트에 모든 유형을 강제하지 않는다. 상세 정본: `planning/specs/04-solution-design.md`.
- **Contract Maturation(성숙)** — Ready 인스턴스 vN을 기준선으로 새 설계 결정을 반영한 v(N+1)을 supersedes 계보로 재발행하는 것. 단일 문서의 상태 변경이 아니라 **완결 인스턴스의 재발행**이다(PC-INV 7·9 무촉). 상세 정본: `planning/specs/04-solution-design.md`.

### §12.2 Discovery Request 인터페이스 추상 (여기서 확정)

**Discovery Request**는 Entry Resolution의 출력이자 Project Discovery의 입력인 데이터 계약이다. 이 추상은 본 절에서 확정되며, 후속 병렬 작업(`entry/specs/01-entry.md`·`discovery/specs/02-discovery.md`)의 **선행 확정 인터페이스**가 된다 — 두 작업은 이 확정 계약만 참조한다.

Discovery Request는 **3요소** 구조다.

| 요소 | 정의 |
|---|---|
| **mode** | 발견 모드. **닫힌 열거가 아니라 확장 가능한 네임스페이스**다. 초기 등재값: `greenfield` / `incremental` / `brownfield`. 신규 모드는 열거 변경 없이 네임스페이스에 등재된다 (Future Extensibility). |
| **inputs** | Discovery가 참조할 **Evidence 참조 목록**. 초기에는 Workspace Evidence(Project Contract 유무·Repository 유무 등)를 참조로 담되, 신규 Evidence Source 타입의 등록으로 확장 가능하다 (스키마 열림). 미완성·동시 작성 중인 산출물이 아니라 **확정된 참조**만 담는다. |
| **policy** | **Discovery Policy 참조**. 임계값·예산·종료 규칙 등 정책 데이터를 가리킨다 (Policy as Data). 정책 값의 상세 정본은 `discovery/specs/02-discovery.md` 소관이며, Discovery Request는 참조만 담는다. |

- **닫힘 없음 원칙.** mode는 확장 네임스페이스, inputs는 Evidence 참조 목록으로 일반화되어 있어, 신규 진입·신규 증거·신규 모드가 이 계약을 깨지 않고 확장된다.
- **경계.** Discovery Request는 Entry Resolution의 산출까지의 계약이다. Contract 자체를 담지 않으며(그것은 Discovery의 산출), Discovery 내부 개념(질문·전략)을 담지 않는다 (의존 방향, §2.5).
