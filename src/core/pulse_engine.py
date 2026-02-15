"""
PulseEngine - The Timekeeper (Engine #6)
Cross-platform scheduler with precision timing and notifications.

Responsibilities:
- Relative time parsing (10s, 5m, 2h)
- Cron-style job scheduling
- Toast notifications (Windows/Linux)
- Reminder catch-up logic (if shell was sleeping)
"""
import os
import subprocess
import json
import platform
from datetime import datetime, timedelta
from pathlib import Path
from src.core.vault_api import VaultAPI  # Will be updated to vault_engine later

class PulseEngine:
    """
    The Timekeeper - Engine #6
    Makes the shell conscious of time and schedules.
    """
    
    @staticmethod
    def parse_time(time_input):
        """
        Parse relative time expressions:
        - "10s" -> 10 seconds from now
        - "5m" -> 5 minutes from now
        - "2h" -> 2 hours from now
        - "14:30" -> Today at 2:30 PM
        - "14:30:00" -> Exact time format
        """
        if not time_input: 
            return None
        
        now = datetime.now()
        ts = str(time_input).lower().strip()
        
        try:
            # Relative seconds
            if ts.endswith('s'):
                return (now + timedelta(seconds=int(ts[:-1]))).strftime("%H:%M:%S")
            
            # Relative minutes
            if ts.endswith('m'):
                return (now + timedelta(minutes=int(ts[:-1]))).strftime("%H:%M:%S")
            
            # Relative hours
            if ts.endswith('h'):
                return (now + timedelta(hours=int(ts[:-1]))).strftime("%H:%M:%S")
            
            # Absolute time (HH:MM or HH:MM:SS)
            if ":" in ts:
                parts = ts.split(":")
                if len(parts) == 2:  # Add seconds if missing
                    return f"{ts}:00"
                return ts
        except:
            return None
        
        return None
    
    @staticmethod
    def show_popup(title, message):
        """
        Cross-platform notification dispatcher.
        Windows: Uses PowerShell toast.ps1 script
        Linux: Uses libnotify (notify-send)
        """
        current_os = platform.system()
        
        if current_os == "Windows":
            # Call the PowerShell script with arguments
            script_path = Path(__file__).parent / "toast.ps1"
            if script_path.exists():
                cmd = [
                    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", 
                    "-File", str(script_path), 
                    "-Title", title, 
                    "-Message", message
                ]
                # Run hidden (no console window)
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
        
        elif current_os == "Linux":
            # Use standard libnotify (part of most distros)
            try:
                subprocess.Popen(["notify-send", title, message])
            except FileNotFoundError:
                # Fallback if notify-send isn't installed
                print(f"\n[Linux Alert] {title}: {message}")
    
    @staticmethod
    def check_reminders():
        """
        Scan vault for due reminders and return list of tasks to fire.
        Implements 'catch-up' logic - if shell was asleep, fires all missed reminders.
        """
        v = VaultAPI()
        now_str = datetime.now().strftime("%H:%M:%S")
        due_list = []
        
        # 1. Check Quick Reminders (Fire & Forget)
        quick_path = v.vault_dir / "reminders" / "quick.json"
        if quick_path.exists():
            try:
                with open(quick_path, "r") as f:
                    quick_tasks = json.load(f)
                
                for t in quick_tasks:
                    due = t.get("due_date", "")
                    if len(due) == 5:  # Add seconds if HH:MM format
                        due += ":00"
                    
                    # LOGIC: If due time is NOW or passed (and not notified)
                    if due <= now_str and not t.get("notified"):
                        due_list.append({"category": "quick", "task": t})
            except:
                pass
        
        # 2. Check Standard Todo Lists
        for cat in ["work", "home", "xsv"]:
            tasks = v.get_tasks(cat)
            for t in tasks:
                due = t.get("due_date", "")
                if not due:
                    continue
                
                if len(due) == 5:  # Add seconds if needed
                    due += ":00"
                
                # Only fire if not completed and not already notified
                if due <= now_str and not t.get("notified") and t.get("status") != "completed":
                    due_list.append({"category": cat, "task": t})
        
        return due_list
    
    @staticmethod
    def silence(category, task_id):
        """
        Mark a reminder as handled (silenced).
        Quick reminders: Delete (fire & forget)
        Standard tasks: Mark as 'notified' to prevent re-firing
        """
        v = VaultAPI()
        
        if category == "quick":
            # Fire & Forget: Delete the task
            quick_path = v.vault_dir / "reminders" / "quick.json"
            if quick_path.exists():
                with open(quick_path, "r") as f:
                    tasks = json.load(f)
                
                tasks = [t for t in tasks if t['id'] != task_id]
                
                with open(quick_path, "w") as f:
                    json.dump(tasks, f, indent=4)
        else:
            # Standard: Mark notified
            tasks = v.get_tasks(category)
            for t in tasks:
                if t['id'] == task_id:
                    t['notified'] = True
            v.save_tasks(category, tasks)
    
    # ============================================================
    # FUTURE: CRON-STYLE SCHEDULING
    # ============================================================
    # - Execute commands at specific intervals
    # - "Every 10 minutes, run clean"
    # - "At 9:00 AM, run backup"
