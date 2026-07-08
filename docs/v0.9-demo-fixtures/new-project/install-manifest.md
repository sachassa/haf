---
# UAHF Install Manifest — v0.9 Scaffold 시연 설치본 (docs/v0.9-demo-fixtures/new-project/)
# 시연 픽스처 산출물 — 실계약 문서·라이브 설정 표면 아님. 이 매니페스트는 이 격리 픽스처의
# 설치 상태 서술자다. 계약 정본 12 §3.2-B / 직렬화 정본 scaffold-binding.md §4 (재정의 0).
# 최초 상태(① 빈 프로젝트 설치): preservedPaths: []  (기록: install-manifest-initial.md)
# 현재 상태(⑤ README.md 존치 재설치 후): preservedPaths: [README.md]
frameworkVersion: "v0.9"
specVersion: "v0.1"
installedModules:
  - runtime
  - agent
  - verifier
installedArtifacts:
  - .claude/AGENT.md
  - .claude/CLAUDE.md
  - .claude/settings.json
  - .claude/agents/advisor.md
  - .claude/agents/planner.md
  - .claude/agents/worker.md
  - .claude/agents/verifier.md
  - framework/core/
  - framework/runtime/
  - framework/adapters/
  - specs/
  - install-manifest.md
preservedPaths:
  - README.md
timestamp: "order:2 (순서 값 — 재설치 시점; 물리 벽시계 시각 주장 아님, L-09)"
---

# UAHF Install Manifest (v0.9 Scaffold 시연 설치본)

이 매니페스트는 이 프로젝트(`docs/v0.9-demo-fixtures/new-project/`)에 설치된 UAHF 내용의 서술자다 (12 §3.2-B).

- `frameworkVersion` / `specVersion` 표기는 필수다 (12 INV-7, CK-7).
- `installedArtifacts`는 제거(Uninstall)·멱등성(재설치) 판정의 기준이다 (12 INV-4·INV-5).
- `preservedPaths`는 설치 시 보존된 기존 사용자 파일이다. 최초 설치(빈 프로젝트) 시 `[]`였고, 사용자 파일 `README.md` 존치 상태의 재설치(⑤) 후 `[README.md]`가 되었다. Uninstall은 이 경로를 보존한다 (12 INV-3·INV-5, CK-8).
- 계약 정본은 specs/12-scaffold.md §3.2-B, 직렬화 정본은 framework/adapters/claude/scaffold-binding.md §4다.

주: 이 파일은 시연 픽스처 경계 내부의 설치본 매니페스트이며 라이브 하네스 상태가 아니다. `installedModules`는 최소 필수 집합(runtime·agent·verifier)만 포함한다("필요한 모듈만" — 12 INV-2, CK-2).
