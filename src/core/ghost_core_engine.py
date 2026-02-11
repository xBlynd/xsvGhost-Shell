"""
GhostCoreEngine - The Kernel
OS detection, environment setup, config loading.
"""
import platform
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

class GhostCoreEngine:
    """The Brain - Environment detector and configurator"""
    
    def __init__(self):
        self.os_type = None
        self.os_version = None
        self.is_linux = False
        self.is_windows = False
        self.is_mac = False
        self.config = {}
    
    def initialize(self):
        """Detect OS and load configuration"""
        self.detect_os()
        self.load_config()
        print(f"GhostCoreEngine: {self.os_type} {self.os_version}")
    
    def detect_os(self):
        """Identify the host operating system"""
        self.os_type = platform.system()
        self.os_version = platform.release()
        
        self.is_linux = self.os_type == "Linux"
        self.is_windows = self.os_type == "Windows"
        self.is_mac = self.os_type == "Darwin"
        
        # Set IS_LINUX flag for other engines
        import os
        os.environ['GHOST_OS'] = self.os_type
    
    def load_config(self):
        """Load settings.json"""
        config_file = ROOT / 'data' / 'config' / 'settings.json'
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Create default config
            self.config = {
                'theme': 'blue',
                'auto_lock': True,
                'idle_timeout': 300,
                'heartbeat_interval': 5
            }
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
    
    def get_config(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set_config(self, key, value):
        """Update configuration"""
        self.config[key] = value
        config_file = ROOT / 'data' / 'config' / 'settings.json'
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def shutdown(self):
        """Cleanup"""
        pass
