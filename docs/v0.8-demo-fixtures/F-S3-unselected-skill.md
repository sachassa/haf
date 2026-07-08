시연 픽스처 — 실계약 문서 아님.

# F-S3 — 미선택 Skill 픽스처 (지연 로드 대조용)

이 파일은 v0.8 Skills 확장 시연(EX-DS)의 **보조 픽스처**다. 실계약 문서가 아니다(검증 대상 계약 아님). 결함은 없다 — 미선택은 실패가 아니며, `NoMatchingSkill` 빈 결과와도 구분되는 **대조 대상**이다(발견 후보 집합에 다른 Skill이 있는 상태에서 이 Skill만 미선택되는 상황). 이 픽스처는 `docs/v0.8-demo-fixtures/` 격리 경계 안에만 존재하고 라이브 표면에 배치되지 않는다. 등록은 **형태 A 규약 등록**(skills-binding §2 행 2 / DP-E7)으로 실현한다. verifier_scope 제외(§4.1).

이 픽스처의 목적: 시연 작업 컨텍스트("커밋 생성 작업")에 대해 발견·선택이 수행될 때, **`trigger`가 컨텍스트에 매칭되지 않아 미선택**되고, 따라서 이 Skill의 **Markdown 본문(`body`)이 Context에 로드되지 않음**(INV-4·지연 로드, skills-binding §5.1 단계 4)을 확인하는 대조물이다. 발견·선택은 이 Skill의 front-matter(메타데이터)만 열람하고 본문은 열지 않는다.

## Skill Manifest (형태 A — 규약 등록 서술)

메타데이터 9필드 = front-matter, `body` = 본문 (skills-binding §3.2 정본 표기).

```yaml
id: db-migration-generator
contract: SkillInterface
version: "1.0"
name: Database Migration Generator
purpose: 스키마 변경으로부터 데이터베이스 마이그레이션 스크립트 초안 작성
trigger: 데이터베이스 마이그레이션 스크립트 생성 작업
io:
  input: 스키마 변경 요약
  output: 마이그레이션 스크립트 초안
requires: []
replaceable: true
```

- **trigger 비매칭 근거.** 시연 작업 컨텍스트는 "커밋 생성 작업"(F-S1이 매칭되는 컨텍스트)이다. 이 Skill의 `trigger`="데이터베이스 마이그레이션 스크립트 생성 작업"은 그 컨텍스트에 매칭되지 않는다 → 후보 집합에 들지 않음(미선택).

## body (지연 로드 대조 — 발견·선택 단계에서 비로드)

아래 본문은 **발견·선택 단계에서 Context에 로드되지 않아야 한다**(INV-4). 미선택 Skill의 body가 로드되면 검증 실패(09 §6). 이 본문의 존재 자체는 대조를 위한 것이며, 시연 발견 단계는 이 텍스트를 열지 않는다.

--- (아래는 미선택 시 비로드되어야 할 body 텍스트) ---

1. 스키마 변경 요약을 읽는다.
2. 변경 유형(테이블 추가·컬럼 변경·인덱스 등)을 식별한다.
3. up/down 마이그레이션 스크립트 초안을 작성한다.
4. 마이그레이션 스크립트 초안을 산출한다.

(위 body는 발견·선택에서 로드되지 않았음을 관측 기록으로 확인한다 — ex-ds-skills-observation.md.)
