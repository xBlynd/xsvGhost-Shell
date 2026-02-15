"""
Sync Engine - The Bridge
USB detection and file synchronization
"""

import os
import platform
from pathlib import Path

class SyncEngine:
    """
    Synchronization engine.
    Detects USB, syncs files, handles offline mode.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "sync"
        self.os_type = platform.system()
        
        core = kernel.engines.get('ghost_core')
        if core:
            self.root_dir = core.ROOT_DIR
        else:
            self.root_dir = Path(__file__).parent.parent.parent
    
    def is_running_from_usb(self):
        """
        Detect if running from removable media.
        The Anchor test - are we portable?
        """
        if self.os_type == "Windows":
            try:
                import ctypes
                drive = os.path.splitdrive(str(self.root_dir))[0]
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive + "\\")
                # 2 = DRIVE_REMOVABLE
                return drive_type == 2
            except:
                return False
        else:
            # Linux/Mac detection (basic)
            root_str = str(self.root_dir)
            return '/media/' in root_str or '/mnt/' in root_str
    
    def get_sync_status(self):
        """Get sync status"""
        return {
            "on_usb": self.is_running_from_usb(),
            "root": str(self.root_dir),
            "status": "USB" if self.is_running_from_usb() else "Local"
        }
