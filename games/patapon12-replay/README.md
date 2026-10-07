# PATAPON 1+2 REPLAY

Việt hóa **PATAPON 1+2 REPLAY** bản PC (Steam và Epic). Đây là một game trong repo, không phải tên repo.

Game dùng Unity IL2CPP và Addressables. Ngôn ngữ chính thức không có tiếng Việt. Chữ nằm trong asset bundle dưới `PATAPON12_REPLAY_Data/StreamingAssets/aa`. Phim `.usme` chưa nằm trong phạm vi.

## Trạng thái

Đã có bản tiếng Việt viết tay cho bảng chuỗi. Bản vá ghi các câu đó vào bốn bundle `LocalizeData`, và thay font Latin bằng Be Vietnam Pro. Menu tựa vẫn là ảnh.

## Trong thư mục này

| Đường dẫn | Việc |
| --- | --- |
| `locale/vi/strings.csv` | Chuỗi dịch của game này. |
| `docs/pipeline.md` | Chữ nằm ở đâu, trích và đóng gói trên máy. |
| `docs/thuat-ngu.md` | Tên riêng và nhịp trống. |
| `docs/van-phong.md` | Văn phong tiếng Việt của game này. |
| `config.example.json` | Mẫu đường dẫn Steam / Epic và file font. |
| `runtime.lock.json` | URL và sha256 của BepInEx và AutoTranslator. |
| `tools/fetch_runtime.py` | Tải hai gói đó vào `patch/`. |
| `tools/extract_strings.py` | Trích hết câu tiếng Anh từ `LocalizeData` vào CSV. |
| `tools/translate_rhythm.py` | Ghi câu hướng dẫn nhịp viết tay vào CSV. |
| `tools/font/` | Nướng atlas Be Vietnam Pro và vá font Latin trong `sharedassets`. |
| `tools/echo_translate.py` | Hook lúc chơi. Không dùng để thu thập câu. |

## Bắt đầu

Làm từ thư mục gốc repo.

1. Copy `games/patapon12-replay/config.example.json` thành `config.json` ngay trong thư mục game. `config.json` không được commit.
2. Đọc `docs/pipeline.md`.
3. Trích câu, rồi kiểm tra CSV:

```powershell
.\.venv\Scripts\python.exe games\patapon12-replay\tools\extract_strings.py
python tools\validate_locale.py games\patapon12-replay
```

4. Dịch cột `vi` trong `locale/vi/strings.csv`. Giữ nguyên `id` và `source`.
5. Vá bundle rồi mở launcher để áp bản dịch:

```powershell
.\.venv\Scripts\Activate.ps1
python tools\validate_locale.py games\patapon12-replay
python -m launcher.app
```

File đè để trong `patch/`. Config AutoTranslator nằm sẵn trong đó. Binary chỉ có sau khi chạy `fetch_runtime.py`. Áp dụng trước khi fetch thì game chỉ nhận file config, chưa có BepInEx.

## Bản quyền

PATAPON và nội dung game thuộc Bandai Namco Entertainment / SAS. Thư mục này chỉ lưu bản dịch và ghi chú cho bản cài hợp pháp.
