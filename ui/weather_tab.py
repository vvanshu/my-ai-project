"""
weather_tab.py — Weather lookup tab with city search and a styled result card.
"""

import tkinter as tk
from tkinter import ttk
import threading

from ui.theme import Colors, Fonts, Dims, make_entry
from assistant.weather import get_weather


class WeatherTab(ttk.Frame):
    """Weather checking tab with live city search."""

    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._last_city = ""
        self._build_ui()

    def _build_ui(self):
        # ── Header ───────────────────────────────────────────
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=Dims.PAD_XL, pady=(Dims.PAD_XL, Dims.PAD_SM))

        ttk.Label(header, text="🌤️  Weather", style="Heading.TLabel").pack(side="left")

        # ── Search row ───────────────────────────────────────
        search_frame = ttk.Frame(self, style="TFrame")
        search_frame.pack(fill="x", padx=Dims.PAD_XL, pady=Dims.PAD_SM)

        self._city_entry = make_entry(search_frame)
        self._city_entry.insert(0, "Enter city name...")
        self._city_entry.config(fg=Colors.TEXT_DISABLED)
        self._city_entry.pack(side="left", fill="x", expand=True, ipady=8)

        # Placeholder behavior
        self._city_entry.bind("<FocusIn>", self._on_focus_in)
        self._city_entry.bind("<FocusOut>", self._on_focus_out)
        self._city_entry.bind("<Return>", lambda e: self._fetch_weather())

        fetch_btn = ttk.Button(
            search_frame, text="🔍  Get Weather", style="Accent.TButton",
            command=self._fetch_weather,
        )
        fetch_btn.pack(side="right", padx=(Dims.PAD_SM, 0))

        # ── Separator ────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=Dims.PAD_XL, pady=Dims.PAD_MD)

        # ── Result area ──────────────────────────────────────
        self._result_frame = ttk.Frame(self, style="TFrame")
        self._result_frame.pack(fill="both", expand=True, padx=Dims.PAD_XL, pady=Dims.PAD_SM)

        self._show_placeholder()

    def _on_focus_in(self, event):
        if self._city_entry.get() == "Enter city name...":
            self._city_entry.delete(0, "end")
            self._city_entry.config(fg=Colors.TEXT_PRIMARY)

    def _on_focus_out(self, event):
        if not self._city_entry.get().strip():
            self._city_entry.insert(0, "Enter city name...")
            self._city_entry.config(fg=Colors.TEXT_DISABLED)

    def _show_placeholder(self):
        for w in self._result_frame.winfo_children():
            w.destroy()

        placeholder = tk.Frame(self._result_frame, bg=Colors.BG_PRIMARY)
        placeholder.pack(expand=True)

        tk.Label(
            placeholder, text="🌍", bg=Colors.BG_PRIMARY,
            font=("Segoe UI Emoji", 48),
        ).pack(pady=(40, 10))

        tk.Label(
            placeholder, text="Search for a city to see the current weather",
            bg=Colors.BG_PRIMARY, fg=Colors.TEXT_SECONDARY,
            font=Fonts.BODY,
        ).pack()

    def _show_loading(self):
        for w in self._result_frame.winfo_children():
            w.destroy()

        loading = tk.Frame(self._result_frame, bg=Colors.BG_PRIMARY)
        loading.pack(expand=True)

        tk.Label(
            loading, text="⏳", bg=Colors.BG_PRIMARY,
            font=("Segoe UI Emoji", 36),
        ).pack(pady=(40, 10))

        self._loading_label = tk.Label(
            loading, text="Fetching weather...",
            bg=Colors.BG_PRIMARY, fg=Colors.TEXT_SECONDARY,
            font=Fonts.BODY,
        )
        self._loading_label.pack()

    def _show_error(self, message):
        for w in self._result_frame.winfo_children():
            w.destroy()

        error_frame = tk.Frame(self._result_frame, bg=Colors.BG_PRIMARY)
        error_frame.pack(expand=True)

        tk.Label(
            error_frame, text="⚠️", bg=Colors.BG_PRIMARY,
            font=("Segoe UI Emoji", 36),
        ).pack(pady=(40, 10))

        tk.Label(
            error_frame, text=message,
            bg=Colors.BG_PRIMARY, fg=Colors.ACCENT_DANGER,
            font=Fonts.BODY, wraplength=400,
        ).pack()

    def _show_weather(self, data):
        for w in self._result_frame.winfo_children():
            w.destroy()

        # ── Main card ────────────────────────────────────────
        card = tk.Frame(self._result_frame, bg=Colors.BG_SECONDARY, padx=30, pady=24)
        card.pack(fill="x", pady=(20, 0))

        # City name + emoji
        top_row = tk.Frame(card, bg=Colors.BG_SECONDARY)
        top_row.pack(fill="x")

        tk.Label(
            top_row, text=data["emoji"], bg=Colors.BG_SECONDARY,
            font=("Segoe UI Emoji", 48),
        ).pack(side="left", padx=(0, 16))

        city_info = tk.Frame(top_row, bg=Colors.BG_SECONDARY)
        city_info.pack(side="left", fill="x", expand=True)

        tk.Label(
            city_info, text=data["city"], bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY, font=Fonts.HEADING_1, anchor="w",
        ).pack(fill="x")

        tk.Label(
            city_info, text=data["description"], bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_SECONDARY, font=Fonts.BODY, anchor="w",
        ).pack(fill="x")

        # Temperature
        tk.Label(
            top_row, text=f'{data["temp_c"]}°C', bg=Colors.BG_SECONDARY,
            fg=Colors.ACCENT_INFO, font=(Fonts.FAMILY, 42, "bold"),
        ).pack(side="right")

        # Separator
        tk.Frame(card, bg=Colors.BORDER, height=1).pack(fill="x", pady=16)

        # Detail grid
        details = tk.Frame(card, bg=Colors.BG_SECONDARY)
        details.pack(fill="x")

        detail_items = [
            ("🌡️  Feels Like", f'{data["feels_like_c"]}°C'),
            ("💧  Humidity", f'{data["humidity"]}%'),
            ("💨  Wind", f'{data["wind_kph"]} km/h {data["wind_dir"]}'),
            ("☀️  UV Index", data["uv_index"]),
            ("🌡️  Temp (F)", f'{data["temp_f"]}°F'),
            ("👁️  Visibility", f'{data["visibility_km"]} km'),
        ]

        for i, (label, value) in enumerate(detail_items):
            col = i % 3
            row = i // 3

            cell = tk.Frame(details, bg=Colors.BG_SECONDARY, padx=8, pady=8)
            cell.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

            tk.Label(
                cell, text=label, bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_SECONDARY, font=Fonts.SMALL, anchor="w",
            ).pack(fill="x")

            tk.Label(
                cell, text=str(value), bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_PRIMARY, font=Fonts.HEADING_3, anchor="w",
            ).pack(fill="x")

        details.columnconfigure(0, weight=1)
        details.columnconfigure(1, weight=1)
        details.columnconfigure(2, weight=1)

    def _fetch_weather(self):
        city = self._city_entry.get().strip()
        if not city or city == "Enter city name...":
            return

        self._last_city = city
        self._show_loading()

        def _do_fetch():
            try:
                data = get_weather(city)
                self.after(0, lambda: self._show_weather(data))
            except ValueError as e:
                self.after(0, lambda: self._show_error(str(e)))
            except Exception as e:
                self.after(0, lambda: self._show_error(f"Unexpected error: {e}"))

        thread = threading.Thread(target=_do_fetch, daemon=True)
        thread.start()
