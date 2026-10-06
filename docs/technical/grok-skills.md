# Grok project skills

## Đã làm

Skill của repo nằm trong `.grok/skills/`. Đó là việc làm theo nhu cầu. Luật luôn bật nằm ở `CLAUDE.md`, bản giống từng byte ở `.github/copilot-instructions.md`. Việc của từng game nằm ở `games/<id>/`.

Grok nạp skill khi người dùng gõ `/<tên>` hoặc khi câu khớp `description`.

## Đã đổi

| Skill | Việc |
| --- | --- |
| `vh-task-workflow` | Issue → nhánh từ `main` → docs → `validate_locale.py` → commit → hỏi trước khi push → PR → review trên PR → hỏi trước khi merge |
| `vh-translate` | Sửa CSV của một game, không đụng game khác |
| `vh-add-game` | Tạo `games/<id>/` mới |

Skill `pp-task-workflow` và `pp-translate` đã bỏ. Hai skill đó gắn repo với Patapon.

Skill trỏ tới docs của đúng game. Không chép bảng tên riêng, không chép nguyên luật git trong `CLAUDE.md`.

## Ảnh hưởng

- Phiên agent dùng `/vh-task-workflow` cho mọi việc
- Thêm game không sửa thư mục game đã có
- Không đổi file cài game hay bundle

## Cách gọi

```text
/vh-task-workflow
/vh-translate
/vh-add-game
```
