"""
main.py — Entry point for the Desktop Assistant application.

Usage:
    python main.py
"""

from ui.app import DesktopAssistant


def main():
    app = DesktopAssistant()
    app.run()


if __name__ == "__main__":
    main()
