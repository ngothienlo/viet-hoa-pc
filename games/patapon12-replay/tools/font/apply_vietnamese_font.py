"""Vá font của PATAPON 1+2 REPLAY để chữ Việt hiện đủ và cùng một mặt chữ.

Danh sách font cần vá lấy từ `fonts.json` (sinh bởi `inventory.py`):

- `compose`: giữ nét gốc (TTake, TShinGo, KakuPop, Londrina), ghép thêm chữ Việt bằng `compose_glyphs.py`.
- `replace-regular` / `replace-bold`: thay cả bảng glyph và atlas bằng Be Vietnam Pro, cho font thiếu chữ gốc để ghép.

Luôn đọc file gốc (qua `original()`), kể cả khi launcher đã áp bản vá cũ.
File vá ghi vào `patch/`, giữ đúng đường dẫn tương đối với thư mục cài.
Không thêm font fallback. Không đụng font Nhật, Hàn, Trung.

    python games/patapon12-replay/tools/font/apply_vietnamese_font.py
    python games/patapon12-replay/tools/font/apply_vietnamese_font.py --no-install
"""

from __future__ import annotations

import argparse
import gc
import io
import sys
from pathlib import Path

import numpy as np
import UnityPy
from PIL import Image
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator

from bake_sdf import PADDING, POINT, bake, collect_codepoints
from compose_glyphs import Composer, vietnamese_letters
from inventory import PATCH, UNITY, check, load, vi_chars

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import extract_strings as ex  # noqa: E402
from game_config import DATA_NAME, ROOT, font_path, original, require_install  # noqa: E402

sys.path.insert(0, str(ROOT))

# Font làm chủ atlas chung khi nhiều font trong một file cùng được thay.
HOST_PREFER = {
    "regular": ("TShinGoPr6-Medium SDF", "TShinGoPr6-Medium SDF_mission", "TShinGoPr6-Regular SDF"),
    "bold": ("TTakeStd-Bold SDF", "TTakeStd-Bold_hcs"),
}
# Font nhỏ (chỉ có chữ và số) mượn dấu của font lớn cùng họ, theo tiền tố tên.
DONORS = {
    "TTakeStd": ("sharedassets5.assets", "TTakeStd-Bold SDF"),
    "TShinGoPr6": ("sharedassets1.assets", "TShinGoPr6-Medium SDF"),
    "DF-KakuPop": ("sharedassets1.assets", "DF-KakuPop-W5 SDF_Padding14_Take"),
    "LondrinaSolid": ("sharedassets1.assets", "DF-KakuPop-W5 SDF_Padding14_Take"),
}
ALPHA8 = 1
TMP_SDFAA = 4165


# Đọc và ghi atlas -------------------------------------------------------


def read_alpha(texture_obj) -> np.ndarray:
    tex = texture_obj.read()
    return np.array(tex.image.convert("RGBA"))[..., 3].copy()


def write_alpha(texture_obj, alpha: np.ndarray) -> None:
    tex = texture_obj.read()
    rgba = np.zeros((alpha.shape[0], alpha.shape[1], 4), np.uint8)
    rgba[..., 0:3] = 255
    rgba[..., 3] = alpha
    tex.set_image(Image.fromarray(rgba, "RGBA"), target_format=ALPHA8)
    tex.save()


# Thay bằng Be Vietnam Pro ----------------------------------------------


def _fill_face(tree: dict, baked: dict) -> None:
    face = tree["m_FaceInfo"]
    src = baked["face"]
    face["m_PointSize"] = src["pointSize"]
    face["m_Scale"] = 1.0
    face["m_UnitsPerEM"] = src["unitsPerEM"]
    face["m_LineHeight"] = src["lineHeight"]
    face["m_AscentLine"] = src["ascentLine"]
    face["m_CapLine"] = src["capLine"]
    face["m_MeanLine"] = src["meanLine"]
    face["m_Baseline"] = 0.0
    face["m_DescentLine"] = src["descentLine"]
    face["m_UnderlineOffset"] = src["underlineOffset"]
    face["m_UnderlineThickness"] = src["underlineThickness"]
    face["m_StrikethroughOffset"] = src["strikethroughOffset"]
    face["m_StrikethroughThickness"] = src["strikethroughThickness"]
    face["m_TabWidth"] = src["tabWidth"]


def replace_font(tree: dict, baked: dict, atlas_pid: int) -> int:
    """Ghi bảng glyph Be Vietnam Pro vào font. Trả path id của atlas cũ."""
    old = int(tree["m_AtlasTextures"][0]["m_PathID"])
    _fill_face(tree, baked)
    tree["m_GlyphTable"] = baked["glyphs"]
    tree["m_CharacterTable"] = baked["characters"]
    tree["m_UsedGlyphRects"] = baked["usedRects"]
    tree["m_FreeGlyphRects"] = baked["freeRects"]
    tree["m_glyphInfoList"] = []
    tree["m_AtlasWidth"] = baked["width"]
    tree["m_AtlasHeight"] = baked["height"]
    tree["m_AtlasPadding"] = baked["padding"]
    tree["m_AtlasRenderMode"] = TMP_SDFAA
    tree["m_AtlasPopulationMode"] = 0
    tree["m_AtlasTextureIndex"] = 0
    tree["m_IsMultiAtlasTexturesEnabled"] = False
    tree["m_FallbackFontAssetTable"] = []
    tree["fallbackFontAssets"] = []
    tree["m_AtlasTextures"] = [{"m_FileID": 0, "m_PathID": atlas_pid}]
    for row in tree.get("m_FontWeightTable") or []:
        for key in ("regularTypeface", "italicTypeface"):
            row[key]["m_FileID"] = 0
            row[key]["m_PathID"] = 0
    settings = tree.get("m_CreationSettings") or {}
    settings["pointSize"] = POINT
    settings["padding"] = baked["padding"]
    settings["atlasWidth"] = baked["width"]
    settings["atlasHeight"] = baked["height"]
    settings["renderMode"] = TMP_SDFAA
    return old


# Material --------------------------------------------------------------


def _pair(item):
    if isinstance(item, dict) and "first" in item:
        return item["first"], item["second"]
    if isinstance(item, (list, tuple)) and len(item) == 2:
        return item[0], item[1]
    return None, None


def retarget_materials(env, owners: set[str], redirect: dict[tuple[str, int], tuple[int, int, int, float | None]]) -> int:
    """Trỏ material sang atlas mới và sửa kích thước atlas trong material.

    redirect: (file, path id atlas cũ) -> (path id atlas mới, rộng, cao, gradient scale hoặc None).
    """
    changed = 0
    for obj in env.objects:
        if obj.type.name != "Material" or obj.assets_file.name not in owners:
            continue
        tree = obj.read_typetree()
        saved = tree.get("m_SavedProperties") or {}
        target = None
        for item in saved.get("m_TexEnvs") or []:
            name, info = _pair(item)
            if name != "_MainTex" or not isinstance(info, dict):
                continue
            tex = info["m_Texture"]
            if tex.get("m_FileID"):
                continue
            found = redirect.get((obj.assets_file.name, int(tex.get("m_PathID") or 0)))
            if found:
                tex["m_PathID"] = found[0]
                target = found
        if target is None:
            continue
        _pid, width, height, gradient = target
        updates = {"_TextureWidth": float(width), "_TextureHeight": float(height)}
        if gradient is not None:
            updates["_GradientScale"] = gradient
        floats = []
        for item in saved.get("m_Floats") or []:
            name, _value = _pair(item)
            if name in updates and isinstance(item, dict):
                item["second"] = updates[name]
                floats.append(item)
            elif name in updates:
                floats.append((name, updates[name]))
            else:
                floats.append(item)
        saved["m_Floats"] = floats
        obj.save_typetree(tree)
        changed += 1
    return changed


# Vá một file -----------------------------------------------------------


def patch_fonts(env, items: list[dict], baked: dict[str, dict], chars: list[str], donors: Donors) -> int:
    """Vá các font trong `items`. Mọi font của một lần gọi nằm trong cùng env."""
    objects = {(obj.assets_file.name, obj.path_id): obj for obj in env.objects}
    owners = {item["serialized"] for item in items}
    redirect: dict[tuple[str, int], tuple[int, int, int, float | None]] = {}
    patched = 0

    for kind in ("regular", "bold"):
        for owner in sorted(owners):
            group = [item for item in items if item["action"] == f"replace-{kind}" and item["serialized"] == owner]
            if not group:
                continue
            host = next((item for name in HOST_PREFER[kind] for item in group if item["name"] == name), group[0])
            host_tree = objects[(owner, host["pathId"])].read_typetree()
            host_pid = int(host_tree["m_AtlasTextures"][0]["m_PathID"])
            write_alpha(objects[(owner, host_pid)], baked[kind]["atlas"])
            for item in group:
                obj = objects[(owner, item["pathId"])]
                tree = obj.read_typetree()
                old = replace_font(tree, baked[kind], host_pid)
                obj.save_typetree(tree)
                redirect[(owner, old)] = (host_pid, baked[kind]["width"], baked[kind]["height"], float(PADDING + 1))
                print(f"  {item['name']}: Be Vietnam Pro {kind}")
                patched += 1

    for item in items:
        if item["action"] != "compose":
            continue
        owner = item["serialized"]
        obj = objects[(owner, item["pathId"])]
        tree = obj.read_typetree()
        atlas_pid = int(tree["m_AtlasTextures"][0]["m_PathID"])
        texture = objects[(owner, atlas_pid)]
        composer = Composer(tree, read_alpha(texture), donors.for_font(item["name"]))
        result = composer.build(chars)
        if not result["added"]:
            continue
        atlas = result["atlas"]
        write_alpha(texture, atlas)
        tree["m_GlyphTable"] = result["glyphs"]
        tree["m_CharacterTable"] = result["characters"]
        tree["m_UsedGlyphRects"] = result["used"]
        tree["m_FreeGlyphRects"] = []
        tree["m_AtlasHeight"] = int(atlas.shape[0])
        settings = tree.get("m_CreationSettings") or {}
        settings["atlasHeight"] = int(atlas.shape[0])
        obj.save_typetree(tree)
        redirect[(owner, atlas_pid)] = (atlas_pid, int(atlas.shape[1]), int(atlas.shape[0]), None)
        skipped = "".join(result["skipped"])
        print(f"  {item['name']}: ghép {len(result['added'])} chữ" + (f", không ghép được {skipped!r}" if skipped else ""))
        patched += 1

    materials = retarget_materials(env, owners, redirect)
    print(f"  material: {materials}")
    if redirect and materials == 0:
        raise SystemExit("Không sửa được material nào. Atlas mới sẽ không hiện.")
    return patched


def open_data_file(filename: str, gen, install: Path):
    """Mở file gốc của bản build, kèm globalgamemanagers và resS để đọc atlas."""
    data = install / DATA_NAME
    env = UnityPy.Environment()
    env.typetree_generator = gen
    for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
        env.load_file(str(data / extra))
    env.load_file(str(original(Path(DATA_NAME) / filename)), name=filename)
    stream = data / f"{filename}.resS"
    if stream.is_file():
        env.load_file(str(stream), name=stream.name)
    return env


class Donors:
    """Nạp font cho mượn dấu khi cần, mỗi font một lần."""

    def __init__(self, fonts: list[dict], gen, install: Path) -> None:
        self.fonts = fonts
        self.gen = gen
        self.install = install
        self.cache: dict[tuple[str, str], Composer] = {}

    def for_font(self, name: str) -> Composer | None:
        key = next((DONORS[prefix] for prefix in DONORS if name.startswith(prefix)), None)
        if key is None or key[1] == name:
            return None
        if key not in self.cache:
            filename, donor_name = key
            item = next(row for row in self.fonts if row.get("file") == filename and row["name"] == donor_name)
            env = open_data_file(filename, self.gen, self.install)
            objects = {(obj.assets_file.name, obj.path_id): obj for obj in env.objects}
            tree = objects[(filename, item["pathId"])].read_typetree()
            atlas = objects[(filename, int(tree["m_AtlasTextures"][0]["m_PathID"]))]
            self.cache[key] = Composer(tree, read_alpha(atlas))
        return self.cache[key]


def patch_data_file(filename: str, items: list[dict], baked: dict, chars: list[str], donors: Donors, gen, install: Path) -> Path:
    env = open_data_file(filename, gen, install)
    patch_fonts(env, items, baked, chars, donors)
    assets = next(obj.assets_file for obj in env.objects if obj.assets_file.name == filename)
    destination = PATCH / DATA_NAME / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(assets.save())
    print(f"  ghi {destination.name} ({destination.stat().st_size / 1048576:.1f} MB)")
    return destination


def patch_bundle(filename: str, items: list[dict], baked: dict, chars: list[str], donors: Donors, hashes: list[bytes], install: Path) -> Path:
    if filename in ex.HINTS.values():
        raise SystemExit(f"{filename} cũng là bundle LocalizeData. Cần gộp hai bản vá trước khi ghi.")
    source = ex.original_bundle(filename)
    key = ex.bundle_key(source, hashes)
    env = ex.open_bundle(source, hashes)
    patch_fonts(env, items, baked, chars, donors)
    destination = PATCH / ex.BUNDLES.relative_to(install) / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(ex.save_bundle(env, key))
    print(f"  ghi {destination.name} ({destination.stat().st_size / 1048576:.1f} MB)")
    return destination


def install_patch(install: Path) -> None:
    from launcher.apply import apply_pack
    from launcher.catalog import load_games
    from launcher.store import Store, default_state_dir

    game = next(item for item in load_games(ROOT) if item.id == "patapon12-replay")
    result = apply_pack(game, install, Store(default_state_dir()))
    print(result.message)
    if not result.ok:
        raise SystemExit(result.message)


def build_fonts() -> None:
    """Vá mọi font trong fonts.json, ghi vào patch_dir(), rồi kiểm tra. Không áp lên bản cài."""
    install = require_install()
    payload = load()
    targets = [item for item in payload["fonts"] if item["action"] != "keep"]
    groups: dict[str, list[dict]] = {}
    for item in targets:
        groups.setdefault(item.get("file") or item["bundle"], []).append(item)

    baked: dict[str, dict] = {}
    if any(item["action"].startswith("replace-") for item in targets):
        codes = collect_codepoints()
        print("nướng atlas Be Vietnam Pro,", len(codes), "mã")
        baked["regular"] = bake(font_path("regular"), codes, 4096, 4096, bold=False)
        baked["bold"] = bake(font_path("bold"), codes, 4096, 2048, bold=True)
    chars = sorted(set(vietnamese_letters()) | vi_chars())

    gen = TypeTreeGenerator(UNITY, "AssetStudio")
    gen.load_local_game(str(install))
    hashes = ex.load_hashes()
    donors = Donors(payload["fonts"], gen, install)
    for where, items in sorted(groups.items()):
        print(where)
        if where.endswith(".bundle"):
            patch_bundle(where, items, baked, chars, donors, hashes, install)
        else:
            patch_data_file(where, items, baked, chars, donors, gen, install)
        gc.collect()

    print("kiểm tra bản vá")
    if check(vi_chars()):
        raise SystemExit("Còn font thiếu chữ. Xem danh sách ở trên.")


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-install", action="store_true", help="chỉ ghi patch/, không áp lên bản cài")
    args = parser.parse_args()
    build_fonts()
    if not args.no_install:
        install_patch(require_install())
    return 0


if __name__ == "__main__":
    sys.exit(main())
