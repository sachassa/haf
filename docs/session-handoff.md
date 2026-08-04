# 세션 핸드오프 (UAF 레벨 정본 · 단일 live 문서)

작성: Advisor · 2026-07-17 · 최근 갱신: 2026-07-30
용도: 새 세션은 **본 파일 하나로 상태를 인수**한다. 원문 전체 정독 강제 없음 — demand-driven(§단위·필요 시점) 규칙을 따른다. (물리 발화 = `/uaf-continue`)
지위: `docs/artifact-lifecycle-policy.md` §6이 정한 **UAF 레벨 단일 live 핸드오프**다. 단수·제자리 갱신이며 버전별 파일을 만들지 않는다. **과거 상태는 git 이력이 정본이다** — `git log -- docs/session-handoff.md`(전신 `docs/next-session-prompt.md` 포함). 종전 갱신 블록 (1)~(20)과 종료 트랙(Performance Tuning·산출물 수명) 서술은 앵커 `90ca19c` 에 보존되며 본 파일은 **현행 스냅샷 1부**만 담는다.

`uaf-allow-legacy:` 본 파일은 종전 갱신 블록의 실측 수치·완전성 문면을 인용 보존한다 — 판정 근거는 각 run 원장·트랙 원장(`ARCHIVE.md` 앵커)이며 본 파일이 판정 근거가 아니다(정책 §4 — 핸드오프는 규칙의 출처로 인용하지 않는다).

---

## §A. 현행 상태 (갱신 2026-08-03(28))

**갱신(29) yt-stt Contract v5 — 실측 반증이 계약을 뒤집고 커버리지 게이트를 열었다(2026-08-04 · yt-stt `214c4bf`→`21a7bc7` 4커밋 푸시 · UAF `895cef3`).** M4-b 착수 판단으로 화면을 열었다가 **v4 D5 삭제 근거의 성립 조건**을 찾았다 — "유튜브가 자막 텍스트를 직접 준다"는 **등재 수동 자막이 있는 영상에서만 참**이고, 등재 0 인 영상이 하필 번인 자막을 갖는다(삭제가 경로를 가장 필요한 지점에서 없앴다). 실측 = 3원 대조(STT `조치로`/구글 ASR `쫓내는`/화면 `쇼츠로` — 기계 2종이 서로 다르게 틀리고 사람 산출만 맞음) · 전문 대조 일치율 93.5%·차이 19곳(STT 오인식 8·자막 생략 3) · 비용 STT 대비 2~3% · 광역 판독은 같은 슬라이드 2프레임이 다르게 읽힘(→ **참고 등급 유지가 실측으로 정당화**·D3 무수정). 결정 4건 확정 → **v5 발행**(append-only 보존) → 판독 모듈+팩트 배선(공집합이던 표본이 **팩트 83줄** 확보) → Projection 8종 개정.

- **⛔→✅ 커버리지 게이트 첫 실차단·해소.** v5 Write 가 `deny`(원장 부재 — yt-stt Contract 07-21 발행 ↔ 커버리지 강제 07-29 도입). `discovery-data/events/` 에 yt-stt run 기록 부재라 **증거 있는 소급 불가**였고, 하필 `structure-delivery-direction`(highImpact) **미심문이 이 규칙의 도입 사례 자체**였다. 해소 = **실제 인터뷰 수행** — Advisor 가 v1~v4 문면에서 축 9종 답 초안 작성 → 사용자 카드 일괄 확인 → `user-stated` 로 원장 산출. **확인 없이 채우면 `inferred` 라 체커가 거부**함을 변이로 확증(9종 KILLED·무변경만 통과). → **갱신(26) 이월 ② "외부 소비 프로젝트 원장 소급 여부" = yt-stt 분 해소**(다른 프로젝트는 미결 유지).
- **⭐ 레인은 사이클이 아니라 작업 단위마다 갈린다** — 같은 사이클에서 Contract 발행=standard(접점 1)/판독 구현=lightweight(접점 0). 원장 = `impl-yt-stt-burntin-lite`(events 15·revisions 4·artifacts 5·`verify_run` PASS) → **B-1 경량 레인 2회차 실운용**.
- **⭐ 오프라인 단언으로 안 드러나는 층 재적중** — 띠 검출 첫 구현("표본 공통 행 교집합")이 실행에서 산출 0. 자막 박스 세로 위치가 프레임마다 달라 교집합이 13행으로 쪼그라들었다. **원인은 Advisor 자신의 편향 표본**(손으로 고른 18장이 2줄 자막에 몰림). 임계값은 실측 분리 간격 안쪽에 놓았다(83% ↔ 33% 사이 0.60).
- 재적중 결함 2 = `verify_run` 화이트리스트의 `gate-resolution-provenance` 미수용(**OQ-PO-B7 그대로**) · Bash 지속 CWD 변경으로 PreToolUse 훅 상대경로 해소 실패 → Write 차단(§B-2 등재분).
- `uaf-verified:` 게이트 11종 exit 0 · 독립 검증 28/28(음성 대조 5) · 배선 검증 13/13 · append-only 보존(v1~v4 무변경). **스윕 범위** = yt-stt `scripts/`·`docs/` 트리·게이트 11종·표본 2영상이며 다른 채널 표본은 범위 밖.

**갱신(28) 첫 경량 레인 실운용(2026-08-03 · yt-stt `dfc426e`→amend `e77b5b9`).** 게이트 시점 의존 단언 3곳 → 실행 전·후 축자 불변 대조로 재정초 · 실행 진입점 `scripts/run.py` 신설. 경량 원장 `impl-yt-stt-gatefix-cli-lite`(events 16·revisions 3·artifacts 11·findings 0). 브리프 결함 9건 전부 Advisor 귀속·Worker 코드 결함 0. 전문 = 커밋 메시지·메모리 `uaf-product-yt-stt`.

**갱신(27) 커밋 시점 재퇴적 방어 배선(2026-07-30 — 전문 = 앵커 `81f2ce3`).** `.githooks/pre-commit` 신설(md 예산·이력 재퇴적 가드를 커밋 직전 실행·fail-open·우회 = `--no-verify`+사유) · 배선 = `core.hooksPath .githooks`(클론당 1회 로컬 설정 · 사망은 침묵하므로 SessionStart `githooks-wiring-guard.sh` 가법). 후속 확장 = `binary_staged_check.py`(스테이징 diff 추가 행 이진 원칙 검사) · `memory_index_guard.py`(메모리 색인 6,000B 초과 Write/Edit 거부·축소 허용). 실호출 검증 완료.

**갱신(26) 커버리지 강제 트랙 완결(2026-07-29 · Wave 0~4 — 전문 = 앵커 `62838fe`·`e00b942`).** 결함 = 인터뷰 필수 질문 축이 기계 강제되지 않음(θ≠커버리지 역설 — Confidence 는 **물어본 것에 대해서만** 계산되므로 미심문 축이 확신을 떨어뜨리지 않는다). 실사례 = yt-stt 전달 플랫폼 미심문. Wave 0 spec 02 v1.2 축 4 Coverage 신설·DISC-INV-10 · Wave 1 정책 2종 `coverage` 절(축 9)·`coverage-ledger.schema.md`(**경량 프로파일 축 목록 = 표준과 동일** — 축을 줄이면 결함이 경량 레인에서 재현) · Wave 2 `coverage_check.py`(fail-closed·변이 12/12 KILLED) · Wave 3 `pretooluse_coverage_guard.py`(원장을 **Contract 디렉터리 병치**해 결정적 도출·Contract 내용 0바이트 판독 — 자기신고 구조 배제 · 훅 fail-open ↔ 체커 fail-closed 분리) · Wave 4 SKILL.md v1.7 배선. 라이브 실증 4회 완료. **이월 ①(실 인터뷰 왕복 실증) = 갱신(29)에서 해소** · **이월 ②(외부 소비 프로젝트 원장 소급) = yt-stt 분 해소·타 프로젝트 미결**.

**운용 영향(의도된 마찰)** — 원장 없는 Contract 발행은 이 저장소·외부 소비 워크스페이스 모두에서 차단된다. 진행 중 프로젝트의 **기존** Contract 소비는 무영향이며, **새 Contract 발행 시점**에 인터뷰 경유 또는 원장 산출이 요구된다(auto-percenty 등 소급 여부 = 프로젝트별 판단·미결).

**갱신(25) K-1 게이트 확정 권위 기계 보호 완결(2026-07-28 — 전문 = 앵커 `30d81c9`).** `GatePolicy` actor 3필드에 코드 소유 허용 목록(`__post_init__` 검증·위반 = 사유 담은 `ValueError`·자동 보정 0) — 정책 데이터의 확정 권위 탈취 차단. 부수 = diff 기반 시점 의존 스코프 가드 1건 제거(교훈 = 스코프 가드는 축자 상태 대조로, diff 대조 금지 — 메모리 `tool-scope-guard-diff-vs-verbatim`).

**갱신(24) 본문 서사 강판 1차 완결(2026-07-27 — 전문 = 앵커 `8c8b82e`·−8,684B·CP2 Pass).** 잔여 = 기슬림 파일들의 본문 서사 2차 심사(착수 미정·사용자 지시 대기). 상세 = 메모리 `uaf-history-compaction-track`.

**갱신(23) 이력 거버넌스 전환 트랙 완결(2026-07-27 — 전문 = 커밋 사슬 `64b6570`→`44b1877`→`2c3992b`→`4f68104`).** in-file 이력 폐지(원칙 12 신설)·71파일 스텁(−237,927B)·재퇴적 가드 + 워터마크 2.5MB 하향·CP2 7/7 Pass. 잔여였던 가드 라이브 발화 확인은 갱신(27)에서 md 예산 가드 실초과 발화로 해소(이력 재퇴적 가드의 위반 실발화는 미관측 잔존 — `--check` 수동 실측만 있음). 상세 = 메모리 `uaf-history-compaction-track`.

**갱신(20)~(22) auto-percenty UAF 정식 편입 + 첫 엔진 run 완주(2026-07-26 — 전문 = git 이력·앵커 `90ca19c` 이후 사슬).** 엔진 경유(`/uaf-implement`)로 Contract v1(`pc-auto-percenty-001`)·SD 7종·run `impl-auto-percenty-p1` 5단위 Passed 5/5 완주(run 중 쿠팡 실접속 0). 관측 체크리스트 자동 발화 5/5·조건 발화 2/3(미관측 = `--response` 조건 주입 — 억지 유발 금지). 신규 결함 2(seed sentinel 프롬프트 문면·invoke 원장 `timeout` 필드)는 갱신(22) 경량 정비로 해소 — 실 run 실증 좌표 = B-1. 절차 비례화 트랙은 여기서 신설되어 완결(아래 착수 목록 0). 미결 판단 8건·웨이브 실전 = B-6.

### ★ 다음 착수 순위 = Advisor 배정(사용자 위임 2026-07-26 "순서 너가 정하는데로 할게")

0. **절차 비례화 트랙 = 완결(2026-07-27·Wave 1~5 완주)**. 전 기록(분해 채택본·게이트 Q-1~Q-7 확정 표·Wave별 Advisor 독립 검증·OQ 판정) = 트랙 원장 앵커 `git show af57be0:docs/proportionality-track-ledger.md` · 커밋 사슬 `cc446cc`→`e802317`(8건)+경계 4건. 현행 정본 = `.claude/CLAUDE.md` 레인 분기 절·`lane-registry.json`·binding §5.9·solution-design-binding §7A.2-S/L·discovery-binding §8.3·delegation-protocol §2.2/§3.2. 실전 실증 좌표 = B-1·잔여 미해소 8건 = B-2 승격분. (편성 정정 기록: SD 스킵 브리지는 전제가 아니었고[성숙 경로] 스킵 경로는 폐기 방향 확정[Q-4] — 종전 목록의 "SD 스킵 브리지"·"SD manifest 배선 3건" 항목은 이 트랙에서 소화·재정의됨.)
~~1. 커버리지 강제~~ **= 완결(2026-07-29 갱신(26)·Wave 0~4)** → 1. **표준 레인 seed 단일파일 가정 해소**(manifest 발견 2 잔존분) → 2. **Q·R 기계 강제** → 3. **§DC-8(a)·02 개정** → 4. **상류 바인딩 2차** → 5. **04 개정 트랙**(SD 스킵 폐기 실행 — Q-4 방향 기확정·경량 레인 실전 실증 후 착수).

(커버리지 트랙 이월 3건 = ① 실 인터뷰 왕복 실증[B-1] ② 외부 소비 프로젝트 기존 Contract 의 원장 소급 여부[프로젝트별 판단] ③ Discovery 실행 호스팅 실재화 시 훅 백스톱 → **엔진 게이트 승격** 재심[Wave 3 후보 ③ — 형태 A 에서는 규약 층이라 불채택].)

(갱신(22)에서 목록 소화 2건: 경량 정비 묶음 = 해소(§A) · .claude md 슬림화 실행 = 트랙 완결이라 제거 — 근거 = 메모리 `uaf-claude-md-slimming-backlog`·병합 푸시 90ca19c..a8f0219.)

(제품 트랙 별축 — 사용자 참여 시 최우선 인터럽트: **auto-percenty 웨이브 실전 ≤30상품**[선행 = 미결 판단 8건 카드·정본 = auto-percenty/docs/project-plan.md §4 표]+**A/B 라이브 실측**[예산 안·두 카드 동시 금지] · yt-stt M4-b 판단.)

커밋 상태: auto-percenty(Contract·SD·run 산출·provenance) + 본 저장소(discovery r005·SD r001 원장·run 원장) 커밋됨. **auto-percenty는 원격 없음(푸시 대기 유지)**.

---

## §B. 이월·미해소 통합 (갱신(19)~(21) + §DC 산재분 병합 — 중복 제거)

### B-1. 다음 실 run 관측 좌표 (하네스 개선분의 라이브 실증)

- 갱신(21) run 에서 **미관측**으로 남은 축: `--response` 조건 주입(조건부 승인할 일이 실제로 있을 때만 — 억지 유발 금지) · per-unit timeout **재기입 값 실물**(갱신(22)에서 원장 `timeout` 필드 배선 완료 — 다음 run 의 `logs/invoke-*.json` 로 관측) · **seed sentinel 프롬프트 강제 효과**(갱신(22) 개정분 — Planner 변형 문면 재발 0 여부).
- **경량 레인 실운용(비례화 트랙 실전 실증 — 첫 소비 프로젝트 경량 작업에서)**: 레인 판별 로더 실사용·`.claude/lane.json` 마커 물리화 · §7A.2-S 시드 + (S3) 원장 기록 실수행 · 직접 위임+경량 원장(binding §5.9) 실기록·`verify_run` 통과 · **절감 폭 실측**(수치 발명 금지 — Measurement First) · 신규 세션에서 lane 훅 재발화 확인 · `--allocation-file` 지정 실 CLI run 의 CP2 저티어 슬롯 `logs/invoke-*.json` 라이브 관측(W3-a 이월) · 경량 인터뷰 20문 실 인터뷰 1건.
- 갱신(19) N 트랙 미검증 축: 조건의 **실 프롬프트 렌더 문면** · Worker 조건 실준수(판정 축은 백로그 R 계열로 유보) · `render_gates` 표면에 "조건부 승인 가능" 인지 경로 부재(저임팩트) · 조건 **누적** 시나리오(현행 구조 게이트 1회 해소 전제) · 소비 프로젝트 레거시 run 혼재.
- 갱신(20) M·O 트랙 미검증 축: 대형 워크스페이스 스윕 성능 · 다단위 run 의 `[REWORK-NOTE]`↔스윕 연결 · `--append-system-prompt` argv 길이 한계.
- 갱신(17)~(18) 잔여: 실 LLM invoker 경유 **다중 escalation** run 미수행 · 한글 `gate_id` 셸 인용 거동 미실측(엔진 파생 규칙상 ASCII — 발생 시 재심) · Planner 의 `timeout` 선택 키 판별 타당성(갱신(21)에서 1건 관측·표본 1).

### B-2. 미해소 하네스 결함 (순위 = §A 다음 착수 목록)

- **SD manifest 배선 3건** — manifest 스키마↔코드 해석 모순·seed 단일파일 가정. 메모리 `uaf-design-manifest-path-defect`.
- **SD 스킵 브리지** — Solution Design 스킵↔구현 게이트 정면 충돌·브리지 코드 0. 메모리 `uaf-solution-design-skip-gap`.
- **백로그 Q·R 기계 강제** — 현재 절차 층만(Q = seed 제약↔브리프 실행 AC 대조 미도입 · R = 정적 CP2 의 done AC 간 동적 상충 무검출). 정본 = `docs/post-tuning-improvement-backlog.md` §Q·§R 「강제 지점」 행.
- **상류 바인딩 2차(디커플링)** — 1차 완결·2차 대기. 메모리 `uahf-binding-placement-defect`.
- **위임 규율 잔여 2건** — B-4 **실시간 전파**(fresh-context 수임 Agent 간 통신 채널 부재 = 환경 제약. 회수 시점 대조로 갈음·재심 = 통신 표면 등장 시) · B-3 **기계 차단**(설계 산출 Write 의 결정적 식별 불가 = 미도입 사유 기록. 재심 = SD 실행 호스팅 도입 시 엔진 게이트 승격). B-0~B-5 6건은 종결 — 메모리 `uaf-delegation-enforcement-gap`.
- **메모리 소급 감사** — "강제 필요한데 메모리에만 있는" 항목 재검토(갱신(15) 미완 항 — 앵커 `90ca19c` 승계). 「강제 없는 규율 신설 금지」 불변은 신설만 막고, 기존 메모리의 소급 감사는 별도 미착수 작업이다.
- **명명 금지 규범(AI·모델·제품 기능 축) 정본 소유 공백** — structure.md §5 C-3이 Adapter 경계를 명시 제외해 각 바인딩의 문서 소유 규범으로 병존 중(사용자 결정 2026-07-26 = 현상 유지). 재심 좌표 = structure.md §5 차기 계약 개정 시 Adapter 경계 조항으로 승격 검토(유형 A 절차).
- **e2e 러너 커버리지 갭(저임팩트)** — `run_all_tests.py` 의 `TEST_TREES` 4트리에 `orchestration/adapters/claude/tests` 미포함이라 그 스위트는 별도 pytest 로 돌려야 한다(uaf-verified: `run_all_tests.py` TEST_TREES 목록 직접 정독 — 갱신(22)). 러너 결과만으로 어댑터 스위트까지 통과로 단정하지 않는다.
- **비례화 트랙 잔여 미해소 승격(원장 아카이브 `af57be0` — §6.3·§8.11 잔존분)** — ① 표준 레인 seed 단일파일 가정(발견 2 표준 측 — `contract_to_graph.py:332` 부근·메모리 `uaf-design-manifest-path-defect`) ② SD 스킵 폐기 **실행**(방향 기확정 Q-4 — 04 유형 A 개정 트랙) ③ 경로 상수 중복(K-5 — `resolve_gate.py`↔`pretooluse_design_guard.py` 동일 문면 별도 선언) ④ floor target 어휘 불일치(K-8 — 컴파일러 기본 정책 target=unitType뿐이라 floor 미발화) ⑤ 01-entry §3.2-D 행 6 policy 열 "기본" 문면 명확화(재심 — Advisor 판정 = 비충돌 클래스 라벨) ⑥ advisor.md 상한 층 적용 여부 ⑦ 보고 표면 2종 병존(invoke 원장↔reports) ⑧ ref 어휘↔policyId 명명 정합. uaf-verified: 원장 §6.3 항 1~10·§8.11 항 8~11 전수 대조로 미해소만 추출 — 스윕 범위 = 그 두 목록.
- **OQ-PO-B7: provenance `ref.kind` 표기 2종 갈라짐(W2-b 실측 발견 2026-07-27)** — 프로덕션 `resolve_gate.py` = `"gate-resolution-provenance"` vs `verify_run.py` 화이트리스트 = `"user-resolution-provenance"` → 표준 레인 프로덕션 run 에 러너 적용 시 어휘 위반 오탐. 정본·해소 2안 = `project-orchestration-binding.md` §7 OQ-PO-B7(uaf-verified: Advisor grep 실측 — 두 파일 해당 라인 대조).
- **PreToolUse 훅 상대경로 ↔ Bash 지속 CWD 취약(갱신(22) 실측)** — Bash 도구의 `cd` 가 지속되면 상대경로 배선 훅이 다른 CWD 에서 실행돼 스크립트를 못 찾고, 이 경우 침묵 통과가 아니라 **Write/Edit 차단**으로 나타난다(uaf-verified: e2e 디렉터리 `cd` 직후 Edit 가 훅 에러로 차단·루트 복귀 후 동일 Edit 통과 — 라이브 재현 1회). 임시 규율 = `cd` 는 서브셸 `(cd … && cmd)` 로 한정. 항구 수정(훅 경로 견고화) = 미착수.

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
- **yt-stt** — **Contract v5·번인 자막 판독·팩트 배선·Projection 8종 개정 완료·origin/master 푸시됨**(갱신(29)). 남은 것 = **M4-b**(광역 화면 — `OQ-M4-A` (b)(c) 미해소가 막음. (a)는 부분 실측) · M5·M6 미착수 · **신설 미해소 5**(`OQ-V5-A` 화면 중앙 대형 문자 연출 미검출 · `OQ-V5-B` 타이핑 연출 채택 규칙 · `OQ-V5-C` 전량↔지점별 길이 경계 · `OQ-V5-D` 기준선 영상 번인 유무→TRAP-2·8 되돌림 종속 · `RISK-13` 편집 관행 다양성·표본 2편뿐) · `OQ-M1-A` 미해소 · RISK-9·10·11 미해결(11 = 노출 면적 확대) · F3′ dedup(fix-5) · JS 런타임 제품 반영 · `duration=0` realtime 게이트 무력 · 갱신(28) 신설 미결 3(`--lang` 미도달 · M3 `skipped` 교정 대상 미정의 · 제목 조회 비공개 함수 의존) · `out/` 표본 미커밋 유지(사용자 결정). 메모리 `uaf-product-yt-stt`.
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
| 측정·검증 도구 (유지 대상) | `uahf/framework/adapters/claude/orchestration-data/e2e/{run_all_tests.py,collect_metrics.py,verify_run.py,delegation_check.py}` (경로 정정 2026-07-28 — 리포 재귀 glob 실측상 `run_all_tests.py` 실재는 이 한 곳뿐이며 종전 표기 `orchestration-data/e2e/…` 는 루트 기준으로 부재) |
| Risk Routing 정책 | `orchestration-data/e2e/policy/{allocation.json,README.md}` |
| UAHF Contract | `discovery-data/contracts/uahf/project-contract.v3.md` |
| 과거 핸드오프·종료 트랙 원장 | git 이력(`git log -- docs/session-handoff.md docs/next-session-prompt.md`) · `ARCHIVE.md` 앵커 |
