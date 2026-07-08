# framework/plugins/module-manifest — Plugins Provider Module Manifest 인스턴스

작성일: 2026-07-06
상태: v0.8 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/01-runtime.md §3.2-A — Module Manifest 7필드(`id`/`contract`/`version`/`requires`/`entrypoint`/`configSchema`/`replaceable`). 본 문서가 채우는 서술자 계약의 정본. 필드명·의미·필수/선택 표기의 진위 판정 기준은 이 §가 유지한다.
- specs/01-runtime.md §3.3 INV-7 — 안정 식별자(`id`·`contract` id 안정성). INV-1 — 교체 가능(`replaceable` 기본값 근거). INV-2 — 단독 사용(필수 계약 해소 시 부분 집합 기동; `requires` 값 논의 근거). INV-4 — Core AI 비의존.
- specs/01-runtime.md §3.1-A — Register/Resolve/Replace/Deregister 연산. Plugins의 Install/Activate/Deactivate/Remove가 **소비**하는 Runtime 연산의 정본이다(이 Manifest는 Register의 입력이 된다).
- specs/01-runtime.md §4 — Adapter Binding(구체 직렬화·물리 진입점 해소·배포 채널 소관). 본 문서는 § 포인터로만 참조한다.
- specs/01-runtime.md §9 결정 기록 — §3.1-A에 Deregister 연산 추가(Registry 수명주기는 Runtime 소유). Plugin의 Deactivate/Remove가 그 위에서 성립함의 원문.
- specs/10-plugins.md §2 — Plugins의 Position(특정 Layer 지층이 아니라 Runtime의 Module 계약 위에서 동작하는 확장·배포 규격). 이 Provider가 구현하는 계약의 성격 근거.
- specs/10-plugins.md §3.1 — Plugins가 노출하는 네 연산(Install/Activate/Deactivate/Remove). `entrypoint`가 노출하는 논리 진입점의 근거.
- specs/10-plugins.md §3.3 INV-2 — 활성화는 Register/Resolve 계약으로만 성립(Plugins는 독자적 등록·해소 경로를 만들지 않는다). INV-7 — Config scope 불변(새 Config scope 미도입). INV-9 — 안정 식별자. INV-10 — AI 비의존 계약.
- specs/10-plugins.md §5 — Memory Access "해당 없음"(Plugins는 ARCHITECTURE 5.1의 Memory 소비자 목록에 없다). `requires`에서 Memory를 제외한 근거.
- framework/runtime/module-manifest.md — Module Manifest **형식 규격**(7필드 작성 지침·안정 식별자 규칙·언어 중립 시그니처). 본 문서는 그 형식을 이 Provider에 대해 채운 **인스턴스**다.
- framework/verifier/module-manifest.md — 선례(`requires`=없음 · `configSchema` 생략 DP-V2). 본 Manifest의 Memory 제외 근거가 이 선례와 **사실 관계 동형**이며, `configSchema` 생략도 동형임의 대비 대상(§3 `requires`·`configSchema`·§5).
- framework/workflow/module-manifest.md — Manifest 인스턴스 **관례 표본**(구성·필수/선택 표기 보존·정본 대조 표·§5 결정 기록 절·"Advisor 확인 — 인스턴스 값" 기록 형식·`version` 독립 축 `0.1.0`·`id` 접미 `-provider` 관례 동형).
- framework/core/structure.md §2(Module 구현 디렉터리 경계 — 자기완결, C-3 확장)·§5(금지 토큰 규칙 C-3 확장)·§7(Core Contract 불변 조건 C-1)·§8(plugins/ — 본 문서가 이 경계의 첫 실사용 인스턴스).
- specs/00-glossary.md — 용어 정본. Module / Module Manifest / 모듈 시스템 / Runtime Context는 §3.2-I, **Plugins (Component)**는 §3.2-D 표제어, **Plugin / Plugin Manifest**는 §3.2-J(J-10) 표제어(정본 specs/10-plugins.md)다.
- AGENT.md — 상위 규약(위임·검증·Memory 원칙).

거버넌스: 이 문서는 `framework/plugins/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인·직렬화 형식·물리 경로 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장, 01 §3.3 INV-4, 10 §3.3 INV-10). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. Plugins Provider Module의 01 §3.2-A 7필드 인스턴스(`id`=`plugins-provider`·`contract`=`PluginsInterface`(DP-E5)·`version`=`0.1.0`(Provider 자체 버전, 독립 축 — Advisor 확인)·`requires`=선언하지 않음(기본 없음 — DP-E5: 10 §5 Memory 미소비로 Verifier 선례 동형, Install/Activate의 Register/Resolve·Deregister는 Runtime 연산 소비이지 Provider contract 의존 아님, 역할 실행도 module Resolve 아님)·`entrypoint`=추상 참조(10 §3.1 Install/Activate/Deactivate/Remove 4연산 노출, 물리 해소 Adapter Binding 소관)·`configSchema`=선언하지 않음(DP-E5 — 10 §3 소비 Config 값 부재 + 10 INV-7 새 Config scope 미도입, Verifier DP-V2 동형)·`replaceable`=기본 true), 필드별 인스턴스 값·근거, 필수/선택 표기 정본 대조 보존, §5 결정 기록 절(Advisor 결정 DP-E5). `requires` 근거를 Verifier 선례(없음)·기존 4 Manifest의 Runtime 비선언 관례와 § 포인터로 구분 서술. 01·10 계약 재정의·확장 0, 금지 토큰 0(자가 부류별 전수 스캔), Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task EX-P1) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **필드 계약의 정본은 specs/01-runtime.md §3.2-A이다.** 이 문서는 그 Module Manifest 계약을 **Plugins Provider Module에 대해 채운 인스턴스**이며, 필드·의미·필수/선택 표기를 **재정의·확장하지 않는다** (framework/core/structure.md §7 확정 조건 C-1). 진위 판정 기준은 정본 01 §3.2-A가 유지하며, 필드 계약 요소는 § 포인터로만 참조한다.
- **형식 규격의 정본은 framework/runtime/module-manifest.md이다.** 그 문서는 임의 Manifest를 **어떻게 작성·판독하는가**(7필드 형식·안정 식별자 규칙·언어 중립 시그니처)를 규율하고, 이 문서는 그 형식을 이 Provider 하나에 대해 **구체 값으로 채운** 등록 서술자다. 두 문서 모두 01 §3.2-A를 진위 판정 기준으로 삼는다.
- **배포·수명주기 계약의 정본은 specs/10-plugins.md이다.** 이 Provider가 구현하는 contract(§3 아래 `PluginsInterface`)가 노출하는 설치·활성화·비활성화·제거 연산·데이터 포맷·불변 규칙은 10 §3이 소유한다. 본 문서는 그 계약을 **재정의·재서술하지 않고** § 포인터로만 참조하며, 이 Manifest는 그 Module의 등록 서술자일 뿐이다.
- **두 Manifest의 구분(혼동 방지).** 이 문서가 채우는 것은 **Plugins Provider Module 자신의 Module Manifest**(01 §3.2-A 7필드 — `PluginsInterface`를 구현하는 Module의 등록 서술자)다. 이는 개별 Plugin의 배포 서술자인 **Plugin Manifest**(10 §3.2-A 6필드 — 인스턴스 소유 문서는 framework/plugins/plugin-manifest.md)와 **다른 서술자**다. 전자는 이 확장·배포 규격을 실현하는 Provider Module을 Runtime에 등록하기 위한 것이고, 후자는 그 Provider가 설치·관리하는 개별 배포 단위(Plugin)를 서술한다.
- **이 문서는 Module 구현 디렉터리 문서다** (framework/core/structure.md §2 — 각 Module의 Manifest를 자기 경계에 두는 자기완결 단위, 01 §3.2-E 규칙 2). 본문 전체에 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명·물리 경로 토큰을 두지 않는다 (framework/core/structure.md §5 C-3 확장, 01 §3.3 INV-4, 10 §3.3 INV-10). 구체 직렬화·물리 진입점 해소·배포 채널·역할 실행 채널·환경 경로 관례는 **Adapter Binding 문서 소관**이며 (01 §4, 10 §4.1·§4.2), 필요한 자리에는 소관 포인터만 둔다. 이 문서가 `framework/plugins/` 경계의 **첫 실사용 인스턴스**다(structure.md §8 트리에서 plugins는 종전 미실현·경계만 확보된 빈 디렉터리였다 — `framework/memory/`가 v0.4에, `verifier/`가 v0.5에, `loop/`가 v0.6에, `workflow/`가 v0.7에 자기 경계의 첫 실사용 인스턴스가 된 것과 동형).
- 용어는 specs/00-glossary.md 정본만 사용한다. Module / Module Manifest / 모듈 시스템 / Runtime Context는 Glossary §3.2-I가, **Plugins (Component)**는 §3.2-D가, **Plugin / Plugin Manifest**는 §3.2-J(J-10)가, Register/Resolve/Deregister·Agent 역할·Memory Service Interface는 Glossary 기존 용어가 정본이다. 새 용어를 정본처럼 신설하지 않는다. **`PluginsInterface`는 이 Provider가 구현하는 contract 식별자 값이고 `plugins-provider`는 `id` 필드 값이지, Glossary 표제어의 신설이 아니다** (§5 DP-E5 경계 문구 참조 — DP-W1·DP-V1 동형).
- 필드명 백틱 표기(`id` 등)와 예시 식별자는 특정 언어·직렬화 형식의 문법이 아니라, 정본 01 §3.2-A가 쓰는 필드명·서술 라벨을 그대로 인용한 것이다.

---

## §1. 목적

이 문서는 **Plugins Provider Module**의 등록 서술자(Module Manifest)다. Plugins Provider는 contract `PluginsInterface`를 구현하는 Module이며, 본체 수정 없이 하나 이상의 Module(및 확장 요소)을 묶어 배포·설치·활성화·비활성화·제거하는 실행 단위를 Runtime이 등록·해소·교체한다 (10 §2·§3.1, 01 §3.1-A·§4.1 `framework/plugins/`).

이 규격의 책임은 두 가지다.

- 01 §3.2-A의 7필드를 이 Provider에 대한 **구체 값**으로 채운다 — `contract`는 `PluginsInterface`로, `id`는 `plugins-provider`로 확정하고(§5 DP-E5), `entrypoint`는 설치·활성화·비활성화·제거 네 연산(10 §3.1)을 노출하는 추상 참조로 두며 물리 해소는 Adapter Binding 문서 소관으로 미룬다. `requires`는 선언하지 않고(§3·§5 DP-E5), `configSchema`도 선언하지 않는다(§5 DP-E5).
- 필드의 필수/선택 표기를 정본 그대로 보존한다 (필수/선택 표기 보존 — session-handoff-v0.2 §1.5 Lesson 후보 2).

이 Manifest는 Runtime의 **Register** 연산(01 §3.1-A, 운용 규칙: framework/runtime/module-registry.md §2.1)의 입력이 된다. 각 Module은 자기완결(self-contained) 단위이므로, 이 Manifest는 그 Module의 `id`·`contract`·`entrypoint` 등 자기완결 참조를 한 서술자에 묶는다 (01 §3.2-E 규칙 2). 이 Provider가 구현하는 배포·수명주기 계약(§3.1 네 연산·§3.2 데이터 포맷·§3.3 불변 규칙)의 정본은 specs/10-plugins.md가 유지하며, 본 문서는 그 계약을 재서술하지 않는다.

---

## §2. 7필드 인스턴스 (정본 대조 표)

아래 표는 01 §3.2-A의 7필드를 이 Provider에 대한 값으로 채운 것이다. **필드명·의미·필수/선택 표기는 정본(01 §3.2-A) 그대로**이며, "값 (이 Provider 인스턴스)" 열만 본 문서가 채운다. 필드 계약을 재정의하지 않는다.

| 필드 | 의미 (정본: 01 §3.2-A) | 값 (이 Provider 인스턴스) | 필수 |
|---|---|---|---|
| `id` | Module 고유 식별자. 안정적(stable)이어야 교체의 기준이 된다. | `plugins-provider` (역할·계약 기반 안정 식별자 — DP-E5; §3·§5 참조) | 예 |
| `contract` | 이 Module이 구현하는 계약(Port/Interface) 식별자. 교체는 동일 `contract` 내에서만 성립한다. | `PluginsInterface` (DP-E5 — §3·§5 참조) | 예 |
| `version` | Module 버전. | `0.1.0` (이 Provider Module 자체 버전, 독립 축 — §3 참조) | 예 |
| `requires` | 의존하는 contract id 목록. Resolve 시 모두 해소되어야 한다. | 선언하지 않음 (기본 없음 — DP-E5, §3·§5 참조) | 아니오(기본 없음) |
| `entrypoint` | 실행 진입점의 추상 참조. 구체 바인딩은 01 §4가 해소한다. | 추상 참조 — 설치(Install)·활성화(Activate)·비활성화(Deactivate)·제거(Remove) 연산(10 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관(§4). | 예 |
| `configSchema` | 이 Module의 Config 스키마. | 선언하지 않음 (생략 — DP-E5, §3·§5 참조) | 아니오 |
| `replaceable` | 교체 가능 여부. 기본 `true` (ARCHITECTURE 3.2). `false`는 예외이며 근거를 요구한다. | 기본 `true` (생략 — §3 참조) | 아니오(기본 true) |

주:

- **필수/선택 표기는 정본 그대로 보존한다.** `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기를 복제한다 — 누락되면 계약 변경으로 읽힌다 (session-handoff-v0.2 §1.5 Lesson 후보 2). 이 Provider는 선택 필드 `requires`에 값을 채우지 않고 기본(없음)을 그대로 취한다 — 필드의 필수/선택 지위를 바꾸지 않는다.
- 필수 4필드: `id`·`contract`·`version`·`entrypoint`. 선택 3필드: `requires`(기본 없음)·`configSchema`·`replaceable`(기본 true).
- 상세 필드 계약의 정본은 01 §3.2-A가, 형식 작성 지침은 framework/runtime/module-manifest.md가 유지한다. 이 표는 값 인스턴스이며 계약의 진위 판정 기준이 아니다.

---

## §3. 필드별 인스턴스 값·근거

각 필드의 값 선택 근거다. 값은 이 Provider의 인스턴스이며, 필드 계약은 재정의하지 않는다.

### `id` = `plugins-provider` (필수)

- 근거: 역할·계약에 기반한 **안정 식별자**. 구현 세부(버전·환경·배포 방식)를 인코딩하지 않는다 (framework/runtime/module-manifest.md §3 `id`, 01 INV-7, 10 INV-9). 구현이 교체돼도 이 `id`는 유지되어 교체(Replace)의 기준이 된다. 명명은 Advisor 결정 DP-E5로 확정하며(§5), 관례 정본(framework/memory/module-manifest.md §3 `id`=`memory-service-provider`, framework/verifier/module-manifest.md §3 `id`=`verifier-provider`, framework/loop/module-manifest.md §3 `id`=`loop-provider`, framework/workflow/module-manifest.md §3 `id`=`workflow-provider`)과 **동형**으로 역할명(Glossary 표제어 "Plugins") + 관례 접미 `-provider`를 조합한 값이다.
- 회피: 배포 방식·리비전·마일스톤 어휘를 `id`에 섞지 않는다 — 그러면 교체마다 `id`가 바뀌어 안정 기준(INV-7, 10 INV-9)이 무너진다.
- 결정 기록: §5 DP-E5(명명) + "Advisor 확인 — 인스턴스 값"(승인).

### `contract` = `PluginsInterface` (필수)

- 근거: 이 Provider가 구현하는 **배포·수명주기 계약(Port/Interface)** 식별자다. Advisor 결정 DP-E5로 확정한다(§5). 구현·배포 방식이 다른 새 Provider로 교체(Replace)해도 동일 `contract` 내이므로, 이 계약의 소비자(설치·활성화·제거 연산을 호출하는 진입점 — Plugins는 Runtime의 Module 계약 위에서 동작하는 확장·배포 규격, 10 §2)의 참조는 그대로다 (01 INV-1, §8 예1 동형). 이 계약이 노출하는 네 연산·데이터 포맷·불변 규칙의 정본은 10 §3이 유지한다.
- 회피: 특정 구현·배포 방식을 `contract`에 섞지 않는다 — 동일 contract 교체(INV-1)가 불가능해진다.
- 결정 기록: §5 DP-E5.

### `version` = `0.1.0` (필수)

- 근거: 이 **Provider Module 자체의 버전**을 가리키는 고정된 버전 문자열이다 (framework/runtime/module-manifest.md §3 `version` — 같은 문자열은 항상 같은 Module 버전). Framework/Spec 버전(현재 v0.8 마일스톤)과는 **별개의 축**이며, Provider 구현이 갱신되면 이 값이 상승한다. 초기 인스턴스 값으로 `0.1.0`을 둔다 (framework/memory/·verifier/·loop/·workflow/module-manifest.md 관례 동형 — Provider Module 버전은 독립 축, 초기 `0.1.0`).
- **개별 Plugin의 `version`과 구분.** 이 `version`은 Plugins Provider Module 자체의 버전이며, 개별 Plugin의 배포 버전(Plugin Manifest `version`, 10 §3.2-A — plugin-manifest.md 소관)과는 다른 축이다. 두 버전은 서로 독립적으로 상승한다.
- 회피: 시점에 따라 대상이 달라지는 비고정 라벨을 쓰지 않는다 — 버전으로서 안정 참조가 되지 못한다.
- 확인 기록: §5 "Advisor 확인 — 인스턴스 값"(승인).

### `requires` = 선언하지 않음 (선택 — 기본 없음)

- 근거 (Advisor 결정 DP-E5, §5): 이 Provider가 구현하는 네 연산(10 §3.1)의 어느 완료 조건도 **다른 named contract에 대한 하드 의존을 요구하지 않는다**. 세 갈래로 근거가 갈린다.
  1. **Memory 미소비 (Verifier 선례와 동형).** 10 §5는 Plugins의 Memory Access를 **"해당 없음"**으로 규정한다 — Plugins는 배포·수명주기 계약이며 ARCHITECTURE 5.1의 Memory 소비자 목록(Agent, Loop, Workflow, Verifier)에 포함되지 않는다. 소비 자체가 없으므로 Memory를 `requires`로 선언하지 않는다. 이는 framework/verifier/module-manifest.md §3이 `requires`=없음을 택한 것과 **사실 관계 동형**이다(Verifier의 Memory 회수는 06 §5 "필요할 때만"의 선택적 보강이라 판정 연산의 Resolve를 게이트하지 않아 `requires`에 넣지 않았다). 단, Plugin이 **포함하는** Module이 Memory에 접근하는 경우에도 접근 경로는 단일 Port 하나뿐이며(10 INV-5), 그 접근 계약은 그 Module 자신의 Manifest·02·04 소관이지 이 Provider Manifest의 `requires`가 아니다(10 §5 단서).
  2. **Runtime 연산 소비는 contract 의존이 아니다.** Install/Activate/Deactivate/Remove(10 §3.1)는 Runtime의 Register/Resolve/Deregister 연산(01 §3.1-A)을 **소비**한다(10 INV-2 — 활성화는 Register/Resolve 계약으로만 성립). 그러나 Runtime 연산을 소비하는 것은 이 Provider Module이 **Resolve로 해소해야 할 contract 의존**과는 다른 층위다. `requires`는 "의존하는 contract id 목록 — Resolve 시 모두 해소되어야 한다"(01 §3.2-A)이며, Runtime은 이 Module을 **호스팅하는 환경**이지 Resolve 대상 contract가 아니다. 기존 4 Manifest(framework/memory/·verifier/·loop/·workflow/module-manifest.md)가 자신이 소비하는 Runtime 연산을 `requires`에 넣지 않은 **관례와 동형**이다.
  3. **개별 Plugin의 `requires`와 구분.** Activate 완료 조건이 "`requires` contract가 모두 Resolve된다"고 할 때의 `requires`는 **처리 대상 개별 Plugin의 Plugin Manifest `requires`**(10 §3.2-A — plugin-manifest.md 소관)이지, 이 Provider Module 자신의 `requires`가 아니다. 즉 이 Provider는 개별 Plugin의 contract 의존을 **Resolve해 주는 주체**이지, 그 자신이 그 contract에 의존하는 것이 아니다. 따라서 이 Provider Manifest의 `requires`는 비워 둔다.
  4. **역할 실행 제외.** 배포·수명주기 연산의 실행이 Agent 역할(Worker/Verifier/Advisor) 흐름에 얹히더라도, 그 역할 디스패치는 위임·보고 메시지(02) 흐름이지 Runtime의 module Resolve가 아니다. 따라서 `requires`에 포함하지 않는다(framework/workflow/module-manifest.md §3 requires 주 동형).
- 회피: 존재하지 않는 contract id를 여기서 **신설·추측하지 않는다** (Glossary 밖 새 용어 금지, 10 §3 재정의 금지). 물리 바인딩(배포 채널·직렬화·진입점 해소)이 추가 Adapter contract 의존을 도입한다면 그 선언은 Adapter Binding 문서가 소유한다 (01 §4, 10 §4.1·§4.2) — 이 Core 서술자가 아니다.
- **INV-2(단독 사용)와의 정합.** `requires`를 비워 두면 이 Provider가 Resolve될 때 강제되는 contract 의존이 없어 최소 Bootstrap(01 INV-2 — 필수 계약만 해소되면 부분 집합으로 기동)에서 부재로 인한 게이트가 발생하지 않는다. 이 Provider가 실제 배포 연산을 수행할 때 처리 대상 개별 Plugin의 `requires`를 Resolve하는 것은 그 연산의 완료 조건(10 §3.1 Activate)이지 이 Provider Module의 Resolve 게이트가 아니다.
- 결정 기록: §5 DP-E5.

### `entrypoint` = 추상 참조 (필수)

- 근거: 이 Module의 활성화 진입 — 자기완결 Plugin bundle을 설치하고(Install), 포함 Module을 Runtime Register/Resolve로 활성화하며(Activate), 활성화의 역순으로 비활성화하고(Deactivate), 잔여물 0으로 제거하는(Remove) 네 연산(10 §3.1)을 노출하는 논리적 진입점을 가리키는 **추상 참조**다. 구체 바인딩(직렬화·물리 경로·호출 규약·배포 채널·bundle 배치·배선 해제 진입점)은 기입하지 않는다. 상세는 §4.
- 회피: 특정 실행 환경의 물리 경로·형식별 로케이터를 Manifest에 직접 기입하지 않는다 — 환경 의존을 Core 서술자에 하드코딩하면 이식 시 서술자가 함께 바뀌어 AI·환경 비의존(01 INV-4, 10 INV-9·INV-10)이 깨진다.

### `configSchema` = 선언하지 않음 (선택)

- 근거 (Advisor 결정 DP-E5, §5): 10 §3 Core Contract에는 이 Provider가 소비하는 **Config 의존 값이 없다** — 네 연산(10 §3.1)의 어느 완료 조건도 Config 키를 소비 지점으로 요구하지 않는다. 나아가 10 INV-7은 **Plugin이 새로운 Config scope를 도입하지 않으며** Config는 Global/Project/Module(01 §3.2-B)로 유지되고 포함 Module은 자신의 configSchema를 그대로 소유한다고 못박는다. 소비 값 자체가 부재하고 새 scope 도입도 금지되므로, 이 Manifest는 `configSchema`를 **선언하지 않는다**(01 §3.2-A 선택 필드). 이는 framework/verifier/module-manifest.md §5 DP-V2(소비 Config 값 부재)와 **동형의 생략**이다.
- 회피: 소비 지점이 없는 Config 키를 이 Manifest의 자기 Module `configSchema`로 창설하지 않는다 — `configSchema`는 자기 Module 네임스페이스에 국한된 설정이고(framework/runtime/module-manifest.md §3 `configSchema`), 소비 값이 없는데 스키마를 두면 10 §3 계약에 없는 소비 지점을 우회 창설하고 10 INV-7(새 Config scope 미도입)을 침범하는 것이 된다.
- 결정 기록: §5 DP-E5.

### `replaceable` = 기본 `true` (선택 — 기본 true)

- 근거: 생략하여 기본값 `true`를 취한다. 모든 Module은 교체 가능이 기본이다 (01 INV-1, ARCHITECTURE 3.2). 배포·수명주기를 관장하는 실행 단위도 Runtime이 호스팅하는 하나의 Module이므로 동일 `contract` 내 교체가 성립해야 한다. 이 Provider에는 교체 불가의 근거가 없다.
- 회피: 근거 없는 `false`를 두지 않는다 — `false`는 근거를 요구하는 명시적 예외다 (01 INV-1).

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider Module의 활성화 진입을 가리키는 **추상(논리) 참조**다. 그것이 노출하는 것은 배포·수명주기 네 연산(10 §3.1) — 자기완결 Plugin bundle 1건의 설치, 포함 Module의 Register/Resolve 경유 활성화, 활성화 역순 비활성화, 잔여물 0 제거 — 이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩 — 직렬화 형식, 물리 경로·로케이터, 호출 규약, Plugin bundle 배치·배선·제거 방식, 배포 채널, 포함 확장 요소의 등록 표면 — 은 전부 **Adapter Binding 문서 소관**이다 (01 §4, 10 §4.1·§4.2). 이 Core 서술자에는 그 어떤 물리 경로·형식 토큰도 하드코딩하지 않는다 (framework/runtime/module-manifest.md §3 `entrypoint` 회피 규칙 정합).
- 이 분리로 실행 환경 이식·교체(01 §8 예1, 10 §4.2 이식 교체 지점) 시에도 이 Manifest의 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고, 물리 바인딩만 Adapter 경계에서 교체된다.
- 네 연산이 소비하는 Runtime 연산(Register/Resolve/Deregister, 01 §3.1-A)의 물리 배선, 그리고 포함 확장 요소(Hook/Skill)의 등록 표면 바인딩 역시 Adapter 소관이다(10 §4.1·§4.2, 확장 요소 표면은 08·09 §4 소관). 이 Core 서술자는 연산을 추상 참조로 노출할 뿐 물리 배선을 기입하지 않는다.

---

## §5. 결정 기록 (Advisor 결정 — DP-E5 + Advisor 확인)

이 절은 이 Manifest에 반영된 Advisor 결정(DP-E5)과 인스턴스 값 확인(`id`·`version`)을 기록한다. DP-E5는 위임의 확정 입력이며, 본 문서는 이를 그대로 반영한다(임의 변경 없음). 인스턴스 값 확인은 새 결정이 아니라, 관례·정본 근거로 채운 값에 대한 Advisor 승인이다.

### DP-E5 — `contract` = `PluginsInterface`, `id` = `plugins-provider`, `requires` 미선언, `configSchema` 미선언

- **결정:** 이 Provider가 구현하는 배포·수명주기 계약 식별자를 `PluginsInterface`로, Module 고유 식별자를 `plugins-provider`로 확정한다. `requires`는 선언하지 않고(기본 없음), `configSchema`도 선언하지 않는다.
- **명명 근거(`contract`·`id`):** 저장소에 이 계약·식별자의 **사전 명명이 없다**(Advisor 실측 2026-07-06 — `PluginsInterface`·`plugins-provider` 저장소 전역 0건. 작성 시점 Worker 재확인: `PluginsInterface`·`plugins-provider`·`PluginsPort` 전역 검색 0건). 따라서 이 명명은 Advisor의 결정 사안이며, Glossary 정본 어휘 **"Plugins"**(Core Component 표제어 "Plugins", Glossary §3.2-D, 정본 specs/10-plugins.md)에 Manifest 관례 접미 **"Interface"**(Port/Interface 계약 식별자 관례, 01 §3.2-A)·**"-provider"**(역할명 + 관례 접미, framework/memory/·verifier/·loop/·workflow/module-manifest.md 동형)를 조합해 확정했다. 이는 **신조어 창설이 아니라** 기존 정본 어휘 + 관례 접미의 조합이며, Verifier 선례(`VerifierInterface`, DP-V1)·Loop 선례(`LoopInterface`, DP-L1)·Workflow 선례(`WorkflowInterface`, DP-W1)와 동형이다.
- **`requires` 미선언 근거:** §3 `requires` 4갈래 근거대로 — (1) 10 §5가 Memory Access를 "해당 없음"으로 규정해 Memory 소비가 없으므로(Verifier 선례 동형), (2) Install/Activate/Deactivate/Remove가 소비하는 Runtime의 Register/Resolve/Deregister는 Runtime **연산 소비**이지 이 Provider Module이 Resolve로 해소할 contract 의존이 아니므로(기존 4 Manifest의 Runtime 비선언 관례 동형), (3) Activate가 Resolve하는 `requires`는 처리 대상 **개별 Plugin의 Plugin Manifest `requires`**이지 이 Provider 자신의 것이 아니므로, (4) 역할 실행은 역할 디스패치이지 module Resolve가 아니므로 — 이 Provider Manifest의 `requires`는 비워 둔다(01 §3.2-A 선택 필드, 기본 없음).
- **`configSchema` 미선언 근거:** 10 §3에 이 Provider가 소비하는 Config 값의 소비 지점이 부재하고, 10 INV-7이 Plugin의 새 Config scope 도입을 금지(Config는 Global/Project/Module 유지)하므로, 선언할 스키마가 없다(01 §3.2-A 선택 필드). 이는 framework/verifier/module-manifest.md §5 DP-V2(소비 Config 값 자체 부재)와 **동형의 생략**이다.
- **경계:** `PluginsInterface`는 이 Manifest의 `contract` 필드 **값(식별자)**이지 Glossary 표제어의 신설이 아니다(§0, §6 — DP-W1·DP-V1 동형 경계 문구). 마찬가지로 `plugins-provider`는 `id` 필드 값이지 새 용어가 아니다. 이 값이 노출하는 설치·활성화·비활성화·제거 계약의 정본은 10 §3이 유지하며, 이 Manifest는 그 계약을 재정의하지 않는다.

### Advisor 확인 — `id`·`version` 인스턴스 값 (2026-07-06)

- **성격:** 이 항목은 두 인스턴스 값(`id`·`version`)에 대한 Advisor **확인(승인)** 기록이다. `id`(=`plugins-provider`)는 DP-E5의 명명 결정으로 확정된 값이고, `version`(=`0.1.0`)은 명시 DP 없이 Manifest 인스턴스 관례로 채운 값이다. 두 값 모두 Advisor 확인으로 승인되었으며, 미확정 잔여가 없다(§3·§6·§9 정합).
- **`id` = `plugins-provider` 승인:** DP-E5 명명 근거(Glossary 표제어 "Plugins" + 관례 접미 "-provider")에 따라 확정되었고, Manifest 인스턴스 관례(framework/memory/·verifier/·loop/·workflow/module-manifest.md §3 `id`=`memory-service-provider`·`verifier-provider`·`loop-provider`·`workflow-provider`)와 동형이며 01 INV-7·10 INV-9 안정 식별자 요건을 충족한다.
- **`version` = `0.1.0` 승인:** Provider Module 자체 버전을 가리키는 고정 버전 문자열이며, Framework/Spec 버전(현재 v0.8 마일스톤) 및 개별 Plugin 배포 버전과 **독립 축**이다(framework/memory/·verifier/·loop/·workflow/module-manifest.md 관례 동형 — 초기 `0.1.0`, Provider 구현 갱신 시 상승).

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- **재정의·확장 0.** 본 문서의 7필드는 01 §3.2-A의 인스턴스다. 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A(필드 계약)와 framework/runtime/module-manifest.md(형식 규격)다. 이 Provider가 구현하는 배포·수명주기 계약(10 §3 네 연산·데이터 포맷·불변 규칙)도 **재정의하지 않고** § 포인터로만 참조했다. 필수/선택 표기(`requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)")를 정본 그대로 보존했고, `requires`의 선택 지위를 바꾸지 않은 채 기본(없음)을 취했으며, 새 필드를 추가하지 않았다.
- **금지 토큰 0 (자가 부류별 전수 스캔).** 본문·표 전체를 다음 후보 부류 **전체**로 전수 대조하여 실증 0건임을 확인했다 (framework/core/structure.md §5 C-3 확장, 단일 토큰 검색에 국한하지 않고 부류별 전수 대조) — { 특정 AI 이름·모델명·제품 기능명 } ∪ { 특정 프로그래밍 언어명·툴체인명 } ∪ { 직렬화 형식명·확장자·OS 토큰 } ∪ { 물리 경로·배포 채널명·Adapter 하위 인스턴스 토큰·특정 Adapter Binding 문서명 }. 진입점·bundle 배치·배포 채널·역할 실행 채널·Runtime 연산 배선의 물리 실현이 필요한 자리에는 구체 토큰 대신 "Adapter Binding 문서 소관 (01 §4, 10 §4.1·§4.2)" 포인터를 두었고, 특정 Adapter Binding 문서명·물리 경로도 인용하지 않았다 (mention/use 경계 — 금지 토큰의 예시도 누출이다, session-handoff-v0.2 §1.5 Lesson 후보 3). 다음은 금지 토큰이 아니다: (i) 계약 필드 값 `plugins-provider`·`PluginsInterface`(및 참조한 `verifier-provider`·`workflow-provider` 등 선례 값) — `id`·`contract` **필드 값**이지 금지 토큰이 아니다; (ii) 연산명(Install/Activate/Deactivate/Remove·Register/Resolve/Deregister)·Glossary 정본 어휘(Plugins·Plugin·Module·역할 명칭) — 정본의 평이한 명칭; (iii) 저장소 문서 식별자(`specs/…`·`framework/…` 상호 참조 및 본 문서 자신의 식별자 `framework/plugins/module-manifest.md`) — 문서 식별자이며 직렬화 형식·물리 경로 토큰이 아니다(structure.md §5·workflow/module-manifest.md §6 분류 선례 동형).
- **새 계약·용어 0.** `requires`에서 존재하지 않는 contract를 신설하지 않았다(그리고 하드 의존 자체를 두지 않았다). Glossary 밖 새 용어를 만들지 않았다. `PluginsInterface`는 `contract` 필드의 식별자 **값**, `plugins-provider`는 `id` 필드 **값**이며 Glossary 표제어의 신설이 아니다 — Glossary 정본 어휘 "Plugins" + 관례 접미의 조합으로 Advisor가 확정했다(§5 DP-E5).
- **미완성 형제 산출물 비인용 (07 R2).** 같은 병렬 집합(v0.8 PS-1)에서 동시 작성 중일 수 있는 형제 산출물(Adapter Binding 바인딩 문서·시연 절차서 등)은 추측·인용하지 않았다. 형제 산출물 중 함께 작성되는 plugin-manifest.md(개별 Plugin 배포 서술자 포맷 인스턴스 소유 문서)는 이 Provider Manifest와 **다른 서술자**임을 §0·§3에서 구분 지시하되, 그 내부 내용을 인용하지 않고 소관 포인터로만 지시했다. 본 문서는 확정 정본(01·10 spec, Glossary)과 기존 Baseline(framework/runtime/·memory/·verifier/·loop/·workflow/·core/ 문서)만 참조했다.
- **설계 확정(Advisor).** `contract`·`id` 명명·`requires` 미선언·`configSchema` 미선언(DP-E5)은 Advisor 결정으로 확정되어 §2·§3·§5에 반영했다. `id`(=`plugins-provider`)·`version`(=`0.1.0`) 인스턴스 값은 Advisor 확인으로 승인되었다(§5 "Advisor 확인 — 인스턴스 값"). 미확정·open 잔여는 없다.

---

## §7. 요약 (한눈에 보기)

- 이 문서 = **Plugins Provider Module**의 등록 서술자(Manifest) **인스턴스**. 필드 계약 정본 = 01 §3.2-A, 형식 규격 = framework/runtime/module-manifest.md, 배포·수명주기 계약 정본 = 10 §3 (본 문서는 값 인스턴스, 재정의 아님 — C-1). 개별 Plugin 배포 서술자(Plugin Manifest, 10 §3.2-A)와는 다른 서술자이며 그 인스턴스 소유 문서는 plugin-manifest.md다.
- 7필드 값: `id`=`plugins-provider`(DP-E5) · `contract`=`PluginsInterface`(DP-E5) · `version`=`0.1.0`(Provider 자체 버전, 독립 축 — Advisor 확인) · `requires`=선언하지 않음(DP-E5 — Memory 미소비(Verifier 선례 동형)·Runtime 연산 소비는 contract 의존 아님·개별 Plugin의 requires와 구분·역할 실행 제외) · `entrypoint`=추상 참조(설치·활성화·비활성화·제거 4연산 10 §3.1 노출, 물리 해소 Adapter 소관) · `configSchema`=선언하지 않음(DP-E5 — 소비 Config 값 부재 + 10 INV-7 새 Config scope 미도입, Verifier DP-V2 동형) · `replaceable`=기본 true.
- 필수 4(`id`·`contract`·`version`·`entrypoint`) / 선택 3(`requires`·`configSchema`·`replaceable`) — 필수/선택 표기 정본 그대로. `requires`는 선택 필드의 기본(없음)을 그대로 취했다.
- 이 Manifest는 Runtime Register(01 §3.1-A, module-registry.md §2.1)의 입력이며, 구현하는 배포·수명주기 계약은 10 §3. 네 연산은 Runtime의 Register/Resolve/Deregister(01 §3.1-A)를 소비하나, 그 연산 소비는 이 Provider의 `requires` contract 의존이 아니다.
- 물리 진입점·직렬화·bundle 배치·배포 채널·역할 실행 채널·Runtime 연산 배선은 Adapter Binding 문서 소관 (01 §4, 10 §4.1·§4.2). Module 구현 디렉터리 문서 본문에는 그 토큰이 0건이다 (C-3 확장).
