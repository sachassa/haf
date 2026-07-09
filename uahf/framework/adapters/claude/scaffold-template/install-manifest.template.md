---
# Install Manifest (정본 12 §3.2-B — 6필드; scaffold-binding.md §4 직렬화)
# 이 파일은 Install Manifest 템플릿이다. 설치(Install) 시 아래 값이 채워져
# 대상 프로젝트에 매니페스트 파일로 배치된다. 멱등성(INV-4)·제거(INV-5) 판정의 기준이다.
frameworkVersion: "v1.0"        # 설치된 UAHF Framework 버전 (필수 — INV-7)
specVersion: "v0.1"             # 설치 기준이 된 spec 기준선 버전 (필수 — INV-7, Frozen)
installedModules:               # moduleSelection 해소 결과 — 실제 설치된 Module 집합 (필수)
  # 최소 필수 집합(Runtime Bootstrap 필수 계약 + 최소 구성 집합 13 §3.2-A)
  - runtime                     #   Runtime 호스팅·모듈 시스템 (필수)
  - agent                       #   Agent 역할 4종 (필수)
  - verifier                    #   검증 게이트 (필수)
  # (선택 Module은 moduleSelection에 따라 추가 — 예: loop, memory, workflow, plugins)
installedArtifacts:             # Scaffold가 생성·소유한 산출물 목록 (필수 — 제거·멱등성 기준)
  - .claude/AGENT.md
  - .claude/CLAUDE.md
  - .claude/agents/advisor.md
  - .claude/agents/planner.md
  - .claude/agents/worker.md
  - .claude/agents/verifier.md
  - framework/core/            #   (배치된 Core 계약 문서)
  - framework/runtime/         #   (배치된 Runtime 프로토콜 문서)
  - framework/adapters/        #   (배치된 Adapter Binding 산출물)
  - specs/                     #   (배치된 spec 기준선)
  - <this manifest file>       #   Install Manifest 자신
preservedPaths: []             # 설치 시 보존된 기존 사용자 파일 목록 (필수 — INV-3; 빈 프로젝트면 빈 목록)
timestamp: "<install-time>"     # 설치 시점 (선택)
---

# UAHF Install Manifest

이 매니페스트는 이 프로젝트에 설치된 UAHF 내용의 서술자다 (12 §3.2-B).

- `frameworkVersion` / `specVersion` 표기는 필수다 (12 INV-7, CK-7).
- `installedArtifacts`는 제거(Uninstall)·멱등성(재설치) 판정의 기준이다 (12 INV-4·INV-5).
- `preservedPaths`는 설치 시 보존된 기존 사용자 파일이다. Uninstall은 이 경로를 보존한다 (12 INV-3·INV-5, CK-8).
- 계약 정본은 specs/12-scaffold.md §3.2-B, 직렬화 정본은 framework/adapters/claude/scaffold-binding.md §4다.
