# Build Script for Mouse Pilot
# This script builds the Windows executable using PyInstaller

Write-Host "Building Mouse Pilot..." -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup first." -ForegroundColor Red
    Write-Host "Run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Check if icon exists
if (!(Test-Path "assets\icon.ico")) {
    Write-Host "Warning: assets\icon.ico not found. Building without custom icon." -ForegroundColor Yellow
}

# Clean previous build
Write-Host "Cleaning previous build..." -ForegroundColor Green
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "MousePilot.spec") { Remove-Item -Force "MousePilot.spec" }

# Build with PyInstaller
Write-Host "Building executable with PyInstaller..." -ForegroundColor Green

$iconArg = ""
if (Test-Path "assets\icon.ico") {
    $iconArg = "--icon=assets\icon.ico"
}

pyinstaller --name=MousePilot `
    --onefile `
    --windowed `
    $iconArg `
    --add-data "assets;assets" `
    --hidden-import=PySide6.QtCore `
    --hidden-import=PySide6.QtGui `
    --hidden-import=PySide6.QtWidgets `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nBuild successful!" -ForegroundColor Green
    Write-Host "Executable location: .\dist\MousePilot.exe" -ForegroundColor Cyan
    Write-Host "`nTo pin to taskbar:" -ForegroundColor Yellow
    Write-Host "1. Navigate to .\dist\ folder" -ForegroundColor White
    Write-Host "2. Right-click MousePilot.exe" -ForegroundColor White
    Write-Host "3. Select 'Pin to taskbar'" -ForegroundColor White
} else {
    Write-Host "`nBuild failed!" -ForegroundColor Red
    exit 1
}
