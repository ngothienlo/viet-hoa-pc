"""Tạo bản vá Potion Permit từ bản cài của người chơi. Launcher gọi `build()`.

Ghi câu Việt trong `locale/vi/strings.csv` vào cột English của cả hai `LanguageSource`
(trong `sharedassets0.assets` và scene `level1`). Người chơi để game ở English thì thấy
tiếng Việt; term chưa dịch giữ tiếng Anh. Đọc file gốc qua bản sao lưu của launcher.
Repo và bản exe không chứa file nào của game.

    python games/potion-permit/tools/build_patch.py "<thư mục cài>" "<thư mục ra>"
"""

from __future__ import annotations

import csv
import io
import os
import shutil
import sys
from pathlib import Path
from typing import Callable

TOOLS = Path(__file__).resolve().parent
# Module của game này. Game khác có module trùng tên, nên bỏ cache trước và sau khi build.
MODULES = ("game_config", "extract_strings")
# Ghi chú của dòng không được đưa vào game.
SKIP_NOTES = {"dịch máy", "không dịch", "lệch placeholder"}


def translations(csv_path: Path) -> dict[str, str]:
    table: dict[str, str] = {}
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            vi = row.get("vi") or ""
            if vi.strip() and (row.get("note") or "").strip() not in SKIP_NOTES:
                table[row["id"]] = vi
    return table


def _use_own_modules() -> None:
    while str(TOOLS) in sys.path:
        sys.path.remove(str(TOOLS))
    sys.path.insert(0, str(TOOLS))
    for name in MODULES:
        sys.modules.pop(name, None)


def build(install: Path, out: Path, log: Callable[[str], None] | None = None) -> None:
    """Ghi bản vá vào `out` (xóa sạch trước). Lỗi thì ném SystemExit kèm thông báo tiếng Việt."""
    if log is None:
        real = sys.stdout

        def log(line: str) -> None:
            if real is not None:
                real.write(line + "\n")
                real.flush()

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    saved = {key: os.environ.get(key) for key in ("VH_INSTALL_DIR", "VH_PATCH_DIR")}
    os.environ["VH_INSTALL_DIR"] = str(install)
    os.environ["VH_PATCH_DIR"] = str(out)
    try:
        _use_own_modules()
        import extract_strings as ex
        from game_config import DATA_NAME

        table = translations(ex.CSV_PATH)
        log(f"Có {len(table)} term tiếng Việt.")
        gen = ex.generator(install)
        for filename in ex.SOURCES:
            env = ex.open_file(filename, install, gen)
            changed = 0
            for obj in ex.language_sources(env, filename):
                tree = obj.read_typetree()
                source = tree["mSource"]
                column = ex.english_index(source)
                for term in source["mTerms"]:
                    vi = table.get(term["Term"])
                    if vi is not None and term["Languages"][column] != vi:
                        term["Languages"][column] = vi
                        changed += 1
                obj.save_typetree(tree)
            assets = next(obj.assets_file for obj in env.objects if obj.assets_file.name == filename)
            destination = out / DATA_NAME / filename
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(assets.save())
            log(f"{filename}: ghi {changed} câu ({destination.stat().st_size / 1048576:.1f} MB)")
            _verify(destination, filename, table, install, gen, ex)
    finally:
        for key, old in saved.items():
            if old is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old
        for name in MODULES:
            sys.modules.pop(name, None)


def _verify(path: Path, filename: str, table: dict[str, str], install: Path, gen, ex) -> None:
    """Đọc lại file vừa ghi, kiểm mọi term đã có đúng câu Việt."""
    import UnityPy

    env = UnityPy.Environment()
    env.typetree_generator = gen
    for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
        env.load_file(str(install / ex.DATA_NAME / extra))
    env.load_file(str(path), name=filename)
    for obj in ex.language_sources(env, filename):
        source = obj.read_typetree()["mSource"]
        column = ex.english_index(source)
        wrong = [term["Term"] for term in source["mTerms"] if term["Term"] in table and term["Languages"][column] != table[term["Term"]]]
        if wrong:
            raise SystemExit(f"{filename}: {len(wrong)} term không ghi được, ví dụ {wrong[0]}")


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    build(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
