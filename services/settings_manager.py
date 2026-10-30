"""
Settings Manager for Mouse Pilot
Handles loading and saving application settings to JSON
"""

import json
import os
from pathlib import Path


class SettingsManager:
    """Manage application settings with local JSON storage"""
    
    def __init__(self):
        self.settings_file = self._get_settings_path()
        self.settings = self._load_settings()
    
    def _get_settings_path(self):
        """Get the path to the settings file in AppData"""
        app_data = os.getenv('APPDATA')
        if app_data:
            settings_dir = Path(app_data) / "MousePilot"
            settings_dir.mkdir(exist_ok=True)
            return settings_dir / "settings.json"
        else:
            # Fallback to current directory
            return Path("mouse_pilot_settings.json")
    
    def _load_settings(self):
        """Load settings from file or create defaults"""
        default_settings = {
            "theme": "light",
            "interval": 60,
            "movement_distance": 5,
            "pause_on_activity": False,
            "minimize_to_tray": True,
            "start_with_windows": False,
            "keep_awake": False
        }
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded_settings)
            except Exception as e:
                print(f"Error loading settings: {e}")
        
        return default_settings
    
    def save(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
    
    def get_all_settings(self):
        """Get all settings as a dictionary"""
        return self.settings.copy()
