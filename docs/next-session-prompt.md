# 다음 세션 부트스트랩 프롬프트 (형태 B Step Hosting — W0~W3 완주·Baseline 사용자 게이트 대기)

작성: Advisor · 2026-07-13 · 형태 B Step Execution Hosting 트랙 W3 마감 시점
용도: 새 세션에서 아래를 붙여넣으면 **추가 재조사 없이** 착수. (물리 발화 = `/uaf-continue`)
상태: **W0~W3 전 Wave 완주·커밋됨** (fbd1b0e → 2d4f948 → a45a3e1 → 94bc97e). **잔여 = Baseline 승격 사용자 게이트 + 게이트 후속(상태행 승격·ROADMAP 등재·repo Memory Update 마일스톤 마감 등록)** — 직전 세션이 Baseline 후보 보고를 제출했고, 사용자 응답이 있었는지 먼저 확인하라.

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

현재 트랙: 형태 B Step Execution Hosting — W0(설계)~W3(dogfooding E2E) 전부 완주·커밋.
버전/마일스톤 번호는 미확정 — 사용자가 부여한다(임의 결정 금지).

■ 트랙 결과 (전부 커밋·CP2 독립 판정 완료)
- W0 설계 정본(fbd1b0e): docs/form-b-step-hosting-design.md — D-1·D-2(3분리)·D-3 사용자 승인.
- W1 프로토콜(2d4f948): uahf/framework/runtime/step-hosting-protocol.md — W1 확정
  (CP2 1차 Fail 1[F-1 cross-layer 앵커] → 재작업 r2 → 재판정 Pass 5/0/0 · CP3).
  설계 정본 §6 ③ stale 배치 정정 포함(사용자 승인).
- W2 구현(a45a3e1): framework/loop/step-host/(중립 Host·unittest 17·AI/provider 토큰 0)
  + adapters/claude/step-hosting-binding.md(W2 확정) + step-invoker/(테스트 19·dangerously
  플래그 유일 소재). CP2 Pass 9 Met/0/0(실행 검증 포함) · CP3.
- W3 E2E(94bc97e): 필수 7 시나리오 전건 실증(실 CLI 21 세션·step-data/runs/ 8 run·
  append-only). CP2 Pass(시나리오 7/7·차원 4/4 Met) · CP3. s3 확장 사가 = blocked exit 2
  → Advisor 실해소(해소 이벤트 중복 append 정직 보존 — retry 예산 1 소모) → 라이브 CP2
  Fail(바이트 불일치 실검출) → retry-limit Escalated exit 2 → 해소#2 → 완주.
  s6 = Full UAF 진입(Contract v2 재사용·상위 재실행 0)에서 호스팅 sonnet Worker가
  claude_invoker.py O-1 결함을 실제 정정(hosted CP2 통과). 정합: loop-binding OQ-LB-2
  해소·workflow-binding OQ-WB-2 부분 해소·step-hosting-binding §7(OQ-SH-1 해소·OQ-SH-4/5
  신규)·protocol §9 W3 행(§7.3은 W1 스냅샷 보존·BPD-17).

■ 잔여 (이 순서로)
1. Baseline 승격 사용자 게이트 — 직전 세션 말미 Baseline 후보 보고에 대한 사용자 응답 확인.
   미응답이면 보고 요지 재제시 후 게이트 요청. 승인 시:
   (a) 상태행 승격 — step-hosting-protocol.md·step-hosting-binding.md의
       "Baseline 승격은 W3 사용자 게이트" 문구를 승인 사실로 갱신(§9 append 동반)
   (b) ROADMAP 등재(사용자가 부여한 버전/마일스톤 번호로)
   (c) repo Memory Update — 마일스톤 마감 등록(memory-data/ mi 신규·재발 판정·store 계수):
       후보 = ①해소 이벤트 중복 append 사건(콘솔 인코딩 실패가 출력 단계에서만 발생했는데
       부수효과[append 성공]를 미확정한 채 재시도 — 부분 실행 검증 교훈·재발 판정 필요)
       ②BPD 후보: 형태 B 무인 구동 E2E 패턴(BPD-14/20 확장 — 실 게이트 개입·append-only
       사가·CP2 라이브 실검출) ③L-26 후보(가칭): 해소=fail 계수 결합의 예산 파장(OQ-SH-5)
   (d) 핸드오프 최종 갱신·마감 커밋
2. 게이트 보류/거부 시: 사용자 지시 반영 후 위 절차 재조정.

■ 이월·Open (비차단 — 차기 트랙 후보 입력)
- OQ-SH-2(interactive의 headless 의미)·OQ-SH-3(stream-json) — 미실증 open.
- OQ-SH-4(CP2 모델 슬롯 결합 — Verifier 독립 모델 지정)·OQ-SH-5(Escalation 해소 전용
  어휘 부재·해소=fail 계수 결합) — W3 실측 관찰·후속 설계 판단.
- adapter-conformance notes 병기 — 설계 §2 "후보만"·판정 무영향이라 defer(이번 미수행).
- 설계 정본 §3.9 bare "04 §3.3" 표기(문서 내부 관례상 가독 문제·프로토콜은 정정됨) — 이월.
- E2E 드라이버 invoke 로그의 프로세스별 덮어쓰기(권위 기록 events.jsonl 무영향) — 드라이버
  개선 후보.
- 물리 동시 디스패치(병렬 집합 원소 동시 실행) — 동시성 invoker 후속 과제(OQ-WB-2 잔여 축).
- Contract v3 성숙 재발행(open 1·3항 부분 해소 반영) — E2E 완주했으므로 착수 가능해졌으나
  별도 성숙 run으로(선전제 금지·사용자 지시 대기).
- Superpowers Brainstorming/Planning UX Gap Analysis — Defer 유지.
- 기존 이월 인벤토리 승계: 02 §3.7 자기 불일치 · 03 bare "§3.7"·§7 done-11 stale ·
  CP1~CP3 인용 앵커(v1.3 §6 승계) · OQ-SD-2 · entry/discovery-binding 시제 서술 ·
  adapter-conformance §6 BP-16 행 stale · [T-b] harness-doc 경로 정규화 ·
  [T-c] AGENT/CLAUDE body 분할(L-14 CRLF hold) · Tier 3(물리 재배치·설치형 패키징).

■ 정독 순서 (재조사 금지)
1. git log --oneline -5 + git status (4 커밋 실재·clean 확인)
2. docs/form-b-step-hosting-design.md (설계 정본) — 필요 절만
3. uahf/framework/runtime/step-hosting-protocol.md §9 + step-hosting-binding.md §7·§9
4. Memory Consult([[uahf-session-entrypoint]]) + Contract 정독(project-contract.v2.md)
5. step-data/runs/ 은 증거 원본 — 수정 금지(append-only)

⚠️ 상시 원칙: 완전성 주장 전 전수 스윕·범위 명시(L-24) · 카운트 본문 재계수(L-25) ·
동결 in-place 금지(L-22) · 라우팅 표 정정(L-23) · Worker 완료 보고 불신·CP2 독립·CP3 승인 ·
버전/마일스톤 번호 임의 변경 금지 · working tree 사용자 변경사항 보존.
```

---

## 🪶 짧은 버전

> 형태 B Step Hosting: W0~W3 전부 완주·커밋(fbd1b0e→2d4f948→a45a3e1→94bc97e). 프로토콜(W1 확정)·중립 Host+claude 바인딩/invoker(W2 확정·테스트 36)·E2E 7 시나리오 전건 실증(실 CLI 21 세션·CP2 독립 Pass 7/7). 잔여 = **Baseline 승격 사용자 게이트**(응답 확인 먼저) → 승인 시 상태행 승격·ROADMAP(번호는 사용자 부여)·repo Memory Update 마감 등록·핸드오프 최종화.

---

## 현재 상태 스냅샷 (2026-07-13 W3 마감 시점)

- **HEAD = 94bc97e** (W3). 비커밋 = 본 핸드오프 재작성분만.
- **CP2 이력**: W1 1차 Fail 1(F-1)→r2→Pass 5/0/0 · W2 Pass 9/0/0(실행 검증) · W3 Pass(7/7·4/4). 전 판정 독립 Verifier 세션·Worker 보고 불신 규율 준수.
- **불변 준수**: Frozen spec 15종·루트 ARCH·04 무수정(C-1 위반 0) · step-host/ AI/provider 토큰 0(2개 독립 도구 교차) · dangerously 문자열 = claude Adapter 경계에만 · 형태 A 회귀 무손상(17+19 재실행 Pass) · append-only 전 run 무결(스키마 10필드 전수 검사).
- **게이트 실증**: Human Decision Gate가 unrestricted에서도 정지(s5b)·Advisor 실개입 해소 2회(s3)·CP3 물리 디스패치(s1) — UAF-INV ⑤ 물리 증거.
- **Contract**: pc-uahf-001 v2 현행(open 1·3항이 본 트랙으로 부분 해소 — v3 재발행은 별도 성숙 run).
