"""Ghi tiếng Việt vào LocalizeData và mã hóa lại bundle để launcher áp.

Không cài BepInEx. Game đọc câu đã vá ngay trong asset.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import UnityPy
from Crypto.Cipher import AES

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
            if note in {"viết tay", "giữ nguyên"} or status == "review":
                table[row["id"]] = vi if vi else source
            else:
                table[row["id"]] = source
    return table


def key_for(path: Path, hashes: list[bytes]) -> bytes:
    data = path.read_bytes()[:16]
    stem = path.stem.encode("ascii")
    for password in hashes:
        key = ex.derive_key(password, stem)
        nonce = (1).to_bytes(8, "little") + b"\x00" * 8
        head = bytes(a ^ b for a, b in zip(data[:7], AES.new(key, AES.MODE_ECB).encrypt(nonce)))
        if head == b"UnityFS":
            return key
    raise RuntimeError(f"Không giải được {path.name}")


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
    source = ex.BUNDLES / filename
    cipher = source.read_bytes()
    key = key_for(source, hashes)
    env = UnityPy.load(ex.decrypt(cipher, key))
    obj = env.container[ex.ASSETS[product]].deref()
    tree = obj.read_typetree()
    items = tree["items"]
    english = items["m_Values"][items["m_Keys"].index("EN")]
    changed = fill_english(product, english, table)
    obj.save_typetree(tree)
    plain = next(iter(env.files.values())).save(packer="original")
    if not plain.startswith(b"UnityFS"):
        raise RuntimeError(f"{product}: bundle sau khi ghi không phải UnityFS")
    patched = ex.decrypt(plain, key)
    check = UnityPy.load(ex.decrypt(patched, key))
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
