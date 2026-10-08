"""Kiểm chính tả tiếng Việt trong cột `vi` của `locale/vi/strings.csv`.

Kiểm theo cấu trúc âm tiết, không dùng từ điển:

- Lỗi (mã thoát 1):
  - âm tiết có dấu tiếng Việt nhưng sai cấu trúc: âm đầu, vần, chỗ đặt dấu, quy tắc c/k, g/gh, ng/ngh,
    vần tắc (p, t, c, ch) đi với dấu khác sắc và nặng. Ví dụ «nghĩ» đúng, «ngĩ» sai, «hoạc» sai.
  - chữ không ở dạng Unicode NFC (font không vẽ được dấu rời);
  - hai dấu cách liền nhau, dấu cách trước `, . ! ? : ;`.
- Cảnh báo: từ viết thường, không dấu, không phải âm tiết tiếng Việt. Thường là tên riêng,
  từ mượn (banjo, tarot), hoặc tiếng Anh còn sót.

Không bắt được nhầm s/x, ch/tr, d/gi/r, l/n, hỏi/ngã: cả hai cách viết đều là âm tiết hợp lệ.

    python tools/check_vietnamese.py games/potion-permit
    python tools/check_vietnamese.py games/potion-permit --words   # in thêm danh sách từ lạ
"""

from __future__ import annotations

import collections
import csv
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"(\{[^{}]+\}|%[sdif]|</?[A-Za-z][^>]*>|<#[0-9A-Fa-f]{3,8}>|\\n)")

TONES = {"́": "sắc", "̀": "huyền", "̉": "hỏi", "̃": "ngã", "̣": "nặng"}
ONSETS = sorted(
    "b c ch d đ g gh gi h k kh l m n ng ngh nh p ph qu r s t th tr v x".split(), key=len, reverse=True
)
RHYMES = set(
    """
    a ac ach ai am an ang anh ao ap at au ay
    ăc ăm ăn ăng ăp ăt
    âc âm ân âng âp ât âu ây
    e ec em en eng eo ep et
    ê êch êm ên ênh êp êt êu
    i ia ich im in inh ip it iu
    iêc iêm iên iêng iêp iêt iêu
    o oa oac oach oai oam oan oang oanh oao oap oat oay oc oe oen oeo oet oi om on ong ooc oong op ot
    oăc oăm oăn oăng oăt
    ô ôc ôi ôm ôn ông ôp ôt
    ơ ơi ơm ơn ơp ơt
    u ua uân uâng uât uây uc ui um un ung up ut uy uya uych uyên uyêt uyn uynh uyp uyt uyu uê uênh uơ
    uôc uôi uôm uôn uông uôt
    ư ưa ưc ưi ưm ưn ưng ưt ưu
    ươc ươi ươm ươn ương ươp ươt ươu
    y yêm yên yêt yêu
    """.split()
)
STOPS = ("p", "t", "c", "ch")
FRONT = ("i", "e", "ê", "y", "iê")


def split_tone(word: str) -> tuple[str, str]:
    """Tách dấu thanh. Trả (chữ không dấu thanh, tên dấu)."""
    tone = ""
    base = []
    for char in unicodedata.normalize("NFD", word):
        if char in TONES:
            tone = TONES[char]
        else:
            base.append(char)
    return unicodedata.normalize("NFC", "".join(base)), tone


def tone_position_ok(word: str, base: str, onset: str) -> bool:
    """Dấu thanh đặt trên đúng nguyên âm, kiểu truyền thống: hòa, khỏe, thủy, quý, loại, toán."""
    marked = None
    index = -1
    for char in unicodedata.normalize("NFD", word):
        if char in TONES:
            marked = index
        elif not unicodedata.combining(char):
            index += 1
    if marked is None:
        return True
    vowels = [i for i, char in enumerate(base) if char in "aăâeêioôơuưy" and i >= len(onset)]
    if not vowels:
        return False
    special = [i for i in vowels if base[i] in "ăâêôơư"]
    if special:
        # Nguyên âm có dấu phụ mang dấu thanh; «ươ» thì đặt trên ơ.
        expected = special[-1]
    elif vowels[-1] < len(base) - 1:
        # Có âm cuối: đặt trên nguyên âm cuối cùng («toán», «hoàng»).
        expected = vowels[-1]
    elif len(vowels) == 3:
        expected = vowels[1]
    else:
        expected = vowels[0]
    return marked == expected


def syllable_error(word: str) -> str | None:
    """Lý do âm tiết sai, hoặc None nếu đúng."""
    lower = word.lower()
    base, tone = split_tone(lower)
    onset = next((item for item in ONSETS if base.startswith(item)), "")
    rhyme = base[len(onset):]
    if re.search(r"(.)\1\1", base) or (re.search(r"(.)\1", base) and not re.fullmatch(r".*oo(c|ng)", base)) or (len(base) == 1 and base not in RHYMES) or base[:2] in ("gr", "br"):
        # Thán từ kéo dài («Hừmmm», «Méooo»), tiếng kêu («Grừ») hoặc chữ lắp bắp («Đ-Đi»).
        return None
    gi = onset == "gi"
    if gi and (rhyme == "" or rhyme[0] not in "aăâeêoôơuưy"):
        # «gì», «gìn»: g + i…
        onset, rhyme = "g", base[1:]
    elif gi and rhyme not in RHYMES and "i" + rhyme in RHYMES:
        # «giếng», «giết»: gi + iêng, iêt viết gọn.
        rhyme = "i" + rhyme
    elif onset == "qu" and rhyme not in RHYMES and "u" + rhyme in RHYMES:
        # «quýnh», «quyết»: qu + uynh, uyêt viết gọn.
        rhyme = "u" + rhyme
    if onset == "qu" and rhyme == "":
        return "thiếu vần"
    if rhyme not in RHYMES:
        if onset == "" and base in RHYMES:
            rhyme = base
        else:
            return f"vần «{rhyme}» không có trong tiếng Việt"
    if onset in ("c", "g", "ng") and rhyme.startswith(FRONT) and not gi:
        return f"«{onset}» trước «{rhyme[0]}» phải viết «{ {'c': 'k', 'g': 'gh', 'ng': 'ngh'}[onset] }»"
    if onset in ("k", "gh", "ngh") and not rhyme.startswith(FRONT):
        return f"«{onset}» chỉ đứng trước i, e, ê, y"
    if rhyme.endswith(STOPS) and tone not in ("sắc", "nặng"):
        return f"vần tắc «{rhyme}» chỉ đi với dấu sắc hoặc nặng"
    if not tone_position_ok(lower, base, onset):
        return "dấu thanh đặt sai chữ"
    return None


SPACE_BEFORE = re.compile(r" [,.!?:;](?!\.)")
VIETNAMESE = set("àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ")


def words(text: str) -> list[str]:
    return re.findall(r"[^\W\d_]+", TOKEN.sub(" ", text))


def check(game_dir: Path, show_words: bool) -> int:
    csv_path = game_dir / "locale" / "vi" / "strings.csv"
    errors: list[str] = []
    foreign: collections.Counter = collections.Counter()
    examples: dict[str, str] = {}
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key, vi = row["id"], row.get("vi") or ""
            if not vi.strip() or key.startswith("EXAMPLE"):
                continue
            if vi == (row.get("source") or "") or (row.get("note") or "").strip() == "giữ nguyên":
                # Câu cố ý giữ nguyên bản gốc (tên riêng, tiếng nước khác).
                continue
            if unicodedata.normalize("NFC", vi) != vi:
                errors.append(f"{key}: không ở dạng NFC")
            plain = TOKEN.sub("X", vi)
            source = TOKEN.sub("X", row.get("source") or "")
            # Chỉ báo khi câu Việt nhiều hơn câu gốc: bản gốc đôi khi cố ý để dấu cách.
            if plain.count("  ") > source.count("  "):
                errors.append(f"{key}: hai dấu cách liền nhau")
            if len(SPACE_BEFORE.findall(plain)) > len(SPACE_BEFORE.findall(source)):
                errors.append(f"{key}: dấu cách trước dấu câu")
            for word in words(vi):
                lower = word.lower()
                if any(char in VIETNAMESE for char in lower):
                    reason = syllable_error(word)
                    if reason:
                        errors.append(f"{key}: «{word}» {reason}")
                elif word == lower and syllable_error(word):
                    foreign[lower] += 1
                    examples.setdefault(lower, key)
    label = game_dir.name
    for message in errors:
        print(f"{label}: lỗi: {message}")
    print(f"{label}: {len(errors)} lỗi, {len(foreign)} từ lạ viết thường (không dấu).")
    if show_words:
        for word, count in foreign.most_common():
            print(f"  {word} ×{count} (ví dụ {examples[word]})")
    return 1 if errors else 0


def main() -> int:
    sys.stdout = io_wrapper()
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    show = "--words" in sys.argv
    dirs = [ROOT / arg if not Path(arg).is_absolute() else Path(arg) for arg in args] or sorted(
        path.parents[2] for path in (ROOT / "games").glob("*/locale/vi/strings.csv")
    )
    return max((check(path, show) for path in dirs), default=0)


def io_wrapper():
    import io

    return io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
