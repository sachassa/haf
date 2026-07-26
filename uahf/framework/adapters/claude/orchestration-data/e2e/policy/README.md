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

## allocation-lightweight.json — 경량 레인 프로파일 (비례화 트랙 W3-a)

경량 레인(절차 비례화 트랙)용 정책 데이터 1건이다. `allocation.json` 과 **형식 동일**이며 두
지점만 다르다.

| 지점 | `allocation.json` | `allocation-lightweight.json` |
|---|---|---|
| `cp2ModelSlots` | `{low-risk-semantic: haiku, high-risk-semantic: sonnet}`(2 class 명시) | `{low-risk-semantic: haiku}`(저위험 1 class만 — 나머지는 전역 `cp2ModelSlot` 폴백) |
| `registry.specs` | 7행 | 7행(같은 수 — `spec-sd-*`·`spec-impl-plan`·`*` 존치) |

- **CP2 는 제거·조건화되지 않는다.** 이 파일이 바꾸는 것은 CP2 **모델 슬롯**뿐이다. CP2 디스패치
  자체는 `uahf/framework/loop/step-host/host.py` `_dispatch_cp2` 무조건 호출이며 정책 데이터가
  닿는 분기가 없다(SH-INV-4·상시 CP2 불변). 이 파일에 CP2 를 끄는 키는 존재하지 않는다.
- **저위험만 저티어.** `cap-impl-mechanical`(저위험 기계적 구현 단위) → `low-risk-semantic` →
  CP2 슬롯 `haiku`. 그 밖의 모든 capability 는 `spec-default`(`*`) → `high-risk-semantic` →
  `cp2ModelSlots` 미매칭 → 전역 `cp2ModelSlot`(`sonnet`·안전측)으로 귀결한다.
- **저위험 capability 어휘는 데이터 소관·가법**이다. selector 매칭은 정확 문자열 일치(글로브
  없음)이므로 저위험 단위를 늘리려면 `registry.specs` 에 행을 **추가**한다. 어휘를 코드에 넣지
  않는다.
- **모델 차등 ≠ 판정 근거.** 어떤 근거로 CP2 가 Pass/Fail 을 내는가(결정적 스크립트 AC 등)는
  위임 브리프의 done 축 소관이며 이 정책 데이터의 표면이 아니다. 이 파일은 판정 **주체·실행
  여부**를 바꾸지 않는다.

## allocation_file 배선 — 런처 표면과 경로 해석 기준

`orchestration/adapters/claude/` 런처가 `allocation_file` 을 **생산·전달**한다(종전에는 소비
슬롯만 있고 생산자가 없어 런처 경로에서 allocation 이 항상 `None` 이었다).

| 지점 | 물리 | 거동 |
|---|---|---|
| config 키 생산 | `contract_to_graph.build_config(..., allocation_file=None)` | 값이 있을 때만 `config["allocation_file"]` 을 **추가**한다. 미지정 시 키 부재 → config.json 직렬화 byte 동일 |
| CLI 표면 | `orchestrate_project.py --allocation-file <경로>` | `prepare_run` → `compile` → `build_config` 로 전달 |
| 명시 인자 전달 | `orchestrate_project.build(run_dir, invoker, allocation_path)` → `build_orchestrator_k(run_dir, invoker, allocation_path)` | `--resume` 경로에도 플래그가 반영된다(조용한 무시 방지) |

**상대경로 해석 기준 = `orchestration-data/e2e/` 디렉터리(`_orch_common.HERE`)** 이며 `run_dir`
기준이 아니다. 절대경로도 허용된다. 우선순위 = 명시 인자 > `config.allocation_file` > `None`.

- 경로 해석은 **소비 슬롯 `resolve_allocation` 단일 소유**다. 런처는 문자열을 그대로 넘기며
  자체 해석·검증을 하지 않는다(제2 해석 지점 신설 0).
- 따라서 런처를 임의 cwd 에서 호출해도 `--allocation-file policy/allocation-lightweight.json`
  은 이 디렉터리의 파일로 해석된다(cwd 무관·결정적).
- 존재하지 않는 경로를 주면 조립 시점에 예외로 표면화된다(침묵 무시 0 — `logs/failure.json`
  기록 후 재raise).

`uaf-verified:` 위 표의 좌표·거동은 `contract_to_graph.py`(`build_config`·`compile`)·
`orchestrate_project.py`(`prepare_run`·`build`·`main`·`_drive`)·`_orch_common.py:248-264`
(`resolve_allocation`)·`k_common.py:30·58`(`build_orchestrator_k`)·
`orchestrator.py:462-486`(`_new_host` cp2 resolver 배선)·`allocation.py:257-269·316-325`
(`cp2_model_for`)·`host.py:280·326-332`(무조건 CP2 디스패치 + 슬롯 우선순위)를 직접 판독하고,
`tests/test_allocation_wiring.py` 실행으로 대조해 얻었다. **검색 범위** = allocation_file·
cp2ModelSlots 문자열의 리포 전수 grep + 그로부터 추적한 호출 지점이며, 소비 프로젝트 워킹트리·
실 LLM 발화 run 은 범위 밖이다(실 CP2 모델 슬롯의 라이브 관측은 오프라인 stub invoker 원장으로
대조했다).

## Gate Policy 결합 (Critical = 사용자 게이트·T2 기존 기능)

고위험/Critical 단위의 독립 2차 검증 강제는 모델 라우팅이 아니라 **Gate Policy**(T2)의
`requireIndependentReview` 로 실현한다(allocation 과 직교). 예시 gate_policy entry:

```json
{"target": {"unitType": "high-risk"}, "gate": "review_required", "requireIndependentReview": true}
```

이때 review_required 는 유효 CP2 evidence 재사용으로 해소하지 않고 항상 독립 Verifier 를
재디스패치한다(gates.py `requires_independent_review`). 모델 차등(allocation)과 검증 강도
차등(gate_policy)은 두 축이며 섞이지 않는다.
