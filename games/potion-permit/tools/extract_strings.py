"""Trích câu tiếng Anh của Potion Permit từ I2 Localization vào `locale/vi/strings.csv`.

Chữ nằm trong component `LanguageSource` (I2 Localization). Có hai bản: trong
`sharedassets0.assets` và trong scene `level1`. Bản `sharedassets0` đúng hơn (bản
`level1` lệch ở vài term), nên lấy làm nguồn. Khi vá, câu Việt được ghi vào cả hai.

`id` là tên term của I2 (ví dụ `MYER/DIALOG_01`), `context` là nhóm term (phần trước `/`).
Chạy lại khi game cập nhật: term có câu gốc không đổi thì giữ `vi`, `status`, `note` cũ.

    python games/potion-permit/tools/extract_strings.py
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator

sys.path.insert(0, str(Path(__file__).resolve().parent))

from game_config import DATA_NAME, GAME_DIR, UNITY, original, require_install  # noqa: E402

CSV_PATH = GAME_DIR / "locale" / "vi" / "strings.csv"
FIELDS = ["id", "context", "source", "vi", "status", "note"]
# File chứa LanguageSource. File đầu là nguồn của CSV.
SOURCES = ("sharedassets0.assets", "level1")
ENGLISH = "en-US"


def generator(install: Path) -> TypeTreeGenerator:
    gen = TypeTreeGenerator(UNITY, "AssetStudio")
    gen.load_local_game(str(install))
    return gen


def open_file(filename: str, install: Path, gen: TypeTreeGenerator):
    """Nạp file gốc (bỏ qua bản đã vá), kèm globalgamemanagers để đọc MonoScript."""
    data = install / DATA_NAME
    env = UnityPy.Environment()
    env.typetree_generator = gen
    for extra in ("globalgamemanagers.assets", "globalgamemanagers"):
        env.load_file(str(data / extra))
    env.load_file(str(original(Path(DATA_NAME) / filename)), name=filename)
    stream = data / f"{filename}.resS"
    if stream.is_file():
        env.load_file(str(stream), name=stream.name)
    return env


def language_sources(env, filename: str) -> list:
    """Mọi object `LanguageSource` có term trong file."""
    found = []
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour" or obj.assets_file.name != filename:
            continue
        try:
            script = obj.parse_monobehaviour_head().m_Script.deref_parse_as_object()
        except Exception:
            continue
        if script.m_ClassName == "LanguageSource":
            found.append(obj)
    if not found:
        raise SystemExit(f"Không thấy LanguageSource trong {filename}.")
    return found


def english_index(source: dict) -> int:
    codes = [language["Code"] for language in source["mLanguages"]]
    if ENGLISH not in codes:
        raise SystemExit(f"LanguageSource không có cột {ENGLISH}: {codes}")
    return codes.index(ENGLISH)


def read_terms(install: Path, gen: TypeTreeGenerator) -> list[tuple[str, str]]:
    filename = SOURCES[0]
    env = open_file(filename, install, gen)
    tree = language_sources(env, filename)[0].read_typetree()
    source = tree["mSource"]
    column = english_index(source)
    return [(term["Term"], term["Languages"][column]) for term in source["mTerms"]]


def load_existing() -> dict[str, dict[str, str]]:
    if not CSV_PATH.is_file():
        return {}
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        return {row["id"]: row for row in csv.DictReader(handle)}


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    install = require_install()
    terms = read_terms(install, generator(install))
    existing = load_existing()
    rows = []
    kept = 0
    for term, english in terms:
        # Term trống hoặc chỉ là số không hiện lên màn hình như câu chữ.
        if not english.strip() or english.strip().isdigit():
            continue
        context = term.split("/", 1)[0] if "/" in term else ""
        old = existing.get(term)
        if old and old["source"] == english:
            rows.append({**old, "context": context})
            kept += 1
            continue
        rows.append({"id": term, "context": context, "source": english, "vi": "", "status": "todo", "note": ""})
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Ghi {len(rows)} term vào {CSV_PATH.relative_to(GAME_DIR)} (giữ bản dịch cũ của {kept} term).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
