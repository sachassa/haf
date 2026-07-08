# UAHF Session Handoff — v0.1 → v0.2

작성일: 2026-07-05
작성자: Advisor (v0.1 세션)
목적: 이 문서만 읽어도 새 세션이 v0.2를 이어갈 수 있게 한다.

---

# 1. 이번 세션 요약

## 1.1 완료한 작업

1. **ROADMAP.md 작성·승인** — v0.1(Specification Baseline)부터 v1.0(Architecture Validation & Release)까지 10단계. 각 버전에 목표/선행 조건/완료 조건/산출물/병렬 작업 가능 여부 정의. 병렬 트랙 맵 포함.
2. **ARCHITECTURE.md 0.1 → 0.2 개정** — Memory를 Layer에서 Cross-cutting Service로 재정의 (설계 검토 후 사용자 승인).
3. **specs/TEMPLATE.md 설계·채택** — 공통 Specification 표준 (§0~§9 구조 + DoD 8항목 + Status 전이 규칙).
4. **ROADMAP v0.1 실행 완료** — specs/00-glossary ~ 13-harness 총 14개 spec을 Wave 방식으로 작성·검증:
   - Wave 1: Glossary (Worker 1명)
   - Wave 2: 01-runtime, 02-agent (병렬 2명)
   - Wave 3: 03~13 (병렬 11명)
   - Wave 4: 통합 (병렬 2명 — Glossary 용어 45건 통합·결정 반영 / 11-adapters 바인딩 지점 17개 통합)
5. **v0.1 기준선 Frozen 확정** — 사용자 승인 (2026-07-05). TEMPLATE + specs 14개 = 15개 문서.

## 1.2 주요 설계 결정 (전부 사용자 승인 또는 Advisor 결정으로 확정, 각 spec §9에 기록됨)

| 결정 | 내용 | 기록 위치 |
|---|---|---|
| 구현 형태 = 하이브리드 | v0.x는 Claude Code 위 self-hosting. 단 모든 산출물에서 Core Contract(AI 비의존, §3)와 Adapter Binding(환경 의존, §4)을 물리적으로 분리. 이식 시 Adapter만 교체 | 사용자 결정, ROADMAP 2.3, TEMPLATE §3/§4 |
| v1.0 범위 | Claude Adapter 완전 구현 + 2nd Adapter(OpenAI 또는 Generic) **최소 구현**으로 Architecture Validation | 사용자 결정, ROADMAP v1.0 |
| Memory = Cross-cutting Service | Layer 아님. 단일 Port(Memory Service Interface)만이 접근 경로. 회수 정책(목적·범위 필수, 전량 로드 금지) 계약 내장. 영속성 백엔드는 Adapter 뒤 | 사용자 승인, ARCHITECTURE 5.1, specs/04 |
| Layer 책임 정의 정본 = Glossary | ARCHITECTURE는 스택 순서만, 책임 정의는 Glossary §3.2-A. Runtime=실행·수명주기·config / Core=AI 비의존 계약·모듈 근간 | Glossary §9-OQ1/OQ3 |
| Loop ∈ Runtime Layer | Lifecycle의 실행·반복은 실행 환경 책임 | Glossary §9-OQ2 |
| Planner 역할 | 계획·분해 **초안 작성** 보조 역할. 채택·승인·Architecture 결정 권한 없음 (Advisor 소관) | Glossary §9-OQ4 |
| 검증 게이트 3단계 | CP1 Worker 자체 점검 → CP2 Verifier 독립 판정(=Verify 통과) → CP3 Advisor 승인(=Complete 게이트) | specs/03 §3.1-A |
| Config 우선순위 | Module > Project > Global (좁은 스코프 우선) | specs/01 §9-OQ-R1 |
| 01↔02 실행 채널 | Agent = Runtime의 generic Module. entrypoint 입력=위임 메시지(02 §3.2-B), 출력=완료/실패 보고(02 §3.2-C/D). 메시지 계약은 02, 호스팅 계약은 01, 물리 채널은 각 §4 소관 | 01·02 §9 |
| Deregister 연산 | 01 §3.1-A에 추가 (10-plugins가 발견한 계약 갭 — Plugin 제거의 전제). Registry 수명주기는 Runtime 소유 | 01 §9 결정 기록 |
| 재발 판정 3분류 | Novel / RecallGap / Recurrence — "같은 실수를 반복하지 않는다"의 검증 가능화 | specs/05 §3.1-C |
| Hook = 비차단 observer (v0.1) | 차단·veto·mutation 미제공. 이벤트 18개는 전부 확정 계약에서 도출 | specs/08, §9 결정 기록 |
| 2nd Adapter 합격선 | 필수 바인딩 지점 **13개**(BP-1~5, 7~11, 13~15) + Core 수정 0건 + 핵심 루프 1회 통과 = Valid(Minimal) | specs/11 §3.2-B |
| Component→Layer 매핑 | Glossary §3.2-D 매핑표가 정본 | Glossary §9-OQ6 |

## 1.3 Architecture 변경 사항

- **ARCHITECTURE.md 0.2** (유일한 변경): 7-Layer → 6-Layer + Memory Cross-cutting Service (5.1 신설), Revision History(§9) 추가. 그 외 ARCHITECTURE·AGENT.md·CLAUDE.md는 무수정.

## 1.4 검증 결과

- 15개 문서 전부 Advisor가 파일 정독으로 독립 검증 — **DoD 위반 최종 0건**.
- Worker 위임 총 16회. 검증 게이트가 실제 작동한 사례 2건:
  1. **Wave 1**: Glossary Worker의 자체 점검이 "Claude" 토큰만 검사해 §3의 모델명("Opus")을 놓침 → Advisor 재검증에서 검출·교정. 이 "검사 범위 부족" 유형은 specs/06 V4·VT-4 계약과 §8 예1 시연 케이스로 편입됨. 이후 Wave에서 재발 0건.
  2. **Wave 3**: 10-plugins Worker가 01의 실제 계약 갭(Deregister 부재)을 추측으로 우회하지 않고 에스컬레이션 → 01 계약 수정으로 해소.
- 상호 참조 무결성: 순환 의존 0건, spec 간 조율 항목 전건 해소 (각 §9 "결정 기록 (Advisor — Wave 4 통합)" 블록 참조).

---

# 2. 현재 프로젝트 상태

## 2.1 버전

- **v0.1 완료 (Frozen, 2026-07-05)**. 다음 단계: v0.2.

## 2.2 완료된 Roadmap 단계

- ✅ v0.1 Specification Baseline — 완료 조건 전부 충족 (spec 15개, Core/Adapter 경계, 상호 참조 무결성, Advisor 검증).
- ⬜ v0.2 ~ v1.0 — 미착수.

## 2.3 Frozen 문서 (15개 — 변경 시 버전 상승 + Revision History 필수, TEMPLATE §4)

`specs/TEMPLATE.md`, `specs/00-glossary.md`, `specs/01-runtime.md` ~ `specs/13-harness.md` (전체).

승인된 기준 문서 (Frozen 아님, 별도 개정 절차): `ARCHITECTURE.md` (0.2), `ROADMAP.md`, `.claude/CLAUDE.md`, `.claude/AGENT.md`.

## 2.4 아직 미완성인 파일

| 파일 | 상태 | 담당 단계 |
|---|---|---|
| `.claude/agents/advisor.md`, `planner.md`, `verifier.md` | 빈 파일 | **v0.2 산출물** |
| `.claude/agents/worker.md` | `model: opus` frontmatter 한 줄만 | **v0.2 산출물** |
| `README.md` | 빈 파일 | v1.0 산출물 |
| `framework/`, `adapters/` 디렉터리 | 미생성 | v0.3+ (01 §4.1 규격) |

## 2.5 하네스 상태

**Bootstrap** (specs/13 §3.2-B, §8 예2 판정). Formal 전이 조건 4개 중 조건 1(관련 spec Frozen)은 이번 승인으로 충족 시작. 조건 2~4는 v0.3~v0.9에서 충족 예정.

---

# 3. 다음 세션에서 수행할 작업 (v0.2 — Agent Harness Bootstrap)

## 3.1 목표 (ROADMAP v0.2)

UAHF가 스스로를 개발할 최소 하네스를 spec 기준으로 완성한다 (self-hosting 정식화의 첫 단계). Agent 4종 정의와 위임·보고 프로토콜을 확정한다.

## 3.2 선행 조건

- v0.1 Frozen ✅ (충족됨 — 특히 specs/02-agent.md가 Agent 정의의 기준)

## 3.3 산출물과 우선순위

1. **`.claude/agents/advisor.md`, `planner.md`, `worker.md`, `verifier.md` 완성** — specs/02-agent.md §3.2-A(역할 경계 표)·§4.1(Claude Code 바인딩)과 AGENT.md를 준수. Worker의 기본 실행 모델 = Opus (02 §4.1 BP-9 바인딩). 4개 병렬 작성 가능 (공통 규약 정합 확인 선행).
2. **위임/보고 프로토콜 문서** — 02 §3.2-B/C/D 메시지 포맷(from/to/task/input/output/done/context/constraints; artifacts/self_check/failures/open_questions/verify_basis; reason/repro/attempted/lesson_candidate/blocking)의 운용 문서화.
3. **Advisor용 검증 체크리스트** — TEMPLATE DoD 8항목 + 06 검증 유형 VT-1~VT-5 기반.
4. **완료 조건 시연**: 위임 → 구현 → 검증 → 승인 사이클 1회 이상 실증 (v0.1 세션의 Wave 사이클을 선례로 인용 가능하나, v0.2는 완성된 agent 정의 위에서 재시연).

## 3.4 v0.2 완료 조건 (ROADMAP)

- 4개 Agent 정의가 specs/02-agent.md와 AGENT.md를 준수한다.
- 위임 → 구현 → 검증 → 승인 사이클을 실제로 1회 이상 시연한다.
- 각 Agent의 입력, 출력, 완료 조건, 실패 보고 포맷이 정의되어 있다.

---

# 4. 다음 세션 시작 프롬프트 (Bootstrap Prompt)

아래를 새 세션에 그대로 붙여넣는다.

```
너는 Universal Agentic Harness Framework(UAHF)의 메인 Advisor다.

이전 세션에서 v0.1 Specification Baseline이 완료되어 Frozen으로 확정되었다.
이번 세션의 목표는 ROADMAP v0.2 (Agent Harness Bootstrap)다.

반드시 다음 순서로 착수하라.

1. docs/session-handoff-v0.1.md를 정독한다 (이전 세션의 결정·상태·주의사항의 정본).
2. ARCHITECTURE.md (0.2), ROADMAP.md의 v0.2 섹션, specs/TEMPLATE.md를 읽는다.
3. specs/02-agent.md를 정독한다 (v0.2 산출물의 기준 spec — 역할 경계 §3.2-A,
   위임/보고 메시지 §3.2-B/C/D, Claude 바인딩 §4.1, Invariants §3.3).
4. .claude/AGENT.md와 .claude/CLAUDE.md를 읽는다 (상위 규약).
5. v0.2 실행 계획을 수립해 사용자 승인을 받은 뒤 착수한다.

작업 규칙 (v0.1 세션에서 확립·검증된 하네스 관행 — 그대로 유지하라):

- 구현은 Worker(Opus)에게 위임한다. Advisor는 계획·분해·위임·검증·승인에 집중한다.
- 모든 위임 메시지는 입력·출력·완료 조건·컨텍스트(읽을 문서 목록)를 포함한다 (02 INV-6).
- Worker 완료 보고를 그대로 신뢰하지 않는다. 산출물을 직접 정독해 독립 검증한다.
- DoD-3 검증(AI 비의존)은 "Claude" 토큰만이 아니라 모델명(Opus 등)·제품 기능명까지
  전수 검사한다 (specs/06 V4·VT-4 — v0.1에서 실제 검출된 결함 유형).
- 병렬 위임 시 각 Worker는 자기 파일만 수정하고, 동시 작성 중인 산출물을 추측·인용하지
  않으며, 조율 필요 사항은 에스컬레이션한다 (specs/07 R1~R4).
- 모든 설계 결정과 미해소 사항은 기록한다. 미확정은 Open Questions로 남기고 추측하지 않는다.
- Frozen spec(TEMPLATE, specs/00~13)의 변경은 버전 상승 + Revision History 기록이
  필수이며, Architecture와 spec이 충돌하면 수정하지 말고 사용자에게 보고한다.

사용자 미결정 사항 2건 (착수 전 확인 권장 — handoff §5.1 참조):
- ARCHITECTURE.md에 Layer 책임 정의 요약 반영 여부 (현재 정본은 Glossary §3.2-A)
- AGENT.md Delegation에 Planner 역할(초안 작성 보조, 결정 권한 없음) 추가 여부
  — v0.2가 planner.md를 작성하므로 이번 세션과 직접 관련된다.

구현 착수 전에 계획을 세우고 사용자 승인을 받아라.
```

---

# 5. 주의사항

## 5.1 아직 확정되지 않은 설계 (사용자 결정 대기 2건)

1. **ARCHITECTURE.md에 Layer 책임 정의 요약 반영 여부** — 현재 정본은 Glossary §3.2-A (사용자 승인된 ROADMAP 산출물 정의에 근거). ARCHITECTURE는 스택 순서만 보유. 반영해도, 안 해도 모순은 없음.
2. **AGENT.md Delegation에 Planner 항목 추가 여부** — 현재 AGENT.md는 Advisor/Worker/Verifier 3자만 명시. Glossary §9-OQ4 결정(Planner=초안 작성 보조)은 확정되어 있으나 상위 규약 반영은 사용자 승인 대상. **v0.2에서 planner.md를 작성하므로 이번에 결정하는 것이 좋다.** 관련 기록: 02 §9-OQ-2, 13 §9-OQ-H5.

## 5.2 보류된 이슈 (차단 아님 — 해당 버전에서 처리)

| 이슈 | 처리 시점 | 기록 위치 |
|---|---|---|
| Skill 발견 모호성 해소 규칙 상세 (골격만 확정: 명시 호출 > 구체적 트리거 > 실패) | v0.8 구현 시 정밀화 | 09 §9 결정 기록 |
| Plugin 배포 채널의 BP-6 흡수 — 분리 필요성 재검토 | v0.8 | 11 §9 결정 기록 |
| 02 완료 보고에 best_practice_candidate 명시 필드 추가 여부 (현재는 보편 후보 자격으로 충족) | v0.2 이후 재검토 | 05 §9 결정 기록 |
| Memory scope taxonomy 4차원의 충분성 재확인 | v0.4 구현 시 | 04 §9-OQ-M3 |
| 재시도 한도 기본값·스코프 (판정 규칙만 확정, 값은 Config) | v0.3 Config 구현 시 | 03 §3.1-B |
| Glossary §3.2-A 서두의 "(도출)" 표기 정리 — OQ1/OQ3 결정으로 실질 해소되었으나 문구가 남음 (내용 모순 없음) | Glossary 차기 개정 시 (버전 상승 필요) | Glossary §3.2-A 주 |

## 5.3 향후 Architecture Review가 필요한 항목

1. **v0.9 Adapter 정식화 시**: specs/11의 BP-1~17 목록과 최소 부분집합(13개)을 실제 `adapters/claude/` 구축 결과와 대조 재검증. v0.2~v0.8에서 새 바인딩 표면이 생기면 11 개정 필요 (버전 상승).
2. **Bootstrap → Formal 전이 추적**: specs/13 §3.2-B 전이 조건 4개의 충족 여부를 매 버전 확인 (특히 v0.3에서 Runtime 호스팅, v0.9에서 Scaffold 설치 대상화).
3. **spec versioning 정책 문서화** — ROADMAP상 v0.9 산출물. Frozen 이후 첫 spec 개정이 발생하면 그 전에 앞당겨 정의할 것을 권함.
4. **Frozen 직후 교정 이력 (투명성 기록)**: Frozen 전이 직후 Glossary §3.2-D 표의 낡은 표기 2건("specs/12·13 (미작성)")이 발견되어 기준선 확정 작업의 일부로 즉시 교정되었다 (버전 무변경, 사실 오기 수정). 동일 유형 재발 방지: Frozen 전 최종 검증에 "문서 내 상태 서술과 실제 상태의 전수 대조"를 포함할 것 — Lesson 후보.

## 5.4 참고: 이 하네스의 작동 방식 (v0.1 세션 실증)

이 프로젝트는 자신의 spec이 규정하는 방식으로 개발된다 (self-hosting). v0.1 세션의 실제 사이클 — Advisor가 Wave로 분해·병렬 위임(07 실증) → Worker가 작성·자체 점검(02 실증) → Advisor가 정독 재검증·거짓 완료 검출(06 실증) → 결정 기록·Glossary 정본화(00 INV-4 실증) → 사용자 승인 게이트 — 이 그대로 v0.2 이후의 작업 방식이다.
