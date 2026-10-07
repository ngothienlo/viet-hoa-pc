"""Ghi tiếng Việt vào LocalizeData và mã hóa lại bundle để launcher áp.

Không cài BepInEx. Game đọc câu đã vá ngay trong asset.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import UnityPy

import extract_strings as ex

PATCH_DIR = (
    ex.GAME
    / "patch"
    / "PATAPON12_REPLAY_Data"
    / "StreamingAssets"
    / "aa"
    / "StandaloneWindows64"
)


def translations() -> dict[str, str]:
    """Chỉ đưa vào game câu viết tay. Bản dịch máy trả về tiếng Anh."""
    table: dict[str, str] = {}
    with ex.CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            note = (row.get("note") or "").strip()
            status = (row.get("status") or "").strip()
            source = row.get("source") or ""
            vi = row.get("vi") or ""
            machine = note in {"dịch máy", "nguồn tiếng Nhật", "không dịch", "lệch placeholder"}
            if vi.strip() and not machine:
                table[row["id"]] = vi
            else:
                table[row["id"]] = source
    return table


def fill(messages: list, product: str, suffix: str, table: dict[str, str]) -> int:
    changed = 0
    for index, current in enumerate(messages):
        key = f"{product}.{suffix}.{index}"
        if key not in table:
            continue
        if table[key] != current:
            messages[index] = table[key]
            changed += 1
    return changed


def fill_english(product: str, english: dict, table: dict[str, str]) -> int:
    changed = 0
    mission = english.get("missionData") or {}
    message = mission.get("message") or {}
    for key, value in zip(message.get("m_Keys") or [], message.get("m_Values") or []):
        changed += fill(value["messages"], product, f"mission.{key}.line", table)
    pre = mission.get("preMessage") or {}
    for key, value in zip(pre.get("m_Keys") or [], pre.get("m_Values") or []):
        changed += fill(value["messages"], product, f"mission.{key}.pre", table)
    colony = (english.get("colonyMsgData") or {}).get("message")
    if colony:
        changed += fill(colony["messages"], product, "colony", table)
    loading = english.get("loadingGroupData") or {}
    for suffix, field in (
        ("error", "errorMessage"),
        ("item", "itemMessage"),
        ("system", "systemMsg"),
        ("title", "titleMsg"),
        ("unit", "unitNameMsg"),
    ):
        node = loading.get(field)
        if node:
            changed += fill(node["messages"], product, suffix, table)
    image = english.get("imageData") or {}
    for suffix, field in (
        ("tips.title", "tipsTitle"),
        ("tips", "tipsText"),
        ("key", "keyGuide"),
        ("titlecard", "titleString"),
    ):
        node = image.get(field)
        if node:
            changed += fill(node["messages"], product, suffix, table)
    help_data = english.get("helpData") or {}
    for suffix, field in (("help.title", "helpTitle"), ("help.text", "helpText")):
        node = help_data.get(field)
        if node:
            changed += fill(node["messages"], product, suffix, table)
    guide = (english.get("guideData") or {}).get("tipsMessage")
    if guide:
        changed += fill(guide["messages"], product, "guide", table)
    return changed


def patch_one(product: str, filename: str, table: dict[str, str], hashes: list[bytes]) -> int:
    source = ex.original_bundle(filename)
    key = ex.bundle_key(source, hashes)
    env = ex.open_bundle(source, hashes)
    obj = env.container[ex.ASSETS[product]].deref()
    tree = obj.read_typetree()
    items = tree["items"]
    english = items["m_Values"][items["m_Keys"].index("EN")]
    changed = fill_english(product, english, table)
    obj.save_typetree(tree)
    patched = ex.save_bundle(env, key)
    check = UnityPy.load(patched if key is None else ex.decrypt(patched, key))
    if ex.ASSETS[product] not in check.container:
        raise RuntimeError(f"{product}: không đọc lại được LocalizeData")
    destination = PATCH_DIR / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(patched)
    print(f"{product}: {changed} câu -> {destination.name}")
    return changed


def main() -> None:
    if not ex.CATALOG.is_file():
        raise SystemExit(f"Không thấy catalog: {ex.CATALOG}")
    table = translations()
    hashes = ex.load_hashes()
    total = 0
    for product, filename in ex.HINTS.items():
        total += patch_one(product, filename, table, hashes)
    print(f"Đã vá {total} câu vào {len(ex.HINTS)} bundle.")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
