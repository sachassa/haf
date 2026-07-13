# framework/adapters/claude/project-orchestration-binding — Claude Project Orchestration Adapter 바인딩

작성일: 2026-07-13
상태: v1.6 Baseline (CP2 5단계 전건 첫 판정 Pass — S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0 · CP3 승인 · 사용자 승인 2026-07-13) — 게이트 큐 제시 채널(§3)·Model Selection 실값 매핑·OQ-SH-4 해소(§4)·직렬화·capability→물리 호출 매핑·run 데이터 백엔드·AgentSpec 실값 레지스트리 관례·Artifact Record 직렬화(§5) 확정. 축소판 종단 dogfooding E2E(시나리오 j) 실 CLI 5 세션으로 실증. 직전 기준선: S5 확정(CP2 판정 대기).
상위 규약: AGENT.md
근거 정본:

- `orchestration/specs/05-project-orchestration.md` (S1 확정) — Project Orchestration provider-중립 계약 정본. 본 문서가 물리 실현으로 인스턴스화하는 대상. 특히 **§3.3 Gate Policy**(5종 어휘·기존 계약 매핑·게이트 단조성·Autonomy 직교)·§2.2(게이트 큐 = `Escalated` 이벤트 + gateKind + scoped question 의 파생 뷰·headless·사용자 채널 분리)·§5(Adapter 바인딩 지점 — 게이트 큐 제시 채널 행). 재정의하지 않고 § 포인터로만 인용한다.
- `orchestration/framework/orchestrator/gates.py` (S3 신설 — 중립 게이트 평가기) — 본 문서가 제시 채널을 붙이는 중립 코드. `pending_gates(events, policy)` 파생 뷰·게이트 이벤트 필드 관례(`gate::<gate_id>` cycle 네임스페이스·ref 의 gate_id/gateKind/target/scoped_question·`append_gate_requirement`/`append_gate_resolution`)·해소 적격성(`is_resolved`·user_decision=사용자 actor 클래스만·escalation=허용 resolver 집합)·`gate_policy_schema.json`. 본 문서는 그 추상을 claude 실값으로 바인딩한다.
- `orchestration/framework/orchestrator/orchestrator.py` (S2·S3) — `_process_gates`(배치 종단 단위 경계 게이트 처리)·`OrchestrationResult.pending_gates`(정지 게이트 큐 반환)·정지 신호(`stop_reason="gate"`). 본 문서 §3 이 그 정지·재개의 물리 채널을 확정한다.
- `uahf/specs/03-loop.md` §3.1-D(사람 개입 5조건 — 코드 소유 하한의 정본)·§3.2-A(전이 이벤트 10필드 — actor 필드) — 게이트 요구·해소 이벤트가 무수정 재사용하는 이벤트 스키마·개입 조건. § 포인터로만 참조(재정의 0).
- `uahf/framework/adapters/claude/step-hosting-binding.md` (v1.5 Baseline) — 자매 Adapter Binding. 문서 관례(§9 이력 머리·§0 정본 경계·격리 지점 방향 반전·형태 A/B 정직 구분·§ 근거 정본·실측 대조·L-07)의 선행 표본. 물리 정지 신호(종료 코드 2)·Autonomy→CLI 권한 플래그 매핑·run 데이터 백엔드 이원화는 이 문서가 이미 확정했고, 본 문서는 그 위에 게이트 큐 제시 채널을 얹는다.
- `uahf/framework/adapters/claude/loop-binding.md`·`verifier-binding.md` — 사람 개입 채널(03 §3.1-D 사람 승인 요청이 Claude Code 세션에서 사용자에게 제시된다)·역할 = 서브에이전트 디스패치 관례의 선행 표본.
- `uahf/framework/core/structure.md` §4·§5 — Adapter 경계 = 격리 지점(C-3 비적용·구체 토큰 허용)의 근거.

거버넌스: 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 중립 계약(05·gates.py)을 특정 실행 환경·AI·직렬화 형식에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 AI·환경·직렬화 형식·물리 경로·실행 옵션 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용·자매 바인딩 §0 동형). 단 이 문서는 05·gates.py 의 계약을 **재정의하지 않는다** — 계약은 § 포인터로만 인용한다. 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다.

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-13 | S3 Draft (부분) | 최초 작성. `framework/adapters/claude/` 경계의 신규 산출물(UAF 레벨 바인딩 5종째를 Adapter 물리 경계에 동거 — contract/entry/discovery/solution-design-binding 선례·05 §5). **본 판은 게이트 큐 제시 채널(§3)만 확정**한다: `pending_gates` 파생 뷰를 이 환경에서 사용자에게 제시하는 물리 채널(Claude Code 세션 표면·구조화 제시)과, 사용자·Advisor 의 해소 응답을 게이트 해소 이벤트로 append 하는 물리 관례(`gate::<gate_id>` cycle·`append_gate_resolution` actor 매핑)를 바인딩한다. 정지 신호(종료 코드 2)·Autonomy→권한 플래그 매핑은 step-hosting-binding 확정분을 상속·인용한다. 직렬화 형식·capability→물리 호출 매핑·run 데이터 백엔드 경로·모델 정책 실값은 **S4·S5 소관으로 미확정**(§1·§4 스텁). 05·gates.py 계약 재정의 0, 새 계약·새 용어·새 개입 조건 0. 신설 경로 밖 파일 무수정. | Worker (Advisor 위임, Task S3) |
| 2026-07-13 | S4 Draft (부분) | **§4 신설(Model Selection 실값 매핑 관례·OQ-SH-4 해소 기록)** + 절 재베이스라인(구 §4 미확정→§5·구 §5 실측→§6·구 §6 OQ→§7 — BPD-17 재베이스라인 패턴·과거 §9 행 문면 불변 보존). §4.1 = 불투명 슬롯(중립 정책·`tier-a` 등)→claude 모델 별칭(`haiku`/`sonnet`/`opus`) 매핑 관례(Policy as Data·격리 지점 구체 토큰 허용)·hysteresis/재선택은 중립 코드(`allocation.RESELECTION_TRIGGER_KINDS`) 소유. §4.2 = CP2 독립 슬롯(`cp2ModelSlot`)→`StepHost(cp2_model=...)`→`--model` 전달 경로. §4.3 = **OQ-SH-4 해소 기록**(중립 Host `host.py _dispatch_cp2` 최소 개정 1개소·`cp2_model` 기본 None 시 기존 거동 바이트 동일·step-host 회귀 17건 무손상·`config_schema.json` 선택 필드 추가). §5 갱신(S5 스텁으로 축소·allocation/model-selection 스키마 실재 반영)·§6 실측 대조 S4 재기술(orchestration 94·step-host 20 전건 Pass·전수 스캔 0). **step-hosting-binding §7 OQ-SH-4 문면 자체 갱신은 트랙 종단 정합 소관 — 미접촉.** 05·중립 코드 계약 재정의 0·새 계약·새 gateKind·새 개입 조건 0. `uahf/` 접촉 = 이 문서 + host.py(+config_schema·테스트) 2건뿐(§6 실측). | Worker (Advisor 위임, Task S4) |
| 2026-07-13 | S5 확정 (CP2 판정 대기) | **§5 재저술(S5 스텁 → 확정)** — Artifact Registry(`artifacts.py`·§0 표 5종째 중립 모듈) 완성에 맞춰 직렬화·capability→물리 호출 매핑·run 데이터 백엔드·AgentSpec 실값 레지스트리·Artifact Record 직렬화 관례를 확정한다(과거 §9 행·§3·§4 문면 불변·BPD-17). §5.1 = 직렬화 형식(events.jsonl·revisions.jsonl·**artifacts.jsonl**·graph.json·gate_policy.json·steps/·정책 JSON — 1행 1레코드 append-only·events.py/revision.py/artifacts.py JsonlStore 관례). §5.2 = capability→물리 호출 매핑(step-invoker `ClaudeInvoker` 무수정 재사용·역할 디스패치 Worker/Verifier/Advisor·게이트 리뷰/승인 단위도 동일 경로). §5.3 = run 데이터 백엔드 = `orchestration-data/runs/<run-id>/`(discovery-data·solution-design-data·step-data 선례 동거). §5.4 = AgentSpec 실값 레지스트리 관례(불투명 modelPolicyClass→§4.1 별칭·PO-INV 6). §5.5 = **Artifact Record 직렬화 + 파생 인덱스**(approvalState = 게이트/검증 이벤트 파생 뷰·레지스트리 저장 0). **축소판 종단 dogfooding E2E(시나리오 j) 실증**: `orchestration-data/e2e/`(비프로덕션 드라이버) 실 claude CLI headless **5 세션**(haiku)로 설계 단위 user_decision 게이트 **물리 정지(exit 2)**→시뮬레이션 라벨 해소→구현 revision→구현 step→review 게이트→완주·deterministic replay 동일·상류 재실행 흔적 0. §6 실측 대조 S5 재기술(orchestration 126·step-host 20·step-invoker 19 전건 Pass). 05·중립 코드 계약 재정의 0·새 계약·새 gateKind·새 개입 조건 0. `uahf/` 접촉 = 이 문서 + host.py(S4·불변) + `orchestration-data/` 신설(§6 git 실측). | Worker (Advisor 위임, Task S5) |
| 2026-07-13 | v1.6 Baseline | 마일스톤 v1.6 「Project Orchestration / Dynamic Agent System」 사용자 승인 — 기준선 확정(상태행 승격). CP2 5단계 전건 첫 판정 Pass(S1 8/0/0·S2 7/0/0·S3 10/0/0·S4 9/0/0·S5 9/0/0)·CP3 승인. 본문 §3·§4·§5 계약 매핑·실측 대조 무변경. | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행·자매 바인딩 §9 동형. 이후 개정은 이 표에 append-only 로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 `orchestration/specs/05-project-orchestration.md`(§3.3)와 `orchestration/framework/orchestrator/gates.py`다.** 이 문서는 그 계약의 **claude 환경 실현 매핑**이며, 계약 요소(gateKind 5종·심각도 전순서·게이트 단조성·해소 적격성·게이트 이벤트 필드 관례)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터·심볼 참조로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 05 §5 가 "게이트 큐 제시 채널·직렬화 형식·capability→물리 호출 매핑·run 데이터 백엔드 경로·정책 실값은 Adapter Binding 문서 소관"이라며 미룬 지점이 실재하는(부분 확정되는) 자리다.
- **격리 지점의 방향 반전(C-3 비적용).** 중립 경계(`orchestration/framework/orchestrator/`·05 본문)는 특정 AI·provider·실행 옵션 토큰이 0건이어야 한다(PO-INV 8). 이 문서는 그 **반대편**이다 — 구체 토큰(`claude` CLI·세션 표면·종료 코드·물리 경로)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 바인딩 §0 동형).
- **범위 = 다섯 책임 전부 확정(S5).** 이 문서는 §3(게이트 큐 제시 채널)·§4(Model Selection 실값 매핑·OQ-SH-4 해소)에 더해 **§5(직렬화·capability→물리 호출 매핑·run 데이터 백엔드·AgentSpec 실값 레지스트리·Artifact Record 직렬화)를 확정**한다. §5 는 축소판 종단 dogfooding E2E(시나리오 j)로 **실 데이터 실증**되었다 — 데이터·물리 실현이 실재하며 그 실측 상태는 §6 이 정직하게 대조한다(L-07). 미실증분은 §7 OQ 로 남긴다.
- **창설 금지.** 이 문서는 05 §3.3·§5·gates.py 를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. 새 gateKind·새 상태·새 개입 조건·새 이벤트 필드를 만들지 않는다. 게이트 이벤트는 03 §3.2-A 10필드 무수정 재사용이다.
- 용어는 `uahf/specs/00-glossary.md` 정본만 사용한다. "게이트 큐"·"제시 채널"·"정지 게이트" 는 05·gates.py 의 서술 라벨이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적 (본 판 = 부분)

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
- **정확한 표면 문법·렌더 템플릿**은 이 제안대로 S5 통합 dogfooding 이 실현·확정한다(step-hosting-binding §3.2 "구조 제안·근거" 관례 동형). 본 판은 채널·구조만 확정하고 데이터를 생성하지 않는다(L-07).

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
- **`uahf/` 트리 접촉 2건(본 트랙 누계).** (i) 이 바인딩 문서(S3 신설·S4 §4 추가). (ii) `framework/loop/step-host/host.py` `_dispatch_cp2` 1개소(+`config_schema.json`·step-host 테스트) — OQ-SH-4 해소. 그 외 `uahf/` 정본·중립 코드·append-only 데이터 무촉(형상 관리 상태 조회로 확인·§6 실측 대조).

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

### §5.3 run 데이터 백엔드 = `framework/adapters/claude/orchestration-data/runs/<run-id>/`

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

`orchestration-data/e2e/` 드라이버가 실 claude CLI headless(haiku·**5 세션**)로 종단 흐름을 실증했다(run 데이터 = `runs/orch-j-e2e/`):

- 초기 그래프 = 설계 단위 d1(user_decision 게이트) → d1 실행(Worker+CP2)·Passed → **user_decision 게이트 물리 정지(exit 2·pending_gates 기록)**(j1).
- 드라이버가 **시뮬레이션 라벨을 append-only 로그(`annotation::sim`)와 `gate-resolution-record.json` 에 명시 기록**한 뒤 사용자 actor(`human`) 해소 이벤트 append(j2 — L-07 실 사용자 위장 금지)·구현 단위 revision(basis.gateEventRef = 해소 게이트) append.
- 재개(fresh 프로세스): 구현 단위 impl 실행(Worker+CP2)·`review_required` 추가 리뷰(Verifier)·완주(exit 0). 이벤트 로그 cycle = {d1·impl·gate::·annotation::sim}뿐 — **상류 Discovery/성숙 재실행 흔적 0**(입력 Contract 는 읽기 전용 참조).
- **deterministic resume replay**: `replay_check.py` 2회 실행 stdout 동일(active_graph·states·ready_set·graph_fingerprint). 최종 레지스트리: `design-decision.md` v1 = **user_approved**(사용자 게이트 해소)·`impl-note.txt` v1 = **verified**(derivedFrom `[design-decision.md]`).
- **실 CLI 실패 은폐 0(O5).** 실 세션 stdout·argv·session_id 는 `logs/invoke-*.json` 에 그대로 캡처된다.

---

## §6. 실측 대조 (L-07)

- **중립 코드 실재 (S5).** S5 는 `orchestration/framework/orchestrator/artifacts.py`·`artifact_record_schema.json`·`tests/test_artifacts.py` 를 신설하고, `orchestrator.py`(선택 `artifact_store`·투명 포집 래퍼 배선·`artifact_registry()`/`resolve_references()` 파생 메서드)를 최소 개정했다(`artifact_store=None` 기본 시 S2~S4 거동 바이트 동일 보존). 자체 테스트는 표준 라이브러리 `unittest` 만으로 통과한다 — **orchestration 126건(신규 32 + S2~S4 회귀 94)·step-host 20건·step-invoker 19건 = 전건 Pass**(실행 출력 실측).
- **PO-INV 8(중립성) 실측.** `orchestration/framework/orchestrator/`(artifacts.py 포함 전 `.py`·전 `.json`·테스트)에 provider·모델·CLI 옵션 토큰 0건(전수 스캔). approvalState 어휘(draft/verified/approved/user_approved)·verdict `Pass` 는 05 §3.6·06 계약 어휘다. 구체 토큰(`claude`·모델 별칭 `haiku`/`sonnet`/`opus`·`--model`·권한 플래그)은 이 바인딩 문서·step-invoker 코드·`orchestration-data/e2e/` 드라이버(격리 지점)에만 존재한다.
- **축소판 종단 E2E 실측 (시나리오 j).** `orchestration-data/e2e/`(비프로덕션 드라이버) 실 claude CLI headless **5 세션**(haiku)로 종단 흐름 실증 — Phase 1(exit 2 게이트 정지·2 세션)·Phase 2(exit 0 완주·3 세션). run 데이터 = `runs/orch-j-e2e/`(events.jsonl 8 이벤트·revisions.jsonl 1·artifacts.jsonl 2·워크스페이스 실 산출 2). 상류 재실행 흔적 0·replay 2회 동일·최종 레지스트리 approvalState 파생(user_approved/verified) 실측. 실 세션 stdout·argv 는 `logs/invoke-*.json` 에 캡처(은폐 0·O5).
- **`uahf/` 접촉 실측(본 트랙 누계).** (i) 이 바인딩 문서(S3 신설·S4·S5 §5 확정). (ii) `framework/loop/step-host/host.py` `_dispatch_cp2` 1개소(S4·**S5 무촉**·`cp2_model=None` 시 기존 거동). (iii) `framework/adapters/claude/orchestration-data/` **신설**(바인딩 물리 경계 동거 run 데이터·E2E 드라이버 — UAF 레벨 바인딩 선례 4건 동형). 그 외 `uahf/` 정본·중립 코드·append-only 데이터(discovery-data·solution-design-data·step-data·memory-data·loop-data) 무촉(형상 관리 상태 조회로 확인·git 실측).
- **정직 구분 (L-07).** 시나리오 j 의 사용자 게이트 해소·구현 단위 제안은 **드라이버 픽스처**이며 실 사용자·실 LLM 제안 step 이 아니다(§5.6·`gate-resolution-record.json`·`annotation::sim` 이벤트에 명시). 실증 대상은 게이트 물리 정지·사용자 actor 적격성·revision 인과 사슬·deterministic 재개이며 그 축들은 실 데이터로 남는다. 산출 내용은 CP2 재현성을 위해 정확 내용으로 고정한 픽스처다(설계 메모를 exact-content 설계 결정 레코드로 축약).

---

## §7. Open Questions (본 판 이월)

- **OQ-PO-B1 (게이트 큐 제시 표면 문법).** `pending_gates` 항목의 사람 친화 렌더 템플릿(라벨·문면·다국어)은 §3.2 구조 제안·§5.6 stop-signal 기록으로 실증되었으나 사용자 대화 세션 표면의 최종 렌더 문법은 트랙 종단/후속 관찰 소관으로 남긴다.
- **OQ-PO-B2 (해소 어휘 성숙).** 전용 해소 이벤트 어휘(재시도 예산 비계수·해소 취소)는 OQ-SH-5·05 §9 OQ 3 이월. 본 판은 `append_gate_resolution` 현행 형태만 바인딩.
- **OQ-PO-B3 (headless 런처 ↔ 사용자 세션 제시 브리지).** orchestrator(headless)의 이벤트 로그를 사용자 대화 세션이 읽어 게이트 큐를 표면화하는 물리 브리지(폴링·훅·수동 조회)의 정밀 형태. §5.6 은 드라이버가 stop-signal 을 읽어 재개하는 형태로 실증했으나, 실 사용자 대화 세션 브리지의 정밀 형태는 후속 관찰 소관.
- **OQ-PO-B4 (실 LLM 제안 step·비픽스처 성숙 run).** §5.6 의 구현 단위 제안은 드라이버 픽스처다. 설계 단위 산출 artifact 를 실 LLM 제안 step 이 소비해 구현 task 를 제안하는 완전 성숙 run(형태 A 성숙 run·BPD-20 동형)은 후속 트랙 소관.
