# framework/runtime/lifecycle — UAHF 수명주기 호스팅 프로토콜

작성일: 2026-07-05
상태: v0.3 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-05)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.1-C — 수명주기 호스팅 연산(Bootstrap / Shutdown)의 정본. 본 문서가 인스턴스화하는 계약.
- specs/01-runtime.md §3.2-C — Runtime Context(effectiveConfig / registry / state)의 정본. 필드·상태값의 상세 정본은 이 § 이 유지한다.
- specs/01-runtime.md §3.2-D — Failure Report(공통 실패 보고 구조)의 정본. 수명주기 연산의 실패 보고는 이 구조를 따른다.
- specs/01-runtime.md §3.3 INV-2 — 부분 집합 기동 불변 규칙(필수 계약만 해소되면 Module 부분 집합으로 기동; 선택 Module 부재는 Degraded이지 Failed 아님).
- specs/01-runtime.md §3.3 INV-6 — 경계 불가침 불변 규칙(Runtime은 Agent Lifecycle 단계를 정의하지 않는다; 호스팅 계약만 정의한다).
- specs/01-runtime.md §3.1-C 말미 "Serve 구간 주의" 문단 — Bootstrap과 Shutdown 사이 구간의 오케스트레이션 주체 경계.
- framework/core/structure.md §6 — 본 파일의 소속 경계(`framework/runtime/`), 소유 경계(이 파일 1개), 인스턴스화하는 01 § 계약 배정.
- framework/core/structure.md §5 — 금지 토큰 규칙(확정 조건 C-3). 본 문서 본문 준수 대상.
- framework/core/structure.md §7 — Core Contract 불변 조건(확정 조건 C-1). 본 문서는 01 §3의 인스턴스이며 계약을 확장·수정하지 않는다.
- specs/00-glossary.md §3.2-I — Runtime Context 용어 정본. 본 문서는 새 용어를 신설하지 않는다.

거버넌스: 이 문서는 `framework/runtime/` 소속 Core 문서다. 문서 본문은 특정 AI·언어·툴체인 비의존을 유지한다(structure.md §5, C-3). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-05 | v0.3 Draft | 최초 작성. Bootstrap/Shutdown 연산, Runtime Context, Serve 구간 경계, 언어 중립 시그니처를 01 §3.1-C·§3.2-C·§3.2-D·INV-2·INV-6의 인스턴스로 대조. 단계 전이 규칙 서술 0건 유지. | Worker (Advisor 위임, Task A4) |
| 2026-07-05 | v0.3 Baseline | v0.3 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass, CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/01-runtime.md §3이다.** 이 문서는 그 수명주기 호스팅 계약(§3.1-C)과 그 산출물·실패 데이터 포맷(§3.2-C·§3.2-D)의 **인스턴스**이며, 계약을 재정의·확장하지 않는다. 계약 요소는 § 포인터로만 참조한다(structure.md §7, C-1).
- 이 문서는 Runtime 호스팅 프로토콜을 서술한다 — 실행 환경이 어떻게 기동(Bootstrap)되고, 기동과 종료 사이(Serve 구간)에 무엇을 제공하며, 어떻게 종료(Shutdown)되는가의 계약이다.
- **이 문서는 Core 문서다.** 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다(structure.md §5, C-3, 01 §3.3 INV-4). 호스트 프로세스의 구체 실현(실행 컨테이너·세션 경계·직렬화 형식 등)은 **Adapter Binding 문서 소관**이며, 필요한 자리에는 소관 포인터만 둔다(01 §4 Adapter Binding).
- **경계 불가침(INV-6).** 이 문서는 Agent Lifecycle 단계를 정의하지 않는다. 단계와 그 전이는 Loop Engine 소관(specs/03-loop.md)이다(§4). 본 문서에는 Lifecycle 단계 전이 규칙 서술이 존재하지 않는다.
- 용어는 specs/00-glossary.md 정본만 사용한다. 새 용어를 신설하지 않는다. Runtime Context는 Glossary §3.2-I 정본이며, 필드 상세는 01 §3.2-C가 유지한다.

---

## §1. 목적

수명주기 호스팅 프로토콜의 책임은 세 가지다.

- 실행 환경의 **기동 계약**(Bootstrap)을 정의한다 — 무엇을 입력받아 어떤 상태를 산출하고, 언제 실패하는가(§2.1).
- 실행 환경의 **종료 계약**(Shutdown)을 정의한다 — 활성 자원을 어떤 순서로 해제하고, 언제 실패하는가(§2.2).
- 기동과 종료 **사이 구간(Serve)의 경계**를 명시한다 — Runtime이 그 구간에 제공하는 것과, 제공하지 않는 것(단계 오케스트레이션)을 가른다(§4).

이 프로토콜은 01 §3.1-C 수명주기 호스팅 연산의 인스턴스다. 형태 A(문서)에서 형태 B(실행 코드)로 전환되어도 01 §3 Core Contract 변경은 0이다(structure.md §7, C-1).

---

## §2. 수명주기 호스팅 연산 (정본: 01 §3.1-C)

Runtime은 두 개의 수명주기 연산을 노출한다: Bootstrap, Shutdown. 두 연산의 상세 정본은 01 §3.1-C가 유지하며, 아래는 그 계약의 인용·대조다(재정의 없음).

### §2.1 Bootstrap (01 §3.1-C)

| 항목 | 계약 (01 §3.1-C 인용) |
|---|---|
| 입력 | effective config(01 §3.2-B 정본의 병합 산출물) + 등록된 Module 집합. |
| 출력 | Runtime Context(01 §3.2-C) — 하위 컴포넌트가 구동될 수 있는 상태. |
| 완료 조건 | 모든 **필수(required)** 계약이 Resolve(01 §3.1-A)된다. **선택** 계약만 누락되면 상태는 Degraded로 Ready에 준한다. |
| 실패 보고 | reason = `MissingRequired` \| `UnresolvedContract`(01 §3.2-D reason 코드 집합의 부분). |

- 입력의 effective config는 01 §3.2-B가 정의하는 스코프·우선순위 병합의 결정적 산출물이다. 그 병합 규칙 상세는 01 §3.2-B(정본)가 유지하며 본 문서는 서술하지 않는다.
- 입력의 "등록된 Module 집합"과 필수/선택 계약의 Resolve는 01 §3.1-A(Register/Resolve) 정본을 참조한다. 본 문서는 이 연산들을 재정의하지 않는다.
- 완료 조건의 필수/선택 구분은 그대로 보존한다 — **필수 계약 미해소는 실패(Failed), 선택 계약 누락은 Degraded**다. 이 구분이 §3 state 값과 INV-2에 연결된다.

### §2.2 Shutdown (01 §3.1-C)

| 항목 | 계약 (01 §3.1-C 인용) |
|---|---|
| 입력 | Runtime Context(01 §3.2-C). |
| 출력 | 종료 결과. |
| 완료 조건 | 활성 Module이 **활성화의 역순으로** Deactivate되고 자원이 해제된다. |
| 실패 보고 | reason = `ShutdownIncomplete`, location = 실패한 module id(01 §3.2-D 구조). |

- Shutdown은 Bootstrap이 산출한 Runtime Context를 입력으로 받아, 활성화된 순서의 역순으로 각 활성 Module을 비활성화(Deactivate)하고 점유 자원을 해제한다.
- Deactivate 연산의 상세와 Module 활성/비활성 규칙 정본은 01 §3.1(§3.1-A Deregister 포함)이 유지한다. 본 문서는 종료 시 이 연산이 역순으로 적용된다는 수명주기 계약만 인스턴스화한다.
- 실패 시 보고는 어느 module id에서 종료가 미완결(`ShutdownIncomplete`)되었는지를 location에 담는다.

### §2.3 실패 보고 소속 경계 (정본: 01 §3.2-D)

수명주기 연산의 모든 실패는 01 §3.2-D의 **공통 Failure Report 구조**(operation / target / reason / location)로 보고한다. 위 §2.1·§2.2가 인용한 reason 코드(`MissingRequired`, `UnresolvedContract`, `ShutdownIncomplete`)와 location 필드는 **01 §3.2-D reason 코드 집합·필드에 소속**된다. 본 문서는 이 필드들을 새로 정의하지 않고, 소속 § 포인터를 명시해 다른 계약의 실패 필드와 혼입되지 않게 한다.

---

## §3. Runtime Context (정본: 01 §3.2-C)

Bootstrap(§2.1)의 산출물이자 호스팅 상태다. 용어 정본은 Glossary §3.2-I, 필드 상세 정본은 01 §3.2-C가 유지한다. 아래는 그 계약의 인용·대조다(재정의 없음).

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

이 규칙은 §2.1 Bootstrap 완료 조건("선택 계약만 누락되면 Degraded로 Ready에 준한다")과 정합하며, ARCHITECTURE 3.2 단독 사용(Modular) 원칙의 인스턴스다. registry·effectiveConfig의 내부 구조 서술이 필요한 경우에도 본 문서는 01 §3.2-C·§3.2-B 정본 § 포인터로만 참조한다.

---

## §4. Serve 구간 경계 (INV-6)

Bootstrap(§2.1)과 Shutdown(§2.2) 사이의 구간을 **Serve 구간**이라 한다(01 §3.1-C 말미 "Serve 구간 주의" 문단의 라벨).

### §4.1 Runtime이 제공하는 것

Serve 구간에서 Runtime은 다음만 제공한다:

- **Config** — effective config(01 §3.2-B)의 유효 설정 조회 표면.
- **계약 해소** — Resolve(01 §3.1-A)를 통한 contract → 활성 Module 핸들 제공.
- **자원** — 활성 Module과 그 점유 자원의 호스팅 유지.

즉 Serve 구간에서 Runtime의 책임은 **호스팅 표면의 유지**다. Runtime은 이 구간에 무엇이 "실행되는가"의 순서를 정하지 않는다.

### §4.2 Runtime이 제공하지 않는 것 — 단계 오케스트레이션 경계

Serve 구간에서 **Agent Lifecycle의 단계 오케스트레이션 주체는 Loop Engine이다**(01 §3.1-C 주의 문단, 01 §3.3 INV-6, Glossary §9-OQ2). Runtime은 그 구간에 Config·계약 해소·자원을 제공할 뿐, 단계 전이를 정의하지 않는다.

따라서:

- 이 문서는 Agent Lifecycle 단계를 **열거하지 않으며**, 단계 진입·완료·전이 규칙을 서술하지 않는다.
- Lifecycle 단계와 그 전이의 정본은 **specs/03-loop.md**다. Runtime은 Loop Engine이 구동될 "환경"만 제공하고, 루프 자체는 침범하지 않는다(01 §2, INV-6).
- Serve 구간과 Loop Engine이 소비하는 호스팅 표면의 정합은 01 §9 "03-loop 조율" 항목이 관장한다.

이 경계로 인해, 본 프로토콜은 "기동 → 호스팅 유지 → 종료"의 **환경 계약**만 정의하고, "그 위에서 무엇이 어떤 단계로 진행되는가"는 정의하지 않는다.

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

- 타입 이름(effective config, Runtime Context, Failure Report, 그 필드·값)은 전부 01 §3.2-B·§3.2-C·§3.2-D 정본의 데이터 포맷이다. 본 시그니처는 이를 **인용**할 뿐 새 타입을 정의하지 않는다.
- 위 표기는 특정 언어의 타입 표기법·직렬화 형식을 재현하지 않는다. 구체 실현(호스트 프로세스·타입 바인딩·직렬화 형식)은 Adapter Binding 문서 소관이다(01 §4).
- **이 시그니처는 01 §3.1-C·§3.2-C의 인스턴스이며 계약 확장·수정이 아니다(structure.md §7, C-1).** 형태 A → 형태 B(실행 코드) 전환 시에도 01 §3 Core Contract 변경은 0이며, 위반이 발견되면 구현하지 않고 Advisor에게 보고한다(structure.md §7 규칙 4).

---

## §6. 요약 (수명주기 한눈에 보기)

```
기동 ──────────────── 유지 ──────────────── 종료
Bootstrap             Serve 구간            Shutdown
(§2.1)                (§4)                  (§2.2)

입력: effective config  Runtime 제공:         입력: Runtime Context
      + 등록 Module 집합   Config·계약 해소·자원  동작: 활성화 역순 Deactivate
출력: Runtime Context    (단계 전이 정의 없음)   출력: 종료 결과
상태: Ready | Degraded  Loop Engine 소관     실패: ShutdownIncomplete
실패: MissingRequired  (specs/03-loop.md)          (+ location=module id)
    | UnresolvedContract
```

- 수명주기 두 연산(Bootstrap/Shutdown)과 그 산출물(Runtime Context)·실패 보고는 01 §3.1-C·§3.2-C·§3.2-D의 인스턴스다(재정의 0).
- 선택 계약 부재는 `Degraded`이지 `Failed`가 아니다 — 부분 집합 기동(INV-2, §3.1).
- Serve 구간에서 단계 오케스트레이션은 Loop Engine 소관이며, 본 문서에 단계 전이 규칙 서술은 0건이다(INV-6, §4).
- Core 문서 본문에 특정 AI·언어·툴체인·직렬화 형식 토큰은 0건이다(structure.md §5, C-3). 구체 실현은 Adapter Binding 문서 소관이다.
- 형태 A → 형태 B 전환에도 Core Contract 변경은 0이다(C-1, §5).
