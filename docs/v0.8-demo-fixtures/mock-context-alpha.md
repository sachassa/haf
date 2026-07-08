시연 픽스처 — 실계약 문서 아님.

# 모사 프로젝트 컨텍스트 A (alpha) — F-S1 재사용 시연용 (부분 재현 1/2)

이 파일은 v0.8 Skills 확장 시연(EX-DS)의 **재사용 시연(INV-5)** 보조 픽스처다. 실계약 문서가 아니다(검증 대상 계약 아님). 결함은 없다. `docs/v0.8-demo-fixtures/` 격리 경계 안에만 존재한다.

목적: 라이브 표면의 F-S1(`.claude/skills/commit-message-writer/`)을 **재등록만으로** 이 모사 프로젝트에 재사용하고, 프로젝트 특정 값이 **Config(01 §3.2-B)/`io.input`으로 주입**됨을 보인다(INV-5, skills-binding §5.3). **F-S1의 `body`는 불변이며**, 이 컨텍스트에 하드코딩되는 값은 0이다 — 모든 프로젝트 특정 값은 아래 주입 채널로 들어간다.

## 재사용 대상 (불변)

- Skill: `commit-message-writer` (F-S1, `.claude/skills/commit-message-writer/SKILL.md`).
- **`body` 불변.** 이 컨텍스트는 F-S1의 `body`를 수정·복제하지 않는다. 동일 `body`를 그대로 참조한다.
- **`io` 계약 불변.** `input`=변경 요약, `output`=커밋 메시지 초안.

## 프로젝트 A 특정 값 (주입만 — body 하드코딩 0)

이 값들은 F-S1 `body`에 없다. Config/`input`으로 주입된다.

| 프로젝트 특정 값 | 주입 채널 | 프로젝트 A 값 |
|---|---|---|
| 커밋 컨벤션 스타일 | Config (Module scope, `target`=commit-message-writer) | Conventional Commits (`type(scope): subject`) |
| 허용 타입 목록 | Config | feat / fix / docs / refactor / test / chore |
| 스코프 규칙 | Config | 디렉터리명 스코프 필수 |
| 이슈 접두어 | Config | `[PROJ-<번호>]` 제목 끝 부착 |
| 본문 언어 | Config | 영어 (English) |
| 제목 최대 길이 | Config | 50자 |

## 주입 예 (io.input)

- `변경 요약` = "인증 미들웨어에 토큰 만료 검증 추가" (호출 Agent 제공 입력).

## 기대 결과 (관측 대조는 ex-ds-skills-observation.md)

- F-S1 `body`의 5단계 절차가 **동일하게** 실행되고, 위 주입 값에 따라 프로젝트 A 스타일의 초안이 산출된다.
- `body`·`io` 계약은 프로젝트 B(beta)와 **동일(불변)**하며, 프로젝트 A와 B의 차이는 **주입 값뿐**이다(INV-5 재사용).
- 재현 범위: **부분 재현**(모사 컨텍스트 2종). 본문 하드코딩 0의 정적 대조는 CP2 소관(OQ-5, §2.3).
