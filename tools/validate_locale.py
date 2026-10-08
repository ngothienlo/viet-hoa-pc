"""Kiểm tra locale/vi/strings.csv của một game hoặc mọi game trong games/."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAMES = ROOT / "games"
REQUIRED = ["id", "context", "source", "vi", "status", "note"]
STATUSES = {"todo", "draft", "review", "done"}
# Placeholder, thẻ rich text (cả thẻ màu `<#ff1d1d>` của TextMesh Pro) và `\n` viết bằng hai ký tự.
TOKEN = re.compile(r"(\{[^{}]+\}|%[sdif]|</?[A-Za-z][^>]*>|<#[0-9A-Fa-f]{3,8}>|\\n)")


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def same_tokens(source: str, vi: str) -> bool:
    """Placeholder `{…}`, `%s` được đổi chỗ (trật tự từ tiếng Việt khác tiếng Anh).
    Thẻ và `\\n` phải giữ đúng thứ tự, vì thẻ mở và đóng đi theo cặp."""
    def split(text: str) -> tuple[list[str], list[str]]:
        found = tokens(text)
        movable = sorted(token for token in found if token.startswith(("{", "%")))
        fixed = [token for token in found if not token.startswith(("{", "%"))]
        return movable, fixed

    return split(source) == split(vi)


def game_dirs(args: list[str]) -> list[Path]:
    if args:
        found: list[Path] = []
        for arg in args:
            path = Path(arg)
            if not path.is_absolute():
                path = ROOT / path
            found.append(path)
        return found
    return sorted(
        path.parent.parent.parent
        for path in GAMES.glob("*/locale/vi/strings.csv")
    )


def check(game_dir: Path) -> int:
    csv_path = game_dir / "locale" / "vi" / "strings.csv"
    label = game_dir.name
    if not csv_path.is_file():
        print(f"{label}: thiếu {csv_path}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    rows = 0

    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [name.strip() for name in (reader.fieldnames or [])]
        if fieldnames != REQUIRED:
            print(f"{label}: cột phải đúng thứ tự: " + ",".join(REQUIRED))
            return 1
        for line_no, row in enumerate(reader, start=2):
            rows += 1
            key = (row.get("id") or "").strip()
            source = row.get("source") or ""
            vi = row.get("vi") or ""
            status = (row.get("status") or "").strip()
            if not key:
                errors.append(f"Dòng {line_no}: thiếu id")
                continue
            if key in seen:
                errors.append(f"Dòng {line_no}: id trùng {key}")
            seen.add(key)
            if key.startswith("EXAMPLE"):
                continue
            if status not in STATUSES:
                errors.append(f"Dòng {line_no} ({key}): status '{status}' không hợp lệ")
            if status in {"review", "done"} and not vi.strip():
                errors.append(
                    f"Dòng {line_no} ({key}): status {status} nhưng chưa có bản dịch"
                )
            if vi.strip() and not same_tokens(source, vi):
                errors.append(
                    f"Dòng {line_no} ({key}): placeholder lệch. "
                    f"Gốc {tokens(source)} / Việt {tokens(vi)}"
                )
            note = (row.get("note") or "").strip()
            if vi.strip() and source.strip() == vi.strip() and note != "giữ nguyên":
                warnings.append(f"Dòng {line_no} ({key}): bản dịch giống chuỗi gốc")

    shown = csv_path
    try:
        shown = csv_path.relative_to(ROOT)
    except ValueError:
        pass
    print(f"{label}: đã đọc {rows} dòng từ {shown}")
    for message in warnings:
        print(f"{label}: cảnh báo: {message}")
    for message in errors:
        print(f"{label}: lỗi: {message}")
    if errors:
        print(f"{label}: {len(errors)} lỗi.")
        return 1
    print(f"{label}: ổn.")
    return 0


def main() -> int:
    dirs = game_dirs(sys.argv[1:])
    if not dirs:
        print("Không có game nào trong games/.")
        return 1
    failed = 0
    for game_dir in dirs:
        failed += check(game_dir)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
