---
# UAHF Install Manifest — ① 최초 설치 스냅샷 (빈 프로젝트, preservedPaths: [])
# 시연 픽스처 산출물 — 실계약 문서·라이브 설정 표면 아님.
# 이 파일은 ① Install(빈 프로젝트) 직후의 Install Manifest 상태 기록이다 (12 §8 예1 — 빈 프로젝트).
# ⑤ 재설치(README.md 존치) 후의 상태는 new-project/install-manifest.md (preservedPaths: [README.md]).
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
preservedPaths: []
timestamp: "order:1 (순서 값 — 최초 설치 시점; 물리 벽시계 시각 주장 아님, L-09)"
---

# UAHF Install Manifest — ① 최초 설치 (빈 프로젝트)

이 매니페스트 스냅샷은 빈 프로젝트에 대한 최초 설치(① Install) 직후 상태다. `preservedPaths`는 빈 목록(`[]`) 이다 — 빈 프로젝트에는 보존할 기존 사용자 파일이 없다 (12 §8 예1).

이후 사용자 파일 `README.md`가 존치된 상태에서 재설치(⑤)되면 `preservedPaths`가 `[README.md]`로 갱신된다 (12 §8 예2 — 기존 프로젝트; new-project/install-manifest.md 참조).
