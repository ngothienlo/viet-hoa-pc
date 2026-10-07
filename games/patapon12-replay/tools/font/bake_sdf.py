"""Nướng atlas SDF Be Vietnam Pro cho TextMeshPro của game.

Unity Editor 2022.3.52f1 trên máy này chưa có license, nên không chạy
Font Asset Creator. Atlas này theo cùng quy ước với font gốc: Alpha8,
cạnh chữ ở 0.5, spread = padding, rect khít bitmap.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import freetype
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from game_config import GAME_DIR, font_path  # noqa: E402

CSV_PATH = GAME_DIR / "locale" / "vi" / "strings.csv"
CHARSET_PATH = Path(__file__).with_name("vietnamese-charset.txt")
PREVIEW_DIR = GAME_DIR / "build" / "font-preview"


# Chỉ dùng cho ký tự Be Vietnam Pro không có. Chữ Việt vẫn một mặt chữ.
def symbol_fonts(bold: bool) -> tuple[tuple[Path, int], ...]:
    gothic = Path(r"C:\Windows\Fonts\YuGothB.ttc" if bold else r"C:\Windows\Fonts\YuGothR.ttc")
    return ((Path(r"C:\Windows\Fonts\seguisym.ttf"), 0), (gothic, 0))

POINT = 64
PADDING = 14
SCALE = 4
REQUIRED = "ăâêôơưđáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵĂÂÊÔƠƯĐÁÀẢÃẠ"


def collect_codepoints() -> list[int]:
    found: set[int] = set(range(32, 127))
    found.update(ord(ch) for ch in CHARSET_PATH.read_text(encoding="utf-8"))
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            found.update(ord(ch) for ch in (row.get("vi") or ""))
    return sorted(cp for cp in found if cp >= 32 and cp != 0x7F)


def _bitmap(glyph: freetype.Glyph) -> np.ndarray:
    bitmap = glyph.bitmap
    if bitmap.width == 0 or bitmap.rows == 0:
        return np.zeros((0, 0), np.uint8)
    pitch = abs(bitmap.pitch) or bitmap.width
    raw = np.array(bitmap.buffer, dtype=np.uint8).reshape(bitmap.rows, pitch)
    return raw[:, : bitmap.width]


def _sdf(coverage: np.ndarray, pad: int, scale: int) -> np.ndarray:
    """Alpha 0..1, gồm cả viền pad. Cạnh chữ nằm ở 0.5, không bị cắt dấu."""
    if coverage.size == 0:
        return np.zeros((0, 0), np.float32)
    height = coverage.shape[0] // scale
    width = coverage.shape[1] // scale
    if height == 0 or width == 0:
        return np.zeros((0, 0), np.float32)
    coverage = coverage[: height * scale, : width * scale]
    hp = pad * scale
    canvas = np.zeros((coverage.shape[0] + 2 * hp, coverage.shape[1] + 2 * hp), np.uint8)
    canvas[hp : hp + coverage.shape[0], hp : hp + coverage.shape[1]] = coverage
    inside = canvas >= 128
    signed = distance_transform_edt(inside) - distance_transform_edt(~inside)
    alpha = np.clip(signed / scale / (2 * pad) + 0.5, 0.0, 1.0)
    out_h = height + 2 * pad
    out_w = width + 2 * pad
    alpha = alpha[: out_h * scale, : out_w * scale]
    return alpha.reshape(out_h, scale, out_w, scale).mean(axis=(1, 3))


def _metrics(glyph: freetype.Glyph, scale: int) -> dict[str, float]:
    metrics = glyph.metrics
    return {
        "m_Width": metrics.width / 64.0 / scale,
        "m_Height": metrics.height / 64.0 / scale,
        "m_HorizontalBearingX": metrics.horiBearingX / 64.0 / scale,
        "m_HorizontalBearingY": metrics.horiBearingY / 64.0 / scale,
        "m_HorizontalAdvance": metrics.horiAdvance / 64.0 / scale,
    }


def _face_info(face: freetype.Face) -> dict:
    face.set_pixel_sizes(POINT, POINT)
    size = face.size
    ascender = size.ascender / 64.0
    descender = size.descender / 64.0
    line_height = size.height / 64.0
    face.load_char("H", freetype.FT_LOAD_NO_HINTING)
    cap = face.glyph.metrics.horiBearingY / 64.0
    face.load_char("x", freetype.FT_LOAD_NO_HINTING)
    mean = face.glyph.metrics.horiBearingY / 64.0
    scale = POINT / face.units_per_EM
    underline = face.underline_position * scale if face.underline_position else -POINT * 0.1
    thickness = face.underline_thickness * scale if face.underline_thickness else POINT * 0.05
    return {
        "pointSize": POINT,
        "lineHeight": float(line_height),
        "ascentLine": float(ascender),
        "capLine": float(cap),
        "meanLine": float(mean),
        "baseline": 0.0,
        "descentLine": float(descender),
        "underlineOffset": float(underline),
        "underlineThickness": float(max(thickness, 1.0)),
        "strikethroughOffset": float(cap / 2.5),
        "strikethroughThickness": float(max(thickness, 1.0)),
        "tabWidth": float(face.get_advance(ord(" "), freetype.FT_LOAD_NO_HINTING) / 64.0),
        "unitsPerEM": int(face.units_per_EM),
    }


def _load_face(path: Path, pixel: int) -> freetype.Face:
    face = freetype.Face(str(path))
    face.set_pixel_sizes(pixel, pixel)
    return face


def bake(ttf: Path, codepoints: list[int], atlas_w: int, atlas_h: int, *, bold: bool = False) -> dict:
    primary = _load_face(ttf, POINT * SCALE)
    fallbacks = []
    for path, index in symbol_fonts(bold):
        if not path.is_file():
            continue
        face = freetype.Face(str(path), index)
        face.set_pixel_sizes(POINT * SCALE, POINT * SCALE)
        fallbacks.append(face)
    missing = [chr(cp) for cp in REQUIRED if primary.get_char_index(ord(cp)) == 0]
    if missing:
        raise SystemExit(f"{ttf.name} thiếu chữ bắt buộc: {''.join(missing)}")

    placed = []
    skipped: list[str] = []
    flags = freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING
    for cp in codepoints:
        face = primary if primary.get_char_index(cp) else None
        if face is None:
            face = next((item for item in fallbacks if item.get_char_index(cp)), None)
        if face is None:
            skipped.append(chr(cp))
            continue
        face.load_char(cp, flags)
        coverage = _bitmap(face.glyph)
        alpha = _sdf(coverage, PADDING, SCALE)
        placed.append((cp, _metrics(face.glyph, SCALE), alpha))

    atlas = np.zeros((atlas_h, atlas_w), np.float32)
    gap = 4
    x = gap
    y = gap
    row_h = 0
    glyphs = []
    characters = []
    used = []
    index = 1
    for cp, metrics, alpha in placed:
        height, width = alpha.shape
        if width == 0 or height == 0:
            rect = {"m_X": 0, "m_Y": 0, "m_Width": 0, "m_Height": 0}
        else:
            # Viền pad nằm trong rect. Dịch bearing để nét chữ vẫn đúng dòng.
            metrics["m_HorizontalBearingX"] -= PADDING
            metrics["m_HorizontalBearingY"] += PADDING
            metrics["m_Width"] = float(width)
            metrics["m_Height"] = float(height)
            if x + width + gap > atlas_w:
                x = gap
                y += row_h + gap
                row_h = 0
            if y + height + gap > atlas_h:
                raise SystemExit(f"Atlas {atlas_w}x{atlas_h} không đủ cho {len(placed)} glyph")
            atlas[y : y + height, x : x + width] = alpha
            rect = {
                "m_X": x,
                "m_Y": atlas_h - y - height,
                "m_Width": width,
                "m_Height": height,
            }
            used.append(rect)
            row_h = max(row_h, height)
            x += width + gap
        glyphs.append(
            {
                "m_Index": index,
                "m_Metrics": metrics,
                "m_GlyphRect": rect,
                "m_Scale": 1.0,
                "m_AtlasIndex": 0,
                "m_ClassDefinitionType": 0,
            }
        )
        characters.append(
            {"m_ElementType": 1, "m_Unicode": cp, "m_GlyphIndex": index, "m_Scale": 1.0}
        )
        index += 1

    face_info = _face_info(_load_face(ttf, POINT))
    print(
        f"{ttf.name}: {len(characters)} glyph, bỏ {len(skipped)}, "
        f"atlas {atlas_w}x{atlas_h}, line {face_info['lineHeight']:.1f}"
    )
    if skipped:
        sample = "".join(skipped[:40])
        print(f"  không có trong font: {sample!r} (+{max(0, len(skipped) - 40)})")
    return {
        "atlas": np.clip(np.round(atlas * 255), 0, 255).astype(np.uint8),
        "glyphs": glyphs,
        "characters": characters,
        "usedRects": used,
        "freeRects": [
            {
                "m_X": 0,
                "m_Y": 0,
                "m_Width": atlas_w,
                "m_Height": max(1, atlas_h - (y + row_h) - 1),
            }
        ],
        "face": face_info,
        "width": atlas_w,
        "height": atlas_h,
        "padding": PADDING,
        "skipped": skipped,
    }


def render_preview(baked: dict, text: str, path: Path) -> None:
    by_cp = {item["m_Unicode"]: item for item in baked["characters"]}
    by_index = {item["m_Index"]: item for item in baked["glyphs"]}
    face = baked["face"]
    atlas = baked["atlas"]
    lines = text.split("\n")
    width = 1400
    line_h = int(face["lineHeight"]) + 8
    image = Image.new("L", (width, line_h * len(lines) + 20), 0)
    draw_px = image.load()
    for line_index, line in enumerate(lines):
        pen = 16.0
        baseline = 16 + face["ascentLine"] + line_index * line_h
        for ch in line:
            character = by_cp.get(ord(ch))
            if character is None:
                pen += face["tabWidth"]
                continue
            glyph = by_index[character["m_GlyphIndex"]]
            rect = glyph["m_GlyphRect"]
            metrics = glyph["m_Metrics"]
            if rect["m_Width"] and rect["m_Height"]:
                top = baked["height"] - rect["m_Y"] - rect["m_Height"]
                crop = atlas[top : top + rect["m_Height"], rect["m_X"] : rect["m_X"] + rect["m_Width"]]
                ox = int(round(pen + metrics["m_HorizontalBearingX"]))
                oy = int(round(baseline - metrics["m_HorizontalBearingY"]))
                for row in range(crop.shape[0]):
                    for col in range(crop.shape[1]):
                        px = ox + col
                        py = oy + row
                        if 0 <= px < width and 0 <= py < image.height:
                            # Cạnh SDF 0.5 thành mực, gần giống shader.
                            ink = int(np.clip((crop[row, col] / 255.0 - 0.5) * 10 + 0.5, 0, 1) * 255)
                            if ink > draw_px[px, py]:
                                draw_px[px, py] = ink
            pen += metrics["m_HorizontalAdvance"]
    image.save(path)
    print("preview", path)


def main() -> None:
    codes = collect_codepoints()
    print("codepoints", len(codes))
    out = PREVIEW_DIR
    out.mkdir(parents=True, exist_ok=True)
    regular = bake(font_path("regular"), codes, 4096, 4096, bold=False)
    bold = bake(font_path("bold"), codes, 4096, 2048, bold=True)
    sample = "Người Chỉ Huy\nớ ợ ự ẫ ỹ ệ Ă Â Ê Ô Ơ Ư Đ\ndân Patapon cổ đại, nhờ quyền năng chiếc trống"
    render_preview(regular, sample, out / "vh-font-preview-regular.png")
    render_preview(bold, sample, out / "vh-font-preview-bold.png")


if __name__ == "__main__":
    main()
