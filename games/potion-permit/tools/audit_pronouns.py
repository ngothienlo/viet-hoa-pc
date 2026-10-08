"""Rà xưng hô trong thoại NPC của Potion Permit. In danh sách để người đọc lại, không sửa gì.

Hai việc:

1. Câu NPC nói riêng với nhân vật chính: báo từ lộ giới tính («anh», «chị», «cô»…)
   không phải cách NPC đó tự xưng, và báo «cậu» khi bảng ghi NPC gọi «cháu».
   Câu sự kiện chỉ tính là «nói riêng» khi cảnh không có NPC nào khác.
2. Danh xưng đứng trước tên NPC («chị Helene», «bác Leano»), gom theo người được gọi.
   Một người bị gọi bằng nhiều danh xưng thì in ra, kèm ai gọi, để soát giữa các lô.

Ai có mặt trong cảnh lấy từ bundle `so-event-data` của game, lưu tạm ở
`extract/scenes.json`. Bảng xưng hô đọc từ `docs/van-phong.md`.

    python games/potion-permit/tools/audit_pronouns.py [lo1.json ...] [--npc MYER,HELENE]

`lo1.json` là bản dịch chưa gộp (mảng `{"id", "vi"}`), đè lên cột `vi` của CSV khi rà.
"""

from __future__ import annotations

import argparse
import collections
import csv
import io
import json
import re
import sys
from pathlib import Path

import UnityPy

sys.path.insert(0, str(Path(__file__).resolve().parent))

from game_config import DATA_NAME, GAME_DIR, require_install  # noqa: E402

CSV_PATH = GAME_DIR / "locale" / "vi" / "strings.csv"
VAN_PHONG = GAME_DIR / "docs" / "van-phong.md"
SCENES = GAME_DIR / "extract" / "scenes.json"
BUNDLES = Path("StreamingAssets") / "aa" / "Windows" / "StandaloneWindows64"

GENDERED = ["anh", "chị", "cô", "chú", "ông", "bà", "chàng", "nàng"]
ADDRESS = GENDERED + ["cậu", "cháu", "con", "em", "nhóc", "cưng", "bác", "sếp", "ngài", "sơ", "mẹ", "bố"]
# Tiếng đi sau làm thành từ ghép, không phải xưng hô: «cô đơn», «chú ý», «ông nội», «anh ấy».
COMPOUND = {
    "anh": {"hùng", "dũng", "minh", "em", "trai", "đào", "tài", "ta", "ấy", "chàng"},
    "chị": {"em", "gái", "ta", "ấy"},
    "cô": {"đơn", "lập", "đặc", "dâu", "gái", "ta", "ấy", "nương"},
    "chú": {"ý", "thích", "tâm", "trọng", "rể", "chó", "mèo", "ta", "ấy", "cún"},
    "ông": {"trời", "bà", "ta", "ấy", "chủ", "lão", "nội", "ngoại", "tôi", "mình", "chú", "cháu"},
    "bà": {"con", "ta", "ấy", "nó", "lão", "nội", "ngoại", "tôi", "mình", "cháu"},
    "chàng": {"trai", "ta", "ấy"},
    "nàng": {"tiên", "ta", "ấy"},
    "cậu": {"ấy", "ta", "bé", "chàng", "nhóc", "con"},
}
WORD = re.compile(r"(?<!\w)(" + "|".join(sorted(ADDRESS, key=len, reverse=True)) + r")(?!\w)", re.IGNORECASE)
NAME_AFTER = re.compile(r"\s+(\{\[|[A-ZÀ-Ỹ][a-zà-ỹ]+)")
# Tiểu sử kể về NPC ở ngôi thứ ba, không nói với ai.
NARRATION = ("BG_STORY",)


def scenes() -> dict[str, dict]:
    """Tên cảnh -> NPC có mặt và lời thoại theo thứ tự (`[người nói, mã term]`)."""
    if SCENES.is_file():
        return json.loads(SCENES.read_text(encoding="utf-8"))
    folder = require_install() / DATA_NAME / BUNDLES
    bundle = next(folder.glob("so-event-data_*.bundle"), None)
    if bundle is None:
        raise SystemExit(f"Không thấy so-event-data_*.bundle trong {folder}")
    skip = {"", "NONE", "CAMERA", "RANDOM", "POSTBIRD"}
    found: dict[str, dict] = {}
    for obj in UnityPy.load(str(bundle)).objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        steps = tree.get("chemistEventSequence")
        if steps is None:
            continue
        actors = {actor["eventActorNPC"] for actor in tree.get("chemistEventActor", [])}
        actors |= {step.get("eventActor", "") for step in steps}
        lines = []
        for step in steps:
            dialog = step.get("eventDialog") or {}
            if step.get("eventType") == "DIALOG" and dialog.get("dialogContent"):
                lines.append([dialog.get("npcIDString") or step.get("eventActor", ""), dialog["dialogContent"]])
        found[tree["m_Name"]] = {"actors": sorted(actors - skip), "lines": lines}
    SCENES.parent.mkdir(parents=True, exist_ok=True)
    SCENES.write_text(json.dumps(found, ensure_ascii=False), encoding="utf-8")
    return found


def load_table() -> dict[str, dict[str, set[str]]]:
    """Bảng «Xưng hô của từng NPC với nhân vật chính»: NPC -> từ tự xưng, từ gọi."""
    def words(text: str) -> set[str]:
        return {word.strip().lower() for word in re.sub(r"\([^)]*\)", "", text).split(",") if word.strip()}

    table: dict[str, dict[str, set[str]]] = {}
    in_table = False
    for line in VAN_PHONG.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_table = line.startswith("## Xưng hô của từng NPC")
            continue
        if not in_table or not line.startswith("| ") or line.startswith(("| NPC", "| ---")):
            continue
        name, _role, self_word, call, *_ = [cell.strip() for cell in line.strip("|").split("|")]
        table[name.upper()] = {"self": words(self_word), "call": words(call)}
    return table


def address_words(text: str) -> list[str]:
    """Từ xưng hô trong câu, bỏ từ ghép và danh xưng đi trước tên («anh Forrest»)."""
    found = []
    for match in WORD.finditer(text):
        word = match.group(1).lower()
        rest = text[match.end():]
        following = re.match(r"\s+(\w+)", rest)
        if following and following.group(1).lower() in COMPOUND.get(word, set()):
            continue
        if word in GENDERED and NAME_AFTER.match(rest):
            continue
        found.append(word)
    return found


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("overlays", nargs="*", help="bản dịch chưa gộp, mảng {id, vi}")
    parser.add_argument("--npc", default="", help="chỉ rà các NPC này, cách nhau bằng dấu phẩy")
    args = parser.parse_args()
    only = {name.strip().upper() for name in args.npc.split(",") if name.strip()}

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        vi = {row["id"]: row["vi"] for row in csv.DictReader(handle) if row["vi"].strip()}
    for path in args.overlays:
        for item in json.loads(Path(path).read_text(encoding="utf-8")):
            vi[item["id"]] = item["vi"]

    table = load_table()
    present: dict[str, set[str]] = {}
    for scene in scenes().values():
        for speaker, term in scene["lines"]:
            present.setdefault(f"{speaker}/{term}", set(scene["actors"]) | {speaker})

    names = {name.capitalize(): name for name in table}
    titled = re.compile(
        r"(?<!\w)(" + "|".join(ADDRESS) + r")\s+(" + "|".join(names) + r")(?!\w)", re.IGNORECASE
    )
    flags: list[str] = []
    titles: dict[str, dict[str, list[str]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    unknown = 0
    for key, text in sorted(vi.items()):
        speaker, _, term = key.partition("/")
        if speaker not in table or (only and speaker not in only) or term.startswith(NARRATION):
            continue
        for match in titled.finditer(text):
            target = names[match.group(2).capitalize()]
            if target != speaker:
                titles[target][match.group(1).lower()].append(key)
        if "EVENTDIALOG" in term:
            if key not in present:
                unknown += 1
                continue
            if present[key] - {speaker, "KIPPS"}:
                continue
        info = table[speaker]
        for word in address_words(text):
            if word in info["self"]:
                continue
            if word in GENDERED:
                flags.append(f"{key}: «{word}» lộ giới? | {text}")
            elif word == "cậu" and "cháu" in info["call"] and "cậu" not in info["call"]:
                flags.append(f"{key}: «cậu» nhưng bảng ghi gọi «cháu» | {text}")

    print(f"# Câu nói riêng với nhân vật chính: {len(flags)} chỗ cần xem")
    for line in flags:
        print("-", line.replace("\n", " / "))
    print()
    print("# Danh xưng trước tên NPC (danh xưng, số lần, ai gọi)")
    for target in sorted(titles):
        by_title = titles[target]
        if len(by_title) < 2:
            continue
        parts = []
        for title, keys in sorted(by_title.items(), key=lambda item: -len(item[1])):
            speakers = collections.Counter(key.split("/")[0] for key in keys)
            parts.append(f"«{title}» {len(keys)} (" + ", ".join(f"{who} {n}" for who, n in speakers.most_common()) + ")")
        print(f"- {target}: " + "; ".join(parts))
    print()
    print(f"Câu sự kiện không tìm thấy cảnh (đọc tay): {unknown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
