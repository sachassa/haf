# 프로젝트 스코프 설정 소스 — Generic 바인딩 실물 (BP-3, Project scope)

이 파일은 3계층 설정 소스 중 **프로젝트(Project) 스코프** 설정·정의 소스다(BP-3). Config 계약의 정본은 specs/01-runtime.md §3.1-B·§3.2-B이며, 이 파일은 그 계약을 재정의하지 않고 최소 인스턴스만 담는다.

## 설정 (key → value, 최소 인스턴스)

```
project.entrypoint.role = Advisor
project.conventions = ../conventions/agent-conventions.md
project.orchestrator.entrypoint = ../conventions/orchestrator-entrypoint.md
project.roles.dir = ../roles/
```

## 병합 (01 §3.2-B 정본 인용)

- 이 프로젝트 소스는 전역 소스(global-config.md)의 값을 덮어쓸 수 있고, 모듈(역할 정의 내부 설정 블록)이 다시 이를 덮어쓴다(우선순위 Module > Project > Global).
- 3계층 = 전역 소스 / 프로젝트 소스(이 파일) / 모듈(역할) 정의 파일 내부 설정 블록(roles/*.md 머리말 메타데이터 블록).
