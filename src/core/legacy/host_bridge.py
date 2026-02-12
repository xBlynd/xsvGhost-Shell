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
        if os.path.exists("/etc/os-release"):
            try:
                with open("/etc/os-release") as f:
                    data = f.read().lower()
                    if "chromeos" in data or "cros" in data: return "chromeos"
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
    def get_deep_info():
        s = platform.system()
        info = {
            "OS": f"{s} {platform.release()}",
            "Build": platform.version(),
            "Disks": [],
            "GPUs": [],
            "Network": [],
            "Cloud": [],
            "USB_Devices": []
        }
        
        if s == "Windows":
            # Advanced PowerShell Script for Enthusiast Hardware
            ps_script = r"""
            $ErrorActionPreference = "SilentlyContinue"
            
            # 1. CPU & Motherboard
            $cpu = Get-CimInstance Win32_Processor
            $mobo = Get-CimInstance Win32_BaseBoard
            
            # 2. RAM Details
            $ram_sticks = Get-CimInstance Win32_PhysicalMemory
            $ram_total = ($ram_sticks | Measure-Object -Property Capacity -Sum).Sum / 1GB
            
            # 3. ALL GPUs (Not just the first one)
            $gpus = Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion
            
            # 4. Storage & Drives
            $disks = Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size, BusType
            $logic = Get-PSDrive -PSProvider FileSystem | Select-Object Name, Root, Description
            
            # 5. Network
            $net = Get-NetAdapter | Where-Object Status -eq 'Up'
            
            # 6. USB/Cooling Scan (Looking for specific enthusiast keywords)
            $usb = Get-PnpDevice -Class 'USB', 'HIDClass' -Status 'OK' | Where-Object { $_.FriendlyName -match 'Corsair|NZXT|Liquid|Pump|AIO|Cooler|Hub|Commander' } | Select-Object FriendlyName

            $info = @{
                CPU = $cpu.Name
                Cores = $cpu.NumberOfCores
                Mobo = "$($mobo.Manufacturer) $($mobo.Product)"
                RAM_Total = [math]::Round($ram_total, 1)
                GPUs = @($gpus)
                Disks = @($disks)
                Drives = @($logic)
                Network = @($net | Select-Object Name, MacAddress)
                USB_Devices = @($usb)
            }
            $info | ConvertTo-Json -Depth 3 -Compress
            """
            try:
                res = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_script], encoding="utf-8", errors="ignore")
                data = json.loads(res)
                info.update(data)
                
                # --- CLOUD DETECTION LOGIC ---
                # Check 1: User Folder
                home = Path.home()
                if (home / "OneDrive").exists(): 
                    info["Cloud"].append({"name": "OneDrive", "path": str(home / "OneDrive")})
                
                # Check 2: Virtual Drives (G: is standard for Google Drive)
                for d in data.get("Drives", []):
                    root = d.get("Root", "").upper()
                    if root == "G:\\":
                        info["Cloud"].append({"name": "Google Drive (Virtual)", "path": "G:\\"})
                    elif "Google" in d.get("Description", ""):
                        info["Cloud"].append({"name": "Google Drive", "path": root})

            except Exception as e: info["Error"] = str(e)
            
        return info