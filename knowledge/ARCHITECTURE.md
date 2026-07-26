# knowledge — Architecture (횡단 공용 Knowledge Base)

작성일: 2026-07-12
상태: v1.3 정합 · 완전 저술 (스텁 대체)
상위 규약: 루트 `ARCHITECTURE.md` (라우터) · `AGENT.md`
근거 정본 (각 § 포인터로만 참조 — 재정의·복제 0):

- 루트 `ARCHITECTURE.md` (라우터) — knowledge 횡단 공용 Knowledge Base의 **상위 정본**. 특히 §4·§2.1·§6 원칙 10·§10·§11·§12.1.
- `uahf/ARCHITECTURE.md` §5.1 — UAHF 내부 Cross-cutting **Memory Service**(단일 Port). knowledge와의 결합 상세의 UAHF 측 정본 (UAF-INV ①).
- (하위 spec 없음 — 1차 정본 선언.) knowledge는 `<layer>/specs/` 하위 정본을 두지 않으므로 **이 문서가 knowledge 구조의 1차 정본**이다.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **개관 고도 · 1차 정본.** 이 문서는 루트 `ARCHITECTURE.md` §4가 선언한 knowledge 횡단 공용 Knowledge Base의 **내부 구조 개관**이며, `<layer>/specs/` 하위 정본이 없으므로 knowledge 구조의 **1차 정본**이다 — 상위 정본(루트 §4)이 위상을 선언하고 이 문서가 그 아래에서 표면 구조·Consult 위상을 확정한다. 접점 원칙(UAF-INV ①)·Core 문서 관행(특정 AI·모델·제품 기능명 0)은 루트 §0·§8을 그대로 따르며 여기서 재서술하지 않는다. (`graphrag`·`retrieval`·`prompts` 등은 일반 표면·기법 명칭이지 제품명이 아니다.)
- **횡단 Base · 파이프라인 단계 아님 · 원천 위임.** knowledge는 UAF 6요소 파이프라인의 한 단계가 아니라 모든 Layer가 Consult하는 횡단 공용 Base이며 payload를 흘려보내지 않는다(루트 §4·§2.1 — 3메커니즘 구분은 §3). 8표면의 실제 원천과 완전 구성(스키마·색인·회수 알고리즘·프롬프트 자산)은 **후속 트랙 소관**이다(§4).

---

## §1. 목적 (Purpose)

knowledge Base는 UAF 최상위 Layer들(Entry·Discovery·Planning·UAHF 및 그 Execution) **모두가 Consult하는 UAF 레벨 횡단 공용 지식 Base**다. 장기 공유 지식(Lessons·패턴·용어 등)을 표면 구조로 담고, 어느 Layer든 결정을 뒷받침할 지식을 회수(Consult)하게 한다 (루트 §4·§6 원칙 10). knowledge는 파이프라인 단계가 아니므로 payload를 흘려보내지 않는다.

이 문서는 knowledge 구조의 **1차 정본**으로서, 내부 8표면의 역할과 Consult 위상을 개관 고도로 확정한다. 각 표면의 원천·완전 구성은 후속 트랙이 소유한다 (§4).

---

## §2. knowledge 내부 구조 — 8표면 역할 확정 (1차 정본 + 실측)

knowledge Base의 내부는 8개 표면(surface)으로 구성된다. 아래는 각 표면의 역할을 **1차 정본**으로 개관 확정한 것이며(각 1~2문장), 표면의 원천·구성 상세는 창설하지 않는다(후속 위임, §4).

- **`markdown/`** — 사람이 읽고 쓰는 **1차 문서 표면**. 장기 공유 지식(Lessons·결정 기록·서술형 지식)을 마크다운 문서 형태로 담는 가독 표면이다.
- **`metadata/`** — 지식 항목의 **구조화 메타데이터 표면**. 태그·출처·시점·색인 등 속성을 담아 회수·필터·라우팅의 근거가 되는 속성 계층이다.
- **`graph/`** — 지식 항목 간 관계를 개체·관계(entity·relation)의 **그래프 구조로 표현하는 표면**. 항목 간 연결과 구조적 탐색의 기반이다.
- **`graphrag/`** — 그래프 구조를 회수에 결합하는 **그래프 증강 회수 표면**(graph + retrieval 기법). `graph/` 표면 위에 구조 인지 회수를 얹는 표면이다.
- **`retrieval/`** — Consult 질의가 관련 지식을 찾아오는 **회수 메커니즘 표면**(질의·순위·선별). 어떤 지식을 얼마나 가져올지의 회수 축이다.
- **`prompts/`** — Consult·회수 시 재사용되는 **프롬프트 자산 표면**(질의 구성·컨텍스트 주입 템플릿). 지식을 표면화하는 재사용 자산 계층이다.
- **`patterns/`** — 재사용 가능한 설계 패턴·모범 사례(Best Practice 후보)를 정제해 담는 **패턴 표면**. 반복 해법의 증류다.
- **`glossary/`** — knowledge Base 전반에서 참조되는 **공유 용어·정의 표면**. 용어의 일관된 정의 계층이다 (UAF 상위 용어 정본은 루트 §12·`uahf/specs/00-glossary.md`이며, 이 표면은 knowledge Base 내부 용어 자산 소관이다).

- **실측 — 8표면 상태 (2026-07-26 파일 시스템 직접 확인).** 위 8표면은 전부 디렉터리로 **실재하나, 각 디렉터리에는 `.gitkeep` 하나만 있고 콘텐츠는 없다** — 즉 현재는 **자리 스캐폴드(빈 스캐폴드)**다. `uaf-verified: knowledge/ 하위 8표면 디렉터리를 각각 ls -A로 열거해 .gitkeep 단일 엔트리를 확인 · 검색 범위 = knowledge/ 1단계 하위 디렉터리.` 각 표면의 실제 원천 채움·구성은 후속 트랙 소관이며(§4), 본 문서는 없는 콘텐츠를 실재로 서술하지 않는다.
- **Layer 디렉터리 구성.** `knowledge/ARCHITECTURE.md`(본 문서·1차 정본) · `knowledge/README.md`·`knowledge/ROADMAP.md`(Base 소개·로드맵) · `knowledge/.claude/README.md`(override 설정 표면 명찰; 현재 override 없음 — 루트 §5) · `knowledge/{markdown,metadata,graph,graphrag,retrieval,prompts,patterns,glossary}/`(8표면).

---

## §3. Consult 계약 (횡단)

- **Consult 위상 (횡단).** knowledge는 루트 §2.2 파이프라인 6요소 순서에 들어가지 않는다. Entry·Discovery·Planning·UAHF·Execution 어느 Layer든 필요 시 knowledge를 회수(Consult)하되, knowledge는 파이프라인 payload를 앞뒤 Layer로 흘려보내지 않는다(파이프가 아님) (루트 §4·§2.1·§6 원칙 10).

```
knowledge ◀──Consult── 모든 Layer   (횡단 — 파이프라인 파이프 아님)
```

- **3메커니즘 구분 (혼동 금지).** **(a) knowledge = 공유 지식(횡단 Consult)** — 모든 Layer가 회수하는 공용 Base이며 방향은 Consult, 파이프라인 축이 아니다(본 문서 소관). **(b) Layer 연결 계약 = 파이프(파이프라인 축)** — Discovery Request·Project Contract처럼 앞 Layer의 출력이 뒤 Layer의 입력이 되는 데이터 계약이다(루트 §3). **(c) session handoff = 시간축 연속** — 공간축 횡단(a)도 파이프라인축(b)도 아니다.
- **UAHF Memory Service와의 관계 (§ 포인터만).** UAHF 내부 6-Layer를 관통하는 Cross-cutting **Memory Service**(단일 Port, `uahf/ARCHITECTURE.md` §5.1)와 UAF 레벨 최상위 Layer 횡단 `knowledge/` Base는 별개 네임스페이스의 횡단 구조다. 둘의 결합 상세(회수 경로·백엔드 공유 여부)는 UAHF 정본(§5.1)과 본 문서의 **후속 소관**이며, 여기서는 위상만 선언하고 재정의하지 않는다(재정의 0).

---

## §4. 원천·구성 위임 경계

- **역할까지 확정 · 원천 채움은 위임.** 본 문서는 8표면 각각의 **역할(1차 정본)까지** 확정한다(§2). 각 표면의 실제 **원천**(어떤 지식이 어떤 형식으로 담기는가)과 **완전 구성**(원천 스키마·색인 규칙·회수 알고리즘·프롬프트 자산·그래프 적재 규칙 등)은 확정하지 않으며, **후속 트랙 소관**이다. 근거 = 8표면이 현재 빈 스캐폴드라는 §2 실측.
- **선취 금지.** 본 문서는 후속 트랙 소관인 원천 스키마·구성 규칙을 **선취해 창설하지 않는다**. 개관 고도를 넘어 표면 구현 상세를 정의하는 서술을 두지 않는다.

---

## §5. 불변 — 개관

knowledge에는 고유 spec이 없으므로 **knowledge 고유 불변을 임의로 명명하지 않는다.** knowledge가 구속받는 상위 원칙·불변의 문면 정본은 루트 §6 원칙 10(Knowledge Consult 횡단) · 루트 §4(횡단 Base 위상) · 루트 §11·§10 비담당 ④(Memory 설계 제외 — `uahf/ARCHITECTURE.md` §5.1 소관) · 루트 §8 UAF-INV ①(접점 원칙)이 소유한다 — 여기서 복제하지 않는다.

---

## §6. 경계 · Non-Goals (Layer 관점)

knowledge Base의 비수행·비설계 경계(파이프라인 단계 수행 · Memory 기록/회수 엔진 설계 · 8표면 원천·구성 설계 · 물리 실현)는 상위·타 정본과 후속 트랙이 소유한다 — 정본 = 루트 §11 Non-Goals · 루트 §10 비담당 ④ · `uahf/ARCHITECTURE.md` §5.1 · 루트 §3·§4(파이프 vs 횡단) · 본 문서 §4(원천·구성 위임)·§0(Core 문서 관행).

---

## §7. 정본 포인터 표 (Routing)

값을 하드코딩하지 않고 정본 위치로만 라우팅한다.

| 항목 | 정본 |
|---|---|
| knowledge 횡단 공용 Knowledge Base (상위 정본) | 루트 `ARCHITECTURE.md` §4 |
| 최상위 Layer 지도 · Knowledge Base 귀속(파이프라인 단계 아님) | 루트 `ARCHITECTURE.md` §2.1 |
| Knowledge Consult 원칙(횡단) | 루트 `ARCHITECTURE.md` §6 원칙 10 |
| 책임 경계표 · Memory Consult 비담당 ④ · Non-Goals | 루트 `ARCHITECTURE.md` §10 · §11 |
| Layer 연결 계약(Discovery Request · Project Contract — 파이프) | 루트 `ARCHITECTURE.md` §3 |
| Knowledge Base 용어 · UAF 상위 용어 | 루트 `ARCHITECTURE.md` §12 · §12.1 |
| UAHF 내부 Cross-cutting Memory Service(단일 Port) | `uahf/ARCHITECTURE.md` §5.1 |
| `.claude` Global Default / override 경계 | 루트 `ARCHITECTURE.md` §5 |
| knowledge 8표면 역할(1차 정본) | 본 문서 §2 |
| 8표면 원천·구성(후속 위임 — 하위 spec 없음) | 후속 트랙 (knowledge는 `<layer>/specs/` 하위 정본을 두지 않는다) |
| 상위 규약 | `AGENT.md` |
