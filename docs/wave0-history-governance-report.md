# Wave 0 — 문서 개정 기록 거버넌스 정본 개정 · Worker 보고 전문 (r2)

수임: Worker (Advisor 위임) · 일자 2026-07-27
근거 권위: 사용자 결정 2026-07-27(파일 내 이력 절 폐지 · 기록 locus = git · 전체 md 예외 없음) + Advisor 재작업 판정 R1~R6
수명 등급 = `evidence` (`docs/artifact-lifecycle-policy.md` §2·§3·§5)

> **주의(축약 도구 대상 아님).** 이 파일은 문서 개정 기록 절이 아니라 **보고 전문**이다. 헤딩에 축약 도구 탐지 토큰을 두지 않는다 — r1 에서 H1 제목이 오탐되어 191줄이 축약 대상으로 잡혔고, r2 에서 제목·소절 표제를 재작성해 해소했다(§6-2).

---

## 1. 착수 전 점검

- 필수 7필드(from/to/task/input/output/done/context) 7/7 존재.
- done 이진 판정 가능 — r1 시점 5/6(④ 전제 결함), **r2 시점 6/6**(R3 판정으로 ④ 종결).
- context 경로 5/5 실재. r2 추가 대상 파일 8건 모두 직독 후 편집.

병렬 집합 위임 아님 → 이탈 선언 비해당.

---

## 2. r1 변경 요지 (파일별)

### 2.1 루트 `ARCHITECTURE.md`

| 지점 | 변경 |
|---|---|
| 머리 상태 라인(:3~4) | `v1.7 (개정 — §6 설계 원칙 12 신설)`. 개정 경위 locus 를 §9 표 → **git(커밋·앵커)**로 표기 전환 + 운용 정본·원칙 근거 포인터 병기 |
| §6 표제(:184) | `Design Principles — 11종` → `12종` |
| §6 도입문(:186) | "다음 11종 원칙" → "다음 12종 원칙" |
| §6 원칙 12 신설 | **자기 문서 경량 (Self-Documentation Frugality)** — UAF는 다른 제품을 만드는 도구다 / 파일 본문 = 제품 생성에 필요한 실행 규범만 / 이력·경위·근거 전문은 git 보존 / UAF 자체 개정 시에만 앵커 참조 / 삭제는 정보 손실이 아니다 / 운용 정본 = `docs/spec-versioning-policy.md` §3 |
| §9 하단 관행 주석(:35) | "이 표에 append-only로 기록한다" → **"이 표가 아니라 git 커밋에 기록한다"** + 폐지 전 기록 표기. 기존 legacy 사유 보존 |

### 2.2 `docs/spec-versioning-policy.md`

머리 상태 라인 · 근거 정본 3행 · 거버넌스 · §0 · §1 · §3.1 · §3.2 표 (A)(B) · §3.2 본문 · §3.3 · **§3.4 대개정** · §4(d) · §5 · §6 요약 · §9 주석 — 총 15지점.

- **§3.2 (A)**: "Revision History에 append한다" → "개정의 취지·범위를 **git 커밋 메시지에 기록**한다". 버전 상승·§4 선행·비호환 시 사용자 승인 요건 **무변**.
- **§3.2 (B)**: "이력 append + 상태 라인 갱신" → "**git 커밋 기록 + 상태 라인 갱신**".
- **§3.1**: 신설 단락 「기록의 locus = git이다」.
- **§3.4**: 표제 `Revision History 관례 (L-10 명문화)` → `개정 기록 관례 (L-10 재정의 — 기록 locus 이전)`. 취지 유지 / 수단 이전(파일 내 문면 불변·append-only → git 커밋 불변성) / 폐지 형태 / **경계**.
- **§3.4 경계**(코디네이터 정정 반영): ARCHIVE 앵커 원장 언급 **제거**. 유지 대상 2건만 — ① run 원장(`RevisionEvent`·`ArtifactRecord`, 정본 05) ② 계약 인스턴스 계보(v1→v2→v3 파일 버전 체인·`supersedes`, 정본 03 §3.4·PC-INV 9). 근거 = "문서 이력이 아니라 제품 생성 동작의 부품". 계보 ≠ 파일 내 이력 절 혼동 방지 문면 포함.

### 2.3 `uahf/framework/core/structure.md` · 2.4 `uahf/framework/memory/lessons.md`

각각 거버넌스 라인(:13 / :14)과 관행 주석(:42 / :35)을 git locus 문면으로 교체. §9 표 행 삭제 0 · 새 행 append 0.

---

## 3. r2 변경 요지 (Advisor 판정 R1~R6)

### 3.1 R1 — §9 밖 거버넌스 라인 전건 교체 (27파일)

- **수단**: 결정적 스크립트(정규식 치환·LLM 0). 대상 문면 = `개정은 Advisor 승인 + (본 문서 )?§9 이력 절 기록으로만 이뤄진다( (docs )?운용 문서 거버넌스 관행)?.`
- **신 문면**: `개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = docs/spec-versioning-policy.md §3).`
- **결과**: 파일 27건 · 치환 27건 · EXIT=0. 각 파일 1건씩(중복 0).
- **실측 검증**: 교체 후 동일 패턴 재grep → **규범 문서 잔존 0건**. 잔여 5건은 전부 본 보고서 내부의 전후 문면 인용이다.
  `uaf-verified: 치환 전후로 grep -rn --include=*.md "이력 절 기록으로만" 을 리포 루트에서 실행하고 잔여 5건을 개별 열람해 전부 본 보고서 소속임을 확인했다. 검색 범위 = 저장소 전 .md(.git 제외).`
- **대상 27파일**: `docs/artifact-lifecycle-policy.md` · `orchestration/specs/05-project-orchestration.md` · `uahf/framework/core/config-schema.md` · `loop/{loop-protocol,loop-state-record,module-manifest,stage-transition-rules}` · `memory/{memory-service,memory-store,module-manifest}` · `plugins/{module-manifest,plugin-lifecycle,plugin-manifest}` · `runtime/{lifecycle,module-manifest,module-registry,step-hosting-protocol}` · `verifier/{criteria-catalog,module-manifest,rework-instruction,verification-report,verifier-protocol}` · `workflow/{decompose-rules,dispatch-protocol,merge-rules,module-manifest,work-graph}`

### 3.2 R2 — `rework-instruction.md` L-10 인용 3지점

| 행 | 인용 취지 판정 | 처리 |
|---|---|---|
| :18 근거 정본 | 사후 왜곡 금지 | 취지 유지 + 근거 재지정 → "안정 근거 = L-10(**시점 기록의 사후 왜곡 금지**) — 실현 수단 현행 정본 = spec-versioning-policy §3.4(기록 locus = git)" |
| :31 | 이력 행(분류 iii) | **무촉** |
| :106 실사례 근거 | 사후 왜곡 금지 | :18과 동형 재지정 |
| §4 규칙 2번째 불릿 | 시점-스코프 기록 제외 | 예시에서 "이력 행(§9 Revision History)" 제거, "인용·교정 경위 + git 커밋 메시지·앵커가 보존하는 개정 기록"으로 재열거 |
| §4 규칙 3번째 불릿 | **"파일 내 행 불변" 자체** | **신규범 문면으로 교체** — 표제 "이력 행 append-only 불변" → "**시점 기록의 사후 왜곡 금지**". 보호 주체를 파일 규율 → 버전 관리 시스템으로 이전. 재검증 기준을 "라이브 본문 교정 + 개정 취지를 커밋에 기록"으로 재서술 |

### 3.3 R4 — Frozen 계약 개정 4파일

신 §3 절차 적용: **버전 상승 + 상태 라인 갱신 + git 커밋 기록**(커밋은 Advisor 소관). **새 이력 행 append 0건**.

| 파일 | 버전 | 전 문면 | 후 문면 |
|---|---|---|---|
| `uahf/specs/00-glossary.md` :285 (§3.2-G) | 0.2 → **0.3** | `Frozen — v0.1 기준선 확정. 이후 변경은 spec 버전 상승과 Revision History 기록이 필수다.` | `Frozen — v0.1 기준선 확정. 이후 변경은 spec 버전 상승과 **개정 기록**이 필수다(기록 locus = git 커밋 — 운용 절차 정본 = docs/spec-versioning-policy.md §3).` |
| `uahf/specs/TEMPLATE.md` :119 (§4 Status 전이) | 0.1 → **0.2** | `Frozen: v0.1 기준선 확정 — 이후 변경은 spec 버전 상승과 Revision History 기록이 필수다.` | `… spec 버전 상승과 **개정 기록**이 필수다(기록 locus = git 커밋 — 운용 절차 정본 = docs/spec-versioning-policy.md §3).` |
| `uahf/specs/TEMPLATE.md` §1 사용 규칙 | 동상 | (해당 규칙 부재) | **불릿 신설** — 개정 이력을 파일 안에 절로 두지 않는다 / 파일이 담는 것은 §0 Header 상태 라인(Version·Status)뿐 / 이력 절 헤딩을 남기면 **git 포인터 1줄 스텁**만 허용 / 정본·원칙 근거 포인터 |
| `uahf/specs/TEMPLATE.md` `# 5.` 절 | 동상 | (항목 3행만) | 절 **보존**하고 머리에 신규범 1줄 추가 — "이후 개정은 이 절이 아니라 git 커밋에 기록한다" + legacy 사유. **항목 행 삭제 0** |
| `uahf/specs/08-hooks.md` :185 | 0.1 → **0.2** | `한 번 공개된 Event ID의 변경·삭제는 spec 버전 상승과 Revision History 기록을 요구한다.` | `… spec 버전 상승과 **개정 기록**을 요구한다(기록 locus = git 커밋 — 운용 절차 정본 = docs/spec-versioning-policy.md §3).` |
| `planning/specs/03-project-contract.md` :204 | v1.2 → **v1.3** | `**스키마 개정 = spec 버전 상승 + Revision History.** … **본 문서(spec)의 버전 상승 + §9 Revision History append**로만 이뤄진다. … (TEMPLATE.md §5 Revision History).` | `**스키마 개정 = spec 버전 상승 + 개정 기록.** … **본 문서(spec)의 버전 상승 + git 커밋 기록**(취지·범위를 커밋 메시지에)으로만 이뤄진다. … (기록 locus 정본 = docs/spec-versioning-policy.md §3 — 파일 내 이력 절은 폐지됨).` + **하위 불릿 신설**(이 항 = 문서 개정 기록이며 §3.4 인스턴스 계보 append-only 와 혼동 금지) |
| `planning/specs/03-project-contract.md` :358 | 동상 | `… 본 spec 버전 상승 + §9 Revision History append를 거친다(§3.3-E).` | `… 본 spec 버전 상승 + git 커밋 기록을 거친다(§3.3-E).` |

**부수 확인(중요)**: TEMPLATE 이 규정하는 spec 필수 구조 §0~§9 에서 **§9 = Open Questions** 이며, Revision History 절은 **필수 구조에 없다**. 즉 spec 파일의 이력 절은 TEMPLATE 강제가 아니라 관행(structure.md 계열)에서 왔다. §0 Header 규정은 이미 상태 라인(Version·Status)만 요구하므로 **필수 구조는 신규범과 이미 정합**이다.
`uaf-verified: TEMPLATE.md 의 헤딩 전체를 grep "^#" 로 열거하고 §0~§9 각 표제와 # 1~# 5 메타 절을 직독해 확인했다. 검색 범위 = uahf/specs/TEMPLATE.md 전문.`

### 3.4 R5 — 배포 템플릿

`uahf/framework/adapters/claude/scaffold-template/specs/README.md` :13 — "변경은 spec 버전 상승과 Revision History 기록이 필수다" → "**개정 기록**이 필수다 … **기록 locus = git 커밋**이다 — spec 파일에는 상태 라인만 두고 취지·범위는 커밋 메시지가 보존하며, 파일 안에 이력 절을 두지 않는다 (TEMPLATE.md §1 사용 규칙)". 소비 제품에 신규약이 전파된다.

### 3.5 R3 — 무촉 확정 (조치 없음)

L-10 원장 `memory-data/store/mi-0027.json`(및 `mi-0023.json`) **무촉**. 개정·supersede 등록 모두 미수행. 살아있는 규범 소유는 `spec-versioning-policy.md` §3.4가 가져갔고, live 인용처 정합(R2)으로 종결. `lessons.md`는 :14·:35 외 추가 조치 없음. **r1 failure ④ 종결**.

### 3.6 R6 — 스텁 형태 대조

도구 상수 `STUB_TEMPLATE`를 직독했다. 실물 형태 = **절 헤딩 보존 + 1줄 스텁**이고 스텁은 ① 그 파일 경로의 git log ② 제거 전 전문 앵커 ③ 규범 § 포인터(`docs/spec-versioning-policy.md` §3) ④ "UAF 자체 개정 시에만 참조" 용법을 담는다. 정책 §3.4의 종전 서술("헤딩 + git 포인터 1줄 스텁")과 **모순 0**이나 형태가 덜 구체적이었으므로 §3.4를 위 4요소 **형태 요건**으로 정밀화했다 — **문자열 사본은 두지 않았다**(재정의 0, 정본 = 실행 도구).

---

## 4. 토큰 스윕 — 3분류 (r2 갱신)

**스윕 수단** = `L-10`·`append-only`·`Revision History`·`이력 append` 리포 전체 grep → 규범 프로즈 패턴 6종으로 재스윕 → 군 단위 분류.
`uaf-verified: 위 4토큰과 6패턴을 리포 루트 grep 으로 실행하고 히트를 파일·행 단위로 열람해 분류했다. 검색 범위 = 저장소 전 .md + .py/.json/.jsonl 별도 확인. 한계 = 원시 append-only 토큰은 100+ 파일에 분포하며 전 히트를 1건씩 열람하지 않고 헤딩·이력 행 패턴으로 군 분류했다.`

| 군 | 히트 | 분류 | r2 처리 |
|---|---|---|---|
| A-1~A-4 | 4파일(루트 ARCH·정책·structure·lessons) 내 규범 지점 | (i) | **정합 완료**(r1) |
| A-5 | §9 밖 거버넌스 라인 **27파일** | (i) | **정합 완료(R1)** — 잔존 0 실측 |
| A-6 | §9 블록 **내부** 관행 주석 **56파일** | (i) | **무촉 유지** — 절 축약과 함께 소멸(도구가 커버) |
| A-7 | `rework-instruction.md` :18·:106·§4 2불릿 | (i) | **정합 완료(R2)** |
| A-8 | `artifact-lifecycle-policy.md` :13 | (i) | **정합 완료(R1에 포함)**. :11 L-10 인용·:23 관행 주석은 A-6/무해 인용 |
| B-1 | 05 RevisionEvent·ArtifactRecord | (ii) | **무촉** — §3.4 경계 ① |
| B-2 | 03 PC-INV 9·§3.4 계보 | (ii) | **무촉** — §3.4 경계 ② (+ :204 하위 불릿으로 혼동 방지 명시) |
| B-3 | `ARCHIVE.md` 앵커 원장 | (ii) | **무촉**, 단 §3.4 문면에서 언급 **제거**(정정 2항) |
| B-4 | Memory Item 원장(store/index) | (ii) | **무촉**(R3 확정) |
| B-5 | 엔진 코드·run 원장 jsonl·logs | (ii) | **무촉** |
| C-1~C-4 | 각 문서 §9 표 행·과거 정정 기록(03:29 등) | (iii) | **무촉**(문면 불변) |
| D-1~D-6 | Frozen 계약 문면 6지점 | (r1 = 별도 게이트) | **정합 완료(R4·R5)** — §5 |

---

## 5. Frozen 정의 인용·긴장 — r2 종결 상태

**r1 판정**(직독 인용, `uahf/specs/00-glossary.md:285` §3.2-G):

> - Frozen — v0.1 기준선 확정. 이후 변경은 spec 버전 상승과 Revision History 기록이 필수다.

r1 판정 = **긴장 있음(fail-closed)** — TEMPLATE.md 에 `# 5. Revision History` 가 실재 절 헤딩이므로 "Revision History"가 in-file 절을 지시하는 독해가 성립한다.

**r2 종결** — Advisor 판정 R4로 사용자 결정 2026-07-27을 승인 근거로 삼아 Glossary·TEMPLATE·08-hooks·03 문면을 신규범으로 개정했다(§3.3). "기록"의 물리 locus가 문면에서 git으로 명시되어 **긴장 해소**. 잔여 = 커밋·사용자 표면화(Advisor 소관).

---

## 6. 미해소 사항 (r2)

1. **[축약 실행 전 정리 필요] 도구 등재 목록 stale 1건.** `.claude/tools/history_compact.py`의 `AMBIGUOUS_SECTIONS`가 옛 표제 `### §3.4 Revision History 관례 (L-10 명문화)`를 하드코딩한다. r1에서 그 표제를 개정했으므로 등재가 STALE이다 — 도구 dry-run이 `! STALE 등재 1건 … 목록 갱신 필요`로 자기 표면화한다. **부수 효과는 안전측**이다: 새 표제 `### §3.4 개정 기록 관례 (L-10 재정의 — 기록 locus 이전)`는 탐지 정규식(`이력|Revision History|개정 ?이력|Changelog`)에 매칭되지 않아 대상에서 자동 제외된다. 즉 §3.4는 보호되며 남은 것은 **등재 목록 정리**뿐이다. 도구는 위임 4파일 밖이라 무촉했다.
2. **[해소됨·기록용] 보고서 H1 오탐.** r1 제목 `# Wave 0 — 이력 거버넌스 …`가 탐지 정규식에 걸려 본 보고서 191줄이 대상으로 잡혔다(dry-run 실측). r2에서 제목과 소절 표제를 트리거 토큰 없이 재작성해 해소했다. **일반화된 위험** = *문서 제목*에 `이력`이 들어간 파일은 본문 전체가 축약된다 — 현 리포에서 이 유형은 본 보고서 1건이었다.
   `uaf-verified: dry-run 로그의 heading 행을 전부 추출해 §9류(§9·# 9.·## 9.)를 제외하고 정렬·중복 제거해 8건을 육안 확인했다. 검색 범위 = history_compact.py --anchor DRYRUN0 dry-run 출력 전문(files 72·sections 73).`
3. **A-6 56파일 관행 주석**은 §9 블록 내부이므로 축약과 함께 소멸한다 — 선제 개정 불요. 다만 축약 실행 전까지는 구 규범 문면이 파일에 남는다.
4. **커밋 미수행**(제약대로). Advisor가 커밋 메시지에 개정 취지·범위를 담아야 신규범상 "기록"이 성립한다 — **이번 개정 자체가 신규범의 첫 적용**이므로 커밋 메시지 품질이 곧 기록이다.
5. **`03-project-contract.md` 버전 상승(v1.2→v1.3)은 Baseline 문서의 버전 이동**이다. 인스턴스 계보(PC-INV 9)와 무관하나, Baseline 재승인이 필요한지는 사용자 게이트 사안이다.

---

## 6-A. r3 — CP2 기준 밖 발견 2건 정정

### F1 — 줄바꿈 회귀 검출·원복

R1 치환 스크립트가 텍스트 모드로 재기록해 27파일을 LF→CRLF 로 바꿨다(CP2 실측 +4,199B).

- **검출 로직(하드코딩 목록 0·예외 0)**: 워킹트리 `M` 상태 md 전수에 대해 `HEAD` blob 의 `\r\n` 카운트 == 0 **AND** 워킹트리 카운트 >= 1 인 파일만 대상. Frozen 4종도 동일 판정을 거쳐 통과(대상 아님)했다 — 판정에 예외를 두지 않았다.
- **정정 수단**: 바이트 모드 전용(`read_bytes`/`write_bytes`) — 텍스트 모드 newline 변환이 개입할 여지를 제거했다(동종 사고 재발 금지).
- **수치**: 검사 **41건** · 검출 **27건** · 바이트 **552,841 → 548,642**(델타 **−4,199B**). CP2 가 관측한 +4,199B 와 정확히 상쇄된다.
- **검증**: 정정 후 동일 검출 재실행 → **검출 0건**. F2 편집 5파일도 CRLF 카운트 0 실측.
  `uaf-verified: 동일 스크립트를 detect-only 로 재실행해 0건을 확인하고, F2 5파일은 read_bytes().count(b'\r\n') 로 개별 확인했다. 검색 범위 = git diff --diff-filter=M HEAD 의 .md 41건.`

### F2 — 거버넌스 라인 변형 문면 5건 교체

| 파일:행 | 전 문면(변형) | 후 문면 |
|---|---|---|
| `uahf/framework/adapters/claude/hooks-binding.md:15` | `개정은 Advisor 승인 + §9 이력 append로만 이뤄진다.` | `개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = docs/spec-versioning-policy.md §3).` |
| `…/workflow-binding.md:13` | `개정은 Advisor 승인 + §9 이력 append로만 이뤄진다` (문장 중간) | 동상 — 후속 `근거 =` 절 보존 |
| `…/loop-binding.md:13` | `개정 절차(Advisor 승인 + 본 문서 §9 이력 append)` | `개정 절차(Advisor 승인 + git 커밋 기록 — 규범 = docs/spec-versioning-policy.md §3)` |
| `…/plugins-binding.md:14` | `개정은 Advisor 승인 + §9 이력 append-only로만 이뤄진다.` | hooks 와 동상 |
| `planning/adapters/claude/contract-binding.md:138` | `논리 스키마 개정은 정본 03의 spec 버전 상승 + §9 Revision History append로만 이뤄지고(03 §3.3-E),` | `… + git 커밋 기록으로만 이뤄지고(03 §3.3-E · 기록 locus 정본 = docs/spec-versioning-policy.md §3),` — **03 v1.3 신문면과 정합**. 같은 문장의 인스턴스 계보 append-only 구는 **보존**(경계 ②) |

각 파일 문체(문장 위치·연결 어미·병기 근거)는 보존했다.

### F2 광역 재스윕 — 잔존 3분류

`§9 이력` · `이력 append` · `Revision History append` 3패턴 리포 전체 grep.
`uaf-verified: 위 3패턴을 grep -rn --include=*.md 로 리포 루트에서 실행하고 전 히트를 행 단위로 열람해 분류했다. 검색 범위 = 저장소 전 .md(.git 제외).`

| 분류 | 건수 | 내역 | 처리 |
|---|---|---|---|
| **(i) 살아있는 규범 지시 — 교체 완료** | 5 | F2 대상 5파일 | **완료** |
| **(i) 살아있는 규범 지시 — 미처리(추가 위임 필요)** | 10 | `planning/specs/03-project-contract.md:321`·`04-solution-design.md:342`(검증 항목 11 "관행 규격(상태 라인·**§9 이력 머리 배치·append-only**·…)" — **DoD 가 구 규범을 강제**) · `uahf/framework/adapters/claude/adapter-conformance.md:4`(상태 라인 "승인 기록은 **§9 이력 표가 정본이다**") · `orchestration/ARCHITECTURE.md:4`(상태 라인 "판정 수치는 §9 이력") · `docs/artifact-lifecycle-policy.md:8`(근거 정본 "§9 이력 머리 배치 관례의 선례 … 같은 관례를 따른다") · `workflow/{decompose-rules:20,dispatch-protocol:17,merge-rules:22,work-graph:19}`(근거 정본 "관례 표본 — §9 이력 절 머리 배치") · `orchestration/specs/05-project-orchestration.md:258`(트랙 종단 결정 목록에 **"step-hosting-protocol §9 이력 append"** 라는 **장래 실행 지시**가 잔존 — 신규범상 폐기된 동작) | **무촉** — "다른 파일 수정 금지" 제약. 이들은 §9 블록 **밖**이라 절 축약 후 dangling 이 된다. 특히 앞 3건은 **검증·정본 지시**여서 구 규범을 계속 강제한다 |
| **(ii) 이력 절 내부 문면** | 6 | `ARCHITECTURE.md:28,30` · `spec-versioning-policy.md:23` · `planning/ARCHITECTURE.md:20` · `scaffold-binding.md:24` · `03-project-contract.md:214` 인접 이력 문맥 | **무촉** — 절째 축약 대상 |
| **(iii) 보고서·전후 인용·무관 문맥** | 나머지 전건 | 본 보고서 5행 · `03:250` PC-INV 9(경계 ②·유지) · `05:16,258`(계보 인용·트랙 결정 기록) · `contract-binding.md:185`(이력 표 부재 사실 서술 — 신규범과 이미 정합) · 각 바인딩 "작성 경계 이력(포인터)" 류 · `ARCHITECTURE.md:43` 등 `이력`이 아닌 문맥 | **무촉** |

**미해소 신규 1건** = 위 (i) 미처리 10지점. 그중 `03:321`·`04:342`는 spec 의 **완료 조건(done) 항목**이라 신규범과 정면 충돌하고, `05:258`은 폐기된 동작을 장래 실행 지시로 남긴다 — 후속 위임 권고.

---

## 6-B. r4 — (i) 분류 10지점 처리

### 처리 목록 (10/10)

| # | 파일:행 | 전 문면 요지 | 후 문면 요지 |
|---|---|---|---|
| 1 | `planning/specs/03-project-contract.md:321` | done 11 관행 규격 = `상태 라인·**§9 이력 머리 배치·append-only**·§ 포인터 재정의 0·…` | `상태 라인·**개정 기록 = git 커밋[규범 §3]**·§ 포인터 재정의 0·…` |
| 2 | `planning/specs/04-solution-design.md:342` | done 12 관행 규격 (동일 구) | 동일 치환 |
| 3 | `orchestration/specs/05-project-orchestration.md:258` | 트랙 종단 결정 목록에 `step-hosting-protocol **§9 이력 append**` | `step-hosting-protocol **개정 기록(git 커밋 — 규범 §3)**` |
| 4 | `uahf/framework/adapters/claude/adapter-conformance.md:4` | 상태 라인 — `승인 기록은 **§9 이력 표가 정본**이다` | `승인 기록의 정본은 **git 커밋(커밋 메시지·앵커)**이다(규범 §3)` |
| 5 | `orchestration/ARCHITECTURE.md:4` | 상태 라인 — `단계별 판정 수치는 **§9 이력**` | `단계별 판정 수치는 **git 이력**` |
| 6 | `docs/artifact-lifecycle-policy.md:8` | 근거 정본 — `관례(**§9 이력 머리 배치**·§0 정본 경계)의 선례` | `관례(**머리 상태 라인**·§0 정본 경계)의 선례이자 **개정 기록 locus 정본(§3)**` |
| 7 | `uahf/framework/workflow/decompose-rules.md:20` | 관례 표본 — `**§9 이력 절 머리 배치**` | `**머리 상태 라인(개정 기록 = git 커밋 — 규범 §3)**` |
| 8 | `uahf/framework/workflow/dispatch-protocol.md:17` | 동상 | 동상 |
| 9 | `uahf/framework/workflow/merge-rules.md:22` | 동상 | 동상 |
| 10 | `uahf/framework/workflow/work-graph.md:19` | 동상 | 동상 |

### 버전 상승 목록

| 파일 | 전 | 후 | 사유 |
|---|---|---|---|
| `planning/specs/03-project-contract.md` | v1.2 | **v1.3** | 이번 웨이브에서 이미 상승 — 지침 2에 따라 **추가 상승 없이** 같은 v1.3 개정에 포함 |
| `planning/specs/04-solution-design.md` | v1.3 Baseline → DC-1 Draft | **v1.4 개정** 표기 추가 | done 12 계약 문면 변경 = 이번 웨이브 첫 변경. 진행 중 트랙(DC-1) 라벨은 보존하고 개정 표기만 병기 |
| `orchestration/specs/05-project-orchestration.md` | v1.6 Baseline | **v1.7 Baseline** | :258 계약 문면 변경 = 이번 웨이브 첫 변경. 직전 기준선 v1.6 표기 유지 |
| `uahf/framework/adapters/claude/adapter-conformance.md` | v1.2 Baseline (r4) | **무변** | 상태 라인의 기록 locus 지시만 교체 — 계약 조항 무촉 |

변경 hunk 는 개정 기록 문면에 국한했다 — 다른 계약 조항 무촉.

### CRLF 실측

전 편집을 Edit 경로(LF 보존)로 수행한 뒤 F1 검출기 재실행: **검사 44건 · 검출 0건 · 델타 +0B**.
`uaf-verified: F1 검출 스크립트(HEAD blob 대조·바이트 모드)를 r4 편집 후 재실행해 0건을 확인했다. 검색 범위 = git diff --diff-filter=M HEAD 의 .md 44건.`

### 재스윕 잔존표 — **(i) 잔존 0 미달성**

3패턴(`§9 이력`·`이력 append`·`Revision History append`) 리포 전체 재실행.
`uaf-verified: 3패턴을 grep -rn --include=*.md 로 리포 루트에서 실행하고 전 히트를 행 단위로 열람해 분류했다. 검색 범위 = 저장소 전 .md(.git 제외).`

| 분류 | 건수 | 상태 |
|---|---|---|
| (i) r4 위임 10지점 | 10 | **교체 완료 — 잔존 0** |
| **(i) 신규 발견 — 미처리** | **15지점 / 14파일** | **잔존 있음(아래)** |
| (ii) 이력 절 내부 문면 | 6 | 무촉 — 절째 축약 대상 |
| (iii) 보고서 인용·과거 기록·무관 문맥 | 나머지 | 무촉 |

**(i) 신규 발견 상세 — 위임 목록에 없던 제3 변형군.** r4 done 조건 "(i) 잔존 0"은 이들 때문에 **미달성**이다. "다른 파일 수정 금지" 제약이 명시적이므로 무촉했다.

1. **변형 C — 거버넌스 라인 "개정은 Advisor 승인 + §9 이력 기록으로만 이뤄진다."("절" 없음) · 11파일 각 1건** `uaf-allow-legacy: 이 구는 r4 시점의 발견 기록이므로 인용 문면을 보존한다.`: `uahf/framework/adapters/claude/{adapter-conformance:19, agent-binding:14, harness-binding:12, memory-binding:13, runtime-binding:12, scaffold-binding:14, skills-binding:14, step-hosting-binding:14, verifier-binding:15}` · `uahf/framework/adapters/generic/{generic-binding:14, generic-adapter-conformance:12}`. R1 정규식("§9 이력 **절** 기록으로만")과 F2 지목 5변형 **양쪽 모두**에서 빠진 군이다.
2. **관례 표본 `§9 이력 절 머리 배치` 2건**: `uahf/framework/plugins/plugin-lifecycle.md:18` · `plugin-manifest.md:16` — r4 #7~#10 과 동일 유형인데 위임 목록에서 누락.
3. **산출물 규격 지시 1건**: `uahf/framework/adapters/claude/verifier-binding.md:108` — 검증 리포트 문서에 `**§9 이력 절을 둔다**(docs 거버넌스 관례 동형)`. **생성 산출물에 구 규범을 계속 심는다**.
4. **에스컬레이션 경로 지시 1건**: `uahf/framework/verifier/rework-instruction.md:111` — `(§9 이력·open_questions 경로)`.

권고 = 변형 C 11건은 단일 정규식(`§9 이력 기록으로만` → `git 커밋 기록으로만(규범 = docs/spec-versioning-policy.md §3)`)으로 일괄 처리 가능하고, 나머지 4건은 개별 편집이다.

---

## 6-C. r5 — 제3 변형군 15지점 + 재량 처리

### 위임 15지점 (15/15)

| 군 | 지점 | 전 문면 | 후 문면 |
|---|---|---|---|
| 변형 C(11파일 각 1건) | `adapters/claude/{adapter-conformance:19, agent-binding:14, harness-binding:12, memory-binding:13, runtime-binding:12, scaffold-binding:14, skills-binding:14, step-hosting-binding:14, verifier-binding:15}` · `adapters/generic/{generic-binding:14, generic-adapter-conformance:12}` | `개정은 Advisor 승인 + §9 이력 기록으로만 이뤄진다.` | `개정은 Advisor 승인 + git 커밋 기록으로만 이뤄진다(규범 = docs/spec-versioning-policy.md §3).` |
| 산출물 규격 | `adapters/claude/verifier-binding.md:108` | `문서 머리에는 작성일·수행 주체·근거 정본·**§9 이력 절을 둔다**(docs 거버넌스 관례 동형).` | `… 근거 정본·**상태 라인**을 둔다(…). **산출물 파일 안에 이력 절을 두지 않는다** — 리포트의 개정 기록은 git 커밋이다(규범 §3).` |
| 관례 표본 2건 | `framework/plugins/{plugin-lifecycle:18, plugin-manifest:16}` | `§9 이력 절 머리 배치` | `머리 상태 라인(개정 기록 = git 커밋 — 규범 §3)` |
| 에스컬레이션 경로 | `framework/verifier/rework-instruction.md:111` | `(§9 이력·open_questions 경로)` | `(개정 기록[git 커밋]·open_questions 경로)` |

변형 C 는 바이트 모드 일괄 스크립트로 처리했고, 치환 전후 `\r\n` 카운트 동일성을 **assert 로 강제**했다(F1 규율).

### 재량 처리 목록 (경계 내 — 위임 추가 없이 즉시 처리)

경계 = (a) 취지 동일(기록 locus = git 커밋·규범 §3) · (b) 변경이 그 문장에 국한 · (c) spec 계약 문면(§ 번호 있는 `specs/` 규범 조항)이 **아님**. 세 조건을 모두 만족한 건만 처리했다.

| # | 지점 | 전 → 후 요지 | 경계 충족 근거 |
|---|---|---|---|
| D1 | `uahf/framework/core/structure.md:157` | `계약 변경은 01의 버전 상승과 **Revision History 기록**이 필수다` → `… **개정 기록(git 커밋 — 규범 §3)**이 필수다` | framework 인스턴스 문서(specs/ 아님) · 문장 국한 |
| D2~D9 | 「작성 경계 이력(포인터)」군 8파일 — `agent-binding:152`·`harness-binding:127`·`memory-binding:243`·`runtime-binding`·`scaffold-binding:253`·`skills-binding:246`·`verifier-binding:177`·`generic-adapter-conformance:146`·`generic-binding:145` | `감사 흔적은 **§9 이력 행/초판 행**에 보존되어 있다` → `**git 이력(초판·개정 커밋)**에 보존되어 있다` (+ 각 `uaf-allow-legacy` 마커 내 `§9 이력 표에 보존` → `git 이력에 보존`) | Adapter Binding 문서 · 문장 국한 · 축약 후 dangling 방지 |
| D10 | `adapters/claude/hooks-binding.md:280` | `감사 서술 … 은 **§9 이력과** git 앵커 90ca19c에 남는다` → `… 은 **git 이력·앵커 90ca19c**에 남는다` | 동상 |
| D11 | `uahf/ROADMAP.md:65`·`:93` | `근거 = git 앵커 90ca19c**(및 # 8 이력 표)**` / `**및 # 8 이력 표가** 근거다` → 자기 이력 표 포인터 제거, git 앵커만 | 운용 문서 · 문장 국한 |

재량 처리 = **12파일 · 22치환**. 전건 위 표에 기록했다(책임 있는 자율 — 기본값 적용 + 이탈·재량 기록).

### 최종 잔존표

분류 수단 = 결정적 스크립트. 각 히트가 **이력 절 스팬 안/밖**인지를 `history_compact.py` 와 **동일한 헤딩 정규식 기준**으로 판정한다(재정의 0). 패턴 8종 = `§9 이력`·`이력 append`·`Revision History append`·`이력 절`·`이력 기록`·`이력 표`·`append-only로`·`Revision History 기록`.
`uaf-verified: 위 8패턴을 저장소 전 .md 에 적용하고, 각 히트의 이력 절 스팬 소속을 스크립트로 판정한 뒤 스팬 밖 41건을 개별 열람해 분류했다. 검색 범위 = 저장소 전 .md(.git·본 보고서 제외).`

| 분류 | 건수 | 상태 |
|---|---|---|
| **(i) 살아있는 구 규범** | **1** | **애매 1건만 잔존 — 아래** |
| (ii) 이력 절 스팬 **내부** | 스팬 밖 41건을 제외한 전건 | 무촉 — 절째 축약 대상 |
| (ii-runtime) 런타임 원장·계보 append-only | 15 (`loop-*`·`03-loop`·`00-glossary` 루프 상태 기록 · `03` PC-INV 9·계보 · `memory-binding` store · `05` 계보 인용) | 무촉 — §3.4 경계 ①② |
| (iii) 신규범 본문·인용·과거 기록 | 25 (`spec-versioning-policy` 9 · `TEMPLATE`·`README`·`rework-instruction`·`artifact-lifecycle-policy`·`verifier-binding` 신문면 · `contract-binding:185`·`getting-started:4`·`step-hosting-binding:159`·`scaffold-binding:259` 과거 기록) | 무촉 |

**(i) 잔존 1건 — 무촉 사유 = 취지 판단 애매(지침 2 단서 적용).**
`uahf/framework/adapters/claude/runtime-binding.md:81` — Module Manifest `version` 필드 표의 셀 `형태 B(전용 필드), **현재 이력 절로 대용**`. 이 구는 **기록 locus 규범이 아니라 "버전 문자열을 어디서 읽는가"의 필드 출처 매핑**이다. 이력 절 축약 후 출처가 사라지므로 정정이 필요하나, 대체 출처를 상태 라인으로 볼지 front-matter 로 볼지가 **계약 판단**(01 §3.2-A Module Manifest)이라 취지 동일 조건 (a)를 만족하지 않는다. **Advisor 판정 요청.**

### CRLF 실측

r5 전 편집(스크립트 2회 + Edit 4회) 후 F1 검출기 재실행: **검사 55건 · 검출 0건 · 델타 +0B**.
`uaf-verified: F1 검출기(HEAD blob 대조·바이트 모드)를 r5 종료 후 재실행해 0건을 확인했다. 검색 범위 = git diff --diff-filter=M HEAD 의 .md 55건.`

---

## 7. 자체 점검 (CP1)

| done / 재작업 항목 | 충족 | 검사 범위(정직 표기) |
|---|---|---|
| ① 루트 ARCH 원칙 12 + 카운트 정합 | 충족 | 파일 직독 + 리포 전체 카운트 패턴 grep 분류 + 개정 후 재스윕 0건 |
| ② 정책 §3 대개정(요건·§3.4·사유·경계·Glossary 판정) | 충족 | 전문 직독 후 15지점 편집. 경계는 정정 지시 반영 |
| ③ structure.md :13·:42 | 충족 | 두 지점 직독 후 치환 |
| ④ lessons.md L-10 | **종결(R3 무촉 확정)** | r1 미충족 → Advisor 판정으로 무촉 확정. :14·:35만 정합 |
| ⑤ 스윕 3분류 표 | 충족(범위 한정) | §4 마커의 한계 표기대로 |
| R1 27파일 | 충족 | 스크립트 치환 + 재grep 잔존 0 실측 |
| R2 rework-instruction | 충족 | §4 전문 직독 후 취지별 분기 처리 |
| R4 Frozen 4파일 | 충족 | 각 파일 상태 라인·대상 행 직독 후 편집. 버전 상승 4건·새 이력 행 0건 |
| R5 배포 템플릿 | 충족 | 파일 직독 후 1지점 교체 |
| R6 스텁 형태 대조 | 충족 | 도구 상수 직독 + dry-run 실행. 정책 §3.4를 **형태 서술**로 정정(문자열 사본 0) |
| F1 줄바꿈 원복 | 충족 | 프로그램 판정(HEAD blob 대조·예외 0) · 검사 41/검출 27/−4,199B · 재검출 0건 · 바이트 모드 기록 |
| F2 변형 5건 교체 + 광역 3분류 | 충족(범위 한정) | 5건 교체 완료 · 3패턴 재스윕 전 히트 분류. **한계** = (i) 미처리 9지점은 "다른 파일 수정 금지" 제약으로 무촉했다(§6-A) |
| r4 10지점 교체 + 버전 상승 | 충족 | 10/10 편집·버전 상승 3건(03은 기존 v1.3에 포함)·hunk 는 기록 문면 국한 |
| r4 CRLF 규율 | 충족 | 편집 후 F1 검출기 재실행 0건(44건 검사) |
| r4 "(i) 잔존 0" 실측 | **미충족** | 위임 10지점은 잔존 0이나, **제3 변형군 15지점/14파일**이 신규 발견됐다(§6-B). 명시 제약("다른 파일 수정 금지")으로 무촉 — 추가 위임 필요 |
| r5 15지점 처리 | 충족 | 변형 C 11 일괄 + 개별 4 · 15/15 |
| r5 재량 처리(경계 내) | 충족 | 12파일 22치환 · 처리 지점을 §6-C 표에 열거 · 경계 3조건 개별 판정 (`uaf-verified: 스크립트 출력 로그의 파일·패턴 목록을 §6-C 표와 1:1 대조했다. 검색 범위 = r5 재량 스크립트 치환 로그 12행.`) |
| r5 "(i) 잔존 0" | **충족(단서 1건)** | (i) 잔존 = 1, 지침 2 단서("취지 애매 시 무촉 + 잔존표")에 따른 의도적 잔존 — `runtime-binding.md:81` Advisor 판정 요청 |
| r5 CRLF 0 | 충족 | 검사 55건 · 검출 0건 · 델타 +0B |
| 이력 절 물리 제거 0 · commit 0 | 충족 | 도구는 dry-run만 실행(`--apply` 미사용) · `git log -1` 불변 확인 |

**자체 점검은 최종 승인이 아니다** — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다.
