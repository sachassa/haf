# 다음 세션 부트스트랩 프롬프트 (마일스톤 v1.5 형태 B Step Hosting — Baseline 확정·트랙 완결)

작성: Advisor · 2026-07-13 · v1.5 마감 시점
용도: 새 세션에서 아래를 붙여넣으면 **추가 재조사 없이** 착수. (물리 발화 = `/uaf-continue`)
상태: **마일스톤 v1.5 「형태 B Step Execution Hosting」 Baseline 확정 — 사용자 승인 2026-07-13** (Baseline 게이트·번호 부여 게이트 통과). W0~W3 완주·상태행 승격·ROADMAP 2종 v1.5 등재·repo Memory Update 마감(store 98→102). **트랙 완결 — 다음 트랙은 사용자 지시 대기.**

---

## 붙여넣을 프롬프트

```
너는 Universal Agentic Framework(UAF/UAHF)의 메인 Advisor다.

직전 완결 트랙: 마일스톤 v1.5 「형태 B Step Execution Hosting」 — Baseline 확정
(사용자 승인 2026-07-13). 커밋 체인: fbd1b0e(W0 설계) → 2d4f948(W1 프로토콜) →
a45a3e1(W2 구현) → 94bc97e(W3 E2E+정합) → e22d2ff(핸드오프) → [Baseline 확정 커밋]
→ [Memory Update 커밋].

■ v1.5 결과 요지
- 형태 B 실행 코드 첫 도입: framework/runtime/step-hosting-protocol.md(v1.5 Baseline·
  SH-INV 8·Frozen spec 개정 0) · framework/loop/step-host/(중립 Host·AI/provider 토큰 0·
  unittest 17) · adapters/claude/step-hosting-binding.md(v1.5 Baseline)+step-invoker/
  (dangerously 유일 소재·테스트 19).
- dogfooding E2E 7 시나리오 전건 실증(실 CLI 21 세션·step-data/runs/ 8 run·append-only):
  게이트 등급 분리(unrestricted에서도 Escalated 정지)·deterministic resume(replay 해시
  동일)·retry feedback 재주입·CP3 물리 디스패치·Full UAF 상위 재실행 0·Standalone 분기·
  s3 게이트 실개입 사가(정지 2회·Advisor 해소 2회·라이브 CP2 실검출 1회).
- CP2 3회 전건 독립 Pass(W1 재판정 5/0/0·W2 9/0/0 실행 검증·W3 7/7+4/4)·CP3 승인.
- Memory Update: mi-0099(Recurrence — cross-layer bare 라벨·L-20/L-22 커널)·
  mi-0100(Novel — 부수효과 미확정 재시도)·mi-0101(L-26 Candidate)·mi-0102(BPD-21
  Candidate — 형태 B 무인 E2E 패턴). store 102.

■ 다음 트랙 후보 (착수는 사용자 지시 — 임의 착수 금지)
1. Contract v3 성숙 재발행 — v2 open 1·3항이 v1.5로 부분 해소됨·별도 성숙 run
   (BPD-20 패턴·04-solution-design 정본).
2. OQ-SH 후속 설계 — OQ-SH-2(interactive headless 의미)·SH-3(stream-json)·
   SH-4(CP2 모델 슬롯 독립 지정)·SH-5(Escalation 해소 전용 어휘 — 해소=fail 계수 결합
   해체)·물리 동시 디스패치(동시성 invoker — OQ-WB-2 잔여 축).
3. 실제 외부 프로젝트 적용(Contract intent "실용화" — 형태 B 도입 완료로 착수 가능).
4. Tier 2 잔여 [T-b] harness-doc 경로 정규화 · [T-c] AGENT/CLAUDE body 분할(L-14 hold).
5. 유지보수 일괄 — 이월 인벤토리(아래) 정리 트랙.

■ 이월 인벤토리 (비차단·승계)
- 설계 정본 §3.9 bare "04 §3.3" 표기(프로토콜은 정정됨·문서 내부 가독) ·
  adapter-conformance notes 병기 defer · E2E 드라이버 invoke 로그 프로세스별 덮어쓰기 ·
  02 §3.7 자기 불일치 · 03 bare "§3.7"·§7 done-11 stale · CP1~CP3 인용 앵커(v1.3 §6 승계) ·
  OQ-SD-2 · entry/discovery-binding 시제 서술 · conformance §6 BP-16 행 stale ·
  settings.json stale(v1.4 검출) · Superpowers Gap Analysis Defer · Tier 3(물리 재배치·
  설치형 패키징).

■ 정독 순서 (재조사 금지)
1. git log --oneline -7 + git status
2. Memory Consult([[uahf-session-entrypoint]]) + Contract 정독(project-contract.v2.md —
   최고 instanceVersion)
3. 필요 시: docs/form-b-step-hosting-design.md·step-hosting-protocol.md §9·
   step-hosting-binding.md §7(OQ 잔여)
4. step-data/runs/ 는 증거 원본 — 수정 금지(append-only)

⚠️ 상시 원칙: 완전성 주장 전 전수 스윕·범위 명시(L-24) · 카운트 본문 재계수(L-25) ·
동결 in-place 금지(L-22) · 라우팅 표 정정(L-23) · 부수효과 실측 확정 후 재시도(L-26
Candidate — 비멱등 연산) · Worker 완료 보고 불신·CP2 독립·CP3 승인 · 버전/마일스톤 번호
임의 변경 금지 · working tree 사용자 변경사항 보존.
```

---

## 🪶 짧은 버전

> **v1.5 형태 B Step Execution Hosting Baseline 확정(사용자 승인 2026-07-13)·트랙 완결.** 실행 코드 첫 도입(프로토콜+중립 Host+claude 바인딩/invoker)·E2E 7/7 실 CLI 실증·CP2 3회 전건 Pass·ROADMAP v1.5 등재·Memory store 102. 다음 트랙 = 사용자 지시 대기(후보: Contract v3 성숙 run·OQ-SH 후속·외부 프로젝트 적용·T-b/T-c·유지보수 일괄).

---

## 현재 상태 스냅샷 (2026-07-13 v1.5 마감)

- **정본 상태**: step-hosting-protocol.md = v1.5 Baseline · step-hosting-binding.md = v1.5 Baseline · loop-binding OQ-LB-2 해소·workflow-binding OQ-WB-2 부분 해소(버전 무상승) · Frozen spec 15종·루트 ARCH·04 무수정(C-1 위반 0).
- **게이트 실증 물리 증거**: s5b(unrestricted에서 Escalated 정지)·s3(Advisor 실개입 해소 2회·exit 2 캡처)·s1(CP3 배치 종단 디스패치 cp3-result.json) — UAF-INV ⑤.
- **Contract**: pc-uahf-001 v2 현행(open 1·3항 v1.5로 부분 해소 — v3 재발행은 별도 성숙 run·사용자 지시 대기).
- **Memory**: store 102·index 102(순수 append +4)·Candidate에 L-26·BPD-21 추가(승격 심사 대기)·기존 mi-0001~0098 무변경.
