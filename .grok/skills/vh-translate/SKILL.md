---
name: vh-translate
description: >
  Edit Vietnamese lines for one game under games/<id>/locale/vi/strings.csv.
  Use when translating or reviewing a line, when the user says việt hóa or dịch
  chuỗi and names a game, or runs /vh-translate.
---

# Dịch một chuỗi

Luật luôn bật nằm ở `CLAUDE.md`. Việc này vẫn đi qua `/vh-task-workflow`: có issue và có nhánh trước khi sửa CSV.

Chỉ sửa một game trong một việc. Game khác để nguyên.

## Đọc trước

Trong `games/<id>/`:

- `docs/pipeline.md`
- `docs/thuat-ngu.md`
- `docs/van-phong.md`

Không chép bảng thuật ngữ vào skill này. Không lấy quy ước của game khác.

## Sửa

- File chính là `games/<id>/locale/vi/strings.csv`.
- Giữ `id` lấy từ bản trích của game đó. Không bịa `id` cho câu thật.
- `source` là câu nguồn. `vi` là câu tiếng Việt.
- Giữ nguyên placeholder, thẻ rich text, và `\n`.
- `status` chỉ là `todo`, `draft`, `review`, hoặc `done`.
- Xóa dòng `EXAMPLE` khi bắt đầu nhập câu thật.
- Không commit bundle, `extract/`, hay thư mục cài game.

## Kiểm tra

```powershell
.\.venv\Scripts\python.exe tools\validate_locale.py games\<id>
.\.venv\Scripts\python.exe tools\check_vietnamese.py games\<id>
```

Hai lệnh phải trả mã 0 trước commit. `check_vietnamese.py` bắt âm tiết sai cấu trúc, dấu đặt sai chữ, dấu cách thừa. Nó không bắt được nhầm s/x, ch/tr, hỏi/ngã, nên vẫn phải đọc lại câu.

## Ngoài phạm vi

- Đóng gói bundle. Việc đó cần issue riêng của đúng game.
- Thêm game mới. Dùng `/vh-add-game`.
