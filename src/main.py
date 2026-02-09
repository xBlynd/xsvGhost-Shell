import sys
from pathlib import Path

# Add 'src' to python path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.host_bridge import HostBridge
from src.commands import cmd_journal

def main():
    # 1. Grab arguments
    if len(sys.argv) < 2:
        HostBridge.clear_screen()
        print("xsvCommandCenter [v0.2-Alpha]")
        print("-----------------------------")
        print("Usage: xsv <command> [args]")
        print("   host info          - Show System Stats")
        print("   host launch <file> - Open a file")
        print("   journal <text>     - Log an entry")
        print("   journal list       - See past logs")
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    # 2. Command Routing
    if command == "host":
        if not args:
            print("Usage: xsv host [info|launch]")
            return
        
        subcmd = args[0].lower()
        if subcmd == "info":
            info = HostBridge.get_system_info()
            print(f"🖥️  System: {info['os']} {info['release']}")
            print(f"👤 User:   {info['user']}")
            if info['is_wsl']: print("🐧 Mode:   WSL")
        
        elif subcmd == "launch":
            if len(args) < 2:
                print("Error: Missing file path.")
            else:
                HostBridge.launch(args[1])

    elif command == "journal":
        cmd_journal.run(args)
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()