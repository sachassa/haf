# Grill Me 독립 분석 보고서

> 이 파일은 **조사 보고서**다. 구현 계획이 아니다.
> 이번 단계의 산출물은 문서/코드 변경 0 — 사용자 지시(금지 사항)에 따라 UAHF 비교·적용·설계는 일절 수행하지 않았다.
> 조사 일자: 2026-07-14. 대상 upstream HEAD: `170ad486` (2026-07-13).

---

## ⚠️ 선행 정정 — 사용자 전제 오류

사용자 제시 전제: *"원본과 로컬 grilling instruction이 문자 단위로 일치"*
→ **거짓이다.** (현재 upstream `main` 기준)

| 파일 | sha256 | 크기 | 판정 |
|---|---|---|---|
| 로컬 `~/.claude/skills/grilling/SKILL.md` | `fe00af3e…c20f` | 666 B | — |
| upstream `bc4cf903` (2026-06-17) 동일 경로 | `fe00af3e…c20f` | 666 B | **완전 일치** |
| upstream `main` = `170ad486` (2026-07-13) | `44331dda…587` | 843 B | **불일치** |

- 로컬 `grilling` = **2026-06-17 스냅샷**. 이후 3개 커밋이 반영되지 않았다.
  누락: ① confirmation gate ② facts/decisions 분리 ③ general-use 재서술.
- 로컬 `grill-me` = upstream HEAD와 **일치**(2026-05-31 이후 무변경이므로 최신).
- 결론: 사용자의 §6 질문("최신 버전에서는 왜 사용자 확인 전 실행하지 않는가")이 가리키는 그 문장은 **로컬 설치본에 존재하지 않는다.**

검증 범위·한계: `C:\Users\aime8\.claude` 하위 depth 4, `projects/` 제외 스윕 → `grill*` 매치는 위 2개 디렉터리뿐. `plugins/installed_plugins.json`에 mattpocock-skills 없음(설치 플러그인 = skill-creator, telegram 2종). 프로젝트 로컬 `.claude/skills/`는 미스윕.

---

## A. Source & Version

**Repository** `github.com/mattpocock/skills` — public, MIT, "Skills for Real Engineers. Straight from my .claude directory." 플러그인 이름 `mattpocock-skills`, `.claude-plugin/plugin.json` version **1.2.0**.

**정확한 경로 (upstream main)**
- 본체: `skills/productivity/grilling/SKILL.md` ← **행동을 만드는 유일한 파일**
- wrapper 1: `skills/productivity/grill-me/SKILL.md` (7행, `disable-model-invocation: true`)
- wrapper 2: `skills/engineering/grill-with-docs/SKILL.md` (7행, "Run a `/grilling` session, using the `/domain-modeling` skill.")
- Codex 메타: `*/agents/openai.yaml` (UI 표시명뿐. 로직 0)
- 사람용 문서: `docs/productivity/grilling.md`, `docs/productivity/grill-me.md`
- 설계 규약: `.agents/invocation.md`, `skills/productivity/writing-great-skills/SKILL.md`
- 정책: `.out-of-scope/question-limits.md` (질문 수 상한 = **명시적 out-of-scope**)

**커밋 계보 (grill-me → grilling)**

| # | commit | date | 변화 |
|---|---|---|---|
| 1 | `78649baa` | 2026-02-25 | `grill-me/SKILL.md` **최초 생성**. frontmatter 없음. 본문 **2문장 28단어** |
| 2 | `d1beb4fe` | 2026-03-13 | frontmatter 추가 + "codebase 탐색" 문장 추가 |
| 3 | `fb3629d3` | 2026-03-19 | **"provide your recommended answer"** 추가 |
| 4 | `a6bdfd9f` | 2026-03-26 | **"Ask the questions one at a time."** 추가 |
| 5 | `383b6a06` → `62f43a18` | 2026-04-28 | 경로 이동(root → `skills/` → `skills/productivity/`) |
| 6 | `221ffca9` | 2026-05-31 | **`grilling` 추출** — 본문이 grilling으로 이동, grill-me는 wrapper 1줄로 축소. `grill-with-docs` 동시 신설 |
| 7 | `800201f7` | 2026-05-31 | grilling description 축약(트리거 중심) |
| 8 | `bc4cf903` | 2026-06-17 | **"Asking multiple questions at once is bewildering."** 추가 ← **로컬 설치본은 여기서 멈춤** |
| 9 | `0e9a0727` | 2026-07-03 | **confirmation gate** + description에 `Grill` leading word |
| 10 | `e5932a7a` | 2026-07-06 | **facts vs decisions 분리** (자기-grilling 버그 수정) |
| 11 | `170ad486` | 2026-07-13 | 소프트웨어 한정 어휘 제거(범용화). **현 HEAD** |

**분량 추이 (본문, frontmatter 제외)**

| 버전 | 단어 | 문장 | 문단 |
|---|---|---|---|
| origin `78649baa` | 28 | 2 | 1 |
| 로컬 = `bc4cf903` | 71 | 6 | 3 |
| HEAD `170ad486` | 106 | 8 | 4 |

→ **5개월간 28단어 → 106단어.** "몇 줄"이라는 규모는 과장이 아니다.

---

## B. Runtime Structure

### 실물 사실 (DIRECT)
- 로컬 설치 디렉터리 재귀 열거(`-Force`): `grilling/SKILL.md` (666 B), `grill-me/SKILL.md` (147 B). **그 외 파일 0.**
- 스크립트 없음. 상태 파일 없음. 실행 코드 없음. 하네스에 별도 엔진 없음.
- upstream에도 grilling 폴더 안에는 `SKILL.md` + `agents/openai.yaml`(UI 메타 2줄)뿐.

### 실제 호출 경로
```
사용자가 /grill-me 입력
  └─ 하네스가 grill-me/SKILL.md 본문을 컨텍스트에 주입
       본문 전체 = "Run a `/grilling` session."          ← 1문장
  └─ 모델이 Skill(grilling) 호출                          [STRONG INFERENCE]
       └─ grilling/SKILL.md 본문(4문단)이 컨텍스트에 주입  ← 여기서 행동이 생긴다
  └─ 모델의 다음 assistant 턴 = 질문 1개
  └─ 사용자 답변 (= 새 user 턴)
  └─ instruction은 여전히 컨텍스트에 살아있음 → 다음 질문 1개
  └─ … 반복 …
  └─ 사용자가 "됐다/맞다" 확인 → (HEAD만) 실행 허가
```

### 이 세션 자체가 증거 (DIRECT)
지금 이 세션의 available-skills 목록에는 `grilling`이 **로컬 description 그대로** 실려 있고, `grill-me`는 **없다**. → `disable-model-invocation: true`의 의미(모델은 못 부름, 사람만 `/grill-me`로 부름)가 런타임에서 실제로 관철됨을 자기 관측으로 확인.

### 각 질문에 대한 답

| 질문 | 답 | 등급 |
|---|---|---|
| 어떤 명령으로 시작? | `/grill-me` (사람만) 또는 `/grilling`, 또는 모델이 grilling을 자율 호출 | DIRECT |
| 어떤 파일이 로드? | `SKILL.md` 본문 텍스트뿐 | DIRECT |
| instruction은 언제 주입? | Skill 호출 시점, 1회. 이후 재주입 없음 | STRONG INFERENCE |
| 별도 코드? | **없음** | DIRECT |
| 별도 state machine? | **없음** — 상태·전이 정의 문자열 자체가 부재 | DIRECT |
| 별도 memory/state 저장? | **없음.** docs가 명시: *"grill-me is **stateless**: it writes nothing and leaves no workspace behind."* | DIRECT |
| 반복 질문은 무엇이 발생시키나? | "one at a time + waiting for feedback"가 매 턴을 1질문으로 절단 → 대화 턴 자체가 loop가 됨 | STRONG INFERENCE |
| 질문 순서는 무엇이 결정? | "each branch of the decision tree, resolving dependencies … one-by-one" — 모델의 의존성 판단 | DIRECT(문구) / STRONG INFERENCE(실행) |
| 종료는 무엇이 결정? | "until we reach a shared understanding" + (HEAD) 사용자 확인. **수치 상한 없음 — 명시적으로 거부됨** | DIRECT |
| 사용자 확인 처리? | HEAD: "Do not act on it until I confirm…" 한 문장. 파싱·플래그 없음 | DIRECT |

---

## C. Original Instructions (원문)

### C-1. origin `78649baa` (2026-02-25) — frontmatter조차 없음
```
Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
```

### C-2. 로컬 설치본 = upstream `bc4cf903` (666 B)
```markdown
---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

### C-3. upstream HEAD `170ad486` (843 B)
```markdown
---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.
```

### C-4. grill-me (로컬 == HEAD, 147 B)
```markdown
---
name: grill-me
description: A relentless interview to sharpen a plan or design.
disable-model-invocation: true
---

Run a `/grilling` session.
```

---

## D. Instruction-by-Instruction Behavioral Analysis

> HEAD 본문을 **8개 독립 mechanism**으로 분해한다. 문단 아닌 문장/절 단위.

### ★ 전역 관측: 문장의 **인칭**
본문은 "Interview **me**", "asking **me**", "The decisions … are **mine**", "**I** confirm" — 전부 **사용자 1인칭 화자**다. 스킬 기술서(3인칭 명세)가 아니라 **사용자가 모델에게 직접 내리는 상시 지시문**의 형태다. 컨텍스트에 주입되는 순간 모델에게는 "방금 사용자가 이렇게 말했다"에 준하는 압력으로 읽힌다. 이것은 3인칭 명세보다 준수 압력이 높다. (DIRECT = 텍스트 인칭 / STRONG INFERENCE = 준수 효과)

---

### S1. `Interview me relentlessly about every aspect of this`
- **문자 그대로**: 나를 인터뷰하라. 가차없이. 이것의 모든 측면에 대해.
- **요구 행동**: 역할 반전. 모델=질문자, 사용자=피면접자.
- **행동 변화**: 기본 LLM은 요청을 받으면 **답을 생산**한다. 이 절은 출력 모드를 **답변 생산 → 질문 생산**으로 전환한다. 이것이 grilling의 1차 원인이다.
- **`relentlessly`의 역할**: 저자 자신의 이론서(`writing-great-skills`)가 이 단어를 **직접 예시로 든다**: *"A weak leading word (be thorough when the agent is already thorough-ish) is a **no-op**; the fix is a stronger word (**relentless**)."* → `relentlessly`는 장식이 아니라 **조기 종료 억제 장치**로 의도적으로 선택된 단어다. (DIRECT)
- **`every aspect`의 역할**: 질문 범위를 전수로 확대 → 질문 소재 고갈을 막는다.
- **없을 때의 실패**: 모델이 1~3개 확인 질문 후 곧장 계획을 써낸다(= 기본 행동).
- **반복 질문 영향**: 질문 **개수의 하한**을 만든다.
- **종료 영향**: 조기 종료를 억제(= 종료를 어렵게 만듦).
- **주도권 영향**: 대화의 진행 주도권을 모델에게, **내용 결정권**은 사용자에게 남긴다.

### S2. `until we reach a shared understanding`
- **문자 그대로**: 공유된 이해에 도달할 때까지.
- **요구 행동**: 종료 술어(termination predicate)를 정의한다. **유일한 종료 조건**이다.
- **핵심**: 술어가 `we`(1인칭 복수)다. 모델 혼자 만족해서는 성립하지 않는 **양자 술어**다. → 모델이 스스로 "끝났다" 선언하기 구조적으로 어렵다.
- **없을 때**: `relentlessly`만 남아 무한 질문 또는 임의 종료. 정지 개념 자체가 사라진다.
- **상호작용**: S8(confirmation gate)이 이 술어를 **관측 가능한 이벤트**(사용자 발화)로 물리화한다. S2 단독은 모델 내부 판단, S2+S8은 외부 관측.
- **종료 영향**: 종료 판정 = LLM 판단. **알고리즘 아님.**
- **주도권**: `we` 때문에 사용자가 종료의 절반을 쥔다.

### S3. `Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.`
- **문자 그대로**: 결정 트리의 각 가지를 내려가라. 결정 간 의존성을 하나씩 해소하며.
- **요구 행동**: 질문 **순서**를 규정한다 — 무작위/평면적 나열이 아니라 **의존성 위상 순서**.
- **행동 변화**: 부모 결정을 먼저 확정하고, 그 답에 따라 자식 질문 집합을 **재생성**한다. → 질문이 사용자의 이전 답에 **의존**하게 된다(= adaptive).
- **`decision tree` = leading word**: 자료구조가 아니다. 트리를 만들라/저장하라/그리라는 지시가 **어디에도 없다**. 저자 문서도 *"The **mental model** is a decision tree"*라고 못박는다. (DIRECT)
- **없을 때**: 질문이 체크리스트처럼 평면적으로 나오고, 후속 질문이 앞 답변을 반영하지 못한다. 수렴하지 않는다.
- **상호작용**: S4(1문/턴)와 결합해야 의미가 산다 — 한꺼번에 물으면 트리 구조가 붕괴한다(저자 문서: *"a firehose of parallel questions loses the structure that makes the interview converge"*).
- **반복 질문 영향**: 질문의 **내용과 순서**를 결정.
- **종료 영향**: "모든 branch를 방문함" = 수렴의 조작적 정의를 제공.

### S4. `For each question, provide your recommended answer.`
- **문자 그대로**: 각 질문마다 네 추천 답을 제시하라.
- **요구 행동**: 질문 = 열린 질문(open question)이 아니라 **제안 + 검토 요청**.
- **행동 변화**: 사용자 응답 비용을 급락시킨다. 백지 답변 → 예/아니오/수정. 저자 문서: *"you are **reacting to a proposal**, not staring at a blank prompt."* (DIRECT)
- **부수 효과 (중요)**: 모델이 매 질문마다 **자기 입장을 선언**해야 한다 → 모델의 암묵적 가정이 표면화되고, 사용자가 그것을 반박할 수 있게 된다. 즉 이 문장은 사용자 편의 장치인 동시에 **모델 가정 노출 장치**다.
- **없을 때**: 세션이 취조(interrogation)가 된다. 사용자 피로 급증 → 중도 포기. (이슈 #44 코멘트: *"feels like I'm being tested"*)
- **주도권 영향**: 양면적 — 사용자 부담을 줄이지만, **앵커링**을 만든다(모델 추천이 기본값이 됨).

### S5. `Ask the questions one at a time, waiting for feedback on each question before continuing.`
- **문자 그대로**: 한 번에 하나씩 물어라. 각 질문의 피드백을 기다린 뒤 계속하라.
- **요구 행동**: 턴당 질문 수 = 1. 그리고 **차단(blocking)** — 답을 받기 전엔 진행 금지.
- **★ 이것이 loop를 만드는 문장이다.** 상세는 §F.
- **두 절은 서로 다른 mechanism이다**:
  - `one at a time` = 질문 **개수** 제약 (배치 금지)
  - `waiting for feedback … before continuing` = **동기화** 제약 (질문 후 반드시 턴 종료 → 사용자 입력 대기)
  - 앞 절만 있으면 "질문 1개 던지고 스스로 답하고 다음으로" 가 가능하다. 뒤 절이 그걸 막는다.
- **없을 때**: 질문 10개를 한 번에 덤프 → 1턴에 종료 → **반복 자체가 발생하지 않는다.** grilling이 grilling이 아니게 된다.
- **종료 영향**: 종료를 **사용자 발화에 종속**시킨다(모델은 계속 대기 상태로 돌아온다).

### S6. `Asking multiple questions at once is bewildering.`
- **문자 그대로**: 한꺼번에 묻는 건 당혹스럽다.
- **요구 행동**: 없음 — **규칙이 아니라 근거(rationale)**다.
- **행동 변화**: S5의 준수율을 올린다. 이유를 아는 규칙은 압박 상황(할 말이 많을 때)에서 덜 깨진다.
- **역사적 근거**: `bc4cf903`에서 추가 — **`writing-great-skills` 스킬을 도입한 바로 그 커밋**. 저자가 스킬 작성 이론을 세우면서 grilling에 근거문을 주입했다. (DIRECT: 커밋 파일 목록)
- **없을 때**: S5는 여전히 작동하나, 복잡한 분기에서 모델이 "관련 질문 3개"로 뭉치는 이탈이 생길 수 있다. (INFERENCE)
- **분류**: Supporting (§I).

### S7. `If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me.`
- **문자 그대로**: 사실은 환경을 뒤져서 찾아라. 나에게 묻지 마라.
- **요구 행동**: 질문 대상에서 **사실**을 배제. 도구 사용으로 대체.
- **행동 변화**: 질문 예산을 보존한다. "이 프로젝트 React 쓰나요?" 같은 질문이 사라진다 → 남는 질문은 전부 **판단이 필요한 것**.
- **없을 때**: 질문의 상당수가 조회 가능한 사실 확인에 낭비된다 → 사용자가 "이건 네가 보면 알잖아"라고 느낌 → 신뢰 하락.
- **`*fact*` 이탤릭**: 강조 마크업이 대비쌍(fact ↔ decision)을 시각적으로 고정한다.
- **주도권**: 사용자의 **입력 부담**을 줄이되 결정권은 건드리지 않는다.

### S8. `The *decisions*, though, are mine — put each one to me and wait for my answer.`
- **문자 그대로**: 다만 **결정은 내 것**이다. 하나씩 나에게 내놓고 내 답을 기다려라.
- **요구 행동**: HITL(human-in-the-loop) **불가침 선언**.
- **★ 이 문장의 존재 이유는 실제 버그다** (`e5932a7a`, DIRECT — 커밋 메시지 원문):
  > *"Students reported /wayfinder picking a grilling ticket and **grilling itself** instead of turning to the human… Root cause: a grilling line written for the live-human case ('explore the codebase instead') **reads as license to answer questions autonomously** once wayfinder runs it in a resolve-the-ticket frame."*
- **이것이 드러내는 원리**: 동일한 문장이 **호출 프레임에 따라 정반대로 읽힌다.** 사람이 앞에 있는 세션에서 "codebase를 탐색해서 해결하라"는 무해했지만, 에이전트가 티켓을 해소하는 프레임에서는 "질문도 스스로 답해도 된다"로 읽혔다. → **프롬프트 문장의 의미는 문맥 의존적이며, 재사용 프레임이 늘어나면 기존 문장이 오독된다.** (DIRECT 사례)
- **수정 방식도 명시적**: *"Fix with **affirmative framing** (no negative-space 'don't')"* — "스스로 답하지 마라"(금지)가 아니라 "결정은 내 것이다"(긍정 귀속)로 썼다. 저자 이론서의 **Negation** 실패 모드(*don't think of an elephant*)를 스스로 적용.
- **없을 때 (= 로컬 설치본)**: grilling이 다른 스킬/에이전트 프레임 안에서 실행되면 **자기 질문에 자기가 답하고 진행**할 수 있다. 로컬은 이 방어가 없다.
- **주도권 영향**: **Essential.** 이 문장이 "누가 결정하는가"를 못박는다.

### S9. `Do not act on it until I confirm we have reached a shared understanding.`
- **문자 그대로**: 내가 공유된 이해에 도달했다고 확인하기 전에는 그것을 **실행하지 마라**.
- **요구 행동**: 인터뷰 종료 ≠ 실행 시작. 그 사이에 **사용자 승인 게이트**를 둔다.
- **행동 변화**: S2의 완료 기준을 **명시적 정지 게이트**로 물리화한다. CHANGELOG 원문(DIRECT):
  > *"turning the skill's existing 'shared understanding' completion criterion into an **explicit stop-gate**."*
- **없을 때 (= 로컬 설치본)**: 모델이 "충분히 물은 것 같다"고 **스스로 판단**하고 곧장 구현/파일 작성으로 넘어갈 수 있다. 사용자는 인터뷰가 끝난 줄도 모르는 채 산출물을 받는다.
- **본문 유일한 금지문(negation)**: 저자는 이론서에서 부정형을 실패 모드로 규정하면서도, *"keep a prohibition only as a **hard guardrail** you can't phrase positively"*라는 예외를 둔다. 이 문장이 바로 그 예외 — **하드 가드레일**.
- **종료 영향**: 종료를 **모델 판단 → 사용자 이벤트**로 이전. grilling의 마지막 상태 전이를 사용자 손에 넘긴다.

### S0. frontmatter `description` (행동이 아닌 **호출** mechanism)
- HEAD: `Grill the user relentlessly about a plan, decision, or idea. Use when…`
- 본문에는 영향이 없다. **언제 이 스킬이 로드되는가**만 결정한다.
- `0e9a0727`이 `Interview` → `Grill`로 바꾼 이유(DIRECT, CHANGELOG): *"recruits the pretrained **`grill`** leading word … to sharpen invocation."* 사용자가 "grill me"라고 말하는 어휘와 description의 어휘를 일치시켜 자동 호출 신뢰도를 올린다.
- `disable-model-invocation`은 grilling에 **없다** → 모델도 자율 호출 가능. grill-me에는 **있다** → 사람만.

---

## E. Core Behavioral Mechanism — 사용자 제시 8요소 검증

| 요소 | 원문 근거 | 실재? |
|---|---|---|
| 역할 반전 | `Interview me relentlessly` | ✅ DIRECT |
| 인터뷰 주도권 | `Interview me` + `Ask the questions` | ✅ DIRECT (단, **진행** 주도권만. 결정 주도권은 사용자) |
| 수렴할 때까지 질문 | `until we reach a shared understanding` | ⚠️ DIRECT하지만 **정의 없음** — 수렴 지표·측정·상한 일절 부재 |
| decision tree 탐색 | `Walk down each branch of the decision tree, resolving dependencies…` | ✅ DIRECT (단, **개념적 규칙**. 자료구조 아님) |
| recommended answer / default | `For each question, provide your recommended answer.` | ✅ DIRECT |
| 한 번에 하나의 질문 | `Ask the questions one at a time, waiting for feedback…` | ✅ DIRECT (+근거문) |
| 사실과 결정의 분리 | `If a *fact* … The *decisions*, though, are mine` | ✅ DIRECT — **단 HEAD에만. 로컬 없음** |
| 사용자 확인 전 실행 금지 | `Do not act on it until I confirm…` | ✅ DIRECT — **단 HEAD에만. 로컬 없음** |

**결합 효과 (이것이 핵심)**

```
S1 relentlessly ─────────┐  조기 종료 억제 (하한)
S3 decision tree ────────┤  질문 내용·순서 생성기
S4 recommended answer ───┤  응답 비용 ↓ + 모델 가정 노출
S5 one-at-a-time+wait ───┤  ★ 턴 절단 → loop 생성기
S7 fact lookup ──────────┤  질문 예산 보존
S2 shared understanding ─┤  종료 술어 (양자)
S8 decisions are mine ───┤  HITL 불가침
S9 confirm before act ───┘  하드 정지 게이트
```
- S1 없이 S5 → 짧은 인터뷰. S5 없이 S1 → 질문 덤프 1회.
- S3 없이 S1+S5 → 무작위 질문의 무한 나열(수렴 없음).
- S8/S9 없이 나머지 전부 → 모델이 프레임에 따라 **스스로 답하고 스스로 실행**. (← 실제 발생한 버그)

---

## F. Why a Few Lines Work

> "프롬프트라서 된다"가 아니라, **무엇이 어디에 위임되었는가**를 분해한다.

### F-1. 저자 자신의 이론 (DIRECT — 추측 아님)
`skills/productivity/writing-great-skills/SKILL.md` 첫 줄:
> *"A skill exists to **wrangle determinism out of a stochastic system**. **Predictability** — the agent taking the same **process** every run, not producing the same output — is the root virtue."*

→ 스킬의 목표는 **출력의 결정성이 아니라 절차의 결정성**이다. grilling은 *무엇을 물을지*를 전혀 정하지 않는다. *어떻게 물을지*만 정한다.

### F-2. LLM 자체 능력에 위임된 것 (프롬프트가 **말하지 않는** 것)
- 질문 **내용 생성** — 이 도메인에서 무엇이 미결정인지 식별. (사전학습)
- **의존성 판단** — A 결정이 B보다 먼저인가. (사전학습된 추론)
- **추천 답 생성** — 각 질문의 합리적 기본값. (사전학습된 도메인 지식)
- **수렴 판단** — 더 물을 게 남았는가. (사전학습된 완결감)
- **branch 재계산** — 사용자 답변이 남은 질문 집합을 어떻게 바꾸는가. (in-context 추론)

이 다섯 가지가 grilling 작업량의 99%다. 그리고 **instruction에 단 한 글자도 없다.**

### F-3. 프롬프트가 고정하는 것 (5개 축뿐)
1. **역할** (질문자 ← 답변자)
2. **단위** (턴당 1문)
3. **순서** (의존성 위상)
4. **기본값** (추천 답 동반)
5. **정지** (사용자 확인)

내용은 전부 비워두고 **형식만 고정**한다. → 그래서 도메인 무관하게 작동한다. `170ad486`이 마지막 남은 도메인 어휘("codebase")까지 제거한 것은 이 성질을 명시화한 것이다.

### F-4. 대화 컨텍스트 = 암묵적 state (별도 저장이 불필요한 이유)
grilling이 유지해야 할 상태는 정확히 세 가지다:
- 이미 물은 질문 → **대화 이력에 그대로 있음**
- 확정된 결정 → **사용자 답변으로 이력에 있음**
- 남은 branch → **위 둘로부터 매 턴 재계산 가능**

세 가지 모두 **컨텍스트 윈도우가 이미 무료로 제공**한다. append-only 로그가 곧 상태다. → 외부 저장소를 만들 이유가 없다. docs가 *"stateless: it writes nothing"*이라고 자랑하는 것은 결핍이 아니라 **설계 귀결**이다.

한계도 여기서 나온다: 컨텍스트가 넘치면 상태가 소실된다. (그래서 저자는 "한 세션에 담기 너무 큰 일"에는 별도 스킬 `wayfinder`를 둔다. — DIRECT, docs/grill-me.md)

### F-5. decision tree — 자료구조인가 탐색 규칙인가
**개념적 탐색 규칙이다.** 근거:
- 트리를 **구축/기록/출력/저장**하라는 지시가 본문에 **전무**.
- docs가 명시: *"The **mental model** is a decision tree."*
- 저자 이론서의 **leading word** 정의에 정확히 부합: *"a compact concept already living in the model's pretraining that the agent **thinks with** while running the skill … anchors a whole region of behaviour in the fewest tokens, by **recruiting priors the model already holds**."*

→ "decision tree"는 두 단어로 **탐색 알고리즘 하나를 통째로 호출**하는 압축 포인터다. 모델은 이미 DFS·의존성 정렬·branch를 안다. 구현할 필요가 없다. **구현하지 않는 것이 요점이다.**

### F-6. convergence — 알고리즘인가 판단인가
**LLM 판단이다.** 그리고 그것이 **의도된 설계**다. `.out-of-scope/question-limits.md` (DIRECT):
> *"Grilling is intentionally open-ended… some plans need three questions, some need fifty. A fixed cap would either cut off useful exploration on hard problems or feel arbitrary on easy ones."*
> *"natural-language steering is **the intended control surface, not a numeric limit**."*

수치 상한 요청(이슈 #44)은 **거부되었다.** 저자의 대응(DIRECT, #44 코멘트):
> *"remember that **you** are the one in charge… It's a **conversation, not an exam**."*

→ 수렴은 **측정되지 않는다.** 사용자가 선언한다.

### F-7. ★ 반복 loop — 코드인가 대화인가 (핵심 답변)

**코드가 아니다. 그리고 "그냥 프롬프트라서"도 아니다. 구조적 이유가 있다.**

LLM의 기본 생성 규칙은 **"턴이 끝날 때까지 유용한 작업을 최대한 수행한다"**이다. 질문을 물어야 한다는 지시만 주면, 모델은 **한 턴 안에서 질문 10개를 다 뱉고 끝낸다.** loop는 생기지 않는다.

`waiting for feedback on each question before continuing`이 이 기본값을 깨뜨린다:

```
턴 N   : 질문 1개 → 더 이상 진행 불가(대기 지시) → 턴 강제 종료
사용자 : 답변 (새 user 메시지)
턴 N+1 : instruction은 여전히 컨텍스트에 살아있음
         + 방금 답변이 새 branch를 열었음
         + 종료 술어(shared understanding)는 아직 미충족
         → 유일하게 합당한 continuation = 다음 질문 1개
```

즉 **loop는 프로그램이 만드는 게 아니라, "1문/턴" 규칙이 작업을 턴 경계로 이산화(discretize)함으로써 대화 턴 그 자체가 loop의 iteration이 되는 것**이다. 하네스가 이미 제공하는 turn loop를 **재사용**한다. 새로 만들 것이 없다.

여기에 3중 지속 장치가 걸린다:
| 장치 | 역할 |
|---|---|
| `relentlessly` + `every aspect` | 모델이 **스스로 그만두려는 성향**을 억제 (loop 하한) |
| `until **we** reach…` | 종료 술어가 **양자적** → 모델 단독으로 충족 불가 |
| `Do not act until **I** confirm` | 실행 전이를 **사용자 이벤트**에 묶음 (하드 게이트) |

**세 장치 모두 "종료를 어렵게 만드는" 방향이다.** 반복은 이 3중 억제의 부산물이다. 개발자가 loop를 만든 게 아니라, **끝내는 길을 막아서 반복이 남게 한 것**이다.

이것이 "왜 몇 줄로 장시간 반복이 되는가"의 실제 답이다.

---

## G. Conversation Dynamics (원본 instruction만으로 재구성)

**가상 요청**: *"내 노트 앱에 오프라인 동기화를 붙이고 싶다. 계획 좀 grill 해줘."*
(HEAD 버전 기준. UAHF와 무관한 순수 예시.)

### 0. 호출
"grill"이라는 단어가 description의 leading word(`Grill the user relentlessly…`)와 매칭 → 스킬 로드. 본문 4문단이 컨텍스트에 들어감.

### 1. 왜 첫 질문이 나오는가
`Interview me` 가 출력 모드를 질문으로 뒤집었고, `Ask the questions one at a time` 이 개수를 1로 묶었다. 모델은 계획서를 쓸 수 없다 — `Do not act on it until I confirm` 이 막는다. **남은 유일한 합법 출력이 질문 1개다.**

첫 질문이 *무엇*인지는 S3가 결정한다: 의존성 최상위 노드. 오프라인 동기화에서 다른 모든 결정이 매달리는 루트는 **충돌 해결 모델**이다.

> **Q1.** 두 기기가 같은 노트를 오프라인에서 각각 수정했을 때 어떻게 화해시킬 겁니까?
> *추천: last-write-wins. 노트 앱이면 대개 충분하고, CRDT는 구현 비용이 큽니다.* ← S4

### 2. 답변 후 branch
사용자: *"아니, 동시 편집이 실제로 일어난다. LWW면 글이 날아간다."*
→ LWW 가지가 **가지치기**된다. CRDT 가지가 열린다. 그리고 CRDT는 **새로운 하위 결정들을 낳는다**(어떤 CRDT 타입? 텍스트 구조? 서버 역할?). 이것이 "answer reshapes which questions come next"의 실체다.

### 3. 왜 후속 질문이 나오는가
종료 술어(`shared understanding`)가 아직 미충족이고, 방금 답변이 **미해소 자식 노드를 열었다**. `relentlessly`가 "이 정도면 됐다"를 억제한다.

> **Q2.** 그럼 노트 본문을 어떤 CRDT로 모델링합니까?
> *추천: 텍스트는 Yjs의 Y.Text. 성숙했고 rich-text 바인딩이 있습니다.*

### 4. 사실은 묻지 않는다 (S7)
모델이 *"현재 저장소가 무엇인가"*를 물으려다 — S7이 개입한다. 이건 **사실**이다. → 파일시스템을 뒤져 `schema.prisma`를 읽고, 묻지 않는다.
반대로 *"충돌 시 사용자에게 알릴 것인가"*는 **결정**이다 → S8에 의해 반드시 사용자에게 간다.

### 5. 왜 하나씩인가
Q1의 답이 Q2의 **존재 여부 자체**를 결정했다. Q1·Q2를 동시에 물었다면 Q2는 LWW 세계의 질문이 되어 무의미했을 것이다. 배치 질문은 **트리를 평면화**해 의존 구조를 파괴한다. (S6: *bewildering*)

### 6. 수렴 판단
열린 branch가 없을 때 — 모든 결정이 답을 얻었고, 마지막 답변이 새 자식을 열지 않았을 때. 이것은 **모델의 판단**이며, 측정 가능한 지표가 아니다.

> 정리하면: Yjs Y.Text CRDT, 서버는 relay, 충돌 시 무통지 자동 병합, 로컬은 IndexedDB… 이 이해가 맞습니까?

### 7. 왜 실행하지 않는가 (S9)
요약은 실행이 아니다. `Do not act on it until I confirm we have reached a shared understanding` 이 **사용자의 확인 발화**를 기다리게 만든다. 사용자가 *"맞다, 진행해"*라고 말하기 전까지 코드는 한 줄도 쓰이지 않는다.
**로컬 구버전에는 이 문장이 없다** → 6단계에서 곧장 구현으로 넘어갈 수 있다.

---

## H. Version Evolution

### H-1. `fb3629d3` (2026-03-19) — recommended answer
- 추가: `For each question, provide your recommended answer.`
- 커밋 메시지: "Added recommendation to grill-me skill" — **이유 미기재.**
- 교정한 실패 (추정): 백지 질문의 응답 비용. 후일 docs에서 사후 명문화됨(*"reacting to a proposal, not staring at a blank prompt"*).
- 등급: 변경 사실 DIRECT / **변경 이유 WEAK INFERENCE** (커밋에 이유 없음)

### H-2. `a6bdfd9f` (2026-03-26) — one question at a time
- 추가: `Ask the questions one at a time.`
- 커밋 메시지: "Add instruction to ask questions one at a time" — **이유 미기재.**
- **이전 버전의 실패 가능성**: 이 문장 이전(`fb3629d3`)에는 턴 절단 규칙이 **전무**했다. 모델은 "every aspect"를 한 턴에 질문 목록으로 쏟아부을 수 있었다 — 그리고 그것이 LLM의 기본 행동이다. 즉 **origin~H-1 구간의 grill-me에는 loop가 없었을 가능성이 높다.**
- **한 문장이 dynamics를 바꾼 지점**: 이 문장이 grilling을 "질문 목록 생성기"에서 "대화형 인터뷰"로 바꿨다. 4개월 뒤 `bc4cf903`이 근거문을 덧붙여 보강한 것도 이 규칙의 중요도를 방증한다.
- 등급: 변경 사실 DIRECT / 실패 서사 **STRONG INFERENCE**

### H-3. `bc4cf903` (2026-06-17) — "bewildering" 근거문
- 추가: `Asking multiple questions at once is bewildering.`
- 같은 커밋이 `writing-great-skills` 스킬을 도입 → 저자가 스킬 이론을 정립하며 grilling에 **근거(rationale)**를 주입. (DIRECT: 파일 목록)
- **← 로컬 설치본은 정확히 여기서 멈춰 있다.**

### H-4. `0e9a0727` (2026-07-03) — confirmation gate + `Grill` leading word
- 추가: `Do not enact the plan until I confirm we have reached a shared understanding.`
- description: `Interview the user…` → `Grill the user…`
- **이유 DIRECT** (커밋 본문): *"Add a **hard stop** so the agent won't enact the plan until the user confirms shared understanding is reached. **Recruit the pretrained 'grill' leading word** in the description."*
- **CHANGELOG DIRECT**: *"turning the skill's existing 'shared understanding' completion criterion into an **explicit stop-gate**."*
- **이전 버전의 실패**: `shared understanding`은 종료 **술어**였을 뿐, 실행을 막는 **게이트**가 아니었다. 모델이 스스로 도달했다고 판단하면 곧장 실행 가능. 한 문장이 "완료 기준"을 "정지 게이트"로 승격시켰다.

### H-5. `e5932a7a` (2026-07-06) — facts vs decisions ★ 가장 중요한 진화
- 교체: `If a question can be answered by exploring the codebase, explore the codebase instead.`
  → `If a *fact* can be found… look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.`
- **이유 DIRECT** (커밋 본문 전문 인용):
  > *"Students reported /wayfinder picking a grilling ticket and **grilling itself** instead of turning to the human (confirmed by @_noshit / @maudova; Matt: 'that sounds like a bug'). **Root cause: a grilling line written for the live-human case ('explore the codebase instead') reads as license to answer questions autonomously once wayfinder runs it in a resolve-the-ticket frame.**"*
  > *"Fix with **affirmative framing** (no negative-space 'don't')"*
- **이 사건이 증명하는 것**:
  1. 프롬프트 문장의 의미는 **호출 프레임에 의존**한다. 사람이 앞에 있을 땐 무해했던 문장이, 에이전트가 자율 해소하는 프레임에서는 정반대로 읽혔다.
  2. 재사용 가능한 primitive로 추출(`221ffca9`)한 **바로 그 결정**이 이 버그를 낳았다. 하나의 프레임(사람 대면)을 전제로 쓰인 문장이 다른 프레임(티켓 해소)에 재사용됐기 때문.
  3. 수정을 **금지문이 아니라 귀속문**으로 썼다 — 저자 이론서의 Negation 실패 모드를 스스로 적용.
- **한 문장의 dynamics 변화**: HITL 여부 자체가 뒤집힌다. 이 문장이 없으면 grilling은 **자문자답 루프**로 붕괴할 수 있다.

### H-6. `170ad486` (2026-07-13) — 범용화
- `this plan`→`this`, `design tree`→`decision tree`, `enact the plan`→`act on it`, `codebase`→`environment (filesystem, tools, etc.)`
- **이유 DIRECT** (changeset): *"The technique is **unchanged**; it now reads as a stress-test of **any plan, decision, or idea**."*
- 기법은 그대로 두고 **도메인 결합만 제거**. §F-3의 "내용은 비우고 형식만 고정" 성질을 명시화한 커밋.

### H-7. 거부된 변경 — 질문 수 상한 (이슈 #44)
- 2026-04-19 `DoozyDoz`: *"Codex just asked me 200 questions — is there a possibility of setting a limit?"*
- 코멘트: *"I'm bogged down at 26… feels like I'm being tested"* / *"I kept thinking maybe this one's the last question, they all seemed important too"*
- 저자 응답 (DIRECT): *"remember that **you** are the one in charge… It's a **conversation, not an exam**."*
- 영구 정책화 (`.out-of-scope/question-limits.md`): 상한은 **out-of-scope**. 이유 — 상한은 두 실패 모드를 혼동시킨다. ① 계획이 진짜 덜 구체화돼서 많이 묻는 것(정상 동작) ② 중복·저가치 질문(프롬프트 품질 문제). 후자의 해법은 **카운터가 아니라 프롬프트**다.
- → **이것이 "grilling은 튜닝 노브가 없다"의 근거다.** 제어면은 자연어뿐.

---

## I. Essential / Important / Supporting

### Essential — 제거하면 grilling이 grilling이 아니게 됨

| 요소 | 근거 |
|---|---|
| `Interview me … about every aspect of this` | 역할 반전. 없으면 모델은 답을 생산한다. grilling의 존재 이유 자체 |
| `relentlessly` | 저자 이론서가 **직접 예시로 지목**: 약한 단어는 no-op, `relentless`가 그 해법. 제거 시 모델 기본값(2~3문 후 진행)으로 회귀 |
| `until we reach a shared understanding` | 유일한 종료 술어. 제거 시 정지 개념 소멸 |
| `Ask the questions one at a time, waiting for feedback … before continuing` | **loop generator.** 제거 시 1턴 질문 덤프 → 반복 자체가 발생하지 않음 (§F-7) |
| `The *decisions* … are mine — put each one to me and wait for my answer` | HITL 불가침. **부재 시 자기-grilling 실증됨**(`e5932a7a`). 증거 기반 Essential |

### Important — 없어도 loop는 돌지만 품질/사용성/안전성이 크게 떨어짐

| 요소 | 근거 |
|---|---|
| `Walk down each branch of the decision tree, resolving dependencies … one-by-one` | 질문의 **순서와 구조**. 없으면 무작위 질문 나열 → 수렴 없음. loop는 돌지만 도달하지 못함 |
| `For each question, provide your recommended answer` | 응답 비용·앵커 제공 + 모델 가정 노출. 없으면 취조가 되어 사용자가 중도 이탈(#44 *"feels like being tested"*) |
| `Do not act on it until I confirm…` | 하드 정지 게이트. **경계선 판정**: 없어도 인터뷰 행동 자체는 유지되므로 Essential이 아니다(로컬 구버전이 실제로 grilling으로 통용된다). 그러나 산출물 안전성·사용자 주도권의 최종 보증이므로 Important 최상단 |
| `If a *fact* can be found … look it up rather than asking me` | 질문 예산 보존. 없으면 조회 가능한 사실을 묻느라 신뢰 하락 |

### Supporting — 핵심은 아니나 특정 실패를 방지

| 요소 | 방지하는 실패 |
|---|---|
| `Asking multiple questions at once is bewildering.` | one-at-a-time 규칙의 압박 상황 이탈. 규칙이 아니라 **근거** |
| description의 `Grill` leading word | **호출** 실패(스킬이 안 뜸). 행동에는 영향 0 |
| `grill-me` wrapper + `disable-model-invocation: true` | 원치 않는 자동 호출 + 컨텍스트 부하. 행동 기여 **0** (본문은 1문장) |
| `agents/openai.yaml` | Codex UI 표시. 행동 기여 **0** |
| `(filesystem, tools, etc.)` 괄호 | 도메인 과결합. 범용화 보조 |
| `*fact*` / `*decisions*` 이탤릭 | 대비쌍 시각 고정 |

---

## J. What Grill Me Is NOT

| 오해 | 판정 | 이유 |
|---|---|---|
| 단순 질문 목록인가? | **No** | instruction에 **예시 질문이 0개**다. 질문은 전부 런타임에 모델이 생성한다 |
| 고정 Interview Script인가? | **No** | 순서가 고정돼 있지 않다. 순서는 **사용자 답변에 따라 재계산**된다(§G-2) |
| 질문을 많이 하는 Prompt인가? | **Partially** | 결과적으로 많이 묻지만, 그건 **양의 지시가 아니라 구조의 부산물**이다 — "많이 물어라"는 문장이 없다. `relentlessly`(하한) + `we`(양자 종료) + `confirm`(사용자 게이트)이 **끝내는 길을 막아서** 반복이 남은 것 |
| Confidence Scoring Engine인가? | **No** | `confidence`·`score`·`threshold`·임계값 어휘가 **전 파일에 단 한 번도 등장하지 않는다** (grilling/grill-me/grill-with-docs 전 버전 원문 전수 확인). 수렴은 측정되지 않고 **선언**된다 |
| State Machine인가? | **No** | 상태·전이·가드 정의가 전무. 유일한 상태 저장소는 **대화 컨텍스트**다. docs가 *"stateless: it writes nothing"*이라 명시 |
| 특정 도메인 방법론인가? | **No** | 오히려 반대 방향으로 진화했다 — `170ad486`이 마지막 남은 소프트웨어 어휘("codebase", "plan")까지 제거해 **any plan, decision, or idea**로 범용화 |
| 요구사항 수집 Checklist인가? | **No** | 수집 항목·카테고리·템플릿이 전무. 무엇을 물을지는 100% 모델에 위임 |
| Stateless인가? | **Yes** | docs DIRECT. 파일 쓰기 0, 워크스페이스 0 |
| 하나의 스킬인가? | **Partially** | `grilling`(본체, 모델 호출 가능) + `grill-me`·`grill-with-docs`(사람 전용 wrapper). **행동은 전부 grilling에 있다** |

---

## K. Evidence & Unresolved Questions

### DIRECT EVIDENCE
- 전 버전 SKILL.md 원문 (GitHub raw, 11개 커밋 시점)
- sha256 대조 (로컬 = `bc4cf903`, ≠ HEAD)
- 커밋 이력·커밋 본문 (GitHub API)
- `CHANGELOG.md` (confirmation gate·facts/decisions 사유 명문화)
- `.changeset/grilling-general-use.md`
- `.out-of-scope/question-limits.md` (질문 상한 거부 정책)
- `.agents/invocation.md` (model-invoked vs user-invoked 규약)
- `skills/productivity/writing-great-skills/SKILL.md` (저자의 스킬 이론 — leading word, no-op, negation)
- 이슈 #44 원문 + 저자 코멘트
- 로컬 디렉터리 재귀 열거 (SKILL.md 외 파일 0)
- **이 세션의 available-skills 목록** (grilling 있음 / grill-me 없음 → `disable-model-invocation` 런타임 확인)

### STRONG INFERENCE
- 2-hop 로딩 메커니즘 (grill-me 본문 → Skill(grilling) 호출) — invocation.md 규약 + Skill 도구 의미론으로부터. **실행 로그로 직접 관측하지는 않았다**
- one-at-a-time = loop generator (§F-7) — 텍스트 구조 + LLM 기본 생성 행동으로부터의 연역
- H-2의 실패 서사 (그 이전엔 loop가 없었을 것) — 커밋 메시지에 이유 없음

### WEAK INFERENCE
- `fb3629d3`(recommended answer)·`a6bdfd9f`(one at a time)의 **동기** — 커밋 메시지가 변경 사실만 기술. 이유는 문서화되지 않았다. docs의 사후 설명은 몇 달 뒤 작성된 것

### UNVERIFIED / 확인 불가
- **로컬 설치본이 어떻게 설치되었는가** — `npx skills add`인지 수동 복사인지. 설치 메타데이터·lock 파일이 로컬에 **존재하지 않는다**. `agents/openai.yaml`이 없는 점은 수동 복사를 시사하나 확정 불가
- 실제 세션 평균 질문 수·수렴 소요 턴 — 계측 데이터 없음
- 모델별(Claude vs Codex) 준수율 차이 — #44가 Codex 사례임은 확인되나 비교 데이터 없음
- PR #463/#464의 리뷰 논의 — 조회하지 않음(필요 시 가능)
- 프로젝트 로컬 `.claude/skills/` 스윕 — 미실시(사용자 홈 디렉터리만 스윕)

### 완전성 주장의 범위·한계
- "전 파일 원문 전수 확인"은 **grilling/grill-me/grill-with-docs의 모든 버전 + 관련 docs/정책 문서 9종**에 한한다. 저장소 전체(60+ 스킬)를 전수 읽지는 않았다.
- "confidence 어휘 부재" 주장의 범위: 위 대상 파일들. 저장소 전역 grep은 수행하지 않았다.

---
---

# PART II — 핵심 결론 심층 기술 해설

> 대상 결론: *"LLM이 대화를 끝내는 모든 경로를 막는 3중 억제 장치입니다. 질문 생성·순서·수렴 판단은 전부 모델의 사전학습 능력에 위임하고, 프롬프트는 역할·단위·순서·기본값·정지 5개 축만 고정합니다. 반복 loop는 코드가 아니라 '1문/턴'이 작업을 턴 경계로 이산화한 결과 하네스의 대화 턴 자체가 iteration이 된 것입니다."*
>
> 증거 표기: **[D]** 원본 파일·커밋·문서 직접 확인 / **[A]** 분석자 해석 / **[A?]** 근거 약한 해석

---

## 0. 선행 자기 정정 — "3중"의 구성이 부정확했습니다

PART I §F-7의 3중 억제는 이렇게 나열됐습니다:

| 원래 제시한 3층 | 담당 문장 |
|---|---|
| ① 조기 종료 억제 | `relentlessly` + `every aspect` |
| ② 양자적 종료 술어 | `until **we** reach a shared understanding` |
| ③ 하드 정지 게이트 | `Do not act on it until **I** confirm` |

그리고 `one at a time`은 **"3중 억제와 별개인 loop generator"**로 따로 놓았습니다.

**이 구분은 틀렸습니다.** `one at a time`이야말로 **가장 큰 종료 경로 하나(일괄 질문 후 1회 왕복 종료)를 차단하는 억제층**입니다. 그것을 억제 목록에서 빼고 별도 범주로 둔 것은, "억제(종료 방지)"와 "생성(반복 발생)"을 서로 다른 것으로 봤기 때문인데 — §6에서 보이듯 **둘은 같은 것**입니다. 반복은 억제의 부산물이고, 일괄 질문 금지는 억제 그 자체입니다.

또 ①과 ②는 **같은 층의 두 부품**입니다. `relentlessly`(성향 억제)와 `we`(술어의 양자성)는 모두 **"모델이 질문을 그만두는 것"**을 막습니다. 별도 층이 아니라 한 층의 두 장치입니다.

**정정된 3층:**

| 층 | 억제 대상 | 담당 문장 |
|---|---|---|
| **A. 조기 수렴 억제** | 모델이 **질문을 그만두는 것** | `relentlessly`, `every aspect`, `each branch`, `until **we** reach a shared understanding` |
| **B. 병렬화/일괄 억제** | 모델이 **질문을 한 턴에 몰아 끝내는 것** | `one at a time`, `waiting for feedback … before continuing`, `bewildering` |
| **C. 확인 없는 실행 억제** | 모델이 **질문 없이/승인 없이 행동으로 넘어가는 것** | `The decisions … are mine — put each one to me and wait`, `Do not act on it until I confirm` |

세 층은 **서로 다른 종류의 종료 경로**를 막습니다. A는 *"이제 됐다"*를, B는 *"한꺼번에 물어보고 끝내자"*를, C는 *"내가 답을 안다/이제 만들자"*를 막습니다.

---

## 1. "LLM이 대화를 끝내는 경로"란 정확히 무엇인가

### 1-1. 왜 LLM은 모호한 요청에서 끝내려 하는가

LLM에 "대화를 끝내려는 의지"가 있는 게 아닙니다. **[A]** 하지만 다음 셋이 결합해 구조적 조기 종료 압력을 만듭니다:

1. **생성 목표의 국소성** — 모델은 "이번 assistant 턴에서 유용한 응답 하나"를 만들도록 학습됐습니다. 다중 턴에 걸친 정보 획득의 장기 가치를 최적화하도록 학습된 게 아닙니다. **[A]**
2. **도움됨(helpfulness) 편향** — 요청에 산출물을 내놓는 것이 "도움"으로 강화됐습니다. 되묻기는 지연이므로 항상 비용이 있습니다. **[A]**
3. **가정 보간 능력** — 모델은 빈칸을 통계적으로 그럴듯하게 채울 수 있습니다. 채울 수 있으면 물을 이유가 사라집니다. **[A]**

즉 **모든 종료 경로는 "물을 필요를 없애는 방법"**입니다. Grilling의 문장들은 각각 그 "없애는 방법" 하나씩을 봉쇄합니다.

### 1-2. 종료 경로 8종과 봉쇄 문장 대응

| # | 종료 경로 | 구체적 발현 | 봉쇄 문장 | 층 |
|---|---|---|---|---|
| P1 | **조기 이해 판단** | "요청 파악했습니다. 계획은 다음과 같습니다…" | `Interview me relentlessly about **every aspect**` — 이해 여부를 모델이 판정할 여지를 주지 않고 범위를 *모든 측면*으로 못박음 | A |
| P2 | **질문 일괄 덤프** | "몇 가지 확인할게요: 1) … 2) … 3) …" → 답 받고 즉시 종합 | `Ask the questions **one at a time**, **waiting for feedback** on each question **before continuing**` | B |
| P3 | **모호함 자체 가정** | "인증은 일반적으로 JWT를 쓰므로 그렇게 가정하고…" | `The ***decisions***, though, **are mine** — put each one to me and **wait for my answer**` | C |
| P4 | **default 임의 선택** | 결정을 조용히 골라 계획에 녹여 넣음 | ★ `For each question, provide your **recommended answer**` — default를 **금지하지 않고, 질문에 붙여 표면화하고 승인을 요구**하는 형태로 전환 (§9) | C |
| P5 | **질문 대신 해결책 제안** | "이렇게 하시면 어떨까요?" (질문형 외피의 제안) | `**Interview** me` — 출력 모드 자체를 질문으로 전환 + P4의 배출구가 제안 욕구를 흡수 | A |
| P6 | **계획 직후 실행** | 요약을 쓰고 곧바로 파일 작성/코드 생성 | `**Do not act on it** until I confirm we have reached a shared understanding` | C |
| P7 | **일부 branch만 탐색** | 주 경로만 묻고 예외·분기 생략 | `Walk down **each branch** of the decision tree, resolving **dependencies** between decisions one-by-one` | A |
| P8 | **사실과 결정의 동시 간주** | 사용자의 의도 진술 하나를 "결정도 다 내려졌다"로 소비 | `If a ***fact*** … look it up rather than asking me. The ***decisions***, though, are mine` | C |

**[D]** 8개 경로 전부에 대응 문장이 있습니다. 우연이 아닙니다 — 커밋 이력이 보여주듯 **각 문장은 실제로 관측된 실패 하나씩에 대응해 사후 추가**되었습니다 (P2 ← `a6bdfd9f`, P6 ← `0e9a0727`, P3/P8 ← `e5932a7a` — 마지막은 커밋 본문에 버그 리포트가 인용되어 있습니다).

### 1-3. ★ 봉쇄의 잔여 공간

**[A]** P1~P8을 전부 막으면, 모델이 이번 턴에 취할 수 있는 **합법 행동 집합이 사실상 하나로 줄어듭니다**:

- 계획을 쓸 수 없다 (P6 차단)
- 가정으로 채울 수 없다 (P3 차단)
- 조용히 default를 고를 수 없다 (P4가 표면화 요구)
- 제안 모드로 갈 수 없다 (P5 차단)
- 질문 5개를 몰아 쓸 수 없다 (P2 차단)
- "충분하다"고 선언할 수 없다 (P1 차단, 술어가 `we`)
- 일부만 묻고 넘어갈 수 없다 (P7 차단)

**남는 것: 추천 답이 딸린 질문 1개, 그리고 턴 종료.**

이것이 grilling의 본질입니다. 프롬프트는 "질문하라"고 **명령해서** 질문을 만드는 게 아니라, **질문 외의 모든 출구를 닫아서** 질문만 남깁니다. **봉쇄의 여집합이 곧 행동입니다.**

---

## 2. "3중 억제 장치"의 정확한 정의

### A층 — 조기 수렴 억제 (질문을 **계속하게** 만드는 층)

**무엇을 억제하는가**: 모델이 자기 정보 상태를 "충분하다"고 판정하고 질문을 멈추는 것.

**담당 instruction [D]**
- `Interview me **relentlessly** about **every aspect** of this`
- `**until we reach** a shared understanding`
- `Walk down **each branch** of the decision tree, resolving dependencies between decisions one-by-one`

**세 문장의 분업 [A]**

| 부품 | 기능 | 기술적 성격 |
|---|---|---|
| `relentlessly` | **성향(disposition) 억제** — "이 정도면 됐다"는 만족 임계를 위로 밀어올림 | 스칼라 강도 조절 |
| `every aspect` / `each branch` | **범위(scope) 확장** — 질문 소재의 고갈을 막음 | 탐색 공간 확대 |
| `until **we** reach` | **종료 술어의 양자화** — 종료 조건을 모델 단독으로 충족 불가능하게 만듦 | 술어 주어를 1인칭 복수로 |

`we`가 결정적입니다. `until you understand`였다면 모델은 **자기 내부 상태만 검사해서** 종료를 선언할 수 있습니다. `we`는 종료 판정에 **사용자 측 상태**를 요구합니다. 모델은 사용자의 이해 상태를 관측할 수 없으므로 술어를 **일방적으로 확정할 수 없습니다**. **[A]** (다만 압력이지 강제는 아닙니다 — 모델은 여전히 "우리가 이해에 도달한 것 같습니다"라고 추정 선언할 수 있습니다. 이 구멍을 C층의 `confirm`이 메웁니다. **이것이 A층과 C층의 접합부입니다.**)

**`relentlessly`가 no-op이 아닌 이유 [D]** — 저자 이론서가 이 단어를 직접 사례로 씁니다:
> *"A weak leading word (**be thorough** when the agent is already thorough-ish) is a **no-op**; the fix is a **stronger word (relentless)**, not a different technique."*

즉 `relentlessly`는 **모델의 기본 성향보다 확실히 위에 있는 지점**을 지정하기 위해 의도적으로 고른 단어입니다. `carefully`·`thoroughly`였다면 기본 행동과 구별되지 않아 아무 효과도 없었을 것입니다.

**없으면 빠지는 행동 [A]**: 확인 질문 1~3개 후 즉시 산출물 생산 = **grilling이 아닌 평범한 clarifying-question 행동**. 이것이 LLM의 기본값입니다.

**다른 층과의 결합**: A층은 loop의 **하한**을 만들지만 **형태**는 만들지 못합니다. A만 있고 B가 없으면 → "every aspect에 대해 relentless하게" 질문 **12개를 한 턴에 쏟아붓고** 끝납니다. A는 질문의 *양*을 보장할 뿐 *분산*을 보장하지 않습니다. **[A]**

---

### B층 — 병렬화/일괄 억제 (질문을 **턴에 흩뿌리는** 층)

**무엇을 억제하는가**: 여러 질문을 한 assistant 턴에 묶어 출력하고, 답을 한꺼번에 받아 1회 왕복으로 종결하는 것.

**담당 instruction [D]**
- `Ask the questions **one at a time**,` ← 개수 제약
- `**waiting for feedback** on each question **before continuing**.` ← 동기화 제약
- `Asking multiple questions at once is **bewildering**.` ← 근거

**두 절이 서로 다른 mechanism [A]**
- `one at a time`만 있으면: 모델이 "질문 1개 → **스스로 답** → 질문 1개 → 스스로 답"을 **한 턴 안에서** 수행할 수 있습니다. 형식적으로는 "한 번에 하나"를 지켰습니다.
- `waiting for feedback before continuing`이 이 구멍을 막습니다. 피드백은 사용자만 줄 수 있고, 사용자 입력을 받으려면 **턴을 끝내는 수밖에 없습니다.** 즉 이 절은 모델에게 **턴 종료(EOT 생성)를 강제**합니다.

**이것이 B층의 진짜 기능: 턴 경계를 강제 삽입하는 것.**

**`bewildering`의 지위 [A]**: 규칙이 아니라 **근거(rationale)**입니다. 행동을 새로 요구하지 않습니다. 규칙에 이유를 붙이면 압박 상황(관련 질문이 3개 떠오를 때)에서 규칙 이탈이 줄어듭니다. **[D]** `writing-great-skills`(스킬 작성 이론)를 도입한 **바로 그 커밋**(`bc4cf903`)에서 추가됐습니다.

**없으면 빠지는 행동 [A]**: 질문 덤프. 그리고 **반복 자체가 발생하지 않습니다.** A층이 아무리 강해도 "relentless한 질문 15개 목록"이 나올 뿐입니다. **B층이 없으면 grilling에는 loop가 없습니다.**

**결합**: B는 A의 산출물을 **시간축에 펼치는** 층입니다. A가 총량을 만들고 B가 턴 단위로 절단합니다. 절단된 조각 사이에 **사용자 답변이 삽입될 자리**가 생기고, 그 자리가 있기 때문에 트리 재계산이 가능해집니다(§6, §8).

---

### C층 — 확인 없는 실행 억제 (결정권·실행권을 사용자에게 결박)

**두 부품**으로 되어 있고, 커밋 이력상 다른 시점에 다른 버그를 고치며 들어왔습니다. **[D]**

| 부품 | 억제 대상 | 원문 | 커밋 |
|---|---|---|---|
| C-1 | 모델이 **결정을 스스로 답하는 것** | `The ***decisions***, though, **are mine** — put each one to me and wait for my answer.` | `e5932a7a` (2026-07-06) |
| C-2 | 모델이 **승인 없이 실행으로 전이하는 것** | `**Do not act on it** until **I confirm** we have reached a shared understanding.` | `0e9a0727` (2026-07-03) |

**C-1이 막는 것 — 자문자답. [D]** 커밋 본문:
> *"Students reported /wayfinder picking a grilling ticket and **grilling itself** instead of turning to the human… Root cause: a grilling line written for the live-human case ('explore the codebase instead') **reads as license to answer questions autonomously** once wayfinder runs it in a resolve-the-ticket frame."*

**C-2가 막는 것 — 조기 실행 전이. [D]** CHANGELOG:
> *"turning the skill's existing 'shared understanding' completion criterion into an **explicit stop-gate**."*

**두 부품의 관계 [A]**: C-1은 **인터뷰 도중**의 이탈(질문을 스스로 소비)을, C-2는 **인터뷰 이후**의 이탈(승인 없이 행동)을 막습니다. 시간축의 서로 다른 지점입니다. C-1 없이 C-2만 있으면 → 모델이 자기 질문에 자기가 답해 "shared understanding"을 혼자 만들고 그 다음 사용자 확인을 요구합니다. **형식은 지켰으나 인터뷰는 없었습니다.**

**없으면 빠지는 행동** — **로컬 설치본이 정확히 이 상태입니다. 두 문장 모두 없습니다.**

**결합**: C층은 A층의 술어(`we`)를 **관측 가능한 이벤트로 물리화**합니다. A층은 "우리가 도달할 때까지"라고 했지만 **판정 주체를 지정하지 않았습니다** → 모델이 추정 선언 가능. C-2가 판정을 **사용자의 발화**라는 관측 가능한 사건에 결박합니다. **A층의 술어를 C층이 완성합니다.**

---

### 3층의 결합 구조 (의존 관계도)

```
A층 (조기 수렴 억제)
  │  질문의 총량과 지속을 보장
  │  ↳ 단독 실패: 질문 15개 한 턴 덤프
  ↓
B층 (일괄 억제)
  │  총량을 턴 단위로 절단 → 사용자 답변 삽입 지점 생성
  │  ↳ 단독 실패: 질문 1개 던지고 곧장 계획
  ↓
C층 (실행 억제)
     인터뷰 중 자문자답 차단(C-1) + 인터뷰 후 무승인 실행 차단(C-2)
     ↳ 단독 실패: 인터뷰 없이 "확인해 주세요" (형식만 남음)

A는 loop의 길이를,  B는 loop의 형태를,  C는 loop의 출구를 통제한다.
셋 중 하나만 빠져도 grilling은 다른 스킬이 된다.
```

---

## 3. "5개 축"과 "3중 억제"의 관계

### 3-1. 5축의 정의

#### 축 1 — 역할(Role)
| 항목 | 내용 |
|---|---|
| 원본 | `**Interview me** relentlessly about every aspect of this` **[D]** |
| 제한하는 기본 행동 | **출력 모드**. LLM은 요청→응답 생산이 기본. 이 축이 응답 생산을 질문 생산으로 뒤집음 |
| 맡기는 것 | 질문의 **내용, 깊이, 표현, 도메인 지식** — 전부 |
| dynamics 영향 | 대화의 **진행 주도권**이 모델로 이동. 사용자는 응답자가 됨. (단 **결정 주도권**은 이동하지 않음 — C층이 지킴) |
| 제거 시 failure | 모델이 계획서를 씀. grilling 자체가 없어짐 |

#### 축 2 — 단위(Unit)
| 항목 | 내용 |
|---|---|
| 원본 | `Ask the questions **one at a time**, **waiting for feedback** on each question **before continuing**.` **[D]** |
| 제한하는 기본 행동 | **턴당 작업량**. LLM은 한 턴에 최대한 많이 하려 함. 이 축이 턴당 산출물을 질문 1개로 고정 |
| 맡기는 것 | *어떤* 질문 1개를 고를지 |
| dynamics 영향 | **턴 경계 = 정보 장벽**을 만들고 그 뒤에 사용자 답변이 도착하게 함. loop의 물리적 원인 |
| 제거 시 failure | 질문 덤프 → 1회 왕복 종결. **반복 소멸** |

#### 축 3 — 순서(Order)
| 항목 | 내용 |
|---|---|
| 원본 | `Walk down **each branch** of the decision tree, **resolving dependencies between decisions one-by-one**.` **[D]** |
| 제한하는 기본 행동 | **질문 배열**. 기본 LLM은 질문을 체크리스트(평면 목록)로 냄. 이 축이 **의존성 위상 순서**를 요구 |
| 맡기는 것 | 무엇이 무엇에 의존하는지 — **의존 그래프 자체를 모델이 구성** |
| dynamics 영향 | 앞 답변이 뒤 질문 집합을 **재구성**하게 함(= adaptive의 근거). 수렴 가능성을 만듦 |
| 제거 시 failure | 무작위·평면 질문. loop는 돌지만 **수렴하지 않음** — 끝없이 곁가지를 묻는다 |

#### 축 4 — 기본값(Default)
| 항목 | 내용 |
|---|---|
| 원본 | `For each question, provide your **recommended answer**.` **[D]** |
| 제한하는 기본 행동 | ★ **가정의 은폐**. LLM은 어차피 default를 갖고 있음. 이 축은 default를 **금지하지 않고**, **질문에 부착해 외재화하고 승인을 요구**함 |
| 맡기는 것 | 추천의 내용과 근거 |
| dynamics 영향 | 사용자를 **생성자 → 검토자**로 전환 → 턴당 사용자 비용 급감 → **긴 loop를 실사용 가능하게 만듦** |
| 제거 시 failure | 사용자 피로 → 중도 이탈. loop가 길어질수록 붕괴 확률 증가 |

#### 축 5 — 정지(Stop)
| 항목 | 내용 |
|---|---|
| 원본 | `until **we** reach a shared understanding` + `**Do not act on it until I confirm** we have reached a shared understanding.` **[D]** |
| 제한하는 기본 행동 | **완료 선언권**. 기본 LLM은 스스로 완료를 선언. 이 축이 선언권을 사용자에게 이전 |
| 맡기는 것 | "수렴한 것 같다"는 **제안** — 모델이 요약을 내놓는 것까지는 허용 |
| dynamics 영향 | loop의 **출구를 사용자 발화에 결박**. 모델은 무한히 대기 상태로 되돌아옴 |
| 제거 시 failure | 모델이 자기 판단으로 인터뷰를 종료하고 실행. 사용자는 인터뷰가 끝난 줄도 모름 |

### 3-2. 5축 ↔ 3층 관계도 — **서로 다른 분류 체계입니다**

두 체계는 **같은 텍스트를 다른 좌표계로 자른 것**입니다. **[A]**

- **5축 = 무엇을 통제하는가 (통제의 *차원*)** — LLM 행동의 서로 다른 **자유도**를 가리킵니다. 기준: *어떤 종류의 결정을 프롬프트가 고정하는가.*
- **3층 = 어느 종료 경로를 막는가 (통제의 *효과 방향*)** — 전부 "끝내지 못하게 한다"는 **하나의 목적**을 다른 지점에서 수행합니다. 기준: *어떤 탈출구를 봉쇄하는가.*

**교차표** (● 주 기여 / ○ 부수 기여 / — 무관)

| | **A. 조기 수렴 억제** | **B. 일괄 억제** | **C. 실행 억제** |
|---|---|---|---|
| **역할(Role)** | ● 질문 모드로 전환해 "즉시 답" 경로 차단 | — | ○ 간접(제안 모드 차단) |
| **단위(Unit)** | — | ● **전담** | — |
| **순서(Order)** | ● 미탐색 branch를 남겨 "다 물었다" 판정을 어렵게 함 | ○ 간접(순서가 있어야 1개 선택이 의미를 가짐) | — |
| **기본값(Default)** | ○ 간접(질문 비용을 낮춰 loop 지속을 가능케 함) | — | ● default를 은폐 가정에서 **승인 요구**로 전환 |
| **정지(Stop)** | ● `we` 술어 | — | ● `confirm` 게이트 |

**읽는 법 [A]**
- **단위(Unit) 축은 B층과 1:1.** 유일하게 한 층에 전속됩니다 — 그래서 이 문장 하나를 빼면 loop가 통째로 사라집니다.
- **정지(Stop) 축은 A와 C에 걸쳐 있습니다.** `we`(술어)는 A, `confirm`(게이트)은 C. 이것이 "A층의 술어를 C층이 완성한다"의 좌표계상 위치입니다.
- **기본값(Default) 축은 겉보기와 달리 C층 소속입니다.** 흔한 오해는 "추천 답 = 사용자 편의"인데, 억제 관점에서는 **모델이 default를 조용히 소비하는 것을 막는 장치**입니다. 편의는 부수효과입니다.
- **역할(Role)과 순서(Order)는 A층의 두 다리.** 역할은 질문을 *시작*시키고, 순서는 질문이 *고갈되지 않게* 합니다.

**결론: 5축 중 일부가 3층을 구성하는 게 아니라, 5축과 3층은 같은 8~9개 문장을 두 방향에서 절단한 직교 분류입니다. 어느 쪽도 다른 쪽의 부분집합이 아닙니다.**

---

## 4. Prompt가 결정하는 것 vs LLM에게 위임하는 것

### 4-1. 항목별 분류

| # | 항목 | 분류 | 근거 |
|---|---|---|---|
| 1 | **질문 내용 생성** | **LLM 자율 판단 (100%)** | 원본에 질문 예시·템플릿·카테고리가 **0개** **[D]** |
| 2 | **다음 질문 선택** | **Prompt가 제약만 제공** + **LLM 자율** | 제약: `each branch` + `resolving dependencies … one-by-one` **[D]** |
| 3 | **질문 순서** | **Prompt가 제약만 제공**(위상 정렬 *요구*) + **LLM이 그래프 구성** | 프롬프트는 "의존성 순서로"만 말함. **의존 그래프 내용은 전부 LLM** |
| 4 | **답변 해석** | **LLM 자율 판단 (100%)** | 파싱 규칙·스키마 없음 **[D]** |
| 5 | **새 branch 발견** | **LLM 자율 판단 (100%)** | 발견 규칙 없음. 매 턴 이력 재조건화로 창발 (§6-4) |
| 6 | **branch 우선순위** | **Prompt가 제약만 제공**(`dependencies` = 위상 우선) + **LLM이 실제 순위 결정** | 우선순위 함수·가중치 없음 **[D]** |
| 7 | **추천 답 생성** | **Prompt가 *존재*를 강제, 내용은 LLM 자율** | `provide your recommended answer` — "제공하라"만 있고 어떻게 고를지 없음 **[D]** |
| 8 | **충분히 탐색했는지 판단** | **LLM 자율 판단** (+ Prompt가 임계를 위로 밀어올림) | `relentlessly`, `every aspect` = 임계 조정. **측정 지표 없음** **[D]** |
| 9 | **수렴 판단** | **LLM 자율 판단** — 단 **선언은 불가** | `until we reach…` — 판단은 모델이 하되 술어가 양자적 **[D]** |
| 10 | **종료 판단** | **사용자 결정** | `Do not act on it until **I confirm**` **[D]** |
| 11 | **실행 시작 판단** | **사용자 결정 (게이트) + Prompt가 전이를 차단** | 동일 문장 **[D]** |
| — | **반복(iteration) 실행** | **Harness/대화 턴 구조가 제공** | 코드 0. 하네스 turn loop 재사용 (§6) **[A]** |
| — | **상태 보존** | **Harness/대화 턴 구조가 제공** | 컨텍스트 = append-only 이력 (§7) **[A]** |

### 4-2. 이 분류가 말하는 것

**작업량 기준으로 grilling의 지적 노동은 거의 전부 1~8에 있습니다. 그리고 그 8개 항목은 모두 "LLM 자율" 또는 "제약만 제공"입니다.** **[A]**

Prompt가 **직접 결정**하는 항목은 **단 하나도 없습니다.** 표 전체에 "Prompt가 직접 결정" 칸이 비어 있습니다. Prompt는 오직 세 가지만 합니다: **① 금지**(P1~P8 봉쇄) **② 강제**(질문 1개는 반드시, 추천 답은 반드시) **③ 결박**(종료·실행을 사용자 이벤트에).

### 4-3. ★ 그래서 Grill Me는 무엇인가

> **Grill Me는 Interview Engine을 구현한 것이 아니라, LLM이 이미 가진 Interview 능력이 특정 방향으로만 발현되도록 행동 공간을 잘라낸 것입니다.** **[A — 이 분석의 중심 주장]**

형식적으로:
- Interview Engine을 만든다 = **함수를 정의하는 것**: `next_question(state) → question`. 질문 풀, 선택 알고리즘, 상태 표현, 종료 조건을 전부 작성해야 합니다.
- Grill Me는 그 함수를 정의하지 않습니다. 대신 **모델의 출력 분포에 제약(constraint)을 겁니다**: 출력은 질문이어야 하고, 1개여야 하고, 추천을 달아야 하고, 의존성 순서여야 하고, 실행이면 안 됩니다.
- 제약이 충분히 조이면 **제약을 만족하는 출력이 사실상 유일해집니다.** 그 유일한 출력이 "다음 최선의 질문"입니다.

**`next_question`은 구현되지 않았습니다. 제약 만족의 결과로 창발합니다.** 이것이 "5줄로 되는" 이유의 핵심입니다.

---

## 5. 왜 별도 질문 생성 알고리즘이 필요 없는가

### 5-1. "LLM이 똑똑해서"로 끝내지 않기 위한 논증 구조

"모델이 능력이 있다"는 **필요조건**이지 충분조건이 아닙니다. 능력이 있어도 **발현되지 않으면** 무의미합니다. 실제로 능력 있는 모델도 기본 상태에서는 질문을 2개쯤 하고 끝냅니다. 설명해야 할 것은 **능력의 존재**가 아니라 **능력의 반복적 발현**입니다. **[A]**

```
(1) 능력이 존재한다                    ← 사전학습 (프롬프트 무관)
(2) 능력이 발현될 자유도가 남아 있다   ← 프롬프트가 "무엇을 물을지"를 비워둠
(3) 능력 외의 출구가 닫혀 있다         ← 프롬프트가 P1~P8을 봉쇄
```

**(2)와 (3)이 프롬프트의 전부이고, 서로를 필요로 합니다:**
- (3) 없이 (2)만 → 자유도는 있지만 모델이 그 방향으로 안 감 (기본값으로 빠짐)
- (2) 없이 (3)만 → 출구는 막혔지만 할 수 있는 게 없음 (템플릿을 주면 템플릿만 반복)

### 5-2. 능력별 매핑 — 남긴 자유도와 제거한 자유도

| LLM 능력 | 프롬프트가 **남긴** 자유도 | 프롬프트가 **제거한** 자유도 | 결과 |
|---|---|---|---|
| **대화 context 이해** | 이력 해석 방식 전부 | (없음 — 건드리지 않음) | 매 턴 이력 전체를 새로 읽음 |
| **미해결 ambiguity 인식** | 무엇이 모호한지 판정 | *"모호하면 가정으로 채운다"* 제거 (C-1) | 인식한 모호함이 **질문으로 배출될 수밖에** 없음 |
| **이전 답변에서 implication 추론** | 추론 내용 전부 | *"답변을 최종 명세로 소비한다"* 제거 (`each branch`, `dependencies`) | 답변이 **새 미결정을 낳는** 것으로 취급됨 |
| **다음으로 중요한 질문 생성** | 중요도 판단 전부 | *"여러 개를 동시에 낸다"* 제거 (B층) | **단 하나를 골라야 함** → 우선순위 판단이 강제 발현 |
| **선택지·추천안 생성** | 추천 내용 전부 | *"추천을 계획에 몰래 넣는다"* 제거 (축 4) | 추천이 **질문에 부착되어 표면화** |
| **암묵적 상태 추적** | 상태 표현 전부 | *"상태를 외부에 쓴다"* — 요구하지 않음 | 컨텍스트가 상태로 그대로 쓰임 |

**읽는 법 [A]**: 프롬프트는 **능력을 지시하지 않습니다. 능력의 배출구를 하나만 남깁니다.** "모호함을 인식하라"는 문장은 원본에 없습니다. 대신 "가정하지 마라(결정은 내 것)"가 있습니다. 모델은 어차피 모호함을 인식합니다 — 프롬프트는 그 인식이 **가정 채우기로 소비되는 경로를 막아서** 질문으로 나오게 만듭니다.

### 5-3. 왜 질문 목록/스키마/스코어가 **오히려 해로운가** [A]

- **질문 목록**: 목록을 주면 모델은 목록을 소진하고 멈춥니다. 목록에 없는 질문은 안 나옵니다. **`every aspect`(무한 범위)가 유한 목록으로 축소**됩니다.
- **dimension schema**: 차원을 고정하면 도메인 결합이 생깁니다. 저자는 정반대로 갔습니다 — `170ad486`은 마지막 도메인 어휘("codebase")조차 제거했습니다 **[D]**.
- **confidence score**: 점수를 도입하면 **임계값이 필요**하고, 임계값은 종료 선언권을 **모델에게 되돌려줍니다**(`score > 0.9 → 종료`). **A층과 C층을 동시에 무력화합니다.** — 저자는 수치 상한 요청을 **영구 out-of-scope로 거부**했고 **[D]**, 이유로 *"natural-language steering is **the intended control surface, not a numeric limit**"*를 들었습니다.
- **state machine**: 상태를 고정하면 **branch 무효화 전파 코드**가 필요해집니다. 저장하지 않으면 공짜인 것을(§8) 굳이 만들어 유지보수해야 합니다.

**결론: 이 항목들은 "없어서 아쉬운 것"이 아니라 "없어야 작동하는 것"입니다.** **[A]**

---

## 6. ★ "1문/턴"이 loop를 만드는 원리

### 6-1. 전제 — assistant 턴 하나 = 생성 패스 하나

**[D — 아키텍처 사실]**
- 하나의 assistant 턴은 **하나의 autoregressive 생성 패스**입니다.
- 그 패스 동안 조건(context)은 **고정**되어 있습니다: 시스템 프롬프트 + 스킬 본문 + 그때까지의 대화 이력.
- 패스 도중 새 정보가 **들어올 수 없습니다.** 사용자는 그 턴이 끝나야만 말할 수 있습니다.
- 턴은 모델이 EOT(end-of-turn)를 생성할 때 끝나고, 하네스가 제어를 사용자에게 넘깁니다.

**이 하나의 사실이 A/B 구조 차이의 전부를 설명합니다.**

### 6-2. 구조 A (일괄 질문)

```
[assistant 턴 1: 생성 패스 1개]
  조건 C₀ = (instruction, 사용자 최초 요청)
  Q1 ~ P(q | C₀)
  Q2 ~ P(q | C₀, Q1)          ← ★ A1이 조건에 없다
  Q3 ~ P(q | C₀, Q1, Q2)      ← ★ A1, A2가 조건에 없다
  Q4, Q5 …
[user 턴: A1..A5 동시 도착]
[assistant 턴 2]
  조건 C₁ = (C₀, Q1..Q5, A1..A5)
  → 종합 및 종료
```

**결함 1 — Q2~Q5는 "답을 모르는 상태에서 만든 질문"입니다. [A]**

Q2의 생성 분포는 `P(Q2 | C₀, Q1)`입니다. `A1`이 조건에 없습니다 — **존재하지 않으므로 조건이 될 수 없습니다.** 그러므로 Q2는 Q1의 **모든 가능한 답에 대해 평균적으로 말이 되는 질문**일 수밖에 없습니다.

트리로 보면: Q1이 branch를 3개로 가른다면 Q2는 **세 branch 어디에 떨어져도 유효한 질문**이어야 합니다. 즉 **branch 교집합**의 질문만 남습니다. 교집합은 얕고 일반적입니다.

→ **일괄 질문은 필연적으로 얕은 질문으로 회귀합니다.** 깊은 질문은 앞 답에 의존하는데 앞 답이 없기 때문입니다. **모델의 게으름이 아니라 조건부 확률의 구조적 결과입니다.**

**결함 2 — 재평가 기회가 딱 한 번, 그것도 종료 신호와 함께 옵니다. [A]**

턴 2에서 모델은 A1..A5를 한꺼번에 봅니다. 새 branch가 5개 열렸을 수 있습니다. 하지만 담화 구조상 이 시점의 자연스러운 continuation은 **종합**입니다 — 모델이 턴 1에서 질문 집합을 **닫힌 목록으로 선언**했고 사용자가 그것을 완료했기 때문입니다. 새 질문 라운드를 여는 것은 담화 규범상 어색합니다("아까 다 물어본다더니?").

→ **일괄 질문은 자기 자신을 종료 신호로 만듭니다.** 이것이 P2가 강력한 종료 경로인 이유입니다.

**결함 3 — 사용자 측 붕괴. [A]** A1..A5를 한꺼번에 쓰려면 5개 결정을 동시에 홀딩해야 합니다. 게다가 A1이 Q3의 전제를 무너뜨려도 사용자는 알아채지 못한 채 Q3에 답합니다 → **모순된 답변 집합**이 만들어질 수 있습니다.

### 6-3. 구조 B (1문/턴)

```
[assistant 턴 n: 생성 패스]
  조건 Hₙ = (instruction, 요청, Q1,A1, Q2,A2, …, Q(n-1),A(n-1))
  Qₙ ~ P(q | Hₙ)              ← ★ 모든 이전 답변이 조건에 들어있다
  EOT 생성 (← "waiting for feedback before continuing"이 강제)
[harness]
  제어를 사용자에게 이양, 입력 대기
[user 턴]
  Aₙ 입력
[harness]
  Hₙ₊₁ = Hₙ + (Qₙ, Aₙ)        ← ★ append. 자동. 코드 불필요
  모델 재호출
[assistant 턴 n+1]
  Q(n+1) ~ P(q | Hₙ₊₁)        ← ★ 새 조건 하에서 전부 다시 계산
```

### 6-4. ★★ "재계산"의 정체 — 재계산이 아니라 **재조건화(re-conditioning)**

**[A — 이 절 전체가 분석자 해석]**

"사용자 답변이 들어오면 트리가 재계산된다"고 말하면 어떤 재평가 루틴이 도는 것처럼 들립니다. **그런 것은 없습니다.** 실제로 일어나는 일은:

> **턴 n+1의 생성은 턴 n의 생성과 완전히 별개의 forward pass이고, 그 pass의 조건 `Hₙ₊₁`은 `Hₙ`과 다릅니다. 다른 조건 → 다른 분포 → 다른 출력. 끝입니다.**

- 모델은 "이전에 무슨 트리를 그렸는지" **기억하지 않습니다.** 기억할 곳이 없습니다.
- 모델은 매 턴 **이력 전체를 처음부터 읽고, 남은 미결정을 처음부터 다시 판정합니다.**
- 이전 판정과 새 판정이 다르면, 그것이 곧 "트리가 바뀐 것"입니다.

**그래서 branch 재계산은 공짜입니다.** 캐시가 없으므로 무효화(invalidation)도 필요 없습니다. 저장하지 않기 때문에 stale이 될 수 없습니다. **명시적 트리를 유지했다면 반드시 필요했을 "무효화 전파 코드"가, 트리를 유지하지 않기 때문에 존재할 필요조차 없습니다.**

한 줄로: **상태를 materialize하지 않고 매 턴 derive하기 때문에, 상태는 항상 최신 이력과 정합적입니다.**

### 6-5. ★ 모델은 왜 턴을 끝내는가 — EOT의 발생

B 구조가 성립하려면 모델이 **질문 하나만 쓰고 멈춰야** 합니다. 두 힘이 겹칩니다. **[A]**

1. **명시적 지시**: `waiting for feedback on each question **before continuing**` — 계속하려면 피드백이 필요하고, 피드백은 이 턴 안에서 얻을 수 없습니다. 계속 쓰는 것은 지시 위반입니다.
2. **담화 규범(adjacency pair)**: 질문–답변은 인접쌍입니다. 질문을 던진 화자가 곧바로 말을 이어가는 것은 대화 규범상 부자연스럽습니다. 모델은 방대한 대화 데이터로 이 규범을 학습했습니다. **프롬프트는 이 사전학습된 규범을 활성화할 뿐입니다.**

**(2)가 (1)을 값싸게 만듭니다.** 프롬프트는 "턴을 끝내라"는 낯선 요구가 아니라 **이미 강력한 대화 규범과 정렬된 요구**를 합니다. 그래서 짧은 문장 하나로 안정적으로 작동합니다. 규범과 어긋나는 요구였다면(예: "질문 후에도 계속 생각을 출력하라") 훨씬 긴 지시가 필요했을 것입니다.

### 6-6. ★★ "하네스의 대화 턴 자체가 iteration"의 기술적 의미

**모든 while-loop는 네 부품으로 됩니다:**

| while-loop 부품 | grilling에서 누가 제공하는가 | 코드가 필요한가 |
|---|---|---|
| **조건 검사** `while (!done)` | **LLM** — 매 턴 "shared understanding에 도달했나?"를 암묵 판정 | ❌ (프롬프트의 술어가 검사를 유발) |
| **루프 본문** `body()` | **Prompt** — instruction이 매 호출마다 컨텍스트에 그대로 존재 → 매 iteration의 본문이 **동일** | ❌ (텍스트가 곧 본문) |
| **반복 구동** | **Harness** — turn loop가 이미 사용자 입력 → 모델 호출을 무한 반복 | ❌ (이미 존재) |
| **상태 갱신** `state = f(state, input)` | **Harness** — 대화 이력에 자동 append | ❌ (이미 존재) |

**네 부품이 모두 이미 존재합니다. 그래서 작성할 코드가 0입니다.**

```python
# 이 코드는 아무도 작성하지 않았다. 그러나 이것이 실행된다.
while not LLM_judges(history, "we have reached a shared understanding"):
    q = LLM_generate_next_question(history)   # 조건: 전체 이력
    emit(q)
    end_turn()                                # ← "waiting for feedback"이 강제
    a = harness.await_user_input()            # ← 하네스가 원래 하는 일
    history.append(q, a)                      # ← 하네스가 원래 하는 일

summary = LLM_propose_understanding(history)
emit(summary)
end_turn()
harness.await_user_input()                    # ← S9: confirm 대기
if user_confirmed:
    act()
```

**핵심 통찰**: grilling은 loop를 **만들지 않았습니다.** 하네스에 이미 존재하는 REPL(사용자 입력 → 모델 생성 → 출력 → 반복)을 **while-loop로 용도 변경**했습니다. 필요했던 것은 단 둘:
1. **루프 본문을 매 iteration 동일하게 유지** → instruction이 컨텍스트에 상주하므로 자동 충족
2. **루프가 조기 탈출하지 않게** → A/B/C 3층 억제

**턴 경계 = iteration 경계. 사용자 입력 = loop의 다음 입력. 대화 이력 = 누적 상태. EOT = `continue`. 사용자 확인 = `break`.**

### 6-7. 이 구조가 지불하는 대가 **[A]**

| 대가 | 내용 |
|---|---|
| **왕복 수 = 질문 수** | 질문 200개면 왕복 200회. 이슈 #44가 정확히 이것 **[D]** |
| **컨텍스트 선형 증가** | 매 iteration마다 (질문+답변) append. 긴 세션은 컨텍스트 한계에 부딪힘 |
| **재조건화 비용** | 매 턴 이력 전체를 다시 처리 (KV 캐시로 완화되지만 이력 길이에 비례) |
| **비결정성** | 같은 이력이어도 다음 질문이 달라질 수 있음. 재현 불가 |
| **사용자 대역폭이 병목** | loop 속도 = 사람의 응답 속도. 이것이 축 4(추천 답)가 필수인 이유 |

---

## 7. 암묵적 State vs 명시적 State

### 7-1. 상태는 정확히 어디에 있는가

**[A]** 흔히 "컨텍스트에 있다"고 뭉뚱그리는데, **원본과 파생물이 다릅니다.**

| 계층 | 정체 | 성질 | 지속성 |
|---|---|---|---|
| **① 대화 이력 텍스트** | 실제 주고받은 문자열 | **원본(source of truth).** append-only, 불변, 순서 보존 | 세션 내 지속 |
| **② 컨텍스트 윈도우** | ①을 토큰화해 모델에 넣은 것 | ①의 **부분집합**(잘릴 수 있음) | 매 호출 재구성 |
| **③ 모델 attention / 활성값** | ②를 forward pass한 내부 표현 | ②의 **함수**. 매 턴 재계산 | **턴 종료 시 소멸** |
| **④ task representation** | 모델이 ③ 위에 암묵 구성한 "지금 무엇이 미결정인가" | ③의 **부분**. 명시적으로 존재한다는 보장조차 없음 | **턴 종료 시 소멸** |

**결정적 사실: ③과 ④는 저장되지 않습니다. 턴마다 새로 만들어집니다. 유일하게 지속되는 상태는 ① 텍스트뿐입니다.**

### 7-2. 상태 종류별 위치

| 상태 종류 | 어디에 있는가 | 형태 |
|---|---|---|
| **현재까지의 사용자 답변** | ① 이력 텍스트 | **명시적. 원문 그대로 보존** |
| **이미 탐색한 branch** | ① 이력 텍스트 (= 이미 던진 질문들) | **명시적. "branch" 라벨은 없음** |
| **확정된 결정** | ① 이력 텍스트 (질문+답 쌍) | **명시적. 구조화되지 않음** |
| **아직 남은 ambiguity** | ★ **어디에도 없음** | **매 턴 ①로부터 재파생** |
| **branch 우선순위** | ★ **어디에도 없음** | **매 턴 재파생** |
| **수렴 정도** | ★ **어디에도 없음** | **관측 불가** |

**★ 표시가 핵심입니다.** grilling이 실제로 필요로 하는 "작업 상태"(남은 것이 무엇인가)는 **저장되지 않습니다.** 매 턴 **이력으로부터 다시 유도**됩니다.

> **grilling의 상태는 materialized view가 아니라 매 턴 재계산되는 derived view입니다.** ①(append-only 로그)만 있고, 그 위의 모든 파생 상태는 휘발성입니다.

### 7-3. 명시적 state 구조들과의 비교

| 명시적 구조 | grilling에 있는가 | 차이 |
|---|---|---|
| **state machine** | ❌ **[D]** 상태·전이 정의 문자열 자체가 부재 | state machine: 상태 공간 **유한**, 전이 **정의됨**, 현재 상태 **검사 가능**. grilling: 상태 공간 = 자연어(**무한**), 전이 = LLM(**정의 불가**), 현재 상태 = **검사 불가** |
| **confidence vector** | ❌ **[D]** `confidence`/`score`/`threshold` 어휘 전무 | 수치가 없으므로 **진척률을 측정할 수 없음** |
| **event log** | ⚠️ **사실상 있음** — 대화 이력이 append-only·순서 보존·불변 | 그러나 **스키마가 없음**. 기계가 질의할 수 없고 LLM/사람이 읽어야만 해석됨 |
| **persistent memory** | ❌ **[D]** docs: *"stateless: it writes nothing and leaves no workspace behind"* | **세션 경계 = 상태 소멸** |

**⚠️ 행이 흥미롭습니다 [A]**: 대화 이력은 **구조 없는 event log**입니다. event sourcing의 핵심 성질(append-only, 불변, 순서 보존)을 다 갖췄지만 **타입도 스키마도 없어서** 해석할 수 있는 것은 LLM뿐입니다. **grilling은 LLM을 이 로그의 유일한 projection 엔진으로 씁니다.**

### 7-4. 장점 **[A]**

1. **구현 비용 0** — 상태 코드가 없으므로 상태 버그도 없습니다.
2. **표현력 무한** — 어떤 결정이든 자연어로 기록됩니다. 스키마 진화 문제도 없습니다.
3. **자동 정합성** — 파생 상태를 저장하지 않으므로 **stale 상태가 원리적으로 불가능**합니다. 무효화 전파가 필요 없습니다.
4. **Late binding** — 턴 30의 재파생은 턴 1~29의 **모든** 정보를 반영합니다. 턴 5에서 잘못 구조화한 트리에 갇히지 않습니다.
5. **되돌리기가 공짜** — 사용자가 턴 20에서 턴 3의 결정을 뒤집으면 턴 21의 재파생이 자동 반영합니다.

### 7-5. 한계 **[A]**

1. **컨텍스트 한계 = 상태 한계.** 이력이 윈도우를 넘으면 **상태가 조용히 소실**됩니다. 신호가 없습니다.
2. **중간 손실(lost in the middle).** 잘리지 않아도 긴 이력의 중간부는 어텐션이 약해집니다.
3. **조용한 번복.** 모델이 턴 30에서 턴 5의 결정을 **잘못 재해석**해도 검출 장치가 없습니다. 명시적 state machine이라면 불가능한 종류의 오류입니다.
4. **관측 불가.** "지금 몇 개 branch가 남았나?"에 답할 수 없습니다. → **이슈 #44의 심리적 고통의 원인**: 사용자가 *"maybe this one's the last question"*이라고 200번 생각했습니다 **[D]**.
5. **감사 불가.** 어떤 결정이 왜 그렇게 됐는지 추적하려면 전체 이력을 사람이 읽어야 합니다.
6. **이관 불가.** 세션이 끝나면 증발합니다. docs가 *"stateless"*를 장점으로 내세우지만 **[D]** 양날입니다 — 그래서 저자는 세션을 넘는 규모를 **별도 스킬(`wayfinder`)로 분리**했습니다 **[D]**. **저자 자신이 이 한계를 인지하고, grilling을 확장하는 대신 범위 밖으로 밀어냈습니다.**

---

## 8. Decision Tree의 실체

### 8-1. 판정

| 후보 | 판정 | 근거 |
|---|---|---|
| 실제 자료구조인가 | **❌ No** | 트리를 **구축/기록/출력/저장**하라는 지시가 원본에 **전무** **[D]** |
| 사전 정의된 질문 트리인가 | **❌ No** | 질문이 **0개** 정의되어 있음 **[D]** |
| 런타임에 저장되는 tree인가 | **❌ No** | 저장할 곳이 없음 (파일 쓰기 0, docs: *"writes nothing"*) **[D]** |
| **LLM이 대화 중 암묵적으로 탐색하는 개념적 구조인가** | **✅ Yes** | docs 명시: *"The **mental model** is a decision tree"* **[D]** |

**추가 근거 [D]** — 저자 이론서의 **leading word** 정의에 정확히 부합:
> *"a compact concept **already living in the model's pretraining** that the agent **thinks with** while running the skill … anchors a whole region of behaviour in the fewest tokens, by **recruiting priors the model already holds**."*

`decision tree`는 **두 단어로 탐색 알고리즘 하나를 통째로 호출하는 압축 포인터**입니다. 모델은 이미 DFS, 의존성 위상 정렬, branch/leaf, 가지치기를 압니다. **구현하지 않는 것이 요점입니다.**

### 8-2. ★★ 저장하지 않기 때문에 동적일 수 있다

**[A]** 반직관적이고 가장 중요한 부분입니다.

사용자 답변 하나가 다음 넷을 동시에 할 수 있습니다: ① 기존 branch를 **닫고** ② 새 branch를 **열고** ③ 우선순위를 **바꾸고** ④ 이전 질문의 전제를 **무효화**.

**명시적 트리를 유지했다면** 넷은 각각 코드가 필요합니다:
```
prune(node)                    # 1. branch 닫기
expand(node, new_children)     # 2. branch 열기
reprioritize(frontier)         # 3. 우선순위 재계산
invalidate_descendants(node)   # 4. ★ 전제 무효화 전파 — 가장 어려움
```
특히 4번은 실무에서 가장 버그가 많습니다. 어떤 노드가 무효화되면 후손 전부를 찾아 무효화해야 하고, 이미 답을 받은 노드도 재질문 대상이 될 수 있습니다.

**grilling은 이 네 함수를 하나도 갖지 않습니다. 그런데도 넷이 다 일어납니다.**

> **트리를 저장하지 않고 매 턴 이력에서 새로 유도하기 때문에, "무효화"라는 개념 자체가 필요 없습니다. 낡은 트리가 존재하지 않으므로 무효화할 대상도 없습니다.**

| 현상 | 명시적 트리에서 | grilling에서 |
|---|---|---|
| branch 닫힘 | `prune()` 호출 필요 | 새 이력으로 재파생하면 **그 branch가 애초에 안 나옴** |
| branch 열림 | `expand()` 호출 필요 | 새 이력으로 재파생하면 **새 branch가 저절로 나옴** |
| 우선순위 변경 | `reprioritize()` 필요 | 재파생 시 우선순위가 **처음부터 다시 매겨짐** |
| 전제 무효화 | `invalidate_descendants()` — **어려움** | 사용자가 턴 20에서 턴 3을 뒤집으면 조건 `H₂₁`에 **뒤집은 발언이 포함**됨. 재파생이 자동 반영 |

**예시** (노트 앱 오프라인 동기화):
- 턴 1: 모델이 LWW 추천 → 사용자 거부, CRDT 요구
- 이 시점에 "LWW 하위 branch"(충돌 UI, 타임스탬프 동기화, clock skew)는 **닫혀야** 합니다.
- grilling은 아무것도 닫지 않습니다. 턴 2의 조건 `H₂`에는 *"CRDT를 쓴다"*는 사용자 발언이 들어 있고, 그 조건 하에서 **clock skew 질문은 애초에 생성 확률이 낮습니다.** **닫는 게 아니라 안 열립니다.**

**대가 [A]**: **보장이 없습니다.** 모델이 실제로 전파하는지 검증할 방법이 없습니다. 이력이 길어지면(§7-5의 2번) 턴 3의 번복을 턴 40에서 놓칠 수 있고, **그것을 검출할 장치가 원본에 없습니다.** 명시적 트리의 무효화 전파 코드는 버그가 많지만 **적어도 결정론적이고 검증 가능**합니다. **grilling은 그 확실성을 포기하고 구현 비용 0을 샀습니다.**

---

## 9. Recommended Answer / Default가 왜 중요한가

### 9-1. 표층 기능 — 사용자를 생성자에서 검토자로

**[A]** 인지 비용의 비대칭이 핵심입니다:
- **생성(generation)**: 백지에서 답을 만들기 — 비용 높음, 시간 김, 도메인 지식 요구
- **인식/평가(recognition)**: 제시된 안을 평가 — 비용 낮음, 빠름, 부분 지식으로도 가능

추천 답은 사용자의 작업을 **생성 → 평가**로 바꿉니다. `accept / reject / modify` 세 동작만 하면 됩니다. **[D]** docs: *"you are **reacting to a proposal**, not staring at a blank prompt."*

### 9-2. ★ 구조적 기능 1 — A층의 부작용을 상쇄하는 짝

**[A]**
```
loop의 총 사용자 비용 = N × c
  N = 질문 수      ← A층(relentlessly)이 이것을 키운다
  c = 질문당 사용자 비용
```

**A층은 N을 키우는 방향으로만 작동합니다.** c를 낮추지 않으면 `N × c`가 사용자의 인내를 초과하고, 사용자는 **loop를 강제 종료**합니다. 그러면 3층이 아무리 잘 작동해도 인터뷰는 미완으로 끝납니다.

**축 4(추천 답)는 c를 낮추는 유일한 장치입니다.**

> **`relentlessly`(N↑)와 `recommended answer`(c↓)는 서로를 필요로 하는 짝입니다. 하나만 있으면 grilling은 실사용 불가능합니다.**

- `relentlessly` 없이 `recommended` — 짧은 인터뷰. 추천 답의 가치가 없음.
- `recommended` 없이 `relentlessly` — **사용자 중도 이탈.** 이슈 #44 코멘트가 정확히 이 실패를 보여줍니다: *"I'm bogged down at 26, each one needing lots of consideration, **feels like I'm being tested**"* **[D]** — 추천 답이 **있는데도** 26개에서 무너졌습니다. 없었다면 5개에서 무너졌을 것입니다.

**커밋 이력이 이 짝 관계를 지지합니다 [D]**: `recommended answer`(`fb3629d3`, 3/19)가 `one at a time`(`a6bdfd9f`, 3/26)보다 **먼저** 들어왔습니다. 저자는 loop를 길게 만들기 전에 **먼저 턴당 비용을 낮췄습니다.** (순서의 **의도성**은 커밋에 이유가 없으므로 **[A?]**. 순서 자체는 사실.)

### 9-3. ★ 구조적 기능 2 — 모델 가정의 강제 외재화

**[A]** 억제 관점에서 가장 중요한 기능입니다.

LLM은 **어차피 default를 갖고 있습니다.** 모든 미결정에 사전확률이 있습니다. 문제는 그 default가 **어디로 가는가**입니다:

| 추천 답 요구가 **없을 때** | 추천 답 요구가 **있을 때** |
|---|---|
| default가 **계획 본문에 조용히 녹아듦** | default가 **질문에 부착되어 표면화됨** |
| 사용자는 그런 결정이 있었는지도 모름 | 사용자가 **명시적으로 승인/거부** |
| = 종료 경로 P4 (default 임의 선택) | = P4 봉쇄 |

**축 4는 default를 금지하지 않습니다. default를 *가시화*하고 *승인 대상*으로 만듭니다.** 이것이 §3-2 교차표에서 축 4를 C층에 배치한 이유입니다 — 편의 장치가 아니라 **은폐된 결정을 드러내는 억제 장치**입니다.

**부수 효과 [A]**: 모델의 **solution-mode 압력에 안전한 배출구**를 제공합니다. 모델은 "답을 주고 싶어" 합니다(§1-1의 편향 2). 축 4가 없으면 그 압력은 P5(질문 대신 제안)로 새어나갑니다. 축 4는 그 압력을 **질문에 부착된 추천**이라는 합법 형태로 흡수합니다. **억누르지 않고 방향을 돌립니다.**

### 9-4. 앵커링 / 편향 위험 **[A]**

**[D]** 원본에는 이 위험에 대한 방어 문장이 **하나도 없습니다.**

| 위험 | 메커니즘 |
|---|---|
| **동의 편향** | 사용자가 추천을 그대로 승인하면 결정은 형식상 사용자 것이지만 **실질은 모델 것**. C-1(`decisions are mine`)의 보증이 **형해화** |
| **평범성 회귀** | 추천은 모델의 사전확률 = **가장 흔한 선택**. 관습적 답으로 수렴하는 압력. 참신한 선택은 사용자가 **능동적으로 거부해야만** 나옴 |
| **프레이밍** | 추천을 제시하는 순간 질문이 "무엇을 할까?"에서 "이것을 할까?"로 좁아짐. **고려되지 않은 3번째 선택지가 대화에 등장하지 않음** |
| **전문성 비대칭** | 사용자가 도메인에 얕을수록 추천 수용률 상승 → **grilling이 가장 필요한 사용자에게 가장 덜 작동** |

**저자의 유일한 대응은 프롬프트가 아니라 사용자 교육입니다 [D]** — 이슈 #44 답변: *"remember that **you** are the one in charge… It's a **conversation, not an exam**."* 앵커링 방어는 **instruction 밖**, 사용자의 태도에 위임되어 있습니다.

---

## 10. Facts와 Decisions의 분리

### 10-1. 왜 분리해야 하는가 — 세 층위의 문제 **[A]**

| 층위 | 문제 | 심각도 |
|---|---|---|
| **표층** | 조회 가능한 사실을 사용자에게 묻는다 → *"그건 네가 보면 알잖아"* → 신뢰 하락 | 낮음 |
| **중층** | 질문 예산이 사실 확인에 소진 → 정작 결정은 못 물어봄 | 중간 |
| **★심층** | **결정까지 "탐색으로 답할 수 있는 것"으로 분류해 스스로 답해버린다** | **치명적** |

### 10-2. ★ 심층 문제의 정확한 원인 — 술어의 과포괄

**[D]** 옛 문장:
```
If a question can be answered by exploring the codebase, explore the codebase instead.
```

술어는 **`can be answered by exploring`**입니다. 문제는:

> **결정도 "답할 수 있습니다."** 모델은 코드베이스를 뒤져서 "이 프로젝트는 Redux를 쓰니까 상태 관리는 Redux로 하죠"라고 **결정에 답할 수 있습니다.** 술어가 참입니다.

즉 `answerable by exploring`은 **사실과 결정을 구분하지 않는 술어**입니다. 과포괄(over-inclusive)입니다. 사람이 앞에 앉아 있는 세션에서는 드러나지 않았습니다 — 모델이 어차피 사람에게 묻고 있었으니까요. **호출 프레임이 바뀌자 드러났습니다.**

**[D]** 커밋 `e5932a7a` 본문:
> *"Root cause: a grilling line **written for the live-human case** ('explore the codebase instead') **reads as license to answer questions autonomously** once wayfinder runs it in a resolve-the-ticket frame."*

**수정된 문장은 술어를 바꿉니다 [D]**:
```
If a *fact* can be found by exploring the environment, look it up rather than asking me.
The *decisions*, though, are mine — put each one to me and wait for my answer.
```
새 술어는 `answerable`이 아니라 **`is a fact`**입니다. **답할 수 있는가**가 아니라 **무엇인가**로 기준이 바뀌었습니다. 이것이 과포괄을 제거합니다.

**수정 방식이 긍정 귀속입니다 [D]**: *"Fix with **affirmative framing** (no negative-space 'don't')"* — "스스로 답하지 마라"(금지, 코끼리를 부름)가 아니라 **"결정은 내 것이다"**(소유권 선언)로 썼습니다.

### 10-3. 사용자 발화에서 fact와 decision을 어떻게 가르는가

**[A]** 일반 메커니즘:

> **사용자의 발화는 대개 *의도(intent)*를 담습니다. 의도는 그 자체로 관측된 사실이지만, 다수의 미결정을 *함축*합니다. 의도를 사실로 기록하고, 함축된 미결정을 branch로 여는 것 — 이것이 분리의 실체입니다.**

**사용자 발화**: *"장기적으로 자동 누적해서 보고 싶다."*

**Fact (관측됨. 되묻지 않는다.)**
```
F1. 사용자는 "장기 누적 관찰" 의도를 갖는다.          ← 발화 자체가 증거
F2. 따라서 일회성 스냅샷이 아니라 시계열이 필요하다.   ← F1의 논리적 귀결(사실)
```
**주의**: F2도 사실입니다 — 사용자의 결정이 아니라 **F1으로부터의 연역**입니다. 이런 것을 묻는 것은 질문 예산 낭비입니다. **[A]**

**환경에서 조회 가능한 Fact (묻지 않고 찾아본다)**
```
F3. 현재 저장소가 무엇인가?             ← 파일시스템 조회
F4. 이미 어떤 이벤트가 발생하고 있는가?  ← 코드 조회
F5. 기존 스키마에 timestamp가 있는가?    ← 조회
```
**[D]** `If a *fact* can be found by exploring the environment … look it up rather than asking me.`

**Decision (사용자만 답할 수 있다. 하나씩. 추천을 붙여서)**
```
D1. 언제 수집하는가?           (이벤트 시점 / 주기적 폴링 / 배치)
D2. 어떤 이벤트에서 기록하는가? (전부 / 상태 변화만 / 명시 표시된 것만)
D3. 보존 기간은?               (무기한 / N일 / 계층적 롤업)
D4. 집계 단위는?               (원시 이벤트 / 분 / 시간 / 일)
```

### 10-4. ★ 이 예시가 드러내는 세 가지 구조 **[A]**

**(1) D1~D4는 서로 의존합니다 — 그래서 축 3(순서)이 필요합니다.**
```
D3(보존 기간) ← D4(집계 단위)에 의존
   무기한 보존이면 → 원시 이벤트는 비용 폭발 → 롤업 필요 → D4가 강제됨
   30일 보존이면  → 원시 이벤트 유지 가능 → D4가 자유로워짐
```
**D3을 먼저 물어야 D4의 선택지 집합이 결정됩니다.** 이것이 `resolving dependencies between decisions one-by-one`의 실제 의미입니다 **[D]**. 넷을 동시에 물으면 이 의존이 붕괴합니다(§6-2 결함 1).

**(2) 분리가 없으면 4개 결정이 1문장에 삼켜집니다.**

분리 문장이 없을 때 모델의 전형적 응답 **[A]**:
> *"장기 누적을 원하시니, 상태 변경 이벤트마다 기록하고 90일 보존, 일 단위 집계로 하겠습니다."*

**D1~D4가 전부 결정되었고, 사용자는 그 중 하나도 결정하지 않았습니다.** P3(가정 채우기) + P4(default 임의 선택)의 결합 발현입니다. 그리고 모델은 이것을 **사용자의 발화에서 도출했다고 믿습니다** — 사실과 결정을 섞었기 때문입니다.

**(3) 경계는 재귀적입니다.**
```
턴 n:   D3 = 미결정 (decision)
턴 n+1: D3 = "90일" (fact — 이력에 기록됨)
        → 다시 묻지 않는다
        → D4의 조건이 된다
```
**이 승격을 기록하는 코드는 없습니다.** 대화 이력이 자동으로 합니다 — 사용자의 "90일" 답변 텍스트가 이력에 append되고 다음 턴의 조건에 들어가기 때문입니다(§6-3). **decision → fact 승격이 append-only 로그의 부산물로 공짜 처리됩니다.** **[A]**

---

## 11. Stop / Confirmation Gate

### 11-1. 5단계 분리

**[A]** 각 단계는 **서로 다른 주체의 서로 다른 종류의 지식**입니다:

| # | 단계 | 판정 주체 | 지식의 종류 | 모델이 알 수 있는가 |
|---|---|---|---|---|
| 1 | 모델이 "충분히 이해했다" 판단 | **모델** | 자기 정보 상태 | ✅ |
| 2 | 질문이 수렴했다고 판단 | **모델** | 열린 branch가 없음 | ✅ (불완전하게) |
| 3 | 사용자에게 최종 이해를 제시 | **모델** | 발화 행위 | ✅ |
| 4 | **사용자가 확인** | **사용자** | **사용자의 동의 상태** | ❌ **원리적으로 알 수 없음** |
| 5 | 실제 행동 시작 | 모델 | — | (4에 의존) |

**★ 4번이 유일하게 모델이 접근할 수 없는 지식입니다.** 모델은 자기가 이해했는지는 알지만, **사용자가 동의했는지는 사용자가 말하기 전까지 알 수 없습니다.**

### 11-2. Gate가 없으면 무엇이 합쳐지는가 **[A]**

```
[게이트 없음 — 로컬 설치본의 상태]
assistant 턴 k:
  (내부) "충분히 물어본 것 같다"        ← 1
  (내부) "새 branch가 안 열린다"        ← 2
  "정리하면 다음과 같습니다: …"          ← 3
  [파일 작성 / 코드 생성 시작]           ← 5   ★ 같은 턴 안에서
```

**4번이 통째로 증발합니다.** 그리고 이것은 사고가 아니라 **자연스러운 continuation**입니다 — 요약 다음에 구현으로 넘어가는 것은 대화 흐름상 매끄럽습니다. 막는 것이 없으면 모델은 그렇게 합니다.

**증발의 진짜 대가 [A]**: 사용자는 **인터뷰가 끝났다는 사실조차 통보받지 못합니다.** 요약과 실행이 한 턴에 들어있으므로, 사용자가 요약을 읽었을 때는 이미 산출물이 만들어진 뒤입니다. **개입 지점이 존재하지 않습니다.**

### 11-3. 왜 "질문 종료"와 "실행 시작"이 다른 결정인가 **[A]**

```
질문 종료  = "더 물을 것이 없다"        ← 모델의 정보 상태에 대한 명제
실행 시작  = "사용자가 동의했다"        ← 사용자의 의사 상태에 대한 명제
```

**전자가 참이어도 후자는 거짓일 수 있습니다.** 모델이 물을 것을 다 물었어도 사용자가 결과물에 동의하지 않을 수 있습니다 — 요약이 사용자의 이해와 다를 수 있고, 사용자가 도중에 마음을 바꿨을 수도 있습니다.

**둘을 하나로 합치면, 모델이 "알 수 없는 명제"(후자)를 "알 수 있는 명제"(전자)로 대체하게 됩니다.** 이것이 근본 오류입니다. 게이트는 이 대체를 금지합니다.

### 11-4. `we` 술어에서 `confirm` 게이트로 — 무엇이 승격되었나

**[D]** CHANGELOG: *"turning the skill's existing **'shared understanding' completion criterion** into an **explicit stop-gate**."*

**[A]**

| | 이전 (`until we reach…`만) | 이후 (+ `Do not act until I confirm`) |
|---|---|---|
| 술어의 형태 | `we가 도달했는가?` — 양자 술어 | 동일 |
| **판정 주체** | **명시되지 않음** → 모델이 **추정 판정** 가능 | **사용자** (`I confirm`) |
| 판정의 관측 가능성 | 모델 내부 상태 — **관측 불가** | 사용자 발화 — **관측 가능한 이벤트** |
| 강제력 | 없음 (기준일 뿐) | **하드 정지** (`Do not act`) |

`we`는 **올바른 술어를 정의했지만 평가자를 지정하지 않았습니다.** 모델은 "우리가 도달한 것 같습니다"라고 **일방적으로 평가**할 수 있었습니다. `confirm`은 평가를 **사용자의 발화라는 외부 이벤트에 결박**합니다. — **술어는 그대로이고, 평가자만 바뀌었습니다.**

### 11-5. 게이트가 막는 것은 **행위**이지 **대화**가 아니다 **[A]**

원문은 `Do not **act** on it`입니다 — `Do not respond`도 `Do not summarize`도 아닙니다. 따라서:
- 모델은 요약을 **낼 수 있습니다** (3단계 허용)
- 모델은 "이게 맞습니까?"라고 **물을 수 있습니다**
- 사용자가 "아니, 하나 더"라고 하면 **loop로 되돌아갑니다**
- **막히는 것은 오직 "행동으로의 전이"뿐입니다**

**게이트는 종료 장치가 아니라 상태 전이 차단 장치입니다.** `interviewing → acting` 간선만 끊고 `interviewing → interviewing` 자기 루프는 그대로 둡니다. 이 때문에 게이트가 loop를 죽이지 않으면서도 실행을 막을 수 있습니다.

---

## 12. 전체 실행 흐름 — 행위자 표기

표기: **[P]** Prompt / **[L]** LLM / **[U]** User / **[H]** Conversation Harness

```
User Request
   │
   │  ← [H] 사용자 입력을 이력에 append
   │  ← [U] 요청 발화. "grill" 어휘가 스킬 트리거와 매칭
   ↓
Skill Load
   │
   │  ← [H] grill-me/SKILL.md 본문 주입 ("Run a /grilling session.")
   │  ← [L] Skill(grilling) 호출 결정
   │  ← [H] grilling/SKILL.md 본문 주입 → ★ 이 시점부터 instruction이 컨텍스트에 상주
   ↓
Role Constraint  ── [P] "Interview me relentlessly" → 출력 모드를 질문으로 고정
   │                [P] "Do not act on it" → 계획/실행 출구 봉쇄
   │                [P] "one at a time" → 출력 개수를 1로 고정
   │  ★ 남은 합법 출력 = 추천 답이 딸린 질문 1개  ([A] §1-3)
   ↓
One Question
   │
   │  ← [L] 질문 내용 생성 (100% 자율)
   │  ← [L] 의존성 최상위 노드 선택 ([P]가 "dependencies" 제약만 제공)
   │  ← [L] 추천 답 생성 ([P]가 존재만 강제)
   │  ← [P]+[L] EOT 생성 ("waiting for feedback" + 인접쌍 규범)
   ↓
   │  ← [H] 제어를 사용자에게 이양. 입력 대기.   ★ 여기가 iteration 경계
   ↓
User Answer
   │
   │  ← [U] 답변 (accept / reject / modify)
   │  ← [U] ★ 결정권 행사 — [P]의 "decisions are mine"가 보장
   ↓
Context Update
   │
   │  ← [H] 이력에 (Q, A) append.  ★ 코드 0. 하네스의 기본 동작
   │  ← ※ 파생 상태 저장 없음. 이력 텍스트만 늘어남 ([A] §7)
   ↓
Implicit Branch Re-evaluation
   │
   │  ← [L] ★ "재계산"이 아니라 재조건화(re-conditioning) ([A] §6-4)
   │         새 조건 Hₙ₊₁ 하에서 forward pass → 남은 미결정을 처음부터 다시 유도
   │  ← ※ 무효화 전파 코드 없음. 낡은 트리가 없으므로 무효화할 대상이 없음
   ↓
Next Best Question
   │
   │  ← [L] 우선순위 판단 (제약: [P]의 "dependencies … one-by-one")
   │  ← [P] 개수 제약이 "단 하나 선택"을 강제 → 우선순위 판단이 강제 발현
   ↓
   ⟲ ── [H] 턴 루프 반복.  ★ 이 순환이 while-loop의 실체 ([A] §6-6)
   │      [P] 루프 본문 = instruction (매 iteration 동일, 컨텍스트에 상주)
   │      [L] 루프 조건 검사 = "shared understanding에 도달했나?" (암묵)
   │      [P] 조기 탈출 봉쇄 = A/B/C 3층
   ↓
Model Judges Convergence
   │
   │  ← [L] 판정 (열린 branch 없음).  ★ 측정 아님. 지표 없음 ([D])
   │  ← [P] 술어가 양자적(`we`) → 모델이 단독 확정 불가
   ↓
Final Understanding / Recommendation
   │
   │  ← [L] 요약 제시 — ★ 이것은 [P]가 허용함 ("Do not **act**", not "do not respond")
   │  ← [H] 턴 종료, 사용자 대기
   ↓
User Confirmation
   │
   │  ← [U] ★ 유일하게 모델이 알 수 없는 지식 ([A] §11-1)
   │  ← [P] "Do not act on it until **I confirm**" — 전이가 이 이벤트에 결박됨
   │  ← ※ 사용자가 "아니, 하나 더"라고 하면 → ⟲ 로 복귀 (게이트는 대화를 막지 않음)
   ↓
Only Then Act
   │
   │  ← [L] 실행
```

**행위자별 담당 [A]**

| 행위자 | 담당 | 코드/텍스트 분량 |
|---|---|---|
| **[P] Prompt** | 봉쇄·강제·결박. **내용은 0** | **106단어** |
| **[L] LLM** | 질문 생성·순서·해석·branch·추천·수렴 판정 — **작업량의 거의 전부** | 0 (사전학습) |
| **[U] User** | 결정·종료·실행 승인 — **모든 권한** | — |
| **[H] Harness** | 반복 구동·상태 누적·턴 경계 — **loop와 state의 물리적 기반** | 0 (이미 존재) |

---

## 13. 핵심 결론

### 1. Grill Me는 왜 5줄 정도로도 작동하는가
**[A]** **프롬프트가 일을 하지 않기 때문입니다.** 질문을 만들지도, 순서를 정하지도, 상태를 관리하지도, 반복을 구동하지도 않습니다. 그 넷은 이미 존재합니다 — 앞의 셋은 LLM에, 마지막은 하네스에.

프롬프트가 하는 일은 **탈출구 봉쇄**뿐입니다. 8개 종료 경로를 막으면 남는 합법 행동이 "추천 답이 딸린 질문 1개 + 턴 종료"로 거의 유일해집니다. **행동을 지정한 게 아니라 여집합을 지정했습니다.** 여집합을 지정하는 데는 106단어면 충분합니다.

### 2. 실제 "지능"은 어디에 있는가
**[A]** **전부 LLM 안에 있습니다.** §4 분류표에서 "Prompt가 직접 결정"하는 항목은 **단 하나도 없습니다.** 질문 내용, 다음 질문 선택, 의존 그래프 구성, 답변 해석, 새 branch 발견, 우선순위, 추천 답, 탐색 충분성 — 여덟 항목 전부 LLM 자율이거나 "제약만 제공"입니다. 그리고 이 능력들은 **grilling이 만든 것이 아닙니다.** 사전학습에서 옵니다.

### 3. Prompt는 무엇을 **추가**하는가
**[A]** 세 가지, 오직 세 가지:

| 추가물 | 문장 |
|---|---|
| **역할 반전** (출력 모드 전환) | `Interview me` |
| **턴 절단** (턴당 1문 + 대기) | `one at a time, waiting for feedback before continuing` |
| **권한 귀속** (결정·실행을 사용자에게) | `The decisions are mine` + `Do not act until I confirm` |

`relentlessly`·`every aspect`·`each branch`는 **추가**가 아니라 **강도 조절**입니다. `recommended answer`는 **추가**가 아니라 **경로 변경**입니다(어차피 있는 default를 은폐에서 표면으로).

### 4. Prompt는 무엇을 **제거**하는가
**[A]** **자유도를 제거합니다. 능력이 아니라.**

| 제거된 자유도 | 남은 자유도 |
|---|---|
| 답을 즉시 생산할 자유 | 질문의 내용 |
| 가정으로 빈칸을 채울 자유 | 질문의 깊이·표현 |
| 여러 질문을 몰아 쓸 자유 | 어떤 질문 1개를 고를지 |
| default를 조용히 고를 자유 | 추천의 내용과 근거 |
| 완료를 스스로 선언할 자유 | 수렴했다고 *제안*할 자유 |
| 승인 없이 실행할 자유 | 요약을 제시할 자유 |

**왼쪽 열이 프롬프트의 전부입니다. 오른쪽 열은 건드리지 않습니다.** 이 비대칭이 설계 원리입니다.

### 5. Loop는 실제로 어디에 존재하는가
**[A]** **하네스의 turn loop에 존재합니다. grilling은 그것을 용도 변경했을 뿐입니다.**

| while-loop 부품 | 제공자 |
|---|---|
| 조건 검사 | **LLM** (매 턴 "shared understanding?" 암묵 판정) |
| 루프 본문 | **Prompt** (컨텍스트 상주 → 매 iteration 동일) |
| 반복 구동 | **Harness** (원래 있던 REPL) |
| 상태 갱신 | **Harness** (이력 append, 자동) |

**네 부품이 전부 이미 존재했으므로 작성할 코드가 0입니다.** `waiting for feedback before continuing`이 **EOT를 강제**해 턴을 절단하는 순간, **턴 경계가 iteration 경계가 됩니다.**

### 6. State는 실제로 어디에 존재하는가
**[A]** **오직 대화 이력 텍스트에만. 그리고 필요한 상태의 절반은 아예 저장되지 않습니다.**
- **저장됨**: 사용자 답변, 던진 질문, 확정된 결정 — 전부 **원문 텍스트로**, append-only, 불변
- **저장 안 됨**: 남은 ambiguity, branch 우선순위, 수렴 정도 — **매 턴 이력에서 재파생**

**materialized view가 아니라 derived view.** 이것이 무효화 전파를 불필요하게 만들고(§8-2), 동시에 관측·감사·이관을 불가능하게 만듭니다(§7-5).

### 7. 종료를 누가 판단하는가
**[A]** **두 단계, 주체가 다릅니다.**

| 판단 | 주체 | 성질 |
|---|---|---|
| **수렴했는가** | **LLM** | 자기 정보 상태 판단. 측정 지표 **없음** |
| **종료하는가** (실행으로 가는가) | **사용자** | `Do not act until **I confirm**` |

**모델은 종료를 *제안*할 수 있지만 *선언*할 수 없습니다.** **[D]** 수치 상한은 영구 out-of-scope — *"natural-language steering is the intended control surface, not a numeric limit."*

### 8. 사용자는 어디에서 최종 권한을 가지는가
**[A]** **세 지점, 오직 그 세 지점:**
1. **매 질문의 답변** — `The decisions are mine` (C-1)
2. **loop의 종료** — `until I confirm` (C-2)
3. **실행의 승인** — `Do not act on it` (C-2)

**그러나 이 권한은 형식적입니다 [A]** — §9-4의 앵커링이 실질을 갉아먹습니다. 추천을 계속 승인하면 결정은 형식상 사용자 것이지만 실질은 모델 것입니다. **원본에 방어 문장은 없습니다 [D]**. 저자의 유일한 대응은 프롬프트 밖의 사용자 교육입니다.

### 9. 왜 이 구조는 복잡한 Interview Engine 없이도 강력한가
**[A]**
1. **엔진이 이미 있습니다.** 다시 만들면 **더 나쁩니다** — 질문 목록은 유한하고, 스키마는 도메인에 결합하고, confidence 임계는 종료 선언권을 모델에게 되돌려줍니다(§5-3).
2. **loop와 state가 이미 있습니다.** 하네스의 turn loop와 대화 이력이 while-loop의 네 부품을 전부 제공합니다(§6-6).
3. **저장하지 않기 때문에 동적입니다.** 무효화 전파가 원리적으로 불필요합니다(§8-2). **구현하지 않은 기능이 구현한 기능보다 강합니다.**

**강력함의 출처는 "잘 만들었다"가 아니라 "만들지 않았다"입니다.** 프롬프트는 이미 존재하는 세 자산(LLM 능력, 하네스 루프, 컨텍스트)을 **연결만** 합니다. **106단어는 접착제이지 엔진이 아닙니다.**

### 10. 이 구조의 본질적 한계는 무엇인가
**[A]** 한계는 전부 **"만들지 않았다"의 이면**입니다.

| 만들지 않은 것 | 얻은 것 | 잃은 것 |
|---|---|---|
| **질문 생성 알고리즘** | 무한 도메인 적용, 적응성 | **보장 없음.** 중요한 질문이 안 나와도 알 방법이 없음 |
| **명시적 state** | 무효화 전파 불필요, late binding | **컨텍스트 한계 = 상태 한계.** 긴 세션에서 초기 결정이 조용히 소실·번복. 검출 불가 |
| **confidence / 진척 지표** | 임의 임계값의 자의성 회피 | ★ **사용자가 남은 양을 알 수 없음** — #44: *"I kept thinking maybe this one's the last question"* **[D]** |
| **질문 수 상한** | 어려운 문제에서 탐색이 잘리지 않음 | ★ **폭주 방어 없음.** 200개 질문이 정상 동작으로 취급됨. 제어면은 자연어뿐 |
| **앵커링 방어** | 프롬프트 단순성 | ★ **결정권의 형해화.** 도메인에 얕은 사용자일수록 심함 — **grilling이 가장 필요한 사용자에게 가장 덜 작동** |
| **세션 간 지속성** | stateless, 어디서나 실행 | **세션 종료 = 상태 증발.** 저자는 해결하지 않고 **범위 밖으로 밀어냈습니다** **[D]** |
| **결정론** | — | **재현 불가.** 같은 이력이어도 다음 질문이 달라질 수 있음. 감사 불가 |

**가장 근본적인 한계 [A]**: **grilling은 자기 자신을 관측할 수 없습니다.** 수렴했는지, 몇 개가 남았는지, 중요한 branch를 놓쳤는지, 사용자가 진짜 결정했는지 아니면 그냥 승인했는지 — **어느 것도 측정되지 않습니다.** 버그가 아니라 설계의 직접적 귀결입니다. 측정하려면 명시적 상태가 필요하고, 명시적 상태는 §8-2의 동적 재파생을 파괴합니다.

> **grilling은 관측 가능성(observability)을 팔아서 적응성(adaptivity)을 샀습니다.** 이 거래가 이 구조의 본질이며, 대가는 되돌릴 수 없습니다 — 상한을 넣거나 confidence를 넣는 순간 다른 스킬이 됩니다. **[D]** 저자가 수치 상한을 영구 out-of-scope로 못박은 것은 바로 이 거래를 지키기 위해서입니다.

---

## PART II 증거 규율 요약

- **[D] 직접 확인**: 원본 SKILL.md 전 버전, 커밋 본문(`e5932a7a`의 버그 리포트, `0e9a0727`의 stop-gate 의도), CHANGELOG, `.out-of-scope/question-limits.md`, 이슈 #44 원문과 저자 코멘트, `writing-great-skills`(저자의 leading word / no-op / negation 이론), docs의 *"mental model is a decision tree"* / *"stateless: it writes nothing"*.
- **[A] 분석자 해석**: §1-1 조기 종료 압력 3요인, §1-3 봉쇄의 여집합 논증, §3-2 교차표(5축 ↔ 3층 직교성), §6 전체(조건부 확률·재조건화·while-loop 부품 사상), §7 상태 계층 ①~④, §8-2 "저장하지 않기 때문에 동적", §9-2 relentless↔recommended 짝, §11 5단계 주체 분리, §13 전체.
- **[A?] 근거 약함**: `fb3629d3`(추천 답)가 `a6bdfd9f`(1문/턴)보다 **먼저** 들어온 순서의 **의도성**. 순서는 사실이지만 커밋에 이유가 없어 "비용을 먼저 낮추고 loop를 늘렸다"는 해석은 사후 재구성입니다.
- **검증 범위·한계**: 원본 근거는 grilling/grill-me/grill-with-docs 전 버전 + 관련 문서 9종에 한합니다. 모델 내부 동작(어텐션·분포)에 대한 서술은 아키텍처 일반론에 기반한 것이며, 이 스킬을 실제로 실행해 계측한 결과가 아닙니다.
