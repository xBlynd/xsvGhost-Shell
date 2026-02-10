"""
Module: reminder_engine
Description: Active pulse tracker with Desktop Popup support.
"""
import os
import subprocess
from datetime import datetime
from src.core.vault_api import VaultAPI

class ReminderEngine:
    @staticmethod
    def show_popup(title, message):
        """Fires a system-level popup notification."""
        if os.name == 'nt': # Windows
            # Standard Windows MessageBox via PowerShell (Zero dependencies)
            cmd = f"powershell -Command \"[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('{message}', '{title}')\""
            subprocess.Popen(cmd, shell=True)
        else: # Linux / Debian
            subprocess.run(["notify-send", title, message])

    @staticmethod
    def check_reminders():
        v = VaultAPI()
        all_tasks = v.get_all_due_tasks()
        due_now = []
        now = datetime.now()
        
        for item in all_tasks:
            cat = item['category']
            task = item['task']
            try:
                due_time = datetime.strptime(task['due_date'], "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                if now >= due_time and not task.get("notified"):
                    due_now.append(item)
            except: continue 
        return due_now

    @staticmethod
    def silence(category, task_id):
        v = VaultAPI()
        tasks = v.get_tasks(category)
        for t in tasks:
            if t['id'] == task_id:
                t['notified'] = True
                break
        v.save_tasks(category, tasks)