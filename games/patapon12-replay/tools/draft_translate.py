"""Điền cột vi cho mọi dòng trùng câu gốc.

Câu lệnh và nút nằm trong OVERRIDES. Câu còn lại dịch một lô bằng Argos
Anh → Việt, rồi sửa ngôi «ngươi». Status là draft. Câu tiếng Nhật trong
bảng EN để todo.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import argostranslate.translate

GAME = Path(__file__).resolve().parents[1]
CSV_PATH = GAME / "locale" / "vi" / "strings.csv"
CACHE = GAME / "extract" / "draft-memory.json"
TOKEN = re.compile(r"(\{[^{}]+\}|%[sdif]|</?[A-Za-z][^>]*>|\\n|&[A-Za-z0-9#]+)")
NAMES = (
    "Ban the Great",
    "Patapon",
    "Hatapon",
    "Yaripon",
    "Tatepon",
    "Yumipon",
    "Kibapon",
    "Dekapon",
    "Megapon",
    "Mahopon",
    "Robopon",
    "Toripon",
    "Zigoton",
    "Karmen",
    "Meden",
    "Fever",
    "Gong",
    "Earthend",
    "Patapolis",
)
DRUM = re.compile(r"\b(PATA|PON|DON|CHAKA|DODON|Pata|Pon|Don|Chaka)\b")
JP = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
YOU = re.compile(r"\b(you|your|you're|youre)\b", re.I)

OVERRIDES = {
    "(no translation needed)": "",
    "(not needed)": "",
    "(delete)": "",
    "Alright!/Charge power!": "Được!/Tích lực!",
    "Huh?/Are you joking?": "Hả?/Ngươi đùa đấy à?",
    "Yikes!": "Ối!",
    "Go!/Go!!/Go!!!": "Đi!/Đi!!/Đi!!!",
    "Charge!": "Xông lên!",
    "Prepare for/attack!": "Chuẩn bị/tấn công!",
    "All set to/attack!": "Sẵn sàng/tấn công!",
    "That's it!": "Đúng rồi!",
    "Crackin' that/CHAKA CHAKA!": "Dồn nhịp/CHAKA CHAKA!",
    "Now!/Attack!": "Giờ!/Tấn công!",
    "Strike hard!/Stick to the rhythm!": "Đánh mạnh!/Giữ nhịp!",
    "Attack! Show/no mercy!": "Tấn công!/Đừng nương tay!",
    "Run away,/run away!": "Chạy đi,/chạy đi!",
    "Danger!/Take cover!": "Nguy!/Nấp đi!",
    "Charge your chi!": "Tích khí!",
    "Put some oomph/in that charge!": "Dồn sức/vào đòn tích!",
    "Annihilate! Hyah!": "Tiêu diệt! Ha!",
    "Withdraw! Hyah!": "Rút lui! Ha!",
    "Listen/to the/beat!": "Nghe/nhịp/trống!",
    "Run away!": "Chạy đi!",
    "Pull out!": "Rút lui!",
    "Ciao!": "Ciao!",
    "Take turns": "Đổi lượt",
    "Hatapon song": "Bài của Hatapon",
    "Ban Tatepon": "Ban Tatepon",
    "Don Yumipon": "Don Yumipon",
    "□□□○/Forward march!": "□□□○/Tiến lên!",
    "○○□○/Attack!": "○○□○/Tấn công!",
    "Return fire!": "Phản kích!",
    "Take 'em on!": "Đánh chúng!",
    "Get them!": "Bắt chúng!",
    "Get back!": "Lùi lại!",
    "Abort! Abort!": "Hủy! Hủy!",
    "They're weak, destroy them!": "Chúng yếu, diệt chúng!",
    "Revenge!": "Báo thù!",
    "For victory!": "Vì chiến thắng!",
    "Retreat!": "Rút lui!",
    "We're out of/here!": "Chuồn/thôi!",
    "How'd they/spot us?!": "Sao chúng/thấy ta?!",
    "How'd they/know?!": "Sao chúng/biết?!",
    "Hah hah!/Fooled you!": "Ha ha!/Lừa ngươi rồi!",
    "Ambush!": "Phục kích!",
    "Have no/mercy!": "Đừng/nương tay!",
    "Spineless/Patapons!": "Patapon/nhát gan!",
    "Cowards!": "Quân hèn!",
    "Flat-footed/oafs!": "Lũ/chậm chạp!",
    "Come and/get us!": "Cứ đến/mà bắt!",
    "Can't/catch us!": "Đừng hòng/đuổi kịp!",
    "No guts,/no glory!": "Không gan,/không vinh!",
    "URK! I'm a goner...": "Ực! Ta xong rồi...",
    "Save me!": "Cứu ta!",
    "Peace out...": "Ta đi đây...",
    "Hrggph!": "Hự!",
    "PATA PON DON CHAKA/Great <N0> protects us!": "PATA PON DON CHAKA/Người Chỉ Huy <N0> phù hộ chúng tôi!",
    "Wahoo!/That's the way!": "Ô hô!/Đúng điệu!",
    "Hmm? What's that?!": "Hử? Cái gì thế?!",
    "Hah hah hah!": "Ha ha ha!",
    "Your timing/is off.": "Nhịp của ngươi/lệch rồi.",
    "Don't rush!": "Đừng vội!",
    "Did you forget/the pattern?": "Ngươi quên/khẩu lệnh à?",
    "Attack!/PON PON!": "Tấn công!/PON PON!",
    "Let's not rush!/Hear that beat!": "Đừng vội!/Nghe nhịp đó!",
    "Your timing/is a bit off.": "Nhịp của ngươi/hơi lệch.",
    "Take it slowly!": "Từ từ thôi!",
    "Oh, c'mon Patapon!/Keep your cool!": "Patapon nào!/Giữ bình tĩnh!",
    "Eep!/I wet myself!": "Úi!/Ta sợ mất mật!",
    "This is bad./May I go home?": "Tệ rồi./Cho ta về được không?",
    "Are you all/tired out?": "Mọi người/mệt cả rồi à?",
    "Stay focused/and beat that/drum!": "Tập trung/và đánh/trống!",
    "You have to drum/to the beat to /reach fever mode!": "Phải đánh trống/đúng nhịp /mới vào Fever!",
    "Taking a break?": "Nghỉ à?",
    "Stay calm!/Stay focused!/Calm! Focused!": "Bình tĩnh!/Tập trung!/Bình tĩnh! Tập trung!",
    "Oopsie-daisie!": "Ối chà!",
    "Eek! Oop!/Watch it!": "Á! Ố!/Coi chừng!",
    "Beat the skin/off it!": "Đánh rách/mặt trống!",
    "Amateur!": "Non tay!",
    "Keep drumming!": "Đánh tiếp!",
    "Keep the song/going on!": "Giữ bài/hát tiếp!",
    "C'mon now!/Onward march!": "Nào!/Tiến lên!",
    "One foot after/the other, hu-ha!": "Từng bước/một, hò-ha!",
    "Kaboom!/Not good!": "Đoàng!/Không ổn!",
    "Yikes!/Oh, gadzooks!": "Ối!/Trời ơi!",
    "Oh no! We're in/a tight spot!": "Hỏng! Ta đang/bí rồi!",
    "What happened/to the beat?": "Nhịp trống/đi đâu rồi?",
    "What?/Taking/a break?": "Gì?/Đang/nghỉ à?",
    "Feel the rhythm,/feel it,/feel it now!": "Cảm nhịp,/cảm đi,/cảm ngay!",
    "Dance!/Sing!/Forward ho!": "Múa!/Hát!/Tiến lên!",
    "Take no/prisoners!": "Không bắt/tù binh!",
    "Forward march!♪": "Tiến lên!♪",
    "Careful!": "Cẩn thận!",
    "Too slow!": "Chậm quá!",
    "Nothing in/sight!": "Chẳng thấy/gì!",
    "Have some guts,/Great <N0>!": "Can đảm lên,/Người Chỉ Huy <N0>!",
    "Alright!/Party on!": "Được!/Cứ thế!",
    "Patapons get/on the defense!": "Patapon/vào thế thủ!",
    "Piece o'/cake!": "Dễ như/trở bàn tay!",
    "OK!/One step at/a time!": "Được!/Từng bước/một!",
    "Bring it on!": "Cứ đến đi!",
    "Nobody's home!": "Chẳng có ai!",
    "On the defense!/This could be bad!": "Thế thủ!/Chuyện này nguy!",
    "Laying low.../Laying low...": "Nằm im.../Nằm im...",
    "Tighten the/defense!": "Siết chặt/thế thủ!",
    "Protect!♪": "Bảo vệ!♪",
    "Our time will/come!": "Đến lượt/ta thôi!",
    "Get 'em!": "Đánh chúng!",
    "Attack!/Attack!/Attaaaack!": "Tấn công!/Tấn công!/Tấnnn công!",
    "Uh, attack/what?": "Ờ, tấn công/cái gì?",
    "No target in/sight!": "Không thấy/đích!",
    "Nothing out/here, cap'n!": "Chẳng có gì,/thưa Người Chỉ Huy!",
    "Spank them/bottoms!♪": "Đánh/chúng!♪",
    "Attack!♪": "Tấn công!♪",
    "Thrash! Pierce!/Don't stop!": "Đập! Đâm!/Đừng dừng!",
    "Hyah!": "Ha!",
    "Duck and cover!": "Cúi xuống nấp!",
    "Yeah! Yeah!/Roll to safety!": "Được! Được!/Lăn vào chỗ an toàn!",
    "Watch out!": "Coi chừng!",
    "Everyone!/Run!": "Mọi người!/Chạy!",
    "Wh-wh-what?!": "C-c-cái gì?!",
    "Ahoy!": "Này!",
    "Doh!/Run away!": "Hự!/Chạy đi!",
    "Run!/Danger ahead!": "Chạy!/Phía trước nguy!",
    "Run away!/Faster!": "Chạy đi!/Nhanh lên!",
    "Phew!": "Phù!",
    "Run! Don't/fall behind!": "Chạy! Đừng/tụt lại!",
    "Run for yer/lives!": "Chạy lấy/mạng!",
    "Focus inward!♪": "Tập trung!♪",
    "Charge power!": "Tích lực!",
    "Alright!/Lay low!": "Được!/Nằm im!",
    "Focus power!/Max effect!": "Dồn lực!/Hết mức!",
    "Hmmgggg...?": "Hừm...?",
    "Feeling the/power!": "Cảm thấy/sức mạnh!",
    "Oop... Can't/hold it in...": "Ố... Không/nín nổi...",
    "I can feel it!/I can feel it!": "Ta cảm thấy!/Ta cảm thấy!",
    "Charge that/energy!": "Tích/năng lượng!",
    "Chi! Chi! The chi/in me!": "Khí! Khí! Khí/trong ta!",
    "Yes": "Có",
    "No": "Không",
    "No!": "Không!",
    "Help": "Trợ giúp",
    "Cancel": "Hủy",
    "Back": "Quay lại",
    "Continue": "Tiếp tục",
    "Understood": "Đã rõ",
    "Information": "Thông tin",
    "Save complete.": "Đã lưu.",
    "Load complete.": "Đã tải.",
    "Altar": "Bàn thờ",
    "Stage": "Màn",
    "Minutes": "Phút",
    "Seconds": "Giây",
    "Spoils": "Chiến lợi phẩm",
    "Clear time": "Thời gian vượt",
    "Casualties": "Thương vong",
    "Metres": "Mét",
    "None": "Không",
    "Default": "Mặc định",
    "Type": "Loại",
    "Number": "Số",
    "Status": "Trạng thái",
    "Items": "Vật phẩm",
    "Missions": "Nhiệm vụ",
    "Deploy": "Điều đi",
    "Remove": "Gỡ",
    "Optimize": "Tối ưu",
    "Scroll": "Cuộn",
    "Proceed": "Tiếp tục",
    "Return to title screen?": "Về màn hình tựa?",
    "Return to Patapolis?": "Về Patapolis?",
    "System Data": "Dữ liệu hệ thống",
    "Game data": "Dữ liệu game",
    "Unknown error": "Lỗi không rõ",
    "Language: English": "Ngôn ngữ: English",
    "Play time：": "Thời gian chơi：",
    "hours": "giờ",
    "New Patapon": "Patapon mới",
    "Save the adventure?": "Lưu cuộc phiêu lưu?",
    "Legendary Memory": "Ký ức huyền thoại",
    "タイミング/ズレてる/かもかも": "Nhịp/lệch rồi/chăng chăng",
    "リズム/よくよく/きくきく！": "Nhịp/nghe kỹ/nghe kỹ!",
    "なんじゃ？/へんちょこリン": "Cái gì?/Nhịp lệch rồi",
    "ポンなこった！": "Hỏng rồi!",
    "いけ/いけ/いけ～ッ！": "Đi/đi/đi nào!",
    "とつにゅ～ッ！": "Xông vào!",
    "こーげき/じゅんび！": "Chuẩn bị/tấn công!",
    "こーげき/じゅんび/よ～しッ！": "Chuẩn bị/tấn công/được!",
    "それそれ～ッ！": "Đó đó!",
    "チャカチャカ/しっかり！": "CHAKA CHAKA/chắc vào!",
    "よ～しッ！/せめろ！！": "Được!/Tấn công!!",
    "リズムに のって/こーげきだ！！": "Theo nhịp/mà tấn công!!",
    "いくぞッ！/ぽこすかポン！！": "Đi nào!/Đánh PON!!",
    "それ～ッ！": "Đó!",
    "にげろ～ッ！": "Chạy đi!",
    "きんきゅ～/かいひ～": "Khẩn cấp/né đi",
    "ここは しんぼう！！": "Chịu đựng đã!!",
    "よ～しッ/ちからを ためろ！": "Được/tích lực!",
    "きあいを こめろ！！": "Dồn khí!!",
    "ぐぐ～ッと こらえて♪": "Cố nín♪",
}


def keep_original(source: str) -> bool:
    words = re.findall(r"[A-Za-z']+", source)
    if not words:
        return False
    drums = {"pata", "pon", "don", "chaka", "dodon", "pa", "cha", "do"}
    names = {name.lower() for name in NAMES}
    return all(word.lower() in drums or word.lower() in names for word in words)


def shield(text: str) -> tuple[str, list[str]]:
    found: list[str] = []

    def take(match: re.Match[str]) -> str:
        found.append(match.group(0))
        return f"XZX{len(found) - 1}XZX"

    protected = TOKEN.sub(take, text)
    for name in NAMES:
        protected = re.sub(rf"\b{re.escape(name)}\b", lambda m, n=name: take_name(m, n, found), protected)
    protected = DRUM.sub(lambda m: take_name(m, m.group(0), found), protected)
    return protected, found


def take_name(match: re.Match[str], value: str, found: list[str]) -> str:
    found.append(value)
    return f"XZX{len(found) - 1}XZX"


def restore(text: str, found: list[str]) -> str:
    for index, value in enumerate(found):
        text = text.replace(f"XZX{index}XZX", value)
    return text


def machine(source: str) -> str:
    parts = source.split("/")
    out: list[str] = []
    for part in parts:
        if not re.search(r"[A-Za-z]", part):
            out.append(part)
            continue
        shielded, found = shield(part)
        translated = argostranslate.translate.translate(shielded, "en", "vi")
        translated = restore(translated, found)
        if YOU.search(source):
            translated = re.sub(r"\bBạn\b", "Ngươi", translated)
            translated = re.sub(r"\bbạn\b", "ngươi", translated)
            translated = re.sub(r"(^|/)Anh\b", r"\1Ngươi", translated)
            translated = re.sub(r"(^|/)anh\b", r"\1ngươi", translated)
        if re.search(r"\bSave\b", part) and not re.search(r"save me", part, re.I):
            translated = re.sub(r"\bCứu\b", "Lưu", translated)
            translated = re.sub(r"\bcứu\b", "lưu", translated)
        if "<N0>" in source and "Người Chỉ Huy" not in translated and "<N0>" in translated:
            if re.search(r"\b(Great|Lord)\b", part):
                translated = translated.replace("<N0>", "Người Chỉ Huy <N0>", 1)
        out.append(translated.strip())
    return "/".join(out)


def polish(source: str, vi: str) -> str:
    if not vi:
        return vi
    if re.search(r"Zigoton", source, re.I):
        vi = vi.replace("Tử Thần", "Zigoton").replace("Zigoons", "Zigoton").replace("Zigotons", "Zigoton")
    if "Patapon" in source:
        vi = vi.replace("Patapons", "Patapon")
    vi = vi.replace("Người Chỉ Huy <N0> vĩ đại", "Người Chỉ Huy <N0>")
    vi = vi.replace("O Người Chỉ Huy", "Người Chỉ Huy")
    if YOU.search(source):
        vi = re.sub(r"\b(Anh|Cậu)\b", "Ngươi", vi)
        vi = re.sub(r"\b(anh|cậu)\b", "ngươi", vi)
        vi = re.sub(r"\bBạn\b", "Ngươi", vi)
        vi = re.sub(r"\bbạn\b", "ngươi", vi)
    return vi


def decide(source: str, cache: dict[str, dict[str, str]]) -> dict[str, str]:
    if source in cache:
        return cache[source]
    if source in OVERRIDES:
        vi = OVERRIDES[source]
        row = {"vi": vi, "status": "draft" if vi else "todo", "note": "" if vi else "không dịch"}
    elif not source.strip():
        row = {"vi": "", "status": "todo", "note": ""}
    elif JP.search(source):
        row = {"vi": "", "status": "todo", "note": "nguồn tiếng Nhật"}
    elif keep_original(source):
        row = {"vi": source, "status": "draft", "note": "giữ nguyên"}
    else:
        vi = machine(source)
        if TOKEN.findall(source) != TOKEN.findall(vi):
            row = {"vi": "", "status": "todo", "note": "lệch placeholder"}
        else:
            row = {"vi": vi, "status": "draft", "note": "dịch máy"}
    cache[source] = row
    return row


def main() -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.is_file() else {}
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    sources = list(dict.fromkeys(row["source"] for row in rows))
    done = 0
    for source in sources:
        if source not in cache:
            decide(source, cache)
            done += 1
            if done % 100 == 0:
                CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
                print(f"đã dịch {done}", flush=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    for row in rows:
        filled = cache[row["source"]]
        row["vi"] = polish(row["source"], filled["vi"])
        row["status"] = filled["status"]
        row["note"] = filled["note"]
        if row["status"] == "draft" and row["vi"].strip() and row["vi"] == row["source"]:
            row["note"] = "giữ nguyên"
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, ["id", "context", "source", "vi", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)
    draft = sum(1 for row in rows if row["status"] == "draft")
    todo = sum(1 for row in rows if row["status"] == "todo")
    print(f"draft {draft} todo {todo}")


if __name__ == "__main__":
    sys.exit(main())
