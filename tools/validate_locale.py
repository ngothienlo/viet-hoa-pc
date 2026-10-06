"""Kiểm tra locale/vi/strings.csv trước khi đóng gói bản dịch."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "locale" / "vi" / "strings.csv"
REQUIRED = ["id", "context", "source", "vi", "status", "note"]
STATUSES = {"todo", "draft", "review", "done"}
TOKEN = re.compile(r"(\{[^{}]+\}|%[sdif]|</?[A-Za-z][^>]*>|\\n)")


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def main() -> int:
    if not CSV_PATH.is_file():
        print(f"Thiếu file: {CSV_PATH}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    rows = 0

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [name.strip() for name in (reader.fieldnames or [])]
        if fieldnames != REQUIRED:
            print("Cột phải đúng thứ tự: " + ",".join(REQUIRED))
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
                errors.append(f"Dòng {line_no} ({key}): status {status} nhưng chưa có bản dịch")
            if vi.strip() and tokens(source) != tokens(vi):
                errors.append(
                    f"Dòng {line_no} ({key}): placeholder lệch. "
                    f"Gốc {tokens(source)} / Việt {tokens(vi)}"
                )
            if vi.strip() and source.strip() == vi.strip():
                warnings.append(f"Dòng {line_no} ({key}): bản dịch giống chuỗi gốc")

    print(f"Đã đọc {rows} dòng từ {CSV_PATH.relative_to(ROOT)}")
    for message in warnings:
        print("Cảnh báo: " + message)
    for message in errors:
        print("Lỗi: " + message)
    if errors:
        print(f"{len(errors)} lỗi.")
        return 1
    print("Ổn.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
