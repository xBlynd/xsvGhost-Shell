import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
PROJECT_ROOT = Path(".")
SRC = PROJECT_ROOT / "src"
CORE = SRC / "core"
CMDS = SRC / "commands"

# --- THE FINAL CODE (Universal Host + Alias Fix) ---
HOST_CODE = r"""
import os, sys, platform, subprocess, shutil, socket, json
from pathlib import Path

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
        s = platform.system().lower()
        return "macos" if s == "darwin" else s

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
            elif s == "linux": subprocess.run(["xdg-open", str(p)])
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
    def get_deep_info():
        s = platform.system()
        info = {"OS": f"{s} {platform.release()}", "Build": platform.version(), "Disks": [], "Network": []}
        
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
                lsblk = subprocess.getoutput("lsblk -d -o NAME,SIZE,MODEL").splitlines()
                if len(lsblk) > 1:
                    for l in lsblk[1:]:
                        p = l.split()
                        if len(p) >= 2: info["Disks"].append({"FriendlyName": p[0], "Size": p[1]})
            except Exception as e: info["Error"] = str(e)
        return info
"""

ALIAS_CODE = r"""
import sys, shutil, os
from pathlib import Path

def run(args):
    if not args:
        print("Usage: xsv alias [add|list|nuke] <name>")
        return
    cmd = args[0].lower()
    root = Path(__file__).parent.parent.parent
    
    if cmd == "add":
        if len(args) < 2: return
        new_name = args[1]
        src = root / "xsv.bat"
        tgt = root / f"{new_name}.bat"
        if src.exists():
            shutil.copy(src, tgt)
            print(f"✅ Alias '{new_name}' created.")
            
    elif cmd == "list":
        print("\n🔗 Aliases:")
        for f in root.glob("*.bat"):
            if f.name not in ["setup_xsv.bat", "setup_path.bat", "xsv.bat"]: print(f"  🔹 {f.stem}")
            
    elif cmd == "nuke":
        if len(args) < 2: return
        tgt = root / f"{args[1]}.bat"
        if tgt.exists(): 
            os.remove(tgt)
            print(f"🗑️ Nuked {args[1]}")
    else:
        print("Unknown alias command.")
"""

def clean_house():
    print("🧹 Starting Deep Clean...")
    
    # 1. DELETE TEMP SCRIPTS
    junk = [
        "upgrade_alias.py", "upgrade_host_deep.py", "upgrade_universal.py", 
        "upgrade_universal_v2.py", "fix_launcher.py", "refactor_v2.py",
        "refactor_final.py", "build_specs.py", "setup_xsv.bat"
    ]
    for f in junk:
        p = PROJECT_ROOT / f
        if p.exists():
            os.remove(p)
            print(f"🔥 Deleted junk: {f}")

    # 2. APPLY FINAL CODE
    print("🛠️  Applying Final Core Updates...")
    with open(CORE / "host_bridge.py", "w", encoding="utf-8") as f:
        f.write(HOST_CODE.strip())
    
    with open(CMDS / "cmd_alias.py", "w", encoding="utf-8") as f:
        f.write(ALIAS_CODE.strip())

    print("\n✅ CLEANUP COMPLETE. Your folder is tidy.")
    print("   You should now only see: xsv.bat, setup_path.ps1, src/, data/, library/")

if __name__ == "__main__":
    clean_house()