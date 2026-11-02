# 🖱️ Mouse Pilot

**A lightweight, modern Windows desktop widget for keeping your PC awake with automatic cursor movement.**

Mouse Pilot is a sleek, floating circular widget that prevents your system from sleeping or locking by simulating mouse activity. Built with Python and PySide6, it features a transparent, draggable design that stays out of your way while keeping you productive.

---

## ✨ Features

### 🎯 Core Functionality
- **Automatic Mouse Movement**: Moves cursor every 10 seconds using Windows SendInput API
- **Real User Input Simulation**: Uses the same technique as professional keep-awake apps
- **Smart Movement**: Cursor moves slightly and returns to original position
- **Works with Energy Saver**: Overrides Windows power settings to keep your PC awake

### � Modern Circular Widget
- **Floating Design**: Transparent, frameless circular widget
- **Visual Progress**: Animated circular countdown showing time until next movement
- **Color Indicators**:
  - 🔵 **Blue** - Idle/Stopped
  - 🟢 **Green** - Running (0-75% progress)
  - 🔴 **Red** - Running (75-100% progress, almost time to move)
- **Draggable**: Drag from the outer ring to reposition anywhere on screen
- **Position Memory**: Remembers where you left it between sessions

### 🖱️ Easy Controls
- **Click to Start/Stop**: Click the inner circle to toggle
- **Close Button**: Hover anywhere on widget to reveal close button (auto-hides after 3 seconds)
- **System Tray**: Minimize to tray with full control menu
- **Taskbar Support**: Can be minimized to taskbar

### ⚡ Keep-Awake Technology
- **Windows SendInput API**: Simulates real mouse input that Windows recognizes
- **SetThreadExecutionState**: Prevents system sleep and display timeout
- **Automatic Activation**: Keep-awake enables when you start, disables when you stop

### 🔒 Privacy & Security
- **100% Local**: No cloud services, no login, no telemetry
- **No Keylogging**: Never captures keystrokes or private information
- **Open Source**: Full transparency - review all code
- **No Admin Required**: Runs with standard user permissions

---

## � Installation

### Quick Install

1. Download `MousePilot.exe` from the `dist` folder
2. Run the executable - that's it!

### Create Desktop/Start Menu Shortcuts

After building, shortcuts are automatically created for:
- **Desktop**: Quick access from your desktop
- **Start Menu**: Search "Mouse Pilot" in Start

### Build from Source

1. **Clone and setup**:
   ```powershell
   git clone <repository-url>
   cd mouse-pilot
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Build executable**:
   ```powershell
   .\build.ps1
   ```

3. **Find your executable**: `.\dist\MousePilot.exe`

---

## 📖 Usage

### Quick Start

1. **Launch Mouse Pilot** - A circular widget appears on screen
2. **Click the inner circle** (with the mouse icon) to **start**
3. **Watch the green progress** circle drain clockwise
4. **Circle turns red** when 75% complete (warning)
5. **Click again** to **stop**

### Widget Controls

| Area | Action |
|------|--------|
| **Inner Circle** (red ring area) | Click to Start/Stop |
| **Outer Ring** | Drag to move widget |
| **Close Button** (top-right) | Appears on hover, click to exit |

### System Tray

Right-click the tray icon for:
- Open Mouse Pilot
- Start / Pause / Stop
- Exit

### Visual States

| Color | Meaning |
|-------|---------|
| 🔵 Blue Circle | Idle - Click to start |
| 🟢 Green Progress | Running - Counting down |
| 🔴 Red Progress | Almost time to move mouse |

---

## 🛠️ Technical Details

### How It Works

1. **Mouse Movement**: Uses Windows `SendInput` API to move the cursor
   - More reliable than PyAutoGUI for preventing sleep
   - Windows recognizes it as real user input

2. **Keep-Awake**: Uses `SetThreadExecutionState` API
   - `ES_SYSTEM_REQUIRED` - Prevents sleep
   - `ES_DISPLAY_REQUIRED` - Keeps screen on

3. **Timing**: 10-second interval with visual countdown

### Project Structure

```
mouse-pilot/
├── main.py                  # Application entry point
├── build.ps1               # Build script
├── requirements.txt        # Dependencies
│
├── assets/
│   ├── mouse_pilot.ico    # App icon
│   ├── widget_icon.png    # Center widget icon
│   └── tray_icon.png      # System tray icon
│
├── ui/
│   ├── main_window.py     # Main widget window
│   └── styles.py          # Light/Dark theme styles
│
├── services/
│   ├── mouse_controller.py # Windows SendInput mouse control
│   ├── scheduler.py        # Timer scheduling
│   ├── keep_awake.py       # Windows power management
│   ├── settings_manager.py # Settings persistence
│   └── tray_manager.py     # System tray
│
└── dist/
    └── MousePilot.exe     # Built executable
```

---

## 🐛 Troubleshooting

### Mouse movement not keeping PC awake
- Make sure the **green circle is animating** (not blue)
- The app uses Windows SendInput API which should work even with Energy Saver on

### Widget not dragging
- Click and drag from the **outer ring area**, not the inner circle
- The inner circle is for start/stop

### Can't find close button
- **Hover your mouse** anywhere on the widget
- Close button appears in top-right corner for 3 seconds

### Settings not saving
- Settings are stored in `%APPDATA%\MousePilot\settings.json`
- Widget position is saved automatically when you drag

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚖️ Disclaimer

Mouse Pilot is intended for legitimate purposes only:
- Keeping system active during long-running tasks
- Preventing sleep during presentations or monitoring
- Personal productivity use

Users are responsible for ensuring their use complies with applicable policies and agreements.

---

**Made with ❤️ for Windows users who need to stay awake**
