# Mouse Pilot - Usage Guide

## Quick Start

### First Launch

1. **Launch the application**
   - Double-click `MousePilot.exe` (if using built version)
   - Or run `python main.py` (if using source)

2. **Configure your interval**
   - Choose from preset intervals: 15s, 30s, 1min, 2min, 5min
   - Or select "Custom" for any interval (5 seconds to 1 hour)

3. **Start mouse movement**
   - Click the **▶️ Start** button
   - Watch the countdown to the next movement
   - Your cursor will move slightly every interval

4. **Monitor status**
   - Main window shows live status
   - System tray icon displays current state
   - Session duration shows how long you've been running

---

## Main Interface

### Status Card
- **Status**: Current state (Stopped, Running, Paused)
- **Session**: Duration of current session (HH:MM:SS)
- **Next action**: Countdown to next movement (seconds)

### Controls
- **▶️ Start**: Begin scheduled movements (or resume from pause)
- **⏸️ Pause**: Temporarily pause movements (keeps session active)
- **⏹️ Stop**: Stop completely (ends session, resets timer)

### Movement Interval
Choose how often the cursor should move:
- **15 seconds**: Very frequent (good for testing)
- **30 seconds**: Frequent
- **60 seconds**: Standard (default)
- **2 minutes**: Moderate
- **5 minutes**: Infrequent
- **Custom**: Set any value from 5-3600 seconds

### Keep-Awake Mode
- **Purpose**: Prevent Windows from going to sleep
- **Use case**: Long-running tasks, presentations, monitoring
- **How to enable**: Check "Enable Keep-Awake Mode"
- **Note**: Respects organization policies

---

## System Tray

### Minimizing to Tray
- Close the main window → app minimizes to system tray
- Change behavior in Settings → uncheck "Minimize to tray"

### Tray Menu
Right-click the tray icon to access:
- **Open Mouse Pilot**: Show main window
- **Start**: Begin movements
- **Pause**: Pause movements
- **Stop**: Stop movements
- **Exit**: Completely close application

### Tray Tooltip
Hover over the tray icon to see current status:
- "Mouse Pilot - Stopped"
- "Mouse Pilot - Running"
- "Mouse Pilot - Paused"

---

## Settings

Click **⚙️ Settings** to customize:

### Appearance
- **Theme**: Light or Dark mode
  - Light: Clean, bright interface
  - Dark: Easy on the eyes

### Mouse Movement
- **Movement Distance**: How far cursor moves (1-100 pixels)
  - Default: 5 pixels
  - Smaller = less noticeable
  - Larger = more apparent

- **Pause on Activity**: Pause when you move the mouse
  - Experimental feature
  - Prevents interference with your work

### System
- **Minimize to Tray**: Hide to tray when closing window
  - Enabled (default): App stays in tray
  - Disabled: Closing window exits app

- **Start with Windows**: Launch on system startup
  - Not yet implemented
  - Future feature

---

## Common Tasks

### Testing the Application
1. Set interval to **15 seconds**
2. Click **Start**
3. Watch the countdown
4. Observe cursor movement every 15 seconds
5. Click **Stop** when done testing

### Normal Usage
1. Set interval to **60 seconds** or **2 minutes**
2. Configure movement distance if desired
3. Enable Keep-Awake if needed
4. Click **Start**
5. Minimize to tray or close window
6. Work normally - movements happen in background

### During Meetings/Presentations
1. Enable **Keep-Awake Mode**
2. Set interval to **2 minutes** or **5 minutes**
3. Click **Start**
4. Minimize to tray
5. System stays awake, cursor movement is subtle

### Pausing for Manual Work
1. While running, click **⏸️ Pause**
2. Do your work (no automatic movements)
3. Click **▶️ Start** to resume
4. Session timer continues from where it was

---

## Keyboard Shortcuts

Currently, Mouse Pilot does not have keyboard shortcuts. All actions are performed through:
- Main window buttons
- System tray menu
- Settings dialog

*Future versions may include keyboard shortcuts.*

---

## Tips & Best Practices

### Choosing an Interval
- **Presentations**: 2-5 minutes (subtle, rare)
- **Monitoring**: 1-2 minutes (balanced)
- **Active work**: 30-60 seconds (frequent)
- **Testing**: 15-30 seconds (verification)

### Movement Distance
- **Subtle**: 3-5 pixels (barely noticeable)
- **Normal**: 5-10 pixels (slightly visible)
- **Obvious**: 10-20 pixels (clearly visible)

### Battery Considerations
- Keep-Awake prevents sleep → drains battery on laptops
- Disable Keep-Awake when not needed
- Consider longer intervals to reduce CPU usage

### Multiple Monitors
- Mouse Pilot respects screen boundaries
- Works seamlessly across all monitors
- Cursor returns to original position after movement

---

## Troubleshooting

### Cursor not moving
- **Check status**: Ensure it says "Running"
- **Verify interval**: Not too long to notice?
- **Screen corners**: Move cursor away from corners (failsafe)
- **Click Start**: Did you click the Start button?

### Application won't start
- **Python required**: Ensure Python 3.11+ installed (source version)
- **Dependencies**: Run `pip install -r requirements.txt`
- **Executable**: Download fresh copy if corrupted

### High CPU usage
- **Check interval**: Is it less than 5 seconds?
- **Restart app**: Close and reopen
- **Multiple instances**: Only run one copy

### Keep-Awake not working
- **Windows only**: Feature is Windows-specific
- **Permissions**: Some policies may prevent this
- **Verify enabled**: Check the checkbox is ticked

### Settings not saving
- **File permissions**: Check `%APPDATA%\MousePilot` is writable
- **Reset settings**: Delete `settings.json` to restore defaults
- **Location**: `C:\Users\[Username]\AppData\Roaming\MousePilot\settings.json`

---

## Data & Privacy

### What data is stored?
- **Settings file**: Local JSON file with your preferences
- **Location**: `%APPDATA%\MousePilot\settings.json`
- **Contents**: Theme, interval, distance, checkboxes

### What is NOT stored?
- No cursor positions
- No timestamps
- No usage statistics
- No personal information
- No telemetry

### Network activity
- **None**: Application never connects to the internet
- **Completely offline**: 100% local operation
- **No updates**: No automatic update checks

---

## Command Line (Advanced)

### Running from Source
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run application
python main.py
```

### Running Tests
```powershell
# Run all tests
pytest

# Verbose output
pytest -v

# Specific test file
pytest tests/test_scheduler.py
```

### Building Executable
```powershell
# Run build script
.\build.ps1

# Output location
.\dist\MousePilot.exe
```

---

## Support

- **Issues**: Report bugs on GitHub Issues
- **Questions**: Ask in GitHub Discussions
- **Documentation**: Read README.md

**Enjoy Mouse Pilot! 🖱️**
