---
# Module Manifest (01 §3.2-A)
id: order-metrics
contract: HookModule
version: "1.0"
requires: []
entrypoint: ./action.sh
configSchema: null
replaceable: true
# Hook Binding (08 §3.2-D)
hooks:
  - hookId: metrics
    event: agent.completionReport
    phase: after
    order: 10
    action: ./action.sh
    replaceable: true
---

# F-H3 — 순서 결정성 Hook `metrics` (픽스처)

**시연 픽스처 — 실계약 문서 아님.** (결함 없음 — 통과 케이스.)

- 물리 위치: 픽스처 경계 (형태 A 규약 등록 — DP-E7).
- 08 §8 예3 동형 — 같은 (event, phase)에 2 Hook, order 10/20으로 결정적 순서 실증(INV-5).
- 짝: F-H4(`archive`, order 20). 같은 (event, phase) = (`agent.completionReport`, `after`).

## Hook Binding (08 §3.2-D)

| 필드 | 값 | 근거 |
|---|---|---|
| `hookId` | `metrics` | 유일 식별자 (08 §8 예3 인스턴스 값). |
| `event` | `agent.completionReport` | 카탈로그(08 §3.2-A) — 완료 보고 생성 지점. hooks-binding §3: 형태 A 실계측 가능. |
| `phase` | `after` | F-H4와 동일. |
| `order` | `10` | 순서 1차 기준(08 §3.1-D). F-H4(20)보다 작으므로 **먼저** 실행. |
| `action` | `./action.sh` | 순서 관측용 진입점 (order-trace append). |
| `replaceable` | `true` | 기본값. |

## 기대 관측 (08 §3.1-D / INV-5)

같은 (event, phase)에서 F-H3(order 10) → F-H4(order 20) 순으로 결정적 실행된다 — 1차 기준 `order` 오름차순(10 < 20)에서 결정. 반복 실행에도 동일 순서(결정성, INV-5).
