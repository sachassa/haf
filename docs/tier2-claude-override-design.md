# Tier 2 — `.claude` Global Default vs uahf override 재설계 (설계 정본)

작성일: 2026-07-09
작성: Worker (Advisor 확정 설계 저술 — 새 설계 결정 없음)
상태: **형태 A 확정 — override 계약(의미론) + 12항목 G/U 명찰 설계 확정 · 물리 재배치(형태 B)는 유보**
성격: 설계 문서 — 코드/구현 수정 없음. 이 트랙은 override의 **의미론과 귀속**을 확정하고, **무위험 정합만** 물리 반영한다.
목적: 이 문서만 읽으면 `.claude`의 Global Default(G) vs uahf override(U) 경계를 재분석 없이 이어갈 수 있게 한다. 후속 **형태 B(설치/스캐폴드)** 트랙과 루트 ARCHITECTURE 재저술의 선결 결정을 확보한다.

> **함께 읽을 문서 (근거 정본 · 읽기 전용):**
> - `docs/v1.2.1-repository-refactoring-brief.md@cd9247b` — 원칙 #3(`:29` — 최상위 `.claude`=Global Default, Layer 하위=Override) · `:142`(`.claude` override 모델 연결) · §C 상태 분리(`:166`–`:171`)
> - `docs/v1.2.1-context-and-design.md@cd9247b` — §7 미착수 관찰(`:130`) · §7.1 stale-allow 마이그레이션 노트(`:137`–`:149`) · Tier 2 트랙 목록(`:173`)
> - `uahf/framework/core/structure.md` §2(`:74` Adapter 경계 — 구체 환경 토큰 허용) · §4(형태 A/B 서술 라벨)
> - `uahf/framework/adapters/claude/entry-binding.md` §3(`:84`–`:93` — 두 진입 명령 확정 · `:87` `uaf-` 접두 DP-X1 · `:91` uahf-status 골격 준거)
>
> 이 문서 = **override 계약·귀속 설계** / 브리프 = 사용자 지시 정본 · 실행 기록 / context-and-design = v1.2.1 통합 이해. 상호보완.
>
> **아카이브 주(2026-07-17).** 위 두 근거 정본(`docs/v1.2.1-repository-refactoring-brief.md`·`docs/v1.2.1-context-and-design.md`)은 산출물 수명 정책(`docs/artifact-lifecycle-policy.md`)에 따라 커밋 `cd9247b`에서 작업 트리 아카이브되었다. 본문 곳곳의 축약 인용 `brief:NN`·`context-and-design:NN`(행 번호)은 이 앵커 커밋 기준으로 해석한다 — 열람: `git show cd9247b:docs/v1.2.1-repository-refactoring-brief.md` · `git show cd9247b:docs/v1.2.1-context-and-design.md`.

---

## 1. 한눈에 (요약)

- **문제.** 이 저장소는 UAF **도구를 개발하는 저장소**이면서 동시에 **UAF를 자신에게 적용하는 dogfooding 프로젝트**다. 그래서 루트 `.claude/`가 두 번들을 물리적으로 겸재한다 — **(G)** 도구가 배포하는 무상태·프로젝트 비의존 Global Default, **(U)** 이 UAHF 프로젝트를 특정하는 override. 브리프 원칙 #3(`brief:29`)의 골격은 물리적으로 실현됐으나(하위 `.claude/` 5개는 README 스텁, override 실물 0건), **무엇이 G이고 무엇이 U인가의 내용 경계**는 정본이 명시적으로 미착수로 남겨 둔(`context-and-design:130`·`:173`) 영역이다. 이 트랙이 그 경계를 확정한다.
- **핵심 원리.** **개념 귀속(어디에 속하는가) ≠ 물리 위치(지금 어디 두는가).** 개념 귀속은 지금 확정하고, 물리 이동은 형태 B가 존재할 때 실행한다.
- **결정적 제약.** Claude Code(환경)는 **루트 `.claude/`만** 네이티브 로드한다. 하위 `uahf/.claude/` 등 Layer override는 환경이 자동 소비하지 않는다 — UAF **논리** 구성물이지 환경 기능이 아니다. 따라서 override의 참된 발화는 **형태 B(합성·스캐폴드)** 를 요구한다(§3).
- **이 세션 범위.** override 계약(의미론)과 각 루트 `.claude/` 항목의 G/U 명찰을 설계 문서로 확정(형태 A)하고, **무위험 정합만** 물리 반영한다. 위험한 물리 재배치는 형태 B로 유보한다(사용자 결정, §6).
- **핵심 결정.** ① 세션 범위 = 설계 문서화 + 안전 정합 ② 귀속 = body 공통(GD) / 운영 파라미터(model·DP-E8) override (§6).

---

## 2. 개념 모델 (요소 ①)

### 2.1 Global Default (G) · override (U) 정의

- **Global Default (`루트/.claude/`)** = UAF 도구가 설치 시 배포하는 **무상태·프로젝트 비의존 기본값**. 공통 Agent 역할 body, 공통 진입 명령, 프로젝트 비의존 레퍼런스, 공통 규약을 담는다. 어떤 프로젝트에 설치되든 동일하게 배포되는 뼈대다(brief 원칙 #3=`brief:29`, `brief:142`).
- **override (`<layer>/.claude/`)** = Global Default의 **특정 요소를 좁은 문맥에서 재정의하는 델타(차이만)**. 전체 복제가 아니라 "무엇이 GD와 다른가"만 담는다. 하위 `.claude/`는 override만 둔다(brief 원칙 #3=`brief:29`, `uahf/.claude/README.md`).

이 두 개념의 관계는 합성으로 표현된다:

```
유효 .claude = GD ⊕ Layer override
```

`⊕`는 §4의 override 합성 3연산(ADD/REPLACE/MERGE)으로 실현된다.

### 2.2 dogfooding 이중역할 — 루트 `.claude/`의 붕괴

이 저장소는 "도구 개발 저장소 = 대상 프로젝트"인 dogfooding 상황이라, 일반 설치형에서 분리되는 두 층이 루트 하나로 **붕괴(collapse)** 한다:

| 개념 층 | 일반 설치형에서의 위치 | 이 저장소(dogfooding)에서 | 귀속 |
|---|---|---|---|
| 도구 배포 기본값 | 설치된 UAF의 Global Default `.claude/` | 루트 `.claude/`에 겸재 | **G** |
| 대상 프로젝트 override | 대상 프로젝트의 `.claude/` | 대상=UAF 자신 → 루트로 붕괴 | (Project override → 루트) |
| UAHF-특정 설정 | uahf Runtime Layer override | 개념상 `uahf/.claude/` override로 흡수 | **U** |

- **Project override의 붕괴.** 일반 설치형에서 대상 프로젝트 상태는 그 프로젝트 `.claude/`에 놓인다(brief §C=`brief:166`–`:171`). dogfooding에서는 대상 프로젝트가 UAF 자신이므로 Project override가 루트 `.claude/`로 붕괴한다.
- **UAHF-특정의 흡수.** 이 UAHF 하네스를 특정하는 요소(운영 파라미터 등)는 개념적으로 **uahf Runtime Layer override**에 귀속한다. 지금은 루트에 물리적으로 있으나(네이티브 로딩 제약, §3), 개념 귀속은 `uahf/.claude/`다.

### 2.3 개념 귀속 ≠ 물리 위치 (핵심 원리)

이 트랙의 중심 원리다.

- **개념 귀속** = "이 요소는 G인가 U인가" — 어디에 **속하는가**. 이 트랙이 지금 확정한다(§4 귀속표).
- **물리 위치** = "이 파일을 지금 디스크의 어디에 두는가" — 지금 어디에 **있는가**. 네이티브 로딩 제약(§3) 때문에 개념 귀속과 어긋날 수 있다(예: 개념상 U인 `model:opus`가 물리적으로 루트에 상주).
- 두 가지가 어긋나는 것은 결함이 아니라 **형태 A/B 분리의 정상 상태**다. 개념 귀속을 명찰로 확정해 두고, 물리 재배치는 형태 B가 존재할 때 수행한다.

### 2.4 형태 A / 형태 B 분리 (entry-binding 선례 동형)

`structure.md` §4의 형태 A/B 서술 라벨을 이 트랙에 동형 적용한다. entry-binding이 진입 명령을 형태 A(문서 규약)로 확정하고 실행 로더를 형태 B로 유보한 것(`entry-binding.md:93`, `uaf-new.md §0`)과 같은 구조다.

| 구분 | 이 트랙에서의 의미 | 이번 세션 |
|---|---|---|
| **형태 A** | override 계약(의미론) 문서 확정 + 각 항목 G/U 명찰 + 무위험 정합만 | **이 트랙 = 형태 A** |
| **형태 B** | 스캐폴드/설치기가 `유효 .claude = GD ⊕ Layer override`를 대상에 **물리 합성** | **후속 유보** |

- 형태 A(이 트랙)는 "무엇이 어디에 속하는가"를 확정하되 물리적으로 옮기지 않는다.
- 형태 B(후속 설치/스캐폴드 트랙)는 확정된 명찰을 근거로 GD와 Layer override를 실제로 합성해 대상 프로젝트에 설치한다. 형태 B는 §3의 네이티브 로딩 제약을 해소하는 유일한 경로다.

---

## 3. 네이티브 로딩 경계의 정직한 한계 (요소 ③)

이 절은 왜 이번 세션이 물리 재배치를 유보하는지의 **정직한 근거**다. override 명찰만으로는 실제 override 동작이 발화되지 않는다는 사실을 숨기지 않는다.

### 3.1 환경은 루트 `.claude/`만 네이티브 로드한다

- Claude Code(실행 환경)는 **루트 `.claude/`만** 네이티브로 로드한다. 하위 `uahf/.claude/`·`entry/.claude/` 등 Layer override는 환경이 자동 소비하지 않는다.
- 하위 `.claude/`의 override는 **UAF 논리 구성물**(브리프 원칙 #3이 정의한 계층 모델)이지, **환경 기능이 아니다**. 즉 `유효 .claude = GD ⊕ Layer override`의 `⊕` 합성을 지금 자동으로 수행하는 주체가 환경에는 없다.

### 3.2 귀결 — 참된 override 발화는 형태 B를 요구한다

- 따라서 override의 **참된 발화**(실제로 GD를 델타로 덮어 유효 설정을 만드는 것)는 **형태 B(합성·스캐폴드)** 를 요구한다. 스캐폴드/설치기가 GD와 Layer override를 읽어 대상에 유효 `.claude/`를 물리 합성해야 비로소 override가 동작한다.
- 지금 `uahf-status`나 `model` 바인딩을 물리적으로 하위 `uahf/.claude/`로 내리면, 합성 주체(형태 B)가 없으므로 **dogfooding 라이브 세션이 그 설정을 잃는다** — 루트에서 사라지고 하위는 로드되지 않기 때문이다.

### 3.3 파생 표면 결합 — uahf-status 이동은 정본 개정을 유발한다

- `uahf-status`는 정본에서 "골격 준거 선례"로 참조된다. 물리 이동은 이 참조 표면을 깨뜨려 정본 개정을 유발한다:
  - `entry-binding.md:91` — "두 명령은 `.claude/commands/uahf-status.md` 선례와 동형이다" (골격 준거).
  - `uaf-new.md:62` — 정본 포인터 표의 "진입 명령 골격 관례 = `.claude/commands/uahf-status.md`". (`uaf-continue.md`도 동형.)
- 따라서 uahf-status 물리 이동은 **UAF-INV ①(정본 무수정)** 대상인 `entry-binding.md`·진입 명령 정본의 개정과 결합한다. 이는 이번 세션 범위(정본 무수정) 밖이며 L-21 파생 표면 전수 스윕을 요구한다.

### 3.4 이번 세션의 유보 근거 (종합)

위 3.1–3.3에 근거해, 이번 세션은 **개념 귀속(명찰)만 확정**하고 override 항목의 **물리 축출을 유보**한다. 물리 재배치는 형태 B 트랙에서, 네이티브 합성 메커니즘이 존재할 때 수행한다.

---

## 4. override 계약 — 합성 3연산 (요소 ②) + 12항목 귀속 결정표 (요소 ④)

### 4.1 합성 3연산 (ADD / REPLACE / MERGE)

`⊕`(§2.1)는 파일 단위·필드 단위로 다음 3연산으로 실현된다.

| 연산 | 정의 | 단위 | 첫 사례 |
|---|---|---|---|
| **ADD** | GD에 대응짝(같은 상대경로)이 없는 **override-only 파일을 추가**한다. | 파일 | `uahf-status`(하네스 특정 Presentation 명령) |
| **REPLACE** | GD의 같은 상대경로 파일을 **통째로 교체**한다. body까지 다르다. | 파일 | (현행 인스턴스 없음 — 의미론만 정의, 형태 B 사용 대기) |
| **MERGE** | 파일은 유지하되 **선언된 필드만 override**하고 body는 GD에서 상속한다. | 필드 | `model` 바인딩(역할 body=GD, `model` 필드+DP-E8=U) |

첫 2사례(계획 채택):

- **ADD 첫 사례 = `uahf-status`.** GD에 대응짝이 없는 하네스 특정 명령(`uahf/docs/session-handoff` 전용, `uahf-status.md:16`·§3 정본 포인터표). 형태 B에서 uahf Runtime Layer override로 **ADD**된다. 물리 이동은 §3.3 근거로 유보.
- **MERGE 첫 사례 = `model`·`effort` 바인딩.** 4-agent 역할 body(role·boundary·message-format)는 GD로 배포되고, 그 위에 `model:opus`(`worker.md:4`·`planner.md:4`·`verifier.md:4`)+DP-E8 근거(`planner.md:17`·`verifier.md:13` — Fable 사용 한도 절약, v1.0 완료까지 유지)와 `effort` 바인딩(`worker.md:5`·`planner.md:5`=medium·`verifier.md:5`=high, Advisor 결정 2026-07-18 — 세션 xhigh 상속 제거로 지연·토큰 절감)만 **필드 MERGE**된다. `advisor.md`는 `model`·`effort` 라인이 없어(세션 상속, `advisor.md:18`) MERGE 델타가 없다 = GD 그대로(중립).

> REPLACE는 완전성을 위해 정의하되 현행 첫 인스턴스가 없다. 형태 B에서 "같은 상대경로 파일을 통째 교체"가 필요한 항목이 나타날 때 이 의미론을 적용한다. 임의 인스턴스를 지금 창설하지 않는다(새 설계 결정 금지).

### 4.2 12항목 귀속 결정표

루트 `.claude/` 12항목(파일 그룹 단위)의 개념 귀속과 분할선이다. **배정은 개념 귀속이며, 이번 세션의 물리 위치는 전부 루트 유지**(§3, §5)임에 유의한다.

| # | 항목 | 배정 | 분할선 / 근거 |
|---|---|---|---|
| 1 | `AGENT.md` | **분할** | body(Core Principles·Agent Lifecycle·Responsibilities·Delegation)=**GD** / 제목 "UAHF Agent Specification"(`:1`)·UAHF 특정 문구·stale `specs/` 참조(예 `:97` `specs/02 §9-OQ-2`)=**U**. **body 분할·`:97` 정합은 이번 세션 미편집** — L-14 CRLF hold, §5.3 참조. |
| 2 | `CLAUDE.md` | **분할** | Advisor persona(구현보다 설계·위임·검증·승인, `:13`–`:25`·§Advisor Rule)=**GD 템플릿** / "UAHF 프로젝트의 메인 Advisor"(`:3`) 등 프로젝트 특정=**U**. **환경 네이티브 로드 merge point**(§3.1 — 환경이 루트 `CLAUDE.md`를 프로젝트 지시로 로드). body 분할은 이번 세션 미편집(L-14 hold). |
| 3–6 | `agents/{advisor,worker,verifier,planner}.md` | **분할** | role·boundary·message-format body=**GD** / `model:opus`+DP-E8(Fable·v1.0) 및 `effort` 바인딩(worker·planner=medium·verifier=high, Advisor 결정 2026-07-18)=**uahf override(MERGE)**. `advisor.md`는 model·effort 라인 없음(`:18`)=중립=**GD 그대로**. **stale `specs/NN`→`uahf/specs/NN` 정합 필요**(§5.2 T2, 무위험). |
| 7–8 | `commands/{uaf-new,uaf-continue}.md` | **GD 유지** | 값 하드코딩 0, entry/specs·entry-binding 포인터 전용(`uaf-new.md:19`·§3 정본 포인터표). 보편 UAF 진입 명령. `uaf-` 접두=UAF 네임스페이스 표면화+빌트인 충돌 회피(DP-X1, `entry-binding.md:87`). |
| 9 | `commands/uahf-status.md` | **uahf override(개념)** | `uahf/docs/session-handoff` 전용=하네스 특정(`uahf-status.md:16`·§3). **file-unit ADD 첫 사례**(§4.1). **물리 이동은 형태 B 유보**(파생 표면·정본 개정 결합, §3.3). |
| 10 | `hooks/audit-complete/{manifest.md,audit.sh}` | **분할/분기** | 콘텐츠=프로젝트 비의존 레퍼런스 Hook Module(v0.8 시연 EX-DH) / **라이브 등록은 GD 상주 시 전 프로젝트 발화** → 배포 GD에서는 **미등록 예제 유지 권고**. 현재 라이브 표면 존치(DP-E7 정상 레퍼런스, `manifest.md:25`). 등록 상태 변경은 형태 B 사안. |
| 11 | `skills/commit-message-writer/SKILL.md` | **GD 유지** | 본문 "프로젝트 비의존"(INV-5) 자기 선언(`SKILL.md:19`). 프로젝트 특정 값은 Config/`io.input`으로 주입. 공통 재사용 Skill. |
| 12 | `settings.local.json` | **유지+정합** | 머신 로컬 override(`Bash(python -)` allow)=관례상 이미 override 성격, GD 아님. **`settings.json` 신설 불요**(hook은 `manifest.md` 자기완결 — 별도 등록 설정 불필요). |

**표 읽기 주의:** "배정"은 **개념 귀속**이다. 이번 세션에서 물리적으로 옮기는 항목은 없다(§3). "분할"은 한 파일 안에 G 부분과 U 부분이 공존함을 뜻하며, 실제 물리 분할(body 추출)은 형태 B 또는 후속 body-split 트랙 소관이다.

---

## 5. 재배치·정합 계획 (요소 ⑤)

이번 세션에 실제로 물리 반영하는 것은 **무위험 정합뿐**이다. 위험한 물리 재배치는 형태 B로 유보한다. 두 부류를 명확히 구분한다.

> 주: 이 문서(설계 문서, T1)는 정합의 **계획**을 확정한다. 실제 정합 편집(T2·T3)은 소유 경계가 비중첩인 **별도 Worker Task**로 수행되며, 이 문서는 기존 파일을 수정하지 않는다(신규 파일 1개 배타 소유).

### 5.1 이번 세션 무위험 정합 (실행 대상 — T2·T3)

| Task | 대상 (ownedBoundary) | 정합 내용 | 안전 근거 |
|---|---|---|---|
| **T2** | `.claude/agents/{advisor,worker,verifier,planner}.md` | stale `specs/NN` → `uahf/specs/NN` **전건**. 실측 지점: worker(`:11,:13,:123,:135`) · advisor(`:10,:104,:113`) · planner(`:15,:156,:184`) · verifier(`:11,:42,:168`). | 편집 가능 경계(정본 아님·append-only 아님). ⚠️ **L-14 CRLF hazard**: disk=CRLF, blob=LF → git 스냅샷 선행 + 편집 후 `git diff`로 의도 라인만 변경·CRLF 보존 확인(ffe71a6 체제 재사용). |
| **T3** | `uahf/.claude/README.md` | 명칭 정합 "runtime/uahf 워크스페이스" → "uahf Runtime Layer 워크스페이스"(`:3`). | 스텁 파일(정본·append-only 아님) → 안전. |

- **L-21 적용 지점.** T2 정합 후 **파생 참조 표면 전수 스윕**을 적용해 옛 경로(`specs/NN` 클릭형/텍스트형) 잔존 0을 실측 확증한다(L-21: "옛 경로/스텁 잔존 0"). 계획의 anchor 라인은 예시이며, 실제 편집 집합은 4파일 내 stale `specs/NN` **전건**이다(L-21 전수 스윕이 관장).

### 5.2 형태 B 유보 항목 (이번 세션 실행 안 함)

| 유보 항목 | 왜 유보 | 유발 결합 |
|---|---|---|
| `uahf-status` 물리 이동(→ `uahf/.claude/commands/`) + 파생 표면 스윕 | override 합성(형태 B) 선행 요구(§3.2). 지금 이동하면 라이브 세션이 명령을 잃음. | `entry-binding.md:91`·`uaf-new.md:62`(골격 준거 선례) **정본 개정 유발**(§3.3, UAF-INV ①). L-21 파생 표면 스윕 동반. |
| `model` 물리 field-merge 추출(`model:opus`+DP-E8을 body에서 분리) | MERGE 물리 실현은 GD body와 override 델타를 분리 저장·합성해야 성립(형태 B). 지금 분리하면 라이브 세션이 model 바인딩을 잃음. | 4-agent body 물리 분할과 결합(형태 B). |

### 5.3 body 분할 · stale specs(AGENT.md/CLAUDE.md) — 후속 결합 처리

- `AGENT.md`·`CLAUDE.md`의 **body 분할**(G 부분/U 부분 물리 분리)과 그 안의 **stale `specs/` 참조**(예 `AGENT.md:97`)는 **이번 세션 미편집**이다 — **L-14 hold**(disk=CRLF, blob=LF; 미검증 편집 금지, `context-and-design:135`). body 분할과 함께 후속 트랙에서 처리한다.
- 이유: 이 두 파일의 stale specs 정합은 body 분할과 분리해 단독 수행할 실익이 낮고(같은 파일을 두 번 CRLF 위험에 노출), body 분할 자체가 형태 B/후속 body-split 트랙 사안이기 때문이다. 이번 세션 무위험 정합(§5.1)은 agent 4종·`uahf/.claude/README`에 한정한다.

---

## 6. 사용자 확정 결정 2축 기록 (요소 ⑥)

사용자 확정 결정(선취 금지 게이트 통과). 결정 일자 **2026-07-09**. (`계획: zippy-launching-boole.md` "사용자 확정 결정", `context-and-design:173` Tier 2 목록.)

| 축 | 확정 | 내용 |
|---|---|---|
| **(1) 세션 범위** | 설계 문서화 + 안전 정합 | override 계약(의미론)과 G/U 명찰을 **설계 문서로 확정**(형태 A) + **무위험 정합만** 물리 반영(§5.1). 위험한 물리 재배치(uahf-status 이동·model 물리 추출)는 **형태 B 트랙으로 유보**(§5.2). |
| **(2) 귀속** | body 공통(GD) / 운영 파라미터 override | 4-agent 역할 body는 프레임워크 공통 **Global Default**로 배포. `model:opus`·**DP-E8**(Fable 사용 한도 절약, v1.0 완료까지 유지)의 운영 결정은 **uahf override**로 개념 귀속(MERGE). |

- 이 두 축을 넘어서는 결정(예: REPLACE 인스턴스 확정, uahf-status 이동 시점, body 물리 분할 방식)은 **이 트랙에서 확정하지 않는다** — §8 Open Questions로 남긴다(새 설계 결정 금지).

---

## 7. 위험 · 불변식 준수 체크 (요소 ⑦)

| 불변식 / 위험 | 준수 방식 (이 트랙) |
|---|---|
| **UAF-INV ①(정본 무수정)** | 정본(`uahf/specs/*`·`structure.md`·`uahf/framework/adapters/claude/*`(entry-binding 등)·루트 `ARCHITECTURE.md`)은 무수정. 이 설계 문서는 **신규 파일만**. uahf-status 이동을 유보해 `entry-binding`·진입 명령 정본 개정을 유발하지 않는다(유발 0, §3.3). |
| **append-only 데이터 무편집** | memory-data·discovery-data·loop-data 바이트 보존. stale `uaf/` 참조(`context-and-design:149`)는 stale 허용·존치 — 손대지 않는다. |
| **L-14 CRLF** | T2 편집(별도 Task) 전 git 스냅샷 + 편집 후 바이트 diff 검증(최소 diff·CRLF 보존). 미검증 편집 금지. AGENT.md/CLAUDE.md는 이번 세션 미편집(L-14 hold, §5.3). 본 설계 문서는 신규 파일이라 CRLF 위험 무관. |
| **L-21(이동 후 파생표면 전수 스윕)** | T2 정합 후 stale `specs/NN` 잔존 0 실측(§5.1). uahf-status 미이동이므로 그 파생 표면 스윕은 형태 B로 이연. |
| **네이티브 로딩 경계** | override 항목 물리 축출은 형태 B 전까지 **명찰·존치**(§3.4). 하위 `.claude/` 미로드 사실을 은폐하지 않고 형태 B 요구로 명문화. |
| **git 안전망** | 모든 물리 편집(T2·T3, 별도 Task) 전 스냅샷 커밋. 이동 완전 가역화(ffe71a6 체제). |
| **프리픽스 이원 혼동 금지** | `uaf-`(하이픈, 현행 물리 명령: `uaf-new`·`uaf-continue`·`uahf-status`) ↔ `uaf:`(콜론, 미래 `uaf:<layer>` 명령, `context-and-design:34`·`:144`) **혼동 금지**. `uahf-status`는 **하이픈 유지**. 이 트랙은 콜론 프리픽스를 도입하지 않는다. |
| **범위 침범 회피** | 루트 ARCHITECTURE 재저술·Layer 완전 저술은 별도 Tier 2 트랙 — 이 트랙 밖(`context-and-design:173`). |

---

## 8. Open Questions (임의 확정 금지)

계획·사용자 결정에 없어 이 트랙이 **확정하지 않는** 항목이다. 형태 B 또는 후속 트랙에서 사용자·Advisor가 확정한다.

1. **REPLACE 첫 인스턴스.** 어떤 항목이 "같은 상대경로 파일 통째 교체"(REPLACE)를 요구하는가. 현행 첫 사례가 없어 의미론만 정의(§4.1). 형태 B에서 판별.
2. **형태 B 합성 메커니즘.** 스캐폴드/설치기가 `GD ⊕ Layer override`를 물리 합성하는 실제 절차·도구(설치형 패키징 트랙, `context-and-design:157`). 이 트랙은 요구만 명문화하고 실현은 미확정.
3. **uahf-status 이동 시점·파생 표면 개정 방식.** 정본 개정(`entry-binding.md:91`·`uaf-new.md:62`)을 어떻게 동반할지(§3.3). 형태 B 착수 시 결정.
4. **AGENT.md/CLAUDE.md body 물리 분할 방식.** G body와 U 델타를 어떤 파일 구조로 분리·상속할지(§5.3). L-14 hold 해소와 함께 후속.
5. **hooks 배포 GD의 등록 상태.** 배포 GD에서 `audit-complete`를 미등록 예제로 둘지, 별도 등록 스위치를 둘지(§4.2 #10). "미등록 예제 유지"는 현재 **권고**이며 형태 B 확정 대상.

---

## 9. 다음 세션 시작 시

- 이 문서로 `.claude` G/U 경계와 override 계약(ADD/REPLACE/MERGE)은 **형태 A로 확정**되었다.
- 무위험 정합(§5.1 T2·T3)은 이 트랙의 별도 Worker Task로 수행된다(소유 경계 비중첩·L-14/L-21 준수).
- **형태 B(설치/스캐폴드) 트랙**이 §8 Open Questions를 해소하고 `GD ⊕ Layer override` 물리 합성을 실현할 때, 이 문서의 명찰·계약이 그 선결 입력이 된다.
- 루트 ARCHITECTURE 재저술 시 이 문서의 §2 개념 모델·§4 귀속표를 `.claude` 절의 근거로 인용한다.
