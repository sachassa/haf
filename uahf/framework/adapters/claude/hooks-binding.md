# framework/adapters/claude/hooks-binding — Claude Code Hooks Adapter 바인딩

작성일: 2026-07-06
상태: v0.9 Baseline (개정 — §7 시연 후 상태 반영 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06). 직전 기준선: v0.8 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/08-hooks.md §4.1 — Claude Code Binding 표(5행). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/08-hooks.md §4.2 — 이식 교체 지점 SP-1~SP-5. 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/08-hooks.md §3.1·§3.2·§3.3 — 이벤트 카탈로그·Hook 정의·능력·등록·Dispatch·순서·실패 처리 연산(§3.1-A~E)·Event Catalog 18행(§3.2-A)·명명 규칙(§3.2-B)·Event Record(§3.2-C)·Hook Binding 6필드(§3.2-D)·Hook Failure Report(§3.2-E)·Invariants INV-1~8(§3.3). 본 문서가 준수·대조하는 계약. 재정의하지 않고 § 포인터로만 인용한다.
- specs/08-hooks.md §9 결정 기록 — OQ-H1(비차단 observer 확정)·OQ-H2(방출 주체 §4 소관 확정)·OQ-H3(order 동률 tie-breaker 확정)·03/04 방출 경계 대응(모순 없음)·Glossary 추가 요청 5건 승인. 본 문서가 §4 소관으로 해소·반영하는 결정의 정본.
- specs/01-runtime.md §3.1-A(Register/Resolve/Replace/Deregister)·§3.2-A(Module Manifest 7필드)·§4.1(확장 Module 표면 `.claude/hooks/`). Hook 등록·Module 직렬화의 원천 계약. § 포인터로만 참조.
- framework/adapters/claude/loop-binding.md (v0.7 Baseline) — 자매 Adapter Binding 문서(관례 정본). **lifecycle 계측 지점 참조원**(§3 전이 이벤트 기록·loop-data/ 백엔드). §0 격리 지점 방향 반전(C-3 비적용)·§2 정본 인용 열+물리 실현 열+실재 여부 열 표 관례·형태 A/B 정직 구분·§6 SP 대응 표·§7 실측 대조·§9 이력 머리 배치의 선행 관례. 본 문서는 그 계측 지점을 참조만 하고 재정의하지 않는다.
- framework/adapters/claude/memory-binding.md (v0.4 Baseline) — 자매 Adapter Binding 문서. **memory 계측 지점 참조원**(§3.1 Record / §3.2 Recall 물리 절차·memory-data/ 백엔드). 관례 표본. 재정의 0.
- framework/adapters/claude/runtime-binding.md (v0.3 Baseline) — 자매 Adapter Binding 문서. **runtime 연산 실현 참조원**(§3.2 Register/Resolve 수행 방식·§3.3 Config·§3.4 Bootstrap/Shutdown). Register/Resolve 수행 방식·Config 스코프 물리 소스의 선행 관례. 재정의 0.
- framework/adapters/claude/verifier-binding.md (v0.5 Baseline) — 자매 Adapter Binding 문서. 관례 표본(형태 A/B 정직 구분·SP 대응 표·실측 대조·configSchema 부재 정직 기록의 선행 관례).
- docs/delegation-protocol.md §3 — 이 프로젝트의 물리 채널 바인딩 관행. **agent 계측 지점 참조원**(§3.1 위임 디스패치 = 서브에이전트 위임 / §3.2 보고 회수 = 최종 응답). 물리 채널 서술의 관행 근거.
- framework/core/structure.md §2·§5 — 4경계 배치(Adapter 경계 = 격리 지점, C-3 비적용)·C-3 금지 토큰 규칙(Adapter 경계는 격리 보유로 비적용). 본 문서 경계의 근거.
- specs/00-glossary.md §3.2-J J-08 — Event·Event Catalog·Phase·Hook Binding·Hook Dispatch 표제어(08 §9 요청으로 Advisor 승인 추가). 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- ROADMAP.md v0.8 (Extension System) — Hooks 완료 조건과 산출물(본체 수정 0 확장·비차단·순서 결정성·카탈로그 도출·경계·AI 비의존)의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 08 §3.3 INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·memory-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형). 단 이 문서는 Core Contract(08 §3)를 **재정의하지 않는다** — 계약(연산·카탈로그 Event ID·필드·Invariants)은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. `framework/adapters/claude/` 경계의 확장 시스템 첫 바인딩 산출물(선행 자매: runtime-binding.md·memory-binding.md·verifier-binding.md·loop-binding.md). 08 §4.1 바인딩 표 **5행 전건**을 물리 실현("정본 인용" 열 + "물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑(§2). 이벤트 카탈로그 **18행 전건**의 계측 지점 매핑(§3) — lifecycle 7행 → loop-binding.md §3 전이 이벤트 기록 지점·agent 3행 → delegation-protocol.md §3 위임/완료/실패 메시지 지점·memory 2행 → memory-binding.md §3.1(Record)/§3.2(Recall) 물리 절차 지점을 형태 A 실계측 가능으로, runtime 6행 → runtime-binding.md 연산 실현 지점의 규약 지점 매핑(실행 계측은 형태 B)으로 정직 구분(Advisor 결정 — OQ-4 해소); 시연 소비 예정 이벤트 `lifecycle.complete` @ after는 형태 A 실계측 가능으로 명시. Hook Module 직렬화·등록 물리 절차 확정(§4) — `.claude/hooks/` 하위 자기완결 경계 구조·Hook Binding 6필드(§3.2-D) 직렬화 표기·등록 = 01 §3.1-A Register 바인딩 경유(형태 A 규약 등록, runtime-binding.md §3.2 동형); **[Advisor 결정 DP-E3] `.claude/settings.json` 생성·수정 0**, 08 §4.1 행 1 "settings.json의 hooks 선언"은 형태 A(표면 정의 실재)/형태 B(실행 훅 선언 — 미도입) 정직 구분으로 실현. Hook Dispatch 물리 절차 확정(§5) — 형태 A 호스트(주 세션 오케스트레이션) 절차 구동·실행 순서 08 §3.1-D 3단 기준(order 오름차순 → Module 등록 순서 → hookId 사전순, 문면 보존)·격리·비차단(INV-2 blocking 항상 false)·Hook Failure Report 6필드(§3.2-E) 직렬화·read-only(INV-3)·Event Record 5필드(§3.2-C) 전달. 08 §4.2 이식 교체 지점 SP-1~5 대응 표(§6 — "교체되는 것/유지되는 것", 유지 열 08 §4.2 유지 목록 전건 커버). 상태 서술 실측 대조 표(§7 — 실재 서술 전건 파일 시스템 실측 후 기입, L-07; `.claude/hooks/` 빈 디렉터리·레퍼런스 Hook 실물 미생성을 실재 불주장으로 정직 기록). 08 §3·01 §3 계약 재정의·창설 0, 새 Event·새 필드·새 reason 신설 0, Glossary 밖 새 용어 0. 동시 작성 형제 산출물(skills-binding·framework/plugins/ 문서·시연 절차서) 불인용(07 R2), 레퍼런스 Hook 실물 실재 불주장(L-07). 이 1파일만 생성 — `.claude/hooks/` 실물·`.claude/settings.json`·specs/·docs/·다른 Baseline 산출물 무수정. | Worker (Advisor 위임, Task EX-H1) |
| 2026-07-06 | v0.8 Draft (r2) | Advisor 개정 지시 반영 — §10 요약 유지 목록 계수 표기 교정("6항"→"5항", §6 5항 계수와 정합화). 본문 여타 지점 무변경, 동종 계수 표기 전수 재스캔 잔여 0건. | Worker (Advisor 개정 지시, Task EX-H1 r2) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.9 Draft (개정 — §7 시연 후 상태 반영) | 비차단 관찰 1 해소 (docs/v0.8-verification-report.md §3.7 관찰 1 · 사용자 결정 DP-U3(a), 2026-07-06). §7 실측 대조 표의 시연 전 "빈 디렉터리 / 레퍼런스 Hook 실물 미생성" 스냅샷 및 같은 상태를 서술하는 전 지점(§0·§2 등록 표면 트리·§2 표 "실재 여부" 열·§2 주·§4.1·§7·§10 — `grep` 전수 열거, L-06)을 시연(PS-4 · EX-DH) 후 실측 실재로 전수 갱신. 착수 시 직접 재실측(L-07): `.claude/hooks/audit-complete/`(F-H1 — manifest.md·audit.sh) 레퍼런스 Hook 실물 실재. `.claude/settings.json`은 **여전히 미존재**(DP-E3 유지)이고 형태 B 실행 훅·native hook 실행 메커니즘 미도입도 불변. §3·§5·§6 계약 서술·SP 표·DP-E3 결정 무변경(개정은 상태 서술·이력·상태 라인에 한정). memory-binding.md r2·loop-binding.md WF13 전수 갱신 선례 동형. 기존 이력 행(v0.8 Draft·r2·Baseline) 문면 불변(L-10). | Worker (Advisor 위임, Task T7) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지). loop-data/·memory-data/·`.claude/` 참조는 백엔드/라이브 경로로 무변경, 삭제 산출물 본문 참조 없음. 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/08-hooks.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·카탈로그 Event ID·필드)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다. Hooks는 별도 Module 구현 디렉터리(framework/hooks/)를 두지 않는다 — Runtime의 Module 등록 계약(01 §3.1-A)을 확장점으로 그대로 사용하며(08 §2·§3.1-C·INV-4), 그 등록 표면의 물리 실현이 본 문서다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 08 §4가 "Hook Module 정의·직렬화·이벤트 계측·Dispatch·Event Record 전달·action 진입점의 구체 실현은 Adapter Binding(§4) 소관"이라며 미룬 **직렬화 형식·파일 구조·저장 위치·계측 지점 물리 참조·Dispatch 물리 절차·action 진입점**이 실재하는(확정되는) 유일한 자리다(08 §4.1·§4.2, §3.2-C `contextView`/`occurredAt` 물리 표현, §3.2-A "방출 경계는 §4 조율").
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 08 §3.3 INV-8). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형식명, 물리 경로 `framework/adapters/claude/…`·`.claude/…`, 파일 확장자, 세션/턴, 서브에이전트 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(runtime-binding.md §0·memory-binding.md §0·verifier-binding.md §0·loop-binding.md §0과 동형).
- **방출 주체 소관 확정(OQ-H2 — §4 소관).** 08 §9 결정 기록은 "이벤트 방출 주체는 §4(Adapter Binding) 소관으로 확정. 계약 수준 고정 불필요"로 OQ-H2를 승인했다. 본 문서가 그 §4 소관자다 — Bootstrap(형태 A)에서 방출 주체는 **호스트 오케스트레이션(주 세션)**이 원천 지점을 관찰하는 것으로 실현되며(§3·§5), 형태 B에서는 원천 직접 방출 또는 공용 dispatch 관찰로 실현된다. 계약(08 §3)은 관찰 가능한 표면(카탈로그·Event Record·순서·격리)만 고정하고 방출 주체를 고정하지 않았으므로, 본 문서의 방출 주체 매핑은 계약 창설이 아니다.
- **창설 금지.** 이 문서는 08 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.8 산출물(Hooks 확장점)의 물리 실현 매핑으로 한정한다. 새 Event·새 domain·새 phase·새 Hook Binding 필드·새 Hook Failure Report reason·새 불변 규칙을 만들지 않는다(08 §3.2-B 확장 규칙·§3.3 준수).
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, runtime-binding.md §0, delegation-protocol.md §0). Hooks는 정식 실행 Module이 아니라 규약 문서(08·본 문서)와 관행(호스트가 원천 지점을 관찰해 바인딩된 Hook을 순서대로 격리 호출)으로 실현된다(형태 A). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(자매 바인딩 4문서·계측 지점 참조원·`.claude/hooks/` 등록 표면 디렉터리 — §7 실측)과, **실행 코드 도입 시 로딩될 지점**(형태 B — 하네스의 hook 실행 메커니즘·이벤트 방출 계측 코드)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(done 7, L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(Active Lesson L-07 — 상태 서술은 실측 후 기록, A5 재발 방지). §2·§3·§7의 "실재" 서술 전건은 파일 시스템 직접 실측에 근거한다 — 미존재를 실재로 쓰지 않는다. **`.claude/hooks/`에는 시연 PS-4(EX-DH)가 이 정본 구조대로 생성한 레퍼런스 Hook 실물 `audit-complete/`(F-H1 — manifest.md·audit.sh)가 실재한다**(v0.9 T7 개정 시 재실측, §7). EX-H1(본 문서)은 등록 표면 구조·직렬화 표기의 정본만 소유했고 실물은 시연 Task가 생성했다(생성 주체 구분, L-07). `.claude/settings.json`은 여전히 미존재다(DP-E3 유지, §4.3·§7).
- 용어는 specs/00-glossary.md 정본만 사용한다. Event·Event Catalog·Phase(before/after)·Hook Binding·Hook Dispatch는 Glossary §3.2-J J-08 정본이며(08 §9 요청으로 Advisor 승인 추가), 본 문서는 그 물리 실현만 확정한다. `형태 A/B`는 structure.md 서술 라벨의 인용이며 Glossary 표제어가 아니다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 08 §4.1(Hooks Claude Code Binding)을 이 환경 위에 **v0.8 시점의 구체 물리 실현**으로 매핑한다.

책임은 다섯 가지다.

- 08 §4.1 바인딩 표의 **5행 전부**를 물리 표면(Hook Module 정의·직렬화·이벤트 계측 지점·Hook Dispatch·Event Record 전달·action 진입점)으로 확정하고, Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을 "실재 여부" 열로 정직하게 구분한다(§2, done 1·7).
- 이벤트 카탈로그(08 §3.2-A) **18행 전부**의 계측 지점을 자매 바인딩(loop·delegation·memory·runtime)의 확정 물리 지점에 매핑하고, 형태 A 실계측 가능 / 규약 지점 매핑(실행 계측 형태 B)을 정직하게 구분한다(§3, done 2 — OQ-4 해소).
- Hook Module의 직렬화·등록 물리 절차를 확정한다(§4, done 3) — `.claude/hooks/` 하위 자기완결 경계 구조, Hook Binding 6필드(§3.2-D) 직렬화 표기, 등록 = 01 §3.1-A Register 바인딩 경유(형태 A), DP-E3(settings.json 생성 0·형태 A 표면/형태 B 실행 훅 정직 구분).
- Hook Dispatch의 물리 절차를 예/아니오 판정 가능한 형태로 확정한다(§5, done 4) — 형태 A 호스트 절차 구동, 08 §3.1-D 3단 순서, 격리·비차단(INV-2 blocking=false), Hook Failure Report(§3.2-E) 직렬화, read-only(INV-3), Event Record(§3.2-C) 전달.
- 08 §4.2 이식 교체 지점 SP-1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§6, done 6). 그리고 상태 서술을 실측과 대조한다(§7, done 7).

이 문서는 08 §3의 어떤 계약 요소도 재정의·확장하지 않는다(§0·§8, done 5). 형태 A → 형태 B 전환 시에도 Core Contract(08 §3) 변경은 0이며(structure.md §7 C-1), 이 문서(§6의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 08 §4.1 바인딩 표 5행 물리 실현 (done 1·7)

08 §4.1 Claude Code Binding 표의 **5행 전부**를 물리 표면으로 매핑한다. 아래 표의 "정본 인용(원문 그대로)" 열은 08 §4.1 표현을 문자 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·구조·형식·채널·절차를, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정을 정직하게 구분한다(§7 실측 대조). "실재" 서술은 전건 파일 시스템 실측 후 기입했다(L-07).

등록 표면 디렉터리 구조(본 문서 정본 — 08 §4.1 행 1·5 물리 실현; 레퍼런스 Hook 실물 `audit-complete/`(F-H1)는 시연 PS-4 생성으로 실재, §7 재실측):

```
.claude/
├─ hooks/                       # Hook Module 등록 표면 (확장 Module 표면 — 01 §4.1·runtime-binding.md §2 #3; 시연 PS-4가 생성한 audit-complete/(F-H1) 실재)
│  └─ <hookModuleId>/           #   Hook Module 자기완결 경계 (01 §3.2-E 규칙 2; 예: audit-complete/(F-H1) — 시연 PS-4 생성 실재, §4·§7)
│     ├─ manifest.md            #     Module Manifest(01 §3.2-A 7필드) + Hook Binding 선언(§3.2-D 6필드) — Markdown + front-matter
│     └─ <action>               #     Hook action 진입점 (스크립트·명령 — 08 §4.1 행 5)
├─ agents/                      # 실재 — 역할 진입점 4파일(자매 참조, §7 실측)
└─ settings.json                # 미존재 — 생성·수정 0 (DP-E3; 형태 B 실행 훅 선언 자리, 미도입)
```

| # | §3 계약 요소 | 정본 인용(원문 그대로) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Hook Module 정의·직렬화 (§3.2-D) | `.claude/hooks/` 하위 정의와 `.claude/settings.json`의 hooks 선언. Manifest 직렬화는 01 §4.1(Markdown + front-matter / 설정 파일)을 따른다. | Hook Module = `.claude/hooks/<hookModuleId>/` 자기완결 경계(01 §3.2-E 규칙 2). 그 안에 Module Manifest(01 §3.2-A 7필드, Markdown + front-matter — runtime-binding.md §3.1 직렬화 동형)와 Hook Binding 선언(§3.2-D 6필드)을 둔다. 물리 구조·6필드 직렬화 표기의 정본은 §4. **`.claude/settings.json`의 hooks 선언**은 형태 A(표면 정의 = `.claude/hooks/` 실재) / 형태 B(실행 훅 선언 — settings.json, 미도입)로 정직 구분한다(DP-E3, §4.3). | 등록 표면 디렉터리(`.claude/hooks/`) 실재(§7 실측). 시연 PS-4가 생성한 레퍼런스 Hook `audit-complete/`(F-H1) 실재(v0.9 T7 재실측). 6필드 직렬화 표기 확정(정본, §4). settings.json hooks 선언(형태 B 실행 훅)은 미도입(DP-E3 — `.claude/settings.json` 미존재). |
| 2 | Event 방출·계측 지점 (§3.2-A) | Claude Code 세션/턴에서 이벤트 원천(lifecycle 전이, runtime 연산, agent 메시지, memory Port 접근)이 발생하는 지점의 계측. | 18행 카탈로그(08 §3.2-A) 각 Event의 계측 지점을 자매 바인딩의 확정 물리 지점에 매핑한다 — lifecycle → loop-binding.md §3(전이 이벤트 기록)·agent → delegation-protocol.md §3(위임/보고 메시지)·memory → memory-binding.md §3.1/§3.2(Record/Recall)·runtime → runtime-binding.md §3.2~§3.4(연산 실현 규약 지점). 방출 주체(형태 A) = 호스트 관찰(OQ-H2). 매핑 정본은 §3. | 형태 A 실계측 가능(lifecycle·agent·memory) / 규약 지점 매핑 실재·실행 계측 형태 B(runtime). 무인 자동 방출 계측(형태 B)은 미도입. §3 참조. |
| 3 | Hook Dispatch·순서·격리 (§3.1-D/E) | Claude Code 하네스의 hook 실행 메커니즘이 결정적 순서와 격리 실행을 실현한다. | Bootstrap(형태 A)에서 Dispatch는 **호스트(주 세션 오케스트레이션)** 절차로 구동된다 — (event, phase)에 바인딩된 Hook을 08 §3.1-D 3단 순서(order 오름차순 → Module 등록 순서 → hookId 사전순)로 정렬해 격리 호출하고, 실패는 Hook Failure Report(§3.2-E, blocking=false)로 남기고 계속한다(INV-2). 하네스의 native hook 실행 메커니즘(settings.json 실행 훅)은 형태 B. 물리 절차의 정본은 §5. | 호스트 절차 구동 규약 실현(형태 A). 하네스 native hook 실행 메커니즘(형태 B)은 미도입(DP-E3). |
| 4 | Event Record 직렬화 (§3.2-C) | 하네스가 원천 컨텍스트를 읽기 전용으로 Hook action에 전달하는 형태. | Dispatch가 원천 지점(§3)에서 읽기 전용 투영을 구성해 Event Record 5필드(§3.2-C: `eventId`/`phase`/`sourceRef`/`contextView`/`occurredAt`)를 action에 전달한다. `sourceRef`·`contextView`는 원천 계측 지점 참조(§3, `contextView` 스키마는 원천 spec 소유 — §8 조율), `occurredAt`은 순서 값(논리 시각, L-09 — 벽시계 아님). Hook은 읽기만 한다(INV-3). 물리 표현은 §5.2. | 읽기 전용 전달 규약 실현(형태 A). 하네스 컨텍스트 투영 채널 코드(형태 B)는 미도입. |
| 5 | Hook action 진입점 (§3.2-D `action`) | `.claude/hooks/` 스크립트·명령 진입점. 실행 모델 지정은 02 §4 실행 모델 바인딩과 정합한다. | Hook Binding `action`(§3.2-D) = `.claude/hooks/<hookModuleId>/` 자기완결 경계 안의 스크립트·명령 진입점(§4.1). Manifest `entrypoint`(01 §3.2-A)의 물리 해소는 §4.2. 실행 모델 지정은 02 §4 소관 — 본 문서는 참조만 한다(08 §4.1 정본 문면 보존). | 진입점 구조 확정(정본, §4). 레퍼런스 action 실물 `audit-complete/audit.sh`(F-H1)는 시연 PS-4 생성으로 실재(v0.9 T7 재실측, §7). 실행 모델 = 02 §4 소관. |

주:

- 위 5행은 08 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 08 §4.1 정본 표현을 이 환경의 구체 경로·형식·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **물리 실재 / 형태 A / 형태 B 구분(정직).** 행 1의 등록 표면 디렉터리(`.claude/hooks/`)·행 2·3·4의 계측·Dispatch·Event Record 참조원(자매 바인딩 4문서·계측 지점)은 물리 실재다. 행 1·3의 정의·Dispatch **수행**은 Bootstrap에서 규약 실현(형태 A)이다 — 호스트 관찰·호스트 절차 구동으로 수행되며, 하네스 native hook 실행 메커니즘(settings.json 실행 훅)·무인 방출 계측은 형태 B다(DP-E3). 행 1의 6필드 직렬화 표기·행 5의 진입점 구조는 정본으로 확정됐고, 레퍼런스 Hook Module 실물은 시연 PS-4(EX-DH)가 이 정본 구조대로 생성해 실재한다(`.claude/hooks/audit-complete/` — F-H1, v0.9 T7 재실측; 생성 주체 구분, L-07 — memory-binding.md §2 주·loop-binding.md §2 주가 백엔드 데이터 생성 주체를 시연 Task로 구분한 관례 동형).
- **Hooks = Runtime Module 등록 재사용(INV-4).** Hook 등록은 별도 메커니즘이 아니라 Runtime의 Module 등록 계약(01 §3.1-A Register)을 그대로 사용한다(08 §3.1-C·INV-4). 따라서 등록·해소·교체가 runtime-binding.md §3.2 Register/Resolve/Replace 수행 방식과 동형으로 실현된다(§4.2). 이는 서브에이전트로 디스패치되는 Agent Module(verifier-binding.md §3.1)과도, 단일 Port로 소비되는 Cross-cutting Service(memory-binding.md §4.1)와도 구별되는 세 번째 실현 방식이다 — Hook은 등록만 되고 원천 이벤트 발생 시 호스트 Dispatch가 호출한다(§5).

---

## §3. 이벤트 카탈로그 18행 계측 지점 매핑 (done 2 — OQ-4 해소)

08 §4.1 행 2("Event 방출·계측 지점 (§3.2-A)")의 물리 실현이다. 08 §3.2-A 이벤트 카탈로그 **18행 전건**의 계측 지점을, 자매 바인딩이 확정한 물리 지점에 매핑한다. **Event ID·domain·원천 계약·phase 계약의 정본은 08 §3.2-A이며, 본 절은 각 Event의 계측 지점(물리 참조원)과 실재 여부(형태)만 확정한다**(재정의 0, 새 Event 0).

방출 경계 정합은 08 §9 결정 기록이 이미 확인했다 — "lifecycle 이벤트는 03 §3.2-A 전이 이벤트 기록 시점과, memory 이벤트는 04 §3.1 Record/Recall 연산과 대응 — 모순 없음". 본 절은 그 대응을 이 환경의 확정 물리 지점(loop-binding.md·memory-binding.md·delegation-protocol.md·runtime-binding.md)으로 좁힌다. 각 계측 지점 참조원의 물리 실현은 그 자매 문서가 소유하며, 본 문서는 참조만 한다(재정의 0).

**실재 여부(형태) 정직 구분 원칙(Advisor 결정 — OQ-4 해소):**

- **형태 A 실계측 가능** — 계측 지점이 Bootstrap에서 물리적으로 산출되는 관찰 가능한 산출물(loop-data/ 전이 이벤트 기록·서브에이전트 위임/최종 응답 메시지·memory-data/ Record/Recall 물리 절차)에 대응하므로, 그 지점의 before/after에서 Hook을 실계측(관찰)할 수 있다.
- **규약 지점 매핑 실재 / 실행 계측 형태 B** — 계측 지점이 규약 실현(형태 A)인 runtime 연산(정의 파일 배치·위임 시 로딩·세션 개시/종료 규약)에 대응하므로, 규약 지점 매핑은 실재하나 per-연산 방출을 계측하는 실행 코드는 형태 B다.

| Event ID | Domain | 원천 계약 (정본 08 §3.2-A) | 계측 지점 (물리 참조원 — 재정의 0) | 실재 여부 (형태) |
|---|---|---|---|---|
| `lifecycle.consult` | lifecycle | Glossary §3.2-F | loop-binding.md §3 — loop-data/`<cycle_id>.jsonl` 전이 이벤트(`to_stage`=Consult) 기록 지점 | 형태 A 실계측 가능 |
| `lifecycle.plan` | lifecycle | Glossary §3.2-F | loop-binding.md §3 — 전이 이벤트(`to_stage`=Plan) 기록 지점 | 형태 A 실계측 가능 |
| `lifecycle.execute` | lifecycle | Glossary §3.2-F | loop-binding.md §3 — 전이 이벤트(`to_stage`=Execute) 기록 지점 | 형태 A 실계측 가능 |
| `lifecycle.verify` | lifecycle | Glossary §3.2-F | loop-binding.md §3 — 전이 이벤트(`to_stage`=Verify) 기록 지점. Hook은 Verify 판정을 대체·무효화하지 않고 관찰만 한다(INV-7, 08 §9 06 조율) | 형태 A 실계측 가능 |
| `lifecycle.learn` | lifecycle | Glossary §3.2-F | loop-binding.md §3 — 전이 이벤트(`to_stage`=Learn) 기록 지점 | 형태 A 실계측 가능 |
| `lifecycle.memoryUpdate` | lifecycle | Glossary §3.2-F | loop-binding.md §3 — 전이 이벤트(`to_stage`=Memory Update) 기록 지점 | 형태 A 실계측 가능 |
| `lifecycle.complete` | lifecycle | Glossary §3.2-F | loop-binding.md §3 — 전이 이벤트(`to_stage`=Complete) 기록 지점. **★ 시연 소비 예정**(08 §7·§8 예1 — `lifecycle.complete` @ after 감사 로그) | 형태 A 실계측 가능 |
| `agent.delegation` | agent | 02 §3.2-B | delegation-protocol.md §3.1 — 위임 디스패치(서브에이전트 위임, 위임 메시지 02 §3.2-B) 발신·수신 지점 | 형태 A 실계측 가능 |
| `agent.completionReport` | agent | 02 §3.2-C | delegation-protocol.md §3.2 — 완료 보고(서브에이전트 최종 응답, 02 §3.2-C) 생성 지점 | 형태 A 실계측 가능 |
| `agent.failureReport` | agent | 02 §3.2-D | delegation-protocol.md §3.2·§3.4 — 실패 보고(최종 응답, 02 §3.2-D) 생성 지점 | 형태 A 실계측 가능 |
| `runtime.register` | runtime | 01 §3.1-A | runtime-binding.md §3.2 Register — Module 정의 파일 배치(규약 실현) 지점 | 규약 지점 매핑 실재 / 실행 계측 형태 B |
| `runtime.resolve` | runtime | 01 §3.1-A | runtime-binding.md §3.2 Resolve — 위임 시 활성 정의 파일 로딩(규약 실현) 지점 | 규약 지점 매핑 실재 / 실행 계측 형태 B |
| `runtime.replace` | runtime | 01 §3.1-A | runtime-binding.md §3.2 Replace — 동일 계약 정의 파일 교체(규약 실현) 지점 | 규약 지점 매핑 실재 / 실행 계측 형태 B |
| `runtime.loadConfig` | runtime | 01 §3.1-B | runtime-binding.md §3.3 Load Config — 스코프별 소스 병합(형태 B 로더) 지점 | 규약 지점 매핑 실재 / 실행 계측 형태 B |
| `runtime.bootstrap` | runtime | 01 §3.1-C | runtime-binding.md §3.4 Bootstrap — 세션 개시(규약 실현) 구간 | 규약 지점 매핑 실재 / 실행 계측 형태 B |
| `runtime.shutdown` | runtime | 01 §3.1-C | runtime-binding.md §3.4 Shutdown — 세션 종료(규약 실현) 구간 | 규약 지점 매핑 실재 / 실행 계측 형태 B |
| `memory.recall` | memory | ARCHITECTURE 5.1, 02 §5 | memory-binding.md §3.2 Recall — 단일 Port index-first 회수(읽기) 물리 절차 지점 | 형태 A 실계측 가능 |
| `memory.record` | memory | ARCHITECTURE 5.1, 02 §5 | memory-binding.md §3.1 Record — 단일 Port Item 기록 + Index 갱신(쓰기) 물리 절차 지점 | 형태 A 실계측 가능 |

주:

- 위 18행은 08 §3.2-A 카탈로그의 전 행이다(lifecycle 7 + agent 3 + runtime 6 + memory 2 = 18). 각 행의 계측 지점은 08 §3.2-A 원천 계약을 이 환경의 확정 물리 참조원으로 좁힌 것이며, 새 Event·새 domain을 창설하지 않는다(08 §3.2-B 확장 규칙 준수 — 추측 이벤트 0, INV-6).
- **모든 Event는 before·after 두 phase를 가진다(08 §3.2-A).** phase는 Event ID의 일부가 아니라 Hook이 바인딩 시점에 선택한다(08 §3.2-B). 계측 지점의 before = 원천 연산·전이·메시지 생성·Port 접근 직전, after = 직후. 시연 소비 예정 이벤트 `lifecycle.complete` @ after는 Complete 전이 기록 직후의 계측이며, loop-data/에 실재하는 전이 이벤트 기록에 대응하므로 **형태 A 실계측 가능**이다.
- **형태 A / 형태 B 구분 근거(정직).** lifecycle·agent·memory 계측 지점은 Bootstrap에서 물리적으로 산출되는 관찰 가능한 산출물에 대응한다 — lifecycle은 loop-data/ 전이 이벤트 기록(loop-binding.md §7 실측 — 시연 데이터 실재), agent는 서브에이전트 위임/최종 응답(delegation-protocol.md §3 물리 채널), memory는 memory-data/ Record/Recall 물리 절차(memory-binding.md §7 실측 — 데이터 실재). 따라서 그 지점의 Hook은 형태 A에서 실계측(관찰) 가능하다. runtime 계측 지점은 규약 실현(형태 A)인 runtime 연산(정의 파일 배치·위임 시 로딩·세션 개시/종료 규약)에 대응하므로 — 규약 지점 매핑은 실재하나 per-연산 방출을 계측하는 실행 코드는 형태 B다(runtime-binding.md §2·§3 형태 구분과 정합).
- **방출 주체(형태 A) = 호스트 관찰(OQ-H2 — §4 소관).** Bootstrap에서 이벤트 방출은 원천이 직접 방출하는 실행 코드가 아니라 **호스트 오케스트레이션(주 세션)이 원천 지점을 관찰**해 Event Record를 구성하고 Dispatch를 구동하는 것으로 실현된다(§5). 이는 08 §3.2-A가 "정확한 방출 경계는 §4 조율"로, 08 §9 OQ-H2가 "방출 주체는 §4 소관"으로 미룬 지점의 이 환경 확정이며, 형태 B(원천 직접 방출 또는 공용 dispatch 관찰)로 전환해도 관찰 가능한 표면(카탈로그·Event Record·순서·격리)은 불변이다(INV-1·§6).
- **경계 불가침(INV-7).** 계측은 관찰이며 원천 연산·전이·메시지·Port 접근을 변경하지 않는다(INV-1·INV-3). memory 도메인 Event의 관찰이 Memory 접근은 아니다(08 §5) — Hook action이 Memory에 기록·회수하려면 단일 Port(memory-service.md §7)만 경유한다(INV-7, §4.4). lifecycle.verify Event의 관찰이 Verify 판정을 대체·무효화하지 않는다(INV-7).

---

## §4. Hook Module 직렬화·등록 물리 절차 (done 3)

08 §4.1 행 1("Hook Module 정의·직렬화")·행 5("Hook action 진입점")의 물리 실현을 확정한다. **이 문서는 Adapter 경계이므로 구체 직렬화 형식·물리 경로 토큰의 사용이 허용된다(§0 격리 지점).** 계약 요소(Hook Binding 6필드·의미·필수 표기, Module Manifest 7필드, Register 완료 조건·reason)의 정본은 08 §3.2-D·§3.1-C·01 §3.2-A·§3.1-A이며, 본 절은 그 물리 실현만 확정한다(재정의 0).

### §4.1 Hook Module 자기완결 경계 구조 (08 §4.1 행 1·5)

- **물리 위치·구조(정본).** Hook Module은 확장 Module 등록 표면 `.claude/hooks/`(01 §4.1·runtime-binding.md §2 #3, 실재 — 시연 PS-4 생성 `audit-complete/`(F-H1) 실재, §7) 아래 **자기완결 경계**(01 §3.2-E 규칙 2)로 배치한다: `.claude/hooks/<hookModuleId>/`. 그 경계 안에 한 Module의 요소(Manifest·Hook Binding 선언·action 진입점)를 모은다 — 한 Module의 요소가 여러 경계로 흩어지지 않는다(structure.md §3 규칙 2 동형).
  - `manifest.md` — Module Manifest(01 §3.2-A 7필드)를 Markdown 본문 + YAML front-matter로 직렬화한다(runtime-binding.md §3.1 직렬화 동형, 01 §4.1 "Markdown + front-matter"). Hook Binding 선언(§3.2-D 6필드)을 이 Module의 자기완결 경계 안에 둔다(08 §3.1-C — "자기완결적 경계 안에 Hook Binding 선언을 둔다"). 한 Module은 하나 이상의 Hook Binding을 담을 수 있다(08 §3.2-D).
  - `<action>` — Hook action 진입점(스크립트·명령, 08 §4.1 행 5). 순수 observer Hook(감사 로그 등, 08 §8 예1)이면 action이 간단해 Module을 단일 파일 `.claude/hooks/<hookModuleId>.md`로 두는 축약형도 허용된다(`.claude/agents/*.md` 단일 파일 Module 동형) — 이 경우 action은 그 파일 내 진입점 참조다.
- **직렬화 형식 = Adapter 선택.** Markdown + front-matter는 이 환경의 직렬화 선택이며(01 §4.1), 이식 시 대상 환경의 확장 정의 메커니즘으로 교체된다(SP-1, §6). 이 형식 선택은 계약(08 §3.2-D 필드·필수 표기)을 바꾸지 않는다.
- **레퍼런스 Hook 실물 실재 — 생성 주체 구분(L-07).** 위 구조는 본 문서가 확정한 **정본 구조**이며, 그 구조대로의 레퍼런스 Hook Module 실물은 시연 PS-4(EX-DH)가 생성해 **실재**한다(v0.9 T7 개정 시 §7 재실측 — `.claude/hooks/audit-complete/`, F-H1). 실물 생성은 시연 Task 소관이며(memory-data/·loop-data/ 데이터를 시연 Task가 생성한 관례 동형), 본 문서(EX-H1)는 구조·직렬화 표기의 정본만 소유한다 — 실물을 생성하지 않았다(생성 주체 구분).

### §4.2 Hook Binding 6필드 직렬화 표기 (정본 08 §3.2-D)

Hook Binding 6필드(08 §3.2-D)를 이 환경의 `manifest.md` 자기완결 경계 안 구조화 선언(front-matter 또는 구조화 블록)으로 직렬화한다. **필드명·의미·필수 표기의 정본은 08 §3.2-D이며, 본 표는 그 물리 직렬화 표기만 확정한다**(재정의 0, 새 필드 0).

| Hook Binding 필드 (정본 08 §3.2-D) | 필수 | 물리 직렬화 (이 Adapter 확정 — 선언 내 값) |
|---|---|---|
| `hookId` | 예 | 문자열 — Hook 고유·안정 식별자. Module 내·across Module 유일(중복 시 `DuplicateHookId` — 08 §3.1-C). 순서 3차 tie-breaker의 사전순 대상(§5, 08 §3.1-D). |
| `event` | 예 | 문자열 — 카탈로그(§3.2-A/§3 매핑 표) Event ID(예 `lifecycle.complete`). 카탈로그 부재 값이면 등록 거부(`UnknownEvent` — 08 §3.1-C). |
| `phase` | 예 | 문자열 — `before` \| `after` 중 하나. 그 외 값이면 등록 거부(`InvalidPhase` — 08 §3.1-C). |
| `order` | 아니오(기본 0) | 정수 — 실행 우선순위(작을수록 먼저). 생략 시 기본 0. 순서 1차 기준(§5, 08 §3.1-D). |
| `action` | 예 | 참조 — Module 경계 안 action 진입점(§4.1 `<action>` 스크립트·명령 또는 단일 파일 진입점 참조). Manifest `entrypoint` 물리 해소와 정합(§4.3). |
| `replaceable` | 아니오(기본 true) | 불리언 — 교체 가능 여부. 생략 시 기본 true. 01 INV-1(동일 contract·소비자 참조 불변)을 따른다(08 §3.2-D). |

- **필수 표기 보존(정본).** 6필드 중 4필드(`hookId`·`event`·`phase`·`action`)는 필수, 2필드(`order`·`replaceable`)는 아니오(기본값 0·true)다(08 §3.2-D). 직렬화는 이 필수/선택 지위와 기본값을 바꾸지 않는다 — 필수 필드는 모든 선언에 존재하고, 선택 필드는 생략 시 기본값이 적용된다.
- **등록 완료 조건 대조 지점(08 §3.1-C).** 각 Hook Binding의 `event`가 카탈로그(§3.2-A/§3)에 존재하고, `phase`가 유효하며, `hookId`가 유일함을 등록 시점에 대조한다(08 §3.1-C 완료 조건). 위반 시 각각 `UnknownEvent`/`InvalidPhase`/`DuplicateHookId`로 등록을 거부한다 — reason 코드의 정본은 08 §3.1-C이며 본 문서는 재정의하지 않는다. Module 계약 위반은 01 Register 실패 코드(`ContractMismatch`/`DuplicateId`)로 위임한다(08 §3.1-C).

### §4.3 등록 = 01 §3.1-A Register 바인딩 경유 (형태 A 규약 등록) · DP-E3

Hook 등록은 새 메커니즘이 아니라 Runtime의 Module 등록 계약(01 §3.1-A Register)만 사용한다(08 §3.1-C·INV-4). runtime-binding.md §3.2의 Register/Resolve/Replace 수행 방식과 동형으로 실현한다.

| 01 §3.1-A 연산 (정본) | Hook Module 물리 실현 (claude 환경) | 형태 |
|---|---|---|
| Register (01 §3.1-A) | Hook Module 정의(`.claude/hooks/<hookModuleId>/`)를 등록 표면에 배치한다(runtime-binding.md §3.2 Register — "정의 파일 배치"). `id`(=`hookModuleId`) 유일성은 디렉터리명 충돌 없음으로 보장(`DuplicateId` 방지). 배치와 함께 각 Hook Binding의 카탈로그 존재·phase 유효·hookId 유일이 대조된다(§4.2, 08 §3.1-C). | 규약 실현(형태 A — 정의 배치) |
| Resolve (01 §3.1-A) | 카탈로그 Event 발생 시 그 (event, phase)에 바인딩된 Hook 집합을 해소한다 — Hook Registry(08 §3.1-C)에 반영된 Binding에서 (event, phase) 일치분을 모은다. 이 해소가 Dispatch 입력이다(§5). | 규약 실현(형태 A) |
| Replace (01 §3.1-A) | Hook Module 교체는 동일 contract·소비자 참조 불변(01 INV-1, 08 §3.2-D `replaceable`)을 따른다 — Hook 추가·교체·제거는 본체를 수정하지 않는다(08 INV-1·INV-4). 정의 파일 교체로 실현(runtime-binding.md §3.2 Replace 동형). | 규약 실현(형태 A) |

- **[Advisor 결정 DP-E3] `.claude/settings.json` 생성·수정 0 — 형태 A/B 정직 구분.** 08 §4.1 행 1은 Hook Module 정의를 "`.claude/hooks/` 하위 정의와 `.claude/settings.json`의 hooks 선언"으로 바인딩한다. 이 두 표면을 다음과 같이 정직하게 구분한다.
  - **형태 A (표면 정의 실재).** Hook Module의 정의·등록은 `.claude/hooks/` 등록 표면(실재 — §7 실측)에 자기완결 경계를 배치하는 것으로 실현된다(§4.1·이 절 Register 행). 이것이 v0.8 Bootstrap의 실현 자리다.
  - **형태 B (실행 훅 선언 — 미도입).** `.claude/settings.json`의 hooks 선언은 하네스의 **실행 시점 훅 선언 메커니즘**(원천 이벤트에 실행 코드를 자동 결선하는 자리)이며, 이는 형태 B다 — **본 문서는 `.claude/settings.json`을 생성·수정하지 않는다**(DP-E3). 실측상 `.claude/settings.json`은 현재 미존재다(§7). 형태 B 실행 훅 선언 도입 시에도 08 §3(카탈로그·Event Record·순서·격리·Invariants)은 불변이며(structure.md §7 C-1), 본 절은 그 도입을 선취·추측하지 않는다(추측 금지, §0 창설 금지).
- **형태 구분 명시.** v0.8 Bootstrap에서 등록은 `.claude/hooks/` 정의 배치로 규약 실현(형태 A)되며, 실행 Registry·실행 훅 선언(형태 B) 도입 시에도 01 §3.1-A Register 계약·08 §3.1-C 완료 조건은 변경 0이다(runtime-binding.md §3.2 형태 B 주 동형).

### §4.4 Manifest `entrypoint` 물리 해소 · Memory 접근 경로 (해당 시)

- **`entrypoint` 물리 해소(형태 A/B).** Module Manifest `entrypoint`(01 §3.2-A 추상 참조)는 형태 A(Bootstrap)에서 `.claude/hooks/<hookModuleId>/` 경계 안 action 진입점(§4.1)으로 규약 실현되며(별도 실행 진입점 파일 없음, runtime-binding.md §3.1 `entrypoint`=정의 파일 동형), 형태 B에서 Hook action을 노출·구동하는 실행 코드 로케이터로 해소된다. 경계 간 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지, verifier-binding.md OQ-VB-2·loop-binding.md OQ-LB-2 동형).
- **Hook action의 Memory 접근(INV-7).** Hooks Component 계약 자체는 Memory를 읽거나 쓰지 않는다(08 §5). 다만 특정 Hook의 action이 Memory에 기록·회수를 수행한다면, 그 접근 경로는 **Memory Service Interface(단일 Port)** 하나뿐이며(memory-binding.md가 확정한 백엔드 `memory-data/`를 memory-service.md §7 경유), 영속성 백엔드에 직접 접근하지 않는다(08 §5·INV-7). 본 문서는 그 물리 배선을 재정의하지 않고 참조만 한다(memory-binding.md 소관).

---

## §5. Hook Dispatch 물리 절차 (done 4)

08 §4.1 행 3("Hook Dispatch·순서·격리 (§3.1-D/E)")·행 4("Event Record 직렬화 (§3.2-C)")의 물리 실현을 예/아니오 판정 가능한 형태로 확정한다. 계약(08 §3.1-D Dispatch·순서 / §3.1-E 실패 처리 / §3.2-C Event Record / §3.2-E Hook Failure Report / INV-2·INV-3·INV-5)은 재정의하지 않고 § 포인터로만 인용한다.

### §5.1 형태 A Dispatch 절차 — 호스트(주 세션 오케스트레이션) 구동

Bootstrap(형태 A)에서 Hook Dispatch는 **호스트 오케스트레이션(주 세션)** 절차로 구동된다. 다음 절차는 예/아니오 판정 가능하다(각 단계가 관찰·대조 가능한 산출을 낸다).

1. **이벤트 관찰.** 카탈로그(§3) 원천 지점에서 (event, phase)가 발생하면 호스트가 이를 관찰한다(방출 주체 = 호스트, OQ-H2 §0). before = 원천 연산·전이·메시지·Port 접근 직전, after = 직후(08 §3.2-A phase 의미).
2. **바인딩 해소.** 그 (event, phase)에 바인딩된 Hook 집합을 Hook Registry(08 §3.1-C)에서 해소한다(§4.3 Resolve). 바인딩이 없으면 Dispatch는 아무 Hook도 호출하지 않고 종료한다(본 작업 결과 불변).
3. **결정적 정렬(08 §3.1-D 3단 기준 — 문면 보존).** 같은 (event, phase)에 여러 Hook이 있으면 다음 순서로 정렬한다 — **1차: `order` 오름차순(작을수록 먼저)**, **2차(동률): Module 등록 순서**, **3차(동률): `hookId` 사전순**. before·after 모두 동일 규칙을 적용한다(08 §3.1-D). tie-breaker(등록 순서 → hookId 사전순)는 OQ-H3 승인 규칙이다(08 §9).
4. **격리 호출.** 정렬 순서대로 각 Hook의 action(§4.1)을 **격리 호출**한다 — 각 호출에 Event Record(§5.2)를 읽기 전용으로 전달한다(INV-3). 바인딩된 모든 Hook이 정확히 한 번 호출된다(08 §3.1-D 완료 조건).
5. **실패 격리·비차단(08 §3.1-E, INV-2).** 한 Hook이 오류·타임아웃으로 실패해도 Hook Failure Report(§5.3)를 남기고, **본 작업과 다른 Hook은 계속 진행**된다. 한 Hook의 실패가 다른 Hook 호출을 막지 않는다(08 §3.1-D). 본 작업(이벤트 원천 연산)의 성공·결과는 Hook 결과와 독립이다(INV-1).

- **본 작업 결과 불변(INV-1·INV-2).** Dispatch는 각 Hook의 Hook Result 모음을 산출하나, 본 작업의 결과에는 영향을 주지 않는다(08 §3.1-D). 순서(3단계)는 부수 동작의 실행 순서에만 영향을 주고 본 작업 결과를 바꾸지 않는다(Hook은 비차단·격리이므로).
- **형태 B 구분.** 하네스의 native hook 실행 메커니즘(`.claude/settings.json` 실행 훅 — DP-E3, 미도입)은 이 절차를 실행 코드로 실현하는 형태 B다. Bootstrap에서 호스트 절차 구동(형태 A)이 결정적 순서·격리·비차단을 규약으로 실현하며, 형태 B 전환 시에도 08 §3.1-D/E 순서·격리·비차단 계약은 불변이다(§6 SP-3·SP-4).

### §5.2 Event Record 5필드 전달 (08 §4.1 행 4 / §3.2-C)

Dispatch 4단계에서 각 Hook에 전달되는 읽기 전용 입력이다. **필드명·의미의 정본은 08 §3.2-C이며, 본 표는 그 물리 표현만 확정한다**(재정의 0).

| Event Record 필드 (정본 08 §3.2-C) | 물리 표현 (이 Adapter 확정) |
|---|---|
| `eventId` | 문자열 — 카탈로그(§3) Event 식별자(예 `lifecycle.complete`). |
| `phase` | 문자열 — `before` \| `after`. |
| `sourceRef` | 참조 — 원천 계측 지점(§3)의 참조. lifecycle = loop-data/`<cycle_id>.jsonl` 전이 이벤트 참조(loop-binding.md §3), agent = 위임/보고 메시지 참조(delegation-protocol.md §3), memory = memory-data/ Record/Recall 참조(memory-binding.md §3), runtime = 연산 지점 참조(runtime-binding.md §3). 내용은 원천 spec 소유(§3 재정의 0). |
| `contextView` | 참조 — 원천이 노출하는 읽기 전용 컨텍스트 투영. **상세 스키마는 원천 spec 소유(§8 조율)** — Hook은 읽기만 한다(INV-3). 본 문서는 물리 전달 채널(읽기 전용 투영)만 바인딩하고 투영 스키마를 재정의하지 않는다. |
| `occurredAt` | 순서 값 — 발생 순서 기준(논리 시각). **물리 벽시계 시각이 아니다**(L-09 — loop-binding.md §3.3 `at` 물리 표현 동형). 실제 물리 시각이 필요하면 별도로 실측해 공개한다(L-09). |

- **읽기 전용 강제(INV-3).** Hook은 Event Record를 읽기만 하며 이벤트 원천의 입력·출력·상태를 변경하지 않는다(08 §3.1-B 할 수 없는 것·INV-3). Dispatch가 전달하는 것은 읽기 전용 투영이다 — Hook이 이를 변경 시도하면 INV-3 위반으로 무효다(08 §6).
- **`contextView` 스키마 소관 경계(§8 조율).** 원천이 노출하는 컨텍스트 투영의 상세 스키마는 각 원천 spec(03·02·04·01) 소유이며(08 §3.2-C), 동시 작성/미확정 스키마를 추측하지 않는다(07 R2·R3). 본 문서는 읽기 전용 전달 채널만 확정하고, 투영 내용 스키마 확정이 필요하면 조율로 에스컬레이션한다(§8 open_questions).

### §5.3 Hook Failure Report 6필드 직렬화 (08 §3.2-E)

Dispatch 5단계에서 Hook 실패 시 남기는 공통 보고 구조다. **필드명·의미의 정본은 08 §3.2-E이며(02 §3.2-D 실패 보고와 정합), 본 표는 그 물리 직렬화만 확정한다**(재정의 0, 새 reason 0).

| Hook Failure Report 필드 (정본 08 §3.2-E) | 물리 직렬화 (이 Adapter 확정) |
|---|---|
| `hookId` | 문자열 — 실패한 Hook 식별자(§4.2 `hookId`). |
| `event` | 문자열 — 바인딩된 Event ID(§3). |
| `phase` | 문자열 — `before` \| `after`. |
| `reason` | 문자열 — 사유(Hook action 오류·타임아웃·경계 위반 등, 08 §3.2-E·§6). reason 값 집합은 08 소관 — 신설 0. |
| `blocking` | **항상 `false`**(INV-2). 본 작업을 차단하지 않았음을 명시한다(08 §3.2-E). v0.1은 차단·veto Hook을 제공하지 않는다(OQ-H1 승인 — 08 §9). |
| `lesson_candidate` | 여부(예/아니오)와 한 줄 요약 — 모든 Hook 실패는 Lesson 후보다(08 §6·§3.2-E). |

- **비차단 불변의 물리 보장(INV-2).** `blocking`은 어떤 실패에서도 `false`로 직렬화된다 — v0.8은 비차단 observer 전용 Hook만 제공하며(OQ-H1 승인, 08 §9), 차단·veto·mutation은 미지원이다(08 §3.1-B·INV-1·INV-2). 이 값이 true가 되는 경로는 존재하지 않는다(차단 Hook 부재). 08 §7 비차단 시연은 이 값(blocking=false)을 확인 대상으로 삼는다.
- **Lesson 후보(08 §6).** 모든 Hook 실패는 Lesson 후보이며(08 §6·AGENT.md Memory), `lesson_candidate`에 여부·한 줄 요약을 남긴다. Memory 기록이 필요하면 단일 Port만 경유한다(§4.4·INV-7).

---

## §6. 08 §4.2 이식 교체 지점 SP-1~5 대응 (done 6)

08 §4.2 이식 교체 지점 SP-1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인하며, 08 §4.2 유지 목록(카탈로그 ID·명명 규칙·Event Record 형태·Hook Binding 필수 필드·순서/격리/비차단 계약·Invariants)을 전건 커버한다.

| # (08 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Hook 정의 위치·포맷 (`.claude/hooks/`, `.claude/settings.json` hooks → 대상 환경의 확장 정의 메커니즘) | §2 행 1·5, §4.1·§4.2·§4.3 | `.claude/hooks/<hookModuleId>/` 자기완결 경계, Markdown + front-matter 직렬화, Hook Binding 6필드 물리 표기, `.claude/settings.json` 형태 B 실행 훅(미도입, DP-E3). | **Hook Binding 필수 필드**(08 §3.2-D — `hookId`/`event`/`phase`/`action` 필수·`order`/`replaceable` 기본값), Register 재사용 계약(08 §3.1-C·INV-4, 01 §3.1-A). |
| SP-2 | 이벤트 계측·방출 지점 (Claude Code 세션/턴 계측 → 대상 환경의 이벤트 방출 메커니즘) | §2 행 2, §3 | 세션/턴 계측 지점 매핑(lifecycle→loop-binding §3·agent→delegation §3·memory→memory-binding §3·runtime→runtime-binding §3), 호스트 관찰 방출 주체(형태 A). | **§3.2-A 이벤트 카탈로그 ID·명명 규칙**(18행 `<domain>.<name>`, domain ∈ {lifecycle,agent,runtime,memory}), 도출된 이벤트(INV-6), 방출 주체 계약 미고정(OQ-H2). |
| SP-3 | Hook Dispatch/실행기 (Claude Code 하네스의 hook 실행 → 대상 환경의 dispatch) | §2 행 3, §5.1 | 호스트(주 세션) 절차 구동 Dispatch, 하네스 native hook 실행(형태 B, 미도입). | **§3.1-D/E 순서·격리·비차단 계약**(3단 순서·격리 호출·완료 조건), Hook Dispatch 계약(Glossary J-08). |
| SP-4 | 순서·격리·비차단 실현 (하네스의 실행 모델 → 대상 환경의 실행 모델) | §2 행 3, §5.1·§5.3 | 호스트 절차의 결정적 정렬·격리 호출·Hook Failure Report(blocking=false) 실현, 실행 모델은 02 §4 정합. | **§3.1-D/E 순서·격리·비차단 계약**, **Hook Failure Report 형태**(§3.2-E 6필드·blocking 항상 false), Invariants INV-2·INV-5. |
| SP-5 | Event Record 직렬화·컨텍스트 전달 (하네스의 컨텍스트 투영 → 대상 환경의 전달 채널) | §2 행 4, §5.2 | Event Record 5필드 물리 표현(`sourceRef`/`contextView` 원천 참조·`occurredAt` 순서 값 L-09), 읽기 전용 투영 전달 채널. | **Event Record 형태**(§3.2-C 5필드), read-only(INV-3), `contextView` 스키마 원천 spec 소유(§8 조율). |

- **유지 열의 08 §4.2 유지 목록 전건 커버(대조).** 08 §4.2 "유지되는 것" 5항 — (a) §3.2-A 이벤트 카탈로그 ID·명명 규칙 = SP-2 유지 열, (b) Event Record 형태 = SP-5 유지 열, (c) Hook Binding 필수 필드 = SP-1 유지 열, (d) §3.1-D/E 순서·격리·비차단 계약 = SP-3·SP-4 유지 열, (e) §3.3 Invariants = 전 행(SP-1 INV-4·SP-2 INV-6·SP-3/SP-4 INV-2·INV-5·SP-5 INV-3 및 전건 관통 INV-1·INV-7·INV-8) — 5항 전건이 유지 열에 커버된다.
- **"유지되는 것" 열의 이식 불변성.** 위 계약(카탈로그 ID·명명 규칙·Event Record 형태·Hook Binding 필수 필드·순서/격리/비차단 계약·Invariants)은 다른 AI·환경으로 이식해도 바뀌지 않는다 — 08 §4.2 말미 "유지되는 것" 목록의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(08 §4.2 말미·runtime-binding.md §4·memory-binding.md §6·verifier-binding.md §6·loop-binding.md §6 동형). 본 문서는 그 정식화를 선취하지 않고 v0.8 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 7 — A5/L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록 — A5 재작업 사례: 미존재 소스를 "실재"로 서술한 것을 파일 시스템 전수 대조로 검출한 데서 도출)에 따라, 본 문서의 "실재/존재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`) + 파일 크기(`wc -c`) 직접 실측. `.claude/hooks/`·`.claude/settings.json` 상태는 `ls -la` 직접 실측. v0.9 T7 개정(관찰 1 해소)은 `.claude/hooks/`·`.claude/skills/` 행을 시연(PS-4) 후 상태로 `find`+`wc -c` 직접 재실측·갱신했다(L-07). `.claude/settings.json`은 여전히 미존재(DP-E3 유지).**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — runtime/memory/verifier/loop-binding.md·백엔드 디렉터리 존재 확인. |
| `framework/adapters/claude/runtime-binding.md` | 실재 (v0.3 Baseline, 자매 — runtime 계측 참조원) | 실재 (32,973 bytes). |
| `framework/adapters/claude/memory-binding.md` | 실재 (v0.4 Baseline, 자매 — memory 계측 참조원) | 실재 (51,144 bytes). |
| `framework/adapters/claude/verifier-binding.md` | 실재 (v0.5 Baseline, 자매 — 관례 표본) | 실재 (46,449 bytes). |
| `framework/adapters/claude/loop-binding.md` | 실재 (v0.7 Baseline, 자매 — lifecycle 계측 참조원) | 실재 (64,012 bytes). |
| `framework/adapters/claude/hooks-binding.md` | 실재 (본 문서 — 본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음. |
| `framework/adapters/claude/workflow-binding.md` | 실재 (기존 확장 트랙 자매, v0.7 — 내용 불인용) | 실재 (66,496 bytes). 존재만 실측; 본 문서 계측 참조원 아님(내용 불인용). |
| `.claude/hooks/` (등록 표면 디렉터리 + F-H1 — §2·§4.1) | **실재 — 시연 PS-4 생성 레퍼런스 Hook `audit-complete/`(F-H1) 실재** | **실재 — `.claude/hooks/audit-complete/`에 manifest.md(3,553 bytes)·audit.sh(1,052 bytes) 실재**(`find`+`wc -c` v0.9 T7 재실측). 등록 표면·레퍼런스 Hook 실물 모두 실재(생성 주체 = 시연 Task, L-07). |
| `.claude/settings.json` (§2 행 1·§4.3 DP-E3) | **미존재** (생성·수정 0 — DP-E3; 형태 B 실행 훅 선언 자리) | **미존재** — `ls` 결과 `No such file or directory`. 본 문서가 생성·수정하지 않음(DP-E3). |
| `.claude/commands/`·`.claude/skills/` (확장 표면 자매 — 참고) | 실재 (`.claude/skills/`는 시연 PS-4 생성 F-S1 실재 — 본 문서 소관 아님) | 실재 — `.claude/commands/`는 빈 디렉터리, `.claude/skills/commit-message-writer/SKILL.md`(F-S1, 2,723 bytes) 실재(v0.9 T7 재실측). 본 문서는 수정하지 않음. |
| `.claude/agents/` 4파일 (역할 진입점 — agent 계측 관련 참조) | 실재 (advisor/planner/verifier/worker.md) | 실재 — 4파일: advisor.md(7,152)·planner.md(9,232)·verifier.md(11,357)·worker.md(7,134). 무수정. |
| `framework/adapters/claude/loop-data/` (lifecycle 계측 산출물 근거) | 실재 (loop-binding.md §7 실측 대상 — 전이 이벤트 기록) | 실재 — loop-binding.md §7이 실측한 백엔드 디렉터리 존재 확인. 본 문서는 참조만(무수정). |
| `framework/adapters/claude/memory-data/` (memory 계측 산출물 근거) | 실재 (memory-binding.md §7 실측 대상 — Record/Recall 백엔드) | 실재 — `memory-data/` 존재 확인. 본 문서는 참조만(무수정). |
| `specs/08-hooks.md` (정본) | 실재 (Frozen 정본) | 실재 (28,469 bytes). |
| Hook 실행 메커니즘·방출 계측 실행 코드 (형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). `.claude/settings.json` 실행 훅·실행 계측 코드 부재. |

- **핵심 구분.** 본 문서가 확정한 Hook Module 자기완결 경계 구조·Hook Binding 6필드 직렬화 표기·Dispatch 물리 절차·Event Record 5필드 물리 표현은 **정본**이며, 그 구조대로의 **레퍼런스 Hook Module 실물은 시연 PS-4(EX-DH)가 생성해 실재**한다(`.claude/hooks/audit-complete/`, F-H1 — v0.9 T7 재실측). 이는 memory-binding.md가 M5 draft 시점 "데이터 미생성"을 M7 시연 후 실재로 전환한 정직 구분(memory-binding.md §7 r2)과 동형이다 — 본 문서는 구조·형식·표기의 정본만 소유하고, 실물 생성은 시연 Task 소관이다(생성 주체 구분, L-07).
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다(v0.9 T7 개정은 `.claude/hooks/`·`.claude/skills/` 행을 시연 후 상태로 직접 재실측). 실측과 불일치하는 서술은 0건이다 — 미존재(`.claude/settings.json` — DP-E3 유지)를 실재로, 실재(등록 표면 디렉터리·시연 후 F-H1 실물)를 미존재로 쓰지 않았다(A5/L-07 재발 방지). 순서 값·시각 서술은 L-09 준수(§5.2 `occurredAt` 순서 값, 시각 주장은 실측 후에만).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 5).** 본 문서의 모든 매핑은 08 §3·§4의 물리 실현이다. 어떤 연산·데이터 계약·불변 규칙·카탈로그 Event ID·필드도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 정본 §(08 §3·§4)다. 계약 요소는 전부 `08 §…`(및 01 §·02 §·04 §·Glossary §3.2-J) 포인터로만 인용했다. **새 Event 0·새 domain 0·새 phase 0·새 Hook Binding 필드 0·새 Event Record 필드 0·새 Hook Failure Report reason 0·새 불변 규칙 0**(08 §3.2-B 확장 규칙·§3.3 준수). 08 §4.1 표 5행을 넘어서는 새 바인딩 계약을 창설하지 않았다.
- **계약 소유 명시.** 이벤트 카탈로그 18행·명명 규칙·확장 규칙 = 08 §3.2-A/B; Hook 정의·능력·경계 = 08 §3.1-B; 등록 완료 조건·reason = 08 §3.1-C(Module reason은 01 §3.1-A); Dispatch·순서 = 08 §3.1-D; 실패 처리·격리 = 08 §3.1-E; Event Record 5필드 = 08 §3.2-C; Hook Binding 6필드 = 08 §3.2-D; Hook Failure Report 6필드 = 08 §3.2-E; Invariants INV-1~8 = 08 §3.3; Module Manifest·Register = 01 §3.2-A·§3.1-A. 계측 지점 물리 실현 = loop-binding.md(lifecycle)·delegation-protocol.md(agent)·memory-binding.md(memory)·runtime-binding.md(runtime). 본 문서는 이들의 **물리 실현**(직렬화 형식·자기완결 경계 구조·계측 지점 매핑·Dispatch 물리 절차·Event Record 물리 표현·등록 물리 절차)만 확정한다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형식(Markdown + front-matter)·물리 경로(`.claude/hooks/…`·`framework/adapters/claude/…`)·파일 확장자·세션/턴·서브에이전트 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. 08 §3(Core Contract, AI 비의존 — INV-8)은 이 토큰을 본문에 두지 않으며, 08 §4가 "구체 실현은 Adapter Binding 소관" 포인터로 미뤘고 본 문서가 그 소관자다(structure.md §5 C-3 확장은 이 경계에 비적용 — 격리 보유, runtime-binding.md §5·memory-binding.md §8·verifier-binding.md §8·loop-binding.md §8 동형).
- **동시 작성 문서 경계(07 R2) 및 생성 주체 구분(L-07).** 같은 병렬 집합(PS-1)에서 동시 작성 중인 형제 산출물(skills-binding·framework/plugins/ 문서·시연 절차서)의 내용을 인용·추측하지 않았다(07 R2 준수 — memory-binding.md가 동시 작성 demo-procedure를 불인용한 선례 동형). Skills·Plugins는 Hooks와 상호 독립 서브시스템이며(08 §2 Non-Goals·§9), 겹치는 계약을 가정하지 않았다. 레퍼런스 Hook Module 실물의 실재를 작성 당시 주장하지 않고 생성 주체를 시연 Task로 구분했다(L-07) — 실물은 시연 PS-4(EX-DH)가 생성해 현재 실재한다(§7). 참조한 확정 정본·Baseline은 08(정본)·01·02·04(§ 포인터)·자매 Adapter Binding 4문서(runtime/memory/verifier/loop-binding.md, Baseline)·delegation-protocol.md·framework/core/structure.md·specs/00-glossary.md뿐이다. workflow-binding.md는 존재만 실측하고 내용을 인용하지 않았다(§7).
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 이 1개 파일(`framework/adapters/claude/hooks-binding.md`)만 생성하며, `.claude/hooks/` 실물·`.claude/settings.json`(DP-E3)·`.claude/` 하위 기타·자매 Baseline 산출물·framework/core/·specs/·docs/를 수정·생성하지 않는다. 레퍼런스 Hook 실물·픽스처·시연 산출물도 생성하지 않는다(후속 시연 Task 소관, L-07).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-EH1 (`contextView` 투영 스키마 원천 조율 — 비차단).** Event Record `contextView`(08 §3.2-C)의 상세 투영 스키마는 각 원천 spec(03 lifecycle·02 agent·04 memory·01 runtime) 소유이며(08 §3.2-C·§9 03/04 조율), 본 문서는 읽기 전용 전달 채널만 바인딩하고 투영 내용 스키마를 확정하지 않았다(추측 금지, 07 R2·R3). 형태 B 실행 계측 도입 시 각 원천이 노출할 `contextView` 스키마의 확정 정합이 필요하다. 계약(08 §3.2-C 필드) 변경이 아니므로 비차단이다.
- **OQ-EH2 (Hook Module 구조 = Worker 제안, Advisor 채택 대상 — 비차단).** DP-E3는 settings.json 미생성·`.claude/hooks/` 표면 사용을 확정했으나, 그 하위 자기완결 경계 구조(`.claude/hooks/<hookModuleId>/` 디렉터리 형 + `manifest.md`에 Manifest+Hook Binding 병치 / 순수 observer는 단일 `.md` 축약형)는 본 문서 §4.1의 **Worker 제안**이다(근거: 01 §3.2-E 자기완결·runtime-binding.md §3.1 Markdown+front-matter·`.claude/agents/*.md` 단일 파일 Module 동형). 대안(전역 hooks 선언 1파일 등)도 계약(08 §3.2-D·§3.1-C)을 위반하지 않는다. 하위 구조 채택 여부는 Advisor 채택 대상이며, 후속 시연 Task가 이 정본 구조대로 레퍼런스 Hook을 생성할 예정이다. 계약 변경이 아니므로 비차단이다.
- **OQ-EH3 (형태 B 경계 분할·실행 훅 결선 — 비차단).** Hook 실행 메커니즘(형태 B — settings.json 실행 훅 또는 실행 코드)이 하네스 native hook 메커니즘과 `framework/adapters/claude/` 사이 어디에 결선·분할되는지는 형태 B 설계 시 확정 대상이다(§4.3·§5.1, structure.md §4 규칙 4 defer — verifier-binding.md OQ-VB-2·loop-binding.md OQ-LB-2 동형). Bootstrap(형태 A)에서는 호스트 절차 구동이므로 이 분할이 필요하지 않으며, 계약(08 §3.1-D/E) 변경이 아니므로 비차단이다.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 확장 시스템 첫 바인딩 산출물(선행 자매: runtime·memory·verifier·loop-binding.md). 08 §4.1(Hooks 바인딩 표 5행)의 **v0.8 물리 실현 매핑**. 정본 = 08 §3·§4(본 문서는 물리 실현, 재정의 아님 — §0). Hooks는 별도 Module 구현 디렉터리를 두지 않고 Runtime의 Module 등록 계약(01 §3.1-A)을 확장점으로 재사용한다(08 INV-4).
- **§2:** 08 §4.1 표 **5행 전부**를 물리 표면으로 매핑("정본 인용" 열 + "물리 실현" 열 + "실재 여부" 열, 물리 실재/형태 A/형태 B 정직 구분). 등록 표면 `.claude/hooks/` 실재(시연 PS-4 생성 F-H1 `audit-complete/` 실재); 정의·Dispatch 수행 = 규약 실현(형태 A); 하네스 native hook 실행·settings.json 실행 훅 = 형태 B(미도입, DP-E3 — `.claude/settings.json` 미존재).
- **§3 (OQ-4 해소):** 이벤트 카탈로그 **18행 전건** 계측 지점 매핑 — lifecycle 7행 → loop-binding.md §3(전이 이벤트 기록)·agent 3행 → delegation-protocol.md §3(위임/보고)·memory 2행 → memory-binding.md §3.1/§3.2(Record/Recall)는 **형태 A 실계측 가능**, runtime 6행 → runtime-binding.md §3.2~§3.4(연산 규약 지점)는 **규약 지점 매핑 실재·실행 계측 형태 B**. 시연 소비 예정 `lifecycle.complete` @ after = 형태 A 실계측 가능. 방출 주체(형태 A) = 호스트 관찰(OQ-H2 §4 소관). 재정의 0·새 Event 0.
- **§4 (DP-E3):** Hook Module 직렬화·등록 — `.claude/hooks/<hookModuleId>/` 자기완결 경계(Markdown+front-matter), Hook Binding 6필드(§3.2-D) 직렬화 표기(필수 표기 보존), 등록 = 01 §3.1-A Register 바인딩 경유(형태 A, runtime-binding.md §3.2 동형). **`.claude/settings.json` 생성·수정 0**, 08 §4.1 행 1 "settings.json hooks 선언" = 형태 A(표면 정의 실재)/형태 B(실행 훅 — 미도입) 정직 구분. `entrypoint` 물리 해소·Memory 접근 단일 Port(§4.4).
- **§5:** Hook Dispatch 물리 절차(예/아니오 판정 가능) — 형태 A 호스트(주 세션) 절차 5단계, 08 §3.1-D 3단 순서(order 오름차순 → 등록 순서 → hookId 사전순, 문면 보존), 격리·비차단(INV-2 blocking 항상 false), Event Record 5필드(§3.2-C) 읽기 전용 전달(INV-3, `occurredAt` 순서 값 L-09), Hook Failure Report 6필드(§3.2-E) 직렬화.
- **§6:** 08 §4.2 이식 교체 지점 SP-1~5 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 08 §4.2 유지 목록 5항(카탈로그 ID·명명 규칙·Event Record 형태·Hook Binding 필수 필드·순서/격리/비차단 계약·Invariants)을 전건 커버·이식 불변(C-1) 재확인.
- **§7:** 실측 대조(2026-07-06 직접 실측; v0.9 T7 개정은 관찰 1 대상 행 시연 후 재실측) — 자매 바인딩 4문서·`.claude/agents/` 4종·loop-data/·memory-data/·specs/08-hooks.md 실재; **`.claude/hooks/audit-complete/`(F-H1) 시연 PS-4 생성 실재**; **`.claude/settings.json` 미존재(DP-E3 — 생성·수정 0, 불변)**; native hook 실행 메커니즘 미도입(형태 B). 실측 불일치 0건(A5/L-07 재발 방지, L-09 시각 구분).
- 08 §3·01 §3 계약 재정의 0, Glossary 밖 새 용어 0, 새 Event·필드·reason 신설 0, 새 바인딩 계약 창설 0. 구체 AI·환경·형식 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 동시 작성 형제 산출물(skills-binding·framework/plugins/·시연 절차서) 불인용(07 R2); 레퍼런스 Hook 실물은 시연 Task(PS-4)가 생성 완료(L-07·생성 주체 구분; v0.9 T7 개정이 시연 후 상태 반영). EX-H1 최초 작성은 이 1파일만 생성.
