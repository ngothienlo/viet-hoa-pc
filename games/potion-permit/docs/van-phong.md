# Văn phong

Potion Permit là game nhẹ nhàng, ấm áp. Thị trấn nhỏ trên đảo, người dân nghi ngờ người lạ lúc đầu rồi dần thân thiết. Câu dịch phải nghe như người Việt nói chuyện với nhau, không như dịch máy.

Bảng này chỉ dùng cho Potion Permit. Không lấy quy ước của game khác.

## Nhân vật chính

- Nghề: Dược sư. Người trẻ, mới ra nghề. Hội Y khoa gọi là «kid», «little Chemist», nên tuổi khoảng hai mươi.
- Không nói thành lời. Game không có dòng thoại hay lựa chọn hội thoại của nhân vật chính. Mọi câu đều là NPC nói, lời kể, hoặc UI.
- **Giới tính do người chơi chọn.** Màn tạo nhân vật có mục giới tính (`UI/UI_CHAR_CREATION_GENDER`). Bản Anh né đại từ: gọi bằng tên, «the chemist», hoặc «they».
  - `MOIRA/EVENTDIALOG_OPENING_TRAINSTATION_04`: «Do you think {[CHARACTER_NAME]} will manage on their own?»
  - `Quest/QUEST_FORREST_FP1_01_DETAIL`: «Forrest and {[CHARACTER_NAME]} arranged to meet… They're hoping…»
  - `Furniture/FURNITURE_DECO_POSTER_01_DETAIL` và `_02_DETAIL`: hai tấm áp phích dược sư tập sự nữ và nam.
- Game chỉ có một placeholder là `{[CHARACTER_NAME]}`. Không có placeholder giới tính. Vì vậy câu Việt phải đúng với cả nam lẫn nữ.

### Đại từ trung tính cho nhân vật chính

Được dùng:

- Tên: `{[CHARACTER_NAME]}`.
- Danh xưng: «Dược sư».
- «cháu», «con»: người lớn tuổi gọi.
- «em»: người lớn hơn vài tuổi gọi. Trẻ con tự xưng «em» được, vì từ này không nói gì về giới của người nghe.
- «cậu»: bạn đồng trang lứa gọi nhau kiểu «tớ – cậu», «mình – cậu», «tôi – cậu».
- «nhóc»: người lớn trêu thân mật (Collin, Leano).
- «cưng»: lời âu yếm, không theo giới (Helene, Hannah).
- «bạn»: chỉ trong UI, hướng dẫn, hộp xác nhận.

Không dùng cho nhân vật chính: «anh», «chị», «chú», «cô», «ông», «bà», «chàng», «nàng», «cậu bé», «cô gái», «người đẹp», «anh ấy», «cô ấy».

NPC tự xưng theo giới của chính NPC thì được. Ví dụ Collin xưng «anh», Helene xưng «chị». Người nghe là nam hay nữ đều hợp.

Người lớn hơn nhiều tuổi không gọi nhân vật chính là «cậu». Từ người lớn tuổi, «cậu» nghe như gọi con trai. Dùng «cháu», «Dược sư» hoặc tên.

Khi đại từ lặp lại nhiều, bỏ chủ ngữ. Tiếng Việt cho phép điều này: «Đến đây làm gì?» thay cho «Cậu đến đây làm gì?».

### Ngôi thứ ba

Trong nhiệm vụ, tiểu sử, bảng tin: gọi bằng tên hoặc «Dược sư». Không dùng «anh ấy», «cô ấy», «họ» cho một người.

- `Martha starts keeping her distance from {[CHARACTER_NAME]}, who gets worried and tries to track her down` → «Martha bắt đầu tránh mặt {[CHARACTER_NAME]}. Lo lắng, Dược sư tìm cách gặp cô ấy để nói chuyện.» Câu Việt phải giữ đúng số placeholder của câu gốc, nên lần nhắc thứ hai dùng «Dược sư».
- `the chemist` chỉ nhân vật chính → «Dược sư», viết hoa. Kể cả trong lời thoại: «Cái đứa mới đến, Dược sư đấy à?».

NPC ở ngôi thứ ba (tiểu sử `BG_STORY`, nhiệm vụ, bảng tin): mỗi NPC một đại từ, dùng giống nhau ở mọi chỗ. Không dùng «cậu ta», «anh ta», «cô ta» (nghe coi thường).

| Đại từ | NPC |
| --- | --- |
| ông | Myer, Osman, Garret, Nestor, Zeke |
| bà | Mercy, Nova |
| anh, anh ấy | Collin, Dean, Derrek, Lucke, Matheo, Reyner, Victor, Xiao, Yorn, Forrest, Ottmar |
| cô, cô ấy | Mariele, Cassandra, Opalheart, Leano, Helene, Olive, Moira, Martha, Hannah, Bubble, Rue, Runeheart, Socellia |
| cậu ấy | Dev, Dan |
| cô bé, cậu bé | Laura, Russo |

Đã có tên ở câu trước thì câu sau bỏ đại từ hoặc nhắc lại tên, đừng lặp «anh ấy» nhiều lần trong một đoạn.

### Nếu sau này có lời của nhân vật chính

Hiện chưa có. Nếu bản cập nhật thêm lựa chọn hội thoại:

- Nhân vật chính tự xưng bằng từ trung tính: «tôi» với người lạ và người lớn, «cháu» với người đáng tuổi cô chú, «mình» hoặc «tớ» với bạn, «em» với người lớn hơn vài tuổi.
- Gọi NPC theo cặp đối ứng trong bảng dưới. NPC gọi nhân vật chính là «cháu» thì nhân vật chính gọi lại «cô/chú/bác + tên». NPC gọi «cậu» thì gọi lại «cậu». Trẻ con thì gọi «em».
- Không để nhân vật chính xưng «anh» hay «chị».

## Xưng hô của từng NPC với nhân vật chính

Tuổi ước lượng từ tiểu sử và lời thoại. «Gọi» là cách NPC gọi nhân vật chính. Ngoài cách gọi trong cột, NPC luôn được gọi bằng tên hoặc «Dược sư» khi bản Anh gọi như vậy.

| NPC | Vai trò, tuổi | NPC xưng | Gọi nhân vật chính | Giọng |
| --- | --- | --- | --- | --- |
| Bubble | Kiểm lâm phụ tá, cô gái trẻ | tớ | cậu | Vui, mơ mộng, mê cây cỏ thú rừng. Hay cảm động |
| Cassandra | Phụ việc ở Nhà tắm, vợ Osman, trung niên | chị | em | Dịu dàng, chăm chỉ, hay lo âu. Câu ngập ngừng khi căng thẳng |
| Collin | Thành viên Hội Y khoa, người lớn | anh | nhóc, em | Lắm lời, đùa giỡn, cường điệu. «little Chemist» → «nhóc Dược sư» |
| Dan | Nhân cách cướp biển của Dev | ta | nhà ngươi | Hò hét kiểu cướp biển. Thán từ biển cả: «Sấm sét đại dương!» cho «Barnacles!» |
| Dean | Cảnh sát, anh sinh đôi, thanh niên | tớ | cậu | Hiền, lười, ham ăn. Hay lắp bắp khi bị bắt lỗi |
| Derrek | Cảnh sát, em sinh đôi, thanh niên | tôi | cậu | Thẳng, sôi nổi, mê tập luyện. Lúc đầu hơi coi thường, sau thân |
| Dev | Người đưa thư, thanh niên | tôi | Dược sư, cậu | Lễ phép, ít nói, nhỏ nhẹ |
| Forrest | Trưởng kiểm lâm, người lớn | tôi | Dược sư, tên | Ít lời, khô, thích cô độc. Câu ngắn |
| Garret | Chủ Trang trại, cha của Lucke và Laura, ngồi xe lăn, trung niên | bác | cháu | Cộc cằn, khó chịu. Hay bỏ chủ ngữ: «Đến đây làm gì? Muốn gì?» |
| Hannah | Phụ tá tiệm may, cô gái trẻ | mình | cưng («sugar») | Sành điệu, nhiệt tình, hay tự ti về tay nghề |
| Helene | Làm ở Khu trò chơi, thầy bói tarot, người lớn | chị | cưng («sweetheart», «sweetie-pie») | Lả lơi, bí ẩn, trêu chọc. Có thể hẹn hò |
| Kipps | Mèo đen của Zeke, cái | không | không | Chỉ kêu: «Meo!», «Meo meo!», «Meo…», «Méo.» (Mrow), «Khèèè!» (Hiss) |
| Laura | Con út nhà Garret, bé gái | em | Dược sư, tên | Hồn nhiên, ngoan, thương gia đình |
| Leano | Chủ tiệm câu Primerose Sail, cựu cướp biển, lớn tuổi | ta | nhóc, thủy thủ («matey») | Giọng thủy thủ già, phóng khoáng: «ye» → «nhóc». Có thể hẹn hò |
| Lucke | Con cả nhà Garret, thanh niên | tôi | cậu | Hiền, lễ độ, mê sách, hay xin lỗi. Có thể hẹn hò |
| Mariele | Vợ Myer, mẹ Rue, trung niên | cô | cháu («dear» → «cháu à») | Quý phái, hậu đậu, hay quên. «Oh dear» → «Trời ơi» |
| Martha | Phục vụ ở Quán rượu, người nơi khác đến, cô gái trẻ | mình | cậu | Nhỏ nhẹ, rụt rè, hay xin lỗi. Có thể hẹn hò |
| Matheo | Thầy lang đời thứ bảy, thanh niên | tôi | cậu | Lạnh, gay gắt, ghét dược sư lúc đầu. Dịu dần khi thân. Có thể hẹn hò |
| Mercy | Vợ Garret, mẹ Lucke và Laura, trung niên | bác | cháu, con («child») | Nghiêm, nói thẳng, thương kiểu nghiêm khắc |
| Moira | Thành viên Hội Y khoa, người lớn | tôi | cậu | Nghiêm, lạnh, hay hoài nghi. Khen thì khen ngắn |
| Myer | Thị trưởng, cha Rue, trung niên | chú | cháu | Ân cần, chững chạc, đôi lúc đãng trí |
| Nestor | Bác sĩ, đứng đầu Hội Y khoa, lớn tuổi | tôi, chúng tôi | Dược sư, tên | Trang trọng, lịch sự kiểu công vụ |
| Nova | Chủ tiệm may, cựu nhà thiết kế ở Thủ đô, góa chồng, trung niên | tôi | Dược sư, tên | Kiêu kỳ, xa cách, chê thẳng. Buồn khi nhắc chồng |
| Olive | Chủ Nhà tắm đời thứ bảy, người lớn | chị | em | Điềm đạm, gắn bó với lề lối cũ |
| Opalheart | Thợ rèn lừng danh, mẹ Runeheart, trung niên | cô | cháu | Mạnh mẽ, to tiếng, tự hào về nghề |
| Osman | Cảnh sát trưởng, chồng Cassandra, trung niên | tôi | Dược sư, tên | Nghiêm, cứng nhắc, ít lời. Vụng về khi nói chuyện tình cảm |
| Ottmar | Phụ tá tiệm câu, to xác, chậm hiểu | Ottmar | Dược sư, tên | Tự gọi mình bằng tên. Câu cụt, đơn giản: «Ottmar cần làm việc.» Mê ngô |
| Reyner | Thợ mộc duy nhất trên đảo, thanh niên | tôi | cậu | Hăng hái, tự tin quá mức, cười lớn «Hahaha!». Có thể hẹn hò |
| Rue | Con gái Myer, muốn thành dược sư, cô gái trẻ | mình | cậu | Vui vẻ, lạc quan, hiếu động. Có thể hẹn hò |
| Runeheart | Con gái và học trò của Opalheart, cô gái trẻ | tôi | cậu | Nóng nảy, cứng đầu, nói cụt: «Oi» → «Này!». Có thể hẹn hò |
| Russo | Trẻ mồ côi ở Tu viện, bé trai | em | Dược sư, tên | Nghịch ngợm, bướng, hay «Hừ!». Cô đơn bên trong |
| Socellia | Nữ tu coi Nhà thờ, giám hộ Russo, người lớn | Sơ | em | Hiền, nghiêm túc mà vụng về. «dear gods» → «Các vị thần ơi» |
| Victor | Người giữ nghĩa trang, thanh niên | tôi | cậu | Kỳ quặc, rùng rợn, cười «Hehehe». Nói chuyện với bạn vô hình. Có thể hẹn hò |
| Xiao | Thủ quỹ, gia sư của Rue, thanh niên | tôi | cậu | Điềm tĩnh, lý trí, chuẩn mực. Có thể hẹn hò |
| Yorn | Chủ Quán rượu, trung niên | tôi | Dược sư, tên | Ít nói, trông dữ nhưng tốt bụng |
| Zeke | Người vô gia cư, chủ mèo Kipps, lớn tuổi | bác | cháu | Thong thả, vô lo, nói chậm, triết lý vặt |

Ghi chú:

- Dan và Dev là một người. Dan gọi Dev là «gã Dev» hoặc «cái tên chán ngắt Dev». Dan gọi người lạ là «lũ chuột đất liền» (landlubbers).
- Khi NPC tức giận vì uy tín thấp (`ANGRY_DIALOG`) hoặc từ chối quà (`REJECTION_DIALOG`), giữ đúng cặp xưng hô, chỉ đổi giọng.
- NPC có thể hẹn hò giữ nguyên cặp xưng hô sau khi tỏ tình. Sự thân mật thể hiện bằng lời: gọi tên, «cưng», «người thương». Không chuyển sang «anh yêu», «em yêu» vì sẽ lộ giới.
- Bảng tin do NPC viết dùng cùng cặp xưng hô. «Dear {[CHARACTER_NAME]},» → «Gửi {[CHARACTER_NAME]},». «Dear Chemist,» → «Gửi Dược sư,».

## Xưng hô giữa các NPC

| Quan hệ | A nói với B | B nói với A |
| --- | --- | --- |
| Osman và Cassandra, vợ chồng | Osman: anh – em | Cassandra: em – anh. «dear» → «anh à», «mình ơi» |
| Garret và Mercy, vợ chồng lớn tuổi | Garret: tôi – bà, «bà nó» | Mercy: tôi – ông, «ông nó» |
| Myer và Mariele, vợ chồng | Myer: anh – em | Mariele: em – anh |
| Garret, Mercy với Lucke, Laura | bố, mẹ – con | con – bố, mẹ. «Mama», «Papa» → «mẹ», «bố» |
| Myer, Mariele với Rue | bố, mẹ – con | con – bố, mẹ |
| Lucke với Laura, anh em | anh – em | em – anh Lucke |
| Opalheart với Runeheart, mẹ con và thầy trò | mẹ – con | con – mẹ. «Mum!» → «Mẹ!» |
| Dean với Derrek, anh em sinh đôi | anh – em | em – anh |
| Dean, Derrek với Osman, cấp dưới | tôi – sếp, «Sir» → «Thưa sếp» | Osman: tôi – cậu, «các cậu» |
| Forrest với Bubble, cấp trên | anh – em | em – anh Forrest |
| Nova với Hannah, chủ và phụ tá | chị – em | em – chị Nova |
| Leano với Ottmar, chủ và phụ tá | ta – cậu, gọi «Ottmar» | Ottmar – Leano. Ottmar luôn gọi tên |
| Yorn với Martha, chủ và nhân viên | tôi – cô | tôi – anh Yorn |
| Myer với Xiao, thị trưởng và thủ quỹ | tôi – cậu | Xiao: tôi – ngài Myer |
| Xiao với Rue, gia sư và học trò | anh – em | em – anh Xiao |
| Socellia với Russo, người giám hộ | Sơ – con | con – Sơ, «Sơ Socellia» |
| Russo với Laura, bạn chơi | tớ – cậu | tớ – cậu |
| Cassandra với Olive, bạn | chị – em | em – chị |
| Zeke với Kipps | bác – cưng, «bé ngoan» | |
| Collin với Moira, đồng nghiệp | anh – em, gọi «Moira» | tôi – anh |
| Collin, Moira với Nestor | tôi – Bác sĩ | Nestor: tôi – cậu, cô |
| Collin với Xiao | anh – ngài Thư ký | tôi – anh |
| Helene với Dean | chị – cậu, «anh cảnh sát» khi trêu | |
| Người trẻ với người lớn tuổi không có quan hệ riêng | cháu – cô, chú, bác + tên | |
| Người ngang tuổi không có quan hệ riêng | tôi – cậu, hoặc gọi tên | |

Hội thoại nhóm (`Group/`) dùng bảng này. Nếu không rõ ai nói với ai, đọc id: `Group/DIALOGROOM_<ngày>_<việc>_<nơi>_<lượt>_<NPC>_<số>`. Các dòng cùng `<ngày>_<việc>_<nơi>` là một cảnh.

### Ai nói với ai

- Người nói: phần trước `/` của id. Mọi câu dưới `MYER/` là Myer nói.
- Thoại hằng ngày, chào hỏi, quà, lời giận (`DAILY_DIALOG`, `GREETING_DIALOG`, `ANGRY_DIALOG`…): nói với nhân vật chính.
- Cảnh sự kiện (`EVENTDIALOG`): id của mỗi NPC đánh số riêng, nên không đọc được thứ tự lời từ id. Thứ tự đúng và ai có mặt nằm trong bundle `so-event-data`. `tools/audit_pronouns.py` đọc bundle này (xem `pipeline.md`).
- **Câu không chắc người nghe thì bỏ đại từ**, không đoán. Tiếng Việt cho phép câu không chủ ngữ: «Phải trang bị tốt hơn cho họ.» Câu hơi trung tính vẫn hơn gọi sai người.

### Cặp chốt khi dịch hội thoại NPC (#22)

Bổ sung cho bảng trên. Lô sau phải theo đúng để hai phía một cuộc nói chuyện khớp nhau.

| Người nói → người nghe | Cách xưng hô |
| --- | --- |
| Myer ↔ Osman | tôi – anh. «my friend» → «anh bạn» |
| Myer → Forrest | tôi – anh |
| Myer → Zeke | tôi – ông. Nói với Dược sư về Zeke: «bác Zeke» |
| Myer → Helene | tôi – cô |
| Myer → Matheo / Matheo → Myer | tôi – cậu / tôi – ông, «ông Myer», «Thị trưởng» |
| Myer → Reyner | tôi – cậu |
| Myer → Runeheart, Russo | chú – cháu |
| Myer → Nestor, Hội Y khoa | tôi – ông, «Bác sĩ», «quý vị» |
| Xiao → Myer | «ngài Myer»; nói về Myer: «ngài ấy» |
| Xiao → Opalheart, Moira | tôi – cô |
| Xiao → Helene, Yorn | tôi – chị Helene, anh Yorn |
| Xiao → Dev, Lucke, Victor | tôi – cậu |
| Matheo → Nestor | tôi – ông, «thưa Bác sĩ» |
| Matheo → Forrest | tôi – anh |
| Dean → Helene | em – chị |
| Helene → Derrek, Reyner | chị – cậu |
| Reyner → Helene | tôi – chị Helene |
| Helene → Yorn / Yorn → Helene | em – anh / tôi – cô |
| Helene ↔ Hannah | chị – em |
| Helene → Russo / Russo → Helene | chị – nhóc / em – cô Helene. Helene gắt «Cô á?! Nhóc tưởng chị là Nova hay sao?», nên Russo phải gọi «cô» |
| Reyner → Runeheart, Derrek, Dean, Dev, Bubble, Rue, Ottmar | tôi – cậu |
| Reyner, Runeheart → Leano, Opalheart, Nova, Myer | cháu – bác Leano, cô Opalheart, cô Nova, chú Myer |
| Runeheart → Reyner, Dev, Bubble | tôi – cậu |
| Opalheart → Xiao | cô – cậu, «boy» → «cậu nhóc» |
| Opalheart ↔ Nova | tôi – chị |
| Opalheart → Derrek / Derrek → Opalheart | cô – cháu, «kid» → «nhóc» / cháu – cô Opalheart |
| Leano → Runeheart | ta – cô nương («m'lady») |
| Leano → Myer, Reyner | ta – cậu |
| Rue → Leano / Leano → Rue | cháu – bác Leano / ta – nhóc |
| Lucke nói về Myer, Opalheart | «chú Myer», «cô Opalheart» |
| Mariele → Lucke / Lucke → Mariele | cô – cháu / cháu – cô |
| Osman → Dev | tôi – cậu |
| Bubble → Nova | cháu – cô |
| Socellia → Cassandra / Cassandra → Socellia | Sơ – chị / tôi – Sơ |
| Dean, Hannah → Zeke | cháu – bác Zeke |
| Victor ↔ Dev | tôi – cậu |
| Olive → Dev / Dev → Olive | chị – em / em – chị Olive |
| Victor → Hannah / Hannah → Victor | tôi – cậu / mình – cậu |
| Martha ↔ Hannah, Rue | mình – cậu |
| Nova ↔ Mariele, Mercy | tôi – chị |
| Reyner → Rue / Rue → Reyner | tôi – cậu / mình – cậu |
| Gọi người thứ ba | Martha: «anh Xiao», «anh Yorn». Rue: «anh Xiao», «chú Yorn». Bubble: «chú Yorn». Russo: «anh Victor». Olive: «anh Osman» |

NPC có thể hẹn hò (Reyner, Lucke, Matheo, Xiao, Runeheart, Helene, Leano) giữ đúng cặp với nhân vật chính sau khi tỏ tình: Helene «chị – cưng», Leano «ta – nhóc», còn lại «tôi – cậu».

Câu NPC hét viết in hoa thì giữ in hoa có dấu: «ĐỦ RỒI! CON KHÔNG CHỊU NỔI NỮA!».

### Cặp chốt khi dịch hội thoại NPC phần 2 (#23)

| Người nói → người nghe | Cách xưng hô |
| --- | --- |
| Forrest → Osman, Myer | tôi – anh / tôi, «thưa Thị trưởng» |
| Forrest → Lucke, Matheo, Dan | tôi – cậu |
| Forrest → Russo | chú – nhóc. Forrest thường xưng «tôi», nhưng nói với trẻ con mà xưng «tôi» thì cứng |
| Zeke → Myer | tôi – cậu, «my friend» → «anh bạn» |
| Zeke → Laura | bác – cháu, «my dear» → «cháu yêu» |
| Mariele → Olive | chị – em |
| Mariele → Derrek / Derrek → Mariele | cô – cháu / tôi – cô, «ma'am» → «thưa cô» khi đang làm việc |
| Rue → Lucke | mình – cậu |
| Dean, Derrek → Cassandra | em – chị Cassandra |
| Derrek → Helene | tôi – chị. Nói về Helene với Dược sư: «chị ta» |
| Derrek → Reyner | tôi – cậu, «brother» → «người anh em» |
| Dean → Russo | anh – em |
| Dean → Yorn | tôi – anh |
| Dean → Martha | tớ – cậu |
| Cassandra → Runeheart | chị – em |
| Olive → Ottmar | chị – cậu |
| Olive → Martha / Martha → Olive | chị – em / em – chị Olive |
| Olive → Mariele | tôi – chị Mariele |
| Martha → Laura | chị – em |
| Martha → Osman | cháu – Cảnh sát trưởng |
| Martha nói với khách khi không rõ là ai | «quý khách» |
| Yorn → Dean | tôi – cậu |
| Nova → Olive | tôi – cô |
| Nova → Bubble, đội kiểm lâm | tôi – cháu, «các cháu» |
| Nova → Socellia / Socellia → Nova | tôi – Sơ / Sơ – chị Nova |
| Nova nói với người chồng đã mất | em – anh, mở đầu «chồng yêu ơi» để người chơi không tưởng Nova gọi mình |
| Hannah → Nova | em – chị Nova |
| Hannah nói về Mariele | «cô Mariele» |
| Russo → Myer | cháu – chú Thị trưởng, chú Myer |
| Russo → Dean, Victor | em – anh Dean, anh Victor |
| Victor → Laura, Russo | anh – các em |
| Laura → Victor | em – anh |
| Laura, Hannah → Zeke | cháu – bác Zeke |
| Garret, Mercy nói về nhau với Dược sư | «bà nhà bác», «ông Garret nhà bác» |
| Nestor → Myer | tôi – ông, «thưa Thị trưởng» |
| Nestor → Matheo | tôi – cậu |
| Moira → Myer | tôi – ông |
| Collin → Yorn | tôi – anh, «Grizzly Guy» → «Anh Gấu Xám» |
| Collin nói về Ottmar | «Cậu Ngô» («Corn Boy») |
| Socellia → các vị thần | con – các ngài |
| Dan → mọi người | ta – nhà ngươi, «crewmate» → «thuyền viên của ta» |
| Dev → Nova, Myer | cháu – cô Nova, chú Myer |
| Dev → Reyner, Runeheart | tôi – cậu |
| Victor → Socellia | tôi – Sơ, «Vâng, thưa Sơ» |
| Victor → Lucke | tôi – cậu |
| Victor → Caenus, Amadeus | tôi – cậu, «Amadeus thân mến» |
| Ottmar → mọi người | luôn gọi tên, không dùng đại từ |

Nestor không gọi Dược sư bằng đại từ ngôi hai: chỉ dùng «Dược sư», tên, hoặc bỏ chủ ngữ.

## Con chó và con mèo

- Con chó của nhân vật chính là đực («he»). Tên là `{[DOG_NAME]}`.
- NPC gọi chó bằng tên hoặc «nó». Hướng dẫn gọi «chú chó của bạn». «chú chó» ở đây là cách nói về chó, không phải xưng hô.
- Khi nói với chó: «Ngoan lắm!», «Giỏi quá!». Không dùng «good boy» dịch sát.
- Kipps là mèo cái. Zeke gọi «cưng», «bé ngoan». «Who's a good girl?» → «Bé ngoan của bác đâu nào?»

## Giọng chung

- Ấm áp, nhẹ nhàng, gần gũi. Người dân nói như hàng xóm.
- Tiếng Việt tự nhiên. Đổi trật tự câu cho xuôi, không bám từng chữ tiếng Anh.
- Tránh khẩu ngữ chat và tiếng lóng mạng: «ok nha», «j», «ko», «hông», «nhaaa».
- Tránh từ địa phương quá đậm. Dùng «bố, mẹ», không dùng «ba, má» hay «tía, u».
- Dùng tiểu từ cuối câu cho có tình: «nhé», «nhỉ», «à», «đấy», «mà». Không lạm dụng.
- Giữ tiếng cười và thán từ cho hợp tiếng Việt: «Hahaha», «Hehehe», «Hừ», «Ối», «Trời ơi», «Ồ».
- Lời lắp bắp giữ dạng lặp chữ đầu. Ở đầu câu, chữ sau gạch cũng viết hoa: «T-Thank you» → «C-Cảm ơn», «K-Không...». Thán từ có gạch không phải lắp bắp thì để thường: «A-men», «Yo-ho-ho», «Ơ-ờ».

## Quy tắc câu

- Nút, nhãn, tiêu đề: cụm ngắn, không chấm cuối. Ví dụ «Cài đặt», «Tặng quà», «Đã mở khóa vạc».
- Hội thoại: câu đủ, có chấm câu đầy đủ như bản gốc.
- Hướng dẫn và mô tả nhiệm vụ: ngôi thứ hai «bạn» trong hướng dẫn, ngôi thứ ba bằng tên trong nhiệm vụ. Câu ngắn, rõ.
- Câu hỏi xác nhận: «Bạn có muốn…?» hoặc ngắn hơn: «Đi ngủ?», «Bắt đầu pha chế?».
- Giữ độ dài gần câu Anh. Nhãn và nút dễ tràn khung.
- Dấu ba chấm giữ đúng kiểu bản gốc (`...` hoặc `…`).

## Viết hoa

- Chỉ viết hoa chữ đầu câu và tên riêng. Không viết hoa từng chữ kiểu tiếng Anh.
- Địa danh: phần chung viết hoa chữ đầu. Ví dụ «Phòng khám Moonbury», «Nhà tắm Willow Waters», «Thảo nguyên Meadow».
- Nơi cụ thể trong game viết hoa như tên riêng kể cả khi đứng một mình: «Phòng khám», «Nhà pha chế», «Tòa thị chính», «Đồn cảnh sát», «Nhà thờ», «Thủ đô».
- Tổ chức: «Hội Y khoa».
- «Dược sư» viết hoa khi là danh xưng của nhân vật chính, viết thường khi nói về nghề.
- Tên vật phẩm, thuốc, nhiệm vụ: viết hoa chữ đầu, còn lại thường, trừ tên riêng.
- Tên loài quái viết hoa mỗi tiếng (xem `thuat-ngu.md`).
- Thứ trong tuần viết hoa: «Thứ Hai» … «Chủ Nhật».

## Dấu câu

- Dấu ngoặc kép trong câu dịch dùng «». Ví dụ tấm chăn thêu chữ «Russo».
- Không để dấu cách trước dấu phẩy, dấu chấm, dấu hỏi, dấu chấm than.
- Giữ dấu chấm than và chấm hỏi như bản gốc. Không thêm.
- Giữ nguyên xuống dòng trong ô. Có thể dời vị trí xuống dòng cho câu Việt xuôi, nhưng giữ số dòng.
- Giờ dùng `07:00`, không đổi thành «7 giờ sáng».
- Số có dấu phân cách hàng nghìn viết kiểu Việt: «1,000» → «1.000». Số trong placeholder (`{0}`) để game điền, không đổi.

## Lỗi hay gặp

Rút ra từ lượt rà soát toàn bộ bản dịch (#29). Script `tools/check_vietnamese.py` không bắt được các lỗi này, phải đọc mới thấy.

- **«we» không gồm người nghe** thì không dịch «chúng ta». Myer kể việc thị trấn đã làm: «Mọi người vừa sửa xong cây cầu», «Bọn chú vừa dọn sạch bãi biển», không phải «Chúng ta vừa…». «Không có cháu thì cả thị trấn chẳng làm nổi đâu.»
- **Dịch sát cấu trúc tiếng Anh.** Viết lại theo cách người Việt nói:

  | Gốc | Tránh | Nên |
  | --- | --- | --- |
  | How's your day? | Hôm nay của cậu thế nào? | Hôm nay cậu thế nào? |
  | I'm glad we talked | Mình vui vì tụi mình đã trò chuyện | Mình vui vì được tâm sự với cậu |
  | Forgive me for… | Tha thứ cho mình vì đã… | Mình … quá, cậu tha thứ cho mình nhé? |
  | The feeling is mutual | Tình cảm này đến từ cả hai phía | Mình cũng có tình cảm với cậu |
  | Only to find… | Chỉ để thấy… | Nào ngờ… |
  | It's here | Nó ở đây | Ở đây ạ |
  | Noted. | Ghi nhớ. | Nhớ rồi. |
  | long face | mặt dài thượt | mặt mày ủ rũ |
  | Accept this from me | Nhận cái này từ tôi | Nhận cái này của tôi |
  | Let me guess | Đoán xem nào | Khỏi nói cũng biết |

- **Câu bị động** («cannot be seen») đảo lại cho đúng chủ thể: «Mắt thường không thể nhìn thấy họ», không phải «Họ không thể nhìn thấy».
- **«giúp» thiếu bổ ngữ** dễ hiểu ngược: «Em cần mọi người giúp», «Tôi cần nhờ một việc», «ngỏ ý giúp Sơ», không phải «Em cần giúp», «xin giúp Sơ».
- **Lặp từ:** «cháu… cháu à» trong một câu ngắn (bỏ «cháu à» khi câu đã có «cháu»), «Được rồi. Thế là được.», «mai… Mai…», «thế nào nào».
- **Vừa gọi danh xưng vừa gọi tên** trong một câu («Dược sư…, {[CHARACTER_NAME]}?»): giữ một.
- **Bỏ chủ ngữ mà vế sau đổi người** thì nhắc tên: «Dược sư càng thân với người bạn này thì nó sẽ càng khôn.»
- **Tiểu từ:** «ạ» là người dưới nói với người trên; Myer nói với Dược sư dùng «à». Không chồng hai tiểu từ («chứ, nhỉ?»).
- **Tiếng Anh còn sót:** «Yay!», «Yeah!» → «Hoan hô!», «Tuyệt quá!», «Ha!».
- **Từ dễ dùng sai nghĩa:** «thành thật» (trung thực) khác «thành hiện thực»; «gỡ lại» (gỡ vốn) khác «khắc phục»; «nửa kia» là người yêu; «người khó khăn» thành «người gặp khó khăn»; «người rất lý tưởng» (hoàn hảo) khác «sống có lý tưởng»; «khét tiếng» là tai tiếng.

## Trạng thái dòng

- `todo`: chưa dịch.
- `draft`: dịch máy hoặc dịch nháp, chưa đọc lại.
- `review`: đã đọc lại theo `thuat-ngu.md` và bảng xưng hô, còn chờ chơi thử trong game.
- `done`: đã thấy trên màn hình, không tràn khung, không vỡ placeholder hay thẻ màu.

Dòng có `id` bắt đầu bằng `EXAMPLE` là mẫu định dạng. Xóa trước khi dịch thật.
