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