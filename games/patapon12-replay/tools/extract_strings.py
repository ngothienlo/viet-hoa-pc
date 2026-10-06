"""Trích câu tiếng Anh từ LocalizeData.asset. Không cần chơi game.

Bundle Addressables được mã hóa bằng SeekableAesStream:
mật khẩu là m_Hash trong catalog, salt là tên file không có đuôi .bundle,
PasswordDeriveBytes SHA1 100 vòng, AES-128-ECB rồi XOR theo block.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import struct
import sys
from pathlib import Path

import UnityPy
from Crypto.Cipher import AES

GAME = Path(__file__).resolve().parents[1]
INSTALL = Path(r"C:\Program Files (x86)\Steam\steamapps\common\PATAPON12_REPLAY")
CATALOG = INSTALL / "PATAPON12_REPLAY_Data" / "StreamingAssets" / "aa" / "catalog.json"
BUNDLES = CATALOG.parent / "StandaloneWindows64"
CSV_PATH = GAME / "locale" / "vi" / "strings.csv"

ASSETS = {
    "P1": "Assets/AddressableMediaData/P1/Dat/LocalizeData.asset",
    "P1S": "Assets/AddressableMediaData/P1S/Dat/LocalizeData.asset",
    "P2": "Assets/AddressableMediaData/P2/Dat/LocalizeData.asset",
    "P2S": "Assets/AddressableMediaData/P2S/Dat/LocalizeData.asset",
}
# Tên file của catalog build ee778df8. Sai thì tool tự tìm lại.
HINTS = {
    "P1": "968081d6a0b7edd943f9968473020761.bundle",
    "P1S": "797f55c2af613b5783b10986ba38b526.bundle",
    "P2": "5592336601a9d01c95fc7ad67f9eeaea.bundle",
    "P2S": "372b82c7be935e013ea369be02d082cd.bundle",
}


def load_hashes() -> list[bytes]:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    raw = base64.b64decode(catalog["m_ExtraDataString"])
    hashes: list[bytes] = []
    for part in raw.split(b"AssetBundleRequestOptions")[1:]:
        length = int.from_bytes(part[:4], "little")
        row = json.loads(part[4 : 4 + length].decode("utf-16le"))
        hashes.append(row["m_Hash"].encode("ascii"))
    return hashes


def derive_key(password: bytes, salt: bytes) -> bytes:
    digest = hashlib.sha1(password + salt).digest()
    for _ in range(99):
        digest = hashlib.sha1(digest).digest()
    return digest[:16]


def decrypt(data: bytes, key: bytes) -> bytes:
    blocks = (len(data) + 15) // 16
    nonces = bytearray(blocks * 16)
    for index in range(blocks):
        struct.pack_into("<Q", nonces, index * 16, index + 1)
    stream = AES.new(key, AES.MODE_ECB).encrypt(bytes(nonces))
    return bytes(left ^ right for left, right in zip(data, stream))


def open_bundle(path: Path, hashes: list[bytes]):
    data = path.read_bytes()
    if data.startswith(b"UnityFS"):
        return UnityPy.load(data)
    stem = path.stem.encode("ascii")
    for password in hashes:
        key = derive_key(password, stem)
        nonce = (1).to_bytes(8, "little") + b"\x00" * 8
        head = bytes(a ^ b for a, b in zip(data[:7], AES.new(key, AES.MODE_ECB).encrypt(nonce)))
        if head == b"UnityFS":
            return UnityPy.load(decrypt(data, key))
    raise RuntimeError(f"Không giải được {path.name}")


def add_lines(rows: list[dict[str, str]], product: str, context: str, suffix: str, messages: list) -> None:
    for index, text in enumerate(messages):
        source = text if isinstance(text, str) else ""
        rows.append(
            {
                "id": f"{product}.{suffix}.{index}",
                "context": context,
                "source": source,
                "vi": "",
                "status": "todo",
                "note": "",
            }
        )


def _lines(node: dict | None) -> list:
    if not node:
        return []
    return list(node.get("messages") or [])


def _keyed(node: dict | None) -> list[tuple[str, list]]:
    if not node:
        return []
    return list(zip(node.get("m_Keys") or [], node.get("m_Values") or []))


def rows_from_english(product: str, english: dict) -> list[dict[str, str]]:
    known = {"missionData", "colonyMsgData", "loadingGroupData", "imageData", "helpData", "guideData"}
    extra = set(english) - known
    if extra:
        raise RuntimeError(f"{product} có nhóm chưa khai: " + ", ".join(sorted(extra)))
    rows: list[dict[str, str]] = []
    mission = english.get("missionData") or {}
    for key, value in _keyed(mission.get("message")):
        add_lines(rows, product, "dialog", f"mission.{key}.line", value["messages"])
    for key, value in _keyed(mission.get("preMessage")):
        add_lines(rows, product, "dialog", f"mission.{key}.pre", value["messages"])
    colony = (english.get("colonyMsgData") or {}).get("message")
    add_lines(rows, product, "dialog", "colony", _lines(colony))
    loading = english.get("loadingGroupData") or {}
    add_lines(rows, product, "ui", "error", _lines(loading.get("errorMessage")))
    add_lines(rows, product, "item", "item", _lines(loading.get("itemMessage")))
    add_lines(rows, product, "ui", "system", _lines(loading.get("systemMsg")))
    add_lines(rows, product, "ui", "title", _lines(loading.get("titleMsg")))
    add_lines(rows, product, "item", "unit", _lines(loading.get("unitNameMsg")))
    image = english.get("imageData") or {}
    image_known = {"tipsTitle", "tipsText", "keyGuide", "titleString"}
    image_extra = set(image) - image_known
    if image_extra:
        raise RuntimeError(f"{product} imageData có nhóm chưa khai: " + ", ".join(sorted(image_extra)))
    add_lines(rows, product, "tips", "tips.title", _lines(image.get("tipsTitle")))
    add_lines(rows, product, "tips", "tips", _lines(image.get("tipsText")))
    add_lines(rows, product, "ui", "key", _lines(image.get("keyGuide")))
    add_lines(rows, product, "ui", "titlecard", _lines(image.get("titleString")))
    help_data = english.get("helpData") or {}
    add_lines(rows, product, "help", "help.title", _lines(help_data.get("helpTitle")))
    add_lines(rows, product, "help", "help.text", _lines(help_data.get("helpText")))
    guide = (english.get("guideData") or {}).get("tipsMessage")
    add_lines(rows, product, "tips", "guide", _lines(guide))
    return rows


def english_of(tree: dict) -> dict:
    items = tree["items"]
    keys = items["m_Keys"]
    if "EN" not in keys:
        raise RuntimeError("LocalizeData không có tiếng Anh")
    return items["m_Values"][keys.index("EN")]


def take(env, path: Path, wanted: dict[str, str], rows: list[dict[str, str]]) -> None:
    found = [name for name, asset in wanted.items() if asset in env.container]
    for name in found:
        tree = env.container[wanted.pop(name)].read_typetree()
        product_rows = rows_from_english(name, english_of(tree))
        print(f"{name}: {len(product_rows)} câu từ {path.name}")
        rows.extend(product_rows)


def collect(hashes: list[bytes]) -> list[dict[str, str]]:
    wanted = dict(ASSETS)
    rows: list[dict[str, str]] = []
    for product, filename in HINTS.items():
        path = BUNDLES / filename
        if product not in wanted or not path.is_file():
            continue
        take(open_bundle(path, hashes), path, wanted, rows)
    if wanted:
        for path in sorted(BUNDLES.glob("*.bundle")):
            if not wanted:
                break
            take(open_bundle(path, hashes), path, wanted, rows)
    if wanted:
        raise SystemExit("Không thấy LocalizeData của " + ", ".join(wanted))
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, ["id", "context", "source", "vi", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if not CATALOG.is_file():
        raise SystemExit(f"Không thấy catalog: {CATALOG}")
    rows = collect(load_hashes())
    write_csv(rows)
    print(f"Đã ghi {len(rows)} câu vào {CSV_PATH}")


if __name__ == "__main__":
    sys.exit(main())
