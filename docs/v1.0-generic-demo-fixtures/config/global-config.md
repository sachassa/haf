# 전역 스코프 설정 소스 — Generic 바인딩 실물 (BP-3, Global scope)

이 파일은 3계층 설정 소스 중 **전역(Global) 스코프** 설정 소스다(BP-3 — 파일 시스템 상 설정 소스의 환경 중립 실현). Config 계약의 정본은 specs/01-runtime.md §3.1-B·§3.2-B이며, 이 파일은 그 계약을 재정의하지 않고 최소 인스턴스만 담는다.

## 설정 (key → value, 최소 인스턴스)

```
framework.retry.limit = 2
memory.recall.policy = minimal-scope (필요할 때만·목적 명시·최소 범위)
```

## 스코프·우선순위 (01 §3.2-B 정본 인용)

- 스코프: Global / Project / Module 3계층.
- 병합 우선순위: **Module > Project > Global** (정본 규약, 01 §3.2-B). 이 전역 소스는 최하위 우선순위 기본값을 제공한다.
- 물리 위치는 파일 시스템 규약으로만 지정한다 — 특정 설정 디렉터리 제품 표기에 종속되지 않는다.
