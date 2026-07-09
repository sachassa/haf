# framework/adapters/claude/plugins-binding — Claude Code Plugins Adapter 바인딩

작성일: 2026-07-06
상태: v0.9 Baseline (개정 — §7 시연 후 상태 반영 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06). 직전 기준선: v0.8 Baseline (CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- specs/10-plugins.md §4.1 — Claude Code Binding 표(8행). 본 문서가 물리 실현으로 인스턴스화하는 바인딩 표의 정본.
- specs/10-plugins.md §4.2 — 이식 교체 지점 5건과 "유지되는 것" 목록. 본 문서 §6이 대응을 명시하는 교체 지점의 정본.
- specs/10-plugins.md §3.1·§3.2·§3.3 — 네 연산(Install/Activate/Deactivate/Remove)·데이터 포맷(Plugin Manifest·공통 Failure Report)·불변 규칙(INV-1~INV-10). 본 문서가 준수·대조하는 계약. 재정의하지 않고 § 포인터로만 인용한다.
- specs/10-plugins.md §9 결정 기록 — 01 Deregister 조율 해소(01 §3.1-A에 Deregister 추가 승인)·OQ-P1 승인(Config scope 불변)·08/09 조율(번들 Hook/Skill 등록은 08 §3.1-C·09 §3.1-A, 10은 배포·제거만 소유)·Glossary §3.2-J J-10 추가. 본 문서가 물리 채널 측면에서 보존하는 조율 결정.
- specs/01-runtime.md §3.1-A — Register/Resolve/Replace/**Deregister** 연산. Activate가 소비하는 Register/Resolve, Deactivate/Remove가 소비하는 Deregister의 정본. 본 문서 §4·§5가 § 포인터로만 참조.
- specs/01-runtime.md §4.1 — Runtime Claude Code Binding 표(특히 "Module 구현 디렉터리 = `framework/{loop,memory,verifier,workflow,plugins}/`" 행). DP-E6 ⓑ가 인스턴스화하는 Frozen 정본 문면.
- framework/plugins/module-manifest.md (EX-P1 확정본) — Plugins Provider Module 등록 서술자(`id`=`plugins-provider`·`contract`=`PluginsInterface`·`entrypoint` 추상 참조·`requires` 미선언·`configSchema` 미선언, DP-E5). `entrypoint`의 물리 해소를 Adapter Binding 문서 소관으로 위임(module-manifest.md §4). 본 문서 §4가 그 물리 해소.
- framework/plugins/plugin-manifest.md (EX-P1 확정본) — Plugin Manifest 6필드(10 §3.2-A)·공통 Failure Report 4필드+`reason` 11종(10 §3.2-B) 포맷의 인스턴스 소유 문서. 직렬화 형식·물리 위치·배포 채널을 Adapter Binding 문서 소관으로 위임(plugin-manifest.md §4). 본 문서 §2·§3이 그 물리 실현.
- framework/plugins/plugin-lifecycle.md (EX-P1 확정본) — 네 연산 규칙 인스턴스. 검사 I1~I5·A1~A2·D1·R1~R2·IG ↔ reason 1:1 결합(§3). 검사 규칙의 물리 실행 방식·bundle 배치·배선·배포 채널을 Adapter Binding 문서 소관으로 위임(plugin-lifecycle.md §3.7·§6). 본 문서 §3·§5가 그 물리 실행 지점.
- framework/adapters/claude/runtime-binding.md (v0.3 Baseline) — 자매 Adapter Binding. **Register/Resolve/Deregister 수행 방식의 정본**(runtime-binding.md §3.2 — 정의 파일 배치/로딩/제거의 규약 실현). 본 문서 §4·§5(Activate/Deactivate/Remove 물리 실현)는 그 실현을 참조만 하고 재정의하지 않는다. 형태 A/B 서술 관례·`<adapter>`=`claude` 구체화 선례.
- framework/adapters/claude/workflow-binding.md (§0·§3 — DP-W4 문서 형태 직렬화 선례·관례) — 자매 Adapter Binding. 격리 지점 방향 반전(§0)·정본 문면이 물리 형태를 지정하면 새 백엔드 디렉터리 신설 없이 그 인스턴스로 해소하는 선례(DP-W4, §3.1)·미래 산출물 실재 불주장(L-07) 관례. **본 문서는 그 §7 실측 표·시연 소산 서술을 인용하지 않는다**(동시 개정 중 — 07 R2); 관례 참조는 §0·§3 구조 관례에 한정한다.
- framework/adapters/claude/memory-binding.md·verifier-binding.md·loop-binding.md (관례 표본) — 자매 Adapter Binding. 3열 표 관례·형태 A/B 정직 구분·SP 대응 표·§7 실측 대조·"데이터 미생성, 시연 시 생성 예정" 관례. loop-binding.md §3 DP-L4(새 백엔드 신설)와 본 문서 DP-E6의 사실 관계 차이 대비 대상.
- framework/core/structure.md §2(4경계 배치 — `framework/{...,plugins}/`가 Module 자기완결 구현 경계)·§5(금지 토큰 규칙 C-3 확장 — Adapter 경계는 격리 보유로 비적용). 본 문서 경계의 근거.
- specs/00-glossary.md §3.2-J(J-10: Plugin·Plugin Manifest)·§3.2-D(Plugins). 본 문서는 새 용어를 신설하지 않는다.
- docs/delegation-protocol.md §3 — 이 프로젝트의 물리 채널 바인딩 관행(위임=서브에이전트 디스패치, 보고 회수=최종 응답). 역할 실행 물리 채널의 관행 근거.
- ROADMAP.md v0.8 (Extension System) — 산출물 "본체 코드/규격 수정 없이 확장"의 환경 실현 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core 계약을 특정 실행 환경·AI·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5, 10 §3.3 INV-10), 구체 AI·환경·직렬화 형식·물리 경로 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, runtime-binding.md §0·workflow-binding.md §0과 동형). 단 이 문서는 Core Contract(10 §3)와 그 인스턴스 문서(framework/plugins/ 3문서)를 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다 (docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.8 Draft | 최초 작성. `framework/adapters/claude/` 경계의 여섯 번째 Core 트랙 바인딩. 10 §4.1 바인딩 표 **8행 전건**을 물리 실현("물리 실현(claude 환경)" 열 + "실재 여부" 열)으로 매핑, 형태 A(규약 실현)/형태 B(실행 코드 예정)/데이터 미생성(시연 소산 예정) 정직 구분(§2, done 1). Plugin bundle 물리 위치·4연산(Install/Activate/Deactivate/Remove) 물리 절차 확정 + Advisor 결정 DP-E6 결정 기록(bundle 원본=`docs/v0.8-demo-fixtures/`·설치본=`framework/plugins/<plugin-id>/`·Remove 잔여물 0=설치 이전 파일 목록 전수 대조·AI 의존 산출물=`.claude/` 격리 구조만 확정)·DP-E6이 01 §4.1 Frozen 문면 인스턴스임(충돌 0) 근거 서술(§3, done 2·5). Plugins Provider `entrypoint`(4연산 노출) 물리 해소 표(형태 A/B 구분, §4, done 4). plugin-lifecycle.md 검사(I1~I5·A1~A2·D1·R1~R2·IG) 물리 실행 지점 확정 — 검사 규칙 자체는 § 포인터 소비(재게재 0), 물리 실행 방식만 확정(§5, done 3). 10 §4.2 이식 교체 지점 5건 대응 표("교체되는 것/유지되는 것" — 유지 열이 Manifest 6필드·4연산 완료 조건·INV-1~10 전건 커버, §6, done 6). 상태 서술 실측 대조 표(§7 — 실재 서술 전건 파일 시스템 직접 실측, L-07; bundle 원본·설치본·`docs/v0.8-demo-fixtures/` 미생성, 후속 시연 Task 생성 예정, 실재 불주장, done 7). 10 §3·framework/plugins/ 3문서 계약 재정의·확장 0(새 연산·새 reason·새 필드 0), Glossary 밖 새 용어 0. 동시 작성 형제 산출물(dispatch-protocol 개정·workflow-binding 개정·시연 절차서) 불인용(07 R2). 이 1파일만 생성(07 R4). | Worker (Advisor 위임, Task EX-P2) |
| 2026-07-06 | v0.8 Baseline | v0.8 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 29/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |
| 2026-07-06 | v0.9 Draft (개정 — §7 시연 후 상태 반영) | 비차단 관찰 1 해소 (docs/v0.8-verification-report.md §3.7 관찰 1 · 사용자 결정 DP-U3(a), 2026-07-06). §7 실측 대조 표의 시연 전 "미생성" 스냅샷 및 같은 상태를 서술하는 전 지점(§0·§2 물리 경계 트리·§2 표 "실재 여부" 열·§2 주·§7·§10 — `grep` 전수 열거, L-06)을 시연(PS-4 · EX-DP) 후 실측 실재로 전수 갱신. 착수 시 직접 재실측(L-07): bundle 원본 `docs/v0.8-demo-fixtures/report-exporter/` 3파일 실재 · 설치본 `framework/plugins/<plugin-id>/`(report-exporter/) 부재 = Remove 잔여물 0(Install→Activate→Deactivate→Remove 전 수명주기 완료 · 설치 이전 목록 전수 대조 성립, DP-E6 ⓒ). §2~§6 계약 서술·SP 표·DP-E6 결정 무변경(개정은 상태 서술·이력·상태 라인에 한정). memory-binding.md r2·loop-binding.md WF13 전수 갱신 선례 동형. 기존 이력 행 문면 불변(L-10). | Worker (Advisor 위임, Task T7) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 specs/10-plugins.md §3·§4(§4.1 바인딩 표·§4.2 이식 교체 지점)와 framework/plugins/ 3문서(module-manifest.md·plugin-manifest.md·plugin-lifecycle.md)다.** 이 문서는 그 계약의 **환경 실현 매핑**이며, 계약 요소(네 연산·데이터 포맷·불변 규칙·Manifest 필드·`reason` 열거·검사 규칙)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. framework/plugins/ 3문서가 "직렬화 형식·물리 위치·물리 경로·물리 진입점 해소·bundle 배치·배선·배포 채널·검사 물리 실행 방식은 Adapter Binding 문서 소관"이라며 미룬 지점이 실재하는(확정되는) 유일한 자리다(module-manifest.md §4, plugin-manifest.md §4, plugin-lifecycle.md §3.7·§6, 10 §4.1).
- **격리 지점의 방향 반전(C-3 비적용).** Module 구현 디렉터리 문서(framework/plugins/ 3문서) 본문은 특정 AI·언어·툴체인·직렬화 형식·물리 경로 토큰이 0건이어야 한다(structure.md §5 C-3 확장, 10 §3.3 INV-10). 이 문서는 그 **반대편**이다 — 구체 토큰(직렬화 형태 서술, 물리 경로 `framework/plugins/…`·`framework/adapters/claude/…`·`.claude/…`·`docs/v0.8-demo-fixtures/…`, 세션/턴, 서브에이전트 위임 등)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(runtime-binding.md §0·workflow-binding.md §0과 동형).
- **Plugin bundle 물리 위치·설치본 배치 정본 선언(Advisor 결정 DP-E6).** 레퍼런스 Plugin **bundle 원본**(self-contained 배포 단위)의 물리 위치는 **`docs/v0.8-demo-fixtures/` 격리 경계 내**(시연 픽스처 관례, 존치)이고, **Install 설치본**은 **`framework/plugins/<plugin-id>/` 하위 자기완결 배치**이며, **Remove** 후 framework/plugins/는 3문서만 잔존(잔여물 0의 물리 판정 = 설치 이전 파일 목록과의 전수 대조), **AI 의존 산출물**이 있는 Plugin이면 **`.claude/` 경계로 격리**한다(10 §4.1 INV-4). 상세·근거·충돌 판단은 §3(결정 기록)이 소유한다. **설치본 배치 위치(`framework/plugins/<plugin-id>/`)는 새 데이터 백엔드 디렉터리 신설이 아니라 01 §4.1 "Module 구현 디렉터리 = `framework/{…,plugins}/`" Frozen 문면과 10 §4.1 행 6("Core-side module 디렉터리(예: framework/plugins/)")의 직접 인스턴스**다 — workflow-binding.md §0의 DP-W4(정본 문면이 물리 형태를 지정하면 새 백엔드 신설 없이 그 인스턴스로 해소)와 **동형**이며, loop-binding.md §3의 DP-L4(정본이 경로를 열어 둬 새 백엔드 신설)와는 사실 관계가 다르다(§3.4).
- **배포 채널 형태 B 정직 구분(DP-E3 동형).** 배포 채널(10 §4.1 행 8 — 설치 메커니즘·marketplace 등)은 형태 B로 정직 구분한다 — 형태 A(Bootstrap)의 배포 = bundle 원본의 격리 경계 보유 + 수동 규약 Install(§3.3·§6). 라이브 하네스 설정 파일을 생성·수정하지 않는다.
- **창설 금지.** 이 문서는 10 §4.1 표를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. v0.8 산출물(본체 수정 없는 확장·추가만의 동작 확장)의 물리 실현 매핑으로 한정한다. 새 연산·새 필드·새 `reason`·새 불변 규칙·새 Config scope를 만들지 않는다(10 INV-7 재확인).
- **하네스 상태 전제(Bootstrap).** 이 하네스는 현재 **Bootstrap 상태**다(Glossary J-13, runtime-binding.md §0, delegation-protocol.md §0). Plugins는 정식 실행 Module이 아니라 규약 문서(10·framework/plugins/ 3문서)와 관행(Advisor 오케스트레이션, 서브에이전트 위임으로 역할 실행, 수동 규약 Install/Activate/Remove)으로 실현된다(형태 A). 따라서 본 문서의 매핑은 **이미 물리적으로 실재하는 표면**(자매 바인딩·framework/plugins/ 3문서·.claude/agents/ 4종·시연 픽스처 경계 관례 — §7 실측), **실행 코드 도입 시 로딩될 지점**(형태 B — 무인 자동 Install/Activate/Remove 실행 진입점·로더), **시연 Task(PS-4 · EX-DP)가 이 정본 구조대로 생성한 시연 소산**(bundle 원본 = `docs/v0.8-demo-fixtures/report-exporter/` 실재 · 설치본 = `framework/plugins/<plugin-id>/` Install→Remove 수명주기 완료로 부재 = Remove 잔여물 0 — 시연 후 §7 재실측, L-07)을 정직하게 구분한다. `형태 A`(문서·규약)·`형태 B`(실행 코드)는 structure.md §4의 서술 라벨이다.
- **실측 기반 상태 서술(L-07).** "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다(session-handoff-v0.3.md §1.4·§1.5, Active Lesson L-07). §2 "실재 여부" 열과 §7 실측 대조 표의 전 행은 파일 시스템 직접 실측에 근거한다 — 미존재를 실재로 쓰지 않고, 실재는 실측 후에만 기입한다. **bundle 원본(`docs/v0.8-demo-fixtures/report-exporter/`)은 시연 PS-4가 §3 정본 구조대로 생성해 실재하고, 설치본(`framework/plugins/<plugin-id>/`)은 Install→Remove 수명주기 완료로 부재(Remove 잔여물 0)**다(v0.9 T7 개정 시 직접 재실측, L-07).
- 용어는 specs/00-glossary.md 정본만 사용한다. Plugin·Plugin Manifest는 §3.2-J(J-10), Plugins(Component)는 §3.2-D 정본이며, `PluginsInterface`·`plugins-provider`는 module-manifest.md가 확정한 `contract`·`id` 필드 **값**이지 Glossary 표제어의 신설이 아니다. `형태 A/B`는 structure.md 서술 라벨의 인용이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 10 §4.1(Plugins Claude Code Binding)을 이 환경 위에 **v0.8 시점의 구체 물리 실현**으로 매핑한다.

책임은 여섯 가지다.

- 10 §4.1 바인딩 표의 **8행 전부**를 물리 표면(bundle·Manifest 직렬화·포함 Module 등록·Install·Deactivate/Remove·AI 비의존 구현·AI 의존 산출물·배포 채널)으로 확정하고, Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정/시연 소산(bundle 원본·설치본 — v0.9 T7 개정 시 시연 PS-4 후 실재·Remove 잔여물 0으로 갱신, §2·§7)을 "실재 여부" 열로 정직하게 구분한다(§2, done 1).
- Plugin bundle 물리 위치와 네 연산(Install/Activate/Deactivate/Remove)의 **물리 절차**를 예/아니오 판정 가능한 형태로 확정하고, Advisor 결정 DP-E6을 결정 기록으로 명문화하며, DP-E6이 01 §4.1 Frozen 문면과 충돌하지 않음을 근거와 함께 서술한다(§3, done 2·5). 특히 **Remove 잔여물 0 스캔 = 설치 이전 파일 목록과의 전수 대조** 절차를 명시한다.
- Plugins Provider Module의 `entrypoint`(네 연산 노출)의 **물리 해소 지점**(형태 A 규약 실현 / 형태 B 실행 코드)을 명시한다(§4, done 4).
- plugin-lifecycle.md의 검사(I1~I5·A1~A2·D1·R1~R2·IG)가 그대로 소비 가능한 **물리 판정 지점**을 확정한다 — 검사 규칙 자체는 § 포인터로 소비(재게재 0)하고, 각 검사의 물리 실행 방식만 확정한다(§5, done 3).
- 10 §4.2 이식 교체 지점 5건 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 표로 명시한다(§6, done 6). 유지 열이 10 §3 계약(Manifest 6필드·4연산 완료 조건·INV-1~10)을 커버함을 확인한다.
- 상태 서술을 실측과 대조한다(§7, done 7).

이 문서는 10 §3·framework/plugins/ 3문서의 어떤 계약 요소도 재정의·확장하지 않는다(§0·§8, done 5). 형태 A → 형태 B 전환 시에도 Core Contract(10 §3) 변경은 0이며(structure.md §7 C-1), 이 문서(§6의 "유지되는 것" 열)가 그 불변을 이식 축에서 재확인한다.

---

## §2. 10 §4.1 바인딩 표 8행 물리 실현 (done 1)

10 §4.1 Claude Code Binding 표의 **8행 전부**를 물리 표면으로 매핑한다. 아래 표의 "10 §4.1 바인딩(정본 인용)" 열은 정본 표현을 **원문 그대로** 인용하고, "물리 실현(claude 환경)" 열이 본 문서가 확정하는 경로·형태·채널·절차를, "실재 여부" 열이 Bootstrap 상태에서의 물리 실재/규약 실현(형태 A)/형태 B 예정/시연 소산(v0.9 T7 개정 시 시연 PS-4 후 실재·Remove 잔여물 0으로 갱신)을 정직하게 구분한다(§7 실측 대조). "실재" 서술은 전건 파일 시스템 실측 후 기입했다(L-07).

Adapter 경계 및 관련 물리 경계(본 문서 실측 2026-07-06):

```
framework/plugins/                       # Module 구현 디렉터리 (Core-side, C-3 확장 — AI·언어·툴체인 비의존)
├─ module-manifest.md                    # 실재 — Plugins Provider 등록 서술자 (EX-P1)
├─ plugin-manifest.md                    # 실재 — Plugin Manifest·Failure Report 포맷 (EX-P1)
├─ plugin-lifecycle.md                   # 실재 — 4연산 규칙 인스턴스 (EX-P1)
└─ <plugin-id>/                          # 부재 = Remove 잔여물 0 — Install 설치본 자리, 시연 PS-4 Install→Remove 후 제거됨 (DP-E6 ⓑ·ⓒ)

framework/adapters/claude/
├─ runtime-binding.md … workflow-binding.md   # 실재 — 자매 Adapter Binding
└─ plugins-binding.md                    # 실재 — 본 문서

docs/
├─ v0.5-demo-fixtures/ v0.6-… v0.7-…     # 실재 — 시연 픽스처 경계 관례
└─ v0.8-demo-fixtures/                   # 실재 — bundle 원본(report-exporter/) 배치, 시연 PS-4 생성 (DP-E6 ⓐ)
```

| # | §3 계약 요소 (정본 §) | 10 §4.1 바인딩 (정본 인용) | 물리 실현 (claude 환경) | 실재 여부 |
|---|---|---|---|---|
| 1 | Plugin bundle (10 §3.1 Install 입력) | Claude Code plugin 디렉터리 — self-contained 배포 단위. | Plugin **bundle 원본**(self-contained 배포 단위)은 `docs/v0.8-demo-fixtures/` 격리 경계 내에 자기완결 디렉터리로 존치한다(DP-E6 ⓐ — 시연 픽스처 관례). 하나의 경계 안에 Manifest·포함 Module 구현을 묶고 내부에서도 Core/Adapter 분리를 유지한다(10 §4.1 말미). 물리 위치 정본은 §3.1. | bundle 원본 실재 — `docs/v0.8-demo-fixtures/report-exporter/` 3파일(plugin-manifest.md·core/report-exporter-module.md·bundle-note.md, 시연 PS-4 생성·v0.9 T7 재실측). `docs/v0.8-demo-fixtures/` 경계 실재(v0.5~v0.8-demo-fixtures). |
| 2 | Plugin Manifest(§3.2-A) 직렬화 | Markdown + front-matter 또는 설정 파일. Module Manifest 직렬화(01 §4.1)와 동일 관례. | Plugin Manifest 직렬화 = **문서 형태**(Markdown 본문 + front-matter 또는 설정 파일), Module Manifest 직렬화(runtime-binding.md §3.1 — Markdown + front-matter)와 동일 관례. 6필드(`id`/`version`/`provides`/`requires`/`dependsOn`/`frameworkCompat`)의 포맷 정본은 plugin-manifest.md §2, 물리 직렬화만 본 문서 소관(재정의 0). | 직렬화 형식 관례 실재(자매 바인딩·`.claude/agents/*.md` front-matter가 형식 예시). Plugin Manifest 인스턴스(bundle 내 `report-exporter/plugin-manifest.md`)는 시연 PS-4가 생성해 실재(v0.9 T7 재실측). |
| 3 | 포함 Module 등록 (Activate) | 01 §4.1의 Register 바인딩 경유 — `.claude/agents/`, `.claude/commands/`, `.claude/hooks/`, `.claude/skills/` 확장 표면에 등록. | Activate = `provides`의 각 Module Manifest를 **Runtime Register**(01 §3.1-A, runtime-binding.md §3.2 — 정의 파일 배치·`id` 유일성)로 등록하고 `requires` contract를 Resolve(10 INV-2). AI 비의존 Module 구현은 Core-side `framework/plugins/<plugin-id>/`에(행 6), Agent/확장 표면 등록은 `.claude/{agents,commands,hooks,skills}`에 바인딩. 번들된 확장 요소(Hook/Skill)의 등록 표면은 **08 §3.1-C·09 §3.1-A 소관**이며(10 §9 조율 결정 보존, 10 §4.2 SP-5) 본 문서는 Module 부분만 확정한다. 물리 절차는 §3.2·§4. | Register 규약 실현(형태 A) — `.claude/agents/` 4종·runtime-binding.md 실재(§7). 무인 자동 등록 실행 코드(형태 B) 미도입. 활성 등록은 시연 PS-4 Activate(A1·A2)로 규약 실현 실증 후 Deactivate·Remove 완료(형태 A). |
| 4 | Install | Plugin 디렉터리 배치 (본체 파일 미수정). | Install = bundle 원본(`docs/v0.8-demo-fixtures/`)을 **설치본 디렉터리 `framework/plugins/<plugin-id>/`로 배치**한다(DP-E6 ⓑ). 본체(기존 3문서·`framework/core/`·`framework/runtime/`·기존 spec·이미 등록된 Module) 파일은 수정하지 않는다(INV-1) — 새 하위 디렉터리 추가만. 상태는 registered-but-inactive(10 §3.1). 물리 절차·검사는 §3.2·§5. | 규약 실현(형태 A). 설치본 부재 = Remove 잔여물 0 — 시연 PS-4 Install→Remove 후 `framework/plugins/` 하위 디렉터리 부재(v0.9 T7 재실측), 3문서만 실재. |
| 5 | Deactivate / Remove | 등록 배선 해제와 Plugin 디렉터리 제거. | Deactivate = `provides`의 각 Module을 활성화 역순으로 **01 §3.1-A Deregister**(runtime-binding.md §3.2 — 정의 파일 제거·바인딩 해제)로 비활성화. Remove = 설치본 디렉터리(`framework/plugins/<plugin-id>/`)·등록 배선·(AI 의존 시) `.claude/` 산출물을 제거하고, **잔여물 0 = 설치 이전 파일 목록과의 전수 대조**로 판정한다(DP-E6 ⓒ, §3.2·§3.3). 제거 후 `framework/plugins/`는 3문서만 잔존. | 규약 실현(형태 A). 시연 PS-4에서 Deactivate·Remove 규약 실현 실증(설치본 제거·잔여물 0). |
| 6 | 포함 Module의 AI 비의존 구현 | Core-side module 디렉터리(예: `framework/plugins/`, 01 §4.1)에 위치. AI 의존 요소 0건 유지. | 설치본의 **AI 비의존 Module 구현**은 Core-side module 디렉터리 `framework/plugins/<plugin-id>/`에 위치한다(DP-E6 ⓑ — 10 §4.1 이 행과 01 §4.1 "Module 구현 디렉터리=framework/{…,plugins}/" Frozen 문면의 직접 인스턴스, 새 백엔드 신설 아님; §3.4). AI 의존 요소 0건 유지(INV-4). Plugins 서브시스템 자기 문서 3건과의 경계는 하위 디렉터리 격리로 **비중첩**(DP-E6 ⓑ). | `framework/plugins/` 경계·3문서 실재(실측). 설치본 하위 디렉터리 부재 = Remove 잔여물 0(시연 PS-4 Install→Remove 후·v0.9 T7 재실측). |
| 7 | AI 의존 산출물 | `.claude/` 등 Adapter 경계로 격리 (INV-4). | AI 의존 산출물이 있는 Plugin이면 그 산출물은 `.claude/` 등 Adapter 경계로 격리한다(DP-E6 ⓓ, INV-4). 단 v0.8 레퍼런스 Plugin은 **AI 비의존 문서형 Module 1개 번들(DP-E2)**이라 이 경로는 **구조만 확정**(미사용). bundle 내부의 Core/Adapter 분리 원칙(10 §4.1 말미)의 물리 실현이다. | `.claude/` 경계 실재(격리 경계). 이 레퍼런스 Plugin의 AI 의존 산출물은 없음 — 경로 구조만 확정(미사용, DP-E6 ⓓ). |
| 8 | 배포 채널 | Claude Code plugin 설치 메커니즘(marketplace 등). | 배포 채널은 형태 A(Bootstrap)에서 **bundle 원본의 격리 경계(`docs/v0.8-demo-fixtures/`) 보유 + 수동 규약 Install**로 실현한다(DP-E3 동형). marketplace 등 자동 설치 메커니즘은 형태 B로, 라이브 하네스 설정 파일 생성·수정 없이 이연한다. 이식 교체 지점 SP-4(§6). | 형태 A 수동 규약 실현. 자동 배포 채널(marketplace 등, 형태 B) 미도입. |

주:

- 위 8행은 10 §4.1 표의 전 행이다. 각 행의 "물리 실현"은 10 §4.1 정본 표현을 이 환경의 구체 경로·형태·채널로 좁힌 것이며, 새 바인딩 계약을 창설하지 않는다(§0).
- **물리 실재 / 형태 A / 형태 B / 시연 소산 구분(정직).** 행 6의 `framework/plugins/` 경계·3문서, 행 3의 `.claude/agents/`·runtime-binding.md, 행 7의 `.claude/` 경계, 행 1의 시연 픽스처 경계 관례(v0.5~v0.8-demo-fixtures)는 물리 실재다. 행 3~5의 등록·배선·제거 오케스트레이션은 Bootstrap에서 **규약 실현(형태 A)**이며, 무인 자동 Install/Activate/Remove 채널은 형태 B다. **행 1의 bundle 원본은 시연 PS-4가 §3 정본 구조대로 생성해 실재하고, 행 4·행 6의 설치본은 Install→Remove 수명주기 완료로 부재 = Remove 잔여물 0**이다(v0.9 T7 개정 시 재실측 — L-07).
- **역할 실행 = Agent Module(서브에이전트 채널).** Install/Activate/Deactivate/Remove의 실행이 Agent 역할(Advisor·Worker·Verifier) 흐름에 얹히더라도, 그 역할 디스패치는 위임·보고 메시지(02) 흐름이지 module Resolve가 아니다(module-manifest.md §3 — 역할 실행은 `requires`에 넣지 않음). 물리 채널은 서브에이전트 위임/최종 응답(delegation-protocol.md §3)이다.

---

## §3. Plugin bundle 물리 위치·4연산 물리 절차 + DP-E6 결정 기록 (done 2·5)

10 §3.1이 정의한 네 연산과 plugin-lifecycle.md가 규칙으로 전개한 완료 조건을, 이 환경의 **예/아니오 판정 가능한 물리 절차**로 확정한다. **이 문서는 Adapter 경계이므로 구체 물리 경로 토큰의 사용이 허용된다(§0 격리 지점).** 연산의 입력·출력·완료 조건·실패 reason·검사 규칙의 정본은 10 §3.1·§3.2와 plugin-lifecycle.md(§2·§3)이며, 본 절은 그 물리 실현만 확정한다(재정의 0).

### §3.1 Plugin bundle·설치본·격리 물리 위치 (DP-E6 ⓐ·ⓑ·ⓓ)

- **bundle 원본(DP-E6 ⓐ).** 레퍼런스 Plugin의 self-contained 배포 단위(10 §4.1 행 1)는 `docs/v0.8-demo-fixtures/` 격리 경계 내에 자기완결 디렉터리로 존치한다. 이는 v0.5~v0.7 시연 픽스처가 `docs/vX.Y-demo-fixtures/`에 배치된 관례와 동형이다(실측: 세 픽스처 경계 실재). bundle 내부에서도 Core/Adapter 경계를 유지해 AI 비의존 Module 구현과 (있다면) AI 의존 바인딩을 물리적으로 분리해 담는다(10 §4.1 말미).
- **설치본(DP-E6 ⓑ).** Install은 bundle 원본을 `framework/plugins/<plugin-id>/` 하위 자기완결 디렉터리로 배치한다. `<plugin-id>`는 Plugin Manifest `id`(안정 식별자, 10 INV-9·plugin-manifest.md §2)이며, 이 디렉터리명이 곧 설치본의 유일성 기준이다(§3.2 I4). 설치본의 AI 비의존 Module 구현은 이 Core-side 디렉터리에(행 6), (있다면) AI 의존 산출물은 `.claude/`에(ⓓ) 격리한다.
- **비중첩(DP-E6 ⓑ).** 설치본 배치 시에도 Plugins 서브시스템 자기 문서 3건(`framework/plugins/{module-manifest,plugin-manifest,plugin-lifecycle}.md` — 최상위 배치)과 설치본(`framework/plugins/<plugin-id>/` — 하위 디렉터리)의 경계는 **하위 디렉터리 격리로 비중첩**이다. 파일 충돌이 없으므로 설치는 3문서를 수정하지 않는다(INV-1 정합, §3.2 I1).
- **AI 의존 격리(DP-E6 ⓓ).** AI 의존 산출물이 있는 Plugin이면 그 산출물은 `.claude/` 경계로 격리한다(10 §4.1 행 7, INV-4). v0.8 레퍼런스 Plugin은 AI 비의존 문서형 Module 1개 번들(DP-E2)이므로 이 경로는 **구조만 확정**하고 실사용하지 않는다.

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
4. **전 부류 전수(정직).** 추가 산출물의 **전 부류**(등록 Module·배치 파일·배선)를 스캔한다 — 한 부류(예: 등록 Module)만 제거 확인하고 다른 부류(배치 파일·배선)를 통과로 간주하지 않는다(좁은 대리 지표 금지, plugin-lifecycle.md §3.5 검사 범위 정직). 차집합이 0이 아니면 R1 = 아니오, reason=ResidueDetected, `location` = 잔여물 지점.
5. **검증 정합.** 이 절차는 10 §7 검증 방법("Verifier가 Remove 후 잔여물 스캔 = 0을 확인")의 물리 실현이며, 파일 시스템 목록 대조로 예/아니오가 결정된다.

### §3.4 DP-E6 결정 기록 — 설치본 배치가 01 §4.1 Frozen 문면과 충돌하지 않음 (done 5)

- **결정(DP-E6, Advisor 확정 입력 — 임의 변경 금지).** bundle 원본 = `docs/v0.8-demo-fixtures/`(ⓐ), 설치본 = `framework/plugins/<plugin-id>/`(ⓑ), Remove 잔여물 0 = 설치 이전 파일 목록 전수 대조(ⓒ), AI 의존 산출물 = `.claude/` 격리(ⓓ — v0.8 레퍼런스 Plugin은 AI 비의존이라 구조만 확정).
- **01 §4.1 Frozen 문면과의 정합(충돌 0).** 01 §4.1은 "Module 구현 디렉터리 | `framework/{loop,memory,verifier,workflow,plugins}/`"라고 Frozen 상태로 지정한다. 10 §4.1 행 6은 "포함 Module의 AI 비의존 구현 | Core-side module 디렉터리(예: `framework/plugins/`, 01 §4.1)에 위치"라고 지정한다. **설치본을 `framework/plugins/<plugin-id>/`에 두는 것은 이 두 정본 문면의 직접 인스턴스**다 —
  - (a) `framework/plugins/`는 이미 01 §4.1이 지정한 Module 구현 디렉터리이므로, 그 하위에 개별 Plugin의 Module 구현을 자기완결 배치하는 것은 **정본 문면 내 인스턴스**이지 새 데이터 백엔드 디렉터리의 창설이 아니다(§0 창설 금지 준수).
  - (b) structure.md §3 규칙 2(각 Module은 자기완결 단위)와 정합한다 — 설치된 Plugin의 Module 구현이 자기 하위 디렉터리 하나에 모인다.
  - (c) INV-1(본체 불가침)과 정합한다 — 새 하위 디렉터리 추가는 기존 3문서·Core 경계 파일을 수정하지 않는 **추가만의 확장**이다(§3.2 I1·비중첩 ⓑ).
  - (d) INV-4(Core AI 비의존)·C-3 확장과 정합한다 — `framework/plugins/<plugin-id>/`의 Module 구현은 AI 비의존이고, AI 의존 산출물은 `.claude/`로 격리한다(ⓓ).
- **DP-W4·DP-L4와의 사실 관계 대비.** 이 해소는 workflow-binding.md §0·§3의 DP-W4와 **동형**이다 — 정본 문면(07 §4.1 행 1이 "계획·로드맵 문서")이 이미 물리 형태를 지정했으므로 새 백엔드 디렉터리 신설 없이 그 인스턴스로 해소한 것처럼, 여기서도 01 §4.1·10 §4.1 정본 문면이 이미 `framework/plugins/`를 Module 구현 디렉터리로 지정했으므로 새 백엔드 없이 그 하위 인스턴스로 해소한다. 이는 loop-binding.md §3의 DP-L4(정본이 경로·문법을 바인딩에 열어 둬 `loop-data/` 신설 백엔드로 격리)와는 사실 관계가 **다르다** — 10·01 §4.1은 물리 디렉터리를 이미 지정하므로 신설이 불필요하다.
- **충돌 판단 시 처리.** 만약 설치본 배치가 어떤 Frozen 문면(01·10 §4.1, INV-1~10)과 충돌한다면 구현하지 않고 Advisor에게 실패 보고한다(structure.md §7 C-1·plugin-lifecycle.md §0 원칙). 본 검토 결과 **충돌은 발견되지 않았다** — DP-E6 ⓐ~ⓓ는 정본 문면의 인스턴스이며 계약 재정의가 없다.

---

## §4. Plugins Provider `entrypoint` 물리 해소 (done 4)

module-manifest.md(EX-P1 확정본)가 "`entrypoint`의 물리 해소는 Adapter Binding 문서 소관(§4)"으로 미룬 지점을 확정한다. loop-binding.md §4.1(v0.6 Baseline)·workflow-binding.md §4.1의 `entrypoint` 물리 해소 표 관례(추상 참조 → 물리 실현, 형태 A/B 구분)와 동형으로 서술한다(done 4). module-manifest.md §2·§4 `entrypoint` = "추상 참조 — 설치(Install)·활성화(Activate)·비활성화(Deactivate)·제거(Remove) 연산(10 §3.1) 노출 진입점. 물리 해소는 Adapter Binding 문서 소관".

| 추상 참조 (module-manifest.md §4) | 물리 해소 (claude 환경) | 형태 |
|---|---|---|
| Install(10 §3.1) 노출 — self-contained bundle 1건 설치, registered-but-inactive | **형태 A(Bootstrap):** bundle 원본(`docs/v0.8-demo-fixtures/`)을 설치본(`framework/plugins/<plugin-id>/`)으로 배치(DP-E6 ⓑ), 본체 무수정(INV-1). I1~I5·IG 검사(§5, plugin-lifecycle.md §3.2·§3.6)를 대조한다. 별도 실행 진입점 파일은 없다 — 수동 규약 배치. | 규약 실현(형태 A) |
| Activate(10 §3.1) 노출 — 포함 Module Register/Resolve 활성화 | **형태 A(Bootstrap):** `provides`의 각 Module Manifest를 Runtime Register(01 §3.1-A, runtime-binding.md §3.2)로 등록하고 `requires`를 Resolve(10 INV-2). A1~A2 검사(§5, plugin-lifecycle.md §3.3)를 대조한다. 확장 요소 등록 표면은 08 §3.1-C·09 §3.1-A 소관(10 §9 결정 기록). | 규약 실현(형태 A) |
| Deactivate(10 §3.1) 노출 — 활성화 역순 비활성화·바인딩 해제 | **형태 A(Bootstrap):** `provides`의 각 Module을 활성화 역순으로 01 §3.1-A Deregister(runtime-binding.md §3.2). D1 검사(§5, plugin-lifecycle.md §3.4)를 대조한다. | 규약 실현(형태 A) |
| Remove(10 §3.1) 노출 — 잔여물 0으로 제거 | **형태 A(Bootstrap):** 설치본 디렉터리·등록 배선을 제거(01 Deregister)하고, 설치 이전 파일 목록 전수 대조로 잔여물 0을 판정한다(§3.3). R2→R1 검사(§5, plugin-lifecycle.md §3.5). | 규약 실현(형태 A) |
| 위 4연산의 실행 코드 로케이터 | **형태 B:** 설치·활성화·비활성화·제거를 사람 없이 자동으로 트리거·수합하는 실행 코드가 non-core 실행 경계(`framework/plugins/` Module 구현 디렉터리 또는 `framework/adapters/claude/`)에 배치되어 연산을 실현한다. 경계 간 정확한 분할은 형태 B 설계 시 확정한다(structure.md §4 규칙 4 defer — 선취·추측 금지, loop-binding.md §4.1 형태 B 관례 동형). | 형태 B |

- **Register/Resolve 정합.** Plugins Provider Module 자체의 등록(Register)은 Manifest(framework/plugins/module-manifest.md) + 본 바인딩 배치로 규약 실현되며(형태 A), 해소(Resolve)는 소비자가 `contract` `PluginsInterface`로 배포·수명주기 오케스트레이션을 요청할 때 이 Provider로 해소되는 것이다. 이 Provider가 **처리 대상 개별 Plugin**의 provides를 Register하고 requires를 Resolve하는 것(Activate)은 그 연산의 완료 조건이지 Provider 자신의 Resolve 게이트가 아니다(module-manifest.md §3 requires 미선언). 이 등록 경로는 이식 교체 지점 SP-2에 대응한다(§6).
- **`requires`·`configSchema` 미선언 재확인.** module-manifest.md §3·§5(DP-E5)가 Memory 미소비·Runtime 연산 소비는 contract 의존 아님 등을 근거로 `requires`를 비우고 `configSchema`를 생략한 결정은 불변이다. 본 문서는 그 결정을 재정의하지 않으며, Provider가 소비하는 Runtime 연산(Register/Resolve/Deregister)의 물리 배선만 runtime-binding.md §3.2 참조로 확인한다(재정의 0).

---

## §5. plugin-lifecycle.md 검사 물리 실행 지점 (done 3)

plugin-lifecycle.md §3의 검사(I1~I5·A1~A2·D1·R1~R2·IG)를 이 환경의 **물리 판정 지점**으로 확정한다. **검사 규칙 자체(판정 형태·대응 연산·완료 조건·reason 결합)는 plugin-lifecycle.md §3이 소유하며 본 표는 재게재하지 않는다(§ 포인터 소비)** — 본 표는 각 검사의 **물리 실행 방식**(무엇을 어떤 물리 대상에 대해 예/아니오로 대조하는가)만 확정한다. reason 열거의 포맷은 plugin-manifest.md §3, 판정 규칙은 10 §3.1이 유지한다(재정의 0).

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

- **소비 가능한 물리 판정 지점.** 위 표는 plugin-lifecycle.md §3의 각 검사가 이 환경에서 **어떤 물리 대상에 대해 예/아니오로 실행되는가**를 확정한다. 검사의 판정 형태·완료 조건 대응·reason 결합은 그 문서 §3이 소유하고, 본 문서는 그것을 **그대로 소비**한다 — 검사 규칙을 재게재·재정의하지 않았다(재게재 0).
- **10 §7 검증 방법과의 정합.** I1(본체 diff=0)·A1/A2(Register/Resolve 호출·반환 핸들)·R1(잔여물 스캔=0)·IG(Memory 단일 Port·Core AI 비의존)는 10 §7 "검증 방법"의 각 항목과 1:1 정합한다. 판정 주체·시점·전이는 06·03-loop 소관이며(plugin-lifecycle.md §3.7 경계), 본 문서는 물리 실행 대상만 확정한다.
- **형태 B 전환.** 실행 코드 도입 시 위 검사는 실행 검증기로 실현되며, 판정 규칙(plugin-lifecycle.md §3)·reason 열거(plugin-manifest.md §3)의 변경은 0이다(structure.md §7 C-1).

---

## §6. 10 §4.2 이식 교체 지점 5건 대응 (done 6)

10 §4.2 이식 교체 지점 5건 각각에 본 문서의 대응 절과 "교체되는 것 / 유지되는 것"을 명시한다. "유지되는 것" 열이 이식 축에서 Core Contract 불변(structure.md §7 C-1)을 재확인하며, 10 §3 계약(Plugin Manifest 6필드·4연산 완료 조건·INV-1~10)을 커버한다.

| # (10 §4.2) | 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (정본 § 불변) |
|---|---|---|---|---|
| SP-1 | Plugin bundle/Manifest 직렬화 → 대상 환경의 패키지·서술자 포맷 | §2 행 1·2, §3.1 | bundle 원본 = `docs/v0.8-demo-fixtures/` 디렉터리, 설치본 = `framework/plugins/<plugin-id>/` 배치, Plugin Manifest 직렬화 = 문서 형태(Markdown + front-matter/설정 파일). | **Plugin Manifest 6필드**(`id`/`version`/`provides`/`requires`/`dependsOn`/`frameworkCompat`, 10 §3.2-A·plugin-manifest.md §2); **공통 Failure Report 4필드·`reason` 11종**(10 §3.2-B·plugin-manifest.md §3); **INV-8(자기완결성)·INV-9(안정 식별자)**. |
| SP-2 | 포함 Module 등록 표면 `.claude/{agents,commands,hooks,skills}` → 대상 환경의 Module 로더·확장 등록 메커니즘 | §2 행 3, §4·§5 | `.claude/{agents,commands,hooks,skills}` 확장 표면 + Core-side `framework/plugins/<plugin-id>/` 배치, Register/Resolve 규약 실현(runtime-binding.md §3.2). | **Activate 완료 조건·INV-2(Register/Resolve 경유)**(10 §3.1·§3.3); **A1·A2 검사**(plugin-lifecycle.md §3.3); **INV-4/5/6(격리 불변)**(IG 검사). |
| SP-3 | Install/Activate/Deactivate/Remove의 물리 실현 → 대상 환경의 패키지 매니저 | §3, §4 | 디렉터리 배치·배선·제거(설치본 배치·01 Deregister·설치 이전 목록 전수 대조 제거)·형태 A 규약 실현·형태 B 실행 코드 로케이터. | **4연산 입력·출력·완료 조건·실패 reason**(10 §3.1·plugin-lifecycle.md §2); **INV-1(본체 불가침)·INV-3(잔여물 0)**; **I1~I5·D1·R1~R2 검사**. |
| SP-4 | 배포 채널 Claude Code plugin 설치 메커니즘(marketplace 등) → 대상 환경의 배포·레지스트리 채널 | §2 행 8, §3.3(DP-E3 동형) | 형태 A(Bootstrap): bundle 원본의 격리 경계(`docs/v0.8-demo-fixtures/`) 보유 + 수동 규약 Install; marketplace 등 자동 채널은 형태 B(미도입). | **INV-1(본체 불가침)·INV-8(자기완결성)**; 배포는 계약(10 §3.1)의 물리 채널일 뿐 계약 요소를 바꾸지 않는다. |
| SP-5 | 확장 요소(Hook/Skill) 표면 바인딩 — 08/09의 §4 소관. Plugins는 참조만 | §2 행 3, §4·§5 | 08/09 §4 소관(참조만) — Plugins는 번들·제거만 소유하고 확장 요소의 등록 표면을 정의하지 않는다. | **08 §3.1-C·09 §3.1-A 등록 계약** + 10이 소유하는 **배포·제거 계약**(10 §9 결정 기록); Plugins의 `provides` 포함 요소 참조 수준(10 §3.2-A). |

- **유지 열이 10 §3 계약을 전건 커버.** 위 유지 열은 10 §3 계약을 다음과 같이 커버한다 — (i) **Plugin Manifest 6필드** = SP-1; (ii) **4연산 완료 조건·실패 reason** = SP-2(Activate)·SP-3(Install/Deactivate/Remove); (iii) **공통 Failure Report·`reason` 11종** = SP-1; (iv) **INV-1~10**: INV-1(본체 불가침)=SP-3·SP-4, INV-2(Register/Resolve 경유)=SP-2, INV-3(잔여물 0)=SP-3, INV-4/5/6(격리 불변)=SP-2, INV-7(Config scope 불변)=아래 주, INV-8(자기완결성)=SP-1·SP-4, INV-9(안정 식별자)=SP-1, INV-10(AI 비의존 계약)=아래 주. 이들은 다른 AI·환경으로 이식해도 바뀌지 않는다(structure.md §7 C-1). framework/plugins/ 3문서가 그 계약의 인스턴스이며, 이식 시에도 계약 요소는 불변이다.
- **INV-7·INV-10 이식 불변(주).** INV-7(Plugin은 새 Config scope 미도입, Config는 Global/Project/Module 유지)은 본 문서가 새 Config scope를 도입하지 않음으로 준수하며(§0 창설 금지, OQ-P1 승인) 이식 시에도 불변이다. INV-10(§3 계약 AI 비의존)은 본 문서가 AI·환경 의존 토큰을 이 Adapter 경계에만 격리하고 framework/plugins/ 3문서는 § 포인터로만 인용해 유지되며, 이식 시 이 경계의 물리 토큰만 교체된다.
- **정식화 이연.** 이 교체 지점 목록은 specs/11-adapters.md가 Adapter Interface로 정식화한다(10 §4.2 말미·runtime-binding.md §4·verifier-binding.md §6 동형). 본 문서는 그 정식화를 선취하지 않고 v0.8 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §7. 상태 서술 실측 대조 (done 7 — L-07 재발 방지)

session-handoff-v0.3.md §1.4·§1.5(상태 서술은 실측 후 기록, Active Lesson L-07)에 따라, 본 문서의 "실재/존재" 서술 전건을 파일 시스템과 직접 대조한 결과다. **대조 시점·방법: 2026-07-06 파일 열거(`ls`/`find`) + 전역 문자열 검색(`grep`) 직접 실측. v0.9 T7 개정(관찰 1 해소)은 bundle 원본·설치본 행을 시연(PS-4) 후 상태로 직접 재실측·갱신했다(L-07) — bundle 원본 `docs/v0.8-demo-fixtures/report-exporter/` 실재 · 설치본 `framework/plugins/<plugin-id>/` 부재 = Remove 잔여물 0. 그 외 행은 EX-P2 실측값을 유지한다.**

| 대상 | 본 문서 서술 | 실측 결과 (2026-07-06, 직접 실측) |
|---|---|---|
| `framework/plugins/` 3문서 (EX-P1 확정본 — § 포인터 대상) | 실재 (module-manifest·plugin-manifest·plugin-lifecycle.md) | 실재 — 3파일: module-manifest.md(34,742)·plugin-manifest.md(23,609)·plugin-lifecycle.md(44,726). 무수정. |
| `framework/plugins/<plugin-id>/` (설치본 — DP-E6 ⓑ·ⓒ) | **부재 = Remove 잔여물 0** (시연 PS-4 Install→Remove 수명주기 완료로 설치본 제거) | **부재 = 잔여물 0** — `find framework/plugins -maxdepth 1 -type d`에 하위 디렉터리 없음(3문서만 최상위 실재, v0.9 T7 재실측). 설치 이전 목록 전수 대조 성립(DP-E6 ⓒ). |
| `docs/v0.8-demo-fixtures/` (bundle 원본 — DP-E6 ⓐ) | **실재** (bundle 원본 자리, 시연 PS-4 생성) | **실재** — `docs/v0.8-demo-fixtures/` 실재(v0.5~v0.8-demo-fixtures). bundle 원본 `report-exporter/` 3파일(plugin-manifest.md·core/report-exporter-module.md·bundle-note.md, v0.9 T7 재실측). |
| `framework/adapters/claude/` 경계 | 실재 (Adapter 경계) | 실재 — runtime/memory/verifier/loop/workflow-binding.md·memory-data/·loop-data/ 등 존재 확인. |
| `framework/adapters/claude/plugins-binding.md` (본 문서) | 실재 (본 산출로 생성) | 실재 (이 파일). 생성 전 미존재였음(실측: `NOT EXISTS`). |
| `framework/adapters/claude/runtime-binding.md` (Register/Resolve/Deregister 참조원 — §4·§5) | 실재 (v0.3 Baseline, 자매) | 실재 (32,973 bytes) — §3.2 Registry 4연산 수행 방식 참조. |
| `framework/adapters/claude/memory-binding.md` (IG INV-5 Memory 백엔드 참조 — §5) | 실재 (v0.4 Baseline, 자매) | 실재 (51,144 bytes) — memory-data/ 백엔드 경유 단일 Port. |
| `.claude/agents/` 4종 (Register 표면·역할 실행 — §2 행 3·§4) | 실재 (advisor/planner/verifier/worker.md) | 실재 — 4파일(advisor·planner·verifier·worker.md). |
| `.claude/` 확장 표면·AI 의존 격리 경계 (§2 행 3·행 7) | 실재 (`.claude/{agents,commands,hooks,skills}`·`.claude/` 격리 경계) | 실재 — `.claude/agents/` 확인. v0.8 레퍼런스 Plugin의 AI 의존 산출물은 없음(DP-E2 — 구조만 확정). |
| `PluginsInterface`·`plugins-provider` 사전 명명 (§4 근거) | 저장소 사전 명명은 framework/plugins/ 확정본에만 (신조어 아님) | 실측 — `grep -rl`: `framework/plugins/module-manifest.md`·`plugin-lifecycle.md`에만 존재(사전 바인딩 0, DP-E5 확정 값). |
| 무인 자동 Install/Activate/Remove 실행 진입점·로더 (형태 B) | 미도입 (형태 B 예정) | 미도입 — Bootstrap 상태(형태 A). `framework/plugins/`는 계약 문서 3건만 실재(실행 코드 0). |

- **핵심 구분.** 본 문서가 확정한 bundle 원본·설치본의 **물리 위치·4연산 절차·검사 물리 실행 지점은 정본(결정 기록·근거)**(§3~§5)이며, 그 **시연 실물은 시연 PS-4(EX-DP)가 이 정본 구조대로 생성**했다 — bundle 원본 `docs/v0.8-demo-fixtures/report-exporter/` 실재, 설치본 `framework/plugins/<plugin-id>/`은 Install→Remove 수명주기 완료로 부재(Remove 잔여물 0). 이는 memory-binding.md가 M5 draft 시점 "데이터 미생성"을 M7 시연 후 실재로 전환한 관례(memory-binding.md §7 r2)와 동형이다. 시연 실물의 생성 주체는 **시연 Task**이며, 본 문서(EX-P2)는 물리 위치·절차·판정 지점의 정본만 소유한다 — 시연 실물을 생성·수정하지 않았고, v0.9 T7 개정은 그 시연 후 상태를 재실측·반영만 한다.
- **`framework/plugins/<plugin-id>/` 부재는 오류가 아니라 상태 정합(Remove 잔여물 0).** 설치본 디렉터리가 없는 것은 정합이다 — 시연 PS-4가 레퍼런스 Plugin의 Install→Activate→Deactivate→Remove 전 수명주기를 규약 실현(형태 A)으로 실증했고, Remove로 설치본을 제거해 `framework/plugins/`가 3문서만 잔존(잔여물 0 = 설치 이전 목록 전수 대조 성립, DP-E6 ⓒ)하기 때문이다. DP-E6 ⓑ가 확정한 것은 그 배치 **위치·규약**이며, 현 부재는 그 규약대로의 수명주기 완결 결과다.
- 실재를 주장하는 모든 행은 파일 시스템 직접 실측 후에만 기입했다(v0.9 T7 개정은 bundle 원본·설치본 행을 시연 후 상태로 직접 재실측·갱신). 실측과 불일치하는 서술은 0건이다 — 미존재를 실재로, 실재를 미존재로 쓰지 않았다(L-07 재발 방지).

---

## §8. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0 (done 5).** 본 문서의 모든 매핑은 10 §3·§4·framework/plugins/ 3문서의 물리 실현이다. 어떤 연산·데이터 계약·불변 규칙·Manifest 필드·`reason` 열거·검사 규칙도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 정본 §(10 §3·§4·module-manifest.md·plugin-manifest.md·plugin-lifecycle.md)다. 10 §4.1 표를 넘어 새 바인딩 계약을 창설하지 않았고, 새 연산·새 필드·새 `reason`·새 불변 규칙·새 Config scope(INV-7)를 추가하지 않았다.
- **계약 소유 명시.** Plugin Manifest 6필드·공통 Failure Report 포맷 = plugin-manifest.md/10 §3.2-A·B; 네 연산 규칙·검사 I1~I5·A1~A2·D1·R1~R2·IG = plugin-lifecycle.md/10 §3.1; Plugins Provider 등록 서술자·`entrypoint`·`contract`=`PluginsInterface`·`id`=`plugins-provider` = module-manifest.md/01 §3.2-A; Register/Resolve/Deregister 수행 방식 = runtime-binding.md/01 §3.1-A; Memory 백엔드(IG INV-5) = memory-binding.md/04 §4; 번들 Hook/Skill 등록 표면 = 08 §3.1-C·09 §3.1-A/§4. 본 문서는 이들의 **물리 실현**(bundle·설치본 물리 위치·4연산 물리 절차·`entrypoint` 물리 해소·검사 물리 실행 지점·이식 교체 지점)만 확정한다.
- **DP-E6이 01 §4.1 Frozen 문면 인스턴스임(충돌 0, done 5).** 설치본 `framework/plugins/<plugin-id>/` 배치는 01 §4.1 "Module 구현 디렉터리=framework/{…,plugins}/"와 10 §4.1 행 6("Core-side module 디렉터리 예: framework/plugins/")의 직접 인스턴스이며, 새 백엔드 신설·계약 재정의가 아니다(§3.4). 충돌 검토 결과 01·10 Frozen 문면·INV-1~10과의 충돌 0건 — 충돌 발견 시 구현하지 않고 Advisor 실패 보고할 것이었으나 발견되지 않았다.
- **격리 토큰의 단일 자리.** 구체 물리 경로(`framework/plugins/…`·`framework/adapters/claude/…`·`.claude/…`·`docs/v0.8-demo-fixtures/…`)·직렬화 형태 서술·세션/턴·서브에이전트 위임 등 환경 토큰은 이 Adapter 경계 문서에만 둔다. framework/plugins/ 3문서(Module 구현 디렉터리 문서 본문)는 이 토큰을 "Adapter Binding 문서 소관" 포인터로만 미뤘고, 본 문서가 그 소관자다(structure.md §5 C-3 확장은 이 경계에 비적용 — 격리 보유, runtime-binding.md §5 동형).
- **동시 작성 형제 불인용(07 R2).** 같은 병렬 집합(v0.8 Wave 2 PS-2)에서 동시 개정 중인 형제 산출물 — dispatch-protocol 개정(EX-R1)·workflow-binding 개정(EX-R2)·시연 절차서 — 의 미완성 내용은 인용·추측하지 않았다. 특히 workflow-binding.md의 §7 실측 표·시연 소산 서술은 인용하지 않았고, 관례 참조는 그 §0·§3 구조 관례(DP-W4 문서 형태 선례·격리 지점 방향 반전)에 한정했다. 확정된 정본(10·01 spec·Glossary·structure.md)과 확정 인터페이스(framework/plugins/ 3문서)·기존 Baseline(runtime/memory-binding.md·delegation-protocol.md·ROADMAP.md)만 참조했다.
- **추측 0 / 소유 경계 준수(07 R4·INV-2).** 불확실한 지점은 아래 open_questions로 에스컬레이션했다(추측 금지, 02 O4). 본 산출은 이 1개 파일(`framework/adapters/claude/plugins-binding.md`)만 생성하며, framework/plugins/ 3문서·자매 바인딩·`docs/`·`.claude/`·bundle 실물·픽스처를 수정·생성하지 않는다(R4, 시연 Task 소관 — 실재 불주장, L-07).

### open_questions (Advisor 에스컬레이션 — 비차단)

- **OQ-PB-1 (bundle 원본·설치본 세부 문서 구조 = Worker 제안 여지, Advisor 채택 대상 — 비차단).** DP-E6은 bundle 원본 물리 위치(`docs/v0.8-demo-fixtures/`)·설치본 배치 위치(`framework/plugins/<plugin-id>/`)·Remove 전수 대조 절차를 확정했다. 그러나 bundle/설치본 **내부의 구체 파일 구성·디렉터리 세부 구조**(예: 레퍼런스 Plugin의 Manifest 파일명·포함 Module 문서 배치)는 후속 시연 Task가 이 정본 위치·규약대로 생성할 때의 재량 여지가 있다(자매 Adapter Binding이 시연 소산·백엔드 하위 구조를 Worker 제안·Advisor 채택 대상 open_questions로 남긴 관례와 동형). 계약(10 §3) 변경이 아니므로 비차단이다. 시연 실물은 시연 PS-4가 §3 정본 위치·규약대로 생성해 실재하며(§7 재실측), 본 문서는 물리 위치·절차·판정 지점의 정본만 소유한다.
- **OQ-PB-2 (형태 B 경계 분할 — 비차단).** 무인 자동 Install/Activate/Deactivate/Remove 실행 코드(형태 B)가 `framework/plugins/` Module 구현 디렉터리와 `framework/adapters/claude/` 사이 어디에 분할 배치되는지는 형태 B 설계 시 확정 대상이다(§4, structure.md §4 규칙 4 defer, 자매 Adapter Binding의 형태 B 경계 분할 open_questions 관례 동형). Bootstrap(형태 A)에서는 규약 실현이므로 이 분할이 필요하지 않으며, 계약(10 §3) 변경이 아니므로 비차단이다.
- **OQ-PB-3 (번들 Hook/Skill 표면 정합 — 비차단, Wave 최종 검증 대상).** Plugin이 확장 요소(Hook/Skill)를 `provides`로 번들하는 시나리오에서, 그 등록 표면의 물리 바인딩은 08 §3.1-C·09 §3.1-A와 그 Adapter Binding 소관이다(10 §9 결정 기록·§4.2 SP-5). 본 문서는 Module 부분만 확정하고 확장 요소 표면은 소관 포인터로만 지시했다. 세 규격(10·08·09)의 등록·제거 계약 정합은 Wave 최종 검증에서 확인 대상이다(10 §9 조율 결정). 계약 변경이 아니므로 비차단이다.

---

## §10. 요약 (한눈에 보기)

- 이 문서 = `framework/adapters/claude/` 경계의 Plugins 트랙 바인딩. 10 §4.1(바인딩 표 8행)의 **v0.8 물리 실현 매핑**. 정본 = 10 §3·§4 + framework/plugins/ 3문서(본 문서는 물리 실현, 재정의 아님 — §0).
- **§2:** 10 §4.1 표 **8행 전부**를 물리 표면으로 매핑("정본 인용" 열 원문 그대로 + "물리 실현" 열 + "실재 여부" 열, 물리 실재/형태 A/형태 B/시연 소산 정직 구분). `framework/plugins/` 3문서·`.claude/agents/`·시연 픽스처 경계 관례 = 실재; 등록·배선·제거 오케스트레이션 = 규약 실현(형태 A); bundle 원본 = 시연 PS-4 생성 실재(`docs/v0.8-demo-fixtures/report-exporter/`)·설치본 = Install→Remove 후 부재(Remove 잔여물 0) — v0.9 T7 재실측.
- **§3 (DP-E6):** Plugin bundle 원본 = `docs/v0.8-demo-fixtures/`(ⓐ), 설치본 = `framework/plugins/<plugin-id>/`(ⓑ, 01 §4.1 Frozen 문면 인스턴스 — 새 백엔드 신설 아님, DP-W4 동형), Remove 잔여물 0 = **설치 이전 파일 목록 전수 대조**(ⓒ), AI 의존 산출물 = `.claude/` 격리(ⓓ, v0.8 레퍼런스 Plugin은 AI 비의존이라 구조만 확정). 4연산 예/아니오 물리 절차 + DP-E6이 01·10 §4.1과 충돌 0임을 근거와 함께 서술.
- **§4:** Plugins Provider `entrypoint`(4연산 노출) 물리 해소 표(형태 A: 수동 규약 배치·Register/Resolve·역순 Deregister·전수 대조 제거 / 형태 B: 무인 실행 코드 이연). Register/Resolve는 runtime-binding.md §3.2 참조(재정의 0).
- **§5:** plugin-lifecycle.md 검사 I1~I5·A1~A2·D1·R1~R2·IG의 **물리 실행 지점** 확정 — 검사 규칙 자체는 § 포인터 소비(재게재 0), 물리 실행 방식만 확정. 10 §7 검증 방법과 1:1 정합.
- **§6:** 10 §4.2 이식 교체 지점 **5건** 대응 표("교체되는 것 / 유지되는 것") — 유지 열이 Plugin Manifest 6필드·4연산 완료 조건·공통 Failure Report·INV-1~10을 전건 커버, 이식 불변(C-1) 재확인.
- **§7:** 실측 대조(2026-07-06 직접 실측; v0.9 T7 개정은 관찰 1 대상 행을 시연 후 재실측) — framework/plugins/ 3문서·자매 바인딩·`.claude/agents/`·시연 픽스처 경계 실재; **bundle 원본(`docs/v0.8-demo-fixtures/report-exporter/`) 실재·설치본(`framework/plugins/<plugin-id>/`) 부재 = Remove 잔여물 0**(시연 PS-4 생성·수명주기 완료). 실측 불일치 0건(L-07 재발 방지).
- 10·framework/plugins/ 3문서 계약 재정의 0, Glossary 용어 신설 0, 새 바인딩 계약 창설 0(새 연산·reason·필드·Config scope 0). 구체 AI·환경·경로 토큰은 이 Adapter 경계에서 허용된다(격리 지점). 동시 개정 형제 산출물 불인용(07 R2); 시연 실물은 시연 Task(PS-4)가 생성 완료(§3·§7, 생성 주체 구분 — L-07; v0.9 T7 개정이 시연 후 상태 반영). EX-P2 최초 작성은 이 1파일만 생성(07 R4).
