import sys
import os
from src.core.host_bridge import HostBridge

def run(args):
    if not args:
        print("Usage: xsv host [ls|nuke|ps|info]")
        return

    cmd = args[0].lower()

    if cmd == "ls":
        target = args[1] if len(args) > 1 else "."
        items = HostBridge.list_path(target)
        if items is None: 
            print("❌ Path not found.")
            return
        print(f"📂 Listing: {os.path.abspath(target)}")
        print(f"{'TYPE':<6} {'SIZE':<10} {'NAME'}")
        print("-" * 50)
        for i in items:
            size = f"{i['size']/1024:.1f} KB" if i['type'] == "FILE" else "-"
            print(f"{i['type']:<6} {size:<10} {i['name']}")

    elif cmd == "nuke":
        if len(args) < 2: return
        target = args[1]
        if input(f"⚠️ NUKE {target}? (y/n): ") == "y":
            if HostBridge.nuke_path(target): print("💥 Nuked.")
            else: print("❌ Nuke failed.")

    elif cmd == "ps":
        procs = HostBridge.get_processes()
        print(f"⚙️ Running Processes ({len(procs)}):")
        for p in procs[:15]: print(p)

    # --- UPDATED INFO COMMAND ---
    elif cmd == "info":
        print("\n⏳ Scanning hardware & cloud services...")
        data = HostBridge.get_deep_info()
        
        print("\n" + "="*60)
        print(f"   SYSTEM AUDIT REPORT | {data.get('OS', 'Unknown')}")
        print("="*60)

        print(f"\n🧠 HARDWARE")
        print(f"   CPU:   {data.get('CPU', 'Unknown')}")
        print(f"   RAM:   {data.get('RAM_Total', '?')} GB")
        print(f"   GPU:   {data.get('GPU_Name', 'Unknown')}")

        print(f"\n☁️ CLOUD STORAGE")
        clouds = data.get('Cloud', [])
        if not clouds:
            print("   (No Cloud Services Detected)")
        else:
            for c in clouds:
                print(f"   • {c['name']}: {c['path']}")

        print(f"\n💽 DRIVES")
        for d in data.get('Disks', []):
            try: 
                # Handle simplified linux disk dict or complex windows dict
                name = d.get('FriendlyName', 'Drive')
                size = d.get('Size', '?')
                # Rough conversion if it looks like bytes
                if str(size).isdigit() and int(size) > 1000: 
                    size = f"{int(size)//(1024**3)} GB"
                print(f"   • {name} [{size}]")
            except: pass

        print(f"\n📡 NETWORK")
        for n in data.get('Network', []):
            print(f"   • {n.get('Name', 'Net')}: {n.get('MacAddress', '')}")

        print("\n" + "="*60 + "\n")

    elif cmd == "open" or cmd == "launch":
        if len(args) > 1: HostBridge.launch(args[1])
        
    else:
        print("Unknown host command.")