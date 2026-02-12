import json
import os
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent.parent.parent / "data" / "config" / "user_settings.json"

def load_settings():
    if not SETTINGS_FILE.exists():
        return {"theme": "default", "username": "admin", "auto_connect": False}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_settings(data):
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Settings Saved.")

def run(args):
    if not args:
        print("\n⚙️  SYSTEM SETTINGS")
        print("Usage: settings [list | set <key> <value>]")
        return

    action = args[0].lower()
    data = load_settings()

    if action == "list":
        print("\n📝 Current Configuration:")
        for k, v in data.items():
            print(f"  • {k}: {v}")
        print("")

    elif action == "set":
        if len(args) < 3:
            print("❌ Usage: settings set <key> <value>")
            return
        key = args[1]
        val = args[2]
        data[key] = val
        save_settings(data)
        print(f"Updated '{key}' to '{val}'")