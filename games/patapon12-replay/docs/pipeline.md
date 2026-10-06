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

Bản trích hiện có 127804 câu: P1 25229, P1S 25229, P2 38673, P2S 38673.

## Áp vào game

Hook BepInEx chỉ để hiện bản dịch sau này, không phải để thu thập câu. Gói là Thunderstore `BepInExPack_Patapon` 6.0.75301 và XUnity.AutoTranslator IL2CPP 5.6.2. Binary không commit.

```powershell
.\.venv\Scripts\python.exe games\patapon12-replay\tools\fetch_runtime.py
```

Rồi mở launcher và bấm Áp dụng. `Endpoint` để trống nên game không gửi câu thoại đi máy dịch. Font tiếng Việt vẫn chưa có, nên chữ Việt có thể thành ô vuông.

## Đã chạy thử

Bản Steam đã được áp. Log BepInEx ghi Unity 2022.3.52f1, BepInEx 6.0.0-be.738, AutoTranslator 5.6.2. Chainloader chạy xong. Plugin báo TextMesh Pro 1.4.0. Hook `TMP_Text.set_text` và `SetText` gắn được. Một overload `SetCharArray` không có trong game. Quét lúc đổi scene báo lỗi; chữ đi qua `set_text` vẫn vào hook.

## Font

`OverrideFontTextMeshPro` và `FallbackFontTextMeshPro` để trống. Không điền đường dẫn TTF. Không dùng fallback, vì dấu tiếng Việt sẽ trộn hai font trong một câu. Tên font hệ thống chỉ dùng được từ TextMesh Pro 3.2.0, còn plugin đang báo 1.4.0, nên không đi đường đó. Font dùng được là TMP FontAsset trong asset bundle build bằng Unity 2022.3.52f1. Máy làm việc hiện chưa có Unity Editor đó, nên chữ Việt có thể thành ô vuông cho đến khi có bundle. Bundle build bằng Unity 6 không dùng.

Bản mod Thái trên Nexus chỉ là tài liệu đóng gói. Không copy file của bản đó vào repo.

## Không commit

- Thư mục cài game, `*.bundle`, `*.assets`, `*.usme`, `global-metadata.dat`, `GameAssembly.dll`
- Binary đã tải trong `patch/`: `*.dll`, `winhttp.dll`, `doorstop_config.ini`, `dotnet/`
- `extract/`, `build/`, `dist/`, `config.json`

File commit trong `patch/` là config AutoTranslator và thư mục `BepInEx/Translation/`.
