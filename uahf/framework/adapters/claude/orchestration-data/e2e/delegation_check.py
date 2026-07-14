"""delegation 참조형 표준화 검사 — 3면 공유 순수 함수 (T4-①).

시나리오 프롬프트(w_scenario·m_scenario)·검증기(resolve_w.validate_impl_plan·
resolve_m.validate_stage_plan)·결정적 검증 러너(verify_run.py (d))가 **같은 함수**를 공유해
delegation.task/done 의 형태를 판정한다. 규칙 문면을 한 곳(이 모듈)에 두어 3면 정합을
보장한다(미결정성 제거).

계약(02-agent §3.2-B:119 "task: 작업 요약" — spec 개정 불요):
  delegation.task/done 은 **둘 중 하나**이면 유효(pass):
    (1) 참조형 sentinel — 정확히 SENTINEL_TASK / SENTINEL_DONE 문면(권장·토큰 절약).
    (2) 원문 전재 — 상위 Task 의 task/done 필드와 **바이트 동일**.
  그 외(요약·변형·부분 발췌)는 무효(fail) — 명확한 오류 메시지를 낸다.

두 형태 모두 baseline 에 실재한다(m 성숙 stages = 참조형 sentinel · w 구현 tasks·k·j =
원문 전재). 따라서 이 검사는 baseline 4 run 전건을 통과한다(무회귀).

순수 함수(입력만으로 결정·run 데이터 무접촉). Adapter 경계(orchestration-data/e2e/) 소속.
"""

from __future__ import annotations

from typing import Any

# 참조형 sentinel 정확 문면(권장형). m 성숙 run 이 이미 산출한 실측 문면과 동일하게 고정한다.
SENTINEL_TASK = "위 task 필드와 동일"
SENTINEL_DONE = "위 done 필드와 동일"


def _short(value: Any, n: int = 48) -> str:
    """오류 메시지용 축약 repr(비문자열은 타입만)."""
    if isinstance(value, str):
        return repr(value if len(value) <= n else value[:n] + "…")
    return "<%s>" % type(value).__name__


def _field_error(field: str, sentinel: str, top_value: Any, deleg_value: Any, where: str) -> str | None:
    """delegation.<field> 가 sentinel 또는 상위 원문과 동일인지 판정. 위반 시 오류 문자열."""
    if isinstance(deleg_value, str) and (deleg_value.strip() == sentinel or deleg_value == top_value):
        return None
    return (
        "%s delegation.%s 가 참조형 sentinel(%r) 도 상위 %s 원문 전재도 아니다"
        "(요약·변형 금지·둘 중 하나여야 함): %s"
        % (where, field, sentinel, field, _short(deleg_value))
    )


def delegation_reference_errors(
    top_task: Any,
    top_done: Any,
    delegation: Any,
    *,
    where: str = "",
) -> list:
    """delegation.task/done 의 참조형 표준 준수 오류 목록(빈 목록 = 통과).

    delegation 이 dict 가 아니면 그 자체를 오류로 표기한다(상위 검증기가 delegation 존재를
    이미 요구하지만, 이 함수 단독 호출에서도 방어적으로 판정한다).
    """
    if not isinstance(delegation, dict):
        return ["%s delegation 이 객체(dict)가 아니다: %s" % (where, _short(delegation))]
    errors: list = []
    e_task = _field_error("task", SENTINEL_TASK, top_task, delegation.get("task"), where)
    if e_task:
        errors.append(e_task)
    e_done = _field_error("done", SENTINEL_DONE, top_done, delegation.get("done"), where)
    if e_done:
        errors.append(e_done)
    return errors


def delegation_errors_for_task(task: Any, *, where: str = "") -> list:
    """Task/stage dict 하나에 대한 delegation.task/done 참조형 검사(빈 목록 = 통과)."""
    if not isinstance(task, dict):
        return ["%s task 가 객체(dict)가 아니다: %s" % (where, _short(task))]
    return delegation_reference_errors(
        task.get("task"), task.get("done"), task.get("delegation"), where=where
    )
