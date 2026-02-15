"""
Pulse Engine - The Heartbeat
Background task scheduler with daemon threads
"""

import threading
import time
from datetime import datetime

class PulseEngine:
    """
    Background task scheduler.
    Uses daemon threads - NEVER blocks main shell.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "pulse"
        self.running = False
        self.tasks = []
        self.thread = None
    
    def post_boot(self):
        """Start pulse after boot"""
        self.start()
    
    def start(self):
        """Start background pulse"""
        if self.running:
            return
        
        self.running = True
        
        # THE ANTI-LAG PATTERN - daemon=True
        self.thread = threading.Thread(target=self._pulse_loop, daemon=True)
        self.thread.start()
    
    def _pulse_loop(self):
        """Background loop - runs forever but doesn't block"""
        while self.running:
            # Check scheduled tasks
            for task in self.tasks:
                if task.should_run():
                    try:
                        task.run()
                    except Exception as e:
                        print(f"[Pulse] Task error: {e}")
            
            # Sleep to avoid CPU spin
            time.sleep(1)
    
    def stop(self):
        """Stop pulse"""
        self.running = False
    
    def schedule(self, task):
        """Schedule a task"""
        self.tasks.append(task)


class Task:
    """Base task class"""
    def __init__(self, name, interval_seconds, callback):
        self.name = name
        self.interval = interval_seconds
        self.callback = callback
        self.last_run = None
    
    def should_run(self):
        """Check if task should run"""
        if self.last_run is None:
            return True
        
        elapsed = (datetime.now() - self.last_run).total_seconds()
        return elapsed >= self.interval
    
    def run(self):
        """Execute task"""
        self.callback()
        self.last_run = datetime.now()
