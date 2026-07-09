# 다음 세션 부트스트랩 프롬프트 (v1.2.1 이후 — Tier 2 진입)

작성: Advisor · 2026-07-09 · v1.2.1 Baseline 확정(커밋 `c09184f`) 직후
용도: 새 세션에서 아래를 붙여넣으면 재분석 없이 이어감. (물리 발화 = `/uaf-continue`)

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 세션에서 v1.2.1 Repository Refactoring이 완전히 종료되었다 —
구조 이동(Phase 1·2·3)에 더해 마감(밀레스톤 Memory Update · 명령 프리픽스 uaf: 확정 ·
root ROADMAP/README Baseline 기록)까지 완료하고, 사용자 Baseline 승인을 받았다.
CP2 독립검증 Pass 7/0/0 · CP3 승인 · 커밋 c09184f · 작업트리 clean.

반드시 다음 순서로 착수하라.

1. Read-First: docs/v1.2.1-context-and-design.md 를 정독한다.
   (상태=완결·Baseline 확정. 비전·아키텍처 2축·Layer 연결 설계(A)·오케스트레이션 모델(B)·
   상태분리·확정 결정·§7.1 stale uaf/ 마이그레이션 노트의 정본. 재분석 불요.)
2. git log --oneline + git status 로 커밋 체인(…6764465→63b3b03→c09184f)·clean 실측.
3. Memory Consult: [[uahf-active-track-v1.2.1]](완결·Baseline) + [[uahf-session-entrypoint]]
   (store 84·Active 22·Candidate 21·다음 트랙 미정 Tier 2/3).
   ※ uahf/docs/session-handoff-v1.2.md는 리팩토링 이전 구조이니 현혹되지 마라.

4. 다음 트랙은 스스로 채택하지 말고 사용자에게 확인하라(선취 금지).
   ★ Advisor 권장 시작점 = Tier 2 「.claude Global Default vs uahf override 재설계」.
     - 이유: (1) 사용자가 직접 짚은 미해결 숙제(루트 .claude가 uahf 거였는데 미이동),
       (2) 범위 명확·빠른 성과, (3) '설치형 도구(Global Default=도구 / override=Layer·프로젝트)'
       북극성 뼈대라 뒤이을 루트 ARCHITECTURE 재저술에 필요한 결정을 선확정한다.
     - Tier 2 권장 순서: .claude 재설계 → 루트 ARCHITECTURE 완전 재저술 →
       각 Layer(entry/discovery/planning) 저술 → stale uaf/ 참조 정식 개정(§7.1).
     - Tier 3(북극성: 상태분리 설계[브리프 C]·Layer 연결/오케스트레이션 정식화·
       uaf:<layer> 명령·Layer별 LLM·설치형 패키징)은 후속.

5. .claude 재설계 착수 확정 시:
   현재 루트 .claude/(AGENT.md·CLAUDE.md·agents/{advisor,worker,verifier,planner}·
   commands/{uaf-new,uaf-continue}·hooks·skills) + uahf/.claude/(빈 override 스텁 README) 실측 →
   "무엇이 도구 전체 Global Default이고 무엇이 uahf Layer 전용 override인가" 경계 설계 →
   검증·커밋.

작업 규칙: 구현은 Worker(Opus) 위임 · 완료 보고 불신 · Verifier 독립 검증(CP2) ·
Advisor 승인(CP3) · 정본·append-only 데이터 무편집(바이트 보존) · 구조 변경은 git 안전망 하.
```

---

## 🪶 짧은 버전 (이것만으로도 됨)

Memory(MEMORY.md)가 자동 로드되므로 사실 이거면 충분하다:

> v1.2.1 끝났고 Baseline 확정됐어. 다음은 Tier 2로 가자 —
> `docs/v1.2.1-context-and-design.md` 먼저 읽고, git log로 상태 확인한 뒤,
> **`.claude` Global Default vs uahf override 재설계**부터 착수 제안해줘.

---

## 현재 상태 스냅샷 (2026-07-09)

- **완결**: v1.2.1 Repository Refactoring — 구조 이동(Phase 1·2·3) + 마감. Baseline 확정(사용자 승인).
- **커밋**: `692c4ca`→`ffe71a6`→`e1b36c4`→`3951407`→`6764465`→`63b3b03`→**`c09184f`**(마감). 작업트리 clean.
- **Memory**: store 84(mi-0082 BPD-15·mi-0083 재발판정 Novel·mi-0084 L-21 신규 등록). Active 22·Candidate 21. BP-04 승격 보류.
- **확정 결정**: 명령 프리픽스 = `uaf:`. UAHF 개발 baseline = v1.2 불변(uahf/ROADMAP 무변경). v1.2.1은 저장소 구조 트랙.
- **다음 트랙 = 미정(사용자 결정)** — Advisor 권장 = Tier 2 `.claude` 재설계.
