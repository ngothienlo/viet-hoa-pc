"""Ghi atlas Be Vietnam Pro vào font Latin của PATAPON 1+2 REPLAY.

Không thêm font fallback. Không đụng font Nhật, Hàn, Trung.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import UnityPy
from PIL import Image
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator

from bake_sdf import POINT, bake, collect_codepoints, font_path, install_dir

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

GAME = install_dir()
DATA = GAME / "PATAPON12_REPLAY_Data"
PATCH = ROOT / "games" / "patapon12-replay" / "patch" / "PATAPON12_REPLAY_Data"

REGULAR_NAMES = {
    "TShinGoPr6-Medium SDF",
    "TShinGoPr6-Medium SDF_mission",
    "TShinGoPr6-Medium_launcher_fs",
    "TShinGoPr6-Medium_launcher_hcs",
    "TShinGoPr6-Medium_launcher_sp",
    "TShinGoPr6-Medium_savewindow",
    "TShinGoPr6-Medium_launcher_fc_bossrush",
}
BOLD_NAMES = {
    "TTakeStd-Bold SDF",
    "TTakeStd-Bold_fs",
    "TTakeStd-Bold_hcs",
    "TTakeStd-Bold SDF_fullwidth_number",
    "TTakeStd-Bold SDF_symbol",
}
HOST_PREFER = {
    "regular": ("TShinGoPr6-Medium SDF", "TShinGoPr6-Medium SDF_mission"),
    "bold": ("TTakeStd-Bold SDF", "TTakeStd-Bold_hcs", "TTakeStd-Bold_fs"),
}
FILES = ("sharedassets0.assets", "sharedassets1.assets", "sharedassets5.assets")


def _kind(name: str) -> str | None:
    if "_ja" in name:
        return None
    if name in REGULAR_NAMES:
        return "regular"
    if name in BOLD_NAMES:
        return "bold"
    return None


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


def _apply_font(tree: dict, baked: dict, atlas_pid: int) -> int:
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
    tree["m_AtlasRenderMode"] = 4165
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
    settings["renderMode"] = 4165
    return old


def _tex_name_info(item):
    if isinstance(item, dict) and "first" in item:
        return item["first"], item["second"]
    if isinstance(item, (list, tuple)) and len(item) == 2:
        return item[0], item[1]
    return None, None


def _retarget_materials(env, filename: str, redirect: dict[int, tuple[int, int, int]]) -> int:
    changed = 0
    for obj in env.objects:
        if obj.type.name != "Material" or not obj.assets_file.name.endswith(filename):
            continue
        tree = obj.read_typetree()
        saved = tree.get("m_SavedProperties") or {}
        new_size = None
        for item in saved.get("m_TexEnvs") or []:
            name, info = _tex_name_info(item)
            if name != "_MainTex" or not isinstance(info, dict):
                continue
            tex = info["m_Texture"]
            if tex.get("m_FileID"):
                continue
            found = redirect.get(int(tex.get("m_PathID") or 0))
            if not found:
                continue
            tex["m_PathID"] = found[0]
            new_size = found
        if new_size is None:
            continue
        _, width, height = new_size
        updates = {
            "_TextureWidth": float(width),
            "_TextureHeight": float(height),
            "_GradientScale": 15.0,
        }
        floats = []
        for item in saved.get("m_Floats") or []:
            if isinstance(item, dict) and item.get("first") in updates:
                item["second"] = updates[item["first"]]
                floats.append(item)
            elif isinstance(item, tuple) and item[0] in updates:
                floats.append((item[0], updates[item[0]]))
            else:
                floats.append(item)
        saved["m_Floats"] = floats
        obj.save_typetree(tree)
        changed += 1
        print(f"  material {tree.get('m_Name')} -> {width}x{height}")
    return changed


def _write_atlas(env, filename: str, path_id: int, baked: dict) -> None:
    obj = next(
        item
        for item in env.objects
        if item.type.name == "Texture2D"
        and item.path_id == path_id
        and item.assets_file.name.endswith(filename)
    )
    tex = obj.read()
    alpha = baked["atlas"]
    rgba = np.zeros((alpha.shape[0], alpha.shape[1], 4), np.uint8)
    rgba[..., 0:3] = 255
    rgba[..., 3] = alpha
    tex.set_image(Image.fromarray(rgba, "RGBA"), target_format=1)
    tex.save()


def patch_file(filename: str, regular: dict, bold: dict, gen: TypeTreeGenerator) -> Path:
    env = UnityPy.Environment()
    env.typetree_generator = gen
    env.load_file(str(DATA / "globalgamemanagers.assets"))
    env.load_file(str(DATA / "globalgamemanagers"))
    env.load_file(str(DATA / filename))
    baked_for = {"regular": regular, "bold": bold}
    found = []
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour" or not obj.assets_file.name.endswith(filename):
            continue
        try:
            head = obj.parse_monobehaviour_head()
            script = head.m_Script.deref_parse_as_object()
        except Exception:
            continue
        if script.m_ClassName != "TMP_FontAsset":
            continue
        tree = obj.read_typetree()
        kind = _kind(tree.get("m_Name") or "")
        if kind is None:
            continue
        found.append((obj, tree, kind, tree["m_Name"]))
    if not found:
        raise SystemExit(f"{filename} không có font Latin cần vá")

    redirect: dict[int, tuple[int, int, int]] = {}
    for kind in ("regular", "bold"):
        group = [item for item in found if item[2] == kind]
        if not group:
            continue
        host = group[0]
        for prefer in HOST_PREFER[kind]:
            match = [item for item in group if item[3] == prefer]
            if match:
                host = match[0]
                break
        host_pid = int(host[1]["m_AtlasTextures"][0]["m_PathID"])
        baked = baked_for[kind]
        _write_atlas(env, filename, host_pid, baked)
        for obj, tree, _kind_name, name in group:
            old = _apply_font(tree, baked, host_pid)
            obj.save_typetree(tree)
            redirect[old] = (host_pid, baked["width"], baked["height"])
            print(f"  {name} -> texture {host_pid}")
    materials = _retarget_materials(env, filename, redirect)
    print(f"  material {materials}")
    if materials == 0:
        raise SystemExit(f"{filename} không sửa material nào")
    assets = next(obj.assets_file for obj, *_rest in found)
    blob = assets.save()
    destination = PATCH / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(blob)
    print(f"  ghi {destination} ({len(blob) / 1048576:.1f} MB)")
    return destination


def verify(path: Path, gen: TypeTreeGenerator) -> None:
    env = UnityPy.Environment()
    env.typetree_generator = gen
    env.load_file(str(DATA / "globalgamemanagers.assets"))
    env.load_file(str(DATA / "globalgamemanagers"))
    env.load_file(str(path))
    wanted = 0x1EDB  # ớ
    hits = []
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour" or obj.assets_file.name != path.name:
            continue
        try:
            head = obj.parse_monobehaviour_head()
            script = head.m_Script.deref_parse_as_object()
        except Exception:
            continue
        if script.m_ClassName != "TMP_FontAsset":
            continue
        tree = obj.read_typetree()
        if _kind(tree.get("m_Name") or "") is None:
            continue
        codes = {item["m_Unicode"] for item in tree["m_CharacterTable"]}
        if wanted not in codes:
            raise SystemExit(f"{path.name} {tree['m_Name']} không có ớ")
        atlas_pid = tree["m_AtlasTextures"][0]["m_PathID"]
        tex = next(
            item.read()
            for item in env.objects
            if item.type.name == "Texture2D" and item.path_id == atlas_pid and item.assets_file.name == path.name
        )
        if tex.m_StreamData and tex.m_StreamData.size:
            raise SystemExit(f"{tree['m_Name']} vẫn trỏ atlas cũ trong resS")
        if (tex.m_Width, tex.m_Height) != (tree["m_AtlasWidth"], tree["m_AtlasHeight"]):
            raise SystemExit(f"{tree['m_Name']} lệch kích thước atlas")
        hits.append(tree["m_Name"])
    if not hits:
        raise SystemExit(f"{path.name} không đọc lại được font")
    print("  đọc lại", ", ".join(hits))


def install_patch() -> None:
    from launcher.apply import apply_pack
    from launcher.catalog import load_games
    from launcher.store import Store, default_state_dir

    game = next(item for item in load_games(ROOT) if item.id == "patapon12-replay")
    result = apply_pack(game, GAME, Store(default_state_dir()))
    print(result.message)
    if not result.ok:
        raise SystemExit(result.message)


def main() -> None:
    codes = collect_codepoints()
    print("nướng atlas", len(codes), "mã")
    regular = bake(font_path("regular"), codes, 4096, 4096, bold=False)
    bold = bake(font_path("bold"), codes, 4096, 2048, bold=True)
    gen = TypeTreeGenerator("2022.3.52f1", "AssetStudio")
    gen.load_local_game(str(GAME))
    written = []
    for filename in FILES:
        print(filename)
        written.append(patch_file(filename, regular, bold, gen))
    for path in written:
        verify(path, gen)
    install_patch()


if __name__ == "__main__":
    main()
