"""
Module: todo
Description: Advanced Task Manager with Status, Description, and Relative Reminders.
"""
import sys
import argparse
import datetime
from src.core.vault_api import VaultAPI
from src.core.reminder_engine import ReminderEngine

def run(args):
    v = VaultAPI()
    parser = argparse.ArgumentParser(prog="todo")
    parser.add_argument("action", choices=["add", "list", "done", "edit", "del"], nargs="?")
    parser.add_argument("id_or_title", nargs="?", default="")
    parser.add_argument("--cat", default="work")
    parser.add_argument("--due", default=None)
    parser.add_argument("--desc", default="")

    if not args:
        print("\n📝 xsv TASK MANAGER")
        print("Usage: todo <add|list|done|edit> [args]")
        return

    try: p = parser.parse_args(args)
    except: return

    if p.action == "add":
        # Math for '10m' or '1h'
        final_time = ReminderEngine.parse_time(p.due) if p.due else None
        tasks = v.get_tasks(p.cat)
        
        new_task = {
            "id": len(tasks) + 1,
            "title": p.id_or_title,
            "desc": p.desc,
            "category": p.cat,
            "due_date": final_time,
            "status": "pending",
            "notified": False,
            "created_at": str(datetime.datetime.now())
        }
        tasks.append(new_task)
        v.save_tasks(p.cat, tasks)
        print(f"✅ Added to {p.cat.upper()}: {p.id_or_title} (Due: {final_time})")

    elif p.action == "list":
        tasks = v.get_tasks(p.cat)
        print(f"\n📋 {p.cat.upper()} TASKS")
        print("-" * 40)
        for t in tasks:
            mark = "[x]" if t['status'] == 'completed' else "[ ]"
            due = f" 🔔 {t['due_date']}" if t['due_date'] else ""
            print(f" {t['id']}. {mark} {t['title']}{due}")
            if t['desc']: print(f"    └─ {t['desc']}")

    elif p.action == "done":
        tasks = v.get_tasks(p.cat)
        for t in tasks:
            if str(t['id']) == p.id_or_title:
                t['status'] = 'completed'
                v.save_tasks(p.cat, tasks)
                print(f"✅ Task {p.id_or_title} marked complete.")
                return

    elif p.action == "edit":
        # Usage: todo edit 1 --desc "New description" --due "20:00"
        tasks = v.get_tasks(p.cat)
        for t in tasks:
            if str(t['id']) == p.id_or_title:
                if p.desc: t['desc'] = p.desc
                if p.due: t['due_date'] = ReminderEngine.parse_time(p.due)
                v.save_tasks(p.cat, tasks)
                print(f"✅ Task {p.id_or_title} updated.")
                return