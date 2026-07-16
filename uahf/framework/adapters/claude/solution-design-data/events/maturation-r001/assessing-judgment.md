# Assessing 판정 기록 — maturation-r001 (pc-uahf-001 v1 성숙 run)

기록: 주 세션(Advisor) Orchestrator 규약 절차 · 2026-07-13 · solution-design-binding §6.1
성격: 성숙 실행 메타(코어 밖 — SP-INV 2·3). Contract 코어 필드로 유입되지 않는다.

## 1. 입력 결속

- 입력 인스턴스: `framework/adapters/claude/discovery-data/contracts/uahf/project-contract.v1.md` — pc-uahf-001 · instanceVersion 1 · 종단 `Ready`(사용자 승인 2026-07-07, G2 seq 28) — **SP-INV 1 충족**(Ready 종단 실측).
- 적용 Policy: `solution-design-data/policy/default-policy.yaml` (default-policy — solution-design-binding §7.2 정본 값).

## 2. 복잡도 판정 (policy (가) 신호 대조 — v1 front-matter 직접 실측)

| # | 신호 | 실측 | 판정 |
|---|---|---|---|
| 1 | `architectureDirection.open` 비공집합 | **2건 실재** — 형태 B 실행 호스팅 경계 분할(OQ-M5-2 외 4건)·UAHF 측 Contract 정식 등재(03 §3.5-C) | 충족 |
| 2 | `readiness.openQuestions` 비공집합 | **3건 실재** — 형태 B 착수 시점·이월 개정 일괄 처리 시점·정식 등재 채택 여부 | 충족 |
| 3 | `assumptionLedger` 비공집합 | **공집합**(빈 원장 — Ready 허용) | 미충족(신호 아님) |
| 4 | 다관심사 지표 | **충족** — (i) 아키텍처/파이프라인(v1 이후 확정 결정 미반영: v1.2.1 Layer 재구성·Solution Design 성숙 루프 신설·루트 문서버전 v1.4) (ii) 거버넌스/정합(요구 라벨 결함 의심·리스크 문면·이월 부채) 2관심사 교차 | 충족 |

**판정 = 성숙 필요** (신호 1·2·4 충족 — 스킵 규칙 불성립). 이진 분기 산출: `성숙 필요` → 역할 할당(04 §3.3) 후 T1 `Proposing` 진입.

## 3. 역할 할당 (policy (나) — 관심사 파생·최소 할당)

식별 관심사 2 → 역할 2 (관심사당 1 · 상한 3 이내 · SP-INV 8). 역할명은 이 run의 개방 네임스페이스 선언이며 표준·카탈로그가 아니다.

| roleId | capability (끌어올리는 설계 관심사) | inputContract | outputContract |
|---|---|---|---|
| `arch-pipeline` | 파이프라인 구조·Layer 배치·architectureDirection 미결(open) 해소 방향에 대한 설계 결정 | v1 인스턴스·v1 이후 확정 결정 집합(저장소 실측)·잔여 미결 | 해당 관심사의 v2 delta Proposal (`proposal-arch-pipeline.md`) |
| `governance-consistency` | 요구·리스크·정합 부채·라벨 정확성에 대한 설계 결정 | v1 인스턴스·대상 spec 실측(라벨 검증)·이월 인벤토리 | 해당 관심사의 v2 delta Proposal (`proposal-governance-consistency.md`) |

- 호스팅: 기존 위임 실행 관행 재사용(solution-design-binding §6.1) — 새 병렬 실행 프레임워크 0.
- Projection 예비 관찰(확정은 Reviewing·게이트): 대상 워크스페이스에 ARCHITECTURE·ROADMAP 등 해당 유형 정본이 이미 실재 → policy (다) existingCanonical상 신규 Projection 강제 0 예상.
