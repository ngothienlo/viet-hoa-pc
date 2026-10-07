"""Kiểm tra ghép chữ Việt trên một font giả. Không đọc bản cài game."""

from __future__ import annotations

import sys
import unicodedata
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compose_glyphs import ACUTE, BREVE, DOT, GUILLEMETS, Composer, plan, vietnamese_letters  # noqa: E402

PADDING = 6
CELL = 48


def fake_font(chars: str) -> tuple[dict, np.ndarray]:
    """Mỗi chữ là một khối chữ nhật đặc, xếp theo hàng trong atlas, rect không gồm padding."""
    width = CELL * 16
    rows = (len(chars) + 15) // 16
    height = CELL * rows
    atlas = np.zeros((height, width), np.uint8)
    glyphs = []
    characters = []
    for index, ch in enumerate(chars, start=1):
        col = (index - 1) % 16
        row = (index - 1) // 16
        small = ch in "`^~'´.,-"
        w, h = (10, 6) if small else (18, 24 if ch.islower() else 30)
        x = col * CELL + PADDING
        top = row * CELL + PADDING
        # Trường khoảng cách đơn giản: trong khối 1, ngoài khối 0, cạnh ở 0.5.
        block = np.zeros((h + 2 * PADDING, w + 2 * PADDING), np.float32)
        block[PADDING : PADDING + h, PADDING : PADDING + w] = 1.0
        atlas[top - PADDING : top + h + PADDING, x - PADDING : x + w + PADDING] = (block * 255).astype(np.uint8)
        bearing_y = 46.0 if small else float(h)
        glyphs.append(
            {
                "m_Index": index,
                "m_Metrics": {
                    "m_Width": float(w),
                    "m_Height": float(h),
                    "m_HorizontalBearingX": 2.0,
                    "m_HorizontalBearingY": bearing_y,
                    "m_HorizontalAdvance": 32.0,
                },
                "m_GlyphRect": {"m_X": x, "m_Y": height - top - h, "m_Width": w, "m_Height": h},
                "m_Scale": 1.0,
                "m_AtlasIndex": 0,
                "m_ClassDefinitionType": 0,
            }
        )
        characters.append({"m_ElementType": 1, "m_Unicode": ord(ch), "m_GlyphIndex": index, "m_Scale": 1.0})
    tree = {
        "m_FaceInfo": {"m_PointSize": 64},
        "m_AtlasPadding": PADDING,
        "m_GlyphTable": glyphs,
        "m_CharacterTable": characters,
        "m_UsedGlyphRects": [],
    }
    return tree, atlas


ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`^~'´.,-?<>"


class PlanTest(unittest.TestCase):
    def test_every_vietnamese_letter_has_a_plan(self) -> None:
        letters = vietnamese_letters()
        # 67 chữ thường có dấu và 67 chữ hoa, kể cả đ/Đ.
        self.assertEqual(len(letters), 134)
        for ch in letters:
            with self.subTest(ch=ch):
                self.assertIsNotNone(plan(ch))

    def test_plan_splits_base_and_marks(self) -> None:
        base, marks = plan("ặ")
        self.assertEqual((base, sorted(marks)), ("a", sorted([BREVE, DOT])))
        self.assertEqual(plan("đ"), ("d", ["bar"]))
        self.assertIsNone(plan("a"))
        self.assertIsNone(plan("©"))


class ComposerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tree, self.atlas = fake_font(ASCII)

    def test_build_adds_every_letter_and_keeps_old_rects(self) -> None:
        composer = Composer(self.tree, self.atlas)
        wanted = vietnamese_letters() + list(GUILLEMETS)
        result = composer.build(wanted)
        self.assertEqual(result["skipped"], [])
        self.assertEqual(sorted(result["added"]), sorted(wanted))
        atlas = result["atlas"]
        self.assertEqual(atlas.shape[1], self.atlas.shape[1])
        # Ảnh cũ nằm ở đáy ảnh mới. Rect tính từ đáy nên không đổi.
        self.assertTrue(np.array_equal(atlas[-self.atlas.shape[0] :, :], self.atlas))
        old = {item["m_Index"]: item["m_GlyphRect"] for item in self.tree["m_GlyphTable"]}
        for item in result["glyphs"]:
            if item["m_Index"] in old:
                self.assertEqual(item["m_GlyphRect"], old[item["m_Index"]])

    def test_new_rects_fit_in_atlas_and_do_not_overlap(self) -> None:
        result = Composer(self.tree, self.atlas).build(vietnamese_letters())
        height, width = result["atlas"].shape
        boxes = []
        for item in result["glyphs"][len(self.tree["m_GlyphTable"]) :]:
            rect = item["m_GlyphRect"]
            x0 = rect["m_X"] - PADDING
            y0 = rect["m_Y"] - PADDING
            x1 = rect["m_X"] + rect["m_Width"] + PADDING
            y1 = rect["m_Y"] + rect["m_Height"] + PADDING
            self.assertGreaterEqual(x0, 0)
            self.assertGreaterEqual(y0, 0)
            self.assertLessEqual(x1, width)
            self.assertLessEqual(y1, height)
            boxes.append((x0, y0, x1, y1))
        for i, a in enumerate(boxes):
            for b in boxes[i + 1 :]:
                overlap = a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
                self.assertFalse(overlap, f"{a} chồng {b}")

    def test_marks_sit_above_base(self) -> None:
        composer = Composer(self.tree, self.atlas)
        base = composer.shape("a")
        shape, _metrics = composer.compose("á")
        self.assertGreater(shape.top, base.top)
        shape, _metrics = composer.compose("ạ")
        self.assertLess(shape.bottom, base.bottom)

    def test_small_font_borrows_marks_from_donor(self) -> None:
        donor = Composer(self.tree, self.atlas)
        tree, atlas = fake_font("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        result = Composer(tree, atlas, donor).build(vietnamese_letters())
        self.assertEqual(result["skipped"], [])
        self.assertIn("ẫ", result["added"])

    def test_horn_sticks_out_right(self) -> None:
        composer = Composer(self.tree, self.atlas)
        shape, metrics = composer.compose("ư")
        self.assertGreater(shape.right, composer.shape("u").right)
        self.assertGreaterEqual(metrics["m_HorizontalAdvance"], shape.right)

    def test_native_mark_is_taken_from_latin1_letter(self) -> None:
        tree, atlas = fake_font(ASCII)
        composer = Composer(tree, atlas)
        # Ghép tay một chữ á giả: khối a cộng một khối dấu phía trên, rồi đưa vào font.
        accented, _ = composer.compose("á")
        self.assertIsNone(composer.native_mark(ACUTE, upper=False))
        result = composer.build(["á"])
        native = Composer({**tree, "m_GlyphTable": result["glyphs"], "m_CharacterTable": result["characters"]}, result["atlas"])
        mark = native.native_mark(ACUTE, upper=False)
        self.assertIsNotNone(mark)
        self.assertGreaterEqual(mark.bottom, native.shape("a").top - 0.5)
        self.assertLess(mark.width, accented.width)

    def test_uppercase_only_font_borrows_base_letters(self) -> None:
        """Như _savewindow: chỉ có vài chữ hoa, mượn chữ gốc, số đo và dấu của donor."""
        donor = Composer(self.tree, self.atlas)
        tree, atlas = fake_font("ACDEGHILMNOPRSTUVW")
        composer = Composer(tree, atlas, donor)
        result = composer.build(["Ư", "Đ", "Ý", "ư"])
        self.assertEqual(result["skipped"], [])
        self.assertEqual(sorted(result["added"]), sorted(["Ư", "Đ", "Ý", "ư"]))

    def test_nfc_output(self) -> None:
        for ch in vietnamese_letters():
            self.assertEqual(unicodedata.normalize("NFC", ch), ch)


if __name__ == "__main__":
    unittest.main()
