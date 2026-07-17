"""
theme.py — Dark theme color palette, fonts, and styling helpers for Tkinter.
"""

import tkinter as tk
from tkinter import ttk


# ── Color Palette ─────────────────────────────────────────────

class Colors:
    # Backgrounds
    BG_PRIMARY      = "#0f0f1a"      # Deep dark navy
    BG_SECONDARY    = "#1a1a2e"      # Card / panel background
    BG_TERTIARY     = "#16213e"      # Elevated surface
    BG_INPUT        = "#1e2a45"      # Input fields
    BG_HOVER        = "#253354"      # Hover state

    # Accents
    ACCENT_PRIMARY  = "#6c63ff"      # Purple-violet (primary action)
    ACCENT_HOVER    = "#7b73ff"      # Lighter accent on hover
    ACCENT_SUCCESS  = "#00c9a7"      # Teal green (success / complete)
    ACCENT_WARNING  = "#ffc75f"      # Warm amber (warnings)
    ACCENT_DANGER   = "#ff6b6b"      # Coral red (delete / error)
    ACCENT_INFO     = "#48dbfb"      # Sky blue (info / weather)

    # Text
    TEXT_PRIMARY    = "#e8e8f0"       # Main text
    TEXT_SECONDARY  = "#9a9ab0"       # Subtle / muted text
    TEXT_DISABLED   = "#555570"       # Disabled text
    TEXT_INVERSE    = "#0f0f1a"       # Text on light/accent bg

    # Borders
    BORDER          = "#2a2a4a"       # Subtle border
    BORDER_FOCUS    = "#6c63ff"       # Focus ring

    # Overlay
    OVERLAY         = "#000000cc"     # Semi-transparent overlay


class Fonts:
    FAMILY       = "Segoe UI"
    FAMILY_MONO  = "Cascadia Code"

    HEADING_1    = (FAMILY, 22, "bold")
    HEADING_2    = (FAMILY, 16, "bold")
    HEADING_3    = (FAMILY, 13, "bold")
    BODY         = (FAMILY, 11)
    BODY_BOLD    = (FAMILY, 11, "bold")
    SMALL        = (FAMILY, 9)
    SMALL_BOLD   = (FAMILY, 9, "bold")
    MONO         = (FAMILY_MONO, 11)
    EMOJI        = ("Segoe UI Emoji", 28)
    EMOJI_LARGE  = ("Segoe UI Emoji", 48)
    QUOTE        = (FAMILY, 14, "italic")
    QUOTE_AUTHOR = (FAMILY, 11)


# ── Dimensions ────────────────────────────────────────────────

class Dims:
    PAD_XS  = 4
    PAD_SM  = 8
    PAD_MD  = 12
    PAD_LG  = 16
    PAD_XL  = 24
    PAD_XXL = 32

    RADIUS  = 8       # For canvas-drawn rounded rects
    ENTRY_H = 38      # Standard input height


# ── Style Configuration ──────────────────────────────────────

def apply_theme(root: tk.Tk):
    """Apply the dark theme to the entire application."""
    root.configure(bg=Colors.BG_PRIMARY)

    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Notebook (tabs) ──
    style.configure("TNotebook", background=Colors.BG_PRIMARY, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=Colors.BG_SECONDARY,
        foreground=Colors.TEXT_SECONDARY,
        padding=(20, 10),
        font=Fonts.BODY_BOLD,
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", Colors.BG_TERTIARY)],
        foreground=[("selected", Colors.TEXT_PRIMARY)],
    )

    # ── Frames ──
    style.configure("TFrame", background=Colors.BG_PRIMARY)
    style.configure("Card.TFrame", background=Colors.BG_SECONDARY)
    style.configure("Elevated.TFrame", background=Colors.BG_TERTIARY)

    # ── Labels ──
    style.configure("TLabel", background=Colors.BG_PRIMARY,
                     foreground=Colors.TEXT_PRIMARY, font=Fonts.BODY)
    style.configure("Card.TLabel", background=Colors.BG_SECONDARY,
                     foreground=Colors.TEXT_PRIMARY, font=Fonts.BODY)
    style.configure("Heading.TLabel", background=Colors.BG_PRIMARY,
                     foreground=Colors.TEXT_PRIMARY, font=Fonts.HEADING_2)
    style.configure("Secondary.TLabel", background=Colors.BG_PRIMARY,
                     foreground=Colors.TEXT_SECONDARY, font=Fonts.SMALL)
    style.configure("Accent.TLabel", background=Colors.BG_PRIMARY,
                     foreground=Colors.ACCENT_PRIMARY, font=Fonts.BODY_BOLD)
    style.configure("Success.TLabel", background=Colors.BG_PRIMARY,
                     foreground=Colors.ACCENT_SUCCESS, font=Fonts.BODY)
    style.configure("Danger.TLabel", background=Colors.BG_PRIMARY,
                     foreground=Colors.ACCENT_DANGER, font=Fonts.BODY)

    # ── Buttons ──
    style.configure(
        "Accent.TButton",
        background=Colors.ACCENT_PRIMARY,
        foreground=Colors.TEXT_PRIMARY,
        font=Fonts.BODY_BOLD,
        borderwidth=0,
        padding=(16, 8),
    )
    style.map(
        "Accent.TButton",
        background=[("active", Colors.ACCENT_HOVER), ("pressed", Colors.ACCENT_PRIMARY)],
    )

    style.configure(
        "Danger.TButton",
        background=Colors.ACCENT_DANGER,
        foreground=Colors.TEXT_PRIMARY,
        font=Fonts.SMALL_BOLD,
        borderwidth=0,
        padding=(8, 4),
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#ff8787")],
    )

    style.configure(
        "Success.TButton",
        background=Colors.ACCENT_SUCCESS,
        foreground=Colors.TEXT_INVERSE,
        font=Fonts.BODY_BOLD,
        borderwidth=0,
        padding=(16, 8),
    )
    style.map(
        "Success.TButton",
        background=[("active", "#33d4b5")],
    )

    style.configure(
        "Ghost.TButton",
        background=Colors.BG_SECONDARY,
        foreground=Colors.TEXT_SECONDARY,
        font=Fonts.SMALL_BOLD,
        borderwidth=0,
        padding=(12, 6),
    )
    style.map(
        "Ghost.TButton",
        background=[("active", Colors.BG_HOVER)],
        foreground=[("active", Colors.TEXT_PRIMARY)],
    )

    # ── Scrollbar ──
    style.configure(
        "TScrollbar",
        background=Colors.BG_SECONDARY,
        troughcolor=Colors.BG_PRIMARY,
        borderwidth=0,
        arrowsize=0,
    )

    # ── Separator ──
    style.configure("TSeparator", background=Colors.BORDER)

    # ── Spinbox ──
    style.configure(
        "TSpinbox",
        fieldbackground=Colors.BG_INPUT,
        background=Colors.BG_SECONDARY,
        foreground=Colors.TEXT_PRIMARY,
        borderwidth=1,
        arrowsize=14,
    )

    return style


def make_entry(parent, **kwargs) -> tk.Entry:
    """Create a styled dark-themed Entry widget."""
    defaults = dict(
        bg=Colors.BG_INPUT,
        fg=Colors.TEXT_PRIMARY,
        insertbackground=Colors.ACCENT_PRIMARY,
        relief="flat",
        font=Fonts.BODY,
        highlightthickness=2,
        highlightbackground=Colors.BORDER,
        highlightcolor=Colors.BORDER_FOCUS,
    )
    defaults.update(kwargs)
    return tk.Entry(parent, **defaults)


def make_text(parent, **kwargs) -> tk.Text:
    """Create a styled dark-themed Text widget."""
    defaults = dict(
        bg=Colors.BG_INPUT,
        fg=Colors.TEXT_PRIMARY,
        insertbackground=Colors.ACCENT_PRIMARY,
        relief="flat",
        font=Fonts.BODY,
        highlightthickness=2,
        highlightbackground=Colors.BORDER,
        highlightcolor=Colors.BORDER_FOCUS,
        wrap="word",
    )
    defaults.update(kwargs)
    return tk.Text(parent, **defaults)


def make_listbox(parent, **kwargs) -> tk.Listbox:
    """Create a styled dark-themed Listbox widget."""
    defaults = dict(
        bg=Colors.BG_SECONDARY,
        fg=Colors.TEXT_PRIMARY,
        selectbackground=Colors.ACCENT_PRIMARY,
        selectforeground=Colors.TEXT_PRIMARY,
        relief="flat",
        font=Fonts.BODY,
        highlightthickness=0,
        activestyle="none",
        borderwidth=0,
    )
    defaults.update(kwargs)
    return tk.Listbox(parent, **defaults)
