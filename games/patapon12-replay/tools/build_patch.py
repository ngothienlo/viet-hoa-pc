"""Tạo bản vá PATAPON 1+2 REPLAY từ bản cài của người chơi. Launcher gọi `build()`.

Đọc file gốc của game trên máy (qua `original()`), ghi file vá vào `out`:
4 bundle `LocalizeData` có câu Việt, và các font đã ghép chữ Việt. Không cần
`config.json` hay file font ngoài. Repo và bản exe không chứa file nào của game.

    python games/patapon12-replay/tools/build_patch.py "<thư mục cài>" "<thư mục ra>"
"""

from __future__ import annotations

import contextlib
import io
import os
import shutil
import sys
from pathlib import Path
from typing import Callable

TOOLS = Path(__file__).resolve().parent
FONT_TOOLS = TOOLS / "font"
# Module của game đọc đường dẫn lúc import. Mỗi lần build phải nạp lại từ đầu.
MODULES = (
    "game_config",
    "extract_strings",
    "apply_locale_patch",
    "bake_sdf",
    "compose_glyphs",
    "inventory",
    "apply_vietnamese_font",
)


class _Lines(io.TextIOBase):
    """Chuyển từng dòng in ra sang hàm log của launcher."""

    def __init__(self, log: Callable[[str], None]) -> None:
        self.log = log
        self.pending = ""

    def write(self, text: str) -> int:
        self.pending += text
        while "\n" in self.pending:
            line, self.pending = self.pending.split("\n", 1)
            if line.strip():
                self.log(line.strip())
        return len(text)

    def flush(self) -> None:
        if self.pending.strip():
            self.log(self.pending.strip())
        self.pending = ""


def build(install: Path, out: Path, log: Callable[[str], None] | None = None) -> None:
    """Ghi bản vá vào `out` (xóa sạch trước). Lỗi thì ném SystemExit kèm thông báo tiếng Việt.

    `log` nhận từng dòng tiến độ. Bỏ trống thì in ra stdout thật, lấy trước khi chuyển hướng.
    """
    if log is None:
        real = sys.stdout

        def log(line: str) -> None:
            if real is not None:
                real.write(line + "\n")
                real.flush()

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    os.environ["VH_INSTALL_DIR"] = str(install)
    os.environ["VH_PATCH_DIR"] = str(out)
    for name in MODULES:
        sys.modules.pop(name, None)
    for folder in (FONT_TOOLS, TOOLS):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))

    stream = _Lines(log)
    with contextlib.redirect_stdout(stream):
        import apply_locale_patch
        import apply_vietnamese_font

        log("Ghi câu tiếng Việt vào LocalizeData...")
        apply_locale_patch.main()
        log("Ghép chữ Việt vào font của game...")
        apply_vietnamese_font.build_fonts()
    stream.flush()


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    build(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
