# 하네스 개선 1순위 트랙 원장 — 백로그 K + 위임 규율 B-1·B-3·B-4

작성: Advisor · 2026-07-26
성격: 트랙 원장(evidence 등급 — `docs/artifact-lifecycle-policy.md` §2·§3·§5 준수·재정의 0). 위임 보고 승격(`docs/delegation-protocol.md` §2.7) + Advisor 결정 기록.
착수 근거: 사용자 확정 2026-07-26(핸드오프 갱신(15) ⑥ — "UAF 하네스 개선 우선 수행"·권고 순서 ① 백로그 K ② B-1·B-3·B-4 ③ RCA 트랙 잔여) + 본 세션 사용자 지시(`/uaf-continue` 인자 — 권고 순서 그대로 착수).

---

## §1. 백로그 K — Contract 포인터 정합 체커 (진행 중)

### 설계 확정 (Advisor · 위임 전)

- **채택안 = 백로그 §K Desired ③** (design-manifest CP2 결정적 체커에 포인터 정합 검사 — 원장 권고·최저비용·기존 체커 자리).
- **판정 규칙 = 최고 참조 버전 규칙**: 산출물 본문의 `project-contract.v<N>.md` 참조 중 최고 N == 현재 인스턴스(contract 디렉터리의 최고 vN). 낮으면 stale·높으면 dangling. 이력 보존을 위한 옛 버전 병기 인용은 최고 참조가 현재이면 통과 — append-only 계보(PC-INV 9)와 충돌하지 않는 유일한 결정적 규칙이다.
- **헤더 위치 강제·포인터 존재 강제는 범위 밖** — 존재 강제는 04 spec 소관(Desired ①·②)이며 이 트랙은 ③만 수행. 참조 0건 산출물은 비적용.
- **path 해석은 기존 produced 존재 검사와 동일 식 재사용** — 해석 이원화가 RC-2(접합부 무소유) 재발 경로라서 사양에 명시.
  - `uaf-verified:` yt-stt 실물 매니페스트(`C:\my-claude-project\yt-stt\.claude\solution-design\design-manifest.json`)를 직접 열어 path 형태 `../../docs/*.md`(매니페스트 기준 상대)와 contract 디렉터리 레이아웃(v1~v4 실재)을 확인함. 검색 범위 = yt-stt 워크스페이스 1건.
- **이탈 채널** = artifact 항목 `contractRefPinned{reason,confirmedBy}`(책임 있는 자율 (b) — 옛 인스턴스 고정이 정당한 경우 사유 기록으로 스킵). 무효 핀은 핀이 아니다(핀 오류 + 포인터 검사 계속).
- **contract 디렉터리 파생** = `manifest.parent.parent / "project-contract"`(배치 규약: 매니페스트 `<ws>/.claude/solution-design/` · Contract `<ws>/.claude/project-contract/` — contract-binding.md §4). 계보 부재 시 검사 비적용(기존 테스트 픽스처·계보 없는 워크스페이스 거동 보존).
- **강제 지점**: 코드 — `design_completeness.py`(resolve_gate task_added 승격 직전 fail-closed + pretooluse_design_guard 백스톱 동일 코드 재사용) + 테스트. 별도 정책 키 미도입 — 사유: 산출물 provenance 무결성은 path 존재 검사와 같은 구조 검사 계열이며 프로젝트 재량 대상이 아니다(이탈은 contractRefPinned로 항목 단위 기록).

### 위임 (단일 위임 — AGENT.md §Roles Advisor 이진 판별에 따라 Advisor 직접 분해 확정)

- Worker 1건 위임(2026-07-26): 변경 4파일(체커·scaffold 미러·스키마 문서·테스트), done 7항(테스트 전건 pass·기존 케이스 무수정·미러 바이트 동일·§5.7 접합부 열거 왕복·§5.8 축 도출·이탈/미결/귀속 보고). 보고 회수 후 본 §에 승격 예정.

### 위임 보고 승격 (회수 직후 2026-07-26 — §2.7 규율. 본 절은 수임 Agent 주장의 회수이며 검증 결과가 아니다. 판정은 아래 CP2)

`uaf-allow-legacy: 본 절의 수치·완전성 문구는 수임 Worker 보고 문면의 인용(주장)이며 Advisor 검증 결과가 아니다 — 판정은 아래 CP2 절이 소유한다(§2.7 원장 ⑤ 규율).`

- **보고 형식**: Worker 보고가 `[착수 전 점검]` 서두 블록을 포함(신설 규율의 첫 실사용) — 필수 필드 5/7 명시·from/to 위임 채널 암묵 판정·done 7/7 이진·context 4/4 실재 확인 후 착수.
- **주장 요지**: 4파일 변경(체커 +122/-12 · 미러 동기화 · 스키마 문서 +44 · 테스트 +228/-0 순수 append). 신규 테스트 13건 + 회귀 127(adapters)+175(framework) pass·EXIT=0 주장. 실물 yt-stt 왕복 양방향(현행 v4 → DESIGN-COMPLETE·EXIT=0 / 합성 v5 주입 → stale 7건·EXIT=2 — 합성 파일은 스크래치패드에만·yt-stt 무수정) 주장. 접합부 5종 왕복·미검증 축 "없음" 주장.
- **사양 이탈 신고 2건(추가 방향)**: ① k11b 테스트 추가(게이트 인과 격리 — 음성 대조의 짝) ② `_current_contract_version` 이 `OSError` 를 비적용(None)으로 흡수 + 산출물 `read_text` `OSError` 를 스킵으로 흡수 — Worker 스스로 실패 은폐 소지를 명시하고 Advisor 결정 요청.
- **미결**: 없음(주장). **관측 보고 1건**: 작업 트리에 Worker 무관 3파일 수정 존재(`.claude/agents/planner.md`·`worker.md`·`docs/delegation-protocol.md`) — Advisor의 B-1·B-4 병렬 편집이 원인(본 원장 §2·§3와 일치·충돌 없음). Worker가 경로 지정 add 를 권고.
- **귀속 후보**: 해당 없음(사양↔코드↔실물 모순 미발견 주장).

### Advisor CP2 독립 판정 — 1차 (2026-07-26)

- `uaf-verified:` 테스트 3트리 직접 재실행 — 127(adapters)+175(framework)+42(uahf step-host·step-invoker) pass·EXIT=0×3. 검색 범위 = 이 3트리이며 수임 보고 출력은 판정 근거로 쓰지 않았다.
- `uaf-verified:` 별도 적대 검증 8케이스 직접 작성·실행(Worker 케이스와 별도 구성·스크래치패드) 8/8 PASS — A1 실물 yt-stt 양성(오류 0) · A2 실물 계보 사본+합성 v5 음성(stale 7건·yt-stt 무촉) · A3 계보 잡파일(fullmatch 경계 — `.bak`·README 계수 제외) · A4 `.MD` 대문자 확장자(md 취급·dangling 검출) · A5 선행 0 참조 v04==v4 정규화 · A6 비-dict 핀(핀 오류+stale 계속) · A7 미러 본문 바이트 동일 직접 대조 · A8 기존 오류 순서 보존(K 오류 후행 append).
- **판정: 구현 결함 0건.** 신고 이탈 ① k11b 추가 = **수용**(음성 대조의 짝 — 게이트 인과 격리·§5.8 통과 사유 확인 원칙 정합). 신고 이탈 ② OSError 흡수 = **기각** — 이진 원칙상 판독 불가 = 판정 불가 = 차단(정책 파싱 실패 표면화 관례와 정합). 계보 정당 부재만 비적용 유지. 재작업 지시 발신(같은 Worker 재개·k13·k14 테스트 포함) — 결과는 2차 판정에 기재.
- 결함 귀속 소견: 이탈 ②는 Worker 임의 결정이 아니라 **브리프가 판독 실패 시 거동을 미지정**한 데서 왔다(귀속 = 위임 문면 — B-5 규율 적용). 재작업 지시에 거동을 명시해 해소.

### 재작업 보고 승격 (회수 직후 2026-07-26 — 주장 인용·판정은 아래 2차)

`uaf-allow-legacy: 본 절 수치·완전성 문구는 수임 Worker 재작업 보고 문면의 인용(주장)이다 — 판정은 아래 2차 CP2 절 소유.`

- **주장 요지**: 지시 5항 전부 반영 — `_current_contract_version` 튜플 반환(정당 부재=비적용 / 실재·판독 실패=차단 오류·검사 중단) · 산출물 판독 실패 오류 표면화 · k13(iterdir OSError)·k14(read_text OSError) 대상 경로 한정 부분 패치 + 패치 전 기저 0건 선행 assert(음성 대조 내장) · 미러 재동기화 · 스키마 판정 표 8행 + 「비적용과 차단의 경계」 문단. 3트리 129+175+42 pass·기존 케이스 수정 0(테스트 275 추가/0 삭제)·실물 yt-stt 회귀 EXIT=0 주장.
- **귀속 자기 판정(Worker)**: 종전 이탈 ②의 귀속 = Worker 자신 — 훅 층의 fail-open 불변을 게이트 체커 판정 불가에 오적용. **Lesson 후보**: "fail-open 불변은 훅 층 소유다 — 게이트 체커에서 판정 불가는 차단이며, 비적용(정당한 부재)과 미확정(판독 실패)을 같은 반환값으로 뭉개면 조용한 오통과가 된다."
- **Advisor 소견(귀속 정정)**: 1차 판정의 귀속 소견(브리프 미지정 = 위임 귀속)과 Worker 자기 판정(불변 오적용 = Worker 귀속)은 양립한다 — 브리프가 거동을 지정했으면 오적용이 발생하지 않았다. 복합 귀속(위임 주·Worker 부)으로 기록한다.

### Advisor CP2 독립 판정 — 2차 + CP3 (2026-07-26)

- `uaf-verified:` 테스트 3트리 직접 재실행 — 129(adapters)+175(framework)+42(uahf 2트리) pass·EXIT=0×3 · 적대 8케이스 재실행 8/8 PASS(미러 바이트 동일 직접 대조 포함) · 정정 코드 정독(`_current_contract_version` 튜플 반환·비적용/차단 경계 docstring·`_check_contract_pointers` 검사 중단 로직). 검색 범위 = 3트리 + 적대 스크립트 + 체커 신규 함수 2개 본문이며 수임 보고 출력은 판정 근거로 쓰지 않았다.
- **판정 = Pass.** 재작업 지시 4항 반영 확인(k13·k14 존재는 테스트 계수 129=127+2로 확인). **CP3 = Advisor 승인** — 백로그 K 해소 확정.
- **강제 지점**(해소 항목): 코드 — `design_completeness.py`(resolve_gate `task_added` 승격 직전 fail-closed + `pretooluse_design_guard` 백스톱이 같은 코드 재사용) + 테스트 15건 + scaffold 미러(미래 소비 프로젝트 상속).
- **Lesson 후보 채택**(Worker 발): "fail-open 불변은 훅 층 소유다 — 게이트 체커에서 판정 불가는 차단이며, 비적용(정당한 부재)과 미확정(판독 실패)을 같은 반환값으로 뭉개면 조용한 오통과가 된다."

---

## §2. 위임 규율 B-1 — 착수 전 점검 산출 의무 (배선 완료 2026-07-26)

- **공백의 정체**: 규칙(INV-6·§2.4 4단계)은 실재하나 ① 문면이 "누락"만 잡고 **모호(비이진 done)** 를 잡지 않았고 ② 점검 **수행의 산출(증거)** 이 강제되지 않아 조용히 생략 가능했다. 실측 = 2026-07-21 병렬 5조·done 비검증 목록·반환 0건(5/5 미작동).
- **배선 3면**:
  1. `docs/delegation-protocol.md` §2.4 「점검 산출 의무」 신설 — 보고 서두 첫 블록 `[착수 전 점검]`(3항 전부 이진: 필드 존재·done 이진 판정 가능성·context 실재), 모호한 done = 누락과 동급, 블록 부재 = 보고 무효.
  2. `.claude/agents/worker.md`·`planner.md` 「착수 전 점검」 절 신설 — 역할 정의는 위임 시마다 시스템 프롬프트로 기계 주입되는 층이다.
  3. §3.2 「점검·이탈 블록 반려」 — Advisor 회수 시 블록 부재 보고를 수리하지 않고 반려.
- **강제 지점**: ① 수임 Agent 정의(기계 주입) ② Advisor 회수 반려(§3.2). 순수 훅 미도입 — 사유: 위임·보고는 도구 호출이 아니어서 PreToolUse 표면이 없다(핸드오프 갱신(15) ⑥ 착수 유의와 동일 판단).
- **verifier.md 무수정 결정** — Verifier는 「대조 기준 부재 처리」(criteria 없으면 판정 불가 반환)를 이미 보유해 착수 전 점검의 동등물이 실재한다. 입력 계약이 위임 7필드와 달라(artifacts+criteria) 동일 블록 강제는 부정합.
- **AGENT.md 무수정** — 규칙 자체는 §Delegation에 기존재(2026-07-21 문면). 이번 변경은 강제 배선만이며 상위 규약 개정이 아니다.

## §3. 위임 규율 B-4 — 동료 계약·이탈 선언 (배선 완료 2026-07-26)

- **공백의 정체**: 병렬 집합에서 한 조의 정당한 이탈이 동료 전제를 무너뜨릴 때 알릴 채널 부재. 실측 = 2026-07-21(조 4의 FR-5b 신설 이탈 → 조 3 산출물이 거짓 사실 주장 보유).
- **정직 기록**: **실행 중 전파는 이 환경에서 불가** — fresh-context 서브에이전트 간 채널이 없다(delegation-protocol §3.3). 실현 가능한 최대치로 배선했다:
  1. 브리프 측 — 병렬 위임마다 **동료 계약 블록**(동료 Task 목록 + 교차 소비 지점). 병렬 분해 초안은 Planner 소관(B-0 이진 판별)이므로 `planner.md` 완료 조건에 편입.
  2. 보고 측 — **이탈 선언 블록**(없으면 "없음"·동료 계약에 닿으면 `[동료 영향]` 지목). `worker.md`·`planner.md` 배선.
  3. 회수 측 — Advisor **이탈 교차 대조**(회수 직후·§2.7 승격과 같은 시점): 이탈 선언 × 동료 계약 → 영향 이진 판정 → 영향 시 CP2 전 재검/재브리프. §2.7 원장 ④항에 기록 의무.
- **강제 지점**: ① 수임 정의·Planner 초안 완료 조건(기계 주입 층) ② Advisor 회수 반려 ③ §2.7 원장 ④항 기록 의무. 순수 훅 미도입 — 사유 = B-1과 동일.
- **잔여(미해소)**: 실행 중 발생 이탈의 실시간 전파는 환경 제약으로 미해소로 남는다. 회수 시점 대조가 커버하지 못하는 것 = 같은 Wave 안에서 이탈 이후에 완료된 동료의 재작업 비용(사후 재검으로 잡되 낭비는 발생). 해소하려면 서브에이전트 간 통신 표면이 필요하다 — 환경 기능 추가 시 재심.

## §4. 위임 규율 B-3 — 설계 층 원장 우회 금지 (사용자 결정 대기)

불변 신설이 기존 작업 방식(Advisor 직접 병렬 위임으로 설계 산출물 작성 — 예: 2026-07-21 yt-stt Projection 8문서·5병렬·원장 0건)을 금지하게 되는 거버넌스 무게 — 핸드오프 ⑥이 사용자 결정 필수로 지정. Advisor 옵션 자료:

| 옵션 | 내용 | 무게·효과 |
|---|---|---|
| A. 구현 동형 불변 | AGENT.md §Invariants에 "설계 산출도 SD 원장·게이트 경유 기본" 신설 — Advisor 직접 병렬 위임으로 Contract 소비 프로젝트 설계 산출물을 만드는 방식 금지 | 강제 최강. 단 SD 실행 호스팅 미도입(binding §6.2 유보) 상태라 다라운드는 form-A 규약 절차로 주 세션이 구동 — 실무 비용 증가. 상위 규약 개정 = 사용자 승인 필수 |
| B. 원장 의무만 | 경로(엔진/직접 위임)는 자유·**SD 원장 기록 의무**만 신설 — 직접 위임으로 돌려도 solution-design-data events에 위임·게이트·산출 기록 | B-2(§2.7 승격)의 설계 층 대응물. 방식 유연성 보존·추적성 확보. AGENT.md 개정 폭 소 |
| C. 미도입 + 사유 기록 | 현행 유지. 백로그·본 원장에 미도입 사유를 강제 지점 행으로 기록(재심 좌표) | 비용 0. 단 RC-1(반응적 강제) 패턴의 반복 — 다음 재발 실측 때 다시 올라온다 |

Advisor 권고 = **B**(원장 의무만). 근거: B-3의 실측 피해는 "우회 자체"가 아니라 **원장 0건**(추적 불가)이었고, A는 실행 호스팅 미도입 상태에서 비용이 강제 이득을 앞선다. A는 실행 호스팅 도입 시 재심.

### 해소 (사용자 결정 2026-07-26 = 옵션 B · 같은 세션 구현)

- 사용자가 결정 카드에서 **B(원장 의무만)** 를 선택했다.
- **배선 2면**: ① `.claude/AGENT.md` §Invariants 「설계 산출 원장 기록 의무(경로 자유·기록 필수)」 신설 — 원장 0건 설계 산출 금지·구현 층(경로 강제)과의 구조 대비 명문화(상위 규약 개정의 승인 = 위 사용자 결정) ② `.claude/CLAUDE.md` §구현 단계 2층에 운용 배선(Advisor 세션마다 상시 로드되는 층 — SD 원장 = `solution-design-data` events·form-A 수기 append 허용).
- **강제 지점**: ① AGENT.md 불변 ② CLAUDE.md 상시 로드 층. 기계 차단 미도입 — 사유: 설계 산출 Write의 결정적 식별이 소비 프로젝트마다 경로가 달라 불가. **재심 좌표 = SD 실행 호스팅 도입 시 엔진 게이트로 승격**(옵션 A 재심과 같은 시점).

---

## §5-A. RCA 트랙 잔여 착수 (같은 세션 연장 — 갱신(15) ⑥ 권고 ③)

### recover_gate --gate-id (Worker 위임 2026-07-26)

- 결함 실측 좌표: `resolve_gate.py` `recover_gate` 가 다중 pending 동일 gateKind 에서 `matches[0]` **침묵 선택**. 사양 = `--gate-id` 특정 지목 + 무지목 다중 매칭 시 명시 오류(후보 열거). 외부 호출부 2곳 실측(main + `test_orchestrate_project.py:440` 2-튜플) — 기본값 인자로 계약 보존.

**위임 보고 승격(회수 직후 — 주장 인용·판정은 CP2)**: `uaf-allow-legacy: 수치·완전성 문구는 수임 보고 인용이다 — 판정은 아래 CP2.` 3파일(+76/-6·+160/-0·+19/-0)·신규 g1~g5 pass·3트리 134+175+42 pass·기존 문면 삭제 0 주장. 접합부 왕복 3면을 **런처 실산출 stop-signal**(`run_and_map` 실행·`gates.pending_gates` 동일 산출 경로)로 수행 주장 — 왕복 불가 접합부 없음 주장. **이탈 1건 신고**: binding §8 개정 이력 1항 추가(문서 관례 — 파일 경계는 준수). **미검증 축 신고 2건**: 실 LLM run 미수행 · `render_gates.py` 의 `resolve_command` 렌더 미검사. **open_questions 2건**: ① 렌더 명령이 `--gate-id` 없이 나오면 다중 pending 에서 사용자 복사 명령이 차단됨 — 렌더에 gate_id 포함 제안 ② `.claude/commands/uaf-implement.md:53` CLI 문면 미반영. 귀속 후보 없음(브리프 좌표 실측 일치 주장).

**후속 위임(open_questions 2건 채택) 보고 승격(회수 직후 — 주장 인용)**: `uaf-allow-legacy: 수치·완전성 문구는 수임 보고 인용 — 판정은 아래 CP2.` 렌더 항목별 `resolve_command` 에 `--gate-id` 상시 포함(가법 — `gate_id=None` 일반형은 종전 문면)·결정적 셸 인용 규칙(`_cli_token`) · 신규 r7a~r7d 4케이스 · 3트리 138+175+42 pass · **기존 assert 갱신 0건**(인자 배치를 `--actor` 뒤로 선택해 기존 부분 문자열 단언 보존) · 실 런처가 자동 출력한 렌더 문면 → argv → resolve → 재렌더 "미해소 0건" 물리 왕복 · `uaf-implement.md` CLI 문면 반영 주장. 이탈 1건(binding §8 이력 관례 — 직전과 동형) · 미검증 축 2건(실 LLM run·한글 gate_id 인용 거동) 신고.

**Advisor CP2 — recover_gate 트랙 2차 + CP3 (2026-07-26)**: `uaf-verified:` 3트리 직접 재실행 138+175+42 pass·EXIT=0×3 + `render_gates.py`·`resolve_gate.py` diff 정독(침묵 첫-선택 제거·kind 불일치/부재 구분 오류 문면·항목별 gate_id 전달·가법 보존). 검색 범위 = 3트리 + 두 파일 diff. **판정 = Pass·CP3 승인.** 이탈(§8 이력 추가) 2건 = 수용(문서 관례 정합). 미검증 축 2건은 이월로 기록(실 LLM run = 다음 실 run 관측 좌표·한글 gate_id = 엔진 파생 규칙상 발생 시 재심).

### per-unit timeout — 설계 조사 완료·구현 이월 (Advisor 결정)

- `uaf-verified:` 코드 정독 조사 — `contract_to_graph.py` `DEFAULT_TIMEOUT=2400` 전역 config → `orchestrator.py` `self.timeout` → ① StepHost 생성자(`_new_host`·host 전역) ② `_dispatch_gate_step` 의 `InvokeRequest(timeout=self.timeout)`. **`InvokeRequest` 에는 per-request `timeout` 필드가 실재**(`uahf/framework/loop/step-host/invoker.py:52`). 검색 범위 = orchestration 트리 + uahf step-host 트리의 timeout 토큰 grep + 해당 지점 정독.
- **이월 사유(이진)**: StepHost 는 uahf 무수정 경계(orchestrator 주석 "무수정 import·재정의 0")이며 host 전역 timeout 만 받는다. per-unit 화의 무접촉 경로 = **orchestration 층 래퍼 invoker**(`_effective_invoker()` 훅 실재)가 step 계약의 단위별 timeout 으로 request.timeout 을 재기입 — 단 `Step.from_dict` 가 임의 필드(timeout)를 보존하는지 미확인(`uaf-assumed:` Step 클래스 본문 미열람) + impl-plan 스키마 필드 신설·검증 규칙이 필요해 **별도 설계 사이클 대상**이다. 오늘 세션 잔여 시간에 밀어넣지 않는다(엔진 변경 품질 규율).
- Q·R 기계 강제 = 백로그 원장의 기존 미도입 사유 행 유지(각각 브리프 렌더 결합·Verifier 판정 축 확장 — 별도 트랙). 이 세션에서 변경 0.

### per-unit timeout — 설계 확정 (2026-07-26 새 세션 · Advisor · 사용자 확정 1순위)

`uaf-verified:` 착수 전 접합부 전건 실측 재확인 — 검색 범위 = orchestration 2트리 + uahf step-host 트리 + step-invoker 어댑터 + scaffold-template 의 해당 지점 정독·glob. 근거 좌표:
- `Step.from_dict`(step.py:64) 화이트리스트 → timeout 은 Step 에서 탈락(직전 세션 실측 유지).
- `InvokeRequest.timeout` per-request 필드 실재(invoker.py:52) + **실 CLI invoker 가 `request.timeout` 을 subprocess timeout 으로 직접 소비**(claude_invoker.py:217) — 재기입 값이 실제 프로세스 타임아웃에 닿는다.
- exec 번들(bundle.py:31)·CP2 verify_bundle(host.py:316)·게이트 디스패치 번들(orchestrator.py:514) **셋 다 `step_contract`(id 포함)를 싣는다** — id 매칭이 세 경로 전부에서 성립.
- task_added 승격은 plan task dict 원문 전달(resolve_gate.py:478)·`fold._copy_task` 는 `dict(task)` 얕은 복제(revision.py:174)·`validate_revision` 에 미지 키 거부 없음(revision.py:321~373) — **timeout 필드는 승격·fold 를 무변경으로 통과**한다.
- config.timeout → `Orchestrator(timeout=cfg.get("timeout"))`(k_common.py:67) → StepHost·게이트 디스패치 전역 적용(현행) — 전역 fallback 경로.
- scaffold-template 파이썬 벤더링 = 훅 2종(design-guard)뿐 — 이번 접촉 파일의 미러 의무 없음.

**설계 결정 D-T1~D-T8 (Advisor 확정 — 사용자는 사이클 착수를 확정했고 세부 결정은 본 원장에 기록):**
- **D-T1 스키마**: impl-plan task 의 **선택 12번째 키 `timeout`** = 실행 예산 초·**양의 정수만**(bool 제외·0/음수/실수/문자열 거부). 부재 = 전역 fallback. REQUIRED_TASK_KEYS 11키는 무변(필수 승격 아님 — 기존 run·플랜 하위호환).
- **D-T2 강제 지점**: `validate_impl_plan_adapter`(resolve_gate.py) — 키 존재 시 불량값이면 오류 목록에 추가(fail-closed·원장 무오염). 판정 불가≠통과(이진 원칙·K 트랙 Lesson 동형).
- **D-T3 래퍼**: 중립층(orchestrator.py) `UnitTimeoutInvoker` 데코레이터 — `{step_id: timeout}` 맵 보유, `request.bundle["step_contract"]["id"]` 매칭 시 `dataclasses.replace(request, timeout=값)` 로 재기입(원본 request 무변조·순수), 비매칭 = 원 request 그대로. inner 반환 투명 통과 + `__getattr__` 속성 투과(HeartbeatInvoker 선례 동형). 판단 0(PO-INV 1).
- **D-T4 맵 원천**: `self.active_graph()["tasks"]` 파생(순수·PO-INV 3 — 제2 진리원천 0). 맵 편입은 유효값(양의 정수·bool 제외)만 — 불량값은 편입하지 않는다. 사유: 차단은 D-T2 검증 게이트가 소유하고 래퍼는 기계 재기입만 한다. 비검증 경로(seed 그래프·레거시 원장)의 불량값이 실행을 죽이지 않게 하는 안전망이며, 검증 경로에서는 불량값이 게이트에서 이미 차단되므로 래퍼에 도달하지 않는다.
- **D-T5 배선(균일 적용)**: ① `_effective_invoker()` — 기존 반환(self.invoker 또는 ArtifactCapturingInvoker)을 맵 비어 있지 않을 때만 최외곽 래핑(맵 공집합 = 래핑 0·기존 거동 보존 — allocation=None 패턴 동형) ② `_dispatch_gate_step` — 같은 맵으로 timeout 래핑만 경유(ArtifactCapturingInvoker 를 게이트 경로에 새로 끼우지 않음 — 기존 포집 배선 무변). 결과: **한 단위의 exec·CP2·review/approval 디스패치가 전부 그 단위의 timeout 을 받는다**(균일 규칙 — 문면 검증 가능성 우선).
- **D-T6 seed proposal 노드**: timeout 미부여(전역 fallback 2400 적용). 사유: 컴파일 시점엔 단위 규모 정보가 없고 값 발명 금지. 원 사고(proposal 900s×3)의 완화는 DEFAULT_TIMEOUT 2400 상향으로 기반영.
- **D-T7 전역 fallback 유지**: config.timeout → Orchestrator.timeout → StepHost/게이트 디스패치 경로 무변. per-unit 값 부재 단위는 기존 거동 그대로.
- **D-T8 Planner 지시**: `_seed_prompt` 구현 task 구성 규칙에 선택 키 안내 1항 추가(대형 단위에만 지정·미지정 = 전역 기본). `_done_ac` 는 필수 11키만 검사하므로 무변.
- 문서 = binding §5.8(미해소 이월 문단의 Desired 4 항 해소 + per-unit timeout 계약 서술 + §8 이력 1행 관례) · 백로그 L §4 해소 행(강제 지점 행 포함). uahf/** ·05 spec·Frozen 무접촉.

**위임 보고 승격(회수 직후 — 주장 인용·판정은 아래 CP2)**: `uaf-allow-legacy: 수치·완전성 문구는 수임 보고 인용이다 — 판정은 아래 CP2.` `[착수 전 점검]` 블록 제출(브리프 좌표 4파일 실물 대조·불일치 0 주장). 산출 6파일(orchestrator.py `UnitTimeoutInvoker`·`_unit_timeouts`·`_wrap_unit_timeout`·`TASK_TIMEOUT_KEY` / resolve_gate 선택 키 검사 / _seed_prompt 1항 / binding §5.8 (g)+이월 문단+§8 1행 / 신규 테스트 11+6). done 6/6 자기 판정 1 · 3트리 186+144+23 EXIT=0×3 + step-invoker 19 주장. **음성 대조 1건 수행 주장**(`_wrap_unit_timeout` 항등 치환 → 왕복 테스트 실패 확인 → 복원 재통과 — 인과 격리). 기존 테스트 문면 삭제 0 주장. **이탈 신고 2건**: ① 왕복 테스트 전용 delegation 8필드 픽스처 로컬 헬퍼(기존 픽스처 무수정 — sentinel 2필드만으론 Host Consult 에스컬레이션으로 디스패치 0 실측) ② binding §8 이력 1행(관례·직전 2트랙 동형). `[동료 영향]` 해당 없음(단일 위임). **미검증 축 신고 3건**: 실 LLM run · Planner 실 준수 · render_gates/런처 표면(브리프 범위 밖). **open_question 1건**: D-T4 불량값 침묵 fallback 의 관측 신호 유무 — Advisor 결정 요청.

### 백로그 N — 조건부 승인 하류 전달: 설계 확정 (2026-07-26 · Advisor · 사용자 확정 순서 ② — 아래 per-unit CP2 블록 이후 착수·기재 위치만 선행)

`uaf-verified:` 착수 전 접합부 실측 — 검색 범위 = resolve_gate.py 전문(구조/에스컬레이션 해소 경로·provenance·기록 파일) + delegation_check.py 전문 + bundle.py·step.py·host.py 해당 지점 + uaf-implement.md `--response` 문면 grep. 근거 좌표:
- **조건 원문의 원장 보존은 이미 성립** — `_append_provenance`(resolve_gate.py:365) 가 `ref.response` 에 원문 동봉·`_write_record`(:389) 도 기록. **부재는 하류 전달뿐**(N 등재 문면과 일치).
- `resolve_structural`(:416) 흐름 = (0)proposingStepRef 파생 → (1)validate → (1.5)설계완성도 → (2)actor 적격 → (3)provenance+해소 append → (4)plan["tasks"] **원문 그대로** `accept_revision`. 주입 지점 = (2)와 (3) 사이에서 승격 payload 를 선구성(실패 시 어떤 append 도 전 — 원장 무오염 보존).
- `delegation_check.py` 는 delegation.task/done 참조형만 검사(context 무접촉) · `Step.missing_fields` 는 context **존재**만 요구 → context 추가 항목은 어댑터·코어 검증 어느 쪽과도 충돌 0.
- 하류 도달 경로 실재: 승격 payload → fold(`_copy_task`=`dict(task)`) → `Step.from_dict`(delegation dict 보존) → `assemble_bundle` 의 `memory_material = delegation.context`(bundle.py:39) = **Worker fresh-context 번들에 물리 도달** · CP2 verify_bundle 의 `step_contract`(Step.contract·delegation 포함) = **Verifier 에게도 보임**.

**설계 결정 D-N1~D-N8 (Advisor 확정):**
- **D-N1 채널 = 승격 시 delegation.context 주입(백로그 N Desired 1 채택)**: `resolve_structural` 에서 `--response` 가 비공백(strip 후 비어있지 않음)이면 각 승격 task 의 **payload 사본**에 조건 항목을 `delegation.context` 에 추가해 `accept_revision` 에 전달한다. `impl-plan.json` 파일은 바이트 무변조(원 산출 보존). response 공백(기본 "")이면 주입 0 — 종전 거동 유지. 원장 분리 보존 = impl-plan 파일(원 산출) + provenance 이벤트(조건 원문) + revision payload(소비 뷰·주입 반영).
- **D-N2 주입 문면(결정적)**: `[게이트 조건 — <gate_id> 해소(actor=<actor>)] <response>` 단일 문자열 항목. gate_id·actor 로 provenance 이벤트와 상호 추적. 타임스탬프 없음(결정성 — 시각은 이벤트 소유).
- **D-N3 타입 규칙**: context 가 list → 사본에 append(원 dict 무변조) · 문자열 → `[원문, 조건]` 2원소 리스트 승격 · **그 외 형 + response 비공백 → 해소 이벤트 append 전 비영 종료·원장 무오염**(조건의 침묵 탈락 금지 — N 이 고발한 결함을 채널 자신이 재생산하지 않는다).
- **D-N4 적용 대상 = 승격 전 task 균일**: task 별 조건 라우팅 미도입 — 응답이 단일 원문이며, 분배는 구조화 스키마(Desired 2) 소관. 하류 단위는 자기 해당 조건을 스스로 식별(브리프 자족 원칙 정합).
- **D-N5 Desired 2(conditional-approval 게이트 종류 신설) 미도입** — 사유: 05 §3.3 게이트 어휘 개정(거버넌스 무게)이고 D-N1 이 "조건의 물리 도달"을 성립시킨다. 조건 미반영의 CP2 판정 축 확장은 백로그 R 계열로 유보. 재심 좌표 = 실 run 에서 균일 주입의 조건 오귀속 실측 시.
- **D-N6 Desired 3(Advisor 수기 편집 절차 명문화) 미도입** — 사유: D-N1 채널 신설로 수기 편집 관행의 필요가 소멸(조건부 승인 = `--response`·산출물 자체 결함 = 게이트 미해소·재작업). 명문화는 원장 밖 편집을 정당화하는 역효과.
- **D-N7 출력 표면**: `[CONDITION]` 라인으로 주입 건수·조건 원문 출처(provenance 이벤트) 명시. render_gates 무접촉.
- **D-N8 접촉 면**: resolve_gate.py(주입·docstring 동작 요약·`--response` help 문면 "기록용"→구조 게이트 하류 주입 채널) + binding §3.2 동기화·§8 이력 1행 + uaf-implement.md `--response` 의미 1문. **엔진(orchestration/framework)·uahf/**·05 spec·scaffold 무접촉.**

**위임 보고 승격(회수 직후 — 주장 인용·판정은 아래 CP2)**: `uaf-allow-legacy: 수치·완전성 문구는 수임 보고 인용이다 — 판정은 아래 CP2.` `[착수 전 점검]` 제출(좌표 일치·delegation_check 경로만 브리프 미표기 자체 해소). 산출 4파일(resolve_gate +106/-2 — `format_condition`·`build_promotion_payloads` 신설·(2.5) 선구성·(4) 소비·`[CONDITION]` 출력 / 테스트 +292 13케이스 / binding §3.3 계약 6항+§8 / uaf-implement 1문). done 6/6 자기 판정 1·4트리 186+157+23+19 EXIT=0×4 주장·음성 대조(항등 치환 → 신규 7건 실패) 주장·자기 검출 계수 오기 1건 정정 주장. **이탈 신고 5건**: ① **context 부재/None → 조건 리스트 신설(비영 종료 아님)** — 기존 테스트 :268 이 context 부재+`--response` rc==0 을 단언해 D-N3 엄격 해석과 done 2 가 정면 충돌·"빈 채널" 해석 채택 ② binding §3.2→**§3.3**(실물 절 구조 — 귀속 후보 = 위임 문면) ③ 주입 문면 `response.strip()` 정규화(원문은 provenance 보존) ④ 테스트 지역 헬퍼·지역 import ⑤ §8 이력 1행(허용 명시). **미검증 축 5건**: 실 LLM run·Worker 조건 실준수(D-N5 유보 범위)·render_gates 표면·조건 누적 시나리오·레거시 run 혼재. **open_questions 2건**: ① 부재 context 주입이 Host missing_fields Escalated 경로를 가려 "context 누락" 결함을 조건부 승인이 은폐 가능 — (a)유지/(b)경고 라인/(c)비영 종료 중 결정 요청 ② escalation 게이트 비대상(비대칭)의 의도 확인 요청.

**Advisor open_question 판정 + 재작업 1회(2026-07-26)**: ① = **(b) 채택** — 근거: `validate_impl_plan_adapter` 는 애초 context 를 요구하지 않아 부재 계획이 조건 없이도 승격 가능했으므로 (c) 차단은 조건부 승인만 더 엄격하게 만드는 비일관·다만 "부재 단위가 주입으로 디스패치 가능해짐(종전 = Host missing_fields Escalated)"은 침묵 금지 → `[CONDITION-NOTE]` 관측 신호 재작업 지시(id 열거·차단 아님·rc 무변). ② = **의도된 비대칭 확정** — escalation 은 J 채널(해소 이벤트 ref → rework feedback)이 이미 대상 단위에 응답을 전달·변경 0. 재작업 회수: `build_promotion_payloads` 4원소 반환(`created`)·`[CONDITION-NOTE]` 2행·테스트 +4(계 17)·binding §3.3 1문·이탈 0건 신고.

**Advisor CP2 — 백로그 N(재작업 포함 2회) + CP3 (2026-07-26)**: `uaf-verified:` ① 4트리 직접 재실행 2회 — 1차 186+157+23+19·재작업 후 186+**161**+23+19, 전건 pass·EXIT=0×4(검색 범위 = orchestration 2트리 + uahf step-host·step-invoker 트리·수임 보고 출력 불신·로그 파일 종료코드 보존) ② 접촉 5파일 diff 전문 정독 — D-N1~D-N8 문면 일치·주입 선구성 위치 = (2.5) 어떤 원장 append 보다 앞(원장 무오염 보존)·기존(HEAD) 테스트 문면 삭제 0행·엔진 중립층·uahf·specs·scaffold 무접촉(git status 목록 기준) ③ **Advisor 독자 프로브**(수임 AC 밖) — response 에 `%s`·`100%%`·CRLF 포함 시 문면 원문 보존(포맷 문자열 이중 해석 0)·원본 task dict 무변조·None→`[조건]` 신설+`created` 등재 실측. **검출 결함 0건**(1차 보고의 자기 검출 계수 오기는 Worker 가 커밋 전 자체 정정 — 직전 트랙 CP2 지적의 예방 재적용 실증). 이탈 5건 수용(② binding §3.2→§3.3 = 위임 문면 귀속·③ strip 정규화 = 원문 provenance 보존으로 정합·①은 위 판정으로 (b) 승격). **판정 = Pass·CP3 승인.** 미검증 축 이월 5건 = 실 LLM run(조건의 실 프롬프트 렌더 문면)·Worker 조건 실준수(D-N5 유보 — 백로그 R 계열)·render_gates 표면(조건부 승인 가능함의 렌더 인지 경로 부재 — 저임팩트 관찰)·조건 누적 시나리오(현행 구조 게이트 1회 해소 전제)·소비 프로젝트 레거시 run 혼재.

**Advisor CP2 — per-unit timeout + CP3 (2026-07-26)**: `uaf-verified:` ① 4트리 직접 재실행 186+144+23+19 전건 pass·EXIT=0×4(검색 범위 = orchestration 2트리 + uahf step-host·step-invoker 트리 — 수임 보고 출력 불신·별도 로그에 종료코드 보존) ② 접촉 7파일 diff 전문 정독 — D-T1~D-T8 문면 일치·numstat 기준 테스트 파일 삭제 0행·`uahf/**`·specs·scaffold-template 무접촉(git status 목록 기준) ③ **Advisor 독립 음성 대조**(수임 것과 별개·스크래치 스크립트·저장소 파일 무수정) — 원본 배선 A={지정 단위: 4321, 미지정: 777} vs `_retarget` 런타임 항등 패치 B={전부 777} — 재기입 인과 격리 성립 ④ 적대 프로브 3종 — 거대 정수(10^12) 통과(상한 미발명·설계 문면)·milestone 단위 timeout 허용(균일 규칙)·1200.0(정수값 실수형) 거부(엄격 int·오류 문면 명시). **검출 결함 1건(경미·문서)**: binding §8 이력 행 "test_orchestrator.py 10케이스" ↔ 실측 11(트리 175→186·`def test_` 계수) — Advisor 직접 정정·귀속 = Worker(자기 산출 계수 오기·코드 무영향). **open_question 판정 = 신호 미도입 유지**: 강제 지점은 검증 게이트가 소유(검증 경로에선 불량값이 래퍼에 도달 불가)·래퍼는 중립 엔진 층이라 사용자 표면 출력은 층 위반·비검증 경로(수기 원장)는 원장 자체가 관측 좌표다. 재심 좌표 = 실 run 에서 불량값 실측 발생 시. 이탈 신고 2건(왕복 전용 픽스처 로컬 헬퍼·§8 이력 행) = 수용(전자는 실측 근거 타당·후자는 관례 동형). **판정 = Pass·CP3 승인.** 미검증 축 이월 2건 = 실 LLM run 재기입 예산 실증(다음 실 run 관측 좌표에 추가)·Planner 선택 키 실 준수(실 run 관측 대상).

## §5. 본 세션 검증·이탈 기록 (정직 기록)

- B-1·B-4 배선은 Advisor 직접 산출(거버넌스 문서 층 — 선례: B-0·B-2·B-5·RCA 처방 3 전부 Advisor 직접). 문서 저술이므로 CP2 독립 판정 대신 아래 자가 검증 + 커밋 전 재검으로 갈음하되, 이 갈음 자체를 이탈로 기록한다(자가 검증은 독립 판정이 아니다).
- `uaf-verified:` 배선 정합 확인 — delegation-protocol.md §2.4·§2.5·§2.7·§3.2 편집 4건과 worker.md·planner.md 편집 3건이 서로 같은 블록 이름(`[착수 전 점검]`·이탈 선언)·같은 판정 술어 3종을 인용함을 편집 직후 문면 대조로 확인. 검색 범위 = 이번 편집 7건의 문면이며 두 문서의 나머지 절 전문 재검은 커밋 전 수행 예정.
