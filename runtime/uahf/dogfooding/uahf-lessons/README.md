# uahf-lessons — UAHF Memory Index 열람 CLI (v1.0 Dogfooding 산출물)

`uahf-lessons`는 UAHF Memory Index 파일(`index.jsonl`)을 읽어, Lesson / Best Practice /
재발 판정 레코드를 `--status` / `--kind` / `--stable-id` 필터(조합 가능, AND)로 조회·표시하는
**읽기 전용 CLI 열람 유틸리티**다. 이 프로젝트는 UAHF를 Scaffold로 설치한 뒤(핵심 루프로)
개발한 v1.0 Dogfooding 대상이다.

- 확정 명세(인터페이스·필터 의미론·완료 기준): `docs/v1.0-dogfooding-spec.md` §1~§4.
- 읽는 파일 포맷 정본: `framework/adapters/claude/memory-binding.md` §2 #4·§5.1·§5.4.
- 성격(DP-V4, 명세 §7): 직렬화 파일에 대한 외부 열람 유틸리티 — Memory에 쓰지 않는다.
- 런타임: Python 3 (표준 라이브러리 `argparse`·`json`·`sys`만 사용, 외부 의존 0).

## 실행

이 CLI는 단일 모듈 `src/uahf_lessons.py`로 구현된다. 논리 명령 `uahf-lessons`는
물리 실행 `python src/uahf_lessons.py`에 대응한다.

```
python src/uahf_lessons.py <index-path> [--status <값>] [--kind <값>] [--stable-id <값>]
```

- `<index-path>` (필수) — 읽을 `index.jsonl` 경로. 부재 시 stderr 오류 + 0이 아닌 종료 코드.
- `--status`  (선택) — `labels.status` == 값 인 라인만 (Candidate/Active/Superseded/Retired).
- `--kind`    (선택) — `kind` == 값 인 라인만 (lesson/best-practice/recurrence-judgment).
- `--stable-id` (선택) — `labels.stable_id` == 값 인 라인만 (예: L-07, BP-01).
- 여러 필터 동시 지정 시 논리곱(AND). 무필터면 전체 레코드.

## 출력

- 매칭된 각 레코드 1라인(탭 구분 5필드): `id`, `kind`, `status`, `stable_id`, `digest`
  (라벨 부재 시 `-`). 매칭이 있으면 머리 행을 1개 낸다.
- 말미에 건수 요약 `matched: N`. 0 매칭도 오류가 아니다 — `matched: 0` + 종료 코드 0.

## 예 (본 리포 index 대상 — 실측)

```
python src/uahf_lessons.py ../../framework/adapters/claude/memory-data/index/index.jsonl
    → matched: 61
python src/uahf_lessons.py <index> --status Active
    → matched: 19
python src/uahf_lessons.py <index> --kind recurrence-judgment
    → matched: 9
python src/uahf_lessons.py ./no-such-file.jsonl
    → error (stderr) + exit 2
```

## 부작용

없음 — 읽기 전용. `index.jsonl` 및 Memory store 파일을 변경하지 않는다(명세 §4 DI-INV-3).
