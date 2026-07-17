"""
todo.py — To-do list manager with JSON persistence.
"""

import json
import os
import uuid
from datetime import datetime


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TODOS_FILE = os.path.join(DATA_DIR, "todos.json")


class TodoManager:
    """Manages a persistent to-do list stored as JSON."""

    def __init__(self):
        self._tasks = []
        self._ensure_data_dir()
        self._load()

    # ── Public API ────────────────────────────────────────────

    def add_task(self, text: str) -> dict:
        """Add a new task and persist."""
        task = {
            "id": uuid.uuid4().hex[:8],
            "text": text.strip(),
            "completed": False,
            "created_at": datetime.now().isoformat(),
        }
        self._tasks.append(task)
        self._save()
        return task

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID. Returns True if found and removed."""
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if t["id"] != task_id]
        if len(self._tasks) < before:
            self._save()
            return True
        return False

    def toggle_complete(self, task_id: str) -> bool:
        """Toggle the completed state of a task. Returns new state."""
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                self._save()
                return task["completed"]
        return False

    def get_all(self) -> list:
        """Return all tasks."""
        return list(self._tasks)

    def get_pending(self) -> list:
        """Return only incomplete tasks."""
        return [t for t in self._tasks if not t["completed"]]

    def get_completed(self) -> list:
        """Return only completed tasks."""
        return [t for t in self._tasks if t["completed"]]

    def clear_completed(self) -> int:
        """Remove all completed tasks. Returns count removed."""
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if not t["completed"]]
        removed = before - len(self._tasks)
        if removed:
            self._save()
        return removed

    @property
    def total_count(self) -> int:
        return len(self._tasks)

    @property
    def pending_count(self) -> int:
        return len(self.get_pending())

    @property
    def completed_count(self) -> int:
        return len(self.get_completed())

    # ── Private helpers ───────────────────────────────────────

    def _ensure_data_dir(self):
        os.makedirs(DATA_DIR, exist_ok=True)

    def _load(self):
        if os.path.exists(TODOS_FILE):
            try:
                with open(TODOS_FILE, "r", encoding="utf-8") as f:
                    self._tasks = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._tasks = []
        else:
            self._tasks = []

    def _save(self):
        self._ensure_data_dir()
        with open(TODOS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._tasks, f, indent=2, ensure_ascii=False)
