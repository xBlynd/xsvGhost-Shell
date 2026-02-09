import os
import datetime
from pathlib import Path

class VaultEngine:
    def __init__(self):
        # Dynamically find the project root (2 levels up from this file)
        self.root = Path(__file__).parent.parent.parent
        self.vault_dir = self.root / "data" / "vault"
        self.journal_dir = self.vault_dir / "journal"
        self.notes_dir = self.vault_dir / "notes"

        # Ensure directories exist
        self.journal_dir.mkdir(parents=True, exist_ok=True)
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def log_journal(self, content):
        """Appends a timestamped entry to today's journal file."""
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # File: data/vault/journal/2026-02-09.md
        filename = self.journal_dir / f"{date_str}.md"
        
        entry = f"\n## [{time_str}] Entry\n{content}\n"
        
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(entry)
            return str(filename)
        except Exception as e:
            print(f"❌ Vault Error: {e}")
            return None

    def list_journals(self):
        """Returns a list of all journal files."""
        if not self.journal_dir.exists():
            return []
        return sorted([f.name for f in self.journal_dir.glob("*.md")])