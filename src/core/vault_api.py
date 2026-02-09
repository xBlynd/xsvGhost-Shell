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