# planning — Project Contract / 설계 Layer

역할: **이중 책임** Layer — ① Project Contract(데이터 계약 스키마·UAF↔UAHF 유일 접점)를 소유하고, ② 그 성숙 활동(Solution Design — Ready 인스턴스 vN → superseding v(N+1), 단순하면 스킵)을 소유한다. 구현 Planning(작업 분해·디스패치)은 UAHF 소관이며 planning/이 아니다(C2 — `planning/ARCHITECTURE.md` §0).
정본 포인터: `planning/specs/03-project-contract.md`(계약 스키마) · `planning/specs/04-solution-design.md`(성숙 활동) · 개관 = `planning/ARCHITECTURE.md` · 비정본 부록 = `planning/docs/appendix/`(열거 = 개관 §2).
상태: 스텁 — 완전 저술은 후속 트랙.
