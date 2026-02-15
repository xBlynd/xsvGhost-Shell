"""
Heartbeat Engine - The Immune System
System health monitoring
"""

import threading
import psutil
from datetime import datetime

class HeartbeatEngine:
    """Monitors system health and resource usage"""
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "heartbeat"
        self.process = psutil.Process()
    
    def get_health(self):
        """Get current system health snapshot"""
        return {
            "memory_mb": self.process.memory_info().rss / 1024 / 1024,
            "threads": threading.active_count(),
            "engines_loaded": len([e for e in self.kernel.engines.values() if e]),
            "commands_loaded": len(self.kernel.commands),
            "uptime": self._get_uptime(),
            "status": "HEALTHY"
        }
    
    def _get_uptime(self):
        """Get session uptime"""
        core = self.kernel.engines.get('ghost_core')
        if not core or not core.session.get('last_boot'):
            return "Unknown"
        
        boot_time = datetime.fromisoformat(core.session['last_boot'])
        uptime = datetime.now() - boot_time
        
        minutes = int(uptime.total_seconds() / 60)
        seconds = int(uptime.total_seconds() % 60)
        
        return f"{minutes}m {seconds}s"
