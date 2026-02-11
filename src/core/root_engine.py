"""
RootEngine - The Mechanic (Engine #5)
God Mode control over the host system.

Responsibilities:
- Process management (kill, list)
- File operations (delete, launch, list)
- System commands (raw shell execution)
- Hardware ID operations (future)
- Registry hacks (future)
"""
import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path

class RootEngine:
    """
    The Mechanic - Engine #5
    Provides God Mode control over the host machine.
    """
    
    # ============================================================
    # DISPLAY & UI OPERATIONS
    # ============================================================
    @staticmethod
    def clear_screen():
        """Clear the terminal screen (cross-platform)"""
        os.system("cls" if os.name == "nt" else "clear")
    
    # ============================================================
    # FILE & LAUNCH OPERATIONS
    # ============================================================
    @staticmethod
    def launch(path):
        """Universal Open/Launch for files and directories"""
        p = Path(path)
        if not p.exists(): 
            return False
        
        s = platform.system().lower()
        try:
            if s == "windows":
                os.startfile(p)
            elif s == "darwin":
                subprocess.run(["open", str(p)])
            else:  # Linux/ChromeOS
                subprocess.run(["xdg-open", str(p)])
            return True
        except:
            return False
    
    @staticmethod
    def list_dir(target="."):
        """List directory contents with metadata"""
        p = Path(target)
        if not p.exists(): 
            return None
        
        items = []
        try:
            for i in p.iterdir():
                items.append({
                    "name": i.name, 
                    "type": "DIR" if i.is_dir() else "FILE",
                    "size": i.stat().st_size if i.is_file() else 0
                })
            return sorted(items, key=lambda x: (x["type"]=="FILE", x["name"]))
        except:
            return []
    
    @staticmethod
    def nuke(target):
        """
        Delete file or directory (DESTRUCTIVE - use with caution)
        Future: Add to trash instead of permanent delete
        """
        p = Path(target)
        if not p.exists(): 
            return False
        
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                os.remove(p)
            return True
        except:
            return False
    
    # ============================================================
    # PROCESS MANAGEMENT
    # ============================================================
    @staticmethod
    def get_procs():
        """Get list of running processes (cross-platform)"""
        cmd = ["tasklist"] if os.name == "nt" else ["ps", "-e"]
        try:
            return subprocess.check_output(cmd, encoding="utf-8", errors="ignore").splitlines()
        except:
            return []
    
    # ============================================================
    # SYSTEM COMMAND EXECUTION
    # ============================================================
    @staticmethod
    def run_sys_command(command):
        """
        Execute raw system command (ping, ipconfig, etc.)
        WARNING: Shell=True can be dangerous with untrusted input
        """
        try:
            subprocess.run(command, shell=True)
            return True
        except Exception as e:
            print(f"❌ Execution Error: {e}")
            return False
    
    # ============================================================
    # DEEP SYSTEM INFORMATION (Harvested from host_bridge.py)
    # ============================================================
    @staticmethod
    def get_deep_info():
        """
        Advanced hardware detection for enthusiast systems.
        Detects:
        - CPU, RAM, Motherboard
        - Multiple GPUs (Gaming/Workstation rigs)
        - NVMe/SSD/HDD storage
        - Cloud drive mounts (OneDrive, Google Drive)
        - Enthusiast USB devices (Corsair, NZXT cooling)
        """
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
                res = subprocess.check_output(
                    ["powershell", "-NoProfile", "-Command", ps_script], 
                    encoding="utf-8", 
                    errors="ignore"
                )
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
                    if root == "G:\\\\":
                        info["Cloud"].append({"name": "Google Drive (Virtual)", "path": "G:\\\\"})
                    elif "Google" in d.get("Description", ""):
                        info["Cloud"].append({"name": "Google Drive", "path": root})

            except Exception as e:
                info["Error"] = str(e)
        
        # Linux/MacOS deep info can be added here in future
        return info
    
    # ============================================================
    # FUTURE: GOD MODE OPERATIONS
    # ============================================================
    # - Registry hacking (Windows)
    # - Process force kill (suspend thread first)
    # - Hardware ID spoofing
    # - Trace wiping (Event Logs, Prefetch, etc.)
