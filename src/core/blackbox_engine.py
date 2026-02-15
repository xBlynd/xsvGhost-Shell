"""
Engine 04: BlackBox Engine - The Network Operator
===================================================
Network interface enumeration, ping with jitter analysis,
traceroute, and future port scanning.

Compartmentalization:
- MUST NOT write to Vault (VaultEngine does that)
- Returns data structures, doesn't format output
"""

import subprocess
import platform
import statistics
import socket
import re
import time


class BlackBoxEngine:
    """The Network Operator - connectivity and diagnostics."""

    ENGINE_NAME = "blackbox"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.os_type = platform.system().upper()

    def ping(self, host, count=4):
        """
        Ping a host with jitter/variance analysis.
        Returns structured data (not formatted output).
        """
        times = []
        lost = 0

        for i in range(count):
            start = time.time()
            try:
                if self.os_type == "WINDOWS":
                    cmd = ["ping", "-n", "1", "-w", "2000", host]
                else:
                    cmd = ["ping", "-c", "1", "-W", "2", host]

                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=5
                )

                # Parse time from output
                output = result.stdout
                if self.os_type == "WINDOWS":
                    match = re.search(r'time[=<](\d+)ms', output)
                else:
                    match = re.search(r'time=(\d+\.?\d*)\s*ms', output)

                if match:
                    times.append(float(match.group(1)))
                else:
                    lost += 1

            except (subprocess.TimeoutExpired, Exception):
                lost += 1

        if not times:
            return {
                "host": host,
                "status": "UNREACHABLE",
                "packets_sent": count,
                "packets_lost": count,
                "loss_pct": 100.0,
            }

        avg = statistics.mean(times)
        jitter = statistics.stdev(times) if len(times) > 1 else 0

        return {
            "host": host,
            "status": "UNSTABLE" if jitter > 20 else "STABLE",
            "average_ms": round(avg, 2),
            "min_ms": round(min(times), 2),
            "max_ms": round(max(times), 2),
            "jitter_ms": round(jitter, 2),
            "packets_sent": count,
            "packets_lost": lost,
            "loss_pct": round((lost / count) * 100, 1),
            "times": times,
        }

    def get_interfaces(self):
        """Enumerate network interfaces."""
        interfaces = []
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            interfaces.append({
                "name": "primary",
                "hostname": hostname,
                "ip": local_ip,
            })
        except Exception:
            pass

        # Get all IPs
        try:
            for info in socket.getaddrinfo(socket.gethostname(), None):
                ip = info[4][0]
                if ip not in [i.get("ip") for i in interfaces]:
                    interfaces.append({
                        "name": f"interface-{len(interfaces)}",
                        "ip": ip,
                    })
        except Exception:
            pass

        return interfaces

    def check_internet(self):
        """Quick internet connectivity check."""
        targets = ["8.8.8.8", "1.1.1.1"]
        for target in targets:
            result = self.ping(target, count=1)
            if result["status"] != "UNREACHABLE":
                return {"connected": True, "via": target, "latency_ms": result["average_ms"]}
        return {"connected": False}

    def resolve_dns(self, hostname):
        """Resolve a hostname to IP."""
        try:
            ip = socket.gethostbyname(hostname)
            return {"hostname": hostname, "ip": ip, "resolved": True}
        except socket.gaierror as e:
            return {"hostname": hostname, "resolved": False, "error": str(e)}
