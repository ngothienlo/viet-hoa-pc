"""Đóng gói launcher thành một file exe bằng PyInstaller, rồi tự kiểm tra exe vừa tạo.

    .\\.venv\\Scripts\\python.exe tools\\build_exe.py
    .\\.venv\\Scripts\\python.exe tools\\build_exe.py --ui-test

Exe ghi ra `dist/VietHoa.exe`, kèm `dist/VietHoa.exe.sha256`. Chỉ gói file đã commit
trong `games/` (theo `git ls-files`), nên không lẫn `patch/` đã sinh, `build/`,
`extract/` hay `config.json`. Không gói file nào của game: bản vá được tạo trên máy
người chơi lúc bấm Áp dụng.

Sau khi build, script chạy `VietHoa.exe --build-only` trên bản cài đã chọn trong
launcher. Exe thiếu thư viện thì bước này báo lỗi. `--ui-test` thêm một lượt bấm
nút Áp dụng trong cửa sổ thật (có áp lên game).

Có chứng chỉ ký số thì đặt `VH_SIGN_PFX` (đường dẫn file .pfx) và `VH_SIGN_PASSWORD`;
script gọi `signtool` để ký exe.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from importlib import metadata
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from launcher import __version__  # noqa: E402

# Stage và thư mục làm việc để ngoài repo: repo có thể nằm trong OneDrive, OneDrive khóa file lúc đồng bộ.
WORK = Path(tempfile.gettempdir()) / "viet-hoa-pc-build"
STAGE = WORK / "stage"
NAME = "VietHoa"
EXE = ROOT / "dist" / f"{NAME}.exe"

# Script vá của game nạp lúc chạy, nên PyInstaller không tự thấy thư viện của chúng.
# Gói nguyên cây phụ thuộc của các thư viện gốc này, kể cả DLL và file dữ liệu.
ROOTS = ("UnityPy", "TypeTreeGeneratorAPI", "freetype-py", "pycryptodome")
# numpy, scipy có hook riêng của PyInstaller; vh_deps.py import sẵn là đủ.
DEPS = '''"""Thư viện mà script vá của game dùng. Chỉ để PyInstaller gói vào exe."""
import argparse, base64, contextlib, csv, dataclasses, gc, hashlib, io, json, re, struct, unicodedata  # noqa: F401
import numpy  # noqa: F401
import scipy.ndimage  # noqa: F401
from PIL import Image, ImageGrab  # noqa: F401
'''
# Thư viện nặng có thể nằm sẵn trong .venv nhưng không dùng. Loại để exe khỏi phình.
EXCLUDE = ("torch", "torchvision", "sympy", "matplotlib", "pandas", "IPython", "pytest", "tensorboard")

ENTRY = '''"""Điểm vào của VietHoa.exe.

--build-only  chỉ tạo bản vá, ghi build.log
--ui-test     bấm nút Áp dụng trong cửa sổ thật, ghi ui-test.log và ui-test.png
"""
import sys

import vh_deps  # noqa: F401

from launcher.app import build_only, run, ui_test

if "--build-only" in sys.argv:
    sys.exit(build_only())
if "--ui-test" in sys.argv:
    sys.exit(ui_test())
run()
'''


def version_info() -> str:
    parts = tuple(int(part) for part in __version__.split(".")) + (0,)
    numbers = ", ".join(str(part) for part in parts[:4])
    return f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers=({numbers}), prodvers=({numbers}), mask=0x3f, flags=0x0, OS=0x40004,
                    fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('CompanyName', 'viet-hoa-pc'),
      StringStruct('FileDescription', 'Viet hoa game PC'),
      StringStruct('FileVersion', '{__version__}'),
      StringStruct('InternalName', '{NAME}'),
      StringStruct('OriginalFilename', '{NAME}.exe'),
      StringStruct('ProductName', 'Viet hoa'),
      StringStruct('ProductVersion', '{__version__}')])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""


def dependency_packages() -> list[str]:
    """Tên package import được của cả cây phụ thuộc từ ROOTS."""
    seen: set[str] = set()
    stack = list(ROOTS)
    found: set[str] = set()
    while stack:
        name = stack.pop()
        key = re.sub(r"[-_.]+", "-", name).lower()
        if key in seen:
            continue
        seen.add(key)
        try:
            dist = metadata.distribution(name)
        except metadata.PackageNotFoundError:
            raise SystemExit(f"Thiếu thư viện {name}. Chạy: python -m pip install -r requirements.txt")
        for entry in dist.files or []:
            parts = PurePosixPath(str(entry)).parts
            if not parts or parts[0] in ("..", "__pycache__") or parts[0].endswith((".dist-info", ".data")):
                continue
            if len(parts) > 1:
                found.add(parts[0])
            elif parts[0].endswith((".py", ".pyd")):
                found.add(parts[0].split(".")[0])
        for requirement in dist.requires or []:
            if "extra ==" in requirement:
                continue
            stack.append(re.split(r"[ ;<>=!~\[(]", requirement, maxsplit=1)[0])
    return sorted(name for name in found if name not in EXCLUDE)


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
    (STAGE / "version.txt").write_text(version_info(), encoding="utf-8")


def pyinstaller(packages: list[str]) -> None:
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
        "--version-file",
        str(STAGE / "version.txt"),
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
    for package in packages:
        args += ["--collect-all", package]
    for module in EXCLUDE:
        args += ["--exclude-module", module]
    args.append(str(STAGE / f"{NAME}.py"))
    subprocess.run(args, cwd=ROOT, check=True)


def sign() -> None:
    pfx = os.environ.get("VH_SIGN_PFX", "").strip()
    if not pfx:
        print("Chưa ký số: không có VH_SIGN_PFX. SmartScreen có thể cảnh báo khi mở exe.")
        return
    signtool = shutil.which("signtool")
    if signtool is None:
        raise SystemExit("Có VH_SIGN_PFX nhưng không thấy signtool (Windows SDK).")
    subprocess.run(
        [
            signtool,
            "sign",
            "/f",
            pfx,
            "/p",
            os.environ.get("VH_SIGN_PASSWORD", ""),
            "/fd",
            "SHA256",
            "/tr",
            "http://timestamp.digicert.com",
            "/td",
            "SHA256",
            str(EXE),
        ],
        check=True,
    )
    print("Đã ký số exe.")


def write_checksum() -> str:
    digest = hashlib.sha256(EXE.read_bytes()).hexdigest()
    (EXE.parent / f"{EXE.name}.sha256").write_text(f"{digest}  {EXE.name}\n", encoding="utf-8")
    return digest


def state_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    return (Path(base) if base else Path.home() / "AppData" / "Local") / "viet-hoa-pc"


def check_exe(flag: str, log_name: str) -> None:
    """Chạy exe với cờ kiểm tra, đọc log. Exe là app cửa sổ nên kết quả nằm trong file log."""
    print(f"Chạy {EXE.name} {flag}...")
    code = subprocess.run([str(EXE), flag], check=False).returncode
    log = state_dir() / log_name
    text = log.read_text(encoding="utf-8") if log.is_file() else ""
    tail = "\n".join(text.splitlines()[-6:])
    if code != 0:
        raise SystemExit(f"{EXE.name} {flag} lỗi (mã {code}). Cuối {log}:\n{tail}")
    print(tail)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ui-test", action="store_true", help="bấm Áp dụng trong cửa sổ exe (áp lên game)")
    parser.add_argument("--skip-check", action="store_true", help="không chạy exe sau khi build")
    args = parser.parse_args()

    packages = dependency_packages()
    print("Gói kèm:", ", ".join(packages))
    stage()
    pyinstaller(packages)
    sign()
    digest = write_checksum()
    print(f"Đã tạo {EXE} ({EXE.stat().st_size / 1048576:.0f} MB), phiên bản {__version__}")
    print(f"SHA-256: {digest}")
    if args.skip_check:
        return 0
    check_exe("--build-only", "build.log")
    if args.ui_test:
        check_exe("--ui-test", "ui-test.log")
    return 0


if __name__ == "__main__":
    sys.exit(main())
