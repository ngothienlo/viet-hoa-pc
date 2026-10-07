"""Ghép chữ Việt từ glyph có sẵn của một TMP Font Asset (KakuPop).

Font KakuPop chỉ có ASCII và kana. Không có file TTF gốc, nên dấu được dựng
từ chính glyph của font: ´ ` ^ ~ có sẵn; móc lấy phần trên của `?`, nặng lấy
`.`, trăng lấy nửa dưới của `o`, râu lấy cung trên phải của `o`, gạch của đ
lấy `-`.

Cách ghép: dựng lại hình chữ ở độ phân giải gấp SCALE lần từ SDF, ghép hình,
rồi tính lại SDF với đúng padding của font. Nét ghép vì vậy cùng độ mềm với
chữ gốc. Rect của glyph là khung mực, padding nằm ngoài rect như font gốc.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

import numpy as np
from scipy.ndimage import label, zoom

from bake_sdf import _sdf

SCALE = 4
GAP = 4  # Khoảng trống giữa hai glyph trong atlas, ngoài phần padding.

# Dấu thanh và dấu phụ theo NFD.
GRAVE, ACUTE, CIRCUMFLEX, TILDE, BREVE, HOOK, HORN, DOT = (
    "̀",
    "́",
    "̂",
    "̃",
    "̆",
    "̉",
    "̛",
    "̣",
)
TONES = {GRAVE, ACUTE, TILDE, HOOK}
# Ngoặc kép kiểu Việt ghép từ hai dấu < hoặc >.
GUILLEMETS = {"«": "<", "»": ">"}
SUPPORTED = {GRAVE, ACUTE, CIRCUMFLEX, TILDE, BREVE, HOOK, HORN, DOT}


@dataclass
class Shape:
    """Hình chữ ở độ phân giải cao. Gốc là góc trên trái, đơn vị là px của atlas."""

    mask: np.ndarray  # bool, hàng 0 ở trên
    left: float
    top: float

    @property
    def width(self) -> float:
        return self.mask.shape[1] / SCALE

    @property
    def height(self) -> float:
        return self.mask.shape[0] / SCALE

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top - self.height

    def scaled(self, sx: float, sy: float | None = None) -> Shape:
        sy = sx if sy is None else sy
        mask = zoom(self.mask.astype(np.float32), (sy, sx), order=1) >= 0.5
        return Shape(mask, self.left, self.top)

    def moved(self, left: float, top: float) -> Shape:
        return Shape(self.mask, left, top)

    def centered(self, cx: float, bottom: float) -> Shape:
        return Shape(self.mask, cx - self.width / 2, bottom + self.height)


def vietnamese_letters() -> list[str]:
    """Mọi chữ cái tiếng Việt có dấu, hoa và thường."""
    shapes = {"a": ("", CIRCUMFLEX, BREVE), "e": ("", CIRCUMFLEX), "o": ("", CIRCUMFLEX, HORN), "u": ("", HORN), "i": ("",), "y": ("",)}
    found = set()
    for base in "aAeEiIoOuUyY":
        for extra in shapes[base.lower()]:
            for tone in ("", GRAVE, ACUTE, TILDE, HOOK, DOT):
                text = unicodedata.normalize("NFC", base + extra + tone)
                if len(text) == 1 and text != base:
                    found.add(text)
    found.update("đĐ")
    return sorted(found)


def plan(ch: str) -> tuple[str, list[str]] | None:
    """Chữ gốc ASCII và danh sách dấu. None nếu không ghép được."""
    if ch in "đĐ":
        return ("d" if ch == "đ" else "D"), ["bar"]
    parts = unicodedata.normalize("NFD", ch)
    base, marks = parts[0], list(parts[1:])
    if not base.isascii() or not base.isalpha() or not marks:
        return None
    if any(mark not in SUPPORTED for mark in marks):
        return None
    return base, marks


class Composer:
    """Ghép chữ cho một font.

    `donor` là font cùng họ có đủ dấu. Font nhỏ (chỉ có chữ và số) mượn dấu
    của donor, co theo tỉ lệ cỡ chữ mẫu của hai font.
    """

    def __init__(self, tree: dict, atlas: np.ndarray, donor: Composer | None = None) -> None:
        self.tree = tree
        self.atlas = atlas
        self.donor = donor
        self.point = float(tree["m_FaceInfo"]["m_PointSize"])
        # Mọi kích thước dấu bên dưới đo trên cỡ mẫu 64. Font cỡ khác thì nhân theo tỉ lệ.
        self.unit = self.point / 64.0
        self.padding = int(tree["m_AtlasPadding"])
        glyphs = {item["m_Index"]: item for item in tree["m_GlyphTable"]}
        self.by_char = {
            chr(item["m_Unicode"]): glyphs[item["m_GlyphIndex"]]
            for item in tree["m_CharacterTable"]
            if item["m_GlyphIndex"] in glyphs
        }
        x_height = self.by_char["x"]["m_Metrics"]["m_HorizontalBearingY"]
        cap = self.by_char["H"]["m_Metrics"]["m_HorizontalBearingY"]
        self.x_height = float(x_height)
        self.cap = float(cap)

    # Đọc hình từ atlas -------------------------------------------------

    def shape(self, ch: str) -> Shape:
        if ch not in self.by_char and self.donor is not None and ch in self.donor.by_char:
            borrowed = self.donor.shape(ch)
            return borrowed.scaled(self.point / self.donor.point)
        glyph = self.by_char[ch]
        rect = glyph["m_GlyphRect"]
        metrics = glyph["m_Metrics"]
        height = self.atlas.shape[0]
        margin = 1
        top = height - rect["m_Y"] - rect["m_Height"] - margin
        left = rect["m_X"] - margin
        crop = self.atlas[
            max(top, 0) : top + rect["m_Height"] + 2 * margin,
            max(left, 0) : left + rect["m_Width"] + 2 * margin,
        ].astype(np.float32)
        mask = zoom(crop, SCALE, order=1) >= 127.5
        # Chỉ giữ phần dính vào khung rect, bỏ mực lấn từ glyph bên cạnh.
        return _fit(mask, metrics, margin)

    def dotless(self, ch: str) -> Shape:
        """i và j không có chấm, để đặt dấu thanh."""
        shape = self.shape(ch)
        labels, count = label(shape.mask)
        if count < 2:
            return shape
        rows = [np.where(labels == index)[0].min() for index in range(1, count + 1)]
        dot = 1 + int(np.argmin(rows))
        mask = shape.mask & (labels != dot)
        return _crop_to_ink(mask, shape.left, shape.top)

    # Dấu --------------------------------------------------------------

    def mark(self, name: str) -> Shape:
        u = self.unit
        if name == GRAVE:
            return self.shape("`")
        if name == ACUTE:
            if "´" in self.by_char or (self.donor is not None and "´" in self.donor.by_char):
                return self.shape("´")
            grave = self.shape("`")
            return Shape(np.fliplr(grave.mask), grave.left, grave.top)
        if name == CIRCUMFLEX:
            return self.shape("^").scaled(0.72)
        if name == TILDE:
            tilde = self.shape("~")
            return tilde.scaled(20 * u / tilde.width, 9 * u / tilde.height)
        if name == HOOK:
            hook = self.shape("?")
            labels, count = label(hook.mask)
            if count >= 2:
                rows = [np.where(labels == index)[0].max() for index in range(1, count + 1)]
                dot = 1 + int(np.argmax(rows))
                hook = _crop_to_ink(hook.mask & (labels != dot), hook.left, hook.top)
            return hook.scaled(12 * u / hook.height)
        if name == DOT:
            dot = self.shape(".")
            return dot.scaled(9 * u / dot.height)
        if name == BREVE:
            ring = self.shape("o")
            rows = ring.mask.shape[0]
            cup = _crop_to_ink(ring.mask[rows // 2 :, :], ring.left, ring.top)
            return cup.scaled(19 * u / cup.width, 8 * u / cup.height)
        if name == HORN:
            # Cung trên phải của `o`, lật dọc: nét ngang bám thân chữ rồi cong lên.
            ring = self.shape("o")
            rows, cols = ring.mask.shape
            arc = ring.mask[: rows // 2, cols // 2 :][::-1, :]
            horn = _crop_to_ink(arc, 0.0, 0.0)
            return horn.scaled(10 * u / horn.width, 10 * u / horn.height)
        if name == "bar":
            bar = self.shape("-")
            return bar.scaled(15 * u / bar.width, 1.0)
        raise KeyError(name)

    # Ghép -------------------------------------------------------------

    def guillemet(self, ch: str) -> tuple[Shape, dict]:
        u = self.unit
        angle = self.shape(GUILLEMETS[ch])
        angle = angle.scaled(0.6 * self.x_height / angle.height)
        top = self.x_height / 2 + angle.height / 2 + 2 * u
        left = 2 * u
        first = angle.moved(left, top)
        second = angle.moved(left + angle.width * 0.8, top)
        merged = _union([first, second])
        source = self.by_char.get(GUILLEMETS[ch]) or self.by_char["a"]
        metrics = dict(source["m_Metrics"])
        metrics["m_HorizontalAdvance"] = max(metrics["m_HorizontalAdvance"], merged.right + 2 * u)
        return merged, metrics

    def compose(self, ch: str) -> tuple[Shape, dict] | None:
        if ch in GUILLEMETS:
            return self.guillemet(ch)
        steps = plan(ch)
        if steps is None:
            return None
        base_ch, marks = steps
        if base_ch not in self.by_char:
            return None
        u = self.unit
        upper = base_ch.isupper()
        base = self.dotless(base_ch) if base_ch in "ij" and any(m != DOT for m in marks) else self.shape(base_ch)
        parts = [base]
        shrink = 0.85 if upper else 1.0
        gap = (3.0 if upper else 4.0) * u
        cx = (base.left + base.right) / 2
        above = base.top + gap

        if "bar" in marks:
            bar = self.mark("bar")
            if upper:
                bar = bar.centered(base.left + 4.0 * u, self.cap * 0.5 - bar.height / 2)
            else:
                bar = bar.centered(base.right - 5.0 * u, (self.cap + self.x_height) / 2 - bar.height / 2 + 2 * u)
            parts.append(bar)

        if HORN in marks:
            horn = self.mark(HORN).scaled(shrink)
            parts.append(horn.moved(base.right - horn.width * 0.45, base.top + horn.height * 0.6))

        if DOT in marks:
            dot = self.mark(DOT).scaled(shrink)
            parts.append(dot.centered(cx, min(base.bottom, 0.0) - 3.0 * u - dot.height))

        shelf = None
        if CIRCUMFLEX in marks or BREVE in marks:
            name = CIRCUMFLEX if CIRCUMFLEX in marks else BREVE
            shelf = self.mark(name).scaled(shrink).centered(cx, above)
            parts.append(shelf)

        tone = next((m for m in marks if m in TONES), None)
        if tone is not None:
            sign = self.mark(tone).scaled(shrink * (0.85 if shelf is not None else 1.0))
            if shelf is None:
                parts.append(sign.centered(cx, above))
            elif tone == TILDE or name == BREVE:
                parts.append(sign.centered(cx, shelf.top + 1.5 * u))
            else:
                # Sắc, huyền, hỏi đứng bên phải mũ, như cách Be Vietnam Pro đặt.
                parts.append(sign.moved(shelf.right - 1.0 * u, shelf.top + sign.height * 0.55))

        merged = _union(parts)
        metrics = dict(self.by_char[base_ch]["m_Metrics"])
        if HORN in marks:
            # Râu chìa ra phải. Nới bước chữ để không đè chữ sau.
            metrics["m_HorizontalAdvance"] = max(metrics["m_HorizontalAdvance"], merged.right + 1.0 * u)
        return merged, metrics

    # Ghi vào atlas ----------------------------------------------------

    def build(self, chars: list[str]) -> dict:
        """Ghép mọi chữ trong `chars` mà font còn thiếu. Trả bảng mới và atlas mới."""
        made: list[tuple[str, Shape, dict, np.ndarray]] = []
        skipped: list[str] = []
        for ch in chars:
            if ch in self.by_char:
                continue
            result = self.compose(ch)
            if result is None:
                skipped.append(ch)
                continue
            shape, metrics = result
            coverage = np.where(shape.mask, 255, 0).astype(np.uint8)
            field = _sdf(_pad_to_scale(coverage), self.padding, SCALE)
            made.append((ch, shape, metrics, field))
        atlas, rects = self._pack([field for *_rest, field in made])
        glyphs = list(self.tree["m_GlyphTable"])
        characters = list(self.tree["m_CharacterTable"])
        used = list(self.tree.get("m_UsedGlyphRects") or [])
        index = max((item["m_Index"] for item in glyphs), default=0) + 1
        for (ch, shape, base_metrics, _field), rect in zip(made, rects):
            metrics = {
                "m_Width": float(rect["m_Width"]),
                "m_Height": float(rect["m_Height"]),
                "m_HorizontalBearingX": float(shape.left),
                "m_HorizontalBearingY": float(shape.top),
                "m_HorizontalAdvance": float(base_metrics["m_HorizontalAdvance"]),
            }
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
            characters.append({"m_ElementType": 1, "m_Unicode": ord(ch), "m_GlyphIndex": index, "m_Scale": 1.0})
            pad = self.padding
            used.append(
                {
                    "m_X": rect["m_X"] - pad,
                    "m_Y": rect["m_Y"] - pad,
                    "m_Width": rect["m_Width"] + 2 * pad,
                    "m_Height": rect["m_Height"] + 2 * pad,
                }
            )
            index += 1
        return {
            "atlas": atlas,
            "glyphs": glyphs,
            "characters": characters,
            "used": used,
            "added": [ch for ch, *_rest in made],
            "skipped": skipped,
        }

    def _pack(self, fields: list[np.ndarray]) -> tuple[np.ndarray, list[dict]]:
        """Nới atlas lên phía trên rồi xếp glyph mới vào phần nới.

        Rect của TMP tính m_Y từ đáy ảnh, nên giữ ảnh cũ ở đáy thì rect cũ không đổi.
        """
        old = self.atlas
        width = old.shape[1]
        height = old.shape[0]
        extra = height
        while True:
            placed = _shelf_pack(fields, width, extra)
            if placed is not None:
                break
            extra *= 2
        canvas = np.zeros((height + extra, width), np.uint8)
        canvas[extra:, :] = old
        rects = []
        pad = self.padding
        total = height + extra
        for field, (x, y) in zip(fields, placed):
            h, w = field.shape
            canvas[y : y + h, x : x + w] = np.clip(np.round(field * 255), 0, 255).astype(np.uint8)
            rects.append(
                {
                    "m_X": x + pad,
                    "m_Y": total - (y + h) + pad,
                    "m_Width": w - 2 * pad,
                    "m_Height": h - 2 * pad,
                }
            )
        return canvas, rects


def _shelf_pack(fields: list[np.ndarray], width: int, height: int) -> list[tuple[int, int]] | None:
    x = GAP
    y = GAP
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


def _fit(mask: np.ndarray, metrics: dict, margin: int) -> Shape:
    left = float(metrics["m_HorizontalBearingX"]) - margin
    top = float(metrics["m_HorizontalBearingY"]) + margin
    labels, count = label(mask)
    if count > 1:
        # Bỏ mảnh nằm hẳn trong viền margin: đó là mực của glyph bên cạnh.
        inner = np.zeros_like(mask)
        edge = margin * SCALE
        inner[edge:-edge or None, edge:-edge or None] = True
        keep = np.zeros_like(mask)
        for index in range(1, count + 1):
            part = labels == index
            if (part & inner).any():
                keep |= part
        mask = keep
    return _crop_to_ink(mask, left, top)


def _crop_to_ink(mask: np.ndarray, left: float, top: float) -> Shape:
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if rows.size == 0:
        return Shape(np.zeros((SCALE, SCALE), bool), left, top)
    r0, r1 = rows[0], rows[-1] + 1
    c0, c1 = cols[0], cols[-1] + 1
    return Shape(mask[r0:r1, c0:c1], left + c0 / SCALE, top - r0 / SCALE)


def _union(parts: list[Shape]) -> Shape:
    left = min(part.left for part in parts)
    top = max(part.top for part in parts)
    right = max(part.right for part in parts)
    bottom = min(part.bottom for part in parts)
    width = int(np.ceil((right - left) * SCALE)) + 1
    height = int(np.ceil((top - bottom) * SCALE)) + 1
    canvas = np.zeros((height, width), bool)
    for part in parts:
        x = int(round((part.left - left) * SCALE))
        y = int(round((top - part.top) * SCALE))
        h, w = part.mask.shape
        canvas[y : y + h, x : x + w] |= part.mask[: height - y, : width - x]
    return _crop_to_ink(canvas, left, top)


def _pad_to_scale(coverage: np.ndarray) -> np.ndarray:
    h, w = coverage.shape
    out = np.zeros(((h + SCALE - 1) // SCALE * SCALE, (w + SCALE - 1) // SCALE * SCALE), np.uint8)
    out[:h, :w] = coverage
    return out
