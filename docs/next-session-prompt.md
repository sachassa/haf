# 다음 세션 부트스트랩 프롬프트 (Tier 2 — 「v1.2-era 잔존물 정리」 채택·착수 대기)

작성: Advisor · 2026-07-09 · 루트 ARCHITECTURE v1.3 재저술 완결(dc805be) + 사용자 트랙 채택 직후
용도: 새 세션에서 아래를 붙여넣으면 재분석 없이 착수. (물리 발화 = `/uaf-continue`)
상태: **트랙 채택됨(사용자, 2026-07-09) — 착수 전 결정 4건 확정 후 plan → Worker → Verifier(CP2) → CP3.**

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 트랙 「루트 ARCHITECTURE v1.3 완전 재저술 + 하위 §앵커 정합」이 완결되었다(크래시
복구·커밋 dc805be·CP2 Pass 9/9). 그 트랙은 TIGHT 스코프였고, 함께 발견된 v1.2-era
선재 부채를 후속으로 유보했다. 사용자가 다음 트랙으로 「v1.2-era 잔존물 정리」를 채택했다.

먼저 다음 순서로 착수하라.

1. Read-First: ARCHITECTURE.md(v1.3 라우터 정본·§0 "uaf/ 소멸") · [[uahf-active-track-arch-v1.3-rewrite]]
   (유보 잔존물 인벤토리 (a)~(e) 보유) · Memory Consult([[uahf-session-entrypoint]] +
   Project Contract pc-uahf-001). store 87·Active 22·Candidate 23(+L-22).
2. git log --oneline + git status (…dc805be→5c47909→eb52266·clean 실측).
3. ⚠️ 핵심 원칙(L-22·L-06/L-20): 동결 영역(§9 이력·날짜 명시 "실측 대조" 스냅샷·
   append-only 인스턴스)은 in-place 수정 금지 — 재측정/재베이스라인 또는 supersede로만 갱신.

정리 대상 인벤토리(실측 확정):
  (a) dogfooding "실측 대조" 표가 루트에 uaf/·specs/·docs/ 존재라고 서술(리팩토링 후 사실 오류)
      — entry-binding.md §10(226-245) · discovery-binding.md §13(340-360). **2026-07-07 동결
      스냅샷** → 단순 치환 금지, 현시점 재측정으로 **재베이스라인**(날짜·상태 갱신).
  (b) default-policy.yaml 헤더 stale 경로 `uaf/specs/02-discovery.md §3.15`(editable config).
  (c) discovery/specs/02:485 · planning/specs/03:289 의 `ARCHITECTURE.md 5.1`(Memory Service)
      → `uahf/ARCHITECTURE.md §5.1` (uahf/ARCHITECTURE.md 실재 확인됨; §5.1 Memory Service 절
      실재 여부 확인 후 정정). Memory Service 정본 = uahf/specs/00-glossary §3.2-C·04-memory.
  (d) project-contract.v1.md(instanceVersion:1) stale `uaf/specs/` 3곳(43·63·87) — append-only
      동결 인스턴스, in-place 편집 금지.
  (e) 'uaf/ 정본'·'uaf/specs/ 경계' 개념어 7+곳(adapter-conformance 1·contract-binding 2·
      discovery-binding 2·entry-binding 2) — §0 "uaf/ 소멸"과의 정합 정책.
  (f) stale 카테고리 라벨 `specs/`·`framework/`(→ uahf/specs/·uahf/framework/) 다수 산재
      (예: `specs/00-glossary.md §3.2-C`, discovery/02:10·64·485·planning/03:12 등).

4. 착수 전 확정할 결정 4건(사용자 확인 — 선취 금지):
   D1 (a) 재베이스라인 방식: 현시점 재측정으로 §10/§13을 갱신(날짜·상태) vs 2026-07-07
      스냅샷 보존 + 새 일자 재측정 행 추가. (동결 역사 보존 원칙과 정합 방식 선택)
   D2 (d) 동결 Contract 인스턴스: **동결 유지(권장 — 역사 기록, §9 이력 동류)** vs supersede v2 발행.
   D3 (e) 개념어 정책: align(현행 경계 표현으로 정정) vs keep(설계 네임스페이스 라벨로 유지).
   D4 (f) 카테고리 라벨 클래스: 이번 트랙에 포함 vs 별도 트랙 분리(범위 관리).

5. 권장: plan mode로 계획 확정·승인 후 → Worker 위임 → Verifier CP2 → Advisor CP3 → 커밋.

작업 규칙: 구현 Worker(Opus) 위임 · 완료 보고 불신 · Verifier 독립 검증(CP2) ·
Advisor 승인(CP3) · 동결 스냅샷/append-only 바이트 보존(L-14 tr -dc 실측) · git 안전망 하.
```

---

## 🪶 짧은 버전 (이것만으로도 됨)

> v1.2-era 잔존물 정리 트랙 채택됐어. `[[uahf-active-track-arch-v1.3-rewrite]]`의 유보 인벤토리 (a)~(f)
> 읽고, 착수 전 결정 4건(재베이스라인 방식·동결 인스턴스 거버넌스·개념어 정책·카테고리 라벨 범위)
> 확인부터 해줘. 동결 스냅샷/append-only는 in-place 금지(L-22)·재측정/supersede로만.

---

## 현재 상태 스냅샷 (2026-07-09)

- **완결 직전 트랙**: 루트 ARCHITECTURE v1.3 재저술 + 하위 §앵커 정합(크래시 복구). CP2 Pass 9/9·CP3·커밋 `dc805be`.
- **커밋 체인**: …`dc805be`(§앵커 정합)→`5c47909`(부트스트랩)→**`eb52266`**(Memory Update — mi-0086 재발판정 Novel·mi-0087 L-22 Candidate). 작업트리 clean.
- **채택 트랙 = 「v1.2-era 잔존물 정리」**(사용자 2026-07-09) — 착수 전 결정 4건(D1~D4) 확정 필요.
- **관련 발견**: `uahf/ARCHITECTURE.md` 실재(라우터 분기 Layer ARCHITECTURE 저술됨) → (c) 처리 가능. (f) 카테고리 라벨 클래스가 (a)~(e)보다 넓게 산재.
- **남은 Tier 2(후속)**: 각 Layer 독립 ARCHITECTURE 저술 · AGENT/CLAUDE body 분할(L-14 hold). **Tier 3**: 상태 분리·오케스트레이션·uaf:<layer>·Layer별 LLM·설치형 패키징(형태 B).
