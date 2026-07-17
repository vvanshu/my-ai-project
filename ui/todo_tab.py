"""
todo_tab.py — To-do list tab with add, complete, delete, and filtering.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.theme import Colors, Fonts, Dims, make_entry


class TodoTab(ttk.Frame):
    """To-do list management tab."""

    def __init__(self, parent, todo_manager):
        super().__init__(parent, style="TFrame")
        self.todo = todo_manager
        self._filter = "all"  # "all", "pending", "completed"
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        # ── Header ───────────────────────────────────────────
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=Dims.PAD_XL, pady=(Dims.PAD_XL, Dims.PAD_SM))

        ttk.Label(header, text="📋  To-Do List", style="Heading.TLabel").pack(side="left")

        self._counter_label = ttk.Label(header, text="", style="Secondary.TLabel")
        self._counter_label.pack(side="right")

        # ── Input row ────────────────────────────────────────
        input_frame = ttk.Frame(self, style="TFrame")
        input_frame.pack(fill="x", padx=Dims.PAD_XL, pady=Dims.PAD_SM)

        self._entry = make_entry(input_frame)
        self._entry.pack(side="left", fill="x", expand=True, ipady=8)
        self._entry.bind("<Return>", lambda e: self._add_task())

        add_btn = ttk.Button(
            input_frame, text="＋ Add Task", style="Accent.TButton",
            command=self._add_task,
        )
        add_btn.pack(side="right", padx=(Dims.PAD_SM, 0))

        # ── Filter row ───────────────────────────────────────
        filter_frame = ttk.Frame(self, style="TFrame")
        filter_frame.pack(fill="x", padx=Dims.PAD_XL, pady=(Dims.PAD_SM, Dims.PAD_XS))

        for label, value in [("All", "all"), ("Pending", "pending"), ("Completed", "completed")]:
            btn = ttk.Button(
                filter_frame, text=label, style="Ghost.TButton",
                command=lambda v=value: self._set_filter(v),
            )
            btn.pack(side="left", padx=(0, Dims.PAD_XS))

        self._clear_btn = ttk.Button(
            filter_frame, text="🗑  Clear Completed", style="Danger.TButton",
            command=self._clear_completed,
        )
        self._clear_btn.pack(side="right")

        # ── Separator ────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=Dims.PAD_XL, pady=Dims.PAD_SM)

        # ── Scrollable task list ─────────────────────────────
        list_container = ttk.Frame(self, style="TFrame")
        list_container.pack(fill="both", expand=True, padx=Dims.PAD_XL, pady=(0, Dims.PAD_XL))

        self._canvas = tk.Canvas(
            list_container, bg=Colors.BG_PRIMARY,
            highlightthickness=0, borderwidth=0,
        )
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self._canvas.yview)
        self._tasks_frame = ttk.Frame(self._canvas, style="TFrame")

        self._tasks_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )

        self._canvas_window = self._canvas.create_window((0, 0), window=self._tasks_frame, anchor="nw")
        self._canvas.configure(yscrollcommand=scrollbar.set)

        self._canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Resize inner frame width with canvas
        self._canvas.bind("<Configure>", self._on_canvas_resize)

        # Mouse wheel scrolling
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")

    def _on_canvas_resize(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _set_filter(self, f):
        self._filter = f
        self._refresh_list()

    def _add_task(self):
        text = self._entry.get().strip()
        if not text:
            return
        self.todo.add_task(text)
        self._entry.delete(0, "end")
        self._refresh_list()

    def _toggle_task(self, task_id):
        self.todo.toggle_complete(task_id)
        self._refresh_list()

    def _delete_task(self, task_id):
        self.todo.remove_task(task_id)
        self._refresh_list()

    def _clear_completed(self):
        count = self.todo.clear_completed()
        if count:
            self._refresh_list()

    def _refresh_list(self):
        # Clear old widgets
        for widget in self._tasks_frame.winfo_children():
            widget.destroy()

        # Get filtered tasks
        if self._filter == "pending":
            tasks = self.todo.get_pending()
        elif self._filter == "completed":
            tasks = self.todo.get_completed()
        else:
            tasks = self.todo.get_all()

        # Update counter
        pending = self.todo.pending_count
        total = self.todo.total_count
        self._counter_label.config(text=f"{pending} pending  ·  {total} total")

        if not tasks:
            empty_label = tk.Label(
                self._tasks_frame,
                text="No tasks yet — add one above! ✨" if self._filter == "all"
                     else f"No {self._filter} tasks.",
                bg=Colors.BG_PRIMARY, fg=Colors.TEXT_SECONDARY,
                font=Fonts.BODY, pady=40,
            )
            empty_label.pack(fill="x")
            return

        for task in tasks:
            self._create_task_row(task)

    def _create_task_row(self, task):
        completed = task["completed"]

        row = tk.Frame(self._tasks_frame, bg=Colors.BG_SECONDARY, padx=Dims.PAD_MD, pady=Dims.PAD_SM)
        row.pack(fill="x", pady=(0, Dims.PAD_XS))

        # Checkbox
        check_text = "✅" if completed else "⬜"
        check_btn = tk.Label(
            row, text=check_text, bg=Colors.BG_SECONDARY,
            font=("Segoe UI Emoji", 14), cursor="hand2",
        )
        check_btn.pack(side="left", padx=(0, Dims.PAD_SM))
        check_btn.bind("<Button-1>", lambda e, tid=task["id"]: self._toggle_task(tid))

        # Task text
        text_color = Colors.TEXT_SECONDARY if completed else Colors.TEXT_PRIMARY
        text_font = Fonts.BODY
        task_label = tk.Label(
            row, text=task["text"], bg=Colors.BG_SECONDARY,
            fg=text_color, font=text_font, anchor="w",
        )
        if completed:
            task_label.config(font=(Fonts.BODY[0], Fonts.BODY[1], "overstrike"))
        task_label.pack(side="left", fill="x", expand=True)

        # Delete button
        del_btn = tk.Label(
            row, text="✕", bg=Colors.BG_SECONDARY,
            fg=Colors.ACCENT_DANGER, font=Fonts.BODY_BOLD,
            cursor="hand2", padx=8,
        )
        del_btn.pack(side="right")
        del_btn.bind("<Button-1>", lambda e, tid=task["id"]: self._delete_task(tid))

        # Hover effects
        def on_enter(e, r=row):
            r.config(bg=Colors.BG_HOVER)
            for child in r.winfo_children():
                child.config(bg=Colors.BG_HOVER)

        def on_leave(e, r=row):
            r.config(bg=Colors.BG_SECONDARY)
            for child in r.winfo_children():
                child.config(bg=Colors.BG_SECONDARY)

        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
