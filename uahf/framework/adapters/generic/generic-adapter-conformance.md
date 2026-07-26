# framework/adapters/generic/generic-adapter-conformance — Generic Adapter 적합성(Conformance) 판정

작성일: 2026-07-06
상태: v1.0 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-07)
상위 규약: AGENT.md
근거 정본 (계약은 § 포인터로만 인용 — 재정의 0 선언은 §0 1곳):

- specs/11-adapters.md **(Frozen v0.1)** §3.1(Judge Conformance C1~C3)·§3.2-A(BP-1~17 목록)·§3.2-B(Valid(Full)/Valid(Minimal)·최소 바인딩 부분집합·최소 구현 Adapter 정의)·§3.2-C·§3.2-D(Conformance Report 6필드)·§3.3(INV-1~8)·§7·§8 예1·예2 — 본 문서가 판정하는 계약의 정본.
- framework/adapters/generic/generic-binding.md(T1 확정본) §2(필수 13 BP 환경 중립 값 표)·§3(선택 4 BP 생략)·§4(DP-V1·DP-V5·DP-V6) — C1 커버리지 대조의 근거.
- `uahf/docs/v1.0-generic-adapter-demo.md@cd9247b` + `uahf/docs/v1.0-generic-demo-fixtures/@cd9247b` — 핵심 루프 1사이클 실수행 기록(4전이 append-only·독립 Verifier final_verdict=Pass·필수 13 BP↔실증 지점 매핑). **C3 판정 근거의 정본**(evidence 등급 아카이브; 열람 = `git show cd9247b:uahf/docs/v1.0-generic-adapter-demo.md`). 본문의 시연 문서·픽스처 참조는 전부 이 앵커 시점 스냅샷이다.
- framework/core/structure.md §2·§5(C2 판정 근거) · specs/00-glossary.md §3.2(용어 정본·`형태 A/B` 라벨, 신설 0) · AGENT.md · docs/delegation-protocol.md §2 · ROADMAP.md v1.0.
거버넌스: 이 문서는 `framework/adapters/generic/` 소속 **Adapter Binding 문서(Conformance 판정)**다. Adapter 경계는 격리 지점이나(structure.md §2·§5, 11 §3.3 INV-3), 본 문서는 **Generic Adapter** 이므로 DP-V6 정체성 제약(특정 AI 이름·모델명·AI 벤더 제품/기능명 **0건**)과 DP-V14(타 Adapter 경계 문서·경로 불명명 — 역할 기반 중립 참조만)를 받는다(§0). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 Frozen specs/11-adapters.md §3(§3.1 Judge Conformance·§3.2-A 바인딩 지점 목록·§3.2-B 적합성 기준·§3.2-C 구조 규격·§3.2-D Conformance Report·§3.3 Invariants)다.** 이 문서는 그 계약의 **판정 인스턴스**(C1~C3 대조 + Report 산출)이며 계약 요소(바인딩 지점 정의·판정 조건·Report 필드·verdict 값·등급 기준·불변 규칙)를 **재정의·확장하지 않는다** — **이 재정의 0 선언은 문서 전체에 대해 여기 1곳에서만 두며**, 이하 각 절은 반복 없이 11 §만 지목한다.
- **본 문서는 판정 자리다.** generic-binding.md(§0 판정 미산출·선취 금지)가 최소 바인딩 부분집합의 환경 중립 값만 확정한 반면, 본 문서는 그 확정 값(generic-binding.md §2)과 핵심 루프 실증(시연 기록 @cd9247b)을 입력으로 **C1~C3 을 대조하고 verdict 를 산출**한다(11 §3.1 Judge Conformance 의 출력 인스턴스).
- **BP 사실의 단일 소재.** 필수/선택 BP 의 구성 사실(필수 13 = BP-1·2·3·4·5·7·8·9·10·11·13·14·15 / 선택 4 = BP-6·12·16·17)은 정본이 11 §3.2-A·§3.2-B 이고, 본 문서에서의 전건 열거는 **§2.1 표 1벌**뿐이다. §3 Report·§3.1 등급·§5 self-note 는 그 표를 가리키며 재열거하지 않는다.
- **DP-V6 정체성 제약(본문 특정 AI/모델/벤더 제품명 0건).** Generic Adapter 이므로 일반적으로 Adapter 경계에 허용되는 구체 환경 토큰을 본문에 두지 않는다(generic-binding.md §4 DP-V6). 이는 structure.md §5 C-3 의무(Core 경계 대상)가 아니라 **generic Adapter 의 정체성 제약**이다. 개방 표준 포맷명·"파일"·"디렉터리"·"텍스트"·"실행 세션"·"실행 주체" 등 중립 메커니즘 표기와 UAHF 계약 용어(Glossary 정본)는 제약 대상이 아니다.
- **DP-V14 타 Adapter 경로 불명명.** 타 Adapter 경계 문서·경로를 본문에 명명하지 않고 **역할 기반 중립 참조**("첫 번째 Adapter" 등)만 쓴다. docs/ 소속 문서 경로·Core 경계 경로·spec 경로·본 Adapter 자신의 경계 경로 인용은 허용된다.
- **창설 금지.** 11 §3.2-A 17개를 넘어서는 새 BP, 11 §3.2-D 6필드를 넘어서는 새 Report 필드, 11 §3.2-B 의 `Valid(Full)`/`Valid(Minimal)`/`Invalid` 를 넘어서는 새 verdict 값·새 등급·새 용어를 만들지 않는다. 기준의 소유자는 11 §3 이고 본 문서는 인스턴스 판정만 낸다.
- **판정 성격(최종 승인 아님).** 규칙 정본은 §3.2 — 여기서는 그 존재만 지목한다(CP2 Verifier 독립 판정·CP3 Advisor 최종 승인이 후속).
- **하네스 상태·실측 규율.** Bootstrap 상태(Glossary J-13)에서 다수 바인딩 지점은 환경 중립 규약(형태 A)으로 실현되며 C3 는 실동작 사이클로 실증됐다(§2.3). "실재/존재/미존재" 주장은 파일 시스템 확인 후에만 기입한다(L-07, §4).

---

## §1. 목적

이 문서는 Frozen specs/11 의 Adapter Interface(§3.2-A)와 적합성 기준(§3.1 C1~C3)을 **Generic Adapter** 위에 대조해 **완전성·불변·루프 통과를 판정**하고, 그 결과를 11 §3.2-D 6필드 Conformance Report 로 산출한다(11 §1·§3.1). 정본 경계·창설 금지·판정 성격·DP-V6/DP-V14 선언은 §0에 1벌만 둔다.

절별 책임 — §2 C1~C3 검사 근거(대조 + 실측·§ 포인터) · §3 Conformance Report 6필드 산출(verdict = **Valid(Minimal)**) + 등급 판정·판정 성격 재확인 · §4 상태 서술 실측 대조 · §5 self-note·verify_basis.

---

## §2. C1~C3 검사 근거 (done 2)

11 §3.1 Judge Conformance의 완료 조건 C1·C2·C3을 각각 대조한다. 각 근거는 실측 또는 § 포인터이며, 판정 기준(C1~C3의 정의)은 11 §3.1이 소유한다(재정의 0).

### §2.1 C1 — 필수 바인딩 완전성 (11 §3.1)

11 §3.1 C1 은 "§3.2-A에서 필수(mandatory)로 표시된 모든 바인딩 지점을 제공한다"를 요구한다. 최소 구현 Adapter 의 판정 대상 필수 부분집합은 11 §3.2-B 가 소유하는 **최소 바인딩 부분집합(필수 13개)**이며, 그 전건 열거는 본 문서에서 아래 표 1벌뿐이다(§0 BP 사실의 단일 소재).

Generic Adapter 는 필수 13개 전건에 환경 중립 바인딩 값을 확정했고(generic-binding.md §2), 각 값은 핵심 루프 실수행에서 실증 지점을 가진다(시연 기록 §4 @cd9247b). 아래가 그 전건 대조다 — 13행 전건, 누락(missing) 0.

| BP (필수) | 무엇을 바인딩하는가 (11 §3.2-A 정본 인용) | 환경 중립 바인딩 값 (generic-binding.md §2) | 핵심 루프 실증 지점 (demo §4) |
|---|---|---|---|
| BP-1 | Module/Plugin Manifest를 대상 환경의 서술자 포맷으로 직렬화 | 서술자 필드를 담는 일반 구조화 텍스트 파일(머리말 메타데이터 블록 + 본문) | Module Manifest 실물(머리말 메타데이터 블록 + 본문 구조화 텍스트) |
| BP-2 | Module 정의를 로드해 entrypoint를 해소하는 로더 | 파일 시스템 경로 규약으로 역할 활성 정의 파일을 읽어 entrypoint 해소하는 로드 절차 | ② 구현 착수 시 Manifest entrypoint 로드로 Worker 역할 정의 해소 |
| BP-3 | Global/Project/Module 스코프 Config의 물리 소스·위치·로딩 메커니즘 | 파일 시스템 상 3계층 설정 소스(전역/프로젝트/역할 정의 내 설정 블록)·우선순위 병합 | 전역 Config + 프로젝트 Config + 역할 정의 머리말 설정 블록 |
| BP-4 | Bootstrap~Serve~Shutdown 구간을 담는 실행 프로세스/세션 | 일반 실행 세션 — 개시~수행~종료 구간을 담는 하나의 실행 컨테이너 | 시연 사이클을 담은 하나의 실행 세션이 개시~수행~종료 완주 |
| BP-5 | Adapter 산출물과 Core를 물리적으로 분리하는 디렉터리·배치 규약 | Core 디렉터리(`framework/core/`·`framework/runtime/`)와 Adapter 산출물 디렉터리(`framework/adapters/generic/`)를 물리 비중첩 배치 | 시연 픽스처 경계가 Core 디렉터리와 물리 비중첩·자기완결 격리 |
| BP-7 | Advisor/Planner/Worker/Verifier 4역할 정의를 대상 환경 메커니즘으로 제공 | 역할 정의 디렉터리 아래 역할별 정의 문서(텍스트 파일 4종) | 역할 정의 4종 — 각 02 §3.2-A 역할 경계 § 포인터 인용 |
| BP-8 | 공통 규약·시스템 프롬프트·오케스트레이터 진입점 주입 방식 | 상위 규약 문서 + 진입점 문서를 실행 주체에 로드·주입 | 공통 규약 문서 + 진입점 문서를 ② 구현 착수 시 로드·주입 |
| BP-9 | 각 Agent 역할의 실행 모델·엔진 지정 | 임의 실행 주체(any executor) — 역할 정의 문서를 준수하는 어떤 실행 주체든 가능(특정 엔진·모델 불강제) | 역할 정의 머리말 `executor: 임의 실행 주체` — 특정 엔진·모델 불강제 |
| BP-10 | 위임 메시지를 Agent에 전달하는 호출·오케스트레이션 채널 | 파일 기반 위임 메시지 — 위임 메시지(02 §3.2-B 8필드) 텍스트 파일을 읽어 착수 | 위임 채널 실물에 8필드 위임 문면 기입 → 대상 실행 주체가 읽어 착수 |
| BP-11 | 완료 보고·실패 보고를 반환하는 결과 채널 | 파일 기반 보고 채널 — 완료/실패 보고(02 §3.2-C/D) 텍스트 파일 반환·회수 | 완료 보고 파일(02 §3.2-C 5필드) 반환 |
| BP-13 | 구조화된 계약 산출물·상태 기록의 직렬화 및 작업 추적·결정 기록 메커니즘 | 계약 산출물·상태 기록을 구조화 텍스트 파일로 직렬화·추적(append-only) | 사이클 기록(4전이 append-only) + 검증 리포트 + 승인 기록 |
| BP-14 | 사람에게 승인·개입 요청을 제시하고 응답을 받는 채널 | 사람 사용자 승인·개입 채널 + 규약 문서 "충돌 시 사람 보고" 규칙(03 §3.1-D 바인딩) | 진입점 문서의 "Architecture/Spec 충돌 시 사람에게 보고" 규칙 실물 |
| BP-15 | 검증에 쓰이는 검사 도구 (존재 확인·전수 스캔·시연 실행) | 일반 검사 도구 표면 — 파일 존재 확인·텍스트 전수 스캔·시연(명령) 실행 | ③ 검증 — 독립 Verifier가 파일 조회·텍스트 검색으로 판정 |

- **판정: `missing_bindings` = 없음.** 필수 13개 전건이 환경 중립 바인딩 값(generic-binding.md §2)을 갖고 각 값이 핵심 루프 실수행에서 실증 지점(시연 기록 §4 — 13행 전건·누락 0)을 가진다. 누락된 필수 바인딩 0건 → C1 충족(11 INV-2 필수 완전성).
- **선택 바인딩은 C1 대상이 아니다.** C1 은 필수 바인딩의 완전성만 요구하고, 선택 4개는 11 §3.2-A·§3.2-B 가 **선택(optional)**으로 지정한 지점이므로 최소 구현 Adapter 는 생략할 수 있다(generic-binding.md §3). 이 생략은 §3 notes 에 기록되며 C1 판정을 침해하지 않는다.

### §2.2 C2 — Core Contract 불변 (11 §3.1)

11 §3.1 C2는 "Core Contract 수정 0건 — Adapter는 바인딩만 추가하고 어떤 Core Contract도 수정·확장·삭제하지 않는다"를 요구한다.

근거:

- **(a) Core 경계 문서 AI 의존 요소 0건 — 직접 실측(전수 스캔).** Core 경계인 `framework/core/`·`framework/runtime/` **전 문서**를 대상으로 후보 집합 전체를 대소문자 무시로 전수 스캔했다. 후보 집합(카테고리) = (a) 특정 대화형 AI 제품명 (b) 특정 모델 계열명 (c) AI 벤더명 (d) 특정 하위 실행 단위 기능명·설정 디렉터리 제품 표기 (e) 특정 프로그래밍 언어명·툴체인명·직렬화 형식명. **다섯 카테고리 전건 instance 토큰 0건**(structure.md §5 C-3, 01 §3.3 INV-4) — 단일 대리 지표 하나로 결론짓지 않았다(06 §3.1 V4). 이 카테고리 목록이 본 문서의 스캔 범위 정의 1벌이며 §5 는 이를 가리킨다. `uaf-verified: Core 경계 두 디렉터리 전 문서 대상 5카테고리 다중 토큰 스캔 — 문서 계수는 drift 이므로 불기재`
- **(b) Generic 경계가 Core 무침범.** Generic Adapter 의 산출물(본 경계의 바인딩 문서·판정 문서와 docs/ 소속 시연 기록·픽스처)은 전부 Core 경계 밖에 물리 격리되어 있고(structure.md §2·§3 규칙 3, 11 §3.3 INV-3), 어떤 Core Contract 문서도 수정·확장·삭제하지 않는다 — 바인딩 값만 자신의 경계 안에 추가한다.
- **판정: `core_modifications` = 없음.** (a) + (b) → 어떤 Core Contract 도 수정되지 않았다. C2 충족(11 INV-1 Core 불변).

### §2.3 C3 — 핵심 루프 통과 (11 §3.1)

11 §3.1 C3 판정 문장을 원문 그대로 인용한다:

> **C3 핵심 루프 통과** — 위임 → 구현 → 검증 → 승인 핵심 루프가 이 Adapter 위에서 1회 이상 통과한다 (ROADMAP v0.2·v1.0). (specs/11-adapters.md §3.1)

근거: 위임 → 구현 → 검증 → 승인 핵심 루프가 Generic Adapter 의 환경 중립 바인딩 값 위에서 **1회 통과**했다. 물리 증거는 시연 기록·픽스처 앵커 1건에 모여 있다 — `uahf/docs/v1.0-generic-adapter-demo.md@cd9247b`(+ `v1.0-generic-demo-fixtures/@cd9247b`; 원장은 산출물 수명 정책으로 작업 트리에서 제거). 실증 지점:

- **4전이 사이클 완주.** 사이클 기록이 위임(Advisor)·구현(Worker)·검증(Verifier)·승인(Advisor) 4전이를 append-only(1행=1전이·seq 1→4 단조·결번/중복 0)로 완주했다. outcome 전건 pass, actor=human 0건.
- **독립 검증 통과.** 검증 단계가 구현 주체와 분리된 독립 실행 주체에 실위임되어 검증 리포트 `final_verdict = 통과(Pass)`(Met 전건·위반 0·판정 불가 0)를 산출했다 — 구현자가 자신의 산출물을 최종 판정하지 못함이 실증됐다.
- **소비 바인딩 표면.** 이 통과가 소비한 표면은 전부 Generic Adapter 의 환경 중립 값이다 — 파일 기반 위임 메시지(BP-10)·보고 파일(BP-11)·기록 파일(BP-13)·문서 역할 정의(BP-7)(generic-binding.md §4 DP-V5).
- **판정: `loop_pass` = 예.** 4전이 사이클 완주 + 독립 검증 Pass 가 Generic Adapter 위에서 핵심 루프 1회 통과를 실증한다. C3 충족.

---

## §3. Conformance Report (done 1 — 11 §3.2-D 6필드)

§2 의 C1~C3 대조 결과를 11 §3.2-D 6필드 구조로 산출한다. 각 필드 정의의 정본은 11 §3.2-D 이며, 아래는 그 인스턴스 값과 근거다.

| 필드 (11 §3.2-D) | 값 |
|---|---|
| `adapter` | **generic** — 두 번째 Adapter(11 §4.2가 배치로 허용한 `framework/adapters/generic/`, generic-binding.md §4 DP-V1). |
| `verdict` | **Valid(Minimal)** — C1·C2·C3(§3.1)을 모두 만족하되, 각 필수 바인딩의 내용은 핵심 루프 1회 통과에 필요한 최소 수준이고 선택 바인딩(BP-6·12·16·17)을 생략한 최소 구현 Adapter(11 §3.2-B). |
| `missing_bindings` | **없음** — C1 검사 결과(§2.1). 최소 바인딩 부분집합 필수 13개(BP-1·2·3·4·5·7·8·9·10·11·13·14·15) 전건 실현(generic-binding.md §2 커버리지·docs/v1.0-generic-adapter-demo.md §4 실증). |
| `core_modifications` | **없음** — C2 검사 결과(§2.2). Core 경계 5문서 AI 의존 토큰 0건(전수 스캔) + Generic 경계 Core 무침범 → Core Contract 수정 0건. |
| `loop_pass` | **예** — C3 검사 결과(§2.3). 위임 → 구현 → 검증 → 승인 핵심 루프가 이 Adapter 위에서 1회 통과(docs/v1.0-generic-adapter-demo.md 사이클 기록 4전이·독립 검증 리포트 final_verdict=Pass 3/3). |
| `notes` | 선택 바인딩 4종(BP-6 확장 표면·BP-12 영속성 백엔드·BP-16 이벤트·Hook Dispatch·BP-17 적용 조건 매칭) **미제공** → 등급 = **최소 구현 Adapter(Minimal Adapter)**(11 §3.2-B — 최소 구현 Adapter는 선택 바인딩을 생략할 수 있다; generic-binding.md §3 생략 명문화). |

### §3.1 등급 판정 (11 §3.2-B)

Generic Adapter 는 C1~C3 을 만족(Valid)하되 각 필수 바인딩의 내용은 핵심 루프 1회 통과에 필요한 최소 수준이며(환경 중립 규약 확정 — 형태 A) 선택 4 BP 를 생략했다(generic-binding.md §3; 11 §3.2-B 가 명시적으로 허용). 따라서 등급은 **최소 구현 Adapter(Minimal Adapter)**, verdict = **Valid(Minimal)** 이며 11 §7·§8 예1과 정렬한다. 최소 구현 Adapter 의 목적은 Adapter Interface 의 타 실행 환경 적용 가능성 증명이지 기능 완성이 아니므로(11 §3.2-B·ROADMAP v1.0), 선택 바인딩 생략은 이 목적과 정렬한다.

### §3.2 판정 성격 재확인 (done 3)

**verdict = Valid(Minimal) 은 근거와 함께 제시된 것이며 본 문서가 스스로 최종 승인 처리한 것이 아니다** — Verifier 독립 판정(CP2 — 필수 바인딩 체크리스트 대조·Core diff·루프 통과 기록 대조)과 Advisor 최종 승인(CP3 — Report 검토)이 뒤따른다(11 §7, 02 §3.2-A, AGENT.md Verification). 조건부·재량 항목을 스스로 통과 처리하지 않는다. 이 관행은 첫 번째 Adapter 의 Conformance 판정 문서 관행과 동형이다(그 문서를 경로로 명명하지 않는다 — DP-V14).

---

## §4. 상태 서술 실측 대조 (L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 "실재/존재/미존재" 서술을 파일 시스템과 직접 대조한다. **일자 박힌 계수·파일 개수 스냅샷은 두지 않는다** — 남기는 것은 재실측으로 참·거짓이 갈리는 불변 주장뿐이다.

| 대상 | 실측 판정 (재실측 대상) |
|---|---|
| `framework/adapters/generic/generic-binding.md` (C1 근거) | 실재 — §2 필수 13 BP 표·§3 선택 4 생략·§4 DP-V1/V5/V6 구성 확인. |
| `framework/adapters/generic/generic-adapter-conformance.md` (본 문서) | 실재 (이 파일). |
| 시연 문서 + 픽스처 (C3 근거) | **아카이브** — `uahf/docs/v1.0-generic-adapter-demo.md@cd9247b` + `uahf/docs/v1.0-generic-demo-fixtures/@cd9247b`(evidence 등급으로 작업 트리에서 제거; 4전이 사이클 기록·final_verdict=Pass 검증 리포트 포함). 열람 = `git show cd9247b:…`. |
| `framework/core/` · `framework/runtime/` (C2 Core 경계) | 실재 — 계약·프로토콜 문서만 담으며 AI 의존 instance 토큰 전수 스캔 0건(§2.2 (a)). 문서 계수는 불기재(drift). |

- **핵심 구분.** 실재를 주장하는 행은 파일 시스템 직접 실측 후에만 기입한다 — 미존재를 실재로, 아카이브를 현재 작업 트리 실재로 쓰지 않는다(L-07). C1·C2·C3 근거가 각각 위 표의 행으로 확인되어 §2·§3 판정의 근거가 실재함을 입증한다.

---

## §5. 정본 경계·격리·계약 소유 (self-note · verify_basis)
- **자기 점검 요지(선언 정본은 §0).** 재정의·확장 0 · 새 BP·새 Report 필드·새 verdict·새 등급·새 용어 창설 0 · Frozen specs/11 문면 무변경 · 판정 성격(최종 승인 아님 — 규칙은 §3.2). 판정 기준의 정본은 11 §3 이다.
- **DP-V6 준수 + verify_basis.** 본문에 특정 AI 이름·모델명·AI 벤더 제품/기능명 **0건**. 자가 스캔은 후보 집합 전체를 대상으로 했고 카테고리 정의는 §2.2 (a)가 1벌로 소유한다. `uaf-verified: 본문 전문에 대한 §2.2 (a) 카테고리 다중 토큰 스캔 — true 위반 0(중립 메커니즘 표기·Glossary 계약 용어는 허용 범위)`
- **DP-V14 준수.** 타 Adapter 경계 문서·경로 명명 0건 — 본문 경계 경로는 본 Adapter 자신의 경계·Core 경계·docs/ 시연 기록·spec 경로뿐이다.
- **작성 경계 이력(포인터).** 초판의 소유 경계 준수(이 1파일, 07 R4)·형제 Task 불인용(07 R2)·읽기 전용 소비 목록 감사 흔적은 git 이력(초판 커밋)에 보존되어 있다. `uaf-allow-legacy: 초판 감사 흔적은 git 이력에 보존, 본문은 포인터 1줄`

---

## §6. 요약 (1줄)

- 이 문서 = Generic Adapter 에 대한 Conformance 판정 인스턴스 — verdict = **Valid(Minimal)**(C1 누락 0 · C2 Core 수정 0 · C3 핵심 루프 1회 통과), 최종 승인은 CP2·CP3 후속. 절 지도·정본 경계·BP 사실 소재는 §1·§0·§2.1 이 소유하며 여기서 재서술하지 않는다.
