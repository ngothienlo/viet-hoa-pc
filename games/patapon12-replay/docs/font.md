# Font

Tài liệu này ghi font nào trong PATAPON 1+2 REPLAY vẽ chữ gì, và vá thế nào để chữ Việt hiện đủ, cùng một mặt chữ. Cách làm chung cho game Unity dùng TextMesh Pro nằm ở `docs/technical/unity-tmp-font.md`.

Không cần quét lại game để biết font. Danh sách đầy đủ nằm trong `tools/font/fonts.json`.

## Hai lỗi đã gặp

Issue #9. Ảnh chụp trong game sau bản vá #8:

1. **Một câu lẫn hai font.** Lời thoại hiện bằng font kiểu Patapon (DF-KakuPop-W5). Font này chỉ có ASCII và kana. Chữ có dấu rơi xuống font dự phòng có nét sans mảnh, nên «Người» vừa có nét Patapon vừa có nét sans.
2. **Ô vuông.** `ẳ` trong «Chẳng» không có trong cả chuỗi dự phòng, nên hiện thành `□`.

Bản vá #8 chỉ thay TShinGo và TTake trong `sharedassets`. KakuPop và các font nằm trong bundle chưa được đụng tới.

## Bản đồ font

`inventory.py` quét `sharedassets*`, `resources.assets`, `level*` và 84 bundle Addressables. Lần quét ngày 2026-10-07 tìm được 109 TMP Font Asset. Đa số là font Nhật, Hàn, Trung, giữ nguyên.

Font cần vá:

| Font | Nằm ở | Cách vá |
| --- | --- | --- |
| `TTakeStd-Bold SDF` | `sharedassets5` | Thay bằng Be Vietnam Pro Bold |
| `TTakeStd-Bold_hcs` | `sharedassets0`, bundle `91aca73a` | Thay bằng Be Vietnam Pro Bold |
| `TShinGoPr6-Medium SDF` | `sharedassets1` | Thay bằng Be Vietnam Pro Regular |
| `TShinGoPr6-Medium SDF_mission`, `_launcher_hcs`, `_savewindow` | `sharedassets0` | Thay bằng Be Vietnam Pro Regular |
| `TShinGoPr6-Regular SDF` | bundle `88a48bd1`, `91aca73a` | Thay bằng Be Vietnam Pro Regular |
| `TShinGoPr6-Medium_hcs`, `TShinGoPr6-Regular_hcs` | bundle `91aca73a` | Thay bằng Be Vietnam Pro Regular |
| `DF-KakuPop-W5 SDF_Padding14_Take` | `sharedassets1` | Ghép dấu, giữ nét KakuPop |
| `DF-KakuPop-W5_hcs`, `DF-KakuPop-W5_name` | bundle `91aca73a` | Ghép dấu |
| `DF-KakuPop-W5_hcs_sc`, `_name_sc` | bundle `f7cd5c4c` (bản Trung giản thể) | Ghép dấu |
| `DF-KakuPop-W5_hcs_tc` | bundle `064a729a` (bản Trung phồn thể) | Ghép dấu |
| `LondrinaSolid_hcs` | bundle `91aca73a`, prefab tips tiếng Anh dùng | Ghép dấu |

Font giữ nguyên, kèm lý do:

- Font Nhật, Hàn, Trung (`_ja`, `_kr`, NotoSansKR, GothicA1, PoorStory, DFPGB, DFT, DFGB…).
- Font chỉ có chữ toàn khổ (`_fs`), chỉ có số hay ký hiệu (`_number`, `_symbol`, `_onpu`), hoặc chỉ có vài ký tự.
- `TTakeStd-Bold_staffroll`: chữ chạy cuối game, không dịch.
- `LiberationSans SDF`: font mặc định của TMP, chỉ dùng làm dự phòng.

Luật chọn cách vá theo tên nằm trong `RULES` của `tools/font/inventory.py`. Font chưa khớp luật nào thì giữ nguyên, và `fonts.json` ghi lý do là «chưa có luật».

## Chuỗi fallback

- Prefab chữ dùng `TTakeStd-Bold SDF` (22 chỗ) và `TShinGoPr6-Medium SDF` (8 chỗ). Hai font này có `DF-KakuPop-W5 SDF_Padding14_Take` trong bảng fallback.
- Không prefab nào trỏ thẳng vào KakuPop. Ảnh chụp lại cho thấy lời thoại tiếng Anh hiện bằng KakuPop. Vậy là game gán font lúc chạy, trong code. `usedBy` trong `fonts.json` chỉ đếm prefab, nên không thấy được việc này.
- KakuPop không có bảng fallback riêng, và `TMP_Settings` không có fallback chung. Chữ KakuPop thiếu sẽ rơi xuống `LiberationSans SDF` rồi tới bản dynamic của nó. Nét sans mảnh trong ảnh chụp khớp với đường này, nhưng chưa được xác nhận trong game.

Hệ quả: font nào có thể vẽ chữ tiếng Anh thì phải tự có đủ chữ Việt. Không được trông vào fallback.

## Cách vá

### Thay bằng Be Vietnam Pro

Dùng cho TShinGo và TTake. `bake_sdf.py` nướng atlas SDF bằng FreeType (padding 14, cỡ mẫu 64, gradient scale 15). Ký tự Be Vietnam Pro không có (□○△♪…) lấy từ Segoe UI Symbol và Yu Gothic. Trong một file, mọi font cùng loại dùng chung một atlas. Font chủ của atlas ưu tiên theo `HOST_PREFER`.

### Ghép dấu

Dùng cho KakuPop và Londrina. Không có file TTF gốc của hai font này, nên `compose_glyphs.py` dựng chữ Việt từ chính glyph của font:

| Dấu | Lấy từ |
| --- | --- |
| sắc, huyền, mũ, ngã | `´` `` ` `` `^` `~` có sẵn |
| hỏi | phần trên của `?`, bỏ chấm |
| nặng | `.` |
| trăng | nửa dưới của `o` |
| râu (ư, ơ) | cung trên phải của `o`, lật dọc |
| gạch của đ, Đ | `-` |
| « » | hai dấu `<` hoặc `>` thu nhỏ |

Cách ghép:

1. Đọc vùng glyph trong atlas, phóng 4 lần, cắt ở mức 0.5 để có hình chữ.
2. Ghép hình chữ gốc với dấu. Chữ hoa có dấu nhỏ hơn và sát hơn. Mũ và trăng đi kèm dấu thanh thì sắc, huyền, hỏi đứng bên phải mũ, còn ngã nằm trên.
3. Tính lại SDF với đúng padding của font đó. Lần thử trên chữ `a`, trường tính lại chỉ lệch khoảng 1% so với trường gốc.
4. Nới atlas lên phía trên rồi xếp glyph mới vào phần nới. Rect của TMP tính `m_Y` từ đáy ảnh, nên rect cũ không đổi.

Font KakuPop nhỏ (chỉ có chữ và số, như `_hcs`) không có dấu để mượn. Chúng mượn dấu của `DF-KakuPop-W5 SDF_Padding14_Take` (`DONOR` trong `apply_vietnamese_font.py`), co theo tỉ lệ cỡ chữ mẫu.

### Chữ nào phải có

`vi_chars()` trong `inventory.py` lấy các chữ có trong câu sẽ đưa vào game (theo `apply_locale_patch.translations()`) nhưng không có trong câu tiếng Anh. Hiện là chữ Việt và «». Chữ có sẵn trong câu tiếng Anh mà font thiếu (kana, chữ toàn khổ, ©…) thì game gốc đã vẽ qua fallback từ trước. Bản vá không đổi đường đó.

Câu dịch mà thêm ký tự mới, ví dụ `—`, thì `--check` sẽ báo thiếu. Khi đó thêm cách ghép ký tự đó vào `compose_glyphs.py`, giống `GUILLEMETS`.

## Lệnh

Chạy từ gốc repo. Cần `config.json` của game có `installs` và `fonts` (xem `config.example.json`).

```powershell
.\.venv\Scripts\python.exe -m pip install UnityPy pycryptodome freetype-py numpy scipy Pillow
.\.venv\Scripts\python.exe games\patapon12-replay\tools\font\apply_vietnamese_font.py
```

`apply_vietnamese_font.py` làm theo thứ tự:

1. Đọc `fonts.json`. Dừng nếu `catalog.json` khác lần quét trước.
2. Nướng atlas Be Vietnam Pro.
3. Vá từng `sharedassets` và từng bundle, ghi vào `patch/`.
4. Kiểm tra bằng `inventory.py --check`. Dừng nếu còn font thiếu chữ.
5. Áp lên bản cài qua launcher. Thêm `--no-install` để bỏ bước này.

Các lệnh khác:

| Lệnh | Việc |
| --- | --- |
| `tools\font\inventory.py` | Quét lại game, ghi `fonts.json`. Mất khoảng một phút. |
| `tools\font\inventory.py --check` | Đọc file trong `patch/`, báo font cần vá còn thiếu chữ nào. |
| `tools\font\preview.py [--name KakuPop]` | Vẽ câu mẫu bằng font đã vá vào `build/font-preview/`. |
| `tools\font\bake_sdf.py` | Chỉ nướng atlas Be Vietnam Pro và vẽ ảnh xem thử. |
| `python -m unittest test_compose_glyphs` (trong `tools\font`) | Kiểm tra phần ghép trên font giả, không cần bản cài. |

`apply_locale_patch.py` và `apply_vietnamese_font.py` ghi vào các bundle khác nhau. Nếu một ngày font nằm chung bundle với `LocalizeData`, script font sẽ dừng và báo. Khi đó phải gộp hai bản vá vào một lần ghi.

## Khi game cập nhật

1. `inventory.py` hoặc `apply_vietnamese_font.py` báo `catalog.json` khác lần quét trước.
2. Chạy `inventory.py`, rồi xem diff của `fonts.json`: font mới, tên bundle mới, font đổi chỗ.
3. Font mới chưa khớp luật thì thêm vào `RULES`.
4. Chạy lại `apply_vietnamese_font.py`, `preview.py`, rồi chơi thử.

## Bẫy

- **Luôn đọc file gốc.** Launcher đè bản vá lên thư mục cài. Script phải đọc qua `original()` trong `tools/game_config.py`. Hàm này lấy bản sao lưu của launcher nếu đã áp. Vá chồng lên bản đã vá sẽ ghép dấu hai lần và atlas nở mãi.
- **Atlas trong `.resS`.** Atlas của file gốc nằm trong `sharedassetsN.assets.resS`. Phải nạp resS cùng file, nếu không UnityPy báo không tìm thấy resource. Atlas mới ghi thẳng vào `.assets`.
- **Typetree.** File trong thư mục Data không kèm typetree. Cần `TypeTreeGenerator("2022.3.52f1")` đọc từ `GameAssembly.dll` và `global-metadata.dat`. Bundle thì có kèm typetree.
- **Rect và padding.** Font gốc của game để rect khít nét chữ, padding nằm ngoài rect. Atlas Be Vietnam Pro của `bake_sdf.py` lại để padding trong rect và dời bearing bù lại. TMP chấp nhận cả hai cách.
- **Material.** Đổi kích thước atlas thì phải sửa `_TextureWidth` và `_TextureHeight` của material trỏ vào atlas đó. Thay font thì còn phải đặt `_GradientScale` bằng padding cộng 1. Ghép dấu thì giữ `_GradientScale` cũ.
- **Mã hóa.** Bundle mã hóa bằng AES. Ghi lại thì phải mã hóa bằng đúng khóa cũ (`save_bundle` trong `extract_strings.py`).

## Chưa kiểm

- Chưa chụp lại trong game sau bản vá này. Cần xem lại màn đầu P1 (`P1.mission.missionid_01_00.line.190`) và lời dẫn ở làng (`P1.colony.128`).
- Chưa xác nhận font dự phòng có nét sans mảnh là LiberationSans.
- Chưa xem tips tiếng Anh vẽ bằng `LondrinaSolid_hcs`.
