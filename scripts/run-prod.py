"""本地生产模式：构建前端并由后端同域托管（无 Nginx，仅本机验证用）"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"
DATA_DIR = ROOT / "data"
PORT = int(os.getenv("PORT", "8000"))


def _require() -> None:
    if not shutil.which("npm"):
        raise SystemExit("未找到 npm，请先安装 Node.js")
    if not (BACKEND_DIR / "main.py").is_file():
        raise SystemExit(f"找不到后端: {BACKEND_DIR}")
    if not (FRONTEND_DIR / "package.json").is_file():
        raise SystemExit(f"找不到前端: {FRONTEND_DIR}")


def _build_frontend() -> None:
    print("[1/2] 构建前端…")
    subprocess.run(["npm", "run", "build"], cwd=str(FRONTEND_DIR), check=True)
    if not (DIST_DIR / "index.html").is_file():
        raise SystemExit(f"构建失败，未找到 {DIST_DIR / 'index.html'}")


def _run_backend() -> None:
    print("[2/2] 启动后端（托管前端静态资源）…")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("DATA_DIR", str(DATA_DIR))
    env["STATIC_DIR"] = str(DIST_DIR.resolve())
    env["SERVE_STATIC"] = "true"
    env.setdefault("HOST", "0.0.0.0")
    env.setdefault("PORT", str(PORT))

    cmd = [
        sys.executable, "-m", "uvicorn", "main:app",
        "--host", env["HOST"],
        "--port", env["PORT"],
    ]
    print(f"\n访问 http://127.0.0.1:{env['PORT']}")
    print(f"数据目录 {env['DATA_DIR']}")
    print("Ctrl+C 停止\n")
    subprocess.run(cmd, cwd=str(BACKEND_DIR), env=env, check=True)


def main() -> None:
    _require()
    _build_frontend()
    _run_backend()


if __name__ == "__main__":
    main()
