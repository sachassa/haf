# orchestration/adapters/claude/project-orchestration-binding — Claude Project Orchestration Adapter 바인딩

작성일: 2026-07-13
상태: 05 계약(§3.3 Gate Policy·§3.5 Model Selection·§3.6 Artifact Record·§2.2 게이트 큐)의 claude 환경 물리 실현 매핑 — 게이트 큐 제시 채널(§3)·Model Selection 실값 매핑·OQ-SH-4 해소(§4)·직렬화·capability→물리 호출 매핑·run 데이터 백엔드·AgentSpec 실값 레지스트리·Artifact Record 직렬화(§5) 확정. 축소판 종단 dogfooding E2E(시나리오 j)로 실증.
상위 규약: AGENT.md
근거 정본: `orchestration/specs/05-project-orchestration.md`(S1 확정 — 특히 §2.2 게이트 큐 파생 뷰·§3.3 Gate Policy·§3.5 Model Selection·§3.6 Artifact Record·§5 Adapter 바인딩 지점) · `orchestration/framework/orchestrator/gates.py`(중립 게이트 평가기 — `pending_gates`·게이트 이벤트 필드 관례·해소 적격성·`gate_policy_schema.json`) · `orchestration/framework/orchestrator/orchestrator.py`(`_process_gates`·`OrchestrationResult.pending_gates`·`stop_reason="gate"`) · `uahf/specs/03-loop.md` §3.1-D·§3.2-A(무수정 재사용하는 개입 조건·이벤트 10필드) · `uahf/framework/adapters/claude/step-hosting-binding.md`(자매 바인딩·문서 관례 선행 표본·§2 상속분 소재) · `uahf/framework/adapters/claude/loop-binding.md`·`verifier-binding.md`(사람 개입 채널·역할 디스패치 선례) · `uahf/framework/core/structure.md` §4·§5 · `uahf/specs/00-glossary.md`. 계약은 § 포인터·심볼 참조로만 인용하며 재정의하지 않는다.

---

## §0. 이 문서의 위치와 정본 경계

- **바인딩 대상 정본 = `orchestration/specs/05-project-orchestration.md`(§2.2·§3.3·§3.5·§3.6·§5)와 `orchestration/framework/orchestrator/gates.py`.** 이 문서는 그 계약의 **claude 환경 실현 매핑**이며 계약 요소(gateKind 5종·심각도 전순서·게이트 단조성·해소 적격성·게이트 이벤트 필드 관례)를 재정의·확장하지 않는다. 05 §5가 "게이트 큐 제시 채널·직렬화 형식·capability→물리 호출 매핑·run 데이터 백엔드 경로·정책 실값은 Adapter Binding 문서 소관"이라며 미룬 지점이 확정되는 자리다.
- **격리 지점의 방향 반전(C-3 비적용).** 중립 경계(`orchestration/framework/orchestrator/`·05 본문)는 특정 AI·provider·실행 옵션 토큰이 0건이어야 한다(PO-INV 8). 이 문서는 그 **반대편**이다 — 구체 토큰(`claude` CLI·세션 표면·종료 코드·물리 경로)의 사용이 허용되며 그 격리가 이 경계의 존재 이유다(structure.md §2·§5·자매 바인딩 §0 동형).
- **범위.** §3(게이트 큐 제시 채널·해소 물리 관례)·§4(Model Selection 실값 매핑·OQ-SH-4 해소)·§5(직렬화·capability→물리 호출 매핑·run 데이터 백엔드·AgentSpec 실값 레지스트리·Artifact Record 직렬화·Run 관측 계약)를 확정하고, 물리 실측 상태는 §6이 대조한다(L-07). 미해소분은 §7 OQ로 남긴다.
- **창설 금지.** 05 §3.3·§5·gates.py를 넘어서는 새 바인딩 계약·새 gateKind·새 상태·새 개입 조건·새 이벤트 필드를 만들지 않는다. 게이트 이벤트는 03 §3.2-A 10필드 무수정 재사용이며 용어는 `uahf/specs/00-glossary.md` 정본만 쓴다("게이트 큐"·"제시 채널"·"정지 게이트"는 05·gates.py의 서술 라벨).

---

## §2. 상속·인용하는 확정분 (step-hosting-binding v1.5 Baseline)

게이트 축의 물리 채널은 자매 `step-hosting-binding.md` 가 이미 확정한 다음을 **상속·인용**한다(중복 확정 0):

| 항목 | 소재(정본) | 게이트 축에서의 의미 |
|---|---|---|
| 물리 정지 신호 = 프로세스 종료 코드 **2** | step-hosting-binding §5.3 | 정지 게이트(`escalation_required`/`user_decision_required`)로 `_process_gates` 가 `status="stopped"` 를 반환할 때, orchestration 런처는 종료 코드 2("사람/상위 개입 대기")로 종료한다. 게이트 정지도 Step Host 의 Escalated 정지와 같은 신호를 쓴다(신설 0). |
| Autonomy → CLI 권한 플래그 매핑(권한 플래그 문자열의 유일 허용 소재 = step-hosting-binding.md §0·§4.2 — 본 문서는 문자열을 재기재하지 않고 그 § 을 가리킨다) | step-hosting-binding §0·§4.2 | **게이트 등급 분리(불가침).** 이 매핑은 도구 실행 승인 프롬프트 축만 제어하며 게이트 축과 **직교**한다(05 §3.3·PO-INV 4). 최상위 autonomy 등급에서도 5종 게이트는 전부 작동하고 정지 게이트는 `stopped` 정지로 보존된다 — orchestrator 의 게이트 **결정** 로직(gateKind 평가·must_stop·해소 적격성)은 `self.policy`(autonomy) 를 참조하지 않는다(서브단위 실행에는 동일 autonomy 전달만 — 중립 코드가 소유하는 강제). 권한 생략 플래그는 claude 세션(도구 승인) 경계에만 적용되고 게이트 정지를 우회하지 못한다. |
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
- **표면 문법·렌더 템플릿 — 확정.** 최종 렌더 문법은 `orchestration/adapters/claude/render_gates.py`(형태 B·결정적·LLM 0·읽기 전용)가 소유하며, 위 구조 제안 bullet을 항목당 블록으로 물리화한다. 계약:
  - **라벨 표**(`user_decision_required`→"사용자 결정 대기(확정 권위)"·`escalation_required`→"Advisor/사람 해소 대기") = **어댑터 소유 데이터**(모듈 상단 상수 dict). 다국어·문면 조정은 이 표 교체가 확장점이다(정책-as-데이터 동형·렌더 로직 본문 무변경).
  - **진리원천 = `pending_gates(events, policy)` 파생 뷰.** `stop-signal.json`에 의존하지 않고 원장(`events.jsonl` + `gate_policy.json`)에서 직접 파생하므로 일부 게이트만 해소된 뒤 재렌더해도 정확하다(해소 이벤트 append 시 파생 뷰가 자동 제외).
  - **해소 명령·적격 actor는 정책 데이터 파생**(하드코딩 0). 항목별 해소 명령에는 그 게이트의 `--gate-id <gate_id>`가 채워지며(무지목 다중 호출은 §3.4가 차단하므로 단일·다중 어느 상황에서도 복사해 그대로 실행된다), 값이 셸 안전 문자 집합을 벗어나면 큰따옴표로 인용한다(결정적 규칙).
  - **출력 경로 2종.** 런처(`orchestrate_project.py run_and_map`)가 정지 시 기존 `[STOP]`/`[PENDING-GATES]` 라인·`stop-signal.json`을 바이트 보존한 뒤 이 렌더를 재사용해 자동 출력하고(렌더 실패는 정지 신호를 깨지 않는 부가 표면), 주 세션 Advisor는 `render_gates.py <run_dir>`로 수동 재렌더한다. `--json` = 구조화 출력(원 필드 + label + eligible_resolvers + resolve_command). **원장 무변경(읽기 전용)** — 어떤 파일도 쓰지 않는다.

### §3.3 해소 응답 → 게이트 해소 이벤트 append 물리 관례

- **해소는 이벤트 append 로만 이뤄진다.** 사용자·Advisor 의 해소 응답은 gates.py 의 `append_gate_resolution(log, gate_id, gateKind, actor=<해소자>)` 로 run 이벤트 로그에 append 된다(mutable 상태 갱신 0). 다음 재기동 시 `_process_gates` 가 그 해소 이벤트를 파생 판정(`is_resolved`)해 통과시킨다(결정적 재개).
- **actor 매핑(적격성의 물리 실현).** 해소 이벤트의 `actor` 필드가 적격성을 결정한다(gates.py `is_eligible_resolver`·정책 데이터 `userActorClass`/`escalationResolvers`). 이 환경의 매핑:

  | gateKind | 적격 해소 actor(이 환경) | 물리 관례 |
  |---|---|---|
  | `user_decision_required` | 사용자 본인의 응답 — actor = 정책 `userActorClass`(기본 `human`, 03 §3.2-A actor 어휘) | 사용자가 Claude Code 세션에서 결정을 내리면 그 응답을 actor=`human` 해소 이벤트로 append. **Advisor 역할·서브에이전트의 해소 시도는 무효**(gates.py 가 파생 뷰에 여전히 pending 으로 남김 — 확정 권위 보존·UAF-INV ⑤). |
  | `escalation_required` | actor ∈ 정책 `escalationResolvers`(기본 `Advisor`·`human`) | Advisor 역할(주 세션) 또는 사용자가 해소. actor=`Advisor` 또는 `human` 해소 이벤트로 append. |

- **부적격 해소의 물리 무효.** 부적격 actor 로 append 된 해소 이벤트도 로그에 남지만(append-only·은폐 0), `is_resolved` 가 적격성 판정에서 배제하므로 게이트는 여전히 pending 이다. 이는 코드가 소유하는 강제이며 제시 채널이 우회할 수 없다.
- **조건부 승인의 하류 전달 — `--response` 는 기록 전용이 아니다.** **구조 게이트(`user_decision_required`) 해소 시 비공백 `--response` 는 승격되는 모든 task 의 `delegation.context` 에 조건 항목으로 주입된다**(`resolve_gate.build_promotion_payloads`). 조건은 승인의 일부이므로 원장에만 남고 실행 단위에 닿지 않는 침묵 탈락을 허용하지 않는다.
  - **문면(결정적).** `[게이트 조건 — <gate_id> 해소(actor=<actor>)] <response>` 단일 문자열 항목. `gate_id`·`actor` 로 provenance 이벤트와 상호 추적하며 **타임스탬프를 넣지 않는다**(시각은 이벤트 소유·payload 는 결정적 — 같은 두 원장 재생 → 같은 바이트).
  - **원장 분리 보존.** `impl-plan.json`(원 산출)은 바이트 무변조, 조건 **원문**은 provenance 이벤트(`gate-resolution-provenance`·`ref.response`) 소유, 주입본은 revision payload(하류 소비 뷰)에만 실린다.
  - **적용 범위 = 승격 전 task 균일.** task 별 조건 라우팅은 도입하지 않는다(응답이 단일 원문이라 분배 근거 0) — 하류 단위가 자기에게 해당하는 조건을 스스로 식별한다(브리프 자족 원칙).
  - **타입 규칙·fail-closed.** `context` 가 리스트면 사본에 append, 문자열이면 `[원문, 조건]` 으로 승격, **부재/`null`이면 `[조건]` 신설**. 그 외 형(객체 등)은 조건을 담을 곳이 없으므로 **비영 종료·원장 무오염**으로 차단한다. 주입 payload 선구성은 **어떤 원장 append 보다 앞서** 수행된다(검증-먼저 패턴).
  - **관측 라인 2종.** 주입 시 `[CONDITION]` 이 주입 건수·원문 출처(provenance 이벤트)를 명시하고, context 부재로 신설한 단위는 `[CONDITION-NOTE]` 에 **id 로 열거**된다 — 조건부 승인이 별개 결함(위임 context 누락)을 가리지 않게 하는 표면화이며 **차단이 아니다**(rc 무변). 응답이 공백(기본)이면 주입 0·두 라인 없음 = 종전 거동 바이트 동일.
  - **하류 도달 경로.** 승격 payload → fold(`_copy_task`) → `Step.from_dict` → `assemble_bundle` 의 `memory_material`(Worker fresh-context 번들) · CP2 `verify_bundle` 의 `step_contract.delegation`(Verifier). escalation 게이트의 `--response` 는 해소 이벤트 ref 동봉·재작업 지시 전파 경로다(§3.4).
- **해소 어휘의 현행 형태(인용).** orchestration 해소 어휘는 재시도 예산 비계수를 이미 충족한다 — `append_gate_resolution`(03 10필드 재사용·`ref.kind=gate-resolved`·outcome=pass·retry_count=0)은 step 재시도 예산(`outcome=fail` 계수)을 소모하지 않는다(§7 OQ-PO-B2 해소). UAHF step-host 층의 해소=fail 계수 결합(OQ-SH-5·step-hosting-binding §7)은 무수정 경계상 별도 트랙 소관이며, 해소 취소(revoke) 어휘는 OQ-PO-B6 저순위 이월이다.

### §3.4 실행 에스컬레이션(Escalated 정지)의 해소 채널

§3.3 은 `_process_gates` 가 발화한 정지 게이트(단위 경계)의 해소를 다룬다. 이 절은 그 앞단 —
**Step Host 가 실행 중 낸 Escalated 정지**(재시도 한도 초과·차단 선언·SH-INV-4)의 해소를
같은 채널로 물리화한다(경위 = git 앵커 90ca19c).

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
- **해소 대상 지목 `--gate-id`.** `resolve_gate.py <run_dir> --gate-kind escalation
  --actor <Advisor|human> --gate-id <gate_id>` 로 해소 대상 게이트를 **특정 지목**한다. 같은
  gateKind 게이트가 **2건 이상 동시에 pending** 이면 지목이 필수다 — 무지목 호출은 후보
  (`gate_id`·`target`·`since`)를 열거하고 **원장 무변경으로 비영 종료**한다(첫 매칭 침묵 선택 금지).
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
- **레거시 run·플래그·다중 escalation.** 좌표 없이 Escalated 로 멈춰 있던 기존 run 도 `--resume`
  1회로 요구 이벤트가 생성되어(정지 유지·재실행 0) 위 절차를 쓸 수 있다. `--retry-limit`
  override 는 `--resume` 에서도 `config.json` 에 반영되나(이전→새 값 출력) 되돌림이 한도와
  무관하게 추가 시도 1회를 부여하므로 해소의 전제가 아니다. 여러 단위가 동시에 Escalated 이면
  한 건의 해소는 그 단위에 되돌림을 append 하되 나머지가 Escalated 로 남아 Host 가 정지하므로
  **추가 디스패치는 나머지 해소 이후**다(SH-INV-4 보존의 귀결·되돌림은 원장에 남아 다음 재개가 소비).

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

- **OQ-SH-4 — 해소됨.** step-hosting-binding §7 OQ-SH-4(중립 Host 가 CP2 를 `model=step.model` 로 디스패치해 검증 전용 모델 독립 지정 불가)는 중립 Host 최소 개정으로 해소되었다 — `StepHost` 생성자 `cp2_model` 파라미터(기본 `None`)·`_dispatch_cp2` 의 CP2 모델을 `self.cp2_model if self.cp2_model is not None else step.model` 로 변경(1개소)·`config_schema.json` 선택 필드 `cp2_model` 추가. 기본값 `None` 시 기존 거동 바이트 동일 보존·계약 무변(02 §4 슬롯 의미)·중립 Host 는 슬롯 값을 해석하지 않는다(SH-INV-8 동형). step-hosting-binding §7 OQ-SH-4 문면 자체의 상태 갱신은 그 문서 소관이며 본 문서가 대신 갱신하지 않는다(무수정 경계 — 05 §6). `uahf/` 접촉 = `host.py` 1개소 + `config_schema.json` + step-host 테스트뿐이다(§6 실측 대조).

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

`orchestration-data/e2e/` 드라이버(비프로덕션)가 실 claude CLI headless(haiku·5 세션)로 종단 흐름을 실증했다 — 설계 단위 실행(Worker+CP2) → `user_decision` 게이트 물리 정지(exit 2·pending_gates 기록) → 시뮬레이션 라벨을 append-only 로그(`annotation::sim`)·`gate-resolution-record.json` 에 명시 기록한 뒤 사용자 actor(`human`) 해소 이벤트 append(L-07 실 사용자 위장 금지) → 구현 단위 revision(basis.gateEventRef) → fresh 프로세스 재개로 구현 단위 실행·`review_required` 추가 리뷰(Verifier)·완주(exit 0). deterministic resume replay(2회 stdout 동일)·최종 레지스트리 approvalState 파생(user_approved/verified)·실 세션 stdout·argv 캡처(`logs/invoke-*.json`·은폐 0·O5)까지 실 데이터로 남았다. run 데이터 = `runs/orch-j-e2e/@cd9247b`(아카이브·ARCHIVE.md 원장).

### §5.7 프로덕션 실 run — 임의 소비 프로젝트 구동 (배선 수정 트랙)

§5.6이 비프로덕션 드라이버(시뮬 사용자 게이트·픽스처 구현 제안)인 것과 달리, **프로덕션 런처**가 임의 소비 프로젝트를 실 claude CLI headless 로 구동하는 경로다. 신설 어댑터 3종(전부 `orchestration/adapters/claude/`·중립 `orchestration/framework/`·`uahf/` 무수정 import 재사용):

- **`contract_to_graph.py`** — Contract vN(파일명 버전 최대·내용 파싱 0) → 초기 Work Graph(단일 seed proposal 단위) + gate_policy(proposal→user_decision·implementation→review·milestone→approval) + config 결정적 컴파일. seed 프롬프트가 런타임 실 LLM 에 Phase 분해(implementation N + milestone 1·DAG 종단·오프라인 안전 done AC)를 위임(05 §3.1 "고정 파이프라인 하드코딩 금지").
- **`orchestrate_project.py`** — `<project_root>`를 컴파일→run_dir 물리화(소비 프로젝트 워크스페이스 무삭제·RUNS_DIR 직속 삭제가드)→중립 `build_orchestrator_k` 무수정 재사용→`orch.run()`→exit-code 매핑(§2 종료 코드 2 상속). `--model`(seed 티어)·`--policy`(기본 `auto_approve` — headless 쓰기·게이트와 직교) override.
- **`resolve_gate.py`** — 게이트 해소: impl-plan 어댑터 검증(F4 계약 수용 = `unitType∈{implementation,milestone}`·milestone≥1·implementation≥1·milestone DAG 종단·`resolve_w` 구조 헬퍼 동일 강도 재사용) **먼저**(실패 시 원장 무변경) → `append_gate_resolution(actor=…)` → 각 구현 task `accept_revision(task_added·basis.gateEventRef)`.

**실 run 실측(첫 프로덕션 run 데이터 = `runs/orch-tms-phase1-smoke/` — 소비 프로젝트 트랙 종료로 앵커 전환 `4934bc8`·ARCHIVE.md):** Stage A = seed proposal 단위(실 LLM)가 Contract + solution-design 정독 후 `impl-plan.json`(implementation N + milestone 1·DAG 종단) 산출 → CP2(`cp2-pass` 이벤트·상시 하한) → `user_decision_required` 게이트 물리 정지(exit 2·`logs/stop-signal.json` pending_gates 기록) → `resolve_gate.py` 가 impl-plan 어댑터 검증 통과 후 실 사용자(actor=`human`·simulated=false) 해소 이벤트 append → 각 구현 task `task_added` revision(basis.proposingStepRef·gateEventRef) 승격 → active_graph fold·ready_set = 선행 impl 단위(결정적 재개 준비).

**정직 대조(L-07).** 이 경로는 §5.6 픽스처를 넘어선 **실 LLM 제안 step + 실 사용자 게이트 해소**다(§7 OQ-PO-B4). milestone 단위(→`approval_required`·CP3)의 물리 CP3 정지·해소는 구현 단위 resume 시 발화하며 첫 run 에서는 gate_policy 파생 평가로 도달성만 확인했다(라이브 CP3 발화·실 코드 산출 = 후속 resume 소관). e2e 드라이버(§5.3)는 비프로덕션이며 이 프로덕션 런처가 그 상위 발화 경로다.

### §5.8 Run 관측 계약 — heartbeat · failure record · 종료 코드

§5.3 run 데이터 레이아웃의 `logs/`에 **런처 소유 관측 산출 2종**을 가법한다. 기존 `logs/` 항목(`invoke-*.json`·`stop-signal.json`·`gate-resolution-record.json`·`host.pid`)과 §2 종료 코드 매핑은 무변경이며 아래는 그 위에 얹는 절이다(재정의 0). 생산자는 `orchestration/adapters/claude/orchestrate_project.py` 하나뿐이고 중립 코드(`orchestration/framework/**`)·`uahf/**`는 무촉이다. hang(무한대기)은 종료 이벤트가 원리적으로 발생하지 않고 엔진 stdout 은 버퍼링돼 실행 중 비어 있으므로, 정체 판정 근거는 **진행의 능동적 증거**(a)여야 한다.

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

**(e) 슬러그 길이 상한.** 컴파일러 `_slug`(seed unit id)와 런처 `slugify_run_id`(run_id)가 **공통 규칙**(`contract_to_graph.fold_slug`)을 쓴다 — 정규화 결과가 48자를 넘으면 `앞 48자 + "-" + sha256(원문)[:8]`(최대 57자)로 접는다. 48자 이하는 바이트 동일이라 기존 run 디렉터리·unit id는 하위호환된다. 근거 = unit id가 `steps/<unitId>.json`·`logs/invoke-NN-<Role>-<unitId>.json` 파일명이 되므로 상한이 없으면 (i) 긴 ASCII `--phase`에서 Windows 경로 한계 크래시·(ii) git `Filename too long`으로 run 원장을 커밋할 수 없다(실측 경위 = git 앵커 90ca19c). 두 함수가 서로 다른 상한을 쓰면 `--resume`의 슬러그 재파생이 실물 run_dir과 어긋나므로 규칙을 하나로 둔다.

**(f) 문서 접합부.** `.claude/commands/uaf-implement.md` §2 재개 예시 = `--resume --run-id <run_id>` 형태이며 위 종료 코드 표를 싣는다(`--resume`만 표기하는 예시는 슬러그 재파생 계약과 어긋나 `--run-id`를 준 run에서 실패한다).

**(g) per-unit timeout — 단위별 실행 예산**

전역 `timeout` 하나(§4 config `timeout` → `Orchestrator.timeout`)는 규모가 크게 다른 단위를 같은 예산에 묶으므로, 이를 **단위 단위의 선택 값**으로 세분한다. 종료 코드 표(d)는 무변경이다. 로그 산출은 invoke 원장(`logs/invoke-*.json`)에 `timeout` 필드 **1개가 가법**된 것 외에는 무변경이다(기존 키·파일명 규칙·다른 원장 무변 — 아래 관측 행).

| 층 | 계약 |
|---|---|
| 스키마 | impl-plan task 의 **선택 키** `timeout`(11키 밖·12번째) = 실행 예산 **초 단위 양의 정수**. 부재 = 전역 fallback. `REQUIRED_TASK_KEYS` 11키는 무변(필수 승격 아님 — 기존 run·플랜 하위호환) |
| 검증 | `resolve_gate.validate_impl_plan_adapter` — 키가 있으면 양의 정수만 수용하고 그 외(bool·0·음수·실수·문자열)는 오류 목록에 올린다. 판정 불가는 통과가 아니다(fail-closed·원장 무오염 — 불량값이 `task_added` 로 승격되지 않는다) |
| 재기입 | 중립 엔진(`orchestrator.UnitTimeoutInvoker`) — `{단위 id: timeout}` 맵을 들고 `request.bundle["step_contract"]["id"]` 매칭 시 `dataclasses.replace` 로 `request.timeout` 을 재기입한다. 원본 request 무변조(순수)·비매칭은 원 객체 그대로·`__getattr__` 속성 투과(`HeartbeatInvoker` 선례 동형) |
| 관측 | 재기입된 **실효 예산**은 invoke 원장 `logs/invoke-*.json` 의 `timeout` 필드로 관측된다 — E2E 하네스 `LoggingClaudeInvoker._bundle_ctx` 가 `request.timeout` 을 캡처하고 `_write_log` entry 에 싣는다. `UnitTimeoutInvoker` 는 최외곽 래핑이라 로깅 래퍼가 받는 요청은 재기입 **후** 객체이므로, 이 필드가 곧 재기입 값의 원장 실증이다(비매칭 단위·미지정 단위는 전역 예산값·`null` 이 실린다). `uaf-verified:` 래핑 순서 = `orchestration/framework/orchestrator/orchestrator.py` `_effective_invoker` 정독 + 단위 테스트 실측(`orchestration-data/e2e/tests/test_t3_t4.py::InvokeLogTimeoutField` — 재기입 값 7200 이 원장에 실림·비매칭 시 전역 600 유지·원본 request 무변조), 검색 범위 = 해당 2파일 및 e2e 로깅 경로. 실 LLM run 원장 관측은 이 가법 이후 첫 run 에서 확인 대상이다 |
| 맵 원천 | `active_graph()` 파생 하나뿐(PO-INV 3 — 제2 진리원천 0). 유효값만 편입하고 불량값은 편입하지 않는다(차단은 검증 게이트 소유·래퍼는 기계 재기입만·판단 0) |
| 적용 범위 | 한 단위의 **exec·CP2·게이트 디스패치 3경로 전부**가 그 단위의 예산을 받는다(균일 규칙). `_effective_invoker()` 는 맵이 비어 있지 않을 때만 최외곽 래핑하고, `_dispatch_gate_step` 은 같은 맵으로 timeout 래핑만 경유한다(산출물 포집 래퍼를 게이트 경로에 새로 끼우지 않는다) |
| 거동 보존 | 맵 공집합(= `timeout` 을 쓴 단위 0)이면 **래핑 자체가 없다** — 기존 반환·기존 요청 객체 그대로다(`allocation=None`·`artifact_store=None` 패턴 동형). seed proposal 노드는 timeout 미부여(컴파일 시점에 단위 규모 정보가 없고 값을 발명하지 않는다) |
| Planner 지시 | `contract_to_graph._seed_prompt` 구현 task 구성 규칙에 선택 키 안내 1항(양의 정수·초·명백히 대형인 단위에만·미지정 = 전역 기본). `_done_ac` 는 11키만 검사하므로 무변 |

`uaf-verified:` 값이 실제 프로세스 예산에 닿는 경로 = `request.timeout` → 실 CLI invoker 의 subprocess timeout(`step-invoker/claude_invoker.py`) — 검색 범위 = orchestration 2트리 + uahf step-host/step-invoker 트리의 해당 지점 정독이며, **실 LLM run 관측은 아직 없다**(현 근거 = 오프라인 stub 통합·접합부 왕복 테스트까지).

**(h) 횡단 결함 검지 — `[REWORK-NOTE]` 관측 라인 + `sweep_units.py` 스윕 도구**

CP2 재작업은 **그 단위만의 결함 신호가 아니다** — 같은 오용이 동료 단위에 복제돼 있어도 각 단위의 done AC는 자기 산출만 보므로 통과한다. 이 항은 복제된 결함을 보이게 하는 장치이며 종료 코드 표(d)·기존 로그 산출·기존 종료 라인은 무변경이다.

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

**Planner 지시 짝.** `contract_to_graph._seed_prompt` milestone 규칙은 두 항을 싣는다 — (i) milestone done AC는 **단위 간 계약 정합 검사를 최소 1건 포함**한다(개별 파일 존재 나열만으로는 불충분·최소 1건은 둘 이상의 단위를 상호 대조. 오프라인 안전형 예 = 선행 `produces`↔후행 `consumes` 경로 상호 대조·모듈 경계 참조 무결·공유 계약 데이터 키 집합 일치) (ii) milestone task 문면에 **횡단 관점** 지시(한 단위에서 발견된 결함 패턴을 동료 단위에 같은 기준으로 대조하고 결과를 보고).

**미해소 이월(정직 구분).** hang 관측의 `current_unit`·`elapsed_s` 필드는 `request_hint` 하나로 축약했다(런처가 단위 경계를 소유하지 않으므로 요청에서 파생 가능한 값만 싣는다). 자동 되돌림(D-M3)은 위 경계 사유로 미도입 — 재심 좌표 = Verifier 구조화 verdict(`sweep_patterns` 필드) 도입 시.

### §5.9 경량 레인 원장 — form-A 수기 append 규약 (절차 비례화 트랙 W2-b·§ 번호 불이동·기존 (a)~(h) 무변)

경량(lightweight) 레인은 엔진 런처(`orchestrate_project.py`)를 구동하지 않고 **Advisor 직접 위임**으로 조율하는 레인이다. **원장 0건 금지는 두 레인 공통**이며(`.claude/AGENT.md` §Invariants), 경량 레인은 원장을 줄이지 않고 조율 주체만 바꾼다 — 엔진이 자동 append 하던 원장을 **form-A 수기 append** 로 남긴다. 신규 레코드 종류·신규 필드·신규 원장 포맷·신규 원장 루트·신규 검증기는 **0**이며 §5.1(직렬화)·§5.3(배치)·§5.5(파생 뷰)를 그대로 상속한다(재정의 0).

**(a) 배치 경로.** `uahf/framework/adapters/claude/orchestration-data/runs/<run-id>-lite/` — §5.3 표준 run 트리의 **형제**이고 신규 루트는 0이다. `-lite` 접미가 레인 표기이며, `config.json` 의 `run_id` 는 디렉터리명(접미 포함)과 **같은 문자열**이다(러너 리포트 파일명·디렉터리 조회 일치).

**(b) 파일 집합 — 필수 7 · 부재 4(엔진 호스팅 산출)**

| 파일 | 경량 레인 | 근거 |
|---|---|---|
| `config.json`·`graph.json`·`gate_policy.json` | 필수 | §5.1·§5.3 동형(정책·초기 그래프 없이는 게이트 파생·fold 가 성립하지 않는다) |
| `events.jsonl`·`revisions.jsonl`·`artifacts.jsonl` | 필수 | 이중 원장 + 선언 원장(§5.1). 승격 0인 run 은 `revisions.jsonl` 0행이 허용된다 |
| `logs/gate-resolution-record.json` | 필수 | `basis.gateEventRef` 가 가리키는 실파일 — (d)·(f) |
| `steps/<id>.json`·`workspace/`·`logs/invoke-*.json`·`logs/heartbeat.json` | 부재(0) | 엔진 호스팅·런처 관측 산출이므로 경량 레인에 존재하지 않는다. 러너는 대응 축을 `skip` 으로 처리한다 |

**(c) 최소 필드 = 닫힌 스키마가 요구하는 것 그대로**

- **RevisionEvent**(`revisions.jsonl` — `revision_schema.json`): `revisionSeq`(1부터 단조)·`kind`(`task_added`\|`dependency_added`\|`task_superseded` — 어휘 신설 0)·`payload`(07 §3.2-B Task 전 필드·`delegation` 8필드)·`basis{proposingStepRef,gateEventRef}`.
- **Artifact 선언**(`artifacts.jsonl`): `artifactId`·`version`·`supersedes`·`derivedFrom`·`producedBy`·`location`·`contentHash` 7키. **`approvalState` 를 기입하지 않는다**(파생 뷰·PO-INV 7). 선언 키 집합은 `artifact_record_schema.json` 의 property 집합의 부분집합이며, 스키마 전 필드 검증 대상은 `derive_registry` 가 낸 **파생 ArtifactRecord** 다.
- **이벤트**: 03 §3.2-A 10필드 무수정(§5.1·§2 상속). `ref.kind` 는 러너 관측 어휘 안에서만 쓴다 — (i).

**(d) `basis` 두 참조의 경량 레인 형태 = `<경로>#<프래그먼트>`**

| 필드 | 경로 해석 기준 | 프래그먼트 | 추가 조건 |
|---|---|---|---|
| `proposingStepRef` | **리포 루트** | 위임 브리프 문서 내 절 식별 문자열 | 경로 실재 1 · 프래그먼트가 그 파일 본문에 실재 1 |
| `gateEventRef` | **run 디렉터리** | `gate_id` | 경로 실재 1 · 프래그먼트가 게이트 기록 본문과 `events.jsonl` 게이트 이벤트 `ref.gate_id` 양쪽에 문자 동일로 실재 1 |

- 경량 레인에는 제안 step 을 호스팅한 엔진 단위가 없으므로 `proposingStepRef` 는 **분해 초안 실파일**을 가리킨다. 스키마는 두 필드를 `string`("참조")으로만 규정하므로 이 형태는 스키마 위반이 아니다(개정 0).
- `gateEventRef.rsplit("#", 1)[-1]` 로 게이트 좌표(`gate_id`)가 **결정적으로 복원**된다.
- 05 §3.2 결정성 조건 ①(게이트 통과 이벤트가 append 된 뒤에만 그 revision 을 append)은 수기 경로에도 적용된다. 그 검사는 (h) 러너가 담당한다.
- **엔진 재개 비호환은 설계상 의도다.** 엔진 `orchestrator._gate_event_exists` 는 `ref.gate_id == basis.gateEventRef` 문자 동일을 요구하므로 복합 형태 참조는 엔진 fold 필터를 통과하지 않는다. 경량 레인은 엔진을 구동하지 않는 것이 전제이므로 `--resume` 대상이 아니며, 표준 레인으로 **승급**할 때는 새 표준 run 을 개시하고 복원된 `gate_id` 로 계보를 인용한다.

**(e) lane 표기 = 기존 필드의 문면(필드 신설 0).** 어휘는 `"standard"` \| `"lightweight"` **2값**이고 세 번째 값은 없다(미선언은 `standard` 로 귀결·fail-closed). override 사유 필드명은 `laneOverrideReason` 이며 override 부재 시 `null` 이다. 원장 문면 3지점 = `graph.json` 의 `goal` · revision `payload.delegation.context` 의 1행(`lane=<값> · laneOverrideReason=<null|사유>`) · `logs/gate-resolution-record.json` 의 `lane`·`laneOverrideReason` 키. **어휘 정본은 레인 판별 로더(절차 비례화 트랙 W2-a)의 방출값**이며 본 절은 소비 측이다(재정의 0).

**(f) 게이트 기록(form-A) 필드 12종.** `gate_id`·`gateKind`·`runId`·`presentedBy`·`scopedQuestion`·`resolvedByActor`·`response`·`resolutionEventAt`·`lane`·`laneOverrideReason`·`simulated`·`note`. 이 기록은 **좌표·문면 보존용**이며 해소 **자격** 판정은 `gates.py`(`is_eligible_resolver`/`is_resolved`)가 코드로 소유한다 — 수기 경로가 그 판정을 우회하지 않는다(게이트 불가침).

**(g) `approvalState` 3전이 전부 파생(직접 기입 0).** `verified`(대상 step 의 CP2 Pass 이벤트) → `approved`(그 단위 게이트의 CP3 승인 마커 `verdict == Pass`) → `user_approved`(`user_decision_required` 게이트가 적격 사용자 actor 로 해소). 경량 레인도 §5.5 사다리를 그대로 쓰고 `derive_registry(선언, 이벤트, gate_id_for=…, gate_policy=…)` 로 파생한다. 게이트 좌표 규약 = `gate-unit-<stepId>`(표준 레인 동형). `gate_id_for` 를 주지 않으면 게이트 축(`approved`·`user_approved`)은 파생되지 않는다 — 등급이 이벤트 실재에 의존한다는 증거다.

**(h) 강제 지점 = 기존 결정적 러너(신설 0).** 경량 레인 종결 조건에 **`python verify_run.py <run-dir>` findings 0 · exit 0** 을 둔다. 적용 축 = (a) 원장 위생(전역 `at` 1..N 연속·cycle 별 `seq` 단조·게이트 순서 `required`→`provenance`→`resolved`·관측 어휘·simulated 라벨 정직성) · (b) revision 무결(중립 `validate_revision`/`fold` progressive) · (d) delegation 참조형 · (e) 계수 정합. **한계(정직 표기)**: 러너는 원장 파일이 부재·0행이면 그 축을 `skip` 으로 떨어뜨리므로 `findings 0` 단독은 원장 실재를 증명하지 않는다 — 종결 조건은 `findings 0` **그리고** `events.jsonl`·`artifacts.jsonl` 비공집합(승격이 있으면 `revisions.jsonl` 도 비공집합)을 함께 요구한다. 이것이 "경량 레인에서도 원장 0건 금지"의 기계 강제다.

**(i) 관측 어휘 실측 주의 — provenance 표기 2종.** 경량 레인은 provenance 이벤트에 `ref.kind = "user-resolution-provenance"` 를 쓴다(러너 관측 어휘 화이트리스트에 실재하는 표기). 프로덕션 resolver 가 append 하는 `"gate-resolution-provenance"`(§3.3·`resolve_gate.py`)는 그 화이트리스트에 **부재**하므로, 표준 레인 run 에 이 러너를 먹이면 축 (a)가 어휘 위반 finding 을 낸다. 이는 표준 레인 측 정합 결함이며 경량 레인 소관이 아니다 — §7 **OQ-PO-B7** 로 등재한다(러너·resolver 어느 쪽도 이 판에서 수정하지 않는다).

**(j) 수명 등급·정직 라벨.** 경량 run 원장 등급 = **ephemeral**(재실행으로 재생성 — `docs/artifact-lifecycle-policy.md` §2). 표본·픽스처는 `events.jsonl` 의 `simulation-annotation` 이벤트(`ref.simulated = true`)와 게이트 기록의 `simulated` 키로 **기계 판독 가능하게** 라벨한다(L-07 — 실 발화와 형태 표본을 구분한다. 해소 이벤트 자체에 `actor=human` + `simulated=true` 를 같이 두지 않는다 — 러너 (a)가 정직성 모순으로 판정한다). ephemeral 산출물의 작업 트리 경로는 판정 근거로 인용하지 않으며(같은 정책 §4) 실증 기록은 트랙 원장·완료 보고에 남긴다.

**(k) 물리화·점검 드라이버(비프로덕션).** `orchestration-data/e2e/setup_lite.py`(stdlib only·LLM 0·네트워크 0·결정적) 가 경량 원장 표본을 물리화하고 5축을 결정적으로 점검한다 — 스키마(닫힌 스키마 2종 판독 검증·선택 `jsonschema` 동반) · `basis` 왕복 · `approvalState` 파생 · 빌더 결정성(재빌드 byte 동일) · 게이트 순서 **음성 대조**(위반 표본에서 러너 findings 비공집합·exit 1). 삭제는 `runs/` 직속 `-lite` 디렉터리에만 허용한다(오삭제 가드 — `setup_m.py` 동형). `e2e/` = 비프로덕션 경계(§5.3 말미 동형).

`uaf-verified:` 본 절의 사실 주장 근거 = (i) 닫힌 스키마 2종·`revision.py`·`artifacts.py`·`gates.py`·`verify_run.py` 좌표 직독 (ii) `setup_lite.py` 5축 실행 로그 (iii) 표본 run 에 대한 `verify_run.py` 실행(status=pass·fail 0·skip 1). **스윕 범위** = 그 6개 코드/스키마 파일과 표본 원장 실물이며, 그 밖(표준 레인 프로덕션 run 전수 재검증·`resolve_gate.py` 어휘 정합 수정)은 이 판의 범위 밖이고 (i)에서 OQ 로 남긴다.

---

## §6. 실측 대조 (L-07)

- **중립 코드 실재.** `orchestration/framework/orchestrator/`에 `artifacts.py`·`artifact_record_schema.json`·`tests/`가 실재하고 `orchestrator.py`가 선택 `artifact_store`·투명 포집 래퍼·`artifact_registry()`/`resolve_references()` 파생 메서드를 갖는다(`artifact_store=None` 기본 시 종전 거동 바이트 동일 보존). 자체 테스트는 표준 라이브러리 `unittest` 만으로 통과한다.
- **PO-INV 8(중립성).** `orchestration/framework/orchestrator/`의 코드·스키마·테스트에 provider·모델·CLI 옵션 토큰 0건이다(스윕 범위 = 그 디렉터리의 `.py`·`.json` 전 파일 grep). approvalState 어휘(draft/verified/approved/user_approved)·verdict `Pass` 는 05 §3.6·06 계약 어휘다. 구체 토큰(`claude`·모델 별칭·`--model`·권한 플래그)은 이 바인딩 문서·step-invoker 코드·`orchestration-data/e2e/` 드라이버(격리 지점)에만 둔다.
- **`uahf/` 접촉.** (i) `uahf/framework/loop/step-host/host.py` `_dispatch_cp2` 1개소(§4.3·`cp2_model=None` 시 기존 거동). (ii) `uahf/framework/adapters/claude/orchestration-data/` 신설(run 데이터 백엔드·E2E 드라이버 — 2차 산출물 디커플링 트랙까지 `uahf/` 잔류). 그 외 `uahf/` 정본·중립 코드·append-only 데이터(discovery-data·solution-design-data·step-data·memory-data·loop-data)는 무촉이다(형상 관리 상태 조회로 확인).
- **정직 구분 (L-07).** §5.6 시나리오 j 의 사용자 게이트 해소·구현 단위 제안은 **드라이버 픽스처**이며 실 사용자·실 LLM 제안 step 이 아니다(`gate-resolution-record.json`·`annotation::sim` 이벤트에 명시). 그 run 의 실증 대상은 게이트 물리 정지·사용자 actor 적격성·revision 인과 사슬·deterministic 재개이며, 실 LLM 제안 + 실 사용자 해소는 §5.7 프로덕션 run 이 남긴다.

---

## §7. Open Questions (본 판 이월)

해소된 OQ 4건은 결론만 남긴다(경위·판정 근거 = git 앵커 90ca19c).

- **OQ-PO-B1 (게이트 큐 제시 표면 문법) — 해소.** 물리 형태 = `render_gates.py`(형태 B·결정적·읽기 전용). 계약 상세 = §3.2.
- **OQ-PO-B2 (해소 어휘 성숙) — 해소(2축 분리·엔진 코드 변경 0).** (1) 재시도 예산 비계수는 orchestration 엔진이 전용 어휘(`gate-resolved`/`outcome=pass`/`retry_count=0`)로 이미 충족한다 — OQ-SH-5 의 "해소=fail 계수 결합" 결함은 `outcome=fail` 을 재사용하는 UAHF step-host 층 국한이며 그 층의 해소는 무수정 경계상 별도 트랙(step-hosting-binding §7) 소관이다(§3.3 말미 인용). (2) 해소 취소(revoke)는 OQ-PO-B6 으로 재스코프·저순위 이월.
- **OQ-PO-B3 (headless 런처 ↔ 사용자 세션 제시 브리지) — 해소.** 브리지 = 종료 코드 2 + `logs/stop-signal.json`(pending_gates) 기록 → 주 세션 Advisor 표면화(§3.2 채널 분리 유지) → `resolve_gate.py` 해소 이벤트 append(적격성 = gates.py 코드 소유) → `--resume` 결정적 재개(원장 fold). §5.7 실 run 으로 실증.
- **OQ-PO-B4 (실 LLM 제안 step·비픽스처 run) — 해소.** §5.7 이 실 LLM 제안 step + 실 사용자 게이트 해소·revision 승격을 남겼다. 잔여 = 승격된 구현 단위의 resume 실 코드 산출(후속 트랙 이월).
- **OQ-PO-B5 (엔진 `accept_revision` 게이트-pass 재검증의 actor 미검사) — 해소.** `orchestrator._gate_event_exists`(→ `_event_grounds_gate`) 강화로 엔진 측 방어를 완성했다. 규칙: 매칭 pass 이벤트가 정지 게이트 해소로 자신을 선언하고(`ref.kind == REF_KIND_RESOLVED` **그리고** `ref.gateKind ∈ STOPPING_GATES`) `self.gate_policy is not None` 이면, 그 해소 actor 가 `gate_policy.is_eligible_resolver(gateKind, actor)` 로 적격일 때만 revision 을 근거지을 수 있다(05 §3.3 확정 권위 정합). 부적격 actor 의 pass 해소 이벤트는 로그에 남아도 승격 근거가 되지 못한다. **거동 보존 3면(불가침):** (a) 레거시 이벤트(`ref.kind == "gate"`·gateKind 부재) = 실재-만 검증 · (b) 비정지 gateKind gate-resolved 이벤트 = 실재-만 검증(`is_eligible_resolver` 는 비정지에 False 라 일괄 적용 시 rework 근거 패턴이 깨진다) · (c) `gate_policy is None` = 실재-만 검증. **적용 시점** = `accept_revision`(수용)과 `_grounded_revisions`(재개 fold 필터) 양쪽이며, 프로덕션 resolver 의 상류 append 거부와 함께 이중 방어를 이룬다.
- **OQ-PO-B7 (provenance `ref.kind` 표기 2종 — 미해소·실측 발견).** 프로덕션 resolver 는 `"gate-resolution-provenance"`(`resolve_gate.py`)를 append 하고 e2e 드라이버·검증 러너 화이트리스트는 `"user-resolution-provenance"`(`resolve_k/m/w.py`·`verify_run.py`)를 쓴다. 두 표기가 갈라져 있어 **표준 레인 프로덕션 run 에 `verify_run.py` 를 먹이면 축 (a)가 관측 어휘 위반 finding 을 낸다**(경량 레인 표본은 후자를 써서 통과한다 — §5.9 (i)). 해소 선택지 = (1) 러너 화이트리스트에 두 표기 병기 (2) resolver 표기를 화이트리스트 표기로 정렬(과거 run 원장은 append-only 이므로 소급 정정 불가 — 병기 없이는 기존 run 이 계속 발화한다). 어느 쪽도 W2-b 범위 밖이라 미수정으로 남긴다(러너·resolver 무촉).
- **OQ-PO-B6 (해소 취소 어휘 부재 — 저순위·미해소).** append-only 원장에서 오append 된 게이트 해소 이벤트를 되돌리는 전용 어휘·연산이 없다(실사용 오용 관측 0·투기적). 도입 시 필요 설계: 취소 actor 적격성(`is_eligible_resolver` 정합)·취소 후 게이트 재-pending 전이 의미·원장 fold 에서 취소가 선행 해소를 무효화하는 규칙(append-only 보존·보상 이벤트 형태). 현행 미도입 — 필요 관측 시 착수.

---

## §8. 개정 이력

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

