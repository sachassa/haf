---
description: UAF 구현 단계 진입점 /implement의 물리 발화 형태 — 확정 Contract를 가진 소비 프로젝트의 구현을 Project Orchestrator 엔진(원장·게이트 큐)으로 구동하고, 게이트 제시·해소 지점을 정본 포인터로 안내한다.
---

# /implement — UAF 구현 오케스트레이션 진입 (물리 발화: uaf-implement 명령)

작성일: 2026-07-18
상태: v1.0 (오케스트레이션 배선 수정 트랙 · F1 발화 — F3 런처/F5 게이트 브리지와 공동 도입)
상위 규약: .claude/AGENT.md · .claude/CLAUDE.md
성격: UAF 구현 진입 명령 — 형태 A 문서 명령(이 파일 자체 실행 코드 0) + 형태 B 런처 호출(orchestrate_project.py) + 형태 A 폴백 공존

---

## §0. 이 명령의 위치와 성격

- 이 파일은 `.claude/commands/` 아래의 **UAF 구현 진입 표면**이다 — Entry(`/uaf-new`·`/uaf-continue`)가 Discovery Request까지 멈추는 것과 달리, 확정 Project Contract를 가진 소비 프로젝트의 **구현 단계**를 물리 발화한다. `uaf-` 접두는 UAF 네임스페이스 표면화·빌트인 충돌 회피용이다.
- `.claude/commands/`는 환경 의존 격리 표면이므로 구체 환경 토큰(python·경로·CLI 옵션)의 사용이 허용된다(structure.md §2 Adapter 경계, uaf-new.md §0 선례 동형).
- **형태 A(문서 명령) — 이 명령 파일 자체는 실행 코드 0.** 오케스트레이션 구동은 두 경로가 공존한다 — (i) **형태 B 런처**(권장): 결정적 프로덕션 런처 `orchestration/adapters/claude/orchestrate_project.py`를 호출해 엔진을 구동한다. (ii) **형태 A 폴백**: 런처 미가용 시 주 세션이 아래 절차(컴파일→run_dir 조립→구동→게이트 해소→재개)를 규약대로 실수행한다. 어느 경로든 05 spec 계약·게이트 5종은 동일하다.
- **정본 재정의 0.** 이 문서는 어떤 계약·게이트 규칙도 스스로 확정하지 않는다. 절차·게이트·불가침은 전부 **정본 포인터**(05 spec·binding·gates.py)로만 안내하며 값을 하드코딩하지 않는다.
- **2층 규율(재발방지).** 이 진입은 **Run 조율(엔진)** 층이다 — 주 세션 Advisor가 원장 없는 임시 Worker 직접 디스패치로 프로젝트를 구현하지 않고, headless Project Orchestrator 엔진에 위임한다. 단위 실행만 엔진이 fresh-context Worker로 디스패치한다(.claude/AGENT.md §Invariants "Run 조율 우회 금지" · 05 §2.1 3분해).

---

## §1. 목적

`/implement` 호출 시 **확정 Contract(project-contract.vN.md)를 가진 소비 프로젝트의 구현**을 오케스트레이션 엔진으로 구동하도록 안내한다 — 엔진은 Contract를 초기 Work Graph로 컴파일해 스케줄·게이트·재개를 결정적으로 조율하고, 그 과정에서 **RevisionEvent/ArtifactRecord 원장 + 게이트 큐(사용자/CP2/CP3)**를 run 데이터로 남긴다. 출력은 원장 기반 오케스트레이션 run이다 — 원장 없는 임시 위임은 이 명령의 실패다(05 §2·§3).

전제: 대상 프로젝트에 확정 Contract가 존재해야 한다(없으면 `/uaf-continue`/`/uaf-new` → Discovery/Solution Design 선행). Contract 유무 판정은 Entry Resolution 소관이다.

---

## §2. 진입 절차 (오케스트레이션 구동 — 정본 포인터)

호출되면 아래 [형태 B 런처 호출]이 권장 경로이고 [형태 A 폴백]이 공존한다. 각 단계·게이트는 정본에서 회수한다(값 하드코딩 없음).

### 형태 B 런처 호출 (권장 경로)

주 세션은 결정적 프로덕션 런처를 호출해 엔진을 구동한다:

```
python orchestration/adapters/claude/orchestrate_project.py <project_root> --phase "<phase>" [--mode incremental] [--run-id <slug>] [--retry-limit N]
```

- 런처는 (1) `contract_to_graph.compile`로 대상의 최신 Contract vN을 초기 Work Graph(단일 proposal seed) + gate_policy + config로 컴파일하고, (2) run_dir(`uahf/framework/adapters/claude/orchestration-data/runs/<run-id>/`, binding §5.3)를 조립하며(소비 프로젝트 워크스페이스 보존·삭제/스캐폴드 금지), (3) 중립 조립부(`build_orchestrator_k`)를 무수정 재사용해 오케스트레이터를 구동한다.
- **엔진이 판단하지 않는다**(05 §2 기계 구동자). 의미 판단은 국소 fresh-context Step(실 LLM), 확정 권위는 사용자다.

### 게이트 정지 → 제시 → 해소 → 재개 (게이트 브리지 — OQ-PO-B3)

- **정지 신호:** 정지 게이트(`user_decision_required`·`escalation_required`)가 미해소면 런처는 `logs/stop-signal.json`(`pending_gates:[{gate_id,gateKind,target,scoped_question,since}]`)을 기록하고 **exit 2**로 멈춘다. 엔진은 headless — 사용자 채널과 분리된다(binding §3.2).
- **제시:** 주 세션 Advisor가 `logs/stop-signal.json`을 읽어 각 대기 게이트를 사용자에게 표면화한다(gateKind·대상 단위·scoped_question). CP2는 게이트가 아니라 상시 하한(우회 없음)이며, CP3는 `approval_required`(Advisor 경계 승인)로 큐에 오른다.
- **해소:** 게이트별 적격 actor만 해소한다(자격은 코드 소유·우회 금지):
  ```
  python orchestration/adapters/claude/resolve_gate.py <run_dir> --gate-kind {user_decision|escalation|approval-escalation} --actor {human|Advisor} [--gate-id <gate_id>] [--response "<원문>"]
  ```
  `user_decision_required`는 **사용자(human)만** 해소한다(확정 권위·UAF-INV ⑤). 구조 게이트 해소 시 산출(impl-plan.json)을 먼저 검증하고, 통과 시에만 해소 이벤트 append + 구현 task 승격(task_added revision).
  `--gate-id`는 해소 대상 게이트를 지목한다. 같은 gateKind 게이트가 **2건 이상 동시에 pending**이면 지목이 필수다 — 무지목 호출은 후보를 열거하고 원장 무변경으로 비영 종료한다(binding §3.4). `render_gates.py`가 내는 게이트별 해소 명령에는 그 게이트의 `--gate-id`가 이미 채워져 있으므로 **복사해 그대로 실행**하면 된다.
- **재개:**
  ```
  python orchestration/adapters/claude/orchestrate_project.py <project_root> --resume --run-id <run_id> [--retry-limit N]
  ```
  엔진이 원장을 fold해 결정적으로 재개한다(이미 Passed 단위는 재실행 안 함). completed(exit 0)까지 정지→제시→해소→재개를 반복한다.
  - **함정(반드시 `--run-id`를 준다):** `--resume`은 기존 run_dir을 쓰는 명령인데도 런처는 `--run-id`가 없으면 슬러그를 `--phase`에서 **재파생**한다(`_resolve_slug(args.run_id, args.phase, root.name)`). 즉 구동 시 `--run-id`를 준 run을 `--run-id` 없이 재개하면 존재하지 않는 경로(`orch-<폴더명>-Phase-1`)를 보고 실패한다. run_id는 `logs/stop-signal.json`이 있는 run 디렉터리 이름이며, 부재 시 런처가 RUNS_DIR 실존 후보 목록을 오류 메시지에 함께 제시한다.

### 종료 코드 규약 (`orchestrate_project.py` — 정본 = 런처 exit 매핑·binding §5.3)

| 코드 | 의미 | 후속 |
|---|---|---|
| `exit 0` | 완료(completed) — 모든 단위 Passed | 없음 |
| `exit 2` | **정상 정지** — 게이트 미해소 또는 실행 에스컬레이션. `logs/stop-signal.json`에 `stop_reason`·`pending_gates` 기록 | 제시 → `resolve_gate.py` 해소 → `--resume` |
| `exit 3` | halted — 완료도 정지도 아님(진행 불가) | 원장·로그 조사 |
| `exit 1` | **런처 실패** — project_root 부재·`--resume` 대상 run_dir 부재 등. 미처리 예외도 비영 종료이며 `logs/failure.json`에 기록 | 메시지·`failure.json` 조사 후 재구동 |

`exit 2`를 실패로 읽지 않는다 — 정지 게이트는 설계상 정상 경로다(05 §3.3 불가침).

### run 관측 파일 (백로그 §L)

- `logs/heartbeat.json` — invoke 시작 전·종료 후 갱신(`ts`·`stage`·`invokes`·`request_hint`·`pid`). 프로세스가 매달려(hang) 종료 이벤트가 오지 않을 때 **정체 판정의 유일한 근거**(마지막 `ts`)다.
- `logs/failure.json` — 미처리 예외의 구조화 기록(`ts`·`run_id`·`argv`·`error_type`·`error`·`traceback`). 스택트레이스는 stderr에도 그대로 나온다(은폐 0).
- 두 기록은 실패해도 run을 중단시키지 않는다(관측 장치가 관측 대상을 죽이지 않는다).

### 형태 A 폴백 (런처 미가용 시)

런처가 가용하지 않으면 주 세션이 동일 규약을 실수행한다 — (a) `contract_to_graph.compile` 결과를 run_dir에 물리화, (b) `build_orchestrator_k`로 구동, (c) exit 2 시 pending_gates 표면화, (d) `resolve_gate.py` 상당의 해소(검증-먼저·적격 actor·원장 append), (e) 재개. 두 경로의 계약·게이트는 동일하다.

### 사용자 개입 지점 (Preserve Human Authority · 05 §2.1 확정 권위)

- **사용자 구조 게이트**(`user_decision_required`) — 초기 proposal(구현 계획) 방출 후 사용자가 계획을 확인·승인해야 구현 task가 그래프에 편입된다. 사용자만 해소한다.
- **CP2**(`review_required`) — 각 구현 단위의 독립 검증. 상시 하한이며 게이트로 우회되지 않는다(Verifier).
- **CP3**(`approval_required`) — Phase 경계 인수/완결 단위(milestone)에서 Advisor 승인. 비-Pass 시 `escalation_required` 정지로 승격된다.
- 확정 게이트는 하류에서 존중된다 — 엔진은 게이트를 원장 이벤트로 표기·강제할 뿐 확정 결정을 대체하지 않는다.

---

## §3. 정본 포인터 (재정의 0)

이 명령이 참조만 하고 재정의·확장하지 않는 정본이다. 충돌 시 정본이 우선하며, 발견되는 충돌은 Advisor에게 보고한다.

| 안내 항목 | 정본 (가리키기만 함) |
|---|---|
| Project Orchestrator 계약·3분해·초기 그래프=데이터 | `orchestration/specs/05-project-orchestration.md` §2.1·§3.1 (Frozen v1.6) |
| 4 레코드(RevisionEvent·GatePolicyEntry·AgentSpec·ArtifactRecord)·게이트 5종·불가침·단조성 | `orchestration/specs/05-project-orchestration.md` §3.2~§3.6·§3.3 |
| 게이트 5종 구현·자격·floor·pending_gates | `orchestration/framework/orchestrator/gates.py` |
| 게이트 큐 채널·해소 이벤트·actor 자격 | `orchestration/adapters/claude/project-orchestration-binding.md` §3 |
| run-data 백엔드 레이아웃(runs/<run-id>/) | `orchestration/adapters/claude/project-orchestration-binding.md` §5.3 |
| Contract vN → 초기 Work Graph 컴파일(결정적) | `orchestration/adapters/claude/contract_to_graph.py` |
| 프로덕션 런처(형태 B 발화·구동·exit 매핑) | `orchestration/adapters/claude/orchestrate_project.py` |
| 게이트 해소 브리지(검증-먼저·적격 actor·승격) | `orchestration/adapters/claude/resolve_gate.py` |
| Contract 저장 위치·직렬화 | `planning/adapters/claude/contract-binding.md` §3·§4 |
| Run 조율 vs 단위 실행 2층 규율(재발방지) | `.claude/AGENT.md` §Invariants "Run 조율 우회 금지" · `.claude/CLAUDE.md` "구현 단계 = 2층" |
| 진입 명령 골격 관례 | `.claude/commands/uaf-new.md` · `uahf-status.md` |
| 상위 규약 | `.claude/AGENT.md` |

이 명령 문서는 정본을 재정의하지 않는다.
