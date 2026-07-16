# Assessing 판정 — pc-uahf-control-plane-001 v1

## 1. 판정: needed

Project Contract v1(pc-uahf-control-plane-001, greenfield-r003 종단 Ready)은 Solution Design 성숙(superseding v2)이 **필요**하다고 판정한다.

## 2. 근거

Contract v1의 실측 필드를 근거로 삼는다.

- **`architectureDirection.decisions`(front-matter 3항)**는 원칙 수준에 머문다 — "계층 분리 — 파서/데이터 계층(UAHF 물리 형식 격리) ↔ 도메인 모델 ↔ UI 컴포넌트"라는 결정은 계층의 *존재*만 선언할 뿐, 각 계층의 내부 설계(도메인 모델 스키마, 이벤트/게이트 분류 판별 로직, revision·artifact 계보 추적 알고리즘, UI 컴포넌트 분해)는 미기재다. 이는 Discovery 산출물(의도·요구·제약·리스크)로서는 충분하지만, 구현 착수 전 기술 설계로서는 공백이다.
- **`requirements.functional`(4항)**이 요구하는 4개 뷰(run 목록 요약·이벤트 타임라인+게이트·revision/artifact 계보·토큰/비용 집계)는 각각 서로 다른 데이터 소스(`events.jsonl`·`revisions.jsonl`·`artifacts.jsonl`·`logs/invoke-*.json`)를 서로 다른 방식(seq 정렬·basis 인과 사슬·derivedFrom 파생·모델별 집계)으로 가공해야 한다 — 단일 파서 함수로 환원되지 않는 복수 설계 결정이 필요하다.
- **`risks`(4항)** 중 "데이터 형식 드리프트"(완화="파서 계층 격리")·"Windows 경로/인코딩"(완화="UTF-8 강제·경로 정규화")은 완화 *방향*만 사용자 진술로 주어졌을 뿐, 그 방향을 실현하는 구체적 인터페이스 경계·정규화 절차는 미확정이다.
- **`architectureDirection.open`(2항)**은 모두 "MVP 밖·확장 시 결정"으로 명시 스코프 아웃되어 있어 이 성숙 run의 대상이 아니다 — 즉 이 판정은 open 항목의 해소를 근거로 삼지 않는다(그 경우라면 스킵이 정당했을 것). needed 판정의 근거는 open 항목이 아니라, MVP 범위 **내부** requirements를 구현 가능한 설계로 끌어올리는 공백이다.
- **`readiness`**는 이미 완전성·confidence vector·사용자 승인을 전건 충족해 "Ready"(2축 판정)에 도달했다 — 이는 Discovery 산출물의 품질 게이트를 통과했다는 뜻이지, 구현 착수에 필요한 기술 설계가 이미 존재한다는 뜻은 아니다. Ready와 "설계 완결"은 별개 축이다.

무근거로 성숙을 강제하지 않기 위해 반대 방향(skip)도 검토했다 — Ready 상태·사용자 승인 기완료·assumptionLedger 빈 원장은 skip 쪽 신호였으나, 위 requirements의 다면적 데이터 가공 요구와 architectureDirection의 원칙 수준 서술 사이의 간극이 이를 상회한다고 판단했다.

## 3. 식별 관심사 (2)

1. **데이터/파싱/도메인 모델 설계** — `orchestration-data/runs/` 하위 append-only 원장(events/revisions/artifacts)과 `logs/invoke-*.json`을 도메인 모델로 정규화하는 설계: 이벤트 분류(step/게이트/annotation) 판별, 게이트 pending/해소 판별, revision basis 인과 사슬·artifact derivedFrom 파생 사슬의 계보 그래프 변환, 읽기 전용 안전성과 Windows 경로/UTF-8/CRLF 리스크 완화, 파서 계층 격리 경계.
2. **UI/뷰 아키텍처 설계** — Next.js/React/TS + Tailwind/shadcn 스택 위에서 run 목록 테이블과 단일 run 심층 뷰(타임라인+게이트+계보+비용 패널)를 구성하는 페이지/컴포넌트 분해, 데이터 계층과의 인터페이스 계약(RSC vs API route 경계 포함).

## 4. 할당 역할 (2 — SP-INV 8 최소 할당 충족)

| roleId | capability |
|---|---|
| `data-layer-designer` | 관심사 1(데이터/파싱/도메인 모델 설계)에 대해 설계 결정을 끌어올린다 |
| `ui-view-designer` | 관심사 2(UI/뷰 아키텍처 설계)에 대해 설계 결정을 끌어올린다 |

역할명은 이 run의 개방 네임스페이스 자유 논리 선언이며 고정 카탈로그를 참조하지 않는다. 두 역할은 Contract의 `architectureDirection.decisions`가 이미 선언한 "파서/데이터 계층 ↔ 도메인 모델 ↔ UI 컴포넌트" 분리와 1:1 대응하므로 3번째 역할(예: 리스크 전담)을 별도로 두지 않고 관심사 1에 접합했다 — 최소 할당 원칙 준수.
