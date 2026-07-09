# UAHF Session Handoff — v0.3 → v0.4

작성일: 2026-07-05
작성자: Advisor (v0.3 세션)
목적: 이 문서만 읽어도 새 세션이 v0.4를 이어갈 수 있게 한다. (이전 기록: docs/session-handoff-v0.2.md, v0.1)

---

# 1. 이번 세션 요약

## 1.1 완료한 작업 (ROADMAP v0.3 — Runtime & Core Kernel)

1. **Execution Plan 수립** — Planner에게 구현 형태 비교안(형태 A 규격 문서+스키마 vs 형태 B 실행 코드) 위임 → Advisor 검토 → 사용자 승인: **형태 A + B-호환 보강 2건** (보강 1: 언어 중립 인터페이스 시그니처 포함, 보강 2: DP-4 예약) + 추가 조건 4건(C-1~C-4, §1.3).
2. **Wave 실행 (A1~A8, 8 Task · 5 Wave)** — 디렉터리 구조 규격(A1) → 병렬 3종: Manifest·Registry / Config 스키마 / 수명주기(A2·A3·A4) → 병렬 2종: Claude Adapter 바인딩 / 시연 절차서(A5·A6) → 시연 수행(A7) → Verifier 독립 검증(A8). 위임·검증은 v0.2 확립 관행(delegation-protocol / verification-checklist 게이트 A~D) 그대로 수행.
3. **시연 3종 완주** — 단독 기동(Bootstrap→Degraded, INV-2) / 모듈 교체(동일 contract Replace, 소비자 참조 변경 0 — SHA256 대조, INV-1) / Config 병합(Module>Project>Global, 결정성, INV-5). 실물 파일 연산 기반 규약 실현(형태 A), Verifier가 실측·재계산으로 재검증.
4. **검증 리포트** — docs/v0.3-verification-report.md: 항목 판정 18건, VT-4 전수 스캔(후보 4부류), 거짓 완료 검출 절차, DP-2 근거 대조표. 최초 Fail(위반 2) → r3 재작업 → **최종 Pass (충족 18/위반 0/판정 불가 0)**.

## 1.2 v0.3 완료 조건 대조 (ROADMAP)

| 완료 조건 | 판정 | 근거 |
|---|---|---|
| 모듈 단독 사용·교체 시연 (Modular 검증) | 충족 | 검증 리포트 items #2·#6·#7 — 시연 ①·② 실물 재검·도출 재계산 |
| Core 디렉터리에 Claude 의존 요소 0건 | 충족 | items #3·#8·#13 — VT-4 전수 스캔 (AI+언어·툴체인·형식, C-3 확장 범위) |
| config 스키마가 스펙과 일치 | 충족 | items #4·#9 — 01 §3.2-B 셀 단위 대조 + 병합 도출 독립 재계산 |
| Verifier 검증 통과 | 충족 | final_verdict = Pass (재작업 1회 후), CP3 승인, 사용자 승인 2026-07-05 |

specs/01 §7 완료 기준 5건(단독/교체/Core AI 비의존/Config 일치/경계 INV-6)도 전건 충족 (items #6~#10).

## 1.3 이번 세션의 설계 결정 (전부 확정, 근거 기록)

| 결정 | 내용 | 주체 |
|---|---|---|
| DP-0: 구현 형태 | 형태 A(규격 문서+스키마) + B-호환 보강 2건. Planner 비교안(§4 매트릭스 a~g) 근거 — 가역성 비대칭(A⊂B), Spec First(01 §4.1 하이브리드 바인딩), 크리티컬 패스 | 사용자 (Option 1 승인) |
| 사용자 조건 C-1~C-4 | C-1: A→B 전환 시 Core Contract 변경 0 / C-2: 실행 코드는 Runtime·Adapter Layer에만, core/는 문서 전용 / C-3: Core는 AI+언어·툴체인 비의존 / C-4: 형태 B 착수는 DP-4 재검토 | 사용자 |
| **DP-1: 재시도 한도** (03 §3.1-B 승계 보류 해소) | 추상 키 `retry.limit`, **기본값 2**, Global 스코프 기본 + Project/Module override. 근거: v0.1·v0.2 실측 재작업 전건 1회 해소. 기록: config-schema.md §7 | Advisor 결정 + 사용자 재가 |
| SchemaViolation 대조 스키마 출처 | Module scope 값 → 대상 Manifest configSchema(부재 시 구조 규칙) / Global·Project → Module 네임스페이스 키면 그 configSchema, Framework 수준 키는 구조 규칙. 01 침묵 지점의 운용 해석(계약 확장 아님). 기록: config-schema.md §5 주 | Advisor (A3 open_question 해소) |
| **DP-2: 하네스 전이 조건 2** (13 §3.2-B) | **미충족 — Bootstrap 상태 유지.** 구조·계약·경계는 확정되었으나 실행 Module 구성(형태 B) 미도입. 근거 대조표: 검증 리포트 §7 (S1~S5 / N1~N5). Formal 전이는 로드맵대로 v0.9 사안 | Advisor 재량 + 사용자 동의 |
| **DP-4: 형태 B 착수 여부** | 유보 — 지금 착수하지 않고 ROADMAP 트랙(v0.4∥v0.5∥v0.8)으로 진행. **v0.9 전후 재상정.** B-호환 시그니처로 전환 비용 0 유지 | 사용자 동의 |
| DP-3: 형태 B 언어 선택 | 계속 유보 — DP-4에서 형태 B 착수 결정 시에만 상정 | (미결 — 정상) |
| `<adapter>` 구체화 | structure.md의 일반형 `<adapter>` = `claude`로 확정. 구체 어댑터명·환경 토큰은 framework/adapters/claude/에만 존재 (mention/use 격리 완성) | Advisor (A5 채택) |
| framework/ 문서 관례 | 머리에 작성일·근거 정본·거버넌스 + §9 이력 절(문서 머리, append-only). docs/ v0.3 산출물도 동형 | Advisor (A1 재량 수용 후 표준화) |

## 1.4 검증 결과 (검증 게이트 실동작 기록)

- 위임 총 8회 (Planner 1 · Worker 6 · Verifier 1) + 재검증 라우팅 2회(기존 에이전트 재개). 거짓 완료 보고 0건.
- **CP2 Fail → 재작업 → Pass 2건:**
  1. **A5 (runtime-binding.md)**: `~/.claude/CLAUDE.md`를 "소스 실재"로 서술했으나 실제 미존재 — Advisor 게이트 C의 파일 시스템 전수 대조가 검출 (v0.1 실검출 유형 §5.3 재발). 재작업에서 Worker가 전수 대조를 실제 수행해 **지시 범위 밖 동종 결함(`.claude/settings.json` 미존재) 1건을 자가 검출·교정·공개** (모범 사례).
  2. **A8 (config-schema.md r2)**: **Verifier가 Advisor 자신의 개정 잔여 결함을 검출** — r2에서 §7 표·결정 기록만 갱신하고 §1·§7 서두·§10의 "미결정" 서술 3곳과 실재하지 않는 "§Open Questions" 참조 1곳을 방치 → Fail. Advisor r3 교정 → 재검증 Pass. **검증 게이트가 Advisor의 오류까지 걸러낸 첫 사례** — 독립 판정(CP2)의 존재 이유 실증.
- Advisor 게이트 C 검증에서 부수 발견: 어느 완료 보고에도 없는 빈 디렉터리 8개(framework 모듈 5종 + .claude 확장 3종) 생성 확인 (생성 시각 클러스터는 A1 수행 구간과 겹침, 주체 단정 없음 — Lesson 후보 1).

## 1.5 Lesson 후보 (v0.4 Memory/Lessons 구현 시 정식 기록 대상 — v0.1·v0.2 후보와 합산)

1. **부수 산출 미보고** — 완료 보고 artifacts에는 파일뿐 아니라 생성한 디렉터리(빈 디렉터리 포함)도 명시한다. 미보고 부수 산출은 소유 경계(R4) 추적을 흐린다.
2. **부분 개정 잔여** — 문서의 한 §만 갱신하면 같은 상태를 서술하는 다른 §(목적·요약·말미 주)에 낡은 서술이 잔존한다. 개정 시 해당 상태를 서술하는 **전 지점을 전수 열거·갱신·대조**한다. (Advisor r2가 이 결함을 만들었고 Verifier가 검출)
3. **상태 서술은 실측 후 기록** — "실재/존재" 주장은 파일 시스템 확인 후에만 기입한다. 지원되나 미존재인 소스는 "지원 소스 — 현 시점 미존재"로 구분 표기한다.
4. **위임 done 문구 정밀도** — "문서 머리에 이력 절" 같은 모호한 표현은 수임자마다 다르게 해석된다(A1 사례). 배치·형식까지 정밀 지정하거나, 기존 문서 관례를 명시 참조시킨다.

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- v0.1·v0.2 완료(기준선). **v0.3 완료 — 사용자 승인으로 공식 기준선 확정 (2026-07-05).** 다음: v0.4.
- 승인 근거: Verifier 독립 판정 Pass(충족 18/위반 0) + CP3 Advisor 승인 + 사용자가 Runtime/Core 책임 분리·Spec 일치·AI Agnostic 유지·독립 검증 통과·handoff 정리를 확인 후 승인.

## 2.2 산출물 상태 (전부 v0.3 Baseline — 사용자 승인 2026-07-05, 각 문서 이력에 기록)

| 파일 | 내용 | 비고 |
|---|---|---|
| `framework/core/structure.md` | 디렉터리 구조 규격 (3경계·C-1~C-3 명문화·산출물 표) | Core 문서 |
| `framework/core/config-schema.md` | Config 스키마 (3스코프·병합·DP-1 해소 기록) | r3 — 개정 3회 이력 |
| `framework/runtime/module-manifest.md` | Manifest 7필드 인스턴스 + 작성 지침 + 시그니처 | Core 문서 |
| `framework/runtime/module-registry.md` | 4연산 운용 규칙 + 절차 규칙 + reason 코드 | Core 문서 |
| `framework/runtime/lifecycle.md` | Bootstrap/Shutdown·Runtime Context·Serve 경계(INV-6) | Core 문서 |
| `framework/adapters/claude/runtime-binding.md` | 01 §4.1 10행 매핑·교체 지점 1~7·구체 토큰 격리 | r2 — CP2 재작업 1회 |
| `docs/v0.3-demo-procedure.md` | 시연 3종 절차·판정 문장·기록 포맷 | |
| `docs/v0.3-demo.md` | 시연 수행 기록 (실물 관측·해시·재병합) | |
| `docs/v0.3-verification-report.md` | A8 검증 리포트 + DP-2 근거 대조표 | Fail→Pass 이력 보존 |
| Frozen specs 15개, ARCHITECTURE.md(0.2), ROADMAP.md, v0.2 산출물 | 무변경 | |
| `framework/{loop,memory,verifier,workflow,plugins}/` | 빈 디렉터리 (v0.4~v0.8 실현 경계) | §1.4 부수 발견 |

## 2.3 하네스 상태

**Bootstrap 유지** (13 §3.2-B — DP-2 판정, 사용자 동의 2026-07-05). 전이 조건 1 충족(v0.2). **조건 2는 진전·미충족**: 구조·계약·경계·바인딩은 확정(검증 리포트 §7 S1~S5), 실행 Module 구성은 미도입(N1~N5). 조건 3~4와 Formal 전이는 v0.9에서 다룬다.

---

# 3. 다음 세션에서 수행할 작업 (v0.4 — Memory & Lessons, Track A)

## 3.1 목표 (ROADMAP v0.4)

Memory Service(Cross-cutting) 구축 — 단일 Port(Memory Service Interface) 경유 구조, 실패→Lesson 생성→다음 작업 회수 사이클. Learn from Failure·Token Efficiency 원칙 구현.

## 3.2 선행 조건

- v0.3 ✅ (사용자 승인 완료, 2026-07-05)

## 3.3 완료 조건 (ROADMAP)

- 실패 → Lesson 생성 → 다음 작업 회수 사이클 시연 / 회수 규칙이 최소 Context 원칙 준수 / 모든 접근이 Memory Service Interface 경유 / Memory·Lessons 포맷이 스펙(04·05)과 일치.

## 3.4 산출물

- Memory Service Interface(단일 Port 계약), Memory store 구조·포맷, Lessons 포맷·생성 규칙, 기록/회수 프로토콜, Memory 인덱스 규격. (실현 경계: framework/memory/ — structure.md §2, 01 §4.1 Module 구현 디렉터리)

## 3.5 참고

- **병렬 트랙**: ROADMAP §4 — v0.3 완료로 {v0.4 ∥ v0.5 Verifier ∥ v0.8 착수}가 전부 개방됨. 사용자 지시는 "다음 세션 = v0.4 시작"이며, 병렬 트랙 확장은 사용자 결정 사안.
- **Lesson 후보 정식 기록**: v0.4 Lessons 구현 시 v0.1~v0.3 handoff의 Lesson 후보 전건(§1.5 — v0.2 3건 + v0.3 4건 + v0.1 승계)을 정식 기록 대상으로 상정.
- Memory 구현 형태는 v0.3과 동일하게 형태 A(규격 문서·프로토콜) 기조 — C-1~C-3 준수, framework/memory/ 문서 본문은 AI·언어 비의존, 물리 백엔드는 Adapter 바인딩 소관.
- 관행 유지: 위임 delegation-protocol.md / 검증 verification-checklist.md / 구현 Worker(Opus) / 완료 보고 불신·독립 검증 / framework·docs 문서 관례(§1.3).

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt)

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v0.3 (Runtime & Core Kernel)가 완료되었다.
이번 세션의 목표는 ROADMAP v0.4 (Memory & Lessons, Track A)다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v0.3.md를 정독한다 (직전 세션 결정·상태의 정본).
2. ARCHITECTURE.md (0.2, 특히 5.1 Memory Service), ROADMAP.md v0.4 섹션,
   specs/04-memory.md, specs/05-lessons.md를 정독한다.
3. .claude/AGENT.md, .claude/agents/ 4종, docs/delegation-protocol.md,
   docs/verification-checklist.md, framework/core/structure.md를 읽는다 (작업 도구·경계 정본).
4. v0.4 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.
   계획·분해 초안은 Planner에게 위임할 수 있다 (초안만 — 채택은 Advisor).

작업 규칙: v0.1~v0.3에서 확립된 하네스 관행을 그대로 유지한다 —
위임/보고는 delegation-protocol.md, 검증은 verification-checklist.md(게이트 A~D),
구현은 Worker(Opus) 위임, 완료 보고 불신·독립 검증, Frozen spec 변경은
버전 상승+Revision History, Architecture-Spec 충돌은 사용자 보고.
v0.3 확정 조건 C-1~C-3(Core Contract 불변·코드 배치 제한·AI/언어 비의존)을
framework/ 산출물 전체에 계속 적용한다.
```

---

# 5. 주의사항

1. **v0.3 산출물의 개정** — framework/·docs/ 문서는 Frozen이 아니다. 개정은 Advisor 승인 + 각 문서 §9 이력 절 기록 (v0.2 §1.3 거버넌스 승계). **개정 시 같은 상태를 서술하는 전 지점을 전수 갱신**한다 (Lesson 후보 2 — Advisor r2 잔여 결함 사례).
2. **DP-4 재상정** — 형태 B(실행 코드) 착수 여부는 v0.9 전후 재검토. 착수 시 DP-3(언어 선택)·B2~B4 완전판 전개·코드 물리 위치(structure.md §4 규칙 4 defer) 확정이 선행된다.
3. **경미 어휘 정리 후보** (검증 리포트 §3.6 기록, 위반 아님) — config-schema.md §7 표 열 라벨 "예약 요소", 근거 정본의 "DP-1 자리 예약의 승계 근거" 문구. 차기 개정 시 일괄 정리.
4. **Glossary 차기 개정 일괄 목록** (v0.1·v0.2 승계) — "Wave" 표제어 승격, §3.2-A "(도출)" 표기 정리. 버전 상승 필요.
5. **v0.9 이월** — 13 §3.2-B 전이 조건 2~4 재판정(Formal 전이), Adapter Interface 정식화(01 §4.2 목록은 11-adapters가 정식화).
