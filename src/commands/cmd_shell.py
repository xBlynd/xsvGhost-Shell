import sys
import os
import socket
import subprocess
import shlex
import getpass
import importlib
from pathlib import Path

# IMPORT THE NEW CORE
from src.core.host_engine import HostEngine
from src.commands import cmd_launcher

# --- CONFIGURATION ---
DEFAULT_USER = "admin"
DEFAULT_PASS = "admin"

def login():
    """Simple Security Check"""
    HostEngine.clear_screen()
    print("🔒 xsvCommandCenter | SECURE SESSION")
    print("-" * 35)
    
    while True:
        try:
            u = input("User: ")
            p = getpass.getpass("Pass: ")
            if u == DEFAULT_USER and p == DEFAULT_PASS:
                return True
            print("❌ Access Denied.")
        except KeyboardInterrupt:
            return False

def run(args):
    # 1. AUTHENTICATE
    if not login(): return

    # 2. INITIALIZE SESSION
    HostEngine.clear_screen()
    hostname = socket.gethostname()
    username = os.getlogin()
    print(f"\n👻 GHOST SHELL ONLINE")
    print(f"   Target: {username}@{hostname}")
    print("-" * 40)
    print("Type 'help' for options. Type 'exit' to disconnect.")
    print("Type 'sh' or 'cmd' to drop into raw host terminal.\n")

    # 3. INTERACTIVE LOOP
    while True:
        try:
            cwd = os.getcwd()
            # Shorten path for display
            display_cwd = cwd
            if len(cwd) > 30: display_cwd = "..." + cwd[-30:]
            
            prompt = f"xsv@{hostname} [{display_cwd}] > "
            user_input = input(prompt).strip()
            
            if not user_input: continue

            parts = shlex.split(user_input)
            cmd = parts[0].lower()
            cmd_args = parts[1:]

            # --- A. SHELL CONTROLS ---
            if cmd in ["exit", "quit"]:
                print("🔌 Disconnecting...")
                break
            
            if cmd in ["clear", "cls"]:
                HostEngine.clear_screen()
                continue
                
            if cmd == "cd":
                target = cmd_args[0] if cmd_args else "."
                try: os.chdir(target)
                except Exception as e: print(f"❌ {e}")
                continue

            # --- B. ESCAPE HATCHES (The "Safety Net") ---
            
            # MODE 2: Force Host Execution ('exec ping')
            if cmd == "exec":
                if not cmd_args:
                    print("⚠️ Usage: exec <command>")
                    continue
                # Join the rest of the arguments exactly as typed
                full_cmd = " ".join(cmd_args)
                print(f"Executing on Host: {full_cmd}")
                try:
                    subprocess.run(full_cmd, shell=True)
                except Exception as e:
                    print(f"❌ Execution failed: {e}")
                continue

            # MODE 3: Drop to Raw Shell ('sh' or 'cmd')
            if cmd in ["sh", "cmd", "bash", "powershell"]:
                print(f"⚠️  Dropping to Host Shell ({cmd})...")
                print("   Type 'exit' to return to Ghost Shell.")
                try:
                    # Windows prefers 'cmd', Linux 'bash'
                    shell_cmd = "cmd" if os.name == 'nt' else "bash"
                    # If they specifically asked for powershell, give it to them
                    if cmd == "powershell": shell_cmd = "powershell"
                    
                    subprocess.call(shell_cmd, shell=True)
                except Exception as e:
                    print(f"❌ Failed to launch shell: {e}")
                
                print("\n👻 Welcome back to Ghost Shell.")
                continue

            # --- C. ALIASES (Your "Shortcuts") ---
            if cmd == "info":
                import src.commands.cmd_host as h
                h.run(["info"])
                continue
            
            if cmd == "ps":
                import src.commands.cmd_host as h
                h.run(["ps"])
                continue

            # --- D. MODULE ROUTING (Mode 1: The "Smart" Way) ---
            try:
                # Tries to find src/commands/cmd_{cmd}.py
                module = importlib.import_module(f"src.commands.cmd_{cmd}")
                module.run(cmd_args)
                continue
            except ModuleNotFoundError:
                pass 

            # --- E. MAGIC COMMANDS ---
            launcher = cmd_launcher.Launcher()
            if launcher.run(cmd):
                continue

            # --- F. SYSTEM FALLBACK (Lazy Mode) ---
            # If nothing else matches, run it as a Windows/Linux command
            try:
                subprocess.run(user_input, shell=True)
            except Exception as e:
                print(f"❌ System Error: {e}")

        except KeyboardInterrupt:
            print("\nType 'exit' to quit.")