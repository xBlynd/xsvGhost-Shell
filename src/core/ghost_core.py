"""
Ghost Core Engine - The Brain
Handles OS detection, path management, session state
"""

import os
import platform
import json
from pathlib import Path

class GhostCoreEngine:
    """
    The foundational engine. Detects environment and manages paths.
    THE ANCHOR - Makes the entire system portable.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "ghost_core"
        
        # THE ANCHOR - No absolute paths, ever
        self.ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
        
        # Detect OS
        self.os_type = platform.system()  # Windows, Linux, Darwin
        self.os_name = self._get_os_name()
        
        # Node identity
        self.node_type = "MASTER"  # MASTER, LEGION, or GUEST
        self.node_id = self._load_or_generate_node_id()
        
        # Session state
        self.session_file = self.ROOT_DIR / "data" / "session" / "current.json"
        self.session = self._load_session()
        
    def _get_os_name(self):
        """Get friendly OS name"""
        os_map = {
            "Windows": "Windows",
            "Linux": "Linux",
            "Darwin": "macOS"
        }
        return os_map.get(self.os_type, self.os_type)
    
    def _load_or_generate_node_id(self):
        """Load or create unique node ID"""
        id_file = self.ROOT_DIR / "data" / "session" / "node_id.txt"
        
        if id_file.exists():
            return id_file.read_text().strip()
        else:
            # Generate ID from hostname + timestamp
            import socket
            from datetime import datetime
            node_id = f"{socket.gethostname()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            id_file.parent.mkdir(parents=True, exist_ok=True)
            id_file.write_text(node_id)
            return node_id
    
    def _load_session(self):
        """Load current session state"""
        if self.session_file.exists():
            try:
                return json.loads(self.session_file.read_text())
            except:
                pass
        
        # Default session
        return {
            "last_boot": None,
            "boot_count": 0,
            "user_role": None
        }
    
    def save_session(self):
        """Save session state"""
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.session_file.write_text(json.dumps(self.session, indent=2))
    
    def post_boot(self):
        """Called after all engines loaded"""
        from datetime import datetime
        self.session["last_boot"] = datetime.now().isoformat()
        self.session["boot_count"] = self.session.get("boot_count", 0) + 1
        self.save_session()
    
    def get_path(self, *parts):
        """Get absolute path relative to ROOT_DIR"""
        return self.ROOT_DIR / Path(*parts)
