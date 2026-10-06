"""Đường dẫn đã chọn và bản sao lưu, nằm ngoài repo."""

from __future__ import annotations

import json
import os
from pathlib import Path


def default_state_dir() -> Path:
    root = os.environ.get("LOCALAPPDATA")
    base = Path(root) if root else Path.home() / "AppData" / "Local"
    return base / "viet-hoa-pc"


class Store:
    def __init__(self, state_dir: Path) -> None:
        self.state_dir = state_dir
        self.path = state_dir / "state.json"
        self.data = self._read()

    def _read(self) -> dict:
        if not self.path.is_file():
            return {"games": {}}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"games": {}}
        games = data.get("games")
        if not isinstance(games, dict):
            data["games"] = {}
        return data

    def save(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)

    def record(self, game_id: str) -> dict:
        games = self.data.setdefault("games", {})
        row = games.get(game_id)
        if not isinstance(row, dict):
            row = {}
            games[game_id] = row
        return row

    def install_path(self, game_id: str) -> str:
        value = self.record(game_id).get("installPath") or ""
        return str(value)

    def set_install_path(self, game_id: str, path: str) -> None:
        self.record(game_id)["installPath"] = path
        self.save()

    def applied_backup(self, game_id: str) -> Path | None:
        row = self.record(game_id)
        if not row.get("applied"):
            return None
        raw = str(row.get("backupDir") or "").strip()
        if not raw:
            return None
        return Path(raw)

    def mark_applied(self, game_id: str, install: Path, backup: Path) -> None:
        row = self.record(game_id)
        row["installPath"] = str(install)
        row["applied"] = True
        row["backupDir"] = str(backup)
        self.save()

    def mark_removed(self, game_id: str) -> None:
        row = self.record(game_id)
        row["applied"] = False
        row["backupDir"] = ""
        self.save()
