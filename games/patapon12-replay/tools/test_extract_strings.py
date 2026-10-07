"""Kiểm tra cách đặt id, không đọc bản cài game."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def load():
    path = Path(__file__).with_name("extract_strings.py")
    spec = importlib.util.spec_from_file_location("extract_strings", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


extract = load()


def english() -> dict:
    block = {"messageCount": 1, "category": 0, "messages": ["Yes"]}
    mission = {"m_Keys": ["missionid_0010"], "m_Values": [{"messages": ["Forward march!"]}]}
    return {
        "missionData": {"message": mission, "preMessage": mission},
        "colonyMsgData": {"message": block},
        "loadingGroupData": {
            "errorMessage": block,
            "itemMessage": block,
            "systemMsg": block,
            "titleMsg": block,
            "unitNameMsg": block,
        },
        "imageData": {"tipsText": block, "keyGuide": block, "titleString": block},
        "helpData": {"helpTitle": block, "helpText": block},
        "guideData": {"tipsMessage": block},
    }


class ExtractTests(unittest.TestCase):
    def test_ids_are_stable_and_unique(self) -> None:
        rows = extract.rows_from_english("P1", english())
        ids = [row["id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("P1.mission.missionid_0010.line.0", ids)
        self.assertIn("P1.mission.missionid_0010.pre.0", ids)
        self.assertIn("P1.colony.0", ids)
        self.assertTrue(all(row["vi"] == "" and row["status"] == "todo" for row in rows))
        march = next(row for row in rows if row["id"] == "P1.mission.missionid_0010.line.0")
        self.assertEqual(march["source"], "Forward march!")
        self.assertEqual(march["context"], "dialog")


if __name__ == "__main__":
    unittest.main()
