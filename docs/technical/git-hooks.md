# Git hook

## Đã làm

Hook nằm trong repo, ở `.githooks/`, và được commit cùng code. Chúng chặn mọi thay đổi đi thẳng vào nhánh chính, để thay đổi chỉ vào `main` qua PR merge trên GitHub (luật 1 trong `CLAUDE.md`). Issue #14.

| Hook | Chặn |
| --- | --- |
| `pre-commit` | Commit khi đang đứng trên nhánh được bảo vệ |
| `pre-merge-commit` | Merge commit tạo trên máy khi đang đứng trên nhánh được bảo vệ |
| `pre-push` | Push lên nhánh được bảo vệ trên remote, kể cả `git push origin feature/x:main` |

Danh sách nhánh được bảo vệ (`main`, `master`, `staging`) nằm trong `.githooks/protected-branches.sh`. Muốn thêm nhánh thì sửa file đó.

## Bật

Git không tự chạy hook nằm trong repo. Mỗi bản clone phải bật một lần:

```powershell
git config core.hooksPath .githooks
```

Kiểm tra đã bật chưa:

```powershell
git config --get core.hooksPath
```

## Kiểm tra

`tools/test_git_hooks.py` dựng repo tạm và chạy commit, merge, push thật qua git. Repo này không bị đụng tới.

```powershell
.\.venv\Scripts\python.exe tools\test_git_hooks.py
```

Đổi file trong `.githooks/` thì chạy lệnh này trước PR.

## Giới hạn

- Hook chỉ chạy trên máy đã bật `core.hooksPath`.
- `git commit --no-verify` và `git push --no-verify` bỏ qua hook. Agent không dùng hai cờ này (`CLAUDE.md` không cho bỏ qua hook).
- Muốn chặn cả ở phía server thì bật branch protection cho `main` trong Settings → Branches của repo trên GitHub. Đó là cài đặt repo, do chủ repo bật.

## Ảnh hưởng

- Merge PR vẫn làm trên GitHub như cũ.
- Sau khi PR merge, kéo `main` về bằng `git pull` (fast-forward) vẫn chạy được, vì không tạo commit trên máy.
- Repo tạm trong test cần commit đầu tiên trên `main`, nên test dùng `--no-verify` riêng cho commit đó.
