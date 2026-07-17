# UAHF Project Template (Scaffold 설치 템플릿 — Claude Code 바인딩)

이 디렉터리는 Scaffold가 신규 프로젝트에 UAHF를 설치할 때 배치하는 **프로젝트 템플릿의 물리 자산**이다 (12 §3.2-A Project Template의 Claude Code 실물).

이 템플릿의 구조·내용 목록의 정본은 `framework/adapters/claude/scaffold-binding.md §6`이며, 설치 절차의 정본은 같은 문서 §2·§3, 설치 가이드는 `uahf/docs/v0.9-install-guide.md@cd9247b`(산출물 수명 정책으로 작업 트리에서 제거·아카이브 — 열람: `git show cd9247b:uahf/docs/v0.9-install-guide.md`)다. 계약 정본은 specs/12-scaffold.md §3(재정의 금지)다.

## 구성 (12 §3.2-A 필수 6요소)

| 템플릿 자산 | 12 §3.2-A 필수 요소 | 설치 대상 경로 |
|---|---|---|
| `dot-claude/AGENT.md` | 규약 문서 (Governance) | `.claude/AGENT.md` |
| `dot-claude/CLAUDE.md` | 규약 문서 + Config Project scope 초기값 | `.claude/CLAUDE.md` |
| `dot-claude/agents/{advisor,planner,worker,verifier}.md` | Agent 정의 4종 | `.claude/agents/*.md` |
| `dot-claude/settings.json.example` | Config Project scope 초기값 (선택) | `.claude/settings.json` |
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

## 최소 구성 (설치 후 성립해야 하는 것)

설치 직후 최소 구성 집합(specs/13-harness.md §3.2-A)의 5요소가 성립해야 한다: 상위 규약 문서(`dot-claude/AGENT.md`) · Agent 역할 정의 4종(`dot-claude/agents/`) · 위임·완료/실패 보고 프로토콜(02 §3.2-B/C/D — 규약) · 검증 게이트(구현 주체와 검증 주체 분리 — Verifier/Advisor) · 작업 추적(위임 사이클·결정 기록 관행). 이 성립이 Runtime Bootstrap 성공(01 §3.1-C)과 루프 1사이클 구동의 전제다.
