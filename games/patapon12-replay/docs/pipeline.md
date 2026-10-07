# Pipeline

Thư mục game này là `games/patapon12-replay/`. Lệnh chạy từ thư mục gốc repo.

Làm trên bản cài hợp pháp. Steam và Epic dùng cùng cấu trúc thư mục cài.

## Chữ nằm ở đâu

- Catalog Addressables: `PATAPON12_REPLAY_Data/StreamingAssets/aa/catalog.json`
- Bundle: `PATAPON12_REPLAY_Data/StreamingAssets/aa/StandaloneWindows64/`
- Hội thoại, menu, tips và trợ giúp nằm trong `LocalizeData.asset` của P1, P1S, P2, P2S. `TipsData.asset` chỉ là tên sprite, không có câu.
- Bundle bị mã hóa bằng AES. Mật khẩu là `m_Hash` trong catalog. Salt là tên file bundle, bỏ đuôi. Giải xong thì UnityPy đọc được typetree của `LocalizeData`. `extract_strings.py` có `open_bundle` và `save_bundle` để đọc và ghi lại đúng khóa.
- Script luôn đọc bundle gốc. Launcher đã áp bản vá thì bản gốc nằm trong thư mục sao lưu của launcher (`original()` trong `tools/game_config.py`).
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

Rà soát hàng loạt (#11) đi qua `tools/apply_fixes.py`. Mỗi file sửa là một mảng JSON `{"source", "vi", "reason"}`. Script loại câu lệch số `/`, mã `&H…#`, placeholder hay ký hiệu nút, báo xung đột khi hai file sửa cùng câu gốc, rồi ghi câu mới cho mọi dòng cùng câu gốc với `status` là `review`.

```powershell
.\.venv\Scripts\python.exe games\patapon12-replay\tools\apply_fixes.py --dry-run fixes1.json fixes2.json
.\.venv\Scripts\python.exe games\patapon12-replay\tools\apply_fixes.py fixes1.json fixes2.json
```

Dòng note `dịch máy`, `không dịch`, `nguồn tiếng Nhật` hoặc `lệch placeholder` không vào bundle. Game hiện tiếng Anh ở các dòng đó. Sau lần rà #11, mọi câu có bản dịch đều ở `review`. Chưa dòng nào lên `done`, vì chưa chơi thử từng màn.

## Áp vào game

Bản dịch ghi đè tiếng Anh trong `LocalizeData.asset`, rồi mã hóa lại đúng bốn bundle. Không dùng BepInEx.

Từ #17, `game.json` có `"build": "tools/build_patch.py"`. Bấm Áp dụng trong launcher (hoặc `VietHoa.exe`) thì launcher tạo bản vá ngay từ bản cài của người chơi: 4 bundle `LocalizeData`, rồi các font đã ghép chữ Việt. Mất khoảng một phút. File ghi vào `%LOCALAPPDATA%\viet-hoa-pc\build\patapon12-replay\`, rồi mới chép lên bản cài. Repo và bản exe không chứa file nào của game.

Chạy tay, không qua launcher:

```powershell
.\.venv\Scripts\python.exe games\patapon12-replay\tools\build_patch.py "<thư mục cài>" "<thư mục ra>"
python -m launcher.app
```

`apply_locale_patch.py` và `font\apply_vietnamese_font.py` vẫn chạy riêng được. Khi đó file ghi vào `patch/` của game, hoặc vào `VH_PATCH_DIR` nếu biến này có giá trị.

Menu tựa, logo và tips vẽ sẵn vẫn là ảnh tiếng Anh. Chữ hội thoại và menu chữ nằm trong asset. Font chữ được vá để chữ Việt hiện đủ dấu và cùng một mặt chữ (xem `docs/font.md`).

## Đã chạy thử

Bản Steam: Unity 2022.3.52f1, TextMesh Pro 1.4.0. Bản vá ghi thẳng vào asset; người dùng đã chơi thử lời thoại và lời dẫn.

Cách cũ dùng BepInEx và XUnity.AutoTranslator để bắt chữ lúc chơi. Cách đó đã bỏ ở #17: `runtime.lock.json`, `fetch_runtime.py`, `echo_translate.py` và config AutoTranslator trong `patch/` đã xóa khỏi repo. Bản cài từng áp cách cũ có thể còn thư mục `BepInEx/` và `dotnet/`. Không có `winhttp.dll` thì BepInEx không chạy, nhưng có thể xóa hai thư mục đó.

## Font

Toàn bộ phần font nằm ở `docs/font.md`: font nào vẽ chữ gì, cách vá từng nhóm, lệnh chạy, và bẫy.

Tóm tắt: mọi font Latin (TTake là font kiểu Patapon của lời thoại, TShinGo, KakuPop, Londrina) giữ nét gốc; chữ Việt được ghép từ glyph của chính font đó. Riêng `_savewindow` chỉ có 18 chữ hoa, nên mượn cả chữ gốc của TShinGo. Không dùng font fallback và không trỏ font hệ thống. Danh sách font đã quét nằm ở `tools/font/fonts.json`.

```powershell
.\.venv\Scripts\python.exe games\patapon12-replay\tools\font\apply_vietnamese_font.py
```

Bản mod Thái trên Nexus chỉ là tài liệu đóng gói. Không copy file của bản đó vào repo.

## Không commit

- Thư mục cài game, `*.bundle`, `*.assets`, `*.usme`, `global-metadata.dat`, `GameAssembly.dll`
- `extract/`, `build/`, `dist/`, `config.json`

`patch/` của game này chỉ còn `.gitkeep`. File vá sinh ra (khi chạy script tay) nằm trong đó nhưng không được commit.
