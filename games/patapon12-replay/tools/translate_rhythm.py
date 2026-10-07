"""Dịch câu hướng dẫn nhịp còn để nguyên tiếng Anh. Giữ PATA PON và nút."""

from __future__ import annotations

import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[1] / "locale" / "vi" / "strings.csv"

# Khóa là câu gốc, đúng từng ký tự. Số dấu / phải khớp.
HAND = {
    "&H20O1R255G255B255#PON PON PON PON.../Beat the drum to the/rhythm. Press the ○/button for PON.": "&H20O1R255G255B255#PON PON PON PON.../Đánh trống theo/nhịp. Nhấn nút ○/để ra PON.",
    "&H20O1R255G255B255#Right, right! Like that!/PON PON PON PON.../Keep on drumming!": "&H20O1R255G255B255#Đúng, đúng! Như vậy!/PON PON PON PON.../Cứ đánh tiếp!",
    "&H20O1R255G255B255#PON PON PON PON…/Beat that drum!/Press the ○ button for PON.": "&H20O1R255G255B255#PON PON PON PON…/Đánh trống đi!/Nhấn nút ○ để ra PON.",
    "&H20O1R255G255B255#PATA PATA PATA PON/Press □□□○ in time/to the rhythm.♪": "&H20O1R255G255B255#PATA PATA PATA PON/Nhấn □□□○ đúng/nhịp.♪",
    "&H20O1R254G096B120#Quiet! Don't drum/while the Patapons/are singing!": "&H20O1R254G096B120#Im lặng! Đừng đánh trống/khi Patapon/đang hát!",
    "&H20O1R255G255B255#That's it!/□□□○/PATA PATA PATA PON/Onward march!♪/Onward march!♪": "&H20O1R255G255B255#Đúng rồi!/□□□○/PATA PATA PATA PON/Tiến lên!♪/Tiến lên!♪",
    "&H20O1R255G255B255#That's the idea!/□□□○/PATA PATA PATA PON/Strike that drum!♪": "&H20O1R255G255B255#Đúng ý đó!/□□□○/PATA PATA PATA PON/Đánh trống đi!♪",
    "&H20O1R255G255B255#Fantastic! Keep it up!/□□□○/PATA PATA PATA PON/March further still!♪": "&H20O1R255G255B255#Tuyệt! Cứ thế!/□□□○/PATA PATA PATA PON/Tiến thêm nữa!♪",
    "&H20O1R255G255B255#Perfect!/Keep up the good work./□□□○/PATA PATA PATA PON": "&H20O1R255G255B255#Hoàn hảo!/Cứ giữ nhịp này./□□□○/PATA PATA PATA PON",
    "&H20O1R254G096B120#Once the song is done,/□□□○/PATA PATA PATA PON/Join in with your drum!": "&H20O1R254G096B120#Khi bài hát dứt,/□□□○/PATA PATA PATA PON/Gõ trống hòa vào!",
    "&H20O1R254G096B120#Relax and feel the rhythm!/□□□○/PATA PATA PATA PON/Take turns keeping the beat!": "&H20O1R254G096B120#Thả lỏng, nghe nhịp!/□□□○/PATA PATA PATA PON/Luân phiên giữ nhịp!",
    "PATA PATA Song/PATA PATA PATA PON♪/All hail the Mighty Patapon!": "Bài PATA PATA/PATA PATA PATA PON♪/Sáng danh Người Chỉ Huy!",
    "Relax and feel the rhythm!/PATA PATA PATA PON/Take turns keeping the beat!": "Thả lỏng, nghe nhịp!/PATA PATA PATA PON/Luân phiên giữ nhịp!",
    "&H20O1R255G255B255#Battle song/○○□○/PON PON PATA PON♪": "&H20O1R255G255B255#Bài chiến/○○□○/PON PON PATA PON♪",
    "&H20O1R255G255B255#PON PON PATA PON/Press ○○□○ in time/to the rhythm.♪": "&H20O1R255G255B255#PON PON PATA PON/Nhấn ○○□○ đúng/nhịp.♪",
    "&H20O1R255G255B255#Right, right!/○○□○/PON PON PATA PON/Get 'em!♪ Get 'em!♪": "&H20O1R255G255B255#Đúng, đúng!/○○□○/PON PON PATA PON/Hạ chúng!♪ Hạ chúng!♪",
    "&H20O1R255G255B255#That's the idea!/○○□○/PON PON PATA PON/Strike that drum!♪": "&H20O1R255G255B255#Đúng ý đó!/○○□○/PON PON PATA PON/Đánh trống đi!♪",
    "&H20O1R255G255B255#Super! Keep going!/○○□○/PON PON PATA PON/Whoop them!♪": "&H20O1R255G255B255#Hay lắm! Cứ tiếp!/○○□○/PON PON PATA PON/Quất chúng!♪",
    "&H20O1R255G255B255#Perfect!/Keep up the good work./○○□○/PON PON PATA PON": "&H20O1R255G255B255#Hoàn hảo!/Cứ giữ nhịp này./○○□○/PON PON PATA PON",
    "&H20O1R254G096B120#Once the song is done,/○○□○/PON PON PATA PON/Join in with your drum!": "&H20O1R254G096B120#Khi bài hát dứt,/○○□○/PON PON PATA PON/Gõ trống hòa vào!",
    "There!/PON PON PATA PON/Launch an attack!♪": "Đó!/PON PON PATA PON/Tấn công!♪",
    "&H20O1R254G096B120#Relax and feel the rhythm!/○○□○/PON PON PATA PON/Take turns keeping the beat!": "&H20O1R254G096B120#Thả lỏng, nghe nhịp!/○○□○/PON PON PATA PON/Luân phiên giữ nhịp!",
    "The PON PON Song is/PON PON PATA PON/Don't give up, Almighty!": "Bài PON PON là/PON PON PATA PON/Đừng bỏ cuộc, Người Chỉ Huy!",
    "&H20O1R255G255B255#CHAKA CHAKA PATA PON/Press △△□○ in time/with the rhythm.♪": "&H20O1R255G255B255#CHAKA CHAKA PATA PON/Nhấn △△□○ đúng/nhịp.♪",
    "&H20O1R255G255B255#Right! That's the idea!/△△□○/CHAKA CHAKA PATA PON/Defend!♪": "&H20O1R255G255B255#Đúng! Đúng ý đó!/△△□○/CHAKA CHAKA PATA PON/Phòng thủ!♪",
    "&H20O1R255G255B255#Great! One more time!/△△□○/CHAKA CHAKA PATA PON/Strike that drum!♪": "&H20O1R255G255B255#Tốt! Thêm lần nữa!/△△□○/CHAKA CHAKA PATA PON/Đánh trống đi!♪",
    "&H20O1R255G255B255#Fantastic! Keep going!/CHAKA CHAKA PATA PON/Defend to the end!♪": "&H20O1R255G255B255#Tuyệt! Cứ tiếp!/CHAKA CHAKA PATA PON/Phòng đến cùng!♪",
    "&H20O1R240G050B000#Once the song is done,/△△□○/CHAKA CHAKA PATA PON/Join in with your drum!": "&H20O1R240G050B000#Khi bài hát dứt,/△△□○/CHAKA CHAKA PATA PON/Gõ trống hòa vào!",
    "&H20O1R240G050B000#Is that the right sound?/△△□○/CHAKA CHAKA PATA PON/Keep the order straight!": "&H20O1R240G050B000#Đúng tiếng đó chứ?/△△□○/CHAKA CHAKA PATA PON/Giữ đúng thứ tự!",
    "The CHAKA CHAKA Song is/CHAKA CHAKA PATA PON/Don't give up, O Mighty Patapon!": "Bài CHAKA CHAKA là/CHAKA CHAKA PATA PON/Đừng bỏ cuộc, hỡi Người Chỉ Huy!",
    "&H20O1R254G096B120#Once the song is done,/○□○□/PON PATA PON PATA/Join in with your drum!": "&H20O1R254G096B120#Khi bài hát dứt,/○□○□/PON PATA PON PATA/Gõ trống hòa vào!",
    "&H20O1R255G255B255#PON PATA PON PATA/Press ○□○□ in time/to the rhythm.♪": "&H20O1R255G255B255#PON PATA PON PATA/Nhấn ○□○□ đúng/nhịp.♪",
    "&H20O1R255G255B255#Yes! That's it!/○□○□/PON PATA PON PATA/Run like the dickens!♪": "&H20O1R255G255B255#Phải! Đúng rồi!/○□○□/PON PATA PON PATA/Chạy thục mạng!♪",
    "&H20O1R255G255B255#Great! One more time!/PON PATA PON PATA/Strike that drum!♪": "&H20O1R255G255B255#Tốt! Thêm lần nữa!/PON PATA PON PATA/Đánh trống đi!♪",
    "&H20O1R255G255B255#Fantastic! Keep going!/PON PATA PON PATA/Run like you're on fire!♪": "&H20O1R255G255B255#Tuyệt! Cứ tiếp!/PON PATA PON PATA/Chạy như lửa đốt!♪",
    "&H20O1R240G050B000#Once the song is done,/○□○□/PON PATA PON PATA/Join in with your drum!": "&H20O1R240G050B000#Khi bài hát dứt,/○□○□/PON PATA PON PATA/Gõ trống hòa vào!",
    "&H20O1R240G050B000#Relax and feel the rhythm!/○□○□/PON PATA PON PATA/Take turns keeping the beat!♪": "&H20O1R240G050B000#Thả lỏng, nghe nhịp!/○□○□/PON PATA PON PATA/Luân phiên giữ nhịp!♪",
    "&H20O1R254G096B120#Once the song is done,/○○△△/PON PON CHAKA CHAKA/Join in with your drum!": "&H20O1R254G096B120#Khi bài hát dứt,/○○△△/PON PON CHAKA CHAKA/Gõ trống hòa vào!",
    "&H20O1R255G255B255#PON PON CHAKA CHAKA/Press ○○△△ in time/to the rhythm.♪": "&H20O1R255G255B255#PON PON CHAKA CHAKA/Nhấn ○○△△ đúng/nhịp.♪",
    "&H20O1R255G255B255#Yes! That's it!/○○△△/PON PON CHAKA CHAKA/Lay low and save up!♪": "&H20O1R255G255B255#Phải! Đúng rồi!/○○△△/PON PON CHAKA CHAKA/Nằm thấp, tích lực!♪",
    "&H20O1R255G255B255#Great! One more time!/PON PON CHAKA CHAKA/Strike that drum!♪": "&H20O1R255G255B255#Tốt! Thêm lần nữa!/PON PON CHAKA CHAKA/Đánh trống đi!♪",
    "&H20O1R255G255B255#Fantastic! Keep going!/PON PON CHAKA CHAKA/Charge that power!♪": "&H20O1R255G255B255#Tuyệt! Cứ tiếp!/PON PON CHAKA CHAKA/Tích sức đi!♪",
    "&H20O1R240G050B000#Once the song is done,/○○△△/PON PON CHAKA CHAKA/Join in with your drum!": "&H20O1R240G050B000#Khi bài hát dứt,/○○△△/PON PON CHAKA CHAKA/Gõ trống hòa vào!",
    "&H20O1R240G050B000#Relax and feel the rhythm!/○○△△/PON PON CHAKA CHAKA/Take turns keeping the beat!♪": "&H20O1R240G050B000#Thả lỏng, nghe nhịp!/○○△△/PON PON CHAKA CHAKA/Luân phiên giữ nhịp!♪",
    "- Gong the Hawkeye -/The Patapon-Zigoton conflict continues, and Gong/the Hawkeye has come to strike back after losing/the fort. Beware of Gong's hammer of fury!": "- Gong Mắt Ưng -/Xung đột Patapon và Zigoton còn tiếp, Gong/Mắt Ưng trở lại trả đũa sau khi mất/pháo đài. Coi chừng búa thịnh nộ của Gong!",
    "- Secret Juju at Lostdon -/Magical artifacts are hidden everywhere, each one/intensely guarded by brutal guardians! Show your/might, O Majestic One, Mighty Patapon creator.": "- Juju bí truyền ở Lostdon -/Bảo vật phép giấu khắp nơi, món nào cũng/có lính canh tàn bạo giữ! Hãy tỏ uy,/hỡi Người Chỉ Huy, đấng tạo nên Patapon.",
    "- Desert Crossing -/Ancient legend tells of a Patapon King that crossed the/desert invoking the Secret Rain JuJu; a power whose/secret is hidden deep in the Patata Plain.": "- Băng sa mạc -/Truyền thuyết kể vua Patapon đã băng/sa mạc nhờ Juju Mưa bí truyền; sức ấy/giấu sâu dưới Đồng bằng Patata.",
    "- Desert Crossing -/Ancient legend tells of a Patapon King that crossed the/desert invoking the Secret Rain Juju; now you must conjure/your powers and prove your might!": "- Băng sa mạc -/Truyền thuyết kể vua Patapon đã băng/sa mạc nhờ Juju Mưa bí truyền; giờ ngươi phải gọi/sức mình và chứng tỏ uy lực!",
    "To make it rain upon the desert,/you must acquire the DON Drum/and Rain Miracle.": "Muốn mưa trên sa mạc,/ngươi phải có Trống DON/và Miracle Mưa.",
    "O Mighty <N0>.../I felt a tragic/emptiness in/Gong's death...": "Hỡi Người Chỉ Huy <N0>.../Ta thấy khoảng trống/bi thảm khi/Gong gục ngã...",
    "No rotten little monster/stands a chance/against the Mighty Patapon!": "Không quái vật thối tha nào/có cửa thắng/Người Chỉ Huy!",
    "I'm the farmer, Fah Zakpon!/I can work the land alrighty, and/owe my life to the One Mighty Patapon!!": "Ta là nông phu Fah Zakpon!/Ta cày được đất đàng hoàng, và/nợ mạng Người Chỉ Huy!!",
    "I'm Chef Rah Gashapon! I/cook for the tribe, and for/you as well O Mighty Patapon!": "Ta là bếp Rah Gashapon! Ta/nấu cho cả bộ tộc, và cho/ngươi nữa, hỡi Người Chỉ Huy!",
    "\"Requiem of Retreat\"/PON PATA PON PATA/Good grief! That's one/big one!♪": "\"Khúc Rút Lui\"/PON PATA PON PATA/Ối trời! Con này/to thật!♪",
    "\"March of Mobility\"/PATA PATA PATA PON/Full speed ahead!♪": "\"Khúc Tiến Bước\"/PATA PATA PATA PON/Hết tốc lực!♪",
    "\"Aria of Attack\"/PON PON PATA PON/Ready, aim, fire!♪": "\"Khúc Tấn Công\"/PON PON PATA PON/Sẵn sàng, nhắm, bắn!♪",
    "\"Lament of Defense\"/CHAKA CHAKA PATA PON/Guard the hearth and home!": "\"Khúc Ai Phòng Thủ\"/CHAKA CHAKA PATA PON/Giữ nhà giữ cửa!",
    "\"Hold Tight Hoe-down\"/PON PON CHAKA CHAKA/Hold back, sit tight!": "\"Điệu Nén Chịu\"/PON PON CHAKA CHAKA/Nén lại, ngồi chắc!",
    "This unique, fearsome/spear made in Mighty /Patapon's honor has flame ability.": "Ngọn giáo độc, dữ dội/này, làm để tôn Người /Chỉ Huy, có sức lửa.",
    "This unique, fearsome/sword made in the Mighty /Patapon's honor has both /flames and critical strike /ability.": "Thanh kiếm độc, dữ dội/này, làm để tôn Người /Chỉ Huy, có cả /lửa và đòn /chí mạng.",
    "This powerful, unique bow /made in the Mighty Patapon's/mighty's honor has flame ability.": "Cây cung mạnh, độc /này, làm để tôn Người Chỉ Huy,/có sức lửa.",
    "This powerful, unique lance/made in the Mighty Patapon's/honor; has both flame and/pushback abilities.": "Ngọn thương mạnh, độc,/làm để tôn Người Chỉ Huy,/có cả lửa và/sức đẩy lùi.",
    "This powerful, unique axe/made in the Mighty Patapon's/honor; has both flame and/critical hit capabilities.": "Chiếc rìu mạnh, độc,/làm để tôn Người Chỉ Huy,/có cả lửa và/đòn chí mạng.",
    "This powerful, unique horn/made in the Mighty Patapon's/honor; has both flame and/critical hit capabilities.": "Chiếc kèn mạnh, độc,/làm để tôn Người Chỉ Huy,/có cả lửa và/đòn chí mạng.",
    "-Call and Response!-/Take turns keeping a 4-beat rhythm with/the Patapons.//Mighty Patapon: PATA PATA PATA PON/Patapons: PATA PATA PATA PON/Mighty Patapon: PATA PATA PATA PON/Patapons: PATA PATA PATA PON//Hit a rhythmical climax to send the/Patapons into fever mode!": "-Hát đáp!-/Luân phiên giữ nhịp bốn phách với/Patapon.//Người Chỉ Huy: PATA PATA PATA PON/Patapon: PATA PATA PATA PON/Người Chỉ Huy: PATA PATA PATA PON/Patapon: PATA PATA PATA PON//Đánh đúng cao trào để đưa/Patapon vào Fever!",
    "-Watch Their Eyes-/The Patapons get a different look in their/eyes when enemies are within attack range.//You'll tell by their eyes if the PON PON Song attack will reach the enemy.//The Patapon whose hit points are shown in the upper left of the screen will also get a different look in their eyes.": "-Hãy nhìn mắt họ-/Mắt Patapon đổi sắc khi/địch nằm trong tầm đánh.//Nhìn mắt là biết đòn bài PON PON có chạm địch không.//Patapon hiện máu ở góc trên bên trái màn hình cũng đổi ánh mắt.",
    "-Master of Defense, Tatepon-/Tatepons defend like no other!//Use the CHAKA CHAKA Song and the Tatepons/will put shields up, reducing the damage of/most attacks!//Defense allows you to lie back and wait/for the perfect moment to fight back.": "-Bậc thầy phòng thủ, Tatepon-/Tatepon phòng thủ không ai sánh!//Dùng bài CHAKA CHAKA, Tatepon/giương khiên, giảm sát thương của/hầu hết đòn đánh!//Phòng thủ để ngươi ngồi chờ/đúng lúc phản công.",
    "-Megapon, Fiend for Sound-/Megapons cream opponents by tooting/devastating triple sound missiles at their foes!//They inflict steady damage, and use a/variety of attacks with the PON CHAKA Song.//Pity these powerful allies were not/brought to the frontlines earlier!": "-Megapon, kẻ mê tiếng-/Megapon nghiền địch bằng cách thổi/ba mũi tên âm thanh hủy diệt!//Chúng gây sát thương đều, và dùng/nhiều đòn với bài PON CHAKA.//Tiếc là đồng minh mạnh này không/được đưa ra tuyến đầu sớm hơn!",
    "PATA PATA PATA PON!/Keep the rhythm/to carry the EGG!": "PATA PATA PATA PON!/Giữ nhịp/để khiêng TRỨNG!",
    "PATA PATA PATA PON!/Everyone keep the rhythm/to march onwards!": "PATA PATA PATA PON!/Mọi người giữ nhịp/để tiến bước!",
    "PON PON PATA PON!/Keep the rhythm/to launch your attack!": "PON PON PATA PON!/Giữ nhịp/để tung đòn!",
    "&H18O1R255G255B255#PON PON PON PON/Strike the drum four times./Press the ○ Button for PON.": "&H18O1R255G255B255#PON PON PON PON/Đánh trống bốn tiếng./Nhấn nút ○ để ra PON.",
    "&H18O1R255G255B255#Listen to the drum's rhythm.../PON PON PON PON/Now press the ○ Button./Keep the rhythm!": "&H18O1R255G255B255#Nghe nhịp trống.../PON PON PON PON/Giờ nhấn nút ○./Giữ nhịp!",
    "&H18O1R255G255B255#Listen to the beat!/PON PON PON PON/Now strike the drum!/Feel the rhythm!": "&H18O1R255G255B255#Nghe nhịp đi!/PON PON PON PON/Giờ đánh trống!/Cảm nhịp!",
    "&H18O1R255G255B255#Next: □, □, □, ○/PATA PATA PATA PON/Hit four drumbeats in/one measure.": "&H18O1R255G255B255#Tiếp: □, □, □, ○/PATA PATA PATA PON/Đánh bốn tiếng/trong một ô nhịp.",
    "&H18O1R255G255B255#Listen to the Earth's rhythm!/PATA PATA PATA PON/Hit that drum! Keep the beat!": "&H18O1R255G255B255#Nghe nhịp của đất!/PATA PATA PATA PON/Đánh trống! Giữ nhịp!",
    "&H22O1R255G255B255#PATA PATA PATA PON/If you match the four beats/properly, the Patapons will/start to move...": "&H22O1R255G255B255#PATA PATA PATA PON/Nếu ngươi khớp bốn phách/cho đúng, Patapon sẽ/bắt đầu bước...",
    "&H18O1R255G255B255#It's time for you to learn a third/song: The CHAKA CHAKA Song. /This is the Lament of Defense./Use it to get out of tough spots.": "&H18O1R255G255B255#Đến lúc học bài thứ ba,/bài CHAKA CHAKA. /Đây là Khúc Ai Phòng Thủ./Dùng khi sa vào thế bí.",
    "&H18O1R255G255B255#CHAKA CHAKA PATA PON/Match the rhythm!/△, △, □, ○": "&H18O1R255G255B255#CHAKA CHAKA PATA PON/Khớp nhịp!/△, △, □, ○",
    "&H18O1R255G255B255#That's it! You got it!/△, △, □, ○/CHAKA CHAKA PATA PON/Shields up! Defend!♪": "&H18O1R255G255B255#Đúng rồi! Ngươi làm được!/△, △, □, ○/CHAKA CHAKA PATA PON/Giương khiên! Phòng thủ!♪",
    "&H18O1R255G255B255#Woo-hoo! Do it again!/△, △, □, ○/CHAKA CHAKA PATA PON/Bang that drum!♪": "&H18O1R255G255B255#Hoan hô! Làm lại đi!/△, △, □, ○/CHAKA CHAKA PATA PON/Đánh trống đi!♪",
    "&H18O1R255G255B255#Sweet! Keep it going!/CHAKA CHAKA PATA PON/We'll make it through!♪": "&H18O1R255G255B255#Ngọt! Cứ tiếp!/CHAKA CHAKA PATA PON/Chúng ta sẽ qua!♪",
    "&H20O1R255G255B255#Let's move forward! Don't/forget to use the Lament of/Defense whenever we get/in trouble.": "&H20O1R255G255B255#Tiến lên! Đừng/quên Khúc Ai/Phòng Thủ mỗi khi sa/vào thế bí.",
    "&H18O1R240G050B000#Once the Patapons finish singing,/△, △, □, ○/CHAKA CHAKA PATA PON/It's your turn to hit the drum!": "&H18O1R240G050B000#Khi Patapon hát xong,/△, △, □, ○/CHAKA CHAKA PATA PON/Đến lượt ngươi đánh trống!",
    "&H18O1R240G050B000#Oh no! Did you make a mistake?/△, △, □, ○/CHAKA CHAKA PATA PON/Keep the order and the rhythm!": "&H18O1R240G050B000#Ôi không! Ngươi gõ nhầm?/△, △, □, ○/CHAKA CHAKA PATA PON/Giữ thứ tự và nhịp!",
    "Stand strong!/Defend! CHAKA/CHAKA PATA PON!": "Đứng vững!/Phòng thủ! CHAKA/CHAKA PATA PON!",
    "&H14O0R000G000B000#~Gong's Trial~/Map: Gangoro Wasteland/BGM: Gyorocchi's Theme": "&H14O0R000G000B000#~Thử thách của Gong~/Bản đồ: Hoang mạc Gangoro/Nhạc: Chủ đề Gyorocchi",
    "Once you're in Fever, hit/×, ××, ××/DON DODON DODON/This is the Juju Rhythm.": "Khi đã vào Fever, đánh/×, ××, ××/DON DODON DODON/Đây là Nhịp Juju.",
    "You've got the Fever!/×, ××, ××/DON DODON DODON/Drum the Juju Rhythm.": "Ngươi đã vào Fever!/×, ××, ××/DON DODON DODON/Đánh Nhịp Juju.",
    "&H14O0R000G000B000#~Absolute Despair~/MAP: Karmen Gate Sokshi/BGM: Moudamepon's Theme": "&H14O0R000G000B000#~Tuyệt vọng tột cùng~/BẢN ĐỒ: Cổng Karmen Sokshi/Nhạc: Chủ đề Moudamepon",
    "&H14O0R000G000B000#~Challenge of Absolute Despair~/MAP: Karmen Gate Sokshi/BGM: Moudamepon's Theme": "&H14O0R000G000B000#~Thử thách tuyệt vọng~/BẢN ĐỒ: Cổng Karmen Sokshi/Nhạc: Chủ đề Moudamepon",
    "&H14O0R000G000B000#~Parabola of Hope~/MAP: Karmen Gate Sokshi/BGM: Moudamepon's Theme": "&H14O0R000G000B000#~Vòng cung hy vọng~/BẢN ĐỒ: Cổng Karmen Sokshi/Nhạc: Chủ đề Moudamepon",
    "&H14O0R000G000B000#~Recover the Zigoton Catapult!~/MAP: Ejiji Cliff/BGM: Totechitentan's Theme": "&H14O0R000G000B000#~Lấy lại máy bắn đá Zigoton!~/BẢN ĐỒ: Vách Ejiji/Nhạc: Chủ đề Totechitentan",
    "Well, well... thanks to/you, I've been chosen/as Lord Ormen/Karmen's successor.": "Ồ, ồ... nhờ/ngươi, ta được chọn/làm người kế vị/Chúa Ormen Karmen.",
    "PON PON CHAKA CHAKA.../Power of thunder,/come dwell in my hands!": "PON PON CHAKA CHAKA.../Sức sấm,/hãy ngự trong tay ta!",
    "&H18O1R255G255B255#The Aria of Attack!/○, ○, □, ○/PON PON PATA PON": "&H18O1R255G255B255#Khúc Tấn Công!/○, ○, □, ○/PON PON PATA PON",
    "&H18O1R255G255B255#PON PON PATA PON/Match the rhythm!/○, ○, □, ○": "&H18O1R255G255B255#PON PON PATA PON/Khớp nhịp!/○, ○, □, ○",
    "&H18O1R255G255B255#That's it!/○, ○, □, ○/PON PON PATA PON/Advance, advance!": "&H18O1R255G255B255#Đúng rồi!/○, ○, □, ○/PON PON PATA PON/Tiến lên, tiến lên!",
    "&H18O1R255G255B255#That's the way!/○, ○, □, ○/PON PON PATA PON/Hit the drum!": "&H18O1R255G255B255#Đúng cách đó!/○, ○, □, ○/PON PON PATA PON/Đánh trống!",
    "&H18O1R255G255B255#That's amazing! Keep going!/○, ○, □, ○/PON PON PATA PON/Beat them all!": "&H18O1R255G255B255#Tuyệt thật! Cứ tiếp!/○, ○, □, ○/PON PON PATA PON/Hạ sạch chúng!",
    "&H18O1R255G255B255#Perfect!!/That's the way to do it!/○, ○, □, ○/PON PON PATA PON": "&H18O1R255G255B255#Hoàn hảo!!/Làm đúng cách đó!/○, ○, □, ○/PON PON PATA PON",
    "&H18O1R254G096B120#When the Patapons finish their song/○, ○, □, ○/PON PON PATA PON/Hit the drum and take turns!": "&H18O1R254G096B120#Khi Patapon hát xong/○, ○, □, ○/PON PON PATA PON/Đánh trống và luân phiên!",
    "&H18O1R254G096B120#Keep your cool and hit the drum./○, ○, □, ○/PON PON PATA PON/Take turns, keep the rhythm!": "&H18O1R254G096B120#Giữ bình tĩnh và đánh trống./○, ○, □, ○/PON PON PATA PON/Luân phiên, giữ nhịp!",
    "PON PON, the Aria of Attack!/PON PON PATA PON/Good luck, Mighty Patapon!!": "PON PON, Khúc Tấn Công!/PON PON PATA PON/Cố lên, hỡi Người Chỉ Huy!!",
    "The opponent's shown an opening!/Use the PON PON Song to attack!": "Địch để lộ sơ hở!/Dùng bài PON PON mà tấn công!",
    "&H18O1R255G255B255#It's time to learn a new song./The PON PATA Requiem of/Retreat! Use it to run away/when you're in trouble!": "&H18O1R255G255B255#Đến lúc học bài mới./Khúc Rút Lui/PON PATA! Dùng để chạy/khi sa vào thế bí!",
    "&H18O1R254G096B120#When the Patapons finish their song,/○, □, ○, □/PON PATA PON PATA/Hit the drum and take turns!": "&H18O1R254G096B120#Khi Patapon hát xong,/○, □, ○, □/PON PATA PON PATA/Đánh trống và luân phiên!",
    "&H18O1R255G255B255#PON PATA PON PATA/Match the rhythm,/○, □, ○, □": "&H18O1R255G255B255#PON PATA PON PATA/Khớp nhịp,/○, □, ○, □",
    "&H18O1R255G255B255#That's it! That's the way!/○, □, ○, □/PON PATA PON PATA/Run away quickly!": "&H18O1R255G255B255#Đúng rồi! Đúng cách đó!/○, □, ○, □/PON PATA PON PATA/Chạy mau!",
    "&H18O1R255G255B255#That's great! Once again!/PON PATA PON PATA/Hit the drum!": "&H18O1R255G255B255#Tốt lắm! Thêm lần nữa!/PON PATA PON PATA/Đánh trống!",
    "&H18O1R255G255B255#That's amazing! Keep going!/PON PATA PON PATA/Run away quickly!": "&H18O1R255G255B255#Tuyệt thật! Cứ tiếp!/PON PATA PON PATA/Chạy mau!",
    "&H18O1R240G050B000#When the Patapons finish their song/○, □, ○, □/PON PATA PON PATA/Hit the drum and take turns!": "&H18O1R240G050B000#Khi Patapon hát xong/○, □, ○, □/PON PATA PON PATA/Đánh trống và luân phiên!",
    "&H18O1R240G050B000#Stay calm and hit the drum./○, □, ○, □/PON PATA PON PATA/Take turns with good rhythm!": "&H18O1R240G050B000#Bình tĩnh và đánh trống./○, □, ○, □/PON PATA PON PATA/Luân phiên, giữ nhịp tốt!",
    "&H18O1R255G255B255#It's time to learn a new song./The DON CHAKA Ballad of 1999!/It helps you recover from fire /and sleep attacks!": "&H18O1R255G255B255#Đến lúc học bài mới./Khúc 1999 của DON CHAKA!/Nó giúp ngươi hồi sau đòn lửa /và đòn ngủ!",
    "&H18O1R254G096B120#When the Patapons finish their song/□, ○, ×, △/PATA PON DON CHAKA/Hit the drum and take turns!": "&H18O1R254G096B120#Khi Patapon hát xong/□, ○, ×, △/PATA PON DON CHAKA/Đánh trống và luân phiên!",
    "&H18O1R255G255B255#PATA PON DON CHAKA/Match the rhythm!/□, ○, ×, △": "&H18O1R255G255B255#PATA PON DON CHAKA/Khớp nhịp!/□, ○, ×, △",
    "&H18O1R255G255B255#That's it! That's the way!/□, ○, ×, △/PATA PON DON CHAKA/It's a party, wha-haa!": "&H18O1R255G255B255#Đúng rồi! Đúng cách đó!/□, ○, ×, △/PATA PON DON CHAKA/Tiệc đây, ha ha!",
    "&H18O1R255G255B255#That's great! Once again!/PATA PON DON CHAKA/Hit the drum!": "&H18O1R255G255B255#Tốt lắm! Thêm lần nữa!/PATA PON DON CHAKA/Đánh trống!",
    "&H18O1R255G255B255#That's amazing! Keep going!/PATA PON DON CHAKA/Let's all celebrate!": "&H18O1R255G255B255#Tuyệt thật! Cứ tiếp!/PATA PON DON CHAKA/Cùng ăn mừng!",
    "&H18O1R240G050B000#When the Patapons finish their song/□, ○, ×, △/PATA PON DON CHAKA/Hit the drum and take turns!": "&H18O1R240G050B000#Khi Patapon hát xong/□, ○, ×, △/PATA PON DON CHAKA/Đánh trống và luân phiên!",
    "&H18O1R240G050B000#Keep calm and hit the drum./□, ○, ×, △/PATA PON DON CHAKA/Take turns with good rhythm!": "&H18O1R240G050B000#Giữ bình tĩnh và đánh trống./□, ○, ×, △/PATA PON DON CHAKA/Luân phiên, giữ nhịp tốt!",
    "&H18O1R254G096B120#When the Patapons finish their song/×, ×, △, △/DON DON CHAKA CHAKA/Hit the drum and take turns!": "&H18O1R254G096B120#Khi Patapon hát xong/×, ×, △, △/DON DON CHAKA CHAKA/Đánh trống và luân phiên!",
    "&H18O1R255G255B255#DON DON CHAKA CHAKA/Match the rhythm/×, ×, △, △": "&H18O1R255G255B255#DON DON CHAKA CHAKA/Khớp nhịp/×, ×, △, △",
    "&H18O1R255G255B255#That's it! That's the way!/×, ×, △, △/DON DON CHAKA CHAKA/Kick up your legs and jump!": "&H18O1R255G255B255#Đúng rồi! Đúng cách đó!/×, ×, △, △/DON DON CHAKA CHAKA/Nhấc chân mà nhảy!",
    "&H18O1R255G255B255#That's great! Once again!/DON DON CHAKA CHAKA/Hit the drum!": "&H18O1R255G255B255#Tốt lắm! Thêm lần nữa!/DON DON CHAKA CHAKA/Đánh trống!",
    "&H18O1R255G255B255#That's amazing! Keep going!/DON DON CHAKA CHAKA/Everybody jump! Jump!": "&H18O1R255G255B255#Tuyệt thật! Cứ tiếp!/DON DON CHAKA CHAKA/Mọi người nhảy! Nhảy!",
    "&H18O1R240G050B000#When the Patapons finish their song/×, ×, △, △/DON DON CHAKA CHAKA/Hit the drum and take turns!": "&H18O1R240G050B000#Khi Patapon hát xong/×, ×, △, △/DON DON CHAKA CHAKA/Đánh trống và luân phiên!",
    "&H18O1R240G050B000#Keep calm and hit the drum./×, ×, △, △/DON DON CHAKA CHAKA/Take turns with good rhythm!": "&H18O1R240G050B000#Giữ bình tĩnh và đánh trống./×, ×, △, △/DON DON CHAKA CHAKA/Luân phiên, giữ nhịp tốt!",
    "&H18O1R255G255B255#It's time for PON CHAKA, The /Hold Tight Hoe-Down! It will/help your troops endure enemy/attacks!": "&H18O1R255G255B255#Đến lúc PON CHAKA, /Điệu Nén Chịu! Nó sẽ/giúp quân ngươi chịu đòn/của địch!",
    "&H18O1R255G255B255#Well done! Once more!/PON PON CHAKA CHAKA/Hit the drum!": "&H18O1R255G255B255#Khá lắm! Thêm lần nữa!/PON PON CHAKA CHAKA/Đánh trống!",
    "&H18O1R255G255B255#Amazing! Keep on!/PON PON CHAKA CHAKA/Shout a battle cry!": "&H18O1R255G255B255#Tuyệt! Cứ tiếp!/PON PON CHAKA CHAKA/Hét tiếng xung trận!",
    "Dance and party!/Is it 1999?/PATA PON PON": "Nhảy và mở tiệc!/Đã đến 1999 chưa?/PATA PON PON",
    "According to the legends, the/sacred Kibapon will rise from/roots of the Yaripon Pyopyo...": "Theo truyền thuyết,/Kibapon thiêng sẽ trỗi lên từ/gốc Yaripon Pyopyo...",
    "~Karmen Fortress in Usso Forest Lv. <N10>~/The fortress in Usso Forest has been rebuilt! You've/captured it once so it's not in your way anymore, but/you should revisit it to uncover some hidden loot!": "~Pháo đài Karmen trong Rừng Usso Lv. <N10>~/Pháo đài ở Rừng Usso đã được dựng lại! Ngươi/đã chiếm một lần nên nó không còn chặn đường, nhưng/nên quay lại để moi đồ giấu!",
    "~Gong's Trial~/Gong retreated without even fighting you, so what on/earth could he want now? What could Gong's/trial at the Gangoro Wasteland possibly be!?": "~Thử thách của Gong~/Gong rút lui mà không đánh, vậy rốt cuộc/hắn muốn gì? Thử thách của Gong/ở Hoang mạc Gangoro là gì thế!?",
    "~Fortress at Ejiji Cliff~/Guided by Gong's words, the Patapons head into the/skies above, where another Karmen fortress stands/before them. It's time to prepare for battle!": "~Pháo đài trên Vách Ejiji~/Theo lời Gong, Patapon tiến lên/trời cao, nơi một pháo đài Karmen khác đứng/trước mặt. Đến lúc sửa soạn chiến đấu!",
    "~Recover the Zigoton Catapult!~/Oh no! The Zigoton catapult that Gong prepared for/your side has been stolen by the Karmen army!/Recover it from the peak of the Ejiji Cliffs!": "~Lấy lại máy bắn đá Zigoton!~/Ôi không! Máy bắn đá Zigoton Gong chuẩn bị cho/phe ngươi đã bị quân Karmen cướp!/Lấy lại từ đỉnh Vách Ejiji!",
    "~Kimen the Spearbearer~/Kimen the Spearbearer is a calculating man and one of/the Karmens' three great generals. He is a true rival/to the Hero Patapon Don Yumipon. Protect the catapult/across the Moakan Desert!": "~Kimen Kẻ Cầm Giáo~/Kimen Kẻ Cầm Giáo là người tính toán, một trong/ba đại tướng Karmen. Hắn là đối thủ thật sự/của Anh hùng Patapon Don Yumipon. Hãy bảo vệ máy bắn đá/băng Sa mạc Moakan!",
    "~Black Hoshipon Eternal~/The Patapons have finally returned home! But the/place of the Patapons' birth, Patapole, is now a ruined /wasteland under Ormen Karmen's control.": "~Hoshipon Đen Vĩnh Cửu~/Patapon cuối cùng cũng về nhà! Nhưng/nơi Patapon sinh ra, Patapole, nay là hoang địa /tan hoang dưới quyền Ormen Karmen.",
    "I think Gong's/leading us somewhere,/though I can't imagine/why...": "Ta nghĩ Gong/đang dẫn chúng ta đi đâu đó,/dù ta không hình dung/nổi vì sao...",
    '"Melody with a Bounce”/DON DON CHAKA CHAKA/Jump up in the air!/Jump♪ Jump♪ Jump/like you just don\'t care!': '"Khúc Nhảy”/DON DON CHAKA CHAKA/Nhảy lên không!/Nhảy♪ Nhảy♪ Nhảy/mặc kệ đời!',
    '"The Ballad of 1999"/PATA PON DON CHAKA/Are you ready to party?!/♪ Party like it\'s 1999 ♪': '"Khúc 1999"/PATA PON DON CHAKA/Sẵn sàng mở tiệc chưa?!/♪ Tiệc như năm 1999 ♪',
    "Long ago, a lone Pata-monk/reached Nirvana beneath this /massive tree. Its trunk, said to /possess a special power, will/stay fresh for eternity.": "Xưa, một thầy tu Pata/đạt Niết bàn dưới gốc /cây khổng lồ này. Thân cây, đồn /có sức đặc biệt, sẽ/tươi mãi.",
    "The seed of Mater, the tree/of life. It's an extremely/precious seed and its/existence is a symbol of hope/for the Patapon's future.": "Hạt Mater, cây/sự sống. Hạt cực/quý, và sự/tồn tại của nó là dấu hy vọng/cho tương lai Patapon.",
    "This unique, fearsome/spear made in Mighty /Patapon's honor has critical,/knockback, stagger, and/piercing abilities.": "Ngọn giáo độc, dữ dội/này, làm để tôn Người /Chỉ Huy, có chí mạng,/đẩy lùi, choáng, và/xuyên thấu.",
    "This powerful, unique lance/made in the Mighty Patapon's/honor raises attack speed/and causes critical,/knockback, and stagger/effects.": "Ngọn thương mạnh, độc,/làm để tôn Người Chỉ Huy,/tăng tốc đánh/và gây chí mạng,/đẩy lùi, và/choáng.",
    "This powerful, unique axe/made in the Mighty Patapon's/honor raises attack speed,/stagger, and knockback.": "Chiếc rìu mạnh, độc,/làm để tôn Người Chỉ Huy,/tăng tốc đánh,/choáng, và đẩy lùi.",
    "This powerful, unique horn/made in the Mighty Patapon's/honor can pierce enemies, and/has high critical, knockback,/and stagger abilities.": "Chiếc kèn mạnh, độc,/làm để tôn Người Chỉ Huy,/xuyên được địch, và/có chí mạng, đẩy lùi,/và choáng rất cao.",
    "~Karmen Battle Egg~ /A mysterious egg that/leads you to the battle/with the Karmens in Usso /Fortress. It has all of /Pataporon's equipment.": "~Trứng chiến Karmen~ /Quả trứng bí ẩn/dẫn ngươi tới trận/với Karmen ở Pháo đài /Usso. Nó có đủ /trang bị của Pataporon.",
    "~Karmen Gate Battle Egg~ /A mysterious egg that/leads you to the battle of/despair at Karmen castle/gate. It grants Mighty/Mutaron's fierce power.": "~Trứng chiến Cổng Karmen~ /Quả trứng bí ẩn/dẫn ngươi tới trận/tuyệt vọng ở cổng/lâu đài Karmen. Nó ban sức dữ/của Mutaron vĩ đại.",
    'Clad in crimson armor,/he shouts, "When you see/them, strike! Strike! Don\'t/look away, strike! Strike!/I don\'t care who I\'m facing,/just strike!!!"': 'Khoác giáp đỏ thẫm,/hắn hét, "Thấy/chúng thì đâm! Đâm! Đừng/nhìn đi chỗ khác, đâm! Đâm!/Ta không cần biết đối thủ là ai,/cứ đâm!!!"',
    "The Horseman of/Pata-Pon-calypse, his/fatal strength and bravery is/feared by many! Sadly, he's/not the brightest of bulbs.": "Kỵ sĩ của/Pata-Pon-calypse, sức/chí mạng và lòng gan của hắn/khiến nhiều kẻ sợ! Tiếc là hắn/không sáng dạ cho lắm.",
    "A Patapon heavy hitter that /delivers fatal blows with every/strike. Resistant to fire and/electric attacks, but staggers/easily.": "Patapon đánh nặng, /mỗi đòn đều chí mạng./Kháng lửa và/đòn điện, nhưng dễ/choáng.",
    "Press the□Button from the hero's/equip change screen to class change!//You can change him to any of the classes/you currently have units of:/Yaripon, Tatepon, Yumipon, etc.": "Nhấn nút□từ màn hình/đổi trang bị anh hùng để đổi lớp!//Ngươi đổi hắn sang lớp nào/mà ngươi đang có đơn vị:/Yaripon, Tatepon, Yumipon, v.v.",
    "If you look closely, you'll notice/that the wind sometimes changes direction.//When the wind stops,/that is when the wind will change.//Read the wind's direction/and look for the best time to use PON PON!": "Nhìn kỹ, ngươi sẽ thấy/gió đôi khi đổi hướng.//Khi gió dừng,/ấy là lúc gió sắp đổi.//Đọc hướng gió/và chọn lúc đẹp nhất để dùng PON PON!",
    "Hunt the fast-running Motiti birds.//The Motitis have a good sense of smell,/so you shouldn't approach them in a tailwind.//Be patient, and wait with CHAKA CHAKA./When you get a headwind, use PON PON/and have the Yaripon target them with spears!": "Săn chim Motiti chạy nhanh.//Motiti đánh hơi giỏi,/đừng áp lại khi có gió xuôi.//Kiên nhẫn, chờ bằng CHAKA CHAKA./Khi có gió ngược, dùng PON PON/và để Yaripon nhắm giáo vào chúng!",
    "Advance your army forward led by Hatapon./This all-purpose command is the PATA PATA Song.//The Patapons hate to retreat, so once/you send them forward, they won't step down themselves.//Whether to attack from afar/or march forward avoiding arrows,/make your decisions depending on the state of battle.": "Đưa quân tiến, Hatapon dẫn đầu./Lệnh đa dụng này là bài PATA PATA.//Patapon ghét rút, nên một khi/ngươi đẩy họ lên, họ không tự lùi.//Đánh từ xa/hay tiến lên né tên,/hãy quyết theo thế trận.",
    "Use this song when you want to deal big damage./This courageous command is the PON PON Song.//If you use PON PON while in Fever status,/the Patapons' morale will be tops!//Your defense is low while you use PON PON,/so decide on the best timing for attack and defense./PON PON is the move of the ultimate leader.": "Dùng bài này khi muốn gây sát thương lớn./Lệnh dũng cảm này là bài PON PON.//Dùng PON PON khi đang Fever,/khí thế Patapon lên đỉnh!//Phòng thủ thấp khi dùng PON PON,/nên chọn đúng lúc đánh và thủ./PON PON là nước của người chỉ huy tối cao.",
    "Reduces the damage dealt by enemy bosses and armies./This wise command is the CHAKA CHAKA Song.//This also lowers the attach rate of fire and ice statuses,/and the effect on defense is magnified while in Fever status.//However, this severely lowers your attack power, so use/it while you're in danger or you have to soak an attack,/and look for an interval when you can swap to PON PON.": "Giảm sát thương từ trùm và quân địch./Lệnh khôn ngoan này là bài CHAKA CHAKA.//Nó cũng giảm tỉ lệ dính lửa và băng,/và hiệu quả phòng thủ tăng khi đang Fever.//Nhưng sức đánh giảm mạnh, nên dùng/khi đang nguy hoặc phải hứng đòn,/rồi tìm khoảng để chuyển sang PON PON.",
    "Tatepons are known as the true tanks/of the Patapon army.//They'll link up their shields as they/march during Fever status, and act/as your guardians on the front line.//If you erect a giant shield with Fever CHAKA CHAKA,/they can bear under all kinds of damage./They're the front-line shields of the Patapon army.": "Tatepon được biết là lá chắn thật/của quân Patapon.//Họ nối khiên khi/tiến trong Fever, và đứng/thành hộ vệ ở tuyến đầu.//Nếu dựng khiên khổng lồ bằng CHAKA CHAKA Fever,/họ chịu được đủ loại sát thương./Họ là khiên tuyến đầu của quân Patapon.",
    "The Kibapons go riding splendidly into battle on horseback,/star actors who withdraw after a single hit.//Their defense goes up during Fever strikes,/and they can deal consecutive damage to/any enemy they touch.//They're extremely weak when not in Fever,/but it's easy to get dependent on them./They're the best damage dealers of the Patapon army.": "Kibapon phi ngựa oai vệ vào trận,/diễn viên chính rút lui sau một đòn.//Phòng thủ tăng khi đánh trong Fever,/và họ gây sát thương liên tiếp lên/mọi địch họ chạm.//Họ cực yếu khi không Fever,/nhưng dễ thành lệ thuộc./Họ là tay sát thương mạnh nhất quân Patapon.",
    "Born of a sudden mutation, these giant Dekapons/can wreak havoc on the front lines.//Their NOSHINOSHIZUGAN from PON CHAKA/will shake the earth to send enemies tumbling.//They're extremely heavy and won't be/knocked back, and they combine/extraordinarily high offense and defense./They're the greatest attackers among the Patapon army.": "Sinh từ đột biến, Dekapon khổng lồ/có thể tàn phá tuyến đầu.//NOSHINOSHIZUGAN từ PON CHAKA/rung đất, hất địch ngã.//Họ cực nặng, không bị/đẩy lùi, và gộp/công thủ cao khác thường./Họ là kẻ tấn công mạnh nhất quân Patapon.",
    "Hatapons indicate the center of the army.//During the PATA PATA Song, the Hatapon/marches with the rest of the army.//When you attack with the PON PON Song,/the Hatapon doesn't move.": "Hatapon đánh dấu tâm đội quân.//Trong bài PATA PATA, Hatapon/tiến cùng cả quân.//Khi ngươi tấn công bằng bài PON PON,/Hatapon đứng yên.",
    "If you get perfect timing/on all four of the command drum beats,/you'll end up with a pleasing, perfect sound!//If you get a Perfect on any song besides Pata Pata/while in Fever status, a Hero will/take you into Hero Mode!//This has many different effects based on class,/so use all the Hero Modes to ride out tough situations!": "Nếu ngươi đúng nhịp hoàn hảo/cả bốn tiếng trống lệnh,/sẽ có tiếng hoàn hảo, êm tai!//Nếu được Perfect ở bài nào ngoài Pata Pata/khi đang Fever, một Anh hùng sẽ/đưa ngươi vào Chế độ Anh hùng!//Hiệu quả đổi theo lớp,/hãy dùng mọi Chế độ Anh hùng để vượt thế bí!",
    "The PON PON attack is strong enough/that you may forget the CHAKA CHAKA defense.//When the boss starts an attack,/make sure to use CHAKA CHAKA when/the enemy squadron rallies for a big push,/the grass starts to smolder,/or whenever you sense danger coming.": "Đòn PON PON mạnh đến mức/ngươi có thể quên phòng thủ CHAKA CHAKA.//Khi trùm bắt đầu tấn công,/nhớ dùng CHAKA CHAKA khi/đội địch dồn lực đánh lớn,/cỏ bắt đầu cháy âm ỉ,/hoặc mỗi khi ngươi cảm thấy nguy đến.",
    'Defend against "Large Armies" and "Kiba"/by putting Tatepons in front and using CHAKA CHAKA.//If you have Kibapons in your formation,/this becomes even more effective.//This "Tatepon Defense Hidden/Kiba CHAKA CHAKA" is/a famous Patapon technique.': 'Chống "Đại quân" và "Kiba"/bằng cách để Tatepon phía trước và dùng CHAKA CHAKA.//Nếu đội hình có Kibapon,/cách này còn hiệu quả hơn.//"Phòng thủ Tatepon giấu/Kiba CHAKA CHAKA" là/tuyệt kỹ nổi tiếng của Patapon.',
    "Using CHAKA CHAKA usually reduces/the damage from a boss attack.//However, the Hatapon doesn't get/a defense boost from CHAKA CHAKA,/so he can't defend this way.//Instead, have him use the PON PATA Song/to simply dodge the boss's attacks!": "Dùng CHAKA CHAKA thường giảm/sát thương từ đòn trùm.//Nhưng Hatapon không được/tăng phòng thủ từ CHAKA CHAKA,/nên không thủ kiểu này được.//Thay vào đó, hãy để hắn dùng bài PON PATA/để né đòn của trùm!",
    "Use PON CHAKA to charge up your/PON PON attack do deal huge damage/even without Fever status.//Dekapons and Robopons have some attacks/that only PON CHAKA will activate./These have very powerful effects.//You can also combine PON CHAKA and CHAKA CHAKA/for the best defense available.": "Dùng PON CHAKA để nạp/đòn PON PON gây sát thương lớn/kể cả khi chưa Fever.//Dekapon và Robopon có đòn/chỉ PON CHAKA mới kích./Những đòn ấy rất mạnh.//Ngươi cũng gộp PON CHAKA với CHAKA CHAKA/để có lối phòng thủ mạnh nhất.",
    "Use this command to escape ground attacks/like lasers and direct charges!//Use the DON DON CHAKA CHAKA command/to get jumps with awesome hang time.//There are some bosses that can hit you/even in the air, though, so be careful!": "Dùng lệnh này để thoát đòn mặt đất/như tia và cú lao thẳng!//Dùng lệnh DON DON CHAKA CHAKA/để nhảy, lơ lửng rất lâu.//Vài trùm vẫn đánh trúng/kể cả khi ngươi ở trên không, nên cẩn thận!",
    "If you are frozen or put to sleep,/don't just sit around waiting/for death...//Instead, use the PATA PON DON CHAKA/Song to restore yourself.//You won't get status effects/while the DON CHAKA Song is playing, either!": "Nếu bị đóng băng hoặc ngủ,/đừng ngồi chờ/chết...//Hãy dùng bài PATA PON DON CHAKA/để hồi lại.//Ngươi cũng không dính hiệu ứng/khi bài DON CHAKA đang chơi!",
    "The Zigoton Hero, Gong the Hawkeye/appeared as the Patapons' rival in the first game.//He fought for the Zigoton queen Kharma,/to stop the Patapons' invasion of his country.//Through many battles, he struck blows against/the Patapons, but in the end was betrayed by/Makoton, and left for dead in the Doyon Fields.": "Anh hùng Zigoton, Gong Mắt Ưng/xuất hiện như đối thủ của Patapon ở phần một.//Hắn chiến đấu cho nữ hoàng Zigoton Kharma,/để chặn Patapon xâm lược đất hắn.//Qua nhiều trận, hắn đánh đau/Patapon, nhưng cuối cùng bị/Makoton phản, bỏ mặc hấp hối ở Cánh đồng Doyon.",
    "Aiton and Makoton are/Zigoton soldiers set in a small watchtower/by the Tamaran Desert to the/Zigoton's border.//One day, Aiton spotted the Patapon army/marching toward Earthend./He tried to defend the tower, but in the deadly fight,/Makoton panicked and fled...": "Aiton và Makoton là/lính Zigoton đóng ở tháp canh nhỏ/cạnh Sa mạc Tamaran, nơi/biên giới Zigoton.//Một hôm, Aiton thấy quân Patapon/tiến về Earthend./Hắn cố giữ tháp, nhưng trong trận chết chóc,/Makoton hoảng và bỏ chạy...",
    "Centura bosses are very weak against fire./This is why they only appear in the rain.//Their central head is their weak point./Attacks to this point deal double damage.//The Yaripon Hero's ultimate attack,/can reliably deal damage to the weak point./This is very effective in the early game.": "Trùm Centura rất yếu trước lửa./Vì thế chúng chỉ hiện khi trời mưa.//Đầu ở giữa là điểm yếu./Đánh vào đó gây sát thương gấp đôi.//Đòn tối thượng của Anh hùng Yaripon/đánh trúng điểm yếu khá chắc./Rất hiệu quả ở đầu game.",
    "Kunels are easy to put to sleep./Especially when their HP is low.//However, many of the Kunel's attacks/can't be defended with CHAKA CHAKA.//If you don't have the PON PATA Song,/get the unopenable box in the Bryun Snowfields,/and beat Dogaeen in the Neogain Ruins.": "Kunel dễ bị ru ngủ./Nhất là khi máu thấp.//Nhưng nhiều đòn của Kunel/không phòng được bằng CHAKA CHAKA.//Nếu chưa có bài PON PATA,/hãy lấy hộp không mở được ở Cánh đồng tuyết Bryun,/và hạ Dogaeen ở Di tích Neogain.",
    "When you reach the goal and carry the egg/to the pedestal, the DON CHAKA will begin.//If you hit the drum well with DON CHAKA/and get a good result, you'll get/Komupon and Hero Mask from the egg.//If you miss the last drum beat,/you'll only get a normal rare item.": "Khi tới đích và đặt trứng/lên bệ, DON CHAKA sẽ bắt đầu.//Nếu đánh trống tốt với DON CHAKA/và được kết quả khá, ngươi nhận/Komupon và Mặt nạ Anh hùng từ trứng.//Nếu trượt tiếng trống cuối,/ngươi chỉ nhận vật hiếm thường.",
}


def main() -> None:
    for source, vi in HAND.items():
        if source.count("/") != vi.count("/"):
            raise SystemExit(f"Lệch dấu /: {source[:60]}")
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    # Câu gốc không còn trong CSV nghĩa là bản trích đã đổi. Dừng, không ghi nửa chừng.
    sources = {row["source"] for row in rows}
    missing = [source for source in HAND if source not in sources]
    if missing:
        raise SystemExit(f"{len(missing)} câu gốc không có trong CSV: {missing[0][:60]}")
    changed = 0
    for row in rows:
        vi = HAND.get(row["source"])
        if vi is None or vi == row["vi"]:
            continue
        row["vi"] = vi
        row["status"] = "review"
        row["note"] = "viết tay"
        changed += 1
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, ["id", "context", "source", "vi", "status", "note"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"viết tay {changed} dòng")


if __name__ == "__main__":
    main()
