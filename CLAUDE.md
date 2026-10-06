# CLAUDE.md - PATAPON 1+2 REPLAY Việt hóa

> This file is kept in sync with `.github/copilot-instructions.md`. When updating one, update the other. The two files must stay byte-identical.

## Quick Reference

```powershell
.\.venv\Scripts\Activate.ps1
python tools\validate_locale.py
py -0p
```

PowerShell: tách lệnh bằng `;`. Không dùng `&&`.

Python của repo là 3.14, nằm trong `.venv`. Tạo lại bằng `py -3.14 -m venv .venv`. Đổi phiên bản: cài bản đó, xóa `.venv`, rồi `py -3.x -m venv .venv`.

## Grok Skills

Việc làm theo nhu cầu nằm trong `.grok/skills/`. Không chép checklist đó vào file này. Gọi bằng `/tên` hoặc để Grok khớp `description` của skill. Mục lục: `docs/technical/grok-skills.md`.

| Skill | Use |
| --- | --- |
| `/pp-task-workflow` | Issue → nhánh → docs → kiểm tra → commit → hỏi trước khi push → PR → review → hỏi trước khi merge |
| `/pp-translate` | Sửa `locale/vi/strings.csv` theo thuật ngữ và văn phong |

## Git Workflow (MANDATORY)

### Vòng làm việc

1. **Tạo GitHub issue** trước khi tạo nhánh hoặc sửa file
2. **Tạo nhánh** từ `main`: `feature/<tên>`, `fix/<tên>`, hoặc `docs/<tên>`
3. **Sửa và kiểm tra** trên nhánh đó
4. **Cập nhật docs** — quy trình dịch ở `/docs`, quy trình agent ở `/docs/technical`
5. **Commit** trên nhánh, kèm `closes #N` hoặc `refs #N`
6. **Hỏi người dùng** trước khi push và mở PR
7. **Review** đăng trên PR, không chỉ trong chat
8. **Hỏi người dùng** trước khi merge

### Nội dung issue và PR

- Issue nói rõ vấn đề, vì sao cần làm, và phạm vi bị ảnh hưởng
- Issue lỗi có bước tái hiện, kết quả đúng, và kết quả đang thấy
- Mọi issue và PR có mục `Technical Solution`: cách làm, file đụng, đánh đổi, việc để sau
- PR nói cái đã làm, chỗ khác với issue, và vì sao chọn cách đó
- Dùng GitHub Markdown. Không escape dấu backtick trong nội dung issue hoặc PR
- PR gồm: Problem, Technical Solution, Files Changed (một dòng mỗi file), Testing

### Luật

1. **Không commit thẳng lên `main`.** Mọi thay đổi đi qua nhánh và PR.
2. **Không commit** thư mục cài game, `*.bundle`, `*.assets`, `*.usme`, `global-metadata.dat`, `GameAssembly.dll`, `extract/`, `build/`, `dist/`, `config.json`, `.venv/`.
3. Trước `checkout --`, `reset --hard`, `clean -fd`, hoặc `stash drop`: chạy `git status`. Không xóa `extract/` hoặc `config.json` đang chưa commit.
4. Không viết lại lịch sử `main` để giấu các commit thẳng ở giai đoạn dựng repo.
5. Chưa dịch hàng loạt khi bộ instructions này chưa nằm trên `main`. Sau đó mỗi đợt dịch vẫn có issue riêng.

## Project

Repo private để việt hóa **PATAPON 1+2 REPLAY** bản PC (Steam và Epic). Ngôn ngữ chính thức không có tiếng Việt. Chữ nằm trong asset bundle Addressables đã mã hóa. Phim `.usme` chưa nằm trong phạm vi cho đến khi có issue riêng.

Sự thật về game nằm trong docs, không chép vào file này:

- Chữ nằm ở đâu và bản vá local để ở đâu: `docs/pipeline.md`
- Tên riêng và nhịp trống giữ nguyên: `docs/thuat-ngu.md`
- Văn phong tiếng Việt: `docs/van-phong.md`
- Kiểm tra CSV: `tools/validate_locale.py`

## Conventions

- Nguồn dịch là tiếng Anh. Đối chiếu tiếng Nhật khi câu Anh tối nghĩa.
- Giữ `Pata`, `Pon`, `Don`, `Chaka` và các tên trong `docs/thuat-ngu.md`.
- Danh xưng người chơi là `Người Chỉ Huy` hoặc `ngươi`. Không dùng `bạn`.
- Cột CSV, đúng thứ tự: `id`, `context`, `source`, `vi`, `status`, `note`.
- `status` chỉ được là `todo`, `draft`, `review`, `done`.
- Dòng có `id` bắt đầu bằng `EXAMPLE` là mẫu định dạng. Xóa trước khi dịch thật.
- Docs và ghi chú trong repo này viết bằng tiếng Việt.

## Validation

Khi đổi `locale/vi/strings.csv` hoặc `tools/validate_locale.py`, lệnh này phải qua trước PR:

```powershell
.\.venv\Scripts\python.exe tools\validate_locale.py
```

Thay đổi chỉ gồm docs vẫn chạy lệnh đó một lần và ghi kết quả vào PR. Repo không có bộ test riêng.

## Documentation

Đọc file liên quan trong `/docs` trước khi đổi cách dịch.

Sau mỗi thay đổi, sửa đúng file sở hữu nội dung đó:

1. Pipeline, thuật ngữ, văn phong → `/docs`
2. Quy trình agent → `/docs/technical`
3. Ghi cái đã đổi và cái bị ảnh hưởng
4. Sửa `CLAUDE.md` thì chép cùng nội dung sang `.github/copilot-instructions.md` trong cùng commit
