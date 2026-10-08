# Thuật ngữ

Bảng này chỉ dùng cho Potion Permit. Không lấy quy ước của game khác.

Nguồn dịch là tiếng Anh (bản Anh-Anh: `Colour`, `Centre`, `GF`/`1F`).

## Không đổi trong câu dịch

- `{[CHARACTER_NAME]}`: tên nhân vật chính, người chơi tự đặt.
- `{[DOG_NAME]}`: tên con chó, người chơi tự đặt. Tên mặc định trong mã là Noxe.
- `{[BODY_PART]}`, `{[SYMPTOM]}`: game chèn chữ thường từ nhóm `BodyPart/` và `Symptom/`. Không đặt hai placeholder này ở đầu câu, vì chữ đầu câu sẽ không được viết hoa.
- `{0}`, `{1}`: số hoặc tên do game chèn.
- Thẻ màu: `<#54ba6a>…</color>`, `<#A27DDE>…</color>`, `<#a27dde>…</color>`, `<#ff1d1d>…</color>`. Giữ nguyên mã màu, chỉ dịch chữ bên trong.
- Xuống dòng thật trong ô CSV. Giữ số dòng gần với bản gốc.
- Giờ `07:00`, `17:00` và con số giữ nguyên.

## Tên giữ nguyên

### Nhân vật

Bubble, Cassandra, Collin, Dan, Dean, Derrek, Dev, Forrest, Garret, Hannah, Helene, Kipps, Laura, Leano, Lucke, Mariele, Martha, Matheo, Mercy, Moira, Myer, Nestor, Nova, Olive, Opalheart, Osman, Ottmar, Reyner, Rue, Runeheart, Russo, Socellia, Victor, Xiao, Yorn, Zeke.

Tên phụ: Caenus, Amadeus (bạn vô hình của Victor), Noxe (tên chó mặc định).

Chức danh đi trước tên được dịch:

| Gốc | Dịch |
| --- | --- |
| Mayor Myer | Thị trưởng Myer |
| Dr Nestor, Doctor, Doc | Bác sĩ Nestor, Bác sĩ |
| Sister Socellia, Sister | Sơ Socellia, Sơ |
| Sir Osman, Sir (cấp dưới gọi Osman) | sếp Osman, sếp |
| Captain Dan | Thuyền trưởng Dan |
| Mr Secretary (Collin trêu Xiao) | ngài Thư ký |
| Mrs. Cassandra | chị Cassandra |
| Officer (gọi cảnh sát) | anh cảnh sát |

### Địa danh và tổ chức

| Gốc | Dịch | Ghi chú |
| --- | --- | --- |
| Moonbury | Moonbury | |
| Moonbury Town | Thị trấn Moonbury | |
| Moonbury Island | Đảo Moonbury | |
| Medical Association | Hội Y khoa | «the Association» → «Hội» |
| Hearts and Sparks | Hearts and Sparks | Tên tiệm rèn và tên bài thử của Opalheart |
| Bulk and Build | Bulk and Build | Tên xưởng mộc |
| Primerose Sail | Primerose Sail | Tên tiệm câu cá |
| Seventh Island | Đảo Thứ Bảy | Tên vật phẩm nhiệm vụ |
| the capital | Thủ đô | Viết hoa vì là một nơi cụ thể |
| Koblin | Koblin | Tộc quái, giữ nguyên |
| Mythril | Mythril | Kim loại hư cấu |

## Dịch thống nhất

### Nghề và vai trò

| Gốc | Dịch | Ghi chú |
| --- | --- | --- |
| Chemist (nhân vật chính) | Dược sư | Viết hoa khi dùng làm danh xưng hoặc chỉ nhân vật chính: «Chào Dược sư!» |
| chemist (nghề nói chung) | dược sư | «các dược sư bị đuổi khỏi Moonbury» |
| chemist apprentice | dược sư tập sự | |
| witch doctor | thầy lang | Nghề của Matheo |
| mayor | thị trưởng | |
| treasurer | thủ quỹ | Xiao |
| ranger, the rangers | kiểm lâm, đội kiểm lâm | |
| Head Ranger | Trưởng kiểm lâm | Forrest |
| assistant ranger | kiểm lâm phụ tá | Bubble |
| Chief of Police | Cảnh sát trưởng | Osman |
| police officer | cảnh sát | |
| blacksmith | thợ rèn | |
| carpenter, woodworker | thợ mộc | |
| tailor | thợ may | |
| postman | người đưa thư | |
| vicar | nữ tu coi nhà thờ | Socellia. Trong thoại gọi là «Sơ» |
| graveyard keeper | người giữ nghĩa trang | Victor |
| villagers, residents, townsfolk | người dân, cư dân | Không dùng «dân làng» vì Moonbury là thị trấn |
| tutor | gia sư | |

### Chữa bệnh

| Gốc | Dịch | Ghi chú |
| --- | --- | --- |
| Clinic | Phòng khám | Viết hoa vì là nơi cụ thể. «Moonbury Clinic» → «Phòng khám Moonbury» |
| patient | bệnh nhân | |
| diagnose, diagnosis | chẩn đoán | |
| Diagnosis Mini-Game | Trò chơi chẩn đoán | |
| symptom | triệu chứng | |
| unidentified symptom | triệu chứng chưa rõ | |
| treat, treatment | chữa, điều trị | |
| Treatment Completed | Đã điều trị xong | |
| Treatment Failure | Điều trị thất bại | |
| cure, cured | chữa khỏi, đã khỏi | |
| disease, sickness, illness | bệnh | |
| fall ill, sick | đổ bệnh, bị ốm | «{0} is currently sick» → «{0} đang ốm» |
| Complaints (lời bệnh nhân kể) | Lời kể bệnh | Xem mục phân vân |
| complaint (không hài lòng) | phàn nàn | Dòng `DIAGNOSE_COMPLETE_COMPLAINT` |
| Satisfaction | Mức hài lòng | |
| bed (ở Phòng khám) | giường bệnh | |
| medical journal | sổ tay y khoa | |
| chemistry test, test | kỳ thi dược sư, bài thi | |
| licence | giấy phép | |
| promotion | thăng hạng | |
| letter of recommendation | thư giới thiệu | |

### Pha chế

| Gốc | Dịch | Ghi chú |
| --- | --- | --- |
| potion | thuốc | Danh mục UI «Potions» → «Thuốc». Khi cần chỉ vật: «lọ thuốc» |
| brew, brewing | pha chế | «Start brewing?» → «Bắt đầu pha chế?» |
| Potion Brewing | Pha chế thuốc | |
| cauldron | vạc | «Cauldron Unlocked» → «Đã mở khóa vạc» |
| recipe | công thức | |
| ingredient | nguyên liệu | |
| material | nguyên liệu | Danh mục UI «Material» → «Nguyên liệu» |
| resources (đi hái lượm) | tài nguyên | «Not enough resources!» là thiếu tiền: dịch «Không đủ tiền!» |
| Permitted Ingredients | Nguyên liệu được dùng | |
| serum | huyết thanh | Basic / Intermediate / Advanced → sơ cấp / trung cấp / cao cấp |
| ointment, balm | thuốc mỡ, cao | |
| tonic | thuốc bổ | |
| elixir | tiên dược | «Sun Elixir» → «Tiên dược Mặt Trời» |
| concoction | hỗn dược | |
| research | nghiên cứu | |
| Fire, Water, Wind, Earth | Lửa, Nước, Gió, Đất | Bốn nguyên tố |
| Post Drop Box | Hộp ký gửi | Hộp bán thuốc qua bưu điện |
| post bird, courier | chim đưa thư | |
| Delivery Box | Hộp giao hàng | Hộp nộp nguyên liệu cho yêu cầu |
| Grow Box | Bồn trồng cây | |

### Xã hội

| Gốc | Dịch | Ghi chú |
| --- | --- | --- |
| Trust | Uy tín | Thanh uy tín của Dược sư trong thị trấn (`UI_REPUTATION_*`). «Trust Up / Down» → «Uy tín tăng / giảm» |
| insufficient trust level | uy tín chưa đủ | |
| thumbs down (biểu tượng) | ngón cái chúc xuống | |
| friendship | tình bạn | Trong văn kể |
| friendship level, friendship bar | mức thân thiết, thanh thân thiết | Trong hệ thống |
| Friendship Level Up | Thân thiết hơn rồi! | Nhãn ngắn, có thể bỏ dấu chấm than nếu chật |
| friendship event | sự kiện thân thiết | |
| Social | Giao lưu | Tab trong sổ |
| Gift | Tặng quà | Nút. Danh từ: «quà» |
| Talk | Trò chuyện | |
| Date, Dating | Hẹn hò | |
| Dating Unlocked | Đã mở khóa hẹn hò | |
| Confess | Tỏ tình | |
| romance path | tuyến tình cảm | |
| Romanceable | Có thể hẹn hò | |
| Moon Cloves | Đinh hương Trăng | Món quà mở khóa tặng quà. Xem mục phân vân |
| Moon Brooch | Trâm cài Trăng | Món dùng để tỏ tình. Xem mục phân vân |
| Background Story | Tiểu sử | |
| Character Image Unlocked | Đã mở khóa ảnh nhân vật | |

### Nhiệm vụ và bảng tin

| Gốc | Dịch | Ghi chú |
| --- | --- | --- |
| quest, task | nhiệm vụ | Tab «Task» → «Nhiệm vụ» |
| request, community request | yêu cầu | Việc người dân nhờ trên bảng |
| Community Board, Quest Board | Bảng yêu cầu | Hai tên cùng chỉ một bảng trước Tòa thị chính |
| Bulletin Board | Bảng tin | Bảng báo sự kiện thân thiết và tin tức |
| Pin Quest, Pinned | Ghim nhiệm vụ, Đã ghim | |
| Available, Taken, Report | Còn trống, Đã nhận, Báo cáo | |
| Quest Completed | Hoàn thành nhiệm vụ | |
| Rewards | Phần thưởng | |
| Requirements | Yêu cầu | |
| {0} Day(s) Left | Còn {0} ngày | |
| Approval Badge | Huy hiệu Công nhận | «Approval Badge 1» → «Huy hiệu Công nhận 1» |
| Badge | Huy hiệu | |
| part-time work | việc làm thêm | |
| Community Growth | Thị trấn đổi mới | Tên mục hướng dẫn |

### Đồ dùng, cơ thể người chơi, di chuyển

| Gốc | Dịch | Gốc | Dịch |
| --- | --- | --- | --- |
| sickle | liềm | Health | Sinh lực |
| axe | rìu | Stamina | Thể lực |
| hammer | búa | Passed Out | Ngất xỉu |
| pickaxe | cuốc chim | Journal | Sổ tay |
| fishing rod | cần câu | Inventory | Túi đồ |
| bait | mồi câu | World Map | Bản đồ thế giới |
| Reel In | Kéo cần | Travel Point | Điểm dịch chuyển |
| Cast | Quăng cần | Teleport, fast travel | Dịch chuyển |
| Whistle | Huýt sáo | Roll | Lăn |
| Iron, Steel | Sắt, Thép | Room Editor | Trang trí phòng |
| Basic / Intermediate / Advanced (cần câu) | Cơ bản / Trung cấp / Cao cấp | Furniture | Đồ nội thất |

### Con chó

| Gốc | Dịch |
| --- | --- |
| Dog: Tracking Ability | Chó: Khả năng lần dấu |
| Dog: Digging Ability | Chó: Khả năng đào bới |
| Pet, Feed, Find | Vuốt ve, Cho ăn, Tìm người |
| Person To Find | Người cần tìm |
| {[DOG_NAME]}'s House | Nhà của {[DOG_NAME]} |

## Địa danh (`Location/`, `Trigger/`, biển hiệu)

Phần chung viết hoa chữ đầu, phần tên riêng giữ nguyên.

Tầng theo kiểu Anh: `GF` là tầng trệt, `1F` là tầng trên. Dịch `GF` → «Tầng 1», `1F` → «Tầng 2».

| Gốc | Dịch |
| --- | --- |
| Willow Waters Bathhouse, Bathhouse | Nhà tắm Willow Waters, Nhà tắm |
| Hearts and Sparks Shop | Tiệm rèn Hearts and Sparks |
| Bulk and Build | Bulk and Build |
| Bulk and Build - GF / - 1F | Bulk and Build - Tầng 1 / - Tầng 2 |
| Silky Stitch Tailor's, Tailor Shop | Tiệm may Silky Stitch, Tiệm may |
| Arcade Centre | Khu trò chơi |
| Lazy Bowl Tavern, Tavern | Quán rượu Lazy Bowl, Quán rượu |
| Farmhouse | Trang trại |
| Primerose Sail | Primerose Sail |
| Church | Nhà thờ |
| Ottmar's Cafe | Quán cà phê Ottmar |
| Ranger Post | Trạm Kiểm lâm |
| Bulletin Board | Bảng tin |
| Coach House | Trạm xe ngựa |
| Town Hall | Tòa thị chính |
| Monastery | Tu viện |
| Police Department | Đồn cảnh sát |
| Post Office | Bưu điện |
| Clinic | Phòng khám |
| Potion House | Nhà pha chế |
| X's House | Nhà X («Osman's House» → «Nhà Osman») |
| House | Nhà dân |
| Zeke's Tent | Lều của Zeke |
| Meadow Range | Thảo nguyên Meadow |
| Glaze Iceberg | Núi băng Glaze |
| Barren Wasteland | Hoang mạc Barren |
| Glaze Grotto | Hang Glaze |
| Barren Chasm | Vực Barren |
| Ire Landslide | Vùng sạt lở Ire |
| Snow Cable Car | Cáp treo Núi tuyết |
| Geyser Reactor | Trạm Mạch nước nóng |
| Moonbury Town Square | Quảng trường Moonbury |
| Moonbury Beach | Bãi biển Moonbury |
| Moonbury Cliff | Vách đá Moonbury |
| Moonbury Park | Công viên Moonbury |
| Moonbury Train Station | Ga tàu Moonbury |
| Park / River / Beach Fishing Spot | Điểm câu Công viên / Sông / Bãi biển |
| Glaze Grotto Fishing Spot | Điểm câu Hang Glaze |
| West / South / North of X | Phía tây / Phía nam / Phía bắc X |
| North-east / South-east / South-west of X | Phía đông bắc / đông nam / tây nam X |
| Heart of X | Trung tâm X |
| X Entrance | Lối vào X |
| East: Meadow Range (biển chỉ đường) | Hướng đông: Thảo nguyên Meadow |

## Bộ phận cơ thể (`BodyPart/`)

Viết thường. Game chèn vào giữa câu qua `{[BODY_PART]}`.

| Gốc | Dịch | Gốc | Dịch |
| --- | --- | --- | --- |
| left eye | mắt trái | right eye | mắt phải |
| mouth | miệng | neck | cổ |
| lower chest | ngực dưới | upper chest | ngực trên |
| left upper stomach | bụng trên bên trái | right upper stomach | bụng trên bên phải |
| lower stomach | bụng dưới | | |
| left shoulder | vai trái | right shoulder | vai phải |
| left upper arm | bắp tay trái | right upper arm | bắp tay phải |
| lower left arm | cẳng tay trái | lower right arm | cẳng tay phải |
| left palm | lòng bàn tay trái | right palm | lòng bàn tay phải |
| left thigh | đùi trái | right thigh | đùi phải |
| left knee | đầu gối trái | right knee | đầu gối phải |
| left ankle | mắt cá chân trái | right ankle | mắt cá chân phải |
| left foot | bàn chân trái | right foot | bàn chân phải |

## Triệu chứng (`Symptom/`)

Viết thường, trừ tên bệnh hư cấu. Game chèn qua `{[SYMPTOM]}`.

| Gốc | Dịch | Gốc | Dịch |
| --- | --- | --- | --- |
| blisters | phồng rộp | lumps | nổi cục |
| bloating | chướng | Moonwarts | Mụn cóc Trăng |
| blurred vision | mờ mắt | numbness | tê bì |
| bruises | bầm tím | oxygen depravation | thiếu oxy |
| burning | nóng rát | rashes | phát ban |
| clammy patches | mảng da ẩm lạnh | stiffness | co cứng |
| cramps | chuột rút | swelling | sưng |
| dryness | khô rát | tingling | râm ran |
| high heart rate | tim đập nhanh | wobbliness | run rẩy |
| inflammation | viêm | Sunworm | Giun Mặt Trời |
| itchiness | ngứa | low heart rate | tim đập chậm |

Câu mẫu `Complaint/` dùng chung cho mọi bệnh nhân, kể cả trẻ con. Bỏ chủ ngữ hoặc dùng cách nói không cần đại từ. Ví dụ:

- `There is something wrong with my {[BODY_PART]}.` → «Hình như {[BODY_PART]} có vấn đề.»
- `I can feel a strange {[SYMPTOM]} in my {[BODY_PART]}.` → «Thấy {[BODY_PART]} bị {[SYMPTOM]} lạ lắm.»

## Quái (`Monster/`)

Dịch nghĩa thành tên ngắn. Tên viết hoa chữ đầu mỗi tiếng vì là tên loài. Tên vật phẩm làm từ quái dùng lại tên này, ví dụ «Ironfin Pickaxe» → «Cuốc Vây Sắt».

| Gốc | Dịch | Gốc | Dịch |
| --- | --- | --- | --- |
| Greedbonnet | Nấm Tham Ăn | Bomber Bee | Ong Ném Bom |
| Green Blob | Nhầy Xanh | Elder Wolf | Sói Cổ Xưa |
| Mini Green Blob | Nhầy Xanh Nhí | Koblin Assassin | Sát Thủ Koblin |
| Honeypaw | Gấu Mật | Sandcrawl | Bọ Cát |
| Crownmite | Bọ Vương Miện | Grandhorn | Bò Sừng Lớn |
| Pangol | Tê Tê Lăn | Sunclaw | Cua Càng Lửa |
| Bonemask | Mặt Nạ Xương | Koblin Mage | Pháp Sư Koblin |
| Blackpaw | Gấu Vuốt Đen | Koblin General | Tướng Koblin |
| Goldenhorn | Bọ Sừng Vàng | Ironfin | Vây Sắt |
| Spook Digger | Chuột Chũi Ma | Blossom Shooter | Hoa Bắn Hạt |

## Nâng cấp (`Upgrade/`, `UI_FEATURE_UNLOCK_*`)

| Gốc | Dịch |
| --- | --- |
| Kitchen Renovation | Sửa sang nhà bếp |
| House Expansion 1 | Mở rộng nhà 1 |
| Clinic Renovation 1 | Cải tạo Phòng khám 1 |
| Cauldron Upgrade 1 | Nâng cấp vạc 1 |
| Iron / Steel / Mythril Sickle | Liềm sắt / Liềm thép / Liềm Mythril |
| Iron / Steel / Mythril Axe | Rìu sắt / Rìu thép / Rìu Mythril |
| Iron / Steel / Mythril Hammer | Búa sắt / Búa thép / Búa Mythril |
| Health Expand | Tăng sinh lực |
| Stamina Expand | Tăng thể lực |
| Post Drop Box Upgrade 1 | Nâng cấp hộp ký gửi 1 |
| Grow Box Repair | Sửa bồn trồng cây |
| Blacksmith Upgrade 1 | Nâng cấp lò rèn 1 |
| Carpenter Upgrade 1 | Nâng cấp xưởng mộc 1 |
| X Unlocked | Đã mở khóa X |
| X Acquired | Đã nhận X |
| X Completed | Đã hoàn thành X |
| Max level reached | Đã đạt cấp tối đa |

## Nút và chú thích phím (`Legend/`, `Interaction/`)

| Gốc | Dịch | Gốc | Dịch |
| --- | --- | --- | --- |
| Select | Chọn | Back | Quay lại |
| Delete | Xóa | Hold to delete | Giữ để xóa |
| Random | Ngẫu nhiên | Change Page | Đổi trang |
| Change Page L / R | Trang trước / Trang sau | Place | Đặt |
| Cancel | Hủy | Move | Di chuyển |
| Buy | Mua | Set Quantity | Chọn số lượng |
| Upgrade | Nâng cấp | Cook | Nấu ăn |
| Confirm | Xác nhận | Change Settings | Đổi cài đặt |
| Eat | Ăn | Read | Đọc |
| Yes / No / OK | Có / Không / OK | Pin Quest | Ghim nhiệm vụ |
| Teleport | Dịch chuyển | Feed | Cho ăn |
| Recipe | Công thức | Edit | Sửa |
| Reel In | Kéo cần | Cast | Quăng cần |
| Roll | Lăn | Repair | Sửa |
| Change Button | Đổi phím | Change Target | Đổi mục tiêu |
| Change Quest | Đổi nhiệm vụ | Left Tab / Right Tab | Tab trái / Tab phải |
| Action 1 | Hành động 1 | Movement Type 1 | Kiểu di chuyển 1 |
| Play | Chơi | Plant | Trồng |
| Harvest | Thu hoạch | Skip | Bỏ qua |
| Sleep | Ngủ | Sit | Ngồi |
| Shop | Mua sắm | Open / Close | Mở / Đóng |
| Craft | Chế tạo | Fish | Câu cá |
| Collect | Thu nhặt | Decorate | Trang trí |
| Activate | Kích hoạt | Check | Xem |
| Research | Nghiên cứu | Report | Báo cáo |

## Tên vật phẩm

- Viết hoa chữ đầu, còn lại thường, trừ tên riêng và chữ «Trăng», «Mặt Trời» khi là phần tên. Ví dụ «Thuốc mỡ tiêu», «Giấy phép», «Đồng hồ bỏ túi».
- Cây có tên Việt quen thì dùng tên Việt: Basil → húng quế, Jasmine → hoa nhài, Lavender → oải hương, Daisy → cúc dại, Marigold → cúc vạn thọ, Sunflower → hướng dương, Ginger → gừng, Garlic → tỏi, Ginseng → nhân sâm, Konjac → khoai nưa.
- Tên bịa thì dịch nghĩa: Rainbow Dew → Sương cầu vồng, Cold Bloom → Hoa băng, Black Lotus → Sen đen.
- Tên thần thoại giữ nguyên: Yggdrasil, Lacrima.
- Đơn vị `lbs` trong sổ cá: giữ «lbs» vì game không đổi số.

## Còn phân vân

Ghi lại để chốt khi chơi thử. Đổi thì sửa bảng trên trước, rồi sửa CSV.

- `Trust`: đã chốt «Uy tín» (#19), vì thanh này là danh tiếng của Dược sư trong thị trấn.
- `Complaints:` trong màn hình bệnh nhân: tạm dịch «Lời kể bệnh:». Cần xem trên màn hình là danh sách triệu chứng bệnh nhân kể hay là lời phàn nàn.
- `Community Board` và `Bulletin Board`: tạm tách thành «Bảng yêu cầu» và «Bảng tin». Cần xác nhận trong game là hai bảng khác nhau.
- `Moon Cloves`, `Moon Brooch`, `Moonite`: «Đinh hương Trăng», «Trâm cài Trăng», tạm để «Moonite». Có thể chọn «Nguyệt…» cho cả nhóm.
- Tên vùng (`Meadow Range`, `Glaze Iceberg`, `Barren Wasteland`): đang giữ chữ tiếng Anh làm tên riêng. Có thể dịch hẳn («Đồng cỏ xanh», «Núi băng», «Hoang mạc cằn») nếu thấy câu Việt lẫn chữ Anh quá nhiều.
- `Geyser Reactor`: «Trạm Mạch nước nóng». Cần xem cảnh trong game.
- Tên quái: đang dịch nghĩa. Nếu tên quá dài trong khung sổ tay, giữ tên gốc.
