# framework/adapters/claude/skills-binding — Claude Code Skills Adapter 바인딩

작성일: 2026-07-06
상태: v0.8 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본 (계약 요소는 § 포인터로만 인용 — 재정의 0 선언은 §0 1곳):

- specs/09-skills.md — §3.1-A~D 4연산 · §3.2-A Manifest 11필드·필수/선택·로드 계층 · §3.2-B I/O Contract · §3.2-C Failure Report(구조 = 01 §3.2-D 재사용, 사유 8종) · §3.3 INV-1~INV-8 · §4.1 Binding 표 7행 · §4.2 SP-1~5 · §9 결정 기록(OQ-S1 해소 순서·enum 소유 경계·Glossary 5건).
- specs/01-runtime.md §3.1-A·§3.2-A/B·§3.2-E·§4.1 · specs/02-agent.md §3.2-A(4역할 역할 경계 표) · specs/00-glossary.md §3.2-J J-09(용어 정본, 신설 0) · framework/core/structure.md §2·§5·§6·§8(Adapter 경계 = 격리 지점) · ROADMAP.md v0.8.
- 자매 Adapter Binding(관례 정본) — runtime-binding.md(§2 #3이 Skill 표면 상세를 09로 미룸 · §3.2 Register/Resolve · §3.3 Config 물리 소스) · memory-binding.md · verifier-binding.md · loop-binding.md.
- 자매 Adapter Binding(관례 정본) — runtime-binding.md(§2 #3이 Skill 표면 상세를 09로 미룸 · §3.2 Register/Resolve · §3.3 Config 물리 소스) · memory-binding.md · verifier-binding.md · loop-binding.md.
- ROADMAP.md v0.8 (Extension System) — Skills 완료 조건·산출물의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다 — Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 09 §3.3 INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 허용된다(C-3 비적용 — 자매 4문서 §0과 동형). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. `framework/adapters/claude/` 경계의 다섯 번째 Adapter Binding 산출물(선행: runtime·memory·verifier·loop-binding.md). 09 §4.1 바인딩 표 **7행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정)/실물 미생성(`.claude/skills/` 빈 디렉터리) 정직 구분(§2). Skill Manifest 직렬화 물리 정본 확정(§3 — `.claude/skills/<skill-id>/` 자기완결 단위, 메타데이터 9필드 = front-matter·`body` = Markdown 본문·`resources` = 본문 로드 계층의 로드 계층 분리(09 §3.2-A 필수/선택·로드 계층 정본 보존, 재정의 0), `contract` 값 = `SkillInterface` — Glossary §3.2-J J-09 / 09 §3.2-A 정본, 신설 아님). 발견·선택 물리 절차(§4 — front-matter `trigger` 평가·메타데이터만 사용·결정적·`NoMatchingSkill` 빈 결과·09 §9 결정 기록 모호성 해소 순서(명시 호출 > 가장 구체적 트리거 > `AmbiguousSelection`) 운용 전개). 지연 로드·호출·Config 주입·실패 물리 판정(§5 — 선택 본문만 로드·미선택 본문 비로드 판정법, 역할 경계 INV-2·우선순위 4단 INV-3 물리 판정, Config 주입 INV-5, Skill Failure Report 8사유 코드 물리 판정 표·enum 소유 경계 보존). 09 §4.2 이식 교체 지점 SP-1~5 대응 표("교체되는 것/유지되는 것" — 유지 열이 §3.2-A 필수 필드·§3.2-B I/O 계약·INV-2·INV-3·INV-4 전건 커버, §6). 상태 서술 실측 대조(§7 — 실재 서술 전건 파일 시스템 직접 실측 후 기입, L-07; `.claude/skills/` 빈 디렉터리·레퍼런스 Skill 실물 미생성 정직 기록, 실재 불주장). 09 §3 계약 재정의·확장 0, 새 필드·새 사유 코드·새 연산 신설 0, Glossary 밖 새 용어 0. 동시 작성 형제 산출물(hooks-binding·framework/plugins/ 문서·시연 절차서) 불인용(07 R2), 조율 필요는 open_questions로(R3). 이 1파일만 생성 — `.claude/skills/` 실물·픽스처·시연 산출물·자매 Baseline 산출물·specs/·docs/ 무수정(R4). | Worker (Advisor 위임, Task EX-S1) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지). `.claude/skills/`·loop-data/·memory-data/ 참조는 라이브/백엔드 경로로 무변경, 삭제 산출물 본문 참조 없음. 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 2 — 비계약 격리 개정: 재서술·스냅샷·죽은 참조 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/09-skills.md §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·필드·로드 계층·불변 규칙·사유 코드)를 **재정의·확장하지 않는다** — 계약 요소는 정본 § 포인터로만 인용한다. **이 재정의 0 선언은 문서 전체에 대해 여기 1곳에서만 선언되며**, 이하 각 절은 이를 반복 선언하지 않고 필요한 곳에서 정본 §만 지목한다.
- **소관 지점.** 09 §4.1이 "`.claude/skills/` 하위 직렬화·트리거 평가·지연 로드·등록 표면"으로 지목하고 runtime-binding.md §2 #3이 09로 미룬 **Skill 표면의 물리 실현**이 확정되는 유일한 자리가 이 문서다 — Skill Manifest 직렬화 파일 구조(§3)·발견/선택(§4)·지연 로드/호출·Config 물리 소스·실패 물리 판정(§5)을 확정한다. 계약 요소의 진위 판정 기준은 항상 09 §3.2-A 등 정본이며, 이 문서는 물리 표기만 확정한다.
- **격리 지점(C-3 비적용).** Core 경계·Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 하지만(structure.md §5 C-3 확장, 09 §3.3 INV-8), 이 문서는 그 **반대편**이다 — 직렬화 형식명(Markdown·front-matter)·물리 경로(`.claude/skills/…`·`~/.claude/…`)·명시 호출 표면·세션/턴·서브에이전트 토큰의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 4문서 §0 동형).
- **창설 금지.** 09 §4.1 표를 넘어서는 새 바인딩 계약·새 연산·필드·사유 코드·불변 규칙을 만들지 않는다. Skill 실물·픽스처·시연 산출물의 생성도 이 문서 소관이 아니다.
- **하네스 상태 전제(Bootstrap).** Skills는 정식 실행 Module이 아니라 규약 문서와 관행으로 실현된다(형태 A — 발견/선택/로드/호출을 호출 Agent가 자신의 턴에서 수행). 따라서 매핑은 **이미 실재하는 표면**과 **실행 코드 도입 시 로딩될 지점**(형태 B — 트리거 평가·지연 로더·우선순위 판정 엔진)을 구분한다. `형태 A/B`는 structure.md §4의 서술 라벨이고, Bootstrap 근거는 Glossary J-13·runtime-binding.md §0이다.
- **실측 기반 상태 서술(done 7, L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다. §2 "실재 여부" 열과 §7 표가 그 대상이며, 두 곳 모두 **재실측으로 참·거짓이 갈리는 형태**로만 쓴다(byte·계수 스냅샷 불기재 — drift). **정정(2026-07-26): `.claude/skills/`는 빈 디렉터리가 아니다** — `commit-message-writer/SKILL.md`·`discovery-interview/SKILL.md` 2단위가 실재하며, 각각 §3.1이 확정한 `<skill-id>/` 하위 디렉터리 자기완결 단위 형태다. 종전 판(2026-07-06)의 "빈 디렉터리·레퍼런스 Skill 실물 미생성" 서술은 그 시점 실측이었고 현재는 사실이 아니다. `uaf-verified: .claude/skills/ 직접 열람 — find -maxdepth 2 -type f 로 하위 전건 열거(2단위·정의 파일 2건)`
- 용어는 specs/00-glossary.md 정본만 사용한다(`Skill Manifest`·`Trigger`·`Skill Body`·`Skill I/O Contract`·`SkillInterface` = §3.2-J J-09, 09 §9 승인). 새 용어 신설 0.

---

## §1. 목적

이 문서는 09 §4.1(Skills Claude Code Binding)을 이 환경 위의 구체 물리 실현으로 매핑한다. 정본 경계·격리·창설 금지·실측 규율 선언은 §0에 1벌만 둔다.

절별 책임 — §2 바인딩 표 7행 물리 표면 매핑(done 1·7) · §3 Skill Manifest 직렬화 물리 정본(done 2) · §4 발견·선택 절차 + 해소 순서 운용 전개(done 3) · §5 지연 로드·호출·Config 주입·실패 물리 판정(done 4) · §6 09 §4.2 SP-1~5 대응(done 6) · §7 상태 서술 실측 대조(done 7).

형태 A → 형태 B 전환 시에도 Core Contract(09 §3) 변경은 0이며(structure.md §7 C-1), §6의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 09 §4.1 바인딩 표 7행 물리 실현 (done 1·7)

09 §4.1 표의 **7행 전부**를 물리 표면으로 매핑한다. "정본 인용(원문 그대로)" 열은 09 §4.1 정본 값을 그대로 인용하고, "물리 실현" 열은 이 환경의 파일 구조·절차·채널을 요지로 확정하며(상세는 §3~§5 소유 — 여기서 재서술하지 않는다), "실재 여부" 열은 물리 실재/형태 A/형태 B를 구분한다(§7).

물리 등록 표면 디렉터리 구조(본 문서 정본 — §3):

```
.claude/skills/                     # 확장 Module 표면(01 §4.1) — Skill 등록 루트. 실재
└─ <skill-id>/                      # Skill 자기완결 단위(01 §3.2-E 규칙 2) — 하위 1개 = Skill 1개. 실재(2단위 — §7)
   ├─ <definition>.md               #   Markdown + front-matter — front-matter=메타데이터 9필드(§3.2-A)·본문=body(§3.2-A)
   └─ (resources 자원)              #   resources(§3.2-A, 선택) 참조 대상 — Skill 경계 안 파일·도구(본문 로드 계층)
```

| # | §3 계약 요소 (정본 §) | 정본 인용 (원문 그대로 — 09 §4.1) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Skill Manifest(§3.2-A) 직렬화 | `.claude/skills/` 하위의 Markdown + front-matter 파일 (01 §4.1 확장 Module 표면과 정렬). 메타데이터 필드는 front-matter, `body`는 Markdown 본문. | Skill 1개 = `.claude/skills/<skill-id>/` 자기완결 단위(01 §3.2-E 규칙 2). 정의 파일 = Markdown + front-matter(메타데이터 9필드) + Markdown 본문(`body`), `resources` = 경계 안 자원. 필드·필수/선택·로드 계층 정본 = 09 §3.2-A · 물리 구조·표기 정본 = §3. | 표면·실물 모두 실재 — 하위 2단위(`commit-message-writer/SKILL.md`·`discovery-interview/SKILL.md`, §7). |
| 2 | Skill 등록(§3.1-A) | Runtime의 Module Register 바인딩(01 §4.1) 위에 Skill 표면으로 등록된다. | Register = 자기완결 단위를 `.claude/skills/<skill-id>/`에 배치(runtime-binding.md §3.2 동형 — 파일 배치 = 규약 실현). `id` 유일성 = 디렉터리 이름 충돌 없음(`DuplicateId` 방지), 필수 필드·`contract`=`SkillInterface` 검사는 등록 전(`ContractMismatch`). 완료 조건·사유 정본 = 09 §3.1-A(01 상속) · 판정 = §5.4. | 표면 규약 실현(형태 A, 파일 배치). 실행 Register(형태 B) 미도입. |
| 3 | Skill 발견·선택(§3.1-B) | 작업 컨텍스트에 대한 front-matter의 `trigger` 평가로 후보를 선정한다. | Discover&Select = 각 Skill front-matter `trigger`를 컨텍스트에 평가해 매칭 Skill만 후보 · 본문 비로드(INV-4) · 결정적(INV-7) · 후보 0 = `NoMatchingSkill` 빈 결과(실패 아님). 절차 정본 = §4(해소 순서 §4.2). | 규약 실현(형태 A — 호출 Agent가 자신의 턴에서 평가). 무인 트리거 엔진(형태 B) 미도입. |
| 4 | Skill 로드(§3.1-C, 지연) | 선택된 Skill의 Markdown 본문만 Context에 로드한다. front-matter는 항상 열람 가능, 본문은 선택 시 로드. | Load = 선택 `<skill-id>/` 정의 파일의 Markdown 본문(`body`)만 Context 로드 · `resources` 참조 해소 · 미선택 Skill 본문 비로드(INV-4). 절차·`SkillBodyUnavailable`/`ResourceUnresolved` 판정 = §5.1·§5.4. | 규약 실현(형태 A — 선택 시 본문 판독). 실행 로더(형태 B) 미도입. |
| 5 | Skill 호출(§3.1-D) | 로드된 본문 절차를 호출 Agent가 자신의 역할 경계(02 §4) 안에서 수행한다. | Invoke = 로드된 `body`를 호출 Agent(`.claude/agents/<role>.md` 서브에이전트)가 02 §3.2-A 역할 경계 안에서 수행. 경계 밖 지시 = `RoleBoundaryViolation`(INV-2) · 상위 규약 충돌 = `PrecedenceConflict`(INV-3 4단) · 입력 불일치 = `InputContractMismatch`. 판정·보고 = §5.2·§5.4. | 규약 실현(형태 A — 호출 Agent가 자신의 턴에서 판정). 실행 강제 엔진(형태 B) 미도입. |
| 6 | 필요 자원(`resources`) | Skill 경계 안의 파일·도구 참조. | `resources`(선택·본문 로드 계층) = `.claude/skills/<skill-id>/` 경계 안 자원 파일·도구 참조. `body`와 함께 선택 시 로드·해소(미해소 = `ResourceUnresolved`). 자기완결 단위이므로 경계 안 co-located. | 물리 위치·해소 규칙 확정(정본, §3·§5.1). 실재 2단위의 정의 파일은 각 `<skill-id>/SKILL.md` 1건(자원 파일 유무는 재실측 대상 — §7). |
| 7 | Config 주입 | 01 §3.2-B Config로 프로젝트 특정 값을 주입한다 (하드코딩 금지, INV-5). | Config 주입 = 스코프별 물리 소스(runtime-binding.md §3.3 동형 — Global `~/.claude/settings.json` · Project `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json` · Module = Skill 정의 설정 블록) 또는 호출 Agent가 제공하는 `input`(§3.2-B). `body` 하드코딩 금지(INV-5). 병합·우선순위(Module > Project > Global) 정본 = 01 §3.2-B · 상세 = §5.3. | Config 물리 소스 실재(runtime-binding.md §3.3 승계). effective config 로딩(형태 B) 미도입. |

주:

- **형태 A / 형태 B 구분(정직).** 행 2(등록)·3(발견)·4(로드)·5(호출)은 Bootstrap에서 **규약 실현(형태 A)** — 호출 Agent가 자신의 턴에서 파일 배치·front-matter 평가·본문 판독·역할 경계 판정을 수행한다. 무인 자동 실행 엔진(트리거 평가·지연 로더·우선순위 판정)과 effective config 로딩은 형태 B로 미도입이다(§7).
- **Skill = 확장 Module.** Skill은 Agent가 아니라 `.claude/skills/` 확장 Module 표면에 등록되는 능력 단위이며(09 §2, runtime-binding.md §2 #3), Register/Resolve가 Runtime Module 계약(01 §3.1-A)을 상속·구현한다(INV-6, 재정의 0). 등록·교체·안정 식별자 규칙은 01 Module 계약을 그대로 따른다.

---

## §3. Skill Manifest 직렬화 물리 정본 (done 2)

09 §4.1이 "Adapter Binding 소관"으로, runtime-binding.md §2 #3이 재차 09로 미룬 Skill Manifest 직렬화의 물리 실현을 확정한다. 필드·필수/선택·로드 계층의 정본은 09 §3.2-A이며, 본 절은 그 물리 표기만 확정한다(새 필드 0).

### §3.1 물리 파일 구조 — Skill 자기완결 단위 (01 §3.2-E 규칙 2)

- **위치·단위.** Skill 1개는 `.claude/skills/<skill-id>/` 하위 디렉터리 1개를 **자기완결 단위**(01 §3.2-E 규칙 2 — Manifest·구현·자원을 한 경계 안에)로 차지한다. `<skill-id>`는 Skill Manifest `id`(09 §3.2-A, 안정 식별자 — 01 INV-7)이며, 하위 디렉터리 이름이 `id`의 유일성 매체다(같은 이름 배치 실패 = `DuplicateId`, §5.4).
- **정의 파일.** 그 단위 안의 정의 파일은 **Markdown + front-matter**다(09 §4.1). front-matter가 메타데이터 필드를, Markdown 본문이 `body`를 담는다(§3.2). `resources`(선택)가 참조하는 자원 파일·도구는 같은 `<skill-id>/` 경계 안에 co-located된다(본문 로드 계층).
- **구조 근거.** 하위 디렉터리 자기완결 단위는 (i) 01 §3.2-E 규칙 2의 직접 물리 실현이고, (ii) `resources`가 정의 파일과 한 경계에 모여 Skill 제거 시 잔여물 0(INV-1)을 물리 보장한다. `resources`가 없는 Skill은 정의 파일 단일로 축약되는 퇴화형이다. 하위 디렉터리 대 단일 파일의 물리 형태 선택은 SP-1·SP-2에 속하며(§6), 실재 2단위가 하위 디렉터리 형태를 취한다(§7 — OQ-SB-1 참조).
- **직렬화 형식 = Adapter 선택.** Markdown + front-matter는 09 §4.1이 지정한 이 환경의 형식이며, 이식 시 대상 환경의 Skill 정의 메커니즘으로 교체된다(SP-1·SP-2). 형식 선택은 09 §3.2-A 추상 스키마를 바꾸지 않는다.

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

- **로드 계층의 물리 보장.** 메타데이터 9필드는 front-matter에 있어 발견·선택 단계에서 항상 열람되고(§4), 본문 로드 계층 2필드(`body`·`resources`)는 선택 뒤에만 로드된다(§5.1). 이 저장 분리가 INV-4(지연 로드)의 물리 기반이며, 발견·선택이 본문을 로드하지 않음을 물리적으로 보장한다.
- **필수/선택·`contract` 값 보존.** 8필드 필수 / 3필드(`resources`·`requires`·`replaceable`) 선택의 지위는 09 §3.2-A 정본이며 물리 직렬화가 이를 바꾸지 않는다(`replaceable` 생략 시 기본 `true`). `contract` 값 `SkillInterface`는 Glossary §3.2-J J-09 / 09 §3.2-A 정본으로, 본 문서는 물리 표기(front-matter 값)만 바인딩한다 — 새 계약·새 용어 신설 0.

---

## §4. 발견·선택(Discover&Select) 물리 절차 · 모호성 해소 순서 운용 전개 (done 3)

09 §3.1-B(Discover&Select)의 계약 — 입력=작업 컨텍스트, 출력=후보 목록·선택, 완료 조건=trigger 평가·결정적, 제약=메타데이터만 사용, 실패=`AmbiguousSelection`/`NoMatchingSkill` — 을 이 환경의 물리 절차로 확정한다. 계약 정본은 09 §3.1-B·INV-4·INV-7이다.

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

09 §9 결정 기록의 해소 순서 — **명시 호출 > 가장 구체적인 트리거 매칭 > `AmbiguousSelection` 실패·에스컬레이션** — 을 물리 절차로 전개한다. **순서는 09 §9 정본이 소유하고, 본 절은 각 단계의 물리 실현만 확정한다**(09 §9 "상세 규칙은 v0.8 구현 시 정밀화 가능 — 계약 골격 확정").

1. **명시 호출(1순위).** 작업 컨텍스트가 특정 Skill을 명시적으로 지정하면(물리 표면 = 명시적 Skill 지정, 예: 슬래시 형태 `/<skill-id>` 또는 skill id 직접 참조) 그 Skill이 즉시 선택된다 — 다른 후보의 trigger 매칭 여부와 무관하게 명시 호출이 이긴다. 명시된 `<skill-id>`가 등록되어 있지 않으면 그 명시 호출은 후보가 되지 못한다(그 경우 2로 진행하거나 `NoMatchingSkill`).
2. **가장 구체적인 트리거 매칭(2순위).** 명시 호출이 없고 후보가 2개 이상이면, front-matter `trigger`가 작업 컨텍스트에 **가장 구체적으로** 매칭되는 Skill을 선택한다(더 좁은·더 제약된 trigger가 이긴다). "가장 구체적"의 정밀 척도(예: trigger 조건의 좁힘 정도)는 이 Adapter의 구현 선택이며 이식 교체 지점 SP-3(트리거 평가 메커니즘)에 속한다 — 순서(명시 > 구체 > 실패)는 09 §9 정본으로 불변이다.
3. **`AmbiguousSelection`(3순위, 실패·에스컬레이션).** 1·2로도 결정적 선택이 불가하면(동등하게 구체적인 다수 후보) `AmbiguousSelection`으로 보고하고 에스컬레이션한다(§5.4). 이는 결정적이어야 한다는 제약(INV-7)과 정합한다 — 임의 선택으로 우회하지 않는다.

---

## §5. 지연 로드(Load)·호출(Invoke)·Config 주입·실패 물리 판정 (done 4)

09 §3.1-C(Load)·§3.1-D(Invoke)의 계약과 Config 주입(01 §3.2-B, INV-5)·실패 물리 판정(09 §3.2-C 8사유 코드)을 물리 절차로 확정한다. 계약 정본은 09 §3.1-C·§3.1-D·§3.2-C·§3.3 INV-2~INV-5·02 §3.2-A다.

### §5.1 지연 로드(Load) 물리 절차 · 미선택 본문 비로드 판정법 (09 §3.1-C, INV-4)

| 09 §3.1-C 계약 단계 | 물리 실현 (claude 환경) | reason (실패 시 — §5.4) |
|---|---|---|
| **1** — 선택된 skill id 입력 | §4에서 선택된 `<skill-id>` 1건을 로드 입력으로 받는다. | — |
| **2** — 선택 Skill 본문만 로드 | 선택된 `.claude/skills/<skill-id>/` 정의 파일의 **Markdown 본문(`body`)만** Context에 로드한다. front-matter는 발견 단계에서 이미 열람됨(메타데이터). 본문이 없거나 판독 불가면 실패. | `SkillBodyUnavailable` (09 §3.1-C) |
| **3** — `resources` 참조 해소 | `body`가 참조하는 `resources`(선택)를 `<skill-id>/` 경계 안에서 해소한다. 참조 대상 자원 파일·도구가 부재·미해소면 실패. | `ResourceUnresolved` (09 §3.1-C) |
| **4** — 미선택 Skill 본문 비로드(INV-4) | 미선택 Skill의 Markdown 본문은 Context에 로드하지 않는다. front-matter만 발견 단계에서 열람됐을 뿐이다. | — (위반 시 §7 검증 실패로 판정 — 09 §6) |

- **미선택 본문 비로드 판정법(done 4).** 로드 후 Context를 대상으로, **선택된 `<skill-id>` 외 Skill의 Markdown 본문 텍스트가 Context에 존재하지 않음**을 확인한다(09 §7 검증 방법). front-matter(메타데이터)는 발견 단계 열람이 정당하나, 본문은 오직 선택된 Skill의 것만 존재해야 한다. 미선택 본문이 Context에 있으면 INV-4 위반으로 검증 실패다(09 §6). Bootstrap(형태 A)에서는 호출 Agent의 본문 판독으로, 형태 B 도입 시에는 지연 로드 메커니즘으로 실현되며 INV-4 계약은 불변이다(SP-4).

### §5.2 호출(Invoke) 물리 절차 · 역할 경계(INV-2)·우선순위 4단(INV-3) 물리 판정 (09 §3.1-D)

로드된 `body` 절차를 호출 Agent(`.claude/agents/<role>.md` 서브에이전트)가 자신의 역할 경계(02 §3.2-A 표) 안에서 수행한다 — Skill은 호출 Agent가 이미 가진 권한 안에서만 실행되며 역할 경계를 확장·우회할 수 없고(INV-2), Skill 지시가 상위 규약과 충돌하면 상위가 이긴다(INV-3).

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

- **물리 판정 방식·형태 구분.** 호출 Agent는 로드된 `body`(계층 4)의 각 지시를 자신의 역할 정의(`.claude/agents/<role>.md` + 02 §3.2-A, 계층 3)와 상위 규약(계층 1·2)에 대조한다 — 역할 밖이면 `RoleBoundaryViolation`(지시 무효), 상위 계층과 충돌이면 `PrecedenceConflict`(상위 우선·Skill 지시 무시). 계층 1~3 문서는 이 환경에 물리 실재한다(§7). Bootstrap(형태 A)에서 이 판정은 호출 Agent가 자신의 턴에서 수행하되 자기 점검을 최종 승인으로 삼지 않으며(02 §3.2-A), 독립 판정은 Verifier(09 §7)·최종 승인은 Advisor다. 실행 강제 엔진(형태 B) 도입 시에도 INV-2·INV-3은 불변이다(SP-3).

### §5.3 Config 주입 물리 소스 (01 §3.2-B, INV-5)

Skill의 I/O 계약과 `body`는 프로젝트 비의존으로 작성되고, 프로젝트 특정 값은 Config나 `input`으로 주입되며 `body`에 하드코딩되지 않는다(INV-5, 09 §3.2-B). 주입 경로는 둘이다.

- **주입 경로 1 — Config(01 §3.2-B).** Config 스코프별 물리 소스는 runtime-binding.md §3.3 동형이다: Global = `~/.claude/settings.json`, Project = `.claude/CLAUDE.md`·`.claude/AGENT.md`·`.claude/settings.local.json`, Module scope = 해당 Skill 정의의 설정 블록(`target` = `<skill-id>`). 병합·우선순위(Module > Project > Global)의 정본은 01 §3.2-B·config-schema.md §4.2이며, 본 문서는 물리 소스만 바인딩한다(재정의 0).
- **주입 경로 2 — `input`(09 §3.2-B).** 호출 Agent가 Invoke 시 `io.input`에 맞는 입력으로 프로젝트 특정 값을 제공한다. 이것이 재사용성의 기반(INV-5)이다 — 동일 Skill이 재등록만으로 다른 프로젝트에 재사용된다.
- **하드코딩 금지 판정.** `body`에 프로젝트 특정 값이 하드코딩되어 있으면 INV-5 위반이며 Config·입력 주입으로 교정한다(09 §6).

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
- **enum 소유 경계 보존(09 §9).** `ContractMismatch`·`DuplicateId`는 01 §3.2-D enum 상속(Register), 나머지 6개는 09 소유(Skill 특화 연산)다. 본 문서는 이 경계를 재정의하지 않고 물리 판정 지점만 바인딩한다.
- **Lesson 후보 경로.** Skill 호출 실패는 Lesson 후보이며(09 §5·§6), 기록은 호출 Agent의 실패 보고(02 §3.2-D)와 Memory Update(02 §5, 단일 Port)를 경유한다 — Skills는 Memory로 향하는 두 번째 경로를 열지 않는다(INV-8). 포인터만 둔다.

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
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(09 §4.2 말미·자매 바인딩 §4/§6 동형). 본 문서는 그 정식화를 선취하지 않는다(창설 금지, §0). Invoke의 역할 경계(INV-2)·우선순위(INV-3)·I/O 계약(§3.2-B)은 특정 SP에 귀속되는 "교체되는 것"이 아니라 모든 이식에서 유지되는 계약이며, 위 표 SP-3 유지 열에 명시했다.

---

## §7. 상태 서술 실측 대조 (done 7 — A5/L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 본 문서의 "실재/존재" 서술을 파일 시스템과 직접 대조한다. **byte 스냅샷·일자 박힌 계수는 두지 않는다** — 자매 문서 크기·하위 항목 계수는 drift 대상이며, 남기는 것은 재실측으로 참·거짓이 갈리는 불변 주장뿐이다(2026-07-26 슬림화에서 종전 판의 byte 5종·`0건` 계수 제거).

| 대상 | 실측 판정 (재실측 대상) |
|---|---|
| `framework/adapters/claude/` 경계 | 실재 — 자매 바인딩 문서군이 이 경계에 co-located. |
| 자매 Adapter Binding — runtime·memory·verifier·loop·workflow-binding.md(관례 정본; workflow는 물리 존재만·내용 불인용) | 실재 5건 전건(2026-07-26 재확인). byte 불기재. |
| `.claude/skills/` (§2 #1 등록 표면) | **실재 + 비어 있지 않음** — 하위 Skill 2단위. 종전 판의 "빈 디렉터리"는 2026-07-06 시점 실측이며 현재는 사실이 아니다(§0 정정). `uaf-verified: find .claude/skills -maxdepth 2 -type f` |
| `.claude/skills/<skill-id>/` Skill 실물 (§2 #1·#6, §3) | **실재 2단위** — `commit-message-writer/SKILL.md`·`discovery-interview/SKILL.md`. 각 단위가 §3.1이 확정한 하위 디렉터리 자기완결 단위 형태를 취한다(OQ-SB-1 제안 형태의 실물 확증). |
| `.claude/agents/` 역할 정의 파일 (§5.2) | 실재 — advisor·planner·verifier·worker(2026-07-26 재확인). |
| 우선순위 4단 물리 근거 (§5.2) — 계층 1~3 규약 문서 | 실재 — `ARCHITECTURE.md`·`.claude/AGENT.md`·`.claude/CLAUDE.md`·specs/02 §3.2-A. |
| Config 물리 소스 (§5.3) | 실재(자매 문서 실측 승계) — runtime-binding.md §3.3 소스 목록. |
| `SkillInterface` 용어 (§3.2 `contract` 값) | 실재 — specs/00-glossary.md §3.2-J J-09(신설 아님). |
| Skill 트리거 평가·지연 로드·호출 실행 진입점·로더 (형태 B) | 미도입 — Bootstrap(형태 A). 실행 엔진 코드 0. |

- **핵심 구분(불변).** 본 문서가 소유하는 것은 직렬화 파일 구조·로드 계층 물리 표기·발견/선택·지연 로드/호출 물리 절차·실패 물리 판정의 **정본**(§3~§5)이다. Skill 실물의 생성·수정은 본 문서 소관이 아니며, 실물 존재 여부는 위 표의 재실측으로만 판정한다 — 실재를 주장하는 행은 전건 파일 시스템 직접 실측 후에만 기입한다(A5/L-07 재발 방지).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **계약 소유 지도.** Manifest 필드·로드 계층 = 09 §3.2-A / Glossary J-09 · I/O 계약 = 09 §3.2-B · Failure Report 구조·사유 코드 = 09 §3.2-C(구조 01 §3.2-D 재사용, 소유 경계 09 §9) · 4연산 완료 조건 = 09 §3.1-A/B/C/D · 불변 규칙 = 09 §3.3 · 모호성 해소 순서 = 09 §9 · 역할 경계 = 02 §3.2-A · Config 병합 = 01 §3.2-B. 본 문서는 이들의 **물리 실현**만 확정한다.
- **작성 경계 이력(포인터).** 초판(2026-07-06, Task EX-S1)의 동시 작성 형제 불인용(07 R2)·조율 에스컬레이션(R3)·1파일 생성 범위(R4) 감사 흔적은 git 이력(초판 커밋)에 보존되어 있다. `uaf-allow-legacy: 초판 감사 흔적은 git 이력에 보존, 본문은 포인터 1줄`

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-SB-1 (Skill 자기완결 단위 물리 형태 = Adapter 선택 — 비차단).** 09 §4.1은 직렬화 형식만 지정하고 자기완결 단위를 **하위 디렉터리**로 둘지 **단일 파일**로 둘지 확정하지 않았다. §3.1은 하위 디렉터리를 정본으로 제안했고(근거: 01 §3.2-E 규칙 2 + resources co-location + INV-1 잔여물 0), 실재 2단위가 그 형태를 취한다(§7 — 제안 형태의 실물 확증). 정식 채택 판정은 Advisor 대상이며 계약(09 §3.2-A) 변경이 아니므로 비차단이다.
- **OQ-SB-2 (모호성 해소 "가장 구체적" 정밀 척도 — 비차단).** 09 §9는 해소 순서 골격만 확정하고 상세 규칙을 v0.8 구현 시 정밀화로 두었다. trigger 좁힘 정도의 정밀 척도는 이 Adapter의 구현 선택(SP-3)이며, 순서(09 §9 정본) 변경이 아니므로 비차단이다.
- **OQ-SB-3 (08/10 조율 — 해소).** 초판 시점 "동시 작성 중·불인용"이었던 자매 바인딩이 실재한다 — `hooks-binding.md`·`plugins-binding.md`(2026-07-26 실측). Plugin 번들 Skill의 등록 경로는 09 §9 결정(10 §3.1 Activate가 01 Register 경유 = 09 등록 계약과 동일)이 정본이며 본 문서 §2 #2와 정합한다. 잔여 조율 필요는 없다.

---

## §10. 요약 (1줄)

- 이 문서 = 09 §4.1(Skills 바인딩 표 7행)의 물리 실현 매핑 — 절 지도·상태·정본 경계는 §1·§2·§7·§0이 소유하며 여기서 재서술하지 않는다.
