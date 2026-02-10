import sys, os, socket, subprocess, shlex, getpass, importlib, json, threading, time
from pathlib import Path
from src.core.host_engine import HostEngine
from src.commands import cmd_launcher
from src.core.reminder_engine import ReminderEngine

# CONFIG
DEFAULT_USER = "admin"
DEFAULT_PASS = "admin"

def get_version_display():
    try:
        path = Path(__file__).parent.parent.parent / "data" / "version.json"
        if path.exists():
            with open(path, "r") as f:
                d = json.load(f)
                return f"v{d['major']}.{d['minor']}.{d['patch']} (Build {d['build']})"
    except: pass
    return "v6.0-Ghost"

def login():
    HostEngine.clear_screen()
    print("🔒 xsvCommandCenter | SECURE SESSION")
    print("-" * 35)
    while True:
        try:
            u = input("User: ")
            p = getpass.getpass("Pass: ")
            if u == DEFAULT_USER and p == DEFAULT_PASS: return True
            print("❌ Access Denied.")
        except KeyboardInterrupt: return False

def reminder_worker():
    """The Background Heartbeat Thread."""
    # We use a global variable so we can 'kill' the thread logic on reload
    while getattr(threading.current_thread(), "do_run", True):
        try:
            cfg_path = Path(__file__).parent.parent.parent / "data" / "config" / "reminders.json"
            cfg = {"terminal_alerts": True, "popup_alerts": True, "check_interval_seconds": 30}
            if cfg_path.exists():
                with open(cfg_path, "r") as f: cfg = json.load(f)

            # Reload the engine logic dynamically inside the thread
            importlib.reload(sys.modules['src.core.reminder_engine'])
            from src.core.reminder_engine import ReminderEngine
            
            due = ReminderEngine.check_reminders()
            for item in due:
                title = f"🔔 {item['category'].upper()} REMINDER"
                msg = item['task']['title']
                if cfg.get("terminal_alerts"): print(f"\n\n{title}\n> {msg}\n")
                if cfg.get("popup_alerts"): ReminderEngine.show_popup(title, msg)
                ReminderEngine.silence(item['category'], item['task']['id'])
            
            time.sleep(cfg.get("check_interval_seconds", 30))
        except: time.sleep(10)

def run(args):
    if not login(): return
    
    # Start the background thread
    t = threading.Thread(target=reminder_worker, daemon=True)
    t.do_run = True
    t.start()
    
    HostEngine.clear_screen()
    hostname = socket.gethostname()
    print(f"\n👻 GHOST SHELL ONLINE [{get_version_display()}]")
    print(f"   Target: {os.getlogin()}@{hostname}\n" + "-"*40)

    while True:
        try:
            prompt = f"xsv@{hostname} [{os.getcwd()[-20:]}] > "
            user_input = input(prompt).strip()
            if not user_input: continue

            parts = shlex.split(user_input)
            cmd = parts[0].lower()
            cmd_args = parts[1:]

            if cmd in ["exit", "quit"]: break
            if cmd in ["clear", "cls"]: 
                HostEngine.clear_screen()
                continue
            if cmd == "cd":
                try: os.chdir(cmd_args[0] if cmd_args else ".")
                except Exception as e: print(f"❌ {e}")
                continue

            if cmd == "reload":
                # Kill existing thread logic before reloading
                t.do_run = False
                importlib.invalidate_caches()
                print("♻️  System Reloaded. Heartbeat Reseting...")
                # Restart the thread
                t = threading.Thread(target=reminder_worker, daemon=True)
                t.do_run = True
                t.start()
                continue

            # --- SMART ROUTER ---
            # 1. System
            try:
                module = importlib.import_module(f"src.commands.cmd_{cmd}")
                module.run(cmd_args)
                continue
            except ModuleNotFoundError: pass 

            # 2. Custom
            try:
                module = importlib.import_module(f"src.commands.custom.cmd_{cmd}")
                module.run(cmd_args)
                continue
            except ModuleNotFoundError: pass 

            # 3. Library Fallback
            launcher = cmd_launcher.Launcher()
            if launcher.run(cmd, cmd_args): continue

            # 4. OS Fallback
            subprocess.run(user_input, shell=True)

        except KeyboardInterrupt:
            print("\nType 'exit' to quit.")