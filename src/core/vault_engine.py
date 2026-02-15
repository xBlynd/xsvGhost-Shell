"""
VaultEngine - The Librarian (Engine #7)
The ONLY module allowed to read/write files in data/vault/.

Responsibilities:
- CRUD operations for Notes and Journals
- Search indexing across markdown files
- Structure repair (auto-create missing folders)
- Encryption hooks (future - via SecurityEngine)
"""
import os
import datetime
import json
from pathlib import Path

class VaultEngine:
    """
    The Librarian - Engine #7
    Manages all user data in the vault with strict separation from other engines.
    """
    
    def __init__(self):
        # Dynamically find the project root relative to this file
        self.root = Path(__file__).parent.parent.parent
        self.vault_dir = self.root / "data" / "vault"
        
        # Tiered Data Structure (Compartmentalized)
        self.folders = {
            "journal": self.vault_dir / "journal",
            "notes": self.vault_dir / "notes",
            "todo": self.vault_dir / "todo",
            "reminders": self.vault_dir / "reminders",
            "docs": self.vault_dir / "documents",
            "loot": self.vault_dir / "loot"  # For silent transfer files
        }
        
        # Auto-Initialize: Self-healing structure
        # If folders are deleted, recreate them
        for folder in self.folders.values():
            folder.mkdir(parents=True, exist_ok=True)
    
    # ============================================================
    # TODO SYSTEM (JSON Database)
    # ============================================================
    def get_tasks(self, category="work"):
        """
        Reads a category-specific JSON file.
        Categories: work, home, xsv, etc.
        """
        file_path = self.folders["todo"] / f"{category.lower()}.json"
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def save_tasks(self, category, tasks):
        """
        Saves a list of tasks to a specific category file.
        This is the ONLY place tasks are written to disk.
        """
        file_path = self.folders["todo"] / f"{category.lower()}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)
    
    # ============================================================
    # JOURNAL SYSTEM (Markdown Daily Logs)
    # ============================================================
    def append_journal(self, title, content):
        """
        Appends to the daily markdown log.
        Format: YYYY-MM-DD.md
        Each day gets its own file for easy searching.
        """
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        target = self.folders["journal"] / f"{date_str}.md"
        timestamp = datetime.datetime.now().strftime("%I:%M %p")
        
        # If new file, add header
        header = f"# Journal: {date_str}\n\n" if not target.exists() else ""
        
        # Entry format with separator
        entry = f"\n## {timestamp} - {title}\n{content}\n\n---\n"
        
        with open(target, "a", encoding="utf-8") as f:
            f.write(header + entry)
        
        return target
    
    # ============================================================
    # NOTES SYSTEM (Future - Multi-Entry with Frontmatter)
    # ============================================================
    # TODO: Implement note categories and tags
    # TODO: Add search indexing for grep-style queries
    
    # ============================================================
    # REMINDER SYSTEM HOOKS
    # ============================================================
    def get_all_due_tasks(self):
        """
        Scans across all JSON categories for active reminders.
        Used by PulseEngine to check for due notifications.
        """
        due_list = []
        
        for file in self.folders["todo"].glob("*.json"):
            cat = file.stem
            tasks = self.get_tasks(cat)
            
            for t in tasks:
                # Logic: Has a due date and hasn't been alerted yet
                if t.get("due_date") and not t.get("notified"):
                    due_list.append({"category": cat, "task": t})
        
        return due_list
    
    # ============================================================
    # FUTURE: ENCRYPTION INTEGRATION
    # ============================================================
    # - Decrypt files on read (via SecurityEngine key)
    # - Encrypt files on write
    # - Never store plaintext passwords
    
    # ============================================================
    # FUTURE: SEARCH & INDEXING
    # ============================================================
    # - grep-style search across all markdown files
    # - Return: [File, Line Number, Snippet]
    # - Used by: `journal search <keyword>` command
