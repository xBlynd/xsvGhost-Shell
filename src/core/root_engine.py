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
import socket


class RootEngine:
    """God Mode - hardware control and system execution."""

    ENGINE_NAME = "root"
    ENGINE_VERSION = "2.0.0"

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
            return self.exec_silent(cmd)
        else:
            if os.geteuid() != 0:
                cmd = f"sudo {cmd}"
            return self.exec_silent(cmd)

    # =========================================================================
    # SYSTEM INFO
    # =========================================================================

    def get_system_info(self):
        """Gather basic system information including disk and RAM."""
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
                import ctypes
                drives = []
                bitmask = ctypes.windll.kernel32.GetLogicalDrives()
                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    if bitmask & 1:
                        drive = f"{letter}:\\"
                        try:
                            free_bytes = ctypes.c_ulonglong(0)
                            total_bytes = ctypes.c_ulonglong(0)
                            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                                drive, None, ctypes.byref(total_bytes), ctypes.byref(free_bytes)
                            )
                            total_gb = total_bytes.value / (1024 ** 3)
                            free_gb = free_bytes.value / (1024 ** 3)
                            if total_gb > 0:
                                drives.append({
                                    "drive": drive,
                                    "total_gb": round(total_gb, 1),
                                    "free_gb": round(free_gb, 1),
                                })
                        except Exception:
                            pass
                    bitmask >>= 1
                info["disks"] = drives
            else:
                # Linux/Mac: statvfs on /
                st = os.statvfs('/')
                info["disks"] = [{
                    "drive": "/",
                    "total_gb": round((st.f_blocks * st.f_frsize) / (1024 ** 3), 1),
                    "free_gb": round((st.f_bavail * st.f_frsize) / (1024 ** 3), 1),
                }]
        except Exception:
            info["disks"] = []

        # RAM
        info["ram"] = self._get_ram()

        return info

    def _get_ram(self):
        """Get RAM info via psutil (if available) or OS fallback."""
        try:
            import psutil
            vm = psutil.virtual_memory()
            return {
                "total_gb": round(vm.total / (1024 ** 3), 1),
                "available_gb": round(vm.available / (1024 ** 3), 1),
                "used_pct": vm.percent,
                "source": "psutil",
            }
        except ImportError:
            pass

        # Windows fallback
        if self.os_type == "WINDOWS":
            try:
                stdout, _ = self.exec_silent(
                    "wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /Value"
                )
                total_kb = free_kb = 0
                for line in stdout.splitlines():
                    if "TotalVisibleMemorySize" in line:
                        total_kb = int(line.split('=')[1].strip())
                    elif "FreePhysicalMemory" in line:
                        free_kb = int(line.split('=')[1].strip())
                if total_kb:
                    return {
                        "total_gb": round(total_kb / (1024 ** 2), 1),
                        "available_gb": round(free_kb / (1024 ** 2), 1),
                        "used_pct": round((1 - free_kb / total_kb) * 100, 1),
                        "source": "wmic",
                    }
            except Exception:
                pass

        return {"total_gb": "?", "available_gb": "?", "used_pct": "?", "source": "unavailable"}

    # =========================================================================
    # NETWORK INFO
    # =========================================================================

    def get_network_info(self):
        """
        Return dict with local IPs, default gateway, DNS servers, connectivity.
        Cross-platform: ipconfig (Windows) / ip addr (Linux).
        """
        info = {
            "interfaces": [],
            "gateway": None,
            "dns_servers": [],
            "internet": False,
        }

        if self.os_type == "WINDOWS":
            self._parse_windows_network(info)
        else:
            self._parse_linux_network(info)

        # Quick connectivity check
        try:
            s = socket.create_connection(("8.8.8.8", 53), timeout=3)
            s.close()
            info["internet"] = True
        except Exception:
            info["internet"] = False

        return info

    def _parse_windows_network(self, info):
        """Parse ipconfig /all output into info dict.
        ipconfig fields use '. . . :' dot-padding notation.
        Must decode as cp1252 (Windows default) to avoid garbled output.
        """
        import subprocess as _sp
        try:
            r = _sp.run("ipconfig /all", capture_output=True, shell=True, timeout=10)
            stdout = r.stdout.decode("cp1252", errors="replace")
        except Exception:
            return

        current_iface = None
        prev_key = None

        for line in stdout.splitlines():
            # Adapter header: no leading space, ends with ':'
            if line and not line.startswith(' ') and line.rstrip().endswith(':'):
                name = line.rstrip(':').strip()
                if name and 'Windows' not in name and 'Configuration' not in name:
                    current_iface = {"name": name, "ips": []}
                    info["interfaces"].append(current_iface)
                prev_key = None
                continue

            # Field lines all have ' : ' separator (after dot-padding)
            if ' : ' not in line:
                # Continuation value (e.g. second gateway IP on its own line)
                val = line.strip()
                if val and prev_key == 'gateway' and val[0].isdigit() and info["gateway"] is None:
                    info["gateway"] = val
                continue

            key, _, val = line.partition(' : ')
            # Normalise key: strip leading spaces and dot-padding
            key_norm = key.strip().replace('. ', '').replace(' ', '').lower()
            val = val.strip()

            if 'ipv4address' in key_norm and current_iface is not None:
                ip = val.replace('(Preferred)', '').replace('(preferred)', '').strip()
                if ip and ip[0].isdigit():
                    current_iface["ips"].append(ip)
                prev_key = 'ipv4'

            elif 'defaultgateway' in key_norm:
                prev_key = 'gateway'
                if val and val[0].isdigit() and info["gateway"] is None:
                    info["gateway"] = val

            elif 'dnsservers' in key_norm:
                prev_key = 'dns'
                # Only record IPv4 DNS to keep output clean
                if val and val[0].isdigit():
                    info["dns_servers"].append(val)

            else:
                prev_key = None

    def _parse_linux_network(self, info):
        """Parse ip addr + route for Linux/Android."""
        stdout, _ = self.exec_silent("ip addr show", timeout=10)
        current_iface = None

        for line in stdout.splitlines():
            if line and not line.startswith(' '):
                parts = line.split(':')
                if len(parts) >= 2:
                    name = parts[1].strip().split('@')[0]
                    current_iface = {"name": name, "ips": []}
                    info["interfaces"].append(current_iface)
            elif current_iface and 'inet ' in line and not 'inet6' in line:
                parts = line.strip().split()
                if len(parts) >= 2:
                    ip = parts[1].split('/')[0]
                    current_iface["ips"].append(ip)

        # Gateway
        stdout, _ = self.exec_silent("ip route show default", timeout=5)
        for line in stdout.splitlines():
            parts = line.split()
            if 'via' in parts:
                idx = parts.index('via')
                if idx + 1 < len(parts):
                    info["gateway"] = parts[idx + 1]
                    break

        # DNS
        try:
            with open("/etc/resolv.conf", 'r') as f:
                for line in f:
                    if line.startswith("nameserver"):
                        parts = line.split()
                        if len(parts) >= 2:
                            info["dns_servers"].append(parts[1])
        except Exception:
            pass

    def flush_dns(self):
        """
        Flush DNS cache. Returns (success: bool, message: str).
        """
        if self.os_type == "WINDOWS":
            stdout, stderr = self.exec_silent("ipconfig /flushdns", timeout=10)
            if "Successfully flushed" in stdout or "successfully flushed" in stdout.lower():
                return True, "DNS cache flushed successfully"
            return False, stderr or "DNS flush failed (may need admin privileges)"
        else:
            # Try systemd-resolve first, then resolvectl
            for cmd in ["systemd-resolve --flush-caches", "resolvectl flush-caches"]:
                stdout, stderr = self.exec_silent(cmd, timeout=10)
                if not stderr or "error" not in stderr.lower():
                    return True, f"DNS cache flushed ({cmd.split()[0]})"
            return False, "DNS flush failed (try with sudo)"

    # =========================================================================
    # CLEANUP
    # =========================================================================

    def cleanup_temp(self, root=None):
        """
        Remove __pycache__ dirs and .pyc files under root (defaults to project root).
        Also clears data/cache/. Returns dict with counts.
        """
        import shutil

        if root is None:
            root = self.kernel.root_dir

        removed_dirs = 0
        removed_files = 0

        # Walk and remove __pycache__ and .pyc
        for dirpath, dirnames, filenames in os.walk(root):
            # Remove __pycache__ directories
            if '__pycache__' in dirnames:
                cache_path = os.path.join(dirpath, '__pycache__')
                try:
                    shutil.rmtree(cache_path)
                    removed_dirs += 1
                    dirnames.remove('__pycache__')
                except Exception:
                    pass

            # Remove loose .pyc files
            for filename in filenames:
                if filename.endswith('.pyc'):
                    try:
                        os.remove(os.path.join(dirpath, filename))
                        removed_files += 1
                    except Exception:
                        pass

        # Clear data/cache/
        cache_dir = os.path.join(self.kernel.root_dir, "data", "cache")
        cleared_cache = 0
        if os.path.exists(cache_dir):
            for item in os.listdir(cache_dir):
                item_path = os.path.join(cache_dir, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                        cleared_cache += 1
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        cleared_cache += 1
                except Exception:
                    pass

        return {
            "pycache_dirs_removed": removed_dirs,
            "pyc_files_removed": removed_files,
            "cache_items_cleared": cleared_cache,
        }

    # =========================================================================
    # PROCESSES
    # =========================================================================

    def get_processes(self, sort_by="cpu", limit=10):
        """
        Return top processes as list of dicts.
        Uses psutil if available, falls back to tasklist/ps aux.
        """
        try:
            import psutil
            procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    info = proc.info
                    mem_mb = round(info['memory_info'].rss / (1024 * 1024), 1) if info.get('memory_info') else 0
                    procs.append({
                        "pid": info['pid'],
                        "name": info['name'] or '?',
                        "cpu_pct": info.get('cpu_percent', 0) or 0,
                        "mem_mb": mem_mb,
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            if sort_by == "mem":
                procs.sort(key=lambda x: x["mem_mb"], reverse=True)
            else:
                procs.sort(key=lambda x: x["cpu_pct"], reverse=True)

            return procs[:limit]

        except ImportError:
            pass

        # Fallback: tasklist (Windows) or ps aux (Linux)
        return self._get_processes_fallback(sort_by, limit)

    def _get_processes_fallback(self, sort_by, limit):
        """Fallback process listing via system commands."""
        procs = []

        if self.os_type == "WINDOWS":
            stdout, _ = self.exec_silent(
                'tasklist /fo csv /nh', timeout=15
            )
            for line in stdout.splitlines():
                if not line.strip():
                    continue
                parts = line.strip('"').split('","')
                if len(parts) >= 5:
                    try:
                        mem_str = parts[4].replace(',', '').replace(' K', '').strip()
                        mem_mb = round(int(mem_str) / 1024, 1)
                    except (ValueError, IndexError):
                        mem_mb = 0
                    procs.append({
                        "pid": parts[1].strip(),
                        "name": parts[0].strip(),
                        "cpu_pct": 0,
                        "mem_mb": mem_mb,
                    })
        else:
            stdout, _ = self.exec_silent("ps aux --sort=-%cpu", timeout=10)
            for line in stdout.splitlines()[1:]:  # skip header
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    try:
                        procs.append({
                            "pid": parts[1],
                            "name": parts[10].split('/')[-1][:30],
                            "cpu_pct": float(parts[2]),
                            "mem_mb": float(parts[5]) / 1024,
                        })
                    except (ValueError, IndexError):
                        pass

        if sort_by == "mem":
            procs.sort(key=lambda x: x["mem_mb"], reverse=True)
        else:
            procs.sort(key=lambda x: x["cpu_pct"], reverse=True)

        return procs[:limit]
