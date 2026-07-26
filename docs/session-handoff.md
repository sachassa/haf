# 세션 핸드오프 (UAF 레벨 정본 · 단일 live 문서)

작성: Advisor · 2026-07-17 · 최근 갱신: 2026-07-26
용도: 새 세션은 **본 파일 하나로 상태를 인수**한다. 원문 전체 정독 강제 없음 — demand-driven(§단위·필요 시점) 규칙을 따른다. (물리 발화 = `/uaf-continue`)
지위: `docs/artifact-lifecycle-policy.md` §6이 정한 **UAF 레벨 단일 live 핸드오프**다. 단수·제자리 갱신이며 버전별 파일을 만들지 않는다. **과거 상태는 git 이력이 정본이다** — `git log -- docs/session-handoff.md`(전신 `docs/next-session-prompt.md` 포함). 종전 갱신 블록 (1)~(20)과 종료 트랙(Performance Tuning·산출물 수명) 서술은 앵커 `90ca19c` 에 보존되며 본 파일은 **현행 스냅샷 1부**만 담는다.

`uaf-allow-legacy:` 본 파일은 종전 갱신 블록의 실측 수치·완전성 문면을 인용 보존한다 — 판정 근거는 각 run 원장·트랙 원장(`ARCHIVE.md` 앵커)이며 본 파일이 판정 근거가 아니다(정책 §4 — 핸드오프는 규칙의 출처로 인용하지 않는다).

---

## §A. 현행 상태 (갱신 2026-07-26(21))

**auto-percenty UAF 정식 편입(Contract v1·SD 7종) + 첫 엔진 run `impl-auto-percenty-p1` 완주 = 갱신(20) 실 run 실증 소화. 신규 결함 후보 2 + 절차 비례화 트랙 신설. ★다음 순위 = Advisor 배정(사용자 위임).**

성립 조건 2 이행: ① 엔진 경유(`/uaf-implement` — Advisor 직접 위임 디스패치 0) ② 첫 행동 = `auto-percenty/START-HERE.md` 전문 정독.

**파이프라인 전 구간 실주행**: Entry(형태 B 로더·행 6 brownfield — Contract 부재 실측) → Brownfield Discovery(`discovery-data/events/brownfield-r005/` — 스캔[Advisor 정독+Explore digest]·인터뷰 4문/40[카드 묶음]·G2 승인) → **Contract v1 발행**(`auto-percenty/.claude/project-contract/project-contract.v1.md` · pc-auto-percenty-001 — 키워드 영역 한정·하루 100상품 유지·목표↔상한 충돌 = RISK-1·미결 판단 8건 run 이월, 사용자 결정 4건) → **SD**(`solution-design-data/events/maturation-auto-percenty-r001/` — 단일 Worker 위임 7종 docs·Advisor CP2 Pass·화면 6종 classExclusions 사용자 확인·design_completeness exit 0 — B-3 옵션 B 원장 의무 첫 실사용) → **엔진 run**(proposal→user 게이트→4 task 승격→5단위 Passed 5/5·invokes 9·완주 exit 0). Advisor 독립 재검증 = milestone 5검사 재실행 PASS·audit 회귀 exit 3(위반 1/25 = 기지 B뿐 — 신규 3축 기존 원장 오탐 0)·probe-usage 40/100 불변(**run 중 쿠팡 실접속 0**). 산출(제품) = 모델명 기계 게이트·audit 정합화(스펙수치·ACCESSORY·모델명)·A/B 실험 하네스(라이브 미실행). `uaf-verified:` 판정 근거 = 런처 로그 2본·heartbeat 실기 2회·invoke 원장 16파일·milestone/audit Advisor 재실행·probe-usage 대조. 스윕 범위 = run 원장 + auto-percenty 워킹트리.

**관측 체크리스트 판정** — 자동 발화 5종 = **5/5 관측**: heartbeat 실기 갱신 ✅ · `[INVOKES] total=` 정상(4→9) ✅ · 게이트 렌더 gate_id 상시 지목 ✅(자동 출력 문면 복사 실행으로 해소 성공) · Planner 3규율 ✅(milestone 상호 대조 AC 3검사 실구현·실출력 픽스처[T20 실캡처+PROVENANCE+미검증 신고 3항]·timeout 선택 키[ab 단위 5400 — 대형 단위 판별 타당]) · **Verifier AC 적정성 축 ✅ 실 Fail 1건**(proposal done "문자열 존재만 검사" 지적 → 실호출·값 assert 재작업 = 백로그 O 실증). 조건 발화 3종: `[REWORK-NOTE]` **실발화 ✅**(재작업 단위 열거·지시 인용·스윕 힌트 = 백로그 M 실증) · `--response` 조건 주입 = **미관측**(사용자 조건 없음 승인 — 억지 유발 금지) · per-unit timeout 재기입 = 조건 발화 ✅·**재기입 값 판정 불가**(아래 결함 ②).

**신규 결함 후보 2**: **① Planner seed sentinel 문면 미고정** — proposal이 delegation 참조형 sentinel을 변형 문면("상위(부모) task 필드 전문과 동일…")으로 산출 → `resolve_gate` 검증-먼저 fail-closed 차단(원장 무오염 — 게이트 정확 작동) → Advisor 수기 정규화 필요(백업+provenance = `auto-percenty/impl-plan.SENTINEL-FIX-PROVENANCE.md`). 수정 후보 = `contract_to_graph.py` seed 프롬프트에 정확 sentinel 문면(`위 task 필드와 동일`/`위 done 필드와 동일`) 고정. **② UnitTimeoutInvoker 재기입 관측 신호 부재** — invoke 원장(`logs/invoke-*.json`)에 request.timeout 미기록이라 재기입 값의 라이브 실증이 원장으로 불가(갱신(18) 미검증 축이 이 부재로 잔존). 수정 후보 = invoke 기록에 timeout 필드 1개 추가.

**★ 절차 비례화(Process Proportionality) 트랙 신설(사용자 피드백 2026-07-26)**: "단순 수정·단순 테스트에 풀 프로세스는 가성비·시간효율 문제 — 경량 프로젝트 간소 절차/엔터프라이즈 복잡 절차". 정본 = 메모리 `feedback-uaf-process-proportionality`. 방향 = 불변(원장 0건 금지·게이트 확정 권위·검증 하한) 유지·**절차 두께만 Policy as Data 레버로 비례화**(변경 등급 신호→경량 레인[경량 원장+직접 위임+스크립트 AC]·SD defaultRequiredSet 복잡도 프로파일·CP2 차등[cp2ModelSlots 기존 장치]·성숙 brownfield 인터뷰 최소). 실측 근거 = 갱신(21) 세션(경량 코드 작업에 Entry→Discovery→Contract→SD 7종→엔진 고정비가 본작업보다 큼 — 단 Contract·SD는 1회성 셋업이라 차회부터 재사용).

### ★ 다음 착수 순위 = Advisor 배정(사용자 위임 2026-07-26 "순서 너가 정하는데로 할게")

1. **경량 정비 묶음** — 신규 결함 ①(seed sentinel 문면 고정)+②(invoke 원장 timeout 필드). 수정 소폭·다음 실 run이 즉시 재검증.
2. **절차 비례화 트랙** — 사용자 피드백 직결·최대 임팩트. 레인 기준(변경 등급 신호)은 사용자 게이트로 확정.
3. **SD 스킵 브리지**(스킵↔구현 게이트 충돌 — 경량 레인의 전제) → 4. **SD manifest 배선 3건**(같은 SD 계열) → 5. **커버리지 강제**(θ≠커버리지) → 6. **.claude md 슬림화 실행**(분석 완결분·무게 절감 계열) → 7. **Q·R 기계 강제** → 8. **§DC-8(a)·02 개정** → 9. **상류 바인딩 2차**.

(제품 트랙 별축 — 사용자 참여 시 최우선 인터럽트: **auto-percenty 웨이브 실전 ≤30상품**[선행 = 미결 판단 8건 카드·정본 = auto-percenty/docs/project-plan.md §4 표]+**A/B 라이브 실측**[예산 안·두 카드 동시 금지] · yt-stt M4-b 판단.)

커밋 상태: auto-percenty(Contract·SD·run 산출·provenance) + 본 저장소(discovery r005·SD r001 원장·run 원장) 커밋됨. **auto-percenty는 원격 없음(푸시 대기 유지)**.

---

## §B. 이월·미해소 통합 (갱신(19)~(21) + §DC 산재분 병합 — 중복 제거)

### B-1. 다음 실 run 관측 좌표 (하네스 개선분의 라이브 실증)

- 갱신(21) run 에서 **미관측**으로 남은 축: `--response` 조건 주입(조건부 승인할 일이 실제로 있을 때만 — 억지 유발 금지) · per-unit timeout **재기입 값** 실증(원장 신호 부재 = 신규 결함 후보 ②가 선결).
- 갱신(19) N 트랙 미검증 축: 조건의 **실 프롬프트 렌더 문면** · Worker 조건 실준수(판정 축은 백로그 R 계열로 유보) · `render_gates` 표면에 "조건부 승인 가능" 인지 경로 부재(저임팩트) · 조건 **누적** 시나리오(현행 구조 게이트 1회 해소 전제) · 소비 프로젝트 레거시 run 혼재.
- 갱신(20) M·O 트랙 미검증 축: 대형 워크스페이스 스윕 성능 · 다단위 run 의 `[REWORK-NOTE]`↔스윕 연결 · `--append-system-prompt` argv 길이 한계.
- 갱신(17)~(18) 잔여: 실 LLM invoker 경유 **다중 escalation** run 미수행 · 한글 `gate_id` 셸 인용 거동 미실측(엔진 파생 규칙상 ASCII — 발생 시 재심) · Planner 의 `timeout` 선택 키 판별 타당성(갱신(21)에서 1건 관측·표본 1).

### B-2. 미해소 하네스 결함 (순위 = §A 다음 착수 목록)

- **커버리지 강제** — 인터뷰 필수 축 기계 강제 0(θ≠커버리지 역설). 상세 = 메모리 `uaf-coverage-enforcement-gap`.
- **SD manifest 배선 3건** — manifest 스키마↔코드 해석 모순·seed 단일파일 가정. 메모리 `uaf-design-manifest-path-defect`.
- **SD 스킵 브리지** — Solution Design 스킵↔구현 게이트 정면 충돌·브리지 코드 0. 메모리 `uaf-solution-design-skip-gap`.
- **백로그 Q·R 기계 강제** — 현재 절차 층만(Q = seed 제약↔브리프 실행 AC 대조 미도입 · R = 정적 CP2 의 done AC 간 동적 상충 무검출). 정본 = `docs/post-tuning-improvement-backlog.md` §Q·§R 「강제 지점」 행.
- **상류 바인딩 2차(디커플링)** — 1차 완결·2차 대기. 메모리 `uahf-binding-placement-defect`.
- **위임 규율 잔여 2건** — B-4 **실시간 전파**(fresh-context 수임 Agent 간 통신 채널 부재 = 환경 제약. 회수 시점 대조로 갈음·재심 = 통신 표면 등장 시) · B-3 **기계 차단**(설계 산출 Write 의 결정적 식별 불가 = 미도입 사유 기록. 재심 = SD 실행 호스팅 도입 시 엔진 게이트 승격). B-0~B-5 6건은 종결 — 메모리 `uaf-delegation-enforcement-gap`.
- **메모리 소급 감사** — "강제 필요한데 메모리에만 있는" 항목 재검토(갱신(15) 미완 항 — 앵커 `90ca19c` 승계). 「강제 없는 규율 신설 금지」 불변은 신설만 막고, 기존 메모리의 소급 감사는 별도 미착수 작업이다.
- **명명 금지 규범(AI·모델·제품 기능 축) 정본 소유 공백** — structure.md §5 C-3이 Adapter 경계를 명시 제외해 각 바인딩의 문서 소유 규범으로 병존 중(사용자 결정 2026-07-26 = 현상 유지). 재심 좌표 = structure.md §5 차기 계약 개정 시 Adapter 경계 조항으로 승격 검토(유형 A 절차).

### B-3. §DC 트랙 잔여 (완결 항목은 본 파일에서 제거 — 앵커 `90ca19c`)

- **§DC-8 (a)** — 03 필수 코어 필드에 **접점 구조 필드** 추가(결정적 검출·거버넌스 무게 큼). 옵션 (b)(`classExclusions{reason,confirmedBy}` 확인 요구)는 해소됨.
- **§DC-8 runtime 관찰 1건** — `replaceable=false` 근거의 게이트 표면화 부재(저임팩트).
- **02 개정 트랙(U4 대안 C)** — 인터뷰 강제 깊이 바닥. Frozen 02 충돌 판정 때문에 대안 A+B(θ 전 차원 +0.05·스킬 비구속 관행 3종)로 갈음한 잔여.
- **오케스트레이션 Stage B** — 실코드 산출은 다음 소비 프로젝트 몫. 메모리 `uaf-orchestration-wiring-gap`.
- 상세·완결 근거 = 메모리 `uaf-design-completeness-gap` · `uaf-accountable-autonomy-principle`.

### B-4. §DC 좌표·정본 포인터 (착수용)

| 항목 | 위치 |
|---|---|
| 실측 산출물(백엔드만 — DC-1 증상 원본) | `git show 4934bc8:tms-system/impl-plan.json` (tms 트랙 종료·삭제 — `ARCHIVE.md`) |
| seed 컴파일러·게이트 정책 | `orchestration/adapters/claude/contract_to_graph.py` |
| 강제 대상 정본 | `planning/specs/04-solution-design.md` §3.5 |
| 비정본 카탈로그 (DC-8 결론 = 승격 불필요) | `planning/docs/appendix/projection-catalog.md` |
| 훅 메커니즘 (차단형 PreToolUse) | `.claude/settings.json` · `.claude/hooks/binary_state_guard.py` · `orchestration/adapters/claude/pretooluse_design_guard.py` |
| 필수 산출물·요소 강제 체커 | `orchestration/adapters/claude/design_completeness.py` |

### B-5. 성능·측정 트랙 잔여 (Performance Tuning 종료 2026-07-14 — 결정 기록은 앵커 `90ca19c`)

- **불가침 앵커**: Baseline = UAHF `ad451ee` · consumer `dd2fd73` · Freeze `013e532`. Baseline run evidence 는 `ARCHIVE.md` 앵커 열람.
- **consumer(`uahf-control-plane`) 워킹트리의 사용자 미커밋 변경분 = 보존·수정 금지**(2026-07-14 사용자 승인).
- **측정 인프라 유지 + 실사용 누적**: 신규 orchestration run 마다 `collect_metrics.py`(bundle_payload 포함)·`verify_run.py` 를 신규 runId 산출물에 실행한다. 산출물 등급 = ephemeral(정책 §3). ⚠ `collect_metrics.main()` 은 aggregate 를 덮어쓰므로 순진한 자동 호출은 baseline aggregate 를 파괴한다.
- **재개 조건**: 실사용에서 병목이 **반복 관찰**되면 누적 데이터를 근거로 별도 트랙을 새로 연다(느낌 기반 재개 금지 — Measurement First).
- 보류·대기: T5 Gate Notification(그룹 B·C 지표 전용) · T2 evidence 재사용 섀도 대조 첫 실적용 · descriptor-aware CP2(`cp2ModelSlots`) 첫 사용 · Skill Extraction P1(백로그 §G 시딩) · 백로그 §H 재개 트리거.
- **트랙 후보(우선순위 미확정·확정 권위는 사용자)**: **Interview Entry-to-Runtime Audit**(사용자 지정 2026-07-14 — 차순위 유지). 정의·범위·성공 기준은 착수 세션의 사용자 지시로 확정하며 본 파일은 명칭·시작점만 기록한다.

### B-6. 제품 트랙 잔여 (상세 정본 = 메모리)

- **auto-percenty** — 미결 판단 8건(Contract v1 발행 시 run 이월·카드 제시 대상) · 웨이브 실전 ≤30상품 · A/B 라이브 실측 · 원격 없음(푸시 대기). ⛔ 만지기 전 `auto-percenty/START-HERE.md` 필독. 메모리 `uaf-product-auto-percenty`.
- **yt-stt** — M4-b 판단(선행 근거 = 잔여 오독 8건 실물) · `OQ-M4-A`·`OQ-M1-A` 미해소(합격선 발명 금지) · RISK-9·10·11 미해결 · F3′ dedup(fix-5) · JS 런타임 제품 반영 · `duration=0` realtime 게이트 무력 · `out/` 표본 미커밋 판단. 메모리 `uaf-product-yt-stt`.
- **복원 불가 기록**: yt-stt 영향 감사 미결정 20건은 집계 숫자만 잔존한다(위임 산출 유실 금지 불변의 근거 사례).

---

## §C. 갱신 규율 (stale 재발 방지)

- **각 단계·트랙 경계 커밋에 본 파일 갱신을 포함한다.** 갱신은 **제자리 교체**이며 블록 누적이 아니다 — 과거 상태는 `git log -- docs/session-handoff.md` 가 정본이다(정책 §6).
- 본 파일은 값 중복 최소·정본 포인터 우선. 본 파일과 정본이 충돌하면 **정본**(git log·해당 spec/binding/백로그)이 우선한다.
- 본 파일은 어떤 문서의 규칙 출처(판례)로도 인용되지 않는다 — 규칙 근거는 정본 §·`L-XX`·`mi-XXXX` 로만 표기한다(정책 §4).

## §D. 정본 포인터

| 항목 | 위치 |
|---|---|
| 에이전트 거버넌스·불변 | `.claude/AGENT.md` |
| 이 환경 운용 배선(훅·관측·2층) | `.claude/CLAUDE.md` |
| 위임·보고 규약 | `docs/delegation-protocol.md` |
| 검증 체크리스트(게이트 A~D·§5.6~§5.8) | `docs/verification-checklist.md` |
| 산출물 수명·삭제·앵커 인용 정책 | `docs/artifact-lifecycle-policy.md` |
| 아카이브 원장 (앵커 열람) | `ARCHIVE.md` |
| 하네스 개선 백로그 (A~R) | `docs/post-tuning-improvement-backlog.md` |
| 오케스트레이션 계약·물리 배선 | `orchestration/specs/05-project-orchestration.md` · `orchestration/adapters/claude/project-orchestration-binding.md` |
| 측정·검증 도구 (유지 대상) | `orchestration-data/e2e/{run_all_tests.py,collect_metrics.py,verify_run.py,delegation_check.py}` |
| Risk Routing 정책 | `orchestration-data/e2e/policy/{allocation.json,README.md}` |
| UAHF Contract | `discovery-data/contracts/uahf/project-contract.v3.md` |
| 과거 핸드오프·종료 트랙 원장 | git 이력(`git log -- docs/session-handoff.md docs/next-session-prompt.md`) · `ARCHIVE.md` 앵커 |
