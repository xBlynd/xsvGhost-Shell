import sys
import os
from src.core.host_engine import HostEngine

def run(args):
    if not args:
        print("Usage: xsv host <sub-command>")
        print("  ls <path>    - List Files")
        print("  nuke <path>  - Force Delete")
        print("  ps           - Process List")
        print("  info         - Deep Scan")
        print("  cmd <cmd>    - Run System Command (e.g., 'ipconfig')")
        return

    sub_cmd = args[0].lower()
    
    # 1. INFO COMMAND (The Deep Scan)
    if sub_cmd == "info":
        print("\n🔎 Running Deep Hardware Scan (CPU-Z Style)...")
        report = HostEngine.get_info()
        data = report.get("Data", {})
        
        print("\n" + "="*60)
        print(f"   SYSTEM REPORT: {data.get('System', {}).get('Model', 'Unknown PC')}")
        print("="*60)

        # BIOS & MOBO
        print(f"\n📟 MOTHERBOARD")
        mobo = data.get("Mobo", {})
        bios = data.get("BIOS", {})
        print(f"   Board: {mobo.get('Make')} {mobo.get('Model')}")
        print(f"   BIOS:  {bios.get('Version')} (Date: {bios.get('Date')})")
        print(f"   S/N:   {bios.get('Serial')}")

        # CPU
        cpu = data.get("CPU", {})
        print(f"\n🧠 PROCESSOR")
        print(f"   Name:   {cpu.get('Name')}")
        print(f"   Socket: {cpu.get('Socket')}")
        print(f"   Specs:  {cpu.get('Cores')} Cores / {cpu.get('Threads')} Threads")

        # RAM
        print(f"\n💾 MEMORY")
        sticks = data.get("RAM_Sticks", [])
        if isinstance(sticks, dict): sticks = [sticks]
        for s in sticks:
            cap = int(s.get('Capacity', 0)) // (1024**3)
            print(f"   • {s.get('Manufacturer')} {cap}GB @ {s.get('Speed')}MHz ({s.get('PartNumber')})")

        # GPU
        print(f"\n🎮 GRAPHICS")
        gpus = data.get("GPUs", [])
        if isinstance(gpus, dict): gpus = [gpus]
        for g in gpus:
            vram = "Unknown"
            if g.get('AdapterRAM'):
                vram = f"{int(g['AdapterRAM']) // (1024**3)} GB"
            print(f"   • {g.get('Name')} [{vram}]")
            print(f"     Driver: {g.get('DriverVersion')}")

        # STORAGE
        print(f"\n💽 DRIVES")
        disks = data.get("Disks", [])
        if isinstance(disks, dict): disks = [disks]
        for d in disks:
            size_gb = int(d.get('Size', 0)) // (1024**3)
            print(f"   • {d.get('Model')} ({d.get('MediaType')}) - {size_gb} GB")

        # CLOUD
        print(f"\n☁️ CLOUD")
        for c in report.get("Cloud", []):
            print(f"   • {c['name']}: {c['path']}")

        # COOLING
        print(f"\n❄️ ENTHUSIAST USB")
        usb = data.get("Cooling", [])
        if usb:
            if isinstance(usb, dict): usb = [usb]
            for u in usb: print(f"   • {u.get('FriendlyName')}")
        else:
            print("   (No smart devices found)")

        print("\n" + "="*60 + "\n")

    # 2. FILE COMMANDS
    elif sub_cmd == "ls":
        target = args[1] if len(args) > 1 else "."
        items = HostEngine.list_dir(target)
        if items:
            print(f"📂 Listing: {os.path.abspath(target)}")
            print("-" * 40)
            for i in items: 
                icon = "📁" if i['type'] == "DIR" else "📄"
                print(f"{icon} {i['name']}")
            
    elif sub_cmd == "nuke":
        if len(args) > 1: HostEngine.nuke(args[1])

    # 3. SYSTEM COMMANDS
    elif sub_cmd == "ps":
        print("Running Processes:")
        for p in HostEngine.get_procs()[:10]: print(p)

    elif sub_cmd == "cmd" or sub_cmd == "exec":
        full_cmd = " ".join(args[1:])
        HostEngine.run_sys_command(full_cmd)
        
    elif sub_cmd == "open" or sub_cmd == "launch":
        if len(args) > 1: HostEngine.launch(args[1])

    else:
        print(f"❌ Unknown host command: {sub_cmd}")