# UAHF Specification Template

Version: 0.1

Status: Frozen (v0.1 기준선 — 공통 Specification 표준, 사용자 승인, 2026-07-05)

적용 대상: specs/00-glossary.md ~ specs/13-harness.md 전체

근거: ARCHITECTURE.md 0.2, ROADMAP.md v0.1, AGENT.md

---

# 1. 사용 규칙

모든 spec은 이 템플릿을 따른다.

- 필수 섹션(§0 ~ §9)을 동일한 순서로 포함한다.
- 해당 없는 섹션은 삭제하지 않는다. "해당 없음"과 그 이유를 한 줄로 남긴다.
- 용어는 specs/00-glossary.md에 정의된 것만 사용한다. 새 용어가 필요하면 Glossary에 먼저 추가를 요청한다.
- 추측하지 않는다. 미확정 사항은 §9 Open Questions에 기록하고 Advisor에게 에스컬레이션한다.
- 문체는 ARCHITECTURE.md를 따른다. 짧은 선언문, 한국어 본문, 영어 기술 용어.

---

# 2. Spec 본문 구조

## §0. Header

```
# specs/NN-<component> — <Component> Specification

Version: <spec 버전>
Status: Draft | Review | Frozen
근거: ARCHITECTURE.md <해당 섹션>
상위 규약: AGENT.md (Agent 관련 spec인 경우)
```

## §1. Purpose

- 이 컴포넌트가 해결하는 문제
- 이 컴포넌트의 책임 (1~3문장)
- Non-Goals (이 컴포넌트가 하지 않는 것)

## §2. Position

- 아키텍처 상 위치: Layer 이름 또는 Cross-cutting Service
- 의존하는 spec 목록 (이 spec을 읽기 전에 이해가 필요한 것)
- 이 spec에 의존하는 spec 목록

## §3. Core Contract (AI 비의존)

- 3.1 Interface — 입력 / 출력 / 완료 조건 / 실패 보고 포맷
- 3.2 Data Format — 파일 포맷, 메시지 포맷, 스키마
- 3.3 Invariants — 어떤 구현에서도 지켜야 할 불변 규칙

이 섹션에는 Claude 의존 내용이 한 줄도 들어가지 않는다.

## §4. Adapter Binding (환경 의존)

- 4.1 Claude Code Binding — v0.x에서 이 계약을 Claude Code로 구현하는 방법
- 4.2 이식 교체 지점 — 다른 AI 환경으로 이식할 때 바뀌는 것 전부

## §5. Memory Access (해당 시)

- Memory 접근은 Memory Service Interface(단일 Port) 경유만 허용된다.
- 읽기: 목적 / 범위 / 시점 (필요할 때만, 최소 범위로)
- 쓰기: 기록 대상 / Lesson 생성 조건

## §6. Failure Modes

- 대표 실패 시나리오와 대응
- Lesson 후보가 되는 실패 유형

## §7. Verification

- 완료 기준 — 검증 가능한 형태. "시연할 수 있는 문장"으로 작성한다.
- 검증 방법 — Verifier가 무엇을 어떻게 확인하는가

## §8. Examples

- 최소 1개의 구체적인 사용 예

## §9. Open Questions

- 미확정 사항 (Advisor 에스컬레이션 대상)
- 비어 있으면 "없음"으로 명시한다.

---

# 3. 품질 기준 (Spec Definition of Done)

spec은 다음 8개 항목을 모두 만족해야 Frozen이 될 수 있다.

1. 필수 섹션 §0 ~ §9가 모두 존재한다.
2. 완료 기준이 검증 가능하다 — 시연 시나리오로 환원된다.
3. Core Contract(§3)에 Claude 의존 요소가 0건이다.
4. Memory 접근이 있다면 Memory Service Interface만 참조한다.
5. 상호 참조(§2)가 실제 파일과 일치하고 순환 의존이 없다.
6. Glossary에 없는 용어를 새로 만들지 않았다.
7. Open Questions가 비어 있거나, 남은 항목이 Frozen을 막지 않는다고 Advisor가 판정했다.
8. Verifier 검증과 Advisor 승인을 통과했다.

---

# 4. Status 전이

Draft

↓

Review

↓

Frozen

- Draft: Worker 작성 중
- Review: 검증 및 Advisor 검토 중
- Frozen: v0.1 기준선 확정 — 이후 변경은 spec 버전 상승과 Revision History 기록이 필수다.

---

# 5. Revision History

- 0.1: 최초 설계 (Advisor)
- 0.1 채택: 사용자 승인으로 공통 Specification 표준 확정. 모든 spec 작성과 Advisor 검증의 기준 문서가 된다.
- 0.1 Frozen (2026-07-05): v0.1 기준선 확정 (사용자 승인). specs/00~13 전체가 함께 Frozen되었다. 이후 변경은 버전 상승과 Revision History 기록이 필수다.
