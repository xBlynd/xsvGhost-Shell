"""
Engine 07: Vault Engine - The Archive
========================================
Data persistence: journals, todos, encrypted storage, exports.
All data lives in data/vault/ using simple files (no database dependency).

Compartmentalization:
- ONLY handles file operations
- Does NOT display data (InterfaceEngine does that)
- Works completely offline
"""

import os
import json
from datetime import datetime


class VaultEngine:
    """The Archive - data persistence and management."""

    ENGINE_NAME = "vault"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.vault_dir = os.path.join(self.root_dir, "data", "vault")
        self.journal_dir = os.path.join(self.vault_dir, "journal")
        self.todos_dir = os.path.join(self.vault_dir, "todos")
        self.encrypted_dir = os.path.join(self.vault_dir, "encrypted")

        # Ensure directories exist
        for d in [self.journal_dir, self.todos_dir, self.encrypted_dir]:
            os.makedirs(d, exist_ok=True)

    # =========================================================================
    # JOURNAL
    # =========================================================================

    def journal_add(self, entry, tags=None):
        """
        Add a journal entry to today's file.
        Entries are appended as markdown with timestamps.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        journal_file = os.path.join(self.journal_dir, f"{today}.md")

        timestamp = datetime.now().strftime("%H:%M:%S")
        tag_str = ""
        if tags:
            tag_str = " " + " ".join(f"#{t}" for t in tags)

        content = f"\n## {timestamp}{tag_str}\n{entry}\n"

        # Create file with header if new
        if not os.path.exists(journal_file):
            header = f"# Ghost Journal - {today}\n"
            content = header + content

        with open(journal_file, 'a', encoding='utf-8') as f:
            f.write(content)

        return {
            "file": journal_file,
            "date": today,
            "timestamp": timestamp,
            "entry": entry,
        }

    def journal_list(self, date=None, last_n=5):
        """List journal entries. If no date, show recent files."""
        if date:
            journal_file = os.path.join(self.journal_dir, f"{date}.md")
            if os.path.exists(journal_file):
                with open(journal_file, 'r', encoding='utf-8') as f:
                    return {"date": date, "content": f.read()}
            return {"date": date, "content": None, "error": "No entries for this date"}

        # List recent journal files
        files = sorted(
            [f for f in os.listdir(self.journal_dir) if f.endswith('.md')],
            reverse=True
        )[:last_n]

        entries = []
        for f in files:
            date_str = f.replace('.md', '')
            filepath = os.path.join(self.journal_dir, f)
            size = os.path.getsize(filepath)
            entries.append({
                "date": date_str,
                "file": f,
                "size_bytes": size,
            })

        return {"entries": entries, "total_files": len(os.listdir(self.journal_dir))}

    def journal_search(self, query):
        """Search across all journal entries."""
        results = []
        query_lower = query.lower()

        for f in sorted(os.listdir(self.journal_dir), reverse=True):
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(self.journal_dir, f)
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()
                if query_lower in content.lower():
                    results.append({
                        "date": f.replace('.md', ''),
                        "file": f,
                        "preview": self._extract_matching_lines(content, query_lower),
                    })

        return {"query": query, "results": results, "total_matches": len(results)}

    def _extract_matching_lines(self, content, query):
        """Extract lines containing the search query."""
        lines = content.split('\n')
        matches = [l.strip() for l in lines if query in l.lower()]
        return matches[:3]  # Max 3 preview lines

    # =========================================================================
    # TODOS
    # =========================================================================

    def todo_add(self, text, priority="normal"):
        """Add a todo item."""
        todos = self._load_todos()

        todo_id = len(todos["items"]) + 1
        item = {
            "id": todo_id,
            "text": text,
            "priority": priority,  # low, normal, high, critical
            "created": datetime.now().isoformat(),
            "completed": None,
            "done": False,
        }
        todos["items"].append(item)
        self._save_todos(todos)

        return item

    def todo_list(self, show_done=False):
        """List todo items."""
        todos = self._load_todos()
        items = todos["items"]

        if not show_done:
            items = [i for i in items if not i["done"]]

        return {"items": items, "total": len(todos["items"])}

    def todo_complete(self, todo_id):
        """Mark a todo as complete."""
        todos = self._load_todos()

        for item in todos["items"]:
            if item["id"] == todo_id:
                item["done"] = True
                item["completed"] = datetime.now().isoformat()
                self._save_todos(todos)
                return item

        return None

    def todo_remove(self, todo_id):
        """Remove a todo item."""
        todos = self._load_todos()
        original_count = len(todos["items"])
        todos["items"] = [i for i in todos["items"] if i["id"] != todo_id]

        if len(todos["items"]) < original_count:
            self._save_todos(todos)
            return True
        return False

    def _load_todos(self):
        """Load todos from file."""
        todo_file = os.path.join(self.todos_dir, "active.json")
        if os.path.exists(todo_file):
            try:
                with open(todo_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"items": []}

    def _save_todos(self, todos):
        """Save todos to file."""
        todo_file = os.path.join(self.todos_dir, "active.json")
        with open(todo_file, 'w', encoding='utf-8') as f:
            json.dump(todos, f, indent=2)

    # =========================================================================
    # GENERAL DATA
    # =========================================================================

    def log(self, message, category="general"):
        """Quick log to vault (used by other engines via kernel)."""
        self.journal_add(f"[{category}] {message}", tags=[category])

    def get_stats(self):
        """Return vault statistics."""
        journal_count = len([
            f for f in os.listdir(self.journal_dir) if f.endswith('.md')
        ])
        todos = self._load_todos()
        active_todos = len([i for i in todos["items"] if not i["done"]])
        done_todos = len([i for i in todos["items"] if i["done"]])

        return {
            "journal_entries": journal_count,
            "active_todos": active_todos,
            "completed_todos": done_todos,
            "vault_dir": self.vault_dir,
        }
