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

## §5. 본 세션 검증·이탈 기록 (정직 기록)

- B-1·B-4 배선은 Advisor 직접 산출(거버넌스 문서 층 — 선례: B-0·B-2·B-5·RCA 처방 3 전부 Advisor 직접). 문서 저술이므로 CP2 독립 판정 대신 아래 자가 검증 + 커밋 전 재검으로 갈음하되, 이 갈음 자체를 이탈로 기록한다(자가 검증은 독립 판정이 아니다).
- `uaf-verified:` 배선 정합 확인 — delegation-protocol.md §2.4·§2.5·§2.7·§3.2 편집 4건과 worker.md·planner.md 편집 3건이 서로 같은 블록 이름(`[착수 전 점검]`·이탈 선언)·같은 판정 술어 3종을 인용함을 편집 직후 문면 대조로 확인. 검색 범위 = 이번 편집 7건의 문면이며 두 문서의 나머지 절 전문 재검은 커밋 전 수행 예정.
