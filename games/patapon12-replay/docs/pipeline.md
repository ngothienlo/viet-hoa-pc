# Pipeline

Thư mục game này là `games/patapon12-replay/`. Đường dẫn CSV và docs bên dưới tính từ đó. Lệnh kiểm tra chạy từ thư mục gốc repo.

Làm trên bản cài hợp pháp. Steam và Epic dùng cùng cấu trúc thư mục cài. Đường dẫn ghi trong `config.json`.

## Chữ nằm ở đâu

- Catalog Addressables: `PATAPON12_REPLAY_Data/StreamingAssets/aa/catalog.json`
- Bundle: `PATAPON12_REPLAY_Data/StreamingAssets/aa/StandaloneWindows64/`
- Catalog khai báo provider bundle đã mã hóa và provider CRIWARE. Vì vậy không sửa chuỗi bằng cách mở file text.
- Bản dịch fan đã có (Nga, Bồ Đào Nha Brazil) thay một số bundle trong `StandaloneWindows64`, rồi chọn một ngôn ngữ có sẵn trong game để chữ mới hiện ra.
- Phim mở đầu và staff roll nằm ở `StreamingAssets/P1/Movie` và `StreamingAssets/P2/Movie` dạng `.usme`. Để sau.

## Việc làm trên máy

1. Copy `config.example.json` thành `config.json`.
2. Trích chuỗi từ bản cài bằng công cụ đọc asset Unity (UABEA hoặc AssetStudio). Để kết quả thô trong `extract/`. Thư mục này bị git bỏ qua.
3. Nguồn dịch là tiếng Anh. Đối chiếu tiếng Nhật khi câu Anh tối nghĩa.
4. Đưa từng khóa vào `locale/vi/strings.csv`.
5. Từ thư mục gốc repo, chạy `python tools/validate_locale.py games/patapon12-replay`.
6. Đóng gói bản vá local trong `build/`. Không commit bundle.

## Cột trong `strings.csv`

| Cột | Ý nghĩa |
| --- | --- |
| `id` | Khóa ổn định, duy nhất. Giữ nguyên khóa của game khi trích được. |
| `context` | Màn hình hoặc nhóm: `ui`, `item`, `dialog`, `help`. |
| `source` | Câu gốc tiếng Anh. |
| `vi` | Câu tiếng Việt. Để trống khi chưa dịch. |
| `status` | `todo`, `draft`, `review`, `done`. |
| `note` | Giới hạn chữ, biến số, chỗ câu dễ lệch nghĩa. |

Dòng có `id` bắt đầu bằng `EXAMPLE` chỉ để minh họa định dạng. Xóa trước khi dịch thật.

## Không commit

- Thư mục cài game, `*.bundle`, `*.assets`, `*.usme`, `global-metadata.dat`, `GameAssembly.dll`
- `extract/`, `build/`, `dist/`, `config.json`

Bản vá gửi cho máy khác chỉ gồm file đã sửa và hướng dẫn cài. Giữ nguyên file gốc trong một bản sao lưu ngoài git trước khi ghi đè.
