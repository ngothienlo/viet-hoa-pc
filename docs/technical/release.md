# Phát hành

## Đã làm

Bản phát hành là một file `VietHoa.exe` trên GitHub Release (#17). Exe chứa launcher, file đã commit trong `games/` (CSV, `fonts.json`, script vá) và thư viện Python. Exe không chứa file nào của game: bản vá được tạo trên máy người chơi lúc bấm Áp dụng (xem `docs/technical/launcher.md`).

Số phiên bản nằm ở `launcher/__init__.py` (`__version__`). Số này hiện trên thanh tiêu đề cửa sổ và trong thông tin file của exe.

## Build exe

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools\build_exe.py --ui-test
```

`tools/build_exe.py` làm theo thứ tự:

1. Dò cả cây phụ thuộc của UnityPy, TypeTreeGeneratorAPI, freetype-py, pycryptodome (đọc metadata của từng gói), rồi `--collect-all` mọi package trong cây đó. Script vá được nạp lúc chạy, nên PyInstaller không tự thấy các thư viện này. Danh sách gõ tay từng thiếu `fmod_toolkit`, `pyfmodex`, `archspec`; dò tự động thì nâng phiên bản UnityPy không phải sửa tay.
2. Chép file `git ls-files games` vào stage. Phải commit trước khi build.
3. Chạy PyInstaller một file, kèm thông tin phiên bản. Stage và thư mục làm việc nằm trong thư mục tạm của Windows, ngoài repo, vì OneDrive khóa file lúc đồng bộ.
4. Ký số nếu có chứng chỉ (xem mục Ký số).
5. Ghi `dist/VietHoa.exe.sha256`.
6. Chạy `VietHoa.exe --build-only` trên bản cài đã chọn trong launcher. Mã thoát khác 0 thì dừng và in cuối `build.log`.
7. Có `--ui-test` thì chạy thêm `VietHoa.exe --ui-test`: mở cửa sổ thật, bấm nút Áp dụng, chờ build và chép xong, chụp `ui-test.png`. Bước này áp thật lên game.

`--skip-check` bỏ bước 6 và 7, dùng khi máy build không có bản cài game.

Thư viện nặng không dùng (torch, sympy…) bị loại bằng `--exclude-module`. Không loại thì exe vượt 200 MB.

## Kiểm tra trước khi phát hành

- `validate_locale.py`, `launcher.test_launcher`, test của game.
- `tools\build_exe.py --ui-test` chạy qua hết. Xem `%LOCALAPPDATA%\viet-hoa-pc\ui-test.png`: trạng thái «Đã áp … file», nhãn game «Đã áp dụng».
- Muốn so với bản Python: chạy `games\<id>\tools\build_patch.py <cài> <ra>`, rồi so từng file với `%LOCALAPPDATA%\viet-hoa-pc\build\<id>\`. Hai bản phải giống từng byte.

## Ký số

Exe chưa ký thì Windows SmartScreen cảnh báo lần đầu mở («Windows protected your PC» → More info → Run anyway). Muốn hết cảnh báo cần chứng chỉ code signing (OV hoặc EV, hoặc dịch vụ như Azure Trusted Signing). Chứng chỉ tự ký không giúp gì.

Có chứng chỉ thì đặt hai biến môi trường trước khi build, `build_exe.py` sẽ gọi `signtool` (Windows SDK):

```powershell
$env:VH_SIGN_PFX = "C:\duong\dan\chung-chi.pfx"
$env:VH_SIGN_PASSWORD = "<mật khẩu của chứng chỉ>"
```

Không commit file `.pfx` hay mật khẩu. Chưa ký thì release ghi kèm SHA-256 để người chơi tự kiểm file.

## Tạo release

```powershell
gh release create v1.0.0 dist\VietHoa.exe dist\VietHoa.exe.sha256 --title "v1.0" --notes-file <ghi chú>
```

Tag tạo trên `main`, sau khi PR đã merge. Hook `pre-push` chỉ chặn nhánh, không chặn tag.

## Các bản đã phát hành

| Bản | Issue | Nội dung |
| --- | --- | --- |
| v1.0 | #17 | PATAPON 1+2 REPLAY |
| v1.1.0 | #31 | Thêm Potion Permit: 9.661 câu, font pixel có chữ Việt. Kiểm chính tả bằng `tools/check_vietnamese.py` |

Bản mới có thêm game hoặc tính năng thì tăng số giữa. Bản chỉ sửa lỗi dịch thì tăng số cuối.

## Giới hạn

- `fonts.json` gắn với một bản game (sha1 của `catalog.json`). Game cập nhật thì exe báo không khớp, không vá. Khi đó quét lại font, build và phát hành bản mới.
