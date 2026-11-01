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
from PySide6.QtCore import Qt, QTimer, QSize, Signal, QRectF, QPoint
from PySide6.QtGui import QIcon, QAction, QCloseEvent, QPainter, QPen, QColor, QCursor

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


# Icon file names
APP_ICON = "mouse_pilot.ico"  # Main app icon
WIDGET_ICON = "widget_icon.png"  # Icon shown in center of circle
TRAY_ICON = "tray_icon.png"  # System tray icon


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
        self.drag_offset = None
        self.is_dragging = False
        self.click_position = None
        self.drag_start_pos = None
        
        # Initialize services
        self.mouse_controller = MouseController()
        self.scheduler = Scheduler()
        self.keep_awake_manager = KeepAwakeManager()
        
        # State
        self.status = "stopped"  # stopped, running, paused
        self.start_time = None
        
        # Setup UI - Frameless and transparent
        self.setWindowTitle("Mouse Pilot")
        
        # Make window frameless - remove WindowStaysOnTopHint to allow taskbar minimize
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        
        # Make window background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Enable mouse tracking for cursor changes
        self.setMouseTracking(True)
        
        # Track if window should stay on top (user preference)
        self.stay_on_top = False
        
        icon_path = get_resource_path(os.path.join("assets", APP_ICON))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setup_ui()
        self.setup_tray()
        self.apply_theme()
        self.load_settings()
        
        # Load and restore last position, or center if first launch
        self.restore_position()
        
        # Setup timers
        self.ui_update_timer = QTimer()
        self.ui_update_timer.timeout.connect(self.update_ui_state)
        self.ui_update_timer.start(50)  # Update every 50ms for smooth animation (20 FPS)
        
        # Connect signals
        self.scheduler.action_triggered.connect(self.execute_scheduled_movement)
    
    def setup_ui(self):
        """Setup the main UI layout - single clickable circle only"""
        central_widget = QWidget()
        central_widget.setAttribute(Qt.WA_TransparentForMouseEvents)  # Let window handle mouse events
        self.setCentralWidget(central_widget)
        
        # Fixed window size for circular design (larger for drag area)
        self.setFixedSize(220, 220)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 20px margin = drag area
        
        # Create the single clickable circle
        self.create_clickable_circle(main_layout)
        
        # Create close button (hidden by default, shows on hover anywhere on app)
        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(24, 24)
        self.close_button.setParent(self)
        self.close_button.move(self.width() - 30, 6)  # Top-right corner
        self.close_button.clicked.connect(self.exit_application)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.hide()  # Hidden by default
        
        # Timer to auto-hide close button after 5 seconds
        self.close_button_timer = QTimer()
        self.close_button_timer.setSingleShot(True)
        self.close_button_timer.timeout.connect(self.hide_close_button)
        
        # Track if click is inside the circle (for start/stop)
        self.circle_radius = 90  # Radius of the clickable circle area
        
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
        container.setAttribute(Qt.WA_TransparentForMouseEvents)  # Let window handle mouse events
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Main clickable button as circle
        self.circle_button = QPushButton()
        self.circle_button.setObjectName("mainCircle")
        self.circle_button.setFixedSize(180, 180)
        # Don't connect clicked - we handle it in mousePressEvent
        self.circle_button.setCursor(Qt.PointingHandCursor)
        
        # Disable button's mouse event handling to let window handle it
        self.circle_button.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        # Make sure the button is clickable
        self.circle_button.setFocusPolicy(Qt.StrongFocus)
        self.circle_button.setMouseTracking(False)
        
        # Layout inside button
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(0)
        
        # Use actual icon file - ONLY the icon, nothing else
        self.mouse_icon_label = QLabel()
        self.mouse_icon_label.setAlignment(Qt.AlignCenter)
        self.mouse_icon_label.setAttribute(Qt.WA_TransparentForMouseEvents)  # Let window handle mouse events
        
        # Load the widget icon (center of circle)
        widget_icon_path = get_resource_path(os.path.join("assets", WIDGET_ICON))
        if os.path.exists(widget_icon_path):
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap(widget_icon_path).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.mouse_icon_label.setPixmap(pixmap)
        else:
            # Fallback to app icon if widget icon not found
            icon_path = get_resource_path(os.path.join("assets", APP_ICON))
            if os.path.exists(icon_path):
                pixmap = QIcon(icon_path).pixmap(90, 90)
                self.mouse_icon_label.setPixmap(pixmap)
            else:
                # Fallback to emoji if no icon found
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
        
        # Store container for position checks
        self.circle_container = container
        
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
    
    def restore_position(self):
        """Restore widget position from settings or center on first launch"""
        settings = self.settings_manager.get_all_settings()
        saved_x = settings.get("window_x", None)
        saved_y = settings.get("window_y", None)
        
        if saved_x is not None and saved_y is not None:
            # Validate that the position is on a visible screen
            from PySide6.QtGui import QGuiApplication
            target_pos = QPoint(int(saved_x), int(saved_y))
            
            # Check if position is visible on any screen
            is_visible = False
            for screen in QGuiApplication.screens():
                if screen.geometry().contains(target_pos):
                    is_visible = True
                    break
            
            if is_visible:
                self.move(int(saved_x), int(saved_y))
            else:
                # Saved position is invalid (monitor disconnected), center it
                self.center_on_screen()
        else:
            # First launch, center the widget
            self.center_on_screen()
    
    def save_position(self):
        """Save current widget position to settings"""
        pos = self.pos()
        self.settings_manager.set("window_x", pos.x())
        self.settings_manager.set("window_y", pos.y())
        self.settings_manager.save()
    

    

    

    
    def setup_tray(self):
        """Setup system tray icon"""
        # Use dedicated tray icon
        tray_icon_path = get_resource_path(os.path.join("assets", TRAY_ICON))
        if os.path.exists(tray_icon_path):
            tray_icon = QIcon(tray_icon_path)
        else:
            # Fallback to app icon
            icon_path = get_resource_path(os.path.join("assets", APP_ICON))
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
                
                # Calculate progress as remaining time (1 = full, 0 = empty)
                # Circle starts FULL and drains to empty
                progress = remaining / interval
                progress = max(0.0, min(1.0, progress))  # Clamp to 0-1
                
                self.progress_widget.set_progress(progress)
                
                # Change to RED when 75% complete (25% remaining)
                if progress <= 0.25:
                    self.progress_widget.set_color("red")
                else:
                    self.progress_widget.set_color("green")
                
                self.progress_widget.update()
                
                self.circle_button.setProperty("status", "running")
                # Force style refresh
                self.circle_button.setStyle(self.circle_button.style())
        else:
            # Show full blue circle when stopped/idle
            self.progress_widget.set_progress(1.0)  # Full circle
            self.progress_widget.set_color("blue")
            self.progress_widget.update()
            
            self.circle_button.setProperty("status", "stopped")
            self.circle_button.setStyle(self.circle_button.style())
    
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
        self.showNormal()  # Restore from minimized state
        self.activateWindow()
        self.raise_()
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
    
    def changeEvent(self, event):
        """Handle window state changes (minimize/restore)"""
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.WindowStateChange:
            # Window state changed (minimized, maximized, etc.)
            pass
        super().changeEvent(event)
    
    def leaveEvent(self, event):
        """When mouse leaves, let the timer handle hiding the close button"""
        # Don't hide immediately - let the 5-second timer handle it
        super().leaveEvent(event)
    
    def enterEvent(self, event):
        """Show close button when mouse enters the window"""
        self.show_close_button()
        super().enterEvent(event)
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event"""
        settings = self.settings_manager.get_all_settings()
        minimize_to_tray = settings.get("minimize_to_tray", True)
        
        if minimize_to_tray:
            event.ignore()
            self.hide()
        else:
            self.exit_application()
    
    def is_near_outer_edge(self, pos):
        """Check if position is near the outer edge (for showing close button)"""
        # Get window center
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        dx = pos.x() - center_x
        dy = pos.y() - center_y
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Near outer edge = between 70 and 110 pixels from center
        return distance >= 70 and distance <= 110
    
    def show_close_button(self):
        """Show close button and start 3-second timer to hide it"""
        self.close_button.show()
        self.close_button_timer.start(3000)  # Hide after 3 seconds
    
    def hide_close_button(self):
        """Hide the close button"""
        self.close_button.hide()
    
    def is_on_center_button(self, pos):
        """Check if position is inside/on the inner red circle (for start/stop toggle)"""
        # Get window center
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        dx = pos.x() - center_x
        dy = pos.y() - center_y
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Inner red circle area = within 60px radius 
        # This covers the red circle shown in the widget icon (which is 90x90 = 45px radius + border)
        return distance <= 60
    
    def mousePressEvent(self, event):
        """Handle mouse press - drag from anywhere except center button"""
        if event.button() == Qt.LeftButton:
            local_pos = event.position().toPoint()
            
            # Store the offset from click position to window top-left
            self.drag_offset = event.globalPosition().toPoint() - self.pos()
            
            # Check if clicking on center button
            if self.is_on_center_button(local_pos):
                # On button - toggle start/stop
                self.toggle_start_stop()
                self.is_dragging = False
            else:
                # Not on button - start dragging
                self.is_dragging = True
                self.setCursor(QCursor(Qt.ClosedHandCursor))
            
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging and cursor changes"""
        local_pos = event.position().toPoint()
        
        if self.is_dragging and hasattr(self, 'drag_offset') and self.drag_offset is not None:
            # Dragging - move the widget
            new_pos = event.globalPosition().toPoint() - self.drag_offset
            self.move(int(new_pos.x()), int(new_pos.y()))
        else:
            # Not dragging - update cursor based on position
            if not self.is_on_center_button(local_pos):
                self.setCursor(QCursor(Qt.OpenHandCursor))
            else:
                self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Show close button when mouse is anywhere on the app
        self.show_close_button()
        
        event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - save position after drag"""
        if event.button() == Qt.LeftButton:
            if self.is_dragging:
                # Finished dragging - save new position
                self.save_position()
            
            self.is_dragging = False
            self.drag_offset = None
            
            # Reset cursor
            local_pos = event.position().toPoint()
            if not self.is_on_center_button(local_pos):
                self.setCursor(QCursor(Qt.OpenHandCursor))
            else:
                self.setCursor(QCursor(Qt.PointingHandCursor))
            
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
        """Draw the circular progress arc - countdown style (full to empty, clockwise)"""
        if self.progress <= 0:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up pen for the arc - thick line to match the idle circle border
        pen = QPen(self.color)
        pen.setWidth(5)  # Match the 5px border width of idle circle
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        # Calculate rectangle for arc - draw at the outer edge to match blue border
        # The blue border is at the edge of the 180x180 button
        # We need margin of half the pen width (2.5) to align the arc center with the border
        margin = 2.5
        rect = QRectF(margin, margin, self.width() - 2*margin, self.height() - 2*margin)
        
        # Draw arc CLOCKWISE - starts at top and drains clockwise
        start_angle = 90 * 16  # Start at top (12 o'clock)
        span_angle = int(self.progress * 360 * 16)
        
        painter.drawArc(rect, start_angle, span_angle)
