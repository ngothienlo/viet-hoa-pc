# Việt hóa game PC

Repo private cho bản dịch tiếng Việt của game PC (Steam và Epic). Mỗi game một thư mục trong `games/`. Patapon là game đầu tiên, không phải tên repo.

Không chứa file cài game, bundle, video hay âm thanh.

## Games

| Thư mục | Game |
| --- | --- |
| `games/patapon12-replay/` | PATAPON 1+2 REPLAY |

Thêm game là thêm `games/<id>/`. Không để chuỗi của game này trong thư mục game kia.

## Cấu trúc

| Đường dẫn | Việc |
| --- | --- |
| `games/<id>/` | Bản dịch, thuật ngữ, văn phong, `patch/` và `game.json` của một game. |
| `launcher/` | Danh sách game, chọn thư mục cài, áp hoặc gỡ bản dịch. |
| `tools/validate_locale.py` | Kiểm tra CSV. Một game hoặc mọi game. |
| `CLAUDE.md` | Luật luôn bật cho agent. Bản giống nằm ở `.github/copilot-instructions.md`. |

## Bắt đầu

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python tools\validate_locale.py
python -m launcher.app
```

Env gắn với Python 3.14. Đổi phiên bản: cài bản đó, xóa `.venv`, rồi tạo lại, ví dụ `py -3.12 -m venv .venv`. Thư mục `.venv` không được commit.

## Bản quyền

Nội dung từng game thuộc nhà phát hành của game đó. Repo chỉ lưu bản dịch và ghi chú cho bản cài hợp pháp.
