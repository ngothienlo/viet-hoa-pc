# Potion Permit

Việt hóa **Potion Permit** bản PC (Steam). Đây là một game trong repo, không phải tên repo.

Game dùng Unity 2020.1 (Mono) và I2 Localization. Ngôn ngữ chính thức không có tiếng Việt. Chữ nằm trong `LanguageSource` của `sharedassets0.assets` và scene `level1`.

## Trạng thái

Đã trích 9.661 term. Đang dịch theo các ticket #19 (UI và nhóm nhỏ), #21 (nhiệm vụ, vật phẩm, bảng tin, tutorial), #22 và #23 (hội thoại NPC). Font pixel chưa có chữ Việt (#20).

## Trong thư mục này

| Đường dẫn | Việc |
| --- | --- |
| `locale/vi/strings.csv` | Chuỗi dịch của game này. |
| `docs/pipeline.md` | Chữ nằm ở đâu, trích, gộp bản dịch, áp vào game. |
| `docs/thuat-ngu.md` | Tên riêng và thuật ngữ. |
| `docs/van-phong.md` | Văn phong, bảng xưng hô theo từng NPC. |
| `config.example.json` | Mẫu đường dẫn Steam / Epic. |
| `tools/extract_strings.py` | Trích câu tiếng Anh từ `LanguageSource` vào CSV. |
| `tools/apply_fixes.py` | Gộp file dịch (JSON) vào CSV, có kiểm tra placeholder, thẻ màu, xuống dòng. |
| `tools/build_patch.py` | Tạo bản vá từ bản cài của người chơi. Launcher gọi script này khi bấm Áp dụng. |
| `tools/game_config.py` | Đọc `config.json`, tìm file gốc trước khi vá. |

## Bắt đầu

Làm từ thư mục gốc repo.

1. Đọc `docs/pipeline.md`, `docs/thuat-ngu.md`, `docs/van-phong.md`.
2. Trích câu, rồi kiểm tra CSV:

```powershell
.\.venv\Scripts\python.exe games\potion-permit\tools\extract_strings.py
python tools\validate_locale.py games\potion-permit
```

3. Mở launcher, chọn Potion Permit, bấm Áp dụng. Trong game, để ngôn ngữ là English.

## Bản quyền

Potion Permit và nội dung game thuộc MasshiveMedia / PQube. Thư mục này chỉ lưu bản dịch và ghi chú cho bản cài hợp pháp.
