"""
Camera manager for handling camera operations.
"""

import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

from .device import CameraDevice
from ..config import ConfigManager


class CameraManager:
    """Manages camera devices and operations."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize camera manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self.current_camera: Optional[CameraDevice] = None
        self.available_cameras: List[CameraDevice] = []
        
    def initialize(self) -> bool:
        """
        Initialize the camera manager and detect available cameras.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing camera manager")
            self._detect_cameras()
            
            if self.available_cameras:
                # Use first available camera by default
                self.current_camera = self.available_cameras[0]
                return self.current_camera.open()
            else:
                self.logger.warning("No cameras detected")
                return False
                
        except Exception as e:
            self.logger.error(f"Camera initialization failed: {e}")
            return False
    
    def _detect_cameras(self) -> None:
        """Detect available camera devices."""
        self.logger.info("Detecting available cameras")
        self.available_cameras.clear()
        
        # Try to detect cameras (placeholder implementation)
        # In a real implementation, this would use OpenCV or similar
        for camera_id in range(3):  # Check first 3 camera indices
            try:
                camera = CameraDevice(camera_id)
                if camera.is_available():
                    self.available_cameras.append(camera)
                    self.logger.info(f"Found camera: {camera.name}")
            except Exception as e:
                self.logger.debug(f"Camera {camera_id} not available: {e}")
    
    def get_available_cameras(self) -> List[CameraDevice]:
        """Get list of available cameras."""
        return self.available_cameras.copy()
    
    def select_camera(self, camera_id: int) -> bool:
        """
        Select a specific camera by ID.
        
        Args:
            camera_id: Camera device ID
            
        Returns:
            True if camera selected successfully
        """
        try:
            for camera in self.available_cameras:
                if camera.device_id == camera_id:
                    if self.current_camera:
                        self.current_camera.close()
                    
                    self.current_camera = camera
                    return self.current_camera.open()
            
            self.logger.warning(f"Camera {camera_id} not found")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to select camera {camera_id}: {e}")
            return False
    
    def capture_image(self, output_path: Path) -> bool:
        """
        Capture an image and save to file.
        
        Args:
            output_path: Path to save the captured image
            
        Returns:
            True if capture successful
        """
        if not self.current_camera:
            self.logger.error("No camera selected")
            return False
        
        try:
            return self.current_camera.capture_image(output_path)
        except Exception as e:
            self.logger.error(f"Image capture failed: {e}")
            return False
    
    def start_preview(self) -> bool:
        """Start camera preview."""
        if not self.current_camera:
            self.logger.error("No camera selected")
            return False
        
        try:
            return self.current_camera.start_preview()
        except Exception as e:
            self.logger.error(f"Failed to start preview: {e}")
            return False
    
    def stop_preview(self) -> None:
        """Stop camera preview."""
        if self.current_camera:
            self.current_camera.stop_preview()
    
    def get_camera_settings(self) -> Dict[str, Any]:
        """Get current camera settings."""
        if self.current_camera:
            return self.current_camera.get_settings()
        return {}
    
    def update_camera_settings(self, settings: Dict[str, Any]) -> bool:
        """Update camera settings."""
        if self.current_camera:
            return self.current_camera.update_settings(settings)
        return False
    
    def cleanup(self) -> None:
        """Clean up camera resources."""
        self.logger.info("Cleaning up camera manager")
        
        if self.current_camera:
            self.current_camera.close()
            self.current_camera = None
        
        for camera in self.available_cameras:
            camera.close()
        
        self.available_cameras.clear()