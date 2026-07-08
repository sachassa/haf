---
# Install Manifest (정본 12 §3.2-B — 6필드; scaffold-binding.md §4 직렬화)
# 이 파일은 dogfooding/uahf-lessons/ 에 설치된 UAHF 내용의 서술자다.
# 값은 install-manifest.template.md 를 설치(Install) 시 채운 것이다.
# 멱등성(INV-4)·제거(INV-5) 판정의 기준이다.
frameworkVersion: "v1.0"        # 설치된 UAHF Framework 버전 (필수 — INV-7)
specVersion: "v0.1"             # 설치 기준이 된 spec 기준선 버전 (필수 — INV-7, Frozen)
installedModules:               # moduleSelection 해소 결과 — 실제 설치된 Module 집합 (필수)
  - runtime                     #   Runtime 호스팅·모듈 시스템 (필수)
  - agent                       #   Agent 역할 4종 (필수)
  - verifier                    #   검증 게이트 (필수)
  # 선택 Module(loop, memory, workflow, plugins)은 미포함 — 열람 CLI 개발에 불필요 (12 INV-2)
installedArtifacts:             # Scaffold가 생성·소유한 산출물 목록 (필수 — 제거·멱등성 기준)
  - .claude/AGENT.md
  - .claude/CLAUDE.md
  - .claude/settings.json
  - .claude/agents/advisor.md
  - .claude/agents/planner.md
  - .claude/agents/worker.md
  - .claude/agents/verifier.md
  - framework/core/            #   README(자리) + structure.md + config-schema.md
  - framework/runtime/         #   README(자리) + lifecycle.md + module-manifest.md + module-registry.md
  - framework/adapters/        #   README(자리 — 격리 지점)
  - specs/                     #   README(자리) + spec 기준선 15건 (00~13 + TEMPLATE)
  - install-manifest.md        #   Install Manifest 자신
preservedPaths: []             # 설치 시 보존된 기존 사용자 파일 (필수 — INV-3; 빈 프로젝트 설치 — 없음)
timestamp: "order:1 (순서 값 — L-09; 물리 벽시계 시각 아님)"   # 설치 시점 (선택)
---

# UAHF Install Manifest — dogfooding/uahf-lessons/

이 매니페스트는 `dogfooding/uahf-lessons/` 프로젝트에 설치된 UAHF 내용의 서술자다 (12 §3.2-B).

- 설치 원본 = `framework/adapters/claude/scaffold-template/`(프로젝트 템플릿 13파일) + spec 기준선(라이브 `specs/` 15건) + Core Contract 인스턴스 문서(라이브 `framework/core/` 2건·`framework/runtime/` 3건).
- `frameworkVersion`("v1.0") / `specVersion`("v0.1") 표기는 필수다 (12 INV-7, CK-7).
- `installedArtifacts`는 제거(Uninstall)·멱등성(재설치) 판정의 기준이다 (12 INV-4·INV-5). 물리 설치 파일 수 = 31 (+ 이 매니페스트 = 32).
- `preservedPaths`는 설치 시 보존된 기존 사용자 파일이다. 이 설치는 빈 프로젝트 대상이므로 빈 목록이다 (12 INV-3·CK-8, 12 §8 예1).
- 계약 정본은 specs/12-scaffold.md §3.2-B, 직렬화 정본은 framework/adapters/claude/scaffold-binding.md §4다. 재정의 0.
