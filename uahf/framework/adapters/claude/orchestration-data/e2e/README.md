# orchestration-data/e2e — 축소판 종단 dogfooding E2E 드라이버 (비프로덕션)

**이 디렉터리는 배포물이 아니다.** Project Orchestration S5 의 종단 흐름(시나리오 j)을 실
claude CLI headless 로 실증하기 위한 dogfooding 드라이버다(step-data/e2e 선례 동형). 여기는
Adapter 경계(orchestration-data/) 이하이므로 provider 토큰(claude CLI·모델 별칭·권한 플래그)
사용이 허용된다(격리 지점·PO-INV 8 무관).

## 무수정 재사용

중립 코드는 **라이브러리로 무수정 사용**된다 — 수정 0:

- 중립 Orchestrator: `orchestration/framework/orchestrator/`(orchestrator·revision·gates·
  allocation·artifacts).
- 중립 Step Host: `uahf/framework/loop/step-host/`.
- claude invoker: `uahf/framework/adapters/claude/step-invoker/claude_invoker.py`.

`LoggingClaudeInvoker`(`_orch_common.py`)는 `ClaudeInvoker` 를 **상속**만 하며 실제 코드 경로를
`super()` 로 그대로 실행하고 argv·원출력·종료 코드·session_id 를 `logs/` 에 캡처한다.

## 시나리오 (j) — 축소판 종단 흐름

```
python setup_j.py                        # runs/orch-j-e2e/ 물리화(초기 그래프·게이트 정책)
python run_orchestration.py <run-dir>    # Phase 1: 설계 실행 → user_decision 게이트 정지(exit 2)
python resolve_and_revise.py <run-dir>   # (시뮬레이션·라벨) 사용자 해소 + 구현 revision append
python run_orchestration.py <run-dir>    # Phase 2: 구현 실행 → review 게이트 → 완주(exit 0)
python replay_check.py <run-dir>         # 결정적 재개 판독(2회 실행 stdout 동일 = 결정성)
```

Windows 콘솔 인코딩 안전을 위해 `PYTHONUTF8=1` 로 실행한다.

## 정직 표기 (L-07·O5)

- **사용자 게이트 해소·구현 단위 제안은 드라이버 픽스처**이며 실 사용자·실 LLM 제안 step 이
  아니다. `logs/gate-resolution-record.json` 과 append-only 로그의 `annotation::sim` 이벤트에
  "드라이버 시뮬레이션(테스트 픽스처)·실 사용자 아님"을 명시 기록한다.
- 실증 대상 = 게이트 **물리 정지(exit 2)**·사용자 actor 적격성·revision 인과 사슬(PO-INV 5)·
  deterministic 재개·상류 재실행 흔적 0·산출물 approvalState 파생. 그 축들은 실 데이터
  (events.jsonl·revisions.jsonl·artifacts.jsonl·workspace)로 남는다.
- 산출 내용은 CP2 재현성을 위해 정확 내용으로 고정한 픽스처다(설계 메모를 exact-content 설계
  결정 레코드로 축약).
- **실 CLI 실패는 은폐하지 않는다** — 실 세션 stdout·argv 는 `logs/invoke-*.json` 에 그대로
  캡처된다.

## T1 Minimal Telemetry (2026-07-14 · 순수 판독)

- `collect_metrics.py <run-dir>...` — invoke 로그·mtime·(선택 `--git-anchor`) git ts 에서
  1차 분석 §15 지표를 `metrics/<runId>.run-metrics.json`·`metrics/aggregate.run-metrics.json`
  으로 재산출한다(원장 무수정·출력은 run 밖 `metrics/` 에만·등급 확인/계산/근사/불가/소실).
- `resolve_k/m/w.py` 는 해소 시점 `logs/stop-signal.json` 을 `stop-signal-<위상>.json` 으로
  mtime 보존 복사(`shutil.copy2`·덮어쓰기 금지)해 다중 게이트 run 의 선행 게이트 정지 시각
  소실을 막는다(**신규 run 에만 효력**).
- `metrics/harness-subagent-metrics.json` — 하네스 서브에이전트 토큰/시간 통지 실측치 전사 슬롯
  (빈 템플릿·기입은 Advisor 절차 소관).

## T3 Verification Architecture + Risk Routing (2026-07-14 · W1~W4)

### verify_run.py — 얇은 결정적 검증 러너 (W1·LLM 0·순수 판독·원장 무수정)

```
python verify_run.py <run-dir>... [--replay] [--git-hygiene] [-o <출력 디렉터리>]
```

기존 중립 검증기·순수 함수를 **조립 없이** 재사용해(collect_metrics 선례 — workspace makedirs
회피) 결정적 축을 검사한다. 리포트는 run 밖 `metrics/verify/<runId>.verify.json`. 검사 축:
(a) 원장 위생(seq/at 단조·ref.kind 관측 어휘·outcome 어휘·게이트 순서·simulated 라벨 정직성)·
(b) revision 무결(`validate_revision`/`fold`)·(c) plan 스키마(`validate_stage_plan`/
`validate_impl_plan` — artifact 실재 시)·(d) delegation 정합(`delegation_check`·W4 공유)·
(e) 계수 정합(`derive_registry` 대조)·[--replay] (f) k 계열 replay 결정성·[--git-hygiene] (g)
git porcelain. **결정적 검사는 러너가 산출하고 LLM CP2 는 의미 축을 전담**한다(T3 분리·SH-INV-4
무촉 — CP2 자체는 제거하지 않는다). Baseline 3+1 run 실행 결과 전건 pass·run 파일 mtime 불변.

### policy/allocation.json — Risk-based Model Routing (W2·opt-in·하위호환)

`build_orchestrator(_k)(run_dir, invoker, allocation_path=...)` 또는 `config.allocation_file`
로 배선한다. 미지정이면 현행 거동 완전 보존(allocation=None). 저위험 semantic=haiku·고위험/
기본=sonnet·CP2=sonnet(균일 haiku·CP2 haiku 고정 금지). capability class 별 CP2 차등은
`cp2ModelSlots`(가법·`policy/README.md` 참조). 자세한 계층·gate_policy 결합은 `policy/README.md`.

### 섀도 검증 (W3·기본 off·관측 전용)

`config.shadow_verify = {enabled, model, log_path?}` 로 켜면 `LoggingClaudeInvoker` 가 Verifier
invoke(criteria 실재)를 지정 상위 모델로 **병행 재호출**해 두 판정 일치 여부를 섀도 로그에
기록한다. **주 판정만 run 에 반영**(섀도는 관측 전용·실패해도 run 무영향·best-effort). 기본
off 시 invoke 거동 byte 동일. 이번 트랙은 실 기동 없이 합성 스텁 단위 테스트로만 확인
(LLM 비용 미발생).

### delegation 참조형 표준 (W4/T4-①)

`delegation_check.py` 가 3면(시나리오 프롬프트·`validate_*` 검증기·`verify_run` (d))의 단일
규칙 소유다. delegation.task/done 은 **참조형 sentinel**(`"위 task 필드와 동일"`·
`"위 done 필드와 동일"`·권장) **또는 상위 원문 전재**만 유효하고 요약·변형은 실패한다. m 성숙
run(sentinel)·w 구현 run(원문 전재) baseline 이 둘 다 통과한다(무회귀). Verifier 브리프도
"참조형 sentinel 은 계약 위반 아님·결정적 리포트 재구현 금지"를 명기한다.

### 테스트

- 중립 트리: `orchestration/framework/orchestrator/tests`(allocation 확장·descriptor-aware CP2)·
  `uahf/framework/loop/step-host/tests`(cp2_model_resolver seam)·`step-invoker/tests`.
- e2e 트리: `e2e/tests/`(delegation 경계·러너 위생 검사·섀도 스텁·번들 payload 계측 — 실 CLI 0).

### 전체 테스트 정본 호출 (R3 · 4-트리 러너 · deterministic·Skill 아님)

R3 의 목적 = 매 단계 4경로 명령을 재도출하는 수고 제거(튜닝 Before/After 효과 주장은 불포함).

정본 호출 = 이 러너 **또는** 아래 원 명령(4경로 병기) 중 택일 — 두 형태는 동일 트리를 실행한다:

```
# (A) 러너(권장·경로 역산)
python run_all_tests.py            # -q 기본. 추가 인자는 pytest 로 패스스루(예: -v -k foo).

# (B) 원 명령(저장소 루트에서·4경로 병기)
python -m pytest \
  orchestration/framework/orchestrator/tests \
  uahf/framework/loop/step-host/tests \
  uahf/framework/adapters/claude/step-invoker/tests \
  uahf/framework/adapters/claude/orchestration-data/e2e/tests -q
```

러너는 pytest 종료코드를 그대로 반환한다. **기대 통과 수는 여기에 하드코딩하지 않는다**(트랙
진행에 따라 증가 — stale 방지). 실측 통과 수는 실행 출력으로 확인한다.

## 실측 (2026-07-13)

실 claude CLI headless(haiku·**5 세션**) 실증: Phase 1(exit 2·2 세션)·Phase 2(exit 0·3 세션).
run 데이터 = `runs/orch-j-e2e/`. replay 2회 동일. 최종 레지스트리:
`design-decision.md` v1 = user_approved · `impl-note.txt` v1 = verified(derivedFrom
`[design-decision.md]`).
