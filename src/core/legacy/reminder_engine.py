"""
Module: reminder_engine
Description: Cross-platform scheduler (Windows/Linux) with 'Catch-Up' logic.
"""
import os
import subprocess
import json
import platform
from datetime import datetime, timedelta
from pathlib import Path
from src.core.vault_api import VaultAPI

class ReminderEngine:
    @staticmethod
    def parse_time(time_input):
        if not time_input: return None
        now = datetime.now()
        ts = str(time_input).lower().strip()
        try:
            if ts.endswith('s'):
                return (now + timedelta(seconds=int(ts[:-1]))).strftime("%H:%M:%S")
            if ts.endswith('m'):
                return (now + timedelta(minutes=int(ts[:-1]))).strftime("%H:%M:%S")
            if ts.endswith('h'):
                return (now + timedelta(hours=int(ts[:-1]))).strftime("%H:%M:%S")
            
            if ":" in ts:
                parts = ts.split(":")
                if len(parts) == 2: return f"{ts}:00"
                return ts
        except: return None
        return None

    @staticmethod
    def show_popup(title, message):
        """Dispatches notification based on OS."""
        current_os = platform.system()
        
        if current_os == "Windows":
            # Call the PowerShell script with arguments
            script_path = Path(__file__).parent / "toast.ps1"
            if script_path.exists():
                cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", 
                       "-File", str(script_path), "-Title", title, "-Message", message]
                # Run hidden
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
        v = VaultAPI()
        now_str = datetime.now().strftime("%H:%M:%S")
        due_list = []
        
        # 1. Check Quick Reminders
        quick_path = v.vault_dir / "reminders" / "quick.json"
        if quick_path.exists():
            try:
                with open(quick_path, "r") as f: quick_tasks = json.load(f)
                for t in quick_tasks:
                    due = t.get("due_date", "")
                    if len(due) == 5: due += ":00"
                    
                    # LOGIC: If due time is NOW or passed (and not notified)
                    if due <= now_str and not t.get("notified"):
                        due_list.append({"category": "quick", "task": t})
            except: pass

        # 2. Check Standard Todo Lists
        for cat in ["work", "home", "xsv"]:
            tasks = v.get_tasks(cat)
            for t in tasks:
                due = t.get("due_date", "")
                if not due: continue
                if len(due) == 5: due += ":00"
                
                if due <= now_str and not t.get("notified") and t.get("status") != "completed":
                    due_list.append({"category": cat, "task": t})
            
        return due_list

    @staticmethod
    def silence(category, task_id):
        v = VaultAPI()
        
        if category == "quick":
            # Fire & Forget: Delete the task
            quick_path = v.vault_dir / "reminders" / "quick.json"
            if quick_path.exists():
                with open(quick_path, "r") as f: tasks = json.load(f)
                tasks = [t for t in tasks if t['id'] != task_id]
                with open(quick_path, "w") as f: json.dump(tasks, f, indent=4)
        else:
            # Standard: Mark notified
            tasks = v.get_tasks(category)
            for t in tasks:
                if t['id'] == task_id:
                    t['notified'] = True
            v.save_tasks(category, tasks)