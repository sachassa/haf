# planning — Project Contract / 설계 Layer

상태: v1.3 경량 갱신 (이중 책임 반영 — 완전 저술은 후속 트랙)
상위: Universal Agentic Framework (root README/ARCHITECTURE 참조)

## 역할
planning은 **이중 책임** Layer다 — ① Project Contract(데이터 계약 스키마)를 소유하고, ② 그 성숙 활동(Solution Design)을 소유한다. Discovery가 컴파일한 Ready Contract 인스턴스 vN은 프로젝트 복잡도에 따라 Solution Design으로 superseding 인스턴스 v(N+1)로 성숙될 수 있다(단순하면 스킵). UAF 파이프라인과 UAHF의 접점은 이 Contract 하나다. 구현 Planning(작업 분해·디스패치)은 UAHF 소관으로 planning/이 아니다(C2).

## 정본 포인터
정본: `planning/specs/03-project-contract.md`(계약 스키마·v1.2) · `planning/specs/04-solution-design.md`(성숙 활동·v1.3). 비정본 부록 = `planning/docs/appendix/`(방법론 대응·Expert Role 카탈로그·Projection 카탈로그).

## 이 문서의 지위
스텁이다. 내용은 후속 트랙에서 완전 저술된다.
