"""在终端输出同时写入日志文件"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 4:
        print("用法: service_runner.py <logfile> <cwd> <command...>", file=sys.stderr)
        return 1

    log_path = Path(sys.argv[1]).resolve()
    cwd = Path(sys.argv[2]).resolve()
    cmd = sys.argv[3:]

    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8", errors="replace") as logf:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"\n{'=' * 60}\n[{stamp}] 启动: {' '.join(cmd)}\n"
        logf.write(header)
        logf.flush()

        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        assert proc.stdout is not None
        for raw in iter(proc.stdout.readline, b""):
            text = raw.decode("utf-8", errors="replace")
            sys.stdout.write(text)
            sys.stdout.flush()
            logf.write(text)
            logf.flush()

        code = proc.wait()
        logf.write(f"\n[{datetime.now():%Y-%m-%d %H:%M:%S}] 退出 code={code}\n")
        return code


if __name__ == "__main__":
    raise SystemExit(main())
