"""
Keep Awake Manager for Mouse Pilot
Prevents system sleep using Windows API
"""

import ctypes
import sys


# Windows API constants
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002


class KeepAwakeManager:
    """Manage Windows keep-awake functionality"""
    
    def __init__(self):
        self.is_enabled = False
        self.is_windows = sys.platform == 'win32'
    
    def enable(self):
        """Enable keep-awake mode to prevent system sleep"""
        if not self.is_windows:
            print("Keep-awake is only supported on Windows")
            return False
        
        try:
            # Prevent system sleep and display sleep
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
            self.is_enabled = True
            print("Keep-awake mode enabled")
            return True
        except Exception as e:
            print(f"Error enabling keep-awake: {e}")
            return False
    
    def disable(self):
        """Disable keep-awake mode to restore normal sleep behavior"""
        if not self.is_windows:
            return False
        
        try:
            # Restore normal sleep behavior
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            self.is_enabled = False
            print("Keep-awake mode disabled")
            return True
        except Exception as e:
            print(f"Error disabling keep-awake: {e}")
            return False
    
    def get_status(self) -> bool:
        """Get current keep-awake status"""
        return self.is_enabled
