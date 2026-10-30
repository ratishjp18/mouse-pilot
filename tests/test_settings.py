"""
Tests for Settings Manager
"""

import pytest
import json
import os
from pathlib import Path
from services.settings_manager import SettingsManager


def test_settings_manager_defaults():
    """Test that settings manager loads default values"""
    manager = SettingsManager()
    settings = manager.get_all_settings()
    
    assert settings["theme"] in ["light", "dark"]
    assert isinstance(settings["interval"], int)
    assert settings["interval"] > 0
    assert isinstance(settings["movement_distance"], int)
    assert isinstance(settings["pause_on_activity"], bool)
    assert isinstance(settings["minimize_to_tray"], bool)


def test_settings_get_set():
    """Test getting and setting individual values"""
    manager = SettingsManager()
    
    manager.set("theme", "dark")
    assert manager.get("theme") == "dark"
    
    manager.set("interval", 120)
    assert manager.get("interval") == 120
    
    manager.set("movement_distance", 10)
    assert manager.get("movement_distance") == 10


def test_settings_persistence(tmp_path):
    """Test that settings persist to file"""
    # Create a temporary settings file
    settings_file = tmp_path / "test_settings.json"
    
    # Create manager and modify settings file path
    manager = SettingsManager()
    manager.settings_file = settings_file
    
    # Set some values
    manager.set("theme", "dark")
    manager.set("interval", 90)
    manager.save()
    
    # Verify file was created
    assert settings_file.exists()
    
    # Load settings in a new manager
    manager2 = SettingsManager()
    manager2.settings_file = settings_file
    manager2.settings = manager2._load_settings()
    
    # Verify values persisted
    assert manager2.get("theme") == "dark"
    assert manager2.get("interval") == 90
