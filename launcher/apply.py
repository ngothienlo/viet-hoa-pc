"""Áp và gỡ file trong patch/ lên thư mục cài. Có sao lưu file gốc."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from launcher.catalog import Game, pack_files
from launcher.store import Store


@dataclass(frozen=True)
class Result:
    ok: bool
    message: str
    file_count: int = 0


def install_error(game: Game, install: Path | None) -> str | None:
    if install is None or not str(install).strip():
        return "Chưa chọn thư mục cài."
    if not install.is_dir():
        return "Thư mục không tồn tại."
    missing = [rel for rel in game.detect if not (install / rel).is_file()]
    if missing:
        return "Không thấy " + ", ".join(missing) + "."
    return None


def inside(root: Path, relative: Path) -> Path:
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Đường dẫn không hợp lệ: {relative}")
    destination = (root / relative).resolve()
    base = root.resolve()
    if destination != base and base not in destination.parents:
        raise ValueError(f"Đường dẫn thoát khỏi thư mục: {relative}")
    return destination


def apply_pack(game: Game, install: Path, store: Store) -> Result:
    error = install_error(game, install)
    if error:
        return Result(False, error)
    files = pack_files(game)
    if not files:
        return Result(False, "Chưa có file trong patch/. Chưa áp gì vào thư mục cài.")
    if store.applied_backup(game.id) is not None:
        removed = remove_pack(game, install, store)
        if not removed.ok:
            return removed
    backup = store.state_dir / "backups" / game.id / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    done: list[dict] = []
    try:
        for source, relative in files:
            destination = inside(install, relative)
            if destination.exists() and not destination.is_file():
                raise ValueError(f"{relative.as_posix()} không phải file.")
            existed = destination.is_file()
            if existed:
                saved = inside(backup, relative)
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(destination, saved)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            done.append({"rel": relative.as_posix(), "existed": existed})
    except (OSError, ValueError) as exc:
        _restore(install, backup, done)
        return Result(False, str(exc))
    backup.mkdir(parents=True, exist_ok=True)
    (backup / "manifest.json").write_text(
        json.dumps({"install": str(install), "files": done}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    store.mark_applied(game.id, install, backup)
    return Result(True, f"Đã áp {len(done)} file.", len(done))


def remove_pack(game: Game, install: Path, store: Store) -> Result:
    backup = store.applied_backup(game.id)
    if backup is None:
        return Result(False, "Chưa áp bản dịch trên game này.")
    manifest_path = backup / "manifest.json"
    if not manifest_path.is_file():
        return Result(False, "Không còn bản sao lưu để gỡ.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    saved_install = Path(str(manifest.get("install") or ""))
    if saved_install.resolve() != install.resolve():
        return Result(False, "Bản dịch đang gắn với thư mục khác. Hãy chọn lại đúng thư mục đã áp.")
    files = manifest.get("files") or []
    try:
        _restore(install, backup, files)
    except (OSError, ValueError) as exc:
        return Result(False, str(exc))
    store.mark_removed(game.id)
    return Result(True, f"Đã gỡ {len(files)} file.", len(files))


def _restore(install: Path, backup: Path, files: list[dict]) -> None:
    for item in reversed(files):
        relative = Path(str(item["rel"]))
        destination = inside(install, relative)
        if item.get("existed"):
            source = inside(backup, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        elif destination.is_file():
            destination.unlink()
