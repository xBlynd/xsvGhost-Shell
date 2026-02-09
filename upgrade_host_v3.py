import os
from pathlib import Path

# --- CONFIGURATION ---
PROJECT_ROOT = Path(".")
CORE = PROJECT_ROOT / "src" / "core"
CMDS = PROJECT_ROOT / "src" / "commands"

def write_file(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Upgraded: {path}")

# --- 1. HOST BRIDGE v3 (Cloud & ChromeOS Support) ---
HOST_BRIDGE_CODE = r"""
import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path

# PowerShell extraction script (Windows only)
PS_PAYLOAD = r'''
$ErrorActionPreference = "SilentlyContinue"
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$gpu = Get-CimInstance Win32_VideoController | Select-Object -First 1
$ram_sticks = Get-CimInstance Win32_PhysicalMemory
$ram_total = ($ram_sticks | Measure-Object -Property Capacity -Sum).Sum / 1GB
$disk = Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size
$net = Get-NetAdapter | Where-Object Status -eq 'Up'

$info = @{
    CPU = $cpu.Name
    Cores = $cpu.NumberOfCores
    GPU_Name = $gpu.Name
    RAM_Total = [math]::Round($ram_total, 1)
    Disks = @($disk)
    Network = @($net | Select-Object Name, MacAddress)
}
$info | ConvertTo-Json -Depth 3 -Compress
'''

class HostBridge:
    @staticmethod
    def get_os_type():
        """Returns: windows, macos, chromeos, or linux"""
        s = platform.system().lower()
        if s == "darwin": return "macos"
        if s == "windows": return "windows"
        
        # Check for ChromeOS / Crostini
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                data = f.read().lower()
                if "chromeos" in data or "cros" in data:
                    return "chromeos"
        return "linux"

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def launch(path):
        p = Path(path)
        if not p.exists(): return False
        s = HostBridge.get_os_type()
        try:
            if s == "windows": os.startfile(p)
            elif s == "linux" or s == "chromeos": subprocess.run(["xdg-open", str(p)])
            else: subprocess.run(["open", str(p)])
            return True
        except: return False

    @staticmethod
    def list_path(target="."):
        p = Path(target)
        if not p.exists(): return None
        items = []
        try:
            for i in p.iterdir():
                items.append({
                    "name": i.name, 
                    "type": "DIR" if i.is_dir() else "FILE",
                    "size": i.stat().st_size if i.is_file() else 0
                })
            return sorted(items, key=lambda x: (x["type"]=="FILE", x["name"]))
        except: return []

    @staticmethod
    def nuke_path(target):
        p = Path(target)
        if not p.exists(): return False
        try:
            if p.is_dir(): shutil.rmtree(p)
            else: os.remove(p)
            return True
        except: return False

    @staticmethod
    def get_processes():
        cmd = ["tasklist"] if os.name == "nt" else ["ps", "-e"]
        try: return subprocess.check_output(cmd, encoding="utf-8", errors="ignore").splitlines()
        except: return []

    @staticmethod
    def get_cloud_storage():
        """Detects OneDrive, Google Drive, Dropbox locations"""
        home = Path.home()
        clouds = []
        
        # Windows Paths
        if os.name == "nt":
            onedrive = os.environ.get("OneDrive")
            if onedrive and Path(onedrive).exists():
                clouds.append({"name": "OneDrive", "path": onedrive})
            
            gdrive = home / "Google Drive"
            if gdrive.exists(): clouds.append({"name": "Google Drive", "path": str(gdrive)})
            
            gdrive_fs = Path("G:/") # Common Google Drive Desktop mount
            if gdrive_fs.exists(): clouds.append({"name": "Google Drive (Virtual)", "path": "G:/"})

        # Linux/ChromeOS Paths
        else:
            # Common Linux Mounts
            candidates = [home / "OneDrive", home / "Google Drive", home / "Dropbox"]
            for c in candidates:
                if c.exists(): clouds.append({"name": c.name, "path": str(c)})
                
            # ChromeOS specific mounts often appear in /mnt/chromeos
            if os.path.exists("/mnt/chromeos/GoogleDrive"):
                clouds.append({"name": "ChromeOS GDrive", "path": "/mnt/chromeos/GoogleDrive"})

        return clouds

    @staticmethod
    def get_deep_info():
        s = platform.system()
        os_type = HostBridge.get_os_type()
        
        info = {
            "OS": f"{s} {platform.release()} ({os_type.upper()})",
            "Build": platform.version(),
            "Disks": [],
            "Network": [],
            "Cloud": HostBridge.get_cloud_storage()
        }
        
        if s == "Windows":
            try:
                res = subprocess.check_output(["powershell", "-NoProfile", "-Command", PS_PAYLOAD], encoding="utf-8", errors="ignore")
                info.update(json.loads(res))
            except Exception as e: info["Error"] = str(e)
            
        elif s == "Linux":
            try:
                if os.path.exists("/proc/cpuinfo"):
                    with open("/proc/cpuinfo") as f:
                        for l in f: 
                            if "model name" in l: info["CPU"] = l.split(":")[1].strip(); break
                
                # RAM
                mem = subprocess.getoutput("free -g").split()
                if "Mem:" in mem: info["RAM_Total"] = f"{mem[1]} GB"

                lsblk = subprocess.getoutput("lsblk -d -o NAME,SIZE,MODEL").splitlines()
                if len(lsblk) > 1:
                    for l in lsblk[1:]:
                        p = l.split()
                        if len(p) >= 2: info["Disks"].append({"FriendlyName": p[0], "Size": p[1]})
            except Exception as e: info["Error"] = str(e)
            
        return info
"""

# --- 2. UPDATE HOST COMMAND TO SHOW CLOUD INFO ---
CMD_HOST_CODE = r"""
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
"""

if __name__ == "__main__":
    print("☁️  Installing Cloud & ChromeOS Support...")
    write_file(CORE / "host_bridge.py", HOST_BRIDGE_CODE)
    write_file(CMDS / "cmd_host.py", CMD_HOST_CODE)
    print("\n✅ System v3.0 Ready.")
    print("TRY THIS: .\\magic.bat host info")