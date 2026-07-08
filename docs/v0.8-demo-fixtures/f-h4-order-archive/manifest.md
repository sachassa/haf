---
# Module Manifest (01 §3.2-A)
id: order-archive
contract: HookModule
version: "1.0"
requires: []
entrypoint: ./action.sh
configSchema: null
replaceable: true
# Hook Binding (08 §3.2-D)
hooks:
  - hookId: archive
    event: agent.completionReport
    phase: after
    order: 20
    action: ./action.sh
    replaceable: true
---

# F-H4 — 순서 결정성 Hook `archive` (픽스처)

**시연 픽스처 — 실계약 문서 아님.** (결함 없음 — 통과 케이스.)

- 물리 위치: 픽스처 경계 (형태 A 규약 등록 — DP-E7).
- 08 §8 예3 동형. 짝: F-H3(`metrics`, order 10). 같은 (event, phase) = (`agent.completionReport`, `after`).

## Hook Binding (08 §3.2-D)

| 필드 | 값 | 근거 |
|---|---|---|
| `hookId` | `archive` | 유일 식별자 (08 §8 예3 인스턴스 값). |
| `event` | `agent.completionReport` | F-H3와 동일 카탈로그 Event. |
| `phase` | `after` | F-H3와 동일. |
| `order` | `20` | 순서 1차 기준(08 §3.1-D). F-H3(10)보다 크므로 **나중** 실행. |
| `action` | `./action.sh` | 순서 관측용 진입점 (order-trace append). |
| `replaceable` | `true` | 기본값. |

## 기대 관측 (08 §3.1-D / INV-5)

F-H3(order 10) → F-H4(order 20) 결정적 순서. order 동률이었다면 2차(Module 등록 순서) → 3차(hookId 사전순)로 결정되나(08 §3.1-D 3단 기준), 본 짝은 **1차 기준에서 결정**(order 10 ≠ 20)된다.
