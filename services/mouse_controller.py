"""
Mouse Controller for Mouse Pilot
Handles cursor movement using Windows API (SendInput) for better system recognition
"""

import ctypes
import sys
from typing import Tuple


# Windows API structures and constants
if sys.platform == 'win32':
    import ctypes.wintypes
    
    # Input type constants
    INPUT_MOUSE = 0
    
    # Mouse event flags
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_ABSOLUTE = 0x8000
    
    # Structure for mouse input
    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ("dx", ctypes.wintypes.LONG),
            ("dy", ctypes.wintypes.LONG),
            ("mouseData", ctypes.wintypes.DWORD),
            ("dwFlags", ctypes.wintypes.DWORD),
            ("time", ctypes.wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
        ]
    
    # Union for input
    class INPUT_UNION(ctypes.Union):
        _fields_ = [
            ("mi", MOUSEINPUT),
        ]
    
    # Input structure
    class INPUT(ctypes.Structure):
        _fields_ = [
            ("type", ctypes.wintypes.DWORD),
            ("union", INPUT_UNION),
        ]


class MouseController:
    """Control mouse cursor movement using Windows API"""
    
    def __init__(self):
        self.last_position = None
        self.is_windows = sys.platform == 'win32'
    
    def get_cursor_position(self) -> Tuple[int, int]:
        """Get current cursor position"""
        if self.is_windows:
            point = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
            return (point.x, point.y)
        return (0, 0)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen size"""
        if self.is_windows:
            width = ctypes.windll.user32.GetSystemMetrics(0)
            height = ctypes.windll.user32.GetSystemMetrics(1)
            return (width, height)
        return (1920, 1080)
    
    def _send_mouse_input(self, x: int, y: int):
        """Send mouse input using Windows SendInput API"""
        if not self.is_windows:
            return
        
        # Convert to absolute coordinates (0-65535 range)
        screen_width, screen_height = self.get_screen_size()
        abs_x = int(x * 65535 / screen_width)
        abs_y = int(y * 65535 / screen_height)
        
        # Create mouse input structure
        mouse_input = INPUT()
        mouse_input.type = INPUT_MOUSE
        mouse_input.union.mi.dx = abs_x
        mouse_input.union.mi.dy = abs_y
        mouse_input.union.mi.mouseData = 0
        mouse_input.union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        mouse_input.union.mi.time = 0
        mouse_input.union.mi.dwExtraInfo = None
        
        # Send input
        ctypes.windll.user32.SendInput(1, ctypes.byref(mouse_input), ctypes.sizeof(INPUT))
    
    def move_cursor(self, distance: int = 5):
        """
        Move cursor by a small distance and return to original position
        Uses Windows SendInput API for proper system recognition
        
        Args:
            distance: Number of pixels to move
        """
        try:
            # Get current position
            original_x, original_y = self.get_cursor_position()
            
            # Get screen size
            screen_width, screen_height = self.get_screen_size()
            
            # Calculate new position (move right and down)
            new_x = original_x + distance
            new_y = original_y + distance
            
            # Ensure we stay within screen bounds
            new_x = max(0, min(new_x, screen_width - 1))
            new_y = max(0, min(new_y, screen_height - 1))
            
            # Move to new position using Windows API
            self._send_mouse_input(new_x, new_y)
            
            # Small delay
            import time
            time.sleep(0.05)
            
            # Move back to original position
            self._send_mouse_input(original_x, original_y)
            
            self.last_position = (original_x, original_y)
            
        except Exception as e:
            print(f"Error moving cursor: {e}")
    
    def move_to_position(self, x: int, y: int, duration: float = 0.2):
        """
        Move cursor to specific position
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to take for the move (ignored for API call)
        """
        try:
            screen_width, screen_height = self.get_screen_size()
            
            # Ensure position is within screen bounds
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))
            
            self._send_mouse_input(x, y)
            self.last_position = (x, y)
            
        except Exception as e:
            print(f"Error moving to position: {e}")
    
    def is_position_safe(self, x: int, y: int) -> bool:
        """
        Check if a position is safe (within screen bounds)
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is safe
        """
        screen_width, screen_height = self.get_screen_size()
        return 0 <= x < screen_width and 0 <= y < screen_height
