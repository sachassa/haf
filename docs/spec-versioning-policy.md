# docs/spec-versioning-policy — Spec Versioning · 하위호환 정책

작성일: 2026-07-06
상태: v0.9 Baseline (r2 · CP2 Pass — 첫 판정 Pass · CP3 승인 · 사용자 승인 2026-07-06)
상위 규약: AGENT.md
근거 정본:

- runtime/uahf/specs/00-glossary.md §3.2-G — **Spec Status(Draft / Review / Frozen) 값의 정본.** 본 문서는 그 상태 값을 재정의하지 않고 운용 절차만 소유한다.
- runtime/uahf/specs/TEMPLATE.md §3 — 품질 기준(Definition of Done, 8항). §4 — Status 전이(Draft → Review → Frozen). §5 — Revision History 관례. 본 문서는 이 계약을 § 포인터로만 인용한다.
- ROADMAP.md v0.9 — 완료 조건 ④("Spec versioning과 하위호환 규칙이 문서화된다")·산출물 목록의 "Spec versioning 정책 문서". 본 문서가 그 산출물이다.
- runtime/uahf/framework/core/structure.md §9 — 확립된 개정 이력 관행의 실례(격리 개정 · 상태 라인 승격 · append-only). Adapter Binding 문서(runtime/uahf/framework/adapters/`<adapter>`/ 이하)의 개정 이력도 동형 관행이다.
- Active Lesson L-06(개정 시 같은 상태 서술의 전 지점 전수 갱신) · L-10(§9 이력 행은 시점 기록 — 문면 불변 · append-only). 본 문서가 이 관행을 정책 문장으로 명문화한다.

거버넌스: 이 문서는 `docs/` 소속 **운용 정책 문서**다. 계약의 정본이 아니라, 정본(Glossary §3.2-G · TEMPLATE)이 정한 상태 값·완료 기준·개정 요건을 **어떻게 운용하는가**의 절차를 소유한다. 이 문서 자체의 개정은 Advisor 승인 + 본 문서 §9 이력 절 기록으로만 이뤄진다(docs 운용 문서 거버넌스 관행 — session-handoff-v0.2 §1.3). 이 문서는 **환경 무관 거버넌스 문서**이므로 본문에 특정 AI 이름·모델명·제품 기능명을 두지 않는다(§0).

---

## §9. 이력 (Revision History)

| 일자 | 버전 | 변경 | 주체 |
|---|---|---|---|
| 2026-07-06 | v0.9 Draft | 최초 작성. Spec versioning · 하위호환 정책 문서. Frozen spec 개정 절차(계약 변경 = 버전 상승 + Revision History append 필수 / 비계약 정합·격리 개정 = 이력 append + 상태 라인 갱신, 이력 행 시점 기록·문면 불변·append-only L-10 명문화, 사용자 승인 상태 승격 절차)(§3), 하위호환 규칙 4항 열거(추가 = 호환 / 삭제·의미 변경·필수화 = 비호환 / dependents 영향 대조 선행 / 인스턴스 정합 이력 기록)(§4), Glossary §3.2-G Spec Status와의 관계(상태 값 정본 = Glossary, 운용 절차 = 본 문서)(§2), 첫 적용 사례(v0.9 Glossary 개정 DP-U2 — 절차만 확정, 내용 추측 0)(§5). 정본(Glossary §3.2-G·TEMPLATE) 재정의 0, Glossary 밖 새 용어 신설 0, 본문 특정 AI 이름·모델명·제품 기능명 0(전수 자체 점검). | Worker (Advisor 위임, Task T2) |
| 2026-07-06 | v0.9 Draft (r2) | §9 하단 주석 § 포인터 오기 교정(§3.3→§3.4) — 동종 § 포인터 전수 자가 대조 불일치 0. (L-10 명문화의 실제 위치는 §3.4 Revision History 관례이며 §3.3은 상태 승격 절차다. 교정 외 본문 무변경 — 계약·문면 취지 불변. 기존 r1 행 문면 불변 — L-10.) | Worker (Advisor 재작업 지시, Task T2 r2) |
| 2026-07-06 | v0.9 Baseline | v0.9 마일스톤 사용자 승인 — 기준선 확정 (CP2 Pass — 첫 판정 Pass·재작업 0회, 충족 20/위반 0/판정 불가 0; CP3 Advisor 승인). | Advisor |

(이력 절은 문서 머리에 둔다 — 거버넌스 추적 대상 문서 관행. 이후 개정은 이 표에 append-only로 기록한다. 이력 행은 시점 기록이므로 문면을 사후 변경하지 않는다 — L-10 §3.4.)

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 Glossary §3.2-G(Spec Status)와 TEMPLATE(§3 DoD · §4 Status 전이 · §5 Revision History)다.** 이 문서는 그 계약을 **재정의·확장하지 않는다.** 상태 값·완료 기준·개정 요건은 정본 § 포인터로만 인용하고, 본 문서는 그 위의 **운용 절차(정책)**만 소유한다.
- 이 문서는 **정책 문서**이지 spec이 아니다. 따라서 TEMPLATE §0~§9 spec 본문 구조를 그대로 따르지 않고, docs 운용 문서 관례(머리 · §9 이력 절 머리 배치 · §0 정본 경계 · 요약)를 따른다.
- 용어는 runtime/uahf/specs/00-glossary.md 정본만 사용한다. 새 용어를 신설하지 않는다. "Baseline"은 framework 인스턴스 문서가 쓰는 상태 라인 라벨(관행 — structure.md §9)의 **인용**이며, Glossary 표제어의 신설이 아니다(§3.3).
- **AI 비의존.** 이 문서는 환경 무관 거버넌스 정책이다. 본문에 특정 AI 이름·모델명·제품 기능명을 두지 않는다. 환경 의존 실현(구체 어댑터명·물리 경로·직렬화 형식·실행 표면)은 Adapter Binding 문서 소관이며, 필요한 자리에는 일반형 표기 `<adapter>`와 소관 포인터만 둔다. 이 정책이 규율하는 대상은 계약 문서(spec·인스턴스 문서)의 **버전·상태·개정**이지 특정 실행 환경이 아니다.

---

## §1. 목적

이 문서는 UAHF spec의 **버전 상승·상태 승격·개정·하위호환**을 어떻게 운용하는가를 규율한다.

책임은 세 가지다.

- Frozen spec을 어떤 절차로 개정하는가를 명문화한다(§3) — 계약 변경과 비계약 정합 개정을 구분하고, 각 경로의 필수 요건(버전 상승 / 이력 append / 상태 라인 갱신 / 사용자 승인)을 확정한다.
- 무엇이 하위호환이고 무엇이 비호환인가를 **검증 가능한 문장**으로 열거한다(§4) — 개정 착수 전 dependents 영향 대조를 강제한다.
- Glossary §3.2-G Spec Status와 본 정책의 소유 경계를 명시한다(§2) — 상태 **값**의 정본은 Glossary, 그 값의 **운용 절차**는 본 문서.

이 문서는 정본(Glossary §3.2-G · TEMPLATE)의 어떤 계약 요소도 재정의·확장하지 않는다(§0).

---

## §2. Spec Status와 이 정책의 관계 (done 3)

### §2.1 소유 경계

- **상태 값의 정본 = Glossary §3.2-G.** Spec Status의 값(Draft / Review / Frozen)과 각 값의 의미는 Glossary §3.2-G가 소유한다. TEMPLATE §4가 그 전이 순서(Draft → Review → Frozen)를 소유한다. 본 문서는 이 값·전이를 **재정의하지 않는다.**
- **운용 절차의 소유 = 본 문서.** "Frozen이 된 뒤 계약을 바꾸려면 어떤 절차를 거치는가", "개정 유형을 어떻게 구분하는가", "무엇이 하위호환인가", "어떻게 상태를 승격하는가"의 절차는 본 문서(§3·§4)가 소유한다.

Glossary §3.2-G Spec Status(정본 인용):

- **Draft** — Worker 작성 중.
- **Review** — 검증 및 Advisor 검토 중.
- **Frozen** — v0.1 기준선 확정. 이후 변경은 spec 버전 상승과 Revision History 기록이 필수다.

본 정책의 §3(개정 절차)은 이 중 **Frozen** 값의 "이후 변경은 버전 상승과 Revision History 기록이 필수"라는 정본 요건을 운용 절차로 전개한 것이다. §4(하위호환)는 그 "변경"이 dependents에 미치는 영향을 판정하는 규칙이다.

### §2.2 규율 대상 범위

이 정책이 규율하는 Frozen 대상은 현재 **numbered spec 14종**(runtime/uahf/specs/00-glossary.md ~ runtime/uahf/specs/13-harness.md)과 **TEMPLATE 1종**(runtime/uahf/specs/TEMPLATE.md)을 합한 **15종**이다(DP-U3(c) 확정 — 종전 "16종" 표기는 오기로 확정됨). runtime/uahf/specs/00~13 전체와 TEMPLATE은 v0.1 기준선으로 함께 Frozen되었다(TEMPLATE §5, Glossary 머리 상태 라인).

runtime/uahf/framework/ 이하 **인스턴스 문서**는 spec이 아니라 spec 계약의 인스턴스이며, spec의 Frozen과 대칭인 확정 상태로 "Baseline" 라벨을 쓴다(관행 — §3.3). 인스턴스 문서의 개정도 본 정책 §3·§4를 따른다.

---

## §3. Frozen spec 개정 절차 (done 1)

### §3.1 개정의 대전제 (Glossary §3.2-G 인용)

**Frozen spec의 계약 변경은 spec 버전 상승 + Revision History append가 필수다**(Glossary §3.2-G Frozen 정의: "이후 변경은 spec 버전 상승과 Revision History 기록이 필수다"). Frozen 상태에서 계약을 임의로 덮어쓰는 개정은 금지된다 — 반드시 버전이 오르고, 그 개정이 이력에 남는다.

### §3.2 개정 유형 구분

개정은 두 유형으로 구분하고, 각 유형이 요구하는 절차가 다르다.

| 유형 | 정의 | 필수 절차 |
|---|---|---|
| **(A) 계약 변경** | 계약 요소(연산 · 데이터 포맷 · 필드 · 불변 규칙 · 완료 조건 · 의미)를 추가·삭제·변경·필수화하는 개정. | **버전 상승 사안.** spec 버전을 올리고, §4 하위호환 판정을 선행하며, Revision History에 append한다. 비호환 변경(§4-b)이면 전 dependents 영향 판정 + 사용자 승인이 필수다. |
| **(B) 비계약 정합·격리 개정** | 계약 요소를 **바꾸지 않는** 개정 — 실측 상태 반영, 오기 교정, 같은 상태 서술의 전 지점 정합화, 트리·목록 갱신, 상태 라인 승격 등. | **이력 append + 상태 라인 갱신.** 계약은 무변경이므로 dependents 참조 변경이 0이다. Revision History에 개정 취지를 append하고, 상태 라인(버전·개정 표기)을 갱신한다. |

유형 (B)는 계약을 재정의하지 않으므로 dependents의 참조·규격 변경이 0이다(§4-a 하위호환의 특수형 — 계약 무변경). structure.md §9의 v0.4~v0.8 "격리 개정(§8 트리 갱신)" 행들이 유형 (B)의 확립된 실례다.

**개정 유형 판정이 불확실하면 추측하지 않는다.** 계약 요소를 건드리는지 여부가 불명확한 개정은 유형 (A)로 보수적으로 취급하거나 Advisor에게 에스컬레이션한다(상위 규약 추측 금지).

### §3.3 상태 승격 절차 (Draft → 확정 상태)

상태 승격은 **사용자 승인**을 확정 게이트로 한다(AGENT.md Core Principles: Human Approval).

- **spec 문서(runtime/uahf/specs/ 이하).** Draft(작성) → Review(검증 및 Advisor 검토) → **사용자 승인으로 Frozen 확정**(TEMPLATE §4, Glossary §3.2-G). Review 단계는 Verifier 독립 판정과 Advisor 검토를 포함하며(TEMPLATE §3 DoD 8: "Verifier 검증과 Advisor 승인을 통과했다"), 사용자 승인이 Frozen 확정의 최종 게이트다.
- **framework 인스턴스 문서(runtime/uahf/framework/ 이하).** Draft → **사용자 승인으로 Baseline 확정.** "Baseline"은 인스턴스 문서가 쓰는 상태 라인 라벨(관행 — structure.md §9 "v0.8 Baseline" 등)이며, spec의 Frozen에 대응하는 milestone 확정 상태다. Baseline을 Glossary 표제어로 신설하지 않는다 — 관행 라벨의 인용이다(§0).

두 경로 공통: Draft에서 확정 상태(Frozen / Baseline)로의 승격은 사용자 승인 없이 성립하지 않는다. 확정 후의 재개정은 §3.1 대전제(버전 상승 + 이력 append)를 다시 따른다.

### §3.4 Revision History 관례 (L-10 명문화)

- **이력 행은 시점 기록이다 — 문면 불변, append-only(L-10).** §9 이력 절의 각 행은 그 개정 시점의 사실 기록이다. 이미 확정된(이전 개정 회차의) 이력 행의 문면은 사후 변경하지 않는다. 개정·정정은 기존 행을 덮어쓰지 않고 **새 행을 append**한다.
- **예외(선례).** 같은 개정 회차에 자신이 append한 행을 그 회차 안에서 교정하는 것은 위반이 아니다(v0.7 r2/r3 판정 선례). 시점 불변의 대상은 이미 확정된 과거 행이다.
- **전 지점 전수 갱신(L-06).** 개정 시, 같은 상태를 서술하는 **전 지점**(상태 머리말 · 계수 · 목록 항 수 · 요약 · 본문 언급)을 전수 갱신해 정합을 유지한다. 한 지점만 갱신하고 다른 지점을 방치하면 같은 상태 서술이 갈리며, 이는 재발 판정 대상이다(L-06 — 예: 같은 유지 목록을 한 절은 "5항"·다른 절은 "6항"으로 계수한 결함).

---

## §4. 하위호환 규칙 (done 2)

무엇이 하위호환이고 무엇이 비호환인가를 검증 가능한 문장으로 열거한다. 개정 유형 (A)(§3.2)의 계약 변경은 착수 전 이 규칙으로 호환 여부를 판정한다.

- **(a) 추가는 하위호환이다.** 표제어 · 계약 요소 · 필드의 **추가**는 하위호환이다 — 기존 소비자(dependents)의 참조 변경이 0이기 때문이다. 추가된 요소를 참조하지 않는 기존 dependents는 개정 전과 동일하게 동작한다. (검증: 개정 전 dependents의 참조 목록이 개정 후에도 전부 유효한가 → 유효하면 하위호환.)
- **(b) 삭제·의미 변경·필수화는 비호환이다.** 기존 계약 요소의 **삭제**, 기존 요소의 **의미 변경**, 선택 요소의 **필수화**는 비호환이다 — 기존 dependents의 참조가 깨지거나 재해석을 요구하기 때문이다. 비호환 변경은 **전 dependents 영향 판정 + 사용자 승인**이 필수다(§3.1 대전제의 강한 형태). (검증: 개정으로 인해 참조가 무효화·재해석되는 dependent가 1건이라도 있는가 → 있으면 비호환.)
- **(c) dependents 영향 대조가 선행한다.** 모든 개정은 착수 **전에** 해당 spec의 dependents를 대조한다. dependents 목록의 정본은 각 spec의 §2 Position("이 spec에 의존하는 spec 목록")이다. 개정자는 이 목록의 각 dependent가 개정으로 영향받는지 항목별로 대조한 뒤 착수한다 — 추측으로 우회하지 않는다.
- **(d) 인스턴스 정합을 이력에 기록한다.** 인스턴스 문서(runtime/uahf/framework/ 이하)는 자신이 인스턴스화하는 정본 spec의 버전과의 **정합**을 개정 이력(§9)에 기록한다. 정본 spec이 버전 상승하면, 그 인스턴스 문서는 정합 상태를 재확인하고 (필요 시 유형 (B) 정합 개정으로) 이력에 반영한다. (검증: 인스턴스 문서 §9 이력에 정본 spec 계약 재정의 0 · Glossary 밖 용어 신설 0 · 정합 근거가 기록되어 있는가.)

호환 판정 요약: **추가 = 호환**(dependents 참조 변경 0), **삭제·의미 변경·필수화 = 비호환**(dependents 영향 판정 + 사용자 승인 필수). 판정이 불확실하면 비호환으로 보수 처리하고 Advisor에게 에스컬레이션한다.

---

## §5. 첫 적용 사례 (done 4)

**이 정책의 첫 실적용은 v0.9 Glossary 개정(사용자 결정 DP-U2, 2026-07-06)이다.**

- 이 개정은 Frozen spec(runtime/uahf/specs/00-glossary.md)에 대한 개정이므로 §3.1 대전제(버전 상승 + Revision History append)와 §3.2 개정 유형 판정, §4 하위호환 규칙을 적용받는 첫 사례가 된다.
- **본 문서는 절차만 확정한다.** 해당 Glossary 개정의 **구체 내용**(무엇을 추가·변경하는가, 어느 유형인가, 호환 판정 결과)은 그 개정을 수행하는 **후속 Task**가 확정하며, 본 정책 문서는 그 내용을 추측·기술하지 않는다(추측 금지 — 상위 규약). 본 문서는 "그 개정이 이 정책의 첫 적용 대상이다"라는 절차적 사실만 명시한다.

---

## §6. 요약

- **정본 경계.** Spec Status 값(Draft/Review/Frozen)의 정본은 Glossary §3.2-G, 전이·이력·DoD의 정본은 TEMPLATE(§3·§4·§5)다. 본 문서는 그 위의 **운용 절차**만 소유하며 계약을 재정의하지 않는다(§0·§2).
- **개정 절차(§3).** Frozen spec의 계약 변경은 버전 상승 + Revision History append 필수(Glossary §3.2-G). 개정 유형은 (A) 계약 변경(버전 상승 사안) / (B) 비계약 정합·격리 개정(이력 append + 상태 라인 갱신)으로 구분. 이력 행은 시점 기록 — 문면 불변·append-only(L-10). 개정 시 같은 상태 서술 전 지점 전수 갱신(L-06). 상태 승격은 사용자 승인이 확정 게이트(Draft → Frozen / Baseline).
- **하위호환(§4).** 추가 = 호환(dependents 참조 변경 0). 삭제·의미 변경·필수화 = 비호환(전 dependents 영향 판정 + 사용자 승인 필수). dependents(각 spec §2 목록) 영향 대조가 선행. 인스턴스 문서는 정본 spec 버전 정합을 이력에 기록.
- **첫 적용(§5).** v0.9 Glossary 개정(DP-U2, 2026-07-06)이 이 정책의 첫 실적용 — 본 문서는 절차만 확정하고 그 개정 내용은 후속 Task 소관(추측 0).
- **규율 대상.** Frozen 대상 = numbered spec 14종 + TEMPLATE 1종 = **15종**(§2.2). runtime/uahf/framework/ 인스턴스 문서의 Baseline 개정도 본 정책을 따른다.
- **AI 비의존.** 본문 전체에 특정 AI 이름·모델명·제품 기능명이 0건이다 — 환경 의존 실현은 Adapter Binding 문서 소관(§0).
