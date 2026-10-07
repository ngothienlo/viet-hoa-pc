---
name: vh-task-workflow
description: >
  Run the PC-game Vietnamese localization workflow: GitHub issue with Technical
  Solution, branch from main, one game directory, validate_locale.py, commit
  with closes #N, ask before push, PR, post the review on the PR, ask before
  merge. Use when starting a change, when the user says làm đúng quy trình, tạo
  ticket, mở PR, or runs /vh-task-workflow.
---

# Task workflow

Luật luôn bật nằm ở `CLAUDE.md`. Skill này chỉ là thứ tự việc.

PowerShell: tách lệnh bằng `;`. Không dùng `&&`.

## 1. Issue trước

Tạo GitHub issue trước khi tạo nhánh hoặc sửa file.

Thân issue dùng GitHub Markdown, không escape backtick:

- Vấn đề, vì sao cần làm, phạm vi, và game nào nếu việc thuộc một game
- Lỗi: bước tái hiện, kết quả đúng, kết quả đang thấy
- Mục `Technical Solution`: cách làm, file, đánh đổi, việc để sau

## 2. Nhánh từ main

`feature/<tên>`, `fix/<tên>`, hoặc `docs/<tên>`. Không commit trên `main`.

Trước `checkout --`, `reset --hard`, `clean -fd`, hoặc `stash drop`: chạy `git status`. Không xóa `extract/` hoặc `config.json` chưa commit.

## 3. Sửa

- Việc của một game chỉ đụng `games/<id>/` của game đó, trừ công cụ dùng chung ở `tools/`.
- Dịch chuỗi thì dùng `/vh-translate`. Thêm game thì dùng `/vh-add-game`.
- Không đưa bundle, thư mục cài game, `extract/`, `build/`, hay `config.json` vào git.

## 4. Kiểm tra

Chạy trước khi báo xong:

```powershell
.\.venv\Scripts\python.exe tools\validate_locale.py
```

Lệnh phải trả mã 0. Đổi chỉ docs vẫn chạy một lần và ghi kết quả vào PR.

## 5. Docs

- Việc của một game → `games/<id>/docs`
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

Việc phát sinh sau khi đã đăng review:

- Lỗi do chính PR này gây ra: sửa trên PR này, rồi comment lên PR nói đã sửa gì.
- Lỗi có sẵn từ trước, hoặc việc mở rộng phạm vi: không đẩy thêm vào PR đã review, kể cả khi người dùng bảo «sửa luôn». Tạo issue mới, nhánh mới từ `main`, PR mới, rồi đi lại từ bước 1. Ghi trong issue mới là việc này phát sinh từ review của PR nào.

## 9. Hỏi trước khi merge

Trước khi merge, xem trạng thái PR (`gh pr view`). Nếu PR có commit mới sau lần review, hoặc sau lần người dùng đồng ý merge, thì hỏi lại người dùng.
