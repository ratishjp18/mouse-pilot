"""
Mouse Pilot - Windows Desktop Application
A lightweight utility for scheduled cursor movement and system keep-awake management.
"""

import sys
import os
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


class MousePilotApp:
    """Main application controller"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Mouse Pilot")
        self.app.setOrganizationName("Mouse Pilot")
        
        # Set application icon
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
        
        # Prevent multiple instances
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
    app = MousePilotApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
