"""Kiểm kê mọi TMP Font Asset của Potion Permit vào `fonts.json`.

Quét các file `.assets`, scene `level*` và bundle Addressables. Ghi tên font, nơi chứa,
số chữ, atlas, fallback, chữ Việt còn thiếu và cách xử lý. Session sau đọc `fonts.json`
thay vì quét lại. Chạy lại khi game cập nhật (dấu vân tay là sha1 của `catalog.json`).

    python games/potion-permit/tools/font/inventory.py
"""

from __future__ import annotations

import datetime
import hashlib
import io
import json
import sys
from pathlib import Path

import UnityPy

FONT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(FONT_DIR.parent))
sys.path.insert(0, str(FONT_DIR))

import pixel_glyphs as pg  # noqa: E402
from extract_strings import generator  # noqa: E402
from game_config import DATA_NAME, UNITY, original, require_install  # noqa: E402
from patch_font import BUNDLE_DIR, TARGET  # noqa: E402

OUT = FONT_DIR / "fonts.json"


def action(name: str) -> tuple[str, str]:
    if name == TARGET:
        return "compose", "font chính của mọi chữ trong game; ghép chữ Việt theo lưới điểm ảnh"
    if name.startswith("PixelMplus12-Latin_Supplement"):
        return "keep", "fallback có chữ Latin-1 (á â ê ô…), cùng họ; dùng làm nguồn dấu"
    if name.startswith("LanaPixel12-Latin_Extended"):
        return "keep", "fallback khác họ có ă đ ĩ ũ; chữ ghép trong font chính được tìm trước nên không còn dùng tới"
    if name == "LiberationSans SDF":
        return "keep", "font mặc định của TMP, không thấy chữ nào của game dùng"
    return "keep", "font Nhật, Hàn, Trung, Cyrillic hoặc ký hiệu"


def scan(install: Path) -> list[dict]:
    data = install / DATA_NAME
    gen = generator(install)
    files = sorted(p for p in data.iterdir() if p.suffix == ".assets" or (p.name.startswith("level") and not p.suffix))
    files += sorted((data / BUNDLE_DIR / "StandaloneWindows64").glob("*.bundle"))
    letters = pg.vietnamese_letters()
    found = []
    for path in files:
        env = UnityPy.Environment()
        env.typetree_generator = gen
        for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
            env.load_file(str(data / extra))
        env.load_file(str(original(path.relative_to(install))), name=path.name)
        fonts = {}
        for obj in env.objects:
            if obj.type.name != "MonoBehaviour" or obj.assets_file.name.startswith("globalgamemanagers"):
                continue
            try:
                tree = obj.read_typetree()
            except Exception:
                continue
            if "m_CharacterTable" in tree and "m_AtlasTextures" in tree:
                fonts[obj.path_id] = tree
        for path_id, tree in fonts.items():
            chars = {chr(item["m_Unicode"]) for item in tree["m_CharacterTable"]}
            todo, why = action(tree["m_Name"])
            found.append(
                {
                    "name": tree["m_Name"],
                    "file": path.relative_to(data).as_posix(),
                    "pathId": path_id,
                    "chars": len(chars),
                    "renderMode": tree.get("m_AtlasRenderMode"),
                    "atlas": {"width": tree["m_AtlasWidth"], "height": tree["m_AtlasHeight"], "padding": tree["m_AtlasPadding"]},
                    "pointSize": tree["m_FaceInfo"]["m_PointSize"],
                    "fallbacks": [fonts[item["m_PathID"]]["m_Name"] for item in tree.get("m_FallbackFontAssetTable") or [] if item["m_PathID"] in fonts],
                    "missingVi": len([char for char in letters if char not in chars]),
                    "action": todo,
                    "why": why,
                }
            )
    return found


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    install = require_install()
    catalog = install / DATA_NAME / BUNDLE_DIR / "catalog.json"
    fonts = scan(install)
    result = {
        "game": "potion-permit",
        "unity": UNITY,
        "catalogSha1": hashlib.sha1(original(catalog.relative_to(install)).read_bytes()).hexdigest(),
        "scanned": datetime.date.today().isoformat(),
        "note": "Sinh bởi tools/font/inventory.py. Không sửa tay.",
        "fonts": fonts,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(fonts)} font → {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
