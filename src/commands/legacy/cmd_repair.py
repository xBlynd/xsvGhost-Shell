"""
Module: repair
Description: Deep system reconstruction and health restoration.
"""
import os
import shutil
from pathlib import Path

def run(args):
    print("\n🛠️  xsv SYSTEM REPAIR INITIATED")
    print("=" * 45)
    
    root = Path(__file__).parent.parent.parent
    
    # 1. Structure Check
    print("[1] Verifying Directory Integrity...")
    required_folders = [
        "data/vault/todo", "data/vault/journal", "data/vault/notes",
        "data/config", "src/commands/custom", "library"
    ]
    for folder in required_folders:
        path = root / folder
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Reconstructed: {folder}")
        else:
            print(f"  · {folder} OK")

    # 2. Config Restoration
    print("\n[2] Checking Core Configurations...")
    settings_path = root / "data" / "config" / "settings.json"
    if not settings_path.exists():
        default_settings = {
            "core": {"debug": True},
            "reminders": {"enabled": True, "popup": True}
        }
        import json
        with open(settings_path, "w") as f:
            json.dump(default_settings, f, indent=4)
        print("  ✅ Factory settings.json restored.")

    # 3. Cache Purge (The 'Ghost' Killer)
    print("\n[3] Purging Python Byte-Code Caches...")
    count = 0
    for p in root.rglob("__pycache__"):
        shutil.rmtree(p)
        count += 1
    print(f"  ✅ Cleared {count} cache directories.")

    print("-" * 45)
    print("✨ Repair Complete. Run 'reload' to refresh system state.")