"""Thêm chữ Việt vào font pixel `PixelMplus12-Regular` của Potion Permit.

Font này có hai bản: trong `resources.assets` và trong bundle `prefab-battle`. Cả hai
được vá như nhau: ghép chữ (xem `pixel_glyphs.py`), tính SDF, nới atlas lên phía trên
rồi xếp glyph mới vào phần nới, sửa bảng glyph và material.

Addressables kiểm CRC của bundle khi nạp, nên `catalog.json` cũng phải sửa: CRC của
bundle đã vá đổi thành 0 (không kiểm), giữ nguyên độ dài chuỗi.

`build_patch.py` gọi `patch(install, out, gen, log)`. Chạy riêng để xem thử:

    python games/potion-permit/tools/font/patch_font.py --preview <ảnh.png> "Chào Dược sư!"
"""

from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path
from typing import Callable

import numpy as np
import UnityPy
from PIL import Image
from scipy.ndimage import distance_transform_edt
from UnityPy.enums import TextureFormat

FONT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(FONT_DIR))

import pixel_glyphs as pg  # noqa: E402

TARGET = "PixelMplus12-Regular"
DONOR = "PixelMplus12-Latin_Supplement_PP"
RESOURCES = "resources.assets"
BUNDLE_DIR = Path("StreamingAssets") / "aa" / "Windows"
BUNDLE_PREFIX = "prefab-battle_assets_all_"
CATALOG = BUNDLE_DIR / "catalog.json"
# Khoảng trống giữa các glyph mới, ngoài viền padding của từng glyph.
GAP = 2
STEP = 64


# Đọc ---------------------------------------------------------------------


def font_assets(env) -> dict[str, tuple]:
    """Tên font -> (object, typetree) của mọi TMP Font Asset trong env."""
    found = {}
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        try:
            tree = obj.read_typetree()
        except Exception:
            continue
        if "m_CharacterTable" in tree and "m_AtlasTextures" in tree:
            found[tree["m_Name"]] = (obj, tree)
    return found


def texture_of(env, obj, tree):
    pid = int(tree["m_AtlasTextures"][0]["m_PathID"])
    return next(item for item in env.objects if item.assets_file is obj.assets_file and item.path_id == pid)


def read_alpha(texture_obj) -> np.ndarray:
    return np.array(texture_obj.read().image.convert("RGBA"))[..., 3].copy()


def glyph_masks(tree: dict, alpha: np.ndarray) -> dict[str, pg.Glyph]:
    """Hình từng chữ, cắt ở mức 0.5 của trường SDF, đặt lên khung của `pixel_glyphs`."""
    glyphs = {item["m_Index"]: item for item in tree["m_GlyphTable"]}
    height = alpha.shape[0]
    out = {}
    for char in tree["m_CharacterTable"]:
        glyph = glyphs[char["m_GlyphIndex"]]
        rect = glyph["m_GlyphRect"]
        metrics = glyph["m_Metrics"]
        mask = pg.blank()
        if rect["m_Width"] and rect["m_Height"]:
            top = height - (rect["m_Y"] + rect["m_Height"])
            ink = alpha[top : top + rect["m_Height"], rect["m_X"] : rect["m_X"] + rect["m_Width"]] >= 128
            for row, col in zip(*np.nonzero(ink)):
                pg.set_unit(mask, int(metrics["m_HorizontalBearingX"]) + int(col), int(metrics["m_HorizontalBearingY"]) - int(row) - 1)
        out[chr(char["m_Unicode"])] = pg.Glyph(mask, float(metrics["m_HorizontalAdvance"]))
    return out


# SDF và xếp atlas ----------------------------------------------------------


def crop(mask: np.ndarray) -> tuple[np.ndarray, int, int]:
    """Cắt sát nét. Trả hình, x trái và y đỉnh (mép trên, không tính hàng đỉnh)."""
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    part = mask[rows[0] : rows[-1] + 1, cols[0] : cols[-1] + 1]
    return part, int(cols[0]) + pg.XMIN, pg.YMAX - int(rows[0])


def sdf(mask: np.ndarray, pad: int) -> np.ndarray:
    """Trường SDF 0..255 kể cả viền pad, theo quy ước TMP: cạnh ở 0.5.

    Khoảng cách đo từ tâm ô tới mép nét, nên trừ nửa ô. So với glyph gốc của game,
    cách này lệch trung bình khoảng 2%; không trừ thì lệch gần 4%.
    """
    canvas = np.zeros((mask.shape[0] + 2 * pad, mask.shape[1] + 2 * pad), bool)
    canvas[pad : pad + mask.shape[0], pad : pad + mask.shape[1]] = mask
    signed = np.where(canvas, distance_transform_edt(canvas) - 0.5, 0.5 - distance_transform_edt(~canvas))
    return np.clip(np.round((signed / (2 * pad) + 0.5) * 255), 0, 255).astype(np.uint8)


def shelf_pack(fields: list[np.ndarray], width: int, height: int) -> list[tuple[int, int]] | None:
    x = y = GAP
    row = 0
    placed = []
    for field in fields:
        h, w = field.shape
        if x + w + GAP > width:
            x = GAP
            y += row + GAP
            row = 0
        if y + h + GAP > height:
            return None
        placed.append((x, y))
        x += w + GAP
        row = max(row, h)
    return placed


def add_glyphs(tree: dict, alpha: np.ndarray, new: dict[str, pg.Glyph]) -> np.ndarray:
    """Ghi glyph mới vào `tree`, trả atlas mới (atlas cũ giữ ở đáy nên rect cũ không đổi)."""
    pad = int(tree["m_AtlasPadding"])
    items = []
    for char in sorted(new):
        part, left, top = crop(new[char].mask)
        items.append((char, part, left, top, sdf(part, pad), new[char].advance))
    items.sort(key=lambda item: -item[4].shape[0])
    width = alpha.shape[1]
    extra = STEP
    while (placed := shelf_pack([item[4] for item in items], width, extra)) is None:
        extra += STEP
    total = alpha.shape[0] + extra
    atlas = np.zeros((total, width), np.uint8)
    atlas[extra:, :] = alpha
    index = max(item["m_Index"] for item in tree["m_GlyphTable"]) + 1
    for (char, part, left, top, field, advance), (x, y) in zip(items, placed):
        h, w = field.shape
        atlas[y : y + h, x : x + w] = field
        rect = {"m_X": x + pad, "m_Y": total - (y + h) + pad, "m_Width": part.shape[1], "m_Height": part.shape[0]}
        tree["m_GlyphTable"].append(
            {
                "m_Index": index,
                "m_Metrics": {
                    "m_Width": float(rect["m_Width"]),
                    "m_Height": float(rect["m_Height"]),
                    "m_HorizontalBearingX": float(left),
                    "m_HorizontalBearingY": float(top),
                    "m_HorizontalAdvance": float(advance),
                },
                "m_GlyphRect": rect,
                "m_Scale": 1.0,
                "m_AtlasIndex": 0,
            }
        )
        tree["m_CharacterTable"].append({"m_ElementType": 1, "m_Unicode": ord(char), "m_GlyphIndex": index, "m_Scale": 1.0})
        tree.setdefault("m_UsedGlyphRects", []).append(
            {"m_X": rect["m_X"] - pad, "m_Y": rect["m_Y"] - pad, "m_Width": w, "m_Height": h}
        )
        index += 1
    tree["m_FreeGlyphRects"] = []
    tree["m_AtlasHeight"] = total
    if isinstance(tree.get("m_CreationSettings"), dict):
        tree["m_CreationSettings"]["atlasHeight"] = total
    return atlas


# Ghi -----------------------------------------------------------------------


def long_path(path: Path) -> Path:
    """Đường dẫn bundle dài khoảng 130 ký tự. Thư mục ra sâu thì vượt 260 ký tự của Windows."""
    text = str(path.resolve())
    if sys.platform == "win32" and len(text) >= 240 and not text.startswith("\\\\?\\"):
        return Path("\\\\?\\" + text)
    return path


def write_alpha(texture_obj, alpha: np.ndarray) -> None:
    tex = texture_obj.read()
    rgba = np.zeros((alpha.shape[0], alpha.shape[1], 4), np.uint8)
    rgba[..., 0:3] = 255
    rgba[..., 3] = alpha
    tex.set_image(Image.fromarray(rgba, "RGBA"), target_format=TextureFormat.Alpha8)
    tex.save()


def _pair(item):
    if isinstance(item, dict):
        return item.get("first"), item.get("second")
    return item[0], item[1]


def retarget_materials(env, atlas_obj, height: int) -> int:
    """Sửa `_TextureHeight` của mọi material vẽ bằng atlas này."""
    changed = 0
    for obj in env.objects:
        if obj.type.name != "Material" or obj.assets_file is not atlas_obj.assets_file:
            continue
        tree = obj.read_typetree()
        saved = tree.get("m_SavedProperties") or {}
        uses = False
        for item in saved.get("m_TexEnvs") or []:
            name, info = _pair(item)
            texture = info.get("m_Texture") if isinstance(info, dict) else None
            if name == "_MainTex" and texture and not texture.get("m_FileID") and int(texture.get("m_PathID") or 0) == atlas_obj.path_id:
                uses = True
        if not uses:
            continue
        floats = []
        for item in saved.get("m_Floats") or []:
            name, _value = _pair(item)
            if name == "_TextureHeight":
                item = {"first": name, "second": float(height)} if isinstance(item, dict) else (name, float(height))
            floats.append(item)
        saved["m_Floats"] = floats
        obj.save_typetree(tree)
        changed += 1
    return changed


def patch_env(env, log: Callable[[str], None]) -> list[str]:
    """Vá font đích trong env. Trả danh sách chữ đã thêm."""
    fonts = font_assets(env)
    if TARGET not in fonts or DONOR not in fonts:
        raise SystemExit(f"Không thấy {TARGET} hoặc {DONOR}. Bản game khác bản đã kiểm kê trong fonts.json.")
    obj, tree = fonts[TARGET]
    donor_obj, donor_tree = fonts[DONOR]
    texture = texture_of(env, obj, tree)
    alpha = read_alpha(texture)
    regular = glyph_masks(tree, alpha)
    latin = glyph_masks(donor_tree, read_alpha(texture_of(env, donor_obj, donor_tree)))
    new = pg.compose(regular, latin)
    missing = [char for char in pg.vietnamese_letters() if char not in regular and char not in latin and char not in new]
    if missing:
        raise SystemExit(f"Không ghép được: {''.join(missing)}")
    atlas = add_glyphs(tree, alpha, new)
    write_alpha(texture, atlas)
    obj.save_typetree(tree)
    materials = retarget_materials(env, texture, atlas.shape[0])
    if materials == 0:
        raise SystemExit(f"{TARGET}: không sửa được material nào, atlas mới sẽ không hiện.")
    log(f"{TARGET}: thêm {len(new)} chữ, atlas {atlas.shape[1]}x{atlas.shape[0]}, {materials} material")
    return sorted(new)


def clear_crc(catalog: bytes, bundle_hash: str) -> bytes:
    """Đổi CRC của một bundle trong catalog Addressables thành 0, giữ nguyên độ dài."""
    data = json.loads(catalog.decode("utf-8"))
    extra = bytearray(base64.b64decode(data["m_ExtraDataString"]))
    at = extra.find(bundle_hash.encode("utf-16-le"))
    if at < 0:
        raise SystemExit(f"catalog.json không có bundle {bundle_hash}")
    key = '"m_Crc":'.encode("utf-16-le")
    start = extra.find(key, at) + len(key)
    end = start
    while extra[end : end + 2].decode("utf-16-le", errors="replace").isdigit():
        end += 2
    digits = (end - start) // 2
    extra[start:end] = ("0" + " " * (digits - 1)).encode("utf-16-le")
    data["m_ExtraDataString"] = base64.b64encode(bytes(extra)).decode("ascii")
    return json.dumps(data, separators=(",", ":")).encode("utf-8")


def patch(install: Path, out: Path, gen, log: Callable[[str], None], original: Callable[[Path], Path]) -> list[Path]:
    """Ghi `resources.assets`, bundle `prefab-battle` và `catalog.json` đã vá vào `out`."""
    from game_config import DATA_NAME

    data = install / DATA_NAME
    written = []

    env = UnityPy.Environment()
    env.typetree_generator = gen
    for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
        env.load_file(str(data / extra))
    env.load_file(str(original(Path(DATA_NAME) / RESOURCES)), name=RESOURCES)
    env.load_file(str(data / f"{RESOURCES}.resS"), name=f"{RESOURCES}.resS")
    patch_env(env, log)
    assets = next(obj.assets_file for obj in env.objects if obj.assets_file.name == RESOURCES)
    destination = long_path(out / DATA_NAME / RESOURCES)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(assets.save())
    written.append(destination)

    bundles = sorted((data / BUNDLE_DIR / "StandaloneWindows64").glob(f"{BUNDLE_PREFIX}*.bundle"))
    if len(bundles) != 1:
        raise SystemExit(f"Cần đúng một bundle {BUNDLE_PREFIX}*, thấy {len(bundles)}.")
    relative = bundles[0].relative_to(install)
    env = UnityPy.load(str(original(relative)))
    patch_env(env, log)
    destination = long_path(out / relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(next(iter(env.files.values())).save(packer="original"))
    written.append(destination)

    bundle_hash = bundles[0].stem.rsplit("_", 1)[-1]
    catalog = Path(DATA_NAME) / CATALOG
    destination = long_path(out / catalog)
    destination.write_bytes(clear_crc(original(catalog).read_bytes(), bundle_hash))
    written.append(destination)
    for path in written:
        log(f"{path.name}: {path.stat().st_size / 1048576:.1f} MB")
    return written


def verify(path: Path, gen=None, data: Path | None = None) -> None:
    """Đọc lại file đã vá: font đích phải có đủ chữ Việt, atlas đúng kích thước.

    File `.assets` cần `gen` và thư mục Data của bản cài (globalgamemanagers, `.resS`).
    """
    env = UnityPy.Environment()
    if gen is not None:
        env.typetree_generator = gen
    if data is not None:
        for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
            env.load_file(str(data / extra))
    env.load_file(path.read_bytes(), name=path.name)
    if data is not None:
        env.load_file(str(data / f"{path.name}.resS"), name=f"{path.name}.resS")
    fonts = font_assets(env)
    obj, tree = fonts[TARGET]
    have = {chr(item["m_Unicode"]) for item in tree["m_CharacterTable"]} | {
        chr(item["m_Unicode"]) for item in fonts[DONOR][1]["m_CharacterTable"]
    }
    missing = [char for char in pg.vietnamese_letters() if char not in have]
    if missing:
        raise SystemExit(f"{path.name}: {TARGET} còn thiếu {''.join(missing)}")
    alpha = read_alpha(texture_of(env, obj, tree))
    if alpha.shape[0] != tree["m_AtlasHeight"]:
        raise SystemExit(f"{path.name}: atlas cao {alpha.shape[0]}, bảng ghi {tree['m_AtlasHeight']}")


# Xem thử -------------------------------------------------------------------


def preview(path: Path, lines: list[str], fonts: list[dict[str, pg.Glyph]], scale: int = 2) -> None:
    """Vẽ chữ bằng hình glyph (đơn vị atlas), mỗi đơn vị `scale`/4 điểm ảnh ảnh."""
    def glyph(char: str) -> pg.Glyph:
        for table in fonts:
            if char in table:
                return table[char]
        return fonts[0]["?"]

    rows = []
    for text in lines:
        width = int(sum(glyph(char).advance for char in text)) + 8
        canvas = np.zeros((pg.YMAX - pg.YMIN, width), bool)
        pen = 4.0
        for char in text:
            item = glyph(char)
            for row, col in zip(*np.nonzero(item.mask)):
                x = int(round(pen)) + int(col) + pg.XMIN
                if 0 <= x < width:
                    canvas[row, x] = True
            pen += item.advance
        rows.append(canvas)
    width = max(row.shape[1] for row in rows)
    sheet = np.ones((sum(row.shape[0] for row in rows), width), np.uint8) * 255
    y = 0
    for row in rows:
        sheet[y : y + row.shape[0], : row.shape[1]][row] = 0
        y += row.shape[0]
    image = Image.fromarray(sheet)
    image.resize((max(1, width * scale // 4), max(1, sheet.shape[0] * scale // 4)), Image.NEAREST).save(path)


def main() -> int:
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.path.insert(0, str(FONT_DIR.parent))
    from extract_strings import generator
    from game_config import DATA_NAME, original, require_install

    args = sys.argv[1:]
    if len(args) < 2 or args[0] != "--preview":
        print(__doc__)
        return 2
    install = require_install()
    env = UnityPy.Environment()
    env.typetree_generator = generator(install)
    data = install / DATA_NAME
    for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
        env.load_file(str(data / extra))
    env.load_file(str(original(Path(DATA_NAME) / RESOURCES)), name=RESOURCES)
    env.load_file(str(data / f"{RESOURCES}.resS"), name=f"{RESOURCES}.resS")
    fonts = font_assets(env)
    regular = glyph_masks(fonts[TARGET][1], read_alpha(texture_of(env, *fonts[TARGET])))
    latin = glyph_masks(fonts[DONOR][1], read_alpha(texture_of(env, *fonts[DONOR])))
    new = pg.compose(regular, latin)
    lines = args[2:] or [pg.vietnamese_letters()[i : i + 34] for i in range(0, len(pg.vietnamese_letters()), 34)]
    preview(Path(args[1]), lines, [regular, new, latin], scale=4)
    print(f"Ghép {len(new)} chữ. Ảnh: {args[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
