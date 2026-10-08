# Font

Cách làm chung cho game Unity dùng TextMesh Pro: `docs/technical/unity-tmp-font.md`. File này ghi những điều riêng của Potion Permit.

## Game có font gì

Danh sách đầy đủ nằm ở `tools/font/fonts.json`, do `tools/font/inventory.py` sinh ra. Không sửa tay. Dấu vân tay của bản game là sha1 của `StreamingAssets/aa/Windows/catalog.json`. Game cập nhật thì chạy lại:

```powershell
.\.venv\Scripts\python.exe games\potion-permit\tools\font\inventory.py
```

Tóm tắt:

- Mọi chữ trong game vẽ bằng `PixelMplus12-Regular`. Font này là SDF dựng từ font pixel 12 px ở cỡ 46, padding 12, atlas 512×512. Nó chỉ có 97 chữ ASCII, kèm 14 font fallback.
- Fallback có chữ Latin:
  - `PixelMplus12-Latin_Supplement_PP`, cùng họ: có á à â ã é ê ó ô… Chữ hoa có dấu bị ép thấp còn 7 hàng điểm ảnh để dấu vừa trong dòng.
  - `LanaPixel12-Latin_Extended_PP`, khác họ, nét đậm hơn: có ă đ ĩ ũ ơ ư.
- Font có hai bản giống nhau: một trong `resources.assets`, một trong bundle `prefab-battle_assets_all_*.bundle` (các prefab của màn đánh nhau). Phải vá cả hai.
- `LiberationSans SDF` là font mặc định của TMP. Không thấy chữ nào của game dùng font này.

Trước khi vá, `Player.log` báo `The character with Unicode value ọ was not found in the [PixelMplus12-Regular] font asset or any potential fallbacks` và chữ hiện thành `□`. Chữ như ă, đ thì lấy từ LanaPixel, nên lệch họ font với phần còn lại của câu.

## Cách vá

`tools/build_patch.py` gọi `tools/font/patch_font.py`. Launcher làm việc này khi bấm Áp dụng.

1. Đọc hình từng chữ của `PixelMplus12-Regular` và `PixelMplus12-Latin_Supplement_PP`, cắt ở mức 0.5 của trường SDF.
2. Ghép 102 chữ Việt font còn thiếu bằng `tools/font/pixel_glyphs.py`. Xem mục dưới.
3. Tính SDF cho chữ mới: khoảng cách từ tâm ô tới mép nét, trừ nửa ô. So với glyph gốc, cách này lệch trung bình khoảng 2%.
4. Nới atlas lên phía trên theo bước 64 hàng (512×512 thành 512×1216), xếp chữ mới vào phần nới. Rect cũ không đổi.
5. Sửa `m_GlyphTable`, `m_CharacterTable`, `m_UsedGlyphRects`, `m_AtlasHeight`, và `_TextureHeight` của material dùng atlas này.
6. Ghi `resources.assets` và bundle `prefab-battle`. Bundle lưu bằng `packer="original"`.
7. Sửa `catalog.json`. Addressables kiểm CRC của bundle khi nạp, nên CRC của bundle đã vá đổi thành `0` (không kiểm). Chuỗi JSON trong `m_ExtraDataString` là UTF-16, nên giữ đúng độ dài: thay chữ số bằng `0` và dấu cách. Mục của bundle tìm theo mã hash ở cuối tên file.
8. Đọc lại hai file đã vá. Font đích phải có đủ 134 chữ Việt (tính cả chữ Latin-1 của fallback cùng họ), atlas đúng kích thước.

Đường dẫn của bundle trong thư mục ra dài khoảng 130 ký tự. Script ghi và xóa bằng dạng `\\?\` để không vướng giới hạn 260 ký tự của Windows.

## Ghép chữ theo lưới điểm ảnh

Một điểm ảnh thiết kế rộng khoảng 3,85 đơn vị atlas, cao khoảng 3,9. Hàng 0 là hàng ngay trên chân chữ, đáy ở y = -2. Chữ thường cao 6 hàng (0–5), chữ hoa 9 hàng (0–8). Dấu của font nằm ở hàng 8–9.

Lưới này không khớp tuyệt đối với cách game làm tròn: dựng lại glyph gốc từ ô điểm ảnh lệch khoảng 6% số đơn vị. Vì vậy:

- Thân chữ và dấu có sẵn (sắc, huyền, ngã, mũ) lấy **nguyên hình** từ atlas, ở đúng vị trí gốc. Không dựng lại.
- Chỉ dấu font không có mới vẽ bằng ô điểm ảnh: hỏi, nặng, trăng, râu, gạch của đ.

| Phần | Nguồn |
| --- | --- |
| Thân chữ thường a e o u y | Chữ ASCII của `PixelMplus12-Regular` |
| Thân i không chấm | Phần dưới của `í` |
| Thân chữ hoa (ép 7 hàng) | Phần dưới của `Á É Í Ó Ú Ý` |
| Sắc, huyền, ngã | Phần trên của `á à ã` (chữ thường), `Á À Ã` (chữ hoa) |
| Mũ | Phần trên của `â`, `Â` |
| Hỏi | Vẽ 3 hàng: `.##` / `...#` / `..#`. Bản nhỏ 2 hàng khi đi cùng mũ hoặc trăng |
| Nặng | 1 điểm ảnh ở hàng -2, cột 2. Chữ y: hàng -3 để tránh đuôi |
| Trăng | Vẽ 2 hàng: `.#..#` / `..##` |
| Râu ơ | 2 điểm ảnh chéo từ góc trên phải của o |
| Râu ư | Nét đứng 2 điểm ảnh, chéo lên từ đỉnh nét phải của u |
| Gạch đ | 2 điểm ảnh ở hàng 7, bên trái nét đứng. Đ: dời D sang phải một cột, gạch ở hàng 4 |

Chữ có hai dấu:

- Chữ thường: mũ hoặc trăng ở hàng 7–8, dấu thanh ở hàng 9–10.
- Chữ hoa: mũ hoặc trăng ở hàng 8–9, dấu thanh ở hàng 10–11. Đỉnh dấu vượt dòng ascent (40) khoảng 5 đơn vị. Dòng cao 52 nên vẫn còn chỗ.

Chữ có râu (ơ ư Ơ Ư và các chữ có dấu thanh của chúng) và Đ rộng thêm một ô: advance 27 thay vì 23. Nếu không, râu sẽ chạm chữ kế bên.

Xem thử mà không ghi gì vào game:

```powershell
.\.venv\Scripts\python.exe games\potion-permit\tools\font\patch_font.py --preview chu-viet.png
.\.venv\Scripts\python.exe games\potion-permit\tools\font\patch_font.py --preview cau.png "Chào Dược sư!"
```

Test không cần bản cài game:

```powershell
.\.venv\Scripts\python.exe -m unittest games\potion-permit\tools\font\test_patch_font.py
```

## Còn phải xem trong game

- Dấu hỏi nhỏ trên chữ có mũ (ẩ ể ổ) chỉ cao 2 hàng. Cần xem có đọc ra là dấu hỏi không.
- Chữ hoa có hai dấu (ĐỦ RỒI, NỔI) cao hơn dòng ascent. Cần xem có bị cắt ở khung thoại không.
- Màn đánh nhau dùng bản font trong bundle `prefab-battle`.
