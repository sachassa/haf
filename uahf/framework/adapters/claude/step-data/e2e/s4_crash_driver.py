"""s4 강제 중단 드라이버 — 호스트를 자식 프로세스로 띄우고 B 의 Active(dispatch)
이벤트가 append 되는 즉시 프로세스 트리를 강제 종료한다(크래시 모사).

사용법:  python s4_crash_driver.py <run-dir>

종료 후 events.jsonl 은 B 가 Active(중단 흔적)로 남는다 — 재개(run_host.py 재실행)가
이를 Failed(실행 중단)으로 append 하고 재시도한다(프로토콜 §4.2).
"""

from __future__ import annotations

import json
import locale
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    run_dir = Path(sys.argv[1]).resolve()
    events = run_dir / "events.jsonl"
    here = Path(__file__).resolve().parent

    proc = subprocess.Popen([sys.executable, "run_host.py", str(run_dir)], cwd=str(here))
    print("[CRASH-DRIVER] host pid=%d launched; polling for B Active(dispatch)..." % proc.pid)

    deadline = time.time() + 400
    killed = False
    while time.time() < deadline:
        if proc.poll() is not None:
            print("[CRASH-DRIVER] host exited early (code=%s) before B-active" % proc.returncode)
            return 1
        if events.exists():
            try:
                lines = events.read_text(encoding="utf-8").splitlines()
            except Exception:
                lines = []
            for ln in lines:
                try:
                    e = json.loads(ln)
                except ValueError:
                    continue
                if e.get("cycle_id") == "B" and (e.get("ref") or {}).get("kind") == "dispatch":
                    print("[CRASH-DRIVER] B Active detected (at=%s) -> taskkill /F /T tree" % e.get("at"))
                    # taskkill 은 콘솔 코드페이지로 출력하는 도구다 — utf-8 강제 금지(한국어
                    # 환경 cp949 를 오디코딩/예외로 만든다). errors="replace" 로 관측 경로 보존
                    # (디코딩 크래시로 아래 진단 출력이 유실되는 것을 막는다).
                    r = subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                                       capture_output=True, text=True,
                                       encoding=locale.getpreferredencoding(False),
                                       errors="replace")
                    print("[CRASH-DRIVER] taskkill rc=%d out=%s" % (r.returncode, (r.stdout or r.stderr).strip()[:200]))
                    killed = True
                    break
        if killed:
            break
        time.sleep(0.5)

    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        pass
    print("[CRASH-DRIVER] result=%s host-exit=%s" % ("KILLED" if killed else "TIMEOUT", proc.returncode))
    return 0 if killed else 2


if __name__ == "__main__":
    sys.exit(main())
