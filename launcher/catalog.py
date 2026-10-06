"""Đọc danh sách game từ games/*/game.json."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Game:
    id: str
    title: str
    summary: str
    root: Path
    exe: str | None
    detect: tuple[str, ...]
    hints: tuple[Path, ...]

    @property
    def patch_dir(self) -> Path:
        return self.root / "patch"


def load_games(repo: Path) -> list[Game]:
    games_dir = repo / "games"
    if not games_dir.is_dir():
        return []
    found: list[Game] = []
    for manifest in sorted(games_dir.glob("*/game.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        root = manifest.parent
        game_id = str(data.get("id") or root.name).strip()
        detect = tuple(str(item) for item in data.get("detect") or [] if str(item).strip())
        exe = data.get("exe")
        found.append(
            Game(
                id=game_id,
                title=str(data.get("title") or game_id),
                summary=str(data.get("summary") or "").strip(),
                root=root,
                exe=str(exe).strip() if exe else None,
                detect=detect,
                hints=tuple(_hints(root)),
            )
        )
    return found


def _hints(root: Path) -> list[Path]:
    example = root / "config.example.json"
    if not example.is_file():
        return []
    data = json.loads(example.read_text(encoding="utf-8"))
    installs = data.get("installs") or {}
    hints: list[Path] = []
    if isinstance(installs, dict):
        for value in installs.values():
            if isinstance(value, str) and value.strip():
                hints.append(Path(value.strip()))
    return hints


def pack_files(game: Game) -> list[tuple[Path, Path]]:
    """File trong patch/, bỏ file ẩn. Trả (nguồn, đường dẫn tương đối)."""
    patch = game.patch_dir
    if not patch.is_dir():
        return []
    files: list[tuple[Path, Path]] = []
    for path in sorted(patch.rglob("*")):
        if not path.is_file() or any(part.startswith(".") for part in path.relative_to(patch).parts):
            continue
        files.append((path, path.relative_to(patch)))
    return files
