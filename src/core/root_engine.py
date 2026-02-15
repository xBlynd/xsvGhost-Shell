"""
Engine 05: Root Engine - God Mode
===================================
Silent subprocess execution, system commands, hardware control.

The key innovation: Silent execution on Windows (no popup CMD windows).

Compartmentalization:
- MUST check SecurityEngine permissions before dangerous commands
- Returns raw output, doesn't interpret it
"""

import subprocess
import platform
import os


class RootEngine:
    """God Mode - hardware control and system execution."""

    ENGINE_NAME = "root"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.os_type = platform.system().upper()

    def exec_silent(self, cmd, shell=True, timeout=30):
        """
        Execute a command silently (no popup window on Windows).
        Returns (stdout, stderr) as strings.
        """
        kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "shell": shell,
            "timeout": timeout,
        }

        # Windows: prevent CMD window popup
        if self.os_type == "WINDOWS":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            kwargs["startupinfo"] = startupinfo

        try:
            process = subprocess.Popen(cmd, **kwargs)
            stdout, stderr = process.communicate(timeout=timeout)

            stdout_str = stdout.decode("utf-8", errors="replace") if stdout else ""
            stderr_str = stderr.decode("utf-8", errors="replace") if stderr else ""

            return stdout_str, stderr_str

        except subprocess.TimeoutExpired:
            return "", f"[!] Command timed out after {timeout}s"
        except FileNotFoundError:
            return "", f"[!] Command not found: {cmd}"
        except Exception as e:
            return "", f"[!] Execution error: {e}"

    def exec_elevated(self, cmd):
        """
        Execute with elevated privileges (requires SecurityEngine GOD check).
        Caller is responsible for checking permissions first.
        """
        if self.os_type == "WINDOWS":
            # On Windows, we'd need UAC elevation
            return self.exec_silent(cmd)
        else:
            # On Linux, prefix with sudo if not already root
            if os.geteuid() != 0:
                cmd = f"sudo {cmd}"
            return self.exec_silent(cmd)

    def get_system_info(self):
        """Gather basic system information."""
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
        }

        # Disk space
        try:
            if self.os_type == "WINDOWS":
                stdout, _ = self.exec_silent("wmic logicaldisk get size,freespace,caption")
                info["disk_raw"] = stdout.strip()
            else:
                stdout, _ = self.exec_silent("df -h /")
                info["disk_raw"] = stdout.strip()
        except Exception:
            pass

        return info
