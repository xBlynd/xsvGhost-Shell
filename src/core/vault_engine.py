"""
Vault Engine - The Archive
Journal and todo management
"""

import json
from datetime import datetime
from pathlib import Path

class VaultEngine:
    """
    Manages persistent data storage.
    Journals stored as markdown, todos as JSON.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "vault"
        
        # Get vault directory
        core = kernel.engines.get('ghost_core')
        if core:
            self.vault_dir = core.get_path("data", "vault")
        else:
            self.vault_dir = Path(__file__).parent.parent.parent / "data" / "vault"
        
        self.journal_dir = self.vault_dir / "journal"
        self.todos_dir = self.vault_dir / "todos"
        
        # Ensure directories exist
        self.journal_dir.mkdir(parents=True, exist_ok=True)
        self.todos_dir.mkdir(parents=True, exist_ok=True)
    
    # ===== JOURNAL OPERATIONS =====
    
    def journal_add(self, entry, tags=None):
        """Add entry to today's journal"""
        today = datetime.now().strftime("%Y-%m-%d")
        journal_file = self.journal_dir / f"{today}.md"
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format entry
        formatted = f"\n## {timestamp}\n{entry}\n"
        
        if tags:
            tag_str = " ".join(f"#{tag}" for tag in tags)
            formatted += f"\n*Tags: {tag_str}*\n"
        
        # Append to file
        with open(journal_file, 'a', encoding='utf-8') as f:
            f.write(formatted)
        
        return True, f"Added to {today}.md"
    
    def journal_list(self, limit=10):
        """List recent journal entries"""
        files = sorted(self.journal_dir.glob("*.md"), reverse=True)
        
        if not files:
            return []
        
        entries = []
        for file in files[:limit]:
            date = file.stem
            size = file.stat().st_size
            entries.append({
                "date": date,
                "size": size,
                "path": str(file)
            })
        
        return entries
    
    def journal_read(self, date=None):
        """Read journal for specific date (or today)"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        journal_file = self.journal_dir / f"{date}.md"
        
        if not journal_file.exists():
            return None
        
        return journal_file.read_text(encoding='utf-8')
    
    # ===== TODO OPERATIONS =====
    
    def todo_add(self, task, priority="normal"):
        """Add todo item"""
        todos = self._load_todos()
        
        new_todo = {
            "id": self._next_todo_id(todos),
            "task": task,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        
        todos.append(new_todo)
        self._save_todos(todos)
        
        return True, f"Added todo #{new_todo['id']}"
    
    def todo_list(self, show_completed=False):
        """List todos"""
        todos = self._load_todos()
        
        if not show_completed:
            todos = [t for t in todos if not t.get("completed", False)]
        
        return todos
    
    def todo_complete(self, todo_id):
        """Mark todo as completed"""
        todos = self._load_todos()
        
        for todo in todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                todo["completed_at"] = datetime.now().isoformat()
                self._save_todos(todos)
                return True, f"Completed todo #{todo_id}"
        
        return False, "Todo not found"
    
    def todo_delete(self, todo_id):
        """Delete todo"""
        todos = self._load_todos()
        todos = [t for t in todos if t["id"] != todo_id]
        self._save_todos(todos)
        return True, f"Deleted todo #{todo_id}"
    
    # ===== INTERNAL HELPERS =====
    
    def _load_todos(self):
        """Load active todos"""
        todos_file = self.todos_dir / "active.json"
        
        if not todos_file.exists():
            return []
        
        try:
            return json.loads(todos_file.read_text())
        except:
            return []
    
    def _save_todos(self, todos):
        """Save todos to file"""
        todos_file = self.todos_dir / "active.json"
        todos_file.write_text(json.dumps(todos, indent=2))
    
    def _next_todo_id(self, todos):
        """Get next todo ID"""
        if not todos:
            return 1
        return max(t["id"] for t in todos) + 1
