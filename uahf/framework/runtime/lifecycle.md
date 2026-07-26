# framework/runtime/lifecycle — UAHF 수명주기 호스팅 프로토콜

작성일: 2026-07-05
상태: v0.3 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-05)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.1-C — 수명주기 호스팅 연산(Bootstrap / Shutdown)의 정본 및 말미 "Serve 구간 주의" 문단(§4).
- specs/01-runtime.md §3.2-C — Runtime Context(effectiveConfig / registry / state)의 정본.
- specs/01-runtime.md §3.2-D — Failure Report 공통 구조의 정본.
- specs/01-runtime.md §3.3 INV-2·INV-6 — 부분 집합 기동·경계 불가침 불변.
- framework/core/structure.md §2·§5·§7 — 소속 경계(4경계 배치 표)·금지 토큰 규칙(C-3)·Core Contract 불변(C-1).
- specs/00-glossary.md §3.2-I — Runtime Context 용어 정본.

거버넌스: 이 문서는 `framework/runtime/` 소속 Core 문서다. 본문은 AI·언어·툴체인 비의존을 유지한다(structure.md §5 C-3). 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3).

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

이 절이 본 문서의 경계 선언 정본이다(다른 절에서 반복하지 않는다).

- **정본은 specs/01-runtime.md §3이다.** 이 문서는 수명주기 호스팅 계약(§3.1-C)과 그 산출물·실패 데이터 포맷(§3.2-C·§3.2-D)의 **인스턴스**이며 계약을 재정의·확장하지 않는다(structure.md §7 C-1). 위반이 발견되면 구현하지 않고 Advisor에게 보고한다.
- 이 문서는 Runtime 호스팅 프로토콜 — 기동(Bootstrap) → Serve 구간 제공 → 종료(Shutdown)의 환경 계약을 서술한다.
- **Core 문서.** 본문 전체에 금지 토큰(AI 이름·모델명·제품 기능명·언어명·툴체인명·직렬화 형식명)을 두지 않는다 — 규칙·분류 정본은 structure.md §5 C-3(및 01 §3.3 INV-4)이다. 호스트 프로세스의 구체 실현(실행 컨테이너·세션 경계·직렬화 형식 등)은 Adapter Binding 문서 소관이다(01 §4).
- **경계 불가침(INV-6).** 이 문서는 Agent Lifecycle 단계를 정의하지 않는다 — 단계와 전이는 Loop Engine 소관(specs/03-loop.md)이며 본 문서에 단계 전이 규칙 서술은 0건이다(§4).
- 용어는 specs/00-glossary.md §3.2-I 정본만 사용한다. 새 용어를 신설하지 않는다.

---

## §1. 목적

이 프로토콜은 세 가지를 확정한다 — 기동 계약(§2.1) · 종료 계약(§2.2) · 기동과 종료 사이 Serve 구간의 경계(§4, Runtime이 제공하는 것과 제공하지 않는 것). 01 §3.1-C의 인스턴스이며 형태 A → 형태 B 전환에도 01 §3 Core Contract 변경은 0이다(C-1).

---

## §2. 수명주기 호스팅 연산 (정본: 01 §3.1-C)

Runtime은 두 수명주기 연산(Bootstrap·Shutdown)을 노출한다. 상세 정본은 01 §3.1-C가 유지하며 아래는 그 계약의 인용·대조다(재정의 없음).

### §2.1 Bootstrap (01 §3.1-C)

| 항목 | 계약 (01 §3.1-C 인용) |
|---|---|
| 입력 | effective config(01 §3.2-B 정본의 병합 산출물) + 등록된 Module 집합. |
| 출력 | Runtime Context(01 §3.2-C) — 하위 컴포넌트가 구동될 수 있는 상태. |
| 완료 조건 | 모든 **필수(required)** 계약이 Resolve(01 §3.1-A)된다. **선택** 계약만 누락되면 상태는 Degraded로 Ready에 준한다. |
| 실패 보고 | reason = `MissingRequired` \| `UnresolvedContract`(01 §3.2-D reason 코드 집합의 부분). |

- effective config의 병합 규칙 상세는 01 §3.2-B, "등록된 Module 집합"과 필수/선택 계약의 Resolve는 01 §3.1-A 정본이 유지한다(본 문서 재정의 0).
- 완료 조건의 필수/선택 구분은 그대로 보존한다 — **필수 계약 미해소는 실패(Failed), 선택 계약 누락은 Degraded**다. 이 구분이 §3 state 값과 INV-2에 연결된다.

### §2.2 Shutdown (01 §3.1-C)

| 항목 | 계약 (01 §3.1-C 인용) |
|---|---|
| 입력 | Runtime Context(01 §3.2-C). |
| 출력 | 종료 결과. |
| 완료 조건 | 활성 Module이 **활성화의 역순으로** Deactivate되고 자원이 해제된다. |
| 실패 보고 | reason = `ShutdownIncomplete`, location = 실패한 module id(01 §3.2-D 구조). |

- Shutdown은 Runtime Context를 입력으로 받아 활성화된 순서의 역순으로 각 활성 Module을 비활성화(Deactivate)하고 점유 자원을 해제한다. Deactivate 연산 상세·Module 활성/비활성 규칙의 정본은 01 §3.1(§3.1-A Deregister 포함)이 유지하며, 본 문서는 종료 시 역순 적용이라는 수명주기 계약만 인스턴스화한다.
- 실패 시 보고는 어느 module id에서 종료가 미완결(`ShutdownIncomplete`)되었는지를 location에 담는다.

### §2.3 실패 보고 소속 경계 (정본: 01 §3.2-D)

수명주기 연산의 모든 실패는 01 §3.2-D의 **공통 Failure Report 구조**(operation / target / reason / location)로 보고한다. §2.1·§2.2가 인용한 reason 코드(`MissingRequired`·`UnresolvedContract`·`ShutdownIncomplete`)와 location 필드는 01 §3.2-D reason 코드 집합·필드에 소속되며, 본 문서는 이를 새로 정의하지 않고 소속 § 포인터를 명시해 다른 계약의 실패 필드와 혼입되지 않게 한다.

---

## §3. Runtime Context (정본: 01 §3.2-C)

Bootstrap(§2.1)의 산출물이자 호스팅 상태다. 용어 정본은 Glossary §3.2-I, 필드 상세 정본은 01 §3.2-C이며 아래는 인용·대조다(재정의 없음).

| 필드 | 의미 (01 §3.2-C 인용) |
|---|---|
| `effectiveConfig` | 01 §3.2-B의 병합 결과. 상세 정본은 01 §3.2-B. |
| `registry` | contract id → 활성 module id 바인딩과 등록된 Manifest 집합. 상세 정본은 01 §3.2-C·§3.2-A. |
| `state` | `Ready` \| `Degraded` \| `Failed`(아래). |

state는 정확히 세 값을 가진다(01 §3.2-C 인용):

- **`Ready`** — 필수 계약 전부 해소.
- **`Degraded`** — 선택 계약 일부 누락. Ready에 준하며 계속 기동 상태다.
- **`Failed`** — 필수 계약 미해소.

### §3.1 부분 집합 기동 규칙 (INV-2)

Runtime은 필수 계약만 해소되면 **Module의 부분 집합만으로 기동**할 수 있다(01 §3.3 INV-2). 따라서:

- 선택 Module의 부재는 **`Degraded`일 뿐 `Failed`가 아니다.** 선택 계약 누락은 실패가 아니라 축소 기동이다.
- 필수 계약이 미해소일 때에만 `Failed`이며, 이때 Bootstrap은 실패한다(§2.1, reason=`MissingRequired`).

이 규칙은 §2.1 Bootstrap 완료 조건("선택 계약만 누락되면 Degraded로 Ready에 준한다")과 정합하며 ARCHITECTURE 3.2 단독 사용(Modular) 원칙의 인스턴스다. registry·effectiveConfig의 내부 구조는 01 §3.2-C·§3.2-B 정본 § 포인터로만 참조한다.

---

## §4. Serve 구간 경계 (INV-6)

Bootstrap(§2.1)과 Shutdown(§2.2) 사이의 구간을 **Serve 구간**이라 한다(01 §3.1-C 말미 "Serve 구간 주의" 문단의 라벨).

### §4.1 Runtime이 제공하는 것

Serve 구간에서 Runtime은 다음만 제공한다 — **Config**(effective config의 유효 설정 조회 표면, 01 §3.2-B) · **계약 해소**(Resolve를 통한 contract → 활성 Module 핸들, 01 §3.1-A) · **자원**(활성 Module과 점유 자원의 호스팅 유지). 즉 Runtime의 책임은 **호스팅 표면의 유지**이며, 이 구간에 무엇이 "실행되는가"의 순서를 정하지 않는다.

### §4.2 Runtime이 제공하지 않는 것 — 단계 오케스트레이션 경계

Serve 구간에서 **Agent Lifecycle의 단계 오케스트레이션 주체는 Loop Engine이다**(01 §3.1-C 주의 문단·INV-6, Glossary §9-OQ2). 따라서 이 문서는 Lifecycle 단계를 열거하지 않고 진입·완료·전이 규칙도 서술하지 않는다 — 그 정본은 specs/03-loop.md이며, Runtime은 Loop Engine이 구동될 "환경"만 제공하고 루프 자체는 침범하지 않는다(01 §2). Serve 구간과 Loop Engine이 소비하는 호스팅 표면의 정합은 01 §9 "03-loop 조율" 항목이 관장한다.

---

## §5. Bootstrap → Serve → Shutdown 언어 중립 시그니처

수명주기의 입력/출력/실패를 **타입 수준**으로 요약한다. 아래 시그니처는 특정 프로그래밍 언어의 타입 문법이 아니라 언어 중립 계약 표기다.

**표기 규약** (언어 중립):

- `( … )` — 입력(들).
- `→` — 산출(출력).
- `|` — 택일(둘 중 하나가 성립).
- `[ … ]` — 산출이 아니라 구간 동안 **유지·제공되는 표면**.

```
Bootstrap : ( effective config , 등록 Module 집합 )
            →  Runtime Context( state = Ready | Degraded )
            |  Failure Report( reason = MissingRequired | UnresolvedContract )

Serve     : ( Runtime Context )
            →  [ 호스팅 표면 유지 : Config · 계약 해소 · 자원 제공 ]
               ※ Runtime 연산이 아니라 Bootstrap–Shutdown 사이 구간.
                 단계 오케스트레이션은 Loop Engine 소관(§4, specs/03-loop.md).

Shutdown  : ( Runtime Context )
            →  종료 결과
            |  Failure Report( reason = ShutdownIncomplete , location = module id )
```

- 타입 이름(effective config, Runtime Context, Failure Report, 그 필드·값)은 전부 01 §3.2-B·§3.2-C·§3.2-D 정본의 데이터 포맷이며 본 시그니처는 이를 **인용**할 뿐 새 타입을 정의하지 않는다. 구체 실현(호스트 프로세스·타입 바인딩·직렬화 형식)은 Adapter Binding 소관이다(01 §4).
- **이 시그니처는 01 §3.1-C·§3.2-C의 인스턴스이며 계약 확장·수정이 아니다(C-1).** 형태 B 전환 시에도 01 §3 Core Contract 변경은 0이며, 위반이 발견되면 구현하지 않고 Advisor에게 보고한다.
