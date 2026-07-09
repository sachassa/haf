# 다음 세션 부트스트랩 프롬프트 (Tier 2 계속 — 루트 ARCHITECTURE 완전 재저술)

작성: Advisor · 2026-07-09 · Tier 2 첫 트랙(.claude override 재설계) 완결 직후(커밋 `9435ee9`)
용도: 새 세션에서 아래를 붙여넣으면 재분석 없이 이어감. (물리 발화 = `/uaf-continue`)

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 세션에서 Tier 2 첫 트랙 「.claude Global Default vs uahf override 재설계」가
완결되었다 — 개념 귀속(루트 .claude 12항목 G/U 명찰)·override 계약(ADD/REPLACE/MERGE)을
형태 A로 확정하고, 무위험 정합(agents specs 경로·uahf/.claude/README 명칭)만 물리 반영했다.
핵심 발견: 환경은 루트 .claude/만 네이티브 로드 → 개념귀속≠물리위치, 물리 재배치는
형태 B(Scaffold 합성, uahf/specs/12-scaffold Frozen v0.1) 유보.
CP2 Pass 전건 · CP3 승인 · 사용자 승인 · 커밋 6fa5bd0·9435ee9 · 작업트리 clean.

반드시 다음 순서로 착수하라.

1. Read-First: docs/tier2-claude-override-design.md 정독(직전 트랙 설계 정본 —
   개념 모델·12항목 귀속표·형태 A/B·§9가 "루트 ARCHITECTURE 재저술의 선결 입력"을 명시).
   보조: docs/v1.2.1-context-and-design.md(§7 루트 ARCHITECTURE 완전 재저술 대상·§7.1 stale uaf/ 노트).
2. git log --oneline + git status 로 커밋 체인(…c09184f→b75bb7b→6fa5bd0→9435ee9)·clean 실측.
3. Memory Consult: [[uahf-active-track-tier2-claude-override]] + [[uahf-session-entrypoint]]
   + 본 저장소 Project Contract 정독(pc-uahf-001).
   (store 85·Active 22·Candidate 22[+BPD-16]·다음 트랙 미정.)
   ※ uahf/docs/session-handoff-v1.2.md는 리팩토링 이전 구조이니 현혹되지 마라.

4. 다음 트랙은 스스로 채택하지 말고 사용자에게 확인하라(선취 금지).
   ★ Advisor 권장 = Tier 2 「루트 ARCHITECTURE 완전 재저술」.
     - 이유: (1) 권장 순서상 .claude 재설계 바로 다음,
       (2) 직전 트랙 설계 문서 §2·§4가 루트 ARCHITECTURE의 .claude 절 선결 입력(§9 명시) — 재료 준비됨,
       (3) 북극성 '루트=라우터 / 각 Layer 독립 ARCHITECTURE' 뼈대라 이후 Layer 저술·
       오케스트레이션·형태 B의 골격, (4) §0 개념 프레이밍(uaf/ vs UAHF)·카테고리 라벨이 stale —
       context-and-design §7이 '완전 재저술 대상'으로 명시(v1.2.1은 이관+경로정합만 함).
     - 함께 묶기 권장: stale uaf/ 참조 정식 개정(§7.1)을 이 재저술에 통합(같은 정본 이중 편집·
       L-14/L-21 재스윕 회피).
     - 대안 후순위: 각 Layer 저술(라우터 먼저) · Tier 3 기능(기반 먼저) ·
       AGENT/CLAUDE body 분할(L-14 hold·형태 B 결합).

5. 루트 ARCHITECTURE 재저술 착수 확정 시:
   - 성격 = 정식 개정 트랙(정본 개정·버전 상승·Advisor 승인). ※ 무수정 대상은 uahf/specs/* 등
     다른 정본이며, 루트 ARCHITECTURE.md는 이 트랙의 개정 대상이다.
   - 재저술 대상: §0 개념 프레이밍(uaf/ vs UAHF) · 카테고리 라벨(specs/·framework/) ·
     라우터 모델(각 Layer 독립 ARCHITECTURE로 분기) · knowledge Base 반영 ·
     .claude 절(tier2 설계 문서 §2·§4 인용) · 내부 stale uaf/ 참조 정합.
   - L-14(CRLF는 tr -dc 원바이트로 실측 — grep -c $'\r' 금지) · L-21(파생 참조 표면 전수 스윕) 준수
     → 검증 → 커밋.

작업 규칙: 구현은 Worker(Opus) 위임 · 완료 보고 불신 · Verifier 독립 검증(CP2) ·
Advisor 승인(CP3) · append-only 데이터 무편집(바이트 보존) · git 안전망 하.
```

---

## 🪶 짧은 버전 (이것만으로도 됨)

Memory(MEMORY.md)가 자동 로드되므로 사실 이거면 충분하다:

> .claude override 재설계 끝났어(형태 A 확정·물리 재배치는 형태 B 유보).
> 다음은 Tier 2 계속 — `docs/tier2-claude-override-design.md` 먼저 읽고, git log로 상태 확인한 뒤,
> **루트 ARCHITECTURE 완전 재저술**부터 착수 제안해줘(stale uaf/ 정식 개정도 함께).

---

## 현재 상태 스냅샷 (2026-07-09)

- **완결**: Tier 2 첫 트랙 「.claude override 재설계」 — 형태 A(개념 귀속 확정 + 무위험 정합). 사용자 승인.
- **커밋**: …`c09184f`→`b75bb7b`→**`6fa5bd0`**(설계 정본+정합)→**`9435ee9`**(Memory Update BPD-16). 작업트리 clean.
- **Memory**: store 85(mi-0085 BPD-16 Candidate — 환경 경계 실측·개념귀속≠물리위치·형태 A/B 유보). Active 22·Candidate 22. BPD-15 재상정 미발동·L-21 예방 적용(승격 보류 유지).
- **설계 정본**: `docs/tier2-claude-override-design.md`(9절) — 다음 트랙의 Read-First.
- **형태 B(물리 재배치) 위치**: Tier 3 「설치형 패키징」 = Scaffold spec `uahf/specs/12-scaffold.md`(Frozen v0.1). 물리 구현 미착수.
- **다음 트랙 = 미정(사용자 결정)** — Advisor 권장 = **루트 ARCHITECTURE 완전 재저술**(+ stale uaf/ 정식 개정 통합).
