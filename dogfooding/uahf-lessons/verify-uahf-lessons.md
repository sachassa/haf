# verify-uahf-lessons — Verifier 독립 검증 리포트 (CP2)

- 판정자: Verifier (독립 판정 CP2 — 02 §3.1, 03 §3.1-A). 실행 모델 Opus.
- 판정 일시: 2026-07-06.
- 판정 방식: Worker 완료 보고를 근거로 삼지 않고(06 INV-1·V1), Verifier가 **직접 CLI를 실행하고 산출물을 관측한 결과만**을 근거로 판정한다. 모든 건수는 CLI와 무관한 독립 json 파싱으로 교차 확인했다(VT-2/VT-5).
- 최종 판정 규칙: 06 §3.2-C (모든 충족→Pass / 하나라도 위반→Fail / 위반 없고 판정불가 존재→Conditional).

---

## target (판정 대상)

- CLI 구현: `dogfooding/uahf-lessons/src/uahf_lessons.py` (Python 3, 표준 라이브러리만).
- 호출: `python dogfooding/uahf-lessons/src/uahf_lessons.py <index-path> [--status V] [--kind V] [--stable-id V]`
- 대상 인덱스(읽기 전용): `framework/adapters/claude/memory-data/index/index.jsonl` (61라인, 18621 bytes)
- Memory store: `framework/adapters/claude/memory-data/store/` (61 파일). 트리 총 62 파일.
- 실행 환경: Python 3.14.4 (Windows). `python --version` 실행 관측.

## criteria_basis (대조 기준 출처)

- `docs/v1.0-dogfooding-spec.md` §1.2(출력 형식·5필드·0매칭), §3(라인 필터 의미론 DI-SEM-1~4), §4(완료 기준 케이스 a~e·DI-INV-1~4), §4.1(보조 실측 케이스). **유일 기준원.**
- 완료 기준 수치는 대상 index.jsonl 실측값(spec §0). Verifier가 착수 시 재실측으로 교차 대조함(L-15).

## 독립 교차검증 근거 (CLI 무관 json 파싱)

Verifier 자체 파싱(`json.loads` 라인별) 결과 — CLI 출력과 대조할 기준선:

```
total records: 61
by kind: {'lesson': 33, 'best-practice': 19, 'recurrence-judgment': 9}
status Active: 19 | status Candidate: 33
lesson+Active: 15 | best-practice+Active: 4 | recurrence+Active: 0
stable_id L-07: 2 | matched_lesson_id L-07: 3
```

독립 파싱값이 spec §4·§4.1 전 수치와 일치한다. 아래 각 항목은 (CLI 관측값) == (독립 파싱값) == (spec 기대값) 삼중 일치를 근거로 판정한다.

---

## items (항목별 판정)

### I-1 · 케이스 a — 무필터 총계 (VT-2/VT-5)
- criterion: `<index-path>` (무필터) → `matched: 61`, 레코드 61건 표시, exit 0.
- verdict: **충족(Met)**
- evidence: `python <cli> <idx>` → `summary_line: matched: 61`, `printed_record_lines: 61`, `exit: 0`. 독립 파싱 total=61 일치.
- scope: 실제 index.jsonl 전체 실행 관측 + 독립 json 파싱 대조.
- verification_type: VT-2(완료 조건 대조)·VT-5(시연 관측).

### I-2 · 케이스 b — --status Active (VT-2)
- criterion: `--status Active` → `matched: 19`.
- verdict: **충족(Met)**
- evidence: `python <cli> <idx> --status Active` → `matched: 19`, `printed_record_lines: 19`, `exit: 0`. 독립 파싱 Active=19 일치.
- scope: 실행 관측 + 독립 파싱 대조.
- verification_type: VT-2/VT-5.

### I-3 · 케이스 c — --kind recurrence-judgment (VT-2)
- criterion: `--kind recurrence-judgment` → `matched: 9`.
- verdict: **충족(Met)**
- evidence: `python <cli> <idx> --kind recurrence-judgment` → `matched: 9`, `printed_record_lines: 9`, `exit: 0`. 독립 파싱 recurrence-judgment=9 일치.
- scope: 실행 관측 + 독립 파싱 대조.
- verification_type: VT-2/VT-5.

### I-4 · 케이스 d — 부재 경로 오류 (VT-2/VT-5, DI-INV-2)
- criterion: `./no-such-file.jsonl` → stderr 오류 + **0 아닌 종료 코드**, 어떤 파일도 읽지/쓰지 않고 실패.
- verdict: **충족(Met)**
- evidence: `python <cli> ./no-such-file.jsonl` → `exit: 2`(0 아님), stdout 비어 있음, stderr = `error: index 파일을 찾을 수 없습니다: ./no-such-file.jsonl`, `no-such-file created? False`(부작용 없음). 종료 코드는 `$LASTEXITCODE`로 파이프 없이 직접 포착.
- scope: 실행 관측. Python 자체 exit code 2 확인. (PowerShell이 자식 stderr를 NativeCommandError로 감싸나 실제 오류 메시지 원문 present.)
- verification_type: VT-2/VT-5.

### I-5 · 케이스 e — 읽기 전용 (VT-4, DI-INV-3) — 전수 스캔
- criterion: a~c 등 실행 전후 index.jsonl 및 store 파일 무변경(바이트·mtime).
- verdict: **충족(Met)**
- evidence: 실행 전/후 memory-data **트리 전체(62 파일)** MD5 집계 해시 비교 —
  - PRE  aggregate MD5 = `dd4214ebe3f51cada6adcb9c7009659e`
  - POST aggregate MD5 = `dd4214ebe3f51cada6adcb9c7009659e` (동일)
  - index.jsonl size 18621→18621, mtime `2026-07-06T12:42:21.8612260Z`→동일.
  - `Compare-Object` 결과 = `TREE DIFF: NONE (0 changes)`.
  - 코드 레벨 corroboration: 소스 전수 스캔 결과 파일 연산은 line 85 `open(path, "r", ...)` **1건(읽기 모드)뿐**, `.write`/`os.remove`/`rename`/`shutil`/append·truncate 0건.
- scope: 단일 파일이 아닌 트리 전체(index+store 61) 바이트·mtime 대조 + 소스 mutation 전수 스캔. 동시성/ACL 레벨은 범위 밖.
- verification_type: VT-4(경계 전수 스캔).

### I-6 · §4.1 --status Candidate = 33 (VT-2)
- verdict: **충족(Met)** — evidence: `--status Candidate` → `matched: 33`, exit 0. 독립 파싱 33 일치. scope: 실행+파싱 대조. VT-2.

### I-7 · §4.1 --kind lesson = 33 (VT-2)
- verdict: **충족(Met)** — evidence: `--kind lesson` → `matched: 33`, exit 0. 독립 파싱 33 일치. VT-2.

### I-8 · §4.1 --kind best-practice = 19 (VT-2)
- verdict: **충족(Met)** — evidence: `--kind best-practice` → `matched: 19`, exit 0. 독립 파싱 19 일치. VT-2.

### I-9 · §4.1 조합 --kind lesson --status Active = 15 (AND, VT-2)
- verdict: **충족(Met)** — evidence: → `matched: 15`, exit 0. 독립 파싱 lesson∧Active=15 일치. AND 의미론(DI-SEM-2) 실증. VT-2.

### I-10 · §4.1 조합 --kind best-practice --status Active = 4 (AND, VT-2)
- verdict: **충족(Met)** — evidence: → `matched: 4`, exit 0. 독립 파싱 4 일치. VT-2.

### I-11 · §4.1 조합 --kind recurrence-judgment --status Active = 0 (DI-SEM-3) + 0매칭 exit 0 (VT-5)
- verdict: **충족(Met)**
- evidence: → `matched: 0`, `header_present: False`(헤더 없이 빈 결과), `exit: 0`(오류 아님). 재발 판정 라인은 status 라벨 부재→매칭 0(DI-SEM-3). 독립 파싱 0 일치. §1.2 "0 매칭도 정상 종료" 동시 실증.
- scope: 실행 관측. verification_type: VT-2/VT-5.

### I-12 · §4.1 --stable-id L-07 = 2 (DI-SEM-4, VT-2)
- verdict: **충족(Met)**
- evidence: `--stable-id L-07` → `matched: 2`; 표시 = `mi-0007 lesson Candidate L-07 …` + `mi-0015 lesson Active L-07 …`(동일 stable_id의 Candidate/Active 라인이 별개 레코드로 2건 — DI-SEM-1 라인 필터 실증). 독립 파싱 stable_id L-07=2, matched_lesson_id L-07=3(대상 아님) 확인 — `matched_lesson_id` 참조 3건은 정확히 제외(DI-SEM-4).
- scope: 실행+파싱 대조. verification_type: VT-2/VT-5.

### I-13 · §1.2 표시 5필드 + 부재 라벨 '-' (VT-3)
- criterion: 각 레코드에 `id, kind, labels.status, labels.stable_id, digest` 표시, 부재 라벨은 `-`.
- verdict: **충족(Met)**
- evidence: 헤더 `id\tkind\tstatus\tstable_id\tdigest` 출력. recurrence-judgment 라인 = `mi-0019  recurrence-judgment  -  -  재발 판정 Novel …`(status·stable_id 부재→`-`). lesson 라인 = 5필드 전부 present.
- scope: 실행 출력 직접 관측. verification_type: VT-3(규격 준수).

### I-14 · 표준 라이브러리만 사용 (VT-4) — 전수 스캔
- criterion: 외부 패키지 의존 0, stdlib만.
- verdict: **충족(Met)**
- evidence: 소스 import 전수 스캔 = `import argparse` / `import json` / `import sys` (line 25~27) 3건뿐, 전부 stdlib. `from`/기타 import 0건. 실제 실행이 외부 의존 없이 Python 3.14.4에서 완주.
- scope: 소스 전수 import 스캔 + 실행 관측. verification_type: VT-4.

---

## final_verdict

**Pass (통과)**

- 항목 판정 집계: 충족(Met) **14** / 위반(Violated) **0** / 판정 불가(Undetermined) **0**.
- 도출(06 §3.2-C 결정적): 전 항목 충족 → **Pass**. 동일 판정 집합은 항상 동일 결론.
- §4 필수 케이스 a~e 전부 실행 관측으로 충족(DI-INV-4 실제 실행 관측 성립). §4.1 보조 케이스 전부 일치. 거짓 완료 보고 징후 없음 — CLI 관측값이 독립 파싱값과 전 항목 일치.

## verifier_scope (검사 범위·제외)

- **검사한 것**: 실제 index.jsonl(61라인)에 대해 §4 a~e + §4.1 7개 보조 케이스 CLI 직접 실행, `matched:` 요약·표시 레코드 수·Python exit code(`$LASTEXITCODE`, 파이프 없음) 포착. 모든 건수를 CLI 무관 독립 json 파싱으로 교차. 읽기 전용은 트리 전체(62 파일) MD5 전후 대조 + 소스 mutation 전수 스캔. stdlib·5필드·'-'·0매칭 exit 0 확인.
- **제외/한계**:
  - malformed 라인 처리(spec OQ-V1)는 §4 필수 기준 밖(정형 파일 대상)이므로 미검증 — 비차단. 현 index.jsonl은 61라인 전부 정형.
  - Node 런타임 미검증 — Worker가 Python 택1(§6). 택한 런타임만 판정.
  - Scaffold 설치(§5 done 4)는 별도 Task 소관 — 본 판정 범위 밖(본 리포트는 §4 CLI 동작 완료 기준만 판정).
  - 읽기 전용은 바이트·mtime·소스 레벨로 증명. 파일시스템 ACL/동시성 레벨은 범위 밖.

## rework

- 없음 (final_verdict = Pass).
