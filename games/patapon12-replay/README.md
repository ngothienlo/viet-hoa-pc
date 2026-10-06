# PATAPON 1+2 REPLAY

Việt hóa **PATAPON 1+2 REPLAY** bản PC (Steam và Epic). Đây là một game trong repo, không phải tên repo.

Game dùng Unity IL2CPP và Addressables. Ngôn ngữ chính thức không có tiếng Việt. Chữ nằm trong asset bundle dưới `PATAPON12_REPLAY_Data/StreamingAssets/aa`. Phim `.usme` chưa nằm trong phạm vi.

## Trạng thái

Khung làm việc. Chưa trích chuỗi, chưa có bản dịch.

## Trong thư mục này

| Đường dẫn | Việc |
| --- | --- |
| `locale/vi/strings.csv` | Chuỗi dịch của game này. |
| `docs/pipeline.md` | Chữ nằm ở đâu, trích và đóng gói trên máy. |
| `docs/thuat-ngu.md` | Tên riêng và nhịp trống. |
| `docs/van-phong.md` | Văn phong tiếng Việt của game này. |
| `config.example.json` | Mẫu đường dẫn Steam / Epic. |

## Bắt đầu

Làm từ thư mục gốc repo.

1. Copy `games/patapon12-replay/config.example.json` thành `config.json` ngay trong thư mục game. `config.json` không được commit.
2. Đọc `docs/pipeline.md`.
3. Điền `locale/vi/strings.csv`. Xóa dòng `EXAMPLE-0001` khi bắt đầu dịch thật.
4. Kiểm tra CSV, rồi mở launcher để chọn thư mục cài:

```powershell
.\.venv\Scripts\Activate.ps1
python tools\validate_locale.py games\patapon12-replay
python -m launcher.app
```

File đè để trong `patch/`. Thư mục này đang trống nên nút Áp dụng tắt. Chọn thư mục và Chơi vẫn dùng được.

## Bản quyền

PATAPON và nội dung game thuộc Bandai Namco Entertainment / SAS. Thư mục này chỉ lưu bản dịch và ghi chú cho bản cài hợp pháp.
