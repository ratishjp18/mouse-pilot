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
        
        # Initialize services
        self.mouse_controller = MouseController()
        self.scheduler = Scheduler()
        self.keep_awake_manager = KeepAwakeManager()
        
        # State
        self.status = "stopped"  # stopped, running, paused
        self.start_time = None
        
        # Setup UI
        self.setWindowTitle("Mouse Pilot")
        self.setMinimumSize(600, 700)
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
        """Setup the main UI layout with circular design"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Fixed window size for circular design
        self.setFixedSize(700, 700)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top-right controls
        top_row = QHBoxLayout()
        top_row.addStretch()
        
        # Minimize button
        minimize_btn = QPushButton("−")
        minimize_btn.setObjectName("circleButton")
        minimize_btn.setFixedSize(40, 40)
        minimize_btn.clicked.connect(self.hide)
        minimize_btn.setToolTip("Minimize to tray")
        top_row.addWidget(minimize_btn)
        
        # Settings button
        settings_btn = QPushButton("⚙")
        settings_btn.setObjectName("circleButton")
        settings_btn.setFixedSize(40, 40)
        settings_btn.clicked.connect(self.show_settings)
        settings_btn.setToolTip("Settings")
        top_row.addWidget(settings_btn)
        
        main_layout.addLayout(top_row)
        
        # Main circular area
        center_widget = QWidget()
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Create circular mouse display
        self.create_circular_mouse_display(center_layout)
        
        center_widget.setLayout(center_layout)
        main_layout.addWidget(center_widget, 1)
        
        # Bottom controls
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(30)
        bottom_layout.setAlignment(Qt.AlignCenter)
        
        # Interval selector (left side)
        interval_widget = self.create_interval_selector()
        bottom_layout.addWidget(interval_widget)
        
        # Control buttons (center)
        controls_widget = self.create_bottom_controls()
        bottom_layout.addWidget(controls_widget)
        
        # Keep awake toggle (right side)
        keep_awake_widget = self.create_keep_awake_toggle()
        bottom_layout.addWidget(keep_awake_widget)
        
        main_layout.addLayout(bottom_layout)
        
        central_widget.setLayout(main_layout)
    
    def create_circular_mouse_display(self, parent_layout):
        """Create the central circular mouse icon with progress ring"""
        # Container for the circular display
        circle_container = QWidget()
        circle_container.setFixedSize(400, 400)
        circle_layout = QVBoxLayout()
        circle_layout.setAlignment(Qt.AlignCenter)
        circle_layout.setContentsMargins(0, 0, 0, 0)
        
        # Mouse icon (using emoji for now - can be replaced with image)
        self.mouse_icon_label = QLabel("🖱️")
        self.mouse_icon_label.setObjectName("mouseIcon")
        self.mouse_icon_label.setAlignment(Qt.AlignCenter)
        self.mouse_icon_label.setStyleSheet("font-size: 120pt; background: transparent;")
        circle_layout.addWidget(self.mouse_icon_label)
        
        # Status text below icon
        self.status_label = QLabel("Stopped")
        self.status_label.setObjectName("circleStatus")
        self.status_label.setAlignment(Qt.AlignCenter)
        circle_layout.addWidget(self.status_label)
        
        # Timer display
        self.timer_label = QLabel("--:--")
        self.timer_label.setObjectName("timerDisplay")
        self.timer_label.setAlignment(Qt.AlignCenter)
        circle_layout.addWidget(self.timer_label)
        
        # Session duration
        self.session_label = QLabel("00:00:00")
        self.session_label.setObjectName("sessionDisplay")
        self.session_label.setAlignment(Qt.AlignCenter)
        circle_layout.addWidget(self.session_label)
        
        circle_container.setLayout(circle_layout)
        circle_container.setObjectName("circleContainer")
        parent_layout.addWidget(circle_container)
    
    def create_bottom_controls(self):
        """Create control buttons at bottom center"""
        controls_widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Start button (circular)
        self.start_button = QPushButton("▶")
        self.start_button.setObjectName("circleControlButton")
        self.start_button.setFixedSize(70, 70)
        self.start_button.clicked.connect(self.start_movement)
        self.start_button.setToolTip("Start")
        layout.addWidget(self.start_button)
        
        # Pause button (circular)
        self.pause_button = QPushButton("⏸")
        self.pause_button.setObjectName("circleControlButton")
        self.pause_button.setFixedSize(70, 70)
        self.pause_button.clicked.connect(self.pause_movement)
        self.pause_button.setEnabled(False)
        self.pause_button.setToolTip("Pause")
        layout.addWidget(self.pause_button)
        
        # Stop button (circular)
        self.stop_button = QPushButton("⏹")
        self.stop_button.setObjectName("circleControlButtonStop")
        self.stop_button.setFixedSize(70, 70)
        self.stop_button.clicked.connect(self.stop_movement)
        self.stop_button.setEnabled(False)
        self.stop_button.setToolTip("Stop")
        layout.addWidget(self.stop_button)
        
        controls_widget.setLayout(layout)
        return controls_widget
    
    def create_interval_selector(self):
        """Create interval selector on the left side"""
        interval_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Circular interval button
        self.interval_button = QPushButton("⏱\n60s")
        self.interval_button.setObjectName("sideCircleButton")
        self.interval_button.setFixedSize(90, 90)
        self.interval_button.clicked.connect(self.show_interval_menu)
        self.interval_button.setToolTip("Change interval")
        layout.addWidget(self.interval_button)
        
        interval_label = QLabel("Interval")
        interval_label.setAlignment(Qt.AlignCenter)
        interval_label.setObjectName("subtitle")
        layout.addWidget(interval_label)
        
        # Hidden combo for interval storage
        self.interval_combo = QComboBox()
        self.interval_combo.addItems([
            "15 seconds",
            "30 seconds",
            "60 seconds",
            "2 minutes",
            "5 minutes",
            "Custom"
        ])
        self.interval_combo.setCurrentText("60 seconds")
        self.interval_combo.currentTextChanged.connect(self.on_interval_changed)
        self.interval_combo.setVisible(False)
        
        # Hidden custom spin
        self.custom_interval_spin = QSpinBox()
        self.custom_interval_spin.setRange(5, 3600)
        self.custom_interval_spin.setValue(60)
        self.custom_interval_spin.setVisible(False)
        
        interval_widget.setLayout(layout)
        return interval_widget
    
    def show_interval_menu(self):
        """Show interval selection menu"""
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        
        intervals = [
            ("15 seconds", "15s"),
            ("30 seconds", "30s"),
            ("60 seconds", "60s"),
            ("2 minutes", "2m"),
            ("5 minutes", "5m"),
        ]
        
        for interval_text, display_text in intervals:
            action = menu.addAction(interval_text)
            action.triggered.connect(lambda checked=False, it=interval_text, dt=display_text: self.set_interval(it, dt))
        
        menu.exec(self.interval_button.mapToGlobal(self.interval_button.rect().bottomLeft()))
    
    def create_keep_awake_toggle(self):
        """Create keep-awake toggle on the right side"""
        keep_awake_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Circular keep-awake button
        self.keep_awake_button = QPushButton("☕")
        self.keep_awake_button.setObjectName("sideCircleButton")
        self.keep_awake_button.setFixedSize(90, 90)
        self.keep_awake_button.setCheckable(True)
        self.keep_awake_button.clicked.connect(self.toggle_keep_awake_button)
        self.keep_awake_button.setToolTip("Keep system awake")
        layout.addWidget(self.keep_awake_button)
        
        keep_awake_label = QLabel("Keep Awake")
        keep_awake_label.setAlignment(Qt.AlignCenter)
        keep_awake_label.setObjectName("subtitle")
        layout.addWidget(keep_awake_label)
        
        # Hidden checkbox for state
        self.keep_awake_checkbox = QCheckBox()
        self.keep_awake_checkbox.setVisible(False)
        
        keep_awake_widget.setLayout(layout)
        return keep_awake_widget
    
    def toggle_keep_awake_button(self):
        """Toggle keep-awake from button"""
        is_checked = self.keep_awake_button.isChecked()
        self.keep_awake_checkbox.setChecked(is_checked)
        self.toggle_keep_awake(Qt.Checked if is_checked else Qt.Unchecked)
        
        # Update button style
        if is_checked:
            self.keep_awake_button.setStyleSheet("background-color: #107C10;")
        else:
            self.keep_awake_button.setStyleSheet("")
    
    def set_interval(self, interval_text, display_text):
        """Set interval from menu selection"""
        self.interval_combo.setCurrentText(interval_text)
        self.interval_button.setText(f"⏱\n{display_text}")
    
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
        text = self.interval_combo.currentText()
        if text == "15 seconds":
            return 15
        elif text == "30 seconds":
            return 30
        elif text == "60 seconds":
            return 60
        elif text == "2 minutes":
            return 120
        elif text == "5 minutes":
            return 300
        else:  # Custom
            return self.custom_interval_spin.value()
    
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
        """Update button states based on current status"""
        if self.status == "stopped":
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
        elif self.status == "running":
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        elif self.status == "paused":
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(True)
    
    def update_ui_state(self):
        """Update UI labels and status"""
        # Update status label
        self.status_label.setText(self.status.capitalize())
        self.status_label.setProperty("status", self.status)
        self.status_label.setStyle(self.status_label.style())
        
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
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
                else:
                    self.timer_label.setText("00:00")
            else:
                self.timer_label.setText("--:--")
        else:
            self.timer_label.setText("--:--")
    
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
