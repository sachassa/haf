#!/usr/bin/env python3
"""design_completeness — 설계완성도 결정적 게이트 체커 (§DC-1 Wave 3·form-B·LLM 0·오프라인 안전).

무엇을 하는가:
  Solution Design 정책(projectionSelection.defaultRequiredSet·requirementClasses·exclusionRule)이
  선언한 **기본 필수 산출물 세트**가, 소비 프로젝트의 설계 매니페스트(design-manifest.json)에서
  실제로 산출(produced)됐거나 **정당화 제외(excluded + reason + confirmedBy)** 됐는지를 결정적으로
  판정한다. 산출도 정당화 제외도 없는 **침묵 누락**(silentOmission)을 오류로 표면화해, impl 단위가
  그래프에 편입되기 직전(resolve_gate.resolve_structural 의 task_added 승격 직전) 차단한다.

  이는 04-solution-design SP-INV 9(침묵 누락 금지·기본 필수 세트)의 실행 코드 물리화이며,
  verify_checks.py(VT-1/VT-4 form-B) 와 동형의 결정적 슬라이스다 — verdict(통과/실패의 최종 승인)는
  내지 않고, "누락 산출물 목록"이라는 결정적·재현 가능한 근거만 방출한다. 최종 게이트 판정·승인은
  엔진(resolve_gate)·Advisor(CP3) 몫이다.

소유 경계:
  - Solution Design 이 **산출**한다(design-manifest.json 을 워크스페이스 SD 데이터에 배치).
  - 오케스트레이션(이 체커·resolve_gate)이 **검증**한다(편입 직전 게이트).
  이 스크립트는 orchestration/adapters/claude/ 어댑터 경계 소속이다. 프레임워크 코어
  (uahf/framework/**·orchestration/framework/**)를 수정·재정의하지 않는다(import 도 하지 않는다).

정책 스키마(소비 = uahf/.../solution-design-data/policy/default-policy.yaml → 워크스페이스로 시드):
  projectionSelection:
    defaultRequiredSet: [ {id, name, requirement}, ... ]   # requirement ∈ {always,touchpoint,interface}
    requirementClasses: { always, touchpoint, interface }  # 각 클래스의 default-required 조건(문면)
    exclusionRule: { silentOmission, autoExclude, manualExclude }

매니페스트 스키마(design-manifest.json — schema 정본: design-manifest.schema.md):
  {
    "declaredTouchpoints": [ ... ],   # 접점(웹·앱·포털) 선언. 비공집합 → touchpoint 클래스 required.
    "declaredInterfaces":  [ ... ],   # 외부 연계 선언. 비공집합 → interface 클래스 required.
    "artifacts": [ {"id","status","path"?,"reason"?,"confirmedBy"?}, ... ]
  }
  status ∈ {produced, excluded}. produced=산출(선택 path 존재검사). excluded=정당화 제외
  (reason 비공백 AND confirmedBy 존재 필수 — 아니면 요건 미충족 오류).

required 판정(requirementClasses):
  - always     : 항상 required.
  - touchpoint : declaredTouchpoints 비공집합일 때만 required(미선언 → 자동 N/A·스킵).
  - interface  : declaredInterfaces 비공집합일 때만 required(미연계 → 자동 N/A·스킵).

오프라인 안전(불변):
  - 네트워크·npm·npx·tsc·빌드 0. 파일 판독·구조 검사만.
  - 결정성: 같은 정책·같은 매니페스트·같은 파일시스템 → 같은 오류 목록(입력 순서 보존).
  - PyYAML(로컬 라이브러리)만 외부 의존 — 부재 시 명확히 실패한다(추측·우회 금지).
  - 순수 판독: 매니페스트·정책·산출물을 일절 수정하지 않는다.

종료 코드(verify_checks.py 관례 동형):
  0 = 통과(오류 목록 공집합 — 모든 required 산출물이 산출 또는 정당화 제외됨).
  2 = 실패(누락·요건 미충족 오류 존재) — 오류를 stderr 로 열거 후 비영 종료(게이트 차단 근거).
  2 = 사용법 오류(인자 부족·argparse)도 동일 계열 비영 종료.

사용법:
  python design_completeness.py <policy.yaml> <design-manifest.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(비ASCII stderr) — verify_checks 선례 동형 -----------------------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

# requirement 클래스 → required 판정에 쓰는 선언 필드 이름.
_TOUCHPOINT = "touchpoint"
_INTERFACE = "interface"
_ALWAYS = "always"
_KNOWN_CLASSES = (_ALWAYS, _TOUCHPOINT, _INTERFACE)

_STATUS_PRODUCED = "produced"
_STATUS_EXCLUDED = "excluded"


def _load_policy_required(policy_path: Path) -> tuple[list, list]:
    """정책에서 defaultRequiredSet 을 파싱한다. (항목목록, 오류목록) 반환.

    PyYAML 부재·파싱 실패·스키마 부재는 오류로 표면화한다(추측·우회 금지).
    """
    if not policy_path.exists():
        return [], ["design policy 부재 — 필수 산출물 세트 판정 불가: %s" % policy_path]
    try:
        import yaml  # 로컬 라이브러리(네트워크 0). 부재 시 명확히 실패.
    except ImportError:
        return [], ["PyYAML 미설치 — 정책 파싱 불가(로컬 라이브러리 필요·설치 후 재시도)"]
    try:
        doc = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:  # type: ignore[attr-defined]
        return [], ["정책 파싱 실패(%s): %s" % (policy_path, exc)]

    if not isinstance(doc, dict):
        return [], ["정책 최상위가 매핑(dict)이 아니다: %s" % type(doc).__name__]
    proj = doc.get("projectionSelection")
    if not isinstance(proj, dict):
        return [], ["정책에 projectionSelection 매핑이 없다(스키마 위반)"]
    required_set = proj.get("defaultRequiredSet")
    if not isinstance(required_set, list) or not required_set:
        return [], ["정책 projectionSelection.defaultRequiredSet 이 비어 있지 않은 목록이 아니다"]

    items: list = []
    errors: list = []
    for i, entry in enumerate(required_set):
        if not isinstance(entry, dict):
            errors.append("defaultRequiredSet[%d] 가 매핑이 아니다: %r" % (i, entry))
            continue
        rid = entry.get("id")
        req = entry.get("requirement")
        name = entry.get("name") or rid
        if not isinstance(rid, str) or not rid.strip():
            errors.append("defaultRequiredSet[%d] id 가 비어 있지 않은 문자열이 아니다: %r" % (i, rid))
            continue
        if req not in _KNOWN_CLASSES:
            errors.append(
                "defaultRequiredSet[%d](id=%r) requirement 이 {always,touchpoint,interface} 중 "
                "하나가 아니다: %r" % (i, rid, req)
            )
            continue
        items.append({"id": rid, "name": name, "requirement": req})
    return items, errors


def _is_required(requirement: str, has_touchpoint: bool, has_interface: bool) -> bool:
    """requirementClasses 규칙으로 required 여부 판정."""
    if requirement == _ALWAYS:
        return True
    if requirement == _TOUCHPOINT:
        return has_touchpoint
    if requirement == _INTERFACE:
        return has_interface
    return False  # 알 수 없는 클래스 — 상류에서 이미 오류 처리됨(도달 시 스킵).


def check_design_completeness(policy_path, manifest_path) -> list:
    """설계완성도 게이트 — 오류 목록 반환(빈 목록 = 통과). 순수 함수·결정적·오프라인.

    로직:
      1) 매니페스트 부재 → 오류(설계 미완 프로젝트 차단의 핵심).
      2) 정책 파싱(defaultRequiredSet·requirementClasses·exclusionRule).
      3) 매니페스트 파싱(declaredTouchpoints·declaredInterfaces·artifacts).
      4) 각 필수 항목 required 판정(always/touchpoint/interface).
      5) required 항목마다 artifacts 조회:
         - produced → 통과(path 주어지면 존재 검사).
         - excluded → reason 비공백 AND confirmedBy 존재해야 통과(정당화 제외).
         - 부재/기타 status → 침묵 누락 오류(silentOmission 금지).
      6) required 아님(touchpoint/interface 미선언) → 자동 N/A·스킵.
    """
    manifest_path = Path(manifest_path)
    policy_path = Path(policy_path)

    # (1) 매니페스트 부재 → 즉시 차단(설계 미완 프로젝트 = manifest 없음).
    if not manifest_path.exists():
        return [
            "design-manifest absent — Solution Design에서 설계 산출 필요: %s" % manifest_path
        ]

    # (2) 정책 파싱.
    required_items, policy_errors = _load_policy_required(policy_path)
    if policy_errors:
        return policy_errors  # 정책 자체가 판정 불가 상태 — 완전성 판정 전에 차단.

    # (3) 매니페스트 파싱.
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ["design-manifest 파싱 실패(%s): %s" % (manifest_path, exc)]
    if not isinstance(manifest, dict):
        return ["design-manifest 최상위가 매핑(dict)이 아니다: %s" % type(manifest).__name__]

    touchpoints = manifest.get("declaredTouchpoints")
    interfaces = manifest.get("declaredInterfaces")
    artifacts = manifest.get("artifacts")

    errors: list = []
    if touchpoints is not None and not isinstance(touchpoints, list):
        errors.append("declaredTouchpoints 가 목록이 아니다: %r" % (touchpoints,))
        touchpoints = []
    if interfaces is not None and not isinstance(interfaces, list):
        errors.append("declaredInterfaces 가 목록이 아니다: %r" % (interfaces,))
        interfaces = []
    if not isinstance(artifacts, list):
        errors.append("artifacts 가 목록이 아니다: %r" % (artifacts,))
        artifacts = []

    has_touchpoint = bool(touchpoints)
    has_interface = bool(interfaces)

    # artifacts id → 항목 매핑(마지막 항목 우선은 결정적이나, 중복 id 는 오류로 표면화).
    by_id: dict = {}
    for a in artifacts:
        if not isinstance(a, dict):
            errors.append("artifacts 항목이 매핑이 아니다: %r" % (a,))
            continue
        aid = a.get("id")
        if not isinstance(aid, str) or not aid.strip():
            errors.append("artifacts 항목 id 가 비어 있지 않은 문자열이 아니다: %r" % (aid,))
            continue
        if aid in by_id:
            errors.append("artifacts 항목 id 중복: %r" % (aid,))
        by_id[aid] = a

    manifest_dir = manifest_path.resolve().parent

    # (4)(5)(6) required 판정 + 산출/정당화 제외 검사(defaultRequiredSet 입력 순서 보존).
    for item in required_items:
        rid = item["id"]
        name = item["name"]
        req = item["requirement"]
        if not _is_required(req, has_touchpoint, has_interface):
            continue  # 자동 N/A(touchpoint/interface 미선언) — 스킵.

        art = by_id.get(rid)
        if art is None:
            errors.append(
                "침묵 누락 — 필수 산출물 '%s'(id=%s·%s) 이 산출도 정당화 제외도 되지 않음"
                "(silentOmission 금지)" % (name, rid, req)
            )
            continue

        status = art.get("status")
        if status == _STATUS_PRODUCED:
            path = art.get("path")
            if isinstance(path, str) and path.strip():
                p = Path(path)
                target = p if p.is_absolute() else (manifest_dir / path)
                if not target.exists():
                    errors.append(
                        "필수 산출물 '%s'(id=%s) status=produced 이나 path 부재: %s"
                        % (name, rid, path)
                    )
            # path 미지정이면 존재 검사 생략(스키마상 선택) — status=produced 만으로 통과.
            continue

        if status == _STATUS_EXCLUDED:
            reason = art.get("reason")
            confirmed = art.get("confirmedBy")
            reason_ok = isinstance(reason, str) and reason.strip()
            confirmed_ok = bool(confirmed) and (
                not isinstance(confirmed, str) or confirmed.strip()
            )
            if not (reason_ok and confirmed_ok):
                miss = []
                if not reason_ok:
                    miss.append("reason(비공백)")
                if not confirmed_ok:
                    miss.append("confirmedBy")
                errors.append(
                    "정당화 제외 요건 미충족 — 필수 산출물 '%s'(id=%s) status=excluded 이나 %s 누락"
                    % (name, rid, "·".join(miss))
                )
            continue

        # status 가 produced/excluded 둘 다 아님 → 침묵 누락과 동급(정당화 없음).
        errors.append(
            "침묵 누락 — 필수 산출물 '%s'(id=%s) status 가 produced/excluded 가 아님: %r"
            % (name, rid, status)
        )

    return errors


def main(argv) -> int:
    if len(argv) != 2:
        print(
            "사용법 오류: python design_completeness.py <policy.yaml> <design-manifest.json>",
            file=sys.stderr,
        )
        return 2
    policy_path, manifest_path = argv
    errors = check_design_completeness(policy_path, manifest_path)
    if errors:
        print(
            "[DESIGN-INCOMPLETE] 설계완성도 게이트 차단 — 누락 산출물(Solution Design에서 산출 또는 "
            "정당화 제외 필요):",
            file=sys.stderr,
        )
        for e in errors:
            print("  - %s" % e, file=sys.stderr)
        return 2
    print("[DESIGN-COMPLETE] 모든 필수 산출물이 산출 또는 정당화 제외됨(게이트 통과).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
