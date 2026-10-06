# Launcher

## Đã làm

Cửa sổ dùng chung cho mọi game trong `games/`. Người dùng chọn game, trỏ thư mục cài, áp bản dịch hoặc gỡ.

Mở từ thư mục gốc repo:

```powershell
python -m launcher.app
```

## Cách áp

- Mỗi game có `games/<id>/game.json`: `id`, `title`, `summary`, `exe`, `detect`.
- File đè nằm trong `games/<id>/patch/`, giữ đường dẫn tương đối với thư mục cài. File tên bắt đầu bằng dấu chấm bị bỏ qua.
- Đường dẫn gợi ý lấy từ `installs` trong `config.example.json` khi thư mục đó có đủ file `detect`.
- Đường dẫn đã chọn ghi ở `%LOCALAPPDATA%\viet-hoa-pc\state.json`. Không commit.
- Khi áp, file gốc được chép vào `%LOCALAPPDATA%\viet-hoa-pc\backups\<id>\<thời điểm>\`. Gỡ thì trả lại. File nào do bản dịch thêm vào thì bị xóa.
- Áp lần nữa thì gỡ trước, rồi copy lại. Bản sao lưu không lấy file đã vá làm bản gốc.
- `patch/` trống thì không ghi gì vào thư mục cài. Nút Áp dụng tắt.

## Ảnh hưởng

Patapon có `game.json` và `patch/` trống. Chọn thư mục và Chơi dùng được. Áp dụng chờ khi có file trong `patch/`.

Game mới cần `game.json` và `patch/`. Xem `/vh-add-game`.
