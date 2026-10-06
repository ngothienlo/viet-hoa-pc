# Grok project skills

## Đã làm

Skill của repo nằm trong `.grok/skills/`. Đó là việc làm theo nhu cầu. Luật luôn bật nằm ở `CLAUDE.md`, bản giống từng byte ở `.github/copilot-instructions.md`. Sự thật về chữ và văn phong nằm ở `/docs`.

Grok nạp skill khi người dùng gõ `/<tên>` hoặc khi câu khớp `description`.

## Đã đổi

| Skill | Việc |
| --- | --- |
| `pp-task-workflow` | Issue → nhánh từ `main` → docs → `validate_locale.py` → commit → hỏi trước khi push → PR → review trên PR → hỏi trước khi merge |
| `pp-translate` | Sửa `locale/vi/strings.csv` sau khi đọc pipeline, thuật ngữ, văn phong |

Skill trỏ tới docs có sẵn. Không chép bảng tên riêng, không chép nguyên luật git trong `CLAUDE.md`.

## Ảnh hưởng

- Phiên agent trong repo này dùng `/pp-task-workflow` cho mọi việc, và `/pp-translate` khi đụng câu dịch
- Không đổi file game, bundle, hay nội dung `locale/vi/strings.csv`
- Chưa có skill trích hoặc đóng gói bundle. Việc đó chờ issue riêng

## Cách gọi

```text
/pp-task-workflow
/pp-translate
```
