# 다음 세션 부트스트랩 프롬프트 (Performance Tuning Track — T0 완료·T1 착수)

작성: Advisor · 2026-07-14 · T0 Baseline Freeze 완료 시점
용도: 새 세션에서 아래를 붙여넣으면 **추가 재조사 없이** T1부터 착수. (물리 발화 = `/uaf-continue`)
상태: **v1.7 완결(Baseline `ad451ee`/`dd2fd73`) → Performance Tuning Track 진행 중 — T0 Baseline Freeze 완료(커밋 `013e532`·사용자 승인 2026-07-14). 다음 = T1 Minimal Telemetry.**

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

현재 트랙: Performance Tuning (v1.7 Dogfooding Baseline 기반). T0 완료 — 지금부터
T1 Minimal Telemetry를 시작하라.

■ 정본 문서 3종 (역할 혼동 금지 — 먼저 정독)
- docs/baseline-performance-cost-analysis.md — 1차 실측(역사 기록·무수정 보존).
  "무엇이 발생했는가". 핵심 수치: 경과 ≈10.8h(야간 게이트 5.45h)·능동 ≈5.3h·
  CLI 37세션 93.3min $24.15·cacheRead 28.0M·게이트 재검증 9세션 $4.51(18.7%).
- docs/performance-tuning-plan.md — **튜닝 정본**(T0~T7·구현 순서·항목별 10필드).
  "무엇을 튜닝하는가".
- docs/post-tuning-improvement-backlog.md — 이후 개선(A~G + 실사용 Dogfooding
  Evidence 7건 + Post-Tuning 우선순위 B+C→D→G→A+F→E). 이번 트랙 혼입 금지.

■ Baseline Freeze 상태 (T0 완료 — 재수행 불요)
- 앵커: UAHF ad451ee · consumer(uahf-control-plane) dd2fd73. Freeze 커밋 013e532.
- Baseline run evidence(orch-k/m/w·maturation-r003·greenfield-r003)는 immutable —
  신규 실험은 반드시 신규 runId.
- consumer 워킹트리에 사용자 변경분 3건+check-error.js가 **미커밋 보존** 상태
  (사용자 방침: 이번 트랙 무수정·미커밋 유지 — Dogfooding Evidence·백로그 기록됨).
  Control Plane 결과물 수정 금지.

■ 상시 원칙 (전 Wave 적용)
- 시간 3지표 분리: A Total Elapsed / B Active Processing / C User Gate Waiting.
  Gate Notification(T5)의 C 개선을 B 개선으로 보고 금지.
- Measurement First: 느낌 판단 금지 — 한 변경 → 측정 → 다음 변경.
- Reuse First: 신규 도구 전 기존 자산 조사(내부 자산 → 설치된 CLI → Skill →
  오픈소스 → 얇은 Adapter → 최후 신규). 기확인 재사용 후보: replay_k.py·
  validate_stage_plan/validate_impl_plan·validate_revision/fold·pytest 165·
  python stdlib·git porcelain.
- 품질 불변: Worker/Verifier 독립성·fresh-context 경계·사용자 게이트·append-only·
  provenance·완료 보고 불신·High-risk 의미 검증 유지. 최적화 대상은 중복 재검증·
  결정적 작업의 LLM 사용·과도 모델·전체 context 재로딩·문면 중복뿐.
- 사용자 설명 방식: ①지금 무엇을 ②왜 ③무엇이 바뀌나 ④추천 ⑤사용자 결정 사항 —
  내부 용어는 [기술 상세]로 분리.
- Wave 절차: Baseline→Reuse Assessment→최소 변경→독립 검증(CP2)→측정→
  Before/After→다음. **CP2 통과 후 커밋**(L-28 후보).

■ T1 Minimal Telemetry — 지금 할 일 (정본 = tuning plan §T1)
목표: 신규 시스템 없이 기존 evidence 집계로 측정 기반 확보.
1. 집계 스크립트 1개(orchestration-data/e2e/ 격리 지점·순수 판독):
   invoke 로그·stop-signal/resolution mtime·git 타임스탬프 → run-metrics.json
   (지표: elapsed/active/gate-wait 3분리·critical path·세션 수[전체/fresh/모델별]·
   모델별 토큰/비용·검증 시간/비용[결정적 vs 의미론]·CP2 수·게이트 재검증 수·
   cache r/w·retry 수·ready_set 동시성).
2. done 기준: Baseline 3 run(k/m/w)에 실행해 1차 분석 수치를 재산출·대조
   (일치 = 산식 고정 성공). 원장 무수정·L-09(벽시계는 순서 값과 분리) 준수.
3. 최소 보완 1건: stop-signal.json 덮어쓰기로 다중 게이트 run의 선행 게이트
   정지 시각 소실(실측: m 구조 게이트) — 위상 번호 파일(stop-signal-<n>.json)
   또는 append 방식, 러너/드라이버(격리 지점) 수준 우선·중립 코드 무촉 옵션 검토.
4. 하네스 서브에이전트 수치(토큰/시간)는 완료 통지 실측치를 트랙 마감 시
   metrics 파일에 절차적으로 전사(시스템 신설 금지).
5. CP2 독립 검증(결정적 검사 우선 적용의 첫 자기 적용 사례) → 커밋.

■ 이후 순서 (tuning plan §5 — T1 완료 후 순차)
T2 Review 재검증→유효 CP2 evidence 재사용(stale 규칙 3종: retry/supersede·revision/
artifact 해시 — 첫 적용 Shadow 대조) → T3 Verification Architecture(Reuse Assessment
→Deterministic/Semantic 분리→Risk-based Model Routing+Shadow — "CP2=haiku 고정" 금지)
→ T4 Context Payload(delegation 참조형 표준화[T3 웨이브 탑재 가능 — 재시도 +341s·
$1.87의 직접 원인 실증]·역할별 payload 차등·Minimal Default+On-demand+Full
Availability) → T5 Gate Notification(그룹 B·Port/Adapter — Telegram 하드코딩 금지·
측정 분리) → T6 동형 Benchmark(신규 runId) → T7 Before/After(3지표 병기) →
T8 Concurrency 재평가(ready_set 데이터 근거) → Post-Tuning Track.

■ 금지 (이번 트랙)
Post-Tuning 기능 구현·Control Plane 수정(오류 수정 포함)·Visual Contract 구현·
외부 capability 설치·Execution Mode·대형 telemetry 시스템·측정 전 다중 튜닝
동시 적용·품질 생략식 고속화·Baseline evidence 수정.

■ Consult
- UAHF 자신 Contract = discovery-data/contracts/uahf/project-contract.v3.md.
- Memory: L-28 후보(CP2 후 커밋)·BPD-23 후보(소비 프로젝트 풀 파이프라인)·
  mi-0107~0110(v1.7 마감 등록·store 110).
```

---

## 정본 포인터

| 항목 | 위치 |
|---|---|
| 튜닝 정본 | `docs/performance-tuning-plan.md` (T0~T7) |
| 1차 실측(불변) | `docs/baseline-performance-cost-analysis.md` |
| 백로그(+실사용 Evidence 7건) | `docs/post-tuning-improvement-backlog.md` |
| Baseline 앵커 | UAHF `ad451ee` · consumer `dd2fd73` · Freeze `013e532` |
| Baseline run evidence (immutable) | `orchestration-data/runs/{orch-k-nonfixture-smoke,orch-m-maturation-cp,orch-w-impl-cp}/` · `solution-design-data/events/maturation-r003/` · `discovery-data/events/greenfield-r003/` |
| 재사용 검증 자산 | `orchestration-data/e2e/{replay_k.py,resolve_m.py,resolve_w.py}`(validate_*)·중립 `revision.py`(validate_revision/fold)·pytest 165 |
| v1.7 트랙 기록 | 직전 핸드오프 내용은 git `ad451ee`의 본 파일 이력 참조 |
