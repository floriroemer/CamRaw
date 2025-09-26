"""
Configuration management for CamRaw.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        self._config = self._load_default_config()
        
        # Load configuration from file if exists
        if self.config_path.exists():
            self.load_config()
        else:
            # Create default config file
            self.save_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            "camera": {
                "default_device_id": 0,
                "default_resolution": [1920, 1080],
                "default_fps": 30,
                "auto_exposure": True,
                "auto_white_balance": True,
                "default_iso": 100
            },
            "capture": {
                "output_directory": "captures",
                "filename_format": "IMG_%Y%m%d_%H%M%S",
                "image_format": "jpg",
                "image_quality": 95,
                "auto_save": True
            },
            "ui": {
                "theme": "light",
                "show_histogram": True,
                "show_grid_overlay": False,
                "preview_size": [640, 480],
                "control_panel_position": "right"
            },
            "processing": {
                "enable_raw_processing": False,
                "auto_enhance": False,
                "noise_reduction": False,
                "sharpening": 0
            },
            "general": {
                "log_level": "INFO",
                "auto_detect_cameras": True,
                "check_for_updates": True
            }
        }
    
    def load_config(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            True if loaded successfully
        """
        try:
            self.logger.info(f"Loading configuration from {self.config_path}")
            
            with open(self.config_path, 'r') as f:
                loaded_config = yaml.safe_load(f)
            
            if loaded_config:
                # Merge loaded config with defaults
                self._merge_config(self._config, loaded_config)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            True if saved successfully
        """
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Saving configuration to {self.config_path}")
            
            with open(self.config_path, 'w') as f:
                yaml.dump(self._config, f, default_flow_style=False, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., "camera.default_fps")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        try:
            keys = key.split('.')
            value = self._config
            
            for k in keys:
                value = value[k]
            
            return value
            
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config_dict = self._config
        
        # Navigate to the correct nested dictionary
        for k in keys[:-1]:
            if k not in config_dict:
                config_dict[k] = {}
            config_dict = config_dict[k]
        
        # Set the value
        config_dict[keys[-1]] = value
    
    def _merge_config(self, default_config: Dict, loaded_config: Dict) -> None:
        """
        Recursively merge loaded configuration with default configuration.
        
        Args:
            default_config: Default configuration dictionary
            loaded_config: Loaded configuration dictionary
        """
        for key, value in loaded_config.items():
            if key in default_config and isinstance(default_config[key], dict) and isinstance(value, dict):
                self._merge_config(default_config[key], value)
            else:
                default_config[key] = value
    
    def get_camera_config(self) -> Dict[str, Any]:
        """Get camera-related configuration."""
        return self.get("camera", {})
    
    def get_capture_config(self) -> Dict[str, Any]:
        """Get capture-related configuration."""
        return self.get("capture", {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI-related configuration."""
        return self.get("ui", {})