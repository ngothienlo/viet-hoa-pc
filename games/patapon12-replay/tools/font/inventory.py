"""Kiểm kê TMP Font Asset của PATAPON 1+2 REPLAY, ghi vào `fonts.json`.

Quét một lần cho mỗi bản game. Session sau đọc `fonts.json`, không cần quét lại.
Script ghi sha1 của `catalog.json`. Game cập nhật thì sha1 đổi, khi đó mới quét lại.

    python games/patapon12-replay/tools/font/inventory.py
    python games/patapon12-replay/tools/font/inventory.py --check

Không tham số: quét bản gốc (qua `original()`, bỏ qua bản đã vá), ghi `fonts.json`.
`--check`: đọc file đã vá trong `patch/`, báo font cần vá nào còn thiếu chữ của
cột `vi`. Mã thoát 1 nếu còn thiếu.
"""

from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import io
import json
import re
import sys
from datetime import date
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import extract_strings as ex  # noqa: E402
from apply_locale_patch import translations  # noqa: E402
from game_config import DATA_NAME, GAME_DIR, original, patch_dir, require_install  # noqa: E402

UNITY = "2022.3.52f1"
OUT = Path(__file__).with_name("fonts.json")
CSV_PATH = GAME_DIR / "locale" / "vi" / "strings.csv"
PATCH = patch_dir()
LANGUAGE = re.compile(r"/Localize/([A-Za-z]+)/")

# Cách vá theo tên font. Thứ tự có nghĩa: luật đầu tiên khớp thì dùng.
# compose: giữ nét gốc, ghép chữ Việt từ glyph của chính font đó. Mặc định cho font Latin.
# replace-regular / replace-bold: thay cả atlas bằng Be Vietnam Pro. Chỉ dùng khi font
#   gốc thiếu chữ để ghép. Bản đầu (#8) thay TTake bằng Be Vietnam Pro và mất nét
#   Patapon của lời thoại, nên đã đổi sang compose (#9).
# keep: không vá.
RULES: list[tuple[str, str, str]] = [
    (r"_ja\b|_ja_|_kr\b|_kr_|NotoSansKR|GothicA1|PoorStory|DFPGB|DFT_R5|DF-KakuPop-W5_kr", "keep", "font Nhật, Hàn, Trung"),
    (r"_staffroll", "keep", "chữ chạy cuối game không dịch"),
    (r"^LiberationSans", "keep", "font mặc định của TMP, chỉ là dự phòng"),
    (r"^TTakeStd", "compose", "font kiểu Patapon của lời thoại, ghép dấu từ glyph gốc"),
    (r"^TShinGoPr6", "compose", "font chữ thường của game, ghép dấu từ glyph gốc"),
    (r"^DF-KakuPop|^LondrinaSolid", "compose", "font kiểu Patapon, ghép dấu từ glyph gốc"),
]


def action_for(name: str, latin: bool) -> tuple[str, str]:
    if name.endswith("_savewindow"):
        # Chỉ có 18 chữ hoa Latin. Ghép dấu, mượn chữ gốc và dấu của TShinGo cùng họ.
        return "compose", "chữ hoa của khung lưu game, mượn chữ gốc của TShinGo"
    if not latin:
        return "keep", "không có chữ Latin"
    for pattern, action, why in RULES:
        if re.search(pattern, name):
            return action, why
    return "keep", "chưa có luật, xem lại khi chữ Việt hiện sai"


def vi_chars() -> set[str]:
    """Chữ mà bản dịch đưa vào game và câu tiếng Anh không có.

    Chữ có sẵn trong câu tiếng Anh mà font thiếu thì game gốc đã vẽ qua font
    fallback từ trước. Chỉ chữ mới (chữ Việt, «») mới bắt buộc phải có trong font.
    """
    shipped: set[str] = set()
    for text in translations().values():
        shipped.update(text)
    source: set[str] = set()
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            source.update(row.get("source") or "")
    return {ch for ch in shipped - source if ch >= " "}


def catalog_sha1() -> str:
    return hashlib.sha1(ex.CATALOG.read_bytes()).hexdigest()


# Đọc font ---------------------------------------------------------------


def _field_names(obj) -> set[str]:
    node = obj.serialized_type.node if obj.serialized_type else None
    if node is None:
        return set()
    return {child.m_Name for child in node.m_Children}


def _kind(obj, cache: dict) -> str | None:
    """`font`, `text` hoặc None. Nhận diện theo tên trường, cache theo kiểu."""
    key = id(obj.serialized_type)
    if key in cache:
        return cache[key]
    names = _field_names(obj)
    if names:
        kind = "font" if {"m_CharacterTable", "m_AtlasTextures"} <= names else "text" if "m_fontAsset" in names else None
    else:
        # File của bản build không kèm typetree. Hỏi tên class qua MonoScript.
        try:
            script = obj.parse_monobehaviour_head().m_Script.deref_parse_as_object()
            name = script.m_ClassName
        except Exception:
            name = ""
        kind = "font" if name == "TMP_FontAsset" else "text" if name in {"TextMeshPro", "TextMeshProUGUI"} else None
    cache[id(obj.serialized_type)] = kind
    return kind


def _ref(assets_file, pointer: dict) -> str | None:
    file_id = int(pointer.get("m_FileID") or 0)
    path_id = int(pointer.get("m_PathID") or 0)
    if path_id == 0:
        return None
    if file_id == 0:
        owner = assets_file.name
    else:
        owner = assets_file.externals[file_id - 1].path
    return f"{Path(owner.replace('archive:/', '')).name}:{path_id}"


def scan_env(env, label: dict, owner_names: set[str], fonts: dict, usage: dict, chars_vi: set[str]) -> None:
    cache: dict = {}
    languages = {match.group(1).upper() for path in env.container for match in [LANGUAGE.search(path)] if match}
    language = languages.pop() if len(languages) == 1 else "common"
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour" or obj.assets_file.name not in owner_names:
            continue
        kind = _kind(obj, cache)
        if kind is None:
            continue
        try:
            tree = obj.read_typetree()
        except Exception:
            continue
        if kind == "text":
            font = _ref(obj.assets_file, tree.get("m_fontAsset") or {})
            if font:
                usage.setdefault(font, {}).setdefault(language, 0)
                usage[font][language] += 1
            continue
        key = f"{obj.assets_file.name}:{obj.path_id}"
        codes = {chr(item["m_Unicode"]) for item in tree.get("m_CharacterTable") or []}
        letters = "".join(sorted(ch for ch in codes if ch.isascii() and ch.isalpha()))
        latin = len(letters) >= 26
        name = str(tree.get("m_Name") or "")
        action, why = action_for(name, latin)
        atlas = (tree.get("m_AtlasTextures") or [{}])[0]
        missing = "".join(sorted(chars_vi - codes))
        fonts[key] = {
            "name": name,
            **label,
            "serialized": obj.assets_file.name,
            "pathId": obj.path_id,
            "chars": len(codes),
            "latin": latin,
            "asciiLetters": letters,
            "atlas": {
                "texture": _ref(obj.assets_file, atlas),
                "width": tree.get("m_AtlasWidth"),
                "height": tree.get("m_AtlasHeight"),
                "padding": tree.get("m_AtlasPadding"),
            },
            "fallbacks": [ref for ref in (_ref(obj.assets_file, item) for item in tree.get("m_FallbackFontAssetTable") or []) if ref],
            "missingVi": len(missing),
            "missingSample": missing[:60],
            "action": action,
            "why": why,
        }


def data_files(install: Path) -> list[str]:
    data = install / DATA_NAME
    names = []
    for path in sorted(data.iterdir()):
        if path.name.startswith(("sharedassets", "level", "resources")) and path.suffix in ("", ".assets"):
            names.append(path.name)
    return names


def scan(install: Path, chars_vi: set[str]) -> dict:
    data = install / DATA_NAME
    gen = TypeTreeGenerator(UNITY, "AssetStudio")
    gen.load_local_game(str(install))
    fonts: dict = {}
    usage: dict = {}
    for name in data_files(install):
        env = UnityPy.Environment()
        env.typetree_generator = gen
        for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
            env.load_file(str(data / extra))
        env.load_file(str(original(Path(DATA_NAME) / name)), name=name)
        scan_env(env, {"file": name}, {name}, fonts, usage, chars_vi)
        print(f"{name}: {sum(1 for item in fonts.values() if item.get('file') == name)} font")
        del env
        gc.collect()
    hashes = ex.load_hashes()
    for path in sorted(ex.BUNDLES.glob("*.bundle")):
        env = ex.open_bundle(ex.original_bundle(path.name), hashes)
        owners = {item.name for item in env.files.values()}
        owners |= {obj.assets_file.name for obj in env.objects}
        before = len(fonts)
        container = sorted(env.container)
        scan_env(env, {"bundle": path.name}, owners, fonts, usage, chars_vi)
        if len(fonts) > before:
            print(f"{path.name}: {len(fonts) - before} font")
        for key, item in fonts.items():
            if item.get("bundle") == path.name and "assetPath" not in item:
                item["assetPath"] = next((c for c in container if c.endswith(f"/{item['name']}.asset")), None)
        del env
        gc.collect()
    by_ref = {f"{Path(item['serialized']).name}:{item['pathId']}": key for key, item in fonts.items()}
    for key, item in fonts.items():
        item["fallbacks"] = [fonts[by_ref[ref]]["name"] if ref in by_ref else ref for ref in item["fallbacks"]]
        item["usedBy"] = usage.get(f"{Path(item['serialized']).name}:{item['pathId']}", {})
    return fonts


def write(fonts: dict) -> None:
    rows = sorted(fonts.values(), key=lambda item: (item["action"], item.get("file") or item.get("bundle"), item["name"]))
    payload = {
        "game": GAME_DIR.name,
        "unity": UNITY,
        "catalogSha1": catalog_sha1(),
        "scanned": date.today().isoformat(),
        "note": "Sinh bởi tools/font/inventory.py. Không sửa tay.",
        "fonts": rows,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Ghi {OUT} ({len(rows)} font)")


def load() -> dict:
    """Đọc fonts.json. Báo rõ khi game đã đổi bản so với lần quét."""
    if not OUT.is_file():
        raise SystemExit(f"Chưa có {OUT.name}. Chạy inventory.py trước.")
    payload = json.loads(OUT.read_text(encoding="utf-8"))
    current = catalog_sha1()
    if payload.get("catalogSha1") != current:
        raise SystemExit("catalog.json khác lần quét trước. Game đã cập nhật: chạy lại inventory.py.")
    return payload


def check(chars_vi: set[str]) -> int:
    """Đọc file đã vá trong patch/ và báo font cần vá còn thiếu chữ."""
    install = require_install()
    payload = load()
    targets = [item for item in payload["fonts"] if item["action"] != "keep"]
    gen = TypeTreeGenerator(UNITY, "AssetStudio")
    gen.load_local_game(str(install))
    hashes = ex.load_hashes()
    data = install / DATA_NAME
    bad = 0
    groups: dict[str, list[dict]] = {}
    for item in targets:
        groups.setdefault(item.get("file") or item["bundle"], []).append(item)
    for where, items in sorted(groups.items()):
        if where.endswith(".bundle"):
            patched = PATCH / ex.BUNDLES.relative_to(install) / where
            if not patched.is_file():
                print(f"{where}: chưa vá ({len(items)} font)")
                bad += len(items)
                continue
            env = ex.open_bundle(patched, hashes)
        else:
            patched = PATCH / DATA_NAME / where
            if not patched.is_file():
                print(f"{where}: chưa vá ({len(items)} font)")
                bad += len(items)
                continue
            env = UnityPy.Environment()
            env.typetree_generator = gen
            for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
                env.load_file(str(data / extra))
            env.load_file(str(patched), name=where)
        objects = {(obj.assets_file.name, obj.path_id): obj for obj in env.objects}
        for item in items:
            obj = objects.get((item["serialized"], item["pathId"]))
            if obj is None:
                print(f"{where}: không thấy {item['name']}")
                bad += 1
                continue
            tree = obj.read_typetree()
            codes = {chr(row["m_Unicode"]) for row in tree.get("m_CharacterTable") or []}
            missing = "".join(sorted(chars_vi - codes))
            status = "đủ" if not missing else f"thiếu {len(missing)}: {missing[:40]}"
            print(f"{where}: {item['name']} ({item['action']}) {status}")
            bad += bool(missing)
        del env
        gc.collect()
    return 1 if bad else 0


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="kiểm tra bản vá trong patch/")
    args = parser.parse_args()
    chars_vi = vi_chars()
    if args.check:
        return check(chars_vi)
    fonts = scan(require_install(), chars_vi)
    write(fonts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
