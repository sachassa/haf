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

거버넌스: 이 문서는 `framework/plugins/` 소속 Module 구현 디렉터리 문서다 (framework/core/structure.md §2). 문서 본문은 AI 비의존이면서 특정 프로그래밍 언어·툴체인·직렬화 형식·물리 경로 비의존을 유지한다 (framework/core/structure.md §5 C-3 확장, 01 §3.3 INV-4, 10 §3.3 INV-10). 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. Plugins Provider Module의 01 §3.2-A 7필드 인스턴스(`id`=`plugins-provider`·`contract`=`PluginsInterface`(DP-E5)·`version`=`0.1.0`(Provider 자체 버전, 독립 축 — Advisor 확인)·`requires`=선언하지 않음(기본 없음 — DP-E5: 10 §5 Memory 미소비로 Verifier 선례 동형, Install/Activate의 Register/Resolve·Deregister는 Runtime 연산 소비이지 Provider contract 의존 아님, 역할 실행도 module Resolve 아님)·`entrypoint`=추상 참조(10 §3.1 Install/Activate/Deactivate/Remove 4연산 노출, 물리 해소 Adapter Binding 소관)·`configSchema`=선언하지 않음(DP-E5 — 10 §3 소비 Config 값 부재 + 10 INV-7 새 Config scope 미도입, Verifier DP-V2 동형)·`replaceable`=기본 true), 필드별 인스턴스 값·근거, 필수/선택 표기 정본 대조 보존, §5 결정 기록 절(Advisor 결정 DP-E5). `requires` 근거를 Verifier 선례(없음)·기존 4 Manifest의 Runtime 비선언 관례와 § 포인터로 구분 서술. 01·10 계약 재정의·확장 0, 금지 토큰 0(자가 부류별 전수 스캔), Glossary 밖 새 용어 0. | Worker (Advisor 위임, Task EX-P1) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-17 | (상태 유지) | 산출물 수명 정책 제정(docs/artifact-lifecycle-policy.md) 정합 — 핸드오프 판례 인용 제거(안정 근거 유지) — 삭제 산출물 참조 없음(앵커 전환 해당 없음). 계약·규범 무변경. | Worker (Advisor 위임, 사용자 결정 2026-07-17) |
| 2026-07-26 | (정합) | md 슬림화 Wave 3 — 비계약 격리 개정: 경계 중복·표-산문 이중·감사 서술 압축, 계약 문면 무변경. 종전 = git 앵커 90ca19c | Advisor 위임 |

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
- 필드의 필수/선택 표기를 정본 그대로 보존한다 (필수/선택 표기 보존).

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

- **필수/선택 표기는 정본 그대로 보존한다.** `requires`의 "(기본 없음)"·`replaceable`의 "(기본 true)" 속성 표기를 복제한다 — 누락되면 계약 변경으로 읽힌다. 이 Provider는 선택 필드 `requires`에 값을 채우지 않고 기본(없음)을 그대로 취한다 — 필드의 필수/선택 지위를 바꾸지 않는다.
- **표 말미 면책(파일당 1곳).** 상세 필드 계약의 정본은 01 §3.2-A가, 형식 작성 지침은 framework/runtime/module-manifest.md가 유지한다. 이 표는 값 인스턴스이며 계약의 진위 판정 기준이 아니다.

---

## §3. 필드별 인스턴스 값·근거

각 필드의 값과 1줄 근거다(§5는 결정 ID·결론만 둔다 — 쌍둥이 서술 제거). 값은 이 Provider의 인스턴스이며 필드 계약은 재정의하지 않는다.

- **`id` = `plugins-provider`** (필수) — 역할·계약 기반 **안정 식별자**(01 INV-7, 10 INV-9): 구현 세부(버전·환경·배포 방식)·마일스톤 어휘를 인코딩하지 않아 교체 기준이 유지된다. 명명 = Glossary 표제어 "Plugins" + 관례 접미 `-provider`(memory/·verifier/·loop/·workflow/module-manifest 동형). 결정 = §5 DP-E5, Advisor 확인 = §5.
- **`contract` = `PluginsInterface`** (필수) — 이 Provider가 구현하는 배포·수명주기 계약(Port/Interface) 식별자. 동일 `contract` 내 교체로 소비자 참조가 유지된다(01 INV-1). 계약이 노출하는 네 연산·데이터 포맷·불변 규칙의 정본은 10 §3. 결정 = §5 DP-E5.
- **`version` = `0.1.0`** (필수) — 이 Provider Module 자체 버전의 고정 문자열. Framework/Spec 버전 및 **개별 Plugin의 배포 버전**(Plugin Manifest `version`, 10 §3.2-A — plugin-manifest.md 소관)과 각각 독립 축이며 서로 독립적으로 상승한다. Advisor 확인 = §5.
- **`requires` = 선언하지 않음** (선택 — 기본 없음) — 네 연산(10 §3.1)의 어느 완료 조건도 다른 named contract에 대한 하드 의존을 요구하지 않는다. 네 갈래 근거:
  1. **Memory 미소비(Verifier 선례 동형).** 10 §5가 Plugins의 Memory Access를 "해당 없음"으로 규정한다(ARCHITECTURE 5.1 Memory 소비자 목록에 부재). 포함 Module이 Memory에 접근하는 경우에도 경로는 단일 Port 하나뿐이며(10 INV-5) 그 접근 계약은 그 Module 자신의 Manifest·02·04 소관이다(10 §5 단서).
  2. **Runtime 연산 소비는 contract 의존이 아니다.** 네 연산은 Register/Resolve/Deregister(01 §3.1-A)를 **소비**하나(10 INV-2), Runtime은 이 Module을 **호스팅하는 환경**이지 Resolve 대상 contract가 아니다(기존 4 Manifest의 Runtime 비선언 관례 동형).
  3. **개별 Plugin의 `requires`와 구분.** Activate가 Resolve하는 `requires`는 **처리 대상 개별 Plugin의 Plugin Manifest `requires`**(plugin-manifest.md 소관)이지 이 Provider 자신의 것이 아니다 — 이 Provider는 그것을 Resolve해 주는 주체다.
  4. **역할 실행 제외.** 역할 디스패치는 위임·보고 메시지(02) 흐름이지 module Resolve가 아니다.
  - **INV-2(단독 사용) 정합.** 비워 두므로 Resolve 시 강제되는 contract 의존이 없어 최소 Bootstrap에서 부재 게이트가 발생하지 않는다. 존재하지 않는 contract id를 신설·추측하지 않는다. 결정 = §5 DP-E5.
- **`entrypoint` = 추상 참조** (필수) — 설치·활성화·비활성화·제거 네 연산(10 §3.1)을 노출하는 논리 진입점. 구체 바인딩(직렬화·물리 경로·호출 규약·배포 채널·bundle 배치·배선 해제 진입점)은 기입하지 않는다 — 환경 의존을 Core 서술자에 하드코딩하면 비의존(01 INV-4, 10 INV-9·INV-10)이 깨진다. 상세 = §4.
- **`configSchema` = 선언하지 않음** (선택) — 10 §3에 소비 지점이 부재하고, 10 INV-7이 새 Config scope 도입을 금지한다(Config는 Global/Project/Module 유지, 포함 Module이 자신의 스키마를 그대로 소유). 소비 지점 없는 키를 자기 Module 스키마로 창설하지 않는다. 결정 = §5 DP-E5.
- **`replaceable` = 기본 `true`** (선택 — 기본 true) — 교체 가능이 기본이며(01 INV-1) 이 Provider에는 교체 불가의 근거가 없다. 근거 없는 `false`를 두지 않는다.

---

## §4. entrypoint 추상 참조와 물리 해소 (Adapter Binding 소관)

- `entrypoint`는 이 Provider Module의 활성화 진입을 가리키는 **추상(논리) 참조**다. 그것이 노출하는 것은 배포·수명주기 네 연산(10 §3.1) — 자기완결 Plugin bundle 1건의 설치, 포함 Module의 Register/Resolve 경유 활성화, 활성화 역순 비활성화, 잔여물 0 제거 — 이다.
- **물리 해소는 이 문서 밖이다.** 진입점의 구체 바인딩 — 직렬화 형식, 물리 경로·로케이터, 호출 규약, Plugin bundle 배치·배선·제거 방식, 배포 채널, 포함 확장 요소의 등록 표면 — 은 전부 **Adapter Binding 문서 소관**이다 (01 §4, 10 §4.1·§4.2). 이 Core 서술자에는 그 어떤 물리 경로·형식 토큰도 하드코딩하지 않는다 (framework/runtime/module-manifest.md §3 `entrypoint` 회피 규칙 정합).
- 이 분리로 실행 환경 이식·교체(01 §8 예1, 10 §4.2 이식 교체 지점) 시에도 이 Manifest의 안정 식별자(`id`·`contract`)와 `entrypoint` 추상 참조는 유지되고, 물리 바인딩만 Adapter 경계에서 교체된다.
- 네 연산이 소비하는 Runtime 연산(Register/Resolve/Deregister, 01 §3.1-A)의 물리 배선, 그리고 포함 확장 요소(Hook/Skill)의 등록 표면 바인딩 역시 Adapter 소관이다(10 §4.1·§4.2, 확장 요소 표면은 08·09 §4 소관). 이 Core 서술자는 연산을 추상 참조로 노출할 뿐 물리 배선을 기입하지 않는다.

---

## §5. 결정 기록 (Advisor 결정 — DP-E5 + Advisor 확인)

결정 ID + 결론만 둔다(근거는 §3 필드별 — 쌍둥이 서술 제거). DP-E5는 위임의 확정 입력이며 본 문서는 이를 그대로 반영한다.

- **DP-E5 — `contract` = `PluginsInterface`, `id` = `plugins-provider`, `requires` 미선언, `configSchema` 미선언.** 네 값을 이렇게 확정한다(저장소 사전 명명 부재 → Advisor 결정 사안. Glossary 표제어 "Plugins"(§3.2-D) + 관례 접미 "Interface"·"-provider"의 조합이며 Verifier DP-V1·Loop DP-L1·Workflow DP-W1과 동형). `requires`·`configSchema` 미선언 근거 = §3. 두 식별자는 필드 **값**이지 Glossary 표제어 신설이 아니며, 그 계약의 정본은 10 §3이 유지한다(§0·§6).
- **Advisor 확인 — `id`·`version` 인스턴스 값 (2026-07-06).** 두 값이 승인되었다(`id`는 DP-E5 명명 결정으로, `version`은 Manifest 인스턴스 관례로 채운 값). 미확정 잔여 = 없음.

---

## §6. 정본 경계·금지 토큰 준수 (self-note)

- **재정의·확장 0.** 본 문서의 7필드는 01 §3.2-A의 인스턴스이며 어떤 필드도 이 문서에서 진위가 확정되지 않는다 — 판정 기준은 01 §3.2-A(필드 계약)와 framework/runtime/module-manifest.md(형식 규격)다. 배포·수명주기 계약(10 §3)은 § 포인터로만 참조했다. 필수/선택 표기를 정본 그대로 보존했고, `requires`의 선택 지위를 바꾸지 않은 채 기본(없음)을 취했으며 새 필드를 추가하지 않았다.
- **새 계약·용어 0.** `requires`에서 존재하지 않는 contract를 신설하지 않았다(하드 의존 자체를 두지 않았다). `PluginsInterface`·`plugins-provider`는 각각 `contract`·`id` 필드의 **값**이며 Glossary 표제어 신설이 아니다(§5 DP-E5).
- **금지 토큰·Glossary 경계.** 금지 토큰 규칙과 정당 매치 분류(계약 필드 값·연산명·Glossary 정본 어휘·저장소 문서 식별자)의 판정 기준은 framework/core/structure.md §5 C-3 확장이 소유한다(01 INV-4, 10 INV-10). 진입점·bundle 배치·배포 채널·역할 실행 채널·Runtime 연산 배선의 물리 실현이 필요한 자리에는 "Adapter Binding 문서 소관(01 §4, 10 §4.1·§4.2)" 포인터만 두고 특정 Adapter Binding 문서명·물리 경로를 인용하지 않는다(mention/use 경계).
- **미완성 형제 산출물 비인용 (07 R2).** 같은 병렬 집합에서 동시 작성 중일 수 있는 형제 산출물은 추측·인용하지 않았다. 함께 작성되는 plugin-manifest.md는 이 Provider Manifest와 **다른 서술자**임을 §0·§3에서 구분 지시하되 그 내부 내용을 인용하지 않고 소관 포인터로만 지시했다.
- **미확정·open 잔여 = 없음.** `contract`·`id` 명명·`requires` 미선언·`configSchema` 미선언(DP-E5)은 Advisor 결정, `id`·`version`은 Advisor 확인(2026-07-06)으로 확정되었다(§5).
