# orchestration/adapters/claude/project-orchestration-binding — Claude Project Orchestration Adapter 바인딩

작성일: 2026-07-13
상태: 05 계약(§3.3 Gate Policy·§3.5 Model Selection·§3.6 Artifact Record·§2.2 게이트 큐)의 claude 환경 물리 실현 매핑 — 게이트 큐 제시 채널(§3)·Model Selection 실값 매핑·OQ-SH-4 해소(§4)·직렬화·capability→물리 호출 매핑·run 데이터 백엔드·AgentSpec 실값 레지스트리·Artifact Record 직렬화(§5) 확정. 축소판 종단 dogfooding E2E(시나리오 j)로 실증.
상위 규약: AGENT.md
근거 정본:

- `orchestration/specs/05-project-orchestration.md` (S1 확정) — Project Orchestration provider-중립 계약 정본. 본 문서가 물리 실현으로 인스턴스화하는 대상. 특히 **§3.3 Gate Policy**(5종 어휘·기존 계약 매핑·게이트 단조성·Autonomy 직교)·§2.2(게이트 큐 = `Escalated` 이벤트 + gateKind + scoped question 의 파생 뷰·headless·사용자 채널 분리)·§5(Adapter 바인딩 지점 — 게이트 큐 제시 채널 행). 재정의하지 않고 § 포인터로만 인용한다.
- `orchestration/framework/orchestrator/gates.py` (S3 신설 — 중립 게이트 평가기) — 본 문서가 제시 채널을 붙이는 중립 코드. `pending_gates(events, policy)` 파생 뷰·게이트 이벤트 필드 관례(`gate::<gate_id>` cycle 네임스페이스·ref 의 gate_id/gateKind/target/scoped_question·`append_gate_requirement`/`append_gate_resolution`)·해소 적격성(`is_resolved`·user_decision=사용자 actor 클래스만·escalation=허용 resolver 집합)·`gate_policy_schema.json`. 본 문서는 그 추상을 claude 실값으로 바인딩한다.
- `orchestration/framework/orchestrator/orchestrator.py` (S2·S3) — `_process_gates`(배치 종단 단위 경계 게이트 처리)·`OrchestrationResult.pending_gates`(정지 게이트 큐 반환)·정지 신호(`stop_reason="gate"`). 본 문서 §3 이 그 정지·재개의 물리 채널을 확정한다.
- `uahf/specs/03-loop.md` §3.1-D(사람 개입 5조건 — 코드 소유 하한의 정본)·§3.2-A(전이 이벤트 10필드 — actor 필드) — 게이트 요구·해소 이벤트가 무수정 재사용하는 이벤트 스키마·개입 조건. § 포인터로만 참조(재정의 0).
- `uahf/framework/adapters/claude/step-hosting-binding.md` (v1.5 Baseline) — 자매 Adapter Binding. 문서 관례(§9 이력 머리·§0 정본 경계·격리 지점 방향 반전·형태 A/B 정직 구분·§ 근거 정본·실측 대조·L-07)의 선행 표본. 물리 정지 신호(종료 코드 2)·Autonomy→CLI 권한 플래그 매핑·run 데이터 백엔드 이원화는 이 문서가 이미 확정했고, 본 문서는 그 위에 게이트 큐 제시 채널을 얹는다.
- `uahf/framework/adapters/claude/loop-binding.md`·`verifier-binding.md` — 사람 개입 채널(03 §3.1-D 사람 승인 요청이 Claude Code 세션에서 사용자에게 제시된다)·역할 = 서브에이전트 디스패치 관례의 선행 표본.
- `uahf/framework/core/structure.md` §4·§5 — Adapter 경계 = 격리 지점(C-3 비적용·구체 토큰 허용)의 근거.

거버넌스: 이 문서는 `orchestration/adapters/claude/` 소속 **Adapter Binding 문서**다 — orchestration 레이어 자신의 Claude 어댑터 바인딩이며 `orchestration/specs/05-project-orchestration.md`(§3.3 등)와 `orchestration/framework/orchestrator/gates.py`를 바인딩한다. 이 경계는 중립 계약(05·gates.py)을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 AI·환경·직렬화 형식·물리 경로·실행 옵션 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용·자매 바인딩 §0 동형). 단 이 문서는 05·gates.py 의 계약을 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인으로 이뤄진다.

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 `orchestration/specs/05-project-orchestration.md`(§3.3)와 `orchestration/framework/orchestrator/gates.py`다.** 이 문서는 그 계약의 **claude 환경 실현 매핑**이며, 계약 요소(gateKind 5종·심각도 전순서·게이트 단조성·해소 적격성·게이트 이벤트 필드 관례)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터·심볼 참조로만 인용한다.
- 이 문서는 `orchestration/adapters/claude/` 소속 **Adapter Binding 문서**다. 05 §5 가 "게이트 큐 제시 채널·직렬화 형식·capability→물리 호출 매핑·run 데이터 백엔드 경로·정책 실값은 Adapter Binding 문서 소관"이라며 미룬 지점이 실재하는(확정되는) 자리다.
- **격리 지점의 방향 반전(C-3 비적용).** 중립 경계(`orchestration/framework/orchestrator/`·05 본문)는 특정 AI·provider·실행 옵션 토큰이 0건이어야 한다(PO-INV 8). 이 문서는 그 **반대편**이다 — 구체 토큰(`claude` CLI·세션 표면·종료 코드·물리 경로)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 바인딩 §0 동형).
- **범위 = 다섯 책임 전부 확정(S5).** 이 문서는 §3(게이트 큐 제시 채널)·§4(Model Selection 실값 매핑·OQ-SH-4 해소)에 더해 **§5(직렬화·capability→물리 호출 매핑·run 데이터 백엔드·AgentSpec 실값 레지스트리·Artifact Record 직렬화)를 확정**한다. §5 는 축소판 종단 dogfooding E2E(시나리오 j)로 **실 데이터 실증**되었다 — 데이터·물리 실현이 실재하며 그 실측 상태는 §6 이 정직하게 대조한다(L-07). 미실증분은 §7 OQ 로 남긴다.
- **창설 금지.** 이 문서는 05 §3.3·§5·gates.py 를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. 새 gateKind·새 상태·새 개입 조건·새 이벤트 필드를 만들지 않는다. 게이트 이벤트는 03 §3.2-A 10필드 무수정 재사용이다.
- 용어는 `uahf/specs/00-glossary.md` 정본만 사용한다. "게이트 큐"·"제시 채널"·"정지 게이트" 는 05·gates.py 의 서술 라벨이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적

이 문서는 05(§3.3 Gate Policy·§3.5 Model Selection·§3.6 Artifact Record·§2.2 게이트 큐)와 중립 코드(`gates.py`·`allocation.py`·`artifacts.py`·`orchestrator.py`)를 claude 환경 위에 **S5 시점의 구체 물리 실현**으로 매핑한다. **다섯 책임 전부 확정**한다:

- **확정(§3).** `pending_gates` 파생 뷰의 사용자 제시 채널 + 해소 응답의 이벤트 append 물리 관례.
- **확정(§4).** Model Selection 정책 실값(불투명 슬롯 → claude 모델 별칭) 매핑 관례 + CP2 독립 슬롯(`cp2ModelSlot`) → `--model` 전달 경로 + OQ-SH-4 해소 기록.
- **확정(§5).** 정책·이벤트·revision·**artifact 선언**·초기 그래프 직렬화 형식 · capability→물리 호출 매핑(step-invoker 무수정 재사용) · run 데이터 백엔드 경로 · AgentSpec 실값 레지스트리 관례 · **Artifact Record 직렬화·파생 인덱스**. 축소판 종단 dogfooding E2E(시나리오 j·§5.6)로 실 데이터 실증.

이 문서는 05·중립 코드의 어떤 계약 요소도 재정의·확장하지 않는다.

---

## §2. 상속·인용하는 확정분 (step-hosting-binding v1.5 Baseline)

게이트 축의 물리 채널은 자매 `step-hosting-binding.md` 가 이미 확정한 다음을 **상속·인용**한다(중복 확정 0):

| 항목 | 소재(정본) | 게이트 축에서의 의미 |
|---|---|---|
| 물리 정지 신호 = 프로세스 종료 코드 **2** | step-hosting-binding §5.3 | 정지 게이트(`escalation_required`/`user_decision_required`)로 `_process_gates` 가 `status="stopped"` 를 반환할 때, orchestration 런처는 종료 코드 2("사람/상위 개입 대기")로 종료한다. 게이트 정지도 Step Host 의 Escalated 정지와 같은 신호를 쓴다(신설 0). |
| Autonomy → CLI 권한 플래그 매핑(`interactive`/`auto_approve`=`--permission-mode acceptEdits`/`unrestricted`=`--dangerously-skip-permissions`) | step-hosting-binding §4.2 | **게이트 등급 분리(불가침).** 이 매핑은 도구 실행 승인 프롬프트 축만 제어하며 게이트 축과 **직교**한다(05 §3.3·PO-INV 4). `unrestricted` 에서도 5종 게이트는 전부 작동하고 정지 게이트는 `stopped` 정지로 보존된다 — orchestrator 의 게이트 **결정** 로직(gateKind 평가·must_stop·해소 적격성)은 `self.policy`(autonomy) 를 참조하지 않는다(서브단위 실행에는 동일 autonomy 전달만 — 중립 코드가 소유하는 강제). `--dangerously-skip-permissions` 는 claude 세션(도구 승인) 경계에만 적용되고 게이트 정지를 우회하지 못한다. |
| 이벤트 로그 = JSONL(1행 1이벤트·03 §3.2-A 10필드) | step-hosting-binding §3.1 | 게이트 요구·해소 이벤트도 같은 run 이벤트 로그에 append 된다 — 별도 백엔드 신설 0. `gate::<gate_id>` cycle 네임스페이스라 step 상태 파생에 간섭하지 않는다(gates.py `is_gate_event`). |
| 역할 = 서브에이전트/fresh 세션 디스패치(Worker/Verifier/Advisor) | step-hosting-binding §5.1·§5.2 | `review_required` 의 추가 리뷰(role=Verifier)·`approval_required` 의 CP3(role=Advisor)는 이 역할 디스패치 물리 형태를 그대로 쓴다(신설 0). |

---

## §3. 게이트 큐 제시 채널 (05 §2.2·§5 게이트 큐 제시 채널 행 — 본 판 확정)

### §3.1 게이트 큐의 정본 = 파생 뷰(제2 상태 아님)

- **제시 대상은 mutable 큐가 아니라 `pending_gates(events, policy)` 파생 뷰다.** 이 환경의 제시 채널은 별도의 큐 자료구조를 유지하지 않는다 — run 이벤트 로그(JSONL)를 접어(fold) 미해소 정지 게이트 목록을 그때그때 파생한다(PO-INV 2). 게이트가 이벤트로 영속하므로 orchestration 런처 크래시에도 게이트 상태가 보존된다(05 §2.2). 세션이 새로 떠도 같은 이벤트 로그 → 같은 큐(결정적·PO-INV 3).
- **큐 항목의 물리 형태.** `pending_gates` 각 항목 `{gate_id, gateKind, target, scoped_question, since}` 를 사용자에게 제시한다. `since` 는 이벤트 로그의 `at`(run 전역 append 순서)이며 물리 시각이 아니다(03 §3.2-A·L-09) — 제시 시 "요구가 걸린 순번"으로 표시한다.

### §3.2 사용자 제시 물리 채널 (Claude Code 세션 표면)

- **채널.** 게이트 큐는 `.claude/CLAUDE.md` 가 바인딩하는 사용자 대화 세션 표면(Claude Code 세션)에서 사용자에게 제시된다 — 03 §3.1-D 사람 승인 요청이 Claude Code 세션에서 제시된다는 자매 관례(loop-binding §4.1·03 §4 "사람 개입 채널")의 프로젝트 오케스트레이션 축 확장이다. **Orchestrator 는 headless 이므로**(05 §2.2) 이 제시는 orchestration 런처가 아니라 사용자 대화 주체(주 세션 Advisor)가 이벤트 로그를 읽어 표면화한다 — 사용자 채널과 orchestrator 는 분리된다.
- **제시 형식(구조 제안).** 각 미해소 항목을 다음 구조화 형태로 제시한다:
  - `gateKind` — `escalation_required` 는 "Advisor/사람 해소 대기", `user_decision_required` 는 "사용자 결정 대기(확정 권위)"로 라벨링한다(05 §3.3 매핑·UAF-INV ⑤).
  - `target` — 어느 단위·전이·artifact class 에 걸렸는가(descriptor).
  - `scoped_question` — 무엇을 결정/해소해야 하는가(gates.py 가 실은 구조화 힌트 `{unitId, gateKind}`; 사람 친화 문면 렌더는 이 제시 채널이 담당).
  - `since` — 요구 순번.
- **정확한 표면 문법·렌더 템플릿 — 확정(§DC-9·2026-07-19).** 최종 렌더 문법은 `orchestration/adapters/claude/render_gates.py`(형태 B·결정적·LLM 0·읽기 전용)가 소유한다. 위 구조 제안 bullet(라벨·`target`·`scoped_question`·`since`)은 확정분으로 유지되며, `render_gates.py`가 항목당 블록으로 물리화한다: 라벨 표(`user_decision_required`→"사용자 결정 대기(확정 권위)"·`escalation_required`→"Advisor/사람 해소 대기")는 **어댑터 소유 데이터**(모듈 상단 상수 dict)이며 **다국어·문면 조정은 이 표 교체가 확장점**이다(정책-as-데이터 동형·렌더 로직 본문 무변경). 진리원천은 `pending_gates(events, policy)` 파생 뷰이며 `stop-signal.json`에 의존하지 않고 원장(events.jsonl + gate_policy.json)에서 **직접 파생**한다 — 부분 해소 후 재렌더도 정확하다(해소 이벤트 append 시 파생 뷰가 자동 제외). 적격 해소 actor·해소 명령(`resolve_gate.py` CLI 1줄)은 정책 데이터에서 파생한다(하드코딩 0). 제시 겸용: 런처(`orchestrate_project.py run_and_map`)가 정지 게이트 시 기존 `[STOP]`/`[PENDING-GATES]` 라인·`stop-signal.json`을 바이트 보존한 뒤 이 렌더 함수를 재사용해 **자동 출력**하고(렌더 실패는 정지 신호를 깨지 않는 부가 표면), 주 세션 Advisor 는 `render_gates.py <run_dir>` 로 **수동 재렌더**할 수 있다. `--json` 은 구조화 출력(원 필드 + label + eligible_resolvers + resolve_command). **원장 무변경(읽기 전용)** — 어떤 파일도 쓰지 않는다.

### §3.3 해소 응답 → 게이트 해소 이벤트 append 물리 관례

- **해소는 이벤트 append 로만 이뤄진다.** 사용자·Advisor 의 해소 응답은 gates.py 의 `append_gate_resolution(log, gate_id, gateKind, actor=<해소자>)` 로 run 이벤트 로그에 append 된다(mutable 상태 갱신 0). 다음 재기동 시 `_process_gates` 가 그 해소 이벤트를 파생 판정(`is_resolved`)해 통과시킨다(결정적 재개).
- **actor 매핑(적격성의 물리 실현).** 해소 이벤트의 `actor` 필드가 적격성을 결정한다(gates.py `is_eligible_resolver`·정책 데이터 `userActorClass`/`escalationResolvers`). 이 환경의 매핑:

  | gateKind | 적격 해소 actor(이 환경) | 물리 관례 |
  |---|---|---|
  | `user_decision_required` | 사용자 본인의 응답 — actor = 정책 `userActorClass`(기본 `human`, 03 §3.2-A actor 어휘) | 사용자가 Claude Code 세션에서 결정을 내리면 그 응답을 actor=`human` 해소 이벤트로 append. **Advisor 역할·서브에이전트의 해소 시도는 무효**(gates.py 가 파생 뷰에 여전히 pending 으로 남김 — 확정 권위 보존·UAF-INV ⑤). |
  | `escalation_required` | actor ∈ 정책 `escalationResolvers`(기본 `Advisor`·`human`) | Advisor 역할(주 세션) 또는 사용자가 해소. actor=`Advisor` 또는 `human` 해소 이벤트로 append. |

- **부적격 해소의 물리 무효.** 부적격 actor 로 append 된 해소 이벤트도 로그에 남지만(append-only·은폐 0), `is_resolved` 가 적격성 판정에서 배제하므로 게이트는 여전히 pending 이다. 이는 코드가 소유하는 강제이며 제시 채널이 우회할 수 없다.
- **해소 어휘의 현행 한계(인용).** 전용 해소 이벤트 어휘의 성숙(재시도 예산 비계수 등)은 OQ-SH-5(step-hosting-binding §7)와 05 §9 OQ 3 의 이월 사안이다. 본 판은 `append_gate_resolution`(03 10필드 재사용·`ref.kind=gate-resolved`·outcome=pass) 의 현행 물리 형태만 바인딩한다.

---

## §4. Model Selection 실값 매핑 관례·OQ-SH-4 해소 (05 §3.5·§5 모델 정책 실값 행 — 본 판 확정)

### §4.1 불투명 슬롯 → claude 모델 별칭 매핑 관례 (격리 지점 — 구체 토큰 허용)

- **정본은 중립이다.** `orchestration/framework/orchestrator/allocation.py`·`model_selection_schema.json`·`gates.py`(CP3 status 소비)는 provider·모델 고유명 토큰이 0건이어야 한다(PO-INV 8·전수 스캔). 모델 슬롯은 **불투명 문자열**(예: `tier-a`)이며 중립 코드는 그 의미를 해석하지 않는다(05 §3.5·PO-INV 6). 이 문서는 그 **반대편**(격리 지점)이며 구체 토큰(`claude` CLI·`--model`·모델 별칭)의 사용이 허용된다.
- **매핑 관례.** Model Selection 정책 데이터(`model_selection_schema.json` 형태)의 불투명 슬롯 값은 이 환경에서 claude CLI `--model <alias|full>`(step-hosting-binding §5.1·§4 CLI 실측)의 별칭으로 매핑된다. 매핑은 **정책 데이터**(Policy as Data·05 §3.5)이며 엔진·계약 무변경으로 조정된다. 예시 매핑(비강제·프로젝트 정책 데이터 소관):

  | 불투명 슬롯(중립 정책) | claude 모델 별칭(이 환경 실값) | capability class 예 |
  |---|---|---|
  | 약 티어 | `haiku` | 기계적(mechanical) |
  | 중 티어 | `sonnet` | 통합(integration) |
  | 강 티어 | `opus` | 설계·최종 리뷰(design) |

  실제 정책 데이터의 `slots`(class→슬롯)·`fallbackChain`(약→강)·`cp2ModelSlot` 실값은 이 별칭 집합으로 채워진다. 값의 의미(모델 지정)는 02 §4 소관이며 invoker 는 `--model <slot>` 전달만 한다(step-hosting-binding §5.1·프로토콜 §3.1). 슬롯이 없으면 세션 기본 모델을 상속한다.
- **hysteresis·재선택은 중립 코드 소유.** 모델 선택 1회 고정과 재선택 트리거 2건 한정(retry 한도 도달·명시적 모델 정책 이벤트)은 orchestrator 가 이벤트 로그에서 결정적으로 소유한다(05 §3.5·`allocation.RESELECTION_TRIGGER_KINDS`). 이 Adapter 는 슬롯→별칭 매핑만 담당하고 재선택 정책을 재정의하지 않는다.

### §4.2 CP2 Verifier 모델 독립 지정 → `--model` 전달 (OQ-SH-4 해소 경로)

- **독립 슬롯의 물리 전달.** Model Selection 정책의 `cp2ModelSlot`(있으면)은 orchestrator 가 `StepHost(cp2_model=...)`로 전달하고, Step Host `_dispatch_cp2` 가 CP2 검증 단위 invoke 요청의 `model` 슬롯으로 실어 이 환경 invoker 가 `--model <cp2 별칭>` 으로 전달한다. 이로써 CP2(Verifier)는 피검증 단위와 **동일 모델에 묶이지 않는다**(예: Worker=`haiku`여도 CP2=`sonnet` 독립 지정 가능). `cp2ModelSlot` 미지정 시 CP2 는 대상 step 슬롯을 상속한다(기존 거동 — W3 e2e-s6 은 Worker=`sonnet`이라 CP2 도 `sonnet`이었다).

### §4.3 OQ-SH-4 해소 기록 (step-hosting-binding §7 OQ-SH-4)

- **OQ-SH-4 — 해소됨 (본 트랙 S4, 2026-07-13).** step-hosting-binding §7 OQ-SH-4(중립 Host `host.py _dispatch_cp2` 가 CP2 를 `model=step.model` 로 디스패치해 검증 전용 모델 독립 지정 불가)는 본 트랙 S4 에서 **중립 Host 최소 개정으로 해소**되었다. 개정 = `StepHost` 생성자에 `cp2_model` 파라미터 추가(기본 `None`)·`_dispatch_cp2` 의 CP2 모델을 `self.cp2_model if self.cp2_model is not None else step.model` 로 변경(1개소). **기본값 `None` 시 기존 거동(model=step.model) 바이트 동일 보존** — 기존 step-host 회귀 전건 무손상. `config_schema.json` 에 선택 필드 `cp2_model`(불투명 슬롯·형태만) 추가. 계약 무변(02 §4 슬롯 의미 그대로)·중립 Host 는 슬롯 값을 해석하지 않는다(SH-INV-8 동형).
- **정본 문면 갱신 위치.** step-hosting-binding §7 OQ-SH-4 문면 자체의 상태 갱신은 **트랙 종단 정합 소관**이며 본 문서가 대신 갱신하지 않는다(무수정 경계 — 05 §6). 해소 사실은 이 § 이 기록한다.
- **`uahf/` 트리 접촉(본 트랙).** `uahf/framework/loop/step-host/host.py` `_dispatch_cp2` 1개소(+`config_schema.json`·step-host 테스트) — OQ-SH-4 해소. 그 외 `uahf/` 정본·중립 코드·append-only 데이터 무촉(형상 관리 상태 조회로 확인·§6 실측 대조).

---

## §5. 직렬화·capability 호출 매핑·run 데이터 백엔드·AgentSpec·Artifact Record (05 §5·§3.6 — 본 판 확정)

이 절은 05 §5 가 "직렬화 형식·capability→물리 호출 매핑·run 데이터 백엔드 경로·정책 실값·Artifact Record"로 미룬 지점을 이 환경 위에 확정한다. 축소판 종단 dogfooding E2E(§5.6·시나리오 j)로 실 데이터 실증되었다.

### §5.1 직렬화 형식 — append-only JSONL 이중 원장 + 선언 원장 + 정책 JSON

- **이벤트 로그 = `events.jsonl`**(1행 1이벤트·03 §3.2-A 10필드·`events.py JsonlEventStore`). step 이벤트와 게이트 이벤트가 같은 로그에 동거하되 `gate::<gate_id>` cycle 네임스페이스로 step 상태 파생과 무간섭(§2·gates.py `is_gate_event`).
- **revision 원장 = `revisions.jsonl`**(1행 1 RevisionEvent·`revision.py JsonlRevisionStore`·`revision_schema.json` 형태). 현재 그래프는 mutable 저장이 아니라 fold 파생 뷰다(PO-INV 2).
- **artifact 선언 원장 = `artifacts.jsonl`**(1행 1선언·`artifacts.py JsonlArtifactDeclarationStore`). 완료 보고 artifacts 에서 append-only 포집된 산출물 선언이며, 레지스트리는 이 선언과 이벤트에서 **파생**될 뿐 저장되지 않는다(§5.5·제2 진리원천 아님).
- **초기 그래프 = `graph.json`**(full Task dict — 게이트 descriptor 용 `unitType` 등 개방 필드 보존·07 개방 데이터). **정책 데이터 = `gate_policy.json`**(GatePolicy)·(선택) allocation/model-selection JSON. **단위 뷰 = `steps/<id>.json`**(참조용 직렬화 미러). 형식은 전부 JSON/JSONL 이며 중립 코드(`orchestration/`)에는 형식 토큰 0(격리 지점 반전).

### §5.2 capability → 물리 호출 매핑 (step-invoker 무수정 재사용·역할 디스패치)

- **실행 주체 = fresh 세션(claude CLI headless)**. Orchestrator 가 직렬화한 단위는 중립 Step Host 를 통해 `step-invoker/claude_invoker.py`(`ClaudeInvoker`·무수정)로 디스패치된다. capability 슬롯은 매칭 입력이고(§5.4), 물리 호출은 role 슬롯이 주도한다 — Worker(실행)·Verifier(CP2·`review_required` 추가 리뷰)·Advisor(`approval_required` CP3)는 전부 `--append-system-prompt` 역할 브리프로 fresh 세션에 실린다(step-hosting-binding §5.1·§5.2 동형·신설 0). 게이트 리뷰/승인 단위도 같은 디스패치 경로를 쓴다(orchestrator `_dispatch_gate_step`).
- **산출물 포집 = 투명 래퍼.** Orchestrator 가 실행 invoker 를 `ArtifactCapturingInvoker`(중립·투명)로 감싸 Worker 완료 보고의 artifacts 를 선언 원장에 포집한다. 래퍼는 반환을 변경하지 않으며(재정의 0) CP2/CP3 verdict 반환은 포집하지 않는다.

### §5.3 run 데이터 백엔드 = `uahf/framework/adapters/claude/orchestration-data/runs/<run-id>/` (물리 위치는 2차 산출물 디커플링 트랙에서 확정)

discovery-data·solution-design-data·step-data 선례 동거. 구조:

```
orchestration-data/runs/<run-id>/
  config.json        run 파라미터·메타(policy·retry_limit·timeout·allowed_tools·run_id)
  graph.json         초기 그래프(full Task dict)
  gate_policy.json   Gate Policy 데이터
  events.jsonl       step + 게이트 이벤트 로그(append-only)
  revisions.jsonl    Graph Revision 원장(append-only)
  artifacts.jsonl    산출물 선언 원장(append-only)
  steps/<id>.json    단위 직렬화 뷰(참조)
  workspace/         호스팅 세션 산출(단위 산출물·물리 파일)
  logs/              invoke 캡처·stop-signal·gate-resolution-record
```

E2E 드라이버(`orchestration-data/e2e/`)는 **비프로덕션** dogfooding 도구다(step-data/e2e 선례 동형). 물리 정지 신호 = 종료 코드 2(§2·바인딩 §5.3 상속).

### §5.4 AgentSpec 실값 레지스트리 관례 (PO-INV 6 — 코어는 capability 선언까지만)

- AgentSpec 레지스트리(`allocation_schema.json` 형태)의 실값은 이 환경에서 데이터로 채워진다 — `capabilitySelector`(capability 매칭)·`modelPolicyClass`(불투명 정책 키→§4.1 별칭). 중립 코드는 capability 선언까지만 소비하고 어느 실행 주체가 호스팅하는가(물리 매핑)는 해석하지 않는다(PO-INV 6). 시나리오 j 는 role/model 슬롯을 단위에 직접 실어(격리 지점 허용) allocation 층 없이도 실행되며, AgentSpec 레지스트리는 capability→모델 슬롯 정책이 필요한 프로젝트에서 데이터로 채워진다.

### §5.5 Artifact Record 직렬화 + 파생 인덱스 (05 §3.6 — 본 판 확정)

- **선언(포집) → 파생 레지스트리.** 완료 보고 artifacts(경로 문자열 또는 구조화 선언)는 `normalize_declaration` 으로 표준 선언(artifactId·version·supersedes·derivedFrom·producedBy·location·contentHash)으로 정규화되어 `artifacts.jsonl` 에 append 된다. `derive_registry(선언, 이벤트)` 가 `{artifactId: [ArtifactRecord]}` 를 **매 호출 새로 파생**한다(mutable 저장 0).
- **approvalState = 게이트/검증 이벤트 파생 뷰(PO-INV 7).** draft → verified(대상 step 의 CP2 Pass 이벤트) → approved(CP3 승인 마커 Pass) → user_approved(user_decision 게이트가 적격 사용자 actor 로 해소). 각 등급은 대응 이벤트 실재에서만 파생되며 직접 쓰이지 않는다(`artifact_record_schema.json` enum = 코드 사다리).
- **번들 확정 참조 = 요구 등급 이상 최신 버전만.** `resolve_references(required_grade)` 는 요구 등급 이상 approvalState 의 최신 version 만 해석한다 — 미완성·미승인 산출물은 추측·인용 0(05 §3.6·07 R2). 계보(구버전·등급 미달)는 배제하지 않고 resolve 만 제외한다(문면 불변 보존).

### §5.6 축소판 종단 dogfooding E2E (시나리오 j — 실 CLI 실증)

`orchestration-data/e2e/` 드라이버가 실 claude CLI headless(haiku·**5 세션**)로 종단 흐름을 실증했다(run 데이터 = `runs/orch-j-e2e/@cd9247b` — 산출물 수명 정책에 따라 아카이브, ARCHIVE.md 원장):

- 초기 그래프 = 설계 단위 d1(user_decision 게이트) → d1 실행(Worker+CP2)·Passed → **user_decision 게이트 물리 정지(exit 2·pending_gates 기록)**(j1).
- 드라이버가 **시뮬레이션 라벨을 append-only 로그(`annotation::sim`)와 `gate-resolution-record.json` 에 명시 기록**한 뒤 사용자 actor(`human`) 해소 이벤트 append(j2 — L-07 실 사용자 위장 금지)·구현 단위 revision(basis.gateEventRef = 해소 게이트) append.
- 재개(fresh 프로세스): 구현 단위 impl 실행(Worker+CP2)·`review_required` 추가 리뷰(Verifier)·완주(exit 0). 이벤트 로그 cycle = {d1·impl·gate::·annotation::sim}뿐 — **상류 Discovery/성숙 재실행 흔적 0**(입력 Contract 는 읽기 전용 참조).
- **deterministic resume replay**: `replay_check.py` 2회 실행 stdout 동일(active_graph·states·ready_set·graph_fingerprint). 최종 레지스트리: `design-decision.md` v1 = **user_approved**(사용자 게이트 해소)·`impl-note.txt` v1 = **verified**(derivedFrom `[design-decision.md]`).
- **실 CLI 실패 은폐 0(O5).** 실 세션 stdout·argv·session_id 는 `logs/invoke-*.json` 에 그대로 캡처된다.

### §5.7 프로덕션 실 run — tms-system Contract v2 (배선 수정 트랙·2026-07-18)

§5.6 시나리오 j 가 비프로덕션 e2e 드라이버(시뮬 사용자 게이트·픽스처 구현 제안)였던 것과 달리, **프로덕션 런처**가 임의 소비 프로젝트를 실 claude CLI headless 로 구동한 첫 실 run 이다. 신설 어댑터 3종(전부 `orchestration/adapters/claude/`·중립 `orchestration/framework/`·`uahf/` 무수정 import 재사용):

- **`contract_to_graph.py`** — Contract vN(파일명 버전 최대·내용 파싱 0) → 초기 Work Graph(단일 seed proposal 단위) + gate_policy(proposal→user_decision·implementation→review·milestone→approval) + config 결정적 컴파일. seed 프롬프트가 런타임 실 LLM 에 Phase 분해(implementation N + milestone 1·DAG 종단·오프라인 안전 done AC)를 위임(05 §3.1 "고정 파이프라인 하드코딩 금지").
- **`orchestrate_project.py`** — `<project_root>`를 컴파일→run_dir 물리화(소비 프로젝트 워크스페이스 무삭제·RUNS_DIR 직속 삭제가드)→중립 `build_orchestrator_k` 무수정 재사용→`orch.run()`→exit-code 매핑(§2 종료 코드 2 상속). `--model`(seed 티어)·`--policy`(기본 `auto_approve` — headless 쓰기·게이트와 직교) override.
- **`resolve_gate.py`** — 게이트 해소: impl-plan 어댑터 검증(F4 계약 수용 = `unitType∈{implementation,milestone}`·milestone≥1·implementation≥1·milestone DAG 종단·`resolve_w` 구조 헬퍼 동일 강도 재사용) **먼저**(실패 시 원장 무변경) → `append_gate_resolution(actor=…)` → 각 구현 task `accept_revision(task_added·basis.gateEventRef)`.

**tms-system(pc-tms-001 v2) 실 run 실측(run 데이터 = `runs/orch-tms-phase1-smoke/` — tms 트랙 종료로 앵커 전환 `4934bc8`·ARCHIVE.md·2026-07-19):**

- Stage A: seed proposal 단위(실 LLM·`haiku`)가 Contract v2 + solution-design 정독 후 `impl-plan.json`(6 task = implementation 5 + milestone 1·DAG 종단) 산출 → CP2(`cp2-pass` 이벤트·상시 하한) → **`user_decision_required` 게이트 물리 정지(exit 2·`logs/stop-signal.json` pending_gates 기록)**.
- 게이트 해소: `resolve_gate.py` 가 impl-plan 어댑터 검증 통과 후 **실 사용자(actor=`human`·simulated=false)** 해소 이벤트 append → 6 `task_added` revision(basis.proposingStepRef=impl-plan-phase1·gateEventRef=해소 게이트) 승격. events.jsonl 5(dispatch·cp2-pass·gate-required·resolution-provenance·gate-resolved)·revisions.jsonl 6·artifacts.jsonl 1·active_graph 7노드(fold)·ready_set=선행 impl 단위(결정적 재개 준비).
- **정직 대조(L-07).** 이 run 은 §5.6 픽스처를 넘어선 **실 LLM 제안 step + 실 사용자 게이트 해소**다(OQ-PO-B4). milestone 단위(→`approval_required`·CP3)의 물리 CP3 정지·해소는 구현 단위 resume 시 발화하며, 본 run 에서는 gate_policy 파생 평가로 도달성만 실증했다(라이브 CP3 발화·실 코드 산출 = 후속 resume 소관·사용자 선택 defer). e2e 드라이버(§5.3)는 여전히 비프로덕션이며, 이 프로덕션 런처가 그 상위 발화 경로다.

---

## §6. 실측 대조 (L-07)

- **중립 코드 실재 (S5).** S5 는 `orchestration/framework/orchestrator/artifacts.py`·`artifact_record_schema.json`·`tests/test_artifacts.py` 를 신설하고, `orchestrator.py`(선택 `artifact_store`·투명 포집 래퍼 배선·`artifact_registry()`/`resolve_references()` 파생 메서드)를 최소 개정했다(`artifact_store=None` 기본 시 S2~S4 거동 바이트 동일 보존). 자체 테스트는 표준 라이브러리 `unittest` 만으로 통과한다 — **orchestration 126건(신규 32 + S2~S4 회귀 94)·step-host 20건·step-invoker 19건 = 전건 Pass**(실행 출력 실측).
- **PO-INV 8(중립성) 실측.** `orchestration/framework/orchestrator/`(artifacts.py 포함 전 `.py`·전 `.json`·테스트)에 provider·모델·CLI 옵션 토큰 0건(전수 스캔). approvalState 어휘(draft/verified/approved/user_approved)·verdict `Pass` 는 05 §3.6·06 계약 어휘다. 구체 토큰(`claude`·모델 별칭 `haiku`/`sonnet`/`opus`·`--model`·권한 플래그)은 이 바인딩 문서·step-invoker 코드·`orchestration-data/e2e/` 드라이버(격리 지점)에만 존재한다.
- **축소판 종단 E2E 실측 (시나리오 j).** `orchestration-data/e2e/`(비프로덕션 드라이버) 실 claude CLI headless **5 세션**(haiku)로 종단 흐름 실증 — Phase 1(exit 2 게이트 정지·2 세션)·Phase 2(exit 0 완주·3 세션). run 데이터 = `runs/orch-j-e2e/@cd9247b`(events.jsonl 8 이벤트·revisions.jsonl 1·artifacts.jsonl 2·워크스페이스 실 산출 2 — 아카이브 보존, 열람 `git show`/ARCHIVE.md). 상류 재실행 흔적 0·replay 2회 동일·최종 레지스트리 approvalState 파생(user_approved/verified) 실측. 실 세션 stdout·argv 는 `logs/invoke-*.json` 에 캡처(은폐 0·O5).
- **`uahf/` 접촉 실측(본 트랙 누계).** (i) `uahf/framework/loop/step-host/host.py` `_dispatch_cp2` 1개소(S4·**S5 무촉**·`cp2_model=None` 시 기존 거동). (ii) `uahf/framework/adapters/claude/orchestration-data/` **신설**(run 데이터 백엔드·E2E 드라이버 — 2차 산출물 디커플링 트랙까지 `uahf/` 잔류). 그 외 `uahf/` 정본·중립 코드·append-only 데이터(discovery-data·solution-design-data·step-data·memory-data·loop-data) 무촉(형상 관리 상태 조회로 확인·git 실측).
- **정직 구분 (L-07).** 시나리오 j 의 사용자 게이트 해소·구현 단위 제안은 **드라이버 픽스처**이며 실 사용자·실 LLM 제안 step 이 아니다(§5.6·`gate-resolution-record.json`·`annotation::sim` 이벤트에 명시). 실증 대상은 게이트 물리 정지·사용자 actor 적격성·revision 인과 사슬·deterministic 재개이며 그 축들은 실 데이터로 남는다. 산출 내용은 CP2 재현성을 위해 정확 내용으로 고정한 픽스처다(설계 메모를 exact-content 설계 결정 레코드로 축약).

---

## §7. Open Questions (본 판 이월)

- **OQ-PO-B1 (게이트 큐 제시 표면 문법) — 해소(2026-07-19·§DC-9).** 물리 형태 확정: `orchestration/adapters/claude/render_gates.py`(형태 B·결정적·LLM 0·읽기 전용)가 `pending_gates` 파생 뷰를 사람 친화 한국어 마크다운(기본)·`--json`(구조화)으로 렌더한다. 라벨 표는 어댑터 소유 데이터(다국어 = 표 교체 확장점)이며, 진리원천은 원장 직접 파생(stop-signal 비의존)이라 부분 해소 후 재렌더도 정확하다. 런처(`orchestrate_project.py`)가 정지 시 기존 라인·`stop-signal.json` 바이트 보존 후 자동 출력하고(부가 표면·렌더 실패는 정지 신호 불변), 주 세션 Advisor 수동 재렌더 겸용. 상세 = §3.2.
- **OQ-PO-B2 (해소 어휘 성숙).** 전용 해소 이벤트 어휘(재시도 예산 비계수·해소 취소)는 OQ-SH-5·05 §9 OQ 3 이월. 본 판은 `append_gate_resolution` 현행 형태만 바인딩.
- **OQ-PO-B3 (headless 런처 ↔ 사용자 세션 제시 브리지) — 해소(production·2026-07-18).** 물리 브리지 형태 확정: 프로덕션 런처(`orchestrate_project.py`)가 정지 게이트 시 **종료 코드 2 + `logs/stop-signal.json`(pending_gates)** 를 기록 → 주 세션 Advisor 가 그 파일을 읽어 게이트 큐를 사용자 대화 세션에 표면화(§3.2 headless·채널 분리 유지) → 사용자/Advisor 해소를 `resolve_gate.py <run_dir> --gate-kind … --actor …` 로 게이트-해소 이벤트 append(적격성 = gates.py `is_eligible_resolver` 코드 소유) → `orchestrate_project.py --resume` 로 결정적 재개(원장 fold). §5.7 tms-system 실 run 으로 실증. (사람 친화 렌더 최종 문법 = OQ-PO-B1 이월.)
- **OQ-PO-B4 (실 LLM 제안 step·비픽스처 성숙 run) — 해소(제안·승격 사이클·production·2026-07-18).** §5.7 tms-system 실 run 에서 확정 설계(Contract v2·solution-design)를 **실 LLM(haiku) 제안 step** 이 소비해 구현 task 6개(implementation 5 + milestone 1)를 제안하고, **실 사용자 게이트 해소**(actor=human·simulated=false)로 revision 승격했다 — 드라이버 픽스처(§5.6 j)가 아닌 실 LLM 제안 + 실 사용자 해소. 잔여(후속 트랙): 승격된 구현 단위의 **resume 실 코드 산출**(형태 A 완전 성숙 run·BPD-20 동형)은 사용자 선택으로 후속 세션 defer — 제안·게이트·승격 사이클은 본 run 으로 실증됐고 코드 산출 축만 이월된다.
- **OQ-PO-B5 (엔진 `accept_revision` 게이트-pass 재검증의 actor 미검사) — 해소(2026-07-19·§DC-9).** `orchestrator._gate_event_exists`(→ `_event_grounds_gate`)를 강화해 방어적 이중화의 **엔진 측을 완성**했다. 강화 규칙: 매칭 pass 이벤트가 **정지 게이트 해소로 자신을 선언**하고(`ref.kind == REF_KIND_RESOLVED` **그리고** `ref.gateKind ∈ STOPPING_GATES`) `self.gate_policy is not None`이면, 그 해소 actor 가 `gate_policy.is_eligible_resolver(gateKind, actor)` 로 적격일 때만 revision 을 근거지을 수 있다(05 §3.3 확정 권위 정합 — user_decision = 사용자 actor 클래스만·escalation = 허용 resolver 집합만). 부적격 actor 의 pass 해소 이벤트는 로그에 남아도 승격 근거가 되지 못한다. **거동 보존 3면(불가침):** (a) 레거시 이벤트(`ref.kind == "gate"`·gateKind 부재·S2 관례) = 실재-만 검증 유지 · (b) 비정지 gateKind(`review_required`/`approval_required` 등) gate-resolved 이벤트 = 실재-만 검증 유지(`is_eligible_resolver` 는 비정지에 False 라 일괄 적용 시 rework 근거 패턴이 깨진다 — 적용 범위를 `STOPPING_GATES` 로 한정하는 이유) · (c) `gate_policy is None`(S2 조립) = 실재-만 검증. **적용 시점:** `_gate_event_exists` 는 `accept_revision`(수용)과 `_grounded_revisions`(재개 fold 필터) 양쪽에서 쓰이므로 이 강화는 **수용 시점과 재개(fold) 시점 모두**에 걸린다. 프로덕션 resolver(`resolve_gate.py`)의 상류 append 거부(독성 pass 이벤트 미생성)와 함께 이중 방어를 이룬다. `orchestration/framework/**` provider·모델 토큰 0(PO-INV 8·`STOPPING_GATES`·`REF_KIND_RESOLVED` 중립 어휘만 가법 import).

---

## §8. 개정 이력

- **2026-07-19 (§DC-9 05 wiring 후속 — OQ-PO-B5·OQ-PO-B1 해소).** OQ-PO-B5 해소: 엔진 `orchestrator._gate_event_exists`(→ `_event_grounds_gate`) 강화 — 정지 게이트 해소 선언(`ref.kind==gate-resolved`·`gateKind∈STOPPING_GATES`)+`gate_policy` 존재 시 `is_eligible_resolver` actor 자격까지 요구(수용+fold 양시점). 거동 보존 3면(레거시 `ref.kind="gate"`·비정지 gateKind·`gate_policy None`) = 실재-만 검증 유지. OQ-PO-B1 해소: `render_gates.py` 신설(형태 B·결정적·LLM 0·읽기 전용 게이트 큐 렌더러·라벨 표 = 어댑터 소유 데이터) + `orchestrate_project.py run_and_map` 배선(기존 `[STOP]`/`[PENDING-GATES]`·`stop-signal.json` 바이트 보존 후 렌더 가법·방어). §3.2 확정 갱신·§7 OQ-PO-B1·B5 해소 갱신(B2~B4 무변경). 신규 테스트: `test_render_gates.py`·`test_orchestrator.py` OQ-PO-B5 6케이스·`test_orchestrate_project.py` 렌더 회귀 1건. **05 계약 본문·gates.py 어휘·§3 게이트 어휘·PO-INV·Frozen 무접촉(재정의 0)·`orchestration/framework/**` provider 토큰 0.**
- **2026-07-18 (오케스트레이션 → 실 프로젝트 배선 수정 트랙).** 코드화된 오케스트레이터 엔진이 실 소비 프로젝트를 정석 구동하도록 배선. 신설(전부 `orchestration/adapters/claude/`·중립 `orchestration/framework/`·`uahf/` 무수정 import): `contract_to_graph.py`(Contract→초기 그래프 컴파일러)·`orchestrate_project.py`(프로덕션 런처)·`resolve_gate.py`(게이트 브리지 resolver). §5.7 신설(tms-system Contract v2 실 run). §7 OQ-PO-B3 해소(브리지 물리 형태 = exit2+stop-signal→표면화→resolve_gate append→resume)·OQ-PO-B4 해소(제안·승격 사이클·production·구현 resume defer)·OQ-PO-B5 신설. 공동 도입: 상위 규약 F2(구현 = Run 조율/단위 실행 2층 구분·`.claude/CLAUDE.md`·`.claude/AGENT.md`)·F1 물리 발화(`/uaf-implement` = `.claude/commands/uaf-implement.md`). Advisor 승인 + 사용자 게이트(smoke 실증 후 기록). **05 계약 본문·gates.py·§3 게이트 어휘·기존 §행·PO-INV 무변(재정의 0)·Frozen 무접촉.**
