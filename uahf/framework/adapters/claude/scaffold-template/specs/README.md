# specs/ — Spec 기준선 배치 자리

이 디렉터리는 spec 문서가 놓이는 자리다 (12 §3.2-A specs 디렉터리 행). 설치 시 UAHF spec 기준선이 이 경계에 배치된다.

## 설치 시 배치 안내

설치 시 spec 기준선(현재 v0.1 기준선, Frozen)을 이 디렉터리에 배치한다. 기준선 구성 (15건 — numbered 00~13 + TEMPLATE):

- `00-glossary.md` — 용어 정본.
- `01-runtime.md` ~ `13-harness.md` — 13개 Core Component 규격.
- `TEMPLATE.md` — spec 공통 템플릿과 DoD.

기준선은 Frozen 상태이며, 변경은 spec 버전 상승과 Revision History 기록이 필수다 (Glossary §3.2-G Spec Status).

## 배치 우선순위

Runtime Bootstrap 필수 계약과 최소 구성 집합(specs/13-harness.md §3.2-A)이 참조하는 기반 spec을 우선 배치한다:

- `00-glossary.md`(용어 기준), `01-runtime.md`(호스팅 계약), `02-agent.md`(역할 계약), `13-harness.md`(최소 구성).

이 자리는 최소 구성 집합이 성립하기 위한 계약 문서의 물리 위치다. 설치 후 VerifyInstall이 이 배치를 CK-1·CK-2로 대조한다 (12 §3.2-C).
