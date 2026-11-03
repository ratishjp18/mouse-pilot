"""
Mouse Pilot - Windows Desktop Application
A lightweight utility for scheduled cursor movement and system keep-awake management.
"""

import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from services.settings_manager import SettingsManager

# Enable High DPI scaling
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def is_already_running():
    """Check if another instance of Mouse Pilot is already running using Windows mutex"""
    if sys.platform != 'win32':
        return False
    
    # Create a named mutex
    mutex_name = "MousePilot_SingleInstance_Mutex"
    
    # Try to create the mutex
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, False, mutex_name)
    
    # Check if mutex already exists (another instance is running)
    ERROR_ALREADY_EXISTS = 183
    if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        kernel32.CloseHandle(mutex)
        return True
    
    # Store mutex handle to keep it alive for the lifetime of the app
    # We don't close it - it will be released when the process exits
    return False


def bring_existing_to_front():
    """Try to bring the existing Mouse Pilot window to the front"""
    if sys.platform != 'win32':
        return
    
    import ctypes.wintypes
    
    # Find the existing Mouse Pilot window
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
    ShowWindow = ctypes.windll.user32.ShowWindow
    SW_RESTORE = 9
    
    def enum_callback(hwnd, lparam):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            if "Mouse Pilot" in buff.value:
                ShowWindow(hwnd, SW_RESTORE)
                SetForegroundWindow(hwnd)
                return False  # Stop enumeration
        return True  # Continue enumeration
    
    EnumWindows(EnumWindowsProc(enum_callback), 0)


class MousePilotApp:
    """Main application controller"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Mouse Pilot")
        self.app.setOrganizationName("Mouse Pilot")
        
        # Set application icon
        icon_path = get_resource_path(os.path.join("assets", "mouse_pilot.ico"))
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
        
        # Prevent app from quitting when window is hidden to tray
        self.app.setQuitOnLastWindowClosed(False)
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Create main window
        self.main_window = MainWindow(self.settings_manager)
        self.main_window.show()
    
    def run(self):
        """Start the application event loop"""
        return self.app.exec()


def main():
    """Application entry point"""
    # Check if already running
    if is_already_running():
        # Try to bring existing window to front
        bring_existing_to_front()
        sys.exit(0)
    
    app = MousePilotApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
