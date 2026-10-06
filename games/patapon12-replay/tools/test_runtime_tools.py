"""Kiểm tra giải nén runtime và endpoint echo, không tải mạng."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import threading
import unittest
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


def load(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


fetch = load("fetch_runtime.py")
echo = load("echo_translate.py")


class FetchTests(unittest.TestCase):
    def test_strips_thunderstore_wrapper_and_skips_metadata(self) -> None:
        names = [
            "icon.png",
            "manifest.json",
            "README.md",
            "BepInExPack/changelog.txt",
            "BepInExPack/winhttp.dll",
            "BepInExPack/doorstop_config.ini",
            "BepInExPack/.doorstop_version",
            "BepInExPack/BepInEx/core/BepInEx.Core.dll",
            "BepInExPack/dotnet/coreclr.dll",
            "BepInExPack/BepInEx/config/AutoTranslatorConfig.ini",
        ]
        selected = dict(fetch.select_members(names))
        self.assertEqual(
            set(selected),
            {
                "BepInExPack/winhttp.dll",
                "BepInExPack/doorstop_config.ini",
                "BepInExPack/.doorstop_version",
                "BepInExPack/BepInEx/core/BepInEx.Core.dll",
                "BepInExPack/dotnet/coreclr.dll",
            },
        )
        self.assertEqual(selected["BepInExPack/winhttp.dll"], "winhttp.dll")
        self.assertEqual(selected["BepInExPack/.doorstop_version"], ".doorstop_version")
        self.assertNotIn("BepInExPack/BepInEx/config/AutoTranslatorConfig.ini", selected)

    def test_keeps_plugin_zip_rooted_at_bepinex(self) -> None:
        names = ["BepInEx/plugins/XUnity.AutoTranslator/CustomTranslate.dll"]
        selected = fetch.select_members(names)
        self.assertEqual(selected, [(names[0], names[0])])

    def test_rejects_zip_slip(self) -> None:
        with self.assertRaises(ValueError):
            fetch.select_members(["../outside.dll"])

    def test_extract_does_not_overwrite_our_ini(self) -> None:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("icon.png", b"icon")
            archive.writestr("BepInExPack/winhttp.dll", b"dll")
            archive.writestr("BepInExPack/BepInEx/config/AutoTranslatorConfig.ini", b"THEIRS")
        with tempfile.TemporaryDirectory() as raw:
            patch = Path(raw)
            ini = patch / "BepInEx" / "config" / "AutoTranslatorConfig.ini"
            ini.parent.mkdir(parents=True)
            ini.write_bytes(b"OURS")
            count = fetch.extract_archive(buffer.getvalue(), patch)
            self.assertEqual(count, 1)
            self.assertEqual(ini.read_bytes(), b"OURS")
            self.assertEqual((patch / "winhttp.dll").read_bytes(), b"dll")
            self.assertFalse((patch / "icon.png").exists())


class EchoTests(unittest.TestCase):
    def test_set_ini_replaces_endpoint_without_touching_fallback(self) -> None:
        original = "[Service]\nEndpoint=GoogleTranslate\nFallbackEndpoint=\n"
        updated = echo.set_ini_values(original, {"Service": {"Endpoint": "CustomTranslate"}})
        self.assertEqual(
            [line for line in updated.splitlines() if "Endpoint" in line],
            ["Endpoint=CustomTranslate", "FallbackEndpoint="],
        )

    def test_set_ini_appends_missing_section(self) -> None:
        updated = echo.set_ini_values("[Service]\nEndpoint=\n", {"Custom": {"Url": "http://127.0.0.1:8765/translate"}})
        self.assertIn("[Custom]\nUrl=http://127.0.0.1:8765/translate\n", updated)

    def test_handler_echoes_and_records_unique_lines(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "captured-en.jsonl"
            echo.capture_path = path
            echo._seen.clear()
            server = echo.serve(0)
            port = server.server_address[1]
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                for _ in range(2):
                    url = "http://127.0.0.1:%s/translate?%s" % (
                        port,
                        urllib.parse.urlencode({"from": "en", "to": "vi", "text": "Pata Pon"}),
                    )
                    with urllib.request.urlopen(url, timeout=5) as response:
                        self.assertEqual(response.read().decode("utf-8"), "Pata Pon")
            finally:
                server.shutdown()
                server.server_close()
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows, [{"text": "Pata Pon"}])


if __name__ == "__main__":
    unittest.main()
