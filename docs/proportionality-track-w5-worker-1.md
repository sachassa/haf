# 절차 비례화 트랙 Wave 5 — Worker 완료 보고 전문 (attempt 1)

수임: Worker (Advisor 위임) · 2026-07-27 · 브리프 정본 = `docs/proportionality-track-ledger.md` §4 Wave 5 + §5 R-1
보고 형식 = `docs/delegation-protocol.md` §2.2 「보고 전문 파일 우선 기록 + 최종 응답 한정 형식」
수명 등급 = `evidence`(`docs/artifact-lifecycle-policy.md` §2·§3·§5)

---

## [착수 전 점검]

필수 필드 7/7 존재 · done 6/6 이진 판정 가능 · context 12/12 실재

- **필드 7/7** — from(Advisor·위임 문면상 명시) · to(Worker) · task("Wave 5 최종 통합 구현") · input(원장 §4 Wave 5 전문 + §5 R-1 + 선행 완료 상태 7건) · output(7항·Advisor 재량 조정으로 원장 output 3 = 핸드오프 갱신 제외) · done(원장 done 1~6이 output 7항에 1:1 사상) · context(원장·선행 산출물 경로).
- **done 6/6 이진** — ① CLAUDE.md 개정 문면 요건 4종(원장 공통 명시·재정의 0·값 하드코딩 0·근거 문면 보존) 각각 문면 대조로 참·거짓이 갈린다 ② 스키마 구예시 정정은 값 대조 ③ 문서 정합 3건은 각 파일 문면 대조 ④ E2E 8지점은 exit code·산출물 실재로 판정 ⑤ 라이브 차단은 deny 반환 유무 ⑥ 회귀 4스위트는 EXIT 값.
- **context 12/12 실재** — `docs/proportionality-track-ledger.md` · `.claude/CLAUDE.md` · `orchestration/adapters/claude/{lane_resolve.py,lane-registry.json,pretooluse_lane_guard.py,design-manifest.schema.md,design_completeness.py,project-orchestration-binding.md}` · `planning/adapters/claude/solution-design-binding.md` · `entry/adapters/claude/entry-binding.md` · `discovery/adapters/claude/discovery-binding.md` · `docs/delegation-protocol.md` · `uahf/framework/adapters/claude/orchestration-data/e2e/{setup_lite.py,verify_run.py}`. 전건 열어서 확인했다.

## [이탈 선언]

단독 위임이므로 병렬 집합(§2.5) 이탈 선언 의무는 **비적용**이다. 아래는 위임 문면 대비 자발 신고다.

| # | 이탈 | 사유 | 영향 |
|---|---|---|---|
| DV-1 | 위임 output 목록 밖 파일 1건 개정 — `planning/adapters/claude/solution-design-binding.md` §7A.2-L 표 「표준 레인」 행 | output 2가 스키마 구예시를 정정하면 그 행의 좌표("`design-manifest.schema.md` 예시 2종의 `artifacts[].path`")가 **stale 이 된다**. 알려진 stale 포인터를 남기는 것은 L-06 교훈이 지목한 결함이다 | 1행 문면 갱신(좌표 교체 + 해소 부기). 계약 요소·값 무변경 |
| DV-2 | 정정 방식 = append 주석이 아니라 **제자리 교체** | 위임이 허용한 2택 중 제자리를 택했다. 근거 = 이 문서는 이력 원장이 아니라 스키마 참조 문서이고 예시는 그대로 복사되는 표면이라 틀린 값이 남으면 소비자가 체커에 차단된다 | 정정 경위는 같은 문서의 정정 절이 보존(이력 소실 0) |
| DV-3 | 정정 대상에 `screen-mock` 의 `mocks/index.html` → `../../mocks/index.html` 포함 | 위임 문면은 `docs/<id>.md` 를 지목했으나 같은 `artifacts[].path` 키이고 동일 해석식에 걸린다. 이 1건만 남기면 예시가 반쪽 정정된다 | 같은 결함의 동종 1건 |
| DV-4 | 스키마 문서·discovery-binding·entry-binding 에서 **인접 상태 문면 동기 갱신** | 정정으로 stale 이 되는 서술(“표준 레인은 미해소다” 문단 · §8.3 미해소 항 3 · 행 B 정정 경위)을 함께 갱신했다 | 문면 정합. 값·계약 무변경 |
| DV-5 | E2E 에서 **SD 설계 층 원장**(`solution-design-data/events/maturation-<run-id>/`)을 별도로 만들지 않았다 | 그 트리는 리포 내 append-only 실데이터 트리이며 픽스처 이벤트를 넣으면 실데이터를 오염시킨다. 대신 경량 run 원장의 S2 단위(`delegation.input`·`interfaceContract.consumes`)에 시드 프로파일을 기록했다 | §7A.2-S (S3) 요구는 **부분 대체**이며 미해소로 등재(OQ-2) |

---

## artifacts

리포 (6 수정 · 1 신규 트리):

1. `C:\my-claude-project\universal-agentic-framework\.claude\CLAUDE.md` — 「구현 단계 = 2층」에 레인 분기 항 추가(아래 §개정 절 전문).
2. `C:\my-claude-project\universal-agentic-framework\orchestration\adapters\claude\design-manifest.schema.md` — 표준 예시 2종 `artifacts[].path` 제자리 정정 + 정정 절·잔여 명시.
3. `C:\my-claude-project\universal-agentic-framework\entry\adapters\claude\entry-binding.md` — §6 표 행 B `policy` 값 stale 정정 + 경위 1항.
4. `C:\my-claude-project\universal-agentic-framework\discovery\adapters\claude\discovery-binding.md` — §8.2 (가) θ 5축 실측값 갱신 + §8.3 미해소 항 3 상태 갱신.
5. `C:\my-claude-project\universal-agentic-framework\docs\delegation-protocol.md` — §4 정본 포인터 표 1행 추가.
6. `C:\my-claude-project\universal-agentic-framework\planning\adapters\claude\solution-design-binding.md` — §7A.2-L 「표준 레인」 행 좌표 갱신(DV-1).
7. `C:\my-claude-project\universal-agentic-framework\uahf\framework\adapters\claude\orchestration-data\runs\w5-e2e-lite\` — 경량 레인 E2E 원장(`config.json`·`graph.json`·`gate_policy.json`·`events.jsonl` 15행·`revisions.jsonl` 3행·`artifacts.jsonl` 4행·`logs/gate-resolution-record.json`·`logs/verify-run.log`).

scratchpad (픽스처·리포 밖 — 등급 ephemeral):

- `...\scratchpad\w5-e2e\ws\` — 픽스처 소비 워크스페이스(`docs/solution-design.md` · `.claude/solution-design/{policy/default-policy.yaml,design-manifest.json}` · `src/report_summary.py` · `tests/test_report_summary.py` · `sample.log`).
- `...\scratchpad\w5-e2e\build_w5_lite.py` — 원장 빌더(결정적·`setup_lite.py` 동형).
- `...\scratchpad\w5-e2e\logs\` — 지점별 실행 로그 9건(각 말미 `EXIT=` 보존).
- `...\scratchpad\w5-e2e\verify-out\` — `verify_run.py` 리포트 2건.

### 개정 절 전문 인용 — `.claude/CLAUDE.md` 추가분

> **레인 분기(절차 비례화 트랙 — 위 기본값의 가법 특수화·기본값 문면 무변).** 라우팅은 레인 값에 따라 두 갈래로 갈린다. 레인은 **두 값만** 가지며 제3의 값을 두지 않는다 — 선언 부재·패턴 매칭 불가는 표준으로 귀결한다(fail-closed·안전측). 어휘·패턴·마커 경로의 정본은 아래 레지스트리 데이터이고 이 절은 **소비 측**이다(재정의 0·값 사본 0).
>
> - **표준 레인(`standard`) = 위 기본값 그대로.** 엔진 경유로 구현하고 원장·게이트 큐는 엔진이 소유한다. 접점(Contract·게이트·정본 문서·스키마·정책 데이터 — 구체 패턴은 레지스트리 데이터)을 건드리는 작업은 전부 이 레인이다.
> - **경량 레인(`lightweight`) = 접점 0 판별 + 마커 물리화 시에만.** **Advisor 직접 위임**으로 조율하고 **경량 원장**(form-A 수기 append)을 남긴다. 판별 = `orchestration/adapters/claude/lane_resolve.py`(형태 B·LLM 0·결정적 — 계산·방출까지만이고 적용은 0). 접점 패턴·레인 어휘·사유 필드명·마커 경로 = `orchestration/adapters/claude/lane-registry.json`(Policy as Data 단일 소스). 적용의 물리 산출물 = 워크스페이스 레인 마커(경로는 레지스트리 `marker` 절). 원장 규약(배치·최소 필드·`basis` 형태·파생 등급·종결 조건) = `orchestration/adapters/claude/project-orchestration-binding.md` §5.9. SD 프로파일 선택·워크스페이스 시드 = `planning/adapters/claude/solution-design-binding.md` §7A.2-S·§7A.2-L(프로파일 실값은 그 policy 파일 데이터). 인터뷰 프로파일 참조 배선 = `discovery/adapters/claude/discovery-binding.md` §8.3.
> - **원장 0건 금지는 두 레인 공통이다.** 경량 레인은 **원장을 줄이지 않고 조율 주체만 바꾼다**(엔진 자동 append → form-A 수기 append). 불변 자체는 `.claude/AGENT.md` §Invariants(Run 조율 우회 금지의 "원장 없는" 조건절 · 설계 산출 원장 기록 의무)가 소유하며 이 절은 재정의하지 않는다 — § 포인터만 둔다. 경량 레인 종결 조건 = 기존 결정적 러너 통과 + 원장 비공집합(binding §5.9 (h)).
> - **강제 지점 = Write 시점 훅.** 경량 레인 마커 하에서 접점 파일 Write 는 PreToolUse 훅(`orchestration/adapters/claude/pretooluse_lane_guard.py` · `.claude/settings.json` 배선)이 차단한다. 훅 배선은 상대경로로 쓰고 **실제 도구 호출로 차단을 확인**한다(위 훅 배선 절 — 단위 검증으로 갈음하지 않는다). 승급 경로 2개 = ① 레인을 표준으로 재판정 ② 사용자 override + 사유를 마커·원장에 기록(사유 필드명은 레지스트리 데이터).
>
> `uaf-verified:` 위 레인 분기 항의 파일 경로·소유 관계는 `lane_resolve.py`·`lane-registry.json`·`pretooluse_lane_guard.py`·`.claude/settings.json` PreToolUse 블록·binding §5.9·solution-design-binding §7A.2-S/§7A.2-L·discovery-binding §8.3 직독으로 확인했다. **검색 범위** = 그 8개 표면이며, 소비 프로젝트에서의 경량 레인 실운용은 이 문면의 범위 밖이다.

기존 「라우팅 기본값」 문단(엔진 경유 기본 · "원장 없는 임시 Worker 직접 디스패치로 프로젝트를 구현하지 않는다" · **git 앵커 90ca19c** · `/uaf-implement` 물리 발화 · 05 §2.1·§3.3 포인터)은 **문자 단위로 보존**했고, 훅 배선 절·관측 배선 절·설계 층 원장 절은 무촉이다.

---

## self_check

| # | done 항목 | 충족 | 근거 · 검사 범위 |
|---|---|---|---|
| 1 | CLAUDE.md 개정 — 원장 0건 금지 두 레인 공통 명시 | 1 | 3번째 불릿 머리글이 그 문장 자체다. 검사 범위 = 개정 절 본문 |
| 2 | 개정이 AGENT.md §Invariants 를 재정의하지 않음(§ 포인터만) | 1 | 개정 절은 불변 소유자를 "`.claude/AGENT.md` §Invariants"로 지목하고 조건절만 인용한다. `.claude/AGENT.md` diff hunk = 0(`git status` 상 미변경) |
| 3 | 개정에 값 하드코딩 0 | 1 | 개정 절에 접점 패턴 문자열 0 · 프로파일 실값(13/1종·예산·θ) 0 — 전부 `lane-registry.json`·policy 파일·binding § 포인터로만 지시. 레인 어휘 2값은 표기했고 그 정본을 레지스트리·로더로 명시했다(binding §5.9 (e) 선례 동형). 검사 범위 = 개정 절 본문 |
| 4 | 기존 엔진 경유 근거 문면 보존 | 1 | git 앵커 90ca19c·`/uaf-implement`·05 § 포인터 포함 문단 무변(위 인용부 말미 참조) |
| 5 | 스키마 구예시 정정(J-4·발견 1) | 1 | 예시 2종의 `artifacts[].path` **18개**(예시 1 = 12 · 예시 2 = 6) 값이 `../../` 접두로 교체됐다. `status: excluded` 항목(`screen-design`)은 `path` 키가 없어 대상 아님. 문서 전체 `"path":` 키 20건 중 구체 값 19건은 모두 `../../` 접두이고(경량 예시 1건은 W1-b 시점부터 정합), 나머지 1건은 §스키마 절의 자리표시자 `<산출물 경로>` 다. 검사 범위 = `design-manifest.schema.md` 본문의 `"path":` 키 grep 20건 |
| 6 | 문서 정합 ① entry-binding 행 B stale 정정 | 1 | 행 B `policy` 칸 = "경량 프로파일 참조 (ref = lightweight)". 대조 근거 = `entry-registry.json` 행 6 `policy.ref == "lightweight"`. 행 A(행 1)는 `default` 로 무변경 |
| 7 | 문서 정합 ② discovery-binding §8.2 (가) θ 드리프트 정정 | 1 | 표 5행이 `discovery-data/policy/default-policy.yaml` `thresholds` 실측값(0.85/0.80/0.75/0.75/0.80)과 일치. §8.3 미해소 항 3의 상태 라인도 해소로 갱신 |
| 8 | 문서 정합 ③ delegation-protocol §4 보고 파일 행 추가 | 1 | 표에 "보고 전문 파일의 지위 … → 05 §3.6" 1행 추가 |
| 9 | E2E (a) 레인 판별 | 1 | `lane_resolve.py --root <ws>` → `lane=lightweight`·`basis=no-touchpoint`·`touchedCount=0`·EXIT=0(`logs/a-lane-resolve.log`) |
| 10 | E2E (b) 마커 물리화 + 경량 SD policy 시드 | 1 | `<ws>/.claude/lane.json` 실물 기입(Write 도구) · `lightweight-policy.yaml` → `<ws>/.claude/solution-design/policy/default-policy.yaml` 로 파일명 `default-policy.yaml` 배치(§7A.2-S (S1)(S2))·EXIT=0 |
| 11 | E2E (c) 통합 설계 문서 1종 산출 | 1 | `<ws>/docs/solution-design.md` 실재(요구·선언·기능·데이터·테스트·미결 6절) |
| 12 | E2E (d) `design_completeness.py` exit 0 | 1 | `[DESIGN-COMPLETE]`·EXIT=0(`logs/d-design-completeness.log`). 매니페스트 `path = ../../docs/solution-design.md` |
| 13 | E2E (e) 구현 1단위 직접 실행 | 1 | `src/report_summary.py` + `tests/test_report_summary.py` 산출, unittest 5건 OK, CLI 2회 출력 동일·EXIT=0(`logs/e-impl-unit.log`). **simulated 라벨** = 수임이 단일 세션 자기 수행이라는 사실을 원장 `at=1 simulation-annotation` 이 기계 판독 가능하게 담는다 |
| 14 | E2E (f) 경량 원장 form-A append | 1 | `runs/w5-e2e-lite/` 필수 7파일 물리화(§5.9 (a)(b)) · `basis` = `<경로>#<프래그먼트>` 2종((d)) · lane 표기 3지점((e)) · 게이트 기록 12필드((f)) |
| 15 | E2E (g) `verify_run.py` findings 0 · exit 0 + 원장 비공집합 | 1 | `status=pass (pass=4 fail=0 skip=1)`·EXIT=0. skip 1 = `plan_schema`(plan 산출 run 아님). 원장 비공집합 = events 15행·revisions 3행·artifacts 4행 |
| 16 | E2E (h) CP2 Pass 원장 실물 | 1 | `cp2-pass` 이벤트 4건(at=3·8·11·14) 실재. 파생 `approvalState` 3전이 = `verified`(설계 문서·구현 단위) → `approved`(밀스톤·CP3 승인 마커) → `user_approved`(초안·사용자 게이트 해소). 선언 원장의 `approvalState` 키 실재 건수 = 0(직접 기입 0·PO-INV 7). `gate_id_for` 미지정 파생 = `['verified']`(게이트 축 파생 의존 증명) |
| 17 | 접점 Write 라이브 차단 1건 | 1 | **실제 Write 도구 호출**로 `<ws>/src/report.schema.json` 시도 → deny 반환(`[LANE-LIGHTWEIGHT] … 접점 클래스 '스키마'(패턴 `**/*.schema.json`)`), 파일 미생성 확인. 단위 테스트 아님 |
| 18 | 임시 마커 정리 · 리포 내 `lane.json` 잔존 0 | 1 | 마커 삭제 확인 · `find . -name lane.json -not -path ./.git/*` 결과 공집합 |
| 19 | 표준 레인 회귀 4스위트 | 1 | 244 passed+13 subtests / 39 / 186 / 22, 각 EXIT=0(`logs/regress-*.log`) |
| 20 | 미해소 전량 열거 | 1 | 아래 §미해소 열거(내용 기록·집계 갈음 0) |
| 21 | 경계 — spec·중립 코드·`gates.py`·호스트·소비 프로젝트 무촉 | 1 | `git status --porcelain` = md 6건 수정 + `runs/w5-e2e-lite/` 신규 1건. `.py`·`.json` 코드/스키마 수정 0, `*/specs/*.md` 수정 0, 소비 프로젝트 경로 0 |
| 22 | 픽스처 워크스페이스를 리포 안에 만들지 않음 | 1 | 워크스페이스 = scratchpad. 리포 안은 경량 원장 run 디렉터리 1건뿐(§5.9 (a)) |

**자체 점검의 한계(정직 표기).** 위 판정은 파일 문면 대조·종료 코드·산출물 실재에 근거하며, **자체 점검은 최종 승인이 아니다** — CP2(Verifier 독립 판정)·CP3(Advisor 승인)이 뒤따른다. E2E 의 게이트 해소·CP2 마커는 이 세션 안의 자기 수행이므로 `simulated` 라벨이 붙어 있고, **실 독립 판정은 이 run 밖에서 나야 한다**.

---

## failures

**없음.** 계획한 산출 7항이 전부 물리화됐고 중단·되돌린 작업은 0건이다.

---

## open_questions

| # | 질문 | 성격 | 좌표 |
|---|---|---|---|
| OQ-1 | 원장 §4 Wave 5 output 3(`docs/session-handoff.md` §A·§B 갱신)은 Advisor 재량으로 이 위임에서 제외됐다 — 갱신 주체·시점 확인 필요 | 비차단 | 위임 문면 「output (Advisor 재량 조정)」 |
| OQ-2 | E2E 가 SD **설계 층 원장**(`solution-design-data/events/maturation-<run-id>/` `MaturationRunStarted` policy 참조)을 남기지 않았다(DV-5). §7A.2-S (S3)의 "기록 없는 시드는 금지" 요구를 픽스처 경로에서 어떻게 충족할지 — 실데이터 트리 오염 없이 남길 위치가 미확정 | 비차단(픽스처 한정) · 실 소비 프로젝트에서는 **차단 요인이 될 수 있다** | `planning/adapters/claude/solution-design-binding.md` §7A.2-S (S3) |
| OQ-3 | 원장 done 5의 "기존 baseline run 을 `verify_run.py` 로 재검증" 은 위임 output 6에서 pytest 4스위트로 대체됐다. 표준 레인 프로덕션 run 재검증은 §5.9 (i) OQ-PO-B7(provenance 표기 2종 어휘 불일치) 때문에 finding 을 낼 것이 예고돼 있다 — 그 재검증을 언제 어느 트랙이 수행할지 | 비차단 | 원장 §4 Wave 5 done 5 · binding §5.9 (i)·§7 OQ-PO-B7 |
| OQ-4 | 트랙 원장(`docs/proportionality-track-ledger.md`) §6.3 항 2·9 · §8.11 항 10 의 상태를 "해소"로 갱신하는 것은 이 위임 output 밖이라 수행하지 않았다 — 원장 갱신 주체 확인 필요 | 비차단 | 원장 §6.3·§8.11 |
| OQ-5 | 경량 레인의 **절감 폭**은 여전히 미측정이다(원장 §7 "성능 주장 부재" 유지). 이 E2E 는 성립을 실증했을 뿐 비용 절감 수치를 내지 않았다 — 측정 축·앵커 확정 필요 | 비차단 | 원장 §7 |

---

## verify_basis

| 축 | 방법 | 범위·한계 |
|---|---|---|
| 문면 개정 5건 | 개정 전후 해당 절 직독 + 데이터 파일과의 값 대조(`entry-registry.json` 행 6 · `default-policy.yaml` `thresholds`) | 개정한 절과 그 인접 상태 문면. 각 문서의 그 밖 절은 정독하지 않았다 |
| 스키마 예시 정정 | 정정 후 `design-manifest.schema.md` 의 `"path":` 키 값 재판독 + `design_completeness` 의 `path` 존재 검사 지점과 `designElements` `pointer` 미검사 확인 | 이 문서 본문 + `design_completeness.py` 2지점. 소비 프로젝트가 이미 복사해 간 구표기 매니페스트는 범위 밖 |
| 경계 무촉 | `git status --porcelain` 전량 판독 | 작업 트리 상태(스테이지 전). 커밋은 하지 않았다(위임 지시) |
| E2E 8지점 | 각 지점 실행 → 로그 파일에 `> log 2>&1; echo "EXIT=$?"` 로 종료 코드 보존(파이프 0) | 픽스처 워크스페이스 1건. **실 소비 프로젝트 적용 0** · **엔진 경유 왕복 0**(경량 레인은 엔진 미구동이 전제) |
| 라이브 차단 | 실제 `Write` 도구 호출 1건 → deny 반환·파일 미생성 확인 | 접점 클래스 「스키마」 1패턴. 나머지 4클래스는 이 주행에서 라이브 검증하지 않았다(W2-a 가 로더 층에서 판정 검증) |
| 원장 검증 | 기존 결정적 러너 `verify_run.py` 재사용(신설 0) + 중립 `derive_registry` 로 파생 등급 산출 | 러너 5축 중 4축 pass·1축 skip. `skip` 은 원장 실재를 증명하지 않으므로 원장 3종 행수 비공집합을 **함께** 확인했다(§5.9 (h) 한계 조항 준수) |
| 회귀 | pytest 4스위트 + 선행 경량 표본 run 재검증 | 위임이 지정한 4스위트 + `lw-w2b-sample-lite`(status=pass). 리포 전 스위트 스윕은 아니다 |

`uaf-verified:` 본 보고의 사실 주장은 위 표의 수단으로 얻었다. **검색 범위** = 개정한 6개 md 의 해당 절 · `lane_resolve.py`/`lane-registry.json`/`pretooluse_lane_guard.py`/`design_completeness.py`/`verify_run.py`/`setup_lite.py`/`artifacts.py` 판독 · 픽스처 워크스페이스 1건 · 경량 run 원장 1건 · pytest 4스위트이며, 그 밖(소비 프로젝트 워킹트리 · `uahf/specs/` 전문 · 표준 레인 프로덕션 run 원장)은 이 보고의 범위 밖이다.

---

## 미해소 열거 (원장 done 6 — 내용 기록 · 집계 갈음 0)

### A. 원장 §6.3 (항 1~10)

1. **표준 레인의 발견 2 — 미해소.** `contract_to_graph.py` `_solution_design_path` 가 SD 입력을 `<project_root>/docs/solution-design.md` 단일 파일로 하드코딩해, 개별 Projection 7~13종을 산출하는 표준 레인과 어긋난다. 이 Wave 는 매니페스트 `path` **표기**만 고쳤고 seed 가정은 무촉이다(코드 diff hunk 0).
2. **발견 1(스키마 예시 `path` 모순) — 해소(본 Wave).** 예시 2종의 `artifacts[].path` 를 `../../docs/<id>.md`(`screen-mock` 은 `../../mocks/index.html`)로 제자리 정정했다.
3. **커버리지 10축의 Policy 데이터화 — 미해소.** 실제 문항 수를 좌우하는 커버리지 축 목록이 `.claude/skills/discovery-interview/SKILL.md` body 하드코딩이라 경량 인터뷰 프로파일은 예산 상한만 낮추고 심문 대상 축 수를 낮추지 못한다(K-6). 좌표 = 메모리 `uaf-coverage-enforcement-gap`.
4. **`userActorClass` 하한 미보호 — 미해소.** 데이터로 `"Advisor"` 치환 시 Advisor 가 사용자 구조 게이트를 해소할 수 있고 floor 로 막혀 있지 않다(K-1·F-13). 이 Wave 는 `gates.py` 를 건드리지 않았다.
5. **경로 상수 중복 정의 — 미해소.** `resolve_gate.py:107-109` 의 `SD_DATA_REL` 과 `pretooluse_design_guard.py:51-52` 가 같은 고정 상대경로를 별도 선언한다(K-5). 한쪽만 바꾸면 게이트와 훅이 갈린다.
6. **floor 테이블 ↔ 컴파일러 target 어휘 불일치 — 미해소.** 컴파일러 기본 정책 target 이 `unitType` 뿐이라 floor 가 발화하지 않는다(K-8·F-15).
7. **SD 스킵 경로 존치/폐기 — 방향 확정·실행 미착수.** 폐기 방향은 2026-07-26 확정됐고 실행은 04 유형 A(버전 상승·사용자 승인) 별 트랙이다. 이 Wave 는 04 spec 무촉이다.
8. **01-entry `§3.2-D` 행 6 `policy` 열 리터럴 "기본" ↔ 데이터 `lightweight` — 존치(Advisor 판정 = 비충돌).** 재심 좌표 = 01 spec 차기 개정 시 policy 열 표기 명확화(유형 A 절차). 이 Wave 는 spec 무촉이므로 갱신하지 않았다.
9. **Wave 5 문서 정합 후보 3건 — 해소(본 Wave).** entry-binding 행 B stale · discovery-binding §8.2 (가) θ 드리프트 · delegation-protocol §4 포인터 표 행 = 3건 모두 반영.
10. **레지스트리 ref 어휘(`lightweight`) ↔ `policyId`(`lightweight-policy`) 형태 이원 — 미해소.** §8.3 (a) ref 해소 규약이 봉합하나 명명 정합 자체는 후속 판단 대상이다.

### B. 원장 §8.11 (항 8~11)

- **항 8** `verifier.md`·`planner.md` 축자 대조 — **해소됨(W3-b)**. 이 Wave 에서 재확인하지 않았다(검사 범위 밖).
- **항 9** 엔진 경로(`logs/invoke-*.json`)와 직접 위임 경로(`reports/*.md`)의 **보고 표면 2종 병존** — 미해소. 이 Wave 의 보고 전문 파일도 트랙 문서 옆(§2.7 2분기의 하네스 측)에 두어 병존을 유지했다.
- **항 10** delegation-protocol §4 포인터 표 보고 파일 행 — **해소(본 Wave)**.
- **항 11** `advisor.md` 상한 미적용 — 미해소. 수임 Agent 3종에만 상한이 걸려 있고 Advisor→사용자 보고 층은 미확정이다(층이 다르다는 판정은 W3-b 가 남겼고 적용 여부는 Advisor·사용자 판단).

### C. 각 Wave 미검증 잔여

- **W1-a** — 실 소비 프로젝트 워크스페이스에서의 시드 실행 미검증. 이 Wave 가 **픽스처 워크스페이스 1건**에서 시드→체커 통과를 실증했으므로 절차 성립은 확인됐으나, 소비 프로젝트 적용은 여전히 0이다.
- **W1-b** — 소비 프로젝트에서의 **엔진 run 경유 실왕복** 미검증. 이 Wave 도 엔진을 구동하지 않았다(경량 레인은 엔진 미구동이 전제이므로 이 축은 표준 레인 트랙 소관이다).
- **W2-a** — 훅 fail-open 4케이스는 W2-a 실측분이며 이 Wave 에서 재현하지 않았다. 라이브 차단은 이 Wave 가 접점 클래스 「스키마」 1건으로 재실증했고, 나머지 4클래스(Contract·게이트·정본 문서·정책 데이터)의 **라이브** 차단은 미실증(로더 층 판정은 W2-a 테스트가 덮는다).
- **W2-b** — 표준 레인 프로덕션 run 재검증 · `resolve_gate.py` 의 `gate-resolution-provenance` 어휘와 러너 화이트리스트의 불일치(OQ-PO-B7) 미해소. 어느 쪽도 이 Wave 에서 수정하지 않았다.
- **W3-a** — `allocation_file` 상대경로 해석 기준(K-7)과 저위험 CP2 저티어 해소의 실 run 관측은 W3-a 소관이며 이 Wave 의 검사 범위 밖이다(재확인 0).
- **W4** — 경량 인터뷰 프로파일이 실제 문항 수를 줄이지 못한다는 한계(§B 항 3과 동일 원인)는 그대로다. 실 인터뷰 세션 문항 수 실측 0.
- **Wave 5(본 Wave) 자체** — ① SD 설계 층 원장 미기록(OQ-2) ② 소비 프로젝트 실적용 0 ③ 경량 레인 절감 폭 미측정(OQ-5) ④ 개정한 md 6종의 **전문** 정독은 하지 않았다(개정 절과 인접 문면만) ⑤ 커밋 미수행(위임 지시 — Advisor 검증 후).
