"""

启动脚本 - 分别在两个终端窗口启动后端与前端，并写入 logs/ 日志

"""

from __future__ import annotations



import shutil

import socket

import subprocess

import sys

from pathlib import Path



ROOT = Path(__file__).resolve().parent

BACKEND_DIR = ROOT / "backend"

FRONTEND_DIR = ROOT / "frontend"

RUNNER = ROOT / "scripts" / "service_runner.py"

LOG_DIR = ROOT / "logs"

BACKEND_LOG = LOG_DIR / "backend.log"

FRONTEND_LOG = LOG_DIR / "frontend.log"

BACKEND_PORT = 8000





def _require_paths() -> None:

    if not BACKEND_DIR.is_dir():

        raise SystemExit(f"找不到后端目录: {BACKEND_DIR}")

    if not FRONTEND_DIR.is_dir():

        raise SystemExit(f"找不到前端目录: {FRONTEND_DIR}")

    if not RUNNER.is_file():

        raise SystemExit(f"找不到启动器: {RUNNER}")

    if not shutil.which("npm"):

        raise SystemExit("未找到 npm，请先安装 Node.js")

    LOG_DIR.mkdir(parents=True, exist_ok=True)





def _port_in_use(port: int) -> bool:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.settimeout(0.5)

        return sock.connect_ex(("127.0.0.1", port)) == 0





def _free_port(port: int) -> None:

    if not _port_in_use(port):

        return



    print(f"[WARN] 端口 {port} 已被占用，正在停止旧进程…")

    if sys.platform == "win32":

        script = (

            f"Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue "

            f"| Select-Object -ExpandProperty OwningProcess -Unique "

            f"| ForEach-Object {{ Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }}"

        )

        subprocess.run(["powershell", "-NoProfile", "-Command", script], check=False)

    else:

        subprocess.run(["fuser", "-k", f"{port}/tcp"], check=False)



    if _port_in_use(port):

        print(f"[WARN] 无法自动释放端口 {port}，请手动关闭占用该端口的进程后重试。")





def _quote(value: str) -> str:

    if " " in value or '"' in value:

        return f'"{value}"'

    return value





def _build_runner_cmd(title: str, log_file: Path, cwd: Path, cmd_parts: list[str]) -> str:

    runner = _quote(str(RUNNER))

    log_path = _quote(str(log_file))

    workdir = _quote(str(cwd))

    command = " ".join(_quote(p) for p in cmd_parts)

    py = _quote(sys.executable)

    return (

        f"title {title} && "

        f"{py} {runner} {log_path} {workdir} {command}"

    )





def _spawn_windows(command: str, cwd: Path) -> None:

    subprocess.Popen(

        command,

        cwd=str(cwd),

        shell=True,

        creationflags=subprocess.CREATE_NEW_CONSOLE,

    )





def _spawn_macos(title: str, command: str, cwd: Path) -> None:

    subprocess.Popen(

        ["osascript", "-e", f'tell application "Terminal" to do script "{command}"'],

    )





def _spawn_linux(title: str, command: str, cwd: Path) -> None:

    bash_cmd = f'cd "{cwd}" && {command}; exec bash'

    candidates = [

        ["gnome-terminal", "--title", title, "--", "bash", "-lc", bash_cmd],

        ["konsole", "--new-tab", "-p", f"tabtitle={title}", "-e", "bash", "-lc", bash_cmd],

        ["xfce4-terminal", "--title", title, "-e", f"bash -lc '{bash_cmd}'"],

        ["xterm", "-T", title, "-e", "bash", "-lc", bash_cmd],

    ]

    for candidate in candidates:

        if shutil.which(candidate[0]):

            subprocess.Popen(candidate)

            return

    raise SystemExit("未找到可用的终端程序（gnome-terminal / konsole / xterm 等）")





def spawn_terminal(title: str, command: str, cwd: Path) -> None:

    if sys.platform == "win32":

        _spawn_windows(command, cwd)

    elif sys.platform == "darwin":

        _spawn_macos(title, command, cwd)

    else:

        _spawn_linux(title, command, cwd)





def main() -> None:

    _require_paths()

    _free_port(BACKEND_PORT)



    npm = shutil.which("npm") or "npm"

    backend_parts = [

        sys.executable, "-m", "uvicorn", "main:app",

        "--reload", "--host", "127.0.0.1", "--port", str(BACKEND_PORT),

    ]

    frontend_parts = [npm, "run", "serve"]



    backend_cmd = _build_runner_cmd("留白 Backend", BACKEND_LOG, BACKEND_DIR, backend_parts)

    frontend_cmd = _build_runner_cmd("留白 Frontend", FRONTEND_LOG, FRONTEND_DIR, frontend_parts)



    print("正在打开终端窗口...")

    spawn_terminal("留白 Backend", backend_cmd, BACKEND_DIR)

    spawn_terminal("留白 Frontend", frontend_cmd, FRONTEND_DIR)



    print("\n已启动：")

    print("  后端  http://127.0.0.1:8000")

    print("  前端  http://localhost:8080")

    print("\n日志文件（终端关闭后仍可查看）：")

    print(f"  后端  {BACKEND_LOG}")

    print(f"  前端  {FRONTEND_LOG}")

    print("\n查看日志：")

    print("  python view_logs.py          # 最近 100 行")

    print("  python view_logs.py -f       # 实时跟踪")

    print("  python view_logs.py backend  # 只看后端")

    print("\n关闭对应终端窗口即可停止服务。")
    print("\n生产部署见 DEPLOY.md（推荐 Nginx + systemd，或 Docker）。")





if __name__ == "__main__":

    main()

