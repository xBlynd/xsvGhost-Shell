"""
Module: remind
Description: Quick fire-and-forget reminders.
"""
import json
import datetime
from pathlib import Path
from src.core.reminder_engine import ReminderEngine

def run(args):
    if not args or len(args) < 2:
        print("\n⏰ QUICK REMINDER")
        print("Usage: remind \"Message\" <time>")
        return

    time_arg = args[-1]
    msg = " ".join(args[:-1]).strip('"')
    
    final_time = ReminderEngine.parse_time(time_arg)
    
    if not final_time:
        print(f"❌ Invalid time format: {time_arg}")
        return

    # Ensure path exists
    vault_dir = Path(__file__).parent.parent.parent / "data" / "vault" / "reminders"
    vault_dir.mkdir(parents=True, exist_ok=True)
    file_path = vault_dir / "quick.json"
    
    tasks = []
    if file_path.exists():
        try:
            with open(file_path, "r") as f: tasks = json.load(f)
        except: pass
    
    new_task = {
        "id": int(datetime.datetime.now().timestamp()),
        "title": msg,
        "due_date": final_time,
        "notified": False,
        "category": "quick"
    }
    tasks.append(new_task)
    
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=4)
        
    print(f"✅ Reminder Set: \"{msg}\" for {final_time}")