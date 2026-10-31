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
from PySide6.QtCore import Qt, QTimer, QSize, Signal, QRectF
from PySide6.QtGui import QIcon, QAction, QCloseEvent, QPainter, QPen, QColor

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
        self.is_dragging = False
        self.click_position = None
        
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
        
        # Center window on screen
        self.center_on_screen()
        
        # Setup timers
        self.ui_update_timer = QTimer()
        self.ui_update_timer.timeout.connect(self.update_ui_state)
        self.ui_update_timer.start(50)  # Update every 50ms for smooth animation (20 FPS)
        
        # Connect signals
        self.scheduler.action_triggered.connect(self.execute_scheduled_movement)
    
    def setup_ui(self):
        """Setup the main UI layout - single clickable circle only"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Fixed window size for circular design
        self.setFixedSize(190, 190)
        
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
        """Create single large clickable circle with progress indicator"""
        # Container widget for circle + progress overlay
        container = QWidget()
        container.setFixedSize(180, 180)
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Main clickable button as circle
        self.circle_button = QPushButton()
        self.circle_button.setObjectName("mainCircle")
        self.circle_button.setFixedSize(180, 180)
        # Don't connect clicked signal - we handle it in mouseReleaseEvent
        self.circle_button.setCursor(Qt.PointingHandCursor)
        
        # Make sure the button is clickable
        self.circle_button.setFocusPolicy(Qt.StrongFocus)
        self.circle_button.setMouseTracking(True)
        
        # Layout inside button
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(0)
        
        # Use actual icon file - ONLY the icon, nothing else
        self.mouse_icon_label = QLabel()
        self.mouse_icon_label.setAlignment(Qt.AlignCenter)
        
        # Load the icon file
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            pixmap = QIcon(icon_path).pixmap(90, 90)  # 90x90 pixel icon (smaller)
            self.mouse_icon_label.setPixmap(pixmap)
        else:
            # Fallback to emoji if icon not found
            self.mouse_icon_label.setText("🖱️")
            self.mouse_icon_label.setStyleSheet("font-size: 90pt; background: transparent; color: #0078D4;")
        
        self.mouse_icon_label.setStyleSheet("background: transparent;")
        button_layout.addWidget(self.mouse_icon_label)
        
        self.circle_button.setLayout(button_layout)
        
        # Progress overlay widget (drawn on top)
        self.progress_widget = ProgressCircle()
        self.progress_widget.setFixedSize(180, 180)
        self.progress_widget.setAttribute(Qt.WA_TransparentForMouseEvents)  # Let clicks pass through
        
        # Stack them
        container_layout.addWidget(self.circle_button)
        container.setLayout(container_layout)
        
        # Add progress overlay on top
        self.progress_widget.setParent(container)
        self.progress_widget.move(0, 0)
        self.progress_widget.raise_()  # Bring to front
        
        parent_layout.addWidget(container, 0, Qt.AlignCenter)
    
    def toggle_start_stop(self):
        """Toggle between start and stop on circle click"""
        if self.status == "stopped":
            self.start_movement()
        elif self.status == "running":
            self.stop_movement()
        elif self.status == "paused":
            self.start_movement()
    
    def center_on_screen(self):
        """Center the window on the primary screen"""
        from PySide6.QtGui import QScreen
        screen = QScreen.availableGeometry(self.screen())
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    

    

    

    
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
        # Just update the circle property, no text changes
        self.circle_button.setProperty("status", self.status)
        # Force style refresh
        self.circle_button.setStyle(self.circle_button.style())
    
    def update_ui_state(self):
        """Update UI - change color based on time remaining and update progress"""
        if self.status == "running":
            next_time = self.scheduler.get_next_action_time()
            if next_time:
                interval = self.get_selected_interval()
                remaining = (next_time - datetime.now()).total_seconds()
                
                # Calculate progress (0 to 1, where 1 is complete)
                progress = 1.0 - (remaining / interval)
                progress = max(0.0, min(1.0, progress))  # Clamp to 0-1
                
                self.progress_widget.set_progress(progress)
                self.progress_widget.update()
                
                # Last 3 seconds: RED warning
                if remaining <= 3 and remaining > 0:
                    self.circle_button.setProperty("status", "warning")
                    self.progress_widget.set_color("red")
                else:
                    self.circle_button.setProperty("status", "running")
                    self.progress_widget.set_color("green")
                
                # Force style refresh
                self.circle_button.setStyle(self.circle_button.style())
        else:
            # Reset progress when stopped
            self.progress_widget.set_progress(0)
            self.progress_widget.set_color("blue")
            self.progress_widget.update()
    
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
        """Handle mouse press - record position for click vs drag detection"""
        if event.button() == Qt.LeftButton:
            self.click_position = event.globalPosition().toPoint()
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.is_dragging = False
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            # Check if moved enough to be considered a drag (threshold: 5 pixels)
            if self.click_position:
                distance = (event.globalPosition().toPoint() - self.click_position)
                if abs(distance.x()) > 5 or abs(distance.y()) > 5:
                    self.is_dragging = True
            
            if self.is_dragging:
                self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - if not dragging, it's a click"""
        if event.button() == Qt.LeftButton:
            # Only trigger click if we weren't dragging
            if not self.is_dragging:
                self.toggle_start_stop()
            
            self.click_position = None
            self.is_dragging = False
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


class ProgressCircle(QWidget):
    """Custom widget to draw circular progress indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0.0  # 0.0 to 1.0
        self.color = QColor(33, 150, 243)  # Blue by default
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def set_progress(self, progress):
        """Set progress from 0.0 to 1.0"""
        self.progress = max(0.0, min(1.0, progress))
    
    def set_color(self, color_name):
        """Set the progress arc color"""
        if color_name == "blue":
            self.color = QColor(33, 150, 243)  # Blue
        elif color_name == "green":
            self.color = QColor(76, 175, 80)  # Green
        elif color_name == "red":
            self.color = QColor(244, 67, 54)  # Red
    
    def paintEvent(self, event):
        """Draw the circular progress arc"""
        if self.progress <= 0:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up pen for the arc
        pen = QPen(self.color)
        pen.setWidth(6)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        # Calculate rectangle for arc (inset from edges)
        margin = 8
        rect = QRectF(margin, margin, self.width() - 2*margin, self.height() - 2*margin)
        
        # Draw arc clockwise from top (starts at 90 degrees, goes clockwise)
        # Qt angles: 0° is 3 o'clock, 90° is 12 o'clock
        # Positive span = counter-clockwise, Negative span = clockwise
        start_angle = 90 * 16  # Start at top (12 o'clock)
        span_angle = -int(self.progress * 360 * 16)  # Negative for clockwise
        
        painter.drawArc(rect, start_angle, span_angle)
