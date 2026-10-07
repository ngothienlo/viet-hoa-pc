# Phát hành

## Đã làm

Bản phát hành là một file `VietHoa.exe` trên GitHub Release (#17). Exe chứa launcher, file đã commit trong `games/` (CSV, `fonts.json`, script vá) và thư viện Python. Exe không chứa file nào của game: bản vá được tạo trên máy người chơi lúc bấm Áp dụng (xem `docs/technical/launcher.md`).

## Build exe

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools\build_exe.py
```

- Exe ghi ra `dist/VietHoa.exe`. `dist/` không được commit.
- Chỉ file `git ls-files games` được gói vào exe, nên phải commit trước khi build.
- Stage và thư mục làm việc của PyInstaller nằm trong thư mục tạm của Windows, ngoài repo. Repo nằm trong OneDrive, mà OneDrive khóa file lúc đồng bộ.
- Script vá được nạp lúc chạy, nên PyInstaller không tự thấy thư viện của chúng. `tools/build_exe.py` sinh `vh_deps.py` import sẵn các thư viện đó, rồi `--collect-all` cho thư viện có DLL hoặc file dữ liệu: UnityPy, TypeTreeGeneratorAPI, texture2ddecoder, etcpak, astc_encoder, freetype, fmod_toolkit, pyfmodex, archspec. Thiếu một gói thì exe chạy được nửa chừng rồi báo thiếu DLL.
- Thư viện nặng không dùng (torch, sympy…) bị loại bằng `--exclude-module`. Không loại thì exe vượt 200 MB.

## Kiểm tra trước khi phát hành

1. `validate_locale.py`, `launcher.test_launcher`, test của game.
2. `dist\VietHoa.exe --build-only`, rồi đọc `%LOCALAPPDATA%\viet-hoa-pc\build.log`. Mã thoát phải là 0, và mọi font phải báo «đủ».
3. So file trong `%LOCALAPPDATA%\viet-hoa-pc\build\<id>\` với bản build bằng Python (`games\<id>\tools\build_patch.py <cài> <ra>`). Hai bản phải giống từng byte.
4. Mở exe, xem cửa sổ «Việt hóa» hiện lên.

## Tạo release

```powershell
gh release create v1.0.0 dist\VietHoa.exe --title "v1.0" --notes-file <ghi chú>
```

Tag tạo trên `main`, sau khi PR đã merge. Hook `pre-push` chỉ chặn nhánh, không chặn tag.

## Giới hạn

- `fonts.json` gắn với một bản game (sha1 của `catalog.json`). Game cập nhật thì exe báo không khớp, không vá. Khi đó quét lại font, rồi build và phát hành bản mới.
- Exe chưa ký số, nên Windows SmartScreen có thể cảnh báo lần đầu mở.
