"""
Main Window UI for Mouse Pilot
"""

import os
import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QCheckBox, QSpinBox, QGroupBox,
    QFrame, QSystemTrayIcon, QMenu, QDialog, QDialogButtonBox,
    QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from PySide6.QtGui import QIcon, QAction, QCloseEvent

from ui.styles import get_theme_stylesheet
from services.mouse_controller import MouseController
from services.scheduler import Scheduler
from services.keep_awake import KeepAwakeManager
from services.tray_manager import TrayManager
from services.settings_manager import SettingsManager


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SettingsDialog(QDialog):
    """Settings dialog window"""
    
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle("Settings - Mouse Pilot")
        self.setMinimumWidth(500)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Theme settings
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()
        
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_row.addWidget(self.theme_combo)
        theme_row.addStretch()
        theme_layout.addLayout(theme_row)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Movement settings
        movement_group = QGroupBox("Mouse Movement")
        movement_layout = QVBoxLayout()
        
        distance_row = QHBoxLayout()
        distance_row.addWidget(QLabel("Movement Distance (pixels):"))
        self.distance_spin = QSpinBox()
        self.distance_spin.setRange(1, 100)
        self.distance_spin.setValue(5)
        distance_row.addWidget(self.distance_spin)
        distance_row.addStretch()
        movement_layout.addLayout(distance_row)
        
        self.pause_on_activity = QCheckBox("Pause on user activity")
        movement_layout.addWidget(self.pause_on_activity)
        
        movement_group.setLayout(movement_layout)
        layout.addWidget(movement_group)
        
        # System settings
        system_group = QGroupBox("System")
        system_layout = QVBoxLayout()
        
        self.minimize_to_tray = QCheckBox("Minimize to system tray")
        system_layout.addWidget(self.minimize_to_tray)
        
        self.start_with_windows = QCheckBox("Start with Windows (not implemented)")
        self.start_with_windows.setEnabled(False)
        system_layout.addWidget(self.start_with_windows)
        
        system_group.setLayout(system_layout)
        layout.addWidget(system_group)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """Load current settings into dialog"""
        settings = self.settings_manager.get_all_settings()
        
        theme = settings.get("theme", "light")
        self.theme_combo.setCurrentText(theme.capitalize())
        
        self.distance_spin.setValue(settings.get("movement_distance", 5))
        self.pause_on_activity.setChecked(settings.get("pause_on_activity", False))
        self.minimize_to_tray.setChecked(settings.get("minimize_to_tray", True))
        self.start_with_windows.setChecked(settings.get("start_with_windows", False))
    
    def get_settings(self):
        """Get settings from dialog"""
        return {
            "theme": self.theme_combo.currentText().lower(),
            "movement_distance": self.distance_spin.value(),
            "pause_on_activity": self.pause_on_activity.isChecked(),
            "minimize_to_tray": self.minimize_to_tray.isChecked(),
            "start_with_windows": self.start_with_windows.isChecked()
        }


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.drag_position = None
        
        # Initialize services
        self.mouse_controller = MouseController()
        self.scheduler = Scheduler()
        self.keep_awake_manager = KeepAwakeManager()
        
        # State
        self.status = "stopped"  # stopped, running, paused
        self.start_time = None
        
        # Setup UI - Frameless and transparent
        self.setWindowTitle("Mouse Pilot")
        
        # Make window frameless but SHOW in taskbar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Make window background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setup_ui()
        self.setup_tray()
        self.apply_theme()
        self.load_settings()
        
        # Setup timers
        self.ui_update_timer = QTimer()
        self.ui_update_timer.timeout.connect(self.update_ui_state)
        self.ui_update_timer.start(1000)  # Update every second
        
        # Connect signals
        self.scheduler.action_triggered.connect(self.execute_scheduled_movement)
    
    def setup_ui(self):
        """Setup the main UI layout - single clickable circle only"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Fixed window size for circular design
        self.setFixedSize(250, 250)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create the single clickable circle
        self.create_clickable_circle(main_layout)
        
        # Hidden controls for internal state
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["15 seconds", "30 seconds", "60 seconds", "2 minutes", "5 minutes"])
        self.interval_combo.setCurrentText("15 seconds")
        self.interval_combo.setVisible(False)
        
        self.custom_interval_spin = QSpinBox()
        self.custom_interval_spin.setRange(5, 3600)
        self.custom_interval_spin.setValue(10)
        self.custom_interval_spin.setVisible(False)
        
        self.keep_awake_checkbox = QCheckBox()
        self.keep_awake_checkbox.setVisible(False)
        
        central_widget.setLayout(main_layout)
    
    def create_clickable_circle(self, parent_layout):
        """Create single large clickable circle"""
        # Main clickable button as circle
        self.circle_button = QPushButton()
        self.circle_button.setObjectName("mainCircle")
        self.circle_button.setFixedSize(240, 240)
        self.circle_button.clicked.connect(self.toggle_start_stop)
        self.circle_button.setCursor(Qt.PointingHandCursor)
        
        # Make sure the button is clickable
        self.circle_button.setFocusPolicy(Qt.StrongFocus)
        self.circle_button.setMouseTracking(True)
        
        # Layout inside button
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(5)
        
        # Mouse icon
        self.mouse_icon_label = QLabel("🖱️")
        self.mouse_icon_label.setAlignment(Qt.AlignCenter)
        self.mouse_icon_label.setStyleSheet("font-size: 70pt; background: transparent; color: #0078D4;")
        button_layout.addWidget(self.mouse_icon_label)
        
        # Status text
        self.status_label = QLabel("Click to Start")
        self.status_label.setObjectName("circleStatus")
        self.status_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.status_label)
        
        # Timer display
        self.timer_label = QLabel("10s")
        self.timer_label.setObjectName("timerDisplay")
        self.timer_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.timer_label)
        
        # Session duration
        self.session_label = QLabel("00:00:00")
        self.session_label.setObjectName("sessionDisplay")
        self.session_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.session_label)
        
        self.circle_button.setLayout(button_layout)
        parent_layout.addWidget(self.circle_button, 0, Qt.AlignCenter)
    
    def toggle_start_stop(self):
        """Toggle between start and stop on circle click"""
        if self.status == "stopped":
            self.start_movement()
        elif self.status == "running":
            self.stop_movement()
        elif self.status == "paused":
            self.start_movement()
    

    

    

    
    def setup_tray(self):
        """Setup system tray icon"""
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            tray_icon = QIcon(icon_path)
        else:
            tray_icon = self.style().standardIcon(self.style().SP_ComputerIcon)
        
        self.tray_icon = QSystemTrayIcon(tray_icon, self)
        self.tray_icon.setToolTip("Mouse Pilot - Stopped")
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Open Mouse Pilot", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        start_action = QAction("Start", self)
        start_action.triggered.connect(self.start_movement)
        tray_menu.addAction(start_action)
        
        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_movement)
        tray_menu.addAction(pause_action)
        
        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.stop_movement)
        tray_menu.addAction(stop_action)
        
        tray_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_application)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
    
    def apply_theme(self):
        """Apply the current theme"""
        settings = self.settings_manager.get_all_settings()
        theme = settings.get("theme", "light")
        stylesheet = get_theme_stylesheet(theme)
        self.setStyleSheet(stylesheet)
    
    def load_settings(self):
        """Load settings from settings manager"""
        settings = self.settings_manager.get_all_settings()
        
        # Load interval
        interval = settings.get("interval", 60)
        if interval == 15:
            self.interval_combo.setCurrentText("15 seconds")
        elif interval == 30:
            self.interval_combo.setCurrentText("30 seconds")
        elif interval == 60:
            self.interval_combo.setCurrentText("60 seconds")
        elif interval == 120:
            self.interval_combo.setCurrentText("2 minutes")
        elif interval == 300:
            self.interval_combo.setCurrentText("5 minutes")
        else:
            self.interval_combo.setCurrentText("Custom")
            self.custom_interval_spin.setValue(interval)
        
        # Load keep awake state
        self.keep_awake_checkbox.setChecked(settings.get("keep_awake", False))
    
    def save_settings(self):
        """Save current settings"""
        interval = self.get_selected_interval()
        self.settings_manager.set("interval", interval)
        self.settings_manager.set("keep_awake", self.keep_awake_checkbox.isChecked())
        self.settings_manager.save()
    
    def get_selected_interval(self):
        """Get the currently selected interval in seconds"""
        # Always use 10 seconds
        return 10
    
    def on_interval_changed(self, text):
        """Handle interval selection change"""
        self.custom_interval_spin.setEnabled(text == "Custom")
        if self.status == "running":
            # Update scheduler with new interval
            interval = self.get_selected_interval()
            self.scheduler.set_interval(interval)
    
    def start_movement(self):
        """Start mouse movement"""
        if self.status == "paused":
            # Resume from pause
            self.status = "running"
            self.scheduler.resume()
        else:
            # Start fresh
            self.status = "running"
            self.start_time = datetime.now()
            interval = self.get_selected_interval()
            self.scheduler.start(interval)
        
        self.update_buttons()
        self.save_settings()
        self.update_tray_tooltip()
    
    def pause_movement(self):
        """Pause mouse movement"""
        self.status = "paused"
        self.scheduler.pause()
        self.update_buttons()
        self.update_tray_tooltip()
    
    def stop_movement(self):
        """Stop mouse movement"""
        self.status = "stopped"
        self.start_time = None
        self.scheduler.stop()
        self.update_buttons()
        self.save_settings()
        self.update_tray_tooltip()
    
    def execute_scheduled_movement(self):
        """Execute the scheduled mouse movement"""
        if self.status == "running":
            settings = self.settings_manager.get_all_settings()
            distance = settings.get("movement_distance", 5)
            self.mouse_controller.move_cursor(distance)
    
    def toggle_keep_awake(self, state):
        """Toggle keep-awake mode"""
        if state == Qt.Checked:
            self.keep_awake_manager.enable()
        else:
            self.keep_awake_manager.disable()
        self.save_settings()
    
    def update_buttons(self):
        """Update circle appearance based on current status"""
        if self.status == "stopped":
            self.status_label.setText("Click to Start")
            self.circle_button.setProperty("status", "stopped")
        elif self.status == "running":
            self.status_label.setText("Running - Click to Stop")
            self.circle_button.setProperty("status", "running")
        elif self.status == "paused":
            self.status_label.setText("Paused - Click to Resume")
            self.circle_button.setProperty("status", "paused")
        
        # Force style refresh
        self.circle_button.setStyle(self.circle_button.style())
    
    def update_ui_state(self):
        """Update UI labels and status"""
        # Update session duration
        if self.start_time:
            duration = datetime.now() - self.start_time
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            seconds = int(duration.total_seconds() % 60)
            self.session_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.session_label.setText("00:00:00")
        
        # Update timer countdown
        if self.status == "running":
            next_time = self.scheduler.get_next_action_time()
            if next_time:
                remaining = (next_time - datetime.now()).total_seconds()
                if remaining > 0:
                    self.timer_label.setText(f"{int(remaining)}s")
                else:
                    self.timer_label.setText("Now!")
            else:
                interval = self.get_selected_interval()
                self.timer_label.setText(f"{interval}s")
        else:
            interval = self.get_selected_interval()
            self.timer_label.setText(f"{interval}s")
    
    def update_tray_tooltip(self):
        """Update system tray tooltip"""
        self.tray_icon.setToolTip(f"Mouse Pilot - {self.status.capitalize()}")
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.settings_manager, self)
        if dialog.exec() == QDialog.Accepted:
            settings = dialog.get_settings()
            for key, value in settings.items():
                self.settings_manager.set(key, value)
            self.settings_manager.save()
            self.apply_theme()
    
    def show_window(self):
        """Show and activate the main window"""
        self.show()
        self.activateWindow()
        self.raise_()
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event"""
        settings = self.settings_manager.get_all_settings()
        minimize_to_tray = settings.get("minimize_to_tray", True)
        
        if minimize_to_tray:
            event.ignore()
            self.hide()
        else:
            self.exit_application()
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def exit_application(self):
        """Clean exit of the application"""
        # Stop all operations
        self.scheduler.stop()
        self.keep_awake_manager.disable()
        
        # Hide tray icon
        self.tray_icon.hide()
        
        # Save settings
        self.save_settings()
        
        # Quit application
        from PySide6.QtWidgets import QApplication
        QApplication.quit()
