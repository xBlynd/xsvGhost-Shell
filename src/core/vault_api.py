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
        
        # New Category-based Folders
        self.journal_dir = self.vault_dir / "journal"
        self.notes_dir = self.vault_dir / "notes"
        self.todo_dir = self.vault_dir / "todo"
        self.reminders_dir = self.vault_dir / "reminders"
        self.docs_dir = self.vault_dir / "documents"
        
        # Ensure all core vault folders exist [cite: 125, 144]
        for d in [self.journal_dir, self.notes_dir, self.todo_dir, self.reminders_dir, self.docs_dir]:
            d.mkdir(parents=True, exist_ok=True)

    # --- NEW DYNAMIC TODO SYSTEM ---
    def get_tasks(self, category="work"):
        """Reads a category-specific JSON file (e.g., work.json)."""
        file_path = self.todo_dir / f"{category.lower()}.json"
        if not file_path.exists():
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_tasks(self, category, tasks):
        """Saves tasks to their specific category file."""
        file_path = self.todo_dir / f"{category.lower()}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

    # --- JOURNAL SYSTEM (Existing Workflow Maintained) ---
    def get_journal_path(self, date_str=None):
        if not date_str:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        return self.journal_dir / f"{date_str}.md"

    def append_journal(self, title, content):
        target = self.get_journal_path()
        now = datetime.datetime.now()
        timestamp = now.strftime("%I:%M %p")
        
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

    # --- REMINDER HOOKS ---
    def get_all_due_tasks(self):
        """Used by the Reminder Engine to scan across ALL categories."""
        all_due = []
        for file in self.todo_dir.glob("*.json"):
            category = file.stem
            tasks = self.get_tasks(category)
            for t in tasks:
                if t.get("due_date") and not t.get("notified"):
                    all_due.append({"category": category, "task": t})
        return all_due