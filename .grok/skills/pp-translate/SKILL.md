---
name: pp-translate
description: >
  Add or edit Vietnamese lines in locale/vi/strings.csv for PATAPON 1+2 REPLAY.
  Use when translating, reviewing a line, changing glossary or style, when the
  user says việt hóa or dịch chuỗi, or runs /pp-translate.
---

# Dịch một chuỗi

Luật luôn bật nằm ở `CLAUDE.md`. Việc này vẫn đi qua `/pp-task-workflow`: có issue và có nhánh trước khi sửa CSV.

Chưa dịch hàng loạt khi bộ instructions chưa nằm trên `main`.

## Đọc trước

- `docs/pipeline.md`
- `docs/thuat-ngu.md`
- `docs/van-phong.md`

Không chép bảng thuật ngữ vào skill này. Sửa tên riêng thì sửa `docs/thuat-ngu.md`.

## Sửa

- File chính là `locale/vi/strings.csv`.
- Giữ `id` lấy từ bản trích. Không bịa `id` cho câu thật.
- `source` là câu tiếng Anh. `vi` là câu tiếng Việt.
- Giữ nguyên placeholder, thẻ rich text, và `\n`.
- `status` chỉ là `todo`, `draft`, `review`, hoặc `done`.
- Xóa dòng `EXAMPLE` khi bắt đầu nhập câu thật.
- Không commit bundle, `extract/`, hay thư mục cài game.

## Kiểm tra

```powershell
.\.venv\Scripts\python.exe tools\validate_locale.py
```

Lệnh phải trả mã 0 trước commit.

## Ngoài phạm vi

- Đóng gói bundle. Việc đó cần issue riêng. `docs/pipeline.md` chỉ nói thư mục local.
- Phim trong `StreamingAssets/P1/Movie` và `StreamingAssets/P2/Movie`.
