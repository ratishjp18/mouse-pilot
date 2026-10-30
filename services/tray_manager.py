"""
Tray Manager for Mouse Pilot
Handles system tray icon and menu
"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction


class TrayManager:
    """Manage system tray icon and interactions"""
    
    def __init__(self, parent=None, icon=None):
        """
        Initialize tray manager
        
        Args:
            parent: Parent widget
            icon: QIcon for the tray icon
        """
        self.parent = parent
        self.tray_icon = QSystemTrayIcon(icon, parent)
        self.menu = QMenu()
        
    def setup_menu(self, actions):
        """
        Setup the tray menu with actions
        
        Args:
            actions: List of tuples (label, callback) or None for separator
        """
        self.menu.clear()
        
        for action in actions:
            if action is None:
                self.menu.addSeparator()
            else:
                label, callback = action
                menu_action = QAction(label, self.parent)
                menu_action.triggered.connect(callback)
                self.menu.addAction(menu_action)
        
        self.tray_icon.setContextMenu(self.menu)
    
    def show(self):
        """Show the tray icon"""
        self.tray_icon.show()
    
    def hide(self):
        """Hide the tray icon"""
        self.tray_icon.hide()
    
    def set_tooltip(self, tooltip):
        """Set tray icon tooltip"""
        self.tray_icon.setToolTip(tooltip)
    
    def set_icon(self, icon):
        """Update tray icon"""
        self.tray_icon.setIcon(icon)
