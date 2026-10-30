"""
Scheduler for Mouse Pilot
Handles timing and scheduling of mouse movements
"""

from datetime import datetime, timedelta
from PySide6.QtCore import QTimer, QObject, Signal


class Scheduler(QObject):
    """Schedule periodic actions using QTimer"""
    
    action_triggered = Signal()  # Emitted when scheduled action should execute
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer_timeout)
        self.interval_seconds = 60
        self.next_action_time = None
        self.is_running = False
        self.is_paused = False
    
    def start(self, interval_seconds: int):
        """
        Start the scheduler
        
        Args:
            interval_seconds: Interval between actions in seconds
        """
        self.interval_seconds = interval_seconds
        self.is_running = True
        self.is_paused = False
        self._schedule_next()
    
    def stop(self):
        """Stop the scheduler"""
        self.timer.stop()
        self.is_running = False
        self.is_paused = False
        self.next_action_time = None
    
    def pause(self):
        """Pause the scheduler"""
        self.timer.stop()
        self.is_paused = True
        self.next_action_time = None
    
    def resume(self):
        """Resume the scheduler from pause"""
        if self.is_paused:
            self.is_paused = False
            self._schedule_next()
    
    def set_interval(self, interval_seconds: int):
        """
        Update the interval
        
        Args:
            interval_seconds: New interval in seconds
        """
        self.interval_seconds = interval_seconds
        if self.is_running and not self.is_paused:
            # Restart timer with new interval
            self.timer.stop()
            self._schedule_next()
    
    def get_next_action_time(self):
        """Get the time of the next scheduled action"""
        return self.next_action_time
    
    def _schedule_next(self):
        """Schedule the next timer event"""
        if self.is_running and not self.is_paused:
            # Convert seconds to milliseconds for QTimer
            interval_ms = self.interval_seconds * 1000
            self.timer.start(interval_ms)
            self.next_action_time = datetime.now() + timedelta(seconds=self.interval_seconds)
    
    def _on_timer_timeout(self):
        """Handle timer timeout"""
        if self.is_running and not self.is_paused:
            self.action_triggered.emit()
            self._schedule_next()
