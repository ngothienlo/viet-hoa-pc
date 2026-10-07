"""Tải BepInEx và AutoTranslator vào patch/. Không ghi đè config của mình."""

from __future__ import annotations

import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path

GAME = Path(__file__).resolve().parents[1]
PATCH = GAME / "patch"
LOCK = GAME / "runtime.lock.json"
STAMP = PATCH / ".fetch-stamp.json"

ROOT_FILES = {"winhttp.dll", "doorstop_config.ini", ".doorstop_version"}
ROOT_DIRS = {"BepInEx", "dotnet"}
METADATA = {"icon.png", "manifest.json", "README.md"}
PROTECTED = {"BepInEx/config/AutoTranslatorConfig.ini"}


def select_members(names: list[str]) -> list[tuple[str, str]]:
    """Chọn file runtime. Trả (tên trong zip, đường dẫn trong patch/)."""
    files = [_safe_name(name) for name in names]
    files = [name for name in files if name]
    wrapper = _wrapper(files)
    selected: list[tuple[str, str]] = []
    for name in files:
        relative = name
        if wrapper:
            prefix = wrapper + "/"
            if not name.startswith(prefix):
                continue
            relative = name[len(prefix) :]
        if not _wanted(relative) or relative in PROTECTED:
            continue
        selected.append((name, relative))
    return selected


def extract_archive(blob: bytes, patch: Path) -> int:
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members = select_members(archive.namelist())
        for source, relative in members:
            destination = _destination(patch, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(source))
    return len(members)


def _safe_name(name: str) -> str:
    relative = name.replace("\\", "/").lstrip("/")
    if not relative or relative.endswith("/"):
        return ""
    parts = relative.split("/")
    if any(part in ("", "..") for part in parts) or ":" in parts[0]:
        raise ValueError(f"Đường dẫn trong zip không hợp lệ: {name}")
    return relative


def _wrapper(files: list[str]) -> str | None:
    tops = {name.split("/", 1)[0] for name in files}
    candidates: list[str] = []
    for top in tops:
        prefix = top + "/"
        inner = [name[len(prefix) :] for name in files if name.startswith(prefix)]
        if any(item in ROOT_FILES or item.startswith("BepInEx/") or item.startswith("dotnet/") for item in inner):
            candidates.append(top)
    if len(candidates) != 1:
        return None
    wrapper = candidates[0]
    outside = [name for name in files if not name.startswith(wrapper + "/")]
    if any("/" in name or name not in METADATA for name in outside):
        return None
    return wrapper


def _wanted(relative: str) -> bool:
    parts = relative.split("/")
    if parts[0] in ROOT_DIRS:
        return True
    return len(parts) == 1 and parts[0] in ROOT_FILES


def _destination(patch: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Đường dẫn không hợp lệ: {relative}")
    destination = (patch / path).resolve()
    base = patch.resolve()
    if destination != base and base not in destination.parents:
        raise ValueError(f"Đường dẫn thoát khỏi patch: {relative}")
    return destination


def _download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "viet-hoa-pc"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def _stamp_matches(archives: list[dict]) -> bool:
    if not STAMP.is_file():
        return False
    saved = json.loads(STAMP.read_text(encoding="utf-8"))
    expected = {item["id"]: item["sha256"] for item in archives}
    if saved != expected:
        return False
    required = (
        PATCH / "winhttp.dll",
        PATCH / "doorstop_config.ini",
        PATCH / ".doorstop_version",
        PATCH / "BepInEx" / "core" / "BepInEx.Unity.IL2CPP.dll",
        PATCH / "BepInEx" / "plugins" / "XUnity.AutoTranslator" / "XUnity.AutoTranslator.Plugin.BepInEx-IL2CPP.dll",
    )
    return all(path.is_file() for path in required)


def fetch(lock_path: Path = LOCK, patch: Path = PATCH) -> int:
    archives = json.loads(lock_path.read_text(encoding="utf-8"))["archives"]
    if patch == PATCH and _stamp_matches(archives):
        print("Runtime đã có trong patch/, đúng sha256.")
        return 0
    count = 0
    for item in archives:
        print(f"Tải {item['id']}...")
        blob = _download(item["url"])
        digest = hashlib.sha256(blob).hexdigest()
        if digest != item["sha256"]:
            raise SystemExit(f"Sai sha256 của {item['id']}: {digest}")
        count += extract_archive(blob, patch)
        print(f"  {item['id']}: {digest[:12]}")
    if patch == PATCH:
        STAMP.write_text(
            json.dumps({item["id"]: item["sha256"] for item in archives}, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Đã giải nén {count} file vào patch/.")
    return count


def main() -> None:
    fetch()


if __name__ == "__main__":
    main()
