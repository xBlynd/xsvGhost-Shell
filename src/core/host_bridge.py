import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

class HostBridge:
    @staticmethod
    def get_os_type():
        """Returns 'windows', 'linux', or 'macos'."""
        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        return system

    @staticmethod
    def clear_screen():
        """Clears terminal window based on OS."""
        command = "cls" if os.name == "nt" else "clear"
        os.system(command)

    @staticmethod
    def is_wsl():
        """Detects if we are running inside WSL (Windows Subsystem for Linux)."""
        if platform.system().lower() != "linux":
            return False
        try:
            with open("/proc/version", "r") as f:
                return "microsoft" in f.read().lower()
        except:
            return False

    @staticmethod
    def launch(path):
        """
        Universal 'Open File' command.
        - Windows: Uses os.startfile
        - Linux: Uses xdg-open
        - WSL: Tries to use explorer.exe if accessible, else xdg-open
        """
        p = Path(path)
        if not p.exists():
            print(f"❌ Error: Path not found: {path}")
            return False

        system = HostBridge.get_os_type()

        try:
            if system == "windows":
                os.startfile(p)
            elif system == "linux":
                # Special handling for WSL to open files in Windows side
                if HostBridge.is_wsl():
                    subprocess.run(["explorer.exe", str(p)])
                else:
                    subprocess.run(["xdg-open", str(p)])
            elif system == "macos":
                subprocess.run(["open", str(p)])
            print(f"🚀 Launched: {p.name}")
            return True
        except Exception as e:
            print(f"❌ Launch Failed: {e}")
            return False

    @staticmethod
    def get_system_info():
        """Returns a dict of system stats for the console."""
        return {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "is_wsl": HostBridge.is_wsl(),
            "python_version": sys.version.split()[0],
            "user": os.getlogin()
        }