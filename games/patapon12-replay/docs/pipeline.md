# Pipeline

Thư mục game này là `games/patapon12-replay/`. Lệnh chạy từ thư mục gốc repo.

Làm trên bản cài hợp pháp. Steam và Epic dùng cùng cấu trúc thư mục cài.

## Chữ nằm ở đâu

- Catalog Addressables: `PATAPON12_REPLAY_Data/StreamingAssets/aa/catalog.json`
- Bundle: `PATAPON12_REPLAY_Data/StreamingAssets/aa/StandaloneWindows64/`
- Hội thoại, menu, tips và trợ giúp nằm trong `LocalizeData.asset` của P1, P1S, P2, P2S. `TipsData.asset` chỉ là tên sprite, không có câu.
- Bundle bị mã hóa bằng AES. Mật khẩu là `m_Hash` trong catalog. Salt là tên file bundle, bỏ đuôi. Giải xong thì UnityPy đọc được typetree của `LocalizeData`.
- Mục `Localize/<ngôn ngữ>` trên catalog chủ yếu là ảnh title, tips và logo. Những ảnh đó để sau.
- Phim `.usme` để sau.

## Trích câu

Không chơi game để bắt câu. Một lệnh đọc hết bảng tiếng Anh:

```powershell
.\.venv\Scripts\python.exe -m pip install UnityPy pycryptodome
.\.venv\Scripts\python.exe games\patapon12-replay\tools\extract_strings.py
```

Script ghi `locale/vi/strings.csv`. Cột `source` là tiếng Anh. `vi` để trống, `status` là `todo`. Id có dạng `P1.mission.missionid_0010.line.0`, `P2.colony.3`, `P1.system.0`. P1 và P1S dùng chung số câu. P2 và P2S cũng vậy, nhưng id khác nhau vì game tải riêng.

Bản trích có 127804 câu. Câu gốc khác nhau chỉ 4691, vì P1S trùng P1, P2S trùng P2, và nhiều khẩu lệnh lặp lại.

Câu viết tay có note `viết tay` và `status` là `review`. Script giữ câu viết tay theo nhóm: `polish_opening.py` cho lời mở đầu và menu, `translate_rhythm.py` cho câu hướng dẫn nhịp trống. Khóa là câu gốc, đúng từng ký tự. Script dừng nếu số dấu `/` lệch, hoặc câu gốc không còn trong CSV. Chạy lại không đổi gì nếu CSV đã có bản dịch đó.

```powershell
.\.venv\Scripts\python.exe games\patapon12-replay\tools\translate_rhythm.py
```

Dòng note `dịch máy`, `không dịch`, `nguồn tiếng Nhật` hoặc `lệch placeholder` không vào bundle. Game hiện tiếng Anh ở các dòng đó. Chưa dòng nào lên `done`, vì chưa chơi thử từng màn.

## Áp vào game

Bản dịch ghi đè tiếng Anh trong `LocalizeData.asset`, rồi mã hóa lại đúng bốn bundle. Launcher chép các bundle đó lên bản cài. Không dùng BepInEx.

```powershell
.\.venv\Scripts\python.exe games\patapon12-replay\tools\apply_locale_patch.py
python -m launcher.app
```

Menu tựa, logo và tips vẽ sẵn vẫn là ảnh tiếng Anh. Chữ hội thoại và menu chữ nằm trong asset. Font chữ Latin đã được thay bằng Be Vietnam Pro, nên dấu tiếng Việt nằm trên cùng một mặt chữ.

## Đã chạy thử

Bản Steam đã được áp. Log BepInEx ghi Unity 2022.3.52f1, BepInEx 6.0.0-be.738, AutoTranslator 5.6.2. Chainloader chạy xong. Plugin báo TextMesh Pro 1.4.0. Hook `TMP_Text.set_text` và `SetText` gắn được. Một overload `SetCharArray` không có trong game. Quét lúc đổi scene báo lỗi; chữ đi qua `set_text` vẫn vào hook.

## Font

Không dùng fallback và không trỏ font hệ thống. Fallback trộn hai mặt chữ trong một câu. Tên font hệ thống cần TextMesh Pro 3.2.0, trong khi asset font của game là bản 1.1.0.

Font chữ là TMP Font Asset gắn trong `sharedassets`. `tools/font/apply_vietnamese_font.py` nướng atlas SDF từ Be Vietnam Pro (thường cho TShinGo, đậm cho TTake) rồi ghi đè bảng glyph và atlas Alpha8. Padding 14, cỡ mẫu 64, gradient scale 15. Font Nhật, Hàn, Trung giữ nguyên. Unity Editor 2022.3.52f1 có trên máy nhưng chưa có license, nên atlas được nướng bằng FreeType thay vì Font Asset Creator. Bundle build bằng Unity 6 không dùng.

Bộ chữ gồm ASCII, `tools/font/vietnamese-charset.txt`, và mọi ký tự trong cột `vi`. Ký tự Be Vietnam Pro không có (□○△♪…) lấy từ Segoe UI Symbol và Yu Gothic của Windows. Chữ Việt vẫn chỉ dùng một mặt chữ.

Cần file TTF Be Vietnam Pro Regular và Bold. Font không nằm trong repo. Ghi đường dẫn vào `fonts.regular` và `fonts.bold` trong `config.json` của game. Thư mục cài lấy từ `installs` trong cùng file. Chưa có `config.json` thì script đọc `config.example.json`.

```powershell
.\.venv\Scripts\python.exe -m pip install freetype-py numpy scipy Pillow UnityPy
.\.venv\Scripts\python.exe games\patapon12-replay\tools\font\bake_sdf.py
.\.venv\Scripts\python.exe games\patapon12-replay\tools\font\apply_vietnamese_font.py
```

`bake_sdf.py` chỉ nướng atlas, rồi ghi ảnh xem thử vào `build/font-preview/`. `apply_vietnamese_font.py` vá `sharedassets0`, `sharedassets1`, `sharedassets5` vào `patch/PATAPON12_REPLAY_Data/`, đọc lại để kiểm tra có chữ `ớ`, rồi gọi launcher áp lên bản cài. File `.assets` sinh ra không được commit.

Bản mod Thái trên Nexus chỉ là tài liệu đóng gói. Không copy file của bản đó vào repo.

## Không commit

- Thư mục cài game, `*.bundle`, `*.assets`, `*.usme`, `global-metadata.dat`, `GameAssembly.dll`
- Binary đã tải trong `patch/`: `*.dll`, `winhttp.dll`, `doorstop_config.ini`, `dotnet/`
- `extract/`, `build/`, `dist/`, `config.json`

File commit trong `patch/` là config AutoTranslator và thư mục `BepInEx/Translation/`.
