# Font

Tài liệu này ghi font nào trong PATAPON 1+2 REPLAY vẽ chữ gì, và vá thế nào để chữ Việt hiện đủ, cùng một mặt chữ, giữ nét gốc của game. Cách làm chung cho game Unity dùng TextMesh Pro nằm ở `docs/technical/unity-tmp-font.md`.

Không cần quét lại game để biết font. Danh sách đầy đủ nằm trong `tools/font/fonts.json`.

## Lịch sử

1. **#8:** thay TShinGo và TTake trong `sharedassets` bằng Be Vietnam Pro.
2. **#9, lần một.** Ảnh chụp lúc đó có hai lỗi: một câu lẫn hai font (nét Patapon và nét sans mảnh), và `ẳ` thành ô vuông. Mình đoán font kiểu Patapon là DF-KakuPop-W5, nên ghép dấu cho KakuPop, Londrina, và thay thêm các font TShinGo, TTake trong bundle bằng Be Vietnam Pro. Kết quả: chữ đồng nhất, nhưng lời thoại mất nét Patapon.
3. **#9, lần hai.** Font kiểu Patapon của lời thoại thực ra là **TTakeStd-Bold**. Vẽ thử atlas gốc thì thấy đúng chữ `g` và nét vuông như trong ảnh chụp. Thay TTake bằng Be Vietnam Pro là làm mất nét gốc. Vì vậy mọi font Latin chuyển sang ghép dấu, giữ nét gốc. Be Vietnam Pro chỉ còn dùng cho `_savewindow`.
4. **#17.** `_savewindow` cũng chuyển sang ghép dấu, mượn chữ gốc, số đo và dấu của `TShinGoPr6-Medium SDF`. Không font nào còn dùng Be Vietnam Pro, nên bản exe không phải mang theo file TTF nào.

Bài học: trước khi chọn cách vá, vẽ atlas gốc của font ra ảnh rồi so với ảnh chụp trong game (`preview.py`, hoặc đoạn đọc atlas trong `compose_glyphs.py`). Không đoán font theo tên.

## Bản đồ font

`inventory.py` quét `sharedassets*`, `resources.assets`, `level*` và 84 bundle Addressables. Lần quét ngày 2026-10-07 tìm được 109 TMP Font Asset. Đa số là font Nhật, Hàn, Trung, giữ nguyên.

Font cần vá:

| Font | Nằm ở | Cách vá |
| --- | --- | --- |
| `TTakeStd-Bold SDF` | `sharedassets5` | Ghép dấu. Đây là font kiểu Patapon của lời thoại. |
| `TTakeStd-Bold_hcs` | `sharedassets0`, bundle `91aca73a` | Ghép dấu |
| `TShinGoPr6-Medium SDF` | `sharedassets1` | Ghép dấu |
| `TShinGoPr6-Medium SDF_mission` (padding 1), `_launcher_hcs` | `sharedassets0` | Ghép dấu |
| `TShinGoPr6-Regular SDF` | bundle `88a48bd1`, `91aca73a` | Ghép dấu |
| `TShinGoPr6-Medium_hcs`, `TShinGoPr6-Regular_hcs` | bundle `91aca73a` | Ghép dấu |
| `DF-KakuPop-W5 SDF_Padding14_Take` | `sharedassets1` | Ghép dấu |
| `DF-KakuPop-W5_hcs`, `DF-KakuPop-W5_name` | bundle `91aca73a` | Ghép dấu |
| `DF-KakuPop-W5_hcs_sc`, `_name_sc` | bundle `f7cd5c4c` (bản Trung giản thể) | Ghép dấu |
| `DF-KakuPop-W5_hcs_tc` | bundle `064a729a` (bản Trung phồn thể) | Ghép dấu |
| `LondrinaSolid_hcs` | bundle `91aca73a`, prefab tips tiếng Anh dùng | Ghép dấu |
| `TShinGoPr6-Medium_savewindow` | `sharedassets0` | Ghép dấu. Font chỉ có 18 chữ hoa, nên mượn cả chữ gốc của TShinGo. |

Font giữ nguyên, kèm lý do:

- Font Nhật, Hàn, Trung (`_ja`, `_kr`, NotoSansKR, GothicA1, PoorStory, DFPGB, DFT, DFGB…).
- Font chỉ có chữ toàn khổ (`_fs`), chỉ có số hay ký hiệu (`_number`, `_symbol`, `_onpu`), hoặc chỉ có vài ký tự.
- `TTakeStd-Bold_staffroll`: chữ chạy cuối game, không dịch.
- `LiberationSans SDF`: font mặc định của TMP, chỉ dùng làm dự phòng.

Luật chọn cách vá theo tên nằm trong `RULES` của `tools/font/inventory.py`. Font chưa khớp luật nào thì giữ nguyên, và `fonts.json` ghi lý do là «chưa có luật».

## Chuỗi fallback

- Prefab chữ dùng `TTakeStd-Bold SDF` (22 chỗ) và `TShinGoPr6-Medium SDF` (8 chỗ). Hai font này có `DF-KakuPop-W5 SDF_Padding14_Take` trong bảng fallback.
- TTake gốc có ASCII và Latin-1 (à á â ã è é ê…), nên «này» hay «cả» vẫn hiện nét Patapon. Chữ riêng của tiếng Việt (ư ơ đ ế ễ…) thì không có.
- Chữ TTake thiếu sẽ rơi xuống KakuPop, rồi tới `LiberationSans SDF` mặc định và bản dynamic của nó, vì `TMP_Settings` không có fallback chung. Nét sans mảnh trong ảnh chụp khớp với đường này. Riêng `ẳ` thành ô vuông vì cả chuỗi đều không có.
- `usedBy` trong `fonts.json` chỉ đếm prefab. Font nào game gán bằng code lúc chạy thì không hiện ở đó.

Hệ quả: font nào có thể vẽ chữ tiếng Anh thì phải tự có đủ chữ Việt. Không được trông vào fallback.

## Cách vá

### Ghép dấu (mặc định)

Không có file TTF gốc của các font này. `compose_glyphs.py` dựng chữ Việt từ chính glyph của font:

| Dấu | Lấy từ, theo thứ tự ưu tiên |
| --- | --- |
| sắc, huyền, mũ, ngã | dấu của chữ Latin-1 có sẵn (`á` `à` `â` `ã`, bản hoa cho chữ hoa), rồi tới `´` `` ` `` `^` `~` `˜` |
| hỏi | phần trên của `?`, bỏ chấm |
| nặng | `.` |
| trăng | nửa dưới của `o` |
| râu (ư, ơ) | dựng theo hình học: một nét ngang bám đỉnh thân phải, một nét đứng vểnh lên, dày bằng nét chữ đo trên `l` |
| gạch của đ, Đ | `-` |
| « » | hai dấu `<` hoặc `>` thu nhỏ |

Dấu tách từ chữ Latin-1 là dấu do người vẽ font làm, đúng nét và đúng cỡ. Đó là lý do TTake và TShinGo ghép đẹp hơn KakuPop: KakuPop không có chữ Latin-1 nào.

Cách ghép:

1. Đọc vùng glyph trong atlas, phóng 4 lần, cắt ở mức 0.5 để có hình chữ.
2. Ghép hình chữ gốc với dấu. Mũ và trăng đi kèm dấu thanh thì sắc, huyền, hỏi đứng bên phải mũ, còn ngã nằm trên. Chữ có râu được nới bước chữ để râu không đè chữ sau.
3. Tính lại SDF với đúng padding của font đó. Lần thử trên chữ `a`, trường tính lại chỉ lệch khoảng 1% so với trường gốc.
4. Nới atlas lên phía trên, mỗi bước 64 hàng, vừa đủ cho glyph mới. Rect của TMP tính `m_Y` từ đáy ảnh, nên rect cũ không đổi.

Font nhỏ (bản `_hcs`, chỉ có chữ và số) không có dấu để mượn. Chúng mượn dấu của font lớn cùng họ, co theo tỉ lệ cỡ chữ mẫu (`DONORS` trong `apply_vietnamese_font.py`):

| Họ | Font cho mượn |
| --- | --- |
| TTakeStd | `TTakeStd-Bold SDF` (`sharedassets5`) |
| TShinGoPr6 | `TShinGoPr6-Medium SDF` (`sharedassets1`) |
| DF-KakuPop, LondrinaSolid | `DF-KakuPop-W5 SDF_Padding14_Take` (`sharedassets1`) |

### Thay bằng Be Vietnam Pro

Hiện không font nào dùng cách này. Đường code vẫn giữ cho game sau, khi có font thiếu chữ gốc mà cũng không mượn được của font cùng họ. `bake_sdf.py` nướng atlas SDF bằng FreeType (padding 14, cỡ mẫu 64, gradient scale 15). Cần file TTF Be Vietnam Pro, khai trong `config.json` (`fonts.regular`, `fonts.bold`).

### Chữ nào phải có

`vi_chars()` trong `inventory.py` lấy các chữ có trong câu sẽ đưa vào game (theo `apply_locale_patch.translations()`) nhưng không có trong câu tiếng Anh. Hiện là chữ Việt và «». Chữ có sẵn trong câu tiếng Anh mà font thiếu (kana, chữ toàn khổ, ©…) thì game gốc đã vẽ qua fallback từ trước. Bản vá không đổi đường đó.

Câu dịch mà thêm ký tự mới, ví dụ `—`, thì `--check` sẽ báo thiếu. Khi đó thêm cách ghép ký tự đó vào `compose_glyphs.py`, giống `GUILLEMETS`.

## Lệnh

Người chơi chỉ cần bấm Áp dụng trong launcher hoặc `VietHoa.exe`: launcher gọi `tools/build_patch.py`, script này chạy cả bản vá câu thoại lẫn bản vá font (xem `docs/technical/launcher.md`). Các lệnh dưới đây để chạy tay từ gốc repo; cần `config.json` của game có `installs`.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe games\patapon12-replay\tools\font\apply_vietnamese_font.py
```

`apply_vietnamese_font.py` làm theo thứ tự:

1. Đọc `fonts.json`. Dừng nếu `catalog.json` khác lần quét trước.
2. Nướng atlas Be Vietnam Pro, chỉ khi `fonts.json` còn font `replace-*` (hiện không có).
3. Vá từng `sharedassets` và từng bundle, ghi vào `patch/`.
4. Kiểm tra bằng `inventory.py --check`. Dừng nếu còn font thiếu chữ.
5. Áp lên bản cài qua launcher. Thêm `--no-install` để bỏ bước này.

Các lệnh khác:

| Lệnh | Việc |
| --- | --- |
| `tools\font\inventory.py` | Quét lại game, ghi `fonts.json`. Mất khoảng một phút. |
| `tools\font\inventory.py --check` | Đọc file trong `patch/`, báo font cần vá còn thiếu chữ nào. |
| `tools\font\preview.py [--name TTake]` | Vẽ câu mẫu bằng font đã vá vào `build/font-preview/`. |
| `tools\font\bake_sdf.py` | Chỉ nướng atlas Be Vietnam Pro và vẽ ảnh xem thử. |
| `python -m unittest test_compose_glyphs` (trong `tools\font`) | Kiểm tra phần ghép trên font giả, không cần bản cài. |

`apply_locale_patch.py` và `apply_vietnamese_font.py` ghi vào các bundle khác nhau. Nếu một ngày font nằm chung bundle với `LocalizeData`, script font sẽ dừng và báo. Khi đó phải gộp hai bản vá vào một lần ghi.

## Khi game cập nhật

1. `inventory.py` hoặc `apply_vietnamese_font.py` báo `catalog.json` khác lần quét trước.
2. Chạy `inventory.py`, rồi xem diff của `fonts.json`: font mới, tên bundle mới, font đổi chỗ.
3. Font mới chưa khớp luật thì vẽ atlas gốc của font đó ra ảnh, rồi thêm vào `RULES`.
4. Chạy lại `apply_vietnamese_font.py`, `preview.py`, rồi chơi thử.

## Bẫy

- **Luôn đọc file gốc.** Launcher đè bản vá lên thư mục cài. Script phải đọc qua `original()` trong `tools/game_config.py`. Hàm này lấy bản sao lưu của launcher nếu đã áp. Vá chồng lên bản đã vá sẽ ghép dấu hai lần và atlas nở mãi.
- **Atlas trong `.resS`.** Atlas của file gốc nằm trong `sharedassetsN.assets.resS`. Phải nạp resS cùng file, nếu không UnityPy báo không tìm thấy resource. Atlas mới ghi thẳng vào `.assets`.
- **Typetree.** File trong thư mục Data không kèm typetree. Cần `TypeTreeGenerator("2022.3.52f1")` đọc từ `GameAssembly.dll` và `global-metadata.dat`. Bundle thì có kèm typetree.
- **Rect và padding.** Font gốc của game để rect khít nét chữ, padding nằm ngoài rect. Atlas Be Vietnam Pro của `bake_sdf.py` lại để padding trong rect và dời bearing bù lại. TMP chấp nhận cả hai cách.
- **Material.** Đổi kích thước atlas thì phải sửa `_TextureWidth` và `_TextureHeight` của material trỏ vào atlas đó. Thay font thì còn phải đặt `_GradientScale` bằng padding cộng 1. Ghép dấu thì giữ `_GradientScale` cũ.
- **Mã hóa.** Bundle mã hóa bằng AES. Ghi lại thì phải mã hóa bằng đúng khóa cũ (`save_bundle` trong `extract_strings.py`).

## Chưa kiểm

- Ảnh chụp sau lần hai (ghép dấu cho TTake): cần xem lại màn đầu P1 (`P1.mission.missionid_01_00.line.190`) và lời dẫn ở làng (`P1.colony.128`).
- Chữ hoa có hai dấu (Ấ, Ẫ, Ỗ) trong bóng thoại hẹp: dấu có thể chạm dòng trên.
- Chưa xác nhận font sans mảnh trong ảnh chụp lần một là LiberationSans.
- Chưa xem tips tiếng Anh vẽ bằng `LondrinaSolid_hcs`.
