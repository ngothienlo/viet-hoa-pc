"""Endpoint local: trả lại đúng câu gốc để AutoTranslator ghi câu chưa dịch.

Chạy sau khi đã Áp dụng. Ctrl+C trả config trong thư mục cài về như cũ.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from launcher.store import Store, default_state_dir

GAME_ID = "patapon12-replay"
HOST = "127.0.0.1"
PORT = 8765
CAPTURE = REPO / "games" / GAME_ID / "extract" / "captured-en.jsonl"

capture_path: Path | None = None
_seen: set[str] = set()


def set_ini_values(text: str, updates: dict[str, dict[str, str]]) -> str:
    """Đặt khóa trong các section. Giữ thứ tự dòng cũ."""
    newline = "\r\n" if "\r\n" in text else "\n"
    pending = {section: dict(keys) for section, keys in updates.items()}
    current: str | None = None
    out: list[str] = []

    def flush() -> None:
        if current is None:
            return
        keys = pending.get(current)
        if not keys:
            return
        for key, value in list(keys.items()):
            out.append(f"{key}={value}")
            del keys[key]

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]") and ";" not in stripped:
            flush()
            current = stripped[1:-1].strip()
            out.append(line)
            continue
        name = _key(line)
        section_keys = pending.get(current or "")
        if name is not None and section_keys is not None and name in section_keys:
            out.append(f"{name}={section_keys.pop(name)}")
            continue
        out.append(line)
    flush()
    for section, keys in pending.items():
        if not keys:
            continue
        if out and out[-1] != "":
            out.append("")
        out.append(f"[{section}]")
        for key, value in keys.items():
            out.append(f"{key}={value}")
    body = newline.join(out)
    if body and not body.endswith(newline):
        body += newline
    return body


def _key(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith(";") or stripped.startswith("#") or stripped.startswith("["):
        return None
    body = stripped.split(";", 1)[0]
    if "=" not in body:
        return None
    return body.split("=", 1)[0].strip()


def install_config(state_dir: Path | None = None) -> Path:
    store = Store(state_dir or default_state_dir())
    raw = store.install_path(GAME_ID).strip()
    if not raw:
        raise SystemExit("Chưa chọn thư mục cài. Mở launcher, chọn game, rồi Áp dụng.")
    path = Path(raw) / "BepInEx" / "config" / "AutoTranslatorConfig.ini"
    if not path.is_file():
        raise SystemExit("Chưa thấy config trong thư mục cài. Chạy fetch_runtime.py rồi bấm Áp dụng.")
    return path


def remember(text: str) -> None:
    if capture_path is None or text == "" or text in _seen:
        return
    _seen.add(text)
    capture_path.parent.mkdir(parents=True, exist_ok=True)
    with capture_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")


def load_seen(path: Path) -> None:
    _seen.clear()
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            _seen.add(item["text"])


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/translate":
            self.send_error(404)
            return
        values = urllib.parse.parse_qs(parsed.query)
        text = values.get("text", [""])[0]
        remember(text)
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def serve(port: int = PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((HOST, port), Handler)


def _arm(text: str) -> str:
    return set_ini_values(
        text,
        {
            "Service": {"Endpoint": "CustomTranslate"},
            "Custom": {"Url": f"http://{HOST}:{PORT}/translate"},
            "Behaviour": {"OutputTooLongText": "True"},
        },
    )


def main() -> None:
    global capture_path
    path = install_config()
    original = path.read_text(encoding="utf-8")
    path.write_text(_arm(original), encoding="utf-8")
    capture_path = CAPTURE
    load_seen(CAPTURE)
    server = None
    try:
        server = serve()
        print(f"Đang nghe http://{HOST}:{PORT}/translate")
        print("Mở game và chơi đến chỗ cần bắt chữ. Ctrl+C để dừng và trả config về như cũ.")
        print(f"Câu mới ghi vào {CAPTURE}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Đã dừng.")
    finally:
        if server is not None:
            server.server_close()
        path.write_text(original, encoding="utf-8")
        print("Đã trả AutoTranslatorConfig.ini trong thư mục cài về như cũ.")


if __name__ == "__main__":
    main()
