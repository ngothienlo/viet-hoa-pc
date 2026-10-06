# PATAPON 1+2 REPLAY — Việt hóa

Dự án riêng để dịch **PATAPON 1+2 REPLAY** bản PC (Steam và Epic) sang tiếng Việt.

Game dùng Unity IL2CPP và Addressables. Ngôn ngữ chính thức gồm tiếng Anh, Nhật, Trung giản thể, Trung phồn thể, Hàn, Pháp, Đức, Ý, Tây Ban Nha. Không có tiếng Việt. Chữ nằm trong asset bundle dưới `PATAPON12_REPLAY_Data/StreamingAssets/aa`. Phim và một phần âm thanh dùng CRIWARE (`.usme`), không nằm trong phạm vi dịch của khung này.

Repo **private**. Chỉ chứa bản dịch, bảng thuật ngữ và công cụ kiểm tra. Không chứa file cài game, bundle, video hay âm thanh.

## Trạng thái

Khung làm việc. Chưa trích chuỗi, chưa có bản dịch.

## Cấu trúc

| Đường dẫn | Việc |
| --- | --- |
| `locale/vi/strings.csv` | Chuỗi dịch. Một dòng một khóa. |
| `docs/pipeline.md` | Cách trích, dịch và đóng gói trên máy. |
| `docs/thuat-ngu.md` | Tên riêng và nhịp trống giữ nguyên. |
| `docs/van-phong.md` | Văn phong tiếng Việt. |
| `config.example.json` | Mẫu đường dẫn Steam / Epic. |
| `tools/validate_locale.py` | Kiểm tra CSV trước khi đóng gói. |

## Bắt đầu

1. Copy `config.example.json` thành `config.json`, điền thư mục cài game. `config.json` không được commit.
2. Đọc `docs/pipeline.md` trước khi trích chuỗi.
3. Điền `locale/vi/strings.csv`. Xóa dòng `EXAMPLE-0001` khi bắt đầu dịch thật.
4. Dùng virtual env rồi kiểm tra CSV:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python tools\validate_locale.py
```

Env này gắn với Python 3.14. Muốn đổi phiên bản thì cài thêm bản đó, xóa `.venv`, rồi tạo lại, ví dụ `py -3.12 -m venv .venv`. Gói cài trong env không lẫn vào Python của hệ thống. Thư mục `.venv` không được commit.

## Bản quyền

PATAPON và nội dung game thuộc Bandai Namco Entertainment / SAS. Repo chỉ lưu bản dịch và ghi chú cho bản cài hợp pháp của người chơi.
