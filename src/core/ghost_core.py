"""
GhostCoreEngine - The Kernel Brain (Engine #1)
The first engine to boot. Detects OS, loads config, and sets up the environment.
"""
import os
import sys
import platform
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

class GhostCoreEngine:
    """
    The Brain - Engine #1
    Responsibilities:
    - OS Detection (Windows/Linux/MacOS/ChromeOS)
    - Config Loading (settings.json)
    - Dependency Checks (Python version, Node, libnotify)
    """
    
    def __init__(self):
        self.os_type = None
        self.config = {}
        self.dependencies = {}
        
    def initialize(self):
        """Boot sequence for GhostCore"""
        self.detect_os()
        self.load_config()
        self.check_dependencies()
        return True
    
    def detect_os(self):
        """
        Returns: 'windows', 'macos', 'linux', or 'chromeos'
        Harvested from host_bridge.py and enhanced
        """
        s = platform.system().lower()
        
        if s == "darwin":
            self.os_type = "macos"
        elif s == "windows":
            self.os_type = "windows"
        elif os.path.exists("/etc/os-release"):
            try:
                with open("/etc/os-release") as f:
                    data = f.read().lower()
                    if "chromeos" in data or "cros" in data:
                        self.os_type = "chromeos"
                    else:
                        self.os_type = "linux"
            except:
                self.os_type = "linux"
        else:
            self.os_type = "linux"  # Default fallback
        
        return self.os_type
    
    def load_config(self):
        """Load settings.json from data/config/"""
        config_file = ROOT / 'data' / 'config' / 'settings.json'
        
        if not config_file.exists():
            # Create default config if missing (self-healing)
            default_config = {
                "theme": "dark",
                "user": "ghost",
                "auto_save": True,
                "heartbeat_interval": 3
            }
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            self.config = default_config
        else:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        
        return self.config
    
    def check_dependencies(self):
        """
        Verify critical dependencies:
        - Python version
        - libnotify (Linux only)
        - Node.js (optional)
        """
        import shutil
        
        # Python version
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.dependencies['python'] = {
            'installed': True,
            'version': py_version,
            'meets_requirement': sys.version_info >= (3, 8)
        }
        
        # libnotify (Linux only)
        if self.os_type in ['linux', 'chromeos']:
            notify_send = shutil.which('notify-send')
            self.dependencies['libnotify'] = {
                'installed': notify_send is not None,
                'path': notify_send if notify_send else None
            }
        
        # Node.js (optional)
        node = shutil.which('node')
        self.dependencies['node'] = {
            'installed': node is not None,
            'path': node if node else None
        }
        
        return self.dependencies
    
    def get_os(self):
        """Public getter for OS type"""
        return self.os_type
    
    def get_config(self, key=None):
        """Get config value(s)"""
        if key:
            return self.config.get(key)
        return self.config
    
    def is_linux(self):
        """Convenience check"""
        return self.os_type in ['linux', 'chromeos']
    
    def is_windows(self):
        """Convenience check"""
        return self.os_type == 'windows'
    
    def shutdown(self):
        """Cleanup on exit"""
        pass
