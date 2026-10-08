"""Gộp file dịch (JSON) vào `locale/vi/strings.csv` của Potion Permit.

Mỗi file là một mảng JSON `{"id": ..., "vi": ...}` (thêm `"reason"` nếu là bản sửa).
Câu bị loại nếu lệch placeholder (`{[CHARACTER_NAME]}`, `{0}`), thẻ màu (`<#a27dde>`,
`</color>`), số lần xuống dòng, hoặc có khoảng trắng thừa ở đầu, cuối. Hai file cho cùng
một id hai câu khác nhau thì báo xung đột và bỏ qua. Câu nhận vào lên `review`.

    python games/potion-permit/tools/apply_fixes.py --dry-run part1.json part2.json
    python games/potion-permit/tools/apply_fixes.py part1.json part2.json
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[1] / "locale" / "vi" / "strings.csv"
FIELDS = ["id", "context", "source", "vi", "status", "note"]
TOKEN = re.compile(r"\{[^{}]+\}|<#[0-9A-Fa-f]{3,8}>|</?[A-Za-z][^>]*>")


def problems(source: str, vi: str) -> list[str]:
    found = []
    if not vi.strip():
        found.append("câu Việt trống")
    if sorted(TOKEN.findall(source)) != sorted(TOKEN.findall(vi)):
        found.append(f"placeholder hoặc thẻ lệch: {TOKEN.findall(source)} và {TOKEN.findall(vi)}")
    if source.count("\n") != vi.count("\n"):
        found.append(f"số dòng lệch ({source.count(chr(10))} và {vi.count(chr(10))})")
    if vi != vi.strip() and source == source.strip():
        found.append("khoảng trắng đầu hoặc cuối")
    if "\r" in vi:
        found.append("có ký tự \\r")
    # Thẻ màu phải mở trước khi đóng, như câu gốc.
    if [tag.startswith("</") for tag in re.findall(r"</?color>|<#[0-9A-Fa-f]{3,8}>", vi)] != [
        tag.startswith("</") for tag in re.findall(r"</?color>|<#[0-9A-Fa-f]{3,8}>", source)
    ]:
        found.append("thứ tự mở, đóng thẻ màu lệch")
    return found


def load_fixes(paths: list[Path]) -> tuple[dict[str, str], list[str]]:
    chosen: dict[str, tuple[str, str]] = {}
    report: list[str] = []
    conflicts: set[str] = set()
    for path in paths:
        for item in json.loads(path.read_text(encoding="utf-8")):
            key, vi = item["id"], item["vi"]
            if key in chosen and chosen[key][0] != vi:
                conflicts.add(key)
                report.append(f"xung đột {path.name} và {chosen[key][1]}: {key}")
                continue
            chosen[key] = (vi, path.name)
    return {key: vi for key, (vi, _name) in chosen.items() if key not in conflicts}, report


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="chỉ kiểm tra, không ghi CSV")
    args = parser.parse_args()

    fixes, report = load_fixes(args.files)
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    by_id = {row["id"]: row for row in rows}
    accepted = 0
    for key, vi in fixes.items():
        row = by_id.get(key)
        if row is None:
            report.append(f"không có id trong CSV: {key}")
            continue
        issues = problems(row["source"], vi)
        if issues:
            report.append(f"loại {key}: {'; '.join(issues)}")
            continue
        row["vi"] = vi
        row["status"] = "review"
        row["note"] = "giữ nguyên" if vi == row["source"] else "viết tay"
        accepted += 1
    for line in report:
        print(line)
    print(f"{len(fixes)} câu đề xuất, nhận {accepted}, loại {len(fixes) - accepted}")
    if args.dry_run:
        return 1 if report else 0
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
