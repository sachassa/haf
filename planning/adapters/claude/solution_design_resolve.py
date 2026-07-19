#!/usr/bin/env python3
"""solution_design_resolve — 산출물 생산 프로토콜 결정적 로더 (§DC-1 Wave 5-B·form-B·LLM 0·오프라인 안전).

무엇을 하는가:
  Solution Design 정책(roleSelection.defaultComposition·artifactOwnership·
  projectionSelection.defaultRequiredSet·requirementClasses)을 읽어, "어떤 역할을 띄우고,
  각자 어떤 산출물을 소유하며, 접점/연계/데이터복잡 선언에 따라 무엇이 필수인지"를 **결정적으로
  계산**해 구조화 JSON 으로 stdout 에 방출한다. 이는 solution-design-binding.md §7A(산출물 생산
  프로토콜 — form-A 규약)의 **결정적 부분을 form-B 로 물리화**한 것이며, entry_resolve.py(형태 B
  로더)·design_completeness.py(결정적 게이트 체커)와 **동일 성격**이다 — LLM 0·순수 판독·계산해서
  방출까지만.

절대 경계 — 실행 호스팅 0 (04 §3.9 확장 포인트·binding §6.2):
  이 로더는 **계산·방출까지만** 한다. 역할 서브에이전트를 자동 소환·구동하거나 산출물 본문을 자동
  생성하지 않는다 — 그 실행 호스팅(형태 B step 실행기)은 04 §3.9 확장 포인트로 binding §6.2(line 200)
  가 "설계하지 않는다"로 명시 유보했다. 실제 위임(서브에이전트 소환)은 주 세션(Advisor)이 form-A 로
  수행한다(binding §6.1 "기존 위임 관행 재사용"). 이 로더는 subagent 를 spawn 하지 않고 Agent/Task
  API 를 호출하지 않는다 — 그것은 경계 위반이다.

결정적 계산(같은 정책·같은 입력 → 같은 JSON·키/목록 순서 불변):
  ① roleComposition — coverageFloor + baseSpecialists + (whenSignal 기계 매칭으로 활성화된
     conditionalSpecialists). 활성/제외 각각 근거와 함께 방출(deviationRule 이탈 사유기록 후보).
  ② artifactPlan — defaultRequiredSet 각 id 의 owner(artifactOwnership)·requirement·required 판정
     (_is_required 규칙 동형: always=항상·touchpoint=접점선언시·interface=연계선언시).
  ③ manifestScaffold — 채워질 자리(declared*·required=true artifacts status=pending·미선언 클래스
     classExclusions placeholder). status="pending"은 **작업중 placeholder**다 — design_completeness
     체커는 produced/excluded 만 인정하므로, 생산 완료 후 status 가 produced/excluded 로 갱신되어야
     게이트를 통과한다. 이 로더는 뼈대(scaffold)만 제공한다.

하드코딩 금지(SP-INV 5·binding §11.3):
  역할명·산출물 유형 id·요건 클래스를 코드에 하드코딩하지 않는다 — 전부 정책(policy.yaml)에서
  읽는다. 이 로더는 계산 로직만 안다. whenSignal 만이 이 로더가 아는 기계 신호 어휘이며(아래
  KNOWN_SIGNALS), 그마저도 정책이 선언한 whenSignal 을 대조·매칭할 뿐 역할·유형을 하드코딩하지 않는다.

whenSignal 기계 매칭(산문 when 파싱 금지 — 결정성):
  conditionalSpecialists 각 항목의 whenSignal(기계 신호)로만 활성화 판정한다. 사람용 when(산문)은
  파싱하지 않는다. 알 수 없는 whenSignal 은 오류로 표면화한다(결정성·추측 금지).
    - touchpoint  → --touchpoints 비공집합일 때 활성.
    - interface   → --interfaces 비공집합일 때 활성.
    - dataComplex → --data-complex 플래그일 때 활성.
    - regulated   → --regulated 플래그일 때 활성(규제·컴플라이언스 신호).

전문 역할 상한 집행(maxSpecialistRoles·cap·§DC-6):
  base(baseSpecialists) + 활성 조건부(activatedConditional)의 합이 정책 maxSpecialistRoles 를
  초과하면 초과분을 결정적으로 제외한다 — 우선순위 = 정책 conditionalSpecialists **선언 순서**
  (base 역할은 항상 보존·cap 산입, coverageFloor 는 불산입). 제외분은 excludedByCap 로 방출한다.
  cap 값·역할명을 코드에 하드코딩하지 않는다 — 전부 정책에서 읽는다.

오프라인 안전(불변):
  - 네트워크·npm·빌드 0. 파일 판독·구조 계산만.
  - 순수 판독. 정책·워크스페이스를 수정하지 않는다. --out 은 선택 편의이며, 기존 파일이 있으면
    덮어쓰지 않고 오류로 표면화한다(산출은 SD 소관·로더는 뼈대만).
  - PyYAML(로컬 라이브러리)만 외부 의존 — 부재 시 명확히 실패(추측·우회 금지).

종료 코드(design_completeness.py 관례 동형):
  0 = 정상 방출(JSON stdout).
  2 = 사용법·정책 오류(argparse·정책 스키마·미지의 whenSignal·owner 매핑 부재·--out 충돌).

사용법:
  python solution_design_resolve.py --policy <policy.yaml> [--touchpoints a,b] [--interfaces x]
                                    [--data-complex] [--out <manifest-scaffold.json>] [--indent N]

이 스크립트는 planning/adapters/claude/ 경계 소속이다(레이어 co-location·환경 의존 격리 지점).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# --- Windows 콘솔 인코딩 안전(한글 stdout/stderr) — design_completeness 선례 동형 ------------
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001  (구버전 안전 — 기능 무영향)
    pass

# requirement 클래스 토큰 — design_completeness.py 와 동일 규칙(자체 구현·타 어댑터 import 0·경계).
_ALWAYS = "always"
_TOUCHPOINT = "touchpoint"
_INTERFACE = "interface"
_KNOWN_CLASSES = (_ALWAYS, _TOUCHPOINT, _INTERFACE)

# whenSignal 기계 신호 어휘 — 정책이 선언한 whenSignal 을 이 어휘로 대조 매칭한다(산문 when 파싱 0).
# 역할/유형이 아니라 신호 어휘만 안다(SP-INV 5 무촉 — 역할명은 정책에서 온다).
_SIG_TOUCHPOINT = "touchpoint"
_SIG_INTERFACE = "interface"
_SIG_DATA_COMPLEX = "dataComplex"
_SIG_REGULATED = "regulated"
_KNOWN_SIGNALS = (_SIG_TOUCHPOINT, _SIG_INTERFACE, _SIG_DATA_COMPLEX, _SIG_REGULATED)


class PolicyError(Exception):
    """정책 스키마·값 위반(미지의 whenSignal·owner 매핑 부재 포함) — 종료 코드 2."""


# ==========================================================================
# 정책 적재
# ==========================================================================
def load_policy(policy_path: Path) -> dict:
    if not policy_path.exists():
        raise PolicyError("정책 파일 부재 — 산출물 생산 계획 불가: %s" % policy_path)
    try:
        import yaml  # 로컬 라이브러리(네트워크 0). 부재 시 명확히 실패.
    except ImportError as exc:
        raise PolicyError("PyYAML 미설치 — 정책 파싱 불가(로컬 라이브러리 필요): %s" % exc)
    try:
        doc = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:  # type: ignore[attr-defined]
        raise PolicyError("정책 파싱 실패(%s): %s" % (policy_path, exc))
    if not isinstance(doc, dict):
        raise PolicyError("정책 최상위가 매핑(dict)이 아니다: %s" % type(doc).__name__)
    return doc


# ==========================================================================
# required 판정 — design_completeness._is_required 와 동일 규칙(자체 구현·경계 준수)
# ==========================================================================
def _is_required(requirement: str, has_touchpoint: bool, has_interface: bool) -> bool:
    if requirement == _ALWAYS:
        return True
    if requirement == _TOUCHPOINT:
        return has_touchpoint
    if requirement == _INTERFACE:
        return has_interface
    return False  # 알 수 없는 클래스 — 상류에서 이미 오류 처리(도달 시 스킵).


def _signal_value(signal: str, has_touchpoint: bool, has_interface: bool,
                  data_complex: bool, regulated: bool) -> bool:
    """whenSignal 기계 신호 → bool. 미지의 signal 은 상류(resolve)에서 오류 처리."""
    if signal == _SIG_TOUCHPOINT:
        return has_touchpoint
    if signal == _SIG_INTERFACE:
        return has_interface
    if signal == _SIG_DATA_COMPLEX:
        return data_complex
    if signal == _SIG_REGULATED:
        return regulated
    return False


# ==========================================================================
# ① roleComposition — 역할 구성 결정적 계산
# ==========================================================================
def _read_max_specialist_roles(role_sel: dict) -> int | None:
    """maxSpecialistRoles(cap) 를 정책에서 읽는다 — 값 하드코딩 0. 부재 시 None(cap 미집행).

    존재하면 양의 정수여야 한다(스키마 위반은 표면화·추측 금지). bool 은 int 하위형이므로 배제.
    """
    if "maxSpecialistRoles" not in role_sel:
        return None
    cap = role_sel.get("maxSpecialistRoles")
    if isinstance(cap, bool) or not isinstance(cap, int) or cap < 1:
        raise PolicyError("roleSelection.maxSpecialistRoles 가 양의 정수가 아니다: %r" % (cap,))
    return cap


def _compute_role_composition(policy: dict, has_touchpoint: bool, has_interface: bool,
                              data_complex: bool, regulated: bool) -> dict:
    role_sel = policy.get("roleSelection")
    if not isinstance(role_sel, dict):
        raise PolicyError("정책에 roleSelection 매핑이 없다(스키마 위반)")
    comp = role_sel.get("defaultComposition")
    if not isinstance(comp, dict):
        raise PolicyError("정책 roleSelection.defaultComposition 매핑이 없다(스키마 위반)")

    coverage_floor = comp.get("coverageFloor")
    if not isinstance(coverage_floor, str) or not coverage_floor.strip():
        raise PolicyError("defaultComposition.coverageFloor 가 비어 있지 않은 문자열이 아니다: %r"
                          % (coverage_floor,))

    base = comp.get("baseSpecialists")
    if not isinstance(base, list) or not all(isinstance(r, str) and r.strip() for r in base):
        raise PolicyError("defaultComposition.baseSpecialists 가 문자열 목록이 아니다: %r" % (base,))

    conditional = comp.get("conditionalSpecialists")
    if conditional is None:
        conditional = []
    if not isinstance(conditional, list):
        raise PolicyError("defaultComposition.conditionalSpecialists 가 목록이 아니다: %r"
                          % (conditional,))

    activated: list = []
    excluded: list = []
    for i, item in enumerate(conditional):
        if not isinstance(item, dict):
            raise PolicyError("conditionalSpecialists[%d] 가 매핑이 아니다: %r" % (i, item))
        role = item.get("role")
        signal = item.get("whenSignal")
        if not isinstance(role, str) or not role.strip():
            raise PolicyError("conditionalSpecialists[%d].role 이 비어 있지 않은 문자열이 아니다: %r"
                              % (i, role))
        if signal not in _KNOWN_SIGNALS:
            # 산문 when 파싱 금지 — 기계 whenSignal 만 인정. 미지의 신호는 결정성 위반으로 표면화.
            raise PolicyError(
                "conditionalSpecialists[%d](role=%r) whenSignal 이 알려진 신호 %r 중 하나가 아니다: %r"
                " — 정책에 기계 whenSignal 병기 필요(산문 when 파싱 안 함)"
                % (i, role, list(_KNOWN_SIGNALS), signal))
        if _signal_value(signal, has_touchpoint, has_interface, data_complex, regulated):
            activated.append({"role": role, "by": "whenSignal=%s 신호 충족(선언됨)" % signal})
        else:
            excluded.append({"role": role, "reason": "whenSignal=%s 신호 미충족(미선언)" % signal})

    # --- 전문 역할 상한(cap) 집행 — 값·역할명 하드코딩 0, 전부 정책에서 판독(§DC-6·SP-INV 8) ---
    # 산입: base(항상 보존) + 활성 조건부. 불산입: coverageFloor(커버리지 바닥·상한 제외·policy L18).
    # 초과 시 우선순위 = 정책 conditionalSpecialists **선언 순서**(activated 는 이미 선언순) —
    # base 는 항상 보존하고, 초과분은 활성 조건부 중 **선언 후순위(뒤쪽)**부터 excludedByCap 로 방출.
    cap = _read_max_specialist_roles(role_sel)
    excluded_by_cap: list = []
    if cap is not None and (len(base) + len(activated)) > cap:
        conditional_slots = cap - len(base)
        if conditional_slots < 0:
            conditional_slots = 0  # base 만으로 이미 상한 초과 — 활성 조건부 전원 cap 제외.
        kept = activated[:conditional_slots]
        for a in activated[conditional_slots:]:
            excluded_by_cap.append({
                "role": a["role"],
                "reason": "maxSpecialistRoles=%d 초과 — 선언 후순위로 cap 밀림(base %d + 활성 조건부)"
                          % (cap, len(base)),
            })
        activated = kept

    # roles = coverageFloor + base + (cap 통과) activated 전체·중복 제거·정책 입력순 보존.
    roles: list = []
    for r in [coverage_floor] + list(base) + [a["role"] for a in activated]:
        if r not in roles:
            roles.append(r)

    return {
        "coverageFloor": coverage_floor,
        "base": list(base),
        "activatedConditional": activated,
        "excludedConditional": excluded,
        "excludedByCap": excluded_by_cap,
        "roles": roles,
    }


# ==========================================================================
# ② artifactPlan — 산출물 계획 결정적 계산
# ==========================================================================
def _build_owner_map(policy: dict) -> dict:
    ownership = policy.get("artifactOwnership")
    if not isinstance(ownership, list) or not ownership:
        raise PolicyError("정책 artifactOwnership 이 비어 있지 않은 목록이 아니다(스키마 위반)")
    owner_of: dict = {}
    for i, entry in enumerate(ownership):
        if not isinstance(entry, dict):
            raise PolicyError("artifactOwnership[%d] 가 매핑이 아니다: %r" % (i, entry))
        aid = entry.get("id")
        owner = entry.get("owner")
        if not isinstance(aid, str) or not aid.strip():
            raise PolicyError("artifactOwnership[%d].id 가 비어 있지 않은 문자열이 아니다: %r" % (i, aid))
        if not isinstance(owner, str) or not owner.strip():
            raise PolicyError("artifactOwnership[%d](id=%r).owner 가 비어 있지 않은 문자열이 아니다: %r"
                              % (i, aid, owner))
        owner_of[aid] = owner
    return owner_of


def _load_required_set(policy: dict) -> list:
    proj = policy.get("projectionSelection")
    if not isinstance(proj, dict):
        raise PolicyError("정책에 projectionSelection 매핑이 없다(스키마 위반)")
    required_set = proj.get("defaultRequiredSet")
    if not isinstance(required_set, list) or not required_set:
        raise PolicyError("정책 projectionSelection.defaultRequiredSet 이 비어 있지 않은 목록이 아니다")
    items: list = []
    for i, entry in enumerate(required_set):
        if not isinstance(entry, dict):
            raise PolicyError("defaultRequiredSet[%d] 가 매핑이 아니다: %r" % (i, entry))
        rid = entry.get("id")
        req = entry.get("requirement")
        name = entry.get("name") or rid
        if not isinstance(rid, str) or not rid.strip():
            raise PolicyError("defaultRequiredSet[%d].id 가 비어 있지 않은 문자열이 아니다: %r" % (i, rid))
        if req not in _KNOWN_CLASSES:
            raise PolicyError(
                "defaultRequiredSet[%d](id=%r) requirement 이 {always,touchpoint,interface} 중 "
                "하나가 아니다: %r" % (i, rid, req))
        items.append({"id": rid, "name": name, "requirement": req})
    return items


def _compute_artifact_plan(required_items: list, owner_of: dict,
                           has_touchpoint: bool, has_interface: bool) -> list:
    _class_label = {_TOUCHPOINT: "접점", _INTERFACE: "연계"}
    plan: list = []
    for item in required_items:
        rid = item["id"]
        req = item["requirement"]
        if rid not in owner_of:
            raise PolicyError(
                "산출물 id=%r 의 소유 역할(artifactOwnership) 매핑이 없다 — 정책 교차 정합 위반"
                % rid)
        required = _is_required(req, has_touchpoint, has_interface)
        if required:
            note = ""
        elif req in _class_label:
            note = "%s 미선언 → classExclusions.%s 확인 필요(고임팩트 이탈 표면화·silentOmission 금지)" % (
                _class_label[req], req)
        else:
            note = ""
        plan.append({
            "id": rid,
            "name": item["name"],
            "owner": owner_of[rid],
            "requirement": req,
            "required": required,
            "note": note,
        })
    return plan


# ==========================================================================
# ③ manifestScaffold — 매니페스트 뼈대(채워질 자리) 결정적 계산
# ==========================================================================
def _compute_manifest_scaffold(required_items: list, artifact_plan: list,
                               touchpoints: list, interfaces: list,
                               has_touchpoint: bool, has_interface: bool) -> dict:
    # required=true 인 id 만 pending placeholder 로. status="pending"은 작업중 표시(체커 미인정).
    artifacts = [{"id": p["id"], "status": "pending"} for p in artifact_plan if p["required"]]

    # 미선언이라 클래스 전체가 제외된 touchpoint/interface 클래스에 대해 classExclusions placeholder.
    class_exclusions: dict = {}
    for cls, triggered in ((_TOUCHPOINT, has_touchpoint), (_INTERFACE, has_interface)):
        class_ids = [it["id"] for it in required_items if it["requirement"] == cls]
        if class_ids and not triggered:
            class_exclusions[cls] = {"reason": "", "confirmedBy": ""}

    return {
        "declaredTouchpoints": list(touchpoints),
        "declaredInterfaces": list(interfaces),
        "artifacts": artifacts,
        "classExclusions": class_exclusions,
    }


# ==========================================================================
# 엔진 실행
# ==========================================================================
def resolve(policy: dict, touchpoints: list, interfaces: list, data_complex: bool,
            regulated: bool = False) -> dict:
    has_touchpoint = bool(touchpoints)
    has_interface = bool(interfaces)

    role_composition = _compute_role_composition(
        policy, has_touchpoint, has_interface, data_complex, regulated)
    owner_of = _build_owner_map(policy)
    required_items = _load_required_set(policy)
    artifact_plan = _compute_artifact_plan(
        required_items, owner_of, has_touchpoint, has_interface)
    manifest_scaffold = _compute_manifest_scaffold(
        required_items, artifact_plan, touchpoints, interfaces,
        has_touchpoint, has_interface)

    return {
        "roleComposition": role_composition,
        "artifactPlan": artifact_plan,
        "manifestScaffold": manifest_scaffold,
        "_note": (
            "결정적 계산·방출까지만(LLM 0·순수 판독). 실제 위임(역할 서브에이전트 소환)은 주 세션이 "
            "form-A 로 수행한다(binding §6.1) — 이 로더는 subagent 를 spawn 하지 않는다(실행 호스팅 "
            "미설계·04 §3.9). manifestScaffold.artifacts status=pending 은 작업중 placeholder 이며, "
            "생산 완료 후 produced/excluded 로 갱신되어야 design_completeness 게이트를 통과한다."),
    }


# ==========================================================================
# CLI
# ==========================================================================
def _parse_csv(raw: str | None) -> list:
    """쉼표구분 목록 파싱(공백 trim·빈 항목 제거). 비면 공집합."""
    if not raw:
        return []
    return [tok.strip() for tok in raw.split(",") if tok.strip()]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="산출물 생산 프로토콜 결정적 로더(form-B·LLM 0·순수 판독·실행 호스팅 0)")
    parser.add_argument("--policy", required=True,
                        help="Solution Design 정책 데이터 파일(default-policy.yaml).")
    parser.add_argument("--touchpoints", default=None,
                        help="쉼표구분 접점 선언 목록(비면 공집합). 주 세션이 SD 복잡도 판정에서 주입.")
    parser.add_argument("--interfaces", default=None,
                        help="쉼표구분 외부 연계 선언 목록(비면 공집합). 주 세션이 주입.")
    parser.add_argument("--data-complex", action="store_true",
                        help="데이터 복잡 신호(whenSignal=dataComplex 활성화).")
    parser.add_argument("--regulated", action="store_true",
                        help="규제·컴플라이언스 신호(whenSignal=regulated 활성화).")
    parser.add_argument("--out", default=None,
                        help="manifestScaffold 를 이 경로에 기록(선택 편의). 기존 파일 있으면 "
                             "덮어쓰지 않고 오류(순수 판독·산출은 SD 소관).")
    parser.add_argument("--indent", type=int, default=2, help="JSON 들여쓰기(기본 2).")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    touchpoints = _parse_csv(args.touchpoints)
    interfaces = _parse_csv(args.interfaces)

    try:
        policy = load_policy(Path(args.policy))
        result = resolve(policy, touchpoints, interfaces, args.data_complex, args.regulated)
    except PolicyError as exc:
        print("[POLICY-ERROR] %s" % exc, file=sys.stderr)
        return 2

    # --out 선택 기록 — 순수 판독 원칙: 기존 파일은 덮어쓰지 않는다(산출은 SD 소관).
    if args.out:
        out_path = Path(args.out)
        if out_path.exists():
            print("[OUT-CONFLICT] --out 대상이 이미 존재한다(덮어쓰지 않음·산출은 SD 소관): %s"
                  % out_path, file=sys.stderr)
            return 2
        out_path.write_text(
            json.dumps(result["manifestScaffold"], ensure_ascii=False, indent=args.indent) + "\n",
            encoding="utf-8")

    json.dump(result, sys.stdout, ensure_ascii=False, indent=args.indent)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
