---
name: vh-add-game
description: >
  Add a new PC game folder under games/<id>/ for Vietnamese localization.
  Use when the user wants to start localizing another game, or runs /vh-add-game.
---

# Thêm một game

Luật luôn bật nằm ở `CLAUDE.md`. Vẫn đi qua `/vh-task-workflow`.

Không sửa `locale/`, thuật ngữ, hoặc văn phong của game đã có, trừ khi issue nói rõ.

## Thư mục

Tạo `games/<id>/`. `<id>` là slug ngắn, chữ thường, không dấu, không khoảng trắng. Ví dụ có sẵn: `patapon12-replay`.

Trong đó:

- `README.md` nói game nào, nền tảng nào, trạng thái
- `config.example.json` với đường dẫn Steam và Epic để trống nếu chưa biết
- `docs/pipeline.md`, `docs/thuat-ngu.md`, `docs/van-phong.md`
- `locale/vi/strings.csv` với dòng tiêu đề `id,context,source,vi,status,note` và một dòng `EXAMPLE` nếu chưa có câu thật

Không copy nguyên docs của game khác. Chỉ mượn hình dạng file.

## Xong việc

- Thêm một dòng vào bảng game ở `README.md` gốc
- Chạy `python tools/validate_locale.py games/<id>`
- Không commit file cài game
