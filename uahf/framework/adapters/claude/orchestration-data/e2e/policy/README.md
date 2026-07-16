# e2e/policy — Risk-based Model Routing 정책 데이터 (T3 W2·신규 run 템플릿)

**비프로덕션 정책 데이터.** Adapter 격리 경계(orchestration-data/e2e/) 소속이므로 provider·
모델 고유명(`haiku`·`sonnet`)이 허용된다(중립 코드 아님·PO-INV 8 무관). 중립 코드
(`orchestration/framework/orchestrator/allocation.py`)는 이 데이터를 불투명 슬롯 문자열로만
소비한다.

## allocation.json — 배선 방법 (하위호환·opt-in)

드라이버 빌더에 정책을 배선한다. **미지정이면 현행 거동 완전 보존**(allocation=None):

```python
# config.json 에 "allocation_file": "policy/allocation.json" 을 넣거나,
build_orchestrator_k(run_dir, invoker, allocation_path="policy/allocation.json")
build_orchestrator(run_dir, invoker, allocation_path="policy/allocation.json")
```

경로는 절대경로이거나 `e2e/` 기준 상대경로다. 우선순위 = 명시 인자 > `config.allocation_file`
> None. **시나리오가 Task 에 `model` 슬롯을 명시 지정하면 그 값이 우선한다**(명시값 우선·
05 §3.4·§3.5) — 현재 시나리오(k/m/w)는 `model="sonnet"` 을 명시하므로 allocation 을 배선해도
Worker 슬롯은 sonnet 그대로다. allocation 은 **model 슬롯을 비운 신규 run** 에서 위험도별
차등을 실현한다.

## T3 4계층 위험도 모델 반영

| 계층 | 소관 | 이 정책에서 |
|---|---|---|
| Deterministic | LLM 0 (결정적 검증 러너 `verify_run.py`) | 모델 슬롯 아님(러너 소관) |
| Low-risk Semantic | 약 티어 | `slots["low-risk-semantic"] = "haiku"` |
| High-risk Semantic | 상위 티어 | `slots["high-risk-semantic"] = "sonnet"` (기본·안전측) |
| Critical | 상위/사용자 | 모델 슬롯 아님 — `gate_policy` 의 `user_decision_required`(사용자 확정 권위·T2)로 처리 |

- **균일 haiku 고정 금지.** 저위험만 haiku, 고위험·기본은 sonnet 이다. 매칭 실패·미지정
  capability 는 `defaultSlot`(sonnet·안전측)으로 귀결한다.
- **CP2 는 haiku 고정 금지(SH-INV-4 무촉).** `cp2ModelSlot = "sonnet"` — CP2 자체는 제거하지
  않으며 검증 단위는 상위 티어로 판정한다(상시 CP2 불변). CP2 는 대상 step 슬롯을 상속하지 않고
  독립 정책 슬롯을 쓴다(OQ-SH-4 해소·05 §3.5 "CP2 = 독립 정책 행").

## descriptor-aware CP2 슬롯 (가법 확장·spec 문면 대조 통과분)

`ModelSelectionPolicy` 는 `cp2ModelSlots`(capability class → CP2 슬롯 오버라이드) 가법 필드를
지원한다(allocation.py — 위험도별 CP2 차등). 매칭 class 가 없으면 전역 `cp2ModelSlot` 으로
폴백하며, 빈 값(기본)이면 전역 단일 거동을 완전 보존한다. 배선은 orchestrator 가
`StepHost(cp2_model_resolver=...)` 로 전달하고 Host 가 CP2 만 그 슬롯으로 디스패치한다(전달만·
해석 0). 예:

```json
"modelSelection": {
  "slots": {"low-risk-semantic": "haiku", "high-risk-semantic": "sonnet"},
  "cp2ModelSlot": "sonnet",
  "cp2ModelSlots": {"low-risk-semantic": "haiku", "high-risk-semantic": "sonnet"}
}
```

**해소(follow-up 완결).** 위 `cp2ModelSlots` 는 코드(allocation.py)·단위 테스트로 실증되며,
`orchestration/framework/orchestrator/model_selection_schema.json` 이 이제 이 필드를 **가법 등재**
한다(선택·object of strings·최상위 `additionalProperties: false` 닫힌 스키마 유지). 따라서
`cp2ModelSlots` 를 데이터로 쓰는 allocation.json 도 스키마-유효이며, 위 `allocation.json` 템플릿은
전역 `cp2ModelSlot`(안전측 폴백)과 함께 `cp2ModelSlots`(capability class 별 CP2 차등)를 실제로 쓴다.
생략/빈 객체(기본)면 전역 단일 거동을 완전 보존한다(기존 데이터 무회귀).

## Gate Policy 결합 (Critical = 사용자 게이트·T2 기존 기능)

고위험/Critical 단위의 독립 2차 검증 강제는 모델 라우팅이 아니라 **Gate Policy**(T2)의
`requireIndependentReview` 로 실현한다(allocation 과 직교). 예시 gate_policy entry:

```json
{"target": {"unitType": "high-risk"}, "gate": "review_required", "requireIndependentReview": true}
```

이때 review_required 는 유효 CP2 evidence 재사용으로 해소하지 않고 항상 독립 Verifier 를
재디스패치한다(gates.py `requires_independent_review`). 모델 차등(allocation)과 검증 강도
차등(gate_policy)은 두 축이며 섞이지 않는다.
