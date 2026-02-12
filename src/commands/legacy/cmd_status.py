"""
Module: status
Description: Sequential diagnostic tool showing real-time testing followed by summary.
"""
import threading
import datetime
from pathlib import Path
from src.core.vault_api import VaultAPI
from src.core.info_engine import InfoEngine

def run(args):
    print("\n🔍 xsv COMMAND CENTER - SYSTEM DIAGNOSTICS")
    print("=" * 45)
    
    # 1. RUN TESTS FIRST (The "Loading" Feed)
    print("🛠️  RUNNING INTEGRITY TESTS...")
    print("-" * 45)
    
    def streamer(msg): print(msg)
    # This calls your info_engine to stream [TESTING] lines
    health_report = InfoEngine.verify_all_commands(verbose_callback=streamer)
    
    # 2. CONSOLIDATED SUMMARY
    print("-" * 45)
    print("📊 SYSTEM SUMMARY:")
    
    v = VaultAPI()
    threads = [t.name for t in threading.enumerate()]
    pulse_active = "ReminderPulse" in threads
    
    print(f"📂 VAULT STORAGE:  {'[ OK ]' if v.vault_dir.exists() else '[ ERROR ]'}")
    print(f"💓 CORE HEARTBEAT: {'[ ACTIVE ]' if pulse_active else '[ STOPPED ]'}")

    for category, cmds in health_report.items():
        if not cmds: continue
        broken = [c for c in cmds if "❌" in c[1]]
        if not broken:
            print(f"  [{category:<7}] ✅ All {len(cmds)} modules functioning.")
        else:
            print(f"  [{category:<7}] ⚠️  {len(broken)} Issues detected.")
            for name, status in broken:
                print(f"    -> {name:<12} {status}")

    print("\n⚙️  ACTIVE ENGINES:")
    print(f"  Reminders:   [{'ONLINE' if pulse_active else 'OFFLINE'}]")
    print(f"  Diagnostics: [ READY ]")
    print("-" * 45)