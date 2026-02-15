"""
Ghost Engine - The Shadow
Stealth operations and cleanup
"""

import os
import shutil
from pathlib import Path

class GhostEngine:
    """
    Stealth and anti-forensics.
    Cleans up temp files, minimal footprint.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "ghost"
        
        core = kernel.engines.get('ghost_core')
        if core:
            self.root_dir = core.ROOT_DIR
        else:
            self.root_dir = Path(__file__).parent.parent.parent
    
    def cleanup(self):
        """Clean up temp files on shutdown"""
        print("[Ghost] Cleaning traces...")
        
        # Remove __pycache__ directories
        for root, dirs, files in os.walk(self.root_dir):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                try:
                    shutil.rmtree(pycache_path)
                except:
                    pass
        
        # Remove .pyc files
        for pyc in self.root_dir.rglob("*.pyc"):
            try:
                pyc.unlink()
            except:
                pass
        
        print("[Ghost] Cleanup complete")
