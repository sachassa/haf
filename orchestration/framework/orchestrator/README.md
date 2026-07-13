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

## 구성 (이번 단계 = S2 산출)

| 파일 | 책임 |
|---|---|
| `revision.py` | RevisionEvent · RevisionLedger(append-only, 인메모리+JSONL) · `fold()`(순수·안정 정렬) · `validate_revision()`(순수·07 §3.1-A 사유 코드 재사용). |
| `orchestrator.py` | ProjectOrchestrator — fold → Step 직렬화 → **StepHost 무수정 구동**(공유 EventStore) → 그래프 성장 확인 → Escalated 즉시 정지. 게이트 근거 실재 검증(PO-INV 5)·결정적 재개. |
| `stephost_bridge.py` | `uahf/framework/loop/step-host/` 중립 모듈의 **무수정 import 경로**(평면 import 를 위한 sys.path 조작은 orchestration 쪽에서만). |
| `revision_schema.json` | RevisionEvent 직렬화 형태 정의(실값 없음 — step-host `config_schema.json` 관례 동형). |
| `tests/` | 모의 invoker 기반 통합 테스트(외부 의존 0). |

**아직 없는 것(후속 단계).** 게이트 정책 평가 엔진(`gates.py`)·할당·모델 선택
(`allocation.py`)·Artifact Registry(`artifacts.py`)·Adapter 바인딩은 S3~S5 소관이며 이번
단계 범위 밖이다(설계 §5). 게이트 승인 이벤트는 이 단계에서 **외부(상위/드라이버)가
append 하는 데이터**이며, orchestrator 는 그 실재만 검증한다.

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
