---
name: vh-font
description: >
  Fix Vietnamese glyphs in a game's fonts: tofu boxes (□), mixed fonts inside
  one line, missing diacritics, or a font patch that must be redone after a game
  update. Use when the user shows a screenshot with broken Vietnamese text, says
  lỗi font, ô vuông, lẫn font, thiếu dấu, or runs /vh-font.
---

# Sửa font chữ Việt

Luật luôn bật nằm ở `CLAUDE.md`. Việc này vẫn đi qua `/vh-task-workflow`: có issue và có nhánh trước khi sửa.

## Đọc trước

- `games/<id>/docs/font.md`: bản đồ font, cách vá, lệnh, bẫy của đúng game đó
- `games/<id>/tools/font/fonts.json`: danh sách font đã quét. Đừng quét lại game nếu file này còn khớp bản game.
- `docs/technical/unity-tmp-font.md`: cách làm chung cho Unity TextMesh Pro

Game chưa có `docs/font.md` thì đọc bản của `patapon12-replay` làm mẫu, rồi viết bản riêng cho game đó.

## Làm

1. Từ ảnh chụp, tìm câu trong `locale/vi/strings.csv` để có `id`, rồi ghi `id` vào issue.
2. Xem `fonts.json`: font nào vẽ chữ đó, font đó vá theo luật nào. Chưa chắc font nào thì vẽ atlas gốc ra ảnh rồi so với ảnh chụp. Không đoán theo tên.
   Mặc định giữ nét gốc (ghép dấu). Chỉ thay font khi font gốc thiếu chữ cái để ghép.
3. Font chưa khớp luật, hoặc game vừa cập nhật thì chạy `inventory.py`, rồi sửa `RULES`.
4. Chạy script vá font của game. Script phải tự kiểm tra (`--check`) trước khi áp.
5. Vẽ ảnh xem thử (`preview.py`) và tự xem ảnh trước khi báo xong.
6. Nhờ người dùng chụp lại đúng chỗ trong game. Ghi kết quả vào `docs/font.md`, mục «Chưa kiểm».

## Không làm

- Không thêm font fallback để vá thiếu chữ.
- Không vá chồng lên file đã vá. Luôn đọc file gốc.
- Không commit atlas, `.assets`, bundle hay file TTF.
