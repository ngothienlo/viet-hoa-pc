"""Kiểm luật âm tiết của check_vietnamese.py.

    python -m unittest tools/test_check_vietnamese.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_vietnamese import syllable_error  # noqa: E402


class SyllableTests(unittest.TestCase):
    def test_valid(self) -> None:
        for word in "nghĩ gì giếng quý quyết quýnh khuya người Đường kiến ghế toán chuyện thuở khuỷu mặt hòa khỏe thủy loại ngoài xoay xở".split():
            self.assertIsNone(syllable_error(word), word)

    def test_invalid(self) -> None:
        for word in "ngĩ kái gế mằt tóan hoà khoẻ".split():
            self.assertIsNotNone(syllable_error(word), word)

    def test_interjections_skipped(self) -> None:
        for word in "Hừmmm Méooo Khèèè Grừ Đ".split():
            self.assertIsNone(syllable_error(word), word)


if __name__ == "__main__":
    unittest.main()
