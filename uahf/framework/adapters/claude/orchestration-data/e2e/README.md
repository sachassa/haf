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

## 실측 (2026-07-13)

실 claude CLI headless(haiku·**5 세션**) 실증: Phase 1(exit 2·2 세션)·Phase 2(exit 0·3 세션).
run 데이터 = `runs/orch-j-e2e/`. replay 2회 동일. 최종 레지스트리:
`design-decision.md` v1 = user_approved · `impl-note.txt` v1 = verified(derivedFrom
`[design-decision.md]`).
