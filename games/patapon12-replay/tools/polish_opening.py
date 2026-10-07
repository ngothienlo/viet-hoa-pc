"""Viết lại lời mở đầu và nhãn menu. Giữ mã &S0# và dấu /."""

from __future__ import annotations

import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[1] / "locale" / "vi" / "strings.csv"

# Khóa là câu gốc, đúng từng ký tự.
HAND = {
    "&S0#Once upon a time,": "&S0#Ngày xửa ngày xưa,",
    "&S0#the Patapon Ancients,/by the power of the Mighty One's drum,": "&S0#tổ tiên Patapon,/nhờ sức trống của Người Chỉ Huy,",
    "&S0#gained Wisdom, Courage,/Strength and Secret Juju.": "&S0#đạt được Trí tuệ, Dũng khí,/Sức mạnh và Juju bí mật.",
    "&S0#The Patapon Ancients,/guided by Great Mighty Patapon,": "&S0#tổ tiên Patapon,/được Người Chỉ Huy dẫn đường,",
    "&S0#ventured to Earthend,/in search of IT.": "&S0#tiến tới Earthend,/đi tìm IT.",
    "&S0#For the all powerful Patapons,/no foe was too mighty,": "&S0#Patapon toàn năng ấy,/không kẻ thù nào quá mạnh,",
    "&S0#no treasure out of reach,/and no land unconquerable.": "&S0#không báu vật nào ngoài tầm,/không vùng đất nào không chinh phục.",
    "&S0#The Ancients fought bravely/in the name of the Great Mighty Patapon,": "&S0#tổ tiên chiến đấu dũng cảm/nhân danh Người Chỉ Huy,",
    "&S0#and spawned a legend/which lasted generations.": "&S0#và dựng nên huyền thoại/truyền qua nhiều thế hệ.",
    "&S0#But today, the Patapons are/far from their former glory...": "&S0#Nhưng hôm nay, Patapon/đã xa hào quang xưa...",
    'The "Legend of the Patapons" is a mysterious/ancient book that is now yours. Lead them, oh/Mighty Ruler and be the Patapon Supreme! Guide them through an endless rhythmic adventure!': "«Huyền thoại Patapon» là cuốn cổ/bí ẩn, nay thuộc về ngươi. Hãy dẫn dắt họ,/hỡi Người Chỉ Huy, thành đấng tối cao của Patapon! Dẫn họ vào hành trình nhịp trống bất tận!",
    "New game": "Chơi mới",
    "Continue": "Tiếp tục",
    "&S0O2#As their ship neared completion, /Hatapon suddenly remembered an old story.": "&S0O2#Khi thuyền sắp hoàn thành, /Hatapon chợt nhớ một chuyện xưa.",
    "&S0O2#O Mighty Leader, let's sail off into the dark unknown/as our search for Earthend continues. Please come/back to us soon.": "&S0O2#Hỡi Người Chỉ Huy, hãy ra khơi vào miền tối/cuộc tìm Earthend vẫn tiếp. Xin hãy/sớm trở lại với chúng tôi.",
    "&S0O2#The Patapons bravely set off on their voyage, leaving behind/their loved ones, friends and the safety of their home island.": "&S0O2#Patapon dũng cảm ra khơi, để lại/người thân, bạn hữu và đảo quê an toàn.",
    "&S0O2#They braved many violent storms and sweated through/many scorching days. It was indeed a long and arduous/voyage... but the brave Patapons refused to give up.": "&S0O2#Họ vượt nhiều bão dữ và chịu/nhiều ngày nắng lửa. Chuyến đi dài, gian khổ.../nhưng Patapon không chịu bỏ cuộc.",
    "&S0O2#However, all their suffering was insignificant/compared to the troubles that awaited them...": "&S0O2#Nhưng mọi khổ ải ấy chẳng là gì/so với tai họa đang chờ...",
    "&S0O2#Only after forty-nine days and forty-nine nights did the/Patapons truly learn of the evils that lurked inside the ocean/blue... a mighty beast of the likes they've never seen before!": "&S0O2#Mãi bốn mươi chín ngày đêm, họ mới/thấy điều ác ẩn trong biển/xanh... một quái thú họ chưa từng gặp!",
    "&S0O2#Their fate unknown... what will become of the Patapons now...": "&S0O2#Số phận chưa rõ... Patapon rồi sẽ ra sao...",
    "OPTIONS": "TÙY CHỌN",
    "Language": "Ngôn ngữ",
    "©2008　Sony Computer Entertainment Inc. ©2008　Rolito/InterLink": "©2008　Sony Computer Entertainment Inc. ©2008　Rolito/InterLink",
    "Patapon Oath//I hereby pledge to honor and keep my/promise to be the Great Leader of the/Patapons and help them reach Earthend.//I will not stray from my goal, even in face/of death or great peril. Even at moments/of weakness, I will keep the beat and feel/the rhythm of the earth.  //From this point forward, I promise to /keep my pledge and take this drum/of courage and be the Mighty Leader/I was meant to be...//This is my oath.": "Lời thề Patapon//Ta nguyện giữ trọn/lời làm Người Chỉ Huy của/Patapon và đưa họ tới Earthend.//Ta không lìa mục tiêu, dù trước/cái chết hay hiểm nguy. Ngay lúc/yếu lòng, ta vẫn giữ nhịp và cảm/nhịp của đất.  //Từ đây về sau, ta nguyện /giữ lời thề, cầm lấy trống/dũng khí, và thành Người Chỉ Huy/mà ta phải trở thành...//Đây là lời thề của ta.",
    'You find a new book in your possession./"Patapon ~ Across the Sea"/Now, hit the mysterious drum/to begin the endless parade!': "Ngươi có một cuốn sách mới./«Patapon ~ Bên kia biển»/Giờ hãy đánh trống bí ẩn/để bắt đầu cuộc diễu hành bất tận!",
    "PATAPON　WORLD MAP": "BẢN ĐỒ THẾ GIỚI",
    "HEADQUARTERS": "BẢN DOANH",
    "EVOLUTION MAP": "BẢN ĐỒ TIẾN HÓA",
    "MISSION COMPLETE": "HOÀN THÀNH",
    "MISSION FAILED": "THẤT BẠI",
    "OPTION": "TÙY CHỌN",
    "SOUND SETTING": "ÂM THANH",
    "HEADPHONE": "TAI NGHE",
    "SPEAKER": "LOA",
    "LEVEL SETTING": "ĐỘ KHÓ",
    "EASY": "DỄ",
    "NORMAL": "THƯỜNG",
    "HARD": "KHÓ",
    "PRESS ANY KEY": "NHẤN PHÍM BẤT KỲ",
    "NOW LOADING": "ĐANG TẢI",
    "Language： English": "Ngôn ngữ: English",
    "SELECT LANGUAGE": "CHỌN NGÔN NGỮ",
    'Zigoton prophecy has decreed:/"Once the Patapon\'s march,/the Earth shall be/engulfed in disaster."': "Lời tiên tri Zigoton:/«Khi Patapon tiến bước,/đất sẽ chìm/trong tai họa.»",
}


def main() -> None:
    for source, vi in HAND.items():
        if source.count("/") != vi.count("/"):
            raise SystemExit(f"Lệch dấu /: {source[:60]}")
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    changed = 0
    restored = 0
    for row in rows:
        vi = HAND.get(row["source"])
        if vi is not None:
            row["vi"] = vi
            row["status"] = "review"
            row["note"] = "viết tay" if vi != row["source"] else "giữ nguyên"
            changed += 1
        elif "XZX" in (row.get("vi") or ""):
            row["vi"] = row["source"]
            row["status"] = "draft"
            row["note"] = "giữ nguyên"
            restored += 1
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, ["id", "context", "source", "vi", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"viết tay {changed} dòng, gỡ token hỏng {restored} dòng")


if __name__ == "__main__":
    main()
