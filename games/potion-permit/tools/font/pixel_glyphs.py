"""Ghép chữ Việt cho font pixel PixelMplus12 của Potion Permit, theo lưới điểm ảnh.

Font trong game là SDF dựng từ font pixel 12 px ở cỡ 46: một điểm ảnh thiết kế rộng
khoảng 3,85 đơn vị atlas, cao khoảng 3,9. Hàng 0 là hàng điểm ảnh ngay trên đường
chân chữ, đáy của nó ở y = -2.

- Chữ cái gốc và dấu sắc, huyền, ngã, mũ lấy nguyên hình từ atlas: chữ ASCII trong
  `PixelMplus12-Regular`, chữ Latin-1 (á à â ã…) trong `PixelMplus12-Latin_Supplement_PP`.
  Dấu trong font này nằm ở hàng 8-9, chữ hoa có dấu bị ép còn 7 hàng (0-6).
- Dấu font không có (hỏi, nặng, trăng, râu, gạch của đ) vẽ bằng ô điểm ảnh.
- Chữ hai dấu: chữ thường để mũ/trăng ở hàng 7-8, dấu thanh ở hàng 9-10.
  Chữ hoa để mũ/trăng ở hàng 8-9, dấu thanh ở hàng 10-11 (vượt dòng ascent một chút).

Hình là mảng bool trên khung cố định, đơn vị atlas, gốc ở đường chân chữ.
Module này không đọc file: `patch_font.py` nạp atlas rồi gọi `compose()`.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

import numpy as np

SX = 3.85
SY = 3.9
Y0 = -2.0
# Khung: x trong [XMIN, XMAX), y trong [YMIN, YMAX). Hàng mảng 0 là y = YMAX - 1.
XMIN, XMAX = -8, 40
YMIN, YMAX = -20, 56
# Hàng bắt đầu vùng dấu, tính bằng đơn vị: chữ thường cao tới y = 21, chữ hoa bị ép cao tới y = 25.
LOWER_MARK_FROM = 25
UPPER_MARK_FROM = 27

VOWELS = "aăâeêioôơuưy"
TONES = {"": "", "́": "sắc", "̀": "huyền", "̉": "hỏi", "̃": "ngã", "̣": "nặng"}


def vietnamese_letters() -> str:
    """Mọi chữ cái tiếng Việt có dấu, cả thường lẫn hoa, kèm đ Đ."""
    letters = []
    for base in VOWELS:
        for tone in TONES:
            letters.append(unicodedata.normalize("NFC", base + tone))
    letters.append("đ")
    out = "".join(letters)
    return "".join(sorted(set(out + out.upper()) - set("aeiouyAEIOUY")))


def blank() -> np.ndarray:
    return np.zeros((YMAX - YMIN, XMAX - XMIN), dtype=bool)


def set_unit(mask: np.ndarray, x: int, y: int) -> None:
    if XMIN <= x < XMAX and YMIN <= y < YMAX:
        mask[YMAX - 1 - y, x - XMIN] = True


def ys(mask: np.ndarray) -> np.ndarray:
    """Tọa độ y (đơn vị) của từng hàng mảng."""
    return YMAX - 1 - np.arange(mask.shape[0])


def above(mask: np.ndarray, y_from: int) -> np.ndarray:
    out = mask.copy()
    out[ys(mask) < y_from, :] = False
    return out


def below(mask: np.ndarray, y_to: int) -> np.ndarray:
    out = mask.copy()
    out[ys(mask) >= y_to, :] = False
    return out


def edge(origin: float, step: float, k: int) -> int:
    return int(np.floor(origin + k * step + 0.5))


def shift(mask: np.ndarray, cols: int = 0, rows: int = 0) -> np.ndarray:
    """Dời theo số ô điểm ảnh, quy ra đơn vị theo lưới."""
    dx = edge(0, SX, cols)
    dy = edge(0, SY, rows)
    out = blank()
    src = mask[max(0, dy):mask.shape[0] + min(0, dy), max(0, -dx):mask.shape[1] - max(0, dx)]
    out[max(0, -dy):mask.shape[0] - max(0, dy), max(0, dx):mask.shape[1] + min(0, dx)] = src
    return out


def cells(points: list[tuple[int, int]]) -> np.ndarray:
    """Vẽ các ô điểm ảnh (cột i, hàng j) lên khung."""
    out = blank()
    for i, j in points:
        for x in range(edge(0, SX, i), edge(0, SX, i + 1)):
            for y in range(edge(Y0, SY, j), edge(Y0, SY, j + 1)):
                set_unit(out, x, y)
    return out


@dataclass
class Glyph:
    mask: np.ndarray
    advance: float


# Dấu vẽ thêm, tọa độ (cột, hàng). Chữ rộng 5 ô (cột 0-4), tâm ở cột 2.
HOOK = [(1, 9), (2, 9), (3, 8), (2, 7)]
HOOK_SMALL = [(1, 10), (2, 10), (3, 9)]
DOT = [(2, -2)]
# Chữ y có đuôi ở hàng -2, nên dấu nặng xuống hàng -3.
DOT_Y = [(2, -3)]
BREVE = [(1, 9), (4, 9), (2, 8), (3, 8)]


def compose(regular: dict[str, Glyph], latin: dict[str, Glyph]) -> dict[str, Glyph]:
    """Dựng mọi chữ Việt font còn thiếu. `regular`, `latin`: hình chữ có sẵn của hai font."""
    have = set(regular) | set(latin)

    def get(char: str) -> Glyph:
        return regular[char] if char in regular else latin[char]

    advance = get("a").advance
    wide = advance + (edge(0, SX, 1))

    def marks(source: str, y_from: int) -> np.ndarray:
        return above(get(source).mask, y_from)

    lower_tone = {
        "́": marks("á", LOWER_MARK_FROM),
        "̀": marks("à", LOWER_MARK_FROM),
        "̃": marks("ã", LOWER_MARK_FROM),
        "̉": cells(HOOK),
    }
    upper_tone = {
        "́": marks("Á", UPPER_MARK_FROM),
        "̀": marks("À", UPPER_MARK_FROM),
        "̃": marks("Ã", UPPER_MARK_FROM),
        "̉": shift(cells(HOOK), rows=1),
    }
    # Dấu thanh khi chữ đã có mũ hoặc trăng: chữ thường lên một hàng, chữ hoa lên hai hàng.
    lower_tone_high = {k: shift(v, rows=1) for k, v in lower_tone.items() if k != "̉"}
    lower_tone_high["̉"] = cells(HOOK_SMALL)
    upper_tone_high = {k: shift(v, rows=2) for k, v in upper_tone.items() if k != "̉"}
    upper_tone_high["̉"] = shift(cells(HOOK_SMALL), rows=1)
    hat = marks("â", LOWER_MARK_FROM)
    hat_upper = marks("Â", UPPER_MARK_FROM)

    # Thân chữ không dấu. Chữ hoa lấy bản bị ép 7 hàng từ chữ Latin-1 có dấu.
    lower_body = {v: get(v).mask for v in "aeouy"}
    lower_body["i"] = below(get("í").mask, LOWER_MARK_FROM)
    upper_body = {v: below(get(src).mask, UPPER_MARK_FROM) for v, src in zip("AEIOUY", "ÁÉÍÓÚÝ")}

    out: dict[str, Glyph] = {}

    def add(char: str, *parts: np.ndarray, width: float = advance) -> None:
        if char in have:
            return
        mask = blank()
        for part in parts:
            mask |= part
        out[char] = Glyph(mask, width)

    def horn(top: int) -> np.ndarray:
        # Râu của ư: nét đứng hai điểm ảnh, chéo lên từ đỉnh nét phải của u.
        return cells([(5, top + 1), (5, top + 2)])

    def horn_o(top: int) -> np.ndarray:
        return cells([(4, top), (5, top + 1)])

    for tone, name in TONES.items():
        if not tone:
            continue
        dot = tone == "̣"
        for upper in (False, True):
            body = upper_body if upper else lower_body
            single = (upper_tone if upper else lower_tone).get(tone)
            high = (upper_tone_high if upper else lower_tone_high).get(tone)
            top = 6 if upper else 5
            hat_mark = hat_upper if upper else shift(hat, rows=-1)
            breve_mark = cells(BREVE) if upper else shift(cells(BREVE), rows=-1)

            def nfc(base: str) -> str:
                char = unicodedata.normalize("NFC", base + tone)
                return char.upper() if upper else char

            tone_mark = cells(DOT) if dot else single
            stacked = cells(DOT) if dot else high
            for v in "aeiouy":
                mark = cells(DOT_Y) if dot and v == "y" and not upper else tone_mark
                add(nfc(v), body[v.upper() if upper else v], mark)
            add(nfc("â"), body["A" if upper else "a"], hat_mark if not dot else (hat_upper if upper else hat), stacked)
            add(nfc("ê"), body["E" if upper else "e"], hat_mark if not dot else (hat_upper if upper else hat), stacked)
            add(nfc("ô"), body["O" if upper else "o"], hat_mark if not dot else (hat_upper if upper else hat), stacked)
            add(nfc("ă"), body["A" if upper else "a"], breve_mark if not dot else cells(BREVE), stacked)
            add(nfc("ơ"), body["O" if upper else "o"], horn_o(top), tone_mark, width=wide)
            add(nfc("ư"), body["U" if upper else "u"], horn(top), tone_mark, width=wide)

    # Không dấu thanh: ă Ă ơ Ơ ư Ư đ Đ.
    add("ă", lower_body["a"], cells(BREVE))
    add("Ă", upper_body["A"], cells(BREVE))
    add("ơ", lower_body["o"], horn_o(5), width=wide)
    add("ư", lower_body["u"], horn(5), width=wide)
    add("Ơ", get("O").mask, horn_o(8), width=wide)
    add("Ư", get("U").mask, horn(8), width=wide)
    add("đ", get("d").mask, cells([(2, 7), (3, 7)]))
    add("Đ", shift(get("D").mask, cols=1), cells([(0, 4), (2, 4)]), width=wide)
    return out
