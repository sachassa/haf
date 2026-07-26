# docs/artifact-lifecycle-policy — 산출물 수명 · 삭제 · 앵커 인용 정책

작성일: 2026-07-17
상태: v1.0 (사용자 결정 2026-07-17 — 제정과 동시 발효)
상위 규약: AGENT.md
근거 정본:

- `docs/spec-versioning-policy.md` — docs 운용 정책 문서 관례(머리 상태 라인·§0 정본 경계)의 선례이자 **개정 기록 locus 정본**(§3 — 기록 = git 커밋·파일 내 이력 절 폐지). 본 문서는 같은 관례를 따른다.
- 루트 `ARCHITECTURE.md` §8 UAF-INV ① (접점 원칙 — 커밋 `5c80284` 재정의) — 무수정(동결) 원칙 폐지로 본 정책의 기존 산출물 정리가 거버넌스상 가능해졌다.
- `uahf/framework/adapters/claude/memory-binding.md` §5.3 (INV-6 기록 불변) — Memory store append-only 계약. 본 정책이 §2에서 유일한 삭제 금지 예외로 인용한다(재정의 0).
- Active Lesson L-07(상태 서술은 실측 후 기록) · L-10(이력 행 문면 불변·append-only) — 본 정책의 앵커 인용 규칙·ARCHIVE 원장 운용이 이 관행과 정합한다.

거버넌스: 이 문서는 `docs/` 소속 **UAF 레벨 운용 정책 문서**다. 계약(spec)의 정본이 아니며, 산출물의 수명·삭제·인용·배치의 **운용 규칙**만 소유한다. 개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = `docs/spec-versioning-policy.md` §3). 환경 무관 거버넌스 문서이므로 본문에 특정 AI 이름·모델명·제품 기능명을 두지 않는다.

---

## §9. 이력 (Revision History)

이력 기록 = git(이 파일 경로의 git log·제거 전 전문 앵커 64b6570). UAF 자체 개정 시에만 참조한다 — 규범 = docs/spec-versioning-policy.md §3.

---

## §0. 이 문서의 위치와 정본 경계

- 이 문서는 **산출물이 언제 생기고 언제 사라지는가**의 정책만 소유한다. 산출물의 내용·형식·계약은 각 정본(spec·binding) 소관이며 재정의하지 않는다.
- 적용 범위: 저장소 전체(루트 `docs/`·`uahf/` 포함 전 Layer). Memory store는 §2의 명시 예외.
- git 이력은 모든 삭제 산출물의 영구 보존 매체다. 본 정책의 "삭제"는 전부 **작업 트리에서의 제거**이며, 원본은 앵커 커밋으로 항상 열람 가능하다.

## §1. 목적

산출물 수명 규약 부재가 만든 세 가지 병을 구조적으로 차단한다:

1. **방치 누적** — run 원장·데모 산출물에 수명 규칙이 없어 무한 누적.
2. **경로 인용 족쇄** — 문서가 "이 경로에 파일이 물리 실재한다"를 판정 근거로 삼아, 해당 파일을 영구히 삭제 불가능하게 만듦.
3. **시간축 기록의 오배치·판례화** — 세션 핸드오프(UAF 레벨 시간축 기록)가 하위 Layer(`uahf/docs/`)에 살면서 규칙의 출처(판례)로 88개 파일에 전이.

## §2. 수명 등급

모든 산출물은 생성 시점에 아래 등급 중 하나에 속한다. 등급이 불명확하면 **ephemeral로 간주**한다(보수적 기본값 — 지워도 git이 보존한다).

| 등급 | 정의 | 예시 |
|---|---|---|
| **live** | 항상 최신 1부만 존재. 제자리 갱신·버전 접미 파일 신설 금지 | `docs/session-handoff.md`, ROADMAP, 운용 정책·프로토콜 문서, 스펙·바인딩, 실행 코드·테스트 |
| **ephemeral** | 작업 잔재. 재실행·재생성 가능 | run 원장(승격 전), metrics 산출물, 캐시, 드라이버 실행 출력 |
| **evidence** | 게이트·마일스톤 판정의 동결 증거. 승격은 Advisor 승인 | Baseline run 원장, CP2 판정 근거, 데모 픽스처 |
| **track-design** | 특정 트랙·마일스톤에 귀속된 설계·분석 문서 | `vX.Y-context-and-design.md`, 트랙 계획·실측 분석 문서 |
| *(예외)* **memory** | Memory store (`memory-data/store/`·`index/`) | 삭제 금지 — append-only 계약(memory-binding INV-6)이 정본. 본 정책의 삭제 규칙 비적용 |

## §3. 삭제 규칙

| 등급 | 삭제 규칙 |
|---|---|
| live | 삭제하지 않는다. 역할이 소멸하면 track-design으로 재분류 후 아카이브 |
| ephemeral | **자유 삭제.** 승인 불요. 재실행 도구가 자동 삭제(rmtree)해도 된다 |
| evidence | **앵커 등재 후 삭제.** `ARCHIVE.md` 원장에 `경로@커밋` 등재(§5)와 같은 커밋에서 작업 트리 제거. Advisor 승인 필요 |
| track-design | 트랙 Baseline 마감 시 evidence와 동일 절차로 아카이브. 트랙 진행 중에는 유지 |
| memory | 삭제 금지 (위 예외) |

재발 방지 조항: **마일스톤·트랙 마감 절차에 "산출물 등급 판정·아카이브"를 포함한다.** 마감 시 그 트랙의 track-design 문서와 evidence 승격분을 원장 등재 후 정리하고, 나머지 run 원장은 ephemeral로 삭제한다. 이 조치 없이 마감을 선언하지 않는다.

## §4. 인용 규칙 (안정 앵커)

- **허용 앵커**: ① `<경로>@<커밋해시>` (열람: `git show <커밋>:<경로>`) ② Active Lesson `L-XX` ③ Memory Item `mi-XXXX` ④ 현행 정본 문서의 § 포인터.
- **금지**: ephemeral·evidence·track-design 산출물을 **작업 트리 경로로** 인용하는 것. 특히 "이 경로에 실재한다"는 물리 실재 주장을 판정·검증 근거로 삼는 것(실재 주장은 live 산출물에만 허용 — L-07의 실측 규율은 유지하되 대상을 live로 한정).
- live 문서 간 상호 경로 참조는 허용한다(둘 다 제자리 갱신되므로 동반 갱신 가능).
- 세션 핸드오프는 어떤 문서의 규칙 출처(판례)로도 인용하지 않는다. 규칙의 근거는 정본 §·L-XX·mi-XXXX로만 표기한다(§6).

## §5. 아카이브 절차 (ARCHIVE 원장)

- 원장 = 루트 `ARCHIVE.md`. **append-only** 표. 필수 필드: 대상(경로 또는 경로 집합) · 앵커 커밋 · 등급 · 사유(어느 트랙·마일스톤의 증거인가) · 등재일.
- 절차: ① 앵커 커밋 확정(대상이 마지막으로 존재하는 커밋) → ② ARCHIVE.md에 등재 → ③ 같은 커밋에서 작업 트리 제거. 등재 없는 evidence/track-design 삭제는 금지.
- 삭제된 대상을 참조하던 활성 문서는 같은 커밋에서 앵커 표기로 개정한다(dangling 0 원칙).

## §6. 배치 규칙 — 세션 핸드오프

- 세션 핸드오프는 **UAF 레벨 단일 live 문서** `docs/session-handoff.md`다. 단수·제자리 갱신이며, 버전별 파일(`session-handoff-vX.Y.md` 형)을 만들지 않는다.
- `uahf/` 등 하위 Layer 트리에 세션 시간축 기록(핸드오프·세션 로그)을 두지 않는다 — 세션 연속성은 프로젝트 전체(UAF) 소관이다.
- 과거 상태의 열람이 필요하면 git 이력(`git log -- docs/session-handoff.md`)이 정본이다.

## §7. 제정 시 일괄 정리 (2026-07-17 조치 기록)

본 정책 제정과 함께 기존 위반을 일괄 정리했다. 상세 목록·앵커는 `ARCHIVE.md` 참조. 요약:

1. **동결 지층 아카이브**: `uahf/docs/` 버전 문서·demo-fixtures 6세대(v0.5~v1.0-generic), `uahf/dogfooding/uahf-lessons/`, 루트 `docs/` 완결 트랙 설계 문서 — 원장 등재 후 작업 트리 제거.
2. **run 원장 아카이브**: `orchestration-data/runs/`·`step-data/runs/`·`solution-design-data/events/`·`discovery-data/events/`·`loop-data/`·`e2e/metrics/` — evidence 승격분 포함 전량 앵커화 후 제거. 재현 도구(드라이버·테스트·측정 스크립트)와 데이터 표면(디렉터리 구조)은 유지.
3. **물리 실재 주장 개정**: 활성 바인딩·conformance 문서의 "실재" 판정 근거를 앵커 표기로 개정.
4. **핸드오프 판례 인용 제거**: 활성 문서의 `session-handoff-vX.Y §Z` 인용을 전량 제거(병기된 L-XX·mi-XXXX·정본 §는 유지). 라우팅·우회 장치는 두지 않는다.
5. **핸드오프 재정착**: `docs/next-session-prompt.md` → `docs/session-handoff.md` (§6 규약 발효).
