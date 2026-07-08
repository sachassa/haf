#!/usr/bin/env python3
"""uahf-lessons — UAHF Memory Index 열람 유틸리티 (v1.0 Dogfooding CLI).

읽기 전용 CLI. UAHF Memory Index 파일(index.jsonl)을 읽어, 각 라인(레코드)을
--status / --kind / --stable-id 필터(각 선택·조합 가능, 논리곱 AND)로 조회·표시한다.

정본 경계 (이 파일은 아래 계약을 재정의하지 않고 소비한다):
  - CLI 인터페이스·필터 의미론·완료 기준 = docs/v1.0-dogfooding-spec.md §1~§4.
  - 읽는 파일 포맷(Index Entry 6필드·kind 3종·라벨 키) = memory-binding.md §2 #4·§5.1·§5.4.
성격 (DP-V4, 명세 §7): 직렬화 파일에 대한 **외부 열람 유틸리티**. Memory에 쓰지 않으며
  프레임워크 단일 Port(04)의 소비자가 아니다 — 백엔드가 남긴 파일을 밖에서 여는 도구다.

의존: 표준 라이브러리만 사용한다 (argparse, json, sys). 외부 패키지 의존 0.

필터 의미론 (명세 §3 — 라인 필터 기준):
  DI-SEM-1 각 라인 = 독립 레코드 (stable_id 최신 상태 해소 안 함).
  DI-SEM-2 --status→labels.status, --kind→kind, --stable-id→labels.stable_id; 다중 지정 시 AND.
  DI-SEM-3 대조 라벨이 없는 라인은 그 필터에 매칭되지 않는다.
  DI-SEM-4 --stable-id 는 labels.stable_id 만 대조 (labels.matched_lesson_id 는 대상 아님).

malformed 라인 정책 (명세 §8 OQ-V1, Advisor 확정):
  파싱 불가한 손상 라인은 **건너뛰고 경고(stderr) 후 정상 진행**한다. 종료 코드에 영향 없음.
"""

import argparse
import json
import sys

EXIT_OK = 0
EXIT_INPUT_ERROR = 2  # 필수 인자 부재·경로 미접근·읽기 불가 (명세 §4 케이스 d·DI-INV-2)


def configure_utf8_output():
    """표준 출력/오류를 UTF-8로 재설정한다.

    레코드 digest는 한국어 텍스트이며 em-dash(—, U+2014) 등을 포함한다. 일부 플랫폼의
    기본 콘솔 인코딩(예: cp949)은 이를 인코딩하지 못해 표시 중 UnicodeEncodeError로
    중단된다. 표준 라이브러리 TextIOWrapper.reconfigure 로 UTF-8 출력을 보장한다
    (읽기 전용 성격·필터 결과에는 영향 없음 — 출력 인코딩만 조정).
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass  # 재설정 불가 환경에서는 기본 인코딩을 그대로 쓴다.


def build_parser():
    parser = argparse.ArgumentParser(
        prog="uahf-lessons",
        description="UAHF Memory Index(index.jsonl) 읽기 전용 열람 유틸리티 "
                    "(Lesson/Best Practice/재발 판정 레코드 필터 조회).",
    )
    parser.add_argument(
        "index_path",
        metavar="<index-path>",
        help="읽을 Memory Index 파일 경로 (index.jsonl). 부재 시 오류 종료(exit != 0).",
    )
    parser.add_argument(
        "--status", metavar="<값>", default=None,
        help="labels.status 필터 (Candidate/Active/Superseded/Retired).",
    )
    parser.add_argument(
        "--kind", metavar="<값>", default=None,
        help="kind 필터 (lesson/best-practice/recurrence-judgment).",
    )
    parser.add_argument(
        "--stable-id", metavar="<값>", dest="stable_id", default=None,
        help="labels.stable_id 필터 (예: L-07, BP-01).",
    )
    return parser


def load_records(path):
    """index.jsonl 을 읽기 전용으로 열어 라인별 레코드를 파싱한다.

    반환: (records, malformed_lines). malformed 라인은 건너뛰고 경고(stderr)한다(OQ-V1).
    파일 부재·읽기 불가는 예외로 전파해 호출부(main)가 exit != 0 로 처리한다.
    """
    records = []
    malformed = 0
    # 'r' 모드 — 읽기 전용. 이 도구는 index.jsonl / store 에 쓰지 않는다(DI-INV-3).
    with open(path, "r", encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue  # 빈 줄은 레코드가 아니다.
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                malformed += 1
                print(
                    "warning: line {n}: malformed JSON — 건너뜀 ({e})".format(n=lineno, e=exc),
                    file=sys.stderr,
                )
    return records, malformed


def record_matches(record, status, kind, stable_id):
    """라인 필터 기준(명세 §3) 매칭. 대조 라벨이 없으면 매칭 실패(DI-SEM-3)."""
    labels = record.get("labels") or {}
    if kind is not None and record.get("kind") != kind:
        return False
    if status is not None and labels.get("status") != status:
        return False
    if stable_id is not None and labels.get("stable_id") != stable_id:
        return False
    return True


def render_record(record):
    """표시 필드 5개(명세 §1.2): id, kind, labels.status, labels.stable_id, digest.

    라벨 부재 시 '-' (명세 §1.2). 탭 구분 1라인.
    """
    labels = record.get("labels") or {}
    return "\t".join([
        str(record.get("id", "-")),
        str(record.get("kind", "-")),
        str(labels.get("status", "-")),
        str(labels.get("stable_id", "-")),
        str(record.get("digest", "-")),
    ])


HEADER = "\t".join(["id", "kind", "status", "stable_id", "digest"])


def main(argv=None):
    configure_utf8_output()
    args = build_parser().parse_args(argv)

    try:
        records, malformed = load_records(args.index_path)
    except FileNotFoundError:
        print("error: index 파일을 찾을 수 없습니다: {p}".format(p=args.index_path),
              file=sys.stderr)
        return EXIT_INPUT_ERROR
    except IsADirectoryError:
        print("error: index 경로가 디렉터리입니다(파일이 아님): {p}".format(p=args.index_path),
              file=sys.stderr)
        return EXIT_INPUT_ERROR
    except OSError as exc:
        print("error: index 파일을 읽을 수 없습니다: {p} ({e})".format(p=args.index_path, e=exc),
              file=sys.stderr)
        return EXIT_INPUT_ERROR

    matched = [r for r in records
               if record_matches(r, args.status, args.kind, args.stable_id)]

    if matched:
        print(HEADER)
        for record in matched:
            print(render_record(record))
    # 0 매칭도 오류가 아니다 — 빈 결과 + matched: 0, exit 0 (명세 §1.2).
    print("matched: {n}".format(n=len(matched)))
    if malformed:
        print("skipped (malformed lines): {n}".format(n=malformed), file=sys.stderr)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
