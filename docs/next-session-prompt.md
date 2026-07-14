# 다음 세션 상태 앵커 + 부트스트랩 (Performance Tuning Track)

작성: Advisor · 2026-07-14 · Core Tuning 마감 시점(T6/T7 = 사용자 승인 대기)
용도: 새 세션은 **본 파일 하나로 상태를 인수**한다. 원문 전체 정독 강제 없음 — §2 최소 read-set·demand-driven 규칙을 따른다. (물리 발화 = `/uaf-continue`)

## §1. 상태 앵커 (git log 대조 가능)

- 활성 트랙: **Performance Tuning** (v1.7 Dogfooding Baseline 기반).
- 완료 단계·커밋:

| 단계 | 커밋 | 요지 |
|---|---|---|
| T0 Baseline Freeze | `013e532` | 앵커 동결(아래 Baseline 앵커) |
| T1 Minimal Telemetry | `d9b2ac6` | collect_metrics.py·산식 고정·stop-signal 위상 아카이브 |
| T2 Review 게이트 evidence 재사용 | `f47ce91` | 재검증 세션 소비 대체·stale 3규칙 fail-closed |
| T3+T4-① 검증 아키텍처·delegation 참조형 | `891e9aa` | verify_run.py(LLM 0)·Risk Routing 배선·섀도 장치(기본 off)·sentinel 표준 |
| T3-② cp2ModelSlots 스키마 등재 | `adaafe9` | 위험도별 CP2 모델 차등 활성화(dormant 해소) |
| T1-② payload 계측 + R3 러너 | `e1147c4` | bundle_payload 지표(baseline 343,183B/37세션)·run_all_tests.py |

- **다음 단계 = 동형 벤치마크 → Before/After 분석(plan §4 항목 T6 = §5 순서 6·7) — 사용자 승인 후에만 착수.**
- T5 Gate Notification = 보류(그룹 B·C지표 전용 — Operational UX 트랙 후보·백로그 유지). Concurrency 재평가(plan §4 항목 T7 = §5 순서 8)는 벤치마크 데이터 이후.
- 번호 표기 주의: plan §4 항목-ID는 T0~T7(T6이 벤치마크+Before/After 통합·T7이 Concurrency), §5 순서 번호는 0~9. 본 파일은 두 체계를 항상 병기한다 — "T8"은 §4 항목-ID에 존재하지 않는다.
- Baseline 앵커(불변): UAHF `ad451ee` · consumer `dd2fd73` · Freeze `013e532`. Baseline run evidence(orch-k/m/w·maturation-r003·greenfield-r003) immutable — 신규 실험은 반드시 신규 runId.
- consumer(`uahf-control-plane`) 워킹트리: 사용자 변경분 미커밋 보존 — 수정 금지.

## §2. 착수 최소 read-set (demand-driven — 전문 정독 강제 없음)

원칙: **존재·버전·포인터 먼저, 원문은 필요한 §만 그때 읽는다.** 아래 외 문서는 필요가 생길 때만 연다.

- 벤치마크 착수 시: `docs/performance-tuning-plan.md` **§4 T6 항목·§5(순서)만** + `orchestration-data/e2e/README.md`(러너·collect_metrics·verify_run 사용법) + `e2e/policy/README.md`(allocation 배선·opt-in).
- Before/After 분석 시: `docs/baseline-performance-cost-analysis.md` **§2(수치)·§15(산식)만** + `e2e/metrics/aggregate.run-metrics.json`(bundle_payload 포함).
- 필요 시에만: Contract v3(`discovery-data/contracts/uahf/project-contract.v3.md` — 프로젝트 정의 확인 필요 시)·백로그(`docs/post-tuning-improvement-backlog.md` — Post-Tuning 착수 시).
- Memory Consult: `memory-binding.md` §3.2 (index-first·최소 범위).

## §3. T6 설계 노트 (확정 위생 사항)

- 신규 runId·동형 워크로드·**workspace_dir는 저장소 밖**(orch-k/w 선례 — spawn 세션의 harness .claude 상속·cacheWrite 오염 방지).
- allocation.json 배선(opt-in)·Task model 슬롯 비움 → 위험도별 Worker 라우팅 + CP2 차등(cp2ModelSlots) 실측. 섀도 기동 여부는 T6 설계에서 확정.
- 측정 도구: `run_all_tests.py`(개발 검증)·`collect_metrics.py`(bundle_payload 포함)·`verify_run.py`(결정적 축·LLM 0).
- 상시 원칙은 **tuning plan §1~§3이 정본**(재정의 0): 3지표 분리(A Elapsed/B Active/C Gate-wait)·Measurement First(한 변경→측정→다음)·Reuse First·품질 불변(CP2 상시·독립성·fail-closed)·측정 전 다중 튜닝 동시 적용 금지·Baseline evidence 무수정.

## §4. 갱신 규율 (stale 재발 방지)

- **각 단계 완료 커밋에 본 파일 §1 상태 앵커 갱신을 포함한다.** (근거: T1~T4 기간 본 파일이 미갱신되어 3단계 stale — 세션마다 Memory·git log로 상태를 재도출하는 비용이 발생했다. 이번 재작성이 그 정정이며, 이 규율이 재발 방지 장치다.)
- 본 파일은 값 중복 최소·정본 포인터 우선. 본 파일과 정본이 충돌하면 정본(tuning plan·git log)이 우선한다.

## 정본 포인터

| 항목 | 위치 |
|---|---|
| 튜닝 정본 (§4 항목 T0~T7·§5 순서 0~9·항목별 10필드) | `docs/performance-tuning-plan.md` |
| 1차 실측 (역사·불변) | `docs/baseline-performance-cost-analysis.md` |
| 백로그 (Post-Tuning A~G·우선순위 B+C→D→G→A+F→E) | `docs/post-tuning-improvement-backlog.md` |
| Baseline run evidence (immutable) | `orchestration-data/runs/{orch-k-nonfixture-smoke,orch-m-maturation-cp,orch-w-impl-cp}/` · `solution-design-data/events/maturation-r003/` · `discovery-data/events/greenfield-r003/` |
| 측정·검증 도구 | `orchestration-data/e2e/{run_all_tests.py,collect_metrics.py,verify_run.py,delegation_check.py}` |
| Risk Routing 정책 | `orchestration-data/e2e/policy/{allocation.json,README.md}` |
| UAHF Contract | `discovery-data/contracts/uahf/project-contract.v3.md` |
| 직전 핸드오프 이력 | git `e1147c4` 이전의 본 파일 이력 참조 |
