# ✦ Desktop Assistant

A sleek, dark-themed Python desktop assistant built with Tkinter. Manage your to-dos, check live weather, get motivational quotes, and set reminders — all from one window.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📋 **To-Do List** | Add, complete, delete, and filter tasks. Persisted to JSON across sessions. |
| 🌤️ **Weather** | Live weather lookup for any city via the free [wttr.in](https://wttr.in) API — no API key needed. |
| 💡 **Quotes** | 50 curated motivational quotes with daily and random modes. |
| ⏰ **Reminders** | Schedule timed popup reminders (1–1440 minutes). |

## 🚀 Getting Started

### Prerequisites

- Python 3.10+  
- `pip` (Python package manager)

### Installation

```bash
# Clone the repo
git clone https://github.com/vvanshu/my-ai-project.git
cd my-ai-project

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## 📁 Project Structure

```
my-ai-project/
├── main.py                 # Entry point
├── assistant/
│   ├── __init__.py
│   ├── todo.py             # To-do list logic + JSON persistence
│   ├── weather.py          # Weather fetching (wttr.in)
│   ├── quotes.py           # Curated motivational quotes
│   └── reminders.py        # Timed reminder scheduler
├── ui/
│   ├── __init__.py
│   ├── app.py              # Main window + tab layout
│   ├── todo_tab.py          # To-do list tab
│   ├── weather_tab.py       # Weather tab
│   ├── quotes_tab.py        # Quotes & reminders tab
│   └── theme.py             # Dark theme colors, fonts, styling
├── data/
│   └── todos.json           # Auto-created on first run
├── requirements.txt
└── README.md
```

## 🎨 Design

- **Dark theme** with a deep navy palette and purple-violet accents  
- **Hover effects** and smooth interactions  
- **Responsive layout** that adapts to window resizing  
- Built entirely with Python's **Tkinter** — no external UI dependencies  

## 📄 License

This project is open source and available under the [MIT License](LICENSE).