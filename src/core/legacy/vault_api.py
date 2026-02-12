import os
import datetime
import json
from pathlib import Path

class VaultAPI:
    def __init__(self):
        # Dynamically find the project root relative to this file
        self.root = Path(__file__).parent.parent.parent
        self.vault_dir = self.root / "data" / "vault"
        
        # Tiered Data Structure
        self.folders = {
            "journal": self.vault_dir / "journal",
            "notes": self.vault_dir / "notes",
            "todo": self.vault_dir / "todo",
            "reminders": self.vault_dir / "reminders",
            "docs": self.vault_dir / "documents"
        }
        
        # Auto-Initialize: Sync-ready structure
        for folder in self.folders.values():
            folder.mkdir(parents=True, exist_ok=True)

    # --- TODO SYSTEM (JSON-DB) ---
    def get_tasks(self, category="work"):
        """Reads a category-specific JSON file."""
        file_path = self.folders["todo"] / f"{category.lower()}.json"
        if not file_path.exists():
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_tasks(self, category, tasks):
        """Saves a list of tasks to a specific category file."""
        file_path = self.folders["todo"] / f"{category.lower()}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

    # --- JOURNAL & NOTES (MD/TEXT) ---
    def append_journal(self, title, content):
        """Appends to the daily markdown log."""
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        target = self.folders["journal"] / f"{date_str}.md"
        timestamp = datetime.datetime.now().strftime("%I:%M %p")
        
        header = f"# Journal: {date_str}\n\n" if not target.exists() else ""
        entry = f"\n## {timestamp} - {title}\n{content}\n\n---\n"
        
        with open(target, "a", encoding="utf-8") as f:
            f.write(header + entry)
        return target

    # --- REMINDER ENGINE HOOKS ---
    def get_all_due_tasks(self):
        """Scans across all JSON categories for active reminders."""
        due_list = []
        for file in self.folders["todo"].glob("*.json"):
            cat = file.stem
            tasks = self.get_tasks(cat)
            for t in tasks:
                # Logic: Has a due date and hasn't been alerted yet
                if t.get("due_date") and not t.get("notified"):
                    due_list.append({"category": cat, "task": t})
        return due_list