"""
quotes_tab.py — Motivational quotes display and reminder management.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.theme import Colors, Fonts, Dims, make_entry
from assistant.quotes import get_random_quote, get_daily_quote
from assistant.reminders import ReminderManager


class QuotesTab(ttk.Frame):
    """Motivational quotes and reminders tab."""

    def __init__(self, parent, reminder_manager: ReminderManager):
        super().__init__(parent, style="TFrame")
        self.reminders = reminder_manager
        self._build_ui()
        self._show_daily_quote()

    def _build_ui(self):
        # ── Header ───────────────────────────────────────────
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=Dims.PAD_XL, pady=(Dims.PAD_XL, Dims.PAD_SM))

        ttk.Label(header, text="💡  Quotes & Reminders", style="Heading.TLabel").pack(side="left")

        # ── Quote card ───────────────────────────────────────
        self._quote_card = tk.Frame(self, bg=Colors.BG_SECONDARY, padx=30, pady=30)
        self._quote_card.pack(fill="x", padx=Dims.PAD_XL, pady=Dims.PAD_SM)

        self._quote_emoji = tk.Label(
            self._quote_card, text="✨", bg=Colors.BG_SECONDARY,
            font=("Segoe UI Emoji", 28),
        )
        self._quote_emoji.pack(pady=(0, 10))

        self._quote_text = tk.Label(
            self._quote_card, text="", bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY, font=Fonts.QUOTE,
            wraplength=500, justify="center",
        )
        self._quote_text.pack()

        self._quote_author = tk.Label(
            self._quote_card, text="", bg=Colors.BG_SECONDARY,
            fg=Colors.ACCENT_PRIMARY, font=Fonts.QUOTE_AUTHOR,
        )
        self._quote_author.pack(pady=(10, 0))

        # ── Quote buttons ────────────────────────────────────
        quote_buttons = ttk.Frame(self, style="TFrame")
        quote_buttons.pack(fill="x", padx=Dims.PAD_XL, pady=Dims.PAD_SM)

        ttk.Button(
            quote_buttons, text="🎲  New Random Quote", style="Accent.TButton",
            command=self._show_random_quote,
        ).pack(side="left", padx=(0, Dims.PAD_SM))

        ttk.Button(
            quote_buttons, text="📅  Today's Quote", style="Ghost.TButton",
            command=self._show_daily_quote,
        ).pack(side="left")

        # ── Separator ────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=Dims.PAD_XL, pady=Dims.PAD_LG)

        # ── Reminders section ────────────────────────────────
        rem_header = ttk.Frame(self, style="TFrame")
        rem_header.pack(fill="x", padx=Dims.PAD_XL, pady=(0, Dims.PAD_SM))

        ttk.Label(rem_header, text="⏰  Set a Reminder", style="Heading.TLabel",
                  font=Fonts.HEADING_3).pack(side="left")

        self._rem_count_label = ttk.Label(rem_header, text="", style="Secondary.TLabel")
        self._rem_count_label.pack(side="right")

        # Reminder input
        rem_input = ttk.Frame(self, style="TFrame")
        rem_input.pack(fill="x", padx=Dims.PAD_XL, pady=(0, Dims.PAD_SM))

        self._rem_entry = make_entry(rem_input)
        self._rem_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self._rem_entry.insert(0, "What should I remind you about?")
        self._rem_entry.config(fg=Colors.TEXT_DISABLED)
        self._rem_entry.bind("<FocusIn>", self._on_rem_focus_in)
        self._rem_entry.bind("<FocusOut>", self._on_rem_focus_out)

        # Minutes spinner
        min_frame = tk.Frame(rem_input, bg=Colors.BG_PRIMARY)
        min_frame.pack(side="left", padx=(Dims.PAD_SM, 0))

        tk.Label(
            min_frame, text="in", bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_SECONDARY, font=Fonts.BODY,
        ).pack(side="left", padx=(0, 4))

        self._min_var = tk.StringVar(value="5")
        self._min_spinbox = tk.Spinbox(
            min_frame, from_=1, to=1440, width=4,
            textvariable=self._min_var,
            bg=Colors.BG_INPUT, fg=Colors.TEXT_PRIMARY,
            buttonbackground=Colors.BG_SECONDARY,
            font=Fonts.BODY, relief="flat",
            highlightthickness=1,
            highlightbackground=Colors.BORDER,
        )
        self._min_spinbox.pack(side="left", ipady=6)

        tk.Label(
            min_frame, text="min", bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_SECONDARY, font=Fonts.BODY,
        ).pack(side="left", padx=(4, 0))

        ttk.Button(
            rem_input, text="⏰  Set", style="Success.TButton",
            command=self._add_reminder,
        ).pack(side="right", padx=(Dims.PAD_SM, 0))

        # ── Active reminders list ────────────────────────────
        self._rem_list_frame = ttk.Frame(self, style="TFrame")
        self._rem_list_frame.pack(fill="both", expand=True, padx=Dims.PAD_XL, pady=(Dims.PAD_SM, Dims.PAD_XL))

        self._refresh_reminders()

    # ── Quote helpers ────────────────────────────────────────

    def _show_random_quote(self):
        text, author = get_random_quote()
        self._update_quote(text, author)

    def _show_daily_quote(self):
        text, author = get_daily_quote()
        self._update_quote(text, author)

    def _update_quote(self, text, author):
        self._quote_text.config(text=f'"{text}"')
        self._quote_author.config(text=f"— {author}")

    # ── Reminder helpers ─────────────────────────────────────

    def _on_rem_focus_in(self, event):
        if self._rem_entry.get() == "What should I remind you about?":
            self._rem_entry.delete(0, "end")
            self._rem_entry.config(fg=Colors.TEXT_PRIMARY)

    def _on_rem_focus_out(self, event):
        if not self._rem_entry.get().strip():
            self._rem_entry.insert(0, "What should I remind you about?")
            self._rem_entry.config(fg=Colors.TEXT_DISABLED)

    def _add_reminder(self):
        text = self._rem_entry.get().strip()
        if not text or text == "What should I remind you about?":
            return

        try:
            minutes = int(self._min_var.get())
        except ValueError:
            messagebox.showwarning("Invalid Time", "Please enter a valid number of minutes.")
            return

        try:
            self.reminders.add_reminder(text, minutes, callback=self._on_reminder_fire)
            self._rem_entry.delete(0, "end")
            self._rem_entry.insert(0, "What should I remind you about?")
            self._rem_entry.config(fg=Colors.TEXT_DISABLED)
            self._refresh_reminders()
        except ValueError as e:
            messagebox.showwarning("Reminder Error", str(e))

    def _cancel_reminder(self, rid):
        self.reminders.cancel_reminder(rid)
        self._refresh_reminders()

    def _on_reminder_fire(self, rid, text):
        """Called when a reminder fires — show a popup."""
        messagebox.showinfo("⏰ Reminder!", f"\n{text}\n")
        self._refresh_reminders()

    def _refresh_reminders(self):
        for w in self._rem_list_frame.winfo_children():
            w.destroy()

        active = self.reminders.get_active()
        self._rem_count_label.config(
            text=f"{len(active)} active" if active else "No active reminders"
        )

        if not active:
            tk.Label(
                self._rem_list_frame,
                text="No active reminders. Set one above! ⏰",
                bg=Colors.BG_PRIMARY, fg=Colors.TEXT_SECONDARY,
                font=Fonts.BODY, pady=20,
            ).pack(fill="x")
            return

        for rem in active:
            row = tk.Frame(self._rem_list_frame, bg=Colors.BG_SECONDARY, padx=Dims.PAD_MD, pady=Dims.PAD_SM)
            row.pack(fill="x", pady=(0, Dims.PAD_XS))

            tk.Label(
                row, text="⏰", bg=Colors.BG_SECONDARY,
                font=("Segoe UI Emoji", 14),
            ).pack(side="left", padx=(0, Dims.PAD_SM))

            info_frame = tk.Frame(row, bg=Colors.BG_SECONDARY)
            info_frame.pack(side="left", fill="x", expand=True)

            tk.Label(
                info_frame, text=rem["text"], bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_PRIMARY, font=Fonts.BODY, anchor="w",
            ).pack(fill="x")

            tk.Label(
                info_frame, text=f"Fires at {rem['fire_at_display']}  ({rem['minutes']} min)",
                bg=Colors.BG_SECONDARY, fg=Colors.TEXT_SECONDARY,
                font=Fonts.SMALL, anchor="w",
            ).pack(fill="x")

            cancel_btn = tk.Label(
                row, text="✕", bg=Colors.BG_SECONDARY,
                fg=Colors.ACCENT_DANGER, font=Fonts.BODY_BOLD,
                cursor="hand2", padx=8,
            )
            cancel_btn.pack(side="right")
            cancel_btn.bind("<Button-1>", lambda e, r=rem["id"]: self._cancel_reminder(r))
