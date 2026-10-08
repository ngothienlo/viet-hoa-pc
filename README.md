# Việt hóa game PC

Repo private cho bản dịch tiếng Việt của game PC (Steam và Epic). Mỗi game một thư mục trong `games/`. Patapon là game đầu tiên, không phải tên repo.

Không chứa file cài game, bundle, video hay âm thanh.

## Games

| Thư mục | Game |
| --- | --- |
| `games/patapon12-replay/` | PATAPON 1+2 REPLAY |
| `games/potion-permit/` | Potion Permit |

Thêm game là thêm `games/<id>/`. Không để chuỗi của game này trong thư mục game kia.

## Cấu trúc

| Đường dẫn | Việc |
| --- | --- |
| `games/<id>/` | Bản dịch, thuật ngữ, văn phong, `patch/` và `game.json` của một game. |
| `launcher/` | Danh sách game, chọn thư mục cài, áp hoặc gỡ bản dịch. |
| `tools/validate_locale.py` | Kiểm tra CSV. Một game hoặc mọi game. |
| `tools/build_exe.py` | Đóng gói launcher thành `VietHoa.exe`. Xem `docs/technical/release.md`. |
| `requirements.txt` | Thư viện cho script vá game và bản exe. |
| `.githooks/` | Chặn commit và push thẳng lên `main`, `master`, `staging`. Bật bằng `git config core.hooksPath .githooks`. |
| `CLAUDE.md` | Luật luôn bật cho agent. Bản giống nằm ở `.github/copilot-instructions.md`. |

## Dùng bản exe

Tải `VietHoa.exe` ở mục Releases của repo, rồi mở file.

1. Chọn game, bấm «Dùng thư mục có sẵn» hoặc «Chọn thư mục» để trỏ tới thư mục cài.
2. Bấm «Áp dụng tiếng Việt». Lần đầu mất khoảng một phút: exe đọc bản cài của ngươi rồi tạo bản vá ngay trên máy.
3. Bấm «Chơi». Muốn trả game về như cũ thì bấm «Gỡ bản dịch».

Exe không chứa file nào của game. Bản cài phải là bản hợp pháp, đúng phiên bản mà bản dịch hỗ trợ. Gặp lỗi thì chạy `VietHoa.exe --build-only` rồi gửi file `%LOCALAPPDATA%\viet-hoa-pc\build.log`.

## Bắt đầu (cho người làm bản dịch)

```powershell
git config core.hooksPath .githooks
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python tools\validate_locale.py
python -m launcher.app
```

Env gắn với Python 3.14. Đổi phiên bản: cài bản đó, xóa `.venv`, rồi tạo lại, ví dụ `py -3.12 -m venv .venv`. Thư mục `.venv` không được commit.

## Bản quyền

Nội dung từng game thuộc nhà phát hành của game đó. Repo chỉ lưu bản dịch và ghi chú cho bản cài hợp pháp.
