"""
BlackBox Engine - The Network Operator
Network diagnostics with jitter analysis
"""

import subprocess
import platform
import statistics
import re

class BlackBoxEngine:
    """Network diagnostics and analysis"""
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "blackbox"
        self.os_type = platform.system()
    
    def ping(self, host, count=10):
        """
        Ping with jitter variance analysis.
        This is what makes Ghost Shell's ping better than the OS default.
        """
        times = []
        
        # Platform-specific ping command
        if self.os_type == "Windows":
            cmd = ["ping", "-n", str(count), host]
        else:
            cmd = ["ping", "-c", str(count), host]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=count + 5
            )
            
            # Parse ping times
            if self.os_type == "Windows":
                pattern = r"time[=<](\d+)ms"
            else:
                pattern = r"time=(\d+\.?\d*) ms"
            
            matches = re.findall(pattern, result.stdout)
            times = [float(t) for t in matches]
            
        except subprocess.TimeoutExpired:
            return {"error": "Ping timeout"}
        except Exception as e:
            return {"error": str(e)}
        
        if not times:
            return {"error": "No response", "raw_output": result.stdout}
        
        # Calculate statistics
        avg = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        
        # Jitter (standard deviation) - the KEY metric
        jitter = statistics.stdev(times) if len(times) > 1 else 0
        
        # Stability assessment
        if jitter < 5:
            stability = "EXCELLENT"
        elif jitter < 20:
            stability = "GOOD"
        elif jitter < 50:
            stability = "FAIR"
        else:
            stability = "POOR"
        
        return {
            "host": host,
            "packets": count,
            "received": len(times),
            "loss_percent": ((count - len(times)) / count) * 100,
            "avg_ms": round(avg, 2),
            "min_ms": round(min_time, 2),
            "max_ms": round(max_time, 2),
            "jitter_ms": round(jitter, 2),
            "stability": stability,
            "times": times
        }
    
    def get_interfaces(self):
        """Get network interfaces (basic)"""
        import socket
        
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        return {
            "hostname": hostname,
            "local_ip": local_ip
        }
