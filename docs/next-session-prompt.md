# 다음 세션 부트스트랩 프롬프트 (Tier 2 계속 — v1.2-era 잔존물 정리 권장)

작성: Advisor · 2026-07-09 · 루트 ARCHITECTURE v1.3 재저술 완결 직후(커밋 `dc805be` — 크래시 중단 복구 완료)
용도: 새 세션에서 아래를 붙여넣으면 재분석 없이 이어감. (물리 발화 = `/uaf-continue`)

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 트랙 「루트 ARCHITECTURE.md 완전 재저술(v1.3 — 라우터 모델·절 재배치)」가 완결되었다.
직전 세션이 재저술 중 크래시 → 이번에 BPD-13(중단 재개: 완료 보고 불신·산출물로 독립 복원)로
재개해, 미수행이던 "하위 §앵커 의미 재정합"(하위 문서들이 옛 절 번호로 ARCHITECTURE를
인용하던 것을 v1.3 번호로 라벨 기준 재정합)을 9파일에 완성했다.
CP2 Pass 9/9(독립 Verifier)·CP3 승인·커밋 dc805be. 작업트리 clean.
동결 보존: §9 이력 행·discovery-binding §13 실측 스냅샷(2026-07-07)은 HEAD 원복.

반드시 다음 순서로 착수하라.

1. Read-First: ARCHITECTURE.md(v1.3 — 라우터 정본, §0 라우터 선언·§2.1 Layer 지도·
   §4 knowledge 횡단 Base·§5 .claude G/U 합성·§12.2 Discovery Request).
   보조: docs/tier2-claude-override-design.md(직전 Tier 2 트랙 설계 정본)·
   docs/v1.2.1-context-and-design.md(§7 재저술 대상·§7.1 stale uaf/ 노트).
2. git log --oneline + git status로 커밋 체인(…9435ee9→64c0662→dc805be)·clean 실측.
3. Memory Consult: [[uahf-session-entrypoint]] + [[uahf-active-track-tier2-claude-override]]
   + 본 저장소 Project Contract 정독(pc-uahf-001).
   (store 85·Active 22·Candidate 22[+BPD-16]·다음 트랙 미정.)
   ※ uahf/docs/session-handoff-v1.2.md는 리팩토링 이전 구조이니 현혹되지 마라.

4. 다음 트랙은 스스로 채택하지 말고 사용자에게 확인하라(선취 금지).
   ★ Advisor 권장 = Tier 2 「v1.2-era 잔존물 정리」(직전 재저술이 TIGHT 스코프로 유보한 선재 부채).
     대상(감사·CP2가 식별):
     (a) dogfooding "실측" 열거의 stale 서술 — entry-binding.md·discovery-binding.md의
         "실측 대조" 표/문안이 저장소 루트에 `uaf/`·`specs/`·`docs/`가 있다고 서술(리팩토링 후
         사실 오류). ※ 이들은 날짜 명시(2026-07-07) 동결 측정 스냅샷이므로, 단순 경로 치환이
         아니라 §13/§10을 현시점 재측정으로 재베이스라인(일자·버전 갱신)하는 방식이 정합.
     (b) default-policy.yaml 헤더의 stale 경로 `uaf/specs/02-discovery.md §3.15`.
     (c) discovery/02·planning/03의 `ARCHITECTURE.md 5.1`(Memory Service) — 루트 ARCH 절이
         아니라 uahf/ 접두 누락 stale-path(→ `uahf/ARCHITECTURE.md §5.1` 소관). 라우터 모델상
         각 Layer 독립 ARCHITECTURE 저술과 함께 처리 권장.
     (d) project-contract.v1.md(instanceVersion:1) 동결 인스턴스의 stale `uaf/specs/` —
         in-place 편집 금지, supersede v2 발행 시에만 갱신(거버넌스 판단 필요).
     (e) 'uaf/ 정본'·'uaf/specs/ 경계' 개념어 정책 — §0 "uaf/ 소멸"과의 정합 확정(keep vs align).
     - 대안 후순위: 각 Layer 독립 ARCHITECTURE 저술(라우터 분기 실체화) · Tier 3 기능(기반 먼저).

5. 착수 확정 시: 동결 영역(§9 이력·날짜 명시 실측 스냅샷·append-only 인스턴스)과
   LIVE 표면을 반드시 구분(L-06/L-20). L-14(CRLF tr -dc 실측·grep -c $'\r' 금지)·
   L-21(파생 참조 표면 전수 스윕) 준수 → Verifier CP2 → Advisor CP3 → 커밋.

작업 규칙: 구현은 Worker(Opus) 위임 · 완료 보고 불신 · Verifier 독립 검증(CP2) ·
Advisor 승인(CP3) · append-only 데이터/동결 스냅샷 바이트 보존 · git 안전망 하.
```

---

## 🪶 짧은 버전 (이것만으로도 됨)

> 루트 ARCHITECTURE v1.3 재저술 + 하위 §앵커 정합 끝났어(크래시 복구·커밋 dc805be).
> 다음은 Tier 2 계속 — **v1.2-era 잔존물 정리**부터 착수 제안해줘(dogfooding 실측 재베이스라인·
> default-policy/ARCHITECTURE 5.1 stale-path·개념어 정책). 동결 스냅샷/append-only는 보존 원칙으로.

---

## 현재 상태 스냅샷 (2026-07-09)

- **완결**: Tier 2 「루트 ARCHITECTURE v1.3 완전 재저술」 — 재저술 본체(직전 세션) + 하위 §앵커 정합(이번, 크래시 복구). 사용자 승인 플로우.
- **커밋**: …`9435ee9`→`64c0662`→**`dc805be`**(하위 §앵커 v1.3 정합·13파일·382+/330−). 작업트리 clean.
- **판정 이력**: L-21 전수 재스캔(스코프 9파일 확정·감사 누락 2 포착) → Worker 146건 재정합 → **CP2 Pass 9/9**(독립 Verifier — G2 §13 동결 침범 검출) → CP3(§13 HEAD 원복) 승인.
- **동결 보존 확립**: §9 이력 행 · discovery-binding §13 "실측 대조"(2026-07-07 스냅샷)는 §9 이력과 동류로 HEAD 보존. project-contract.v1.md·default-policy.yaml은 v1.2-era 잔존으로 유보.
- **다음 트랙 = 미정(사용자 결정)** — Advisor 권장 = **v1.2-era 잔존물 정리**(§4 (a)~(e)).
