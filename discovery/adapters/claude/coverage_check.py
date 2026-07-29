#!/usr/bin/env python3
"""coverage_check — Discovery 커버리지(축 4) 결정적 게이트 체커 (form-B·LLM 0·오프라인 안전).

무엇을 하는가:
  Discovery Policy 데이터(`coverage.requiredAxes`)가 선언한 **필수 질문 축 집합**이, 그 run 의
  Coverage 원장(`coverage-ledger.json`)에서 실제로 심문됐거나(`interrogated` + 사용자 진술 근거)
  **정당화 제외**(`excluded` + reason + confirmedBy)됐는지를 결정적으로 판정한다. 축을 조용히
  지나친 것(원장 부재·항목 부재·`unasked`·요건 미충족 제외·추론/가정 충족)은 모두 **미심문**으로
  계수해 표면화한다 — 02 §3.7 축 4(Coverage)·DISC-INV-10(침묵 생략 금지)의 실행 코드 물리화다.

계약 정본:
  - 판정 규칙·상태 어휘·필드 의미 = `discovery/adapters/claude/coverage-ledger.schema.md`
    (「판정 규칙」 표가 이 파일의 구현 계약이다 — 이 코드는 규칙을 창설하지 않는다).
  - 축 실값(id·label·dimension·highImpact) = Discovery Policy 데이터 단독 소유
    (`uahf/framework/adapters/claude/discovery-data/policy/<ref>-policy.yaml`). 구성 요건 정본 문면 =
    `discovery/adapters/claude/discovery-binding.md` §8.2 (마)·§8.3 (a) ref 해소 규약.
  - 축 id·라벨의 **사본을 이 파일에 두지 않는다**(DISC-INV-7·UAF-INV ⑥ — Strategy Provider 마다
    축 집합이 다를 수 있다). 축 집합은 전량 정책 데이터에서 읽는다.

소유 경계:
  - 인터뷰 수행 측이 원장을 **산출**한다. 이 체커는 **검증**만 한다(schema.md §소유 경계).
  - 이 스크립트는 discovery/adapters/claude/ 어댑터 경계 소속이다. 프레임워크 코어를 수정·재정의·
    import 하지 않는다. 선례 = `orchestration/adapters/claude/design_completeness.py`(동일 성격).
  - **선언 완전성만** 판정한다 — `interrogated` 로 선언된 축이 실제로 실질 심문을 받았는지,
    `reason` 이 타당한지의 진위는 내용 판정이므로 사용자 승인 게이트(축 3)·CP2 몫이다.

fail-closed 불변(핵심):
  원장 파일 부재 · 원장 JSON 판독 실패 · 정책 판독 실패 · 정책 `coverage` 절 부재는 **통과가 아니다**.
  축 4 판정이 미확정인 상태이며, 미확정을 통과로 처리하면 이 축이 막으려는 침묵 생략을 그대로
  재생산한다(schema.md 「판정 불가는 통과가 아니다」·이진 상태 원칙). 부재를 "제외 0·미심문 0"으로
  해석하는 경로는 이 파일에 0건이다.
  이 체커는 fail-closed 다 — PreToolUse 훅(fail-open)과 경계가 다르다. 유일한 best-effort 예외는
  콘솔 인코딩 설정이며(아래), 그것은 판정에 관여하지 않는다(design_completeness 와 동형 분할).

오프라인 안전(불변):
  - 네트워크·빌드 0. 파일 판독·구조 검사만.
  - 결정성: 같은 정책·같은 원장 → 같은 오류 목록(정책 축 순서 → 원장 항목 순서 보존).
  - PyYAML(로컬 라이브러리)만 외부 의존 — 부재 시 명확히 실패한다(추측·우회 금지).
  - 순수 판독: 정책·원장을 일절 수정·생성하지 않는다.

종료 코드(design_completeness.py 관례 동형):
  0 = 통과(오류 목록 공집합 — 정책 전 축이 심문됨 또는 정당화 제외됨).
  2 = 실패(미심문·요건 미충족·미상응·판정 불가 오류 존재) — stderr 열거 후 비영 종료(차단 근거).
  2 = 사용법 오류(인자 수)도 동일 계열 비영 종료.

사용법:
  python coverage_check.py <policy.yaml> <coverage-ledger.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(비ASCII stderr) — design_completeness 선례 동형 -------------------
# 판정에 관여하지 않는 best-effort 구간이다(여기서만 예외를 삼킨다).
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

# 상태 어휘(schema.md §상태 어휘 3값 — 축 실값이 아니라 형식 계약의 기계 값).
_STATUS_INTERROGATED = "interrogated"
_STATUS_EXCLUDED = "excluded"
_STATUS_UNASKED = "unasked"
_KNOWN_STATUS = (_STATUS_INTERROGATED, _STATUS_EXCLUDED, _STATUS_UNASKED)

# 근거 등급 어휘(schema.md §스키마 evidenceGrade — 02 §3.12 사용자 진술 > 추론 > 가정).
_GRADE_USER_STATED = "user-stated"
_GRADE_INFERRED = "inferred"
_GRADE_ASSUMED = "assumed"
_KNOWN_GRADES = (_GRADE_USER_STATED, _GRADE_INFERRED, _GRADE_ASSUMED)
# 심문됨의 근거가 되지 못하는 등급 — 미심문으로 계수(02 §3.7 축 4 "추론 충족 불가").
_NON_SATISFYING_GRADES = (_GRADE_INFERRED, _GRADE_ASSUMED)


def _nonblank_str(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _present(v) -> bool:
    """'존재' 요건 — 값이 있고, 문자열이면 공백만이 아니어야 한다(design_completeness 동형)."""
    return bool(v) and (not isinstance(v, str) or bool(v.strip()))


def load_policy_axes(policy_path) -> tuple:
    """정책에서 coverage.requiredAxes 를 파싱한다. (축목록, 오류목록) 반환.

    축목록 원소 = {"id", "label", "highImpact"}. 정책 선언 순서를 보존한다(결정성).
    부재·PyYAML 부재·파싱 실패·`coverage` 절 부재는 **판정 불가 = 차단**으로 표면화한다.
    `highImpact` 가 bool 로 선언되지 않으면 오류다 — 결여를 false 로 관대 해석하면 highImpact 축의
    즉시 표면화(surfacedAt) 요건이 조용히 사라진다(침묵 생략 재생산).
    """
    policy_path = Path(policy_path)
    if not policy_path.exists():
        return [], ["Discovery Policy 부재 — 커버리지 축 집합 판정 불가(차단): %s" % policy_path]
    try:
        import yaml  # 로컬 라이브러리(네트워크 0). 부재 시 명확히 실패.
    except ImportError:
        return [], ["PyYAML 미설치 — 정책 파싱 불가(로컬 라이브러리 필요·설치 후 재시도)"]
    try:
        doc = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:  # type: ignore[attr-defined]
        return [], ["정책 파싱 실패(%s): %s — 커버리지 판정 불가(차단)" % (policy_path, exc)]

    if not isinstance(doc, dict):
        return [], ["정책 최상위가 매핑(dict)이 아니다: %s" % type(doc).__name__]
    cov = doc.get("coverage")
    if cov is None:
        return [], [
            "정책에 coverage 절이 없다 — 필수 질문 축 집합 미선언(판정 불가는 통과가 아니다·"
            "discovery-binding §8.2 (마)): %s" % policy_path
        ]
    if not isinstance(cov, dict):
        return [], ["정책 coverage 가 매핑(dict)이 아니다: %r" % (cov,)]
    required = cov.get("requiredAxes")
    if not isinstance(required, list) or not required:
        return [], ["정책 coverage.requiredAxes 가 비어 있지 않은 목록이 아니다: %r" % (required,)]

    axes: list = []
    errors: list = []
    seen: set = set()
    for i, entry in enumerate(required):
        if not isinstance(entry, dict):
            errors.append("coverage.requiredAxes[%d] 가 매핑이 아니다: %r" % (i, entry))
            continue
        aid = entry.get("id")
        if not _nonblank_str(aid):
            errors.append(
                "coverage.requiredAxes[%d].id 가 비어 있지 않은 문자열이 아니다: %r" % (i, aid)
            )
            continue
        if aid in seen:
            errors.append("coverage.requiredAxes 축 id 중복 선언: %r" % (aid,))
            continue
        high = entry.get("highImpact")
        if not isinstance(high, bool):
            errors.append(
                "coverage.requiredAxes[%d](id=%s).highImpact 가 bool 로 선언되지 않았다: %r "
                "— 고임팩트 여부 미확정(즉시 표면화 요건 판정 불가·차단)" % (i, aid, high)
            )
            continue
        seen.add(aid)
        label = entry.get("label")
        axes.append({"id": aid, "label": label if _nonblank_str(label) else aid,
                     "highImpact": high})
    return axes, errors


def load_ledger(ledger_path) -> tuple:
    """Coverage 원장을 판독한다. (axes 목록, 오류목록) 반환.

    부재·판독 실패·JSON 손상·구조 위반은 **판정 불가 = 차단**이다(schema.md §원장 부재 —
    부재를 "제외 0·미심문 0"으로 해석하지 않는다).
    """
    ledger_path = Path(ledger_path)
    if not ledger_path.exists():
        return [], [
            "Coverage 원장 부재 — 축 4 미확정(판정 불가는 통과가 아니다·DISC-INV-10): %s"
            % ledger_path
        ]
    try:
        doc = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [], ["Coverage 원장 판독 실패(%s): %s — 축 4 판정 불가(차단)" % (ledger_path, exc)]
    if not isinstance(doc, dict):
        return [], ["Coverage 원장 최상위가 매핑(dict)이 아니다: %s" % type(doc).__name__]
    axes = doc.get("axes")
    if not isinstance(axes, list):
        return [], [
            "Coverage 원장 axes 가 목록이 아니다: %r — 축 상태 판정 불가(차단)" % (axes,)
        ]
    return axes, []


def _check_axis_entry(axis: dict, entry: dict, errors: list) -> None:
    """정책 축 1건에 대응하는 원장 항목 1건의 상태 요건 판정(schema.md 판정 규칙 표 2~5행)."""
    aid = axis["id"]
    label = axis["label"]
    where = "축 '%s'(id=%s)" % (label, aid)
    status = entry.get("status")

    if status == _STATUS_INTERROGATED:
        grade = entry.get("evidenceGrade")
        if grade in _NON_SATISFYING_GRADES:
            errors.append(
                "미심문 계수 — %s status=interrogated 이나 evidenceGrade=%r 는 심문됨의 근거가 "
                "되지 못한다(02 §3.7 축 4 추론 충족 불가)" % (where, grade)
            )
            return
        if grade not in _KNOWN_GRADES:
            errors.append(
                "미심문 계수 — %s status=interrogated 이나 evidenceGrade 가 어휘 %s 중 하나가 "
                "아니다: %r(근거 등급 미확정은 통과가 아니다)"
                % (where, "{%s}" % ", ".join(_KNOWN_GRADES), grade)
            )
            return
        return  # user-stated — 선언 완전성 충족(진위는 게이트 몫).

    if status == _STATUS_EXCLUDED:
        miss = []
        if not _nonblank_str(entry.get("reason")):
            miss.append("reason(비공백)")
        if not _present(entry.get("confirmedBy")):
            miss.append("confirmedBy")
        if miss:
            errors.append(
                "미심문 계수 — %s status=excluded 이나 %s 누락 — 제외로 성립하지 않는다"
                "(coverage.exclusionRule.requiredFields)" % (where, "·".join(miss))
            )
        if axis["highImpact"] and not _present(entry.get("surfacedAt")):
            errors.append(
                "즉시 표면화 기록 부재 — %s 는 highImpact 축인데 status=excluded 이면서 "
                "surfacedAt 이 없다(원칙 11 (c) 미이행·승인 게이트까지 미룰 수 없다)" % where
            )
        return

    if status == _STATUS_UNASKED:
        errors.append(
            "미심문 — %s status=unasked(축 4 미충족 — Ready·ReadyWithAssumptions 어느 종단에도 "
            "도달하지 못한다)" % where
        )
        return

    errors.append(
        "미심문 계수 — %s status 가 어휘 %s 중 하나가 아니다: %r(침묵 생략 금지·DISC-INV-10)"
        % (where, "{%s}" % ", ".join(_KNOWN_STATUS), status)
    )


def check_coverage(policy_path, ledger_path) -> list:
    """커버리지(축 4) 게이트 — 오류 목록 반환(빈 목록 = 통과). 순수 함수·결정적·오프라인.

    로직(schema.md 「판정 규칙」 표의 구현):
      1) 정책 coverage.requiredAxes 파싱 — 부재·판독 실패·절 부재는 차단(fail-closed).
      2) 원장 판독 — 부재·손상·구조 위반은 차단(fail-closed).
      3) 정책 축마다 원장 항목 조회(정책 선언 순서 보존):
         - 0건 → 미심문과 동치(침묵 생략 금지).
         - 2건 이상 → 중복 위반(schema.md 는 "1건씩"을 요구한다). 상태 판정은 수행하지 않는다.
         - 1건 → 상태 요건 판정(_check_axis_entry).
      4) 원장에만 있는 id → 미상응 위반(정책이 축 집합의 단일 소유자이므로 원장은 축을 창설 못 한다).
    """
    axes_policy, policy_errors = load_policy_axes(policy_path)
    if policy_errors:
        return policy_errors  # 축 집합 자체가 미확정 — 대조 이전에 차단.

    ledger_axes, ledger_errors = load_ledger(ledger_path)
    if ledger_errors:
        return ledger_errors  # 원장 미확정 — 대조 이전에 차단.

    errors: list = []

    # 원장 항목 색인(id → 항목 목록). 항목 구조 위반은 그 자리에서 표면화한다.
    by_id: dict = {}
    for i, e in enumerate(ledger_axes):
        if not isinstance(e, dict):
            errors.append("원장 axes[%d] 가 매핑(dict)이 아니다: %r" % (i, e))
            continue
        eid = e.get("id")
        if not _nonblank_str(eid):
            errors.append("원장 axes[%d].id 가 비어 있지 않은 문자열이 아니다: %r" % (i, eid))
            continue
        by_id.setdefault(eid, []).append(e)

    # (3) 정책 축 순서로 대조.
    for axis in axes_policy:
        aid = axis["id"]
        label = axis["label"]
        found = by_id.get(aid)
        if not found:
            errors.append(
                "미심문 — 축 '%s'(id=%s) 이 원장 axes 에 없다(원장에 없는 축 = 미심문과 동치·"
                "침묵 생략 금지·DISC-INV-10)" % (label, aid)
            )
            continue
        if len(found) > 1:
            errors.append(
                "원장 축 id 중복 — 축 '%s'(id=%s) 항목이 %d 건(스키마는 정책 축마다 1건씩을 "
                "요구한다 — 어느 항목이 정본인지 미확정이므로 상태 판정 불가·차단)"
                % (label, aid, len(found))
            )
            continue
        _check_axis_entry(axis, found[0], errors)

    # (4) 미상응 항목 — 원장 등장 순서 보존.
    policy_ids = {a["id"] for a in axes_policy}
    for eid in by_id:
        if eid not in policy_ids:
            errors.append(
                "미상응 항목 — 원장 axes 의 id=%s 가 정책 coverage.requiredAxes 에 없다"
                "(정책이 축 집합의 단일 소유자 — 원장은 축을 창설하지 못한다)" % eid
            )

    return errors


def main(argv) -> int:
    if len(argv) != 2:
        print(
            "사용법 오류: python coverage_check.py <policy.yaml> <coverage-ledger.json>",
            file=sys.stderr,
        )
        return 2
    errors = check_coverage(argv[0], argv[1])
    if errors:
        print(
            "[COVERAGE-INCOMPLETE] 커버리지(축 4) 게이트 차단 — 미심문 축(심문 또는 정당화 제외 필요):",
            file=sys.stderr,
        )
        for e in errors:
            print("  - %s" % e, file=sys.stderr)
        return 2
    print("[COVERAGE-COMPLETE] 정책 필수 질문 축 전부가 심문됨 또는 정당화 제외됨(게이트 통과).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
