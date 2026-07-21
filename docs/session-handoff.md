# 세션 핸드오프 (UAF 레벨 정본 · 단일 live 문서)

작성: Advisor · 2026-07-17 (직전 상태 앵커: Performance Tuning Track 종료 2026-07-14)
용도: 새 세션은 **본 파일 하나로 상태를 인수**한다. 원문 전체 정독 강제 없음 — demand-driven(§단위·필요 시점) 규칙을 따른다. (물리 발화 = `/uaf-continue`)
지위: `docs/artifact-lifecycle-policy.md` §6이 정한 **UAF 레벨 단일 live 핸드오프**다. 단수·제자리 갱신이며 버전별 파일을 만들지 않는다. 과거 상태는 git 이력이 정본이다. (전신: `docs/next-session-prompt.md` — 본 파일로 개명·재정착 2026-07-17)

> **🔴 갱신 2026-07-19 — §DC-1 트랙 = 완결·master 머지·푸시 완료** (branch `feat/dc1-design-completeness` → master FF 머지·origin 푸시 `7241710`, 2026-07-19). Wave 1-4로 백엔드 직행 차단 실증: SP-INV 9(코어 04)+필수 산출물 10종(어댑터 정책)+엔진 게이트(`resolve_gate` fail-closed·프레임워크 무수정). 각 Wave CP2 독립검증(테스트 재실행)·CP3 승인. 커밋 `08a3321`(설계+정책)·`8e1f18d`(실행코드). tms 실선언(3접점+연계)으로 필수 10종 미산출 차단 실증. **+책임 있는 자율 원칙**(ARCH §6 원칙11·CLAUDE.md — 필수=Core/Policy 강제·자율=기본값+이탈 사유기록·이탈=게이트 일괄 표면화; "비정본이 항상 문제" 근본 대응·메모리 `uaf-accountable-autonomy-principle`). **+Wave 5-A 생산 프로토콜**(정책·바인딩 §7A·부록 — 역할 구성[PM 커버리지 바닥+기획·아키텍처 기본+디자이너·DBA 조건부]·역할→산출물 소유 맵 1:1·위임 산출·MD 본문+JSON 매니페스트·docs 배치·CP1-3+Validating 게이트 컨펌). 원칙·Wave 5-A 각 CP2/CP3. **§DC-3 PreToolUse 백스톱 = 완결 2026-07-19**(master 머지·푸시 완료): 차단형 **운영 훅** 3 Wave — W1 `orchestration/adapters/claude/pretooluse_design_guard.py`(design_completeness 재사용·스코프=게이트 워크스페이스+src/·fail-closed on finding/fail-open on guard error) + 리포 `.claude/settings.json` PreToolUse 배선 + 테스트 9종, **메인+서브에이전트 Write 라이브 차단 실증**(PreToolUse 서브에이전트 발화 경험 확증); W2 `hooks-binding.md` §4.5 운영 훅 경계 명문화(**운영 훅≠Hooks Component 바인딩**·PreToolUse∉08 카탈로그→INV-2 미저촉·**spec 08 무수정**·DP-E3 stale 정정); W3 scaffold 벤더링(`dot-claude/hooks/design-guard/`·settings.example·install-manifest·scaffold-binding §6·PyYAML 전제조건). 각 CP2/CP3. 엔진 게이트(fail-closed)+훅 백스톱 **이중방어**+미래 상속 완성. 백로그=인프라 부재 fail-open. 상세=메모리 `uaf-design-completeness-gap`. **잔여:** Wave 5-B 코어(form-B 로더 `solution_design_resolve.py`·브리프 템플릿·배선 §7A.5)=완결 2026-07-19(기록기·실행 호스팅[04 §3.9]은 미도입 유지)·**§DC-9 완결 2026-07-19**(OQ-PO-B5 엔진 actor 재검증+OQ-PO-B1 게이트 큐 렌더 문법 — 상세 아래 §DC-9)·(**§DC-5+6 완결 2026-07-19** — 다라운드 §7B·deliberation policy·보안 역할·cap 집행·θ 상향, 상세 아래 §DC-5·§DC-6 · §DC-7 완결 2026-07-19 — WBS 소유 삼분 명문화+seed proposal role Worker→Planner 정정 · §DC-8 완결 2026-07-19 — 비정본 승격 불필요·접점 제외 표면화 옵션 b 해소·옵션 a 잔여)·~~tms 실제 10종 설계 산출~~(**소멸** — tms 트랙 종료·삭제 2026-07-19·앵커 `4934bc8`·ARCHIVE.md·테스트 목적 완수). 상세 정본 = 메모리 `uaf-design-completeness-gap`. 이하 §DC-1~9는 원 백로그 기록(§DC-1~4 코어 반영 완료). 이하 §1~§5는 직전 상태(Performance Tuning·산출물 수명).

> **🔴 갱신 2026-07-19(2) — Visual Contract 트랙 = 완결**(백로그 §B+§C 실체화·사용자 지시·본 커밋). 3 Wave: **W1** 필수 산출물 +3종(design-tokens·screen-mock·mock-convergence-record·touchpoint) + designElements 필수 요소 + design_completeness 요소 검사(fail-closed·하위호환 바이트 보존) + binding §7C mock 수렴 규약(기획 확정→1화면 3안 톤 수렴→**피드백은 정본 설계 산출물 먼저 갱신 후 mock 재생성**→사용자 수렴 기록→오케스트레이션 진입·04 §3.9 슬롯 물리화·spec 무수정) · **W2** designPrinciples(Figma UI 7·gist 자체 문면·출처 앵커)+accessibility-floor criteria 실값(WCAG AA)+§7A.1 디자이너 브리프 주입·§7C.3a 리뷰 차원 · **W3** UX 요소 3종(여정 맵·오류 복구·피드백 규칙)+Nielsen 10종(계 17)+근거 기록=문서 단위 1회. **사용자 결정(오버엔지니어링 방지): 강제 바닥 최소 — designElements=11종만, 제품 의존 항목(온보딩·사용자 유형·UX 카피·다국어)은 기본 세트 제외·인터뷰 표면화 시 프로젝트 policy 사본 데이터 추가로 편입**(부록 §2a·binding §7.2 (바) 메커니즘). 테스트 271→281(+10)·CP2 10항목 전건 Pass(신구 체커 바이트 대조·적대 실증·이탈 5건 전건 타당)·CP3 승인. planning/ARCHITECTURE §2·§7 부록 등재. 상세 = 메모리 `uaf-visual-contract-track`. **잔여(후속 후보): 설계→구현 충실도 게이트**(구현 화면↔mock·토큰 대조 — 구현 CP2 리뷰 차원 or dev-browser 스크린샷 대조·백로그 §D 연결)·scaffold 기본 토큰 템플릿(제품 2개째)·Interactive Prototype(조건 발동형).

> **🔴 갱신 2026-07-19(3) — OQ-PO-B2(해소 어휘 성숙) 종결 → §DC-9 계열 OQ 전건 마감.** 문서·설계 수준 종결(사용자 결정 A·엔진 코드 무변경): `orchestration/adapters/claude/project-orchestration-binding.md` §6/§7/§8만 갱신 — orchestration 해소 어휘가 재시도-비계수를 **이미 충족**함을 명문화(전용 `gate-resolved`/`outcome=pass`/`retry_count=0`; OQ-SH-5 fail-계수 결합은 `outcome=fail` 재사용 UAHF step-host 층 국한·무수정 경계상 별도 트랙)·stale 포인터 "05 §9 OQ 3"(05 spec §9=순수 이력표·OQ 절 부재·전수 실측) 정정·'해소 취소(revoke)' = 신규 **OQ-PO-B6** 저순위 재스코프. 순수 문서 변경(코드 델타 0). 상세 = §3 다음 작업·아래 §DC-9.

> **🔴 갱신 2026-07-21 — yt-stt Contract v3 + M1 구현 + 결함 수정 run 완주. 백로그 K·L·M 신설.**
>
> **소비 프로젝트 `yt-stt`**(`C:\my-claude-project\yt-stt` · UAF 밖 · **git 저장소 아님**):
> - **Contract v3 확정**(`pc-yt-stt-003`) — M0 실측 반영. 문서 9종 개정(Contract 신규 + Projection 7종 + 인덱스). v1(17,190B)·v2(12,998B) **문면 불변**(append-only PC-INV 9). CP2 11항목 → 지적 4건 조치 → 잔여 0 → 사용자 승인.
>   - RISK-2·RISK-12 **해소** / RISK-1 **부분 해소**(업스케일 전제로 1차 팩트 층 유지·강등안 부결) / RISK-6·9·10·11 **미해결 유지**.
>   - 신설: **OQ-M0-A**(광역 OCR 가독률 재측정·케이스 M0-3·임계 TBD) · **OCR 전처리 업스케일**(2x↑) 파이프라인 단계 · `ocrUpscale`/`upscale` 스키마 필드 · 환경 전제 2건(`HF_HUB_DISABLE_SYMLINKS=1`·자막 429 스킵).
> - **M1 run `impl-yt-stt-m1`** — 6단위 Passed · CP3 **Conditional** → 에스컬레이션 → Advisor 조건부 수용 → completed. 산출 `scripts/m1/` 7종.
> - **수정 run `impl-yt-stt-m1fix`** — 4단위 Passed · **rework 0** · CP3 Pass · completed. 결함 2계열 해소(`acquisition.py` glob 대괄호 4곳 → `os.listdir` 접두어 매칭 / `pipeline_m1.py` `assets_exist` → `_subtitle_check_complete`). 명세 = `yt-stt/M1-DEFECTS.md`. **Advisor 독립 실증 전건 통과**(엔진 AC 와 별개 케이스).
>
> **UAF 백로그 신설 3건**(기록만·미착수): **K** Projection 정본 포인터 stale(SD 성숙이 헤더 갱신 안 함 — append-only 라 파일이 실재해 **조용히 틀린다**) · **L** Run Observability(heartbeat·failure record·종료코드 규약·per-unit timeout·`--resume` run-id 재파생 함정) · **M** Cross-Unit Defect Sweep(**CP2 는 단위별이라 횡단 결함에 눈이 없다** — 먼저 통과한 동료 단위는 그대로 남는다).
>
> **실측 교훈 2건(재사용 가치 높음):**
> 1. **AC 가 구문·존재만 검사하면 동작이 틀려도 통과한다.** M1 원 결함이 그래서 통과했고, 수정 run 은 AC 를 **실증형**(tempfile 로 대괄호 폴더 생성 + 몽키패치로 함수 실제 호출)으로 바꿔 rework 0 으로 끝났다. **통과 자체가 증거가 되게 하라.**
> 2. **백그라운드 발사 시 파이프 금지·종료코드 보존·감시 무장.** 이 세션에서 엔진 종료 코드 `2`·`1`·`2` 가 하네스에 전부 `exit 0` 으로 보고됐다(파이프라인이 삼킴). 특히 두 번째는 **진짜 실패**였다. 규율 = 메모리 `feedback-background-task-watchdog`.

## §DC. 활성 트랙 (최우선) — UAF 설계 완성도·산출물 강제 (Design Completeness Enforcement)

용도: 아래 항목을 다른 세션에서 하나씩 수정한다. **§DC-1이 1순위.** 근거는 2026-07-18 세션 실측.

### §DC-1 [1순위] 전체 제품 설계(모든 메뉴·기능·프로세스·화면)를 산출·강제하는 단계가 없음
**증상(실측):** tms-system 오케스트레이션 run이 **UI/UX·전체 기능/화면/프로세스 설계 없이** 백엔드 구현 계획으로 직행했다.
- `tms-system/impl-plan.json` = 6 task **전부 백엔드/데이터**(domain·master·order-dispatch·settlement·audit + milestone). **UI/UX·화면·PRD·기능맵 task 0건.** SD-D2의 3접점(기사PWA·화주포털·내부웹)이 설계로도 구현으로도 없음.
- `orchestration/adapters/claude/contract_to_graph.py` seed 프롬프트가 Phase 1을 "마스터+수주+배차+정산코어"로 **하드코딩**하고 백엔드 결정(SD-D4/D7/D9/D11/D16)만 앵커 — UI/UX·기능맵·PRD 요구 0.
- 같은 파일 `gate_policy()` = proposal→user_decision·impl→review·milestone→approval. **설계완성도 게이트 없음.**
- 프레임워크 전체 스윕: UI/UX·설계완성도 **강제 규정 0건.** Discovery(`SKILL.md:42`)·SD 둘 다 "화면·기능은 하류"로 미루고 하류(구현 Planning)도 필수화 안 함.

**뿌리:** 전체 설계(PRD·UI/UX·프로세스)를 담을 **Projection이 비정본 부록·선택**(`planning/docs/appendix/projection-catalog.md`·04 §3.5 "예시일 뿐 강제 아님") → 컴파일러·게이트·훅 아무도 안 챙김. **("비정본이 항상 문제")**

### §DC-2 최소 필수 산출물 정의 + 정본화
- 최소 세트: (1) **전체 기능·범위 명세(PRD)** — 영역이 아니라 모든 기능 (2) **UI/UX 설계**(화면 목록·주요 플로우·와이어프레임 — 접점 선언 프로젝트 필수) (3) **전체 프로세스맵 + 데이터모델(ERD)** (4) **WBS**(위 3개에서 파생·Contract 직행 금지).
- **정본 승격:** 이 세트를 `planning/specs/04-solution-design.md`에 "필수 Projection 세트"로 등재(비정본 catalog → 정본). 컴파일러·게이트·훅 공통 참조원.

### §DC-3 [완결 2026-07-19] 강제 시점·메커니즘
- **시점 = 구현 착수 직전(설계→구현 경계·UAHF 넘기기 전).** 오케스트레이션 종료 시점 아님(다 짓고 검사는 늦음).
- **주 장치 = 엔진 게이트(완결):** `resolve_gate.py`가 `check_design_completeness`를 task_added 승격 직전 호출·**fail-closed**(§DC-1 Wave 3). 설계 미완이면 impl 편입 차단.
- **백스톱 = 차단형 훅(완결 2026-07-19):** `pretooluse_design_guard.py` PreToolUse **운영 훅** — 게이트-소비 워크스페이스의 `src/` Write 시 `check_design_completeness` 재실행, 설계 미완이면 deny. 리포 `.claude/settings.json` 배선 + scaffold 상속. **메인+서브에이전트 발화 라이브 실증.** 알림형(SessionStart)뿐이던 상태에서 차단형 신설 완료. 정본 경계 = `hooks-binding.md` §4.5(운영 훅≠Hooks Component·spec 08 무수정).
- **왜 둘 다:** 게이트=의미·승인(내용), 훅=존재 최후방어(그래프 오류로 새도 막음). 존재≠완성이므로 훅 단독 불충분. → 이중방어 실재.

### §DC-4 UI/UX 단계 신설
- 접점(웹·앱·포털)이 선언된 프로젝트는 UI/UX 설계 필수 단계. 현재 완전 부재.

### §DC-5~9 나머지 백로그 (전부 수정 대상)
- **§DC-5 [완결 2026-07-19] SD 협업 깊이:** 조사 확정 — 04 §3.4-C는 **이미 다라운드를 명령**(증상=spec 위반 아닌 실행층 공백: binding §7A.1 fresh-context 블라인드+resolve 1패스+§6.2 호스팅 유보). 해소 = binding **§7B** 다라운드 심의 규약 절차 신설(form-A·라운드 2+ 브리프에 동료 Proposal 동봉=fresh-context 유지·블라인드 해소·비소유 활성 역할 form-A 참여 브리프·상한 도달 시 잔여 충돌 Validating 표면화·실행 호스팅[04 §3.9] 불침범) + policy `deliberation`(maxRounds 3·convergence·peerVisibility — 값 정본 문면 = binding §7.2 (라)) + 브리프 템플릿 `{PEER_PROPOSALS}` 필드. **인터뷰 깊이:** 강제 floor(차원별 최소 깊이)는 **Frozen 02 충돌 판정**(Ready 판정식·DimensionSaturated·포화 스킵 — 문면 검증 CONFIRMED) → 사용자 결정 = 대안 A+B(θ 전 차원 +0.05·discovery-interview 스킬 v1.5 비구속 관행 3종), 대안 C(02 개정 트랙)=백로그 등재.
- **§DC-6 [완결 2026-07-19] 역할 상한 정책:** 실측 — 상한은 이미 4(Wave 5-A 반영)·본 백로그 문면("상한 3")이 stale였음. 해소 = 보안 조건부 역할 확충(whenSignal `regulated`·산출물 미소유·defaultRequiredSet 10종 불변) + `maxSpecialistRoles` **5**(사용자 결정) + 로더 **cap 집행 신설**(종전엔 값 미판독·미집행 — 선언순 우선·base 보존·`excludedByCap` 방출·Validating 게이트 표면화·역할명 하드코딩 0) + binding §7.2 (나)/§13/§14 값 동기화(**CP2 F-B drift 검출→U2 정정·재검증 Pass** — "Wave 경계 계약 통합검증 필수" 재적중). **이월→소멸:** tms 사본 policy 동기화 이월 건은 tms 트랙 종료·삭제(2026-07-19·앵커 `4934bc8`·ARCHIVE.md)로 소멸.
- **§DC-7 [완결 2026-07-19] WBS 소유 명문화:** 삼분(관리=엔진 / 초안 분해=Planner Lifecycle 역할 / 실행=Worker) 정본화. 접지가 3중 불일치(정본 무명 LLM step ↔ 배선 seed role=Worker ↔ DC-7 목표 Planner)를 드러냄 → 사용자 결정(배선 정정+명문화)으로 해소. **배선:** `contract_to_graph.py` seed proposal 노드 role·delegation.to Worker→Planner(자식 impl task는 Worker 유지)·217 tests pass. **명문화:** 05 §2.1/§3.4 명확화(+§9 이력)·`roles-quick-reference.md` §4 신설·AGENT.md/CLAUDE.md 2층에 중간 축·planner.md 2경로. 07·Glossary(Frozen) 무수정·재정의 0. 2경로(a 엔진 컴파일러가 Planner-role proposal step 디스패치 / b Advisor 직접 위임). scaffold 사본은 2층 부재로 반영 보류.
- **§DC-8 [완결 2026-07-19] 비정본 전수 스윕 (책임 있는 자율 원칙 적용):** 부록 4종·spec 04/05/02·runtime 4종(lifecycle·module-registry 포함)·전역 exhaustiveness를 4갈래 병렬 감사(원칙 (a) 테스트) → **비정본 승격 불필요 결론.** 강제-필요분은 DC-1이 이미 정리, 나머지 방대한 비정본은 정당 자율(SP-INV 5·UAF-INV ⑥가 카탈로그의 비정본 유지를 *강제* — 승격 시 오히려 불변 위반). 감사자가 올린 유일 후보(04 §3.9 Visual Contract)는 Advisor가 policy 실값 대조로 **정정** — 시각 산출물 3종(화면목록·메뉴·화면설계서)이 이미 `touchpoint`-required이고 §3.9는 협의 *방법론*이라 SP-INV 5상 정당 비정본.
  - **발견된 유일 실질 갭(스코프 밖 인접·해소):** 접점 **과소선언** + silent autoExclude. SP-INV 9는 *선언된* 범위만 강제하는데 접점을 선언하도록 강제하는 필드가 03에 없어(03 §3.2 필수 코어 필드 9종에 접점 부재), 접점 미선언 시 UI/UX 클래스가 **사용자 확인 없이 조용히** 제외(DC-1 증상이 다른 문으로 재발). Discovery 인터뷰 Skill은 전달 플랫폼을 elicit하나 `replaceable`이라 코어 보증 아님.
  - **옵션 (b) 해소(본 커밋·사용자 결정 2026-07-19):** `design_completeness.py`가 접점/연계 미선언으로 클래스 전체 제외 시 매니페스트 `classExclusions.<class>{reason,confirmedBy}` 확인을 요구(없으면 차단) — 고임팩트 이탈 표면화(원칙 (c)). policy `classExclusionOnNonDeclaration`·바인딩 §7.2/§7A.4·`design-manifest.schema.md`·테스트. **CP2 강제 실증**(BAD exit2·OK exit0·PARTIAL per-class 차단)·pytest 49·**CP3 승인**. 03·04 spec 무변경·SP-INV 5 보존·코어 무수정.
  - **잔여(백로그):** 옵션 (a) 03 필수 코어 필드에 접점 구조 필드 추가(결정적 검출·거버넌스 무게 큼) · runtime 관찰 1건(`replaceable=false` 근거 게이트 표면화 부재·저임팩트). 상세 = 메모리 `uaf-design-completeness-gap`·`uaf-accountable-autonomy-principle`.
- **§DC-9 [완결 2026-07-19] 05 wiring 후속:** **OQ-PO-B5 해소** — 엔진 `orchestrator._gate_event_exists`(→`_event_grounds_gate`) 강화: 정지 게이트 해소 선언(`ref.kind==gate-resolved`·`gateKind∈STOPPING_GATES`)+`gate_policy` 존재 시 `is_eligible_resolver` actor 자격까지 요구(수용+fold 양시점·방어적 이중화의 엔진 측 완성). 거동 보존 3면(레거시 `ref.kind="gate"`·비정지 gateKind·`gate_policy None`=실재-만 검증) — 일괄 적용 시 approval 근거 패턴 파괴를 실측으로 확인하고 범위 한정. **OQ-PO-B1 해소** — `render_gates.py` 신설(형태 B·결정적·LLM 0·원장 파생 읽기 전용·한국어 라벨 표=어댑터 데이터·적격 actor/해소 명령 정책 파생)+런처 정지 시 자동 출력(기존 `[STOP]`/`[PENDING-GATES]`·stop-signal 바이트 보존·렌더 실패 방어)+binding §3.2/§7/§8 확정. 테스트 217→234(+17)·CP2 10항목 전건 Pass(적대 실증·경계 6사례·중립성 0건·CLI 계약 교차 대조)·CP3 승인. 05 spec·gates.py·Frozen·`uahf/**` 무접촉. Stage B 실코드 산출은 다음 소비 프로젝트 몫(§3 참조) → `uaf-orchestration-wiring-gap` 메모리.

### §DC 좌표·정본 포인터 (착수용)
| 항목 | 위치 |
|---|---|
| 실측 산출물(백엔드만) | `git show 4934bc8:tms-system/impl-plan.json` (트랙 종료·삭제 — ARCHIVE.md) |
| seed 컴파일러·게이트 정책 | `orchestration/adapters/claude/contract_to_graph.py` |
| 강제 대상 정본 | `planning/specs/04-solution-design.md` §3.5 |
| 비정본(정본화 대상) | `planning/docs/appendix/projection-catalog.md` |
| 훅 메커니즘 | `.claude/settings.json`(SessionStart) · `.claude/hooks/` |
| 관련 메모리 | `uaf-design-completeness-gap` · `uaf-orchestration-wiring-gap` · `uaf-product-tms-system` |

## §1. 상태 앵커 (git log 대조 가능)

- **산출물 수명 정책 트랙 = 완결** (2026-07-17 사용자 결정·본 커밋): `docs/artifact-lifecycle-policy.md` 제정(`cd9247b`) → 일괄 정리(삭제 406파일 앵커 보존·`ARCHIVE.md` 원장 17행·활성 문서 61개 앵커 전환/판례 인용 제거·CP2 Fail 1건 정정 후 재검증 Pass·pytest 4-트리 236/236). 핸드오프 판례 인용은 전량 제거(라우팅 장치 없음 — 근거는 L-XX·mi·정본 §만). 이연 확인: 2차 산출물 디커플링 트랙(상류 바인딩 데이터 위치 확정)·Frozen spec 02/03의 옛 경로 "예정" 열거(무촉 판정).
- **Performance Tuning Track = 종료** (2026-07-14 사용자 확정). Core Tuning 구현·CP2 검증 결과 유지. **T6/T7 동형 벤치마크·Before/After는 미실시**(사용자 결정 — 아래 §2 결정 기록).
- 완료 단계·커밋:

| 단계 | 커밋 | 요지 |
|---|---|---|
| T0 Baseline Freeze | `013e532` | 앵커 동결(UAHF `ad451ee`·consumer `dd2fd73`) |
| T1 Minimal Telemetry | `d9b2ac6` | collect_metrics.py·산식 고정·stop-signal 위상 아카이브 |
| T2 Review 게이트 evidence 재사용 | `f47ce91` | 재검증 세션 소비 대체·stale 3규칙 fail-closed |
| T3+T4-① 검증 아키텍처·delegation 참조형 | `891e9aa` | verify_run.py(LLM 0)·Risk Routing 배선·섀도 장치(기본 off)·sentinel 표준 |
| T3-② cp2ModelSlots 스키마 등재 | `adaafe9` | 위험도별 CP2 모델 차등 활성화(dormant 해소) |
| T1-② payload 계측 + R3 러너 | `e1147c4` | bundle_payload 지표(baseline 343,183B/37세션)·run_all_tests.py |
| T4-② 핸드오프 재구조화 | `2342659` | 착수 강제 read-set 61,145B→5,331B(-91.3%)·상태 앵커·갱신 규율 |
| 트랙 종료 마감 | (2026-07-14) | 종료 상태 기록·Memory 갱신 |

- 번호 표기 주의: plan §4 항목-ID는 T0~T7(T6=벤치마크+Before/After 통합·T7=Concurrency — **T8은 §4 항목-ID에 부존**), §5 순서 번호는 0~9. 본 파일은 두 체계를 병기한다.
- Baseline 앵커(불변): UAHF `ad451ee` · consumer `dd2fd73` · Freeze `013e532`. Baseline run evidence(orch-k/m/w·maturation-r003·greenfield-r003)는 앵커 커밋으로 보존 — 열람은 `ARCHIVE.md` 원장 참조.
- consumer(`uahf-control-plane`) 워킹트리: 사용자 변경분 미커밋 보존 — 수정 금지.

## §2. 트랙 종료 결정 기록 (사용자 확정 2026-07-14)

1. 현재 구현·CP2 검증 결과 유지(재작업 없음).
2. 추가 A/B·동형 벤치마크(plan §4 T6 = §5 순서 6·7)는 지금 수행하지 않음.
3. **측정 인프라 유지 + 실사용 누적**: 향후 실제 UAHF 사용(신규 orchestration run)마다 `collect_metrics.py`(bundle_payload 포함)·`verify_run.py`를 신규 runId 산출물에 실행해 `e2e/metrics/`에 산출한다. 산출물은 ephemeral — 트랙 마감 시 evidence 승격분만 앵커 등재 후 정리한다(`docs/artifact-lifecycle-policy.md` §3).
4. **재개 조건**: 실사용에서 실제 병목이 관찰되면 누적 측정 데이터를 근거로 **별도 Performance Tuning 트랙을 새로 연다**(느낌 기반 재개 금지 — Measurement First 유지).
5. Post-Tuning Backlog(A~G·우선순위 B+C→D→G→A+F→E) 미구현 항목은 향후 후보로 유지.
6. 본 핸드오프에 상태·다음 시작점 기록.

## §3. 다음 작업 (별도 새 세션 — 본 세션 미착수)

- ~~[1순위] §DC-9 05 wiring 후속~~ — **완결 2026-07-19**(상세 위 §DC-9). ~~잔여 OQ = B2~~ → **OQ-PO-B2(해소 어휘 성숙) = 종결 2026-07-19**(문서·설계 수준·사용자 결정 A·엔진 코드 무변경). binding §6/§7/§8만 갱신: orchestration 해소 어휘가 재시도-비계수를 **이미 충족**함을 명문화(`gate-resolved`/`outcome=pass`/`retry_count=0` — OQ-SH-5 fail-계수 결합은 `outcome=fail` 재사용 UAHF step-host 층 국한·무수정 경계상 별도 트랙)·stale 포인터 "05 §9 OQ 3"(05엔 OQ 절 부재·실측) 정정·'해소 취소'는 신규 **OQ-PO-B6** 저순위 재스코프. **§DC-9 계열 OQ 전건 종결.**
### 🔵 2026-07-21 기준 다음 착수 (1순위 = 사용자 확정 2026-07-21)

## ★ 1순위 — yt-stt **M1 실기 검증** (M2 보다 먼저)

**왜 M2 가 아닌가.** M1 코드는 **한 번도 실행된 적이 없다** — 오프라인 AC(구문·존재·합성 단위 테스트)만 통과했고 실제 `yt-dlp`·`ffmpeg` 호출 경로는 미검증이다. 특히 2026-07-21 수정한 **자산 스킵 로직(429 재발방지)은 논리로만 검증**됐다. 이 상태로 M2 를 쌓으면 미실행 층 위에 쌓는 것이다.

**이 프로젝트의 사고 이력이 정확히 M1 층에 몰려 있다**(HANDOFF §6): ① "자막 없음" 오판(`--print` 무효 지정자가 NA 를 냄 — 실제로는 자막이 있었다) ② 위상 반전 무음(STT 가 180초를 3.6초에 "처리"하고 0줄 산출 — **실패가 성공처럼 보였다**). 둘 다 **실제로 돌려봐야만** 드러났다.

**비용이 낮고 조건이 최적이다.** `yt-stt/out/m0-probe/` 에 기준선 2영상의 자산(`video.720p.mp4`·`audio.mp3`·`subs/`)이 이미 있다. **자산이 존재하는 상태 자체가 스킵 로직의 시험 조건**이다 — 재다운로드가 일어나면 수정 실패, 안 일어나면 성공.

**확인 항목 5종:**
1. **자산 스킵** — 기존 자산에 `run_acquisition` 이 재호출되지 않는가(429 재발방지 실증·이번 수정의 실경로 검증)
2. **자막 판별** — `--list-subs` 가 두 영상의 한국어 자동자막을 실제로 잡는가(`--print` 금지 규칙이 실효 있는가)
3. **다운믹스 실측 선택** — mono/left/right 레벨 비교가 실제 오디오에서 동작하는가(`-ac 1` 맹목 금지)
4. **무음 실패 게이트** — 정상 오디오를 무음으로 **오판하지 않는가**(false positive 확인)
5. **`DEFAULT_SILENCE_THRESHOLD_DB`** 가 실제 측정치와 맞는가 — 현재 이 상수의 근거가 실측인지 도메인 상식인지 **미확인**이다

**최소 read-set**: `yt-stt/scripts/m1/` + `yt-stt/docs/interface-spec.md` §1·§3 + 메모리 `uaf-product-yt-stt`.
**주의**: yt-stt 는 이제 git 저장소다(베이스라인 `5472522`) — 실기 실행이 워크스페이스를 오염시켜도 되돌릴 수 있다.

---

## 2순위 이하 후보

**(가) yt-stt M2 구현 — 실기 검증 통과 후**
- ⚠ **선결**: RISK-6(OCR 용어 선별 규칙·주체)은 **여전히 open** 이다. 필요성만 실증됐고 규칙은 미정 — M2 착수 시 이 결정을 먼저 내려야 한다.
```
python orchestration/adapters/claude/orchestrate_project.py "C:/my-claude-project/yt-stt" \
  --phase "M2" --mode incremental --run-id impl-yt-stt-m2 > <로그파일> 2>&1
echo "ENGINE_EXIT=$?" >> <로그파일>
```
- M2 = 1차 팩트 층(수동/번인 자막 확정 전사 + 화면 OCR). **OCR 경로 = 프레임 → OCR 전처리 업스케일(2x↑) → WinRT OCR**(v3 신규 결정).
- 착수 전 최소 read-set: `yt-stt/.claude/project-contract/project-contract.v3.md` + `yt-stt/docs/project-plan.md` §1 M2 + 메모리 `uaf-product-yt-stt`.
- **M2 에서 반드시 확인할 것**: RISK-6 선별 관문(무선별 힌트 주입 금지는 **실증**됨 — 규칙은 여전히 open) · `ocrUpscale`/`upscale` 기록 · OQ-M0-A 대응 케이스 M0-3.

**(나) yt-stt 실기 검증 — 오프라인 미검증분 해소**
- M1 산출은 **코드 구조·판정 논리만 실증**됐다. 실제 `yt-dlp`/`ffmpeg` 실행은 AC 범위 밖(오프라인 환경).
- 미확인: `DEFAULT_SILENCE_THRESHOLD_DB` 상수 근거(실측 vs 도메인 상식).

**(다) UAF 백로그 K·L·M 착수** — 셋 다 이번 세션 실측 기반. **L 이 J 의 상류**이므로 J 착수 시 L 을 선행으로 묶을 것.

**(라) M3 착수 시 선결 확인(잊으면 사고)**: 무음 게이트의 `{"failed": True}` 를 STT 층이 실제로 확인하는가. **"무음이면 STT 로 넘기지 않는다"는 강제가 코드가 아니라 규약에만 있다** — 위상 반전 사고(HANDOFF §6-①) 재발 경로가 정확히 여기다.

**(마) 커밋 미실시** — 이번 세션 변경(백로그 K·L·M · 본 핸드오프 · run 원장 3건)은 **미커밋**이다. 소비 프로젝트 `yt-stt` 는 git 저장소가 아니어서 되돌리기·해시 검증이 불가하다는 점 유의.

---

- **기존 트랙 후보**(우선순위 미확정 — 확정 권위는 사용자):
  - **Interview Entry-to-Runtime Audit** (사용자 지정 2026-07-14 — 차순위 유지). 정의·범위·성공 기준은 착수 세션에서 사용자 지시로 확정한다 — 본 파일은 명칭과 시작점만 기록하며 범위를 추정하지 않는다. 착수 시 최소 read-set: 본 §1 앵커 + 착수 세션의 사용자 지시. 관련 정본은 필요 §만 demand-driven(후보 포인터: `entry/specs/01-entry.md`·`discovery`/`orchestration` specs — 실제 선택은 지시 범위 확정 후).
  - ~~seed 컴파일러 tms 하드코딩 일반화~~ — **완결 2026-07-19**(사용자 지정·본 커밋). `contract_to_graph.py` 도메인 하드코딩 전면 제거: 프로젝트 표기/버전/run_id/seed id/경계 문구 = 파생(root.name·파일명 v\<N\>·`_slug`·내용 파싱 0 불변), 도메인 설계 앵커 블록 → 일반 지시(설계 앵커 자가 식별·결정 식별자 인용·**전 영역 계층 편향 없이 커버** — §DC-1 백엔드 편향 뿌리 제거), `resolve_gate.py` `PROPOSING_STEP_REF` 하드코딩 제거 → graph.json proposal 노드 파생(F4↔F5 교차 계약 동시·통합 관통 테스트). 테스트 234→245(+11)·CP2 10항목 전건 Pass(적대 픽스처 acme-erp v3 도메인 토큰 유출 0·순수성 해시 실증)·CP3 승인. binding §8 1행(§5.7 역사 기록 무촉). **Stage B 실코드 실증의 선행 조건 해소** — 다음 소비 프로젝트에서 즉시 착수 가능. CP2 관찰(비차단): 오프라인 AC allowlist의 python/node 경사(환경 제약·비-JS/Python 스택 등장 시 확장 검토 백로그).
  - **§DC-8(a)** 03 접점 코어 필드 · **02 개정 트랙**(강제 깊이 바닥·U4 대안 C) — 백로그.
- **Interview Entry-to-Runtime Audit** (사용자 지정 2026-07-14 — 차순위 유지). 정의·범위·성공 기준은 착수 세션에서 사용자 지시로 확정한다 — 본 파일은 명칭과 시작점만 기록하며 범위를 추정하지 않는다. 착수 시 최소 read-set: 본 §1 앵커 + 착수 세션의 사용자 지시. 관련 정본은 필요 §만 demand-driven(후보 포인터: `entry/specs/01-entry.md`·`discovery`/`orchestration` specs — 실제 선택은 지시 범위 확정 후).

## §4. 미결·이월 항목 (다음 관련 세션에서 참조)

- **번호 표기 이중 체계(주의)**: plan §4 항목-ID(T0~T7)와 §5 순서 번호(0~9)가 병존 — 본 파일·후속 기록은 두 체계를 병기한다(T4-② CP2 r1~r3 경위). plan 파일 자체에는 "T0~T8" 문자열이 없음(CP2 전수 스윕 확증 — 과거 Memory 색인의 "(T0~T8)" 표기가 오기였고 Memory 측을 정정).
- **Continuous Telemetry / Lifecycle Observability = 백로그 §H 등재**(2026-07-14 사용자 지시 — **기록만·구현 보류**): 전체 lifecycle 지속 누적 관측·Telemetry Session Skill + deterministic script/CLI 후보·미해결 질문 5종 = `docs/post-tuning-improvement-backlog.md` §H 참조. 재개 트리거 = 실사용 병목 반복 관찰.
- T5 Gate Notification = 보류(그룹 B·C지표 전용 — Operational UX 트랙 후보·백로그 유지).
- 첫 실 적용 대기: T2 evidence 재사용 섀도 대조·descriptor-aware CP2(cp2ModelSlots) 첫 사용·섀도 장치 기동 — 향후 실 orchestration run에서(§2-3 누적과 병행).
- Skill Extraction P1(Post-Tuning G 시딩): CP2 게이트워크 Skill·하네스 CP2 evidence packet 표준화·소비측 Skill 표면(Scaffold 선행 필요).

## §5. 갱신 규율 (stale 재발 방지 — 유지)

- **각 단계/트랙 경계 커밋에 본 파일 §1 상태 앵커 갱신을 포함한다.**
- 본 파일은 값 중복 최소·정본 포인터 우선. 본 파일과 정본이 충돌하면 정본(git log·해당 spec/plan)이 우선한다.

## 정본 포인터

| 항목 | 위치 |
|---|---|
| 산출물 수명·삭제·앵커 인용 정책 | `docs/artifact-lifecycle-policy.md` |
| 아카이브 원장 (앵커 열람) | `ARCHIVE.md` |
| 백로그 (Post-Tuning A~G·H) | `docs/post-tuning-improvement-backlog.md` |
| 측정·검증 도구 (유지 대상) | `orchestration-data/e2e/{run_all_tests.py,collect_metrics.py,verify_run.py,delegation_check.py}` |
| Risk Routing 정책 | `orchestration-data/e2e/policy/{allocation.json,README.md}` |
| UAHF Contract | `discovery-data/contracts/uahf/project-contract.v3.md` |
| 과거 핸드오프 이력 | git 이력 (`git log -- docs/session-handoff.md docs/next-session-prompt.md`) · 튜닝 정본·1차 실측 문서는 `ARCHIVE.md` 앵커 참조 |
