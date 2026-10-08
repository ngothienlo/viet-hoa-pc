"""Đường dẫn của máy này: thư mục cài, thư mục ra, và file gốc trước khi vá.

Launcher (và bản exe) đặt `VH_INSTALL_DIR`, `VH_PATCH_DIR`, `VH_STATE_DIR` trước khi gọi script vá.
Không có biến môi trường thì đọc `config.json` của game, rồi `config.example.json`.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

GAME_DIR = Path(__file__).resolve().parents[1]
EXE = "Potion Permit.exe"
DATA_NAME = "Potion Permit_Data"
UNITY = "2020.1.1f1"
DEFAULT_INSTALL = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Potion Permit")


def load_config() -> dict:
    for name in ("config.json", "config.example.json"):
        path = GAME_DIR / name
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}


def install_dir() -> Path:
    """Thư mục cài đầu tiên có file exe. Không có thì trả đường dẫn đầu tiên đã điền."""
    chosen = os.environ.get("VH_INSTALL_DIR", "").strip()
    if chosen:
        return Path(chosen)
    installs = load_config().get("installs") or {}
    filled = [Path(value) for value in installs.values() if isinstance(value, str) and value.strip()]
    for path in filled:
        if (path / EXE).is_file():
            return path
    return filled[0] if filled else DEFAULT_INSTALL


def require_install() -> Path:
    path = install_dir()
    if not (path / EXE).is_file():
        raise SystemExit(f"Không thấy {EXE} trong {path}. Điền installs trong config.json của game.")
    return path


def patch_dir() -> Path:
    """Nơi ghi file vá. Mặc định là `patch/` của game; launcher trỏ sang thư mục build."""
    chosen = os.environ.get("VH_PATCH_DIR", "").strip()
    return Path(chosen) if chosen else GAME_DIR / "patch"


def _applied_backup() -> Path | None:
    chosen = os.environ.get("VH_STATE_DIR", "").strip()
    base = os.environ.get("LOCALAPPDATA")
    state_dir = Path(chosen) if chosen else (Path(base) if base else Path.home() / "AppData" / "Local") / "viet-hoa-pc"
    state = state_dir / "state.json"
    if not state.is_file():
        return None
    row = (json.loads(state.read_text(encoding="utf-8")).get("games") or {}).get(GAME_DIR.name) or {}
    raw = str(row.get("backupDir") or "").strip()
    return Path(raw) if row.get("applied") and raw else None


def original(relative: str | Path) -> Path:
    """File gốc của game, kể cả khi launcher đã đè bản vá lên.

    Launcher chép file gốc vào thư mục sao lưu trước khi áp. Vá lại từ bản đã vá
    sẽ ghi chồng, nên script vá luôn đọc qua hàm này.
    """
    relative = Path(relative)
    backup = _applied_backup()
    if backup is not None and (backup / relative).is_file():
        return backup / relative
    return install_dir() / relative
