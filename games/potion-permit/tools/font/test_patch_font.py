"""Kiểm phần ghép chữ và sửa catalog, không cần bản cài game.

    python -m unittest games/potion-permit/tools/font/test_patch_font.py
"""

from __future__ import annotations

import base64
import json
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import patch_font as pf  # noqa: E402
import pixel_glyphs as pg  # noqa: E402


def block(cols: range, rows: range) -> np.ndarray:
    return pg.cells([(i, j) for i in cols for j in rows])


def fake_fonts() -> tuple[dict[str, pg.Glyph], dict[str, pg.Glyph]]:
    """Font giả: chữ thường cao 6 hàng, chữ hoa 9 hàng, chữ hoa có dấu bị ép 7 hàng, dấu ở hàng 8-9."""
    lower = block(range(0, 5), range(0, 6))
    upper = block(range(0, 5), range(0, 9))
    squashed = block(range(0, 5), range(0, 7))
    mark = block(range(2, 4), range(8, 10))
    regular = {char: pg.Glyph(lower, 23.0) for char in "aeiouyd"}
    regular.update({char: pg.Glyph(upper, 23.0) for char in "AEIOUYD"})
    regular["?"] = pg.Glyph(upper, 23.0)
    latin = {}
    for char in "áàãâéèêíìóòõôúùý":
        latin[char] = pg.Glyph(lower | mark, 23.0)
    for char in "ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÝ":
        latin[char] = pg.Glyph(squashed | mark, 23.0)
    return regular, latin


class ComposeTests(unittest.TestCase):
    def test_letter_set(self) -> None:
        letters = pg.vietnamese_letters()
        self.assertEqual(len(letters), 134)
        for char in "ăâđêôơưĂÂĐÊÔƠƯấẬỹỴ":
            self.assertIn(char, letters)

    def test_compose_fills_every_missing_letter(self) -> None:
        regular, latin = fake_fonts()
        new = pg.compose(regular, latin)
        have = set(regular) | set(latin) | set(new)
        self.assertEqual([char for char in pg.vietnamese_letters() if char not in have], [])
        self.assertFalse(set(new) & set(latin), "không ghép đè chữ font đã có")

    def test_marks_sit_where_expected(self) -> None:
        regular, latin = fake_fonts()
        new = pg.compose(regular, latin)

        def top(char: str) -> int:
            rows = np.where(new[char].mask.any(axis=1))[0]
            return pg.YMAX - int(rows[0])

        def bottom(char: str) -> int:
            rows = np.where(new[char].mask.any(axis=1))[0]
            return pg.YMAX - 1 - int(rows[-1])

        # Hai dấu cao hơn một dấu; chữ hoa hai dấu cao hơn chữ thường hai dấu.
        self.assertGreater(top("ấ"), top("ả"))
        self.assertGreater(top("Ấ"), top("ấ"))
        # Dấu nặng nằm dưới chân chữ, của y thấp hơn để tránh đuôi.
        self.assertLess(bottom("ạ"), 0)
        self.assertLess(bottom("ỵ"), bottom("ạ"))
        # Chữ có râu rộng thêm một ô.
        self.assertGreater(new["ư"].advance, regular["u"].advance)


class SdfTests(unittest.TestCase):
    def test_edge_at_half(self) -> None:
        mask = np.zeros((8, 8), bool)
        mask[2:6, 2:6] = True
        field = pf.sdf(mask, 4)
        inside = field[4 + 2, 4 + 2]
        outside = field[4 + 2, 4 + 1]
        self.assertGreater(inside, 127)
        self.assertLess(outside, 128)
        self.assertEqual(field.shape, (16, 16))


class CatalogTests(unittest.TestCase):
    def test_clear_crc_keeps_length(self) -> None:
        entry = '{"m_Hash":"affb7c71","m_Crc":2852493535,"m_BundleSize":10}'
        other = '{"m_Hash":"0000aaaa","m_Crc":123,"m_BundleSize":1}'
        extra = b"\x01" + entry.encode("utf-16-le") + b"\x02" + other.encode("utf-16-le")
        catalog = json.dumps({"m_ExtraDataString": base64.b64encode(extra).decode("ascii")}).encode("utf-8")
        out = json.loads(pf.clear_crc(catalog, "affb7c71"))
        data = base64.b64decode(out["m_ExtraDataString"])
        self.assertEqual(len(data), len(extra))
        text = data[1 : 1 + len(entry) * 2].decode("utf-16-le")
        self.assertEqual(json.loads(text)["m_Crc"], 0)
        self.assertIn('"m_Crc":123', data[2 + len(entry) * 2 :].decode("utf-16-le"))

    def test_clear_crc_unknown_bundle(self) -> None:
        catalog = json.dumps({"m_ExtraDataString": base64.b64encode(b"").decode("ascii")}).encode("utf-8")
        with self.assertRaises(SystemExit):
            pf.clear_crc(catalog, "nothere")


if __name__ == "__main__":
    unittest.main()
