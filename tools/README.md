# Công cụ

`validate_locale.py` kiểm tra `locale/vi/strings.csv` của từng game. Chạy từ thư mục gốc repo.

Một game:

```powershell
python tools\validate_locale.py games\patapon12-replay
```

Mọi game trong `games/`:

```powershell
python tools\validate_locale.py
```

Script báo:

- thiếu file CSV hoặc sai thứ tự cột
- `id` trống hoặc trùng
- `status` ngoài `todo`, `draft`, `review`, `done`
- dòng `review` hoặc `done` nhưng ô `vi` trống
- lệch placeholder, thẻ rich text hoặc `\n` giữa câu gốc và câu Việt

Dòng có `id` bắt đầu bằng `EXAMPLE` được bỏ qua. Mã thoát 0 khi mọi game được chỉ định đều hợp lệ, mã 1 khi có lỗi.

`test_git_hooks.py` kiểm tra hook trong `.githooks/` bằng repo tạm. Xem `docs/technical/git-hooks.md`.
