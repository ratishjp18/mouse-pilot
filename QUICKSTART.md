# 🚀 Mouse Pilot - Quick Start Guide

## For End Users

### Using the Executable (Recommended)

1. **Download** `MousePilot.exe` from releases
2. **Run** the executable (no installation needed)
3. **Select interval** (default: 60 seconds)
4. **Click Start** ▶️
5. **Minimize** to system tray

### Pinning to Taskbar

1. Navigate to the folder containing `MousePilot.exe`
2. Right-click `MousePilot.exe`
3. Select **"Pin to taskbar"**
4. Launch from taskbar anytime

---

## For Developers

### Setup Development Environment

```powershell
# Clone repository
git clone https://github.com/yourusername/mouse-pilot.git
cd mouse-pilot

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create icon
python create_icon.py

# Run application
python main.py
```

### Run Tests

```powershell
.\venv\Scripts\Activate.ps1
pytest -v
```

### Build Executable

```powershell
.\venv\Scripts\Activate.ps1
.\build.ps1
```

**Output**: `dist\MousePilot.exe` (approx. 60 MB)

---

## Command Reference

### Launch Application
```powershell
# From source
python main.py

# From executable
.\dist\MousePilot.exe
```

### Testing
```powershell
# Run all tests
pytest

# With coverage
pytest --cov=services --cov=ui

# Verbose
pytest -v
```

### Building
```powershell
# Full build
.\build.ps1

# Manual PyInstaller
pyinstaller --name=MousePilot --onefile --windowed --icon=assets\icon.ico main.py
```

---

## Essential Files

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `requirements.txt` | Python dependencies |
| `build.ps1` | Build executable script |
| `assets/icon.ico` | Application icon |
| `README.md` | Full documentation |
| `USAGE.md` | User guide |
| `CONTRIBUTING.md` | Developer guide |

---

## Key Features

✅ **Scheduled Movement** - 15s to 5 minutes  
✅ **System Tray** - Minimize to tray  
✅ **Keep-Awake** - Prevent sleep  
✅ **Dark/Light Theme** - Your choice  
✅ **No Telemetry** - 100% private  
✅ **Pin to Taskbar** - Quick access  

---

## Troubleshooting

### Won't start
```powershell
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests fail
```powershell
# Clean and reinstall
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Build fails
```powershell
# Clean build artifacts
Remove-Item -Recurse -Force build, dist
Remove-Item -Force MousePilot.spec

# Rebuild
.\build.ps1
```

---

## Next Steps

1. ⭐ **Star** the repository
2. 📖 Read [USAGE.md](USAGE.md) for detailed guide
3. 🐛 Report issues on GitHub
4. 💡 Suggest features
5. 🤝 Contribute (see [CONTRIBUTING.md](CONTRIBUTING.md))

---

**Happy Piloting! 🖱️**
