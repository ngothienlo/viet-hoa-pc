# Pipeline

Thư mục game này là `games/potion-permit/`. Lệnh chạy từ thư mục gốc repo.

Làm trên bản cài hợp pháp. Bản Steam: app id 1337760.

## Chữ nằm ở đâu

- Unity 2020.1.1f1, bản Mono (`Potion Permit_Data/Managed/`). File `.assets` và bundle Addressables không mã hóa.
- Chữ dùng I2 Localization. Toàn bộ term nằm trong component `LanguageSource`. Có hai bản:
  - `sharedassets0.assets` (path id 36): bản đúng, dùng làm nguồn.
  - scene `level1` (path id 55587): gần trùng. Hai term XIAO (`EVENTDIALOG_FP3_05_03`, `_04`) bị lệch.
- `resources.assets` có `I2Languages` (LanguageSourceAsset) chỉ gồm 7 term mẫu của I2. Không dùng.
- 9.952 term, 11 ngôn ngữ (English `en-US`, French, German, Spanish, Japanese, Russian, Korean, Simplified Chinese, Portuguese Brazil, Indonesian, Chinese Traditional). Chưa có tiếng Việt.
- ScriptableObject trong bundle `so-*` (vật phẩm, nhiệm vụ, phòng hội thoại…) chỉ lưu mã term, không lưu chữ.
- Đọc MonoBehaviour cần `TypeTreeGenerator("2020.1.1f1", "AssetStudio")`, nạp từ `Managed/`. Thiếu backend `AssetStudio` thì typetree đọc lệch.

## Trích câu

```powershell
.\.venv\Scripts\python.exe games\potion-permit\tools\extract_strings.py
python tools\validate_locale.py games\potion-permit
```

Script ghi `locale/vi/strings.csv`:
- `id` là tên term của I2, ví dụ `MYER/DIALOG_01`.
- `context` là nhóm term (phần trước `/`): NPC (`MYER`, `REYNER`…), `Group` (hội thoại nhóm), `Quest`, `Item`, `UI`…
- Bỏ term trống và term chỉ có số. Còn 9.661 term.

Chạy lại sau khi game cập nhật: term có câu gốc không đổi thì giữ nguyên bản dịch.

Câu gốc có:
- placeholder `{[CHARACTER_NAME]}` (tên người chơi), `{[DOG_NAME]}`, `{[BODY_PART]}`, `{[SYMPTOM]}`, `{0}`
- thẻ màu `<#a27dde>…</color>`
- xuống dòng thật trong câu

Ba thứ này phải giữ nguyên số lượng.

## Dịch

Theo `docs/thuat-ngu.md` và `docs/van-phong.md`. Bản dịch theo lô gộp bằng:

```powershell
.\.venv\Scripts\python.exe games\potion-permit\tools\apply_fixes.py --dry-run lo1.json
.\.venv\Scripts\python.exe games\potion-permit\tools\apply_fixes.py lo1.json
```

Mỗi file là mảng JSON `{"id", "vi"}`. Script loại câu lệch placeholder, thẻ màu, số dòng, thứ tự mở và đóng thẻ. Câu nhận vào lên `review`.

## Áp vào game

`game.json` có `"build": "tools/build_patch.py"`. Bấm Áp dụng trong launcher (hoặc `VietHoa.exe`) thì launcher làm như sau:

1. Đọc `sharedassets0.assets` và `level1` gốc của người chơi, qua bản sao lưu nếu đã áp.
2. Ghi câu Việt vào **cột English** của cả hai `LanguageSource`.
3. Đọc lại để kiểm.
4. Chép hai file vào bản cài.

Người chơi để ngôn ngữ của game là English thì thấy tiếng Việt. Term chưa dịch giữ tiếng Anh.

Chạy tay:

```powershell
.\.venv\Scripts\python.exe games\potion-permit\tools\build_patch.py "<thư mục cài>" "<thư mục ra>"
```

Ghi đè cột English, không thêm cột Vietnamese: menu chọn ngôn ngữ của game không có tiếng Việt, và các ngôn ngữ khác giữ nguyên.

## Đã chạy thử

2026-10-08, bản Steam (#19): áp 782 term qua launcher (734 câu khác bản gốc trong mỗi file), mở game. Game nạp bình thường. `Player.log` (`%USERPROFILE%\AppData\LocalLow\MasshiveMedia\Potion Permit\`) chỉ báo thiếu glyph chữ Việt (ự, ề, ị, ể…) trong `PixelMplus12-Regular` và các fallback, đúng như dự kiến khi chưa vá font.

## Font

Game dùng font pixel họ PixelMplus12 kèm 14 font fallback. Font chưa có chữ Việt riêng (ư, ơ, ế…). Xem ticket font (#20) và `docs/font.md` khi có.

## Không commit

- Thư mục cài game, `*.assets`, `level*`, `*.bundle`, `*.resS`
- `patch/` chỉ có `.gitkeep`. File vá sinh ra khi chạy tay nằm trong đó nhưng không commit.
- `config.json`
