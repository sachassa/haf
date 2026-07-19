# 세션 핸드오프 (UAF 레벨 정본 · 단일 live 문서)

작성: Advisor · 2026-07-17 (직전 상태 앵커: Performance Tuning Track 종료 2026-07-14)
용도: 새 세션은 **본 파일 하나로 상태를 인수**한다. 원문 전체 정독 강제 없음 — demand-driven(§단위·필요 시점) 규칙을 따른다. (물리 발화 = `/uaf-continue`)
지위: `docs/artifact-lifecycle-policy.md` §6이 정한 **UAF 레벨 단일 live 핸드오프**다. 단수·제자리 갱신이며 버전별 파일을 만들지 않는다. 과거 상태는 git 이력이 정본이다. (전신: `docs/next-session-prompt.md` — 본 파일로 개명·재정착 2026-07-17)

> **🔴 갱신 2026-07-19 — §DC-1 코어 강제 = 완결** (branch `feat/dc1-design-completeness`·미머지·미푸시). Wave 1-4로 백엔드 직행 차단 실증: SP-INV 9(코어 04)+필수 산출물 10종(어댑터 정책)+엔진 게이트(`resolve_gate` fail-closed·프레임워크 무수정). 각 Wave CP2 독립검증(테스트 재실행)·CP3 승인. 커밋 `08a3321`(설계+정책)·`8e1f18d`(실행코드). tms 실선언(3접점+연계)으로 필수 10종 미산출 차단 실증. **+책임 있는 자율 원칙**(ARCH §6 원칙11·CLAUDE.md — 필수=Core/Policy 강제·자율=기본값+이탈 사유기록·이탈=게이트 일괄 표면화; "비정본이 항상 문제" 근본 대응·메모리 `uaf-accountable-autonomy-principle`). **+Wave 5-A 생산 프로토콜**(정책·바인딩 §7A·부록 — 역할 구성[PM 커버리지 바닥+기획·아키텍처 기본+디자이너·DBA 조건부]·역할→산출물 소유 맵 1:1·위임 산출·MD 본문+JSON 매니페스트·docs 배치·CP1-3+Validating 게이트 컨펌). 원칙·Wave 5-A 각 CP2/CP3. **잔여:** Wave 5-B(생산 물리 배선·서브에이전트 브리프 템플릿·form-B)·PreToolUse 훅(후순위)·§DC-5/6/7/9 백로그(§DC-8 완결 2026-07-19 — 비정본 승격 불필요·접점 제외 표면화 옵션 b 해소·옵션 a 잔여)·tms 실제 10종 설계 산출(별도 제품 트랙). 상세 정본 = 메모리 `uaf-design-completeness-gap`. 이하 §DC-1~9는 원 백로그 기록(§DC-1~4 코어 반영 완료). 이하 §1~§5는 직전 상태(Performance Tuning·산출물 수명).

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

### §DC-3 강제 시점·메커니즘 (검토 세션 추천)
- **시점 = 구현 착수 직전(설계→구현 경계·UAHF 넘기기 전).** 오케스트레이션 종료 시점 아님(다 짓고 검사는 늦음).
- **주 장치 = 엔진 게이트:** `contract_to_graph.py`가 접점 선언 시 design/UI-UX 단위를 impl 단위 **앞에** 필수 삽입 + design-completeness 게이트(통과·승인 전 impl ready 금지).
- **백스톱 = 차단형 훅:** 필수 산출물 없으면 `src/` Write 거부(PreToolUse류). 현 훅은 알림형(SessionStart)뿐 → 차단형 신설 필요(`.claude/settings.json`·`.claude/hooks/` 실재).
- **왜 둘 다:** 게이트=의미·승인(내용), 훅=존재 최후방어(그래프 오류로 새도 막음). 존재≠완성이므로 훅 단독 불충분.

### §DC-4 UI/UX 단계 신설
- 접점(웹·앱·포털)이 선언된 프로젝트는 UI/UX 설계 필수 단계. 현재 완전 부재.

### §DC-5~9 나머지 백로그 (전부 수정 대상)
- **§DC-5 SD 협업 깊이:** 이번 04 = 단일 라운드·병렬 블라인드(전문가 서로 안 봄). 04 프로토콜 T5/T7 다라운드 미활용 → 전문가가 서로 안에 반응·수렴하도록 심화. 인터뷰 깊이(자율→너무 짧음) 보완 연계.
- **§DC-6 역할 상한 정책:** Expert Role 상한 3 = 정책 기본값(`.claude/solution-design/policy/`·configurable)·고정 아님. 복잡 프로젝트 상향·역할 추가(UX·보안규제·데이터모델). 최소할당 vs 완성도 균형 재검토.
- **§DC-7 WBS 소유 문서화:** 관리=오케스트레이션 엔진 · 초안(분해)=Planner 역할 · 실행=Worker (혼동 방지 명문화).
- **§DC-8 [완결 2026-07-19] 비정본 전수 스윕 (책임 있는 자율 원칙 적용):** 부록 4종·spec 04/05/02·runtime 4종(lifecycle·module-registry 포함)·전역 exhaustiveness를 4갈래 병렬 감사(원칙 (a) 테스트) → **비정본 승격 불필요 결론.** 강제-필요분은 DC-1이 이미 정리, 나머지 방대한 비정본은 정당 자율(SP-INV 5·UAF-INV ⑥가 카탈로그의 비정본 유지를 *강제* — 승격 시 오히려 불변 위반). 감사자가 올린 유일 후보(04 §3.9 Visual Contract)는 Advisor가 policy 실값 대조로 **정정** — 시각 산출물 3종(화면목록·메뉴·화면설계서)이 이미 `touchpoint`-required이고 §3.9는 협의 *방법론*이라 SP-INV 5상 정당 비정본.
  - **발견된 유일 실질 갭(스코프 밖 인접·해소):** 접점 **과소선언** + silent autoExclude. SP-INV 9는 *선언된* 범위만 강제하는데 접점을 선언하도록 강제하는 필드가 03에 없어(03 §3.2 필수 코어 필드 9종에 접점 부재), 접점 미선언 시 UI/UX 클래스가 **사용자 확인 없이 조용히** 제외(DC-1 증상이 다른 문으로 재발). Discovery 인터뷰 Skill은 전달 플랫폼을 elicit하나 `replaceable`이라 코어 보증 아님.
  - **옵션 (b) 해소(본 커밋·사용자 결정 2026-07-19):** `design_completeness.py`가 접점/연계 미선언으로 클래스 전체 제외 시 매니페스트 `classExclusions.<class>{reason,confirmedBy}` 확인을 요구(없으면 차단) — 고임팩트 이탈 표면화(원칙 (c)). policy `classExclusionOnNonDeclaration`·바인딩 §7.2/§7A.4·`design-manifest.schema.md`·테스트. **CP2 강제 실증**(BAD exit2·OK exit0·PARTIAL per-class 차단)·pytest 49·**CP3 승인**. 03·04 spec 무변경·SP-INV 5 보존·코어 무수정.
  - **잔여(백로그):** 옵션 (a) 03 필수 코어 필드에 접점 구조 필드 추가(결정적 검출·거버넌스 무게 큼) · runtime 관찰 1건(`replaceable=false` 근거 게이트 표면화 부재·저임팩트). 상세 = 메모리 `uaf-design-completeness-gap`·`uaf-accountable-autonomy-principle`.
- **§DC-9 05 wiring 후속:** OQ-PO-B5(actor 재검증)·OQ-PO-B1(게이트 렌더)·Stage B 실코드 산출 → `uaf-orchestration-wiring-gap` 메모리.

### §DC 좌표·정본 포인터 (착수용)
| 항목 | 위치 |
|---|---|
| 실측 산출물(백엔드만) | `tms-system/impl-plan.json` |
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

- **Interview Entry-to-Runtime Audit** (사용자 지정 2026-07-14). 정의·범위·성공 기준은 착수 세션에서 사용자 지시로 확정한다 — 본 파일은 명칭과 시작점만 기록하며 범위를 추정하지 않는다.
- 착수 시 최소 read-set: 본 §1 앵커 + 착수 세션의 사용자 지시. 관련 정본은 필요 §만 demand-driven(후보 포인터: `entry/specs/01-entry.md`·`discovery`/`orchestration` specs — 실제 선택은 지시 범위 확정 후).

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
