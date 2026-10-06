---
name: pp-task-workflow
description: >
  Run the PATAPON 1+2 REPLAY localization git workflow: GitHub issue with
  Technical Solution, branch from main, docs, validate_locale.py, commit with
  closes #N, ask before push, PR, post the review on the PR, ask before merge.
  Use when starting a change, when the user says làm đúng quy trình, tạo ticket,
  mở PR, or runs /pp-task-workflow.
---

# Patapon task workflow

Luật luôn bật nằm ở `CLAUDE.md`. Skill này chỉ là thứ tự việc.

PowerShell: tách lệnh bằng `;`. Không dùng `&&`.

## 1. Issue trước

Tạo GitHub issue trước khi tạo nhánh hoặc sửa file.

Thân issue dùng GitHub Markdown, không escape backtick:

- Vấn đề, vì sao cần làm, phạm vi
- Lỗi: bước tái hiện, kết quả đúng, kết quả đang thấy
- Mục `Technical Solution`: cách làm, file, đánh đổi, việc để sau

## 2. Nhánh từ main

`feature/<tên>`, `fix/<tên>`, hoặc `docs/<tên>`. Không commit trên `main`.

Trước `checkout --`, `reset --hard`, `clean -fd`, hoặc `stash drop`: chạy `git status`. Không xóa `extract/` hoặc `config.json` chưa commit.

## 3. Sửa

- Đọc file liên quan trong `/docs` trước khi đổi cách dịch.
- Dịch chuỗi thì dùng `/pp-translate`. Không chép checklist đó vào đây.
- Không đưa bundle, thư mục cài game, `extract/`, `build/`, hay `config.json` vào git.

## 4. Kiểm tra

Chạy trước khi báo xong:

```powershell
.\.venv\Scripts\python.exe tools\validate_locale.py
```

Lệnh phải trả mã 0. Đổi chỉ docs vẫn chạy một lần và ghi kết quả vào PR.

## 5. Docs

- Pipeline, thuật ngữ, văn phong → `/docs`
- Quy trình agent → `/docs/technical`
- Ghi cái đã đổi và cái bị ảnh hưởng
- Sửa `CLAUDE.md` thì giữ `.github/copilot-instructions.md` giống từng byte

## 6. Commit trên nhánh

Kèm `closes #N` hoặc `refs #N`.

## 7. Hỏi trước khi push và mở PR

Không push, không mở PR, cho đến khi người dùng đồng ý.

Thân PR gồm Problem, Technical Solution, Files Changed, Testing. Dùng `.github/PULL_REQUEST_TEMPLATE.md`.

## 8. Review trên PR

Đăng review lên PR, không chỉ ghi trong chat. Nói đúng chỗ nào, chỗ dễ lệch, và test nào đã chạy. Tách lỗi do PR này với lỗi có sẵn từ trước.

## 9. Hỏi trước khi merge
