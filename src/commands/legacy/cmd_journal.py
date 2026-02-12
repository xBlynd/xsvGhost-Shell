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