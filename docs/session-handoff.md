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
