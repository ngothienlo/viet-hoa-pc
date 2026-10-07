"""Cửa sổ danh sách game: chọn thư mục cài, áp hoặc gỡ bản dịch."""

from __future__ import annotations

import ctypes
import queue
import subprocess
import threading
from pathlib import Path

import tkinter as tk
from tkinter import filedialog

from launcher.apply import apply_pack, install_error, remove_pack, run_build
from launcher.catalog import Game, load_games, pack_files
from launcher.store import Store, default_state_dir

BG = "#171412"
PANEL = "#241f1c"
CARD = "#2c2622"
CARD_ON = "#3f342c"
LINE = "#4a4038"
TEXT = "#f6f1ea"
MUTED = "#b3a89c"
ACCENT = "#e4a15a"
ACCENT_TEXT = "#2a1c0e"
OK = "#b6d7a8"
WARN = "#e6c07b"
BAD = "#e7a398"

TITLE_FONT = ("Segoe UI", 20, "bold")
HEAD_FONT = ("Segoe UI", 16, "bold")
BODY_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 9)


class Launcher:
    def __init__(self, root: tk.Tk, repo: Path, state_dir: Path | None = None) -> None:
        self.root = root
        self.repo = repo
        self.store = Store(state_dir or default_state_dir())
        self.games = load_games(repo)
        self.selected: Game | None = None
        self.rows: dict[str, tk.Frame] = {}
        self.busy = False
        self._build()
        if self.games:
            self.select(self.games[0].id)

    def _build(self) -> None:
        self.root.title("Việt hóa")
        self.root.configure(bg=BG)
        self.root.minsize(860, 560)
        self.root.geometry("980x640")
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = tk.Frame(self.root, bg=BG)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(16, 8))
        tk.Label(header, text="Việt hóa", bg=BG, fg=TEXT, font=TITLE_FONT).pack(anchor="w")
        tk.Label(
            header,
            text="Chọn game, trỏ thư mục cài, rồi áp bản dịch.",
            bg=BG,
            fg=MUTED,
            font=BODY_FONT,
        ).pack(anchor="w", pady=(2, 0))

        sidebar = tk.Frame(self.root, bg=PANEL, width=300)
        sidebar.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=(0, 16))
        sidebar.grid_propagate(False)
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(1, weight=1)
        tk.Label(sidebar, text="Game", bg=PANEL, fg=MUTED, font=SMALL_FONT).grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 6)
        )
        self.list_canvas = tk.Canvas(sidebar, bg=PANEL, highlightthickness=0, bd=0)
        self.list_canvas.grid(row=1, column=0, sticky="nsew", padx=(8, 0), pady=(0, 8))
        scroll = tk.Scrollbar(sidebar, command=self.list_canvas.yview)
        scroll.grid(row=1, column=1, sticky="ns", pady=(0, 8))
        self.list_canvas.configure(yscrollcommand=scroll.set)
        self.list_frame = tk.Frame(self.list_canvas, bg=PANEL)
        self.list_frame.columnconfigure(0, weight=1)
        self.list_window = self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.list_frame.bind("<Configure>", self._fit_list)
        self.list_canvas.bind("<Configure>", self._fit_list_width)
        self.list_canvas.bind("<MouseWheel>", self._scroll_list)
        self._fill_list()

        detail = tk.Frame(self.root, bg=PANEL)
        detail.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(0, 16))
        detail.columnconfigure(0, weight=1)
        detail.rowconfigure(4, weight=1)

        self.title_label = tk.Label(detail, text="", bg=PANEL, fg=TEXT, font=HEAD_FONT, anchor="w")
        self.title_label.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 0))
        self.summary_label = tk.Label(
            detail, text="", bg=PANEL, fg=MUTED, font=BODY_FONT, anchor="w", justify="left", wraplength=560
        )
        self.summary_label.grid(row=1, column=0, sticky="ew", padx=18, pady=(4, 12))

        path_box = tk.Frame(detail, bg=PANEL)
        path_box.grid(row=2, column=0, sticky="ew", padx=18)
        path_box.columnconfigure(0, weight=1)
        tk.Label(path_box, text="Thư mục cài", bg=PANEL, fg=MUTED, font=SMALL_FONT).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(
            path_box,
            textvariable=self.path_var,
            readonlybackground=CARD,
            fg=TEXT,
            font=BODY_FONT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            state="readonly",
        )
        self.path_entry.grid(row=1, column=0, sticky="ew", pady=(6, 0), ipady=7)
        self.browse_button = self._button(path_box, "Chọn thư mục", self.browse, primary=False)
        self.browse_button.grid(row=1, column=1, padx=(8, 0), pady=(6, 0))
        self.hint_button = self._button(path_box, "Dùng thư mục có sẵn", self.use_hint, primary=False)
        self.hint_button.grid(row=2, column=0, sticky="w", pady=(8, 0))

        self.status_label = tk.Label(
            detail, text="", bg=PANEL, fg=TEXT, font=BODY_FONT, anchor="w", justify="left", wraplength=560
        )
        self.status_label.grid(row=3, column=0, sticky="ew", padx=18, pady=(16, 0))

        actions = tk.Frame(detail, bg=PANEL)
        actions.grid(row=5, column=0, sticky="sew", padx=18, pady=(8, 18))
        self.apply_button = self._button(actions, "Áp dụng tiếng Việt", self.on_apply, primary=True)
        self.apply_button.pack(side="left")
        self.remove_button = self._button(actions, "Gỡ bản dịch", self.on_remove, primary=False)
        self.remove_button.pack(side="left", padx=(8, 0))
        self.play_button = self._button(actions, "Chơi", self.on_play, primary=False)
        self.play_button.pack(side="left", padx=(8, 0))

        if not self.games:
            self.title_label.configure(text="Chưa có game")
            self.summary_label.configure(text="Thêm games/<id>/game.json để hiện ở danh sách.")
            self._set_enabled(self.browse_button, False)
            self._set_enabled(self.hint_button, False)
            self._set_enabled(self.apply_button, False)
            self._set_enabled(self.remove_button, False)
            self._set_enabled(self.play_button, False)

    def _button(self, parent: tk.Widget, text: str, command, primary: bool) -> tk.Button:
        bg = ACCENT if primary else CARD
        fg = ACCENT_TEXT if primary else TEXT
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            font=BODY_FONT,
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
        )
        return button

    def _set_enabled(self, button: tk.Button, enabled: bool) -> None:
        button.configure(state="normal" if enabled else "disabled")

    def _fit_list(self, _event: tk.Event) -> None:
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def _fit_list_width(self, event: tk.Event) -> None:
        self.list_canvas.itemconfigure(self.list_window, width=event.width)

    def _scroll_list(self, event: tk.Event) -> None:
        self.list_canvas.yview_scroll(int(-event.delta / 120), "units")

    def _fill_list(self) -> None:
        for child in self.list_frame.winfo_children():
            child.destroy()
        self.rows.clear()
        if not self.games:
            tk.Label(self.list_frame, text="Trống", bg=PANEL, fg=MUTED, font=BODY_FONT).grid(
                row=0, column=0, sticky="w", padx=6, pady=8
            )
            return
        for index, game in enumerate(self.games):
            row = tk.Frame(self.list_frame, bg=CARD, cursor="hand2")
            row.grid(row=index, column=0, sticky="ew", pady=4)
            row.columnconfigure(0, weight=1)
            name = tk.Label(row, text=game.title, bg=CARD, fg=TEXT, font=BODY_FONT, anchor="w")
            name.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 0))
            badge = tk.Label(row, text="", bg=CARD, fg=MUTED, font=SMALL_FONT, anchor="w")
            badge.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))
            row.badge = badge  # type: ignore[attr-defined]
            for widget in (row, name, badge):
                widget.bind("<Button-1>", lambda _event, game_id=game.id: self.select(game_id))
                widget.bind("<MouseWheel>", self._scroll_list)
            self.rows[game.id] = row

    def select(self, game_id: str) -> None:
        self.selected = next((game for game in self.games if game.id == game_id), None)
        for key, row in self.rows.items():
            bg = CARD_ON if key == game_id else CARD
            row.configure(bg=bg)
            for child in row.winfo_children():
                child.configure(bg=bg)
        self.refresh()

    def current_install(self) -> Path | None:
        if self.selected is None:
            return None
        raw = self.store.install_path(self.selected.id).strip()
        if not raw:
            return None
        return Path(raw)

    def browse(self) -> None:
        if self.selected is None:
            return
        chosen = filedialog.askdirectory(parent=self.root, title="Chọn thư mục cài game")
        if chosen:
            self.set_path(Path(chosen))

    def use_hint(self) -> None:
        hint = self._ready_hint()
        if hint is not None:
            self.set_path(hint)

    def set_path(self, path: Path) -> None:
        if self.selected is None:
            return
        self.store.set_install_path(self.selected.id, str(path))
        self.refresh()

    def on_apply(self) -> None:
        game, install = self._pair()
        if game is None or install is None or self.busy:
            return
        if game.build is None:
            result = apply_pack(game, install, self.store)
            self.status_label.configure(text=result.message, fg=OK if result.ok else BAD)
            self.refresh(keep_status=True)
            return
        # Build đọc bản cài và ghép font, mất khoảng một phút. Chạy nền để cửa sổ không treo.
        self.busy = True
        self._lock_actions()
        self.status_label.configure(text="Đang tạo bản vá từ bản cài của ngươi...", fg=WARN)
        events: queue.Queue = queue.Queue()

        def work() -> None:
            result = run_build(game, install, self.store, lambda line: events.put(("log", line)))
            if result.ok:
                events.put(("log", "Đang chép file vào thư mục cài..."))
                result = apply_pack(game, install, self.store)
            events.put(("done", result))

        threading.Thread(target=work, daemon=True).start()
        self._poll(events)

    def _poll(self, events: queue.Queue) -> None:
        while True:
            try:
                kind, value = events.get_nowait()
            except queue.Empty:
                break
            if kind == "log":
                self.status_label.configure(text=value, fg=WARN)
            else:
                self.busy = False
                self.status_label.configure(text=value.message, fg=OK if value.ok else BAD)
                self.refresh(keep_status=True)
                return
        self.root.after(150, self._poll, events)

    def _lock_actions(self) -> None:
        for button in (self.apply_button, self.remove_button, self.play_button, self.browse_button, self.hint_button):
            self._set_enabled(button, False)

    def on_remove(self) -> None:
        game, install = self._pair()
        if game is None or install is None or self.busy:
            return
        result = remove_pack(game, install, self.store)
        self.status_label.configure(text=result.message, fg=OK if result.ok else BAD)
        self.refresh(keep_status=True)

    def on_play(self) -> None:
        game, install = self._pair()
        if game is None or install is None or not game.exe:
            return
        exe = install / game.exe
        if not exe.is_file():
            self.status_label.configure(text=f"Không thấy {game.exe}.", fg=BAD)
            return
        subprocess.Popen([str(exe)], cwd=str(install))  # noqa: S603

    def refresh(self, keep_status: bool = False) -> None:
        self._paint_badges()
        game = self.selected
        if game is None:
            return
        if self.busy:
            self._lock_actions()
            return
        self.title_label.configure(text=game.title)
        self.summary_label.configure(text=game.summary or "Chưa có mô tả.")
        install = self.current_install()
        self.path_var.set("" if install is None else str(install))
        hint = self._ready_hint()
        self._set_enabled(self.hint_button, hint is not None)
        error = install_error(game, install)
        ready = error is None
        has_pack = self._has_pack(game)
        applied = self._applied_here(game, install)
        self._set_enabled(self.browse_button, True)
        self._set_enabled(self.apply_button, ready and has_pack)
        self._set_enabled(self.remove_button, applied)
        self._set_enabled(self.play_button, ready and bool(game.exe))
        if keep_status:
            return
        self.status_label.configure(text=self._status_text(game, error, has_pack, applied), fg=self._status_color(error, has_pack, applied))

    def _has_pack(self, game: Game) -> bool:
        """Game có bước build thì luôn áp được: file vá tạo ngay trên máy."""
        return game.build is not None or bool(pack_files(game))

    def _pair(self) -> tuple[Game | None, Path | None]:
        return self.selected, self.current_install()

    def _ready_hint(self) -> Path | None:
        if self.selected is None:
            return None
        for hint in self.selected.hints:
            if install_error(self.selected, hint) is None:
                return hint
        return None

    def _applied_here(self, game: Game, install: Path | None) -> bool:
        backup = self.store.applied_backup(game.id)
        if backup is None or install is None or not (backup / "manifest.json").is_file():
            return False
        saved = self.store.install_path(game.id)
        try:
            return Path(saved).resolve() == install.resolve()
        except OSError:
            return False

    def _status_text(self, game: Game, error: str | None, has_pack: bool, applied: bool) -> str:
        count = len(pack_files(game))
        if error:
            return error
        if applied:
            return "Đang dùng bản dịch trên thư mục này."
        if not has_pack:
            return "Đường dẫn hợp lệ. patch/ chưa có file nên chưa áp được."
        if game.build is not None:
            return "Sẵn sàng. Áp dụng sẽ tạo bản vá từ chính bản cài này, mất khoảng một phút."
        return f"Sẵn sàng áp {count} file."

    def _status_color(self, error: str | None, has_pack: bool, applied: bool) -> str:
        if error:
            return BAD if error != "Chưa chọn thư mục cài." else WARN
        if applied:
            return OK
        if not has_pack:
            return WARN
        return OK

    def _paint_badges(self) -> None:
        for game in self.games:
            row = self.rows.get(game.id)
            if row is None:
                continue
            install_raw = self.store.install_path(game.id).strip()
            install = Path(install_raw) if install_raw else None
            error = install_error(game, install)
            if error == "Chưa chọn thư mục cài.":
                text, color = "Chưa chọn", MUTED
            elif error:
                text, color = "Sai thư mục", BAD
            elif self._applied_here(game, install):
                text, color = "Đã áp dụng", OK
            elif self._has_pack(game):
                text, color = "Sẵn sàng", OK
            else:
                text, color = "Chưa có gói", WARN
            row.badge.configure(text=text, fg=color)  # type: ignore[attr-defined]


def run(repo: Path | None = None) -> None:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass
    root = tk.Tk()
    Launcher(root, repo or Path(__file__).resolve().parents[1])
    root.mainloop()


if __name__ == "__main__":
    run()
