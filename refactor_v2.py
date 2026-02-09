import os
from pathlib import Path

# --- CONFIGURATION ---
PROJECT_ROOT = Path(".")
SRC_DIR = PROJECT_ROOT / "src"
CORE_DIR = SRC_DIR / "core"
CMD_DIR = SRC_DIR / "commands"

def write_file(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # .strip() removes the leading/trailing whitespace from our template
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Created: {path}")

def delete_file(path):
    p = Path(path)
    if p.exists():
        try:
            os.remove(p)
            print(f"🗑️  Deleted: {path}")
        except:
            print(f"⚠️  Could not delete: {path}")

# --- FILE CONTENTS (Safe Raw Strings) ---

# 1. VAULT API (The Brain)
VAULT_API_CODE = r"""
import os
import datetime
import json
from pathlib import Path

class VaultAPI:
    def __init__(self):
        # Dynamically find the project root
        self.root = Path(__file__).parent.parent.parent
        self.data_dir = self.root / "data"
        self.vault_dir = self.data_dir / "vault"
        
        self.journal_dir = self.vault_dir / "journal"
        self.lists_dir = self.vault_dir / "lists"
        
        # Ensure Critical Folders Exist
        for d in [self.journal_dir, self.lists_dir]:
            d.mkdir(parents=True, exist_ok=True)

    # --- JOURNAL SYSTEM ---
    def get_journal_path(self, date_str=None):
        if not date_str:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        return self.journal_dir / f"{date_str}.md"

    def append_journal(self, title, content):
        target = self.get_journal_path()
        now = datetime.datetime.now()
        timestamp = now.strftime("%I:%M %p")
        
        # Create header if new day
        header = ""
        if not target.exists():
            header = f"# Journal: {now.strftime('%Y-%m-%d')}\n\n"
            
        entry = f"\n## {timestamp} - {title}\n{content}\n\n---\n"
        
        try:
            with open(target, "a", encoding="utf-8") as f:
                if header: f.write(header)
                f.write(entry)
            return True, target
        except Exception as e:
            return False, str(e)

    def read_journal(self, date_str=None):
        target = self.get_journal_path(date_str)
        if not target.exists():
            return "📭 No entries found."
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

    # --- LISTS / TODO SYSTEM ---
    def get_list_path(self, list_name="todo"):
        return self.lists_dir / f"{list_name}.md"

    def add_todo(self, item, list_name="todo"):
        target = self.get_list_path(list_name)
        # Format: - [ ] Buy Milk
        entry = f"- [ ] {item}\n"
        with open(target, "a", encoding="utf-8") as f:
            f.write(entry)
        return target

    def get_todos(self, list_name="todo"):
        target = self.get_list_path(list_name)
        if not target.exists():
            return []
        with open(target, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Return list of (index, text, is_done)
        todos = []
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("- [ ]"):
                todos.append({"id": i, "text": line[6:], "done": False, "raw": line})
            elif line.startswith("- [x]"):
                todos.append({"id": i, "text": line[6:], "done": True, "raw": line})
        return todos

    def complete_todo(self, index, list_name="todo"):
        target = self.get_list_path(list_name)
        if not target.exists(): return False
        
        with open(target, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if 0 <= index < len(lines):
            if lines[index].startswith("- [ ]"):
                lines[index] = lines[index].replace("- [ ]", "- [x]", 1)
                with open(target, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                return True
        return False
"""

# 2. JOURNAL COMMAND (The Interface)
CMD_JOURNAL_CODE = r"""
import sys
from src.core.vault_api import VaultAPI
from src.core.host_bridge import HostBridge

def run(args):
    api = VaultAPI()
    if not args:
        print("Usage: xsv journal <add|view|open> [args]")
        return

    cmd = args[0].lower()

    if cmd == "add":
        if len(args) < 2:
            print("Usage: xsv journal add 'Title' 'Content'")
            return
        # If user provides 1 arg, treat as content with generic title
        if len(args) == 2:
            title = "Note"
            content = args[1]
        else:
            title = args[1]
            content = " ".join(args[2:])
            
        success, res = api.append_journal(title, content)
        if success: print(f"✅ Saved to {res.name}")

    elif cmd == "view":
        print(api.read_journal())

    elif cmd == "open":
        path = api.get_journal_path()
        if not path.exists(): api.append_journal("Init", "Log started.")
        print(f"🚀 Opening {path.name}...")
        HostBridge.launch(str(path))
    else:
        print("Unknown command.")
"""

# 3. TODO COMMAND (The New Feature)
CMD_TODO_CODE = r"""
import sys
from src.core.vault_api import VaultAPI

def run(args):
    api = VaultAPI()
    if not args:
        print("Usage:")
        print("  xsv todo add 'Buy Milk'")
        print("  xsv todo list")
        print("  xsv todo done <ID>")
        return

    cmd = args[0].lower()

    if cmd == "add":
        if len(args) < 2: return
        item = " ".join(args[1:])
        api.add_todo(item)
        print(f"✅ Added: {item}")

    elif cmd == "list":
        todos = api.get_todos()
        print("\n📝 TODO LIST:")
        for t in todos:
            icon = "✅" if t['done'] else "⬜"
            # Color code index for easy reading
            print(f" {t['id']} {icon} {t['text']}")
        print("")

    elif cmd == "done":
        if len(args) < 2: return
        try:
            idx = int(args[1])
            if api.complete_todo(idx):
                print(f"🎉 Task {idx} Complete!")
            else:
                print("❌ Invalid ID")
        except:
            print("❌ ID must be a number")
"""

# 4. MAIN ROUTER (The Switchboard)
MAIN_CODE = r"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.host_bridge import HostBridge
from src.commands import cmd_journal, cmd_todo

def main():
    if len(sys.argv) < 2:
        HostBridge.clear_screen()
        print("xsvCommandCenter [v2.0-API]")
        print("---------------------------")
        print("Commands:")
        print("  host [info|launch]   - OS Control")
        print("  journal [add|view]   - Daily Logs")
        print("  todo [add|list|done] - Task Manager")
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == "host":
        if not args: return
        sub = args[0]
        if sub == "info": print(HostBridge.get_system_info())
        elif sub == "launch": HostBridge.launch(args[1])
    
    elif cmd == "journal":
        cmd_journal.run(args)
    
    elif cmd == "todo":
        cmd_todo.run(args)
        
    else:
        print(f"❌ Unknown command: {cmd}")

if __name__ == "__main__":
    main()
"""

def run_refactor():
    print("🚀 Starting Refactor V2.0 (Safe Mode)...")
    
    # 1. Clean up Legacy
    delete_file(CORE_DIR / "vault_engine.py")

    # 2. Write New Files
    write_file(CORE_DIR / "vault_api.py", VAULT_API_CODE)
    write_file(CMD_DIR / "cmd_journal.py", CMD_JOURNAL_CODE)
    write_file(CMD_DIR / "cmd_todo.py", CMD_TODO_CODE)
    write_file(SRC_DIR / "main.py", MAIN_CODE)

    print("\n✅ Refactor Complete.")
    print("Test command: .\\xsv.bat todo add \"System Check\"")

if __name__ == "__main__":
    run_refactor()