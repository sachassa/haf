---
meta:
  id: pc-tms-001
  schemaVersion: "1.0"
  instanceVersion: 1
  supersedes: null
intent: >-
  국내 화물자동차(트럭) 운송주선업(3인 사업장)을 위한 운송관리시스템(TMS).
  화주의 화물을 받아 차주/운송사에 배차하고 운송을 관리하며 운임을 정산하는 종합 전산 시스템.
  도입 동기 4가지 전부: (1) 수작업(엑셀·전화·수기) 비효율 해소, (2) 물량·거래처 확장 대비,
  (3) 정산 정확도·비용 절감, (4) 화주/기사 대상 가시성·서비스 차별화.
  전 과정(수주 → 배차 → 운송 → 정산)을 전산화하되 최우선은 정산이다.
requirements:
  functional:
    - id: F1
      name: 수주·오더 관리
      내용: 화주 화물 접수 — 상·하차지, 품목·중량, 희망일시, 운임.
    - id: F2
      name: 배차 관리
      내용: >-
        세 채널 병행 — (a) 고정·전속 차주 직배차, (b) 화물정보망(24시콜·화물맨 등) 수시 섭외,
        (c) 용차(협력 운송사) 재위탁. 배차 확정·기사 통보 포함.
    - id: F3
      name: 운송 진행·추적
      내용: 상차 → 운송 → 하차 상태 관리, 인수증(인수확인).
    - id: F4
      name: 정산 (최우선)
      내용: >-
        (a) 화주 청구운임 ↔ 차주/용차 지급운임 건별 자동 대조(2자·3자 정산 혼재),
        (b) 화주·노선·건별 단가표 기반 자동 계산,
        (c) 전자세금계산서 발행/역발행 수취,
        (d) 월마감·미수/미지급 자동 집계·대사.
    - id: F5
      name: 거래처·차량·단가 마스터
      내용: 화주·차주·운송사·차량 정보, 노선/구간 단가표.
    - id: F6
      name: 실적·매출 리포트·조회
      내용: 매출·건수·미정산 현황 통계.
    - id: F7
      name: 대외 채널
      내용: 화주용 조회 포털, 기사용 모바일(배차 수락·상태 입력·인수증 사진 전송).
    - id: F8
      name: 외부 연동
      내용: >-
        전자세금계산서, 문자·카카오 알림, 회계·ERP 연동.
        (화물정보망 연동은 리스크로 별도 — risks 참조.)
    - id: F9
      name: 예외 처리
      내용: >-
        재배차(기사 펑크/취소), 화물 사고·클레임, 정산 이의·수정·재발행,
        미수·연체 관리(추적·독촉 근거).
  quality:
    - id: Q1
      name: 권한·접근 통제
      내용: 화주는 자기 건만, 기사는 자기 배차만, 정산 등 민감정보는 내부만 접근.
    - id: Q2
      name: 기존 엑셀 데이터 이관
      내용: 거래처·단가표·미정산 내역 초기 이관.
constraints:
  - id: C1
    내용: >-
      3인 사업장(관리자 + 배차·정산 겸직자 + 1) — 내부 역할 분리가 약함 →
      권한 설계 단순(겸용 화면 중심).
  - id: C2
    내용: >-
      도입 방식 = 정산부터 단계적 확장(핵심 먼저 출시 후 리포트·포털·연동 순차 확대).
  - id: C3
    내용: 전달 접점 3개 — 사무실 웹(PC) + 기사용 모바일 + 화주용 조회 포털.
risks:
  - id: R1
    수준: high
    name: 화물정보망 자동연동 (⚠️)
    내용: >-
      사용자가 자동 연동을 필수 요구했으나 대부분의 화물정보망은 외부 공식 API를 제공하지 않는다 →
      실현 불가 또는 크롤링 등 비공식 수단(약관 위반·법적 위험·불안정) 우려.
      다음 단계(Solution Design)에서 대상 정보망별 실현 가능성·법적 위험을 별도 검증하고,
      미해소 시 반자동(엑셀 업로드/붙여넣기)으로 폴백한다. 요구 자체는 사용자 결정으로 유지.
  - id: R2
    내용: >-
      2자·3자 정산 혼재로 인한 정산 로직 복잡도 — 핵심 난이도이자 최우선 모듈의 위험.
  - id: R3
    내용: 운영 예외 — 재배차(펑크)·화물 사고/클레임·정산 이의/수정·미수/연체.
architectureDirection:
  decisions:
    - id: D1
      내용: 접점 3개 — 내부 사무실 웹 · 기사 모바일 · 화주 조회 포털.
    - id: D2
      내용: >-
        외부 연동 — 전자세금계산서·문자/카카오 알림·회계/ERP(정식 연동),
        화물정보망(조건부·검증 필요).
    - id: D3
      내용: 정산 우선 단계적 구축.
    - id: D4
      내용: 배포 = 클라우드(SaaS) — 가정(assumptionLedger A2 참조).
  open:
    - id: O1
      내용: 화물정보망 연동 실현 방식(자동 vs 반자동) — 대상 정보망별 검증 필요.
    - id: O2
      내용: 배차 상세 기준(누가·어떤 우선순위로 어느 채널을 선택하나) — Solution Design에서 구체화.
    - id: O3
      내용: 회계/ERP 대상 제품 미확정.
    - id: O4
      내용: >-
        상세 설계(화면·데이터모델/ERD·API 명세·Wireframe)는 Discovery 범위 밖 →
        Solution Design 이후.
assumptionLedger:
  - id: A1
    대상필드: Intent / Requirements
    내용: 화주는 주로 기업으로 가정(개인 화주 여부 미확인).
    근거: 사용자 미언급·가정.
    상태: 미해결
  - id: A2
    대상필드: Architecture Direction / Constraints
    내용: 배포 = 클라우드(SaaS) 가정.
    근거: 3인 소규모 + 다접점 기본값.
    상태: 미해결
  - id: A3
    대상필드: Requirements(quality)
    내용: 자동 백업은 미선택이나 데이터 유실 방지 baseline으로 최소 수준 반영 권장.
    근거: 운영 기본 안전장치.
    상태: 미해결
  - id: A4
    대상필드: Requirements(quality)
    내용: 감사이력(변경 추적)은 사용자 미선택으로 범위 밖 처리하나, 정산 이의/수정 대비상 권장.
    근거: 사용자 미선택 vs 예외 요구 상충.
    상태: 미해결
  - id: A5
    대상필드: Requirements
    내용: 사용 시점·장소(WHEN/WHERE) = 사무실 업무시간 + 기사 현장 실시간(모바일) 가정.
    근거: 명시 질의 없이 추정.
    상태: 미해결
  - id: A6
    대상필드: Architecture Direction
    내용: 회계/ERP 대상 제품·화물정보망 대상 서비스명 미확정.
    근거: 구체 대상 미수집.
    상태: 미해결
readiness:
  completeness: >-
    필수 코어 필드 10 전건 충족(일부는 가정으로 충족 — assumptionLedger 기재).
  confidenceVector: >-
    5차원(Intent·Requirement·Constraint·Risk·Architecture) 방향 수준 포화
    (breadth-first 1회전 완료).
  openQuestions:
    - 화물정보망 연동 실현성 검증
    - 배차 상세 기준
    - 회계/ERP·정보망 대상 제품 확정
    - 화주 유형(기업/개인) 확정
    - 감사이력·백업 최종 결정
  userApproval: >-
    승인됨 — 2026-07-18, 사용자 최종 승인 게이트(Validating) 통과, "승인 — 이대로 확정".
provenance:
  runId: greenfield-tms-system-001
  mode: greenfield
  entry:
    name: "/new"
    물리발화: uaf-new
    intent: new
    matchedRow: 1
    gate: false
  inputs:
    - contract-presence: 무
    - repository-presence: 무
  policy: default
  discoveryProvider: 레퍼런스 적응 질문 Provider(discovery-interview v1.4 breadth-first)
  discoveryTerminal: ReadyWithAssumptions
  date: 2026-07-18
  주: 내부 형식은 비계약(불투명). UAHF tolerant reader는 이 컨테이너 전체를 must-ignore한다.
---

# Project Contract — 운송관리시스템(TMS)

> 이 문서는 Project Contract v1 인스턴스다. 위 YAML front-matter가 기계 파싱 가능한
> 자기서술 구조(9 그룹·필수 코어 필드 10)를, 아래 본문이 같은 정의의 한국어 인간 가독
> 렌더링을 담는다. 종단 = ReadyWithAssumptions(assumptionLedger 6건 전부 미해결).
> `provenance` 컨테이너는 불투명 부속으로 UAHF must-ignore 대상이다.

## 1. 정체성·의도 (Meta · Intent)

- 인스턴스 식별자: `pc-tms-001`
- schemaVersion: `1.0` / instanceVersion: `1` / supersedes: 없음(최초 인스턴스)

국내 화물자동차(트럭) **운송주선업(3인 사업장)**을 위한 **운송관리시스템(TMS)**이다.
화주의 화물을 받아 차주/운송사에 배차하고 운송을 관리하며 운임을 정산하는 종합 전산 시스템이다.

도입 동기는 네 가지 모두다.

1. 수작업(엑셀·전화·수기) 비효율 해소
2. 물량·거래처 확장 대비
3. 정산 정확도·비용 절감
4. 화주/기사 대상 가시성·서비스 차별화

전 과정(수주 → 배차 → 운송 → 정산)을 전산화하되 **최우선은 정산**이다.

## 2. 기능 요구 (Requirements · Functional)

1. **수주·오더 관리** — 화주 화물 접수(상·하차지, 품목·중량, 희망일시, 운임).
2. **배차 관리** — 세 채널 병행: (a) 고정·전속 차주 직배차, (b) 화물정보망(24시콜·화물맨 등)
   수시 섭외, (c) 용차(협력 운송사) 재위탁. 배차 확정·기사 통보 포함.
3. **운송 진행·추적** — 상차 → 운송 → 하차 상태 관리, 인수증(인수확인).
4. **정산 (최우선)** — (a) 화주 청구운임 ↔ 차주/용차 지급운임 **건별 자동 대조(2자·3자 정산 혼재)**,
   (b) 화주·노선·건별 **단가표 기반 자동 계산**, (c) **전자세금계산서** 발행/역발행 수취,
   (d) **월마감·미수/미지급 자동 집계·대사**.
5. **거래처·차량·단가 마스터** — 화주·차주·운송사·차량 정보, 노선/구간 단가표.
6. **실적·매출 리포트·조회** — 매출·건수·미정산 현황 통계.
7. **대외 채널** — 화주용 조회 포털, 기사용 모바일(배차 수락·상태 입력·인수증 사진 전송).
8. **외부 연동** — 전자세금계산서, 문자·카카오 알림, 회계·ERP. (화물정보망 연동은 리스크로 별도 — §5 참조.)
9. **예외 처리** — 재배차(기사 펑크/취소), 화물 사고·클레임, 정산 이의·수정·재발행,
   미수·연체 관리(추적·독촉 근거).

## 3. 품질 요구 (Requirements · Quality)

- **권한·접근 통제** — 화주는 자기 건만, 기사는 자기 배차만, 정산 등 민감정보는 내부만 접근한다.
- **기존 엑셀 데이터 이관** — 거래처·단가표·미정산 내역 초기 이관.

## 4. 제약 (Constraints)

- **3인 사업장**(관리자 + 배차·정산 겸직자 + 1) — 내부 역할 분리가 약함 → 권한 설계 단순(겸용 화면 중심).
- **도입 방식** — 정산부터 단계적 확장(핵심 먼저 출시 후 리포트·포털·연동 순차 확대).
- **전달 접점 3개** — 사무실 웹(PC) + 기사용 모바일 + 화주용 조회 포털.

## 5. 리스크 (Risks)

- ⚠️ **화물정보망 자동연동** — 사용자가 자동 연동을 필수 요구했으나, 대부분의 화물정보망은
  외부 공식 API를 제공하지 않는다 → 실현 불가 또는 크롤링 등 비공식 수단(약관 위반·법적 위험·불안정)
  우려. **다음 단계(Solution Design)에서 대상 정보망별 실현 가능성·법적 위험을 별도 검증**하고,
  미해소 시 반자동(엑셀 업로드/붙여넣기)으로 폴백한다. (요구 자체는 사용자 결정으로 유지.)
- **2자·3자 정산 혼재로 인한 정산 로직 복잡도** — 핵심 난이도이자 최우선 모듈의 위험.
- **운영 예외** — 재배차(펑크)·화물 사고/클레임·정산 이의/수정·미수/연체.

## 6. 아키텍처 방향 (Architecture Direction)

### 6.1 결정 (Decisions)

- 접점 3개 — 내부 사무실 웹 · 기사 모바일 · 화주 조회 포털.
- 외부 연동 — 전자세금계산서·문자/카카오 알림·회계/ERP(정식 연동), 화물정보망(조건부·검증 필요).
- 정산 우선 단계적 구축.
- 배포 = 클라우드(SaaS) — 가정(가정 원장 A2 참조).

### 6.2 미결 (Open)

- 화물정보망 연동 실현 방식(자동 vs 반자동) — 대상 정보망별 검증 필요.
- 배차 상세 기준(누가·어떤 우선순위로 어느 채널을 선택하나) — Solution Design에서 구체화.
- 회계/ERP 대상 제품 미확정.
- 상세 설계(화면·데이터모델/ERD·API 명세·Wireframe)는 Discovery 범위 밖 → Solution Design 이후.

## 7. 가정 원장 (Assumption Ledger)

종단이 **ReadyWithAssumptions**이므로 원장은 비어 있지 않다. 아래 6건 전부 상태 = **미해결**이다.

| ID | 대상 필드 | 내용 | 근거 | 상태 |
|---|---|---|---|---|
| A1 | Intent / Requirements | 화주는 주로 **기업**으로 가정(개인 화주 여부 미확인) | 사용자 미언급·가정 | 미해결 |
| A2 | Architecture Direction / Constraints | 배포 = **클라우드(SaaS)** 가정 | 3인 소규모 + 다접점 기본값 | 미해결 |
| A3 | Requirements(quality) | **자동 백업**은 미선택이나 데이터 유실 방지 baseline으로 최소 수준 반영 권장 | 운영 기본 안전장치 | 미해결 |
| A4 | Requirements(quality) | **감사이력(변경 추적)**은 사용자 미선택으로 범위 밖 처리하나, 정산 이의/수정 대비상 권장 | 사용자 미선택 vs 예외 요구 상충 | 미해결 |
| A5 | Requirements | 사용 시점·장소(WHEN/WHERE) = 사무실 업무시간 + 기사 현장 실시간(모바일) 가정 | 명시 질의 없이 추정 | 미해결 |
| A6 | Architecture Direction | 회계/ERP 대상 제품·화물정보망 대상 서비스명 미확정 | 구체 대상 미수집 | 미해결 |

## 8. Readiness

- **Completeness** — 필수 코어 필드 10 전건 충족(일부는 가정으로 충족 — 가정 원장 기재).
- **Confidence Vector** — 5차원(Intent·Requirement·Constraint·Risk·Architecture) 방향 수준 포화
  (breadth-first 1회전 완료).
- **Open Questions**
  1. 화물정보망 연동 실현성 검증
  2. 배차 상세 기준
  3. 회계/ERP·정보망 대상 제품 확정
  4. 화주 유형(기업/개인) 확정
  5. 감사이력·백업 최종 결정
- **User Approval** — 승인됨 (2026-07-18). 사용자 최종 승인 게이트(Validating) 통과 — "승인 — 이대로 확정".

## 9. Provenance (주석 — 불투명 부속)

> 아래는 이 Contract를 생성한 Discovery 실행의 메타다. **불투명 부속(opaque annex)**이며
> UAHF는 이 컨테이너 전체를 **must-ignore**한다. 내부 형식은 비계약이다.

- runId: `greenfield-tms-system-001`
- mode: greenfield
- entry: name=`/new`, 물리발화=uaf-new, intent=new, matchedRow=1, gate=false
- inputs: contract-presence(무), repository-presence(무)
- policy: default
- discoveryProvider: 레퍼런스 적응 질문 Provider (discovery-interview v1.4 breadth-first)
- discoveryTerminal: ReadyWithAssumptions
- date: 2026-07-18
