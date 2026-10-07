"""Áp và gỡ file trong patch/ lên thư mục cài. Có sao lưu file gốc."""

from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import shutil
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

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


# Mỗi lần chỉ một build: script build đặt biến môi trường và nạp lại module của game.
_BUILD_LOCK = threading.Lock()


@contextlib.contextmanager
def scoped_env(values: dict[str, str]):
    """Đặt biến môi trường trong khối with, rồi trả lại giá trị cũ."""
    saved = {key: os.environ.get(key) for key in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for key, old in saved.items():
            if old is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old


def build_dir(game: Game, store: Store) -> Path:
    return store.state_dir / "build" / game.id


def pack_source(game: Game, store: Store) -> Path:
    """Nơi lấy file để áp: thư mục build nếu game có bước build, không thì patch/."""
    return build_dir(game, store) if game.build else game.patch_dir


def run_build(game: Game, install: Path, store: Store, log: Callable[[str], None]) -> Result:
    """Chạy script build của game trên bản cài, ghi file vá vào thư mục build.

    Script nhận (thư mục cài, thư mục ra, hàm log) và đọc file gốc qua bản sao lưu
    của launcher, nên chạy lại sau khi đã áp vẫn ra cùng kết quả.
    """
    if game.build is None:
        return Result(True, "Game này không cần build.")
    error = install_error(game, install)
    if error:
        return Result(False, error)
    if not game.build.is_file():
        return Result(False, f"Không thấy script build: {game.build.name}")
    try:
        with _BUILD_LOCK, scoped_env({"VH_STATE_DIR": str(store.state_dir)}):
            spec = importlib.util.spec_from_file_location(f"vh_build_{game.id.replace('-', '_')}", game.build)
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            module.build(install, build_dir(game, store), log)
    except SystemExit as exc:
        return Result(False, str(exc) or "Không tạo được bản vá.")
    except Exception as exc:  # noqa: BLE001 - lỗi nào cũng phải hiện lên cửa sổ
        return Result(False, f"Không tạo được bản vá: {exc}")
    count = len(pack_files(game, build_dir(game, store)))
    return Result(True, f"Đã tạo {count} file vá.", count)


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
    files = pack_files(game, pack_source(game, store))
    if not files:
        return Result(False, "Chưa có file vá. Chưa áp gì vào thư mục cài.")
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
