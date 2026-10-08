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
- `game.json` với `id`, `title`, `summary`, `exe`, `detect`, và `build` nếu bản vá phải tạo từ bản cài của người chơi (gần như mọi game Unity: không đưa file game vào repo hay vào exe). Xem `docs/technical/launcher.md`, mục Bước build
- `tools/extract_strings.py` (trích câu gốc vào CSV) và `tools/build_patch.py` (tạo bản vá). Mẫu: `games/potion-permit/tools/`
- `config.example.json` với đường dẫn Steam và Epic để trống nếu chưa biết
- `patch/` để trống. File trong này là bản đè, launcher sẽ copy vào thư mục cài
- `docs/pipeline.md`, `docs/thuat-ngu.md`, `docs/van-phong.md`
- `locale/vi/strings.csv` với dòng tiêu đề `id,context,source,vi,status,note` và một dòng `EXAMPLE` nếu chưa có câu thật

Không copy nguyên docs của game khác. Chỉ mượn hình dạng file.

## Xong việc

- Thêm một dòng vào bảng game ở `README.md` gốc
- Chạy `python tools/validate_locale.py games/<id>`
- Không commit file cài game
