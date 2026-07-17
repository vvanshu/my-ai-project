"""
app.py — Main application window with tabbed interface and status bar.
"""

import tkinter as tk
from tkinter import ttk

from ui.theme import Colors, Fonts, Dims, apply_theme
from ui.todo_tab import TodoTab
from ui.weather_tab import WeatherTab
from ui.quotes_tab import QuotesTab
from assistant.todo import TodoManager
from assistant.quotes import get_daily_quote
from assistant.reminders import ReminderManager


class DesktopAssistant(tk.Tk):
    """Main desktop assistant application window."""

    APP_TITLE = "✦ Desktop Assistant"
    MIN_WIDTH = 750
    MIN_HEIGHT = 600

    def __init__(self):
        super().__init__()

        # ── Window setup ─────────────────────────────────────
        self.title(self.APP_TITLE)
        self.geometry("800x650")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.configure(bg=Colors.BG_PRIMARY)

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 800) // 2
        y = (self.winfo_screenheight() - 650) // 2
        self.geometry(f"+{x}+{y}")

        # ── Apply theme ──────────────────────────────────────
        apply_theme(self)

        # ── Initialize managers ──────────────────────────────
        self.todo_manager = TodoManager()
        self.reminder_manager = ReminderManager()
        self.reminder_manager.set_root(self)

        # ── Build UI ─────────────────────────────────────────
        self._build_header()
        self._build_tabs()
        self._build_status_bar()

    def _build_header(self):
        """Top title bar with app name."""
        header = tk.Frame(self, bg=Colors.BG_TERTIARY, padx=Dims.PAD_XL, pady=Dims.PAD_MD)
        header.pack(fill="x")

        # App icon + title
        title_frame = tk.Frame(header, bg=Colors.BG_TERTIARY)
        title_frame.pack(side="left")

        tk.Label(
            title_frame, text="✦", bg=Colors.BG_TERTIARY,
            fg=Colors.ACCENT_PRIMARY, font=("Segoe UI Emoji", 20),
        ).pack(side="left", padx=(0, 8))

        tk.Label(
            title_frame, text="Desktop Assistant", bg=Colors.BG_TERTIARY,
            fg=Colors.TEXT_PRIMARY, font=Fonts.HEADING_2,
        ).pack(side="left")

        # Subtitle
        tk.Label(
            header, text="Your personal productivity companion",
            bg=Colors.BG_TERTIARY, fg=Colors.TEXT_SECONDARY,
            font=Fonts.SMALL,
        ).pack(side="right")

    def _build_tabs(self):
        """Create the tabbed notebook with all three tabs."""
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill="both", expand=True, padx=0, pady=0)

        # Create tabs
        self._todo_tab = TodoTab(self._notebook, self.todo_manager)
        self._weather_tab = WeatherTab(self._notebook)
        self._quotes_tab = QuotesTab(self._notebook, self.reminder_manager)

        # Add tabs with labels
        self._notebook.add(self._todo_tab, text="  📋  To-Do List  ")
        self._notebook.add(self._weather_tab, text="  🌤️  Weather  ")
        self._notebook.add(self._quotes_tab, text="  💡  Quotes & Reminders  ")

    def _build_status_bar(self):
        """Bottom status bar with daily quote."""
        status = tk.Frame(self, bg=Colors.BG_TERTIARY, padx=Dims.PAD_LG, pady=Dims.PAD_SM)
        status.pack(fill="x", side="bottom")

        # Daily quote in status bar
        quote_text, quote_author = get_daily_quote()
        display_text = f'💬  "{quote_text}" — {quote_author}'
        if len(display_text) > 100:
            display_text = display_text[:97] + "..."

        tk.Label(
            status, text=display_text, bg=Colors.BG_TERTIARY,
            fg=Colors.TEXT_SECONDARY, font=Fonts.SMALL, anchor="w",
        ).pack(side="left", fill="x", expand=True)

        tk.Label(
            status, text="✦ v1.0", bg=Colors.BG_TERTIARY,
            fg=Colors.TEXT_DISABLED, font=Fonts.SMALL,
        ).pack(side="right")

    def run(self):
        """Start the application main loop."""
        self.mainloop()
