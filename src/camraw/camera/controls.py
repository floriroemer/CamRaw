"""
Camera controls for manual camera settings.
"""

import logging
from typing import Dict, Any, Optional, Tuple
from enum import Enum


class WhiteBalanceMode(Enum):
    """White balance modes."""
    AUTO = "auto"
    DAYLIGHT = "daylight"
    CLOUDY = "cloudy"
    TUNGSTEN = "tungsten"
    FLUORESCENT = "fluorescent"
    FLASH = "flash"


class FocusMode(Enum):
    """Focus modes."""
    AUTO = "auto"
    MANUAL = "manual"
    INFINITY = "infinity"
    MACRO = "macro"


class CameraControls:
    """Provides high-level camera control interface."""
    
    def __init__(self, camera_device):
        """
        Initialize camera controls.
        
        Args:
            camera_device: CameraDevice instance to control
        """
        self.camera_device = camera_device
        self.logger = logging.getLogger(__name__)
    
    def set_exposure(self, value: int) -> bool:
        """
        Set camera exposure.
        
        Args:
            value: Exposure value (-100 to 100, 0 = auto)
            
        Returns:
            True if set successfully
        """
        if not -100 <= value <= 100:
            self.logger.error(f"Invalid exposure value: {value}")
            return False
        
        return self.camera_device.update_settings({"exposure": value})
    
    def set_iso(self, value: int) -> bool:
        """
        Set camera ISO sensitivity.
        
        Args:
            value: ISO value (100, 200, 400, 800, 1600, 3200, etc.)
            
        Returns:
            True if set successfully
        """
        valid_iso_values = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
        
        if value not in valid_iso_values:
            self.logger.error(f"Invalid ISO value: {value}")
            return False
        
        return self.camera_device.update_settings({"iso": value})
    
    def set_white_balance(self, mode: WhiteBalanceMode) -> bool:
        """
        Set white balance mode.
        
        Args:
            mode: White balance mode
            
        Returns:
            True if set successfully
        """
        return self.camera_device.update_settings({"white_balance": mode.value})
    
    def set_focus_mode(self, mode: FocusMode) -> bool:
        """
        Set focus mode.
        
        Args:
            mode: Focus mode
            
        Returns:
            True if set successfully
        """
        return self.camera_device.update_settings({"focus": mode.value})
    
    def set_resolution(self, width: int, height: int) -> bool:
        """
        Set camera resolution.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            True if set successfully
        """
        # Common resolutions
        valid_resolutions = [
            (640, 480),    # VGA
            (1280, 720),   # HD
            (1920, 1080),  # Full HD
            (2560, 1440),  # QHD
            (3840, 2160),  # 4K UHD
        ]
        
        resolution = (width, height)
        if resolution not in valid_resolutions:
            self.logger.warning(f"Non-standard resolution: {resolution}")
        
        return self.camera_device.update_settings({"resolution": resolution})
    
    def set_fps(self, fps: int) -> bool:
        """
        Set camera frame rate.
        
        Args:
            fps: Frames per second (15, 30, 60, etc.)
            
        Returns:
            True if set successfully
        """
        valid_fps = [15, 24, 30, 60, 120]
        
        if fps not in valid_fps:
            self.logger.warning(f"Non-standard FPS: {fps}")
        
        return self.camera_device.update_settings({"fps": fps})
    
    def get_current_settings(self) -> Dict[str, Any]:
        """
        Get current camera settings.
        
        Returns:
            Dictionary of current settings
        """
        return self.camera_device.get_settings()
    
    def reset_to_defaults(self) -> bool:
        """
        Reset camera settings to defaults.
        
        Returns:
            True if reset successfully
        """
        default_settings = {
            "exposure": 0,
            "iso": 100,
            "white_balance": WhiteBalanceMode.AUTO.value,
            "focus": FocusMode.AUTO.value,
            "resolution": (1920, 1080),
            "fps": 30
        }
        
        return self.camera_device.update_settings(default_settings)
    
    def get_supported_resolutions(self) -> list[Tuple[int, int]]:
        """
        Get list of supported resolutions.
        
        Returns:
            List of (width, height) tuples
        """
        return [
            (640, 480),    # VGA
            (1280, 720),   # HD
            (1920, 1080),  # Full HD
            (2560, 1440),  # QHD
            (3840, 2160),  # 4K UHD
        ]
    
    def get_supported_fps(self) -> list[int]:
        """
        Get list of supported frame rates.
        
        Returns:
            List of supported FPS values
        """
        return [15, 24, 30, 60, 120]