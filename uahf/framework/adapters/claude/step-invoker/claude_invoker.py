"""invoker 인터페이스의 claude 구현 (형태 B — Adapter 격리 경계).

이 모듈은 framework/loop/step-host/ 의 provider-중립 Invoker 계약을 claude CLI headless
호출로 실현한다. 여기는 Adapter 경계이므로 특정 실행 환경·CLI·권한 옵션 토큰의 사용이
허용되며(structure.md §4 규칙 4·자매 바인딩 §0 동형), 그 격리가 이 경계의 존재 이유다.

책임(프로토콜 §7.2 바인딩 지점):
  - 직렬화 번들 -> claude CLI headless 호출(subprocess·shell=False·타임아웃·작업 디렉터리).
  - Autonomy Policy -> CLI 권한 플래그 매핑.
  - 역할/모델 슬롯 전달.
  - 완료 보고 / 실패 보고 회수 · 차단(blocked) 표면화.

게이트 등급 분리(SH-INV-4)는 중립 Host 가 소유한다 — 이 모듈은 policy 를 CLI 플래그로
매핑만 하며, unrestricted 라도 Host 의 CP2 디스패치·Escalated 정지를 우회할 수 없다.

실제 CLI 실호출 검증은 W3 E2E 소관이다. 이 모듈의 자체 테스트는 명령행 조립·결과
파싱만 검증한다(CLI 실호출 없음).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# provider-중립 Invoker 계약을 framework/loop/step-host/ 에서 로드한다.
# 경로: .../framework/adapters/claude/step-invoker/claude_invoker.py
#   parents[3] = .../framework  ->  framework/loop/step-host
_STEP_HOST_DIR = Path(__file__).resolve().parents[3] / "loop" / "step-host"
if str(_STEP_HOST_DIR) not in sys.path:
    sys.path.insert(0, str(_STEP_HOST_DIR))

from invoker import (  # noqa: E402
    Invoker,
    InvokeRequest,
    InvokeResult,
    KIND_BLOCKED,
    KIND_COMPLETION,
    KIND_FAILURE,
    POLICY_AUTO_APPROVE,
    POLICY_INTERACTIVE,
    POLICY_UNRESTRICTED,
    ROLE_ADVISOR,
    ROLE_VERIFIER,
    ROLE_WORKER,
)

# 실측 기준(2026-07-13): claude 2.1.207 · Python 3.14.4 · win32 (`python` 런처).
# CLI 플래그는 `claude --help` 실측 확인분만 사용한다.
DEFAULT_CLI = "claude"
BLOCKING_MARK = "차단됨"

# 역할별 브리프 — 신규 fresh 세션이 자기 역할로 수행하고 구조화 보고(JSON)를 최종
# 메시지로 내도록 지시한다. 실행 상세는 run 데이터 백엔드에 남고 상위로는 보고만
# 회수된다(SH-INV-8).
_ROLE_BRIEFS = {
    ROLE_WORKER: (
        "너는 Worker 다. 주어진 Step Contract·확정 참조·constraints·(있으면) feedback 만으로 "
        "구현하고 Execute 종료 시 CP1 자체 점검을 수행하라. 자기 점검을 최종 승인으로 삼지 "
        "말라. 최종 메시지의 마지막 줄에 완료 보고 또는 실패 보고를 JSON 한 객체로 출력하라 "
        "— 완료: {\"artifacts\":[...],\"self_check\":...,\"failures\":...,\"open_questions\":...,"
        "\"verify_basis\":...} · 실패: {\"reason\":...,\"repro\":...,\"blocking\":\"차단됨|계속 가능\"}."
    ),
    ROLE_VERIFIER: (
        "너는 Verifier 다. 완료 보고를 그대로 신뢰하지 말고 산출물(artifacts) 자체를 근거로 "
        "criteria(done) 충족을 독립 판정하라. 결정적(스크립트로 판독 가능한) 검사는 제공된 "
        "결정적 검증 리포트가 있으면 그것을 소비하고 재구현하지 말라 — 너는 의미 축(요건 충족·"
        "설계 정합·누락)에 집중한다. delegation.task/done 이 참조형 sentinel(예 \"위 task 필드와 "
        "동일\")인 것은 계약 위반이 아니다(참조형 표준). 또한 **AC 적정성**을 판정하라 — done AC "
        "자체가 산출을 실제로 판별하는 증거인지 의심하라: (i) 합성(손으로 지어낸) 입력이 외부 "
        "도구의 실출력을 대체하고 있지 않은가 (ii) assert 가 실제 값을 못박는가, 아니면 거의 항상 "
        "참인 형태(비어있지 않음·타입만 확인·예외 미발생)인가 (iii) \"통과했다\"는 사실 자체가 "
        "요건 충족의 증거가 되는가. AC 가 부적정하면 산출물이 그럴듯해 보여도 **Fail** 로 판정하고 "
        "rework 에 산출 결함과 구분해 **AC 결함**임을 명시하라. 특히 외부 도구·프로세스를 호출하는 "
        "단위는 그 도구의 **실출력 캡처 픽스처를 AC 가 실제로 소비**하는지 확인하고, 소비하지 "
        "않으면서 외부 계약을 검증했다고 주장하는 보고는 신뢰하지 말라 — 미검증이면 완료 보고 "
        "open_questions 에 「미검증 외부 계약」으로 신고되어 있어야 한다. 최종 메시지의 마지막 줄에 "
        "판정을 JSON 한 객체로 출력하라 — {\"verdict\":\"Pass|Fail\",\"rework\":...}."
    ),
    ROLE_ADVISOR: (
        "너는 Advisor 다. 최종 승인 판정을 수행하라. 최종 메시지의 마지막 줄에 "
        "{\"verdict\":\"Pass|Fail|Conditional\",\"rework\":...} 를 JSON 으로 출력하라."
    ),
}


class ClaudeInvoker(Invoker):
    """claude CLI headless 호출로 신규 실행 컨텍스트를 기동하는 invoker."""

    def __init__(self, cli: str = DEFAULT_CLI, output_format: str = "json",
                 extra_args: list[str] | None = None) -> None:
        self.cli = cli
        self.output_format = output_format
        self.extra_args = list(extra_args or [])

    # ------------------------------------------------------------------
    # Autonomy Policy -> CLI 권한 플래그 매핑 (§6.2 · 바인딩)
    # ------------------------------------------------------------------
    def permission_flags(self, policy: str) -> list[str]:
        """policy 를 claude 권한 실행 옵션으로 매핑한다.

        게이트 등급 분리: 이 매핑은 '도구 실행 승인 프롬프트 축'만 제어한다. Human
        Decision Gate(Escalated) 는 어떤 policy 에서도 Host 가 정지시키며 이 플래그가
        우회하지 못한다(SH-INV-4).
        """
        if policy == POLICY_UNRESTRICTED:
            # 승인 프롬프트 전면 생략. 이 문자열은 이 바인딩 경계(step-invoker/ · binding md)
            # 에만 존재한다(저장소 전수 스캔 AC).
            return ["--dangerously-skip-permissions"]
        if policy == POLICY_AUTO_APPROVE:
            # 선언된 허용 범위 내 자동 승인.
            return ["--permission-mode", "acceptEdits"]
        # interactive(기본): 별도 권한 생략 플래그 없음.
        return []

    # ------------------------------------------------------------------
    # 명령행 조립 · 프롬프트 직렬화
    # ------------------------------------------------------------------
    def build_prompt(self, request: InvokeRequest) -> str:
        """Fresh Context 번들을 세션 프롬프트(자기서술 JSON)로 직렬화한다."""
        return json.dumps(request.bundle, ensure_ascii=False, sort_keys=True)

    def system_brief(self, request: InvokeRequest) -> str:
        role = request.role or ROLE_WORKER
        return _ROLE_BRIEFS.get(role, _ROLE_BRIEFS[ROLE_WORKER])

    def build_command(self, request: InvokeRequest) -> list[str]:
        """subprocess argv(shell=False) 조립. 실측 플래그만 사용한다."""
        cmd: list[str] = [self.cli, "-p", self.build_prompt(request)]
        cmd += ["--output-format", self.output_format]
        cmd += ["--append-system-prompt", self.system_brief(request)]
        # 모델 슬롯 전달(있을 때만) — 값의 의미는 02 §4 소관, Host 는 전달만 한다.
        if request.model:
            cmd += ["--model", str(request.model)]
        # 작업 디렉터리를 도구 접근 허용에 추가.
        if request.workdir:
            cmd += ["--add-dir", str(Path(request.workdir))]
        cmd += self.permission_flags(request.policy)
        cmd += self.extra_args
        return cmd

    # ------------------------------------------------------------------
    # 결과 파싱 — 완료/실패/차단/verdict 분류
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_report(text: str) -> dict[str, Any] | None:
        """텍스트에서 마지막 JSON 객체(구조화 보고)를 추출한다."""
        if not text:
            return None
        depth = 0
        start = -1
        candidate = None
        for i, ch in enumerate(text):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}":
                if depth > 0:
                    depth -= 1
                    if depth == 0 and start >= 0:
                        snippet = text[start:i + 1]
                        try:
                            candidate = json.loads(snippet)
                        except (ValueError, TypeError):
                            pass  # 파싱 실패 시 마지막 유효 후보를 유지
        return candidate

    def parse_result(self, stdout: str, returncode: int) -> InvokeResult:
        """CLI 표준출력(--output-format json 봉투)과 종료 코드를 InvokeResult 로 매핑한다.

        Host 는 kind 로만 분기하므로(SH-INV-1), 여기서 실행 단위·Verifier 의 선언을 kind 로
        표면화한다 — 내용 판정을 대신 내리지 않는다.
        """
        result_text = stdout
        envelope = None
        try:
            envelope = json.loads(stdout) if stdout else None
        except (ValueError, TypeError):
            envelope = None
        if isinstance(envelope, dict):
            # `--output-format json` 봉투에서 결과 텍스트를 꺼낸다.
            result_text = envelope.get("result") or envelope.get("text") or stdout
            if envelope.get("is_error"):
                returncode = returncode or 1

        report = self._extract_report(result_text if isinstance(result_text, str) else stdout)

        if report is None:
            # 보고를 파싱하지 못함 — 추측하지 않고 실패로 처리(재시도 대상).
            return InvokeResult(
                kind=KIND_FAILURE,
                failure={"reason": "구조화 보고 파싱 실패", "repro": "returncode=" + str(returncode),
                         "blocking": "계속 가능"},
                ref="parse-miss",
            )

        # Verifier/Advisor verdict.
        if "verdict" in report:
            return InvokeResult(kind=KIND_COMPLETION, completion=report, ref="verdict")

        # 실패/차단 보고(blocking 필드 존재).
        if "blocking" in report:
            if str(report.get("blocking")).strip() == BLOCKING_MARK:
                return InvokeResult(kind=KIND_BLOCKED, failure=report, ref="blocked")
            return InvokeResult(kind=KIND_FAILURE, failure=report, ref="failure")

        # 완료 보고.
        return InvokeResult(kind=KIND_COMPLETION, completion=report, ref="completion")

    # ------------------------------------------------------------------
    # 실행 (subprocess) — 실호출 검증은 W3
    # ------------------------------------------------------------------
    def invoke(self, request: InvokeRequest) -> InvokeResult:
        cmd = self.build_command(request)
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=False,  # 인젝션 방지 — argv 직접 전달.
                cwd=(str(Path(request.workdir)) if request.workdir else None),
                timeout=request.timeout,
                encoding="utf-8",
            )
        except subprocess.TimeoutExpired:
            # 타임아웃은 차단이 아니라 실패로 처리(재시도 규칙 적용). 정지 신호는 Host 소관.
            return InvokeResult(
                kind=KIND_FAILURE,
                failure={"reason": "실행 컨텍스트 타임아웃", "repro": "timeout=" + str(request.timeout),
                         "blocking": "계속 가능"},
                ref="timeout",
            )
        except FileNotFoundError:
            return InvokeResult(
                kind=KIND_FAILURE,
                failure={"reason": "claude CLI 미탐지: " + self.cli, "repro": "PATH 확인 필요",
                         "blocking": "계속 가능"},
                ref="cli-missing",
            )
        return self.parse_result(proc.stdout or "", proc.returncode)
