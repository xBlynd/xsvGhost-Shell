"""
Ghost Shell Inline Login — Challenge System
============================================
Handles the 'login' command experience.
"""

import os
import sys
import questionary
import time
from datetime import datetime

def clear_screen():
    """Clear the terminal screen based on OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_login_challenge(kernel):
    """
    The 'Login Sequence': 
    1. Clear Screen
    2. Logo
    3. Cool Info
    4. Passphrase Challenge
    """
    clear_screen()
    
    # 1. Show Logo (from Interface Engine)
    interface = kernel.get_engine("interface")
    security = kernel.get_engine("security")
    
    # We show the GOD banner for the login screen to look cool
    if interface:
        print(interface.BANNER_GOD)
    else:
        print("\n   === GHOST SHELL PHOENIX ===\n")

    # 2. Show 'Cool Info' Stats
    core = kernel.get_engine("ghost_core")
    heartbeat = kernel.get_engine("heartbeat")
    vault = kernel.get_engine("vault")
    
    node_id = core.node_id if core else "Unknown"
    uptime = f"{heartbeat.check_health()['uptime_seconds']}s" if heartbeat else "0s"
    todo_count = "0"
    if vault:
        todo_count = str(len(vault.todo_list().get("items", [])))

    print(f"   [ NODE: {node_id} ] [ UPTIME: {uptime} ] [ TODOS: {todo_count} ]")
    print(f"   " + "—" * 50 + "\n")

    # 3. Credentials Challenge
    # We fetch the god key data to validate the passphrase
    god_key_path = os.path.join(kernel.root_dir, "data", "keys", "god.key")
    
    # If no god key exists, we can't really 'login' normally (first boot case handled by security engine)
    if not os.path.exists(god_key_path):
        print("   [!] No God Key detected. Please run standard boot.")
        time.sleep(2)
        return False

    try:
        import json
        with open(god_key_path, 'r') as f:
            key_data = json.load(f)
        
        passphrase = questionary.password(
            "   ENTER MASTERKEY PASSPHRASE:",
            style=questionary.Style([
                ('question', 'fg:#00ff00 bold'),
                ('answer', 'fg:#ffff00'),
            ])
        ).ask()

        if not passphrase:
            return False

        if security.validate_passphrase(passphrase, key_data):
            print("\n   [✓] ACCESS GRANTED. Initializing shell...")
            time.sleep(1)
            return True
        else:
            print("\n   [!] ACCESS DENIED. Incorrect passphrase.")
            time.sleep(2)
            return False

    except Exception as e:
        print(f"   [!] Login Error: {e}")
        time.sleep(2)
        return False
