# framework/orchestrator — 중립 Project Orchestrator 모듈 (경계 문서)

## 위상

Project Orchestrator 는 **판단하지 않는 기계 구동자**다(05 §2). 상류 산출물을 인수해
프로젝트 완료까지 lifecycle 을 조율하되, 단일 run 의 무인 실행은 UAHF Step Host 를
substrate 로 **라이브러리 무수정 재사용**하여 위임하고 재구현하지 않는다(05 §0·§2.2).
자신은 run/작업 단위 입도로 그래프 진화(Revision Ledger)·게이트 근거 실재 검증을
deterministic 하게 구동할 뿐, 의미 판단(완료·실패·검증·승인·게이트 정책 평가)을 하지
않는다.

이 디렉터리는 그 구동자의 **provider-중립 실현**이다 — 실행 표면은 전부 Step Host 의
`invoker` 추상 인터페이스 너머 Adapter 구현체 소관이며, 이 코드에는 특정 실행 환경·
provider·모델·상류 Layer 고유명 토큰을 두지 않는다(PO-INV 8).

## 계약 정본 (05 바인딩 지점 포인터)

이 코드가 준수하는 계약의 정본은 이 디렉터리가 아니라 다음 문서다:

- `orchestration/specs/05-project-orchestration.md` — Project Orchestration 중립 계약 전부.
  - §2 위상 · §3.1 Project Work Graph · §3.2 Graph Revision Ledger(RevisionEvent·
    결정성 3조건) · §3.3~§3.6 Gate Policy·할당·Model Selection·Artifact Record ·
    §4 PO-INV 1~8 · §5 Adapter 바인딩 지점 · §6 무수정 경계.
- `uahf/framework/runtime/step-hosting-protocol.md` — substrate 계약(단일 run 무인 관리).
- 물리 실현(직렬화 형식·run 데이터 백엔드 경로·게이트 큐 제시 채널·capability→물리 호출
  매핑·정책 실값)은 이 코드가 아니라 **Adapter Binding 문서** 소관이다(05 §5). 이 코드는
  그 지점을 추상(RevisionStore·EventStore·Invoker·config)으로 열어 둔다.

## 구성 (S2·S3 산출)

| 파일 | 책임 |
|---|---|
| `revision.py` | RevisionEvent · RevisionLedger(append-only, 인메모리+JSONL) · `fold()`(순수·안정 정렬) · `validate_revision()`(순수·07 §3.1-A 사유 코드 재사용). |
| `orchestrator.py` | ProjectOrchestrator — fold → Step 직렬화 → **StepHost 무수정 구동**(공유 EventStore) → 그래프 성장 확인 → Escalated 즉시 정지. 게이트 근거 실재 검증(PO-INV 5)·결정적 재개. **S3: 단위 경계 게이트 처리(`_process_gates` — 배치 종단 일괄)·정지 게이트 정지·재개**. |
| `gates.py` | **(S3)** Gate Policy 평가기 — gateKind 5종·심각도 전순서·`GatePolicy.evaluate`(순수·결정적)·게이트 단조성 하한(`floor`·`effective_gate`)·게이트 이벤트 필드 관례 단일 소유(`gate::` 관례 정식화)·`pending_gates` 파생 뷰·해소 적격성. |
| `stephost_bridge.py` | `uahf/framework/loop/step-host/` 중립 모듈의 **무수정 import 경로**(평면 import 를 위한 sys.path 조작은 orchestration 쪽에서만). |
| `revision_schema.json` | RevisionEvent 직렬화 형태 정의(실값 없음 — step-host `config_schema.json` 관례 동형). |
| `gate_policy_schema.json` | **(S3)** Gate Policy 데이터 형태 정의(실값 없음). **floor 는 스키마가 아니라 코드(`gates.py floor()`) 소유** — 정책 데이터로 하한을 약화 불가(주석 명시). |
| `tests/` | 모의 invoker 기반 통합 테스트(외부 의존 0). `test_gates.py`(S3) = gates 순수 + orchestrator 게이트 통합. |

**아직 없는 것(후속 단계).** 할당·모델 선택(`allocation.py`)·Artifact Registry
(`artifacts.py`)·Adapter 바인딩 완성은 S4~S5 소관이며 이번 단계 범위 밖이다(설계 §5).

## 게이트 처리 (S3 — 05 §3.3·PO-INV 4)

- **gateKind 5종·심각도 전순서.** `auto_continue < review_required < approval_required <
  escalation_required < user_decision_required`(05 §3.3 표 어휘·순서 그대로). `gates.py`
  가 이 어휘·전순서·기존 계약 매핑을 단일 소유한다.
- **evaluate 매칭 우선순위·tie-break.** `GatePolicy.evaluate(descriptor)` 는 매칭
  우선순위 **명시 target(전이·artifact class·tier 2) > 단위 유형 기본(unitType·tier 1) >
  전역 기본(빈 target·tier 0)** 로 gateKind 를 고른다. **tie-break: 같은 tier 에서 복수
  엔트리가 매칭하면 가장 심각한 gateKind(max severity)를 채택**한다 — 모호성에서 약한
  게이트를 고르지 않는 안전측 규칙(단조성 보존·결정적). 매칭 0 이면 auto_continue.
- **게이트 단조성(PO-INV 4) = 코드 소유 하한(floor).** `floor(descriptor)` 는
  (i) 실행 착수/Contract 지점 target class → `user_decision_required`
  (ii) 03 §3.1-D 조건 2~5(개입 조건) → `escalation_required` 이상. `effective_gate =
  max(floor, policy)` 이므로 **정책 데이터가 하한보다 약한 값을 지정해도 하한으로
  클램프**된다(약화 불가·강화만). floor 테이블은 `gates.py` 가 소유하며 스키마·정책
  데이터로 내릴 수 없다.
- **CP2 는 게이트가 관여하지 않는다.** CP2(Verifier 독립 판정)는 **Step Host 가
  policy·gate 무관하게 무조건 별도 디스패치**하며(host.py `_dispatch_cp2`·SH-INV-4),
  **우회 경로 자체가 존재하지 않는다**. 따라서 CP2 는 floor 테이블에도, Gate Policy
  에도 없다 — 게이트 정책이 CP2 를 켜고 끌 수 없다(구조적 불변). `auto_continue` 는
  "추가 게이트 0"이되 CP2 하한은 그대로다.
- **Autonomy 직교.** 게이트 축은 Autonomy Policy 3값(interactive/auto_approve/
  unrestricted — 도구 승인 축)과 **직교**한다. 게이트 **결정** 로직(gateKind 평가·must_stop·
  해소 적격성)은 `self.policy`(autonomy) 를 참조하지 않으므로 — 서브단위 실행에는 동일
  autonomy 를 전달만 한다 — `unrestricted` 에서도 정지 게이트는 그대로 정지한다(05 §3.3).
- **게이트 큐 = 파생 뷰(mutable 큐 0).** `pending_gates(events, policy)` 는 미해소 정지
  게이트 요구의 파생 함수다(PO-INV 2). 게이트 요구·해소 이벤트는 03 §3.2-A 10필드 무수정
  재사용이며 `gate::<gate_id>` cycle 네임스페이스라 step 상태 파생에 간섭하지 않는다.
  해소 적격성: `user_decision_required` = 사용자 actor 클래스만·`escalation_required` =
  허용 resolver 집합(actor 클래스 값은 정책 데이터·기본값은 스키마).
- **판단 0(PO-INV 1).** 게이트 처리의 모든 분기는 데이터(gateKind)·순수 함수(evaluate·
  floor·is_resolved) 결과로만 이뤄진다 — orchestrator·gates 에 내용 판정 로직 0.
  review(Verifier)·approval(Advisor 역할·CP3 물리화)의 실제 판정은 디스패치된 실행
  단위가 소유하고, orchestrator 는 반환을 소비만 한다.

## 게이트 승인 이벤트(S2 잔여 관례)

S2 단계에서 게이트 승인 이벤트는 **외부(상위/드라이버)가 append 하는 데이터**였고
orchestrator 는 그 실재만 검증했다(revision 근거·PO-INV 5). S3 는 이 `gate::` 관례를
`gates.py` 가 단일 소유로 정식화한다. revision 근거 검증(`_gate_event_exists`)은 게이트
**통과**(outcome=="pass") 이벤트만 인정한다 — S3 게이트 요구 이벤트(outcome=="escalated")는
미해소이므로 revision 을 근거지어서는 안 된다(강화적 정정·S2 승인 이벤트는 전부 pass 라
거동 보존).

## 재사용 경계 (uahf/ 무촉)

- Step Host(`step.py`·`events.py`·`host.py`·`invoker.py`·`bundle.py`)를 라이브러리로
  **무수정 import** 한다. 새 Step 클래스·새 이벤트 스키마·새 상태 열거를 창설하지 않는다 —
  기존 `Step`·이벤트 로그(10필드)·상태 5종(Pending/Active/Passed/Failed/Escalated)을
  그대로 쓴다.
- `RevisionEvent` 는 본 Layer 신규 소유 레코드다(05 §0 표). 이는 Step·이벤트·상태 열거가
  아니라 Graph Revision Ledger 계약이며, 05 §3.2 가 승인한 신규 소유물이다.

## 불변 (요지 — 정본은 05 §4)

- 판단 0 (PO-INV 1) · 이중 원장 append-only (PO-INV 2) · 결정적 재개 (PO-INV 3) ·
  게이트 단조성(Step Host 소유·PO-INV 4) · revision 근거 필수 (PO-INV 5) ·
  역할 추상 유지 (PO-INV 6) · artifact 계보(후속·PO-INV 7) · 중립성·격리 (PO-INV 8).

## 결정성 3조건 대응물 (05 §3.2)

- ① **전순서** — `RevisionLedger` 가 `revisionSeq` 를 append 시점에 단조 부여 +
  orchestrator 가 `gateEventRef` 실재를 검증(게이트 이벤트 append 후에만 수용).
- ② **안정 정렬** — `fold()` 가 `revisionSeq` 기준 안정 정렬 + 파생 Task 순서 결정.
- ③ **순수 함수 검증** — `validate_revision()`·`fold()` 는 I/O·상태 없는 순수 함수.

## 테스트 실행

이 디렉터리의 모듈은 평면(flat) import 를 쓰므로, 테스트 파일이 이 디렉터리를 `sys.path`
에 넣고 실행한다. `stephost_bridge` 가 `uahf/` step-host 디렉터리를 sys.path 에 넣어
라이브러리로 무수정 import 한다. 외부 패키지 의존은 없다(표준 라이브러리 `unittest` 만).

```
python orchestration/framework/orchestrator/tests/test_revision.py
python orchestration/framework/orchestrator/tests/test_orchestrator.py
```

**테스트 성격 (정직 표기).** `tests/test_orchestrator.py` 는 **모의 invoker 통합
테스트**다 — 기존 `invoker.py` Invoker 추상을 구현한 중립 stub 으로 설계 §5 S2 시나리오
3건(제안→게이트→revision→실행 / 결정적 재개 / 순환 차단)을 실증한다. **실 CLI E2E 는
S5 소관**이며 이번 테스트에 포함되지 않는다.
