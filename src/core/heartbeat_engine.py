"""
HeartbeatEngine - System Health Monitor
Runs in background thread, monitors all engines, auto-recovery.
"""
import time
import threading
from queue import Queue, Empty

class HeartbeatEngine:
    """The Immune System - Monitors and heals the Ghost Shell"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.message_queue = Queue()
        self.check_interval = 5  # seconds
        self.kernel = None  # Set by kernel after initialization
    
    def initialize(self):
        """Start the heartbeat thread"""
        self.running = True
        self.thread = threading.Thread(target=self._pulse, daemon=True, name="HeartbeatEngine")
        self.thread.start()
        print("HeartbeatEngine started")
    
    def _pulse(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Check message queue
                try:
                    message = self.message_queue.get(timeout=0.1)
                    self._handle_message(message)
                except Empty:
                    pass
                
                # Health checks
                if self.kernel:
                    health = self.kernel.monitor_health()
                    self._check_health(health)
                
                # Check for scheduled tasks (if PulseEngine is available)
                # TODO: Integrate with PulseEngine
                
                time.sleep(self.check_interval)
            
            except Exception as e:
                print(f"⚠ Heartbeat error: {e}")
                time.sleep(self.check_interval)
    
    def _handle_message(self, message):
        """Process incoming messages from other engines"""
        msg_type = message.get('type')
        
        if msg_type == 'health_check':
            # Respond with health status
            pass
        elif msg_type == 'restart_request':
            engine_name = message.get('engine')
            self._attempt_restart(engine_name)
    
    def _check_health(self, health_data):
        """Analyze engine health and take action"""
        for engine_name, status in health_data.items():
            if status['state'] == 'failed':
                if status['restarts'] < 3:
                    print(f"⚠ {engine_name} failed, attempting restart...")
                    self._attempt_restart(engine_name)
    
    def _attempt_restart(self, engine_name):
        """Request kernel to restart failed engine"""
        if self.kernel:
            wrapper = self.kernel.engines.get(engine_name)
            if wrapper:
                wrapper.restart()
    
    def send_message(self, message):
        """Thread-safe message sending"""
        self.message_queue.put(message)
    
    def shutdown(self):
        """Stop the heartbeat thread"""
        print("Stopping HeartbeatEngine...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("HeartbeatEngine stopped")
