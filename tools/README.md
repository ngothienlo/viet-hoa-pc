# Công cụ

`validate_locale.py` đọc `locale/vi/strings.csv` và báo:

- thiếu cột hoặc sai thứ tự cột
- `id` trống hoặc trùng
- `status` ngoài `todo`, `draft`, `review`, `done`
- dòng `review` hoặc `done` nhưng ô `vi` trống
- lệch placeholder, thẻ rich text hoặc `\n` giữa câu gốc và câu Việt

Dòng có `id` bắt đầu bằng `EXAMPLE` được bỏ qua.

Trong env của dự án:

```powershell
.\.venv\Scripts\Activate.ps1
python tools\validate_locale.py
```

Chưa có `.venv` thì tạo bằng `py -3.14 -m venv .venv` ở thư mục gốc repo. Script trả về mã 0 khi file hợp lệ, mã 1 khi có lỗi.
