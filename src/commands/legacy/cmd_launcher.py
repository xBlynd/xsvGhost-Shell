import sys
import os
import json
import subprocess
import shutil
from pathlib import Path
from src.core.host_bridge import HostBridge

class Launcher:
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.config_path = self.root / "data" / "config" / "commands.json"
        self.library_path = self.root / "library"

    def load_commands(self):
        if not self.config_path.exists(): return {}
        try:
            with open(self.config_path, "r") as f:
                return json.load(f).get("commands", {})
        except: return {}

    def get_library_script(self, cmd_name):
        if not self.library_path.exists(): return None
        # Priority: Python > Node > PowerShell > Bash > Batch > Exe
        extensions = [".py", ".js", ".ps1", ".sh", ".bat", ".cmd", ".exe"]
        for ext in extensions:
            script_path = self.library_path / (cmd_name + ext)
            if script_path.exists(): return script_path
        return None

    def execute_script(self, path, args):
        ext = path.suffix.lower()
        cmd_str = str(path)
        try:
            if ext == ".js":
                if shutil.which("node"): subprocess.run(["node", cmd_str] + args, check=False)
                else: print("❌ Node.js not found.")
            elif ext == ".py":
                subprocess.run([sys.executable, cmd_str] + args, check=False)
            elif ext == ".ps1":
                exe = "pwsh" if shutil.which("pwsh") else "powershell"
                if shutil.which(exe): subprocess.run([exe, "-ExecutionPolicy", "Bypass", "-File", cmd_str] + args, check=False)
            elif ext == ".sh":
                if shutil.which("bash"): subprocess.run(["bash", cmd_str] + args, check=False)
            elif ext in [".bat", ".cmd"]:
                 if os.name == 'nt': subprocess.run(f'"{cmd_str}" {" ".join(args)}', shell=True, check=False)
            elif ext == ".exe":
                subprocess.run([cmd_str] + args, check=False)
            else:
                HostBridge.launch(cmd_str)
            return True
        except Exception as e:
            print(f"❌ Execution failed: {e}")
            return False

    def run(self, cmd, args):
        # 1. Aliases
        aliases = self.load_commands()
        if cmd in aliases:
            cfg = aliases[cmd]
            if cfg.get("confirm", False):
                 if input("⚠️  Sure? (y/n): ").lower() != "y": return True
            if cfg['type'] == 'script': return self.execute_script(self.root / cfg['path'], args)
            elif cfg['type'] == 'shell': 
                subprocess.run(f"{cfg['cmd']} {' '.join(args)}", shell=True)
                return True

        # 2. Library Auto-Discovery
        script_path = self.get_library_script(cmd)
        if script_path:
            print(f"📜 Library Found: {script_path.name}")
            return self.execute_script(script_path, args)

        return False