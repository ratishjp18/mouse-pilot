"""
Mouse Controller for Mouse Pilot
Handles cursor movement using PyAutoGUI
"""

import pyautogui
from typing import Tuple


# Configure PyAutoGUI
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Small pause between PyAutoGUI calls


class MouseController:
    """Control mouse cursor movement"""
    
    def __init__(self):
        self.last_position = None
    
    def get_cursor_position(self) -> Tuple[int, int]:
        """Get current cursor position"""
        return pyautogui.position()
    
    def move_cursor(self, distance: int = 5):
        """
        Move cursor by a small distance and return to original position
        
        Args:
            distance: Number of pixels to move
        """
        try:
            # Get current position
            original_x, original_y = self.get_cursor_position()
            
            # Get screen size
            screen_width, screen_height = pyautogui.size()
            
            # Calculate new position (move right and down)
            new_x = original_x + distance
            new_y = original_y + distance
            
            # Ensure we stay within screen bounds
            new_x = max(0, min(new_x, screen_width - 1))
            new_y = max(0, min(new_y, screen_height - 1))
            
            # Move to new position
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            
            # Move back to original position
            pyautogui.moveTo(original_x, original_y, duration=0.1)
            
            self.last_position = (original_x, original_y)
            
        except Exception as e:
            print(f"Error moving cursor: {e}")
    
    def move_to_position(self, x: int, y: int, duration: float = 0.2):
        """
        Move cursor to specific position
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to take for the move
        """
        try:
            screen_width, screen_height = pyautogui.size()
            
            # Ensure position is within screen bounds
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))
            
            pyautogui.moveTo(x, y, duration=duration)
            self.last_position = (x, y)
            
        except Exception as e:
            print(f"Error moving to position: {e}")
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen size"""
        return pyautogui.size()
    
    def is_position_safe(self, x: int, y: int) -> bool:
        """
        Check if a position is safe (within screen bounds)
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is safe
        """
        screen_width, screen_height = pyautogui.size()
        return 0 <= x < screen_width and 0 <= y < screen_height
