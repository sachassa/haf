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

> **🔴 갱신 2026-07-21(2) — yt-stt M1 실기 검증 완료 + 결함 2차 수정 run 완주. UAF 백로그 L 보강·N·O 신설. 규율 2건 정본화.**
>
> **1순위였던 M1 실기 검증 = 종결.** Advisor 직접 실기(m0-probe 자산을 M1 저장 규약 폴더로 **하드링크**해 재다운로드 0) 결과 5종 중 **1 PASS / 3 FAIL / 1 조건부**. 1차 수정 run 이 해소한 **자산 스킵은 실경로에서 유효**함이 확인됐고(yt-dlp 0회), 나머지 3종이 실패했다. 원인은 **HANDOFF ①·② 원사고의 재발**:
> - **결함1** `_parse_list_subs_output` 이 실제 헤더 `[info] Available automatic captions for <id>:` 를 `startswith("Available …")` 로 검사 → **입력 무관 항상 빈 목록**. M0 프로브는 `search()` 라 정상이었던 **재작성 회귀**. (덤: 꼬리줄 `<id> has no subtitles` 흡수가 M0 meta 언어목록에 영상ID 가 섞인 원인)
> - **결함2** `subprocess.run(..., text=True)` 가 cp949 로 디코딩 → 한글 경로 stderr 에서 `UnicodeDecodeError` 가 **reader 스레드에서** 터져 주 흐름은 `rc==0` 수신·stderr 만 유실 → `-90.0` 폴백 → 동률 시 `max()` 가 dict 첫 키 **`mono`(위상 상쇄 채널)** 선택 → **정상 오디오(-21.8dB)를 무음 실패로 오판**.
> - **결함3(설계 공백)** 파서를 고치면 auto 157종이 `--sub-langs` 에 전량 투입 → 429 직행. 스펙에 자막 **언어 선택 규칙 부재**. → **사용자 확정: 원어(`-orig` 표기) + 요청 언어(기본 `ko`)만 다운로드 · 판별 157종은 meta 전량 보존**(F3).
>
> **수정 run `impl-yt-stt-m1fix2`** — 4단위 전건 Passed · CP2 4건 pass · **rework 0 · escalation 0** · 실측 **40.6분**. 명세 = `yt-stt/M1-DEFECTS-2.md`, 실출력 픽스처 = `yt-stt/fixtures/yt-dlp.list-subs.*.txt` 2건. 사용자 **조건부 승인**(보강 2건: 측정실패≠무음 구분 필수화 · `run_acquisition` 시그니처 호환 실검증).
> **Advisor 독립 실증 6/6 PASS**(엔진 AC 미호출·별도 작성 · `audio16k.wav` 삭제 후 전 구간 재실행): 파서 157종·`ko`/`ko-orig` · 측정실패→`downmix-measurement-failed` 구분 · `--sub-langs=['ko-orig']`+판별 157종 보존 · 시그니처 호환 · 원어 미검출 fallback · `failed=False`·yt-dlp 0회·mono -54.8/left -22.0/right -21.8→right(**M0 실측과 정확 일치**). `text=True` 잔존 0. → **CP3 승인.**
>
> **M1 실기 5종 최종**: ①자산스킵 ✅ ②자막판별 ✅ ③다운믹스 실측 ✅ ④무음게이트 오탐 ✅ ⑤`DEFAULT_SILENCE_THRESHOLD_DB` 🟡 — **판정: 도메인 상식값이며 실측 1건이 우연히 뒷받침**(정상 -21.8 대 임계 -50 마진 28.2dB / 상쇄 -54.8 은 임계 아래 **4.8dB 뿐**·표본 2영상). 실측에서 도출된 값이 아니다 → OQ 후보.
>
> **비차단 관찰 2건**: (a) `ko-orig` 의 base 가 `ko` 라 "같으면 하나만" 규칙에 걸려 **`ko` 트랙은 받지 않는다** — 명세 문구대로지만 유튜브에서 두 트랙은 다를 수 있음(자동자막=4차 잔여·참고 등급이라 비치명·**M2 확인 필요**). (b) `meta.downmix.measurements` 구조가 스칼라→`{level_db, measured}` 로 변경 — `table-def.md:231` 이 구조를 못박지 않아 위반 아니나 M2/M3 소비 시 주의.
>
> **UAF 하네스 측 산출:**
> - **백로그 L 보강** — `--resume` run-id 재파생 함정을 **등재 뒤 같은 세션에 다시 밟았고**, 근본 원인 하나가 더 드러났다: **`.claude/commands/uaf-implement.md` §2 재개 예시가 `--resume` 만 표기**해 런처 계약과 어긋난다(`--run-id` 를 준 run 은 그 예시대로 하면 반드시 실패). **예시 정정은 코드 변경 0 으로 즉시 가능.**
> - **백로그 N 신설** — 조건부 승인의 하류 전달 배선 부재. `resolve_gate.py --response` 는 provenance 기록 전용이고 승격되는 건 `impl-plan.json` 본문이라, 보강 반영을 위해 **Advisor 가 Worker 산출물을 직접 편집**해야 했다(백업 `impl-plan.json.pre-advisor-augment`+provenance 기록으로 정직 처리했으나 **관행이지 강제가 아님**). J 와 같은 계열 — J=거부 후 재작업 채널 부재, N=**승인하면서 조건 붙일 채널 부재**.
> - **백로그 O 신설** — AC 실출력 픽스처 규율 + 자기출제 구조. **"실증형 AC" 라벨은 충분조건이 아니다** — 몽키패치로 *내 함수*를 실호출하는 것과 **외부 프로세스의 실제 출력을 먹이는 것**은 다른 층위다. M(횡단 결함)과 인접하나 별건(M 을 고쳐도 O 는 남는다).
> - **규율 2건 정본화(메모리→문서)** — 사용자 지적: *"메모리만 기록되어 있는 게 문제다. UAF 문서에서 제어되어야지. 메모리 리셋하면 어떻게 되는데"*. 메모리는 **비정본이라 강제 근거가 아니고**(책임 있는 자율 (a)), worktree 는 경로 기반이라 **메모리 네임스페이스가 갈려 처음부터 안 보인다**(실측 확인). → `.claude/AGENT.md` §Invariants 에 **관측 경로 유실 금지**(= 실패 은폐 금지의 기계적 대응물)·**침묵의 성공 해석 금지** 추가(도구 중립), `.claude/CLAUDE.md` 에 이 환경 배선 신설(파이프 금지·exit 보존·timeout·**Monitor 판단기준=완료 알림만으로 충분한가**·무장엔 해제가 짝·필터 커버리지·`PYTHONIOENCODING=utf-8`). 기계 강제(SessionStart 훅)는 **미도입**.
>
> **잔여**: UAF 자체 스크립트의 인코딩 전수 스윕 미실시(이 세션에서 `graph.json` 출력이 `UnicodeEncodeError` 로 깨진 실측 있음) · 메모리 13종 중 "강제 필요한데 메모리에만 있는" 항목 재검토 미실시.

> **🔴 갱신 2026-07-21(3) — yt-stt 화면 OCR 층 재배치 결정 + 영향 감사 168건 + UAF 이진 원칙 정본화·기계 강제.**
>
> ## ① yt-stt — 화면 OCR 을 1차 팩트에서 최후 수단으로 내린다 (사용자 확정)
>
> M1 실기 검증 후속으로 OCR 실물을 열어본 결과 **소스 영상이 강의실 촬영**이었다(`frames/transition/frame_0020.png` 육안 확인). 슬라이드가 빔프로젝터로 투사된 것을 멀리서 찍어 실효 해상도가 무너지고, 슬라이드 안에 페이스북 광고관리자 스크린샷이 또 들어 있어 2중 축소이며, 배경(수강생·노트북·천장·창문)까지 OCR 이 읽어 `(| 돈까리시 라1| NAWR` 같은 잡음을 낸다. 40프레임 OCR 결과는 **동일 문자열 반복 0회**(같은 로고가 `개시트리`/`캐시트리`/`캐시트길`/`구귀트리Q` 등 7가지 이상으로 흔들림).
> - M0 가 "2x 업스케일로 정확 판독" 을 측정한 `ocr-diag/720p.png` 는 **슬라이드 풀스크린 편집 화면**이다. 같은 영상에 두 종류 화면이 섞여 있고 40장은 후자 위주였다. 즉 **RISK-2 "해소" 판정은 화면 캡처형 슬라이드에 한정**된다.
> - 표본 2영상 모두 **수동 자막이 없다**(`fixtures/*.txt` 의 `has no subtitles`). `ko-orig` 도 자동자막 섹션 소속이라 ASR 파생이다. 즉 이 영상들의 1차 팩트 층은 공집합이었고, 그래서 OCR 이 유일한 팩트원으로 떠받쳐지고 있었다.
>
> **확정 구조**: `P0 수집 → 자막 판별 → [수동 자막 有] P1 1차 팩트=자막 확정 전사 / [無] 1차 팩트 공집합 → P2 STT 본체 → P3 문맥 교정 → [오독 잔존] 해당 구간 on-demand 프레임 → PPT 형태만 참고 → 확신 없으면 원문 유지`.
> - 프레임 게이트 2분류: **① PPT형 텍스트 화면 = 참고 / ③ 비정형(사람 등) = 제외**. 애매하면 ③(오교정 0 우선 비대칭). **② 자막 구간은 삭제** — 유튜브가 `--write-subs` 로 텍스트를 직접 주므로 번인 자막 OCR 은 원 도구의 잔재다.
> - **사용자 결정 4건**: (a) **R5** — 참고 등급 근거로도 숫자를 확정한다(R1 "참고자료 단독 확정 불가" 에 화면 예외 조항 신설) · (b) **R1 서열** — 화면을 문맥 **아래**로(`자막 팩트 > 문맥 > 화면 > 참고자료`) · (c) **STT 힌트** — OCR 유래는 소멸, **자막·사전 유래는 존치** · (d) 개정은 다음 세션.
>
> ## ② 영향 감사 — [A] 수정 168건 · [C] 삭제 23곳 · 판단 보류 20건
>
> 3 병렬 감사(Contract v3 / 상류 4종 / 하류 4종). **스윕 범위** = `.claude/project-contract/project-contract.v3.md` + `docs/*.md` 8종 + `design-manifest.json` + `policy/default-policy.yaml` = 11파일. 각 감사자가 전문 통독 + ripgrep 패턴 스윕을 병행했고 각자 한계를 명시했다. **manifest·policy 는 무영향**. v1·v2 는 append-only 불변이라 대상 밖.
>
> **★ Contract v4 발행이 Projection 개정보다 선행한다.** Contract v3 L18~19 가 구설계("1차 팩트(수동/번인 자막·화면 OCR)")를 **계약 본문으로 선언**하고 docs 8종이 모두 머리말에 "근거 정본 = Contract v3" 를 명시한다. Projection 만 고치면 하위 문서가 정본을 배신한다(CLAUDE.md "Architecture↔Spec 충돌은 사용자 보고" 규율 해당).
>
> **누락되기 쉬운 지점 3종(감사자 지목)**:
> - **"OCR 경로 = 프레임 → 업스케일 → WinRT OCR" 이 6개 문서에 중복 선언**. 경로 자체는 유효하고 **소속만 P1 → P3 후단으로 이동**하므로, 6곳을 동시에 옮기지 않으면 P1 잔재가 남는다.
> - **OQ-M0-A 동일 문장이 5곳에 복제**("재측정 낮으면 1차 팩트 층 지위 재검토"). 한 곳만 고치면 나머지가 폐기된 지위를 계속 가리킨다. 재검토가 이미 끝났으므로 OQ 자체가 종결 대상이다.
> - **RISK-1 배너 정본 문면이 4곳에 바이트 동일 요구**(`table-def` L273 · `interface-spec` L227 · `requirements-def` FR-3(f) · `test-plan-cases` L147).
>
> **구조 파급(내가 놓쳤던 것)**:
> - **역류(back-edge) 신설** — "앞 층 산출이 뒤 층 입력" 원칙에 P3 산출이 OCR 대상을 결정하는 역방향 간선이 생긴다. 3개 문서가 각각 이 원칙을 서술한다.
> - **교정의 입력이 출력 이후로 이동** — `interface-spec §5.2` 가 팩트 층(OCR·자막)을 교정 **입력**으로 정의한다.
> - **M4↔M5 의존 역전** — 시점 프레임 추출(FR-10)이 M5 인데 최후 수단 OCR(M4)이 그걸 입력으로 요구한다. M4 이전으로 당겨야 한다.
> - **TRAP-2·TRAP-8 이 "번인 자막 근거로만 확정" 을 회귀 정답 판정 규칙으로 사용** — 번인 경로 삭제가 회귀 기준선 판정에 닿는다.
> - **`facts/burnt-in.md` 에 이미 생성 경로가 둘**(`table-def §2.1` 텍스트 파생=존치 / `interface-spec §4.2` OCR 출력=삭제). 현 상태에서 이미 잠재 모순이었고, OCR 경로만 지우면 이름과 내용이 어긋난다.
> - **같은 날 사용자 결정 2건이 정반대** — `project-plan` L99 가 강등 폴백을 "부결(2026-07-21 사용자 확정)" 로 원장 기록했는데 오늘 결정이 그 방향이다. 이력 보존 + 후행 결정 레코드 추가가 필요하다.
> - **어느 문서에도 없어 신설이 필요한 것 3건**: "수동 자막 없음 → 1차 팩트 공집합" · "PPT 형태 판정 게이트" · "P3 잔여 오독 → on-demand 자동 트리거". 감사자들이 "부재는 스윕으로 증명되지 않는다" 는 한계를 달아 보고했다.
>
> ## ③ UAF — 이진 원칙 정본화 + PreToolUse 기계 강제 (커밋 `164e41b`·푸시 완료)
>
> 사용자 지적: *"애매한 근거가 항상 문제를 일으킨다. 비정본·확인필요는 강제성이 없으니 다른 세션이나 구현 단계에서 넘어가 버린다. 해도 그만 안 해도 그만인 것을 UAF 에서 없애고 0 아니면 1 로 하자."*
> 문제의 정체는 애매함이 아니라 **판정 불가**다 — 게이트는 통과/차단만 판정하는데 "부분 해소"·"조건부 확정"·"판정 보류" 는 0 도 1 도 아니라 아무것도 막지 못하고 **관성 통과**한다. 같은 세션에서 6회 재현(그중 1건은 Advisor 가 `M1-DEFECTS-2.md` 에 쓴 "부수 방어(권장)" 가 실행층에서 실제 누락된 것).
> - **AGENT.md §Invariants 불변 2건 신설**(도구 중립): **이진 상태(0 아니면 1)** · **근거 표기 이진(확인함 아니면 추정)**. 두 불변에 같은 구조를 넣었다 — **"정당하되 하류를 막는다"**. 미해소도 추정도 금지 대상이 아니라 진행을 멈추는 신호다(자율을 죽이지 않고 자율의 조건을 명시).
> - **`.claude/hooks/binary_state_guard.py`** 신설 — PreToolUse 운영 훅. `pretooluse_design_guard.py` 계약 동형(stdin JSON → stdout deny + exit 0), **fail-open**(자기-DoS 방지), 스코프 = **새로 쓰는 텍스트만**(`Write.content`/`Edit.new_string`·기존 본문 미판독 = 사용자 결정 "신규부터 + 닿는 것만"), 대상 = `.md` 만. 이탈은 `uaf-allow-legacy:`/`uaf-verified:`/`uaf-assumed:` 마커로 사유 기록 시 통과. `settings.json` 배선 + CLAUDE.md 배선 문서.
> - **단위 검증 16/16 PASS**. **라이브 차단은 미실증** — `settings.json` 은 세션 시작 시 읽히므로 현 세션에서 금지어 `.md` 쓰기가 차단되지 않았다. 단위 검증만으로 작동을 주장하지 않는다.
>
> ## ④ 다음 세션 진입 순서
>
> 1. ~~**[1순위] 훅 라이브 차단 실증**~~ → **완료 2026-07-21(4)** — 차단 확인. 다만 원인은 훅 로직이 아니라 **배선 경로**였다(아래 갱신 블록 참조).
> 2. **yt-stt Contract v4 작성**(append-only·v1~v3 문면 불변) — 위 ① 결정 4건 + RISK-1/2/6 판정 갱신 + OQ-M0-A·OQ-1 처분. **v4 없이 Projection 을 건드리지 않는다.**
> 3. **Projection 8종 개정** — 감사 [A] 168건·[C] 23곳. 위 "누락되기 쉬운 지점 3종" 을 체크리스트로 쓸 것.
> 4. **Advisor 기술 안 7건 일괄 승인** — `layer` 값 집합(F/S/C/R 에 최후 참고 OCR 자리 없음) · `frames/transition` 존폐 · `facts/burnt-in.md` 개명 · `selected_terms` 처분 · M4↔M5 의존 순서 · 최후 단계 프로세스 번호 · OQ-1 처분.
> 5. 최소 read-set: 본 갱신 블록 + `yt-stt/.claude/project-contract/project-contract.v3.md` + 메모리 `uaf-product-yt-stt`.
>
> **미완(정직 기록)**: 훅 라이브 실증 · UAF 자체 스크립트 인코딩 스윕 · 메모리 중 "강제 필요한데 메모리에만 있는" 항목 재검토 · 감사 판단 보류 20건 중 사용자 결정분 외 나머지.

> **🔴 갱신 2026-07-21(4) — 훅 라이브 차단 실증 완료. 원인은 훅이 아니라 배선 경로였고, 설계완성도 백스톱도 같은 결함을 공유했다.**
>
> **1순위였던 훅 라이브 차단 실증 = 종결.** 다만 결과가 예상과 달랐다 — 첫 시도에서 금지어 `.md` 쓰기가 **차단되지 않았다**. 훅 스크립트 자체는 동일 페이로드를 stdin 으로 주면 정확한 deny JSON + exit 0 을 내므로, 문제는 로직이 아니라 **`.claude/settings.json` 배선**이었다.
>
> **원인 = `$CLAUDE_PROJECT_DIR`.** 이 환경(Windows 10 + Git Bash + `shell: "bash"`)의 PreToolUse 훅에서 이 변수형 경로는 차단을 내지 못한다. **A-B-A 대조로 확정**했다 — 절대경로=차단 → 변수형=통과 → 절대경로=차단(동일 세션·훅 핫리로드·변수 하나만 교체). 상대경로도 차단이 확인돼, 사용자 결정으로 **상대경로**를 최종 형태로 확정했다(scaffold 는 설치 경로가 미정이라 절대경로를 쓸 수 없어 규칙이 하나로 통일된다).
> - **왜 눈에 안 띄었나.** 훅 명령이 실패해도 도구 호출은 **조용히 통과**한다. 배선이 죽어도 표면에 아무 신호가 없다 — `.claude/AGENT.md` §Invariants **침묵의 성공 해석 금지**가 정확히 걸리는 지점이다. 그래서 **단위 검증(16/16 PASS)이 통과했는데 실제로는 아무것도 막지 못하는 상태**가 이틀간 유지됐다.
> - **파급 — 설계완성도 백스톱(§DC-3)도 같은 배선이었다.** 도입 커밋 `7241710`(2026-07-19)부터 변수형이었음을 git 이력으로 확인했다. 즉 **§DC-3 이중방어의 백스톱 축이 죽어 있었을 개연이 있다.** 사용자 지시로 재실증했고, 상대경로 배선에서 설계 미완 워크스페이스의 `src/` Write 가 `[DESIGN-INCOMPLETE]` 로 **차단**됨을 확인했다(스코프 밖 `docs/` 는 통과 — 오탐 없음).
> - **미해소**: `hooks-binding.md` §4.5 는 2026-07-19 에 변수형 배선으로 "메인+서브에이전트 Write 둘 다 deny 차단 확증" 을 기록한다. 오늘 실측과 충돌하며, **환경 변화인지 기록 오류인지 판별하지 못했다**(당시 세션 재현 불가). 문서에 양쪽을 병기하고 현행 배선을 실측 확인된 형태로 확정했다.
>
> **실증 범위(6종·binary guard)**: 금지어 `.md` Write → deny · 이탈 마커 `uaf-allow-legacy:` → 통과 · 근거 없는 완전성 주장 → deny · 근거 마커 + 스윕 범위 명시 → 통과 · **Edit 경로** → deny · 스코프 밖(`.py`·비 md) → 통과. **design guard 2종**: 설계 미완 `src/` → deny · 스코프 밖 `docs/` → 통과.
>
> **변경분**: `.claude/settings.json`(훅 2건 상대경로) · scaffold `dot-claude/settings.json.example`(같은 결함 — 미래 소비 프로젝트 상속 차단) · `hooks-binding.md` §4.5(배선 현행화 + 충돌 병기) · `.claude/CLAUDE.md`(실증 완료 + **훅 배선 경로 규칙** 신설).
> - `uaf-verified:` `CLAUDE_PROJECT_DIR` 를 ripgrep 으로 스윕해 배선 명령 문자열 2건을 찾아 둘 다 교체했다. **검색 범위** = 이 저장소 워킹트리이며, 사용자 전역 설정(`~/.claude/`)·이미 설치된 소비 프로젝트는 그 밖이다. guard 코드 안의 `os.environ.get("CLAUDE_PROJECT_DIR")` 은 `payload["cwd"]` 다음 순위 폴백이라 무관하다(무수정).
>
> **교훈(재사용 가치 높음)**: **훅은 단위 검증으로 작동을 주장할 수 없다.** 스크립트가 옳아도 배선이 죽으면 결과는 "아무것도 막지 않음"이고, 그 실패는 침묵한다. 훅을 새로 배선하거나 경로를 옮기면 **실제 도구 호출로 차단을 확인**한다. 이는 백로그 L(Run Observability)·"파이프 금지·exit 보존" 과 같은 계열 — **관측되지 않는 강제는 강제가 아니다.**

> **🔴 갱신 2026-07-21(5) — yt-stt Contract v4 발행·승인·커밋. 기술 안 8건 확정. 다음 = Projection 7종 개정.**
>
> **직전 1순위였던 "Contract v4 작성" = 종결**(yt-stt `fd21ef3`). 다만 착수 순서를 바꿨다 — 종전 핸드오프 §④는 `v4 작성 → Projection 개정 → 기술 안 7건 승인` 순이었는데, **7건 중 4건(`layer` 값 집합·M4↔M5 순서·프로세스 번호·OQ-1 처분)이 v4 본문에 들어갈 내용을 결정**한다. 그대로 하면 v4를 쓴 뒤 다시 고쳐야 하고 append-only 계약에서 그것은 v5 발행을 뜻한다. **결정을 선행**시켰다.
>
> **원 7건이 8건이 됐다** — 결정 과정에서 2건이 추가로 드러났다.
> - `layer` 필드의 값 집합이 **이미 두 벌**이었다(`table-def.md:138` glossary = 화면OCR/수동자막/문맥/참고자료 · `:179-188` 전사본 = fact/voice/context/residual). 같은 이름이 문서 안에서 다른 집합을 갖고 있었고, FR-7 외부 참고자료의 자리는 어느 쪽에도 없었다.
> - **회귀 기준선의 정답 판정 규칙이 번인 OCR에 묶여 있었다**(`test-plan-cases.md:49·55` TRAP-2·TRAP-8 = "번인 자막 근거로만 확정"). 정답 데이터는 확정돼 있어 불변이지만, 규칙 문면이 새 도구가 재현할 수 없는 경로를 가리키게 된다.
>
> **확정 8건**: D1 `layer` 5값(`fact/voice/context/screen/reference`)·축약 F/S/C/R 폐기·두 벌 통합 · D2 `frames/transition/` 폐지 · D3 `selected_terms`·`selection_note` 폐지+RISK-6 종결+**묶음 사전 경유 금지** · D4 M4 통합(FR-10+OCR)·P3-a/P3-b 분할(P번호 시프트 0) · D5 `facts/burnt-in.md`→`facts/subtitle.md` · D6 OQ-1·OQ-M0-A 종결+**OQ-M4-A** 신설 · D7 RISK-1 부결 문면 보존+반전 레코드 · D8 TRAP-2·8 판정 규칙 교체. 원장 = `yt-stt/V4-DECISIONS.md`(커밋됨).
>
> **CP2 독립 검증에서 결함 3건 검출**(Worker 보고를 근거로 쓰지 않고 산출물 자체로 판정 — Advisor 직접 수정 후 재검증 Pass):
> - **C1** `projections`를 7종에서 8종으로 늘린 오기. `docs/solution-design.md`는 Projection이 아니라 **7종으로 라우팅하는 인덱스**이며 해당 파일 머리말이 스스로 그렇게 선언한다. `design_completeness` CP2 PASS도 7종 기준이라 8로 바꾸면 매니페스트와 계약이 어긋난다. **원인은 Advisor 브리프** — 결정 원장에 "docs 8종"이라 쓴 것이 Worker를 오도했다(파일 수 8 = Projection 7 + 인덱스 1). 원장에 문서 수 주의 블록을 추가해 다음 단계 재발을 막았다.
> - **C2** `assumptionLedger` 신규 가정이 "강의실 촬영이 표준 형태"라고 촬영 형태를 단정했다. yt-stt는 **범용** 도구인데 표본 2로 표준을 못박은 것이고, 같은 계약의 RISK-2가 슬라이드형에서는 판독이 성립함을 인정해 **두 서술이 충돌**한다. 새 구조는 P3-b 게이트가 프레임마다 런타임 판정하므로 가정 자체가 불필요하다 → **런타임 게이트 위임**으로 교체.
> - **C3** `scopeDeviation`이 "[v4] 범위 이탈 0건"이라 선언하는데 실제로는 3건(M0-3 폐기·RISK-11 추가·가정 신설)이었다. **Worker가 완료 보고에서 스스로 올린 것이 이탈의 증거**인데 계약 표면에서는 0건이 됐다 — 책임 있는 자율 (b)의 사유 기록이 지워지는 형태다. 3건 명시로 정정.
>
> **append-only 실증**: v1(17,190B)·v2(12,998B)·v3(23,145B) + `docs/*.md` 8종 = **11파일 SHA256을 작성 전에 고정하고 작성 후 대조**해 불일치 0을 확인했다. `git status` 수정 0건. 검증 수단 = sha256sum 대조·git status·PyYAML 파싱·ripgrep 패턴 스윕 9종(`residual`·`F/S/C/R`·`frames/transition`·`selected_terms`·`selection_note`·`burnt-in`·`OQ-1`·`OQ-M0-A`·`8종`). **한계** = D1~D8의 반영 여부는 확인했으나 서술 내용의 설계적 타당성을 전부 재심사한 것은 아니며, `docs/*.md` 본문은 범위 밖이라 열람하지 않았다.
>
> **교훈(재사용 가치 높음)**: **Advisor 브리프의 부정확이 Worker 결함으로 나타난다.** C1은 Worker의 실수가 아니라 내가 원장에 쓴 "docs 8종"이 만든 것이다. 위임 규율은 "Worker 결과를 검증한다"인데, 검증에서 걸린 것이 **위임자 자신의 입력 오류**일 수 있다. 결함의 귀속을 Worker로 단정하면 같은 브리프로 재위임해 재발한다.
>
> **다음 착수**: **Projection 7종 개정**(선행 감사 = 수정 168건·삭제 23곳·미결정 20건). v4가 발행됐으므로 선행 조건은 해소됐다. 착수 시 체크리스트 = `yt-stt/V4-DECISIONS.md` §Projection 개정 체크리스트(누락되기 쉬운 3종 = OCR 경로 선언 6곳 중복·OQ-M0-A 문장 5곳 복제·RISK-1 배너 4곳 바이트 동일 요구 / 구조 파급 = 역방향 간선·교정 입력이 출력 이후로 이동·`facts/burnt-in.md` 생성 경로 2개·`meta.downmix.measurements` 구조 변경). 최소 read-set = 본 갱신 블록 + `yt-stt/.claude/project-contract/project-contract.v4.md` + `yt-stt/V4-DECISIONS.md`.
>
> **미해소 이월**: UAF 자체 스크립트 인코딩 스윕 · 메모리 중 "강제 필요한데 메모리에만 있는" 항목 재검토 · 감사 미결정 20건 · 백로그 K·L·M·N·O 미착수 · RISK-6은 종결됐으나 RISK-9·10·11 및 신설 OQ-M4-A는 미해소.

> **🔴 갱신 2026-07-21(6) — yt-stt Projection 7종+인덱스 개정 완결·푸시. UAF 위임 규율 검수 → B-2 불변 신설.**
>
> **직전 1순위였던 "Projection 7종 개정" = 종결**(yt-stt `9afe0cb` · master 병합·origin 푸시). Contract v4 파일 무촉(append-only 보존).
>
> **개정 내용**: 파이프라인 P3 → P3-a/P3-b 분할(P4·P5 시프트 0·역간선 1개 명시) · `layer` 5값 단일 정본 통합(같은 필드가 두 벌 값 집합을 갖던 상태 해소·축약 `F/S/C/R` 폐기·`residual`→`reference` 흡수) · OCR 경로는 유지하고 소속만 P1→P3-b 이동(8파일 9곳) · 프레임 게이트 2분류 + `gate_class` 신설 · `frames/transition` 폐지 · `selected_terms`/`selection_note` 폐지 · `facts/burnt-in.md`→`facts/subtitle.md` · `facts/ocr.md`→`screen/ocr.md` · `FR-5b`·`FS-3b` 신설 · TRAP-2·8 판정 규칙 교체 · OQ-1·OQ-M0-A·RISK-6 종결 / **OQ-M4-A·OQ-M1-A 신설(둘 다 미해소)**.
>
> **검증**: CP2 횡단 독립 검증 **1차 FAIL**(위반 3 + 검증 가능성 공백 1) → 지시서 §G 로 공백 해소 → 2차 개정(6문서) → **CP2 재판정 PASS**(위반 0·판정 불가 0) → CP3 승인. 이력 보존 바이트 대조 3블록(RISK-1 강등 부결 문면 604B 동일 · 회귀 기준선 정답지 113건 · M0-1 설계 표).
>
> **산출 원장 2종**(yt-stt 트리): `V4-PROJECTION-CANON.md`(횡단 정본 문면 13종·삭제 식별자 7종·§G 2차 지시) · `V4-PROJECTION-LEDGER.md`(게이트 결정·미결정 17건·이탈 26건·교차 확인 7건).
>
> **★ 핵심 교훈 — 결함 5건이 전부 Advisor 지시서에서 나왔다.** ①§D-1 이 기본값만 주고 **적용 시점**을 안 씀 → 5조가 4갈래로 갈림 ②§A7 이 게이트 *규칙*만 정본화하고 *산출 기록*을 안 함 → 통과 조건은 있는데 판정 수단이 없는 케이스 발생 ③§A11 이 **저장과 전송**을 구분 안 함 → 한 문서가 계약보다 강한 금지를 신설 ④§C 브리프가 `FR-5b` 신설을 병렬 동료에게 못 알림 → 한 문서가 거짓 사실 주장을 보유 ⑤재검증 기준과 §E-2 가 자기모순. **Advisor 자신이 발견한 것은 0건**이며 전부 Worker·Verifier 가 잡았다. 검증 층이 실제로 작동한 실증이자, "결함 귀속을 Worker 로 단정하면 같은 브리프로 재위임해 재발한다"의 실측 사례다.
>
> ## UAF 위임 규율 검수 (사용자 지시)
>
> `uaf-verified:` `.claude/AGENT.md` 전문 + `docs/delegation-protocol.md` 전문 정독, 정본 포인터 4종 실재 확인. **스윕 범위** = 두 문서 + 경로 실재 확인이며 `uahf/specs/02·07` 본문은 미열람.
>
> **규칙이 실제로 틀린 것 = B-0 하나.** `.claude/AGENT.md` 안에서 **"작업 분해"가 Advisor·Planner 두 역할에 이중 귀속**돼 있다(§Roles Advisor "계획·작업 분해·위임·검증·승인에 집중" / §Roles Planner "책임은 계획, 작업 분해, Wave 설계"). `초안=Planner / 채택=Advisor` 로 읽으면 해소되나 §Roles 문면이 그렇게 말하지 않는다. → **해소(아래 갱신 (7))**.
>
> **나머지는 규칙이 없는 것**이고 B-1·B-2·B-3 은 한 뿌리다 — **위임·보고 층만 강제 장치 없이 문서로 운영**된다(이진 원칙=PreToolUse 훅 / 설계완성도=엔진 게이트+훅 / 위임=강제 0).
> - **B-1 미수정** — INV-6 반환 규율(§2.4)이 4단계 절차까지 정의하는데 이번 세션 브리프에 `done` 이 검증 가능 목록으로 없었음에도 **5조 중 반환 0건(5/5 미작동)**.
> - **B-3 미수정** — "Run 조율 우회 금지" 불변이 **구현에만** 걸린다. 설계 층은 메커니즘이 실재하는데(`solution_design_resolve.py`·`solution-design-data/` 실재 확인) 우회 금지 불변이 없어, 오늘 8문서·5 병렬 Worker 를 **원장 0건**으로 돌린 것이 규칙 위반이 아니다.
> - **B-4 미수정** — 병렬 Wave R1~R4 가 전부 **쓰기** 경계라 **읽은 스냅샷이 낡는 위험**이 없다. 위 결함 ④가 이것의 실증이다(조 4 의 정당한 이탈이 조 3 의 전제를 무너뜨렸는데 알릴 채널이 없었다).
> - **B-5** — "Worker 결함이 Advisor 브리프에서 온다"가 메모리에만 있고 AGENT.md·delegation-protocol 어디에도 없다. → **해소(아래 갱신 (7))**.
>
> ## B-2 수정 (사용자 승인 · 본 커밋)
>
> **`.claude/AGENT.md` §Invariants 에 「위임 산출 유실 금지」 신설**(도구 중립) — 위임 보고의 미결·이탈·판정 근거를 회수 채널에만 두지 않고 **회수 직후** 산출물로 승격한다. **관측 경로 유실 금지의 판단 측 대응물**로 위치시켰다(그쪽=실행 결과 종료코드·실패신호 / 이쪽=판단 결과). 부수 규칙 셋 = 집계는 내용을 대체하지 않는다(개수만 남으면 미해소가 아무것도 막지 못한다) · 승격 시점은 회수 직후다(마감까지 미루면 기억 의존이고 기억은 세션 경계를 못 넘는다) · 승격 대상은 다음 사이클이 소비할 것으로 한정.
>
> **`docs/delegation-protocol.md` §2.7 신설 + §3.2 보강 + §4 포인터 2행.** 승격 대상·시점·위치·등급(**evidence**)·원장 구성 5항·금지(개수 갈음). 수명·삭제·인용은 `artifact-lifecycle-policy.md` §2·§3·§5 참조만 하고 재정의 0. **절 번호를 밀지 않는 배치**(에스컬레이션 §2.6 보존·신설을 §2.7)로 외부 참조 파장 0 — `v1.0-user-guide.md:70` 의 `§2.5·§2.6` 인용이 그대로 유효하다.
>
> **실증 근거**: 이번 세션에서 감사 미결정 20건이 집계 숫자만 남기고 소실됐고(선행 세션), 오늘 5조 보고도 Advisor 가 **기억해서 손으로** 원장을 쓰지 않았으면 같은 운명이었다. 그 기억 의존이 결함이다.
>
> **다음 착수 후보**: (가) yt-stt **M2**(선결 = M2 확인 항목에 `ko` 트랙 미수신 여부 추가 · `OQ-M4-A`·`OQ-M1-A` 는 미해소로 하류를 막는다) · (나) UAF **B-0**(문면 모순·수정 한 문단) · (다) UAF **B-1/B-4**(위임 필드 강제·병렬 동시편집 채널) · (라) 백로그 K·L·M·N·O 미착수.
>
> **미해소 이월**: B-0·B-1·B-3·B-4·B-5 · UAF 자체 스크립트 인코딩 스윕 · 감사 미결정 20건은 **복원 불가**(집계만 잔존) · `OQ-M1-A` 의 계약 등재 보류(v5 발행 필요 여부는 미결) · RISK-9·10·11.

> **🔴 갱신 2026-07-21(7) — B-0·B-5 해소. 위임 규율 6건 중 3건 마감.**
>
> **B-0(규칙이 실제로 틀린 유일 건) 해소** — `.claude/AGENT.md` §Roles Advisor.
> - **"작업 분해"의 소유 구분**을 문면으로 못박았다: 분해의 **초안 작성 = Planner** / 분해의 **채택·확정 = Advisor**. 같은 낱말이 두 역할 §Roles에 등장하되 다른 것을 가리킨다는 사실이 종전에는 어디에도 없었고, Planner 경계·§Delegation 중간 축이 **함의**만 하고 있었다.
> - Advisor 경계에 **판별 이진 술어** 신설: **병렬 집합(동시 위임 2건 이상)** 을 만드는 분해는 Planner 초안을 받아 채택 · **단일 위임**의 분해는 Advisor 직접 확정. 기준은 **동시 위임 건수**이며 규모 감각이 아니다(강도 부사 금지 규율 준수). 근거 = 병렬 집합에서는 위임 문면의 결함이 여러 산출물에 동시 착지해 갈라지고, 그 발산은 문서 단위 검증이 구조적으로 못 본다(이번 세션 실측).
>
> **B-5(브리프 결함 귀속) 해소** — 불변 + 운용 2면.
> - `.claude/AGENT.md` §Invariants **「결함 귀속 단정 금지」** 신설. **Verify Everything을 위임자 자신에게 적용**한 것으로 위치시켰다 — 완료 보고를 그대로 신뢰하지 않는다면 그 보고를 낳은 위임도 그대로 신뢰하지 않는다. 부수 규칙 셋 = **재위임 전에 위임 문면부터 점검**(산출물보다 위임을 먼저 고친다) · **Verifier는 귀속 후보를 함께 보고**(비워 두면 기본 귀속이 관성 적용) · **검사 도구의 출력도 결함원**(도구 출력은 좌표이지 판정이 아니다).
> - `docs/verification-checklist.md` **§5.6 결함 귀속 판정** 신설(게이트 C Fail 후·재작업 지시 **전**). 점검 5항 + 판정 규칙 — 귀속이 **위임**이면 문면 보완이 재작업에 선행하고, 귀속이 **도구**이면 위반 항목을 철회하고 도구를 고친다. §5.5 Fail 처리 라인을 §5.6 경유로 배선.
> - 외부 §참조 파장 0(verification-checklist 절 참조는 외부에 없음·실측).
>
> **근거는 전부 이번 세션 실측이다** — 지시서 결함 5건(전부 Advisor 귀속·Advisor 자신이 발견한 것 0건) · Verifier가 4건 모두를 지시서 귀속으로 판정 · Advisor 체커 정규식이 **실재 문면 7파일 9곳을 0 적중으로 오보**(그대로 믿었으면 없는 결함을 올릴 뻔했다).
>
> **위임 규율 6건 현황**: B-0 해소 · B-2 해소 · B-5 해소 / **B-1·B-3·B-4 미해소**.
> - **B-1** INV-6 반환 규율 강제 0(5/5 미작동). 착수 시 유의 = PreToolUse로는 안 잡힌다(위임은 도구 호출이 아니다) → 수임 Agent 정의(`.claude/agents/*.md`)에 착수 전 점검을 박는 쪽이 현실적.
> - **B-3** 설계 층 원장 우회 금지 불변 부재. 거버넌스 무게가 크다 — 불변 신설은 이번 세션 방식(Advisor 직접 병렬 위임) 자체를 금지하게 된다.
> - **B-4** 병렬 Wave R1~R4가 전부 쓰기 경계라 읽은 스냅샷이 낡는 위험·이탈 전파 채널이 없다. **B-0 의 새 규율이 이것을 부분적으로 덮는다**(병렬 분해에 Planner 초안이 개입하면 이탈 지점이 초안 단계에서 드러날 확률이 오른다). 다만 실행 중 발생하는 이탈은 여전히 미해결이다.
>
> 상세 = 메모리 `uaf-delegation-enforcement-gap`.

> **🔴 갱신 2026-07-21(8) — M2 착수 시도가 차단성 결함을 드러냄. M1 결함 3차 수정 run 완주. UAF 백로그 P 신설.**
>
> **착수 목표는 yt-stt M2 였고, 실제 성과는 M2 를 막던 결함을 찾은 것이다.** 그대로 M2 에 들어갔으면 **입력이 0 인 층**을 짓고, 자동 자막으로 팩트가 채워진 것처럼 보이는 산출물을 얻었을 것이다.
>
> ## ① 핸드오프 기록 2건 정정
>
> - **“OQ-M4-A·OQ-M1-A 는 미해소로 하류를 막는다”(갱신 (7) §다음 착수 후보) 는 M2 에 대해 부정확하다.** `project-plan.md:274-275` 실측 — OQ-M4-A 의 닫는 시점은 **M4-b**, OQ-M1-A 의 닫는 시점은 **M2** 다. 전자는 M2 비차단, 후자는 M2 가 닫는 주체다. 둘 다 M2 진입을 막지 않는다.
> - **비차단 관찰 (a)(갱신 (2)) 의 등급이 틀렸다.** “`ko-orig` 의 base 가 `ko` 라 `ko` 트랙은 받지 않는다 · 자동자막=4차 잔여·참고 등급이라 비치명”으로 기록됐으나, 실제 범위는 자동 `ko` 트랙 1개가 아니라 **수동 자막 전량 미취득**이었다. 수동 자막은 v4 에서 1차 팩트 층의 유일한 입력이다 → **비차단이 아니라 차단.**
>
> ## ② 대상 채널에 수동 자막이 없다 (표본 스크리닝 실측)
>
> `uaf-verified:` 채널 `@wisa-tv`(UCWxpGNtoa5YTFnUoOqbhXog) 영상 163건 목록을 취득하고 그중 **12건**을 `yt-dlp --list-subs` 실호출로 판정했다. **검색 범위 = 12/163 이며 전수가 아니다.** 선정은 사전확률 최상위 두 갈래(영어 제목 8 + 한국어 장편 4)다.
> - **12/12 `auto-only` · 수동 자막 0.** 영어 제목은 유튜브 **자동 번역 제목**이었고 다국어 캡션 등록 신호가 아니었다(Advisor 가설 오류).
> - **대조군 TED 3건 중 2건 MANUAL**(`ar,en,es` / `ar,en,ro,es`) — “수동 자막 0”이 도구 결함이 아니라 채널의 실제 속성임이 분리 확인됐다.
> - `uaf-assumed:` 잔여 151건에서 수동 자막이 나올 기대치는 낮다고 **추정**한다. 확인한 것이 아니다.
> - **함의**: `project-plan.md:63` 은 “공집합은 예외가 아니라 정상 입력”이라 썼는데, 실측은 그보다 강하다 — **대상 도메인에서 1차 팩트 층은 상시 공집합에 가깝다.** 사용자 결정 = **2트랙 표본**(TED 로 수동 자막 경로 실증 · 위사로 공집합 경로 실증).
>
> ## ③ 차단성 결함 — 수동 자막 전량 미취득
>
> `uaf-verified:` TED 영상 1건의 `--list-subs` 실출력(픽스처 `fixtures/yt-dlp.list-subs._JlQOnnEwxc.txt` 636행) + `acquisition.py` 자막 선택 경로 정독.
> - **`-orig` 접미 표기는 자동 자막 섹션에만 나타난다. 수동 자막 코드는 base 뿐이다.**
> - `_detect_origin_lang` 이 `-orig` 붙은 **코드 자체**(`en-orig`)를 원어로 반환 → target `{en-orig, ko}` → manual `{ar,en,es}` 와 **문자열 완전 일치** 교집합이 **공집합** → manual 다운로드 호출 0건.
> - **원어 판별이 성공하는 전 시나리오에서 재현**(요청≠원어 · 요청=원어 · 한국어 수동 자막 보유 영상 모두 0건).
> - **왜 안 드러났나** — 표본 2영상이 수동 자막을 보유하지 않아 이 경로에 도달한 적이 없다. M1 CP2·CP3·Advisor 독립 실증 6/6 이 전부 통과했다. **공집합이 결함을 가렸다.**
>
> **귀속 = 명세**(B-5 절차 적용). `M1-DEFECTS-2.md:154` 의 **사용자 확정 규칙**이 원어를 *언어*가 아니라 **표기 문자열**로 정의했고 코드는 그 문면을 정확히 구현했다. 코드부터 고치면 같은 규칙으로 재발한다 → **F3′ 정정을 코드 수정에 선행**시켰다.
>
> **F3′(사용자 확정 2026-07-21)** — `-orig` 는 원어 판별 **신호**일 뿐 다운로드 대상 코드가 아니다(접미 제거한 base 가 원어 언어) · 대상은 **언어 집합** `L = {원어 언어, 요청 언어}` · **수동·자동 섹션별로 base 정규화 매칭**(신설) · 언어 코드 하드코딩 금지와 판별 결과 전량 보존은 존치. 정본 = `yt-stt/M1-DEFECTS-3.md` §3.
>
> ## ④ 수정 run `impl-yt-stt-m1fix3` — 완주
>
> 3 단위(implementation 2 + milestone 1) **전건 Passed · rework 0 · escalation 0**(원장의 `escalated` 1건은 사용자 게이트 제기이며 실패가 아니다). 사용자 결정 게이트는 **actor=human·simulated=false** 로 해소했다 — Advisor 가 확정 권위를 대행하지 않았다.
>
> **Advisor 독립 실증 11/11 PASS**(엔진 AC 미호출·별도 작성·스크래치패드 격리). 엔진 AC 세트에 **없는 3항**을 포함한다 — A8(요청 언어 == 원어일 때도 manual 취득) · A9(판별 결과 전량 보존) · A10(로컬 자산 스킵 불변).
> - **음성 대조(negative control) 실시** — 원 로직을 재구성해 `manual_langs == []` 를 재현하고 신 로직에서 `['en']` 이 나옴을 대조했다. **검증기가 통과했다는 사실 자체가 판별력의 증거가 되게** 만든 것이며, 이것이 없으면 내 검증기도 “구문·존재만 보는 AC”와 구분되지 않는다.
> - 회귀 전건 PASS(1차·2차) — 2차는 한글 경로 실자산 구동이며 mono -54.8 / left -22.0 / right -21.8 → `right` 로 **M0 실측과 정확 일치**.
> - 보호 경계 무촉(mtime 대조) — `.claude/**` · `docs/*.md` · `fixtures/` 기존 2건 · `M1-DEFECTS.md` · `M1-DEFECTS-2.md`.
> - **CP3 = Advisor Pass.** 엔진이 `actor=Advisor` 로 자동 Pass 를 기록하나 그것은 엔진의 판단이며, 위 독립 근거로 내가 별도 판정했다.
>
> ## ⑤ UAF 하네스 — 백로그 P 신설 (실측 크래시)
>
> **`orchestrate_project.py` 가 긴 `--phase` 에 크래시한다.** seed 노드 id = `"impl-plan-" + _slug(phase_scope)` 가 **그대로 파일명**이 되는데(`orchestrate_project.py:122`) `_slug` 에 길이 상한이 없어 Windows 경로 한계에서 `OSError: [Errno 22]` 로 런처가 죽는다. 성격은 백로그 L(관측) 계열이 아니라 **입력 검증 부재**다.
> - 원장 오염 0 — 크래시가 게이트·원장 이전 단계라 `config.json`·`gate_policy.json`·`graph.json` 3건만 생성됐고 events/revisions/artifacts 는 0 이었다(실측 후 제거·재발화).
> - **관측 함정 재확인**: 래퍼의 `echo EXIT=$?` 덕에 잡혔다. 하네스에는 **exit 0** 으로 보고됐고 실제 엔진 종료 코드는 **1** 이었다. 갱신 (2) 의 “파이프 금지·exit 보존” 규율이 이번에도 적중했다.
> - **부수 실측**: 엔진 stdout 이 버퍼링돼 실행 중 로그가 비어 있다 → 이 run 에서 `tail -F` Monitor 는 이벤트를 내지 못했다. 다단위 순차 실행이라 Monitor 를 걸었으나 **이 엔진에 한해 중복**이다.
>
> ## ⑥ 다음 착수
>
> 1. **[1순위] 2트랙 표본 수집** — TED(수동 자막 보유·경로 실증) + 위사 채널 추가분(공집합 경로 + **OQ-M1-A** dB 분포). `run_m1(url, bundle, title, out_root)` 이 진입점이다. `requested_lang` 은 `run_m1` 시그니처에 노출돼 있지 않다(기본 `ko`) — TED 표본에서 이 경계를 확인할 것.
> 2. **M2 구현** — 1차 팩트 층. 확정 전사 경로와 공집합 기록 경로를 **둘 다** 실행되게 한다.
> 3. **UAF 백로그 P** — `_slug` 길이 절단 또는 phase 길이 검증.
> 4. 최소 read-set = 본 갱신 블록 + `yt-stt/M1-DEFECTS-3.md` + `yt-stt/docs/project-plan.md` §M2.
>
> **미해소 이월**: 위임 규율 B-1·B-3·B-4 · 백로그 K·L·M·N·O·**P** 미착수 · UAF 자체 스크립트 인코딩 스윕 · 감사 미결정 20건(복원 불가) · RISK-9·10·11 · OQ-M4-A · **OQ-M1-A**(M2 에서 닫는다) · 채널 잔여 151건 수동 자막 유무 미확인.

> **🔴 갱신 2026-07-21(9) — 실경로 수집 1회가 결함 4차를 드러냄. 오프라인 AC 12/12 위에 남아 있던 층.**
>
> 3차 수정 직후 TED 표본을 **실경로로 1회 수집**한 결과, 오프라인 AC 가 전부 통과한 상태에서 **또 하나의 차단성 결함**이 나왔다. 백로그 O 의 명제("몽키패치로 내 함수를 실호출하는 것과 외부 프로세스의 실제 출력을 먹이는 것은 다른 층위")가 한 단계 더 확장된다 — **실제로 파일이 떨어지는 것**은 또 다른 층이다.
>
> ## ① 결함 4차 — 등급 역전 + 부분 성공 기록 유실
>
> `uaf-verified:` TED `_JlQOnnEwxc` 실경로 수집 1회 + 재실행 1회 + 산출 폴더·`meta.json`·`subs/` 직접 판독 + `out/*/*/meta.json` **3건 전수** 대조. **검색 범위** = 이 저장소 `out/` 트리와 `acquisition.py` 자막 다운로드 경로다.
> - `manual.en.vtt` **20,920B 취득 성공**(사람이 쓴 자막 — 3차 수정이 실경로에서 작동함이 확인된 지점). 그 뒤 auto(`ko`)가 **429**를 맞자 예외가 전파돼 `m1_ingest=failed` · **`meta.subtitles = null`**.
> - **자기봉인**: 재실행하면 `_subtitle_check_complete` 가 디스크 파일 존재로 참이 되어 자막 단계를 건너뛴다(실측 — `failed=False` · **yt-dlp 호출 0회**). `meta.subtitles` 는 **영영 null** 이다. 일시적 실패가 아니라 **기록과 실물의 영구 불일치**이며, M2 는 이 meta 를 읽고 **1차 팩트 공집합**이라는 틀린 결론에 도달한다.
> - Contract v4 의 **R1 서열**(`자막 팩트 > 문맥 > 화면 > 참고자료`)과 **품질 비대칭**(`오교정 0 이 누락보다 먼저`)에 정면으로 어긋난다.
>
> **귀속 = 코드.** 명세(F3·F3′)는 다운로드 **대상 선택**만 정의했고 **실패 처리 등급**은 정의한 적이 없다 — 규칙이 없는 자리를 구현이 일괄 전파로 채웠다. **3차와 정확히 대비된다**(3차 = 명세가 코드를 잘못 이끔 / 4차 = 명세가 침묵한 자리를 코드가 임의로 채움). 귀속을 기본값으로 두지 않고 매번 판정해야 하는 이유의 실례다.
>
> **확정 규칙(§3)**: 수동 실패는 차단 · 수동 부재는 정상 · 자동 실패는 비차단이되 사유 기록 · **차단 시에도 부분 결과를 먼저 기록**.
>
> ## ② 수정안 설계에서 잡은 회귀 함정 (재사용 가치 높음)
>
> 완결 판정 기준을 `meta.subtitles` 로 바꾸는 것이 가장 자연스러운 수정처럼 보인다. **그 수정은 2차 게이트를 깬다.** `uaf-verified:` `out/*/*/meta.json` 3건 전수 판독 결과 **전부 `subtitles = null`** 이고, 2차 회귀 게이트가 쓰는 `out/m1-live/…[r9Hs79sqfeI]` 는 `subtitleKinds` 도 null 이라 **디스크 파일 존재에만 의존해 통과**하고 있다. 기준을 바꾸면 그 자산이 재수집 대상이 되어 "yt-dlp 호출 0회" AC 가 깨진다(FR-11(c) 429 방지 회귀).
> → **판정 기준이 아니라 기록 측만** 고치도록 명세를 좁혔다. **브리프를 쓰기 전에 회귀를 실측한 것이 결정적이었다** — 안 했으면 그럴듯한 수정이 게이트를 깨고 들어갔다.
>
> ## ③ run `impl-yt-stt-m1fix4` — 완주
>
> 3단위 Passed · rework 0. 사용자 결정 게이트는 **actor=human** 으로 해소.
> **Advisor 독립 실증 12/12 PASS** — **엔진 AC 가 덮지 않는 4축** 포함: B7 수동·자동 **동시 실패** · B8 **기존 반환 키 4종 하위호환**(§4 가 "소비처가 있다"고 요구하는데 AC 부재) · B9 **429 문면 보존**(진단 가능성) · B11 3차 회귀. **음성 대조** 재실시(원 로직 예외 전파 재현 / 신 로직 미전파).
> 게이트 1·2·3·4차 **전건 exit 0** · §3.1 회귀 지점 `yt-dlp 호출 실측 0회`. 불가침 4파일(`pipeline_m1.py`·`meta_schema.py`·`storage.py`·`downmix_gate.py`) git 기준 무수정.
>
> ## ④ 부수 실측
>
> - **OQ-M1-A 표본 +1**: TED(정상 스테레오) mono **-21.1** / L -21.0 / R -21.0 → `left`. 위사 `r9Hs79sqfeI`(위상 반전) mono -54.8 / L -22.0 / R -21.8 과 대조된다. **상쇄 사례는 여전히 1건**이라 임계를 닫지 않는다.
> - `auto.en.vtt` 와 `auto.en-orig.vtt` 가 **바이트 동일**(실측). F3′ 3항의 base 매칭이 같은 트랙을 두 번 받는다 — 요청 1회를 줄이면 429 위험이 줄지만 **F3′ 는 사용자 확정 규칙이라 이 run 에서 바꾸지 않았다.** 사용자 결정 대상.
> - 갱신 (2) 의 비차단 관찰 (a)("두 트랙은 다를 수 있음")는 **이 표본에서 거짓**이다(측정된 사실).
> - **429 의 일부 책임은 Advisor 에게 있다** — 표본 스크리닝으로 `--list-subs` 를 15회 이상 호출했다. 등급 역전 결함은 429 원인과 무관하게 성립한다.
>
> ## ⑤ 다음 착수 (갱신 (8) ⑥을 대체)
>
> 1. **[1순위] 표본 수집 재개** — 429 냉각 후. TED 추가 1건 + 위사 추가분(공집합 경로 + OQ-M1-A dB 분포). **TED 표본의 `meta.subtitles = null` 복구는 별도 조치**다(4차 수정은 새 수집만 고치며 소급 정정하지 않는다 — `M1-DEFECTS-4.md` §7).
> 2. **M2 구현** — 확정 전사 경로와 공집합 기록 경로를 둘 다 실행되게 한다.
> 3. **F3′ 중복 다운로드** 사용자 결정 — `-orig` 와 base 가 동일 트랙일 때 하나만 받을 것인가.
> 4. **UAF 백로그 P** — `_slug` 길이 절단.
> 5. 최소 read-set = 본 갱신 블록 + 갱신 (8) + `yt-stt/M1-DEFECTS-4.md`.

> **🔴 갱신 2026-07-23(10) — 2트랙 표본 수집 완주 · fix-4 실경로 검증(실제 429 자연 발생) · JS 런타임 환경 차단 발견+워크어라운드. 1순위 종결.**
>
> **직전 1순위 "표본 수집 재개" = 종결.** `uaf-verified:` git status — 보호 경계(scripts/·fixtures/·docs/·.claude/) 변경 없음, out/m2-samples/ 에 신규 폴더 2개(TED·위사)만. **검색 범위** = yt-stt working tree. yt-stt 커밋 미실시(신규 out/ 미커밋).
>
> ## ① fix-4(등급 역전) 실경로 검증 — 실제 429 자연 발생
> `uaf-verified:` TED `kz-I5zIGbj4`("Why I Love My Bad Days"·수동 자막 사전 확인) 실경로 수집 + 저장 `meta.json` 독립 판독(runner 요약을 근거로 쓰지 않고 디스크 아티팩트 직접). **검색 범위** = 이 표본의 out/ meta·subs.
> - 수동 `manual.en.vtt` 7,740B 취득 성공(실제 사람 캡션 육안 확인 — "I was one month out from my Olympic race in Rio") → `meta.subtitles.downloaded.manual.en` 기록.
> - 자동(`ko`)이 실제 HTTP 429. fix-4 등급 처리로 비차단 → `autoFailure` 에 429 사유 기록·예외 미전파·`subtitles ≠ null`·`failed=false`·acq/ingest/downmix 전부 ok.
> - fix-4 이전 로직이라면 자기봉인(auto 429 예외 전파 → 취득한 manual 폐기 → subtitles=null). **오프라인 AC 12/12 위에 남아있던 층을 실제 429 가 밟아 검증했다** — "실경로 1회가 층을 드러낸다" 교훈 재적중(이번엔 코드가 옳았고 실제 429 가 이를 입증).
>
> ## ② 위사 공집합 경로 검증
> `uaf-verified:` 위사 `YY_mbFY7y4E`(채널 @wisa-tv·온도메인 제휴마케팅) 수집 + meta 판독. `subtitleKinds.manual=[]`·`downloaded.manual={}`·`failed=false` — 수동 자막 없음을 정상 입력으로 완주. auto(ko) 성공(autoFailure=None).
>
> ## ③ JS 런타임 환경 차단 (신규·중요) — yt-stt 제품 함의
> `uaf-verified:` 첫 TED 수집이 429 아닌 403 으로 실패: `No supported JavaScript runtime ... deno` + `HTTP Error 403 Forbidden`. yt-dlp 2026.07.04 + YouTube JS 챌린지 강화(2일 전 수집은 성공했음)로 **미디어(video/audio) 다운로드가 deno/node 런타임 없이 403**. `--list-subs`(메타)는 통과하나 포맷 취득 차단.
> - **해소**: node v24.15.0 존재 → `--js-runtimes node` 직접 테스트로 audio 3.9MB 취득 성공 확증 → yt-dlp 설정 파일(`~/.config/yt-dlp/config` · `%APPDATA%\yt-dlp\config` · **ASCII-only** — yt-dlp 가 설정을 cp949 로 읽어 한글 주석이 파싱 에러를 냈다) 에 `--js-runtimes node` 배치 → `acquisition.py` 무수정으로 내부 호출 전부 적용(`[debug] JS runtimes: node-24.15.0` 로딩 확인).
> - **⚠ 환경 뮤테이션**: 위 yt-dlp 설정은 이 머신의 모든 yt-dlp 호출에 적용된다(되돌리기 = 파일 삭제). 세션 워크어라운드이며 프로젝트 전제로 승격할지는 미결(사용자 결정).
> - **⚠ 제품 함의(백로그·신규 결함/전제)**: `acquisition.py` 가 `--js-runtimes` 를 붙이지 않아 **deno 없는 환경에서 yt-stt 미디어 취득이 깨진다**(yt-dlp 기본 활성 런타임 = deno 뿐). 대응 = 환경 전제 문서화 or acquisition.py 런타임 처리. 이번 세션은 워크어라운드로 수집만 진행하고 코드 반영은 다음 사이클로 이연(사유: 수집이 1순위·사용자 결정 대상).
>
> ## ④ 부수 관찰
> - **F3′ 중복 실물 확인**: TED `auto.en.vtt`·`auto.en-orig.vtt` 42,029B 바이트 동일 · 위사 `auto.ko.vtt`·`auto.ko-orig.vtt` 25,933B 바이트 동일. dedup(fix-5) 값 재확인.
> - **F3′ dedup 은 fix-3 규칙 개정임이 확인됨(백로그)**: `uaf-verified:` `verify_defects3_acquisition.py` AC-5(L99-100)·AC-6(L126-127)이 en+en-orig·ko+ko-orig 를 둘 다 요청함을 단언 → dedup 시 그 AC revise 필수. `M1-DEFECTS-4.md §6.8` 무수정 경계도 뒤집힌다. 사용자 결정 = 수집 먼저·dedup 나중(별도 fix-5·verify_defects3 AC 개정 동반).
> - **prefix 매칭 quirk(비차단·잠복)**: 위사 `downloaded.auto` 가 `ko`·`ko-orig` 두 키 모두 `auto.ko-orig.vtt` 를 가리킨다(`_download_subtitle_kind` 의 `startswith("auto.ko")` 가 `auto.ko-orig` 도 포착). 두 파일 바이트 동일이라 무해하나, 두 코드가 달랐다면 오배선. dedup 시 소멸.
> - **auto 부분성공 기록 갭(비차단)**: TED `auto.en`·`auto.en-orig` 파일은 디스크에 있으나 ko 429 로 auto 호출이 실패 반환돼 `downloaded.auto={}`. 참고 등급이라 비차단.
> - **OQ-M1-A 표본 +2**: TED mono -19.8 / L·R -19.6 · 위사 mono -14.6 / L·R -14.5 — 둘 다 정상 스테레오. 위상 상쇄 사례는 위사 `r9Hs79sqfeI`(-54.8) 1건뿐이라 임계 미해소 유지.
> - **TED 기존 표본 `_JlQOnnEwxc` meta 복구 미실시**(별도 조치·`verify_defects4_acquisition.py` AC 픽스처라 무촉 유지).
>
> ## ⑤ 다음 착수 (갱신 (9) ⑤ 대체) — M2 는 새 세션에서(사용자 지시 2026-07-23 "다음 작업 새 세션에서")
> **M2 dispatch-ready 계획(스코핑 완료·결정 2건 확정).** 새 세션 절차: (i) 아래 결정 2건을 `yt-stt/M2-BRIEF.md` 로 물리화 → (ii) 엔진 dispatch `python orchestration/adapters/claude/orchestrate_project.py "C:/my-claude-project/yt-stt" --phase "M2 1차 팩트 층 (정본 명세 = M2-BRIEF.md)" --mode incremental --run-id impl-yt-stt-m2` (로그 리다이렉트 + `echo ENGINE_EXIT=$?`) → (iii) 사용자 구조 게이트에서 impl-plan 검증 → CP2 → milestone CP3.
> - **M2 = 1차 팩트 층**: 경로 (a) 수동 자막 有 → `facts/subtitle.md`(확정 전사·layer=`fact`)+확정 용어 하류 · 경로 (b) 無 → 공집합 명시 기록("확인 안 함" ↔ "팩트 없음" 구분·빈 `facts/` 정상). 입력 = `meta.json.subtitleKinds.manual` + `subs/manual.*`. **OCR 은 M2 범위 아님**(v4 D1/D2/D4/D5 로 M4/P3-b 이동). RISK-6 종결(D3·선별 게이트 없음). 앵커 = FR-3·FS-3·table-def §2.1·§4.3.
> - **결정 1(사용자 확정 2026-07-23)**: M2 = 팩트 층만 출하 · **OQ-M1-A(무음 임계) 열어둔다** — 위상 상쇄 표본이 `r9Hs79sqfeI`(-54.8) 1건뿐이라 임계 미확정(정상 4건: TED -19.6·위사 -14.5·`_JlQOnnEwxc` -21·`rijkvfvJe2U`). 합격선 숫자 발명 금지 정책 준수. 무음 임계는 M1 다운믹스 게이트 소관이라 팩트 층과 별개.
> - **결정 2(사용자 확정 2026-07-23·설계 공백 보충)**: 다중 수동 자막 언어 시 **팩트 = 원어(음성 언어) 수동 자막**. 번역 자막은 전사가 아니라 팩트 아님. **원어 수동 자막이 없으면 팩트 층 공집합 취급.** M1 이 원어를 auto `-orig` 로 판별하므로 구현 가능(우리 TED 표본은 원어 en·수동 en 으로 깔끔). 이 규칙은 문서 공백 보충이므로 canon(Contract v5/Projection) 반영 여부는 별도 판단(백로그).
> - **완결 판정** = FR-3 (a)(b)(c) + project-plan 부록 A 완결 원칙(오교정 0·타임스탬프 불가침·원본 불변·층 출처 명시·침묵 성공 금지). FS-3 미결 없음.
> - **보호 경계**(M2 impl 읽기 전용): Contract v1~v4(append-only)·docs Projection 7종+solution-design·scripts/m1·scripts/m0·fixtures·tests/baseline. 데이터 주의 = `meta.downmix.measurements` 는 `{level_db, measured}` 객체(스칼라 아님).
> - **⚠ 워크어라운드 유지(삭제 금지·사용자 지시 2026-07-23 "우회는 놔두고")**: yt-dlp 설정 `~/.config/yt-dlp/config`·`%APPDATA%\yt-dlp\config` 의 `--js-runtimes node`(ASCII-only). **삭제하면 향후 유튜브 수집이 다시 403**. M2 자체는 디스크 표본을 소비해 새 다운로드가 불필요하나 워크어라운드는 유지한다. 제품 반영(코드/전제)은 백로그.
> - **최소 read-set**(M2 세션) = 본 갱신 블록 + `yt-stt/docs/functional-spec.md` FS-3 · `requirements-def.md` FR-3 · `table-def.md` §2.1 + 메모리 `uaf-product-yt-stt`.
>
> **동시 백로그**(M2 후보): JS 런타임 제품 반영(전제 문서화 or acquisition.py 런타임 처리) · F3′ dedup fix-5(규칙 개정 + verify_defects3 AC-5/6 revise + `M1-DEFECTS-4.md §6.8` 경계 갱신) · UAF 백로그 P(`_slug` 길이 절단) · TED 기존 표본 `_JlQOnnEwxc` meta 복구.

> **🔴 갱신 2026-07-23(11) — yt-stt M2(1차 팩트 층) 구현 완료·커밋 `5013bad`. CP2 v1 REJECT→v2 실증. 세션 마무리.**
>
> **직전 1순위 "M2 구현" = 종결**(yt-stt master `5013bad`·9파일). 엔진 orchestration run `impl-yt-stt-m2` — proposal+4단위(fact_selection·subtitle_transcript·pipeline·milestone). `uaf-verified:` run_dir STATES 판독 = 5단위 Passed·resume 로그 `ENGINE_EXIT=0` 실판독(래퍼 echo 아님). **검색 범위** = run_dir events/graph.json + 산출 파일 + git.
>
> ## ① CP2 v1 REJECT — impl-plan이 fix-4 픽스처에 쓰려 함 (귀속=브리프·B-5)
> 1차 impl-plan CP2 독립검증에서 차단성 결함: task3이 **committed fix-4 픽스처 `_JlQOnnEwxc` 폴더에 `facts/`를 쓰는** 계획. `uaf-verified:` `git ls-files`=그 폴더 4파일 추적·`verify_defects4_acquisition.py:28-29`가 §5 고정입력으로 참조. **검색 범위** = git ls-files + verify_defects4 grep. **귀속=내 브리프** — v1 §2가 픽스처를 표본으로 열거+§4(b) "구현조 판정" 허용 → Planner 오도. 부수: **disk-fallback 로직도 브리프 발명**(두 클린 표본 미사용·fix-4가 self-sealing을 이미 고쳐 production에 `subtitles=null` 없음 = 죽은 코드).
> → **사용자 결정 REJECT + 브리프 수정.** 재위임 전 브리프부터 고침(B-5 절차). 브리프 v2: `_JlQOnnEwxc` 표본 제외(read-only·무촉)·disk-fallback 제거·시그니처 `select_fact_source(meta)` 1-arg. 개정 사유는 브리프 개정이력에 원장화(run_dir는 재-dispatch 시 wipe되므로).
>
> ## ② 재proposal → CP2 PASS + 자가 회귀가드
> v2 impl-plan CP2 재검증: `_JlQOnnEwxc` 언급이 금지/부정단언 문맥뿐(스윕: impl-plan.json 전문 grep 8회)·disk-fallback 제거·시그니처 교차일치(task3의 `run_m2`가 1-arg 호출)·음성대조 보존. **Planner가 자발적으로 회귀가드 추가** — task3 `assert not exists([_JlQOnnEwxc]/facts)` + task4 판정항목7(픽스처 미침범). → 사용자 승인(`actor=human·simulated=false` — 확정 권위 대행 안 함).
>
> ## ③ Advisor 독립 CP3 — 17/17 PASS
> `uaf-verified:` 엔진 auto-Pass·gate_check_m2(자기출제) 미사용·별도 스크립트로 실표본+적대케이스 판정. **검색 범위** = out/m2-samples 2표본 + fact_selection/pipeline 산출 + git status.
> - **오교정 0** — kz `facts/subtitle.md` 111줄 ↔ `manual.en.vtt` 111큐 글자 동일(불일치 0).
> - **판별력** — 음성대조(원어 en·번역 ko만 → `translation-only`) + **적대(엔진 AC 미포함)**: 원어+번역 둘 다 다운로드 시 **원어 선택**(번역 아님).
> - 타임스탬프 단일·단조 · BOM 없음 · 팩트원=`manual.*` · **픽스처 무촉** · **추적파일 수정 0**(scripts/m1·docs·.claude·픽스처 meta/subs 불변) · 재실행 원본 불변.
> - 결정 2 구현: 원어=팩트·번역 아님·원어부재=공집합. Option C(M1 `_detect_origin_lang` import·순수 meta·`subtitleKinds.auto`의 `-orig` 신호).
>
> ## ④ 산출·확인필요·백로그
> - 산출(커밋 `5013bad`): `scripts/m2/`{`fact_selection`·`subtitle_transcript`·`pipeline_m2`·`gate_check_m2`·`GATE_RECORD_M2`} + kz `facts/subtitle.md`(111줄) + 위사 `facts/EMPTY-SET.md` + `M2-BRIEF.md`·`impl-plan.json`. 표본 미디어·meta·subs 미커밋(대용량 제외·사용자 결정).
> - **확인 필요 목록**(§6 "완료=목록 제출"·비차단): ① Option C가 `-orig` 신호 의존(부재 영상 미확인) ② §3 규칙 계약(Contract v5) 반영 보류.
> - **미세 관찰(백로그 후보)**: `fact_selection`이 "원어 탐지됐으나 다운로드 실패" 케이스를 `translation-only`로 라벨 — 결과는 공집합으로 옳으나 사유 라벨 부정확(표본 미저촉).
> - **엔진 dispatch 백로그 P 미저촉 실측**: `_slug`가 한글을 전량 제거 → 긴 `--phase`도 seed 파일명 `impl-plan-m2-1-m2-brief-md.json`(31자)로 접힘. 백로그 P는 긴 **ASCII** phase에만 유효.
>
> ## ⑤ 다음 착수 (세션 마무리 중)
> - **OQ-M1-A(무음 임계)는 M2에서 안 닫음**(결정 1 — 위상 상쇄 표본 1건뿐·합격선 미발명). M2는 팩트 층만 출하.
> - 후보: **M3(2차 STT)** — 선결 = 무음 게이트 `{"failed":True}`를 STT층이 실제 확인하는가(위상반전 사고 재발 경로·규약만 있고 코드 강제 미확인) · F3′ dedup(fix-5) · JS런타임 제품반영 · UAF 백로그 P/K/L/M/N/O.
> - **미커밋 이월**: UAF 핸드오프(§갱신10+11 — 사용자가 yt-stt만 커밋 선택)·yt-stt 표본 미디어. yt-stt M2 코드는 커밋됨(`5013bad`).

> **🔴 갱신 2026-07-24(12) — yt-stt M3(2차 음성 STT 층) 구현 완료·커밋 `9d1f275`. escalated 2회 해소·Advisor 독립 CP3 19/19.**
>
> **M3 = 종결**(yt-stt master `9d1f275`·8파일 1529줄). 엔진 run `impl-yt-stt-m3` 5단위(silence-gate·completion-gate·stt-engine·pipeline·milestone) 전건 Passed·**ENGINE_EXIT=0** 완주. UAF run 원장 커밋(본 커밋).
>
> ## ① escalated 2회 — 둘 다 Advisor 브리프/CP2 귀속 (B-5)
> - **escalated-1(§8↔seed 충돌)**: dispatch v1 proposal이 900초 실행 컨텍스트 타임아웃 2회→retry-limit 초과→escalated. 원인 = M3-BRIEF §8("실증형 AC·실제 audio16k 먹이기·몽키패치 대체 금지")이 proposal seed 의 "done=오프라인 안전 검사만" 제약과 정면 충돌 → Planner 가 구현 task done 에 실제 large-v3 STT 실행을 넣음. **해소 = §8 개정**(엔진 task done=오프라인 / 실제 large-v3=Advisor CP3 분리).
> - **escalated-2(completion_gate 임계↔stub elapsed)**: resume 에서 gate 3단위 Passed 후 pipeline escalated. 원인 = pipeline 이 wall-clock 으로 elapsed 측정 → 즉시반환 스텁에서 극소(0.1s) → completion_gate realtime 40x 거짓양성(임계 20x). **Worker 가 sleep/clamp 위조를 §6-1(무음 위장 없음) 위반이라 거부하고 정직하게 escalate**(이진 원칙 작동 실증). **해소 = 옵션 D**(§3.4 — elapsed 측정 책임을 pipeline wall-clock→`stt_engine.transcribe_audio` 반환으로 이동). done AC 에 `rtm<20` 회귀 방어 추가.
> - **핵심 교훈**: **정적 CP2 로는 done AC 간 동적 상충**(게이트 임계↔스텁 elapsed)을 못 본다. 엔진 Verifier CP2 도 통과시켰고(정적) Worker 실행에서 드러났다(동적). 메모리 `feedback-delegation-brief-defect-attribution` 재적중(이번엔 실행-시점 동적 결함).
>
> ## ② Advisor 독립 CP3 = 19/19 PASS (엔진 밖·실제 large-v3)
> `uaf-verified:` 위사 표본(공집합·전구간) 실제 large-v3 STT 1회(445s 순수·별도 스크립트·엔진 auto-Pass·gate_check_m3 자기출제 미사용). **검색 범위** = 위사 산출(transcript.raw.txt·json·meta) + 픽스처(`_JlQOnnEwxc`)/kz 무촉 + git. 오교정 0(raw 60줄==json 60seg text)·타임스탬프 단조·형식 단일·BOM 없음·json 무선별(id·seek·tokens·words 등)·meta R7(large-v3·cpu:int8·ko)·픽스처/kz 무촉·**한국어 STT 품질 육안 정확**. 엔진 gate_check_m3 GATE_EXIT=0 별도 확인.
>
> ## ③ 비차단 관찰(백로그)
> - **duration=0 → realtime 게이트 무력**: `stages.stt.realtimeMultiplier=0.0`은 M1 이 `meta.duration`을 미기록(0.0·impl-plan task1이 이미 지목)해서 나온 값. completion_gate realtime 축이 duration=0에서 무의미. 다만 위상반전 **주 방어인 0줄 축은 유효**(실제 60줄)라 비치명. 대응 = M1 duration 기록 or completion_gate duration=0 별도 처리.
> - fact_selection "번역만" 라벨 부정확(M2 백로그)·select_device 경계값 2048 미검증(CP3 실측 대상)·completion_gate 임계 20.0 하드코딩(§9 방침).
>
> ## ④ UAF 하네스 백로그 신설 2건
> - **Q(신설)**: proposal seed "오프라인 done" 제약 ↔ 브리프 "실제 실행 AC" 충돌 해소 메커니즘 부재. 무거운 실행 검증이 필요한 phase 에서 브리프가 seed 제약을 모르면 escalated. 대응 = seed 제약을 브리프 작성 규율에 명시 or 브리프 검증에서 대조.
> - **R(신설)**: 정적 CP2 가 done AC 간 동적 상충을 못 본다. escalated-2가 실증. 대응 = CP2에 "게이트 임계↔테스트 시나리오 정합" 점검 or done AC 상호 실행 대조.
>
> ## ⑤ 다음 착수
> - **M4(3차 문맥 교정 + 최후 수단 화면 OCR·P3-a/P3-b)** — 선결 = M3 산출(`transcript.raw.txt`·voice층)을 교정 입력으로 소비. Contract v4 에서 M4=FR-10+OCR 통합·M4↔M5 역전 해소.
> - 동시 백로그: F3′ dedup(fix-5)·JS런타임 제품반영·UAF 백로그 K/L/M/N/O/P/**Q/R**·duration=0 realtime 무력·위임 규율 B-1/B-3/B-4.
> - 미커밋 이월: yt-stt 표본 transcript/meta/subs(대용량·사용자 결정).

> **🔴 갱신 2026-07-24(13) — yt-stt M4-a(3차 문맥 교정 하네스) 완료·커밋 `91270d0`. Advisor 독립 CP3 38/38. 결함 3건 전부 Advisor 귀속·검증기 결함 5건(거짓 통과 1).**
>
> **M4-a = 종결**(yt-stt master `91270d0`). run 2개 — `impl-yt-stt-m4a`(6단위)·`impl-yt-stt-m4afix`(6단위) 둘 다 `ENGINE_EXIT=0`. 정본 = `M4A-BRIEF.md` v2. 산출 = `scripts/m4a/` 14파일.
>
> **사용자 확정 3건**: 범위=**M4-a 하네스만**(M4-b는 `OQ-M4-A` 미해소로 계약이 하류 차단 신호로 존치 — 숫자는 M4-a 실측이 있어야 근거가 생긴다) · 실행구조=**엔진 순차 릴레이**(interface-spec §5.6 미결 OQ 해소 — 하네스가 청크·carry·자족 브리프를 준비하고 엔진이 청크마다 fresh-context 수임자를 순차 디스패치. 원장·게이트가 남는다 = yt-stt를 UAF에 편입한 동기의 직접 해소) · 표본=위사 1건+`chunk_lines` 축소 실증.
>
> ## ① 결함 3건 — 전부 Advisor 귀속, Worker 코드 결함 0 (B-5 한 세션 3회 적중)
> - **(1) 경로 함정 경고 부재** — CP2(impl-plan 판독)에서 잡음. 한글+대괄호 경로를 task4·5가 직접 다루는데 브리프 §8에 M1 결함 1차(`glob` 대괄호 오해석)·2차(cp949 stderr 유실) 경고가 없었다. **브리프 선행 수정 후** impl-plan 2 task 직접 편집(백업 + `_advisorAugment` provenance·백로그 N 관행 경로). `uaf-verified:` **결과 실측** = 산출 코드의 `glob` 실사용 0건·`os.listdir` 채택·주석이 이유까지 명시. 보강하지 않았으면 M1에서 네 번 재발한 함정을 다섯 번째로 밟았을 개연이 있다.
> - **(2) `notes.json` 스키마 미명시 = 침묵 실패** — CP3 수행 중 발견. **다음 사이클 차단성**. 하네스가 읽는 키 6종(`changes`·`uncorrected`·`lowConfidence`·`entities`·`numbers`·`notes`)을 렌더된 브리프가 하나도 대지 않았다. 브리프는 설계상 교정자의 **유일한 입력**이라(§3.3) 키가 어긋나면 게이트가 아무것도 거부하지 않고 산출은 "잔여 오독 0"으로 **위장**된다 → P3-b 입력 소멸. **이 프로젝트가 이미 물린 "공집합이 결함을 가린다" 패턴.** **증거 = 명세를 쓴 Advisor 자신이 CP3 작성 시 키를 틀리게 추측했다**(`residual`로 씀) — 명세 저자가 틀리면 fresh-context 교정자는 틀린다. **해소 = 하드코딩 열거가 아니라 단일 소스 + 표류 가드**(소비 측이 키를 바꿔도 브리프가 옛 키를 계속 말하는 stale 결함 = 백로그 K 동형을 구조적으로 차단 · FS-5 6조를 런타임 추출로 푼 것과 같은 원리).
> - **(3) 내 CP3 검증기 결함 5건** — 아래 ②.
>
> ## ② ⭐⭐ 검증기 결함 5건 · 그중 거짓 통과 1건 (재사용 가치 최상)
> `uaf-verified:` 1차 실행 27/31의 FAIL 4건이 **전부 내 스크립트 탓**이었다(상대경로 해시 키 3건·부분문자열 휴리스틱 1건). 확장판에서 1건 더 — AST 대신 `#` 주석만 걸러내 **모듈 docstring의 설명 문면을 코드로 오인**했다.
> - **거짓 통과(가장 중요)**: "원본 변조를 거부한다"는 체크가 **통과했으나** 실제로는 해시 불일치가 아니라 **파일을 못 읽어서** 거부된 것이었다. 고친 뒤에야 진짜 축을 밟았다. **통과 사실만 봤으면 검증하지 않은 축을 검증했다고 보고했을 것이다.** → 규율: **통과한 항목도 이유를 봐야 한다.**
> - **느슨한 단언은 통과를 증거로 만들지 못한다**: v1 G1이 `kinds ⊆ {두 값}` 이라 **2건 넣고 1건만 나와도 통과**했다. 리팩터 후 J7을 `kinds == 두 값 and n == 2`로 못박아 한 부류가 떨어지면 반드시 실패하게 했다.
> - **탐지기에도 음성 대조를 붙였다** — 키 리터럴 탐지기가 단일 소스 파일에서 6건을 잡아야 통과하게 해서, 검사를 느슨하게 만든 것이 아님을 증명했다.
> - 이는 갱신 (6) "Advisor 체커 정규식이 실재 문면 7파일 9곳을 0 적중으로 오보"의 재발이며, **B-5 불변의 "검사 도구의 출력도 결함원"이 물린 세 번째 사례**다.
>
> ## ③ Advisor 독립 CP3 = 38/38 PASS
> `uaf-verified:` 엔진 밖·별도 스크립트·`gate_check_m4a*.py`(44KB Worker 자기출제) 미사용. **`gate_check`가 디스크에 없는 시점에 작성**해 자기출제 오염이 구조적으로 불가능하다. **검색 범위** = `scripts/m4a/` 전 모듈 + 위사 실입력 + 보호경계 7트리 해시 + 수정 run 사전 기준선 대조. 음성 대조 **11건**이 실제 거부를 냈다(줄 수 증감·타임스탬프 1글자·BOM·원본 해시 불일치·근거 없는 숫자 변경·키 빠진 브리프). 수정 run 변경 범위 = 신규 2·수정 4·무변경 6으로 소유 경계 이탈 0.
>
> ## ④ 백그라운드 run 중단 반복 (환경 실측·백로그 L 재적중)
> `uaf-verified:` 이 세션 백그라운드 엔진 run **4회 중 3회 중단**. 포그라운드(`timeout 560`) 재개만 완주. **검색 범위** = 이 세션 run 4건 로그·원장.
> - **원장이 없었으면 진행을 전혀 몰랐다** — 엔진 stdout 버퍼링으로 로그가 0바이트이거나 `ENGINE_EXIT` 한 줄뿐이고, 실제 진행(4단위 Complete)은 `events.jsonl` 에만 있었다.
> - **중단이 재시도를 소모한다** — 엔진이 `outcome=fail·kind=interrupted`로 정직 기록하고 `retry_count`가 오른다(한도 2). 중단 2회면 escalated. 다단위 run에서 실질 위험.
> - **대응** = 긴 run은 포그라운드 + `timeout` 명시. `--resume`(+`--run-id`)은 원장 기준으로 정확히 이어간다(실측 확인).
> - **부수**: 상대경로 훅 배선이 셸 cwd가 프로젝트 루트 밖으로 이동하면 깨진다(실측 — `binary_state_guard.py` 를 못 찾아 Edit 차단). 이때는 **조용히 통과하지 않고 오류로 막았다** — 문서화된 fail-open보다 강한 동작.
>
> ## ⑤ 미해소·다음 착수
> - **미해소로 남김(닫지 않음)**: `OQ-M4-A`(프레임 트리거 규칙 — M4-b 차단 신호·합격선 발명 금지) · `OQ-4`(중단 복구 — 보수적 기본값은 하네스에 넣되 실측 비교 없어 미해소) · `OQ-M1-A`.
> - **실증 한계(정직 기록)**: 유효 표본이 위사 59줄 1건뿐이라 `chunk_lines=15` 축소로 분할 경로를 **구조 실증**했다. LLM 출력 한계라는 실제 압력은 재현되지 않았다(브리프 §9 이탈 등재).
> - **다음 착수 = M4-a 릴레이 실행**(사용자 확정) — 청크마다 fresh-context 수임자 순차 디스패치 → `transcript.corrected.md`+`.diff.md`+`residual-spans.json` 산출. 이것이 `OQ-M4-A`를 닫을 근거를 만든다. 착수 시 필수 확인 = **수용 거부가 "신호 반환"일 뿐 하네스가 진행을 강제 차단하지는 않는다**(이번 범위엔 릴레이 실행이 없어 무영향이었다).
> - 동시 백로그: F3′ dedup(fix-5)·JS런타임 제품반영·duration=0 realtime 무력·UAF 백로그 K/L/M/N/O/P/Q/R·위임 규율 B-1/B-3/B-4.
> - 미커밋 이월: yt-stt `out/` 표본(대용량·종전 사용자 결정 유지).

> **🔴 갱신 2026-07-25(14) — yt-stt M4-a 릴레이 실행 완결(첫 실제 LLM 교정) + 병합 게이트 결함 4건 해소 + UAF `DEFAULT_TIMEOUT` 상향. 백로그 J 재발 실증·반증.**
>
> **직전 1순위였던 "M4-a 릴레이 실행" = 종결.** run 3개 — `impl-yt-stt-m4afix2`(Escalated·폐기) · `impl-yt-stt-m4afix3`(4단위 Passed·`ENGINE_EXIT=0`·커밋 `7e72df8`) · `impl-yt-stt-m4a-relay`(**6단위 Passed·`INVOKES=11`·`ENGINE_EXIT=0`**). UAF 측 커밋 `96c07f6`.
>
> ## ① 릴레이 실행 — 이 프로젝트의 UAF 편입 동기가 해소됐다
>
> `uaf-verified:` Advisor 독립 CP3 **41/41 PASS**(엔진 밖·별도 스크립트·`GATE_RECORD_M4A_RELAY.md` 미사용·**산출물이 디스크에 없던 시점에 작성**). **검색 범위** = 위사 표본 raw 60줄 + 4청크 work/ 22파일 + 산출 3종 + 사전 기준선 165파일 해시 + git HEAD 대조.
> - **산출**: `transcript.corrected.md`(5,879B·60줄) · `transcript.corrected.diff.md`(3,159B·4항목 6필드) · `residual-spans.json`(3,700B·**8건** = `uncorrected` 5 + `lowConfidence` 3).
> - **⭐⭐ carry 연속성이 실제 교정 근거가 됐다.** chunk01 이 `에디센스`→`애드센스` 2건을 확정 → `carry.confirmedTerms` 누적 → **chunk03 이 그 전례를 근거로 `에디션스`→`애드센스` 교정**. evidence 문면이 그것을 명시하고, 동시에 "철자 패턴이 기존 확정 사례와 정확히 일치하지 않아(에디센스 vs 에디션스) 확신 낮음"으로 `lowConfidence` 등재했다. **앞→뒤 순차 전달이 물리로 작동한 첫 실증**이며 Worker 13명 수기 팬아웃 브리프 미저장(UAF 편입 동기)의 직접 해소다.
> - **교정 4건 / 60줄**(chunk01 2 · chunk02 0 · chunk03 2 · chunk04 0) · **layer 전부 `context`**(팩트 공집합이므로 `fact` 0 — 강화된 게이트가 강제). 숫자 6곳 전부 사유와 함께 보존.
> - **해석 금지가 실행층에서 작동했다** — `조치로`(쇼츠로 후보)·`실행사`(시행사 후보)·`광고매체로`·`영상을 킵니다`·조사 오류를 전부 "그 자리에서 성립한다"며 `uncorrected` 로 보류. 오교정 0 우선(비대칭) 준수. 보류분이 P3-b 입력이 되는 설계된 흐름.
> - **침묵 통과 차단 작동** — done AC `assert not (changes==[] and notes==[])` + 브리프 §4 문면. chunk02·04 가 `changes=0` 을 내면서 판단 근거를 notes 에 남겼다.
> - **`OQ-M4-A` 근거 실물 확보** — 잔여 오독 8건. 프레임 트리거 규칙의 숫자를 실측 위에서 논의 가능(**여전히 미해소** — 숫자 발명 금지).
>
> ## ② 병합 게이트 근거 검증 결함 4건 — 귀속 = Advisor 브리프
>
> `uaf-verified:` 계약(`table-def` §7.5 4항 "허용 근거 = 팩트 근거"·§4.4 "역추적 가능한 참조")보다 구현이 약했다. 실호출 재현 + `git show HEAD` 대조.
> - **결함 1** `_evidence_layer` 가 `layer=="fact"` 면 `evidence` 를 읽지 않고 통과 → 임의 산문·빈 문자열·공백만으로 숫자 변경이 병합됐다. **결함 2** `_FACT_EVIDENCE_MARKERS` 의 `facts/` 접두가 **팩트 공집합 기록 `facts/EMPTY-SET.md` 까지 팩트 근거로 인정**(위사가 정확히 이 경우). **결함 3** 브리프가 공집합 귀결을 미명시 + 성립 불가능한 `facts/subtitle.md` 예시 제시. **결함 4** `screen` 자기신고 동형(M4-b 에서 재발 경로).
> - **귀속 = Advisor 브리프.** `M4A-BRIEF` §8 음성 대조가 "근거 없음→거부 / 근거 있음→통과" **두 축만** 요구하고 "거짓·공허한 근거→거부" 축이 없었다. **Advisor CP3 38/38 도 같은 두 축만 밟았다 — 명세가 안 쓴 축은 검증기도 안 봤다.**
> - 해소 = R-1~R-5(`M4A-DEFECTS.md` §3·전부 §4.4 열거에서 도출·발명 0). CP3 39/39 PASS(음성 대조 7건이 실제 거부·그중 5건이 수정 전엔 통과했음을 HEAD 대조로 재현·양성 2건과 R-5 범위 1건 보존).
> - **⭐ 통과한 항목도 이유를 봐야 한다** — A10(`layer=screen`+팩트 앵커)은 수정 전에도 거부됐지만 사유가 `numeric-invalid-evidence-layer`(우연)였고 수정 후 `numeric-evidence-layer-mismatch`(정확)로 바뀌었다. 통과 여부만 봤다면 이 개선을 확인할 수 없었다.
>
> ## ③ UAF — `DEFAULT_TIMEOUT` 900→2400 + 백로그 J 재발·반증
>
> `uaf-verified:` `contract_to_graph.py:51`. **근거 = 원장 실측 5건** — cheongryong-bubble `impl-s14-15-ui-sound` 가 같은 단위에서 **3회 연속**(retry 0·1·2 소진→Escalated) · `impl-s16-18-final` 1 · `impl-s04-08-core` 1 · yt-stt `m4afix2` 1. **검색 범위** = `DEFAULT_TIMEOUT`·`timeout=900` ripgrep 스윕 + 적중 run events 판독. 테스트 25+90 전건 통과(회귀 0). 상향 후 새 run 이 첫 시도에 proposal 완주.
> - **백로그 J 가 이미 등재한 결함의 재발이다**(2026-07-20 청룡 버블 실측 — 같은 원인 900초×3·같은 증상 stop-signal 미갱신). 제가 "새 발견"이라 보고했던 것을 정정한다.
> - **⭐ J 의 좌표를 확정했다** — `escalated` 이벤트에 **`gate_id` 가 없다**(`cycle_id` 만 있다). `recover_gate` 는 `stop-signal.json` 의 `pending_gates[].gate_id` 를 요구하고 주석이 "추측 0" 을 명시하므로 stop-signal 을 손으로 만들려면 **없는 gate_id 를 발명**해야 한다. 런처의 미기록은 **의도된 설계**다(`orchestrate_project.py:18-19` — `stop_reason=="gate"` 분기만 기록). `--gate-kind escalation` CLI·`escalationResolvers` 정책·`uaf-implement.md` §2 문서가 모두 있는데 **retry 소진 경로에서는 도달 불가능**하고, `--retry-limit` 상향으로도 부활하지 않는다(실측 `INVOKES=0` 즉시 재정지).
> - **⚠ 앞선 보고 정정**: 세션 중 이를 "J 의 '우회 가능' 판단이 반증됐다"고 보고했으나 **과한 표현이었다.** J 가 말한 우회는 **엔진 밖 처리**(Advisor 대역 완수)이며 그 자체는 여전히 가능하다. 다만 그것은 「Run 조율 우회 금지」 불변에 저촉되므로, **원장을 보존하려면 현 run 폐기 + 새 run-id 재실행이 유일한 경로**다(이번에 택한 길). 즉 J 의 회피책이 거버넌스 불변과 충돌함이 확인된 것이고, 그 사실을 백로그 §J 에 등재했다. `m4afix2` 원장은 이 증거로 보존한다.
>
> ## ④ 엔진 구조 게이트가 Advisor CP2 를 잡았다 (거버넌스 실증)
>
> 릴레이 impl-plan 의 `carry.json` 이 4 task `ownedBoundary` 에 중복 등재돼 게이트 해소가 **`[REJECT]` 6쌍 비중첩 위반**으로 거부됐다(원장 무오염·이벤트/revision 0 append). **Advisor CP2 는 "순차라 충돌 없다"고 판단해 통과시켰다** — 엔진이 잡았다. 귀속 = Advisor 브리프(§3.1 이 `carry.json` 소유권을 정하지 않았다). 해소 = B-5 절차대로 **브리프 §3.1a 선행 신설**(공유 상태 3종을 chunk01 단독 등재·소유 등재 ≠ 유일 기록자·`prepare()` 멱등성 근거) → impl-plan 직접 편집(백업+provenance·백로그 N 관행).
>
> ## ⑤ 이번 세션 결함 귀속 집계 — Advisor 5건 · 검증기 5건
>
> **Advisor 귀속 5건**: ①병합 게이트 음성 대조 축 누락(결함 4건의 원인) ②`merge_gate` 를 "순수 함수"라 서술(AST 로 반증 — 원본 해시 검사가 이미 파일을 연다) ③게이트 기록을 보호 경계에 미명시(`gate_check_m4a.py` 재실행이 `GATE_RECORD_M4A.md` 를 덮는 구조적 반복) ④`carry.json` 소유권 미정(엔진이 잡음) ⑤Escalated 결함을 "새 발견"이라 오보(백로그 J 재발).
> **검증기 결함 5건**: ①결함 아닌 케이스(A10)를 결함 목록에 넣음 ②**부분문자열이 FS-5 정본 인용문을 오검출해 거짓 통과**(차분 기반으로 재설계) ③sanity check 조건 오류 ④릴레이 기준선을 선행 run 이전 시점으로 잡아 거짓 FAIL ⑤허용 목록에 Advisor 자신의 브리프 수정분 누락.
> **Worker 코드 결함 = 0.** 요구받은 것을 정확히 구현했다.
>
> ## ⑥ 비차단 관찰 (다음 사이클 입력)
>
> - **`carry` 교정자 산출 갈래는 누적이 아니라 교체다**(`update_carry` docstring 명시·의도된 설계). `confirmedTerms`(기계 파생)만 누적한다. 논리는 있다 — 교정자 산출은 맥락 메모이고 누적하면 오래된 추정이 계속 흘러간다. **결함 아님.**
> - **⚠ 브리프 렌더 문면이 이를 오해시킨다** — `<key>Provided=False` 면 "**이번 청크까지** 산출이 없었다는 뜻"이라 렌더되는데 실제는 "이번 청크에서"다. **chunk02 교정자가 정확히 이 지점에서 오해**해 "이월됨"이라 기록했다(이월되지 않고 교체된다). M4-a 결함 2(키 미명시)와 같은 계열 — 한 낱말이 동작을 오해시킨다. 비차단(연속성은 `confirmedTerms` 담당).
> - **§6 확인항목 1(타임스탬프 중복) = 잠복 미발현.** `[02:27]` 2줄을 교정자가 건드리지 않아 `build_diff_entries` 의 `changes_by_ts` dict 키 충돌 경로가 밟히지 않았다. **다만 교정자가 직접 코드를 확인해 위험을 등재했다** — 브리프에 확인 항목을 둔 목적이 이것이다(밟히지 않아도 침묵하지 않게).
> - `evidence` 앵커가 가리키는 파일의 **실재는 검증하지 않는다**(사용자 확정 — 근거 판정 경로에 파일 접근 미도입). 존재하지 않는 `facts/subtitle.md` 앵커는 강화 후에도 통과한다.
>
> ## ⑦ 다음 착수 후보
>
> - **(가) M4-b(P3-b) 착수 판단** — `OQ-M4-A` 근거 실물(잔여 오독 8건)이 확보됐다. 트리거 규칙(전후 범위·장수·PPT형 판정 주체)을 이제 실측 위에서 사용자와 결정할 수 있다. **숫자 발명 금지는 유효**하다.
> - **(나) UAF 백로그 J 근본 수정** — Escalated 해소 채널 신설(런처가 모든 정지 사유에서 stop-signal 갱신 or `resolve_gate` 가 원장에서 좌표 복원). 이번 세션이 J 의 "우회 가능" 전제를 반증했으므로 우선순위가 올라갔다.
> - **(다) 브리프 렌더 문면 정정**(위 ⑥ "이번 청크까지") + 게이트 기록 보호 경계 명문화.
> - **(라) F3′ dedup(fix-5)** · JS런타임 제품 반영 · `duration=0` · 백로그 K·L·M·N·O·P·Q·R · 위임 규율 B-1·B-3·B-4.
> - **미커밋 이월 판단 필요**: yt-stt `out/` 텍스트 1.5MB(미디어 제외) — 릴레이 산출 3종(13KB)+`work/` 22파일(111KB)이 이 사이클의 실측 증거다. `transcript.raw.txt`(원본)도 미추적이라 교정본만 커밋하면 반쪽이 된다.

> **🔴 갱신 2026-07-26(15) — UAF 자체 RCA + 처방 5건 전부 실행. 백로그 J 본체·L 핵심·P 해소 + 거버넌스 규율 3종 신설·기계 강제 라이브 실증.**
>
> 사용자 지시 = "uaf 자체 root cause analysis" → RCA 보고 → "처방 모두 진행". 트랙 원장 = `docs/rca-prescriptions-ledger.md`(위임 보고 승격 + Advisor CP2 판정 — evidence 등급).
>
> ## ① RCA 결론 — 근본 원인 4 + 수렴 1
>
> - **RC-1 반응적 강제**: 규율은 발견 즉시 문서·메모리에 적히지만 기계 강제 전환의 트리거가 "재발 실측"이다(완전성 규율 4트랙 연속 재발·이진 원칙 6회 재현 뒤에야 각각 훅 도입 — 원장 실측). 재발이 우연이 아니라 설계된 결과였다.
> - **RC-2 접합부 무소유**: 생산자→소비자 계약 경계를 어떤 검증도 소유하지 않는다(스키마 예시↔체커 해석·런처 stop-signal 기록 조건↔resolve 전제·seed 단일파일 가정↔SD 실산출·K·Q — **각자는 옳고 접합부가 틀렸다**). 엔진 CP2가 단위별이라 횡단을 못 보는 것(M·R)과 UAF 자체 개발의 파일·Wave 단위 검증이 같은 위상 — 자기 유사성.
> - **RC-3 비정상 경로 후순위**: 성공·정상 정지만 1급 배선(J escalated 좌표 부재·L 관측 부재·N 조건부 채널 부재·P 입력 검증 부재·침묵 실패 계열).
> - **RC-4 검증 축 단일 근원**: 명세·브리프·검증 축이 전부 Advisor에서 나와 맹점을 공유("명세가 안 쓴 축은 검증기도 안 봤다" — 최근 5세션 연속 Worker 코드 결함 0·Advisor/검증기 귀속 집중).
> - **수렴**: UAF는 소비 프로젝트에 부과하는 원칙(기계 강제·fail-closed·원장·독립 검증)을 **자기 자신에게는 반응적·불균등하게 적용**한다. 기계 강제로 전환된 층에서는 실제로 잡혔으므로(엔진 구조 게이트가 Advisor CP2 실수를 잡은 실측 등) 명제가 아니라 적용이 문제다.
> - **라이브 발견**: 백로그 P·Q·R이 원장 파일에 부재했다(핸드오프 갱신 블록에만 "신설" — 등재가 등재가 아니었다). `uaf-verified:` 백로그 파일 전문 + 헤딩 패턴 스윕(검색 범위 = 그 파일)으로 확인 후 전입 해소.
>
> ## ② 처방 실행 내역 (5/5)
>
> - **처방 5**: P(슬러그 크래시)·Q(seed↔브리프 충돌)·R(정적 CP2 동적 상충) 백로그 원장 전입 — 각 항목에 「강제 지점」 행 포함.
> - **처방 3 (RC-1)**: `.claude/AGENT.md` §Invariants **「강제 없는 규율 신설 금지(강제 지점 결정)」** 신설(도입=지점 명시 / 미도입=사유 기록 — 결정도 이진) + 백로그 머리 「등재 형식 규율」 + **기계 강제** = `binary_state_guard.py` 확장(백로그 파일 신규 `## X.` 항목을 세그먼트 단위로 「강제 지점」 검사·+86/-0·테스트 18종) + **라이브 차단 실증 3건**(실파일 Edit deny·스크래치 Write deny·「강제 지점: 미도입—사유」 양성 통과). ⚠ AGENT.md는 상위 규약 — **사용자 승인 대기**.
> - **처방 2 (RC-2)**: `docs/verification-checklist.md` **§5.7 접합부 왕복 검증** 신설(생산 실물을 소비자에 실제로 먹인다·왕복 없는 접합부=판정 불가) + `docs/delegation-protocol.md` §2.1 done 지침에 접합부 왕복 항목 의무.
> - **처방 4 (RC-4)**: **§5.8 검증 축 도출** 신설(축은 정본 열거에서 도출·발명 금지·미검증 축 목록 의무·음성 대조·통과 사유 확인) + `.claude/agents/verifier.md`에 미검증 축 보고·귀속 후보 병기 의무.
> - **처방 1 (RC-3)**: 백로그 **J 본체 + L 핵심 + P** — Worker 2건 순차 위임·각각 Advisor CP2 Pass. 상세 ③.
>
> ## ③ 엔진 변경 (J·L) — 비정상 경로의 1급 시민화
>
> - **J(에스컬레이션 해소 채널)**: 엔진이 escalated 정지에 게이트 좌표(`gate-unit-<id>::exec-escalation`) 요구를 발급하고 pending_gates에 탑재 → 런처가 **모든 정지 사유에서** stop-signal.json을 게이트 분기와 같은 계약 4필드로 기록 → `resolve_gate --gate-kind escalation --response`가 응답을 해소 이벤트에 동봉 → `--resume`이 해소를 소비해 되돌림 이벤트 append → **해소 1건 = 추가 시도 1회**(재실패 시 새 요구 발급·이전 해소 소진 — 무한 재시도 없음). 응답은 되돌림 ref→재디스패치 번들 feedback까지 전파(실측 1). **좌표 없이 멈춰 있던 레거시 run도 `--resume` 1회로 해소 가능 상태가 된다.** 정본 = binding §3.4.
> - **L(관측 계약)**: `HeartbeatInvoker`(invoke 시작·종료마다 `logs/heartbeat.json` — hang(F2) 탐지의 유일 근거·failure-isolated) · `logs/failure.json`(미처리 예외 구조화 기록 후 재raise — 은폐 0) · `fold_slug` 48자+sha8(P 크래시·L 4-b 원장 커밋 불가 차단·48자 이하 바이트 동일·`_slug`/`slugify_run_id` 공통 규칙) · `--resume` 부재 오류에 실존 run 후보 목록 · `uaf-implement.md` §2 재개 예시 `--run-id` 정정 + 종료코드 표(0/2/3/1 — exit 2는 정상 정지). 정본 = binding §5.8.
> - **검증**: `uaf-verified:` Advisor가 3트리 테스트 직접 재실행 — 175+114+23=**312 전건 OK·EXIT=0×3**(검색 범위 = orchestration 2트리 + uahf step-host 트리·수임 보고 출력 불신). 접합부 왕복은 **실물**(런처가 쓴 stop-signal → resolve CLI 실호출 → 엔진 재기동 → 재디스패치·원장 직접 파싱)로 검증. `uahf/**`·05 spec·Frozen 접촉 0(git status 목록 기준). 신설 §5.7·§5.8 형식을 이 세션의 Worker 브리프 done이 즉시 소비했다(dogfooding).
>
> ## ④ 세션 내 결함·관찰 (정직 기록)
>
> - Advisor 원장 편집 실수 1건(문장 훼손) — 즉시 원복. 훅이 Advisor 문면 2건을 차단(금지 상태어 인용 1·본 핸드오프 초안 1) — **규율이 저자 자신에게 작동함의 실증**. 훅 1차 라이브 테스트는 내 테스트 입력 결함(본문에 검사 토큰 포함)으로 통과했다 — "통과한 항목도 이유를 봐야 한다" 재적중. 토큰 포함 검사는 바닥 장치다(의미 판정은 게이트·리뷰 소관 — rca 원장에 한계 명시).
> - Worker 코드 결함 = 이번 세션 0건 유지(2 Worker·브리프 좌표 불일치 보고 0 — 브리프에 실측 좌표만 담고 미확인 지점을 `uaf-assumed:`로 표기한 것이 유효했다고 추정한다).
>
> ## ⑤ 미해소·대기
>
> - **사용자 결정 대기**: AGENT.md 불변 신설 승인(상위 규약) · 커밋 방식.
> - **미해소 이월**: per-unit timeout(L §4) · `recover_gate` 다중 pending 특정 지목(`--gate-id`) · Q·R의 기계 강제(현재 절차 층만) · 위임 규율 B-1·B-3·B-4 · 커버리지 강제·SD manifest 배선·스킵 브리지(메모리 하네스 결함 3종) · UAF 스크립트 인코딩 스윕 · 백로그 K·M·N·O.
> - **다음 실 run 관측 좌표**: 실 CLI invoker 래핑(`[INVOKES] total=` 정상 표시)·heartbeat 실기 갱신.
>
> ## ⑥ 다음 착수 — ★ 사용자 확정 2026-07-26: **UAF 하네스 개선을 우선 수행**
>
> **다음 세션 1순위 = UAF 개선(사용자 지시 원문: "uaf 관련 개선을 우선 수행으로 진행"). 제품 트랙(yt-stt M4-b)은 그 다음이다.** 개선 대상의 선택·순서 확정 권위는 착수 세션의 사용자다 — 아래는 Advisor 권고 순서(①→②→③)다.
>
> 1. **백로그 K** — Projection 정본 포인터 정합 체커(RC-2 계열 잔여 중 최저비용·design_completeness 체커 자리에 추가·append-only라 파일이 실재해 **조용히 틀리는** 결함).
> 2. **위임 규율 B-1·B-3·B-4** — RC-1 잔여 최대 덩어리(위임·보고 층 강제 0). 착수 유의: B-1은 PreToolUse로 안 잡힌다(위임은 도구 호출이 아니다) → 수임 Agent 정의(`.claude/agents/*.md`)에 착수 전 점검을 박는 쪽이 현실적. B-3은 불변 신설이 Advisor 직접 병렬 위임 방식 자체를 금지하게 되는 거버넌스 무게 — 사용자 결정 필수. 상세 = 메모리 `uaf-delegation-enforcement-gap`.
> 3. **이번 트랙 잔여** — per-unit timeout(백로그 L §4) · `recover_gate --gate-id`(다중 pending 특정 지목) · Q·R 기계 강제(현재 절차 층만).
>
> 그 외 열린 하네스 결함(순위 미배정): 커버리지 강제(θ≠커버리지 역설·메모리 `uaf-coverage-enforcement-gap`) · SD manifest 배선 3건(`uaf-design-manifest-path-defect`) · SD 스킵 브리지(`uaf-solution-design-skip-gap`) · 백로그 M·N·O · §DC-8(a)·02 개정 · UAF 스크립트 인코딩 스윕 · 상류 바인딩 2차(디커플링).
>
> **착수 시 최소 read-set** = 본 갱신 블록(15) + `docs/rca-prescriptions-ledger.md` + `docs/post-tuning-improvement-backlog.md` 해당 § + 메모리 `uaf-rca-prescriptions-track`. 신설 규율 준수 사항: 새 규율·백로그 등재엔 「강제 지점」 행(훅이 차단한다) · 새 배선엔 접합부 왕복(§5.7) · 검증 축은 정본 열거 도출(§5.8).
>
> (후순위·제품 트랙) yt-stt **M4-b 판단** — escalated가 나도 이제 엔진 채널로 해소·재개 가능. 메모리 `uaf-product-yt-stt`.

> **🔴 갱신 2026-07-26(16) — 백로그 K 해소 + 위임 규율 B-1·B-3·B-4 종결(B-3 = 사용자 결정 옵션 B). 갱신(15) ⑥ 권고 순서 ①·② 소화 — 잔여 = ③ RCA 트랙 잔여.**
>
> 사용자 지시 = `/uaf-continue` 인자("핸드오프 갱신(15) ⑥의 사용자 확정대로 UAF 하네스 개선 1순위 착수 — 권고 순서 K → B-1·B-3·B-4 → RCA 트랙 잔여"). 트랙 원장 = `docs/backlog-k-delegation-b-ledger.md`(위임 보고 승격 2회 + Advisor CP2 2회 + B 계열 결정 — evidence 등급).
>
> ## ① 백로그 K 해소 — Contract 포인터 정합 체커 (Desired ③)
>
> - `design_completeness.py` 신규 검사: produced·실재·`.md` 산출물의 **최고 `project-contract.v<N>.md` 참조 == 계보 현재 인스턴스**. 미달=stale·초과=dangling·**판독 실패=차단**(판정 불가≠통과·이진 원칙)·계보 정당 부재/참조 0건/비-md=비적용. 이탈 채널 `contractRefPinned{reason,confirmedBy}`. path 해석은 기존 존재 검사와 **동일 식 재사용**(해석 이원화 금지 — RC-2 재발 방지). 시그니처 `check_design_completeness(policy, manifest, contract_dir=None)` — 기존 호출부(resolve_gate·pretooluse 가드) 무변경, 파생 = `<manifest>/../../project-contract`.
> - `uaf-verified:` 실물 yt-stt 접합부 왕복 양방향 — 현행 v4 → `[DESIGN-COMPLETE]` EXIT=0 / 실물 계보 사본+합성 v5 → **stale 7건 EXIT=2**(yt-stt 무촉·검색 범위 = 매니페스트 등재 7종). K 원 증상(성숙 후 헤더 stale — "조용히 틀린다")의 재발 경로가 이제 구현 편입 게이트에서 차단된다.
> - **Worker 위임 1건 + 재작업 1회.** 1차 CP2(Advisor): 구현 결함 0·신고 이탈 ②(OSError 흡수)를 **기각**(훅 층 fail-open 불변을 게이트 체커에 오적용 — 판정 불가는 차단) → 재작업 → 2차 CP2 Pass·CP3 승인. `uaf-verified:` 테스트 3트리 독립 재실행 129+175+42·EXIT=0×3 + 별도 적대 8케이스(잡파일 fullmatch·`.MD`·v04 정규화·비-dict 핀·오류 순서 보존·미러 바이트 직접 대조) 8/8. **Lesson 후보**: "fail-open 불변은 훅 층 소유 — 게이트 체커에서 판정 불가는 차단이며, 비적용(정당한 부재)과 미확정(판독 실패)을 같은 반환값으로 뭉개면 조용한 오통과가 된다."
> - 산출: 체커·scaffold 미러(바이트 동일)·`design-manifest.schema.md` §Contract 포인터 정합 규칙(판정 표 8행·비적용/차단 경계 문단)·테스트 15건(+275/-0 순수 append). Desired ①·② 미도입 사유는 백로그 §K 해소 행에 기록.
>
> ## ② 위임 규율 B-1·B-4 강제 배선 (Advisor 직접 — 거버넌스 문서 층·선례 B-0·B-2·B-5)
>
> - **B-1(착수 전 점검 산출 의무)**: 공백의 정체 = 규칙은 있는데 ① "누락"만 잡고 **모호(비이진 done)** 를 안 잡았고 ② 점검 **산출(증거)** 이 강제되지 않아 조용히 생략 가능(2026-07-21 실측 5/5 미작동). 배선 = `delegation-protocol.md` §2.4 「점검 산출 의무」(보고 서두 `[착수 전 점검]` 블록·3항 이진: 필드 존재·done 이진성·context 실재·**모호한 done=누락과 동급**·블록 부재=보고 무효) + `worker.md`·`planner.md` 착수 전 점검 절(역할 정의 = 수임 시마다 자동 주입되는 층) + §3.2 회수 반려. **첫 실사용 실증**: 이 세션 Worker 보고 2건이 `[착수 전 점검]` 블록을 실제로 제출했다.
> - **B-4(동료 계약·이탈 선언)**: 실행 중 전파는 이 환경에서 **불가**(fresh-context 수임 Agent 간 채널 부재 — 정직 기록). 실현 가능한 최대치 = §2.5 「동료 계약·이탈 선언」(브리프 측 동료 계약 블록[Planner 초안 완료 조건] + 보고 측 이탈 선언 블록[`[동료 영향]` 지목] + **회수 직후 Advisor 이탈 교차 대조**·§2.7 원장 ④항 기록 의무). 07 R1~R4 재정의 0. 잔여 미해소 = 실시간 전파(수임 Agent 간 통신 표면 등장 시 재심).
> - 강제 지점(공통): ① 수임 역할 정의(자동 주입 층) ② Advisor 회수 반려(§3.2). 자동 차단 장치 미도입 — 사유: 위임·보고는 도구 호출이 아니어서 개입 표면이 없다. `uaf-verified:` Core 순수성(02 INV-7) — §2 신설 문면에서 환경 토큰(PreToolUse·시스템 프롬프트·서브에이전트) 자가 검출·정정 후 ripgrep 스윕으로 §3·§4에만 잔존 확인(검색 범위 = delegation-protocol.md 전문).
> - verifier.md 무수정 결정(「대조 기준 부재 처리」가 착수 전 점검의 동등물) · AGENT.md 무수정(규칙 기존재 — 강제 배선만).
>
> ## ③ B-3 해소 — 사용자 결정(카드) = 옵션 B 「원장 의무만」 · 같은 세션 구현
>
> 옵션 A(구현 동형 불변)/B(원장 기록 의무만·Advisor 권고)/C(미도입+사유 기록) 중 **사용자가 B 선택**. 배선 = `.claude/AGENT.md` §Invariants 「설계 산출 원장 기록 의무(경로 자유·기록 필수)」 신설(**원장 0건 설계 산출 금지** — 구현 층은 경로를, 설계 층은 기록을 강제·상위 규약 개정 승인 = 이 사용자 결정) + `.claude/CLAUDE.md` §구현 단계 2층 운용 배선(상시 로드 층·SD 원장 = `solution-design-data` events·form-A 수기 append 허용). 기계 차단 미도입 — 사유: 설계 산출 Write 의 결정적 식별이 소비 프로젝트마다 경로가 달라 불가. **재심 좌표 = SD 실행 호스팅 도입 시 엔진 게이트 승격**(옵션 A 재심 동일 시점). → **위임 규율 트랙 B-0~B-5 = 6건 종결**(개별 근거 = 메모리 `uaf-delegation-enforcement-gap` 표·원장 §2~§4).
>
> ## ④ 세션 관찰 (정직 기록)
>
> - 훅 차단 2회 실증 — 원장 초안의 미검증 주장 인용("전건" 무마커)·백로그 편집의 세그먼트 오파싱(헤딩 조각). 전자는 규율이 저자에게 작동한 실증, 후자는 앵커 조정으로 해소(훅 결함 아님·편집 문자열에 헤딩 포함이 원인).
> - Advisor 도구 호출 실수 1건 — 기존 Worker 재개(SendMessage) 대신 무의미 fork 발사 → 즉시 무해 종료 확인·재발신. 산출물 영향 0.
> - 귀속 복합 판정 1건 — OSError 이탈의 귀속 = 위임(브리프가 판독 실패 거동 미지정) 주 + Worker(불변 적용 범위 혼동) 부. B-5 규율 실사용.
>
> ## ⑤ 다음 착수 (갱신(15) ⑥ 권고 순서의 잔여 = ③만)
>
> 1. **RCA 트랙 잔여** — per-unit timeout(백로그 L §4) · `recover_gate --gate-id`(다중 pending 특정 지목) · Q·R 기계 강제(현재 절차 층만).
> 2. 그 외 열린 하네스 결함(순위 미배정)은 갱신(15) ⑥ 목록 유지: 커버리지 강제 · SD manifest 배선 3건 · SD 스킵 브리지 · 백로그 M·N·O · §DC-8(a)·02 개정 · UAF 스크립트 인코딩 스윕 · 상류 바인딩 2차.
> 3. (제품 트랙) yt-stt M4-b 판단.
>
> **미해소 이월**: B-4 실시간 전파(환경 제약·수임 Agent 간 통신 표면 등장 시 재심) · B-3 기계 차단(SD 실행 호스팅 도입 시 엔진 게이트 승격 재심) · 갱신(15) ⑤ 목록 중 K·B-1·B-3·B-4 를 제외한 나머지 유지.

> **🔴 갱신 2026-07-26(17) — RCA 잔여 부분 소화: `recover_gate --gate-id` 해소(접합 3면 포함). per-unit timeout = 설계 조사 후 이월.**
>
> - **`recover_gate --gate-id` 해소**(Worker 위임 2건·각 Advisor CP2 Pass·CP3 승인): ① `resolve_gate.py` — 다중 pending 동일 gateKind 의 **침묵 첫-선택 제거**(무지목 다중 매칭 = 후보 열거·원장 무변경 비영 종료) + `--gate-id` 특정 지목(부재/kind 불일치 사유 구분 출력) ② `render_gates.py` — 항목별 `resolve_command` 가 자기 gate_id 를 상시 지목(결정적 셸 인용 규칙·가법) ③ `uaf-implement.md`·binding §3.2/§3.4 문면 동기화. `uaf-verified:` 접합부 왕복 = 런처 실산출 stop-signal → 렌더 자동 출력 문면 → 실제 argv 실행 → 재렌더 "미해소 0건"(수임 실행 + Advisor 3트리 재실행 138+175+42·diff 정독으로 재확인). 신규 테스트 9건(g1~g5·r7a~r7d)·기존 케이스 문면 수정 0.
> - **per-unit timeout(백로그 L §4) = 설계 조사 완료·구현 이월**: `InvokeRequest.timeout` per-request 필드 실재 확인·StepHost 는 uahf 무수정 경계 → **orchestration 층 래퍼 invoker(`_effective_invoker()`) 경로가 무접촉 해법 후보**. 미확인 = `Step.from_dict` 임의 필드 보존 여부 + impl-plan 스키마 신설·검증 규칙 — 별도 설계 사이클 대상(좌표 = 원장 §5-A·백로그 L 잔여 행).
> - **Q·R 기계 강제** = 변경 0(백로그 기존 미도입 사유 행 유지 — 각각 브리프 렌더 결합·Verifier 판정 축 확장의 별도 트랙).
> - **미검증 축 이월 2건**(수임 신고·Advisor 수용): 실 LLM invoker 경유 다중 escalation run 미수행(다음 실 run 관측 좌표에 추가) · 한글 gate_id 셸 인용 거동 미실측(엔진 파생 규칙상 ASCII — 발생 시 재심).
> - **다음 착수**: per-unit timeout 설계 사이클(위 좌표에서 시작 — Step 필드 보존 확인이 첫 단계) · 그 외 갱신(16) ⑤ 목록 유지.

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

## ~~★ 1순위 — yt-stt M1 실기 검증~~ → **완료 2026-07-21** (상세 = 위 갱신 블록 §갱신 2026-07-21(2))

> 5종 판정 = ①자산스킵 ✅ ②자막판별 ✅ ③다운믹스 실측 ✅ ④무음게이트 오탐 ✅ ⑤임계 근거 🟡(도메인 상식값·실측 1건이 뒷받침·OQ 후보). 결함 3계열은 run `impl-yt-stt-m1fix2` 로 해소(Advisor 독립 실증 6/6 PASS·CP3 승인). **다음 착수는 아래 "2순위 이하 후보" 의 (가) M2 로 승격** — 선결 = RISK-6(OCR 용어 선별 규칙) 결정 · M2 확인 항목에 **`ko` 트랙 미수신 여부**(위 비차단 관찰 a) 추가.
>
> <details><summary>원 1순위 기록(착수 근거 — 이력 보존)</summary>

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

</details>

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
