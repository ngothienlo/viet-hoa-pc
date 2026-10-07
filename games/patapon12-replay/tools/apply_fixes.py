"""Gộp file sửa bản dịch vào `locale/vi/strings.csv`.

Mỗi file là một mảng JSON `{"source": ..., "vi": ..., "reason": ...}`. `source` phải
chép y nguyên câu gốc. Câu mới được ghi cho mọi dòng cùng câu gốc, lên `review`,
note `viết tay` (hoặc `giữ nguyên` khi câu Việt trùng câu gốc).

Câu bị loại nếu lệch số `/`, mã `&H…#`, placeholder `<N…>`, ký hiệu nút, hoặc có
xuống dòng thật. Hai file sửa cùng một câu gốc khác nhau thì báo xung đột và bỏ qua.

    python games/patapon12-replay/tools/apply_fixes.py fixes1.json fixes2.json
    python games/patapon12-replay/tools/apply_fixes.py --dry-run fixes*.json
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
CODE = re.compile(r"&H[0-9A-Z]+#")
HOLDER = re.compile(r"<N[O0-9]+>")
SYMBOLS = "○□△×・♪☆【】"


def problems(source: str, vi: str) -> list[str]:
    found = []
    if not vi.strip():
        found.append("câu Việt trống")
    if source.count("/") != vi.count("/"):
        found.append(f"số / lệch ({source.count('/')} và {vi.count('/')})")
    if CODE.findall(source) != CODE.findall(vi):
        found.append("mã &H…# lệch")
    if sorted(HOLDER.findall(source)) != sorted(HOLDER.findall(vi)):
        found.append("placeholder lệch")
    for ch in SYMBOLS:
        if source.count(ch) != vi.count(ch):
            found.append(f"ký hiệu {ch} lệch")
    if "\n" in vi or "\r" in vi:
        found.append("có xuống dòng thật")
    if vi != vi.strip():
        found.append("khoảng trắng đầu hoặc cuối")
    return found


def load_fixes(paths: list[Path]) -> tuple[dict[str, str], list[str]]:
    chosen: dict[str, tuple[str, str]] = {}
    report: list[str] = []
    conflicts: set[str] = set()
    for path in paths:
        for item in json.loads(path.read_text(encoding="utf-8")):
            source, vi = item["source"], item["vi"]
            if source in chosen and chosen[source][0] != vi:
                conflicts.add(source)
                report.append(f"xung đột {path.name} và {chosen[source][1]}: {source[:60]!r}")
                continue
            chosen[source] = (vi, path.name)
    fixes = {source: vi for source, (vi, _name) in chosen.items() if source not in conflicts}
    return fixes, report


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="chỉ kiểm tra, không ghi CSV")
    args = parser.parse_args()

    fixes, report = load_fixes(args.files)
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    sources = {row["source"] for row in rows}

    accepted: dict[str, str] = {}
    for source, vi in fixes.items():
        if source not in sources:
            report.append(f"không có trong CSV: {source[:60]!r}")
            continue
        issues = problems(source, vi)
        if issues:
            report.append(f"loại ({'; '.join(issues)}): {source[:60]!r}")
            continue
        accepted[source] = vi

    changed_rows = 0
    changed_sources = set()
    for row in rows:
        vi = accepted.get(row["source"])
        if vi is None:
            continue
        note = "giữ nguyên" if vi == row["source"] else "viết tay"
        if row["vi"] != vi or row["status"] != "review" or row["note"] != note:
            row["vi"] = vi
            row["status"] = "review"
            row["note"] = note
            changed_rows += 1
            changed_sources.add(row["source"])

    for line in report:
        print(line)
    print(f"{len(fixes)} câu đề xuất, nhận {len(accepted)}, đổi {len(changed_sources)} câu gốc ({changed_rows} dòng)")
    if args.dry_run:
        return 1 if report else 0
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
