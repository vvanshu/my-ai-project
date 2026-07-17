"""Quick verification script — tests all imports and core functionality."""

import sys

try:
    from ui.app import DesktopAssistant
    from assistant import TodoManager, get_weather, get_random_quote, get_daily_quote, ReminderManager
    print("[OK] All imports successful")

    # Test TodoManager
    tm = TodoManager()
    t = tm.add_task("Test task from verification")
    assert t["text"] == "Test task from verification"
    tm.remove_task(t["id"])
    print("[OK] TodoManager: add/remove works")

    # Test quotes
    q, a = get_random_quote()
    assert len(q) > 0 and len(a) > 0
    dq, da = get_daily_quote()
    assert len(dq) > 0
    print(f"[OK] Quotes: \"{q[:50]}...\" — {a}")

    # Test ReminderManager init
    rm = ReminderManager()
    assert rm.count == 0
    print("[OK] ReminderManager initializes correctly")

    print("\n=== ALL CHECKS PASSED! The app is ready to launch. ===")
    print("    Run: python main.py")

except Exception as e:
    print(f"\n=== VERIFICATION FAILED: {e} ===", file=sys.stderr)
    sys.exit(1)
