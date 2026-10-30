# 🖱️ Mouse Pilot

**A lightweight, professional Windows desktop utility for scheduled cursor movement and system keep-awake management.**

Mouse Pilot is a clean, modern Windows application that allows you to schedule automatic cursor movements and optionally prevent system sleep during legitimate long-running tasks. Built with Python and PySide6, it features a native Windows 11-style interface with both light and dark themes.

---

## ✨ Features

### 🎯 Core Functionality
- **Scheduled Mouse Movement**: Automatically move cursor at configurable intervals (15s to 5 minutes, or custom)
- **Precise Control**: Start, pause, and stop operations with large, clear buttons
- **Smart Movement**: Cursor returns to original position; respects screen boundaries
- **Multi-Monitor Support**: Works seamlessly across multiple displays

### 🖥️ Native Windows Experience
- **Taskbar Integration**: Appears as a proper Windows application with custom icon
- **System Tray Support**: Minimize to tray with full control menu
- **Pin to Taskbar**: Pin the executable for quick access
- **No Console Window**: Launches cleanly as a windowed application

### ⚡ Keep-Awake Mode
- **System Sleep Prevention**: Optionally prevent Windows from sleeping during work
- **Policy Compliant**: Uses documented Windows power management APIs
- **Easily Reversible**: Restore normal sleep behavior with one click

### 🎨 Modern Interface
- **Windows 11 Design**: Clean, rounded cards with subtle shadows
- **Dark & Light Themes**: Switch between themes in settings
- **Real-Time Status**: Live countdown to next action
- **Session Tracking**: View current session duration

### ⚙️ Customizable Settings
- **Movement Distance**: Configure pixel movement (1-100 pixels)
- **Custom Intervals**: Set any interval from 5 seconds to 1 hour
- **Minimize Behavior**: Choose whether to minimize to tray
- **Pause on Activity**: Optional detection of user interaction

### 🔒 Privacy & Security
- **100% Local**: No cloud services, no login, no telemetry
- **No Keylogging**: Never captures keystrokes or private information
- **Open Source**: Full transparency - review all code
- **No Admin Required**: Runs with standard user permissions

---

## 📸 Screenshots

*Screenshot placeholders - add actual screenshots here:*

### Main Dashboard
![Main Dashboard - Light Theme](docs/screenshot_light.png)

### Main Dashboard - Dark Theme
![Main Dashboard - Dark Theme](docs/screenshot_dark.png)

### Settings Panel
![Settings Dialog](docs/screenshot_settings.png)

### System Tray
![System Tray Integration](docs/screenshot_tray.png)

---

## 🛠️ Technology Stack

- **Python 3.11+**: Modern Python with type hints
- **PySide6**: Qt6 bindings for native GUI
- **PyAutoGUI**: Cross-platform cursor control
- **Windows ctypes**: Native Windows power management APIs
- **PyInstaller**: Single-file executable packaging
- **pytest**: Unit testing framework

---

## 📦 Installation

### Option 1: Download Executable (Recommended)

1. Download `MousePilot.exe` from the [Releases](../../releases) page
2. Move the executable to a permanent location (e.g., `C:\Program Files\MousePilot\`)
3. Right-click `MousePilot.exe` → **Pin to taskbar** (optional)
4. Double-click to run

### Option 2: Run from Source

1. **Clone the repository**:
   ```powershell
   git clone https://github.com/yourusername/mouse-pilot.git
   cd mouse-pilot
   ```

2. **Create virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```powershell
   python main.py
   ```

---

## 🏗️ Building from Source

### Prerequisites

- Python 3.11 or higher
- Windows 10/11
- PowerShell
- Git (optional)

### Build Steps

1. **Clone and setup**:
   ```powershell
   git clone https://github.com/yourusername/mouse-pilot.git
   cd mouse-pilot
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Create the icon** (if PIL is installed):
   ```powershell
   pip install Pillow
   python -c "from create_icon import create_icon; create_icon()"
   ```

3. **Build executable**:
   ```powershell
   .\build.ps1
   ```

4. **Find your executable**:
   - Output: `.\dist\MousePilot.exe`
   - Size: ~40-60 MB (single file, no installation needed)

### Build Script Details

The `build.ps1` script:
- Activates the virtual environment
- Cleans previous builds
- Runs PyInstaller with optimal settings:
  - `--onefile`: Single executable file
  - `--windowed`: No console window
  - `--icon`: Embeds custom icon
  - `--add-data`: Includes assets
- Reports build status and provides pinning instructions

---

## 📖 Usage Guide

### Quick Start

1. **Launch Mouse Pilot**
2. **Select an interval** from the dropdown (default: 60 seconds)
3. **Click Start** to begin scheduled movements
4. **Monitor status** through the main window or system tray

### Controls

| Button | Action |
|--------|--------|
| **▶️ Start** | Begin scheduled cursor movements |
| **⏸️ Pause** | Temporarily pause (resume with Start) |
| **⏹️ Stop** | Stop completely and reset timer |

### Settings

Access via **⚙️ Settings** button:

- **Theme**: Switch between Light and Dark mode
- **Movement Distance**: Adjust pixel movement (1-100)
- **Pause on Activity**: Pause when user moves mouse (experimental)
- **Minimize to Tray**: Hide to system tray when closing window
- **Start with Windows**: Launch automatically (not yet implemented)

### System Tray

Right-click the tray icon for quick actions:
- Open Mouse Pilot
- Start / Pause / Stop
- Exit

### Intervals

Pre-configured options:
- 15 seconds
- 30 seconds
- 60 seconds (1 minute)
- 2 minutes
- 5 minutes
- Custom (5 seconds to 1 hour)

---

## 🧪 Development

### Project Structure

```
mouse-pilot/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── build.ps1               # Build script for executable
├── README.md               # This file
├── .gitignore              # Git ignore rules
│
├── assets/
│   └── icon.ico            # Application icon
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Main window and dialogs
│   └── styles.py           # Theme stylesheets
│
├── services/
│   ├── __init__.py
│   ├── mouse_controller.py # PyAutoGUI wrapper
│   ├── scheduler.py        # QTimer-based scheduling
│   ├── keep_awake.py       # Windows power management
│   ├── settings_manager.py # JSON settings persistence
│   └── tray_manager.py     # System tray management
│
└── tests/
    ├── __init__.py
    ├── test_mouse_controller.py
    ├── test_scheduler.py
    └── test_settings.py
```

### Running Tests

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=ui

# Run specific test file
pytest tests/test_scheduler.py
```

### Code Style

This project follows:
- PEP 8 style guidelines
- Type hints where appropriate
- Docstrings for classes and public methods
- Clear, descriptive variable names

### Adding Features

1. Create feature branch: `git checkout -b feature/my-feature`
2. Implement changes with tests
3. Run test suite: `pytest`
4. Update documentation
5. Submit pull request

---

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.11+ is installed: `python --version`
- Check all dependencies are installed: `pip install -r requirements.txt`
- Try running with: `python main.py` to see error messages

### Icon not showing
- Ensure `assets/icon.ico` exists
- Rebuild with: `.\build.ps1`
- For source runs, icon is loaded from assets directory

### Mouse movement not working
- Check PyAutoGUI is installed: `pip show pyautogui`
- Ensure you clicked "Start" button
- Move cursor away from screen corners (failsafe feature)
- Check selected interval is reasonable

### Keep-Awake not working
- Only supported on Windows
- Requires proper Windows power permissions
- Some enterprise policies may override

### High CPU usage
- Check interval isn't set too low (< 5 seconds)
- Ensure only one instance is running
- Close and restart the application

### Settings not saving
- Check write permissions in `%APPDATA%\MousePilot`
- Settings file: `%APPDATA%\MousePilot\settings.json`
- Delete settings file to reset to defaults

### Build fails
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check PyInstaller version: `pip show pyinstaller`
- Try clean build: delete `build/`, `dist/`, `*.spec` files

---

## 🗺️ Roadmap

### Planned Features
- [ ] Start with Windows support via registry/startup folder
- [ ] Detection of user activity for auto-pause
- [ ] Configurable movement patterns (circle, figure-8, etc.)
- [ ] Operating hours/schedule restrictions
- [ ] Activity logging (optional)
- [ ] Multi-language support
- [ ] Portable mode (settings in app directory)
- [ ] Update checker

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚖️ Disclaimer

Mouse Pilot is intended for legitimate purposes only:
- Keeping system active during long-running tasks
- Preventing sleep during presentations or monitoring
- Personal productivity use

**Do not use this tool to**:
- Bypass employer monitoring or activity tracking
- Falsify work hours or activity reports
- Circumvent security policies
- Violate terms of service or employment agreements

Users are solely responsible for ensuring their use complies with applicable laws, policies, and agreements.

---

## 🙏 Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython/)
- Mouse control via [PyAutoGUI](https://pyautogui.readthedocs.io/)
- Icons inspired by Windows 11 Fluent Design
- Packaged with [PyInstaller](https://pyinstaller.org/)

---

## 📞 Support

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Email**: support@example.com (update with actual contact)

---

**Made with ❤️ for Windows power users**
