"""Vẽ thử font đã vá trong `patch/` ra ảnh, để soát dấu mà không cần mở game.

    python games/patapon12-replay/tools/font/preview.py
    python games/patapon12-replay/tools/font/preview.py --name KakuPop

Ảnh ghi vào `games/patapon12-replay/build/font-preview/`. Thư mục `build/` không commit.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

import numpy as np
import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator

from bake_sdf import PREVIEW_DIR, render_preview
from inventory import PATCH, UNITY, load

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import extract_strings as ex  # noqa: E402
from game_config import DATA_NAME, require_install  # noqa: E402

SAMPLE = (
    "Ta biết ngươi sẽ đến, hỡi Người Chỉ Huy!\n"
    "Chẳng bao lâu tới đêm, và yến tiệc bắt đầu.\n"
    "«Tiến lên!» Ấ Ầ Ẩ Ẫ Ậ Ắ Ặ Ế Ệ Ố Ộ Ớ Ợ Ứ Ự Đ\n"
    "ấ ầ ẩ ẫ ậ ắ ằ ẳ ẵ ặ ế ề ể ễ ệ ố ồ ổ ỗ ộ ớ ờ ở ỡ ợ ứ ừ ử ữ ự đ ỳ ỵ"
)


def open_patched(where: str, install: Path, gen, hashes: list[bytes]):
    if where.endswith(".bundle"):
        return ex.open_bundle(PATCH / ex.BUNDLES.relative_to(install) / where, hashes)
    data = install / DATA_NAME
    env = UnityPy.Environment()
    env.typetree_generator = gen
    for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
        env.load_file(str(data / extra))
    env.load_file(str(PATCH / DATA_NAME / where), name=where)
    stream = data / f"{where}.resS"
    if stream.is_file():
        env.load_file(str(stream), name=stream.name)
    return env


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--name", default="", help="chỉ vẽ font có tên chứa chuỗi này")
    parser.add_argument("--text", default=SAMPLE, help="câu mẫu, dùng \\n để xuống dòng")
    args = parser.parse_args()
    install = require_install()
    targets = [item for item in load()["fonts"] if item["action"] != "keep" and args.name in item["name"]]
    gen = TypeTreeGenerator(UNITY, "AssetStudio")
    gen.load_local_game(str(install))
    hashes = ex.load_hashes()
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    groups: dict[str, list[dict]] = {}
    for item in targets:
        groups.setdefault(item.get("file") or item["bundle"], []).append(item)
    for where, items in sorted(groups.items()):
        env = open_patched(where, install, gen, hashes)
        objects = {(obj.assets_file.name, obj.path_id): obj for obj in env.objects}
        for item in items:
            tree = objects[(item["serialized"], item["pathId"])].read_typetree()
            texture = objects[(item["serialized"], int(tree["m_AtlasTextures"][0]["m_PathID"]))].read()
            atlas = np.array(texture.image.convert("RGBA"))[..., 3]
            face = tree["m_FaceInfo"]
            baked = {
                "characters": tree["m_CharacterTable"],
                "glyphs": tree["m_GlyphTable"],
                "atlas": atlas,
                "height": atlas.shape[0],
                "face": {
                    "lineHeight": face["m_LineHeight"] * 1.25,
                    "ascentLine": face["m_AscentLine"] * 1.2,
                    "tabWidth": face["m_TabWidth"],
                },
            }
            name = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{item['name']}-{where[:8]}")
            render_preview(baked, args.text.replace("\\n", "\n"), PREVIEW_DIR / f"{name}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
