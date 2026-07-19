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
  designElements:                                           # (선택·Visual Contract 트랙) 디자인 필수 요소.
    appliesWhen: touchpoint                                 #   접점 선언 시에만 적용(미선언 → 비적용).
    projectScope: [ {id, name}, ... ]                       #   프로젝트 단위 1회 요소.
    screenScope:  [ {id, name}, ... ]                       #   각 화면이 커버할 요소.
    exclusionRule: { silentOmission }                       #   요소 제외 = reason+confirmedBy(산출물 동형).
    # 하위호환: 이 섹션이 없으면 designElements 검사는 전혀 수행되지 않는다(구 정책 거동 바이트 동일).

매니페스트 스키마(design-manifest.json — schema 정본: design-manifest.schema.md):
  {
    "declaredTouchpoints": [ ... ],   # 접점(웹·앱·포털) 선언. 비공집합 → touchpoint 클래스 required.
    "declaredInterfaces":  [ ... ],   # 외부 연계 선언. 비공집합 → interface 클래스 required.
    "classExclusions": {              # 클래스 전체 제외 확인(고임팩트 이탈 표면화·원칙 11 (c)).
      "touchpoint": {"reason","confirmedBy"},   # 접점 미선언으로 touchpoint 클래스 전체 제외 시 필수.
      "interface":  {"reason","confirmedBy"}     # 연계 미선언으로 interface 클래스 전체 제외 시 필수.
    },
    "artifacts": [ {"id","status","path"?,"reason"?,"confirmedBy"?}, ... ],
    "designElements": {               # (선택·Visual Contract) 정책 designElements 활성 시 검사 대상.
      "project": { "<elementId>": {"status":"covered","pointer"?} | {"status":"excluded","reason","confirmedBy"} },
      "screens": { "<screenId>": { "<elementId>": <동일 형태> } }   # 비공집합 필수(접점 선언 시).
    }
  }
  status ∈ {produced, excluded}. produced=산출(선택 path 존재검사). excluded=정당화 제외
  (reason 비공백 AND confirmedBy 존재 필수 — 아니면 요건 미충족 오류).
  designElements(요소) status ∈ {covered, excluded}. 체커는 **선언 완전성만** 결정적 판정한다 —
  covered 의 진위(실제 커버 여부)·screens 키와 실제 화면목록의 대응 진위는 내용 파싱 없이는 불가하므로
  CP2/사용자 게이트(mock 리뷰) 몫이다. excluded 는 reason 비공백 AND confirmedBy 필수.

required 판정(requirementClasses):
  - always     : 항상 required.
  - touchpoint : declaredTouchpoints 비공집합일 때만 required. 미선언 시 정책에 touchpoint 항목이
                 있으면 클래스 전체 제외이므로 classExclusions.touchpoint{reason,confirmedBy} 확인 필요
                 (없으면 차단 — 조용한 자동 N/A 폐기·고임팩트 이탈 표면화·silentOmission 금지).
  - interface  : declaredInterfaces 비공집합일 때만 required. 미선언 시 정책에 interface 항목이
                 있으면 클래스 전체 제외이므로 classExclusions.interface{reason,confirmedBy} 확인 필요
                 (없으면 차단 — 위와 동형).

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
_STATUS_COVERED = "covered"  # designElements 요소 커버 상태(artifacts 의 produced 에 대응).


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


def _reason_confirmed_ok(obj) -> tuple[bool, list]:
    """정당화 제외 요건(reason 비공백 AND confirmedBy 존재) 판정 — (ok, 누락항목목록) 반환.

    개별 artifact 의 excluded 블록과 클래스 제외(classExclusions)가 동일 규칙을 공유한다.
    """
    reason = obj.get("reason") if isinstance(obj, dict) else None
    confirmed = obj.get("confirmedBy") if isinstance(obj, dict) else None
    reason_ok = isinstance(reason, str) and bool(reason.strip())
    confirmed_ok = bool(confirmed) and (not isinstance(confirmed, str) or bool(confirmed.strip()))
    miss: list = []
    if not reason_ok:
        miss.append("reason(비공백)")
    if not confirmed_ok:
        miss.append("confirmedBy")
    return (reason_ok and confirmed_ok), miss


def _is_required(requirement: str, has_touchpoint: bool, has_interface: bool) -> bool:
    """requirementClasses 규칙으로 required 여부 판정."""
    if requirement == _ALWAYS:
        return True
    if requirement == _TOUCHPOINT:
        return has_touchpoint
    if requirement == _INTERFACE:
        return has_interface
    return False  # 알 수 없는 클래스 — 상류에서 이미 오류 처리됨(도달 시 스킵).


# --- designElements(Visual Contract 트랙) — 디자인 필수 요소 선언 완전성 결정적 판정 ------------
def _load_design_elements_policy(policy_path: Path) -> tuple:
    """정책에서 designElements 섹션을 파싱한다. (섹션 dict 또는 None, 오류목록) 반환.

    섹션 부재 → (None, []) : designElements 검사 전면 비적용(하위호환 — 구 정책 거동 바이트 동일).
    _load_policy_required 가 이미 정책 파싱에 성공한 뒤에만 호출된다(같은 파일 재판독·결정적·순수).
    """
    try:
        import yaml  # 로컬 라이브러리(네트워크 0).
    except ImportError:
        return None, ["PyYAML 미설치 — 정책 파싱 불가(로컬 라이브러리 필요)"]
    try:
        doc = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:  # type: ignore[attr-defined]
        return None, ["정책 파싱 실패(%s): %s" % (policy_path, exc)]
    if not isinstance(doc, dict):
        return None, []  # 상류(_load_policy_required)에서 이미 오류 처리된 케이스.
    de = doc.get("designElements")
    if de is None:
        return None, []  # 섹션 부재 → 비적용.
    if not isinstance(de, dict):
        return None, ["designElements 가 매핑(dict)이 아니다: %r" % (de,)]
    return de, []


def _element_scope(section: dict, key: str, errors: list) -> list:
    """designElements 의 projectScope/screenScope 를 [{id,name}] 로 파싱(오류는 errors 에 append)."""
    lst = section.get(key)
    if lst is None:
        return []  # 스코프 미정의 → 요구 요소 없음.
    if not isinstance(lst, list):
        errors.append("designElements.%s 가 목록이 아니다: %r" % (key, lst))
        return []
    out: list = []
    for i, e in enumerate(lst):
        if not isinstance(e, dict):
            errors.append("designElements.%s[%d] 가 매핑이 아니다: %r" % (key, i, e))
            continue
        eid = e.get("id")
        if not isinstance(eid, str) or not eid.strip():
            errors.append("designElements.%s[%d].id 가 비어 있지 않은 문자열이 아니다: %r" % (key, i, eid))
            continue
        out.append({"id": eid, "name": e.get("name") or eid})
    return out


def _check_element(scope_label: str, screen_id, element: dict, entry, errors: list) -> None:
    """단일 요소의 선언 완전성 판정 — covered/정당화 excluded 만 통과. 미선언·기타 = 침묵 누락.

    선언 완전성만 판정한다(covered 의 진위는 CP2/사용자 게이트 몫). excluded 는 reason+confirmedBy 필수.
    """
    where = ("화면 '%s' × " % screen_id) if screen_id is not None else ""
    eid = element["id"]
    ename = element["name"]
    if entry is None:
        errors.append(
            "침묵 누락 — %s%s 요소 '%s'(id=%s) 이 covered 도 정당화 excluded 도 되지 않음"
            "(designElements silentOmission 금지)" % (where, scope_label, ename, eid)
        )
        return
    if not isinstance(entry, dict):
        errors.append(
            "%s%s 요소 '%s'(id=%s) 항목이 매핑이 아니다: %r" % (where, scope_label, ename, eid, entry)
        )
        return
    status = entry.get("status")
    if status == _STATUS_COVERED:
        return  # 선언 완전성 충족(진위는 게이트 몫).
    if status == _STATUS_EXCLUDED:
        ok, miss = _reason_confirmed_ok(entry)
        if not ok:
            errors.append(
                "정당화 제외 요건 미충족 — %s%s 요소 '%s'(id=%s) status=excluded 이나 %s 누락"
                % (where, scope_label, ename, eid, "·".join(miss))
            )
        return
    errors.append(
        "침묵 누락 — %s%s 요소 '%s'(id=%s) status 가 covered/excluded 가 아님: %r"
        % (where, scope_label, ename, eid, status)
    )


def _check_design_elements(de_policy: dict, manifest: dict, errors: list) -> None:
    """활성 조건 충족(접점 선언 + 정책 designElements 존재) 시 디자인 필수 요소 선언 완전성 검사.

    (a) projectScope 전 요소 선언 완전성 · (b) screens 공집합이면 오류 · (c) 각 화면 × screenScope
    전 요소 완전성 · (d) excluded 는 reason+confirmedBy 필수 · (e) 미선언 요소 = silentOmission 오류.
    오류는 입력 순서(projectScope → 화면(매니페스트 순서) × screenScope)로 errors 에 append(결정적).
    """
    project_scope = _element_scope(de_policy, "projectScope", errors)
    screen_scope = _element_scope(de_policy, "screenScope", errors)

    de_manifest = manifest.get("designElements")
    if not isinstance(de_manifest, dict):
        errors.append(
            "접점 선언 + designElements 정책 활성인데 매니페스트 designElements 매핑 부재/비매핑: %r"
            "(silentOmission 금지)" % (de_manifest,)
        )
        de_manifest = {}

    proj_m = de_manifest.get("project")
    if proj_m is None:
        proj_m = {}
    elif not isinstance(proj_m, dict):
        errors.append("designElements.project 가 매핑(dict)이 아니다: %r" % (proj_m,))
        proj_m = {}

    screens_m = de_manifest.get("screens")
    if not isinstance(screens_m, dict) or not screens_m:
        # (b) screens 공집합/부재 → 오류.
        errors.append(
            "접점 선언인데 designElements.screens 가 비어 있음 — 최소 1개 화면의 요소 선언 필요"
            "(silentOmission 금지)"
        )
        screens_m = screens_m if isinstance(screens_m, dict) else {}

    # (a) projectScope 완전성(정책 정의 순서 보존).
    for el in project_scope:
        _check_element("project", None, el, proj_m.get(el["id"]), errors)

    # (c) 각 화면 × screenScope 완전성(매니페스트 화면 삽입 순서 보존 — json.loads 가 순서 유지·결정적).
    for sid, smap in screens_m.items():
        if not isinstance(smap, dict):
            errors.append("designElements.screens[%s] 가 매핑(dict)이 아니다: %r" % (sid, smap))
            continue
        for el in screen_scope:
            _check_element("screen", sid, el, smap.get(el["id"]), errors)


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
      6) touchpoint/interface 클래스가 미선언으로 전체 제외될 때(정책에 해당 클래스 항목이 있는데
         미트리거): 조용한 자동 N/A 대신 매니페스트 classExclusions.<class>{reason,confirmedBy}
         확인을 요구한다(없으면 차단 — 고임팩트 이탈 표면화·원칙 11 (c)·silentOmission 금지).
         클래스가 선언(트리거)되면 6은 적용 안 되고 per-item(5)이 적용된다.
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
    class_exclusions = manifest.get("classExclusions")

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
    # classExclusions 방어적 파싱(없으면 빈 dict, dict 아니면 오류 표면화).
    if class_exclusions is None:
        class_exclusions = {}
    elif not isinstance(class_exclusions, dict):
        errors.append("classExclusions 가 매핑(dict)이 아니다: %r" % (class_exclusions,))
        class_exclusions = {}

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

    # (6) 클래스 전체 제외 표면화 — 고정 순서(touchpoint→interface)로 결정적으로 검사·append.
    #     정책에 클래스 C 항목이 있는데 C 가 미트리거(미선언)면 조용한 자동 N/A 대신
    #     classExclusions.C{reason,confirmedBy} 확인을 요구한다(원칙 11 (c)·silentOmission 금지).
    _class_labels = {_TOUCHPOINT: "접점", _INTERFACE: "연계"}
    for cls, triggered in ((_TOUCHPOINT, has_touchpoint), (_INTERFACE, has_interface)):
        class_ids = [it["id"] for it in required_items if it["requirement"] == cls]
        if not class_ids:
            continue  # 정책에 해당 클래스 항목 없음 — 요구 안 함.
        if triggered:
            continue  # 클래스 선언(트리거)됨 — per-item(5) 로 검사.
        # 미선언 → 클래스 전체 제외. classExclusions.<cls> 확인 필요.
        excl = class_exclusions.get(cls)
        if not isinstance(excl, dict):
            errors.append(
                "%s 미선언으로 %s 클래스 전체 제외(%s) — 사유+사용자 확인"
                "(classExclusions.%s {reason,confirmedBy}) 필요"
                "(고임팩트 이탈 표면화·원칙 11 (c)·silentOmission 금지)"
                % (_class_labels[cls], cls, "·".join(class_ids), cls)
            )
            continue
        ok, miss = _reason_confirmed_ok(excl)
        if not ok:
            errors.append(
                "%s 미선언으로 %s 클래스 전체 제외(%s) — classExclusions.%s 요건 미충족: %s 누락"
                "(고임팩트 이탈 표면화·원칙 11 (c)·silentOmission 금지)"
                % (_class_labels[cls], cls, "·".join(class_ids), cls, "·".join(miss))
            )

    # (4)(5) required 판정 + 산출/정당화 제외 검사(defaultRequiredSet 입력 순서 보존).
    for item in required_items:
        rid = item["id"]
        name = item["name"]
        req = item["requirement"]
        if not _is_required(req, has_touchpoint, has_interface):
            continue  # 미트리거 클래스 — 클래스 제외(6)에서 이미 표면화 검사됨. per-item 스킵.

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
            ok, miss = _reason_confirmed_ok(art)
            if not ok:
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

    # (7) designElements(Visual Contract) 디자인 필수 요소 검사 — 정책에 섹션 존재 + 접점 선언 시에만.
    #     하위호환: 섹션 부재 → 아래 블록 전면 스킵(구 정책·구 매니페스트 조합 거동 바이트 동일).
    #     접점 미선언 → 비적용(appliesWhen=touchpoint · classExclusions 경로가 표면화 담당·(6)에서 처리).
    de_policy, de_errors = _load_design_elements_policy(policy_path)
    if de_errors:
        errors.extend(de_errors)
    elif de_policy is not None:
        applies = de_policy.get("appliesWhen", _TOUCHPOINT)
        active = (applies == _ALWAYS) or has_touchpoint  # 기본 touchpoint → 접점 선언 시 활성.
        if active:
            _check_design_elements(de_policy, manifest, errors)

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
