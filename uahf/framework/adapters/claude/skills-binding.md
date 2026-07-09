# framework/adapters/claude/skills-binding — Claude Code Skills Adapter 바인딩

작성일: 2026-07-06
상태: v0.8 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/09-skills.md §4.1 — Claude Code Binding 표(7행). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/09-skills.md §4.2 — 이식 교체 지점 SP-1~SP-5. 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/09-skills.md §3.1-A·§3.1-B·§3.1-C·§3.1-D — Register / Discover&Select / Load / Invoke 연산. 본 문서는 이 계약을 재정의하지 않고 § 포인터로만 인용한다.
- specs/09-skills.md §3.2-A — Skill Manifest 11필드·로드 계층(메타데이터/본문). 본 문서 §3이 직렬화하는 대상 계약(재정의 0 — 필수/선택·로드 계층 정본 보존).
- specs/09-skills.md §3.2-B — Skill I/O Contract(`input`/`output`). § 포인터로만 인용.
- specs/09-skills.md §3.2-C — Skill Failure Report 구조(01 §3.2-D 재사용)·사유 코드 8종. 본 문서 §5.4가 물리 판정으로 실현하는 대상 계약(enum 소유 경계 보존).
- specs/09-skills.md §3.3 INV-1~INV-8 — 특히 INV-2(역할 경계 불침범)·INV-3(상위 규약 우선 4단)·INV-4(지연 로드)·INV-6(Module 계약 준수)·INV-7(결정적 발견). 본 문서가 물리 실현에서 준수·대조하는 불변.
- specs/09-skills.md §9 결정 기록 — OQ-S1(모호성 해소 순서 = 명시 호출 > 가장 구체적인 트리거 매칭 > `AmbiguousSelection` 실패·에스컬레이션), Failure enum 소유(구조 01 재사용·연산별 사유 각 spec 소유), Glossary 5건 승인. 본 문서 §4가 운용 전개하는 결정의 정본.
- specs/01-runtime.md §4.1 — 확장 Module 표면(`.claude/skills/`)·Module Register 바인딩. §3.1-A Register·§3.2-A Module Manifest·§3.2-B Config(Global/Project/Module 병합). § 포인터로만 참조.
- specs/02-agent.md §3.2-A — 4역할 역할 경계 표(Advisor/Planner/Worker/Verifier). Invoke의 역할 경계·우선순위 판정 근거. § 포인터로만 인용(02 소관).
- framework/adapters/claude/runtime-binding.md — 자매 Adapter Binding. §2 #3 확장 Module 표면(`.claude/skills/` — 등록·트리거·디스패치 상세를 09 소관으로 미룸, 현재 비어 있음)·§3.2 Register/Resolve 수행 방식·§3.3 Config 스코프 물리 소스·§5 `<adapter>`=`claude` 구체화의 선행 관례. 본 문서는 그 미룬 지점의 소관자다.
- framework/adapters/claude/memory-binding.md · verifier-binding.md · loop-binding.md — 자매 Adapter Binding(관례 정본). 격리 지점 방향 반전(§0)·7행 물리 실현 표 관례(§2 — 정본 인용/물리 실현/실재 여부 3열)·형태 A/B 정직 구분·1:1 절차 대응·교체 지점 표("교체되는 것/유지되는 것" 열)·실측 대조(§7)·open_questions·"구조 정본 확정 + 데이터 미생성, 시연 시 생성 예정" 관례(memory-binding.md M5 draft·loop-binding.md L8 draft 동형)의 선행 관례.
- framework/core/structure.md §2·§5·§6·§8 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·확장 Module 표면·`<adapter>` 일반형·§8 트리. 본 문서 경계의 근거.
- specs/00-glossary.md §3.2-J J-09 — Skill Manifest·Trigger·Skill Body·Skill I/O Contract·`SkillInterface` 정본(§9 요청으로 Advisor 승인 추가). 본 문서는 새 용어를 신설하지 않고 이 정본만 사용한다.
- ROADMAP.md v0.8 (Extension System) — Skills 완료 조건과 산출물("본체 수정 0 확장·지연 로드·역할 경계·우선순위·재사용")의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 09 §3.3 INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·memory-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형). 단 이 문서는 Core Contract(09 §3)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. `framework/adapters/claude/` 경계의 다섯 번째 Adapter Binding 산출물(선행: runtime·memory·verifier·loop-binding.md). 09 §4.1 바인딩 표 **7행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정)/실물 미생성(`.claude/skills/` 빈 디렉터리) 정직 구분(§2). Skill Manifest 직렬화 물리 정본 확정(§3 — `.claude/skills/<skill-id>/` 자기완결 단위, 메타데이터 9필드 = front-matter·`body` = Markdown 본문·`resources` = 본문 로드 계층의 로드 계층 분리(09 §3.2-A 필수/선택·로드 계층 정본 보존, 재정의 0), `contract` 값 = `SkillInterface` — Glossary §3.2-J J-09 / 09 §3.2-A 정본, 신설 아님). 발견·선택 물리 절차(§4 — front-matter `trigger` 평가·메타데이터만 사용·결정적·`NoMatchingSkill` 빈 결과·09 §9 결정 기록 모호성 해소 순서(명시 호출 > 가장 구체적 트리거 > `AmbiguousSelection`) 운용 전개). 지연 로드·호출·Config 주입·실패 물리 판정(§5 — 선택 본문만 로드·미선택 본문 비로드 판정법, 역할 경계 INV-2·우선순위 4단 INV-3 물리 판정, Config 주입 INV-5, Skill Failure Report 8사유 코드 물리 판정 표·enum 소유 경계 보존). 09 §4.2 이식 교체 지점 SP-1~5 대응 표("교체되는 것/유지되는 것" — 유지 열이 §3.2-A 필수 필드·§3.2-B I/O 계약·INV-2·INV-3·INV-4 전건 커버, §6). 상태 서술 실측 대조(§7 — 실재 서술 전건 파일 시스템 직접 실측 후 기입, L-07; `.claude/skills/` 빈 디렉터리·레퍼런스 Skill 실물 미생성 정직 기록, 실재 불주장). 09 §3 계약 재정의·확장 0, 새 필드·새 사유 코드·새 연산 신설 0, Glossary 밖 새 용어 0. 동시 작성 형제 산출물(hooks-binding·framework/plugins/ 문서·시연 절차서) 불인용(07 R2), 조율 필요는 open_questions로(R3). 이 1파일만 생성 — `.claude/skills/` 실물·픽스처·시연 산출물·자매 Baseline 산출물·specs/·docs/ 무수정(R4). | Worker (Advisor 위임, Task EX-S1) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/09-skills.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·필드·로드 계층·불변 규칙·사유 코드)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 09 §4.1이 "`.claude/skills/` 하위 직렬화·트리거 평가·지연 로드·등록 표면"으로 지목하고, runtime-binding.md §2 #3이 "등록·트리거·디스패치 상세 계약은 08·09·10 소관 — 포인터만 둔다"며 **09에 미룬 Skill 표면의 물리 실현**이 실재하는(확정되는) 유일한 자리다. 본 문서가 그 소관자로서, Skill Manifest 직렬화 파일 구조·발견/선택 물리 절차·지연 로드/호출 물리 절차·실패 물리 판정·Config 주입 물리 소스를 확정한다.
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리(`framework/{loop,memory,verifier,workflow,plugins}/`) 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 09 §3.3 INV-8). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형식명 Markdown·front-matter, 물리 경로 `.claude/skills/…`·`~/.claude/…`·`framework/adapters/claude/…`, 명시 호출 표면, 세션/턴, 서브에이전트 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 4문서 §0과 동형).
- **Skill Manifest 직렬화 물리 정본 선언(done 2).** `.claude/skills/` 하위 Skill 자기완결 단위의 파일 구조·메타데이터/본문 로드 계층 분리·`contract` 값 표기의 **물리 실현 정본은 이 문서(§3)다**. 09 §4.1은 이 직렬화를 "Adapter Binding 소관"으로 미뤘고(runtime-binding.md §2 #3이 09로 재차 미룸), 본 문서가 그 소유자로서 확정한다. 계약 요소의 진위 판정 기준은 항상 09 §3.2-A(필드·필수/선택·로드 계층)이며 본 문서는 물리 표기만 확정한다(재정의 0).
- **창설 금지.** 이 문서는 09 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.8 산출물(Skill 정의·등록·발견·호출의 물리 실현)의 매핑으로 한정한다. 새 Skill 연산·필드·사유 코드·불변 규칙을 만들지 않는다. Skill 계약이 정의하지 않은 Skill 실물·픽스처·시연 산출물을 생성하지 않는다(후속 시연 Task 소관, 실재 불주장).
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, runtime-binding.md §0, delegation-protocol.md §0). Skills는 정식 실행 Module이 아니라 규약 문서(09·framework/…)와 관행으로 실현된다(형태 A — 발견/선택/로드/호출을 호출 Agent가 자신의 턴에서 수행). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(`.claude/skills/` 등록 표면 디렉터리·자매 바인딩 4문서·역할 정의 파일 — §7 실측)과, **실행 코드 도입 시 로딩될 지점**(형태 B — 트리거 평가·지연 로드·우선순위 판정의 실행 엔진)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(done 7, L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(session-handoff-v0.3.md §1.4 A5 사례·§1.5 Lesson 후보 3, Active Lesson L-07). §2 "실재 여부" 열과 §7 실측 대조 표의 전 행은 파일 시스템 직접 실측에 근거한다. **`.claude/skills/`는 현재 빈 디렉터리이며 레퍼런스 Skill 실물은 미생성이다** — 본 문서는 그 실물의 실재를 주장하지 않는다(후속 시연 Task 생성 예정, memory-binding.md M5 draft·loop-binding.md L8 draft가 "구조 정본 + 데이터 미생성"을 정직 기록한 관례 동형).
- 용어는 specs/00-glossary.md 정본만 사용한다. `Skill Manifest`·`Trigger`·`Skill Body`·`Skill I/O Contract`·`SkillInterface`는 Glossary §3.2-J J-09 정본(09 §9 승인)이며, 본 문서는 새 용어를 신설하지 않는다. `형태 A/B`는 structure.md 서술 라벨의 인용이다.

---

## §1. 목적

이 문서는 09 §4.1(Skills Claude Code Binding)을 이 환경 위에 **v0.8 시점의 구체 물리 실현**으로 매핑한다.

책임은 다섯 가지다.

- 09 §4.1 바인딩 표의 **7행 전부**를 물리 표면(직렬화 파일 구조·등록·발견/선택·지연 로드·호출·resources·Config 주입)으로 확정하고, Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정/실물 미생성을 "실재 여부" 열로 정직하게 구분한다(§2, done 1·7).
- Skill Manifest 직렬화의 **물리 정본**을 확정한다(§3, done 2) — `.claude/skills/<skill-id>/` 자기완결 단위, 메타데이터 9필드 = front-matter·`body` = Markdown 본문·`resources` = 본문 로드 계층의 로드 계층 분리(09 §3.2-A 필수/선택·로드 계층 정본 보존), `contract` 값 = `SkillInterface`(Glossary §3.2-J J-09 / 09 §3.2-A 정본, 신설 아님).
- 발견·선택(Discover&Select)의 **물리 절차**를 예/아니오 판정 가능하게 확정한다(§4, done 3) — front-matter `trigger` 평가·메타데이터만 사용(본문 비로드, INV-4)·결정적(INV-7)·후보 0 = `NoMatchingSkill` 빈 결과·다수 매칭 시 09 §9 결정 기록의 해소 순서 운용 전개.
- 지연 로드(Load)·호출(Invoke)의 **물리 절차**와 Config 주입·실패 물리 판정을 확정한다(§5, done 4) — 선택 본문만 로드·미선택 본문 비로드 판정법, 역할 경계(INV-2)·우선순위 4단(INV-3) 물리 판정·보고, Config 주입(INV-5), Skill Failure Report 8사유 코드 물리 판정(enum 소유 경계 보존).
- 09 §4.2 이식 교체 지점 SP-1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§6, done 6). 그리고 상태 서술을 실측과 대조한다(§7, done 7).

이 문서는 09 §3의 어떤 계약 요소도 재정의·확장하지 않는다(§0·§8, done 5). 형태 A → 형태 B 전환 시에도 Core Contract(09 §3) 변경은 0이며(structure.md §7 C-1), 이 문서(§6의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 09 §4.1 바인딩 표 7행 물리 실현 (done 1·7)

09 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. 아래 표의 "정본 인용(원문 그대로)" 열은 09 §4.1 정본 표의 값을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 파일 구조·절차·채널을, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정/실물 미생성을 정직하게 구분한다(§7 실측 대조). "실재" 서술은 전건 파일 시스템 실측 후 기입했다(L-07).

물리 등록 표면 디렉터리 구조(본 문서 정본 — §3; `.claude/skills/`는 실재하되 현재 비어 있음, 레퍼런스 Skill 실물은 미생성 — §7 실측):

```
.claude/skills/                     # 확장 Module 표면(01 §4.1) — Skill 등록 루트. 실재(빈 디렉터리 — §7 실측)
└─ <skill-id>/                      # Skill 자기완결 단위(01 §3.2-E 규칙 2) — 하위 1개 = Skill 1개. (실물 미생성 — 예시 형태)
   ├─ <definition>.md               #   Markdown + front-matter — front-matter=메타데이터 9필드(§3.2-A)·본문=body(§3.2-A)
   └─ (resources 자원)              #   resources(§3.2-A, 선택) 참조 대상 — Skill 경계 안 파일·도구(본문 로드 계층)
```

| # | §3 계약 요소 (정본 §) | 정본 인용 (원문 그대로 — 09 §4.1) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Skill Manifest(§3.2-A) 직렬화 | `.claude/skills/` 하위의 Markdown + front-matter 파일 (01 §4.1 확장 Module 표면과 정렬). 메타데이터 필드는 front-matter, `body`는 Markdown 본문. | Skill 1개 = `.claude/skills/<skill-id>/` 자기완결 단위(01 §3.2-E 규칙 2). 정의 파일 = Markdown + front-matter — front-matter에 메타데이터 9필드(§3.2-A 로드 계층=메타데이터), Markdown 본문에 `body`(로드 계층=본문). `resources`는 본문에서 참조되는 Skill 경계 안 자원. 필드·필수/선택·로드 계층 정본은 09 §3.2-A(재정의 0). 물리 구조·표기 정본은 §3. | `.claude/skills/` 표면 실재(빈 디렉터리). 파일 구조·표기 확정(정본, §3). 레퍼런스 Skill 실물은 미생성(시연 Task 예정 — 실재 불주장). |
| 2 | Skill 등록(§3.1-A) | Runtime의 Module Register 바인딩(01 §4.1) 위에 Skill 표면으로 등록된다. | Register(09 §3.1-A) 물리 실현 = Skill 자기완결 단위를 `.claude/skills/<skill-id>/`에 배치(runtime-binding.md §3.2 Register 동형 — 파일 배치 = 규약 실현). `id` 유일성은 하위 디렉터리 이름 충돌 없음으로 물리 보장(`DuplicateId` 방지 — §5.4). Manifest 필수 필드·`contract`=`SkillInterface` 만족 검사는 등록 전 수행(`ContractMismatch` — §5.4). 완료 조건·사유 코드 정본은 09 §3.1-A(01 §3.1-A 상속). | 표면 규약 실현(형태 A, 파일 배치). 실행 Register(형태 B)는 미도입. |
| 3 | Skill 발견·선택(§3.1-B) | 작업 컨텍스트에 대한 front-matter의 `trigger` 평가로 후보를 선정한다. | Discover&Select(09 §3.1-B) 물리 실현 = 등록된 각 Skill의 front-matter `trigger`(메타데이터, 항상 열람 가능)를 작업 컨텍스트에 대해 평가해 매칭 Skill만 후보. 본문(`body`)은 비로드(INV-4). 결정적(동일 컨텍스트 → 동일 후보, INV-7). 후보 0 = `NoMatchingSkill` 빈 결과(실패 아님). 다수 매칭 해소 순서(09 §9)는 §4.2. 물리 절차 정본은 §4. | 규약 실현(형태 A — 호출 Agent가 자신의 턴에서 평가). 무인 트리거 실행 엔진(형태 B)은 미도입. |
| 4 | Skill 로드(§3.1-C, 지연) | 선택된 Skill의 Markdown 본문만 Context에 로드한다. front-matter는 항상 열람 가능, 본문은 선택 시 로드. | Load(09 §3.1-C) 물리 실현 = 선택된 `<skill-id>/`의 정의 파일 Markdown 본문(`body`)만 Context에 로드, `resources`는 본문에서 참조 해소. 미선택 Skill의 Markdown 본문은 로드하지 않는다(INV-4 — 판정법 §5.1). front-matter는 발견 단계에서 이미 열람(메타데이터). 물리 절차·`SkillBodyUnavailable`/`ResourceUnresolved` 판정은 §5.1·§5.4. | 규약 실현(형태 A — 선택 시 본문 판독). 실행 로더(형태 B)는 미도입. |
| 5 | Skill 호출(§3.1-D) | 로드된 본문 절차를 호출 Agent가 자신의 역할 경계(02 §4) 안에서 수행한다. | Invoke(09 §3.1-D) 물리 실현 = 로드된 `body` 절차를 호출 Agent(`.claude/agents/<role>.md` 서브에이전트)가 자신의 역할 경계(02 §3.2-A 표) 안에서 수행. 역할 경계 밖 지시 = `RoleBoundaryViolation`(INV-2), 상위 규약 충돌 = `PrecedenceConflict`(INV-3 4단), 입력 불일치 = `InputContractMismatch`. 물리 판정·보고는 §5.2·§5.4. | 규약 실현(형태 A — 호출 Agent가 자신의 턴에서 판정 수행). 실행 강제 엔진(형태 B)은 미도입. |
| 6 | 필요 자원(`resources`) | Skill 경계 안의 파일·도구 참조. | `resources`(09 §3.2-A, 선택·본문 로드 계층) 물리 실현 = `.claude/skills/<skill-id>/` 경계 안의 자원 파일·도구 참조. 본문(`body`)과 함께 선택 시 로드·해소된다(미해소 = `ResourceUnresolved` — §5.4). 자기완결 단위(01 §3.2-E 규칙 2)이므로 자원은 그 경계 안에 co-located. | 물리 위치·해소 규칙 확정(정본, §3·§5.1). 실물 자원은 미생성(Skill 실물 미생성과 함께 — 실재 불주장). |
| 7 | Config 주입 | 01 §3.2-B Config로 프로젝트 특정 값을 주입한다 (하드코딩 금지, INV-5). | Config 주입(01 §3.2-B, INV-5) 물리 실현 = 프로젝트 특정 값을 Config 스코프별 물리 소스(runtime-binding.md §3.3 동형: Global `~/.claude/settings.json`, Project `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`, Module scope = Skill 정의 설정 블록) 또는 호출 Agent가 제공하는 `input`(§3.2-B)으로 주입. `body`에 하드코딩하지 않는다(INV-5). 병합·우선순위(Module > Project > Global) 정본은 01 §3.2-B. 물리 상세는 §5.3. | Config 물리 소스 실재(`~/.claude/settings.json`·`.claude/` — runtime-binding.md §3.3 실측 승계). effective config 로딩(형태 B)은 미도입. |

주:

- 위 7행은 09 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 09 §4.1 정본 표현을 이 환경의 구체 파일 구조·절차·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **형태 A / 형태 B / 실물 미생성 구분(정직).** 행 1의 `.claude/skills/` 표면 디렉터리는 물리 실재(빈 디렉터리)이나 그 안의 레퍼런스 Skill 실물은 미생성이다(후속 시연 Task 소관 — 실재 불주장). 행 2(등록)·3(발견)·4(로드)·5(호출)은 Bootstrap에서 **규약 실현(형태 A)**이다 — 호출 Agent가 자신의 턴에서 파일 배치·front-matter 평가·본문 판독·역할 경계 판정을 수행하며, 무인 자동 실행 엔진(트리거 평가·지연 로더·우선순위 판정)은 형태 B다. 행 7의 Config 물리 소스는 실재하나 effective config 실행 로딩은 형태 B다.
- **Skill = 확장 Module(등록 표면의 성격).** Skill은 Agent가 아니라 `.claude/skills/` 확장 Module 표면에 등록되는 능력 단위이며(09 §2, runtime-binding.md §2 #3), Register/Resolve가 Runtime Module 계약(01 §3.1-A)을 상속·구현한다(INV-6, 재정의 0). 등록·교체·안정 식별자 규칙은 01의 Module 계약을 그대로 따른다(09 §3 서두).
- **실물 미생성 불주장(L-07).** 레퍼런스 Skill의 개별 실물은 현 시점 미존재다(§7 실측). 행 1·6의 실재는 `.claude/skills/` 등록 표면 디렉터리와 파일 구조·표기 관례에 대한 것이며, Skill 실물·`resources` 자원은 v0.8 시연 Task 수행 시 이 정본 구조대로 생성될 **예정** 산출물이다. 본 문서는 그 미래 산출물의 실재를 주장하지 않는다.

---

## §3. Skill Manifest 직렬화 물리 정본 (done 2)

09 §4.1이 "Adapter Binding 소관"으로, runtime-binding.md §2 #3이 재차 09로 미룬 Skill Manifest 직렬화의 물리 실현을 확정한다. **이 문서는 Adapter 경계이므로 구체 직렬화 형식·물리 경로 토큰의 사용이 허용된다(§0 격리 지점).** 필드·필수/선택·로드 계층의 정본은 09 §3.2-A이며, 본 절은 그 물리 표기만 확정한다(재정의 0, 새 필드 0).

### §3.1 물리 파일 구조 — Skill 자기완결 단위 (01 §3.2-E 규칙 2)

- **위치·단위.** Skill 1개는 `.claude/skills/<skill-id>/` 하위 디렉터리 1개를 **자기완결 단위**(01 §3.2-E 규칙 2 — Manifest·구현·자원을 한 경계 안에)로 차지한다. `<skill-id>`는 Skill Manifest `id`(09 §3.2-A, 안정 식별자 — 01 INV-7)이며, 하위 디렉터리 이름이 `id`의 유일성 매체다(같은 이름 배치 실패 = `DuplicateId`, §5.4).
- **정의 파일.** 그 단위 안의 정의 파일은 **Markdown + front-matter**다(09 §4.1). front-matter가 메타데이터 필드를, Markdown 본문이 `body`를 담는다(§3.2). `resources`(선택)가 참조하는 자원 파일·도구는 같은 `<skill-id>/` 경계 안에 co-located된다(본문 로드 계층).
- **구조 근거.** 자기완결 단위를 하위 디렉터리로 두는 것은 (i) 01 §3.2-E 규칙 2(Module 자기완결)의 직접 물리 실현이고, (ii) `resources`가 정의 파일과 한 경계에 모여 Skill 제거 시 잔여물 0(INV-1 — Skill 부재 전 상태 복원)을 물리적으로 보장한다. `resources`가 없는 Skill은 정의 파일 단일로 축약되는 퇴화형이며, 하위 디렉터리 대 단일 파일의 정확한 물리 형태는 Adapter 선택으로 이식 교체 지점 SP-1·SP-2에 속한다(§6, open_questions OQ-SB-1).
- **직렬화 형식 = Adapter 선택.** Markdown + front-matter는 09 §4.1이 지정한 이 환경의 직렬화 형식이며, 이식 시 대상 환경의 Skill 정의 메커니즘으로 교체된다(SP-1·SP-2, §6). 형식 선택은 09 §3.2-A 추상 스키마를 바꾸지 않는다(재정의 0).

### §3.2 로드 계층 분리 물리 표기 — 메타데이터(front-matter) vs 본문(Markdown) (09 §3.2-A 정본 보존)

09 §3.2-A "로드 계층"(메타데이터는 발견·선택 시 항상 열람, 본문은 선택 뒤에만 로드 — INV-4)을 이 환경의 물리 저장 분리로 확정한다. **아래 표는 09 §3.2-A 11필드의 필수/선택·로드 계층을 그대로 보존하고, "물리 위치" 열만 확정한다**(재정의 0).

| Skill Manifest 필드 (09 §3.2-A 정본) | 필수 (정본 보존) | 로드 계층 (09 §3.2-A 정본) | 물리 위치 (이 Adapter 확정) |
|---|---|---|---|
| `id` | 예 | 메타데이터 | front-matter. 값 = `<skill-id>`(하위 디렉터리 이름과 동일 — 유일성 매체, 안정 식별자 01 INV-7). |
| `contract` | 예 | 메타데이터 | front-matter. 값 = `SkillInterface`(Glossary §3.2-J J-09 / 09 §3.2-A 정본 — **신설 아님**). 교체는 동일 `contract` 내에서만(01 INV-1). |
| `version` | 예 | 메타데이터 | front-matter (01 상속). |
| `name` | 예 | 메타데이터 | front-matter (사람이 읽는 이름). |
| `purpose` | 예 | 메타데이터 | front-matter (발견 단계 사용 — §4). |
| `trigger` | 예 | 메타데이터 | front-matter (발견·선택 평가 대상 — §4). |
| `io` | 예 | 메타데이터 | front-matter (`input`/`output` — 09 §3.2-B I/O 계약; Config·`input` 주입 기반 §5.3). |
| `body` | 예 | 본문 | Markdown 본문 (선택 뒤에만 로드 — §5.1, INV-4). |
| `resources` | 아니오 | 본문 | 본문에서 참조 — `<skill-id>/` 경계 안 자원 파일·도구(§3.1, §5.1). |
| `requires` | 아니오 | 메타데이터 | front-matter (의존 contract id 목록 — 01 상속, Resolve 시 해소). |
| `replaceable` | 아니오(기본 true) | 메타데이터 | front-matter (기본 `true` — 01 INV-1·ARCHITECTURE 3.2; `false`는 근거 요구). |

- **로드 계층의 물리 보장.** 메타데이터 9필드는 front-matter에 있어 발견·선택 단계에서 항상 열람되고(§4), 본문 로드 계층 2필드(`body`·`resources`)는 선택 뒤에만 로드된다(§5.1). 이 저장 분리(front-matter vs Markdown 본문)가 INV-4(지연 로드)의 물리 기반이며, 발견·선택이 본문을 로드하지 않음을 물리적으로 보장한다.
- **`contract` = `SkillInterface`(신설 아님).** `contract` 필드의 값은 Skill이 구현하는 공통 계약 식별자 `SkillInterface`다 — Glossary §3.2-J J-09가 정본(09 §9 승인)이고 필드 정본은 09 §3.2-A다. 본 문서는 이 값을 물리 표기(front-matter `contract` 값)로 바인딩할 뿐 새 계약·새 용어를 신설하지 않는다(용어 신설 0).
- **필수/선택 보존.** 8필드는 필수, 3필드(`resources`·`requires`·`replaceable`)는 선택이다(09 §3.2-A). 물리 직렬화는 이 필수/선택 지위를 바꾸지 않는다 — 필수 필드는 모든 Skill 정의에 존재하고, 선택 필드는 생략 가능하다(`replaceable` 생략 시 기본 `true`). 필드 의미·필수 지위의 정본은 09 §3.2-A이며 본 표는 물리 위치만 확정한다.

---

## §4. 발견·선택(Discover&Select) 물리 절차 · 모호성 해소 순서 운용 전개 (done 3)

09 §3.1-B(Discover&Select)의 계약을 이 환경의 물리 절차로 확정한다. 계약(입력=작업 컨텍스트, 출력=후보 목록·선택, 완료 조건=trigger 평가·결정적, 제약=메타데이터만 사용, 실패=`AmbiguousSelection`/`NoMatchingSkill`)의 정본은 09 §3.1-B·INV-4·INV-7이며, 본 절은 물리 실현만 확정한다(재정의 0).

### §4.1 발견·선택 물리 절차 (예/아니오 판정 가능)

| 09 §3.1-B 계약 단계 | 물리 실현 (claude 환경) | 판정 (예/아니오) |
|---|---|---|
| **1** — 작업 컨텍스트 입력 | 현재 task 요약 또는 트리거 신호(09 §3.1-B 입력)를 발견 입력으로 받는다. | task 요약/트리거 신호가 주어졌는가? |
| **2** — 각 등록 Skill의 `trigger` 평가(메타데이터만) | `.claude/skills/<skill-id>/` 각각의 front-matter `trigger`(메타데이터, 항상 열람)를 작업 컨텍스트에 대해 평가한다. **Markdown 본문(`body`)·`resources`는 열지 않는다**(INV-4). | 평가에 front-matter만 사용했는가? 미선택 Skill 본문을 열지 않았는가? |
| **3** — 매칭 Skill만 후보 | `trigger`가 컨텍스트에 매칭된 Skill만 후보 집합에 넣는다(09 §3.1-B 완료 조건). | 후보 = 매칭 Skill 집합인가? |
| **4** — 결정성(INV-7) | 동일 작업 컨텍스트 + 동일 등록 Skill 집합 → 동일 후보 집합. 평가는 (컨텍스트, front-matter)의 순수 함수이며 숨은 상태에 의존하지 않는다. | 반복 실행에서 후보 집합이 동일한가?(09 §7 검증 방법) |
| **5** — 후보 0 = `NoMatchingSkill` | 매칭 후보가 0이면 **실패가 아니라** `NoMatchingSkill` 빈 결과다(09 §3.1-B). 호출 Agent는 Skill 없이 진행한다. | 후보 0을 빈 결과로 처리했는가?(실패로 보고하지 않았는가?) |
| **6** — 다수 매칭 해소 | 다수 Skill 매칭 시 §4.2 해소 순서를 적용한다. 결정적 선택 불가 시에만 `AmbiguousSelection`(09 §3.1-B). | 다수 매칭에 해소 순서를 적용했는가? |

### §4.2 모호성 해소 순서 운용 전개 (09 §9 결정 기록 OQ-S1)

09 §9 결정 기록의 해소 순서 — **명시 호출 > 가장 구체적인 트리거 매칭 > 그래도 모호하면 `AmbiguousSelection` 실패·에스컬레이션** — 을 이 환경의 물리 절차로 전개한다. **순서(정본)는 09 §9가 소유하고, 본 절은 각 단계의 물리 실현만 확정한다**(재정의 0; 09 §9 "상세 규칙은 v0.8 구현 시 정밀화 가능 — 계약 골격 확정").

1. **명시 호출(1순위).** 작업 컨텍스트가 특정 Skill을 명시적으로 지정하면(물리 표면 = 명시적 Skill 지정, 예: 슬래시 형태 `/<skill-id>` 또는 skill id 직접 참조) 그 Skill이 즉시 선택된다 — 다른 후보의 trigger 매칭 여부와 무관하게 명시 호출이 이긴다. 명시된 `<skill-id>`가 등록되어 있지 않으면 그 명시 호출은 후보가 되지 못한다(그 경우 2로 진행하거나 `NoMatchingSkill`).
2. **가장 구체적인 트리거 매칭(2순위).** 명시 호출이 없고 후보가 2개 이상이면, front-matter `trigger`가 작업 컨텍스트에 **가장 구체적으로** 매칭되는 Skill을 선택한다(더 좁은·더 제약된 trigger가 이긴다). "가장 구체적"의 정밀 척도(예: trigger 조건의 좁힘 정도)는 이 Adapter의 구현 선택이며 이식 교체 지점 SP-3(트리거 평가 메커니즘)에 속한다 — 순서(명시 > 구체 > 실패)는 09 §9 정본으로 불변이다.
3. **`AmbiguousSelection`(3순위, 실패·에스컬레이션).** 1·2로도 결정적 선택이 불가하면(동등하게 구체적인 다수 후보) `AmbiguousSelection`으로 보고하고 에스컬레이션한다(§5.4). 이는 결정적이어야 한다는 제약(INV-7)과 정합한다 — 임의 선택으로 우회하지 않는다.

- **정본/구현 경계.** 해소 **순서**(3단)는 09 §9 결정 기록 정본이다. 본 절이 확정하는 것은 각 단계의 **물리 표면**(명시 호출 = 명시적 Skill 지정 표면, 구체성 = trigger 평가 척도)뿐이며, 순서 자체를 바꾸지 않는다. 정밀 척도는 v0.8 구현 시 정밀화 가능(09 §9)하며, 그 정밀화는 SP-3 교체 지점에서 이뤄진다(계약 골격 불변).

---

## §5. 지연 로드(Load)·호출(Invoke)·Config 주입·실패 물리 판정 (done 4)

09 §3.1-C(Load)·§3.1-D(Invoke)의 계약과 Config 주입(01 §3.2-B, INV-5)·실패 물리 판정(09 §3.2-C 8사유 코드)을 이 환경의 물리 절차로 확정한다. 계약의 정본은 09 §3.1-C·§3.1-D·§3.2-C·§3.3 INV-2·INV-3·INV-4·INV-5·02 §3.2-A이며, 본 절은 물리 실현만 확정한다(재정의 0).

### §5.1 지연 로드(Load) 물리 절차 · 미선택 본문 비로드 판정법 (09 §3.1-C, INV-4)

| 09 §3.1-C 계약 단계 | 물리 실현 (claude 환경) | reason (실패 시 — §5.4) |
|---|---|---|
| **1** — 선택된 skill id 입력 | §4에서 선택된 `<skill-id>` 1건을 로드 입력으로 받는다. | — |
| **2** — 선택 Skill 본문만 로드 | 선택된 `.claude/skills/<skill-id>/` 정의 파일의 **Markdown 본문(`body`)만** Context에 로드한다. front-matter는 발견 단계에서 이미 열람됨(메타데이터). 본문이 없거나 판독 불가면 실패. | `SkillBodyUnavailable` (09 §3.1-C) |
| **3** — `resources` 참조 해소 | `body`가 참조하는 `resources`(선택)를 `<skill-id>/` 경계 안에서 해소한다. 참조 대상 자원 파일·도구가 부재·미해소면 실패. | `ResourceUnresolved` (09 §3.1-C) |
| **4** — 미선택 Skill 본문 비로드(INV-4) | 미선택 Skill의 Markdown 본문은 Context에 로드하지 않는다. front-matter만 발견 단계에서 열람됐을 뿐이다. | — (위반 시 §7 검증 실패로 판정 — 09 §6) |

- **미선택 본문 비로드 판정법(done 4).** 물리 판정: 로드 후 Context를 대상으로, **선택된 `<skill-id>` 외 Skill의 Markdown 본문 텍스트가 Context에 존재하지 않음**을 확인한다(09 §7 검증 방법 — "Verifier가 로드된 Context에 미선택 Skill 본문이 없음을 확인"). front-matter(메타데이터)는 발견 단계 열람이 정당하나, 본문은 오직 선택된 Skill의 것만 존재해야 한다. 미선택 본문이 Context에 있으면 INV-4 위반으로 검증 실패다(09 §6 "미선택 Skill 본문까지 로드 → 검증 실패로 판정").
- **형태 구분.** Bootstrap(형태 A)에서 이 로드는 호출 Agent가 선택된 정의 파일 본문을 판독하는 것으로 실현된다. 실행 로더(형태 B) 도입 시 선택된 본문만 Context에 주입하는 지연 로드 메커니즘으로 실현되며, INV-4 계약은 불변이다(SP-4, §6).

### §5.2 호출(Invoke) 물리 절차 · 역할 경계(INV-2)·우선순위 4단(INV-3) 물리 판정 (09 §3.1-D)

로드된 `body` 절차를 호출 Agent(`.claude/agents/<role>.md` 서브에이전트)가 자신의 역할 경계(02 §3.2-A 표) 안에서 수행한다. Skill은 호출 Agent가 이미 가진 권한 안에서만 실행되며 역할 경계를 확장·우회할 수 없다(INV-2). Skill 지시가 상위 규약과 충돌하면 우선순위(INV-3)에 따라 상위 규약이 이긴다.

| 09 §3.1-D 계약 요소 | 물리 판정·보고 (claude 환경) | reason (실패 시 — §5.4) |
|---|---|---|
| 입력 = 로드된 `body` + `io.input` 맞는 입력 + 호출 Agent 역할 | 호출 Agent가 제공한 입력이 `io.input`(09 §3.2-B) 형태·의미에 맞는지 확인. 불일치면 실패. | `InputContractMismatch` (09 §3.1-D) |
| 역할 경계 안 수행(INV-2) | `body` 지시가 호출 Agent의 02 §3.2-A 역할 행(예: Worker = 구현·보고, Architecture 결정 안 함) 안에 있는지 물리 판정. 역할 경계 밖 지시(예: Worker에게 Architecture 결정 지시)는 **무효**이며, 호출 Agent는 추측하지 않고 Advisor에게 에스컬레이션한다(02 O4, 09 §8 예3). | `RoleBoundaryViolation` (09 §3.1-D, INV-2) |
| 우선순위 4단(INV-3) 충돌 처리 | `body` 지시가 상위 규약과 충돌하면 우선순위 4단(아래)으로 물리 판정 — 상위가 이기고 충돌 Skill 지시는 **무시**되며 충돌이 보고된다(09 §8 예2). | `PrecedenceConflict` (09 §3.1-D, INV-3) |
| 완료 조건 = 역할 경계 안 + 상위 규약 충돌 없이 수행 | 위 판정을 통과한 `body` 절차를 수행하고, 산출물은 호출 Agent의 완료 보고(02 §3.2-C)/실패 보고(02 §3.2-D)에 반영한다. | — |

**우선순위 4단(INV-3 정본 — 높음 → 낮음, 이 환경의 물리 근거):**

1. **ARCHITECTURE.md** (최우선) — 물리 근거 = `ARCHITECTURE.md`(및 `.claude/CLAUDE.md` "항상 ARCHITECTURE.md를 최우선으로 따른다").
2. **AGENT.md** (상위 규약) — 물리 근거 = `.claude/AGENT.md`.
3. **담당 spec 계약 + 위임 메시지 제약** — 물리 근거 = 담당 spec(예: 02 역할 경계 §3.2-A) 및 위임 메시지 제약(02 §3.2-B constraints, O1 위임 범위).
4. **Skill 지시** (최하위) — 물리 근거 = 로드된 `body`.

- **물리 판정 방식.** 호출 Agent는 서브에이전트로서, 로드된 `body`(계층 4)의 각 지시를 자신의 역할 정의(`.claude/agents/<role>.md` + 02 §3.2-A, 계층 3)와 상위 규약(계층 1·2 = `ARCHITECTURE.md`·`.claude/AGENT.md`)에 대조한다. 역할 밖이면 `RoleBoundaryViolation`(무효), 상위 계층과 충돌이면 `PrecedenceConflict`(상위 우선·Skill 지시 무시). 이 규약(우선순위·역할 경계)은 전부 이 환경에 물리적으로 실재하는 문서다(§7 실측).
- **형태 구분.** Bootstrap(형태 A)에서 이 판정은 호출 Agent가 자신의 턴에서 수행한다 — 자기 점검을 최종 승인으로 삼지 않으며(02 §3.2-A), 독립 판정은 Verifier(09 §7 — "역할 경계·우선순위 위반 케이스를 02 §3.2-A 표와 §3.3과 대조"), 최종 승인은 Advisor다. 실행 강제 엔진(형태 B)은 미도입이며, 도입 시에도 INV-2·INV-3 계약은 불변이다(SP-3, §6).

### §5.3 Config 주입 물리 소스 (01 §3.2-B, INV-5)

Skill의 I/O 계약과 `body`는 프로젝트 비의존으로 작성되고, 프로젝트 특정 값은 Config나 `input`으로 주입되며 `body`에 하드코딩되지 않는다(INV-5, 09 §3.2-B).

- **주입 경로 1 — Config(01 §3.2-B).** Config 스코프별 물리 소스는 runtime-binding.md §3.3 동형이다: Global = `~/.claude/settings.json`, Project = `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`, Module scope = 해당 Skill 정의의 설정 블록(`target` = `<skill-id>`). 병합·우선순위(Module > Project > Global)의 정본은 01 §3.2-B·config-schema.md §4.2이며, 본 문서는 물리 소스만 바인딩한다(재정의 0).
- **주입 경로 2 — `input`(09 §3.2-B).** 호출 Agent가 Invoke 시 `io.input`에 맞는 입력으로 프로젝트 특정 값을 제공한다. 이는 재사용성의 기반(INV-5)이다 — 동일 Skill이 다른 프로젝트에 재등록만으로 재사용되며, 프로젝트 특정 값은 Config·`input`으로 주입된다.
- **하드코딩 금지 판정.** `body`에 프로젝트 특정 값이 하드코딩되어 있으면 INV-5 위반이며 Config·입력 주입으로 교정한다(09 §6). 재사용 시연(09 §7)은 이 주입을 보인다.

### §5.4 Skill Failure Report 물리 판정 — 8사유 코드 (09 §3.2-C, enum 소유 경계 보존)

모든 Skill 연산의 실패는 Skill Failure Report(09 §3.2-C — 구조는 01 §3.2-D 재사용: `operation`/`target`/`reason`/`location` 4필드)로 보고한다. **구조·사유 코드 정의의 정본은 09 §3.2-C이며, 본 표는 각 사유 코드의 물리 판정 지점만 확정한다**(새 사유 코드 0). enum 소유 경계(09 §9 결정: Register 사유는 01 §3.2-D 상속, Skill 특화 연산 사유는 09 소유)를 보존한다.

| reason (09 §3.2-C) | 연산 | enum 소유 (09 §9) | 물리 판정 지점 (claude 환경) |
|---|---|---|---|
| `ContractMismatch` | Register | 01 §3.2-D 상속 | 등록 전, Skill 정의의 front-matter가 Module/Skill 필수 필드(§3.2) 또는 `contract`=`SkillInterface`를 만족하지 않음(누락·불일치). |
| `DuplicateId` | Register | 01 §3.2-D 상속 | 배치 시 `.claude/skills/<skill-id>/` 이름이 기존 등록과 충돌(id 유일성 위반 — §3.1). |
| `AmbiguousSelection` | Discover&Select | 09 소유 | §4.2 해소 순서(명시 호출 > 가장 구체적 트리거) 적용 후에도 결정적 선택 불가(동등 구체 다수 후보). |
| `SkillBodyUnavailable` | Load | 09 소유 | 선택된 `<skill-id>/` 정의 파일의 Markdown 본문(`body`)이 부재·판독 불가(§5.1 단계 2). |
| `ResourceUnresolved` | Load | 09 소유 | `body`가 참조하는 `resources`가 `<skill-id>/` 경계 안에서 미해소·부재(§5.1 단계 3). |
| `RoleBoundaryViolation` | Invoke | 09 소유 | `body` 지시가 호출 Agent의 02 §3.2-A 역할 경계 밖(§5.2 — 지시 무효, 에스컬레이션). |
| `PrecedenceConflict` | Invoke | 09 소유 | `body` 지시가 상위 규약(우선순위 계층 1~3)과 충돌(§5.2 — 상위 우선, Skill 지시 무시). |
| `InputContractMismatch` | Invoke | 09 소유 | 호출 Agent가 제공한 입력이 `io.input`(§3.2-B) 형태·의미와 불일치(§5.2). |

- **`NoMatchingSkill`은 실패 아님.** 발견 후보 0은 사유 코드가 아니라 `NoMatchingSkill` 빈 결과로 구분된다(09 §3.1-B·§3.2-C). 위 8사유 코드에 포함되지 않으며, Agent는 Skill 없이 진행한다(§4.1 단계 5).
- **enum 소유 경계 보존(09 §9, 01 조율).** `ContractMismatch`·`DuplicateId`는 01 §3.2-D enum 상속(Register — 01 Register 계약), 나머지 6개(`AmbiguousSelection`/`SkillBodyUnavailable`/`ResourceUnresolved`/`RoleBoundaryViolation`/`PrecedenceConflict`/`InputContractMismatch`)는 09 소유(Skill 특화 연산)다. 본 문서는 이 소유 경계를 재정의하지 않고 물리 판정 지점만 바인딩한다.
- **Lesson 후보.** Skill 호출 실패는 Lesson 후보이며(09 §5·§6), 그 기록은 호출 Agent의 실패 보고(02 §3.2-D)와 Memory Update(02 §5, 단일 Port)를 경유한다 — Skills는 Memory로 향하는 두 번째 경로를 열지 않는다(09 §5, INV-8). 본 문서는 이 경로를 재서술하지 않고 포인터만 둔다.

---

## §6. 09 §4.2 이식 교체 지점 SP-1~5 대응 (done 6)

09 §4.2 이식 교체 지점 SP-1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인하며, **09 §4.2 유지 목록(§3.2-A Manifest 필수 필드·§3.2-B I/O 계약·§3.3 Invariants — 특히 INV-2 역할 경계·INV-3 우선순위·INV-4 지연 로드)을 전건 커버**한다.

| # (09 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Skill 정의 위치·포맷(`.claude/skills/`, Markdown + front-matter) → 대상 환경의 Skill 정의 메커니즘 | §2 #1, §3.1 | `.claude/skills/<skill-id>/` 자기완결 단위, Markdown + front-matter 정의 파일, 하위 디렉터리 대 단일 파일 물리 형태. | §3.2-A **Manifest 필수 필드**(id/contract/version/name/purpose/trigger/io/body)·필수/선택 지위, INV-6(Module 계약 준수)·안정 식별자(01 INV-7). |
| SP-2 | 메타데이터/본문 저장 분리(front-matter vs 본문) → 대상 환경의 경량 메타데이터·본문 분리 표현 | §2 #1·#4, §3.2, §5.1 | 메타데이터 9필드 = front-matter·`body`/`resources` = Markdown 본문/경계 자원의 물리 저장 분리. | §3.2-A **로드 계층**(메타데이터 항상 열람·본문 선택 후 로드), **INV-4(지연 로드)**. |
| SP-3 | 트리거 평가 메커니즘 → 대상 환경의 Skill 매칭·선택 방식 | §2 #3·#5, §4, §5.2 | front-matter `trigger` 평가·"가장 구체적" 척도(§4.2 2순위), 명시 호출 표면(`/<skill-id>`), 역할 경계·우선순위 판정의 형태 A 수행. | **INV-7(결정적 발견)**, 09 §9 해소 순서(명시 > 구체 > `AmbiguousSelection`), **INV-2(역할 경계)**·**INV-3(우선순위 4단)**, §3.2-B I/O 계약(`io.input` 대조). |
| SP-4 | 지연 로드 메커니즘(선택된 본문의 Context 주입) → 대상 환경의 지연 로드 방식 | §2 #4, §5.1 | 선택 `<skill-id>` 정의 파일 Markdown 본문만 Context 로드, 미선택 본문 비로드 판정법(형태 A 판독 / 형태 B 로더). | **INV-4(지연 로드)** — 미선택 본문 비로드, 발견은 메타데이터만. |
| SP-5 | 등록 표면(Runtime Module Register 바인딩 경유) → 01 §4.2 이식 교체 지점 상속 | §2 #2, §3.1 | `.claude/skills/<skill-id>/` 배치 = Register(형태 A), 실행 Register(형태 B). Runtime 이식 시 함께 교체(01 §4.2 상속). | §3.1-A Register 완료 조건·사유 코드(`ContractMismatch`/`DuplicateId` 01 상속), **INV-6(Module 계약)**, 01 §3.1-A·§4.2 이식 교체 지점. |

- **유지 목록 전건 커버 확인(done 6).** 09 §4.2 "유지되는 것" 목록 = { §3.2-A Manifest 필수 필드, §3.2-B I/O 계약, §3.3 Invariants(특히 INV-2·INV-3·INV-4) }. 위 표 유지 열 커버: **§3.2-A Manifest 필수 필드** = SP-1; **§3.2-B I/O 계약** = SP-3(`io.input` 대조); **INV-2 역할 경계** = SP-3; **INV-3 우선순위** = SP-3; **INV-4 지연 로드** = SP-2·SP-4; 추가로 INV-6(Module 계약) = SP-1·SP-5, INV-7(결정적 발견) = SP-3. 09 §4.2 유지 목록 전건이 유지 열에 나타난다.
- **호출 계약의 이식 불변성(SP 비귀속).** Invoke의 역할 경계(INV-2)·우선순위(INV-3)·I/O 계약(§3.2-B)은 특정 SP에 묶이는 "교체되는 것"이 아니라 **모든 이식에서 유지되는 계약**이다 — 호출은 대상 환경에서도 호출 Agent의 역할 경계 안에서, 상위 규약 우선으로 수행된다(09 §4.2 유지 목록). 위 표는 이를 SP-3의 유지 열에 명시했다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(09 §4.2 말미·runtime-binding.md §4·memory-binding.md §6·verifier-binding.md §6·loop-binding.md §6 동형). 본 문서는 그 정식화를 선취하지 않고 v0.8 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 7 — A5/L-07 재발 방지)

session-handoff-v0.3.md §1.4(A5 사례 — 미존재 소스를 "실재"로 서술 → 파일 시스템 전수 대조로 검출)·§1.5 Lesson 후보 3(상태 서술은 실측 후 기록, Active Lesson L-07)에 따라, 본 문서의 "실재/존재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`) + 디렉터리 내용 열거(`find`) + 파일 크기 직접 실측.**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — runtime/memory/verifier/loop/workflow-binding.md·memory-data/·loop-data/ 존재 확인. |
| `framework/adapters/claude/runtime-binding.md` | 실재 (v0.3 Baseline, 자매 — 관례 정본) | 실재 (32,973 bytes). |
| `framework/adapters/claude/memory-binding.md` | 실재 (v0.4 Baseline, 자매 — 관례 정본) | 실재 (51,144 bytes). |
| `framework/adapters/claude/verifier-binding.md` | 실재 (v0.5 Baseline, 자매 — 관례 정본) | 실재 (46,449 bytes). |
| `framework/adapters/claude/loop-binding.md` | 실재 (v0.7 Baseline, 자매 — 관례 정본) | 실재 (64,012 bytes). |
| `framework/adapters/claude/workflow-binding.md` | 실재 (자매 Baseline — 물리 존재만 확인, 내용 불인용) | 실재 (66,496 bytes). 본 문서는 그 내용을 인용하지 않는다. |
| `framework/adapters/claude/skills-binding.md` | 실재 (본 문서 — 본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음. |
| `.claude/skills/` (§2 #1 등록 표면) | **실재하되 빈 디렉터리** (등록 표면 존재, 레퍼런스 Skill 실물 미생성) | **실재 — 빈 디렉터리** (`find` 결과 0건). runtime-binding.md §2 #3 "세 디렉터리 존재, 현재 비어 있음"과 정합. |
| `.claude/skills/<skill-id>/` 레퍼런스 Skill 실물 (§2 #1·#6, §3) | **미생성** (구조·표기 정본 확정, 실물은 후속 시연 Task 생성 예정 — 실재 불주장) | **미생성** — `.claude/skills/` 하위 항목 0건. 미래 산출물로 실재 불주장(L-07). |
| `.claude/agents/` 역할 정의 파일 (§5.2 Invoke 호출 Agent) | 실재 (호출 Agent 서브에이전트 정의 — 02 §3.2-A 역할 경계 물리 근거) | 실재 — advisor.md·planner.md·verifier.md·worker.md 존재(자매 문서 §7 실측 승계, loop-binding.md §7). |
| 우선순위 4단 물리 근거 (§5.2) — `ARCHITECTURE.md`·`.claude/AGENT.md`·담당 spec·`body` | 실재 (계층 1~3 규약 문서 실재) | 실재 — `.claude/AGENT.md`·`.claude/CLAUDE.md`("항상 ARCHITECTURE.md를 최우선")·specs/02 §3.2-A 확인. |
| Config 물리 소스 (§5.3) — `~/.claude/settings.json`·`.claude/` | 실재 (runtime-binding.md §3.3 동형) | 실재(자매 문서 실측 승계) — runtime-binding.md §3.3 소스 목록 참조. |
| `SkillInterface` 용어 (§3.2 `contract` 값) | 실재 (Glossary §3.2-J J-09 정본 — 신설 아님) | 실재 — specs/00-glossary.md §3.2-J J-09 "SkillInterface — Skill이 구현하는 공통 계약 식별자" 확인. |
| Skill 트리거 평가·지연 로드·호출 실행 진입점·로더 (형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). 실행 엔진 코드 0. |

- **핵심 구분.** 본 문서가 확정한 Skill Manifest 직렬화 파일 구조·로드 계층 물리 표기·발견/선택·지연 로드/호출 물리 절차·실패 물리 판정은 **정본**(§3~§5)이며, `.claude/skills/`는 등록 표면으로 **실재하되 현재 비어 있다** — 레퍼런스 Skill 실물은 미생성이다. 이는 memory-binding.md M5 draft("구조 정본 확정 + 데이터 미생성, 시연 시 생성 예정")·loop-binding.md L8 draft와 동형이다. Skill 실물·`resources` 자원의 생성 주체는 **후속 시연 Task**이며, 본 문서(EX-S1)는 구조·표기·절차의 정본만 소유한다 — 실물을 생성·주장하지 않는다.
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로, 미래 산출물을 현재 실재로 쓰지 않았다(A5/L-07 재발 방지). `.claude/skills/`가 빈 디렉터리임을 실재 불주장으로 정직 기록했다(done 7).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 5).** 본 문서의 모든 매핑은 09 §3·§4의 물리 실현이다. 어떤 연산·데이터 계약·필드·로드 계층·불변 규칙·사유 코드도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 정본 §(09 §3.1·§3.2·§3.3·§4)다. 계약 요소는 전부 `09 §…` 포인터로 인용했으며, **새 필드·새 사유 코드·새 연산을 신설하지 않았다**(Manifest 11필드·8사유 코드·`NoMatchingSkill` 빈 결과·4연산 전부 09 정본 인용). Glossary 밖 새 용어 신설 0(`SkillInterface` 등 5용어는 Glossary §3.2-J J-09 정본).
- **계약 소유 명시.** Skill Manifest 필드·로드 계층 = 09 §3.2-A / Glossary J-09; I/O 계약 = 09 §3.2-B; Failure Report 구조·사유 코드 = 09 §3.2-C(구조 01 §3.2-D 재사용, 소유 경계 09 §9); 4연산 완료 조건 = 09 §3.1-A/B/C/D; 불변 규칙 = 09 §3.3; 모호성 해소 순서 = 09 §9 결정 기록; 역할 경계 = 02 §3.2-A; Config 병합 = 01 §3.2-B. 본 문서는 이들의 **물리 실현**(직렬화 파일 구조·로드 계층 물리 표기·발견/선택 물리 절차·지연 로드/호출 물리 절차·실패 물리 판정 지점·Config 물리 소스)만 확정한다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형식(Markdown·front-matter)·물리 경로(`.claude/skills/…`·`~/.claude/…`·`framework/adapters/claude/…`)·명시 호출 표면·세션/턴·서브에이전트 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. 09(Core Contract)·framework/core/·framework/runtime/ 문서 본문은 이 토큰을 "Adapter Binding 문서 소관" 포인터로만 미뤘고(runtime-binding.md §2 #3), 본 문서가 그 소관자다(structure.md §5 C-3 확장은 이 경계에 비적용 — 격리 보유, 자매 4문서 §0과 동형).
- **동시 작성 문서 경계(07 R2) 및 미래 산출물(L-07).** 같은 Wave에서 동시 작성 중인 형제 산출물 — hooks-binding(08)·framework/plugins/ 문서(10)·시연 절차서 — 의 내용을 인용·추측하지 않았다(07 R2 준수). `.claude/hooks/`(Hooks 08 소관)·Plugins 배포(10 소관)와의 경계 정합은 09 §9 08/10 조율 항목이며, 09 §9 결정("Plugin에 번들된 Skill의 등록 경로는 10 §3.1 Activate가 01 Register 경유 — 09 등록 계약과 동일")을 인용만 하고 10의 내용을 추측하지 않았다. 참조한 확정 정본은 09(정본)·자매 Adapter Binding 4문서(runtime·memory·verifier·loop-binding.md — 관례 정본)·framework/core/structure.md·specs/01·02·00-glossary.md·`.claude/agents/`·`.claude/AGENT.md`·`.claude/CLAUDE.md`·ROADMAP.md뿐이다. workflow-binding.md는 물리 존재만 실측했고 내용을 인용하지 않았다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4, 07 R3). 본 산출은 이 1개 파일(`framework/adapters/claude/skills-binding.md`)만 생성하며, `.claude/skills/` 실물·픽스처·시연 산출물·자매 Baseline 산출물(runtime/memory/verifier/loop/workflow-binding.md·memory-data/·loop-data/)·`.claude/agents/`·specs/·docs/를 수정·생성하지 않는다(R4).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-SB-1 (Skill 자기완결 단위 물리 형태 = Adapter 선택, Advisor 채택 대상 — 비차단).** 09 §4.1은 "`.claude/skills/` 하위의 Markdown + front-matter 파일"로 직렬화를 지정하나, 그 자기완결 단위를 **하위 디렉터리**(`.claude/skills/<skill-id>/` — resources co-location, 01 §3.2-E 규칙 2)로 둘지 **단일 파일**(resources 없는 퇴화형)로 둘지의 정확한 물리 형태는 09가 확정하지 않았다. 본 문서 §3.1은 하위 디렉터리 자기완결 단위를 정본으로 제안했다(근거: 규칙 2 + resources 경계 co-location + INV-1 잔여물 0). 대안(단일 파일 + 별도 resources 참조)도 09 §3.2-A 계약을 위반하지 않는다. 이 물리 형태 채택은 Advisor 채택 대상이며, 계약(09 §3.2-A) 변경이 아니므로 비차단이다. memory-binding.md OQ(구조 제안)·loop-binding.md OQ-LB-1(사이클당 파일 제안)과 동형이다.
- **OQ-SB-2 (모호성 해소 "가장 구체적" 정밀 척도 — 비차단).** 09 §9 결정 기록은 해소 순서(명시 호출 > 가장 구체적 트리거 > `AmbiguousSelection`)의 **골격**만 확정하고 "상세 규칙은 v0.8 구현 시 정밀화 가능"으로 두었다. "가장 구체적인 트리거 매칭"의 정밀 척도(trigger 조건의 좁힘 정도를 어떻게 측정하는가)는 이 Adapter의 구현 선택(SP-3)이며 §4.2에서 순서만 물리 전개했다. 정밀 척도의 확정은 v0.8 실행 코드(형태 B) 설계·시연 시 정밀화 대상이다. 순서(09 §9 정본) 변경이 아니므로 비차단이다.
- **OQ-SB-3 (08/10 조율 — 비차단, 추측 안 함).** `.claude/hooks/`(Hooks)·Plugins 배포에 번들된 Skill의 등록 경로 경계 정합은 09 §9 08/10 조율 항목이다. 09 §9 결정(Plugin 번들 Skill = 10 §3.1 Activate가 01 Register 경유 — 09 등록 계약과 동일)을 인용만 했고, 동시 작성 중인 hooks-binding·framework/plugins/ 문서의 내용을 추측·인용하지 않았다(07 R2·R3). 이 경계의 물리 실현 정합은 08/10 바인딩과의 조율 대상이며, 계약(09) 변경이 아니므로 비차단이다.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 다섯 번째 Adapter Binding 산출물(선행: runtime·memory·verifier·loop-binding.md). 09 §4.1(Skills 바인딩 표 7행)의 **v0.8 물리 실현 매핑**. 정본 = 09 §3·§4(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 09 §4.1 표 **7행 전부**를 물리 표면으로 매핑("정본 인용(원문 그대로)" 열 + "물리 실현" 열 + "실재 여부" 열, 형태 A/B/실물 미생성 정직 구분). `.claude/skills/` 등록 표면 = 실재(빈 디렉터리); 등록·발견·로드·호출 = 규약 실현(형태 A); 레퍼런스 Skill 실물 = 미생성(시연 Task 예정, 실재 불주장); 실행 엔진·로더 = 형태 B.
- **§3 (직렬화 물리 정본):** `.claude/skills/<skill-id>/` 자기완결 단위(01 §3.2-E 규칙 2), 로드 계층 분리 — 메타데이터 9필드 = front-matter·`body` = Markdown 본문·`resources` = 본문 로드 계층(09 §3.2-A 필수/선택·로드 계층 정본 보존, 재정의 0), `contract` 값 = `SkillInterface`(Glossary §3.2-J J-09 / 09 §3.2-A 정본 — 신설 아님).
- **§4:** 발견·선택 물리 절차(예/아니오 판정 가능 — front-matter `trigger` 평가·메타데이터만·결정적 INV-7·`NoMatchingSkill` 빈 결과) + 모호성 해소 순서 운용 전개(09 §9: 명시 호출 > 가장 구체적 트리거 > `AmbiguousSelection` — 순서는 정본, 물리 표면만 확정).
- **§5:** 지연 로드(선택 본문만 로드·미선택 본문 비로드 판정법, INV-4) + 호출(역할 경계 INV-2·우선순위 4단 INV-3 물리 판정·보고) + Config 주입(01 §3.2-B 물리 소스·`input`, INV-5) + Skill Failure Report 8사유 코드 물리 판정(enum 소유 경계 보존 — Register 01 상속·Skill 특화 09 소유).
- **§6:** 09 §4.2 이식 교체 지점 SP-1~5 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 09 §4.2 유지 목록(§3.2-A 필수 필드·§3.2-B I/O 계약·INV-2·INV-3·INV-4)을 **전건 커버**(C-1 이식 불변 재확인).
- **§7:** 실측 대조(2026-07-06 직접 실측) — 자매 바인딩 4문서·`.claude/skills/` 등록 표면(빈 디렉터리)·역할 정의 파일·우선순위 규약 문서·`SkillInterface` 용어 실재; 레퍼런스 Skill 실물 미생성(미래 산출물, 실재 불주장); 실행 엔진 미도입(형태 B). 실측 불일치 0건(A5/L-07 재발 방지).
- 09 §3 계약 재정의·확장 0, 새 필드·새 사유 코드·새 연산 신설 0, Glossary 밖 새 용어 0, 새 바인딩 계약 창설 0. 구체 AI·환경·형식 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 동시 작성 형제 산출물(hooks-binding·framework/plugins/·시연 절차서) 불인용(07 R2), 조율 필요는 open_questions로(R3). 이 1파일만 생성(R4).
