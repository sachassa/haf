# framework/adapters/claude/plugins-binding — Claude Code Plugins Adapter 바인딩

작성일: 2026-07-06
상태: v0.9 Baseline (CP2 Pass · CP3 승인 · 사용자 승인 2026-07-06). 기준선 이력 = §9.
상위 규약: AGENT.md
근거 정본 (재정의 0 — 계약은 § 포인터로만 인용한다):

- specs/10-plugins.md §3.1·§3.2·§3.3(4연산·Plugin Manifest·공통 Failure Report·INV-1~10)·§4.1(Claude Code Binding 표 8행)·§4.2(이식 교체 지점 5건)·§9(결정 기록 — 01 Deregister 추가·OQ-P1 Config scope 불변·08/09 조율·Glossary J-10).
- specs/01-runtime.md §3.1-A(Register/Resolve/Replace/**Deregister**)·§4.1("Module 구현 디렉터리 = `framework/{loop,memory,verifier,workflow,plugins}/`" Frozen 문면).
- framework/plugins/module-manifest.md·plugin-manifest.md·plugin-lifecycle.md (EX-P1 확정본) — Provider 등록 서술자(`id`=`plugins-provider`·`contract`=`PluginsInterface`·`requires`/`configSchema` 미선언, DP-E5)·Manifest 6필드/Failure Report 4필드+`reason` 11종 포맷·4연산 규칙과 검사(I1~I5·A1~A2·D1·R1~R2·IG). 세 문서가 "직렬화 형식·물리 위치·`entrypoint` 물리 해소·bundle 배치·배포 채널·검사 물리 실행 방식은 Adapter Binding 소관"으로 미룬 지점의 소관자가 본 문서다(module-manifest.md §4·plugin-manifest.md §4·plugin-lifecycle.md §3.7·§6).
- framework/adapters/claude/runtime-binding.md §3.2 — **Register/Resolve/Deregister 수행 방식의 정본**. 본 문서 §4·§5는 참조만 하고 재정의하지 않는다. 자매 {workflow,memory,verifier,loop}-binding.md — 표·형태 A/B·SP 대응 관례, DP-W4/DP-L4 대비 대상(§3.4).
- specs/00-glossary.md §3.2-J(J-10)·§3.2-D — 새 용어 신설 0. docs/delegation-protocol.md §3 — 역할 실행 물리 채널. ROADMAP.md v0.8 — "본체 수정 없는 확장"의 환경 실현 근거.

경계·전제·거버넌스(공통): 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**이므로 구체 AI·환경·직렬화 형식·물리 경로 토큰이 허용되는 **격리 지점**이고(structure.md §5 금지 토큰 C-3 비적용·§2 4경계 배치·§4 계약/실행 코드 배치), 이 하네스는 **Bootstrap 상태**이며(Glossary J-13), 용어는 specs/00-glossary.md 정본만 쓰고, 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3). Core Contract(10 §3)와 framework/plugins/ 3문서를 재정의하지 않는다.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/10-plugins.md §3·§4와 framework/plugins/ 3문서다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(네 연산·데이터 포맷·불변 규칙·Manifest 필드·`reason` 열거·검사 규칙)를 **재정의·확장하지 않는다** — 정본 § 포인터로만 인용한다.
- **격리 지점의 방향 반전(C-3 비적용).** framework/plugins/ 3문서 본문은 AI·언어·툴체인·직렬화·물리 경로 토큰이 0건이어야 하지만(structure.md §5, 10 INV-10), 이 문서는 그 **반대편**이며 구체 토큰 사용이 허용된다 — 그 격리가 이 경계의 존재 이유다.
- **Plugin bundle·설치본 물리 위치 정본 선언(Advisor 결정 DP-E6).** ⓐ bundle 원본 = `docs/v0.8-demo-fixtures/` 격리 경계 내 자기완결 디렉터리 · ⓑ Install 설치본 = `framework/plugins/<plugin-id>/` 하위 자기완결 배치 · ⓒ Remove 후 framework/plugins/는 3문서만 잔존(잔여물 0의 물리 판정 = 설치 이전 파일 목록 전수 대조) · ⓓ AI 의존 산출물은 `.claude/` 경계로 격리(INV-4). 상세·근거는 §3이 소유한다. 설치본 배치는 새 데이터 백엔드 신설이 아니라 01 §4.1·10 §4.1 행 6 Frozen 문면의 직접 인스턴스다(DP-W4 동형·DP-L4와 상이 — §3.4).
- **배포 채널 형태 B 정직 구분(DP-E3 동형).** 배포 채널(10 §4.1 행 8)은 형태 B다 — 형태 A(Bootstrap)의 배포 = bundle 원본의 격리 경계 보유 + 수동 규약 Install(§3.3·§6). 라이브 하네스 설정 파일을 생성·수정하지 않는다.
- **창설 금지.** 10 §4.1 표를 넘어서는 새 바인딩 계약을 창설하지 않는다 — 새 연산·새 필드·새 `reason`·새 불변 규칙·새 Config scope 0(INV-7 재확인).
- **형태 구분(정직).** `형태 A`(문서·규약 실현)·`형태 B`(실행 코드 예정)는 structure.md §4의 서술 라벨이다. Bootstrap에서 Plugins는 규약 문서와 관행(수동 규약 Install/Activate/Deactivate/Remove)으로 실현되며, 본 문서의 매핑은 물리 실재 / 형태 B 예정 / 시연 소산을 구분한다(§2 "실재 여부" 열·§7).
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다. bundle 원본이 놓인 `docs/v0.8-demo-fixtures/`는 산출물 수명 정책(docs/artifact-lifecycle-policy.md §7)으로 작업 트리에서 제거되었으므로 관련 실재 서술은 **앵커 `cd9247b` 열람** 대상이며, DP-E6의 결정·규약과 설치본 경로(계약)는 유지된다. uaf-allow-legacy: 삭제된 시연 픽스처를 가리키는 종전 결정 기록의 보존 인용.

---

## §1. 목적

이 문서는 10 §4.1(Plugins Claude Code Binding) 바인딩 표 **8행 전부**를 이 환경의 구체 물리 실현으로 매핑한다 — bundle·설치본 물리 위치와 4연산의 예/아니오 판정 가능한 물리 절차 + DP-E6 결정 기록(§2·§3), `entrypoint` 물리 해소(§4), 검사 물리 판정 지점(§5), 이식 교체 지점 5건 대응(§6), 상태 서술 실측 대조(§7).

Bootstrap 상태의 물리 실재 / 규약 실현(형태 A) / 형태 B 예정 / 시연 소산을 "실재 여부" 열로 정직하게 구분한다. 10 §3·framework/plugins/ 3문서의 계약 요소는 재정의·확장하지 않으며, 형태 A → 형태 B 전환 시에도 Core Contract 변경은 0이다(structure.md §7 C-1) — §6 "유지되는 것" 열이 그 불변을 이식 축에서 재확인한다.

---

## §2. 10 §4.1 바인딩 표 8행 물리 실현 (done 1)

10 §4.1 Claude Code Binding 표의 **8행 전부**를 물리 표면으로 매핑한다. "10 §4.1 바인딩(정본 인용)" 열은 정본 표현을 **원문 그대로** 인용하고, "물리 실현" 열이 이 환경의 경로·형태·채널·절차를, "실재 여부" 열이 물리 실재/형태 A/형태 B/시연 소산을 정직하게 구분한다(§7·L-07).

관련 물리 경계: `framework/plugins/` = Module 구현 디렉터리(Core-side) — 3문서 최상위 + 설치본 `<plugin-id>/` 하위 자리 · `framework/adapters/claude/` = 본 Adapter 경계 · `.claude/{agents,commands,hooks,skills}` = 등록 표면·AI 의존 격리 · `docs/v0.8-demo-fixtures/` = bundle 원본 자리(앵커 `cd9247b`).

| # | §3 계약 요소 (정본 §) | 10 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Plugin bundle (10 §3.1 Install 입력) | Claude Code plugin 디렉터리 — self-contained 배포 단위. | bundle 원본 = `docs/v0.8-demo-fixtures/` 격리 경계 내 자기완결 디렉터리(DP-E6 ⓐ). 내부에서도 Core/Adapter 분리 유지(10 §4.1 말미). 물리 위치 정본 = §3.1. | 시연 소산 — 앵커 `cd9247b` 열람(§7). |
| 2 | Plugin Manifest(§3.2-A) 직렬화 | Markdown + front-matter 또는 설정 파일. Module Manifest 직렬화(01 §4.1)와 동일 관례. | 직렬화 = **문서 형태**(Markdown 본문 + front-matter 또는 설정 파일) — Module Manifest 직렬화(runtime-binding.md §3.1)와 동일 관례. 6필드 포맷 정본 = plugin-manifest.md §2(재정의 0). | 직렬화 형식 관례 실재(자매 바인딩·`.claude/agents/*.md` front-matter가 형식 예시). Manifest 인스턴스는 시연 소산(§7). |
| 3 | 포함 Module 등록 (Activate) | 01 §4.1의 Register 바인딩 경유 — `.claude/agents/`, `.claude/commands/`, `.claude/hooks/`, `.claude/skills/` 확장 표면에 등록. | Activate = `provides` 각 Module Manifest를 **Runtime Register**로 등록하고 `requires`를 Resolve(10 INV-2). AI 비의존 Module 구현은 Core-side `framework/plugins/<plugin-id>/`(행 6), 확장 표면 등록은 `.claude/{agents,commands,hooks,skills}`. 번들 Hook/Skill 등록 표면은 **08 §3.1-C·09 §3.1-A 소관**(SP-5). 절차 = §3.2·§4. | 규약 실현(형태 A) — `.claude/agents/` 4종·runtime-binding.md 실재(§7). 무인 자동 등록 실행 코드(형태 B) 미도입. |
| 4 | Install | Plugin 디렉터리 배치 (본체 파일 미수정). | Install = bundle 원본을 설치본 `framework/plugins/<plugin-id>/`로 배치(DP-E6 ⓑ) — 본체 무수정(INV-1), 새 하위 디렉터리 추가만, 상태 = registered-but-inactive. 절차·검사 = §3.2·§5. | 규약 실현(형태 A). 설치본 부재 = Remove 잔여물 0(§7). |
| 5 | Deactivate / Remove | 등록 배선 해제와 Plugin 디렉터리 제거. | Deactivate = 활성화 역순 **01 §3.1-A Deregister**. Remove = 설치본·등록 배선·(AI 의존 시) `.claude/` 산출물 제거 + **잔여물 0 = 설치 이전 파일 목록 전수 대조**(DP-E6 ⓒ). 절차 = §3.2·§3.3. | 규약 실현(형태 A). 시연에서 Deactivate·Remove 실증(§7). |
| 6 | 포함 Module의 AI 비의존 구현 | Core-side module 디렉터리(예: `framework/plugins/`, 01 §4.1)에 위치. AI 의존 요소 0건 유지. | 설치본의 AI 비의존 Module 구현 = `framework/plugins/<plugin-id>/`(DP-E6 ⓑ — 01 §4.1·10 §4.1 Frozen 문면의 직접 인스턴스, 새 백엔드 아님; §3.4). AI 의존 요소 0건 유지(INV-4). 3문서와는 하위 디렉터리 격리로 비중첩. | `framework/plugins/` 경계·3문서 실재. 설치본 하위 디렉터리 부재 = Remove 잔여물 0(§7). |
| 7 | AI 의존 산출물 | `.claude/` 등 Adapter 경계로 격리 (INV-4). | AI 의존 산출물은 `.claude/` 등 Adapter 경계로 격리한다(DP-E6 ⓓ, INV-4). v0.8 레퍼런스 Plugin은 AI 비의존(DP-E2)이라 이 경로는 **구조만 확정**(미사용). | `.claude/` 격리 경계 실재. 이 레퍼런스 Plugin의 AI 의존 산출물은 없다(구조만 확정, DP-E6 ⓓ). |
| 8 | 배포 채널 | Claude Code plugin 설치 메커니즘(marketplace 등). | 형태 A = bundle 원본의 격리 경계 보유 + 수동 규약 Install(DP-E3 동형). marketplace 등 자동 설치 메커니즘은 형태 B로 이연한다(라이브 하네스 설정 파일 무수정). SP-4(§6). | 형태 A 수동 규약 실현. 자동 배포 채널(형태 B) 미도입. |

주:

- **역할 실행 = Agent Module(서브에이전트 채널).** 4연산 실행이 Agent 역할 흐름에 얹히더라도 그 역할 디스패치는 위임·보고 메시지(02) 흐름이지 module Resolve가 아니다(module-manifest.md §3 — 역할 실행은 `requires`에 넣지 않음). 물리 채널은 서브에이전트 위임/최종 응답(delegation-protocol.md §3)이다.

---

## §3. Plugin bundle 물리 위치·4연산 물리 절차 + DP-E6 결정 기록 (done 2·5)

10 §3.1이 정의한 네 연산과 plugin-lifecycle.md가 규칙으로 전개한 완료 조건을, 이 환경의 **예/아니오 판정 가능한 물리 절차**로 확정한다. 입력·출력·완료 조건·실패 reason·검사 규칙의 정본은 10 §3.1·§3.2와 plugin-lifecycle.md(§2·§3)이며, 본 절은 그 물리 실현만 확정한다(재정의 0).

### §3.1 Plugin bundle·설치본·격리 물리 위치 (DP-E6 ⓐ·ⓑ·ⓓ)

- **bundle 원본(ⓐ).** self-contained 배포 단위(10 §4.1 행 1)는 `docs/v0.8-demo-fixtures/` 격리 경계 내 자기완결 디렉터리에 존치한다(v0.5~v0.7 시연 픽스처 관례와 동형). bundle 내부에서도 Core/Adapter 경계를 유지해 AI 비의존 Module 구현과 (있다면) AI 의존 바인딩을 물리적으로 분리해 담는다(10 §4.1 말미).
- **설치본(ⓑ).** Install은 bundle 원본을 `framework/plugins/<plugin-id>/` 하위 자기완결 디렉터리로 배치한다. `<plugin-id>`는 Plugin Manifest `id`(안정 식별자, 10 INV-9·plugin-manifest.md §2)이며, 이 디렉터리명이 곧 설치본의 유일성 기준이다(§3.2 I4). AI 비의존 Module 구현은 이 Core-side 디렉터리에, (있다면) AI 의존 산출물은 `.claude/`에(ⓓ) 격리한다.
- **비중첩(ⓑ).** Plugins 서브시스템 자기 문서 3건(최상위 배치)과 설치본(하위 디렉터리)의 경계는 **하위 디렉터리 격리로 비중첩**이다. 파일 충돌이 없으므로 설치는 3문서를 수정하지 않는다(INV-1 정합, §3.2 I1).
- **AI 의존 격리(ⓓ).** AI 의존 산출물이 있는 Plugin이면 그 산출물은 `.claude/` 경계로 격리한다(10 §4.1 행 7, INV-4). v0.8 레퍼런스 Plugin은 AI 비의존 문서형 Module 1개 번들(DP-E2)이므로 이 경로는 **구조만 확정**하고 실사용하지 않는다.

### §3.2 4연산 물리 절차 (예/아니오 판정 가능)

각 연산의 물리 절차다. 완료 성립 = plugin-lifecycle.md §3의 해당 검사가 모두 "예"(§5). 검사 규칙 자체는 § 포인터로 소비하며 여기서는 물리 수행 순서만 확정한다.

- **Install (설치본 배치 + I1~I5·IG).**
  1. bundle 원본(`docs/v0.8-demo-fixtures/<plugin>`)과 Plugin Manifest(plugin-manifest.md §2)를 입력으로 받는다.
  2. I2(frameworkCompat 포함) → I3(dependsOn 기설치 전수) → I4(`<plugin-id>` 디렉터리명 유일) → I5(자기완결 — 선언 밖 본체 내부 경로 은닉 의존 0) → IG(격리 불변 INV-4/5/6) 검사(§5)를 대조한다. 하나라도 "아니오"이면 배치하지 않고 공통 Failure Report(plugin-manifest.md §3)를 낸다.
  3. 전부 "예"이면 설치본을 `framework/plugins/<plugin-id>/`에 배치한다. **본체 미수정(I1)** — 기존 3문서·Core 경계 파일 diff = 0.
  4. 출력: 설치된 plugin id, 상태 registered-but-inactive. (예/아니오: 설치본 디렉터리가 존재하고 본체 diff = 0인가?)
- **Activate (Register/Resolve + A1~A2).**
  1. 설치된 plugin id를 입력으로 받는다.
  2. A1: `provides`의 각 Module Manifest를 Runtime Register(01 §3.1-A, runtime-binding.md §3.2)로 등록한다 — 정의 파일 배치, `id` 유일성 확인, 반환 핸들 획득. 번들된 확장 요소(Hook/Skill) 등록 표면은 08 §3.1-C·09 §3.1-A 소관(포인터).
  3. A2: `requires` contract를 Runtime Resolve(01 §3.1-A)로 해소한다 — 활성 바인딩 정확히 1개 확인.
  4. 출력: 등록된 module id 목록. (예/아니오: provides 전수 Register 성공 ∧ requires 전수 Resolve 성공인가?)
- **Deactivate (역순 Deregister + D1).**
  1. 활성 plugin id를 입력으로 받는다.
  2. D1: `provides`의 각 Module을 활성화 **역순**으로 01 §3.1-A Deregister(runtime-binding.md §3.2 — 정의 파일 제거·바인딩 해제)한다. 다른 Plugin이 제공한 계약 소비자 참조는 침범하지 않는다(01 Deregister 완료 조건 — 의존 중이면 해제 거부, plugin-lifecycle.md §4).
  3. 출력: 비활성화 결과. (예/아니오: provides 전수가 역순 비활성화·바인딩 해제 완결이고 타 Plugin 소비자 비침범인가?)
- **Remove (전수 대조 제거 + R2·R1).** 논리 순서 = R2(의존 부재 게이트) → 제거 수행 → R1(잔여물 0 확인).
  1. 설치된(가능하면 비활성) plugin id를 입력으로 받는다.
  2. R2: 기설치 Plugin 집합의 `dependsOn` 전수를 대상 Plugin에 대해 대조한다. 의존하는 Plugin이 하나라도 있으면 제거를 거부한다(reason=DependentExists).
  3. 제거 수행: 등록 Module을 01 §3.1-A Deregister로 제거하고, 설치본 디렉터리(`framework/plugins/<plugin-id>/`)·등록 배선·(AI 의존 시) `.claude/` 산출물을 제거한다.
  4. R1: **잔여물 0 스캔**(§3.3)을 수행한다.
  5. 출력: 제거 결과. (예/아니오: R2 게이트 통과 ∧ R1 잔여물 0인가?)

### §3.3 Remove 잔여물 0 스캔 = 설치 이전 파일 목록과의 전수 대조 (DP-E6 ⓒ)

Remove의 R1(잔여물 0, plugin-lifecycle.md §3.5 R1 / 10 INV-3)을 이 환경에서 **예/아니오 판정 가능한 전수 대조 절차**로 확정한다.

1. **설치 이전 스냅샷.** Install 착수 **전**, 영향 경계 전체의 파일 목록을 스냅샷으로 확보한다 — 최소한 `framework/plugins/`(기준선 = {`module-manifest.md`, `plugin-manifest.md`, `plugin-lifecycle.md`}), Activate가 등록 표면으로 쓴 `.claude/{agents,commands,hooks,skills}`, (AI 의존 시) `.claude/` 산출물 경로. 이것이 "본체의 설치 이전 상태"(10 INV-3)다.
2. **제거 후 재열거.** Remove 수행 후 동일 경계의 파일 목록을 다시 열거한다.
3. **전수 대조.** 두 목록의 차집합을 계산한다. **차집합이 0**(제거 후 목록 = 설치 이전 스냅샷)이면 R1 = 예(잔여물 0). 설치본 디렉터리·등록 정의 파일·배선·(AI 의존 시) `.claude/` 산출물이 모두 사라지고 `framework/plugins/`는 3문서만 잔존한다.
4. **전 부류 전수(정직).** 추가 산출물의 **전 부류**(등록 Module·배치 파일·배선)를 스캔한다 — 한 부류(예: 등록 Module)만 제거 확인하고 다른 부류(배치 파일·배선)를 통과로 간주하지 않는다(좁은 대리 지표 금지, plugin-lifecycle.md §3.1 검사 범위 정직 — 2026-07-26 §3.5 개별 조항의 §3.1 전역 통합에 따른 좌표 갱신). 차집합이 0이 아니면 R1 = 아니오, reason=ResidueDetected, `location` = 잔여물 지점.
5. **검증 정합.** 이 절차는 10 §7 검증 방법("Verifier가 Remove 후 잔여물 스캔 = 0을 확인")의 물리 실현이며, 파일 시스템 목록 대조로 예/아니오가 결정된다.

### §3.4 DP-E6 결정 기록 — 설치본 배치와 01 §4.1 Frozen 문면 (done 5)

- **결정(DP-E6, Advisor 확정 입력 — 임의 변경 금지).** ⓐ bundle 원본 = `docs/v0.8-demo-fixtures/` · ⓑ 설치본 = `framework/plugins/<plugin-id>/` · ⓒ Remove 잔여물 0 = 설치 이전 파일 목록 전수 대조 · ⓓ AI 의존 산출물 = `.claude/` 격리(v0.8 레퍼런스 Plugin은 AI 비의존이라 구조만 확정).
- **판정 결과: 01 §4.1·10 §4.1 Frozen 문면·INV-1~10과 충돌 0.** 설치본 배치는 정본이 이미 Module 구현 디렉터리로 지정한 `framework/plugins/` 하위의 **인스턴스**이므로 새 백엔드 창설이 아니며(§0 창설 금지), structure.md §3 규칙 2(자기완결)·INV-1(추가만의 확장)·INV-4(Core AI 비의존 + `.claude/` 격리)와 정합한다. 논증 산문의 종전 문면 = git 앵커 90ca19c.
- **DP-W4와 동형·DP-L4와 상이.** 정본 문면이 물리 디렉터리를 이미 지정했으므로 새 백엔드 신설이 불필요하다(DP-L4는 정본이 경로를 열어 둔 경우 — 사실 관계가 다르다).
- **충돌 판단 시 처리.** 설치본 배치가 어떤 Frozen 문면(01·10 §4.1, INV-1~10)과 충돌한다면 구현하지 않고 Advisor에게 실패 보고한다(structure.md §7 C-1·plugin-lifecycle.md §0).

---

## §4. Plugins Provider `entrypoint` 물리 해소 (done 4)

module-manifest.md §2·§4가 "`entrypoint`(Install/Activate/Deactivate/Remove 연산 노출 진입점)의 물리 해소는 Adapter Binding 문서 소관"으로 미룬 지점을 확정한다. loop-binding.md §4.1·workflow-binding.md §4.1의 `entrypoint` 물리 해소 표 관례(추상 참조 → 물리 실현, 형태 A/B 구분)와 동형이다.

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Install(10 §3.1) 노출 — self-contained bundle 1건 설치, registered-but-inactive | **형태 A:** bundle 원본을 설치본 `framework/plugins/<plugin-id>/`으로 배치(DP-E6 ⓑ)·본체 무수정(INV-1)·I1~I5·IG 대조(§5). 별도 실행 진입점 파일은 없다 — 수동 규약 배치. | 규약 실현(형태 A) |
| Activate(10 §3.1) 노출 — 포함 Module Register/Resolve 활성화 | **형태 A:** `provides` Register + `requires` Resolve(01 §3.1-A, runtime-binding.md §3.2)·A1~A2 대조(§5). 확장 요소 등록 표면은 08 §3.1-C·09 §3.1-A 소관. | 규약 실현(형태 A) |
| Deactivate(10 §3.1) 노출 — 활성화 역순 비활성화·바인딩 해제 | **형태 A:** 활성화 역순 01 §3.1-A Deregister(runtime-binding.md §3.2)·D1 대조(§5). | 규약 실현(형태 A) |
| Remove(10 §3.1) 노출 — 잔여물 0으로 제거 | **형태 A:** 설치본·등록 배선 제거(01 Deregister) + 설치 이전 파일 목록 전수 대조로 잔여물 0 판정(§3.3)·R2→R1 대조(§5). | 규약 실현(형태 A) |
| 위 4연산의 실행 코드 로케이터 | **형태 B:** 4연산을 사람 없이 자동으로 트리거·수합하는 실행 코드가 non-core 실행 경계(`framework/plugins/` 또는 `framework/adapters/claude/`)에 배치된다. 경계 간 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취 금지). | 형태 B |

- **Register/Resolve 정합.** Provider 자체의 등록(Register)은 Manifest + 본 바인딩 배치로 규약 실현되고(형태 A), 해소(Resolve)는 소비자가 `contract` `PluginsInterface`로 요청할 때 이 Provider로 이뤄진다. Provider가 처리 대상 Plugin의 provides를 Register하고 requires를 Resolve하는 것(Activate)은 그 연산의 완료 조건이지 Provider 자신의 Resolve 게이트가 아니다(module-manifest.md §3 requires 미선언). 이 경로는 SP-2에 대응한다(§6).
- **`requires`·`configSchema` 미선언 재확인(DP-E5).** module-manifest.md §3·§5의 결정은 불변이며 본 문서는 재정의하지 않는다. Provider가 소비하는 Runtime 연산의 물리 배선은 runtime-binding.md §3.2 참조다.

---

## §5. plugin-lifecycle.md 검사 물리 실행 지점 (done 3)

plugin-lifecycle.md §3의 검사(I1~I5·A1~A2·D1·R1~R2·IG)를 이 환경의 **물리 판정 지점**으로 확정한다. **검사 규칙 자체(판정 형태·대응 연산·완료 조건·reason 결합)는 plugin-lifecycle.md §3이 소유하며 본 표는 재게재하지 않는다** — 본 표는 각 검사의 **물리 실행 방식**만 확정한다(reason 포맷 = plugin-manifest.md §3, 판정 규칙 = 10 §3.1, 재정의 0).

| 검사 (규칙 정본: plugin-lifecycle.md §3) | 물리 실행 방식 (claude 환경) | 형태 |
|---|---|---|
| **I1** 본체 불가침 | Install 전후 본체(`framework/core/`·`framework/runtime/`·기존 spec·기존 3문서·이미 등록된 Module) **파일 시스템 diff = 0** 확인(10 §7 — Verifier가 Install 전후 본체 diff=0 확인). 설치본은 새 하위 디렉터리 추가만이므로 diff는 추가 경로에 국한된다(§3.4 c). | 규약 실현(형태 A) |
| **I2** Framework 호환 | Plugin Manifest `frameworkCompat` 범위가 현재 Framework 버전(v0.8)을 포함하는지 대조. | 규약 실현(형태 A) |
| **I3** 의존 Plugin 기설치 | `dependsOn`의 각 plugin id가 설치본 집합(`framework/plugins/` 하위 디렉터리 집합)에 존재하는지 **전수** 대조. | 규약 실현(형태 A) |
| **I4** plugin id 유일 | 설치될 `<plugin-id>`가 기설치 설치본 디렉터리명과 충돌하지 않는지 대조(설치본 = `framework/plugins/<plugin-id>/`이므로 디렉터리명 충돌 = `id` 충돌). | 규약 실현(형태 A) |
| **I5** 자기완결 | bundle이 선언(`requires`·`dependsOn`) 밖의 본체 내부 경로에 은닉 의존하지 않는지 bundle **전체** 스캔. | 규약 실현(형태 A) |
| **A1** provides 등록 | `provides`의 각 Module Manifest를 Runtime Register(01 §3.1-A, runtime-binding.md §3.2 — 정의 파일 배치·`id` 유일성)로 등록하고 반환 핸들 확인(10 §7 — Register/Resolve 호출·반환 핸들 확인). 전수. | 규약 실현(형태 A) |
| **A2** requires 해소 | Plugin Manifest `requires` contract를 Runtime Resolve(01 §3.1-A)로 해소, 활성 바인딩 정확히 1개 확인. 전수. | 규약 실현(형태 A) |
| **D1** 비활성화 완결 | `provides`의 각 Module을 활성화 역순으로 01 Deregister(runtime-binding.md §3.2)하고, 다른 Plugin 제공 계약 소비자 비침범을 전수 대조. | 규약 실현(형태 A) |
| **R2** 의존 Plugin 부재 | 기설치 Plugin 집합의 `dependsOn` 전수를 대상 Plugin에 대해 대조(제거 착수 전 게이트). | 규약 실현(형태 A) |
| **R1** 잔여물 0 | 설치 이전 파일 목록과 Remove 후 목록의 **전수 대조**(§3.3) — 전 부류(등록 Module·배치 파일·배선) 스캔(10 §7 — 잔여물 스캔=0). | 규약 실현(형태 A) |
| **IG** 격리 불변 가드 | 포함 Module의 Memory 접근이 단일 Port(memory-binding.md 백엔드 경유)만 경유하는지(INV-5), Core 배치(`framework/plugins/<plugin-id>/`)가 AI 비의존인지(INV-4), 역할 경계 비재정의(INV-6)를 포함 요소 **전수** 대조(10 §7 — Memory 접근 경로 단일 Port·Core 배치 AI 비의존 확인). | 규약 실현(형태 A) |

- **10 §7 검증 방법과의 정합.** I1(본체 diff=0)·A1/A2(Register/Resolve 호출·반환 핸들)·R1(잔여물 스캔=0)·IG(Memory 접근 단일 Port·Core 배치 AI 비의존)는 10 §7 "검증 방법"의 각 항목과 1:1 정합한다. 판정 주체·시점·전이는 06·03-loop 소관이며(plugin-lifecycle.md §3.7 경계), 본 문서는 물리 실행 대상만 확정한다.
- **형태 B 전환.** 실행 코드 도입 시 위 검사는 실행 검증기로 실현되며, 판정 규칙(plugin-lifecycle.md §3)·reason 열거(plugin-manifest.md §3)의 변경은 0이다(structure.md §7 C-1).

---

## §6. 10 §4.2 이식 교체 지점 5건 대응 (done 6)

10 §4.2 이식 교체 지점 5건 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인하며, 10 §3 계약(Plugin Manifest 6필드·4연산 완료 조건·INV-1~10)을 커버한다.

| # (10 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Plugin bundle/Manifest 직렬화 → 대상 환경의 패키지·서술자 포맷 | §2 행 1·2, §3.1 | bundle 원본 = `docs/v0.8-demo-fixtures/`, 설치본 = `framework/plugins/<plugin-id>/`, Manifest 직렬화 = 문서 형태. | **Plugin Manifest 6필드**(`id`/`version`/`provides`/`requires`/`dependsOn`/`frameworkCompat`, 10 §3.2-A·plugin-manifest.md §2); **공통 Failure Report 4필드·`reason` 11종**(10 §3.2-B·plugin-manifest.md §3); **INV-8(자기완결성)·INV-9(안정 식별자)**. |
| SP-2 | 포함 Module 등록 표면 `.claude/{agents,commands,hooks,skills}` → 대상 환경의 Module 로더·확장 등록 메커니즘 | §2 행 3, §4·§5 | `.claude/{agents,commands,hooks,skills}` 확장 표면 + Core-side `framework/plugins/<plugin-id>/` 배치, Register/Resolve 규약 실현(runtime-binding.md §3.2). | **Activate 완료 조건·INV-2(Register/Resolve 경유)**(10 §3.1·§3.3); **A1·A2 검사**(plugin-lifecycle.md §3.3); **INV-4/5/6(격리 불변)**(IG 검사). |
| SP-3 | Install/Activate/Deactivate/Remove의 물리 실현 → 대상 환경의 패키지 매니저 | §3, §4 | 디렉터리 배치·배선·전수 대조 제거 — 형태 A 규약 실현 / 형태 B 실행 코드 로케이터. | **4연산 입력·출력·완료 조건·실패 reason**(10 §3.1·plugin-lifecycle.md §2); **INV-1(본체 불가침)·INV-3(잔여물 0)**; **I1~I5·D1·R1~R2 검사**. |
| SP-4 | 배포 채널 Claude Code plugin 설치 메커니즘(marketplace 등) → 대상 환경의 배포·레지스트리 채널 | §2 행 8, §3.3(DP-E3 동형) | 형태 A: bundle 원본의 격리 경계 보유 + 수동 규약 Install; 자동 채널(marketplace 등)은 형태 B(미도입). | **INV-1(본체 불가침)·INV-8(자기완결성)**; 배포는 계약(10 §3.1)의 물리 채널일 뿐 계약 요소를 바꾸지 않는다. |
| SP-5 | 확장 요소(Hook/Skill) 표면 바인딩 — 08/09의 §4 소관. Plugins는 참조만 | §2 행 3, §4·§5 | 08/09 §4 소관(참조만) — Plugins는 번들·제거만 소유하고 확장 요소의 등록 표면을 정의하지 않는다. | **08 §3.1-C·09 §3.1-A 등록 계약** + 10이 소유하는 **배포·제거 계약**(10 §9 결정 기록); Plugins의 `provides` 포함 요소 참조 수준(10 §3.2-A). |

- **유지 열이 10 §3 계약을 전건 커버.** Manifest 6필드 = SP-1 · 4연산 완료 조건·실패 reason = SP-2(Activate)·SP-3(Install/Deactivate/Remove) · 공통 Failure Report·`reason` 11종 = SP-1 · INV-1 = SP-3·SP-4, INV-2 = SP-2, INV-3 = SP-3, INV-4/5/6 = SP-2, INV-7·INV-10 = 아래 주, INV-8 = SP-1·SP-4, INV-9 = SP-1. 이식해도 바뀌지 않는다(structure.md §7 C-1). uaf-verified: 10 §3 계약 요소(6필드·4연산 완료 조건·Failure Report·INV 10건)를 SP-1~5에 1:1 사상해 열거 — 미대응 0.
- **INV-7·INV-10 이식 불변(주).** INV-7(새 Config scope 미도입 — Global/Project/Module 유지)은 본 문서가 새 scope를 도입하지 않음으로 준수하고(§0 창설 금지·OQ-P1 승인), INV-10(§3 계약 AI 비의존)은 환경 의존 토큰을 이 Adapter 경계에만 격리함으로 유지된다 — 이식 시 이 경계의 물리 토큰만 교체된다.
- **정식화 이연.** 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(10 §4.2 말미) — 본 문서는 선취하지 않는다(§0).

---

## §7. 상태 서술 실측 대조 (done 7 — L-07 재발 방지)

Active Lesson L-07(상태 서술은 실측 후 기록)에 따라 "실재/존재" 서술을 파일 시스템과 직접 대조한다. 아래 표는 날짜 박힌 byte·파일 수 스냅샷을 재기록하지 않고 **불변 주장**만 남긴다 — 스냅샷은 다시 썩기 때문이다. uaf-verified: `ls framework/plugins/`·`find framework/plugins -mindepth 1 -maxdepth 1 -type d`·`ls framework/adapters/claude/`·`ls .claude/ .claude/agents/`·`ls -d docs/v0.*demo*`·`grep -rl PluginsInterface` 직접 실행(스윕 범위 = 본 문서가 실재를 주장하는 전 경로).

| 대상 | 불변 주장 |
|---|---|
| `framework/plugins/` 3문서 (EX-P1 확정본 — § 포인터 대상) | 실재·무수정 — module-manifest.md·plugin-manifest.md·plugin-lifecycle.md. |
| `framework/plugins/<plugin-id>/` (설치본 — DP-E6 ⓑ·ⓒ) | **부재 = Remove 잔여물 0.** 하위 디렉터리 0건·3문서만 최상위 실재 — 설치 이전 목록 전수 대조 성립(ⓒ). 시연 PS-4의 Install→Activate→Deactivate→Remove 수명주기 완결 결과이므로 이 부재는 오류가 아니라 상태 정합이다. |
| `docs/v0.8-demo-fixtures/` (bundle 원본 — DP-E6 ⓐ) | 산출물 수명 정책으로 작업 트리에서 제거 — 앵커 `cd9247b` 열람(`git show cd9247b:uahf/docs/v0.8-demo-fixtures/…`). DP-E6의 결정·규약과 설치본 경로(계약)는 유지된다. uaf-allow-legacy: 제거된 시연 픽스처의 종전 실재 서술 보존 인용. |
| 자매 Adapter Binding (runtime-binding.md §3.2 = Register/Resolve/Deregister 참조원 · memory-binding.md = IG INV-5 Memory 단일 Port 참조원) | 실재 — §4·§5의 참조가 1:1로 대응한다. |
| `.claude/{agents,commands,hooks,skills}` (Register 표면·AI 의존 격리 경계 — §2 행 3·행 7) | 실재 — `.claude/agents/`는 advisor·planner·verifier·worker.md 4종. v0.8 레퍼런스 Plugin의 AI 의존 산출물은 없다(DP-E2 — 구조만 확정, 미사용). |
| `PluginsInterface`·`plugins-provider` 사전 명명 (§4 근거) | framework/plugins/ 확정본(module-manifest.md·plugin-lifecycle.md)에만 존재하는 `contract`·`id` 필드 **값**이며 Glossary 표제어 신설이 아니다(DP-E5). 사전 바인딩 0. |
| 무인 자동 Install/Activate/Remove 실행 진입점·로더 (형태 B) | 미도입 — Bootstrap 상태(형태 A). `framework/plugins/`에 실행 코드 0. |

- **생성 주체 구분.** 본 문서는 물리 위치·4연산 절차·검사 물리 실행 지점의 **정본(결정 기록·근거)**(§3~§5)만 소유하고, 시연 실물은 **시연 Task(PS-4 · EX-DP)**가 그 정본 구조대로 생성했다 — 본 문서는 시연 실물을 생성·수정하지 않는다(memory-binding.md §7 r2 관례 동형).

---

## §8. 정본 경계·계약 소유 (self-note)

- **소유 경계.** 본 문서는 **물리 실현**(bundle·설치본 물리 위치·4연산 물리 절차·`entrypoint` 물리 해소·검사 물리 실행 지점·이식 교체 지점)만 소유한다. 계약 소유 = Manifest 6필드·Failure Report → plugin-manifest.md/10 §3.2-A·B · 4연산 규칙·검사 → plugin-lifecycle.md/10 §3.1 · Provider 등록 서술자·`entrypoint` → module-manifest.md/01 §3.2-A · Register/Resolve/Deregister 수행 방식 → runtime-binding.md/01 §3.1-A · Memory 백엔드(IG INV-5) → memory-binding.md/04 §4 · 번들 Hook/Skill 등록 표면 → 08 §3.1-C·09 §3.1-A.
- **델타 = 재정의·확장 0.** 새 연산·새 데이터 계약·새 필드·새 `reason`·새 불변 규칙·새 Config scope(INV-7)·새 Glossary 용어 0이고, 10 §4.1 표를 넘는 새 바인딩 계약도 창설하지 않았다. DP-E6은 01·10 §4.1 Frozen 문면의 인스턴스로 충돌 0이다(§3.4). 작성 시점 자가 감사 서술(금지 토큰 스캔·동시 개정 형제 불인용 07 R2·1파일 한정 07 R4)의 종전 문면 = git 앵커 90ca19c.

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-PB-1 (bundle·설치본 내부 세부 구조 — 비차단).** DP-E6이 확정한 것은 물리 **위치·규약**이다. bundle/설치본 **내부**의 파일 구성·디렉터리 세부 구조는 시연 Task의 재량 여지이며(Worker 제안·Advisor 채택 대상) 계약(10 §3) 변경이 아니다.
- **OQ-PB-2 (형태 B 경계 분할 — 비차단).** 무인 자동 4연산 실행 코드가 `framework/plugins/`와 `framework/adapters/claude/` 사이 어디에 분할 배치되는지는 형태 B 설계 시 확정 대상이다(§4, structure.md §4 규칙 4 defer — 선취 금지). Bootstrap(형태 A)에서는 이 분할이 필요하지 않다.
- **OQ-PB-3 (번들 Hook/Skill 표면 정합 — 비차단, Wave 최종 검증 대상).** Plugin이 확장 요소를 `provides`로 번들할 때 그 등록 표면의 물리 바인딩은 08 §3.1-C·09 §3.1-A 소관이며(10 §9·§4.2 SP-5), 본 문서는 Module 부분만 확정했다. 세 규격(10·08·09)의 등록·제거 계약 정합은 Wave 최종 검증에서 확인한다.
