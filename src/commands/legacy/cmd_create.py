import sys
import os
import importlib
from pathlib import Path

# --- CONFIG ---
# We point to where the CUSTOM commands live
CUSTOM_DIR = Path(__file__).parent / "custom"

def create_command_wizard(name=None):
    """
    Handles the creation of NEW scripts/tools (The 'Custom' stuff).
    This logic lives HERE because 'creating a command' is this module's job.
    """
    print("\n 🛠️  CREATE CUSTOM COMMAND")
    print(" " + "="*30)

    if not name:
        name = input(" [?] Command Name (One word): ").lower().strip()
    
    if not name: return

    filename = f"cmd_{name}.py"
    filepath = CUSTOM_DIR / filename
    
    if filepath.exists():
        print(f" ⚠️  Warning: '{name}' already exists.")
        if input("     Overwrite? (y/n): ").lower() != 'y': return

    desc = input(" [?] Description: ").strip()

    print("\n [?] Paste Python code. Type 'END' or 'DONE' on new line to finish.")
    lines = []
    while True:
        line = input()
        if line.strip().upper() in ["END", "DONE"]: break
        lines.append(line)
    
    user_code = "\n    ".join(lines)
    
    file_content = f'''import sys
import os

# Module: {name}
# Description: {desc}

def run(args):
    print("\\n🚀 Running Custom Command: {name}...")
    
    # --- USER CODE START ---
    {user_code}
    # --- USER CODE END ---
    
    print("\\n✅ {name} finished.")
'''

    # Ensure dir exists
    CUSTOM_DIR.mkdir(parents=True, exist_ok=True)
    if not (CUSTOM_DIR / "__init__.py").exists():
        (CUSTOM_DIR / "__init__.py").touch()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(file_content)

    print(f" ✅ Created command '{name}' in src/commands/custom/")

def run(args):
    """
    The Master Dispatcher.
    Routes 'todo' to the Todo Module, 'journal' to the Journal Module.
    """
    if not args:
        print("\n✨ CREATION STATION")
        print("Usage:")
        print("  create command <name>   -> Build a new tool (Wizard)")
        print("  create todo <text>      -> Dispatches to Core Todo Module")
        print("  create journal <text>   -> Dispatches to Core Journal Module")
        return

    category = args[0].lower()
    payload = args[1:] # The rest of the words

    # --- ROUTE 1: NEW COMMANDS (Handled Here) ---
    if category in ["command", "script", "module"]:
        name = payload[0] if payload else None
        create_command_wizard(name)

    # --- ROUTE 2: CORE TODO MODULE ---
    elif category in ["todo", "task"]:
        try:
            # We import the CORE module dynamically
            # This ensures we use the EXACT logic defined in cmd_todo.py
            todo_module = importlib.import_module("src.commands.cmd_todo")
            
            # We construct the arguments as if the user typed 'todo add ...'
            # If payload is ["Buy", "Milk"], we send ["add", "Buy", "Milk"]
            dispatch_args = ["add"] + payload
            
            print(f" ↪️  Dispatching to Core Todo Module...")
            todo_module.run(dispatch_args)
            
        except ModuleNotFoundError:
            print(" ❌ Error: Core 'cmd_todo.py' not found!")
        except Exception as e:
            print(f" ❌ Dispatch Error: {e}")

    # --- ROUTE 3: CORE JOURNAL MODULE ---
    elif category in ["journal", "note", "log"]:
        try:
            journal_module = importlib.import_module("src.commands.cmd_journal")
            
            # Construct args: 'journal add ...'
            dispatch_args = ["add"] + payload
            
            print(f" ↪️  Dispatching to Core Journal Module...")
            journal_module.run(dispatch_args)
            
        except ModuleNotFoundError:
            print(" ❌ Error: Core 'cmd_journal.py' not found!")
        except Exception as e:
            print(f" ❌ Dispatch Error: {e}")

    else:
        print(f" ❌ Unknown category '{category}'.")
        print("    Supported: command, todo, journal")