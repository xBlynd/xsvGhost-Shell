import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path

class HostBridge:
    @staticmethod
    def get_os_type():
        """Returns: windows, macos, chromeos, or linux"""
        s = platform.system().lower()
        if s == "darwin": return "macos"
        if s == "windows": return "windows"
        
        # Check for ChromeOS / Crostini
        if os.path.exists("/etc/os-release"):
            try:
                with open("/etc/os-release") as f:
                    data = f.read().lower()
                    if "chromeos" in data or "cros" in data:
                        return "chromeos"
            except: pass
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
            candidates = [home / "OneDrive", home / "Google Drive", home / "Dropbox"]
            for c in candidates:
                if c.exists(): clouds.append({"name": c.name, "path": str(c)})
                
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
            ps_script = r"""
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
            """
            try:
                res = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_script], encoding="utf-8", errors="ignore")
                info.update(json.loads(res))
            except Exception as e: info["Error"] = str(e)
            
        elif s == "Linux":
            try:
                if os.path.exists("/proc/cpuinfo"):
                    with open("/proc/cpuinfo") as f:
                        for l in f: 
                            if "model name" in l: info["CPU"] = l.split(":")[1].strip(); break
                
                mem = subprocess.getoutput("free -g").split()
                if "Mem:" in mem: info["RAM_Total"] = f"{mem[1]} GB"

                lsblk = subprocess.getoutput("lsblk -d -o NAME,SIZE,MODEL").splitlines()
                if len(lsblk) > 1:
                    for l in lsblk[1:]:
                        p = l.split()
                        if len(p) >= 2: info["Disks"].append({"FriendlyName": p[0], "Size": p[1]})
            except Exception as e: info["Error"] = str(e)
            
        return info