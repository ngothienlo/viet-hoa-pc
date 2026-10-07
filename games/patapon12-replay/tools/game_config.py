"""Đường dẫn của máy này: thư mục cài, font, và file gốc trước khi vá.

Đọc `config.json` của game. Chưa có thì đọc `config.example.json`.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

GAME_DIR = Path(__file__).resolve().parents[1]
ROOT = GAME_DIR.parents[1]
EXE = "PATAPON12_REPLAY.exe"
DATA_NAME = "PATAPON12_REPLAY_Data"
DEFAULT_INSTALL = Path(r"C:\Program Files (x86)\Steam\steamapps\common\PATAPON12_REPLAY")


def load_config() -> dict:
    for name in ("config.json", "config.example.json"):
        path = GAME_DIR / name
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}


def install_dir() -> Path:
    """Thư mục cài đầu tiên có file exe. Không có thì trả đường dẫn đầu tiên đã điền."""
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


def font_path(kind: str) -> Path:
    raw = str((load_config().get("fonts") or {}).get(kind) or "").strip()
    if not raw or not Path(raw).is_file():
        raise SystemExit(f"Thiếu font fonts.{kind}. Điền đường dẫn TTF Be Vietnam Pro trong config.json.")
    return Path(raw)


def _applied_backup() -> Path | None:
    base = os.environ.get("LOCALAPPDATA")
    state = (Path(base) if base else Path.home() / "AppData" / "Local") / "viet-hoa-pc" / "state.json"
    if not state.is_file():
        return None
    row = (json.loads(state.read_text(encoding="utf-8")).get("games") or {}).get(GAME_DIR.name) or {}
    raw = str(row.get("backupDir") or "").strip()
    return Path(raw) if row.get("applied") and raw else None


def original(relative: str | Path) -> Path:
    """File gốc của game, kể cả khi launcher đã đè bản vá lên.

    Launcher chép file gốc vào thư mục sao lưu trước khi áp. Vá lại từ bản đã vá
    sẽ chồng glyph và atlas, nên script vá luôn đọc qua hàm này.
    """
    relative = Path(relative)
    backup = _applied_backup()
    if backup is not None and (backup / relative).is_file():
        return backup / relative
    return install_dir() / relative
