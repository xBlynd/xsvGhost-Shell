"""
Ghost Shell Claude-Style Login — Rich Dashboard
================================================
A sleek, modern login experience inspired by Claude-CLI.
"""

import os
import time
import getpass
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from rich.theme import Theme

# Set up Ghost Green theme
custom_theme = Theme({
    "ghost": "bold #00ff00",
    "info": "bold #00ffff",
    "warn": "bold #ffff00",
    "error": "bold #ff0000",
    "muted": "dim #888888",
})

console = Console(theme=custom_theme)

def show_claude_login(kernel):
    """
    The 'Claude-Style' Login Sequence:
    1. Elegant Logo + Stats Header
    2. Side-by-Side Status Panels
    3. Minimalist Passphrase Prompt
    """
    # 1. Gather Engine Data (Cool Info)
    core = kernel.get_engine("ghost_core")
    heartbeat = kernel.get_engine("heartbeat")
    vault = kernel.get_engine("vault")
    loader = kernel.get_engine("loader")
    security = kernel.get_engine("security")

    node_id = core.node_id if core else "Unknown"
    uptime = f"{heartbeat.check_health()['uptime_seconds']}s" if heartbeat else "0s"
    todo_count = str(len(vault.todo_list().get("items", []))) if vault else "0"
    cmd_count = str(len(kernel.commands))

    # 2. Render Elegant Dashboard
    console.print("\n")
    
    # ASCII Logo using rich text for coloring
    logo = Text(r"""
   ╔═══════════════════════════════════════════════════╗
   ║        G H O S T   S H E L L   P H O E N I X      ║
   ║                  v6.5 - Phoenix                   ║
   ╚═══════════════════════════════════════════════════╝
    """, style="ghost")
    console.print(logo, justify="center")

    # Stats Panels (Claude Style - side-by-side)
    panels = [
        Panel(f"[ghost]NODE ID[/]\n[info]{node_id}[/]", expand=False, border_style="ghost"),
        Panel(f"[ghost]UPTIME[/]\n[info]{uptime}[/]", expand=False, border_style="ghost"),
        Panel(f"[ghost]TODOS[/]\n[info]{todo_count}[/]", expand=False, border_style="ghost"),
        Panel(f"[ghost]CMDS[/]\n[info]{cmd_count}[/]", expand=False, border_style="ghost"),
    ]
    console.print(Columns(panels), justify="center")

    # 3. Secure Passphrase Challenge
    god_key_path = os.path.join(kernel.root_dir, "data", "keys", "god.key")
    if not os.path.exists(god_key_path):
        console.print("[error] [!] No God Key detected. First boot required.[/]")
        return False

    try:
        import json
        with open(god_key_path, 'r') as f:
            key_data = json.load(f)

        # Minimalist, clean prompt
        console.print("\n[muted] ── Authentication Required ── [/]")
        passphrase = getpass.getpass("    Enter Masterkey: ")

        if not passphrase:
            return False

        if security.validate_passphrase(passphrase, key_data):
            console.print("\n[ghost] [✓] Authenticated. Initializing shell session...[/]\n")
            time.sleep(0.5)
            return True
        else:
            console.print("\n[error] [!] Access Denied. Passphrase mismatch.[/]\n")
            return False

    except Exception as e:
        console.print(f"[error] [!] Internal login error: {e}[/]")
        return False
