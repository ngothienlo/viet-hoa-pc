"""Kiểm tra áp/gỡ bản dịch và trạng thái nút, không đụng bản cài thật."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import tkinter as tk

from launcher.apply import apply_pack, build_dir, inside, install_error, remove_pack, run_build
from launcher.app import Launcher
from launcher.catalog import load_games, pack_files
from launcher.store import Store


def write_game(root: Path, files: dict[str, str]) -> None:
    game = root / "games" / "demo"
    patch = game / "patch"
    patch.mkdir(parents=True)
    (game / "game.json").write_text(
        json.dumps(
            {
                "id": "demo",
                "title": "Demo",
                "summary": "Game thử.",
                "exe": "Game.exe",
                "detect": ["Game.exe"],
            }
        ),
        encoding="utf-8",
    )
    (game / "config.example.json").write_text(
        json.dumps({"installs": {"steam": str(root / "missing-steam"), "epic": ""}}),
        encoding="utf-8",
    )
    for name, text in files.items():
        path = patch / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    (patch / ".gitkeep").write_text("", encoding="utf-8")


BUILDER = """
from pathlib import Path


def build(install, out, log):
    if (install / "broken.flag").exists():
        raise SystemExit("Bản cài không khớp.")
    log("đang build")
    (out / "data").mkdir(parents=True, exist_ok=True)
    original = (install / "data" / "old.txt").read_text(encoding="utf-8")
    (out / "data" / "old.txt").write_text(original + "+vi", encoding="utf-8")
"""


class BuildTests(unittest.TestCase):
    """Game có khóa build: file vá được tạo từ bản cài, không lấy từ patch/."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_game(self.root, {"data/stale.txt": "không được áp"})
        game_dir = self.root / "games" / "demo"
        manifest = json.loads((game_dir / "game.json").read_text(encoding="utf-8"))
        manifest["build"] = "build.py"
        (game_dir / "game.json").write_text(json.dumps(manifest), encoding="utf-8")
        (game_dir / "build.py").write_text(BUILDER, encoding="utf-8")
        self.install = self.root / "install"
        (self.install / "data").mkdir(parents=True)
        (self.install / "Game.exe").write_text("exe", encoding="utf-8")
        (self.install / "data" / "old.txt").write_text("old", encoding="utf-8")
        self.store = Store(self.root / "state")
        self.game = load_games(self.root)[0]

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_build_then_apply_uses_build_output(self) -> None:
        lines: list[str] = []
        result = run_build(self.game, self.install, self.store, lines.append)
        self.assertTrue(result.ok, result.message)
        self.assertEqual(lines, ["đang build"])
        self.assertTrue((build_dir(self.game, self.store) / "data" / "old.txt").is_file())
        applied = apply_pack(self.game, self.install, self.store)
        self.assertTrue(applied.ok, applied.message)
        self.assertEqual((self.install / "data" / "old.txt").read_text(encoding="utf-8"), "old+vi")
        self.assertFalse((self.install / "data" / "stale.txt").exists())
        removed = remove_pack(self.game, self.install, self.store)
        self.assertTrue(removed.ok)
        self.assertEqual((self.install / "data" / "old.txt").read_text(encoding="utf-8"), "old")

    def test_build_error_is_reported(self) -> None:
        (self.install / "broken.flag").write_text("", encoding="utf-8")
        result = run_build(self.game, self.install, self.store, lambda _line: None)
        self.assertFalse(result.ok)
        self.assertIn("không khớp", result.message)

    def test_build_refuses_wrong_install(self) -> None:
        result = run_build(self.game, self.root / "nowhere", self.store, lambda _line: None)
        self.assertFalse(result.ok)


class ApplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_game(self.root, {"data/old.txt": "new", "data/added.txt": "added"})
        self.install = self.root / "install"
        (self.install / "data").mkdir(parents=True)
        (self.install / "Game.exe").write_text("exe", encoding="utf-8")
        (self.install / "data" / "old.txt").write_text("old", encoding="utf-8")
        self.store = Store(self.root / "state")
        self.game = load_games(self.root)[0]

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_apply_then_remove_restores_original(self) -> None:
        applied = apply_pack(self.game, self.install, self.store)
        self.assertTrue(applied.ok)
        self.assertEqual((self.install / "data" / "old.txt").read_text(encoding="utf-8"), "new")
        self.assertEqual((self.install / "data" / "added.txt").read_text(encoding="utf-8"), "added")
        (self.game.patch_dir / "data" / "old.txt").write_text("newer", encoding="utf-8")
        again = apply_pack(self.game, self.install, self.store)
        self.assertTrue(again.ok)
        self.assertEqual((self.install / "data" / "old.txt").read_text(encoding="utf-8"), "newer")
        removed = remove_pack(self.game, self.install, self.store)
        self.assertTrue(removed.ok)
        self.assertEqual((self.install / "data" / "old.txt").read_text(encoding="utf-8"), "old")
        self.assertFalse((self.install / "data" / "added.txt").exists())

    def test_empty_pack_does_not_write(self) -> None:
        for path in (self.game.patch_dir).rglob("*"):
            if path.is_file() and path.name != ".gitkeep":
                path.unlink()
        before = (self.install / "data" / "old.txt").read_text(encoding="utf-8")
        result = apply_pack(self.game, self.install, self.store)
        self.assertFalse(result.ok)
        self.assertEqual((self.install / "data" / "old.txt").read_text(encoding="utf-8"), before)
        self.assertIsNone(self.store.applied_backup("demo"))

    def test_rejects_escape(self) -> None:
        with self.assertRaises(ValueError):
            inside(self.install, Path("..") / "outside.txt")

    def test_missing_exe(self) -> None:
        empty = self.root / "empty"
        empty.mkdir()
        self.assertIsNotNone(install_error(self.game, empty))
        result = apply_pack(self.game, empty, self.store)
        self.assertFalse(result.ok)

    def test_pack_keeps_doorstop_marker(self) -> None:
        marker = self.game.patch_dir / ".doorstop_version"
        marker.write_text("4.3.0", encoding="utf-8")
        names = {relative.as_posix() for _, relative in pack_files(self.game)}
        self.assertIn(".doorstop_version", names)
        self.assertIn("data/old.txt", names)
        self.assertNotIn(".gitkeep", names)

    def test_real_repo_lists_patapon(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        games = load_games(repo)
        patapon = next(game for game in games if game.id == "patapon12-replay")
        self.assertEqual(patapon.exe, "PATAPON12_REPLAY.exe")
        names = {relative.as_posix() for _, relative in pack_files(patapon)}
        self.assertIn("BepInEx/config/AutoTranslatorConfig.ini", names)
        self.assertNotIn(".gitkeep", names)
        self.assertTrue(any("PATAPON12_REPLAY" in str(hint) for hint in patapon.hints))


class ButtonTests(unittest.TestCase):
    def test_apply_stays_off_until_path_and_pack_are_ready(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root_path = Path(raw)
            write_game(root_path, {"note.txt": "vi"})
            install = root_path / "install"
            install.mkdir()
            (install / "Game.exe").write_text("exe", encoding="utf-8")
            (install / "note.txt").write_text("en", encoding="utf-8")
            window = tk.Tk()
            window.withdraw()
            try:
                app = Launcher(window, root_path, root_path / "state")
                self.assertEqual(str(app.apply_button["state"]), "disabled")
                self.assertEqual(str(app.play_button["state"]), "disabled")
                app.set_path(install)
                self.assertEqual(str(app.apply_button["state"]), "normal")
                self.assertEqual(str(app.play_button["state"]), "normal")
                app.on_apply()
                self.assertEqual((install / "note.txt").read_text(encoding="utf-8"), "vi")
                self.assertEqual(str(app.remove_button["state"]), "normal")
                app.on_remove()
                self.assertEqual((install / "note.txt").read_text(encoding="utf-8"), "en")
                self.assertEqual(str(app.remove_button["state"]), "disabled")
            finally:
                window.destroy()


if __name__ == "__main__":
    unittest.main()
