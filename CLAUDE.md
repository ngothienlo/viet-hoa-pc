# CLAUDE.md - Việt hóa game PC

> This file is kept in sync with `.github/copilot-instructions.md`. When updating one, update the other. The two files must stay byte-identical.

## Quick Reference

```powershell
git config core.hooksPath .githooks
.\.venv\Scripts\Activate.ps1
python tools\validate_locale.py
python tools\validate_locale.py games\patapon12-replay
python -m launcher.app
python -m launcher.test_launcher
py -0p
```

PowerShell: tách lệnh bằng `;`. Không dùng `&&`.

Python của repo là 3.14, nằm trong `.venv` ở gốc. Tạo lại bằng `py -3.14 -m venv .venv`. Đổi phiên bản: cài bản đó, xóa `.venv`, rồi `py -3.x -m venv .venv`.

## Grok Skills

Việc làm theo nhu cầu nằm trong `.grok/skills/`. Không chép checklist đó vào file này. Gọi bằng `/tên` hoặc để Grok khớp `description` của skill. Mục lục: `docs/technical/grok-skills.md`.

| Skill | Use |
| --- | --- |
| `/vh-task-workflow` | Issue → nhánh → docs → kiểm tra → commit → hỏi trước khi push → PR → review → hỏi trước khi merge |
| `/vh-translate` | Sửa CSV của một game trong `games/<id>/` |
| `/vh-add-game` | Thêm `games/<id>/` cho một game mới |
| `/vh-font` | Sửa ô vuông, lẫn font, thiếu dấu trong font của một game |

## Git Workflow (MANDATORY)

### Vòng làm việc

1. **Tạo GitHub issue** trước khi tạo nhánh hoặc sửa file
2. **Tạo nhánh** từ `main`: `feature/<tên>`, `fix/<tên>`, hoặc `docs/<tên>`
3. **Sửa và kiểm tra** trên nhánh đó
4. **Cập nhật docs** — việc của một game ở `games/<id>/docs`, quy trình agent ở `/docs/technical`
5. **Commit** trên nhánh, kèm `closes #N` hoặc `refs #N`
6. **Hỏi người dùng** trước khi push và mở PR
7. **Review** đăng trên PR, không chỉ trong chat
8. **Hỏi người dùng** trước khi merge

### Nội dung issue và PR

- Issue nói rõ vấn đề, vì sao cần làm, và phạm vi bị ảnh hưởng, kể cả game nào
- Issue lỗi có bước tái hiện, kết quả đúng, và kết quả đang thấy
- Mọi issue và PR có mục `Technical Solution`: cách làm, file, đánh đổi, việc để sau
- PR nói cái đã làm, chỗ khác với issue, và vì sao chọn cách đó
- Dùng GitHub Markdown. Không escape dấu backtick trong nội dung issue hoặc PR
- PR gồm: Problem, Technical Solution, Files Changed (một dòng mỗi file), Testing

### Luật

1. **Không commit thẳng lên `main`.** Mọi thay đổi đi qua nhánh và PR. Hook trong `.githooks/` chặn commit và push thẳng lên `main`, `master`, `staging`; bật bằng `git config core.hooksPath .githooks`. Không dùng `--no-verify`. Chi tiết: `docs/technical/git-hooks.md`.
2. **Một game một thư mục** `games/<id>/`. Không để chuỗi, thuật ngữ, hoặc config của game này trong thư mục game kia.
3. **Không commit** thư mục cài game, `*.bundle`, `*.assets`, `*.usme`, `global-metadata.dat`, `GameAssembly.dll`, `extract/`, `build/`, `dist/`, `config.json`, `.venv/`.
4. Trước `checkout --`, `reset --hard`, `clean -fd`, hoặc `stash drop`: chạy `git status`. Không xóa `extract/` hoặc `config.json` đang chưa commit.
5. Không viết lại lịch sử `main` để giấu các commit thẳng ở giai đoạn dựng repo.

## Project

Repo private để việt hóa nhiều game PC (Steam và Epic). Tên repo không gắn với một game. Game hiện có nằm trong `games/`. Game đầu tiên là `games/patapon12-replay/`.

Sự thật của từng game nằm trong thư mục game đó:

- Chữ nằm ở đâu: `games/<id>/docs/pipeline.md`
- Tên riêng: `games/<id>/docs/thuat-ngu.md`
- Văn phong: `games/<id>/docs/van-phong.md`
- Font: `games/<id>/docs/font.md`, cách làm chung ở `docs/technical/unity-tmp-font.md`
- Chuỗi: `games/<id>/locale/vi/strings.csv`

Công cụ dùng chung nằm ở `tools/validate_locale.py` và `launcher/`. Launcher đọc `games/<id>/game.json`, áp file trong `games/<id>/patch/`. Chi tiết: `docs/technical/launcher.md`.

## Conventions

- Nguồn dịch là tiếng Anh, trừ khi docs của game đó chọn nguồn khác.
- Giữ placeholder, thẻ rich text, và `\n`.
- Cột CSV, đúng thứ tự: `id`, `context`, `source`, `vi`, `status`, `note`.
- `status` chỉ được là `todo`, `draft`, `review`, `done`.
- Dòng có `id` bắt đầu bằng `EXAMPLE` là mẫu định dạng. Xóa trước khi dịch thật.
- Docs và ghi chú trong repo này viết bằng tiếng Việt.
- Danh xưng và tên riêng theo docs của đúng game. Không lấy quy ước Patapon áp sang game khác.

## Validation

Khi đổi CSV hoặc `tools/validate_locale.py`, lệnh này phải qua trước PR:

```powershell
.\.venv\Scripts\python.exe tools\validate_locale.py
```

Khi đổi `.githooks/`, chạy thêm `.\.venv\Scripts\python.exe tools\test_git_hooks.py`.

Khi đổi `launcher/`, chạy thêm:

```powershell
.\.venv\Scripts\python.exe -m launcher.test_launcher
```

Chỉ đụng một game thì chạy validator với đường dẫn, ví dụ `games\patapon12-replay`. Thay đổi chỉ gồm docs vẫn chạy validator không tham số một lần và ghi kết quả vào PR.

## Documentation

Đọc docs của đúng game trước khi đổi cách dịch game đó.

Sau mỗi thay đổi:

1. Pipeline, thuật ngữ, văn phong của game → `games/<id>/docs`
2. Quy trình agent → `/docs/technical`
3. Ghi cái đã đổi và cái bị ảnh hưởng
4. Sửa `CLAUDE.md` thì chép cùng nội dung sang `.github/copilot-instructions.md` trong cùng commit
