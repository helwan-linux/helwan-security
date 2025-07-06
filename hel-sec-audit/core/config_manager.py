# core/config_manager.py
# Manages application configuration settings safely for installed environments.

import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_filename="config.json"):
        # مسار إعدادات المستخدم: ~/.config/hel-sec-audit/config.json
        config_dir = Path.home() / ".config" / "hel-sec-audit"
        config_dir.mkdir(parents=True, exist_ok=True)

        self.config_path = config_dir / config_filename

        self.default_config = {
            "checks_enabled": {
                "System Updates Status": True,
                "Weak Password Policies/Usage": True,
                "Open Network Ports": True,
                "Firewall Status": True
            },
            "general_settings": {
                "dark_mode": False
            }
        }

        self.config = self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    loaded_config = json.load(f)
                    merged_config = self.default_config.copy()
                    for key, value in loaded_config.items():
                        if isinstance(value, dict) and key in merged_config:
                            merged_config[key].update(value)
                        else:
                            merged_config[key] = value
                    return merged_config
            except json.JSONDecodeError:
                print(f"Warning: Corrupted config file '{self.config_path}'. Using default settings.")
                return self.default_config
        return self.default_config

    def save_config(self):
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config file: {e}")

    def get_setting(self, category, key):
        return self.config.get(category, {}).get(key)

    def set_setting(self, category, key, value):
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = value
        self.save_config()

    def get_all_check_settings(self):
        return self.config.get("checks_enabled", {})
    
    def set_check_enabled(self, check_name, enabled):
        if "checks_enabled" not in self.config:
            self.config["checks_enabled"] = {}
        self.config["checks_enabled"][check_name] = enabled
        self.save_config()
