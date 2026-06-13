"""查看开发服务日志（终端关闭后仍可查看）"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"

FILES = {
    "backend": LOG_DIR / "backend.log",
    "frontend": LOG_DIR / "frontend.log",
}


def print_tail(path: Path, lines: int) -> None:
    if not path.exists():
        print(f"[缺失] {path}")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    chunk = text.splitlines()[-lines:]
    print(f"\n----- {path.name} (最近 {len(chunk)} 行) -----")
    print("\n".join(chunk))


def follow_one(path: Path, prefix: str) -> None:
    if not path.exists():
        print(f"{prefix}日志不存在: {path}")
        return

    with path.open("r", encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                print(f"{prefix}{line}", end="")
            else:
                time.sleep(0.25)


def main() -> None:
    parser = argparse.ArgumentParser(description="查看 minimal 项目开发日志")
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        choices=["backend", "frontend", "all"],
        help="要查看的服务",
    )
    parser.add_argument("-f", "--follow", action="store_true", help="实时跟踪新日志")
    parser.add_argument("-n", "--lines", type=int, default=100, help="显示最近 N 行")
    args = parser.parse_args()

    targets = list(FILES.keys()) if args.target == "all" else [args.target]

    if args.follow:
        if len(targets) > 1:
            import threading

            print("实时跟踪日志（Ctrl+C 退出）...")
            threads = []
            for name in targets:
                prefix = "[后端] " if name == "backend" else "[前端] "
                t = threading.Thread(
                    target=follow_one,
                    args=(FILES[name], prefix),
                    daemon=True,
                )
                t.start()
                threads.append(t)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n已停止跟踪。")
        else:
            name = targets[0]
            prefix = "[后端] " if name == "backend" else "[前端] "
            print(f"实时跟踪 {FILES[name]} （Ctrl+C 退出）...")
            try:
                follow_one(FILES[name], prefix)
            except KeyboardInterrupt:
                print("\n已停止跟踪。")
        return

    for name in targets:
        print_tail(FILES[name], args.lines)


if __name__ == "__main__":
    main()
