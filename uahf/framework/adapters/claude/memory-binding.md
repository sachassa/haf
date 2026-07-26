# framework/adapters/claude/memory-binding — Claude Code Memory Adapter 바인딩

작성일: 2026-07-05
상태: v0.4 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06. 직전 기준선: v0.3 Baseline)
상위 규약: AGENT.md
근거 정본 (계약 요소는 § 포인터로만 인용 — 재정의 0 선언은 §0 1곳):

- specs/04-memory.md — §3.1-A/B Record·Recall 연산 · §3.2-A Memory Item · §3.2-C Memory Index/Index Entry · §3.2-E 저장 구조 · §3.3 INV-1·3·4·5·6·7·8(단일 Port·전량 로드 금지·최소 Context·content 불투명·기록 불변·인덱스 정합·백엔드 비의존) · §4.1 Claude Code Binding 표 7행 · §4.2 이식 교체 지점 1~5.
- specs/05-lessons.md §3·§4.1·§4.2 — 특히 SP-1(레코드 직렬화·저장 위치 = Adapter 소관)·SP-2(적용 조건 매칭 구현 = Adapter 소관). 계약 표면(스키마·매칭 계약·`kind` 값 정체성·labels 투영 규칙)은 05가 소유한다.
- framework/memory/ 4문서(인스턴스 계약 — 본 문서가 물리 실현만 확정) — memory-service.md §3.2·§4.2·§5.1·§5.2·§5.3·§7(프로토콜 단계·Recall 상한 소비 지점·reason 소속·Port) · module-manifest.md(`entrypoint` 추상 참조·`configSchema` `recall.limit.max` 기본 20) · memory-store.md §2·§3·§4·§5 · lessons.md §5.1·§5.2(`kind` 3종·투영 규칙).
- specs/01-runtime.md §3.2-B·§4(Config 병합 Module > Project > Global·Provider 등록·물리 진입점 해소) · specs/00-glossary.md(용어 정본 — 신설 0) · framework/core/structure.md §2·§5·§6(Adapter 경계 = 격리 지점) · framework/adapters/claude/runtime-binding.md §3.2·§3.3(Register/Resolve·Config 물리 소스의 선행 관례) · Active Lesson L-07(상태 서술은 실측 후 기록 — §7 근거) · ROADMAP.md v0.4.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다 — Core 계약을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 04 §3.3 INV-8, 01 §3.2-E 규칙 3), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 허용된다(C-3 비적용 — runtime-binding.md §0 동형). 개정은 Advisor 승인 + §9 이력 기록으로만 이뤄진다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.4 Draft | 최초 작성. `framework/adapters/claude/` 경계의 두 번째 산출물(첫 산출물: runtime-binding.md). 04 §4.1 바인딩 표 7행의 물리 실현 매핑(§2 — Provider·Item 직렬화·Store·Index·Record·Recall·백엔드 격리), 물리 store·index 경로를 `framework/adapters/claude/memory-data/` 이하로 확정·본 문서 정본 선언(§0·§2), Record/Recall 물리 절차의 memory-service.md §5.1/§5.2 1:1 단계 대응(§3), entrypoint 물리 해소·`recall.limit.max`(기본 20) 물리 반영(§4), Lessons `kind` 3종 직렬화 표기·applicability 매칭 구현·재발/승격 물리 기록 위치(§5), 04 §4.2 이식 교체 지점 1~5 대응(§6), 실측 대조 표(§7 — store·index 물리 자산은 현 시점 미존재, 시연 시 생성 예정). 04·05 계약 재정의 0, 동시 작성 시연 절차서(docs/v0.4-demo-procedure.md) 내용 불인용(07 R2). | Worker (Advisor 위임, Task M5) |
| 2026-07-05 | v0.4 Draft (r2) | Advisor 개정 지시 반영 (OQ-M7-1 해소 — 라벨 키 물리 표기 정본 갭 보완). (1) §5.4 신설 — 라벨 키 물리 표기(정본) 표 5키(`situation`/`stable_id`/`status`/`verdict`/`matched_lesson_id`) ↔ 투영 대상 ↔ 값 형태. lessons.md §5.2가 "무엇을 투영하는가"를 소유하고 본 표는 "키 이름·표기"만 확정(계약 표면 재정의 0). 첫 실사용 = v0.4 시연(docs/v0.4-demo.md). (2) 같은 상태 서술 전 지점 전수 갱신 — §5 헤더·도입·§5.2·§5.3 포인터, §6 SP-1 행, §0·§10. (3) §7 실측 대조 전면 갱신 — memory-data/ 실재 반영(직접 실측: store 21파일 mi-0001~mi-0021.json, index.jsonl 21라인; kind lesson 16/best-practice 2/recurrence-judgment 3). 데이터 미생성 전제의 라이브 상태 서술을 실재 반영으로 전건 교체(L-07 실측 후 기록). (4) OQ-M5-1 해소 표기(lessons.md §5.2 r2 투영 규칙 확정 + §5.4). 04·05 계약 재정의 0, 물리 데이터·framework/memory/·demo 파일 무수정. | Worker (Advisor 개정 지시, Task M5 r2) |
| 2026-07-05 | v0.4 Draft (r3) | r1 이력 행 문면 원복 — r2에서 교정했던 M5(r1) 행의 §7 참조 구문·동시 작성 절차서 불인용 문구를 r1 원문 그대로 되돌림. 이력 행은 시점 기록이며 작성 시점에 참인 서술은 stale이 아니다 — §9 append-only 문면 불변(Advisor 판정). "잔존 서술 0건" 재검증은 라이브 본문에만 적용된다. 라이브 본문·§5.4·§7 실측 서술은 무변경. | Worker (Advisor 교정 지시, Task M5 r3) |
| 2026-07-06 | v0.4 Baseline | v0.4 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 재작업 1회 후 재검증, CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 L-07 유지)·삭제 산출물(docs/v0.4-demo*.md 시연 기록) 참조 @cd9247b 앵커 전환. memory-data/ store·index 참조는 append-only 예외(정책 §2)로 유지. 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 2 — 비계약 격리 개정: 재서술·스냅샷·죽은 참조 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/04-memory.md §3·§4, specs/05-lessons.md §3·§4, framework/memory/ 4문서다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(연산·데이터 포맷·불변 규칙·필드·`kind` 값)를 **재정의·확장하지 않는다** — 정본 § 포인터로만 인용한다. **이 재정의 0 선언은 문서 전체에 대해 여기 1곳에서만 선언되며**, 이하 각 절은 이를 반복 선언하지 않고 정본 §만 지목한다.
- **소관 지점.** framework/memory/ 4문서가 "물리 저장·직렬화·백엔드 I/O·물리 진입점 해소·매칭 구현은 Adapter Binding 문서 소관"이라며 미룬 **물리 경로·파일 구조·직렬화 형식·I/O 절차·매칭 알고리즘**이 확정되는 유일한 자리가 이 문서다(memory-service.md §0·§8, memory-store.md §4.2, module-manifest.md §4, lessons.md §5.2, 04 §4.1, 05 §4).
- **격리 지점(C-3 비적용).** Core 경계와 Module 구현 디렉터리(`framework/memory/` 등) 문서 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이어야 하지만(structure.md §5 C-3 확장, 04 §3.3 INV-8), 이 문서는 그 **반대편**이다 — 직렬화 형식명·물리 경로·파일 확장자·세션/턴 토큰의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다.
- **물리 store·index 위치 정본 선언(done 2).** Memory Store·Memory Index의 물리 데이터 위치는 **`framework/adapters/claude/memory-data/`로 확정한다**(Advisor 결정 — Adapter 경계 이하). 이 위치는 Core 경계·`specs/`·`docs/` **밖**이다. **하위 경로·파일 구조·직렬화 형식·I/O 절차의 정본은 §2**이며, 라벨 키 물리 표기의 정본은 §5.4다.
- **창설 금지.** 04 §4.1·05 §4.1 표를 넘어서는 새 바인딩 계약·새 연산·필드·불변 규칙·`kind` 값·reason 코드를 만들지 않는다.
- **하네스 상태 전제(Bootstrap).** 이 하네스는 Bootstrap 상태다(Glossary J-13). Memory Service는 정식 실행 Module이 아니라 규약 문서와 관행으로 실현되며(형태 A), 본 문서의 매핑은 **이미 실재하는 표면**(디렉터리·정의 문서·store/index 데이터 — §7)과 **실행 코드 도입 시 로딩될 지점**(형태 B — 실행 진입점·로더)을 구분한다. `형태 A/B`는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(done 7, L-07) · 용어.** "실재/존재" 주장은 파일 시스템 확인 후에만 기입하며, §7 표는 **재실측으로 참·거짓이 갈리는 불변 주장**만 담는다(계수·byte 스냅샷 불기재 — store/index는 append-only로 증가하므로 계수는 drift다). 용어는 Glossary 정본만 사용한다 — `lesson`·`best-practice`·`recurrence-judgment`는 05가 소유한 `kind` 값(lessons.md §5.1)이고 본 문서는 물리 직렬화 표기만 확정한다(용어 신설 0).

---

## §1. 목적

이 문서는 04 §4.1(Memory Claude Code Binding)과 05 §4.1(Lessons Claude Code Binding)을 이 환경 위의 구체 물리 실현으로 매핑한다. 정본 경계·격리·창설 금지·실측 규율 선언은 §0에 1벌만 둔다.

절별 책임 — §2 04 §4.1 바인딩 표 7행 전건의 물리 경로·구조·형식·I/O 확정(물리 store·index 위치 = `framework/adapters/claude/memory-data/`) · §3 Record·Recall 물리 절차(memory-service.md §5.1·§5.2와 1:1 단계 대응) · §4 `entrypoint` 물리 해소 + `recall.limit.max`(기본 20) 물리 반영 · §5 `kind` 3종 직렬화 표기·applicability 매칭 구현·라벨 키 물리 표기(§5.4 정본)·재발/승격 물리 기록 위치 · §6 04 §4.2 이식 교체 지점 1~5 대응 · §7 상태 서술 실측 대조.

형태 A → 형태 B 전환 시에도 Core Contract 변경은 0이며(structure.md §7 C-1), §6의 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 04 §4.1 바인딩 표 7행 물리 실현 (done 1·2·7)

04 §4.1 Claude Code Binding 표의 **7행 전부**를 물리 표면으로 매핑한다. "04 §4.1 바인딩 (정본 인용)" 열은 정본 표현을 그대로 인용하고, "물리 실현" 열이 본 문서가 확정하는 경로·구조·형식·절차를(상세 절차는 §3~§5 소유), "실재 여부" 열이 물리 실재/형태 A/형태 B를 구분한다(§7).

물리 백엔드 디렉터리 구조(본 문서 정본 — 데이터 실재, §7):

```
framework/adapters/claude/
├─ runtime-binding.md          # 자매 Adapter Binding
├─ memory-binding.md           # 본 문서
└─ memory-data/                # ★ 백엔드 격리 루트 — 실재
   ├─ store/                   #   Memory Store — Memory Item 파일들
   │  └─ <id>.json             #     Memory Item 1건 = 파일 1개 (append-only·불변; id 스킴 `mi-<정렬가능토큰>`)
   └─ index/
      └─ index.jsonl           #   Memory Index — Index Entry append-log (1 line = 1 Index Entry)
```

| # | §3 계약 요소 (정본 §) | 04 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Memory Service Interface (Port) | Memory Service Provider Module. `framework/memory/`에 구현. contract = `MemoryServiceInterface`. Runtime이 Register/Resolve. | Provider의 계약 인스턴스 = framework/memory/memory-service.md, 등록 서술자 = framework/memory/module-manifest.md(실재). 활성화 진입점의 **물리 해소**는 §4 — 이 백엔드(memory-data/)에 대한 Record/Recall 수행. contract `MemoryServiceInterface`는 module-manifest.md `contract` 값과 정합. | 계약 인스턴스·Manifest 실재. 실행 진입점은 형태 B. |
| 2 | Memory Item 직렬화 (§3.2-A) | item 당 파일 또는 append-log 레코드. `content`는 불투명 페이로드로 직렬화. | **item 당 파일**: `memory-data/store/<id>.json` — Memory Item 1건 = JSON 파일 1개. 필드 = memory-store.md §2(정본 04 §3.2-A)의 6필드(`id`/`kind`/`content`/`source`/`timestamp`/`labels`). `content`는 불투명 페이로드로 그대로 직렬화(Adapter가 내부 해석 안 함 — 04 INV-5). 파일명 = `<id>` → id 유일성을 파일명 충돌로 물리 보장. | 형식·경로 구조 확정(정본). 데이터 파일 실재(§7). |
| 3 | Memory Store 물리 저장 (§3.2-E) | 파일 기반 store. 물리 경로·구조는 Adapter 경계 뒤. | `memory-data/store/` 디렉터리. **append-only**(04 INV-6) — 기록된 `<id>.json`은 재작성하지 않는다. 갱신·정정은 새 `<id>.json`(새 Memory Item) 추가로 표현(memory-store.md §4.1). 전량 로드 없음 — store 파일은 Recall이 scope로 한정된 대상만 읽는다(§3.2, 04 INV-3). | 경로 구조 확정(정본). 데이터 실재(§7). |
| 4 | Memory Index 물리 구현 (§3.2-C) | 파일 기반 인덱스. scope 해소는 인덱스 파일 조회로 수행. | `memory-data/index/index.jsonl` — Index Entry append-log(1 line = 1 Index Entry, Record 순서로 append). 각 line 필드 = memory-store.md §3.2(정본 04 §3.2-C)의 6필드(`id`/`kind`/`source`/`timestamp`/`labels`/`digest`). **`content` 원문 없음**(04 INV-4). scope 해소 = index.jsonl line 스캔으로 narrowing 차원(memory-store.md §5 대응) 필터 → 후보 `id` 집합. store 전체 스캔 없음. | 형식·경로 구조 확정(정본). 데이터 실재(§7). |
| 5 | Record 실행 (§3.1-A) | Memory Item 파일 기록 + 인덱스 파일 갱신을 함께 수행(정합 갱신 — INV-7). | store/`<id>.json` 쓰기 + index.jsonl에 대응 Index Entry line append를 **함께 완료**(04 INV-7). 물리 절차·정합 규칙은 §3.1(memory-service.md §5.1 1:1 대응). | 절차 확정(정본). 실행은 시연/형태 B. |
| 6 | Recall 실행 (§3.1-B) | 인덱스 조회로 Index Entry 후보 해소 → scope 내 대상 Item 파일만 읽음. 전량 로드 금지(INV-3/INV-4). | index.jsonl 조회로 scope 해소 → `detail=index`면 매칭 Index Entry만 반환, `detail=full`+scope 한정이면 매칭 `id`의 store/`<id>.json`만 로드. 물리 절차는 §3.2(memory-service.md §5.2 1:1 대응). | 절차 확정(정본). 실행은 시연/형태 B. |
| 7 | 백엔드 격리 | store·index·직렬화·I/O는 `framework/adapters/` 뒤로 격리. Port 앞에서는 백엔드가 보이지 않는다. | store·index·직렬화 형식(JSON/JSONL)·파일 I/O 전부 `framework/adapters/claude/memory-data/`(이 Adapter 경계 뒤)에 격리. 소비자(Agent·Loop·Workflow·Verifier)는 Port(memory-service.md §7) 경유만 하며 이 경로·형식을 참조하지 않는다(04 INV-1·INV-8). | 격리 경계 확정(정본). 격리 뒤 데이터 실재(§7). |

주:

- 위 7행은 04 §4.1 표의 전 행이며, "물리 실현"은 정본 표현을 구체 경로·형식으로 좁힌 것이다(새 바인딩 창설 0 — §0).
- **id 할당 스킴.** Memory Item `id`는 Record가 유일하게 할당하는(04 §3.2-A) 안정·유일 토큰이다. 물리 실현: 파일명 `<id>.json`이 유일성 보장 매체이며(같은 이름 생성 실패 = `DuplicateId`), 사전식 정렬 가능한 형태(`mi-<정렬가능토큰>`)로 index.jsonl의 append 순서(= Record 순서)와 정합시킨다. 정확한 토큰 형태는 Adapter 선택(SP-1, §6)이고 `id`의 안정성·유일성·불변 참조 계약(04 §3.2-A·INV-6)은 유지된다. 순서 기준 자체의 의미(예: 05 `ordering_ref`)는 특화 계약 소관이다.
- **직렬화 형식(JSON/JSONL) = Adapter 선택.** `content`가 kind별 임의 구조의 불투명 페이로드이므로(04 INV-5) 중첩 구조를 담는 자기서술적 형식(JSON)을 store 레코드에, 라인 구분 로그(JSON Lines)를 index에 사용한다. 이 선택은 04 §4.2-1·05 SP-1의 교체 지점이다(§6). store는 평면(flat) 배치이며 샤딩 등 규모 대응은 형태 B/규모 사안으로 미룬다(선취 금지).
- **구조 = 본 문서 정본 / 데이터 = 시연 Task 산출.** memory-data/의 경로·구조·형식은 본 문서가 확정한 정본이고, 실제 데이터 생성은 시연 Task 소관이다(`uahf/docs/v0.4-demo.md@cd9247b` — Task M7 수행 기록). 본 문서는 물리 데이터를 생성하지 않는다.

---

## §3. Record·Recall 물리 실행 절차 — memory-service.md §5.1/§5.2 1:1 대응 (done 3)

memory-service.md §5.1(Record)·§5.2(Recall)의 계약 수준 프로토콜 단계를 이 환경의 물리 파일 연산으로 **단계 번호 1:1** 대응시킨다. 진위 판정 기준은 memory-service.md §5(정본 04 §3.1)이다.

### §3.1 Record 물리 절차 — Item 기록 + Index 갱신 정합 (04 INV-7)

| memory-service.md §5.1 단계 | 물리 실현 (claude 환경) | reason (실패 시) |
|---|---|---|
| **1** — `id` 제외 필수 필드(`kind`·`content`·`source`·`timestamp`) 확인 | store/`<id>.json` 쓰기 **전에** 입력 Memory Item의 필수 4필드 유무를 검사한다. 누락이면 어떤 파일도 쓰지 않고 거부한다. | `SchemaViolation` (Record — 04 §3.1-A) |
| **2** — `id`를 Memory Store에서 유일 할당 | 할당 `id`에 대해 store/`<id>.json`을 **없을 때만 생성**(create-if-absent)한다. 같은 이름 파일이 이미 있으면 유일 할당 실패로 거부한다(파일명 = 유일성 매체). | `DuplicateId` (Record — 04 §3.1-A) |
| **3** — Memory Item 기록 + 대응 Index Entry 생성 **함께 완료** | store/`<id>.json` 쓰기 **직후** index/index.jsonl에 대응 Index Entry line 1개를 append한다. 둘 다 완료해야 Record 성립. 한쪽만 반영된 상태(예: store 파일은 있으나 index line 없음)는 정합 위반이며, store 파일명 집합과 index `id` 집합의 대조로 검출된다. | `IndexInconsistent` (Record, INV-7 — 04 §3.1-A) |
| **4** — Record는 **추가(append)** 만, 기록 불변 | 기록된 `<id>.json`과 index.jsonl의 기존 line은 재작성·삭제하지 않는다. 갱신·정정은 새 `<id>.json`(새 Memory Item, 새 Index Entry line) 추가로 표현한다(04 INV-6, memory-store.md §4.1). | — (불변 위반은 절차상 발생 안 함) |
| **5** — `content` 불투명 페이로드 | `content` 필드는 입력 그대로 JSON 값으로 직렬화한다. Adapter는 `kind`·`content` 내부를 해석·검증하지 않는다(04 INV-5). | — |

- **정합 갱신(INV-7)의 물리 순서와 한계.** 물리 순서는 (item 파일 쓰기) → (index line append)이며 둘 다 존재해야 Record 완료다(단계 3). 형태 A에서 이 "함께 완료"는 절차 준수 + 완료 후 대조(store 파일명 집합 ↔ index `id` 집합)로 보증한다. 더 강한 원자성(임시 파일 후 이름 변경·선기록 마커 등)은 **형태 B 실행 코드 소관**이며, 그 도입 시에도 04 §3.1-A 완료 조건·INV-7 계약 변경은 0이다(structure.md §7 C-1) — 본 문서는 계약을 넘는 메커니즘을 추측·확정하지 않는다. reason 코드의 소속(Record 3종)은 memory-service.md §5.3 표를 따른다.

### §3.2 Recall 물리 절차 — index-first, scope 내 대상 Item만 로드 (04 INV-3/INV-4)

| memory-service.md §5.2 단계 | 물리 실현 (claude 환경) | reason (실패 시) |
|---|---|---|
| **1** — `purpose`·`scope` 존재 확인 | Recall Request에서 `purpose`·`scope` 유무를 먼저 검사한다. 하나라도 없으면 index.jsonl을 **열지 않고** 거부한다. | `MissingPurpose` / `MissingScope` (Recall, INV-2 — 04 §3.1-B) |
| **2** — `scope` bounded 확인 | `scope`가 narrowing 차원(`kind`/`labels`/`timeRange`/`source`) 최소 하나 또는 finite `limit`을 갖는지 검사한다. 없으면(전체 store 겨냥) store·index를 읽지 않고 거부한다. | `UnboundedScope` (Recall, INV-3 — 04 §3.1-B) |
| **3** — `scope`를 Memory Index로 해소 | index/index.jsonl **line만 스캔**하여(각 line은 `content` 원문 없는 경량 서술자) scope narrowing 차원을 memory-store.md §5 대응(`kind`→`kind`, `labels`→`labels`, `timeRange`→`timestamp`, `source`→`source`)으로 필터해 후보 `id` 집합을 얻는다. **store 파일은 아직 읽지 않는다.** 부합 line이 없으면 해소 실패. | `ScopeUnresolvable` (Recall — 04 §3.1-B) |
| **4** — index-first, content는 `detail=full`+scope 한정 시에만 | 기본(`detail=index`)이면 매칭 Index Entry line만 반환하고 store 파일을 읽지 않는다. `detail=full`이 명시되고 scope로 한정된 경우에만 매칭 후보 `id`의 store/`<id>.json`을 **그 대상만** 로드해 Memory Item으로 반환한다(04 INV-4). | — |
| **5** — 반환량 `limit`·시스템 상한 이내, `truncated` 표시 | 반환 후보 수를 요청 `limit`과 시스템 상한(= `recall.limit.max`, 기본 20 — §4)의 더 작은 값으로 절단하고, 절단되면 `truncated=true`로 표시한다. 어떤 경우에도 store 전량을 반환하지 않는다(04 INV-3). | — |

- **최소 Context 우선(INV-4)의 물리 보장.** 단계 3에서 index만 스캔하고 단계 4에서 매칭 대상 store 파일만 로드하므로 `content` 원문은 명시적 `detail=full`+scope 한정에서만 물리적으로 읽힌다. index.jsonl 스캔은 `content` 원문을 담지 않는 경량 서술자 대상이므로 전량 로드가 아니다 — INV-3은 **store(Memory Item content)** 전량 반환 금지이며 경량 index 조회는 그 금지 대상이 아니다.
- 정본 예(memory-service.md §5.2, 04 §8 예1) 정합: `scope = { labels: { task: A }, kind: decision }`·`detail=index`(기본) → 해당 index line만 반환. 특정 `id` 원문 필요 시 `scope = { id }`·`detail=full`로 재Recall → store/`<id>.json` 1개만 로드. 접근은 contract `MemoryServiceInterface`(단일 Port) 경유다.

---

## §4. entrypoint 물리 해소 · `recall.limit.max` 물리 반영 (done 4)

module-manifest.md가 "물리 해소는 Adapter Binding 문서 소관"으로 미룬 두 지점을 확정한다(runtime-binding.md 교체 지점 관례 동형 — 추상 참조 → 물리 실현, 형태 A/B 구분).

### §4.1 `entrypoint` 추상 참조의 물리 해소

module-manifest.md `entrypoint` = "추상 참조 — Record/Recall 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4)". 그 물리 해소:

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Provider Module 활성화 진입 — Record/Recall(memory-service.md §3) 노출 | **형태 A(Bootstrap):** 활성화 진입은 규약으로 실현된다 — Record/Recall은 memory-service.md §5 프로토콜(§3의 물리 절차)에 따라 이 백엔드(`memory-data/`)를 대상으로 수행된다. 별도 실행 진입점 파일은 없다. | 규약 실현(형태 A) |
| 위 진입점의 실행 코드 로케이터 | **형태 B:** Record/Recall을 노출하는 실행 코드가 non-core 실행 경계(`framework/memory/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 `memory-data/` 백엔드에 대해 두 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지). | 형태 B |

- **Register/Resolve 정합(runtime-binding.md §3.2 동형).** 이 Provider의 등록(Register)은 Manifest + 본 바인딩 배치로 규약 실현되며(형태 A), 해소(Resolve)는 소비자가 Port(contract `MemoryServiceInterface`)로 Record/Recall을 호출할 때 이 백엔드로 해소되는 것이다. Memory Service는 Agent가 아니라 Cross-cutting Service이므로 Resolve는 서브에이전트 디스패치가 아니라 **Port 소비 경로**로 실현된다(04 §3.4, memory-service.md §7). 이 등록 경로는 SP-5에 대응한다(§6).

### §4.2 `recall.limit.max`(기본 20)의 물리 반영 — 어디서 읽혀 어떻게 적용되는가

module-manifest.md `configSchema` 키 `recall.limit.max`(유한 양의 정수, 기본 20 — Recall 시스템 상한의 값 원천, Advisor 결정 DP-M1). 그 물리 반영:

| 관점 | 물리 실현 (claude 환경) | 형태 |
|---|---|---|
| **값·기본값 선언 위치** | 스키마+기본값(20) 선언은 Manifest configSchema(framework/memory/module-manifest.md §3, 실재)에 있다 — v0.3 `retry.limit` 기본값이 결정 기록으로 실현된 것과 동형(runtime-binding.md §3.3). | 실재(형태 A 선언) |
| **override 물리 소스** | override는 Config 스코프별 물리 소스에서 온다(runtime-binding.md §3.3 동형): Module 스코프 = 이 Provider Module의 설정 블록(물리 해소는 §4.1 진입점과 함께 형태 B에서), Project 스코프 = `.claude/settings.local.json` 등, Global 스코프 = `~/.claude/settings.json`. 병합은 Module > Project > Global(01 §3.2-B). | Global/Project 소스 실재, Module 소스는 형태 B |
| **읽히는 지점(read)** | Recall 시 읽힌다 — 소비 지점은 memory-service.md §3.2(Recall 완료 조건)·§4.2(Recall Request `limit`). | 규약 실현(형태 A) / 형태 B 로더 |
| **적용 방식(apply)** | Recall 물리 절차 §3.2 **단계 5**에서 적용된다 — 반환 후보 수를 `min(요청 limit, recall.limit.max)`로 절단하고, 요청 `limit` 미지정 시 `recall.limit.max`(기본 20)를 상한으로 적용한다. 절단 시 `truncated=true`. | §3.2-5의 절차 |

- **형태 구분.** Bootstrap에서 이 값은 Manifest configSchema 선언(기본 20)으로 실현(형태 A)되며, 실행 로더(형태 B) 도입 시 effective config(Module > Project > Global 병합)로 로딩되어 Recall이 §3.2-5로 적용한다. 상한의 **존재·의미**(04 §3.1-B) 계약은 불변이고, 본 문서는 값 원천·읽힘·적용의 물리 지점만 바인딩한다.

---

## §5. Lessons `kind` 3종 직렬화 · applicability 매칭 구현 · 라벨 키 물리 표기 · 재발/승격 물리 기록 (done 5)

lessons.md가 "직렬화 표기·매칭 구현·라벨 키 물리 표기·저장 위치는 Adapter 소관"으로 미룬 지점을 확정한다. **계약 표면 소유 = lessons.md·05**(스키마·매칭 계약 표면·`kind` 값 정체성·"무엇을 `labels`에 투영하는가") / **이 절 소유 = 물리 표기·구현·기록 위치**. 이 소유 경계는 여기 1곳에서 선언하고 §5.1~§5.4에서 반복하지 않는다.

### §5.1 `kind` 값 3종 직렬화 표기 (05 §4.2 SP-1 — Adapter 소관)

lessons.md §5.1이 확정한 세 안정 분류자 값의 Memory Item `kind` 필드 직렬화 표기다.

| 특화 기록 (스키마 소유) | `kind` 값 (lessons.md §5.1 소유) | 물리 직렬화 표기 (이 Adapter 확정) |
|---|---|---|
| Lesson (lessons.md §2.1 / 05 §3.2-A) | `lesson` | store/`<id>.json`의 `kind` 필드 값 = 문자열 `"lesson"` (소문자, 구분자 없음) |
| Best Practice (lessons.md §2.2 / 05 §3.2-B) | `best-practice` | `kind` 필드 값 = 문자열 `"best-practice"` (소문자, 하이픈 구분) |
| 재발 판정 레코드 (lessons.md §2.5 / 05 §3.2-E) | `recurrence-judgment` | `kind` 필드 값 = 문자열 `"recurrence-judgment"` (소문자, 하이픈 구분) |

- 세 값은 각 Memory Item의 `kind` 필드에 위 문자열 그대로 직렬화되고 index.jsonl line의 `kind` 필드에도 동일하게 반영된다(scope `kind` 차원 해소용). Memory·Adapter는 이 값을 **불투명 분류자**로만 취급한다(04 INV-5) — `content` 상세 스키마는 05 소유이며 Adapter는 해석하지 않는다.

### §5.2 applicability 매칭 구현 (05 §4.2 SP-2 — 구현은 Adapter, 계약 표면은 05 소유)

lessons.md §5.2: 회수는 Port의 `kind`/`labels` 범위 조회로 후보를 좁힌 뒤 상황 서술자 ↔ `applicability` 최종 대조를 Port 위에서 수행한다. **매칭 계약 표면(질의 파라미터·반환 집합)은 05가 소유하고**(05 §3.2-C, lessons.md §5.2), 매칭 **구현(대조 알고리즘)**을 이 Adapter가 확정한다.

- **1단계 — Port 범위 조회(index 후보 축소).** Recall scope로 index.jsonl을 조회해 후보를 좁힌다(§3.2 단계 3): `kind` 차원 = 회수 대상 종류 구분, `labels` 차원 = applicability가 투영된 `labels`(투영 규칙 = 05 소유)와 상황 서술자의 겹침. 이 단계는 `kind`/`labels`/`timeRange`/`source` 범위 조회만 사용한다(04 §9 결정 기록).
- **2단계 — 좁혀진 후보 위 관련성 산출(매칭 구현).** 상황 서술자와 각 후보 `applicability`의 **라벨 집합 겹침(label-set overlap)**으로 관련성을 산출하고, 겹침이 큰 순으로 정렬해 회수 정책(최소 범위)에 따라 최소 집합만 반환하되 `recall.limit.max`(§4.2)로 상한한다. 매칭 없으면 빈 집합(실패 아님 — 05 §3.1-B).
- **구현 선택임을 명시.** 라벨 집합 겹침(키워드형 대조)은 이 Adapter의 구현 선택이며, 의미 검색·임베딩 등으로의 교체가 SP-2다(§6). 계약 표면과 `applicability` → `labels`/`kind` 투영 규칙은 05·lessons.md §5.2 소유이고, 그 투영에 쓰이는 **물리 라벨 키 이름·값 형태**는 §5.4가 정본으로 확정한다.

### §5.3 재발 판정·승격의 물리 기록 위치 (kind 3종 위에서 일관 서술)

세 특화 기록은 별도 저장 경로를 갖지 않고 **전부 Memory Item의 `kind`로 단일 Port·단일 백엔드 위에 올라탄다**(04 §3.4, lessons.md §5). 물리 기록 위치는 §2와 동일한 store/index 백엔드다.

- **승격(Candidate → Active).** Register Candidate·Promote는 각각 `kind="lesson"`(또는 `"best-practice"`) Memory Item을 **Record**로 기록한다 → store/`<id>.json` + index.jsonl line(§3.1). 기록 불변(04 INV-6)이므로 status 전이(Candidate→Active→Superseded/Retired)는 기존 파일 수정이 아니라 **새 Memory Item 추가**로 표현된다. 안정 `id`·`status`·`supersedes`는 `content`(05 소유, Adapter 불투명)에 담기고, 회수 대조에 필요한 투영은 lessons.md §5.2 투영 규칙에 따라 `labels`/`kind`로 반영된다(물리 라벨 키 = §5.4). **승격 승인 권한(Advisor 전속 — 05 INV-4)은 백엔드 사안이 아니다** — 백엔드는 Record 호출만 기록하고 승인 판정은 05·02 §3.2-A 소관이다.
- **재발 판정.** Judge Recurrence의 산출물은 `kind="recurrence-judgment"` Memory Item으로 **Record**되어 동일 백엔드에 기록된다(§3.1). `verdict`·`matched_lesson_id`(필드 정본 lessons.md §2.5 / 05 §3.2-E)는 index 단계 조회용으로 `labels`에 투영되며 물리 키는 §5.4가 확정한다. 판정 입력인 "작업별 회수 집합"은 **03 루프 상태 기록 소관**이며 이 백엔드가 생성·저장하지 않는다.
- **일관성.** 세 `kind` 값 모두 §2의 동일 물리 규칙(item 당 파일·append-only·index 정합 갱신·index-first 회수)을 따르며, 백엔드가 `kind`를 불투명하게 다루므로(04 INV-5) 저장·색인·회수 절차가 분기되지 않는다. status 생애주기·supersede 의미·승격 권한·최신 Active 해소 규칙은 전부 05 소관이다.

### §5.4 라벨 키 물리 표기 (정본 — 05 §4 SP-1 / lessons.md §5.2 위임)

lessons.md §5.2(r2)와 §5.2는 "무엇을 `labels`에 투영하는가는 05가 소유하고, **라벨 키의 물리 표기(키 이름·값 형태)는 Adapter 소관**"으로 확정했다(05 §4 SP-1). 그 물리 표기의 **정본 자리가 이 절**이며, 아래 5키가 정본이다(첫 실사용 = `uahf/docs/v0.4-demo.md@cd9247b` Task M7 기록).

| 투영 대상 (무엇을 투영하는가 — 소유) | 물리 라벨 키 (이 Adapter 정본) | 값 형태 (실측 근거) |
|---|---|---|
| applicability 상황 유형·트리거 서술 (lessons.md §5.2 소유) | `situation` | 문자열 태그 배열 — 상황 유형·트리거 term 집합 (예 형태 `["<태그>", …]`) |
| Lesson·Best Practice 안정 `id` (lessons.md §5.2 투영; 필드 정본 05 §3.2-A/B) | `stable_id` | 문자열 — 특화 기록의 안정 식별자 |
| Lesson·Best Practice `status` (lessons.md §5.2 투영; 필드 정본 05 §3.2-A/B) | `status` | 문자열 — `Candidate`/`Active`/`Superseded`/`Retired` 중 하나 |
| 재발 판정 레코드 `verdict` (필드 정본 lessons.md §2.5 / 05 §3.2-E) | `verdict` | 문자열 — `Novel`/`RecallGap`/`Recurrence` 중 하나 |
| 재발 판정 레코드 `matched_lesson_id` (필드 정본 lessons.md §2.5 / 05 §3.2-E) | `matched_lesson_id` | 문자열 — 매칭된 Active Lesson 안정 id (`Novel`이면 부재 가능) |

- **소유 경계(계약 표면 침범 0).** "무엇을 투영하는가"(투영 대상·투영 규칙·필드 의미)는 lessons.md §5.2·§2.5·05가 소유한다. **이 표는 그 투영 대상에 대한 물리 라벨 키 이름·값 형태만 확정**한다. 라벨 키 표기 관례(소문자·언더스코어 구분)는 Adapter 선택이며 SP-1에 속한다(§6).
- **물리 위치.** 위 키들은 Memory Item의 `labels`(04 §3.2-A) 아래에 놓이고 Index Entry의 `labels`(04 §3.2-C)에도 그대로 실려 index 단계 후보 축소(§3.2 단계 3)에 쓰인다. `content` 원문 로드 없이 index 단계에서 필터되므로 최소 Context 원칙(04 INV-4, 05 INV-6)과 정합한다.
- **실측 정합(불변).** index.jsonl의 `labels` 키 집합은 이 5키와 정확히 일치한다 — 초과 키 0(§7).

---

## §6. 04 §4.2 이식 교체 지점 1~5 대응 (done 6)

04 §4.2 이식 교체 지점 1~5 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다(05 §4.2 SP-1·SP-2도 겹치는 자리에 병기). "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인한다.

| # (04 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| 1 | Memory Item / Index Entry 직렬화 포맷 | §2 #2·#4, §5.1, §5.4 (05 SP-1) | store `<id>.json`(JSON) 레코드·index.jsonl(JSON Lines) line 포맷, `kind` 값 문자열 표기, 라벨 키 물리 표기(§5.4 — `situation`/`stable_id`/`status`/`verdict`/`matched_lesson_id`). | Memory Item(04 §3.2-A)·Index Entry(04 §3.2-C) 추상 스키마, `kind` 값 정체성(05 소유), labels 투영 규칙(05 §5.2 소유). |
| 2 | Memory Store 물리 저장 | §2 #3, §3.1 | `memory-data/store/` 파일 기반 store(item 당 파일, append-only). | 저장 구조 규칙(04 §3.2-E), append-only·정합 갱신(INV-6/INV-7). |
| 3 | Memory Index 구현 | §2 #4, §3.2 | `memory-data/index/index.jsonl` append-log 인덱스, line 스캔 scope 해소. | Memory Index 계약·scope 해소 대응(04 §3.2-C, memory-store.md §5), 최소 Context(INV-4). |
| 4 | 백엔드 I/O 메커니즘 | §2 #5·#6·#7, §3, §5.2 (05 SP-2) | 파일 I/O(create-if-absent·append·line 스캔·대상 파일 로드), applicability 매칭 대조 알고리즘(라벨 겹침). | Record/Recall 시그니처·회수 정책(04 §3.1), 매칭 계약 표면(05 §3.2-C 소유). |
| 5 | Provider Module 등록 경로 | §2 #1, §4.1 | Manifest + 본 바인딩 배치(형태 A)·형태 B 실행 진입점 로케이터. Runtime 이식 시 함께 교체(01 §4.2). | contract `MemoryServiceInterface`, Provider 등록·해소 계약(01 §3.1-A·§4, module-manifest.md). Memory는 참조만. |

- "유지되는 것" 열의 계약(04 §3 Core Contract·framework/memory/ 인스턴스·05 계약 표면)은 다른 AI·저장 환경으로 이식해도 바뀌지 않는다(structure.md §7 C-1). 이 목록의 Adapter Interface 정식화는 specs/11-adapters.md 소관이며 본 문서는 선취하지 않는다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 7 — A5 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 본 문서의 "실재" 서술을 파일 시스템과 직접 대조한다. **계수·byte 스냅샷은 두지 않는다** — store·index는 append-only로 계속 증가하므로 파일 수·라인 수·byte는 drift이며, 대신 **재실측으로 참·거짓이 갈리는 불변 주장**만 남긴다(2026-07-26 슬림화에서 종전 판의 시점 계수·byte·kind 분포 제거).

| 대상 | 실측 판정 (재실측 대상) |
|---|---|
| `framework/adapters/claude/` 경계 · runtime-binding.md(자매) · memory-binding.md(본 문서) | 실재. |
| framework/memory/ 4문서(memory-service·module-manifest·memory-store·lessons) | 실재 — 4파일 전건(§ 포인터 대상, 무수정). |
| `framework/adapters/claude/memory-data/` (백엔드 루트) | 실재 — `store/`·`index/` 2하위. |
| **store ↔ index 1:1 정합 (04 INV-7)** | **성립** — `store/*.json` 파일명 집합과 `index/index.jsonl`의 `id` 집합이 **정확히 동일**(차집합 양방향 0). 계수는 기재하지 않는다(append-only 증가). `uaf-verified: store 디렉터리 전수 열거 + index.jsonl 전 라인 파싱 후 id 집합 양방향 비교` |
| **index Entry에 `content` 원문 없음 (04 INV-4)** | **성립** — index.jsonl 전 라인에 `content` 필드 부재. `uaf-verified: index.jsonl 전 라인 JSON 파싱 후 content 키 존재 검사` |
| store/index `kind` 값 (§5.1) | `lesson`·`best-practice`·`recurrence-judgment` **3종 전부 사용 중이며 그 밖의 값 0**. 종별 분포 계수는 기재하지 않는다(drift). `uaf-verified: index.jsonl 전 라인 kind 값 집계` |
| index `labels` 라벨 키 (§5.4) | §5.4 정본 5키(`situation`·`stable_id`·`status`·`verdict`·`matched_lesson_id`)와 **정확히 일치 — 초과 키 0**. `uaf-verified: index.jsonl 전 라인 labels 키 집계 후 §5.4 표와 대조` |
| id 스킴 (§2 주) | 성립 — `mi-<정렬가능토큰>` 형태이며 사전식 정렬 순서가 index append 순서와 정합한다. |
| Manifest configSchema `recall.limit.max` = 20 | 실재 — framework/memory/module-manifest.md §3 configSchema 표 선언(형태 A). |
| 실행 진입점·실행 로더(형태 B) | 미도입 — Bootstrap 상태(형태 A). |

- **핵심 구분.** 본 문서가 확정한 물리 store·index의 **경로·파일 구조·직렬화 형식·I/O 절차·라벨 키 표기(§5.4)는 정본**이며, 데이터 생성 주체는 시연 Task(`uahf/docs/v0.4-demo.md@cd9247b` — Task M7)다. 위 표의 판정은 전부 파일 시스템·데이터 직접 실측이며, 실재를 주장하는 행은 실측 후에만 기입한다(A5/L-07 재발 방지).

---

## §8. 정본 경계·격리·계약 소유 (self-note — 1줄 + 소유 지도)

- **재정의 0·창설 0·격리 선언은 §0이 1벌로 소유한다.** 이 절은 그 선언을 반복하지 않고 계약 소유 지도만 둔다.
- **계약 소유 지도.** Record/Recall 완료 조건·reason = 04 §3.1 / memory-service.md §5.3 · Memory Item·Index Entry·저장 구조 = 04 §3.2-A/C/E · 불변 규칙 = 04 §3.3 · Config 병합 = 01 §3.2-B · Provider 등록·해소 = 01 §3.1-A·§4 · Lesson·Best Practice·재발 판정 스키마·`kind` 값 정체성·매칭 계약 표면·labels 투영 규칙·status 생애주기·supersede·승격 권한 = 05 / lessons.md. 본 문서가 소유하는 정본은 **물리 경로·파일 구조·직렬화 형식·I/O 절차(§2·§3)·물리 해소·값 반영(§4)·직렬화 표기·매칭 구현·라벨 키 물리 표기(§5)** 뿐이다.
- **작성 경계 이력(포인터).** 초판(Task M5)의 동시 작성 산출물 불인용(07 R2)·1파일 생성 범위(07 R4)·r2/r3 개정 경위 감사 흔적은 §9 이력 행에 보존되어 있다. `uaf-allow-legacy: 초판·r2·r3 감사 흔적은 §9 이력 표에 보존, 본문은 포인터 1줄`

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-M5-1 (05 조율) — 해소(v0.4 r2).** lessons.md §5.2 r2가 투영 규칙(안정 식별·상태 투영·최신 `timestamp` = 현재 상태)을 확정하고 라벨 키 물리 표기를 Adapter에 위임했으며, 그 5키는 §5.4가 정본으로 확정했다. 계약 표면은 05 소유·본 문서는 키 이름·값 형태만 확정 — 침범 0, 잔여 없음. 경위는 §9 r2 행.
- **OQ-M5-2 (원자성 — 비차단).** Record의 "Item 기록 + Index 갱신 함께 완료"(INV-7)는 형태 A에서 절차 준수 + 완료 후 대조로 보증하고, 강한 원자성 메커니즘은 형태 B 실행 코드 소관으로 미뤘다(§3.1). 형태 B 착수 시 확정 대상이며 계약(INV-7) 변경이 아니므로 비차단이다.

---

## §10. 요약 (1줄)

- 이 문서 = 04 §4.1(Memory 바인딩 표 7행)·05 §4.1의 물리 실현 매핑이며, 물리 백엔드 정본은 `framework/adapters/claude/memory-data/`(store/`<id>.json` + index/index.jsonl)다 — 절 지도는 §1, 정본 경계는 §0, 상태는 §7이 소유하며 여기서 재서술하지 않는다.
