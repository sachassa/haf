# 다음 세션 부트스트랩 프롬프트 (Tier 2 — 「v1.2-era 잔존물 정리」 완결·다음 트랙 미정)

작성: Advisor · 2026-07-09 · v1.2-era 잔존물 정리 완결(a032c52) + Memory Update 직후
용도: 새 세션에서 아래를 붙여넣으면 재분석 없이 착수. (물리 발화 = `/uaf-continue`)
상태: **직전 트랙 완결(커밋 a032c52·CP2 Pass 5/5) — 다음 트랙 미정(사용자 선택 대기).**

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 트랙 「v1.2-era 잔존물 정리」가 완결되었다(커밋 a032c52·CP2 Pass 5/5·Memory Update
mi-0088~0090). v1.2.1 리팩토링(루트 uaf/ 소멸) 후 남은 stale 참조/라벨을 정정 라우팅
표(⚠️ 접두 치환 금지)로 정합했고, 동결 역사(측정 스냅샷·append-only 인스턴스·Revision
History)는 편집 없이 재베이스라인/보존했다. 다음 트랙은 미정이다.

먼저 다음 순서로 착수하라.

1. Read-First: ARCHITECTURE.md(v1.3 라우터 정본·§0 "uaf/ 소멸") · Memory Consult
   ([[uahf-session-entrypoint]] + Project Contract pc-uahf-001 정독).
   최신 트랙 상세=[[uahf-active-track-v1.2-era-cleanup]]. store 90·Active 22·Candidate 25.
2. git log --oneline + git status (…dc805be→5c47909→eb52266→963076d→a032c52→[Memory
   Update]·clean 실측).
3. ⚠️ 상시 원칙(L-22·L-23·BPD-17): 동결 영역(§9 이력·날짜 명시 "실측 대조" 스냅샷·
   append-only 인스턴스·Revision History)은 in-place 수정 금지 — 재측정/재베이스라인
   또는 supersede로만. 리팩토링 후 경로 정정은 접두 치환이 아니라 대상별 라우팅 표로.

다음 트랙 후보(사용자 선택 — 선취 금지):
  [T-a] 각 Layer 독립 ARCHITECTURE 완전 저술 — 현재 entry/·discovery/·planning/·knowledge/·
        uahf/ ARCHITECTURE.md 실재하나 완성도 편차. 라우터(루트 §2.1)와의 정합·상세화.
  [T-b] harness-doc 내부 약칭 정규화 pass — uahf/framework/** 내부 bare specs/·framework/
        (uahf-root-relative 약칭)·.claude/ bare specs/를 명시 경로로 정규화할지 여부·범위
        결정. (v1.2-era 정리에서 비대상으로 유보한 클래스.)
  [T-c] AGENT.md/CLAUDE.md body 분할 — L-14 hold 상태(편집 보류). 해제 조건·설계 선행.
  [T-d] Tier 3 착수 — 상태 분리 설계[브리프 C]·Layer 오케스트레이션 정식화·uaf:<layer>
        명령·Layer별 LLM·설치형 패키징(형태 B, Scaffold spec 12-scaffold Frozen v0.1).

4. 권장: 트랙 확정 후 plan mode로 계획 확정·승인 → Worker 위임 → Verifier CP2 → Advisor
   CP3 → 커밋.

작업 규칙: 구현 Worker(Opus) 위임 · 완료 보고 불신 · Verifier 독립 검증(CP2) ·
Advisor 승인(CP3) · 동결 스냅샷/append-only 바이트 보존(L-14 tr -dc 실측) · git 안전망 하.
```

---

## 🪶 짧은 버전 (이것만으로도 됨)

> v1.2-era 잔존물 정리 트랙 완결됐어(a032c52). 다음 트랙은 미정 — `[[uahf-session-entrypoint]]`
> Consult부터 하고, 다음 트랙 후보(각 Layer ARCHITECTURE 저술·harness-doc 약칭 정규화·
> AGENT/CLAUDE body 분할·Tier 3) 중 뭘 할지 정하자. 동결/append-only는 in-place 금지(L-22)·
> 리팩토링 후 경로 정정은 라우팅 표로(L-23).

---

## 현재 상태 스냅샷 (2026-07-09)

- **완결 직전 트랙**: v1.2-era 잔존물 정리. 진입 `/uaf-continue`(Incremental·행 8). 결정 D1~D4
  사용자 확정 → 9파일 정합(a)~(f)·(d) 동결 유지 무편집. CP2 Pass 5/5·CP3 승인·커밋 `a032c52`.
- **커밋 체인**: …`dc805be`→`5c47909`→`eb52266`→`963076d`→**`a032c52`**(정리)→**[이 커밋]**
  (Memory Update — mi-0088 Recurrence·mi-0089 L-23·mi-0090 BPD-17·store 87→90). 작업트리 clean.
- **최신 교훈**: L-23(리팩토링 후 정정=대상별 라우팅 표·접두 치환 금지)·BPD-17(동결 스냅샷
  재베이스라인=byte 보존+날짜 서브블록 append)·mi-0088(L-21 커널 3트랙 연속 재발 → L-21 승격
  근거 강화). L-22/L-23/BPD-17·L-21 승격 심사 대기.
- **다음 트랙 = 미정** — 후보 [T-a]~[T-d] (위 프롬프트). 사용자 선택.
- **남은 Tier 2**: 각 Layer 독립 ARCHITECTURE 저술·AGENT/CLAUDE body 분할(L-14 hold)·harness-doc
  약칭 정규화. **Tier 3**: 상태 분리·오케스트레이션·uaf:<layer>·Layer별 LLM·설치형 패키징(형태 B).
