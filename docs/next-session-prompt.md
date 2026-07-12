# 다음 세션 부트스트랩 프롬프트 (Tier 2 잔여 [T-b]·[T-c] — T-a 완결 후)

작성: Advisor · 2026-07-12 · Tier 2 T-a(Layer ARCHITECTURE 4개 저술) 완결 직후
용도: 새 세션에서 아래를 붙여넣으면 재분석 없이 착수. (물리 발화 = `/uaf-continue`)
상태: **T-a 완결·커밋 `d14788d`·밀레스톤 Memory Update 완료(mi-0092~0094). 잔여 = Tier 2 [T-b]·[T-c] 택1.**

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 세션에서 Tier 2 T-a(각 Layer 독립 ARCHITECTURE 완전 저술)를 완결했다
(커밋 d14788d — entry/discovery/planning/knowledge 4파일·exemplar-first 2-Wave·
CP2 4/4 Pass 10/0/0). 밀레스톤 Memory Update 완료(mi-0092~0094·store 94).
이제 Tier 2 잔여 [T-b]·[T-c] 중 하나를 한다.

먼저 다음 순서로 착수하라.

1. Read-First: ARCHITECTURE.md(v1.3 라우터 정본·§2.1 지도) · Memory Consult
   ([[uahf-session-entrypoint]] + Project Contract pc-uahf-001 정독).
   store 94·Active 22·Candidate 28. 직전 트랙 상세=[[uahf-active-track-ta-layer-arch]].
2. git log --oneline + git status (…d27c472→d14788d→(Memory Update 커밋)·clean 실측).
3. ⚠️ 상시 원칙:
   - 완전성·사실 주장 규율(L-24·CLAUDE.md 규율절): "정확히 N·전수·잔여 0" 주장 전
     관련 패턴 전수 스윕·검색 범위 명시. 단일 좁은 스캔 exhaustive 단정 금지.
   - 정본 카운트 인용은 §9 이력/요약 아닌 §N 본문 열거 재계수(L-25 — T-a 부수검출).
   - 동결 영역(§9 이력·날짜 실측 스냅샷·append-only)은 in-place 금지(L-22)·재측정/supersede만.
   - 리팩토링 후 경로 정정은 접두 치환 아닌 대상별 라우팅 표(L-23).
   - 다수 파일 균일 저술은 exemplar-first 파일럿→동결→팬아웃(BPD-18 — T-a 실증).

Tier 2 잔여 2항목(사용자 택1 — 선취 금지):
  [T-b] harness-doc 내부 약칭/경로 정규화 pass : uahf/framework/**·.claude/ 내부 bare
        specs/·framework/(uahf-root-relative 약칭) 및 **bare `AGENT.md` vs `.claude/AGENT.md`
        경로**(T-a 이월)를 "유지 vs 명시" 결정·정리. 저위험·저효용.
  [T-c] AGENT.md/CLAUDE.md body 분할 : 한 파일의 GD(공통) 부분과 U(프로젝트 특정) 부분 분리.
        ⚠️ L-14 CRLF hold — disk=CRLF·blob=LF 위험. 편집 전 git 스냅샷·후 diff로
        additive/의도 라인만 확인.

4. 택1 후: plan mode로 계획 확정·승인 → Worker 위임 → Verifier CP2 → Advisor CP3 → 커밋.

작업 규칙: 구현 Worker(Opus) 위임 · 완료 보고 불신 · Verifier 독립 검증(CP2) ·
Advisor 승인(CP3) · 동결/append-only 바이트 보존(L-14 tr -dc 실측) · git 안전망 하.
```

---

## 🪶 짧은 버전 (이것만으로도 됨)

> Tier 2 T-a(Layer ARCHITECTURE 4개) 끝났어(d14788d). `[[uahf-session-entrypoint]]`
> Consult부터 하고, Tier 2 잔여 [T-b](경로/약칭 정규화·AGENT.md 경로 포함)·[T-c](AGENT/CLAUDE
> body 분할[L-14 hold]) 중 뭘 할지 정하자. 완전성·카운트 주장은 본문 재계수 후(L-24·L-25).

---

## 현재 상태 스냅샷 (2026-07-12)

- **직전 완료**: Tier 2 T-a Layer ARCHITECTURE 4개 저술(`d14788d`·CP2 4/4 Pass 10/0/0) →
  밀레스톤 Memory Update(mi-0092 recurrence-judgment Novel·mi-0093 BPD-18·mi-0094 L-25).
- **T-a 요약**: exemplar-first 2-Wave — W1 entry 파일럿→독립 CP2/CP3→스켈레톤 A 동결→
  W2 discovery/planning/knowledge 3-병렬→각 CP2 Pass 10/0/0. rework 0. 개관 고도(하위
  spec 01/02/03 복제 0)·라우터 §2.1 정합·knowledge=1차 정본(스켈레톤 B). bare AGENT.md·
  `<adapter>` 플레이스홀더·§2 실측·CR 0·`uahf/**` 무촉·spec 버전 무상승.
- **커밋 체인**: …`d27c472`(T-D1)→**`d14788d`**(T-a 4파일)→(Memory Update 커밋). 작업트리 clean.
- **⭐ T-a 부수검출(이월)**:
  - (i) **AGENT.md 코퍼스 경로**: 정본 형제 전부 bare `AGENT.md`이나 실경로는 `.claude/AGENT.md`
    (루트 `AGENT.md` 미존재). T-a는 코퍼스 일관 위해 bare 표준 계승 — 경로 정확화는 **T-b 소관**.
  - (ii) **Frozen `03-project-contract.md` 내부 불일치**: §9 이력=`PC-INV 11건` vs §3.6 본문=
    1~12=12 고유. planning ARCH는 본문 인용해 무결. **03 정정은 Frozen 개정 규율(버전 상승+
    Revision History) 소관** — 별도 트랙.
  - (iii) **discovery §4 위상 체인**: 5노드 표기·"비종단 6상태" 라벨(6번째 `Initiated`=인스턴스화
    상태로 흐름 제외·비결함). 명료화는 선택.
- **[T-b]·[T-c] 택1이 Tier 2 잔여의 마지막.** 이후 **Tier 3(북극성)**: 상태분리 설계·Layer
  오케스트레이션 정식화·`uaf:<layer>` 명령·Layer별 LLM·설치형 패키징(형태 B = Scaffold spec
  12-scaffold Frozen v0.1·구현 미착수). **agents·commands·model override 물리 이동은 전부
  형태 B(Tier 3) 소관** — 환경이 루트 .claude/만 로드하므로 그 전엔 물리 이동 금지.
- **최신 교훈**: BPD-18(exemplar-first 2-Wave)·L-25(정본 카운트=본문 재계수 인용)·L-24(완전성
  주장 전 전수 스윕·자기 주장도 검증)·L-23(라우팅 표)·BPD-17(재베이스라인). L-21 커널 4연속
  재발 → 승격 근거 강화. L-21~L-25·BPD-17·BPD-18 승격 심사 대기.
