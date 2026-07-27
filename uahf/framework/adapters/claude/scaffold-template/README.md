# UAHF Project Template (Scaffold 설치 템플릿 — Claude Code 바인딩)

이 디렉터리는 Scaffold가 신규 프로젝트에 UAHF를 설치할 때 배치하는 **프로젝트 템플릿의 물리 자산**이다 (12 §3.2-A Project Template의 Claude Code 실물).

이 템플릿의 구조·내용 목록의 정본은 `framework/adapters/claude/scaffold-binding.md §6`이며, 설치 절차의 정본은 같은 문서 §2·§3, 설치 가이드는 `uahf/docs/v0.9-install-guide.md@cd9247b`다. 계약 정본은 specs/12-scaffold.md §3(재정의 금지)다.

## 구성 (12 §3.2-A 필수 6요소)

| 템플릿 자산 | 12 §3.2-A 필수 요소 | 설치 대상 경로 |
|---|---|---|
| `dot-claude/AGENT.md` | 규약 문서 (Governance) | `.claude/AGENT.md` |
| `dot-claude/CLAUDE.md` | 규약 문서 + Config Project scope 초기값 | `.claude/CLAUDE.md` |
| `dot-claude/agents/{advisor,planner,worker,verifier}.md` | Agent 정의 4종 | `.claude/agents/*.md` |
| `dot-claude/settings.json.example` | Config Project scope 초기값 (선택) | `.claude/settings.json` |
| `dot-claude/hooks/design-guard/` (2파일) | 설계완성도 백스톱 훅 (운영 훅 — Component 아님) | `.claude/hooks/design-guard/` |
| `framework/core/` (자리) | Core 경계 | `framework/core/` |
| `framework/runtime/` (자리) | Core 경계 (Runtime) | `framework/runtime/` |
| `framework/adapters/` (자리) | Adapter 경계 | `framework/adapters/` |
| `specs/` (자리) | specs 디렉터리 | `specs/` |
| `install-manifest.template.md` | Install Manifest (12 §3.2-B) | 프로젝트 내 매니페스트 파일 |

주:

- **`dot-claude/` → `.claude/` 이름 변경.** 템플릿의 `dot-claude/`는 설치 시 대상 프로젝트의 `.claude/`로 배치된다. 템플릿 자산이 라이브 설정 표면으로 오인되지 않도록 `dot-claude/` 이름을 쓴다 (스캐폴드 관례). 이름 변경 매핑의 정본은 scaffold-binding.md §6이다.
- **Config Global scope는 사용자 환경 소관.** Global scope(Framework 전역 기본값)의 물리 소스는 사용자·환경 전역 설정이며 Scaffold는 이를 초기화·덮어쓰지 않는다. Scaffold는 Global·Project 두 스코프 중 Project scope만 대상 프로젝트에 배치하고, Global 기본값은 문서 기본값으로 제공한다 (12 §3.2-A 주, 01 §4.1).
- **Module scope Config는 초기화 대상 아님.** 각 Module이 소유한다 (12 §3.2-A 주).
- **Core부(`framework/core`·`framework/runtime` 자리)는 AI 의존 토큰 0건.** 설치된 Core 디렉터리가 CK-6(설치된 Core 디렉터리 AI 의존 0건)을 통과하도록 이 템플릿의 Core 자리 문서는 AI 비의존으로 작성되었다 (12 §3.2-C CK-6, 01 §3.3 INV-4).
- **specs/ 자리.** 설치 시 spec 기준선(v0.1 Frozen, 15건)이 이 자리에 배치된다 (specs/README.md의 배치 안내 참조).
- **설계완성도 백스톱 훅(`dot-claude/hooks/design-guard/`).** 필수 설계 산출물(design-manifest) 미완 시 소비 프로젝트의 `src/` Write/Edit/MultiEdit 를 PreToolUse 에서 차단하는 "존재 최후방어"다 (§DC-3). 두 파일(`pretooluse_design_guard.py`·`design_completeness.py`)은 `orchestration/adapters/claude/` 원본의 **벤더링 미러**이며, 독립 소비 리포에는 `orchestration/` 트리가 없으므로 자기완결 형태로 `.claude/hooks/design-guard/`에 병치 배치된다(guard 가 병치된 checker 를 `Path(__file__).parent` 기준으로 import). 배선은 `settings.json.example`의 `hooks.PreToolUse` 에 있으며 설치 시 `.claude/settings.json` 으로 배치된다. 이 디렉터리는 **운영 훅 스크립트 자리**이지 Hooks Component 의 Hook Module 이 아니다(manifest.md 를 두지 않는다 — 운영 훅 vs Component 경계).
- **전제조건 — PyYAML 설치 필요.** 설계완성도 checker(`design_completeness.py`)가 정책(`default-policy.yaml`)을 파싱하려면 로컬 라이브러리 **PyYAML** 이 소비 리포 실행 환경에 설치돼 있어야 한다(`pip install pyyaml`). PyYAML 부재 시 checker 는 "PyYAML 미설치" 오류를 반환하고, guard 는 이를 설계 미완으로 간주해 `src/` 쓰기를 차단(fail-closed)할 수 있다. 백스톱을 사용하는 소비 프로젝트는 PyYAML 을 선설치한다.

## 최소 구성 (설치 후 성립해야 하는 것)

설치 직후 최소 구성 집합(specs/13-harness.md §3.2-A)의 5요소가 성립해야 한다: 상위 규약 문서(`dot-claude/AGENT.md`) · Agent 역할 정의 4종(`dot-claude/agents/`) · 위임·완료/실패 보고 프로토콜(02 §3.2-B/C/D — 규약) · 검증 게이트(구현 주체와 검증 주체 분리 — Verifier/Advisor) · 작업 추적(위임 사이클·결정 기록 관행). 이 성립이 Runtime Bootstrap 성공(01 §3.1-C)과 루프 1사이클 구동의 전제다.
