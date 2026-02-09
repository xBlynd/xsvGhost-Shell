import sys
import os
import json
from pathlib import Path

# CONSTANTS
PROJECT_ROOT = Path(__file__).parent.parent.parent
COMMANDS_JSON = PROJECT_ROOT / "data" / "config" / "commands.json"
COMMANDS_DIR = PROJECT_ROOT / "src" / "commands"

def load_json():
    if not COMMANDS_JSON.exists(): return {}
    with open(COMMANDS_JSON, "r") as f: return json.load(f)

def save_json(data):
    with open(COMMANDS_JSON, "w") as f: json.dump(data, f, indent=4)

def create_alias(name):
    print(f"\n[Creating Alias: '{name}']")
    desc = input("Description: ")
    cmd = input("Shell Command to Run (e.g., 'ipconfig /all'): ")
    
    data = load_json()
    data[name] = {
        "type": "shell",
        "cmd": cmd,
        "description": desc
    }
    save_json(data)
    print(f"✅ Alias '{name}' created! Type '{name}' to run it.")

def create_module(name):
    print(f"\n[Creating Python Module: '{name}']")
    desc = input("Description: ")
    
    # Python Filename
    filename = f"cmd_{name}.py"
    filepath = COMMANDS_DIR / filename
    
    if filepath.exists():
        print(f"❌ Error: {filename} already exists!")
        return

    # The Template
    code = f'''import sys
import os

# Module: {name}
# Description: {desc}

def run(args):
    print("\\n🚀 Running {name}...")
    
    # --- YOUR CODE BELOW ---
    print("TODO: Add logic for {desc}")
    
    # Example:
    # if args and args[0] == "test":
    #     print("Test mode")
    
    print("✅ Done.")
'''
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
        
    print(f"✅ Module '{filename}' created!")
    print(f"   Location: src/commands/{filename}")
    print(f"   Action: Open that file and paste your AI code.")

def run(args):
    print("\n🛠️  COMMAND FACTORY")
    print("-------------------")
    
    if not args:
        name = input("Enter new command name: ").lower().strip()
    else:
        name = args[0].lower().strip()

    if not name: return

    print("Type of Command:")
    print("  1. Alias/Shortcut (Runs a one-line shell command)")
    print("  2. Python Module  (Complex logic, menus, advanced tools)")
    
    choice = input("Select [1/2]: ").strip()
    
    if choice == "1":
        create_alias(name)
    elif choice == "2":
        create_module(name)
    else:
        print("❌ Invalid choice.")