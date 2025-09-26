#!/usr/bin/env python3
"""
Basic usage example for CamRaw.

This example demonstrates how to:
1. Initialize the camera application
2. Capture a single image
3. Configure camera settings
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from camraw import CameraApp
from camraw.camera import CameraManager
from camraw.config import ConfigManager


def basic_capture_example():
    """Example: Basic image capture."""
    print("=== Basic Capture Example ===")
    
    try:
        # Initialize the camera app
        app = CameraApp(headless=True, debug=True)
        
        # The app will automatically initialize camera
        print("Camera app initialized")
        
        # Capture an image
        output_path = Path("captures/example_capture.jpg")
        success = app.camera_manager.capture_image(output_path)
        
        if success:
            print(f"Image captured successfully: {output_path}")
        else:
            print("Failed to capture image")
        
        # Cleanup
        app.cleanup()
        
    except Exception as e:
        print(f"Error: {e}")


def camera_settings_example():
    """Example: Configuring camera settings."""
    print("\n=== Camera Settings Example ===")
    
    try:
        # Initialize components
        config_manager = ConfigManager()
        camera_manager = CameraManager(config_manager)
        
        if not camera_manager.initialize():
            print("Failed to initialize camera")
            return
        
        # Get current settings
        current_settings = camera_manager.get_camera_settings()
        print(f"Current settings: {current_settings}")
        
        # Update settings
        new_settings = {
            "iso": 400,
            "exposure": -20,
            "resolution": (1280, 720)
        }
        
        success = camera_manager.update_camera_settings(new_settings)
        if success:
            print(f"Settings updated: {new_settings}")
            
            # Get updated settings
            updated_settings = camera_manager.get_camera_settings()
            print(f"Updated settings: {updated_settings}")
        else:
            print("Failed to update settings")
        
        # Cleanup
        camera_manager.cleanup()
        
    except Exception as e:
        print(f"Error: {e}")


def config_example():
    """Example: Working with configuration."""
    print("\n=== Configuration Example ===")
    
    try:
        config = ConfigManager()
        
        # Get configuration values
        print(f"Default camera device: {config.get('camera.default_device_id')}")
        print(f"Output directory: {config.get('capture.output_directory')}")
        print(f"Image quality: {config.get('capture.image_quality')}")
        
        # Modify configuration
        config.set('capture.image_quality', 85)
        config.set('camera.default_fps', 60)
        
        # Save configuration
        if config.save_config():
            print("Configuration saved successfully")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("CamRaw Usage Examples")
    print("=" * 40)
    
    basic_capture_example()
    camera_settings_example() 
    config_example()
    
    print("\nExamples completed!")