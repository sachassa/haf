# framework/adapters/claude/memory-binding — Claude Code Memory Adapter 바인딩

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본:

- specs/04-memory.md §4.1 — Claude Code Binding 표(7행). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/04-memory.md §4.2 — 이식 교체 지점(1~5). 본 문서가 대응을 명시하는 교체 지점의 정본.
- specs/04-memory.md §3.1-A·§3.1-B — Record / Recall 연산. 본 문서는 이 계약을 재정의하지 않고 § 포인터로만 인용한다.
- specs/04-memory.md §3.2-A·§3.2-C·§3.2-E — Memory Item·Memory Index/Index Entry·저장 구조 규격. 물리 실현의 대상 계약(재정의 0).
- specs/04-memory.md §3.3 INV-1·INV-3·INV-4·INV-6·INV-7·INV-8 — 단일 Port·전량 로드 금지·최소 Context·기록 불변·인덱스 정합·백엔드 비의존. 본 문서가 물리 실현에서 준수·대조하는 불변.
- specs/05-lessons.md §4.1·§4.2 — Lessons Claude Code 바인딩과 이식 교체 지점. 특히 SP-1(레코드 직렬화·저장 위치 — Adapter 소관)·SP-2(적용 조건 매칭 구현 — Adapter 소관). 계약 표면(스키마·매칭 계약)은 05가 소유한다.
- framework/memory/memory-service.md §5.1·§5.2 — 기록·회수 프로토콜(계약 수준 단계). 본 문서 §3의 물리 절차가 1:1 대응하는 프로토콜 정본. §3.2·§4.2(Recall 시스템 상한 소비 지점)·§5.3(reason 소속).
- framework/memory/module-manifest.md — Memory Service Provider Module Manifest. `entrypoint` 추상 참조의 물리 해소 위임 지점(§4), `configSchema` 키 `recall.limit.max`(유한 양의 정수, 기본 20).
- framework/memory/memory-store.md §2·§3·§4·§5 — Memory Item(§2)·Memory Index/Index Entry(§3)·Store 계약 구조(§4)·scope 해소 대응(§5)의 인스턴스 소유 문서. 본 문서는 그 데이터 계약을 § 포인터로 참조하고 물리 실현만 확정한다.
- framework/memory/lessons.md §5.1·§5.2 — `kind` 값 3종(`lesson`/`best-practice`/`recurrence-judgment`)·applicability의 labels·kind 투영 규칙. 계약 표면 소유 문서(본 문서는 물리 직렬화·매칭 구현만 확정).
- framework/adapters/claude/runtime-binding.md — 자매 Adapter Binding 문서. 교체 지점 표 관례·구체 토큰 격리·실측 기반 상태 서술·형태 A/B 구분·Config 스코프 물리 소스(§3.3)·Register/Resolve 수행 방식(§3.2)의 선행 관례.
- framework/core/structure.md §2·§5·§6 — 4경계 배치, C-3 금지 토큰 규칙(Adapter 경계는 격리 보유로 비적용), 산출물 표. 본 문서 경계의 근거.
- specs/01-runtime.md §4·§3.2-B — Adapter Binding(Provider 등록·물리 진입점 해소)·Config 병합 규칙(Module > Project > Global). § 포인터로만 참조.
- docs/session-handoff-v0.3.md §1.4·§1.5 — A5 재작업 사례(미존재를 "실재"로 서술 → 파일 시스템 전수 대조로 검출)와 Lesson 후보 3(상태 서술은 실측 후 기록). 본 문서 §7의 실측 대조 근거.
- specs/00-glossary.md — 용어 정본. 본 문서는 새 용어를 신설하지 않는다.
- ROADMAP.md v0.4 (Memory & Lessons) — 산출물 "Memory store 구조·포맷 / 인덱스 규격 / 기록·회수 프로토콜"의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 04 §3.3 INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0과 동형). 단 이 문서는 Core Contract(04 §3·05 §3)와 그 인스턴스 문서(framework/memory/ 4문서)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. `framework/adapters/claude/` 경계의 두 번째 산출물(첫 산출물: runtime-binding.md). 04 §4.1 바인딩 표 7행의 물리 실현 매핑(§2 — Provider·Item 직렬화·Store·Index·Record·Recall·백엔드 격리), 물리 store·index 경로를 `framework/adapters/claude/memory-data/` 이하로 확정·본 문서 정본 선언(§0·§2), Record/Recall 물리 절차의 memory-service.md §5.1/§5.2 1:1 단계 대응(§3), entrypoint 물리 해소·`recall.limit.max`(기본 20) 물리 반영(§4), Lessons `kind` 3종 직렬화 표기·applicability 매칭 구현·재발/승격 물리 기록 위치(§5), 04 §4.2 이식 교체 지점 1~5 대응(§6), 실측 대조 표(§7 — store·index 물리 자산은 현 시점 미존재, 시연 시 생성 예정). 04·05 계약 재정의 0, 동시 작성 시연 절차서(docs/v0.4-demo-procedure.md) 내용 불인용(07 R2). | Worker (Advisor 위임, Task M5) |
| 2026-07-05 | v0.4 Draft (r2) | Advisor 개정 지시 반영 (OQ-M7-1 해소 — 라벨 키 물리 표기 정본 갭 보완). (1) §5.4 신설 — 라벨 키 물리 표기(정본) 표 5키(`situation`/`stable_id`/`status`/`verdict`/`matched_lesson_id`) ↔ 투영 대상 ↔ 값 형태. lessons.md §5.2가 "무엇을 투영하는가"를 소유하고 본 표는 "키 이름·표기"만 확정(계약 표면 재정의 0). 첫 실사용 = v0.4 시연(docs/v0.4-demo.md). (2) 같은 상태 서술 전 지점 전수 갱신 — §5 헤더·도입·§5.2·§5.3 포인터, §6 SP-1 행, §0·§10. (3) §7 실측 대조 전면 갱신 — memory-data/ 실재 반영(직접 실측: store 21파일 mi-0001~mi-0021.json, index.jsonl 21라인; kind lesson 16/best-practice 2/recurrence-judgment 3). 데이터 미생성 전제의 라이브 상태 서술을 실재 반영으로 전건 교체(L-07 실측 후 기록). (4) OQ-M5-1 해소 표기(lessons.md §5.2 r2 투영 규칙 확정 + §5.4). 04·05 계약 재정의 0, 물리 데이터·framework/memory/·demo 파일 무수정. | Worker (Advisor 개정 지시, Task M5 r2) |
| 2026-07-05 | v0.4 Draft (r3) | r1 이력 행 문면 원복 — r2에서 교정했던 M5(r1) 행의 §7 참조 구문·동시 작성 절차서 불인용 문구를 r1 원문 그대로 되돌림. 이력 행은 시점 기록이며 작성 시점에 참인 서술은 stale이 아니다 — §9 append-only 문면 불변(Advisor 판정). "잔존 서술 0건" 재검증은 라이브 본문에만 적용된다. 라이브 본문·§5.4·§7 실측 서술은 무변경. | Worker (Advisor 교정 지시, Task M5 r3) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/04-memory.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)와 specs/05-lessons.md §3·§4, 그리고 framework/memory/ 4문서(memory-service.md·module-manifest.md·memory-store.md·lessons.md)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·필드·`kind` 값)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. framework/memory/ 4문서가 "물리 저장·직렬화·백엔드 I/O·물리 진입점 해소·매칭 구현은 Adapter Binding 문서 소관"이라며 미룬 **물리 경로·파일 구조·직렬화 형식·I/O 절차·매칭 알고리즘**이 실재하는(확정되는) 유일한 자리다(memory-service.md §0·§8, memory-store.md §4.2, module-manifest.md §4, lessons.md §5.2, 04 §4.1, 05 §4).
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계(`framework/core/`·`framework/runtime/`)와 Module 구현 디렉터리(`framework/memory/` 등) 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 04 §3.3 INV-8). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형식명, 물리 경로 `framework/adapters/claude/…`, 파일 확장자, 세션/턴 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(runtime-binding.md §0·§5와 동형).
- **물리 store·index 위치 정본 선언(done 2).** Memory Store·Memory Index의 물리 데이터 위치는 **Adapter 경계 이하 `framework/adapters/claude/memory-data/`로 확정한다**(Advisor 결정 — 물리 store·index는 Adapter 경계 이하). 이 위치는 Core 경계(`framework/core/`·`framework/runtime/`·`framework/memory/` 등)·`specs/`·`docs/` **밖**이다. **정확한 하위 경로·파일 구조·직렬화 형식·I/O 절차의 정본은 이 문서(§2)다.** framework/memory/ 4문서는 이 물리 위치를 "Adapter Binding 문서 소관" 포인터로만 미뤘고, 본 문서가 그 소유자로서 확정한다.
- **창설 금지.** 이 문서는 04 §4.1·05 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.4 산출물의 물리 실현 매핑으로 한정한다. 새 Memory 연산·필드·불변 규칙·`kind` 값을 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, runtime-binding.md §0, delegation-protocol.md §0). Memory Service는 정식 실행 Module이 아니라 규약 문서와 관행으로 실현된다(형태 A). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(디렉터리·정의 문서, 그리고 v0.4 시연 M7이 생성한 store·index 데이터 — §7 실측)과, **실행 코드 도입 시 로딩될 지점**(형태 B — 실행 진입점·로더)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(done 7).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(session-handoff-v0.3.md §1.4 A5 사례·§1.5 Lesson 후보 3 재발 방지). store·index 물리 자산의 실재 여부는 실측으로 판정한다 — M5 draft 시점엔 데이터 미생성이었고, v0.4 시연(M7) 실행 후 실재로 전환되었다. §7이 그 실측 대조 표이며 r2에서 현재 상태로 전수 갱신했다.
- 용어는 specs/00-glossary.md 정본만 사용한다. `lesson`·`best-practice`·`recurrence-judgment`는 05가 소유한 `kind` 값(lessons.md §5.1)이며, 본 문서는 그 물리 직렬화 표기만 확정한다(용어 신설 아님).

---

## §1. 목적

이 문서는 04 §4.1(Memory Claude Code Binding)과 05 §4.1(Lessons Claude Code Binding)을 이 환경 위에 **v0.4 시점의 구체 물리 실현**으로 매핑한다.

책임은 다섯 가지다.

- 04 §4.1 바인딩 표의 **7행 전부**를 물리 경로·파일 구조·직렬화 형식·I/O 절차로 확정한다(§2). 물리 store·index 위치는 `framework/adapters/claude/memory-data/`로 확정하고 그 정본이 본 문서임을 명시한다(§0·§2, done 1·2).
- Record·Recall의 **물리 실행 절차**를 memory-service.md §5.1·§5.2 프로토콜 단계와 **1:1로 대응**시킨다 — Record = Item 기록 + Index 갱신의 정합 수행(04 INV-7), Recall = index 조회 → scope 내 대상 Item만 로드(04 INV-3/INV-4)(§3, done 3).
- module-manifest.md `entrypoint` 추상 참조의 **물리 해소 지점**과 `configSchema` 키 `recall.limit.max`(기본 20)의 **물리 반영**(어디서 읽혀 어떻게 적용되는가)을 명시한다(§4, runtime-binding.md 교체 지점 관례 동형, done 4).
- lessons.md `kind` 3종의 **직렬화 표기**를 확정하고(05 §4.2 SP-1), applicability **매칭의 구현 방식**을 확정하며(05 SP-2 — 계약 표면은 05 소유), 재발 판정·승격의 **물리 기록 위치**를 `kind` 3종 위에서 일관되게 서술한다(§5, done 5).
- 04 §4.2 이식 교체 지점 1~5 각각에 본 문서의 대응 절을 표로 명시한다(§6, done 6). 그리고 상태 서술을 실측과 대조한다(§7, done 7).

이 문서는 04 §3·05 §3·framework/memory/ 4문서의 어떤 계약 요소도 재정의·확장하지 않는다(§0). 형태 A → 형태 B 전환 시에도 Core Contract 변경은 0이며(structure.md §7 C-1), 이 문서(§6의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 04 §4.1 바인딩 표 7행 물리 실현 (done 1·2·7)

04 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. 아래 표의 "04 §4.1 바인딩" 열은 정본 표현을 그대로 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·구조·형식·절차를, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현/시연 예정을 정직하게 구분한다(§7 실측 대조).

물리 백엔드 디렉터리 구조(본 문서 정본 — v0.4 시연 M7 실행으로 데이터 실재, §7 실측):

```
framework/adapters/claude/
├─ runtime-binding.md          # 실재 (v0.3 Baseline)
├─ memory-binding.md           # 실재 (본 문서)
└─ memory-data/                # ★ 백엔드 격리 루트 — 실재 (M7 시연 생성)
   ├─ store/                   #   Memory Store — Memory Item 파일들 (실측: 21파일)
   │  └─ <id>.json             #     Memory Item 1건 = 파일 1개 (append-only, 불변; 실측: mi-0001~mi-0021.json)
   └─ index/
      └─ index.jsonl           #   Memory Index — Index Entry append-log (1 line = 1 Index Entry; 실측: 21라인)
```

| # | §3 계약 요소 (정본 §) | 04 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Memory Service Interface (Port) | Memory Service Provider Module. `framework/memory/`에 구현. contract = `MemoryServiceInterface`. Runtime이 Register/Resolve. | Provider의 계약 인스턴스 = framework/memory/memory-service.md, 등록 서술자 = framework/memory/module-manifest.md(실재). 활성화 진입점의 **물리 해소**는 §4 — 이 백엔드(memory-data/)에 대한 Record/Recall 수행. contract `MemoryServiceInterface`는 module-manifest.md `contract` 값과 정합. | 계약 인스턴스·Manifest 실재. 실행 진입점은 형태 B. |
| 2 | Memory Item 직렬화 (§3.2-A) | item 당 파일 또는 append-log 레코드. `content`는 불투명 페이로드로 직렬화. | **item 당 파일**: `memory-data/store/<id>.json` — Memory Item 1건 = JSON 파일 1개. 필드 = memory-store.md §2(정본 04 §3.2-A)의 6필드(`id`/`kind`/`content`/`source`/`timestamp`/`labels`). `content`는 불투명 페이로드로 그대로 직렬화(Adapter가 내부 해석 안 함 — 04 INV-5). 파일명 = `<id>` → id 유일성을 파일명 충돌로 물리 보장. | 형식·경로 구조 확정(정본). 데이터 파일 실재 — M7 시연 생성(실측: store/ 21파일, mi-0001~mi-0021.json). |
| 3 | Memory Store 물리 저장 (§3.2-E) | 파일 기반 store. 물리 경로·구조는 Adapter 경계 뒤. | `memory-data/store/` 디렉터리. **append-only**(04 INV-6) — 기록된 `<id>.json`은 재작성하지 않는다. 갱신·정정은 새 `<id>.json`(새 Memory Item) 추가로 표현(memory-store.md §4.1). 전량 로드 없음 — store 파일은 Recall이 scope로 한정된 대상만 읽는다(§3.2, 04 INV-3). | 경로 구조 확정(정본). 데이터 실재 — M7 시연 store/ 21파일(실측). |
| 4 | Memory Index 물리 구현 (§3.2-C) | 파일 기반 인덱스. scope 해소는 인덱스 파일 조회로 수행. | `memory-data/index/index.jsonl` — Index Entry append-log(1 line = 1 Index Entry, Record 순서로 append). 각 line 필드 = memory-store.md §3.2(정본 04 §3.2-C)의 6필드(`id`/`kind`/`source`/`timestamp`/`labels`/`digest`). **`content` 원문 없음**(04 INV-4). scope 해소 = index.jsonl line 스캔으로 narrowing 차원(memory-store.md §5 대응) 필터 → 후보 `id` 집합. store 전체 스캔 없음. | 형식·경로 구조 확정(정본). 데이터 실재 — index.jsonl 21라인(실측). |
| 5 | Record 실행 (§3.1-A) | Memory Item 파일 기록 + 인덱스 파일 갱신을 함께 수행(정합 갱신 — INV-7). | store/`<id>.json` 쓰기 + index.jsonl에 대응 Index Entry line append를 **함께 완료**(04 INV-7). 물리 절차·정합 규칙은 §3.1(memory-service.md §5.1 1:1 대응). | 절차 확정(정본). 실행은 시연/형태 B. |
| 6 | Recall 실행 (§3.1-B) | 인덱스 조회로 Index Entry 후보 해소 → scope 내 대상 Item 파일만 읽음. 전량 로드 금지(INV-3/INV-4). | index.jsonl 조회로 scope 해소 → `detail=index`면 매칭 Index Entry만 반환, `detail=full`+scope 한정이면 매칭 `id`의 store/`<id>.json`만 로드. 물리 절차는 §3.2(memory-service.md §5.2 1:1 대응). | 절차 확정(정본). 실행은 시연/형태 B. |
| 7 | 백엔드 격리 | store·index·직렬화·I/O는 `framework/adapters/` 뒤로 격리. Port 앞에서는 백엔드가 보이지 않는다. | store·index·직렬화 형식(JSON/JSONL)·파일 I/O 전부 `framework/adapters/claude/memory-data/`(이 Adapter 경계 뒤)에 격리. 소비자(Agent·Loop·Workflow·Verifier)는 Port(memory-service.md §7) 경유만 하며 이 경로·형식을 참조하지 않는다(04 INV-1·INV-8). | 격리 경계 확정(정본). memory-data/ 격리 뒤 데이터 실재 — M7 시연 생성(실측). |

주:

- 위 7행은 04 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 04 §4.1 정본 표현을 이 환경의 구체 경로·형식으로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **id 할당 스킴.** Memory Item `id`는 Record가 유일하게 할당하는(04 §3.2-A) 안정·유일 토큰이다. 물리 실현: 파일명 `<id>.json`이 그 자체로 유일성 보장 매체이며(같은 이름 파일 생성 실패 = `DuplicateId`), 사전식으로 정렬 가능한 형태(예시 형태 `mi-<정렬가능토큰>`)를 사용해 index.jsonl의 append 순서(= Record 순서)와 정합시킨다. 정확한 토큰 형태는 Adapter 선택이며(이식 교체 지점 §6-SP1), `id`의 안정성·유일성·불변 참조 계약(04 §3.2-A·INV-6)은 유지된다. 순서 기준 자체의 의미(예: 05 `ordering_ref`)는 특화 계약 소관으로 본 문서가 정의하지 않는다.
- **직렬화 형식(JSON/JSONL) = Adapter 선택.** Memory Item의 `content`는 kind별 임의 구조의 불투명 페이로드이므로(04 INV-5), 중첩 구조를 담는 자기서술적 데이터 형식(JSON)을 store 레코드에, 라인 구분 로그(JSON Lines)를 index에 사용한다. 이 형식 선택은 04 §4.2-1·05 §4.2 SP-1의 교체 지점이며, 이식 시 대상 환경 포맷으로 교체된다(§6). v0.x 실측 기억 규모(module-manifest.md §3)에서는 store를 평면(flat) 배치로 두고, 샤딩 등 규모 대응은 형태 B/규모 사안으로 미룬다(추측·선취 금지).
- **memory-data/ 경로·구조·형식은 본 문서가 확정한 지원 구조(정본)이며, 데이터는 시연 Task가 생성했다.** 실제 디렉터리·데이터 파일 생성은 **시연 Task 소관**(docs/v0.4-demo.md — Task M7 수행 기록)이며, v0.4 시연이 이 정본 구조 그대로 store 21파일·index 21라인을 생성했다(§7 실측 대조). 본 문서(M5)는 물리 데이터 자산을 생성하지 않는다 — 구조·형식·절차의 정본만 소유한다.

---

## §3. Record·Recall 물리 실행 절차 — memory-service.md §5.1/§5.2 1:1 대응 (done 3)

memory-service.md §5.1(Record)·§5.2(Recall)의 계약 수준 프로토콜 단계를 이 환경의 물리 파일 연산으로 **단계 번호 1:1** 대응시킨다. 계약의 진위 판정 기준은 memory-service.md §5(정본 04 §3.1)이며, 본 절은 각 단계를 물리 연산으로 실현할 뿐 재정의하지 않는다.

### §3.1 Record 물리 절차 — Item 기록 + Index 갱신 정합 (04 INV-7)

| memory-service.md §5.1 단계 | 물리 실현 (claude 환경) | reason (실패 시) |
|---|---|---|
| **1** — `id` 제외 필수 필드(`kind`·`content`·`source`·`timestamp`) 확인 | store/`<id>.json` 쓰기 **전에** 입력 Memory Item의 필수 4필드 유무를 검사한다. 누락이면 어떤 파일도 쓰지 않고 거부한다. | `SchemaViolation` (Record — 04 §3.1-A) |
| **2** — `id`를 Memory Store에서 유일 할당 | 할당 `id`에 대해 store/`<id>.json`을 **없을 때만 생성**(create-if-absent)한다. 같은 이름 파일이 이미 있으면 유일 할당 실패로 거부한다(파일명 = 유일성 매체). | `DuplicateId` (Record — 04 §3.1-A) |
| **3** — Memory Item 기록 + 대응 Index Entry 생성 **함께 완료** | store/`<id>.json` 쓰기 **직후** index/index.jsonl에 대응 Index Entry line 1개를 append한다. 둘 다 완료해야 Record 성립. 한쪽만 반영된 상태(예: store 파일은 있으나 index line 없음)는 정합 위반이며, store 파일명 집합과 index `id` 집합의 대조로 검출된다. | `IndexInconsistent` (Record, INV-7 — 04 §3.1-A) |
| **4** — Record는 **추가(append)** 만, 기록 불변 | 기록된 `<id>.json`과 index.jsonl의 기존 line은 재작성·삭제하지 않는다. 갱신·정정은 새 `<id>.json`(새 Memory Item, 새 Index Entry line) 추가로 표현한다(04 INV-6, memory-store.md §4.1). | — (불변 위반은 절차상 발생 안 함) |
| **5** — `content` 불투명 페이로드 | `content` 필드는 입력 그대로 JSON 값으로 직렬화한다. Adapter는 `kind`·`content` 내부를 해석·검증하지 않는다(04 INV-5). | — |

- **정합 갱신(INV-7)의 물리 순서와 한계.** 물리 순서는 (item 파일 쓰기) → (index line append)이며, 둘 다 존재해야 Record 완료다(단계 3). Bootstrap(형태 A)에서 이 "함께 완료"는 절차 준수 + 완료 후 대조(store 파일명 ↔ index `id`)로 보증한다. 더 강한 원자성 보장(예: 임시 파일 후 이름 변경, 선기록 마커)은 **형태 B 실행 코드 소관**이며, 그 도입 시에도 04 §3.1-A 완료 조건·INV-7 계약 변경은 0이다(structure.md §7 C-1). 본 문서는 계약을 넘는 원자성 메커니즘을 추측·확정하지 않는다.
- reason 코드의 소속(Record 3종)은 memory-service.md §5.3 표를 따른다 — 본 문서는 재정의하지 않는다.

### §3.2 Recall 물리 절차 — index-first, scope 내 대상 Item만 로드 (04 INV-3/INV-4)

| memory-service.md §5.2 단계 | 물리 실현 (claude 환경) | reason (실패 시) |
|---|---|---|
| **1** — `purpose`·`scope` 존재 확인 | Recall Request에서 `purpose`·`scope` 유무를 먼저 검사한다. 하나라도 없으면 index.jsonl을 **열지 않고** 거부한다. | `MissingPurpose` / `MissingScope` (Recall, INV-2 — 04 §3.1-B) |
| **2** — `scope` bounded 확인 | `scope`가 narrowing 차원(`kind`/`labels`/`timeRange`/`source`) 최소 하나 또는 finite `limit`을 갖는지 검사한다. 없으면(전체 store 겨냥) store·index를 읽지 않고 거부한다. | `UnboundedScope` (Recall, INV-3 — 04 §3.1-B) |
| **3** — `scope`를 Memory Index로 해소 | index/index.jsonl **line만 스캔**하여(각 line은 `content` 원문 없는 경량 서술자) scope narrowing 차원을 memory-store.md §5 대응(`kind`→`kind`, `labels`→`labels`, `timeRange`→`timestamp`, `source`→`source`)으로 필터해 후보 `id` 집합을 얻는다. **store 파일은 아직 읽지 않는다.** 부합 line이 없으면 해소 실패. | `ScopeUnresolvable` (Recall — 04 §3.1-B) |
| **4** — index-first, content는 `detail=full`+scope 한정 시에만 | 기본(`detail=index`)이면 매칭 Index Entry line만 반환하고 store 파일을 읽지 않는다. `detail=full`이 명시되고 scope로 한정된 경우에만 매칭 후보 `id`의 store/`<id>.json`을 **그 대상만** 로드해 Memory Item으로 반환한다(04 INV-4). | — |
| **5** — 반환량 `limit`·시스템 상한 이내, `truncated` 표시 | 반환 후보 수를 요청 `limit`과 시스템 상한(= `recall.limit.max`, 기본 20 — §4)의 더 작은 값으로 절단하고, 절단되면 `truncated=true`로 표시한다. 어떤 경우에도 store 전량을 반환하지 않는다(04 INV-3). | — |

- **최소 Context 우선(INV-4)의 물리 보장.** 단계 3에서 index만 스캔하고 단계 4에서 매칭 대상 store 파일만 로드하므로, `content` 원문은 명시적 `detail=full`+scope 한정에서만 물리적으로 읽힌다. index.jsonl 스캔은 `content` 원문을 담지 않는 경량 서술자 대상이므로 전량 로드(INV-3)가 아니다 — INV-3은 **store(Memory Item content)** 전량 반환 금지이며, 경량 index 조회는 그 금지 대상이 아니다.
- 정본 예(memory-service.md §5.2 예, 04 §8 예1) 정합: `scope = { labels: { task: A }, kind: decision }`, `detail=index`(기본) → index.jsonl에서 해당 line만 반환. 특정 `id` 원문 필요 시 `scope = { id }`, `detail=full`로 재Recall → store/`<id>.json` 1개만 로드. 접근은 contract `MemoryServiceInterface`(단일 Port) 경유다.

---

## §4. entrypoint 물리 해소 · `recall.limit.max` 물리 반영 (done 4)

module-manifest.md가 "물리 해소는 Adapter Binding 문서 소관"으로 미룬 두 지점을 확정한다. runtime-binding.md의 교체 지점 관례(추상 참조 → 물리 실현, 형태 A/B 구분)와 동형으로 서술한다.

### §4.1 `entrypoint` 추상 참조의 물리 해소

module-manifest.md `entrypoint` = "추상 참조 — Record/Recall 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4)". 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Provider Module 활성화 진입 — Record/Recall(memory-service.md §3) 노출 | **형태 A(Bootstrap):** 활성화 진입은 규약으로 실현된다 — Record/Recall은 memory-service.md §5 프로토콜(§3의 물리 절차)에 따라 이 백엔드(`memory-data/`)를 대상으로 수행된다. 별도 실행 진입점 파일은 없다. | 규약 실현(형태 A) |
| 위 진입점의 실행 코드 로케이터 | **형태 B:** Record/Recall을 노출하는 실행 코드가 non-core 실행 경계(`framework/memory/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 `memory-data/` 백엔드에 대해 두 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지). | 형태 B |

- **Register/Resolve 정합(runtime-binding.md §3.2 동형).** 이 Provider의 등록(Register)은 Manifest(framework/memory/module-manifest.md) + 본 바인딩 배치로 규약 실현되며(형태 A), 해소(Resolve)는 소비자가 Port(contract `MemoryServiceInterface`)로 Record/Recall을 호출할 때 이 백엔드로 해소되는 것이다. Memory Service는 Agent가 아니라 Cross-cutting Service이므로 Resolve는 서브에이전트 디스패치가 아니라 **Port 소비 경로**로 실현된다(04 §3.4, memory-service.md §7). 이 등록 경로는 이식 교체 지점 SP-5에 대응한다(§6).

### §4.2 `recall.limit.max`(기본 20)의 물리 반영 — 어디서 읽혀 어떻게 적용되는가

module-manifest.md `configSchema` 키 `recall.limit.max`(유한 양의 정수, 기본 20; Recall 시스템 상한의 값 원천 — Advisor 결정 DP-M1). 그 물리 반영:

| 관점 | 물리 실현 (claude 환경) | 형태 |
|---|---|---|
| **값·기본값 선언 위치** | 스키마+기본값(20) 선언은 Manifest configSchema(framework/memory/module-manifest.md §3, 실재)에 있다 — v0.3 `retry.limit` 기본값이 결정 기록으로 실현된 것과 동형(runtime-binding.md §3.3). | 실재(형태 A 선언) |
| **override 물리 소스** | override는 Config 스코프별 물리 소스에서 온다(runtime-binding.md §3.3 동형): Module 스코프 = 이 Provider Module의 설정 블록(물리 해소는 §4.1 진입점과 함께 형태 B에서), Project 스코프 = `.claude/settings.local.json` 등, Global 스코프 = `~/.claude/settings.json`. 병합은 Module > Project > Global(01 §3.2-B). | Global/Project 소스 실재, Module 소스는 형태 B |
| **읽히는 지점(read)** | Recall 시 읽힌다 — 소비 지점은 memory-service.md §3.2(Recall 완료 조건)·§4.2(Recall Request `limit`). | 규약 실현(형태 A) / 형태 B 로더 |
| **적용 방식(apply)** | Recall 물리 절차 §3.2 **단계 5**에서 적용된다 — 반환 후보 수를 `min(요청 limit, recall.limit.max)`로 절단하고, 요청 `limit` 미지정 시 `recall.limit.max`(기본 20)를 상한으로 적용한다. 절단 시 `truncated=true`. | §3.2-5의 절차 |

- **형태 구분.** v0.4 Bootstrap에서 이 값은 Manifest configSchema 선언(기본 20)으로 실현(형태 A)되며, 실행 로더(형태 B) 도입 시 effective config(Module > Project > Global 병합)로 로딩되어 Recall이 §3.2-5로 적용한다. 상한의 **존재·의미**(04 §3.1-B) 계약은 불변이며, 본 문서는 값 원천·읽힘·적용의 물리 지점만 바인딩한다(module-manifest.md §3 재정의 0).

---

## §5. Lessons `kind` 3종 직렬화 · applicability 매칭 구현 · 라벨 키 물리 표기 · 재발/승격 물리 기록 (done 5)

lessons.md가 "직렬화 표기·매칭 구현·라벨 키 물리 표기·저장 위치는 Adapter 소관"으로 미룬 지점을 확정한다. **계약 표면(스키마·매칭 계약 표면·`kind` 값 정체성·"무엇을 `labels`에 투영하는가")은 lessons.md·05가 소유하며**(05 §3.2, 05 §4 SP-1·SP-2, lessons.md §5.1·§5.2), 본 절은 물리 직렬화·매칭 구현·**라벨 키 물리 표기(§5.4)**·기록 위치만 바인딩한다.

### §5.1 `kind` 값 3종 직렬화 표기 (05 §4.2 SP-1 — Adapter 소관)

lessons.md §5.1이 확정한 세 안정 분류자 값을, 이 환경의 Memory Item `kind` 필드 직렬화 표기로 확정한다.

| 특화 기록 (스키마 소유) | `kind` 값 (lessons.md §5.1 소유) | 물리 직렬화 표기 (이 Adapter 확정) |
|---|---|---|
| Lesson (lessons.md §2.1 / 05 §3.2-A) | `lesson` | store/`<id>.json`의 `kind` 필드 값 = 문자열 `"lesson"` (소문자, 구분자 없음) |
| Best Practice (lessons.md §2.2 / 05 §3.2-B) | `best-practice` | `kind` 필드 값 = 문자열 `"best-practice"` (소문자, 하이픈 구분) |
| 재발 판정 레코드 (lessons.md §2.5 / 05 §3.2-E) | `recurrence-judgment` | `kind` 필드 값 = 문자열 `"recurrence-judgment"` (소문자, 하이픈 구분) |

- 세 값은 각 Memory Item의 `kind` 필드에 위 문자열 그대로 직렬화되며, index.jsonl line의 `kind` 필드에도 동일하게 반영된다(scope의 `kind` 차원 해소용). Memory·Adapter는 이 값을 **불투명 분류자**로만 취급한다(04 INV-5) — Lesson/Best Practice/재발 판정의 `content` 상세 스키마는 05가 소유하며 Adapter는 해석하지 않는다.
- 구분자·대소문자·물리 인코딩이 이 문서가 확정하는 SP-1 소관 표기다(05 §4.2 SP-1, lessons.md §5.1). 분류자의 안정적 정체성(무엇을 지칭하는가)은 lessons.md §5.1이 소유한다 — 본 문서는 표기만 확정한다.

### §5.2 applicability 매칭 구현 (05 §4.2 SP-2 — 구현은 Adapter, 계약 표면은 05 소유)

lessons.md §5.2: 회수는 Port의 `kind`/`labels` 범위 조회로 후보를 좁힌 뒤 상황 서술자 ↔ `applicability` 최종 대조를 Port 위에서 수행한다. **매칭 계약 표면(질의 파라미터로 상황 서술자를 전달하고 관련성 매칭 집합을 반환)은 05가 소유하고**(05 §3.2-C, lessons.md §5.2), 매칭 **구현(대조 알고리즘)**을 이 Adapter가 확정한다.

- **1단계 — Port 범위 조회(index 후보 축소).** Recall scope로 index.jsonl을 조회해 후보를 좁힌다(§3.2 단계 3): `kind` 차원 = 회수 대상 종류(`lesson`/`best-practice`) 구분, `labels` 차원 = applicability가 투영된 `labels`(lessons.md §5.2 투영 규칙 — 05 소유)와 상황 서술자의 겹침. 이 단계는 04 계약을 변경하지 않고 `kind`/`labels`/`timeRange`/`source` 범위 조회만 사용한다(04 §9 결정 기록, lessons.md §5.2).
- **2단계 — 좁혀진 후보 위 관련성 산출(매칭 구현).** Port가 좁힌 후보 집합에 대해, 상황 서술자와 각 후보의 `applicability`(labels로 투영된 트리거 서술)의 **라벨 집합 겹침(label-set overlap)**으로 관련성을 산출한다. 겹침이 큰 순으로 정렬하고, 회수 정책(최소 범위)에 따라 최소 집합만 반환하되 `recall.limit.max`(§4.2)로 상한한다. 매칭 없으면 빈 집합(실패 아님 — 05 §3.1-B).
- **구현 선택임을 명시.** 위 라벨 집합 겹침(키워드형 대조)은 이 Adapter의 v0.4 **구현 선택**이다. 의미 검색·임베딩 등 다른 대조 알고리즘으로의 교체가 이식 교체 지점 SP-2다(05 §4.2 SP-2, §6). **계약 표면(어떤 질의를 받고 무엇을 반환하는가)은 05가 소유**하며, 본 문서는 그 표면을 바꾸지 않고 대조 알고리즘만 바인딩한다. `applicability` → `labels`/`kind` 투영 규칙 자체는 lessons.md §5.2(05 소유)이며 본 문서가 정의하지 않는다 — 그 투영에 쓰이는 **물리 라벨 키 이름·값 형태**는 §5.4가 정본으로 확정한다(05 §4 SP-1 위임).

### §5.3 재발 판정·승격의 물리 기록 위치 (kind 3종 위에서 일관 서술)

세 특화 기록은 별도 저장 경로를 갖지 않고 **전부 Memory Item의 `kind`로 단일 Port·단일 백엔드 위에 올라탄다**(04 §3.4, lessons.md §5). 물리 기록 위치는 §2와 동일한 store/index 백엔드다.

- **승격(Candidate → Active).** Register Candidate와 Promote는 각각 `kind="lesson"`(또는 `"best-practice"`) Memory Item을 **Record**로 기록한다 → store/`<id>.json` + index.jsonl line(§3.1). 기록 불변(04 INV-6)이므로 status 전이(Candidate→Active→Superseded/Retired)는 기존 파일 수정이 아니라 **새 Memory Item(새 `<id>.json`) 추가**로 표현된다. Lesson의 안정 `id`·`status`·`supersedes`는 `content`(05 소유, Adapter 불투명)에 담기고, 회수 대조에 필요한 투영은 lessons.md §5.2 투영 규칙(05 소유)에 따라 `labels`/`kind`로 반영된다(물리 라벨 키 `stable_id`·`status`는 §5.4). **승격 승인 권한(Advisor 전속 — 05 INV-4)은 백엔드 사안이 아니다** — 백엔드는 Record가 호출된 것만 기록하며, 승인 판정은 Lessons 계약(05)·역할 경계(02 §3.2-A) 소관이다.
- **재발 판정.** Judge Recurrence의 산출물(재발 판정 레코드, lessons.md §2.5)은 `kind="recurrence-judgment"` Memory Item으로 **Record**되어 동일 store/index 백엔드에 기록된다(§3.1). 이 레코드의 `verdict`·`matched_lesson_id`(필드 정본 lessons.md §2.5 / 05 §3.2-E)는 index 단계 조회용으로 `labels`에 투영되며, 그 물리 라벨 키는 §5.4가 확정한다. 판정 입력인 "작업별 회수 집합(회수 이력)"은 **03 루프 상태 기록 소관**이며(lessons.md §4, 05 §9·04 §9 결정 기록) 이 Memory 백엔드가 생성·저장하지 않는다 — 판정 연산의 입력으로 받는다.
- **일관성.** 세 `kind` 값 모두 §2의 동일 물리 규칙(item 당 파일, append-only, index 정합 갱신, index-first 회수)을 그대로 따른다. 백엔드는 `kind`를 불투명하게 다루므로(04 INV-5) 세 종류에 대해 저장·색인·회수 물리 절차가 분기되지 않는다. status 생애주기·supersede 의미·승격 권한·최신 Active 해소 규칙은 전부 05 계약 소관이며, 본 문서는 물리 기록 위치·회수 매칭 구현·라벨 키 물리 표기(§5.4)만 확정한다.

### §5.4 라벨 키 물리 표기 (정본 — 05 §4 SP-1 / lessons.md §5.2 위임)

lessons.md §5.2(r2)와 본 문서 §5.2는 "무엇을 `labels`에 투영하는가는 05가 소유하고, **라벨 키의 물리 표기(키 이름·값 형태)는 Adapter 소관**"으로 확정했다(lessons.md §5.2 말미, 05 §4 SP-1). 그 물리 표기의 **정본 자리가 이 절**이다. 아래 5개 라벨 키가 정본이며, 첫 실사용은 v0.4 시연(docs/v0.4-demo.md — Task M7 수행 기록)이다. 값 형태는 index/store 실측(§7)에 근거한다.

| 투영 대상 (무엇을 투영하는가 — 소유) | 물리 라벨 키 (이 Adapter 정본) | 값 형태 (실측 근거) |
|---|---|---|
| applicability 상황 유형·트리거 서술 (lessons.md §5.2 소유) | `situation` | 문자열 태그 배열 — 상황 유형·트리거 term 집합 (예 형태 `["<태그>", …]`) |
| Lesson·Best Practice 안정 `id` (lessons.md §5.2 투영; 필드 정본 05 §3.2-A/B) | `stable_id` | 문자열 — 특화 기록의 안정 식별자 |
| Lesson·Best Practice `status` (lessons.md §5.2 투영; 필드 정본 05 §3.2-A/B) | `status` | 문자열 — `Candidate`/`Active`/`Superseded`/`Retired` 중 하나 |
| 재발 판정 레코드 `verdict` (필드 정본 lessons.md §2.5 / 05 §3.2-E) | `verdict` | 문자열 — `Novel`/`RecallGap`/`Recurrence` 중 하나 |
| 재발 판정 레코드 `matched_lesson_id` (필드 정본 lessons.md §2.5 / 05 §3.2-E) | `matched_lesson_id` | 문자열 — 매칭된 Active Lesson 안정 id (`Novel`이면 부재 가능) |

- **소유 경계 (계약 표면 침범 0).** "무엇을 투영하는가"(투영 대상·투영 규칙·필드 의미)는 lessons.md §5.2(applicability·안정 `id`·`status`)·§2.5(재발 판정 레코드 필드)·05가 소유한다. **이 표는 그 투영 대상에 대한 물리 라벨 키 이름·값 형태만 확정**하며 투영 규칙·필드 의미를 재정의하지 않는다. 라벨 키 표기 관례(소문자·언더스코어 구분)는 이 Adapter 선택이며 이식 교체 지점 SP-1에 속한다(§6).
- **물리 위치.** 위 키들은 Memory Item의 `labels`(04 §3.2-A — 자유 태그 집합) 아래에 놓이고, Index Entry의 `labels`(04 §3.2-C)에도 그대로 실려 index 단계 후보 축소(§3.2 단계 3)에 쓰인다. `content` 원문 로드 없이 index 단계에서 `kind`/`labels`로 필터되므로 최소 Context 원칙(04 INV-4, 05 INV-6)과 정합한다.
- **실측 정합.** 이 5키는 index.jsonl 실측 결과(§7 — `situation`·`stable_id`·`status`·`verdict`·`matched_lesson_id`)와 일치한다. 이 표가 정본이며 demo.md는 그 첫 실사용 기록이다(정본이 자기 소관 표기를 기록 — OQ-M7-1 갭 보완).

---

## §6. 04 §4.2 이식 교체 지점 1~5 대응 (done 6)

04 §4.2 이식 교체 지점 1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인한다. 05 §4.2 SP-1·SP-2도 04 교체 지점과 겹치는 자리에 병기한다.

| # (04 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| 1 | Memory Item / Index Entry 직렬화 포맷 | §2 #2·#4, §5.1, §5.4 (05 SP-1) | store `<id>.json`(JSON) 레코드·index.jsonl(JSON Lines) line 포맷, `kind` 값 문자열 표기, 라벨 키 물리 표기(§5.4 — `situation`/`stable_id`/`status`/`verdict`/`matched_lesson_id`). | Memory Item(04 §3.2-A)·Index Entry(04 §3.2-C) 추상 스키마, `kind` 값 정체성(05 소유), labels 투영 규칙(05 §5.2 소유). |
| 2 | Memory Store 물리 저장 | §2 #3, §3.1 | `memory-data/store/` 파일 기반 store(item 당 파일, append-only). | 저장 구조 규칙(04 §3.2-E), append-only·정합 갱신(INV-6/INV-7). |
| 3 | Memory Index 구현 | §2 #4, §3.2 | `memory-data/index/index.jsonl` append-log 인덱스, line 스캔 scope 해소. | Memory Index 계약·scope 해소 대응(04 §3.2-C, memory-store.md §5), 최소 Context(INV-4). |
| 4 | 백엔드 I/O 메커니즘 | §2 #5·#6·#7, §3, §5.2 (05 SP-2) | 파일 I/O(create-if-absent·append·line 스캔·대상 파일 로드), applicability 매칭 대조 알고리즘(라벨 겹침). | Record/Recall 시그니처·회수 정책(04 §3.1), 매칭 계약 표면(05 §3.2-C 소유). |
| 5 | Provider Module 등록 경로 | §2 #1, §4.1 | Manifest + 본 바인딩 배치(형태 A)·형태 B 실행 진입점 로케이터. Runtime 이식 시 함께 교체(01 §4.2). | contract `MemoryServiceInterface`, Provider 등록·해소 계약(01 §3.1-A·§4, module-manifest.md). Memory는 참조만. |

- "유지되는 것" 열의 계약은 다른 AI·저장 환경으로 이식해도 바뀌지 않는다 — 04 §3 Core Contract·framework/memory/ 인스턴스·05 계약 표면의 이식 불변성이며, structure.md §7 C-1(형태 A→B 및 환경 전환에도 Core Contract 변경 0)과 정합한다.
- 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(04 §4.2 말미). 본 문서는 그 정식화를 선취하지 않고 v0.4 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 7 — A5 재발 방지)

session-handoff-v0.3.md §1.4(A5 사례 — 미존재 소스를 "실재"로 서술 → 파일 시스템 전수 대조로 검출)·§1.5 Lesson 후보 3(상태 서술은 실측 후 기록)에 따라, 본 문서의 "실재" 서술을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-05 r2 개정 시 `ls`/`find`/`grep`/`wc`/`diff` 직접 실측.** M5 draft 시점엔 memory-data/ 데이터가 미생성이었고, v0.4 시연 M7 실행으로 실재로 전환되었다 — 아래 표가 현재 상태다.

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-05 r2, 직접 실측) |
|---|---|---|
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — runtime-binding.md·memory-binding.md 존재 확인. |
| `framework/adapters/claude/runtime-binding.md` | 실재 (v0.3 Baseline, 자매 문서) | 실재. |
| `framework/adapters/claude/memory-binding.md` | 실재 (본 문서) | 실재 (이 파일). |
| framework/memory/ 4문서(memory-service·module-manifest·memory-store·lessons) | 실재 (계약 인스턴스·Manifest — § 포인터 대상) | 실재 — 4파일 확인(무수정). |
| `framework/adapters/claude/memory-data/` (백엔드 루트) | **실재** (본 문서 확정 구조대로 M7 시연 생성) | **실재** — `memory-data/store/`·`memory-data/index/` 존재 확인. |
| `memory-data/store/` Memory Item 파일 | **실재** (item 당 파일, `<id>.json`) | **실재 — 21파일**, `mi-0001.json`~`mi-0021.json` (id 스킴 §2 정본과 일치). |
| `memory-data/index/index.jsonl` | **실재** (Index Entry append-log) | **실재 — 21라인** (5704 bytes; store 21파일 id와 `diff` 0 = 1:1, INV-7 정합). |
| store/index `kind` 값 분포 (§5.1) | `lesson`/`best-practice`/`recurrence-judgment` | 실측 — `lesson` 16 / `best-practice` 2 / `recurrence-judgment` 3 (합 21). |
| index `labels` 라벨 키 (§5.4) | `situation`/`stable_id`/`status`/`verdict`/`matched_lesson_id` | 실측 — 5키 전부 사용 확인(§5.4 정본과 일치). |
| Manifest configSchema `recall.limit.max` = 20 | 실재 (형태 A 선언, framework/memory/module-manifest.md §3) | 실재 — module-manifest.md §3 configSchema 표에 선언 확인. |
| 실행 진입점·실행 로더(형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). |

- **핵심 구분.** 본 문서가 확정한 물리 store·index의 **경로·파일 구조·직렬화 형식·I/O 절차·라벨 키 표기(§5.4)는 정본**이며, v0.4 시연(M7)이 이 정본 구조 그대로 데이터를 생성했다 — 실측이 정본과 일치한다(store 21·index 21·id 스킴·`kind` 분포·라벨 키). 데이터 생성 주체는 **시연 Task(docs/v0.4-demo.md — Task M7)**이며, 본 문서(M5)는 구조·형식·절차·라벨 키 표기의 정본만 소유한다. r2는 데이터를 생성·수정하지 않고 실측 상태만 반영했다.
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다. 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로 쓰지 않았다(A5 재발 방지).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 04 §3·§4·05 §3·§4·framework/memory/ 4문서의 물리 실현이다. 어떤 연산·데이터 계약·불변 규칙·`kind` 값도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 정본 §다. 새 Memory 연산·필드·reason 코드·차원·`kind` 값을 추가하지 않았다.
- **계약 표면 소유 명시(done 5).** Lesson·Best Practice·재발 판정 레코드의 스키마·`kind` 값 정체성·applicability **매칭 계약 표면**·**"무엇을 `labels`에 투영하는가"**(투영 규칙)는 lessons.md·05가 소유한다. 본 문서는 물리 직렬화 표기(§5.1)·매칭 대조 알고리즘 구현(§5.2)·물리 기록 위치(§5.3)·**라벨 키 물리 표기(§5.4 — 키 이름·값 형태만)**만 확정한다. status 생애주기·supersede·승격 권한·최신 Active 해소 규칙·투영 규칙은 05 소관이다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형식(JSON/JSONL)·물리 경로(`framework/adapters/claude/memory-data/…`)·파일 확장자·세션/턴 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. framework/memory/ 4문서(Core/Module 구현 디렉터리 문서 본문)는 이 토큰을 "Adapter Binding 문서 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3 확장은 이 경계에 비적용 — 격리 보유).
- **동시 작성 문서 경계(07 R2) 및 r2 참조 범위.** M5 draft 시점엔 같은 Wave에서 동시 작성 중이던 시연 절차서(docs/v0.4-demo-procedure.md)·병렬 Task M6 산출물의 내용을 인용·추측하지 않았다(07 R2 준수). r2에서는 시연이 완료된 상태로, docs/v0.4-demo.md(Task M7 수행 기록)를 **첫 실사용 기록**의 사실(라벨 키 실사용·데이터 생성 주체)로만 참조한다 — 내부 서술·추론을 인용하지 않고, §5.4·§7의 정본 서술은 **파일 시스템 직접 실측**에 근거한다(demo.md 텍스트 인용 아님).
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 §8 open_questions로 에스컬레이션했다(추측 금지). 본 산출은 이 1개 파일(`framework/adapters/claude/memory-binding.md`)만 생성하며, framework/memory/ 4문서·Core 경계·specs·docs·물리 데이터 파일을 수정·생성하지 않는다.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-M5-1 (05 조율) — 해소됨 (v0.4 r2).** M5 draft 시점의 미결 — "안정 `id`·`status`가 index `labels`로 투영되는지 05 확정 필요" — 은 **lessons.md §5.2 r2**가 해소했다: 안정 식별 투영→`labels`·상태 투영→`labels`·최신 상태 해소 규칙(최신 `timestamp` = 현재 상태)을 05가 확정하고, "라벨 키의 물리 표기는 Adapter 소관"으로 명시 위임했다. 그 물리 라벨 키(`stable_id`·`status` 등 5키)는 본 문서 **§5.4가 정본으로 확정**했다(OQ-M7-1 갭 보완). 계약 표면(투영 규칙)은 05가 소유하고 본 문서는 키 이름·값 형태만 확정 — 침범 0. 잔여 없음.
- **OQ-M5-2 (원자성 — 비차단).** Record의 "Item 기록 + Index 갱신 함께 완료"(INV-7)를 Bootstrap(형태 A)에서는 절차 준수 + 완료 후 대조로 보증하고, 강한 원자성 메커니즘은 형태 B 실행 코드 소관으로 미뤘다(§3.1). 형태 B 착수(DP-4 재상정) 시 원자성 메커니즘 확정이 필요하다. 계약(INV-7) 변경은 아니므로 비차단이다.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 두 번째 산출물. 04 §4.1(Memory 바인딩 표 7행)·05 §4.1의 **v0.4 물리 실현 매핑**. 정본 = 04·05 §3·§4 + framework/memory/ 4문서(본 문서는 물리 실현, 재정의 아님 — §0).
- **물리 백엔드(정본, v0.4 시연 M7으로 데이터 실재 — §7 실측):** `framework/adapters/claude/memory-data/` — store/`<id>.json`(item 당 JSON 파일, append-only; 실측 21파일 mi-0001~mi-0021) + index/index.jsonl(Index Entry append-log, `content` 원문 없음; 실측 21라인, store와 1:1). 물리 위치는 Core·specs·docs 밖 Adapter 경계 이하로 확정(§0·§2).
- **§2:** 04 §4.1 표 **7행 전부**를 경로·구조·형식·절차로 매핑(실재/시연 예정 구분).
- **§3:** Record/Recall 물리 절차를 memory-service.md §5.1/§5.2 단계와 **1:1 대응**(단계 번호 표기) — Record = item 파일 쓰기+index line append 정합(INV-7), Recall = index-first(scope 내 대상 Item만 로드, INV-3/INV-4).
- **§4:** `entrypoint` 물리 해소(형태 A 규약/형태 B 실행 코드)·`recall.limit.max`(기본 20) 물리 반영(Manifest 선언→Recall §3.2-5 적용) — runtime-binding.md 교체 지점 관례 동형.
- **§5:** `kind` 3종 직렬화 표기(`lesson`/`best-practice`/`recurrence-judgment` — SP-1)·applicability 매칭 구현(라벨 겹침 — SP-2, 계약 표면은 05 소유)·**라벨 키 물리 표기 정본(§5.4 — `situation`/`stable_id`/`status`/`verdict`/`matched_lesson_id` 5키; "무엇을 투영하는가"는 05 소유, 키 이름·값 형태만 확정)**·재발/승격 물리 기록 위치(동일 store/index, append-only, `kind` 불투명).
- **§6:** 04 §4.2 이식 교체 지점 1~5 + 05 SP-1·SP-2 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 이식 불변(C-1) 재확인.
- **§7:** 실측 대조(r2 직접 실측) — store·index 물리 자산은 **v0.4 시연 M7으로 실재**(store 21·index 21·id 스킴·`kind` 분포·라벨 키가 정본과 일치). 데이터 생성 주체는 시연 Task(docs/v0.4-demo.md), 본 문서(M5)는 구조·형식·표기 정본만 소유(A5 재발 방지 — 실측 후 기록).
- 04·05 계약 재정의 0, Glossary 용어 신설 0, 새 바인딩 계약 창설 0. 구체 AI·환경·형식 토큰은 이 Adapter 경계에서 허용된다(격리 지점).
