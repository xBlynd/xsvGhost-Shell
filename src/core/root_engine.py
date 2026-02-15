"""
Root Engine - God Mode
Silent system command execution
"""

import subprocess
import platform

class RootEngine:
    """
    System-level command execution.
    Silent by default (no popup windows on Windows).
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "root"
        self.os_type = platform.system()
    
    def execute_silent(self, cmd, shell=True):
        """
        Execute command silently.
        THE CRITICAL PATTERN for stealth on Windows.
        """
        startupinfo = None
        
        if self.os_type == "Windows":
            # Prevent CMD window popup
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        try:
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                startupinfo=startupinfo,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute(self, cmd):
        """Execute command with output"""
        return self.execute_silent(cmd)
