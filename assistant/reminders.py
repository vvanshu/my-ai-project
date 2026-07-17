"""
reminders.py — Simple reminder scheduler using Tkinter's after() mechanism.
"""

import uuid
from datetime import datetime, timedelta


class ReminderManager:
    """
    Manages timed reminders that trigger popup notifications.
    Relies on a Tkinter root window for scheduling via .after().
    """

    def __init__(self):
        self._reminders = {}  # id -> {text, fire_at, after_id, callback}
        self._root = None

    def set_root(self, root):
        """Attach the Tkinter root window for scheduling."""
        self._root = root

    def add_reminder(self, text: str, minutes: int, callback=None) -> str:
        """
        Schedule a reminder.

        Args:
            text:     The reminder message.
            minutes:  Minutes from now until the reminder fires.
            callback: Function to call with (reminder_id, text) when it fires.

        Returns:
            The reminder ID string.
        """
        if not self._root:
            raise RuntimeError("ReminderManager has no Tkinter root. Call set_root() first.")

        if minutes < 1:
            raise ValueError("Reminder must be at least 1 minute in the future.")

        reminder_id = uuid.uuid4().hex[:8]
        fire_at = datetime.now() + timedelta(minutes=minutes)
        delay_ms = minutes * 60 * 1000

        def _fire():
            if reminder_id in self._reminders:
                info = self._reminders.pop(reminder_id)
                if callback:
                    callback(reminder_id, info["text"])

        after_id = self._root.after(delay_ms, _fire)

        self._reminders[reminder_id] = {
            "text": text.strip(),
            "fire_at": fire_at.isoformat(),
            "fire_at_display": fire_at.strftime("%I:%M %p"),
            "after_id": after_id,
            "minutes": minutes,
        }

        return reminder_id

    def cancel_reminder(self, reminder_id: str) -> bool:
        """Cancel a pending reminder. Returns True if found and cancelled."""
        if reminder_id in self._reminders:
            info = self._reminders.pop(reminder_id)
            if self._root:
                try:
                    self._root.after_cancel(info["after_id"])
                except (ValueError, Exception):
                    pass
            return True
        return False

    def cancel_all(self):
        """Cancel all pending reminders."""
        for rid in list(self._reminders.keys()):
            self.cancel_reminder(rid)

    def get_active(self) -> list[dict]:
        """Return a list of active reminder dicts."""
        return [
            {"id": rid, **info}
            for rid, info in self._reminders.items()
        ]

    @property
    def count(self) -> int:
        return len(self._reminders)
