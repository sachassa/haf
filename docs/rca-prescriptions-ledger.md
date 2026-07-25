# RCA 처방 트랙 원장 (2026-07-26) — evidence

지위: 위임 보고 산출의 원장 승격(`docs/delegation-protocol.md` §2.7 · AGENT.md §Invariants 위임 산출 유실 금지). 수명 등급 = **evidence**(수명·삭제·인용 = `docs/artifact-lifecycle-policy.md` §2·§3·§5). 본 문서의 위임 보고 항목은 **수임 Agent의 주장을 회수한 것이며 검증 결과가 아니다** — 판정은 CP2(독립 검증)·CP3(승인)가 별도 수행하고 그 결과를 이 파일에 追記한다.

트랙 범위: 2026-07-26 UAF 자체 RCA 처방 1~5 (사용자 지시 "처방 모두 진행"). 처방 2·3·4(거버넌스 문면)와 처방 5(백로그 P·Q·R 전입)는 Advisor 직접 수행 — 좌표는 세션 핸드오프 갱신 블록이 소유한다.

---

## W-hook — binary_state_guard 백로그 검사 확장 (보고 회수 2026-07-26)

- **주장 요약**: guard `+86/-0` · 신설 테스트 18종 OK(`PYTHONIOENCODING=utf-8` 명시·EXIT=0) · 기존 검사 로직 문면 무변(numstat 삭제 0) · deny 계약 동형(stdin 주입 E2E 1건).
- **open_questions 승격**:
  1. **백로그 전체 파일 Write는 레거시 15항목(A~O)의 「강제 지점」 행 부재로 차단된다**(수임 Agent 실측 주장 — 헤딩 18개 중 15개 부재). → **Advisor 결정(2026-07-26): 구현 유지.** 레거시 항목은 "신규부터 + 닿는 것만" 원칙(2026-07-21 사용자 결정과 동형)대로 그 항목을 실제로 고칠 때 「강제 지점」을 기입한다. 전체 파일 Write가 필요한 예외 상황은 `uaf-allow-legacy:` 마커로 사유를 기록하고 통과한다.
  2. 헤딩 패턴은 대문자 `## X.`형(1~3자)만 검사 — 현행 파일 관례와 일치. 소문자·번호형 헤딩 관례가 생기면 재확인 좌표.
- **부수 판명(주장)**: 2026-07-21 기록의 "단위 검증 16종"은 테스트 파일로 잔존하지 않음(수임 Agent 저장소 스윕 주장 — 검색 범위는 보고 원문 참조). 회귀 8종 + 순수 함수 4종으로 대체 커버했다고 보고.
- **적용 기본값**: 없음(위임 문면 그대로 구현했다고 보고).
- **CP2 판정(Advisor 독립 검증 2026-07-26) = Pass.** 근거: ① 테스트 18종 독립 재실행 OK·EXIT=0(수임 Agent 출력을 근거로 쓰지 않고 직접 실행) ② `git diff` 전문 판독 — 추가 86줄·삭제 0줄·기존 검사 로직 무촉 확증 ③ **라이브 실증 3건**: 실파일 Edit에 토큰 없는 신규 항목 → deny(사유 문면 정확) · 스크래치패드 동명 파일 Write 토큰 없는 항목 → deny · 「강제 지점: 미도입 — 사유」 행 포함 항목 → 통과. 검사 범위 = 이 3경로 + 테스트 18종이며 MultiEdit 라이브 경로는 별도 실증하지 않음(단위 테스트로만 커버).
- **관찰(비차단·한계 명시)**: 토큰 포함 검사는 **바닥 장치**다 — 항목 본문이 「강제 지점」을 결정 없이 언급만 해도 기계 검사는 통과한다(Advisor의 1차 라이브 테스트 입력이 정확히 이 경로로 통과했음을 실측). 의미 판정은 게이트·리뷰 층 소관이며 훅은 존재 최후방어다(§DC-3 이중방어 구분과 동형).
- **fail-open 경로 관찰(비차단)**: 백로그 검사 내부 예외 시 `_fail_open`이 즉시 허용을 확정하므로 그 호출 1건에 한해 기존 어휘 검사가 생략된다 — fail-open 철학 안의 의도된 순서이며 정상 경로 무영향(diff 판독 근거).

---

## W-J — 엔진 에스컬레이션 해소 채널 (보고 회수 2026-07-26)

- **주장 요약**: D1(요구 이벤트+pending_gates)·D2(rework 되돌림)·D3(response 전파 — last_failure_ref→번들 전달 실측 1)·D4(escalated stop-signal·gate 분기 무변)·D5(resume --retry-limit 반영)·D6(binding §3.4 신설) 전부 구현. gate_id 스킴 = `gate-unit-<id>::exec-escalation`(접두 보존·approvalState 파생 비간섭·재개 안정). 신규 테스트 17건·3트리 295건(175+97+23) 실패 0. 기존 테스트 문면 수정 0. 브리프 좌표·성질 불일치 0 보고.
- **open_questions 승격 + Advisor 결정**:
  1. `recover_gate`는 같은 gateKind pending 중 첫 항목만 반환(기존 코드·무수정) — 다중 escalation 공존 시 특정 지목 불가. → **결정: 이번 트랙에서 미도입.** `--gate-id` 옵션은 백로그 §J 잔여로 등재한다.
  2. 여러 단위가 동시에 Escalated일 때 그중 하나만 해소하면, 그 단위의 되돌림 실행은 나머지 해소 이후로 미뤄진다(SH-INV-4 보존의 귀결·정보 손실 없음). → **결정: 거동 수용.** 마감 시 binding §3.4에 한 줄 명시한다.
  3. 백로그 §J 상태 갱신 미수행(diff 범위 제약 준수). → **결정: CP3 후 Advisor가 갱신한다.**
  4. `resolve_structural`(user_decision)에는 response 동봉 미적용 — 백로그 N(조건부 승인 채널)의 소관이며 이번 범위 밖. → **결정: 수용·N 미해소 유지.**
- **CP2 판정(Advisor 독립 검증 2026-07-26) = Pass.** 근거: ① 3트리 테스트 독립 재실행 175+97+23=295 OK·EXIT=0×3(수임 출력 불신·직접 실행) ② 소스 diff 4파일 전문 판독 — D1~D6 설계 정합·판단 0 원칙 보존(적격성은 gates.py 소유)·가법 확장(response 미지정 시 ref 종전 동일)·레거시 분기 보존(gate_policy None) ③ 접합부 왕복 테스트 본문 판독 — 런처 산출 stop-signal **실물**→recover_gate→resolve CLI **실호출**→엔진 재기동→invoke>0→원장에서 gate-rework·response 직접 파싱(§5.7 충족) ④ 변경 경계 — git status 목록에 uahf/**·specs/**·Frozen 부재(검색 범위 = git status 목록). **미검증 축(§5.8)**: per-unit timeout(백로그 J ③ — 브리프에서 명시 제외·사유 기록됨) · 실 CLI invoker 경로(오프라인 스텁만 — 실 run은 다음 소비 프로젝트 실사용에서 검증). 관찰(비차단): 왕복 테스트 457행 단언은 456행과 동어반복(무해).

---

## W-L — 엔진 관측 계약 (보고 회수 2026-07-26)

- **주장 요약**: HeartbeatInvoker 래퍼(invoke 경계 기록·failure isolation A-B 대조 실증·속성 투과)·failure.json(미처리 예외 시 필드 6종·재raise로 은폐 0)·슬러그 상한 48+sha8(`fold_slug` — 48자 이하 바이트 동일·P 크래시 케이스 재현→해소 실증)·--resume 부재 오류에 실존 후보 목록·uaf-implement.md §2 정정+종료코드 표·binding §5.8 신설. 신규 테스트 17건·3트리 312건(175+114+23) OK. 직전 위임 반영분(escalated 분기) 바이트 동일 확증 보고.
- **open_questions 승격 + Advisor 결정**:
  1. per-unit timeout(백로그 L §Desired 4)은 미해소 잔존 — binding §5.8에 이월 명시했다고 보고. → **결정: 수용.** 산정 규칙은 별도 설계 트랙 소관(DEFAULT_TIMEOUT 2400은 기반영).
  2. heartbeat 필드가 백로그 문면({ts, current_unit, stage, elapsed_s, invokes})과 다르게 {ts, stage, invokes, request_hint, pid}로 확정됨 — Advisor 설계 결정이며 Worker는 따름. → **결정: 수용.** 사유: 런처는 단위 경계·경과시간을 소유하지 않고, F2 탐지의 실사용은 "마지막 ts와 현재 시각의 차"이므로 elapsed_s는 관측자 파생값이다. 백로그 L 마감 표기에 이 축약을 병기한다.
  3. prepare_run 구간(run_dir 미확정) 예외는 failure.json 없이 [FAILURE-SKIP] stderr + 재raise. → **결정: 수용**(임의 경로 추측 금지·은폐 0 유지). 공용 경로 도입은 비요구.
  4. 실 CLI invoker를 감싼 경로는 스텁으로만 검증 — 다음 실 run에서 `[INVOKES] total=` 정상 출력이 관측 좌표. → **결정: 수용·다음 소비 프로젝트 실 run에서 확인.**
- **CP2 판정(Advisor 독립 검증 2026-07-26) = Pass.** 근거: ① 3트리 독립 재실행 175+114+23=312 OK·EXIT=0×3 ② 소스 판독 — HeartbeatInvoker 인터페이스 투과(`__getattr__` 무한재귀 방지 포함)·`_record_failure` 재raise 경로·`_drive` 분리·resume 힌트가 기존 [ERR] 라인 보존 후 가법·**fold_slug 공통 규칙을 `_slug`와 `slugify_run_id` 양쪽이 재사용**(런처↔컴파일러 슬러그 접합부 일치 — §5.7 취지 정합) ③ `py_compile` 2파일 통과 ④ `uaf-implement.md` §2·binding §5.8 문면 판독 — 종료코드 표·`--run-id` 함정 문단·관측 파일 계약 실재. **미검증 축(§5.8)**: 실 CLI invoker 래핑 경로(오프라인 — 다음 실 run에서 `[INVOKES] total=` 표시로 관측) · per-unit timeout(범위 밖·이월).
