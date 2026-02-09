import sys
from src.core.vault_engine import VaultEngine

def run(args):
    """
    Handles the 'journal' command.
    Usage: xsv journal "My log entry"
    """
    vault = VaultEngine()

    if not args:
        print("Usage: xsv journal <text>")
        print("       xsv journal list")
        return

    subcmd = args[0].lower()

    if subcmd == "list":
        files = vault.list_journals()
        print(f"📚 Found {len(files)} Journal Days:")
        for f in files:
            print(f" - {f}")
    else:
        # Treat all arguments as the log message
        message = " ".join(args)
        path = vault.log_journal(message)
        
        if path:
            print(f"✅ Logged to: {path}")