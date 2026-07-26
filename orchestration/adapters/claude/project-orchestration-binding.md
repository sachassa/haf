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
- **정확한 표면 문법·렌더 템플릿 — 확정(§DC-9·2026-07-19).** 최종 렌더 문법은 `orchestration/adapters/claude/render_gates.py`(형태 B·결정적·LLM 0·읽기 전용)가 소유한다. 위 구조 제안 bullet(라벨·`target`·`scoped_question`·`since`)은 확정분으로 유지되며, `render_gates.py`가 항목당 블록으로 물리화한다: 라벨 표(`user_decision_required`→"사용자 결정 대기(확정 권위)"·`escalation_required`→"Advisor/사람 해소 대기")는 **어댑터 소유 데이터**(모듈 상단 상수 dict)이며 **다국어·문면 조정은 이 표 교체가 확장점**이다(정책-as-데이터 동형·렌더 로직 본문 무변경). 진리원천은 `pending_gates(events, policy)` 파생 뷰이며 `stop-signal.json`에 의존하지 않고 원장(events.jsonl + gate_policy.json)에서 **직접 파생**한다 — 부분 해소 후 재렌더도 정확하다(해소 이벤트 append 시 파생 뷰가 자동 제외). 적격 해소 actor·해소 명령(`resolve_gate.py` CLI 1줄)은 정책 데이터에서 파생한다(하드코딩 0). **항목별 해소 명령에는 그 게이트의 `--gate-id <gate_id>`가 채워진다(2026-07-26)** — 같은 gateKind 가 다중 pending 이면 무지목 호출이 차단되므로(§3.4), 지목을 항상 실어 렌더 명령이 단일·다중 어느 상황에서도 **복사해 그대로 실행**되게 한다. 값이 셸 안전 문자 집합을 벗어나면 큰따옴표로 인용한다(결정적 규칙). 제시 겸용: 런처(`orchestrate_project.py run_and_map`)가 정지 게이트 시 기존 `[STOP]`/`[PENDING-GATES]` 라인·`stop-signal.json`을 바이트 보존한 뒤 이 렌더 함수를 재사용해 **자동 출력**하고(렌더 실패는 정지 신호를 깨지 않는 부가 표면), 주 세션 Advisor 는 `render_gates.py <run_dir>` 로 **수동 재렌더**할 수 있다. `--json` 은 구조화 출력(원 필드 + label + eligible_resolvers + resolve_command). **원장 무변경(읽기 전용)** — 어떤 파일도 쓰지 않는다.

### §3.3 해소 응답 → 게이트 해소 이벤트 append 물리 관례

- **해소는 이벤트 append 로만 이뤄진다.** 사용자·Advisor 의 해소 응답은 gates.py 의 `append_gate_resolution(log, gate_id, gateKind, actor=<해소자>)` 로 run 이벤트 로그에 append 된다(mutable 상태 갱신 0). 다음 재기동 시 `_process_gates` 가 그 해소 이벤트를 파생 판정(`is_resolved`)해 통과시킨다(결정적 재개).
- **actor 매핑(적격성의 물리 실현).** 해소 이벤트의 `actor` 필드가 적격성을 결정한다(gates.py `is_eligible_resolver`·정책 데이터 `userActorClass`/`escalationResolvers`). 이 환경의 매핑:

  | gateKind | 적격 해소 actor(이 환경) | 물리 관례 |
  |---|---|---|
  | `user_decision_required` | 사용자 본인의 응답 — actor = 정책 `userActorClass`(기본 `human`, 03 §3.2-A actor 어휘) | 사용자가 Claude Code 세션에서 결정을 내리면 그 응답을 actor=`human` 해소 이벤트로 append. **Advisor 역할·서브에이전트의 해소 시도는 무효**(gates.py 가 파생 뷰에 여전히 pending 으로 남김 — 확정 권위 보존·UAF-INV ⑤). |
  | `escalation_required` | actor ∈ 정책 `escalationResolvers`(기본 `Advisor`·`human`) | Advisor 역할(주 세션) 또는 사용자가 해소. actor=`Advisor` 또는 `human` 해소 이벤트로 append. |

- **부적격 해소의 물리 무효.** 부적격 actor 로 append 된 해소 이벤트도 로그에 남지만(append-only·은폐 0), `is_resolved` 가 적격성 판정에서 배제하므로 게이트는 여전히 pending 이다. 이는 코드가 소유하는 강제이며 제시 채널이 우회할 수 없다.
- **조건부 승인의 하류 전달 — `--response` 는 기록 전용이 아니다(백로그 §N·2026-07-26).** 사용자가 게이트를 "조건부"로 승인하면(예: "로그 마스킹 적용 후 진행"), 그 조건은 원장에만 남고 실행 단위에는 닿지 않았다 — 조건이 승인의 일부인데 하류 계약에 반영되지 않는 **침묵 탈락**이다. 이 판부터 **구조 게이트(`user_decision_required`) 해소 시 비공백 `--response` 는 승격되는 모든 task 의 `delegation.context` 에 조건 항목으로 주입된다**(`resolve_gate.build_promotion_payloads`).
  - **문면(결정적).** `[게이트 조건 — <gate_id> 해소(actor=<actor>)] <response>` 단일 문자열 항목. `gate_id`·`actor` 로 provenance 이벤트와 상호 추적하며, **타임스탬프를 넣지 않는다** — 시각은 이벤트가 소유하고 payload 는 결정적이어야 한다(같은 두 원장 재생 → 같은 바이트).
  - **원장 분리 보존.** `impl-plan.json`(원 산출)은 **바이트 무변조**이고, 조건 **원문**은 provenance 이벤트(`gate-resolution-provenance`·`ref.response`)가 계속 소유하며, 주입본은 revision payload(하류 소비 뷰)에만 실린다. 세 원장이 각자의 역할을 유지한다.
  - **적용 범위 = 승격 전 task 균일(D-N4).** task 별 조건 라우팅은 도입하지 않는다 — 응답이 단일 원문이므로 분배 근거가 없다. 하류 단위가 자기에게 해당하는 조건을 스스로 식별한다(브리프 자족 원칙).
  - **타입 규칙·fail-closed(D-N3).** `context` 가 리스트면 사본에 append, 문자열이면 `[원문, 조건]` 으로 승격, **부재/`null`이면 `[조건]` 신설**(빈 채널). 그 외 형(객체 등)이면 조건을 담을 곳이 없으므로 **비영 종료·원장 무오염**으로 차단한다 — 채널 자신이 조건의 침묵 탈락을 재생산하지 않는다. 주입 payload 선구성은 **어떤 원장 append 보다 앞서** 수행된다(검증-먼저 패턴 동형).
  - **context 신설의 관측 신호.** context 부재로 조건만 담아 신설한 단위는 `[CONDITION-NOTE]` 라인에 **id 로 열거**된다 — 그 단위는 종전이라면 Host 가 디스패치 직전 `missing_fields`(`delegation.context`)로 잡아 Escalated 시켰을 단위이고, 주입으로 디스패치 가능해지기 때문이다. 조건부 승인이 **별개 결함(위임 context 누락)을 가리지 않도록** 표면화하는 것이며 **차단이 아니다**(rc 무변). 차단하지 않는 근거: 어댑터 검증기가 애초에 `delegation.context` 를 요구하지 않아 부재 계획은 조건 없이도 승격 가능하므로, 조건부 승인만 더 엄격하게 만드는 것은 비일관이다.
  - **관측(D-N7).** 주입 시 `[CONDITION]` 라인이 주입 건수와 원문 출처(provenance 이벤트)를 명시한다. 응답이 공백(기본)이면 주입 0 이고 이 라인도 없다 — 종전 거동 바이트 동일.
  - **하류 도달 경로.** 승격 payload → fold(`_copy_task`) → `Step.from_dict` → `assemble_bundle` 의 `memory_material`(Worker fresh-context 번들) · CP2 `verify_bundle` 의 `step_contract.delegation`(Verifier). escalation 게이트의 `--response` 는 종전대로 해소 이벤트 ref 동봉·재작업 지시 전파 경로다(§3.4).
- **해소 어휘의 현행 형태(인용).** orchestration 해소 어휘는 재시도 예산 비계수를 이미 충족한다 — `append_gate_resolution`(03 10필드 재사용·`ref.kind=gate-resolved`·outcome=pass·retry_count=0)은 step 재시도 예산(`outcome=fail` 계수)을 소모하지 않는다(§7 OQ-PO-B2 해소). UAHF step-host 층의 해소=fail 계수 결합(OQ-SH-5·step-hosting-binding §7)은 무수정 경계상 별도 트랙 소관이며, 해소 취소(revoke) 어휘는 OQ-PO-B6 저순위 이월이다.

### §3.4 실행 에스컬레이션(Escalated 정지)의 해소 채널 (백로그 §J 본체 해소·2026-07-26)

§3.3 은 `_process_gates` 가 발화한 정지 게이트(단위 경계)의 해소를 다룬다. 이 절은 그 앞단 —
**Step Host 가 실행 중 낸 Escalated 정지**(재시도 한도 초과·차단 선언·SH-INV-4)의 해소를
같은 채널로 물리화한다. 이전 판에서 이 정지는 gate_id 가 없어 해소 이벤트를 append 할
대상 자체가 없었고, 그래서 `--resume` 이 대상 단위를 재디스패치하지 못했다(백로그 §J ①②).

- **좌표 발급(엔진).** `orchestrator.run()` 이 Host 의 `stopped/escalated` 를 받으면,
  `gate_policy` 가 있을 때 각 정지 단위에 대해 `escalation_required` **게이트 요구**를
  append 한다(`append_gate_requirement` 재사용·새 어휘 0). gate_id =
  `gate-unit-<단위 id>::exec-escalation` — 단위 경계 게이트(`gate-unit-<id>`)와 비충돌하는
  결정적 파생이며 재개 간 안정하다. `scoped_question` = `{unitId, gateKind, cause:
  "execution_escalated"}`. `gate_policy` 미지정(레거시 조립)이면 append 0 = 종전 거동.
- **멱등·재에스컬레이션.** 요구가 이미 실재하고 그것이 마지막 escalated 이벤트보다 뒤면
  재append 하지 않는다(같은 두 원장 재생 → 같은 로그). 되돌림 후 **다시 실패**하면 새
  escalated 이벤트가 그 요구보다 뒤서므로 **새 요구**를 append 한다 — `is_resolved` 의
  since 규칙(최신 요구 이후 해소만 인정)이 이전 해소를 소진시킨다. 즉 **해소 1건 = 추가
  시도 1회**이며, 한 번의 해소가 무한 재시도로 번지지 않는다.
- **정지 신호(런처).** `orchestrate_project.run_and_map` 은 escalated 정지에서도
  `logs/stop-signal.json` 을 **게이트 분기와 같은 계약 형태**
  `{stop_reason, stopped_tasks, pending_gates, note}` 로 기록하고 `[PENDING-GATES]` 출력과
  게이트 큐 렌더를 덧붙인다. 기존 `[STOP] escalated -> exit code 2` 라인과 exit 2 매핑,
  그리고 gate 분기의 출력·기록은 그대로다(가법). `pending_gates` 가 비면(게이트 정책 없는
  레거시 run) 빈 배열 + note 에 그 사실을 명시한다 — 침묵으로 넘기지 않는다.
- **해소(주 세션).** `resolve_gate.py <run_dir> --gate-kind escalation --actor <Advisor|human>
  --response "<재작업 지시>"`. 적격성 판정은 §3.3 표 그대로이며(`escalationResolvers`) 이
  스크립트가 우회하지 않는다. `--response` 원문은 해소 이벤트 `ref.response` 에 **동봉**된다
  (미지정 시 ref 형태는 종전과 동일 — 가법).
- **해소 대상 지목 `--gate-id` (2026-07-26).** `resolve_gate.py <run_dir> --gate-kind escalation
  --actor <Advisor|human> --gate-id <gate_id>` 로 해소 대상 게이트를 **특정 지목**한다. 같은
  gateKind 게이트가 **2건 이상 동시에 pending** 이면 지목이 필수다 — 무지목 호출은 후보
  (`gate_id`·`target`·`since`)를 열거하고 **원장 무변경으로 비영 종료**한다. 이전 판은 첫
  매칭을 침묵 선택했고, 그 결과 사용자가 지목하지 않은 단위의 게이트가 해소될 수 있었다.
  지목한 `gate_id` 가 pending 에 없거나 그 게이트의 gateKind 가 `--gate-kind` 와 다르면
  사유를 구분해 출력하고 역시 비영 종료한다(원장 무변경). 지목 없이 매칭이 **정확히 1건**인
  단일 게이트 경로의 거동은 종전과 같다(가법).
- **재디스패치(재개).** `orchestrate_project.py <project_root> --resume` 재기동 시 엔진이
  적격 해소(해소 at > 마지막 escalated at)를 소비해 그 단위 사이클에 **되돌림 이벤트**를
  1건 append 한다(`outcome=fail`·`trigger=재작업 되돌림(에스컬레이션 해소)`·
  `ref={kind:"gate-rework", gate_id, response}`·03 §3.2-A 10필드 무수정). 상태 파생이
  Escalated → Failed 로 바뀌어 `ready_set` 이 그 단위를 다시 포함하고, Host 는 한도를
  **실패 시점에만** 판정하므로 정확히 1회의 추가 디스패치가 일어난다. 해소 응답은 그 되돌림
  ref 를 거쳐 재디스패치 번들의 `feedback` 으로 실행 단위에 도달한다(테스트로 실측).
- **레거시 run 의 회복 경로.** 좌표 없이 Escalated 로 멈춰 있던 기존 run 도 `--resume` 1회면
  요구 이벤트가 생성되어(정지 유지·재실행 0) 그 다음부터 위 해소 절차를 쓸 수 있다.
- **`--retry-limit` 의 위치.** `--resume` 에서도 이 override 가 `config.json` 에 반영되고
  이전→새 값이 출력된다. 되돌림은 한도와 무관하게 추가 시도 1회를 부여하므로 이 플래그는
  편의이지 해소의 전제가 아니다.
- **다중 escalation 의 순차 해소.** 여러 단위가 동시에 Escalated 이면 그중 하나의 해소는 그
  단위에 되돌림 이벤트를 append 하되, 다른 단위가 Escalated 로 남아 Host 가 정지하므로
  **추가 디스패치는 나머지 해소 이후에 실행된다**(SH-INV-4 보존의 귀결·정보 손실 없음 —
  되돌림은 원장에 이미 기록돼 있어 다음 재개가 소비한다).

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

- **실행 주체 = fresh 세션(claude CLI headless)**. Orchestrator 가 직렬화한 단위는 중립 Step Host 를 통해 `step-invoker/claude_invoker.py`(`ClaudeInvoker`·무수정 재사용 — 오케스트레이션 층이 포크·재정의하지 않는다는 뜻이며, UAF 층의 브리프 개정까지 금지하는 것은 아니다)로 디스패치된다. capability 슬롯은 매칭 입력이고(§5.4), 물리 호출은 role 슬롯이 주도한다 — Worker(실행)·Verifier(CP2·`review_required` 추가 리뷰)·Advisor(`approval_required` CP3)는 전부 `--append-system-prompt` 역할 브리프로 fresh 세션에 실린다(step-hosting-binding §5.1·§5.2 동형·신설 0). 게이트 리뷰/승인 단위도 같은 디스패치 경로를 쓴다(orchestrator `_dispatch_gate_step`).
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

### §5.8 Run 관측 계약 — heartbeat · failure record · 종료 코드 (백로그 §L·§P·2026-07-26)

§5.3 run 데이터 레이아웃의 `logs/`에 **런처 소유 관측 산출 2종**을 가법한다. 기존 `logs/` 항목(`invoke-*.json`·`stop-signal.json`·`gate-resolution-record.json`·`host.pid`)과 §2 종료 코드 매핑은 무변경이며, 아래는 그 위에 얹는 절이다(재정의 0). 생산자는 `orchestration/adapters/claude/orchestrate_project.py` 하나뿐이고 중립 코드(`orchestration/framework/**`)·`uahf/**`는 무촉이다.

**왜 필요한가.** 실패 모드 3종의 관측 난이도가 다르다 — F1(죽음)은 프로세스가 끝나므로 종료로 드러나고, F3(오해석)은 종료 코드 규약으로 해소되지만, **F2(hang·무한대기)는 종료 이벤트가 원리적으로 발생하지 않는다.** 엔진 stdout은 버퍼링돼 실행 중에는 비어 있으므로 로그 tail도 대체가 되지 않는다(실측 2026-07-24). 따라서 정체 판정에는 **진행의 능동적 증거**가 필요하다.

**(a) `logs/heartbeat.json` — 계약 필드 5종·덮어쓰기**

| 필드 | 의미 |
|---|---|
| `ts` | 물리 시각 ISO 문자열(어댑터 경계이므로 실시각 허용) |
| `stage` | `invoke-start` \| `invoke-end` |
| `invokes` | 래퍼가 센 invoke 누계(1부터) |
| `request_hint` | 요청에서 파생한 단위 식별 최선값(`<role>/<unitId>`) 또는 `null` |
| `pid` | 러너 프로세스 id(`host.pid`와 대조 가능) |

- 갱신 시점 = invoke **시작 전**과 **종료 후** 각 1회. 파일은 append가 아니라 **덮어쓰기**다 — 소비자가 알아야 하는 값은 "마지막 진행 시각" 하나이며, 누적 계측은 백로그 H(Continuous Telemetry) 소관이다(경계 구분).
- 소비 방법 = 외부 감시자가 `ts`의 경과를 본다. `stage=invoke-start`로 오래 머물면 그 `request_hint` 단위에서 정체 중이다.
- 물리 형태 = 런처 소유 invoker 데코레이터(`HeartbeatInvoker`). `invoke`만 위임 가로채고 나머지 속성은 투과하므로 `invoke_count` 등 기존 관측 수치가 왜곡되지 않는다.

**(b) `logs/failure.json` — 계약 필드 6종**

`{ts, run_id, argv, error_type, error, traceback}`. 런처 구동 경로의 **미처리 예외**에서만 기록되며, 기록 후 예외를 **재raise**하므로 스택트레이스는 stderr에도 그대로 올라간다(은폐 0). 기존 정직 실패 경로(`[ERR]` 출력 + `return 1`)는 예외가 아니므로 이 파일을 만들지 않는다 — 거동 보존.

**(c) 관측 장치의 불변 — failure isolation.** 두 기록은 모두 실패해도 run을 실패시키지 않는다(`[HEARTBEAT-SKIP]`·`[FAILURE-SKIP]` stderr 경고 후 진행). 관측 장치가 관측 대상을 죽이면 안 된다(render_gates 부가 표면 방어와 동형). 다만 실패를 조용히 삼키지도 않는다(침묵 0).

**(d) 종료 코드 표(§2·`run_and_map` 매핑의 사용자 표면 인용 — 값 재정의 0)**

| 코드 | 의미 | 후속 |
|---|---|---|
| `0` | completed | 없음 |
| `2` | **정상 정지** — 게이트 미해소(`stop_reason=gate`) 또는 실행 에스컬레이션(`escalated`). 양쪽 모두 같은 계약 형태로 `stop-signal.json` 기록(§3.4) | 제시 → `resolve_gate.py` → `--resume` |
| `3` | halted | 원장 조사 |
| `1` | 런처 실패(정직 실패 또는 미처리 예외 — 후자는 `failure.json` 동반) | 메시지 조사 |

**(e) 슬러그 길이 상한(백로그 §P·§L 4-b 해소).** 컴파일러 `_slug`(seed unit id)와 런처 `slugify_run_id`(run_id)가 **공통 규칙**(`contract_to_graph.fold_slug`)을 쓴다 — 정규화 결과가 48자를 넘으면 `앞 48자 + "-" + sha256(원문)[:8]`(최대 57자)로 접는다. 48자 이하는 바이트 동일이라 기존 run 디렉터리·unit id는 하위호환된다. 근거 = unit id가 `steps/<unitId>.json`·`logs/invoke-NN-<Role>-<unitId>.json` 파일명이 되므로 상한이 없으면 (i) 긴 ASCII `--phase`에서 Windows 경로 한계 크래시(§P 실측)·(ii) git `Filename too long`으로 **run 원장을 커밋할 수 없다**(§L 4-b 실측 — 파일명 239자·경로 367자). 두 함수가 서로 다른 상한을 쓰면 `--resume`의 슬러그 재파생이 실물 run_dir과 어긋나므로 규칙을 하나로 둔다.

**(f) 문서 접합부.** `.claude/commands/uaf-implement.md` §2의 재개 예시를 `--resume --run-id <run_id>` 형태로 정정하고 위 종료 코드 표를 실었다 — 종전 예시(`--resume`만 표기)는 런처의 슬러그 재파생 계약과 어긋나 `--run-id`를 준 run에서 반드시 실패했다(백로그 §L 5 재발 실측).

**(g) per-unit timeout — 단위별 실행 예산(백로그 §L Desired 4 해소·2026-07-26)**

전역 `timeout` 하나(§4 config `timeout` → `Orchestrator.timeout`)는 규모가 크게 다른 단위를 같은 예산에 묶는다. 이를 **단위 단위의 선택 값**으로 세분한다. 관측 계약(a·b)이 정체를 *보이게* 하는 장치라면 이 항은 정체의 한 원인(예산 부적합)을 *줄이는* 장치이며, 종료 코드 표(d)·기존 로그 산출은 무변경이다.

| 층 | 계약 |
|---|---|
| 스키마 | impl-plan task 의 **선택 키** `timeout`(11키 밖·12번째) = 실행 예산 **초 단위 양의 정수**. 부재 = 전역 fallback. `REQUIRED_TASK_KEYS` 11키는 무변(필수 승격 아님 — 기존 run·플랜 하위호환) |
| 검증 | `resolve_gate.validate_impl_plan_adapter` — 키가 있으면 양의 정수만 수용하고 그 외(bool·0·음수·실수·문자열)는 오류 목록에 올린다. 판정 불가는 통과가 아니다(fail-closed·원장 무오염 — 불량값이 `task_added` 로 승격되지 않는다) |
| 재기입 | 중립 엔진(`orchestrator.UnitTimeoutInvoker`) — `{단위 id: timeout}` 맵을 들고 `request.bundle["step_contract"]["id"]` 매칭 시 `dataclasses.replace` 로 `request.timeout` 을 재기입한다. 원본 request 무변조(순수)·비매칭은 원 객체 그대로·`__getattr__` 속성 투과(`HeartbeatInvoker` 선례 동형) |
| 맵 원천 | `active_graph()` 파생 하나뿐(PO-INV 3 — 제2 진리원천 0). 유효값만 편입하고 불량값은 편입하지 않는다(차단은 검증 게이트 소유·래퍼는 기계 재기입만·판단 0) |
| 적용 범위 | 한 단위의 **exec·CP2·게이트 디스패치 3경로 전부**가 그 단위의 예산을 받는다(균일 규칙). `_effective_invoker()` 는 맵이 비어 있지 않을 때만 최외곽 래핑하고, `_dispatch_gate_step` 은 같은 맵으로 timeout 래핑만 경유한다(산출물 포집 래퍼를 게이트 경로에 새로 끼우지 않는다) |
| 거동 보존 | 맵 공집합(= `timeout` 을 쓴 단위 0)이면 **래핑 자체가 없다** — 기존 반환·기존 요청 객체 그대로다(`allocation=None`·`artifact_store=None` 패턴 동형). seed proposal 노드는 timeout 미부여(컴파일 시점에 단위 규모 정보가 없고 값을 발명하지 않는다) |
| Planner 지시 | `contract_to_graph._seed_prompt` 구현 task 구성 규칙에 선택 키 안내 1항(양의 정수·초·명백히 대형인 단위에만·미지정 = 전역 기본). `_done_ac` 는 11키만 검사하므로 무변 |

`uaf-verified:` 값이 실제 프로세스 예산에 닿는 경로 = `request.timeout` → 실 CLI invoker 의 subprocess timeout(`step-invoker/claude_invoker.py`). 검색 범위 = orchestration 2트리 + uahf step-host/step-invoker 트리의 해당 지점 정독이며, 실 LLM run 관측은 아직 없다(오프라인 stub 통합·접합부 왕복 테스트까지가 현 근거).

**(h) 횡단 결함 검지 — `[REWORK-NOTE]` 관측 라인 + `sweep_units.py` 스윕 도구 (백로그 §M D-M2·2026-07-26)**

CP2 재작업은 **그 단위만의 결함 신호가 아니다.** 같은 API 오용·같은 잘못된 관례가 동료 단위에 복제돼 있어도 각 단위의 done AC는 자기 산출만 보므로 통과한다 — 개별 단위 합격의 합이 phase 완결과 같지 않은 구조적 이유다. (a)·(b)가 *정체*를 보이게 하는 장치라면 이 항은 *복제된 결함*을 보이게 하는 장치이며, 종료 코드 표(d)·기존 로그 산출·기존 종료 라인은 무변경이다.

**경계(불가침) — 판단 0.** 어떤 패턴이 결함인지, 적중을 어떻게 조치할지는 **전부 사람/Advisor 소유**다(PO-INV 1). 런처와 도구는 기계 파생·기계 스캔·권고까지만 한다. 자동 되돌림은 **미도입**이다(D-M3 — 결함 패턴 추출은 내용 판단이라 엔진이 소유할 수 없고, Passed 단위의 기계 되돌림은 상태 어휘 변경 또는 supersede 의미론 신설을 요구한다).

| 층 | 계약 |
|---|---|
| 신호 원천 | `events.jsonl` 의 `ref.kind == "rework"` 이벤트(step-host `_record_failure` — CP2 Fail/Conditional 경로). 런처는 이 어휘를 **읽기만** 하며 재정의하지 않는다 |
| 파생 | `orchestrate_project.rework_units(run_dir)` → 해당 이벤트를 가진 `cycle_id` 목록(원장 등장 순·중복 제거·결정적) |
| 출력 | `orchestrate_project.print_rework_note` — `[INVOKES]` 라인 **이후**, status 분기 **이전**에 3행: ① 재작업 단위 id 열거 ② 동료 단위 횡단 스윕 권고 ③ 스윕 명령 힌트(`python orchestration/adapters/claude/sweep_units.py <run_dir> --pattern "<정규식>"`) |
| 지시 인용 | ①과 ② 사이에 단위별 1행으로 그 단위의 **마지막** `ref.rework` 를 **원문 인용**한다(`· <단위 id> ← <지시 원문>`). 비-문자열은 `json.dumps` 직렬화·개행은 행 맞춤용 공백 접기·200자 초과는 `…(클립)` 표기(`REWORK_QUOTE_CLIP` = sweep `LINE_CLIP` 동형). **인용만 한다** — 해석·요약·패턴 추출은 하지 않는다(표면화는 판단이 아니다·`render_gates` 의 `scoped_question` 렌더 동형·PO-INV 1 비저촉). `ref.rework` 부재/None/공백이면 그 단위의 인용 행을 생략한다(발명 0·본행은 유지) |
| 거동 보존 | rework 0이면 **어떤 라인도 출력하지 않는다**(종전 출력 바이트 보존). 원장 부재·파손은 note만 생략하고 `[REWORK-NOTE-SKIP]` stderr 1행으로 생략 사실을 명시한다 — 런처 흐름·종료 코드 불변(render_gates 부가 표면 방어와 동형·침묵 0) |
| 스윕 도구 | `orchestration/adapters/claude/sweep_units.py`(form-B·LLM 0·읽기 전용). `build_orchestrator_k` 무수정 재사용 → `active_graph()`·`derive_states()` 파생 → 각 단위 `ownedBoundary`(워크스페이스 상대경로)를 config `workspace_dir` 아래에서 해석(디렉터리는 재귀) → 라인 단위 정규식 검색 → 단위별 `file:line :: 문면` + 단위 상태 병기 |
| 판독 규율 | 파일 판독은 `encoding="utf-8", errors="replace"` 고정(한국어·혼합 인코딩에서 디코딩 예외로 스윕이 끊기면 관측 경로가 유실된다). 바이너리(NUL 바이트 표본)·판독 불가 파일은 건너뛰되 **건수를 항상 보고**한다(`[SKIPPED] binary=N unreadable=M` — 0건도 명시). 미실재 경계 항목·워크스페이스 밖 경계 항목도 건수 표면화(침묵 스킵 0) |
| 쓰기 | **0(사전 검사로 보장).** `build_orchestrator_k` 는 라이브러리로서 쓰기 부작용을 갖는다 — 부재 시 `events.jsonl`·`revisions.jsonl`·`artifacts.jsonl` 을 빈 파일로 생성하고 `workspace_dir` 을 `makedirs` 한다. 따라서 `sweep_units.precheck(run_dir)` 가 **조립 전에** 그 대상 전부(+ `config.json`·`graph.json`·`gate_policy.json`)와 config `workspace_dir` 디렉터리의 실재를 순수 판독으로 확인하고, 하나라도 없으면 **아무것도 만들지 않고** exit 1 + 부재 목록 열거 + "읽기 전용 도구라 생성하지 않는다(불완전 run_dir)". 결과: **정상·오류 모든 경로에서 실행 전후의 run_dir·워크스페이스 파일 집합이 바이트·목록 동일**하다(관측 장치가 관측 대상을 바꾸지 않는다) |
| 조치 안내 | 출력 말미 `[NEXT]` 1행 = 조치는 **수정 run 또는 supersede(원장 경유)**. 적중 단위를 워크스페이스에서 직접 손보는 것은 금지(원장 밖 직접 수정 = 계보 단절) |

**종료 코드(스윕 도구 — (d) 런처 표와 별개 표면):**

| 코드 | 의미 |
|---|---|
| `0` | 스윕 정상 수행·**히트 0** |
| `2` | **히트 존재**(단위별 `file:line` 보고) |
| `1` | 오류 — `run_dir` 부재/비디렉터리 · `--pattern` 무지정(도구는 패턴을 발명하지 않는다) · 정규식 컴파일 실패 · **불완전 run_dir**(`precheck` 부재 항목 — 생성 0) · 그래프/원장 판독 불가 |

**Planner 지시 짝(D-M1).** `contract_to_graph._seed_prompt` milestone 규칙에 두 항을 가법했다 — (i) milestone done AC는 **단위 간 계약 정합 검사를 최소 1건 포함**한다(개별 파일 존재 나열만으로는 불충분·최소 1건은 둘 이상의 단위를 상호 대조. 오프라인 안전형 예 = 선행 `produces`↔후행 `consumes` 경로 상호 대조·모듈 경계 참조 무결·공유 계약 데이터 키 집합 일치) (ii) milestone task 문면에 **횡단 관점** 지시(한 단위에서 발견된 결함 패턴을 동료 단위에 같은 기준으로 대조하고 그 결과를 보고). 기존 문면(오프라인 AC 허용 3종·금지 목록·11키·per-unit `timeout` 선택 키 항)은 무변이다.

**미해소 이월(정직 구분).** 백로그 §L 1의 `current_unit`·`elapsed_s` 필드는 `request_hint` 하나로 축약했다(런처가 단위 경계를 소유하지 않으므로 요청에서 파생 가능한 값만 싣는다). §M의 자동 되돌림(D-M3)은 위 경계 사유로 미도입 — 재심 좌표 = Verifier 구조화 verdict(`sweep_patterns` 필드) 도입 시.

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
- **OQ-PO-B2 (해소 어휘 성숙) — 해소(2026-07-19·문서·설계 수준 종결).** 2축 분리로 종결한다. **(1) 재시도 예산 비계수 = orchestration 엔진 이미 충족.** 엔진의 해소 어휘는 전용이다 — `append_gate_resolution` 이 `ref.kind=gate-resolved`·`outcome=pass`·`retry_count=0` 으로, 요구 이벤트도 `outcome=escalated`·`retry_count=0` 으로 append 하므로(gates.py) 게이트 해소가 step 재시도 예산(`outcome=fail` 계수)을 소모하지 않는다. OQ-SH-5 의 "해소=fail 계수 결합" 결함은 `outcome=fail` 을 재사용하는 UAHF step-host(`uahf/framework/loop/step-host/`) 층에 국한되며, orchestration 은 자체 `gate-resolved`/`pass` 어휘를 쓰므로 그 결함을 상속하지 않는다 — UAHF 층 자체 해소는 무수정 경계(§6·05 §262)상 별도 트랙(OQ-SH-5·step-hosting-binding §7) 소관이다. **(2) 해소 취소(revoke)** = 저임팩트·실사용 오용 관측 0 의 투기적 잔여로, OQ-PO-B6 으로 정밀 재스코프해 저순위 이월한다. 본 판은 `append_gate_resolution` 현행 형태만 바인딩한다(엔진 코드·계약 변경 0). (구 이월 포인터 "05 §9 OQ 3" 은 05 spec §9 가 순수 이력표이고 OQ 절이 부재함을 전수 실측 확인해 정정 — 05 엔 OQ 3 부재.)
- **OQ-PO-B3 (headless 런처 ↔ 사용자 세션 제시 브리지) — 해소(production·2026-07-18).** 물리 브리지 형태 확정: 프로덕션 런처(`orchestrate_project.py`)가 정지 게이트 시 **종료 코드 2 + `logs/stop-signal.json`(pending_gates)** 를 기록 → 주 세션 Advisor 가 그 파일을 읽어 게이트 큐를 사용자 대화 세션에 표면화(§3.2 headless·채널 분리 유지) → 사용자/Advisor 해소를 `resolve_gate.py <run_dir> --gate-kind … --actor …` 로 게이트-해소 이벤트 append(적격성 = gates.py `is_eligible_resolver` 코드 소유) → `orchestrate_project.py --resume` 로 결정적 재개(원장 fold). §5.7 tms-system 실 run 으로 실증. (사람 친화 렌더 최종 문법 = OQ-PO-B1 이월.)
- **OQ-PO-B4 (실 LLM 제안 step·비픽스처 성숙 run) — 해소(제안·승격 사이클·production·2026-07-18).** §5.7 tms-system 실 run 에서 확정 설계(Contract v2·solution-design)를 **실 LLM(haiku) 제안 step** 이 소비해 구현 task 6개(implementation 5 + milestone 1)를 제안하고, **실 사용자 게이트 해소**(actor=human·simulated=false)로 revision 승격했다 — 드라이버 픽스처(§5.6 j)가 아닌 실 LLM 제안 + 실 사용자 해소. 잔여(후속 트랙): 승격된 구현 단위의 **resume 실 코드 산출**(형태 A 완전 성숙 run·BPD-20 동형)은 사용자 선택으로 후속 세션 defer — 제안·게이트·승격 사이클은 본 run 으로 실증됐고 코드 산출 축만 이월된다.
- **OQ-PO-B5 (엔진 `accept_revision` 게이트-pass 재검증의 actor 미검사) — 해소(2026-07-19·§DC-9).** `orchestrator._gate_event_exists`(→ `_event_grounds_gate`)를 강화해 방어적 이중화의 **엔진 측을 완성**했다. 강화 규칙: 매칭 pass 이벤트가 **정지 게이트 해소로 자신을 선언**하고(`ref.kind == REF_KIND_RESOLVED` **그리고** `ref.gateKind ∈ STOPPING_GATES`) `self.gate_policy is not None`이면, 그 해소 actor 가 `gate_policy.is_eligible_resolver(gateKind, actor)` 로 적격일 때만 revision 을 근거지을 수 있다(05 §3.3 확정 권위 정합 — user_decision = 사용자 actor 클래스만·escalation = 허용 resolver 집합만). 부적격 actor 의 pass 해소 이벤트는 로그에 남아도 승격 근거가 되지 못한다. **거동 보존 3면(불가침):** (a) 레거시 이벤트(`ref.kind == "gate"`·gateKind 부재·S2 관례) = 실재-만 검증 유지 · (b) 비정지 gateKind(`review_required`/`approval_required` 등) gate-resolved 이벤트 = 실재-만 검증 유지(`is_eligible_resolver` 는 비정지에 False 라 일괄 적용 시 rework 근거 패턴이 깨진다 — 적용 범위를 `STOPPING_GATES` 로 한정하는 이유) · (c) `gate_policy is None`(S2 조립) = 실재-만 검증. **적용 시점:** `_gate_event_exists` 는 `accept_revision`(수용)과 `_grounded_revisions`(재개 fold 필터) 양쪽에서 쓰이므로 이 강화는 **수용 시점과 재개(fold) 시점 모두**에 걸린다. 프로덕션 resolver(`resolve_gate.py`)의 상류 append 거부(독성 pass 이벤트 미생성)와 함께 이중 방어를 이룬다. `orchestration/framework/**` provider·모델 토큰 0(PO-INV 8·`STOPPING_GATES`·`REF_KIND_RESOLVED` 중립 어휘만 가법 import).
- **OQ-PO-B6 (해소 취소 어휘 부재 — 저순위·OQ-PO-B2 에서 재스코프).** append-only 원장에서 오append 된 게이트 해소 이벤트를 되돌리는 전용 어휘·연산이 없다(실사용 오용 관측 0·투기적). 도입 시 필요 설계: 취소 actor 적격성(누가 취소 가능한가·`is_eligible_resolver` 정합)·취소 후 게이트 재-pending 전이 의미·원장 fold 에서 취소가 선행 해소를 무효화하는 규칙(append-only 보존·보상 이벤트 형태). 현행 미도입 — 필요 관측 시 착수.

---

## §8. 개정 이력

- **2026-07-26 (AC 실출력 픽스처 규율·자기출제 — 백로그 §O 해소·D-O1·D-O2·D-O3).** AC 를 스스로
  출제한 단위가 합성 입력으로 통과시킨 검사를 외부 도구 계약의 검증으로 주장할 수 있던 결함을 두
  층으로 해소했다: (i) **출제 층** — `contract_to_graph._seed_prompt` [구현 task 구성 규칙]에
  「실출력 픽스처 규율」 가법 — 외부 도구·프로세스를 호출하는 단위는 실출력 캡처 픽스처를
  워크스페이스에 고정하고 done AC 가 그것을 소비해야 하며(픽스처는 ownedBoundary·
  `interfaceContract.produces` 등재·캡처 명령/버전/시점 기록), 캡처 불가 시 완료 보고
  `open_questions` 에 「미검증 외부 계약」으로 신고한다(침묵 금지·이진). 기존 문면(밀스톤 상호
  대조·per-unit `timeout` 선택 키·오프라인 안전 AC) 삭제 0 (ii) **판정 층** —
  `step-invoker/claude_invoker.py` `_ROLE_BRIEFS[ROLE_VERIFIER]` 에 **AC 적정성** 판정 축 가법
  (합성 입력의 실출력 대체 여부·assert 가 실값을 못박는가·"통과 자체가 증거가 되는가"·부적정 시
  산출 결함과 구분해 **Fail + rework 에 AC 결함 명시**) + 외부 도구 호출 단위의 실출력 픽스처
  소비 확인. Worker/Advisor 브리프 무변. (iii) **인코딩 스윕(D-O3)** —
  `uaf-verified: 스윕 범위 = orchestration/**·entry/**·uahf/framework/adapters/**·.claude/hooks/**
  의 실행 .py 48개(tests·orchestration-data/runs 제외)를 subprocess 계열·텍스트 open() 두 축으로
  grep 수집 후 호출 단위 정독으로 판정 — 라인 grep 단독은 오탐(claude_invoker 의 text=True 는
  후행 행에 encoding 실재)이라 채택하지 않았다.` 판정 결과와 미수정 사유는 백로그 원장에 기재.
  신규 테스트: `test_contract_to_graph.py` 5케이스 · `test_claude_invoker.py` 5케이스(브리프 상수
  직독이 아니라 `build_command()` argv 의 `--append-system-prompt` 값 왕복 검사).
  **05 spec 계약 본문·게이트 어휘·PO-INV·Frozen·`orchestration/framework/**`·
  `uahf/framework/loop/**`·uahf specs·scaffold-template 무접촉(재정의 0).**

- **2026-07-26 (횡단 결함 검지 — 백로그 §M 해소·D-M1·D-M2).** CP2 재작업이 동료 단위의 복제 결함을
  가리키는 신호임에도 그것을 볼 경로가 없던 결함을 두 층으로 해소했다: (i) **Planner 지시** —
  `contract_to_graph._seed_prompt` milestone 규칙에 「단위 간 계약 정합 검사 최소 1건 의무」
  (개별 파일 존재 나열 불충분·`produces`↔`consumes` 상호 대조 등 오프라인 안전형 예 3종) +
  「횡단 관점 지시」 가법(기존 문면·per-unit `timeout` 선택 키 항 무변) (ii) **관측·도구** —
  런처에 `rework_units`/`print_rework_note` 신설(`[INVOKES]` 이후·status 분기 이전·rework 0이면
  무출력·원장 부재/파손은 `[REWORK-NOTE-SKIP]` stderr 1행 후 흐름·종료 코드 불변) + 신규
  `sweep_units.py`(form-B·LLM 0·읽기 전용 — `build_orchestrator_k` 재사용 → `active_graph`/
  `derive_states` 파생 → `ownedBoundary` 해석·디렉터리 재귀 → 라인 정규식 스캔 → 단위별
  `file:line` 보고·exit 0/2/1). 판단 0 보존(패턴 선정·조치 판단은 사람/Advisor 소유·PO-INV 1) —
  자동 되돌림(D-M3)은 미도입. **CP2 재작업 2건 반영**: (1) `sweep_units.precheck` 신설 —
  조립(`build_orchestrator_k`)이 부재 시 생성하는 JSONL 3종 + 소비 JSON 3종 + `workspace_dir`
  디렉터리의 실재를 **조립 전에** 순수 판독으로 확인하고 부재 시 생성 0·exit 1(종전 docstring
  "쓰기 0" 선언과 조립 부작용의 문서-진실 불일치 해소 — 이제 모든 경로에서 실행 전후 파일 집합
  동일) (2) `[REWORK-NOTE]` 에 단위별 마지막 `ref.rework` **원문 인용** 행 가법(`rework_details`
  신설·`rework_units` 는 그 투영·비문자열 `json.dumps`·200자 클립 표기·부재 시 행 생략 —
  인용만이며 해석·요약·추출 0). §5.8 (h) 신설(§ 번호 불이동·기존 (a)~(g) 무변). 신규 테스트
  `test_sweep_units.py` 22케이스(seed 문면 3 = 계약 정합 의무·횡단 지시·기존 문면 보존 /
  `[REWORK-NOTE]` 8 = 실 rework run 열거·클린 run 무출력·원장 부재·원장 파손·파생 단위 계약·
  마지막 지시 인용+클립·부재 시 인용 생략·비문자열 직렬화 / 스윕 10 = 히트 exit 2·무히트 exit 0·
  오류 3종 exit 1·불완전 run_dir 3종 생성 0·워크스페이스 부재 미생성·precheck 단위 계약·
  재귀/바이너리 스킵 건수·읽기 전용·JSON 결정성·`--ignore-case` / **접합부 왕복 1 = 엔진 실구동
  CP2 Fail→rework→재시도 Pass → 실물 events.jsonl 판독 → 실 argv 스윕 히트** — 계수 근거:
  `def test_` 계수로 어댑터 트리 161→183).
  `uaf-verified:` 접촉 경계 = `git status` 목록 대조 — 엔진(`orchestration/framework/**`)·
  05 spec·게이트 어휘·PO-INV·Frozen·`uahf/**`·scaffold-template 무접촉(재정의 0).

- **2026-07-26 (조건부 승인 하류 전달 — 백로그 §N 해소).** 구조 게이트 해소의 비공백
  `--response` 를 승격 payload 의 `delegation.context` 로 주입하는 채널을 신설했다
  (`resolve_gate.format_condition`·`build_promotion_payloads`). 조건 원문의 **원장 보존은
  이미 성립**했으므로(`_append_provenance` 의 `ref.response`) 이번 판이 더한 것은 **하류 전달**
  뿐이다 — 조건이 승인의 일부인데 실행 단위 브리프에 닿지 않던 침묵 탈락의 해소.
  주입은 payload **사본**에만 이뤄져 `impl-plan.json` 은 바이트 무변조이고, 선구성이 어떤
  원장 append 보다 앞서므로 주입 불가 형(객체 등)은 원장 무오염으로 차단된다. 문면은
  타임스탬프 없는 결정적 형태(`[게이트 조건 — <gate_id> 해소(actor=<actor>)] <response>`).
  응답 공백(기본)이면 주입 0·`[CONDITION]` 라인 없음 = 종전 거동 바이트 동일. context 부재로
  신설한 단위는 `[CONDITION-NOTE]` 로 id 열거(관측 신호·차단 아님 — 조건 주입이 위임 context
  누락이라는 별개 결함을 가리지 않게 한다). §3.3 에 계약 문면 7항 추가(§ 번호 불이동)·`--response` help 및 모듈 docstring 4)항 동기화·
  `.claude/commands/uaf-implement.md` 사용법 1문 가법. 신규 테스트 17케이스
  (`test_resolve_gate.py` — 승격 3건 전부에 주입·결정적 문면·gate_id/actor 동봉·미지정/공백
  3종 주입 0·레거시 context 부재 계획 통과·리스트 사본 append·문자열 2원소 승격·불가 형
  차단+원장 sha 무변·무응답 시 형 무검사·검증기 context 무접촉·`[CONDITION]` 건수·
  `[CONDITION-NOTE]` 신설 id 열거/미신설 시 부재/혼재 계획 부분 신설/무응답 시 부재 4건·**실
  argv→revision payload→fold→엔진 run→Worker `memory_material`+CP2 `step_contract` 실물
  왕복** 1건 — 계수 근거: `def test_` 계수로 파일 63→80·어댑터 트리 144→161).
  `uaf-verified:` 접촉 경계 = `git status` 목록 대조 — 엔진(`orchestration/framework/**`)·
  05 spec·게이트 어휘·PO-INV·Frozen·`uahf/**`·scaffold-template 무접촉(재정의 0).

- **2026-07-26 (per-unit timeout — 백로그 §L Desired 4 해소).** 단위별 실행 예산을 impl-plan
  스키마의 **선택 키** `timeout`(양의 정수·초)으로 도입하고 세 층에 배선했다: (i) 검증 —
  `resolve_gate.validate_impl_plan_adapter` 가 키 존재 시 양의 정수만 수용(bool·0·음수·실수·
  문자열 거부·fail-closed·원장 무오염), `REQUIRED_TASK_KEYS` 11키 무변 (ii) 재기입 — 중립
  엔진에 `UnitTimeoutInvoker` 신설(맵 매칭 시 `dataclasses.replace` 로 `request.timeout` 재기입·
  원본 무변조·비매칭 원 객체 통과·`__getattr__` 투과), 맵 원천은 `active_graph()` 파생 하나
  (유효값만 편입) (iii) 배선 — `_effective_invoker()` 최외곽 래핑 + `_dispatch_gate_step` 동일
  맵 경유로 exec·CP2·게이트 3경로 균일 적용. 맵 공집합이면 래핑 0(기존 거동 보존).
  `contract_to_graph._seed_prompt` 에 Planner 선택 키 안내 1항 추가(`_done_ac` 무변). §5.8 (g)
  신설(§ 번호 불이동·기존 (a)~(f) 무변). 신규 테스트: `test_orchestrator.py` 11케이스(래퍼 재기입·원본 무변조
  ·비매칭 원 객체 통과·step_contract 부재 통과·속성 투과·맵 유효값 필터·공집합 래핑 0·비공집합
  최외곽 래핑·포집 래퍼 내측 순서·3경로 균일+미지정 전역 fallback·timeout 부재 그래프 거동
  보존·승격 단위 적용 — 계수 근거: 트리 175→186) · `test_resolve_gate.py` 6케이스(부재/양의 정수 통과·불량
  5종 거부·11키 불변·resolver 경로 차단·**impl-plan→검증→승격→fold→엔진 run→`request.timeout`
  실물 왕복** 1건). `revision.py`(fold 는 `dict(task)` 얕은 복제라 무변경 통과)·05 spec 계약 본문
  ·게이트 어휘·PO-INV·Frozen·`uahf/**`·scaffold-template 무접촉(재정의 0).

- **2026-07-26 (해소 대상 특정 지목 `--gate-id` — 백로그 §J 잔여 해소).** `resolve_gate.py` 의
  `recover_gate(run_dir, wanted_kind, gate_id=None)` 가 다중 pending 동일 gateKind 에서 첫
  매칭을 침묵 선택하던 것을 제거했다: 무지목 다중 매칭은 `ValueError`(후보 `gate_id`·`target`
  ·`since` 열거 + 지목 안내) → CLI 가 stderr 출력 + exit 1(원장 append 0). `--gate-id` 지정
  시 gate_id·gateKind **양쪽** 일치만 수용하고, 부재/kind 불일치를 구분해 보고한다. 기본
  인자로 기존 2-튜플 반환 계약·단일 게이트 경로 거동을 보존했다(호출부 무수정). §3.4 에 CLI
  행 추가. 신규 테스트 `test_resolve_gate.py` 5케이스(무지목 다중 차단·지목 해소 격리·부재
  id·kind 불일치·`recover_gate` 단위 계약). 게이트 적격 판정(`gates.py`)·해소 의미론
  (`resolve_structural`/`resolve_escalation`)·05 spec·`orchestration/framework/**`·`uahf/**`
  무접촉(재정의 0). **동일 트랙 후속:** `render_gates.resolve_command(gate_kind, policy,
  gate_id=None)` 이 항목별 명령에 `--gate-id` 를 싣도록 확장(텍스트·JSON 양쪽·셸 안전 인용
  규칙 포함·렌더는 판독 전용 유지)하고 `.claude/commands/uaf-implement.md` CLI 문면을
  동기화했다. 신규 테스트 `test_render_gates.py` 4케이스(텍스트/JSON 지목·단위 계약·다중
  pending 왕복 실행·단일 pending 왕복 실행).

- **2026-07-26 (백로그 §L 핵심 + §P 해소 — Run 관측 계약).** 런처(`orchestrate_project.py`)에 관측 계약 물리화: `HeartbeatInvoker` 데코레이터(invoke 시작 전·종료 후 `logs/heartbeat.json` 덮어쓰기·계약 필드 5종·인터페이스 투과로 `invoke_count` 보존) · 구동 경로 top-level 예외 포착 → `logs/failure.json`(계약 필드 6종) 기록 후 **재raise**(스택트레이스 stderr 보존·은폐 0·기존 `[ERR]` return 1 경로 무변) · `--resume` 대상 부재 시 RUNS_DIR 실존 후보 목록(수정시각 최신순·최대 10) 제시(기존 `[ERR]` 라인 바이트 보존 후 가법). 슬러그 길이 상한 공통 규칙 `contract_to_graph.fold_slug`(48자 초과 시 앞 48자 + `-<sha8>`·48자 이하 바이트 동일) 신설 후 `_slug`·`slugify_run_id` 양쪽 적용(§P 크래시·§L 4-b 원장 커밋 불가 해소). 두 기록 모두 failure-isolated(`[HEARTBEAT-SKIP]`·`[FAILURE-SKIP]`). `.claude/commands/uaf-implement.md` §2 재개 예시 `--resume --run-id` 정정 + 종료 코드 표 + 관측 파일 소개. §5.8 신설(§ 번호 불이동·§5 하위 append). 신규 테스트: `test_orchestrate_project.py` 14케이스(하트비트 3·failure 2·슬러그 4·resume 힌트 2·문서 왕복 3) · `test_contract_to_graph.py` 3케이스 = 17건(어댑터 트리 97→114 실측). **05 spec 계약 본문·게이트 어휘·`orchestration/framework/**`(gates.py·orchestrator.py)·PO-INV·Frozen·`uahf/**` 무접촉(재정의 0).** 미해소 이월 = 백로그 §L Desired 4(per-unit timeout).
- **2026-07-26 (백로그 §J 본체 해소 — 실행 에스컬레이션 해소 채널).** Host 의 Escalated 정지에 원장 좌표를 부여하고 해소→재디스패치 경로를 물리화. 엔진(`orchestrator.py`): escalated 정지 시 `escalation_required` 요구 append(gate_id = `gate-unit-<id>::exec-escalation`·cause `execution_escalated`)+`pending_gates` 탑재·멱등·재에스컬레이션 시 새 요구 append·적격 해소 소비 시 되돌림 이벤트(`ref.kind=gate-rework`) 1건 append → 추가 디스패치 1회. `gates.py`: `latest_eligible_resolution`/`resolution_response` 신설(순수 판독)·`append_gate_resolution(response=...)` 가법(미지정 시 ref 형태 종전과 동일). 런처: escalated 정지도 gate 분기와 같은 계약 형태로 `stop-signal.json` 기록+`[PENDING-GATES]`+렌더(기존 라인·gate 분기 출력·exit 매핑 무변), `--resume` 의 `--retry-limit` override 를 config 에 반영. `resolve_gate.py`: 해소 응답 동봉 + 재개 명령 안내 출력. §3.4 신설. 신규 테스트: `test_orchestrator.py` 7케이스(좌표 발급·멱등·레거시 보존·되돌림/응답 전파·부적격/선행 해소 무효·재에스컬레이션)·`test_gates.py` 3케이스·`test_orchestrate_project.py` 4케이스(정지 신호 계약·레거시 note·접합부 왕복·resume override)·`test_resolve_gate.py` 3케이스. **05 spec 계약 본문·게이트 어휘·해소 적격성·03 10필드·PO-INV·Frozen·`uahf/**` 무접촉(재정의 0).**
- **2026-07-19 (OQ-PO-B2 해소 — 해소 어휘 성숙·문서·설계 수준 종결).** OQ-PO-B2 를 2축 분리로 종결(사용자 결정 A·엔진 코드 무변경). (1) 재시도 예산 비계수 = orchestration 엔진이 전용 어휘(`gate-resolved`/`outcome=pass`/`retry_count=0`)로 이미 충족함을 명문화(OQ-SH-5 fail-계수 결합은 `outcome=fail` 재사용 UAHF step-host 층 국한·무수정 경계상 별도 트랙). (2) 해소 취소(revoke) = OQ-PO-B6 으로 정밀 재스코프·저순위 이월(신규 OQ 등재). stale 포인터 "05 §9 OQ 3"(05 spec §9 = 순수 이력표·OQ 절 부재·전수 실측) 정정 — §6·§7 인용 2곳. **§6 해소 어휘 인용·§7 OQ-PO-B2 해소·OQ-PO-B6 신설만 갱신 — 05 계약 본문·gates.py·PO-INV·§3 게이트 어휘·Frozen·`orchestration/framework/**`·`uahf/**` 무접촉(재정의 0).**
- **2026-07-19 (seed 컴파일러 일반화 — §DC-1 뿌리·백로그 해소).** `contract_to_graph.py`(F4)의 tms 도메인 하드코딩(프로젝트 표기·`pc-tms-001 v2`·정산 최소폐포 SD-D 앵커 블록·milestone 문면·`orch-tms-` run_id·seed id·워크스페이스 경계 문구)을 제거하고 소비 프로젝트에서 파생하도록 일반화: 프로젝트 표기=워크스페이스 루트 폴더명·Contract 버전=파일명 파생(`contract_version`·내용 파싱 0 불변)·seed id=`seed_task_id(phase_scope)`·run_id=`orch-<root.name>-<phase>`. 설계 앵커 하드코딩 블록 → 일반 지시(런타임 LLM 이 입력 문서에서 phase 범위·설계 결정 식별자 자가 식별·계층 편향 없이 전 영역 커버·05 §3.1 정합). F4↔F5 proposing step 파생(최중요 교차 계약): `resolve_gate.py`의 `PROPOSING_STEP_REF` 하드코딩 제거 → `derive_proposing_step_ref(run_dir)`가 물리 `graph.json`의 proposal 노드 id 파생(0건/2건 시 원장 무변경 비영 종료). compile→물리화→resolve_gate 관통 통합 테스트로 proposingStepRef=파생 id 실증. `orchestrate_project._resolve_slug`도 root.name 파생으로 동조. **11키 스키마·3~6 배합·milestone 종단·오프라인 AC·`gate_policy` 3엔트리·resolve/compile 순수성·stdlib only·`orchestration/framework/**`·`uahf/**`·spec/Frozen 무접촉(재정의 0).**
- **2026-07-19 (§DC-9 05 wiring 후속 — OQ-PO-B5·OQ-PO-B1 해소).** OQ-PO-B5 해소: 엔진 `orchestrator._gate_event_exists`(→ `_event_grounds_gate`) 강화 — 정지 게이트 해소 선언(`ref.kind==gate-resolved`·`gateKind∈STOPPING_GATES`)+`gate_policy` 존재 시 `is_eligible_resolver` actor 자격까지 요구(수용+fold 양시점). 거동 보존 3면(레거시 `ref.kind="gate"`·비정지 gateKind·`gate_policy None`) = 실재-만 검증 유지. OQ-PO-B1 해소: `render_gates.py` 신설(형태 B·결정적·LLM 0·읽기 전용 게이트 큐 렌더러·라벨 표 = 어댑터 소유 데이터) + `orchestrate_project.py run_and_map` 배선(기존 `[STOP]`/`[PENDING-GATES]`·`stop-signal.json` 바이트 보존 후 렌더 가법·방어). §3.2 확정 갱신·§7 OQ-PO-B1·B5 해소 갱신(B2~B4 무변경). 신규 테스트: `test_render_gates.py`·`test_orchestrator.py` OQ-PO-B5 6케이스·`test_orchestrate_project.py` 렌더 회귀 1건. **05 계약 본문·gates.py 어휘·§3 게이트 어휘·PO-INV·Frozen 무접촉(재정의 0)·`orchestration/framework/**` provider 토큰 0.**
- **2026-07-18 (오케스트레이션 → 실 프로젝트 배선 수정 트랙).** 코드화된 오케스트레이터 엔진이 실 소비 프로젝트를 정석 구동하도록 배선. 신설(전부 `orchestration/adapters/claude/`·중립 `orchestration/framework/`·`uahf/` 무수정 import): `contract_to_graph.py`(Contract→초기 그래프 컴파일러)·`orchestrate_project.py`(프로덕션 런처)·`resolve_gate.py`(게이트 브리지 resolver). §5.7 신설(tms-system Contract v2 실 run). §7 OQ-PO-B3 해소(브리지 물리 형태 = exit2+stop-signal→표면화→resolve_gate append→resume)·OQ-PO-B4 해소(제안·승격 사이클·production·구현 resume defer)·OQ-PO-B5 신설. 공동 도입: 상위 규약 F2(구현 = Run 조율/단위 실행 2층 구분·`.claude/CLAUDE.md`·`.claude/AGENT.md`)·F1 물리 발화(`/uaf-implement` = `.claude/commands/uaf-implement.md`). Advisor 승인 + 사용자 게이트(smoke 실증 후 기록). **05 계약 본문·gates.py·§3 게이트 어휘·기존 §행·PO-INV 무변(재정의 0)·Frozen 무접촉.**
