---
# Module Manifest (정본 01 §3.2-A — 7필드; hooks-binding §4.1 직렬화)
id: audit-complete
contract: HookModule
version: "1.0"
requires: []
entrypoint: ./audit.sh
configSchema: null
replaceable: true
# Hook Binding (정본 08 §3.2-D — 6필드; hooks-binding §4.2 직렬화)
# 한 Module은 하나 이상의 Hook Binding을 담을 수 있다 (08 §3.2-D). 이 Module은 1건.
hooks:
  - hookId: audit-complete
    event: lifecycle.complete
    phase: after
    order: 0
    action: ./audit.sh
    replaceable: true
---

# F-H1 — 레퍼런스 Hook Module `audit-complete`

레퍼런스 Hook Module (v0.8 Extension System 시연 EX-DH). 08 §8 예1 동형 — "모든 작업이 완료될 때 감사 로그를 남긴다."

- 물리 위치: `.claude/hooks/audit-complete/` (라이브 표면 존치 — DP-E7 정상 레퍼런스, hooks-binding §4.1 자기완결 경계).
- 결함 지위: 결함 없음 (통과 케이스).

## Module Manifest (01 §3.2-A 7필드)

| 필드 | 값 | 필수 | 근거 |
|---|---|---|---|
| `id` | `audit-complete` | 예 | Module 고유·안정 식별자 = hookModuleId (디렉터리명, hooks-binding §4.3 Register `DuplicateId` 방지). |
| `contract` | `HookModule` | 예 | 01 §3.2-A `contract` 필수 필드 충족용 인스턴스 값. **08·hooks-binding은 Hook Module의 정본 contract 값을 규정하지 않으므로 이는 Worker 제안 인스턴스 값이며 Advisor 채택 대상이다(hooks-binding OQ-EH2). 신규 Glossary 용어 창설이 아니다** (완료 보고 open_questions 참조). |
| `version` | `1.0` | 예 | Module 버전. |
| `requires` | `[]` | 아니오(기본 없음) | 의존 contract 없음. |
| `entrypoint` | `./audit.sh` | 예 | 형태 A(Bootstrap)에서 이 경계 안 action 진입점으로 규약 실현 (hooks-binding §4.4). |
| `configSchema` | `null` | 아니오 | 미선언. |
| `replaceable` | `true` | 아니오(기본 true) | 01 INV-1(동일 contract·소비자 참조 불변). |

## Hook Binding (08 §3.2-D 6필드)

| 필드 | 값 | 필수 | 근거 |
|---|---|---|---|
| `hookId` | `audit-complete` | 예 | Hook 고유·안정 식별자 (across Module 유일). |
| `event` | `lifecycle.complete` | 예 | 카탈로그(08 §3.2-A / hooks-binding §3) Event ID — Complete 단계 전이. hooks-binding §3: `lifecycle.complete`는 형태 A 실계측 가능(★ 시연 소비 예정). |
| `phase` | `after` | 예 | Complete 전이 기록 직후. |
| `order` | `0` | 아니오(기본 0) | 실행 우선순위. |
| `action` | `./audit.sh` | 예 | 이 Module 경계 안 action 진입점 (감사 기록). Manifest `entrypoint`와 정합 (hooks-binding §4.4). |
| `replaceable` | `true` | 아니오(기본 true) | 01 INV-1. |

## 동작 (08 §3.1-B / INV-3)

`audit.sh`는 전달된 Event Record(08 §3.2-C / hooks-binding §5.2)를 **읽기 전용**으로 소비하고(INV-3), 자기 경계 안 부수 동작(감사 기록 생성)만 수행한다 — 이벤트 원천의 입력·출력·상태를 변경하지 않는다(08 §3.1-B 할 수 없는 것). 본체(Loop·Runtime)의 코드·규격은 이 Module 추가로 한 줄도 바뀌지 않는다(INV-1·INV-4 — Runtime Module 등록 재사용).

`occurredAt`은 순서 값(논리 시각)이며 물리 벽시계 시각이 아니다 (hooks-binding §5.2, L-09).

## 정본 경계

Hook Binding 6필드·Event 카탈로그·순서·격리·비차단 계약의 정본은 specs/08-hooks.md §3이다. 이 파일은 그 계약의 물리 인스턴스이며 계약을 재정의하지 않는다 (Frozen 08 재정의 0).
