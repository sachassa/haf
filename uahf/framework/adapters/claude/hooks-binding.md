# framework/adapters/claude/hooks-binding — Claude Code Hooks Adapter 바인딩

작성일: 2026-07-06
상태: v0.9 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06). 이후 개정 이력·시점·경위 = §9.
상위 규약: AGENT.md
근거 정본:

- specs/08-hooks.md §3(§3.1 연산 · §3.2-A Event Catalog 18행 · §3.2-B 명명·확장 규칙 · §3.2-C Event Record · §3.2-D Hook Binding 6필드 · §3.2-E Hook Failure Report · §3.3 INV-1~8)·§4.1 Binding 표(5행)·§4.2 SP-1~5·§9 결정 기록(OQ-H1·OQ-H2·OQ-H3) — 본 문서가 물리 실현으로 인스턴스화·대조하는 정본. § 포인터 인용만.
- specs/01-runtime.md §3.1-A(Register/Resolve/Replace/Deregister)·§3.2-A(Module Manifest 7필드)·§4.1(확장 Module 표면 `.claude/hooks/`) — Hook 등록·Module 직렬화의 원천 계약. § 포인터로만 참조.
- specs/00-glossary.md §3.2-J J-08 — Event·Event Catalog·Phase·Hook Binding·Hook Dispatch 표제어. 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- 계측 지점 참조원(재정의 0) — loop-binding.md §3(lifecycle 전이 이벤트 기록)·docs/delegation-protocol.md §3(agent 위임·보고)·memory-binding.md §3.1/§3.2(memory Record/Recall)·runtime-binding.md §3.2~§3.4(runtime 연산·Config·Bootstrap/Shutdown). 관례 표본 = loop-binding.md·verifier-binding.md.
- framework/core/structure.md §2·§4·§5 — 4경계 배치·소유 계약 / 계약·문서 전용 경계와 실행 코드 배치 규칙(형태 A/B 라벨) / C-3 금지 토큰 규칙. 본 문서 경계의 근거.
- ROADMAP.md v0.8 (Extension System) — Hooks 완료 조건과 산출물(본체 수정 0 확장·비차단·순서 결정성·카탈로그 도출·경계·AI 비의존)의 환경 실현 근거.

거버넌스·경계(공통): 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다 — Adapter 경계는 구체 AI·환경·직렬화 형식·물리 경로 토큰이 **허용**되는 격리 지점이고(structure.md §5 C-3 비적용·§2 4경계·§4 형태 A/B 라벨, 08 INV-8, 01 §3.2-E 규칙 3), 이 하네스는 Bootstrap 상태이므로 계약 실현을 형태 A(문서·규약)/형태 B(실행 코드)로 정직 구분하며, 용어는 specs/00-glossary.md 정본만 쓰고 Core Contract(08 §3)를 재정의하지 않는다. 개정은 Advisor 승인 + §9 이력 append로만 이뤄진다.

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
| 2026-07-19 | (상태 유지 — 운영 훅 경계 명문화) | 운영 훅(Operational Harness Hooks) 경계 **§4.5 신설** — 하네스 네이티브 훅(`.claude/settings.json`의 `SessionStart`·`PreToolUse` 등 세션 수명·tool-use 이벤트에 결선되는 훅)은 08 §3.2-A 카탈로그(18종) 밖 **운영 훅**으로, 정본 Hooks Component 계약(특히 INV-2 비차단·blocking 항상 false)의 **적용 대상이 아니며 차단(blocking)이 가능**함을 판별 기준·INV-2 미저촉 근거·선례(기존 `SessionStart` 운영 훅 completeness-reminder·memory-guard)와 함께 명문화. 설계 완성도 강제 트랙(§DC-1)의 PreToolUse 차단 훅 백스톱이 이 범주에 속하며 1차 강제는 이식 가능한 엔진 게이트(resolve_gate.py fail-closed)임을 명시. **DP-E3 서술 stale 정정** — `.claude/settings.json`이 이제 하네스 운영 훅(`SessionStart` 2건 + `PreToolUse` 운영 백스톱 1건 → pretooluse_design_guard.py)을 호스팅하며 **실재**하되 Hooks Component 형태 B(08 §3.2-A 카탈로그 이벤트 자동 결선) 실행 훅 선언은 **여전히 미도입**임을 정직 구분(2026-07-19 직접 재실측). "settings.json 미존재"·"SessionStart만" 서술을 문서 전체에서 전수 스윕해 갱신(§0·§2 등록 표면 트리·§2 표 행 1·§4.3·§5.1·§6 SP-1·§7 실측 표·§7 개요·§7 주·§10 §2/§4/§7 요약). **PreToolUse 운영 백스톱 배선·라이브 실증 실측 반영**(§7·§4.5·§10) — 경쟁 조건으로 Wave 1이 최초 실측 후 PreToolUse 훅을 배선; matcher `Write\|Edit\|MultiEdit` → `pretooluse_design_guard.py`(timeout 15)로 결선됐고 메인/서브에이전트 Write가 둘 다 deny(`[DESIGN-INCOMPLETE]` 사유) 차단으로 발화 확증(Advisor 직접 검증, L-07). §DC 백스톱 라벨 정밀화 — §DC-1 트랙 내 §DC-3(강제 시점·메커니즘 = 백스톱=차단형 훅). **spec 08(`uahf/specs/08-hooks.md`) 무수정**(Frozen — § 포인터 인용만), 08 §3 계약 요소(카탈로그 Event ID·필드·Invariants) **재정의·신설 0**, Glossary 밖 새 용어 0("운영 훅"은 서술 라벨). 기존 이력 행(v0.8·v0.9·2026-07-17) 문면 불변(append-only, L-10). | Worker (Advisor 위임) |
| 2026-07-26 | (정합) | md 슬림화 Wave 2 — 비계약 격리 개정: 재서술·감사 서술·죽은 참조 압축, 계약 문면 무변경. 종전 문면 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/08-hooks.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며 계약 요소(연산·데이터 포맷·불변 규칙·카탈로그 Event ID·필드)를 **재정의·확장하지 않는다** — § 포인터로만 인용한다. Hooks는 별도 Module 구현 디렉터리를 두지 않고 Runtime의 Module 등록 계약(01 §3.1-A)을 확장점으로 그대로 쓰며(08 §2·§3.1-C·INV-4), 08 §4가 Adapter Binding 소관으로 미룬 **직렬화 형식·파일 구조·저장 위치·계측 지점 물리 참조·Dispatch 물리 절차·action 진입점**이 확정되는 유일한 자리가 여기다.
- **방출 주체 소관 확정(OQ-H2 — §4 소관).** 08 §9는 "이벤트 방출 주체는 §4 소관으로 확정. 계약 수준 고정 불필요"로 OQ-H2를 승인했고 본 문서가 그 소관자다 — 형태 A에서 방출 주체는 **호스트 오케스트레이션(주 세션)**이 원천 지점을 관찰하는 것이며(§3·§5), 형태 B에서는 원천 직접 방출 또는 공용 dispatch 관찰이다. 계약(08 §3)은 관찰 가능한 표면만 고정하고 방출 주체를 고정하지 않으므로 이 매핑은 계약 창설이 아니다.
- **창설 금지.** 08 §4.1 표를 넘어서는 새 바인딩 계약을 창설하지 않는다 — 새 Event·새 domain·새 phase·새 Hook Binding 필드·새 Hook Failure Report reason·새 불변 규칙 0(08 §3.2-B·§3.3 준수).
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다 — 대상·결과는 §7.

---

## §1. 목적

이 문서는 08 §4.1(Hooks Claude Code Binding)을 이 환경 위에 구체 물리 실현으로 매핑한다. 책임 5가지 = 바인딩 표 5행 전건의 물리 표면 확정·실재 여부 정직 구분(§2) · 이벤트 카탈로그 18행 전건의 계측 지점 매핑(§3, OQ-4 해소) · Hook Module 직렬화·등록 물리 절차(§4 — DP-E3·운영 훅 경계 §4.5) · Hook Dispatch 물리 절차의 예/아니오 판정 가능한 확정(§5) · SP-1~5 대응(§6)과 상태 서술 실측 대조(§7).

08 §3의 어떤 계약 요소도 재정의·확장하지 않는다(§0·§8, done 5). 형태 A → 형태 B 전환 시에도 Core Contract(08 §3) 변경은 0이며(structure.md §7 C-1), §6의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 08 §4.1 바인딩 표 5행 물리 실현 (done 1·7)

08 §4.1 Claude Code Binding 표의 **5행 전부**를 물리 표면으로 매핑한다. "정본 인용(원문 그대로)" 열 = 08 §4.1 문면의 문자 그대로 인용(Frozen 정본 대조 앵커), "물리 실현" 열 = 본 문서가 확정하는 경로·구조·형식·채널·절차, "실재 여부" 열 = 물리 실재 / 규약 실현(형태 A) / 형태 B 예정의 정직 구분(§7, L-07).

등록 표면 디렉터리 구조(본 문서 정본 — 08 §4.1 행 1·5 물리 실현):

```
.claude/
├─ hooks/                       # Hook Module 등록 표면 (확장 Module 표면 — 01 §4.1·runtime-binding.md §2 #3; 시연 PS-4가 생성한 audit-complete/(F-H1) 실재)
│  └─ <hookModuleId>/           #   Hook Module 자기완결 경계 (01 §3.2-E 규칙 2; 예: audit-complete/(F-H1) — 시연 PS-4 생성 실재, §4·§7)
│     ├─ manifest.md            #     Module Manifest(01 §3.2-A 7필드) + Hook Binding 선언(§3.2-D 6필드) — Markdown + front-matter
│     └─ <action>               #     Hook action 진입점 (스크립트·명령 — 08 §4.1 행 5)
├─ agents/                      # 실재 — 역할 진입점 4파일(자매 참조, §7 실측)
└─ settings.json                # 실재 — 하네스 운영 훅(SessionStart 2건 + PreToolUse 2건) 호스팅; 본 문서 생성·수정 0 (DP-E3). Component 형태 B 실행 훅(카탈로그 이벤트 자동 결선)은 미도입 (운영 훅 경계 = §4.5·§7)
```

| # | §3 계약 요소 | 정본 인용(원문 그대로) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Hook Module 정의·직렬화 (§3.2-D) | `.claude/hooks/` 하위 정의와 `.claude/settings.json`의 hooks 선언. Manifest 직렬화는 01 §4.1(Markdown + front-matter / 설정 파일)을 따른다. | Hook Module = `.claude/hooks/<hookModuleId>/` 자기완결 경계(01 §3.2-E 규칙 2) 안에 Module Manifest(01 §3.2-A 7필드, Markdown + front-matter)와 Hook Binding 선언(§3.2-D 6필드)을 둔다 — 구조·직렬화 표기 정본 = §4. settings.json의 hooks 선언은 형태 A(표면 정의)/Component 형태 B(카탈로그 이벤트 자동 결선 — 미도입) 정직 구분(DP-E3 §4.3); 운영 훅은 별개 층위(§4.5). | 등록 표면 `.claude/hooks/`·레퍼런스 Hook `audit-complete/`(F-H1) 실재(§7). 6필드 직렬화 표기 확정(§4). settings.json은 실재하며 운영 훅 호스팅, Component 형태 B는 미도입(§4.5·§7). |
| 2 | Event 방출·계측 지점 (§3.2-A) | Claude Code 세션/턴에서 이벤트 원천(lifecycle 전이, runtime 연산, agent 메시지, memory Port 접근)이 발생하는 지점의 계측. | 각 Event의 계측 지점을 자매 바인딩의 확정 물리 지점에 매핑한다(lifecycle→loop-binding §3 · agent→delegation-protocol §3 · memory→memory-binding §3.1/§3.2 · runtime→runtime-binding §3.2~§3.4). 방출 주체(형태 A) = 호스트 관찰(OQ-H2). 매핑 정본 = §3. | 형태 A 실계측 가능(lifecycle·agent·memory) / 규약 지점 매핑 실재·실행 계측 형태 B(runtime). 무인 자동 방출 계측은 미도입(§3). |
| 3 | Hook Dispatch·순서·격리 (§3.1-D/E) | Claude Code 하네스의 hook 실행 메커니즘이 결정적 순서와 격리 실행을 실현한다. | Bootstrap(형태 A)에서 Dispatch는 **호스트(주 세션 오케스트레이션)** 절차로 구동된다 — 08 §3.1-D 3단 순서로 정렬해 격리 호출하고, 실패는 Hook Failure Report(§3.2-E, blocking=false)로 남기고 계속한다(INV-2). 하네스 native hook 실행은 형태 B. 물리 절차 정본 = §5. | 호스트 절차 구동 규약 실현(형태 A). 하네스 native hook 실행 메커니즘(형태 B)은 미도입(DP-E3). |
| 4 | Event Record 직렬화 (§3.2-C) | 하네스가 원천 컨텍스트를 읽기 전용으로 Hook action에 전달하는 형태. | Dispatch가 원천 지점(§3)에서 읽기 전용 투영을 구성해 Event Record 5필드(§3.2-C: `eventId`/`phase`/`sourceRef`/`contextView`/`occurredAt`)를 action에 전달한다 — `contextView` 스키마는 원천 spec 소유, `occurredAt`은 순서 값(L-09). Hook은 읽기만 한다(INV-3). 물리 표현 = §5.2. | 읽기 전용 전달 규약 실현(형태 A). 하네스 컨텍스트 투영 채널 코드(형태 B)는 미도입. |
| 5 | Hook action 진입점 (§3.2-D `action`) | `.claude/hooks/` 스크립트·명령 진입점. 실행 모델 지정은 02 §4 실행 모델 바인딩과 정합한다. | Hook Binding `action`(§3.2-D) = `.claude/hooks/<hookModuleId>/` 경계 안의 스크립트·명령 진입점(§4.1). `entrypoint` 물리 해소 = §4.4. 실행 모델 지정은 02 §4 소관 — 참조만 한다(정본 문면 보존). | 진입점 구조 확정(정본, §4). 레퍼런스 action 실물 `audit-complete/audit.sh`(F-H1)는 시연 PS-4 생성으로 실재(§7). 실행 모델 = 02 §4 소관. |

주:

- 위 5행은 08 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 정본 표현을 이 환경의 구체 경로·형식·채널로 좁힌 것이며 새 바인딩 계약을 창설하지 않는다(§0). 등록 표면 디렉터리·계측/Dispatch/Event Record 참조원은 물리 실재이고, 정의·Dispatch **수행**은 Bootstrap에서 규약 실현(형태 A — 호스트 관찰·호스트 절차 구동)이며, 하네스 native hook 실행 메커니즘·무인 방출 계측은 형태 B다(DP-E3).
- **Hooks = Runtime Module 등록 재사용(INV-4).** Hook 등록은 별도 메커니즘이 아니라 01 §3.1-A Register를 그대로 사용하므로(08 §3.1-C·INV-4) 등록·해소·교체가 runtime-binding.md §3.2와 동형으로 실현된다(§4.3). Hook은 등록만 되고 원천 이벤트 발생 시 호스트 Dispatch가 호출한다(§5) — 서브에이전트로 디스패치되는 Agent Module·단일 Port로 소비되는 Cross-cutting Service와 구별되는 세 번째 실현 방식이다.

---

## §3. 이벤트 카탈로그 18행 계측 지점 매핑 (done 2 — OQ-4 해소)

08 §4.1 행 2("Event 방출·계측 지점 (§3.2-A)")의 물리 실현이다. 08 §3.2-A 이벤트 카탈로그 **18행 전건**의 계측 지점을 자매 바인딩이 확정한 물리 지점에 매핑한다. **Event ID·domain·원천 계약·phase 계약의 정본은 08 §3.2-A이며, 본 절은 각 Event의 계측 지점(물리 참조원)과 실재 여부(형태)만 확정한다**(재정의 0, 새 Event 0).

방출 경계 정합은 08 §9 결정 기록이 이미 확인했다(lifecycle ↔ 03 §3.2-A 전이 이벤트 기록 시점, memory ↔ 04 §3.1 Record/Recall — 모순 없음). 각 계측 지점 참조원의 물리 실현은 그 자매 문서가 소유하며 본 문서는 참조만 한다(재정의 0).

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
- **방출 주체(형태 A) = 호스트 관찰(OQ-H2 §0).** 방출은 원천이 직접 방출하는 실행 코드가 아니라 **호스트 오케스트레이션(주 세션)이 원천 지점을 관찰**해 Event Record를 구성하고 Dispatch를 구동하는 것으로 실현되며(§5), 형태 B(원천 직접 방출 또는 공용 dispatch 관찰)로 전환해도 관찰 가능한 표면(카탈로그·Event Record·순서·격리)은 불변이다(INV-1·§6).
- **경계 불가침(INV-7).** 계측은 관찰이며 원천 연산·전이·메시지·Port 접근을 변경하지 않는다(INV-1·INV-3). memory 도메인 Event의 관찰이 Memory 접근은 아니다(08 §5) — Hook action이 Memory에 기록·회수하려면 단일 Port(memory-service.md §7)만 경유한다(INV-7, §4.4). lifecycle.verify Event의 관찰이 Verify 판정을 대체·무효화하지 않는다(INV-7).

---

## §4. Hook Module 직렬화·등록 물리 절차 (done 3)

08 §4.1 행 1("Hook Module 정의·직렬화")·행 5("Hook action 진입점")의 물리 실현을 확정한다. 계약 요소(Hook Binding 6필드·의미·필수 표기, Module Manifest 7필드, Register 완료 조건·reason)의 정본은 08 §3.2-D·§3.1-C·01 §3.2-A·§3.1-A이며, 본 절은 그 물리 실현만 확정한다(재정의 0).

### §4.1 Hook Module 자기완결 경계 구조 (08 §4.1 행 1·5)

- **물리 위치·구조(정본).** Hook Module은 확장 Module 등록 표면 `.claude/hooks/`(01 §4.1·runtime-binding.md §2 #3, 실재 — §7) 아래 **자기완결 경계**(01 §3.2-E 규칙 2)로 배치한다: `.claude/hooks/<hookModuleId>/`. 그 경계 안에 한 Module의 요소(Manifest·Hook Binding 선언·action 진입점)를 모은다 — 한 Module의 요소가 여러 경계로 흩어지지 않는다.
  - `manifest.md` — Module Manifest(01 §3.2-A 7필드)를 Markdown 본문 + YAML front-matter로 직렬화한다(runtime-binding.md §3.1 직렬화 동형, 01 §4.1 "Markdown + front-matter"). Hook Binding 선언(§3.2-D 6필드)을 이 Module의 자기완결 경계 안에 둔다(08 §3.1-C — "자기완결적 경계 안에 Hook Binding 선언을 둔다"). 한 Module은 하나 이상의 Hook Binding을 담을 수 있다(08 §3.2-D).
  - `<action>` — Hook action 진입점(스크립트·명령, 08 §4.1 행 5). 순수 observer Hook(감사 로그 등, 08 §8 예1)이면 action이 간단해 Module을 단일 파일 `.claude/hooks/<hookModuleId>.md`로 두는 축약형도 허용된다(`.claude/agents/*.md` 단일 파일 Module 동형) — 이 경우 action은 그 파일 내 진입점 참조다.
- **직렬화 형식 = Adapter 선택.** Markdown + front-matter는 이 환경의 직렬화 선택이며(01 §4.1), 이식 시 대상 환경의 확장 정의 메커니즘으로 교체된다(SP-1, §6). 이 형식 선택은 계약(08 §3.2-D 필드·필수 표기)을 바꾸지 않는다.
- **레퍼런스 Hook 실물 = 시연 Task 생성(L-07).** 위 구조는 본 문서가 확정한 **정본 구조**이며, 그 구조대로의 실물(`audit-complete/` — F-H1)은 시연 PS-4(EX-DH)가 생성해 실재한다(§7). 본 문서는 구조·직렬화 표기의 정본만 소유한다.

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

- **[Advisor 결정 DP-E3] `.claude/settings.json` 생성·수정 0 — 형태 A/B 정직 구분.** 08 §4.1 행 1은 Hook Module 정의를 "`.claude/hooks/` 하위 정의와 `.claude/settings.json`의 hooks 선언"으로 바인딩한다. 이 두 표면을 다음과 같이 구분한다.
  - **형태 A (표면 정의 실재).** Hook Module의 정의·등록은 `.claude/hooks/` 등록 표면(실재 — §7 실측)에 자기완결 경계를 배치하는 것으로 실현된다(§4.1·이 절 Register 행).
  - **형태 B (Component 실행 훅 선언 — 미도입).** `.claude/settings.json`의 hooks 선언 메커니즘으로 **08 §3.2-A 카탈로그 이벤트를 실행 코드에 자동 결선**하는 것이 Hooks Component의 형태 B이며 **미도입**이다. settings.json은 실재하나 하네스 네이티브 운영 훅만 호스팅하며 이는 카탈로그 밖 **별개 층위**이므로(§4.5·§7), 운영 훅 실재가 Component 형태 B 도입을 뜻하지 않는다. **본 문서는 `.claude/settings.json`을 생성·수정하지 않는다**(DP-E3). 형태 B 도입 시에도 08 §3은 불변이며(structure.md §7 C-1) 본 절은 그 도입을 선취·추측하지 않는다.
- **형태 구분 명시.** Bootstrap에서 등록은 `.claude/hooks/` 정의 배치로 규약 실현(형태 A)되며, 실행 Registry·실행 훅 선언(형태 B) 도입 시에도 01 §3.1-A Register 계약·08 §3.1-C 완료 조건은 변경 0이다.

### §4.4 Manifest `entrypoint` 물리 해소 · Memory 접근 경로 (해당 시)

- **`entrypoint` 물리 해소(형태 A/B).** Module Manifest `entrypoint`(01 §3.2-A)는 형태 A에서 `.claude/hooks/<hookModuleId>/` 경계 안 action 진입점(§4.1)으로 규약 실현되고, 형태 B에서 Hook action을 노출·구동하는 실행 코드 로케이터로 해소된다. 경계 간 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer, OQ-EH3).
- **Hook action의 Memory 접근(INV-7).** Hooks Component 계약 자체는 Memory를 읽거나 쓰지 않는다(08 §5). Hook action이 Memory에 기록·회수한다면 경로는 **Memory Service Interface(단일 Port — memory-service.md §7)** 하나뿐이며 영속성 백엔드에 직접 접근하지 않는다(08 §5·INV-7). 물리 배선은 memory-binding.md 소관(재정의 0).

### §4.5 운영 훅(Operational Harness Hooks) — Component 바인딩과의 경계

하네스는 정본 Hooks Component(08 §3)와 **다른 층위**의 확장점을 네이티브로 제공한다. 본 절은 그 층위를 **운영 훅**으로 구분하고 어떤 훅이 08 Component 계약(특히 INV-2 비차단)의 적용 대상인지의 판별 기준을 명문화한다(§4.3 DP-E3의 연장 · spec 08 Frozen 무수정 · § 포인터 인용만).

- **정의(서술 라벨).** 하네스가 네이티브로 제공하는 실행 시점 확장점(`.claude/settings.json`의 `SessionStart`·`PreToolUse` 등 세션 수명·tool-use 이벤트에 결선되는 훅)을 **운영 훅(operational harness hook)**이라 부른다. 이는 환경이 제공하는 실행 시점 확장 메커니즘이며, Glossary §3.2-J 용어(Event·Hook Binding·Hook Dispatch 등)를 재정의·확장하지 않는 서술 라벨이다.

- **경계 기준(판별).** 어떤 훅이 08 §3.2-A 이벤트 카탈로그(18종 `<domain>.<name>` — lifecycle 7·agent 3·runtime 6·memory 2)의 (event, phase)에 바인딩되면 **Component 바인딩**이며 08 §3 계약(INV-2 비차단·INV-1 본체 불가침·INV-3 read-only·§3.1-D/E 순서·격리)이 적용된다(§2·§3·§5). 카탈로그에 **없는** 하네스 네이티브 이벤트(`SessionStart`·`PreToolUse` 등)에 결선되면 **운영 훅**이며 Component 계약의 적용 대상이 **아니다** — 특히 **INV-2(비차단·blocking 항상 false)가 적용되지 않으므로 차단(blocking)이 가능**하다. `SessionStart`·`PreToolUse`는 카탈로그 18행 어디에도 없다(§3 표 대조 — 카탈로그는 lifecycle/agent/runtime/memory 도메인만 포함하며 tool-use·세션 수명 도메인은 부재).

- **INV-2 미저촉.** INV-2(08 §3.3)의 적용 범위는 카탈로그 이벤트에 바인딩된 Hook이므로, 카탈로그 밖에 결선된 **차단형 운영 훅(예: PreToolUse Write 거부)이 존재해도 INV-2를 위반하지 않는다**. 08 §3.1-E·INV-2·§9 OQ-H1(v0.1 Hook = 비차단 observer 전용)은 Component에 대한 결정이므로 무수정이다(spec 08 Frozen).

- **선례.** `.claude/settings.json`의 `SessionStart` 운영 훅(completeness-reminder·memory-guard)이 이미 이 범주다(§7) — 운영 훅은 이 프레임워크에 이미 실재하는 층위다.

- **§DC-1 트랙 §DC-3 백스톱의 위치(배선·실증 완료).** 설계 완성도 강제 트랙의 **PreToolUse 차단 훅**(설계 산출물 부재 시 소비 프로젝트 `src/` Write 거부 — `orchestration/adapters/claude/pretooluse_design_guard.py`, 실재)은 **운영 훅 범주**이므로 Component 계약(INV-2 포함) 미적용이고 차단이 허용된다. **1차 방어**는 이식 가능한 엔진 게이트(`orchestration/adapters/claude/resolve_gate.py` fail-closed)이고 PreToolUse 운영 훅은 그 뒤의 **백스톱**이다. 배선·라이브 차단 실증은 완료 상태다(근거 = git 앵커 90ca19c).

  - **⚠ 규칙 — 훅 배선 경로는 상대경로로 쓴다. `$CLAUDE_PROJECT_DIR` 을 쓰지 않는다.** 이 환경의 PreToolUse 훅에서 변수형은 차단을 내지 못했다(A-B-A 대조 실측 — 근거 = git 앵커 90ca19c). **훅이 실패해도 도구 호출은 조용히 통과**하므로 배선이 죽어도 표면에 드러나지 않는다(침묵의 성공 해석 금지 — `.claude/AGENT.md` §Invariants) — 훅을 새로 배선하거나 경로를 옮길 때는 단위 검증이 아니라 **실제 도구 호출로 차단을 확인한다**. 현행 배선은 실측으로 차단이 확인된 상대경로로 확정한다. 이식 시 다른 환경은 자기 환경의 운영 훅 메커니즘으로 대응한다(이는 Component 계약의 SP가 아니라 환경별 운영 훅 실현이다). **미해소** — 2026-07-19 확증 기록과 2026-07-21 A-B-A 실측이 충돌하며 어느 쪽이 환경 변화/기록 오류인지 판정 대기다(경위 = git 앵커 `90ca19c`).

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
- **형태 B 구분.** 이 절차(카탈로그 이벤트 Dispatch)를 하네스 native hook 실행 메커니즘으로 실행 코드화하는 것이 Component 형태 B이며 미도입이다(DP-E3 — settings.json은 카탈로그 밖 운영 훅만 호스팅, §4.5). 형태 B 전환 시에도 08 §3.1-D/E 순서·격리·비차단 계약은 불변이다(§6 SP-3·SP-4).

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
- **`contextView` 스키마 소관 경계.** 투영의 상세 스키마는 각 원천 spec(03·02·04·01) 소유이며(08 §3.2-C), 미확정 스키마를 추측하지 않는다 — 본 문서는 읽기 전용 전달 채널만 확정하고, 확정 정합이 필요하면 조율로 에스컬레이션한다(OQ-EH1).

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

08 §4.2 이식 교체 지점 SP-1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인하며 08 §4.2 유지 목록을 전건 커버한다.

| # (08 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Hook 정의 위치·포맷 (`.claude/hooks/`, `.claude/settings.json` hooks → 대상 환경의 확장 정의 메커니즘) | §2 행 1·5, §4.1·§4.2·§4.3 | `.claude/hooks/<hookModuleId>/` 자기완결 경계, Markdown + front-matter 직렬화, Hook Binding 6필드 물리 표기, `.claude/settings.json`의 Component 형태 B 실행 훅(카탈로그 이벤트 자동 결선 — 미도입, DP-E3; settings.json은 하네스 운영 훅으로 실재하되 별개 층위 = §4.5). | **Hook Binding 필수 필드**(08 §3.2-D — `hookId`/`event`/`phase`/`action` 필수·`order`/`replaceable` 기본값), Register 재사용 계약(08 §3.1-C·INV-4, 01 §3.1-A). |
| SP-2 | 이벤트 계측·방출 지점 (Claude Code 세션/턴 계측 → 대상 환경의 이벤트 방출 메커니즘) | §2 행 2, §3 | 세션/턴 계측 지점 매핑(lifecycle→loop-binding §3·agent→delegation §3·memory→memory-binding §3·runtime→runtime-binding §3), 호스트 관찰 방출 주체(형태 A). | **§3.2-A 이벤트 카탈로그 ID·명명 규칙**(18행 `<domain>.<name>`, domain ∈ {lifecycle,agent,runtime,memory}), 도출된 이벤트(INV-6), 방출 주체 계약 미고정(OQ-H2). |
| SP-3 | Hook Dispatch/실행기 (Claude Code 하네스의 hook 실행 → 대상 환경의 dispatch) | §2 행 3, §5.1 | 호스트(주 세션) 절차 구동 Dispatch, 하네스 native hook 실행(형태 B, 미도입). | **§3.1-D/E 순서·격리·비차단 계약**(3단 순서·격리 호출·완료 조건), Hook Dispatch 계약(Glossary J-08). |
| SP-4 | 순서·격리·비차단 실현 (하네스의 실행 모델 → 대상 환경의 실행 모델) | §2 행 3, §5.1·§5.3 | 호스트 절차의 결정적 정렬·격리 호출·Hook Failure Report(blocking=false) 실현, 실행 모델은 02 §4 정합. | **§3.1-D/E 순서·격리·비차단 계약**, **Hook Failure Report 형태**(§3.2-E 6필드·blocking 항상 false), Invariants INV-2·INV-5. |
| SP-5 | Event Record 직렬화·컨텍스트 전달 (하네스의 컨텍스트 투영 → 대상 환경의 전달 채널) | §2 행 4, §5.2 | Event Record 5필드 물리 표현(`sourceRef`/`contextView` 원천 참조·`occurredAt` 순서 값 L-09), 읽기 전용 투영 전달 채널. | **Event Record 형태**(§3.2-C 5필드), read-only(INV-3), `contextView` 스키마 원천 spec 소유(§8 조율). |

- **유지 열의 08 §4.2 유지 목록 5항 전건 커버(대조).** (a) 카탈로그 ID·명명 규칙 = SP-2, (b) Event Record 형태 = SP-5, (c) Hook Binding 필수 필드 = SP-1, (d) §3.1-D/E 순서·격리·비차단 계약 = SP-3·SP-4, (e) §3.3 Invariants = 전 행(SP-1 INV-4·SP-2 INV-6·SP-3/4 INV-2·INV-5·SP-5 INV-3, 관통 INV-1·INV-7·INV-8). `uaf-verified: 08 §4.2 유지 목록 5항을 위 표 "유지되는 것" 열과 1:1 대조 — 스윕 범위 = 본 절 SP-1~5 5행`
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(08 §4.2 말미). 본 문서는 그 정식화를 선취하지 않고 물리 실현 매핑에 한정한다(§0 창설 금지).

---

## §7. 상태 서술 실측 대조 (done 7 — A5/L-07 재발 방지)

L-07(상태 서술은 실측 후 기록 — A5 재발 방지)에 따라 본 문서의 "실재/존재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **자매 문서의 byte 스냅샷은 기록하지 않는다** — 날짜 박힌 크기 값은 stale해지므로 불변 주장(구조·1:1 대응·실재 여부)만 남긴다. 개정 시점·경위는 §9.

| 대상 | 본 문서 서술 | 실측 대조 결과 (불변 주장) |
|---|---|---|
| 자매 바인딩 4문서 (runtime·memory·verifier·loop-binding.md) | 실재 (Baseline — 계측 지점 참조원 + 관례 표본) | 실재 — 4문서 모두 존재. §3 매핑 표의 계측 지점 참조원과 1:1 대응. |
| `.claude/hooks/` (등록 표면 디렉터리 + F-H1 — §2·§4.1) | **실재 — 시연 PS-4 생성 레퍼런스 Hook `audit-complete/`(F-H1) 실재** | **실재 — `.claude/hooks/audit-complete/`에 manifest.md·audit.sh 실재.** 등록 표면·레퍼런스 Hook 실물 모두 실재(생성 주체 = 시연 Task, L-07). |
| `.claude/settings.json` (§2 행 1·§4.3 DP-E3·§4.5) | **실재** — 하네스 네이티브 운영 훅(`SessionStart`·`PreToolUse`) 호스팅; 본 문서 생성·수정 0(DP-E3). Component 형태 B 실행 훅은 미도입 | **실재** — `hooks.SessionStart`(matcher `startup\|resume\|clear`)에 운영 훅 2건(`completeness-reminder.txt`·`memory-guard.sh`), `hooks.PreToolUse`(matcher `Write\|Edit\|MultiEdit`)에 운영 훅 2건(`pretooluse_design_guard.py` 설계완성도 백스톱 · `binary_state_guard.py` 이진 원칙 가드) = 운영 훅 4건. 모두 08 §3.2-A 카탈로그 밖 하네스 네이티브 이벤트 결선(§4.5). 카탈로그 이벤트 자동 결선(Component 형태 B)은 부재. 본 문서는 생성·수정하지 않음. `uaf-verified: .claude/settings.json 직접 정독 — 스윕 범위 = 이 파일의 hooks 선언 전건` |
| `.claude/agents/` 4파일 (역할 진입점 — agent 계측 관련 참조) | 실재 (advisor/planner/verifier/worker.md) | 실재 — 4파일 모두 존재. 무수정. |
| `loop-data/`·`memory-data/` (lifecycle·memory 계측 산출물 근거) | 실재 (loop-binding.md §7·memory-binding.md §7 실측 대상) | 실재 — 백엔드 디렉터리 존재 확인. 본 문서는 참조만(무수정). |
| `specs/08-hooks.md` (정본) | 실재 (Frozen 정본) | 실재. |
| Hook 실행 메커니즘·방출 계측 실행 코드 (Component 형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). settings.json은 운영 훅만 호스팅하며 **카탈로그 이벤트 자동 결선·per-연산 방출 계측 실행 코드는 부재**(§4.5). |

- **핵심 구분.** 본 문서가 확정한 Hook Module 자기완결 경계 구조·Hook Binding 6필드 직렬화 표기·Dispatch 물리 절차·Event Record 5필드 물리 표현은 **정본**이며, 그 구조대로의 레퍼런스 Hook 실물은 시연 PS-4(EX-DH)가 생성해 실재한다(생성 주체 구분, L-07).
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다 — 종전의 "settings.json 미존재"·"SessionStart만"·"PreToolUse 1건" 서술은 실측 정정 완료다. 시각 서술은 L-09 준수(§5.2 `occurredAt` = 순서 값, 벽시계 아님). `uaf-verified: 본 문서의 "실재" 주장 지점을 §7 표 대상과 1:1 대조 — 스윕 범위 = §0·§2·§3·§4·§7`

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **소유 경계 (재정의·확장 0).** 계약 소유 = 08 §3(§3.1-B 정의·능력·경계 · §3.1-C 등록 완료 조건·reason · §3.1-D Dispatch·순서 · §3.1-E 실패 처리·격리 · §3.2-A/B 카탈로그·명명·확장 규칙 · §3.2-C Event Record · §3.2-D Hook Binding · §3.2-E Failure Report · §3.3 INV-1~8)와 01 §3.2-A·§3.1-A(Module Manifest·Register); 계측 지점 물리 실현 소유 = loop-binding.md(lifecycle)·delegation-protocol.md(agent)·memory-binding.md(memory)·runtime-binding.md(runtime). 본 문서는 그 **물리 실현**만 확정하며 새 Event·domain·phase·필드·reason·불변 규칙 신설 0이다 — 판정 기준은 정본 §(08 §3·§4)다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형식·물리 경로·파일 확장자·세션/턴·서브에이전트 등 환경 토큰은 이 Adapter 경계 문서에만 둔다(08 §3은 AI 비의존 — INV-8). 작성 시점 감사 서술(동시 작성 형제 불인용·금지 토큰 자가 스캔·생성 파일 범위)은 §9 이력과 git 앵커 90ca19c에 남는다.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-EH1 (`contextView` 투영 스키마 원천 조율 — 비차단).** 상세 투영 스키마는 각 원천 spec(03·02·04·01) 소유이며(08 §3.2-C) 본 문서는 읽기 전용 전달 채널만 바인딩했다. 형태 B 실행 계측 도입 시 각 원천이 노출할 스키마의 확정 정합이 필요하다. 계약 변경이 아니므로 비차단.
- **OQ-EH2 (Hook Module 하위 구조 = Worker 제안, Advisor 채택 대상 — 비차단).** `.claude/hooks/<hookModuleId>/` + `manifest.md` 병치(순수 observer는 단일 `.md` 축약형)는 §4.1의 제안이며 대안(전역 hooks 선언 1파일 등)도 계약(08 §3.2-D·§3.1-C)을 위반하지 않는다. 시연 Task가 이 정본 구조대로 레퍼런스 Hook을 생성했다(§7). 비차단.
- **OQ-EH3 (형태 B 경계 분할·실행 훅 결선 — 비차단).** Hook 실행 메커니즘(형태 B)이 하네스 native 메커니즘과 `framework/adapters/claude/` 사이 어디에 결선·분할되는지는 형태 B 설계 시 확정 대상이다(structure.md §4 규칙 4 defer). 형태 A에서는 이 분할이 필요하지 않다. 비차단.
