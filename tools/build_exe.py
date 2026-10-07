"""Đóng gói launcher thành một file exe bằng PyInstaller.

    .\\.venv\\Scripts\\python.exe tools\\build_exe.py

Exe ghi ra `dist/VietHoa.exe`. Chỉ gói file đã commit trong `games/` (theo
`git ls-files`), nên không lẫn `patch/` đã sinh, `build/`, `extract/` hay `config.json`.
Không gói file nào của game: bản vá được tạo trên máy người chơi lúc bấm Áp dụng.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Stage và thư mục làm việc để ngoài repo: repo có thể nằm trong OneDrive, OneDrive khóa file lúc đồng bộ.
WORK = Path(tempfile.gettempdir()) / "viet-hoa-pc-build"
STAGE = WORK / "stage"
NAME = "VietHoa"

# Script vá của từng game được nạp lúc chạy, nên PyInstaller không tự thấy thư viện
# chúng dùng. File này import sẵn các thư viện đó để PyInstaller gói vào.
DEPS = '''"""Thư viện mà script vá của game dùng. Chỉ để PyInstaller gói vào exe."""
import argparse, base64, contextlib, csv, dataclasses, gc, hashlib, io, json, re, struct, unicodedata  # noqa: F401
import numpy  # noqa: F401
import scipy.ndimage  # noqa: F401
import freetype  # noqa: F401
import UnityPy  # noqa: F401
import UnityPy.helpers.TypeTreeGenerator  # noqa: F401
import TypeTreeGeneratorAPI  # noqa: F401
from Crypto.Cipher import AES  # noqa: F401
from PIL import Image  # noqa: F401
'''

ENTRY = '''"""Điểm vào của VietHoa.exe. `VietHoa.exe --build-only` chỉ tạo bản vá và ghi build.log."""
import sys

import vh_deps  # noqa: F401

from launcher.app import build_only, run

if "--build-only" in sys.argv:
    sys.exit(build_only())
run()
'''

# Gói kèm cả file dữ liệu và DLL của các thư viện có phần native.
COLLECT = (
    "UnityPy",
    "TypeTreeGeneratorAPI",
    "texture2ddecoder",
    "etcpak",
    "astc_encoder",
    "freetype",
    "fmod_toolkit",
    "pyfmodex",
    "archspec",
)
# Thư viện nặng có thể nằm sẵn trong .venv nhưng không dùng. Loại để exe khỏi phình.
EXCLUDE = ("torch", "torchvision", "sympy", "matplotlib", "pandas", "IPython", "pytest", "tensorboard")


def tracked_game_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "games"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def stage() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    for relative in tracked_game_files():
        source = ROOT / relative
        if not source.is_file():
            continue
        destination = STAGE / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    (STAGE / "vh_deps.py").write_text(DEPS, encoding="utf-8")
    (STAGE / f"{NAME}.py").write_text(ENTRY, encoding="utf-8")


def main() -> int:
    stage()
    args = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name",
        NAME,
        "--distpath",
        str(ROOT / "dist"),
        "--workpath",
        str(WORK / "pyinstaller"),
        "--specpath",
        str(WORK),
        "--paths",
        str(ROOT),
        "--paths",
        str(STAGE),
        "--add-data",
        f"{STAGE / 'games'};games",
    ]
    for package in COLLECT:
        args += ["--collect-all", package]
    for module in EXCLUDE:
        args += ["--exclude-module", module]
    args.append(str(STAGE / f"{NAME}.py"))
    subprocess.run(args, cwd=ROOT, check=True)
    exe = ROOT / "dist" / f"{NAME}.exe"
    print(f"Đã tạo {exe} ({exe.stat().st_size / 1048576:.0f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
