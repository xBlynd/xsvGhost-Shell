import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.host_bridge import HostBridge
from src.commands import cmd_journal, cmd_todo

def main():
    if len(sys.argv) < 2:
        HostBridge.clear_screen()
        print("xsvCommandCenter [v2.0-API]")
        print("---------------------------")
        print("Commands:")
        print("  host [info|launch]   - OS Control")
        print("  journal [add|view]   - Daily Logs")
        print("  todo [add|list|done] - Task Manager")
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == "host":
        if not args: return
        sub = args[0]
        if sub == "info": print(HostBridge.get_system_info())
        elif sub == "launch": HostBridge.launch(args[1])
    
    elif cmd == "journal":
        cmd_journal.run(args)
    
    elif cmd == "todo":
        cmd_todo.run(args)
        
    else:
        print(f"❌ Unknown command: {cmd}")

if __name__ == "__main__":
    main()