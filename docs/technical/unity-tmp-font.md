# Font chữ Việt cho game Unity dùng TextMesh Pro

Cách làm chung, rút ra từ PATAPON 1+2 REPLAY. Sự thật của từng game (font nào, nằm ở đâu, vá thế nào) ghi ở `games/<id>/docs/font.md`. Bản đầy đủ nhất hiện có: `games/patapon12-replay/docs/font.md`.

## Triệu chứng và nguyên nhân

| Thấy trong game | Nguyên nhân thường gặp |
| --- | --- |
| Chữ có dấu khác nét với phần còn lại của câu | Font chính thiếu chữ đó. TMP lấy chữ từ font khác trong chuỗi fallback. |
| `□` | Không font nào trong chuỗi fallback có chữ đó. |
| Dấu bị cắt, chồng lên dòng trên | Dấu cao quá `m_AscentLine`, hoặc khoảng cách dòng của prefab quá chặt. |
| Chữ mới hiện, chữ cũ biến mất | Đã thay bảng glyph nhưng chưa đổi material sang atlas mới. |

Thứ tự TMP tìm chữ: font chính → `m_FallbackFontAssetTable` của font đó (đệ quy) → fallback chung trong `TMP_Settings` → font mặc định trong `TMP_Settings` và fallback của nó → ký tự thay thế (`□`).

Kết luận: font nào có thể vẽ chữ của bản dịch thì phải tự có đủ chữ Việt. Fallback chỉ dùng cho chữ mà bản gốc vốn đã vẽ qua fallback.

## Quy trình cho một game mới

1. **Kiểm kê một lần, ghi lại.** Viết `inventory.py` cho game đó. Ghi mọi TMP Font Asset vào `games/<id>/tools/font/fonts.json`: tên, file hoặc bundle, số chữ, atlas, padding, fallback, prefab nào dùng, và chữ của bản dịch mà font còn thiếu. Ghi kèm dấu vân tay của bản game (Patapon dùng sha1 của `catalog.json`). Session sau đọc file này thay vì quét lại.
2. **Chọn cách vá cho từng font** bằng luật theo tên, đặt trong code (`RULES`), không làm tay:
   - Font chữ thường của game (kiểu Gothic, Sans) → thay cả atlas bằng một font có đủ tiếng Việt, ví dụ Be Vietnam Pro.
   - Font mang bản sắc của game, không có TTF gốc → ghép dấu từ chính glyph của font.
   - Font Nhật, Hàn, Trung, font chỉ có số hay ký hiệu → giữ nguyên.
3. **Chữ bắt buộc** là chữ có trong câu sẽ đưa vào game mà không có trong câu gốc. Đừng bắt font có đủ mọi ký tự của cột `vi`: kana hay chữ toàn khổ vốn đã được game vẽ qua fallback.
4. **Vá từ file gốc**, không vá chồng lên bản đã vá. Launcher giữ bản sao lưu trong `%LOCALAPPDATA%\viet-hoa-pc\backups`.
5. **Kiểm tra trước khi áp**: đọc lại file đã vá, đối chiếu chữ bắt buộc, vẽ ảnh xem thử.
6. **Chơi thử** những chỗ có chữ kiểu riêng của game: lời thoại, tên, tips, menu.

## Kỹ thuật

### Đọc

- Bản build IL2CPP không kèm typetree trong thư mục Data. Dùng `UnityPy.helpers.TypeTreeGenerator(<bản Unity>)` với `load_local_game(<thư mục cài>)`.
- Bundle Addressables thường kèm typetree. Nhận diện TMP Font Asset theo tên trường (`m_CharacterTable` và `m_AtlasTextures`), không cần đọc MonoScript ở bundle khác.
- Atlas lớn nằm trong `.resS`. Phải nạp file `.resS` cùng env.
- Bundle có thể bị mã hóa. Cách mã hóa riêng của từng game, ghi trong `games/<id>/docs/pipeline.md`.

### SDF

- TMP dùng Alpha8. Cạnh chữ ở 0.5. Khoảng cách được chuẩn hóa: `alpha = 0.5 + d / (2 * padding)`.
- `_GradientScale` của material bằng padding cộng 1.
- `m_GlyphRect` tính `m_Y` từ đáy ảnh. Nới atlas lên phía trên (giữ ảnh cũ ở đáy) thì rect cũ không đổi.
- Font của game thường để rect khít nét chữ, padding nằm ngoài rect. Phải chừa đủ padding và khoảng hở quanh mỗi glyph mới.

### Ghép dấu từ glyph có sẵn

1. Cắt vùng glyph trong atlas, phóng lên (Patapon dùng 4 lần), cắt ở mức 0.5 để có hình chữ.
2. Dấu lấy từ glyph sẵn có: `´ ` ^ ~ . ? o - < >`. Font nhỏ không có dấu thì mượn của font cùng họ.
3. Ghép bằng phép hợp hình, rồi tính lại SDF bằng biến đổi khoảng cách (`scipy.ndimage.distance_transform_edt`) với đúng padding.
4. Kiểm tra quy ước: dựng lại trường của một chữ có sẵn rồi so với atlas gốc. Lệch khoảng 1% là đúng quy ước.

Đổi lại, dấu ghép không đẹp bằng dấu do người vẽ font làm. Bù lại, chữ giữ nguyên nét của game, và không phải mang font ngoài vào.

### Ghi

- Thay atlas: `Texture2D.set_image(..., target_format=Alpha8)` rồi `save()`. Dữ liệu được ghi thẳng vào file, không còn trỏ sang `.resS`.
- Sửa bảng glyph: `m_GlyphTable`, `m_CharacterTable`, `m_UsedGlyphRects`, `m_AtlasWidth`, `m_AtlasHeight`, `m_CreationSettings`.
- Sửa material trỏ vào atlas: `_MainTex`, `_TextureWidth`, `_TextureHeight`, và `_GradientScale` nếu đổi padding.
- Bundle: lưu bằng `packer="original"`, mã hóa lại bằng đúng khóa cũ, rồi đọc lại một lần để kiểm tra.

## Không làm

- Không thêm font fallback để vá thiếu chữ. Một câu sẽ lẫn hai mặt chữ.
- Không trỏ font hệ thống qua tên font khi bản TMP của game cũ hơn 3.2.
- Không commit atlas, `.assets`, bundle hay file TTF. Chỉ commit script, `fonts.json` và docs.
