# Launcher

## Đã làm

Cửa sổ dùng chung cho mọi game trong `games/`. Người dùng chọn game, trỏ thư mục cài, áp bản dịch hoặc gỡ.

Mở từ thư mục gốc repo:

```powershell
python -m launcher.app
```

## Cách áp

- Mỗi game có `games/<id>/game.json`: `id`, `title`, `summary`, `exe`, `detect`, và `build` nếu game tạo bản vá trên máy.
- File đè nằm trong `games/<id>/patch/`, giữ đường dẫn tương đối với thư mục cài. File tên bắt đầu bằng dấu chấm bị bỏ qua.
- Đường dẫn gợi ý lấy từ `installs` trong `config.example.json` khi thư mục đó có đủ file `detect`.
- Đường dẫn đã chọn ghi ở `%LOCALAPPDATA%\viet-hoa-pc\state.json`. Không commit.
- Khi áp, file gốc được chép vào `%LOCALAPPDATA%\viet-hoa-pc\backups\<id>\<thời điểm>\`. Gỡ thì trả lại. File nào do bản dịch thêm vào thì bị xóa.
- Áp lần nữa thì gỡ trước, rồi copy lại. Bản sao lưu không lấy file đã vá làm bản gốc.
- `patch/` trống thì không ghi gì vào thư mục cài. Nút Áp dụng tắt.
- File ẩn bị bỏ qua, trừ `.doorstop_version`. Doorstop 4 cần đúng tên đó cạnh `winhttp.dll`. `.gitkeep` không được copy.

## Bước build (#17)

Game có khóa `build` trong `game.json` thì file vá không lấy từ `patch/`, mà được tạo ngay trên máy người chơi, từ bản cài của họ:

1. Bấm Áp dụng. Launcher nạp script `build` của game (đường dẫn tương đối với thư mục game) và gọi `build(thư mục cài, thư mục ra, log)` ở luồng nền. Cửa sổ hiện từng dòng tiến độ.
2. Script ghi file vá vào `%LOCALAPPDATA%\viet-hoa-pc\build\<id>\`, thư mục này được xóa sạch trước mỗi lần build.
3. Build xong thì launcher chép như cũ, có sao lưu.

Trước khi gọi script, launcher đặt biến môi trường `VH_STATE_DIR`. Script đọc file gốc qua bản sao lưu của launcher, nên build lại sau khi đã áp vẫn ra đúng kết quả.

Lỗi trong script (kể cả `SystemExit`) hiện lên cửa sổ, không làm launcher dừng.

Patapon dùng `tools/build_patch.py`. Script đó cần UnityPy và các thư viện trong `requirements.txt`.

`VietHoa.exe --build-only` (hoặc gọi `launcher.app.build_only()`) chỉ tạo bản vá cho mọi game đã chọn thư mục cài, không mở cửa sổ, không áp lên game, rồi ghi log vào `%LOCALAPPDATA%\viet-hoa-pc\build.log`. Dùng để kiểm tra bản exe, hoặc để người chơi gửi log khi báo lỗi.

`VietHoa.exe --ui-test` (hoặc `launcher.app.ui_test()`) mở cửa sổ thật, chọn game có bước build, bấm nút Áp dụng qua `invoke()`, chờ luồng nền xong, chụp cửa sổ. Ghi `ui-test.log` và `ui-test.png` vào thư mục state. Mã thoát 0 khi trạng thái cuối là «Đã áp …». Lệnh này áp thật lên game.

Biến môi trường `VH_STATE_DIR` (launcher đặt) và `VH_INSTALL_DIR`, `VH_PATCH_DIR` (script build đặt) chỉ tồn tại trong lúc build, xong thì trả lại giá trị cũ. Mỗi lần chỉ một build chạy (khóa trong `launcher/apply.py`), vì script build nạp lại module của game.

## Ảnh hưởng

Patapon có `game.json` với `build`, nên `patch/` của Patapon không được áp. Config BepInEx cũ trong đó đã xóa ở #17.

Game không có `build` vẫn áp `patch/` như cũ.

Game mới cần `game.json` và `patch/`. Xem `/vh-add-game`.
