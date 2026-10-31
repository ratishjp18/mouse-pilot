# 🎨 Mouse Pilot - Circular UI Guide

## Interface Layout

```
                 [−] [⚙]
              minimize settings


     [⏱]          🖱️          [☕]
   Interval      MOUSE      Keep-Awake
   (Click)     Stopped      (Toggle)
              00:00 timer
              00:00:00 session


           [▶] [⏸] [⏹]
          Start Pause Stop
```

---

## 🎯 Center Circle - Mouse Icon

**The main display area with blue circular border**

### What it shows:
- **🖱️ Mouse emoji** - The app icon
- **Status** - "Stopped", "Running", or "Paused"
- **Timer** - Countdown to next movement (MM:SS format)
- **Session** - Total session time (HH:MM:SS)

### What happens:
- Timer counts down when running
- Circular border can animate (future feature)
- Status changes color based on state

---

## ⏱ Left Circle - Interval Selector

**Click to change movement interval**

### Default intervals:
- 15 seconds
- 30 seconds
- 60 seconds (default)
- 2 minutes
- 5 minutes

### How to use:
1. **Click** the circular button
2. **Menu appears** with interval options
3. **Select** your preferred interval
4. **Button updates** to show selected time (e.g., "60s", "2m")

### Button display:
- Shows ⏱ emoji
- Shows current interval below (15s, 30s, 60s, 2m, 5m)

---

## ☕ Right Circle - Keep-Awake Toggle

**Click to toggle system keep-awake mode**

### What it does:
- **Prevents Windows from sleeping**
- Uses Windows power management APIs
- Keeps display and system active

### How to use:
1. **Click** the circular button to enable
2. Button turns **green** when active
3. **Click again** to disable
4. Button returns to **normal** color

### Use cases:
- Long presentations
- Video rendering
- Download monitoring
- Extended work sessions

---

## Top-Right Controls

### [−] Minimize Button
- **Click** to minimize to system tray
- App continues running in background
- **Double-click** tray icon to restore

### [⚙] Settings Button
- **Click** to open settings dialog
- Change:
  - Theme (Light/Dark)
  - Movement distance
  - Minimize behavior

---

## Bottom Controls (3 Circular Buttons)

### [▶] Start Button (Blue)
- **Starts** mouse movement
- **Resumes** from pause
- Enables Pause and Stop buttons
- Timer begins countdown

### [⏸] Pause Button (Blue)
- **Pauses** mouse movement temporarily
- Session continues
- Timer stops
- Click Start to resume

### [⏹] Stop Button (Red)
- **Stops** mouse movement completely
- Resets session timer
- Ends current session
- Returns to stopped state

---

## 🎮 Quick Usage Examples

### Example 1: Quick Test
```
1. Click [⏱] interval button → Select "15 seconds"
2. Click [▶] Start
3. Watch timer countdown from 00:15
4. Cursor moves every 15 seconds
5. Click [⏹] Stop when done
```

### Example 2: Normal Use
```
1. Leave interval at default (60s)
2. Click [▶] Start
3. Click [−] to minimize to tray
4. Work normally - movements happen automatically
5. Right-click tray icon → Stop when finished
```

### Example 3: Presentation Mode
```
1. Click [☕] Keep-Awake (turns green)
2. Click [⏱] → Select "5 minutes"
3. Click [▶] Start
4. Minimize window
5. System stays awake, subtle movements every 5 min
```

---

## 🎨 Visual States

### Stopped State
- Status: "Stopped"
- Timer: "--:--"
- Session: "00:00:00"
- Start button: Enabled (blue)
- Pause/Stop: Disabled (gray)

### Running State
- Status: "Running"
- Timer: Counting down (e.g., "00:45")
- Session: Counting up (e.g., "00:15:32")
- Start button: Disabled (gray)
- Pause/Stop: Enabled (blue/red)

### Paused State
- Status: "Paused"
- Timer: "--:--"
- Session: Frozen at pause time
- Start button: Enabled (to resume)
- Pause: Disabled
- Stop: Enabled

---

## 💡 Pro Tips

### Tip 1: Quick Interval Change
- Click interval button anytime (even while running)
- New interval takes effect immediately
- No need to stop and restart

### Tip 2: Silent Operation
- Minimize to tray for distraction-free operation
- Tray tooltip shows current status
- Right-click tray for quick controls

### Tip 3: Visual Feedback
- All buttons have hover effects
- Click effects provide tactile feedback
- Keep-Awake turns green when active

### Tip 4: Window Management
- Window is fixed size (700x700)
- Cannot be resized (maintains circular design)
- Always centered on screen

---

## 🎨 Theme Support

### Light Theme
- White background
- Blue accents (#0078D4)
- Clear, bright interface
- Perfect for daytime use

### Dark Theme
- Dark background (#1F1F1F)
- Cyan accents (#60CDFF)
- Easy on the eyes
- Perfect for night use

**Change in Settings → Theme → Light/Dark**

---

## 🔑 Keyboard Shortcuts

Currently, there are no keyboard shortcuts. All actions use mouse clicks on the circular interface.

*Future version may add shortcuts like:*
- Space = Start/Pause
- Escape = Stop
- 1-5 = Quick interval selection

---

## 📱 Window Behavior

- **Fixed size**: 700x700 pixels
- **Non-resizable**: Maintains perfect circle
- **Minimize**: Hides to system tray
- **Close**: Minimizes to tray (default) or exits
- **Taskbar**: Shows app icon and title

---

## 🎯 Design Philosophy

The circular design focuses on:
- **Simplicity**: Essential controls only
- **Clarity**: Large, obvious buttons
- **Aesthetics**: Modern, clean look
- **Functionality**: Everything one click away

**Mouse at center = main focus**
**Controls around = satellite actions**
**Circular = continuous operation**

---

Enjoy your new circular Mouse Pilot interface! 🖱️✨
