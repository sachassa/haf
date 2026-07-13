# framework/adapters/claude/project-orchestration-binding — Claude Project Orchestration Adapter 바인딩

작성일: 2026-07-13
상태: S4 Draft (부분 — 게이트 큐 제시 채널 + Model Selection 실값 매핑 관례·OQ-SH-4 해소 기록 확정. 직렬화·capability→물리 호출 매핑·run 데이터 백엔드는 S5 완성). 직전 기준선: 없음(신규 산출물 — 트랙 「Project Orchestration / Dynamic Agent System」)
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

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행·자매 바인딩 §9 동형. 이후 개정은 이 표에 append-only 로 기록한다.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 `orchestration/specs/05-project-orchestration.md`(§3.3)와 `orchestration/framework/orchestrator/gates.py`다.** 이 문서는 그 계약의 **claude 환경 실현 매핑**이며, 계약 요소(gateKind 5종·심각도 전순서·게이트 단조성·해소 적격성·게이트 이벤트 필드 관례)를 **재정의·확장하지 않는다**. 계약 요소는 정본 § 포인터·심볼 참조로만 인용한다.
- 이 문서는 `framework/adapters/claude/` 소속 **Adapter Binding 문서**다. 05 §5 가 "게이트 큐 제시 채널·직렬화 형식·capability→물리 호출 매핑·run 데이터 백엔드 경로·정책 실값은 Adapter Binding 문서 소관"이라며 미룬 지점이 실재하는(부분 확정되는) 자리다.
- **격리 지점의 방향 반전(C-3 비적용).** 중립 경계(`orchestration/framework/orchestrator/`·05 본문)는 특정 AI·provider·실행 옵션 토큰이 0건이어야 한다(PO-INV 8). 이 문서는 그 **반대편**이다 — 구체 토큰(`claude` CLI·세션 표면·종료 코드·물리 경로)의 사용이 허용되며, 그 격리가 이 경계의 존재 이유다(자매 바인딩 §0 동형).
- **본 판의 범위 = 게이트 큐 제시 채널 + Model Selection 실값 매핑·OQ-SH-4 해소(부분).** 이 문서는 §3(게이트 큐 제시 채널)과 **§4(Model Selection 실값 매핑 관례·OQ-SH-4 해소 기록)**을 확정한다. §5 의 나머지(직렬화·capability→물리 호출 매핑·run 데이터 백엔드)는 S5 완성 대상의 스텁이며, 데이터·물리 실현을 **주장하지 않는다**(L-07 — 미존재를 실재로 쓰지 않는다).
- **창설 금지.** 이 문서는 05 §3.3·§5·gates.py 를 **넘어서는 새 바인딩 계약을 창설하지 않는다**. 새 gateKind·새 상태·새 개입 조건·새 이벤트 필드를 만들지 않는다. 게이트 이벤트는 03 §3.2-A 10필드 무수정 재사용이다.
- 용어는 `uahf/specs/00-glossary.md` 정본만 사용한다. "게이트 큐"·"제시 채널"·"정지 게이트" 는 05·gates.py 의 서술 라벨이다. 본 문서는 새 용어를 신설하지 않는다.

---

## §1. 목적 (본 판 = 부분)

이 문서는 05(§3.3 Gate Policy·§2.2 게이트 큐)와 gates.py 를 claude 환경 위에 **S3 시점의 구체 물리 실현**으로 매핑한다. **본 판은 다섯 책임 중 하나(게이트 큐 제시 채널)만** 확정한다:

- **확정(§3).** `pending_gates` 파생 뷰의 사용자 제시 채널 + 해소 응답의 이벤트 append 물리 관례.
- **확정(§4).** Model Selection 정책 실값(불투명 슬롯 → claude 모델 별칭) 매핑 관례 + CP2 독립 슬롯(`cp2ModelSlot`) → `--model` 전달 경로 + OQ-SH-4 해소 기록.
- **미확정(S5 스텁·§5).** 정책·이벤트 직렬화 형식 · capability→물리 호출 매핑 · run 데이터 백엔드 경로 · AgentSpec 실값 레지스트리. 이들은 후속 단계가 확정한다.

이 문서는 05·gates.py 의 어떤 계약 요소도 재정의·확장하지 않는다.

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

## §5. 미확정 (S5 스텁 — L-07)

아래는 후속 단계(S5) 소관이며, 본 판은 물리 실현·데이터를 **주장하지 않는다**.

| 바인딩 지점 | 소관 | 상태 |
|---|---|---|
| Gate Policy·Allocation·Model Selection 데이터 직렬화 형식·물리 경로 | S5 (JSON·`orchestration-data/` 예상) | **미확정.** `gate_policy_schema.json`·`allocation_schema.json`·`model_selection_schema.json` 형태만 실재(중립 코드). 실값 정책 데이터 미생성. |
| capability → 물리 호출 매핑·AgentSpec 실값 레지스트리 | S5 | **미확정**(05 §3.4·PO-INV 6 — 중립 코드는 capability 선언까지만 소비·AgentSpec 물리 매핑 미해석). |
| Model Selection 정책 실값(슬롯→별칭 실 데이터) | S5 (§4.1 매핑 관례 확정·실 데이터 미생성) | **관례 확정·실값 미생성.** 매핑 관례(§4.1)는 본 판 확정이나 실 정책 데이터(`slots`/`fallbackChain`/`cp2ModelSlot` 실값)는 S5 dogfooding 이 생성한다. |
| run 데이터 백엔드 경로(dogfooding) | S5 (`framework/adapters/claude/orchestration-data/` 예상 — discovery-data·solution-design-data 선례) | **미확정·미생성.** |
| 게이트 큐 제시 표면 문법·렌더 템플릿 실값 | S5 통합 dogfooding | **구조만 확정**(§3.2). 실값 미생성. |

---

## §6. 실측 대조 (L-07)

- **중립 코드 실재 (S4).** S4 는 `orchestration/framework/orchestrator/allocation.py`·`allocation_schema.json`·`model_selection_schema.json`·`tests/test_allocation.py` 를 신설하고, `gates.py`(`latest_marker_verdict` — CP3 status 소비)·`orchestrator.py`(슬롯 채움·재선택 차수 파생·CP2 슬롯 전달·CP3 비-Pass 정지)를 최소 개정했다. 자체 테스트는 표준 라이브러리 `unittest` 만으로 통과한다 — **orchestration 94건(신규 32 + S2·S3 회귀 62)·step-host 20건(신규 3 + 회귀 17) = 전건 Pass**.
- **PO-INV 8(중립성) 실측.** `orchestration/framework/orchestrator/`(allocation.py 포함 전 `.py`·전 `.json`·테스트)에 provider·모델·CLI 옵션 토큰 0건(전수 스캔). 모델 슬롯은 불투명 문자열(테스트는 `tier-a`/`tier-verify` 등)이다. 구체 토큰(`claude`·모델 별칭 `haiku`/`sonnet`/`opus`·`--model`)은 이 바인딩 문서(§4)와 step-invoker 코드에만 존재한다(격리 지점).
- **`uahf/` 접촉 실측(본 트랙 누계 2건).** (i) 이 바인딩 문서(S3 신설·S4 §4 추가). (ii) `framework/loop/step-host/host.py` `_dispatch_cp2` 1개소(+`config_schema.json` 선택 필드·`tests/test_step_host.py` 신규 3건) — OQ-SH-4 해소. 그 외 `uahf/` 정본·중립 코드·append-only 데이터 무촉(형상 관리 상태 조회로 확인).
- **OQ-SH-4 해소 실측.** host.py diff = 생성자 `cp2_model` 파라미터 추가 + `_dispatch_cp2` 의 `model=step.model` → `model=cp2_model`(1행·`cp2_model=None` 시 기존 값). 기본 `None` 시 기존 step-host 회귀 17건 **무수정 Pass**(바이트 동일 거동 실측).
- **미생성 구분.** §5 의 실 정책 데이터(슬롯→별칭 실 데이터)·run 데이터 백엔드·capability→물리 호출 매핑·AgentSpec 실값 레지스트리는 **미생성**이다 — S5 가 생성한다. §4.1 매핑 관례는 확정이나 실 데이터는 아직 없다(L-07 — 미존재를 실재로 쓰지 않는다).

---

## §7. Open Questions (본 판 이월)

- **OQ-PO-B1 (게이트 큐 제시 표면 문법).** `pending_gates` 항목의 사람 친화 렌더 템플릿(라벨·문면·다국어)은 §3.2 구조 제안대로 S5 통합 dogfooding 이 실현·확정한다. 현재는 구조화 제안만.
- **OQ-PO-B2 (해소 어휘 성숙).** 전용 해소 이벤트 어휘(재시도 예산 비계수·해소 취소)는 OQ-SH-5·05 §9 OQ 3 이월. 본 판은 `append_gate_resolution` 현행 형태만 바인딩.
- **OQ-PO-B3 (headless 런처 ↔ 사용자 세션 제시 브리지).** orchestrator(headless)의 이벤트 로그를 사용자 대화 세션이 읽어 게이트 큐를 표면화하는 물리 브리지(폴링·훅·수동 조회)의 정밀 형태는 S5 관찰로 확정한다. 현재는 "사용자 채널이 이벤트 로그를 읽어 제시"로만 바인딩(§3.2).
