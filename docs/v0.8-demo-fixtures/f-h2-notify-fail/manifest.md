---
# Module Manifest (01 §3.2-A)
id: notify-fail
contract: HookModule
version: "1.0"
requires: []
entrypoint: ./action.sh
configSchema: null
replaceable: true
# Hook Binding (08 §3.2-D)
hooks:
  - hookId: notify-fail
    event: lifecycle.complete
    phase: after
    order: -10
    action: ./action.sh
    replaceable: true
---

# F-H2 — 비차단 실패 Hook (픽스처)

**시연 픽스처 — 실계약 문서 아님.**
**의도적 결함 정당 보유.** 이 Hook의 action은 시연을 위해 **의도적으로 실패**(timeout/오류 모사)하도록 구성됐다. 이 결함은 비차단 격리(08 §3.1-E·INV-2)를 실증하기 위한 정당한 보유물이며, 실계약 문서(specs/08 §3)의 결함이 아니다. 픽스처 경계(`docs/v0.8-demo-fixtures/`) 내부에만 존재하고 verifier_scope에서 제외된다(절차서 §4.1, DP-E7).

- 물리 위치: 픽스처 경계 (형태 A 규약 등록 — 라이브 표면 `.claude/hooks/` 미배치, DP-E7). 시연 Dispatch가 이 경계의 등록을 참조한다.
- 08 §8 예2 동형 (비차단 실패). 단, 본 작업·다른 Hook(F-H1) 계속 실행을 함께 실증하기 위해 F-H1과 **같은 (event, phase) = (`lifecycle.complete`, `after`)** 에 바인딩한다.

## Hook Binding (08 §3.2-D)

| 필드 | 값 | 근거 |
|---|---|---|
| `hookId` | `notify-fail` | 유일 식별자. |
| `event` | `lifecycle.complete` | F-H1과 같은 이벤트에 co-dispatch → INV-2("다른 Hook 계속") 실증. |
| `phase` | `after` | F-H1과 동일 phase. |
| `order` | `-10` | 정수 order (작을수록 먼저, 08 §3.2-D). **F-H1(order 0)보다 먼저 실행**하도록 배치 → 실패한 F-H2 다음에도 F-H1이 계속 호출됨을 보인다(08 §3.1-D "한 Hook의 실패가 다른 Hook 호출을 막지 않는다"). 음수는 유효한 정수 order다. |
| `action` | `./action.sh` | 의도적 실패 진입점. |
| `replaceable` | `true` | 기본값. |

## 기대 관측 (08 §3.1-E / INV-2)

Dispatch 5단계에서 이 action이 오류(exit≠0)로 실패하면, Hook Failure Report(08 §3.2-E / hooks-binding §5.3)가 `blocking=false`·`lesson_candidate=예`로 남고, **본 작업과 다른 Hook(F-H1)은 계속 진행**된다. 본 작업(이벤트 원천 연산)의 결과는 Hook 결과와 독립이다(INV-1).
