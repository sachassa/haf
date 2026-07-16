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

## 구성 (S2·S3·S4·S5 산출)

| 파일 | 책임 |
|---|---|
| `revision.py` | RevisionEvent · RevisionLedger(append-only, 인메모리+JSONL) · `fold()`(순수·안정 정렬) · `validate_revision()`(순수·07 §3.1-A 사유 코드 재사용). |
| `orchestrator.py` | ProjectOrchestrator — fold → Step 직렬화 → **StepHost 무수정 구동**(공유 EventStore) → 그래프 성장 확인 → Escalated 즉시 정지. 게이트 근거 실재 검증(PO-INV 5)·결정적 재개. **S3: 단위 경계 게이트 처리(`_process_gates` — 배치 종단 일괄)·정지 게이트 정지·재개**. **S4: Step 직렬화 시점 슬롯 채움(`_build_steps`→`_fill_slots`·명시값 우선)·재선택 차수 파생(`_fallback_level`)·CP2 독립 모델 슬롯 StepHost 전달(`_new_host`)·CP3 비-Pass 정지 배선(`_process_gates` approval 분기)**. **S5: 선택 `artifact_store` 투명 포집 래퍼 배선(`_effective_invoker`)·`artifact_registry()`/`resolve_references()` 파생 메서드(읽기만·mutable 저장 0)**. |
| `gates.py` | **(S3)** Gate Policy 평가기 — gateKind 5종·심각도 전순서·`GatePolicy.evaluate`(순수·결정적)·게이트 단조성 하한(`floor`·`effective_gate`)·게이트 이벤트 필드 관례 단일 소유(`gate::` 관례 정식화)·`pending_gates` 파생 뷰·해소 적격성. **(S4)** `latest_marker_verdict`(승인/리뷰 마커 verdict **status** 소비·내용 판정 0 — CP3 비-Pass 정지의 소비 함수). |
| `allocation.py` | **(S4)** Dynamic Allocation + Model Selection Policy — `AgentSpec`(7필드 실행 프로파일)·`AgentSpecRegistry`(버전 있는 데이터·`match` deterministic·불투명 참조)·`ModelSelectionPolicy`(Policy as Data·`select_model` 순수·fallback·CP2 독립 슬롯)·`Allocation` 파사드. |
| `artifacts.py` | **(S5)** Artifact Record·Registry — `ArtifactRecord`(8필드 계보·provenance)·approvalState 파생 사다리(draft→verified→approved→user_approved·게이트/검증 이벤트 파생 뷰)·Artifact 선언 원장(append-only 인메모리+JSONL)·`ArtifactCapturingInvoker`(완료 보고 artifacts 투명 포집 래퍼)·`derive_registry()`(순수·계보 보존·approvalState 파생)·`resolve_references()`(요구 등급 이상 최신 버전만). **레지스트리는 저장되지 않고 매 호출 파생된다(제2 진리원천 아님).** |
| `stephost_bridge.py` | `uahf/framework/loop/step-host/` 중립 모듈의 **무수정 import 경로**(평면 import 를 위한 sys.path 조작은 orchestration 쪽에서만). |
| `revision_schema.json` | RevisionEvent 직렬화 형태 정의(실값 없음 — step-host `config_schema.json` 관례 동형). |
| `gate_policy_schema.json` | **(S3)** Gate Policy 데이터 형태 정의(실값 없음). **floor 는 스키마가 아니라 코드(`gates.py floor()`) 소유** — 정책 데이터로 하한을 약화 불가(주석 명시). |
| `allocation_schema.json` | **(S4)** AgentSpec 레지스트리 + 매칭 tie-break 정책 형태(실값 없음). tie-break 스키마 default 는 코드 fallback(`allocation.DEFAULT_TIE_BREAK`)과 일치(단일 진리원천). |
| `model_selection_schema.json` | **(S4)** Model Selection 정책 형태(실값 없음) — `slots`(class→불투명 슬롯)·`fallbackChain`·`cp2ModelSlot`·`cp2ModelSlots`(class별 CP2 오버라이드·가법)·`defaultSlot`(OQ-SH-4). 실제 모델명은 스키마·중립 코드 밖(Adapter 실값)에만. |
| `artifact_record_schema.json` | **(S5)** ArtifactRecord 형태 정의(실값 없음) — 8필드·approvalState enum(4등급·코드 사다리와 일치). |
| `tests/` | 모의 invoker 기반 통합 테스트(외부 의존 0). `test_gates.py`(S3)·`test_allocation.py`(S4)·`test_artifacts.py`(S5) = artifacts 순수 + orchestrator 산출물 계보 통합(시나리오 i). |

## 할당·모델 선택 (S4 — 05 §3.4·§3.5·PO-INV 6·8)

- **AgentSpec 3층 병존.** 할당은 Role(04 §3.3 Expert Role — 인용·재정의 0) / AgentSpec(실행
  프로파일·본 Layer 신규 소유) / Instance(비영속·이벤트 로그 파생) 3층이며, 02 §3.2-A 4역할
  (Lifecycle 의무 축)과 병존한다. `allocation.py` 는 AgentSpec 층만 소유한다 — Role 재정의 0.
- **AgentSpec 7필드.** `{specId·capabilitySelector·briefTemplateRef·defaultConstraints·
  toolPolicyClass·modelPolicyClass·version}`(05 §3.4). briefTemplateRef·defaultConstraints·
  toolPolicyClass·modelPolicyClass 는 **불투명 참조**다 — 코드는 실값의 의미를 해석하지 않고
  매칭·키 사용·전달만 한다(PO-INV 6 — 어느 실행 주체가 호스팅하는가는 Adapter 소관).
- **매칭 deterministic + tie-break.** `AgentSpecRegistry.match(capability)` 는 capability 선언
  까지만 소비해(제안=LLM step·수용=게이트·05 §3.4) 매칭 AgentSpec 중 하나를 결정적으로 고른다.
  **tie-break 기본값(05 §9 OQ 8 S4 확정): 더 구체적인 selector 우선 → 같으면 최고 version.**
  진짜 동률은 specId 사전순으로 결정적 해소한다. 규칙은 `tieBreak` 데이터로 오버라이드 가능하다.
- **Model Selection = Policy as Data·hysteresis.** `ModelSelectionPolicy.select_model(class,
  level)` 는 순수 함수다 — 같은 입력 → 같은 슬롯(정상 재실행에서 재선택 없음). 모델 선택은 Step
  직렬화 시점 1회 고정이며, 슬롯을 바꾸는 **재선택 트리거는 정확히 2건뿐**이다(`allocation.
  RESELECTION_TRIGGER_KINDS` — (a) retry 한도 도달 (b) 명시적 모델 정책 이벤트). orchestrator
  `_fallback_level` 이 이벤트 로그에서 그 2종만 세어 재선택 차수를 파생한다 — 그 외 어떤 경로도
  모델 슬롯을 바꾸지 않는다(코드 구조로 2건 한정 확인 가능). 슬롯은 별도 mutable 기록이 아니라
  (capability, 정책, 트리거 이벤트)의 결정적 파생이다(같은 두 원장 → 같은 슬롯·PO-INV 3 동형).
- **CP2 Verifier 모델 독립(OQ-SH-4 해소).** `cp2ModelSlot` 이 지정되면 orchestrator 가
  `StepHost(cp2_model=...)` 로 전달하고, Step Host 가 CP2 만 그 슬롯으로 디스패치한다(피검증
  단위와 결합 해소). 미지정(기본)은 대상 step 슬롯 상속(기존 거동 완전 보존).
- **CP3 비-Pass 정지(S4 배선).** `approval_required` 게이트에서 CP3(Advisor 역할) 디스패치의
  verdict **status** 가 비-Pass 면 escalation 게이트 요구를 append 하고 정지한다 — 적격 해소
  (Advisor/사람)로만 재개된다. verdict 는 **status 소비**이지 내용 판정이 아니다(PO-INV 1·
  host.py `verdict_pass` 동형). CP3 Pass 면 기존처럼 무정지 통과한다.
- **중립성(PO-INV 8).** `allocation.py`·스키마·테스트에 실제 모델명·provider 토큰 0건이다 —
  모델 슬롯은 불투명 문자열이며(테스트는 `tier-a`/`tier-verify` 등 사용) 실값은 Adapter 정책
  데이터 소관이다(model_selection_schema.json 주석).

## Artifact Registry (S5 — 05 §3.6·PO-INV 7·2·8)

- **레지스트리 = 파생 인덱스(제2 진리원천 아님).** `artifacts.py` 는 완료 보고(02 §3.2-C
  `artifacts`)에서 포집한 append-only 선언 원장과 게이트/검증 이벤트로부터 `{artifactId:
  [ArtifactRecord]}` 를 **매 호출 새로 파생**한다(`derive_registry` — 순수 함수·별도 mutable
  저장 0). 완료 보고 artifacts 는 `ArtifactCapturingInvoker`(투명 래퍼)가 실행 경로에서
  포집하며, 래퍼는 inner 반환을 변경하지 않고 CP2/CP3 verdict 반환은 포집하지 않는다.
- **ArtifactRecord 8필드.** `{artifactId·version·supersedes·derivedFrom·producedBy·
  approvalState·location·contentHash}`(05 §3.6). `producedBy`(provenance)는 **불투명 부속**
  (SP-INV 3 동형)이며 소비 조건으로 쓰지 않는다.
- **approvalState = 게이트/검증 이벤트 파생 뷰(PO-INV 7).** draft → verified(대상 step 의
  CP2 Pass 이벤트) → approved(CP3 승인 마커 Pass) → user_approved(user_decision 게이트가
  적격 사용자 actor 로 해소). **각 등급은 대응 이벤트 실재에서만 파생**되며 직접 쓰이지 않는다.
  게이트 판독은 `gates.py` 순수 함수에 위임한다(재구현 0).
- **계보 append-only(PO-INV 7).** `supersedes` 는 삭제가 아니라 계보 append 이며 과거 버전
  문면(location+contentHash 내용)은 불변이다(PC-INV 9 동형). `derive_registry` 는 계보 전체를
  version 오름차순으로 보존한다.
- **번들 확정 참조 = 요구 등급 이상 최신 버전만.** `resolve_references(registry,
  required_grade)` 는 각 artifactId 에 대해 요구 등급 이상 approvalState 의 최신 version 하나만
  해석한다 — 미완성·미승인 산출물은 추측·인용 0(05 §3.6·07 R2). 등급 미달·구버전은 배제하지
  않고 resolve 만 제외한다(문면 불변 보존).
- **orchestrator 통합(최소).** `ProjectOrchestrator(artifact_store=...)` 지정 시 실행 invoker
  를 포집 래퍼로 감싸고 `artifact_registry()`·`resolve_references(required_grade)` 를
  파생 제공한다. 미지정(기본) 시 포집 0·S2~S4 거동 바이트 동일 보존.
- **중립성(PO-INV 8).** `artifacts.py`·스키마·테스트에 provider·모델 토큰 0건(전수 스캔).
  approvalState 어휘·verdict `Pass` 는 05 §3.6·06 계약 어휘다.

**아직 없는 것(후속).** 실 LLM 제안 step 기반 비픽스처 성숙 run 은 후속 소관이다(설계 §6·바인딩 §7 OQ-PO-B4).
루트 라우터 등재는 v1.6 Baseline 으로 완료되었다(루트 `ARCHITECTURE.md` v1.5 §2.1 라우터 표).

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
python -B -m unittest discover -s orchestration/framework/orchestrator/tests -p "test_*.py"
```

(`-B` 로 pyc 부산물을 만들지 않는다. pytest 는 쓰지 않는다.)

**테스트 성격 (정직 표기).** `tests/` 는 전부 **모의 invoker 통합 테스트 + 순수 함수
테스트**다 — 기존 `invoker.py` Invoker 추상을 구현한 중립 stub 으로 설계 §5 S2~S5 시나리오를
실증한다(S2 제안→게이트→revision→실행·결정적 재개·순환 차단 / S3 게이트 5종·단조성·자율성
직교 / S4 모델 슬롯·hysteresis·CP2 독립·CP3 정지·tie-break / **S5 ArtifactRecord·approvalState
파생 사다리·derive_registry 순수·resolve_references·시나리오 i 계보(설계 v1→rework v2
supersedes·derivedFrom·소비 번들 required_grade·v1 문면 불변 물리 해시)**). 전건 Pass:
orchestration 126·step-host 20·step-invoker 19. **실 CLI 종단 E2E(시나리오 j)는 Adapter
경계의 `orchestration-data/e2e/` 드라이버**가 소유한다(비프로덕션·격리 지점 — 05 §5).
