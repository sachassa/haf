# framework/loop/step-host — provider-중립 Step Host (경계 문서)

## 위상

Step Host 는 **판단하지 않는 기계 구동자**다. 03 사이클 구동과 07 디스패치·순서 규칙을
사람 없이 무인으로 트리거·반복만 하며, 의미 판단(완료·실패·차단·검증·승인)은 하지
않는다. 그 판단은 전부 실행 단위·Verifier·Advisor·사람이 소유하고, Host 는 반환값을
소비만 한다.

이 디렉터리는 그 구동자의 **provider-중립 실현**이다 — 실행 표면(신규 컨텍스트 기동·권한
옵션 등)은 전부 `invoker` 추상 인터페이스 너머의 Adapter 구현체 소관이며, 이 코드에는
특정 실행 환경·provider 토큰을 두지 않는다. 구현체는 config 의 모듈 경로 문자열로만
로드한다.

## 계약 정본 (프로토콜 §7.2 바인딩 지점 포인터)

이 코드가 준수하는 계약의 정본은 이 디렉터리가 아니라 다음 문서다:

- `framework/runtime/step-hosting-protocol.md` — Step Host 의 provider-중립 계약 전부.
  - §2 위상 · §3 Step 계약/Fresh Context · §4 상태 파생·결정적 재개·4 국면 ·
    §5 재시도·피드백·CP1~CP3 · §6 진입 판정·Autonomy·게이트 등급 분리 · §7.1 SH-INV 8건.
- 물리 실현(직렬화 형식·run 데이터 백엔드 경로·정지 신호 값·Autonomy→실행 옵션 매핑·
  모델/역할 슬롯 지정 의미)은 이 코드가 아니라 **Adapter Binding 문서** 소관이다
  (프로토콜 §7.2). 이 코드는 그 지점을 추상(EventStore·Invoker·stop_handler·config)으로
  열어 둔다.

## 구성

| 파일 | 책임 |
|---|---|
| `step.py` | Step 로드·유효성 검사(필수 필드 누락 → 디스패치 금지)·Step Contract 뷰. |
| `events.py` | append-only 이벤트 로그(10필드)·상태 파생 뷰(5종)·EventStore 추상. |
| `bundle.py` | Fresh Context 번들 조립(Memory 직접 접근 코드 경로 없음). |
| `invoker.py` | 신규 실행 컨텍스트 기동 추상 인터페이스·config 모듈 경로 로더. |
| `host.py` | 실행 루프 4 국면·결정적 재개·재시도·게이트 등급 분리·정지 신호 위임. |
| `config_schema.json` | config 형태 정의(실값 없음). |
| `tests/` | stub invoker 기반 자체 테스트(외부 의존 0). |

## 불변 (요지)

- 판단 0 (SH-INV-1) · append-only 파생 뷰 (SH-INV-2) · 결정적 재개 (SH-INV-3) ·
  게이트 등급 분리 — 어떤 policy 값에서도 CP2 우회 없음·Escalated 정지 (SH-INV-4) ·
  Memory 직접 접근 금지 (SH-INV-5) · 컨텍스트 격리 (SH-INV-8).

## 테스트 실행

이 디렉터리의 모듈은 평면(flat) 임포트를 쓰므로, 테스트 파일이 이 디렉터리를
`sys.path` 에 넣고 실행한다. 외부 패키지 의존은 없다(표준 라이브러리 `unittest` 만).

```
python framework/loop/step-host/tests/test_step_host.py
```

또는 저장소 루트에서:

```
python uahf/framework/loop/step-host/tests/test_step_host.py
```
