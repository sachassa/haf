# 다음 세션 부트스트랩 프롬프트 (Tier 2 잔여 — 사용자 채택 2026-07-09)

작성: Advisor · 2026-07-09 · v1.2-era 정리 완결 + 후속(agents 정정·완전성 규율 강제) 직후
용도: 새 세션에서 아래를 붙여넣으면 재분석 없이 착수. (물리 발화 = `/uaf-continue`)
상태: **다음 = Tier 2 잔여 작업(사용자 결정 2026-07-09). 세부 항목 택1 후 착수.**

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 세션에서 v1.2-era 잔존물 정리(커밋 a032c52)·후속 agents ARCHITECTURE.md 참조 정정
(a6a4ccb)·완전성·사실 주장 규율 강제(2be4cd1)를 완료했다. 사용자가 다음은 「Tier 2 잔여
작업」을 하기로 정했다.

먼저 다음 순서로 착수하라.

1. Read-First: ARCHITECTURE.md(v1.3 라우터 정본·§0 "uaf/ 소멸") · Memory Consult
   ([[uahf-session-entrypoint]] + Project Contract pc-uahf-001 정독).
   store 91·Active 22·Candidate 26. 직전 트랙 상세=[[uahf-active-track-v1.2-era-cleanup]].
2. git log --oneline + git status (…a032c52→b079f22→a6a4ccb→2be4cd1·clean 실측).
3. ⚠️ 상시 원칙:
   - 완전성·사실 주장 규율(L-24·CLAUDE.md 규율절): "정확히 N·전수·잔여 0" 주장 전
     관련 패턴 전수 스윕·검색 범위 명시. 단일 좁은 스캔 exhaustive 단정 금지.
   - 동결 영역(§9 이력·날짜 실측 스냅샷·append-only)은 in-place 금지(L-22)·재측정/supersede만.
   - 리팩토링 후 경로 정정은 접두 치환 아닌 대상별 라우팅 표(L-23).
   - ✅ SessionStart 리마인더 훅(.claude/settings.json)이 이번 세션에 떴는지 확인 —
     지난 세션 신설이라 이번부터 활성 예상. 안 뜨면 /hooks 재로드.

Tier 2 잔여 3항목(사용자 택1 — 선취 금지):
  [T-a] 각 Layer 독립 ARCHITECTURE 완전 저술 (⭐ 권장 — 본론) : entry/·discovery/·planning/·
        knowledge/·uahf/ ARCHITECTURE.md 완성도 편차 해소·루트 라우터(§2.1)와 정합·상세화.
  [T-b] harness-doc 내부 약칭 정규화 pass : uahf/framework/**·.claude/ 내부 bare specs/·
        framework/(uahf-root-relative 약칭)를 명시 경로로 정규화할지 "유지 vs 명시" 결정·정리.
        저위험·저효용. (v1.2-era에서 비대상 유보한 클래스.)
  [T-c] AGENT.md/CLAUDE.md body 분할 : 한 파일의 GD(공통) 부분과 U(프로젝트 특정) 부분 분리.
        ⚠️ L-14 CRLF hold — disk=CRLF·blob=LF 위험(이번 세션 CLAUDE.md 편집서 실제 발동,
        blob 기준 재구성으로 교정). 편집 전 git 스냅샷·편집 후 diff로 additive/의도 라인만 확인.

4. 택1 후: plan mode로 계획 확정·승인 → Worker 위임 → Verifier CP2 → Advisor CP3 → 커밋.

작업 규칙: 구현 Worker(Opus) 위임 · 완료 보고 불신 · Verifier 독립 검증(CP2) ·
Advisor 승인(CP3) · 동결/append-only 바이트 보존(L-14 tr -dc 실측) · git 안전망 하.
```

---

## 🪶 짧은 버전 (이것만으로도 됨)

> Tier 2 잔여 하기로 했어. `[[uahf-session-entrypoint]]` Consult부터 하고, Tier 2 3항목
> ([T-a] 각 Layer ARCHITECTURE 저술[권장]·[T-b] 경로 약칭 정규화·[T-c] AGENT/CLAUDE body
> 분할[L-14 hold]) 중 뭘 할지 정하자. 완전성 주장은 전수 스윕 후(L-24)·동결은 in-place 금지(L-22).

---

## 현재 상태 스냅샷 (2026-07-09)

- **직전 완료**: v1.2-era 정리(a032c52·CP2 5/5) → Memory Update(b079f22·mi-0088~90) →
  agents ARCHITECTURE.md 참조 정정(a6a4ccb·6곳) → 완전성·사실 주장 규율 강제(2be4cd1·
  CLAUDE.md 규율절+L-24+SessionStart 훅).
- **커밋 체인**: …`a032c52`→`b079f22`→`a6a4ccb`→**`2be4cd1`**. 작업트리 clean.
- **다음 = Tier 2 잔여**(사용자 2026-07-09) — [T-a]~[T-c] 중 택1. 권장=[T-a].
- **Tier 3(북극성) 대기**: 상태 분리·Layer 오케스트레이션·uaf:<layer>·Layer별 LLM·설치형
  패키징(형태 B = Scaffold spec 12-scaffold Frozen v0.1·구현 미착수). **agents·commands·model
  override 물리 이동은 전부 형태 B(Tier 3) 소관** — 환경이 루트 .claude/만 로드하므로 그 전엔
  물리 이동 금지(개념 귀속=형태 A로 확정됨, 정본 docs/tier2-claude-override-design.md).
- **최신 교훈**: L-24(완전성 주장 전 전수 스윕·자기 주장도 검증)·L-23(라우팅 표)·BPD-17
  (재베이스라인). L-21 커널 4연속 재발 → 승격 근거 강화. L-21~L-24·BPD-17 승격 심사 대기.
