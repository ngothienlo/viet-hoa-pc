# Việt hóa game PC

Bản dịch tiếng Việt cho game PC (Steam và Epic), làm bởi người hâm mộ, phi thương mại. Mỗi game một thư mục trong `games/`. Kèm launcher `VietHoa.exe` để áp và gỡ bản dịch.

Không chứa file cài game, bundle, video hay âm thanh. Xem mục [Bản quyền và miễn trừ trách nhiệm](#bản-quyền-và-miễn-trừ-trách-nhiệm).

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
2. Bấm «Áp dụng tiếng Việt». Lần đầu mất khoảng một phút: exe đọc bản cài của bạn rồi tạo bản vá ngay trên máy.
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

## Bản quyền và miễn trừ trách nhiệm

Đây là dự án của người hâm mộ, phi thương mại. Dự án **không liên kết, không được tài trợ hay xác nhận** bởi nhà phát triển hay nhà phát hành của bất kỳ game nào trong repo.

**Chủ sở hữu.** Tên game, nhân vật, hình ảnh, âm thanh và chữ gốc của game thuộc chủ sở hữu tương ứng:

| Game | Chủ sở hữu |
| --- | --- |
| PATAPON 1+2 REPLAY | Bandai Namco Entertainment Inc., Sony Interactive Entertainment |
| Potion Permit | MassHive Media, PQube |

**Repo chứa gì.**
- Có: bản dịch tiếng Việt, ghi chú thuật ngữ và văn phong, script tạo bản vá, launcher.
- Chữ gốc tiếng Anh: cột `source` trong `locale/vi/strings.csv`. Chữ này chỉ để đối chiếu khi dịch và để kiểm bản vá khớp đúng phiên bản game.
- Không có: file cài game, bundle, texture, font gốc, video, âm thanh.
- Bản vá được tạo ngay trên máy người chơi, từ bản cài của chính người đó.

**Cần sở hữu game.** Bản dịch chỉ dùng được với bản cài **hợp pháp**, mua trên Steam hoặc Epic. Không dùng bản dịch hay launcher cho bản crack, và không chia sẻ bản dịch kèm file game.

**Không bảo đảm.** Bản dịch và công cụ được cung cấp nguyên trạng, không kèm bảo đảm nào. Launcher sao lưu file gốc trước khi vá và gỡ được bất cứ lúc nào. Dù vậy, bạn nên tự sao lưu file save trước khi áp. Người làm bản dịch không chịu trách nhiệm về hư hỏng dữ liệu, lỗi game hay mất tiến trình. Nếu game cập nhật, hãy gỡ bản dịch trước rồi chờ bản phát hành mới.

**Yêu cầu gỡ.** Nếu bạn là chủ sở hữu và không muốn nội dung của mình xuất hiện ở đây, hãy mở một issue trong repo. Phần liên quan sẽ được gỡ ngay.
