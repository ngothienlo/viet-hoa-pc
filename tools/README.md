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
- lệch placeholder, thẻ rich text hoặc `\n` giữa câu gốc và câu Việt. Placeholder (`{…}`, `%s`) được đổi chỗ vì trật tự từ tiếng Việt khác tiếng Anh; thẻ và `\n` phải giữ thứ tự.

Dòng có `id` bắt đầu bằng `EXAMPLE` được bỏ qua. Mã thoát 0 khi mọi game được chỉ định đều hợp lệ, mã 1 khi có lỗi.

`check_vietnamese.py` kiểm chính tả cột `vi` theo cấu trúc âm tiết tiếng Việt, không dùng từ điển:

```powershell
python tools\check_vietnamese.py games\potion-permit
python tools\check_vietnamese.py games\potion-permit --words
```

- Báo lỗi (mã thoát 1) khi:
  - âm tiết có dấu nhưng sai âm đầu hoặc vần;
  - sai quy tắc c/k, g/gh, ng/ngh;
  - vần tắc (p, t, c, ch) đi với dấu khác sắc và nặng;
  - dấu thanh đặt sai chữ, theo kiểu truyền thống: «hòa, khỏe, thủy, loại»;
  - chữ không ở dạng NFC;
  - câu Việt có dấu cách thừa nhiều hơn câu gốc.
- Bỏ qua thán từ kéo dài («Hừmmm», «Méooo») và chữ lắp bắp.
- `--words` in thêm các từ viết thường, không dấu, không phải tiếng Việt. Thường là tên riêng hay từ mượn, nhưng cũng có thể là tiếng Anh còn sót.
- Không bắt được nhầm s/x, ch/tr, d/gi/r, l/n, hỏi/ngã. Những lỗi này phải đọc lại câu mới thấy.

`test_git_hooks.py` kiểm tra hook trong `.githooks/` bằng repo tạm. Xem `docs/technical/git-hooks.md`.
